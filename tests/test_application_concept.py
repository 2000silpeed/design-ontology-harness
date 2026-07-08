import json

from design_ontology_harness.authoring import build_token_schema
from design_ontology_harness.scaffold import scaffold_project


def test_scaffold_prompts_for_application_concept_and_layout_skeleton(tmp_path) -> None:
    project_dir = tmp_path / "concept-app"

    scaffold_project(project_dir, brand_name="Concept App")

    profile = json.loads((project_dir / "brand_profile.json").read_text(encoding="utf-8"))
    assert "application_concept" in profile
    assert "layout_skeleton" in profile
    assert "design_differentiation" in profile
    assert profile["layout_skeleton"]["first_screen_contract"]
    assert "generic hero plus card grid" in profile["layout_skeleton"]["avoid_layouts"]


def test_layout_skeleton_flows_into_token_schema() -> None:
    brand_profile = {
        "brand_name": "Evidence Workbench",
        "system_name": "Evidence Workbench System",
        "brand_keywords": ["precise", "calm", "structured"],
        "visual_keywords": ["dense", "inspectable"],
        "interaction_keywords": ["review", "compare"],
    }
    blueprint = {
        "system_name": "Evidence Workbench System",
        "application_concept": {
            "primary_job": "Review evidence and decide whether a claim is supported.",
            "operating_mode": "review",
            "success_moment": "Reviewer reaches a documented approve or reject state.",
        },
        "layout_skeleton": {
            "composition": "split-workbench",
            "navigation_model": "task-rail",
            "density": "dense",
            "primary_regions": [
                {
                    "name": "Evidence queue",
                    "role": "Items waiting for review",
                    "priority": "primary",
                }
            ],
            "first_screen_contract": [
                "Show the evidence queue and active claim side by side.",
            ],
            "avoid_layouts": ["uniform dashboard metric cards"],
        },
        "differentiation_strategy": {
            "signature_moves": ["Queue and claim detail remain co-present."],
            "repetition_risks": ["metric cards before the evidence surface"],
        },
        "governance": {},
    }

    schema = build_token_schema(brand_profile, blueprint)

    assert schema["categories"]["spacing"]["density_modes"] == ["compact", "dense"]
    skeleton = schema["categories"]["layout"]["skeleton"]
    assert skeleton["composition"] == "split-workbench"
    assert skeleton["navigation_model"] == "task-rail"
    assert skeleton["signature_moves"] == ["Queue and claim detail remain co-present."]
    assert schema["brand_alignment"]["application_concept"]["operating_mode"] == "review"
