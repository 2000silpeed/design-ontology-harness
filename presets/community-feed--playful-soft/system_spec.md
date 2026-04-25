# Bloom System Spec

## 1. Positioning

- **Brand**: Bloom
- **Product**: 친근한 소셜 피드 · 스레드 · 프레즌스 · 알림 — playful-soft 톤 커뮤니티 앱
- **Audience**: 친구/이웃과 가볍게 근황을 나누는 일반 사용자, 팬덤·취미 커뮤니티에서 글·이미지·코멘트를 주고받는 크리에이터, 관심사 기반 마이크로 커뮤니티 운영자
- **Platforms**: web, mobile-web
- **Accessibility floor**: WCAG 2.2 AA

## 2. Identity Guardrails

- **Brand keywords**: community-feed, social, feed, thread, presence, notification, friendly, rounded, playful, pastel
- **Anti-keywords**: corporate, enterprise, sharp, dense, monochrome, utilitarian, minimal-tech, magazine-serif, industrial
- **Tone of voice**: friendly, warm, approachable, light-hearted, conversational
- **Visual direction**: rounded corners, pastel surfaces, soft shadows, warm accent, friendly avatar, reaction bubble, presence dot, notification badge, loose spacing, illustrated empty state
- **Interaction direction**: pull-to-refresh, optimistic reaction, quick reply, emoji picker, presence indicator, follow toggle, notification center, swipe archive, mention autocomplete, soft dialog

## 3. Design Principles

- **Community-Feed**: `community-feed`를 시각적 선택과 인터랙션 선택의 기본 기준으로 삼습니다.
- **Social**: `social`를 시각적 선택과 인터랙션 선택의 기본 기준으로 삼습니다.
- **Feed**: `feed`를 시각적 선택과 인터랙션 선택의 기본 기준으로 삼습니다.
- **Thread**: `thread`를 시각적 선택과 인터랙션 선택의 기본 기준으로 삼습니다.

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

- **Heading**: SUIT
- **Body**: SUIT
- **Korean**: SUIT
- **Product type detected**: mobile
- **Pairing source**: auto-scored
- **Line height**: comfortable
- **Type scale**: base 14px, ratio 1.2 (xs=11px, sm=12px, md=14px, lg=17px, xl=20px, 2xl=24px, 3xl=29px)
- **Strategy**:
  - 단일 서체(SUIT)로 weight 대비 위계 — 일관성 우선
  - 한글 서체: SUIT — 라틴과 x-height/weight 조화
- **Heading note**: Pretendard 계열이지만 더 둥글고 부드러운 한글 서체.
- **Body note**: Pretendard 계열이지만 더 둥글고 부드러운 한글 서체.
- **Korean rationale**: SUIT — Pretendard보다 부드럽고 친근한 인상. 교육, 라이프스타일, 커뮤니티 서비스에 적합.
- **Heading tracking**: xl=-0.01em, 2xl=-0.01em, 3xl=-0.01em
- **Primary script**: korean
- **Hangul headline defaults**: SUIT | line-height 1.25-1.35 | tracking 0em
- **Hangul body defaults**: SUIT | line-height 1.6-1.7 | label line-height 1.4-1.5
- **Wrap defaults**: headline word-break=keep-all, headline text-wrap=balance, body word-break=keep-all
- **Scale guidance**: 기본 스케일을 사용할 수 있지만 한글 문장 기준으로 실제 wrap을 먼저 검증한다.
- **Hangul warning**: 기관/금융 — 너무 캐주얼할 수 있음
- **Hangul warning**: 기관/금융 — 너무 캐주얼할 수 있음
- **Loading**: SUIT(preload) | display: swap

## 6. Color Reference

- **Source**: REFERENCE X Vol.1 - Color Reference (/Users/sungwoon/ai-projects/design-ontology-harness/docs/color-reference.md)
- **Selection mode**: manual
- **Preferred families**: Pastel Oranges, Pastel Reds, Pastel Greens, Pastel Yellows
- **Palette strategy**: temperature=warm, contrast=soft, diversity=balanced, surface_style=tinted
- **Palette expansion**: supporting_color_count=10, combination_count=3, prefer_pairings=True
- **Palette roles**:
  - `primary` -> Coral Blush #F88379 / Pastel Oranges
  - `accent` -> Mint Green #98FF98 / Pastel Greens
  - `surface_tint` -> Cornsilk #FFF8DC / Pastel Yellows
