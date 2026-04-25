# Curator System Spec

## 1. Positioning

- **Brand**: Curator
- **Product**: editorial-warm 톤 editorial/publishing 운영 대시보드 — sidebar-nav · topbar · data-table · kpi-card · filter-chip · curation-queue · editorial-calendar · publishing-pipeline · contributor-roster, warm neutral surface + serif heading + muted accent + reading-first calm chrome, 한국어 1급
- **Audience**: 매거진/뉴스룸 에디터 (이슈/피처/오피니언 큐레이션, 피어 리뷰, 발행 스케줄), 출판사 편집장/편집자 (연간/분기 호 플래닝, 기고자 로스터, 편집 파이프라인), Content Studio 운영자 (메일 매거진·블로그 큐레이션, 리딩 애널리틱스)
- **Platforms**: web, desktop-web, tablet-web
- **Accessibility floor**: WCAG 2.2 AA

## 2. Identity Guardrails

- **Brand keywords**: dashboard, admin, console, editorial, publishing, curation, newsroom, magazine-admin, content-studio, editor-dashboard, warm, serif, calm, reading-first, muted
- **Anti-keywords**: minimal-tech, bold-confident, saturated, playful-pastel, corporate-conservative, streetwear, high-contrast, neon, fintech-heavy
- **Tone of voice**: calm, thoughtful, editorial, warm, measured
- **Visual direction**: warm neutral sidebar, serif heading pair, muted editorial accent, reading-first data table, calm kpi card, soft cream surface, restrained editorial chrome, muted warm divider, long-form article preview drawer
- **Interaction direction**: calm row hover, gentle filter chip toggle, slow fade drawer, warm focus ring, muted mention chip, soft toast, restrained sort indicator, editorial reading drawer transition, curation queue drag, schedule cell focus glow

## 3. Design Principles

- **Dashboard**: `dashboard`를 시각적 선택과 인터랙션 선택의 기본 기준으로 삼습니다.
- **Admin**: `admin`를 시각적 선택과 인터랙션 선택의 기본 기준으로 삼습니다.
- **Console**: `console`를 시각적 선택과 인터랙션 선택의 기본 기준으로 삼습니다.
- **Editorial Hierarchy**: 타이포그래피와 여백으로 위계를 만들고, 장식은 의미를 돕는 범위에서만 사용합니다.

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
- **Mono**: Fira Code
- **Product type detected**: editorial
- **Pairing source**: editorial (KR native)
- **Line height**: relaxed
- **Type scale**: base 16px, ratio 1.333 (xs=12px, sm=14px, md=16px, lg=21px, xl=28px, 2xl=38px, 3xl=50px)
- **Strategy**:
  - 헤딩(세리프) + 본문(산세리프) 대비 구조 — 에디토리얼 정석
  - 한글 서체: Pretendard — 라틴과 x-height/weight 조화
  - 모노스페이스: Fira Code — 코드/데이터 영역 전용
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
- **Loading**: Pretendard(preload), Noto Serif KR(preload), Fira Code(lazy) | display: swap

## 6. Color Reference

- **Source**: REFERENCE X Vol.1 - Color Reference (/Users/sungwoon/ai-projects/design-ontology-harness/docs/color-reference.md)
- **Selection mode**: manual
- **Preferred families**: Deep Violets, Pastel Yellows, Pastel Reds
- **Palette strategy**: temperature=warm, contrast=balanced, diversity=balanced, surface_style=grounded
- **Palette expansion**: supporting_color_count=10, combination_count=3, prefer_pairings=True
- **Palette roles**:
  - `primary` -> Aubergine #614051 / Deep Violets
  - `accent` -> Naples Yellow #FADA5E / Pastel Yellows
  - `surface_tint` -> Blush #F9C0C4 / Pastel Reds
- **Selected colors**:
  - Chili Oil #944537 / Pantone Trend Oranges / 저명도, 저채도, 레드 브라운 계열의 딥한 오렌지 톤 / 고급스러움, 안정감, 따뜻함, 자연
  - Salmon #FA8072 / Pastel Reds / 밝고 따뜻한 핑크 오렌지 톤 / 따뜻함, 부드러움, 친근함, 자연스러움
  - Apricot #FFB27F / Natural Oranges / 밝은 명도, 낮은 채도, 살짝 핑크빛이 도는 부드러운 오렌지 / 따뜻함, 부드러움, 친근함, 여유, 자연스러움
