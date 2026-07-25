from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from .graph_builders import (
    VISUAL_ASSET_MANIFEST_SCHEMA,
    VISUAL_IMAGE_GENERATOR_ID,
)
from .utils import write_json


PROMPT_PACKET_SCHEMA = "design-ontology.visual-prompt-packet.v1"
PROMPT_CONTRACT_MIGRATION_SCHEMA = "visual-asset-prompt-contract-migration/v1"
FINAL_GENERATED_STATUSES = {"accepted", "integrated"}

SPECIALIZED_SLOT_TERMS = {
    "editorial-cover": ("editorial", "article", "magazine", "press", "publishing", "case study", "편집", "기사", "잡지", "출판", "사례"),
    "comic-cover": ("comic", "manga", "webtoon", "만화", "웹툰", "코믹"),
    "comic-panel-preview": ("comic", "manga", "webtoon", "panel", "만화", "웹툰", "연재"),
}


@dataclass(slots=True)
class VisualPromptOutput:
    packet_path: Path
    markdown_path: Path
    manifest_path: Path
    prompt_count: int


def build_visual_prompt_packet(
    *,
    brand_profile: dict[str, Any],
    blueprint: dict[str, Any],
    ontology: dict[str, Any],
    candidates_per_slot: int = 3,
    project_dir: Path | None = None,
) -> dict[str, Any]:
    """Turn ontology visual slots into tool-neutral, imagegen-ready prompt briefs."""
    if candidates_per_slot < 1 or candidates_per_slot > 4:
        raise ValueError("candidates_per_slot must be between 1 and 4")

    brand_name = str(brand_profile.get("brand_name") or "Product")
    product_summary = str(brand_profile.get("product_summary") or "").strip()
    concept = brand_profile.get("application_concept") or {}
    layout = brand_profile.get("layout_skeleton") or {}
    differentiation = brand_profile.get("design_differentiation") or {}
    domain = product_summary or str(concept.get("primary_job") or "professional digital product")
    palette = _palette_summary(blueprint)
    visual_cues = _visual_cues(blueprint, brand_profile)
    concept_context = _concept_context(concept, layout, differentiation)
    product_avoid = _product_avoid_constraints(layout, differentiation)
    design_references = _project_design_references(project_dir)
    anti_keywords = _string_list(
        brand_profile.get("anti_keywords")
        or brand_profile.get("brand_anti_keywords")
        or []
    )

    slots = []
    for node in ontology.get("nodes", []):
        if node.get("type") != "GeneratedVisualAsset":
            continue
        meta = node.get("meta") or {}
        if meta.get("status") not in {None, "promptable", "planned"}:
            continue
        slot = str(meta.get("slot") or node.get("id", "visual").split(":")[-1])
        if not _slot_matches_domain(slot, brand_profile, domain):
            continue
        if _slot_conflicts_with_layout(slot, layout):
            continue
        ratios = _string_list(meta.get("aspect_ratios") or ["4:3"])
        visual_scope = str(meta.get("visual_scope") or "runtime-support")
        generation_status = "ready"
        brief_references = (
            design_references if visual_scope == "design-reference-only" else []
        )
        brief = {
            "id": node.get("id") or f"visual-asset:{slot}",
            "slot": slot,
            "label": node.get("label") or slot.replace("-", " ").title(),
            "purpose": meta.get("usage") or "Brand-aligned product visual",
            "intended_for": _edge_targets(ontology, node.get("id")),
            "aspect_ratios": ratios,
            "candidate_count": candidates_per_slot,
            "visual_scope": visual_scope,
            "active_generation": True,
            "design_references": brief_references,
            "prompt": _compose_prompt(
                brand_name=brand_name,
                domain=domain,
                slot=slot,
                purpose=str(meta.get("usage") or "product visual"),
                palette=palette,
                visual_cues=visual_cues,
                anti_keywords=anti_keywords,
                product_avoid=product_avoid,
                concept_context=concept_context,
                visual_scope=visual_scope,
                design_references=brief_references,
            ),
            "negative_constraints": _dedupe([
                "no logos or third-party trademarks",
                "no generic SaaS gradient or stock-photo staging",
                "no emoji, watermark, or decorative UI chrome",
                *([] if visual_scope == "design-reference-only" else ["no readable interface text embedded in the image"]),
                *product_avoid,
                *anti_keywords,
            ]),
            "composition_constraints": _composition_constraints(
                visual_scope=visual_scope,
                concept_context=concept_context,
                design_references=brief_references,
            ),
            "review_criteria": [
                "domain subject is immediately recognizable",
                "visual language matches the design tokens and component surfaces",
                "asset adds product meaning rather than atmosphere alone",
                "crop works at every declared aspect ratio",
                "no accidental text, logos, anatomy defects, or misleading product state",
            ],
            "generation": {
                "preferred_tool": "Codex/GPT built-in image generation",
                "api_fallback": "disabled",
                "status": generation_status,
            },
        }
        slots.append(brief)

    return {
        "schema_version": PROMPT_PACKET_SCHEMA,
        "brand": brand_name,
        "domain_context": domain,
        "prompt_basis": [
            "brand_profile.json",
            "design_system_blueprint.json",
            "system_ontology.json",
        ],
        "palette_context": palette,
        "visual_cues": visual_cues,
        "concept_context": concept_context,
        "design_references": design_references,
        "slots": slots,
    }


