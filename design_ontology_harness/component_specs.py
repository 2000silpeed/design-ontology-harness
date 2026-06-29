"""Generate detailed, implementation-ready component specifications."""

from __future__ import annotations

from pathlib import Path

from .advanced_components import get_advanced_component
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
            "320px viewport에서도 버튼 전체와 focus ring이 화면 밖으로 나가지 않아야 함",
        ],
        "tokens": {
            "surface": "var(--color-brand-primary)",
            "text": "var(--color-text-inverse)",
            "border": "var(--color-brand-primary)",
            "radius": "var(--radius-md)",
            "padding": "var(--space-12) var(--space-24)",
            "max-inline-size": "100%",
            "min-inline-size": "0",
            "label-wrap": "white-space: normal",
            "font": "var(--font-body) / var(--text-md) / semibold",
            "hover-surface": "var(--color-link-hover)",
            "focus-ring": "box-shadow: 0 0 0 2px var(--color-surface), 0 0 0 4px var(--color-brand-primary)",
            "motion": "background var(--duration-180) var(--ease-standard)",
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
            "surface": "var(--color-surface)",
            "text": "var(--color-text)",
            "placeholder": "var(--color-text-subtle)",
            "border": "var(--color-border)",
            "border-focus": "var(--color-brand-primary)",
            "border-error": "var(--color-danger)",
            "radius": "var(--radius-sm)",
            "padding": "var(--space-8) var(--space-12)",
            "font": "var(--font-body) / var(--text-md) / regular",
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
            "surface": "var(--color-surface)",
            "text": "var(--color-text-muted)",
            "text-active": "var(--color-text)",
            "indicator": "var(--color-brand-accent)",
            "padding": "var(--space-8) var(--space-16)",
            "font": "var(--font-body) / var(--text-sm) / medium",
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
            "surface": "var(--color-surface)",
            "border": "var(--color-border)",
            "radius": "var(--radius-md)",
            "padding": "var(--space-16) var(--space-20)",
            "heading-font": "var(--font-heading) / var(--text-md) / semibold",
            "body-font": "var(--font-body) / var(--text-sm) / regular",
            "text": "var(--color-text)",
            "text-muted": "var(--color-text-muted)",
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
            "surface": "var(--color-surface-muted)",
            "text": "var(--color-text)",
            "icon": "var(--color-info)",
            "border": "var(--color-border)",
            "radius": "var(--radius-sm)",
            "padding": "var(--space-12) var(--space-16)",
            "severity-info": "var(--color-info)",
            "severity-success": "var(--color-success)",
            "severity-warning": "var(--color-warning)",
            "severity-danger": "var(--color-danger)",
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
            "surface": "var(--color-surface-elevated)",
            "backdrop": "rgb(0 0 0 / 0.5)",
            "radius": "var(--radius-lg)",
            "padding": "var(--space-24)",
            "border": "var(--color-border)",
            "motion": "opacity var(--duration-180) var(--ease-standard)",
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
            "surface": "var(--color-surface)",
            "text": "var(--color-text)",
            "font": "var(--font-body) / var(--text-md) / regular",
            "heading-font": "var(--font-heading) / var(--text-2xl) / bold",
            "padding": "var(--space-24) var(--space-32)",
            "line-height": "var(--leading-relaxed)",
        },
    },
    "marketing": {
        "parts": ["section-container", "inner-max-width", "content"],
        "states": ["default", "in-view", "hover"],
        "accessibility": [
            "의미 있는 <section> 또는 <header>/<footer> 랜드마크 사용",
            "aria-labelledby로 제목(<h1>/<h2>)과 연결",
            "색상만으로 의미 전달 금지",
            "키보드로 CTA와 링크 접근 가능",
        ],
        "tokens": {
            "section-background": "var(--color-canvas)",
            "inner-padding": "var(--space-96) var(--space-24)",
            "inner-max-width": "1120px",
            "heading-font": "var(--font-heading) / var(--text-3xl) / semibold",
            "body-font": "var(--font-body) / var(--text-md) / regular",
            "text": "var(--color-text)",
            "text-muted": "var(--color-text-muted)",
        },
    },
}


# ---------------------------------------------------------------------------
# Slot archetypes — component-level overrides picked by name pattern.
# Each archetype supplies its own parts / states / tokens / accessibility.
# When an archetype matches, it overrides the family-default anatomy.
# Tokens use real CSS variable names so specs are directly consumable.
# ---------------------------------------------------------------------------


