# Lattice System Spec

## 1. Positioning

- **Brand**: Lattice
- **Product**: 개발자용 API 레퍼런스 · 기술 문서 플랫폼 — TOC, article, code block, callout, API reference table 중심
- **Audience**: API 를 통합하는 외부 개발자, SDK/라이브러리를 학습하는 개발자, 내부 플랫폼 엔지니어 / DevEx 담당
- **Platforms**: web, desktop
- **Accessibility floor**: WCAG 2.2 AA

## 2. Identity Guardrails

- **Brand keywords**: reference-docs, api-docs, developer-docs, technical-writing, documentation, devtools, minimal, precise, reference, developer
- **Anti-keywords**: editorial, magazine-style, decorative, playful, marketing-heavy, ornamental, candy-pastel
- **Tone of voice**: precise, matter-of-fact, technical, clear, reference-grade
- **Visual direction**: cool neutral surfaces, hairline borders, monochrome + single accent, code-first hierarchy, dense toc sidebar, generous reading measure, inline code emphasis, syntax-highlight palette, anchor-linked headings, mono-first table chrome
- **Interaction direction**: search-first (⌘K), anchor-linked headings, copy-code inline, version switcher, edit-on-github, keyboard next/prev, sidebar collapse, language tab switch, prev/next pager, breadcrumb trail

## 3. Design Principles

- **Reference-Docs**: `reference-docs`를 시각적 선택과 인터랙션 선택의 기본 기준으로 삼습니다.
- **Api-Docs**: `api-docs`를 시각적 선택과 인터랙션 선택의 기본 기준으로 삼습니다.
- **Developer-Docs**: `developer-docs`를 시각적 선택과 인터랙션 선택의 기본 기준으로 삼습니다.
- **Technical-Writing**: `technical-writing`를 시각적 선택과 인터랙션 선택의 기본 기준으로 삼습니다.

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
- **Product type detected**: developer-tool
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
- **Preferred families**: Standard Violets, Deep Violets, Natural Violets, Pastel Violets
- **Palette strategy**: temperature=mixed, contrast=balanced, diversity=balanced, surface_style=tinted
- **Palette expansion**: supporting_color_count=10, combination_count=3, prefer_pairings=True
- **Palette roles**:
  - `primary` -> Iris Violet #5A4FCF / Natural Violets
  - `accent` -> Cerulean #2A52BE / Standard Blues
  - `surface_tint` -> Lavender Mist #E6E6FA / Pastel Violets
- **Selected colors**:
  - Cerulean #2A52BE / Standard Blues / 중명도, 중채도, 스탠다드한 청색 계열 / 안정감, 명료함, 신뢰, 여유, 시각적 청량감
  - Ochre #CC7722 / Standard Oranges / 중명도, 중채도, 흙기 섞인 따뜻한 오렌지 / 안정감, 내추럴, 신뢰감, 지속성
  - Sky Blue #87CEEB / Natural Blues / 고명도, 중채도의 밝은 쿨톤 / 청량함, 평화, 유연함, 긍정, 맑음
- **Palette candidates**:
  - signature-1 (Signature): primary=Cerulean, accent=Ochre, surface_tint=Sky Blue / Cerulean matches brand tone keywords.; Ochre matches brand tone keywords.
  - soft-spread-2 (Soft Spread): primary=Ochre, accent=Cerulean, surface_tint=Misty Blue / Ochre matches brand tone keywords.; Cerulean matches brand tone keywords.