def write_visual_prompt_outputs(
    output_dir: Path,
    packet: dict[str, Any],
) -> VisualPromptOutput:
    output_dir.mkdir(parents=True, exist_ok=True)
    packet_path = output_dir / "imagegen-prompt-packet.json"
    markdown_path = output_dir / "imagegen-prompts.md"
    manifest_path = output_dir / "manifest.json"
    existing_manifest = None
    if manifest_path.exists():
        try:
            existing_manifest = load_json_object(manifest_path)
        except (json.JSONDecodeError, ValueError) as exc:
            raise ValueError(
                f"Existing visual asset manifest is invalid and was not overwritten: {manifest_path}"
            ) from exc
    packet, source_packets = _with_legacy_prompt_contract_slots(
        packet,
        output_dir=output_dir,
        existing_manifest=existing_manifest,
    )
    packet_bytes = _json_bytes(packet)
    prompt_packet_sha256 = hashlib.sha256(packet_bytes).hexdigest()
    migration_archives = _prepare_prompt_contract_archives(
        packet=packet,
        existing_manifest=existing_manifest,
        source_packets=source_packets,
        output_dir=output_dir,
        prompt_packet_sha256=prompt_packet_sha256,
    )
    packet_path.write_bytes(packet_bytes)
    markdown_path.write_text(_render_markdown(packet), encoding="utf-8")
    write_json(
        manifest_path,
        _manifest_template(
            packet,
            existing_manifest,
            prompt_packet_sha256=prompt_packet_sha256,
            migration_archives=migration_archives,
        ),
    )
    return VisualPromptOutput(
        packet_path,
        markdown_path,
        manifest_path,
        sum(1 for slot in packet.get("slots", []) if slot.get("active_generation") is not False),
    )


def load_json_object(path: Path) -> dict[str, Any]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ValueError(f"Expected a JSON object: {path}")
    return payload


def _compose_prompt(**context: Any) -> str:
    anti = ", ".join(context["anti_keywords"]) or "generic AI imagery"
    cues = ", ".join(context["visual_cues"]) or "restrained production-grade art direction"
    concept = "; ".join(context["concept_context"]) or "keep the product workflow concrete"
    avoid = ", ".join(context["product_avoid"]) or "generic layout defaults"
    references = context.get("design_references") or []
    reference_note = ""
    if references:
        reference_note = (
            " A selected local visual direction is available as a morphology-only reference: "
            + "; ".join(
                f"{item['path']} ({item['role']})" for item in references
            )
            + ". Do not copy its palette, typography, text, logos, or images."
        )
    if context["visual_scope"] == "design-reference-only":
        return (
            f"High-fidelity production UI direction for {context['brand_name']}, a {context['domain']} product. "
            f"Create a concrete {context['slot']} design reference for: {context['purpose']}. "
            f"The product facts are: {concept}. Use {context['palette']}; reflect {cues}. "
            "Show a compact operation header, date/group/team/status filters, a dense fixture comparison table, "
            "and a persistent selected-match rail that connects match detail, prediction, source state, and fan "
            "discussion. The fixture workflow must occupy the first viewport before any imagery. "
            "Use practical Korean sports-data UI hierarchy and real interface affordances, but leave exact runtime "
            "copy to the implementation. This is a design-reference mockup, not an in-product hero asset. "
            f"Avoid {avoid}, {anti}, betting controls, casino cues, oversized stadium art, and uniform card walls."
            f"{reference_note}"
        )
    return (
        f"Professional production supporting visual for {context['brand_name']}, a {context['domain']} product. "
        f"Create a concrete {context['slot']} asset for: {context['purpose']}. "
        f"The product facts are: {concept}. Use {context['palette']}; reflect {cues}. "
        "Show domain-specific subject matter and believable materials, lighting, scale, and context. "
        "This asset appears only after the fixture filters, schedule table, and selected-match rail; it must add "
        "context rather than replace product data. Compose for responsive UI cropping with calm negative space. "
        f"Avoid {avoid}, {anti}, logos, readable text, stock-photo clichés, generic gradients, fake interface "
        "screenshots, betting language, and decorative card walls."
    )


