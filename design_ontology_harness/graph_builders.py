"""Graph Builders — construct the design ontology graph from existing data sources.

Each build_*_layer function adds nodes and edges to a DesignOntologyGraph.
build_full_ontology_graph() orchestrates all layers into a complete graph.
"""

from __future__ import annotations


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
    categories = token_schema.get("categories", {})

    for token in categories.get("spacing", {}).get("scale", []):
        tid = f"spacing:{token}"
        graph.add_node(OntologyNode(id=tid, type=NodeType.SpacingToken, label=str(token)))

    for token in categories.get("radius", {}).get("scale", []):
        tid = f"radius:{token}"
        graph.add_node(OntologyNode(id=tid, type=NodeType.RadiusToken, label=str(token)))

    for token in categories.get("motion", {}).get("durations", []):
        tid = f"motion:{token}"
        graph.add_node(OntologyNode(id=tid, type=NodeType.MotionToken, label=str(token)))

    for token in categories.get("elevation", {}).get("scale", []):
        tid = f"elevation:{token}"
        graph.add_node(OntologyNode(id=tid, type=NodeType.ElevationToken, label=str(token)))


def build_component_layer(
    graph: DesignOntologyGraph, component_inventory: dict, brand_profile: dict
) -> None:
    component_meta_by_name = {
        comp.get("name"): comp
        for comp in component_inventory.get("components", [])
        if comp.get("name")
    }
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
            meta = component_meta_by_name.get(comp_name, {})
            node_meta = {}
            if meta.get("advanced_component"):
                node_meta = {
                    "advanced_component": True,
                    "usage_guidance": meta.get("usage_guidance", []),
                    "pairs_with": meta.get("pairs_with", []),
                    "matched_signals": meta.get("matched_signals", []),
                }
            graph.add_node(OntologyNode(id=cid, type=NodeType.Component, label=comp_name, meta=node_meta))
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

    seen_families: set[str] = set()
    for color_info in color_ref.get("selected_colors", []):
        family = color_info.get("family", "")
        if family and family not in seen_families:
            seen_families.add(family)
            pal_id = f"palette:{slugify(family)}"
            graph.add_node(OntologyNode(
                id=pal_id, type=NodeType.ColorPalette, label=family,
            ))

        name = color_info.get("name", "")
        if name:
            token_id = f"color:{slugify(name)}"
            graph.add_node(OntologyNode(
                id=token_id, type=NodeType.ColorToken, label=name,
                meta={"hex": color_info.get("hex", ""), "tier": "core", "mood": color_info.get("mood", "")},
            ))
            if family:
                graph.add_edge(OntologyEdge(
                    type=EdgeType.belongs_to_palette, source=token_id, target=f"palette:{slugify(family)}",
                ))

    for role_name, role_data in color_ref.get("palette_roles", {}).items():
        if isinstance(role_data, dict):
            name = role_data.get("name", role_name)
            token_id = f"color:{slugify(name)}"
            graph.add_node(OntologyNode(
                id=token_id, type=NodeType.ColorToken, label=name,
                meta={"hex": role_data.get("hex", ""), "tier": "semantic", "role": role_name},
            ))

    expanded = color_ref.get("expanded_palette", {})
    for role_name, role_data in expanded.get("semantic_roles", {}).items():
        if isinstance(role_data, dict):
            name = role_data.get("name", role_name)
            token_id = f"color:{slugify(name)}"
            graph.add_node(OntologyNode(
                id=token_id, type=NodeType.ColorToken, label=name,
                meta={"hex": role_data.get("hex", ""), "tier": "semantic", "role": role_name},
            ))

    for color_info in expanded.get("supporting_colors", []):
        name = color_info.get("name", "")
        if name:
            token_id = f"color:{slugify(name)}"
            graph.add_node(OntologyNode(
                id=token_id, type=NodeType.ColorToken, label=name,
                meta={"hex": color_info.get("hex", ""), "tier": "supporting"},
            ))
            family = color_info.get("family", "")
            if family:
                pal_id = f"palette:{slugify(family)}"
                if not graph.get_node(pal_id):
                    graph.add_node(OntologyNode(id=pal_id, type=NodeType.ColorPalette, label=family))
                graph.add_edge(OntologyEdge(
                    type=EdgeType.belongs_to_palette, source=token_id, target=pal_id,
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

    if var_chains:
        for derived, source in var_chains.items():
            derived_id = f"color:{slugify(derived)}"
            source_id = f"color:{slugify(source)}"
            if graph.get_node(derived_id) and graph.get_node(source_id):
                graph.add_edge(OntologyEdge(type=EdgeType.derived_from, source=derived_id, target=source_id))

    _build_semantic_color_ontology_layer(graph, color_ref)
    _build_contrast_pairs(graph, color_ref)


def _build_semantic_color_ontology_layer(graph: DesignOntologyGraph, color_ref: dict) -> None:
    semantic = color_ref.get("semantic_ontology", {}) or {}
    if not semantic:
        return

    source = semantic.get("source", {}) or {}
    source_id = "source:semantic-color-ontology"
    graph.add_node(OntologyNode(
        id=source_id,
        type=NodeType.SourceReference,
        label="Semantic OS color ontology",
        meta={
            "repo": source.get("repo"),
            "path": source.get("path"),
            "schema_version": semantic.get("schema_version"),
            "node_count": semantic.get("node_count"),
            "edge_count": semantic.get("edge_count"),
            "copyright_handling": semantic.get("copyright_handling"),
        },
    ))

    semantic_token_ids: list[str] = []
    for item in semantic.get("matched_keywords", []):
        name = item.get("name")
        if not name:
            continue
        token_id = f"semantic-color:{slugify(name)}"
        semantic_token_ids.append(token_id)
        graph.add_node(OntologyNode(
            id=token_id,
            type=NodeType.ColorToken,
            label=name,
            meta={
                "hex": item.get("hex"),
                "tier": "semantic-color-ontology",
                "role": item.get("role"),
                "semantic_node_id": item.get("id"),
                "spectrum": item.get("spectrum"),
                "family": item.get("family"),
                "mood_tags": item.get("mood_tags", []),
                "tone_axes": item.get("tone_axes", []),
                "source_pages": item.get("source_pages", {}),
            },
        ))
        graph.add_edge(OntologyEdge(type=EdgeType.inspired_by, source=token_id, target=source_id))

    for item in semantic.get("guidelines", []):
        guideline_id = item.get("id")
        if not guideline_id:
            continue
        node_id = f"governance:semantic-color-{slugify(guideline_id)}"
        graph.add_node(OntologyNode(
            id=node_id,
            type=NodeType.GovernanceRule,
            label=item.get("label") or guideline_id,
            meta={
                "semantic_node_id": guideline_id,
                "summary": item.get("summary"),
                "prompt_do": item.get("prompt_do", []),
                "prompt_avoid": item.get("prompt_avoid", []),
            },
        ))
        graph.add_edge(OntologyEdge(type=EdgeType.inspired_by, source=node_id, target=source_id))
        for token_id in semantic_token_ids:
            graph.add_edge(OntologyEdge(type=EdgeType.governs, source=node_id, target=token_id))


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
    for role in ["heading", "body", "mono"]:
        font_data = font_system.get(role)
        if not font_data:
            continue
        if isinstance(font_data, dict):
            font_name = font_data.get("name", "")
            meta = {
                "role": role,
                "family_type": font_data.get("family", ""),
                "weight_range": font_data.get("weight_range", ""),
                "variable": font_data.get("variable", False),
                "source": font_data.get("source", ""),
            }
        else:
            font_name = str(font_data)
            meta = {"role": role}

        if not font_name:
            continue
        fid = f"font:{slugify(font_name)}"
        graph.add_node(OntologyNode(id=fid, type=NodeType.FontFamily, label=font_name, meta=meta))
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


DEFAULT_LAYOUT_PATTERNS = [
    "workspace navigation", "dashboard cards", "data tables",
]
DEFAULT_INTERACTION_PATTERNS = [
    "command palette", "forms", "notifications",
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


def _classify_primitive(primitive: str) -> str:
    from .authoring import INTERACTION_PRIMITIVE_KEYWORDS, LAYOUT_PRIMITIVE_KEYWORDS

    low = primitive.lower()
    if any(keyword in low for keyword in INTERACTION_PRIMITIVE_KEYWORDS):
        return "interaction"
    if any(keyword in low for keyword in LAYOUT_PRIMITIVE_KEYWORDS):
        return "layout"
    return "layout"


def build_pattern_layer(
    graph: DesignOntologyGraph,
    component_inventory: dict,
    brand_profile: dict | None = None,
) -> None:
    from .authoring import PRIMITIVE_COMPONENTS

    primitives = []
    if brand_profile:
        primitives = [p for p in brand_profile.get("product_primitives", []) if isinstance(p, str) and p.strip()]

    layout_set: list[str] = []
    interaction_set: list[str] = []
    seen: set[str] = set()

    for primitive in primitives:
        key = primitive.strip().lower()
        if key in seen:
            continue
        seen.add(key)
        bucket = _classify_primitive(primitive)
        if bucket == "layout":
            layout_set.append(primitive)
        else:
            interaction_set.append(primitive)

    for fallback in DEFAULT_LAYOUT_PATTERNS:
        if fallback.lower() not in seen:
            seen.add(fallback.lower())
            layout_set.append(fallback)
    for fallback in DEFAULT_INTERACTION_PATTERNS:
        if fallback.lower() not in seen:
            seen.add(fallback.lower())
            interaction_set.append(fallback)

    def _wire_pattern(pattern_name: str, node_type: NodeType, prefix: str) -> None:
        pid = f"pattern:{prefix}-{slugify(pattern_name)}"
        graph.add_node(OntologyNode(id=pid, type=node_type, label=pattern_name))
        wired: set[str] = set()

        for comp_name in PRIMITIVE_COMPONENTS.get(pattern_name.lower(), []):
            cid = f"component:{slugify(comp_name)}"
            if cid in wired or not graph.get_node(cid):
                continue
            graph.add_edge(OntologyEdge(type=EdgeType.composed_of, source=pid, target=cid))
            graph.add_edge(OntologyEdge(type=EdgeType.implements, source=cid, target=pid))
            wired.add(cid)

        for comp in component_inventory.get("components", []):
            supports = (comp.get("supports_primitive") or "").strip().lower()
            if supports and supports == pattern_name.strip().lower():
                cid = f"component:{slugify(comp['name'])}"
                if cid in wired or not graph.get_node(cid):
                    continue
                graph.add_edge(OntologyEdge(type=EdgeType.composed_of, source=pid, target=cid))
                graph.add_edge(OntologyEdge(type=EdgeType.implements, source=cid, target=pid))
                wired.add(cid)

    for pattern_name in layout_set:
        _wire_pattern(pattern_name, NodeType.LayoutPattern, "layout")
    for pattern_name in interaction_set:
        _wire_pattern(pattern_name, NodeType.InteractionPattern, "interaction")


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


def build_component_token_layer(
    graph: DesignOntologyGraph,
    component_inventory: dict,
    brand_profile: dict,
) -> None:
    """Link components to color/spacing/radius/font tokens via `uses_token` / `uses_font`.

    Uses the resolved color palette roles (primary/accent/surface_tint) as the color
    token targets. Interactive families (button/input/navigation/overlay) also wire up
    radius and spacing defaults so that Section 17 (Component-Token Map) is populated.
    """
    color_ref = brand_profile.get("_resolved_color_reference") or {}
    palette_roles = color_ref.get("palette_roles", {}) or {}
    role_token_ids: dict[str, str] = {}
    for role_name, role_data in palette_roles.items():
        if isinstance(role_data, dict):
            name = role_data.get("name", role_name)
            tid = f"color:{slugify(name)}"
            if graph.get_node(tid):
                role_token_ids[role_name] = tid

    font_system = brand_profile.get("_resolved_font_system") or {}
    font_ids: dict[str, str] = {}
    for role in ("heading", "body", "mono"):
        entry = font_system.get(role)
        if isinstance(entry, dict):
            name = entry.get("name") or ""
        else:
            name = str(entry) if entry else ""
        if name:
            fid = f"font:{slugify(name)}"
            if graph.get_node(fid):
                font_ids[role] = fid

    spacing_md = "spacing:12"
    radius_md = "radius:md"

    interactive = {"button", "input", "navigation", "overlay"}

    for comp in component_inventory.get("components", []):
        cid = f"component:{slugify(comp['name'])}"
        if not graph.get_node(cid):
            continue
        family = comp.get("family", "")
        is_interactive = family in interactive

        if is_interactive and "primary" in role_token_ids:
            graph.add_edge(OntologyEdge(
                type=EdgeType.uses_token, source=cid, target=role_token_ids["primary"],
                meta={"slot": "surface"},
            ))
        if is_interactive and "accent" in role_token_ids:
            graph.add_edge(OntologyEdge(
                type=EdgeType.uses_token, source=cid, target=role_token_ids["accent"],
                meta={"slot": "emphasis"},
            ))
        if "surface_tint" in role_token_ids:
            graph.add_edge(OntologyEdge(
                type=EdgeType.uses_token, source=cid, target=role_token_ids["surface_tint"],
                meta={"slot": "background"},
            ))

        if graph.get_node(spacing_md):
            graph.add_edge(OntologyEdge(
                type=EdgeType.uses_token, source=cid, target=spacing_md,
                meta={"slot": "padding"},
            ))
        if graph.get_node(radius_md):
            graph.add_edge(OntologyEdge(
                type=EdgeType.uses_token, source=cid, target=radius_md,
                meta={"slot": "radius"},
            ))

        if "body" in font_ids:
            graph.add_edge(OntologyEdge(
                type=EdgeType.uses_font, source=cid, target=font_ids["body"],
            ))


def _hex_to_rgb(hex_code: str) -> tuple[int, int, int] | None:
    value = (hex_code or "").strip().lstrip("#")
    if len(value) == 3:
        value = "".join(ch * 2 for ch in value)
    if len(value) != 6:
        return None
    try:
        return int(value[0:2], 16), int(value[2:4], 16), int(value[4:6], 16)
    except ValueError:
        return None


def _relative_luminance(rgb: tuple[int, int, int]) -> float:
    def _channel(v: int) -> float:
        c = v / 255.0
        return c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4

    r, g, b = rgb
    return 0.2126 * _channel(r) + 0.7152 * _channel(g) + 0.0722 * _channel(b)


def _contrast_ratio(bg_hex: str, fg_hex: str) -> float | None:
    bg = _hex_to_rgb(bg_hex)
    fg = _hex_to_rgb(fg_hex)
    if not bg or not fg:
        return None
    l1 = _relative_luminance(bg)
    l2 = _relative_luminance(fg)
    lighter, darker = max(l1, l2), min(l1, l2)
    return (lighter + 0.05) / (darker + 0.05)


def build_contrast_audit_layer(graph: DesignOntologyGraph, brand_profile: dict) -> None:
    """Emit `contrast_pair` edges for the active palette + common ink/paper combos.

    If `contrast_surfaces` is manually defined in color_reference, it is honored via
    `_build_contrast_pairs` (already called from build_color_layer). Otherwise we auto-
    compose the palette roles against black/white baselines so Section 18 is never empty.
    """
    color_ref = brand_profile.get("_resolved_color_reference") or {}
    roles = color_ref.get("palette_roles", {}) or {}

    role_colors: dict[str, dict] = {}
    for role_name, role_data in roles.items():
        if isinstance(role_data, dict) and role_data.get("hex"):
            role_colors[role_name] = role_data

    if not role_colors:
        return

    baselines = [
        {"name": "Paper", "hex": "#FFFFFF"},
        {"name": "Ink", "hex": "#111111"},
    ]
    for baseline in baselines:
        token_id = f"color:{slugify(baseline['name'])}"
        if not graph.get_node(token_id):
            graph.add_node(OntologyNode(
                id=token_id, type=NodeType.ColorToken, label=baseline["name"],
                meta={"hex": baseline["hex"], "tier": "baseline", "role": baseline["name"].lower()},
            ))

    pairings: list[tuple[str, str, str, str]] = []
    for role_name, role_data in role_colors.items():
        role_hex = role_data["hex"]
        role_name_label = role_data.get("name") or role_name
        role_id = f"color:{slugify(role_name_label)}"
        for baseline in baselines:
            pairings.append((role_id, role_hex, f"color:{slugify(baseline['name'])}", baseline["hex"]))

    role_items = list(role_colors.items())
    for i in range(len(role_items)):
        for j in range(i + 1, len(role_items)):
            a_name, a_data = role_items[i]
            b_name, b_data = role_items[j]
            a_id = f"color:{slugify(a_data.get('name') or a_name)}"
            b_id = f"color:{slugify(b_data.get('name') or b_name)}"
            pairings.append((a_id, a_data["hex"], b_id, b_data["hex"]))

    seen_edges: set[tuple[str, str]] = set()
    for bg_id, bg_hex, fg_id, fg_hex in pairings:
        if (bg_id, fg_id) in seen_edges:
            continue
        if not graph.get_node(bg_id) or not graph.get_node(fg_id):
            continue
        ratio = _contrast_ratio(bg_hex, fg_hex)
        if ratio is None:
            continue
        level = "AAA" if ratio >= 7 else "AA" if ratio >= 4.5 else "AA-large" if ratio >= 3 else "fail"
        graph.add_edge(OntologyEdge(
            type=EdgeType.contrast_pair, source=bg_id, target=fg_id,
            meta={"ratio": round(ratio, 2), "level": level},
        ))
        seen_edges.add((bg_id, fg_id))


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
# Generated visual asset layer
# ---------------------------------------------------------------------------


VISUAL_ASSET_MANIFEST_PATH = "public/generated/design-system/manifest.json"
VISUAL_ASSET_PROMPT_PACK_PATH = "public/generated/design-system/imagegen-prompts.md"
VISUAL_IMAGE_GENERATOR_ID = "image-model:codex-imagegen"
VISUAL_IMAGE_GENERATOR_LABEL = "Codex image_gen skill"
VISUAL_IMAGE_GENERATOR_FAILURE_POLICY = "no API fallback"
VISUAL_ASSET_MEDIUM_SELECTION_POLICY_ID = "governance:visual-asset-medium-selection"
VISUAL_ASSET_CONTRACT_ID = "governance:generated-visual-asset-contract"
SOURCED_VISUAL_ASSET_CONTRACT_ID = "governance:sourced-visual-asset-fallback-contract"
SOURCED_VISUAL_ASSET_FALLBACK_POLICY = "license-verified sourced visual fallback"
SOURCED_VISUAL_ASSET_CANDIDATE_MANIFEST_PATH = "public/generated/design-system/sourced-visual-candidates.json"
VISUAL_ASSET_MANIFEST_SCHEMA = "visual-asset-manifest/v1"
VISUAL_ASSET_COMPATIBLE_MANIFEST_PATHS = [
    VISUAL_ASSET_MANIFEST_PATH,
    "design-system/generated_visual_assets.json",
]
VISUAL_ASSET_MANIFEST_REQUIRED_FIELDS = [
    "schema_version",
    "project",
    "brand",
    "generator",
    "source_session",
    "assets",
]
VISUAL_ASSET_RECORD_REQUIRED_FIELDS = [
    "id",
    "label",
    "slot",
    "status",
    "asset_path",
    "original_png_path",
    "format",
    "dimensions",
    "size_kb",
    "sha256",
    "intended_for",
    "alt_text",
    "prompt_summary",
]
SOURCED_VISUAL_ASSET_RECORD_REQUIRED_FIELDS = [
    "id",
    "label",
    "slot",
    "status",
    "acquisition_mode",
    "asset_path",
    "source_url",
    "download_url",
    "provider",
    "author",
    "license",
    "attribution_required",
    "sha256",
    "intended_for",
    "alt_text",
    "selection_reason",
]
VISUAL_ASSET_CONTRACT_RULES = [
    "Use Codex built-in image_gen as the default generation path; do not call CLI, SDK, or OpenAI API fallback unless the user explicitly requests that path.",
    "Copy every project-bound final asset into the workspace before implementation code references it.",
    "Preserve the original generated PNG path in the manifest when available, but never make runtime code depend on the Codex home directory.",
    "Record alt_text, prompt_summary, intended_for, dimensions, size_kb, and sha256 for each integrated raster asset.",
    "Generated images are not valid replacements for icons, logos, button glyphs, status markers, or deterministic diagrams.",
]
SOURCED_VISUAL_ASSET_CONTRACT_RULES = [
    "Use sourced visuals only as a fallback when Codex image_gen is unavailable, fails, or the product needs real-world photographic evidence more than generated imagery.",
    "Search only allowlisted free sourced providers, licensed providers with user-supplied proof, local licensed files, or user-supplied assets with explicit permission.",
    "Use reference-only providers for morphology, density, hierarchy, and flow research only; never copy their images into runtime assets.",
    "Paid stock providers require license_proof, usage_scope, and licensed_to metadata before an image can be promoted into implementation.",
    "Do not use a result unless the source URL, provider, author, license label, attribution requirement, and download URL are recorded.",
    "Copy accepted assets into the workspace; never hotlink a search result or CDN URL from runtime code.",
    "Store selection_reason, crop/focal-point notes, alt_text, sha256, and intended_for before wiring the image into UI code.",
    "Do not use sourced search images for logos, app icons, favicons, button glyphs, status markers, or flags unless the specific asset license and identity use are explicitly approved.",
]

FREE_SOURCED_VISUAL_PROVIDER_RULES = [
    {
        "id": "openverse",
        "label": "Openverse",
        "tier": "free-sourced",
        "kind": "free-image-search",
        "license_scope": ["CC0", "Public Domain", "CC BY", "CC BY-SA"],
        "attribution_default": "license-dependent",
        "license_proof_required": False,
        "asset_usage": "may become SourcedVisualAsset when per-asset metadata is recorded",
        "notes": "Prefer results with machine-readable Creative Commons metadata.",
    },
    {
        "id": "wikimedia-commons",
        "label": "Wikimedia Commons",
        "tier": "free-sourced",
        "kind": "free-media-commons",
        "license_scope": ["CC0", "Public Domain", "CC BY", "CC BY-SA", "GFDL"],
        "attribution_default": "usually required",
        "license_proof_required": False,
        "asset_usage": "may become SourcedVisualAsset when file-page license and author metadata are recorded",
        "notes": "Use only files with visible license and author metadata on the file page.",
    },
    {
        "id": "unsplash",
        "label": "Unsplash",
        "tier": "free-sourced",
        "kind": "free-photo-provider",
        "license_scope": ["Unsplash License"],
        "attribution_default": "recommended",
        "license_proof_required": False,
        "asset_usage": "may become SourcedVisualAsset when photo URL, photographer, and license page are recorded",
        "notes": "Record the photo page URL and photographer; avoid brand/logo-like use.",
    },
    {
        "id": "pexels",
        "label": "Pexels",
        "tier": "free-sourced",
        "kind": "free-photo-provider",
        "license_scope": ["Pexels License"],
        "attribution_default": "recommended",
        "license_proof_required": False,
        "asset_usage": "may become SourcedVisualAsset when photo URL, photographer, and license page are recorded",
        "notes": "Record the photo page URL and photographer; avoid implying endorsement.",
    },
]

LICENSED_VISUAL_PROVIDER_RULES = [
    {
        "id": "adobe-stock",
        "label": "Adobe Stock",
        "tier": "licensed",
        "kind": "paid-stock-provider",
        "license_scope": ["Adobe Stock Standard License", "Adobe Stock Extended License"],
        "attribution_default": "license-dependent",
        "license_proof_required": True,
        "asset_usage": "may become SourcedVisualAsset only when purchase/license proof is recorded",
        "notes": "Use for production-grade licensed stock when the user has rights or supplies proof.",
    },
    {
        "id": "shutterstock",
        "label": "Shutterstock",
        "tier": "licensed",
        "kind": "paid-stock-provider",
        "license_scope": ["Shutterstock Standard License", "Shutterstock Enhanced License"],
        "attribution_default": "license-dependent",
        "license_proof_required": True,
        "asset_usage": "may become SourcedVisualAsset only when purchase/license proof is recorded",
        "notes": "Editorial or sensitive-subject content may have additional restrictions.",
    },
    {
        "id": "getty-images",
        "label": "Getty Images",
        "tier": "licensed",
        "kind": "paid-stock-provider",
        "license_scope": ["Getty Images royalty-free", "Getty Images rights-managed"],
        "attribution_default": "license-dependent",
        "license_proof_required": True,
        "asset_usage": "may become SourcedVisualAsset only when use-specific license proof is recorded",
        "notes": "Rights-managed assets are use-specific; record the permitted usage scope.",
    },
    {
        "id": "istock",
        "label": "iStock",
        "tier": "licensed",
        "kind": "paid-stock-provider",
        "license_scope": ["iStock Standard License", "iStock Extended License"],
        "attribution_default": "license-dependent",
        "license_proof_required": True,
        "asset_usage": "may become SourcedVisualAsset only when purchase/license proof is recorded",
        "notes": "Use only under the user's account or supplied license documentation.",
    },
    {
        "id": "envato-elements",
        "label": "Envato Elements",
        "tier": "licensed",
        "kind": "subscription-asset-provider",
        "license_scope": ["Envato Elements License"],
        "attribution_default": "license-dependent",
        "license_proof_required": True,
        "asset_usage": "may become SourcedVisualAsset only when project registration/license proof is recorded",
        "notes": "Record project registration or equivalent license evidence for each asset.",
    },
    {
        "id": "local-licensed-file",
        "label": "Local licensed file",
        "tier": "licensed",
        "kind": "user-supplied-or-curated",
        "license_scope": ["explicit project permission"],
        "attribution_default": "project-defined",
        "license_proof_required": True,
        "asset_usage": "may become SourcedVisualAsset when explicit project permission is recorded",
        "notes": "Use when the user provides or curates an asset with redistribution permission.",
    },
]

REFERENCE_ONLY_PROVIDER_RULES = [
    {
        "id": "lazyweb",
        "label": "Lazyweb",
        "tier": "reference-only",
        "kind": "design-reference-corpus",
        "license_scope": ["reference use only"],
        "attribution_default": "not applicable",
        "license_proof_required": False,
        "asset_usage": "morphology and UX reference only; do not copy images into runtime assets",
        "notes": "Use for layout, density, hierarchy, and product morphology research.",
    },
    {
        "id": "mobbin",
        "label": "Mobbin",
        "tier": "reference-only",
        "kind": "app-screen-reference",
        "license_scope": ["reference use only"],
        "attribution_default": "not applicable",
        "license_proof_required": False,
        "asset_usage": "morphology and UX reference only; do not copy images into runtime assets",
        "notes": "Use for app UI patterns, flows, and screen density research.",
    },
    {
        "id": "dribbble",
        "label": "Dribbble",
        "tier": "reference-only",
        "kind": "design-inspiration-site",
        "license_scope": ["reference use only unless explicitly licensed"],
        "attribution_default": "not applicable",
        "license_proof_required": False,
        "asset_usage": "inspiration/reference only; do not copy images into runtime assets",
        "notes": "Treat as visual inspiration; avoid copying composition, imagery, or brand work.",
    },
    {
        "id": "behance",
        "label": "Behance",
        "tier": "reference-only",
        "kind": "portfolio-reference-site",
        "license_scope": ["reference use only unless explicitly licensed"],
        "attribution_default": "not applicable",
        "license_proof_required": False,
        "asset_usage": "inspiration/reference only; do not copy images into runtime assets",
        "notes": "Use as design research, not as an asset source.",
    },
    {
        "id": "awwwards",
        "label": "Awwwards",
        "tier": "reference-only",
        "kind": "website-reference-gallery",
        "license_scope": ["reference use only"],
        "attribution_default": "not applicable",
        "license_proof_required": False,
        "asset_usage": "morphology and interaction reference only; do not copy images into runtime assets",
        "notes": "Use for layout and interaction research, not for runtime media assets.",
    },
]

VISUAL_ASSET_PROVIDER_RULES = (
    FREE_SOURCED_VISUAL_PROVIDER_RULES
    + LICENSED_VISUAL_PROVIDER_RULES
    + REFERENCE_ONLY_PROVIDER_RULES
)
SOURCED_VISUAL_PROVIDER_RULES = FREE_SOURCED_VISUAL_PROVIDER_RULES + LICENSED_VISUAL_PROVIDER_RULES

FREE_SOURCED_VISUAL_ASSET_LICENSE_POLICY = {
    "id": "license-policy:verified-free-visual-asset",
    "label": "Verified free visual asset license",
    "allowed_license_kinds": [
        "CC0",
        "Public Domain",
        "CC BY",
        "CC BY-SA",
        "Unsplash License",
        "Pexels License",
        "explicit project permission",
    ],
    "required_metadata": [
        "source_url",
        "download_url",
        "provider",
        "author",
        "license",
        "attribution_required",
        "retrieved_at",
        "sha256",
    ],
    "denied": [
        "unknown license",
        "metadata-free image search result",
        "hotlinked runtime asset",
        "logo or app icon replacement from stock/search",
        "rights-unclear celebrity, character, brand, or private-location imagery",
    ],
}
LICENSED_VISUAL_ASSET_PROOF_POLICY = {
    "id": "license-policy:paid-visual-provider-proof",
    "label": "Paid visual provider license proof",
    "required_metadata": [
        "provider",
        "source_url",
        "download_url",
        "license",
        "license_proof",
        "usage_scope",
        "licensed_to",
        "retrieved_at",
        "sha256",
    ],
    "denied": [
        "paid stock asset without purchase proof",
        "account-only asset with no project license record",
        "editorial asset used commercially without clearance",
        "rights-managed asset used outside recorded usage scope",
    ],
}
REFERENCE_ONLY_VISUAL_POLICY = {
    "id": "license-policy:reference-only-provider-no-runtime-assets",
    "label": "Reference-only provider no runtime assets",
    "allowed": [
        "component morphology",
        "layout density",
        "interaction pattern",
        "module hierarchy",
        "screen flow notes",
    ],
    "denied": [
        "runtime image asset",
        "downloaded stock/photo asset",
        "brand artwork copy",
        "competitor UI screenshot as shipped content",
        "logo, icon, or illustration reuse",
    ],
}

VISUAL_ASSET_SLOT_RULES = [
    {
        "slot": "brand-aligned-raster",
        "label": "Brand-aligned raster image",
        "keywords": (),
        "family_keywords": (),
        "aspect_ratios": ["16:9", "4:3", "1:1"],
        "usage": "Optional Codex imagery when a screen needs professional raster substance.",
        "activation": "only when the implementation surface would benefit from generated imagery",
        "medium_role": "high-fidelity-raster-support",
        "default_acquisition_modes": ["image_gen", "user_supplied", "sourced"],
        "deterministic_svg_allowed": False,
    },
    {
        "slot": "hero-image",
        "label": "Hero image",
        "keywords": ("hero", "landing", "spotlight", "masthead", "feature"),
        "family_keywords": ("marketing",),
        "aspect_ratios": ["16:9", "3:2"],
        "usage": "First-viewport visual signal for landing, product, or editorial hero sections.",
        "activation": "hero, landing, product, or editorial first screen",
        "medium_role": "high-fidelity-raster-support",
        "default_acquisition_modes": ["image_gen", "user_supplied", "sourced"],
        "deterministic_svg_allowed": False,
    },
    {
        "slot": "card-thumbnail",
        "label": "Card thumbnail",
        "keywords": ("card", "thumbnail", "media", "product", "gallery", "case-study"),
        "family_keywords": ("marketing", "data-display", "editorial"),
        "aspect_ratios": ["4:3", "1:1"],
        "usage": "Content image for product, venue, object, media, or feature cards.",
        "activation": "card grids or repeated content surfaces need real visual content",
        "medium_role": "content-media",
        "default_acquisition_modes": ["image_gen", "user_supplied", "sourced"],
        "deterministic_svg_allowed": "only for approved product schematics or semantic vector thumbnails",
    },
    {
        "slot": "editorial-cover",
        "label": "Editorial cover",
        "keywords": ("editorial", "article", "cover", "story", "case-study", "press"),
        "family_keywords": ("editorial", "marketing"),
        "aspect_ratios": ["4:5", "3:4"],
        "usage": "Cover image for articles, case studies, press stories, or narrative modules.",
        "activation": "editorial or story-led content module",
        "medium_role": "high-fidelity-narrative-media",
        "default_acquisition_modes": ["image_gen", "user_supplied", "sourced"],
        "deterministic_svg_allowed": "denied unless approved production vector artwork exists",
    },
    {
        "slot": "comic-cover",
        "label": "Comic/manga cover art",
        "keywords": ("comic", "manga", "webtoon", "toon", "cover", "issue", "magazine", "만화", "웹툰", "표지", "잡지"),
        "family_keywords": (),
        "aspect_ratios": ["2:3", "3:4", "4:5"],
        "usage": "Finished cover artwork for comic, manga, webtoon, or illustrated magazine content.",
        "activation": "comic, manga, webtoon, magazine issue, or cover-led reader surface",
        "medium_role": "high-fidelity-narrative-media",
        "default_acquisition_modes": ["image_gen", "user_supplied", "sourced"],
        "deterministic_svg_allowed": "denied unless approved production vector cover art exists",
    },
    {
        "slot": "comic-panel-preview",
        "label": "Comic panel preview",
        "keywords": ("panel", "strip", "episode", "chapter", "reader", "comic", "manga", "webtoon", "컷", "회차", "연재"),
        "family_keywords": (),
        "aspect_ratios": ["2:1", "16:9", "4:3"],
        "usage": "Finished panel or strip preview artwork for story-led comic content.",
        "activation": "comic reader, webtoon episode, manga chapter, or panel-preview rail",
        "medium_role": "high-fidelity-narrative-media",
        "default_acquisition_modes": ["image_gen", "user_supplied", "sourced"],
        "deterministic_svg_allowed": "denied unless approved production vector panel art exists",
    },
    {
        "slot": "empty-state-illustration",
        "label": "Empty-state illustration",
        "keywords": ("empty-state", "onboarding", "welcome", "blank", "no-results"),
        "family_keywords": ("feedback",),
        "aspect_ratios": ["4:3", "1:1"],
        "usage": "Supportive illustration for empty states, onboarding, or no-result panels.",
        "activation": "empty state benefits from clarification without replacing text",
        "medium_role": "supportive-illustration",
        "default_acquisition_modes": ["image_gen", "deterministic_svg", "user_supplied", "sourced"],
        "deterministic_svg_allowed": "allowed when polished, semantic, and not substituting for content media",
    },
]


def build_generated_visual_asset_layer(
    graph: DesignOntologyGraph,
    brand_profile: dict,
    blueprint: dict,
    component_inventory: dict,
) -> None:
    """Represent generated imagery plus sourced visual fallback as ontology nodes and edges."""
    brand_name = brand_profile.get("brand_name", "Brand")
    brand_id = f"brand:{slugify(brand_name)}"
    model_id = VISUAL_IMAGE_GENERATOR_ID

    _add_visual_asset_contract_nodes(graph)
    _add_sourced_visual_asset_contract_nodes(graph, brand_id)

    graph.add_node(OntologyNode(
        id=model_id,
        type=NodeType.ImageGenerationModel,
        label=VISUAL_IMAGE_GENERATOR_LABEL,
        meta={
            "runtime": "Codex built-in image_gen skill",
            "default_path": True,
            "selection_rule": "Use the Codex imagegen skill's built-in image_gen tool for default generated imagery.",
            "fallback_policy": VISUAL_IMAGE_GENERATOR_FAILURE_POLICY,
            "sourced_fallback_policy": SOURCED_VISUAL_ASSET_FALLBACK_POLICY,
            "api_fallback": "disabled",
            "failure_behavior": "If built-in image_gen is unavailable or fails, use the license-verified sourced visual fallback or write a prompt pack; do not invoke CLI or OpenAI API fallback.",
            "source_session_tracking": True,
            "default_source_directory": "$CODEX_HOME/generated_images/<session-id>",
            "workspace_copy_required": True,
            "contract_id": VISUAL_ASSET_CONTRACT_ID,
            "fallback_contract_id": SOURCED_VISUAL_ASSET_CONTRACT_ID,
        },
    ))
    graph.add_edge(OntologyEdge(type=EdgeType.governs, source=VISUAL_ASSET_CONTRACT_ID, target=model_id))
    graph.add_edge(OntologyEdge(type=EdgeType.governs, source=SOURCED_VISUAL_ASSET_CONTRACT_ID, target=model_id))

    for manifest in _iter_generated_visual_asset_manifests(brand_profile, blueprint):
        _add_integrated_visual_assets_from_manifest(
            graph=graph,
            manifest=manifest,
            brand_id=brand_id,
            model_id=model_id,
        )

    prompt_basis = [
        "system_spec.md",
        "token_schema.json",
        "component_inventory.json",
        "components/component_specs.md",
    ]
    if brand_profile.get("_resolved_visual_reference") or blueprint.get("visual_reference"):
        prompt_basis.append("visual_reference_report.json")

    slot_plans = _infer_visual_asset_slots(component_inventory)
    for rule, targets in slot_plans:
        asset_id = f"visual-asset:{rule['slot']}"
        graph.add_node(OntologyNode(
            id=asset_id,
            type=NodeType.GeneratedVisualAsset,
            label=rule["label"],
            meta={
                "slot": rule["slot"],
                "model": VISUAL_IMAGE_GENERATOR_LABEL,
                "api_fallback": "disabled",
                "fallback_policy": VISUAL_IMAGE_GENERATOR_FAILURE_POLICY,
                "failure_behavior": "Do not call external image APIs if Codex image_gen fails.",
                "candidate_count": "2-4",
                "manifest_path": VISUAL_ASSET_MANIFEST_PATH,
                "compatible_manifest_paths": VISUAL_ASSET_COMPATIBLE_MANIFEST_PATHS,
                "manifest_schema": VISUAL_ASSET_MANIFEST_SCHEMA,
                "manifest_required_fields": VISUAL_ASSET_MANIFEST_REQUIRED_FIELDS,
                "asset_record_required_fields": VISUAL_ASSET_RECORD_REQUIRED_FIELDS,
                "prompt_pack_path": VISUAL_ASSET_PROMPT_PACK_PATH,
                "prompt_basis": prompt_basis,
                "aspect_ratios": rule["aspect_ratios"],
                "usage": rule["usage"],
                "activation": rule["activation"],
                "medium_role": rule.get("medium_role", "brand-aligned-raster"),
                "default_acquisition_modes": rule.get("default_acquisition_modes", ["image_gen", "user_supplied", "sourced"]),
                "deterministic_svg_allowed": rule.get("deterministic_svg_allowed", False),
                "medium_selection_policy_id": VISUAL_ASSET_MEDIUM_SELECTION_POLICY_ID,
                "alt_text_required": True,
                "prompt_summary_required": True,
                "sha256_required": True,
                "original_preservation_required": True,
                "workspace_copy_required": True,
                "source_session_tracking": True,
                "contract_id": VISUAL_ASSET_CONTRACT_ID,
                "status": "promptable",
            },
        ))
        graph.add_edge(OntologyEdge(type=EdgeType.generated_with, source=asset_id, target=model_id))
        graph.add_edge(OntologyEdge(type=EdgeType.governs, source=VISUAL_ASSET_CONTRACT_ID, target=asset_id))
        if graph.get_node(brand_id):
            graph.add_edge(OntologyEdge(type=EdgeType.grounded_in, source=asset_id, target=brand_id))

        for principle in blueprint.get("principles", []):
            principle_id = f"principle:{slugify(principle['keyword'])}"
            if graph.get_node(principle_id):
                graph.add_edge(OntologyEdge(type=EdgeType.constrains, source=principle_id, target=asset_id))

        for target_id in targets:
            if graph.get_node(target_id):
                graph.add_edge(OntologyEdge(type=EdgeType.intended_for, source=asset_id, target=target_id))

        _add_sourced_visual_asset_slot_plan(
            graph=graph,
            rule=rule,
            targets=targets,
            brand_id=brand_id,
        )

    visual_policy = graph.get_node("governance:mockup-visual-substance")
    if visual_policy:
        for target_id in (
            VISUAL_ASSET_CONTRACT_ID,
            SOURCED_VISUAL_ASSET_CONTRACT_ID,
            model_id,
            "identity-asset:app-icon",
        ):
            if graph.get_node(target_id):
                graph.add_edge(OntologyEdge(type=EdgeType.enforces, source=visual_policy.id, target=target_id))
        for asset in (
            graph.get_nodes_by_type(NodeType.GeneratedVisualAsset)
            + graph.get_nodes_by_type(NodeType.SourcedVisualAsset)
        ):
            graph.add_edge(OntologyEdge(type=EdgeType.enforces, source=visual_policy.id, target=asset.id))

    medium_policy = graph.get_node(VISUAL_ASSET_MEDIUM_SELECTION_POLICY_ID)
    if medium_policy:
        for target_id in (
            VISUAL_ASSET_CONTRACT_ID,
            SOURCED_VISUAL_ASSET_CONTRACT_ID,
            model_id,
        ):
            if graph.get_node(target_id):
                graph.add_edge(OntologyEdge(type=EdgeType.enforces, source=medium_policy.id, target=target_id))
        for asset in (
            graph.get_nodes_by_type(NodeType.GeneratedVisualAsset)
            + graph.get_nodes_by_type(NodeType.SourcedVisualAsset)
            + graph.get_nodes_by_type(NodeType.BrandIdentityAsset)
        ):
            graph.add_edge(OntologyEdge(type=EdgeType.enforces, source=medium_policy.id, target=asset.id))


def _add_visual_asset_contract_nodes(graph: DesignOntologyGraph) -> None:
    graph.add_node(OntologyNode(
        id=VISUAL_ASSET_CONTRACT_ID,
        type=NodeType.GovernanceRule,
        label="Generated visual asset contract",
        meta={
            "schema_version": VISUAL_ASSET_MANIFEST_SCHEMA,
            "preferred_manifest_path": VISUAL_ASSET_MANIFEST_PATH,
            "compatible_manifest_paths": VISUAL_ASSET_COMPATIBLE_MANIFEST_PATHS,
            "prompt_pack_path": VISUAL_ASSET_PROMPT_PACK_PATH,
            "default_source_directory": "$CODEX_HOME/generated_images/<session-id>",
            "preserve_originals": True,
            "workspace_copy_required": True,
            "runtime_code_must_not_reference_codex_home": True,
            "api_fallback": "disabled",
            "failure_policy": VISUAL_IMAGE_GENERATOR_FAILURE_POLICY,
            "manifest_required_fields": VISUAL_ASSET_MANIFEST_REQUIRED_FIELDS,
            "asset_record_required_fields": VISUAL_ASSET_RECORD_REQUIRED_FIELDS,
            "rules": VISUAL_ASSET_CONTRACT_RULES,
            "medium_selection_policy_id": VISUAL_ASSET_MEDIUM_SELECTION_POLICY_ID,
            "source_project_pattern": "sprout-community-mock/design-system/generated_visual_assets.json",
        },
    ))

    failure_patterns = [
        {
            "id": "failure-pattern:generated-image-api-fallback",
            "label": "Generated image API fallback",
            "trigger": "Implementation calls a CLI, SDK runner, or OpenAI image API after Codex image_gen is unavailable or fails.",
            "prevention": "Stop, report the skipped generation, and write imagegen-prompts.md instead of silently changing generation path.",
        },
        {
            "id": "failure-pattern:generated-image-untracked-asset",
            "label": "Untracked generated image",
            "trigger": "A generated raster image is referenced by product code without a manifest record.",
            "prevention": "Record asset_path, original_png_path, dimensions, sha256, intended_for, alt_text, and prompt_summary before wiring the asset.",
        },
        {
            "id": "failure-pattern:generated-image-codex-home-runtime-reference",
            "label": "Codex home runtime asset reference",
            "trigger": "Runtime HTML/CSS/JS points at $CODEX_HOME or another agent-local generated image path.",
            "prevention": "Copy the final asset into the workspace and reference the workspace-relative asset path only.",
        },
        {
            "id": "failure-pattern:generated-image-missing-accessibility-record",
            "label": "Generated image missing accessibility record",
            "trigger": "A generated visual asset is integrated without alt_text or an intended_for target.",
            "prevention": "Treat alt text and target component linkage as required manifest fields, not implementation notes.",
        },
        {
            "id": "failure-pattern:wrong-medium-svg-for-narrative-media",
            "label": "Wrong medium SVG for narrative media",
            "trigger": "A narrative/content media slot such as a comic cover, panel preview, story scene, or editorial cover is implemented with a rough or placeholder SVG.",
            "prevention": "Use image_gen, user-supplied artwork, sourced imagery, or approved high-fidelity artwork; reserve deterministic SVG for identity, controls, diagrams, maps, charts, or schematics.",
        },
    ]
    for failure in failure_patterns:
        graph.add_node(OntologyNode(
            id=failure["id"],
            type=NodeType.ImplementationFailurePattern,
            label=failure["label"],
            meta={
                "trigger": failure["trigger"],
                "prevention": failure["prevention"],
                "technical_controls": [
                    "system_ontology.json GeneratedVisualAsset",
                    "system_spec.md Generated Visual Asset Plan",
                    VISUAL_ASSET_MANIFEST_PATH,
                    VISUAL_ASSET_PROMPT_PACK_PATH,
                ],
            },
        ))
        graph.add_edge(OntologyEdge(type=EdgeType.prevents, source=VISUAL_ASSET_CONTRACT_ID, target=failure["id"]))


def _add_sourced_visual_asset_contract_nodes(graph: DesignOntologyGraph, brand_id: str) -> None:
    graph.add_node(OntologyNode(
        id=SOURCED_VISUAL_ASSET_CONTRACT_ID,
        type=NodeType.GovernanceRule,
        label="Sourced visual asset fallback contract",
        meta={
            "schema_version": VISUAL_ASSET_MANIFEST_SCHEMA,
            "preferred_manifest_path": VISUAL_ASSET_MANIFEST_PATH,
            "candidate_manifest_path": SOURCED_VISUAL_ASSET_CANDIDATE_MANIFEST_PATH,
            "compatible_manifest_paths": VISUAL_ASSET_COMPATIBLE_MANIFEST_PATHS,
            "fallback_policy": SOURCED_VISUAL_ASSET_FALLBACK_POLICY,
            "fallback_for": VISUAL_ASSET_CONTRACT_ID,
            "api_fallback": "disabled",
            "hotlinking_allowed": False,
            "workspace_copy_required": True,
            "license_metadata_required": True,
            "asset_record_required_fields": SOURCED_VISUAL_ASSET_RECORD_REQUIRED_FIELDS,
            "provider_allowlist": [provider["id"] for provider in SOURCED_VISUAL_PROVIDER_RULES],
            "free_provider_allowlist": [provider["id"] for provider in FREE_SOURCED_VISUAL_PROVIDER_RULES],
            "licensed_provider_allowlist": [provider["id"] for provider in LICENSED_VISUAL_PROVIDER_RULES],
            "reference_only_providers": [provider["id"] for provider in REFERENCE_ONLY_PROVIDER_RULES],
            "license_policy_id": FREE_SOURCED_VISUAL_ASSET_LICENSE_POLICY["id"],
            "paid_license_policy_id": LICENSED_VISUAL_ASSET_PROOF_POLICY["id"],
            "reference_only_policy_id": REFERENCE_ONLY_VISUAL_POLICY["id"],
            "medium_selection_policy_id": VISUAL_ASSET_MEDIUM_SELECTION_POLICY_ID,
            "rules": SOURCED_VISUAL_ASSET_CONTRACT_RULES,
        },
    ))
    if graph.get_node(brand_id):
        graph.add_edge(OntologyEdge(type=EdgeType.grounded_in, source=SOURCED_VISUAL_ASSET_CONTRACT_ID, target=brand_id))

    free_license_policy_id = FREE_SOURCED_VISUAL_ASSET_LICENSE_POLICY["id"]
    graph.add_node(OntologyNode(
        id=free_license_policy_id,
        type=NodeType.LicensePolicy,
        label=FREE_SOURCED_VISUAL_ASSET_LICENSE_POLICY["label"],
        meta={
            "provider_tier": "free-sourced",
            "allowed_license_kinds": FREE_SOURCED_VISUAL_ASSET_LICENSE_POLICY["allowed_license_kinds"],
            "required_metadata": FREE_SOURCED_VISUAL_ASSET_LICENSE_POLICY["required_metadata"],
            "denied": FREE_SOURCED_VISUAL_ASSET_LICENSE_POLICY["denied"],
        },
    ))
    graph.add_edge(OntologyEdge(type=EdgeType.governs, source=SOURCED_VISUAL_ASSET_CONTRACT_ID, target=free_license_policy_id))

    paid_license_policy_id = LICENSED_VISUAL_ASSET_PROOF_POLICY["id"]
    graph.add_node(OntologyNode(
        id=paid_license_policy_id,
        type=NodeType.LicensePolicy,
        label=LICENSED_VISUAL_ASSET_PROOF_POLICY["label"],
        meta={
            "provider_tier": "licensed",
            "required_metadata": LICENSED_VISUAL_ASSET_PROOF_POLICY["required_metadata"],
            "denied": LICENSED_VISUAL_ASSET_PROOF_POLICY["denied"],
        },
    ))
    graph.add_edge(OntologyEdge(type=EdgeType.governs, source=SOURCED_VISUAL_ASSET_CONTRACT_ID, target=paid_license_policy_id))

    reference_only_policy_id = REFERENCE_ONLY_VISUAL_POLICY["id"]
    graph.add_node(OntologyNode(
        id=reference_only_policy_id,
        type=NodeType.LicensePolicy,
        label=REFERENCE_ONLY_VISUAL_POLICY["label"],
        meta={
            "provider_tier": "reference-only",
            "allowed": REFERENCE_ONLY_VISUAL_POLICY["allowed"],
            "denied": REFERENCE_ONLY_VISUAL_POLICY["denied"],
        },
    ))
    graph.add_edge(OntologyEdge(type=EdgeType.governs, source=SOURCED_VISUAL_ASSET_CONTRACT_ID, target=reference_only_policy_id))

    for provider in VISUAL_ASSET_PROVIDER_RULES:
        provider_id = f"visual-asset-provider:{slugify(provider['id'])}"
        graph.add_node(OntologyNode(
            id=provider_id,
            type=_visual_asset_provider_node_type(provider),
            label=provider["label"],
            meta={
                "provider_id": provider["id"],
                "tier": provider["tier"],
                "kind": provider["kind"],
                "license_scope": provider["license_scope"],
                "attribution_default": provider["attribution_default"],
                "license_proof_required": provider["license_proof_required"],
                "license_metadata_required": True,
                "workspace_copy_required": provider["tier"] != "reference-only",
                "asset_copy_allowed": provider["tier"] != "reference-only",
                "asset_usage": provider["asset_usage"],
                "notes": provider["notes"],
            },
        ))
        graph.add_edge(OntologyEdge(type=EdgeType.governs, source=SOURCED_VISUAL_ASSET_CONTRACT_ID, target=provider_id))

    failure_patterns = [
        {
            "id": "failure-pattern:unverified-search-image",
            "label": "Unverified search image",
            "trigger": "A free image search result is integrated without source URL, author, license, or attribution metadata.",
            "prevention": "Use only allowlisted providers or user-supplied files with explicit permission, and record full license metadata before implementation.",
        },
        {
            "id": "failure-pattern:hotlinked-sourced-visual",
            "label": "Hotlinked sourced visual",
            "trigger": "Runtime code references a remote search/CDN URL instead of a workspace-local asset copy.",
            "prevention": "Download or copy the accepted visual into the project assets folder and reference the workspace path only.",
        },
        {
            "id": "failure-pattern:stock-image-as-identity-asset",
            "label": "Stock image used as identity asset",
            "trigger": "A searched photo or illustration is used as an app icon, favicon, logo, button glyph, status marker, or flag substitute.",
            "prevention": "Keep identity assets deterministic and brand-specific; use sourced images only for content, hero, card, editorial, or contextual imagery slots.",
        },
        {
            "id": "failure-pattern:missing-visual-attribution",
            "label": "Missing sourced visual attribution",
            "trigger": "A sourced visual requiring attribution is shipped without visible or documented credit.",
            "prevention": "Record attribution_required and attribution_text in the manifest, then place or document the credit according to the license.",
        },
    ]
    for failure in failure_patterns:
        graph.add_node(OntologyNode(
            id=failure["id"],
            type=NodeType.ImplementationFailurePattern,
            label=failure["label"],
            meta={
                "trigger": failure["trigger"],
                "prevention": failure["prevention"],
                "technical_controls": [
                    "system_ontology.json SourcedVisualAsset",
                    "system_spec.md Generated Visual Asset Plan",
                    VISUAL_ASSET_MANIFEST_PATH,
                    SOURCED_VISUAL_ASSET_CANDIDATE_MANIFEST_PATH,
                ],
            },
        ))
        graph.add_edge(OntologyEdge(type=EdgeType.prevents, source=SOURCED_VISUAL_ASSET_CONTRACT_ID, target=failure["id"]))


def _visual_asset_provider_node_type(provider: dict) -> NodeType:
    tier = str(provider.get("tier") or "").strip().lower()
    if tier == "free-sourced":
        return NodeType.FreeSourcedVisualProvider
    if tier == "licensed":
        return NodeType.LicensedVisualProvider
    if tier == "reference-only":
        return NodeType.ReferenceOnlyProvider
    return NodeType.VisualAssetProvider


def _visual_asset_provider_rule(provider_id: str) -> dict | None:
    normalized = slugify(provider_id)
    for provider in VISUAL_ASSET_PROVIDER_RULES:
        if slugify(str(provider.get("id", ""))) == normalized:
            return provider
    return None


def _license_policy_id_for_provider_rule(provider: dict | None) -> str:
    tier = str((provider or {}).get("tier") or "").strip().lower()
    if tier == "licensed":
        return LICENSED_VISUAL_ASSET_PROOF_POLICY["id"]
    if tier == "reference-only":
        return REFERENCE_ONLY_VISUAL_POLICY["id"]
    return FREE_SOURCED_VISUAL_ASSET_LICENSE_POLICY["id"]


def _add_sourced_visual_asset_slot_plan(
    graph: DesignOntologyGraph,
    rule: dict,
    targets: list[str],
    brand_id: str,
) -> None:
    asset_id = f"sourced-visual-asset:{rule['slot']}-fallback"
    provider_ids = [f"visual-asset-provider:{slugify(provider['id'])}" for provider in SOURCED_VISUAL_PROVIDER_RULES]
    graph.add_node(OntologyNode(
        id=asset_id,
        type=NodeType.SourcedVisualAsset,
        label=f"{rule['label']} sourced fallback",
        meta={
            "slot": rule["slot"],
            "acquisition_mode": "sourced",
            "fallback_for": f"visual-asset:{rule['slot']}",
            "fallback_policy": SOURCED_VISUAL_ASSET_FALLBACK_POLICY,
            "candidate_manifest_path": SOURCED_VISUAL_ASSET_CANDIDATE_MANIFEST_PATH,
            "manifest_path": VISUAL_ASSET_MANIFEST_PATH,
            "compatible_manifest_paths": VISUAL_ASSET_COMPATIBLE_MANIFEST_PATHS,
            "manifest_schema": VISUAL_ASSET_MANIFEST_SCHEMA,
            "asset_record_required_fields": SOURCED_VISUAL_ASSET_RECORD_REQUIRED_FIELDS,
            "provider_allowlist": [provider["id"] for provider in SOURCED_VISUAL_PROVIDER_RULES],
            "free_provider_allowlist": [provider["id"] for provider in FREE_SOURCED_VISUAL_PROVIDER_RULES],
            "licensed_provider_allowlist": [provider["id"] for provider in LICENSED_VISUAL_PROVIDER_RULES],
            "reference_only_excluded": [provider["id"] for provider in REFERENCE_ONLY_PROVIDER_RULES],
            "license_policy_id": FREE_SOURCED_VISUAL_ASSET_LICENSE_POLICY["id"],
            "paid_license_policy_id": LICENSED_VISUAL_ASSET_PROOF_POLICY["id"],
            "aspect_ratios": rule["aspect_ratios"],
            "usage": rule["usage"],
            "activation": rule["activation"],
            "medium_role": rule.get("medium_role", "content-media"),
            "default_acquisition_modes": rule.get("default_acquisition_modes", ["image_gen", "user_supplied", "sourced"]),
            "deterministic_svg_allowed": rule.get("deterministic_svg_allowed", False),
            "medium_selection_policy_id": VISUAL_ASSET_MEDIUM_SELECTION_POLICY_ID,
            "hotlinking_allowed": False,
            "workspace_copy_required": True,
            "license_metadata_required": True,
            "alt_text_required": True,
            "sha256_required": True,
            "selection_reason_required": True,
            "status": "searchable-fallback",
            "contract_id": SOURCED_VISUAL_ASSET_CONTRACT_ID,
        },
    ))
    graph.add_edge(OntologyEdge(type=EdgeType.governs, source=SOURCED_VISUAL_ASSET_CONTRACT_ID, target=asset_id))
    graph.add_edge(OntologyEdge(type=EdgeType.licensed_under, source=asset_id, target=FREE_SOURCED_VISUAL_ASSET_LICENSE_POLICY["id"]))
    if graph.get_node(brand_id):
        graph.add_edge(OntologyEdge(type=EdgeType.grounded_in, source=asset_id, target=brand_id))
    for provider_id in provider_ids:
        if graph.get_node(provider_id):
            graph.add_edge(OntologyEdge(type=EdgeType.sourced_from, source=asset_id, target=provider_id))
    for target_id in targets:
        if graph.get_node(target_id):
            graph.add_edge(OntologyEdge(type=EdgeType.intended_for, source=asset_id, target=target_id))


def _iter_generated_visual_asset_manifests(brand_profile: dict, blueprint: dict) -> list[dict]:
    manifests: list[dict] = []
    seen: set[str] = set()
    for candidate_list in (
        brand_profile.get("_generated_visual_asset_manifests", []),
        blueprint.get("generated_visual_assets", []),
    ):
        if not isinstance(candidate_list, list):
            continue
        for manifest in candidate_list:
            if not isinstance(manifest, dict):
                continue
            key = str(manifest.get("absolute_path") or manifest.get("path") or id(manifest))
            if key in seen:
                continue
            seen.add(key)
            manifests.append(manifest)
    return manifests


def _add_integrated_visual_assets_from_manifest(
    graph: DesignOntologyGraph,
    manifest: dict,
    brand_id: str,
    model_id: str,
) -> None:
    source_session = manifest.get("source_session") if isinstance(manifest.get("source_session"), dict) else {}
    manifest_path = str(manifest.get("path") or VISUAL_ASSET_MANIFEST_PATH)
    schema_version = str(manifest.get("schema_version") or VISUAL_ASSET_MANIFEST_SCHEMA)
    assets = manifest.get("assets") or []
    if not isinstance(assets, list):
        return

    for index, asset in enumerate(asset for asset in assets if isinstance(asset, dict)):
        is_sourced = _is_sourced_visual_asset_record(asset)
        raw_id = str(asset.get("id") or "").strip()
        if raw_id:
            if raw_id.startswith(("visual-asset:", "sourced-visual-asset:")):
                asset_id = raw_id
            elif is_sourced:
                asset_id = f"sourced-visual-asset:{slugify(raw_id)}"
            else:
                asset_id = f"visual-asset:{slugify(raw_id)}"
        else:
            fallback = asset.get("label") or asset.get("asset_path") or asset.get("slot") or f"asset-{index + 1}"
            prefix = "sourced-visual-asset" if is_sourced else "visual-asset"
            asset_id = f"{prefix}:{slugify(str(fallback))}"
        if graph.get_node(asset_id):
            asset_id = f"{asset_id}-integrated"

        label = str(asset.get("label") or asset_id.removeprefix("visual-asset:")).strip()
        contract_id = SOURCED_VISUAL_ASSET_CONTRACT_ID if is_sourced else VISUAL_ASSET_CONTRACT_ID
        node_type = NodeType.SourcedVisualAsset if is_sourced else NodeType.GeneratedVisualAsset
        acquisition_mode = str(asset.get("acquisition_mode") or ("sourced" if is_sourced else "generated"))
        provider_id = _asset_provider_id(asset)
        provider_rule = _visual_asset_provider_rule(provider_id) if provider_id else None
        provider_tier = str((provider_rule or {}).get("tier") or "unrecognized")
        meta = {
            "slot": asset.get("slot"),
            "status": asset.get("status", "integrated"),
            "acquisition_mode": acquisition_mode,
            "asset_path": asset.get("asset_path"),
            "original_png_path": asset.get("original_png_path"),
            "format": asset.get("format"),
            "dimensions": asset.get("dimensions"),
            "size_kb": asset.get("size_kb"),
            "sha256": asset.get("sha256"),
            "intended_for": asset.get("intended_for", []),
            "alt_text": asset.get("alt_text"),
            "prompt_summary": asset.get("prompt_summary"),
            "source_url": asset.get("source_url") or asset.get("source_page_url"),
            "download_url": asset.get("download_url"),
            "provider": provider_id,
            "provider_tier": provider_tier if is_sourced else None,
            "author": asset.get("author") or asset.get("creator"),
            "license": _asset_license_label(asset),
            "license_proof": asset.get("license_proof"),
            "usage_scope": asset.get("usage_scope"),
            "licensed_to": asset.get("licensed_to"),
            "attribution_required": asset.get("attribution_required"),
            "attribution_text": asset.get("attribution_text"),
            "retrieved_at": asset.get("retrieved_at"),
            "selection_reason": asset.get("selection_reason"),
            "crop_notes": asset.get("crop_notes"),
            "focal_point": asset.get("focal_point"),
            "manifest_path": manifest_path,
            "manifest_schema": schema_version,
            "manifest_absolute_path": manifest.get("absolute_path"),
            "source_session_id": source_session.get("id"),
            "source_session_directory": source_session.get("default_directory"),
            "model": None if is_sourced else VISUAL_IMAGE_GENERATOR_LABEL,
            "api_fallback": "disabled",
            "fallback_policy": SOURCED_VISUAL_ASSET_FALLBACK_POLICY if is_sourced else VISUAL_IMAGE_GENERATOR_FAILURE_POLICY,
            "workspace_copy_required": True,
            "original_preservation_required": None if is_sourced else True,
            "source_session_tracking": None if is_sourced else True,
            "license_metadata_required": True if is_sourced else None,
            "license_proof_required": provider_rule.get("license_proof_required") if is_sourced and provider_rule else None,
            "hotlinking_allowed": False if is_sourced else None,
            "asset_copy_allowed": provider_tier != "reference-only" if is_sourced else None,
            "candidate_manifest_path": SOURCED_VISUAL_ASSET_CANDIDATE_MANIFEST_PATH if is_sourced else None,
            "asset_record_required_fields": SOURCED_VISUAL_ASSET_RECORD_REQUIRED_FIELDS if is_sourced else None,
            "contract_id": contract_id,
            "integrated": True,
        }
        graph.add_node(OntologyNode(
            id=asset_id,
            type=node_type,
            label=label,
            meta={key: value for key, value in meta.items() if value not in (None, "", [])},
        ))
        if is_sourced:
            provider_node_id = _ensure_manifest_visual_asset_provider(graph, asset)
            if provider_node_id:
                graph.add_edge(OntologyEdge(type=EdgeType.sourced_from, source=asset_id, target=provider_node_id))
            graph.add_edge(OntologyEdge(
                type=EdgeType.licensed_under,
                source=asset_id,
                target=_license_policy_id_for_provider_rule(provider_rule),
            ))
            specific_license_id = _ensure_manifest_license_policy(graph, asset)
            if specific_license_id:
                graph.add_edge(OntologyEdge(type=EdgeType.licensed_under, source=asset_id, target=specific_license_id))
        else:
            graph.add_edge(OntologyEdge(type=EdgeType.generated_with, source=asset_id, target=model_id))
        graph.add_edge(OntologyEdge(type=EdgeType.governs, source=contract_id, target=asset_id))
        if graph.get_node(brand_id):
            graph.add_edge(OntologyEdge(type=EdgeType.grounded_in, source=asset_id, target=brand_id))

        for target in asset.get("intended_for", []) or []:
            target_id = str(target).strip()
            if not target_id:
                continue
            candidate_ids = [
                target_id,
                f"component:{slugify(target_id)}",
                f"family:{slugify(target_id)}",
            ]
            for candidate_id in candidate_ids:
                if graph.get_node(candidate_id):
                    graph.add_edge(OntologyEdge(type=EdgeType.intended_for, source=asset_id, target=candidate_id))
                    break


def _is_sourced_visual_asset_record(asset: dict) -> bool:
    mode = str(asset.get("acquisition_mode") or "").strip().lower()
    if mode in {"sourced", "stock", "free-search", "user_supplied", "user-supplied"}:
        return True
    return any(asset.get(key) for key in ("source_url", "source_page_url", "download_url", "provider", "license", "author"))


def _asset_provider_id(asset: dict) -> str:
    provider = asset.get("provider")
    if isinstance(provider, dict):
        value = provider.get("id") or provider.get("provider_id") or provider.get("name") or provider.get("label")
    else:
        value = provider
    return str(value or "").strip()


def _asset_license_label(asset: dict) -> str:
    license_data = asset.get("license")
    if isinstance(license_data, dict):
        value = license_data.get("label") or license_data.get("id") or license_data.get("name")
    else:
        value = license_data
    return str(value or "").strip()


def _ensure_manifest_visual_asset_provider(graph: DesignOntologyGraph, asset: dict) -> str | None:
    provider_id = _asset_provider_id(asset)
    if not provider_id:
        return None
    node_id = f"visual-asset-provider:{slugify(provider_id)}"
    if graph.get_node(node_id):
        return node_id

    provider_rule = _visual_asset_provider_rule(provider_id)
    provider_meta = provider_rule or {
        "id": provider_id,
        "label": provider_id,
        "tier": "unrecognized",
        "kind": "manifest-provider",
        "license_scope": [],
        "attribution_default": "unknown",
        "license_proof_required": True,
        "asset_usage": "requires manual review before runtime use",
        "notes": "Provider was found in a manifest but is not in the ontology allowlist.",
    }
    graph.add_node(OntologyNode(
        id=node_id,
        type=_visual_asset_provider_node_type(provider_meta),
        label=provider_meta.get("label") or provider_id,
        meta={
            "provider_id": provider_id,
            "tier": provider_meta.get("tier"),
            "kind": provider_meta.get("kind"),
            "license_scope": provider_meta.get("license_scope", []),
            "attribution_default": provider_meta.get("attribution_default"),
            "license_proof_required": provider_meta.get("license_proof_required"),
            "license_metadata_required": True,
            "workspace_copy_required": provider_meta.get("tier") != "reference-only",
            "asset_copy_allowed": provider_meta.get("tier") != "reference-only",
            "asset_usage": provider_meta.get("asset_usage"),
            "allowlist_status": "known" if provider_rule else "unrecognized",
            "notes": provider_meta.get("notes"),
        },
    ))
    graph.add_edge(OntologyEdge(type=EdgeType.governs, source=SOURCED_VISUAL_ASSET_CONTRACT_ID, target=node_id))
    return node_id


def _ensure_manifest_license_policy(graph: DesignOntologyGraph, asset: dict) -> str | None:
    license_label = _asset_license_label(asset)
    if not license_label:
        return None
    node_id = f"license-policy:{slugify(license_label)}"
    if graph.get_node(node_id):
        return node_id

    graph.add_node(OntologyNode(
        id=node_id,
        type=NodeType.LicensePolicy,
        label=license_label,
        meta={
            "source": "visual asset manifest",
            "attribution_required": asset.get("attribution_required"),
            "attribution_text": asset.get("attribution_text"),
            "source_url": asset.get("source_url") or asset.get("source_page_url"),
        },
    ))
    graph.add_edge(OntologyEdge(type=EdgeType.governs, source=SOURCED_VISUAL_ASSET_CONTRACT_ID, target=node_id))
    return node_id


def build_reference_context_layer(
    graph: DesignOntologyGraph,
    brand_profile: dict,
    blueprint: dict,
) -> None:
    """Represent provider-neutral design context as ontology nodes."""

    pack = blueprint.get("design_context_pack") or brand_profile.get("_design_context_pack")
    if not isinstance(pack, dict) or not pack:
        return

    brand_name = brand_profile.get("brand_name") or blueprint.get("brand_name") or "Brand"
    brand_id = f"brand:{slugify(brand_name)}"
    pack_id = "design-context-pack:default"
    graph.add_node(OntologyNode(
        id=pack_id,
        type=NodeType.DesignContextPack,
        label="Design context pack",
        meta={
            "schema_version": pack.get("schema_version"),
            "activation_state": pack.get("activation_state"),
            "purpose": pack.get("purpose"),
            "research_gap_count": len(pack.get("research_gaps", []) or []),
            "authority_order": (pack.get("absorption_policy") or {}).get("authority_order", []),
            "allowed": (pack.get("absorption_policy") or {}).get("allowed", []),
            "denied": (pack.get("absorption_policy") or {}).get("denied", []),
        },
    ))
    if graph.get_node(brand_id):
        graph.add_edge(OntologyEdge(type=EdgeType.grounded_in, source=pack_id, target=brand_id))

    provider_ids: set[str] = set()
    for provider in pack.get("providers", []) or []:
        if not isinstance(provider, dict):
            continue
        provider_id = str(provider.get("provider_id") or provider.get("kind") or "").strip()
        if not provider_id:
            continue
        node_id = f"reference-provider:{slugify(provider_id)}"
        provider_ids.add(provider_id)
        graph.add_node(OntologyNode(
            id=node_id,
            type=NodeType.ReferenceProvider,
            label=provider.get("label") or provider_id,
            meta={
                "provider_id": provider_id,
                "kind": provider.get("kind"),
                "status": provider.get("status"),
                "access_mode": provider.get("access_mode"),
                "truth_role": provider.get("truth_role"),
                "allowed_outputs": provider.get("allowed_outputs", []),
                "denied_outputs": provider.get("denied_outputs", []),
            },
        ))
        graph.add_edge(OntologyEdge(type=EdgeType.provided_by, source=pack_id, target=node_id))

    for card in pack.get("context_cards", [])[:48]:
        if not isinstance(card, dict):
            continue
        context_id = str(card.get("context_id") or card.get("label") or "").strip()
        if not context_id:
            continue
        card_id = f"design-context-card:{slugify(context_id)}"
        graph.add_node(OntologyNode(
            id=card_id,
            type=NodeType.DesignContextCard,
            label=card.get("label") or context_id,
            meta={
                "context_id": context_id,
                "kind": card.get("kind"),
                "status": card.get("status"),
                "provenance_level": card.get("provenance_level"),
                "flows": card.get("flows", []),
                "morphology": card.get("morphology", []),
                "absorbed_traits": card.get("absorbed_traits", []),
                "must_not_absorb": card.get("must_not_absorb", []),
                "source_path": card.get("source_path"),
                "source_url": card.get("source_url"),
            },
        ))
        graph.add_edge(OntologyEdge(type=EdgeType.extracted_from, source=card_id, target=pack_id))
        provider_id = str(card.get("provider_id") or "").strip()
        provider_node_id = f"reference-provider:{slugify(provider_id)}"
        if provider_id in provider_ids and graph.get_node(provider_node_id):
            graph.add_edge(OntologyEdge(type=EdgeType.provided_by, source=card_id, target=provider_node_id))
            graph.add_edge(OntologyEdge(type=EdgeType.captures, source=provider_node_id, target=card_id))


def _infer_visual_asset_slots(component_inventory: dict) -> list[tuple[dict, list[str]]]:
    components = component_inventory.get("components", [])
    families = component_inventory.get("families", [])
    family_names = {
        str(family.get("family", "")).strip().lower()
        for family in families
        if str(family.get("family", "")).strip()
    }
    plans: list[tuple[dict, list[str]]] = [(VISUAL_ASSET_SLOT_RULES[0], [])]

    for rule in VISUAL_ASSET_SLOT_RULES[1:]:
        targets: list[str] = []
        for component in components:
            text = " ".join(
                str(component.get(key, ""))
                for key in ("name", "family", "role", "supports_primitive")
            ).lower()
            if any(keyword in text for keyword in rule["keywords"]):
                targets.append(f"component:{slugify(component.get('name', ''))}")

        for family in families:
            family_name = str(family.get("family", "")).strip()
            if not family_name:
                continue
            if family_name.lower() in rule["family_keywords"]:
                targets.append(f"family:{slugify(family_name)}")

        if targets or any(keyword in family_names for keyword in rule["family_keywords"]):
            plans.append((rule, sorted(set(targets))))

    return plans


# ---------------------------------------------------------------------------
# Governance + feedback promotion layer
# ---------------------------------------------------------------------------


def build_governance_layer(
    graph: DesignOntologyGraph,
    brand_profile: dict,
    blueprint: dict,
) -> None:
    """Promote implementation review learnings into ontology nodes."""
    brand_name = brand_profile.get("brand_name", "Brand")
    brand_id = f"brand:{slugify(brand_name)}"
    governance = blueprint.get("governance") or {}
    reference_scope = governance.get("reference_absorption_scope") or {}
    color_mode_policy = governance.get("color_mode_parity_policy") or {}
    responsive_policy = governance.get("responsive_resilience_policy") or {}
    icon_policy = governance.get("icon_refactor_policy") or {}
    app_icon_policy = governance.get("app_icon_identity_policy") or {}
    visual_substance_policy = governance.get("mockup_visual_substance_policy") or {}
    visual_medium_policy = governance.get("visual_asset_medium_selection_policy") or {}
    commercial_policy = governance.get("commercial_product_realism_policy") or {}

    scope_id = "governance:reference-absorption-scope"
    graph.add_node(OntologyNode(
        id=scope_id,
        type=NodeType.GovernanceRule,
        label="Reference absorption scope",
        meta={
            "rule": reference_scope.get("rule", ""),
            "allowed": reference_scope.get("allowed", []),
            "denied": reference_scope.get("denied", []),
        },
    ))
    if graph.get_node(brand_id):
        graph.add_edge(OntologyEdge(type=EdgeType.grounded_in, source=scope_id, target=brand_id))

    for category in ("color", "typography"):
        target_id = f"token-category:{category}"
        if graph.get_node(target_id):
            graph.add_edge(OntologyEdge(type=EdgeType.enforces, source=scope_id, target=target_id))

    for pattern in reference_scope.get("failure_patterns", []):
        pattern_id = f"failure-pattern:{slugify(pattern.get('id', 'implementation-failure'))}"
        graph.add_node(OntologyNode(
            id=pattern_id,
            type=NodeType.ImplementationFailurePattern,
            label=pattern.get("id", "implementation failure"),
            meta={
                "trigger": pattern.get("trigger", ""),
                "rule": pattern.get("rule", ""),
                "prevention": pattern.get("prevention", ""),
                "technical_controls": pattern.get("technical_controls", []),
            },
        ))
        graph.add_edge(OntologyEdge(type=EdgeType.prevents, source=scope_id, target=pattern_id))

    promotion = governance.get("feedback_promotion_policy") or reference_scope.get("promotion_policy") or {}
    if promotion:
        promotion_id = f"governance:{slugify(promotion.get('id', 'feedback-promotion'))}"
        graph.add_node(OntologyNode(
            id=promotion_id,
            type=NodeType.GovernanceRule,
            label=promotion.get("id", "feedback promotion"),
            meta={
                "rule": promotion.get("rule", ""),
                "outputs": promotion.get("outputs", []),
            },
        ))
        if graph.get_node(brand_id):
            graph.add_edge(OntologyEdge(type=EdgeType.grounded_in, source=promotion_id, target=brand_id))
        graph.add_edge(OntologyEdge(type=EdgeType.enforces, source=promotion_id, target=scope_id))

    if color_mode_policy:
        color_mode_id = f"governance:{slugify(color_mode_policy.get('id', 'color-mode-parity'))}"
        graph.add_node(OntologyNode(
            id=color_mode_id,
            type=NodeType.GovernanceRule,
            label=color_mode_policy.get("id", "color mode parity"),
            meta={
                "rule": color_mode_policy.get("rule", ""),
                "required_modes": color_mode_policy.get("required_modes", []),
                "default_mode": color_mode_policy.get("default_mode", "light"),
                "implementation_rules": color_mode_policy.get("implementation_rules", []),
                "outputs": color_mode_policy.get("outputs", []),
            },
        ))
        if graph.get_node(brand_id):
            graph.add_edge(OntologyEdge(type=EdgeType.grounded_in, source=color_mode_id, target=brand_id))

        for mode in color_mode_policy.get("required_modes", []):
            mode_id = f"color-mode:{slugify(str(mode))}"
            graph.add_node(OntologyNode(
                id=mode_id,
                type=NodeType.ColorMode,
                label=str(mode),
                meta={
                    "required": True,
                    "default": mode == color_mode_policy.get("default_mode", "light"),
                    "source_policy": color_mode_id,
                },
            ))
            graph.add_edge(OntologyEdge(type=EdgeType.governs, source=color_mode_id, target=mode_id))
            graph.add_edge(OntologyEdge(type=EdgeType.defines, source=color_mode_id, target=mode_id))

        for pattern in color_mode_policy.get("failure_patterns", []):
            pattern_id = f"failure-pattern:{slugify(pattern.get('id', 'color-mode-failure'))}"
            graph.add_node(OntologyNode(
                id=pattern_id,
                type=NodeType.ImplementationFailurePattern,
                label=pattern.get("id", "color mode failure"),
                meta={
                    "trigger": pattern.get("trigger", ""),
                    "rule": pattern.get("rule", ""),
                    "prevention": pattern.get("prevention", ""),
                    "technical_controls": pattern.get("technical_controls", []),
                },
            ))
            graph.add_edge(OntologyEdge(type=EdgeType.prevents, source=color_mode_id, target=pattern_id))

    if responsive_policy:
        responsive_id = f"governance:{slugify(responsive_policy.get('id', 'responsive-resilience'))}"
        graph.add_node(OntologyNode(
            id=responsive_id,
            type=NodeType.GovernanceRule,
            label=responsive_policy.get("id", "responsive resilience"),
            meta={
                "rule": responsive_policy.get("rule", ""),
                "viewport_contract": responsive_policy.get("viewport_contract", {}),
                "control_rules": responsive_policy.get("control_rules", []),
                "outputs": responsive_policy.get("outputs", []),
            },
        ))
        if graph.get_node(brand_id):
            graph.add_edge(OntologyEdge(type=EdgeType.grounded_in, source=responsive_id, target=brand_id))

        for pattern in responsive_policy.get("failure_patterns", []):
            pattern_id = f"failure-pattern:{slugify(pattern.get('id', 'responsive-failure'))}"
            graph.add_node(OntologyNode(
                id=pattern_id,
                type=NodeType.ImplementationFailurePattern,
                label=pattern.get("id", "responsive failure"),
                meta={
                    "trigger": pattern.get("trigger", ""),
                    "rule": pattern.get("rule", ""),
                    "prevention": pattern.get("prevention", ""),
                    "technical_controls": pattern.get("technical_controls", []),
                },
            ))
            graph.add_edge(OntologyEdge(type=EdgeType.prevents, source=responsive_id, target=pattern_id))

    if icon_policy:
        icon_policy_id = f"governance:{slugify(icon_policy.get('id', 'emoji-to-svg-refactor'))}"
        graph.add_node(OntologyNode(
            id=icon_policy_id,
            type=NodeType.GovernanceRule,
            label=icon_policy.get("id", "emoji to svg refactor"),
            meta={
                "rule": icon_policy.get("rule", ""),
                "targets": icon_policy.get("targets", []),
                "replacement_order": icon_policy.get("replacement_order", []),
                "quality_floor": icon_policy.get("quality_floor", {}),
                "implementation_rules": icon_policy.get("implementation_rules", []),
                "outputs": icon_policy.get("outputs", []),
            },
        ))
        if graph.get_node(brand_id):
            graph.add_edge(OntologyEdge(type=EdgeType.grounded_in, source=icon_policy_id, target=brand_id))

        for pattern in icon_policy.get("failure_patterns", []):
            pattern_id = f"failure-pattern:{slugify(pattern.get('id', 'emoji-ui-affordance'))}"
            graph.add_node(OntologyNode(
                id=pattern_id,
                type=NodeType.ImplementationFailurePattern,
                label=pattern.get("id", "emoji UI affordance"),
                meta={
                    "trigger": pattern.get("trigger", ""),
                    "rule": pattern.get("rule", ""),
                    "prevention": pattern.get("prevention", ""),
                    "technical_controls": pattern.get("technical_controls", []),
                },
            ))
            graph.add_edge(OntologyEdge(type=EdgeType.prevents, source=icon_policy_id, target=pattern_id))

    if commercial_policy:
        commercial_policy_id = f"governance:{slugify(commercial_policy.get('id', 'commercial-product-realism'))}"
        graph.add_node(OntologyNode(
            id=commercial_policy_id,
            type=NodeType.GovernanceRule,
            label=commercial_policy.get("id", "commercial product realism"),
            meta={
                "rule": commercial_policy.get("rule", ""),
                "applies_to": commercial_policy.get("applies_to", []),
                "diagnosis": commercial_policy.get("diagnosis", []),
                "required_signals": commercial_policy.get("required_signals", []),
                "successful_patterns": commercial_policy.get("successful_patterns", []),
                "implementation_rules": commercial_policy.get("implementation_rules", []),
                "outputs": commercial_policy.get("outputs", []),
            },
        ))
        if graph.get_node(brand_id):
            graph.add_edge(OntologyEdge(type=EdgeType.grounded_in, source=commercial_policy_id, target=brand_id))

        for target_id in (
            "pattern:layout-dashboard-cards",
            "pattern:layout-data-tables",
            "pattern:layout-workspace-navigation",
            "component:table",
            "component:data-table",
            "component:status-badge",
            "component:tabs",
            "component:filter-chip",
        ):
            if graph.get_node(target_id):
                graph.add_edge(OntologyEdge(type=EdgeType.enforces, source=commercial_policy_id, target=target_id))

        for pattern in commercial_policy.get("failure_patterns", []):
            pattern_id = f"failure-pattern:{slugify(pattern.get('id', 'commercial-product-realism-failure'))}"
            graph.add_node(OntologyNode(
                id=pattern_id,
                type=NodeType.ImplementationFailurePattern,
                label=pattern.get("id", "commercial product realism failure"),
                meta={
                    "trigger": pattern.get("trigger", ""),
                    "rule": pattern.get("rule", ""),
                    "prevention": pattern.get("prevention", ""),
                    "technical_controls": pattern.get("technical_controls", []),
                },
            ))
            graph.add_edge(OntologyEdge(type=EdgeType.prevents, source=commercial_policy_id, target=pattern_id))

    if visual_substance_policy:
        visual_policy_id = f"governance:{slugify(visual_substance_policy.get('id', 'mockup-visual-substance'))}"
        graph.add_node(OntologyNode(
            id=visual_policy_id,
            type=NodeType.GovernanceRule,
            label=visual_substance_policy.get("id", "mockup visual substance"),
            meta={
                "rule": visual_substance_policy.get("rule", ""),
                "applies_to": visual_substance_policy.get("applies_to", []),
                "diagnosis": visual_substance_policy.get("diagnosis", []),
                "required_signals": visual_substance_policy.get("required_signals", []),
                "image_acquisition_order": visual_substance_policy.get("image_acquisition_order", []),
                "implementation_rules": visual_substance_policy.get("implementation_rules", []),
                "outputs": visual_substance_policy.get("outputs", []),
            },
        ))
        if graph.get_node(brand_id):
            graph.add_edge(OntologyEdge(type=EdgeType.grounded_in, source=visual_policy_id, target=brand_id))

        for target_id in (
            "governance:generated-visual-asset-contract",
            "governance:sourced-visual-asset-fallback-contract",
            "identity-asset:app-icon",
        ):
            if graph.get_node(target_id):
                graph.add_edge(OntologyEdge(type=EdgeType.enforces, source=visual_policy_id, target=target_id))

        for pattern in visual_substance_policy.get("failure_patterns", []):
            pattern_id = f"failure-pattern:{slugify(pattern.get('id', 'mockup-visual-substance-failure'))}"
            graph.add_node(OntologyNode(
                id=pattern_id,
                type=NodeType.ImplementationFailurePattern,
                label=pattern.get("id", "mockup visual substance failure"),
                meta={
                    "trigger": pattern.get("trigger", ""),
                    "rule": pattern.get("rule", ""),
                    "prevention": pattern.get("prevention", ""),
                    "technical_controls": pattern.get("technical_controls", []),
                },
            ))
            graph.add_edge(OntologyEdge(type=EdgeType.prevents, source=visual_policy_id, target=pattern_id))

    if visual_medium_policy:
        visual_medium_policy_id = f"governance:{slugify(visual_medium_policy.get('id', 'visual-asset-medium-selection'))}"
        graph.add_node(OntologyNode(
            id=visual_medium_policy_id,
            type=NodeType.GovernanceRule,
            label=visual_medium_policy.get("id", "visual asset medium selection"),
            meta={
                "rule": visual_medium_policy.get("rule", ""),
                "directive_overrides": visual_medium_policy.get("directive_overrides", []),
                "decision_sequence": visual_medium_policy.get("decision_sequence", []),
                "slot_families": visual_medium_policy.get("slot_families", []),
                "implementation_rules": visual_medium_policy.get("implementation_rules", []),
                "outputs": visual_medium_policy.get("outputs", []),
            },
        ))
        if graph.get_node(brand_id):
            graph.add_edge(OntologyEdge(type=EdgeType.grounded_in, source=visual_medium_policy_id, target=brand_id))

        for target_id in (
            VISUAL_ASSET_CONTRACT_ID,
            SOURCED_VISUAL_ASSET_CONTRACT_ID,
            "identity-asset:app-icon",
        ):
            if graph.get_node(target_id):
                graph.add_edge(OntologyEdge(type=EdgeType.enforces, source=visual_medium_policy_id, target=target_id))

        for pattern in visual_medium_policy.get("failure_patterns", []):
            pattern_id = f"failure-pattern:{slugify(pattern.get('id', 'visual-asset-medium-failure'))}"
            graph.add_node(OntologyNode(
                id=pattern_id,
                type=NodeType.ImplementationFailurePattern,
                label=pattern.get("id", "visual asset medium failure"),
                meta={
                    "trigger": pattern.get("trigger", ""),
                    "rule": pattern.get("rule", ""),
                    "prevention": pattern.get("prevention", ""),
                    "technical_controls": pattern.get("technical_controls", []),
                },
            ))
            graph.add_edge(OntologyEdge(type=EdgeType.prevents, source=visual_medium_policy_id, target=pattern_id))

    if app_icon_policy:
        app_icon_policy_id = f"governance:{slugify(app_icon_policy.get('id', 'brand-app-icon-identity'))}"
        profile_identity_assets: dict[str, dict] = {}
        for identity_asset in (
            brand_profile.get("_identity_assets", [])
            or brand_profile.get("identity_assets", [])
            or blueprint.get("identity_assets", [])
        ):
            if not isinstance(identity_asset, dict):
                continue
            asset_id = str(identity_asset.get("id") or "")
            if asset_id:
                profile_identity_assets[asset_id] = identity_asset
        graph.add_node(OntologyNode(
            id=app_icon_policy_id,
            type=NodeType.GovernanceRule,
            label=app_icon_policy.get("id", "brand app icon identity"),
            meta={
                "rule": app_icon_policy.get("rule", ""),
                "implementation_rules": app_icon_policy.get("implementation_rules", []),
                "outputs": app_icon_policy.get("outputs", []),
            },
        ))
        if graph.get_node(brand_id):
            graph.add_edge(OntologyEdge(type=EdgeType.grounded_in, source=app_icon_policy_id, target=brand_id))

        required_asset_ids: set[str] = set()
        for asset in app_icon_policy.get("required_assets", []):
            asset_id = asset.get("id") or f"identity-asset:{slugify(asset.get('label', 'app-icon'))}"
            required_asset_ids.add(asset_id)
            project_asset = profile_identity_assets.get(asset_id, {})
            targets = sorted(set((asset.get("targets", []) or []) + (project_asset.get("targets", []) or [])))
            formats = sorted(set((asset.get("formats", []) or []) + ([project_asset.get("format")] if project_asset.get("format") else []) + (project_asset.get("formats", []) or [])))
            graph.add_node(OntologyNode(
                id=asset_id,
                type=NodeType.BrandIdentityAsset,
                label=project_asset.get("label") or asset.get("label", "Brand app icon"),
                meta={
                    "required": bool(asset.get("required", True) or project_asset.get("required", False)),
                    "integrated": bool(project_asset.get("integrated") or project_asset.get("asset_path")),
                    "slot": project_asset.get("slot") or "app-icon",
                    "asset_path": project_asset.get("asset_path"),
                    "manifest_path": project_asset.get("manifest_path"),
                    "favicon_path": project_asset.get("favicon_path"),
                    "formats": formats,
                    "targets": targets,
                    "description": project_asset.get("description") or asset.get("description", ""),
                    "discovered_from": project_asset.get("discovered_from"),
                    "source_policy": app_icon_policy_id,
                },
            ))
            graph.add_edge(OntologyEdge(type=EdgeType.governs, source=app_icon_policy_id, target=asset_id))
            graph.add_edge(OntologyEdge(type=EdgeType.defines, source=app_icon_policy_id, target=asset_id))
            if graph.get_node(brand_id):
                graph.add_edge(OntologyEdge(type=EdgeType.grounded_in, source=asset_id, target=brand_id))
            for target_id in ("component:app-shell", "component:top-navigation", "pattern:layout-app-shell", "pattern:layout-top-navigation"):
                if graph.get_node(target_id):
                    graph.add_edge(OntologyEdge(type=EdgeType.intended_for, source=asset_id, target=target_id))

        for asset_id, project_asset in profile_identity_assets.items():
            if asset_id in required_asset_ids:
                continue
            graph.add_node(OntologyNode(
                id=asset_id,
                type=NodeType.BrandIdentityAsset,
                label=project_asset.get("label", "Brand identity asset"),
                meta={
                    "required": bool(project_asset.get("required", False)),
                    "integrated": bool(project_asset.get("integrated") or project_asset.get("asset_path")),
                    "slot": project_asset.get("slot"),
                    "asset_path": project_asset.get("asset_path"),
                    "manifest_path": project_asset.get("manifest_path"),
                    "favicon_path": project_asset.get("favicon_path"),
                    "formats": project_asset.get("formats", []) or ([project_asset.get("format")] if project_asset.get("format") else []),
                    "targets": project_asset.get("targets", []),
                    "description": project_asset.get("description", ""),
                    "discovered_from": project_asset.get("discovered_from"),
                    "source_policy": app_icon_policy_id,
                },
            ))
            graph.add_edge(OntologyEdge(type=EdgeType.governs, source=app_icon_policy_id, target=asset_id))
            if graph.get_node(brand_id):
                graph.add_edge(OntologyEdge(type=EdgeType.grounded_in, source=asset_id, target=brand_id))

        for pattern in app_icon_policy.get("failure_patterns", []):
            pattern_id = f"failure-pattern:{slugify(pattern.get('id', 'generic-initials-app-icon'))}"
            graph.add_node(OntologyNode(
                id=pattern_id,
                type=NodeType.ImplementationFailurePattern,
                label=pattern.get("id", "generic initials app icon"),
                meta={
                    "trigger": pattern.get("trigger", ""),
                    "rule": pattern.get("rule", ""),
                    "prevention": pattern.get("prevention", ""),
                    "technical_controls": pattern.get("technical_controls", []),
                },
            ))
            graph.add_edge(OntologyEdge(type=EdgeType.prevents, source=app_icon_policy_id, target=pattern_id))


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
    build_pattern_layer(graph, component_inventory, brand_profile)
    build_component_token_layer(graph, component_inventory, brand_profile)
    build_contrast_audit_layer(graph, brand_profile)
    build_accessibility_layer(graph, component_inventory)
    build_benchmark_layer(graph, brand_profile)
    build_governance_layer(graph, brand_profile, blueprint)
    build_reference_context_layer(graph, brand_profile, blueprint)
    build_generated_visual_asset_layer(graph, brand_profile, blueprint, component_inventory)

    return graph
