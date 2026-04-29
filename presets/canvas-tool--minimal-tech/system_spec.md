# Atelier System Spec

## 1. Positioning

- **Brand**: Atelier
- **Product**: 크리에이티브 팀을 위한 minimal-tech 톤 캔버스 · 레이어 · 인스펙터 도구 — keyboard-first, 픽셀 정밀, 한국어 1급
- **Audience**: 프로덕트 디자이너 / UI 디자이너, 디자인 시스템 메인테이너 / 디자인 엔지니어, 프로토타이퍼 / 인터랙션 디자이너
- **Platforms**: web, desktop
- **Accessibility floor**: WCAG 2.2 AA

## 2. Identity Guardrails

- **Brand keywords**: canvas-tool, creative, canvas, layer, inspector, toolbar, design-tool, vector, prototyping, whiteboard, minimal, precise
- **Anti-keywords**: playful, pastel, decorative, magazine-serif, marketing-heavy, cute, ornamental, dashboard-heavy, warm-editorial
- **Tone of voice**: precise, neutral, matter-of-fact, keyboard-first, pixel-precise
- **Visual direction**: neutral canvas surface, hairline borders, monochrome + single accent, thin inspector panels, dense layer tree, snap guide, ruler chrome, keyboard-first toolbar, pixel-precise grid, selection handle, minimap
- **Interaction direction**: keyboard-first (⌘ shortcut grid), layer drag reorder, inspector number input with scrub, snap to grid / guide, zoom and pan canvas, multi-select drag handle, undo redo stack, quick duplicate (⌥-drag), contextual toolbar, asset drag-to-canvas

## 3. Design Principles

- **Canvas-Tool**: `canvas-tool`를 시각적 선택과 인터랙션 선택의 기본 기준으로 삼습니다.
- **Creative**: `creative`를 시각적 선택과 인터랙션 선택의 기본 기준으로 삼습니다.
- **Canvas**: `canvas`를 시각적 선택과 인터랙션 선택의 기본 기준으로 삼습니다.
- **Layer**: `layer`를 시각적 선택과 인터랙션 선택의 기본 기준으로 삼습니다.

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
- **Preferred families**: Standard Violets, Pastel Blues, Standard Yellows
- **Palette strategy**: temperature=mixed, contrast=balanced, diversity=balanced, surface_style=tinted
- **Palette expansion**: supporting_color_count=10, combination_count=3, prefer_pairings=True
- **Palette roles**:
  - `primary` -> Cobalt Violet #804AA8 / Standard Violets
  - `accent` -> Amber #FFBF00 / Standard Yellows
  - `surface_tint` -> Misty Blue #B5C7EB / Pastel Blues
- **Selected colors**:
  - Ochre #CC7722 / Standard Oranges / 중명도, 중채도, 흙기 섞인 따뜻한 오렌지 / 안정감, 내추럴, 신뢰감, 지속성
  - Cobalt Violet #804AA8 / Standard Violets / 중명도, 중채도의 쿨 퍼플 톤 / 안정감, 차분함, 예술적, 신비감
  - Misty Blue #B5C7EB / Pastel Blues / 중명도, 저채도, 보라색이 섞인 뉴트럴 블루 톤 / 차분함, 사색적, 몽환적, 잔잔함, 감정의 여운
- **Palette candidates**:
  - signature-1 (Signature): primary=Ochre, accent=Cobalt Violet, surface_tint=Misty Blue / Ochre matches brand tone keywords.; Cobalt Violet is inside preferred families.
  - soft-spread-2 (Soft Spread): primary=Cobalt Violet, accent=Ochre, surface_tint=Ice Blue / Cobalt Violet is inside preferred families.; Ochre matches brand tone keywords.
  - assertive-3 (Assertive): primary=Ochre, accent=Cobalt Violet, surface_tint=Sky Blue / Ochre matches brand tone keywords.; Cobalt Violet is inside preferred families.
