# Glacier System Spec

## 1. Positioning

- **Brand**: Glacier
- **Product**: 개발팀을 위한 코드와 데이터 아카이브 서비스. 장기 보관, 검증된 복원, 감사 로그.
- **Audience**: 플랫폼 엔지니어, SRE / DevOps, 데이터 플랫폼 팀
- **Platforms**: web
- **Accessibility floor**: WCAG 2.2 AA

## 2. Identity Guardrails

- **Brand keywords**: precise, resilient, minimal, technical
- **Anti-keywords**: playful, decorative, warm, noisy
- **Tone of voice**: direct, technical, measured
- **Visual direction**: mono-weight icons, dense data tables, text-first hierarchy, low-chroma surfaces
- **Interaction direction**: predictable states, zero-surprise motion, keyboard-first

## 3. Design Principles

- **Precision Over Ornament**: 장식보다 정보의 정렬, 상태의 정확성, 반응의 일관성을 우선합니다.
- **Resilient**: `resilient`를 시각적 선택과 인터랙션 선택의 기본 기준으로 삼습니다.
- **Minimal**: `minimal`를 시각적 선택과 인터랙션 선택의 기본 기준으로 삼습니다.
- **Technical**: `technical`를 시각적 선택과 인터랙션 선택의 기본 기준으로 삼습니다.

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
- **Product type detected**: saas
- **Pairing source**: auto-scored
- **Line height**: normal
- **Type scale**: base 15px, ratio 1.25 (xs=12px, sm=13px, md=15px, lg=19px, xl=24px, 2xl=30px, 3xl=37px)
- **Strategy**:
  - 단일 서체(Spoqa Han Sans Neo)로 weight 대비 위계 — 일관성 우선
  - 한글 서체: Spoqa Han Sans Neo — 라틴과 x-height/weight 조화
  - 모노스페이스: JetBrains Mono — 코드/데이터 영역 전용
  - precise 키워드 → tight letter-spacing, tabular figures 권장
- **Heading note**: 스포카에서 만든 한글 산세리프. Source Sans Pro 기반. 깔끔한 데이터 UI에 적합.
- **Body note**: 스포카에서 만든 한글 산세리프. Source Sans Pro 기반. 깔끔한 데이터 UI에 적합.
- **Korean rationale**: Spoqa Han Sans Neo — Pretendard 이전 시대의 한글 UI 표준. 요기요, 여기어때 등에서 사용. 깔끔하지만 weight 범위와 Variable 미지원이 아쉬움. 신규 프로젝트에서는 Pretendard 추천.
- **Heading tracking**: xl=-0.015em, 2xl=-0.02em, 3xl=-0.02em
- **Primary script**: korean
- **Hangul headline defaults**: Spoqa Han Sans Neo | line-height 1.2-1.3 | tracking -0.02em
- **Hangul body defaults**: Spoqa Han Sans Neo | line-height 1.5-1.6 | label line-height 1.4-1.5
- **Wrap defaults**: headline word-break=keep-all, headline text-wrap=balance, body word-break=keep-all
- **Scale guidance**: 기본 스케일을 사용할 수 있지만 한글 문장 기준으로 실제 wrap을 먼저 검증한다.
- **Hangul warning**: 장문 본문 — line-height 여유 부족
- **Hangul warning**: 감성적 브랜딩
- **Hangul warning**: 장문 본문 — line-height 여유 부족
- **Loading**: Spoqa Han Sans Neo(preload), JetBrains Mono(lazy) | display: swap

## 6. Color Reference

- **Source**: REFERENCE X Vol.1 - Color Reference (/Users/sungwoon/Documents/designSystem/docs/color-reference.md)
- **Selection mode**: brand-guided
- **Preferred families**: Deep Blues, Natural Blues, Standard Blues
- **Palette strategy**: temperature=mixed, contrast=balanced, diversity=balanced, surface_style=tinted
- **Palette expansion**: supporting_color_count=8, combination_count=3, prefer_pairings=True
- **Active palette**: signature-1
- **Active roles**:
  - `primary` -> Navy Blue #000080 / Deep Blues
  - `accent` -> Ochre #CC7722 / Standard Oranges
  - `surface_tint` -> Sky Blue #87CEEB / Natural Blues
