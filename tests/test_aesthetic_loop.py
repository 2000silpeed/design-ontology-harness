from __future__ import annotations

import subprocess
import sys
from pathlib import Path

from design_ontology_harness.aesthetic_loop import (
    AESTHETIC_CANDIDATE_TEMPLATE_RELATIVE_PATH,
    AESTHETIC_LATEST_REPORT_RELATIVE_PATH,
    AESTHETIC_LOOP_POLICY_RELATIVE_PATH,
    AESTHETIC_ONTOLOGY_RELATIVE_PATH,
    DEFAULT_METRICS,
    build_aesthetic_ontology,
    run_self_improvement_loop,
    write_aesthetic_project_artifacts,
)
from design_ontology_harness.utils import write_json


REPO_ROOT = Path(__file__).resolve().parent.parent


def _metrics(value: float) -> dict[str, float]:
    return {metric_id: value for metric_id in DEFAULT_METRICS}


def test_aesthetic_loop_passes_when_overall_and_dimensions_clear_threshold():
    ontology = build_aesthetic_ontology({"brand_name": "Signal Desk"})
    candidate = {
        "design_id": "landing-v3",
        "score_scale": 10,
        "metrics": _metrics(9.0),
    }

    report = run_self_improvement_loop(candidate, ontology, threshold=0.82)

    assert report["passed"]
    assert report["ready_to_execute"]
    assert report["execution_gate"]["state"] == "open"
    assert report["selected_iteration"] == "iteration-1"
    assert report["iterations"][0]["score_100"] == 90.0


def test_aesthetic_loop_blocks_and_returns_action_brief_for_weak_candidate():
    ontology = build_aesthetic_ontology({"brand_name": "Signal Desk"})
    metrics = _metrics(8.0)
    metrics["hierarchy_clarity"] = 3.0
    metrics["task_focus"] = 3.0
    candidate = {
        "design_id": "landing-v3",
        "score_scale": 10,
        "metrics": metrics,
    }

    report = run_self_improvement_loop(candidate, ontology, threshold=0.82)

    assert not report["passed"]
    assert not report["ready_to_execute"]
    assert report["execution_gate"]["state"] == "blocked"
    assert report["next_iteration_brief"]
    action_ids = {action["action_id"] for action in report["next_iteration_brief"]["actions"]}
    assert "clarity:hierarchy_clarity" in action_ids
    assert "clarity:task_focus" in action_ids


def test_aesthetic_loop_uses_later_candidate_iteration_as_real_pass():
    ontology = build_aesthetic_ontology({"brand_name": "Signal Desk"})
    candidate = {
        "design_id": "landing-v3",
        "score_scale": 10,
        "iterations": [
            {"iteration_id": "v1", "metrics": _metrics(5.0)},
            {"iteration_id": "v2", "metrics": _metrics(9.0)},
        ],
    }

    report = run_self_improvement_loop(candidate, ontology, threshold=0.82, max_iterations=3)

    assert report["passed"]
    assert report["selected_iteration"] == "v2"
    assert [item["iteration_id"] for item in report["iterations"]] == ["v1", "v2"]


def test_aesthetic_loop_recommends_actions_when_average_is_below_threshold_only():
    ontology = build_aesthetic_ontology({"brand_name": "Signal Desk"})
    candidate = {
        "design_id": "landing-v3",
        "score_scale": 10,
        "metrics": _metrics(7.6),
    }

    report = run_self_improvement_loop(candidate, ontology, threshold=0.82)

    assert not report["passed"]
    assert report["next_iteration_brief"]["actions"]


def test_brand_profile_generates_brand_owned_aesthetic_metrics():
    ontology = build_aesthetic_ontology(
        {
            "brand_name": "Alley Sense",
            "brand_keywords": ["quiet", "sensory"],
            "anti_keywords": ["generic-map"],
            "product_primitives": ["map pin layer"],
            "audiences": ["서울 산책자"],
            "accessibility_targets": ["WCAG 2.2 AA"],
            "visual_reference": {
                "must_include": ["sensory metadata visible on cards"],
                "avoid_patterns": ["photo feed dominance"],
            },
        }
    )

    dimension_ids = {dimension["id"] for dimension in ontology["dimensions"]}
    metric_ids = set(ontology["metrics"])

    assert "brand_semantic_fit" in dimension_ids
    assert "brand_boundary_fit" in dimension_ids
    assert "product_ontology_fit" in dimension_ids
    assert "audience_context_fit" in dimension_ids
    assert any(metric_id.startswith("brand_keyword:quiet") for metric_id in metric_ids)
    assert any(metric_id.startswith("anti_keyword:generic-map") for metric_id in metric_ids)
    assert any(metric_id.startswith("product_primitive:map-pin-layer") for metric_id in metric_ids)