- **Palette candidates**:
  - signature-1 (Signature): primary=Chili Oil, accent=Salmon, surface_tint=Apricot / Chili Oil matches brand tone keywords.; Salmon is inside preferred families.
  - soft-spread-2 (Soft Spread): primary=Terracotta, accent=Apricot, surface_tint=Wheat / Terracotta matches brand tone keywords.; Apricot matches brand tone keywords.
- **Expanded supporting colors**:
  - Apricot #FFB27F / Natural Oranges / reference-color / Apricot reinforces the brand mood signals.
  - Salmon #FA8072 / Pastel Reds / reference-color / Salmon stays inside the preferred families.; Salmon reinforces the brand mood signals.
  - Wheat #F5DEB3 / Natural Yellows / reference-color / Wheat reinforces the brand mood signals.
  - Terracotta #E2725B / Natural Reds / reference-color / Terracotta reinforces the brand mood signals.
  - Amber #FFBF00 / Standard Yellows / reference-color / Amber reinforces the brand mood signals.
  - Flax #EEDC82 / Natural Yellows / reference-color / Flax reinforces the brand mood signals.
  - Autumn Blaze #D1933F / Pantone Trend Yellows / reference-color / Autumn Blaze reinforces the brand mood signals.
  - Cornsilk #FFF8DC / Pastel Yellows / reference-color / Cornsilk stays inside the preferred families.; Cornsilk reinforces the brand mood signals.
- **Expanded semantic roles**:
  - `brand_primary` -> Aubergine #614051 / Deep Violets
  - `brand_accent` -> Naples Yellow #FADA5E / Pastel Yellows
  - `surface_tint` -> Blush #F9C0C4 / Pastel Reds
  - `canvas` -> Canvas White #F7F8FA / Generated Fallback
  - `surface` -> Paper #FFFFFF / Generated Fallback
  - `surface_muted` -> Surface Muted #EEF1F6 / Generated Fallback
  - `surface_elevated` -> Paper #FFFFFF / Generated Fallback
  - `border` -> Border Neutral #D6DDE6 / Generated Fallback
  - `border_strong` -> Border Strong #B0BAC7 / Generated Fallback
  - `ink` -> Ink #111111 / Generated Fallback
- **Combination lists**:
  - Seed Core: primary=Aubergine, accent=Naples Yellow, surface_tint=Blush
  - Surface System: canvas=Canvas White, surface=Paper, surface_tint=Blush, border=Border Neutral, ink=Ink, ink_muted=Aubergine
  - Support Spectrum: support=Apricot, support=Salmon, support=Wheat, support=Terracotta, support=Amber, support=Flax
- **Notes**: Aubergine #614051 primary — 가지 껍질 유래 deep warm violet-brown, boutique newsroom / 출판사 editorial admin chrome 의 masthead · sidebar · primary CTA, signal-desk Ochre (#CC7722) / quill Marsala (#964F4C) 와 HEX 겹침 0, purple-forward editorial 정체성, Naples Yellow #FADA5E accent — 르네상스 회화 안료 유래 creamy warm yellow, editorial-calendar schedule highlight / kpi-card trend indicator / draft-status-pill 강조, quill Flax (#EEDC82) 와 다른 deeper saturated 변형, Blush #F9C0C4 surface_tint — 홍조 연상 연한 pink cream, workspace surface / article-preview-pane drawer 배경 / filter-chip resting state, signal-desk Wheat (#F5DEB3) / drop Buttercream (#F3E5AB) / colorfit 등과 완전히 다른 pastel red 계열, light mode 가 기본 — editorial 큐레이션 대시보드 관례 (원고 드래프트 + reading 톤), dark 옵션 제공 (tuned Aubergine deep surface + Naples Yellow muted + Blush desaturated), 기존 14종 프리셋 HEX 와 겹침 0 — Aubergine/Naples Yellow/Blush 조합, editorial-warm 는 document-content (signal-desk Ochre/Terracotta/Wheat) + commerce (colorfit) + conversation-copilot (quill Marsala/Moss/Flax) 3종에 이미 등장 — curator 는 dashboard 첫 editorial-warm 이므로 purple-forward palette 로 편집장 / 출판사 / 매거진 운영 색 스토리 확립
- **Application rule**: 레퍼런스 컬러는 semantic token으로 번역해서 사용하고, 접근성과 theme 호환성을 우선합니다.

## 7. Visual Reference Signals

