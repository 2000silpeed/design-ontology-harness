from __future__ import annotations

from pathlib import Path

from .advanced_components import catalog_entries, get_advanced_component, recommend_advanced_components
from .component_reference_baseline import (
    BASELINE_FAMILY_COMPONENTS,
    FAMILY_SPECS,
    baseline_component_meta,
    reference_baseline_summary,
)
from .models import DocumentRecord, ReferenceLink
from .utils import ensure_dir, write_json
from .graph_builders import (
    SOURCED_VISUAL_ASSET_CANDIDATE_MANIFEST_PATH,
    SOURCED_VISUAL_ASSET_CONTRACT_ID,
    SOURCED_VISUAL_ASSET_FALLBACK_POLICY,
    SOURCED_VISUAL_ASSET_RECORD_REQUIRED_FIELDS,
    VISUAL_ASSET_COMPATIBLE_MANIFEST_PATHS,
    VISUAL_ASSET_CONTRACT_ID,
    VISUAL_ASSET_MANIFEST_PATH,
    VISUAL_ASSET_MANIFEST_REQUIRED_FIELDS,
    VISUAL_ASSET_MANIFEST_SCHEMA,
    VISUAL_ASSET_PROMPT_PACK_PATH,
    VISUAL_ASSET_RECORD_REQUIRED_FIELDS,
    build_full_ontology_graph,
)
from .graph_spec_sections import build_graph_spec_sections

REQUIRED_PROFILE_KEYS = {
    "brand_name": str,
    "system_name": str,
    "product_summary": str,
    "audiences": list,
    "brand_keywords": list,
    "anti_keywords": list,
    "tone_of_voice": list,
    "visual_keywords": list,
    "interaction_keywords": list,
    "platforms": list,
    "accessibility_targets": list,
    "product_primitives": list,
}

PRIMITIVE_COMPONENTS = {
    "workspace navigation": ["app-shell", "sidebar-nav", "topbar", "breadcrumb", "workspace-switcher"],
    "rich text editor": ["editor-canvas", "editor-toolbar", "inline-format-menu", "slash-command-menu", "block-controls"],
    "command palette": ["command-palette", "command-result-item", "shortcut-hint", "scope-switcher"],
    "operational overview": ["metric-strip", "status-summary-row", "task-surface-header", "source-ledger", "operational-rail", "section-header"],
    "dashboard cards": ["stat-card", "insight-card", "activity-card", "section-header"],
    "data tables": ["data-table", "column-header", "filter-chip", "row-actions", "pagination"],
    "forms": ["text-field", "select", "checkbox", "radio", "textarea", "form-section"],
    "notifications": ["toast", "inline-alert", "empty-state", "banner"],
}

LAYOUT_PRIMITIVE_KEYWORDS = {
    "workspace navigation", "operational overview", "dashboard cards", "data tables", "layout", "grid",
    "sidebar", "table", "card", "navigation", "archive browser", "audit log",
    "status rail", "metric strip", "source ledger", "task surface",
}

INTERACTION_PRIMITIVE_KEYWORDS = {
    "command palette", "rich text editor", "forms", "notifications",
    "restore workflow", "wizard", "editor", "search", "filter",
}

FOUNDATION_FROM_CONCEPT = {
    "color": "Color tokens and semantic color policy",
    "typography": "Type scale and editorial hierarchy",
    "spacing": "Spacing scale and density model",
    "layout": "Grid, container, and page rhythm",
    "motion": "Motion tokens and transition rules",
    "accessibility": "Accessibility rules and contrast baseline",
    "iconography": "Icon family and stroke policy",
    "content": "Content design and microcopy rules",
    "design_token": "Token layering and naming",
    "foundation": "Foundation primitives",
    "imagery": "Generated visual assets and media policy",
}

ONTOLOGY_RELATIONS = [
    {"id": "expresses", "from": "Brand", "to": "Principle"},
    {"id": "constrains", "from": "Principle", "to": "TokenCategory"},
    {"id": "defines", "from": "TokenCategory", "to": "Token"},
    {"id": "governs", "from": "Principle", "to": "ComponentFamily"},
    {"id": "composed_of", "from": "ComponentFamily", "to": "Component"},
    {"id": "supports", "from": "Component", "to": "ProductPrimitive"},
    {"id": "applies_to", "from": "AccessibilityRule", "to": "ComponentFamily"},
    {"id": "inspired_by", "from": "Brand", "to": "SourceReference"},
    {"id": "generated_with", "from": "GeneratedVisualAsset", "to": "ImageGenerationModel"},
    {"id": "sourced_from", "from": "SourcedVisualAsset", "to": "FreeSourcedVisualProvider"},
    {"id": "sourced_from", "from": "SourcedVisualAsset", "to": "LicensedVisualProvider"},
    {"id": "licensed_under", "from": "SourcedVisualAsset", "to": "LicensePolicy"},
    {"id": "grounded_in", "from": "GeneratedVisualAsset", "to": "Brand"},
    {"id": "grounded_in", "from": "SourcedVisualAsset", "to": "Brand"},
    {"id": "intended_for", "from": "GeneratedVisualAsset", "to": "Component"},
    {"id": "intended_for", "from": "SourcedVisualAsset", "to": "Component"},
    {"id": "enforces", "from": "GovernanceRule", "to": "TokenCategory"},
    {"id": "prevents", "from": "GovernanceRule", "to": "ImplementationFailurePattern"},
]

def generate_system_pack(
    output_dir: Path,
    brand_profile: dict,
    blueprint: dict,
    references: list[ReferenceLink],
    documents: list[DocumentRecord],
) -> dict:
    blueprint_dir = ensure_dir(output_dir / "blueprint")

    validation = validate_brand_profile(brand_profile)
    foundations = derive_foundations(blueprint)
    token_schema = build_token_schema(brand_profile, blueprint)
    component_inventory = build_component_inventory(brand_profile, blueprint)
    css_extraction = blueprint.get("css_extraction") or {}
    alias_result = None
    var_chains = None
    typo_scale = None
    if css_extraction:
        alias_data = css_extraction.get("alias_layer") or {}
        if isinstance(alias_data, dict):
            alias_result = {
                tier: alias_data.get(tier, [])
                for tier in ["core", "util", "action", "component"]
                if alias_data.get(tier)
            } or None
        var_data = css_extraction.get("var_resolution") or {}
        resolved_vars = var_data.get("resolved") or {}
        if isinstance(resolved_vars, dict):
            var_chains = {
                k: v for k, v in resolved_vars.items()
                if isinstance(v, str) and v.startswith("var(")
            } or None
        typo_data = css_extraction.get("typography") or {}
        typo_scale = typo_data.get("scale") or None

    ontology_graph = build_full_ontology_graph(
        brand_profile=brand_profile,
        blueprint=blueprint,
        component_inventory=component_inventory,
        token_schema=token_schema,
        alias_result=alias_result,
        var_chains=var_chains,
        typo_scale=typo_scale,
    )
    ontology_dict = ontology_graph.to_dict()
    graph_sections = build_graph_spec_sections(ontology_graph)
    system_spec = build_system_spec_markdown(
        brand_profile=brand_profile,
        blueprint=blueprint,
        validation=validation,
        foundations=foundations,
        token_schema=token_schema,
        component_inventory=component_inventory,
        documents=documents,
        css_extraction=blueprint.get("css_extraction"),
        graph_sections=graph_sections,
    )

    write_json(blueprint_dir / "profile_validation.json", validation)
    write_json(blueprint_dir / "token_schema.json", token_schema)
    write_json(blueprint_dir / "component_inventory.json", component_inventory)
    write_json(blueprint_dir / "system_ontology.json", ontology_dict)
    (blueprint_dir / "system_spec.md").write_text(system_spec, encoding="utf-8")

    return {
        "validation": validation,
        "token_schema": token_schema,
        "component_inventory": component_inventory,
        "system_ontology": ontology_dict,
    }


def validate_brand_profile(profile: dict) -> dict:
    errors: list[str] = []
    warnings: list[str] = []

    for key, expected_type in REQUIRED_PROFILE_KEYS.items():
        if key not in profile:
            errors.append(f"Missing required key: {key}")
            continue
        if not isinstance(profile[key], expected_type):
            errors.append(f"Invalid type for {key}: expected {expected_type.__name__}")
            continue
        if expected_type in {str, list} and not profile[key]:
            warnings.append(f"{key} is present but empty")

    keyword_overlap = set(profile.get("brand_keywords", [])) & set(profile.get("anti_keywords", []))
    if keyword_overlap:
        errors.append(f"brand_keywords and anti_keywords overlap: {sorted(keyword_overlap)}")

    if len(profile.get("brand_keywords", [])) < 3:
        warnings.append("At least 3 brand_keywords are recommended to shape a distinctive system.")
    if len(profile.get("product_primitives", [])) < 3:
        warnings.append("Add more product_primitives so component planning reflects the real app surface.")
    if not profile.get("accessibility_targets"):
        warnings.append("Define accessibility_targets so the system has an explicit compliance floor.")
    for issue in profile.get("_color_reference_issues", []):
        warnings.append(issue)
    for issue in profile.get("_visual_reference_issues", []):
        warnings.append(issue)

    return {
        "valid": not errors,
        "errors": errors,
        "warnings": warnings,
    }


def derive_foundations(blueprint: dict) -> list[dict]:
    targets = blueprint.get("ontology_targets", [])
    foundations: list[dict] = []
    seen: set[str] = set()
    for target in targets:
        concept_id = target["concept_id"]
        if concept_id in FOUNDATION_FROM_CONCEPT and concept_id not in seen:
            seen.add(concept_id)
            foundations.append(
                {
                    "concept_id": concept_id,
                    "name": FOUNDATION_FROM_CONCEPT[concept_id],
                    "priority": "high" if target["count"] >= 8 else "medium",
                    "signal_count": target["count"],
                }
            )
    return foundations


