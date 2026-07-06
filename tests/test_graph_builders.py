from design_ontology_harness.graph_builders import build_component_token_layer
from design_ontology_harness.graph_schema import DesignOntologyGraph, EdgeType, NodeType, OntologyNode


def _add_token_nodes(graph: DesignOntologyGraph) -> None:
    for node_id, label in [
        ("color:navy-blue", "Navy Blue"),
        ("color:ochre", "Ochre"),
        ("color:sky-blue", "Sky Blue"),
        ("spacing:8", "8"),
        ("spacing:12", "12"),
        ("radius:none", "none"),
        ("radius:md", "md"),
        ("font:inter", "Inter"),
    ]:
        if node_id.startswith("color:"):
            node_type = NodeType.ColorToken
        elif node_id.startswith("spacing:"):
            node_type = NodeType.SpacingToken
        elif node_id.startswith("radius:"):
            node_type = NodeType.RadiusToken
        else:
            node_type = NodeType.FontFamily
        graph.add_node(OntologyNode(id=node_id, type=node_type, label=label))


def _add_component_nodes(graph: DesignOntologyGraph, names: list[str]) -> None:
    for name in names:
        graph.add_node(OntologyNode(id=f"component:{name}", type=NodeType.Component, label=name))


def _targets(graph: DesignOntologyGraph, component_name: str) -> set[str]:
    return {
        edge.target
        for edge in graph.get_edges_from(f"component:{component_name}", EdgeType.uses_token)
    }


def test_component_token_layer_distinguishes_cards_from_operational_surfaces() -> None:
    graph = DesignOntologyGraph()
    _add_token_nodes(graph)
    _add_component_nodes(
        graph,
        ["data-table", "metric-strip", "policy-matrix", "diff-viewer", "stat-card", "primary-button"],
    )

    brand_profile = {
        "_resolved_color_reference": {
            "palette_roles": {
                "primary": {"name": "Navy Blue"},
                "accent": {"name": "Ochre"},
                "surface_tint": {"name": "Sky Blue"},
            }
        },
        "_resolved_font_system": {"body": {"name": "Inter"}},
    }
    component_inventory = {
        "components": [
            {"name": "data-table", "family": "data-display"},
            {"name": "metric-strip", "family": "data-display"},
            {"name": "policy-matrix", "family": "data-display"},
            {"name": "diff-viewer", "family": "document"},
            {"name": "stat-card", "family": "data-display"},
            {"name": "primary-button", "family": "button"},
        ]
    }

    build_component_token_layer(graph, component_inventory, brand_profile)

    assert "color:sky-blue" not in _targets(graph, "data-table")
    assert "spacing:8" in _targets(graph, "data-table")
    assert "radius:none" in _targets(graph, "data-table")

    assert "color:sky-blue" not in _targets(graph, "metric-strip")
    assert "spacing:8" in _targets(graph, "metric-strip")
    assert "radius:none" in _targets(graph, "metric-strip")

    assert "color:sky-blue" not in _targets(graph, "policy-matrix")
    assert "spacing:8" in _targets(graph, "policy-matrix")
    assert "radius:none" in _targets(graph, "policy-matrix")

    assert "color:sky-blue" not in _targets(graph, "diff-viewer")
    assert "spacing:8" in _targets(graph, "diff-viewer")
    assert "radius:none" in _targets(graph, "diff-viewer")

    assert "color:sky-blue" in _targets(graph, "stat-card")
    assert "spacing:12" in _targets(graph, "stat-card")
    assert "radius:md" in _targets(graph, "stat-card")

    assert "color:navy-blue" in _targets(graph, "primary-button")
    assert "color:ochre" in _targets(graph, "primary-button")
    assert "color:sky-blue" not in _targets(graph, "primary-button")
