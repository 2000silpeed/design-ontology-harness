from pathlib import Path

from design_ontology_harness.component_specs import generate_component_specs
from design_ontology_harness.reference_context import build_design_context_pack
from design_ontology_harness.website_inspection import build_design_context_source


def _sample_report() -> dict:
    return {
        "schema_version": "website-reference-inspection/v1",
        "label": "Operations Console",
        "title": "Operations Console",
        "url": "https://example.com/app",
        "final_url": "https://example.com/app",
        "screenshots": [
            {"viewport": "desktop", "width": 1440, "height": 1200, "path": "screenshots/desktop.png"},
            {"viewport": "mobile", "width": 390, "height": 844, "path": "screenshots/mobile.png"},
        ],
        "topology": [
            {
                "index": 1,
                "selector": "header",
                "role": "navigation",
                "label": "Workspace navigation",
                "interaction_model": "scroll-aware",
                "layout_hint": "fixed-layer",
            },
            {
                "index": 2,
                "selector": "main > section",
                "role": "section",
                "label": "Dashboard table and metric cards",
                "interaction_model": "click-or-input",
                "layout_hint": "grid:repeat(3, 1fr)",
            },
        ],
        "behavior_summary": {
            "interaction_models": ["scroll-aware", "click-or-input"],
            "asset_counts": {"images": 2, "videos": 0, "background_images": 1, "inline_svgs": 6},
        },
        "absorption_policy": {
            "denied": ["color palette", "typography scale", "product copy"],
        },
    }


def test_website_inspection_source_flows_into_design_context_pack(tmp_path: Path) -> None:
    source = build_design_context_source(_sample_report(), tmp_path)
    pack = build_design_context_pack(
        {
            "brand_name": "OpsDesk",
            "product_primitives": ["dashboard table", "workspace navigation"],
            "visual_reference": {"sources": [source]},
        },
        {"mode": "website-inspection", "sources": [source]},
    )

    providers = {item["provider_id"]: item for item in pack["providers"]}
    assert providers["website-inspection"]["status"] == "active"
    assert providers["website-inspection"]["access_mode"] == "playwright-capture"
    assert "color palette" in providers["website-inspection"]["denied_outputs"]
    assert pack["activation_state"] == "grounded"

    card = pack["context_cards"][0]
    assert card["provider_id"] == "website-inspection"
    assert card["provenance_level"] == "observed"
    assert "dashboard" in card["flows"]
    assert any(trait.startswith("sections=") for trait in card["absorbed_traits"])
    assert any(trait.startswith("interaction=") for trait in card["absorbed_traits"])


def test_component_specs_include_observed_website_reference_evidence(tmp_path: Path) -> None:
    source = build_design_context_source(_sample_report(), tmp_path)
    pack = build_design_context_pack(
        {
            "brand_name": "OpsDesk",
            "product_primitives": ["dashboard table", "workspace navigation"],
            "visual_reference": {"sources": [source]},
        },
        {"mode": "website-inspection", "sources": [source]},
    )

    specs = generate_component_specs(
        brand_profile={"brand_name": "OpsDesk", "brand_keywords": [], "anti_keywords": []},
        blueprint={"design_context_pack": pack},
        component_list=[
            {"name": "dashboard-table", "family": "data-display", "role": "Data table", "source": "spec"},
            {"name": "workspace-nav", "family": "navigation", "role": "Primary navigation", "source": "spec"},
        ],
        documents=[],
    )

    by_name = {spec["name"]: spec for spec in specs["specs"]}
    assert specs["visual_guidance"]["reference_observations"]
    assert by_name["dashboard-table"]["observed_reference_evidence"]
    assert by_name["workspace-nav"]["observed_reference_evidence"]
    assert by_name["dashboard-table"]["observed_reference_evidence"][0]["provider_id"] == "website-inspection"
