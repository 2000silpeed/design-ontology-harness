"""Font decision engine based on real-world designer practices.

Selects optimal typeface combinations based on brand keywords,
product type, platform, and reading context. All fonts in the
database are production-proven choices used by professional designers.

Supports optional font-reference.md for curated font data.
"""

from __future__ import annotations

from pathlib import Path


# ──────────────────────────────────────────────
# 1. Font Database — 실제 디자이너들이 쓰는 서체
# ──────────────────────────────────────────────

FONT_DB: list[dict] = [
    # ── Geometric Sans ──
    {
        "name": "Inter",
        "family": "geometric-sans",
        "personality": ["neutral", "precise", "modern"],
        "best_for": ["saas", "dashboard", "developer-tool", "mobile"],
        "korean_pair": "Pretendard",
        "weight_range": "100-900",
        "variable": True,
        "source": "Google Fonts",
        "note": "가장 범용적인 UI 서체. 작은 크기에서도 가독성 우수. Figma 기본 서체.",
    },
    {
        "name": "DM Sans",
        "family": "geometric-sans",
        "personality": ["clean", "friendly", "geometric"],
        "best_for": ["saas", "mobile", "marketing"],
        "korean_pair": "Pretendard",
        "weight_range": "400-700",
        "variable": True,
        "source": "Google Fonts",
        "note": "Inter보다 기하학적이고 부드러운 인상. 스타트업에서 인기.",
    },
    {
        "name": "Plus Jakarta Sans",
        "family": "geometric-sans",
        "personality": ["bold", "confident", "contemporary"],
        "best_for": ["saas", "fintech", "branding"],
        "korean_pair": "Wanted Sans",
        "weight_range": "200-800",
        "variable": True,
        "source": "Google Fonts",
        "note": "두꺼운 weight에서 임팩트가 강함. 헤드라인용으로 우수.",
    },
    {
        "name": "Space Grotesk",
        "family": "geometric-sans",
        "personality": ["precise", "technical", "distinctive"],
        "best_for": ["developer-tool", "fintech", "data-heavy"],
        "korean_pair": "Pretendard",
        "weight_range": "300-700",
        "variable": True,
        "source": "Google Fonts",
        "note": "숫자 디자인이 뛰어남. 데이터 대시보드에 적합.",
    },
    {
        "name": "Outfit",
        "family": "geometric-sans",
        "personality": ["bold", "modern", "energetic"],
        "best_for": ["mobile", "marketing", "consumer"],
        "korean_pair": "SUIT",
        "weight_range": "100-900",
        "variable": True,
        "source": "Google Fonts",
        "note": "둥근 터미널로 친근하면서도 현대적. 모바일 UI에 좋음.",
    },
    # ── Humanist Sans ──
    {
        "name": "Pretendard",
        "family": "humanist-sans",
        "personality": ["trustworthy", "readable", "professional"],
        "best_for": ["saas", "enterprise", "editorial", "mobile"],
        "korean_pair": None,
        "korean_native": True,
        "korean_context": {
            "glyph_width": "중간",
            "jaso_balance": "우수 — 초성/중성/종성 균형이 잘 잡혀 있음",
            "small_size": "13px까지 가독성 유지",
            "best_for_kr": ["UI 전반", "대시보드", "모바일 앱", "장문 본문"],
            "avoid_for_kr": [],
            "pair_with_latin": "Inter (x-height/weight 일치)",
            "note_kr": "한글 UI 서체의 사실상 표준. 토스, 당근, 리디 등 국내 주요 서비스에서 사용. 자간이 자연스럽고 weight 전 구간에서 안정적.",
        },
        "weight_range": "100-900",
        "variable": True,
        "source": "GitHub (cactus/pretendard)",
        "note": "한글 UI 서체의 사실상 표준. Apple SD Gothic Neo 기반이지만 더 정교함. 라틴은 Inter 계열.",
    },
    {
        "name": "Source Sans 3",
        "family": "humanist-sans",
        "personality": ["trustworthy", "clear", "institutional"],
        "best_for": ["enterprise", "government", "documentation"],
        "korean_pair": "Noto Sans KR",
        "weight_range": "200-900",
        "variable": True,
        "source": "Google Fonts",
        "note": "Adobe가 만든 오픈소스 서체. 공공/기관 서비스에서 많이 사용.",
    },
    {
        "name": "IBM Plex Sans",
        "family": "humanist-sans",
        "personality": ["trustworthy", "precise", "institutional"],
        "best_for": ["enterprise", "fintech", "data-heavy", "developer-tool"],
        "korean_pair": "IBM Plex Sans KR",
        "weight_range": "100-700",
        "variable": False,
        "source": "Google Fonts",
        "note": "IBM Carbon Design System 공식 서체. Mono 패밀리까지 일관된 디자인.",
    },
    {
        "name": "Noto Sans KR",
        "family": "humanist-sans",
        "personality": ["neutral", "readable", "universal"],
        "best_for": ["global", "enterprise", "documentation", "mobile"],
        "korean_pair": None,
        "korean_native": True,
        "korean_context": {
            "glyph_width": "넓음",
            "jaso_balance": "양호 — 고딕 기반 깔끔한 형태",
            "small_size": "12px까지 가독성 유지",
            "best_for_kr": ["다국어 서비스", "공공/기관", "문서 중심", "장문 본문"],
            "avoid_for_kr": ["좁은 UI 공간 — 글자폭이 넓어서 공간을 많이 차지"],
            "pair_with_latin": "Noto Sans (같은 Noto 패밀리)",
            "note_kr": "Google이 만든 범용 한글 서체. 글자폭이 넓어서 여유 있는 레이아웃에 적합. 다국어 지원이 필요한 서비스의 기본 선택.",
        },
        "weight_range": "100-900",
        "variable": True,
        "source": "Google Fonts",
        "note": "Google의 범용 서체. 전 세계 문자 지원. Noto Sans KR은 한글 최적화.",
    },
    {
        "name": "Wanted Sans",
        "family": "humanist-sans",
        "personality": ["modern", "confident", "professional"],
        "best_for": ["saas", "hr-tech", "mobile"],
        "korean_pair": None,
        "korean_native": True,
        "korean_context": {
            "glyph_width": "중간-좁음",
            "jaso_balance": "우수 — 현대적 비율, 자간이 좋음",
            "small_size": "13px까지 가독성 유지",
            "best_for_kr": ["SaaS", "모바일 앱", "현대적 브랜딩", "데이터 대시보드"],
            "avoid_for_kr": ["장문 본문 — Pretendard보다 line-height 여유가 적음"],
            "pair_with_latin": "Plus Jakarta Sans (weight/personality 일치)",
            "note_kr": "원티드에서 공개. Pretendard보다 현대적이고 자신감 있는 인상. 헤딩에서 특히 좋음. bold weight에서 임팩트.",
        },
        "weight_range": "400-800",
        "variable": True,
        "source": "GitHub (wanteddev)",
        "note": "원티드에서 공개한 한글 서체. 현대적이고 깔끔한 인상. 한글 자간이 좋음.",
    },
    {
        "name": "SUIT",
        "family": "humanist-sans",
        "personality": ["clean", "modern", "friendly"],
        "best_for": ["mobile", "consumer", "saas"],
        "korean_pair": None,
        "korean_native": True,
        "korean_context": {
            "glyph_width": "중간",
            "jaso_balance": "양호 — Pretendard 계열이지만 더 둥글고 부드러움",
            "small_size": "13px까지 가독성 유지",
            "best_for_kr": ["소비자 앱", "모바일", "친근한 톤의 서비스"],
            "avoid_for_kr": ["기관/금융 — 너무 캐주얼할 수 있음"],
            "pair_with_latin": "Outfit (둥근 터미널 매칭)",
            "note_kr": "Pretendard보다 부드럽고 친근한 인상. 교육, 라이프스타일, 커뮤니티 서비스에 적합.",
        },
        "weight_range": "100-900",
        "variable": True,
        "source": "GitHub (sun-typeface)",
        "note": "Pretendard 계열이지만 더 둥글고 부드러운 한글 서체.",
    },
    # ── Serif Display ──
    {
        "name": "Spoqa Han Sans Neo",
        "family": "geometric-sans",
        "personality": ["clean", "precise", "geometric"],
        "best_for": ["saas", "dashboard", "data-heavy"],
        "korean_pair": None,
        "korean_native": True,
        "korean_context": {
            "glyph_width": "중간-좁음",
            "jaso_balance": "양호 — 기하학적이고 직선적",
            "small_size": "13px까지 가독성 유지",
            "best_for_kr": ["SaaS", "데이터 대시보드", "깔끔한 UI"],
            "avoid_for_kr": ["장문 본문 — line-height 여유 부족", "감성적 브랜딩"],
            "pair_with_latin": "Source Sans 3 (같은 Source 계열)",
            "note_kr": "Pretendard 이전 시대의 한글 UI 표준. 요기요, 여기어때 등에서 사용. 깔끔하지만 weight 범위와 Variable 미지원이 아쉬움. 신규 프로젝트에서는 Pretendard 추천.",
        },
        "weight_range": "100-700",
        "variable": False,
        "source": "GitHub (spoqa/spoqa-han-sans)",
        "note": "스포카에서 만든 한글 산세리프. Source Sans Pro 기반. 깔끔한 데이터 UI에 적합.",
    },
    # ── Serif Display ──
    {
        "name": "Playfair Display",
        "family": "serif-display",
        "personality": ["editorial", "luxury", "elegant"],
        "best_for": ["editorial", "fashion", "luxury", "branding"],
        "korean_pair": "Noto Serif KR",
        "weight_range": "400-900",
        "variable": True,
        "source": "Google Fonts",
        "note": "에디토리얼 디자인의 대표 서체. 헤드라인 전용으로 사용.",
    },
    {
        "name": "DM Serif Display",
        "family": "serif-display",
        "personality": ["editorial", "warm", "classic"],
        "best_for": ["editorial", "content", "branding"],
        "korean_pair": "Noto Serif KR",
        "weight_range": "400",
        "variable": False,
        "source": "Google Fonts",
        "note": "DM Sans와 짝을 이루는 세리프. 따뜻하고 고전적인 인상.",
    },
    {
        "name": "Libre Baskerville",
        "family": "serif-display",
        "personality": ["trustworthy", "classic", "readable"],
        "best_for": ["editorial", "documentation", "legal", "finance"],
        "korean_pair": "Noto Serif KR",
        "weight_range": "400-700",
        "variable": False,
        "source": "Google Fonts",
        "note": "Baskerville 계열. 본문에서도 읽기 좋은 세리프. 신뢰감 있는 인상.",
    },
    {
        "name": "EB Garamond",
        "family": "serif-display",
        "personality": ["luxury", "classic", "elegant"],
        "best_for": ["luxury", "editorial", "publishing"],
        "korean_pair": "Noto Serif KR",
        "weight_range": "400-800",
        "variable": True,
        "source": "Google Fonts",
        "note": "클래식 Garamond의 디지털 버전. 장문 읽기에 최적. 고급 브랜드에 적합.",
    },
    {
        "name": "Cormorant Garamond",
        "family": "serif-display",
        "personality": ["luxury", "elegant", "delicate"],
        "best_for": ["luxury", "fashion", "branding"],
        "korean_pair": "Noto Serif KR",
        "weight_range": "300-700",
        "variable": False,
        "source": "Google Fonts",
        "note": "얇은 weight에서 매우 우아한 인상. 대형 헤드라인에 효과적.",
    },
    {
        "name": "Lora",
        "family": "serif-body",
        "personality": ["warm", "readable", "editorial"],
        "best_for": ["editorial", "blog", "content", "documentation"],
        "korean_pair": "Noto Serif KR",
        "weight_range": "400-700",
        "variable": True,
        "source": "Google Fonts",
        "note": "본문 읽기에 최적화된 세리프. 블로그, 매거진에 많이 사용.",
    },
    # ── Korean Serif ──
    {
        "name": "Noto Serif KR",
        "family": "serif-body",
        "personality": ["editorial", "classic", "readable"],
        "best_for": ["editorial", "publishing", "content"],
        "korean_pair": None,
        "korean_native": True,
        "korean_context": {
            "glyph_width": "넓음",
            "jaso_balance": "우수 — 전통 명조 기반 현대적 재해석",
            "small_size": "14px 이상 권장 (세리프 특성상)",
            "best_for_kr": ["에디토리얼 헤딩", "콘텐츠 플랫폼", "매거진", "장문 읽기"],
            "avoid_for_kr": ["UI 라벨 — 작은 크기에서 가독성 저하", "모바일 본문 — 화면이 좁으면 답답함"],
            "pair_with_latin": "Playfair Display (세리프 헤딩) 또는 Lora (세리프 본문)",
            "note_kr": "한글 세리프 웹폰트 중 사실상 유일한 고품질 선택지. 헤딩에서 격조 있는 인상. 본문에도 쓸 수 있지만 16px 이상 추천.",
        },
        "weight_range": "200-900",
        "variable": False,
        "source": "Google Fonts",
        "note": "한글 세리프의 사실상 유일한 고품질 웹폰트. 에디토리얼 한글에 필수.",
    },
    {
        "name": "KoPubWorldBatang",
        "family": "serif-body",
        "personality": ["classic", "institutional", "readable"],
        "best_for": ["publishing", "government", "documentation"],
        "korean_pair": None,
        "korean_native": True,
        "korean_context": {
            "glyph_width": "넓음",
            "jaso_balance": "전통적 — 인쇄용 바탕체에 가까움",
            "small_size": "14px 이상 권장",
            "best_for_kr": ["출판물", "공공 문서", "법률/계약서", "전통적 인상이 필요한 서비스"],
            "avoid_for_kr": ["모던 UI — 너무 전통적", "모바일 — 글자폭이 넓어 공간 부족"],
            "pair_with_latin": "Libre Baskerville",
            "note_kr": "한국 출판 표준 바탕체. 웹보다는 PDF/인쇄 맥락에 더 적합. 웹에서는 Noto Serif KR이 더 안정적.",
        },
        "weight_range": "300-700",
        "variable": False,
        "source": "한국출판인회의",
        "note": "한국 출판 표준 바탕체. 인쇄물 디자인에서 많이 사용.",
    },
    # ── Monospace ──
    {
        "name": "JetBrains Mono",
        "family": "monospace",
        "personality": ["precise", "technical", "developer"],
        "best_for": ["developer-tool", "code", "data-heavy"],
        "korean_pair": "Pretendard",
        "weight_range": "100-800",
        "variable": True,
        "source": "Google Fonts",
        "note": "개발자 도구의 사실상 표준 모노스페이스. 리거처 지원.",
    },
    {
        "name": "Fira Code",
        "family": "monospace",
        "personality": ["friendly", "technical", "readable"],
        "best_for": ["developer-tool", "code"],
        "korean_pair": "Pretendard",
        "weight_range": "300-700",
        "variable": True,
        "source": "Google Fonts",
        "note": "리거처가 특징. 코드 에디터에서 인기.",
    },
    {
        "name": "IBM Plex Mono",
        "family": "monospace",
        "personality": ["trustworthy", "institutional", "precise"],
        "best_for": ["enterprise", "developer-tool", "data-heavy", "fintech"],
        "korean_pair": "IBM Plex Sans KR",
        "weight_range": "100-700",
        "variable": False,
        "source": "Google Fonts",
        "note": "IBM Plex 패밀리와 일관된 디자인. Sans/Serif/Mono 통일 시 최적.",
    },
    {
        "name": "Source Code Pro",
        "family": "monospace",
        "personality": ["neutral", "readable", "professional"],
        "best_for": ["developer-tool", "code", "documentation"],
        "korean_pair": "Noto Sans KR",
        "weight_range": "200-900",
        "variable": True,
        "source": "Google Fonts",
        "note": "Source Sans와 짝을 이루는 모노스페이스. 범용적.",
    },
    # ── Rounded / Friendly ──
    {
        "name": "Nunito",
        "family": "rounded-sans",
        "personality": ["friendly", "playful", "warm"],
        "best_for": ["consumer", "education", "health", "kids"],
        "korean_pair": "SUIT",
        "weight_range": "200-900",
        "variable": True,
        "source": "Google Fonts",
        "note": "둥근 터미널의 친근한 산세리프. 교육/헬스케어 서비스에 적합.",
    },
    {
        "name": "Quicksand",
        "family": "rounded-sans",
        "personality": ["playful", "light", "modern"],
        "best_for": ["consumer", "lifestyle", "mobile"],
        "korean_pair": "SUIT",
        "weight_range": "300-700",
        "variable": True,
        "source": "Google Fonts",
        "note": "기하학적이면서 둥근 서체. 가벼운 톤의 서비스에 적합.",
    },
]


