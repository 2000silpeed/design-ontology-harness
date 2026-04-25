"""Phase 15-2: promote-preset lifecycle tests.

Each test scaffolds a throwaway `presets/` under tmp_path by copying a single
real preset + matrix.json + compatibility.json, then rewriting the copied
tier so there is room to promote. This exercises the full gate stack
(validate → lint → adapter round-trip → sources → self-match) against
realistic inputs without touching the shared repo state.
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

from design_ontology_harness import preset_ops as preset_ops_module
from design_ontology_harness.preset_ops import (
    GateResult,
    format_promote_report,
    promote_preset,
)


SOURCE_PRESET = "dashboard--minimal-tech"
REAL_PRESETS = REPO_ROOT / "presets"


def _scaffold_root(tmp_path: Path, *, tier: str = "P3") -> Path:
    root = tmp_path / "presets"
    root.mkdir()

    shutil.copytree(REAL_PRESETS / SOURCE_PRESET, root / SOURCE_PRESET)
    shutil.copy2(REAL_PRESETS / "compatibility.json", root / "compatibility.json")

    matrix = json.loads((REAL_PRESETS / "matrix.json").read_text(encoding="utf-8"))
    matrix["presets"] = [
        {**entry, "tier": tier}
        for entry in matrix.get("presets", [])
        if entry.get("id") == SOURCE_PRESET
    ]
    (root / "matrix.json").write_text(
        json.dumps(matrix, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    manifest_path = root / SOURCE_PRESET / "manifest.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    manifest["tier"] = tier
    manifest_path.write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    # P3 promotions gate sources.json strictly; provide a stub that matches
    # the Phase 15-9 schema so the happy path reaches the self-match step.
    (root / SOURCE_PRESET / "sources.json").write_text(
        json.dumps(
            {
                "preset_id": SOURCE_PRESET,
                "source_project": "orbit",
                "seeds": [
                    {
                        "url": "https://example.com/kb-seed",
                        "kind": "design-system",
                        "title": "Example KB Seed",
                        "notes": "stub for promote-preset test",
                    }
                ],
                "pretendard_font_license": "SIL OFL 1.1",
                "created_at": "2026-04-20T00:00:00Z",
            },
            ensure_ascii=False,
            indent=2,
        ),
        encoding="utf-8",
    )

    return root


def test_promote_p3_to_p2_happy_path(tmp_path: Path):
    root = _scaffold_root(tmp_path, tier="P3")
    report = promote_preset(SOURCE_PRESET, target_tier="P2", presets_root=root)

    assert report.ok, format_promote_report(report)
    assert report.from_tier == "P3"
    assert report.target_tier == "P2"
    assert report.promoted_at is not None
    assert not report.dry_run

    manifest = json.loads((root / SOURCE_PRESET / "manifest.json").read_text(encoding="utf-8"))
    assert manifest["tier"] == "P2"
    assert manifest["promoted_from"] == "P3"
    assert manifest["promoted_at"] == report.promoted_at

    matrix = json.loads((root / "matrix.json").read_text(encoding="utf-8"))
    entry = next(p for p in matrix["presets"] if p["id"] == SOURCE_PRESET)
    assert entry["tier"] == "P2"

    gate_names = {g.name for g in report.gates}
    assert {"validate-presets", "lint-previews", "adapter-round-trip", "sources.json", "self-match"} == gate_names


def test_promote_dry_run_runs_gates_but_leaves_files_untouched(tmp_path: Path):
    root = _scaffold_root(tmp_path, tier="P3")
    manifest_before = (root / SOURCE_PRESET / "manifest.json").read_text(encoding="utf-8")
    matrix_before = (root / "matrix.json").read_text(encoding="utf-8")

    report = promote_preset(
        SOURCE_PRESET,
        target_tier="P2",
        dry_run=True,
        presets_root=root,
    )

    assert report.ok
    assert report.dry_run
    assert report.promoted_at is None
    assert (root / SOURCE_PRESET / "manifest.json").read_text(encoding="utf-8") == manifest_before
    assert (root / "matrix.json").read_text(encoding="utf-8") == matrix_before


def test_promote_blocked_when_validate_fails(tmp_path: Path):
    root = _scaffold_root(tmp_path, tier="P3")
    manifest_path = root / SOURCE_PRESET / "manifest.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    # Drop owner — validate-presets flags this as an error.
    del manifest["owner"]
    manifest_path.write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    report = promote_preset(SOURCE_PRESET, target_tier="P2", presets_root=root)
    assert not report.ok
    gates = {g.name: g for g in report.gates}
    assert not gates["validate-presets"].passed
    # Post-conditions: manifest tier unchanged on disk.
    manifest_now = json.loads(manifest_path.read_text(encoding="utf-8"))
    assert manifest_now["tier"] == "P3"


def test_promote_blocked_when_self_match_fails(tmp_path: Path, monkeypatch):
    root = _scaffold_root(tmp_path, tier="P3")

    def _fail_self_match(*_args, **_kwargs):
        return GateResult(
            "self-match",
            False,
            f"Top-1 is other--preset (expected {SOURCE_PRESET})",
        )

    monkeypatch.setattr(preset_ops_module, "_self_match_gate", _fail_self_match)
    report = promote_preset(SOURCE_PRESET, target_tier="P2", presets_root=root)

    assert not report.ok
    gates = {g.name: g for g in report.gates}
    assert not gates["self-match"].passed
    manifest = json.loads((root / SOURCE_PRESET / "manifest.json").read_text(encoding="utf-8"))
    assert manifest["tier"] == "P3"


def test_promote_usage_error_when_already_top_tier(tmp_path: Path):
    root = _scaffold_root(tmp_path, tier="P0")
    report = promote_preset(SOURCE_PRESET, presets_root=root)  # no --target → bump
    assert not report.ok
    assert report.error is not None
    assert "top" in report.error or "nothing to promote" in report.error


def test_promote_rejects_downward_target(tmp_path: Path):
    root = _scaffold_root(tmp_path, tier="P1")
    report = promote_preset(SOURCE_PRESET, target_tier="P2", presets_root=root)
    assert not report.ok
    assert report.error is not None
    assert "not above" in report.error
