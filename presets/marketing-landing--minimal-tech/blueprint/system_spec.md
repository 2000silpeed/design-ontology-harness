# Beacon System Spec

## 1. Positioning

- **Brand**: Beacon
- **Product**: B2B/SaaS 팀을 위한 minimal-tech 톤 마케팅 랜딩 — hero · feature grid · pricing · social proof · testimonial · faq · cta · site header/footer, 한국어 1급
- **Audience**: B2B/SaaS 프로덕트 팀 — 성장/마케팅 엔지니어, 개발자 도구 회사 마케터 — devtools 랜딩 제작, 스타트업 초기 마케팅 리드 — 투명하고 정직한 전환 페이지
- **Platforms**: web, mobile-web
- **Accessibility floor**: WCAG 2.2 AA

## 2. Identity Guardrails

- **Brand keywords**: marketing-landing, landing, saas-landing, hero, pricing, feature-grid, social-proof, testimonial, faq, cta-section, site-footer, site-header, minimal, precise
- **Anti-keywords**: bold-confident, saturated, magazine-serif, playful, decorative, ornamental, dashboard-heavy, warm-editorial
- **Tone of voice**: clean, neutral, precise, trustworthy, restrained
- **Visual direction**: neutral hero surface, hairline borders, monochrome + restrained accent, thin pricing card, compact feature grid, logo cloud trust strip, muted testimonial card, geometric sans hierarchy, low-contrast section divider
- **Interaction direction**: sticky site header on scroll, anchor scroll to section, pricing toggle (monthly/yearly), faq accordion expand, scroll-snap section, cta button focus highlight, logo marquee subtle motion, hover-only secondary CTA

## 3. Design Principles

- **Marketing-Landing**: `marketing-landing`를 시각적 선택과 인터랙션 선택의 기본 기준으로 삼습니다.
- **Landing**: `landing`를 시각적 선택과 인터랙션 선택의 기본 기준으로 삼습니다.
- **Saas-Landing**: `saas-landing`를 시각적 선택과 인터랙션 선택의 기본 기준으로 삼습니다.
- **Hero**: `hero`를 시각적 선택과 인터랙션 선택의 기본 기준으로 삼습니다.

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

- **Source**: REFERENCE X Vol.1 - Color Reference (/Users/sungwoon/ai-projects/design-ontology-harness/docs/color-reference.md)
- **Selection mode**: manual
- **Preferred families**: Pantone Trend Blues, Pastel Blues, Standard Yellows
- **Palette strategy**: temperature=mixed, contrast=balanced, diversity=balanced, surface_style=tinted
- **Palette expansion**: supporting_color_count=10, combination_count=3, prefer_pairings=True
- **Palette roles**:
  - `primary` -> Teal Blue #01889F / Standard Blues
  - `accent` -> Goldenrod #DAA520 / Standard Yellows
  - `surface_tint` -> Powder Blue #B0E0E6 / Pastel Blues
- **Selected colors**:
  - Classic Blue #0F4C81 / Pantone Trend Blues / 중명도, 중채도, 클래식한 딥 블루 톤 / 신뢰, 평온함, 지성, 안정감
  - Ochre #CC7722 / Standard Oranges / 중명도, 중채도, 흙기 섞인 따뜻한 오렌지 / 안정감, 내추럴, 신뢰감, 지속성
  - Misty Blue #B5C7EB / Pastel Blues / 중명도, 저채도, 보라색이 섞인 뉴트럴 블루 톤 / 차분함, 사색적, 몽환적, 잔잔함, 감정의 여운
- **Palette candidates**:
  - signature-1 (Signature): primary=Classic Blue, accent=Ochre, surface_tint=Misty Blue / Classic Blue is inside preferred families.; Ochre matches brand tone keywords.
  - assertive-3 (Assertive): primary=Classic Blue, accent=Ochre, surface_tint=Sky Blue / Classic Blue is inside preferred families.; Ochre matches brand tone keywords.
