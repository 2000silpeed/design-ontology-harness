# Lattice-Dash System Spec

## 1. Positioning

- **Brand**: Lattice-Dash
- **Product**: B2C 스타트업 운영 대시보드 — bold-confident 톤 vivid admin console, activation · retention · cohort · referral 지표를 impact typography 로 한 화면에 모은 운영팀 어드민, 한국어 1급
- **Audience**: B2C 스타트업 운영팀 (그로스/프로덕트 매니저) — activation funnel / cohort retention / A/B 결과 주시, 스타트업 CEO/파운더 — 주간 MAU/DAU/ARPU impact KPI 확인 + 투자자 리포트, 커뮤니티/지원 리드 — 유저 이슈 티켓 · 알람 · incident 운영 큐
- **Platforms**: web, desktop
- **Accessibility floor**: WCAG 2.2 AA

## 2. Identity Guardrails

- **Brand keywords**: dashboard, admin, console, startup, saas, b2c, growth, activation, retention, cohort, referral, bold, vivid, energetic, high-contrast, impact
- **Anti-keywords**: editorial-warm, magazine-serif, minimal-only, playful-pastel, corporate-conservative, document-heavy, commerce-checkout
- **Tone of voice**: confident, energetic, direct, data-forward, youthful
- **Visual direction**: high-contrast headline, vivid ultra violet primary, illuminating yellow accent, saturated KPI card, dense data table, impact metric typography, youthful startup, admin-first bold, activation funnel visual, cohort matrix heat-scale
- **Interaction direction**: keyboard-first, command palette, sticky filter bar, hover-emphasis row, activation funnel drill, cohort retention hover, referral share action, impact toast, saturated primary CTA

## 3. Design Principles

- **Dashboard**: `dashboard`를 시각적 선택과 인터랙션 선택의 기본 기준으로 삼습니다.
- **Admin**: `admin`를 시각적 선택과 인터랙션 선택의 기본 기준으로 삼습니다.
- **Console**: `console`를 시각적 선택과 인터랙션 선택의 기본 기준으로 삼습니다.
- **Startup**: `startup`를 시각적 선택과 인터랙션 선택의 기본 기준으로 삼습니다.

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
- **Product type detected**: dashboard
- **Pairing source**: auto-scored
- **Line height**: tight
- **Type scale**: base 14px, ratio 1.2 (xs=11px, sm=12px, md=14px, lg=17px, xl=20px, 2xl=24px, 3xl=29px)
- **Strategy**:
  - 단일 서체(Spoqa Han Sans Neo)로 weight 대비 위계 — 일관성 우선
  - 한글 서체: Spoqa Han Sans Neo — 라틴과 x-height/weight 조화
  - 모노스페이스: JetBrains Mono — 코드/데이터 영역 전용
- **Heading note**: 스포카에서 만든 한글 산세리프. Source Sans Pro 기반. 깔끔한 데이터 UI에 적합.
- **Body note**: 스포카에서 만든 한글 산세리프. Source Sans Pro 기반. 깔끔한 데이터 UI에 적합.
- **Korean rationale**: Spoqa Han Sans Neo — Pretendard 이전 시대의 한글 UI 표준. 요기요, 여기어때 등에서 사용. 깔끔하지만 weight 범위와 Variable 미지원이 아쉬움. 신규 프로젝트에서는 Pretendard 추천.
- **Heading tracking**: xl=-0.01em, 2xl=-0.01em, 3xl=-0.01em
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

- **Source**: REFERENCE X Vol.1 - Color Reference (/Users/sungwoon/ai-projects/design-ontology-harness/docs/color-reference.md)
- **Selection mode**: manual
- **Preferred families**: Pantone Trend Violets, Pantone Trend Yellows, Pastel Oranges
- **Palette strategy**: temperature=mixed, contrast=balanced, diversity=balanced, surface_style=tinted
- **Palette expansion**: supporting_color_count=10, combination_count=3, prefer_pairings=True
- **Palette roles**:
  - `primary` -> Ultra Violet #5F4B8B / Pantone Trend Violets
  - `accent` -> Illuminating #F5DF4D / Pantone Trend Yellows
  - `surface_tint` -> Creamsicle #FFD7A0 / Pastel Oranges
- **Selected colors**:
  - Grenadine #DC4C46 / Pantone Trend Reds / 밝고 따뜻한 레드 오렌지 계열, 중채도 이상의 밝은 톤 / 활력, 열정, 관능, 현대적
  - Scarlet #FF2400 / Standard Reds / 강렬한 주황빛 레드 계열, 고채도와 고명도의 따뜻한 톤 / 활기, 생동감, 열정, 역동성, 주목성
  - Pure Red #FF0000 / Standard Reds / 순수 원색 레드 계열, 고채도와 중명도의 강렬한 톤 / 열정, 에너지, 주목성, 상징적, 강렬함