# ──────────────────────────────────────────────
# 1-b. Korean typography implementation profiles
# ──────────────────────────────────────────────

KOREAN_TYPOGRAPHY_PROFILES: dict[str, dict[str, str]] = {
    "Pretendard": {
        "heading_line_height": "1.25-1.35",
        "body_line_height": "1.6-1.7",
        "ui_label_line_height": "1.4-1.5",
        "heading_tracking": "0em",
        "body_tracking": "0em",
        "display_scale_bias": "stable",
        "note": "기본 자간/행간이 안정적이라 추가 보정 없이 바로 쓰기 좋다.",
    },
    "Wanted Sans": {
        "heading_line_height": "1.2-1.3",
        "body_line_height": "1.5-1.6",
        "ui_label_line_height": "1.4-1.5",
        "heading_tracking": "-0.01em",
        "body_tracking": "0em",
        "display_scale_bias": "stable",
        "note": "현대적 헤딩에는 강하지만 장문 본문은 Pretendard보다 여유를 덜 준다.",
    },
    "Noto Sans KR": {
        "heading_line_height": "1.25-1.4",
        "body_line_height": "1.6-1.8",
        "ui_label_line_height": "1.45-1.55",
        "heading_tracking": "-0.01em",
        "body_tracking": "-0.01em",
        "display_scale_bias": "reduce-one-step",
        "note": "글자폭이 넓어 밀집 UI에서는 더 넓은 inline space와 보수적인 display scale이 필요하다.",
    },
    "SUIT": {
        "heading_line_height": "1.25-1.35",
        "body_line_height": "1.6-1.7",
        "ui_label_line_height": "1.4-1.5",
        "heading_tracking": "0em",
        "body_tracking": "0em",
        "display_scale_bias": "stable",
        "note": "Pretendard 계열의 안정성을 유지하면서 더 부드러운 톤을 낸다.",
    },
    "Spoqa Han Sans Neo": {
        "heading_line_height": "1.2-1.3",
        "body_line_height": "1.5-1.6",
        "ui_label_line_height": "1.4-1.5",
        "heading_tracking": "-0.02em",
        "body_tracking": "0em",
        "display_scale_bias": "stable",
        "note": "조밀한 UI에서는 tracking 보정이 유효하지만 장문 본문용으로는 여유가 적다.",
    },
    "IBM Plex Sans KR": {
        "heading_line_height": "1.2-1.3",
        "body_line_height": "1.5-1.6",
        "ui_label_line_height": "1.4-1.5",
        "heading_tracking": "0em",
        "body_tracking": "0em",
        "display_scale_bias": "stable",
        "note": "기업형 제품에서 안정적이며 과한 tracking 보정보다 정확한 weight 운용이 중요하다.",
    },
    "Noto Serif KR": {
        "heading_line_height": "1.2-1.4",
        "body_line_height": "1.7-1.9",
        "ui_label_line_height": "avoid-small-serif-ui",
        "heading_tracking": "-0.02em",
        "body_tracking": "0em",
        "display_scale_bias": "reduce-one-step",
        "note": "넓은 획과 글자폭 때문에 헤딩은 짧고 크게, 본문은 충분한 행간과 여백이 필요하다.",
    },
    "KoPubWorldBatang": {
        "heading_line_height": "1.25-1.45",
        "body_line_height": "1.8-2.0",
        "ui_label_line_height": "avoid-small-serif-ui",
        "heading_tracking": "0em",
        "body_tracking": "0em",
        "display_scale_bias": "reduce-one-step",
        "note": "전통적 바탕체라 웹 UI보다 문서형 레이아웃에서 더 넓은 measure와 행간이 필요하다.",
    },
}


