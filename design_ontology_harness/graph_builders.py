"""Graph Builders — construct the design ontology graph from existing data sources.

Each build_*_layer function adds nodes and edges to a DesignOntologyGraph.
build_full_ontology_graph() orchestrates all layers into a complete graph.
"""

from __future__ import annotations

import math
import re
from collections import Counter

from .graph_schema import (
    DesignOntologyGraph,
    EdgeType,
    NodeType,
    OntologyEdge,
    OntologyNode,
)


def slugify(value: str) -> str:
    return "".join(ch.lower() if ch.isalnum() else "-" for ch in value).strip("-")


# ---------------------------------------------------------------------------
# O-2: Brand, Foundation, Component layers
# ---------------------------------------------------------------------------


def build_brand_layer(graph: DesignOntologyGraph, brand_profile: dict, blueprint: dict) -> None:
    brand_name = brand_profile.get("brand_name", "Brand")
    brand_id = f"brand:{slugify(brand_name)}"
    graph.add_node(OntologyNode(id=brand_id, type=NodeType.Brand, label=brand_name))

    for principle in blueprint.get("principles", []):
        pid = f"principle:{slugify(principle['keyword'])}"
        graph.add_node(OntologyNode(id=pid, type=NodeType.Principle, label=principle["name"]))
        graph.add_edge(OntologyEdge(type=EdgeType.expresses, source=brand_id, target=pid))


def build_foundation_layer(graph: DesignOntologyGraph, token_schema: dict) -> None:
    layers = token_schema.get("layers", {})

    for token in layers.get("core", {}).get("spacing", {}).get("scale", []):
        tid = f"spacing:{token}"
        graph.add_node(OntologyNode(id=tid, type=NodeType.SpacingToken, label=token))

    for token in layers.get("core", {}).get("radius", {}).get("scale", []):
        tid = f"radius:{token}"
        graph.add_node(OntologyNode(id=tid, type=NodeType.RadiusToken, label=token))

    for token in layers.get("core", {}).get("motion", {}).get("durations", []):
        tid = f"motion:{token}"
        graph.add_node(OntologyNode(id=tid, type=NodeType.MotionToken, label=token))

    for token in layers.get("core", {}).get("elevation", {}).get("scale", []):
        tid = f"elevation:{token}"
        graph.add_node(OntologyNode(id=tid, type=NodeType.ElevationToken, label=token))


def build_component_layer(
    graph: DesignOntologyGraph, component_inventory: dict, brand_profile: dict
) -> None:
    for family in component_inventory.get("families", []):
        family_name = family["family"]
        fid = f"family:{slugify(family_name)}"
        graph.add_node(OntologyNode(
            id=fid, type=NodeType.ComponentFamily, label=family_name,
            meta={"priority": family.get("priority", "medium")},
        ))

        for state in family.get("required_states", []):
            sid = f"state:{slugify(family_name)}-{slugify(state)}"
            graph.add_node(OntologyNode(id=sid, type=NodeType.ComponentState, label=f"{family_name}/{state}"))
            graph.add_edge(OntologyEdge(type=EdgeType.has_state, source=fid, target=sid))

        for comp_name in family.get("components", []):
            cid = f"component:{slugify(comp_name)}"
            graph.add_node(OntologyNode(id=cid, type=NodeType.Component, label=comp_name))
            graph.add_edge(OntologyEdge(type=EdgeType.member_of_family, source=cid, target=fid))

    for comp in component_inventory.get("components", []):
        cid = f"component:{slugify(comp['name'])}"
        primitive = comp.get("supports_primitive", "")
        if primitive and primitive != "system baseline":
            prim_id = f"primitive:{slugify(primitive)}"
            graph.add_node(OntologyNode(id=prim_id, type=NodeType.ProductPrimitive, label=primitive))
            graph.add_edge(OntologyEdge(type=EdgeType.supports, source=cid, target=prim_id))


# ---------------------------------------------------------------------------
# O-3: Color + Typography layers
# ---------------------------------------------------------------------------


