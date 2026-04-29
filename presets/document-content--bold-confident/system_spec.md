# Broadside System Spec

## 1. Positioning

- **Brand**: Broadside
- **Product**: bold-confident 톤 magazine/opinion long-form reading — masthead · issue-header · cover-story · feature-article · pull-quote · drop-cap · article · table-of-contents · reading-pane · archive-index · manifesto-section, saturated primary + high-contrast + impact typography, 한국어 1급
- **Audience**: 정치·사회 opinion 저널을 탐독하는 독자 (The Atlantic / New Yorker 성향), bold 컬처/음악/영화 리뷰 매거진 reader (Pitchfork / Vice 성향), declaration/manifesto 단일호 zine 구독자 (Gen Z 젊은 에디토리얼)
- **Platforms**: web, desktop-web, tablet-web
- **Accessibility floor**: WCAG 2.2 AA

## 2. Identity Guardrails

- **Brand keywords**: document-content, magazine, editorial-feature, opinion, manifesto, long-form, article, feature-story, pull-quote, masthead, bold, energetic, high-contrast, impact, zine
- **Anti-keywords**: minimal-tech, editorial-warm, playful-pastel, corporate-conservative, dashboard-heavy, commerce-heavy, streetwear-drop, reading-calm, muted
- **Tone of voice**: confident, energetic, opinionated, impactful, declarative
- **Visual direction**: saturated primary masthead, high-contrast cover, impact headline typography, oversized kicker eyebrow, full-bleed feature spread, bold pull-quote block, chunky divider rule, editorial number-heavy TOC, opinionated long-form spread
- **Interaction direction**: bold entry hero reveal, sticky masthead scroll, pull-quote magnification, section jump TOC, feature scroll-snap, impact cover transition, reading progress bar, footnote flash highlight, masthead focus ring bold, bold share overlay

## 3. Design Principles

- **Document-Content**: `document-content`를 시각적 선택과 인터랙션 선택의 기본 기준으로 삼습니다.
- **Magazine**: `magazine`를 시각적 선택과 인터랙션 선택의 기본 기준으로 삼습니다.
- **Editorial-Feature**: `editorial-feature`를 시각적 선택과 인터랙션 선택의 기본 기준으로 삼습니다.
- **Opinion**: `opinion`를 시각적 선택과 인터랙션 선택의 기본 기준으로 삼습니다.

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
- **Product type detected**: editorial
- **Pairing source**: auto-scored
- **Line height**: tight
- **Type scale**: base 16px, ratio 1.333 (xs=12px, sm=14px, md=16px, lg=21px, xl=28px, 2xl=38px, 3xl=50px)
- **Strategy**:
  - 단일 서체(Pretendard)로 weight 대비 위계 — 일관성 우선
  - 한글 서체: Pretendard — 라틴과 x-height/weight 조화
- **Heading note**: 한글 UI 서체의 사실상 표준. Apple SD Gothic Neo 기반이지만 더 정교함. 라틴은 Inter 계열.
- **Body note**: 한글 UI 서체의 사실상 표준. Apple SD Gothic Neo 기반이지만 더 정교함. 라틴은 Inter 계열.
- **Korean rationale**: Pretendard — 한글 UI 서체의 사실상 표준. 토스, 당근, 리디 등 국내 주요 서비스에서 사용. 자간이 자연스럽고 weight 전 구간에서 안정적.
- **Heading tracking**: lg=-0.01em, xl=-0.01em, 2xl=-0.02em, 3xl=-0.02em
- **Primary script**: korean
- **Hangul headline defaults**: Pretendard | line-height 1.25-1.35 | tracking 0em
- **Hangul body defaults**: Pretendard | line-height 1.6-1.7 | label line-height 1.4-1.5
- **Wrap defaults**: headline word-break=keep-all, headline text-wrap=balance, body word-break=keep-all
- **Scale guidance**: 한글 hero/section heading은 영문 시안보다 한 단계 작은 스케일에서 시작해 wrap을 확인한 뒤 확장한다.
- **Loading**: Pretendard(preload) | display: swap

## 6. Color Reference

