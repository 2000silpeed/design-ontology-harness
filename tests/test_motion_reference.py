from __future__ import annotations

import json
from pathlib import Path

import pytest

from design_ontology_harness.motion_reference import (
    MotionReferencePackError,
    load_motion_reference_pack,
    motion_pattern_ids,
    validate_motion_reference_pack,
)


ROOT = Path(__file__).resolve().parent.parent
PACK_PATH = ROOT / "design_ontology_harness" / "resources" / "vibecoding-motion-reference.json"
TOKEN_PATH = ROOT / "presets" / "dashboard--minimal-tech" / "token_schema.json"


def test_bundled_motion_pack_loads_and_exposes_existing_ontology_concepts() -> None:
    pack = load_motion_reference_pack()

    assert pack["status"] == "draft"
    assert len(pack["sources"]) == 5
    assert "interaction:dot-progress" in motion_pattern_ids(pack)
    assert all(pattern["ontology_type"] == "InteractionPattern" for pattern in pack["patterns"])
    assert {rule["ontology_type"] for rule in pack["rules"]} == {
        "AccessibilityRule",
        "GovernanceRule",
    }


def test_motion_pack_matches_dashboard_minimal_motion_contract() -> None:
    pack = load_motion_reference_pack()
    token_schema = json.loads(TOKEN_PATH.read_text(encoding="utf-8"))
    motion = token_schema["categories"]["motion"]

    for pattern in pack["patterns"]:
        assert pattern["motion"]["duration_ms"] in motion["durations_ms"]
        assert pattern["motion"]["easing"] in motion["easing_tokens"]

    assert "low-noise motion" in token_schema["brand_alignment"]["interaction_keywords"]
    assert any(
        rule["id"] == "governance:low-noise-dashboard" and rule["severity"] == "required"
        for rule in pack["rules"]
    )


def test_verified_source_cannot_omit_canonical_url() -> None:
    pack = load_motion_reference_pack()
    pack["sources"][0]["license_status"] = "verified"
    pack["sources"][0]["canonical_url"] = None

    with pytest.raises(MotionReferencePackError, match="canonical_url"):
        validate_motion_reference_pack(pack)


def test_pattern_cannot_bypass_reduced_motion() -> None:
    pack = load_motion_reference_pack()
    pack["patterns"][0]["motion"]["reduced_motion"] = "unbounded"

    with pytest.raises(MotionReferencePackError, match="reduced-motion"):
        validate_motion_reference_pack(pack)