# ──────────────────────────────────────────────
# 2. 브랜드 키워드 → 서체 성격 매핑
# ──────────────────────────────────────────────

KEYWORD_FONT_SIGNALS: dict[str, dict] = {
    "calm": {
        "prefer_personality": ["readable", "neutral", "warm"],
        "prefer_family": ["humanist-sans", "serif-body"],
        "avoid_family": ["rounded-sans"],
        "line_height": "relaxed",
        "letter_spacing": "normal",
        "note": "읽기 편하고 조용한 서체. 과한 기하학적 형태 지양.",
    },
    "precise": {
        "prefer_personality": ["precise", "clean", "geometric"],
        "prefer_family": ["geometric-sans", "monospace"],
        "avoid_family": ["rounded-sans", "serif-display"],
        "line_height": "normal",
        "letter_spacing": "tight",
        "note": "정돈된 기하학적 산세리프. 숫자와 데이터 표현에 강한 서체.",
    },
    "editorial": {
        "prefer_personality": ["editorial", "elegant", "classic"],
        "prefer_family": ["serif-display"],
        "body_prefer_family": ["humanist-sans"],
        "avoid_family": ["rounded-sans"],
        "line_height": "relaxed",
        "letter_spacing": "normal",
        "heading_style": "serif",
        "note": "헤드라인에 세리프, 본문에 산세리프의 대비 구조.",
    },
    "trustworthy": {
        "prefer_personality": ["trustworthy", "institutional", "readable"],
        "prefer_family": ["humanist-sans"],
        "avoid_family": ["rounded-sans", "serif-display"],
        "line_height": "comfortable",
        "letter_spacing": "normal",
        "note": "검증된 서체. IBM Plex, Source Sans 같은 기관형 서체.",
    },
    "bold": {
        "prefer_personality": ["bold", "confident", "contemporary"],
        "prefer_family": ["geometric-sans"],
        "avoid_family": ["serif-body"],
        "line_height": "tight",
        "letter_spacing": "tight",
        "note": "두꺼운 weight에서 임팩트 있는 서체. 헤드라인 중심.",
    },
    "minimal": {
        "prefer_personality": ["neutral", "clean", "modern"],
        "prefer_family": ["geometric-sans"],
        "avoid_family": ["serif-display", "rounded-sans"],
        "line_height": "normal",
        "letter_spacing": "tight",
        "note": "군더더기 없는 중립적 서체. Inter, DM Sans 계열.",
    },
    "luxury": {
        "prefer_personality": ["luxury", "elegant", "delicate"],
        "prefer_family": ["serif-display"],
        "avoid_family": ["rounded-sans", "monospace"],
        "line_height": "relaxed",
        "letter_spacing": "wide",
        "heading_style": "serif",
        "note": "얇은 세리프로 우아함 표현. Cormorant, EB Garamond.",
    },
    "friendly": {
        "prefer_personality": ["friendly", "warm", "readable"],
        "prefer_family": ["rounded-sans", "humanist-sans"],
        "avoid_family": ["serif-display"],
        "line_height": "comfortable",
        "letter_spacing": "normal",
        "note": "둥근 터미널, 따뜻한 인상의 서체. Nunito, Outfit.",
    },
    "warm": {
        "prefer_personality": ["warm", "readable", "friendly"],
        "prefer_family": ["humanist-sans", "serif-body"],
        "avoid_family": [],
        "line_height": "relaxed",
        "letter_spacing": "normal",
        "note": "따뜻한 톤. 세리프 본문 또는 부드러운 산세리프.",
    },
    "playful": {
        "prefer_personality": ["playful", "friendly", "light"],
        "prefer_family": ["rounded-sans"],
        "avoid_family": ["serif-display", "monospace"],
        "line_height": "comfortable",
        "letter_spacing": "normal",
        "note": "둥글고 경쾌한 서체. Quicksand, Nunito.",
    },
}


