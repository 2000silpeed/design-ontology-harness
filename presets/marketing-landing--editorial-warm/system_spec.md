# Loom System Spec

## 1. Positioning

- **Brand**: Loom
- **Product**: 독립 뉴스레터·매거진 발행인을 위한 editorial-warm 톤 마케팅 랜딩 — hero + featured issue + subscribe pricing + social proof testimonial + author profile + cta, warm ochre deep + rust copper accent + cream wheat surface, reading-first 랜딩, 한국어 1급
- **Audience**: 독립 뉴스레터 발행인 — 본인 문체와 잘 맞는 editorial-warm 랜딩을 1일 만에 셋업하고 싶은 1인 저자, 독립 매거진·퍼블리셔 — 발행 주기 issue pipeline + 구독 pricing + archive 가 랜딩에서 한눈에 보이길 원하는 소규모 편집팀, 뉴스레터 구독 전환 최적화 담당 — hero copy / pricing table / social proof / issue archive 전환 스토리를 명확히 배치하고 싶은 growth 담당자
- **Platforms**: web, mobile-web
- **Accessibility floor**: WCAG 2.2 AA

## 2. Identity Guardrails

- **Brand keywords**: marketing-landing, editorial, newsletter, publisher, warm, calm, reading-first, serif-ish, ochre, rust, wheat, cream, issue-archive, subscribe
- **Anti-keywords**: bold-saturated, streetwear-drop, fintech-dense, playful-pastel, dashboard-only, corporate-navy, magazine-cover-heavy-illustration
- **Tone of voice**: calm, warm, thoughtful, literary, sincere, inviting
- **Visual direction**: warm neutral backdrop, ochre-yellow primary emphasis, rust copper accent link, wheat cream surface tint, serif-ish heading pairing, reading-first hero, issue card archive strip, calm pricing table, author portrait circle, warm testimonial block
- **Interaction direction**: calm hover fade, sticky header subtle, issue card reveal, subscribe cta focus-ring, pricing toggle monthly-yearly, testimonial carousel gentle, author hovercard, archive scroll infinite

## 3. Design Principles

- **Marketing-Landing**: `marketing-landing`를 시각적 선택과 인터랙션 선택의 기본 기준으로 삼습니다.
- **Editorial Hierarchy**: 타이포그래피와 여백으로 위계를 만들고, 장식은 의미를 돕는 범위에서만 사용합니다.
- **Newsletter**: `newsletter`를 시각적 선택과 인터랙션 선택의 기본 기준으로 삼습니다.
- **Publisher**: `publisher`를 시각적 선택과 인터랙션 선택의 기본 기준으로 삼습니다.

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
- **Typography families**: display, text, mono
- **Spacing scale**: 0, 2, 4, 8, 12, 16, 24, 32, 48, 64, 96

### Typography System (auto-resolved)

- **Heading**: Noto Serif KR
- **Body**: Pretendard
- **Korean**: Pretendard
- **Product type detected**: editorial
- **Pairing source**: editorial (KR native)
- **Line height**: relaxed
- **Type scale**: base 16px, ratio 1.333 (xs=12px, sm=14px, md=16px, lg=21px, xl=28px, 2xl=38px, 3xl=50px)
- **Strategy**:
  - 헤딩(세리프) + 본문(산세리프) 대비 구조 — 에디토리얼 정석
  - 한글 서체: Pretendard — 라틴과 x-height/weight 조화
  - editorial 키워드 → 넉넉한 line-height, 헤딩에 serif 사용
  - calm 키워드 → comfortable spacing, 과한 weight 대비 지양