SLOT_ARCHETYPES: dict[str, dict] = {
    "text-heading": {
        "parts": ["heading-text"],
        "states": ["default"],
        "accessibility": [
            "의미 있는 heading 태그 사용 (<h1>~<h3>)",
            "페이지당 <h1>은 1개",
            "aria-labelledby의 id 타깃이 되어야 함",
        ],
        "tokens": {
            "font": "var(--font-heading)",
            "size": "var(--text-3xl)",
            "weight": "semibold (600)",
            "line-height": "var(--leading-tight)",
            "color": "var(--color-text)",
            "letter-spacing": "-0.01em",
        },
    },
    "text-eyebrow": {
        "parts": ["eyebrow-label"],
        "states": ["default"],
        "accessibility": [
            "장식용 카테고리 레이블 — 스크린 리더가 건너뛸 수 있어야 함",
            "의미가 필요하면 heading 위 <p> 또는 <span> 사용",
        ],
        "tokens": {
            "font": "var(--font-mono)",
            "size": "var(--text-xs)",
            "weight": "medium (500)",
            "color": "var(--color-text-subtle)",
            "letter-spacing": "0.08em",
            "text-transform": "uppercase",
        },
    },
    "text-body": {
        "parts": ["body-text"],
        "states": ["default"],
        "accessibility": [
            "의미 있는 <p> 태그 사용",
            "line-length 75ch 이하 권장",
        ],
        "tokens": {
            "font": "var(--font-body)",
            "size": "var(--text-lg)",
            "line-height": "var(--leading-relaxed)",
            "color": "var(--color-text-muted)",
            "max-width": "65ch",
        },
    },
    "surface-card": {
        "parts": ["container", "inner-content"],
        "states": ["default", "hover", "focus-visible"],
        "accessibility": [
            "카드 자체가 링크/버튼이면 <a>/<button> 래퍼 사용",
            "장식적 카드는 단순 <article> 또는 <div>",
        ],
        "tokens": {
            "surface": "var(--color-surface)",
            "border": "var(--color-border)",
            "border-hover": "var(--color-border-strong)",
            "radius": "var(--radius-lg)",
            "padding": "var(--space-32)",
            "gap": "var(--space-16)",
            "motion": "border-color var(--duration-180) var(--ease-standard)",
        },
    },
    "icon-holder": {
        "parts": ["icon-container", "icon-svg"],
        "states": ["default"],
        "accessibility": [
            "장식용이면 aria-hidden=\"true\"",
            "의미가 있으면 <title> 포함",
        ],
        "tokens": {
            "container-surface": "var(--color-surface-tint)",
            "container-size": "40px",
            "container-radius": "var(--radius-md)",
            "icon-stroke": "var(--color-brand-primary)",
            "icon-size": "20px",
            "icon-stroke-width": "1.75",
        },
    },
    "nav-bar": {
        "parts": ["sticky-container", "inner-max-width", "left-group", "right-group"],
        "states": ["default", "scrolled"],
        "accessibility": [
            "<header role=\"banner\"> 또는 <nav aria-label=\"Primary\">",
            "키보드 탐색 시 논리적 탭 순서 유지",
            "랜드마크가 중복되지 않도록 main 이외 영역에만 배치",
        ],
        "tokens": {
            "surface": "var(--color-surface)",
            "border-bottom": "var(--color-border)",
            "height": "64px",
            "padding": "0 var(--space-24)",
            "inner-max-width": "1120px",
            "z-index": "50",
            "backdrop-filter": "blur(8px)",
        },
    },
    "footer-bar": {
        "parts": ["container", "column-grid", "legal-strip", "social-strip"],
        "states": ["default"],
        "accessibility": [
            "<footer role=\"contentinfo\">",
            "링크 그룹에 의미 있는 heading 제공",
        ],
        "tokens": {
            "surface": "var(--color-surface-muted)",
            "border-top": "var(--color-border)",
            "padding": "var(--space-64) var(--space-24) var(--space-32)",
            "column-gap": "var(--space-48)",
            "inner-max-width": "1120px",
            "text": "var(--color-text-muted)",
        },
    },
    "layout-grid": {
        "parts": ["grid-container"],
        "states": ["default"],
        "accessibility": [
            "장식적 컨테이너 — 시맨틱은 자식 요소에 위임",
        ],
        "tokens": {
            "display": "grid",
            "gap": "var(--space-24)",
            "grid-1": "1 column <768px",
            "grid-2": "2 columns 768-1039px",
            "grid-3": "3 columns ≥1040px",
        },
    },
    "link": {
        "parts": ["anchor"],
        "states": ["default", "hover", "focus-visible", "visited"],
        "accessibility": [
            "의미 있는 링크 텍스트 (\"여기 클릭\" 금지)",
            "외부 링크는 aria-label에 명시",
            "focus ring은 전역 :focus-visible 규칙 사용",
        ],
        "tokens": {
            "color": "var(--color-text-muted)",
            "color-hover": "var(--color-text)",
            "underline-hover": "1px solid currentColor",
            "motion": "color var(--duration-120) var(--ease-standard)",
        },
    },
    "cta-inverse": {
        "parts": ["section-container", "headline", "supporting-text", "button-group"],
        "states": ["default"],
        "accessibility": [
            "aria-labelledby로 cta-headline id 연결",
            "primary CTA는 페이지당 1-2개로 제한",
        ],
        "tokens": {
            "surface": "var(--color-brand-primary)",
            "text": "var(--color-text-inverse)",
            "text-supporting": "var(--color-surface-tint)",
            "radius": "var(--radius-xl)",
            "padding": "var(--space-96) var(--space-48)",
            "button-primary-surface": "var(--color-surface)",
            "button-primary-text": "var(--color-brand-primary)",
            "button-secondary-border": "var(--color-text-inverse)",
        },
    },
    "quote-block": {
        "parts": ["blockquote", "quote-text", "attribution"],
        "states": ["default"],
        "accessibility": [
            "<blockquote>과 <cite> 사용",
            "인용부호는 CSS content 또는 장식 SVG로 처리",
        ],
        "tokens": {
            "border-left": "2px solid var(--color-border-strong)",
            "padding-left": "var(--space-16)",
            "text": "var(--color-text)",
            "text-muted": "var(--color-text-muted)",
            "font": "var(--font-body)",
            "size": "var(--text-lg)",
            "line-height": "var(--leading-relaxed)",
        },
    },
    "badge": {
        "parts": ["container", "value", "label(optional)"],
        "states": ["default"],
        "accessibility": [
            "정보를 담으면 aria-label 제공",
            "장식이면 aria-hidden=\"true\"",
        ],
        "tokens": {
            "surface": "var(--color-surface-tint)",
            "text": "var(--color-brand-primary)",
            "value-size": "var(--text-4xl)",
            "label-size": "var(--text-sm)",
            "label-color": "var(--color-text-muted)",
            "radius": "var(--radius-md)",
            "padding": "var(--space-12) var(--space-16)",
        },
    },
    "media-frame": {
        "parts": ["frame-container", "visual"],
        "states": ["default"],
        "accessibility": [
            "의미 있는 이미지면 alt 필수, 장식이면 alt=\"\"",
            "SVG는 role=\"img\"과 <title> 포함",
        ],
        "tokens": {
            "radius": "var(--radius-xl)",
            "border": "var(--color-border)",
            "surface": "var(--color-surface-tint)",
            "aspect-ratio": "4 / 3",
            "padding": "var(--space-24)",
        },
    },
    "trust-strip": {
        "parts": ["list-container", "item", "bullet-icon"],
        "states": ["default"],
        "accessibility": [
            "role=\"list\"로 리스트 시맨틱 유지",
            "불릿 SVG는 aria-hidden=\"true\"",
        ],
        "tokens": {
            "text": "var(--color-text-muted)",
            "font": "var(--font-mono)",
            "size": "var(--text-xs)",
            "bullet-color": "var(--color-brand-primary)",
            "gap": "var(--space-16)",
        },
    },
}