def _concept_context(
    concept: dict[str, Any],
    layout: dict[str, Any],
    differentiation: dict[str, Any],
) -> list[str]:
    context: list[str] = []
    for value in (
        concept.get("primary_job"),
        concept.get("operating_mode"),
        layout.get("composition"),
    ):
        if isinstance(value, str) and value.strip():
            context.append(value.strip())
    for value in layout.get("first_screen_contract", []) if isinstance(layout, dict) else []:
        if isinstance(value, str) and value.strip():
            context.append(value.strip())
    for value in differentiation.get("signature_moves", []) if isinstance(differentiation, dict) else []:
        if isinstance(value, str) and value.strip():
            context.append(value.strip())
    return _dedupe(context)[:8]


def _product_avoid_constraints(
    layout: dict[str, Any],
    differentiation: dict[str, Any],
) -> list[str]:
    values: list[str] = []
    for source, key in (
        (layout, "avoid_layouts"),
        (differentiation, "must_feel_different_from"),
        (differentiation, "repetition_risks"),
    ):
        if not isinstance(source, dict):
            continue
        values.extend(_string_list(source.get(key)))
    return _dedupe(values)


def _slot_conflicts_with_layout(slot: str, layout: dict[str, Any]) -> bool:
    avoids = " ".join(_string_list(layout.get("avoid_layouts"))).casefold()
    if slot == "hero-image":
        return "hero" in avoids
    if slot == "card-thumbnail":
        return "card grid" in avoids or "decorative card" in avoids
    return False


def _composition_constraints(
    *,
    visual_scope: str,
    concept_context: list[str],
    design_references: list[dict[str, str]],
) -> list[str]:
    if visual_scope == "design-reference-only":
        constraints = [
            "start the first viewport with filters and a dense fixture comparison table",
            "keep one selected match visibly synchronized with the contextual rail",
            "show source, data mode, freshness, and verification near the related data",
            "do not place an image, hero, or KPI-card wall before the fixture workflow",
            "keep schedule scan and selected-match rail readable at desktop and mobile crops",
        ]
        if design_references:
            constraints.append(
                "use the selected local direction only for thin rules, calm surfaces, asymmetric rail, and selection linkage"
            )
        return constraints
    return [
        "preserve a clear focal subject at desktop and mobile crops",
        "leave calm negative space near likely contextual copy",
        "keep important subjects away from crop-sensitive edges",
        "never displace the fixture table or selected-match rail from the primary workflow",
        *(
            ["reflect the accepted fixture-led workflow context"]
            if concept_context
            else []
        ),
    ]


def _project_design_references(project_dir: Path | None) -> list[dict[str, str]]:
    if project_dir is None:
        return []
    reference_dir = project_dir / "design-system" / "references"
    if not reference_dir.is_dir():
        return []
    references: list[dict[str, str]] = []
    for image_path in sorted(reference_dir.glob("selected-direction-*.png")):
        references.append(
            {
                "path": image_path.relative_to(project_dir).as_posix(),
                "sha256": _sha256(image_path),
                "role": "morphology, density, contextual-rail, and selection-linkage reference only",
            }
        )
    return references


def _palette_summary(blueprint: dict[str, Any]) -> str:
    palette = blueprint.get("active_palette") or blueprint.get("palette") or {}
    if not palette:
        color_reference = blueprint.get("color_reference") or {}
        palette = color_reference.get("palette_roles") or color_reference.get("active_palette") or {}
    if isinstance(palette, dict):
        pairs = []
        for key, value in palette.items():
            if isinstance(value, dict):
                value = value.get("hex") or value.get("value")
            if isinstance(value, str):
                pairs.append(f"{key} {value}")
            if len(pairs) >= 8:
                break
        if pairs:
            return "a controlled palette of " + ", ".join(pairs)
    return "the semantic palette defined by the design system"


