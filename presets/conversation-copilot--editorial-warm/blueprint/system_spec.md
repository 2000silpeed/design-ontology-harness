# Quill System Spec

## 1. Positioning

- **Brand**: Quill
- **Product**: editorial-warm 톤 writing/reading AI copilot — chat · prompt · artifact(draft) · thread · composer, 차분한 warm neutral + serif-ish pairing, reading-first editorial canvas, 한국어 1급
- **Audience**: 에세이 / 뉴스레터 / 블로그 글쓰기 작가 (차분한 writing partner 필요), 저널 / 독서 노트 / 북 리뷰를 기록하는 reading-first 사용자, 매거진 / 에디토리얼 에디터 (AI 드래프트 편집 + 아티팩트 리뷰)
- **Platforms**: web, desktop-web, tablet-web
- **Accessibility floor**: WCAG 2.2 AA

## 2. Identity Guardrails

- **Brand keywords**: conversation-copilot, copilot, assistant, chat, prompt, thread, artifact, writing-assistant, editorial-copilot, essay-draft, newsletter-draft, calm, warm, editorial, serif
- **Anti-keywords**: minimal-tech, bold-confident, saturated, playful-pastel, dashboard-heavy, commerce-heavy, streetwear, high-contrast, neon
- **Tone of voice**: calm, thoughtful, editorial, warm, measured
- **Visual direction**: warm neutral surface, serif heading pair, muted editorial accent, reading-first layout, calm writing canvas, soft cream surface, muted warm divider, restrained bibliographic chrome, long-form artifact preview
- **Interaction direction**: calm streaming cursor, gentle prompt composer, writing artifact side panel, draft revision timeline, outline collapse toggle, citation footnote hover, reading-mode toggle, slow fade transition, warm focus ring, muted mention chip

## 3. Design Principles

- **Conversation-Copilot**: `conversation-copilot`를 시각적 선택과 인터랙션 선택의 기본 기준으로 삼습니다.
- **Copilot**: `copilot`를 시각적 선택과 인터랙션 선택의 기본 기준으로 삼습니다.
- **Assistant**: `assistant`를 시각적 선택과 인터랙션 선택의 기본 기준으로 삼습니다.
- **Chat**: `chat`를 시각적 선택과 인터랙션 선택의 기본 기준으로 삼습니다.

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
- **Preferred families**: Pantone Trend Reds, Natural Greens, Natural Yellows
- **Palette strategy**: temperature=warm, contrast=balanced, diversity=balanced, surface_style=grounded
- **Palette expansion**: supporting_color_count=10, combination_count=3, prefer_pairings=True
- **Palette roles**:
  - `primary` -> Marsala #964F4C / Pantone Trend Reds
  - `accent` -> Moss Green #8A9A5B / Natural Greens
  - `surface_tint` -> Flax #EEDC82 / Natural Yellows
- **Selected colors**:
  - Chili Oil #944537 / Pantone Trend Oranges / 저명도, 저채도, 레드 브라운 계열의 딥한 오렌지 톤 / 고급스러움, 안정감, 따뜻함, 자연
  - Wheat #F5DEB3 / Natural Yellows / 중명도, 저채도, 베이지 옐로 계열의 따뜻한 톤 / 따뜻함, 자연스러움, 부드러움, 안정감
  - Apricot #FFB27F / Natural Oranges / 밝은 명도, 낮은 채도, 살짝 핑크빛이 도는 부드러운 오렌지 / 따뜻함, 부드러움, 친근함, 여유, 자연스러움
- **Palette candidates**:
  - signature-1 (Signature): primary=Chili Oil, accent=Wheat, surface_tint=Apricot / Chili Oil matches brand tone keywords.; Wheat is inside preferred families.
  - soft-spread-2 (Soft Spread): primary=Terracotta, accent=Apricot, surface_tint=Wheat / Terracotta matches brand tone keywords.; Apricot matches brand tone keywords.
