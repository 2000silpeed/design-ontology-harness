# PL Stats System Spec

## 1. Positioning

- **Brand**: PL Stats
- **Product**: 프리미어리그 경기 결과, 순위, 선수 통계를 보여주는 스포츠 데이터 웹사이트
- **Audience**: 프리미어리그 팬, 축구 데이터 분석에 관심 있는 사용자, 판타지 풋볼 플레이어
- **Platforms**: web, mobile-web
- **Accessibility floor**: WCAG 2.2 AA

## 2. Identity Guardrails

- **Brand keywords**: bold, precise, energetic
- **Anti-keywords**: generic, cluttered, childish
- **Tone of voice**: confident, data-driven, exciting
- **Visual direction**: strong contrast, data-rich layout, sport editorial, dark mode first
- **Interaction direction**: fast navigation, real-time updates, comparison tools

## 3. Design Principles

- **Bold with Discipline**: 강한 개성은 허용하되 구조를 해치지 않는 선에서 통제합니다.
- **Precision Over Ornament**: 장식보다 정보의 정렬, 상태의 정확성, 반응의 일관성을 우선합니다.
- **Energetic**: `energetic`를 시각적 선택과 인터랙션 선택의 기본 기준으로 삼습니다.

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

- **Heading**: Spoqa Han Sans Neo
- **Body**: Spoqa Han Sans Neo
- **Korean**: Spoqa Han Sans Neo
- **Mono**: JetBrains Mono
- **Product type detected**: editorial
- **Pairing source**: auto-scored
- **Line height**: tight
- **Type scale**: base 16px, ratio 1.333 (xs=12px, sm=14px, md=16px, lg=21px, xl=28px, 2xl=38px, 3xl=50px)
- **Strategy**:
  - 단일 서체(Spoqa Han Sans Neo)로 weight 대비 위계 — 일관성 우선
  - 한글 서체: Spoqa Han Sans Neo — 라틴과 x-height/weight 조화
  - 모노스페이스: JetBrains Mono — 코드/데이터 영역 전용
  - precise 키워드 → tight letter-spacing, tabular figures 권장
- **Heading note**: 스포카에서 만든 한글 산세리프. Source Sans Pro 기반. 깔끔한 데이터 UI에 적합.
- **Body note**: 스포카에서 만든 한글 산세리프. Source Sans Pro 기반. 깔끔한 데이터 UI에 적합.
- **Korean rationale**: Spoqa Han Sans Neo — Pretendard 이전 시대의 한글 UI 표준. 요기요, 여기어때 등에서 사용. 깔끔하지만 weight 범위와 Variable 미지원이 아쉬움. 신규 프로젝트에서는 Pretendard 추천.
- **Heading tracking**: lg=-0.015em, xl=-0.015em, 2xl=-0.02em, 3xl=-0.02em
- **Primary script**: korean
- **Hangul headline defaults**: Spoqa Han Sans Neo | line-height 1.2-1.3 | tracking -0.02em
- **Hangul body defaults**: Spoqa Han Sans Neo | line-height 1.5-1.6 | label line-height 1.4-1.5
- **Wrap defaults**: headline word-break=keep-all, headline text-wrap=balance, body word-break=keep-all
- **Scale guidance**: 한글 hero/section heading은 영문 시안보다 한 단계 작은 스케일에서 시작해 wrap을 확인한 뒤 확장한다.
- **Hangul warning**: 장문 본문 — line-height 여유 부족
- **Hangul warning**: 감성적 브랜딩
- **Hangul warning**: 장문 본문 — line-height 여유 부족
- **Loading**: Spoqa Han Sans Neo(preload), JetBrains Mono(lazy) | display: swap

## 6. Color Reference

- **Source**: Premier League Color Palette (/Users/sungwoon/ai-projects/design-ontology-harness/projects/premier-league/docs/color-reference.md)
- **Selection mode**: brand-guided
- **Preferred families**: Deep Reds, Deep Neutrals
- **Palette strategy**: temperature=neutral, contrast=vivid, diversity=balanced, surface_style=grounded
- **Palette expansion**: supporting_color_count=10, combination_count=3, prefer_pairings=True
- **Active palette**: signature-1
- **Active roles**:
  - `primary` -> Matchday Red #E90052 / Deep Reds
  - `accent` -> Electric Green #00FF85 / Accent Brights
  - `surface_tint` -> Golden Score #FFD700 / Accent Brights