- **Expanded supporting colors**:
  - Pairing #C4C3D0 #C4C3D0 / Derived Pairing / pairing-swatch / Pairing #C4C3D0 comes from the seed pairing references.; Pairing #C4C3D0 is explicitly paired with Misty Blue.
  - Pairing #004E4E #004E4E / Derived Pairing / pairing-swatch / Pairing #004E4E comes from the seed pairing references.; Pairing #004E4E is explicitly paired with Amber.
  - Pairing #1A2633 #1A2633 / Derived Pairing / pairing-swatch / Pairing #1A2633 comes from the seed pairing references.; Pairing #1A2633 is explicitly paired with Amber.
  - Pairing #2C3456 #2C3456 / Derived Pairing / pairing-swatch / Pairing #2C3456 comes from the seed pairing references.; Pairing #2C3456 is explicitly paired with Misty Blue.
  - Pairing #3A4374 #3A4374 / Derived Pairing / pairing-swatch / Pairing #3A4374 comes from the seed pairing references.; Pairing #3A4374 is explicitly paired with Cobalt Violet.
  - Pairing #6A7BA2 #6A7BA2 / Derived Pairing / pairing-swatch / Pairing #6A7BA2 comes from the seed pairing references.; Pairing #6A7BA2 is explicitly paired with Misty Blue.
  - Pairing #F9F9F6 #F9F9F6 / Derived Pairing / pairing-swatch / Pairing #F9F9F6 comes from the seed pairing references.; Pairing #F9F9F6 is explicitly paired with Misty Blue.
  - Pairing #BEB5A7 #BEB5A7 / Derived Pairing / pairing-swatch / Pairing #BEB5A7 comes from the seed pairing references.; Pairing #BEB5A7 is explicitly paired with Cobalt Violet.
- **Expanded semantic roles**:
  - `brand_primary` -> Cobalt Violet #804AA8 / Standard Violets
  - `brand_accent` -> Amber #FFBF00 / Standard Yellows
  - `surface_tint` -> Misty Blue #B5C7EB / Pastel Blues
  - `canvas` -> Canvas White #F7F8FA / Generated Fallback
  - `surface` -> Paper #FFFFFF / Generated Fallback
  - `surface_muted` -> Surface Muted #EEF1F6 / Generated Fallback
  - `surface_elevated` -> Paper #FFFFFF / Generated Fallback
  - `border` -> Pairing #C4C3D0 #C4C3D0 / Derived Pairing
  - `border_strong` -> Pairing #BEB5A7 #BEB5A7 / Derived Pairing
  - `ink` -> Pairing #004E4E #004E4E / Derived Pairing
- **Combination lists**:
  - Seed Core: primary=Cobalt Violet, accent=Amber, surface_tint=Misty Blue
  - Surface System: canvas=Canvas White, surface=Paper, surface_tint=Misty Blue, border=Pairing #C4C3D0, ink=Pairing #004E4E, ink_muted=Muted Ink
  - Support Spectrum: support=Pairing #C4C3D0, support=Pairing #004E4E, support=Pairing #1A2633, support=Pairing #2C3456, support=Pairing #3A4374, support=Pairing #6A7BA2
- **Notes**: Cobalt Violet 를 primary 로 — 차분/예술적 cool purple, blue 비율 높아 minimal-tech 정체성 유지, Amber accent — Figma-esque single vivid accent, snap guide / selection handle / active toolbar group 강조, Misty Blue 는 surface_tint — 보라 섞인 뉴트럴 블루, ruler / grid overlay / property row 차분 surface, light mode 가 기본 — Figma/tldraw 관례, dark 는 옵션으로 제공, 기존 minimal-tech 4종 (Navy / Azure / Iris Violet / Bronze) 과 HEX 겹침 회피 — Cobalt Violet + Amber + Misty Blue 조합
- **Application rule**: 레퍼런스 컬러는 semantic token으로 번역해서 사용하고, 접근성과 theme 호환성을 우선합니다.

## 7. Visual Reference Signals

- **Mode**: local-images
- **Coverage**: source 0 / image 0 / selected 0
- **Rule**: visual references are advisory signals for motif and layout direction; official KB/spec remain the structural source of truth.
- **Provenance**: `observed` = directly measured from local pixels, `inferred` = synthesized from image/query/brand signals, `unverified` = reliable visual evidence not yet available.
- **Query seeds**: figma canvas inspector layer panel, framer canvas tool, excalidraw whiteboard, tldraw canvas, rive editor, spline 3d editor
### Visual Direction

