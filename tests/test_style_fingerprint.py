import json
import re
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

import pytest

from design_ontology_harness.adapters.base import _contrast_ratio
from design_ontology_harness.style_fingerprint import (
    StyleFingerprint,
    check_and_register_fingerprint,
    check_style_divergence,
    compare_fingerprints,
    detect_attractors,
    extract_style_fingerprint,
    load_registry,
    register_fingerprint,
)
from design_ontology_harness.token_emitter import emit_project_tokens


WARM_EDITORIAL_CSS = """
:root {
  --bg: #fbf6eb;
}
body {
  background: var(--bg);
  color: #16211f;
  font-family: Pretendard, system-ui, sans-serif;
}
h1 {
  font-family: "Noto Serif KR", serif;
}
.badge { background: #8a2635; border-radius: 999px; }
.chip { background: #7cb7b1; border-radius: 8px; }
.highlight { background: #c8d646; border-radius: 18px; }
"""

COOL_TOOL_CSS = """
body {
  background: #ffffff;
  color: #111827;
  font-family: "Wanted Sans", system-ui, sans-serif;
}
.action { background: #4338ca; border-radius: 4px; }
.ok { background: #15803d; }
"""


def _write_project(tmp_path: Path, name: str, css: str) -> Path:
    project = tmp_path / name
    project.mkdir()
    (project / "index.html").write_text(
        "<html><head><link rel='stylesheet' href='styles.css'></head><body></body></html>",
        encoding="utf-8",
    )
    (project / "styles.css").write_text(css, encoding="utf-8")
    return project


def test_extract_warm_editorial_fingerprint(tmp_path):
    project = _write_project(tmp_path, "warm", WARM_EDITORIAL_CSS)
    fp = extract_style_fingerprint(project)
    assert fp.surface_tone == "warm-paper"
    assert "red" in fp.accent_hue_buckets or "magenta" in fp.accent_hue_buckets
    assert any(bucket in fp.accent_hue_buckets for bucket in ("teal", "cyan", "green"))
    assert fp.serif_accent is True
    assert "Noto Serif KR" in fp.font_families
    assert fp.uses_pill_shapes is True


def test_attractor_detection(tmp_path):
    warm = extract_style_fingerprint(_write_project(tmp_path, "warm", WARM_EDITORIAL_CSS))
    matches = detect_attractors(warm)
    assert any(m["id"] == "warm-editorial-default" for m in matches)

    cool = extract_style_fingerprint(_write_project(tmp_path, "cool", COOL_TOOL_CSS))
    assert not any(m["id"] == "warm-editorial-default" for m in detect_attractors(cool)), (
        "A white-surface sans tool UI must not match the warm editorial attractor"
    )


def test_compare_similarity_of_clone_vs_distinct(tmp_path):
    warm_a = extract_style_fingerprint(_write_project(tmp_path, "a", WARM_EDITORIAL_CSS))
    warm_b = extract_style_fingerprint(_write_project(tmp_path, "b", WARM_EDITORIAL_CSS))
    cool = extract_style_fingerprint(_write_project(tmp_path, "c", COOL_TOOL_CSS))

    clone = compare_fingerprints(warm_a, warm_b)
    distinct = compare_fingerprints(warm_a, cool)
    assert clone["similarity"] >= 0.9
    assert distinct["similarity"] < clone["similarity"]
    assert distinct["similarity"] < 0.62


def test_divergence_gate_fails_on_repeat(tmp_path):
    registry_path = tmp_path / "registry" / "style_fingerprints.json"
    first = extract_style_fingerprint(_write_project(tmp_path, "first", WARM_EDITORIAL_CSS))
    register_fingerprint(registry_path, first)

    repeat_project = _write_project(tmp_path, "repeat", WARM_EDITORIAL_CSS)
    report = check_style_divergence(repeat_project, registry_path=registry_path)
    assert report["verdict"] == "fail"
    assert report["too_similar_to"], "clone styling must be flagged as too similar"
    assert report["attractor_matches"]
    assert report["suggestions"]

    fresh_project = _write_project(tmp_path, "fresh", COOL_TOOL_CSS)
    fresh_report = check_style_divergence(fresh_project, registry_path=registry_path)
    assert fresh_report["verdict"] == "ok"