- **Selected colors**:
  - Salmon #FA8072 / Pastel Reds / 밝고 따뜻한 핑크 오렌지 톤 / 따뜻함, 부드러움, 친근함, 자연스러움
  - Peach Puff #FFDAB9 / Pastel Oranges / 고명도, 저채도, 오렌지와 핑크 사이의 파스텔 계열 / 따뜻함, 부드러움, 순수함, 친근함, 생기
  - Buttercream #F3E5AB / Pastel Yellows / 고명도, 저채도, 크리미한 웜 옐로 톤 / 부드러움, 따뜻함, 포근함, 달콤함
- **Palette candidates**:
  - signature-1 (Signature): primary=Salmon, accent=Peach Puff, surface_tint=Buttercream / Salmon is inside preferred families.; Peach Puff is inside preferred families.
  - soft-spread-2 (Soft Spread): primary=Apricot, accent=Salmon, surface_tint=Peach Puff / Apricot matches brand tone keywords.; Salmon is inside preferred families.
- **Expanded supporting colors**:
  - Peach Puff #FFDAB9 / Pastel Oranges / reference-color / Peach Puff stays inside the preferred families.; Peach Puff reinforces the brand mood signals.
  - Salmon #FA8072 / Pastel Reds / reference-color / Salmon stays inside the preferred families.; Salmon reinforces the brand mood signals.
  - Creamsicle #FFD7A0 / Pastel Oranges / reference-color / Creamsicle stays inside the preferred families.; Creamsicle reinforces the brand mood signals.
  - Buttercream #F3E5AB / Pastel Yellows / reference-color / Buttercream stays inside the preferred families.; Buttercream reinforces the brand mood signals.
  - Apricot #FFB27F / Natural Oranges / reference-color / Apricot reinforces the brand mood signals.
  - Celadon #ACE1AF / Pastel Greens / reference-color / Celadon stays inside the preferred families.; Celadon reinforces the brand mood signals.
  - Naples Yellow #FADA5E / Pastel Yellows / reference-color / Naples Yellow stays inside the preferred families.; Naples Yellow reinforces the brand mood signals.
  - Blush #F9C0C4 / Pastel Reds / reference-color / Blush stays inside the preferred families.; Blush reinforces the brand mood signals.
- **Expanded semantic roles**:
  - `brand_primary` -> Coral Blush #F88379 / Pastel Oranges
  - `brand_accent` -> Mint Green #98FF98 / Pastel Greens
  - `surface_tint` -> Cornsilk #FFF8DC / Pastel Yellows
  - `canvas` -> Canvas White #F7F8FA / Generated Fallback
  - `surface` -> Paper #FFFFFF / Generated Fallback
  - `surface_muted` -> Surface Muted #EEF1F6 / Generated Fallback
  - `surface_elevated` -> Paper #FFFFFF / Generated Fallback
  - `border` -> Border Neutral #D6DDE6 / Generated Fallback
  - `border_strong` -> Pairing #B8A79A #B8A79A / Derived Pairing
  - `ink` -> Ink #111111 / Generated Fallback
- **Combination lists**:
  - Seed Core: primary=Coral Blush, accent=Mint Green, surface_tint=Cornsilk
  - Surface System: canvas=Canvas White, surface=Paper, surface_tint=Cornsilk, border=Border Neutral, ink=Ink, ink_muted=Muted Ink
  - Support Spectrum: support=Peach Puff, support=Salmon, support=Creamsicle, support=Buttercream, support=Apricot, support=Celadon
- **Notes**: Coral Blush 를 primary 로 — 따뜻한 파스텔, 친근/명랑 톤 1급, Mint Green accent — reaction/presence dot 쿨 파스텔 보색, Cornsilk 는 surface_tint — 크리미 웜 배경, 장시간 피드 열람 피로감 최소화, light mode 가 기본 — 친근 소셜 피드 관례, dark 는 옵션으로 제공, minimal-tech / corporate-trust 와 정반대 방향 — warm + rounded + pastel
- **Application rule**: 레퍼런스 컬러는 semantic token으로 번역해서 사용하고, 접근성과 theme 호환성을 우선합니다.

## 7. Visual Reference Signals

- **Mode**: local-images
- **Coverage**: source 0 / image 0 / selected 0
- **Rule**: visual references are advisory signals for motif and layout direction; official KB/spec remain the structural source of truth.
- **Provenance**: `observed` = directly measured from local pixels, `inferred` = synthesized from image/query/brand signals, `unverified` = reliable visual evidence not yet available.
- **Query seeds**: threads social feed, bluesky timeline, mastodon community feed, tumblr playful feed
### Visual Direction

- **Density**: airy (confidence 0.45, provenance inferred) / editorial x1, hero x1
- **Surface Style**: tinted (confidence 0.54, provenance inferred) / warm x2, editorial x1, soft x4
- **Corner Style**: round (confidence 0.94, provenance inferred) / rounded x3, soft x4
- **Typography Mood**: editorial (confidence 0.71, provenance inferred) / editorial x1, magazine x2, serif x2
- **Color balance**: temperature=unknown, contrast=unknown, neutral_bias=unknown, provenance=unverified

