from __future__ import annotations

import json
import re
from pathlib import Path

import pytest

from design_ontology_harness.motion_reference import (
    MotionReferencePackError,
    build_motion_system,
    default_motion_system,
    load_motion_reference_pack,
    motion_pattern_ids,
    motion_token_declarations,
    validate_motion_reference_pack,
)


ROOT = Path(__file__).resolve().parent.parent
PACK_PATH = ROOT / "design_ontology_harness" / "resources" / "vibecoding-motion-reference.json"
TOKEN_PATH = ROOT / "presets" / "dashboard--minimal-tech" / "token_schema.json"


def test_bundled_motion_pack_loads_and_exposes_existing_ontology_concepts() -> None:
    pack = load_motion_reference_pack()

    assert pack["status"] == "reviewed"
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

    # Transitions and loops draw on separate budgets. A loading affordance may
    # cycle for over a second; a state transition may not.
    for pattern in pack["patterns"]:
        kind = pattern["motion"].get("kind", "transition")
        budget = motion["loop_ms"] if kind == "loop" else motion["durations_ms"]
        assert pattern["motion"]["duration_ms"] in budget, (
            f"{pattern['id']} ({kind}) is outside its budget"
        )
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


def test_every_source_carries_a_confirmed_url() -> None:
    """The pack left draft on the strength of these URLs; keep them present."""
    pack = load_motion_reference_pack()

    for source in pack["sources"]:
        assert source["canonical_url"], f"{source['id']} lost its canonical_url"
        assert source["provenance"] == "inspected"
        assert source["license_status"] in {"reference-only", "verified"}


def test_pattern_cannot_bypass_reduced_motion() -> None:
    pack = load_motion_reference_pack()
    pack["patterns"][0]["motion"]["reduced_motion"] = "unbounded"

    with pytest.raises(MotionReferencePackError, match="reduced-motion"):
        validate_motion_reference_pack(pack)


def test_transition_pattern_cannot_borrow_the_loop_budget() -> None:
    pack = load_motion_reference_pack()
    pack["patterns"][0]["motion"]["kind"] = "transition"
    pack["patterns"][0]["motion"]["duration_ms"] = 1200

    with pytest.raises(MotionReferencePackError, match="transition budget"):
        validate_motion_reference_pack(pack)


def test_motion_tokens_cover_the_whole_scale_and_easing_set() -> None:
    declarations = motion_token_declarations(default_motion_system())
    rendered = "\n".join(declarations)

    for step in (80, 120, 180, 240, 320):
        assert f"--ds-duration-{step}:" in rendered
    for name in ("fast", "medium", "slow"):
        assert f"--ds-loop-{name}:" in rendered
    for name in ("standard", "enter", "exit", "emphasized"):
        assert f"--ds-ease-{name}:" in rendered
    assert "--ds-motion-reduced-strategy:" in rendered


def test_motion_system_override_merges_without_dropping_scale_steps() -> None:
    system = build_motion_system(
        {"motion_system": {"easing": {"standard": "linear"}, "reduced_motion_strategy": "static"}}
    )

    assert system["easing"]["standard"] == "linear"
    assert system["easing"]["enter"] == default_motion_system()["easing"]["enter"]
    assert system["reduced_motion_strategy"] == "static"
    assert system["transition_scale_ms"] == default_motion_system()["transition_scale_ms"]


def test_component_contract_motion_variables_exist_in_emitted_tokens() -> None:
    """The contract may only reference custom properties the emitter defines.

    Component specs previously asked implementations for ``var(--duration-180)``
    while the emitter defined ``--ds-duration-180``. Nothing resolved, so every
    mockup fell back to raw literals.
    """
    from design_ontology_harness.component_specs import (
        BRAND_ADAPTATIONS,
        COMPONENT_ANATOMY,
    )

    declared = {
        line.strip().split(":")[0].strip()
        for line in motion_token_declarations(default_motion_system())
    }
    contract_text = json.dumps([COMPONENT_ANATOMY, BRAND_ADAPTATIONS], ensure_ascii=False)
    referenced = set(
        re.findall(r"var\((--ds-(?:duration|loop|ease)-[a-z0-9]+)\)", contract_text)
    )

    assert referenced, "component specs should bind motion through tokens"
    assert referenced <= declared, f"unresolvable motion variables: {sorted(referenced - declared)}"
