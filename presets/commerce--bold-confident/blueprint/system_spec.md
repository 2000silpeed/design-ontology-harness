# Drop System Spec

## 1. Positioning

- **Brand**: Drop
- **Product**: 젊은 B2C commerce — bold-confident 톤 드롭 · 제품 그리드 · 제품 상세 · 장바구니 · 체크아웃, high-contrast saturated, impact typography, 한국어 1급
- **Audience**: 스트리트웨어/스니커 드롭을 기다리는 젊은 소비자 (Gen Z, 밀레니얼), 게이밍/e스포츠 머천다이즈를 구매하는 팬, bold beauty · 스포츠 굿즈 · 한정판 컬렉션을 탐색하는 모바일 쇼핑 사용자
- **Platforms**: web, mobile-web
- **Accessibility floor**: WCAG 2.2 AA

## 2. Identity Guardrails

- **Brand keywords**: commerce, ecommerce, shop, store, product-grid, product-detail, cart, checkout, drop, merchandise, streetwear, bold, energetic, high-contrast
- **Anti-keywords**: editorial-warm, magazine-serif, minimal, playful-pastel, corporate-conservative, dashboard-heavy, document-heavy
- **Tone of voice**: confident, energetic, direct, hype, street
- **Visual direction**: saturated primary hero, high-contrast headline, dense product grid, large product hero image, impact typography, purple accent callout, full-bleed drop banner, bold price tag, countdown timer chip
- **Interaction direction**: add-to-cart animation, quick-view modal, size selector chip, wishlist toggle heart, drop countdown timer, quantity stepper, cart drawer slide-in, checkout step progress, promo code input flash, hero scroll-snap banner

## 3. Design Principles

- **Commerce**: `commerce`를 시각적 선택과 인터랙션 선택의 기본 기준으로 삼습니다.
- **Ecommerce**: `ecommerce`를 시각적 선택과 인터랙션 선택의 기본 기준으로 삼습니다.
- **Shop**: `shop`를 시각적 선택과 인터랙션 선택의 기본 기준으로 삼습니다.
- **Store**: `store`를 시각적 선택과 인터랙션 선택의 기본 기준으로 삼습니다.

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
- **Body**: Wanted Sans
- **Korean**: Wanted Sans
- **Mono**: JetBrains Mono
- **Product type detected**: saas
- **Pairing source**: auto-scored
- **Line height**: tight
- **Type scale**: base 15px, ratio 1.25 (xs=12px, sm=13px, md=15px, lg=19px, xl=24px, 2xl=30px, 3xl=37px)
- **Strategy**:
  - 헤딩(geometric-sans) + 본문(humanist-sans) 조합
  - 한글 서체: Wanted Sans — 라틴과 x-height/weight 조화
  - 모노스페이스: JetBrains Mono — 코드/데이터 영역 전용
- **Heading note**: 스포카에서 만든 한글 산세리프. Source Sans Pro 기반. 깔끔한 데이터 UI에 적합.
- **Body note**: 원티드에서 공개한 한글 서체. 현대적이고 깔끔한 인상. 한글 자간이 좋음.
- **Korean rationale**: Wanted Sans — 원티드에서 공개. Pretendard보다 현대적이고 자신감 있는 인상. 헤딩에서 특히 좋음. bold weight에서 임팩트.
- **Heading tracking**: xl=-0.01em, 2xl=-0.02em, 3xl=-0.02em
- **Primary script**: korean
- **Hangul headline defaults**: Spoqa Han Sans Neo | line-height 1.2-1.3 | tracking -0.02em
- **Hangul body defaults**: Wanted Sans | line-height 1.5-1.6 | label line-height 1.4-1.5
- **Wrap defaults**: headline word-break=keep-all, headline text-wrap=balance, body word-break=keep-all
- **Scale guidance**: 기본 스케일을 사용할 수 있지만 한글 문장 기준으로 실제 wrap을 먼저 검증한다.
- **Hangul warning**: 장문 본문 — line-height 여유 부족
- **Hangul warning**: 감성적 브랜딩
- **Hangul warning**: 장문 본문 — Pretendard보다 line-height 여유가 적음
- **Loading**: Wanted Sans(preload), Spoqa Han Sans Neo(preload), JetBrains Mono(lazy) | display: swap

## 6. Color Reference

- **Source**: REFERENCE X Vol.1 - Color Reference (/Users/sungwoon/ai-projects/design-ontology-harness/docs/color-reference.md)
- **Selection mode**: manual
- **Preferred families**: Standard Reds, Cobalt Violet, Buttercream
- **Palette strategy**: temperature=warm, contrast=balanced, diversity=balanced, surface_style=grounded
- **Palette expansion**: supporting_color_count=10, combination_count=3, prefer_pairings=True
- **Palette roles**:
  - `primary` -> Crimson #BD2E4A / Standard Reds
  - `accent` -> Royal Purple #6C3BAA / Standard Violets
  - `surface_tint` -> Buttercream #F3E5AB / Pastel Yellows
- **Selected colors**:
  - Grenadine #DC4C46 / Pantone Trend Reds / 밝고 따뜻한 레드 오렌지 계열, 중채도 이상의 밝은 톤 / 활력, 열정, 관능, 현대적
  - Scarlet #FF2400 / Standard Reds / 강렬한 주황빛 레드 계열, 고채도와 고명도의 따뜻한 톤 / 활기, 생동감, 열정, 역동성, 주목성
  - Pure Red #FF0000 / Standard Reds / 순수 원색 레드 계열, 고채도와 중명도의 강렬한 톤 / 열정, 에너지, 주목성, 상징적, 강렬함
- **Palette candidates**:
  - signature-1 (Signature): primary=Grenadine, accent=Scarlet, surface_tint=Pure Red / Grenadine matches brand tone keywords.; Scarlet is inside preferred families.
