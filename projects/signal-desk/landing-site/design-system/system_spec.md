# Signal System Spec

## 1. Positioning

- **Brand**: Signal Desk
- **Product**: 작은 팀과 개인 제작자를 위한 고집 있는 에디토리얼 업무 앱
- **Audience**: 독립 창작자, 콘텐츠 팀, 브랜드 운영자
- **Platforms**: web, ios
- **Accessibility floor**: WCAG 2.2 AA

## 2. Identity Guardrails

- **Brand keywords**: calm, precise, editorial, trustworthy
- **Anti-keywords**: generic, noisy, overdecorated, playful
- **Tone of voice**: clear, warm, confident
- **Visual direction**: structured whitespace, measured contrast, text-first hierarchy
- **Interaction direction**: predictable states, low-noise motion, deliberate emphasis

## 3. Design Principles

- **Calm by Default**: 기본 상태는 조용해야 하고, 강조는 정말 필요할 때만 사용합니다.
- **Precision Over Ornament**: 장식보다 정보의 정렬, 상태의 정확성, 반응의 일관성을 우선합니다.
- **Editorial Hierarchy**: 타이포그래피와 여백으로 위계를 만들고, 장식은 의미를 돕는 범위에서만 사용합니다.
- **Trust Through Consistency**: 예측 가능한 인터랙션과 안정적인 시각 언어로 신뢰를 쌓습니다.

## 4. Foundation Priorities

- **Content design and microcopy rules** (high): signal 84
- **Color tokens and semantic color policy** (high): signal 55
- **Accessibility rules and contrast baseline** (high): signal 54
- **Type scale and editorial hierarchy** (high): signal 30

## 5. Token Strategy

- **Layering**: core -> semantic -> component
- **Core categories**: color, spacing, radius, typography, motion, elevation
- **Semantic categories**: surface, text, border, focus, feedback
- **Component categories**: button, input, navigation, overlay, editor
- **Typography families**: display, text, mono
- **Spacing scale**: 0, 2, 4, 8, 12, 16, 24, 32, 48, 64, 96

### Typography System (auto-resolved)

- **Heading**: Noto Serif KR
- **Body**: Pretendard
- **Korean**: Pretendard
- **Mono**: Source Code Pro
- **Product type detected**: editorial
- **Pairing source**: editorial (KR native)
- **Line height**: relaxed
- **Type scale**: base 16px, ratio 1.333 (xs=12px, sm=14px, md=16px, lg=21px, xl=28px, 2xl=38px, 3xl=50px)
- **Strategy**:
  - 헤딩(세리프) + 본문(산세리프) 대비 구조 — 에디토리얼 정석
  - 한글 서체: Pretendard — 라틴과 x-height/weight 조화
  - 모노스페이스: Source Code Pro — 코드/데이터 영역 전용
  - editorial 키워드 → 넉넉한 line-height, 헤딩에 serif 사용
  - calm 키워드 → comfortable spacing, 과한 weight 대비 지양
  - precise 키워드 → tight letter-spacing, tabular figures 권장
- **Heading note**: 한글 세리프의 사실상 유일한 고품질 웹폰트. 에디토리얼 한글에 필수.
- **Body note**: 한글 UI 서체의 사실상 표준. Apple SD Gothic Neo 기반이지만 더 정교함. 라틴은 Inter 계열.
- **Korean rationale**: Pretendard — 한글 UI 서체의 사실상 표준. 토스, 당근, 리디 등 국내 주요 서비스에서 사용. 자간이 자연스럽고 weight 전 구간에서 안정적.
- **Heading tracking**: lg=-0.015em, xl=-0.015em, 2xl=-0.02em, 3xl=-0.02em
- **Primary script**: korean
- **Hangul headline defaults**: Noto Serif KR | line-height 1.2-1.4 | tracking -0.02em
- **Hangul body defaults**: Pretendard | line-height 1.6-1.7 | label line-height 1.4-1.5
- **Wrap defaults**: headline word-break=keep-all, headline text-wrap=balance, body word-break=keep-all
- **Scale guidance**: 한글 hero/section heading은 영문 시안보다 한 단계 작은 스케일에서 시작해 wrap을 확인한 뒤 확장한다.
- **Hangul warning**: UI 라벨 — 작은 크기에서 가독성 저하
- **Hangul warning**: 모바일 본문 — 화면이 좁으면 답답함
- **Loading**: Pretendard(preload), Noto Serif KR(preload), Source Code Pro(lazy) | display: swap

## 6. Color Reference

