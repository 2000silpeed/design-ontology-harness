from __future__ import annotations

from pathlib import Path

from design_ontology_harness.implementation_linter import lint_implementation


def _codes(report) -> set[str]:
    return {issue.code for issue in report.issues}


def _write_ui(tmp_path: Path, css: str, html: str = "<main class='app-mockup'></main>") -> Path:
    (tmp_path / "index.html").write_text(
        f"<html><head><link rel='stylesheet' href='styles.css'></head><body>{html}</body></html>",
        encoding="utf-8",
    )
    (tmp_path / "styles.css").write_text(css, encoding="utf-8")
    return tmp_path


def test_ds090_flags_doc_callout_border(tmp_path: Path):
    _write_ui(
        tmp_path,
        """
        .restraint-note {
          padding-left: var(--ds-space-3);
          border-left: 2px solid var(--ds-color-ink);
        }
        """,
    )
    report = lint_implementation(tmp_path)
    assert "DS090" in _codes(report)


def test_ds090_ignores_non_callout_selectors(tmp_path: Path):
    _write_ui(
        tmp_path,
        """
        .nav-item-active {
          border-left: 2px solid var(--ds-color-ink);
        }
        """,
    )
    report = lint_implementation(tmp_path)
    assert "DS090" not in _codes(report)


def test_ds091_flags_radius_monoculture(tmp_path: Path):
    rules = "\n".join(
        f".c{i} {{ border-radius: var(--ds-radius-md); }}" for i in range(9)
    )
    _write_ui(tmp_path, rules)
    report = lint_implementation(tmp_path)
    assert "DS091" in _codes(report)


def test_ds091_allows_two_step_radius(tmp_path: Path):
    rules = "\n".join(
        f".c{i} {{ border-radius: var(--ds-radius-{'sm' if i % 2 else 'lg'}); }}"
        for i in range(9)
    )
    _write_ui(tmp_path, rules)
    report = lint_implementation(tmp_path)
    assert "DS091" not in _codes(report)


def test_ds092_flags_hedging_weights(tmp_path: Path):
    _write_ui(
        tmp_path,
        """
        .a { font-weight: 500; }
        .b { font-weight: 600; }
        """,
    )
    report = lint_implementation(tmp_path)
    assert "DS092" in _codes(report)


def test_ds092_allows_anchored_weights(tmp_path: Path):
    _write_ui(
        tmp_path,
        """
        .a { font-weight: 400; }
        .b { font-weight: 700; }
        """,
    )
    report = lint_implementation(tmp_path)
    assert "DS092" not in _codes(report)


def test_ds093_flags_compressed_type_scale(tmp_path: Path):
    css = "\n".join(
        f".t{i} {{ font-size: {size}rem; }}"
        for i, size in enumerate(["0.75", "0.8125", "0.875", "0.9375", "1", "1.125", "1.25"])
    )
    _write_ui(tmp_path, css)
    report = lint_implementation(tmp_path)
    assert "DS093" in _codes(report)


def test_ds093_passes_with_display_tier(tmp_path: Path):
    css = "\n".join(
        f".t{i} {{ font-size: {size}rem; }}"
        for i, size in enumerate(["0.6875", "0.75", "0.875", "0.9375", "1.375", "2", "3.5"])
    )
    _write_ui(tmp_path, css)
    report = lint_implementation(tmp_path)
    assert "DS093" not in _codes(report)


def test_ds094_flags_placeholder_copy(tmp_path: Path):
    _write_ui(
        tmp_path,
        ".a { color: var(--ds-color-ink); }",
        html="<main class='app-mockup'><ul><li>항목 1</li><li>항목 2</li></ul></main>",
    )
    report = lint_implementation(tmp_path)
    assert "DS094" in _codes(report)


def test_ds095_flags_css_painted_gridfield(tmp_path: Path):
    _write_ui(
        tmp_path,
        """
        .compass-field {
          background:
            linear-gradient(var(--ds-color-border) 1px, transparent 1px),
            linear-gradient(90deg, var(--ds-color-border) 1px, transparent 1px);
          background-size: 25% 25%;
        }
        """,
    )
    report = lint_implementation(tmp_path)
    assert "DS095" in _codes(report)


def test_ds095_ignores_svg_instrument(tmp_path: Path):
    _write_ui(
        tmp_path,
        ".compass-instrument { display: block; width: 100%; }",
        html=(
            "<main class='app-mockup'><svg viewBox='0 0 320 200'><title>좌표 필드</title>"
            "<rect width='320' height='200' fill='var(--ds-color-surface)' />"
            "<line x1='160' y1='0' x2='160' y2='200' stroke='var(--ds-color-border)' />"
            "<circle cx='198' cy='118' r='11' fill='var(--ds-color-accent)' /></svg></main>"
        ),
    )
    report = lint_implementation(tmp_path)
    assert "DS095" not in _codes(report)


