# Ledger System Spec

## 1. Positioning

- **Brand**: Ledger
- **Product**: 기업·금융팀을 위한 콘서버티브/신뢰 톤의 핀테크 운영 대시보드 — 거래/잔고/컴플라이언스 콘솔
- **Audience**: 기업 재무/회계 담당자, 핀테크 운영/컴플라이언스 팀, B2B SaaS 프로덕트 매니저
- **Platforms**: web, desktop
- **Accessibility floor**: WCAG 2.2 AA

## 2. Identity Guardrails

- **Brand keywords**: corporate, trust, fintech, financial, conservative, enterprise, compliance, institutional
- **Anti-keywords**: playful, decorative, saturated neon, bold casual, experimental
- **Tone of voice**: professional, trustworthy, precise, formal
- **Visual direction**: navy/deep blue primary, muted secondary, dense data hierarchy, restrained accent, thin borders, clear whitespace, numeric-first layout
- **Interaction direction**: keyboard-friendly, predictable states, low-noise motion, audit-trail affordances, dense table filters

## 3. Design Principles

- **Corporate**: `corporate`를 시각적 선택과 인터랙션 선택의 기본 기준으로 삼습니다.
- **Trust**: `trust`를 시각적 선택과 인터랙션 선택의 기본 기준으로 삼습니다.
- **Fintech**: `fintech`를 시각적 선택과 인터랙션 선택의 기본 기준으로 삼습니다.
- **Financial**: `financial`를 시각적 선택과 인터랙션 선택의 기본 기준으로 삼습니다.

## 4. Foundation Priorities

- **Grid, container, and page rhythm** (high): signal 42
- **Content design and microcopy rules** (high): signal 36
- **Accessibility rules and contrast baseline** (high): signal 35
- **Color tokens and semantic color policy** (high): signal 35
- **Icon family and stroke policy** (high): signal 30

## 5. Token Strategy

- **Layering**: core -> semantic -> component
- **Core categories**: color, spacing, radius, typography, motion, elevation
- **Semantic categories**: surface, text, border, focus, feedback
- **Component categories**: button, input, navigation, overlay, editor
- **Typography families**: brand, text, mono
- **Spacing scale**: 0, 2, 4, 8, 12, 16, 24, 32, 48, 64, 96

### Typography System (auto-resolved)

- **Heading**: Pretendard
- **Body**: Pretendard
- **Korean**: Pretendard
- **Mono**: IBM Plex Mono
- **Product type detected**: enterprise
- **Pairing source**: auto-scored
- **Line height**: normal
- **Type scale**: base 15px, ratio 1.25 (xs=12px, sm=13px, md=15px, lg=19px, xl=24px, 2xl=30px, 3xl=37px)
- **Strategy**:
  - 단일 서체(Pretendard)로 weight 대비 위계 — 일관성 우선
  - 한글 서체: Pretendard — 라틴과 x-height/weight 조화
  - 모노스페이스: IBM Plex Mono — 코드/데이터 영역 전용
- **Heading note**: 한글 UI 서체의 사실상 표준. Apple SD Gothic Neo 기반이지만 더 정교함. 라틴은 Inter 계열.
- **Body note**: 한글 UI 서체의 사실상 표준. Apple SD Gothic Neo 기반이지만 더 정교함. 라틴은 Inter 계열.
- **Korean rationale**: Pretendard — 한글 UI 서체의 사실상 표준. 토스, 당근, 리디 등 국내 주요 서비스에서 사용. 자간이 자연스럽고 weight 전 구간에서 안정적.
- **Heading tracking**: xl=-0.01em, 2xl=-0.02em, 3xl=-0.02em
- **Primary script**: korean
- **Hangul headline defaults**: Pretendard | line-height 1.25-1.35 | tracking 0em
- **Hangul body defaults**: Pretendard | line-height 1.6-1.7 | label line-height 1.4-1.5
- **Wrap defaults**: headline word-break=keep-all, headline text-wrap=balance, body word-break=keep-all
- **Scale guidance**: 기본 스케일을 사용할 수 있지만 한글 문장 기준으로 실제 wrap을 먼저 검증한다.
- **Loading**: Pretendard(preload), IBM Plex Mono(lazy) | display: swap

## 6. Color Reference

- **Source**: REFERENCE X Vol.1 - Color Reference (/Users/sungwoon/ai-projects/design-ontology-harness/docs/color-reference.md)
- **Selection mode**: manual
- **Preferred families**: Deep Blues, Pantone Trend Blues, Natural Blues, Pastel Blues
- **Palette strategy**: temperature=mixed, contrast=balanced, diversity=balanced, surface_style=tinted
- **Palette expansion**: supporting_color_count=10, combination_count=3, prefer_pairings=True
- **Palette roles**:
  - `primary` -> Prussian Blue #003153 / Deep Blues
  - `accent` -> Bronze Gold #A97132 / Deep Yellows
  - `surface_tint` -> Ice Blue #D6EAF8 / Pastel Blues