- **Source**: REFERENCE X Vol.1 - Color Reference (/Users/sungwoon/Documents/designSystem/docs/color-reference.md)
- **Selection mode**: brand-guided
- **Preferred families**: Deep Reds, Natural Reds, Pastel Reds, Standard Oranges, Natural Oranges, Pastel Oranges
- **Palette strategy**: temperature=warm, contrast=balanced, diversity=balanced, surface_style=tinted
- **Palette expansion**: supporting_color_count=12, combination_count=4, prefer_pairings=True
- **Active palette**: signature-1
- **Active roles**:
  - `primary` -> Ochre #CC7722 / Standard Oranges
  - `accent` -> Apricot #FFB27F / Natural Oranges
  - `surface_tint` -> Wheat #F5DEB3 / Natural Yellows
- **Selected colors**:
  - Ochre #CC7722 / Standard Oranges / 중명도, 중채도, 흙기 섞인 따뜻한 오렌지 / 안정감, 내추럴, 신뢰감, 지속성
  - Apricot #FFB27F / Natural Oranges / 밝은 명도, 낮은 채도, 살짝 핑크빛이 도는 부드러운 오렌지 / 따뜻함, 부드러움, 친근함, 여유, 자연스러움
  - Wheat #F5DEB3 / Natural Yellows / 중명도, 저채도, 베이지 옐로 계열의 따뜻한 톤 / 따뜻함, 자연스러움, 부드러움, 안정감
- **Palette candidates**:
  - signature-1 (Signature): primary=Ochre, accent=Apricot, surface_tint=Wheat / Ochre is inside preferred families.; Apricot is inside preferred families.
  - assertive-3 (Assertive): primary=Classic Blue, accent=Ochre, surface_tint=Terracotta / Classic Blue matches brand tone keywords.; Ochre is inside preferred families.
- **Expanded supporting colors**:
  - Terracotta #E2725B / Natural Reds / reference-color / Terracotta stays inside the preferred families.; Terracotta reinforces the brand mood signals.
  - Amber #FFBF00 / Standard Yellows / reference-color / Amber reinforces the brand mood signals.
  - Persimmon #EC5800 / Natural Oranges / reference-color / Persimmon stays inside the preferred families.; Persimmon reinforces the brand mood signals.
  - Ochre Yellow #CB9D06 / Deep Yellows / reference-color / Ochre Yellow reinforces the brand mood signals.
  - Classic Blue #0F4C81 / Pantone Trend Blues / reference-color / Classic Blue reinforces the brand mood signals.
  - Navy Blue #000080 / Deep Blues / reference-color / Navy Blue reinforces the brand mood signals.
  - Pumpkin #FF7518 / Natural Oranges / reference-color / Pumpkin stays inside the preferred families.; Pumpkin reinforces the brand mood signals.
  - Forest Green #27503D / Deep Greens / reference-color / Forest Green reinforces the brand mood signals.
- **Expanded semantic roles**:
  - `brand_primary` -> Ochre #CC7722 / Standard Oranges
  - `brand_accent` -> Apricot #FFB27F / Natural Oranges
  - `surface_tint` -> Wheat #F5DEB3 / Natural Yellows
  - `canvas` -> Canvas White #F7F8FA / Generated Fallback
  - `surface` -> Paper #FFFFFF / Generated Fallback
  - `surface_muted` -> Surface Muted #EEF1F6 / Generated Fallback
  - `surface_elevated` -> Paper #FFFFFF / Generated Fallback
  - `border` -> Border Neutral #D6DDE6 / Generated Fallback
  - `border_strong` -> Border Strong #B0BAC7 / Generated Fallback
  - `ink` -> Ink #111111 / Generated Fallback
- **Combination lists**:
  - Seed Core: primary=Ochre, accent=Apricot, surface_tint=Wheat
  - Surface System: canvas=Canvas White, surface=Paper, surface_tint=Wheat, border=Border Neutral, ink=Ink, ink_muted=Muted Ink
  - Support Spectrum: support=Terracotta, support=Amber, support=Persimmon, support=Ochre Yellow, support=Classic Blue, support=Navy Blue
  - Semantic States: info=Classic Blue, success=Forest Green, warning=Apricot, danger=Terracotta
- **Notes**: 색상 레퍼런스는 semantic token 설계의 출발점으로 사용, raw reference color를 그대로 전체 UI에 덮지 않기, selected_colors와 palette_roles를 넣으면 manual override로 동작, palette_expansion은 seed color를 기반으로 support, neutral, semantic state 후보를 확장합니다
- **Application rule**: 레퍼런스 컬러는 semantic token으로 번역해서 사용하고, 접근성과 theme 호환성을 우선합니다.

## 7. Visual Reference Signals

- **Mode**: pinterest-assisted
- **Coverage**: source 1 / image 2 / selected 2
- **Rule**: visual references are advisory signals for motif and layout direction; official KB/spec remain the structural source of truth.
- **Provenance**: `observed` = directly measured from local pixels, `inferred` = synthesized from image/query/brand signals, `unverified` = reliable visual evidence not yet available.
- **Query seeds**: editorial dashboard ui, warm premium onboarding flow, serif product landing page
### Visual Direction