def build_color_layer(
    graph: DesignOntologyGraph,
    brand_profile: dict,
    alias_result: dict | None = None,
    var_chains: dict | None = None,
) -> None:
    color_ref = brand_profile.get("_resolved_color_reference")
    if not color_ref:
        return

    for palette_name, palette_data in color_ref.get("palettes", {}).items():
        pal_id = f"palette:{slugify(palette_name)}"
        graph.add_node(OntologyNode(
            id=pal_id, type=NodeType.ColorPalette, label=palette_name,
            meta={"role": palette_data.get("role", "")},
        ))

        for swatch in palette_data.get("swatches", []):
            token_id = f"color:{slugify(palette_name)}-{slugify(swatch.get('name', swatch.get('scale', '')))}"
            graph.add_node(OntologyNode(
                id=token_id, type=NodeType.ColorToken, label=swatch.get("name", ""),
                meta={"hex": swatch.get("hex", ""), "tier": "core"},
            ))
            graph.add_edge(OntologyEdge(type=EdgeType.belongs_to_palette, source=token_id, target=pal_id))

    for role_name, role_value in color_ref.get("roles", {}).items():
        token_id = f"color:{slugify(role_name)}"
        graph.add_node(OntologyNode(
            id=token_id, type=NodeType.ColorToken, label=role_name,
            meta={"hex": role_value if isinstance(role_value, str) else "", "tier": "semantic"},
        ))

    if alias_result:
        for tier_name, tokens in alias_result.items():
            for token_info in tokens:
                name = token_info.get("name", "")
                if not name:
                    continue
                token_id = f"color:{slugify(name)}"
                graph.add_node(OntologyNode(
                    id=token_id, type=NodeType.ColorToken, label=name,
                    meta={"tier": tier_name, "value": token_info.get("resolved", "")},
                ))
                if tier_name == "component":
                    graph.add_edge(OntologyEdge(
                        type=EdgeType.maps_to_tier, source=token_id, target="tier:component",
                    ))

    if var_chains:
        for derived, source in var_chains.items():
            derived_id = f"color:{slugify(derived)}"
            source_id = f"color:{slugify(source)}"
            if graph.get_node(derived_id) and graph.get_node(source_id):
                graph.add_edge(OntologyEdge(type=EdgeType.derived_from, source=derived_id, target=source_id))

    _build_contrast_pairs(graph, color_ref)

    modes = color_ref.get("modes", [])
    for mode in modes:
        mode_id = f"mode:{slugify(mode.get('name', 'default'))}"
        graph.add_node(OntologyNode(id=mode_id, type=NodeType.ColorMode, label=mode.get("name", "")))
        for override in mode.get("overrides", []):
            token_id = f"color:{slugify(override.get('token', ''))}"
            if graph.get_node(token_id):
                graph.add_edge(OntologyEdge(
                    type=EdgeType.overrides_in_mode, source=token_id, target=mode_id,
                    meta={"value": override.get("value", "")},
                ))


def _build_contrast_pairs(graph: DesignOntologyGraph, color_ref: dict) -> None:
    surfaces = color_ref.get("contrast_surfaces", [])
    if not surfaces:
        return

    color_nodes = graph.get_nodes_by_type(NodeType.ColorToken)
    label_to_id: dict[str, str] = {}
    for node in color_nodes:
        label_to_id[slugify(node.label)] = node.id
        short = node.id.replace("color:", "")
        label_to_id[short] = node.id

    for pair in surfaces:
        bg_key = slugify(pair.get("background", ""))
        fg_key = slugify(pair.get("foreground", ""))
        bg_id = label_to_id.get(bg_key) or f"color:{bg_key}"
        fg_id = label_to_id.get(fg_key) or f"color:{fg_key}"
        if graph.get_node(bg_id) and graph.get_node(fg_id):
            ratio = pair.get("ratio", 0)
            level = "AAA" if ratio >= 7 else "AA" if ratio >= 4.5 else "fail"
            graph.add_edge(OntologyEdge(
                type=EdgeType.contrast_pair, source=bg_id, target=fg_id,
                meta={"ratio": ratio, "level": level},
            ))