- **Expanded supporting colors**:
  - Scarlet #FF2400 / Standard Reds / reference-color / Scarlet stays inside the preferred families.; Scarlet reinforces the brand mood signals.
  - Pure Red #FF0000 / Standard Reds / reference-color / Pure Red stays inside the preferred families.; Pure Red reinforces the brand mood signals.
  - Persimmon #EC5800 / Natural Oranges / reference-color / Persimmon reinforces the brand mood signals.
  - Pure Orange #FFA500 / Standard Oranges / reference-color / Pure Orange reinforces the brand mood signals.
  - Pairing #C4B8A2 #C4B8A2 / Derived Pairing / pairing-swatch / Pairing #C4B8A2 reinforces the brand mood signals.; Pairing #C4B8A2 comes from the seed pairing references.
  - Pairing #D39C7D #D39C7D / Derived Pairing / pairing-swatch / Pairing #D39C7D reinforces the brand mood signals.; Pairing #D39C7D comes from the seed pairing references.
  - Pairing #D5A48E #D5A48E / Derived Pairing / pairing-swatch / Pairing #D5A48E reinforces the brand mood signals.; Pairing #D5A48E comes from the seed pairing references.
  - Pairing #EAD9B7 #EAD9B7 / Derived Pairing / pairing-swatch / Pairing #EAD9B7 reinforces the brand mood signals.; Pairing #EAD9B7 comes from the seed pairing references.
- **Expanded semantic roles**:
  - `brand_primary` -> Crimson #BD2E4A / Standard Reds
  - `brand_accent` -> Royal Purple #6C3BAA / Standard Violets
  - `surface_tint` -> Buttercream #F3E5AB / Pastel Yellows
  - `canvas` -> Canvas White #F7F8FA / Generated Fallback
  - `surface` -> Paper #FFFFFF / Generated Fallback
  - `surface_muted` -> Surface Muted #EEF1F6 / Generated Fallback
  - `surface_elevated` -> Paper #FFFFFF / Generated Fallback
  - `border` -> Border Neutral #D6DDE6 / Generated Fallback
  - `border_strong` -> Pairing #C4B8A2 #C4B8A2 / Derived Pairing
  - `ink` -> Ink #111111 / Generated Fallback
- **Combination lists**:
  - Seed Core: primary=Crimson, accent=Royal Purple, surface_tint=Buttercream
  - Surface System: canvas=Canvas White, surface=Paper, surface_tint=Buttercream, border=Border Neutral, ink=Ink, ink_muted=Muted Ink
  - Support Spectrum: support=Scarlet, support=Pure Red, support=Persimmon, support=Pure Orange, support=Pairing #C4B8A2, support=Pairing #D39C7D
- **Notes**: Crimson #BD2E4A primary — saturated blood red, drop banner / add-to-cart / price tag / sale badge 전면 사용, premier-league #E90052 와 톤 명확히 차별화 (darker wine red), Royal Purple #6C3BAA accent — bold vivid purple, split-complement pop, countdown timer / drop label / wishlist heart / secondary CTA 강조, 기존 purple HEX (Cobalt Violet #804AA8, Iris Violet #5A4FCF) 와 겹침 없음, Buttercream #F3E5AB surface_tint — warm cream hero surface, saturated primaries 포용, bloom 의 cornsilk #FFF8DC 와 다른 더 yellow-leaning cream, light mode 가 기본 — 상품 사진 기반 commerce 관례, dark 옵션 제공 (깊은 neutral black + tuned Crimson/Purple 채도 낮춤), 기존 11종 프리셋 HEX 와 겹침 0 — Crimson/Royal Purple/Buttercream 조합, premier-league bold-confident 의 #E90052/#00FF85/#FFD700 팔레트 회피 — commerce 는 streetwear/drop 정체성으로 차별화
- **Application rule**: 레퍼런스 컬러는 semantic token으로 번역해서 사용하고, 접근성과 theme 호환성을 우선합니다.

## 7. Visual Reference Signals

- **Mode**: local-images
- **Coverage**: source 0 / image 0 / selected 0
- **Rule**: visual references are advisory signals for motif and layout direction; official KB/spec remain the structural source of truth.
- **Provenance**: `observed` = directly measured from local pixels, `inferred` = synthesized from image/query/brand signals, `unverified` = reliable visual evidence not yet available.
- **Query seeds**: nike streetwear drop commerce, supreme product grid, kith product detail bold, ssense checkout flow, musinsa mobile commerce, 29cm product detail bold
### Visual Direction

- **Density**: airy (confidence 0.94, provenance inferred) / editorial x2, landing x1, hero x6
- **Surface Style**: flat (confidence 0.41, provenance inferred) / minimal x2
- **Corner Style**: pill (confidence 0.43, provenance inferred) / pill x1
- **Typography Mood**: editorial (confidence 0.9, provenance inferred) / editorial x2, article x1, magazine x2
- **Color balance**: temperature=unknown, contrast=unknown, neutral_bias=unknown, provenance=unverified

### Layout Rhythm

- **Editorial feed**: confidence 0.94 / provenance inferred / editorial x2, article x1, feed x1, magazine x2
- **Narrative landing flow**: confidence 0.94 / provenance inferred / landing x1, hero x6
- **Data review surface**: confidence 0.92 / provenance inferred / grid x6, filter x1
- **Dashboard grid**: confidence 0.56 / provenance inferred / dashboard x2

### Image-derived Component Hints

- **Cards**: flat card planes를 기본으로 하고, 넓은 내부 여백과 강한 section breathing room. pill-like actions만 제한적으로 허용. / provenance inferred / surface=flat, density=airy, corner=pill
- **Navigation**: navigation은 정보 구조를 안정적으로 고정하고 시각적 장식보다 위치 신호를 우선한다. / provenance inferred / Editorial feed
- **Typography**: headline rhythm과 본문 리듬의 대비를 키우고, label/metadata는 조용하게 유지한다. / provenance inferred / typography_mood=editorial
- **Data Display**: 정보 밀도를 유지하되 thin dividers와 restrained accent로 hierarchy를 만든다. / provenance inferred / layout=dashboard-grid, density=airy

### Synthesis Notes

- layout는 Editorial feed 기준으로 정리
- surface language는 flat 성향 우선
- typography mood는 editorial 축 유지
- density는 airy 기준으로 primitive spacing 조정
- palette temperature는 unknown 쪽을 우선
- Avoid: warm editorial magazine hero
- Avoid: minimal saas landing
- Avoid: pastel playful feed
- Avoid: dense dashboard chrome