- **Source**: REFERENCE X Vol.1 - Color Reference (/Users/sungwoon/ai-projects/design-ontology-harness/docs/color-reference.md)
- **Selection mode**: manual
- **Preferred families**: Pantone Trend Blues, Pantone Trend Reds, Pantone Trend Oranges
- **Palette strategy**: temperature=mixed, contrast=balanced, diversity=balanced, surface_style=grounded
- **Palette expansion**: supporting_color_count=10, combination_count=3, prefer_pairings=True
- **Palette roles**:
  - `primary` -> Classic Blue #0F4C81 / Pantone Trend Blues
  - `accent` -> Goji Berry #CC142F / Pantone Trend Reds
  - `surface_tint` -> Flame #F2552C / Pantone Trend Oranges
- **Selected colors**:
  - Grenadine #DC4C46 / Pantone Trend Reds / 밝고 따뜻한 레드 오렌지 계열, 중채도 이상의 밝은 톤 / 활력, 열정, 관능, 현대적
  - Scarlet #FF2400 / Standard Reds / 강렬한 주황빛 레드 계열, 고채도와 고명도의 따뜻한 톤 / 활기, 생동감, 열정, 역동성, 주목성
  - Pure Red #FF0000 / Standard Reds / 순수 원색 레드 계열, 고채도와 중명도의 강렬한 톤 / 열정, 에너지, 주목성, 상징적, 강렬함
- **Palette candidates**:
  - signature-1 (Signature): primary=Grenadine, accent=Scarlet, surface_tint=Pure Red / Grenadine is inside preferred families.; Scarlet matches brand tone keywords.
- **Expanded supporting colors**:
  - Scarlet #FF2400 / Standard Reds / reference-color / Scarlet reinforces the brand mood signals.
  - Pure Red #FF0000 / Standard Reds / reference-color / Pure Red reinforces the brand mood signals.
  - Persimmon #EC5800 / Natural Oranges / reference-color / Persimmon reinforces the brand mood signals.
  - Pure Orange #FFA500 / Standard Oranges / reference-color / Pure Orange reinforces the brand mood signals.
  - Grenadine #DC4C46 / Pantone Trend Reds / reference-color / Grenadine stays inside the preferred families.; Grenadine reinforces the brand mood signals.
  - Pairing #BEB7A4 #BEB7A4 / Derived Pairing / pairing-swatch / Pairing #BEB7A4 reinforces the brand mood signals.; Pairing #BEB7A4 comes from the seed pairing references.
  - Living Coral #FF6F61 / Pantone Trend Oranges / reference-color / Living Coral stays inside the preferred families.; Living Coral reinforces the brand mood signals.
  - Pairing #F8F5EF #F8F5EF / Derived Pairing / pairing-swatch / Pairing #F8F5EF reinforces the brand mood signals.; Pairing #F8F5EF comes from the seed pairing references.
- **Expanded semantic roles**:
  - `brand_primary` -> Classic Blue #0F4C81 / Pantone Trend Blues
  - `brand_accent` -> Goji Berry #CC142F / Pantone Trend Reds
  - `surface_tint` -> Flame #F2552C / Pantone Trend Oranges
  - `canvas` -> Canvas White #F7F8FA / Generated Fallback
  - `surface` -> Paper #FFFFFF / Generated Fallback
  - `surface_muted` -> Surface Muted #EEF1F6 / Generated Fallback
  - `surface_elevated` -> Paper #FFFFFF / Generated Fallback
  - `border` -> Border Neutral #D6DDE6 / Generated Fallback
  - `border_strong` -> Pairing #BEB7A4 #BEB7A4 / Derived Pairing
  - `ink` -> Ink #111111 / Generated Fallback
- **Combination lists**:
  - Seed Core: primary=Classic Blue, accent=Goji Berry, surface_tint=Flame
  - Surface System: canvas=Canvas White, surface=Paper, surface_tint=Flame, border=Border Neutral, ink=Ink, ink_muted=Muted Ink
  - Support Spectrum: support=Scarlet, support=Pure Red, support=Persimmon, support=Pure Orange, support=Grenadine, support=Pairing #BEB7A4
