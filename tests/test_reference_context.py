from __future__ import annotations

from design_ontology_harness.graph_builders import build_full_ontology_graph
from design_ontology_harness.graph_schema import EdgeType, NodeType
from design_ontology_harness.graph_spec_sections import build_graph_spec_sections
from design_ontology_harness.reference_context import build_design_context_pack


def test_design_context_pack_normalizes_lazyweb_and_local_screens() -> None:
    brand_profile = {
        "brand_name": "Mercer",
        "product_primitives": ["chat and messaging", "data tables"],
        "visual_reference": {
            "mode": "local-images",
            "reference_providers": [
                {"provider_id": "lazyweb", "enabled": True, "access_mode": "mcp"},
            ],
        },
    }
    visual_reference = {
        "mode": "local-images",
        "query": ["enterprise chat sources drawer", "policy audit table"],
        "coverage": {"image_count": 1},
        "selected_images": [
            {
                "image_id": "source-01-image-01",
                "label": "chat policy table",
                "relative_path": "references/chat-policy-table.png",
                "orientation": "landscape",
                "aspect_ratio_bucket": "16:9-ish",
                "mime_type": "image/png",
                "signal_terms": ["chat", "policy", "table", "citation", "sidebar"],
                "tags": ["enterprise"],
            }
        ],
    }

    pack = build_design_context_pack(brand_profile, visual_reference)

    assert pack["schema_version"] == "design-context-pack/v1"
    assert pack["activation_state"] == "grounded"
    providers = {item["provider_id"]: item for item in pack["providers"]}
    assert providers["lazyweb"]["status"] == "suggested"
    assert providers["lazyweb"]["access_mode"] == "mcp"
    assert "color palette" in providers["lazyweb"]["denied_outputs"]
    assert providers["local-images"]["status"] == "active"

    card = pack["context_cards"][0]
    assert card["provider_id"] == "local-images"
    assert "messaging" in card["flows"]
    assert "dense-table" in card["morphology"]
    assert "color palette" in card["must_not_absorb"]


def test_design_context_pack_promotes_lazyweb_source_urls_to_observed_context() -> None:
    pack = build_design_context_pack(
        {
            "brand_name": "Mercer",
            "product_primitives": ["policy-check badge", "audit-trail timeline"],
            "visual_reference": {
                "reference_providers": [
                    {"provider_id": "lazyweb", "status": "active", "access_mode": "mcp"},
                ],
                "sources": [
                    {
                        "kind": "lazyweb",
                        "label": "Remote contractor compliance dashboard",
                        "url": "https://remote.com/global-hr/contractor-of-record?token=temporary",
                        "tags": ["compliance", "dashboard", "approval", "card"],
                    }
                ],
            },
        },
        {
            "sources": [
                {
                    "source_id": "source-01",
                    "kind": "lazyweb",
                    "label": "Remote contractor compliance dashboard",
                    "status": "unsupported-url",
                    "url": "https://remote.com/global-hr/contractor-of-record?token=temporary",
                    "tags": ["compliance", "dashboard", "approval", "card"],
                    "visionDescription": "Compliance dashboard with overview cards, approvals, and contractor lists.",
                }
            ],
        },
    )

    providers = {item["provider_id"]: item for item in pack["providers"]}
    assert providers["lazyweb"]["status"] == "active"
    assert pack["activation_state"] == "grounded"

    card = pack["context_cards"][0]
    assert card["kind"] == "external-reference"
    assert card["provider_id"] == "lazyweb"
    assert card["provenance_level"] == "observed"
    assert card["source_url"] == "https://remote.com/global-hr/contractor-of-record"
    assert "token=" not in card["source_url"]
    assert "dashboard" in card["flows"]
    assert "card-stack" in card["morphology"]
    assert "color palette" in card["must_not_absorb"]


def test_design_context_pack_is_modeled_in_ontology_and_spec_sections() -> None:
    pack = build_design_context_pack(
        {
            "brand_name": "Mercer",
            "product_primitives": ["chat and messaging"],
            "visual_reference": {"reference_providers": ["lazyweb"]},
        },
        {
            "query": ["chatgpt enterprise message thread"],
            "coverage": {"image_count": 0},
            "selected_images": [],
        },
    )

    graph = build_full_ontology_graph(
        brand_profile={"brand_name": "Mercer"},
        blueprint={"principles": [], "design_context_pack": pack},
        component_inventory={"families": [], "components": []},
        token_schema={"categories": {}},
    )

    provider = graph.get_node("reference-provider:lazyweb")
    assert provider is not None
    assert provider.type == NodeType.ReferenceProvider

    pack_node = graph.get_node("design-context-pack:default")
    assert pack_node is not None
    assert pack_node.type == NodeType.DesignContextPack

    cards = graph.get_nodes_by_type(NodeType.DesignContextCard)
    assert cards

    provider_edges = graph.get_edges_from("design-context-pack:default", EdgeType.provided_by)
    assert "reference-provider:lazyweb" in {edge.target for edge in provider_edges}

    sections = build_graph_spec_sections(graph)
    assert "Reference Intelligence Pack" in sections
    assert "Lazyweb MCP real-app corpus" in sections