- **Density**: airy (confidence 0.94, provenance inferred) / editorial x6, landing x4, hero x2
- **Surface Style**: tinted (confidence 0.67, provenance inferred) / warm x4, editorial x6
- **Corner Style**: pill (confidence 0.38, provenance inferred) / svg corner ratio 0.50
- **Typography Mood**: editorial (confidence 0.94, provenance inferred) / editorial x6, serif x2
- **Color balance**: temperature=warm, contrast=high, neutral_bias=moderate, provenance=observed / dominant #D9B7A2, #FFF9F3, #8A6A58

### Layout Rhythm

- **Dashboard grid**: confidence 0.94 / provenance inferred / dashboard x4, 3:2-ish x2
- **Editorial feed**: confidence 0.94 / provenance inferred / editorial x6
- **Narrative landing flow**: confidence 0.94 / provenance inferred / landing x4, hero x2, pricing x1, testimonial x1
- **Split-pane workspace**: confidence 0.94 / provenance inferred / workspace x2, editor x1, navigation x1, command x1

### Image-derived Component Hints

- **Cards**: low-elevation tinted cards를 기본으로 하고, 넓은 내부 여백과 강한 section breathing room. pill-like actions만 제한적으로 허용. / provenance inferred / surface=tinted, density=airy, corner=pill
- **Navigation**: 고정 sidebar 또는 split-pane navigation을 우선하고, 현재 위치와 scope를 항상 명시한다. / provenance inferred / Split-pane workspace
- **Typography**: headline rhythm과 본문 리듬의 대비를 키우고, label/metadata는 조용하게 유지한다. / provenance inferred / typography_mood=editorial
- **Data Display**: 정보 밀도를 유지하되 thin dividers와 restrained accent로 hierarchy를 만든다. / provenance inferred / layout=dashboard-grid, density=airy

### Synthesis Notes

- layout는 Dashboard grid 기준으로 정리
- surface language는 tinted 성향 우선
- typography mood는 editorial 축 유지
- density는 airy 기준으로 primitive spacing 조정
- palette temperature는 warm 쪽을 우선
- Avoid: glassmorphism-heavy surfaces
- Avoid: high-saturation neon UI
- Avoid: playful candy gradients

## 8. Component Strategy

- **Product primitives**: workspace navigation, rich text editor, command palette, dashboard cards, data tables, hero section, feature grid, social proof, testimonial, faq accordion, landing cta section, site footer, site header, pricing and plans
- **Required families**: button, data-display, editorial, feedback, input, marketing, navigation, foundation, overlay
- **Visual-reference archetypes**:

- **Dashboard insight module** (data-display / 0.94): stat-card, insight-card, chart-panel, section-header, filter-chip
- **Editorial content block** (editorial / 0.94): content-card, featured-story-card, section-header, content-meta, byline-row
- **Marketing hero stack** (marketing / 0.94): hero-section, hero-headline, hero-visual, cta-button-group, trust-strip
- **Workspace shell** (navigation / 0.94): app-shell, sidebar-nav, workspace-switcher, breadcrumb, context-panel
- **Data review table** (data-display / 0.87): data-table, column-header, row-actions, filter-toolbar, pagination
- **Conversation sidecar** (overlay / 0.52): chat-panel, message-thread, message-composer, context-drawer

- **button**: primary-button, secondary-button, ghost-button, icon-button, cta-button, link-button, form-actions, hero-cta-group
- **data-display**: data-table, column-header, row-actions, kanban-board, kanban-column, kanban-card, comment-thread, calendar-grid / visual signals: Dashboard insight module (0.94), Data review table (0.87)
- **editorial**: editor-canvas, editor-toolbar, slash-command-menu, block-controls, inline-format-menu, content-card, featured-story-card, content-meta / visual signals: Editorial content block (0.94)
- **feedback**: filter-chip, inline-alert, empty-state, toast, banner, shortcut-hint, upgrade-banner, status-badge
- **input**: text-field, search-field, segmented-control, textarea, select, checkbox, radio-group, form-section
- **marketing**: hero-container, hero-eyebrow, hero-headline, hero-subheadline, hero-visual, hero-trust-strip, logo-cloud, customer-logo / visual signals: Marketing hero stack (0.94)
- **navigation**: sidebar-nav, topbar, breadcrumb, workspace-switcher, scope-switcher, mobile-topbar, mobile-tab-bar, back-button / visual signals: Workspace shell (0.94)
- **foundation**: app-shell, command-result-item, shortcut-hint, stat-card, insight-card, activity-card, section-header, column-header
- **overlay**: inline-format-menu, command-palette, bottom-sheet, modal-dialog, mention-popup, autocomplete, command-result-item, user-menu

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