- **Expanded supporting colors**:
  - Wheat #F5DEB3 / Natural Yellows / reference-color / Wheat stays inside the preferred families.; Wheat reinforces the brand mood signals.
  - Apricot #FFB27F / Natural Oranges / reference-color / Apricot reinforces the brand mood signals.
  - Terracotta #E2725B / Natural Reds / reference-color / Terracotta reinforces the brand mood signals.
  - Salmon #FA8072 / Pastel Reds / reference-color / Salmon reinforces the brand mood signals.
  - Amber #FFBF00 / Standard Yellows / reference-color / Amber reinforces the brand mood signals.
  - Autumn Blaze #D1933F / Pantone Trend Yellows / reference-color / Autumn Blaze reinforces the brand mood signals.
  - Chili Oil #944537 / Pantone Trend Oranges / reference-color / Chili Oil reinforces the brand mood signals.
  - Ochre Yellow #CB9D06 / Deep Yellows / reference-color / Ochre Yellow reinforces the brand mood signals.
- **Expanded semantic roles**:
  - `brand_primary` -> Marsala #964F4C / Pantone Trend Reds
  - `brand_accent` -> Moss Green #8A9A5B / Natural Greens
  - `surface_tint` -> Flax #EEDC82 / Natural Yellows
  - `canvas` -> Canvas White #F7F8FA / Generated Fallback
  - `surface` -> Paper #FFFFFF / Generated Fallback
  - `surface_muted` -> Surface Muted #EEF1F6 / Generated Fallback
  - `surface_elevated` -> Paper #FFFFFF / Generated Fallback
  - `border` -> Border Neutral #D6DDE6 / Generated Fallback
  - `border_strong` -> Border Strong #B0BAC7 / Generated Fallback
  - `ink` -> Ink #111111 / Generated Fallback
- **Combination lists**:
  - Seed Core: primary=Marsala, accent=Moss Green, surface_tint=Flax
  - Surface System: canvas=Canvas White, surface=Paper, surface_tint=Flax, border=Border Neutral, ink=Ink, ink_muted=Moss Green
  - Support Spectrum: support=Wheat, support=Apricot, support=Terracotta, support=Salmon, support=Amber, support=Autumn Blaze
- **Notes**: Marsala #964F4C primary — 와인-브라운 중후 editorial primary, 성숙/안정/클래식 무드, 기존 12종 HEX 겹침 0 (signal-desk editorial-warm Ochre #CC7722 / Terracotta #E2725B 와 정반대의 deep warm wine red), Moss Green #8A9A5B accent — 자연 빈티지 muted sage, calm reading-first 강조 accent (Celadon #ACE1AF / Emerald #4A7C59 / Mint #98FF98 과 겹침 0, writing-artifact/citation 강조에 적합), Flax #EEDC82 surface_tint — 광택 없는 건조한 종이 질감 베이지-옐로, editorial writing canvas 와 reading-first 레이아웃의 base surface (Wheat #F5DEB3 / Buttercream #F3E5AB / Cornsilk #FFF8DC 와 겹침 0), light mode 가 기본 — reading-first editorial 관례, dark 옵션 제공 (deep warm brown surface + tuned Marsala/Moss 채도 낮춤), 기존 12종 프리셋 HEX 와 겹침 0 — Marsala/Moss Green/Flax 조합, document-content--editorial-warm (signal-desk) 와 commerce--editorial-warm (colorfit) 와 톤만 공유 — HEX 는 완전 차별화, conversation-copilot 어휘로 매칭 축 분리
- **Application rule**: 레퍼런스 컬러는 semantic token으로 번역해서 사용하고, 접근성과 theme 호환성을 우선합니다.

## 7. Visual Reference Signals

- **Mode**: local-images
- **Coverage**: source 0 / image 0 / selected 0
- **Rule**: visual references are advisory signals for motif and layout direction; official KB/spec remain the structural source of truth.
- **Provenance**: `observed` = directly measured from local pixels, `inferred` = synthesized from image/query/brand signals, `unverified` = reliable visual evidence not yet available.
- **Query seeds**: lex page writing copilot, jasper ai editor calm, sudowrite writing assistant, notion ai writing panel, ulysses writing app editorial, substack editor warm
### Visual Direction

