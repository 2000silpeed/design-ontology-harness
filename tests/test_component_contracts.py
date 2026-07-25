from __future__ import annotations

from copy import deepcopy
import json
from pathlib import Path

import pytest

from design_ontology_harness.authoring import (
    build_component_inventory,
    validate_brand_profile,
)
from design_ontology_harness.component_contracts import validate_component_contracts
from design_ontology_harness.component_specs import generate_component_specs
from design_ontology_harness.preset_builder import _validate_component_contract_source
from design_ontology_harness.synthesis import load_brand_profile


def _authored_profile(*, complete: bool) -> dict:
    component = {
        "name": "evidence-verdict",
        "family": "content",
        "role": "Records a reviewer decision against evidence.",
        "supports_primitive": "evidence verdict",
        "states": ["draft", "approved", "rejected"],
    }
    if complete:
        component.update({
            "anatomy": ["root", "evidence-summary", "verdict-control", "decision-note"],
            "content_rules": ["Always show the evidence source and decision owner."],
            "accessibility_notes": ["Expose verdict as a labelled radio group."],
            "dos_and_donts": {"do": ["show provenance"], "dont": ["use color alone"]},
            "variants": {"axes": ["density"], "default": "compact", "constraints": []},
            "interaction": {
                "events": ["approve", "reject"],
                "state_transitions": ["draft -> approved", "draft -> rejected"],
                "focus_behavior": "Return focus to the verdict summary.",
                "state_coverage": ["draft", "approved", "rejected"],
            },
            "data_contract": {
                "domain_object": "evidence verdict",
                "required_fields": ["evidence_id", "decision", "reviewer_id"],
                "provenance_required": True,
                "empty_state_required": False,
            },
            "responsive": {
                "required_widths_px": [320, 390, 768],
                "control_rules": ["stack verdict controls below 390px"],
                "container_behavior": "stack",
            },
            "tokens": {
                "component.verdict.surface": "var(--ds-color-surface)",
                "part.evidence-summary.text": "var(--ds-color-ink)",
                "state.draft.surface": "var(--ds-color-surface-muted)",
            },
        })
    return {
        "brand_name": "Fieldnote",
        "brand_keywords": ["precise"],
        "anti_keywords": ["generic"],
        "product_primitives": ["evidence verdict"],
        "component_decision": {
            "mode": "llm-authored",
            "primitive_reconciliation_version": "product-primitive-reconciliation/v1",
            "primitive_reconciliation": [{
                "primitive": "evidence verdict",
                "resolution": "component",
                "component": "evidence-verdict",
                "reason": "The authored verdict contract owns this product primitive.",
            }],
            "core_components": [component],
        },
    }


def _generate(profile: dict) -> dict:
    blueprint = {"component_strategy": {"required_component_families": ["content"]}}
    inventory = build_component_inventory(profile, blueprint)
    return generate_component_specs(profile, blueprint, inventory["components"], [])


def test_strict_validation_blocks_incomplete_authored_contract() -> None:
    specs = _generate(_authored_profile(complete=False))

    report = validate_component_contracts(specs, strict_authored=True)
    relaxed = validate_component_contracts(specs, strict_authored=False)

    assert not report["ok"]
    assert report["needs_authoring_count"] == 1
    assert any("needs component authoring" in error for error in report["errors"])
    assert specs["specs"][0]["tokens"] == {}
    assert specs["specs"][0]["token_provenance"] == "missing-authored-input"
    assert "missing authored token bindings" in specs["specs"][0]["contract_issues"]
    assert relaxed["ok"]
    assert any("needs component authoring" in warning for warning in relaxed["warnings"])


def test_complete_authored_contract_preserves_domain_states_and_ds_tokens() -> None:
    specs = _generate(_authored_profile(complete=True))
    spec = specs["specs"][0]

    report = validate_component_contracts(specs, strict_authored=True)

    assert report["ok"], report["errors"]
    assert spec["contract_status"] == "complete"
    assert spec["anatomy"]["states"] == ["draft", "approved", "rejected"]
    assert spec["state_model"]["domain_states"] == ["draft", "approved", "rejected"]
    assert spec["data_contract"]["required_fields"] == ["evidence_id", "decision", "reviewer_id"]
    assert spec["token_provenance"] == "authored-input"
    assert all("var(--ds-" in str(value) or "var(" not in str(value) for value in spec["tokens"].values())