def build_typography_layer(
    graph: DesignOntologyGraph,
    brand_profile: dict,
    typo_scale: list[dict] | None = None,
) -> None:
    font_system = brand_profile.get("_resolved_font_system")
    if not font_system:
        return

    font_ids: dict[str, str] = {}
    for role, font_name in font_system.get("fonts", {}).items():
        fid = f"font:{slugify(font_name)}"
        graph.add_node(OntologyNode(
            id=fid, type=NodeType.FontFamily, label=font_name,
            meta={"role": role},
        ))
        font_ids[role] = fid

    if "heading" in font_ids and "body" in font_ids and font_ids["heading"] != font_ids["body"]:
        graph.add_edge(OntologyEdge(
            type=EdgeType.pairs_with, source=font_ids["heading"], target=font_ids["body"],
        ))

    if typo_scale:
        for entry in typo_scale:
            entry_name = entry.get("name", entry.get("category", ""))
            eid = f"typescale:{slugify(entry_name)}"
            graph.add_node(OntologyNode(
                id=eid, type=NodeType.TypeScaleEntry, label=entry_name,
                meta={
                    "size": entry.get("size", ""),
                    "weight": entry.get("weight", ""),
                    "line_height": entry.get("line_height", ""),
                    "category": entry.get("category", ""),
                },
            ))
            entry_font = entry.get("font_family", "")
            for role, fid in font_ids.items():
                font_label = graph.get_node(fid)
                if font_label and entry_font and slugify(entry_font) == slugify(font_label.label):
                    graph.add_edge(OntologyEdge(type=EdgeType.uses_font, source=eid, target=fid))
                    break


# ---------------------------------------------------------------------------
# O-4: Pattern, Accessibility, Benchmark layers
# ---------------------------------------------------------------------------


LAYOUT_PATTERNS = [
    "workspace navigation", "dashboard cards", "data tables", "recommendation feed",
    "closet analysis", "shopping price comparison",
]
INTERACTION_PATTERNS = [
    "command palette", "rich text editor", "forms", "notifications",
    "personal color onboarding", "outfit detail and comparison",
]

ACCESSIBILITY_RULES = [
    {"id": "contrast-aa", "label": "Color contrast AA (4.5:1 text, 3:1 UI)"},
    {"id": "keyboard-nav", "label": "Full keyboard navigation"},
    {"id": "label-association", "label": "Input label association"},
    {"id": "focus-visible", "label": "Visible focus indicator"},
    {"id": "motion-reduce", "label": "Reduced motion support"},
    {"id": "screen-reader", "label": "Screen reader compatibility"},
    {"id": "touch-target", "label": "Touch target 44x44 minimum"},
    {"id": "aria-landmarks", "label": "ARIA landmarks and roles"},
]


def build_pattern_layer(graph: DesignOntologyGraph, component_inventory: dict) -> None:
    from .authoring import PRIMITIVE_COMPONENTS

    for pattern_name in LAYOUT_PATTERNS:
        pid = f"pattern:layout-{slugify(pattern_name)}"
        graph.add_node(OntologyNode(id=pid, type=NodeType.LayoutPattern, label=pattern_name))
        for comp_name in PRIMITIVE_COMPONENTS.get(pattern_name, []):
            cid = f"component:{slugify(comp_name)}"
            if graph.get_node(cid):
                graph.add_edge(OntologyEdge(type=EdgeType.composed_of, source=pid, target=cid))
                graph.add_edge(OntologyEdge(type=EdgeType.implements, source=cid, target=pid))

    for pattern_name in INTERACTION_PATTERNS:
        pid = f"pattern:interaction-{slugify(pattern_name)}"
        graph.add_node(OntologyNode(id=pid, type=NodeType.InteractionPattern, label=pattern_name))
        for comp_name in PRIMITIVE_COMPONENTS.get(pattern_name, []):
            cid = f"component:{slugify(comp_name)}"
            if graph.get_node(cid):
                graph.add_edge(OntologyEdge(type=EdgeType.composed_of, source=pid, target=cid))
                graph.add_edge(OntologyEdge(type=EdgeType.implements, source=cid, target=pid))


