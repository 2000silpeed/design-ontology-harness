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

    _build_contrast_pairs(graph, color_ref)


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

VISUAL_ASSET_SLOT_RULES = [
    {
        "slot": "brand-aligned-raster",
        "label": "Brand-aligned raster image",
        "keywords": (),
        "family_keywords": (),
        "aspect_ratios": ["16:9", "4:3", "1:1"],
        "usage": "Optional Codex imagery when a screen needs professional raster substance.",
        "activation": "only when the implementation surface would benefit from generated imagery",
    },
    {
        "slot": "hero-image",
        "label": "Hero image",
        "keywords": ("hero", "landing", "spotlight", "masthead", "feature"),
        "family_keywords": ("marketing",),
        "aspect_ratios": ["16:9", "3:2"],
        "usage": "First-viewport visual signal for landing, product, or editorial hero sections.",
        "activation": "hero, landing, product, or editorial first screen",
    },
    {
        "slot": "card-thumbnail",
        "label": "Card thumbnail",
        "keywords": ("card", "thumbnail", "media", "product", "gallery", "case-study"),
        "family_keywords": ("marketing", "data-display", "editorial"),
        "aspect_ratios": ["4:3", "1:1"],
        "usage": "Content image for product, venue, object, media, or feature cards.",
        "activation": "card grids or repeated content surfaces need real visual content",
    },
    {
        "slot": "editorial-cover",
        "label": "Editorial cover",
        "keywords": ("editorial", "article", "cover", "story", "case-study", "press"),
        "family_keywords": ("editorial", "marketing"),
        "aspect_ratios": ["4:5", "3:4"],
        "usage": "Cover image for articles, case studies, press stories, or narrative modules.",
        "activation": "editorial or story-led content module",
    },
    {
        "slot": "empty-state-illustration",
        "label": "Empty-state illustration",
        "keywords": ("empty-state", "onboarding", "welcome", "blank", "no-results"),
        "family_keywords": ("feedback",),
        "aspect_ratios": ["4:3", "1:1"],
        "usage": "Supportive illustration for empty states, onboarding, or no-result panels.",
        "activation": "empty state benefits from clarification without replacing text",
    },
]


def build_generated_visual_asset_layer(
    graph: DesignOntologyGraph,
    brand_profile: dict,
    blueprint: dict,
    component_inventory: dict,
) -> None:
    """Represent Codex/imagine2 visual generation as ontology nodes and edges."""
    brand_name = brand_profile.get("brand_name", "Brand")
    brand_id = f"brand:{slugify(brand_name)}"
    model_id = "image-model:imagine2"

    graph.add_node(OntologyNode(
        id=model_id,
        type=NodeType.ImageGenerationModel,
        label="imagine2",
        meta={
            "runtime": "Codex image generation",
            "selection_rule": "Use when Codex exposes image-generation tooling or a model selector.",
        },
    ))

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
                "model": "imagine2",
                "candidate_count": "2-4",
                "manifest_path": VISUAL_ASSET_MANIFEST_PATH,
                "prompt_basis": prompt_basis,
                "aspect_ratios": rule["aspect_ratios"],
                "usage": rule["usage"],
                "activation": rule["activation"],
                "alt_text_required": True,
                "status": "promptable",
            },
        ))
        graph.add_edge(OntologyEdge(type=EdgeType.generated_with, source=asset_id, target=model_id))
        if graph.get_node(brand_id):
            graph.add_edge(OntologyEdge(type=EdgeType.grounded_in, source=asset_id, target=brand_id))

        for principle in blueprint.get("principles", []):
            principle_id = f"principle:{slugify(principle['keyword'])}"
            if graph.get_node(principle_id):
                graph.add_edge(OntologyEdge(type=EdgeType.constrains, source=principle_id, target=asset_id))

        for target_id in targets:
            if graph.get_node(target_id):
                graph.add_edge(OntologyEdge(type=EdgeType.intended_for, source=asset_id, target=target_id))


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
    build_generated_visual_asset_layer(graph, brand_profile, blueprint, component_inventory)

    return graph
