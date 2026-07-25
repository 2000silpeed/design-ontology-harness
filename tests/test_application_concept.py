import json
from pathlib import Path

import pytest

from design_ontology_harness.authoring import (
    build_token_schema,
    generate_system_pack,
    validate_brand_profile,
)
from design_ontology_harness.scaffold import scaffold_project


REPO_ROOT = Path(__file__).resolve().parents[1]


def _legacy_profile() -> dict:
    return {
        "brand_name": "Legacy App",
        "system_name": "Legacy App System",
        "product_summary": "A legacy profile that predates authored concept fields.",
        "audiences": ["Operators"],
        "brand_keywords": ["clear", "reliable", "focused"],
        "anti_keywords": ["generic"],
        "tone_of_voice": ["direct"],
        "visual_keywords": ["structured"],
        "interaction_keywords": ["inspectable"],
        "platforms": ["web"],
        "accessibility_targets": ["WCAG 2.2 AA"],
        "product_primitives": ["shell", "table", "detail panel"],
    }


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


def test_legacy_profile_without_authored_scope_keeps_compatibility() -> None:
    report = validate_brand_profile(_legacy_profile())

    assert report["valid"] is True
    assert report["errors"] == []


def test_authored_component_scope_requires_all_concept_fields() -> None:
    profile = _legacy_profile()
    profile["component_decision_path"] = "design-system/component-contracts.json"

    report = validate_brand_profile(profile)

    assert report["valid"] is False
    assert report["errors"] == [
        "Missing required concept key: application_concept",
        "Missing required concept key: layout_skeleton",
        "Missing required concept key: design_differentiation",
    ]


def test_system_generation_stops_at_failed_concept_gate(tmp_path) -> None:
    profile = _legacy_profile()
    profile["component_decision_path"] = "design-system/component-contracts.json"

    with pytest.raises(ValueError, match="Missing required concept key: application_concept"):
        generate_system_pack(tmp_path / "build", profile, {}, [], [])


def test_strict_concept_gate_rejects_unedited_scaffold_placeholders(tmp_path) -> None:
    project_dir = tmp_path / "placeholder-app"
    scaffold_project(project_dir, brand_name="Placeholder App")
    profile = json.loads((project_dir / "brand_profile.json").read_text(encoding="utf-8"))
    profile["component_decision_path"] = "design-system/component-contracts.json"

    report = validate_brand_profile(profile)

    assert report["valid"] is False
    assert any("application_concept.primary_job" in error for error in report["errors"])
    assert any("layout_skeleton.composition" in error for error in report["errors"])
    assert any("design_differentiation.signature_moves" in error for error in report["errors"])
    assert all("scaffold placeholder" in error for error in report["errors"])


def test_world_cup_hub_profile_passes_authored_concept_gate() -> None:
    profile = json.loads(
        (REPO_ROOT / "projects" / "world-cup-hub" / "brand_profile.json").read_text(
            encoding="utf-8"
        )
    )

    report = validate_brand_profile(profile)

    assert report["valid"] is True
    assert report["errors"] == []
