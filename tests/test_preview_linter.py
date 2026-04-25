"""Phase 12A-2: preview.md linter tests.

Covers:
- P0 5종: errors=[] (current builder output must pass cleanly)
- Synthetic broken previews injected under tmp_path for each rule:
  E001/E002/E003/E004/E005/E006/E007/E008/W001/W002/W003
- CLI: `design-ontology lint-previews --preset-id ...` exits 0 on OK
"""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from design_ontology_harness.preview_linter import (
    lint_all_previews,
    lint_preview,
)

PRESETS_ROOT = REPO_ROOT / "presets"

P0_IDS = {
    "commerce--editorial-warm",
    "conversation-copilot--minimal-tech",
    "dashboard--minimal-tech",
    "document-content--editorial-warm",
    "marketing-landing--bold-confident",
}

_BASE_MANIFEST = {
    "id": "dashboard--minimal-tech",
    "app_mode": "dashboard",
    "brand_tone": "minimal-tech",
    "color_modes": ["light", "dark"],
    "default_color_mode": "light",
    "tags": ["saas", "ko"],
    "locale_pairings": {
        "ko": {"heading_font": "Pretendard", "body_font": "Pretendard"}
    },
}

_CLEAN_PREVIEW = """# dashboard--minimal-tech

## 어떤 제품에 맞나
- SaaS 운영 대시보드

- app_mode: `dashboard` / brand_tone: `minimal-tech`

## Color Tokens (light + dark)
### Core
- primary: `#0A7CFF`
- accent: `#6366F1`
- surface_tint: `#FFFFFF`

### Semantic
- success: `#22C55E`
- warning: `#F59E0B`
- danger: `#EF4444`
- info: `#3B82F6`

## Typography
- heading: Inter
- body: Inter
- mono: JetBrains Mono
- korean: Pretendard

## 대표 컴포넌트
- **DataTable** — parts: header, row
- **KpiCard** — parts: container, value
- **SidebarNav** — parts: container, item

## 주의사항
- editorial 톤에는 editorial-warm 계열 권장
- 랜딩에는 부적합
"""


def _write_preset(
    tmp_path: Path,
    *,
    preset_id: str = "dashboard--minimal-tech",
    preview: str = _CLEAN_PREVIEW,
    manifest_overrides: dict | None = None,
    omit_preview: bool = False,
) -> Path:
    preset_dir = tmp_path / preset_id
    preset_dir.mkdir(parents=True, exist_ok=True)
    if not omit_preview:
        (preset_dir / "preview.md").write_text(preview, encoding="utf-8")
    manifest = dict(_BASE_MANIFEST)
    manifest["id"] = preset_id
    if manifest_overrides:
        manifest.update(manifest_overrides)
    (preset_dir / "manifest.json").write_text(
        json.dumps(manifest, ensure_ascii=False), encoding="utf-8"
    )
    return preset_dir


def _codes(issues) -> list[str]:
    return [i.code for i in issues]


# ---------------------------------------------------------------------------
# P0 baseline
# ---------------------------------------------------------------------------


def test_p0_previews_pass_clean():
    reports = lint_all_previews(PRESETS_ROOT)
    seen = {r.preset_id for r in reports}
    assert P0_IDS.issubset(seen), f"Missing P0 presets: {P0_IDS - seen}"
    for report in reports:
        if report.preset_id not in P0_IDS:
            continue
        assert report.errors == [], (
            f"{report.preset_id} has unexpected errors: {report.errors}"
        )


# ---------------------------------------------------------------------------
# E001 / E002
# ---------------------------------------------------------------------------


def test_e001_missing_preview_file(tmp_path: Path):
    preset_dir = _write_preset(tmp_path, omit_preview=True)
    report = lint_preview(preset_dir)
    assert "E001" in _codes(report.errors)
    assert not report.ok


def test_e002_empty_preview_file(tmp_path: Path):
    preset_dir = _write_preset(tmp_path, preview="   \n\n  \n")
    report = lint_preview(preset_dir)
    assert "E002" in _codes(report.errors)


# ---------------------------------------------------------------------------
# E003 — missing sections
# ---------------------------------------------------------------------------


def test_e003_missing_multiple_sections(tmp_path: Path):
    minimal = """# x

## 어떤 제품에 맞나
- foo

## Color Tokens (light + dark)
- primary: `#000000`
- surface: `#FFFFFF`
- ink: `#111111`
- border: `#CCCCCC`
"""
    preset_dir = _write_preset(tmp_path, preview=minimal)
    report = lint_preview(preset_dir)
    codes = _codes(report.errors)
    assert codes.count("E003") == 3
    joined = " ".join(i.message for i in report.errors if i.code == "E003")
    assert "Typography" in joined
    assert "대표 컴포넌트" in joined
    assert "주의사항" in joined


def test_e003_accepts_english_alias(tmp_path: Path):
    aliased = _CLEAN_PREVIEW.replace("## 주의사항", "## Caveats")
    preset_dir = _write_preset(tmp_path, preview=aliased)
    report = lint_preview(preset_dir)
    assert "E003" not in _codes(report.errors)


# ---------------------------------------------------------------------------
# E004 — color swatches
# ---------------------------------------------------------------------------


def test_e004_insufficient_hex_swatches(tmp_path: Path):
    sparse = _CLEAN_PREVIEW.replace(
        """## Color Tokens (light + dark)
### Core
- primary: `#0A7CFF`
- accent: `#6366F1`
- surface_tint: `#FFFFFF`

### Semantic
- success: `#22C55E`
- warning: `#F59E0B`
- danger: `#EF4444`
- info: `#3B82F6`""",
        """## Color Tokens (light + dark)
- primary: `#0A7CFF`
- accent: `#6366F1`""",
    )
    preset_dir = _write_preset(tmp_path, preview=sparse)
    report = lint_preview(preset_dir)
    assert "E004" in _codes(report.errors)