## 8. Component Strategy

- **Product primitives**: product card, product grid, product detail, product gallery, image thumbnail, variant selector, size selector, color swatch selector, add-to-cart button, quick-view modal, wishlist toggle, drop banner, countdown timer, price tag, original price strikethrough, discount badge, cart drawer, cart item, cart summary, checkout step, address form, payment form, promo code input, order summary, empty cart state, search bar, filter sidebar, sort dropdown, pagination, breadcrumb, category pill, hero banner, site header, site footer
- **Required families**: button, data-display, editorial, feedback, input, marketing, navigation, commerce, document, overlay, social
- **Visual-reference archetypes**:

- **Data review table** (data-display / 0.94): data-table, column-header, row-actions, filter-toolbar, pagination
- **Editorial content block** (editorial / 0.94): content-card, featured-story-card, section-header, content-meta, byline-row
- **Marketing hero stack** (marketing / 0.94): hero-section, hero-headline, hero-visual, cta-button-group, trust-strip
- **Dashboard insight module** (data-display / 0.71): stat-card, insight-card, chart-panel, section-header, filter-chip

- **button**: primary-button, secondary-button, ghost-button, icon-button, cta-button, link-button, add-to-cart-button, wishlist-toggle
- **data-display**: tag, pricing-card, feature-comparison, data-table, column-header, row-actions, search-results, kanban-board / visual signals: Data review table (0.94), Dashboard insight module (0.71)
- **editorial**: editor-canvas, editor-toolbar, inline-format-menu, slash-command-menu, block-controls, content-card, featured-story-card, content-meta / visual signals: Editorial content block (0.94)
- **feedback**: inline-alert, empty-state, toast, discount-badge, checkout-step-progress, empty-cart-state, status-badge, upgrade-banner
- **input**: text-field, search-field, segmented-control, variant-selector, size-selector, color-swatch-selector, filter-sidebar, sort-dropdown
- **marketing**: hero-container, hero-eyebrow, hero-headline, hero-subheadline, hero-visual, hero-trust-strip, site-footer, footer-column / visual signals: Marketing hero stack (0.94)
- **navigation**: mobile-topbar, mobile-tab-bar, back-button, section-tabs, category-pill, wizard-layout, pagination, app-shell
- **commerce**: product-grid, product-card, product-detail, product-gallery, product-hero-image, image-thumbnail, price-tag, original-price-strikethrough
- **document**: callout, admonition-block, api-reference-table, parameter-table
- **overlay**: bottom-sheet, modal-dialog, quick-view-modal, confirm-dialog, tooltip-guide, autocomplete, chart-tooltip, mention-popup
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

이 문서는 **Drop System**의 디자인 시스템 사양입니다.

### 시작하기

1. **토큰 적용**: Drop-in CSS(아래 섹션 16)의 CSS 변수를 프로젝트에 복사합니다.
2. **컬러 세팅**: Color Reference(섹션 6)의 semantic role을 기준으로 surface/text/border를 잡습니다.
3. **타이포 세팅**: Token Strategy(섹션 5)의 font family와 type scale을 적용합니다.
4. **시각 방향 확인**: Visual Reference Signals(섹션 7)에서 density/surface/layout cue를 먼저 확인합니다.
5. **컴포넌트 구현**: Component Strategy(섹션 8)의 family 순서대로 하나씩 빌드합니다.

### 우선순위

핵심 primitive: **product card, product grid, product detail, product gallery, image thumbnail**

이 primitive를 지원하는 컴포넌트부터 구현하고, 나머지는 필요에 따라 확장합니다.

## 15. DO / DON'T

### DO

- **Commerce**: commerce와 충돌하는 컴포넌트 변형은 만들지 않기
- **Ecommerce**: ecommerce와 충돌하는 컴포넌트 변형은 만들지 않기
- **Shop**: shop와 충돌하는 컴포넌트 변형은 만들지 않기
- **Store**: store와 충돌하는 컴포넌트 변형은 만들지 않기
- 모든 시각적 선택에서 **commerce, ecommerce, shop** 기준을 적용
- semantic token을 통해 컬러를 적용 (하드코딩 금지)
- 접근성 기준을 모든 text/surface 조합에서 먼저 검증
- 컴포넌트 변형 추가 전 기존 variant로 해결 가능한지 먼저 확인
- 아이콘은 SVG 컴포넌트 또는 Lucide/Heroicons/Phosphor/Tabler 등 라이브러리로 구현
- component_specs.md의 anatomy/states/token binding을 그대로 따라 완전히 구현

### DON'T

