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
    COMMERCIAL_PRODUCT_REALISM_POLICY,
    ICON_REFACTOR_POLICY,
    MOCKUP_VISUAL_SUBSTANCE_POLICY,
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


def test_flags_homogeneous_card_wall_risk(tmp_path: Path):
    (tmp_path / "index.html").write_text(
        """
        <main class="card-grid">
          <section class="hero-card"></section>
          <article class="metric-card"></article>
          <article class="metric-card"></article>
          <article class="feature-card"></article>
          <article class="feature-card"></article>
          <aside class="summary-panel"></aside>
          <aside class="detail-panel"></aside>
        </main>
        """,
        encoding="utf-8",
    )
    (tmp_path / "styles.css").write_text(
        """
        .hero-card, .metric-card, .feature-card, .summary-panel, .detail-panel {
          border: 1px solid var(--ds-color-border);
          border-radius: var(--ds-radius-md);
          background: var(--ds-color-surface);
        }
        .card-grid { display: grid; gap: 12px; }
        """,
        encoding="utf-8",
    )

    report = lint_implementation(tmp_path)
    codes = {issue.code for issue in report.issues}

    assert not report.ok
    assert "DS070" in codes


def test_flags_icon_starved_interactive_surface(tmp_path: Path):
    (tmp_path / "design-system").mkdir()
    (tmp_path / "index.html").write_text(
        """
        <main>
          <nav><button>저장</button><button>공유</button></nav>
          <section class="filter-toolbar">
            <button class="filter-chip">아침</button>
            <button class="filter-chip">저녁</button>
            <button class="status-badge">활성</button>
            <button class="primary-action">장소 기록</button>
          </section>
        </main>
        """,
        encoding="utf-8",
    )

    report = lint_implementation(tmp_path)
    codes = {issue.code for issue in report.issues}

    assert not report.ok
    assert "DS071" in codes


def test_flags_missing_domain_visual_substance(tmp_path: Path):
    (tmp_path / "design-system").mkdir()
    (tmp_path / "design-system" / "brand_profile.json").write_text(
        '{"product_summary": "서울 장소와 골목을 추천하는 지도 앱"}',
        encoding="utf-8",
    )
    (tmp_path / "index.html").write_text(
        """
        <main>
          <button class="filter-chip"><svg class="icon"><use href="#icon-clock" /></svg>아침</button>
          <button class="filter-chip"><svg class="icon"><use href="#icon-clock" /></svg>저녁</button>
          <button class="primary-action"><svg class="icon"><use href="#icon-plus" /></svg>장소 기록</button>
          <section class="result-list">
            <div class="place-row">서촌 골목</div>
            <div class="place-row">을지로 골목</div>
          </section>
        </main>
        """,
        encoding="utf-8",
    )

    report = lint_implementation(tmp_path)
    codes = {issue.code for issue in report.issues}

    assert not report.ok
    assert "DS072" in codes


def test_flags_low_information_inline_domain_svg(tmp_path: Path):
    (tmp_path / "design-system").mkdir()
    (tmp_path / "design-system" / "brand_profile.json").write_text(
        '{"product_summary": "서울 장소와 골목을 추천하는 지도 앱"}',
        encoding="utf-8",
    )
    (tmp_path / "index.html").write_text(
        """
        <main>
          <section class="map-visual">
            <svg class="alley-map" viewBox="0 0 200 120" role="img" aria-label="골목 그림">
              <path d="M10 90h180" />
              <path d="M24 32h50v58H24Z" />
              <path d="M126 24h44v66h-44Z" />
              <circle cx="92" cy="58" r="12" />
            </svg>
          </section>
          <figure class="place-illustration">서촌 장소</figure>
        </main>
        """,
        encoding="utf-8",
    )

    report = lint_implementation(tmp_path)
    codes = {issue.code for issue in report.issues}

    assert not report.ok
    assert "DS073" in codes


def test_allows_semantic_inline_domain_svg(tmp_path: Path):
    (tmp_path / "design-system").mkdir()
    (tmp_path / "design-system" / "brand_profile.json").write_text(
        '{"product_summary": "서울 장소와 골목을 추천하는 지도 앱"}',
        encoding="utf-8",
    )
    (tmp_path / "index.html").write_text(
        """
        <main>
          <section class="map-visual">
            <svg class="alley-map" viewBox="0 0 200 120" role="img" aria-labelledby="mapTitle mapDesc">
              <title id="mapTitle">서촌 산책선 지도</title>
              <desc id="mapDesc">서점, 찻집, 계단을 감각 신호와 연결한 지도</desc>
              <g data-subject="paper-alley">
                <path d="M10 90h180" />
                <path d="M24 32h50v58H24Z" />
                <path d="M126 24h44v66h-44Z" />
                <circle cx="92" cy="58" r="12" />
                <text x="24" y="28">서점 골목</text>
              </g>
            </svg>
          </section>
          <figure class="place-illustration">서촌 장소</figure>
        </main>
        """,
        encoding="utf-8",
    )

    report = lint_implementation(tmp_path)
    codes = {issue.code for issue in report.issues}

    assert "DS073" not in codes