- Analysed live reference sources: 47
- Rule: copy visuals from no single source; absorb patterns only when they reinforce brand keywords and avoid anti-keywords.
- Use references to validate structure, accessibility, token discipline, and documentation quality.

## 11. AI Synthesis Principles

- **hex를 만들지 않는다**: AI는 색상 hex 값을 임의로 생성하지 않는다. 반드시 color_reference, CSS 추출, 브랜드 가이드 등 실증 소스에서 가져온 값만 사용한다.
- **토큰명을 만들지 않는다**: AI는 토큰 이름을 임의로 발명하지 않는다. 네이밍 패턴(core/semantic/component 레이어 규칙)은 정의하되, 구체적 토큰명은 실제 컴포넌트와 역할에서 도출한다.
- **팩트 위에 해석만**: AI는 수집된 레퍼런스, 프로필, 온톨로지 증거 위에 해석과 구조화만 수행한다. 증거 없는 추론, 존재하지 않는 패턴 서술, 가상의 사용 사례 생성을 금지한다.
- **이모지를 UI 요소로 쓰지 않는다**: AI는 아이콘, 상태 표시, 버튼 장식, 네비게이션 지표 등 UI 컴포넌트 자리에 이모지(🎨 ✅ 🔥 ⚡ 🚀 ❌ ⭐ 📊 등)를 절대 넣지 않는다. 반드시 SVG 아이콘 컴포넌트를 직접 구현하거나, 아이콘 라이브러리(Lucide, Heroicons, Phosphor, Tabler 등)를 import해서 사용한다. 이모지는 본문 콘텐츠(예: 블로그 텍스트, 사용자 입력)에서만 허용되며, 시스템 UI 요소로는 금지한다. 이 규칙은 AI가 UI를 만들 때 가장 자주 저지르는 실수이므로 엄격히 적용한다.
- **컴포넌트를 직접 구현한다**: AI는 '임시 버튼', '플레이스홀더 카드', 'TODO 컴포넌트' 같은 반쪽 구현을 남기지 않는다. system_spec.md의 Component Strategy와 component_specs.md에 정의된 구조(anatomy), 상태(states), 토큰 바인딩, 접근성 규칙을 그대로 따라 완전한 컴포넌트를 구현한다. 기존 라이브러리 컴포넌트를 그냥 import해서 쓰는 대신, 디자인 시스템 토큰으로 스타일을 명시적으로 바인딩한다.

## 12. Ontology Targets

- **component**: 319
- **design_system**: 229
- **pattern**: 84
- **content**: 84
- **brand**: 80
- **color**: 55
- **accessibility**: 54
- **typography**: 30

## 13. Profile Validation