def test_separation_style_detection(tmp_path):
    hairline_css = "\n".join(
        f".row{i} {{ border-bottom: 1px solid var(--ds-color-border); }}" for i in range(6)
    )
    fp = extract_style_fingerprint(_write_project(tmp_path, "hair", hairline_css))
    assert fp.separation_style == "hairline-rows"

    card_css = "\n".join(
        f".card{i} {{ border: 1px solid var(--ds-color-border); border-radius: var(--ds-radius-md); }}"
        for i in range(6)
    )
    fp_card = extract_style_fingerprint(_write_project(tmp_path, "card", card_css))
    assert fp_card.separation_style == "card-wall"

    same_a = extract_style_fingerprint(_write_project(tmp_path, "ha", hairline_css))
    same_b = extract_style_fingerprint(_write_project(tmp_path, "hb", hairline_css))
    diff = extract_style_fingerprint(_write_project(tmp_path, "cw", card_css))
    same_score = compare_fingerprints(same_a, same_b)["similarity"]
    diff_score = compare_fingerprints(same_a, diff)["similarity"]
    assert same_score > diff_score, "shared composition grammar must raise similarity"


def test_operational_table_rail_is_not_mislabeled_as_card_wall(tmp_path):
    operational_css = "\n".join(
        [
            *(f".ops-card-{i} {{ border: 1px solid #ddd; border-radius: 8px; }}" for i in range(10)),
            *(f".schedule-table-{i} .fixture-row {{ border-bottom: 1px solid #ddd; }}" for i in range(10)),
            ".match-ticker .ticker-rail { display: grid; }",
            ".source-ledger .ledger-row { border-bottom: 1px solid #ddd; }",
            ".standings-table .result-row { border-bottom: 1px solid #ddd; }",
        ]
    )
    project = _write_project(tmp_path, "operations", operational_css)
    (project / "index.html").write_text(
        "<main data-product-surface='fixture-review-workspace'><table class='schedule-table'></table></main>",
        encoding="utf-8",
    )

    fingerprint = extract_style_fingerprint(project)

    assert fingerprint.separation_style == "operations-table-rail"
    assert "fixture-workspace" in fingerprint.composition_markers


def test_dark_support_is_recorded_without_erasing_the_measured_tone(tmp_path):
    """Dark-mode support is a capability, not a surface tone.

    Overwriting the tone with "dual-theme" made every emit-tokens project report
    the same value, so the axis stopped separating anything while still adding
    to the similarity score.
    """
    css = """
    :root { --surface: #ffffff; }
    body { background: var(--surface); color: #101820; }
    html[data-theme="dark"] { --surface: #071821; }
    """
    fingerprint = extract_style_fingerprint(_write_project(tmp_path, "dual", css))

    assert fingerprint.supports_dark_theme is True
    assert fingerprint.surface_tone == "neutral-light"


def test_status_and_link_colours_stay_out_of_the_accent_signature(tmp_path):
    """Red means danger everywhere; sharing it is meaning, not convergence."""
    css = """
    :root {
      --ds-color-primary: #2F6F4F;
      --ds-color-accent: #B07D2A;
      --ds-color-danger: #B91C1C;
      --ds-color-success: #15803D;
      --ds-color-info: #2F6FEB;
      --ds-color-link: #2563EB;
    }
    body { background: #FFFFFF; color: #101820; }
    """
    fingerprint = extract_style_fingerprint(_write_project(tmp_path, "status", css))

    # primary(green) + accent(orange)만 남고, danger/success/info/link의
    # red·blue 계열은 지문에서 빠진다.
    assert set(fingerprint.accent_hue_buckets) == {"green", "orange"}


def test_tsx_structure_clone_fails_even_when_palette_and_fonts_change(tmp_path):
    registry_path = tmp_path / "registry.json"
    structure = """
      export function App() {
        return <><header className="header"/><aside className="sidebar"/>
          <div className="filter-bar"/><section className="card-grid feature-card metric-card"/>
          <table className="data-table"><tbody><tr className="table-row"/></tbody></table></>
      }
    """
    first = tmp_path / "first"
    (first / "src").mkdir(parents=True)
    (first / "src" / "App.tsx").write_text(structure, encoding="utf-8")
    (first / "styles.css").write_text(
        'body { background: #F1F5F9; color: #162033; font-family: "Wanted Sans", sans-serif; } .action { background: #C66A2B; border-radius: 2px; }',
        encoding="utf-8",
    )
    register_fingerprint(registry_path, extract_style_fingerprint(first))

    second = tmp_path / "second"
    (second / "src").mkdir(parents=True)
    (second / "src" / "App.tsx").write_text(structure, encoding="utf-8")
    (second / "styles.css").write_text(
        'body { background: #101816; color: #E8F2ED; font-family: "IBM Plex Sans", sans-serif; } .action { background: #B13A86; border-radius: 18px; }',
        encoding="utf-8",
    )

    report = check_style_divergence(second, registry_path=registry_path)

    assert "src/App.tsx" in report["fingerprint"]["source_files"]
    assert len(report["fingerprint"]["composition_markers"]) >= 4
    assert report["verdict"] == "fail"
    assert report["too_similar_to"][0]["structural_similarity"] == 1.0


