from __future__ import annotations

import subprocess
import sys
from pathlib import Path

from design_ontology_harness.adapters import load_preset_bundle
from design_ontology_harness.adapters.base import implementation_contract
from design_ontology_harness.implementation_linter import lint_implementation
from design_ontology_harness.synthesis import (
    APP_ICON_IDENTITY_POLICY,
    COLOR_MODE_PARITY_POLICY,
    ICON_REFACTOR_POLICY,
    REFERENCE_ABSORPTION_SCOPE,
    RESPONSIVE_RESILIENCE_POLICY,
)


REPO_ROOT = Path(__file__).resolve().parent.parent


def test_token_bound_css_passes(tmp_path: Path):
    (tmp_path / "design-system").mkdir()
    (tmp_path / "design-system" / "tokens.css").write_text(
        ":root { --ds-color-primary: #0071A8; --ds-radius-sm: 4px; }\n",
        encoding="utf-8",
    )
    (tmp_path / "styles.css").write_text(
        """
        .panel {
          color: var(--ds-color-ink);
          background: color-mix(in srgb, var(--ds-color-surface-tint) 24%, var(--ds-color-surface));
          border-color: var(--ds-color-border);
          border-radius: var(--ds-radius-sm);
          font-family: var(--ds-font-ko);
        }
        .dot { border-radius: 999px; }
        """,
        encoding="utf-8",
    )

    report = lint_implementation(tmp_path)

    assert report.ok
    assert report.checked_files == ["styles.css"]


def test_flags_hardcoded_visual_values(tmp_path: Path):
    (tmp_path / "styles.css").write_text(
        """
        .bad {
          color: #123456;
          background: rgb(10, 20, 30);
          border-color: teal;
          border-radius: 8px;
          font-family: Inter, sans-serif;
        }
        """,
        encoding="utf-8",
    )

    report = lint_implementation(tmp_path)
    codes = {issue.code for issue in report.issues}

    assert not report.ok
    assert {"DS001", "DS002", "DS003", "DS010", "DS020"} <= codes


def test_flags_token_bound_reference_palette_mixing(tmp_path: Path):
    (tmp_path / "styles.css").write_text(
        """
        :root {
          --chart-secondary: color-mix(in srgb, var(--ds-color-info) 52%, var(--ds-color-surface-tint));
          --sidebar-bg: color-mix(in srgb, var(--ds-color-info) 84%, var(--ds-color-ink) 16%);
          --panel-shadow: color-mix(in srgb, var(--ds-color-ink) 12%, transparent);
        }
        """,
        encoding="utf-8",
    )

    report = lint_implementation(tmp_path)
    codes = {issue.code for issue in report.issues}

    assert not report.ok
    assert {"DS030", "DS031"} <= codes


def test_flags_mobile_button_overflow_patterns(tmp_path: Path):
    (tmp_path / "styles.css").write_text(
        """
        .hero-actions {
          display: flex;
          flex-wrap: nowrap;
        }
        .cta-button {
          min-width: 360px;
          white-space: nowrap;
        }
        .page-shell {
          width: 100vw;
        }
        """,
        encoding="utf-8",
    )

    report = lint_implementation(tmp_path)
    codes = {issue.code for issue in report.issues}

    assert not report.ok
    assert {"DS040", "DS041", "DS042", "DS043"} <= codes


def test_flags_tailwind_mobile_button_overflow_patterns(tmp_path: Path):
    (tmp_path / "Button.tsx").write_text(
        """
        export function Button() {
          return <button className="cta-button min-w-[360px] whitespace-nowrap">긴 CTA 버튼 문구</button>
        }
        export function Shell() {
          return <main className="w-screen px-6" />
        }
        """,
        encoding="utf-8",
    )

    report = lint_implementation(tmp_path)
    codes = {issue.code for issue in report.issues}

    assert not report.ok
    assert {"DS040", "DS041", "DS043"} <= codes


def test_flags_emoji_used_as_ui_affordance(tmp_path: Path):
    (tmp_path / "Cards.tsx").write_text(
        """
        export function Actions() {
          return (
            <section>
              <button className="primary-button">🚀 시작하기</button>
              <article className="feature-card"><span className="feature-icon">🔥</span><h3>자동 분석</h3></article>
              <span className="status-badge">✅ 완료</span>
            </section>
          )
        }
        """,
        encoding="utf-8",
    )

    report = lint_implementation(tmp_path)
    codes = {issue.code for issue in report.issues}

    assert not report.ok
    assert "DS050" in codes


def test_allows_emoji_in_user_generated_content_context(tmp_path: Path):
    (tmp_path / "Post.tsx").write_text(
        """
        export function Post() {
          return <article className="blog-body">오늘 기분은 😊 입니다.</article>
        }
        export const emojiPickerOptions = ["🔥", "✅", "🚀"]
        """,
        encoding="utf-8",
    )

    report = lint_implementation(tmp_path)

    assert report.ok


def test_flags_dark_only_color_mode(tmp_path: Path):
    (tmp_path / "styles.css").write_text(
        """
        :root {
          color-scheme: dark;
          --ds-color-canvas: #061116;
        }
        """,
        encoding="utf-8",
    )

    report = lint_implementation(tmp_path)
    codes = {issue.code for issue in report.issues}

    assert not report.ok
    assert "DS060" in codes


def test_allows_light_and_dark_color_modes(tmp_path: Path):
    (tmp_path / "styles.css").write_text(
        """
        :root {
          color-scheme: light;
          --ds-color-canvas: var(--brand-light);
        }
        [data-theme="dark"] {
          color-scheme: dark;
          --ds-color-canvas: var(--brand-dark);
        }
        """,
        encoding="utf-8",
    )

    report = lint_implementation(tmp_path)
    codes = {issue.code for issue in report.issues}

    assert "DS060" not in codes


