from __future__ import annotations

import json
from pathlib import Path

from .models import DocumentRecord, ReferenceLink
from .utils import ensure_dir, write_json

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
    "dashboard cards": ["stat-card", "insight-card", "activity-card", "section-header"],
    "data tables": ["data-table", "column-header", "filter-chip", "row-actions", "pagination"],
    "forms": ["text-field", "select", "checkbox", "radio", "textarea", "form-section"],
    "notifications": ["toast", "inline-alert", "empty-state", "banner"],
    "personal color onboarding": [
        "step-progress",
        "tone-selector",
        "mood-tag-selector",
        "budget-range-slider",
        "preference-card",
    ],
    "recommendation feed": [
        "outfit-feed-card",
        "score-bar-chart",
        "reason-chip",
        "tpo-filter-tab",
        "save-toggle",
    ],
    "outfit detail and comparison": [
        "outfit-detail-sheet",
        "comparison-overlay-chart",
        "top-pick-badge",
        "recommendation-reason-list",
    ],
    "shopping price comparison": [
        "price-compare-table",
        "merchant-row",
        "price-highlight-badge",
        "similar-item-card",
    ],
    "closet analysis": [
        "closet-grid",
        "item-score-badge",
        "upload-dropzone",
        "analysis-summary-card",
    ],
    "ai try-on": [
        "try-on-preview",
        "generation-state-panel",
        "premium-gate-card",
        "multi-item-selector",
    ],
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
]