def build_token_schema(brand_profile: dict, blueprint: dict) -> dict:
    brand_keywords = [keyword.lower() for keyword in brand_profile.get("brand_keywords", [])]
    calm_system = "calm" in brand_keywords or "trustworthy" in brand_keywords
    editorial_system = "editorial" in brand_keywords
    color_reference = brand_profile.get("_resolved_color_reference")
    font_system = brand_profile.get("_resolved_font_system")
    visual_reference = brand_profile.get("_resolved_visual_reference")
    responsive_policy = (blueprint.get("governance") or {}).get("responsive_resilience_policy") or {}
    application_concept = blueprint.get("application_concept") or {}
    layout_skeleton = blueprint.get("layout_skeleton") or {}
    differentiation_strategy = blueprint.get("differentiation_strategy") or {}
    layout_density = str(layout_skeleton.get("density") or "").lower()
    if layout_density == "dense":
        density_modes = ["compact", "dense"]
    elif layout_density == "spacious":
        density_modes = ["comfortable", "spacious"]
    else:
        density_modes = ["comfortable", "compact"] if calm_system else ["default", "dense"]

    schema = {
        "naming": {
            "core": "{category}.{role}.{scale}",
            "semantic": "{category}.{intent}.{state}",
            "component": "{component}.{slot}.{property}",
            "rule": "네이밍 패턴만 정의하고 구체적 토큰명은 실제 컴포넌트·역할에서 도출 — 임의 토큰명 생성 금지",
        },
        "layers": [
            {
                "name": "core",
                "purpose": "브랜드에 종속되지 않는 수치와 원재료 토큰",
                "categories": ["color", "spacing", "radius", "typography", "motion", "elevation"],
            },
            {
                "name": "semantic",
                "purpose": "역할 중심 토큰",
                "categories": ["surface", "text", "border", "focus", "feedback"],
            },
            {
                "name": "component",
                "purpose": "컴포넌트 슬롯별 적용 토큰",
                "categories": ["button", "input", "navigation", "overlay", "editor"],
            },
        ],
        "categories": {
            "color": {
                "core_groups": ["neutral", "accent", "success", "warning", "danger", "info"],
                "scale": [0, 50, 100, 200, 300, 400, 500, 600, 700, 800, 900, 1000],
                "rules": [
                    "accent는 최대 1개의 주 계열로 시작",
                    "semantic feedback은 accent와 분리",
                    "text/surface 조합은 접근성 기준을 우선",
                    "hex 값은 color_reference·CSS 추출·브랜드 가이드에서만 가져오고 임의 생성 금지",
                ],
            },
            "typography": _build_typography_category(editorial_system, font_system),
            "spacing": {
                "scale": [0, 2, 4, 8, 12, 16, 24, 32, 48, 64, 96],
                "density_modes": density_modes,
                "layout_density": layout_skeleton.get("density"),
            },
            "layout": {
                "breakpoints_px": responsive_policy.get("viewport_contract", {}).get(
                    "required_widths_px",
                    [320, 360, 390, 430, 768, 1024, 1440],
                ),
                "skeleton": {
                    "composition": layout_skeleton.get("composition"),
                    "navigation_model": layout_skeleton.get("navigation_model"),
                    "density": layout_skeleton.get("density"),
                    "primary_regions": layout_skeleton.get("primary_regions", []),
                    "first_screen_contract": layout_skeleton.get("first_screen_contract", []),
                    "avoid_layouts": layout_skeleton.get("avoid_layouts", []),
                    "signature_moves": differentiation_strategy.get("signature_moves", []),
                    "repetition_risks": differentiation_strategy.get("repetition_risks", []),
                },
                "container_rules": [
                    "모든 section/container는 box-sizing: border-box 기준으로 320px viewport에서 overflow-x 없이 맞아야 함",
                    "grid/flex children에는 필요한 경우 min-width: 0 또는 min-inline-size: 0을 명시",
                    "repeat(N, 1fr) 고정 grid는 모바일에서 1열 또는 minmax(0, 1fr) fallback을 제공",
                    "padded container 내부에서 width: 100vw 사용 금지",
                ],
                "control_rules": responsive_policy.get("control_rules", []),
                "viewport_pass_condition": responsive_policy.get("viewport_contract", {}).get(
                    "pass_condition",
                    "scrollWidth <= innerWidth and primary controls stay reachable.",
                ),
            },
            "radius": {
                "scale": ["none", "sm", "md", "lg", "xl", "pill"],
                "rule": "라운딩은 브랜드 성격을 드러내지만 컴포넌트 계층별로 제한적으로 사용",
            },
            "motion": {
                "durations_ms": [0, 80, 120, 180, 240, 320],
                "easing_tokens": ["standard", "enter", "exit", "emphasized"],
                "rule": "모션은 상태 설명용이며 과장된 장식 효과는 금지",
            },
            "elevation": {
                "levels": ["flat", "raised", "overlay", "modal"],
                "rule": "그림자보다 layer 의미가 먼저 드러나야 함",
            },
        },
        "brand_alignment": {
            "visual_keywords": brand_profile.get("visual_keywords", []),
            "interaction_keywords": brand_profile.get("interaction_keywords", []),
            "system_name": blueprint.get("system_name"),
            "application_concept": application_concept,
            "differentiation_strategy": differentiation_strategy,
        },
    }
    if color_reference:
        active_palette = color_reference.get("active_palette", {}) or {}
        expanded_palette = color_reference.get("expanded_palette", {}) or {}
        schema["categories"]["color"]["reference_palette"] = {
            "source_title": color_reference.get("title"),
            "source_path": color_reference.get("source_path"),
            "preferred_families": color_reference.get("preferred_families", []),
            "selection_mode": color_reference.get("selection_mode"),
            "strategy": color_reference.get("strategy"),
            "expansion": color_reference.get("expansion"),
            "selected_colors": [
                {
                    "name": item.get("name"),
                    "family": item.get("family"),
                    "hex": item.get("hex"),
                    "mood": item.get("mood"),
                    "pairings": item.get("pairings", [])[:6],
                }
                for item in color_reference.get("selected_colors", [])
            ],
            "palette_roles": {
                role: {
                    "name": item.get("name"),
                    "family": item.get("family"),
                    "hex": item.get("hex"),
                    "mood": item.get("mood"),
                    "pairings": item.get("pairings", [])[:6],
                }
                for role, item in color_reference.get("palette_roles", {}).items()
            },
            "active_palette": {
                "candidate_id": active_palette.get("candidate_id"),
                "selection_mode": active_palette.get("selection_mode"),
                "roles": {
                    role: {
                        "name": item.get("name"),
                        "family": item.get("family"),
                        "hex": item.get("hex"),
                        "mood": item.get("mood"),
                    }
                    for role, item in active_palette.get("roles", {}).items()
                },
            },
            "palette_candidates": [
                {
                    "id": candidate.get("id"),
                    "label": candidate.get("label"),
                    "score": candidate.get("score"),
                    "rationale": candidate.get("rationale", []),
                    "strategy_snapshot": candidate.get("strategy_snapshot", {}),
                    "roles": {
                        role: {
                            "name": item.get("name"),
                            "family": item.get("family"),
                            "hex": item.get("hex"),
                            "mood": item.get("mood"),
                        }
                        for role, item in candidate.get("roles", {}).items()
                    },
                }
                for candidate in color_reference.get("palette_candidates", [])
            ],
            "expanded_palette": {
                "search_strategy": expanded_palette.get("search_strategy", {}),
                "supporting_colors": [
                    {
                        "name": item.get("name"),
                        "family": item.get("family"),
                        "hex": item.get("hex"),
                        "mood": item.get("mood"),
                        "source_type": item.get("source_type"),
                        "source_seed_names": item.get("source_seed_names", []),
                        "search_score": item.get("search_score"),
                        "search_reasons": item.get("search_reasons", []),
                    }
                    for item in expanded_palette.get("supporting_colors", [])
                ],
                "semantic_roles": {
                    role: {
                        "name": item.get("name"),
                        "family": item.get("family"),
                        "hex": item.get("hex"),
                        "source_type": item.get("source_type"),
                    }
                    for role, item in expanded_palette.get("semantic_roles", {}).items()
                },
                "combination_lists": expanded_palette.get("combination_lists", []),
            },
            "semantic_ontology": _compact_semantic_color_ontology_for_token_schema(
                color_reference.get("semantic_ontology", {})
            ),
            "semantic_color_selection": _compact_semantic_color_selection_for_token_schema(
                color_reference.get("semantic_color_selection", {})
            ),
            "rules": [
                "컬러 레퍼런스의 mood와 pairings를 semantic token 설계의 출발점으로 사용",
                "chosen palette는 semantic roles로 번역하고 raw reference color를 그대로 남용하지 않기",
                "앱 내용 기반 색상 선택은 미리 만든 팔레트 세트가 아니라 Semantic OS ontology 검색으로 매번 수행하기",
                "seed color만 쓰지 말고 expanded palette에서 surface/text/border/support 역할까지 확장하기",
                "surface/text/border 대비는 레퍼런스보다 접근성 기준을 우선"
            ],
        }
    if visual_reference:
        motifs = visual_reference.get("visual_motifs", {}) or {}
        layout_cues = visual_reference.get("layout_cues", []) or []
        color_balance = motifs.get("color_balance", {}) or {}
        schema["brand_alignment"]["visual_reference_hints"] = {
            "density_bias": (motifs.get("density") or {}).get("value"),
            "surface_style": (motifs.get("surface_style") or {}).get("value"),
            "corner_style": (motifs.get("corner_style") or {}).get("value"),
            "typography_mood": (motifs.get("typography_mood") or {}).get("value"),
            "top_layout_cue": layout_cues[0]["id"] if layout_cues else None,
        }
        schema["categories"]["spacing"]["visual_density_bias"] = (motifs.get("density") or {}).get("value")
        schema["categories"]["radius"]["visual_corner_bias"] = (motifs.get("corner_style") or {}).get("value")
        schema["categories"]["elevation"]["visual_surface_bias"] = (motifs.get("surface_style") or {}).get("value")
        if color_balance:
            schema["categories"]["color"]["visual_balance"] = {
                "observed": color_balance.get("observed"),
                "temperature": color_balance.get("temperature"),
                "contrast_profile": color_balance.get("contrast_profile"),
                "neutral_bias": color_balance.get("neutral_bias"),
            }
    return schema


def _compact_semantic_color_ontology_for_token_schema(semantic_ontology: dict) -> dict:
    if not semantic_ontology:
        return {}

    return {
        "schema_version": semantic_ontology.get("schema_version"),
        "source": semantic_ontology.get("source", {}),
        "node_count": semantic_ontology.get("node_count"),
        "edge_count": semantic_ontology.get("edge_count"),
        "matched_keywords": [
            {
                "id": item.get("id"),
                "role": item.get("role"),
                "name": item.get("name"),
                "hex": item.get("hex"),
                "spectrum": item.get("spectrum"),
                "family": item.get("family"),
                "mood_tags": item.get("mood_tags", []),
                "tone_axes": item.get("tone_axes", []),
            }
            for item in semantic_ontology.get("matched_keywords", [])
        ],
        "recommended_keywords": [
            {
                "id": item.get("id"),
                "name": item.get("name"),
                "hex": item.get("hex"),
                "spectrum": item.get("spectrum"),
                "family": item.get("family"),
                "score": item.get("score"),
                "reasons": item.get("reasons", []),
            }
            for item in semantic_ontology.get("recommended_keywords", [])[:8]
        ],
        "guidelines": [
            {
                "id": item.get("id"),
                "label": item.get("label"),
                "summary": item.get("summary"),
            }
            for item in semantic_ontology.get("guidelines", [])
        ],
        "rules": semantic_ontology.get("rules", []),
        "copyright_handling": semantic_ontology.get("copyright_handling", ""),
    }


def _compact_semantic_color_selection_for_token_schema(selection: dict) -> dict:
    if not selection:
        return {}

    active = selection.get("active_palette") or {}
    return {
        "schema_version": selection.get("schema_version"),
        "selection_method": selection.get("selection_method"),
        "matched_pattern": selection.get("matched_pattern"),
        "role_model": selection.get("role_model", []),
        "active_palette": _compact_semantic_selection_candidate(active),
        "candidate_palettes": [
            _compact_semantic_selection_candidate(candidate)
            for candidate in selection.get("candidate_palettes", [])[:8]
        ],
        "rules": selection.get("rules", []),
    }


def _compact_semantic_selection_candidate(candidate: dict) -> dict:
    if not candidate:
        return {}
    return {
        "id": candidate.get("id"),
        "label": candidate.get("label"),
        "score": candidate.get("score"),
        "rationale": candidate.get("rationale", [])[:6],
        "roles": {
            role: {
                "name": item.get("name"),
                "hex": item.get("hex"),
                "spectrum": item.get("spectrum"),
                "family": item.get("family"),
                "score": item.get("score"),
                "reason": item.get("reason"),
                "behavior": item.get("behavior"),
            }
            for role, item in (candidate.get("roles") or {}).items()
        },
    }


