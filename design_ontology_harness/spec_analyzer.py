"""Analyze product specs to auto-detect UI primitives needed."""

from __future__ import annotations

import re
from pathlib import Path


UI_PATTERNS: dict[str, dict] = {
    "workspace navigation": {
        "terms": [
            "사이드바", "사이드 바", "네비게이션", "메뉴", "탐색", "워크스페이스",
            "앱 셸", "탑바", "탭바", "브레드크럼",
            "sidebar", "navigation", "nav bar", "topbar", "breadcrumb",
            "workspace", "app shell", "tab bar", "menu",
        ],
        "description": "앱의 주요 영역 간 이동을 위한 네비게이션 구조",
    },
    "rich text editor": {
        "terms": [
            "에디터", "편집기", "글쓰기", "작성기", "텍스트 편집", "마크다운",
            "위지윅", "리치텍스트", "본문 작성", "콘텐츠 작성", "글 작성",
            "editor", "rich text", "wysiwyg", "markdown", "writing",
            "compose", "draft", "authoring",
        ],
        "description": "서식이 있는 텍스트를 작성하고 편집하는 영역",
    },
    "command palette": {
        "terms": [
            "커맨드 팔레트", "명령 팔레트", "빠른 실행", "빠른 검색",
            "글로벌 검색", "통합 검색", "단축키", "커맨드",
            "command palette", "quick action", "spotlight", "omnibar",
            "global search", "shortcut",
        ],
        "description": "키보드로 빠르게 명령을 실행하거나 검색하는 오버레이",
    },
    "dashboard cards": {
        "terms": [
            "대시보드", "통계", "요약", "현황", "인사이트", "지표",
            "KPI", "메트릭", "카드형", "활동 피드",
            "dashboard", "stat card", "insight", "metric", "KPI",
            "activity feed", "overview", "summary card",
        ],
        "description": "주요 지표와 활동을 카드 형태로 보여주는 대시보드",
    },
    "data tables": {
        "terms": [
            "테이블", "표", "목록", "리스트", "데이터 목록", "정렬",
            "필터", "페이지네이션", "페이징", "그리드 뷰",
            "table", "data grid", "list view", "sortable", "filterable",
            "pagination", "column", "row",
        ],
        "description": "정렬·필터가 가능한 데이터 테이블 또는 목록",
    },
    "forms": {
        "terms": [
            "폼", "양식", "입력", "설정", "프로필 편집", "등록",
            "가입", "로그인", "회원가입", "입력 필드", "드롭다운",
            "체크박스", "라디오", "선택", "셀렉트",
            "form", "input", "text field", "dropdown", "checkbox",
            "radio", "select", "sign up", "login", "settings",
            "register", "configuration",
        ],
        "description": "사용자 입력을 받는 폼과 설정 화면",
    },
    "notifications": {
        "terms": [
            "알림", "알럿", "토스트", "배너", "공지", "안내",
            "에러 메시지", "성공 메시지", "경고", "빈 상태",
            "notification", "alert", "toast", "banner", "snackbar",
            "empty state", "error message", "success message",
        ],
        "description": "사용자에게 상태 변화나 결과를 알려주는 피드백 요소",
    },
    "file upload": {
        "terms": [
            "파일 업로드", "이미지 업로드", "첨부", "드래그앤드롭",
            "드롭존", "파일 선택", "미디어 업로드",
            "file upload", "drag and drop", "dropzone", "attachment",
            "media upload", "image upload",
        ],
        "description": "파일이나 이미지를 업로드하는 영역",
    },
    "calendar and dates": {
        "terms": [
            "캘린더", "달력", "날짜 선택", "일정", "스케줄", "타임라인",
            "date picker", "calendar", "schedule", "timeline",
            "date range", "time picker",
        ],
        "description": "날짜/시간을 선택하거나 일정을 표시하는 요소",
    },
    "charts and visualization": {
        "terms": [
            "차트", "그래프", "시각화", "파이 차트", "바 차트",
            "라인 차트", "도넛", "히트맵",
            "chart", "graph", "visualization", "pie chart", "bar chart",
            "line chart", "donut", "heatmap", "sparkline",
        ],
        "description": "데이터를 시각적으로 표현하는 차트/그래프",
    },
    "user profile and avatar": {
        "terms": [
            "프로필", "아바타", "사용자 정보", "계정", "마이페이지",
            "profile", "avatar", "user info", "account", "my page",
        ],
        "description": "사용자 프로필과 아바타를 표시하는 요소",
    },
    "comments and discussion": {
        "terms": [
            "댓글", "코멘트", "토론", "답글", "피드백", "리뷰",
            "comment", "discussion", "reply", "thread", "feedback",
            "review", "mention",
        ],
        "description": "댓글, 토론, 피드백을 주고받는 영역",
    },
    "tags and labels": {
        "terms": [
            "태그", "라벨", "뱃지", "칩", "카테고리", "분류",
            "tag", "label", "badge", "chip", "category", "status badge",
        ],
        "description": "상태나 분류를 표시하는 태그/뱃지",
    },
    "search and filter": {
        "terms": [
            "검색", "필터", "검색바", "검색 결과", "자동완성",
            "search", "filter", "search bar", "autocomplete",
            "search result", "faceted search",
        ],
        "description": "콘텐츠를 검색하고 필터링하는 요소",
    },
    "modal and dialog": {
        "terms": [
            "모달", "다이얼로그", "팝업", "확인 창", "바텀시트",
            "오버레이", "드로어",
            "modal", "dialog", "popup", "bottom sheet", "drawer",
            "overlay", "confirmation",
        ],
        "description": "사용자 확인이나 추가 입력을 받는 오버레이",
    },
    "onboarding and stepper": {
        "terms": [
            "온보딩", "튜토리얼", "가이드", "스텝", "단계", "위저드",
            "진행률", "프로그레스",
            "onboarding", "tutorial", "wizard", "stepper", "progress",
            "walkthrough", "getting started",
        ],
        "description": "단계별 안내나 온보딩 흐름",
    },
    "pricing and plans": {
        "terms": [
            "가격", "플랜", "요금", "구독", "결제", "과금",
            "pricing", "plan", "subscription", "billing", "payment",
            "checkout", "upgrade",
        ],
        "description": "가격 비교, 구독 플랜, 결제 관련 요소",
    },
    "kanban and board": {
        "terms": [
            "칸반", "보드", "드래그", "카드 이동", "컬럼",
            "kanban", "board", "drag", "card move", "column",
            "trello", "project board",
        ],
        "description": "칸반 보드 형태의 작업 관리 UI",
    },
    "chat and messaging": {
        "terms": [
            "채팅", "메시지", "대화", "챗", "DM", "인박스",
            "chat", "message", "conversation", "inbox", "direct message",
            "messenger",
        ],
        "description": "실시간 또는 비동기 메시지를 주고받는 UI",
    },
    "media player": {
        "terms": [
            "비디오", "동영상", "플레이어", "오디오", "재생",
            "video", "player", "audio", "playback", "streaming",
            "media player",
        ],
        "description": "비디오/오디오 재생 컨트롤",
    },
    "hero section": {
        "terms": [
            "히어로", "메인 비주얼", "랜딩 상단", "랜딩 헤더",
            "가치 제안", "첫 화면", "메인 헤드라인", "어보브 더 폴드",
            "hero", "hero section", "headline", "value proposition",
            "above the fold", "lead copy", "tagline",
        ],
        "description": "랜딩 페이지 최상단의 헤드라인과 핵심 메시지 영역",
    },
    "feature grid": {
        "terms": [
            "기능 소개", "특징", "주요 기능", "기능 카드", "장점",
            "혜택", "benefit", "feature section", "feature grid",
            "feature card", "key feature", "capability", "highlight grid",
        ],
        "description": "제품의 핵심 기능과 혜택을 카드나 컬럼으로 소개하는 섹션",
    },
    "social proof": {
        "terms": [
            "고객사", "사용 기업", "파트너 로고", "로고 클라우드",
            "신뢰", "사용자 수", "지표", "metric highlight",
            "logo cloud", "trusted by", "social proof", "customer logo",
            "partner", "press mention",
        ],
        "description": "고객 로고·지표·언론 인용으로 신뢰를 구축하는 섹션",
    },
    "testimonial": {
        "terms": [
            "고객 후기", "사용자 후기", "고객 추천사", "추천사", "인용구",
            "testimonial", "customer quote", "customer testimonial",
            "customer story", "case study", "endorsement",
        ],
        "description": "고객 추천사와 사용자 인용을 보여주는 마케팅 섹션",
    },
    "faq accordion": {
        "terms": [
            "자주 묻는 질문", "질문과 답변", "FAQ", "궁금한 점",
            "아코디언",
            "faq", "frequently asked", "q and a", "question and answer",
            "accordion",
        ],
        "description": "자주 묻는 질문을 접고 펼치는 아코디언 섹션",
    },
    "landing cta section": {
        "terms": [
            "시작하기", "무료로 시작", "지금 시작", "가입 유도", "전환 섹션",
            "CTA 섹션", "행동 유도",
            "get started", "start free", "sign up banner", "cta section",
            "conversion section", "call to action",
        ],
        "description": "랜딩 페이지 하단에서 가입/전환을 유도하는 CTA 섹션",
    },
    "site footer": {
        "terms": [
            "푸터", "사이트 하단", "하단 링크", "저작권", "사이트맵",
            "법적 고지",
            "footer", "site footer", "copyright", "sitemap", "legal links",
            "bottom navigation",
        ],
        "description": "사이트 전역 하단의 링크·법적 고지·소셜 영역",
    },
    "site header": {
        "terms": [
            "사이트 헤더", "랜딩 네비", "마케팅 헤더", "상단 메뉴",
            "site header", "marketing nav", "landing nav", "top navigation",
            "nav menu", "hamburger menu",
        ],
        "description": "랜딩/마케팅 페이지 상단의 고정 헤더와 내비게이션",
    },
    "reference documentation": {
        "terms": [
            "레퍼런스 문서", "기술 문서", "개발자 문서",
            "reference documentation", "technical documentation",
            "developer documentation", "api docs", "api-docs",
            "table of contents", "toc sidebar",
            "heading anchor", "anchor link", "heading-anchor",
            "article body", "article-body",
            "prose block", "prose-block",
            "reading pane", "reading-pane", "reading measure",
            "footnote", "각주",
            "prev/next pager", "prev-next pager", "prev-next-pager",
            "link card", "link-card",
        ],
        "description": "레퍼런스·기술 문서용 article body · TOC · heading anchor · footnote 구조",
    },
    "code documentation": {
        "terms": [
            "code-block", "syntax highlight", "syntax-highlight",
            "inline code", "inline-code",
            "language tab", "language-tab",
            "copy code button", "copy-code", "copy-code-button",
        ],
        "description": "코드 블록 · 인라인 코드 · 언어 탭 · 복사 버튼",
    },
    "callout and admonition": {
        "terms": [
            "callout", "admonition", "admonition-block",
            "info callout", "info-callout",
            "tip callout", "tip-callout",
            "warning callout", "warning-callout",
            "danger callout", "danger-callout",
        ],
        "description": "문서 내 강조 박스 (info/warning/danger/tip)",
    },
    "api reference": {
        "terms": [
            "api reference", "api-reference", "api 레퍼런스",
            "endpoint reference", "엔드포인트 레퍼런스",
            "api reference table", "api-reference-table",
            "parameter table", "parameter-table",
            "response schema", "request schema",
            "version switcher", "version-switcher",
        ],
        "description": "API 레퍼런스 테이블 · 파라미터 테이블 · 버전 스위처",
    },
    "community feed": {
        "terms": [
            "community feed", "community-feed", "social feed", "social-feed",
            "feed item", "feed-item",
            "post card", "post-card",
            "thread view", "thread-view",
            "reply composer", "reply-composer",
            "reaction bar", "reaction-bar", "reaction bubble",
            "follow button", "follow-button", "follow toggle",
            "timeline stream", "timeline-stream",
            "avatar cluster", "avatar-cluster",
            "tag pill", "tag-pill",
            "share sheet", "share-sheet",
            "empty-feed illustration", "empty-feed-illustration",
            "gentle toast", "gentle-toast",
            "soft dialog", "soft-dialog",
        ],
        "description": "친근한 소셜 피드/스레드 구조 — feed item · post card · thread view · reaction bar · follow button",
    },
    "presence and notifications": {
        "terms": [
            "presence indicator", "presence-indicator", "presence dot",
            "notification center", "notification-center",
            "notification item", "notification-item",
            "notification badge",
            "mention highlight", "mention-highlight",
        ],
        "description": "프레즌스 · 알림 센터 · 알림 아이템 · 멘션 하이라이트",
    },
    "canvas workspace": {
        "terms": [
            "canvas workspace", "canvas-workspace",
            "ruler", "snap guide", "snap-guide",
            "grid overlay", "grid-overlay",
            "selection handle", "selection-handle",
            "zoom control", "zoom-control",
            "minimap",
        ],
        "description": "캔버스 작업 영역 — ruler · snap guide · grid overlay · selection handle · zoom · minimap",
    },
    "design tool chrome": {
        "terms": [
            "layer panel", "layer-panel",
            "layer item", "layer-item",
            "layer thumbnail", "layer-thumbnail",
            "inspector panel", "inspector-panel",
            "property row", "property-row",
            "toolbar group", "toolbar-group",
            "contextual toolbar", "contextual-toolbar",
            "asset library", "asset-library",
            "asset card", "asset-card",
            "export panel", "export-panel",
            "format selector", "format-selector",
            "shortcut cheatsheet", "shortcut-cheatsheet",
            "keyboard shortcut cheatsheet", "keyboard-shortcut-cheatsheet",
            "design tool", "design-tool",
        ],
        "description": "캔버스 도구 chrome — layer panel · inspector panel · property row · toolbar group · asset library · export panel",
    },
    "product catalog": {
        "terms": [
            "product grid", "product-grid",
            "product card", "product-card",
            "product detail", "product-detail",
            "product gallery", "product-gallery",
            "product hero image", "product-hero-image",
            "image thumbnail", "image-thumbnail",
            "variant selector", "variant-selector",
            "size selector", "size-selector", "size chip",
            "color swatch selector", "color-swatch-selector", "color swatch",
            "add-to-cart", "add to cart", "add-to-cart-button",
            "quick view modal", "quick-view modal", "quick-view-modal",
            "wishlist toggle", "wishlist-toggle",
            "price tag", "price-tag",
            "original price strikethrough", "original-price-strikethrough",
            "discount badge", "discount-badge",
            "cross-sell grid", "cross-sell-grid",
            "category pill", "category-pill",
            "filter sidebar", "filter-sidebar",
            "sort dropdown", "sort-dropdown",
        ],
        "description": "커머스 제품 카탈로그 — product grid · product card · product detail · product gallery · variant/size/color selector · add-to-cart · price tag · discount badge",
    },
    "cart and checkout": {
        "terms": [
            "cart drawer", "cart-drawer",
            "cart item", "cart-item",
            "cart summary", "cart-summary",
            "quantity stepper", "quantity-stepper",
            "checkout step", "checkout-step",
            "checkout step progress", "checkout-step-progress",
            "address form", "address-form",
            "payment form", "payment-form",
            "promo code input", "promo-code-input", "promo code",
            "order summary", "order-summary",
            "empty cart state", "empty-cart-state", "empty cart",
        ],
        "description": "커머스 장바구니/결제 — cart drawer · cart item · quantity stepper · cart summary · checkout step · address/payment form · promo code · order summary · empty cart",
    },
    "playful commerce": {
        "terms": [
            "add-to-cart-pill", "add to cart pill", "gentle add-to-cart",
            "variant-chip", "rounded-variant-chip", "rounded variant chip",
            "rounded product-card", "soft product-card",
            "review-card", "emoji-reaction", "emoji review",
            "bestseller-ribbon", "bestseller ribbon",
            "gift-message-input", "gift message input", "gift-message",
            "subscription-toggle", "subscription toggle",
            "subscription-card", "subscription card",
            "consumer-toast", "gentle checkout", "playful-checkout",
            "rounded cart-drawer", "soft cart drawer",
            "empty cart illustration",
        ],
        "description": "playful-soft commerce 특화 — rounded product-card · variant-chip · gentle add-to-cart-pill · review-card · emoji-reaction · bestseller-ribbon · gift-message-input · subscription-toggle · consumer-toast, D2C craft 컨슈머 commerce 정체성",
    },
    "drop and merchandising": {
        "terms": [
            "drop banner", "drop-banner",
            "countdown timer", "countdown-timer", "countdown timer chip",
            "lookbook hero", "lookbook-hero",
            "featured category tile", "featured-category-tile",
            "hero banner", "hero-banner",
            "drop countdown",
        ],
        "description": "커머스 드롭/머천다이즈 — drop banner · countdown timer · lookbook hero · featured category tile · hero banner",
    },
    "writing artifact": {
        "terms": [
            "writing artifact", "writing-artifact",
            "message artifact", "message-artifact",
            "artifact preview panel", "artifact-preview-panel",
            "draft document", "draft-document",
            "outline sidebar", "outline-sidebar",
            "revision timeline", "revision-timeline",
            "tone slider", "tone-slider",
            "reading mode toggle", "reading-mode-toggle", "reading-mode",
            "citation footnote", "citation-footnote",
            "quote block", "quote-block",
            "paragraph block", "paragraph-block",
        ],
        "description": "writing copilot artifact — message artifact · artifact preview panel · draft document · outline sidebar · revision timeline · tone slider · reading-mode toggle · citation footnote · quote/paragraph block",
    },
    "conversation copilot chrome": {
        "terms": [
            "prompt composer", "prompt-composer",
            "streaming cursor", "streaming-cursor",
            "typing indicator", "typing-indicator",
            "inline citation", "inline-citation",
            "regenerate button", "regenerate-button",
            "stop-generation button", "stop-generation-button", "stop generation",
            "mention chip", "mention-chip",
            "suggestion card", "suggestion-card",
            "thread header", "thread-header",
            "new thread button", "new-thread-button",
            "empty conversation state", "empty-conversation-state", "empty conversation",
        ],
        "description": "대화형 copilot chrome — prompt composer · streaming cursor · typing indicator · inline citation · regenerate/stop button · mention chip · suggestion card · thread header · new-thread button · empty conversation state",
    },
    "bold editorial magazine": {
        "terms": [
            "masthead",
            "issue header", "issue-header",
            "issue number", "issue-number",
            "cover story", "cover-story",
            "opening spread", "opening-spread",
            "feature article", "feature-article",
            "kicker eyebrow", "kicker-eyebrow",
            "pull quote", "pull-quote",
            "drop cap", "drop-cap",
            "section break", "section-break",
            "article gallery", "article-gallery",
            "subscription callout", "subscription-callout",
        ],
        "description": "bold editorial magazine chrome — masthead · issue header · cover story · opening spread · feature article · kicker eyebrow · pull quote · drop cap · section break · article gallery · subscription callout",
    },
    "opinion long-form": {
        "terms": [
            "opinion byline", "opinion-byline",
            "manifesto section", "manifesto-section",
            "feature grid index", "feature-grid-index",
            "archive index", "archive-index",
            "issue archive", "issue-archive",
            "reading progress bar", "reading-progress-bar",
            "credit line", "credit-line",
        ],
        "description": "opinion long-form chrome — opinion byline · manifesto section · feature grid index · archive index · issue archive · reading progress bar · credit line",
    },
    "editorial curation dashboard": {
        "terms": [
            "curation queue", "curation-queue",
            "editorial calendar", "editorial-calendar",
            "draft status pill", "draft-status-pill",
            "article preview pane", "article-preview-pane",
            "contributor roster", "contributor-roster",
            "editorial analytics kpi", "editorial-analytics-kpi", "editorial analytics",
            "reading analytics kpi", "reading-analytics-kpi", "reading analytics",
            "archive shelf", "archive-shelf",
            "tag taxonomy manager", "tag-taxonomy-manager",
        ],
        "description": "editorial 큐레이션 운영 대시보드 chrome — curation queue · editorial calendar · draft status pill · article preview pane · contributor roster · editorial analytics · reading analytics · archive shelf · tag taxonomy manager",
    },
    "publishing workflow": {
        "terms": [
            "publishing pipeline", "publishing-pipeline",
            "issue planner", "issue-planner",
            "pipeline stage", "pipeline-stage",
            "schedule cell", "schedule-cell",
            "editorial workflow", "editorial-workflow",
            "assign reviewer", "assign-reviewer",
            "publish scheduler", "publish-scheduler",
            "content status timeline", "content-status-timeline",
        ],
        "description": "퍼블리싱 워크플로 chrome — publishing pipeline · issue planner · pipeline stage · schedule cell · editorial workflow · assign reviewer · publish scheduler · content status timeline",
    },
    "growth analytics admin": {
        "terms": [
            "activation funnel", "activation-funnel",
            "cohort matrix", "cohort-matrix",
            "referral widget", "referral-widget",
            "retention chart", "retention-chart",
            "conversion funnel", "conversion-funnel",
            "experiment panel", "experiment-panel",
            "goal tracker", "goal-tracker",
            "ticket queue", "ticket-queue",
            "alert list", "alert-list",
            "segment filter", "segment-filter",
            "user list", "user-list",
            "filter bar", "filter-bar",
        ],
        "description": "B2C 스타트업 그로스 admin chrome — activation funnel · cohort matrix · retention chart · conversion funnel · referral widget · experiment panel · goal tracker · user list · ticket queue · alert list · segment filter · filter bar",
    },
    "wellness habit tracking": {
        "terms": [
            "streak indicator", "streak-indicator",
            "habit calendar", "habit-calendar",
            "wellness score", "wellness-score",
            "mood check", "mood-check",
            "mood chart", "mood-chart",
            "session tracker", "session-tracker",
            "session timeline", "session-timeline",
            "goal grid", "goal-grid",
            "dashboard card", "dashboard-card",
        ],
        "description": "consumer wellness habit admin chrome — streak indicator · habit calendar · wellness score · mood check · mood chart · session tracker · session timeline · goal grid · dashboard card",
    },
}