# ──────────────────────────────────────────────
# 3. 제품 유형 → 서체 전략 매핑
# ──────────────────────────────────────────────

PRODUCT_TYPE_SIGNALS: dict[str, dict] = {
    "saas": {
        "body": ["geometric-sans", "humanist-sans"],
        "heading": ["geometric-sans"],
        "mono_needed": True,
        "note": "SaaS는 범용 산세리프 기본. 데이터가 많으면 숫자가 좋은 서체 선호.",
    },
    "dashboard": {
        "body": ["geometric-sans"],
        "heading": ["geometric-sans"],
        "mono_needed": True,
        "note": "대시보드는 숫자 가독성이 핵심. Space Grotesk, Inter tabular figures.",
    },
    "editorial": {
        "body": ["humanist-sans"],
        "heading": ["serif-display"],
        "mono_needed": False,
        "note": "에디토리얼은 세리프 헤딩 + 산세리프 본문 대비가 정석.",
    },
    "content": {
        "body": ["humanist-sans", "serif-body"],
        "heading": ["serif-display", "humanist-sans"],
        "mono_needed": False,
        "note": "콘텐츠 중심 서비스. 장문 가독성 우선.",
    },
    "mobile": {
        "body": ["humanist-sans", "geometric-sans"],
        "heading": ["geometric-sans", "humanist-sans"],
        "mono_needed": False,
        "note": "모바일은 작은 크기 가독성이 핵심. Pretendard, Inter 기본.",
    },
    "developer-tool": {
        "body": ["geometric-sans"],
        "heading": ["geometric-sans"],
        "mono_needed": True,
        "note": "개발자 도구는 모노스페이스가 핵심. JetBrains Mono 표준.",
    },
    "enterprise": {
        "body": ["humanist-sans"],
        "heading": ["humanist-sans"],
        "mono_needed": True,
        "note": "기업용은 검증된 서체. IBM Plex, Source Sans 계열.",
    },
    "consumer": {
        "body": ["geometric-sans", "rounded-sans"],
        "heading": ["geometric-sans", "rounded-sans"],
        "mono_needed": False,
        "note": "소비자 앱은 친근하고 현대적인 산세리프.",
    },
    "fintech": {
        "body": ["geometric-sans", "humanist-sans"],
        "heading": ["geometric-sans"],
        "mono_needed": True,
        "note": "핀테크는 숫자 디자인이 핵심. tabular figures 필수.",
    },
    "fashion": {
        "body": ["humanist-sans"],
        "heading": ["serif-display"],
        "mono_needed": False,
        "note": "패션은 세리프 디스플레이가 정석. 얇은 weight 활용.",
    },
    "luxury": {
        "body": ["humanist-sans"],
        "heading": ["serif-display"],
        "mono_needed": False,
        "note": "럭셔리는 세리프 + 넉넉한 여백. letter-spacing 넓게.",
    },
    "education": {
        "body": ["humanist-sans", "rounded-sans"],
        "heading": ["humanist-sans", "rounded-sans"],
        "mono_needed": False,
        "note": "교육은 가독성과 친근함 중심.",
    },
}


# ──────────────────────────────────────────────
# 4. Type Scale 프리셋
# ──────────────────────────────────────────────

TYPE_SCALES: dict[str, dict] = {
    "compact": {
        "base": 14,
        "scale_ratio": 1.2,
        "sizes": {"xs": 11, "sm": 12, "md": 14, "lg": 17, "xl": 20, "2xl": 24, "3xl": 29},
        "line_heights": {"tight": 1.25, "normal": 1.4, "comfortable": 1.5, "relaxed": 1.6},
        "best_for": ["dashboard", "data-heavy", "mobile"],
    },
    "default": {
        "base": 15,
        "scale_ratio": 1.25,
        "sizes": {"xs": 12, "sm": 13, "md": 15, "lg": 19, "xl": 24, "2xl": 30, "3xl": 37},
        "line_heights": {"tight": 1.25, "normal": 1.45, "comfortable": 1.55, "relaxed": 1.65},
        "best_for": ["saas", "enterprise", "consumer"],
    },
    "editorial": {
        "base": 16,
        "scale_ratio": 1.333,
        "sizes": {"xs": 12, "sm": 14, "md": 16, "lg": 21, "xl": 28, "2xl": 38, "3xl": 50},
        "line_heights": {"tight": 1.2, "normal": 1.5, "comfortable": 1.6, "relaxed": 1.75},
        "best_for": ["editorial", "content", "blog", "publishing"],
    },
    "display": {
        "base": 16,
        "scale_ratio": 1.414,
        "sizes": {"xs": 12, "sm": 14, "md": 16, "lg": 23, "xl": 32, "2xl": 45, "3xl": 64},
        "line_heights": {"tight": 1.1, "normal": 1.4, "comfortable": 1.5, "relaxed": 1.6},
        "best_for": ["fashion", "luxury", "branding", "landing"],
    },
}


# ──────────────────────────────────────────────
# 5. Font Pairing Rules
# ──────────────────────────────────────────────

PROVEN_PAIRINGS: list[dict] = [
    {"heading": "Playfair Display", "body": "Inter", "context": "editorial, content", "vibe": "classic + modern"},
    {"heading": "Playfair Display", "body": "Pretendard", "context": "editorial (KR)", "vibe": "고전 + 현대 한글"},
    {"heading": "DM Serif Display", "body": "DM Sans", "context": "warm editorial", "vibe": "같은 DM 패밀리 조화"},
    {"heading": "Libre Baskerville", "body": "Source Sans 3", "context": "trustworthy editorial", "vibe": "기관형 + 클래식"},
    {"heading": "EB Garamond", "body": "IBM Plex Sans", "context": "luxury + institutional", "vibe": "우아함 + 신뢰"},
    {"heading": "Cormorant Garamond", "body": "Pretendard", "context": "luxury (KR)", "vibe": "럭셔리 헤딩 + 깔끔 한글"},
    {"heading": "Plus Jakarta Sans", "body": "Inter", "context": "bold saas", "vibe": "임팩트 헤딩 + 중립 본문"},
    {"heading": "Space Grotesk", "body": "Inter", "context": "data dashboard", "vibe": "숫자 + 범용"},
    {"heading": "Outfit", "body": "Pretendard", "context": "modern mobile (KR)", "vibe": "현대적 + 깔끔 한글"},
    {"heading": "Noto Serif KR", "body": "Pretendard", "context": "editorial (KR native)", "vibe": "한글 세리프 + 한글 산세리프"},
    {"heading": "IBM Plex Sans", "body": "IBM Plex Sans", "context": "enterprise unified", "vibe": "같은 패밀리 통일"},
    {"heading": "Lora", "body": "Noto Sans KR", "context": "warm content (KR)", "vibe": "따뜻한 세리프 + 범용 한글"},
]