def _visual_cues(blueprint: dict[str, Any], brand_profile: dict[str, Any]) -> list[str]:
    cues: list[str] = []
    for source in (
        {"visual_motifs": blueprint.get("visual_language") or {}},
        blueprint.get("visual_reference") or {},
        brand_profile.get("_resolved_visual_reference") or {},
    ):
        if not isinstance(source, dict):
            continue
        motifs = source.get("visual_motifs") or {}
        if isinstance(motifs, dict):
            for key in ("density", "surface_style", "image_treatment", "composition"):
                value = motifs.get(key)
                if isinstance(value, dict):
                    value = value.get("value")
                if isinstance(value, str) and value:
                    cues.append(f"{key.replace('_', ' ')}: {value}")
    return _dedupe(cues)[:8]


def _edge_targets(ontology: dict[str, Any], source_id: Any) -> list[str]:
    return [
        str(edge["target"])
        for edge in ontology.get("edges", [])
        if edge.get("type") == "intended_for" and edge.get("source") == source_id and edge.get("target")
    ]


def _slot_matches_domain(slot: str, brand_profile: dict[str, Any], domain: str) -> bool:
    required_terms = SPECIALIZED_SLOT_TERMS.get(slot)
    if not required_terms:
        return True
    concept = brand_profile.get("application_concept") or {}
    haystack = " ".join([
        domain,
        " ".join(_string_list(brand_profile.get("brand_keywords") or [])),
        " ".join(_string_list(brand_profile.get("visual_keywords") or [])),
        " ".join(_string_list(concept.get("domain_objects") or [])),
    ]).lower()
    return any(term in haystack for term in required_terms)


def _string_list(value: Any) -> list[str]:
    if isinstance(value, str):
        return [value]
    if isinstance(value, list):
        return [str(item) for item in value if item]
    return []


def _dedupe(values: list[str]) -> list[str]:
    return list(dict.fromkeys(value.strip() for value in values if value and value.strip()))


def _render_markdown(packet: dict[str, Any]) -> str:
    lines = [
        "# Image Generation Prompt Pack",
        "",
        f"Brand: {packet.get('brand', 'Product')}",
        f"Domain context: {packet.get('domain_context', '')}",
        "",
        "Use the built-in Codex/GPT image generation capability. Review candidates before copying accepted assets into the application workspace.",
    ]
    active_index = 0
    for slot in packet.get("slots", []):
        active = slot.get("active_generation") is not False
        if active:
            active_index += 1
        heading = (
            f"## {active_index}. {slot['label']}"
            if active
            else f"## Preserved historic prompt contract — {slot['label']}"
        )
        lines.extend([
            "",
            heading,
            "",
            f"- Slot: `{slot['slot']}`",
            f"- Aspect ratios: {', '.join(slot['aspect_ratios'])}",
            f"- Candidates: {slot['candidate_count'] if active else 'do not generate'}",
            f"- Scope: {slot.get('visual_scope', 'runtime-support')}",
            "",
            "### Prompt",
            "",
            slot["prompt"],
            "",
            "### Review gate",
            "",
            *[f"- {criterion}" for criterion in slot["review_criteria"]],
        ])
    return "\n".join(lines).rstrip() + "\n"