- **Expanded supporting colors**:
  - Classic Blue #0F4C81 / Pantone Trend Blues / reference-color / Classic Blue stays inside the preferred families.; Classic Blue reinforces the brand mood signals.
  - Pairing #C4C4C4 #C4C4C4 / Derived Pairing / pairing-swatch / Pairing #C4C4C4 comes from the seed pairing references.; Pairing #C4C4C4 is explicitly paired with Powder Blue.
  - Pairing #2C3E50 #2C3E50 / Derived Pairing / pairing-swatch / Pairing #2C3E50 comes from the seed pairing references.; Pairing #2C3E50 is explicitly paired with Powder Blue.
  - Pairing #7A9EAF #7A9EAF / Derived Pairing / pairing-swatch / Pairing #7A9EAF comes from the seed pairing references.; Pairing #7A9EAF is explicitly paired with Goldenrod.
  - Pairing #F6F4E6 #F6F4E6 / Derived Pairing / pairing-swatch / Pairing #F6F4E6 comes from the seed pairing references.; Pairing #F6F4E6 is explicitly paired with Goldenrod.
  - Pairing #F8F5E1 #F8F5E1 / Derived Pairing / pairing-swatch / Pairing #F8F5E1 comes from the seed pairing references.; Pairing #F8F5E1 is explicitly paired with Teal Blue.
  - Navy Blue #000080 / Deep Blues / reference-color / Navy Blue reinforces the brand mood signals.
  - Pairing #333333 #333333 / Derived Pairing / pairing-swatch / Pairing #333333 comes from the seed pairing references.; Pairing #333333 is explicitly paired with Teal Blue.
- **Expanded semantic roles**:
  - `brand_primary` -> Teal Blue #01889F / Standard Blues
  - `brand_accent` -> Goldenrod #DAA520 / Standard Yellows
  - `surface_tint` -> Powder Blue #B0E0E6 / Pastel Blues
  - `canvas` -> Canvas White #F7F8FA / Generated Fallback
  - `surface` -> Paper #FFFFFF / Generated Fallback
  - `surface_muted` -> Surface Muted #EEF1F6 / Generated Fallback
  - `surface_elevated` -> Paper #FFFFFF / Generated Fallback
  - `border` -> Pairing #C4C4C4 #C4C4C4 / Derived Pairing
  - `border_strong` -> Pairing #C4C4C4 #C4C4C4 / Derived Pairing
  - `ink` -> Pairing #333333 #333333 / Derived Pairing
- **Combination lists**:
  - Seed Core: primary=Teal Blue, accent=Goldenrod, surface_tint=Powder Blue
  - Surface System: canvas=Canvas White, surface=Paper, surface_tint=Powder Blue, border=Pairing #C4C4C4, ink=Pairing #333333, ink_muted=Pairing #6B705C
  - Support Spectrum: support=Classic Blue, support=Pairing #C4C4C4, support=Pairing #2C3E50, support=Pairing #7A9EAF, support=Pairing #F6F4E6, support=Pairing #F8F5E1
- **Notes**: Teal Blue primary — cool 계열, minimal-tech 정체성 유지, hero CTA 및 site-header 링크 hover 강조, Goldenrod accent — restrained warm gold, primary CTA button · pricing featured plan · metric highlight 숫자 강조, Powder Blue surface_tint — 부드러운 파스텔 cool, neutral hero surface / section divider / logo cloud 배경, light mode 가 기본 — 마케팅 랜딩 관례, dark 옵션 제공, 기존 minimal-tech 5종 (Navy / Azure / Iris Violet / Cobalt Violet / Prussian Blue) 과 HEX 겹침 회피 — Teal Blue + Goldenrod + Powder Blue 조합
- **Application rule**: 레퍼런스 컬러는 semantic token으로 번역해서 사용하고, 접근성과 theme 호환성을 우선합니다.

## 7. Visual Reference Signals