def build_component_inventory(brand_profile: dict, blueprint: dict) -> dict:
    primitives = brand_profile.get("product_primitives", [])
    visual_reference = brand_profile.get("_resolved_visual_reference") or {}
    candidate_archetypes = visual_reference.get("candidate_component_archetypes", []) or []
    families: dict[str, dict] = {}
    all_components: list[dict] = []

    family_specs = FAMILY_SPECS

    for family in blueprint.get("component_strategy", {}).get("required_component_families", []):
        spec = family_specs.get(family, {"states": ["default"], "priority": "medium"})
        families[family] = {
            "family": family,
            "priority": spec["priority"],
            "required_states": spec["states"],
            "components": [],
            "visual_reference_signals": [],
        }

    for primitive in primitives:
        component_names = PRIMITIVE_COMPONENTS.get(primitive.lower(), [])
        for component_name in component_names:
            family = classify_component_family(component_name)
            component = {
                "name": component_name,
                "family": family,
                "supports_primitive": primitive,
                "status": "planned",
                "must_document": ["anatomy", "states", "content rules", "accessibility", "dos and donts"],
            }
            all_components.append(component)
            families.setdefault(
                family,
                {
                    "family": family,
                    "priority": "medium",
                    "required_states": ["default"],
                    "components": [],
                    "visual_reference_signals": [],
                },
            )
            families[family]["components"].append(component_name)

    for family_name, baseline_components in BASELINE_FAMILY_COMPONENTS.items():
        if family_name not in families:
            continue
        existing = set(families[family_name]["components"])
        for component_name in baseline_components:
            if component_name in existing:
                continue
            component_meta = baseline_component_meta(component_name)
            families[family_name]["components"].append(component_name)
            all_components.append(
                {
                    "name": component_name,
                    "family": family_name,
                    "role": component_meta.get("role", ""),
                    "supports_primitive": "reference baseline",
                    "source": "astryx-geist-reference-baseline",
                    "reference_components": component_meta.get("reference_components", []),
                    "status": "planned",
                    "must_document": ["anatomy", "states", "content rules", "accessibility", "dos and donts"],
                }
            )
            existing.add(component_name)

    spec_components = brand_profile.get("_spec_components") or []
    for entry in spec_components:
        if not isinstance(entry, dict):
            continue
        component_name = entry.get("name")
        if not component_name:
            continue
        family = entry.get("family") or classify_component_family(component_name)
        primitive = entry.get("source") or entry.get("supports_primitive") or "spec-detected"
        families.setdefault(
            family,
            {
                "family": family,
                "priority": family_specs.get(family, {}).get("priority", "medium"),
                "required_states": family_specs.get(family, {}).get("states", ["default"]),
                "components": [],
                "visual_reference_signals": [],
            },
        )
        if component_name in families[family]["components"]:
            continue
        families[family]["components"].append(component_name)
        all_components.append(
            {
                "name": component_name,
                "family": family,
                "supports_primitive": primitive,
                "status": "planned",
                "must_document": ["anatomy", "states", "content rules", "accessibility", "dos and donts"],
            }
        )

    advanced_recommendations = recommend_advanced_components(
        brand_profile=brand_profile,
        blueprint=blueprint,
        existing_components=[component["name"] for component in all_components],
        limit=12,
    )
    for recommendation in advanced_recommendations:
        component_name = recommendation["name"]
        component_spec = get_advanced_component(component_name) or {}
        family = recommendation.get("family") or component_spec.get("family") or classify_component_family(component_name)
        families.setdefault(
            family,
            {
                "family": family,
                "priority": family_specs.get(family, {}).get("priority", "medium"),
                "required_states": family_specs.get(family, {}).get("states", ["default"]),
                "components": [],
                "visual_reference_signals": [],
            },
        )
        if component_name not in families[family]["components"]:
            families[family]["components"].append(component_name)
        all_components.append(
            {
                "name": component_name,
                "family": family,
                "role": recommendation.get("role", component_spec.get("role", "")),
                "supports_primitive": "advanced-component-catalog",
                "status": "recommended-advanced",
                "advanced_component": True,
                "usage_guidance": recommendation.get("use_when", []),
                "avoid_when": recommendation.get("avoid_when", []),
                "pairs_with": recommendation.get("pairs_with", []),
                "matched_signals": recommendation.get("matched_signals", []),
                "score": recommendation.get("score"),
                "must_document": ["anatomy", "states", "content rules", "accessibility", "dos and donts"],
            }
        )

    existing_components_by_name = {component["name"]: component for component in all_components}
    for archetype in candidate_archetypes:
        if archetype.get("confidence", 0.0) < 0.55:
            continue
        family = archetype.get("family") or "foundation"
        family_entry = families.setdefault(
            family,
            {
                "family": family,
                "priority": family_specs.get(family, {}).get("priority", "medium"),
                "required_states": family_specs.get(family, {}).get("states", ["default"]),
                "components": [],
                "visual_reference_signals": [],
            },
        )
        signal = {
            "id": archetype.get("id"),
            "label": archetype.get("label"),
            "confidence": archetype.get("confidence"),
            "evidence": archetype.get("evidence", []),
        }
        family_entry["visual_reference_signals"].append(signal)

        supports_primitive = (
            (archetype.get("supports_primitives") or ["visual-reference"])[0]
        )
        for component_name in archetype.get("suggested_components", [])[:5]:
            existing_component = existing_components_by_name.get(component_name)
            if existing_component:
                existing_family = existing_component.get("family")
                if existing_family == "foundation" and family != "foundation":
                    old_family_entry = families.get(existing_family)
                    if old_family_entry and component_name in old_family_entry["components"]:
                        old_family_entry["components"].remove(component_name)
                    existing_component["family"] = family
                    existing_component.setdefault("source", "visual-reference")
                    existing_component.setdefault("archetype", archetype.get("id"))
                    if component_name not in family_entry["components"]:
                        family_entry["components"].append(component_name)
                elif existing_family == family:
                    if component_name not in family_entry["components"]:
                        family_entry["components"].append(component_name)
                continue
            if component_name not in family_entry["components"]:
                family_entry["components"].append(component_name)
            all_components.append(
                {
                    "name": component_name,
                    "family": family,
                    "supports_primitive": supports_primitive,
                    "status": "candidate-from-visual-reference",
                    "source": "visual-reference",
                    "archetype": archetype.get("id"),
                    "must_document": ["anatomy", "states", "content rules", "accessibility", "dos and donts"],
                }
            )
            existing_components_by_name[component_name] = all_components[-1]

    return {
        "families": sorted(families.values(), key=lambda item: (item["priority"] != "high", item["family"])),
        "components": all_components,
        "candidate_component_archetypes": candidate_archetypes,
        "reference_baseline": reference_baseline_summary(),
        "advanced_component_catalog": catalog_entries(),
        "advanced_recommendations": advanced_recommendations,
    }


def classify_component_family(component_name: str) -> str:
    if any(token in component_name for token in [
        "hero", "feature-card", "feature-grid", "feature-icon", "feature-title",
        "feature-description", "feature-section", "logo-cloud", "customer-logo",
        "metric-highlight", "press-quote", "testimonial", "faq", "cta-section",
        "cta-headline", "cta-supporting", "site-footer", "footer-column",
        "footer-link", "footer-legal", "footer-social", "site-header",
        "site-logo", "site-nav",
    ]):
        return "marketing"
    if any(token in component_name for token in [
        "chart", "table", "grid", "summary", "score", "metric", "ledger",
        "status-summary", "source-ledger", "surface-header", "insight-row",
        "list", "queue", "timeline", "strip",
    ]):
        return "data-display"
    if any(token in component_name for token in ["editor", "block", "slash"]):
        return "editorial"
    if any(token in component_name for token in ["nav", "breadcrumb", "switcher", "topbar", "sidebar", "tab", "pagination"]):
        return "navigation"
    if any(token in component_name for token in ["badge", "chip", "highlight", "status-dot"]):
        return "feedback"
    if any(token in component_name for token in ["toast", "alert", "banner", "empty-state"]):
        return "feedback"
    if any(token in component_name for token in ["palette", "menu", "overlay", "modal", "dialog", "popover", "tooltip", "drawer"]):
        return "overlay"
    if any(token in component_name for token in ["sheet", "preview", "panel"]):
        return "overlay"
    if any(token in component_name for token in ["field", "select", "checkbox", "radio", "textarea", "switch"]):
        return "input"
    if any(token in component_name for token in ["slider", "dropzone", "selector"]):
        return "input"
    if any(token in component_name for token in ["card", "thumbnail", "avatar"]):
        return "surface"
    return "button" if "button" in component_name else "foundation"