- **Selected colors**:
  - Navy Blue #000080 / Deep Blues / 저명도, 중채도, 차가운 온도감이 강한 블루 계열 / 신뢰, 권위, 집중, 전문성, 절제된 우아함
  - Classic Blue #0F4C81 / Pantone Trend Blues / 중명도, 중채도, 클래식한 딥 블루 톤 / 신뢰, 평온함, 지성, 안정감
  - Misty Blue #B5C7EB / Pastel Blues / 중명도, 저채도, 보라색이 섞인 뉴트럴 블루 톤 / 차분함, 사색적, 몽환적, 잔잔함, 감정의 여운
- **Palette candidates**:
  - signature-1 (Signature): primary=Navy Blue, accent=Classic Blue, surface_tint=Misty Blue / Navy Blue is inside preferred families.; Classic Blue is inside preferred families.
  - soft-spread-2 (Soft Spread): primary=Navy Blue, accent=Classic Blue, surface_tint=Ice Blue / Navy Blue is inside preferred families.; Classic Blue is inside preferred families.
  - assertive-3 (Assertive): primary=Navy Blue, accent=Classic Blue, surface_tint=Sky Blue / Navy Blue is inside preferred families.; Classic Blue is inside preferred families.
- **Expanded supporting colors**:
  - Pairing #B8CBD0 #B8CBD0 / Derived Pairing / pairing-swatch / Pairing #B8CBD0 comes from the seed pairing references.; Pairing #B8CBD0 is explicitly paired with Prussian Blue.
  - Pairing #1C2E4A #1C2E4A / Derived Pairing / pairing-swatch / Pairing #1C2E4A comes from the seed pairing references.; Pairing #1C2E4A is explicitly paired with Bronze Gold.
  - Pairing #2E4E68 #2E4E68 / Derived Pairing / pairing-swatch / Pairing #2E4E68 comes from the seed pairing references.; Pairing #2E4E68 is explicitly paired with Ice Blue.
  - Pairing #F5F3E7 #F5F3E7 / Derived Pairing / pairing-swatch / Pairing #F5F3E7 comes from the seed pairing references.; Pairing #F5F3E7 is explicitly paired with Prussian Blue.
  - Pairing #C0C0C0 #C0C0C0 / Derived Pairing / pairing-swatch / Pairing #C0C0C0 comes from the seed pairing references.; Pairing #C0C0C0 is explicitly paired with Ice Blue.
  - Pairing #3E3E3E #3E3E3E / Derived Pairing / pairing-swatch / Pairing #3E3E3E comes from the seed pairing references.; Pairing #3E3E3E is explicitly paired with Ice Blue.
  - Pairing #4A4A4A #4A4A4A / Derived Pairing / pairing-swatch / Pairing #4A4A4A comes from the seed pairing references.; Pairing #4A4A4A is explicitly paired with Bronze Gold.
  - Pairing #8A8E80 #8A8E80 / Derived Pairing / pairing-swatch / Pairing #8A8E80 comes from the seed pairing references.; Pairing #8A8E80 is explicitly paired with Prussian Blue.
- **Expanded semantic roles**:
  - `brand_primary` -> Prussian Blue #003153 / Deep Blues
  - `brand_accent` -> Bronze Gold #A97132 / Deep Yellows
  - `surface_tint` -> Ice Blue #D6EAF8 / Pastel Blues
  - `canvas` -> Canvas White #F7F8FA / Generated Fallback
  - `surface` -> Paper #FFFFFF / Generated Fallback
  - `surface_muted` -> Surface Muted #EEF1F6 / Generated Fallback
  - `surface_elevated` -> Paper #FFFFFF / Generated Fallback
  - `border` -> Border Neutral #D6DDE6 / Generated Fallback
  - `border_strong` -> Pairing #B8CBD0 #B8CBD0 / Derived Pairing
  - `ink` -> Pairing #1C2E4A #1C2E4A / Derived Pairing
- **Combination lists**:
  - Seed Core: primary=Prussian Blue, accent=Bronze Gold, surface_tint=Ice Blue
  - Surface System: canvas=Canvas White, surface=Paper, surface_tint=Ice Blue, border=Border Neutral, ink=Pairing #1C2E4A, ink_muted=Muted Ink
  - Support Spectrum: support=Pairing #B8CBD0, support=Pairing #1C2E4A, support=Pairing #2E4E68, support=Pairing #F5F3E7, support=Pairing #C0C0C0, support=Pairing #3E3E3E
