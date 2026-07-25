from pathlib import Path

from design_ontology_harness.authoring import build_system_spec_markdown, build_token_schema
from design_ontology_harness.color_reference import (
    resolve_color_reference,
    resolve_semantic_color_reference,
)
from design_ontology_harness.graph_builders import build_full_ontology_graph
from design_ontology_harness.graph_schema import EdgeType, NodeType
from design_ontology_harness.semantic_color_ontology import load_semantic_color_ontology
from design_ontology_harness.semantic_color_selector import build_semantic_color_selection

REPO_ROOT = Path(__file__).resolve().parents[1]


def _resolved_reference() -> dict:
    resolved, issues = resolve_color_reference(
        {
            "path": "docs/color-reference.md",
            "palette_roles": {
                "primary": "Navy Blue",
                "accent": "Arcadia",
                "surface_tint": "Celadon",
            },
            "palette_strategy": {
                "temperature": "neutral",
                "contrast": "balanced",
                "prefer_moods": ["신뢰", "고요"],
            },
        },
        REPO_ROOT,
        {
            "brand_name": "Care Console",
            "brand_keywords": ["calm", "trustworthy", "precise"],
            "visual_keywords": ["stable green UI surface", "quiet panels"],
            "product_primitives": ["dashboard cards", "service UI"],
        },
    )
    assert resolved is not None
    assert not [issue for issue in issues if "entry not found" in issue]
    return resolved


def test_semantic_color_ontology_export_is_packaged():
    ontology = load_semantic_color_ontology()

    assert ontology["schema_version"] == "design-ontology-harness/semantic-color-ontology-compact-v1"
    assert ontology["node_count"] >= 137
    assert ontology["edge_count"] >= 487
    assert any(
        node["id"] == "color-keyword-navy-blue"
        and node["properties"]["rgb_hex"] == "#000080"
        for node in ontology["nodes"]
    )


def test_packaged_semantic_color_data_has_no_local_dependency():
    resource = REPO_ROOT / "design_ontology_harness/resources/semantic_color_ontology.json"
    text = resource.read_text(encoding="utf-8")

    assert "/Users/" not in text
    assert "source_path" not in text
    assert "domains/color/ontology/build/graph.json" in text


def test_resolved_color_reference_includes_semantic_context():
    resolved = _resolved_reference()
    semantic = resolved["semantic_ontology"]

    matched = {item["name"]: item for item in semantic["matched_keywords"]}
    assert matched["Navy Blue"]["spectrum"] == "blue"
    assert "low_value" in matched["Navy Blue"]["tone_axes"]
    assert matched["Celadon"]["family"] == "pastel"
    assert any(item["id"] == "guideline-no-palette-table-reconstruction" for item in semantic["guidelines"])
    assert any(item["id"] == "pattern-palette-by-role-and-contrast-not-table-row" for item in semantic["patterns"])
    assert semantic["recommended_keywords"]


def test_semantic_color_selection_searches_ontology_for_app_brief():
    selection = build_semantic_color_selection(
        brand_profile={
            "brand_name": "Koma Weekly",
            "system_name": "Koma Weekly System",
            "product_summary": "A manga magazine site for weekly issue drops, covers, creator notes, and serial navigation.",
            "brand_keywords": ["editorial", "bold", "playful"],
            "visual_keywords": ["manga magazine", "pop editorial", "issue rhythm"],
            "interaction_keywords": ["fast scanning", "chapter navigation"],
            "product_primitives": ["magazine issue cards", "cover grid", "series navigation"],
            "_spec_components": [
                {"name": "issue-card", "family": "editorial", "role": "cover browsing"},
                {"name": "chapter-row", "family": "navigation", "role": "serial navigation"},
            ],
        },
        strategy={"candidate_count": 3},
    )

    assert selection["selection_method"] == "semantic-os-markdown-search-per-run"
    assert selection["source"]["authority"] == "semantic-os-synced-markdown"
    assert selection["matched_pattern"]["id"] == "pattern-brief-palette-manga-magazine-pop-editorial"
    assert len(selection["candidate_palettes"]) >= 5
    active_roles = selection["active_palette"]["roles"]
    assert len(active_roles) == 5
    assert "masthead_energy" in active_roles
    assert all(item["hex"].startswith("#") for item in active_roles.values())
    assert any("Do not ship pre-authored palette sets" in rule for rule in selection["rules"])


