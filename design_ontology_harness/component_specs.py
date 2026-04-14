"""Generate detailed, implementation-ready component specifications."""

from __future__ import annotations

import re
from pathlib import Path

from .models import DocumentRecord
from .utils import ensure_dir, write_json


COMPONENT_ANATOMY: dict[str, dict] = {
    "button": {
        "parts": ["container", "label", "leading-icon(optional)", "trailing-icon(optional)"],
        "states": ["default", "hover", "active", "disabled", "loading"],
        "accessibility": [
            "role=\"button\"",
            "aria-disabled=\"true\" when disabled",
            "aria-busy=\"true\" when loading",
            "최소 44x44 터치 영역",
            "텍스트 대비 4.5:1 이상",
        ],
        "tokens": {
            "surface": "{component}.surface.{state}",
            "text": "{component}.text.{state}",
            "border": "{component}.border.{state}",
            "radius": "radius.md",
            "padding": "spacing.12 spacing.24",
            "font": "typography.text.md.semibold",
        },
    },
    "input": {
        "parts": ["container", "label", "input-area", "helper-text(optional)", "leading-icon(optional)", "clear-button(optional)"],
        "states": ["default", "focus", "filled", "error", "disabled", "readonly"],
        "accessibility": [
            "label과 input을 for/id로 연결",
            "aria-describedby로 helper/error text 연결",
            "aria-invalid=\"true\" when error",
            "aria-required=\"true\" when required",
        ],
        "tokens": {
            "surface": "surface.input.{state}",
            "text": "text.input.{state}",
            "border": "border.input.{state}",
            "radius": "radius.sm",
            "padding": "spacing.8 spacing.12",
            "font": "typography.text.md.regular",
        },
    },
    "navigation": {
        "parts": ["container", "nav-item", "icon(optional)", "label", "indicator(active)", "badge(optional)"],
        "states": ["default", "hover", "active", "collapsed"],
        "accessibility": [
            "nav landmark (role=\"navigation\")",
            "aria-current=\"page\" for active item",
            "키보드 화살표 탐색 지원",
        ],
        "tokens": {
            "surface": "surface.nav.{state}",
            "text": "text.nav.{state}",
            "indicator": "color.accent.500",
            "padding": "spacing.8 spacing.16",
        },
    },
    "data-display": {
        "parts": ["container", "header", "content-area", "footer(optional)", "action(optional)"],
        "states": ["default", "loading", "empty", "error"],
        "accessibility": [
            "적절한 heading level 사용",
            "데이터 테이블은 scope와 caption 필수",
            "빈 상태에서 안내 텍스트 제공",
        ],
        "tokens": {
            "surface": "surface.card.default",
            "border": "border.subtle",
            "radius": "radius.md",
            "padding": "spacing.16 spacing.20",
            "shadow": "elevation.raised",
        },
    },
    "feedback": {
        "parts": ["container", "icon", "message", "action(optional)", "close-button(optional)"],
        "states": ["info", "success", "warning", "danger"],
        "accessibility": [
            "role=\"alert\" for urgent messages",
            "role=\"status\" for non-urgent",
            "aria-live=\"polite\" or \"assertive\"",
            "닫기 버튼에 aria-label 필수",
        ],
        "tokens": {
            "surface": "feedback.{severity}.surface",
            "text": "feedback.{severity}.text",
            "icon": "feedback.{severity}.icon",
            "border": "feedback.{severity}.border",
            "radius": "radius.sm",
        },
    },
    "overlay": {
        "parts": ["backdrop", "container", "header", "content", "footer(optional)", "close-button"],
        "states": ["closed", "opening", "open", "closing"],
        "accessibility": [
            "role=\"dialog\" with aria-modal=\"true\"",
            "focus trap (Tab 순환)",
            "Escape로 닫기",
            "aria-labelledby로 제목 연결",
            "닫은 후 trigger 요소로 포커스 복귀",
        ],
        "tokens": {
            "surface": "surface.overlay",
            "backdrop": "color.neutral.900/60",
            "radius": "radius.lg",
            "shadow": "elevation.modal",
            "padding": "spacing.24",
        },
    },
    "editorial": {
        "parts": ["canvas", "toolbar", "content-blocks", "selection-handle(optional)"],
        "states": ["default", "editing", "selecting", "readonly"],
        "accessibility": [
            "contenteditable 영역에 role=\"textbox\"",
            "aria-multiline=\"true\"",
            "도구 모음에 role=\"toolbar\"",
            "서식 버튼에 aria-pressed 상태",
        ],
        "tokens": {
            "surface": "surface.canvas.default",
            "text": "typography.text.md.regular",
            "heading": "typography.display.lg.bold",
            "padding": "spacing.24 spacing.32",
            "line-height": "typography.leading.relaxed",
        },
    },
}