# ──────────────────────────────────────────────
# 6. Decision Engine
# ──────────────────────────────────────────────

def resolve_font_system(brand_profile: dict) -> dict:
    explicit_system = brand_profile.get("font_system")
    explicit_system = explicit_system if isinstance(explicit_system, dict) else {}
    brand_keywords = [kw.lower() for kw in brand_profile.get("brand_keywords", [])]
    anti_keywords = [kw.lower() for kw in brand_profile.get("anti_keywords", [])]
    platforms = [p.lower() for p in brand_profile.get("platforms", ["web"])]
    product_summary = brand_profile.get("product_summary", "").lower()
    visual_keywords = [kw.lower() for kw in brand_profile.get("visual_keywords", [])]

    product_type = _infer_product_type(product_summary, brand_keywords, visual_keywords)
    needs_korean = _needs_korean(brand_profile)
    needs_mono = _needs_mono(product_type, brand_profile)

    heading_scores = _score_fonts(brand_keywords, anti_keywords, product_type, "heading", needs_korean)
    body_scores = _score_fonts(brand_keywords, anti_keywords, product_type, "body", needs_korean)
    mono_scores = _score_fonts(brand_keywords, anti_keywords, product_type, "mono", needs_korean) if needs_mono else {}

    heading_font = _pick_best(heading_scores)
    body_font = _pick_best(body_scores, exclude=heading_font if _should_contrast(brand_keywords) else None)
    mono_font = _pick_best(mono_scores) if needs_mono else None

    pairing = _find_proven_pairing(heading_font, body_font, needs_korean)
    if pairing:
        heading_font = _get_font(pairing["heading"]) or heading_font
        body_font = _get_font(pairing["body"]) or body_font

    explicit_heading = _explicit_font(explicit_system, "heading")
    explicit_body = _explicit_font(explicit_system, "body")
    explicit_mono = _explicit_font(explicit_system, "mono")
    explicit_korean = _explicit_font(explicit_system, "korean")
    explicit_any = any([explicit_heading, explicit_body, explicit_mono, explicit_korean])
    if explicit_heading:
        heading_font = explicit_heading
    if explicit_body:
        body_font = explicit_body
    if explicit_mono:
        mono_font = explicit_mono

    korean_font = _pick_korean_font(
        body_font,
        heading_font,
        needs_korean,
        product_type=product_type,
        brand_keywords=brand_keywords,
    )
    if explicit_korean:
        korean_font = explicit_korean
    type_scale = _pick_type_scale(product_type, brand_keywords)
    line_height = _pick_line_height(brand_keywords)

    # 한글 서체 선택 이유 기록
    korean_rationale = None
    if needs_korean and body_font:
        if body_font.get("korean_native"):
            kr_ctx = body_font.get("korean_context", {})
            korean_rationale = {
                "primary_is_korean": True,
                "font": body_font["name"],
                "reason": kr_ctx.get("note_kr", "한글 네이티브 서체"),
                "glyph_width": kr_ctx.get("glyph_width"),
                "small_size_limit": kr_ctx.get("small_size"),
                "best_for_kr": kr_ctx.get("best_for_kr", []),
                "avoid_for_kr": kr_ctx.get("avoid_for_kr", []),
                "latin_pair": kr_ctx.get("pair_with_latin"),
            }
        elif korean_font:
            kr_ctx = korean_font.get("korean_context", {})
            korean_rationale = {
                "primary_is_korean": False,
                "font": korean_font["name"],
                "reason": kr_ctx.get("note_kr", "한글 페어링 서체") if kr_ctx else "기본 한글 페어링",
                "latin_pair": body_font["name"],
            }

    # ── Pitfall guardrails ──
    pitfall_warnings: list[str] = []

    # #14 Variable font 비표준 weight: 표준 100단위가 아닌 weight 경고
    for role_font, role_name in [(heading_font, "heading"), (body_font, "body"), (mono_font, "mono")]:
        if role_font:
            warnings = _check_nonstandard_weights(role_font)
            for w in warnings:
                pitfall_warnings.append(f"[pitfall#14] {role_name}: {w}")

    # #9 next/font fallback: fallback 폰트명이 선택되지 않도록 확인
    for role_font, role_name in [(heading_font, "heading"), (body_font, "body")]:
        if role_font and _is_nextfont_fallback(role_font["name"]):
            pitfall_warnings.append(
                f"[pitfall#9] {role_name}: '{role_font['name']}' appears to be a next/font metric fallback, not a real font."
            )

    # #13 Letter-spacing optical compensation: heading에 negative tracking 권장
    letter_spacing_note = _heading_tracking_recommendation(type_scale, brand_keywords)

    result = {
        "heading": _font_summary(heading_font),
        "body": _font_summary(body_font),
        "korean": _font_summary(korean_font) if korean_font else None,
        "korean_rationale": korean_rationale,
        "mono": _font_summary(mono_font) if mono_font else None,
        "type_scale": type_scale,
        "line_height_preset": line_height,
        "product_type_detected": product_type,
        "needs_korean": needs_korean,
        "pairing_source": "manual font_system" if explicit_any else pairing.get("context") if pairing else "auto-scored",
        "strategy": _build_strategy_notes(heading_font, body_font, mono_font, korean_font, brand_keywords, product_type),
        "loading": _build_loading_strategy(heading_font, body_font, mono_font, korean_font, platforms),
        "pitfall_warnings": pitfall_warnings,
        "letter_spacing": letter_spacing_note,
        "script_guardrails": _build_script_guardrails(
            heading=heading_font,
            body=body_font,
            korean=korean_font,
            brand_keywords=brand_keywords,
            product_type=product_type,
            needs_korean=needs_korean,
        ),
    }
    return result


def _explicit_font(font_system: dict, role: str) -> dict | None:
    entry = font_system.get(role)
    if not entry:
        return None
    if isinstance(entry, str):
        name = entry
        weights = None
        note = ""
    elif isinstance(entry, dict):
        name = entry.get("name") or entry.get("font") or entry.get("family_name")
        weights = entry.get("weights")
        note = entry.get("notes") or entry.get("note") or ""
    else:
        return None
    if not isinstance(name, str) or not name.strip():
        return None

    base = _get_font(name.strip())
    if base:
        font = dict(base)
    else:
        font = _custom_font(name.strip(), role)
    if weights:
        font["weight_range"] = _format_weight_range(weights)
    if note:
        font["note"] = note
    return font


def _custom_font(name: str, role: str) -> dict:
    if role == "mono":
        family = "monospace"
        personality = ["precise", "technical"]
    elif role == "korean":
        family = "humanist-sans"
        personality = ["readable", "professional"]
    else:
        family = "geometric-sans" if role == "heading" else "humanist-sans"
        personality = ["custom", "professional"]
    return {
        "name": name,
        "family": family,
        "personality": personality,
        "best_for": [],
        "weight_range": "400-700",
        "variable": False,
        "source": "brand_profile.font_system",
        "note": "Explicitly configured in brand_profile.font_system.",
    }