- **Mode**: local-images
- **Coverage**: source 0 / image 0 / selected 0
- **Rule**: visual references are advisory signals for motif and layout direction; official KB/spec remain the structural source of truth.
- **Provenance**: `observed` = directly measured from local pixels, `inferred` = synthesized from image/query/brand signals, `unverified` = reliable visual evidence not yet available.
- **Query seeds**: ghost editorial dashboard curation, substack writer dashboard publishing, medium creator dashboard editorial analytics, notion editorial calendar publishing pipeline, readwise reading analytics dashboard, buttondown newsletter editorial dashboard
### Visual Direction

- **Density**: dense (confidence 0.94, provenance inferred) / dashboard x11, table x5, analytics x6
- **Surface Style**: tinted (confidence 0.94, provenance inferred) / warm x7, editorial x17, cream x2
- **Corner Style**: medium (confidence 0.79, provenance inferred) / card x11
- **Typography Mood**: editorial (confidence 0.94, provenance inferred) / editorial x17, article x3, magazine x2
- **Color balance**: temperature=unknown, contrast=unknown, neutral_bias=unknown, provenance=unverified

### Layout Rhythm

- **Dashboard grid**: confidence 0.94 / provenance inferred / dashboard x11, analytics x6, kpi x7, stat x1
- **Data review surface**: confidence 0.94 / provenance inferred / table x5, grid x1, data x5, filter x5
- **Editorial feed**: confidence 0.94 / provenance inferred / editorial x17, article x3, content x1, feed x1
- **Split-pane workspace**: confidence 0.94 / provenance inferred / workspace x1, sidebar x6, editor x1, dashboard x11

### Image-derived Component Hints

- **Cards**: low-elevation tinted cards를 기본으로 하고, 압축된 spacing과 얇은 divider 중심의 hierarchy. 중간 반경으로 제품 UI 절제 유지. / provenance inferred / surface=tinted, density=dense, corner=medium
- **Navigation**: 고정 sidebar 또는 split-pane navigation을 우선하고, 현재 위치와 scope를 항상 명시한다. / provenance inferred / Split-pane workspace
- **Typography**: headline rhythm과 본문 리듬의 대비를 키우고, label/metadata는 조용하게 유지한다. / provenance inferred / typography_mood=editorial
- **Data Display**: 정보 밀도를 유지하되 thin dividers와 restrained accent로 hierarchy를 만든다. / provenance inferred / layout=dashboard-grid, density=dense

### Synthesis Notes

- layout는 Dashboard grid 기준으로 정리
- surface language는 tinted 성향 우선
- typography mood는 editorial 축 유지
- density는 dense 기준으로 primitive spacing 조정
- palette temperature는 unknown 쪽을 우선
- Avoid: saturated commerce hero
- Avoid: bold magazine cover
- Avoid: fintech navy dashboard (corporate-trust dense)
- Avoid: neon dark developer dashboard (minimal-tech)

## 8. Component Strategy

- **Product primitives**: sidebar-nav, topbar, workspace-header, breadcrumb, data-table, column-header, row-actions, pagination, filter-sidebar, filter-chip, sort-dropdown, search-field, kpi-card, stat-card, insight-card, activity-card, section-header, tag, status-badge, chip, comment-thread, avatar, user-menu, profile-card, date-picker, modal-dialog, toast, empty-state, primary-button, secondary-button, ghost-button, icon-button, curation-queue, editorial-calendar, draft-status-pill, publishing-pipeline, issue-planner, contributor-roster, article-preview-pane, editorial-analytics-kpi, reading-analytics-kpi, archive-shelf, tag-taxonomy-manager
- **Required families**: button, data-display, editorial, feedback, input, marketing, navigation, commerce, copilot-artifact, copilot-chat, dashboard-editorial, document, magazine, overlay, social
- **Visual-reference archetypes**:

- **Dashboard insight module** (data-display / 0.94): stat-card, insight-card, chart-panel, section-header, filter-chip
- **Data review table** (data-display / 0.94): data-table, column-header, row-actions, filter-toolbar, pagination
- **Editorial content block** (editorial / 0.94): content-card, featured-story-card, section-header, content-meta, byline-row
- **Workspace shell** (navigation / 0.94): app-shell, sidebar-nav, workspace-switcher, breadcrumb, context-panel
- **Conversation sidecar** (overlay / 0.52): chat-panel, message-thread, message-composer, context-drawer