def build_system_ontology(
    brand_profile: dict,
    blueprint: dict,
    references: list[ReferenceLink],
    component_inventory: dict,
) -> dict:
    brand_id = f"brand:{slugify_text(brand_profile.get('brand_name', 'brand'))}"
    nodes = [
        {"id": brand_id, "type": "Brand", "label": brand_profile.get("brand_name", "Brand")},
    ]
    edges = []

    for principle in blueprint.get("principles", []):
        principle_id = f"principle:{slugify_text(principle['keyword'])}"
        nodes.append({"id": principle_id, "type": "Principle", "label": principle["name"]})
        edges.append({"type": "expresses", "from": brand_id, "to": principle_id})

    for layer in ["color", "typography", "spacing", "motion"]:
        token_category_id = f"token-category:{layer}"
        nodes.append({"id": token_category_id, "type": "TokenCategory", "label": layer})
        for principle in blueprint.get("principles", []):
            principle_id = f"principle:{slugify_text(principle['keyword'])}"
            edges.append({"type": "constrains", "from": principle_id, "to": token_category_id})

    image_model_id = "image-model:codex-imagegen"
    visual_asset_id = "visual-asset:brand-aligned-raster"
    sourced_visual_asset_id = "sourced-visual-asset:brand-aligned-raster-fallback"
    visual_asset_contract_id = VISUAL_ASSET_CONTRACT_ID
    sourced_visual_asset_contract_id = SOURCED_VISUAL_ASSET_CONTRACT_ID
    nodes.append({
        "id": visual_asset_contract_id,
        "type": "GovernanceRule",
        "label": "Generated visual asset contract",
        "meta": {
            "schema_version": VISUAL_ASSET_MANIFEST_SCHEMA,
            "preferred_manifest_path": VISUAL_ASSET_MANIFEST_PATH,
            "compatible_manifest_paths": VISUAL_ASSET_COMPATIBLE_MANIFEST_PATHS,
            "prompt_pack_path": VISUAL_ASSET_PROMPT_PACK_PATH,
            "default_source_directory": "$CODEX_HOME/generated_images/<session-id>",
            "preserve_originals": True,
            "workspace_copy_required": True,
            "runtime_code_must_not_reference_codex_home": True,
            "api_fallback": "disabled",
            "failure_policy": "no API fallback",
            "manifest_required_fields": VISUAL_ASSET_MANIFEST_REQUIRED_FIELDS,
            "asset_record_required_fields": VISUAL_ASSET_RECORD_REQUIRED_FIELDS,
        },
    })
    nodes.append({
        "id": image_model_id,
        "type": "ImageGenerationModel",
        "label": "Codex image_gen skill",
        "meta": {
            "runtime": "Codex built-in image_gen skill",
            "default_path": True,
            "api_fallback": "disabled",
            "fallback_policy": "no API fallback",
            "failure_behavior": "If Codex image_gen fails, do not invoke CLI or OpenAI API fallback.",
            "source_session_tracking": True,
            "default_source_directory": "$CODEX_HOME/generated_images/<session-id>",
            "workspace_copy_required": True,
            "contract_id": visual_asset_contract_id,
        },
    })
    nodes.append({
        "id": sourced_visual_asset_contract_id,
        "type": "GovernanceRule",
        "label": "Sourced visual asset fallback contract",
        "meta": {
            "schema_version": VISUAL_ASSET_MANIFEST_SCHEMA,
            "preferred_manifest_path": VISUAL_ASSET_MANIFEST_PATH,
            "candidate_manifest_path": SOURCED_VISUAL_ASSET_CANDIDATE_MANIFEST_PATH,
            "compatible_manifest_paths": VISUAL_ASSET_COMPATIBLE_MANIFEST_PATHS,
            "fallback_policy": SOURCED_VISUAL_ASSET_FALLBACK_POLICY,
            "fallback_for": visual_asset_contract_id,
            "api_fallback": "disabled",
            "hotlinking_allowed": False,
            "workspace_copy_required": True,
            "license_metadata_required": True,
            "asset_record_required_fields": SOURCED_VISUAL_ASSET_RECORD_REQUIRED_FIELDS,
        },
    })
    nodes.append({
        "id": "visual-asset-provider:openverse",
        "type": "FreeSourcedVisualProvider",
        "label": "Openverse",
        "meta": {
            "provider_id": "openverse",
            "tier": "free-sourced",
            "kind": "free-image-search",
            "license_metadata_required": True,
            "license_proof_required": False,
            "workspace_copy_required": True,
        },
    })
    nodes.append({
        "id": "visual-asset-provider:adobe-stock",
        "type": "LicensedVisualProvider",
        "label": "Adobe Stock",
        "meta": {
            "provider_id": "adobe-stock",
            "tier": "licensed",
            "kind": "paid-stock-provider",
            "license_metadata_required": True,
            "license_proof_required": True,
            "workspace_copy_required": True,
        },
    })
    nodes.append({
        "id": "visual-asset-provider:lazyweb",
        "type": "ReferenceOnlyProvider",
        "label": "Lazyweb",
        "meta": {
            "provider_id": "lazyweb",
            "tier": "reference-only",
            "kind": "design-reference-corpus",
            "asset_copy_allowed": False,
            "workspace_copy_required": False,
        },
    })
    nodes.append({
        "id": "license-policy:verified-free-visual-asset",
        "type": "LicensePolicy",
        "label": "Verified free visual asset license",
        "meta": {
            "required_metadata": [
                "source_url",
                "download_url",
                "provider",
                "author",
                "license",
                "attribution_required",
                "sha256",
            ],
        },
    })
    nodes.append(
        {
            "id": visual_asset_id,
            "type": "GeneratedVisualAsset",
            "label": "Brand-aligned raster image",
            "meta": {
                "model": "Codex image_gen skill",
                "api_fallback": "disabled",
                "fallback_policy": "no API fallback",
                "manifest_path": VISUAL_ASSET_MANIFEST_PATH,
                "compatible_manifest_paths": VISUAL_ASSET_COMPATIBLE_MANIFEST_PATHS,
                "manifest_schema": VISUAL_ASSET_MANIFEST_SCHEMA,
                "manifest_required_fields": VISUAL_ASSET_MANIFEST_REQUIRED_FIELDS,
                "asset_record_required_fields": VISUAL_ASSET_RECORD_REQUIRED_FIELDS,
                "prompt_pack_path": VISUAL_ASSET_PROMPT_PACK_PATH,
                "alt_text_required": True,
                "prompt_summary_required": True,
                "sha256_required": True,
                "original_preservation_required": True,
                "workspace_copy_required": True,
                "source_session_tracking": True,
                "contract_id": visual_asset_contract_id,
            },
        }
    )
    nodes.append(
        {
            "id": sourced_visual_asset_id,
            "type": "SourcedVisualAsset",
            "label": "Brand-aligned sourced visual fallback",
            "meta": {
                "acquisition_mode": "sourced",
                "fallback_for": visual_asset_id,
                "fallback_policy": SOURCED_VISUAL_ASSET_FALLBACK_POLICY,
                "candidate_manifest_path": SOURCED_VISUAL_ASSET_CANDIDATE_MANIFEST_PATH,
                "manifest_path": VISUAL_ASSET_MANIFEST_PATH,
                "manifest_schema": VISUAL_ASSET_MANIFEST_SCHEMA,
                "asset_record_required_fields": SOURCED_VISUAL_ASSET_RECORD_REQUIRED_FIELDS,
                "hotlinking_allowed": False,
                "workspace_copy_required": True,
                "license_metadata_required": True,
                "contract_id": sourced_visual_asset_contract_id,
            },
        }
    )
    edges.append({"type": "governs", "from": visual_asset_contract_id, "to": image_model_id})
    edges.append({"type": "governs", "from": visual_asset_contract_id, "to": visual_asset_id})
    edges.append({"type": "governs", "from": sourced_visual_asset_contract_id, "to": sourced_visual_asset_id})
    edges.append({"type": "governs", "from": sourced_visual_asset_contract_id, "to": "visual-asset-provider:openverse"})
    edges.append({"type": "governs", "from": sourced_visual_asset_contract_id, "to": "license-policy:verified-free-visual-asset"})
    edges.append({"type": "generated_with", "from": visual_asset_id, "to": image_model_id})
    edges.append({"type": "sourced_from", "from": sourced_visual_asset_id, "to": "visual-asset-provider:openverse"})
    edges.append({"type": "licensed_under", "from": sourced_visual_asset_id, "to": "license-policy:verified-free-visual-asset"})
    edges.append({"type": "grounded_in", "from": visual_asset_id, "to": brand_id})
    edges.append({"type": "grounded_in", "from": sourced_visual_asset_id, "to": brand_id})

    component_meta_by_name = {
        component.get("name"): component
        for component in component_inventory.get("components", [])
        if component.get("name")
    }

    for family in component_inventory.get("families", []):
        family_id = f"component-family:{family['family']}"
        nodes.append({"id": family_id, "type": "ComponentFamily", "label": family["family"]})
        for component_name in family.get("components", []):
            component_id = f"component:{slugify_text(component_name)}"
            meta = component_meta_by_name.get(component_name, {})
            node = {"id": component_id, "type": "Component", "label": component_name}
            if meta.get("advanced_component"):
                node["meta"] = {
                    "advanced_component": True,
                    "usage_guidance": meta.get("usage_guidance", []),
                    "pairs_with": meta.get("pairs_with", []),
                    "matched_signals": meta.get("matched_signals", []),
                }
            nodes.append(node)
            edges.append({"type": "composed_of", "from": family_id, "to": component_id})

    for primitive in brand_profile.get("product_primitives", []):
        primitive_id = f"primitive:{slugify_text(primitive)}"
        nodes.append({"id": primitive_id, "type": "ProductPrimitive", "label": primitive})
        for component in component_inventory.get("components", []):
            if component["supports_primitive"] == primitive:
                edges.append(
                    {
                        "type": "supports",
                        "from": f"component:{slugify_text(component['name'])}",
                        "to": primitive_id,
                    }
                )

    for target in blueprint.get("reference_strategy", {}).get("top_sources_by_concept_coverage", []):
        ref_id = f"source:{slugify_text(target['source_label'])}"
        nodes.append({"id": ref_id, "type": "SourceReference", "label": target["source_label"]})
        edges.append({"type": "inspired_by", "from": brand_id, "to": ref_id})

    governance = blueprint.get("governance", {})
    reference_scope = governance.get("reference_absorption_scope", {})
    scope_id = "governance:reference-absorption-scope"
    nodes.append(
        {
            "id": scope_id,
            "type": "GovernanceRule",
            "label": "Reference absorption scope",
            "meta": {
                "rule": reference_scope.get("rule", ""),
                "allowed": reference_scope.get("allowed", []),
                "denied": reference_scope.get("denied", []),
            },
        }
    )
    edges.append({"type": "grounded_in", "from": scope_id, "to": brand_id})
    for layer in ["color", "typography"]:
        edges.append({"type": "enforces", "from": scope_id, "to": f"token-category:{layer}"})
    for pattern in reference_scope.get("failure_patterns", []):
        pattern_id = f"failure-pattern:{slugify_text(pattern.get('id', 'implementation-failure'))}"
        nodes.append(
            {
                "id": pattern_id,
                "type": "ImplementationFailurePattern",
                "label": pattern.get("id", "implementation failure"),
                "meta": pattern,
            }
        )
        edges.append({"type": "prevents", "from": scope_id, "to": pattern_id})

    return {
        "entity_types": [
            "Brand",
            "Principle",
            "TokenCategory",
            "Token",
            "ComponentFamily",
            "Component",
            "ProductPrimitive",
            "SourceReference",
            "AccessibilityRule",
            "GeneratedVisualAsset",
            "ImageGenerationModel",
            "SourcedVisualAsset",
            "VisualAssetProvider",
            "FreeSourcedVisualProvider",
            "LicensedVisualProvider",
            "ReferenceOnlyProvider",
            "LicensePolicy",
            "GovernanceRule",
            "ImplementationFailurePattern",
        ],
        "relation_types": ONTOLOGY_RELATIONS,
        "nodes": _dedupe_nodes(nodes),
        "edges": _dedupe_edges(edges),
    }