- **Heading note**: 한글 세리프의 사실상 유일한 고품질 웹폰트. 에디토리얼 한글에 필수.
- **Body note**: 한글 UI 서체의 사실상 표준. Apple SD Gothic Neo 기반이지만 더 정교함. 라틴은 Inter 계열.
- **Korean rationale**: Pretendard — 한글 UI 서체의 사실상 표준. 토스, 당근, 리디 등 국내 주요 서비스에서 사용. 자간이 자연스럽고 weight 전 구간에서 안정적.
- **Heading tracking**: lg=-0.01em, xl=-0.01em, 2xl=-0.02em, 3xl=-0.02em
- **Primary script**: korean
- **Hangul headline defaults**: Noto Serif KR | line-height 1.2-1.4 | tracking -0.02em
- **Hangul body defaults**: Pretendard | line-height 1.6-1.7 | label line-height 1.4-1.5
- **Wrap defaults**: headline word-break=keep-all, headline text-wrap=balance, body word-break=keep-all
- **Scale guidance**: 한글 hero/section heading은 영문 시안보다 한 단계 작은 스케일에서 시작해 wrap을 확인한 뒤 확장한다.
- **Hangul warning**: UI 라벨 — 작은 크기에서 가독성 저하
- **Hangul warning**: 모바일 본문 — 화면이 좁으면 답답함
- **Loading**: Pretendard(preload), Noto Serif KR(preload) | display: swap

## 6. Color Reference

- **Source**: REFERENCE X Vol.1 - Color Reference (/Users/sungwoon/ai-projects/design-ontology-harness/docs/color-reference.md)
- **Selection mode**: manual
- **Preferred families**: Standard Yellows, Pastel Yellows, Standard Oranges, Pastel Oranges
- **Palette strategy**: temperature=warm, contrast=soft, diversity=balanced, surface_style=tinted
- **Palette expansion**: supporting_color_count=10, combination_count=3, prefer_pairings=True
- **Palette roles**:
  - `primary` -> Ochre Yellow #CB9D06 / Deep Yellows
  - `accent` -> Rust #B7410E / Deep Oranges
  - `surface_tint` -> Wheat #F5DEB3 / Natural Yellows
- **Selected colors**:
  - Olive Green #708238 / Standard Greens / 중명도, 저채도의 그린 & 브라운 중간 톤 / 내추럴, 빈티지, 안정감, 따뜻함, 실용성
  - Apricot #FFB27F / Natural Oranges / 밝은 명도, 낮은 채도, 살짝 핑크빛이 도는 부드러운 오렌지 / 따뜻함, 부드러움, 친근함, 여유, 자연스러움
  - Wheat #F5DEB3 / Natural Yellows / 중명도, 저채도, 베이지 옐로 계열의 따뜻한 톤 / 따뜻함, 자연스러움, 부드러움, 안정감
- **Palette candidates**:
  - signature-1 (Signature): primary=Olive Green, accent=Apricot, surface_tint=Wheat / Olive Green matches brand tone keywords.; Apricot matches brand tone keywords.
  - assertive-3 (Assertive): primary=Olive Green, accent=Apricot, surface_tint=Terracotta / Olive Green matches brand tone keywords.; Apricot matches brand tone keywords.
- **Expanded supporting colors**:
  - Apricot #FFB27F / Natural Oranges / reference-color / Apricot reinforces the brand mood signals.
  - Peach Puff #FFDAB9 / Pastel Oranges / reference-color / Peach Puff stays inside the preferred families.; Peach Puff reinforces the brand mood signals.
  - Amber #FFBF00 / Standard Yellows / reference-color / Amber stays inside the preferred families.; Amber reinforces the brand mood signals.
  - Blanched Almond #FFEBCD / Pastel Yellows / reference-color / Blanched Almond stays inside the preferred families.; Blanched Almond reinforces the brand mood signals.
  - Coral Blush #F88379 / Pastel Oranges / reference-color / Coral Blush stays inside the preferred families.; Coral Blush reinforces the brand mood signals.
  - Chili Oil #944537 / Pantone Trend Oranges / reference-color / Chili Oil reinforces the brand mood signals.
  - Terracotta #E2725B / Natural Reds / reference-color / Terracotta reinforces the brand mood signals.
  - Flax #EEDC82 / Natural Yellows / reference-color / Flax reinforces the brand mood signals.