- **editorial-warm** 방향의 디자인 결정을 하지 않음
- **magazine-serif** 방향의 디자인 결정을 하지 않음
- **minimal** 방향의 디자인 결정을 하지 않음
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
  --font-body: 'Wanted Sans', sans-serif;
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
  --color-primary: #BD2E4A;
  --color-accent: #6C3BAA;
  --color-surface-tint: #F3E5AB;

  /* --- Semantic roles (expanded) --- */
  --color-brand-primary: #BD2E4A;
  --color-brand-accent: #6C3BAA;
  --color-surface-tint: #F3E5AB;
  --color-canvas: #F7F8FA;
  --color-surface: #FFFFFF;
  --color-surface-muted: #EEF1F6;
  --color-surface-elevated: #FFFFFF;
  --color-border: #D6DDE6;
  --color-border-strong: #C4B8A2;
  --color-ink: #111111;
  --color-ink-muted: #4B5563;
  --color-ink-subtle: #6B7280;
  --color-ink-inverse: #FFFFFF;
  --color-primary-support: #FF2400;
  --color-accent-support: #6C3BAA;
  --color-info: #6C3BAA;
  --color-success: #4A7C59;
  --color-warning: #EC5800;
  --color-danger: #BD2E4A;
  --color-link: #BD2E4A;
  --color-link-hover: #9C263D;

  /* --- Button — primary --- */
  --color-button-primary-surface-default: #BD2E4A;
  --color-button-primary-surface-hover: #A42840;
  --color-button-primary-surface-active: #94243A;
  --color-button-primary-surface-disabled: #E0A7B4;
  --color-button-primary-text-default: #FFFFFF;
  --color-button-primary-text-disabled: #FBFCFC;
  --color-button-primary-border-default: #BD2E4A;
  --color-button-primary-focus-ring: #BD2E4A;

  /* --- Button — secondary --- */
  --color-button-secondary-surface-default: #FFFFFF;
  --color-button-secondary-surface-hover: #F1F1F1;
  --color-button-secondary-surface-active: #E7E7E7;
  --color-button-secondary-surface-disabled: #F7F8FA;
  --color-button-secondary-text-default: #111111;
  --color-button-secondary-text-disabled: #909091;
  --color-button-secondary-border-default: #BDC8D7;
  --color-button-secondary-border-hover: #A3B3C7;
  --color-button-secondary-focus-ring: #BD2E4A;

  /* --- Button — ghost --- */
  --color-button-ghost-surface-default: transparent;
  --color-button-ghost-surface-hover: #F3F3F3;
  --color-button-ghost-surface-active: #EAEAEA;
  --color-button-ghost-surface-disabled: transparent;
  --color-button-ghost-text-default: #4B5563;
  --color-button-ghost-text-hover: #111111;
  --color-button-ghost-text-disabled: #AAAFB6;
  --color-button-ghost-border-default: transparent;
  --color-button-ghost-focus-ring: #BD2E4A;

  /* --- Button — danger --- */
  --color-button-danger-surface-default: #BD2E4A;
  --color-button-danger-surface-hover: #A42840;
  --color-button-danger-surface-active: #94243A;
  --color-button-danger-text-default: #FFFFFF;
  --color-button-danger-border-default: #BD2E4A;
  --color-button-danger-focus-ring: #BD2E4A;

  /* --- Input --- */
  --color-input-surface-default: #FFFFFF;
  --color-input-surface-filled: #FFFFFF;
  --color-input-surface-disabled: #F7F8FA;
  --color-input-text-default: #111111;
  --color-input-text-placeholder: #90969F;
  --color-input-text-disabled: #AAAFB6;
  --color-input-border-default: #D6DDE6;
  --color-input-border-hover: #B6C3D3;
  --color-input-border-focus: #BD2E4A;
  --color-input-border-error: #BD2E4A;
  --color-input-border-disabled: #E6EAF0;

  /* --- Card --- */
  --color-card-surface-default: #FFFFFF;
  --color-card-surface-hover: #FAFAFA;
  --color-card-surface-muted: #F7F8FA;
  --color-card-border-default: #D6DDE6;
  --color-card-border-hover: #B6C3D3;
  --color-card-border-focus: #BD2E4A;

  /* --- Nav link --- */
  --color-nav-link-text-default: #4B5563;
  --color-nav-link-text-hover: #111111;
  --color-nav-link-text-active: #BD2E4A;
  --color-nav-link-surface-hover: #F5F5F5;
  --color-nav-link-indicator: #6C3BAA;

  /* --- Link --- */
  --color-link-text-default: #BD2E4A;
  --color-link-text-hover: #94243A;
  --color-link-text-visited: #943E4F;

  /* --- Feedback — info --- */
  --color-feedback-info-surface: #EDE7F5;
  --color-feedback-info-text: #6C3BAA;
  --color-feedback-info-border: #9674C2;
  --color-feedback-info-icon: #6C3BAA;

  /* --- Feedback — success --- */
  --color-feedback-success-surface: #E9EFEB;
  --color-feedback-success-text: #4A7C59;
  --color-feedback-success-border: #7EA189;
  --color-feedback-success-icon: #4A7C59;

  /* --- Feedback — warning --- */
  --color-feedback-warning-surface: #FDEBE0;
  --color-feedback-warning-text: #EC5800;
  --color-feedback-warning-border: #EF884B;
  --color-feedback-warning-icon: #EC5800;

  /* --- Feedback — danger --- */
  --color-feedback-danger-surface: #F7E6E9;
  --color-feedback-danger-text: #BD2E4A;
  --color-feedback-danger-border: #CE6B7F;
  --color-feedback-danger-icon: #BD2E4A;

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
| activity-card | `color.Buttercream→background`, `spacing.12→padding`, `radius.md→radius`, `font:Wanted Sans` |
| add-to-cart-button | `color.Crimson→surface`, `color.Royal Purple→emphasis`, `color.Buttercream→background`, `spacing.12→padding`, `radius.md→radius`, `font:Wanted Sans` |
| address-form | `color.Crimson→surface`, `color.Royal Purple→emphasis`, `color.Buttercream→background`, `spacing.12→padding`, `radius.md→radius`, `font:Wanted Sans` |
| admonition-block | `color.Buttercream→background`, `spacing.12→padding`, `radius.md→radius`, `font:Wanted Sans` |
| api-reference-table | `color.Buttercream→background`, `spacing.12→padding`, `radius.md→radius`, `font:Wanted Sans` |
| app-shell | `color.Crimson→surface`, `color.Royal Purple→emphasis`, `color.Buttercream→background`, `spacing.12→padding`, `radius.md→radius`, `font:Wanted Sans` |
| autocomplete | `color.Crimson→surface`, `color.Royal Purple→emphasis`, `color.Buttercream→background`, `spacing.12→padding`, `radius.md→radius`, `font:Wanted Sans` |
| avatar | `color.Buttercream→background`, `spacing.12→padding`, `radius.md→radius`, `font:Wanted Sans` |
| avatar-cluster | `color.Buttercream→background`, `spacing.12→padding`, `radius.md→radius`, `font:Wanted Sans` |
| back-button | `color.Crimson→surface`, `color.Royal Purple→emphasis`, `color.Buttercream→background`, `spacing.12→padding`, `radius.md→radius`, `font:Wanted Sans` |
| banner | `color.Buttercream→background`, `spacing.12→padding`, `radius.md→radius`, `font:Wanted Sans` |
| block-controls | `color.Buttercream→background`, `spacing.12→padding`, `radius.md→radius`, `font:Wanted Sans` |
| bottom-sheet | `color.Crimson→surface`, `color.Royal Purple→emphasis`, `color.Buttercream→background`, `spacing.12→padding`, `radius.md→radius`, `font:Wanted Sans` |
| breadcrumb | `color.Crimson→surface`, `color.Royal Purple→emphasis`, `color.Buttercream→background`, `spacing.12→padding`, `radius.md→radius`, `font:Wanted Sans` |
| byline-row | `color.Buttercream→background`, `spacing.12→padding`, `radius.md→radius`, `font:Wanted Sans` |
| callout | `color.Buttercream→background`, `spacing.12→padding`, `radius.md→radius`, `font:Wanted Sans` |
| cart-drawer | `color.Buttercream→background`, `spacing.12→padding`, `radius.md→radius`, `font:Wanted Sans` |
| cart-item | `color.Buttercream→background`, `spacing.12→padding`, `radius.md→radius`, `font:Wanted Sans` |
| cart-summary | `color.Buttercream→background`, `spacing.12→padding`, `radius.md→radius`, `font:Wanted Sans` |
| category-pill | `color.Crimson→surface`, `color.Royal Purple→emphasis`, `color.Buttercream→background`, `spacing.12→padding`, `radius.md→radius`, `font:Wanted Sans` |
| chart-container | `color.Buttercream→background`, `spacing.12→padding`, `radius.md→radius`, `font:Wanted Sans` |
| chart-legend | `color.Buttercream→background`, `spacing.12→padding`, `radius.md→radius`, `font:Wanted Sans` |
| chart-panel | `color.Buttercream→background`, `spacing.12→padding`, `radius.md→radius`, `font:Wanted Sans` |
| chart-tooltip | `color.Crimson→surface`, `color.Royal Purple→emphasis`, `color.Buttercream→background`, `spacing.12→padding`, `radius.md→radius`, `font:Wanted Sans` |
| chat-input | `color.Crimson→surface`, `color.Royal Purple→emphasis`, `color.Buttercream→background`, `spacing.12→padding`, `radius.md→radius`, `font:Wanted Sans` |
| chat-message | `color.Buttercream→background`, `spacing.12→padding`, `radius.md→radius`, `font:Wanted Sans` |
| chat-thread | `color.Buttercream→background`, `spacing.12→padding`, `radius.md→radius`, `font:Wanted Sans` |
| checkbox | `color.Crimson→surface`, `color.Royal Purple→emphasis`, `color.Buttercream→background`, `spacing.12→padding`, `radius.md→radius`, `font:Wanted Sans` |
| checkout-step | `color.Buttercream→background`, `spacing.12→padding`, `radius.md→radius`, `font:Wanted Sans` |
| checkout-step-progress | `color.Buttercream→background`, `spacing.12→padding`, `radius.md→radius`, `font:Wanted Sans` |
| chip | `color.Crimson→surface`, `color.Royal Purple→emphasis`, `color.Buttercream→background`, `spacing.12→padding`, `radius.md→radius`, `font:Wanted Sans` |
| color-swatch-selector | `color.Crimson→surface`, `color.Royal Purple→emphasis`, `color.Buttercream→background`, `spacing.12→padding`, `radius.md→radius`, `font:Wanted Sans` |
| column-header | `color.Buttercream→background`, `spacing.12→padding`, `radius.md→radius`, `font:Wanted Sans` |
| comment-input | `color.Crimson→surface`, `color.Royal Purple→emphasis`, `color.Buttercream→background`, `spacing.12→padding`, `radius.md→radius`, `font:Wanted Sans` |
| comment-thread | `color.Buttercream→background`, `spacing.12→padding`, `radius.md→radius`, `font:Wanted Sans` |
| confirm-dialog | `color.Crimson→surface`, `color.Royal Purple→emphasis`, `color.Buttercream→background`, `spacing.12→padding`, `radius.md→radius`, `font:Wanted Sans` |
| content-card | `color.Buttercream→background`, `spacing.12→padding`, `radius.md→radius`, `font:Wanted Sans` |
| content-meta | `color.Buttercream→background`, `spacing.12→padding`, `radius.md→radius`, `font:Wanted Sans` |
| countdown-timer | `color.Buttercream→background`, `spacing.12→padding`, `radius.md→radius`, `font:Wanted Sans` |
| cross-sell-grid | `color.Buttercream→background`, `spacing.12→padding`, `radius.md→radius`, `font:Wanted Sans` |
| cta-button | `color.Crimson→surface`, `color.Royal Purple→emphasis`, `color.Buttercream→background`, `spacing.12→padding`, `radius.md→radius`, `font:Wanted Sans` |
| cta-button-group | `color.Buttercream→background`, `spacing.12→padding`, `radius.md→radius`, `font:Wanted Sans` |
| data-table | `color.Buttercream→background`, `spacing.12→padding`, `radius.md→radius`, `font:Wanted Sans` |
| discount-badge | `color.Buttercream→background`, `spacing.12→padding`, `radius.md→radius`, `font:Wanted Sans` |
| drop-banner | `color.Buttercream→background`, `spacing.12→padding`, `radius.md→radius`, `font:Wanted Sans` |
| editor-canvas | `color.Buttercream→background`, `spacing.12→padding`, `radius.md→radius`, `font:Wanted Sans` |
| editor-toolbar | `color.Buttercream→background`, `spacing.12→padding`, `radius.md→radius`, `font:Wanted Sans` |
| empty-cart-state | `color.Buttercream→background`, `spacing.12→padding`, `radius.md→radius`, `font:Wanted Sans` |
| empty-feed-illustration | `color.Buttercream→background`, `spacing.12→padding`, `radius.md→radius`, `font:Wanted Sans` |
| empty-state | `color.Buttercream→background`, `spacing.12→padding`, `radius.md→radius`, `font:Wanted Sans` |
| feature-comparison | `color.Buttercream→background`, `spacing.12→padding`, `radius.md→radius`, `font:Wanted Sans` |
| featured-category-tile | `color.Buttercream→background`, `spacing.12→padding`, `radius.md→radius`, `font:Wanted Sans` |
| featured-story-card | `color.Buttercream→background`, `spacing.12→padding`, `radius.md→radius`, `font:Wanted Sans` |
| feed-item | `color.Buttercream→background`, `spacing.12→padding`, `radius.md→radius`, `font:Wanted Sans` |
| filter-chip | `color.Crimson→surface`, `color.Royal Purple→emphasis`, `color.Buttercream→background`, `spacing.12→padding`, `radius.md→radius`, `font:Wanted Sans` |
| filter-panel | `color.Crimson→surface`, `color.Royal Purple→emphasis`, `color.Buttercream→background`, `spacing.12→padding`, `radius.md→radius`, `font:Wanted Sans` |
| filter-sidebar | `color.Crimson→surface`, `color.Royal Purple→emphasis`, `color.Buttercream→background`, `spacing.12→padding`, `radius.md→radius`, `font:Wanted Sans` |
| filter-toolbar | `color.Buttercream→background`, `spacing.12→padding`, `radius.md→radius`, `font:Wanted Sans` |
| follow-button | `color.Crimson→surface`, `color.Royal Purple→emphasis`, `color.Buttercream→background`, `spacing.12→padding`, `radius.md→radius`, `font:Wanted Sans` |
| footer-column | `color.Buttercream→background`, `spacing.12→padding`, `radius.md→radius`, `font:Wanted Sans` |
| footer-legal | `color.Buttercream→background`, `spacing.12→padding`, `radius.md→radius`, `font:Wanted Sans` |
| footer-link | `color.Buttercream→background`, `spacing.12→padding`, `radius.md→radius`, `font:Wanted Sans` |
| footer-social | `color.Buttercream→background`, `spacing.12→padding`, `radius.md→radius`, `font:Wanted Sans` |
| form-actions | `color.Crimson→surface`, `color.Royal Purple→emphasis`, `color.Buttercream→background`, `spacing.12→padding`, `radius.md→radius`, `font:Wanted Sans` |
| form-section | `color.Crimson→surface`, `color.Royal Purple→emphasis`, `color.Buttercream→background`, `spacing.12→padding`, `radius.md→radius`, `font:Wanted Sans` |
| gentle-toast | `color.Buttercream→background`, `spacing.12→padding`, `radius.md→radius`, `font:Wanted Sans` |
| ghost-button | `color.Crimson→surface`, `color.Royal Purple→emphasis`, `color.Buttercream→background`, `spacing.12→padding`, `radius.md→radius`, `font:Wanted Sans` |
| hero-banner | `color.Buttercream→background`, `spacing.12→padding`, `radius.md→radius`, `font:Wanted Sans` |
| hero-container | `color.Buttercream→background`, `spacing.12→padding`, `radius.md→radius`, `font:Wanted Sans` |
| hero-cta-group | `color.Crimson→surface`, `color.Royal Purple→emphasis`, `color.Buttercream→background`, `spacing.12→padding`, `radius.md→radius`, `font:Wanted Sans` |
| hero-eyebrow | `color.Buttercream→background`, `spacing.12→padding`, `radius.md→radius`, `font:Wanted Sans` |
| hero-headline | `color.Buttercream→background`, `spacing.12→padding`, `radius.md→radius`, `font:Wanted Sans` |
| hero-section | `color.Buttercream→background`, `spacing.12→padding`, `radius.md→radius`, `font:Wanted Sans` |
| hero-subheadline | `color.Buttercream→background`, `spacing.12→padding`, `radius.md→radius`, `font:Wanted Sans` |
| hero-trust-strip | `color.Buttercream→background`, `spacing.12→padding`, `radius.md→radius`, `font:Wanted Sans` |
| hero-visual | `color.Buttercream→background`, `spacing.12→padding`, `radius.md→radius`, `font:Wanted Sans` |
| icon-button | `color.Crimson→surface`, `color.Royal Purple→emphasis`, `color.Buttercream→background`, `spacing.12→padding`, `radius.md→radius`, `font:Wanted Sans` |
| image-thumbnail | `color.Buttercream→background`, `spacing.12→padding`, `radius.md→radius`, `font:Wanted Sans` |
| inline-alert | `color.Buttercream→background`, `spacing.12→padding`, `radius.md→radius`, `font:Wanted Sans` |
| inline-format-menu | `color.Buttercream→background`, `spacing.12→padding`, `radius.md→radius`, `font:Wanted Sans` |
| insight-card | `color.Buttercream→background`, `spacing.12→padding`, `radius.md→radius`, `font:Wanted Sans` |
| kanban-board | `color.Buttercream→background`, `spacing.12→padding`, `radius.md→radius`, `font:Wanted Sans` |
| kanban-card | `color.Buttercream→background`, `spacing.12→padding`, `radius.md→radius`, `font:Wanted Sans` |
| kanban-column | `color.Buttercream→background`, `spacing.12→padding`, `radius.md→radius`, `font:Wanted Sans` |
| link-button | `color.Crimson→surface`, `color.Royal Purple→emphasis`, `color.Buttercream→background`, `spacing.12→padding`, `radius.md→radius`, `font:Wanted Sans` |
| lookbook-hero | `color.Buttercream→background`, `spacing.12→padding`, `radius.md→radius`, `font:Wanted Sans` |
| mention-popup | `color.Crimson→surface`, `color.Royal Purple→emphasis`, `color.Buttercream→background`, `spacing.12→padding`, `radius.md→radius`, `font:Wanted Sans` |
| mobile-menu-trigger | `color.Crimson→surface`, `color.Royal Purple→emphasis`, `color.Buttercream→background`, `spacing.12→padding`, `radius.md→radius`, `font:Wanted Sans` |
| mobile-tab-bar | `color.Crimson→surface`, `color.Royal Purple→emphasis`, `color.Buttercream→background`, `spacing.12→padding`, `radius.md→radius`, `font:Wanted Sans` |
| mobile-topbar | `color.Crimson→surface`, `color.Royal Purple→emphasis`, `color.Buttercream→background`, `spacing.12→padding`, `radius.md→radius`, `font:Wanted Sans` |
| modal-dialog | `color.Crimson→surface`, `color.Royal Purple→emphasis`, `color.Buttercream→background`, `spacing.12→padding`, `radius.md→radius`, `font:Wanted Sans` |
| order-summary | `color.Buttercream→background`, `spacing.12→padding`, `radius.md→radius`, `font:Wanted Sans` |
| original-price-strikethrough | `color.Buttercream→background`, `spacing.12→padding`, `radius.md→radius`, `font:Wanted Sans` |
| pagination | `color.Crimson→surface`, `color.Royal Purple→emphasis`, `color.Buttercream→background`, `spacing.12→padding`, `radius.md→radius`, `font:Wanted Sans` |
| parameter-table | `color.Buttercream→background`, `spacing.12→padding`, `radius.md→radius`, `font:Wanted Sans` |
| payment-form | `color.Crimson→surface`, `color.Royal Purple→emphasis`, `color.Buttercream→background`, `spacing.12→padding`, `radius.md→radius`, `font:Wanted Sans` |
| post-card | `color.Buttercream→background`, `spacing.12→padding`, `radius.md→radius`, `font:Wanted Sans` |
| price-tag | `color.Buttercream→background`, `spacing.12→padding`, `radius.md→radius`, `font:Wanted Sans` |
| pricing-card | `color.Buttercream→background`, `spacing.12→padding`, `radius.md→radius`, `font:Wanted Sans` |
| primary-button | `color.Crimson→surface`, `color.Royal Purple→emphasis`, `color.Buttercream→background`, `spacing.12→padding`, `radius.md→radius`, `font:Wanted Sans` |
| product-card | `color.Buttercream→background`, `spacing.12→padding`, `radius.md→radius`, `font:Wanted Sans` |
| product-detail | `color.Buttercream→background`, `spacing.12→padding`, `radius.md→radius`, `font:Wanted Sans` |
| product-gallery | `color.Buttercream→background`, `spacing.12→padding`, `radius.md→radius`, `font:Wanted Sans` |
| product-grid | `color.Buttercream→background`, `spacing.12→padding`, `radius.md→radius`, `font:Wanted Sans` |
| product-hero-image | `color.Buttercream→background`, `spacing.12→padding`, `radius.md→radius`, `font:Wanted Sans` |
| profile-card | `color.Buttercream→background`, `spacing.12→padding`, `radius.md→radius`, `font:Wanted Sans` |
| promo-code-input | `color.Crimson→surface`, `color.Royal Purple→emphasis`, `color.Buttercream→background`, `spacing.12→padding`, `radius.md→radius`, `font:Wanted Sans` |
| quantity-stepper | `color.Crimson→surface`, `color.Royal Purple→emphasis`, `color.Buttercream→background`, `spacing.12→padding`, `radius.md→radius`, `font:Wanted Sans` |
| quick-view-modal | `color.Crimson→surface`, `color.Royal Purple→emphasis`, `color.Buttercream→background`, `spacing.12→padding`, `radius.md→radius`, `font:Wanted Sans` |
| radio-group | `color.Crimson→surface`, `color.Royal Purple→emphasis`, `color.Buttercream→background`, `spacing.12→padding`, `radius.md→radius`, `font:Wanted Sans` |
| reaction-bar | `color.Buttercream→background`, `spacing.12→padding`, `radius.md→radius`, `font:Wanted Sans` |
| reply-composer | `color.Crimson→surface`, `color.Royal Purple→emphasis`, `color.Buttercream→background`, `spacing.12→padding`, `radius.md→radius`, `font:Wanted Sans` |
| row-actions | `color.Buttercream→background`, `spacing.12→padding`, `radius.md→radius`, `font:Wanted Sans` |
| search-field | `color.Crimson→surface`, `color.Royal Purple→emphasis`, `color.Buttercream→background`, `spacing.12→padding`, `radius.md→radius`, `font:Wanted Sans` |
| search-results | `color.Buttercream→background`, `spacing.12→padding`, `radius.md→radius`, `font:Wanted Sans` |
| secondary-button | `color.Crimson→surface`, `color.Royal Purple→emphasis`, `color.Buttercream→background`, `spacing.12→padding`, `radius.md→radius`, `font:Wanted Sans` |
| section-header | `color.Buttercream→background`, `spacing.12→padding`, `radius.md→radius`, `font:Wanted Sans` |
| section-tabs | `color.Crimson→surface`, `color.Royal Purple→emphasis`, `color.Buttercream→background`, `spacing.12→padding`, `radius.md→radius`, `font:Wanted Sans` |
| segmented-control | `color.Crimson→surface`, `color.Royal Purple→emphasis`, `color.Buttercream→background`, `spacing.12→padding`, `radius.md→radius`, `font:Wanted Sans` |
| select | `color.Crimson→surface`, `color.Royal Purple→emphasis`, `color.Buttercream→background`, `spacing.12→padding`, `radius.md→radius`, `font:Wanted Sans` |
| share-sheet | `color.Crimson→surface`, `color.Royal Purple→emphasis`, `color.Buttercream→background`, `spacing.12→padding`, `radius.md→radius`, `font:Wanted Sans` |
| sidebar-nav | `color.Crimson→surface`, `color.Royal Purple→emphasis`, `color.Buttercream→background`, `spacing.12→padding`, `radius.md→radius`, `font:Wanted Sans` |
| site-footer | `color.Buttercream→background`, `spacing.12→padding`, `radius.md→radius`, `font:Wanted Sans` |
| site-header | `color.Buttercream→background`, `spacing.12→padding`, `radius.md→radius`, `font:Wanted Sans` |
| site-logo | `color.Buttercream→background`, `spacing.12→padding`, `radius.md→radius`, `font:Wanted Sans` |
| site-nav | `color.Buttercream→background`, `spacing.12→padding`, `radius.md→radius`, `font:Wanted Sans` |
| site-nav-cta | `color.Crimson→surface`, `color.Royal Purple→emphasis`, `color.Buttercream→background`, `spacing.12→padding`, `radius.md→radius`, `font:Wanted Sans` |
| size-selector | `color.Crimson→surface`, `color.Royal Purple→emphasis`, `color.Buttercream→background`, `spacing.12→padding`, `radius.md→radius`, `font:Wanted Sans` |
| slash-command-menu | `color.Buttercream→background`, `spacing.12→padding`, `radius.md→radius`, `font:Wanted Sans` |
| soft-dialog | `color.Crimson→surface`, `color.Royal Purple→emphasis`, `color.Buttercream→background`, `spacing.12→padding`, `radius.md→radius`, `font:Wanted Sans` |
| sort-dropdown | `color.Crimson→surface`, `color.Royal Purple→emphasis`, `color.Buttercream→background`, `spacing.12→padding`, `radius.md→radius`, `font:Wanted Sans` |
| stat-card | `color.Buttercream→background`, `spacing.12→padding`, `radius.md→radius`, `font:Wanted Sans` |
| status-badge | `color.Buttercream→background`, `spacing.12→padding`, `radius.md→radius`, `font:Wanted Sans` |
| step-progress | `color.Buttercream→background`, `spacing.12→padding`, `radius.md→radius`, `font:Wanted Sans` |
| tab-bar | `color.Crimson→surface`, `color.Royal Purple→emphasis`, `color.Buttercream→background`, `spacing.12→padding`, `radius.md→radius`, `font:Wanted Sans` |
| tag | `color.Buttercream→background`, `spacing.12→padding`, `radius.md→radius`, `font:Wanted Sans` |
| tag-pill | `color.Buttercream→background`, `spacing.12→padding`, `radius.md→radius`, `font:Wanted Sans` |
| text-field | `color.Crimson→surface`, `color.Royal Purple→emphasis`, `color.Buttercream→background`, `spacing.12→padding`, `radius.md→radius`, `font:Wanted Sans` |
| textarea | `color.Crimson→surface`, `color.Royal Purple→emphasis`, `color.Buttercream→background`, `spacing.12→padding`, `radius.md→radius`, `font:Wanted Sans` |
| thread-view | `color.Buttercream→background`, `spacing.12→padding`, `radius.md→radius`, `font:Wanted Sans` |
| timeline-stream | `color.Buttercream→background`, `spacing.12→padding`, `radius.md→radius`, `font:Wanted Sans` |
| toast | `color.Buttercream→background`, `spacing.12→padding`, `radius.md→radius`, `font:Wanted Sans` |
| tooltip-guide | `color.Crimson→surface`, `color.Royal Purple→emphasis`, `color.Buttercream→background`, `spacing.12→padding`, `radius.md→radius`, `font:Wanted Sans` |
| topbar | `color.Crimson→surface`, `color.Royal Purple→emphasis`, `color.Buttercream→background`, `spacing.12→padding`, `radius.md→radius`, `font:Wanted Sans` |
| trust-strip | `color.Buttercream→background`, `spacing.12→padding`, `radius.md→radius`, `font:Wanted Sans` |
| upgrade-banner | `color.Buttercream→background`, `spacing.12→padding`, `radius.md→radius`, `font:Wanted Sans` |
| user-menu | `color.Crimson→surface`, `color.Royal Purple→emphasis`, `color.Buttercream→background`, `spacing.12→padding`, `radius.md→radius`, `font:Wanted Sans` |
| variant-selector | `color.Crimson→surface`, `color.Royal Purple→emphasis`, `color.Buttercream→background`, `spacing.12→padding`, `radius.md→radius`, `font:Wanted Sans` |
| version-switcher | `color.Crimson→surface`, `color.Royal Purple→emphasis`, `color.Buttercream→background`, `spacing.12→padding`, `radius.md→radius`, `font:Wanted Sans` |
| wishlist-toggle | `color.Crimson→surface`, `color.Royal Purple→emphasis`, `color.Buttercream→background`, `spacing.12→padding`, `radius.md→radius`, `font:Wanted Sans` |
| wizard-layout | `color.Crimson→surface`, `color.Royal Purple→emphasis`, `color.Buttercream→background`, `spacing.12→padding`, `radius.md→radius`, `font:Wanted Sans` |