def _format_weight_range(weights: object) -> str:
    if isinstance(weights, list) and weights:
        values = [str(weight) for weight in weights]
        return "-".join([values[0], values[-1]]) if len(values) > 1 else values[0]
    if isinstance(weights, str):
        return weights
    return "400-700"


def _infer_product_type(summary: str, keywords: list[str], visual_kw: list[str]) -> str:
    type_signals = {
        "editorial": [
            "에디토리얼",
            "콘텐츠",
            "글쓰기",
            "발행",
            "매거진",
            "비평",
            "리뷰",
            "editorial",
            "content",
            "writing",
            "publishing",
            "review",
            "critique",
        ],
        "dashboard": ["대시보드", "통계", "분석", "모니터링", "dashboard", "analytics", "monitoring"],
        "saas": ["saas", "팀", "협업", "프로젝트", "관리", "team", "collaboration", "management"],
        "mobile": ["모바일", "앱", "mobile", "ios", "android"],
        "developer-tool": ["개발자", "코드", "api", "cli", "developer", "sdk"],
        "enterprise": ["기업", "b2b", "enterprise", "조직"],
        "fintech": ["금융", "결제", "은행", "투자", "fintech", "payment", "banking"],
        "fashion": ["패션", "의류", "스타일", "fashion", "clothing", "outfit"],
        "luxury": ["럭셔리", "프리미엄", "하이엔드", "luxury", "premium"],
        "consumer": ["소비자", "쇼핑", "consumer", "shopping"],
        "education": ["교육", "학습", "education", "learning"],
        "content": ["블로그", "뉴스", "미디어", "매체", "blog", "news", "media", "publisher"],
    }

    all_text = summary + " " + " ".join(keywords) + " " + " ".join(visual_kw)

    scores: dict[str, int] = {}
    for ptype, signals in type_signals.items():
        score = sum(1 for s in signals if s in all_text)
        if score > 0:
            scores[ptype] = score

    if "editorial" in keywords:
        scores["editorial"] = scores.get("editorial", 0) + 3

    if not scores:
        return "saas"
    return max(scores, key=scores.get)


def _needs_korean(profile: dict) -> bool:
    text = (
        profile.get("product_summary", "")
        + " ".join(profile.get("audiences", []))
        + " ".join(profile.get("tone_of_voice", []))
    )
    korean_chars = sum(1 for ch in text if "\uac00" <= ch <= "\ud7a3")
    return korean_chars > 3


def _needs_mono(product_type: str, profile: dict) -> bool:
    product_config = PRODUCT_TYPE_SIGNALS.get(product_type, {})
    if product_config.get("mono_needed"):
        return True
    primitives = " ".join(profile.get("product_primitives", [])).lower()
    return any(kw in primitives for kw in ["code", "editor", "command", "terminal", "데이터", "data table"])


def _score_fonts(
    brand_keywords: list[str],
    anti_keywords: list[str],
    product_type: str,
    role: str,
    needs_korean: bool = False,
) -> dict[str, float]:
    scores: dict[str, float] = {}
    product_config = PRODUCT_TYPE_SIGNALS.get(product_type, {})

    if role == "mono":
        target_families = {"monospace"}
    elif role == "heading":
        target_families = set(product_config.get("heading", ["geometric-sans"]))
    else:
        target_families = set(product_config.get("body", ["humanist-sans"]))

    for font in FONT_DB:
        score = 0.0
        family = font["family"]

        if role == "mono" and family != "monospace":
            continue
        if role != "mono" and family == "monospace":
            continue

        editorial_heading_context = role == "heading" and product_type in {"editorial", "content", "fashion", "luxury"}
        serif_heading = role == "heading" and "serif" in family

        # 한국어 제품이면 한글 네이티브 서체를 우선하되, 에디토리얼 헤딩은 세리프 방향을 살린다.
        if needs_korean:
            if font.get("korean_native"):
                if role == "body":
                    score += 5.0
                elif editorial_heading_context and serif_heading:
                    score += 4.5
                elif role == "heading":
                    score += 1.75
                else:
                    score += 3.0
                kr_ctx = font.get("korean_context", {})
                # 제품 유형이 한글 best_for에 포함되면 추가 가산
                kr_best = [x.lower() for x in kr_ctx.get("best_for_kr", [])]
                if any(product_type in item for item in kr_best):
                    score += 2.0
                # avoid_for에 해당하면 감점
                kr_avoid = [x.lower() for x in kr_ctx.get("avoid_for_kr", [])]
                if any(product_type in item for item in kr_avoid):
                    score -= 3.0
            else:
                # 한국어 제품인데 영어 전용 서체면 감점. 단, 에디토리얼 헤딩용 세리프는 한글 pair가 있을 수 있어 감점을 완화한다.
                score -= 0.5 if editorial_heading_context and serif_heading else 2.0

        if family in target_families:
            score += 3.0

        for kw in brand_keywords:
            signals = KEYWORD_FONT_SIGNALS.get(kw, {})
            for pref in signals.get("prefer_personality", []):
                if pref in font["personality"]:
                    score += 2.0
            prefer_key = "body_prefer_family" if role == "body" and "body_prefer_family" in signals else "prefer_family"
            for pref_fam in signals.get(prefer_key, []):
                if pref_fam == family:
                    score += 1.5
            for avoid_fam in signals.get("avoid_family", []):
                if avoid_fam == family:
                    score -= 3.0
            if signals.get("heading_style") == "serif" and role == "heading" and "serif" in family:
                score += 2.0
            if signals.get("heading_style") == "serif" and role == "body" and "serif" in family:
                score -= 2.0

        for akw in anti_keywords:
            signals = KEYWORD_FONT_SIGNALS.get(akw, {})
            for pref in signals.get("prefer_personality", []):
                if pref in font["personality"]:
                    score -= 1.5

        if product_type in font.get("best_for", []):
            score += 2.0

        if font.get("variable"):
            score += 0.5

        scores[font["name"]] = score

    return scores


def _pick_best(scores: dict[str, float], exclude: dict | None = None) -> dict | None:
    if not scores:
        return None
    exclude_name = exclude["name"] if exclude else None
    sorted_fonts = sorted(scores.items(), key=lambda x: x[1], reverse=True)
    for name, score in sorted_fonts:
        if name != exclude_name:
            return _get_font(name)
    return _get_font(sorted_fonts[0][0]) if sorted_fonts else None


def _should_contrast(brand_keywords: list[str]) -> bool:
    return any(kw in brand_keywords for kw in ["editorial", "luxury", "fashion"])


def _get_font(name: str) -> dict | None:
    for font in FONT_DB:
        if font["name"] == name:
            return font
    return None


def _find_proven_pairing(heading: dict | None, body: dict | None, needs_korean: bool) -> dict | None:
    if not heading or not body:
        return None
    for pairing in PROVEN_PAIRINGS:
        h_match = pairing["heading"] == heading["name"]
        b_match = pairing["body"] == body["name"]
        if h_match and b_match:
            return pairing
        if h_match:
            candidate_body = _get_font(pairing["body"])
            if candidate_body:
                if needs_korean and "(KR)" in pairing.get("context", ""):
                    return pairing
                if not needs_korean:
                    return pairing
    return None