- **Expanded supporting colors**:
  - Pairing #CAB7E1 #CAB7E1 / Derived Pairing / pairing-swatch / Pairing #CAB7E1 comes from the seed pairing references.; Pairing #CAB7E1 is explicitly paired with Iris Violet.
  - Pairing #D7CBEF #D7CBEF / Derived Pairing / pairing-swatch / Pairing #D7CBEF comes from the seed pairing references.; Pairing #D7CBEF is explicitly paired with Lavender Mist.
  - Pairing #C0C0C0 #C0C0C0 / Derived Pairing / pairing-swatch / Pairing #C0C0C0 comes from the seed pairing references.; Pairing #C0C0C0 is explicitly paired with Lavender Mist.
  - Pairing #D8D8D8 #D8D8D8 / Derived Pairing / pairing-swatch / Pairing #D8D8D8 comes from the seed pairing references.; Pairing #D8D8D8 is explicitly paired with Iris Violet.
  - Pairing #D9D9D9 #D9D9D9 / Derived Pairing / pairing-swatch / Pairing #D9D9D9 comes from the seed pairing references.; Pairing #D9D9D9 is explicitly paired with Cerulean.
  - Lavender Violet #967BB6 / Natural Violets / reference-color / Lavender Violet stays inside the preferred families.; Lavender Violet reinforces the brand mood signals.
  - Pairing #C7DAF0 #C7DAF0 / Derived Pairing / pairing-swatch / Pairing #C7DAF0 comes from the seed pairing references.; Pairing #C7DAF0 is explicitly paired with Lavender Mist.
  - Pairing #333333 #333333 / Derived Pairing / pairing-swatch / Pairing #333333 comes from the seed pairing references.; Pairing #333333 is explicitly paired with Iris Violet.
- **Expanded semantic roles**:
  - `brand_primary` -> Iris Violet #5A4FCF / Natural Violets
  - `brand_accent` -> Cerulean #2A52BE / Standard Blues
  - `surface_tint` -> Lavender Mist #E6E6FA / Pastel Violets
  - `canvas` -> Canvas White #F7F8FA / Generated Fallback
  - `surface` -> Paper #FFFFFF / Generated Fallback
  - `surface_muted` -> Surface Muted #EEF1F6 / Generated Fallback
  - `surface_elevated` -> Paper #FFFFFF / Generated Fallback
  - `border` -> Pairing #D8D8D8 #D8D8D8 / Derived Pairing
  - `border_strong` -> Pairing #C0C0C0 #C0C0C0 / Derived Pairing
  - `ink` -> Pairing #333333 #333333 / Derived Pairing
- **Combination lists**:
  - Seed Core: primary=Iris Violet, accent=Cerulean, surface_tint=Lavender Mist
  - Surface System: canvas=Canvas White, surface=Paper, surface_tint=Lavender Mist, border=Pairing #D8D8D8, ink=Pairing #333333, ink_muted=Muted Ink
  - Support Spectrum: support=Pairing #CAB7E1, support=Pairing #D7CBEF, support=Pairing #C0C0C0, support=Pairing #D8D8D8, support=Pairing #D9D9D9, support=Lavender Violet
- **Notes**: Iris Violet 를 primary 로 — 지적·정제된 톤, Blue 기가 강해 명료, Cerulean accent — 링크·inline code 강조용 안정적 블루, Lavender Mist 는 surface_tint — 코드 블록 배경·callout 바탕 차분 쿨 파스텔, light mode 가 기본 — Stripe/Vercel docs 관례, dark 는 toggle 지원, editorial-warm 대조군과 정반대 방향: cool + mono-first + monochromatic
- **Application rule**: 레퍼런스 컬러는 semantic token으로 번역해서 사용하고, 접근성과 theme 호환성을 우선합니다.

## 7. Visual Reference Signals

- **Mode**: local-images
- **Coverage**: source 0 / image 0 / selected 0
- **Rule**: visual references are advisory signals for motif and layout direction; official KB/spec remain the structural source of truth.
- **Provenance**: `observed` = directly measured from local pixels, `inferred` = synthesized from image/query/brand signals, `unverified` = reliable visual evidence not yet available.
- **Query seeds**: linear docs reference, stripe documentation api, vercel docs technical, mdn reference layout
### Visual Direction

- **Density**: dense (confidence 0.94, provenance inferred) / table x5
- **Surface Style**: tinted (confidence 0.37, provenance inferred) / warm x1, editorial x2
- **Corner Style**: medium (confidence 0.29, provenance inferred) / card x1
- **Typography Mood**: editorial (confidence 0.94, provenance inferred) / editorial x2, article x2, magazine x2
- **Color balance**: temperature=unknown, contrast=unknown, neutral_bias=unknown, provenance=unverified

### Layout Rhythm

- **Data review surface**: confidence 0.94 / provenance inferred / table x5
- **Editorial feed**: confidence 0.94 / provenance inferred / editorial x2, article x2, magazine x2
- **Split-pane workspace**: confidence 0.9 / provenance inferred / sidebar x4
- **Dashboard grid**: confidence 0.79 / provenance inferred / table x5