BRAND_ADAPTATIONS: dict[str, dict[str, str]] = {
    "calm": {
        "hover": "opacity 변화 (0.08-0.12), elevation 변화 없음",
        "motion": "150-200ms ease-out, bounce/spring 없음",
        "color": "중성 톤 위주, accent는 최소한으로",
        "density": "comfortable 모드 기본, 여유로운 padding",
        "feedback": "subtle inline alert 선호, 과한 컬러 블록 지양",
    },
    "precise": {
        "hover": "정확한 border/outline 변화",
        "motion": "120-180ms, 군더더기 없는 전환",
        "color": "정확한 semantic 분리, 모호한 중간 톤 지양",
        "density": "엄격한 spacing scale 준수, 임의 값 금지",
        "feedback": "명확한 상태 구분, 진행률/결과를 수치로 표시",
    },
    "editorial": {
        "hover": "텍스트 underline 또는 color shift, 장식적 효과 없음",
        "motion": "콘텐츠 전환 위주, UI chrome 모션 최소화",
        "color": "타이포그래피로 위계 형성, 컬러보다 weight/size 활용",
        "density": "넉넉한 line-height와 margin, 읽기 편한 간격",
        "feedback": "콘텐츠 맥락 안에서 인라인 표시, 토스트보다 인라인 선호",
    },
    "trustworthy": {
        "hover": "예측 가능하고 일관된 hover 패턴",
        "motion": "모든 전환에 동일한 easing/duration",
        "color": "안정적인 neutral 기반, 과한 accent 변화 없음",
        "density": "기존 레이아웃 유지, 갑작스런 위치 변경 없음",
        "feedback": "결과를 반드시 확인, 실패 시 복구 방법 안내",
    },
    "bold": {
        "hover": "확실한 색상 변화 또는 scale 변화",
        "motion": "200-300ms, 시각적으로 확실한 전환",
        "color": "대비가 강한 accent, primary에 집중",
        "density": "큰 터치 영역, 핵심 요소 강조",
        "feedback": "눈에 띄는 성공/에러 표시, 컬러 블록 활용",
    },
    "minimal": {
        "hover": "미세한 opacity 또는 underline만",
        "motion": "80-120ms, 거의 즉각적",
        "color": "monochrome 기반, accent 최소화",
        "density": "compact 가능, 불필요한 여백 제거",
        "feedback": "아이콘+텍스트 조합, 색상 배경 최소화",
    },
}


