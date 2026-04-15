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