### Image-derived Component Hints

- **Cards**: low-elevation tinted cards를 기본으로 하고, 압축된 spacing과 얇은 divider 중심의 hierarchy. 중간 반경으로 제품 UI 절제 유지. / provenance inferred / surface=tinted, density=dense, corner=medium
- **Navigation**: 고정 sidebar 또는 split-pane navigation을 우선하고, 현재 위치와 scope를 항상 명시한다. / provenance inferred / Split-pane workspace
- **Typography**: headline rhythm과 본문 리듬의 대비를 키우고, label/metadata는 조용하게 유지한다. / provenance inferred / typography_mood=editorial
- **Data Display**: 정보 밀도를 유지하되 thin dividers와 restrained accent로 hierarchy를 만든다. / provenance inferred / layout=dashboard-grid, density=dense

### Synthesis Notes

- layout는 Data review surface 기준으로 정리
- surface language는 tinted 성향 우선
- typography mood는 editorial 축 유지
- density는 dense 기준으로 primitive spacing 조정
- palette temperature는 unknown 쪽을 우선
- Avoid: magazine serif hero
- Avoid: glassmorphism
- Avoid: gradient-heavy surfaces
- Avoid: playful illustrations

## 8. Component Strategy

- **Product primitives**: article body, table of contents, heading anchor, code block, inline code, api reference table, parameter table, callout, admonition, search chrome, version switcher, breadcrumbs, prev-next pager, footnote, link card, sidebar nav, language tab, reading pane, prose block
- **Required families**: button, data-display, editorial, feedback, input, marketing, navigation, document, overlay
- **Visual-reference archetypes**:

- **Data review table** (data-display / 0.94): data-table, column-header, row-actions, filter-toolbar, pagination
- **Editorial content block** (editorial / 0.94): content-card, featured-story-card, section-header, content-meta, byline-row
- **Workspace shell** (navigation / 0.94): app-shell, sidebar-nav, workspace-switcher, breadcrumb, context-panel
- **Dashboard insight module** (data-display / 0.55): stat-card, insight-card, chart-panel, section-header, filter-chip
- **Conversation sidecar** (overlay / 0.51): chat-panel, message-thread, message-composer, context-drawer
- **Marketing hero stack** (marketing / 0.49): hero-section, hero-headline, hero-visual, cta-button-group, trust-strip

- **button**: primary-button, secondary-button, ghost-button, icon-button, cta-button, link-button, copy-code-button, form-actions
- **data-display**: data-table, column-header, row-actions, search-results, kanban-board, kanban-column, kanban-card, stat-card / visual signals: Data review table (0.94), Dashboard insight module (0.55)
- **editorial**: editor-canvas, editor-toolbar, inline-format-menu, slash-command-menu, block-controls, content-card, featured-story-card, content-meta / visual signals: Editorial content block (0.94)
- **feedback**: inline-alert, empty-state, toast, banner, status-badge, step-progress, shortcut-hint
- **input**: text-field, search-field, segmented-control, filter-chip, filter-panel, textarea, select, checkbox
- **marketing**: hero-container, hero-eyebrow, hero-headline, hero-subheadline, hero-visual, hero-trust-strip
- **navigation**: mobile-topbar, mobile-tab-bar, back-button, section-tabs, prev-next-pager, version-switcher, pagination, app-shell / visual signals: Workspace shell (0.94)
- **document**: article-body, table-of-contents, heading-anchor, prose-block, reading-pane, footnote, link-card, api-reference-table
- **overlay**: bottom-sheet, modal-dialog, autocomplete, confirm-dialog, tooltip-guide, command-palette, command-result-item, mention-popup

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