- **Notes**: Prussian Blue 를 primary 로 — 금융/공공 기관 신뢰감, Bronze Gold 액센트로 클래식/프리미엄 감도 보조, Ice Blue 는 surface_tint — 데이터 밀도 높은 표에서 피로감 최소화, dark mode 1급 지원 — 야간 운영/모니터링 환경, semantic feedback(success/warn/danger/info) 별도 role, 과포화 금지
- **Application rule**: 레퍼런스 컬러는 semantic token으로 번역해서 사용하고, 접근성과 theme 호환성을 우선합니다.

## 7. Visual Reference Signals

- **Mode**: local-images
- **Coverage**: source 0 / image 0 / selected 0
- **Rule**: visual references are advisory signals for motif and layout direction; official KB/spec remain the structural source of truth.
- **Provenance**: `observed` = directly measured from local pixels, `inferred` = synthesized from image/query/brand signals, `unverified` = reliable visual evidence not yet available.
- **Query seeds**: enterprise fintech dashboard navy, stripe dashboard transactions table, brex admin reporting, conservative banking UI
### Visual Direction

- **Density**: dense (confidence 0.94, provenance inferred) / dashboard x2, table x4
- **Surface Style**: flat (confidence 0.24, provenance inferred) / fallback=flat
- **Corner Style**: medium (confidence 0.29, provenance inferred) / card x1
- **Typography Mood**: utilitarian (confidence 0.92, provenance inferred) / dashboard x2, admin x1, enterprise x2
- **Color balance**: temperature=unknown, contrast=unknown, neutral_bias=unknown, provenance=unverified

### Layout Rhythm

- **Dashboard grid**: confidence 0.94 / provenance inferred / dashboard x2, kpi x2, table x4
- **Data review surface**: confidence 0.94 / provenance inferred / table x4, audit x2, data x1, filter x1
- **Split-pane workspace**: confidence 0.94 / provenance inferred / workspace x1, sidebar x2, panel x1, navigation x1

### Image-derived Component Hints

- **Cards**: flat card planes를 기본으로 하고, 압축된 spacing과 얇은 divider 중심의 hierarchy. 중간 반경으로 제품 UI 절제 유지. / provenance inferred / surface=flat, density=dense, corner=medium
- **Navigation**: 고정 sidebar 또는 split-pane navigation을 우선하고, 현재 위치와 scope를 항상 명시한다. / provenance inferred / Split-pane workspace
- **Typography**: 정보 밀도에 맞춰 type scale 차이를 줄이고 table/list label의 정렬 정확도를 우선한다. / provenance inferred / typography_mood=utilitarian
- **Data Display**: 정보 밀도를 유지하되 thin dividers와 restrained accent로 hierarchy를 만든다. / provenance inferred / layout=dashboard-grid, density=dense

### Synthesis Notes

- layout는 Dashboard grid 기준으로 정리
- surface language는 flat 성향 우선
- typography mood는 utilitarian 축 유지
- density는 dense 기준으로 primitive spacing 조정
- palette temperature는 unknown 쪽을 우선
- Avoid: glassmorphism
- Avoid: gradient-heavy surfaces
- Avoid: playful illustrations

## 8. Component Strategy

- **Product primitives**: sidebar navigation, workspace switcher, transactions table, balance kpi card, compliance banner, alert list, audit timeline, filter chrome, status badge, date range picker, member roster, settings panel
- **Required families**: button, data-display, feedback, input, navigation, overlay
- **Visual-reference archetypes**:

- **Dashboard insight module** (data-display / 0.94): stat-card, insight-card, chart-panel, section-header, filter-chip
- **Data review table** (data-display / 0.94): data-table, column-header, row-actions, filter-toolbar, pagination
- **Workspace shell** (navigation / 0.94): app-shell, sidebar-nav, workspace-switcher, breadcrumb, context-panel
- **Conversation sidecar** (overlay / 0.57): chat-panel, message-thread, message-composer, context-drawer

- **button**: primary-button, secondary-button, ghost-button, icon-button, cta-button, link-button, form-actions
- **data-display**: data-table, column-header, row-actions, stat-card, insight-card, activity-card, section-header, kanban-board / visual signals: Dashboard insight module (0.94), Data review table (0.94)
- **feedback**: inline-alert, empty-state, toast, banner, status-badge, upload-progress, step-progress
- **input**: text-field, search-field, segmented-control, filter-chip, chip, textarea, select, checkbox
- **navigation**: mobile-topbar, mobile-tab-bar, back-button, section-tabs, pagination, app-shell, sidebar-nav, topbar / visual signals: Workspace shell (0.94)
- **overlay**: bottom-sheet, modal-dialog, user-menu, autocomplete, chart-tooltip, confirm-dialog, tooltip-guide, chat-panel / visual signals: Conversation sidecar (0.57)