- **button**: primary-button, secondary-button, ghost-button, icon-button, cta-button, link-button, form-actions, add-to-cart-button
- **data-display**: stat-card, insight-card, activity-card, section-header, data-table, column-header, row-actions, draft-status-pill / visual signals: Dashboard insight module (0.94), Data review table (0.94)
- **editorial**: editor-canvas, editor-toolbar, inline-format-menu, slash-command-menu, block-controls, content-card, featured-story-card, content-meta / visual signals: Editorial content block (0.94)
- **feedback**: inline-alert, empty-state, toast, status-badge, banner, upgrade-banner, discount-badge, shortcut-hint
- **input**: text-field, search-field, segmented-control, filter-chip, chip, comment-input, date-picker, time-picker
- **marketing**: logo-cloud, customer-logo, metric-highlight, press-quote
- **navigation**: mobile-topbar, mobile-tab-bar, back-button, section-tabs, pagination, app-shell, sidebar-nav, topbar / visual signals: Workspace shell (0.94)
- **commerce**: product-grid, product-card, product-detail, product-gallery, product-hero-image, image-thumbnail, price-tag, original-price-strikethrough
- **copilot-artifact**: message-artifact, artifact-preview-panel, draft-document, outline-sidebar, revision-timeline, reading-mode-toggle, citation-footnote, quote-block
- **copilot-chat**: streaming-cursor, typing-indicator, inline-citation, mention-chip, suggestion-card, thread-header
- **dashboard-editorial**: curation-queue, editorial-calendar, article-preview-pane, contributor-roster, editorial-analytics-kpi, reading-analytics-kpi, archive-shelf, tag-taxonomy-manager
- **document**: article-body, table-of-contents, heading-anchor, prose-block, reading-pane, footnote, link-card, api-reference-table
- **magazine**: masthead, issue-header, issue-number, cover-story, opening-spread, feature-article, kicker-eyebrow, pull-quote
- **overlay**: bottom-sheet, modal-dialog, mention-popup, autocomplete, confirm-dialog, user-menu, quick-view-modal, command-palette
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

이 문서는 **Curator System**의 디자인 시스템 사양입니다.

### 시작하기

1. **토큰 적용**: Drop-in CSS(아래 섹션 16)의 CSS 변수를 프로젝트에 복사합니다.
2. **컬러 세팅**: Color Reference(섹션 6)의 semantic role을 기준으로 surface/text/border를 잡습니다.
3. **타이포 세팅**: Token Strategy(섹션 5)의 font family와 type scale을 적용합니다.
4. **시각 방향 확인**: Visual Reference Signals(섹션 7)에서 density/surface/layout cue를 먼저 확인합니다.
5. **컴포넌트 구현**: Component Strategy(섹션 8)의 family 순서대로 하나씩 빌드합니다.

### 우선순위

핵심 primitive: **sidebar-nav, topbar, workspace-header, breadcrumb, data-table**

이 primitive를 지원하는 컴포넌트부터 구현하고, 나머지는 필요에 따라 확장합니다.

## 15. DO / DON'T

### DO