- Warning: [pitfall#3-rebrand] Cerulean vs Sky Blue (blue): lightness diff 27, saturation diff 8 — possible rebrand remnant
- Warning: visual_reference.sources is empty

## 14. Quick Start

이 문서는 **Lattice System**의 디자인 시스템 사양입니다.

### 시작하기

1. **토큰 적용**: Drop-in CSS(아래 섹션 16)의 CSS 변수를 프로젝트에 복사합니다.
2. **컬러 세팅**: Color Reference(섹션 6)의 semantic role을 기준으로 surface/text/border를 잡습니다.
3. **타이포 세팅**: Token Strategy(섹션 5)의 font family와 type scale을 적용합니다.
4. **시각 방향 확인**: Visual Reference Signals(섹션 7)에서 density/surface/layout cue를 먼저 확인합니다.
5. **컴포넌트 구현**: Component Strategy(섹션 8)의 family 순서대로 하나씩 빌드합니다.

### 우선순위

핵심 primitive: **article body, table of contents, heading anchor, code block, inline code**

이 primitive를 지원하는 컴포넌트부터 구현하고, 나머지는 필요에 따라 확장합니다.

## 15. DO / DON'T

### DO

- **Reference-Docs**: reference-docs와 충돌하는 컴포넌트 변형은 만들지 않기
- **Api-Docs**: api-docs와 충돌하는 컴포넌트 변형은 만들지 않기
- **Developer-Docs**: developer-docs와 충돌하는 컴포넌트 변형은 만들지 않기
- **Technical-Writing**: technical-writing와 충돌하는 컴포넌트 변형은 만들지 않기
- 모든 시각적 선택에서 **reference-docs, api-docs, developer-docs** 기준을 적용
- semantic token을 통해 컬러를 적용 (하드코딩 금지)
- 접근성 기준을 모든 text/surface 조합에서 먼저 검증
- 컴포넌트 변형 추가 전 기존 variant로 해결 가능한지 먼저 확인
- 아이콘은 SVG 컴포넌트 또는 Lucide/Heroicons/Phosphor/Tabler 등 라이브러리로 구현
- component_specs.md의 anatomy/states/token binding을 그대로 따라 완전히 구현

### DON'T

- **editorial** 방향의 디자인 결정을 하지 않음
- **magazine-style** 방향의 디자인 결정을 하지 않음
- **decorative** 방향의 디자인 결정을 하지 않음
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
  --color-primary: #5A4FCF;
  --color-accent: #2A52BE;
  --color-surface-tint: #E6E6FA;

  /* --- Semantic roles (expanded) --- */
  --color-brand-primary: #5A4FCF;
  --color-brand-accent: #2A52BE;
  --color-surface-tint: #E6E6FA;
  --color-canvas: #F7F8FA;
  --color-surface: #FFFFFF;
  --color-surface-muted: #EEF1F6;
  --color-surface-elevated: #FFFFFF;
  --color-border: #D8D8D8;
  --color-border-strong: #C0C0C0;
  --color-ink: #333333;
  --color-ink-muted: #4B5563;
  --color-ink-subtle: #6B7280;
  --color-ink-inverse: #FFFFFF;
  --color-primary-support: #CAB7E1;
  --color-accent-support: #C7DAF0;
  --color-info: #CAB7E1;
  --color-success: #4A7C59;
  --color-warning: #F7F5EB;
  --color-danger: #8B2252;
  --color-link: #5A4FCF;
  --color-link-hover: #4135C1;

  /* --- Button — primary --- */
  --color-button-primary-surface-default: #5A4FCF;
  --color-button-primary-surface-hover: #4337C8;
  --color-button-primary-surface-active: #3E32B9;
  --color-button-primary-surface-disabled: #B8B4E9;
  --color-button-primary-text-default: #333333;
  --color-button-primary-text-disabled: #959696;
  --color-button-primary-border-default: #5A4FCF;
  --color-button-primary-focus-ring: #5A4FCF;

  /* --- Button — secondary --- */
  --color-button-secondary-surface-default: #FFFFFF;
  --color-button-secondary-surface-hover: #F3F3F3;
  --color-button-secondary-surface-active: #EBEBEB;
  --color-button-secondary-surface-disabled: #F7F8FA;
  --color-button-secondary-text-default: #333333;
  --color-button-secondary-text-disabled: #9F9FA0;
  --color-button-secondary-border-default: #C4C4C4;
  --color-button-secondary-border-hover: #AFAFAF;
  --color-button-secondary-focus-ring: #5A4FCF;

  /* --- Button — ghost --- */
  --color-button-ghost-surface-default: transparent;
  --color-button-ghost-surface-hover: #F5F5F5;
  --color-button-ghost-surface-active: #EDEDED;
  --color-button-ghost-surface-disabled: transparent;
  --color-button-ghost-text-default: #4B5563;
  --color-button-ghost-text-hover: #333333;
  --color-button-ghost-text-disabled: #AAAFB6;
  --color-button-ghost-border-default: transparent;
  --color-button-ghost-focus-ring: #5A4FCF;

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
  --color-input-text-placeholder: #90969F;
  --color-input-text-disabled: #AAAFB6;
  --color-input-border-default: #D8D8D8;
  --color-input-border-hover: #BEBEBE;
  --color-input-border-focus: #5A4FCF;
  --color-input-border-error: #8B2252;
  --color-input-border-disabled: #E5E5E5;

  /* --- Card --- */
  --color-card-surface-default: #FFFFFF;
  --color-card-surface-hover: #FBFBFB;
  --color-card-surface-muted: #F7F8FA;
  --color-card-border-default: #D8D8D8;
  --color-card-border-hover: #BEBEBE;
  --color-card-border-focus: #5A4FCF;

  /* --- Nav link --- */
  --color-nav-link-text-default: #4B5563;
  --color-nav-link-text-hover: #333333;
  --color-nav-link-text-active: #5A4FCF;
  --color-nav-link-surface-hover: #F7F7F7;
  --color-nav-link-indicator: #2A52BE;

  /* --- Link --- */
  --color-link-text-default: #5A4FCF;
  --color-link-text-hover: #3E32B9;
  --color-link-text-visited: #5C54B1;

  /* --- Feedback — info --- */
  --color-feedback-info-surface: #F9F6FB;
  --color-feedback-info-text: #CAB7E1;
  --color-feedback-info-border: #D8CAE8;
  --color-feedback-info-icon: #CAB7E1;

  /* --- Feedback — success --- */
  --color-feedback-success-surface: #E9EFEB;
  --color-feedback-success-text: #4A7C59;
  --color-feedback-success-border: #7EA189;
  --color-feedback-success-icon: #4A7C59;

  /* --- Feedback — warning --- */
  --color-feedback-warning-surface: #FEFEFD;
  --color-feedback-warning-text: #F7F5EB;
  --color-feedback-warning-border: #F7F6F0;
  --color-feedback-warning-icon: #F7F5EB;

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
| activity-card | `color.Lavender Mist→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo` |
| admonition-block | `color.Lavender Mist→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo` |
| api-reference-table | `color.Lavender Mist→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo` |
| app-shell | `color.Iris Violet→surface`, `color.Cerulean→emphasis`, `color.Lavender Mist→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo` |
| article-body | `color.Lavender Mist→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo` |
| autocomplete | `color.Iris Violet→surface`, `color.Cerulean→emphasis`, `color.Lavender Mist→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo` |
| back-button | `color.Iris Violet→surface`, `color.Cerulean→emphasis`, `color.Lavender Mist→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo` |
| banner | `color.Lavender Mist→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo` |
| block-controls | `color.Lavender Mist→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo` |
| bottom-sheet | `color.Iris Violet→surface`, `color.Cerulean→emphasis`, `color.Lavender Mist→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo` |
| breadcrumb | `color.Iris Violet→surface`, `color.Cerulean→emphasis`, `color.Lavender Mist→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo` |
| byline-row | `color.Lavender Mist→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo` |
| callout | `color.Lavender Mist→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo` |
| chart-panel | `color.Lavender Mist→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo` |
| chat-input | `color.Iris Violet→surface`, `color.Cerulean→emphasis`, `color.Lavender Mist→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo` |
| chat-message | `color.Lavender Mist→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo` |
| chat-thread | `color.Lavender Mist→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo` |
| checkbox | `color.Iris Violet→surface`, `color.Cerulean→emphasis`, `color.Lavender Mist→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo` |
| chip | `color.Iris Violet→surface`, `color.Cerulean→emphasis`, `color.Lavender Mist→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo` |
| code-block | `color.Lavender Mist→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo` |
| column-header | `color.Lavender Mist→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo` |
| command-palette | `color.Iris Violet→surface`, `color.Cerulean→emphasis`, `color.Lavender Mist→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo` |
| command-result-item | `color.Iris Violet→surface`, `color.Cerulean→emphasis`, `color.Lavender Mist→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo` |
| comment-input | `color.Iris Violet→surface`, `color.Cerulean→emphasis`, `color.Lavender Mist→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo` |
| comment-thread | `color.Lavender Mist→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo` |
| confirm-dialog | `color.Iris Violet→surface`, `color.Cerulean→emphasis`, `color.Lavender Mist→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo` |
| content-card | `color.Lavender Mist→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo` |
| content-meta | `color.Lavender Mist→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo` |
| context-panel | `color.Iris Violet→surface`, `color.Cerulean→emphasis`, `color.Lavender Mist→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo` |
| copy-code-button | `color.Iris Violet→surface`, `color.Cerulean→emphasis`, `color.Lavender Mist→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo` |
| cta-button | `color.Iris Violet→surface`, `color.Cerulean→emphasis`, `color.Lavender Mist→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo` |
| data-table | `color.Lavender Mist→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo` |
| editor-canvas | `color.Lavender Mist→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo` |
| editor-toolbar | `color.Lavender Mist→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo` |
| empty-state | `color.Lavender Mist→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo` |
| featured-story-card | `color.Lavender Mist→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo` |
| filter-chip | `color.Iris Violet→surface`, `color.Cerulean→emphasis`, `color.Lavender Mist→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo` |
| filter-panel | `color.Iris Violet→surface`, `color.Cerulean→emphasis`, `color.Lavender Mist→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo` |
| filter-toolbar | `color.Lavender Mist→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo` |
| footnote | `color.Lavender Mist→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo` |
| form-actions | `color.Iris Violet→surface`, `color.Cerulean→emphasis`, `color.Lavender Mist→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo` |
| form-section | `color.Iris Violet→surface`, `color.Cerulean→emphasis`, `color.Lavender Mist→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo` |
| ghost-button | `color.Iris Violet→surface`, `color.Cerulean→emphasis`, `color.Lavender Mist→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo` |
| heading-anchor | `color.Lavender Mist→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo` |
| hero-container | `color.Lavender Mist→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo` |
| hero-cta-group | `color.Iris Violet→surface`, `color.Cerulean→emphasis`, `color.Lavender Mist→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo` |
| hero-eyebrow | `color.Lavender Mist→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo` |
| hero-headline | `color.Lavender Mist→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo` |
| hero-subheadline | `color.Lavender Mist→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo` |
| hero-trust-strip | `color.Lavender Mist→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo` |
| hero-visual | `color.Lavender Mist→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo` |
| icon-button | `color.Iris Violet→surface`, `color.Cerulean→emphasis`, `color.Lavender Mist→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo` |
| inline-alert | `color.Lavender Mist→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo` |
| inline-code | `color.Lavender Mist→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo` |
| inline-format-menu | `color.Lavender Mist→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo` |
| insight-card | `color.Lavender Mist→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo` |
| kanban-board | `color.Lavender Mist→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo` |
| kanban-card | `color.Lavender Mist→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo` |
| kanban-column | `color.Lavender Mist→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo` |
| language-tab | `color.Lavender Mist→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo` |
| link-button | `color.Iris Violet→surface`, `color.Cerulean→emphasis`, `color.Lavender Mist→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo` |
| link-card | `color.Lavender Mist→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo` |
| mention-popup | `color.Iris Violet→surface`, `color.Cerulean→emphasis`, `color.Lavender Mist→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo` |
| mobile-tab-bar | `color.Iris Violet→surface`, `color.Cerulean→emphasis`, `color.Lavender Mist→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo` |
| mobile-topbar | `color.Iris Violet→surface`, `color.Cerulean→emphasis`, `color.Lavender Mist→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo` |
| modal-dialog | `color.Iris Violet→surface`, `color.Cerulean→emphasis`, `color.Lavender Mist→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo` |
| pagination | `color.Iris Violet→surface`, `color.Cerulean→emphasis`, `color.Lavender Mist→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo` |
| parameter-table | `color.Lavender Mist→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo` |
| prev-next-pager | `color.Iris Violet→surface`, `color.Cerulean→emphasis`, `color.Lavender Mist→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo` |
| primary-button | `color.Iris Violet→surface`, `color.Cerulean→emphasis`, `color.Lavender Mist→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo` |
| prose-block | `color.Lavender Mist→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo` |
| radio-group | `color.Iris Violet→surface`, `color.Cerulean→emphasis`, `color.Lavender Mist→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo` |
| reading-pane | `color.Lavender Mist→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo` |
| row-actions | `color.Lavender Mist→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo` |
| search-field | `color.Iris Violet→surface`, `color.Cerulean→emphasis`, `color.Lavender Mist→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo` |
| search-results | `color.Lavender Mist→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo` |
| secondary-button | `color.Iris Violet→surface`, `color.Cerulean→emphasis`, `color.Lavender Mist→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo` |
| section-header | `color.Lavender Mist→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo` |
| section-tabs | `color.Iris Violet→surface`, `color.Cerulean→emphasis`, `color.Lavender Mist→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo` |
| segmented-control | `color.Iris Violet→surface`, `color.Cerulean→emphasis`, `color.Lavender Mist→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo` |
| select | `color.Iris Violet→surface`, `color.Cerulean→emphasis`, `color.Lavender Mist→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo` |
| shortcut-hint | `color.Lavender Mist→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo` |
| sidebar-nav | `color.Iris Violet→surface`, `color.Cerulean→emphasis`, `color.Lavender Mist→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo` |
| slash-command-menu | `color.Lavender Mist→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo` |
| stat-card | `color.Lavender Mist→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo` |
| status-badge | `color.Lavender Mist→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo` |
| step-progress | `color.Lavender Mist→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo` |
| tab-bar | `color.Iris Violet→surface`, `color.Cerulean→emphasis`, `color.Lavender Mist→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo` |
| table-of-contents | `color.Lavender Mist→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo` |
| tag | `color.Lavender Mist→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo` |
| text-field | `color.Iris Violet→surface`, `color.Cerulean→emphasis`, `color.Lavender Mist→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo` |
| textarea | `color.Iris Violet→surface`, `color.Cerulean→emphasis`, `color.Lavender Mist→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo` |
| toast | `color.Lavender Mist→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo` |
| tooltip-guide | `color.Iris Violet→surface`, `color.Cerulean→emphasis`, `color.Lavender Mist→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo` |
| topbar | `color.Iris Violet→surface`, `color.Cerulean→emphasis`, `color.Lavender Mist→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo` |
| version-switcher | `color.Iris Violet→surface`, `color.Cerulean→emphasis`, `color.Lavender Mist→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo` |
| wizard-layout | `color.Iris Violet→surface`, `color.Cerulean→emphasis`, `color.Lavender Mist→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo` |
| workspace-switcher | `color.Iris Violet→surface`, `color.Cerulean→emphasis`, `color.Lavender Mist→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo` |

## 19. Contrast Audit

| Background | Foreground | Ratio | Level |
|------------|------------|-------|-------|
| Lavender Mist | Ink | 15.34:1 | AAA (pass) |
| Cerulean | Paper | 6.89:1 | AA (pass) |
| Iris Violet | Paper | 6.08:1 | AA (pass) |
| Cerulean | Lavender Mist | 5.60:1 | AA (pass) |
| Iris Violet | Lavender Mist | 4.94:1 | AA (pass) |
| Iris Violet | Ink | 3.11:1 | AA-large (large-only) |
| Cerulean | Ink | 2.74:1 | fail (FAIL) |
| Lavender Mist | Paper | 1.23:1 | fail (FAIL) |
| Iris Violet | Cerulean | 1.13:1 | fail (FAIL) |

## 20. Pattern Catalog

### Layout Patterns

- **article body**: —
- **table of contents**: —
- **heading anchor**: —
- **code block**: —
- **inline code**: —
- **api reference table**: —
- **parameter table**: —
- **callout**: —
- **admonition**: —
- **version switcher**: —
- **breadcrumbs**: —
- **prev-next pager**: —
- **footnote**: —
- **link card**: —
- **sidebar nav**: —
- **language tab**: —
- **reading pane**: —
- **prose block**: —
- **workspace navigation**: app-shell, sidebar-nav, topbar, breadcrumb, workspace-switcher, tab-bar, context-panel
- **dashboard cards**: stat-card, insight-card, activity-card, section-header, chart-panel
- **data tables**: data-table, column-header, filter-chip, row-actions, pagination, filter-toolbar

### Interaction Patterns

- **search chrome**: —
- **command palette**: command-palette, command-result-item, shortcut-hint
- **forms**: text-field, select, checkbox, textarea, form-section, radio-group, form-actions
- **notifications**: toast, inline-alert, empty-state, banner
