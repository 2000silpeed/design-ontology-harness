# Checkpoint System Spec

## 1. Positioning

- **Brand**: Checkpoint
- **Product**: 콘솔과 PC 게임을 비평, 비교, 추천하는 에디토리얼 게임 리뷰 사이트
- **Audience**: 신작 구매 결정을 빠르게 내리고 싶은 코어 게이머, 플랫폼별 성능과 완성도를 비교하려는 사용자, 신뢰 가능한 비평과 추천 큐레이션을 찾는 독자
- **Platforms**: web, mobile-web
- **Accessibility floor**: WCAG 2.2 AA

## 2. Identity Guardrails

- **Brand keywords**: bold, editorial, analytical, trustworthy
- **Anti-keywords**: generic, cluttered, clickbait, childish
- **Tone of voice**: sharp, confident, credible
- **Visual direction**: cinematic crops, poster-led cards, strong contrast, data-rich editorial layout, dark mode first
- **Interaction direction**: fast filtering, clear comparison flows, predictable navigation, low-noise motion

## 3. Design Principles

- **Bold with Discipline**: 강한 개성은 허용하되 구조를 해치지 않는 선에서 통제합니다.
- **Editorial Hierarchy**: 타이포그래피와 여백으로 위계를 만들고, 장식은 의미를 돕는 범위에서만 사용합니다.
- **Analytical**: `analytical`를 시각적 선택과 인터랙션 선택의 기본 기준으로 삼습니다.
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

- **Heading**: Pretendard
- **Body**: Noto Sans KR
- **Korean**: Noto Sans KR
- **Product type detected**: editorial
- **Pairing source**: auto-scored
- **Line height**: tight
- **Type scale**: base 16px, ratio 1.333 (xs=12px, sm=14px, md=16px, lg=21px, xl=28px, 2xl=38px, 3xl=50px)
- **Strategy**:
  - 같은 패밀리에서 weight 대비로 위계 형성
  - 한글 서체: Noto Sans KR — 라틴과 x-height/weight 조화
  - editorial 키워드 → 넉넉한 line-height, 헤딩에 serif 사용
- **Heading note**: 한글 UI 서체의 사실상 표준. Apple SD Gothic Neo 기반이지만 더 정교함. 라틴은 Inter 계열.
- **Body note**: Google의 범용 서체. 전 세계 문자 지원. Noto Sans KR은 한글 최적화.
- **Korean rationale**: Noto Sans KR — Google이 만든 범용 한글 서체. 글자폭이 넓어서 여유 있는 레이아웃에 적합. 다국어 지원이 필요한 서비스의 기본 선택.
- **Heading tracking**: lg=-0.01em, xl=-0.01em, 2xl=-0.02em, 3xl=-0.02em
- **Primary script**: korean
- **Hangul headline defaults**: Pretendard | line-height 1.25-1.35 | tracking 0em
- **Hangul body defaults**: Noto Sans KR | line-height 1.6-1.8 | label line-height 1.45-1.55
- **Wrap defaults**: headline word-break=keep-all, headline text-wrap=balance, body word-break=keep-all
- **Scale guidance**: 한글 hero/section heading은 영문 시안보다 한 단계 작은 스케일에서 시작해 wrap을 확인한 뒤 확장한다.
- **Hangul warning**: 좁은 UI 공간 — 글자폭이 넓어서 공간을 많이 차지
- **Loading**: Noto Sans KR(preload), Pretendard(preload) | display: swap

## 6. Color Reference

- **Source**: Checkpoint Color Palette (/Users/sungwoon/Documents/designSystem/projects/checkpoint/docs/color-reference.md)
- **Selection mode**: brand-guided
- **Preferred families**: Carbon Neutrals, Signal Reds, Boss Stage Accents
- **Palette strategy**: temperature=neutral, contrast=vivid, diversity=balanced, surface_style=grounded
- **Palette expansion**: supporting_color_count=12, combination_count=4, prefer_pairings=True
- **Active palette**: signature-1
- **Active roles**:
  - `primary` -> Controller Slate #161D28 / Carbon Neutrals
  - `accent` -> XP Lime #A6FF4D / Boss Stage Accents
  - `surface_tint` -> Critical Ember #FF5A36 / Signal Reds
- **Selected colors**:
  - Controller Slate #161D28 / Carbon Neutrals / 안정감, 차분함, 기술적
  - XP Lime #A6FF4D / Boss Stage Accents / 생동감, 긍정, 반응성
  - Critical Ember #FF5A36 / Signal Reds / 긴장감, 주목성, 확신