## 9. Implementation Guardrails

- 기존 핵심 화면, 진입점, 작업 흐름은 명시적 승인 없이 제거하거나 숨기지 않음
- 전면 셸 리라이트보다 토큰 -> primitive -> feature surface 순서의 점진적 롤아웃을 우선
- 새 시각 규칙은 지원 대상 테마와 breakpoint 전체에서 먼저 검증
- 기존 데이터 밀도와 업무 완료 경로를 유지한 상태에서 시각 품질을 높이는 방향을 우선
- 기능 위치 변경, 정보 구조 변경, 패널 제거는 별도의 migration plan이 있을 때만 수행
- 아이콘 자리에 이모지(🎨 ✅ 🔥 등)를 넣지 않음 — SVG 아이콘 또는 아이콘 라이브러리만 사용
- 컴포넌트는 component_specs.md의 anatomy/states/token binding을 그대로 따라 완전히 구현
- 'TODO 컴포넌트', '임시 버튼', '플레이스홀더 카드' 같은 반쪽 구현을 남기지 않음

## 10. Reference Absorption Rule

- Analysed live reference sources: 3
- Rule: copy visuals from no single source; absorb patterns only when they reinforce brand keywords and avoid anti-keywords.
- Use references to validate structure, accessibility, token discipline, and documentation quality.

## 11. AI Synthesis Principles

- **hex를 만들지 않는다**: AI는 색상 hex 값을 임의로 생성하지 않는다. 반드시 color_reference, CSS 추출, 브랜드 가이드 등 실증 소스에서 가져온 값만 사용한다.
- **토큰명을 만들지 않는다**: AI는 토큰 이름을 임의로 발명하지 않는다. 네이밍 패턴(core/semantic/component 레이어 규칙)은 정의하되, 구체적 토큰명은 실제 컴포넌트와 역할에서 도출한다.
- **팩트 위에 해석만**: AI는 수집된 레퍼런스, 프로필, 온톨로지 증거 위에 해석과 구조화만 수행한다. 증거 없는 추론, 존재하지 않는 패턴 서술, 가상의 사용 사례 생성을 금지한다.
- **이모지를 UI 요소로 쓰지 않는다**: AI는 아이콘, 상태 표시, 버튼 장식, 네비게이션 지표 등 UI 컴포넌트 자리에 이모지(🎨 ✅ 🔥 ⚡ 🚀 ❌ ⭐ 📊 등)를 절대 넣지 않는다. 반드시 SVG 아이콘 컴포넌트를 직접 구현하거나, 아이콘 라이브러리(Lucide, Heroicons, Phosphor, Tabler 등)를 import해서 사용한다. 이모지는 본문 콘텐츠(예: 블로그 텍스트, 사용자 입력)에서만 허용되며, 시스템 UI 요소로는 금지한다. 이 규칙은 AI가 UI를 만들 때 가장 자주 저지르는 실수이므로 엄격히 적용한다.
- **컴포넌트를 직접 구현한다**: AI는 '임시 버튼', '플레이스홀더 카드', 'TODO 컴포넌트' 같은 반쪽 구현을 남기지 않는다. system_spec.md의 Component Strategy와 component_specs.md에 정의된 구조(anatomy), 상태(states), 토큰 바인딩, 접근성 규칙을 그대로 따라 완전한 컴포넌트를 구현한다. 기존 라이브러리 컴포넌트를 그냥 import해서 쓰는 대신, 디자인 시스템 토큰으로 스타일을 명시적으로 바인딩한다.

## 12. Ontology Targets

- **component**: 121
- **design_system**: 68
- **layout**: 42
- **content**: 36
- **accessibility**: 35
- **color**: 35
- **pattern**: 35
- **iconography**: 30

## 13. Profile Validation