### Layout Rhythm

- **Editorial feed**: confidence 0.94 / provenance inferred / editorial x1, feed x8, magazine x2
- **Data review surface**: confidence 0.71 / provenance inferred / table x1, grid x1, data x1, timeline x2
- **Conversation side panel**: confidence 0.56 / provenance inferred / thread x3
- **Narrative landing flow**: confidence 0.4 / provenance inferred / hero x1

### Image-derived Component Hints

- **Cards**: low-elevation tinted cards를 기본으로 하고, 넓은 내부 여백과 강한 section breathing room. soft round corner를 기본값으로 유지. / provenance inferred / surface=tinted, density=airy, corner=round
- **Navigation**: navigation은 정보 구조를 안정적으로 고정하고 시각적 장식보다 위치 신호를 우선한다. / provenance inferred / Editorial feed
- **Typography**: headline rhythm과 본문 리듬의 대비를 키우고, label/metadata는 조용하게 유지한다. / provenance inferred / typography_mood=editorial
- **Data Display**: 정보 밀도를 유지하되 thin dividers와 restrained accent로 hierarchy를 만든다. / provenance inferred / layout=data-review-surface, density=airy

### Synthesis Notes

- layout는 Editorial feed 기준으로 정리
- surface language는 tinted 성향 우선
- typography mood는 editorial 축 유지
- density는 airy 기준으로 primitive spacing 조정
- palette temperature는 unknown 쪽을 우선
- Avoid: dense data table
- Avoid: alert-first severity grid
- Avoid: magazine serif hero
- Avoid: corporate navy surfaces

## 8. Component Strategy

- **Product primitives**: feed item, post card, thread view, reply composer, comment thread, reaction bar, follow button, presence indicator, notification center, notification item, avatar cluster, timeline stream, mention highlight, tag pill, share sheet, empty-feed illustration, gentle toast, soft dialog
- **Required families**: button, data-display, editorial, feedback, input, navigation, overlay, social
- **Visual-reference archetypes**:

- **Editorial content block** (editorial / 0.94): content-card, featured-story-card, section-header, content-meta, byline-row
- **Data review table** (data-display / 0.8): data-table, column-header, row-actions, filter-toolbar, pagination
- **Marketing hero stack** (marketing / 0.51): hero-section, hero-headline, hero-visual, cta-button-group, trust-strip

- **button**: primary-button, secondary-button, ghost-button, icon-button, cta-button, link-button, follow-button, form-actions
- **data-display**: tag-pill, comment-thread, notification-item, mention-highlight, tag, avatar, profile-card, search-results / visual signals: Data review table (0.8)
- **editorial**: editor-canvas, editor-toolbar, inline-format-menu, slash-command-menu, block-controls, content-card, featured-story-card, content-meta / visual signals: Editorial content block (0.94)
- **feedback**: inline-alert, empty-state, toast, empty-feed-illustration, gentle-toast, banner, status-badge, shortcut-hint
- **input**: text-field, search-field, segmented-control, reply-composer, comment-input, chip, textarea, select
- **navigation**: mobile-topbar, mobile-tab-bar, back-button, section-tabs, pagination, app-shell, sidebar-nav, topbar
- **overlay**: bottom-sheet, modal-dialog, share-sheet, soft-dialog, mention-popup, notification-center, user-menu, confirm-dialog
- **social**: feed-item, post-card, thread-view, reaction-bar, timeline-stream, avatar-cluster, presence-indicator

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

이 문서는 **Bloom System**의 디자인 시스템 사양입니다.

### 시작하기

1. **토큰 적용**: Drop-in CSS(아래 섹션 16)의 CSS 변수를 프로젝트에 복사합니다.
2. **컬러 세팅**: Color Reference(섹션 6)의 semantic role을 기준으로 surface/text/border를 잡습니다.
3. **타이포 세팅**: Token Strategy(섹션 5)의 font family와 type scale을 적용합니다.
4. **시각 방향 확인**: Visual Reference Signals(섹션 7)에서 density/surface/layout cue를 먼저 확인합니다.
5. **컴포넌트 구현**: Component Strategy(섹션 8)의 family 순서대로 하나씩 빌드합니다.

### 우선순위

핵심 primitive: **feed item, post card, thread view, reply composer, comment thread**

이 primitive를 지원하는 컴포넌트부터 구현하고, 나머지는 필요에 따라 확장합니다.

## 15. DO / DON'T

### DO