- **Density**: airy (confidence 0.94, provenance inferred) / editorial x6, hero x1, calm x5
- **Surface Style**: tinted (confidence 0.92, provenance inferred) / warm x7, editorial x6, cream x1
- **Corner Style**: medium (confidence 0.33, provenance inferred) / card x2
- **Typography Mood**: editorial (confidence 0.94, provenance inferred) / editorial x6, serif x3
- **Color balance**: temperature=unknown, contrast=unknown, neutral_bias=unknown, provenance=unverified

### Layout Rhythm

- **Conversation side panel**: confidence 0.94 / provenance inferred / chat x3, assistant x4, message x4, thread x5
- **Editorial feed**: confidence 0.94 / provenance inferred / editorial x6, feed x1
- **Split-pane workspace**: confidence 0.94 / provenance inferred / sidebar x2, panel x5, editor x2, dashboard x2
- **Dashboard grid**: confidence 0.77 / provenance inferred / dashboard x2, chart x1, monitoring x1

### Image-derived Component Hints

- **Cards**: low-elevation tinted cards를 기본으로 하고, 넓은 내부 여백과 강한 section breathing room. 중간 반경으로 제품 UI 절제 유지. / provenance inferred / surface=tinted, density=airy, corner=medium
- **Navigation**: 고정 sidebar 또는 split-pane navigation을 우선하고, 현재 위치와 scope를 항상 명시한다. / provenance inferred / Split-pane workspace
- **Typography**: headline rhythm과 본문 리듬의 대비를 키우고, label/metadata는 조용하게 유지한다. / provenance inferred / typography_mood=editorial
- **Data Display**: 정보 밀도를 유지하되 thin dividers와 restrained accent로 hierarchy를 만든다. / provenance inferred / layout=dashboard-grid, density=airy
- **Panel**: 보조 패널은 메인 표면보다 한 단계 더 조용한 tint와 명확한 section framing으로 구분한다. / provenance inferred / Conversation side panel

### Synthesis Notes

- layout는 Conversation side panel 기준으로 정리
- surface language는 tinted 성향 우선
- typography mood는 editorial 축 유지
- density는 airy 기준으로 primitive spacing 조정
- palette temperature는 unknown 쪽을 우선
- Avoid: saturated commerce hero
- Avoid: neon bold dashboard
- Avoid: playful pastel feed
- Avoid: dense chart monitoring canvas

## 8. Component Strategy

- **Product primitives**: chat message, chat thread, assistant message, user message, prompt composer, streaming cursor, typing indicator, inline citation, message artifact, artifact preview panel, draft document, outline sidebar, heading anchor, revision timeline, tone slider, reading-mode toggle, citation footnote, quote block, paragraph block, mention chip, suggestion card, thread header, new thread button, regenerate button, stop-generation button, empty conversation state
- **Required families**: button, data-display, editorial, feedback, input, marketing, navigation, copilot-artifact, copilot-chat, document, overlay, social
- **Visual-reference archetypes**:

- **Conversation sidecar** (overlay / 0.94): chat-panel, message-thread, message-composer, context-drawer
- **Editorial content block** (editorial / 0.94): content-card, featured-story-card, section-header, content-meta, byline-row
- **Workspace shell** (navigation / 0.94): app-shell, sidebar-nav, workspace-switcher, breadcrumb, context-panel
- **Dashboard insight module** (data-display / 0.87): stat-card, insight-card, chart-panel, section-header, filter-chip
- **Data review table** (data-display / 0.47): data-table, column-header, row-actions, filter-toolbar, pagination