def _with_legacy_prompt_contract_slots(
    packet: dict[str, Any],
    *,
    output_dir: Path,
    existing_manifest: dict[str, Any] | None,
) -> tuple[dict[str, Any], dict[str, Path]]:
    """Keep final asset prompts inspectable when the active slot plan evolves.

    An accepted or integrated raster may be a legitimate historic output even
    after the product concept decides that its slot must not be generated
    again. Removing its slot from the new packet would either orphan evidence
    or tempt callers to rewrite provenance. Instead retain the exact old slot
    as a non-generatable contract. Before the generated manifest moves its
    direct linkage to that current contract, the writer archives the old raw
    packet and appends a versioned migration record.
    """
    copied = json.loads(json.dumps(packet, ensure_ascii=False))
    if not existing_manifest:
        return copied, {}
    existing_slots = {
        str(slot.get("id")): slot
        for slot in copied.get("slots", [])
        if isinstance(slot, dict) and slot.get("id")
    }
    final_records = _final_generated_records(existing_manifest)
    if not final_records:
        return copied, {}
    old_packet_path = output_dir / str(
        existing_manifest.get("prompt_packet") or "imagegen-prompt-packet.json"
    )
    try:
        old_packet = load_json_object(old_packet_path)
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        raise ValueError(
            "cannot preserve a final generated asset without its prior prompt packet: "
            f"{old_packet_path}"
        ) from exc
    old_packet_sha256 = _sha256(old_packet_path)
    if existing_manifest.get("prompt_packet_sha256") != old_packet_sha256:
        raise ValueError(
            "cannot preserve a final generated asset because the prior prompt packet "
            "does not match manifest.prompt_packet_sha256"
        )
    old_slots = {
        str(slot.get("id")): slot
        for slot in old_packet.get("slots", [])
        if isinstance(slot, dict) and slot.get("id")
    }
    source_packets: dict[str, Path] = {}
    for record in final_records:
        slot_id = str(record.get("prompt_packet_slot_id") or "")
        if not slot_id:
            raise ValueError(
                f"cannot preserve final generated asset {record.get('id')}: "
                "prompt_packet_slot_id is missing"
            )
        historic_slot = old_slots.get(slot_id)
        if not historic_slot:
            raise ValueError(
                f"cannot preserve final generated asset {record.get('id')}: "
                f"slot {slot_id} is absent from the prior prompt packet"
            )
        _assert_record_matches_prompt_slot(
            record,
            historic_slot,
            prompt_packet_sha256=old_packet_sha256,
        )
        source_packets[str(record["id"])] = old_packet_path
        if slot_id in existing_slots:
            continue
        legacy = json.loads(json.dumps(historic_slot, ensure_ascii=False))
        if legacy.get("active_generation") is not False:
            legacy["active_generation"] = False
            legacy["visual_scope"] = "legacy-supporting-asset"
            legacy["legacy_contract"] = {
                "schema_version": PROMPT_CONTRACT_MIGRATION_SCHEMA,
                "reason": (
                    "The active product slot plan no longer permits this reviewed asset as "
                    "a primary generation target; retain it only as a legacy supporting asset."
                ),
            }
        elif not isinstance(legacy.get("legacy_contract"), dict):
            raise ValueError(
                f"cannot preserve final generated asset {record.get('id')}: "
                "an inactive historic slot is missing legacy_contract metadata"
            )
        generation = legacy.get("generation") if isinstance(legacy.get("generation"), dict) else {}
        legacy["generation"] = {
            **generation,
            "status": "legacy-contract-preserved",
            "api_fallback": "disabled",
        }
        copied.setdefault("slots", []).append(legacy)
        existing_slots[slot_id] = legacy
    return copied, source_packets


