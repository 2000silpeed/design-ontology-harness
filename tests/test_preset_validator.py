"""Phase 15-7: preset_validator adapter-version cross-check tests.

Validates that `validate_all` flags adapter drift:
- preset range contains current adapter version → OK
- preset range excludes current adapter version → ERROR
- malformed range → ERROR (existing behaviour, guarded against regression)
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

from design_ontology_harness.preset_validator import validate_all


SOURCE_PRESET = "dashboard--minimal-tech"
REAL_PRESETS = REPO_ROOT / "presets"


def _scaffold_preset_root(tmp_path: Path, *, adapter_range: str) -> Path:
    root = tmp_path / "presets"
    root.mkdir()
    shutil.copytree(REAL_PRESETS / SOURCE_PRESET, root / SOURCE_PRESET)
    shutil.copy2(REAL_PRESETS / "compatibility.json", root / "compatibility.json")
    matrix = json.loads((REAL_PRESETS / "matrix.json").read_text(encoding="utf-8"))
    matrix["presets"] = [
        entry for entry in matrix.get("presets", []) if entry.get("id") == SOURCE_PRESET
    ]
    (root / "matrix.json").write_text(
        json.dumps(matrix, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    manifest_path = root / SOURCE_PRESET / "manifest.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    manifest["adapter_compatibility"] = {"nextjs-tailwind-shadcn": adapter_range}
    manifest_path.write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    return root


def test_adapter_version_in_range_passes(tmp_path: Path):
    root = _scaffold_preset_root(tmp_path, adapter_range=">=0.1.0 <1.0.0")
    report = validate_all(
        root, adapter_versions={"nextjs-tailwind-shadcn": "0.1.0"}
    )
    drift_errors = [e for e in report.errors if "outside range" in e]
    assert drift_errors == []


def test_adapter_version_outside_range_flags_error(tmp_path: Path):
    root = _scaffold_preset_root(tmp_path, adapter_range=">=0.1.0 <1.0.0")
    report = validate_all(
        root, adapter_versions={"nextjs-tailwind-shadcn": "1.0.0"}
    )
    drift_errors = [
        e for e in report.errors if f"[{SOURCE_PRESET}]" in e and "outside range" in e
    ]
    assert len(drift_errors) == 1
    assert "current=1.0.0" in drift_errors[0]


def test_malformed_adapter_range_errors(tmp_path: Path):
    root = _scaffold_preset_root(tmp_path, adapter_range="not-a-range")
    report = validate_all(
        root, adapter_versions={"nextjs-tailwind-shadcn": "0.1.0"}
    )
    invalid_range_errors = [
        e for e in report.errors
        if "invalid range" in e and f"[{SOURCE_PRESET}]" in e
    ]
    assert len(invalid_range_errors) == 1


def test_real_catalog_clean_against_current_adapter_versions():
    """Guardrail: running validate_all on the shipped presets/ must not
    report adapter drift. This locks in the invariant that all 15 presets
    cover the currently registered adapter versions."""

    from design_ontology_harness.preset_builder import PRESETS_ROOT

    report = validate_all(PRESETS_ROOT)
    drift_errors = [e for e in report.errors if "outside range" in e]
    assert drift_errors == [], drift_errors
