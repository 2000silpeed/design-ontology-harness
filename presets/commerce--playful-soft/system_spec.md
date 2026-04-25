# Orchard System Spec

## 1. Positioning

- **Brand**: Orchard
- **Product**: 친근한 D2C 크래프트 스낵/음료 커머스 — playful-soft 톤 warm pastel consumer commerce, 상품 그리드 · 상품 상세 · 장바구니 · 체크아웃을 rounded 카드와 gentle 인터랙션으로 엮은 모바일 친화 D2C 쇼핑 경험, 한국어 1급
- **Audience**: D2C 크래프트 스낵·음료 쇼핑 고객 — rounded 상품 카드 + 친근 카피 + gentle checkout 선호, 기프팅·구독 박스 고객 — 정기 배송 / 구성 변경 / 선물 메시지 직관적 관리, 소형 D2C 브랜드 운영자 — 작은 카탈로그 + 리뷰/이모지 반응 + 소프트 CTA 정체성
- **Platforms**: web, mobile-web
- **Accessibility floor**: WCAG 2.2 AA

## 2. Identity Guardrails

- **Brand keywords**: commerce, d2c, consumer, craft, snack, wellness-food, rounded, playful, warm-pastel, friendly, emoji-friendly, gentle, soft, gift, subscription
- **Anti-keywords**: corporate-navy, minimal-tech-cool, bold-saturated, streetwear-high-contrast, magazine-serif, editorial-long-form, enterprise-sharp, dense-dashboard-only
- **Tone of voice**: friendly, warm, cheerful, gentle, approachable, sincere
- **Visual direction**: rounded corners, pastel surfaces, soft shadow, rounded product card, warm rose quartz primary, terracotta soft accent, blanched almond cream surface, emoji-friendly review, gentle add-to-cart pill, illustrated empty cart, craft d2c packaging warmth
- **Interaction direction**: rounded add-to-cart, gentle checkout, soft variant chip, emoji review reaction, soft toast, rounded dialog, bottom-sheet cart, pull-to-refresh feed, optimistic quantity bump, gentle empty-cart illustration

## 3. Design Principles

- **Commerce**: `commerce`를 시각적 선택과 인터랙션 선택의 기본 기준으로 삼습니다.
- **D2C**: `d2c`를 시각적 선택과 인터랙션 선택의 기본 기준으로 삼습니다.
- **Consumer**: `consumer`를 시각적 선택과 인터랙션 선택의 기본 기준으로 삼습니다.
- **Craft**: `craft`를 시각적 선택과 인터랙션 선택의 기본 기준으로 삼습니다.

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

- **Heading**: Nunito
- **Body**: Nunito
- **Korean**: SUIT
- **Product type detected**: consumer
- **Pairing source**: auto-scored
- **Line height**: comfortable
- **Type scale**: base 15px, ratio 1.25 (xs=12px, sm=13px, md=15px, lg=19px, xl=24px, 2xl=30px, 3xl=37px)
- **Strategy**:
  - 단일 서체(Nunito)로 weight 대비 위계 — 일관성 우선
  - 한글 서체: SUIT — 라틴과 x-height/weight 조화
- **Heading note**: 둥근 터미널의 친근한 산세리프. 교육/헬스케어 서비스에 적합.
- **Body note**: 둥근 터미널의 친근한 산세리프. 교육/헬스케어 서비스에 적합.
- **Korean rationale**: SUIT — Pretendard보다 부드럽고 친근한 인상. 교육, 라이프스타일, 커뮤니티 서비스에 적합.
- **Heading tracking**: xl=-0.01em, 2xl=-0.02em, 3xl=-0.02em
- **Primary script**: korean
- **Hangul headline defaults**: SUIT | line-height 1.25-1.35 | tracking 0em
- **Hangul body defaults**: SUIT | line-height 1.6-1.7 | label line-height 1.4-1.5
- **Wrap defaults**: headline word-break=keep-all, headline text-wrap=balance, body word-break=keep-all
- **Scale guidance**: 기본 스케일을 사용할 수 있지만 한글 문장 기준으로 실제 wrap을 먼저 검증한다.
- **Hangul warning**: 기관/금융 — 너무 캐주얼할 수 있음
- **Hangul warning**: 기관/금융 — 너무 캐주얼할 수 있음
- **Loading**: Nunito(preload), SUIT(preload) | display: swap

## 6. Color Reference

- **Source**: REFERENCE X Vol.1 - Color Reference (/Users/sungwoon/ai-projects/design-ontology-harness/docs/color-reference.md)
- **Selection mode**: manual
- **Preferred families**: Pastel Reds, Pastel Oranges, Pastel Yellows
- **Palette strategy**: temperature=warm, contrast=soft, diversity=balanced, surface_style=tinted
- **Palette expansion**: supporting_color_count=10, combination_count=3, prefer_pairings=True
- **Palette roles**:
  - `primary` -> Rose Quartz #F7CAC9 / Pastel Reds
  - `accent` -> Dark Salmon #E9967A / Pastel Oranges
  - `surface_tint` -> Blanched Almond #FFEBCD / Pastel Yellows
- **Selected colors**:
  - Salmon #FA8072 / Pastel Reds / 밝고 따뜻한 핑크 오렌지 톤 / 따뜻함, 부드러움, 친근함, 자연스러움
  - Peach Puff #FFDAB9 / Pastel Oranges / 고명도, 저채도, 오렌지와 핑크 사이의 파스텔 계열 / 따뜻함, 부드러움, 순수함, 친근함, 생기
  - Rose Quartz #F7CAC9 / Pastel Reds / 고명도, 저채도, 살구빛이 섞인 파스텔 핑크 / 부드러움, 친근함, 따뜻함, 크래프트, 달콤한 소비자 감성
- **Palette candidates**:
  - signature-1 (Signature): primary=Salmon, accent=Peach Puff, surface_tint=Rose Quartz / Salmon is inside preferred families.; Peach Puff is inside preferred families.