- **Selected colors**:
  - Matchday Red #E90052 / Deep Reds / 강렬함, 열정, 주목성
  - Electric Green #00FF85 / Accent Brights / 활기, 생동감, 주목성
  - Golden Score #FFD700 / Accent Brights / 열정, 주목성, 상징적
- **Palette candidates**:
  - signature-1 (Signature): primary=Matchday Red, accent=Electric Green, surface_tint=Golden Score / Matchday Red is inside preferred families.; Electric Green matches brand tone keywords.
- **Expanded supporting colors**:
  - Matchday Red #E90052 / Deep Reds / pairing-reference / Matchday Red stays inside the preferred families.; Matchday Red reinforces the brand mood signals.
  - Midnight Navy #1A1A2E / Deep Neutrals / pairing-reference / Midnight Navy stays inside the preferred families.; Midnight Navy reinforces the brand mood signals.
  - Premier Purple #38003C / Deep Reds / pairing-reference / Premier Purple stays inside the preferred families.; Premier Purple reinforces the brand mood signals.
  - Pairing #FFFFFF #FFFFFF / Derived Pairing / pairing-swatch / Pairing #FFFFFF reinforces the brand mood signals.; Pairing #FFFFFF comes from the seed pairing references.
  - Caution Amber #FF8C00 / Accent Brights / reference-color / Caution Amber reinforces the brand mood signals.
  - Victory Green #00C853 / Semantic States / reference-color / Victory Green reinforces the brand mood signals.
  - Defeat Red #FF1744 / Semantic States / reference-color / Defeat Red reinforces the brand mood signals.
  - Draw Gray #78909C / Semantic States / reference-color / Draw Gray reinforces the brand mood signals.; Draw Gray can act as a neutral support color.
- **Expanded semantic roles**:
  - `brand_primary` -> Matchday Red #E90052 / Deep Reds
  - `brand_accent` -> Electric Green #00FF85 / Accent Brights
  - `surface_tint` -> Golden Score #FFD700 / Accent Brights
  - `canvas` -> Pairing #FFFFFF #FFFFFF / Derived Pairing
  - `surface` -> Pairing #FFFFFF #FFFFFF / Derived Pairing
  - `surface_muted` -> Surface Muted #EEF1F6 / Generated Fallback
  - `surface_elevated` -> Pairing #FFFFFF #FFFFFF / Derived Pairing
  - `border` -> Border Neutral #D6DDE6 / Generated Fallback
  - `border_strong` -> Border Strong #B0BAC7 / Generated Fallback
  - `ink` -> Midnight Navy #1A1A2E / Deep Neutrals
- **Combination lists**:
  - Seed Core: primary=Matchday Red, accent=Electric Green, surface_tint=Golden Score
  - Surface System: canvas=Pairing #FFFFFF, surface=Pairing #FFFFFF, surface_tint=Golden Score, border=Border Neutral, ink=Midnight Navy, ink_muted=Steel Gray
  - Support Spectrum: support=Matchday Red, support=Midnight Navy, support=Premier Purple, support=Pairing #FFFFFF, support=Caution Amber, support=Victory Green
- **Application rule**: 레퍼런스 컬러는 semantic token으로 번역해서 사용하고, 접근성과 theme 호환성을 우선합니다.

## 7. Visual Reference Signals

- No visual reference connected.

## 8. Component Strategy

- **Product primitives**: dashboard cards, data tables, workspace navigation, search and filter, charts and visualization, tags and labels
- **Required families**: button, data-display, feedback, input, marketing, navigation, foundation, overlay
- **Visual-reference archetypes**:

- No visual-reference archetypes suggested.

- **button**: primary-button, secondary-button, ghost-button, icon-button, cta-button, link-button, form-actions, hero-cta-group
- **data-display**: data-table, column-header, row-actions, search-results, stat-card, insight-card, activity-card, section-header
- **feedback**: filter-chip, inline-alert, empty-state, toast, status-badge, shortcut-hint
- **input**: text-field, search-field, segmented-control, filter-chip, filter-panel, textarea, select, checkbox
- **marketing**: hero-container, hero-eyebrow, hero-headline, hero-subheadline, hero-visual, hero-trust-strip
- **navigation**: sidebar-nav, topbar, breadcrumb, workspace-switcher, mobile-topbar, mobile-tab-bar, back-button, section-tabs
- **foundation**: stat-card, insight-card, activity-card, section-header, column-header, row-actions, pagination, app-shell
- **overlay**: bottom-sheet, modal-dialog, autocomplete, chart-tooltip, command-palette, command-result-item, user-menu

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