def _pick_korean_font(
    body: dict | None,
    heading: dict | None,
    needs_korean: bool,
    product_type: str,
    brand_keywords: list[str],
) -> dict | None:
    if not needs_korean:
        return None
    prefer_heading_pair = (
        heading
        and heading.get("korean_pair")
        and (
            "editorial" in brand_keywords
            or product_type in {"editorial", "content", "fashion", "luxury"}
            or "serif" in (heading or {}).get("family", "")
        )
    )
    if prefer_heading_pair:
        paired = _get_font(heading["korean_pair"])
        if paired:
            return paired
    if body and body.get("korean_native"):
        return body
    if body and body.get("korean_pair"):
        return _get_font(body["korean_pair"])
    if heading and heading.get("korean_pair"):
        return _get_font(heading["korean_pair"])
    return _get_font("Pretendard")


def _pick_type_scale(product_type: str, brand_keywords: list[str]) -> dict:
    if "editorial" in brand_keywords or product_type in ("editorial", "content", "publishing"):
        return TYPE_SCALES["editorial"]
    if product_type in ("fashion", "luxury"):
        return TYPE_SCALES["display"]
    if product_type in ("dashboard", "mobile"):
        return TYPE_SCALES["compact"]
    return TYPE_SCALES["default"]


def _pick_line_height(brand_keywords: list[str]) -> str:
    for kw in brand_keywords:
        signals = KEYWORD_FONT_SIGNALS.get(kw, {})
        lh = signals.get("line_height")
        if lh:
            return lh
    return "normal"


def _font_summary(font: dict | None) -> dict | None:
    if not font:
        return None
    return {
        "name": font["name"],
        "family": font["family"],
        "personality": font["personality"],
        "weight_range": font["weight_range"],
        "variable": font.get("variable", False),
        "source": font.get("source", ""),
        "note": font.get("note", ""),
    }


def _build_strategy_notes(
    heading: dict | None,
    body: dict | None,
    mono: dict | None,
    korean: dict | None,
    brand_keywords: list[str],
    product_type: str,
) -> list[str]:
    notes = []
    if heading and body and heading["name"] != body["name"]:
        h_fam = heading["family"]
        b_fam = body["family"]
        if "serif" in h_fam and "sans" in b_fam:
            notes.append("헤딩(세리프) + 본문(산세리프) 대비 구조 — 에디토리얼 정석")
        elif h_fam == b_fam:
            notes.append("같은 패밀리에서 weight 대비로 위계 형성")
        else:
            notes.append(f"헤딩({h_fam}) + 본문({b_fam}) 조합")
    elif heading and body:
        notes.append(f"단일 서체({heading['name']})로 weight 대비 위계 — 일관성 우선")

    if korean:
        notes.append(f"한글 서체: {korean['name']} — 라틴과 x-height/weight 조화")

    if mono:
        notes.append(f"모노스페이스: {mono['name']} — 코드/데이터 영역 전용")

    if "editorial" in brand_keywords:
        notes.append("editorial 키워드 → 넉넉한 line-height, 헤딩에 serif 사용")
    if "calm" in brand_keywords:
        notes.append("calm 키워드 → comfortable spacing, 과한 weight 대비 지양")
    if "precise" in brand_keywords:
        notes.append("precise 키워드 → tight letter-spacing, tabular figures 권장")

    return notes


def _build_loading_strategy(
    heading: dict | None,
    body: dict | None,
    mono: dict | None,
    korean: dict | None,
    platforms: list[str],
) -> dict:
    fonts_to_load = []
    if body:
        fonts_to_load.append({"font": body["name"], "weights": "400;500;600", "priority": "preload"})
    if heading and heading["name"] != (body or {}).get("name"):
        fonts_to_load.append({"font": heading["name"], "weights": "600;700", "priority": "preload"})
    if korean and korean["name"] != (body or {}).get("name"):
        fonts_to_load.append({"font": korean["name"], "weights": "400;500;600", "priority": "preload"})
    if mono:
        fonts_to_load.append({"font": mono["name"], "weights": "400;500", "priority": "lazy"})

    return {
        "fonts": fonts_to_load,
        "fallback_strategy": "system-ui → font swap",
        "display": "swap",
        "subset": "latin,korean" if korean else "latin",
        "note": "본문 서체를 preload, 모노스페이스는 lazy load. font-display: swap으로 FOUT 최소화.",
    }


def _build_script_guardrails(
    heading: dict | None,
    body: dict | None,
    korean: dict | None,
    brand_keywords: list[str],
    product_type: str,
    needs_korean: bool,
) -> dict | None:
    if not needs_korean:
        return None

    headline_font = _pick_korean_script_font(heading, korean, fallback=body)
    body_font = _pick_korean_script_font(body, korean, fallback=heading)
    headline_profile = _lookup_korean_typography_profile(headline_font)
    body_profile = _lookup_korean_typography_profile(body_font)

    headline_name = (headline_font or {}).get("name", "Korean heading font")
    body_name = (body_font or {}).get("name", "Korean body font")
    headline_ctx = (headline_font or {}).get("korean_context", {})
    body_ctx = (body_font or {}).get("korean_context", {})

    conservative_scale = headline_profile.get("display_scale_bias") == "reduce-one-step"
    editorial_headline = (
        "editorial" in brand_keywords
        or "luxury" in brand_keywords
        or "serif" in (headline_font or {}).get("family", "")
        or product_type in {"editorial", "content", "luxury", "fashion"}
    )
    if editorial_headline:
        conservative_scale = True

    rules = [
        "한글 카피는 `word-break: keep-all`과 `overflow-wrap: normal`을 기본값으로 두고, 주요 헤딩에서 지원되면 `text-wrap: balance`를 사용한다.",
        "한글 헤딩에는 breakpoint 검증 전 강제 `<br />`를 넣지 않는다. 줄바꿈이 필요하면 먼저 컨테이너 폭과 type scale을 조정한다.",
        "한글 화면은 영문 시안의 `ch` 기준이나 single-line slogan 가정에 맞추지 말고, 실제 한글 문장으로 wrap을 검증한다.",
    ]
    if conservative_scale:
        rules.append("폭이 넓은 한글 또는 명조 헤딩은 영문 hero보다 한 단계 작은 display scale에서 시작하고, 줄바꿈이 안정적일 때만 키운다.")
    if body_ctx.get("glyph_width") == "넓음":
        rules.append(f"{body_name}처럼 글자폭이 넓은 본문은 카드, 배지, 표 헤더에 더 넓은 inline space를 남긴다.")
    if headline_profile.get("ui_label_line_height") == "avoid-small-serif-ui":
        rules.append(f"{headline_name}는 작은 UI 라벨/배지용으로 쓰지 않고, 그런 슬롯은 sans body font로 분리한다.")

    warnings = []
    if headline_ctx.get("avoid_for_kr"):
        warnings.extend(headline_ctx.get("avoid_for_kr", [])[:2])
    if body_ctx.get("avoid_for_kr"):
        warnings.extend(body_ctx.get("avoid_for_kr", [])[:2])

    return {
        "primary_script": "korean",
        "headline_font": {
            "name": headline_name,
            "line_height": headline_profile.get("heading_line_height"),
            "letter_spacing": headline_profile.get("heading_tracking"),
            "note": headline_profile.get("note") or headline_ctx.get("note_kr"),
        },
        "body_font": {
            "name": body_name,
            "line_height": body_profile.get("body_line_height"),
            "ui_label_line_height": body_profile.get("ui_label_line_height"),
            "letter_spacing": body_profile.get("body_tracking"),
            "note": body_profile.get("note") or body_ctx.get("note_kr"),
        },
        "wrap": {
            "headline": {
                "word_break": "keep-all",
                "overflow_wrap": "normal",
                "text_wrap": "balance",
            },
            "body": {
                "word_break": "keep-all",
                "overflow_wrap": "normal",
            },
            "avoid": [
                "forced <br /> before breakpoint QA",
                "English-first ch heuristics without real Korean copy review",
            ],
        },
        "scale": {
            "headline_start": "one-step-smaller" if conservative_scale else "default-scale",
            "guidance": (
                "한글 hero/section heading은 영문 시안보다 한 단계 작은 스케일에서 시작해 wrap을 확인한 뒤 확장한다."
                if conservative_scale
                else "기본 스케일을 사용할 수 있지만 한글 문장 기준으로 실제 wrap을 먼저 검증한다."
            ),
        },
        "warnings": warnings,
        "rules": rules,
    }