# 패턴 → 생성할 컴포넌트 매핑
PATTERN_COMPONENTS: dict[str, list[dict]] = {
    "workspace navigation": [
        {"name": "app-shell", "family": "navigation", "role": "전체 앱 레이아웃과 네비게이션 컨테이너"},
        {"name": "sidebar-nav", "family": "navigation", "role": "주요 섹션 간 이동을 위한 사이드 네비게이션"},
        {"name": "topbar", "family": "navigation", "role": "앱 상단 바 (로고, 검색, 사용자 메뉴)"},
        {"name": "breadcrumb", "family": "navigation", "role": "현재 위치를 계층적으로 표시"},
        {"name": "tab-bar", "family": "navigation", "role": "섹션 내 하위 탭 전환"},
    ],
    "rich text editor": [
        {"name": "editor-canvas", "family": "editorial", "role": "텍스트 편집 영역"},
        {"name": "editor-toolbar", "family": "editorial", "role": "서식 도구 모음"},
        {"name": "inline-format-menu", "family": "editorial", "role": "텍스트 선택 시 나타나는 인라인 포맷 메뉴"},
        {"name": "slash-command-menu", "family": "editorial", "role": "/ 입력으로 블록 타입 선택"},
        {"name": "block-controls", "family": "editorial", "role": "블록 이동/삭제/타입 변경 컨트롤"},
    ],
    "command palette": [
        {"name": "command-palette", "family": "overlay", "role": "글로벌 커맨드 팔레트 오버레이"},
        {"name": "command-result-item", "family": "overlay", "role": "검색/명령 결과 항목"},
        {"name": "shortcut-hint", "family": "feedback", "role": "키보드 단축키 힌트 표시"},
    ],
    "dashboard cards": [
        {"name": "stat-card", "family": "data-display", "role": "주요 수치를 표시하는 통계 카드"},
        {"name": "insight-card", "family": "data-display", "role": "인사이트나 트렌드를 요약하는 카드"},
        {"name": "activity-card", "family": "data-display", "role": "최근 활동 피드 카드"},
        {"name": "section-header", "family": "data-display", "role": "대시보드 섹션 구분 헤더"},
    ],
    "data tables": [
        {"name": "data-table", "family": "data-display", "role": "정렬·필터 가능한 데이터 테이블"},
        {"name": "column-header", "family": "data-display", "role": "테이블 컬럼 헤더 (정렬 토글)"},
        {"name": "row-actions", "family": "data-display", "role": "행별 액션 메뉴"},
        {"name": "pagination", "family": "navigation", "role": "페이지 이동 컨트롤"},
        {"name": "filter-chip", "family": "input", "role": "활성 필터를 칩으로 표시/해제"},
    ],
    "forms": [
        {"name": "text-field", "family": "input", "role": "단일 줄 텍스트 입력"},
        {"name": "textarea", "family": "input", "role": "여러 줄 텍스트 입력"},
        {"name": "select", "family": "input", "role": "드롭다운 선택"},
        {"name": "checkbox", "family": "input", "role": "체크박스"},
        {"name": "radio-group", "family": "input", "role": "라디오 버튼 그룹"},
        {"name": "form-section", "family": "input", "role": "폼 섹션 그룹핑과 레이블"},
        {"name": "form-actions", "family": "button", "role": "폼 하단 제출/취소 버튼 영역"},
    ],
    "notifications": [
        {"name": "toast", "family": "feedback", "role": "일시적 성공/에러 알림"},
        {"name": "inline-alert", "family": "feedback", "role": "페이지 내 알림 배너"},
        {"name": "empty-state", "family": "feedback", "role": "데이터가 없을 때 안내 화면"},
        {"name": "banner", "family": "feedback", "role": "전체 화면 상단 공지 배너"},
    ],
    "file upload": [
        {"name": "upload-dropzone", "family": "input", "role": "드래그앤드롭 파일 업로드 영역"},
        {"name": "file-preview", "family": "data-display", "role": "업로드된 파일 미리보기"},
        {"name": "upload-progress", "family": "feedback", "role": "업로드 진행률 표시"},
    ],
    "calendar and dates": [
        {"name": "date-picker", "family": "input", "role": "날짜 선택기"},
        {"name": "calendar-grid", "family": "data-display", "role": "월간 캘린더 그리드"},
        {"name": "time-picker", "family": "input", "role": "시간 선택기"},
        {"name": "date-range-picker", "family": "input", "role": "기간 선택기"},
    ],
    "charts and visualization": [
        {"name": "chart-container", "family": "data-display", "role": "차트 래퍼 (타이틀, 범례 포함)"},
        {"name": "chart-tooltip", "family": "overlay", "role": "데이터 포인트 호버 시 상세 정보"},
        {"name": "chart-legend", "family": "data-display", "role": "차트 범례"},
    ],
    "user profile and avatar": [
        {"name": "avatar", "family": "data-display", "role": "사용자 프로필 이미지/이니셜"},
        {"name": "user-menu", "family": "overlay", "role": "사용자 드롭다운 메뉴"},
        {"name": "profile-card", "family": "data-display", "role": "사용자 프로필 요약 카드"},
    ],
    "comments and discussion": [
        {"name": "comment-thread", "family": "data-display", "role": "댓글 스레드 목록"},
        {"name": "comment-input", "family": "input", "role": "댓글 입력 영역"},
        {"name": "mention-popup", "family": "overlay", "role": "@멘션 자동완성 팝업"},
    ],
    "tags and labels": [
        {"name": "tag", "family": "data-display", "role": "분류/라벨 태그"},
        {"name": "status-badge", "family": "feedback", "role": "상태를 색상으로 표시하는 뱃지"},
        {"name": "chip", "family": "input", "role": "선택/해제 가능한 칩"},
    ],
    "search and filter": [
        {"name": "search-field", "family": "input", "role": "검색 입력 필드"},
        {"name": "search-results", "family": "data-display", "role": "검색 결과 목록"},
        {"name": "filter-panel", "family": "input", "role": "필터 옵션 패널"},
        {"name": "autocomplete", "family": "overlay", "role": "자동완성 드롭다운"},
    ],
    "modal and dialog": [
        {"name": "modal-dialog", "family": "overlay", "role": "확인/입력을 받는 모달"},
        {"name": "bottom-sheet", "family": "overlay", "role": "모바일용 하단 시트"},
        {"name": "confirm-dialog", "family": "overlay", "role": "삭제/위험 작업 확인 다이얼로그"},
    ],
    "onboarding and stepper": [
        {"name": "step-progress", "family": "feedback", "role": "단계별 진행 표시"},
        {"name": "wizard-layout", "family": "navigation", "role": "위저드 레이아웃 (이전/다음)"},
        {"name": "tooltip-guide", "family": "overlay", "role": "기능 안내 툴팁"},
    ],
    "pricing and plans": [
        {"name": "pricing-card", "family": "data-display", "role": "플랜별 가격/기능 비교 카드"},
        {"name": "feature-comparison", "family": "data-display", "role": "플랜 간 기능 비교 테이블"},
        {"name": "upgrade-banner", "family": "feedback", "role": "업그레이드 유도 배너"},
    ],
    "kanban and board": [
        {"name": "kanban-board", "family": "data-display", "role": "칸반 보드 레이아웃"},
        {"name": "kanban-column", "family": "data-display", "role": "칸반 컬럼 (상태별)"},
        {"name": "kanban-card", "family": "data-display", "role": "드래그 가능한 작업 카드"},
    ],
    "chat and messaging": [
        {"name": "chat-message", "family": "data-display", "role": "채팅 메시지 말풍선"},
        {"name": "chat-input", "family": "input", "role": "메시지 입력 영역"},
        {"name": "chat-thread", "family": "data-display", "role": "대화 스레드 목록"},
    ],
    "media player": [
        {"name": "video-player", "family": "data-display", "role": "비디오 재생기"},
        {"name": "player-controls", "family": "button", "role": "재생/일시정지/시크 컨트롤"},
        {"name": "volume-slider", "family": "input", "role": "볼륨 조절 슬라이더"},
    ],
    "hero section": [
        {"name": "hero-container", "family": "marketing", "role": "랜딩 상단 히어로 섹션 컨테이너"},
        {"name": "hero-eyebrow", "family": "marketing", "role": "헤드라인 위 카테고리/레이블 텍스트"},
        {"name": "hero-headline", "family": "marketing", "role": "핵심 가치 제안 헤드라인"},
        {"name": "hero-subheadline", "family": "marketing", "role": "헤드라인을 보강하는 서브 카피"},
        {"name": "hero-cta-group", "family": "button", "role": "primary/secondary CTA 버튼 묶음"},
        {"name": "hero-visual", "family": "marketing", "role": "히어로 우측/하단의 제품 스크린샷 또는 일러스트"},
        {"name": "hero-trust-strip", "family": "marketing", "role": "히어로 바로 아래의 신뢰 라인 (사용자 수, 평가 등)"},
    ],
    "feature grid": [
        {"name": "feature-section", "family": "marketing", "role": "기능 섹션 컨테이너와 섹션 헤더"},
        {"name": "feature-grid", "family": "marketing", "role": "여러 개의 기능 카드를 배치하는 그리드"},
        {"name": "feature-card", "family": "marketing", "role": "개별 기능 카드 (아이콘+제목+설명)"},
        {"name": "feature-icon", "family": "marketing", "role": "기능을 상징하는 아이콘"},
        {"name": "feature-title", "family": "marketing", "role": "기능 카드 제목"},
        {"name": "feature-description", "family": "marketing", "role": "기능 카드 본문 설명"},
    ],
    "social proof": [
        {"name": "logo-cloud", "family": "marketing", "role": "고객/파트너 로고를 나열하는 영역"},
        {"name": "customer-logo", "family": "marketing", "role": "개별 고객사 로고 아이템"},
        {"name": "metric-highlight", "family": "marketing", "role": "주요 지표를 크게 강조하는 숫자 카드"},
        {"name": "press-quote", "family": "marketing", "role": "언론 인용 또는 어워드 스트립"},
    ],
    "testimonial": [
        {"name": "testimonial-section", "family": "marketing", "role": "추천사 섹션 컨테이너"},
        {"name": "testimonial-card", "family": "marketing", "role": "고객 인용을 담는 카드"},
        {"name": "testimonial-quote", "family": "marketing", "role": "추천사 본문 텍스트"},
        {"name": "testimonial-author", "family": "marketing", "role": "추천사 작성자 정보 (이름/직책/회사)"},
    ],
    "faq accordion": [
        {"name": "faq-section", "family": "marketing", "role": "FAQ 섹션 컨테이너와 섹션 헤더"},
        {"name": "faq-item", "family": "marketing", "role": "접고 펼 수 있는 개별 FAQ 항목"},
        {"name": "faq-question", "family": "marketing", "role": "FAQ 질문 헤더 (클릭 가능한 트리거)"},
        {"name": "faq-answer", "family": "marketing", "role": "FAQ 답변 본문"},
    ],
    "landing cta section": [
        {"name": "cta-section", "family": "marketing", "role": "전환 유도 CTA 섹션 컨테이너"},
        {"name": "cta-headline", "family": "marketing", "role": "전환을 유도하는 헤드라인"},
        {"name": "cta-supporting-text", "family": "marketing", "role": "CTA를 보강하는 서포팅 카피"},
        {"name": "cta-button-group", "family": "button", "role": "primary/secondary CTA 묶음"},
    ],
    "site footer": [
        {"name": "site-footer", "family": "marketing", "role": "사이트 전역 하단 컨테이너"},
        {"name": "footer-column", "family": "marketing", "role": "링크 그룹을 담는 세로 컬럼"},
        {"name": "footer-link", "family": "marketing", "role": "푸터 내 개별 링크"},
        {"name": "footer-legal", "family": "marketing", "role": "저작권·법적 고지 영역"},
        {"name": "footer-social", "family": "marketing", "role": "소셜 링크 아이콘 그룹"},
    ],
    "site header": [
        {"name": "site-header", "family": "marketing", "role": "랜딩 상단 고정 헤더"},
        {"name": "site-logo", "family": "marketing", "role": "브랜드 로고 영역"},
        {"name": "site-nav", "family": "marketing", "role": "주요 섹션 내비게이션 링크"},
        {"name": "site-nav-cta", "family": "button", "role": "헤더 우측 CTA 버튼 (로그인/시작하기)"},
        {"name": "mobile-menu-trigger", "family": "button", "role": "모바일 햄버거 메뉴 버튼"},
    ],
    "reference documentation": [
        {"name": "article-body", "family": "document", "role": "long-form article body — prose block + heading anchor"},
        {"name": "table-of-contents", "family": "document", "role": "TOC sidebar with anchor-linked heading outline"},
        {"name": "heading-anchor", "family": "document", "role": "h1~h6 heading with #id anchor and copy-link"},
        {"name": "prose-block", "family": "document", "role": "prose reading block rendering markdown article content"},
        {"name": "reading-pane", "family": "document", "role": "main reading column, measured width 65–75ch"},
        {"name": "footnote", "family": "document", "role": "numbered reference footnote inside article body"},
        {"name": "prev-next-pager", "family": "navigation", "role": "bottom-of-article prev/next reference link"},
        {"name": "link-card", "family": "document", "role": "related article card with title + summary"},
    ],
    "code documentation": [
        {"name": "code-block", "family": "document", "role": "syntax-highlighted code block with copy button + language tab"},
        {"name": "inline-code", "family": "document", "role": "inline code span with mono font and subtle background"},
        {"name": "language-tab", "family": "document", "role": "code block language switcher (ts/python/curl/go)"},
        {"name": "copy-code-button", "family": "button", "role": "copy-to-clipboard button for code block"},
    ],
    "callout and admonition": [
        {"name": "callout", "family": "document", "role": "article callout — info/warning/tip/danger variants"},
        {"name": "admonition-block", "family": "document", "role": "admonition block with icon + label + body"},
    ],
    "api reference": [
        {"name": "api-reference-table", "family": "document", "role": "endpoint/method/status/type API reference table"},
        {"name": "parameter-table", "family": "document", "role": "parameter list (name/type/required/description)"},
        {"name": "version-switcher", "family": "navigation", "role": "dropdown to switch doc version (v1/v2/latest)"},
    ],
    "community feed": [
        {"name": "feed-item", "family": "social", "role": "timeline stream 의 기본 단위 — avatar + post card wrap"},
        {"name": "post-card", "family": "social", "role": "rounded post card — 본문 + 이미지 + 반응 + 스레드 미리보기"},
        {"name": "thread-view", "family": "social", "role": "부모 post + reply list + composer 를 엮는 thread 페이지"},
        {"name": "reply-composer", "family": "input", "role": "친근한 quick reply 입력기 (이모지 picker + mention)"},
        {"name": "reaction-bar", "family": "social", "role": "이모지 reaction bubble — optimistic update, 좋아요/하트/축하"},
        {"name": "follow-button", "family": "button", "role": "rounded follow toggle — presence 연동, 친근 micro-interaction"},
        {"name": "timeline-stream", "family": "social", "role": "infinite scroll feed stream, pull-to-refresh"},
        {"name": "avatar-cluster", "family": "social", "role": "여러 아바타를 겹쳐 보여주는 reaction/참여자 요약"},
        {"name": "tag-pill", "family": "data-display", "role": "rounded tag pill — 해시태그/토픽/카테고리"},
        {"name": "share-sheet", "family": "overlay", "role": "친근한 bottom sheet 공유 패널"},
        {"name": "empty-feed-illustration", "family": "feedback", "role": "empty state illustration — 친근 톤 copy"},
        {"name": "gentle-toast", "family": "feedback", "role": "low-noise 성공/완료 toast — playful-soft 모션"},
        {"name": "soft-dialog", "family": "overlay", "role": "rounded-16 dialog — 파괴적 액션도 부드럽게 confirm"},
    ],
    "presence and notifications": [
        {"name": "presence-indicator", "family": "social", "role": "avatar 옆 presence dot — online/idle/offline"},
        {"name": "notification-center", "family": "overlay", "role": "알림 모아보기 패널 — grouped + swipe archive"},
        {"name": "notification-item", "family": "data-display", "role": "개별 알림 (mention/reply/follow/reaction) + presence"},
        {"name": "mention-highlight", "family": "data-display", "role": "@mention 텍스트 강조 + tap 프로필 미리보기"},
    ],
    "canvas workspace": [
        {"name": "canvas-workspace", "family": "canvas", "role": "neutral canvas surface with ruler + grid overlay + infinite zoom/pan"},
        {"name": "ruler", "family": "canvas", "role": "canvas 좌/상단 ruler chrome — px/pt/% 단위, drag 로 guide 생성"},
        {"name": "snap-guide", "family": "canvas", "role": "selection 정렬 시 나타나는 single-accent snap guide line"},
        {"name": "grid-overlay", "family": "canvas", "role": "pixel-precise grid overlay — 8px/16px/custom toggle"},
        {"name": "selection-handle", "family": "canvas", "role": "선택된 객체의 8 handle (corner + edge), shift 비례 스케일"},
        {"name": "zoom-control", "family": "canvas", "role": "canvas 우하단 zoom 입력 + 100%/fit 버튼"},
        {"name": "minimap", "family": "canvas", "role": "큰 캔버스용 minimap — 현재 viewport 박스 표시"},
    ],
    "design tool chrome": [
        {"name": "layer-panel", "family": "tool-chrome", "role": "dense layer tree — depth indent · drag reorder · visibility/lock toggle"},
        {"name": "layer-item", "family": "tool-chrome", "role": "layer panel 의 단위 — thumbnail + name + visibility/lock + depth chevron"},
        {"name": "layer-thumbnail", "family": "tool-chrome", "role": "16–24px 미니 미리보기 thumbnail — 빈 레이어는 muted 아이콘"},
        {"name": "inspector-panel", "family": "tool-chrome", "role": "thin inspector panel — property row 컨테이너, section collapse"},
        {"name": "property-row", "family": "input", "role": "라벨 + 입력(숫자/색/select) + unit, mono-font 숫자, drag-to-scrub"},
        {"name": "toolbar-group", "family": "tool-chrome", "role": "toolbar 안의 도구 묶음 — active state 는 single accent 강조"},
        {"name": "contextual-toolbar", "family": "tool-chrome", "role": "선택 상태에 따라 canvas 위에 부드럽게 떠오르는 toolbar"},
        {"name": "asset-library", "family": "tool-chrome", "role": "좌측 패널 asset grid + drag-to-canvas — 태그/검색 필터"},
        {"name": "asset-card", "family": "tool-chrome", "role": "asset library 의 단위 — thumbnail + name + tag pill"},
        {"name": "export-panel", "family": "tool-chrome", "role": "우측 sheet — format/scale/preview/export queue"},
        {"name": "format-selector", "family": "input", "role": "png/svg/pdf/webp 토글 + 스케일 (1x/2x/3x)"},
        {"name": "keyboard-shortcut-cheatsheet", "family": "overlay", "role": "`?` 단축키로 호출되는 shortcut grid + 검색 + section filter"},
    ],
    "product catalog": [
        {"name": "product-grid", "family": "commerce", "role": "dense product grid — 카테고리/검색/홈에서 여러 제품 카드를 배치"},
        {"name": "product-card", "family": "commerce", "role": "개별 product card — thumbnail + 제품 title + price tag + discount badge + quick-view trigger"},
        {"name": "product-detail", "family": "commerce", "role": "product detail 화면 컨테이너 — gallery + selectors + add-to-cart + cross-sell"},
        {"name": "product-gallery", "family": "commerce", "role": "제품 상세 gallery — main image + thumbnail rail, swipe/keyboard 지원"},
        {"name": "product-hero-image", "family": "commerce", "role": "제품 상세 상단 full-bleed hero image"},
        {"name": "image-thumbnail", "family": "commerce", "role": "제품 썸네일 이미지 — aspect-ratio fixed, hover zoom"},
        {"name": "variant-selector", "family": "input", "role": "variant (색상/사이즈/모델) 선택기 — segmented chip group"},
        {"name": "size-selector", "family": "input", "role": "size selector chip (S/M/L/XL) — 품절 state 포함"},
        {"name": "color-swatch-selector", "family": "input", "role": "color swatch chip 선택기 — 선택 ring 강조"},
        {"name": "add-to-cart-button", "family": "button", "role": "primary CTA add-to-cart — saturated fill + impact label + bump animation"},
        {"name": "quick-view-modal", "family": "overlay", "role": "product grid 위에서 뜨는 quick-view modal — gallery 축소 + add-to-cart"},
        {"name": "wishlist-toggle", "family": "button", "role": "heart toggle — optimistic update, aria-pressed"},
        {"name": "price-tag", "family": "commerce", "role": "bold price tag — mono tabular-nums, 세일가 강조"},
        {"name": "original-price-strikethrough", "family": "commerce", "role": "할인 시 원가 strikethrough — muted mono"},
        {"name": "discount-badge", "family": "feedback", "role": "할인율 badge (-NN% / SALE / HOT / DROP)"},
        {"name": "cross-sell-grid", "family": "commerce", "role": "제품 상세 하단 추천 product grid (함께 구매 / 비슷한 상품)"},
        {"name": "category-pill", "family": "navigation", "role": "카테고리 필터 pill row — New / 의류 / 신발 / 액세서리 / Sale"},
        {"name": "filter-sidebar", "family": "input", "role": "카테고리/가격/브랜드/사이즈/색상 필터 사이드바"},
        {"name": "sort-dropdown", "family": "input", "role": "정렬 dropdown — 신상품 / 인기순 / 가격 낮은순 / 가격 높은순"},
    ],
    "cart and checkout": [
        {"name": "cart-drawer", "family": "commerce", "role": "cart drawer slide-in — 우측 슬라이드, backdrop dim, focus trap"},
        {"name": "cart-item", "family": "commerce", "role": "장바구니 상품 — thumbnail + 제품 title + variant + price + quantity stepper + 삭제"},
        {"name": "cart-summary", "family": "commerce", "role": "cart summary — 소계 + 배송비 + 할인 + 총액, mono tabular-nums"},
        {"name": "quantity-stepper", "family": "input", "role": "quantity stepper — -/+ 버튼 + 직접 입력, mono tabular-nums, 재고 clamp"},
        {"name": "checkout-step", "family": "commerce", "role": "checkout step — 배송 → 결제 → 확인, active/완료/대기 상태"},
        {"name": "checkout-step-progress", "family": "feedback", "role": "상단 checkout step indicator bar — role=progressbar"},
        {"name": "address-form", "family": "input", "role": "배송지 form — 수령인/전화/주소/요청사항"},
        {"name": "payment-form", "family": "input", "role": "결제 form — 카드/간편결제/무통장 선택 + 카드 입력"},
        {"name": "promo-code-input", "family": "input", "role": "promo code input + apply 버튼 + flash feedback"},
        {"name": "order-summary", "family": "commerce", "role": "주문 요약 — cart item 축소 + 배송비 + 할인 + 총액"},
        {"name": "empty-cart-state", "family": "feedback", "role": "empty cart 안내 illustration + 계속 쇼핑 CTA"},
    ],
    "drop and merchandising": [
        {"name": "drop-banner", "family": "commerce", "role": "hero drop 전용 banner — drop name + countdown + CTA + impact typography"},
        {"name": "countdown-timer", "family": "commerce", "role": "drop countdown timer chip — D/H/M/S mono tabular-nums, accent 강조"},
        {"name": "lookbook-hero", "family": "commerce", "role": "에디토리얼 lookbook tile — full-bleed image + overlay copy"},
        {"name": "featured-category-tile", "family": "commerce", "role": "홈 featured category tile — large product image + category label"},
        {"name": "hero-banner", "family": "commerce", "role": "full-bleed hero banner — saturated primary surface, large product hero image"},
    ],
    "writing artifact": [
        {"name": "message-artifact", "family": "copilot-artifact", "role": "chat message 내 artifact 진입 카드 — 드래프트 미리보기 + 열기 CTA"},
        {"name": "artifact-preview-panel", "family": "copilot-artifact", "role": "우측 아티팩트 미리보기 패널 — draft document + outline + revision timeline"},
        {"name": "draft-document", "family": "copilot-artifact", "role": "에세이/뉴스레터/저널 드래프트 문서 본체 — reading-first 65–75ch"},
        {"name": "outline-sidebar", "family": "copilot-artifact", "role": "heading anchor 기반 outline 목차 — 접기/펼치기"},
        {"name": "revision-timeline", "family": "copilot-artifact", "role": "드래프트 리비전 세로 타임라인 — 시간 순 diff preview 진입"},
        {"name": "tone-slider", "family": "input", "role": "calm↔warm / formal↔casual tone slider — 아티팩트 재작성 트리거"},
        {"name": "reading-mode-toggle", "family": "copilot-artifact", "role": "reading mode 토글 — wide/narrow · serif/sans · line-height"},
        {"name": "citation-footnote", "family": "copilot-artifact", "role": "아티팩트 하단 주석 · 인용 출처 목록"},
        {"name": "quote-block", "family": "copilot-artifact", "role": "인용문 블록 — serif italic, muted vertical rule"},
        {"name": "paragraph-block", "family": "copilot-artifact", "role": "본문 문단 블록 — reading pane line-height 1.6–1.7"},
    ],
    "conversation copilot chrome": [
        {"name": "prompt-composer", "family": "input", "role": "멀티라인 prompt composer — 수납형 grow, 한글 IME keep-all, 제출/개행 규칙"},
        {"name": "streaming-cursor", "family": "copilot-chat", "role": "응답 생성 중 calm blinking cursor — slow fade, prefers-reduced-motion 존중"},
        {"name": "typing-indicator", "family": "copilot-chat", "role": "'copilot is thinking…' typing dots — low-noise 상태"},
        {"name": "inline-citation", "family": "copilot-chat", "role": "본문 내 citation 번호/괄호 링크 — hover tooltip + footnote 연결"},
        {"name": "regenerate-button", "family": "button", "role": "응답 재생성 버튼 — ghost serif label, 생성 완료 후 활성"},
        {"name": "stop-generation-button", "family": "button", "role": "응답 중단 버튼 — muted danger ghost, 생성 중에만 활성"},
        {"name": "mention-chip", "family": "copilot-chat", "role": "@thread/@citation/@note mention 칩 — muted accent fill"},
        {"name": "suggestion-card", "family": "copilot-chat", "role": "prompt 시작 suggestion card — 에세이/뉴스레터/저널 editorial 스타터"},
        {"name": "thread-header", "family": "copilot-chat", "role": "현재 thread 제목 · 작성 시점 · 아카이브 토글 — restrained editorial chrome"},
        {"name": "new-thread-button", "family": "button", "role": "새 대화 시작 버튼 — warm accent primary"},
        {"name": "empty-conversation-state", "family": "feedback", "role": "empty conversation 안내 — 일러스트 + gentle 온보딩 카피 + suggestion card"},
    ],
    "bold editorial magazine": [
        {"name": "masthead", "family": "magazine", "role": "issue masthead — 잡지 제호 · 로고 · issue 번호 · 표지 링크"},
        {"name": "issue-header", "family": "magazine", "role": "이슈 헤더 — issue title · 발행일 · 권/호 · 주요 섹션 jump"},
        {"name": "issue-number", "family": "magazine", "role": "issue 번호 칩 — mono tabular-nums, bold accent"},
        {"name": "cover-story", "family": "magazine", "role": "표지 feature cover story — full-bleed hero + kicker + headline + byline"},
        {"name": "opening-spread", "family": "magazine", "role": "기사 opening spread — drop cap 시작 · pull quote · 여백 많은 bold 레이아웃"},
        {"name": "feature-article", "family": "magazine", "role": "feature article 본체 — article-body + pull-quote + drop-cap + section-break + heading-anchor + prose-block + reading-pane long-form"},
        {"name": "kicker-eyebrow", "family": "magazine", "role": "기사 kicker eyebrow — headline 위 카테고리/섹션 라벨, letter-spacing tight"},
        {"name": "pull-quote", "family": "magazine", "role": "bold pull quote block — oversized serif/sans, saturated accent rule"},
        {"name": "drop-cap", "family": "magazine", "role": "기사 첫 문단 drop cap — 3–4 line initial letter, impact"},
        {"name": "section-break", "family": "magazine", "role": "article 내 section break — chunky divider rule + ornament glyph"},
        {"name": "article-gallery", "family": "magazine", "role": "기사 내 이미지 갤러리 — full-bleed / caption / credit-line"},
        {"name": "subscription-callout", "family": "magazine", "role": "구독 유도 callout — bold offer copy + CTA, article 하단 / sidebar"},
    ],
    "opinion long-form": [
        {"name": "opinion-byline", "family": "magazine", "role": "opinion 필자 byline — 필자 이름 + 직함 + 사진 + SNS 링크"},
        {"name": "manifesto-section", "family": "magazine", "role": "매니페스토/선언 섹션 — bold declaration 문단 + saturated accent surface"},
        {"name": "feature-grid-index", "family": "magazine", "role": "issue feature 목차 그리드 — number-heavy tile + kicker + title + byline"},
        {"name": "archive-index", "family": "magazine", "role": "전체 아카이브 인덱스 — year/issue 필터 + list"},
        {"name": "issue-archive", "family": "magazine", "role": "과거 이슈 아카이브 — cover thumbnail + issue number + publish date"},
        {"name": "reading-progress-bar", "family": "feedback", "role": "article 상단 reading progress bar — long-form prose scroll 위치 추적, heading-anchor 진행 하이라이트"},
        {"name": "credit-line", "family": "magazine", "role": "article 하단 credit line — 사진/일러스트/에디터 크레딧, mono"},
    ],
    "editorial curation dashboard": [
        {"name": "curation-queue", "family": "dashboard-editorial", "role": "sidebar-nav + data-table + filter-chip + kpi-card 기반 editorial 큐레이션 큐 — 초안 후보 row, draft-status-pill, 기고자 avatar, 예정 스케줄, row-actions, warm neutral row + Naples Yellow hover, column-header sort"},
        {"name": "editorial-calendar", "family": "dashboard-editorial", "role": "편집 캘린더 그리드 — schedule cell · 이슈/호 · 섹션 라벨 · sidebar-nav 진입, data-table row 와 연계, filter-chip 으로 기고자/섹션 필터"},
        {"name": "draft-status-pill", "family": "data-display", "role": "초안 상태 pill — 아이디어/초안/리뷰/스케줄/발행/보류/아카이브, data-table row + curation-queue card 내 status-badge 변형"},
        {"name": "article-preview-pane", "family": "dashboard-editorial", "role": "curation-queue row 또는 editorial-calendar schedule cell 클릭 시 우측 slide-in reading drawer — article-body 미리 보기, byline, draft-status-pill, comment-thread, long-form Pretendard"},
        {"name": "contributor-roster", "family": "dashboard-editorial", "role": "기고자 명단 data-table — 프로필 avatar · 소속 · 기고 섹션 · 최근 활동 · 읽기 수, sidebar-nav 진입 + filter-chip, profile-card drawer"},
        {"name": "editorial-analytics-kpi", "family": "dashboard-editorial", "role": "편집 운영 kpi-card 스택 — 이슈 리드 타임 · 리뷰 처리 · 발행 지연율 · 기고자당 발행 수, mono tabular-nums, sidebar-nav 진입"},
        {"name": "reading-analytics-kpi", "family": "dashboard-editorial", "role": "리딩 kpi-card 스택 — 평균 체류 · 완독률 · 스크롤 심도 · 메일 오픈, Naples Yellow trend indicator, chart-container 연계"},
        {"name": "archive-shelf", "family": "dashboard-editorial", "role": "과거 이슈 / 발행 기사 아카이브 — filter-sidebar + data-table + kpi-card 조합, issue-number chip, 태그 필터, sidebar-nav 진입"},
        {"name": "tag-taxonomy-manager", "family": "dashboard-editorial", "role": "섹션/카테고리/태그 체계 편집 — tree + data-table + modal-dialog, sidebar-nav 진입, muted warm divider"},
    ],
    "publishing workflow": [
        {"name": "publishing-pipeline", "family": "dashboard-editorial", "role": "수평 publishing 파이프라인 보드 — pipeline-stage column (아이디어 → 초안 → 리뷰 → 스케줄 → 발행 → 아카이브), data-table 연계, sidebar-nav 진입, filter-chip 필터, article-preview-pane drawer 연계"},
        {"name": "issue-planner", "family": "dashboard-editorial", "role": "분기/연간 호 플래너 — 이슈 row · 섹션 cell · 책임 편집자 avatar · 발행 예정, sidebar-nav + data-table + filter-chip 진입, kpi-card 요약"},
        {"name": "pipeline-stage", "family": "dashboard-editorial", "role": "publishing-pipeline 단계 column — active/완료/대기 상태, draft-status-pill, row-actions, filter-chip + sort-dropdown 연계"},
        {"name": "schedule-cell", "family": "dashboard-editorial", "role": "editorial-calendar 그리드 날짜 cell — 이슈/섹션/기고자/draft-status-pill 표시, focus-glow, article-preview-pane 진입"},
        {"name": "editorial-workflow", "family": "dashboard-editorial", "role": "편집 workflow 진행 stepper — sidebar-nav 상단 stage indicator, kpi-card 연계"},
        {"name": "assign-reviewer", "family": "input", "role": "리뷰어 지정 — mention-chip / avatar-cluster 기반 picker, profile-card 미리 보기, data-table row-actions 로 진입"},
        {"name": "publish-scheduler", "family": "input", "role": "발행 스케줄러 — date-picker + time-picker 조합, sidebar-nav + filter-chip 진입, draft-status-pill 전환"},
        {"name": "content-status-timeline", "family": "data-display", "role": "article status 타임라인 — 아이디어 → 초안 → 리뷰 → 스케줄 → 발행 이벤트 stream, mono timestamp, data-table 연계"},
    ],
    "growth analytics admin": [
        {"name": "activation-funnel", "family": "dashboard-growth", "role": "B2C 스타트업 activation 4–6 stage funnel — sidebar-nav 진입 + kpi-card summary + filter-chip (세그먼트/기간), stage 별 drop-off 퍼센트 mono tabular-nums, vivid primary active stage + muted drop-off, data-table row drill-down"},
        {"name": "cohort-matrix", "family": "dashboard-growth", "role": "주간/일간 cohort retention matrix — data-table row · heat-scale cell · filter-chip 연계, sidebar-nav 진입, cell hover 시 tooltip + user-list 드릴, mono tabular-nums"},
        {"name": "referral-widget", "family": "dashboard-growth", "role": "referral share CTA 카드 — kpi-card (referrals · viral coefficient · k-factor) + share-link + reward tracker, saturated accent primary CTA, sidebar-nav 진입, filter-chip 필터"},
        {"name": "retention-chart", "family": "dashboard-growth", "role": "retention curve line/area chart — chart-container 안, filter-chip (기간/세그먼트) 연계, kpi-card 요약, sidebar-nav 진입"},
        {"name": "conversion-funnel", "family": "dashboard-growth", "role": "marketing/commerce conversion funnel — 4 stage, stage drop-off rate mono, filter-chip + segment-filter + kpi-card 연계"},
        {"name": "experiment-panel", "family": "dashboard-growth", "role": "A/B experiment variant card grid — variant + uplift + confidence + winner badge, data-table row 스타일, sidebar-nav + filter-chip 진입, kpi-card 요약"},
        {"name": "goal-tracker", "family": "dashboard-growth", "role": "목표 progress bar + 완료 체크 — kpi-card 내 progress variant, saturated accent complete, sidebar-nav 진입, filter-chip 기간 필터, data-table 요약"},
        {"name": "user-list", "family": "dashboard-growth", "role": "user data-table — rounded avatar + email + signup + segment tag-pill + last-active + row-actions, sidebar-nav 진입, filter-chip + segment-filter 연계"},
        {"name": "ticket-queue", "family": "dashboard-growth", "role": "지원 티켓 data-table queue — status-badge + priority + assignee + last-activity, row-actions, sidebar-nav 진입, filter-chip 필터"},
        {"name": "alert-list", "family": "dashboard-growth", "role": "incident / alert list — severity + source + ack 버튼 + saturated danger, data-table row, sidebar-nav 진입, filter-chip 필터, kpi-card 요약"},
        {"name": "segment-filter", "family": "input", "role": "세그먼트 필터 dropdown — saved-segment + new-segment, filter-chip 연계, sidebar-nav 필터 bar"},
        {"name": "filter-bar", "family": "navigation", "role": "상단 sticky filter bar — filter-chip + segment-filter + search-field 통합, dashboard section 별 컨텍스트"},
    ],
    "wellness habit tracking": [
        {"name": "dashboard-card", "family": "dashboard-wellness", "role": "consumer wellness admin soft rounded dashboard card — Periwinkle hairline + Mauve hover, sidebar-nav 진입, kpi-card 래퍼, insight-card 컨테이너, dashboard 섹션 wrap, data-table row 연계, filter-chip 필터 컨테이너"},
        {"name": "streak-indicator", "family": "dashboard-wellness", "role": "연속 habit/wellness streak pill indicator — kpi-card 내 mini, Peach Puff flame + mono days + Periwinkle ring, sidebar-nav 진입 + filter-chip 기간 필터, dashboard-card 단위, data-table row 진입 드릴-다운"},
        {"name": "habit-calendar", "family": "dashboard-wellness", "role": "habit week×day calendar grid — heat-scale cell (완료 Periwinkle deepest → empty Mauve lightest), today cell Peach Puff ring, sidebar-nav 진입, filter-chip 필터, data-table row 연계, kpi-card 요약, dashboard-card wrapper"},
        {"name": "wellness-score", "family": "dashboard-wellness", "role": "wellness score gauge/ring — kpi-card 진입, Periwinkle base + Peach Puff highlight + mono score, sidebar-nav 진입, filter-chip 기간 필터, soft radial gradient, data-table row 연계, dashboard-card wrapper"},
        {"name": "mood-check", "family": "dashboard-wellness", "role": "mood quick-select emoji/color gradient — kpi-card 카드 내, Peach Puff happy → Periwinkle calm → Mauve thoughtful → soft neutral low, sidebar-nav 진입, filter-chip 기간 필터, data-table row 진입"},
        {"name": "mood-chart", "family": "dashboard-wellness", "role": "mood 시계열 chart — chart-container 안, kpi-card 연계, filter-chip (기간/세그먼트) 필터, sidebar-nav 진입, data-table row 진입, dashboard-card wrapper"},
        {"name": "session-tracker", "family": "dashboard-wellness", "role": "명상/수면/운동 session card — dashboard-card 단위, 지속 시간 mono + Peach Puff complete pill + kpi-card 요약, sidebar-nav 진입, filter-chip 필터, data-table row 진입"},
        {"name": "session-timeline", "family": "dashboard-wellness", "role": "하루 session timeline — 시간대별 block stack, dashboard-card 안, rounded, kpi-card 요약, sidebar-nav 진입, filter-chip 기간 필터, data-table row 연계"},
        {"name": "goal-grid", "family": "dashboard-wellness", "role": "여러 goal-tracker card grid — dashboard-card wrapper, rounded, kpi-card 요약, sidebar-nav 진입, filter-chip 필터, data-table row 연계"},
    ],
}