- No validation issues.

## 14. Quick Start

이 문서는 **PL Stats System**의 디자인 시스템 사양입니다.

### 시작하기

1. **토큰 적용**: Drop-in CSS(아래 섹션 16)의 CSS 변수를 프로젝트에 복사합니다.
2. **컬러 세팅**: Color Reference(섹션 6)의 semantic role을 기준으로 surface/text/border를 잡습니다.
3. **타이포 세팅**: Token Strategy(섹션 5)의 font family와 type scale을 적용합니다.
4. **시각 방향 확인**: Visual Reference Signals(섹션 7)에서 density/surface/layout cue를 먼저 확인합니다.
5. **컴포넌트 구현**: Component Strategy(섹션 8)의 family 순서대로 하나씩 빌드합니다.

### 우선순위

핵심 primitive: **dashboard cards, data tables, workspace navigation, search and filter, charts and visualization**

이 primitive를 지원하는 컴포넌트부터 구현하고, 나머지는 필요에 따라 확장합니다.

## 15. DO / DON'T

### DO

- **Bold with Discipline**: 강한 accent 색상 1개 중심
- **Precision Over Ornament**: 명확한 상태 규칙
- **Energetic**: energetic와 충돌하는 컴포넌트 변형은 만들지 않기
- 모든 시각적 선택에서 **bold, precise, energetic** 기준을 적용
- semantic token을 통해 컬러를 적용 (하드코딩 금지)
- 접근성 기준을 모든 text/surface 조합에서 먼저 검증
- 컴포넌트 변형 추가 전 기존 variant로 해결 가능한지 먼저 확인
- 아이콘은 SVG 컴포넌트 또는 Lucide/Heroicons/Phosphor/Tabler 등 라이브러리로 구현
- component_specs.md의 anatomy/states/token binding을 그대로 따라 완전히 구현

### DON'T