- **Expanded semantic roles**:
  - `brand_primary` -> Ochre Yellow #CB9D06 / Deep Yellows
  - `brand_accent` -> Rust #B7410E / Deep Oranges
  - `surface_tint` -> Wheat #F5DEB3 / Natural Yellows
  - `canvas` -> Canvas White #F7F8FA / Generated Fallback
  - `surface` -> Paper #FFFFFF / Generated Fallback
  - `surface_muted` -> Surface Muted #EEF1F6 / Generated Fallback
  - `surface_elevated` -> Paper #FFFFFF / Generated Fallback
  - `border` -> Border Neutral #D6DDE6 / Generated Fallback
  - `border_strong` -> Border Strong #B0BAC7 / Generated Fallback
  - `ink` -> Ink #111111 / Generated Fallback
- **Combination lists**:
  - Seed Core: primary=Ochre Yellow, accent=Rust, surface_tint=Wheat
  - Surface System: canvas=Canvas White, surface=Paper, surface_tint=Wheat, border=Border Neutral, ink=Ink, ink_muted=Muted Ink
  - Support Spectrum: support=Apricot, support=Peach Puff, support=Amber, support=Blanched Almond, support=Coral Blush, support=Chili Oil
- **Notes**: Ochre Yellow #CB9D06 primary — warm deep mustard yellow, subscribe-cta / pricing-highlight-tier / hero-keyword 강조 / link underline, Rust #B7410E accent — warm copper-brown deep, testimonial quote mark / pricing secondary badge / author-role chip / issue-count counter, Wheat #F5DEB3 surface_tint — warm cream near-white, hero soft band / pricing column hover / testimonial card / issue card, light mode 기본 — 독립 뉴스레터·매거진 랜딩 관례 (reading-first 톤), dark 옵션 제공 (warm deep neutral + 채도 낮춘 Ochre/Rust + Wheat 대체는 Bronze Gold deep variant 로 대비 유지), HEX 겹침 현황: signal-desk (document-content--editorial-warm) 의 surface_tint Wheat #F5DEB3 와 1 role 겹침 — editorial-warm 4 종 중 serif-paper 공통 톤을 공유하되 primary/accent 에서 Ochre Yellow/Rust 로 완전 차별화. document-content 와 marketing-landing 의 app_mode 축 분기로 랜딩 hero + pricing 중심 카드 구성으로 다름. 기존 editorial-warm 3 종 (colorfit / quill / curator) 과는 HEX 겹침 0., quill (conversation-copilot--editorial-warm) #964F4C/#8A9A5B/#EEDC82 와 primary/accent/surface_tint 전부 다름 — warm deep wine-moss-paper vs ochre-rust-wheat, curator (dashboard--editorial-warm) #614051/#FADA5E/#F9C0C4 와 전부 다름 — aubergine-naples-blush vs ochre-rust-wheat, colorfit (commerce--editorial-warm) legacy 팔레트 mirror 미등록 — HEX 겹침 검증 대상 아님
- **Application rule**: 레퍼런스 컬러는 semantic token으로 번역해서 사용하고, 접근성과 theme 호환성을 우선합니다.

## 7. Visual Reference Signals

- **Mode**: local-images
- **Coverage**: source 0 / image 0 / selected 0
- **Rule**: visual references are advisory signals for motif and layout direction; official KB/spec remain the structural source of truth.
- **Provenance**: `observed` = directly measured from local pixels, `inferred` = synthesized from image/query/brand signals, `unverified` = reliable visual evidence not yet available.
- **Query seeds**: stratechery subscribe landing, ghost publisher hero pricing, every newsletter landing, substack top publisher landing, the verge newsletter hub
### Visual Direction

- **Density**: airy (confidence 0.94, provenance inferred) / editorial x4, landing x4, hero x6
- **Surface Style**: tinted (confidence 0.94, provenance inferred) / warm x8, editorial x4, cream x2
- **Corner Style**: medium (confidence 0.5, provenance inferred) / card x5
- **Typography Mood**: editorial (confidence 0.94, provenance inferred) / editorial x4, magazine x1, serif x3
- **Color balance**: temperature=unknown, contrast=unknown, neutral_bias=unknown, provenance=unverified

### Layout Rhythm

- **Data review surface**: confidence 0.94 / provenance inferred / table x4, grid x2, data x1
- **Editorial feed**: confidence 0.94 / provenance inferred / editorial x4, magazine x1
- **Narrative landing flow**: confidence 0.94 / provenance inferred / landing x4, hero x6, pricing x7, testimonial x5
- **Dashboard grid**: confidence 0.92 / provenance inferred / dashboard x1, table x4, monitoring x1