## 19. Contrast Audit

| Background | Foreground | Ratio | Level |
|------------|------------|-------|-------|
| Buttercream | Ink | 14.93:1 | AAA (pass) |
| Royal Purple | Paper | 7.38:1 | AAA (pass) |
| Royal Purple | Buttercream | 5.84:1 | AA (pass) |
| Crimson | Paper | 5.75:1 | AA (pass) |
| Crimson | Buttercream | 4.55:1 | AA (pass) |
| Crimson | Ink | 3.29:1 | AA-large (large-only) |
| Royal Purple | Ink | 2.56:1 | fail (FAIL) |
| Crimson | Royal Purple | 1.28:1 | fail (FAIL) |
| Buttercream | Paper | 1.26:1 | fail (FAIL) |

## 20. Pattern Catalog

### Layout Patterns

- **product card**: —
- **product grid**: —
- **product detail**: —
- **product gallery**: —
- **image thumbnail**: —
- **variant selector**: —
- **size selector**: —
- **color swatch selector**: —
- **add-to-cart button**: —
- **quick-view modal**: —
- **wishlist toggle**: —
- **drop banner**: —
- **countdown timer**: —
- **price tag**: —
- **original price strikethrough**: —
- **discount badge**: —
- **cart drawer**: —
- **cart item**: —
- **cart summary**: —
- **checkout step**: —
- **address form**: —
- **payment form**: —
- **promo code input**: —
- **order summary**: —
- **empty cart state**: —
- **sort dropdown**: —
- **pagination**: —
- **breadcrumb**: —
- **category pill**: —
- **hero banner**: —
- **site header**: site-header, site-logo, site-nav, site-nav-cta, mobile-menu-trigger
- **site footer**: site-footer, footer-column, footer-link, footer-legal, footer-social
- **workspace navigation**: app-shell, sidebar-nav, topbar, breadcrumb, tab-bar
- **dashboard cards**: stat-card, insight-card, activity-card, section-header, chart-panel
- **data tables**: data-table, column-header, filter-chip, row-actions, pagination, filter-toolbar

### Interaction Patterns

- **search bar**: —
- **filter sidebar**: —
- **command palette**: —
- **forms**: text-field, select, checkbox, textarea, form-section, radio-group, form-actions
- **notifications**: toast, inline-alert, empty-state, banner