def test_write_aesthetic_project_artifacts_creates_ontology_template_and_policy(tmp_path: Path):
    output_dir = tmp_path / "build" / "system"
    paths = write_aesthetic_project_artifacts(
        output_dir,
        {
            "brand_name": "Signal Desk",
            "system_name": "Signal Desk System",
            "product_summary": "Decision dashboard",
        },
    )

    assert Path(paths["ontology_path"]) == output_dir / AESTHETIC_ONTOLOGY_RELATIVE_PATH
    assert Path(paths["candidate_template_path"]) == output_dir / AESTHETIC_CANDIDATE_TEMPLATE_RELATIVE_PATH
    assert Path(paths["loop_policy_path"]) == output_dir / AESTHETIC_LOOP_POLICY_RELATIVE_PATH
    assert (output_dir / AESTHETIC_ONTOLOGY_RELATIVE_PATH).exists()
    template = (output_dir / AESTHETIC_CANDIDATE_TEMPLATE_RELATIVE_PATH).read_text(encoding="utf-8")
    assert "hierarchy_clarity" in template
    assert "Signal Desk System" in template


def test_cli_aesthetic_loop_exits_nonzero_before_execution_when_blocked(tmp_path: Path):
    candidate = tmp_path / "candidate.json"
    marker = tmp_path / "should-not-exist.txt"
    write_json(
        candidate,
        {
            "design_id": "landing-v3",
            "score_scale": 10,
            "metrics": _metrics(4.0),
        },
    )

    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "design_ontology_harness.cli",
            "aesthetic-loop",
            "--candidate",
            str(candidate),
            "--threshold",
            "0.82",
            "--execute-command",
            f"{sys.executable} -c \"from pathlib import Path; Path('{marker}').write_text('ran')\"",
        ],
        cwd=REPO_ROOT,
        text=True,
        capture_output=True,
        check=False,
    )

    assert result.returncode == 1
    assert "Aesthetic self-improvement loop: BLOCKED" in result.stdout
    assert not marker.exists()


def test_cli_aesthetic_loop_project_dir_uses_default_candidate_and_writes_report(tmp_path: Path):
    project_dir = tmp_path / "project"
    output_dir = project_dir / "build" / "system"
    project_dir.mkdir()
    (output_dir / "aesthetic").mkdir(parents=True)
    write_json(
        project_dir / "project_manifest.json",
        {
            "brand_profile": "brand_profile.json",
            "build_dir": "build",
            "kb_dir": None,
        },
    )
    write_json(
        project_dir / "brand_profile.json",
        {
            "brand_name": "Signal Desk",
            "system_name": "Signal Desk System",
            "product_summary": "Decision dashboard",
        },
    )
    write_aesthetic_project_artifacts(
        output_dir,
        {
            "brand_name": "Signal Desk",
            "system_name": "Signal Desk System",
            "product_summary": "Decision dashboard",
        },
    )
    write_json(
        output_dir / "aesthetic" / "candidate.json",
        {
            "design_id": "landing-v3",
            "score_scale": 10,
            "metrics": _metrics(9.0),
        },
    )

    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "design_ontology_harness.cli",
            "aesthetic-loop",
            "--project-dir",
            str(project_dir),
            "--threshold",
            "0.82",
        ],
        cwd=REPO_ROOT,
        text=True,
        capture_output=True,
        check=False,
    )

    assert result.returncode == 0
    assert "Aesthetic self-improvement loop: PASS" in result.stdout
    report_path = output_dir / AESTHETIC_LATEST_REPORT_RELATIVE_PATH
    assert report_path.exists()
    assert '"ready_to_execute": true' in report_path.read_text(encoding="utf-8")
