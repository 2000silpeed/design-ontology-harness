"""Design Ontology Graph Schema — 22 node types, 27 edge types.

Defines the typed graph structure for representing design system relationships.
Replaces the flat keyword-matching approach in ontology.py with a true
relational graph where colors, typography, components, and patterns connect.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any


class NodeType(str, Enum):
    Brand = "Brand"
    Principle = "Principle"
    ColorPalette = "ColorPalette"
    ColorToken = "ColorToken"
    ColorMode = "ColorMode"
    FontFamily = "FontFamily"
    TypeScaleEntry = "TypeScaleEntry"
    SpacingToken = "SpacingToken"
    RadiusToken = "RadiusToken"
    MotionToken = "MotionToken"
    ElevationToken = "ElevationToken"
    ComponentFamily = "ComponentFamily"
    Component = "Component"
    ComponentState = "ComponentState"
    LayoutPattern = "LayoutPattern"
    InteractionPattern = "InteractionPattern"
    AccessibilityRule = "AccessibilityRule"
    ProductPrimitive = "ProductPrimitive"
    SourceReference = "SourceReference"
    BenchmarkSystem = "BenchmarkSystem"
    GeneratedVisualAsset = "GeneratedVisualAsset"
    ImageGenerationModel = "ImageGenerationModel"
    GovernanceRule = "GovernanceRule"
    ImplementationFailurePattern = "ImplementationFailurePattern"


class EdgeType(str, Enum):
    expresses = "expresses"
    constrains = "constrains"
    belongs_to_palette = "belongs_to_palette"
    derived_from = "derived_from"
    overrides_in_mode = "overrides_in_mode"
    contrast_pair = "contrast_pair"
    pairs_with = "pairs_with"
    uses_font = "uses_font"
    member_of_family = "member_of_family"
    has_state = "has_state"
    uses_token = "uses_token"
    state_modifies_token = "state_modifies_token"
    uses_type_scale = "uses_type_scale"
    supports = "supports"
    implements = "implements"
    composed_of = "composed_of"
    requires = "requires"
    inspired_by = "inspired_by"
    similar_to = "similar_to"
    references_font = "references_font"
    governs = "governs"
    defines = "defines"
    applies_to = "applies_to"
    maps_to_tier = "maps_to_tier"
    generated_with = "generated_with"
    grounded_in = "grounded_in"
    intended_for = "intended_for"
    enforces = "enforces"
    prevents = "prevents"


@dataclass(slots=True)
class OntologyNode:
    id: str
    type: NodeType
    label: str
    meta: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        d = {"id": self.id, "type": self.type.value, "label": self.label}
        if self.meta:
            d["meta"] = self.meta
        return d


@dataclass(slots=True)
class OntologyEdge:
    type: EdgeType
    source: str
    target: str
    meta: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        d = {"type": self.type.value, "source": self.source, "target": self.target}
        if self.meta:
            d["meta"] = self.meta
        return d


@dataclass
class DesignOntologyGraph:
    nodes: list[OntologyNode] = field(default_factory=list)
    edges: list[OntologyEdge] = field(default_factory=list)

    _node_index: dict[str, OntologyNode] = field(default_factory=dict, repr=False)
    _type_index: dict[NodeType, list[OntologyNode]] = field(default_factory=dict, repr=False)
    _edges_from: dict[str, list[OntologyEdge]] = field(default_factory=dict, repr=False)
    _edges_to: dict[str, list[OntologyEdge]] = field(default_factory=dict, repr=False)

    def add_node(self, node: OntologyNode) -> None:
        if node.id in self._node_index:
            return
        self.nodes.append(node)
        self._node_index[node.id] = node
        self._type_index.setdefault(node.type, []).append(node)

    def add_edge(self, edge: OntologyEdge) -> None:
        self.edges.append(edge)
        self._edges_from.setdefault(edge.source, []).append(edge)
        self._edges_to.setdefault(edge.target, []).append(edge)

    def get_node(self, node_id: str) -> OntologyNode | None:
        return self._node_index.get(node_id)

    def get_nodes_by_type(self, node_type: NodeType) -> list[OntologyNode]:
        return self._type_index.get(node_type, [])

    def get_edges_from(self, node_id: str, edge_type: EdgeType | None = None) -> list[OntologyEdge]:
        edges = self._edges_from.get(node_id, [])
        if edge_type is not None:
            return [e for e in edges if e.type == edge_type]
        return edges

    def get_edges_to(self, node_id: str, edge_type: EdgeType | None = None) -> list[OntologyEdge]:
        edges = self._edges_to.get(node_id, [])
        if edge_type is not None:
            return [e for e in edges if e.type == edge_type]
        return edges

    def get_neighbors(self, node_id: str, edge_type: EdgeType | None = None) -> list[OntologyNode]:
        targets = [e.target for e in self.get_edges_from(node_id, edge_type)]
        sources = [e.source for e in self.get_edges_to(node_id, edge_type)]
        neighbor_ids = set(targets + sources) - {node_id}
        return [self._node_index[nid] for nid in neighbor_ids if nid in self._node_index]

    def to_dict(self) -> dict[str, Any]:
        return {
            "node_types": [t.value for t in NodeType],
            "edge_types": [t.value for t in EdgeType],
            "nodes": [n.to_dict() for n in self.nodes],
            "edges": [e.to_dict() for e in self.edges],
            "stats": {
                "node_count": len(self.nodes),
                "edge_count": len(self.edges),
                "nodes_by_type": {
                    t.value: len(nodes) for t, nodes in self._type_index.items()
                },
            },
        }
