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
