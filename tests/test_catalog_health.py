"""Phase 15-1: catalog_health unit tests with synthesized fixtures."""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from design_ontology_harness import catalog_health


PREVIEW_OK = """# {preset_id}

## 어떤 제품에 맞나
- fixture {preset_id}

## Color Tokens (light + dark)
### Core
- primary: `#112233`
- accent: `#445566`
- surface_tint: `#778899`

### Semantic
- success: `#4A7C59`
- warning: `#CC7722`
- danger: `#8B2252`
- info: `#708090`

## Typography
- heading: Pretendard
- body: Pretendard
- mono: JetBrains Mono
- korean: Pretendard

## 대표 컴포넌트
- **alpha** — parts: container | states: default
- **beta** — parts: container | states: default
- **gamma** — parts: container | states: default

## 주의사항
- fixture
"""


def _write_preset(
    root: Path,
    preset_id: str,
    *,
    app_mode: str,
    brand_tone: str,
    tier: str,
    tags: list[str],
    harness_version: str,
    content_hash: str,
    generated_at: str = "2026-04-20T00:00:00Z",
    preview_text: str | None = None,
) -> dict:
    preset_dir = root / preset_id
    preset_dir.mkdir(parents=True, exist_ok=True)
    manifest = {
        "id": preset_id,
        "schema_version": "1.0.0",
        "preset_api_version": "1.0.0",
        "generated_by_harness_version": harness_version,
        "preview_version": "1.0.0",
        "adapter_compatibility": {
            "nextjs-tailwind-shadcn": ">=0.1.0 <1.0.0",
        },
        "source_project": "fixture",
        "content_hash": content_hash,
        "app_mode": app_mode,
        "brand_tone": brand_tone,
        "color_modes": ["light", "dark"],
        "default_color_mode": "light",
        "tags": tags,
        "locale_pairings": {},
        "owner": "@fixture",
        "tier": tier,
        "generated_at": generated_at,
        "description": "fixture preset",
    }
    (preset_dir / "manifest.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    (preset_dir / "preview.md").write_text(
        preview_text if preview_text is not None else PREVIEW_OK.format(preset_id=preset_id),
        encoding="utf-8",
    )
    (preset_dir / "system_spec.md").write_text("# fixture\n", encoding="utf-8")
    (preset_dir / "token_schema.json").write_text("{}", encoding="utf-8")
    return manifest


def _write_matrix(root: Path, entries: list[dict]) -> None:
    matrix = {
        "matrix_version": "1.0.0",
        "app_modes": [],
        "brand_tones": [],
        "color_modes": ["light", "dark", "both"],
        "presets": entries,
    }
    (root / "matrix.json").write_text(
        json.dumps(matrix, ensure_ascii=False, indent=2), encoding="utf-8"
    )


def _matrix_entry(preset_id: str, app_mode: str, brand_tone: str, tier: str, tags: list[str]) -> dict:
    return {
        "id": preset_id,
        "app_mode": app_mode,
        "brand_tone": brand_tone,
        "color_modes": ["light", "dark"],
        "default_color_mode": "light",
        "tags": tags,
        "description": "fixture",
        "source_project": "fixture",
        "owner": "@fixture",
        "preview_path": f"presets/{preset_id}/preview.md",
        "locale_pairings": {},
        "tier": tier,
    }


def _make_pyproject(tmp_path: Path, version: str) -> Path:
    path = tmp_path / "pyproject.toml"
    path.write_text(f'[project]\nname = "x"\nversion = "{version}"\n', encoding="utf-8")
    return path


@pytest.fixture
def basic_root(tmp_path: Path) -> Path:
    root = tmp_path / "presets"
    root.mkdir()
    _write_preset(
        root,
        "dashboard--minimal-tech",
        app_mode="dashboard",
        brand_tone="minimal-tech",
        tier="P0",
        tags=["saas"],
        harness_version="0.3.0",
        content_hash="sha256:aaaa",
    )
    _write_preset(
        root,
        "commerce--editorial-warm",
        app_mode="commerce",
        brand_tone="editorial-warm",
        tier="P1",
        tags=["fashion"],
        harness_version="0.1.0",
        content_hash="sha256:bbbb",
    )
    _write_matrix(
        root,
        [
            _matrix_entry("dashboard--minimal-tech", "dashboard", "minimal-tech", "P0", ["saas"]),
            _matrix_entry("commerce--editorial-warm", "commerce", "editorial-warm", "P1", ["fashion"]),
        ],
    )
    return root


