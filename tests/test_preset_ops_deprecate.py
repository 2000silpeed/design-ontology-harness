"""Phase 15-3: deprecate-preset lifecycle tests.

Covers manifest mutation, matcher hiding, --force behaviour, and
catalog_health reporting of deprecated entries.
"""

from __future__ import annotations

import json
import shutil
import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from design_ontology_harness import catalog_health
from design_ontology_harness.preset_matcher.engine import MatchQuery, match_presets
from design_ontology_harness.preset_ops import (
    deprecate_preset,
    format_deprecate_report,
)


PRIMARY_PRESET = "dashboard--minimal-tech"
REPLACEMENT_PRESET = "dashboard--corporate-trust"
REAL_PRESETS = REPO_ROOT / "presets"


def _copy_preset(src_root: Path, dst_root: Path, preset_id: str) -> None:
    shutil.copytree(src_root / preset_id, dst_root / preset_id)


def _scaffold_two_presets(tmp_path: Path) -> Path:
    root = tmp_path / "presets"
    root.mkdir()
    _copy_preset(REAL_PRESETS, root, PRIMARY_PRESET)
    _copy_preset(REAL_PRESETS, root, REPLACEMENT_PRESET)
    shutil.copy2(REAL_PRESETS / "compatibility.json", root / "compatibility.json")

    matrix = json.loads((REAL_PRESETS / "matrix.json").read_text(encoding="utf-8"))
    matrix["presets"] = [
        entry for entry in matrix.get("presets", [])
        if entry.get("id") in {PRIMARY_PRESET, REPLACEMENT_PRESET}
    ]
    (root / "matrix.json").write_text(
        json.dumps(matrix, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    return root


def test_deprecate_writes_manifest_fields(tmp_path: Path):
    root = _scaffold_two_presets(tmp_path)
    report = deprecate_preset(
        PRIMARY_PRESET,
        reason="manual:smoke test",
        replacement=REPLACEMENT_PRESET,
        presets_root=root,
    )
    assert report.ok, format_deprecate_report(report)
    assert report.deprecated_at is not None

    manifest = json.loads((root / PRIMARY_PRESET / "manifest.json").read_text(encoding="utf-8"))
    assert manifest["deprecated_at"] == report.deprecated_at
    assert manifest["deprecation_reason"] == "manual:smoke test"
    assert manifest["deprecated_replacement"] == REPLACEMENT_PRESET


def test_matcher_hides_deprecated_by_default(tmp_path: Path):
    root = _scaffold_two_presets(tmp_path)
    deprecate_preset(
        PRIMARY_PRESET,
        reason="zero_hits",
        replacement=REPLACEMENT_PRESET,
        presets_root=root,
    )

    matrix_path = root / "matrix.json"
    query = MatchQuery(app_mode="dashboard", brand_tone="minimal-tech", tags=["saas"])
    hidden = match_presets(query, matrix_path=matrix_path, top_k=5)
    assert all(r.preset_id != PRIMARY_PRESET for r in hidden)

    visible = match_presets(
        query,
        matrix_path=matrix_path,
        top_k=5,
        include_deprecated=True,
    )
    primary = next((r for r in visible if r.preset_id == PRIMARY_PRESET), None)
    assert primary is not None, "include_deprecated=True must surface deprecated preset"
    assert primary.deprecated is True
    assert primary.deprecated_replacement == REPLACEMENT_PRESET
    assert any("deprecated" in note for note in primary.rationale)


def test_deprecate_refuses_second_call_without_force(tmp_path: Path):
    root = _scaffold_two_presets(tmp_path)
    first = deprecate_preset(PRIMARY_PRESET, reason="zero_hits", presets_root=root)
    assert first.ok

    second = deprecate_preset(
        PRIMARY_PRESET,
        reason="manual:updated",
        presets_root=root,
    )
    assert not second.ok
    assert second.error is not None
    assert "already deprecated" in second.error

    forced = deprecate_preset(
        PRIMARY_PRESET,
        reason="manual:updated",
        force=True,
        presets_root=root,
    )
    assert forced.ok
    manifest = json.loads((root / PRIMARY_PRESET / "manifest.json").read_text(encoding="utf-8"))
    assert manifest["deprecation_reason"] == "manual:updated"


def test_deprecate_rejects_invalid_reason(tmp_path: Path):
    root = _scaffold_two_presets(tmp_path)
    report = deprecate_preset(
        PRIMARY_PRESET,
        reason="totally-bogus-reason",
        presets_root=root,
    )
    assert not report.ok
    assert "deprecation_reason" in (report.error or "")


def test_deprecate_rejects_missing_replacement(tmp_path: Path):
    root = _scaffold_two_presets(tmp_path)
    report = deprecate_preset(
        PRIMARY_PRESET,
        reason="zero_hits",
        replacement="does-not--exist",
        presets_root=root,
    )
    assert not report.ok
    assert "replacement preset not found" in (report.error or "")


def test_catalog_health_surfaces_deprecated(tmp_path: Path):
    root = _scaffold_two_presets(tmp_path)
    deprecate_preset(
        PRIMARY_PRESET,
        reason="snapshot_drift",
        replacement=REPLACEMENT_PRESET,
        presets_root=root,
    )
    pyproject = tmp_path / "pyproject.toml"
    pyproject.write_text('[project]\nname="x"\nversion = "0.1.0"\n', encoding="utf-8")

    report = catalog_health.compute_health(
        presets_root=root,
        snapshot_fixture_path=tmp_path / "missing_snapshot.json",
        pyproject_path=pyproject,
    )
    assert report["deprecated_count"] == 1
    deprecated_ids = {p["preset_id"] for p in report["deprecated_presets"]}
    assert PRIMARY_PRESET in deprecated_ids
    # An already-deprecated preset should NOT re-appear in candidate list.
    candidate_ids = {p["preset_id"] for p in report["deprecation_candidates"]}
    assert PRIMARY_PRESET not in candidate_ids

    md = catalog_health.format_markdown(report)
    assert "## Deprecated" in md
    assert PRIMARY_PRESET in md
    assert "snapshot_drift" in md