- **Expanded supporting colors**:
  - Rose Quartz #F7CAC9 / Pastel Reds / pairing-reference / Rose Quartz stays inside the preferred families.; Rose Quartz reinforces the brand mood signals.
  - Dark Salmon #E9967A / Pastel Oranges / pairing-reference / Dark Salmon stays inside the preferred families.; Dark Salmon reinforces the brand mood signals.
  - Blanched Almond #FFEBCD / Pastel Yellows / pairing-reference / Blanched Almond stays inside the preferred families.; Blanched Almond reinforces the brand mood signals.
  - Peach Puff #FFDAB9 / Pastel Oranges / reference-color / Peach Puff stays inside the preferred families.; Peach Puff reinforces the brand mood signals.
  - Salmon #FA8072 / Pastel Reds / reference-color / Salmon stays inside the preferred families.; Salmon reinforces the brand mood signals.
  - Creamsicle #FFD7A0 / Pastel Oranges / reference-color / Creamsicle stays inside the preferred families.; Creamsicle reinforces the brand mood signals.
  - Powder Blue #B0E0E6 / Pastel Blues / pairing-reference / Powder Blue reinforces the brand mood signals.; Powder Blue comes from the seed pairing references.
  - Buttercream #F3E5AB / Pastel Yellows / reference-color / Buttercream stays inside the preferred families.; Buttercream reinforces the brand mood signals.
- **Expanded semantic roles**:
  - `brand_primary` -> Rose Quartz #F7CAC9 / Pastel Reds
  - `brand_accent` -> Dark Salmon #E9967A / Pastel Oranges
  - `surface_tint` -> Blanched Almond #FFEBCD / Pastel Yellows
  - `canvas` -> Canvas White #F7F8FA / Generated Fallback
  - `surface` -> Paper #FFFFFF / Generated Fallback
  - `surface_muted` -> Surface Muted #EEF1F6 / Generated Fallback
  - `surface_elevated` -> Paper #FFFFFF / Generated Fallback
  - `border` -> Border Neutral #D6DDE6 / Generated Fallback
  - `border_strong` -> Border Strong #B0BAC7 / Generated Fallback
  - `ink` -> Ink #111111 / Generated Fallback
- **Combination lists**:
  - Seed Core: primary=Rose Quartz, accent=Dark Salmon, surface_tint=Blanched Almond
  - Surface System: canvas=Canvas White, surface=Paper, surface_tint=Blanched Almond, border=Border Neutral, ink=Ink, ink_muted=Muted Ink
  - Support Spectrum: support=Rose Quartz, support=Dark Salmon, support=Blanched Almond, support=Peach Puff, support=Salmon, support=Creamsicle
- **Notes**: Rose Quartz #F7CAC9 primary — Pantone 13-1520 warm pastel pink, primary-button / variant-chip active / add-to-cart pill / cart-drawer header / subscription toggle on, Dark Salmon #E9967A accent — warm terracotta-salmon, discount-pill / gentle-toast 성공 / review heart / gift message highlight / bestseller ribbon, Blanched Almond #FFEBCD surface_tint — cream warm near-white, product-card soft hover surface / cart drawer bg tint / empty-state illustration / bottom-sheet handle area, light mode 가 기본 — D2C consumer commerce 관례, dark 옵션 제공 (warm deep neutral + 채도 낮춘 Rose Quartz/Dark Salmon + Blanched Almond soft border), 기존 17종 프리셋 HEX 와 겹침 0 — Rose Quartz #F7CAC9 / Dark Salmon #E9967A / Blanched Almond #FFEBCD 조합, bloom (community-feed--playful-soft) #F88379/#98FF98/#FFF8DC 와 전면 차별화 — playful-soft commerce 정체성은 warm pink + terracotta + cream (feed 의 coral + mint 와 대비), meadow (dashboard--playful-soft) #8E9AF1/#FFDAB9/#E0B0FF 와 전면 차별화 — consumer wellness admin 의 violet-peach-mauve 와 다른 pink-terracotta-cream 정체성, colorfit (commerce--editorial-warm) / drop (commerce--bold-confident) 와도 HEX 겹침 0 — 동일 app_mode 내 commerce 톤 다변화
- **Application rule**: 레퍼런스 컬러는 semantic token으로 번역해서 사용하고, 접근성과 theme 호환성을 우선합니다.

## 7. Visual Reference Signals

- **Mode**: local-images
- **Coverage**: source 0 / image 0 / selected 0
- **Rule**: visual references are advisory signals for motif and layout direction; official KB/spec remain the structural source of truth.
- **Provenance**: `observed` = directly measured from local pixels, `inferred` = synthesized from image/query/brand signals, `unverified` = reliable visual evidence not yet available.
- **Query seeds**: olipop d2c soda ecommerce, magic spoon cereal shop, poppi prebiotic soda store, graza olive oil craft d2c, caraway cookware warm pastel shop
### Visual Direction

- **Density**: balanced (confidence 0.66, provenance inferred) / product x8
- **Surface Style**: tinted (confidence 0.94, provenance inferred) / warm x6, editorial x2, cream x2
- **Corner Style**: round (confidence 0.94, provenance inferred) / rounded x10, soft x11
- **Typography Mood**: editorial (confidence 0.75, provenance inferred) / editorial x2, magazine x2, serif x1
- **Color balance**: temperature=unknown, contrast=unknown, neutral_bias=unknown, provenance=unverified

### Layout Rhythm

- **Data review surface**: confidence 0.92 / provenance inferred / table x1, grid x4, data x1
- **Editorial feed**: confidence 0.87 / provenance inferred / editorial x2, feed x1, magazine x2
- **Dashboard grid**: confidence 0.5 / provenance inferred / dashboard x1, table x1
- **Narrative landing flow**: confidence 0.4 / provenance inferred / hero x1

### Image-derived Component Hints