def build_system_spec_markdown(
    brand_profile: dict,
    blueprint: dict,
    validation: dict,
    foundations: list[dict],
    token_schema: dict,
    component_inventory: dict,
    documents: list[DocumentRecord],
    css_extraction: dict | None = None,
    graph_sections: str = "",
) -> str:
    source_count = len({document.reference_slug for document in documents if not document.error})
    principle_lines = "\n".join(
        f"- **{principle['name']}**: {principle['rule']}"
        for principle in blueprint.get("principles", [])
    )
    foundation_lines = "\n".join(
        f"- **{foundation['name']}** ({foundation['priority']}): signal {foundation['signal_count']}"
        for foundation in foundations
    )
    governance = blueprint.get("governance", {})
    implementation_guardrail_lines = "\n".join(
        f"- {line}"
        for line in governance.get("implementation_guardrails", [])
    ) or "- No implementation guardrails defined."
    family_lines = "\n".join(
        (
            f"- **{family['family']}**: {', '.join(family.get('components', [])[:8]) or 'TBD'}"
            + (
                " / visual signals: "
                + ", ".join(
                    f"{signal.get('label')} ({signal.get('confidence')})"
                    for signal in family.get("visual_reference_signals", [])[:2]
                )
                if family.get("visual_reference_signals")
                else ""
            )
        )
        for family in component_inventory.get("families", [])
    )
    archetype_lines = "\n".join(
        f"- **{item.get('label')}** ({item.get('family')} / {item.get('confidence')}): "
        f"{', '.join(item.get('suggested_components', [])[:5])}"
        for item in component_inventory.get("candidate_component_archetypes", [])[:6]
    ) or "- No visual-reference archetypes suggested."
    advanced_component_lines = "\n".join(
        f"- **{item.get('name')}** ({item.get('family')}, score {item.get('score')}): "
        f"{'; '.join(item.get('use_when', [])[:2])}"
        + (
            f" / pairs with: {', '.join(item.get('pairs_with', [])[:4])}"
            if item.get("pairs_with")
            else ""
        )
        for item in component_inventory.get("advanced_recommendations", [])[:8]
    ) or "- No advanced components recommended from this product context."
    reference_baseline = component_inventory.get("reference_baseline") or {}
    reference_baseline_systems = ", ".join(
        f"{system.get('name')} ({system.get('url')})"
        for system in reference_baseline.get("systems", [])
    ) or "No reference baseline recorded."
    reference_baseline_policy = (
        (reference_baseline.get("absorption_policy") or {}).get("rule")
        or "Use external systems only as advisory taxonomy evidence."
    )
    contextual_not_baseline = ", ".join(
        sorted((reference_baseline.get("contextual_not_baseline") or {}).keys())
    ) or "None"
    color_reference = brand_profile.get("_resolved_color_reference")
    visual_reference = brand_profile.get("_resolved_visual_reference")
    color_reference_lines = _build_color_reference_section(color_reference)
    visual_reference_lines = _build_visual_reference_section(visual_reference)
    design_context_lines = _build_design_context_pack_section(
        blueprint.get("design_context_pack") or brand_profile.get("_design_context_pack")
    )
    validation_lines = "\n".join(
        [f"- Error: {message}" for message in validation.get("errors", [])]
        + [f"- Warning: {message}" for message in validation.get("warnings", [])]
    ) or "- No validation issues."
    ai_synthesis_lines = "\n".join(
        f"- **{principle['rule']}**: {principle['detail']}"
        for principle in governance.get("ai_synthesis_principles", [])
    ) or "- No AI synthesis principles defined."
    reference_scope = governance.get("reference_absorption_scope", {})
    allowed_reference_lines = "\n".join(
        f"  - {item}" for item in reference_scope.get("allowed", [])
    ) or "  - No allowed reference scope defined."
    denied_reference_lines = "\n".join(
        f"  - {item}" for item in reference_scope.get("denied", [])
    ) or "  - No denied reference scope defined."
    failure_pattern_lines = "\n".join(
        f"  - **{item.get('id', 'failure-pattern')}**: {item.get('rule', '')} Prevention: {item.get('prevention', '')}"
        for item in reference_scope.get("failure_patterns", [])
    ) or "  - No promoted failure patterns defined."
    promotion_policy = (
        governance.get("feedback_promotion_policy")
        or reference_scope.get("promotion_policy", {})
    )
    promotion_policy_line = (
        f"- Feedback promotion: {promotion_policy.get('rule')} Outputs: {', '.join(promotion_policy.get('outputs', []))}"
        if promotion_policy
        else "- Feedback promotion: No promotion policy defined."
    )
    reference_scope_rule = reference_scope.get(
        "rule",
        "References are advisory and never replace token/component/product IA authority.",
    )
    color_mode_policy = governance.get("color_mode_parity_policy", {})
    color_mode_rules = "\n".join(
        f"- {item}" for item in color_mode_policy.get("implementation_rules", [])
    ) or "- No color mode parity rules defined."
    color_mode_failures = "\n".join(
        f"- **{item.get('id', 'dark-only-implementation')}**: {item.get('rule', '')} Prevention: {item.get('prevention', '')}"
        for item in color_mode_policy.get("failure_patterns", [])
    ) or "- No color mode failure patterns defined."
    color_mode_section = f"""### Color Mode Parity

- **Rule**: {color_mode_policy.get('rule', 'Every product UI needs light and dark modes.')}
- **Required modes**: {', '.join(color_mode_policy.get('required_modes', ['light', 'dark']))}
- **Default mode**: {color_mode_policy.get('default_mode', 'light')}
- **Implementation rules**:
{color_mode_rules}
- **Promoted color mode failure patterns**:
{color_mode_failures}"""
    responsive_policy = governance.get("responsive_resilience_policy", {})
    responsive_contract = responsive_policy.get("viewport_contract", {})
    responsive_widths = responsive_contract.get("required_widths_px", [320, 360, 390, 430, 768, 1024, 1440])
    responsive_control_lines = "\n".join(
        f"- {item}" for item in responsive_policy.get("control_rules", [])
    ) or "- No responsive control rules defined."
    responsive_failure_lines = "\n".join(
        f"- **{item.get('id', 'responsive-failure')}**: {item.get('rule', '')} Prevention: {item.get('prevention', '')}"
        for item in responsive_policy.get("failure_patterns", [])
    ) or "- No responsive failure patterns defined."
    responsive_section = f"""### Responsive Resilience

- **Viewport contract**: verify {', '.join(str(width) + 'px' for width in responsive_widths)}.
- **Pass condition**: {responsive_contract.get('pass_condition', 'scrollWidth <= innerWidth and primary controls stay reachable.')}
- **Control rules**:
{responsive_control_lines}
- **Promoted responsive failure patterns**:
{responsive_failure_lines}"""
    icon_policy = governance.get("icon_refactor_policy", {})
    icon_targets = ", ".join(icon_policy.get("targets", [])) or "button, card, badge, navigation, status UI"
    icon_replacement_lines = "\n".join(
        f"- {item}" for item in icon_policy.get("replacement_order", [])
    ) or "- Use existing icon library, local SVG components, or create a minimal SVG asset."
    icon_quality = icon_policy.get("quality_floor", {})
    icon_quality_lines = "\n".join(
        f"- {item}" for item in icon_quality.get("required_grammar", [])
    ) or "- No icon quality grammar defined."
    icon_rule_lines = "\n".join(
        f"- {item}" for item in icon_policy.get("implementation_rules", [])
    ) or "- No icon refactor implementation rules defined."
    icon_failure_lines = "\n".join(
        f"- **{item.get('id', 'emoji-ui-affordance')}**: {item.get('rule', '')} Prevention: {item.get('prevention', '')}"
        for item in icon_policy.get("failure_patterns", [])
    ) or "- No icon refactor failure patterns defined."
    icon_refactor_section = f"""### Emoji-to-SVG Refactor

- **Rule**: {icon_policy.get('rule', 'Replace emoji UI affordances with SVG icons during refactors.')}
- **Targets**: {icon_targets}
- **Replacement order**:
{icon_replacement_lines}
- **Quality floor**: {icon_quality.get('rule', 'Use an approved icon system or documented icon grammar.')}
{icon_quality_lines}
- **Implementation rules**:
{icon_rule_lines}
- **Promoted icon failure patterns**:
{icon_failure_lines}"""
    app_icon_policy = governance.get("app_icon_identity_policy", {})
    app_icon_assets = "\n".join(
        f"- **{item.get('label', 'Brand app icon')}**: targets {', '.join(item.get('targets', []))}; formats {', '.join(item.get('formats', []))}"
        for item in app_icon_policy.get("required_assets", [])
    ) or "- No app icon identity assets defined."
    app_icon_rules = "\n".join(
        f"- {item}" for item in app_icon_policy.get("implementation_rules", [])
    ) or "- No app icon implementation rules defined."
    app_icon_failures = "\n".join(
        f"- **{item.get('id', 'generic-initials-app-icon')}**: {item.get('rule', '')} Prevention: {item.get('prevention', '')}"
        for item in app_icon_policy.get("failure_patterns", [])
    ) or "- No app icon failure patterns defined."
    app_icon_section = f"""### Brand App Icon Identity

- **Rule**: {app_icon_policy.get('rule', 'Every app or website implementation must include a brand-specific app icon identity asset.')}
- **Required assets**:
{app_icon_assets}
- **Implementation rules**:
{app_icon_rules}
- **Promoted app icon failure patterns**:
{app_icon_failures}"""
    visual_substance_policy = governance.get("mockup_visual_substance_policy", {})
    visual_substance_applies_to = ", ".join(visual_substance_policy.get("applies_to", [])) or "website, landing, product, venue, editorial, content-led mockups"
    visual_substance_diagnosis_lines = "\n".join(
        f"- {item}" for item in visual_substance_policy.get("diagnosis", [])
    ) or "- No mockup visual substance diagnosis defined."
    visual_substance_signal_lines = "\n".join(
        f"- {item}" for item in visual_substance_policy.get("required_signals", [])
    ) or "- No mockup visual substance signals defined."
    visual_substance_order_lines = "\n".join(
        f"- {item}" for item in visual_substance_policy.get("image_acquisition_order", [])
    ) or "- Use user-supplied, generated, sourced, or deterministic identity assets as appropriate."
    visual_substance_rule_lines = "\n".join(
        f"- {item}" for item in visual_substance_policy.get("implementation_rules", [])
    ) or "- No mockup visual substance implementation rules defined."
    visual_substance_failure_lines = "\n".join(
        f"- **{item.get('id', 'mockup-visual-substance-failure')}**: {item.get('rule', '')} Prevention: {item.get('prevention', '')}"
        for item in visual_substance_policy.get("failure_patterns", [])
    ) or "- No mockup visual substance failure patterns defined."
    visual_substance_section = f"""### Mockup Visual Substance

- **Rule**: {visual_substance_policy.get('rule', 'Commercial mockups should use relevant visual assets by default.')}
- **Applies to**: {visual_substance_applies_to}
- **Why image-free mockups fail**:
{visual_substance_diagnosis_lines}
- **Required visual substance signals**:
{visual_substance_signal_lines}
- **Image acquisition order**:
{visual_substance_order_lines}
- **Implementation rules**:
{visual_substance_rule_lines}
- **Promoted visual substance failure patterns**:
{visual_substance_failure_lines}"""
    html_prototype_policy = governance.get("html_prototype_contract_policy", {})
    html_prototype_applies_to = ", ".join(html_prototype_policy.get("applies_to", [])) or "static HTML mockups, product workflow prototypes"
    html_prototype_contract_lines = "\n".join(
        f"- {item}" for item in html_prototype_policy.get("required_contracts", [])
    ) or "- No HTML prototype contracts defined."
    html_prototype_rule_lines = "\n".join(
        f"- {item}" for item in html_prototype_policy.get("implementation_rules", [])
    ) or "- No HTML prototype implementation rules defined."
    html_prototype_loop_lines = "\n".join(
        f"- **{item.get('step', 'loop')}**: {item.get('rule', '')}"
        for item in html_prototype_policy.get("improvement_loop", [])
        if isinstance(item, dict)
    ) or "- No HTML prototype improvement loop defined."
    html_prototype_failure_lines = "\n".join(
        f"- **{item.get('id', 'html-prototype-failure')}**: {item.get('rule', '')} Prevention: {item.get('prevention', '')}"
        for item in html_prototype_policy.get("failure_patterns", [])
    ) or "- No HTML prototype failure patterns defined."
    html_prototype_section = f"""### HTML Prototype Contract

- **Rule**: {html_prototype_policy.get('rule', 'HTML mockups must behave as thin executable product prototypes.')}
- **Applies to**: {html_prototype_applies_to}
- **Required contracts**:
{html_prototype_contract_lines}
- **Implementation rules**:
{html_prototype_rule_lines}
- **Improvement loop**:
{html_prototype_loop_lines}
- **Promoted prototype failure patterns**:
{html_prototype_failure_lines}"""
    visual_medium_policy = governance.get("visual_asset_medium_selection_policy", {})
    visual_medium_override_lines = "\n".join(
        (
            f"- **{item.get('id', 'medium-override')}**: priority {item.get('priority', 'highest')}; "
            f"required {item.get('required_medium', '')}; denied {', '.join(item.get('denied_formats', []))}; "
            f"triggers {', '.join(item.get('trigger_phrases', [])[:6])}"
        )
        for item in visual_medium_policy.get("directive_overrides", [])
        if isinstance(item, dict)
    ) or "- No explicit medium directive overrides defined."
    visual_medium_decision_lines = "\n".join(
        f"- {item}" for item in visual_medium_policy.get("decision_sequence", [])
    ) or "- Classify visual slots before choosing an asset medium."
    visual_medium_family_lines = "\n".join(
        f"- **{item.get('id', 'slot-family')}**: modes {', '.join(item.get('default_acquisition_modes', []))}; examples {', '.join(item.get('examples', []))}; SVG: {item.get('deterministic_svg', '')}"
        for item in visual_medium_policy.get("slot_families", [])
    ) or "- No medium selection slot families defined."
    visual_medium_rule_lines = "\n".join(
        f"- {item}" for item in visual_medium_policy.get("implementation_rules", [])
    ) or "- No visual medium selection rules defined."
    visual_medium_failure_lines = "\n".join(
        f"- **{item.get('id', 'visual-asset-medium-failure')}**: {item.get('rule', '')} Prevention: {item.get('prevention', '')}"
        for item in visual_medium_policy.get("failure_patterns", [])
    ) or "- No visual medium failure patterns defined."
    visual_medium_section = f"""### Visual Asset Medium Selection

- **Rule**: {visual_medium_policy.get('rule', 'Choose visual asset medium according to slot role and subject matter.')}
- **Directive overrides**:
{visual_medium_override_lines}
- **Decision sequence**:
{visual_medium_decision_lines}
- **Slot family defaults**:
{visual_medium_family_lines}
- **Implementation rules**:
{visual_medium_rule_lines}
- **Promoted medium failure patterns**:
{visual_medium_failure_lines}"""
    commercial_policy = governance.get("commercial_product_realism_policy", {})
    commercial_applies_to = ", ".join(commercial_policy.get("applies_to", [])) or "dashboard, tool, data product, operational UI"
    commercial_diagnosis_lines = "\n".join(
        f"- {item}" for item in commercial_policy.get("diagnosis", [])
    ) or "- No commercial realism diagnosis defined."
    commercial_signal_lines = "\n".join(
        f"- {item}" for item in commercial_policy.get("required_signals", [])
    ) or "- No commercial realism signals defined."
    commercial_success_lines = "\n".join(
        f"- **{item.get('id', 'successful-pattern')}**: {item.get('rule', '')} Implementation: {item.get('implementation', '')} Verification: {item.get('verification', '')}"
        for item in commercial_policy.get("successful_patterns", [])
    ) or "- No commercial realism success patterns defined."
    commercial_rule_lines = "\n".join(
        f"- {item}" for item in commercial_policy.get("implementation_rules", [])
    ) or "- No commercial realism implementation rules defined."
    commercial_failure_lines = "\n".join(
        f"- **{item.get('id', 'commercial-product-realism-failure')}**: {item.get('rule', '')} Prevention: {item.get('prevention', '')}"
        for item in commercial_policy.get("failure_patterns", [])
    ) or "- No commercial realism failure patterns defined."
    commercial_section = f"""### Commercial Product Realism

- **Rule**: {commercial_policy.get('rule', 'Product UI should lead with operational substance rather than presentation-only composition.')}
- **Applies to**: {commercial_applies_to}
- **Why AI-looking screens fail**:
{commercial_diagnosis_lines}
- **Required realism signals**:
{commercial_signal_lines}
- **Successful reusable patterns**:
{commercial_success_lines}
- **Implementation rules**:
{commercial_rule_lines}
- **Promoted realism failure patterns**:
{commercial_failure_lines}"""
    concept_lines = "\n".join(
        f"- **{target['concept_id']}**: {target['count']}"
        for target in blueprint.get("ontology_targets", [])
    )
    application_concept_section = _build_application_concept_section(
        blueprint.get("application_concept") or {},
        blueprint.get("differentiation_strategy") or {},
    )
    layout_skeleton_section = _build_layout_skeleton_section(
        blueprint.get("layout_skeleton") or {}
    )

    quick_start_section = _build_quick_start_section(brand_profile, token_schema, color_reference)
    do_dont_section = _build_do_dont_section(brand_profile, blueprint)
    drop_in_css_section = _build_drop_in_css_section(brand_profile, token_schema, color_reference)
    css_extraction_section = _build_css_extraction_section(css_extraction)

    return f"""# {blueprint.get('system_name', 'Design System')} Spec

## 1. Positioning

- **Brand**: {brand_profile.get('brand_name', '')}
- **Product**: {brand_profile.get('product_summary', '')}
- **Audience**: {', '.join(brand_profile.get('audiences', []))}
- **Platforms**: {', '.join(brand_profile.get('platforms', []))}
- **Accessibility floor**: {', '.join(brand_profile.get('accessibility_targets', []))}

### Application Concept

{application_concept_section}

### Layout Skeleton

{layout_skeleton_section}

## 2. Identity Guardrails

- **Brand keywords**: {', '.join(brand_profile.get('brand_keywords', []))}
- **Anti-keywords**: {', '.join(brand_profile.get('anti_keywords', []))}
- **Tone of voice**: {', '.join(brand_profile.get('tone_of_voice', []))}
- **Visual direction**: {', '.join(brand_profile.get('visual_keywords', []))}
- **Interaction direction**: {', '.join(brand_profile.get('interaction_keywords', []))}

## 3. Design Principles

{principle_lines}

## 4. Foundation Priorities

{foundation_lines}

## 5. Token Strategy

- **Layering**: core -> semantic -> component
- **Core categories**: {', '.join(token_schema['layers'][0]['categories'])}
- **Semantic categories**: {', '.join(token_schema['layers'][1]['categories'])}
- **Component categories**: {', '.join(token_schema['layers'][2]['categories'])}
- **Typography families**: {', '.join(token_schema['categories']['typography']['families'])}
- **Spacing scale**: {', '.join(str(item) for item in token_schema['categories']['spacing']['scale'])}

{_build_typography_section(token_schema['categories']['typography'])}

## 6. Color Reference

{color_reference_lines}

## 7. Visual Reference Signals

{visual_reference_lines}

### Design Context Pack

{design_context_lines}

## 8. Component Strategy

- **Product primitives**: {', '.join(brand_profile.get('product_primitives', []))}
- **Required families**: {', '.join(item['family'] for item in component_inventory.get('families', []))}
- **Reference baseline**: {reference_baseline_systems}
- **Reference absorption rule**: {reference_baseline_policy}
- **Contextual, not baseline**: {contextual_not_baseline}
- **Advanced component recommendations**:

{advanced_component_lines}

- **Visual-reference archetypes**:

{archetype_lines}

{family_lines}

## 9. Implementation Guardrails

{implementation_guardrail_lines}

{color_mode_section}

{responsive_section}

{icon_refactor_section}

{app_icon_section}

{visual_substance_section}

{html_prototype_section}

{visual_medium_section}

{commercial_section}

## 10. Reference Absorption Rule

- Analysed live reference sources: {source_count}
- Rule: copy visuals from no single source; absorb patterns only when they reinforce brand keywords and avoid anti-keywords.
- Use references to validate structure, accessibility, token discipline, and documentation quality.
- Scope rule: {reference_scope_rule}
- Allowed from references:
{allowed_reference_lines}
- Denied from references:
{denied_reference_lines}
- Promoted failure patterns:
{failure_pattern_lines}
{promotion_policy_line}

## 11. AI Synthesis Principles

{ai_synthesis_lines}

## 12. Ontology Targets

{concept_lines}

## 13. Profile Validation

{validation_lines}

## 14. Quick Start

{quick_start_section}

## 15. DO / DON'T

{do_dont_section}

## 16. Drop-in CSS

{drop_in_css_section}

## 17. CSS Extraction Summary

{css_extraction_section}

{graph_sections}"""