- **Community-Feed**: community-feed와 충돌하는 컴포넌트 변형은 만들지 않기
- **Social**: social와 충돌하는 컴포넌트 변형은 만들지 않기
- **Feed**: feed와 충돌하는 컴포넌트 변형은 만들지 않기
- **Thread**: thread와 충돌하는 컴포넌트 변형은 만들지 않기
- 모든 시각적 선택에서 **community-feed, social, feed** 기준을 적용
- semantic token을 통해 컬러를 적용 (하드코딩 금지)
- 접근성 기준을 모든 text/surface 조합에서 먼저 검증
- 컴포넌트 변형 추가 전 기존 variant로 해결 가능한지 먼저 확인
- 아이콘은 SVG 컴포넌트 또는 Lucide/Heroicons/Phosphor/Tabler 등 라이브러리로 구현
- component_specs.md의 anatomy/states/token binding을 그대로 따라 완전히 구현

### DON'T

- **corporate** 방향의 디자인 결정을 하지 않음
- **enterprise** 방향의 디자인 결정을 하지 않음
- **sharp** 방향의 디자인 결정을 하지 않음
- **dense** 방향의 디자인 결정을 하지 않음
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
  --font-heading: 'SUIT', serif;
  --font-body: 'SUIT', sans-serif;
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
  --color-primary: #F88379;
  --color-accent: #98FF98;
  --color-surface-tint: #FFF8DC;

  /* --- Semantic roles (expanded) --- */
  --color-brand-primary: #F88379;
  --color-brand-accent: #98FF98;
  --color-surface-tint: #FFF8DC;
  --color-canvas: #F7F8FA;
  --color-surface: #FFFFFF;
  --color-surface-muted: #EEF1F6;
  --color-surface-elevated: #FFFFFF;
  --color-border: #D6DDE6;
  --color-border-strong: #B8A79A;
  --color-ink: #111111;
  --color-ink-muted: #4B5563;
  --color-ink-subtle: #6B7280;
  --color-ink-inverse: #FFFFFF;
  --color-primary-support: #FFDAB9;
  --color-accent-support: #ACE1AF;
  --color-info: #B0E0E6;
  --color-success: #ACE1AF;
  --color-warning: #FFDAB9;
  --color-danger: #FA8072;
  --color-link: #F88379;
  --color-link-hover: #F65F52;

  /* --- Button — primary --- */
  --color-button-primary-surface-default: #F88379;
  --color-button-primary-surface-hover: #F6685C;
  --color-button-primary-surface-active: #F55649;
  --color-button-primary-surface-disabled: #F7C9C6;
  --color-button-primary-text-default: #111111;
  --color-button-primary-text-disabled: #848486;
  --color-button-primary-border-default: #F88379;
  --color-button-primary-focus-ring: #F88379;

  /* --- Button — secondary --- */
  --color-button-secondary-surface-default: #FFFFFF;
  --color-button-secondary-surface-hover: #F1F1F1;
  --color-button-secondary-surface-active: #E7E7E7;
  --color-button-secondary-surface-disabled: #F7F8FA;
  --color-button-secondary-text-default: #111111;
  --color-button-secondary-text-disabled: #909091;
  --color-button-secondary-border-default: #BDC8D7;
  --color-button-secondary-border-hover: #A3B3C7;
  --color-button-secondary-focus-ring: #F88379;

  /* --- Button — ghost --- */
  --color-button-ghost-surface-default: transparent;
  --color-button-ghost-surface-hover: #F3F3F3;
  --color-button-ghost-surface-active: #EAEAEA;
  --color-button-ghost-surface-disabled: transparent;
  --color-button-ghost-text-default: #4B5563;
  --color-button-ghost-text-hover: #111111;
  --color-button-ghost-text-disabled: #AAAFB6;
  --color-button-ghost-border-default: transparent;
  --color-button-ghost-focus-ring: #F88379;

  /* --- Button — danger --- */
  --color-button-danger-surface-default: #FA8072;
  --color-button-danger-surface-hover: #F96554;
  --color-button-danger-surface-active: #F85441;
  --color-button-danger-text-default: #111111;
  --color-button-danger-border-default: #FA8072;
  --color-button-danger-focus-ring: #FA8072;

  /* --- Input --- */
  --color-input-surface-default: #FFFFFF;
  --color-input-surface-filled: #FFFFFF;
  --color-input-surface-disabled: #F7F8FA;
  --color-input-text-default: #111111;
  --color-input-text-placeholder: #90969F;
  --color-input-text-disabled: #AAAFB6;
  --color-input-border-default: #D6DDE6;
  --color-input-border-hover: #B6C3D3;
  --color-input-border-focus: #F88379;
  --color-input-border-error: #FA8072;
  --color-input-border-disabled: #E6EAF0;

  /* --- Card --- */
  --color-card-surface-default: #FFFFFF;
  --color-card-surface-hover: #FAFAFA;
  --color-card-surface-muted: #F7F8FA;
  --color-card-border-default: #D6DDE6;
  --color-card-border-hover: #B6C3D3;
  --color-card-border-focus: #F88379;

  /* --- Nav link --- */
  --color-nav-link-text-default: #4B5563;
  --color-nav-link-text-hover: #111111;
  --color-nav-link-text-active: #F88379;
  --color-nav-link-surface-hover: #F5F5F5;
  --color-nav-link-indicator: #98FF98;

  /* --- Link --- */
  --color-link-text-default: #F88379;
  --color-link-text-hover: #F55649;
  --color-link-text-visited: #E67B71;

  /* --- Feedback — info --- */
  --color-feedback-info-surface: #F6FBFC;
  --color-feedback-info-text: #B0E0E6;
  --color-feedback-info-border: #C5E7EC;
  --color-feedback-info-icon: #B0E0E6;

  /* --- Feedback — success --- */
  --color-feedback-success-surface: #F5FBF5;
  --color-feedback-success-text: #ACE1AF;
  --color-feedback-success-border: #C2E8C6;
  --color-feedback-success-icon: #ACE1AF;

  /* --- Feedback — warning --- */
  --color-feedback-warning-surface: #FFFBF7;
  --color-feedback-warning-text: #FFDAB9;
  --color-feedback-warning-border: #FDE3CC;
  --color-feedback-warning-icon: #FFDAB9;

  /* --- Feedback — danger --- */
  --color-feedback-danger-surface: #FEF0EE;
  --color-feedback-danger-text: #FA8072;
  --color-feedback-danger-border: #F9A49B;
  --color-feedback-danger-icon: #FA8072;

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
| activity-card | `color.Cornsilk→background`, `spacing.12→padding`, `radius.md→radius`, `font:SUIT` |
| app-shell | `color.Coral Blush→surface`, `color.Mint Green→emphasis`, `color.Cornsilk→background`, `spacing.12→padding`, `radius.md→radius`, `font:SUIT` |
| autocomplete | `color.Coral Blush→surface`, `color.Mint Green→emphasis`, `color.Cornsilk→background`, `spacing.12→padding`, `radius.md→radius`, `font:SUIT` |
| avatar | `color.Cornsilk→background`, `spacing.12→padding`, `radius.md→radius`, `font:SUIT` |
| avatar-cluster | `color.Cornsilk→background`, `spacing.12→padding`, `radius.md→radius`, `font:SUIT` |
| back-button | `color.Coral Blush→surface`, `color.Mint Green→emphasis`, `color.Cornsilk→background`, `spacing.12→padding`, `radius.md→radius`, `font:SUIT` |
| banner | `color.Cornsilk→background`, `spacing.12→padding`, `radius.md→radius`, `font:SUIT` |
| block-controls | `color.Cornsilk→background`, `spacing.12→padding`, `radius.md→radius`, `font:SUIT` |
| bottom-sheet | `color.Coral Blush→surface`, `color.Mint Green→emphasis`, `color.Cornsilk→background`, `spacing.12→padding`, `radius.md→radius`, `font:SUIT` |
| breadcrumb | `color.Coral Blush→surface`, `color.Mint Green→emphasis`, `color.Cornsilk→background`, `spacing.12→padding`, `radius.md→radius`, `font:SUIT` |
| byline-row | `color.Cornsilk→background`, `spacing.12→padding`, `radius.md→radius`, `font:SUIT` |
| calendar-grid | `color.Cornsilk→background`, `spacing.12→padding`, `radius.md→radius`, `font:SUIT` |
| chat-input | `color.Coral Blush→surface`, `color.Mint Green→emphasis`, `color.Cornsilk→background`, `spacing.12→padding`, `radius.md→radius`, `font:SUIT` |
| chat-message | `color.Cornsilk→background`, `spacing.12→padding`, `radius.md→radius`, `font:SUIT` |
| chat-thread | `color.Cornsilk→background`, `spacing.12→padding`, `radius.md→radius`, `font:SUIT` |
| checkbox | `color.Coral Blush→surface`, `color.Mint Green→emphasis`, `color.Cornsilk→background`, `spacing.12→padding`, `radius.md→radius`, `font:SUIT` |
| chip | `color.Coral Blush→surface`, `color.Mint Green→emphasis`, `color.Cornsilk→background`, `spacing.12→padding`, `radius.md→radius`, `font:SUIT` |
| column-header | `color.Cornsilk→background`, `spacing.12→padding`, `radius.md→radius`, `font:SUIT` |
| command-palette | `color.Coral Blush→surface`, `color.Mint Green→emphasis`, `color.Cornsilk→background`, `spacing.12→padding`, `radius.md→radius`, `font:SUIT` |
| command-result-item | `color.Coral Blush→surface`, `color.Mint Green→emphasis`, `color.Cornsilk→background`, `spacing.12→padding`, `radius.md→radius`, `font:SUIT` |
| comment-input | `color.Coral Blush→surface`, `color.Mint Green→emphasis`, `color.Cornsilk→background`, `spacing.12→padding`, `radius.md→radius`, `font:SUIT` |
| comment-thread | `color.Cornsilk→background`, `spacing.12→padding`, `radius.md→radius`, `font:SUIT` |
| confirm-dialog | `color.Coral Blush→surface`, `color.Mint Green→emphasis`, `color.Cornsilk→background`, `spacing.12→padding`, `radius.md→radius`, `font:SUIT` |
| content-card | `color.Cornsilk→background`, `spacing.12→padding`, `radius.md→radius`, `font:SUIT` |
| content-meta | `color.Cornsilk→background`, `spacing.12→padding`, `radius.md→radius`, `font:SUIT` |
| cta-button | `color.Coral Blush→surface`, `color.Mint Green→emphasis`, `color.Cornsilk→background`, `spacing.12→padding`, `radius.md→radius`, `font:SUIT` |
| data-table | `color.Cornsilk→background`, `spacing.12→padding`, `radius.md→radius`, `font:SUIT` |
| date-picker | `color.Coral Blush→surface`, `color.Mint Green→emphasis`, `color.Cornsilk→background`, `spacing.12→padding`, `radius.md→radius`, `font:SUIT` |
| date-range-picker | `color.Coral Blush→surface`, `color.Mint Green→emphasis`, `color.Cornsilk→background`, `spacing.12→padding`, `radius.md→radius`, `font:SUIT` |
| editor-canvas | `color.Cornsilk→background`, `spacing.12→padding`, `radius.md→radius`, `font:SUIT` |
| editor-toolbar | `color.Cornsilk→background`, `spacing.12→padding`, `radius.md→radius`, `font:SUIT` |
| empty-feed-illustration | `color.Cornsilk→background`, `spacing.12→padding`, `radius.md→radius`, `font:SUIT` |
| empty-state | `color.Cornsilk→background`, `spacing.12→padding`, `radius.md→radius`, `font:SUIT` |
| featured-story-card | `color.Cornsilk→background`, `spacing.12→padding`, `radius.md→radius`, `font:SUIT` |
| feed-item | `color.Cornsilk→background`, `spacing.12→padding`, `radius.md→radius`, `font:SUIT` |
| filter-chip | `color.Coral Blush→surface`, `color.Mint Green→emphasis`, `color.Cornsilk→background`, `spacing.12→padding`, `radius.md→radius`, `font:SUIT` |
| filter-panel | `color.Coral Blush→surface`, `color.Mint Green→emphasis`, `color.Cornsilk→background`, `spacing.12→padding`, `radius.md→radius`, `font:SUIT` |
| filter-toolbar | `color.Cornsilk→background`, `spacing.12→padding`, `radius.md→radius`, `font:SUIT` |
| follow-button | `color.Coral Blush→surface`, `color.Mint Green→emphasis`, `color.Cornsilk→background`, `spacing.12→padding`, `radius.md→radius`, `font:SUIT` |
| form-actions | `color.Coral Blush→surface`, `color.Mint Green→emphasis`, `color.Cornsilk→background`, `spacing.12→padding`, `radius.md→radius`, `font:SUIT` |
| form-section | `color.Coral Blush→surface`, `color.Mint Green→emphasis`, `color.Cornsilk→background`, `spacing.12→padding`, `radius.md→radius`, `font:SUIT` |
| gentle-toast | `color.Cornsilk→background`, `spacing.12→padding`, `radius.md→radius`, `font:SUIT` |
| ghost-button | `color.Coral Blush→surface`, `color.Mint Green→emphasis`, `color.Cornsilk→background`, `spacing.12→padding`, `radius.md→radius`, `font:SUIT` |
| icon-button | `color.Coral Blush→surface`, `color.Mint Green→emphasis`, `color.Cornsilk→background`, `spacing.12→padding`, `radius.md→radius`, `font:SUIT` |
| inline-alert | `color.Cornsilk→background`, `spacing.12→padding`, `radius.md→radius`, `font:SUIT` |
| inline-format-menu | `color.Cornsilk→background`, `spacing.12→padding`, `radius.md→radius`, `font:SUIT` |
| insight-card | `color.Cornsilk→background`, `spacing.12→padding`, `radius.md→radius`, `font:SUIT` |
| kanban-board | `color.Cornsilk→background`, `spacing.12→padding`, `radius.md→radius`, `font:SUIT` |
| kanban-card | `color.Cornsilk→background`, `spacing.12→padding`, `radius.md→radius`, `font:SUIT` |
| kanban-column | `color.Cornsilk→background`, `spacing.12→padding`, `radius.md→radius`, `font:SUIT` |
| link-button | `color.Coral Blush→surface`, `color.Mint Green→emphasis`, `color.Cornsilk→background`, `spacing.12→padding`, `radius.md→radius`, `font:SUIT` |
| mention-highlight | `color.Cornsilk→background`, `spacing.12→padding`, `radius.md→radius`, `font:SUIT` |
| mention-popup | `color.Coral Blush→surface`, `color.Mint Green→emphasis`, `color.Cornsilk→background`, `spacing.12→padding`, `radius.md→radius`, `font:SUIT` |
| mobile-tab-bar | `color.Coral Blush→surface`, `color.Mint Green→emphasis`, `color.Cornsilk→background`, `spacing.12→padding`, `radius.md→radius`, `font:SUIT` |
| mobile-topbar | `color.Coral Blush→surface`, `color.Mint Green→emphasis`, `color.Cornsilk→background`, `spacing.12→padding`, `radius.md→radius`, `font:SUIT` |
| modal-dialog | `color.Coral Blush→surface`, `color.Mint Green→emphasis`, `color.Cornsilk→background`, `spacing.12→padding`, `radius.md→radius`, `font:SUIT` |
| notification-center | `color.Coral Blush→surface`, `color.Mint Green→emphasis`, `color.Cornsilk→background`, `spacing.12→padding`, `radius.md→radius`, `font:SUIT` |
| notification-item | `color.Cornsilk→background`, `spacing.12→padding`, `radius.md→radius`, `font:SUIT` |
| pagination | `color.Coral Blush→surface`, `color.Mint Green→emphasis`, `color.Cornsilk→background`, `spacing.12→padding`, `radius.md→radius`, `font:SUIT` |
| post-card | `color.Cornsilk→background`, `spacing.12→padding`, `radius.md→radius`, `font:SUIT` |
| presence-indicator | `color.Cornsilk→background`, `spacing.12→padding`, `radius.md→radius`, `font:SUIT` |
| primary-button | `color.Coral Blush→surface`, `color.Mint Green→emphasis`, `color.Cornsilk→background`, `spacing.12→padding`, `radius.md→radius`, `font:SUIT` |
| profile-card | `color.Cornsilk→background`, `spacing.12→padding`, `radius.md→radius`, `font:SUIT` |
| radio-group | `color.Coral Blush→surface`, `color.Mint Green→emphasis`, `color.Cornsilk→background`, `spacing.12→padding`, `radius.md→radius`, `font:SUIT` |
| reaction-bar | `color.Cornsilk→background`, `spacing.12→padding`, `radius.md→radius`, `font:SUIT` |
| reply-composer | `color.Coral Blush→surface`, `color.Mint Green→emphasis`, `color.Cornsilk→background`, `spacing.12→padding`, `radius.md→radius`, `font:SUIT` |
| row-actions | `color.Cornsilk→background`, `spacing.12→padding`, `radius.md→radius`, `font:SUIT` |
| search-field | `color.Coral Blush→surface`, `color.Mint Green→emphasis`, `color.Cornsilk→background`, `spacing.12→padding`, `radius.md→radius`, `font:SUIT` |
| search-results | `color.Cornsilk→background`, `spacing.12→padding`, `radius.md→radius`, `font:SUIT` |
| secondary-button | `color.Coral Blush→surface`, `color.Mint Green→emphasis`, `color.Cornsilk→background`, `spacing.12→padding`, `radius.md→radius`, `font:SUIT` |
| section-header | `color.Cornsilk→background`, `spacing.12→padding`, `radius.md→radius`, `font:SUIT` |
| section-tabs | `color.Coral Blush→surface`, `color.Mint Green→emphasis`, `color.Cornsilk→background`, `spacing.12→padding`, `radius.md→radius`, `font:SUIT` |
| segmented-control | `color.Coral Blush→surface`, `color.Mint Green→emphasis`, `color.Cornsilk→background`, `spacing.12→padding`, `radius.md→radius`, `font:SUIT` |
| select | `color.Coral Blush→surface`, `color.Mint Green→emphasis`, `color.Cornsilk→background`, `spacing.12→padding`, `radius.md→radius`, `font:SUIT` |
| share-sheet | `color.Coral Blush→surface`, `color.Mint Green→emphasis`, `color.Cornsilk→background`, `spacing.12→padding`, `radius.md→radius`, `font:SUIT` |
| shortcut-hint | `color.Cornsilk→background`, `spacing.12→padding`, `radius.md→radius`, `font:SUIT` |
| sidebar-nav | `color.Coral Blush→surface`, `color.Mint Green→emphasis`, `color.Cornsilk→background`, `spacing.12→padding`, `radius.md→radius`, `font:SUIT` |
| slash-command-menu | `color.Cornsilk→background`, `spacing.12→padding`, `radius.md→radius`, `font:SUIT` |
| soft-dialog | `color.Coral Blush→surface`, `color.Mint Green→emphasis`, `color.Cornsilk→background`, `spacing.12→padding`, `radius.md→radius`, `font:SUIT` |
| stat-card | `color.Cornsilk→background`, `spacing.12→padding`, `radius.md→radius`, `font:SUIT` |
| status-badge | `color.Cornsilk→background`, `spacing.12→padding`, `radius.md→radius`, `font:SUIT` |
| tab-bar | `color.Coral Blush→surface`, `color.Mint Green→emphasis`, `color.Cornsilk→background`, `spacing.12→padding`, `radius.md→radius`, `font:SUIT` |
| tag | `color.Cornsilk→background`, `spacing.12→padding`, `radius.md→radius`, `font:SUIT` |
| tag-pill | `color.Cornsilk→background`, `spacing.12→padding`, `radius.md→radius`, `font:SUIT` |
| text-field | `color.Coral Blush→surface`, `color.Mint Green→emphasis`, `color.Cornsilk→background`, `spacing.12→padding`, `radius.md→radius`, `font:SUIT` |
| textarea | `color.Coral Blush→surface`, `color.Mint Green→emphasis`, `color.Cornsilk→background`, `spacing.12→padding`, `radius.md→radius`, `font:SUIT` |
| thread-view | `color.Cornsilk→background`, `spacing.12→padding`, `radius.md→radius`, `font:SUIT` |
| time-picker | `color.Coral Blush→surface`, `color.Mint Green→emphasis`, `color.Cornsilk→background`, `spacing.12→padding`, `radius.md→radius`, `font:SUIT` |
| timeline-stream | `color.Cornsilk→background`, `spacing.12→padding`, `radius.md→radius`, `font:SUIT` |
| toast | `color.Cornsilk→background`, `spacing.12→padding`, `radius.md→radius`, `font:SUIT` |
| topbar | `color.Coral Blush→surface`, `color.Mint Green→emphasis`, `color.Cornsilk→background`, `spacing.12→padding`, `radius.md→radius`, `font:SUIT` |
| user-menu | `color.Coral Blush→surface`, `color.Mint Green→emphasis`, `color.Cornsilk→background`, `spacing.12→padding`, `radius.md→radius`, `font:SUIT` |