- **Palette candidates**:
  - signature-1 (Signature): primary=Controller Slate, accent=XP Lime, surface_tint=Critical Ember / Controller Slate is inside preferred families.; XP Lime is inside preferred families.
  - soft-spread-2 (Soft Spread): primary=Controller Slate, accent=Critical Ember, surface_tint=Save White / Controller Slate is inside preferred families.; Critical Ember is inside preferred families.
- **Expanded supporting colors**:
  - Controller Slate #161D28 / Carbon Neutrals / pairing-reference / Controller Slate stays inside the preferred families.; Controller Slate reinforces the brand mood signals.
  - Critical Ember #FF5A36 / Signal Reds / pairing-reference / Critical Ember stays inside the preferred families.; Critical Ember reinforces the brand mood signals.
  - Night Server #0B0F16 / Carbon Neutrals / pairing-reference / Night Server stays inside the preferred families.; Night Server reinforces the brand mood signals.
  - XP Lime #A6FF4D / Boss Stage Accents / pairing-reference / XP Lime stays inside the preferred families.; XP Lime reinforces the brand mood signals.
  - HUD Cyan #5DD6FF / Boss Stage Accents / pairing-reference / HUD Cyan stays inside the preferred families.; HUD Cyan reinforces the brand mood signals.
  - Pairing #FFF1EC #FFF1EC / Derived Pairing / pairing-swatch / Pairing #FFF1EC reinforces the brand mood signals.; Pairing #FFF1EC comes from the seed pairing references.
  - Save White #F4F7FB / Light Surface / pairing-reference / Save White reinforces the brand mood signals.; Save White comes from the seed pairing references.
  - Patch Gray #7F8A9A / Carbon Neutrals / reference-color / Patch Gray stays inside the preferred families.; Patch Gray reinforces the brand mood signals.
- **Expanded semantic roles**:
  - `brand_primary` -> Controller Slate #161D28 / Carbon Neutrals
  - `brand_accent` -> XP Lime #A6FF4D / Boss Stage Accents
  - `surface_tint` -> Critical Ember #FF5A36 / Signal Reds
  - `canvas` -> Canvas White #F7F8FA / Generated Fallback
  - `surface` -> Paper #FFFFFF / Generated Fallback
  - `surface_muted` -> Surface Muted #EEF1F6 / Generated Fallback
  - `surface_elevated` -> Paper #FFFFFF / Generated Fallback
  - `border` -> Border Neutral #D6DDE6 / Generated Fallback
  - `border_strong` -> Border Strong #B0BAC7 / Generated Fallback
  - `ink` -> Night Server #0B0F16 / Carbon Neutrals
- **Combination lists**:
  - Seed Core: primary=Controller Slate, accent=XP Lime, surface_tint=Critical Ember
  - Surface System: canvas=Canvas White, surface=Paper, surface_tint=Critical Ember, border=Border Neutral, ink=Night Server, ink_muted=Muted Ink
  - Support Spectrum: support=Controller Slate, support=Critical Ember, support=Night Server, support=XP Lime, support=HUD Cyan, support=Pairing #FFF1EC
  - Semantic States: info=Night Server, success=Strong Buy, warning=Pairing #FFF1EC, danger=Boss Warning
- **Notes**: 게임 매거진처럼 어두운 배경 위에 강한 포인트 컬러가 올라오는 조합을 우선합니다, primary는 깊고 안정적이어야 하고 accent는 리뷰 스코어와 CTA를 분리해 보여줄 만큼 선명해야 합니다
- **Application rule**: 레퍼런스 컬러는 semantic token으로 번역해서 사용하고, 접근성과 theme 호환성을 우선합니다.

## 7. Visual Reference Signals

- **Mode**: local-images
- **Coverage**: source 0 / image 0 / selected 0
- **Rule**: visual references are advisory signals for motif and layout direction; official KB/spec remain the structural source of truth.
- **Provenance**: `observed` = directly measured from local pixels, `inferred` = synthesized from image/query/brand signals, `unverified` = reliable visual evidence not yet available.
- **Query seeds**: bold high-contrast data review table ui, editorial text-first operations control panel, trustworthy measured comment thread interface, cinematic crops collaboration feedback panel, poster-led cards faceted search interface, strong contrast filter toolbar ui
### Visual Direction

- **Density**: airy (confidence 0.87, provenance inferred) / editorial x5, hero x1
- **Surface Style**: tinted (confidence 0.45, provenance inferred) / editorial x5
- **Corner Style**: medium (confidence 0.24, provenance inferred) / fallback=medium
- **Typography Mood**: editorial (confidence 0.94, provenance inferred) / editorial x5, content x1
- **Color balance**: temperature=unknown, contrast=unknown, neutral_bias=unknown, provenance=unverified