# Ordered list of (pattern, archetype) — first match wins.
# Regex-free simple substring matching keeps this easy to audit and extend.
SLOT_NAME_PATTERNS: list[tuple[str, str]] = [
    ("subheadline", "text-body"),
    ("supporting-text", "text-body"),
    ("description", "text-body"),
    ("-answer", "text-body"),
    ("eyebrow", "text-eyebrow"),
    ("headline", "text-heading"),
    ("-title", "text-heading"),
    ("site-header", "nav-bar"),
    ("site-nav", "nav-bar"),
    ("site-footer", "footer-bar"),
    ("footer-column", "footer-bar"),
    ("footer-legal", "footer-bar"),
    ("footer-social", "footer-bar"),
    ("footer-link", "link"),
    ("-link", "link"),
    ("press-quote", "quote-block"),
    ("-quote", "quote-block"),
    ("trust-strip", "trust-strip"),
    ("metric-highlight", "badge"),
    ("upgrade-banner", "badge"),
    ("feature-icon", "icon-holder"),
    ("-icon", "icon-holder"),
    ("feature-card", "surface-card"),
    ("testimonial-card", "surface-card"),
    ("pricing-card", "surface-card"),
    ("-card", "surface-card"),
    ("feature-grid", "layout-grid"),
    ("logo-cloud", "layout-grid"),
    ("-grid", "layout-grid"),
    ("cta-section", "cta-inverse"),
    ("cta-headline", "text-heading"),
    ("hero-visual", "media-frame"),
    ("-visual", "media-frame"),
]


def _infer_slot_archetype(name: str) -> str | None:
    """Return the archetype key for a component name, or None for family default."""
    low = name.lower()
    for needle, archetype in SLOT_NAME_PATTERNS:
        if needle in low:
            return archetype
    return None


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

CARD_COMPONENT_TOKENS = (
    "card",
    "tile",
    "module",
    "banner",
)

CTA_COMPONENT_TOKENS = (
    "button",
    "cta",
    "upgrade-banner",
)

NAV_DENSITY_TOKENS = (
    "nav",
    "menu",
    "sidebar",
    "topbar",
    "breadcrumb",
    "tab",
    "pagination",
    "filter",
    "chip",
    "toolbar",
    "switcher",
    "search",
)