- **button**: primary-button, secondary-button, ghost-button, icon-button, cta-button, link-button, regenerate-button, stop-generation-button
- **data-display**: comment-thread, chat-message, chat-thread, tag, calendar-grid, video-player, chart-container, chart-legend / visual signals: Dashboard insight module (0.87)
- **editorial**: editor-canvas, editor-toolbar, inline-format-menu, slash-command-menu, block-controls, content-card, featured-story-card, content-meta / visual signals: Editorial content block (0.94)
- **feedback**: inline-alert, empty-state, toast, empty-conversation-state, status-badge, banner, step-progress, empty-feed-illustration
- **input**: text-field, search-field, segmented-control, tone-slider, prompt-composer, comment-input, chat-input, chip
- **marketing**: site-footer, footer-column, footer-link, footer-legal, footer-social, logo-cloud, customer-logo, metric-highlight
- **navigation**: mobile-topbar, mobile-tab-bar, back-button, section-tabs, prev-next-pager, app-shell, sidebar-nav, topbar / visual signals: Workspace shell (0.94)
- **copilot-artifact**: message-artifact, artifact-preview-panel, draft-document, outline-sidebar, revision-timeline, reading-mode-toggle, citation-footnote, quote-block
- **copilot-chat**: streaming-cursor, typing-indicator, inline-citation, mention-chip, suggestion-card, thread-header
- **document**: article-body, table-of-contents, heading-anchor, prose-block, reading-pane, footnote, link-card, code-block
- **overlay**: bottom-sheet, modal-dialog, mention-popup, chart-tooltip, confirm-dialog, autocomplete, tooltip-guide, share-sheet / visual signals: Conversation sidecar (0.94)
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

