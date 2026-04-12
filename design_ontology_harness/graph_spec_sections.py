"""Generate system_spec.md sections 17-19 from the ontology graph."""

from __future__ import annotations

from .graph_schema import DesignOntologyGraph, EdgeType, NodeType


def build_component_token_map_section(graph: DesignOntologyGraph) -> str:
    components = graph.get_nodes_by_type(NodeType.Component)
    if not components:
        return "No component-token mappings available."

    rows: list[str] = []
    rows.append("| Component | Tokens Used |")
    rows.append("|-----------|-------------|")

    for comp in sorted(components, key=lambda n: n.label):
        token_edges = graph.get_edges_from(comp.id, EdgeType.uses_token)
        if not token_edges:
            continue
        token_labels = []
        for edge in token_edges:
            node = graph.get_node(edge.target)
            if node:
                token_labels.append(f"`{node.label}`")
        if token_labels:
            rows.append(f"| {comp.label} | {', '.join(token_labels[:8])} |")

    if len(rows) <= 2:
        return "No component-token mappings found. Run with CSS extraction for token resolution."

    return "\n".join(rows)


def build_contrast_audit_section(graph: DesignOntologyGraph) -> str:
    contrast_edges = [e for e in graph.edges if e.type == EdgeType.contrast_pair]
    if not contrast_edges:
        return "No contrast pairs defined. Add `contrast_surfaces` to color_reference for audit."

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
        emoji = "pass" if level in ("AA", "AAA") else "FAIL"
        rows.append(f"| {bg.label} | {fg.label} | {ratio:.1f}:1 | {level} ({emoji}) |")

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


def build_graph_spec_sections(graph: DesignOntologyGraph) -> str:
    return f"""## 17. Component-Token Map

{build_component_token_map_section(graph)}

## 18. Contrast Audit

{build_contrast_audit_section(graph)}

## 19. Pattern Catalog

{build_pattern_catalog_section(graph)}
"""