def test_empty_generated_baseline_is_needs_authoring_and_cannot_forge_complete() -> None:
    specs = generate_component_specs(
        {"brand_name": "Matchroom", "brand_keywords": ["precise"], "anti_keywords": []},
        {},
        [{
            "name": "match-schedule",
            "family": "data-display",
            "role": "Lists tournament fixtures.",
            "source": "spec",
            "supports_primitive": "fixture schedule",
        }],
        [],
    )
    spec = specs["specs"][0]

    assert spec["contract_provenance"] == "generated-baseline"
    assert spec["token_provenance"] == "generated-family-default"
    assert spec["contract_status"] == "needs-authoring"
    assert {
        "missing domain states",
        "missing interaction events",
        "missing required data fields",
        "missing content rules",
        "missing dos guidance",
        "missing donts guidance",
    } <= set(spec["contract_issues"])
    assert not validate_component_contracts(specs, strict_authored=True)["ok"]
    assert validate_component_contracts(specs, strict_authored=False)["ok"]

    forged = deepcopy(specs)
    forged["specs"][0]["contract_status"] = "complete"
    forged["specs"][0]["contract_issues"] = []
    forged_report = validate_component_contracts(forged, strict_authored=True)

    assert not forged_report["ok"]
    for field in (
        "state_model.domain_states",
        "interaction.events",
        "data_contract.required_fields",
        "content_rules",
        "dos_and_donts.do",
        "dos_and_donts.dont",
    ):
        assert any(field in error for error in forged_report["errors"]), forged_report["errors"]


def test_meaningful_domain_generated_contract_passes_strict_validation() -> None:
    domain_states = ["scheduled", "live", "final"]
    specs = generate_component_specs(
        {"brand_name": "Matchroom", "brand_keywords": ["precise"], "anti_keywords": []},
        {},
        [{
            "name": "match-schedule",
            "family": "data-display",
            "role": "Lists tournament fixtures and score status.",
            "source": "spec",
            "supports_primitive": "fixture schedule",
            "states": domain_states,
            "interaction": {
                "events": ["open-match", "refresh-score"],
                "state_transitions": ["scheduled -> live", "live -> final"],
                "focus_behavior": "Keep focus on the selected fixture after score refresh.",
                "state_coverage": domain_states,
            },
            "data_contract": {
                "domain_object": "fixture",
                "required_fields": ["fixture_id", "kickoff_at", "home_team", "away_team", "status"],
                "provenance_required": True,
                "empty_state_required": True,
            },
            "content_rules": ["Show the timezone beside every kickoff time."],
            "dos_and_donts": {
                "do": ["Keep team names and score status visible together."],
                "dont": ["Do not imply a final score while the fixture is live."],
            },
        }],
        [],
    )
    spec = specs["specs"][0]

    report = validate_component_contracts(specs, strict_authored=True)

    assert report["ok"], report["errors"]
    assert spec["contract_provenance"] == "generated-baseline"
    assert spec["contract_status"] == "complete"
    assert spec["state_model"]["domain_states"] == domain_states


def test_validation_blocks_token_not_emitted_by_tokens_css() -> None:
    specs = _generate(_authored_profile(complete=True))
    token_css = ":root { --ds-color-surface: #fff; }"

    report = validate_component_contracts(specs, token_css=token_css)

    assert not report["ok"]
    assert any("missing emitted token" in error for error in report["errors"])


