from __future__ import annotations

import json
from pathlib import Path

from design_ontology_harness.implementation_linter import (
    BODY_LINE_HEIGHT_FLOOR,
    BODY_LINE_HEIGHT_FLOOR_HANGUL,
    lint_implementation,
)
from design_ontology_harness.token_emitter import emit_project_tokens


def _write_project(tmp_path: Path, font_system: dict) -> Path:
    project = tmp_path / "proj"
    blueprint_dir = project / "build" / "system" / "blueprint"
    blueprint_dir.mkdir(parents=True)
    (blueprint_dir / "design_system_blueprint.json").write_text(
        json.dumps({"font_system": font_system}), encoding="utf-8"
    )
    (blueprint_dir / "token_schema.json").write_text(
        json.dumps(
            {
                "categories": {
                    "color": {
                        "reference_palette": {
                            "active_palette": {
                                "roles": {"anchor_surface": {"hex": "#27503D"}}
                            }
                        }
                    },
                    "radius": {"visual_corner_bias": "medium"},
                    "spacing": {"scale": [0, 4, 8]},
                }
            }
        ),
        encoding="utf-8",
    )
    return project


def _korean_font_system() -> dict:
    return {
        "heading": {"name": "Pretendard", "family": "humanist-sans"},
        "body": {"name": "Pretendard", "family": "humanist-sans"},
        "needs_korean": True,
        "type_scale": {"line_heights": {"tight": 1.2, "normal": 1.5, "relaxed": 1.75}},
        "script_guardrails": {
            "primary_script": "korean",
            "body_font": {"name": "Pretendard", "line_height": "1.6-1.7", "letter_spacing": "0em"},
            "wrap": {"body": {"word_break": "keep-all", "overflow_wrap": "normal"}},
        },
    }


def _latin_font_system() -> dict:
    return {
        "heading": {"name": "Inter", "family": "humanist-sans"},
        "body": {"name": "Inter", "family": "humanist-sans"},
        "needs_korean": False,
        "type_scale": {"line_heights": {"tight": 1.2, "normal": 1.5, "relaxed": 1.65}},
    }


def test_korean_project_emits_korean_reading_rhythm(tmp_path: Path):
    css = emit_project_tokens(_write_project(tmp_path, _korean_font_system())).read_text(
        encoding="utf-8"
    )
    assert "--ds-leading-body: 1.6;" in css
    assert "--ds-tracking-body: 0em;" in css
    assert "--ds-wrap-word-break: keep-all;" in css
    assert "--ds-wrap-overflow: normal;" in css


def test_latin_project_emits_latin_floor_without_wrap_contract(tmp_path: Path):
    css = emit_project_tokens(_write_project(tmp_path, _latin_font_system())).read_text(
        encoding="utf-8"
    )
    assert "--ds-leading-body: 1.5;" in css
    assert "--ds-tracking-body: normal;" in css
    assert "--ds-wrap-word-break" not in css


def test_korean_leading_never_falls_below_the_lint_floor(tmp_path: Path):
    """서체 프로필이 낮은 값을 들고 있어도 게이트 하한 아래로는 내려가지 않는다."""
    font_system = _korean_font_system()
    font_system["script_guardrails"]["body_font"]["line_height"] = "1.3-1.4"
    css = emit_project_tokens(_write_project(tmp_path, font_system)).read_text(encoding="utf-8")
    assert f"--ds-leading-body: {BODY_LINE_HEIGHT_FLOOR_HANGUL:g};" in css


def test_latin_leading_never_falls_below_the_lint_floor(tmp_path: Path):
    font_system = _latin_font_system()
    font_system["type_scale"]["line_heights"]["normal"] = 1.2
    css = emit_project_tokens(_write_project(tmp_path, font_system)).read_text(encoding="utf-8")
    assert f"--ds-leading-body: {BODY_LINE_HEIGHT_FLOOR:g};" in css


def test_positive_korean_tracking_is_clamped_to_zero(tmp_path: Path):
    font_system = _korean_font_system()
    font_system["script_guardrails"]["body_font"]["letter_spacing"] = "0.04em"
    css = emit_project_tokens(_write_project(tmp_path, font_system)).read_text(encoding="utf-8")
    assert "--ds-tracking-body: 0em;" in css


def test_negative_korean_tracking_is_preserved(tmp_path: Path):
    font_system = _korean_font_system()
    font_system["script_guardrails"]["body_font"]["letter_spacing"] = "-0.01em"
    css = emit_project_tokens(_write_project(tmp_path, font_system)).read_text(encoding="utf-8")
    assert "--ds-tracking-body: -0.01em;" in css


def test_emitted_tokens_satisfy_the_base_rules(tmp_path: Path):
    """생성기가 내보낸 토큰만 소비하는 구현은 DS100~DS107을 통과해야 한다."""
    project = _write_project(tmp_path, _korean_font_system())
    emit_project_tokens(project)
    (project / "index.html").write_text(
        "<html><head><link rel='stylesheet' href='styles.css'></head><body>"
        "<main class='app-shell'><p class='description'>"
        "구단 순위와 경기 일정을 한 화면에서 확인하고 관심 팀의 다음 경기를 놓치지 않도록 돕는 화면입니다."
        "</p></main></body></html>",
        encoding="utf-8",
    )
    (project / "styles.css").write_text(
        """
        .description {
          font-family: var(--ds-font-ko);
          color: var(--ds-color-ink);
          background: var(--ds-color-surface);
          line-height: var(--ds-leading-body);
          letter-spacing: var(--ds-tracking-body);
          word-break: var(--ds-wrap-word-break);
          overflow-wrap: var(--ds-wrap-overflow);
          text-align: left;
        }
        """,
        encoding="utf-8",
    )
    report = lint_implementation(project)
    base_rule_issues = [issue for issue in report.issues if issue.code.startswith("DS1")]
    assert base_rule_issues == []