def generate_component_specs(
    brand_profile: dict,
    blueprint: dict,
    component_list: list[dict],
    documents: list[DocumentRecord],
) -> dict:
    brand_keywords = [kw.lower() for kw in brand_profile.get("brand_keywords", [])]
    anti_keywords = [kw.lower() for kw in brand_profile.get("anti_keywords", [])]
    brand_name = brand_profile.get("brand_name", "Brand")

    adaptations = _collect_brand_adaptations(brand_keywords)
    anti_rules = _collect_anti_rules(anti_keywords)

    families: dict[str, list[dict]] = {}
    for comp in component_list:
        families.setdefault(comp["family"], []).append(comp)

    specs: list[dict] = []
    for comp in component_list:
        family = comp["family"]
        anatomy = COMPONENT_ANATOMY.get(family, COMPONENT_ANATOMY.get("data-display", {}))
        kb_evidence = _find_kb_evidence(comp["name"], family, documents)

        spec = {
            "name": comp["name"],
            "family": family,
            "role": comp.get("role", ""),
            "source_pattern": comp.get("source", ""),
            "anatomy": {
                "parts": anatomy.get("parts", []),
                "states": anatomy.get("states", []),
            },
            "tokens": _build_token_bindings(comp["name"], family, anatomy),
            "accessibility": anatomy.get("accessibility", []),
            "brand_adaptation": _build_adaptation_notes(
                comp["name"], family, brand_keywords, anti_keywords, adaptations, anti_rules
            ),
            "reference_evidence": kb_evidence,
            "implementation_notes": _build_implementation_notes(comp["name"], family, brand_keywords),
        }
        specs.append(spec)

    return {
        "brand": brand_name,
        "total_components": len(specs),
        "families": sorted(families.keys()),
        "brand_keywords": brand_keywords,
        "anti_keywords": anti_keywords,
        "global_adaptation": adaptations,
        "specs": specs,
    }


def write_component_specs(output_dir: Path, specs_data: dict) -> None:
    components_dir = ensure_dir(output_dir / "components")

    write_json(components_dir / "component_specs.json", specs_data)

    md_lines = [f"# {specs_data['brand']} Component Specs\n"]
    md_lines.append(f"총 {specs_data['total_components']}개 컴포넌트 | "
                    f"패밀리: {', '.join(specs_data['families'])}\n")

    md_lines.append("## 구현 원칙 (Non-negotiable)\n")
    md_lines.append("이 스펙의 모든 컴포넌트를 구현할 때 반드시 지킨다:\n")
    md_lines.append("1. **이모지를 UI로 쓰지 않는다** — 🎨 ✅ 🔥 ⚡ 🚀 ❌ ⭐ 📊 등 이모지를 아이콘, 상태 표시, 버튼 장식, 네비게이션 지표 자리에 절대 넣지 않는다. 아이콘 자리에는 SVG 컴포넌트 또는 Lucide/Heroicons/Phosphor/Tabler 라이브러리를 사용한다.")
    md_lines.append("2. **컴포넌트를 직접 구현한다** — 아래 각 컴포넌트의 anatomy(구조), states(상태), 토큰 바인딩, 접근성 규칙을 그대로 따라 완전하게 구현한다. '임시', 'TODO', '플레이스홀더' 같은 반쪽 구현을 남기지 않는다.")
    md_lines.append("3. **라이브러리 기본 스타일 금지** — 라이브러리 컴포넌트를 그대로 import해서 쓰지 않는다. 반드시 디자인 토큰(--color-*, --space-*, --radius-*, --font-*)으로 스타일을 명시적으로 바인딩한다.")
    md_lines.append("4. **접근성은 옵션이 아니다** — 각 컴포넌트의 '접근성' 섹션에 정의된 role, aria-*, label, focus 관리 규칙을 전부 적용한다.")
    md_lines.append("5. **hex 값 하드코딩 금지** — 색상은 반드시 semantic token을 경유한다 (예: `color: var(--color-ink)` not `color: #2C2C2C`).")
    md_lines.append("")

    md_lines.append("## 브랜드 적용 규칙\n")
    for aspect, rule in specs_data.get("global_adaptation", {}).items():
        md_lines.append(f"- **{aspect}**: {rule}")
    md_lines.append("")

    for spec in specs_data["specs"]:
        md_lines.append(f"---\n")
        md_lines.append(f"## {spec['family']} / {spec['name']}\n")
        md_lines.append(f"**역할**: {spec['role']}\n")

        if spec.get("source_pattern"):
            md_lines.append(f"**탐지 출처**: {spec['source_pattern']}\n")

        md_lines.append("### 구조 (Anatomy)\n")
        for part in spec["anatomy"]["parts"]:
            md_lines.append(f"- {part}")
        md_lines.append("")

        md_lines.append("### 상태 (States)\n")
        md_lines.append(f"| 상태 | 설명 |")
        md_lines.append(f"|------|------|")
        for state in spec["anatomy"]["states"]:
            desc = _state_description(state, spec["family"])
            md_lines.append(f"| `{state}` | {desc} |")
        md_lines.append("")

        md_lines.append("### 토큰 바인딩\n")
        md_lines.append("```")
        for slot, token in spec["tokens"].items():
            md_lines.append(f"{slot}: {token}")
        md_lines.append("```\n")

        md_lines.append("### 접근성\n")
        for rule in spec["accessibility"]:
            md_lines.append(f"- {rule}")
        md_lines.append("")

        md_lines.append("### 브랜드 적용\n")
        for note in spec["brand_adaptation"]:
            md_lines.append(f"- {note}")
        md_lines.append("")

        if spec["reference_evidence"]:
            md_lines.append("### 레퍼런스 근거\n")
            for evidence in spec["reference_evidence"][:3]:
                md_lines.append(f"- **{evidence['source']}**: {evidence['excerpt']}")
            md_lines.append("")

        md_lines.append("### 구현 노트\n")
        for note in spec["implementation_notes"]:
            md_lines.append(f"- {note}")
        md_lines.append("")

    (components_dir / "component_specs.md").write_text(
        "\n".join(md_lines), encoding="utf-8"
    )