- **Mode**: local-images
- **Coverage**: source 0 / image 0 / selected 0
- **Rule**: visual references are advisory signals for motif and layout direction; official KB/spec remain the structural source of truth.
- **Provenance**: `observed` = directly measured from local pixels, `inferred` = synthesized from image/query/brand signals, `unverified` = reliable visual evidence not yet available.
- **Query seeds**: linear landing hero, vercel landing marketing, stripe pricing page, railway landing, supabase landing, saas devtools landing minimal
### Visual Direction

- **Density**: airy (confidence 0.94, provenance inferred) / editorial x1, landing x9, hero x11
- **Surface Style**: flat (confidence 0.58, provenance inferred) / minimal x4
- **Corner Style**: medium (confidence 0.52, provenance inferred) / card x6
- **Typography Mood**: editorial (confidence 0.76, provenance inferred) / editorial x1, magazine x2, serif x2
- **Color balance**: temperature=unknown, contrast=unknown, neutral_bias=unknown, provenance=unverified

### Layout Rhythm

- **Narrative landing flow**: confidence 0.94 / provenance inferred / landing x9, hero x11, pricing x6, testimonial x5
- **Data review surface**: confidence 0.73 / provenance inferred / grid x4, timeline x1
- **Editorial feed**: confidence 0.73 / provenance inferred / editorial x1, feed x1, magazine x2
- **Dashboard grid**: confidence 0.68 / provenance inferred / dashboard x2, metric x1

### Image-derived Component Hints

- **Cards**: flat card planes를 기본으로 하고, 넓은 내부 여백과 강한 section breathing room. 중간 반경으로 제품 UI 절제 유지. / provenance inferred / surface=flat, density=airy, corner=medium
- **Navigation**: top navigation은 가볍게 유지하고 CTA와 section anchors를 분명하게 분리한다. / provenance inferred / Narrative landing flow
- **Typography**: headline rhythm과 본문 리듬의 대비를 키우고, label/metadata는 조용하게 유지한다. / provenance inferred / typography_mood=editorial
- **Data Display**: 정보 밀도를 유지하되 thin dividers와 restrained accent로 hierarchy를 만든다. / provenance inferred / layout=dashboard-grid, density=airy
- **Hero**: 대형 hero와 trust strip, CTA cluster를 허용하되 과장된 glass/gradient 효과는 지양한다. / provenance inferred / Narrative landing flow

### Synthesis Notes

- layout는 Narrative landing flow 기준으로 정리
- surface language는 flat 성향 우선
- typography mood는 editorial 축 유지
- density는 airy 기준으로 primitive spacing 조정
- palette temperature는 unknown 쪽을 우선
- Avoid: magazine serif hero
- Avoid: playful pastel illustration
- Avoid: saturated sports banner
- Avoid: dense dashboard chrome

## 8. Component Strategy

- **Product primitives**: hero container, hero headline, hero subheadline, hero CTA group, hero visual, hero trust strip, feature section, feature grid, feature card, feature icon, social proof logo cloud, customer logo, metric highlight, testimonial section, testimonial card, pricing card, feature comparison, upgrade banner, FAQ section, FAQ item, CTA section, CTA headline, site header, site nav, site footer, footer column, footer legal
- **Required families**: button, data-display, editorial, feedback, input, marketing, navigation, document, overlay, social
- **Visual-reference archetypes**:

- **Data review table** (data-display / 0.94): data-table, column-header, row-actions, filter-toolbar, pagination
- **Marketing hero stack** (marketing / 0.94): hero-section, hero-headline, hero-visual, cta-button-group, trust-strip
- **Editorial content block** (editorial / 0.91): content-card, featured-story-card, section-header, content-meta, byline-row
- **Dashboard insight module** (data-display / 0.84): stat-card, insight-card, chart-panel, section-header, filter-chip

