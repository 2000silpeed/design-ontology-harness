from __future__ import annotations

import json
from pathlib import Path

import pytest

from design_ontology_harness.reference_fidelity import (
    CONTRACT_SCHEMA,
    LOOP_SCHEMA,
    REVIEW_SCHEMA,
    run_reference_fidelity_loop,
    sha256_file,
    validate_reference_fidelity_contract,
    validate_reference_fidelity_report,
)


def _write_json(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def _contract(project: Path) -> Path:
    brief = project / "design-system" / "references" / "selected-direction.md"
    reference = project / "design-system" / "references" / "approved.png"
    brief.parent.mkdir(parents=True, exist_ok=True)
    brief.write_text(
        "# Selected direction\nPreserve asymmetric composition, compact density, and a persistent context rail.\n",
        encoding="utf-8",
    )
    reference.write_bytes(b"approved-reference-image")
    path = project / "design-system" / "reference-fidelity-contract.json"
    _write_json(
        path,
        {
            "schema_version": CONTRACT_SCHEMA,
            "contract_id": "fixture-desk-direction",
            "authority": {
                "source_order": "brief-and-ontology-before-reference",
                "prohibited_similarity_scopes": [
                    "palette",
                    "typography",
                    "information_architecture",
                    "product_copy",
                    "logos",
                    "redistributable_assets",
                ],
            },
            "brief": {
                "path": brief.relative_to(project).as_posix(),
                "sha256": sha256_file(brief),
            },
            "references": [
                {
                    "path": reference.relative_to(project).as_posix(),
                    "sha256": sha256_file(reference),
                }
            ],
            "gate": {"threshold": 0.82, "max_iterations": 3},
            "metrics": [
                {
                    "id": "asymmetric_workspace_composition",
                    "dimension": "composition",
                    "statement": "Keep a dominant workspace beside a persistent contextual rail.",
                    "source_quote": "strong asymmetric desktop composition",
                    "weight": 0.55,
                    "minimum_score": 0.78,
                    "critical": True,
                },
                {
                    "id": "first_viewport_task_priority",
                    "dimension": "task_visibility",
                    "statement": "Keep the primary fixture task visible in the first viewport.",
                    "source_quote": "single decisive selection state",
                    "weight": 0.45,
                    "minimum_score": 0.76,
                    "critical": True,
                },
            ],
        },
    )
    return path


def _review(
    project: Path,
    contract: Path,
    *,
    name: str,
    screenshot_hash: str,
    composition_score: float,
    task_score: float,
) -> Path:
    contract_payload = json.loads(contract.read_text(encoding="utf-8"))
    reference_hashes = sorted(item["sha256"] for item in contract_payload["references"])
    path = project / "build" / "system" / "production" / "reference-fidelity" / f"{name}.json"

    def finding(score: float, observation: str, remediation: str) -> dict:
        return {
            "score": score,
            "status": "passed" if score >= 0.78 else "failed",
            "observation": observation,
            "remediation": remediation,
        }

    task_finding = finding(
        task_score,
        "The approved direction opens on the fixture task, while the candidate uses the first viewport for a prose-led status header.",
        "Move the operational fixture workspace above explanatory status content.",
    )
    task_finding["status"] = "passed" if task_score >= 0.76 else "failed"
    _write_json(
        path,
        {
            "schema_version": REVIEW_SCHEMA,
            "contract_sha256": sha256_file(contract),
            "reference_sha256": reference_hashes,
            "implementation_tree_sha256": "b" * 64,
            "screenshot_sha256": [screenshot_hash],
            "source": "multimodal-review",
            "reviewer": "reference-fidelity-auditor",
            "model": "gpt-5-codex",
            "method": "Paired image review of approved invariants against the frozen implementation screenshots.",
            "reviewed_at": "2026-07-14T15:00:00+09:00",
            "metric_findings": {
                "asymmetric_workspace_composition": finding(
                    composition_score,
                    "The approved image has a dominant asymmetric three-region workspace, but the candidate begins as a wide editorial header and ticker.",
                    "Restore the dominant workspace and persistent context rail as the page silhouette.",
                ),
                "first_viewport_task_priority": task_finding,
            },
        },
    )
    return path


def test_blocked_review_emits_actionable_correction_brief(tmp_path: Path) -> None:
    contract = _contract(tmp_path)
    screenshot_hash = "a" * 64
    review = _review(
        tmp_path,
        contract,
        name="review-1",
        screenshot_hash=screenshot_hash,
        composition_score=0.42,
        task_score=0.31,
    )

    report = run_reference_fidelity_loop(
        contract_path=contract,
        review_artifact_paths=[review],
        project_dir=tmp_path,
        expected_screenshot_sha256={screenshot_hash},
        implementation_tree_sha256="b" * 64,
    )

    assert report["schema_version"] == LOOP_SCHEMA
    assert not report["passed"]
    assert report["status"] == "blocked"
    assert report["selected_iteration"] is None
    assert {action["metric_id"] for action in report["next_iteration_brief"]["actions"]} == {
        "asymmetric_workspace_composition",
        "first_viewport_task_priority",
    }


def test_passing_latest_review_is_content_bound_for_release(tmp_path: Path) -> None:
    contract = _contract(tmp_path)
    screenshot_hash = "c" * 64
    review = _review(
        tmp_path,
        contract,
        name="review-pass",
        screenshot_hash=screenshot_hash,
        composition_score=0.9,
        task_score=0.88,
    )
    report = run_reference_fidelity_loop(
        contract_path=contract,
        review_artifact_paths=[review],
        project_dir=tmp_path,
        expected_screenshot_sha256={screenshot_hash},
        implementation_tree_sha256="b" * 64,
    )
    report_path = tmp_path / "build/system/production/reference-fidelity/latest_loop_report.json"
    _write_json(report_path, report)

    errors, evidence = validate_reference_fidelity_report(
        report_path,
        contract_path=contract,
        project_dir=tmp_path,
        screenshot_sha256={screenshot_hash},
        implementation_tree_sha256="b" * 64,
    )

    assert not errors
    assert evidence["latest_score"] > 0.82

    review_payload = json.loads(review.read_text(encoding="utf-8"))
    review_payload["metric_findings"]["first_viewport_task_priority"]["score"] = 0.2
    _write_json(review, review_payload)
    errors, _ = validate_reference_fidelity_report(
        report_path,
        contract_path=contract,
        project_dir=tmp_path,
        screenshot_sha256={screenshot_hash},
        implementation_tree_sha256="b" * 64,
    )
    assert any("sha256 does not match" in error for error in errors)


def test_loop_rejects_score_only_iteration_with_same_screenshots(tmp_path: Path) -> None:
    contract = _contract(tmp_path)
    screenshot_hash = "d" * 64
    first = _review(
        tmp_path,
        contract,
        name="review-1",
        screenshot_hash=screenshot_hash,
        composition_score=0.4,
        task_score=0.3,
    )
    second = _review(
        tmp_path,
        contract,
        name="review-2",
        screenshot_hash=screenshot_hash,
        composition_score=0.9,
        task_score=0.9,
    )

    with pytest.raises(ValueError, match="fresh screenshot SHA set"):
        run_reference_fidelity_loop(
            contract_path=contract,
            review_artifact_paths=[first, second],
            project_dir=tmp_path,
        )


def test_loop_rejects_new_screenshots_from_an_unchanged_runtime(tmp_path: Path) -> None:
    contract = _contract(tmp_path)
    first = _review(
        tmp_path,
        contract,
        name="review-runtime-1",
        screenshot_hash="e" * 64,
        composition_score=0.4,
        task_score=0.3,
    )
    second = _review(
        tmp_path,
        contract,
        name="review-runtime-2",
        screenshot_hash="f" * 64,
        composition_score=0.9,
        task_score=0.9,
    )

    with pytest.raises(ValueError, match="fresh runtime-tree SHA"):
        run_reference_fidelity_loop(
            contract_path=contract,
            review_artifact_paths=[first, second],
            project_dir=tmp_path,
        )


def test_contract_forbids_reference_authority_over_palette_and_copy(tmp_path: Path) -> None:
    contract = _contract(tmp_path)
    payload = json.loads(contract.read_text(encoding="utf-8"))
    payload["authority"]["prohibited_similarity_scopes"].remove("palette")
    payload["metrics"][0]["dimension"] = "color_similarity"
    _write_json(contract, payload)

    errors, _ = validate_reference_fidelity_contract(contract, project_dir=tmp_path)

    assert any("missing: palette" in error for error in errors)
    assert any("color_similarity" in error for error in errors)
