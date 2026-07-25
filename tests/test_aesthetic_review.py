from __future__ import annotations

import hashlib
import json
import subprocess
import sys
from pathlib import Path

import pytest

from design_ontology_harness.aesthetic_loop import (
    DEFAULT_METRICS,
    apply_aesthetic_review,
    build_aesthetic_ontology,
    run_self_improvement_loop,
)


REPO_ROOT = Path(__file__).resolve().parent.parent


def _write_json(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _candidate(screenshot: Path, *, value: float = 7.6) -> dict:
    screenshot_hash = _sha256(screenshot)
    return {
        "schema_version": "aesthetic-candidate/v1",
        "design_id": "signal-desk",
        "score_scale": 10,
        "source_screenshots": [str(screenshot)],
        "measurement_protocol": {
            "method": "automated screenshot heuristic v1",
            "note": "Pixel proxy baseline.",
        },
        "metrics": {metric_id: value for metric_id in DEFAULT_METRICS},
        "metric_evidence": {
            metric_id: [{"source": "automated", "method": "screenshot heuristic"}]
            for metric_id in DEFAULT_METRICS
        },
        "automated_feature_report": {
            "screenshots": [
                {
                    "path": str(screenshot),
                    "sha256": screenshot_hash,
                    "width": 1440,
                    "height": 1000,
                }
            ]
        },
    }


def _artifact(screenshot: Path, *, metrics: dict[str, float]) -> dict:
    return {
        "schema_version": "production-ui-review-artifact/v1",
        "run_id": "visual-review-20260712",
        "reviewed_at": "2026-07-12T12:00:00+09:00",
        "screenshot_sha256": [_sha256(screenshot)],
        "metric_findings": {
            metric_id: {
                "score": score,
                "note": f"Reviewed {metric_id} against the complete screenshot set.",
            }
            for metric_id, score in metrics.items()
        },
    }


def test_apply_aesthetic_review_builds_a_hashed_second_iteration(tmp_path: Path) -> None:
    screenshot = tmp_path / "dashboard.png"
    screenshot.write_bytes(b"rendered-dashboard")
    candidate = _candidate(screenshot)
    artifact = _artifact(screenshot, metrics={"hierarchy_clarity": 9.2, "domain_fit": 8.9})
    candidate_path = tmp_path / "candidate.json"
    artifact_path = tmp_path / "review.json"
    _write_json(candidate_path, candidate)
    _write_json(artifact_path, artifact)

    merged = apply_aesthetic_review(
        candidate,
        artifact,
        review_artifact_path=artifact_path,
        reviewer="codex-visual-qa",
        model="gpt-5-codex",
        method="Structured side-by-side multimodal review",
        candidate_path=candidate_path,
    )

    assert merged["source_screenshots"] == candidate["source_screenshots"]
    assert merged["measurement_protocol"]["method"] == candidate["measurement_protocol"]["method"]
    assert merged["measurement_protocol"]["note"] == candidate["measurement_protocol"]["note"]
    assert len(merged["iterations"]) == 2
    base, reviewed = merged["iterations"]
    assert base["metrics"] == candidate["metrics"]
    assert base["iteration_id"] == "iteration-1"
    assert reviewed["iteration_id"] == "iteration-2"
    assert reviewed["metrics"]["hierarchy_clarity"] == 9.2
    assert reviewed["metrics"]["domain_fit"] == 8.9
    assert reviewed["metrics"]["color_harmony"] == candidate["metrics"]["color_harmony"]

    evidence = reviewed["metric_evidence"]["hierarchy_clarity"][-1]
    assert evidence["source"] == "multimodal-review"
    assert evidence["reviewer"] == "codex-visual-qa"
    assert evidence["model"] == "gpt-5-codex"
    assert evidence["method"] == "Structured side-by-side multimodal review"
    assert evidence["artifact"] == str(artifact_path.resolve())
    assert evidence["artifact_sha256"] == _sha256(artifact_path)
    assert evidence["screenshot_sha256"] == [_sha256(screenshot)]
    assert reviewed["metric_evidence"]["color_harmony"] == candidate["metric_evidence"]["color_harmony"]
    production_review = merged["measurement_protocol"]["production_review"]
    assert production_review["schema_version"] == "production-ui-review/v1"
    assert production_review["review_runs"] == [
        {
            "run_id": "visual-review-20260712",
            "source": "multimodal-review",
            "reviewer": "codex-visual-qa",
            "model": "gpt-5-codex",
            "method": "Structured side-by-side multimodal review",
            "reviewed_at": "2026-07-12T12:00:00+09:00",
            "screenshot_sha256": [_sha256(screenshot)],
            "artifact": {
                "path": str(artifact_path.resolve()),
                "sha256": _sha256(artifact_path),
            },
        }
    ]
    assert reviewed["measurement_protocol"] == merged["measurement_protocol"]


def test_applied_review_is_evaluated_as_a_real_second_loop_iteration(tmp_path: Path) -> None:
    screenshot = tmp_path / "dashboard.png"
    screenshot.write_bytes(b"rendered-dashboard")
    candidate = _candidate(screenshot, value=7.5)
    artifact = _artifact(
        screenshot,
        metrics={metric_id: 9.0 for metric_id in DEFAULT_METRICS},
    )
    artifact_path = tmp_path / "review.json"
    _write_json(artifact_path, artifact)

    merged = apply_aesthetic_review(
        candidate,
        artifact,
        review_artifact_path=artifact_path,
        reviewer="codex-visual-qa",
        model="gpt-5-codex",
        method="Structured side-by-side multimodal review",
    )
    report = run_self_improvement_loop(
        merged,
        build_aesthetic_ontology({"brand_name": "Signal Desk"}),
        threshold=0.82,
    )

    assert [iteration["iteration_id"] for iteration in report["iterations"]] == [
        "iteration-1",
        "iteration-2",
    ]
    assert report["selected_iteration"] == "iteration-2"
    assert report["iterations"][1]["evidence_sources"] == [
        "automated",
        "multimodal-review",
    ]
    assert (
        report["measurement_protocol"]["production_review"]["schema_version"]
        == "production-ui-review/v1"
    )
    assert report["measurement_protocol"]["production_review"]["review_runs"][0][
        "run_id"
    ] == "visual-review-20260712"


def test_apply_aesthetic_review_rejects_unknown_metrics_and_hash_mismatch(tmp_path: Path) -> None:
    screenshot = tmp_path / "dashboard.png"
    screenshot.write_bytes(b"rendered-dashboard")
    candidate = _candidate(screenshot)

    unknown_artifact = _artifact(screenshot, metrics={"invented_metric": 9.0})
    unknown_path = tmp_path / "unknown.json"
    _write_json(unknown_path, unknown_artifact)
    with pytest.raises(ValueError, match="unknown candidate metric"):
        apply_aesthetic_review(
            candidate,
            unknown_artifact,
            review_artifact_path=unknown_path,
            reviewer="reviewer",
            model="model",
            method="method",
        )

    mismatched_artifact = _artifact(screenshot, metrics={"domain_fit": 9.0})
    mismatched_artifact["screenshot_sha256"] = ["0" * 64]
    mismatched_path = tmp_path / "mismatched.json"
    _write_json(mismatched_path, mismatched_artifact)
    with pytest.raises(ValueError, match="must exactly match"):
        apply_aesthetic_review(
            candidate,
            mismatched_artifact,
            review_artifact_path=mismatched_path,
            reviewer="reviewer",
            model="model",
            method="method",
        )


def test_apply_aesthetic_review_hashes_source_files_when_feature_report_is_absent(tmp_path: Path) -> None:
    screenshot = tmp_path / "screens" / "mobile.png"
    screenshot.parent.mkdir()
    screenshot.write_bytes(b"mobile-render")
    candidate = _candidate(screenshot)
    candidate.pop("automated_feature_report")
    candidate["source_screenshots"] = ["screens/mobile.png"]
    candidate_path = tmp_path / "candidate.json"
    artifact = _artifact(screenshot, metrics={"responsive_fit": 9.4})
    artifact.update(
        {
            "reviewer": "artifact-reviewer",
            "model": "artifact-model",
            "method": "Artifact-declared multimodal review method",
        }
    )
    artifact_path = tmp_path / "review.json"
    _write_json(candidate_path, candidate)
    _write_json(artifact_path, artifact)

    merged = apply_aesthetic_review(
        candidate,
        artifact,
        review_artifact_path=artifact_path,
        candidate_path=candidate_path,
    )

    assert merged["iterations"][1]["metrics"]["responsive_fit"] == 9.4
    review_run = merged["measurement_protocol"]["production_review"]["review_runs"][0]
    assert review_run["reviewer"] == "artifact-reviewer"
    assert review_run["model"] == "artifact-model"
    assert review_run["method"] == "Artifact-declared multimodal review method"


def test_apply_aesthetic_review_upserts_review_run_and_preserves_runtime_checks(tmp_path: Path) -> None:
    screenshot = tmp_path / "dashboard.png"
    screenshot.write_bytes(b"rendered-dashboard")
    candidate = _candidate(screenshot)
    candidate["measurement_protocol"]["production_review"] = {
        "schema_version": "legacy",
        "review_runs": [
            {
                "run_id": "visual-review-20260712",
                "source": "automated",
                "reviewer": "old-reviewer",
                "custom_field": "preserve-on-upsert",
            }
        ],
        "runtime_checks": [{"kind": "interaction", "status": "passed"}],
    }
    artifact = _artifact(screenshot, metrics={"domain_fit": 9.3})
    artifact_path = tmp_path / "review.json"
    _write_json(artifact_path, artifact)

    merged = apply_aesthetic_review(
        candidate,
        artifact,
        review_artifact_path=artifact_path,
        reviewer="codex-visual-qa",
        model="gpt-5-codex",
        method="Structured side-by-side multimodal review",
    )

    production_review = merged["measurement_protocol"]["production_review"]
    assert production_review["schema_version"] == "production-ui-review/v1"
    assert production_review["runtime_checks"] == [
        {"kind": "interaction", "status": "passed"}
    ]
    assert len(production_review["review_runs"]) == 1
    assert production_review["review_runs"][0]["source"] == "multimodal-review"
    assert production_review["review_runs"][0]["custom_field"] == "preserve-on-upsert"


def test_cli_apply_aesthetic_review_writes_the_merged_candidate(tmp_path: Path) -> None:
    screenshot = tmp_path / "dashboard.png"
    screenshot.write_bytes(b"rendered-dashboard")
    candidate = _candidate(screenshot)
    artifact = _artifact(screenshot, metrics={"domain_fit": 9.3})
    candidate_path = tmp_path / "candidate.json"
    artifact_path = tmp_path / "review.json"
    output_path = tmp_path / "output" / "reviewed-candidate.json"
    _write_json(candidate_path, candidate)
    _write_json(artifact_path, artifact)

    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "design_ontology_harness.cli",
            "apply-aesthetic-review",
            "--candidate",
            str(candidate_path),
            "--review-artifact",
            str(artifact_path),
            "--output",
            str(output_path),
            "--reviewer",
            "codex-visual-qa",
            "--model",
            "gpt-5-codex",
            "--method",
            "Structured multimodal review",
            "--json",
        ],
        cwd=REPO_ROOT,
        text=True,
        capture_output=True,
        check=False,
    )

    assert result.returncode == 0, result.stderr
    payload = json.loads(result.stdout)
    assert payload["iterations"][1]["metrics"]["domain_fit"] == 9.3
    assert output_path.exists()
    assert json.loads(output_path.read_text(encoding="utf-8")) == payload