- Warning: [pitfall#3-rebrand] Ochre vs Apricot (orange): lightness diff 28, saturation diff 29 — possible rebrand remnant

## 14. Quick Start

이 문서는 **Signal System**의 디자인 시스템 사양입니다.

### 시작하기

1. **토큰 적용**: Drop-in CSS(아래 섹션 16)의 CSS 변수를 프로젝트에 복사합니다.
2. **컬러 세팅**: Color Reference(섹션 6)의 semantic role을 기준으로 surface/text/border를 잡습니다.
3. **타이포 세팅**: Token Strategy(섹션 5)의 font family와 type scale을 적용합니다.
4. **시각 방향 확인**: Visual Reference Signals(섹션 7)에서 density/surface/layout cue를 먼저 확인합니다.
5. **컴포넌트 구현**: Component Strategy(섹션 8)의 family 순서대로 하나씩 빌드합니다.

### 우선순위

핵심 primitive: **workspace navigation, rich text editor, command palette, dashboard cards, data tables**

이 primitive를 지원하는 컴포넌트부터 구현하고, 나머지는 필요에 따라 확장합니다.

## 15. DO / DON'T

### DO

- **Calm by Default**: 채도 낮은 기본 팔레트
- **Precision Over Ornament**: 명확한 상태 규칙
- **Editorial Hierarchy**: 텍스트 중심 레이아웃
- **Trust Through Consistency**: 일관된 disabled/error/success 패턴
- 모든 시각적 선택에서 **calm, precise, editorial** 기준을 적용
- semantic token을 통해 컬러를 적용 (하드코딩 금지)
- 접근성 기준을 모든 text/surface 조합에서 먼저 검증
- 컴포넌트 변형 추가 전 기존 variant로 해결 가능한지 먼저 확인
- 아이콘은 SVG 컴포넌트 또는 Lucide/Heroicons/Phosphor/Tabler 등 라이브러리로 구현
- component_specs.md의 anatomy/states/token binding을 그대로 따라 완전히 구현

### DON'T

- **generic** 방향의 디자인 결정을 하지 않음
- **noisy** 방향의 디자인 결정을 하지 않음
- **overdecorated** 방향의 디자인 결정을 하지 않음
- **playful** 방향의 디자인 결정을 하지 않음
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
  --font-heading: 'Noto Serif KR', serif;
  --font-body: 'Pretendard', sans-serif;
  --font-mono: 'Source Code Pro', monospace;
  --text-xs: 12px;
  --text-sm: 14px;
  --text-md: 16px;
  --text-lg: 21px;
  --text-xl: 28px;
  --text-2xl: 38px;
  --text-3xl: 50px;

  --leading-tight: 1.2;
  --leading-normal: 1.5;
  --leading-comfortable: 1.6;
  --leading-relaxed: 1.75;

  /* --- Color (from reference) --- */
  --color-primary: #CC7722;
  --color-accent: #FFB27F;
  --color-surface-tint: #F5DEB3;

  /* --- Semantic roles (expanded) --- */
  --color-brand-primary: #CC7722;
  --color-brand-accent: #FFB27F;
  --color-surface-tint: #F5DEB3;
  --color-canvas: #F7F8FA;
  --color-surface: #FFFFFF;
  --color-surface-muted: #EEF1F6;
  --color-surface-elevated: #FFFFFF;
  --color-border: #D6DDE6;
  --color-border-strong: #B0BAC7;
  --color-ink: #111111;
  --color-ink-muted: #4B5563;
  --color-ink-subtle: #6B7280;
  --color-ink-inverse: #FFFFFF;
  --color-primary-support: #EC5800;
  --color-accent-support: #EC5800;
  --color-info: #0F4C81;
  --color-success: #27503D;
  --color-warning: #FFB27F;
  --color-danger: #E2725B;
  --color-link: #CC7722;
  --color-link-hover: #A9631C;

  /* --- Button — primary --- */
  --color-button-primary-surface-default: #CC7722;
  --color-button-primary-surface-hover: #B2681E;
  --color-button-primary-surface-active: #A05E1B;
  --color-button-primary-surface-disabled: #E6C4A4;
  --color-button-primary-text-default: #FFFFFF;
  --color-button-primary-text-disabled: #FBFCFC;
  --color-button-primary-border-default: #CC7722;
  --color-button-primary-focus-ring: #CC7722;

  /* --- Button — secondary --- */
  --color-button-secondary-surface-default: #FFFFFF;
  --color-button-secondary-surface-hover: #F1F1F1;
  --color-button-secondary-surface-active: #E7E7E7;
  --color-button-secondary-surface-disabled: #F7F8FA;
  --color-button-secondary-text-default: #111111;
  --color-button-secondary-text-disabled: #909091;
  --color-button-secondary-border-default: #BDC8D7;
  --color-button-secondary-border-hover: #A3B3C7;
  --color-button-secondary-focus-ring: #CC7722;

  /* --- Button — ghost --- */
  --color-button-ghost-surface-default: transparent;
  --color-button-ghost-surface-hover: #F3F3F3;
  --color-button-ghost-surface-active: #EAEAEA;
  --color-button-ghost-surface-disabled: transparent;
  --color-button-ghost-text-default: #4B5563;
  --color-button-ghost-text-hover: #111111;
  --color-button-ghost-text-disabled: #AAAFB6;
  --color-button-ghost-border-default: transparent;
  --color-button-ghost-focus-ring: #CC7722;

  /* --- Button — danger --- */
  --color-button-danger-surface-default: #E2725B;
  --color-button-danger-surface-hover: #DD5C41;
  --color-button-danger-surface-active: #DA4D30;
  --color-button-danger-text-default: #111111;
  --color-button-danger-border-default: #E2725B;
  --color-button-danger-focus-ring: #E2725B;

  /* --- Input --- */
  --color-input-surface-default: #FFFFFF;
  --color-input-surface-filled: #FFFFFF;
  --color-input-surface-disabled: #F7F8FA;
  --color-input-text-default: #111111;
  --color-input-text-placeholder: #90969F;
  --color-input-text-disabled: #AAAFB6;
  --color-input-border-default: #D6DDE6;
  --color-input-border-hover: #B6C3D3;
  --color-input-border-focus: #CC7722;
  --color-input-border-error: #E2725B;
  --color-input-border-disabled: #E6EAF0;

  /* --- Card --- */
  --color-card-surface-default: #FFFFFF;
  --color-card-surface-hover: #FAFAFA;
  --color-card-surface-muted: #F7F8FA;
  --color-card-border-default: #D6DDE6;
  --color-card-border-hover: #B6C3D3;
  --color-card-border-focus: #CC7722;

  /* --- Nav link --- */
  --color-nav-link-text-default: #4B5563;
  --color-nav-link-text-hover: #111111;
  --color-nav-link-text-active: #CC7722;
  --color-nav-link-surface-hover: #F5F5F5;
  --color-nav-link-indicator: #FFB27F;

  /* --- Link --- */
  --color-link-text-default: #CC7722;
  --color-link-text-hover: #A05E1B;
  --color-link-text-visited: #A16A34;

  /* --- Feedback — info --- */
  --color-feedback-info-surface: #E2EAF0;
  --color-feedback-info-text: #0F4C81;
  --color-feedback-info-border: #5580A5;
  --color-feedback-info-icon: #0F4C81;

  /* --- Feedback — success --- */
  --color-feedback-success-surface: #E5EAE8;
  --color-feedback-success-text: #27503D;
  --color-feedback-success-border: #658276;
  --color-feedback-success-icon: #27503D;

  /* --- Feedback — warning --- */
  --color-feedback-warning-surface: #FFF6F0;
  --color-feedback-warning-text: #FFB27F;
  --color-feedback-warning-border: #FDC7A4;
  --color-feedback-warning-icon: #FFB27F;

  /* --- Feedback — danger --- */
  --color-feedback-danger-surface: #FCEEEB;
  --color-feedback-danger-text: #E2725B;
  --color-feedback-danger-border: #E89A8B;
  --color-feedback-danger-icon: #E2725B;

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

### Variable Resolution

- 전체 CSS 변수: **25284**개
- 해결됨: **18707**개 (74%)
- 미해결: **6577**개

### Brand Color Candidates

- 후보 수: **6791**개
- Role 분포: selector=6046, primary=267, brand=255, accent=107, action=84, neutral=18, chromatic=12, cta=2

### Typography Extraction

- 스케일 항목: **0**개
- 고유 폰트 패밀리: **339**개
- 고유 weight 수: **16**개

### Alias Layer

- 전체 토큰: **25284**개
- Tier 분포: action=6520, component=9295, core=6931, util=2538
- Schema layer 분포: component=9295, core=9469, semantic=6520
- var() 체인: 평균 2.79, 최대 9

## 18. Component-Token Map

| Component | Tokens Used |
|-----------|-------------|
| activity-card | `color.Wheat→background`, `spacing.12→padding`, `radius.md→radius`, `color.Wheat→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard`, `font:Pretendard` |
| app-shell | `color.Wheat→background`, `spacing.12→padding`, `radius.md→radius`, `color.Ochre→surface`, `color.Apricot→emphasis`, `color.Wheat→background`, `spacing.12→padding`, `radius.md→radius` |
| autocomplete | `color.Ochre→surface`, `color.Apricot→emphasis`, `color.Wheat→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| avatar | `color.Wheat→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| back-button | `color.Ochre→surface`, `color.Apricot→emphasis`, `color.Wheat→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| banner | `color.Wheat→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| block-controls | `color.Wheat→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| bottom-sheet | `color.Ochre→surface`, `color.Apricot→emphasis`, `color.Wheat→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| breadcrumb | `color.Ochre→surface`, `color.Apricot→emphasis`, `color.Wheat→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| byline-row | `color.Wheat→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| calendar-grid | `color.Wheat→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| chart-panel | `color.Wheat→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| checkbox | `color.Ochre→surface`, `color.Apricot→emphasis`, `color.Wheat→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| chip | `color.Ochre→surface`, `color.Apricot→emphasis`, `color.Wheat→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| column-header | `color.Wheat→background`, `spacing.12→padding`, `radius.md→radius`, `color.Wheat→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard`, `font:Pretendard` |
| command-palette | `color.Ochre→surface`, `color.Apricot→emphasis`, `color.Wheat→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| command-result-item | `color.Wheat→background`, `spacing.12→padding`, `radius.md→radius`, `color.Ochre→surface`, `color.Apricot→emphasis`, `color.Wheat→background`, `spacing.12→padding`, `radius.md→radius` |
| comment-input | `color.Ochre→surface`, `color.Apricot→emphasis`, `color.Wheat→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| comment-thread | `color.Wheat→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| content-card | `color.Wheat→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| content-meta | `color.Wheat→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| context-panel | `color.Ochre→surface`, `color.Apricot→emphasis`, `color.Wheat→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| cta-button | `color.Ochre→surface`, `color.Apricot→emphasis`, `color.Wheat→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| cta-button-group | `color.Ochre→surface`, `color.Apricot→emphasis`, `color.Wheat→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| cta-headline | `color.Wheat→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| cta-section | `color.Wheat→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| cta-supporting-text | `color.Wheat→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| customer-logo | `color.Wheat→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| data-table | `color.Wheat→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| date-picker | `color.Ochre→surface`, `color.Apricot→emphasis`, `color.Wheat→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| date-range-picker | `color.Ochre→surface`, `color.Apricot→emphasis`, `color.Wheat→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| editor-canvas | `color.Wheat→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| editor-toolbar | `color.Wheat→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| empty-state | `color.Wheat→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| faq-answer | `color.Wheat→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| faq-item | `color.Wheat→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| faq-question | `color.Wheat→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| faq-section | `color.Wheat→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| feature-card | `color.Wheat→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| feature-comparison | `color.Wheat→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| feature-description | `color.Wheat→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| feature-grid | `color.Wheat→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| feature-icon | `color.Wheat→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| feature-section | `color.Wheat→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| feature-title | `color.Wheat→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| featured-story-card | `color.Wheat→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| file-preview | `color.Wheat→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| filter-chip | `color.Wheat→background`, `spacing.12→padding`, `radius.md→radius`, `color.Ochre→surface`, `color.Apricot→emphasis`, `color.Wheat→background`, `spacing.12→padding`, `radius.md→radius` |
| filter-panel | `color.Ochre→surface`, `color.Apricot→emphasis`, `color.Wheat→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| filter-toolbar | `color.Wheat→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| footer-column | `color.Wheat→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| footer-legal | `color.Wheat→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| footer-link | `color.Wheat→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| footer-social | `color.Wheat→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| form-actions | `color.Ochre→surface`, `color.Apricot→emphasis`, `color.Wheat→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| form-section | `color.Ochre→surface`, `color.Apricot→emphasis`, `color.Wheat→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| ghost-button | `color.Ochre→surface`, `color.Apricot→emphasis`, `color.Wheat→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| hero-container | `color.Wheat→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| hero-cta-group | `color.Ochre→surface`, `color.Apricot→emphasis`, `color.Wheat→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| hero-eyebrow | `color.Wheat→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| hero-headline | `color.Wheat→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| hero-section | `color.Wheat→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| hero-subheadline | `color.Wheat→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| hero-trust-strip | `color.Wheat→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| hero-visual | `color.Wheat→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| icon-button | `color.Ochre→surface`, `color.Apricot→emphasis`, `color.Wheat→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| inline-alert | `color.Wheat→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| inline-format-menu | `color.Ochre→surface`, `color.Apricot→emphasis`, `color.Wheat→background`, `spacing.12→padding`, `radius.md→radius`, `color.Wheat→background`, `spacing.12→padding`, `radius.md→radius` |
| insight-card | `color.Wheat→background`, `spacing.12→padding`, `radius.md→radius`, `color.Wheat→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard`, `font:Pretendard` |
| kanban-board | `color.Wheat→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| kanban-card | `color.Wheat→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| kanban-column | `color.Wheat→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| link-button | `color.Ochre→surface`, `color.Apricot→emphasis`, `color.Wheat→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| logo-cloud | `color.Wheat→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| mention-popup | `color.Ochre→surface`, `color.Apricot→emphasis`, `color.Wheat→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| metric-highlight | `color.Wheat→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| mobile-menu-trigger | `color.Ochre→surface`, `color.Apricot→emphasis`, `color.Wheat→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| mobile-tab-bar | `color.Ochre→surface`, `color.Apricot→emphasis`, `color.Wheat→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| mobile-topbar | `color.Ochre→surface`, `color.Apricot→emphasis`, `color.Wheat→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| modal-dialog | `color.Ochre→surface`, `color.Apricot→emphasis`, `color.Wheat→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| pagination | `color.Wheat→background`, `spacing.12→padding`, `radius.md→radius`, `color.Ochre→surface`, `color.Apricot→emphasis`, `color.Wheat→background`, `spacing.12→padding`, `radius.md→radius` |
| press-quote | `color.Wheat→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| pricing-card | `color.Wheat→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| primary-button | `color.Ochre→surface`, `color.Apricot→emphasis`, `color.Wheat→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| profile-card | `color.Wheat→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| radio-group | `color.Ochre→surface`, `color.Apricot→emphasis`, `color.Wheat→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| row-actions | `color.Wheat→background`, `spacing.12→padding`, `radius.md→radius`, `color.Wheat→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard`, `font:Pretendard` |
| scope-switcher | `color.Ochre→surface`, `color.Apricot→emphasis`, `color.Wheat→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| search-field | `color.Ochre→surface`, `color.Apricot→emphasis`, `color.Wheat→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| search-results | `color.Wheat→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| secondary-button | `color.Ochre→surface`, `color.Apricot→emphasis`, `color.Wheat→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| section-header | `color.Wheat→background`, `spacing.12→padding`, `radius.md→radius`, `color.Wheat→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard`, `font:Pretendard` |
| section-tabs | `color.Ochre→surface`, `color.Apricot→emphasis`, `color.Wheat→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| segmented-control | `color.Ochre→surface`, `color.Apricot→emphasis`, `color.Wheat→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| select | `color.Ochre→surface`, `color.Apricot→emphasis`, `color.Wheat→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| shortcut-hint | `color.Wheat→background`, `spacing.12→padding`, `radius.md→radius`, `color.Wheat→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard`, `font:Pretendard` |
| sidebar-nav | `color.Ochre→surface`, `color.Apricot→emphasis`, `color.Wheat→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| site-footer | `color.Wheat→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| site-header | `color.Wheat→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| site-logo | `color.Wheat→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| site-nav | `color.Wheat→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| site-nav-cta | `color.Ochre→surface`, `color.Apricot→emphasis`, `color.Wheat→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| slash-command-menu | `color.Wheat→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| stat-card | `color.Wheat→background`, `spacing.12→padding`, `radius.md→radius`, `color.Wheat→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard`, `font:Pretendard` |
| status-badge | `color.Wheat→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| step-progress | `color.Wheat→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| tab-bar | `color.Ochre→surface`, `color.Apricot→emphasis`, `color.Wheat→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| tag | `color.Wheat→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| testimonial-author | `color.Wheat→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| testimonial-card | `color.Wheat→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| testimonial-quote | `color.Wheat→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| testimonial-section | `color.Wheat→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| text-field | `color.Ochre→surface`, `color.Apricot→emphasis`, `color.Wheat→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| textarea | `color.Ochre→surface`, `color.Apricot→emphasis`, `color.Wheat→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| time-picker | `color.Ochre→surface`, `color.Apricot→emphasis`, `color.Wheat→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| toast | `color.Wheat→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| tooltip-guide | `color.Ochre→surface`, `color.Apricot→emphasis`, `color.Wheat→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| topbar | `color.Ochre→surface`, `color.Apricot→emphasis`, `color.Wheat→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| trust-strip | `color.Wheat→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| upgrade-banner | `color.Wheat→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| upload-dropzone | `color.Ochre→surface`, `color.Apricot→emphasis`, `color.Wheat→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| upload-progress | `color.Wheat→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| user-menu | `color.Ochre→surface`, `color.Apricot→emphasis`, `color.Wheat→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| wizard-layout | `color.Ochre→surface`, `color.Apricot→emphasis`, `color.Wheat→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| workspace-switcher | `color.Ochre→surface`, `color.Apricot→emphasis`, `color.Wheat→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |

## 19. Contrast Audit

| Background | Foreground | Ratio | Level |
|------------|------------|-------|-------|
| Wheat | Ink | 14.37:1 | AAA (pass) |
| Apricot | Ink | 10.72:1 | AAA (pass) |
| Ochre | Ink | 5.60:1 | AA (pass) |
| Ochre | Paper | 3.37:1 | AA-large (large-only) |
| Ochre | Wheat | 2.57:1 | fail (FAIL) |
| Ochre | Apricot | 1.91:1 | fail (FAIL) |
| Apricot | Paper | 1.76:1 | fail (FAIL) |
| Apricot | Wheat | 1.34:1 | fail (FAIL) |
| Wheat | Paper | 1.31:1 | fail (FAIL) |

## 20. Pattern Catalog

### Layout Patterns

- **workspace navigation**: app-shell, sidebar-nav, topbar, breadcrumb, workspace-switcher, tab-bar, context-panel
- **dashboard cards**: stat-card, insight-card, activity-card, section-header, chart-panel
- **data tables**: data-table, column-header, filter-chip, row-actions, pagination, filter-toolbar
- **hero section**: hero-container, hero-eyebrow, hero-headline, hero-subheadline, hero-cta-group, hero-visual, hero-trust-strip, hero-section, trust-strip
- **feature grid**: feature-section, feature-grid, feature-card, feature-icon, feature-title, feature-description
- **social proof**: logo-cloud, customer-logo, metric-highlight, press-quote
- **testimonial**: testimonial-section, testimonial-card, testimonial-quote, testimonial-author
- **faq accordion**: faq-section, faq-item, faq-question, faq-answer
- **landing cta section**: cta-section, cta-headline, cta-supporting-text, cta-button-group
- **site footer**: site-footer, footer-column, footer-link, footer-legal, footer-social
- **site header**: site-header, site-logo, site-nav, site-nav-cta, mobile-menu-trigger
- **pricing and plans**: pricing-card, feature-comparison, upgrade-banner

### Interaction Patterns

- **rich text editor**: editor-canvas, editor-toolbar, inline-format-menu, slash-command-menu, block-controls, content-card, featured-story-card, content-meta, byline-row
- **command palette**: command-palette, command-result-item, shortcut-hint, scope-switcher
- **forms**: text-field, select, checkbox, textarea, form-section, radio-group, form-actions
- **notifications**: toast, inline-alert, empty-state, banner