### Layout Rhythm

- **Editorial feed**: confidence 0.94 / provenance inferred / editorial x5, content x1
- **Split-pane workspace**: confidence 0.94 / provenance inferred / workspace x2, panel x2, editor x1, navigation x2
- **Data review surface**: confidence 0.77 / provenance inferred / table x1, data x2, filter x3
- **Narrative landing flow**: confidence 0.4 / provenance inferred / hero x1

### Image-derived Component Hints

- **Cards**: low-elevation tinted cards를 기본으로 하고, 넓은 내부 여백과 강한 section breathing room. 중간 반경으로 제품 UI 절제 유지. / provenance inferred / surface=tinted, density=airy, corner=medium
- **Navigation**: 고정 sidebar 또는 split-pane navigation을 우선하고, 현재 위치와 scope를 항상 명시한다. / provenance inferred / Split-pane workspace
- **Typography**: headline rhythm과 본문 리듬의 대비를 키우고, label/metadata는 조용하게 유지한다. / provenance inferred / typography_mood=editorial
- **Data Display**: 정보 밀도를 유지하되 thin dividers와 restrained accent로 hierarchy를 만든다. / provenance inferred / layout=data-review-surface, density=airy

### Synthesis Notes

- layout는 Editorial feed 기준으로 정리
- surface language는 tinted 성향 우선
- typography mood는 editorial 축 유지
- density는 airy 기준으로 primitive spacing 조정
- palette temperature는 unknown 쪽을 우선
- Avoid: streamer overlay aesthetics
- Avoid: glassmorphism-heavy cards
- Avoid: rainbow neon clutter

## 8. Component Strategy

- **Product primitives**: hero spotlight, review cards, score badges, platform filters, comparison tables, ranking lists, search and autocomplete, release calendar
- **Required families**: button, data-display, editorial, feedback, input, marketing, navigation, overlay
- **Visual-reference archetypes**:

- **Data review table** (data-display / 0.94): data-table, column-header, row-actions, filter-toolbar, pagination
- **Editorial content block** (editorial / 0.94): content-card, featured-story-card, section-header, content-meta, byline-row
- **Workspace shell** (navigation / 0.94): app-shell, sidebar-nav, workspace-switcher, breadcrumb, context-panel
- **Conversation sidecar** (overlay / 0.62): chat-panel, message-thread, message-composer, context-drawer
- **Marketing hero stack** (marketing / 0.51): hero-section, hero-headline, hero-visual, cta-button-group, trust-strip

- **button**: primary-button, secondary-button, ghost-button, icon-button, cta-button, link-button, form-actions, hero-cta-group
- **data-display**: data-table, column-header, row-actions, comment-thread, search-results, tag, stat-card, insight-card / visual signals: Data review table (0.94)
- **editorial**: editor-canvas, editor-toolbar, inline-format-menu, slash-command-menu, block-controls, content-card, featured-story-card, content-meta / visual signals: Editorial content block (0.94)
- **feedback**: inline-alert, empty-state, toast, status-badge, shortcut-hint, upgrade-banner
- **input**: text-field, search-field, segmented-control, filter-chip, comment-input, filter-panel, textarea, select
- **marketing**: hero-container, hero-eyebrow, hero-headline, hero-subheadline, hero-visual, hero-trust-strip, feature-section, feature-grid
- **navigation**: mobile-topbar, mobile-tab-bar, back-button, section-tabs, pagination, app-shell, sidebar-nav, topbar / visual signals: Workspace shell (0.94)
- **overlay**: bottom-sheet, modal-dialog, mention-popup, autocomplete, command-palette, command-result-item, chart-tooltip, chat-panel / visual signals: Conversation sidecar (0.62)

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

- Warning: visual_reference.sources is empty

## 14. Quick Start

이 문서는 **Checkpoint System**의 디자인 시스템 사양입니다.

### 시작하기

1. **토큰 적용**: Drop-in CSS(아래 섹션 16)의 CSS 변수를 프로젝트에 복사합니다.
2. **컬러 세팅**: Color Reference(섹션 6)의 semantic role을 기준으로 surface/text/border를 잡습니다.
3. **타이포 세팅**: Token Strategy(섹션 5)의 font family와 type scale을 적용합니다.
4. **시각 방향 확인**: Visual Reference Signals(섹션 7)에서 density/surface/layout cue를 먼저 확인합니다.
5. **컴포넌트 구현**: Component Strategy(섹션 8)의 family 순서대로 하나씩 빌드합니다.

### 우선순위

핵심 primitive: **hero spotlight, review cards, score badges, platform filters, comparison tables**