### Image-derived Component Hints

- **Cards**: low-elevation tinted cards를 기본으로 하고, 넓은 내부 여백과 강한 section breathing room. 중간 반경으로 제품 UI 절제 유지. / provenance inferred / surface=tinted, density=airy, corner=medium
- **Navigation**: navigation은 정보 구조를 안정적으로 고정하고 시각적 장식보다 위치 신호를 우선한다. / provenance inferred / Data review surface
- **Typography**: headline rhythm과 본문 리듬의 대비를 키우고, label/metadata는 조용하게 유지한다. / provenance inferred / typography_mood=editorial
- **Data Display**: 정보 밀도를 유지하되 thin dividers와 restrained accent로 hierarchy를 만든다. / provenance inferred / layout=dashboard-grid, density=airy

### Synthesis Notes

- layout는 Data review surface 기준으로 정리
- surface language는 tinted 성향 우선
- typography mood는 editorial 축 유지
- density는 airy 기준으로 primitive spacing 조정
- palette temperature는 unknown 쪽을 우선
- Avoid: bold saturated sports hero
- Avoid: streetwear drop countdown
- Avoid: fintech dense data-table
- Avoid: SRE dark monitoring console

## 8. Component Strategy

- **Product primitives**: hero section, featured issue card, issue archive strip, pricing table, pricing toggle, subscribe cta, email capture input, testimonial card, author profile card, site header, site footer, newsletter preview, social proof logo strip, faq accordion, cta banner
- **Required families**: button, data-display, editorial, feedback, input, marketing, navigation, commerce, magazine, overlay
- **Visual-reference archetypes**:

- **Data review table** (data-display / 0.94): data-table, column-header, row-actions, filter-toolbar, pagination
- **Editorial content block** (editorial / 0.94): content-card, featured-story-card, section-header, content-meta, byline-row
- **Marketing hero stack** (marketing / 0.94): hero-section, hero-headline, hero-visual, cta-button-group, trust-strip
- **Dashboard insight module** (data-display / 0.67): stat-card, insight-card, chart-panel, section-header, filter-chip

- **button**: primary-button, secondary-button, ghost-button, icon-button, cta-button, link-button, hero-cta-group, form-actions
- **data-display**: pricing-card, feature-comparison, tag, data-table, column-header, row-actions, avatar, profile-card / visual signals: Data review table (0.94), Dashboard insight module (0.67)
- **editorial**: editor-canvas, editor-toolbar, inline-format-menu, slash-command-menu, block-controls, content-card, featured-story-card, section-header / visual signals: Editorial content block (0.94)
- **feedback**: inline-alert, empty-state, toast, upgrade-banner, status-badge, reading-progress-bar, banner, discount-badge
- **input**: text-field, search-field, segmented-control, textarea, select, checkbox, radio-group, form-section
- **marketing**: hero-container, hero-eyebrow, hero-headline, hero-subheadline, hero-visual, hero-trust-strip, faq-section, faq-item / visual signals: Marketing hero stack (0.94)
- **navigation**: mobile-topbar, mobile-tab-bar, back-button, section-tabs, pagination, app-shell, sidebar-nav, topbar
- **commerce**: product-grid, product-card, product-detail, product-gallery, product-hero-image, image-thumbnail, price-tag, original-price-strikethrough
- **magazine**: opinion-byline, manifesto-section, feature-grid-index, archive-index, issue-archive, credit-line, masthead, issue-header
- **overlay**: bottom-sheet, modal-dialog, user-menu, mention-popup, chart-tooltip, quick-view-modal

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

이 문서는 **Loom System**의 디자인 시스템 사양입니다.

### 시작하기

1. **토큰 적용**: Drop-in CSS(아래 섹션 16)의 CSS 변수를 프로젝트에 복사합니다.
2. **컬러 세팅**: Color Reference(섹션 6)의 semantic role을 기준으로 surface/text/border를 잡습니다.
3. **타이포 세팅**: Token Strategy(섹션 5)의 font family와 type scale을 적용합니다.
4. **시각 방향 확인**: Visual Reference Signals(섹션 7)에서 density/surface/layout cue를 먼저 확인합니다.
5. **컴포넌트 구현**: Component Strategy(섹션 8)의 family 순서대로 하나씩 빌드합니다.