# 모든 프로젝트에 기본으로 포함되는 컴포넌트
BASELINE_COMPONENTS: list[dict] = [
    {"name": "primary-button", "family": "button", "role": "주요 행동을 유도하는 CTA 버튼"},
    {"name": "secondary-button", "family": "button", "role": "보조 행동 버튼"},
    {"name": "ghost-button", "family": "button", "role": "최소한의 시각적 무게를 가진 버튼"},
    {"name": "icon-button", "family": "button", "role": "아이콘만 있는 액션 버튼"},
    {"name": "link-button", "family": "button", "role": "텍스트 링크 스타일 버튼"},
]


def analyze_spec(spec_text: str) -> list[dict]:
    text_lower = spec_text.lower()
    detected: list[dict] = []

    for pattern_name, config in UI_PATTERNS.items():
        matches: list[str] = []
        for term in config["terms"]:
            if term.lower() in text_lower:
                occurrences = len(re.findall(re.escape(term.lower()), text_lower))
                matches.extend([term] * occurrences)

        if matches:
            unique_terms = sorted(set(matches))
            detected.append({
                "pattern": pattern_name,
                "confidence": len(matches),
                "matched_terms": unique_terms,
                "description": config["description"],
                "components": PATTERN_COMPONENTS.get(pattern_name, []),
            })

    detected.sort(key=lambda x: x["confidence"], reverse=True)
    return detected


def analyze_spec_file(spec_path: Path) -> list[dict]:
    text = spec_path.read_text(encoding="utf-8")
    return analyze_spec(text)


def build_component_list(detected_patterns: list[dict]) -> list[dict]:
    seen: set[str] = set()
    components: list[dict] = []

    for comp in BASELINE_COMPONENTS:
        if comp["name"] not in seen:
            seen.add(comp["name"])
            components.append({**comp, "source": "baseline"})

    for pattern in detected_patterns:
        for comp in pattern["components"]:
            if comp["name"] not in seen:
                seen.add(comp["name"])
                components.append({**comp, "source": pattern["pattern"]})

    return components


def detected_to_primitives(detected_patterns: list[dict]) -> list[str]:
    return [p["pattern"] for p in detected_patterns]
