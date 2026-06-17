"""Tests for the image-first site design workflow (scaffold + check)."""

from __future__ import annotations

import json
from pathlib import Path

from design_ontology_harness.site_design import (
    WORKFLOW_ID,
    check_site_design,
    scaffold_site_design_project,
)


def _scaffold(tmp_path: Path) -> Path:
    project_dir = tmp_path / "demo"
    scaffold_site_design_project(
        project_dir=project_dir,
        brand_name="Demo",
        product_summary="A demo product",
        concept="Test Concept",
        surfaces=["landing", "detail"],
    )
    return project_dir


def test_scaffold_creates_expected_structure(tmp_path: Path) -> None:
    project_dir = _scaffold(tmp_path)

    manifest = json.loads((project_dir / "project_manifest.json").read_text())
    assert manifest["workflow"] == WORKFLOW_ID
    assert manifest["image_model"] == "gpt_image_2"

    for name in ("concept_brief.md", "color_set.json", "screen_plan.json"):
        assert (project_dir / name).exists()
    assert (project_dir / "generated").is_dir()
    assert (project_dir / "design-system").is_dir()

    plan = json.loads((project_dir / "screen_plan.json").read_text())
    surfaces = [s["surface"] for s in plan["screens"]]
    assert surfaces == ["landing", "detail"]


def test_check_fails_before_screens_and_system(tmp_path: Path) -> None:
    project_dir = _scaffold(tmp_path)
    report = check_site_design(project_dir, repo_root=tmp_path)
    # No generated images and no derived token_schema yet.
    assert not report.ok
    assert any("no local image" in e or "no remote provenance" in e for e in report.errors)
    assert any("token_schema.json" in e for e in report.errors)


def test_remote_provenance_satisfies_screen_evidence(tmp_path: Path) -> None:
    project_dir = _scaffold(tmp_path)

    plan = json.loads((project_dir / "screen_plan.json").read_text())
    for screen in plan["screens"]:
        screen["url"] = "https://cdn.example/" + screen["surface"] + ".png"
        screen["job_id"] = "00000000-0000-4000-8000-000000000000"
        screen["prompt"] = "a prompt"
    (project_dir / "screen_plan.json").write_text(json.dumps(plan))

    # Minimal derived system grounded in the color set.
    color_set = json.loads((project_dir / "color_set.json").read_text())
    color_set["candidates"][0]["roles"]["dominant"]["hex"] = "#2F4733"
    (project_dir / "color_set.json").write_text(json.dumps(color_set))

    ds = project_dir / "design-system"
    (ds / "token_schema.json").write_text(
        json.dumps({"color": {"brand": {"forest": {"value": "#2F4733"}}}})
    )
    (ds / "component_inventory.json").write_text(json.dumps({"families": []}))
    (ds / "system_spec.md").write_text("# spec")
    (ds / "STYLE.md").write_text("# style")

    report = check_site_design(project_dir, repo_root=tmp_path)
    assert report.ok, report.errors
    assert any("remote provenance" in w for w in report.warnings)


def test_copied_tokens_from_existing_source_are_flagged(tmp_path: Path) -> None:
    project_dir = _scaffold(tmp_path)

    plan = json.loads((project_dir / "screen_plan.json").read_text())
    for screen in plan["screens"]:
        screen["url"] = "https://cdn.example/x.png"
        screen["job_id"] = "00000000-0000-4000-8000-000000000000"
    (project_dir / "screen_plan.json").write_text(json.dumps(plan))

    copied = {"#112233", "#445566", "#778899"}
    # An existing preset with the same colors.
    preset_dir = tmp_path / "presets" / "some-preset"
    preset_dir.mkdir(parents=True)
    (preset_dir / "token_schema.json").write_text(
        json.dumps({"color": {c: c for c in copied}})
    )

    ds = project_dir / "design-system"
    (ds / "token_schema.json").write_text(json.dumps({"color": {c: c for c in copied}}))
    (ds / "component_inventory.json").write_text(json.dumps({"families": []}))
    (ds / "system_spec.md").write_text("# spec")
    (ds / "STYLE.md").write_text("# style")

    report = check_site_design(project_dir, repo_root=tmp_path)
    assert not report.ok
    assert any("copied from a test case" in e for e in report.errors)
