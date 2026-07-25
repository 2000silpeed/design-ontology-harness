"""EKOS Knowledge Intake 합성 실행 래퍼.

harness의 run-project를 그대로 실행하되, 두 가지 인간 디자인 결정을 강제한다.

1. 상태 색 계약 (화면 명세 §3):
   성공=Hunter Green, 경고=Goldenrod, 실패·충돌=Marsala, 정보/링크=Ocean Blue.
   Rust는 brand_accent(강조)로만 남기고 warning 상속을 차단한다.

2. 다크 모드 수동 팔레트 (역전 도면 — 프러시안 심해 위 콘실크 잉크):
   docs/ekos-design-system.html의 ink 테마 값을 기준으로
   expanded_palette.dark_semantic_roles에 주입한다. 어댑터(tokens_for_mode)가
   자동 유도 대신 이 값을 사용한다 (contrast floor 보정은 유지됨).
"""
import sys
from pathlib import Path

HARNESS = Path("/Users/sungwoon/ai-projects/design-ontology-harness")
COLOR_MD = HARNESS / "docs" / "color-reference.md"

from design_ontology_harness import color_reference as cr

parsed = cr.parse_color_reference_markdown(COLOR_MD)
by_name = {c["name"].lower(): c for c in parsed["colors"]}

SPEC_FEEDBACK = {
    "info": "Ocean Blue",
    "success": "Hunter Green",
    "warning": "Goldenrod",
    "danger": "Marsala",
    "link": "Ocean Blue",
}

_orig = cr._build_semantic_roles


def _entry(name: str, usage: str) -> dict:
    base = dict(by_name[name.lower()])
    base["usage"] = usage
    base["source_type"] = "spec-status-contract"
    return base


def patched(active_palette, supporting_colors):
    roles = _orig(active_palette, supporting_colors)
    roles["info"] = _entry("Ocean Blue", "정보·진행 안내 (신뢰 축)")
    roles["success"] = _entry("Hunter Green", "성공·검사 통과·공식 상태")
    roles["warning"] = _entry("Goldenrod", "경고·확인 필요")
    roles["danger"] = _entry("Marsala", "실패·충돌 확인")
    link = _entry("Ocean Blue", "링크·포커스 (신뢰 축)")
    roles["link"] = link
    shifted = cr._shift_hex(link["hex"], dl=-0.08) or link["hex"]
    if hasattr(cr, "_derived_runtime_color"):
        roles["link_hover"] = cr._derived_runtime_color(
            "Link Hover", shifted, derived_from="link"
        )
    elif hasattr(cr, "_fallback_color"):
        roles["link_hover"] = cr._fallback_color("Link Hover", shifted)
    else:
        roles["link_hover"] = {"name": "Link Hover", "hex": shifted}
    return roles


cr._build_semantic_roles = patched

# ── 다크 모드 수동 팔레트 ──
# 키는 어댑터 토큰명(CSS 변수 --ds-color-<key>)과 일치해야 한다.
# 출처: EKOS docs/ekos-design-system.html [data-theme="ink"] 램프.
DARK_SEMANTIC_ROLES = {
    "canvas": "#0B1E2E",            # paper — 프러시안 심해 페이지 배경
    "surface": "#11283C",           # card
    "surface-muted": "#081726",     # paper-deep
    "surface-elevated": "#16324A",  # card보다 한 단계 부양
    "surface-tint": "#36301C",      # cornsilk 강조면의 다크 대응 (gold-mist)
    "border": "#27425A",            # rule
    "border-strong": "#3A5A75",     # rule-strong
    "ink": "#EBE4CE",               # 콘실크 잉크 (본문)
    "ink-muted": "#B0BCC4",         # ink-soft
    "ink-subtle": "#76879A",        # ink-faint
    "ink-inverse": "#0B1E2E",       # 밝은 칩 위의 어두운 글자
    "primary": "#6FA5CC",           # Prussian의 다크 부양 (차분한 채도 유지)
    "accent": "#D96B43",            # Rust → seal (강조 전용)
    "info": "#6FB5C0",              # Ocean → trust
    "link": "#6FB5C0",              # trust
    "link-hover": "#8FCBD4",        # trust-deep
    "success": "#7FAF87",           # Hunter → assure
    "warning": "#E0B54A",           # Goldenrod → gold
    "danger": "#C9837F",            # Marsala 다크 부양
}

_orig_expanded = cr._build_expanded_palette


def patched_expanded(**kwargs):
    expanded = _orig_expanded(**kwargs)
    expanded["dark_semantic_roles"] = {
        role: {"hex": value, "source_type": "spec-manual-dark"}
        for role, value in DARK_SEMANTIC_ROLES.items()
    }
    return expanded


cr._build_expanded_palette = patched_expanded

sys.argv = [
    "design-ontology",
    "run-project",
    "--project-dir",
    "projects/ekos-knowledge-intake",
    "--kb-dir",
    "kb/default",
]
from design_ontology_harness.cli import main

main()