def _collect_brand_adaptations(brand_keywords: list[str]) -> dict[str, str]:
    merged: dict[str, str] = {}
    for keyword in brand_keywords:
        rules = BRAND_ADAPTATIONS.get(keyword, {})
        for aspect, rule in rules.items():
            if aspect in merged:
                merged[aspect] += f" + {rule}"
            else:
                merged[aspect] = rule
    return merged


def _collect_anti_rules(anti_keywords: list[str]) -> list[str]:
    rules = []
    for keyword in anti_keywords:
        adaptation = BRAND_ADAPTATIONS.get(keyword, {})
        if adaptation:
            for aspect, rule in adaptation.items():
                rules.append(f"({keyword}) {aspect}: {rule} — 이것을 피할 것")
    return rules


def _build_token_bindings(name: str, family: str, anatomy: dict) -> dict[str, str]:
    raw = anatomy.get("tokens", {})
    result = {}
    for slot, pattern in raw.items():
        result[slot] = pattern.replace("{component}", name).replace("{severity}", "info")
    return result


def _build_adaptation_notes(
    name: str,
    family: str,
    brand_keywords: list[str],
    anti_keywords: list[str],
    adaptations: dict[str, str],
    anti_rules: list[str],
) -> list[str]:
    notes: list[str] = []

    family_aspects = {
        "button": ["hover", "motion", "color"],
        "input": ["hover", "density", "feedback"],
        "navigation": ["hover", "density", "motion"],
        "data-display": ["density", "color"],
        "feedback": ["feedback", "motion", "color"],
        "overlay": ["motion", "density"],
        "editorial": ["density", "color", "motion"],
    }
    relevant = family_aspects.get(family, ["hover", "motion", "color"])

    for aspect in relevant:
        if aspect in adaptations:
            keywords_str = "+".join(kw for kw in brand_keywords if kw in BRAND_ADAPTATIONS and aspect in BRAND_ADAPTATIONS[kw])
            if keywords_str:
                notes.append(f"[{keywords_str}] {aspect}: {adaptations[aspect]}")

    for rule in anti_rules[:2]:
        notes.append(f"[금지] {rule}")

    return notes or ["브랜드 기본 규칙을 따릅니다."]