- **Palette candidates**:
  - signature-1 (Signature): primary=Grenadine, accent=Scarlet, surface_tint=Pure Red / Grenadine matches brand tone keywords.; Scarlet matches brand tone keywords.
- **Expanded supporting colors**:
  - Scarlet #FF2400 / Standard Reds / reference-color / Scarlet reinforces the brand mood signals.
  - Pure Red #FF0000 / Standard Reds / reference-color / Pure Red reinforces the brand mood signals.
  - Living Coral #FF6F61 / Pantone Trend Oranges / pairing-reference / Living Coral reinforces the brand mood signals.; Living Coral comes from the seed pairing references.
  - Persimmon #EC5800 / Natural Oranges / reference-color / Persimmon reinforces the brand mood signals.
  - Pure Orange #FFA500 / Standard Oranges / reference-color / Pure Orange reinforces the brand mood signals.
  - Pairing #CFC6BA #CFC6BA / Derived Pairing / pairing-swatch / Pairing #CFC6BA reinforces the brand mood signals.; Pairing #CFC6BA comes from the seed pairing references.
  - Pairing #F6F1E7 #F6F1E7 / Derived Pairing / pairing-swatch / Pairing #F6F1E7 reinforces the brand mood signals.; Pairing #F6F1E7 comes from the seed pairing references.
  - Pairing #E3C9A8 #E3C9A8 / Derived Pairing / pairing-swatch / Pairing #E3C9A8 reinforces the brand mood signals.; Pairing #E3C9A8 comes from the seed pairing references.
- **Expanded semantic roles**:
  - `brand_primary` -> Ultra Violet #5F4B8B / Pantone Trend Violets
  - `brand_accent` -> Illuminating #F5DF4D / Pantone Trend Yellows
  - `surface_tint` -> Creamsicle #FFD7A0 / Pastel Oranges
  - `canvas` -> Canvas White #F7F8FA / Generated Fallback
  - `surface` -> Paper #FFFFFF / Generated Fallback
  - `surface_muted` -> Surface Muted #EEF1F6 / Generated Fallback
  - `surface_elevated` -> Paper #FFFFFF / Generated Fallback
  - `border` -> Pairing #CFC6BA #CFC6BA / Derived Pairing
  - `border_strong` -> Pairing #CFC6BA #CFC6BA / Derived Pairing
  - `ink` -> Ink #111111 / Generated Fallback
- **Combination lists**:
  - Seed Core: primary=Ultra Violet, accent=Illuminating, surface_tint=Creamsicle
  - Surface System: canvas=Canvas White, surface=Paper, surface_tint=Creamsicle, border=Pairing #CFC6BA, ink=Ink, ink_muted=Ultra Violet
  - Support Spectrum: support=Scarlet, support=Pure Red, support=Living Coral, support=Persimmon, support=Pure Orange, support=Pairing #CFC6BA
- **Notes**: Ultra Violet #5F4B8B primary — 2018 Pantone, vivid deep purple, sidebar-nav active / primary-button / activation-funnel active stage / cohort heat-scale 최고단계 / command palette focus / KPI delta 강조, Illuminating #F5DF4D accent — 2021 Pantone, vivid yellow, activation callout / referral-widget share CTA / goal-tracker complete / experiment-panel winner / impact toast 성공, Creamsicle #FFD7A0 surface_tint — warm cream surface, KPI card 보조 surface / empty-state illustration / filter-chip soft group bg, admin dense row 에는 near-white 기본 surface 유지, light mode 가 기본 — B2C startup admin 관례, dark 옵션 제공 (deep cool neutral surface + tuned Ultra Violet/Illuminating 채도 낮춤), 기존 15종 프리셋 HEX 와 겹침 0 — Ultra Violet/Illuminating/Creamsicle 조합, bold-confident 3종 (premier-league #E90052/#00FF85/#FFD700, drop #BD2E4A/#6C3BAA/#F3E5AB, broadside #0F4C81/#CC142F/#F2552C) 와 전면 차별화 — 'startup admin purple' 정체성
- **Application rule**: 레퍼런스 컬러는 semantic token으로 번역해서 사용하고, 접근성과 theme 호환성을 우선합니다.

## 7. Visual Reference Signals

- **Mode**: local-images
- **Coverage**: source 0 / image 0 / selected 0
- **Rule**: visual references are advisory signals for motif and layout direction; official KB/spec remain the structural source of truth.
- **Provenance**: `observed` = directly measured from local pixels, `inferred` = synthesized from image/query/brand signals, `unverified` = reliable visual evidence not yet available.
- **Query seeds**: retool admin console, appsmith internal tool, stripe radar dashboard, posthog activation funnel, plausible analytics dashboard, mixpanel cohort matrix
### Visual Direction