def _manifest_template(
    packet: dict[str, Any],
    existing_manifest: dict[str, Any] | None = None,
    *,
    prompt_packet_sha256: str,
    migration_archives: dict[str, dict[str, str]] | None = None,
) -> dict[str, Any]:
    existing_manifest = existing_manifest or {}
    migration_archives = migration_archives or {}
    existing_assets = {
        asset.get("id"): asset
        for asset in existing_manifest.get("assets", [])
        if isinstance(asset, dict) and asset.get("id")
    }
    planned_assets = []
    for slot in packet.get("slots", []):
        existing = existing_assets.pop(slot["id"], None)
        prompt_contract = _prompt_contract_for_slot(slot, prompt_packet_sha256)
        if existing and existing.get("status") != "planned":
            if _is_final_generated_record(existing):
                planned_assets.append(
                    _migrate_final_asset_prompt_contract(
                        existing,
                        slot=slot,
                        prompt_contract=prompt_contract,
                        archive=migration_archives.get(str(existing.get("id") or "")),
                    )
                )
            else:
                planned_assets.append({
                    **existing,
                    "visual_scope": slot.get("visual_scope", "runtime-support"),
                    "active_generation": slot.get("active_generation") is not False,
                })
            continue
        planned_assets.append({
            "id": slot["id"],
            "label": slot["label"],
            "slot": slot["slot"],
            "expected_aspect_ratios": slot.get("aspect_ratios", []),
            "status": "planned",
            "acquisition_mode": "generated",
            "asset_path": None,
            "original_png_path": None,
            "format": None,
            "dimensions": None,
            "size_kb": None,
            "sha256": None,
            "intended_for": slot["intended_for"],
            "alt_text": None,
            "prompt_summary": slot["prompt"],
            "selection_reason": None,
            "reviewed_criteria": [],
            "review_criteria": slot.get("review_criteria", []),
            "review_gate_version": "visual-asset-review/v1",
            "generation_provenance_version": None,
            "generator": None,
            "generation_run_id": None,
            "candidate_id": None,
            "visual_scope": slot.get("visual_scope", "runtime-support"),
            "active_generation": slot.get("active_generation") is not False,
            "lifecycle_role": (
                "legacy-supporting-asset"
                if slot.get("active_generation") is False
                else "active-generation-slot"
            ),
            **prompt_contract,
        })

    historic_assets = []
    for existing in existing_assets.values():
        if not isinstance(existing, dict):
            continue
        if _is_final_generated_record(existing):
            raise ValueError(
                f"final generated asset {existing.get('id')} is absent from the rebuilt "
                "prompt packet; retain it as a legacy contract before rebuilding"
            )
        if existing.get("status") == "integrated" or existing.get("status") == "accepted":
            historic_assets.append(existing)
        elif existing.get("status") == "rejected":
            historic_assets.append(existing)

    return {
        "schema_version": VISUAL_ASSET_MANIFEST_SCHEMA,
        "project": packet.get("project") or existing_manifest.get("project") or packet.get("brand", "product"),
        "brand": packet.get("brand") or existing_manifest.get("brand") or "Product",
        "generator": {"id": VISUAL_IMAGE_GENERATOR_ID, "api_fallback": "disabled"},
        "source_session": existing_manifest.get("source_session") or {
            "id": None,
            "default_directory": "$CODEX_HOME/generated_images/<session-id>",
            "preserve_originals": True,
        },
        "prompt_packet": "imagegen-prompt-packet.json",
        "prompt_packet_sha256": prompt_packet_sha256,
        "assets": [*planned_assets, *historic_assets],
    }


def _final_generated_records(manifest: dict[str, Any]) -> list[dict[str, Any]]:
    return [
        record
        for record in manifest.get("assets", [])
        if _is_final_generated_record(record)
    ]


def _is_final_generated_record(record: Any) -> bool:
    if not isinstance(record, dict):
        return False
    if record.get("status") not in FINAL_GENERATED_STATUSES:
        return False
    return record.get("acquisition_mode") != "sourced"


def _prompt_contract_for_slot(
    slot: dict[str, Any],
    prompt_packet_sha256: str,
) -> dict[str, Any]:
    return {
        "prompt_packet_sha256": prompt_packet_sha256,
        "prompt_packet_slot_id": str(slot["id"]),
        "prompt_slot_sha256": _canonical_sha256(slot),
        "prompt_summary": str(slot.get("prompt") or ""),
        "review_criteria": [
            str(item) for item in slot.get("review_criteria", []) if item
        ],
    }


def _prompt_contract_from_record(record: dict[str, Any]) -> dict[str, Any]:
    return {
        "prompt_packet_sha256": str(record.get("prompt_packet_sha256") or ""),
        "prompt_packet_slot_id": str(record.get("prompt_packet_slot_id") or ""),
        "prompt_slot_sha256": str(record.get("prompt_slot_sha256") or ""),
        "prompt_summary": str(record.get("prompt_summary") or ""),
        "review_criteria": [
            str(item) for item in record.get("review_criteria", []) if item
        ],
    }


def _assert_record_matches_prompt_slot(
    record: dict[str, Any],
    slot: dict[str, Any],
    *,
    prompt_packet_sha256: str,
) -> None:
    expected = _prompt_contract_for_slot(slot, prompt_packet_sha256)
    actual = _prompt_contract_from_record(record)
    if actual != expected:
        raise ValueError(
            f"cannot preserve final generated asset {record.get('id')}: its prompt "
            "contract does not match the prior prompt packet"
        )


