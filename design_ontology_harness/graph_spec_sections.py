"""Generate system_spec.md sections 18-20 from the ontology graph."""

from __future__ import annotations

from .graph_schema import DesignOntologyGraph, EdgeType, NodeType


_TOKEN_CATEGORY_LABEL = {
    NodeType.ColorToken: "color",
    NodeType.SpacingToken: "spacing",
    NodeType.RadiusToken: "radius",
    NodeType.MotionToken: "motion",
    NodeType.ElevationToken: "elevation",
    NodeType.FontFamily: "font",
}


def _token_pretty(category: str, label: str, slot: str | None) -> str:
    prefix = f"{category}.{label}" if category != "font" else f"font:{label}"
    return f"{prefix}→{slot}" if slot else prefix


def build_component_token_map_section(graph: DesignOntologyGraph) -> str:
    components = graph.get_nodes_by_type(NodeType.Component)
    if not components:
        return "No component-token mappings available."

    rows: list[str] = []
    rows.append("| Component | Tokens Used |")
    rows.append("|-----------|-------------|")

    for comp in sorted(components, key=lambda n: n.label):
        token_edges = list(graph.get_edges_from(comp.id, EdgeType.uses_token))
        token_edges += list(graph.get_edges_from(comp.id, EdgeType.uses_font))
        if not token_edges:
            continue

        token_labels: list[str] = []
        for edge in token_edges:
            node = graph.get_node(edge.target)
            if not node:
                continue
            category = _TOKEN_CATEGORY_LABEL.get(node.type, node.type.value.lower())
            slot = (edge.meta or {}).get("slot")
            token_labels.append(f"`{_token_pretty(category, node.label, slot)}`")

        if token_labels:
            rows.append(f"| {comp.label} | {', '.join(token_labels[:8])} |")

    if len(rows) <= 2:
        return "No component-token mappings emitted. Check build_component_token_layer."

    return "\n".join(rows)


def build_contrast_audit_section(graph: DesignOntologyGraph) -> str:
    contrast_edges = [e for e in graph.edges if e.type == EdgeType.contrast_pair]
    if not contrast_edges:
        return "No contrast pairs defined. Add `contrast_surfaces` to color_reference or verify palette_roles."

    rows: list[str] = []
    rows.append("| Background | Foreground | Ratio | Level |")
    rows.append("|------------|------------|-------|-------|")

    for edge in sorted(contrast_edges, key=lambda e: e.meta.get("ratio", 0), reverse=True):
        bg = graph.get_node(edge.source)
        fg = graph.get_node(edge.target)
        if not bg or not fg:
            continue
        ratio = edge.meta.get("ratio", 0)
        level = edge.meta.get("level", "fail")
        status = "pass" if level in ("AA", "AAA") else "large-only" if level == "AA-large" else "FAIL"
        rows.append(f"| {bg.label} | {fg.label} | {ratio:.2f}:1 | {level} ({status}) |")

    return "\n".join(rows)


def build_pattern_catalog_section(graph: DesignOntologyGraph) -> str:
    layout_patterns = graph.get_nodes_by_type(NodeType.LayoutPattern)
    interaction_patterns = graph.get_nodes_by_type(NodeType.InteractionPattern)

    if not layout_patterns and not interaction_patterns:
        return "No patterns cataloged."

    lines: list[str] = []

    if layout_patterns:
        lines.append("### Layout Patterns")
        lines.append("")
        for pattern in layout_patterns:
            comp_edges = graph.get_edges_from(pattern.id, EdgeType.composed_of)
            comp_names = []
            for edge in comp_edges:
                node = graph.get_node(edge.target)
                if node:
                    comp_names.append(node.label)
            comp_str = ", ".join(comp_names) if comp_names else "—"
            lines.append(f"- **{pattern.label}**: {comp_str}")

    if interaction_patterns:
        lines.append("")
        lines.append("### Interaction Patterns")
        lines.append("")
        for pattern in interaction_patterns:
            comp_edges = graph.get_edges_from(pattern.id, EdgeType.composed_of)
            comp_names = []
            for edge in comp_edges:
                node = graph.get_node(edge.target)
                if node:
                    comp_names.append(node.label)
            comp_str = ", ".join(comp_names) if comp_names else "—"
            lines.append(f"- **{pattern.label}**: {comp_str}")

    return "\n".join(lines)


def build_generated_visual_asset_section(graph: DesignOntologyGraph) -> str:
    assets = graph.get_nodes_by_type(NodeType.GeneratedVisualAsset)
    if not assets:
        return "No generated visual asset slots defined."

    rows: list[str] = []
    rows.append("| Asset Slot | Model | Intended For | Manifest |")
    rows.append("|------------|-------|--------------|----------|")

    for asset in sorted(assets, key=lambda n: n.label):
        model = "—"
        for edge in graph.get_edges_from(asset.id, EdgeType.generated_with):
            node = graph.get_node(edge.target)
            if node:
                model = node.label
                break

        targets: list[str] = []
        for edge in graph.get_edges_from(asset.id, EdgeType.intended_for):
            node = graph.get_node(edge.target)
            if node:
                targets.append(node.label)

        manifest = asset.meta.get("manifest_path", "—")
        intended_for = ", ".join(targets[:6]) if targets else asset.meta.get("activation", "optional")
        rows.append(f"| {asset.label} | {model} | {intended_for} | `{manifest}` |")

    return "\n".join(rows)


def build_graph_spec_sections(graph: DesignOntologyGraph) -> str:
    return f"""## 18. Component-Token Map

{build_component_token_map_section(graph)}

## 19. Contrast Audit

{build_contrast_audit_section(graph)}

## 20. Pattern Catalog

{build_pattern_catalog_section(graph)}

## 21. Generated Visual Asset Plan

{build_generated_visual_asset_section(graph)}
"""