이 primitive를 지원하는 컴포넌트부터 구현하고, 나머지는 필요에 따라 확장합니다.

## 15. DO / DON'T

### DO

- **Bold with Discipline**: 강한 accent 색상 1개 중심
- **Editorial Hierarchy**: 텍스트 중심 레이아웃
- **Analytical**: analytical와 충돌하는 컴포넌트 변형은 만들지 않기
- **Trust Through Consistency**: 일관된 disabled/error/success 패턴
- 모든 시각적 선택에서 **bold, editorial, analytical** 기준을 적용
- semantic token을 통해 컬러를 적용 (하드코딩 금지)
- 접근성 기준을 모든 text/surface 조합에서 먼저 검증
- 컴포넌트 변형 추가 전 기존 variant로 해결 가능한지 먼저 확인
- 아이콘은 SVG 컴포넌트 또는 Lucide/Heroicons/Phosphor/Tabler 등 라이브러리로 구현
- component_specs.md의 anatomy/states/token binding을 그대로 따라 완전히 구현

### DON'T

- **generic** 방향의 디자인 결정을 하지 않음
- **cluttered** 방향의 디자인 결정을 하지 않음
- **clickbait** 방향의 디자인 결정을 하지 않음
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
  --font-heading: 'Pretendard', serif;
  --font-body: 'Noto Sans KR', sans-serif;
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
  --color-primary: #161D28;
  --color-accent: #A6FF4D;
  --color-surface-tint: #FF5A36;

  /* --- Semantic roles (expanded) --- */
  --color-brand-primary: #161D28;
  --color-brand-accent: #A6FF4D;
  --color-surface-tint: #FF5A36;
  --color-canvas: #F7F8FA;
  --color-surface: #FFFFFF;
  --color-surface-muted: #EEF1F6;
  --color-surface-elevated: #FFFFFF;
  --color-border: #D6DDE6;
  --color-border-strong: #B0BAC7;
  --color-ink: #0B0F16;
  --color-ink-muted: #4B5563;
  --color-ink-subtle: #7F8A9A;
  --color-ink-inverse: #FFFFFF;
  --color-primary-support: #7F8A9A;
  --color-accent-support: #3DDC84;
  --color-info: #0B0F16;
  --color-success: #3DDC84;
  --color-warning: #FFF1EC;
  --color-danger: #FF7A00;
  --color-link: #161D28;
  --color-link-hover: #080A0E;

  /* --- Button — primary --- */
  --color-button-primary-surface-default: #161D28;
  --color-button-primary-surface-hover: #0B0F14;
  --color-button-primary-surface-active: #040507;
  --color-button-primary-surface-disabled: #9DA0A6;
  --color-button-primary-text-default: #FFFFFF;
  --color-button-primary-text-disabled: #FBFCFC;
  --color-button-primary-border-default: #161D28;
  --color-button-primary-focus-ring: #161D28;

  /* --- Button — secondary --- */
  --color-button-secondary-surface-default: #FFFFFF;
  --color-button-secondary-surface-hover: #F0F1F1;
  --color-button-secondary-surface-active: #E7E7E8;
  --color-button-secondary-surface-disabled: #F7F8FA;
  --color-button-secondary-text-default: #0B0F16;
  --color-button-secondary-text-disabled: #8D8F93;
  --color-button-secondary-border-default: #BDC8D7;
  --color-button-secondary-border-hover: #A3B3C7;
  --color-button-secondary-focus-ring: #161D28;

  /* --- Button — ghost --- */
  --color-button-ghost-surface-default: transparent;
  --color-button-ghost-surface-hover: #F3F3F3;
  --color-button-ghost-surface-active: #E9E9EA;
  --color-button-ghost-surface-disabled: transparent;
  --color-button-ghost-text-default: #4B5563;
  --color-button-ghost-text-hover: #0B0F16;
  --color-button-ghost-text-disabled: #AAAFB6;
  --color-button-ghost-border-default: transparent;
  --color-button-ghost-focus-ring: #161D28;

  /* --- Button — danger --- */
  --color-button-danger-surface-default: #FF7A00;
  --color-button-danger-surface-hover: #E06B00;
  --color-button-danger-surface-active: #CC6200;
  --color-button-danger-text-default: #FFFFFF;
  --color-button-danger-border-default: #FF7A00;
  --color-button-danger-focus-ring: #FF7A00;

  /* --- Input --- */
  --color-input-surface-default: #FFFFFF;
  --color-input-surface-filled: #FFFFFF;
  --color-input-surface-disabled: #F7F8FA;
  --color-input-text-default: #0B0F16;
  --color-input-text-placeholder: #90969F;
  --color-input-text-disabled: #AAAFB6;
  --color-input-border-default: #D6DDE6;
  --color-input-border-hover: #B6C3D3;
  --color-input-border-focus: #161D28;
  --color-input-border-error: #FF7A00;
  --color-input-border-disabled: #E6EAF0;

  /* --- Card --- */
  --color-card-surface-default: #FFFFFF;
  --color-card-surface-hover: #FAFAFA;
  --color-card-surface-muted: #F7F8FA;
  --color-card-border-default: #D6DDE6;
  --color-card-border-hover: #B6C3D3;
  --color-card-border-focus: #161D28;

  /* --- Nav link --- */
  --color-nav-link-text-default: #4B5563;
  --color-nav-link-text-hover: #0B0F16;
  --color-nav-link-text-active: #161D28;
  --color-nav-link-surface-hover: #F5F5F6;
  --color-nav-link-indicator: #A6FF4D;

  /* --- Link --- */
  --color-link-text-default: #161D28;
  --color-link-text-hover: #040507;
  --color-link-text-visited: #111214;

  /* --- Feedback — info --- */
  --color-feedback-info-surface: #E2E2E3;
  --color-feedback-info-text: #0B0F16;
  --color-feedback-info-border: #52555A;
  --color-feedback-info-icon: #0B0F16;

  /* --- Feedback — success --- */
  --color-feedback-success-surface: #E8FBF0;
  --color-feedback-success-text: #3DDC84;
  --color-feedback-success-border: #75E4A7;
  --color-feedback-success-icon: #3DDC84;

  /* --- Feedback — warning --- */
  --color-feedback-warning-surface: #FFFDFD;
  --color-feedback-warning-text: #FFF1EC;
  --color-feedback-warning-border: #FDF3F0;
  --color-feedback-warning-icon: #FFF1EC;

  /* --- Feedback — danger --- */
  --color-feedback-danger-surface: #FFEFE0;
  --color-feedback-danger-text: #FF7A00;
  --color-feedback-danger-border: #FDA04B;
  --color-feedback-danger-icon: #FF7A00;

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
| activity-card | `color.Critical Ember→background`, `spacing.12→padding`, `radius.md→radius`, `font:Noto Sans KR` |
| app-shell | `color.Controller Slate→surface`, `color.XP Lime→emphasis`, `color.Critical Ember→background`, `spacing.12→padding`, `radius.md→radius`, `font:Noto Sans KR` |
| autocomplete | `color.Controller Slate→surface`, `color.XP Lime→emphasis`, `color.Critical Ember→background`, `spacing.12→padding`, `radius.md→radius`, `font:Noto Sans KR` |
| back-button | `color.Controller Slate→surface`, `color.XP Lime→emphasis`, `color.Critical Ember→background`, `spacing.12→padding`, `radius.md→radius`, `font:Noto Sans KR` |
| block-controls | `color.Critical Ember→background`, `spacing.12→padding`, `radius.md→radius`, `font:Noto Sans KR` |
| bottom-sheet | `color.Controller Slate→surface`, `color.XP Lime→emphasis`, `color.Critical Ember→background`, `spacing.12→padding`, `radius.md→radius`, `font:Noto Sans KR` |
| breadcrumb | `color.Controller Slate→surface`, `color.XP Lime→emphasis`, `color.Critical Ember→background`, `spacing.12→padding`, `radius.md→radius`, `font:Noto Sans KR` |
| byline-row | `color.Critical Ember→background`, `spacing.12→padding`, `radius.md→radius`, `font:Noto Sans KR` |
| chart-container | `color.Critical Ember→background`, `spacing.12→padding`, `radius.md→radius`, `font:Noto Sans KR` |
| chart-legend | `color.Critical Ember→background`, `spacing.12→padding`, `radius.md→radius`, `font:Noto Sans KR` |
| chart-tooltip | `color.Controller Slate→surface`, `color.XP Lime→emphasis`, `color.Critical Ember→background`, `spacing.12→padding`, `radius.md→radius`, `font:Noto Sans KR` |
| chat-panel | `color.Controller Slate→surface`, `color.XP Lime→emphasis`, `color.Critical Ember→background`, `spacing.12→padding`, `radius.md→radius`, `font:Noto Sans KR` |
| checkbox | `color.Controller Slate→surface`, `color.XP Lime→emphasis`, `color.Critical Ember→background`, `spacing.12→padding`, `radius.md→radius`, `font:Noto Sans KR` |
| chip | `color.Controller Slate→surface`, `color.XP Lime→emphasis`, `color.Critical Ember→background`, `spacing.12→padding`, `radius.md→radius`, `font:Noto Sans KR` |
| column-header | `color.Critical Ember→background`, `spacing.12→padding`, `radius.md→radius`, `font:Noto Sans KR` |
| command-palette | `color.Controller Slate→surface`, `color.XP Lime→emphasis`, `color.Critical Ember→background`, `spacing.12→padding`, `radius.md→radius`, `font:Noto Sans KR` |
| command-result-item | `color.Controller Slate→surface`, `color.XP Lime→emphasis`, `color.Critical Ember→background`, `spacing.12→padding`, `radius.md→radius`, `font:Noto Sans KR` |
| comment-input | `color.Controller Slate→surface`, `color.XP Lime→emphasis`, `color.Critical Ember→background`, `spacing.12→padding`, `radius.md→radius`, `font:Noto Sans KR` |
| comment-thread | `color.Critical Ember→background`, `spacing.12→padding`, `radius.md→radius`, `font:Noto Sans KR` |
| content-card | `color.Critical Ember→background`, `spacing.12→padding`, `radius.md→radius`, `font:Noto Sans KR` |
| content-meta | `color.Critical Ember→background`, `spacing.12→padding`, `radius.md→radius`, `font:Noto Sans KR` |
| context-drawer | `color.Controller Slate→surface`, `color.XP Lime→emphasis`, `color.Critical Ember→background`, `spacing.12→padding`, `radius.md→radius`, `font:Noto Sans KR` |
| context-panel | `color.Controller Slate→surface`, `color.XP Lime→emphasis`, `color.Critical Ember→background`, `spacing.12→padding`, `radius.md→radius`, `font:Noto Sans KR` |
| cta-button | `color.Controller Slate→surface`, `color.XP Lime→emphasis`, `color.Critical Ember→background`, `spacing.12→padding`, `radius.md→radius`, `font:Noto Sans KR` |
| data-table | `color.Critical Ember→background`, `spacing.12→padding`, `radius.md→radius`, `font:Noto Sans KR` |
| editor-canvas | `color.Critical Ember→background`, `spacing.12→padding`, `radius.md→radius`, `font:Noto Sans KR` |
| editor-toolbar | `color.Critical Ember→background`, `spacing.12→padding`, `radius.md→radius`, `font:Noto Sans KR` |
| empty-state | `color.Critical Ember→background`, `spacing.12→padding`, `radius.md→radius`, `font:Noto Sans KR` |
| feature-card | `color.Critical Ember→background`, `spacing.12→padding`, `radius.md→radius`, `font:Noto Sans KR` |
| feature-comparison | `color.Critical Ember→background`, `spacing.12→padding`, `radius.md→radius`, `font:Noto Sans KR` |
| feature-description | `color.Critical Ember→background`, `spacing.12→padding`, `radius.md→radius`, `font:Noto Sans KR` |
| feature-grid | `color.Critical Ember→background`, `spacing.12→padding`, `radius.md→radius`, `font:Noto Sans KR` |
| feature-icon | `color.Critical Ember→background`, `spacing.12→padding`, `radius.md→radius`, `font:Noto Sans KR` |
| feature-section | `color.Critical Ember→background`, `spacing.12→padding`, `radius.md→radius`, `font:Noto Sans KR` |
| feature-title | `color.Critical Ember→background`, `spacing.12→padding`, `radius.md→radius`, `font:Noto Sans KR` |
| featured-story-card | `color.Critical Ember→background`, `spacing.12→padding`, `radius.md→radius`, `font:Noto Sans KR` |
| filter-chip | `color.Controller Slate→surface`, `color.XP Lime→emphasis`, `color.Critical Ember→background`, `spacing.12→padding`, `radius.md→radius`, `font:Noto Sans KR` |
| filter-panel | `color.Controller Slate→surface`, `color.XP Lime→emphasis`, `color.Critical Ember→background`, `spacing.12→padding`, `radius.md→radius`, `font:Noto Sans KR` |
| filter-toolbar | `color.Critical Ember→background`, `spacing.12→padding`, `radius.md→radius`, `font:Noto Sans KR` |
| form-actions | `color.Controller Slate→surface`, `color.XP Lime→emphasis`, `color.Critical Ember→background`, `spacing.12→padding`, `radius.md→radius`, `font:Noto Sans KR` |
| form-section | `color.Controller Slate→surface`, `color.XP Lime→emphasis`, `color.Critical Ember→background`, `spacing.12→padding`, `radius.md→radius`, `font:Noto Sans KR` |
| ghost-button | `color.Controller Slate→surface`, `color.XP Lime→emphasis`, `color.Critical Ember→background`, `spacing.12→padding`, `radius.md→radius`, `font:Noto Sans KR` |
| hero-container | `color.Critical Ember→background`, `spacing.12→padding`, `radius.md→radius`, `font:Noto Sans KR` |
| hero-cta-group | `color.Controller Slate→surface`, `color.XP Lime→emphasis`, `color.Critical Ember→background`, `spacing.12→padding`, `radius.md→radius`, `font:Noto Sans KR` |
| hero-eyebrow | `color.Critical Ember→background`, `spacing.12→padding`, `radius.md→radius`, `font:Noto Sans KR` |
| hero-headline | `color.Critical Ember→background`, `spacing.12→padding`, `radius.md→radius`, `font:Noto Sans KR` |
| hero-subheadline | `color.Critical Ember→background`, `spacing.12→padding`, `radius.md→radius`, `font:Noto Sans KR` |
| hero-trust-strip | `color.Critical Ember→background`, `spacing.12→padding`, `radius.md→radius`, `font:Noto Sans KR` |
| hero-visual | `color.Critical Ember→background`, `spacing.12→padding`, `radius.md→radius`, `font:Noto Sans KR` |
| icon-button | `color.Controller Slate→surface`, `color.XP Lime→emphasis`, `color.Critical Ember→background`, `spacing.12→padding`, `radius.md→radius`, `font:Noto Sans KR` |
| inline-alert | `color.Critical Ember→background`, `spacing.12→padding`, `radius.md→radius`, `font:Noto Sans KR` |
| inline-format-menu | `color.Critical Ember→background`, `spacing.12→padding`, `radius.md→radius`, `font:Noto Sans KR` |
| insight-card | `color.Critical Ember→background`, `spacing.12→padding`, `radius.md→radius`, `font:Noto Sans KR` |
| link-button | `color.Controller Slate→surface`, `color.XP Lime→emphasis`, `color.Critical Ember→background`, `spacing.12→padding`, `radius.md→radius`, `font:Noto Sans KR` |
| mention-popup | `color.Controller Slate→surface`, `color.XP Lime→emphasis`, `color.Critical Ember→background`, `spacing.12→padding`, `radius.md→radius`, `font:Noto Sans KR` |
| message-composer | `color.Controller Slate→surface`, `color.XP Lime→emphasis`, `color.Critical Ember→background`, `spacing.12→padding`, `radius.md→radius`, `font:Noto Sans KR` |
| message-thread | `color.Controller Slate→surface`, `color.XP Lime→emphasis`, `color.Critical Ember→background`, `spacing.12→padding`, `radius.md→radius`, `font:Noto Sans KR` |
| mobile-tab-bar | `color.Controller Slate→surface`, `color.XP Lime→emphasis`, `color.Critical Ember→background`, `spacing.12→padding`, `radius.md→radius`, `font:Noto Sans KR` |
| mobile-topbar | `color.Controller Slate→surface`, `color.XP Lime→emphasis`, `color.Critical Ember→background`, `spacing.12→padding`, `radius.md→radius`, `font:Noto Sans KR` |
| modal-dialog | `color.Controller Slate→surface`, `color.XP Lime→emphasis`, `color.Critical Ember→background`, `spacing.12→padding`, `radius.md→radius`, `font:Noto Sans KR` |
| pagination | `color.Controller Slate→surface`, `color.XP Lime→emphasis`, `color.Critical Ember→background`, `spacing.12→padding`, `radius.md→radius`, `font:Noto Sans KR` |
| pricing-card | `color.Critical Ember→background`, `spacing.12→padding`, `radius.md→radius`, `font:Noto Sans KR` |
| primary-button | `color.Controller Slate→surface`, `color.XP Lime→emphasis`, `color.Critical Ember→background`, `spacing.12→padding`, `radius.md→radius`, `font:Noto Sans KR` |
| radio-group | `color.Controller Slate→surface`, `color.XP Lime→emphasis`, `color.Critical Ember→background`, `spacing.12→padding`, `radius.md→radius`, `font:Noto Sans KR` |
| row-actions | `color.Critical Ember→background`, `spacing.12→padding`, `radius.md→radius`, `font:Noto Sans KR` |
| search-field | `color.Controller Slate→surface`, `color.XP Lime→emphasis`, `color.Critical Ember→background`, `spacing.12→padding`, `radius.md→radius`, `font:Noto Sans KR` |
| search-results | `color.Critical Ember→background`, `spacing.12→padding`, `radius.md→radius`, `font:Noto Sans KR` |
| secondary-button | `color.Controller Slate→surface`, `color.XP Lime→emphasis`, `color.Critical Ember→background`, `spacing.12→padding`, `radius.md→radius`, `font:Noto Sans KR` |
| section-header | `color.Critical Ember→background`, `spacing.12→padding`, `radius.md→radius`, `font:Noto Sans KR` |
| section-tabs | `color.Controller Slate→surface`, `color.XP Lime→emphasis`, `color.Critical Ember→background`, `spacing.12→padding`, `radius.md→radius`, `font:Noto Sans KR` |
| segmented-control | `color.Controller Slate→surface`, `color.XP Lime→emphasis`, `color.Critical Ember→background`, `spacing.12→padding`, `radius.md→radius`, `font:Noto Sans KR` |
| select | `color.Controller Slate→surface`, `color.XP Lime→emphasis`, `color.Critical Ember→background`, `spacing.12→padding`, `radius.md→radius`, `font:Noto Sans KR` |
| shortcut-hint | `color.Critical Ember→background`, `spacing.12→padding`, `radius.md→radius`, `font:Noto Sans KR` |
| sidebar-nav | `color.Controller Slate→surface`, `color.XP Lime→emphasis`, `color.Critical Ember→background`, `spacing.12→padding`, `radius.md→radius`, `font:Noto Sans KR` |
| slash-command-menu | `color.Critical Ember→background`, `spacing.12→padding`, `radius.md→radius`, `font:Noto Sans KR` |
| stat-card | `color.Critical Ember→background`, `spacing.12→padding`, `radius.md→radius`, `font:Noto Sans KR` |
| status-badge | `color.Critical Ember→background`, `spacing.12→padding`, `radius.md→radius`, `font:Noto Sans KR` |
| tab-bar | `color.Controller Slate→surface`, `color.XP Lime→emphasis`, `color.Critical Ember→background`, `spacing.12→padding`, `radius.md→radius`, `font:Noto Sans KR` |
| tag | `color.Critical Ember→background`, `spacing.12→padding`, `radius.md→radius`, `font:Noto Sans KR` |
| text-field | `color.Controller Slate→surface`, `color.XP Lime→emphasis`, `color.Critical Ember→background`, `spacing.12→padding`, `radius.md→radius`, `font:Noto Sans KR` |
| textarea | `color.Controller Slate→surface`, `color.XP Lime→emphasis`, `color.Critical Ember→background`, `spacing.12→padding`, `radius.md→radius`, `font:Noto Sans KR` |
| toast | `color.Critical Ember→background`, `spacing.12→padding`, `radius.md→radius`, `font:Noto Sans KR` |
| topbar | `color.Controller Slate→surface`, `color.XP Lime→emphasis`, `color.Critical Ember→background`, `spacing.12→padding`, `radius.md→radius`, `font:Noto Sans KR` |
| upgrade-banner | `color.Critical Ember→background`, `spacing.12→padding`, `radius.md→radius`, `font:Noto Sans KR` |
| workspace-switcher | `color.Controller Slate→surface`, `color.XP Lime→emphasis`, `color.Critical Ember→background`, `spacing.12→padding`, `radius.md→radius`, `font:Noto Sans KR` |