- **Dashboard**: dashboard와 충돌하는 컴포넌트 변형은 만들지 않기
- **Admin**: admin와 충돌하는 컴포넌트 변형은 만들지 않기
- **Console**: console와 충돌하는 컴포넌트 변형은 만들지 않기
- **Editorial Hierarchy**: 텍스트 중심 레이아웃
- 모든 시각적 선택에서 **dashboard, admin, console** 기준을 적용
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
  --font-mono: 'Fira Code', monospace;
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
  --color-primary: #614051;
  --color-accent: #FADA5E;
  --color-surface-tint: #F9C0C4;

  /* --- Semantic roles (expanded) --- */
  --color-brand-primary: #614051;
  --color-brand-accent: #FADA5E;
  --color-surface-tint: #F9C0C4;
  --color-canvas: #F7F8FA;
  --color-surface: #FFFFFF;
  --color-surface-muted: #EEF1F6;
  --color-surface-elevated: #FFFFFF;
  --color-border: #D6DDE6;
  --color-border-strong: #B0BAC7;
  --color-ink: #111111;
  --color-ink-muted: #614051;
  --color-ink-subtle: #6B7280;
  --color-ink-inverse: #FFFFFF;
  --color-primary-support: #614051;
  --color-accent-support: #F5DEB3;
  --color-info: #614051;
  --color-success: #4A7C59;
  --color-warning: #FADA5E;
  --color-danger: #FA8072;
  --color-link: #614051;
  --color-link-hover: #48303C;

  /* --- Button — primary --- */
  --color-button-primary-surface-default: #614051;
  --color-button-primary-surface-hover: #4F3442;
  --color-button-primary-surface-active: #422C37;
  --color-button-primary-surface-disabled: #BBAEB6;
  --color-button-primary-text-default: #FFFFFF;
  --color-button-primary-text-disabled: #FBFCFC;
  --color-button-primary-border-default: #614051;
  --color-button-primary-focus-ring: #614051;

  /* --- Button — secondary --- */
  --color-button-secondary-surface-default: #FFFFFF;
  --color-button-secondary-surface-hover: #F1F1F1;
  --color-button-secondary-surface-active: #E7E7E7;
  --color-button-secondary-surface-disabled: #F7F8FA;
  --color-button-secondary-text-default: #111111;
  --color-button-secondary-text-disabled: #909091;
  --color-button-secondary-border-default: #BDC8D7;
  --color-button-secondary-border-hover: #A3B3C7;
  --color-button-secondary-focus-ring: #614051;

  /* --- Button — ghost --- */
  --color-button-ghost-surface-default: transparent;
  --color-button-ghost-surface-hover: #F3F3F3;
  --color-button-ghost-surface-active: #EAEAEA;
  --color-button-ghost-surface-disabled: transparent;
  --color-button-ghost-text-default: #614051;
  --color-button-ghost-text-hover: #111111;
  --color-button-ghost-text-disabled: #B4A5AE;
  --color-button-ghost-border-default: transparent;
  --color-button-ghost-focus-ring: #614051;

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
  --color-input-text-placeholder: #9D8A95;
  --color-input-text-disabled: #B4A5AE;
  --color-input-border-default: #D6DDE6;
  --color-input-border-hover: #B6C3D3;
  --color-input-border-focus: #614051;
  --color-input-border-error: #FA8072;
  --color-input-border-disabled: #E6EAF0;

  /* --- Card --- */
  --color-card-surface-default: #FFFFFF;
  --color-card-surface-hover: #FAFAFA;
  --color-card-surface-muted: #F7F8FA;
  --color-card-border-default: #D6DDE6;
  --color-card-border-hover: #B6C3D3;
  --color-card-border-focus: #614051;

  /* --- Nav link --- */
  --color-nav-link-text-default: #614051;
  --color-nav-link-text-hover: #111111;
  --color-nav-link-text-active: #614051;
  --color-nav-link-surface-hover: #F5F5F5;
  --color-nav-link-indicator: #FADA5E;

  /* --- Link --- */
  --color-link-text-default: #614051;
  --color-link-text-hover: #422C37;
  --color-link-text-visited: #444344;

  /* --- Feedback — info --- */
  --color-feedback-info-surface: #ECE8EA;
  --color-feedback-info-text: #614051;
  --color-feedback-info-border: #8E7784;
  --color-feedback-info-icon: #614051;

  /* --- Feedback — success --- */
  --color-feedback-success-surface: #E9EFEB;
  --color-feedback-success-text: #4A7C59;
  --color-feedback-success-border: #7EA189;
  --color-feedback-success-icon: #4A7C59;

  /* --- Feedback — warning --- */
  --color-feedback-warning-surface: #FEFBEC;
  --color-feedback-warning-text: #FADA5E;
  --color-feedback-warning-border: #F9E38D;
  --color-feedback-warning-icon: #FADA5E;

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
| activity-card | `color.Blush→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| add-to-cart-button | `color.Aubergine→surface`, `color.Naples Yellow→emphasis`, `color.Blush→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| api-reference-table | `color.Blush→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| app-shell | `color.Aubergine→surface`, `color.Naples Yellow→emphasis`, `color.Blush→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| archive-shelf | `color.Blush→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| article-body | `color.Blush→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| article-gallery | `color.Blush→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| article-preview-pane | `color.Blush→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| artifact-preview-panel | `color.Blush→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| assign-reviewer | `color.Aubergine→surface`, `color.Naples Yellow→emphasis`, `color.Blush→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| autocomplete | `color.Aubergine→surface`, `color.Naples Yellow→emphasis`, `color.Blush→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| avatar | `color.Blush→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| avatar-cluster | `color.Blush→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| back-button | `color.Aubergine→surface`, `color.Naples Yellow→emphasis`, `color.Blush→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| banner | `color.Blush→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| block-controls | `color.Blush→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| bottom-sheet | `color.Aubergine→surface`, `color.Naples Yellow→emphasis`, `color.Blush→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| breadcrumb | `color.Aubergine→surface`, `color.Naples Yellow→emphasis`, `color.Blush→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| byline-row | `color.Blush→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| calendar-grid | `color.Blush→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| category-pill | `color.Aubergine→surface`, `color.Naples Yellow→emphasis`, `color.Blush→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| chart-container | `color.Blush→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| chart-legend | `color.Blush→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| chart-panel | `color.Blush→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| chart-tooltip | `color.Aubergine→surface`, `color.Naples Yellow→emphasis`, `color.Blush→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| chat-input | `color.Aubergine→surface`, `color.Naples Yellow→emphasis`, `color.Blush→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| chat-message | `color.Blush→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| chat-thread | `color.Blush→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| checkbox | `color.Aubergine→surface`, `color.Naples Yellow→emphasis`, `color.Blush→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| chip | `color.Aubergine→surface`, `color.Naples Yellow→emphasis`, `color.Blush→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| citation-footnote | `color.Blush→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| color-swatch-selector | `color.Aubergine→surface`, `color.Naples Yellow→emphasis`, `color.Blush→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| column-header | `color.Blush→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| command-palette | `color.Aubergine→surface`, `color.Naples Yellow→emphasis`, `color.Blush→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| command-result-item | `color.Aubergine→surface`, `color.Naples Yellow→emphasis`, `color.Blush→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| comment-input | `color.Aubergine→surface`, `color.Naples Yellow→emphasis`, `color.Blush→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| comment-thread | `color.Blush→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| confirm-dialog | `color.Aubergine→surface`, `color.Naples Yellow→emphasis`, `color.Blush→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| content-card | `color.Blush→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| content-meta | `color.Blush→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| content-status-timeline | `color.Blush→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| context-panel | `color.Aubergine→surface`, `color.Naples Yellow→emphasis`, `color.Blush→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| contributor-roster | `color.Blush→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| cover-story | `color.Blush→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| cross-sell-grid | `color.Blush→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| cta-button | `color.Aubergine→surface`, `color.Naples Yellow→emphasis`, `color.Blush→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| curation-queue | `color.Blush→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| customer-logo | `color.Blush→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| data-table | `color.Blush→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| date-picker | `color.Aubergine→surface`, `color.Naples Yellow→emphasis`, `color.Blush→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| date-range-picker | `color.Aubergine→surface`, `color.Naples Yellow→emphasis`, `color.Blush→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| discount-badge | `color.Blush→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| draft-document | `color.Blush→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| draft-status-pill | `color.Blush→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| drop-cap | `color.Blush→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| editor-canvas | `color.Blush→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| editor-toolbar | `color.Blush→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| editorial-analytics-kpi | `color.Blush→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| editorial-calendar | `color.Blush→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| editorial-workflow | `color.Blush→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| empty-conversation-state | `color.Blush→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| empty-feed-illustration | `color.Blush→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| empty-state | `color.Blush→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| feature-article | `color.Blush→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| feature-comparison | `color.Blush→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| featured-story-card | `color.Blush→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| feed-item | `color.Blush→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| filter-chip | `color.Aubergine→surface`, `color.Naples Yellow→emphasis`, `color.Blush→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| filter-panel | `color.Aubergine→surface`, `color.Naples Yellow→emphasis`, `color.Blush→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| filter-sidebar | `color.Aubergine→surface`, `color.Naples Yellow→emphasis`, `color.Blush→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| filter-toolbar | `color.Blush→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| follow-button | `color.Aubergine→surface`, `color.Naples Yellow→emphasis`, `color.Blush→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| footnote | `color.Blush→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| form-actions | `color.Aubergine→surface`, `color.Naples Yellow→emphasis`, `color.Blush→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| form-section | `color.Aubergine→surface`, `color.Naples Yellow→emphasis`, `color.Blush→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| gentle-toast | `color.Blush→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| ghost-button | `color.Aubergine→surface`, `color.Naples Yellow→emphasis`, `color.Blush→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| heading-anchor | `color.Blush→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| icon-button | `color.Aubergine→surface`, `color.Naples Yellow→emphasis`, `color.Blush→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| image-thumbnail | `color.Blush→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| inline-alert | `color.Blush→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| inline-citation | `color.Blush→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| inline-format-menu | `color.Blush→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| insight-card | `color.Blush→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| issue-header | `color.Blush→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| issue-number | `color.Blush→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| issue-planner | `color.Blush→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| kanban-board | `color.Blush→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| kanban-card | `color.Blush→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| kanban-column | `color.Blush→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| kicker-eyebrow | `color.Blush→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| link-button | `color.Aubergine→surface`, `color.Naples Yellow→emphasis`, `color.Blush→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| link-card | `color.Blush→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| logo-cloud | `color.Blush→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| masthead | `color.Blush→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| mention-chip | `color.Blush→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| mention-popup | `color.Aubergine→surface`, `color.Naples Yellow→emphasis`, `color.Blush→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| message-artifact | `color.Blush→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| metric-highlight | `color.Blush→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| mobile-tab-bar | `color.Aubergine→surface`, `color.Naples Yellow→emphasis`, `color.Blush→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| mobile-topbar | `color.Aubergine→surface`, `color.Naples Yellow→emphasis`, `color.Blush→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| modal-dialog | `color.Aubergine→surface`, `color.Naples Yellow→emphasis`, `color.Blush→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| new-thread-button | `color.Aubergine→surface`, `color.Naples Yellow→emphasis`, `color.Blush→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| opening-spread | `color.Blush→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| original-price-strikethrough | `color.Blush→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| outline-sidebar | `color.Blush→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| pagination | `color.Aubergine→surface`, `color.Naples Yellow→emphasis`, `color.Blush→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| paragraph-block | `color.Blush→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| parameter-table | `color.Blush→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| pipeline-stage | `color.Blush→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| post-card | `color.Blush→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| press-quote | `color.Blush→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| prev-next-pager | `color.Aubergine→surface`, `color.Naples Yellow→emphasis`, `color.Blush→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| price-tag | `color.Blush→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| pricing-card | `color.Blush→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| primary-button | `color.Aubergine→surface`, `color.Naples Yellow→emphasis`, `color.Blush→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| product-card | `color.Blush→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| product-detail | `color.Blush→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| product-gallery | `color.Blush→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| product-grid | `color.Blush→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| product-hero-image | `color.Blush→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| profile-card | `color.Blush→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| prompt-composer | `color.Aubergine→surface`, `color.Naples Yellow→emphasis`, `color.Blush→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| prose-block | `color.Blush→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| publish-scheduler | `color.Aubergine→surface`, `color.Naples Yellow→emphasis`, `color.Blush→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| publishing-pipeline | `color.Blush→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| pull-quote | `color.Blush→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| quick-view-modal | `color.Aubergine→surface`, `color.Naples Yellow→emphasis`, `color.Blush→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| quote-block | `color.Blush→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| radio-group | `color.Aubergine→surface`, `color.Naples Yellow→emphasis`, `color.Blush→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| reaction-bar | `color.Blush→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| reading-analytics-kpi | `color.Blush→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| reading-mode-toggle | `color.Blush→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| reading-pane | `color.Blush→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| regenerate-button | `color.Aubergine→surface`, `color.Naples Yellow→emphasis`, `color.Blush→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| reply-composer | `color.Aubergine→surface`, `color.Naples Yellow→emphasis`, `color.Blush→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| revision-timeline | `color.Blush→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| row-actions | `color.Blush→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| schedule-cell | `color.Blush→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| search-field | `color.Aubergine→surface`, `color.Naples Yellow→emphasis`, `color.Blush→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| search-results | `color.Blush→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| secondary-button | `color.Aubergine→surface`, `color.Naples Yellow→emphasis`, `color.Blush→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| section-break | `color.Blush→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| section-header | `color.Blush→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| section-tabs | `color.Aubergine→surface`, `color.Naples Yellow→emphasis`, `color.Blush→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| segmented-control | `color.Aubergine→surface`, `color.Naples Yellow→emphasis`, `color.Blush→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| select | `color.Aubergine→surface`, `color.Naples Yellow→emphasis`, `color.Blush→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| share-sheet | `color.Aubergine→surface`, `color.Naples Yellow→emphasis`, `color.Blush→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| shortcut-hint | `color.Blush→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| sidebar-nav | `color.Aubergine→surface`, `color.Naples Yellow→emphasis`, `color.Blush→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| size-selector | `color.Aubergine→surface`, `color.Naples Yellow→emphasis`, `color.Blush→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| slash-command-menu | `color.Blush→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| soft-dialog | `color.Aubergine→surface`, `color.Naples Yellow→emphasis`, `color.Blush→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| sort-dropdown | `color.Aubergine→surface`, `color.Naples Yellow→emphasis`, `color.Blush→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| stat-card | `color.Blush→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| status-badge | `color.Blush→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| step-progress | `color.Blush→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| stop-generation-button | `color.Aubergine→surface`, `color.Naples Yellow→emphasis`, `color.Blush→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| streaming-cursor | `color.Blush→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| subscription-callout | `color.Blush→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| suggestion-card | `color.Blush→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| tab-bar | `color.Aubergine→surface`, `color.Naples Yellow→emphasis`, `color.Blush→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| table-of-contents | `color.Blush→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| tag | `color.Blush→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| tag-pill | `color.Blush→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| tag-taxonomy-manager | `color.Blush→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| text-field | `color.Aubergine→surface`, `color.Naples Yellow→emphasis`, `color.Blush→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| textarea | `color.Aubergine→surface`, `color.Naples Yellow→emphasis`, `color.Blush→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| thread-header | `color.Blush→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| thread-view | `color.Blush→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| time-picker | `color.Aubergine→surface`, `color.Naples Yellow→emphasis`, `color.Blush→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| timeline-stream | `color.Blush→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| toast | `color.Blush→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| tone-slider | `color.Aubergine→surface`, `color.Naples Yellow→emphasis`, `color.Blush→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| tooltip-guide | `color.Aubergine→surface`, `color.Naples Yellow→emphasis`, `color.Blush→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| topbar | `color.Aubergine→surface`, `color.Naples Yellow→emphasis`, `color.Blush→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| typing-indicator | `color.Blush→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| upgrade-banner | `color.Blush→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| user-menu | `color.Aubergine→surface`, `color.Naples Yellow→emphasis`, `color.Blush→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| variant-selector | `color.Aubergine→surface`, `color.Naples Yellow→emphasis`, `color.Blush→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| version-switcher | `color.Aubergine→surface`, `color.Naples Yellow→emphasis`, `color.Blush→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| wishlist-toggle | `color.Aubergine→surface`, `color.Naples Yellow→emphasis`, `color.Blush→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| wizard-layout | `color.Aubergine→surface`, `color.Naples Yellow→emphasis`, `color.Blush→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| workspace-switcher | `color.Aubergine→surface`, `color.Naples Yellow→emphasis`, `color.Blush→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |

## 19. Contrast Audit

| Background | Foreground | Ratio | Level |
|------------|------------|-------|-------|
| Naples Yellow | Ink | 13.72:1 | AAA (pass) |
| Blush | Ink | 12.02:1 | AAA (pass) |
| Aubergine | Paper | 8.90:1 | AAA (pass) |
| Aubergine | Naples Yellow | 6.46:1 | AA (pass) |
| Aubergine | Blush | 5.66:1 | AA (pass) |
| Aubergine | Ink | 2.12:1 | fail (FAIL) |
| Blush | Paper | 1.57:1 | fail (FAIL) |
| Naples Yellow | Paper | 1.38:1 | fail (FAIL) |
| Naples Yellow | Blush | 1.14:1 | fail (FAIL) |

## 20. Pattern Catalog

### Layout Patterns

- **sidebar-nav**: —
- **topbar**: —
- **workspace-header**: —
- **breadcrumb**: —
- **data-table**: —
- **column-header**: —
- **row-actions**: —
- **pagination**: —
- **sort-dropdown**: —
- **kpi-card**: —
- **stat-card**: —
- **insight-card**: —
- **activity-card**: —
- **section-header**: —
- **tag**: —
- **status-badge**: —
- **chip**: —
- **comment-thread**: —
- **avatar**: —
- **user-menu**: —
- **profile-card**: —
- **date-picker**: —
- **modal-dialog**: —
- **toast**: —
- **empty-state**: —
- **primary-button**: —
- **secondary-button**: —
- **ghost-button**: —
- **icon-button**: —
- **curation-queue**: —
- **draft-status-pill**: —
- **publishing-pipeline**: —
- **issue-planner**: —
- **contributor-roster**: —
- **article-preview-pane**: —
- **reading-analytics-kpi**: —
- **archive-shelf**: —
- **tag-taxonomy-manager**: —
- **workspace navigation**: app-shell, sidebar-nav, topbar, breadcrumb, workspace-switcher, tab-bar, context-panel
- **dashboard cards**: stat-card, insight-card, activity-card, section-header, chart-panel
- **data tables**: data-table, column-header, filter-chip, row-actions, pagination, filter-toolbar

### Interaction Patterns

- **filter-sidebar**: —
- **filter-chip**: —
- **search-field**: —
- **editorial-calendar**: —
- **editorial-analytics-kpi**: —
- **command palette**: command-palette, command-result-item, shortcut-hint
- **forms**: text-field, select, checkbox, textarea, form-section, radio-group, form-actions
- **notifications**: toast, inline-alert, empty-state, banner