- **Density**: dense (confidence 0.94, provenance inferred) / dashboard x4, table x4, analytics x1
- **Surface Style**: tinted (confidence 0.37, provenance inferred) / warm x2, editorial x1
- **Corner Style**: medium (confidence 0.39, provenance inferred) / card x3
- **Typography Mood**: utilitarian (confidence 0.94, provenance inferred) / dashboard x4, admin x5, table x4
- **Color balance**: temperature=unknown, contrast=unknown, neutral_bias=unknown, provenance=unverified

### Layout Rhythm

- **Dashboard grid**: confidence 0.94 / provenance inferred / dashboard x4, analytics x1, metric x1, kpi x3
- **Data review surface**: confidence 0.94 / provenance inferred / table x4, data x3, filter x5
- **Editorial feed**: confidence 0.94 / provenance inferred / editorial x1, article x1, feed x2, story x1
- **Narrative landing flow**: confidence 0.94 / provenance inferred / landing x1, hero x2, cta x4

### Image-derived Component Hints

- **Cards**: low-elevation tinted cards를 기본으로 하고, 압축된 spacing과 얇은 divider 중심의 hierarchy. 중간 반경으로 제품 UI 절제 유지. / provenance inferred / surface=tinted, density=dense, corner=medium
- **Navigation**: navigation은 compact하게 유지하되 filter/scope controls와 혼합하지 않는다. / provenance inferred / Dashboard grid
- **Typography**: 정보 밀도에 맞춰 type scale 차이를 줄이고 table/list label의 정렬 정확도를 우선한다. / provenance inferred / typography_mood=utilitarian
- **Data Display**: 정보 밀도를 유지하되 thin dividers와 restrained accent로 hierarchy를 만든다. / provenance inferred / layout=dashboard-grid, density=dense

### Synthesis Notes

- layout는 Dashboard grid 기준으로 정리
- surface language는 tinted 성향 우선
- typography mood는 utilitarian 축 유지
- density는 dense 기준으로 primitive spacing 조정
- palette temperature는 unknown 쪽을 우선
- Avoid: magazine hero cover story
- Avoid: commerce product detail
- Avoid: pastel playful feed
- Avoid: corporate navy blueprint

## 8. Component Strategy

- **Product primitives**: sidebar navigation, workspace switcher, data table, kpi card, filter chip, command palette, activity feed, activation funnel, referral widget, cohort matrix, retention chart, conversion funnel, experiment panel, user list, ticket queue, alert list, segment filter, goal tracker, settings panel
- **Required families**: button, data-display, editorial, feedback, input, marketing, navigation, commerce, dashboard-growth, document, foundation, overlay, social
- **Visual-reference archetypes**:

- **Dashboard insight module** (data-display / 0.94): stat-card, insight-card, chart-panel, section-header, filter-chip
- **Data review table** (data-display / 0.94): data-table, column-header, row-actions, filter-toolbar, pagination
- **Editorial content block** (editorial / 0.94): content-card, featured-story-card, section-header, content-meta, byline-row
- **Marketing hero stack** (marketing / 0.94): hero-section, hero-headline, hero-visual, cta-button-group, trust-strip
- **Workspace shell** (navigation / 0.94): app-shell, sidebar-nav, workspace-switcher, breadcrumb, context-panel

- **button**: primary-button, secondary-button, ghost-button, icon-button, cta-button, link-button, form-actions, hero-cta-group
- **data-display**: stat-card, insight-card, activity-card, section-header, data-table, column-header, row-actions, tag / visual signals: Dashboard insight module (0.94), Data review table (0.94)
- **editorial**: editor-canvas, editor-toolbar, inline-format-menu, slash-command-menu, block-controls, content-card, featured-story-card, content-meta / visual signals: Editorial content block (0.94)
- **feedback**: inline-alert, empty-state, toast, status-badge, banner, empty-feed-illustration, gentle-toast, shortcut-hint
- **input**: text-field, search-field, segmented-control, segment-filter, filter-chip, chip, filter-panel, textarea
- **marketing**: hero-container, hero-eyebrow, hero-headline, hero-subheadline, hero-visual, hero-trust-strip, logo-cloud, customer-logo / visual signals: Marketing hero stack (0.94)
- **navigation**: scope-switcher, mobile-topbar, mobile-tab-bar, back-button, section-tabs, filter-bar, pagination, app-shell / visual signals: Workspace shell (0.94)
- **commerce**: product-grid, product-card, product-detail, product-gallery, product-hero-image, image-thumbnail, price-tag, original-price-strikethrough
- **dashboard-growth**: activation-funnel, cohort-matrix, referral-widget, retention-chart, conversion-funnel, experiment-panel, goal-tracker, user-list
- **document**: callout, admonition-block
- **foundation**: command-result-item, shortcut-hint
- **overlay**: command-palette, bottom-sheet, modal-dialog, autocomplete, chart-tooltip, confirm-dialog, mention-popup, user-menu
- **social**: feed-item, post-card, thread-view, reaction-bar, timeline-stream, avatar-cluster

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