- **Cards**: low-elevation tinted cards를 기본으로 하고, 균형 잡힌 spacing과 명확한 slot hierarchy. soft round corner를 기본값으로 유지. / provenance inferred / surface=tinted, density=balanced, corner=round
- **Navigation**: navigation은 정보 구조를 안정적으로 고정하고 시각적 장식보다 위치 신호를 우선한다. / provenance inferred / Data review surface
- **Typography**: headline rhythm과 본문 리듬의 대비를 키우고, label/metadata는 조용하게 유지한다. / provenance inferred / typography_mood=editorial
- **Data Display**: 정보 밀도를 유지하되 thin dividers와 restrained accent로 hierarchy를 만든다. / provenance inferred / layout=dashboard-grid, density=balanced

### Synthesis Notes

- layout는 Data review surface 기준으로 정리
- surface language는 tinted 성향 우선
- typography mood는 editorial 축 유지
- density는 balanced 기준으로 primitive spacing 조정
- palette temperature는 unknown 쪽을 우선
- Avoid: streetwear drop high-contrast product grid
- Avoid: fashion editorial hero masthead
- Avoid: fintech dense data-table
- Avoid: SRE alert severity grid

## 8. Component Strategy

- **Product primitives**: product grid, product card, product detail, variant chip, add-to-cart pill, quantity stepper, cart drawer, cart line-item, checkout form, shipping step, payment step, order summary, review card, emoji reaction, empty cart, gentle toast, soft dialog, bottom sheet, gift-message input, subscription toggle
- **Required families**: button, data-display, editorial, feedback, input, marketing, navigation, commerce, dashboard-growth, dashboard-wellness, overlay, social
- **Visual-reference archetypes**:

- **Data review table** (data-display / 0.94): data-table, column-header, row-actions, filter-toolbar, pagination
- **Editorial content block** (editorial / 0.94): content-card, featured-story-card, section-header, content-meta, byline-row
- **Dashboard insight module** (data-display / 0.54): stat-card, insight-card, chart-panel, section-header, filter-chip
- **Marketing hero stack** (marketing / 0.51): hero-section, hero-headline, hero-visual, cta-button-group, trust-strip

- **button**: primary-button, secondary-button, ghost-button, icon-button, cta-button, link-button, form-actions, add-to-cart-button
- **data-display**: pricing-card, feature-comparison, tag, comment-thread, search-results, tag-pill, chat-message, chat-thread / visual signals: Data review table (0.94)
- **editorial**: editor-canvas, editor-toolbar, inline-format-menu, slash-command-menu, block-controls, content-card, featured-story-card, content-meta / visual signals: Editorial content block (0.94)
- **feedback**: inline-alert, empty-state, toast, upgrade-banner, status-badge, discount-badge, checkout-step-progress, empty-cart-state
- **input**: text-field, search-field, segmented-control, textarea, select, checkbox, radio-group, form-section
- **marketing**: hero-container, hero-eyebrow, hero-headline, hero-subheadline, hero-visual, hero-trust-strip
- **navigation**: mobile-topbar, mobile-tab-bar, back-button, section-tabs, category-pill, wizard-layout, pagination, filter-bar
- **commerce**: product-grid, product-card, product-detail, product-gallery, product-hero-image, image-thumbnail, price-tag, original-price-strikethrough
- **dashboard-growth**: activation-funnel, cohort-matrix, referral-widget, retention-chart, conversion-funnel, experiment-panel, goal-tracker, user-list
- **dashboard-wellness**: dashboard-card, streak-indicator, habit-calendar, wellness-score, mood-check, mood-chart, session-tracker, session-timeline
- **overlay**: bottom-sheet, modal-dialog, quick-view-modal, mention-popup, autocomplete, confirm-dialog, share-sheet, soft-dialog
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

- Warning: visual_reference.sources is empty

## 14. Quick Start

이 문서는 **Orchard System**의 디자인 시스템 사양입니다.

### 시작하기

1. **토큰 적용**: Drop-in CSS(아래 섹션 16)의 CSS 변수를 프로젝트에 복사합니다.
2. **컬러 세팅**: Color Reference(섹션 6)의 semantic role을 기준으로 surface/text/border를 잡습니다.
3. **타이포 세팅**: Token Strategy(섹션 5)의 font family와 type scale을 적용합니다.
4. **시각 방향 확인**: Visual Reference Signals(섹션 7)에서 density/surface/layout cue를 먼저 확인합니다.
5. **컴포넌트 구현**: Component Strategy(섹션 8)의 family 순서대로 하나씩 빌드합니다.

### 우선순위

핵심 primitive: **product grid, product card, product detail, variant chip, add-to-cart pill**

이 primitive를 지원하는 컴포넌트부터 구현하고, 나머지는 필요에 따라 확장합니다.

## 15. DO / DON'T

### DO

- **Commerce**: commerce와 충돌하는 컴포넌트 변형은 만들지 않기
- **D2C**: d2c와 충돌하는 컴포넌트 변형은 만들지 않기
- **Consumer**: consumer와 충돌하는 컴포넌트 변형은 만들지 않기
- **Craft**: craft와 충돌하는 컴포넌트 변형은 만들지 않기
- 모든 시각적 선택에서 **commerce, d2c, consumer** 기준을 적용
- semantic token을 통해 컬러를 적용 (하드코딩 금지)
- 접근성 기준을 모든 text/surface 조합에서 먼저 검증
- 컴포넌트 변형 추가 전 기존 variant로 해결 가능한지 먼저 확인
- 아이콘은 SVG 컴포넌트 또는 Lucide/Heroicons/Phosphor/Tabler 등 라이브러리로 구현
- component_specs.md의 anatomy/states/token binding을 그대로 따라 완전히 구현

### DON'T

