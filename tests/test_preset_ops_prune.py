"""Phase 15-4: prune-preset lifecycle tests.

Tests scaffold a throwaway `presets/` under tmp_path by copying a real preset,
then exercise the four pruning gates (deprecated / age / zero-hits / confirm)
plus the actual deletion of directory + matrix entry + snapshot fixture entry.
"""

from __future__ import annotations

import json
import shutil
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from design_ontology_harness import catalog_health
from design_ontology_harness.preset_ops import (
    deprecate_preset,
    find_prune_eligible,
    format_prune_report,
    prune_preset,
)


PRIMARY_PRESET = "dashboard--minimal-tech"
REAL_PRESETS = REPO_ROOT / "presets"


def _scaffold_root(tmp_path: Path, *, preset_id: str = PRIMARY_PRESET) -> Path:
    root = tmp_path / "presets"
    root.mkdir(parents=True)
    shutil.copytree(REAL_PRESETS / preset_id, root / preset_id)
    shutil.copy2(REAL_PRESETS / "compatibility.json", root / "compatibility.json")
    matrix = json.loads((REAL_PRESETS / "matrix.json").read_text(encoding="utf-8"))
    matrix["presets"] = [
        entry for entry in matrix.get("presets", [])
        if entry.get("id") == preset_id
    ]
    (root / "matrix.json").write_text(
        json.dumps(matrix, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    metrics_dir = root / ".metrics"
    metrics_dir.mkdir()
    (metrics_dir / "install_hits.json").write_text("{}", encoding="utf-8")
    (metrics_dir / "match_hits.json").write_text("{}", encoding="utf-8")

    return root


def _write_snapshot_fixture(tmp_path: Path, preset_id: str) -> Path:
    path = tmp_path / "preset_snapshots.json"
    path.write_text(
        json.dumps({preset_id: "sha256:placeholder"}, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    return path


def _set_deprecated_at(root: Path, preset_id: str, *, days_ago: int, reason: str = "zero_hits") -> str:
    manifest_path = root / preset_id / "manifest.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    ts = datetime.now(timezone.utc) - timedelta(days=days_ago)
    iso = ts.strftime("%Y-%m-%dT%H:%M:%SZ")
    manifest["deprecated_at"] = iso
    manifest["deprecation_reason"] = reason
    manifest_path.write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    return iso


def test_prune_happy_path_deprecated_and_aged(tmp_path: Path):
    root = _scaffold_root(tmp_path)
    snapshot = _write_snapshot_fixture(tmp_path, PRIMARY_PRESET)
    _set_deprecated_at(root, PRIMARY_PRESET, days_ago=120)

    report = prune_preset(
        PRIMARY_PRESET,
        confirm=True,
        dry_run=False,
        presets_root=root,
        snapshot_fixture_path=snapshot,
    )

    assert report.ok, format_prune_report(report)
    assert report.deleted is True
    assert report.deleted_at is not None
    # directory removed
    assert not (root / PRIMARY_PRESET).exists()
    # matrix entry removed
    matrix = json.loads((root / "matrix.json").read_text(encoding="utf-8"))
    assert all(entry["id"] != PRIMARY_PRESET for entry in matrix.get("presets", []))
    # snapshot fixture entry removed
    snapshot_data = json.loads(snapshot.read_text(encoding="utf-8"))
    assert PRIMARY_PRESET not in snapshot_data


def test_prune_blocks_when_not_deprecated(tmp_path: Path):
    root = _scaffold_root(tmp_path)
    report = prune_preset(PRIMARY_PRESET, presets_root=root)
    assert not report.ok
    deprecated_check = next(c for c in report.checks if c.name == "deprecated")
    assert not deprecated_check.passed
    # Directory still present.
    assert (root / PRIMARY_PRESET).is_dir()


def test_prune_blocks_when_under_age(tmp_path: Path):
    root = _scaffold_root(tmp_path)
    _set_deprecated_at(root, PRIMARY_PRESET, days_ago=5)
    report = prune_preset(PRIMARY_PRESET, presets_root=root)
    assert not report.ok
    age_check = next(c for c in report.checks if c.name == "age")
    assert not age_check.passed
    assert "remaining" in age_check.detail
    assert (root / PRIMARY_PRESET).is_dir()


def test_prune_blocks_when_hits_present(tmp_path: Path):
    root = _scaffold_root(tmp_path)
    _set_deprecated_at(root, PRIMARY_PRESET, days_ago=120)
    # Seed install hits so zero-hits gate fails.
    (root / ".metrics" / "install_hits.json").write_text(
        json.dumps({PRIMARY_PRESET: 3}),
        encoding="utf-8",
    )
    report = prune_preset(PRIMARY_PRESET, presets_root=root)
    assert not report.ok
    hits_check = next(c for c in report.checks if c.name == "zero-hits")
    assert not hits_check.passed
    assert (root / PRIMARY_PRESET).is_dir()


def test_prune_blocks_without_confirm_when_not_dry_run(tmp_path: Path):
    root = _scaffold_root(tmp_path)
    _set_deprecated_at(root, PRIMARY_PRESET, days_ago=120)
    report = prune_preset(
        PRIMARY_PRESET,
        confirm=False,
        dry_run=False,
        presets_root=root,
    )
    assert not report.ok
    confirm_check = next(c for c in report.checks if c.name == "confirm")
    assert not confirm_check.passed
    assert (root / PRIMARY_PRESET).is_dir()


def test_prune_dry_run_passes_all_gates_without_mutation(tmp_path: Path):
    root = _scaffold_root(tmp_path)
    snapshot = _write_snapshot_fixture(tmp_path, PRIMARY_PRESET)
    _set_deprecated_at(root, PRIMARY_PRESET, days_ago=120)

    manifest_before = (root / PRIMARY_PRESET / "manifest.json").read_text(encoding="utf-8")
    matrix_before = (root / "matrix.json").read_text(encoding="utf-8")
    snapshot_before = snapshot.read_text(encoding="utf-8")

    report = prune_preset(
        PRIMARY_PRESET,
        confirm=False,
        dry_run=True,
        presets_root=root,
        snapshot_fixture_path=snapshot,
    )
    assert report.ok, format_prune_report(report)
    assert report.deleted is False
    # nothing on disk changed
    assert (root / PRIMARY_PRESET / "manifest.json").read_text(encoding="utf-8") == manifest_before
    assert (root / "matrix.json").read_text(encoding="utf-8") == matrix_before
    assert snapshot.read_text(encoding="utf-8") == snapshot_before


def test_prune_min_age_override_zero_accepts_fresh_deprecation(tmp_path: Path):
    root = _scaffold_root(tmp_path)
    snapshot = _write_snapshot_fixture(tmp_path, PRIMARY_PRESET)
    # Fresh deprecation (0 days old) — only passes when min_deprecated_age_days=0.
    _set_deprecated_at(root, PRIMARY_PRESET, days_ago=0)

    report = prune_preset(
        PRIMARY_PRESET,
        confirm=False,
        dry_run=True,
        min_deprecated_age_days=0,
        presets_root=root,
        snapshot_fixture_path=snapshot,
    )
    assert report.ok, format_prune_report(report)


def test_find_prune_eligible_lists_only_aged_zero_hit_deprecated(tmp_path: Path):
    root = _scaffold_root(tmp_path)
    _set_deprecated_at(root, PRIMARY_PRESET, days_ago=120)
    eligible = find_prune_eligible(presets_root=root)
    assert eligible == [PRIMARY_PRESET]

    # Under-age: not eligible even when deprecated.
    root2 = _scaffold_root(tmp_path / "case2")
    _set_deprecated_at(root2, PRIMARY_PRESET, days_ago=10)
    eligible_under = find_prune_eligible(presets_root=root2)
    assert eligible_under == []


def test_catalog_health_surfaces_prune_eligible(tmp_path: Path):
    root = _scaffold_root(tmp_path)
    _set_deprecated_at(root, PRIMARY_PRESET, days_ago=120)

    pyproject = tmp_path / "pyproject.toml"
    pyproject.write_text('[project]\nname="x"\nversion = "0.1.0"\n', encoding="utf-8")

    report = catalog_health.compute_health(
        presets_root=root,
        snapshot_fixture_path=tmp_path / "missing_snapshot.json",
        pyproject_path=pyproject,
    )
    assert report["prune_eligible_count"] == 1
    ids = {p["preset_id"] for p in report["prune_eligible_presets"]}
    assert PRIMARY_PRESET in ids

    md = catalog_health.format_markdown(report)
    assert "## Prune Eligible" in md
    assert PRIMARY_PRESET in md
