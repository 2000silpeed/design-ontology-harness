from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path

from design_ontology_harness.component_runtime import (
    COMPONENT_RUNTIME_EVIDENCE_SCHEMA,
    COMPONENT_RUNTIME_MANIFEST_SCHEMA,
    DEFAULT_COMPONENT_RUNTIME_MANIFEST,
    LEGACY_COMPONENT_RUNTIME_MANIFEST_SCHEMA,
    validate_component_runtime_conformance,
)
from design_ontology_harness.production_verifier import _runtime_implementation_tree


def _write_json(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _contract() -> dict:
    return {
        "name": "evidence-review",
        "contract_status": "complete",
        "anatomy": {
            "parts": ["root", "evidence-list", "decision-action"],
            "states": ["evidence-loaded", "empty", "focus-visible"],
        },
        "state_model": {
            "domain_states": ["evidence-loaded", "empty"],
            "interaction_states": ["focus-visible"],
            "all_states": ["evidence-loaded", "empty", "focus-visible"],
        },
        "variants": {
            "axes": ["state"],
            "default": "evidence-loaded",
            "constraints": [],
        },
        "props": {
            "state": {"type": "enum"},
            "evidence": {"type": "EvidenceRecord[]", "required": True},
        },
        "interaction": {
            "events": ["select-evidence", "record-decision"],
            "state_transitions": [
                {
                    "from": "evidence-loaded",
                    "event": "record-decision",
                    "to": "empty",
                }
            ],
            "focus_behavior": "Return focus to the selected evidence record.",
            "state_coverage": ["evidence-loaded", "empty"],
        },
        "data_contract": {
            "domain_object": "EvidenceReview",
            "required_fields": ["evidence_id", "source_name"],
            "provenance_required": True,
            "empty_state_required": True,
        },
        "responsive": {
            "required_widths_px": [390, 1280],
            "control_rules": ["Keep the decision action in document flow."],
            "container_behavior": "Reflow the evidence rail into one column.",
        },
        "content_rules": ["Keep source identity beside each record."],
        "dos_and_donts": {
            "do": ["Keep decision status visible."],
            "dont": ["Do not hide provenance."],
        },
        "accessibility": ["Expose the evidence list as a labelled region."],
    }


def _setup_project(tmp_path: Path) -> Path:
    project = tmp_path / "fieldnote"
    project.mkdir()
    source = project / "index.html"
    source.write_text(
        """
        <main data-component-id="evidence-review" data-component-part="root"
              data-component-state="evidence-loaded">
          <ul data-component-part="evidence-list"></ul>
          <button data-component-part="decision-action">Record decision</button>
        </main>
        """,
        encoding="utf-8",
    )
    _write_json(
        project / "build/system/components/component_specs.json",
        {"specs": [_contract()]},
    )
    return project


def _write_v1_manifest(project: Path) -> tuple[dict, Path, Path]:
    contract = _contract()
    tree = _runtime_implementation_tree(project)
    checked_at = datetime.now(timezone.utc).isoformat(timespec="microseconds")
    component_marker = {
        "source_path": "index.html",
        "attribute": "data-component-id",
        "value": "evidence-review",
    }
    part_markers = [
        {
            "part": part,
            "source_path": "index.html",
            "attribute": "data-component-part",
            "value": part,
        }
        for part in contract["anatomy"]["parts"]
    ]
    assertion = [{"id": "browser-observation", "passed": True}]
    state_scenarios = [
        {
            "scenario_id": f"state-{state}",
            "state": state,
            "route": "/review",
            "observed_marker": {
                "attribute": "data-component-state",
                "value": state,
            },
            "assertions": assertion,
        }
        for state in contract["state_model"]["all_states"]
    ]
    interaction_scenarios = [
        {
            "scenario_id": "interaction-select-evidence",
            "event": "select-evidence",
            "route": "/review",
            "assertions": assertion,
            "focus_assertions": assertion,
        },
        {
            "scenario_id": "interaction-record-decision",
            "event": "record-decision",
            "route": "/review",
            "transition": contract["interaction"]["state_transitions"][0],
            "assertions": assertion,
            "focus_assertions": assertion,
        },
    ]
    responsive_scenarios = [
        {
            "scenario_id": f"responsive-{width}",
            "width_px": width,
            "covered_rules": contract["responsive"]["control_rules"],
            "container_behavior": contract["responsive"]["container_behavior"],
            "assertions": assertion,
        }
        for width in contract["responsive"]["required_widths_px"]
    ]
    evidence = {
        "schema_version": COMPONENT_RUNTIME_EVIDENCE_SCHEMA,
        "component_id": "evidence-review",
        "implementation_tree_sha256": tree["sha256"],
        "checked_at": checked_at,
        "dom": {
            "component_marker": component_marker,
            "part_markers": part_markers,
        },
        "state_scenarios": state_scenarios,
        "interaction_scenarios": interaction_scenarios,
        "responsive_scenarios": responsive_scenarios,
        "contract_coverage": {
            "props": list(contract["props"]),
            "data_fields": contract["data_contract"]["required_fields"],
            "content_rules": contract["content_rules"],
            "accessibility_rules": contract["accessibility"],
            "do_rules": contract["dos_and_donts"]["do"],
            "dont_rules": contract["dos_and_donts"]["dont"],
            "variant_axes": contract["variants"]["axes"],
            "default_variant": contract["variants"]["default"],
            "provenance_observed": True,
            "empty_state_observed": True,
        },
    }
    evidence_path = (
        project
        / "build/system/production/component-runtime/evidence-review.json"
    )
    _write_json(evidence_path, evidence)
    manifest = {
        "schema_version": COMPONENT_RUNTIME_MANIFEST_SCHEMA,
        "production_claim": True,
        "legacy_policy": "fail-closed",
        "implementation_tree_sha256": tree["sha256"],
        "checked_at": checked_at,
        "components": [
            {
                "component_id": "evidence-review",
                "source_paths": [
                    {"path": "index.html", "sha256": _sha256(project / "index.html")}
                ],
                "component_marker": component_marker,
                "part_markers": part_markers,
                "evidence": {
                    "path": "build/system/production/component-runtime/evidence-review.json",
                    "sha256": _sha256(evidence_path),
                },
            }
        ],
    }
    manifest_path = project / DEFAULT_COMPONENT_RUNTIME_MANIFEST
    _write_json(manifest_path, manifest)
    return tree, manifest_path, evidence_path


def test_v1_manifest_verifies_static_html_runtime_contract_coverage(tmp_path: Path) -> None:
    project = _setup_project(tmp_path)
    tree, manifest_path, _ = _write_v1_manifest(project)

    report = validate_component_runtime_conformance(
        project_dir=project,
        target_repo=project,
        implementation_tree=tree,
        manifest_path=manifest_path,
        production_claim=True,
    )

    assert report["ok"], report["errors"]
    assert report["verified"]
    assert report["production_eligible"]
    assert report["verified_component_count"] == 1


def test_production_claim_fails_closed_without_manifest(tmp_path: Path) -> None:
    project = _setup_project(tmp_path)
    tree = _runtime_implementation_tree(project)

    production = validate_component_runtime_conformance(
        project_dir=project,
        target_repo=project,
        implementation_tree=tree,
        production_claim=True,
    )
    compatibility = validate_component_runtime_conformance(
        project_dir=project,
        target_repo=project,
        implementation_tree=tree,
        production_claim=False,
    )

    assert not production["ok"]
    assert any("manifest not found" in error for error in production["errors"])
    assert compatibility["ok"]
    assert compatibility["legacy_mode"]
    assert not compatibility["verified"]
    assert not compatibility["production_eligible"]


def test_explicit_v0_manifest_is_legacy_only(tmp_path: Path) -> None:
    project = _setup_project(tmp_path)
    tree = _runtime_implementation_tree(project)
    manifest_path = project / DEFAULT_COMPONENT_RUNTIME_MANIFEST
    _write_json(
        manifest_path,
        {
            "schema_version": LEGACY_COMPONENT_RUNTIME_MANIFEST_SCHEMA,
            "mode": "legacy-unverified",
            "production_eligible": False,
        },
    )

    compatibility = validate_component_runtime_conformance(
        project_dir=project,
        target_repo=project,
        implementation_tree=tree,
        production_claim=False,
    )
    production = validate_component_runtime_conformance(
        project_dir=project,
        target_repo=project,
        implementation_tree=tree,
        production_claim=True,
    )

    assert compatibility["ok"]
    assert compatibility["legacy_mode"]
    assert not compatibility["production_eligible"]
    assert not production["ok"]
    assert any("cannot support a production claim" in error for error in production["errors"])


def test_v1_manifest_rejects_missing_state_and_responsive_evidence(tmp_path: Path) -> None:
    project = _setup_project(tmp_path)
    tree, manifest_path, evidence_path = _write_v1_manifest(project)
    evidence = json.loads(evidence_path.read_text(encoding="utf-8"))
    evidence["state_scenarios"] = evidence["state_scenarios"][:-1]
    evidence["responsive_scenarios"] = evidence["responsive_scenarios"][:-1]
    _write_json(evidence_path, evidence)
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    manifest["components"][0]["evidence"]["sha256"] = _sha256(evidence_path)
    _write_json(manifest_path, manifest)

    report = validate_component_runtime_conformance(
        project_dir=project,
        target_repo=project,
        implementation_tree=tree,
        production_claim=True,
    )

    assert not report["ok"]
    assert any("does not cover states" in error for error in report["errors"])
    assert any("does not cover required widths" in error for error in report["errors"])


def test_v1_manifest_rejects_missing_event_and_transition_evidence(tmp_path: Path) -> None:
    project = _setup_project(tmp_path)
    tree, manifest_path, evidence_path = _write_v1_manifest(project)
    evidence = json.loads(evidence_path.read_text(encoding="utf-8"))
    evidence["interaction_scenarios"] = evidence["interaction_scenarios"][:1]
    _write_json(evidence_path, evidence)
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    manifest["components"][0]["evidence"]["sha256"] = _sha256(evidence_path)
    _write_json(manifest_path, manifest)

    report = validate_component_runtime_conformance(
        project_dir=project,
        target_repo=project,
        implementation_tree=tree,
        production_claim=True,
    )

    assert not report["ok"]
    assert any("does not cover events" in error for error in report["errors"])
    assert any("does not cover contract transitions" in error for error in report["errors"])


def test_v1_manifest_binds_structured_transition_to_scenario_event(tmp_path: Path) -> None:
    project = _setup_project(tmp_path)
    tree, manifest_path, evidence_path = _write_v1_manifest(project)
    evidence = json.loads(evidence_path.read_text(encoding="utf-8"))
    evidence["interaction_scenarios"][1]["event"] = "select-evidence"
    _write_json(evidence_path, evidence)
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    manifest["components"][0]["evidence"]["sha256"] = _sha256(evidence_path)
    _write_json(manifest_path, manifest)

    report = validate_component_runtime_conformance(
        project_dir=project,
        target_repo=project,
        implementation_tree=tree,
        production_claim=True,
    )

    assert not report["ok"]
    assert any(
        "transition event must match the scenario event" in error
        for error in report["errors"]
    )


def test_v1_manifest_is_invalidated_by_runtime_source_change(tmp_path: Path) -> None:
    project = _setup_project(tmp_path)
    _, _, _ = _write_v1_manifest(project)
    source = project / "index.html"
    source.write_text(source.read_text(encoding="utf-8") + "\n<!-- changed -->", encoding="utf-8")
    current_tree = _runtime_implementation_tree(project)

    report = validate_component_runtime_conformance(
        project_dir=project,
        target_repo=project,
        implementation_tree=current_tree,
        production_claim=True,
    )

    assert not report["ok"]
    assert any("implementation_tree_sha256" in error for error in report["errors"])
    assert any("source_paths[0].sha256" in error for error in report["errors"])


def test_v1_manifest_rejects_marker_source_outside_runtime_tree(tmp_path: Path) -> None:
    project = _setup_project(tmp_path)
    tree, manifest_path, evidence_path = _write_v1_manifest(project)
    fake_source = project / "build/system/fake-component.html"
    fake_source.write_text(
        (project / "index.html").read_text(encoding="utf-8"),
        encoding="utf-8",
    )
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    mapping = manifest["components"][0]
    mapping["source_paths"] = [
        {"path": "build/system/fake-component.html", "sha256": _sha256(fake_source)}
    ]
    mapping["component_marker"]["source_path"] = "build/system/fake-component.html"
    for marker in mapping["part_markers"]:
        marker["source_path"] = "build/system/fake-component.html"
    evidence = json.loads(evidence_path.read_text(encoding="utf-8"))
    evidence["dom"]["component_marker"] = mapping["component_marker"]
    evidence["dom"]["part_markers"] = mapping["part_markers"]
    _write_json(evidence_path, evidence)
    mapping["evidence"]["sha256"] = _sha256(evidence_path)
    _write_json(manifest_path, manifest)

    report = validate_component_runtime_conformance(
        project_dir=project,
        target_repo=project,
        implementation_tree=tree,
        production_claim=True,
    )

    assert not report["ok"]
    assert any(
        "not included in the current runtime implementation tree" in error
        for error in report["errors"]
    )


def test_v1_manifest_rejects_marker_and_hashed_artifact_tampering(tmp_path: Path) -> None:
    project = _setup_project(tmp_path)
    tree, manifest_path, evidence_path = _write_v1_manifest(project)
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    manifest["components"][0]["component_marker"]["value"] = "invented-component"
    evidence_path.write_text("{}", encoding="utf-8")
    _write_json(manifest_path, manifest)

    report = validate_component_runtime_conformance(
        project_dir=project,
        target_repo=project,
        implementation_tree=tree,
        production_claim=True,
    )

    assert not report["ok"]
    assert any("component_marker.value" in error for error in report["errors"])
    assert any("sha256 does not match the evidence artifact" in error for error in report["errors"])