def _dedupe_nodes(nodes: list[dict]) -> list[dict]:
    seen: set[str] = set()
    result = []
    for node in nodes:
        if node["id"] in seen:
            continue
        seen.add(node["id"])
        result.append(node)
    return result


def _dedupe_edges(edges: list[dict]) -> list[dict]:
    seen: set[tuple[str, str, str]] = set()
    result = []
    for edge in edges:
        key = (edge["type"], edge["from"], edge["to"])
        if key in seen:
            continue
        seen.add(key)
        result.append(edge)
    return result


def slugify_text(value: str) -> str:
    return "".join(ch.lower() if ch.isalnum() else "-" for ch in value).strip("-")


def _build_typography_category(editorial_system: bool, font_system: dict | None) -> dict:
    base = {
        "families": ["display", "text", "mono"] if editorial_system else ["brand", "text", "mono"],
        "size_scale": ["xs", "sm", "md", "lg", "xl", "2xl", "3xl", "4xl"],
        "rules": [
            "display는 마케팅/영웅 구역으로 제한",
            "text는 제품 본문과 UI 라벨의 기본",
            "mono는 데이터와 shortcut hint에 제한",
        ],
    }
    if not font_system:
        return base

    heading = font_system.get("heading") or {}
    body = font_system.get("body") or {}
    mono = font_system.get("mono")
    korean = font_system.get("korean")
    type_scale = font_system.get("type_scale", {})

    base["recommended_fonts"] = {
        "heading": heading.get("name"),
        "body": body.get("name"),
        "mono": mono.get("name") if mono else None,
        "korean": korean.get("name") if korean else None,
    }
    base["heading_note"] = heading.get("note", "")
    base["body_note"] = body.get("note", "")
    base["product_type"] = font_system.get("product_type_detected", "")
    base["pairing_source"] = font_system.get("pairing_source", "")
    base["line_height_preset"] = font_system.get("line_height_preset", "normal")
    base["strategy"] = font_system.get("strategy", [])
    base["loading"] = font_system.get("loading", {})
    base["korean_rationale"] = font_system.get("korean_rationale")
    base["pitfall_warnings"] = font_system.get("pitfall_warnings", [])
    base["letter_spacing"] = font_system.get("letter_spacing")

    script_guardrails = font_system.get("script_guardrails")
    if script_guardrails:
        base["script_guardrails"] = script_guardrails
        base["rules"].extend(script_guardrails.get("rules", []))

    if type_scale:
        base["type_scale"] = {
            "base_size": type_scale.get("base"),
            "scale_ratio": type_scale.get("scale_ratio"),
            "sizes": type_scale.get("sizes", {}),
            "line_heights": type_scale.get("line_heights", {}),
        }

    return base


def _markdown_list(items: list | tuple, fallback: str = "Not specified.") -> str:
    lines = [f"- {item}" for item in items if str(item).strip()]
    return "\n".join(lines) if lines else f"- {fallback}"


def _build_application_concept_section(application_concept: dict, differentiation_strategy: dict) -> str:
    domain_objects = application_concept.get("domain_objects") or []
    differentiation = application_concept.get("differentiation") or []
    signature_moves = differentiation_strategy.get("signature_moves") or []
    repetition_risks = differentiation_strategy.get("repetition_risks") or []
    must_differ = differentiation_strategy.get("must_feel_different_from") or []
    return f"""- **Primary job**: {application_concept.get('primary_job', 'Not specified.')}
- **Operating mode**: {application_concept.get('operating_mode', 'Not specified.')}
- **Success moment**: {application_concept.get('success_moment', 'Not specified.')}
- **Domain objects**:
{_markdown_list(domain_objects)}
- **Differentiation intent**:
{_markdown_list(differentiation)}
- **Must feel different from**:
{_markdown_list(must_differ)}
- **Signature structural moves**:
{_markdown_list(signature_moves)}
- **Repetition risks**:
{_markdown_list(repetition_risks)}
- **Anti-convergence rule**: {differentiation_strategy.get('anti_convergence_rule', 'The first screen must not collapse into a generic template.')}"""


def _build_layout_skeleton_section(layout_skeleton: dict) -> str:
    primary_regions = layout_skeleton.get("primary_regions") or []
    region_lines = []
    for region in primary_regions:
        if isinstance(region, dict):
            region_lines.append(
                "- "
                f"**{region.get('name', 'Unnamed region')}** "
                f"({region.get('priority', 'secondary')}): {region.get('role', '')}"
            )
        else:
            region_lines.append(f"- {region}")
    return f"""- **Composition**: {layout_skeleton.get('composition', 'task-led-product-surface')}
- **Navigation model**: {layout_skeleton.get('navigation_model', 'contextual')}
- **Density**: {layout_skeleton.get('density', 'balanced')}
- **Primary regions**:
{chr(10).join(region_lines) if region_lines else '- Primary task surface'}
- **First-screen contract**:
{_markdown_list(layout_skeleton.get('first_screen_contract') or [])}
- **Avoid layouts**:
{_markdown_list(layout_skeleton.get('avoid_layouts') or [])}"""


def _build_typography_section(typography: dict) -> str:
    fonts = typography.get("recommended_fonts")
    if not fonts:
        return ""

    lines = ["### Typography System (auto-resolved)\n"]
    lines.append(f"- **Heading**: {fonts.get('heading', 'N/A')}")
    lines.append(f"- **Body**: {fonts.get('body', 'N/A')}")
    if fonts.get("korean"):
        lines.append(f"- **Korean**: {fonts.get('korean')}")
    if fonts.get("mono"):
        lines.append(f"- **Mono**: {fonts.get('mono')}")

    if typography.get("product_type"):
        lines.append(f"- **Product type detected**: {typography['product_type']}")
    if typography.get("pairing_source"):
        lines.append(f"- **Pairing source**: {typography['pairing_source']}")
    if typography.get("line_height_preset"):
        lines.append(f"- **Line height**: {typography['line_height_preset']}")

    type_scale = typography.get("type_scale", {})
    if type_scale:
        sizes = type_scale.get("sizes", {})
        if sizes:
            scale_str = ", ".join(f"{k}={v}px" for k, v in sizes.items())
            lines.append(f"- **Type scale**: base {type_scale.get('base_size', '?')}px, ratio {type_scale.get('scale_ratio', '?')} ({scale_str})")

    strategy = typography.get("strategy", [])
    if strategy:
        lines.append("- **Strategy**:")
        for note in strategy:
            lines.append(f"  - {note}")

    heading_note = typography.get("heading_note")
    body_note = typography.get("body_note")
    if heading_note:
        lines.append(f"- **Heading note**: {heading_note}")
    if body_note:
        lines.append(f"- **Body note**: {body_note}")

    korean_rationale = typography.get("korean_rationale") or {}
    if korean_rationale:
        lines.append(
            "- **Korean rationale**: "
            f"{korean_rationale.get('font', 'N/A')} — {korean_rationale.get('reason', '')}"
        )

    letter_spacing = typography.get("letter_spacing") or {}
    heading_tracking = (letter_spacing.get("heading_tracking") or {})
    if heading_tracking:
        tracking_str = ", ".join(f"{k}={v}" for k, v in heading_tracking.items())
        lines.append(f"- **Heading tracking**: {tracking_str}")

    script_guardrails = typography.get("script_guardrails") or {}
    if script_guardrails:
        headline_font = script_guardrails.get("headline_font") or {}
        body_font = script_guardrails.get("body_font") or {}
        wrap = script_guardrails.get("wrap") or {}
        headline_wrap = wrap.get("headline") or {}
        body_wrap = wrap.get("body") or {}

        lines.append(f"- **Primary script**: {script_guardrails.get('primary_script', 'N/A')}")
        lines.append(
            "- **Hangul headline defaults**: "
            f"{headline_font.get('name', 'N/A')} | line-height {headline_font.get('line_height', 'n/a')} | "
            f"tracking {headline_font.get('letter_spacing', 'n/a')}"
        )
        lines.append(
            "- **Hangul body defaults**: "
            f"{body_font.get('name', 'N/A')} | line-height {body_font.get('line_height', 'n/a')} | "
            f"label line-height {body_font.get('ui_label_line_height', 'n/a')}"
        )
        lines.append(
            "- **Wrap defaults**: "
            f"headline word-break={headline_wrap.get('word_break', 'n/a')}, "
            f"headline text-wrap={headline_wrap.get('text_wrap', 'n/a')}, "
            f"body word-break={body_wrap.get('word_break', 'n/a')}"
        )
        scale = script_guardrails.get("scale") or {}
        if scale.get("guidance"):
            lines.append(f"- **Scale guidance**: {scale['guidance']}")
        constraints = (script_guardrails.get("implementation_constraints") or {}).get("headline_display") or {}
        if constraints:
            lines.append(
                "- **Hangul display safety**: "
                f"line-height >= {constraints.get('line_height_min', 'n/a')} | "
                f"tracking {constraints.get('letter_spacing_min', 'n/a')} to {constraints.get('letter_spacing_max', 'n/a')} | "
                "forced <br /> 금지 until breakpoint QA"
            )
        for warning in script_guardrails.get("warnings", [])[:3]:
            lines.append(f"- **Hangul warning**: {warning}")

    loading = typography.get("loading", {})
    if loading.get("fonts"):
        font_list = ", ".join(f"{f['font']}({f['priority']})" for f in loading["fonts"])
        lines.append(f"- **Loading**: {font_list} | display: {loading.get('display', 'swap')}")

    pitfall_warnings = typography.get("pitfall_warnings", [])
    for warning in pitfall_warnings[:3]:
        lines.append(f"- **Pitfall warning**: {warning}")

    return "\n".join(lines)