- Warning: [pitfall#3-rebrand] Grenadine vs Scarlet (red): lightness diff 7, saturation diff 32 — possible rebrand remnant
- Warning: [pitfall#3-rebrand] Grenadine vs Pure Red (red): lightness diff 7, saturation diff 32 — possible rebrand remnant
- Warning: visual_reference.sources is empty

## 14. Quick Start

이 문서는 **Lattice-Dash System**의 디자인 시스템 사양입니다.

### 시작하기

1. **토큰 적용**: Drop-in CSS(아래 섹션 16)의 CSS 변수를 프로젝트에 복사합니다.
2. **컬러 세팅**: Color Reference(섹션 6)의 semantic role을 기준으로 surface/text/border를 잡습니다.
3. **타이포 세팅**: Token Strategy(섹션 5)의 font family와 type scale을 적용합니다.
4. **시각 방향 확인**: Visual Reference Signals(섹션 7)에서 density/surface/layout cue를 먼저 확인합니다.
5. **컴포넌트 구현**: Component Strategy(섹션 8)의 family 순서대로 하나씩 빌드합니다.

### 우선순위

핵심 primitive: **sidebar navigation, workspace switcher, data table, kpi card, filter chip**

이 primitive를 지원하는 컴포넌트부터 구현하고, 나머지는 필요에 따라 확장합니다.

## 15. DO / DON'T

### DO

- **Dashboard**: dashboard와 충돌하는 컴포넌트 변형은 만들지 않기
- **Admin**: admin와 충돌하는 컴포넌트 변형은 만들지 않기
- **Console**: console와 충돌하는 컴포넌트 변형은 만들지 않기
- **Startup**: startup와 충돌하는 컴포넌트 변형은 만들지 않기
- 모든 시각적 선택에서 **dashboard, admin, console** 기준을 적용
- semantic token을 통해 컬러를 적용 (하드코딩 금지)
- 접근성 기준을 모든 text/surface 조합에서 먼저 검증
- 컴포넌트 변형 추가 전 기존 variant로 해결 가능한지 먼저 확인
- 아이콘은 SVG 컴포넌트 또는 Lucide/Heroicons/Phosphor/Tabler 등 라이브러리로 구현
- component_specs.md의 anatomy/states/token binding을 그대로 따라 완전히 구현

### DON'T

- **editorial-warm** 방향의 디자인 결정을 하지 않음
- **magazine-serif** 방향의 디자인 결정을 하지 않음
- **minimal-only** 방향의 디자인 결정을 하지 않음
- **playful-pastel** 방향의 디자인 결정을 하지 않음
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
  --text-xs: 11px;
  --text-sm: 12px;
  --text-md: 14px;
  --text-lg: 17px;
  --text-xl: 20px;
  --text-2xl: 24px;
  --text-3xl: 29px;

  --leading-tight: 1.25;
  --leading-normal: 1.4;
  --leading-comfortable: 1.5;
  --leading-relaxed: 1.6;

  /* --- Color (from reference) --- */
  --color-primary: #5F4B8B;
  --color-accent: #F5DF4D;
  --color-surface-tint: #FFD7A0;

  /* --- Semantic roles (expanded) --- */
  --color-brand-primary: #5F4B8B;
  --color-brand-accent: #F5DF4D;
  --color-surface-tint: #FFD7A0;
  --color-canvas: #F7F8FA;
  --color-surface: #FFFFFF;
  --color-surface-muted: #EEF1F6;
  --color-surface-elevated: #FFFFFF;
  --color-border: #CFC6BA;
  --color-border-strong: #CFC6BA;
  --color-ink: #111111;
  --color-ink-muted: #5F4B8B;
  --color-ink-subtle: #6B7280;
  --color-ink-inverse: #FFFFFF;
  --color-primary-support: #FF2400;
  --color-accent-support: #F5DF4D;
  --color-info: #4A6B8A;
  --color-success: #4A7C59;
  --color-warning: #F5DF4D;
  --color-danger: #5F4B8B;
  --color-link: #5F4B8B;
  --color-link-hover: #4D3D70;

  /* --- Button — primary --- */
  --color-button-primary-surface-default: #5F4B8B;
  --color-button-primary-surface-hover: #514077;
  --color-button-primary-surface-active: #48396A;
  --color-button-primary-surface-disabled: #BAB3CE;
  --color-button-primary-text-default: #FFFFFF;
  --color-button-primary-text-disabled: #FBFCFC;
  --color-button-primary-border-default: #5F4B8B;
  --color-button-primary-focus-ring: #5F4B8B;

  /* --- Button — secondary --- */
  --color-button-secondary-surface-default: #FFFFFF;
  --color-button-secondary-surface-hover: #F1F1F1;
  --color-button-secondary-surface-active: #E7E7E7;
  --color-button-secondary-surface-disabled: #F7F8FA;
  --color-button-secondary-text-default: #111111;
  --color-button-secondary-text-disabled: #909091;
  --color-button-secondary-border-default: #BEB2A2;
  --color-button-secondary-border-hover: #AE9E8A;
  --color-button-secondary-focus-ring: #5F4B8B;

  /* --- Button — ghost --- */
  --color-button-ghost-surface-default: transparent;
  --color-button-ghost-surface-hover: #F3F3F3;
  --color-button-ghost-surface-active: #EAEAEA;
  --color-button-ghost-surface-disabled: transparent;
  --color-button-ghost-text-default: #5F4B8B;
  --color-button-ghost-text-hover: #111111;
  --color-button-ghost-text-disabled: #B3AAC8;
  --color-button-ghost-border-default: transparent;
  --color-button-ghost-focus-ring: #5F4B8B;

  /* --- Button — danger --- */
  --color-button-danger-surface-default: #5F4B8B;
  --color-button-danger-surface-hover: #514077;
  --color-button-danger-surface-active: #48396A;
  --color-button-danger-text-default: #FFFFFF;
  --color-button-danger-border-default: #5F4B8B;
  --color-button-danger-focus-ring: #5F4B8B;

  /* --- Input --- */
  --color-input-surface-default: #FFFFFF;
  --color-input-surface-filled: #FFFFFF;
  --color-input-surface-disabled: #F7F8FA;
  --color-input-text-default: #111111;
  --color-input-text-placeholder: #9C90B7;
  --color-input-text-disabled: #B3AAC8;
  --color-input-border-default: #CFC6BA;
  --color-input-border-hover: #BAAD9C;
  --color-input-border-focus: #5F4B8B;
  --color-input-border-error: #5F4B8B;
  --color-input-border-disabled: #D9D2C9;

  /* --- Card --- */
  --color-card-surface-default: #FFFFFF;
  --color-card-surface-hover: #FAFAFA;
  --color-card-surface-muted: #F7F8FA;
  --color-card-border-default: #CFC6BA;
  --color-card-border-hover: #BAAD9C;
  --color-card-border-focus: #5F4B8B;

  /* --- Nav link --- */
  --color-nav-link-text-default: #5F4B8B;
  --color-nav-link-text-hover: #111111;
  --color-nav-link-text-active: #5F4B8B;
  --color-nav-link-surface-hover: #F5F5F5;
  --color-nav-link-indicator: #F5DF4D;

  /* --- Link --- */
  --color-link-text-default: #5F4B8B;
  --color-link-text-hover: #48396A;
  --color-link-text-visited: #5B5568;

  /* --- Feedback — info --- */
  --color-feedback-info-surface: #E9EDF1;
  --color-feedback-info-text: #4A6B8A;
  --color-feedback-info-border: #7E95AC;
  --color-feedback-info-icon: #4A6B8A;

  /* --- Feedback — success --- */
  --color-feedback-success-surface: #E9EFEB;
  --color-feedback-success-text: #4A7C59;
  --color-feedback-success-border: #7EA189;
  --color-feedback-success-icon: #4A7C59;

  /* --- Feedback — warning --- */
  --color-feedback-warning-surface: #FEFBEA;
  --color-feedback-warning-text: #F5DF4D;
  --color-feedback-warning-border: #F6E681;
  --color-feedback-warning-icon: #F5DF4D;

  /* --- Feedback — danger --- */
  --color-feedback-danger-surface: #ECE9F1;
  --color-feedback-danger-text: #5F4B8B;
  --color-feedback-danger-border: #8D7FAC;
  --color-feedback-danger-icon: #5F4B8B;

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
| activation-funnel | `color.Creamsicle→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo` |
| activity-card | `color.Creamsicle→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo` |
| add-to-cart-button | `color.Ultra Violet→surface`, `color.Illuminating→emphasis`, `color.Creamsicle→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo` |
| admonition-block | `color.Creamsicle→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo` |
| alert-list | `color.Creamsicle→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo` |
| app-shell | `color.Ultra Violet→surface`, `color.Illuminating→emphasis`, `color.Creamsicle→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo` |
| autocomplete | `color.Ultra Violet→surface`, `color.Illuminating→emphasis`, `color.Creamsicle→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo` |
| avatar | `color.Creamsicle→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo` |
| avatar-cluster | `color.Creamsicle→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo` |
| back-button | `color.Ultra Violet→surface`, `color.Illuminating→emphasis`, `color.Creamsicle→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo` |
| banner | `color.Creamsicle→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo` |
| block-controls | `color.Creamsicle→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo` |
| bottom-sheet | `color.Ultra Violet→surface`, `color.Illuminating→emphasis`, `color.Creamsicle→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo` |
| breadcrumb | `color.Ultra Violet→surface`, `color.Illuminating→emphasis`, `color.Creamsicle→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo` |
| byline-row | `color.Creamsicle→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo` |
| calendar-grid | `color.Creamsicle→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo` |
| callout | `color.Creamsicle→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo` |
| category-pill | `color.Ultra Violet→surface`, `color.Illuminating→emphasis`, `color.Creamsicle→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo` |
| chart-container | `color.Creamsicle→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo` |
| chart-legend | `color.Creamsicle→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo` |
| chart-panel | `color.Creamsicle→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo` |
| chart-tooltip | `color.Ultra Violet→surface`, `color.Illuminating→emphasis`, `color.Creamsicle→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo` |
| chat-input | `color.Ultra Violet→surface`, `color.Illuminating→emphasis`, `color.Creamsicle→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo` |
| chat-message | `color.Creamsicle→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo` |
| chat-thread | `color.Creamsicle→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo` |
| checkbox | `color.Ultra Violet→surface`, `color.Illuminating→emphasis`, `color.Creamsicle→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo` |
| chip | `color.Ultra Violet→surface`, `color.Illuminating→emphasis`, `color.Creamsicle→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo` |
| cohort-matrix | `color.Creamsicle→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo` |
| color-swatch-selector | `color.Ultra Violet→surface`, `color.Illuminating→emphasis`, `color.Creamsicle→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo` |
| column-header | `color.Creamsicle→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo` |
| command-palette | `color.Ultra Violet→surface`, `color.Illuminating→emphasis`, `color.Creamsicle→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo` |
| command-result-item | `color.Creamsicle→background`, `spacing.12→padding`, `radius.md→radius`, `color.Ultra Violet→surface`, `color.Illuminating→emphasis`, `color.Creamsicle→background`, `spacing.12→padding`, `radius.md→radius` |
| comment-input | `color.Ultra Violet→surface`, `color.Illuminating→emphasis`, `color.Creamsicle→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo` |
| comment-thread | `color.Creamsicle→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo` |
| confirm-dialog | `color.Ultra Violet→surface`, `color.Illuminating→emphasis`, `color.Creamsicle→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo` |
| content-card | `color.Creamsicle→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo` |
| content-meta | `color.Creamsicle→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo` |
| context-panel | `color.Ultra Violet→surface`, `color.Illuminating→emphasis`, `color.Creamsicle→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo` |
| conversion-funnel | `color.Creamsicle→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo` |
| cross-sell-grid | `color.Creamsicle→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo` |
| cta-button | `color.Ultra Violet→surface`, `color.Illuminating→emphasis`, `color.Creamsicle→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo` |
| cta-button-group | `color.Creamsicle→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo` |
| customer-logo | `color.Creamsicle→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo` |
| data-table | `color.Creamsicle→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo` |
| date-picker | `color.Ultra Violet→surface`, `color.Illuminating→emphasis`, `color.Creamsicle→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo` |
| date-range-picker | `color.Ultra Violet→surface`, `color.Illuminating→emphasis`, `color.Creamsicle→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo` |
| discount-badge | `color.Creamsicle→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo` |
| editor-canvas | `color.Creamsicle→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo` |
| editor-toolbar | `color.Creamsicle→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo` |
| empty-feed-illustration | `color.Creamsicle→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo` |
| empty-state | `color.Creamsicle→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo` |
| experiment-panel | `color.Creamsicle→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo` |
| featured-story-card | `color.Creamsicle→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo` |
| feed-item | `color.Creamsicle→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo` |
| filter-bar | `color.Ultra Violet→surface`, `color.Illuminating→emphasis`, `color.Creamsicle→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo` |
| filter-chip | `color.Ultra Violet→surface`, `color.Illuminating→emphasis`, `color.Creamsicle→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo` |
| filter-panel | `color.Ultra Violet→surface`, `color.Illuminating→emphasis`, `color.Creamsicle→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo` |
| filter-sidebar | `color.Ultra Violet→surface`, `color.Illuminating→emphasis`, `color.Creamsicle→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo` |
| filter-toolbar | `color.Creamsicle→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo` |
| follow-button | `color.Ultra Violet→surface`, `color.Illuminating→emphasis`, `color.Creamsicle→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo` |
| form-actions | `color.Ultra Violet→surface`, `color.Illuminating→emphasis`, `color.Creamsicle→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo` |
| form-section | `color.Ultra Violet→surface`, `color.Illuminating→emphasis`, `color.Creamsicle→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo` |
| gentle-toast | `color.Creamsicle→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo` |
| ghost-button | `color.Ultra Violet→surface`, `color.Illuminating→emphasis`, `color.Creamsicle→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo` |
| goal-tracker | `color.Creamsicle→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo` |
| hero-container | `color.Creamsicle→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo` |
| hero-cta-group | `color.Ultra Violet→surface`, `color.Illuminating→emphasis`, `color.Creamsicle→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo` |
| hero-eyebrow | `color.Creamsicle→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo` |
| hero-headline | `color.Creamsicle→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo` |
| hero-section | `color.Creamsicle→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo` |
| hero-subheadline | `color.Creamsicle→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo` |
| hero-trust-strip | `color.Creamsicle→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo` |
| hero-visual | `color.Creamsicle→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo` |
| icon-button | `color.Ultra Violet→surface`, `color.Illuminating→emphasis`, `color.Creamsicle→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo` |
| image-thumbnail | `color.Creamsicle→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo` |
| inline-alert | `color.Creamsicle→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo` |
| inline-format-menu | `color.Creamsicle→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo` |
| insight-card | `color.Creamsicle→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo` |
| kanban-board | `color.Creamsicle→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo` |
| kanban-card | `color.Creamsicle→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo` |
| kanban-column | `color.Creamsicle→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo` |
| link-button | `color.Ultra Violet→surface`, `color.Illuminating→emphasis`, `color.Creamsicle→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo` |
| logo-cloud | `color.Creamsicle→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo` |
| mention-popup | `color.Ultra Violet→surface`, `color.Illuminating→emphasis`, `color.Creamsicle→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo` |
| metric-highlight | `color.Creamsicle→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo` |
| mobile-tab-bar | `color.Ultra Violet→surface`, `color.Illuminating→emphasis`, `color.Creamsicle→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo` |
| mobile-topbar | `color.Ultra Violet→surface`, `color.Illuminating→emphasis`, `color.Creamsicle→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo` |
| modal-dialog | `color.Ultra Violet→surface`, `color.Illuminating→emphasis`, `color.Creamsicle→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo` |
| original-price-strikethrough | `color.Creamsicle→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo` |
| pagination | `color.Ultra Violet→surface`, `color.Illuminating→emphasis`, `color.Creamsicle→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo` |
| post-card | `color.Creamsicle→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo` |
| press-quote | `color.Creamsicle→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo` |
| price-tag | `color.Creamsicle→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo` |
| primary-button | `color.Ultra Violet→surface`, `color.Illuminating→emphasis`, `color.Creamsicle→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo` |
| product-card | `color.Creamsicle→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo` |
| product-detail | `color.Creamsicle→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo` |
| product-gallery | `color.Creamsicle→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo` |
| product-grid | `color.Creamsicle→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo` |
| product-hero-image | `color.Creamsicle→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo` |
| profile-card | `color.Creamsicle→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo` |
| quick-view-modal | `color.Ultra Violet→surface`, `color.Illuminating→emphasis`, `color.Creamsicle→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo` |
| radio-group | `color.Ultra Violet→surface`, `color.Illuminating→emphasis`, `color.Creamsicle→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo` |
| reaction-bar | `color.Creamsicle→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo` |
| referral-widget | `color.Creamsicle→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo` |
| reply-composer | `color.Ultra Violet→surface`, `color.Illuminating→emphasis`, `color.Creamsicle→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo` |
| retention-chart | `color.Creamsicle→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo` |
| row-actions | `color.Creamsicle→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo` |
| scope-switcher | `color.Ultra Violet→surface`, `color.Illuminating→emphasis`, `color.Creamsicle→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo` |
| search-field | `color.Ultra Violet→surface`, `color.Illuminating→emphasis`, `color.Creamsicle→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo` |
| search-results | `color.Creamsicle→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo` |
| secondary-button | `color.Ultra Violet→surface`, `color.Illuminating→emphasis`, `color.Creamsicle→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo` |
| section-header | `color.Creamsicle→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo` |
| section-tabs | `color.Ultra Violet→surface`, `color.Illuminating→emphasis`, `color.Creamsicle→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo` |
| segment-filter | `color.Ultra Violet→surface`, `color.Illuminating→emphasis`, `color.Creamsicle→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo` |
| segmented-control | `color.Ultra Violet→surface`, `color.Illuminating→emphasis`, `color.Creamsicle→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo` |
| select | `color.Ultra Violet→surface`, `color.Illuminating→emphasis`, `color.Creamsicle→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo` |
| share-sheet | `color.Ultra Violet→surface`, `color.Illuminating→emphasis`, `color.Creamsicle→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo` |
| shortcut-hint | `color.Creamsicle→background`, `spacing.12→padding`, `radius.md→radius`, `color.Creamsicle→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo`, `font:Spoqa Han Sans Neo` |
| sidebar-nav | `color.Ultra Violet→surface`, `color.Illuminating→emphasis`, `color.Creamsicle→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo` |
| size-selector | `color.Ultra Violet→surface`, `color.Illuminating→emphasis`, `color.Creamsicle→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo` |
| slash-command-menu | `color.Creamsicle→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo` |
| soft-dialog | `color.Ultra Violet→surface`, `color.Illuminating→emphasis`, `color.Creamsicle→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo` |
| sort-dropdown | `color.Ultra Violet→surface`, `color.Illuminating→emphasis`, `color.Creamsicle→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo` |
| stat-card | `color.Creamsicle→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo` |
| status-badge | `color.Creamsicle→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo` |
| step-progress | `color.Creamsicle→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo` |
| tab-bar | `color.Ultra Violet→surface`, `color.Illuminating→emphasis`, `color.Creamsicle→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo` |
| tag | `color.Creamsicle→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo` |
| tag-pill | `color.Creamsicle→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo` |
| text-field | `color.Ultra Violet→surface`, `color.Illuminating→emphasis`, `color.Creamsicle→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo` |
| textarea | `color.Ultra Violet→surface`, `color.Illuminating→emphasis`, `color.Creamsicle→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo` |
| thread-view | `color.Creamsicle→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo` |
| ticket-queue | `color.Creamsicle→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo` |
| time-picker | `color.Ultra Violet→surface`, `color.Illuminating→emphasis`, `color.Creamsicle→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo` |
| timeline-stream | `color.Creamsicle→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo` |
| toast | `color.Creamsicle→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo` |
| tooltip-guide | `color.Ultra Violet→surface`, `color.Illuminating→emphasis`, `color.Creamsicle→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo` |
| topbar | `color.Ultra Violet→surface`, `color.Illuminating→emphasis`, `color.Creamsicle→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo` |
| trust-strip | `color.Creamsicle→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo` |
| user-list | `color.Creamsicle→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo` |
| user-menu | `color.Ultra Violet→surface`, `color.Illuminating→emphasis`, `color.Creamsicle→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo` |
| variant-selector | `color.Ultra Violet→surface`, `color.Illuminating→emphasis`, `color.Creamsicle→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo` |
| wishlist-toggle | `color.Ultra Violet→surface`, `color.Illuminating→emphasis`, `color.Creamsicle→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo` |
| wizard-layout | `color.Ultra Violet→surface`, `color.Illuminating→emphasis`, `color.Creamsicle→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo` |
| workspace-switcher | `color.Ultra Violet→surface`, `color.Illuminating→emphasis`, `color.Creamsicle→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo` |

## 19. Contrast Audit

| Background | Foreground | Ratio | Level |
|------------|------------|-------|-------|
| Illuminating | Ink | 13.98:1 | AAA (pass) |
| Creamsicle | Ink | 13.92:1 | AAA (pass) |
| Ultra Violet | Paper | 7.33:1 | AAA (pass) |
| Ultra Violet | Illuminating | 5.42:1 | AA (pass) |
| Ultra Violet | Creamsicle | 5.40:1 | AA (pass) |
| Ultra Violet | Ink | 2.58:1 | fail (FAIL) |
| Creamsicle | Paper | 1.36:1 | fail (FAIL) |
| Illuminating | Paper | 1.35:1 | fail (FAIL) |
| Illuminating | Creamsicle | 1.00:1 | fail (FAIL) |

## 20. Pattern Catalog

### Layout Patterns

- **sidebar navigation**: —
- **workspace switcher**: —
- **data table**: —
- **kpi card**: —
- **activity feed**: —
- **activation funnel**: —
- **referral widget**: —
- **cohort matrix**: —
- **retention chart**: —
- **conversion funnel**: —
- **experiment panel**: —
- **user list**: —
- **ticket queue**: —
- **alert list**: —
- **goal tracker**: —
- **settings panel**: —
- **workspace navigation**: app-shell, sidebar-nav, topbar, breadcrumb, workspace-switcher, tab-bar, context-panel
- **dashboard cards**: stat-card, insight-card, activity-card, section-header, chart-panel
- **data tables**: data-table, column-header, filter-chip, row-actions, pagination, filter-toolbar

### Interaction Patterns

- **filter chip**: —
- **command palette**: command-palette, command-result-item, shortcut-hint, scope-switcher
- **segment filter**: —
- **forms**: text-field, select, checkbox, textarea, form-section, radio-group, form-actions
- **notifications**: toast, inline-alert, empty-state, banner