def build_accessibility_layer(graph: DesignOntologyGraph, component_inventory: dict) -> None:
    for rule in ACCESSIBILITY_RULES:
        rid = f"a11y:{rule['id']}"
        graph.add_node(OntologyNode(id=rid, type=NodeType.AccessibilityRule, label=rule["label"]))

    interactive_families = {"button", "input", "navigation", "overlay"}
    for family in component_inventory.get("families", []):
        family_name = family["family"]
        fid = f"family:{slugify(family_name)}"

        graph.add_edge(OntologyEdge(
            type=EdgeType.requires, source=fid, target="a11y:focus-visible",
        ))
        graph.add_edge(OntologyEdge(
            type=EdgeType.requires, source=fid, target="a11y:contrast-aa",
        ))

        if family_name in interactive_families:
            graph.add_edge(OntologyEdge(type=EdgeType.requires, source=fid, target="a11y:keyboard-nav"))

        if family_name == "input":
            graph.add_edge(OntologyEdge(type=EdgeType.requires, source=fid, target="a11y:label-association"))


def build_benchmark_layer(graph: DesignOntologyGraph, brand_profile: dict) -> None:
    from .benchmark_kb import BENCHMARK_SYSTEMS

    brand_name = brand_profile.get("brand_name", "Brand")
    brand_id = f"brand:{slugify(brand_name)}"
    brand_keywords = set(k.lower() for k in brand_profile.get("brand_keywords", []))

    system_keywords: dict[str, set[str]] = {}
    for system in BENCHMARK_SYSTEMS:
        sys_id = f"benchmark:{system['id']}"
        graph.add_node(OntologyNode(
            id=sys_id, type=NodeType.BenchmarkSystem, label=system["name"],
            meta={
                "url": system.get("url", ""),
                "category": system.get("category", ""),
                "color_strategy": system.get("color_strategy", ""),
            },
        ))
        sys_keywords = set(k.lower() for k in system.get("keywords", []))
        system_keywords[sys_id] = sys_keywords

        overlap = brand_keywords & sys_keywords
        if overlap:
            graph.add_edge(OntologyEdge(
                type=EdgeType.inspired_by, source=brand_id, target=sys_id,
                meta={"shared_keywords": sorted(overlap)},
            ))

        typo = system.get("typography", {})
        for role in ["heading", "body", "mono"]:
            font_name = typo.get(role, "")
            if font_name:
                fid = f"font:{slugify(font_name)}"
                if graph.get_node(fid):
                    graph.add_edge(OntologyEdge(
                        type=EdgeType.references_font, source=sys_id, target=fid,
                    ))

    sys_ids = list(system_keywords.keys())
    for i in range(len(sys_ids)):
        for j in range(i + 1, len(sys_ids)):
            kw_a = system_keywords[sys_ids[i]]
            kw_b = system_keywords[sys_ids[j]]
            if not kw_a or not kw_b:
                continue
            jaccard = len(kw_a & kw_b) / len(kw_a | kw_b)
            if jaccard >= 0.5:
                graph.add_edge(OntologyEdge(
                    type=EdgeType.similar_to, source=sys_ids[i], target=sys_ids[j],
                    meta={"jaccard": round(jaccard, 3)},
                ))


# ---------------------------------------------------------------------------
# Orchestrator
# ---------------------------------------------------------------------------


def build_full_ontology_graph(
    brand_profile: dict,
    blueprint: dict,
    component_inventory: dict,
    token_schema: dict,
    alias_result: dict | None = None,
    var_chains: dict | None = None,
    typo_scale: list[dict] | None = None,
) -> DesignOntologyGraph:
    graph = DesignOntologyGraph()

    build_brand_layer(graph, brand_profile, blueprint)
    build_foundation_layer(graph, token_schema)
    build_component_layer(graph, component_inventory, brand_profile)
    build_color_layer(graph, brand_profile, alias_result, var_chains)
    build_typography_layer(graph, brand_profile, typo_scale)
    build_pattern_layer(graph, component_inventory)
    build_accessibility_layer(graph, component_inventory)
    build_benchmark_layer(graph, brand_profile)

    return graph