def _prepare_prompt_contract_archives(
    *,
    packet: dict[str, Any],
    existing_manifest: dict[str, Any] | None,
    source_packets: dict[str, Path],
    output_dir: Path,
    prompt_packet_sha256: str,
) -> dict[str, dict[str, str]]:
    if not existing_manifest:
        return {}
    existing_assets = {
        str(record.get("id")): record
        for record in _final_generated_records(existing_manifest)
        if record.get("id")
    }
    archives: dict[str, dict[str, str]] = {}
    for slot in packet.get("slots", []):
        if not isinstance(slot, dict) or not slot.get("id"):
            continue
        record = existing_assets.get(str(slot["id"]))
        if record is None:
            continue
        previous = _prompt_contract_from_record(record)
        current = _prompt_contract_for_slot(slot, prompt_packet_sha256)
        if previous == current:
            continue
        slot_changed = (
            previous["prompt_slot_sha256"] != current["prompt_slot_sha256"]
            or previous["prompt_summary"] != current["prompt_summary"]
            or previous["review_criteria"] != current["review_criteria"]
        )
        if slot_changed and slot.get("active_generation") is not False:
            raise ValueError(
                f"final generated asset {record.get('id')} has a changed active prompt slot; "
                "create a new slot or retain the old asset as a legacy contract"
            )
        source_path = source_packets.get(str(record["id"]))
        if source_path is None:
            raise ValueError(
                f"cannot archive prior prompt contract for final generated asset {record.get('id')}"
            )
        archives[str(record["id"])] = _archive_prompt_packet(
            source_path,
            output_dir=output_dir,
            contract=previous,
        )
    return archives


def _archive_prompt_packet(
    source_path: Path,
    *,
    output_dir: Path,
    contract: dict[str, Any],
) -> dict[str, str]:
    source_sha256 = _sha256(source_path)
    if source_sha256 != contract["prompt_packet_sha256"]:
        raise ValueError(
            "cannot archive a prompt contract whose packet digest does not match "
            "the final asset record"
        )
    history_dir = output_dir / "prompt-contract-history"
    history_dir.mkdir(parents=True, exist_ok=True)
    archive_path = history_dir / f"{source_sha256}.json"
    if archive_path.exists() and _sha256(archive_path) != source_sha256:
        raise ValueError(f"prompt contract archive digest mismatch: {archive_path}")
    if not archive_path.exists():
        archive_path.write_bytes(source_path.read_bytes())
    return {
        "path": archive_path.relative_to(output_dir).as_posix(),
        "packet_sha256": source_sha256,
        "slot_id": contract["prompt_packet_slot_id"],
    }


def _migrate_final_asset_prompt_contract(
    existing: dict[str, Any],
    *,
    slot: dict[str, Any],
    prompt_contract: dict[str, Any],
    archive: dict[str, str] | None,
) -> dict[str, Any]:
    previous = _prompt_contract_from_record(existing)
    migrations = existing.get("prompt_contract_migrations") or []
    if not isinstance(migrations, list):
        raise ValueError(
            f"final generated asset {existing.get('id')} has invalid prompt_contract_migrations"
        )
    if migrations:
        last = migrations[-1]
        if not isinstance(last, dict) or last.get("to") != previous:
            raise ValueError(
                f"final generated asset {existing.get('id')} has a broken prompt-contract migration chain"
            )
    if previous != prompt_contract:
        if archive is None:
            raise ValueError(
                f"final generated asset {existing.get('id')} needs an archived prompt-contract migration"
            )
        migration = {
            "schema_version": PROMPT_CONTRACT_MIGRATION_SCHEMA,
            "reason": str(
                (slot.get("legacy_contract") or {}).get("reason")
                or "The prompt packet was rebuilt while preserving a reviewed generated asset."
            ),
            "from": previous,
            "to": prompt_contract,
            "archive": archive,
        }
        migrations = [*migrations, migration]
    if slot.get("active_generation") is False and not migrations:
        raise ValueError(
            f"legacy final generated asset {existing.get('id')} requires prompt-contract migration evidence"
        )
    return {
        **existing,
        **prompt_contract,
        "visual_scope": slot.get("visual_scope", "runtime-support"),
        "active_generation": slot.get("active_generation") is not False,
        "lifecycle_role": (
            "legacy-supporting-asset"
            if slot.get("active_generation") is False
            else "active-generation-slot"
        ),
        "prompt_contract_migrations": migrations,
    }


def _json_bytes(payload: Any) -> bytes:
    return (json.dumps(payload, ensure_ascii=False, indent=2) + "\n").encode("utf-8")


def _canonical_sha256(payload: Any) -> str:
    encoded = json.dumps(
        payload,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()