def _find_kb_evidence(
    component_name: str,
    family: str,
    documents: list[DocumentRecord],
) -> list[dict]:
    search_terms = [
        component_name.replace("-", " "),
        component_name.replace("-", ""),
        family,
    ]
    evidence: list[dict] = []
    seen_slugs: set[str] = set()

    for doc in documents:
        if doc.error or not doc.text:
            continue
        text_lower = doc.text.lower()
        title_lower = (doc.title or "").lower()
        matched = False
        matched_term = ""

        for term in search_terms:
            if term.lower() in text_lower or term.lower() in title_lower:
                matched = True
                matched_term = term
                break

        if matched and doc.reference_slug not in seen_slugs:
            seen_slugs.add(doc.reference_slug)
            excerpt = _extract_relevant_excerpt(doc.text, matched_term)
            evidence.append({
                "source": doc.source_label or doc.reference_slug,
                "url": doc.url,
                "matched_term": matched_term,
                "excerpt": excerpt,
            })
            if len(evidence) >= 5:
                break

    return evidence


def _extract_relevant_excerpt(text: str, term: str) -> str:
    lines = text.split("\n")
    for i, line in enumerate(lines):
        if term.lower() in line.lower():
            context = lines[max(0, i):min(len(lines), i + 2)]
            excerpt = " ".join(ln.strip() for ln in context if ln.strip())
            if len(excerpt) > 150:
                excerpt = excerpt[:147] + "..."
            return excerpt
    return f"'{term}' 관련 내용 포함"


def _state_description(state: str, family: str) -> str:
    descriptions = {
        "default": "기본 상태",
        "hover": "마우스 오버 시",
        "active": "클릭/탭 중",
        "disabled": "비활성 (상호작용 불가)",
        "loading": "로딩 중 (스피너 표시)",
        "focus": "키보드 포커스 시",
        "filled": "값이 입력된 상태",
        "error": "유효성 검증 실패",
        "readonly": "읽기 전용",
        "collapsed": "접힌 상태",
        "open": "열린 상태",
        "opening": "열리는 중 (전환 애니메이션)",
        "closed": "닫힌 상태",
        "closing": "닫히는 중",
        "editing": "편집 모드 활성",
        "selecting": "텍스트/블록 선택 중",
        "info": "정보 알림",
        "success": "성공 알림",
        "warning": "경고 알림",
        "danger": "에러/위험 알림",
        "empty": "데이터 없음",
        "sorted": "정렬 적용됨",
        "filtered": "필터 적용됨",
    }
    return descriptions.get(state, state)


def _build_implementation_notes(name: str, family: str, brand_keywords: list[str]) -> list[str]:
    notes = [
        "기존에 같은 역할의 컴포넌트가 있으면 토큰 교체부터 시작",
        "variant prop으로 시각적 변형을 관리 (하드코딩 금지)",
    ]

    if family == "button":
        notes.append("size prop: sm / md / lg (터치 영역은 항상 최소 44px 보장)")
    elif family == "input":
        notes.append("error 상태에서 helper text → error message로 자동 전환")
        notes.append("label은 항상 visible (placeholder만으로 대체 금지)")
    elif family == "navigation":
        notes.append("active 상태는 URL/라우터와 자동 동기화")
    elif family == "overlay":
        notes.append("Escape / backdrop click으로 닫기, 열 때 첫 focusable 요소로 이동")
    elif family == "editorial":
        notes.append("블록 단위 데이터 모델, JSON 직렬화 가능한 구조")
    elif family == "feedback":
        notes.append("auto-dismiss 시간은 내용 길이에 비례 (기본 5초)")
    elif family == "data-display":
        notes.append("빈 상태(empty-state)와 에러 상태를 반드시 처리")

    if "calm" in brand_keywords:
        notes.append("애니메이션은 상태 설명용으로만 사용, 장식 효과 금지")
    if "editorial" in brand_keywords:
        notes.append("텍스트 위계가 핵심 — 컬러보다 weight/size로 구분")

    return notes