- **generic** 방향의 디자인 결정을 하지 않음
- **cluttered** 방향의 디자인 결정을 하지 않음
- **childish** 방향의 디자인 결정을 하지 않음
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
  --font-heading: 'Spoqa Han Sans Neo', serif;
  --font-body: 'Spoqa Han Sans Neo', sans-serif;
  --font-mono: 'JetBrains Mono', monospace;
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
  --color-primary: #E90052;
  --color-accent: #00FF85;
  --color-surface-tint: #FFD700;

  /* --- Semantic roles (expanded) --- */
  --color-brand-primary: #E90052;
  --color-brand-accent: #00FF85;
  --color-surface-tint: #FFD700;
  --color-canvas: #FFFFFF;
  --color-surface: #FFFFFF;
  --color-surface-muted: #EEF1F6;
  --color-surface-elevated: #FFFFFF;
  --color-border: #D6DDE6;
  --color-border-strong: #B0BAC7;
  --color-ink: #1A1A2E;
  --color-ink-muted: #4A4A5E;
  --color-ink-subtle: #78909C;
  --color-ink-inverse: #FFFFFF;
  --color-primary-support: #FF1744;
  --color-accent-support: #00C853;
  --color-info: #1A1A2E;
  --color-success: #00C853;
  --color-warning: #FF8C00;
  --color-danger: #E90052;
  --color-link: #E90052;
  --color-link-hover: #C00044;

  /* --- Button — primary --- */
  --color-button-primary-surface-default: #E90052;
  --color-button-primary-surface-hover: #CA0047;
  --color-button-primary-surface-active: #B60040;
  --color-button-primary-surface-disabled: #F699BA;
  --color-button-primary-text-default: #FFFFFF;
  --color-button-primary-text-disabled: #FFFFFF;
  --color-button-primary-border-default: #E90052;
  --color-button-primary-focus-ring: #E90052;

  /* --- Button — secondary --- */
  --color-button-secondary-surface-default: #FFFFFF;
  --color-button-secondary-surface-hover: #F1F1F2;
  --color-button-secondary-surface-active: #E8E8EA;
  --color-button-secondary-surface-disabled: #FFFFFF;
  --color-button-secondary-text-default: #1A1A2E;
  --color-button-secondary-text-disabled: #9898A1;
  --color-button-secondary-border-default: #BDC8D7;
  --color-button-secondary-border-hover: #A3B3C7;
  --color-button-secondary-focus-ring: #E90052;

  /* --- Button — ghost --- */
  --color-button-ghost-surface-default: transparent;
  --color-button-ghost-surface-hover: #F4F4F5;
  --color-button-ghost-surface-active: #EAEAEC;
  --color-button-ghost-surface-disabled: transparent;
  --color-button-ghost-text-default: #4A4A5E;
  --color-button-ghost-text-hover: #1A1A2E;
  --color-button-ghost-text-disabled: #AEAEB7;
  --color-button-ghost-border-default: transparent;
  --color-button-ghost-focus-ring: #E90052;

  /* --- Button — danger --- */
  --color-button-danger-surface-default: #E90052;
  --color-button-danger-surface-hover: #CA0047;
  --color-button-danger-surface-active: #B60040;
  --color-button-danger-text-default: #FFFFFF;
  --color-button-danger-border-default: #E90052;
  --color-button-danger-focus-ring: #E90052;

  /* --- Input --- */
  --color-input-surface-default: #FFFFFF;
  --color-input-surface-filled: #FFFFFF;
  --color-input-surface-disabled: #FFFFFF;
  --color-input-text-default: #1A1A2E;
  --color-input-text-placeholder: #92929E;
  --color-input-text-disabled: #AEAEB7;
  --color-input-border-default: #D6DDE6;
  --color-input-border-hover: #B6C3D3;
  --color-input-border-focus: #E90052;
  --color-input-border-error: #E90052;
  --color-input-border-disabled: #E6EAF0;

  /* --- Card --- */
  --color-card-surface-default: #FFFFFF;
  --color-card-surface-hover: #FAFAFB;
  --color-card-surface-muted: #FFFFFF;
  --color-card-border-default: #D6DDE6;
  --color-card-border-hover: #B6C3D3;
  --color-card-border-focus: #E90052;

  /* --- Nav link --- */
  --color-nav-link-text-default: #4A4A5E;
  --color-nav-link-text-hover: #1A1A2E;
  --color-nav-link-text-active: #E90052;
  --color-nav-link-surface-hover: #F6F6F7;
  --color-nav-link-indicator: #00FF85;

  /* --- Link --- */
  --color-link-text-default: #E90052;
  --color-link-text-hover: #B60040;
  --color-link-text-visited: #BB154F;

  /* --- Feedback — info --- */
  --color-feedback-info-surface: #E4E4E6;
  --color-feedback-info-text: #1A1A2E;
  --color-feedback-info-border: #5F5F6D;
  --color-feedback-info-icon: #1A1A2E;

  /* --- Feedback — success --- */
  --color-feedback-success-surface: #E0F8EA;
  --color-feedback-success-text: #00C853;
  --color-feedback-success-border: #4DD887;
  --color-feedback-success-icon: #00C853;

  /* --- Feedback — warning --- */
  --color-feedback-warning-surface: #FFF1E0;
  --color-feedback-warning-text: #FF8C00;
  --color-feedback-warning-border: #FFAE4D;
  --color-feedback-warning-icon: #FF8C00;

  /* --- Feedback — danger --- */
  --color-feedback-danger-surface: #FCE0EA;
  --color-feedback-danger-text: #E90052;
  --color-feedback-danger-border: #F04D86;
  --color-feedback-danger-icon: #E90052;

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
| activity-card | `color.Golden Score→background`, `spacing.12→padding`, `radius.md→radius`, `color.Golden Score→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo`, `font:Spoqa Han Sans Neo` |
| app-shell | `color.Golden Score→background`, `spacing.12→padding`, `radius.md→radius`, `color.Matchday Red→surface`, `color.Electric Green→emphasis`, `color.Golden Score→background`, `spacing.12→padding`, `radius.md→radius` |
| autocomplete | `color.Matchday Red→surface`, `color.Electric Green→emphasis`, `color.Golden Score→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo` |
| avatar | `color.Golden Score→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo` |
| back-button | `color.Matchday Red→surface`, `color.Electric Green→emphasis`, `color.Golden Score→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo` |
| bottom-sheet | `color.Matchday Red→surface`, `color.Electric Green→emphasis`, `color.Golden Score→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo` |
| breadcrumb | `color.Matchday Red→surface`, `color.Electric Green→emphasis`, `color.Golden Score→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo` |
| calendar-grid | `color.Golden Score→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo` |
| chart-container | `color.Golden Score→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo` |
| chart-legend | `color.Golden Score→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo` |
| chart-tooltip | `color.Matchday Red→surface`, `color.Electric Green→emphasis`, `color.Golden Score→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo` |
| checkbox | `color.Matchday Red→surface`, `color.Electric Green→emphasis`, `color.Golden Score→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo` |
| chip | `color.Matchday Red→surface`, `color.Electric Green→emphasis`, `color.Golden Score→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo` |
| column-header | `color.Golden Score→background`, `spacing.12→padding`, `radius.md→radius`, `color.Golden Score→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo`, `font:Spoqa Han Sans Neo` |
| command-palette | `color.Matchday Red→surface`, `color.Electric Green→emphasis`, `color.Golden Score→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo` |
| command-result-item | `color.Matchday Red→surface`, `color.Electric Green→emphasis`, `color.Golden Score→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo` |
| cta-button | `color.Matchday Red→surface`, `color.Electric Green→emphasis`, `color.Golden Score→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo` |
| data-table | `color.Golden Score→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo` |
| date-picker | `color.Matchday Red→surface`, `color.Electric Green→emphasis`, `color.Golden Score→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo` |
| date-range-picker | `color.Matchday Red→surface`, `color.Electric Green→emphasis`, `color.Golden Score→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo` |
| empty-state | `color.Golden Score→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo` |
| filter-chip | `color.Golden Score→background`, `spacing.12→padding`, `radius.md→radius`, `color.Matchday Red→surface`, `color.Electric Green→emphasis`, `color.Golden Score→background`, `spacing.12→padding`, `radius.md→radius` |
| filter-panel | `color.Matchday Red→surface`, `color.Electric Green→emphasis`, `color.Golden Score→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo` |
| form-actions | `color.Matchday Red→surface`, `color.Electric Green→emphasis`, `color.Golden Score→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo` |
| form-section | `color.Matchday Red→surface`, `color.Electric Green→emphasis`, `color.Golden Score→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo` |
| ghost-button | `color.Matchday Red→surface`, `color.Electric Green→emphasis`, `color.Golden Score→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo` |
| hero-container | `color.Golden Score→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo` |
| hero-cta-group | `color.Matchday Red→surface`, `color.Electric Green→emphasis`, `color.Golden Score→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo` |
| hero-eyebrow | `color.Golden Score→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo` |
| hero-headline | `color.Golden Score→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo` |
| hero-subheadline | `color.Golden Score→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo` |
| hero-trust-strip | `color.Golden Score→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo` |
| hero-visual | `color.Golden Score→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo` |
| icon-button | `color.Matchday Red→surface`, `color.Electric Green→emphasis`, `color.Golden Score→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo` |
| inline-alert | `color.Golden Score→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo` |
| insight-card | `color.Golden Score→background`, `spacing.12→padding`, `radius.md→radius`, `color.Golden Score→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo`, `font:Spoqa Han Sans Neo` |
| kanban-board | `color.Golden Score→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo` |
| kanban-card | `color.Golden Score→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo` |
| kanban-column | `color.Golden Score→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo` |
| link-button | `color.Matchday Red→surface`, `color.Electric Green→emphasis`, `color.Golden Score→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo` |
| mobile-tab-bar | `color.Matchday Red→surface`, `color.Electric Green→emphasis`, `color.Golden Score→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo` |
| mobile-topbar | `color.Matchday Red→surface`, `color.Electric Green→emphasis`, `color.Golden Score→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo` |
| modal-dialog | `color.Matchday Red→surface`, `color.Electric Green→emphasis`, `color.Golden Score→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo` |
| pagination | `color.Golden Score→background`, `spacing.12→padding`, `radius.md→radius`, `color.Matchday Red→surface`, `color.Electric Green→emphasis`, `color.Golden Score→background`, `spacing.12→padding`, `radius.md→radius` |
| primary-button | `color.Matchday Red→surface`, `color.Electric Green→emphasis`, `color.Golden Score→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo` |
| profile-card | `color.Golden Score→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo` |
| radio-group | `color.Matchday Red→surface`, `color.Electric Green→emphasis`, `color.Golden Score→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo` |
| row-actions | `color.Golden Score→background`, `spacing.12→padding`, `radius.md→radius`, `color.Golden Score→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo`, `font:Spoqa Han Sans Neo` |
| search-field | `color.Matchday Red→surface`, `color.Electric Green→emphasis`, `color.Golden Score→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo` |
| search-results | `color.Golden Score→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo` |
| secondary-button | `color.Matchday Red→surface`, `color.Electric Green→emphasis`, `color.Golden Score→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo` |
| section-header | `color.Golden Score→background`, `spacing.12→padding`, `radius.md→radius`, `color.Golden Score→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo`, `font:Spoqa Han Sans Neo` |
| section-tabs | `color.Matchday Red→surface`, `color.Electric Green→emphasis`, `color.Golden Score→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo` |
| segmented-control | `color.Matchday Red→surface`, `color.Electric Green→emphasis`, `color.Golden Score→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo` |
| select | `color.Matchday Red→surface`, `color.Electric Green→emphasis`, `color.Golden Score→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo` |
| shortcut-hint | `color.Golden Score→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo` |
| sidebar-nav | `color.Matchday Red→surface`, `color.Electric Green→emphasis`, `color.Golden Score→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo` |
| stat-card | `color.Golden Score→background`, `spacing.12→padding`, `radius.md→radius`, `color.Golden Score→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo`, `font:Spoqa Han Sans Neo` |
| status-badge | `color.Golden Score→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo` |
| tab-bar | `color.Matchday Red→surface`, `color.Electric Green→emphasis`, `color.Golden Score→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo` |
| tag | `color.Golden Score→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo` |
| text-field | `color.Matchday Red→surface`, `color.Electric Green→emphasis`, `color.Golden Score→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo` |
| textarea | `color.Matchday Red→surface`, `color.Electric Green→emphasis`, `color.Golden Score→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo` |
| time-picker | `color.Matchday Red→surface`, `color.Electric Green→emphasis`, `color.Golden Score→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo` |
| toast | `color.Golden Score→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo` |
| topbar | `color.Matchday Red→surface`, `color.Electric Green→emphasis`, `color.Golden Score→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo` |
| user-menu | `color.Matchday Red→surface`, `color.Electric Green→emphasis`, `color.Golden Score→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo` |
| workspace-switcher | `color.Matchday Red→surface`, `color.Electric Green→emphasis`, `color.Golden Score→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo` |