def _build_color_reference_section(color_reference: dict | None) -> str:
    if not color_reference:
        return "- No curated color reference connected."

    lines = [
        f"- **Source**: {color_reference.get('title', 'Color Reference')} ({color_reference.get('source_path', '')})",
    ]
    if color_reference.get("selection_mode"):
        lines.append(f"- **Selection mode**: {color_reference.get('selection_mode')}")
    preferred_families = color_reference.get("preferred_families", [])
    if preferred_families:
        lines.append(f"- **Preferred families**: {', '.join(preferred_families)}")
    strategy = color_reference.get("strategy", {})
    if strategy:
        lines.append(
            "- **Palette strategy**: "
            f"temperature={strategy.get('temperature')}, "
            f"contrast={strategy.get('contrast')}, "
            f"diversity={strategy.get('diversity')}, "
            f"surface_style={strategy.get('surface_style')}"
        )
    expansion = color_reference.get("expansion", {})
    if expansion:
        lines.append(
            "- **Palette expansion**: "
            f"supporting_color_count={expansion.get('supporting_color_count')}, "
            f"combination_count={expansion.get('combination_count')}, "
            f"prefer_pairings={expansion.get('prefer_pairings')}"
        )

    active_palette = color_reference.get("active_palette", {}) or {}
    palette_roles = active_palette.get("roles") or color_reference.get("palette_roles", {})
    if palette_roles:
        candidate_id = active_palette.get("candidate_id")
        label = "Active palette" if candidate_id else "Palette roles"
        if candidate_id:
            lines.append(f"- **{label}**: {candidate_id}")
        else:
            lines.append(f"- **{label}**:")
        if candidate_id:
            lines.append("- **Active roles**:")
        for role, item in palette_roles.items():
            lines.append(
                f"  - `{role}` -> {item.get('name')} {item.get('hex', '')} / {item.get('family', '')}"
            )

    selected_colors = color_reference.get("selected_colors", [])
    if selected_colors:
        lines.append("- **Selected colors**:")
        for item in selected_colors[:6]:
            mood = item.get("mood") or ""
            lines.append(
                f"  - {item.get('name')} {item.get('hex', '')} / {item.get('family', '')} / {mood}"
            )

    palette_candidates = color_reference.get("palette_candidates", [])
    if palette_candidates:
        lines.append("- **Palette candidates**:")
        for candidate in palette_candidates[:4]:
            role_summary = ", ".join(
                f"{role}={item.get('name')}"
                for role, item in candidate.get("roles", {}).items()
            )
            rationale = "; ".join(candidate.get("rationale", [])[:2])
            lines.append(
                f"  - {candidate.get('id')} ({candidate.get('label')}): {role_summary}"
                + (f" / {rationale}" if rationale else "")
            )

    expanded_palette = color_reference.get("expanded_palette", {}) or {}
    supporting_colors = expanded_palette.get("supporting_colors", [])
    if supporting_colors:
        lines.append("- **Expanded supporting colors**:")
        for item in supporting_colors[:8]:
            reasons = "; ".join(item.get("search_reasons", [])[:2])
            lines.append(
                f"  - {item.get('name')} {item.get('hex', '')} / {item.get('family', '')} / {item.get('source_type', '')}"
                + (f" / {reasons}" if reasons else "")
            )

    semantic_roles = expanded_palette.get("semantic_roles", {})
    if semantic_roles:
        lines.append("- **Expanded semantic roles**:")
        for role, item in list(semantic_roles.items())[:10]:
            lines.append(
                f"  - `{role}` -> {item.get('name')} {item.get('hex', '')} / {item.get('family', '')}"
            )

    combination_lists = expanded_palette.get("combination_lists", [])
    if combination_lists:
        lines.append("- **Combination lists**:")
        for combination in combination_lists[:4]:
            color_summary = ", ".join(
                f"{item.get('role')}={item.get('name')}"
                for item in combination.get("colors", [])[:6]
            )
            lines.append(
                f"  - {combination.get('label')}: {color_summary}"
            )

    semantic_selection = color_reference.get("semantic_color_selection", {}) or {}
    if semantic_selection:
        lines.append(
            "- **Semantic color selection**: "
            f"{semantic_selection.get('selection_method', 'ontology-search-per-run')}"
        )
        pattern = semantic_selection.get("matched_pattern") or {}
        if pattern:
            lines.append(
                f"  - matched pattern: `{pattern.get('id')}` / {pattern.get('label')}"
            )
        candidates = semantic_selection.get("candidate_palettes", [])
        if candidates:
            lines.append("- **Ontology-searched candidate palettes**:")
            for candidate in candidates[:5]:
                role_summary = ", ".join(
                    f"{role}={item.get('name')}"
                    for role, item in (candidate.get("roles") or {}).items()
                )
                lines.append(
                    f"  - {candidate.get('id')} ({candidate.get('label')}, score={candidate.get('score')}): "
                    f"{role_summary}"
                )
        rules = semantic_selection.get("rules", [])
        if rules:
            lines.append("- **Selection rules**:")
            for rule in rules[:4]:
                lines.append(f"  - {rule}")

    semantic_ontology = color_reference.get("semantic_ontology", {}) or {}
    if semantic_ontology:
        source = semantic_ontology.get("source", {}) or {}
        lines.append(
            "- **Semantic color ontology**: "
            f"{semantic_ontology.get('node_count', 0)} nodes / "
            f"{semantic_ontology.get('edge_count', 0)} edges"
            + (f" from {source.get('repo')}" if source.get("repo") else "")
        )
        matched_keywords = semantic_ontology.get("matched_keywords", [])
        if matched_keywords:
            lines.append("- **Matched color keywords**:")
            for item in matched_keywords[:6]:
                moods = ", ".join(item.get("mood_tags", [])[:3])
                axes = ", ".join(item.get("tone_axes", [])[:3])
                lines.append(
                    f"  - `{item.get('role')}` -> {item.get('name')} {item.get('hex', '')} "
                    f"/ {item.get('spectrum', '')}.{item.get('family', '')}"
                    + (f" / mood={moods}" if moods else "")
                    + (f" / axes={axes}" if axes else "")
                )
        recommended_keywords = semantic_ontology.get("recommended_keywords", [])
        if recommended_keywords:
            lines.append("- **Ontology keyword recommendations**:")
            for item in recommended_keywords[:5]:
                reasons = "; ".join(item.get("reasons", [])[:2])
                lines.append(
                    f"  - {item.get('name')} {item.get('hex', '')} / {item.get('spectrum', '')}.{item.get('family', '')}"
                    + (f" / {reasons}" if reasons else "")
                )
        guidelines = semantic_ontology.get("guidelines", [])
        if guidelines:
            lines.append("- **Semantic color guardrails**:")
            for item in guidelines[:5]:
                lines.append(f"  - {item.get('label')}: {item.get('summary')}")

    notes = color_reference.get("notes", [])
    if notes:
        lines.append(f"- **Notes**: {', '.join(str(item) for item in notes)}")

    lines.append("- **Application rule**: 레퍼런스 컬러는 semantic token으로 번역해서 사용하고, 접근성과 theme 호환성을 우선합니다.")
    return "\n".join(lines)


def _build_visual_reference_section(visual_reference: dict | None) -> str:
    if not visual_reference:
        return "- No visual reference connected."

    lines = [
        f"- **Mode**: {visual_reference.get('mode', 'local-images')}",
        f"- **Coverage**: source {visual_reference.get('coverage', {}).get('source_count', 0)} / image {visual_reference.get('coverage', {}).get('image_count', 0)} / selected {visual_reference.get('coverage', {}).get('selected_image_count', 0)}",
        "- **Rule**: visual references are advisory signals for motif and layout direction; official KB/spec remain the structural source of truth.",
        "- **Provenance**: `observed` = directly measured from local pixels, `inferred` = synthesized from image/query/brand signals, `unverified` = reliable visual evidence not yet available.",
    ]

    queries = visual_reference.get("query", [])
    if queries:
        lines.append(f"- **Query seeds**: {', '.join(queries[:6])}")

    motifs = visual_reference.get("visual_motifs", {}) or {}
    if motifs:
        lines.append("### Visual Direction\n")
        for key in ["density", "surface_style", "corner_style", "typography_mood"]:
            item = motifs.get(key) or {}
            if not item:
                continue
            evidence = ", ".join(item.get("evidence", [])[:3])
            provenance = ((item.get("provenance") or {}).get("level") or "n/a")
            lines.append(
                f"- **{key.replace('_', ' ').title()}**: {item.get('value')} "
                f"(confidence {item.get('confidence')}, provenance {provenance})"
                + (f" / {evidence}" if evidence else "")
            )
        color_balance = motifs.get("color_balance", {}) or {}
        if color_balance:
            dominant = ", ".join(item.get("hex") for item in color_balance.get("dominant", [])[:4] if item.get("hex"))
            provenance = ((color_balance.get("provenance") or {}).get("level") or "n/a")
            lines.append(
                f"- **Color balance**: temperature={color_balance.get('temperature')}, "
                f"contrast={color_balance.get('contrast_profile')}, "
                f"neutral_bias={color_balance.get('neutral_bias')}, "
                f"provenance={provenance}"
                + (f" / dominant {dominant}" if dominant else "")
            )

    layout_cues = visual_reference.get("layout_cues", [])
    if layout_cues:
        lines.append("\n### Layout Rhythm\n")
        for cue in layout_cues[:4]:
            evidence = ", ".join(cue.get("evidence", [])[:4])
            provenance = ((cue.get("provenance") or {}).get("level") or "n/a")
            lines.append(
                f"- **{cue.get('label')}**: confidence {cue.get('confidence')} / provenance {provenance}"
                + (f" / {evidence}" if evidence else "")
            )

    component_hints = visual_reference.get("component_style_hints", {}) or {}
    if component_hints:
        lines.append("\n### Image-derived Component Hints\n")
        for name, hint in list(component_hints.items())[:6]:
            evidence = ", ".join(hint.get("evidence", [])[:3])
            provenance = ((hint.get("provenance") or {}).get("level") or "n/a")
            lines.append(
                f"- **{name.replace('_', ' ').title()}**: {hint.get('direction')} / provenance {provenance}"
                + (f" / {evidence}" if evidence else "")
            )

    mood_summary = visual_reference.get("reference_mood_summary", {}) or {}
    if mood_summary.get("recommended_direction"):
        lines.append("\n### Synthesis Notes\n")
        for item in mood_summary.get("recommended_direction", [])[:5]:
            lines.append(f"- {item}")
        for item in mood_summary.get("avoidance", [])[:4]:
            lines.append(f"- Avoid: {item}")

    return "\n".join(lines)


def _build_design_context_pack_section(design_context_pack: dict | None) -> str:
    if not design_context_pack:
        return "- No design context pack generated. Connect visual_reference sources or provider plans to ground reference research."

    lines = [
        f"- **Activation**: {design_context_pack.get('activation_state', 'planned')}",
        f"- **Schema**: {design_context_pack.get('schema_version', 'design-context-pack/v1')}",
        f"- **Rule**: {(design_context_pack.get('absorption_policy') or {}).get('rule', 'References stay advisory.')}",
    ]

    providers = design_context_pack.get("providers", []) or []
    if providers:
        lines.append("- **Providers**:")
        for provider in providers[:6]:
            lines.append(
                f"  - `{provider.get('provider_id')}`: {provider.get('status')} / "
                f"{provider.get('access_mode')} / {provider.get('truth_role')}"
            )

    flow_index = design_context_pack.get("flow_index", []) or []
    if flow_index:
        lines.append("- **Flow coverage**:")
        for item in flow_index[:6]:
            providers_text = ", ".join(item.get("providers", [])[:3]) or "no selected provider evidence"
            lines.append(
                f"  - {item.get('flow')}: {item.get('status')} "
                f"({item.get('context_count', 0)} context cards; {providers_text})"
            )

    cards = design_context_pack.get("context_cards", []) or []
    if cards:
        lines.append("- **Context cards**:")
        for card in cards[:5]:
            flows = ", ".join(card.get("flows", [])[:3]) or "general"
            morphology = ", ".join(card.get("morphology", [])[:3]) or "general"
            lines.append(
                f"  - `{card.get('context_id')}` ({card.get('kind')}, {card.get('provenance_level')}): "
                f"{card.get('label')} / flows: {flows} / morphology: {morphology}"
            )

    gaps = design_context_pack.get("research_gaps", []) or []
    if gaps:
        lines.append("- **Research gaps**:")
        for gap in gaps[:4]:
            lines.append(
                f"  - {gap.get('id')} ({gap.get('severity')}): {gap.get('recommended_action')}"
            )

    return "\n".join(lines)