- **Notes**: Classic Blue #0F4C81 primary — Pantone 2020 trend color, deep saturated editorial magazine blue, masthead / cover-story hero / feature-article headline impact 라인, 기존 13종 core palette 와 HEX 겹침 0 (signal-desk 의 info role 에만 등장하므로 core-role 간 충돌 없음), Goji Berry #CC142F accent — Pantone Trend 선명한 구기자 적색, pull-quote vertical rule / opinion-byline accent / manifesto-section fill / subscription-callout CTA 강조, drop Crimson #BD2E4A 와 다른 depth, premier-league Vivid Pink #E90052 와 완전 차별화, Flame #F2552C surface_tint — Pantone Trend 밝은 불꽃 오렌지 surface pop, kicker-eyebrow / issue-number chip / section-break ornament / footnote flash 에 한정 사용, bloom Coral Blush #F88379 및 Buttercream #F3E5AB 과 다른 true orange 계열, light mode 가 기본 — magazine cover spread 관례, dark 옵션 제공 (deep cool black surface + tuned Electric Blue/Goji Berry 채도 낮춤, paragraph prose 는 near-white contrast), 기존 13종 프리셋 HEX 와 겹침 0 — Electric Blue/Goji Berry/Flame 조합, document-content 는 editorial-warm (Ochre/Terracotta/Wheat) + minimal-tech (Iris Violet/Cerulean/Lavender) 2종 이미 존재 — Broadside 는 saturated primary + high-contrast impact 로 세 번째 톤 축 완성, bold-confident 는 marketing-landing (premier-league Pink/Green/Gold) + commerce (drop Crimson/Royal Purple/Buttercream) 이미 2종 존재 — Broadside 는 Electric Blue-중심 neon magazine cover 감성으로 톤 3종째 차별화
- **Application rule**: 레퍼런스 컬러는 semantic token으로 번역해서 사용하고, 접근성과 theme 호환성을 우선합니다.

## 7. Visual Reference Signals

- **Mode**: local-images
- **Coverage**: source 0 / image 0 / selected 0
- **Rule**: visual references are advisory signals for motif and layout direction; official KB/spec remain the structural source of truth.
- **Provenance**: `observed` = directly measured from local pixels, `inferred` = synthesized from image/query/brand signals, `unverified` = reliable visual evidence not yet available.
- **Query seeds**: the atlantic magazine feature cover, new yorker magazine issue cover, vice long-form opinion, pitchfork music review feature, nytimes magazine feature spread, guardian long read opinion
### Visual Direction

- **Density**: airy (confidence 0.94, provenance inferred) / editorial x4, hero x3, calm x2
- **Surface Style**: tinted (confidence 0.54, provenance inferred) / warm x3, editorial x4
- **Corner Style**: medium (confidence 0.24, provenance inferred) / fallback=medium
- **Typography Mood**: editorial (confidence 0.94, provenance inferred) / editorial x4, article x5, magazine x7
- **Color balance**: temperature=unknown, contrast=unknown, neutral_bias=unknown, provenance=unverified

### Layout Rhythm

- **Editorial feed**: confidence 0.94 / provenance inferred / editorial x4, article x5, content x1, feed x1
- **Data review surface**: confidence 0.77 / provenance inferred / table x2, grid x2
- **Narrative landing flow**: confidence 0.71 / provenance inferred / hero x3
- **Dashboard grid**: confidence 0.61 / provenance inferred / dashboard x1, table x2

### Image-derived Component Hints

- **Cards**: low-elevation tinted cards를 기본으로 하고, 넓은 내부 여백과 강한 section breathing room. 중간 반경으로 제품 UI 절제 유지. / provenance inferred / surface=tinted, density=airy, corner=medium
- **Navigation**: navigation은 정보 구조를 안정적으로 고정하고 시각적 장식보다 위치 신호를 우선한다. / provenance inferred / Editorial feed
- **Typography**: headline rhythm과 본문 리듬의 대비를 키우고, label/metadata는 조용하게 유지한다. / provenance inferred / typography_mood=editorial
- **Data Display**: 정보 밀도를 유지하되 thin dividers와 restrained accent로 hierarchy를 만든다. / provenance inferred / layout=dashboard-grid, density=airy

### Synthesis Notes

- layout는 Editorial feed 기준으로 정리
- surface language는 tinted 성향 우선
- typography mood는 editorial 축 유지
- density는 airy 기준으로 primitive spacing 조정
- palette temperature는 unknown 쪽을 우선
- Avoid: saturated commerce hero
- Avoid: calm editorial-warm magazine (Lora serif warm)
- Avoid: minimal developer docs reference
- Avoid: playful pastel feed