def test_ignores_design_system_and_managed_blocks(tmp_path: Path):
    (tmp_path / "design-system").mkdir()
    (tmp_path / "design-system" / "tokens.css").write_text(
        ":root { --ds-color-primary: #0071A8; }\n",
        encoding="utf-8",
    )
    (tmp_path / "app.css").write_text(
        """
        /* design-ontology:START */
        :root { --ds-color-primary: #0071A8; }
        body { font-family: Inter, sans-serif; color: #111111; border-radius: 8px; }
        /* design-ontology:END */

        .user {
          color: var(--ds-color-ink);
          border-radius: var(--ds-radius-sm);
          font-family: var(--ds-font-body);
        }
        """,
        encoding="utf-8",
    )

    report = lint_implementation(tmp_path)

    assert report.ok
    assert report.checked_files == ["app.css"]


def test_implementation_contract_declares_reference_scope():
    bundle = load_preset_bundle(REPO_ROOT / "presets" / "conversation-copilot--corporate-trust")
    contract = implementation_contract(bundle)

    assert "Reference Absorption Scope" in contract
    assert "Allowed from visual references" in contract
    assert "Denied from visual references" in contract
    assert "color palette" in contract
    assert "palette composition or derived secondary palettes" in contract
    assert "Feedback Promotion Rule" in contract
    assert "Color Mode Parity" in contract
    assert "normal light mode and dark mode" in contract
    assert "Responsive Resilience" in contract
    assert "320, 360, 390, 430" in contract
    assert "Buttons, CTAs, tabs, chips" in contract
    assert "Emoji-to-SVG Refactor" in contract
    assert "existing icon library" in contract
    assert "uv run design-ontology lint-implementation --target-repo ." in contract


def test_reference_absorption_scope_is_structured_for_ontology():
    assert "component morphology" in REFERENCE_ABSORPTION_SCOPE["allowed"]
    assert "layout density" in REFERENCE_ABSORPTION_SCOPE["allowed"]
    assert "color palette" in REFERENCE_ABSORPTION_SCOPE["denied"]
    assert "palette composition or derived secondary palettes" in REFERENCE_ABSORPTION_SCOPE["denied"]
    assert "typography family or scale" in REFERENCE_ABSORPTION_SCOPE["denied"]
    assert "product data model" in REFERENCE_ABSORPTION_SCOPE["denied"]
    assert REFERENCE_ABSORPTION_SCOPE["failure_patterns"][0]["id"] == "token-bound-reference-palette-mixing"
    assert REFERENCE_ABSORPTION_SCOPE["promotion_policy"]["id"] == "implementation-feedback-promotion"


def test_responsive_resilience_policy_is_structured_for_ontology():
    assert RESPONSIVE_RESILIENCE_POLICY["id"] == "responsive-resilience"
    assert 320 in RESPONSIVE_RESILIENCE_POLICY["viewport_contract"]["required_widths_px"]
    assert any("Buttons" in rule for rule in RESPONSIVE_RESILIENCE_POLICY["control_rules"])
    pattern_ids = {item["id"] for item in RESPONSIVE_RESILIENCE_POLICY["failure_patterns"]}
    assert {"mobile-control-overflow", "viewport-horizontal-overflow"} <= pattern_ids
    assert "lint-implementation" in RESPONSIVE_RESILIENCE_POLICY["outputs"]


def test_color_mode_parity_policy_is_structured_for_ontology():
    assert COLOR_MODE_PARITY_POLICY["id"] == "color-mode-parity"
    assert COLOR_MODE_PARITY_POLICY["required_modes"] == ["light", "dark"]
    assert COLOR_MODE_PARITY_POLICY["default_mode"] == "light"
    pattern_ids = {item["id"] for item in COLOR_MODE_PARITY_POLICY["failure_patterns"]}
    assert {"dark-only-implementation", "theme-token-drift"} <= pattern_ids
    assert "lint-implementation" in COLOR_MODE_PARITY_POLICY["outputs"]


def test_icon_refactor_policy_is_structured_for_ontology():
    assert ICON_REFACTOR_POLICY["id"] == "emoji-to-svg-refactor"
    assert "button" in ICON_REFACTOR_POLICY["targets"]
    assert any("existing icon library" in item for item in ICON_REFACTOR_POLICY["replacement_order"])
    assert ICON_REFACTOR_POLICY["failure_patterns"][0]["id"] == "emoji-ui-affordance"
    assert "lint-implementation" in ICON_REFACTOR_POLICY["outputs"]


def test_app_icon_identity_policy_is_structured_for_ontology():
    assert APP_ICON_IDENTITY_POLICY["id"] == "brand-app-icon-identity"
    assert APP_ICON_IDENTITY_POLICY["required_assets"][0]["id"] == "identity-asset:app-icon"
    assert "favicon" in APP_ICON_IDENTITY_POLICY["required_assets"][0]["targets"]
    assert APP_ICON_IDENTITY_POLICY["failure_patterns"][0]["id"] == "generic-initials-app-icon"
    assert "system_ontology.json" in APP_ICON_IDENTITY_POLICY["outputs"]


def test_cli_exits_nonzero_on_implementation_violation(tmp_path: Path):
    (tmp_path / "styles.css").write_text(
        ".bad { color: #123456; }\n",
        encoding="utf-8",
    )

    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "design_ontology_harness.cli",
            "lint-implementation",
            "--target-repo",
            str(tmp_path),
        ],
        cwd=REPO_ROOT,
        text=True,
        capture_output=True,
        check=False,
    )

    assert result.returncode == 1
    assert "DS001" in result.stdout