def _pick_korean_script_font(
    preferred: dict | None,
    korean: dict | None,
    fallback: dict | None = None,
) -> dict | None:
    if preferred and preferred.get("korean_native"):
        return preferred
    if preferred and preferred.get("korean_pair"):
        paired = _get_font(preferred["korean_pair"])
        if paired and paired.get("korean_native"):
            return paired
    if korean and korean.get("korean_native"):
        return korean
    return preferred or korean or fallback


def _lookup_korean_typography_profile(font: dict | None) -> dict[str, str]:
    if not font:
        return {}
    profile = KOREAN_TYPOGRAPHY_PROFILES.get(font.get("name"), {})
    if profile:
        return profile
    family = font.get("family", "")
    if "serif" in family:
        return {
            "heading_line_height": "1.2-1.4",
            "body_line_height": "1.7-1.9",
            "ui_label_line_height": "avoid-small-serif-ui",
            "heading_tracking": "-0.02em",
            "body_tracking": "0em",
            "display_scale_bias": "reduce-one-step",
            "note": "한글 세리프는 넓은 획과 글자폭 때문에 더 보수적인 display scale과 넉넉한 행간이 필요하다.",
        }
    return {
        "heading_line_height": "1.2-1.35",
        "body_line_height": "1.55-1.7",
        "ui_label_line_height": "1.4-1.5",
        "heading_tracking": "0em",
        "body_tracking": "0em",
        "display_scale_bias": "stable",
        "note": "한글 산세리프 기본값을 따르되 실제 문자열 기준으로 wrap을 확인한다.",
    }


# ──────────────────────────────────────────────
# 8. Font Reference Markdown Parser
# ──────────────────────────────────────────────

def parse_font_reference_markdown(path: Path) -> dict:
    """Parse a font-reference.md file into structured data."""
    title = path.stem
    current_category: str | None = None
    current_font: dict | None = None
    fonts: list[dict] = []

    for raw_line in path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line:
            continue

        if line.startswith("# "):
            title = line[2:].strip()
            continue

        if line.startswith("## "):
            current_category = line[3:].strip()
            continue

        if line.startswith("### ") and not line.startswith("### 제품") and not line.startswith("### 브랜드") and not line.startswith("### 한글"):
            current_font = {
                "name": line[4:].strip(),
                "category": current_category,
                "classification": None,
                "maker": None,
                "source": None,
                "license": None,
                "weight_range": None,
                "latin_compatible": None,
                "glyph_width": None,
                "jaso_balance": None,
                "small_size": None,
                "line_height_recommend": None,
                "letter_spacing": None,
                "rendering": None,
                "used_by": [],
                "best_for": [],
                "avoid_for": [],
                "pairing": [],
                "selection_reason": None,
            }
            fonts.append(current_font)
            continue

        if not current_font or not line.startswith("- **"):
            continue

        try:
            label_part, value = line[2:].split("**:", 1)
        except ValueError:
            continue

        label = label_part.replace("**", "").strip()
        value = value.strip()

        field_map = {
            "분류": "classification",
            "제작": "maker",
            "소스": "source",
            "라이선스": "license",
            "웨이트": "weight_range",
            "라틴 호환": "latin_compatible",
            "글자폭": "glyph_width",
            "자소 균형": "jaso_balance",
            "소형 가독성": "small_size",
            "행간 권장": "line_height_recommend",
            "자간 특성": "letter_spacing",
            "렌더링 특성": "rendering",
            "선택 이유": "selection_reason",
        }

        if label in field_map:
            current_font[field_map[label]] = value
        elif label == "사용 서비스":
            current_font["used_by"] = [s.strip() for s in value.split(",")]
        elif label == "적합한 용도":
            current_font["best_for"] = [s.strip() for s in value.split(",")]
        elif label == "부적합한 용도":
            current_font["avoid_for"] = [s.strip() for s in value.split(",")]
        elif label == "페어링":
            current_font["pairing"] = [s.strip() for s in value.split(",")]

    return {
        "title": title,
        "source_path": str(path),
        "font_count": len(fonts),
        "categories": sorted({f["category"] for f in fonts if f.get("category")}),
        "fonts": fonts,
    }


# ──────────────────────────────────────────────
# 9. Pitfall Guardrails
# ──────────────────────────────────────────────

_STANDARD_WEIGHTS = {100, 200, 300, 400, 500, 600, 700, 800, 900}


def _parse_weight_range(weight_range: str) -> list[int]:
    """Parse weight_range string like '100-900' or '300/380/570' into int list."""
    if "-" in weight_range and "/" not in weight_range:
        parts = weight_range.split("-")
        try:
            lo, hi = int(parts[0].strip()), int(parts[-1].strip())
            return list(range(lo, hi + 1, 100))
        except ValueError:
            return []
    if "/" in weight_range:
        try:
            return [int(w.strip()) for w in weight_range.split("/")]
        except ValueError:
            return []
    try:
        return [int(weight_range.strip())]
    except ValueError:
        return []


def _check_nonstandard_weights(font: dict) -> list[str]:
    """Pitfall #14: warn if a font uses non-standard weight values.

    Saans uses 300/380/570, ShopifySans uses 330/420/550.
    These can't be reproduced with standard Inter-like weights.
    """
    weight_range = font.get("weight_range", "")
    weights = _parse_weight_range(weight_range)
    nonstandard = [w for w in weights if w not in _STANDARD_WEIGHTS]
    if nonstandard:
        return [
            f"'{font['name']}' has non-standard weights {nonstandard} "
            f"(from '{weight_range}'). Cannot reproduce with standard font weights."
        ]
    return []


def _is_nextfont_fallback(font_name: str) -> bool:
    """Pitfall #9: detect next/font metric fallback font names.

    Names like 'Inter Fallback', 'Mona Sans Header Fallback' are
    layout-shift prevention fonts injected by Next.js, not real choices.
    """
    lower = font_name.lower()
    return "fallback" in lower and any(
        kw in lower for kw in ["inter", "mona", "sans", "serif", "mono"]
    )


def _heading_tracking_recommendation(type_scale: dict, brand_keywords: list[str]) -> dict:
    """Pitfall #13: recommend negative letter-spacing for large headings.

    Large headings without negative tracking look 'loose'.
    Standard: -0.01em for md~xl, -0.02em for 2xl+.
    """
    sizes = type_scale.get("sizes", {})
    tracking: dict[str, str] = {}
    for size_key, size_px in sizes.items():
        if size_px >= 30:
            tracking[size_key] = "-0.02em"
        elif size_px >= 20:
            tracking[size_key] = "-0.01em"
    if "precise" in brand_keywords or "minimal" in brand_keywords:
        for key in tracking:
            if tracking[key] == "-0.01em":
                tracking[key] = "-0.015em"
    return {
        "heading_tracking": tracking,
        "note": "큰 헤딩에 negative tracking 적용. 미적용 시 글자가 풀어진 느낌.",
    }