- Warning: [pitfall#3-rebrand] Navy Blue vs Misty Blue (blue): lightness diff 56, saturation diff 43 — possible rebrand remnant
- Warning: [pitfall#3-rebrand] Classic Blue vs Misty Blue (blue): lightness diff 53, saturation diff 22 — possible rebrand remnant
- Warning: visual_reference.sources is empty

## 14. Quick Start

이 문서는 **Ledger System**의 디자인 시스템 사양입니다.

### 시작하기

1. **토큰 적용**: Drop-in CSS(아래 섹션 16)의 CSS 변수를 프로젝트에 복사합니다.
2. **컬러 세팅**: Color Reference(섹션 6)의 semantic role을 기준으로 surface/text/border를 잡습니다.
3. **타이포 세팅**: Token Strategy(섹션 5)의 font family와 type scale을 적용합니다.
4. **시각 방향 확인**: Visual Reference Signals(섹션 7)에서 density/surface/layout cue를 먼저 확인합니다.
5. **컴포넌트 구현**: Component Strategy(섹션 8)의 family 순서대로 하나씩 빌드합니다.

### 우선순위

핵심 primitive: **sidebar navigation, workspace switcher, transactions table, balance kpi card, compliance banner**

이 primitive를 지원하는 컴포넌트부터 구현하고, 나머지는 필요에 따라 확장합니다.

## 15. DO / DON'T

### DO

- **Corporate**: corporate와 충돌하는 컴포넌트 변형은 만들지 않기
- **Trust**: trust와 충돌하는 컴포넌트 변형은 만들지 않기
- **Fintech**: fintech와 충돌하는 컴포넌트 변형은 만들지 않기
- **Financial**: financial와 충돌하는 컴포넌트 변형은 만들지 않기
- 모든 시각적 선택에서 **corporate, trust, fintech** 기준을 적용
- semantic token을 통해 컬러를 적용 (하드코딩 금지)
- 접근성 기준을 모든 text/surface 조합에서 먼저 검증
- 컴포넌트 변형 추가 전 기존 variant로 해결 가능한지 먼저 확인
- 아이콘은 SVG 컴포넌트 또는 Lucide/Heroicons/Phosphor/Tabler 등 라이브러리로 구현
- component_specs.md의 anatomy/states/token binding을 그대로 따라 완전히 구현

### DON'T

- **playful** 방향의 디자인 결정을 하지 않음
- **decorative** 방향의 디자인 결정을 하지 않음
- **saturated neon** 방향의 디자인 결정을 하지 않음
- **bold casual** 방향의 디자인 결정을 하지 않음
- hex 값을 임의로 생성하지 않음 (반드시 레퍼런스에서 가져오기)
- 토큰명을 임의로 발명하지 않음 (네이밍 패턴에서 도출)
- 한 레퍼런스의 비주얼을 그대로 복제하지 않음
- 기존 기능 진입점을 승인 없이 제거하지 않음
- **이모지(🎨 ✅ 🔥 ⚡ 🚀 ❌ ⭐ 📊 등)를 아이콘/버튼/상태 표시로 절대 쓰지 않음** — 본문 콘텐츠에만 허용
- '임시 버튼', 'TODO 컴포넌트', '플레이스홀더 카드' 같은 반쪽 구현을 남기지 않음
- 라이브러리 컴포넌트를 기본 스타일로 그냥 쓰지 않음 — 반드시 디자인 토큰으로 스타일 바인딩

## 16. Drop-in CSS

아래 CSS 변수를 `:root`에 복사하여 즉시 사용할 수 있습니다.

```css
:root {
  /* --- Spacing --- */
  --space-0: 0px;
  --space-2: 2px;
  --space-4: 4px;
  --space-8: 8px;
  --space-12: 12px;
  --space-16: 16px;
  --space-24: 24px;
  --space-32: 32px;
  --space-48: 48px;
  --space-64: 64px;
  --space-96: 96px;

  /* --- Radius --- */
  --radius-none: 0;
  --radius-sm: 4px;
  --radius-md: 8px;
  --radius-lg: 12px;
  --radius-xl: 16px;
  --radius-pill: 9999px;

  /* --- Typography --- */
  --font-heading: 'Pretendard', serif;
  --font-body: 'Pretendard', sans-serif;
  --font-mono: 'IBM Plex Mono', monospace;
  --text-xs: 12px;
  --text-sm: 13px;
  --text-md: 15px;
  --text-lg: 19px;
  --text-xl: 24px;
  --text-2xl: 30px;
  --text-3xl: 37px;

  --leading-tight: 1.25;
  --leading-normal: 1.45;
  --leading-comfortable: 1.55;
  --leading-relaxed: 1.65;

  /* --- Color (from reference) --- */
  --color-primary: #003153;
  --color-accent: #A97132;
  --color-surface-tint: #D6EAF8;

  /* --- Semantic roles (expanded) --- */
  --color-brand-primary: #003153;
  --color-brand-accent: #A97132;
  --color-surface-tint: #D6EAF8;
  --color-canvas: #F7F8FA;
  --color-surface: #FFFFFF;
  --color-surface-muted: #EEF1F6;
  --color-surface-elevated: #FFFFFF;
  --color-border: #D6DDE6;
  --color-border-strong: #B8CBD0;
  --color-ink: #1C2E4A;
  --color-ink-muted: #4B5563;
  --color-ink-subtle: #8A8E80;
  --color-ink-inverse: #FFFFFF;
  --color-primary-support: #B8CBD0;
  --color-accent-support: #F5F3E7;
  --color-info: #B8CBD0;
  --color-success: #4A7C59;
  --color-warning: #A97132;
  --color-danger: #D4A6A6;
  --color-link: #003153;
  --color-link-hover: #00192A;

  /* --- Button — primary --- */
  --color-button-primary-surface-default: #003153;
  --color-button-primary-surface-hover: #001F34;
  --color-button-primary-surface-active: #001320;
  --color-button-primary-surface-disabled: #94A8B7;
  --color-button-primary-text-default: #FFFFFF;
  --color-button-primary-text-disabled: #FBFCFC;
  --color-button-primary-border-default: #003153;
  --color-button-primary-focus-ring: #003153;

  /* --- Button — secondary --- */
  --color-button-secondary-surface-default: #FFFFFF;
  --color-button-secondary-surface-hover: #F1F2F4;
  --color-button-secondary-surface-active: #E8EAED;
  --color-button-secondary-surface-disabled: #F7F8FA;
  --color-button-secondary-text-default: #1C2E4A;
  --color-button-secondary-text-disabled: #949DAB;
  --color-button-secondary-border-default: #BDC8D7;
  --color-button-secondary-border-hover: #A3B3C7;
  --color-button-secondary-focus-ring: #003153;

  /* --- Button — ghost --- */
  --color-button-ghost-surface-default: transparent;
  --color-button-ghost-surface-hover: #F4F5F6;
  --color-button-ghost-surface-active: #EBECEF;
  --color-button-ghost-surface-disabled: transparent;
  --color-button-ghost-text-default: #4B5563;
  --color-button-ghost-text-hover: #1C2E4A;
  --color-button-ghost-text-disabled: #AAAFB6;
  --color-button-ghost-border-default: transparent;
  --color-button-ghost-focus-ring: #003153;

  /* --- Button — danger --- */
  --color-button-danger-surface-default: #D4A6A6;
  --color-button-danger-surface-hover: #CA9191;
  --color-button-danger-surface-active: #C38484;
  --color-button-danger-text-default: #1C2E4A;
  --color-button-danger-border-default: #D4A6A6;
  --color-button-danger-focus-ring: #D4A6A6;

  /* --- Input --- */
  --color-input-surface-default: #FFFFFF;
  --color-input-surface-filled: #FFFFFF;
  --color-input-surface-disabled: #F7F8FA;
  --color-input-text-default: #1C2E4A;
  --color-input-text-placeholder: #90969F;
  --color-input-text-disabled: #AAAFB6;
  --color-input-border-default: #D6DDE6;
  --color-input-border-hover: #B6C3D3;
  --color-input-border-focus: #003153;
  --color-input-border-error: #D4A6A6;
  --color-input-border-disabled: #E6EAF0;

  /* --- Card --- */
  --color-card-surface-default: #FFFFFF;
  --color-card-surface-hover: #FAFBFB;
  --color-card-surface-muted: #F7F8FA;
  --color-card-border-default: #D6DDE6;
  --color-card-border-hover: #B6C3D3;
  --color-card-border-focus: #003153;

  /* --- Nav link --- */
  --color-nav-link-text-default: #4B5563;
  --color-nav-link-text-hover: #1C2E4A;
  --color-nav-link-text-active: #003153;
  --color-nav-link-surface-hover: #F6F7F8;
  --color-nav-link-indicator: #A97132;

  /* --- Link --- */
  --color-link-text-default: #003153;
  --color-link-text-hover: #001320;
  --color-link-text-visited: #062134;

  /* --- Feedback — info --- */
  --color-feedback-info-surface: #F6F9F9;
  --color-feedback-info-text: #B8CBD0;
  --color-feedback-info-border: #CBD8DD;
  --color-feedback-info-icon: #B8CBD0;

  /* --- Feedback — success --- */
  --color-feedback-success-surface: #E9EFEB;
  --color-feedback-success-text: #4A7C59;
  --color-feedback-success-border: #7EA189;
  --color-feedback-success-icon: #4A7C59;

  /* --- Feedback — warning --- */
  --color-feedback-warning-surface: #F5EEE6;
  --color-feedback-warning-text: #A97132;
  --color-feedback-warning-border: #C09A6E;
  --color-feedback-warning-icon: #A97132;

  /* --- Feedback — danger --- */
  --color-feedback-danger-surface: #FAF4F4;
  --color-feedback-danger-text: #D4A6A6;
  --color-feedback-danger-border: #DEBFBF;
  --color-feedback-danger-icon: #D4A6A6;

  /* --- Motion --- */
  --duration-0: 0ms;
  --duration-80: 80ms;
  --duration-120: 120ms;
  --duration-180: 180ms;
  --duration-240: 240ms;
  --duration-320: 320ms;
  --ease-standard: cubic-bezier(0.4, 0, 0.2, 1);
  --ease-enter: cubic-bezier(0, 0, 0.2, 1);
  --ease-exit: cubic-bezier(0.4, 0, 1, 1);
  --ease-emphasized: cubic-bezier(0.2, 0, 0, 1);
}
```

## 17. CSS Extraction Summary

- CSS 추출 데이터 없음 (크롤링 시 CSS가 수집되지 않았거나 extract-css가 실행되지 않음)

## 18. Component-Token Map

| Component | Tokens Used |
|-----------|-------------|
| activity-card | `color.Ice Blue→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| app-shell | `color.Prussian Blue→surface`, `color.Bronze Gold→emphasis`, `color.Ice Blue→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| autocomplete | `color.Prussian Blue→surface`, `color.Bronze Gold→emphasis`, `color.Ice Blue→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| avatar | `color.Ice Blue→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| back-button | `color.Prussian Blue→surface`, `color.Bronze Gold→emphasis`, `color.Ice Blue→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| banner | `color.Ice Blue→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| bottom-sheet | `color.Prussian Blue→surface`, `color.Bronze Gold→emphasis`, `color.Ice Blue→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| breadcrumb | `color.Prussian Blue→surface`, `color.Bronze Gold→emphasis`, `color.Ice Blue→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| calendar-grid | `color.Ice Blue→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| chart-container | `color.Ice Blue→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| chart-legend | `color.Ice Blue→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| chart-panel | `color.Ice Blue→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| chart-tooltip | `color.Prussian Blue→surface`, `color.Bronze Gold→emphasis`, `color.Ice Blue→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| chat-panel | `color.Prussian Blue→surface`, `color.Bronze Gold→emphasis`, `color.Ice Blue→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| checkbox | `color.Prussian Blue→surface`, `color.Bronze Gold→emphasis`, `color.Ice Blue→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| chip | `color.Prussian Blue→surface`, `color.Bronze Gold→emphasis`, `color.Ice Blue→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| column-header | `color.Ice Blue→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| confirm-dialog | `color.Prussian Blue→surface`, `color.Bronze Gold→emphasis`, `color.Ice Blue→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| context-drawer | `color.Prussian Blue→surface`, `color.Bronze Gold→emphasis`, `color.Ice Blue→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| context-panel | `color.Prussian Blue→surface`, `color.Bronze Gold→emphasis`, `color.Ice Blue→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| cta-button | `color.Prussian Blue→surface`, `color.Bronze Gold→emphasis`, `color.Ice Blue→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| data-table | `color.Ice Blue→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| date-picker | `color.Prussian Blue→surface`, `color.Bronze Gold→emphasis`, `color.Ice Blue→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| date-range-picker | `color.Prussian Blue→surface`, `color.Bronze Gold→emphasis`, `color.Ice Blue→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| empty-state | `color.Ice Blue→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| file-preview | `color.Ice Blue→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| filter-chip | `color.Prussian Blue→surface`, `color.Bronze Gold→emphasis`, `color.Ice Blue→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| filter-panel | `color.Prussian Blue→surface`, `color.Bronze Gold→emphasis`, `color.Ice Blue→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| filter-toolbar | `color.Ice Blue→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| form-actions | `color.Prussian Blue→surface`, `color.Bronze Gold→emphasis`, `color.Ice Blue→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| form-section | `color.Prussian Blue→surface`, `color.Bronze Gold→emphasis`, `color.Ice Blue→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| ghost-button | `color.Prussian Blue→surface`, `color.Bronze Gold→emphasis`, `color.Ice Blue→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| icon-button | `color.Prussian Blue→surface`, `color.Bronze Gold→emphasis`, `color.Ice Blue→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| inline-alert | `color.Ice Blue→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| insight-card | `color.Ice Blue→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| kanban-board | `color.Ice Blue→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| kanban-card | `color.Ice Blue→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| kanban-column | `color.Ice Blue→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| link-button | `color.Prussian Blue→surface`, `color.Bronze Gold→emphasis`, `color.Ice Blue→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| message-composer | `color.Prussian Blue→surface`, `color.Bronze Gold→emphasis`, `color.Ice Blue→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| message-thread | `color.Prussian Blue→surface`, `color.Bronze Gold→emphasis`, `color.Ice Blue→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| mobile-tab-bar | `color.Prussian Blue→surface`, `color.Bronze Gold→emphasis`, `color.Ice Blue→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| mobile-topbar | `color.Prussian Blue→surface`, `color.Bronze Gold→emphasis`, `color.Ice Blue→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| modal-dialog | `color.Prussian Blue→surface`, `color.Bronze Gold→emphasis`, `color.Ice Blue→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| pagination | `color.Prussian Blue→surface`, `color.Bronze Gold→emphasis`, `color.Ice Blue→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| primary-button | `color.Prussian Blue→surface`, `color.Bronze Gold→emphasis`, `color.Ice Blue→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| profile-card | `color.Ice Blue→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| radio-group | `color.Prussian Blue→surface`, `color.Bronze Gold→emphasis`, `color.Ice Blue→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| row-actions | `color.Ice Blue→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| search-field | `color.Prussian Blue→surface`, `color.Bronze Gold→emphasis`, `color.Ice Blue→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| search-results | `color.Ice Blue→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| secondary-button | `color.Prussian Blue→surface`, `color.Bronze Gold→emphasis`, `color.Ice Blue→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| section-header | `color.Ice Blue→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| section-tabs | `color.Prussian Blue→surface`, `color.Bronze Gold→emphasis`, `color.Ice Blue→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| segmented-control | `color.Prussian Blue→surface`, `color.Bronze Gold→emphasis`, `color.Ice Blue→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| select | `color.Prussian Blue→surface`, `color.Bronze Gold→emphasis`, `color.Ice Blue→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| sidebar-nav | `color.Prussian Blue→surface`, `color.Bronze Gold→emphasis`, `color.Ice Blue→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| stat-card | `color.Ice Blue→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| status-badge | `color.Ice Blue→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| step-progress | `color.Ice Blue→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| tab-bar | `color.Prussian Blue→surface`, `color.Bronze Gold→emphasis`, `color.Ice Blue→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| tag | `color.Ice Blue→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| text-field | `color.Prussian Blue→surface`, `color.Bronze Gold→emphasis`, `color.Ice Blue→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| textarea | `color.Prussian Blue→surface`, `color.Bronze Gold→emphasis`, `color.Ice Blue→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| time-picker | `color.Prussian Blue→surface`, `color.Bronze Gold→emphasis`, `color.Ice Blue→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| toast | `color.Ice Blue→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| tooltip-guide | `color.Prussian Blue→surface`, `color.Bronze Gold→emphasis`, `color.Ice Blue→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| topbar | `color.Prussian Blue→surface`, `color.Bronze Gold→emphasis`, `color.Ice Blue→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| upload-dropzone | `color.Prussian Blue→surface`, `color.Bronze Gold→emphasis`, `color.Ice Blue→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| upload-progress | `color.Ice Blue→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| user-menu | `color.Prussian Blue→surface`, `color.Bronze Gold→emphasis`, `color.Ice Blue→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| wizard-layout | `color.Prussian Blue→surface`, `color.Bronze Gold→emphasis`, `color.Ice Blue→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| workspace-switcher | `color.Prussian Blue→surface`, `color.Bronze Gold→emphasis`, `color.Ice Blue→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |

## 19. Contrast Audit

| Background | Foreground | Ratio | Level |
|------------|------------|-------|-------|
| Ice Blue | Ink | 15.27:1 | AAA (pass) |
| Prussian Blue | Paper | 13.43:1 | AAA (pass) |
| Prussian Blue | Ice Blue | 10.86:1 | AAA (pass) |
| Bronze Gold | Ink | 4.58:1 | AA (pass) |
| Bronze Gold | Paper | 4.12:1 | AA-large (large-only) |
| Bronze Gold | Ice Blue | 3.33:1 | AA-large (large-only) |
| Prussian Blue | Bronze Gold | 3.26:1 | AA-large (large-only) |
| Prussian Blue | Ink | 1.41:1 | fail (FAIL) |
| Ice Blue | Paper | 1.24:1 | fail (FAIL) |

## 20. Pattern Catalog

### Layout Patterns

- **sidebar navigation**: —
- **workspace switcher**: —
- **transactions table**: —
- **balance kpi card**: —
- **compliance banner**: —
- **alert list**: —
- **audit timeline**: —
- **status badge**: —
- **date range picker**: —
- **member roster**: —
- **settings panel**: —
- **workspace navigation**: app-shell, sidebar-nav, topbar, breadcrumb, workspace-switcher, tab-bar, context-panel
- **dashboard cards**: stat-card, insight-card, activity-card, section-header, chart-panel
- **data tables**: data-table, column-header, filter-chip, row-actions, pagination, filter-toolbar

### Interaction Patterns

- **filter chrome**: —
- **command palette**: —
- **forms**: text-field, select, checkbox, textarea, form-section, radio-group, form-actions
- **notifications**: toast, inline-alert, empty-state, banner
