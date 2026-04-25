"""Phase 13-12-3: tests for scripts/validate-community-preset.py.

Synthesizes tiny preset fixtures (manifest + preview + matrix + compatibility)
so every check path runs against known inputs:
    1. pass (no warnings)
    2. hex overlap warning
    3. cell duplicate warning
    4. structural error (missing required file)
    5. self-match failure (manifest tags disagree → Top-1 goes elsewhere)
    6. CLI entry returns the right exit code
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

SCRIPTS_DIR = REPO_ROOT / "scripts"
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

# The script filename has hyphens, so load it via importlib.util.
import importlib.util

_spec = importlib.util.spec_from_file_location(
    "validate_community_preset",
    SCRIPTS_DIR / "validate-community-preset.py",
)
assert _spec is not None and _spec.loader is not None
validate_mod = importlib.util.module_from_spec(_spec)
sys.modules[_spec.name] = validate_mod
_spec.loader.exec_module(validate_mod)


PREVIEW_TEMPLATE = """# {preset_id}

## 어떤 제품에 맞나
- 합성 fixture: {preset_id}

## Color Tokens (light + dark)
### Core
- primary: `{primary}`
- accent: `{accent}`
- surface_tint: `{surface_tint}`

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
- **alpha** — parts: container, label | states: default
- **beta** — parts: container, label | states: default
- **gamma** — parts: container, label | states: default

