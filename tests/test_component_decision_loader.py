import json
from pathlib import Path

import pytest

from design_ontology_harness.synthesis import load_brand_profile


def _profile() -> dict:
    return {
        "brand_name": "Test",
        "system_name": "Test System",
        "product_summary": "Test product",
        "audiences": [],
        "brand_keywords": [],
        "anti_keywords": [],
        "tone_of_voice": [],
        "visual_keywords": [],
        "interaction_keywords": [],
        "platforms": ["web"],
        "accessibility_targets": [],
        "product_primitives": [],
    }


def test_loads_project_local_component_decision(tmp_path: Path) -> None:
    profile = _profile()
    profile["component_decision_path"] = "design/component-contracts.json"
    decision = {
        "mode": "authored",
        "core_components": [{"name": "fixture-table"}],
    }
    (tmp_path / "design").mkdir()
    (tmp_path / "design" / "component-contracts.json").write_text(
        json.dumps({"component_decision": decision}), encoding="utf-8"
    )
    profile_path = tmp_path / "brand_profile.json"
    profile_path.write_text(json.dumps(profile), encoding="utf-8")

    loaded = load_brand_profile(profile_path)

    assert loaded["component_decision"] == decision
    assert loaded["_component_decision_source"] == "design/component-contracts.json"


def test_rejects_component_decision_path_escape(tmp_path: Path) -> None:
    profile = _profile()
    profile["component_decision_path"] = "../outside.json"
    profile_path = tmp_path / "brand_profile.json"
    profile_path.write_text(json.dumps(profile), encoding="utf-8")

    with pytest.raises(ValueError, match="inside the project"):
        load_brand_profile(profile_path)


def test_rejects_inline_and_external_component_decision(tmp_path: Path) -> None:
    profile = _profile()
    profile["component_decision_path"] = "components.json"
    profile["component_decision"] = {"core_components": []}
    profile_path = tmp_path / "brand_profile.json"
    profile_path.write_text(json.dumps(profile), encoding="utf-8")

    with pytest.raises(ValueError, match="either component_decision"):
        load_brand_profile(profile_path)
