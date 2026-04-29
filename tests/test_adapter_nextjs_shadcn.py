"""Phase 10A-5: round-trip tests for nextjs-tailwind-shadcn adapter.

Covers:
- P0 5종 × each declared color_mode: render() produces the expected file set
- Generated tailwind.config.ts and globals.css parse with regex-based checks
- components.json is valid JSON with shadcn schema hook
- locale='ko' injects Pretendard assets only when the preset declares a ko pairing
- detect() scores a synthetic Next+Tailwind+shadcn repo ≥ 0.7
- merge() preserves user code outside the managed block
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
from design_ontology_harness.adapters.nextjs_tailwind_shadcn import (
    ADAPTER_ID,
    ADAPTER_VERSION,
    NextjsTailwindShadcnAdapter,
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


def _preset_ids() -> list[str]:
    return sorted(
        p.name for p in PRESETS_ROOT.iterdir()
        if p.is_dir() and (p / "manifest.json").exists()
    )


@pytest.fixture(scope="module")
def adapter() -> NextjsTailwindShadcnAdapter:
    return NextjsTailwindShadcnAdapter()


def test_registry_exposes_adapter():
    assert ADAPTER_ID in list_adapters()
    cls = get_adapter(ADAPTER_ID)
    instance = cls()
    assert instance.id == ADAPTER_ID
    assert instance.version == ADAPTER_VERSION
    assert instance.supported_preset_api.startswith(">=1.0.0")


def test_p0_set_present():
    assert EXPECTED_P0_IDS.issubset(set(_preset_ids())), (
        f"Missing P0 presets: {EXPECTED_P0_IDS - set(_preset_ids())}"
    )


def test_compatibility_matches_adapter_version(tmp_path: Path):
    compat = json.loads((PRESETS_ROOT / "compatibility.json").read_text(encoding="utf-8"))
    entry = next(
        e for e in compat["entries"]
        if e["preset_api_version"] == compat["current_preset_api_version"]
    )
    nextjs_range = entry["adapter_ranges"][ADAPTER_ID]
    from design_ontology_harness.semver_range import satisfies
    assert satisfies(ADAPTER_VERSION, nextjs_range), (
        f"adapter version {ADAPTER_VERSION} does not satisfy compat range {nextjs_range}"
    )


@pytest.mark.parametrize("preset_id", sorted(EXPECTED_P0_IDS))
def test_roundtrip_each_mode(preset_id: str, adapter: NextjsTailwindShadcnAdapter, tmp_path: Path):
    bundle = load_preset_bundle(PRESETS_ROOT / preset_id)
    assert bundle.color_modes, f"{preset_id} declares no color_modes"

    for mode in bundle.color_modes:
        target = tmp_path / preset_id / mode
        target.mkdir(parents=True, exist_ok=True)
        ops = adapter.render(bundle, target, mode, locale="en")

        paths = {op.path for op in ops}
        assert "tailwind.config.ts" in paths
        assert "app/globals.css" in paths
        assert "components.json" in paths
        assert "design-system/manifest.json" in paths

        report = adapter.apply(target, ops)
        assert not report.proposed, f"unexpected .ds-proposed writes: {report.proposed}"

        # Tailwind config sanity — regex checks (Node-free)
        tw_text = (target / "tailwind.config.ts").read_text(encoding="utf-8")
        _assert_tailwind_config_ok(tw_text, bundle.color_modes)

        css_text = (target / "app/globals.css").read_text(encoding="utf-8")
        _assert_globals_css_ok(css_text, bundle.color_modes)

        cj = json.loads((target / "components.json").read_text(encoding="utf-8"))
        assert cj["$schema"] == "https://ui.shadcn.com/schema.json"
        assert cj["tailwind"]["cssVariables"] is True
        assert cj["tailwind"]["config"] == "tailwind.config.ts"
        assert cj["tailwind"]["css"] == "app/globals.css"
        assert cj["x-design-ontology"]["preset"] == preset_id


def test_rejects_unsupported_color_mode(adapter: NextjsTailwindShadcnAdapter, tmp_path: Path):
    # commerce--editorial-warm is light-only
    bundle = load_preset_bundle(PRESETS_ROOT / "commerce--editorial-warm")
    assert "dark" not in bundle.color_modes
    with pytest.raises(ValueError):
        adapter.render(bundle, tmp_path, "dark")


def test_locale_ko_injects_assets(adapter: NextjsTailwindShadcnAdapter, tmp_path: Path):
    bundle = load_preset_bundle(PRESETS_ROOT / "dashboard--minimal-tech")
    assert "ko" in bundle.locale_pairings

    ops = adapter.render(bundle, tmp_path, "light", locale="ko")
    paths = {op.path for op in ops}
    assert "public/fonts/PretendardVariable.placeholder" in paths
    assert "public/fonts/LICENSE-FONTS" in paths
    assert "scripts/fetch-pretendard.mjs" in paths

    css = next(op for op in ops if op.path == "app/globals.css").content
    assert "Pretendard Variable" in css
    assert "@font-face" in css

    # English mode should NOT inject ko assets
    ops_en = adapter.render(bundle, tmp_path, "light", locale="en")
    paths_en = {op.path for op in ops_en}
    assert "public/fonts/PretendardVariable.placeholder" not in paths_en


def test_locale_ko_noop_for_non_ko_preset(adapter: NextjsTailwindShadcnAdapter, tmp_path: Path):
    # marketing-landing--bold-confident has no ko pairing
    bundle = load_preset_bundle(PRESETS_ROOT / "marketing-landing--bold-confident")
    assert "ko" not in bundle.locale_pairings

    ops = adapter.render(bundle, tmp_path, "light", locale="ko")
    paths = {op.path for op in ops}
    # Without a ko pairing, we must not ship Pretendard files.
    assert "public/fonts/PretendardVariable.placeholder" not in paths
    assert "public/fonts/LICENSE-FONTS" not in paths


def test_detect_scores_matching_repo(adapter: NextjsTailwindShadcnAdapter, tmp_path: Path):
    (tmp_path / "package.json").write_text(
        json.dumps(
            {
                "name": "demo",
                "dependencies": {
                    "next": "14.2.0",
                    "react": "18.3.0",
                    "tailwindcss": "3.4.0",
                    "@radix-ui/react-slot": "1.1.0",
                    "class-variance-authority": "0.7.0",
                },
            }
        ),
        encoding="utf-8",
    )
    (tmp_path / "tailwind.config.ts").write_text("export default {}", encoding="utf-8")
    (tmp_path / "components.json").write_text(
        '{"$schema":"https://ui.shadcn.com/schema.json"}', encoding="utf-8"
    )
    score = adapter.detect(tmp_path)
    assert score >= 0.7, f"detect score too low: {score}"


def test_detect_scores_bare_repo_low(adapter: NextjsTailwindShadcnAdapter, tmp_path: Path):
    (tmp_path / "package.json").write_text(
        json.dumps({"name": "bare", "dependencies": {"express": "4.19.0"}}),
        encoding="utf-8",
    )
    score = adapter.detect(tmp_path)
    assert score <= 0.15, f"detect should be low for non-matching repo: {score}"


def test_merge_idempotent_on_globals_css(adapter: NextjsTailwindShadcnAdapter, tmp_path: Path):
    bundle = load_preset_bundle(PRESETS_ROOT / "dashboard--minimal-tech")

    # First apply — clean install.
    ops1 = adapter.render(bundle, tmp_path, "light", locale="en")
    adapter.apply(tmp_path, ops1)
    globals_path = tmp_path / "app/globals.css"
    original = globals_path.read_text(encoding="utf-8")

    # Add user-owned CSS outside the managed block.
    user_suffix = "\n\n/* user-owned styles */\n.my-button { color: red; }\n"
    globals_path.write_text(original + user_suffix, encoding="utf-8")

    # Second apply — should preserve user block and update generated block.
    ops2 = adapter.render(bundle, tmp_path, "light", locale="en")
    report = adapter.apply(tmp_path, ops2)
    assert "app/globals.css" in report.merged
    assert not report.proposed

    updated = globals_path.read_text(encoding="utf-8")
    assert ".my-button { color: red; }" in updated, "user CSS must survive merge"
    assert "design-ontology:START" in updated and "design-ontology:END" in updated


def test_merge_falls_back_to_proposed_when_markers_missing(
    adapter: NextjsTailwindShadcnAdapter, tmp_path: Path
):
    bundle = load_preset_bundle(PRESETS_ROOT / "dashboard--minimal-tech")
    # Pre-existing tailwind.config.ts with NO design-ontology markers.
    (tmp_path / "tailwind.config.ts").write_text(
        "export default { content: ['./app/**/*.tsx'] };\n", encoding="utf-8"
    )

    ops = adapter.render(bundle, tmp_path, "light", locale="en")
    report = adapter.apply(tmp_path, ops)
    assert any(path == "tailwind.config.ts.ds-proposed" for path, _ in report.proposed), (
        f"expected tailwind.config.ts to land as .ds-proposed, got {report.proposed}"
    )
    # User's original config must be untouched.
    preserved = (tmp_path / "tailwind.config.ts").read_text(encoding="utf-8")
    assert "./app/**/*.tsx" in preserved


def test_components_json_deep_merge_preserves_user_aliases(
    adapter: NextjsTailwindShadcnAdapter, tmp_path: Path
):
    bundle = load_preset_bundle(PRESETS_ROOT / "dashboard--minimal-tech")
    (tmp_path / "components.json").write_text(
        json.dumps(
            {
                "$schema": "https://ui.shadcn.com/schema.json",
                "style": "default",
                "rsc": True,
                "tsx": True,
                "tailwind": {
                    "config": "tailwind.config.ts",
                    "css": "app/globals.css",
                    "baseColor": "slate",
                    "cssVariables": True,
                    "prefix": "",
                },
                "aliases": {
                    "components": "@/components",
                    "utils": "@/lib/utils",
                    "ui": "@/components/ui",
                    "hooks": "@/hooks",
                    "lib": "@/lib",
                    "user-custom": "@/src/user-custom",
                },
            },
            ensure_ascii=False,
            indent=2,
        ),
        encoding="utf-8",
    )

    ops = adapter.render(bundle, tmp_path, "light", locale="en")
    report = adapter.apply(tmp_path, ops)
    assert "components.json" in report.merged, report

    merged = json.loads((tmp_path / "components.json").read_text(encoding="utf-8"))
    assert merged["aliases"]["user-custom"] == "@/src/user-custom", (
        "user alias must survive deep-merge"
    )
    assert merged["x-design-ontology"]["preset"] == "dashboard--minimal-tech"


# ---------------------------------------------------------------------------
# Helpers — regex-based parse validation


def _assert_tailwind_config_ok(text: str, color_modes: list[str]) -> None:
    assert "design-ontology:START" in text and "design-ontology:END" in text
    assert "import type { Config }" in text
    assert "export default config" in text
    assert "theme:" in text and "extend:" in text
    assert "darkMode" in text
    if "dark" in color_modes:
        assert "[data-theme='dark']" in text, "dark mode selector must be wired when preset supports dark"
    # Brace balance (minus the comment block markers)
    body = text.replace("/* design-ontology:START */", "").replace("/* design-ontology:END */", "")
    opens = body.count("{")
    closes = body.count("}")
    assert opens == closes, f"unbalanced braces in tailwind.config.ts ({opens} vs {closes})"
    # All color values route through CSS vars
    assert "var(--ds-color-primary)" in text
    assert "var(--ds-color-accent)" in text


def _assert_globals_css_ok(text: str, color_modes: list[str]) -> None:
    assert "design-ontology:START" in text and "design-ontology:END" in text
    assert ":root" in text
    # At least the core tokens must be declared
    for required in ("--ds-color-primary", "--ds-color-surface", "--ds-color-ink", "--ds-color-border"):
        assert required in text, f"missing {required} in globals.css"
    # Every declaration ends with a semicolon and each value parses as a color/var
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
    # Brace balance
    opens = text.count("{")
    closes = text.count("}")
    assert opens == closes, f"unbalanced braces in globals.css ({opens} vs {closes})"
