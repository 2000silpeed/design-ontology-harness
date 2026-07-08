from pathlib import Path

from design_ontology_harness.style_fingerprint import (
    StyleFingerprint,
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


def test_registry_upserts_by_project(tmp_path):
    registry_path = tmp_path / "registry.json"
    fp = StyleFingerprint(project="x", surface_tone="dark")
    register_fingerprint(registry_path, fp)
    register_fingerprint(registry_path, StyleFingerprint(project="x", surface_tone="neutral-light"))
    registry = load_registry(registry_path)
    entries = [e for e in registry["entries"] if e["project"] == "x"]
    assert len(entries) == 1
    assert entries[0]["fingerprint"]["surface_tone"] == "neutral-light"


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
    assert "--ds-color-accent: #00A591;" in css
    assert '--ds-font-heading: "Wanted Sans"' in css
    assert "--ds-radius-lg: 16px;" in css
    assert "--ds-space-2: 8px;" in css