DATA_PANEL_TOKENS = (
    "chart",
    "panel",
    "table",
    "grid",
    "stat",
    "insight",
    "metric",
    "summary",
)


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
    visual_guidance = _collect_visual_guidance(brand_profile, blueprint)
    typography_guidance = _collect_typography_guidance(brand_profile)
    responsive_guidance = _collect_responsive_guidance(blueprint)

    families: dict[str, list[dict]] = {}
    for comp in component_list:
        families.setdefault(comp["family"], []).append(comp)

    specs: list[dict] = []
    for comp in component_list:
        family = comp["family"]
        advanced = get_advanced_component(comp["name"])
        archetype_key = _infer_slot_archetype(comp["name"])
        archetype = SLOT_ARCHETYPES.get(archetype_key) if archetype_key else None
        family_anatomy = COMPONENT_ANATOMY.get(family) or COMPONENT_ANATOMY.get("data-display", {})
        source = advanced or archetype or family_anatomy

        kb_evidence = _find_kb_evidence(comp["name"], family, documents)

        spec = {
            "name": comp["name"],
            "family": family,
            "archetype": f"advanced:{comp['name']}" if advanced else archetype_key,
            "advanced_component": bool(advanced),
            "role": comp.get("role", ""),
            "source_pattern": comp.get("source", ""),
            "usage_guidance": (advanced or {}).get("use_when", comp.get("usage_guidance", [])),
            "avoid_when": (advanced or {}).get("avoid_when", comp.get("avoid_when", [])),
            "pairs_with": (advanced or {}).get("pairs_with", comp.get("pairs_with", [])),
            "anatomy": {
                "parts": (source.get("anatomy", {}) if isinstance(source.get("anatomy"), dict) else source).get("parts", []),
                "states": (source.get("anatomy", {}) if isinstance(source.get("anatomy"), dict) else source).get("states", []),
            },
            "tokens": _build_token_bindings(comp["name"], family, source),
            "accessibility": source.get("accessibility", []),
            "brand_adaptation": _build_adaptation_notes(
                comp["name"], family, brand_keywords, anti_keywords, adaptations, anti_rules
            ),
            "visual_adaptation": _build_visual_adaptation_notes(
                comp["name"], family, archetype_key, visual_guidance
            ),
            "observed_reference_evidence": _build_observed_reference_evidence(
                comp["name"], family, visual_guidance
            ),
            "reference_evidence": kb_evidence,
            "implementation_notes": _build_implementation_notes(
                comp["name"],
                family,
                brand_keywords,
                typography_guidance,
                responsive_guidance,
            ),
        }
        specs.append(spec)

    return {
        "brand": brand_name,
        "total_components": len(specs),
        "families": sorted(families.keys()),
        "brand_keywords": brand_keywords,
        "anti_keywords": anti_keywords,
        "global_adaptation": adaptations,
        "visual_guidance": visual_guidance,
        "typography_guidance": typography_guidance,
        "responsive_guidance": responsive_guidance,
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
    md_lines.append("1. **이모지를 UI로 쓰지 않는다** — 🎨 ✅ 🔥 ⚡ 🚀 ❌ ⭐ 📊 등 이모지를 아이콘, 상태 표시, 버튼 장식, 네비게이션 지표 자리에 절대 넣지 않는다. 리팩토링 중 카드/버튼/배지/탭/상태 UI에서 이모지를 발견하면 SVG 파일, SVG 컴포넌트, 또는 Lucide/Heroicons/Phosphor/Tabler 같은 아이콘 라이브러리로 교체한다.")
    md_lines.append("2. **컴포넌트를 직접 구현한다** — 아래 각 컴포넌트의 anatomy(구조), states(상태), 토큰 바인딩, 접근성 규칙을 그대로 따라 완전하게 구현한다. '임시', 'TODO', '플레이스홀더' 같은 반쪽 구현을 남기지 않는다.")
    md_lines.append("3. **라이브러리 기본 스타일 금지** — 라이브러리 컴포넌트를 그대로 import해서 쓰지 않는다. 반드시 디자인 토큰(--color-*, --space-*, --radius-*, --font-*)으로 스타일을 명시적으로 바인딩한다.")
    md_lines.append("4. **접근성은 옵션이 아니다** — 각 컴포넌트의 '접근성' 섹션에 정의된 role, aria-*, label, focus 관리 규칙을 전부 적용한다.")
    md_lines.append("5. **hex 값 하드코딩 금지** — 색상은 반드시 semantic token을 경유한다 (예: `color: var(--color-ink)` not `color: #2C2C2C`).")
    md_lines.append("6. **모바일 overflow 금지** — 버튼, CTA, 탭, 필터칩, 툴바 액션은 320px viewport에서 화면 밖으로 나가면 안 된다. fixed/min-width px 값으로 폭을 고정하지 말고 wrap/stack fallback을 제공한다.")
    md_lines.append("")

    md_lines.append("## 브랜드 적용 규칙\n")
    for aspect, rule in specs_data.get("global_adaptation", {}).items():
        md_lines.append(f"- **{aspect}**: {rule}")
    md_lines.append("")

    visual_guidance = specs_data.get("visual_guidance") or {}
    if visual_guidance.get("connected"):
        md_lines.append("## Visual-reference 적용 원칙\n")
        md_lines.append("- anatomy / states / accessibility는 설계서(spec)와 KB 근거를 유지하고, visual adaptation은 elevation / framing / prominence / density 같은 표현 계층에만 advisory signal로 적용한다.")
        summary_bits = []
        for key in ["surface_style", "density", "corner_style", "top_layout_cue"]:
            value = visual_guidance.get(key)
            if value:
                summary_bits.append(f"{key}={value}")
        if summary_bits:
            md_lines.append(f"- Active visual signals: {', '.join(summary_bits)}")
        hint_keys = sorted((visual_guidance.get("component_style_hints") or {}).keys())
        if hint_keys:
            md_lines.append(f"- Connected component hints: {', '.join(hint_keys)}")
        md_lines.append("")

    typography_guidance = specs_data.get("typography_guidance") or {}
    if typography_guidance.get("active"):
        md_lines.append("## Typography Guardrails\n")
        md_lines.append(
            "- 한글 기반 제품은 line-break / scale / tracking을 영문 랜딩 기본값으로 처리하지 않고, 아래 가드레일을 구현 기본값으로 사용한다."
        )
        headline_font = typography_guidance.get("headline_font") or {}
        body_font = typography_guidance.get("body_font") or {}
        wrap = typography_guidance.get("wrap") or {}
        headline_wrap = wrap.get("headline") or {}
        body_wrap = wrap.get("body") or {}
        md_lines.append(
            f"- Headline: {headline_font.get('name', 'N/A')} | line-height {headline_font.get('line_height', 'n/a')} | tracking {headline_font.get('letter_spacing', 'n/a')}"
        )
        md_lines.append(
            f"- Body: {body_font.get('name', 'N/A')} | line-height {body_font.get('line_height', 'n/a')} | label line-height {body_font.get('ui_label_line_height', 'n/a')}"
        )
        md_lines.append(
            "- Wrap defaults: "
            f"headline word-break={headline_wrap.get('word_break', 'n/a')}, "
            f"headline text-wrap={headline_wrap.get('text_wrap', 'n/a')}, "
            f"body word-break={body_wrap.get('word_break', 'n/a')}"
        )
        scale = typography_guidance.get("scale") or {}
        if scale.get("guidance"):
            md_lines.append(f"- Scale guidance: {scale['guidance']}")
        for rule in typography_guidance.get("rules", [])[:4]:
            md_lines.append(f"- {rule}")
        md_lines.append("")

    responsive_guidance = specs_data.get("responsive_guidance") or {}
    if responsive_guidance.get("active"):
        md_lines.append("## Responsive Resilience\n")
        md_lines.append(
            "- 모바일에서 horizontal scroll이 생기거나 primary action이 화면 밖으로 나가면 컴포넌트 구현이 완료된 것이 아니다."
        )
        widths = responsive_guidance.get("required_widths_px", [])
        if widths:
            md_lines.append(f"- Required viewport checks: {', '.join(str(width) + 'px' for width in widths)}")
        for rule in responsive_guidance.get("control_rules", [])[:5]:
            md_lines.append(f"- {rule}")
        md_lines.append("")

    for spec in specs_data["specs"]:
        md_lines.append("---\n")
        md_lines.append(f"## {spec['family']} / {spec['name']}\n")
        role = spec.get("role") or "—"
        md_lines.append(f"**역할**: {role}\n")

        if spec.get("source_pattern"):
            md_lines.append(f"**탐지 출처**: {spec['source_pattern']}\n")
        if spec.get("archetype"):
            md_lines.append(f"**Slot archetype**: `{spec['archetype']}`\n")

        if spec.get("advanced_component"):
            md_lines.append("### Advanced Usage\n")
            if spec.get("usage_guidance"):
                md_lines.append("Use when:")
                for item in spec.get("usage_guidance", [])[:3]:
                    md_lines.append(f"- {item}")
            if spec.get("avoid_when"):
                md_lines.append("Avoid when:")
                for item in spec.get("avoid_when", [])[:2]:
                    md_lines.append(f"- {item}")
            if spec.get("pairs_with"):
                md_lines.append(f"Pairs with: {', '.join(spec.get('pairs_with', [])[:6])}")
            md_lines.append("")

        md_lines.append("### 구조 (Anatomy)\n")
        for part in spec["anatomy"]["parts"]:
            md_lines.append(f"- {part}")
        md_lines.append("")

        md_lines.append("### 상태 (States)\n")
        md_lines.append("| 상태 | 설명 |")
        md_lines.append("|------|------|")
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

        if spec.get("visual_adaptation"):
            md_lines.append("### Visual Adaptation Hints\n")
            for note in spec["visual_adaptation"]:
                meta_bits = []
                if note.get("source_hint"):
                    meta_bits.append(f"source={note['source_hint']}")
                if note.get("confidence") is not None:
                    meta_bits.append(f"confidence={note['confidence']}")
                if note.get("provenance"):
                    meta_bits.append(f"provenance={note['provenance']}")
                if note.get("direction"):
                    meta_bits.append(f"direction={note['direction']}")
                if note.get("evidence"):
                    meta_bits.append(f"evidence={', '.join(note['evidence'])}")
                suffix = f" ({'; '.join(meta_bits)})" if meta_bits else ""
                md_lines.append(f"- **{note['aspect']}**: {note['summary']}{suffix}")
            md_lines.append("")

        if spec.get("observed_reference_evidence"):
            md_lines.append("### Observed Reference Evidence\n")
            md_lines.append("- 아래 근거는 형태, 밀도, 상호작용 affordance 참고용이다. 색상, 폰트, IA, 카피, 외부 에셋은 흡수하지 않는다.")
            for evidence in spec["observed_reference_evidence"][:3]:
                traits = evidence.get("absorbed_traits") or []
                trait_suffix = f" traits={', '.join(traits[:4])}" if traits else ""
                md_lines.append(
                    f"- **{evidence['provider_id']} / {evidence['context_id']}**: "
                    f"{evidence['label']}{trait_suffix}"
                )
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


def _collect_visual_guidance(brand_profile: dict, blueprint: dict) -> dict:
    visual_reference = blueprint.get("visual_reference") or brand_profile.get("_resolved_visual_reference") or {}
    component_style_hints = (
        blueprint.get("component_style_hints")
        or visual_reference.get("component_style_hints")
        or {}
    )
    visual_motifs = blueprint.get("visual_language") or visual_reference.get("visual_motifs") or {}
    layout_cues = blueprint.get("layout_cues") or visual_reference.get("layout_cues") or []
    design_context_pack = blueprint.get("design_context_pack") or brand_profile.get("_design_context_pack") or {}

    return {
        "connected": bool(visual_reference or component_style_hints or visual_motifs or layout_cues),
        "policy": "advisory-only: anatomy / states / accessibility stay grounded in spec and KB evidence",
        "surface_style": (visual_motifs.get("surface_style") or {}).get("value"),
        "density": (visual_motifs.get("density") or {}).get("value"),
        "corner_style": (visual_motifs.get("corner_style") or {}).get("value"),
        "typography_mood": (visual_motifs.get("typography_mood") or {}).get("value"),
        "top_layout_cue": layout_cues[0]["id"] if layout_cues else None,
        "component_style_hints": component_style_hints,
        "design_context_activation": design_context_pack.get("activation_state"),
        "reference_observations": _collect_reference_observations(design_context_pack),
    }


def _collect_typography_guidance(brand_profile: dict) -> dict:
    font_system = brand_profile.get("_resolved_font_system") or {}
    script_guardrails = font_system.get("script_guardrails") or {}
    if not script_guardrails:
        return {"active": False}
    return {"active": True, **script_guardrails}


def _collect_responsive_guidance(blueprint: dict) -> dict:
    policy = (blueprint.get("governance") or {}).get("responsive_resilience_policy") or {}
    if not policy:
        return {"active": False}
    contract = policy.get("viewport_contract") or {}
    return {
        "active": True,
        "rule": policy.get("rule", ""),
        "required_widths_px": contract.get("required_widths_px", [320, 360, 390, 430, 768, 1024, 1440]),
        "pass_condition": contract.get("pass_condition", ""),
        "control_rules": policy.get("control_rules", []),
        "failure_patterns": policy.get("failure_patterns", []),
    }


def _collect_reference_observations(design_context_pack: dict) -> list[dict]:
    if not isinstance(design_context_pack, dict):
        return []
    observations: list[dict] = []
    for card in design_context_pack.get("context_cards", []) or []:
        if not isinstance(card, dict):
            continue
        if card.get("provenance_level") != "observed":
            continue
        observations.append(
            {
                "context_id": card.get("context_id"),
                "provider_id": card.get("provider_id"),
                "kind": card.get("kind"),
                "label": card.get("label"),
                "flows": card.get("flows", []),
                "morphology": card.get("morphology", []),
                "absorbed_traits": card.get("absorbed_traits", []),
                "must_not_absorb": card.get("must_not_absorb", []),
            }
        )
    return observations[:12]


def _build_token_bindings(name: str, family: str, source: dict) -> dict[str, str]:
    """Return the token bindings for a component.

    Uses the provided source (either a slot archetype or a family anatomy entry)
    and substitutes any remaining `{component}` / `{severity}` placeholders that
    predate the var(--*) migration.
    """
    raw = source.get("tokens", {})
    result: dict[str, str] = {}
    for slot, pattern in raw.items():
        if not isinstance(pattern, str):
            result[slot] = pattern
            continue
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
        "marketing": ["color", "motion", "density"],
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


def _build_visual_adaptation_notes(
    name: str,
    family: str,
    archetype_key: str | None,
    visual_guidance: dict,
) -> list[dict]:
    if not visual_guidance.get("connected"):
        return []

    hints = visual_guidance.get("component_style_hints") or {}
    low_name = name.lower()
    surface_style = visual_guidance.get("surface_style") or "flat"
    density = visual_guidance.get("density") or "balanced"
    top_layout_cue = visual_guidance.get("top_layout_cue")

    notes: list[dict] = []
    card_signal = hints.get("cards")
    nav_signal = hints.get("navigation")
    data_signal = hints.get("data_display")
    hero_signal = hints.get("hero")
    panel_signal = hints.get("panel")

    card_like = archetype_key == "surface-card" or _matches_any_token(low_name, CARD_COMPONENT_TOKENS)
    cta_like = family == "button" or archetype_key == "cta-inverse" or _matches_any_token(low_name, CTA_COMPONENT_TOKENS)
    nav_like = family == "navigation" or archetype_key == "nav-bar" or _matches_any_token(low_name, NAV_DENSITY_TOKENS)
    data_panel_like = family == "data-display" or _matches_any_token(low_name, DATA_PANEL_TOKENS)

    if card_like or data_panel_like:
        notes.append(
            _make_visual_note(
                aspect="card_elevation_tendency",
                summary=_describe_card_elevation_tendency(surface_style, density),
                source_hint="cards",
                signal=card_signal,
                extra_evidence=[f"surface={surface_style}", f"density={density}"],
            )
        )
        notes.append(
            _make_visual_note(
                aspect="border_vs_fill_emphasis",
                summary=_describe_border_fill_emphasis(surface_style),
                source_hint="cards",
                signal=card_signal,
                extra_evidence=[f"surface={surface_style}"],
            )
        )

    if cta_like:
        cta_signal = hero_signal or card_signal
        cta_source = "hero" if hero_signal else "cards" if card_signal else "layout_cue"
        extra = [f"layout={top_layout_cue}"] if top_layout_cue else []
        extra.append(f"density={density}")
        notes.append(
            _make_visual_note(
                aspect="cta_prominence",
                summary=_describe_cta_prominence(
                    top_layout_cue,
                    density,
                    has_hero_signal=bool(hero_signal or archetype_key == "cta-inverse" or "cta" in low_name),
                ),
                source_hint=cta_source,
                signal=cta_signal,
                extra_evidence=extra,
            )
        )

    if nav_like:
        nav_source = "navigation" if nav_signal else "data_display" if data_signal else "layout_cue"
        nav_primary_signal = nav_signal or data_signal
        extra = [f"layout={top_layout_cue}"] if top_layout_cue else []
        extra.append(f"density={density}")
        notes.append(
            _make_visual_note(
                aspect="filter_nav_density",
                summary=_describe_filter_nav_density(top_layout_cue, density),
                source_hint=nav_source,
                signal=nav_primary_signal,
                extra_evidence=extra,
            )
        )

    if data_panel_like:
        panel_source = "data_display" if data_signal else "panel" if panel_signal else "cards"
        panel_primary_signal = data_signal or panel_signal or card_signal
        extra = [f"layout={top_layout_cue}"] if top_layout_cue else []
        extra.extend([f"surface={surface_style}", f"density={density}"])
        notes.append(
            _make_visual_note(
                aspect="chart_panel_framing",
                summary=_describe_chart_panel_framing(surface_style, density, top_layout_cue),
                source_hint=panel_source,
                signal=panel_primary_signal,
                extra_evidence=extra,
            )
        )

    deduped: list[dict] = []
    seen_aspects: set[str] = set()
    for note in notes:
        aspect = note.get("aspect")
        if not aspect or aspect in seen_aspects:
            continue
        seen_aspects.add(aspect)
        deduped.append(note)
    return deduped


def _build_observed_reference_evidence(name: str, family: str, visual_guidance: dict) -> list[dict]:
    observations = visual_guidance.get("reference_observations") or []
    if not observations:
        return []

    component_terms = _component_match_terms(name, family)
    scored: list[tuple[int, dict]] = []
    for observation in observations:
        if not isinstance(observation, dict):
            continue
        obs_terms = _observation_terms(observation)
        score = len(component_terms & obs_terms)
        provider_id = str(observation.get("provider_id") or "")
        if provider_id == "website-inspection":
            score += 1
        if family == "navigation" and {"navigation", "nav", "sidebar"} & obs_terms:
            score += 3
        if family == "data-display" and {"dashboard", "data", "table", "grid", "card", "panel"} & obs_terms:
            score += 3
        if family == "button" and {"click", "input", "cta"} & obs_terms:
            score += 2
        if family == "overlay" and {"drawer", "modal", "overlay", "inspector"} & obs_terms:
            score += 2
        if score:
            scored.append((score, observation))

    if not scored:
        scored = [
            (1, observation)
            for observation in observations
            if isinstance(observation, dict) and observation.get("provider_id") == "website-inspection"
        ][:1]

    scored.sort(key=lambda item: (-item[0], str(item[1].get("context_id") or "")))
    evidence: list[dict] = []
    for _score, observation in scored[:3]:
        evidence.append(
            {
                "context_id": observation.get("context_id"),
                "provider_id": observation.get("provider_id"),
                "kind": observation.get("kind"),
                "label": observation.get("label"),
                "flows": observation.get("flows", []),
                "morphology": observation.get("morphology", []),
                "absorbed_traits": observation.get("absorbed_traits", []),
                "must_not_absorb": observation.get("must_not_absorb", []),
            }
        )
    return evidence


def _component_match_terms(name: str, family: str) -> set[str]:
    terms = set(_split_component_terms(name))
    terms.update(_split_component_terms(family))
    family_expansions = {
        "navigation": {"navigation", "nav", "sidebar", "topbar", "tabs", "menu"},
        "data-display": {"dashboard", "data", "table", "grid", "card", "panel", "metric"},
        "button": {"button", "cta", "click", "action"},
        "input": {"input", "form", "composer", "search"},
        "feedback": {"badge", "status", "alert", "toast"},
        "overlay": {"modal", "drawer", "overlay", "inspector"},
        "marketing": {"hero", "section", "cta", "landing"},
    }
    terms.update(family_expansions.get(family, set()))
    return terms


def _observation_terms(observation: dict) -> set[str]:
    values: list[str] = []
    for key in ("provider_id", "kind", "label"):
        value = observation.get(key)
        if value:
            values.append(str(value))
    for key in ("flows", "morphology", "absorbed_traits"):
        for item in observation.get(key, []) or []:
            values.append(str(item))
    return set(_split_component_terms(" ".join(values)))


def _split_component_terms(value: str) -> list[str]:
    normalized = "".join(ch.lower() if ch.isalnum() else " " for ch in str(value))
    return [part for part in normalized.split() if part]


def _make_visual_note(
    aspect: str,
    summary: str,
    source_hint: str,
    signal: dict | None,
    extra_evidence: list[str] | None = None,
) -> dict:
    confidence = 0.45
    direction = None
    evidence: list[str] = []

    if isinstance(signal, dict):
        raw_confidence = signal.get("confidence")
        if isinstance(raw_confidence, (int, float)):
            confidence = round(float(raw_confidence), 2)
        raw_direction = signal.get("direction")
        if isinstance(raw_direction, str) and raw_direction.strip():
            direction = raw_direction.strip()
        for item in signal.get("evidence", []):
            if isinstance(item, str) and item.strip():
                evidence.append(item.strip())

    for item in extra_evidence or []:
        if item:
            evidence.append(item)

    deduped_evidence = list(dict.fromkeys(evidence))[:4]
    return {
        "aspect": aspect,
        "summary": summary,
        "source_hint": source_hint,
        "confidence": confidence,
        "provenance": ((signal or {}).get("provenance") or {}).get("level") if isinstance(signal, dict) else None,
        "direction": direction,
        "evidence": deduped_evidence,
    }


def _matches_any_token(name: str, tokens: tuple[str, ...]) -> bool:
    return any(token in name for token in tokens)


def _describe_card_elevation_tendency(surface_style: str, density: str) -> str:
    base = {
        "flat": "카드는 거의 무그림자 평면으로 유지하고 tint/divider로 계층을 만든다.",
        "tinted": "카드는 낮은 elevation만 허용하고 색면 차이로 그룹을 구분한다.",
        "outlined": "카드는 shadow보다 thin border framing으로 위계를 만든다.",
        "elevated": "카드는 중간 이하 shadow만 허용하고 deep shadow stack은 피한다.",
        "glassy": "카드는 translucent fill과 얕은 blur를 쓰되 contrast guardrail을 먼저 확보한다.",
    }.get(surface_style, "카드는 과장된 depth 없이 절제된 surface hierarchy로 정리한다.")
    density_note = {
        "airy": "내부 여백은 넉넉하게 두고 card breathing room을 확보한다.",
        "balanced": "padding은 균형 있게 유지하되 header/body 구획은 분명하게 둔다.",
        "dense": "압축된 spacing에서도 header/body/footer 구획은 divider나 tint로 유지한다.",
    }.get(density, "spacing 계층은 안정적으로 유지한다.")
    return f"{base} {density_note}"


def _describe_border_fill_emphasis(surface_style: str) -> str:
    return {
        "flat": "fill 중심이다. neutral surface를 기본으로 하고 border는 상태 변화나 구획 보조에만 쓴다.",
        "tinted": "fill 중심이다. tint surface로 성격을 만들고 border는 아주 얇게 보조한다.",
        "outlined": "border 중심이다. fill은 조용하게 유지하고 thin outline과 divider로 구조를 드러낸다.",
        "elevated": "fill 중심이다. depth와 surface contrast가 우선이며 border는 선택적으로만 쓴다.",
        "glassy": "fill 중심이되 edge contrast guardrail이 필요하다. 투명 fill과 얇은 경계선을 함께 관리한다.",
    }.get(surface_style, "fill과 border를 동시에 과장하지 말고 한 축만 주도적으로 사용한다.")


def _describe_cta_prominence(top_layout_cue: str | None, density: str, has_hero_signal: bool = False) -> str:
    if has_hero_signal or top_layout_cue == "landing-narrative":
        return "CTA prominence는 strong이다. 섹션당 primary CTA 1개만 fill/accent로 강하게 띄우고 secondary는 조용하게 후퇴시킨다."
    if top_layout_cue in {"dashboard-grid", "data-review-surface", "split-pane-workspace"} or density == "dense":
        return "CTA prominence는 restrained이다. 데이터 작업 흐름을 가리지 않도록 primary만 선명하게 두고 나머지는 text/ghost로 낮춘다."
    return "CTA prominence는 medium이다. primary action은 분명하게 보이되 화면 전체를 지배하지 않게 유지한다."


def _describe_filter_nav_density(top_layout_cue: str | None, density: str) -> str:
    if top_layout_cue == "split-pane-workspace":
        return "filter/nav density는 compact하다. 고정 sidebar와 scope controls를 묶고 toolbar는 1줄 우선으로 유지한다."
    if top_layout_cue == "landing-narrative":
        return "filter/nav density는 low다. top nav는 가볍게 유지하고 filter controls는 별도 섹션 또는 로컬 toolbar로 분리한다."
    if top_layout_cue == "data-review-surface" or density == "dense":
        return "filter/nav density는 compact하다. chip, scope, pagination을 촘촘하게 묶되 의미 단위별 group은 분리한다."
    return "filter/nav density는 balanced다. global nav와 local filter를 섞지 말고 계층별 간격 차이로 구조를 드러낸다."


def _describe_chart_panel_framing(surface_style: str, density: str, top_layout_cue: str | None) -> str:
    base = {
        "flat": "차트 패널은 flush surface와 thin divider 중심으로 프레이밍한다.",
        "tinted": "차트 패널은 soft tint frame과 restrained divider로 프레이밍한다.",
        "outlined": "차트 패널은 thin border, labeled header, body/footer 분리로 프레이밍한다.",
        "elevated": "차트 패널은 single raised surface로 프레이밍하고 nested card는 피한다.",
        "glassy": "차트 패널은 translucent surface를 쓰더라도 axis, legend, tooltip 대비를 먼저 확보한다.",
    }.get(surface_style, "차트 패널은 데이터를 읽기 쉬운 단일 frame으로 정리한다.")
    if top_layout_cue in {"dashboard-grid", "data-review-surface"} or density == "dense":
        return f"{base} 헤더의 metric, controls, plot 영역을 분리하고 내부 여백은 촘촘하게 관리한다."
    return f"{base} 헤더 메타데이터와 본문 visualization 사이의 breathing room을 충분히 둔다."


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


def _build_implementation_notes(
    name: str,
    family: str,
    brand_keywords: list[str],
    typography_guidance: dict | None = None,
    responsive_guidance: dict | None = None,
) -> list[str]:
    notes = [
        "기존에 같은 역할의 컴포넌트가 있으면 토큰 교체부터 시작",
        "variant prop으로 시각적 변형을 관리 (하드코딩 금지)",
    ]

    if family == "button":
        notes.append("size prop: sm / md / lg (터치 영역은 항상 최소 44px 보장)")
        notes.append("모든 버튼은 `max-inline-size: 100%`와 `min-inline-size: 0`을 기본 보호값으로 갖고, 긴 라벨은 모바일에서 wrap 또는 action-group stack으로 처리")
        notes.append("fixed `width`/`min-width` px 값으로 CTA 폭을 고정하지 않음 — 필요하면 container query 또는 <=480px stack fallback을 함께 정의")
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
    elif family == "marketing":
        notes.append("섹션에 <h2 id=\"...\">과 aria-labelledby 필수")
        notes.append("CSS 변수(var(--color-*))를 그대로 쓰고 hex 하드코딩 금지")
        notes.append("다크 모드는 globals.css의 prefers-color-scheme 블록에 위임")

    if typography_guidance and typography_guidance.get("primary_script") == "korean":
        if family in {"marketing", "editorial"}:
            notes.append("한글 헤딩은 `word-break: keep-all` / `overflow-wrap: normal`을 기본값으로 두고, 강제 `<br />`는 breakpoint 검증 전 넣지 않음")
            scale = typography_guidance.get("scale") or {}
            if scale.get("guidance"):
                notes.append(scale["guidance"])
        if family in {"marketing", "editorial", "data-display", "navigation"}:
            body_font = typography_guidance.get("body_font") or {}
            if body_font.get("ui_label_line_height"):
                notes.append(
                    f"좁은 UI 텍스트는 {body_font.get('name', 'body font')} 기준 label line-height {body_font.get('ui_label_line_height')}를 참고해 뭉침을 방지"
                )

    if responsive_guidance and responsive_guidance.get("active"):
        if family in {"button", "navigation", "feedback", "input"} or any(token in name for token in ["button", "cta", "tab", "chip", "toolbar"]):
            widths = responsive_guidance.get("required_widths_px", [])
            if widths:
                notes.append(
                    f"반응형 검증: {', '.join(str(width) + 'px' for width in widths[:4])}에서 control overflow와 viewport horizontal scroll이 없어야 함"
                )
            notes.append("action row는 narrow viewport에서 `flex-wrap: wrap` 또는 세로 stack으로 전환하고, overflow-x 숨김으로 문제를 덮지 않음")

    if "calm" in brand_keywords:
        notes.append("애니메이션은 상태 설명용으로만 사용, 장식 효과 금지")
    if "editorial" in brand_keywords:
        notes.append("텍스트 위계가 핵심 — 컬러보다 weight/size로 구분")

    return notes