def test_flags_ad_hoc_sketch_domain_visual(tmp_path: Path):
    (tmp_path / "design-system").mkdir()
    (tmp_path / "design-system" / "brand_profile.json").write_text(
        '{"product_summary": "서울 장소와 골목을 추천하는 지도 앱"}',
        encoding="utf-8",
    )
    (tmp_path / "index.html").write_text(
        """
        <main>
          <section class="map-visual">
            <svg class="place-sketch" viewBox="0 0 200 120" role="img" aria-labelledby="mapTitle mapDesc">
              <title id="mapTitle">골목 그림</title>
              <desc id="mapDesc">즉흥 스케치</desc>
              <g data-subject="alley">
                <path d="M10 90h180" />
                <path d="M24 32h50v58H24Z" />
                <path d="M126 24h44v66h-44Z" />
                <circle cx="92" cy="58" r="12" />
                <text x="24" y="28">서점 골목</text>
              </g>
            </svg>
          </section>
          <figure class="place-visual">서촌 장소</figure>
        </main>
        """,
        encoding="utf-8",
    )

    report = lint_implementation(tmp_path)
    codes = {issue.code for issue in report.issues}

    assert not report.ok
    assert "DS074" in codes


def test_flags_ambiguous_mock_runtime_surface(tmp_path: Path):
    (tmp_path / "design-system").mkdir()
    (tmp_path / "design-system" / "brand_profile.json").write_text(
        '{"product_summary": "서울 장소와 골목을 추천하는 지도 앱"}',
        encoding="utf-8",
    )
    (tmp_path / "index.html").write_text(
        """
        <main>
          <section class="map-visual schematic-map">
            <div class="placeholder-map">서촌 감각 도식</div>
          </section>
          <figure class="place-visual">장소 이미지</figure>
        </main>
        """,
        encoding="utf-8",
    )

    report = lint_implementation(tmp_path)
    codes = {issue.code for issue in report.issues}

    assert not report.ok
    assert "DS075" in codes


def test_allows_declared_runtime_surface(tmp_path: Path):
    (tmp_path / "design-system").mkdir()
    (tmp_path / "design-system" / "brand_profile.json").write_text(
        '{"product_summary": "서울 장소와 골목을 추천하는 지도 앱"}',
        encoding="utf-8",
    )
    (tmp_path / "index.html").write_text(
        """
        <main>
          <section class="map-visual" data-runtime-surface="map-sdk-layer">
            <div class="real-map">서촌 지도 레이어</div>
          </section>
          <figure class="place-visual" data-runtime-surface="generated-place-photo">장소 이미지</figure>
        </main>
        """,
        encoding="utf-8",
    )

    report = lint_implementation(tmp_path)
    codes = {issue.code for issue in report.issues}

    assert "DS075" not in codes


def test_flags_media_runtime_surface_without_asset(tmp_path: Path):
    (tmp_path / "design-system").mkdir()
    (tmp_path / "design-system" / "brand_profile.json").write_text(
        '{"product_summary": "서울 장소와 골목을 추천하는 지도 앱"}',
        encoding="utf-8",
    )
    (tmp_path / "index.html").write_text(
        """
        <main>
          <section class="map-visual" data-runtime-surface="map-sdk-layer">
            <div class="real-map">서촌 지도 레이어</div>
          </section>
          <section class="place-media-surface" data-runtime-surface="place-media-evidence">
            <figure class="place-photo">패턴만 있는 장소 사진 슬롯</figure>
          </section>
        </main>
        """,
        encoding="utf-8",
    )

    report = lint_implementation(tmp_path)
    codes = {issue.code for issue in report.issues}

    assert not report.ok
    assert "DS076" in codes


def test_allows_media_runtime_surface_with_image_asset(tmp_path: Path):
    (tmp_path / "design-system").mkdir()
    (tmp_path / "design-system" / "brand_profile.json").write_text(
        '{"product_summary": "서울 장소와 골목을 추천하는 지도 앱"}',
        encoding="utf-8",
    )
    (tmp_path / "index.html").write_text(
        """
        <main>
          <section class="map-visual" data-runtime-surface="map-sdk-layer">
            <div class="real-map">서촌 지도 레이어</div>
          </section>
          <section class="place-media-surface" data-runtime-surface="place-media-evidence">
            <figure class="place-photo"><img src="./assets/place.png" alt="장소 사진" /></figure>
          </section>
        </main>
        """,
        encoding="utf-8",
    )

    report = lint_implementation(tmp_path)
    codes = {issue.code for issue in report.issues}

    assert "DS076" not in codes