- **Selected colors**:
  - Navy Blue #000080 / Deep Blues / 저명도, 중채도, 차가운 온도감이 강한 블루 계열 / 신뢰, 권위, 집중, 전문성, 절제된 우아함
  - Ochre #CC7722 / Standard Oranges / 중명도, 중채도, 흙기 섞인 따뜻한 오렌지 / 안정감, 내추럴, 신뢰감, 지속성
  - Sky Blue #87CEEB / Natural Blues / 고명도, 중채도의 밝은 쿨톤 / 청량함, 평화, 유연함, 긍정, 맑음
- **Palette candidates**:
  - signature-1 (Signature): primary=Navy Blue, accent=Ochre, surface_tint=Sky Blue / Navy Blue is inside preferred families.; Ochre matches brand tone keywords.
  - soft-spread-2 (Soft Spread): primary=Navy Blue, accent=Ochre, surface_tint=Ocean Blue / Navy Blue is inside preferred families.; Ochre matches brand tone keywords.
  - assertive-3 (Assertive): primary=Navy Blue, accent=Classic Blue, surface_tint=Sky Blue / Navy Blue is inside preferred families.; Classic Blue matches brand tone keywords.
- **Expanded supporting colors**:
  - Pairing #708090 #708090 / Derived Pairing / pairing-swatch / Pairing #708090 comes from the seed pairing references.; Pairing #708090 is explicitly paired with Navy Blue.
  - Pairing #B0C4DE #B0C4DE / Derived Pairing / pairing-swatch / Pairing #B0C4DE comes from the seed pairing references.; Pairing #B0C4DE is explicitly paired with Navy Blue.
  - Pairing #1C2E4A #1C2E4A / Derived Pairing / pairing-swatch / Pairing #1C2E4A comes from the seed pairing references.; Pairing #1C2E4A is explicitly paired with Ochre.
  - Pairing #4C7A77 #4C7A77 / Derived Pairing / pairing-swatch / Pairing #4C7A77 comes from the seed pairing references.; Pairing #4C7A77 is explicitly paired with Ochre.
  - Classic Blue #0F4C81 / Pantone Trend Blues / reference-color / Classic Blue reinforces the brand mood signals.
  - Pairing #333333 #333333 / Derived Pairing / pairing-swatch / Pairing #333333 comes from the seed pairing references.; Pairing #333333 is explicitly paired with Sky Blue.
  - Pairing #6E7B8B #6E7B8B / Derived Pairing / pairing-swatch / Pairing #6E7B8B comes from the seed pairing references.; Pairing #6E7B8B is explicitly paired with Ochre.
  - Pairing #B6E3C1 #B6E3C1 / Derived Pairing / pairing-swatch / Pairing #B6E3C1 comes from the seed pairing references.; Pairing #B6E3C1 is explicitly paired with Sky Blue.
- **Expanded semantic roles**:
  - `brand_primary` -> Navy Blue #000080 / Deep Blues
  - `brand_accent` -> Ochre #CC7722 / Standard Oranges
  - `surface_tint` -> Sky Blue #87CEEB / Natural Blues
  - `canvas` -> Canvas White #F7F8FA / Generated Fallback
  - `surface` -> Paper #FFFFFF / Generated Fallback
  - `surface_muted` -> Surface Muted #EEF1F6 / Generated Fallback
  - `surface_elevated` -> Paper #FFFFFF / Generated Fallback
  - `border` -> Border Neutral #D6DDE6 / Generated Fallback
  - `border_strong` -> Border Strong #B0BAC7 / Generated Fallback
  - `ink` -> Pairing #1C2E4A #1C2E4A / Derived Pairing
- **Combination lists**:
  - Seed Core: primary=Navy Blue, accent=Ochre, surface_tint=Sky Blue
  - Surface System: canvas=Canvas White, surface=Paper, surface_tint=Sky Blue, border=Border Neutral, ink=Pairing #1C2E4A, ink_muted=Pairing #708090
  - Support Spectrum: support=Pairing #708090, support=Pairing #B0C4DE, support=Pairing #1C2E4A, support=Pairing #4C7A77, support=Classic Blue, support=Pairing #333333