BASELINE_FAMILY_COMPONENTS = {
    "button": ["primary-button", "secondary-button", "ghost-button", "icon-button", "cta-button"],
    "navigation": ["mobile-topbar", "mobile-tab-bar", "back-button", "section-tabs"],
    "feedback": ["inline-alert", "empty-state", "toast"],
    "overlay": ["bottom-sheet", "modal-dialog"],
    "input": ["text-field", "search-field", "segmented-control"],
}


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
    ontology_graph = build_system_ontology(brand_profile, blueprint, references, component_inventory)
    system_spec = build_system_spec_markdown(
        brand_profile=brand_profile,
        blueprint=blueprint,
        validation=validation,
        foundations=foundations,
        token_schema=token_schema,
        component_inventory=component_inventory,
        documents=documents,
    )

    write_json(blueprint_dir / "profile_validation.json", validation)
    write_json(blueprint_dir / "token_schema.json", token_schema)
    write_json(blueprint_dir / "component_inventory.json", component_inventory)
    write_json(blueprint_dir / "system_ontology.json", ontology_graph)
    (blueprint_dir / "system_spec.md").write_text(system_spec, encoding="utf-8")

    return {
        "validation": validation,
        "token_schema": token_schema,
        "component_inventory": component_inventory,
        "system_ontology": ontology_graph,
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

    schema = {
        "naming": {
            "core": "{category}.{role}.{scale}",
            "semantic": "{category}.{intent}.{state}",
            "component": "{component}.{slot}.{property}",
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
                    "text/surface 조합은 접근성 기준을 우선"
                ],
            },
            "typography": {
                "families": ["display", "text", "mono"] if editorial_system else ["brand", "text", "mono"],
                "size_scale": ["xs", "sm", "md", "lg", "xl", "2xl", "3xl", "4xl"],
                "rules": [
                    "display는 마케팅/영웅 구역으로 제한",
                    "text는 제품 본문과 UI 라벨의 기본",
                    "mono는 데이터와 shortcut hint에 제한"
                ],
            },
            "spacing": {
                "scale": [0, 2, 4, 8, 12, 16, 24, 32, 48, 64, 96],
                "density_modes": ["comfortable", "compact"] if calm_system else ["default", "dense"],
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
            "rules": [
                "컬러 레퍼런스의 mood와 pairings를 semantic token 설계의 출발점으로 사용",
                "chosen palette는 semantic roles로 번역하고 raw reference color를 그대로 남용하지 않기",
                "seed color만 쓰지 말고 expanded palette에서 surface/text/border/support 역할까지 확장하기",
                "surface/text/border 대비는 레퍼런스보다 접근성 기준을 우선"
            ],
        }
    return schema


def build_component_inventory(brand_profile: dict, blueprint: dict) -> dict:
    primitives = brand_profile.get("product_primitives", [])
    families: dict[str, dict] = {}
    all_components: list[dict] = []

    family_specs = {
        "button": {"states": ["default", "hover", "active", "disabled", "loading"], "priority": "high"},
        "input": {"states": ["default", "focus", "error", "disabled"], "priority": "high"},
        "navigation": {"states": ["default", "active", "hover", "collapsed"], "priority": "high"},
        "feedback": {"states": ["info", "success", "warning", "danger"], "priority": "high"},
        "overlay": {"states": ["closed", "opening", "open"], "priority": "medium"},
        "editorial": {"states": ["default", "selected", "editing"], "priority": "high"},
        "data-display": {"states": ["default", "sorted", "filtered", "empty"], "priority": "high"},
    }

    for family in blueprint.get("component_strategy", {}).get("required_component_families", []):
        spec = family_specs.get(family, {"states": ["default"], "priority": "medium"})
        families[family] = {
            "family": family,
            "priority": spec["priority"],
            "required_states": spec["states"],
            "components": [],
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
                {"family": family, "priority": "medium", "required_states": ["default"], "components": []},
            )
            families[family]["components"].append(component_name)

    for family_name, baseline_components in BASELINE_FAMILY_COMPONENTS.items():
        if family_name not in families:
            continue
        existing = set(families[family_name]["components"])
        for component_name in baseline_components:
            if component_name in existing:
                continue
            families[family_name]["components"].append(component_name)
            all_components.append(
                {
                    "name": component_name,
                    "family": family_name,
                    "supports_primitive": "system baseline",
                    "status": "planned",
                    "must_document": ["anatomy", "states", "content rules", "accessibility", "dos and donts"],
                }
            )
            existing.add(component_name)

    return {
        "families": sorted(families.values(), key=lambda item: (item["priority"] != "high", item["family"])),
        "components": all_components,
    }


def classify_component_family(component_name: str) -> str:
    if any(token in component_name for token in ["chart", "table", "grid", "summary", "score"]):
        return "data-display"
    if any(token in component_name for token in ["editor", "block", "slash"]):
        return "editorial"
    if any(token in component_name for token in ["nav", "breadcrumb", "switcher", "topbar", "sidebar"]):
        return "navigation"
    if any(token in component_name for token in ["badge", "chip", "highlight"]):
        return "feedback"
    if any(token in component_name for token in ["toast", "alert", "banner", "empty-state"]):
        return "feedback"
    if any(token in component_name for token in ["palette", "menu", "overlay", "modal"]):
        return "overlay"
    if any(token in component_name for token in ["sheet", "preview", "panel"]):
        return "overlay"
    if any(token in component_name for token in ["field", "select", "checkbox", "radio", "textarea"]):
        return "input"
    if any(token in component_name for token in ["slider", "dropzone", "selector"]):
        return "input"
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

    for family in component_inventory.get("families", []):
        family_id = f"component-family:{family['family']}"
        nodes.append({"id": family_id, "type": "ComponentFamily", "label": family["family"]})
        for component_name in family.get("components", []):
            component_id = f"component:{slugify_text(component_name)}"
            nodes.append({"id": component_id, "type": "Component", "label": component_name})
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
    implementation_guardrail_lines = "\n".join(
        f"- {line}"
        for line in blueprint.get("governance", {}).get("implementation_guardrails", [])
    ) or "- No implementation guardrails defined."
    family_lines = "\n".join(
        f"- **{family['family']}**: {', '.join(family.get('components', [])[:8]) or 'TBD'}"
        for family in component_inventory.get("families", [])
    )
    color_reference = brand_profile.get("_resolved_color_reference")
    color_reference_lines = _build_color_reference_section(color_reference)
    validation_lines = "\n".join(
        [f"- Error: {message}" for message in validation.get("errors", [])]
        + [f"- Warning: {message}" for message in validation.get("warnings", [])]
    ) or "- No validation issues."
    concept_lines = "\n".join(
        f"- **{target['concept_id']}**: {target['count']}"
        for target in blueprint.get("ontology_targets", [])
    )

    return f"""# {blueprint.get('system_name', 'Design System')} Spec

## 1. Positioning

- **Brand**: {brand_profile.get('brand_name', '')}
- **Product**: {brand_profile.get('product_summary', '')}
- **Audience**: {', '.join(brand_profile.get('audiences', []))}
- **Platforms**: {', '.join(brand_profile.get('platforms', []))}
- **Accessibility floor**: {', '.join(brand_profile.get('accessibility_targets', []))}

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

## 6. Color Reference

{color_reference_lines}

## 7. Component Strategy

- **Product primitives**: {', '.join(brand_profile.get('product_primitives', []))}
- **Required families**: {', '.join(item['family'] for item in component_inventory.get('families', []))}

{family_lines}

## 8. Implementation Guardrails

{implementation_guardrail_lines}

## 9. Reference Absorption Rule

- Analysed live reference sources: {source_count}
- Rule: copy visuals from no single source; absorb patterns only when they reinforce brand keywords and avoid anti-keywords.
- Use references to validate structure, accessibility, token discipline, and documentation quality.

## 10. Ontology Targets

{concept_lines}

## 11. Profile Validation

{validation_lines}
"""


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

    notes = color_reference.get("notes", [])
    if notes:
        lines.append(f"- **Notes**: {', '.join(str(item) for item in notes)}")

    lines.append("- **Application rule**: 레퍼런스 컬러는 semantic token으로 번역해서 사용하고, 접근성과 theme 호환성을 우선합니다.")
    return "\n".join(lines)