def test_registry_upserts_by_project(tmp_path):
    registry_path = tmp_path / "registry.json"
    fp = StyleFingerprint(project="x", surface_tone="dark")
    register_fingerprint(registry_path, fp)
    register_fingerprint(registry_path, StyleFingerprint(project="x", surface_tone="neutral-light"))
    registry = load_registry(registry_path)
    entries = [e for e in registry["entries"] if e["project"] == "x"]
    assert len(entries) == 1
    assert entries[0]["fingerprint"]["surface_tone"] == "neutral-light"


def test_registry_rejects_wrong_schema(tmp_path):
    registry_path = tmp_path / "registry.json"
    registry_path.write_text(
        json.dumps({"schema_version": "wrong/v1", "entries": []}),
        encoding="utf-8",
    )

    with pytest.raises(ValueError, match="schema_version"):
        load_registry(registry_path)


def test_registry_rejects_incomplete_fingerprint_and_duplicate_project(tmp_path):
    registry_path = tmp_path / "registry.json"
    registry_path.write_text(
        json.dumps(
            {
                "schema_version": "style-fingerprint-registry/v1",
                "entries": [
                    {
                        "project": "incomplete",
                        "fingerprint": {"schema_version": "style-fingerprint/v1"},
                    }
                ],
            }
        ),
        encoding="utf-8",
    )
    with pytest.raises(ValueError, match="fingerprint.project"):
        load_registry(registry_path)

    fingerprint = StyleFingerprint(project="duplicate").to_dict()
    registry_path.write_text(
        json.dumps(
            {
                "schema_version": "style-fingerprint-registry/v1",
                "entries": [
                    {"project": "duplicate", "fingerprint": fingerprint},
                    {"project": "duplicate", "fingerprint": fingerprint},
                ],
            }
        ),
        encoding="utf-8",
    )
    with pytest.raises(ValueError, match="duplicates"):
        load_registry(registry_path)


def test_registry_registration_serializes_concurrent_writers(tmp_path):
    registry_path = tmp_path / "registry.json"

    def register(index: int) -> None:
        register_fingerprint(
            registry_path,
            StyleFingerprint(project=f"project-{index}", surface_tone="neutral-light"),
        )

    with ThreadPoolExecutor(max_workers=6) as executor:
        list(executor.map(register, range(12)))

    registry = load_registry(registry_path)
    assert {entry["project"] for entry in registry["entries"]} == {
        f"project-{index}" for index in range(12)
    }


def test_atomic_check_and_register_prevents_concurrent_clone_admission(tmp_path):
    registry_path = tmp_path / "registry.json"

    def candidate(project: str) -> StyleFingerprint:
        return StyleFingerprint(
            project=project,
            surface_tone="dark",
            accent_hue_buckets=["orange"],
            font_families=["Example Sans"],
            radius_values_px=[4.0, 8.0],
            separation_style="split-panel",
            composition_markers=["header", "sidebar", "table", "toolbar"],
        )

    def admit(project: str):
        return check_and_register_fingerprint(
            tmp_path,
            registry_path=registry_path,
            fingerprint=candidate(project),
        )

    with ThreadPoolExecutor(max_workers=2) as executor:
        results = list(executor.map(admit, ["clone-a", "clone-b"]))

    assert sum(entry is not None for _, entry in results) == 1
    assert len(load_registry(registry_path)["entries"]) == 1


def test_fingerprint_fails_when_a_selected_source_is_unreadable(tmp_path):
    project = _write_project(tmp_path, "unreadable", COOL_TOOL_CSS)
    unreadable = project / "bad.css"
    unreadable.write_bytes(b"\xff\xfe\x00")

    with pytest.raises(ValueError, match="bad.css"):
        extract_style_fingerprint(project)


def test_fingerprint_rejects_source_symlink_outside_project(tmp_path):
    outside = tmp_path / "outside.css"
    outside.write_text(COOL_TOOL_CSS, encoding="utf-8")
    project = tmp_path / "project"
    project.mkdir()
    (project / "link.css").symlink_to(outside)

    with pytest.raises(ValueError, match="resolves outside"):
        extract_style_fingerprint(project)