- **Notes**: Glacier는 차가운 중성톤 중심의 최소주의 시스템, raw reference color를 그대로 전체 UI에 덮지 않기, 팔레트 확장은 semantic state와 surface tier 생성에만 사용
- **Application rule**: 레퍼런스 컬러는 semantic token으로 번역해서 사용하고, 접근성과 theme 호환성을 우선합니다.

## 7. Visual Reference Signals

- **Mode**: pinterest-assisted
- **Coverage**: source 1 / image 2 / selected 2
- **Rule**: visual references are advisory signals for motif and layout direction; official KB/spec remain the structural source of truth.
- **Provenance**: `observed` = directly measured from local pixels, `inferred` = synthesized from image/query/brand signals, `unverified` = reliable visual evidence not yet available.
- **Query seeds**: technical archive dashboard ui, dense audit log table interface, minimal enterprise landing page
### Visual Direction

- **Density**: dense (confidence 0.94, provenance inferred) / dashboard x4, table x3, ops x1
- **Surface Style**: flat (confidence 0.6, provenance inferred) / minimal x4
- **Corner Style**: round (confidence 0.43, provenance inferred) / soft x1, svg corner ratio 0.50
- **Typography Mood**: utilitarian (confidence 0.94, provenance inferred) / dashboard x4, enterprise x2, ops x1
- **Color balance**: temperature=cool, contrast=high, neutral_bias=low, provenance=observed / dominant #0B1623, #22354B, #29435C

### Layout Rhythm

- **Dashboard grid**: confidence 0.94 / provenance inferred / dashboard x4, table x3, ops x1, 3:2-ish x2
- **Data review surface**: confidence 0.94 / provenance inferred / table x3, grid x2, audit x5, log x3
- **Narrative landing flow**: confidence 0.94 / provenance inferred / landing x2, hero x1, pricing x1, testimonial x1
- **Split-pane workspace**: confidence 0.62 / provenance inferred / command x1, dashboard x4, 3:2-ish x2

### Image-derived Component Hints

- **Cards**: flat card planes를 기본으로 하고, 압축된 spacing과 얇은 divider 중심의 hierarchy. soft round corner를 기본값으로 유지. / provenance inferred / surface=flat, density=dense, corner=round
- **Navigation**: 고정 sidebar 또는 split-pane navigation을 우선하고, 현재 위치와 scope를 항상 명시한다. / provenance inferred / Split-pane workspace
- **Typography**: 정보 밀도에 맞춰 type scale 차이를 줄이고 table/list label의 정렬 정확도를 우선한다. / provenance inferred / typography_mood=utilitarian
- **Data Display**: 정보 밀도를 유지하되 thin dividers와 restrained accent로 hierarchy를 만든다. / provenance inferred / layout=dashboard-grid, density=dense

### Synthesis Notes

- layout는 Dashboard grid 기준으로 정리
- surface language는 flat 성향 우선
- typography mood는 utilitarian 축 유지
- density는 dense 기준으로 primitive spacing 조정
- palette temperature는 cool 쪽을 우선
- Avoid: warm playful gradients
- Avoid: soft whimsical illustrations
- Avoid: exaggerated glassmorphism

## 8. Component Strategy

- **Product primitives**: archive browser, restore workflow, audit log, data tables, command palette, dashboard cards, hero section, feature grid, social proof, testimonial, faq accordion, landing cta section, site footer, site header, pricing and plans
- **Required families**: button, data-display, feedback, input, marketing, navigation, foundation, overlay
- **Visual-reference archetypes**:

- **Dashboard insight module** (data-display / 0.94): stat-card, insight-card, chart-panel, section-header, filter-chip
- **Data review table** (data-display / 0.94): data-table, column-header, row-actions, filter-toolbar, pagination
- **Marketing hero stack** (marketing / 0.94): hero-section, hero-headline, hero-visual, cta-button-group, trust-strip
- **Workspace shell** (navigation / 0.48): app-shell, sidebar-nav, workspace-switcher, breadcrumb, context-panel