def test_ds096_flags_edge_status_bar(tmp_path: Path):
    _write_ui(
        tmp_path,
        """
        .post-row[data-state="unread"]::before {
          content: "";
          position: absolute;
          left: 0;
          top: var(--ds-space-5);
          bottom: var(--ds-space-5);
          width: 2px;
          background: var(--ds-color-ink);
        }
        """,
    )
    report = lint_implementation(tmp_path)
    assert "DS096" in _codes(report)


def test_ds096_ignores_inline_thread_spine(tmp_path: Path):
    _write_ui(
        tmp_path,
        """
        .thread-spine {
          position: absolute;
          left: calc(var(--ds-space-5) + 19px);
          top: 0;
          bottom: 0;
          width: 2px;
          background: var(--ds-color-border-strong);
        }
        """,
    )
    report = lint_implementation(tmp_path)
    assert "DS096" not in _codes(report)


def test_ds109_flags_transition_all_css_and_utility(tmp_path: Path):
    _write_ui(
        tmp_path,
        ".button { transition: all 180ms ease; }",
        html="<main class='app-mockup'><button class='transition-all'>Save</button></main>",
    )

    report = lint_implementation(tmp_path)

    assert "DS109" in _codes(report)


def test_ds109_allows_explicit_transition_properties(tmp_path: Path):
    _write_ui(
        tmp_path,
        ".button { transition: color 180ms ease, transform 180ms ease; }",
    )

    report = lint_implementation(tmp_path)

    assert "DS109" not in _codes(report)


def test_ds109_ignores_similarly_named_custom_property(tmp_path: Path):
    _write_ui(
        tmp_path,
        ":root { --transition-all: color 180ms ease; --transition: all 180ms ease; }",
    )

    report = lint_implementation(tmp_path)

    assert "DS109" not in _codes(report)


def test_ds110_flags_layout_property_transition(tmp_path: Path):
    _write_ui(
        tmp_path,
        ".drawer { transition: width 220ms ease, margin-left 220ms ease; }",
    )

    report = lint_implementation(tmp_path)

    assert "DS110" in _codes(report)


def test_ds110_flags_multiline_layout_property_transition(tmp_path: Path):
    _write_ui(
        tmp_path,
        """
        .drawer {
          transition:
            inline-size 220ms ease,
            opacity 180ms ease;
        }
        """,
    )

    report = lint_implementation(tmp_path)

    assert "DS110" in _codes(report)


def test_ds110_allows_compositor_property_transition(tmp_path: Path):
    _write_ui(
        tmp_path,
        ".drawer { transition: transform 220ms ease, opacity 180ms ease; }",
    )

    report = lint_implementation(tmp_path)

    assert "DS110" not in _codes(report)


def test_ds110_ignores_custom_property_and_flags_logical_layout_property(tmp_path: Path):
    _write_ui(
        tmp_path,
        """
        :root { --transition: width 220ms ease; }
        .drawer { transition: inline-size 220ms ease; }
        """,
    )

    report = lint_implementation(tmp_path)

    ds110 = [issue for issue in report.issues if issue.code == "DS110"]
    assert len(ds110) == 1
    assert ".drawer" in ds110[0].snippet


def test_ds111_flags_animation_without_reduced_motion_fallback(tmp_path: Path):
    _write_ui(
        tmp_path,
        """
        .loader { animation: spin 600ms linear infinite; }
        @keyframes spin { to { transform: rotate(1turn); } }
        """,
    )

    report = lint_implementation(tmp_path)

    assert "DS111" in _codes(report)
    issue = next(issue for issue in report.issues if issue.code == "DS111")
    assert issue.path == "styles.css"
    assert issue.line == 2
    assert issue.column == 19


def test_ds111_ignores_similarly_named_custom_property(tmp_path: Path):
    _write_ui(
        tmp_path,
        ":root { --animation: spin 600ms linear infinite; }",
    )

    report = lint_implementation(tmp_path)

    assert "DS111" not in _codes(report)


def test_ds111_allows_explicit_animation_none_reset(tmp_path: Path):
    _write_ui(
        tmp_path,
        ".loader, .reset { animation: none; animation-name: none; }",
    )

    report = lint_implementation(tmp_path)

    assert "DS111" not in _codes(report)


def test_ds111_ignores_commented_animation(tmp_path: Path):
    _write_ui(
        tmp_path,
        "/* .loader { animation: spin 600ms linear infinite; } */",
    )

    report = lint_implementation(tmp_path)

    assert "DS111" not in _codes(report)