## 19. Contrast Audit

| Background | Foreground | Ratio | Level |
|------------|------------|-------|-------|
| Controller Slate | Paper | 16.93:1 | AAA (pass) |
| XP Lime | Ink | 15.32:1 | AAA (pass) |
| Controller Slate | XP Lime | 13.73:1 | AAA (pass) |
| Critical Ember | Ink | 6.09:1 | AA (pass) |
| Controller Slate | Critical Ember | 5.46:1 | AA (pass) |
| Critical Ember | Paper | 3.10:1 | AA-large (large-only) |
| XP Lime | Critical Ember | 2.52:1 | fail (FAIL) |
| XP Lime | Paper | 1.23:1 | fail (FAIL) |
| Controller Slate | Ink | 1.12:1 | fail (FAIL) |

## 20. Pattern Catalog

### Layout Patterns

- **hero spotlight**: —
- **review cards**: —
- **score badges**: —
- **comparison tables**: —
- **ranking lists**: —
- **release calendar**: —
- **workspace navigation**: app-shell, sidebar-nav, topbar, breadcrumb, workspace-switcher, tab-bar, context-panel
- **dashboard cards**: stat-card, insight-card, activity-card, section-header
- **data tables**: data-table, column-header, filter-chip, row-actions, pagination, filter-toolbar

### Interaction Patterns

- **platform filters**: —
- **search and autocomplete**: —
- **command palette**: command-palette, command-result-item, shortcut-hint
- **forms**: text-field, select, checkbox, textarea, form-section, radio-group, form-actions
- **notifications**: toast, inline-alert, empty-state