def test_semantic_color_reference_can_run_without_manual_color_file():
    resolved = resolve_semantic_color_reference(
        {
            "brand_name": "Surface Ledger",
            "system_name": "Surface Ledger System",
            "product_summary": "A stable green service operations UI with queues, tables, and review states.",
            "brand_keywords": ["trustworthy", "calm", "precise"],
            "visual_keywords": ["stable green UI surface", "quiet panels"],
            "product_primitives": ["dashboard cards", "data tables", "service UI"],
        },
        {"palette_strategy": {"candidate_count": 2}},
    )

    assert resolved["selection_mode"] == "semantic-os-markdown"
    assert resolved["source_path"].endswith("docs/color-reference.md")
    assert (
        resolved["semantic_color_selection"]["selection_method"]
        == "semantic-os-markdown-search-per-run"
    )
    assert len(resolved["semantic_color_selection"]["candidate_palettes"]) >= 5
    assert len(resolved["palette_roles"]) == 5
    assert resolved["active_palette"]["candidate_id"].startswith("ontology-")


def test_token_schema_and_spec_surface_semantic_color_ontology():
    profile = {
        "brand_name": "Care Console",
        "system_name": "Care Console System",
        "_resolved_color_reference": _resolved_reference(),
    }
    token_schema = build_token_schema(profile, {"system_name": "Care Console System"})
    semantic = token_schema["categories"]["color"]["reference_palette"]["semantic_ontology"]
    selection = token_schema["categories"]["color"]["reference_palette"]["semantic_color_selection"]

    assert semantic["node_count"] >= 137
    assert any(item["name"] == "Navy Blue" for item in semantic["matched_keywords"])
    assert any("palette tables" in rule for rule in semantic["rules"])
    assert selection["selection_method"] == "semantic-os-markdown-search-per-run"
    assert len(selection["candidate_palettes"]) >= 5

    spec = build_system_spec_markdown(
        brand_profile=profile,
        blueprint={"system_name": "Care Console System", "principles": [], "governance": {}},
        validation={"errors": [], "warnings": []},
        foundations=[],
        token_schema=token_schema,
        component_inventory={"families": [], "candidate_component_archetypes": []},
        documents=[],
    )
    assert "Semantic color ontology" in spec
    assert "Semantic color selection" in spec
    assert "Navy Blue" in spec
    assert "배색표를 재구성할 수 있는 수준" in spec


def test_graph_promotes_semantic_color_ontology_nodes():
    profile = {
        "brand_name": "Care Console",
        "_resolved_color_reference": _resolved_reference(),
    }
    graph = build_full_ontology_graph(
        brand_profile=profile,
        blueprint={"principles": []},
        component_inventory={"families": [], "components": []},
        token_schema={"categories": {}},
    )

    source = graph.get_node("source:semantic-color-ontology")
    assert source is not None
    assert source.type == NodeType.SourceReference
    assert source.meta["node_count"] >= 137

    navy = graph.get_node("semantic-color:navy-blue")
    assert navy is not None
    assert navy.type == NodeType.ColorToken
    assert navy.meta["semantic_node_id"] == "color-keyword-navy-blue"
    assert "전문성" in navy.meta["mood_tags"]

    guideline = graph.get_node(
        "governance:semantic-color-guideline-no-palette-table-reconstruction"
    )
    assert guideline is not None
    assert guideline.type == NodeType.GovernanceRule

    governed = {edge.target for edge in graph.get_edges_from(guideline.id, EdgeType.governs)}
    assert "semantic-color:navy-blue" in governed