- **Density**: dense (confidence 0.68, provenance inferred) / dashboard x2, control x1
- **Surface Style**: flat (confidence 0.41, provenance inferred) / minimal x2
- **Corner Style**: medium (confidence 0.24, provenance inferred) / fallback=medium
- **Typography Mood**: editorial (confidence 0.73, provenance inferred) / editorial x1, magazine x2, serif x2
- **Color balance**: temperature=unknown, contrast=unknown, neutral_bias=unknown, provenance=unverified

### Layout Rhythm

- **Split-pane workspace**: confidence 0.94 / provenance inferred / workspace x2, panel x5, editor x2, command x1
- **Data review surface**: confidence 0.85 / provenance inferred / grid x4, data x1, timeline x1
- **Narrative landing flow**: confidence 0.79 / provenance inferred / landing x1, hero x1, marketing x2
- **Editorial feed**: confidence 0.73 / provenance inferred / editorial x1, feed x1, magazine x2

### Image-derived Component Hints

- **Cards**: flat card planes를 기본으로 하고, 압축된 spacing과 얇은 divider 중심의 hierarchy. 중간 반경으로 제품 UI 절제 유지. / provenance inferred / surface=flat, density=dense, corner=medium
- **Navigation**: 고정 sidebar 또는 split-pane navigation을 우선하고, 현재 위치와 scope를 항상 명시한다. / provenance inferred / Split-pane workspace
- **Typography**: headline rhythm과 본문 리듬의 대비를 키우고, label/metadata는 조용하게 유지한다. / provenance inferred / typography_mood=editorial
- **Data Display**: 정보 밀도를 유지하되 thin dividers와 restrained accent로 hierarchy를 만든다. / provenance inferred / layout=data-review-surface, density=dense

### Synthesis Notes

- layout는 Split-pane workspace 기준으로 정리
- surface language는 flat 성향 우선
- typography mood는 editorial 축 유지
- density는 dense 기준으로 primitive spacing 조정
- palette temperature는 unknown 쪽을 우선
- Avoid: magazine serif hero
- Avoid: playful pastel illustration
- Avoid: marketing landing copy
- Avoid: dense data dashboard

## 8. Component Strategy

- **Product primitives**: canvas workspace, layer panel, layer item, layer thumbnail, inspector panel, property row, toolbar, toolbar group, contextual toolbar, ruler, snap guide, grid overlay, selection handle, zoom control, minimap, keyboard shortcut cheatsheet, command palette, asset library, export panel
- **Required families**: button, data-display, editorial, feedback, input, marketing, navigation, canvas, document, foundation, overlay, social, tool-chrome
- **Visual-reference archetypes**:

- **Data review table** (data-display / 0.94): data-table, column-header, row-actions, filter-toolbar, pagination
- **Marketing hero stack** (marketing / 0.94): hero-section, hero-headline, hero-visual, cta-button-group, trust-strip
- **Workspace shell** (navigation / 0.94): app-shell, sidebar-nav, workspace-switcher, breadcrumb, context-panel
- **Editorial content block** (editorial / 0.91): content-card, featured-story-card, section-header, content-meta, byline-row
- **Conversation sidecar** (overlay / 0.77): chat-panel, message-thread, message-composer, context-drawer
- **Dashboard insight module** (data-display / 0.61): stat-card, insight-card, chart-panel, section-header, filter-chip

- **button**: primary-button, secondary-button, ghost-button, icon-button, cta-button, link-button, form-actions, follow-button
- **data-display**: kanban-board, kanban-column, kanban-card, data-table, column-header, row-actions, search-results, tag / visual signals: Data review table (0.94), Dashboard insight module (0.61)
- **editorial**: editor-canvas, editor-toolbar, inline-format-menu, slash-command-menu, block-controls, content-card, featured-story-card, content-meta / visual signals: Editorial content block (0.91)
- **feedback**: inline-alert, empty-state, toast, shortcut-hint, status-badge, banner, step-progress, empty-feed-illustration
- **input**: text-field, search-field, segmented-control, property-row, format-selector, textarea, select, checkbox
- **marketing**: hero-section, hero-headline, hero-visual, cta-button-group, trust-strip / visual signals: Marketing hero stack (0.94)
- **navigation**: scope-switcher, mobile-topbar, mobile-tab-bar, back-button, section-tabs, pagination, app-shell, sidebar-nav / visual signals: Workspace shell (0.94)
- **canvas**: canvas-workspace, ruler, snap-guide, grid-overlay, selection-handle, zoom-control, minimap
- **document**: article-body, table-of-contents, heading-anchor, prose-block, reading-pane, footnote, link-card, api-reference-table
- **foundation**: command-result-item, shortcut-hint
- **overlay**: command-palette, bottom-sheet, modal-dialog, keyboard-shortcut-cheatsheet, command-result-item, autocomplete, confirm-dialog, mention-popup / visual signals: Conversation sidecar (0.77)
- **social**: feed-item, post-card, thread-view, reaction-bar, timeline-stream, avatar-cluster
- **tool-chrome**: layer-panel, layer-item, layer-thumbnail, inspector-panel, toolbar-group, contextual-toolbar, asset-library, asset-card

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