def test_flags_individual_media_tile_without_asset(tmp_path: Path):
    (tmp_path / "design-system").mkdir()
    (tmp_path / "design-system" / "brand_profile.json").write_text(
        '{"product_summary": "서울 장소와 골목을 추천하는 지도 앱"}',
        encoding="utf-8",
    )
    (tmp_path / "index.html").write_text(
        """
        <main>
          <section class="place-media-surface" data-runtime-surface="place-media-evidence">
            <figure class="place-photo"><img src="./assets/place.png" alt="장소 사진" /></figure>
            <figure class="texture-card">패턴만 남은 질감 카드</figure>
          </section>
        </main>
        """,
        encoding="utf-8",
    )

    report = lint_implementation(tmp_path)
    codes = {issue.code for issue in report.issues}

    assert not report.ok
    assert "DS078" in codes


def test_allows_explicit_pending_media_tile_without_asset(tmp_path: Path):
    (tmp_path / "design-system").mkdir()
    (tmp_path / "design-system" / "brand_profile.json").write_text(
        '{"product_summary": "서울 장소와 골목을 추천하는 지도 앱"}',
        encoding="utf-8",
    )
    (tmp_path / "index.html").write_text(
        """
        <main>
          <section class="place-media-surface" data-runtime-surface="place-media-evidence">
            <figure class="place-photo"><img src="./assets/place.png" alt="장소 사진" /></figure>
            <figure class="texture-card" data-state="pending">수집 대기</figure>
          </section>
        </main>
        """,
        encoding="utf-8",
    )

    report = lint_implementation(tmp_path)
    codes = {issue.code for issue in report.issues}

    assert "DS078" not in codes


def test_flags_generic_initials_brand_mark_without_app_icon(tmp_path: Path):
    (tmp_path / "design-system").mkdir()
    (tmp_path / "index.html").write_text(
        """
        <header>
          <span class="brand-mark">AS</span>
        </header>
        """,
        encoding="utf-8",
    )

    report = lint_implementation(tmp_path)
    codes = {issue.code for issue in report.issues}

    assert not report.ok
    assert "DS077" in codes


def test_allows_wired_app_icon_brand_mark(tmp_path: Path):
    (tmp_path / "design-system").mkdir()
    (tmp_path / "index.html").write_text(
        """
        <head>
          <link rel="icon" href="./assets/app-icon.svg" type="image/svg+xml" />
          <link rel="manifest" href="./manifest.webmanifest" />
        </head>
        <header>
          <span class="brand-mark"><img src="./assets/app-icon.svg" alt="" /></span>
        </header>
        """,
        encoding="utf-8",
    )

    report = lint_implementation(tmp_path)
    codes = {issue.code for issue in report.issues}

    assert "DS077" not in codes


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


def test_excludes_design_system_but_flags_managed_blocks_in_implementation(tmp_path: Path):
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
    codes = {issue.code for issue in report.issues}

    assert not report.ok
    assert "DS061" in codes
    assert "DS001" not in codes
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
    assert "Do not hard-code hex/rgb/hsl colors in implementation files" in contract
    assert "tokens.css" in contract
    assert "Color Mode Parity" in contract
    assert "normal light mode and dark mode" in contract
    assert "Responsive Resilience" in contract
    assert "320, 360, 390, 430" in contract
    assert "Buttons, CTAs, tabs, chips" in contract
    assert "Emoji-to-SVG Refactor" in contract
    assert "existing icon library" in contract
    assert "Icon And Visual Affordance Coverage" in contract
    assert "Visual Evidence And Screenshot Comparison" in contract
    assert "Mock Fidelity And Runtime Representation" in contract
    assert "data-runtime-surface" in contract
    assert "compare-visuals" in contract
    assert "image_gen" in contract
    assert "DS070" in contract
    assert "DS071" in contract
    assert "DS072" in contract
    assert "DS073" in contract
    assert "DS074" in contract
    assert "DS075" in contract
    assert "DS076" in contract
    assert "DS077" in contract
    assert "DS078" in contract
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
    assert any("Horizontal rails" in rule for rule in RESPONSIVE_RESILIENCE_POLICY["control_rules"])
    pattern_ids = {item["id"] for item in RESPONSIVE_RESILIENCE_POLICY["failure_patterns"]}
    assert {"mobile-control-overflow", "viewport-horizontal-overflow", "horizontal-rail-label-clipping"} <= pattern_ids
    assert "lint-implementation" in RESPONSIVE_RESILIENCE_POLICY["outputs"]


