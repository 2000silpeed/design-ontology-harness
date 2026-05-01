"""Phase 10B-5: round-trip tests for raw-css-variables adapter.

Covers:
- P0 5종 × each declared color_mode: render() produces the expected file set
- tokens.css has all core --ds-color-* tokens as parseable #HEX or var(...)
- dark-supporting presets include [data-theme='dark'] + prefers-color-scheme block
- light-only presets skip dark blocks entirely
- Brace balance across tokens.css and fonts.css
- locale='ko' injects fonts.css + Pretendard scaffolds; non-ko preset skips
- detect(): bare tmp_path ≥ 0.5 (universal fallback)
- merge() preserves user code outside managed block on tokens.css
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
from design_ontology_harness.adapters.raw_css_variables import (
    ADAPTER_ID,
    ADAPTER_VERSION,
    RawCssVariablesAdapter,
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
def adapter() -> RawCssVariablesAdapter:
    return RawCssVariablesAdapter()


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
    raw_range = entry["adapter_ranges"][ADAPTER_ID]
    from design_ontology_harness.semver_range import satisfies
    assert satisfies(ADAPTER_VERSION, raw_range), (
        f"adapter version {ADAPTER_VERSION} does not satisfy compat range {raw_range}"
    )


@pytest.mark.parametrize("preset_id", sorted(EXPECTED_P0_IDS))
def test_roundtrip_each_mode(preset_id: str, adapter: RawCssVariablesAdapter, tmp_path: Path):
    bundle = load_preset_bundle(PRESETS_ROOT / preset_id)
    assert bundle.color_modes, f"{preset_id} declares no color_modes"

    for mode in bundle.color_modes:
        target = tmp_path / preset_id / mode
        target.mkdir(parents=True, exist_ok=True)
        ops = adapter.render(bundle, target, mode, locale="en")

        paths = {op.path for op in ops}
        assert "design-system/tokens.css" in paths
        assert "design-system/README.md" in paths
        assert "design-system/IMPLEMENTATION_CONTRACT.md" in paths
        assert "design-system/manifest.json" in paths
        # Raw adapter never writes outside design-system/.
        for op in ops:
            assert op.path.startswith("design-system/"), (
                f"raw adapter leaked outside design-system/: {op.path}"
            )

        report = adapter.apply(target, ops)
        assert not report.proposed, f"unexpected .ds-proposed writes: {report.proposed}"

        tokens_text = (target / "design-system/tokens.css").read_text(encoding="utf-8")
        _assert_tokens_css_ok(tokens_text, bundle.color_modes)

        # README mentions tokens.css link
        readme = (target / "design-system/README.md").read_text(encoding="utf-8")
        assert './design-system/tokens.css' in readme


def test_rejects_unsupported_color_mode(adapter: RawCssVariablesAdapter, tmp_path: Path):
    bundle = load_preset_bundle(PRESETS_ROOT / "commerce--editorial-warm")
    assert "dark" not in bundle.color_modes
    with pytest.raises(ValueError):
        adapter.render(bundle, tmp_path, "dark")


def test_locale_ko_injects_fonts(adapter: RawCssVariablesAdapter, tmp_path: Path):
    bundle = load_preset_bundle(PRESETS_ROOT / "dashboard--minimal-tech")
    assert "ko" in bundle.locale_pairings

    ops = adapter.render(bundle, tmp_path, "light", locale="ko")
    paths = {op.path for op in ops}
    assert "design-system/fonts.css" in paths
    assert "design-system/fonts/PretendardVariable.placeholder" in paths
    assert "design-system/fonts/LICENSE-FONTS" in paths
    assert "design-system/fonts/fetch-pretendard.mjs" in paths

    fonts_css = next(op for op in ops if op.path == "design-system/fonts.css").content
    assert "Pretendard Variable" in fonts_css
    assert "@font-face" in fonts_css
    assert "--ds-font-ko" in fonts_css
    assert "--ds-font-heading" in fonts_css
    assert "--ds-font-body" in fonts_css
    assert "--ds-font-mono" in fonts_css
    _assert_balanced_braces(fonts_css, label="fonts.css")

    # README should reference fonts.css when ko assets are present.
    readme = next(op for op in ops if op.path == "design-system/README.md").content
    assert "./design-system/fonts.css" in readme

    # Fetch script TARGET must point into design-system/fonts/, not public/fonts/.
    fetch = next(op for op in ops if op.path == "design-system/fonts/fetch-pretendard.mjs").content
    assert 'const TARGET = "design-system/fonts/PretendardVariable.woff2"' in fetch

    # English mode must NOT inject ko assets.
    ops_en = adapter.render(bundle, tmp_path, "light", locale="en")
    paths_en = {op.path for op in ops_en}
    assert "design-system/fonts.css" not in paths_en
    assert "design-system/fonts/PretendardVariable.placeholder" not in paths_en


def test_locale_ko_noop_for_non_ko_preset(adapter: RawCssVariablesAdapter, tmp_path: Path):
    bundle = load_preset_bundle(PRESETS_ROOT / "marketing-landing--bold-confident")
    assert "ko" not in bundle.locale_pairings

    ops = adapter.render(bundle, tmp_path, "light", locale="ko")
    paths = {op.path for op in ops}
    assert "design-system/fonts.css" not in paths
    assert "design-system/fonts/PretendardVariable.placeholder" not in paths


def test_mirror_copies_style_capsule_when_present(adapter: RawCssVariablesAdapter, tmp_path: Path):
    bundle = load_preset_bundle(PRESETS_ROOT / "conversation-copilot--corporate-trust")

    ops = adapter.render(bundle, tmp_path, "light", locale="ko")
    paths = {op.path for op in ops}

    assert "design-system/STYLE.md" in paths
    assert "design-system/DESIGN.md" in paths
    style_text = next(op.content for op in ops if op.path == "design-system/STYLE.md")
    assert "Style Capsule" in style_text
    assert "Token binding is necessary but not sufficient" in style_text


def test_detect_bare_tmp_path_scores_above_threshold(
    adapter: RawCssVariablesAdapter, tmp_path: Path
):
    score = adapter.detect(tmp_path)
    assert score >= 0.5, f"raw-css must be a viable fallback on empty repo, got {score}"


def test_detect_tailwind_repo_still_viable(
    adapter: RawCssVariablesAdapter, tmp_path: Path
):
    # A fully-wired Next+Tailwind+shadcn repo. Raw-css is still a valid option
    # (universal fallback) — we don't require it to be high, only not broken.
    (tmp_path / "package.json").write_text(
        json.dumps({"name": "demo", "dependencies": {"next": "14.2.0", "tailwindcss": "3.4.0"}}),
        encoding="utf-8",
    )
    (tmp_path / "tailwind.config.ts").write_text("export default {}", encoding="utf-8")
    (tmp_path / "components.json").write_text(
        '{"$schema":"https://ui.shadcn.com/schema.json"}', encoding="utf-8"
    )
    score = adapter.detect(tmp_path)
    assert 0.0 <= score <= 1.0


def test_merge_idempotent_on_tokens_css(adapter: RawCssVariablesAdapter, tmp_path: Path):
    bundle = load_preset_bundle(PRESETS_ROOT / "dashboard--minimal-tech")

    ops1 = adapter.render(bundle, tmp_path, "light", locale="en")
    adapter.apply(tmp_path, ops1)
    tokens_path = tmp_path / "design-system/tokens.css"
    original = tokens_path.read_text(encoding="utf-8")

    user_suffix = "\n\n/* user overrides */\n.custom { color: red; }\n"
    tokens_path.write_text(original + user_suffix, encoding="utf-8")

    ops2 = adapter.render(bundle, tmp_path, "light", locale="en")
    report = adapter.apply(tmp_path, ops2)
    assert "design-system/tokens.css" in report.merged
    assert not report.proposed

    updated = tokens_path.read_text(encoding="utf-8")
    assert ".custom { color: red; }" in updated, "user CSS must survive merge"
    assert "design-ontology:START" in updated and "design-ontology:END" in updated


def test_merge_falls_back_to_proposed_when_markers_missing(
    adapter: RawCssVariablesAdapter, tmp_path: Path
):
    bundle = load_preset_bundle(PRESETS_ROOT / "dashboard--minimal-tech")

    # Pre-create a tokens.css without design-ontology markers.
    (tmp_path / "design-system").mkdir(parents=True, exist_ok=True)
    (tmp_path / "design-system/tokens.css").write_text(
        ":root { --brand: red; }\n", encoding="utf-8"
    )

    ops = adapter.render(bundle, tmp_path, "light", locale="en")
    report = adapter.apply(tmp_path, ops)
    assert any(
        path == "design-system/tokens.css.ds-proposed" for path, _ in report.proposed
    ), f"expected tokens.css to land as .ds-proposed, got {report.proposed}"

    preserved = (tmp_path / "design-system/tokens.css").read_text(encoding="utf-8")
    assert "--brand: red" in preserved


# ---------------------------------------------------------------------------
# Helpers


def _assert_tokens_css_ok(text: str, color_modes: list[str]) -> None:
    assert "design-ontology:START" in text and "design-ontology:END" in text
    assert ":root" in text
    # Core tokens must be declared
    for required in (
        "--ds-color-primary",
        "--ds-color-surface",
        "--ds-color-ink",
        "--ds-color-border",
    ):
        assert required in text, f"missing {required} in tokens.css"
    # Every --ds-color-* declaration must parse as hex or var(...)
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
        assert "[data-theme='dark']" not in text, (
            "light-only preset must not emit dark block"
        )
        assert "prefers-color-scheme" not in text
    _assert_balanced_braces(text, label="tokens.css")


def _assert_balanced_braces(text: str, *, label: str) -> None:
    opens = text.count("{")
    closes = text.count("}")
    assert opens == closes, f"unbalanced braces in {label} ({opens} vs {closes})"