- **corporate-navy** 방향의 디자인 결정을 하지 않음
- **minimal-tech-cool** 방향의 디자인 결정을 하지 않음
- **bold-saturated** 방향의 디자인 결정을 하지 않음
- **streetwear-high-contrast** 방향의 디자인 결정을 하지 않음
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
  --font-heading: 'Nunito', serif;
  --font-body: 'Nunito', sans-serif;
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
  --color-primary: #F7CAC9;
  --color-accent: #E9967A;
  --color-surface-tint: #FFEBCD;

  /* --- Semantic roles (expanded) --- */
  --color-brand-primary: #F7CAC9;
  --color-brand-accent: #E9967A;
  --color-surface-tint: #FFEBCD;
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
  --color-primary-support: #FA8072;
  --color-accent-support: #FFDAB9;
  --color-info: #B0E0E6;
  --color-success: #4A7C59;
  --color-warning: #E9967A;
  --color-danger: #F7CAC9;
  --color-link: #F7CAC9;
  --color-link-hover: #F2A7A5;

  /* --- Button — primary --- */
  --color-button-primary-surface-default: #F7CAC9;
  --color-button-primary-surface-hover: #F3B0AE;
  --color-button-primary-surface-active: #F09E9D;
  --color-button-primary-surface-disabled: #F7E6E6;
  --color-button-primary-text-default: #111111;
  --color-button-primary-text-disabled: #848486;
  --color-button-primary-border-default: #F7CAC9;
  --color-button-primary-focus-ring: #F7CAC9;

  /* --- Button — secondary --- */
  --color-button-secondary-surface-default: #FFFFFF;
  --color-button-secondary-surface-hover: #F1F1F1;
  --color-button-secondary-surface-active: #E7E7E7;
  --color-button-secondary-surface-disabled: #F7F8FA;
  --color-button-secondary-text-default: #111111;
  --color-button-secondary-text-disabled: #909091;
  --color-button-secondary-border-default: #BDC8D7;
  --color-button-secondary-border-hover: #A3B3C7;
  --color-button-secondary-focus-ring: #F7CAC9;

  /* --- Button — ghost --- */
  --color-button-ghost-surface-default: transparent;
  --color-button-ghost-surface-hover: #F3F3F3;
  --color-button-ghost-surface-active: #EAEAEA;
  --color-button-ghost-surface-disabled: transparent;
  --color-button-ghost-text-default: #4B5563;
  --color-button-ghost-text-hover: #111111;
  --color-button-ghost-text-disabled: #AAAFB6;
  --color-button-ghost-border-default: transparent;
  --color-button-ghost-focus-ring: #F7CAC9;

  /* --- Button — danger --- */
  --color-button-danger-surface-default: #F7CAC9;
  --color-button-danger-surface-hover: #F3B0AE;
  --color-button-danger-surface-active: #F09E9D;
  --color-button-danger-text-default: #111111;
  --color-button-danger-border-default: #F7CAC9;
  --color-button-danger-focus-ring: #F7CAC9;

  /* --- Input --- */
  --color-input-surface-default: #FFFFFF;
  --color-input-surface-filled: #FFFFFF;
  --color-input-surface-disabled: #F7F8FA;
  --color-input-text-default: #111111;
  --color-input-text-placeholder: #90969F;
  --color-input-text-disabled: #AAAFB6;
  --color-input-border-default: #D6DDE6;
  --color-input-border-hover: #B6C3D3;
  --color-input-border-focus: #F7CAC9;
  --color-input-border-error: #F7CAC9;
  --color-input-border-disabled: #E6EAF0;

  /* --- Card --- */
  --color-card-surface-default: #FFFFFF;
  --color-card-surface-hover: #FAFAFA;
  --color-card-surface-muted: #F7F8FA;
  --color-card-border-default: #D6DDE6;
  --color-card-border-hover: #B6C3D3;
  --color-card-border-focus: #F7CAC9;

  /* --- Nav link --- */
  --color-nav-link-text-default: #4B5563;
  --color-nav-link-text-hover: #111111;
  --color-nav-link-text-active: #F7CAC9;
  --color-nav-link-surface-hover: #F5F5F5;
  --color-nav-link-indicator: #E9967A;

  /* --- Link --- */
  --color-link-text-default: #F7CAC9;
  --color-link-text-hover: #F09E9D;
  --color-link-text-visited: #EBBDBC;

  /* --- Feedback — info --- */
  --color-feedback-info-surface: #F6FBFC;
  --color-feedback-info-text: #B0E0E6;
  --color-feedback-info-border: #C5E7EC;
  --color-feedback-info-icon: #B0E0E6;

  /* --- Feedback — success --- */
  --color-feedback-success-surface: #E9EFEB;
  --color-feedback-success-text: #4A7C59;
  --color-feedback-success-border: #7EA189;
  --color-feedback-success-icon: #4A7C59;

  /* --- Feedback — warning --- */
  --color-feedback-warning-surface: #FCF2EF;
  --color-feedback-warning-text: #E9967A;
  --color-feedback-warning-border: #EDB3A0;
  --color-feedback-warning-icon: #E9967A;

  /* --- Feedback — danger --- */
  --color-feedback-danger-surface: #FEF9F9;
  --color-feedback-danger-text: #F7CAC9;
  --color-feedback-danger-border: #F7D8D8;
  --color-feedback-danger-icon: #F7CAC9;

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
| activation-funnel | `color.Blanched Almond→background`, `spacing.12→padding`, `radius.md→radius`, `font:Nunito` |
| activity-card | `color.Blanched Almond→background`, `spacing.12→padding`, `radius.md→radius`, `font:Nunito` |
| add-to-cart-button | `color.Rose Quartz→surface`, `color.Dark Salmon→emphasis`, `color.Blanched Almond→background`, `spacing.12→padding`, `radius.md→radius`, `font:Nunito` |
| address-form | `color.Rose Quartz→surface`, `color.Dark Salmon→emphasis`, `color.Blanched Almond→background`, `spacing.12→padding`, `radius.md→radius`, `font:Nunito` |
| alert-list | `color.Blanched Almond→background`, `spacing.12→padding`, `radius.md→radius`, `font:Nunito` |
| app-shell | `color.Rose Quartz→surface`, `color.Dark Salmon→emphasis`, `color.Blanched Almond→background`, `spacing.12→padding`, `radius.md→radius`, `font:Nunito` |
| autocomplete | `color.Rose Quartz→surface`, `color.Dark Salmon→emphasis`, `color.Blanched Almond→background`, `spacing.12→padding`, `radius.md→radius`, `font:Nunito` |
| avatar | `color.Blanched Almond→background`, `spacing.12→padding`, `radius.md→radius`, `font:Nunito` |
| avatar-cluster | `color.Blanched Almond→background`, `spacing.12→padding`, `radius.md→radius`, `font:Nunito` |
| back-button | `color.Rose Quartz→surface`, `color.Dark Salmon→emphasis`, `color.Blanched Almond→background`, `spacing.12→padding`, `radius.md→radius`, `font:Nunito` |
| banner | `color.Blanched Almond→background`, `spacing.12→padding`, `radius.md→radius`, `font:Nunito` |
| block-controls | `color.Blanched Almond→background`, `spacing.12→padding`, `radius.md→radius`, `font:Nunito` |
| bottom-sheet | `color.Rose Quartz→surface`, `color.Dark Salmon→emphasis`, `color.Blanched Almond→background`, `spacing.12→padding`, `radius.md→radius`, `font:Nunito` |
| breadcrumb | `color.Rose Quartz→surface`, `color.Dark Salmon→emphasis`, `color.Blanched Almond→background`, `spacing.12→padding`, `radius.md→radius`, `font:Nunito` |
| byline-row | `color.Blanched Almond→background`, `spacing.12→padding`, `radius.md→radius`, `font:Nunito` |
| cart-drawer | `color.Blanched Almond→background`, `spacing.12→padding`, `radius.md→radius`, `font:Nunito` |
| cart-item | `color.Blanched Almond→background`, `spacing.12→padding`, `radius.md→radius`, `font:Nunito` |
| cart-summary | `color.Blanched Almond→background`, `spacing.12→padding`, `radius.md→radius`, `font:Nunito` |
| category-pill | `color.Rose Quartz→surface`, `color.Dark Salmon→emphasis`, `color.Blanched Almond→background`, `spacing.12→padding`, `radius.md→radius`, `font:Nunito` |
| chat-input | `color.Rose Quartz→surface`, `color.Dark Salmon→emphasis`, `color.Blanched Almond→background`, `spacing.12→padding`, `radius.md→radius`, `font:Nunito` |
| chat-message | `color.Blanched Almond→background`, `spacing.12→padding`, `radius.md→radius`, `font:Nunito` |
| chat-thread | `color.Blanched Almond→background`, `spacing.12→padding`, `radius.md→radius`, `font:Nunito` |
| checkbox | `color.Rose Quartz→surface`, `color.Dark Salmon→emphasis`, `color.Blanched Almond→background`, `spacing.12→padding`, `radius.md→radius`, `font:Nunito` |
| checkout-step | `color.Blanched Almond→background`, `spacing.12→padding`, `radius.md→radius`, `font:Nunito` |
| checkout-step-progress | `color.Blanched Almond→background`, `spacing.12→padding`, `radius.md→radius`, `font:Nunito` |
| chip | `color.Rose Quartz→surface`, `color.Dark Salmon→emphasis`, `color.Blanched Almond→background`, `spacing.12→padding`, `radius.md→radius`, `font:Nunito` |
| cohort-matrix | `color.Blanched Almond→background`, `spacing.12→padding`, `radius.md→radius`, `font:Nunito` |
| color-swatch-selector | `color.Rose Quartz→surface`, `color.Dark Salmon→emphasis`, `color.Blanched Almond→background`, `spacing.12→padding`, `radius.md→radius`, `font:Nunito` |
| column-header | `color.Blanched Almond→background`, `spacing.12→padding`, `radius.md→radius`, `font:Nunito` |
| comment-input | `color.Rose Quartz→surface`, `color.Dark Salmon→emphasis`, `color.Blanched Almond→background`, `spacing.12→padding`, `radius.md→radius`, `font:Nunito` |
| comment-thread | `color.Blanched Almond→background`, `spacing.12→padding`, `radius.md→radius`, `font:Nunito` |
| confirm-dialog | `color.Rose Quartz→surface`, `color.Dark Salmon→emphasis`, `color.Blanched Almond→background`, `spacing.12→padding`, `radius.md→radius`, `font:Nunito` |
| content-card | `color.Blanched Almond→background`, `spacing.12→padding`, `radius.md→radius`, `font:Nunito` |
| content-meta | `color.Blanched Almond→background`, `spacing.12→padding`, `radius.md→radius`, `font:Nunito` |
| conversion-funnel | `color.Blanched Almond→background`, `spacing.12→padding`, `radius.md→radius`, `font:Nunito` |
| cross-sell-grid | `color.Blanched Almond→background`, `spacing.12→padding`, `radius.md→radius`, `font:Nunito` |
| cta-button | `color.Rose Quartz→surface`, `color.Dark Salmon→emphasis`, `color.Blanched Almond→background`, `spacing.12→padding`, `radius.md→radius`, `font:Nunito` |
| dashboard-card | `color.Blanched Almond→background`, `spacing.12→padding`, `radius.md→radius`, `font:Nunito` |
| data-table | `color.Blanched Almond→background`, `spacing.12→padding`, `radius.md→radius`, `font:Nunito` |
| discount-badge | `color.Blanched Almond→background`, `spacing.12→padding`, `radius.md→radius`, `font:Nunito` |
| editor-canvas | `color.Blanched Almond→background`, `spacing.12→padding`, `radius.md→radius`, `font:Nunito` |
| editor-toolbar | `color.Blanched Almond→background`, `spacing.12→padding`, `radius.md→radius`, `font:Nunito` |
| empty-cart-state | `color.Blanched Almond→background`, `spacing.12→padding`, `radius.md→radius`, `font:Nunito` |
| empty-feed-illustration | `color.Blanched Almond→background`, `spacing.12→padding`, `radius.md→radius`, `font:Nunito` |
| empty-state | `color.Blanched Almond→background`, `spacing.12→padding`, `radius.md→radius`, `font:Nunito` |
| experiment-panel | `color.Blanched Almond→background`, `spacing.12→padding`, `radius.md→radius`, `font:Nunito` |
| feature-comparison | `color.Blanched Almond→background`, `spacing.12→padding`, `radius.md→radius`, `font:Nunito` |
| featured-story-card | `color.Blanched Almond→background`, `spacing.12→padding`, `radius.md→radius`, `font:Nunito` |
| feed-item | `color.Blanched Almond→background`, `spacing.12→padding`, `radius.md→radius`, `font:Nunito` |
| filter-bar | `color.Rose Quartz→surface`, `color.Dark Salmon→emphasis`, `color.Blanched Almond→background`, `spacing.12→padding`, `radius.md→radius`, `font:Nunito` |
| filter-chip | `color.Rose Quartz→surface`, `color.Dark Salmon→emphasis`, `color.Blanched Almond→background`, `spacing.12→padding`, `radius.md→radius`, `font:Nunito` |
| filter-panel | `color.Rose Quartz→surface`, `color.Dark Salmon→emphasis`, `color.Blanched Almond→background`, `spacing.12→padding`, `radius.md→radius`, `font:Nunito` |
| filter-sidebar | `color.Rose Quartz→surface`, `color.Dark Salmon→emphasis`, `color.Blanched Almond→background`, `spacing.12→padding`, `radius.md→radius`, `font:Nunito` |
| filter-toolbar | `color.Blanched Almond→background`, `spacing.12→padding`, `radius.md→radius`, `font:Nunito` |
| follow-button | `color.Rose Quartz→surface`, `color.Dark Salmon→emphasis`, `color.Blanched Almond→background`, `spacing.12→padding`, `radius.md→radius`, `font:Nunito` |
| form-actions | `color.Rose Quartz→surface`, `color.Dark Salmon→emphasis`, `color.Blanched Almond→background`, `spacing.12→padding`, `radius.md→radius`, `font:Nunito` |
| form-section | `color.Rose Quartz→surface`, `color.Dark Salmon→emphasis`, `color.Blanched Almond→background`, `spacing.12→padding`, `radius.md→radius`, `font:Nunito` |
| gentle-toast | `color.Blanched Almond→background`, `spacing.12→padding`, `radius.md→radius`, `font:Nunito` |
| ghost-button | `color.Rose Quartz→surface`, `color.Dark Salmon→emphasis`, `color.Blanched Almond→background`, `spacing.12→padding`, `radius.md→radius`, `font:Nunito` |
| goal-grid | `color.Blanched Almond→background`, `spacing.12→padding`, `radius.md→radius`, `font:Nunito` |
| goal-tracker | `color.Blanched Almond→background`, `spacing.12→padding`, `radius.md→radius`, `font:Nunito` |
| habit-calendar | `color.Blanched Almond→background`, `spacing.12→padding`, `radius.md→radius`, `font:Nunito` |
| hero-container | `color.Blanched Almond→background`, `spacing.12→padding`, `radius.md→radius`, `font:Nunito` |
| hero-cta-group | `color.Rose Quartz→surface`, `color.Dark Salmon→emphasis`, `color.Blanched Almond→background`, `spacing.12→padding`, `radius.md→radius`, `font:Nunito` |
| hero-eyebrow | `color.Blanched Almond→background`, `spacing.12→padding`, `radius.md→radius`, `font:Nunito` |
| hero-headline | `color.Blanched Almond→background`, `spacing.12→padding`, `radius.md→radius`, `font:Nunito` |
| hero-subheadline | `color.Blanched Almond→background`, `spacing.12→padding`, `radius.md→radius`, `font:Nunito` |
| hero-trust-strip | `color.Blanched Almond→background`, `spacing.12→padding`, `radius.md→radius`, `font:Nunito` |
| hero-visual | `color.Blanched Almond→background`, `spacing.12→padding`, `radius.md→radius`, `font:Nunito` |
| icon-button | `color.Rose Quartz→surface`, `color.Dark Salmon→emphasis`, `color.Blanched Almond→background`, `spacing.12→padding`, `radius.md→radius`, `font:Nunito` |
| image-thumbnail | `color.Blanched Almond→background`, `spacing.12→padding`, `radius.md→radius`, `font:Nunito` |
| inline-alert | `color.Blanched Almond→background`, `spacing.12→padding`, `radius.md→radius`, `font:Nunito` |
| inline-format-menu | `color.Blanched Almond→background`, `spacing.12→padding`, `radius.md→radius`, `font:Nunito` |
| insight-card | `color.Blanched Almond→background`, `spacing.12→padding`, `radius.md→radius`, `font:Nunito` |
| kanban-board | `color.Blanched Almond→background`, `spacing.12→padding`, `radius.md→radius`, `font:Nunito` |
| kanban-card | `color.Blanched Almond→background`, `spacing.12→padding`, `radius.md→radius`, `font:Nunito` |
| kanban-column | `color.Blanched Almond→background`, `spacing.12→padding`, `radius.md→radius`, `font:Nunito` |
| link-button | `color.Rose Quartz→surface`, `color.Dark Salmon→emphasis`, `color.Blanched Almond→background`, `spacing.12→padding`, `radius.md→radius`, `font:Nunito` |
| mention-popup | `color.Rose Quartz→surface`, `color.Dark Salmon→emphasis`, `color.Blanched Almond→background`, `spacing.12→padding`, `radius.md→radius`, `font:Nunito` |
| mobile-tab-bar | `color.Rose Quartz→surface`, `color.Dark Salmon→emphasis`, `color.Blanched Almond→background`, `spacing.12→padding`, `radius.md→radius`, `font:Nunito` |
| mobile-topbar | `color.Rose Quartz→surface`, `color.Dark Salmon→emphasis`, `color.Blanched Almond→background`, `spacing.12→padding`, `radius.md→radius`, `font:Nunito` |
| modal-dialog | `color.Rose Quartz→surface`, `color.Dark Salmon→emphasis`, `color.Blanched Almond→background`, `spacing.12→padding`, `radius.md→radius`, `font:Nunito` |
| mood-chart | `color.Blanched Almond→background`, `spacing.12→padding`, `radius.md→radius`, `font:Nunito` |
| mood-check | `color.Blanched Almond→background`, `spacing.12→padding`, `radius.md→radius`, `font:Nunito` |
| order-summary | `color.Blanched Almond→background`, `spacing.12→padding`, `radius.md→radius`, `font:Nunito` |
| original-price-strikethrough | `color.Blanched Almond→background`, `spacing.12→padding`, `radius.md→radius`, `font:Nunito` |
| pagination | `color.Rose Quartz→surface`, `color.Dark Salmon→emphasis`, `color.Blanched Almond→background`, `spacing.12→padding`, `radius.md→radius`, `font:Nunito` |
| payment-form | `color.Rose Quartz→surface`, `color.Dark Salmon→emphasis`, `color.Blanched Almond→background`, `spacing.12→padding`, `radius.md→radius`, `font:Nunito` |
| post-card | `color.Blanched Almond→background`, `spacing.12→padding`, `radius.md→radius`, `font:Nunito` |
| price-tag | `color.Blanched Almond→background`, `spacing.12→padding`, `radius.md→radius`, `font:Nunito` |
| pricing-card | `color.Blanched Almond→background`, `spacing.12→padding`, `radius.md→radius`, `font:Nunito` |
| primary-button | `color.Rose Quartz→surface`, `color.Dark Salmon→emphasis`, `color.Blanched Almond→background`, `spacing.12→padding`, `radius.md→radius`, `font:Nunito` |
| product-card | `color.Blanched Almond→background`, `spacing.12→padding`, `radius.md→radius`, `font:Nunito` |
| product-detail | `color.Blanched Almond→background`, `spacing.12→padding`, `radius.md→radius`, `font:Nunito` |
| product-gallery | `color.Blanched Almond→background`, `spacing.12→padding`, `radius.md→radius`, `font:Nunito` |
| product-grid | `color.Blanched Almond→background`, `spacing.12→padding`, `radius.md→radius`, `font:Nunito` |
| product-hero-image | `color.Blanched Almond→background`, `spacing.12→padding`, `radius.md→radius`, `font:Nunito` |
| profile-card | `color.Blanched Almond→background`, `spacing.12→padding`, `radius.md→radius`, `font:Nunito` |
| promo-code-input | `color.Rose Quartz→surface`, `color.Dark Salmon→emphasis`, `color.Blanched Almond→background`, `spacing.12→padding`, `radius.md→radius`, `font:Nunito` |
| quantity-stepper | `color.Rose Quartz→surface`, `color.Dark Salmon→emphasis`, `color.Blanched Almond→background`, `spacing.12→padding`, `radius.md→radius`, `font:Nunito` |
| quick-view-modal | `color.Rose Quartz→surface`, `color.Dark Salmon→emphasis`, `color.Blanched Almond→background`, `spacing.12→padding`, `radius.md→radius`, `font:Nunito` |
| radio-group | `color.Rose Quartz→surface`, `color.Dark Salmon→emphasis`, `color.Blanched Almond→background`, `spacing.12→padding`, `radius.md→radius`, `font:Nunito` |
| reaction-bar | `color.Blanched Almond→background`, `spacing.12→padding`, `radius.md→radius`, `font:Nunito` |
| referral-widget | `color.Blanched Almond→background`, `spacing.12→padding`, `radius.md→radius`, `font:Nunito` |
| reply-composer | `color.Rose Quartz→surface`, `color.Dark Salmon→emphasis`, `color.Blanched Almond→background`, `spacing.12→padding`, `radius.md→radius`, `font:Nunito` |
| retention-chart | `color.Blanched Almond→background`, `spacing.12→padding`, `radius.md→radius`, `font:Nunito` |
| row-actions | `color.Blanched Almond→background`, `spacing.12→padding`, `radius.md→radius`, `font:Nunito` |
| search-field | `color.Rose Quartz→surface`, `color.Dark Salmon→emphasis`, `color.Blanched Almond→background`, `spacing.12→padding`, `radius.md→radius`, `font:Nunito` |
| search-results | `color.Blanched Almond→background`, `spacing.12→padding`, `radius.md→radius`, `font:Nunito` |
| secondary-button | `color.Rose Quartz→surface`, `color.Dark Salmon→emphasis`, `color.Blanched Almond→background`, `spacing.12→padding`, `radius.md→radius`, `font:Nunito` |
| section-header | `color.Blanched Almond→background`, `spacing.12→padding`, `radius.md→radius`, `font:Nunito` |
| section-tabs | `color.Rose Quartz→surface`, `color.Dark Salmon→emphasis`, `color.Blanched Almond→background`, `spacing.12→padding`, `radius.md→radius`, `font:Nunito` |
| segment-filter | `color.Rose Quartz→surface`, `color.Dark Salmon→emphasis`, `color.Blanched Almond→background`, `spacing.12→padding`, `radius.md→radius`, `font:Nunito` |
| segmented-control | `color.Rose Quartz→surface`, `color.Dark Salmon→emphasis`, `color.Blanched Almond→background`, `spacing.12→padding`, `radius.md→radius`, `font:Nunito` |
| select | `color.Rose Quartz→surface`, `color.Dark Salmon→emphasis`, `color.Blanched Almond→background`, `spacing.12→padding`, `radius.md→radius`, `font:Nunito` |
| session-timeline | `color.Blanched Almond→background`, `spacing.12→padding`, `radius.md→radius`, `font:Nunito` |
| session-tracker | `color.Blanched Almond→background`, `spacing.12→padding`, `radius.md→radius`, `font:Nunito` |
| share-sheet | `color.Rose Quartz→surface`, `color.Dark Salmon→emphasis`, `color.Blanched Almond→background`, `spacing.12→padding`, `radius.md→radius`, `font:Nunito` |
| sidebar-nav | `color.Rose Quartz→surface`, `color.Dark Salmon→emphasis`, `color.Blanched Almond→background`, `spacing.12→padding`, `radius.md→radius`, `font:Nunito` |
| size-selector | `color.Rose Quartz→surface`, `color.Dark Salmon→emphasis`, `color.Blanched Almond→background`, `spacing.12→padding`, `radius.md→radius`, `font:Nunito` |
| slash-command-menu | `color.Blanched Almond→background`, `spacing.12→padding`, `radius.md→radius`, `font:Nunito` |
| soft-dialog | `color.Rose Quartz→surface`, `color.Dark Salmon→emphasis`, `color.Blanched Almond→background`, `spacing.12→padding`, `radius.md→radius`, `font:Nunito` |
| sort-dropdown | `color.Rose Quartz→surface`, `color.Dark Salmon→emphasis`, `color.Blanched Almond→background`, `spacing.12→padding`, `radius.md→radius`, `font:Nunito` |
| stat-card | `color.Blanched Almond→background`, `spacing.12→padding`, `radius.md→radius`, `font:Nunito` |
| status-badge | `color.Blanched Almond→background`, `spacing.12→padding`, `radius.md→radius`, `font:Nunito` |
| step-progress | `color.Blanched Almond→background`, `spacing.12→padding`, `radius.md→radius`, `font:Nunito` |
| streak-indicator | `color.Blanched Almond→background`, `spacing.12→padding`, `radius.md→radius`, `font:Nunito` |
| tab-bar | `color.Rose Quartz→surface`, `color.Dark Salmon→emphasis`, `color.Blanched Almond→background`, `spacing.12→padding`, `radius.md→radius`, `font:Nunito` |
| tag | `color.Blanched Almond→background`, `spacing.12→padding`, `radius.md→radius`, `font:Nunito` |
| tag-pill | `color.Blanched Almond→background`, `spacing.12→padding`, `radius.md→radius`, `font:Nunito` |
| text-field | `color.Rose Quartz→surface`, `color.Dark Salmon→emphasis`, `color.Blanched Almond→background`, `spacing.12→padding`, `radius.md→radius`, `font:Nunito` |
| textarea | `color.Rose Quartz→surface`, `color.Dark Salmon→emphasis`, `color.Blanched Almond→background`, `spacing.12→padding`, `radius.md→radius`, `font:Nunito` |
| thread-view | `color.Blanched Almond→background`, `spacing.12→padding`, `radius.md→radius`, `font:Nunito` |
| ticket-queue | `color.Blanched Almond→background`, `spacing.12→padding`, `radius.md→radius`, `font:Nunito` |
| timeline-stream | `color.Blanched Almond→background`, `spacing.12→padding`, `radius.md→radius`, `font:Nunito` |
| toast | `color.Blanched Almond→background`, `spacing.12→padding`, `radius.md→radius`, `font:Nunito` |
| tooltip-guide | `color.Rose Quartz→surface`, `color.Dark Salmon→emphasis`, `color.Blanched Almond→background`, `spacing.12→padding`, `radius.md→radius`, `font:Nunito` |
| topbar | `color.Rose Quartz→surface`, `color.Dark Salmon→emphasis`, `color.Blanched Almond→background`, `spacing.12→padding`, `radius.md→radius`, `font:Nunito` |
| upgrade-banner | `color.Blanched Almond→background`, `spacing.12→padding`, `radius.md→radius`, `font:Nunito` |
| user-list | `color.Blanched Almond→background`, `spacing.12→padding`, `radius.md→radius`, `font:Nunito` |
| user-menu | `color.Rose Quartz→surface`, `color.Dark Salmon→emphasis`, `color.Blanched Almond→background`, `spacing.12→padding`, `radius.md→radius`, `font:Nunito` |
| variant-selector | `color.Rose Quartz→surface`, `color.Dark Salmon→emphasis`, `color.Blanched Almond→background`, `spacing.12→padding`, `radius.md→radius`, `font:Nunito` |
| wellness-score | `color.Blanched Almond→background`, `spacing.12→padding`, `radius.md→radius`, `font:Nunito` |
| wishlist-toggle | `color.Rose Quartz→surface`, `color.Dark Salmon→emphasis`, `color.Blanched Almond→background`, `spacing.12→padding`, `radius.md→radius`, `font:Nunito` |
| wizard-layout | `color.Rose Quartz→surface`, `color.Dark Salmon→emphasis`, `color.Blanched Almond→background`, `spacing.12→padding`, `radius.md→radius`, `font:Nunito` |