- **button**: primary-button, secondary-button, ghost-button, icon-button, cta-button, link-button, hero-cta-group, cta-button-group
- **data-display**: pricing-card, feature-comparison, stat-card, insight-card, activity-card, section-header, data-table, column-header / visual signals: Data review table (0.94), Dashboard insight module (0.84)
- **editorial**: content-card, featured-story-card, content-meta, byline-row / visual signals: Editorial content block (0.91)
- **feedback**: inline-alert, empty-state, toast, upgrade-banner, banner, status-badge, empty-feed-illustration, gentle-toast
- **input**: text-field, search-field, segmented-control, filter-chip, textarea, select, checkbox, radio-group
- **marketing**: faq-section, faq-item, faq-question, faq-answer, hero-container, hero-eyebrow, hero-headline, hero-subheadline / visual signals: Marketing hero stack (0.94)
- **navigation**: mobile-topbar, mobile-tab-bar, back-button, section-tabs, pagination, app-shell, sidebar-nav, topbar
- **document**: article-body, table-of-contents, heading-anchor, prose-block, reading-pane, footnote, link-card, api-reference-table
- **overlay**: bottom-sheet, modal-dialog, mention-popup, confirm-dialog, share-sheet, soft-dialog
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

- Warning: [pitfall#3-rebrand] Classic Blue vs Misty Blue (blue): lightness diff 53, saturation diff 22 — possible rebrand remnant
- Warning: visual_reference.sources is empty

## 14. Quick Start

이 문서는 **Beacon System**의 디자인 시스템 사양입니다.

### 시작하기

1. **토큰 적용**: Drop-in CSS(아래 섹션 16)의 CSS 변수를 프로젝트에 복사합니다.
2. **컬러 세팅**: Color Reference(섹션 6)의 semantic role을 기준으로 surface/text/border를 잡습니다.
3. **타이포 세팅**: Token Strategy(섹션 5)의 font family와 type scale을 적용합니다.
4. **시각 방향 확인**: Visual Reference Signals(섹션 7)에서 density/surface/layout cue를 먼저 확인합니다.
5. **컴포넌트 구현**: Component Strategy(섹션 8)의 family 순서대로 하나씩 빌드합니다.

### 우선순위

핵심 primitive: **hero container, hero headline, hero subheadline, hero CTA group, hero visual**

이 primitive를 지원하는 컴포넌트부터 구현하고, 나머지는 필요에 따라 확장합니다.

## 15. DO / DON'T

### DO

- **Marketing-Landing**: marketing-landing와 충돌하는 컴포넌트 변형은 만들지 않기
- **Landing**: landing와 충돌하는 컴포넌트 변형은 만들지 않기
- **Saas-Landing**: saas-landing와 충돌하는 컴포넌트 변형은 만들지 않기
- **Hero**: hero와 충돌하는 컴포넌트 변형은 만들지 않기
- 모든 시각적 선택에서 **marketing-landing, landing, saas-landing** 기준을 적용
- semantic token을 통해 컬러를 적용 (하드코딩 금지)
- 접근성 기준을 모든 text/surface 조합에서 먼저 검증
- 컴포넌트 변형 추가 전 기존 variant로 해결 가능한지 먼저 확인
- 아이콘은 SVG 컴포넌트 또는 Lucide/Heroicons/Phosphor/Tabler 등 라이브러리로 구현
- component_specs.md의 anatomy/states/token binding을 그대로 따라 완전히 구현

### DON'T

- **bold-confident** 방향의 디자인 결정을 하지 않음
- **saturated** 방향의 디자인 결정을 하지 않음
- **magazine-serif** 방향의 디자인 결정을 하지 않음
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
  --color-primary: #01889F;
  --color-accent: #DAA520;
  --color-surface-tint: #B0E0E6;

  /* --- Semantic roles (expanded) --- */
  --color-brand-primary: #01889F;
  --color-brand-accent: #DAA520;
  --color-surface-tint: #B0E0E6;
  --color-canvas: #F7F8FA;
  --color-surface: #FFFFFF;
  --color-surface-muted: #EEF1F6;
  --color-surface-elevated: #FFFFFF;
  --color-border: #C4C4C4;
  --color-border-strong: #C4C4C4;
  --color-ink: #333333;
  --color-ink-muted: #6B705C;
  --color-ink-subtle: #7A9EAF;
  --color-ink-inverse: #FFFFFF;
  --color-primary-support: #0F4C81;
  --color-accent-support: #F6F4E6;
  --color-info: #0F4C81;
  --color-success: #4A7C59;
  --color-warning: #DAA520;
  --color-danger: #8B2252;
  --color-link: #01889F;
  --color-link-hover: #016576;

  /* --- Button — primary --- */
  --color-button-primary-surface-default: #01889F;
  --color-button-primary-surface-hover: #016E81;
  --color-button-primary-surface-active: #015D6C;
  --color-button-primary-surface-disabled: #95CBD6;
  --color-button-primary-text-default: #FFFFFF;
  --color-button-primary-text-disabled: #FBFCFC;
  --color-button-primary-border-default: #01889F;
  --color-button-primary-focus-ring: #01889F;

  /* --- Button — secondary --- */
  --color-button-secondary-surface-default: #FFFFFF;
  --color-button-secondary-surface-hover: #F3F3F3;
  --color-button-secondary-surface-active: #EBEBEB;
  --color-button-secondary-surface-disabled: #F7F8FA;
  --color-button-secondary-text-default: #333333;
  --color-button-secondary-text-disabled: #9F9FA0;
  --color-button-secondary-border-default: #B0B0B0;
  --color-button-secondary-border-hover: #9B9B9B;
  --color-button-secondary-focus-ring: #01889F;

  /* --- Button — ghost --- */
  --color-button-ghost-surface-default: transparent;
  --color-button-ghost-surface-hover: #F5F5F5;
  --color-button-ghost-surface-active: #EDEDED;
  --color-button-ghost-surface-disabled: transparent;
  --color-button-ghost-text-default: #6B705C;
  --color-button-ghost-text-hover: #333333;
  --color-button-ghost-text-disabled: #B8BBB3;
  --color-button-ghost-border-default: transparent;
  --color-button-ghost-focus-ring: #01889F;

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
  --color-input-text-default: #333333;
  --color-input-text-placeholder: #A3A69B;
  --color-input-text-disabled: #B8BBB3;
  --color-input-border-default: #C4C4C4;
  --color-input-border-hover: #ABABAB;
  --color-input-border-focus: #01889F;
  --color-input-border-error: #8B2252;
  --color-input-border-disabled: #D1D1D1;

  /* --- Card --- */
  --color-card-surface-default: #FFFFFF;
  --color-card-surface-hover: #FBFBFB;
  --color-card-surface-muted: #F7F8FA;
  --color-card-border-default: #C4C4C4;
  --color-card-border-hover: #ABABAB;
  --color-card-border-focus: #01889F;

  /* --- Nav link --- */
  --color-nav-link-text-default: #6B705C;
  --color-nav-link-text-hover: #333333;
  --color-nav-link-text-active: #01889F;
  --color-nav-link-surface-hover: #F7F7F7;
  --color-nav-link-indicator: #DAA520;

  /* --- Link --- */
  --color-link-text-default: #01889F;
  --color-link-text-hover: #015D6C;
  --color-link-text-visited: #0E6978;

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
  --color-feedback-warning-surface: #FBF4E4;
  --color-feedback-warning-text: #DAA520;
  --color-feedback-warning-border: #E3BE61;
  --color-feedback-warning-icon: #DAA520;

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
| activity-card | `color.Powder Blue→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo` |
| api-reference-table | `color.Powder Blue→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo` |
| app-shell | `color.Teal Blue→surface`, `color.Goldenrod→emphasis`, `color.Powder Blue→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo` |
| article-body | `color.Powder Blue→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo` |
| avatar-cluster | `color.Powder Blue→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo` |
| back-button | `color.Teal Blue→surface`, `color.Goldenrod→emphasis`, `color.Powder Blue→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo` |
| banner | `color.Powder Blue→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo` |
| bottom-sheet | `color.Teal Blue→surface`, `color.Goldenrod→emphasis`, `color.Powder Blue→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo` |
| breadcrumb | `color.Teal Blue→surface`, `color.Goldenrod→emphasis`, `color.Powder Blue→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo` |
| byline-row | `color.Powder Blue→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo` |
| chart-panel | `color.Powder Blue→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo` |
| chat-input | `color.Teal Blue→surface`, `color.Goldenrod→emphasis`, `color.Powder Blue→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo` |
| chat-message | `color.Powder Blue→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo` |
| chat-thread | `color.Powder Blue→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo` |
| checkbox | `color.Teal Blue→surface`, `color.Goldenrod→emphasis`, `color.Powder Blue→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo` |
| chip | `color.Teal Blue→surface`, `color.Goldenrod→emphasis`, `color.Powder Blue→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo` |
| column-header | `color.Powder Blue→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo` |
| comment-input | `color.Teal Blue→surface`, `color.Goldenrod→emphasis`, `color.Powder Blue→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo` |
| comment-thread | `color.Powder Blue→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo` |
| confirm-dialog | `color.Teal Blue→surface`, `color.Goldenrod→emphasis`, `color.Powder Blue→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo` |
| content-card | `color.Powder Blue→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo` |
| content-meta | `color.Powder Blue→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo` |
| cta-button | `color.Teal Blue→surface`, `color.Goldenrod→emphasis`, `color.Powder Blue→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo` |
| cta-button-group | `color.Teal Blue→surface`, `color.Goldenrod→emphasis`, `color.Powder Blue→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo` |
| cta-headline | `color.Powder Blue→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo` |
| cta-section | `color.Powder Blue→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo` |
| cta-supporting-text | `color.Powder Blue→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo` |
| customer-logo | `color.Powder Blue→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo` |
| data-table | `color.Powder Blue→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo` |
| empty-feed-illustration | `color.Powder Blue→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo` |
| empty-state | `color.Powder Blue→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo` |
| faq-answer | `color.Powder Blue→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo` |
| faq-item | `color.Powder Blue→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo` |
| faq-question | `color.Powder Blue→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo` |
| faq-section | `color.Powder Blue→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo` |
| feature-card | `color.Powder Blue→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo` |
| feature-comparison | `color.Powder Blue→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo` |
| feature-description | `color.Powder Blue→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo` |
| feature-grid | `color.Powder Blue→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo` |
| feature-icon | `color.Powder Blue→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo` |
| feature-section | `color.Powder Blue→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo` |
| feature-title | `color.Powder Blue→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo` |
| featured-story-card | `color.Powder Blue→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo` |
| feed-item | `color.Powder Blue→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo` |
| filter-chip | `color.Teal Blue→surface`, `color.Goldenrod→emphasis`, `color.Powder Blue→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo` |
| filter-toolbar | `color.Powder Blue→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo` |
| follow-button | `color.Teal Blue→surface`, `color.Goldenrod→emphasis`, `color.Powder Blue→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo` |
| footer-column | `color.Powder Blue→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo` |
| footer-legal | `color.Powder Blue→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo` |
| footer-link | `color.Powder Blue→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo` |
| footer-social | `color.Powder Blue→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo` |
| footnote | `color.Powder Blue→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo` |
| form-actions | `color.Teal Blue→surface`, `color.Goldenrod→emphasis`, `color.Powder Blue→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo` |
| form-section | `color.Teal Blue→surface`, `color.Goldenrod→emphasis`, `color.Powder Blue→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo` |
| gentle-toast | `color.Powder Blue→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo` |
| ghost-button | `color.Teal Blue→surface`, `color.Goldenrod→emphasis`, `color.Powder Blue→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo` |
| heading-anchor | `color.Powder Blue→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo` |
| hero-container | `color.Powder Blue→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo` |
| hero-cta-group | `color.Teal Blue→surface`, `color.Goldenrod→emphasis`, `color.Powder Blue→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo` |
| hero-eyebrow | `color.Powder Blue→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo` |
| hero-headline | `color.Powder Blue→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo` |
| hero-section | `color.Powder Blue→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo` |
| hero-subheadline | `color.Powder Blue→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo` |
| hero-trust-strip | `color.Powder Blue→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo` |
| hero-visual | `color.Powder Blue→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo` |
| icon-button | `color.Teal Blue→surface`, `color.Goldenrod→emphasis`, `color.Powder Blue→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo` |
| inline-alert | `color.Powder Blue→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo` |
| insight-card | `color.Powder Blue→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo` |
| kanban-board | `color.Powder Blue→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo` |
| kanban-card | `color.Powder Blue→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo` |
| kanban-column | `color.Powder Blue→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo` |
| link-button | `color.Teal Blue→surface`, `color.Goldenrod→emphasis`, `color.Powder Blue→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo` |
| link-card | `color.Powder Blue→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo` |
| logo-cloud | `color.Powder Blue→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo` |
| mention-popup | `color.Teal Blue→surface`, `color.Goldenrod→emphasis`, `color.Powder Blue→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo` |
| metric-highlight | `color.Powder Blue→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo` |
| mobile-menu-trigger | `color.Teal Blue→surface`, `color.Goldenrod→emphasis`, `color.Powder Blue→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo` |
| mobile-tab-bar | `color.Teal Blue→surface`, `color.Goldenrod→emphasis`, `color.Powder Blue→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo` |
| mobile-topbar | `color.Teal Blue→surface`, `color.Goldenrod→emphasis`, `color.Powder Blue→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo` |
| modal-dialog | `color.Teal Blue→surface`, `color.Goldenrod→emphasis`, `color.Powder Blue→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo` |
| pagination | `color.Teal Blue→surface`, `color.Goldenrod→emphasis`, `color.Powder Blue→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo` |
| parameter-table | `color.Powder Blue→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo` |
| post-card | `color.Powder Blue→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo` |
| press-quote | `color.Powder Blue→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo` |
| prev-next-pager | `color.Teal Blue→surface`, `color.Goldenrod→emphasis`, `color.Powder Blue→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo` |
| pricing-card | `color.Powder Blue→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo` |
| primary-button | `color.Teal Blue→surface`, `color.Goldenrod→emphasis`, `color.Powder Blue→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo` |
| prose-block | `color.Powder Blue→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo` |
| radio-group | `color.Teal Blue→surface`, `color.Goldenrod→emphasis`, `color.Powder Blue→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo` |
| reaction-bar | `color.Powder Blue→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo` |
| reading-pane | `color.Powder Blue→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo` |
| reply-composer | `color.Teal Blue→surface`, `color.Goldenrod→emphasis`, `color.Powder Blue→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo` |
| row-actions | `color.Powder Blue→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo` |
| search-field | `color.Teal Blue→surface`, `color.Goldenrod→emphasis`, `color.Powder Blue→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo` |
| secondary-button | `color.Teal Blue→surface`, `color.Goldenrod→emphasis`, `color.Powder Blue→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo` |
| section-header | `color.Powder Blue→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo` |
| section-tabs | `color.Teal Blue→surface`, `color.Goldenrod→emphasis`, `color.Powder Blue→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo` |
| segmented-control | `color.Teal Blue→surface`, `color.Goldenrod→emphasis`, `color.Powder Blue→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo` |
| select | `color.Teal Blue→surface`, `color.Goldenrod→emphasis`, `color.Powder Blue→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo` |
| share-sheet | `color.Teal Blue→surface`, `color.Goldenrod→emphasis`, `color.Powder Blue→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo` |
| sidebar-nav | `color.Teal Blue→surface`, `color.Goldenrod→emphasis`, `color.Powder Blue→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo` |
| site-footer | `color.Powder Blue→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo` |
| site-header | `color.Powder Blue→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo` |
| site-logo | `color.Powder Blue→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo` |
| site-nav | `color.Powder Blue→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo` |
| site-nav-cta | `color.Teal Blue→surface`, `color.Goldenrod→emphasis`, `color.Powder Blue→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo` |
| soft-dialog | `color.Teal Blue→surface`, `color.Goldenrod→emphasis`, `color.Powder Blue→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo` |
| stat-card | `color.Powder Blue→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo` |
| status-badge | `color.Powder Blue→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo` |
| tab-bar | `color.Teal Blue→surface`, `color.Goldenrod→emphasis`, `color.Powder Blue→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo` |
| table-of-contents | `color.Powder Blue→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo` |
| tag | `color.Powder Blue→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo` |
| tag-pill | `color.Powder Blue→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo` |
| testimonial-author | `color.Powder Blue→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo` |
| testimonial-card | `color.Powder Blue→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo` |
| testimonial-quote | `color.Powder Blue→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo` |
| testimonial-section | `color.Powder Blue→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo` |
| text-field | `color.Teal Blue→surface`, `color.Goldenrod→emphasis`, `color.Powder Blue→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo` |
| textarea | `color.Teal Blue→surface`, `color.Goldenrod→emphasis`, `color.Powder Blue→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo` |
| thread-view | `color.Powder Blue→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo` |
| timeline-stream | `color.Powder Blue→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo` |
| toast | `color.Powder Blue→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo` |
| topbar | `color.Teal Blue→surface`, `color.Goldenrod→emphasis`, `color.Powder Blue→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo` |
| trust-strip | `color.Powder Blue→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo` |
| upgrade-banner | `color.Powder Blue→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo` |
| version-switcher | `color.Teal Blue→surface`, `color.Goldenrod→emphasis`, `color.Powder Blue→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo` |

## 19. Contrast Audit

| Background | Foreground | Ratio | Level |
|------------|------------|-------|-------|
| Powder Blue | Ink | 13.17:1 | AAA (pass) |
| Goldenrod | Ink | 8.44:1 | AAA (pass) |
| Teal Blue | Ink | 4.52:1 | AA (pass) |
| Teal Blue | Paper | 4.18:1 | AA-large (large-only) |
| Teal Blue | Powder Blue | 2.92:1 | fail (FAIL) |
| Goldenrod | Paper | 2.24:1 | fail (FAIL) |
| Teal Blue | Goldenrod | 1.87:1 | fail (FAIL) |
| Goldenrod | Powder Blue | 1.56:1 | fail (FAIL) |
| Powder Blue | Paper | 1.43:1 | fail (FAIL) |

## 20. Pattern Catalog

### Layout Patterns

- **hero container**: —
- **hero headline**: —
- **hero subheadline**: —
- **hero CTA group**: —
- **hero visual**: —
- **hero trust strip**: —
- **feature section**: —
- **feature grid**: feature-section, feature-grid, feature-card, feature-icon, feature-title, feature-description
- **feature card**: —
- **feature icon**: —
- **social proof logo cloud**: —
- **customer logo**: —
- **metric highlight**: —
- **testimonial section**: —
- **testimonial card**: —
- **pricing card**: —
- **feature comparison**: —
- **upgrade banner**: —
- **FAQ section**: —
- **FAQ item**: —
- **CTA section**: —
- **CTA headline**: —
- **site header**: site-header, site-logo, site-nav, site-nav-cta, mobile-menu-trigger
- **site nav**: —
- **site footer**: site-footer, footer-column, footer-link, footer-legal, footer-social
- **footer column**: —
- **footer legal**: —
- **workspace navigation**: app-shell, sidebar-nav, topbar, breadcrumb, tab-bar
- **dashboard cards**: stat-card, insight-card, activity-card, section-header, chart-panel
- **data tables**: data-table, column-header, filter-chip, row-actions, pagination, filter-toolbar

### Interaction Patterns

- **command palette**: —
- **forms**: text-field, select, checkbox, textarea, form-section, radio-group, form-actions
- **notifications**: toast, inline-alert, empty-state, banner