def test_ds111_rejects_empty_reduced_motion_query(tmp_path: Path):
    _write_ui(
        tmp_path,
        """
        .loader { animation: spin 600ms linear infinite; }
        @media (prefers-reduced-motion: reduce) { .loader { color: inherit; } }
        """,
    )

    report = lint_implementation(tmp_path)

    assert "DS111" in _codes(report)


def test_ds111_rejects_unrelated_reduced_motion_reset(tmp_path: Path):
    _write_ui(
        tmp_path,
        """
        .loader { animation: spin 600ms linear infinite; }
        @media (prefers-reduced-motion: reduce) {
          .decorative { animation: none; }
        }
        """,
    )

    report = lint_implementation(tmp_path)

    assert "DS111" in _codes(report)


def test_ds111_does_not_treat_descendant_wildcard_as_universal_reset(tmp_path: Path):
    _write_ui(
        tmp_path,
        """
        .loader { animation: spin 600ms linear infinite; }
        @media (prefers-reduced-motion: reduce) {
          * .decorative { animation: none; }
        }
        """,
    )

    report = lint_implementation(tmp_path)

    assert "DS111" in _codes(report)


def test_ds111_runs_for_css_only_packages(tmp_path: Path):
    (tmp_path / "motion.css").write_text(
        ".loader { animation: spin 600ms linear infinite; }",
        encoding="utf-8",
    )

    report = lint_implementation(tmp_path)

    assert "DS111" in _codes(report)


def test_ds111_runs_inside_vue_style_blocks(tmp_path: Path):
    (tmp_path / "App.vue").write_text(
        "<template><main /></template><style>.loader { animation: spin 600ms infinite; }</style>",
        encoding="utf-8",
    )

    report = lint_implementation(tmp_path)

    assert "DS111" in _codes(report)


def test_ds111_accepts_short_duration_reduced_motion_fallback(tmp_path: Path):
    _write_ui(
        tmp_path,
        """
        .loader { animation: spin 600ms linear infinite; }
        @media (prefers-reduced-motion: reduce) {
          .loader { animation-duration: 0.01ms; }
        }
        """,
    )

    report = lint_implementation(tmp_path)

    assert "DS111" not in _codes(report)


def test_ds111_accepts_cross_file_universal_reduced_motion_fallback(tmp_path: Path):
    _write_ui(
        tmp_path,
        ".loader { animation: spin 600ms linear infinite; }",
    )
    (tmp_path / "accessibility.css").write_text(
        """
        @media (prefers-reduced-motion: reduce) {
          *, *::before, *::after { animation-name: none !important; }
        }
        """,
        encoding="utf-8",
    )

    report = lint_implementation(tmp_path)

    assert "DS111" not in _codes(report)


def test_ds111_accepts_cross_file_selector_matched_fallback(tmp_path: Path):
    _write_ui(
        tmp_path,
        ".loader { animation: spin 600ms linear infinite; }",
    )
    (tmp_path / "accessibility.css").write_text(
        """
        @media (prefers-reduced-motion: reduce) {
          .loader { animation: none; }
        }
        """,
        encoding="utf-8",
    )

    report = lint_implementation(tmp_path)

    assert "DS111" not in _codes(report)


def test_motion_rules_ignore_ordinary_component_strings_and_none_style(tmp_path: Path):
    (tmp_path / "App.tsx").write_text(
        """
        const docs = 'transition: all 200ms';
        export function App() {
          return <main style={{ animation: 'none' }}>Ready</main>;
        }
        """,
        encoding="utf-8",
    )

    report = lint_implementation(tmp_path)

    assert not _codes(report) & {"DS109", "DS110", "DS111"}


def test_ds111_allows_animation_with_reduced_motion_fallback(tmp_path: Path):
    _write_ui(
        tmp_path,
        """
        .loader { animation: spin 600ms linear infinite; }
        @keyframes spin { to { transform: rotate(1turn); } }
        @media (prefers-reduced-motion: reduce) {
          .loader { animation: none; }
        }
        """,
    )

    report = lint_implementation(tmp_path)

    assert "DS111" not in _codes(report)


def test_realistic_surface_passes_all_tells(tmp_path: Path):
    _write_ui(
        tmp_path,
        """
        .brand { font-size: 2rem; font-weight: 700; }
        .body { font-size: 0.9375rem; font-weight: 400; }
        .pill { border-radius: var(--ds-radius-pill); }
        .card { border-radius: var(--ds-radius-sm); }
        """,
        html="<main class='app-mockup'><p>오프화이트 셔츠 · 면 포플린</p></main>",
    )
    report = lint_implementation(tmp_path)
    assert not _codes(report) & {"DS090", "DS091", "DS092", "DS093", "DS094"}