### 우선순위

핵심 primitive: **hero section, featured issue card, issue archive strip, pricing table, pricing toggle**

이 primitive를 지원하는 컴포넌트부터 구현하고, 나머지는 필요에 따라 확장합니다.

## 15. DO / DON'T

### DO

- **Marketing-Landing**: marketing-landing와 충돌하는 컴포넌트 변형은 만들지 않기
- **Editorial Hierarchy**: 텍스트 중심 레이아웃
- **Newsletter**: newsletter와 충돌하는 컴포넌트 변형은 만들지 않기
- **Publisher**: publisher와 충돌하는 컴포넌트 변형은 만들지 않기
- 모든 시각적 선택에서 **marketing-landing, editorial, newsletter** 기준을 적용
- semantic token을 통해 컬러를 적용 (하드코딩 금지)
- 접근성 기준을 모든 text/surface 조합에서 먼저 검증
- 컴포넌트 변형 추가 전 기존 variant로 해결 가능한지 먼저 확인
- 아이콘은 SVG 컴포넌트 또는 Lucide/Heroicons/Phosphor/Tabler 등 라이브러리로 구현
- component_specs.md의 anatomy/states/token binding을 그대로 따라 완전히 구현

### DON'T

- **bold-saturated** 방향의 디자인 결정을 하지 않음
- **streetwear-drop** 방향의 디자인 결정을 하지 않음
- **fintech-dense** 방향의 디자인 결정을 하지 않음
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
  --font-heading: 'Noto Serif KR', serif;
  --font-body: 'Pretendard', sans-serif;
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
  --color-primary: #CB9D06;
  --color-accent: #B7410E;
  --color-surface-tint: #F5DEB3;

  /* --- Semantic roles (expanded) --- */
  --color-brand-primary: #CB9D06;
  --color-brand-accent: #B7410E;
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
  --color-primary-support: #FFB27F;
  --color-accent-support: #FFB27F;
  --color-info: #4A6B8A;
  --color-success: #4A7C59;
  --color-warning: #B7410E;
  --color-danger: #E2725B;
  --color-link: #CB9D06;
  --color-link-hover: #A37E05;

  /* --- Button — primary --- */
  --color-button-primary-surface-default: #CB9D06;
  --color-button-primary-surface-hover: #AD8605;
  --color-button-primary-surface-active: #997705;
  --color-button-primary-surface-disabled: #E5D498;
  --color-button-primary-text-default: #FFFFFF;
  --color-button-primary-text-disabled: #FBFCFC;
  --color-button-primary-border-default: #CB9D06;
  --color-button-primary-focus-ring: #CB9D06;

  /* --- Button — secondary --- */
  --color-button-secondary-surface-default: #FFFFFF;
  --color-button-secondary-surface-hover: #F1F1F1;
  --color-button-secondary-surface-active: #E7E7E7;
  --color-button-secondary-surface-disabled: #F7F8FA;
  --color-button-secondary-text-default: #111111;
  --color-button-secondary-text-disabled: #909091;
  --color-button-secondary-border-default: #BDC8D7;
  --color-button-secondary-border-hover: #A3B3C7;
  --color-button-secondary-focus-ring: #CB9D06;

  /* --- Button — ghost --- */
  --color-button-ghost-surface-default: transparent;
  --color-button-ghost-surface-hover: #F3F3F3;
  --color-button-ghost-surface-active: #EAEAEA;
  --color-button-ghost-surface-disabled: transparent;
  --color-button-ghost-text-default: #4B5563;
  --color-button-ghost-text-hover: #111111;
  --color-button-ghost-text-disabled: #AAAFB6;
  --color-button-ghost-border-default: transparent;
  --color-button-ghost-focus-ring: #CB9D06;

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
  --color-input-border-focus: #CB9D06;
  --color-input-border-error: #E2725B;
  --color-input-border-disabled: #E6EAF0;

  /* --- Card --- */
  --color-card-surface-default: #FFFFFF;
  --color-card-surface-hover: #FAFAFA;
  --color-card-surface-muted: #F7F8FA;
  --color-card-border-default: #D6DDE6;
  --color-card-border-hover: #B6C3D3;
  --color-card-border-focus: #CB9D06;

  /* --- Nav link --- */
  --color-nav-link-text-default: #4B5563;
  --color-nav-link-text-hover: #111111;
  --color-nav-link-text-active: #CB9D06;
  --color-nav-link-surface-hover: #F5F5F5;
  --color-nav-link-indicator: #B7410E;

  /* --- Link --- */
  --color-link-text-default: #CB9D06;
  --color-link-text-hover: #997705;
  --color-link-text-visited: #A08018;

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
  --color-feedback-warning-surface: #F6E8E2;
  --color-feedback-warning-text: #B7410E;
  --color-feedback-warning-border: #CA7855;
  --color-feedback-warning-icon: #B7410E;

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