def test_aggregate_summary_counts(basic_root: Path, tmp_path: Path):
    pyproject = _make_pyproject(tmp_path, "0.3.0")
    report = catalog_health.compute_health(
        presets_root=basic_root,
        snapshot_fixture_path=tmp_path / "missing_snapshot.json",
        pyproject_path=pyproject,
    )
    assert report["preset_total"] == 2
    assert report["tier_counts"]["P0"] == 1
    assert report["tier_counts"]["P1"] == 1
    assert report["cell_coverage"]["total"] == 8 * 5
    assert report["cell_coverage"]["occupied"] == 2
    # Top-10 priority cells: none of them collide with our 2 fixtures →
    # all 10 should still be empty.
    assert len(report["priority_empty_cells_top10"]) == 10


def test_version_drift_calculation(basic_root: Path, tmp_path: Path):
    pyproject = _make_pyproject(tmp_path, "0.3.0")
    report = catalog_health.compute_health(
        presets_root=basic_root,
        snapshot_fixture_path=tmp_path / "missing_snapshot.json",
        pyproject_path=pyproject,
    )
    by_id = {p["preset_id"]: p for p in report["presets"]}
    # 0.3.0 vs 0.3.0 → drift 0
    assert by_id["dashboard--minimal-tech"]["version_drift_minor"] == 0
    # 0.3.0 vs 0.1.0 → drift 2
    assert by_id["commerce--editorial-warm"]["version_drift_minor"] == 2


def test_deprecation_candidates_zero_hits_plus_drift(basic_root: Path, tmp_path: Path):
    pyproject = _make_pyproject(tmp_path, "0.3.0")
    # No metrics file → install/match hits = 0; 0.1.0 vs 0.3.0 → drift = 2.
    report = catalog_health.compute_health(
        presets_root=basic_root,
        metrics_dir=tmp_path / "absent_metrics",
        snapshot_fixture_path=tmp_path / "missing_snapshot.json",
        pyproject_path=pyproject,
    )
    deprecated_ids = [p["preset_id"] for p in report["deprecation_candidates"]]
    # Both presets have zero hits AND one has drift 2 — both qualify.
    assert "commerce--editorial-warm" in deprecated_ids
    assert "dashboard--minimal-tech" in deprecated_ids
    commerce = next(p for p in report["deprecation_candidates"] if p["preset_id"] == "commerce--editorial-warm")
    assert "zero_hits" in commerce["deprecation_reasons"]
    assert any("version_drift_minor" in r for r in commerce["deprecation_reasons"])


def test_metrics_files_default_to_zero(basic_root: Path, tmp_path: Path):
    metrics = basic_root / ".metrics"
    metrics.mkdir()
    # install_hits records one preset, match_hits absent entirely.
    (metrics / "install_hits.json").write_text(
        json.dumps({"dashboard--minimal-tech": 5}), encoding="utf-8"
    )
    pyproject = _make_pyproject(tmp_path, "0.3.0")
    report = catalog_health.compute_health(
        presets_root=basic_root,
        snapshot_fixture_path=tmp_path / "missing_snapshot.json",
        pyproject_path=pyproject,
    )
    by_id = {p["preset_id"]: p for p in report["presets"]}
    assert by_id["dashboard--minimal-tech"]["install_hits"] == 5
    assert by_id["dashboard--minimal-tech"]["match_hits"] == 0
    assert by_id["commerce--editorial-warm"]["install_hits"] == 0
    # dashboard now has install_hits > 0 → no zero_hits trigger; drift 0; lint OK
    # → not a deprecation candidate.
    deprecated_ids = [p["preset_id"] for p in report["deprecation_candidates"]]
    assert "dashboard--minimal-tech" not in deprecated_ids


def test_snapshot_drift_detected(basic_root: Path, tmp_path: Path):
    snapshot = tmp_path / "snapshots.json"
    snapshot.write_text(
        json.dumps({"dashboard--minimal-tech": "sha256:DIFFERENT"}),
        encoding="utf-8",
    )
    pyproject = _make_pyproject(tmp_path, "0.3.0")
    report = catalog_health.compute_health(
        presets_root=basic_root,
        snapshot_fixture_path=snapshot,
        pyproject_path=pyproject,
    )
    by_id = {p["preset_id"]: p for p in report["presets"]}
    assert by_id["dashboard--minimal-tech"]["snapshot_drift"] is True
    # commerce--editorial-warm has no snapshot entry → no drift.
    assert by_id["commerce--editorial-warm"]["snapshot_drift"] is False
    assert report["snapshot_drift_count"] == 1


def test_format_markdown_smoke(basic_root: Path, tmp_path: Path):
    pyproject = _make_pyproject(tmp_path, "0.3.0")
    report = catalog_health.compute_health(
        presets_root=basic_root,
        snapshot_fixture_path=tmp_path / "missing_snapshot.json",
        pyproject_path=pyproject,
    )
    md = catalog_health.format_markdown(report)
    assert "# Catalog Health Report" in md
    assert "## Priority Empty Cells (Top-10)" in md
    assert "dashboard--minimal-tech" in md
    summary = catalog_health.format_summary(report)
    assert "[catalog-health]" in summary
    assert "셀 커버리지" in summary