## 8. Component Strategy

- **Product primitives**: masthead, issue-header, issue-number, kicker-eyebrow, feature-article, cover-story, opening-spread, article-body, pull-quote, byline, credit-line, drop-cap, section-break, callout, table-of-contents, heading-anchor, footnote, reading-pane, prose-block, article-gallery, subscription-callout, manifesto-section, opinion-byline, feature-grid-index, archive-index, issue-archive, reading-progress-bar
- **Required families**: button, data-display, editorial, feedback, input, marketing, navigation, copilot-artifact, document, magazine, overlay, social
- **Visual-reference archetypes**:

- **Data review table** (data-display / 0.94): data-table, column-header, row-actions, filter-toolbar, pagination
- **Editorial content block** (editorial / 0.94): content-card, featured-story-card, section-header, content-meta, byline-row
- **Marketing hero stack** (marketing / 0.9): hero-section, hero-headline, hero-visual, cta-button-group, trust-strip
- **Dashboard insight module** (data-display / 0.57): stat-card, insight-card, chart-panel, section-header, filter-chip

- **button**: primary-button, secondary-button, ghost-button, icon-button, cta-button, link-button, hero-cta-group, form-actions
- **data-display**: data-table, column-header, row-actions, pricing-card, feature-comparison, tag, chart-container, chart-legend / visual signals: Data review table (0.94), Dashboard insight module (0.57)
- **editorial**: editor-canvas, editor-toolbar, inline-format-menu, slash-command-menu, block-controls, content-card, featured-story-card, content-meta / visual signals: Editorial content block (0.94)
- **feedback**: inline-alert, empty-state, toast, reading-progress-bar, upgrade-banner, step-progress, status-badge, banner
- **input**: text-field, search-field, segmented-control, filter-chip, chip, textarea, select, checkbox
- **marketing**: hero-container, hero-eyebrow, hero-headline, hero-subheadline, hero-visual, hero-trust-strip, feature-section, feature-grid / visual signals: Marketing hero stack (0.9)
- **navigation**: mobile-topbar, mobile-tab-bar, back-button, section-tabs, prev-next-pager, pagination, wizard-layout, app-shell
- **copilot-artifact**: message-artifact, artifact-preview-panel, draft-document, outline-sidebar, revision-timeline, reading-mode-toggle, citation-footnote, quote-block
- **document**: article-body, table-of-contents, heading-anchor, prose-block, reading-pane, footnote, link-card, callout
- **magazine**: masthead, issue-header, issue-number, cover-story, opening-spread, feature-article, kicker-eyebrow, pull-quote
- **overlay**: bottom-sheet, modal-dialog, tooltip-guide, confirm-dialog, chart-tooltip, autocomplete, mention-popup, share-sheet
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

이 문서는 **Broadside System**의 디자인 시스템 사양입니다.

### 시작하기

1. **토큰 적용**: Drop-in CSS(아래 섹션 16)의 CSS 변수를 프로젝트에 복사합니다.
2. **컬러 세팅**: Color Reference(섹션 6)의 semantic role을 기준으로 surface/text/border를 잡습니다.
3. **타이포 세팅**: Token Strategy(섹션 5)의 font family와 type scale을 적용합니다.
4. **시각 방향 확인**: Visual Reference Signals(섹션 7)에서 density/surface/layout cue를 먼저 확인합니다.
5. **컴포넌트 구현**: Component Strategy(섹션 8)의 family 순서대로 하나씩 빌드합니다.

### 우선순위

핵심 primitive: **masthead, issue-header, issue-number, kicker-eyebrow, feature-article**

이 primitive를 지원하는 컴포넌트부터 구현하고, 나머지는 필요에 따라 확장합니다.

## 15. DO / DON'T

### DO