- Warning: [pitfall#3-rebrand] Chili Oil vs Apricot (orange): lightness diff 35, saturation diff 54 — possible rebrand remnant
- Warning: visual_reference.sources is empty

## 14. Quick Start

이 문서는 **Quill System**의 디자인 시스템 사양입니다.

### 시작하기

1. **토큰 적용**: Drop-in CSS(아래 섹션 16)의 CSS 변수를 프로젝트에 복사합니다.
2. **컬러 세팅**: Color Reference(섹션 6)의 semantic role을 기준으로 surface/text/border를 잡습니다.
3. **타이포 세팅**: Token Strategy(섹션 5)의 font family와 type scale을 적용합니다.
4. **시각 방향 확인**: Visual Reference Signals(섹션 7)에서 density/surface/layout cue를 먼저 확인합니다.
5. **컴포넌트 구현**: Component Strategy(섹션 8)의 family 순서대로 하나씩 빌드합니다.

### 우선순위

핵심 primitive: **chat message, chat thread, assistant message, user message, prompt composer**

이 primitive를 지원하는 컴포넌트부터 구현하고, 나머지는 필요에 따라 확장합니다.

## 15. DO / DON'T

### DO

- **Conversation-Copilot**: conversation-copilot와 충돌하는 컴포넌트 변형은 만들지 않기
- **Copilot**: copilot와 충돌하는 컴포넌트 변형은 만들지 않기
- **Assistant**: assistant와 충돌하는 컴포넌트 변형은 만들지 않기
- **Chat**: chat와 충돌하는 컴포넌트 변형은 만들지 않기
- 모든 시각적 선택에서 **conversation-copilot, copilot, assistant** 기준을 적용
- semantic token을 통해 컬러를 적용 (하드코딩 금지)
- 접근성 기준을 모든 text/surface 조합에서 먼저 검증
- 컴포넌트 변형 추가 전 기존 variant로 해결 가능한지 먼저 확인
- 아이콘은 SVG 컴포넌트 또는 Lucide/Heroicons/Phosphor/Tabler 등 라이브러리로 구현
- component_specs.md의 anatomy/states/token binding을 그대로 따라 완전히 구현

### DON'T

- **minimal-tech** 방향의 디자인 결정을 하지 않음
- **bold-confident** 방향의 디자인 결정을 하지 않음
- **saturated** 방향의 디자인 결정을 하지 않음
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
  --color-primary: #964F4C;
  --color-accent: #8A9A5B;
  --color-surface-tint: #EEDC82;

  /* --- Semantic roles (expanded) --- */
  --color-brand-primary: #964F4C;
  --color-brand-accent: #8A9A5B;
  --color-surface-tint: #EEDC82;
  --color-canvas: #F7F8FA;
  --color-surface: #FFFFFF;
  --color-surface-muted: #EEF1F6;
  --color-surface-elevated: #FFFFFF;
  --color-border: #D6DDE6;
  --color-border-strong: #B0BAC7;
  --color-ink: #111111;
  --color-ink-muted: #8A9A5B;
  --color-ink-subtle: #8A9A5B;
  --color-ink-inverse: #FFFFFF;
  --color-primary-support: #E2725B;
  --color-accent-support: #8A9A5B;
  --color-info: #4A6B8A;
  --color-success: #8A9A5B;
  --color-warning: #F5DEB3;
  --color-danger: #964F4C;
  --color-link: #964F4C;
  --color-link-hover: #7B413E;

  /* --- Button — primary --- */
  --color-button-primary-surface-default: #964F4C;
  --color-button-primary-surface-hover: #824442;
  --color-button-primary-surface-active: #743D3B;
  --color-button-primary-surface-disabled: #D0B4B4;
  --color-button-primary-text-default: #FFFFFF;
  --color-button-primary-text-disabled: #FBFCFC;
  --color-button-primary-border-default: #964F4C;
  --color-button-primary-focus-ring: #964F4C;

  /* --- Button — secondary --- */
  --color-button-secondary-surface-default: #FFFFFF;
  --color-button-secondary-surface-hover: #F1F1F1;
  --color-button-secondary-surface-active: #E7E7E7;
  --color-button-secondary-surface-disabled: #F7F8FA;
  --color-button-secondary-text-default: #111111;
  --color-button-secondary-text-disabled: #909091;
  --color-button-secondary-border-default: #BDC8D7;
  --color-button-secondary-border-hover: #A3B3C7;
  --color-button-secondary-focus-ring: #964F4C;

  /* --- Button — ghost --- */
  --color-button-ghost-surface-default: transparent;
  --color-button-ghost-surface-hover: #F3F3F3;
  --color-button-ghost-surface-active: #EAEAEA;
  --color-button-ghost-surface-disabled: transparent;
  --color-button-ghost-text-default: #8A9A5B;
  --color-button-ghost-text-hover: #111111;
  --color-button-ghost-text-disabled: #C6CEB2;
  --color-button-ghost-border-default: transparent;
  --color-button-ghost-focus-ring: #964F4C;

  /* --- Button — danger --- */
  --color-button-danger-surface-default: #964F4C;
  --color-button-danger-surface-hover: #824442;
  --color-button-danger-surface-active: #743D3B;
  --color-button-danger-text-default: #FFFFFF;
  --color-button-danger-border-default: #964F4C;
  --color-button-danger-focus-ring: #964F4C;

  /* --- Input --- */
  --color-input-surface-default: #FFFFFF;
  --color-input-surface-filled: #FFFFFF;
  --color-input-surface-disabled: #F7F8FA;
  --color-input-text-default: #111111;
  --color-input-text-placeholder: #B6C09B;
  --color-input-text-disabled: #C6CEB2;
  --color-input-border-default: #D6DDE6;
  --color-input-border-hover: #B6C3D3;
  --color-input-border-focus: #964F4C;
  --color-input-border-error: #964F4C;
  --color-input-border-disabled: #E6EAF0;

  /* --- Card --- */
  --color-card-surface-default: #FFFFFF;
  --color-card-surface-hover: #FAFAFA;
  --color-card-surface-muted: #F7F8FA;
  --color-card-border-default: #D6DDE6;
  --color-card-border-hover: #B6C3D3;
  --color-card-border-focus: #964F4C;

  /* --- Nav link --- */
  --color-nav-link-text-default: #8A9A5B;
  --color-nav-link-text-hover: #111111;
  --color-nav-link-text-active: #964F4C;
  --color-nav-link-surface-hover: #F5F5F5;
  --color-nav-link-indicator: #8A9A5B;

  /* --- Link --- */
  --color-link-text-default: #964F4C;
  --color-link-text-hover: #743D3B;
  --color-link-text-visited: #715957;

  /* --- Feedback — info --- */
  --color-feedback-info-surface: #E9EDF1;
  --color-feedback-info-text: #4A6B8A;
  --color-feedback-info-border: #7E95AC;
  --color-feedback-info-icon: #4A6B8A;

  /* --- Feedback — success --- */
  --color-feedback-success-surface: #F1F3EB;
  --color-feedback-success-text: #8A9A5B;
  --color-feedback-success-border: #ABB68B;
  --color-feedback-success-icon: #8A9A5B;

  /* --- Feedback — warning --- */
  --color-feedback-warning-surface: #FEFBF6;
  --color-feedback-warning-text: #F5DEB3;
  --color-feedback-warning-border: #F6E6C8;
  --color-feedback-warning-icon: #F5DEB3;

  /* --- Feedback — danger --- */
  --color-feedback-danger-surface: #F2EAEA;
  --color-feedback-danger-text: #964F4C;
  --color-feedback-danger-border: #B38280;
  --color-feedback-danger-icon: #964F4C;

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
| activity-card | `color.Flax→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| app-shell | `color.Marsala→surface`, `color.Moss Green→emphasis`, `color.Flax→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| article-body | `color.Flax→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| artifact-preview-panel | `color.Flax→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| autocomplete | `color.Marsala→surface`, `color.Moss Green→emphasis`, `color.Flax→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| avatar | `color.Flax→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| avatar-cluster | `color.Flax→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| back-button | `color.Marsala→surface`, `color.Moss Green→emphasis`, `color.Flax→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| banner | `color.Flax→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| block-controls | `color.Flax→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| bottom-sheet | `color.Marsala→surface`, `color.Moss Green→emphasis`, `color.Flax→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| breadcrumb | `color.Marsala→surface`, `color.Moss Green→emphasis`, `color.Flax→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| byline-row | `color.Flax→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| calendar-grid | `color.Flax→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| chart-container | `color.Flax→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| chart-legend | `color.Flax→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| chart-panel | `color.Flax→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| chart-tooltip | `color.Marsala→surface`, `color.Moss Green→emphasis`, `color.Flax→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| chat-input | `color.Marsala→surface`, `color.Moss Green→emphasis`, `color.Flax→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| chat-message | `color.Flax→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| chat-panel | `color.Marsala→surface`, `color.Moss Green→emphasis`, `color.Flax→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| chat-thread | `color.Flax→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| checkbox | `color.Marsala→surface`, `color.Moss Green→emphasis`, `color.Flax→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| chip | `color.Marsala→surface`, `color.Moss Green→emphasis`, `color.Flax→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| citation-footnote | `color.Flax→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| code-block | `color.Flax→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| column-header | `color.Flax→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| comment-input | `color.Marsala→surface`, `color.Moss Green→emphasis`, `color.Flax→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| comment-thread | `color.Flax→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| confirm-dialog | `color.Marsala→surface`, `color.Moss Green→emphasis`, `color.Flax→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| content-card | `color.Flax→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| content-meta | `color.Flax→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| context-drawer | `color.Marsala→surface`, `color.Moss Green→emphasis`, `color.Flax→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| context-panel | `color.Marsala→surface`, `color.Moss Green→emphasis`, `color.Flax→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| copy-code-button | `color.Marsala→surface`, `color.Moss Green→emphasis`, `color.Flax→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| cta-button | `color.Marsala→surface`, `color.Moss Green→emphasis`, `color.Flax→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| customer-logo | `color.Flax→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| data-table | `color.Flax→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| date-picker | `color.Marsala→surface`, `color.Moss Green→emphasis`, `color.Flax→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| date-range-picker | `color.Marsala→surface`, `color.Moss Green→emphasis`, `color.Flax→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| draft-document | `color.Flax→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| editor-canvas | `color.Flax→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| editor-toolbar | `color.Flax→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| empty-conversation-state | `color.Flax→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| empty-feed-illustration | `color.Flax→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| empty-state | `color.Flax→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| featured-story-card | `color.Flax→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| feed-item | `color.Flax→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| filter-chip | `color.Marsala→surface`, `color.Moss Green→emphasis`, `color.Flax→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| filter-panel | `color.Marsala→surface`, `color.Moss Green→emphasis`, `color.Flax→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| follow-button | `color.Marsala→surface`, `color.Moss Green→emphasis`, `color.Flax→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| footer-column | `color.Flax→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| footer-legal | `color.Flax→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| footer-link | `color.Flax→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| footer-social | `color.Flax→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| footnote | `color.Flax→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| form-actions | `color.Marsala→surface`, `color.Moss Green→emphasis`, `color.Flax→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| form-section | `color.Marsala→surface`, `color.Moss Green→emphasis`, `color.Flax→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| gentle-toast | `color.Flax→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| ghost-button | `color.Marsala→surface`, `color.Moss Green→emphasis`, `color.Flax→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| heading-anchor | `color.Flax→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| icon-button | `color.Marsala→surface`, `color.Moss Green→emphasis`, `color.Flax→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| inline-alert | `color.Flax→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| inline-citation | `color.Flax→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| inline-code | `color.Flax→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| inline-format-menu | `color.Flax→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| insight-card | `color.Flax→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| kanban-board | `color.Flax→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| kanban-card | `color.Flax→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| kanban-column | `color.Flax→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| language-tab | `color.Flax→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| link-button | `color.Marsala→surface`, `color.Moss Green→emphasis`, `color.Flax→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| link-card | `color.Flax→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| logo-cloud | `color.Flax→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| mention-chip | `color.Flax→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| mention-popup | `color.Marsala→surface`, `color.Moss Green→emphasis`, `color.Flax→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| message-artifact | `color.Flax→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| message-composer | `color.Marsala→surface`, `color.Moss Green→emphasis`, `color.Flax→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| message-thread | `color.Marsala→surface`, `color.Moss Green→emphasis`, `color.Flax→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| metric-highlight | `color.Flax→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| mobile-tab-bar | `color.Marsala→surface`, `color.Moss Green→emphasis`, `color.Flax→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| mobile-topbar | `color.Marsala→surface`, `color.Moss Green→emphasis`, `color.Flax→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| modal-dialog | `color.Marsala→surface`, `color.Moss Green→emphasis`, `color.Flax→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| new-thread-button | `color.Marsala→surface`, `color.Moss Green→emphasis`, `color.Flax→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| outline-sidebar | `color.Flax→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| pagination | `color.Marsala→surface`, `color.Moss Green→emphasis`, `color.Flax→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| paragraph-block | `color.Flax→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| player-controls | `color.Marsala→surface`, `color.Moss Green→emphasis`, `color.Flax→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| post-card | `color.Flax→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| press-quote | `color.Flax→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| prev-next-pager | `color.Marsala→surface`, `color.Moss Green→emphasis`, `color.Flax→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| primary-button | `color.Marsala→surface`, `color.Moss Green→emphasis`, `color.Flax→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| profile-card | `color.Flax→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| prompt-composer | `color.Marsala→surface`, `color.Moss Green→emphasis`, `color.Flax→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| prose-block | `color.Flax→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| quote-block | `color.Flax→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| radio-group | `color.Marsala→surface`, `color.Moss Green→emphasis`, `color.Flax→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| reaction-bar | `color.Flax→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| reading-mode-toggle | `color.Flax→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| reading-pane | `color.Flax→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| regenerate-button | `color.Marsala→surface`, `color.Moss Green→emphasis`, `color.Flax→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| reply-composer | `color.Marsala→surface`, `color.Moss Green→emphasis`, `color.Flax→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| revision-timeline | `color.Flax→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| row-actions | `color.Flax→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| search-field | `color.Marsala→surface`, `color.Moss Green→emphasis`, `color.Flax→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| search-results | `color.Flax→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| secondary-button | `color.Marsala→surface`, `color.Moss Green→emphasis`, `color.Flax→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| section-header | `color.Flax→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| section-tabs | `color.Marsala→surface`, `color.Moss Green→emphasis`, `color.Flax→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| segmented-control | `color.Marsala→surface`, `color.Moss Green→emphasis`, `color.Flax→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| select | `color.Marsala→surface`, `color.Moss Green→emphasis`, `color.Flax→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| share-sheet | `color.Marsala→surface`, `color.Moss Green→emphasis`, `color.Flax→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| sidebar-nav | `color.Marsala→surface`, `color.Moss Green→emphasis`, `color.Flax→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| site-footer | `color.Flax→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| slash-command-menu | `color.Flax→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| soft-dialog | `color.Marsala→surface`, `color.Moss Green→emphasis`, `color.Flax→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| stat-card | `color.Flax→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| status-badge | `color.Flax→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| step-progress | `color.Flax→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| stop-generation-button | `color.Marsala→surface`, `color.Moss Green→emphasis`, `color.Flax→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| streaming-cursor | `color.Flax→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| suggestion-card | `color.Flax→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| tab-bar | `color.Marsala→surface`, `color.Moss Green→emphasis`, `color.Flax→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| table-of-contents | `color.Flax→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| tag | `color.Flax→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| tag-pill | `color.Flax→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| text-field | `color.Marsala→surface`, `color.Moss Green→emphasis`, `color.Flax→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| textarea | `color.Marsala→surface`, `color.Moss Green→emphasis`, `color.Flax→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| thread-header | `color.Flax→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| thread-view | `color.Flax→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| time-picker | `color.Marsala→surface`, `color.Moss Green→emphasis`, `color.Flax→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| timeline-stream | `color.Flax→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| toast | `color.Flax→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| tone-slider | `color.Marsala→surface`, `color.Moss Green→emphasis`, `color.Flax→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| tooltip-guide | `color.Marsala→surface`, `color.Moss Green→emphasis`, `color.Flax→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| topbar | `color.Marsala→surface`, `color.Moss Green→emphasis`, `color.Flax→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| typing-indicator | `color.Flax→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| user-menu | `color.Marsala→surface`, `color.Moss Green→emphasis`, `color.Flax→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| video-player | `color.Flax→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| volume-slider | `color.Marsala→surface`, `color.Moss Green→emphasis`, `color.Flax→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| wizard-layout | `color.Marsala→surface`, `color.Moss Green→emphasis`, `color.Flax→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| workspace-switcher | `color.Marsala→surface`, `color.Moss Green→emphasis`, `color.Flax→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |

## 19. Contrast Audit

| Background | Foreground | Ratio | Level |
|------------|------------|-------|-------|
| Flax | Ink | 13.66:1 | AAA (pass) |
| Moss Green | Ink | 6.16:1 | AA (pass) |
| Marsala | Paper | 5.97:1 | AA (pass) |
| Marsala | Flax | 4.32:1 | AA-large (large-only) |
| Marsala | Ink | 3.16:1 | AA-large (large-only) |
| Moss Green | Paper | 3.06:1 | AA-large (large-only) |
| Moss Green | Flax | 2.22:1 | fail (FAIL) |
| Marsala | Moss Green | 1.95:1 | fail (FAIL) |
| Flax | Paper | 1.38:1 | fail (FAIL) |

## 20. Pattern Catalog

### Layout Patterns

- **chat message**: —
- **chat thread**: —
- **assistant message**: —
- **user message**: —
- **prompt composer**: —
- **streaming cursor**: —
- **typing indicator**: —
- **inline citation**: —
- **message artifact**: —
- **artifact preview panel**: —
- **draft document**: —
- **outline sidebar**: —
- **heading anchor**: —
- **revision timeline**: —
- **tone slider**: —
- **reading-mode toggle**: —
- **citation footnote**: —
- **quote block**: —
- **paragraph block**: —
- **mention chip**: —
- **suggestion card**: —
- **thread header**: —
- **new thread button**: —
- **regenerate button**: —
- **stop-generation button**: —
- **empty conversation state**: —
- **workspace navigation**: app-shell, sidebar-nav, topbar, breadcrumb, workspace-switcher, tab-bar, context-panel
- **dashboard cards**: stat-card, insight-card, activity-card, section-header, chart-panel
- **data tables**: data-table, column-header, filter-chip, row-actions, pagination

### Interaction Patterns

- **command palette**: —
- **forms**: text-field, select, checkbox, textarea, form-section, radio-group, form-actions
- **notifications**: toast, inline-alert, empty-state, banner