## 19. Contrast Audit

| Background | Foreground | Ratio | Level |
|------------|------------|-------|-------|
| Cornsilk | Ink | 17.73:1 | AAA (pass) |
| Mint Green | Ink | 15.37:1 | AAA (pass) |
| Coral Blush | Ink | 7.66:1 | AAA (pass) |
| Coral Blush | Paper | 2.47:1 | fail (FAIL) |
| Coral Blush | Cornsilk | 2.32:1 | fail (FAIL) |
| Coral Blush | Mint Green | 2.01:1 | fail (FAIL) |
| Mint Green | Paper | 1.23:1 | fail (FAIL) |
| Mint Green | Cornsilk | 1.15:1 | fail (FAIL) |
| Cornsilk | Paper | 1.07:1 | fail (FAIL) |

## 20. Pattern Catalog

### Layout Patterns

- **feed item**: —
- **post card**: —
- **thread view**: —
- **reply composer**: —
- **comment thread**: —
- **reaction bar**: —
- **follow button**: —
- **presence indicator**: —
- **notification center**: —
- **notification item**: —
- **avatar cluster**: —
- **timeline stream**: —
- **mention highlight**: —
- **tag pill**: —
- **share sheet**: —
- **empty-feed illustration**: —
- **gentle toast**: —
- **soft dialog**: —
- **workspace navigation**: app-shell, sidebar-nav, topbar, breadcrumb, tab-bar
- **dashboard cards**: stat-card, insight-card, activity-card, section-header
- **data tables**: data-table, column-header, filter-chip, row-actions, pagination, filter-toolbar

### Interaction Patterns

- **command palette**: command-palette, command-result-item, shortcut-hint
- **forms**: text-field, select, checkbox, textarea, form-section, radio-group, form-actions
- **notifications**: toast, inline-alert, empty-state, banner