def test_commercial_product_realism_success_patterns_are_structured_for_ontology():
    assert COMMERCIAL_PRODUCT_REALISM_POLICY["id"] == "commercial-product-realism"
    pattern_ids = {item["id"] for item in COMMERCIAL_PRODUCT_REALISM_POLICY["successful_patterns"]}
    assert "same-domain-reference-before-redesign" in pattern_ids
    assert "score-ticker-as-scan-surface" in pattern_ids
    assert "national-flag-code-identity" in pattern_ids
    assert "source-ledger-and-sample-labeling" in pattern_ids
    assert "editorial-insight-side-rail" in pattern_ids
    assert "dual-mode-screenshot-qa" in pattern_ids
    assert "brand-app-icon-as-required-identity" in pattern_ids
    failure_ids = {item["id"] for item in COMMERCIAL_PRODUCT_REALISM_POLICY["failure_patterns"]}
    assert "generic-national-team-badges" in failure_ids
    assert "untokenized-domain-identity-colors" in failure_ids
    assert "unverified-redesign-screenshot" in failure_ids
    card_wall = next(item for item in COMMERCIAL_PRODUCT_REALISM_POLICY["failure_patterns"] if item["id"] == "homogeneous-card-wall")
    assert "lint-implementation DS070" in card_wall["technical_controls"]
    unverified = next(item for item in COMMERCIAL_PRODUCT_REALISM_POLICY["failure_patterns"] if item["id"] == "unverified-redesign-screenshot")
    assert "compare-visuals" in unverified["technical_controls"]
    assert "compare-visuals" in COMMERCIAL_PRODUCT_REALISM_POLICY["outputs"]


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
    failure_ids = {item["id"] for item in ICON_REFACTOR_POLICY["failure_patterns"]}
    assert {"emoji-ui-affordance", "icon-starved-control-surface"} <= failure_ids
    assert "lint-implementation" in ICON_REFACTOR_POLICY["outputs"]


def test_mockup_visual_substance_policy_flags_low_information_svg():
    failure_ids = {item["id"] for item in MOCKUP_VISUAL_SUBSTANCE_POLICY["failure_patterns"]}
    assert "low-information-inline-svg-visual" in failure_ids
    assert "amateur-ad-hoc-illustration" in failure_ids
    assert "ambiguous-mock-runtime-surface" in failure_ids
    assert "media-runtime-surface-without-asset" in failure_ids
    assert "media-tile-without-asset" in failure_ids
    low_info = next(item for item in MOCKUP_VISUAL_SUBSTANCE_POLICY["failure_patterns"] if item["id"] == "low-information-inline-svg-visual")
    assert "lint-implementation DS073" in low_info["technical_controls"]
    amateur = next(item for item in MOCKUP_VISUAL_SUBSTANCE_POLICY["failure_patterns"] if item["id"] == "amateur-ad-hoc-illustration")
    assert "lint-implementation DS074" in amateur["technical_controls"]
    assert "image_gen" in amateur["prevention"]
    ambiguous = next(item for item in MOCKUP_VISUAL_SUBSTANCE_POLICY["failure_patterns"] if item["id"] == "ambiguous-mock-runtime-surface")
    assert "lint-implementation DS075" in ambiguous["technical_controls"]
    media = next(item for item in MOCKUP_VISUAL_SUBSTANCE_POLICY["failure_patterns"] if item["id"] == "media-runtime-surface-without-asset")
    assert "lint-implementation DS076" in media["technical_controls"]
    tile = next(item for item in MOCKUP_VISUAL_SUBSTANCE_POLICY["failure_patterns"] if item["id"] == "media-tile-without-asset")
    assert "lint-implementation DS078" in tile["technical_controls"]


def test_app_icon_identity_policy_is_structured_for_ontology():
    assert APP_ICON_IDENTITY_POLICY["id"] == "brand-app-icon-identity"
    assert APP_ICON_IDENTITY_POLICY["required_assets"][0]["id"] == "identity-asset:app-icon"
    assert "favicon" in APP_ICON_IDENTITY_POLICY["required_assets"][0]["targets"]
    assert APP_ICON_IDENTITY_POLICY["failure_patterns"][0]["id"] == "generic-initials-app-icon"
    assert "lint-implementation DS077" in APP_ICON_IDENTITY_POLICY["failure_patterns"][0]["technical_controls"]
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