def test_e004_skipped_when_builder_fallback_sentinel(tmp_path: Path):
    fallback = _CLEAN_PREVIEW.replace(
        """## Color Tokens (light + dark)
### Core
- primary: `#0A7CFF`
- accent: `#6366F1`
- surface_tint: `#FFFFFF`

### Semantic
- success: `#22C55E`
- warning: `#F59E0B`
- danger: `#EF4444`
- info: `#3B82F6`""",
        """## Color Tokens (light)
- (color_reference 미설정 — brand_profile.color_reference를 채우면 자동 추출)""",
    )
    preset_dir = _write_preset(
        tmp_path,
        preview=fallback,
        manifest_overrides={"color_modes": ["light"], "default_color_mode": "light"},
    )
    report = lint_preview(preset_dir)
    assert "E004" not in _codes(report.errors)


# ---------------------------------------------------------------------------
# E005 / E006 — dark drift
# ---------------------------------------------------------------------------


def test_e005_dark_declared_but_preview_silent(tmp_path: Path):
    silent = _CLEAN_PREVIEW.replace(
        "## Color Tokens (light + dark)", "## Color Tokens (light)"
    )
    preset_dir = _write_preset(tmp_path, preview=silent)  # manifest still has dark
    report = lint_preview(preset_dir)
    assert "E005" in _codes(report.errors)


def test_e006_light_only_but_preview_has_dark(tmp_path: Path):
    preset_dir = _write_preset(
        tmp_path,
        preview=_CLEAN_PREVIEW,  # header mentions "dark"
        manifest_overrides={"color_modes": ["light"], "default_color_mode": "light"},
    )
    report = lint_preview(preset_dir)
    assert "E006" in _codes(report.errors)


# ---------------------------------------------------------------------------
# E007 — typography missing
# ---------------------------------------------------------------------------


def test_e007_typography_section_lacks_font_bullets(tmp_path: Path):
    broken = _CLEAN_PREVIEW.replace(
        """## Typography
- heading: Inter
- body: Inter
- mono: JetBrains Mono
- korean: Pretendard""",
        """## Typography
(placeholder text without any font bullet)""",
    )
    preset_dir = _write_preset(tmp_path, preview=broken)
    report = lint_preview(preset_dir)
    assert "E007" in _codes(report.errors)


# ---------------------------------------------------------------------------
# E008 — component count
# ---------------------------------------------------------------------------


def test_e008_fewer_than_three_components(tmp_path: Path):
    short = _CLEAN_PREVIEW.replace(
        """## 대표 컴포넌트
- **DataTable** — parts: header, row
- **KpiCard** — parts: container, value
- **SidebarNav** — parts: container, item""",
        """## 대표 컴포넌트
- **DataTable** — parts: header, row
- **KpiCard** — parts: container, value""",
    )
    preset_dir = _write_preset(tmp_path, preview=short)
    report = lint_preview(preset_dir)
    assert "E008" in _codes(report.errors)


# ---------------------------------------------------------------------------
# W001 — hex invalid
# ---------------------------------------------------------------------------


def test_w001_malformed_hex_triggers_warning(tmp_path: Path):
    bad_hex = _CLEAN_PREVIEW.replace("`#6366F1`", "`#GGG123`")
    preset_dir = _write_preset(tmp_path, preview=bad_hex)
    report = lint_preview(preset_dir)
    assert "W001" in _codes(report.warnings)


# ---------------------------------------------------------------------------
# W002 — ko locale untagged
# ---------------------------------------------------------------------------


def test_w002_ko_in_manifest_but_typography_has_no_ko_hint(tmp_path: Path):
    no_ko_font = _CLEAN_PREVIEW.replace(
        """## Typography
- heading: Inter
- body: Inter
- mono: JetBrains Mono
- korean: Pretendard""",
        """## Typography
- heading: Inter
- body: Inter
- mono: JetBrains Mono""",
    )
    preset_dir = _write_preset(tmp_path, preview=no_ko_font)
    report = lint_preview(preset_dir)
    assert "W002" in _codes(report.warnings)


# ---------------------------------------------------------------------------
# W003 — caution empty
# ---------------------------------------------------------------------------


def test_w003_caveat_section_without_bullets(tmp_path: Path):
    empty_caveat = _CLEAN_PREVIEW.replace(
        """## 주의사항
- editorial 톤에는 editorial-warm 계열 권장
- 랜딩에는 부적합""",
        """## 주의사항
""",
    )
    preset_dir = _write_preset(tmp_path, preview=empty_caveat)
    report = lint_preview(preset_dir)
    assert "W003" in _codes(report.warnings)


# ---------------------------------------------------------------------------
# CLI smoke
# ---------------------------------------------------------------------------


def test_cli_lint_single_preset_exit_zero():
    result = subprocess.run(
        [
            "uv",
            "run",
            "design-ontology",
            "lint-previews",
            "--preset-id",
            "dashboard--minimal-tech",
        ],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, result.stderr
    assert "dashboard--minimal-tech" in result.stdout
    assert "OK" in result.stdout


def test_cli_lint_all_presets_exit_zero():
    result = subprocess.run(
        ["uv", "run", "design-ontology", "lint-previews"],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, result.stderr
    for pid in P0_IDS:
        assert pid in result.stdout
    assert "ERRORS: 0" in result.stdout
