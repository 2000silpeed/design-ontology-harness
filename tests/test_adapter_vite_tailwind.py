"""Phase 10C-5: round-trip tests for vite-tailwind adapter.

Covers:
- P0 5종 × each declared color_mode: render() produces the expected file set
- tailwind.config.ts has `Config` import, darkMode, var(--ds-color-*), managed block
- src/index.css has @tailwind directives inside the managed block + core tokens
- dark-supporting presets emit [data-theme='dark'] + prefers-color-scheme block
- light-only presets skip dark blocks
- components.json / app/globals.css are NEVER written by this adapter
- locale='ko' injects public/fonts/ scaffolds + scripts/fetch-pretendard.mjs
- non-ko preset with locale='ko' skips ko assets
- detect() scores a Vite+React+Tailwind repo ≥ 0.7
- detect() penalises a Next repo (no vite, has next) ≤ 0.15
- merge() is idempotent on both managed files and preserves user CSS
- merge() falls back to .ds-proposed when markers are missing
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from design_ontology_harness.adapters import (
    get_adapter,
    list_adapters,
    load_preset_bundle,
)
from design_ontology_harness.adapters.vite_tailwind import (
    ADAPTER_ID,
    ADAPTER_VERSION,
    ViteTailwindAdapter,
)

PRESETS_ROOT = REPO_ROOT / "presets"
EXPECTED_P0_IDS = {
    "commerce--editorial-warm",
    "conversation-copilot--minimal-tech",
    "dashboard--minimal-tech",
    "document-content--editorial-warm",
    "marketing-landing--bold-confident",
}

_HEX_RE = re.compile(r"#[0-9A-F]{6}", re.IGNORECASE)


@pytest.fixture(scope="module")
def adapter() -> ViteTailwindAdapter:
    return ViteTailwindAdapter()


def test_registry_exposes_adapter():
    assert ADAPTER_ID in list_adapters()
    assert list_adapters() == [
        "nextjs-tailwind-shadcn",
        "raw-css-variables",
        "vite-tailwind",
    ]
    cls = get_adapter(ADAPTER_ID)
    instance = cls()
    assert instance.id == ADAPTER_ID
    assert instance.version == ADAPTER_VERSION
    assert instance.supported_preset_api.startswith(">=1.0.0")


def test_compatibility_matches_adapter_version():
    compat = json.loads((PRESETS_ROOT / "compatibility.json").read_text(encoding="utf-8"))
    entry = next(
        e for e in compat["entries"]
        if e["preset_api_version"] == compat["current_preset_api_version"]
    )
    vite_range = entry["adapter_ranges"][ADAPTER_ID]
    from design_ontology_harness.semver_range import satisfies
    assert satisfies(ADAPTER_VERSION, vite_range), (
        f"adapter version {ADAPTER_VERSION} does not satisfy compat range {vite_range}"
    )


@pytest.mark.parametrize("preset_id", sorted(EXPECTED_P0_IDS))
def test_roundtrip_each_mode(preset_id: str, adapter: ViteTailwindAdapter, tmp_path: Path):
    bundle = load_preset_bundle(PRESETS_ROOT / preset_id)
    assert bundle.color_modes, f"{preset_id} declares no color_modes"

    for mode in bundle.color_modes:
        target = tmp_path / preset_id / mode
        target.mkdir(parents=True, exist_ok=True)
        ops = adapter.render(bundle, target, mode, locale="en")

        paths = {op.path for op in ops}
        assert "tailwind.config.ts" in paths
        assert "src/index.css" in paths
        assert "design-system/manifest.json" in paths

        # Shadcn-specific files must NOT be generated.
        assert "components.json" not in paths
        assert "app/globals.css" not in paths

        report = adapter.apply(target, ops)
        assert not report.proposed, f"unexpected .ds-proposed writes: {report.proposed}"

        tw_text = (target / "tailwind.config.ts").read_text(encoding="utf-8")
        _assert_tailwind_config_ok(tw_text, bundle.color_modes)

        css_text = (target / "src/index.css").read_text(encoding="utf-8")
        _assert_index_css_ok(css_text, bundle.color_modes)

        assert not (target / "components.json").exists()
        assert not (target / "app/globals.css").exists()


def test_rejects_unsupported_color_mode(adapter: ViteTailwindAdapter, tmp_path: Path):
    bundle = load_preset_bundle(PRESETS_ROOT / "commerce--editorial-warm")
    assert "dark" not in bundle.color_modes
    with pytest.raises(ValueError):
        adapter.render(bundle, tmp_path, "dark")


def test_locale_ko_injects_assets(adapter: ViteTailwindAdapter, tmp_path: Path):
    bundle = load_preset_bundle(PRESETS_ROOT / "dashboard--minimal-tech")
    assert "ko" in bundle.locale_pairings

    ops = adapter.render(bundle, tmp_path, "light", locale="ko")
    paths = {op.path for op in ops}
    assert "public/fonts/PretendardVariable.placeholder" in paths
    assert "public/fonts/LICENSE-FONTS" in paths
    assert "scripts/fetch-pretendard.mjs" in paths

    css = next(op for op in ops if op.path == "src/index.css").content
    assert "Pretendard Variable" in css
    assert "@font-face" in css

    fetch = next(op for op in ops if op.path == "scripts/fetch-pretendard.mjs").content
    assert 'const TARGET = "public/fonts/PretendardVariable.woff2"' in fetch

    # English mode must not inject ko assets.
    ops_en = adapter.render(bundle, tmp_path, "light", locale="en")
    paths_en = {op.path for op in ops_en}
    assert "public/fonts/PretendardVariable.placeholder" not in paths_en


def test_locale_ko_noop_for_non_ko_preset(adapter: ViteTailwindAdapter, tmp_path: Path):
    bundle = load_preset_bundle(PRESETS_ROOT / "marketing-landing--bold-confident")
    assert "ko" not in bundle.locale_pairings

    ops = adapter.render(bundle, tmp_path, "light", locale="ko")
    paths = {op.path for op in ops}
    assert "public/fonts/PretendardVariable.placeholder" not in paths
    assert "public/fonts/LICENSE-FONTS" not in paths


def test_detect_scores_vite_repo_high(adapter: ViteTailwindAdapter, tmp_path: Path):
    (tmp_path / "package.json").write_text(
        json.dumps(
            {
                "name": "demo",
                "dependencies": {
                    "react": "18.3.0",
                },
                "devDependencies": {
                    "vite": "5.2.0",
                    "@vitejs/plugin-react": "4.3.0",
                    "tailwindcss": "3.4.0",
                },
            }
        ),
        encoding="utf-8",
    )
    (tmp_path / "vite.config.ts").write_text(
        "import { defineConfig } from 'vite';\nexport default defineConfig({});\n",
        encoding="utf-8",
    )
    (tmp_path / "tailwind.config.ts").write_text("export default {}", encoding="utf-8")
    score = adapter.detect(tmp_path)
    assert score >= 0.7, f"vite repo should score high, got {score}"


def test_detect_penalises_next_repo(adapter: ViteTailwindAdapter, tmp_path: Path):
    # Pure Next + shadcn repo: no vite, but has next + tailwind. Vite adapter
    # must score ≤ 0.15 so the Next adapter wins.
    (tmp_path / "package.json").write_text(
        json.dumps(
            {
                "name": "next-demo",
                "dependencies": {
                    "next": "14.2.0",
                    "react": "18.3.0",
                    "tailwindcss": "3.4.0",
                },
            }
        ),
        encoding="utf-8",
    )
    (tmp_path / "tailwind.config.ts").write_text("export default {}", encoding="utf-8")
    score = adapter.detect(tmp_path)
    assert score <= 0.15, f"Next repo must yield to Next adapter, got {score}"


def test_detect_bare_repo_low(adapter: ViteTailwindAdapter, tmp_path: Path):
    (tmp_path / "package.json").write_text(
        json.dumps({"name": "bare", "dependencies": {"express": "4.19.0"}}),
        encoding="utf-8",
    )
    score = adapter.detect(tmp_path)
    assert score <= 0.15, f"unrelated repo should score low, got {score}"


def test_merge_idempotent_on_index_css(adapter: ViteTailwindAdapter, tmp_path: Path):
    bundle = load_preset_bundle(PRESETS_ROOT / "dashboard--minimal-tech")

    # Seed an existing src/index.css that already has a DS managed block
    # (first install). User code outside the block must survive re-apply.
    ops1 = adapter.render(bundle, tmp_path, "light", locale="en")
    adapter.apply(tmp_path, ops1)
    css_path = tmp_path / "src/index.css"
    original = css_path.read_text(encoding="utf-8")

    user_suffix = "\n\n/* user-owned styles */\n.my-button { color: red; }\n"
    css_path.write_text(original + user_suffix, encoding="utf-8")

    ops2 = adapter.render(bundle, tmp_path, "light", locale="en")
    report = adapter.apply(tmp_path, ops2)
    assert "src/index.css" in report.merged
    assert not report.proposed

    updated = css_path.read_text(encoding="utf-8")
    assert ".my-button { color: red; }" in updated, "user CSS must survive merge"
    assert "design-ontology:START" in updated and "design-ontology:END" in updated
    # Tailwind directives must still be present inside the replaced block.
    assert "@tailwind base;" in updated
    assert "@tailwind utilities;" in updated


def test_merge_falls_back_to_proposed_when_markers_missing(
    adapter: ViteTailwindAdapter, tmp_path: Path
):
    bundle = load_preset_bundle(PRESETS_ROOT / "dashboard--minimal-tech")
    # Pre-existing tailwind.config.ts without DS markers → must land as proposed.
    (tmp_path / "tailwind.config.ts").write_text(
        "export default { content: ['./index.html'] };\n", encoding="utf-8"
    )
    # Same for src/index.css
    (tmp_path / "src").mkdir(parents=True, exist_ok=True)
    (tmp_path / "src/index.css").write_text(
        "/* existing user CSS */\n.custom { color: hotpink; }\n", encoding="utf-8"
    )

    ops = adapter.render(bundle, tmp_path, "light", locale="en")
    report = adapter.apply(tmp_path, ops)
    proposed_paths = {path for path, _ in report.proposed}
    assert "tailwind.config.ts.ds-proposed" in proposed_paths
    assert "src/index.css.ds-proposed" in proposed_paths

    # User files stay untouched.
    tw = (tmp_path / "tailwind.config.ts").read_text(encoding="utf-8")
    assert "./index.html" in tw
    css = (tmp_path / "src/index.css").read_text(encoding="utf-8")
    assert ".custom { color: hotpink; }" in css


# ---------------------------------------------------------------------------
# Helpers


def _assert_tailwind_config_ok(text: str, color_modes: list[str]) -> None:
    assert "design-ontology:START" in text and "design-ontology:END" in text
    assert "import type { Config }" in text
    assert "export default config" in text
    assert "theme:" in text and "extend:" in text
    assert "darkMode" in text
    # Vite-specific content globs
    assert "./index.html" in text
    assert "./src/**" in text
    if "dark" in color_modes:
        assert "[data-theme='dark']" in text
    # Brace balance excluding DS comment markers
    body = text.replace("/* design-ontology:START */", "").replace(
        "/* design-ontology:END */", ""
    )
    opens = body.count("{")
    closes = body.count("}")
    assert opens == closes, f"unbalanced braces in tailwind.config.ts ({opens} vs {closes})"
    # Tokens route through CSS vars
    assert "var(--ds-color-primary)" in text
    assert "var(--ds-color-accent)" in text


def _assert_index_css_ok(text: str, color_modes: list[str]) -> None:
    assert "design-ontology:START" in text and "design-ontology:END" in text
    # @tailwind directives inside the managed block
    assert "@tailwind base;" in text
    assert "@tailwind components;" in text
    assert "@tailwind utilities;" in text
    assert ":root" in text
    for required in (
        "--ds-color-primary",
        "--ds-color-surface",
        "--ds-color-ink",
        "--ds-color-border",
    ):
        assert required in text, f"missing {required} in index.css"
    for line in text.splitlines():
        stripped = line.strip()
        if stripped.startswith("--ds-color-") and ":" in stripped:
            assert stripped.endswith(";"), f"missing semicolon: {stripped!r}"
            _, value = stripped.split(":", 1)
            value = value.rstrip(";").strip()
            assert _HEX_RE.match(value) or value.startswith("var("), (
                f"non-hex, non-var value: {stripped!r}"
            )
    if "dark" in color_modes:
        assert "[data-theme='dark']" in text
        assert "prefers-color-scheme: dark" in text
    else:
        assert "[data-theme='dark']" not in text
        assert "prefers-color-scheme" not in text
    opens = text.count("{")
    closes = text.count("}")
    assert opens == closes, f"unbalanced braces in index.css ({opens} vs {closes})"
