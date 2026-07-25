"""Phase 14-3: build-catalog script tests.

Covers:
- parse_preview extracts summary / core / semantic / typography / components / cautions
- _swatch_for_hex maps luminance to ⬛ or ⬜
- render_catalog emits expected sections + anchors for the current 15-preset catalog
- CLI: `scripts/build-catalog.py --output <tmp>` writes a markdown file containing all preset ids
"""

from __future__ import annotations

import importlib.util
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
SCRIPT = REPO_ROOT / "scripts" / "build-catalog.py"
PRESETS_ROOT = REPO_ROOT / "presets"


def _load_script_module():
    name = "build_catalog_script"
    spec = importlib.util.spec_from_file_location(name, SCRIPT)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


BC = _load_script_module()


CLEAN_PREVIEW = """# demo--minimal-tech

## 어떤 제품에 맞나
- Sample summary line for preview parsing.

- app_mode: `demo` / brand_tone: `minimal-tech`

## Color Tokens (light + dark)
### Core
- primary: `#0A7CFF`
- accent: `#6366F1`
- surface_tint: `#F1F5F9`

### Semantic
- success: `#4A7C59`
- danger: `#8B2252`

## Typography
- heading: Inter
- body: Inter
- mono: JetBrains Mono
- korean: Pretendard

## 대표 컴포넌트
- **sidebar-nav** — parts: container, nav-item | states: default, hover
- **stat-card** — parts: container | states: default
- **insight-card** — parts: container | states: default, hover

## 주의사항
- image-derived hints are advisory
- try another brand_tone if this misses
"""


def test_parse_preview_extracts_all_sections():
    block = BC.parse_preview(CLEAN_PREVIEW)
    assert block.summary == "Sample summary line for preview parsing."
    assert block.core_colors == {
        "primary": "#0A7CFF",
        "accent": "#6366F1",
        "surface_tint": "#F1F5F9",
    }
    assert block.semantic_colors == {"success": "#4A7C59", "danger": "#8B2252"}
    assert block.typography["heading"] == "Inter"
    assert block.typography["korean"] == "Pretendard"
    assert [name for name, _ in block.components[:3]] == [
        "sidebar-nav",
        "stat-card",
        "insight-card",
    ]
    assert len(block.cautions) == 2


def test_parse_preview_handles_missing_sections():
    block = BC.parse_preview("# empty\n\n## Other section\n- item\n")
    assert block.summary is None
    assert block.core_colors == {}
    assert block.components == []


def test_swatch_for_hex_luminance_mapping():
    assert BC._swatch_for_hex("#000000") == "⬛"
    assert BC._swatch_for_hex("#FFFFFF") == "⬜"
    # mid-light blue → ⬜, dark navy → ⬛
    assert BC._swatch_for_hex("#87CEEB") == "⬜"
    assert BC._swatch_for_hex("#000080") == "⬛"


def test_render_catalog_current_presets_matrix():
    md = BC.render_catalog(PRESETS_ROOT)
    # Axis counts line
    assert "Axes: app_mode (×8) × brand_tone (×5)" in md
    # 25 presets currently in matrix.json after adding the corporate-trust document preset.
    assert "Total presets: **25**" in md
    # Matrix header row with all 5 brand tones
    for tone in ("minimal-tech", "editorial-warm", "bold-confident", "playful-soft", "corporate-trust"):
        assert tone in md
    # Every preset id must appear as an anchor header
    import json
    matrix = json.loads((PRESETS_ROOT / "matrix.json").read_text(encoding="utf-8"))
    for entry in matrix["presets"]:
        assert f"#### `{entry['id']}`" in md


def test_build_catalog_cli_writes_output(tmp_path):
    output = tmp_path / "CATALOG.md"
    result = subprocess.run(
        [sys.executable, str(SCRIPT), "--output", str(output)],
        cwd=REPO_ROOT,
        check=True,
        capture_output=True,
        text=True,
    )
    assert "wrote" in result.stdout
    assert output.exists()
    content = output.read_text(encoding="utf-8")
    assert content.startswith("# Preset Catalog")
    # Pick a known preset and confirm it rendered
    assert "`dashboard--minimal-tech`" in content