- Warning: [pitfall#3-rebrand] Cobalt Violet vs Misty Blue (blue): lightness diff 34, saturation diff 19 — possible rebrand remnant
- Warning: visual_reference.sources is empty

## 14. Quick Start

이 문서는 **Atelier System**의 디자인 시스템 사양입니다.

### 시작하기

1. **토큰 적용**: Drop-in CSS(아래 섹션 16)의 CSS 변수를 프로젝트에 복사합니다.
2. **컬러 세팅**: Color Reference(섹션 6)의 semantic role을 기준으로 surface/text/border를 잡습니다.
3. **타이포 세팅**: Token Strategy(섹션 5)의 font family와 type scale을 적용합니다.
4. **시각 방향 확인**: Visual Reference Signals(섹션 7)에서 density/surface/layout cue를 먼저 확인합니다.
5. **컴포넌트 구현**: Component Strategy(섹션 8)의 family 순서대로 하나씩 빌드합니다.

### 우선순위

핵심 primitive: **canvas workspace, layer panel, layer item, layer thumbnail, inspector panel**

이 primitive를 지원하는 컴포넌트부터 구현하고, 나머지는 필요에 따라 확장합니다.

## 15. DO / DON'T

### DO

- **Canvas-Tool**: canvas-tool와 충돌하는 컴포넌트 변형은 만들지 않기
- **Creative**: creative와 충돌하는 컴포넌트 변형은 만들지 않기
- **Canvas**: canvas와 충돌하는 컴포넌트 변형은 만들지 않기
- **Layer**: layer와 충돌하는 컴포넌트 변형은 만들지 않기
- 모든 시각적 선택에서 **canvas-tool, creative, canvas** 기준을 적용
- semantic token을 통해 컬러를 적용 (하드코딩 금지)
- 접근성 기준을 모든 text/surface 조합에서 먼저 검증
- 컴포넌트 변형 추가 전 기존 variant로 해결 가능한지 먼저 확인
- 아이콘은 SVG 컴포넌트 또는 Lucide/Heroicons/Phosphor/Tabler 등 라이브러리로 구현
- component_specs.md의 anatomy/states/token binding을 그대로 따라 완전히 구현

### DON'T

- **playful** 방향의 디자인 결정을 하지 않음
- **pastel** 방향의 디자인 결정을 하지 않음
- **decorative** 방향의 디자인 결정을 하지 않음
- **magazine-serif** 방향의 디자인 결정을 하지 않음
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
  --color-primary: #804AA8;
  --color-accent: #FFBF00;
  --color-surface-tint: #B5C7EB;

  /* --- Semantic roles (expanded) --- */
  --color-brand-primary: #804AA8;
  --color-brand-accent: #FFBF00;
  --color-surface-tint: #B5C7EB;
  --color-canvas: #F7F8FA;
  --color-surface: #FFFFFF;
  --color-surface-muted: #EEF1F6;
  --color-surface-elevated: #FFFFFF;
  --color-border: #C4C3D0;
  --color-border-strong: #BEB5A7;
  --color-ink: #004E4E;
  --color-ink-muted: #4B5563;
  --color-ink-subtle: #6A7BA2;
  --color-ink-inverse: #FFFFFF;
  --color-primary-support: #C4C3D0;
  --color-accent-support: #F9F9F6;
  --color-info: #C4C3D0;
  --color-success: #4A7C59;
  --color-warning: #FFBF00;
  --color-danger: #8B2252;
  --color-link: #804AA8;
  --color-link-hover: #6A3E8C;

  /* --- Button — primary --- */
  --color-button-primary-surface-default: #804AA8;
  --color-button-primary-surface-hover: #704193;
  --color-button-primary-surface-active: #653A85;
  --color-button-primary-surface-disabled: #C7B2D9;
  --color-button-primary-text-default: #FFFFFF;
  --color-button-primary-text-disabled: #FBFCFC;
  --color-button-primary-border-default: #804AA8;
  --color-button-primary-focus-ring: #804AA8;

  /* --- Button — secondary --- */
  --color-button-secondary-surface-default: #FFFFFF;
  --color-button-secondary-surface-hover: #F0F4F4;
  --color-button-secondary-surface-active: #E6EDED;
  --color-button-secondary-surface-disabled: #F7F8FA;
  --color-button-secondary-text-default: #004E4E;
  --color-button-secondary-text-disabled: #88ACAD;
  --color-button-secondary-border-default: #AEACBE;
  --color-button-secondary-border-hover: #9795AC;
  --color-button-secondary-focus-ring: #804AA8;

  /* --- Button — ghost --- */
  --color-button-ghost-surface-default: transparent;
  --color-button-ghost-surface-hover: #F2F6F6;
  --color-button-ghost-surface-active: #E8EFEF;
  --color-button-ghost-surface-disabled: transparent;
  --color-button-ghost-text-default: #4B5563;
  --color-button-ghost-text-hover: #004E4E;
  --color-button-ghost-text-disabled: #AAAFB6;
  --color-button-ghost-border-default: transparent;
  --color-button-ghost-focus-ring: #804AA8;

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
  --color-input-text-default: #004E4E;
  --color-input-text-placeholder: #90969F;
  --color-input-text-disabled: #AAAFB6;
  --color-input-border-default: #C4C3D0;
  --color-input-border-hover: #A8A6BA;
  --color-input-border-focus: #804AA8;
  --color-input-border-error: #8B2252;
  --color-input-border-disabled: #D2D1DB;

  /* --- Card --- */
  --color-card-surface-default: #FFFFFF;
  --color-card-surface-hover: #FAFBFB;
  --color-card-surface-muted: #F7F8FA;
  --color-card-border-default: #C4C3D0;
  --color-card-border-hover: #A8A6BA;
  --color-card-border-focus: #804AA8;

  /* --- Nav link --- */
  --color-nav-link-text-default: #4B5563;
  --color-nav-link-text-hover: #004E4E;
  --color-nav-link-text-active: #804AA8;
  --color-nav-link-surface-hover: #F5F8F8;
  --color-nav-link-indicator: #FFBF00;

  /* --- Link --- */
  --color-link-text-default: #804AA8;
  --color-link-text-hover: #653A85;
  --color-link-text-visited: #6F5881;

  /* --- Feedback — info --- */
  --color-feedback-info-surface: #F8F8F9;
  --color-feedback-info-text: #C4C3D0;
  --color-feedback-info-border: #D3D3DD;
  --color-feedback-info-icon: #C4C3D0;

  /* --- Feedback — success --- */
  --color-feedback-success-surface: #E9EFEB;
  --color-feedback-success-text: #4A7C59;
  --color-feedback-success-border: #7EA189;
  --color-feedback-success-icon: #4A7C59;

  /* --- Feedback — warning --- */
  --color-feedback-warning-surface: #FFF7E0;
  --color-feedback-warning-text: #FFBF00;
  --color-feedback-warning-border: #FDD04B;
  --color-feedback-warning-icon: #FFBF00;

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
| activity-card | `color.Misty Blue→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo` |
| api-reference-table | `color.Misty Blue→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo` |
| app-shell | `color.Cobalt Violet→surface`, `color.Amber→emphasis`, `color.Misty Blue→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo` |
| article-body | `color.Misty Blue→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo` |
| asset-card | `color.Misty Blue→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo` |
| asset-library | `color.Misty Blue→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo` |
| autocomplete | `color.Cobalt Violet→surface`, `color.Amber→emphasis`, `color.Misty Blue→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo` |
| avatar-cluster | `color.Misty Blue→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo` |
| back-button | `color.Cobalt Violet→surface`, `color.Amber→emphasis`, `color.Misty Blue→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo` |
| banner | `color.Misty Blue→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo` |
| block-controls | `color.Misty Blue→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo` |
| bottom-sheet | `color.Cobalt Violet→surface`, `color.Amber→emphasis`, `color.Misty Blue→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo` |
| breadcrumb | `color.Cobalt Violet→surface`, `color.Amber→emphasis`, `color.Misty Blue→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo` |
| byline-row | `color.Misty Blue→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo` |
| canvas-workspace | `color.Misty Blue→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo` |
| chart-panel | `color.Misty Blue→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo` |
| chat-input | `color.Cobalt Violet→surface`, `color.Amber→emphasis`, `color.Misty Blue→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo` |
| chat-message | `color.Misty Blue→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo` |
| chat-panel | `color.Cobalt Violet→surface`, `color.Amber→emphasis`, `color.Misty Blue→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo` |
| chat-thread | `color.Misty Blue→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo` |
| checkbox | `color.Cobalt Violet→surface`, `color.Amber→emphasis`, `color.Misty Blue→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo` |
| chip | `color.Cobalt Violet→surface`, `color.Amber→emphasis`, `color.Misty Blue→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo` |
| column-header | `color.Misty Blue→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo` |
| command-palette | `color.Cobalt Violet→surface`, `color.Amber→emphasis`, `color.Misty Blue→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo` |
| command-result-item | `color.Misty Blue→background`, `spacing.12→padding`, `radius.md→radius`, `color.Cobalt Violet→surface`, `color.Amber→emphasis`, `color.Misty Blue→background`, `spacing.12→padding`, `radius.md→radius` |
| comment-input | `color.Cobalt Violet→surface`, `color.Amber→emphasis`, `color.Misty Blue→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo` |
| comment-thread | `color.Misty Blue→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo` |
| confirm-dialog | `color.Cobalt Violet→surface`, `color.Amber→emphasis`, `color.Misty Blue→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo` |
| content-card | `color.Misty Blue→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo` |
| content-meta | `color.Misty Blue→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo` |
| context-drawer | `color.Cobalt Violet→surface`, `color.Amber→emphasis`, `color.Misty Blue→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo` |
| context-panel | `color.Cobalt Violet→surface`, `color.Amber→emphasis`, `color.Misty Blue→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo` |
| contextual-toolbar | `color.Misty Blue→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo` |
| cta-button | `color.Cobalt Violet→surface`, `color.Amber→emphasis`, `color.Misty Blue→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo` |
| cta-button-group | `color.Misty Blue→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo` |
| data-table | `color.Misty Blue→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo` |
| editor-canvas | `color.Misty Blue→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo` |
| editor-toolbar | `color.Misty Blue→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo` |
| empty-feed-illustration | `color.Misty Blue→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo` |
| empty-state | `color.Misty Blue→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo` |
| export-panel | `color.Misty Blue→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo` |
| featured-story-card | `color.Misty Blue→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo` |
| feed-item | `color.Misty Blue→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo` |
| filter-chip | `color.Cobalt Violet→surface`, `color.Amber→emphasis`, `color.Misty Blue→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo` |
| filter-panel | `color.Cobalt Violet→surface`, `color.Amber→emphasis`, `color.Misty Blue→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo` |
| filter-toolbar | `color.Misty Blue→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo` |
| follow-button | `color.Cobalt Violet→surface`, `color.Amber→emphasis`, `color.Misty Blue→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo` |
| footnote | `color.Misty Blue→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo` |
| form-actions | `color.Cobalt Violet→surface`, `color.Amber→emphasis`, `color.Misty Blue→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo` |
| form-section | `color.Cobalt Violet→surface`, `color.Amber→emphasis`, `color.Misty Blue→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo` |
| format-selector | `color.Cobalt Violet→surface`, `color.Amber→emphasis`, `color.Misty Blue→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo` |
| gentle-toast | `color.Misty Blue→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo` |
| ghost-button | `color.Cobalt Violet→surface`, `color.Amber→emphasis`, `color.Misty Blue→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo` |
| grid-overlay | `color.Misty Blue→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo` |
| heading-anchor | `color.Misty Blue→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo` |
| hero-headline | `color.Misty Blue→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo` |
| hero-section | `color.Misty Blue→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo` |
| hero-visual | `color.Misty Blue→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo` |
| icon-button | `color.Cobalt Violet→surface`, `color.Amber→emphasis`, `color.Misty Blue→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo` |
| inline-alert | `color.Misty Blue→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo` |
| inline-format-menu | `color.Misty Blue→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo` |
| insight-card | `color.Misty Blue→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo` |
| inspector-panel | `color.Misty Blue→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo` |
| kanban-board | `color.Misty Blue→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo` |
| kanban-card | `color.Misty Blue→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo` |
| kanban-column | `color.Misty Blue→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo` |
| keyboard-shortcut-cheatsheet | `color.Cobalt Violet→surface`, `color.Amber→emphasis`, `color.Misty Blue→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo` |
| layer-item | `color.Misty Blue→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo` |
| layer-panel | `color.Misty Blue→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo` |
| layer-thumbnail | `color.Misty Blue→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo` |
| link-button | `color.Cobalt Violet→surface`, `color.Amber→emphasis`, `color.Misty Blue→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo` |
| link-card | `color.Misty Blue→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo` |
| mention-popup | `color.Cobalt Violet→surface`, `color.Amber→emphasis`, `color.Misty Blue→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo` |
| message-composer | `color.Cobalt Violet→surface`, `color.Amber→emphasis`, `color.Misty Blue→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo` |
| message-thread | `color.Cobalt Violet→surface`, `color.Amber→emphasis`, `color.Misty Blue→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo` |
| minimap | `color.Misty Blue→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo` |
| mobile-tab-bar | `color.Cobalt Violet→surface`, `color.Amber→emphasis`, `color.Misty Blue→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo` |
| mobile-topbar | `color.Cobalt Violet→surface`, `color.Amber→emphasis`, `color.Misty Blue→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo` |
| modal-dialog | `color.Cobalt Violet→surface`, `color.Amber→emphasis`, `color.Misty Blue→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo` |
| pagination | `color.Cobalt Violet→surface`, `color.Amber→emphasis`, `color.Misty Blue→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo` |
| parameter-table | `color.Misty Blue→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo` |
| post-card | `color.Misty Blue→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo` |
| prev-next-pager | `color.Cobalt Violet→surface`, `color.Amber→emphasis`, `color.Misty Blue→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo` |
| primary-button | `color.Cobalt Violet→surface`, `color.Amber→emphasis`, `color.Misty Blue→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo` |
| property-row | `color.Cobalt Violet→surface`, `color.Amber→emphasis`, `color.Misty Blue→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo` |
| prose-block | `color.Misty Blue→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo` |
| radio-group | `color.Cobalt Violet→surface`, `color.Amber→emphasis`, `color.Misty Blue→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo` |
| reaction-bar | `color.Misty Blue→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo` |
| reading-pane | `color.Misty Blue→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo` |
| reply-composer | `color.Cobalt Violet→surface`, `color.Amber→emphasis`, `color.Misty Blue→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo` |
| row-actions | `color.Misty Blue→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo` |
| ruler | `color.Misty Blue→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo` |
| scope-switcher | `color.Cobalt Violet→surface`, `color.Amber→emphasis`, `color.Misty Blue→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo` |
| search-field | `color.Cobalt Violet→surface`, `color.Amber→emphasis`, `color.Misty Blue→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo` |
| search-results | `color.Misty Blue→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo` |
| secondary-button | `color.Cobalt Violet→surface`, `color.Amber→emphasis`, `color.Misty Blue→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo` |
| section-header | `color.Misty Blue→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo` |
| section-tabs | `color.Cobalt Violet→surface`, `color.Amber→emphasis`, `color.Misty Blue→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo` |
| segmented-control | `color.Cobalt Violet→surface`, `color.Amber→emphasis`, `color.Misty Blue→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo` |
| select | `color.Cobalt Violet→surface`, `color.Amber→emphasis`, `color.Misty Blue→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo` |
| selection-handle | `color.Misty Blue→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo` |
| share-sheet | `color.Cobalt Violet→surface`, `color.Amber→emphasis`, `color.Misty Blue→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo` |
| shortcut-hint | `color.Misty Blue→background`, `spacing.12→padding`, `radius.md→radius`, `color.Misty Blue→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo`, `font:Spoqa Han Sans Neo` |
| sidebar-nav | `color.Cobalt Violet→surface`, `color.Amber→emphasis`, `color.Misty Blue→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo` |
| slash-command-menu | `color.Misty Blue→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo` |
| snap-guide | `color.Misty Blue→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo` |
| soft-dialog | `color.Cobalt Violet→surface`, `color.Amber→emphasis`, `color.Misty Blue→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo` |
| stat-card | `color.Misty Blue→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo` |
| status-badge | `color.Misty Blue→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo` |
| step-progress | `color.Misty Blue→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo` |
| tab-bar | `color.Cobalt Violet→surface`, `color.Amber→emphasis`, `color.Misty Blue→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo` |
| table-of-contents | `color.Misty Blue→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo` |
| tag | `color.Misty Blue→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo` |
| tag-pill | `color.Misty Blue→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo` |
| text-field | `color.Cobalt Violet→surface`, `color.Amber→emphasis`, `color.Misty Blue→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo` |
| textarea | `color.Cobalt Violet→surface`, `color.Amber→emphasis`, `color.Misty Blue→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo` |
| thread-view | `color.Misty Blue→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo` |
| timeline-stream | `color.Misty Blue→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo` |
| toast | `color.Misty Blue→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo` |
| toolbar-group | `color.Misty Blue→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo` |
| tooltip-guide | `color.Cobalt Violet→surface`, `color.Amber→emphasis`, `color.Misty Blue→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo` |
| topbar | `color.Cobalt Violet→surface`, `color.Amber→emphasis`, `color.Misty Blue→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo` |
| trust-strip | `color.Misty Blue→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo` |
| version-switcher | `color.Cobalt Violet→surface`, `color.Amber→emphasis`, `color.Misty Blue→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo` |
| wizard-layout | `color.Cobalt Violet→surface`, `color.Amber→emphasis`, `color.Misty Blue→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo` |
| workspace-switcher | `color.Cobalt Violet→surface`, `color.Amber→emphasis`, `color.Misty Blue→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo` |
| zoom-control | `color.Misty Blue→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo` |

## 19. Contrast Audit

| Background | Foreground | Ratio | Level |
|------------|------------|-------|-------|
| Amber | Ink | 11.42:1 | AAA (pass) |
| Misty Blue | Ink | 11.09:1 | AAA (pass) |
| Cobalt Violet | Paper | 6.06:1 | AA (pass) |
| Cobalt Violet | Amber | 3.67:1 | AA-large (large-only) |
| Cobalt Violet | Misty Blue | 3.56:1 | AA-large (large-only) |
| Cobalt Violet | Ink | 3.11:1 | AA-large (large-only) |
| Misty Blue | Paper | 1.70:1 | fail (FAIL) |
| Amber | Paper | 1.65:1 | fail (FAIL) |
| Amber | Misty Blue | 1.03:1 | fail (FAIL) |

## 20. Pattern Catalog

### Layout Patterns

- **canvas workspace**: canvas-workspace, ruler, snap-guide, grid-overlay, selection-handle, zoom-control, minimap
- **layer panel**: —
- **layer item**: —
- **layer thumbnail**: —
- **inspector panel**: —
- **property row**: —
- **toolbar**: —
- **toolbar group**: —
- **contextual toolbar**: —
- **ruler**: —
- **snap guide**: —
- **grid overlay**: —
- **selection handle**: —
- **zoom control**: —
- **minimap**: —
- **keyboard shortcut cheatsheet**: —
- **asset library**: —
- **export panel**: —
- **workspace navigation**: app-shell, sidebar-nav, topbar, breadcrumb, workspace-switcher, tab-bar, context-panel
- **dashboard cards**: stat-card, insight-card, activity-card, section-header, chart-panel
- **data tables**: data-table, column-header, filter-chip, row-actions, pagination, filter-toolbar

### Interaction Patterns

- **command palette**: command-palette, command-result-item, shortcut-hint, scope-switcher
- **forms**: text-field, select, checkbox, textarea, form-section, radio-group, form-actions
- **notifications**: toast, inline-alert, empty-state, banner