def test_fingerprint_binds_the_source_bytes(tmp_path):
    project = _write_project(tmp_path, "bound-source", COOL_TOOL_CSS)

    fingerprint = extract_style_fingerprint(project)

    assert fingerprint.source_snapshot_sha256 is not None
    assert len(fingerprint.source_snapshot_sha256) == 64


def test_emit_project_tokens_binds_blueprint_palette(tmp_path):
    project = tmp_path / "proj"
    blueprint_dir = project / "build" / "system" / "blueprint"
    blueprint_dir.mkdir(parents=True)
    (blueprint_dir / "design_system_blueprint.json").write_text(
        """{
          "font_system": {
            "heading": {"name": "Wanted Sans", "family": "geometric-sans"},
            "body": {"name": "Pretendard", "family": "humanist-sans"}
          }
        }""",
        encoding="utf-8",
    )
    (blueprint_dir / "token_schema.json").write_text(
        """{
          "categories": {
            "color": {
              "reference_palette": {
                "active_palette": {
                  "roles": {
                    "anchor_surface": {"hex": "#27503D"},
                    "fresh_accent": {"hex": "#00A591"},
                    "quiet_background": {"hex": "#ACE1AF"}
                  }
                }
              }
            },
            "radius": {"visual_corner_bias": "high"},
            "spacing": {"scale": [0, 4, 8]}
          }
        }""",
        encoding="utf-8",
    )

    target = emit_project_tokens(project)
    css = target.read_text(encoding="utf-8")
    assert target == project / "design-system" / "tokens.css"
    assert "--ds-color-brand-anchor-surface: #27503D;" in css
    assert "--ds-color-primary: #27503D;" in css, "primary must derive from the anchor role, not a generic default"
    assert "--ds-color-brand-fresh-accent: #00A591;" in css
    runtime_accent = re.search(r"(?m)^\s*--ds-color-accent:\s*(#[0-9A-F]{6});", css)
    assert runtime_accent is not None
    assert runtime_accent.group(1) != "#00A591"
    assert _contrast_ratio(runtime_accent.group(1), "#FFFFFF") >= 4.5
    assert '--ds-font-heading: "Wanted Sans"' in css
    assert "--ds-radius-lg: 16px;" in css
    assert "--ds-space-2: 8px;" in css
    assert "--ds-space-px-24: 24px;" in css
    assert "--ds-text-md: 1rem;" in css
    assert "--ds-duration-180: 180ms;" in css
    assert "--ds-ease-standard:" in css


def test_fingerprint_captures_motion_axes(tmp_path: Path):
    project = tmp_path / "motion-project"
    project.mkdir()
    (project / "styles.css").write_text(
        """
        .panel {
          transition: opacity var(--ds-duration-180) var(--ds-ease-enter),
                      transform var(--ds-duration-240) var(--ds-ease-exit);
        }
        .spinner { animation: spin var(--ds-loop-fast) var(--ds-ease-standard) infinite; }
        """,
        encoding="utf-8",
    )

    fingerprint = extract_style_fingerprint(project)

    assert 180.0 in fingerprint.duration_values_ms
    assert 240.0 in fingerprint.duration_values_ms
    assert 1200.0 in fingerprint.duration_values_ms
    assert {"enter", "exit", "standard"} <= set(fingerprint.easing_signatures)
    assert {"opacity", "transform"} <= set(fingerprint.transition_properties)
    assert fingerprint.enter_exit_asymmetry is True
    assert fingerprint.has_decorative_loop is False


def test_fingerprint_flags_transition_budget_spent_on_a_loop(tmp_path: Path):
    project = tmp_path / "decorated"
    project.mkdir()
    (project / "styles.css").write_text(
        ".glow { animation: breathe 2.8s ease-in-out infinite; }\n",
        encoding="utf-8",
    )

    fingerprint = extract_style_fingerprint(project)

    assert fingerprint.has_decorative_loop is True
    assert 2800.0 in fingerprint.duration_values_ms


def test_identical_motion_grammar_raises_similarity(tmp_path: Path):
    def _build(name: str, accent: str) -> StyleFingerprint:
        project = tmp_path / name
        project.mkdir()
        (project / "styles.css").write_text(
            f"""
            .a {{ color: {accent}; }}
            .panel {{ transition: opacity 180ms cubic-bezier(0.2, 0, 0, 1); }}
            """,
            encoding="utf-8",
        )
        return extract_style_fingerprint(project)

    first = _build("alpha", "#B03A2E")
    second = _build("beta", "#1F6F78")

    comparison = compare_fingerprints(first, second)

    assert comparison["motion_similarity"] == 1.0
    assert any("모션 문법 중복" in reason for reason in comparison["reasons"])