- CSS 추출 데이터 없음 (크롤링 시 CSS가 수집되지 않았거나 extract-css가 실행되지 않음)

## 18. Component-Token Map

| Component | Tokens Used |
|-----------|-------------|
| add-to-cart-button | `color.Ochre Yellow→surface`, `color.Rust→emphasis`, `color.Wheat→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| app-shell | `color.Ochre Yellow→surface`, `color.Rust→emphasis`, `color.Wheat→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| archive-index | `color.Wheat→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| article-gallery | `color.Wheat→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| avatar | `color.Wheat→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| back-button | `color.Ochre Yellow→surface`, `color.Rust→emphasis`, `color.Wheat→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| banner | `color.Wheat→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| block-controls | `color.Wheat→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| bottom-sheet | `color.Ochre Yellow→surface`, `color.Rust→emphasis`, `color.Wheat→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| breadcrumb | `color.Ochre Yellow→surface`, `color.Rust→emphasis`, `color.Wheat→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| byline-row | `color.Wheat→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| category-pill | `color.Ochre Yellow→surface`, `color.Rust→emphasis`, `color.Wheat→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| chart-container | `color.Wheat→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| chart-legend | `color.Wheat→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| chart-panel | `color.Wheat→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| chart-tooltip | `color.Ochre Yellow→surface`, `color.Rust→emphasis`, `color.Wheat→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| checkbox | `color.Ochre Yellow→surface`, `color.Rust→emphasis`, `color.Wheat→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| chip | `color.Ochre Yellow→surface`, `color.Rust→emphasis`, `color.Wheat→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| color-swatch-selector | `color.Ochre Yellow→surface`, `color.Rust→emphasis`, `color.Wheat→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| column-header | `color.Wheat→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| comment-input | `color.Ochre Yellow→surface`, `color.Rust→emphasis`, `color.Wheat→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| comment-thread | `color.Wheat→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| content-card | `color.Wheat→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| content-meta | `color.Wheat→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| countdown-timer | `color.Wheat→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| cover-story | `color.Wheat→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| credit-line | `color.Wheat→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| cross-sell-grid | `color.Wheat→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| cta-button | `color.Ochre Yellow→surface`, `color.Rust→emphasis`, `color.Wheat→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| cta-button-group | `color.Wheat→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| customer-logo | `color.Wheat→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| data-table | `color.Wheat→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| discount-badge | `color.Wheat→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| drop-banner | `color.Wheat→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| drop-cap | `color.Wheat→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| editor-canvas | `color.Wheat→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| editor-toolbar | `color.Wheat→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| empty-state | `color.Wheat→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| faq-answer | `color.Wheat→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| faq-item | `color.Wheat→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| faq-question | `color.Wheat→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| faq-section | `color.Wheat→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| feature-article | `color.Wheat→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| feature-comparison | `color.Wheat→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| feature-grid-index | `color.Wheat→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| featured-category-tile | `color.Wheat→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| featured-story-card | `color.Wheat→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| filter-chip | `color.Ochre Yellow→surface`, `color.Rust→emphasis`, `color.Wheat→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| filter-sidebar | `color.Ochre Yellow→surface`, `color.Rust→emphasis`, `color.Wheat→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| filter-toolbar | `color.Wheat→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| footer-column | `color.Wheat→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| footer-legal | `color.Wheat→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| footer-link | `color.Wheat→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| footer-social | `color.Wheat→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| form-actions | `color.Ochre Yellow→surface`, `color.Rust→emphasis`, `color.Wheat→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| form-section | `color.Ochre Yellow→surface`, `color.Rust→emphasis`, `color.Wheat→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| ghost-button | `color.Ochre Yellow→surface`, `color.Rust→emphasis`, `color.Wheat→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| hero-banner | `color.Wheat→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| hero-container | `color.Wheat→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| hero-cta-group | `color.Ochre Yellow→surface`, `color.Rust→emphasis`, `color.Wheat→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| hero-eyebrow | `color.Wheat→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| hero-headline | `color.Wheat→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| hero-section | `color.Wheat→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| hero-subheadline | `color.Wheat→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| hero-trust-strip | `color.Wheat→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| hero-visual | `color.Wheat→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| icon-button | `color.Ochre Yellow→surface`, `color.Rust→emphasis`, `color.Wheat→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| image-thumbnail | `color.Wheat→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| inline-alert | `color.Wheat→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| inline-format-menu | `color.Wheat→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| insight-card | `color.Wheat→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| issue-archive | `color.Wheat→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| issue-header | `color.Wheat→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| issue-number | `color.Wheat→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| kanban-board | `color.Wheat→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| kanban-card | `color.Wheat→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| kanban-column | `color.Wheat→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| kicker-eyebrow | `color.Wheat→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| link-button | `color.Ochre Yellow→surface`, `color.Rust→emphasis`, `color.Wheat→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| logo-cloud | `color.Wheat→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| lookbook-hero | `color.Wheat→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| manifesto-section | `color.Wheat→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| masthead | `color.Wheat→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| mention-popup | `color.Ochre Yellow→surface`, `color.Rust→emphasis`, `color.Wheat→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| metric-highlight | `color.Wheat→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| mobile-menu-trigger | `color.Ochre Yellow→surface`, `color.Rust→emphasis`, `color.Wheat→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| mobile-tab-bar | `color.Ochre Yellow→surface`, `color.Rust→emphasis`, `color.Wheat→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| mobile-topbar | `color.Ochre Yellow→surface`, `color.Rust→emphasis`, `color.Wheat→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| modal-dialog | `color.Ochre Yellow→surface`, `color.Rust→emphasis`, `color.Wheat→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| opening-spread | `color.Wheat→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| opinion-byline | `color.Wheat→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| original-price-strikethrough | `color.Wheat→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| pagination | `color.Ochre Yellow→surface`, `color.Rust→emphasis`, `color.Wheat→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| player-controls | `color.Ochre Yellow→surface`, `color.Rust→emphasis`, `color.Wheat→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| press-quote | `color.Wheat→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| price-tag | `color.Wheat→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| pricing-card | `color.Wheat→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| primary-button | `color.Ochre Yellow→surface`, `color.Rust→emphasis`, `color.Wheat→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| product-card | `color.Wheat→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| product-detail | `color.Wheat→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| product-gallery | `color.Wheat→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| product-grid | `color.Wheat→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| product-hero-image | `color.Wheat→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| profile-card | `color.Wheat→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| pull-quote | `color.Wheat→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| quick-view-modal | `color.Ochre Yellow→surface`, `color.Rust→emphasis`, `color.Wheat→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| radio-group | `color.Ochre Yellow→surface`, `color.Rust→emphasis`, `color.Wheat→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| reading-progress-bar | `color.Wheat→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| row-actions | `color.Wheat→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| search-field | `color.Ochre Yellow→surface`, `color.Rust→emphasis`, `color.Wheat→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| secondary-button | `color.Ochre Yellow→surface`, `color.Rust→emphasis`, `color.Wheat→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| section-break | `color.Wheat→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| section-header | `color.Wheat→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| section-tabs | `color.Ochre Yellow→surface`, `color.Rust→emphasis`, `color.Wheat→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| segmented-control | `color.Ochre Yellow→surface`, `color.Rust→emphasis`, `color.Wheat→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| select | `color.Ochre Yellow→surface`, `color.Rust→emphasis`, `color.Wheat→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| sidebar-nav | `color.Ochre Yellow→surface`, `color.Rust→emphasis`, `color.Wheat→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| site-footer | `color.Wheat→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| site-header | `color.Wheat→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| site-logo | `color.Wheat→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| site-nav | `color.Wheat→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| site-nav-cta | `color.Ochre Yellow→surface`, `color.Rust→emphasis`, `color.Wheat→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| size-selector | `color.Ochre Yellow→surface`, `color.Rust→emphasis`, `color.Wheat→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| slash-command-menu | `color.Wheat→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| sort-dropdown | `color.Ochre Yellow→surface`, `color.Rust→emphasis`, `color.Wheat→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| stat-card | `color.Wheat→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| status-badge | `color.Wheat→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| subscription-callout | `color.Wheat→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| tab-bar | `color.Ochre Yellow→surface`, `color.Rust→emphasis`, `color.Wheat→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| tag | `color.Wheat→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| testimonial-author | `color.Wheat→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| testimonial-card | `color.Wheat→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| testimonial-quote | `color.Wheat→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| testimonial-section | `color.Wheat→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| text-field | `color.Ochre Yellow→surface`, `color.Rust→emphasis`, `color.Wheat→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| textarea | `color.Ochre Yellow→surface`, `color.Rust→emphasis`, `color.Wheat→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| toast | `color.Wheat→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| topbar | `color.Ochre Yellow→surface`, `color.Rust→emphasis`, `color.Wheat→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| trust-strip | `color.Wheat→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| upgrade-banner | `color.Wheat→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| user-menu | `color.Ochre Yellow→surface`, `color.Rust→emphasis`, `color.Wheat→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| variant-selector | `color.Ochre Yellow→surface`, `color.Rust→emphasis`, `color.Wheat→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| video-player | `color.Wheat→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| volume-slider | `color.Ochre Yellow→surface`, `color.Rust→emphasis`, `color.Wheat→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| wishlist-toggle | `color.Ochre Yellow→surface`, `color.Rust→emphasis`, `color.Wheat→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |

## 19. Contrast Audit

| Background | Foreground | Ratio | Level |
|------------|------------|-------|-------|
| Wheat | Ink | 14.37:1 | AAA (pass) |
| Ochre Yellow | Ink | 7.52:1 | AAA (pass) |
| Rust | Paper | 5.56:1 | AA (pass) |
| Rust | Wheat | 4.23:1 | AA-large (large-only) |
| Rust | Ink | 3.40:1 | AA-large (large-only) |
| Ochre Yellow | Paper | 2.51:1 | fail (FAIL) |
| Ochre Yellow | Rust | 2.22:1 | fail (FAIL) |
| Ochre Yellow | Wheat | 1.91:1 | fail (FAIL) |
| Wheat | Paper | 1.31:1 | fail (FAIL) |

## 20. Pattern Catalog

### Layout Patterns

- **hero section**: hero-container, hero-eyebrow, hero-headline, hero-subheadline, hero-cta-group, hero-visual, hero-trust-strip, hero-section, cta-button-group, trust-strip
- **featured issue card**: —
- **issue archive strip**: —
- **pricing table**: —
- **pricing toggle**: —
- **subscribe cta**: —
- **email capture input**: —
- **testimonial card**: —
- **author profile card**: —
- **site header**: site-header, site-logo, site-nav, site-nav-cta, mobile-menu-trigger
- **site footer**: site-footer, footer-column, footer-link, footer-legal, footer-social
- **newsletter preview**: —
- **social proof logo strip**: —
- **faq accordion**: faq-section, faq-item, faq-question, faq-answer
- **cta banner**: —
- **workspace navigation**: app-shell, sidebar-nav, topbar, breadcrumb, tab-bar
- **dashboard cards**: stat-card, insight-card, section-header, chart-panel
- **data tables**: data-table, column-header, filter-chip, row-actions, pagination, filter-toolbar

### Interaction Patterns

- **command palette**: —
- **forms**: text-field, select, checkbox, textarea, form-section, radio-group, form-actions
- **notifications**: toast, inline-alert, empty-state, banner