## 19. Contrast Audit

| Background | Foreground | Ratio | Level |
|------------|------------|-------|-------|
| Electric Green | Ink | 14.07:1 | AAA (pass) |
| Golden Score | Ink | 13.46:1 | AAA (pass) |
| Matchday Red | Paper | 4.58:1 | AA (pass) |
| Matchday Red | Ink | 4.12:1 | AA-large (large-only) |
| Matchday Red | Electric Green | 3.41:1 | AA-large (large-only) |
| Matchday Red | Golden Score | 3.26:1 | AA-large (large-only) |
| Golden Score | Paper | 1.40:1 | fail (FAIL) |
| Electric Green | Paper | 1.34:1 | fail (FAIL) |
| Electric Green | Golden Score | 1.04:1 | fail (FAIL) |

## 20. Pattern Catalog

### Layout Patterns

- **dashboard cards**: stat-card, insight-card, activity-card, section-header
- **data tables**: data-table, column-header, filter-chip, row-actions, pagination
- **workspace navigation**: app-shell, sidebar-nav, topbar, breadcrumb, workspace-switcher, tab-bar
- **charts and visualization**: chart-container, chart-tooltip, chart-legend
- **tags and labels**: tag, status-badge, chip

### Interaction Patterns

- **search and filter**: search-results, filter-panel, autocomplete
- **command palette**: command-palette, command-result-item, shortcut-hint
- **forms**: text-field, select, checkbox, textarea, form-section, radio-group, form-actions
- **notifications**: toast, inline-alert, empty-state