def test_preset_promotion_blocks_needs_authoring_contracts(tmp_path) -> None:
    components_dir = tmp_path / "components"
    components_dir.mkdir()
    specs_path = components_dir / "component_specs.json"
    specs_path.write_text(json.dumps(_generate(_authored_profile(complete=False))), encoding="utf-8")

    with pytest.raises(ValueError, match="not promotion-ready"):
        _validate_component_contract_source(tmp_path)

    specs_path.write_text(json.dumps(_generate(_authored_profile(complete=True))), encoding="utf-8")
    metadata = _validate_component_contract_source(tmp_path)
    assert metadata["component_contract_version"] == "component-contract/v1"
    assert metadata["component_contract_count"] == 1
    assert metadata["component_contract_needs_authoring"] == 0


def test_authored_token_notes_cannot_masquerade_as_authored_bindings() -> None:
    profile = _authored_profile(complete=True)
    component = profile["component_decision"]["core_components"][0]
    component.pop("tokens")
    component["token_notes"] = {
        "surface": "var(--ds-color-surface)",
        "text": "var(--ds-color-ink)",
    }

    specs = _generate(profile)
    spec = specs["specs"][0]

    assert spec["tokens"] == {}
    assert spec["token_provenance"] == "missing-authored-input"
    assert spec["contract_status"] == "needs-authoring"
    assert not validate_component_contracts(specs, strict_authored=True)["ok"]


def test_authored_token_targets_must_name_declared_anatomy_and_state() -> None:
    profile = _authored_profile(complete=True)
    tokens = profile["component_decision"]["core_components"][0]["tokens"]
    tokens["part.unknown-part.text"] = "var(--ds-color-ink)"
    tokens["state.unknown-state.surface"] = "var(--ds-color-surface)"

    specs = _generate(profile)
    spec = specs["specs"][0]
    report = validate_component_contracts(specs, strict_authored=True)

    assert spec["contract_status"] == "needs-authoring"
    assert any("unknown anatomy part" in issue for issue in spec["contract_issues"])
    assert any("unknown state" in issue for issue in spec["contract_issues"])
    assert not report["ok"]


def test_world_cup_authored_source_reconciles_every_primitive_and_passes_strict() -> None:
    root = Path(__file__).resolve().parents[1]
    project = root / "projects" / "world-cup-hub"
    profile = load_brand_profile(project / "brand_profile.json")
    validation = validate_brand_profile(profile)
    assert validation["valid"], validation["errors"]

    blueprint = {
        "component_strategy": {
            "required_component_families": [
                "layout",
                "navigation",
                "input",
                "data-display",
                "feedback",
                "content",
            ]
        }
    }
    inventory = build_component_inventory(profile, blueprint)
    specs = generate_component_specs(profile, blueprint, inventory["components"], [])
    report = validate_component_contracts(
        specs,
        token_css=(project / "design-system" / "tokens.css").read_text(
            encoding="utf-8"
        ),
        strict_authored=True,
    )

    assert report["ok"], report["errors"]
    assert report["authored_contract_count"] == 19
    assert report["primitive_reconciliation_count"] == 28
    assert report["primitive_waiver_count"] == 3
    assert {spec["token_provenance"] for spec in specs["specs"]} == {
        "authored-input"
    }
    assert len({tuple(sorted(spec["tokens"])) for spec in specs["specs"]}) == 19
    assert {entry["primitive"] for entry in specs["primitive_reconciliation"]} == set(
        profile["product_primitives"]
    )


def test_world_cup_waivers_require_machine_verifiable_approval_fields() -> None:
    root = Path(__file__).resolve().parents[1]
    profile = load_brand_profile(
        root / "projects" / "world-cup-hub" / "brand_profile.json"
    )
    decision = profile["component_decision"]
    bracket = next(
        record
        for record in decision["primitive_reconciliation"]
        if record["primitive"] == "bracket preview"
    )
    bracket["waiver"].pop("decision_source")
    bracket["waiver"]["approval_status"] = "pending"

    validation = validate_brand_profile(profile)

    assert not validation["valid"]
    assert any("waiver.decision_source is required" in error for error in validation["errors"])
    assert any(
        "waiver.approval_status must be approved" in error
        for error in validation["errors"]
    )