def _build_quick_start_section(
    brand_profile: dict,
    token_schema: dict,
    color_reference: dict | None,
) -> str:
    system_name = brand_profile.get("system_name", "Design System")
    lines = [
        f"이 문서는 **{system_name}**의 디자인 시스템 사양입니다.",
        "",
        "### 시작하기",
        "",
        "1. **토큰 적용**: Drop-in CSS(아래 섹션 16)의 CSS 변수를 프로젝트에 복사합니다.",
        "2. **컬러 세팅**: Color Reference(섹션 6)의 semantic role을 기준으로 surface/text/border를 잡습니다.",
        "3. **타이포 세팅**: Token Strategy(섹션 5)의 font family와 type scale을 적용합니다.",
        "4. **시각 방향 확인**: Visual Reference Signals(섹션 7)에서 density/surface/layout cue를 먼저 확인합니다.",
        "5. **컴포넌트 구현**: Component Strategy(섹션 8)의 family 순서대로 하나씩 빌드합니다.",
        "",
        "### 우선순위",
        "",
    ]
    primitives = brand_profile.get("product_primitives", [])[:5]
    if primitives:
        lines.append(f"핵심 primitive: **{', '.join(primitives)}**")
        lines.append("")
        lines.append("이 primitive를 지원하는 컴포넌트부터 구현하고, 나머지는 필요에 따라 확장합니다.")
    else:
        lines.append("product_primitives를 brand_profile에 정의하면 우선순위가 자동으로 결정됩니다.")
    return "\n".join(lines)


def _build_do_dont_section(brand_profile: dict, blueprint: dict) -> str:
    brand_keywords = brand_profile.get("brand_keywords", [])
    anti_keywords = brand_profile.get("anti_keywords", [])
    principles = blueprint.get("principles", [])

    lines = ["### DO\n"]
    for principle in principles[:4]:
        implications = principle.get("implications", [])
        if implications:
            lines.append(f"- **{principle['name']}**: {implications[0]}")
    if brand_keywords:
        lines.append(f"- 모든 시각적 선택에서 **{', '.join(brand_keywords[:3])}** 기준을 적용")
    lines.append("- semantic token을 통해 컬러를 적용 (하드코딩 금지)")
    lines.append("- 일반(light) 모드와 dark 모드를 같은 semantic token 역할로 함께 구현")
    lines.append("- 접근성 기준을 모든 text/surface 조합에서 먼저 검증")
    lines.append("- 컴포넌트 변형 추가 전 기존 variant로 해결 가능한지 먼저 확인")
    lines.append("- 아이콘은 SVG 컴포넌트 또는 Lucide/Heroicons/Phosphor/Tabler 등 라이브러리로 구현")
    lines.append("- 앱 아이콘은 브랜드 특정 SVG identity asset으로 구현하고 favicon/manifest/app shell에 연결")
    lines.append("- component_specs.md의 anatomy/states/token binding을 그대로 따라 완전히 구현")

    lines.append("\n### DON'T\n")
    if anti_keywords:
        for keyword in anti_keywords[:4]:
            lines.append(f"- **{keyword}** 방향의 디자인 결정을 하지 않음")
    lines.append("- hex 값을 임의로 생성하지 않음 (반드시 레퍼런스에서 가져오기)")
    lines.append("- 토큰명을 임의로 발명하지 않음 (네이밍 패턴에서 도출)")
    lines.append("- 한 레퍼런스의 비주얼을 그대로 복제하지 않음")
    lines.append("- 다크모드만 구현하고 일반 모드를 빠뜨리지 않음")
    lines.append("- 기존 기능 진입점을 승인 없이 제거하지 않음")
    lines.append("- **이모지(🎨 ✅ 🔥 ⚡ 🚀 ❌ ⭐ 📊 등)를 아이콘/버튼/상태 표시로 절대 쓰지 않음** — 본문 콘텐츠에만 허용")
    lines.append("- '임시 버튼', 'TODO 컴포넌트', '플레이스홀더 카드' 같은 반쪽 구현을 남기지 않음")
    lines.append("- 라이브러리 컴포넌트를 기본 스타일로 그냥 쓰지 않음 — 반드시 디자인 토큰으로 스타일 바인딩")
    return "\n".join(lines)


def _build_drop_in_css_section(
    brand_profile: dict,
    token_schema: dict,
    color_reference: dict | None,
) -> str:
    lines = ["아래 CSS 변수를 `:root`에 복사하여 즉시 사용할 수 있습니다.\n"]
    lines.append("```css")
    lines.append(":root {")

    lines.append("  /* --- Spacing --- */")
    spacing_scale = token_schema.get("categories", {}).get("spacing", {}).get("scale", [])
    for val in spacing_scale:
        lines.append(f"  --space-{val}: {val}px;")

    lines.append("")
    lines.append("  /* --- Radius --- */")
    radius_map = {"none": "0", "sm": "4px", "md": "8px", "lg": "12px", "xl": "16px", "pill": "9999px"}
    for name, val in radius_map.items():
        lines.append(f"  --radius-{name}: {val};")

    lines.append("")
    lines.append("  /* --- Typography --- */")
    typography = token_schema.get("categories", {}).get("typography", {})
    fonts = typography.get("recommended_fonts", {})
    if fonts:
        if fonts.get("heading"):
            lines.append(f"  --font-heading: '{fonts['heading']}', serif;")
        if fonts.get("body"):
            lines.append(f"  --font-body: '{fonts['body']}', sans-serif;")
        if fonts.get("mono"):
            lines.append(f"  --font-mono: '{fonts['mono']}', monospace;")

    type_scale = typography.get("type_scale", {})
    sizes = type_scale.get("sizes", {})
    if sizes:
        for name, px in sizes.items():
            lines.append(f"  --text-{name}: {px}px;")

    line_heights = type_scale.get("line_heights", {})
    if line_heights:
        lines.append("")
        for name, lh in line_heights.items():
            lines.append(f"  --leading-{name}: {lh};")

    if color_reference:
        lines.append("")
        lines.append("  /* --- Color (from reference) --- */")
        active_palette = color_reference.get("active_palette", {}) or {}
        roles = active_palette.get("roles") or color_reference.get("palette_roles", {})
        for role, item in roles.items():
            hex_val = item.get("hex", "")
            if hex_val:
                lines.append(f"  --color-{role.replace('_', '-')}: {hex_val};")
        expanded = color_reference.get("expanded_palette", {}) or {}
        semantic_roles = expanded.get("semantic_roles", {})
        if semantic_roles:
            lines.append("")
            lines.append("  /* --- Semantic roles (expanded) --- */")
            for role, item in semantic_roles.items():
                hex_val = item.get("hex", "") if isinstance(item, dict) else ""
                if hex_val:
                    lines.append(f"  --color-{role.replace('_', '-')}: {hex_val};")

        component_sets = expanded.get("component_sets") or {}
        if component_sets:
            pretty_group_labels = {
                "button_primary": "Button — primary",
                "button_secondary": "Button — secondary",
                "button_ghost": "Button — ghost",
                "button_danger": "Button — danger",
                "input": "Input",
                "card": "Card",
                "nav_link": "Nav link",
                "link": "Link",
                "feedback_info": "Feedback — info",
                "feedback_success": "Feedback — success",
                "feedback_warning": "Feedback — warning",
                "feedback_danger": "Feedback — danger",
            }
            preferred_order = [
                "button_primary", "button_secondary", "button_ghost", "button_danger",
                "input", "card", "nav_link", "link",
                "feedback_info", "feedback_success", "feedback_warning", "feedback_danger",
            ]
            ordered_keys = [k for k in preferred_order if k in component_sets]
            ordered_keys += [k for k in component_sets if k not in preferred_order]
            for group_key in ordered_keys:
                entries = component_sets.get(group_key) or {}
                if not entries:
                    continue
                lines.append("")
                label = pretty_group_labels.get(group_key, group_key.replace("_", " ").title())
                lines.append(f"  /* --- {label} --- */")
                prefix = group_key.replace("_", "-")
                for slot, hex_val in entries.items():
                    if not hex_val:
                        continue
                    slot_name = slot.replace("_", "-")
                    lines.append(f"  --color-{prefix}-{slot_name}: {hex_val};")

    lines.append("")
    lines.append("  /* --- Motion --- */")
    motion = token_schema.get("categories", {}).get("motion", {})
    for dur in motion.get("durations_ms", []):
        lines.append(f"  --duration-{dur}: {dur}ms;")
    for easing in motion.get("easing_tokens", []):
        if easing == "standard":
            lines.append(f"  --ease-{easing}: cubic-bezier(0.4, 0, 0.2, 1);")
        elif easing == "enter":
            lines.append(f"  --ease-{easing}: cubic-bezier(0, 0, 0.2, 1);")
        elif easing == "exit":
            lines.append(f"  --ease-{easing}: cubic-bezier(0.4, 0, 1, 1);")
        elif easing == "emphasized":
            lines.append(f"  --ease-{easing}: cubic-bezier(0.2, 0, 0, 1);")

    lines.append("}")
    lines.append("```")
    return "\n".join(lines)


def _build_css_extraction_section(css_extraction: dict | None) -> str:
    if not css_extraction:
        return "- CSS 추출 데이터 없음 (크롤링 시 CSS가 수집되지 않았거나 extract-css가 실행되지 않음)"

    lines = []

    var_info = css_extraction.get("var_resolution", {})
    if var_info:
        total = var_info.get("total_vars", 0)
        resolved = var_info.get("resolved_count", 0)
        unresolved = var_info.get("unresolved_count", 0)
        lines.append("### Variable Resolution\n")
        lines.append(f"- 전체 CSS 변수: **{total}**개")
        lines.append(f"- 해결됨: **{resolved}**개 ({round(resolved / total * 100) if total else 0}%)")
        lines.append(f"- 미해결: **{unresolved}**개")

    brand_info = css_extraction.get("brand_colors", {})
    summary = brand_info.get("summary", {})
    if summary:
        lines.append("\n### Brand Color Candidates\n")
        lines.append(f"- 후보 수: **{summary.get('total_candidates', 0)}**개")
        by_role = summary.get("by_role", {}) or {}
        if by_role:
            top_roles = sorted(by_role.items(), key=lambda kv: kv[1], reverse=True)
            role_str = ", ".join(f"{k}={v}" for k, v in top_roles)
            lines.append(f"- Role 분포: {role_str}")

    typo_info = css_extraction.get("typography", {})
    stats = typo_info.get("stats", {})
    if stats:
        lines.append("\n### Typography Extraction\n")
        lines.append(f"- 스케일 항목: **{stats.get('scale_entries', 0)}**개")
        lines.append(f"- 고유 폰트 패밀리: **{stats.get('unique_families', 0)}**개")
        lines.append(f"- 고유 weight 수: **{stats.get('unique_weights', 0)}**개")

    alias_info = css_extraction.get("alias_layer", {})
    alias_stats = alias_info.get("stats", {})
    if alias_stats:
        lines.append("\n### Alias Layer\n")
        lines.append(f"- 전체 토큰: **{alias_stats.get('total', 0)}**개")
        tiers = alias_stats.get("by_tier", {}) or {}
        if tiers:
            tier_str = ", ".join(f"{k}={v}" for k, v in sorted(tiers.items()))
            lines.append(f"- Tier 분포: {tier_str}")
        schema_layers = alias_stats.get("by_schema_layer", {}) or {}
        if schema_layers:
            schema_str = ", ".join(f"{k}={v}" for k, v in sorted(schema_layers.items()))
            lines.append(f"- Schema layer 분포: {schema_str}")
        avg_chain = alias_stats.get("avg_chain_length")
        max_chain = alias_stats.get("max_chain_length")
        if avg_chain is not None:
            lines.append(f"- var() 체인: 평균 {avg_chain}, 최대 {max_chain}")

    return "\n".join(lines) if lines else "- CSS 추출 결과가 비어 있습니다."