## 19. Contrast Audit

| Background | Foreground | Ratio | Level |
|------------|------------|-------|-------|
| Blanched Almond | Ink | 16.20:1 | AAA (pass) |
| Rose Quartz | Ink | 12.81:1 | AAA (pass) |
| Dark Salmon | Ink | 8.19:1 | AAA (pass) |
| Dark Salmon | Paper | 2.31:1 | fail (FAIL) |
| Dark Salmon | Blanched Almond | 1.98:1 | fail (FAIL) |
| Rose Quartz | Dark Salmon | 1.56:1 | fail (FAIL) |
| Rose Quartz | Paper | 1.47:1 | fail (FAIL) |
| Rose Quartz | Blanched Almond | 1.26:1 | fail (FAIL) |
| Blanched Almond | Paper | 1.17:1 | fail (FAIL) |

## 20. Pattern Catalog

### Layout Patterns

- **product grid**: —
- **product card**: —
- **product detail**: —
- **variant chip**: —
- **add-to-cart pill**: —
- **quantity stepper**: —
- **cart drawer**: —
- **cart line-item**: —
- **checkout form**: —
- **shipping step**: —
- **payment step**: —
- **order summary**: —
- **review card**: —
- **emoji reaction**: —
- **empty cart**: —
- **gentle toast**: —
- **soft dialog**: —
- **bottom sheet**: —
- **gift-message input**: —
- **subscription toggle**: —
- **workspace navigation**: app-shell, sidebar-nav, topbar, breadcrumb, tab-bar
- **dashboard cards**: stat-card, insight-card, activity-card, section-header
- **data tables**: data-table, column-header, filter-chip, row-actions, pagination, filter-toolbar

### Interaction Patterns

- **command palette**: —
- **forms**: text-field, select, checkbox, textarea, form-section, radio-group, form-actions
- **notifications**: toast, inline-alert, empty-state, banner