- **button**: primary-button, secondary-button, ghost-button, icon-button, cta-button, link-button, form-actions, hero-cta-group
- **data-display**: data-table, column-header, row-actions, pricing-card, feature-comparison, kanban-board, kanban-column, kanban-card / visual signals: Dashboard insight module (0.94), Data review table (0.94)
- **feedback**: filter-chip, inline-alert, empty-state, toast, upgrade-banner, status-badge, step-progress, shortcut-hint
- **input**: text-field, search-field, segmented-control, filter-chip, textarea, select, checkbox, radio-group
- **marketing**: hero-container, hero-eyebrow, hero-headline, hero-subheadline, hero-visual, hero-trust-strip, faq-section, faq-item / visual signals: Marketing hero stack (0.94)
- **navigation**: scope-switcher, mobile-topbar, mobile-tab-bar, back-button, section-tabs, pagination, app-shell, sidebar-nav
- **foundation**: column-header, row-actions, pagination, command-result-item, shortcut-hint, stat-card, insight-card, activity-card
- **overlay**: command-palette, bottom-sheet, modal-dialog, autocomplete, tooltip-guide, user-menu, confirm-dialog, command-result-item

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

- Warning: [pitfall#3-rebrand] Navy Blue vs Sky Blue (blue): lightness diff 47, saturation diff 29 — possible rebrand remnant

## 14. Quick Start

이 문서는 **Glacier System**의 디자인 시스템 사양입니다.

### 시작하기

1. **토큰 적용**: Drop-in CSS(아래 섹션 16)의 CSS 변수를 프로젝트에 복사합니다.
2. **컬러 세팅**: Color Reference(섹션 6)의 semantic role을 기준으로 surface/text/border를 잡습니다.
3. **타이포 세팅**: Token Strategy(섹션 5)의 font family와 type scale을 적용합니다.
4. **시각 방향 확인**: Visual Reference Signals(섹션 7)에서 density/surface/layout cue를 먼저 확인합니다.
5. **컴포넌트 구현**: Component Strategy(섹션 8)의 family 순서대로 하나씩 빌드합니다.

### 우선순위

핵심 primitive: **archive browser, restore workflow, audit log, data tables, command palette**

이 primitive를 지원하는 컴포넌트부터 구현하고, 나머지는 필요에 따라 확장합니다.

## 15. DO / DON'T

### DO

- **Precision Over Ornament**: 명확한 상태 규칙
- **Resilient**: resilient와 충돌하는 컴포넌트 변형은 만들지 않기
- **Minimal**: minimal와 충돌하는 컴포넌트 변형은 만들지 않기
- **Technical**: technical와 충돌하는 컴포넌트 변형은 만들지 않기
- 모든 시각적 선택에서 **precise, resilient, minimal** 기준을 적용
- semantic token을 통해 컬러를 적용 (하드코딩 금지)
- 접근성 기준을 모든 text/surface 조합에서 먼저 검증
- 컴포넌트 변형 추가 전 기존 variant로 해결 가능한지 먼저 확인
- 아이콘은 SVG 컴포넌트 또는 Lucide/Heroicons/Phosphor/Tabler 등 라이브러리로 구현
- component_specs.md의 anatomy/states/token binding을 그대로 따라 완전히 구현

### DON'T

- **playful** 방향의 디자인 결정을 하지 않음
- **decorative** 방향의 디자인 결정을 하지 않음
- **warm** 방향의 디자인 결정을 하지 않음
- **noisy** 방향의 디자인 결정을 하지 않음
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
  --color-primary: #000080;
  --color-accent: #CC7722;
  --color-surface-tint: #87CEEB;

  /* --- Semantic roles (expanded) --- */
  --color-brand-primary: #000080;
  --color-brand-accent: #CC7722;
  --color-surface-tint: #87CEEB;
  --color-canvas: #F7F8FA;
  --color-surface: #FFFFFF;
  --color-surface-muted: #EEF1F6;
  --color-surface-elevated: #FFFFFF;
  --color-border: #D6DDE6;
  --color-border-strong: #B0BAC7;
  --color-ink: #1C2E4A;
  --color-ink-muted: #708090;
  --color-ink-subtle: #708090;
  --color-ink-inverse: #FFFFFF;
  --color-primary-support: #708090;
  --color-accent-support: #CC7722;
  --color-info: #708090;
  --color-success: #B6E3C1;
  --color-warning: #CC7722;
  --color-danger: #8B2252;
  --color-link: #000080;
  --color-link-hover: #000057;

  /* --- Button — primary --- */
  --color-button-primary-surface-default: #000080;
  --color-button-primary-surface-hover: #000061;
  --color-button-primary-surface-active: #00004D;
  --color-button-primary-surface-disabled: #9495C9;
  --color-button-primary-text-default: #FFFFFF;
  --color-button-primary-text-disabled: #FBFCFC;
  --color-button-primary-border-default: #000080;
  --color-button-primary-focus-ring: #000080;

  /* --- Button — secondary --- */
  --color-button-secondary-surface-default: #FFFFFF;
  --color-button-secondary-surface-hover: #F1F2F4;
  --color-button-secondary-surface-active: #E8EAED;
  --color-button-secondary-surface-disabled: #F7F8FA;
  --color-button-secondary-text-default: #1C2E4A;
  --color-button-secondary-text-disabled: #949DAB;
  --color-button-secondary-border-default: #BDC8D7;
  --color-button-secondary-border-hover: #A3B3C7;
  --color-button-secondary-focus-ring: #000080;

  /* --- Button — ghost --- */
  --color-button-ghost-surface-default: transparent;
  --color-button-ghost-surface-hover: #F4F5F6;
  --color-button-ghost-surface-active: #EBECEF;
  --color-button-ghost-surface-disabled: transparent;
  --color-button-ghost-text-default: #708090;
  --color-button-ghost-text-hover: #1C2E4A;
  --color-button-ghost-text-disabled: #BAC2CA;
  --color-button-ghost-border-default: transparent;
  --color-button-ghost-focus-ring: #000080;

  /* --- Button — danger --- */
  --color-button-danger-surface-default: #8B2252;
  --color-button-danger-surface-hover: #721C43;
  --color-button-danger-surface-active: #62183A;
  --color-button-danger-text-default: #FFFFFF;
  --color-button-danger-border-default: #8B2252;
  --color-button-danger-focus-ring: #8B2252;

  /* --- Input --- */
  --color-input-surface-default: #FFFFFF;
  --color-input-surface-filled: #FFFFFF;
  --color-input-surface-disabled: #F7F8FA;
  --color-input-text-default: #1C2E4A;
  --color-input-text-placeholder: #A6B0BA;
  --color-input-text-disabled: #BAC2CA;
  --color-input-border-default: #D6DDE6;
  --color-input-border-hover: #B6C3D3;
  --color-input-border-focus: #000080;
  --color-input-border-error: #8B2252;
  --color-input-border-disabled: #E6EAF0;

  /* --- Card --- */
  --color-card-surface-default: #FFFFFF;
  --color-card-surface-hover: #FAFBFB;
  --color-card-surface-muted: #F7F8FA;
  --color-card-border-default: #D6DDE6;
  --color-card-border-hover: #B6C3D3;
  --color-card-border-focus: #000080;

  /* --- Nav link --- */
  --color-nav-link-text-default: #708090;
  --color-nav-link-text-hover: #1C2E4A;
  --color-nav-link-text-active: #000080;
  --color-nav-link-surface-hover: #F6F7F8;
  --color-nav-link-indicator: #CC7722;

  /* --- Link --- */
  --color-link-text-default: #000080;
  --color-link-text-hover: #00004D;
  --color-link-text-visited: #0A0A5C;

  /* --- Feedback — info --- */
  --color-feedback-info-surface: #EEF0F2;
  --color-feedback-info-text: #708090;
  --color-feedback-info-border: #98A4B0;
  --color-feedback-info-icon: #708090;

  /* --- Feedback — success --- */
  --color-feedback-success-surface: #F6FCF8;
  --color-feedback-success-text: #B6E3C1;
  --color-feedback-success-border: #CAE9D2;
  --color-feedback-success-icon: #B6E3C1;

  /* --- Feedback — warning --- */
  --color-feedback-warning-surface: #F9EFE4;
  --color-feedback-warning-text: #CC7722;
  --color-feedback-warning-border: #D99E63;
  --color-feedback-warning-icon: #CC7722;

  /* --- Feedback — danger --- */
  --color-feedback-danger-surface: #F1E4EA;
  --color-feedback-danger-text: #8B2252;
  --color-feedback-danger-border: #AB6284;
  --color-feedback-danger-icon: #8B2252;

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
| activity-card | `color.Sky Blue→background`, `spacing.12→padding`, `radius.md→radius`, `color.Sky Blue→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo`, `font:Spoqa Han Sans Neo` |
| app-shell | `color.Navy Blue→surface`, `color.Ochre→emphasis`, `color.Sky Blue→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo` |
| autocomplete | `color.Navy Blue→surface`, `color.Ochre→emphasis`, `color.Sky Blue→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo` |
| avatar | `color.Sky Blue→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo` |
| back-button | `color.Navy Blue→surface`, `color.Ochre→emphasis`, `color.Sky Blue→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo` |
| banner | `color.Sky Blue→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo` |
| bottom-sheet | `color.Navy Blue→surface`, `color.Ochre→emphasis`, `color.Sky Blue→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo` |
| breadcrumb | `color.Navy Blue→surface`, `color.Ochre→emphasis`, `color.Sky Blue→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo` |
| calendar-grid | `color.Sky Blue→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo` |
| chart-panel | `color.Sky Blue→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo` |
| checkbox | `color.Navy Blue→surface`, `color.Ochre→emphasis`, `color.Sky Blue→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo` |
| chip | `color.Navy Blue→surface`, `color.Ochre→emphasis`, `color.Sky Blue→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo` |
| column-header | `color.Sky Blue→background`, `spacing.12→padding`, `radius.md→radius`, `color.Sky Blue→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo`, `font:Spoqa Han Sans Neo` |
| command-palette | `color.Navy Blue→surface`, `color.Ochre→emphasis`, `color.Sky Blue→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo` |
| command-result-item | `color.Sky Blue→background`, `spacing.12→padding`, `radius.md→radius`, `color.Navy Blue→surface`, `color.Ochre→emphasis`, `color.Sky Blue→background`, `spacing.12→padding`, `radius.md→radius` |
| confirm-dialog | `color.Navy Blue→surface`, `color.Ochre→emphasis`, `color.Sky Blue→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo` |
| cta-button | `color.Navy Blue→surface`, `color.Ochre→emphasis`, `color.Sky Blue→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo` |
| cta-button-group | `color.Navy Blue→surface`, `color.Ochre→emphasis`, `color.Sky Blue→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo` |
| cta-headline | `color.Sky Blue→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo` |
| cta-section | `color.Sky Blue→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo` |
| cta-supporting-text | `color.Sky Blue→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo` |
| customer-logo | `color.Sky Blue→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo` |
| data-table | `color.Sky Blue→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo` |
| date-picker | `color.Navy Blue→surface`, `color.Ochre→emphasis`, `color.Sky Blue→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo` |
| date-range-picker | `color.Navy Blue→surface`, `color.Ochre→emphasis`, `color.Sky Blue→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo` |
| empty-state | `color.Sky Blue→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo` |
| faq-answer | `color.Sky Blue→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo` |
| faq-item | `color.Sky Blue→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo` |
| faq-question | `color.Sky Blue→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo` |
| faq-section | `color.Sky Blue→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo` |
| feature-card | `color.Sky Blue→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo` |
| feature-comparison | `color.Sky Blue→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo` |
| feature-description | `color.Sky Blue→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo` |
| feature-grid | `color.Sky Blue→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo` |
| feature-icon | `color.Sky Blue→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo` |
| feature-section | `color.Sky Blue→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo` |
| feature-title | `color.Sky Blue→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo` |
| filter-chip | `color.Sky Blue→background`, `spacing.12→padding`, `radius.md→radius`, `color.Navy Blue→surface`, `color.Ochre→emphasis`, `color.Sky Blue→background`, `spacing.12→padding`, `radius.md→radius` |
| filter-panel | `color.Navy Blue→surface`, `color.Ochre→emphasis`, `color.Sky Blue→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo` |
| filter-toolbar | `color.Sky Blue→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo` |
| footer-column | `color.Sky Blue→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo` |
| footer-legal | `color.Sky Blue→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo` |
| footer-link | `color.Sky Blue→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo` |
| footer-social | `color.Sky Blue→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo` |
| form-actions | `color.Navy Blue→surface`, `color.Ochre→emphasis`, `color.Sky Blue→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo` |
| form-section | `color.Navy Blue→surface`, `color.Ochre→emphasis`, `color.Sky Blue→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo` |
| ghost-button | `color.Navy Blue→surface`, `color.Ochre→emphasis`, `color.Sky Blue→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo` |
| hero-container | `color.Sky Blue→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo` |
| hero-cta-group | `color.Navy Blue→surface`, `color.Ochre→emphasis`, `color.Sky Blue→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo` |
| hero-eyebrow | `color.Sky Blue→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo` |
| hero-headline | `color.Sky Blue→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo` |
| hero-section | `color.Sky Blue→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo` |
| hero-subheadline | `color.Sky Blue→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo` |
| hero-trust-strip | `color.Sky Blue→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo` |
| hero-visual | `color.Sky Blue→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo` |
| icon-button | `color.Navy Blue→surface`, `color.Ochre→emphasis`, `color.Sky Blue→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo` |
| inline-alert | `color.Sky Blue→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo` |
| insight-card | `color.Sky Blue→background`, `spacing.12→padding`, `radius.md→radius`, `color.Sky Blue→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo`, `font:Spoqa Han Sans Neo` |
| kanban-board | `color.Sky Blue→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo` |
| kanban-card | `color.Sky Blue→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo` |
| kanban-column | `color.Sky Blue→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo` |
| link-button | `color.Navy Blue→surface`, `color.Ochre→emphasis`, `color.Sky Blue→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo` |
| logo-cloud | `color.Sky Blue→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo` |
| metric-highlight | `color.Sky Blue→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo` |
| mobile-menu-trigger | `color.Navy Blue→surface`, `color.Ochre→emphasis`, `color.Sky Blue→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo` |
| mobile-tab-bar | `color.Navy Blue→surface`, `color.Ochre→emphasis`, `color.Sky Blue→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo` |
| mobile-topbar | `color.Navy Blue→surface`, `color.Ochre→emphasis`, `color.Sky Blue→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo` |
| modal-dialog | `color.Navy Blue→surface`, `color.Ochre→emphasis`, `color.Sky Blue→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo` |
| pagination | `color.Sky Blue→background`, `spacing.12→padding`, `radius.md→radius`, `color.Navy Blue→surface`, `color.Ochre→emphasis`, `color.Sky Blue→background`, `spacing.12→padding`, `radius.md→radius` |
| press-quote | `color.Sky Blue→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo` |
| pricing-card | `color.Sky Blue→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo` |
| primary-button | `color.Navy Blue→surface`, `color.Ochre→emphasis`, `color.Sky Blue→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo` |
| profile-card | `color.Sky Blue→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo` |
| radio-group | `color.Navy Blue→surface`, `color.Ochre→emphasis`, `color.Sky Blue→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo` |
| row-actions | `color.Sky Blue→background`, `spacing.12→padding`, `radius.md→radius`, `color.Sky Blue→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo`, `font:Spoqa Han Sans Neo` |
| scope-switcher | `color.Navy Blue→surface`, `color.Ochre→emphasis`, `color.Sky Blue→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo` |
| search-field | `color.Navy Blue→surface`, `color.Ochre→emphasis`, `color.Sky Blue→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo` |
| search-results | `color.Sky Blue→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo` |
| secondary-button | `color.Navy Blue→surface`, `color.Ochre→emphasis`, `color.Sky Blue→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo` |
| section-header | `color.Sky Blue→background`, `spacing.12→padding`, `radius.md→radius`, `color.Sky Blue→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo`, `font:Spoqa Han Sans Neo` |
| section-tabs | `color.Navy Blue→surface`, `color.Ochre→emphasis`, `color.Sky Blue→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo` |
| segmented-control | `color.Navy Blue→surface`, `color.Ochre→emphasis`, `color.Sky Blue→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo` |
| select | `color.Navy Blue→surface`, `color.Ochre→emphasis`, `color.Sky Blue→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo` |
| shortcut-hint | `color.Sky Blue→background`, `spacing.12→padding`, `radius.md→radius`, `color.Sky Blue→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo`, `font:Spoqa Han Sans Neo` |
| sidebar-nav | `color.Navy Blue→surface`, `color.Ochre→emphasis`, `color.Sky Blue→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo` |
| site-footer | `color.Sky Blue→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo` |
| site-header | `color.Sky Blue→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo` |
| site-logo | `color.Sky Blue→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo` |
| site-nav | `color.Sky Blue→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo` |
| site-nav-cta | `color.Navy Blue→surface`, `color.Ochre→emphasis`, `color.Sky Blue→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo` |
| stat-card | `color.Sky Blue→background`, `spacing.12→padding`, `radius.md→radius`, `color.Sky Blue→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo`, `font:Spoqa Han Sans Neo` |
| status-badge | `color.Sky Blue→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo` |
| step-progress | `color.Sky Blue→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo` |
| tab-bar | `color.Navy Blue→surface`, `color.Ochre→emphasis`, `color.Sky Blue→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo` |
| tag | `color.Sky Blue→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo` |
| testimonial-author | `color.Sky Blue→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo` |
| testimonial-card | `color.Sky Blue→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo` |
| testimonial-quote | `color.Sky Blue→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo` |
| testimonial-section | `color.Sky Blue→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo` |
| text-field | `color.Navy Blue→surface`, `color.Ochre→emphasis`, `color.Sky Blue→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo` |
| textarea | `color.Navy Blue→surface`, `color.Ochre→emphasis`, `color.Sky Blue→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo` |
| time-picker | `color.Navy Blue→surface`, `color.Ochre→emphasis`, `color.Sky Blue→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo` |
| toast | `color.Sky Blue→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo` |
| tooltip-guide | `color.Navy Blue→surface`, `color.Ochre→emphasis`, `color.Sky Blue→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo` |
| topbar | `color.Navy Blue→surface`, `color.Ochre→emphasis`, `color.Sky Blue→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo` |
| trust-strip | `color.Sky Blue→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo` |
| upgrade-banner | `color.Sky Blue→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo` |
| user-menu | `color.Navy Blue→surface`, `color.Ochre→emphasis`, `color.Sky Blue→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo` |
| wizard-layout | `color.Navy Blue→surface`, `color.Ochre→emphasis`, `color.Sky Blue→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo` |

## 19. Contrast Audit

| Background | Foreground | Ratio | Level |
|------------|------------|-------|-------|
| Navy Blue | Paper | 16.01:1 | AAA (pass) |
| Sky Blue | Ink | 10.84:1 | AAA (pass) |
| Navy Blue | Sky Blue | 9.19:1 | AAA (pass) |
| Ochre | Ink | 5.60:1 | AA (pass) |
| Navy Blue | Ochre | 4.75:1 | AA (pass) |
| Ochre | Paper | 3.37:1 | AA-large (large-only) |
| Ochre | Sky Blue | 1.94:1 | fail (FAIL) |
| Sky Blue | Paper | 1.74:1 | fail (FAIL) |
| Navy Blue | Ink | 1.18:1 | fail (FAIL) |

## 20. Pattern Catalog

### Layout Patterns

- **archive browser**: —
- **audit log**: —
- **data tables**: data-table, column-header, filter-chip, row-actions, pagination, filter-toolbar
- **dashboard cards**: stat-card, insight-card, activity-card, section-header, chart-panel
- **hero section**: hero-container, hero-eyebrow, hero-headline, hero-subheadline, hero-cta-group, hero-visual, hero-trust-strip, hero-section, trust-strip
- **feature grid**: feature-section, feature-grid, feature-card, feature-icon, feature-title, feature-description
- **social proof**: logo-cloud, customer-logo, metric-highlight, press-quote
- **testimonial**: testimonial-section, testimonial-card, testimonial-quote, testimonial-author
- **faq accordion**: faq-section, faq-item, faq-question, faq-answer
- **landing cta section**: cta-section, cta-headline, cta-supporting-text, cta-button-group
- **site footer**: site-footer, footer-column, footer-link, footer-legal, footer-social
- **site header**: site-header, site-logo, site-nav, site-nav-cta, mobile-menu-trigger
- **pricing and plans**: pricing-card, feature-comparison, upgrade-banner
- **workspace navigation**: app-shell, sidebar-nav, topbar, breadcrumb, tab-bar

### Interaction Patterns

- **restore workflow**: —
- **command palette**: command-palette, command-result-item, shortcut-hint, scope-switcher
- **forms**: text-field, select, checkbox, textarea, form-section, radio-group, form-actions
- **notifications**: toast, inline-alert, empty-state, banner