## 주의사항
- 합성 fixture — 실제 프리셋 아님
"""

MANIFEST_TEMPLATE = {
    "schema_version": "1.0.0",
    "preset_api_version": "1.0.0",
    "generated_by_harness_version": "0.1.0",
    "preview_version": "1.0.0",
    "adapter_compatibility": {
        "nextjs-tailwind-shadcn": ">=0.1.0 <1.0.0",
        "raw-css-variables": ">=0.1.0 <1.0.0",
    },
    "source_project": "fixture",
    "content_hash": "sha256:0000000000000000000000000000000000000000000000000000000000000000",
    "color_modes": ["light", "dark"],
    "default_color_mode": "light",
    "locale_pairings": {},
    "owner": "@fixture",
    "tier": "P3",
    "generated_at": "2026-04-20T00:00:00Z",
    "description": "fixture preset",
}

COMPATIBILITY_JSON = {
    "current_preset_api_version": "1.0.0",
    "supported_preset_api_range": ">=1.0.0 <2.0.0",
    "entries": [
        {
            "preset_api_version": "1.0.0",
            "deprecated": False,
            "notes": "fixture",
            "adapter_ranges": {
                "nextjs-tailwind-shadcn": ">=0.1.0 <1.0.0",
                "raw-css-variables": ">=0.1.0 <1.0.0",
            },
        }
    ],
}

TOKEN_SCHEMA_MIN = {"type": "object", "properties": {}}

SYSTEM_SPEC_MIN = "# system\n\nfixture spec\n"


def _write_preset(
    root: Path,
    preset_id: str,
    *,
    app_mode: str,
    brand_tone: str,
    tags: list[str],
    primary: str,
    accent: str,
    surface_tint: str,
    tier: str = "P3",
    skip_file: str | None = None,
) -> None:
    preset_dir = root / preset_id
    preset_dir.mkdir(parents=True, exist_ok=True)

    manifest = dict(MANIFEST_TEMPLATE)
    manifest.update(
        {
            "id": preset_id,
            "app_mode": app_mode,
            "brand_tone": brand_tone,
            "tags": tags,
            "tier": tier,
        }
    )

    files = {
        "manifest.json": json.dumps(manifest, ensure_ascii=False, indent=2),
        "preview.md": PREVIEW_TEMPLATE.format(
            preset_id=preset_id,
            primary=primary,
            accent=accent,
            surface_tint=surface_tint,
        ),
        "system_spec.md": SYSTEM_SPEC_MIN,
        "token_schema.json": json.dumps(TOKEN_SCHEMA_MIN),
    }
    for name, content in files.items():
        if skip_file == name:
            continue
        (preset_dir / name).write_text(content, encoding="utf-8")


def _write_matrix(root: Path, preset_entries: list[dict]) -> None:
    matrix = {
        "matrix_version": "1.0.0",
        "app_modes": [{"id": "dashboard", "label": "d", "representative_ux": []}],
        "brand_tones": [
            {"id": "minimal-tech", "label": "m", "keywords": [], "palette_bias": ""},
            {"id": "bold-confident", "label": "b", "keywords": [], "palette_bias": ""},
        ],
        "color_modes": ["light", "dark", "both"],
        "presets": preset_entries,
    }
    (root / "matrix.json").write_text(
        json.dumps(matrix, ensure_ascii=False, indent=2), encoding="utf-8"
    )


def _write_compat(root: Path) -> None:
    (root / "compatibility.json").write_text(
        json.dumps(COMPATIBILITY_JSON, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )


@pytest.fixture
def fixture_root(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> Path:
    """Builds a 'presets root' with two presets and points the matcher + validator at it."""

    root = tmp_path / "presets"
    root.mkdir()
    _write_compat(root)

    # Existing P1 preset occupying dashboard × minimal-tech.
    _write_preset(
        root,
        "dashboard--minimal-tech",
        app_mode="dashboard",
        brand_tone="minimal-tech",
        tags=["saas", "ko"],
        primary="#123456",
        accent="#AABBCC",
        surface_tint="#DDEEFF",
        tier="P1",
    )
    matrix_entries = [
        {
            "id": "dashboard--minimal-tech",
            "app_mode": "dashboard",
            "brand_tone": "minimal-tech",
            "color_modes": ["light", "dark"],
            "default_color_mode": "light",
            "tags": ["saas", "ko"],
            "description": "fixture",
            "source_project": "fixture",
            "owner": "@fixture",
            "preview_path": "presets/dashboard--minimal-tech/preview.md",
            "locale_pairings": {},
            "tier": "P1",
        }
    ]
    _write_matrix(root, matrix_entries)

    # Point the matcher engine at this fixture matrix.
    from design_ontology_harness.preset_matcher import engine as engine_mod

    monkeypatch.setattr(engine_mod, "MATRIX_PATH", root / "matrix.json")
    return root


def _run(preset_id: str, presets_root: Path) -> validate_mod.CheckReport:
    return validate_mod.run_checks(preset_id, presets_root)


def _add_candidate(
    root: Path,
    *,
    preset_id: str,
    app_mode: str,
    brand_tone: str,
    tags: list[str],
    primary: str,
    accent: str,
    surface_tint: str,
    skip_file: str | None = None,
) -> None:
    _write_preset(
        root,
        preset_id,
        app_mode=app_mode,
        brand_tone=brand_tone,
        tags=tags,
        primary=primary,
        accent=accent,
        surface_tint=surface_tint,
        tier="P3",
        skip_file=skip_file,
    )
    matrix_path = root / "matrix.json"
    matrix = json.loads(matrix_path.read_text(encoding="utf-8"))
    matrix["presets"].append(
        {
            "id": preset_id,
            "app_mode": app_mode,
            "brand_tone": brand_tone,
            "color_modes": ["light", "dark"],
            "default_color_mode": "light",
            "tags": tags,
            "description": "candidate fixture",
            "source_project": "fixture",
            "owner": "@candidate",
            "preview_path": f"presets/{preset_id}/preview.md",
            "locale_pairings": {},
            "tier": "P3",
        }
    )
    matrix["presets"].sort(key=lambda e: e["id"])
    matrix_path.write_text(
        json.dumps(matrix, ensure_ascii=False, indent=2), encoding="utf-8"
    )


def test_pass_case(fixture_root: Path):
    _add_candidate(
        fixture_root,
        preset_id="dashboard--bold-confident",
        app_mode="dashboard",
        brand_tone="bold-confident",
        tags=["b2c", "sports"],
        primary="#FF3300",
        accent="#00AA55",
        surface_tint="#FFEE88",
    )
    report = _run("dashboard--bold-confident", fixture_root)
    assert report.ok, f"errors: {report.errors}"
    assert report.warnings == [], f"unexpected warnings: {report.warnings}"


def test_hex_overlap_warning(fixture_root: Path):
    # 2 of 3 HEXes collide with the existing dashboard--minimal-tech.
    _add_candidate(
        fixture_root,
        preset_id="dashboard--bold-confident",
        app_mode="dashboard",
        brand_tone="bold-confident",
        tags=["b2c"],
        primary="#123456",      # collide
        accent="#AABBCC",       # collide
        surface_tint="#FFEE88",
    )
    report = _run("dashboard--bold-confident", fixture_root)
    assert report.ok, f"errors: {report.errors}"
    overlap_warnings = [w for w in report.warnings if "HEX overlap" in w]
    assert overlap_warnings, report.warnings


def test_cell_duplicate_warning(fixture_root: Path):
    # Same (dashboard, minimal-tech) cell as existing P1.
    _add_candidate(
        fixture_root,
        preset_id="dashboard--minimal-tech-v2",  # different id to avoid clash
        app_mode="dashboard",
        brand_tone="minimal-tech",
        tags=["fintech"],
        primary="#ABCDEF",
        accent="#112233",
        surface_tint="#FEDCBA",
    )
    # The validator expects id == f"{app_mode}--{brand_tone}", so this id is
    # invalid. Instead, simulate by registering a valid P3 under the same cell
    # via matrix-only duplication check — but our check_cell_duplicate reads
    # matrix.json entries, not on-disk id uniqueness.
    # To exercise just the cell duplication check, run it directly:
    manifest = {
        "id": "dashboard--minimal-tech-v2",
        "app_mode": "dashboard",
        "brand_tone": "minimal-tech",
    }
    matrix = validate_mod._load_matrix(fixture_root)
    report = validate_mod.CheckReport(preset_id="dashboard--minimal-tech-v2")
    validate_mod.check_cell_duplicate(
        report, manifest, matrix, "dashboard--minimal-tech-v2"
    )
    assert any("Cell duplicate" in w for w in report.warnings), report.warnings


def test_missing_required_file_error(fixture_root: Path):
    _add_candidate(
        fixture_root,
        preset_id="dashboard--bold-confident",
        app_mode="dashboard",
        brand_tone="bold-confident",
        tags=["x"],
        primary="#FF3300",
        accent="#00AA55",
        surface_tint="#FFEE88",
        skip_file="system_spec.md",
    )
    report = _run("dashboard--bold-confident", fixture_root)
    assert not report.ok
    assert any("system_spec.md" in e for e in report.errors), report.errors


def test_self_match_failure(fixture_root: Path):
    # Manifest claims dashboard × bold-confident, but tags align strongly
    # with the existing preset — self-match happens on explicit fields so
    # top-1 must still be the new preset. To trigger a miss, we build the
    # candidate with a tag set empty and same app_mode/brand_tone as a cell
    # already occupied by its own registered self. We simulate failure by
    # manually mutating the matrix after the preset is written so the
    # matcher doesn't see the candidate.
    _add_candidate(
        fixture_root,
        preset_id="dashboard--bold-confident",
        app_mode="dashboard",
        brand_tone="bold-confident",
        tags=["unique-tag"],
        primary="#FF3300",
        accent="#00AA55",
        surface_tint="#FFEE88",
    )
    matrix_path = fixture_root / "matrix.json"
    matrix = json.loads(matrix_path.read_text(encoding="utf-8"))
    matrix["presets"] = [
        e for e in matrix["presets"] if e["id"] != "dashboard--bold-confident"
    ]
    matrix_path.write_text(
        json.dumps(matrix, ensure_ascii=False, indent=2), encoding="utf-8"
    )

    # Run only the self-match check so other checks don't flag structure.
    manifest = json.loads(
        (fixture_root / "dashboard--bold-confident" / "manifest.json").read_text(
            encoding="utf-8"
        )
    )
    report = validate_mod.CheckReport(preset_id="dashboard--bold-confident")
    validate_mod.check_self_match(report, manifest, "dashboard--bold-confident")
    assert not report.ok
    assert any("self-match" in e for e in report.errors), report.errors


def test_cli_exit_code_on_pass(fixture_root: Path, capsys: pytest.CaptureFixture[str]):
    _add_candidate(
        fixture_root,
        preset_id="dashboard--bold-confident",
        app_mode="dashboard",
        brand_tone="bold-confident",
        tags=["sports"],
        primary="#FF3300",
        accent="#00AA55",
        surface_tint="#FFEE88",
    )
    exit_code = validate_mod.main(
        [
            "--preset-id",
            "dashboard--bold-confident",
            "--presets-dir",
            str(fixture_root),
        ]
    )
    captured = capsys.readouterr()
    assert exit_code == 0, captured.out
    assert "dashboard--bold-confident" in captured.out