- **Document-Content**: document-content와 충돌하는 컴포넌트 변형은 만들지 않기
- **Magazine**: magazine와 충돌하는 컴포넌트 변형은 만들지 않기
- **Editorial-Feature**: editorial-feature와 충돌하는 컴포넌트 변형은 만들지 않기
- **Opinion**: opinion와 충돌하는 컴포넌트 변형은 만들지 않기
- 모든 시각적 선택에서 **document-content, magazine, editorial-feature** 기준을 적용
- semantic token을 통해 컬러를 적용 (하드코딩 금지)
- 접근성 기준을 모든 text/surface 조합에서 먼저 검증
- 컴포넌트 변형 추가 전 기존 variant로 해결 가능한지 먼저 확인
- 아이콘은 SVG 컴포넌트 또는 Lucide/Heroicons/Phosphor/Tabler 등 라이브러리로 구현
- component_specs.md의 anatomy/states/token binding을 그대로 따라 완전히 구현

### DON'T

- **minimal-tech** 방향의 디자인 결정을 하지 않음
- **editorial-warm** 방향의 디자인 결정을 하지 않음
- **playful-pastel** 방향의 디자인 결정을 하지 않음
- **corporate-conservative** 방향의 디자인 결정을 하지 않음
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
  --color-primary: #0F4C81;
  --color-accent: #CC142F;
  --color-surface-tint: #F2552C;

  /* --- Semantic roles (expanded) --- */
  --color-brand-primary: #0F4C81;
  --color-brand-accent: #CC142F;
  --color-surface-tint: #F2552C;
  --color-canvas: #F7F8FA;
  --color-surface: #FFFFFF;
  --color-surface-muted: #EEF1F6;
  --color-surface-elevated: #FFFFFF;
  --color-border: #D6DDE6;
  --color-border-strong: #BEB7A4;
  --color-ink: #111111;
  --color-ink-muted: #4B5563;
  --color-ink-subtle: #6B7280;
  --color-ink-inverse: #FFFFFF;
  --color-primary-support: #0F4C81;
  --color-accent-support: #FF2400;
  --color-info: #0F4C81;
  --color-success: #4A7C59;
  --color-warning: #EC5800;
  --color-danger: #FF2400;
  --color-link: #0F4C81;
  --color-link-hover: #0B365C;

  /* --- Button — primary --- */
  --color-button-primary-surface-default: #0F4C81;
  --color-button-primary-surface-hover: #0C3C66;
  --color-button-primary-surface-active: #0A3153;
  --color-button-primary-surface-disabled: #9AB3CA;
  --color-button-primary-text-default: #FFFFFF;
  --color-button-primary-text-disabled: #FBFCFC;
  --color-button-primary-border-default: #0F4C81;
  --color-button-primary-focus-ring: #0F4C81;

  /* --- Button — secondary --- */
  --color-button-secondary-surface-default: #FFFFFF;
  --color-button-secondary-surface-hover: #F1F1F1;
  --color-button-secondary-surface-active: #E7E7E7;
  --color-button-secondary-surface-disabled: #F7F8FA;
  --color-button-secondary-text-default: #111111;
  --color-button-secondary-text-disabled: #909091;
  --color-button-secondary-border-default: #BDC8D7;
  --color-button-secondary-border-hover: #A3B3C7;
  --color-button-secondary-focus-ring: #0F4C81;

  /* --- Button — ghost --- */
  --color-button-ghost-surface-default: transparent;
  --color-button-ghost-surface-hover: #F3F3F3;
  --color-button-ghost-surface-active: #EAEAEA;
  --color-button-ghost-surface-disabled: transparent;
  --color-button-ghost-text-default: #4B5563;
  --color-button-ghost-text-hover: #111111;
  --color-button-ghost-text-disabled: #AAAFB6;
  --color-button-ghost-border-default: transparent;
  --color-button-ghost-focus-ring: #0F4C81;

  /* --- Button — danger --- */
  --color-button-danger-surface-default: #FF2400;
  --color-button-danger-surface-hover: #E02000;
  --color-button-danger-surface-active: #CC1D00;
  --color-button-danger-text-default: #FFFFFF;
  --color-button-danger-border-default: #FF2400;
  --color-button-danger-focus-ring: #FF2400;

  /* --- Input --- */
  --color-input-surface-default: #FFFFFF;
  --color-input-surface-filled: #FFFFFF;
  --color-input-surface-disabled: #F7F8FA;
  --color-input-text-default: #111111;
  --color-input-text-placeholder: #90969F;
  --color-input-text-disabled: #AAAFB6;
  --color-input-border-default: #D6DDE6;
  --color-input-border-hover: #B6C3D3;
  --color-input-border-focus: #0F4C81;
  --color-input-border-error: #FF2400;
  --color-input-border-disabled: #E6EAF0;

  /* --- Card --- */
  --color-card-surface-default: #FFFFFF;
  --color-card-surface-hover: #FAFAFA;
  --color-card-surface-muted: #F7F8FA;
  --color-card-border-default: #D6DDE6;
  --color-card-border-hover: #B6C3D3;
  --color-card-border-focus: #0F4C81;

  /* --- Nav link --- */
  --color-nav-link-text-default: #4B5563;
  --color-nav-link-text-hover: #111111;
  --color-nav-link-text-active: #0F4C81;
  --color-nav-link-surface-hover: #F5F5F5;
  --color-nav-link-indicator: #CC142F;

  /* --- Link --- */
  --color-link-text-default: #0F4C81;
  --color-link-text-hover: #0A3153;
  --color-link-text-visited: #183E5E;

  /* --- Feedback — info --- */
  --color-feedback-info-surface: #E2EAF0;
  --color-feedback-info-text: #0F4C81;
  --color-feedback-info-border: #5580A5;
  --color-feedback-info-icon: #0F4C81;

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
  --color-feedback-danger-surface: #FFE5E0;
  --color-feedback-danger-text: #FF2400;
  --color-feedback-danger-border: #FD644B;
  --color-feedback-danger-icon: #FF2400;

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
| activity-card | `color.Flame→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| admonition-block | `color.Flame→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| api-reference-table | `color.Flame→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| app-shell | `color.Classic Blue→surface`, `color.Goji Berry→emphasis`, `color.Flame→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| archive-index | `color.Flame→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| article-body | `color.Flame→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| article-gallery | `color.Flame→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| artifact-preview-panel | `color.Flame→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| autocomplete | `color.Classic Blue→surface`, `color.Goji Berry→emphasis`, `color.Flame→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| avatar-cluster | `color.Flame→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| back-button | `color.Classic Blue→surface`, `color.Goji Berry→emphasis`, `color.Flame→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| banner | `color.Flame→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| block-controls | `color.Flame→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| bottom-sheet | `color.Classic Blue→surface`, `color.Goji Berry→emphasis`, `color.Flame→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| breadcrumb | `color.Classic Blue→surface`, `color.Goji Berry→emphasis`, `color.Flame→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| byline-row | `color.Flame→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| callout | `color.Flame→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| chart-container | `color.Flame→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| chart-legend | `color.Flame→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| chart-panel | `color.Flame→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| chart-tooltip | `color.Classic Blue→surface`, `color.Goji Berry→emphasis`, `color.Flame→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| chat-input | `color.Classic Blue→surface`, `color.Goji Berry→emphasis`, `color.Flame→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| chat-message | `color.Flame→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| chat-thread | `color.Flame→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| checkbox | `color.Classic Blue→surface`, `color.Goji Berry→emphasis`, `color.Flame→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| chip | `color.Classic Blue→surface`, `color.Goji Berry→emphasis`, `color.Flame→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| citation-footnote | `color.Flame→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| column-header | `color.Flame→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| comment-input | `color.Classic Blue→surface`, `color.Goji Berry→emphasis`, `color.Flame→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| comment-thread | `color.Flame→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| confirm-dialog | `color.Classic Blue→surface`, `color.Goji Berry→emphasis`, `color.Flame→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| content-card | `color.Flame→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| content-meta | `color.Flame→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| cover-story | `color.Flame→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| credit-line | `color.Flame→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| cta-button | `color.Classic Blue→surface`, `color.Goji Berry→emphasis`, `color.Flame→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| cta-button-group | `color.Flame→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| customer-logo | `color.Flame→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| data-table | `color.Flame→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| draft-document | `color.Flame→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| drop-cap | `color.Flame→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| editor-canvas | `color.Flame→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| editor-toolbar | `color.Flame→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| empty-feed-illustration | `color.Flame→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| empty-state | `color.Flame→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| feature-article | `color.Flame→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| feature-card | `color.Flame→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| feature-comparison | `color.Flame→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| feature-description | `color.Flame→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| feature-grid | `color.Flame→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| feature-grid-index | `color.Flame→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| feature-icon | `color.Flame→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| feature-section | `color.Flame→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| feature-title | `color.Flame→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| featured-story-card | `color.Flame→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| feed-item | `color.Flame→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| filter-chip | `color.Classic Blue→surface`, `color.Goji Berry→emphasis`, `color.Flame→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| filter-panel | `color.Classic Blue→surface`, `color.Goji Berry→emphasis`, `color.Flame→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| filter-toolbar | `color.Flame→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| follow-button | `color.Classic Blue→surface`, `color.Goji Berry→emphasis`, `color.Flame→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| footnote | `color.Flame→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| form-actions | `color.Classic Blue→surface`, `color.Goji Berry→emphasis`, `color.Flame→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| form-section | `color.Classic Blue→surface`, `color.Goji Berry→emphasis`, `color.Flame→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| gentle-toast | `color.Flame→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| ghost-button | `color.Classic Blue→surface`, `color.Goji Berry→emphasis`, `color.Flame→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| heading-anchor | `color.Flame→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| hero-container | `color.Flame→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| hero-cta-group | `color.Classic Blue→surface`, `color.Goji Berry→emphasis`, `color.Flame→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| hero-eyebrow | `color.Flame→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| hero-headline | `color.Flame→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| hero-section | `color.Flame→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| hero-subheadline | `color.Flame→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| hero-trust-strip | `color.Flame→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| hero-visual | `color.Flame→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| icon-button | `color.Classic Blue→surface`, `color.Goji Berry→emphasis`, `color.Flame→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| inline-alert | `color.Flame→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| inline-format-menu | `color.Flame→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| insight-card | `color.Flame→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| issue-archive | `color.Flame→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| issue-header | `color.Flame→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| issue-number | `color.Flame→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| kanban-board | `color.Flame→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| kanban-card | `color.Flame→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| kanban-column | `color.Flame→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| kicker-eyebrow | `color.Flame→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| link-button | `color.Classic Blue→surface`, `color.Goji Berry→emphasis`, `color.Flame→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| link-card | `color.Flame→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| logo-cloud | `color.Flame→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| manifesto-section | `color.Flame→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| masthead | `color.Flame→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| mention-popup | `color.Classic Blue→surface`, `color.Goji Berry→emphasis`, `color.Flame→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| message-artifact | `color.Flame→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| metric-highlight | `color.Flame→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| mobile-tab-bar | `color.Classic Blue→surface`, `color.Goji Berry→emphasis`, `color.Flame→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| mobile-topbar | `color.Classic Blue→surface`, `color.Goji Berry→emphasis`, `color.Flame→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| modal-dialog | `color.Classic Blue→surface`, `color.Goji Berry→emphasis`, `color.Flame→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| opening-spread | `color.Flame→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| opinion-byline | `color.Flame→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| outline-sidebar | `color.Flame→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| pagination | `color.Classic Blue→surface`, `color.Goji Berry→emphasis`, `color.Flame→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| paragraph-block | `color.Flame→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| parameter-table | `color.Flame→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| post-card | `color.Flame→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| press-quote | `color.Flame→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| prev-next-pager | `color.Classic Blue→surface`, `color.Goji Berry→emphasis`, `color.Flame→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| pricing-card | `color.Flame→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| primary-button | `color.Classic Blue→surface`, `color.Goji Berry→emphasis`, `color.Flame→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| prose-block | `color.Flame→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| pull-quote | `color.Flame→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| quote-block | `color.Flame→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| radio-group | `color.Classic Blue→surface`, `color.Goji Berry→emphasis`, `color.Flame→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| reaction-bar | `color.Flame→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| reading-mode-toggle | `color.Flame→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| reading-pane | `color.Flame→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| reading-progress-bar | `color.Flame→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| reply-composer | `color.Classic Blue→surface`, `color.Goji Berry→emphasis`, `color.Flame→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| revision-timeline | `color.Flame→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| row-actions | `color.Flame→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| search-field | `color.Classic Blue→surface`, `color.Goji Berry→emphasis`, `color.Flame→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| search-results | `color.Flame→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| secondary-button | `color.Classic Blue→surface`, `color.Goji Berry→emphasis`, `color.Flame→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| section-break | `color.Flame→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| section-header | `color.Flame→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| section-tabs | `color.Classic Blue→surface`, `color.Goji Berry→emphasis`, `color.Flame→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| segmented-control | `color.Classic Blue→surface`, `color.Goji Berry→emphasis`, `color.Flame→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| select | `color.Classic Blue→surface`, `color.Goji Berry→emphasis`, `color.Flame→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| share-sheet | `color.Classic Blue→surface`, `color.Goji Berry→emphasis`, `color.Flame→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| sidebar-nav | `color.Classic Blue→surface`, `color.Goji Berry→emphasis`, `color.Flame→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| slash-command-menu | `color.Flame→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| soft-dialog | `color.Classic Blue→surface`, `color.Goji Berry→emphasis`, `color.Flame→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| stat-card | `color.Flame→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| status-badge | `color.Flame→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| step-progress | `color.Flame→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| subscription-callout | `color.Flame→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| tab-bar | `color.Classic Blue→surface`, `color.Goji Berry→emphasis`, `color.Flame→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| table-of-contents | `color.Flame→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| tag | `color.Flame→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| tag-pill | `color.Flame→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| text-field | `color.Classic Blue→surface`, `color.Goji Berry→emphasis`, `color.Flame→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| textarea | `color.Classic Blue→surface`, `color.Goji Berry→emphasis`, `color.Flame→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| thread-view | `color.Flame→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| timeline-stream | `color.Flame→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| toast | `color.Flame→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| tone-slider | `color.Classic Blue→surface`, `color.Goji Berry→emphasis`, `color.Flame→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| tooltip-guide | `color.Classic Blue→surface`, `color.Goji Berry→emphasis`, `color.Flame→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| topbar | `color.Classic Blue→surface`, `color.Goji Berry→emphasis`, `color.Flame→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| trust-strip | `color.Flame→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| upgrade-banner | `color.Flame→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| version-switcher | `color.Classic Blue→surface`, `color.Goji Berry→emphasis`, `color.Flame→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| wizard-layout | `color.Classic Blue→surface`, `color.Goji Berry→emphasis`, `color.Flame→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |

## 19. Contrast Audit

| Background | Foreground | Ratio | Level |
|------------|------------|-------|-------|
| Classic Blue | Paper | 8.86:1 | AAA (pass) |
| Goji Berry | Paper | 5.66:1 | AA (pass) |
| Flame | Ink | 5.50:1 | AA (pass) |
| Flame | Paper | 3.44:1 | AA-large (large-only) |
| Goji Berry | Ink | 3.33:1 | AA-large (large-only) |
| Classic Blue | Flame | 2.58:1 | fail (FAIL) |
| Classic Blue | Ink | 2.13:1 | fail (FAIL) |
| Goji Berry | Flame | 1.65:1 | fail (FAIL) |
| Classic Blue | Goji Berry | 1.56:1 | fail (FAIL) |

## 20. Pattern Catalog

### Layout Patterns

- **masthead**: —
- **issue-header**: —
- **issue-number**: —
- **kicker-eyebrow**: —
- **feature-article**: —
- **cover-story**: —
- **opening-spread**: —
- **article-body**: —
- **pull-quote**: —
- **byline**: —
- **credit-line**: —
- **drop-cap**: —
- **section-break**: —
- **callout**: —
- **table-of-contents**: —
- **heading-anchor**: —
- **footnote**: —
- **reading-pane**: —
- **prose-block**: —
- **article-gallery**: —
- **subscription-callout**: —
- **manifesto-section**: —
- **opinion-byline**: —
- **feature-grid-index**: —
- **archive-index**: —
- **issue-archive**: —
- **reading-progress-bar**: —
- **workspace navigation**: app-shell, sidebar-nav, topbar, breadcrumb, tab-bar
- **dashboard cards**: stat-card, insight-card, activity-card, section-header, chart-panel
- **data tables**: data-table, column-header, filter-chip, row-actions, pagination, filter-toolbar

### Interaction Patterns

- **command palette**: —
- **forms**: text-field, select, checkbox, textarea, form-section, radio-group, form-actions
- **notifications**: toast, inline-alert, empty-state, banner
