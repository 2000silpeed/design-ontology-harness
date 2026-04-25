# Meadow System Spec

## 1. Positioning

- **Brand**: Meadow
- **Product**: consumer wellness / habit admin — playful-soft 톤 pastel dashboard, 가계부 · 건강 · 습관 · 수면 · 명상 트래킹 admin console, 한국어 1급
- **Audience**: consumer wellness / habit 앱 운영팀 PM — 유저 streak · 수면 · 명상 세션 · mood 지표 관찰, 건강 · 웰니스 스타트업 운영자 — cohort 리텐션 + wellness score + habit-calendar 운영, 가계부 · 저축 · 목표 트래킹 앱 admin — goal-tracker + streak-indicator + gentle nudge
- **Platforms**: web, mobile-web
- **Accessibility floor**: WCAG 2.2 AA

## 2. Identity Guardrails

- **Brand keywords**: dashboard, admin, consumer, wellness, habit, tracking, mindful, calm, soft, rounded, pastel, friendly, playful, gentle, warm
- **Anti-keywords**: minimal-tech-cool, corporate-navy, bold-saturated, magazine-serif, high-contrast, dense-only, enterprise-sharp
- **Tone of voice**: friendly, warm, encouraging, gentle, approachable, mindful
- **Visual direction**: rounded corners, pastel surfaces, soft shadow, gentle card, warm periwinkle primary, peach puff accent, mauve dreamy surface, habit streak flame, wellness score gauge, mood color gradient, illustrated empty state
- **Interaction direction**: gentle nudge, soft toast, rounded dialog, habit streak celebration, mood check quick-select, wellness score animated, swipe archive, pull-to-refresh, optimistic reaction

## 3. Design Principles

- **Dashboard**: `dashboard`를 시각적 선택과 인터랙션 선택의 기본 기준으로 삼습니다.
- **Admin**: `admin`를 시각적 선택과 인터랙션 선택의 기본 기준으로 삼습니다.
- **Consumer**: `consumer`를 시각적 선택과 인터랙션 선택의 기본 기준으로 삼습니다.
- **Wellness**: `wellness`를 시각적 선택과 인터랙션 선택의 기본 기준으로 삼습니다.

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

- **Heading**: Noto Sans KR
- **Body**: Noto Sans KR
- **Korean**: Noto Sans KR
- **Mono**: Fira Code
- **Product type detected**: dashboard
- **Pairing source**: auto-scored
- **Line height**: relaxed
- **Type scale**: base 14px, ratio 1.2 (xs=11px, sm=12px, md=14px, lg=17px, xl=20px, 2xl=24px, 3xl=29px)
- **Strategy**:
  - 단일 서체(Noto Sans KR)로 weight 대비 위계 — 일관성 우선
  - 한글 서체: Noto Sans KR — 라틴과 x-height/weight 조화
  - 모노스페이스: Fira Code — 코드/데이터 영역 전용
  - calm 키워드 → comfortable spacing, 과한 weight 대비 지양
- **Heading note**: Google의 범용 서체. 전 세계 문자 지원. Noto Sans KR은 한글 최적화.
- **Body note**: Google의 범용 서체. 전 세계 문자 지원. Noto Sans KR은 한글 최적화.
- **Korean rationale**: Noto Sans KR — Google이 만든 범용 한글 서체. 글자폭이 넓어서 여유 있는 레이아웃에 적합. 다국어 지원이 필요한 서비스의 기본 선택.
- **Heading tracking**: xl=-0.01em, 2xl=-0.01em, 3xl=-0.01em
- **Primary script**: korean
- **Hangul headline defaults**: Noto Sans KR | line-height 1.25-1.4 | tracking -0.01em
- **Hangul body defaults**: Noto Sans KR | line-height 1.6-1.8 | label line-height 1.45-1.55
- **Wrap defaults**: headline word-break=keep-all, headline text-wrap=balance, body word-break=keep-all
- **Scale guidance**: 한글 hero/section heading은 영문 시안보다 한 단계 작은 스케일에서 시작해 wrap을 확인한 뒤 확장한다.
- **Hangul warning**: 좁은 UI 공간 — 글자폭이 넓어서 공간을 많이 차지
- **Hangul warning**: 좁은 UI 공간 — 글자폭이 넓어서 공간을 많이 차지
- **Loading**: Noto Sans KR(preload), Fira Code(lazy) | display: swap

## 6. Color Reference

- **Source**: REFERENCE X Vol.1 - Color Reference (/Users/sungwoon/ai-projects/design-ontology-harness/docs/color-reference.md)
- **Selection mode**: manual
- **Preferred families**: Pastel Violets, Pastel Oranges, Pantone Trend Violets
- **Palette strategy**: temperature=warm, contrast=soft, diversity=balanced, surface_style=tinted
- **Palette expansion**: supporting_color_count=10, combination_count=3, prefer_pairings=True
- **Palette roles**:
  - `primary` -> Periwinkle #8E9AF1 / Pastel Violets
  - `accent` -> Peach Puff #FFDAB9 / Pastel Oranges
  - `surface_tint` -> Mauve #E0B0FF / Pastel Violets
- **Selected colors**:
  - Apricot #FFB27F / Natural Oranges / 밝은 명도, 낮은 채도, 살짝 핑크빛이 도는 부드러운 오렌지 / 따뜻함, 부드러움, 친근함, 여유, 자연스러움
  - Peach Puff #FFDAB9 / Pastel Oranges / 고명도, 저채도, 오렌지와 핑크 사이의 파스텔 계열 / 따뜻함, 부드러움, 순수함, 친근함, 생기
  - Salmon #FA8072 / Pastel Reds / 밝고 따뜻한 핑크 오렌지 톤 / 따뜻함, 부드러움, 친근함, 자연스러움
- **Palette candidates**:
  - signature-1 (Signature): primary=Apricot, accent=Peach Puff, surface_tint=Salmon / Apricot matches brand tone keywords.; Peach Puff is inside preferred families.
  - soft-spread-2 (Soft Spread): primary=Apricot, accent=Salmon, surface_tint=Peach Puff / Apricot matches brand tone keywords.; Salmon matches brand tone keywords.
- **Expanded supporting colors**:
  - Apricot #FFB27F / Natural Oranges / reference-color / Apricot reinforces the brand mood signals.
  - Salmon #FA8072 / Pastel Reds / reference-color / Salmon reinforces the brand mood signals.
  - Wheat #F5DEB3 / Natural Yellows / reference-color / Wheat reinforces the brand mood signals.
  - Creamsicle #FFD7A0 / Pastel Oranges / reference-color / Creamsicle stays inside the preferred families.; Creamsicle reinforces the brand mood signals.
  - Buttercream #F3E5AB / Pastel Yellows / reference-color / Buttercream reinforces the brand mood signals.
  - Terracotta #E2725B / Natural Reds / reference-color / Terracotta reinforces the brand mood signals.
  - Cornsilk #FFF8DC / Pastel Yellows / reference-color / Cornsilk reinforces the brand mood signals.
  - Celadon #ACE1AF / Pastel Greens / reference-color / Celadon reinforces the brand mood signals.
- **Expanded semantic roles**:
  - `brand_primary` -> Periwinkle #8E9AF1 / Pastel Violets
  - `brand_accent` -> Peach Puff #FFDAB9 / Pastel Oranges
  - `surface_tint` -> Mauve #E0B0FF / Pastel Violets
  - `canvas` -> Canvas White #F7F8FA / Generated Fallback
  - `surface` -> Paper #FFFFFF / Generated Fallback
  - `surface_muted` -> Surface Muted #EEF1F6 / Generated Fallback
  - `surface_elevated` -> Paper #FFFFFF / Generated Fallback
  - `border` -> Border Neutral #D6DDE6 / Generated Fallback
  - `border_strong` -> Border Strong #B0BAC7 / Generated Fallback
  - `ink` -> Ink #111111 / Generated Fallback
- **Combination lists**:
  - Seed Core: primary=Periwinkle, accent=Peach Puff, surface_tint=Mauve
  - Surface System: canvas=Canvas White, surface=Paper, surface_tint=Mauve, border=Border Neutral, ink=Ink, ink_muted=Muted Ink
  - Support Spectrum: support=Apricot, support=Salmon, support=Wheat, support=Creamsicle, support=Buttercream, support=Terracotta
- **Notes**: Periwinkle #8E9AF1 primary — 푸른빛 웜 퍼플, sidebar-nav active / primary-button / streak-indicator / wellness-score ring / habit-calendar today cell / goal-tracker progress, Peach Puff #FFDAB9 accent — warm pastel 오렌지, mood-check happy / insight-card accent / habit-streak flame / gentle-toast 성공 / goal-tracker complete, Mauve #E0B0FF surface_tint — dreamy pastel violet-rose, dashboard card soft surface / empty-state illustration / filter-chip soft group bg / row hover, light mode 가 기본 — consumer wellness admin 관례, dark 옵션 제공 (warm deep neutral + 채도 낮춘 Periwinkle/Peach Puff + Mauve soft border), 기존 15종 프리셋 HEX 와 겹침 0 — Periwinkle/Peach Puff/Mauve 조합, bloom playful-soft (community-feed) 의 #F88379/#98FF98/#FFF8DC 와 전면 차별화 — dashboard--playful-soft 정체성은 violet-pink 몽환 + warm peach accent, minimal-tech / corporate-trust 의 cool 무채색 팔레트와 정반대 — rounded + warm pastel + soft shadow
- **Application rule**: 레퍼런스 컬러는 semantic token으로 번역해서 사용하고, 접근성과 theme 호환성을 우선합니다.

## 7. Visual Reference Signals

- **Mode**: local-images
- **Coverage**: source 0 / image 0 / selected 0
- **Rule**: visual references are advisory signals for motif and layout direction; official KB/spec remain the structural source of truth.
- **Provenance**: `observed` = directly measured from local pixels, `inferred` = synthesized from image/query/brand signals, `unverified` = reliable visual evidence not yet available.
- **Query seeds**: cal.com booking dashboard, notion habit tracker, flo wellness dashboard, finch self care dashboard, calm meditation admin, headspace session stats
### Visual Direction

- **Density**: dense (confidence 0.94, provenance inferred) / dashboard x7, table x2
- **Surface Style**: tinted (confidence 0.79, provenance inferred) / warm x3, editorial x1, soft x9
- **Corner Style**: round (confidence 0.94, provenance inferred) / rounded x5, soft x9
- **Typography Mood**: utilitarian (confidence 0.94, provenance inferred) / dashboard x7, admin x4, enterprise x1
- **Color balance**: temperature=unknown, contrast=unknown, neutral_bias=unknown, provenance=unverified

### Layout Rhythm

- **Dashboard grid**: confidence 0.94 / provenance inferred / dashboard x7, kpi x2, chart x1, table x2
- **Data review surface**: confidence 0.94 / provenance inferred / table x2, grid x3, data x1, filter x1
- **Split-pane workspace**: confidence 0.94 / provenance inferred / workspace x1, sidebar x2, panel x1, navigation x1
- **Editorial feed**: confidence 0.71 / provenance inferred / editorial x1, feed x1, magazine x2

### Image-derived Component Hints

- **Cards**: low-elevation tinted cards를 기본으로 하고, 압축된 spacing과 얇은 divider 중심의 hierarchy. soft round corner를 기본값으로 유지. / provenance inferred / surface=tinted, density=dense, corner=round
- **Navigation**: 고정 sidebar 또는 split-pane navigation을 우선하고, 현재 위치와 scope를 항상 명시한다. / provenance inferred / Split-pane workspace
- **Typography**: 정보 밀도에 맞춰 type scale 차이를 줄이고 table/list label의 정렬 정확도를 우선한다. / provenance inferred / typography_mood=utilitarian
- **Data Display**: 정보 밀도를 유지하되 thin dividers와 restrained accent로 hierarchy를 만든다. / provenance inferred / layout=dashboard-grid, density=dense

### Synthesis Notes

- layout는 Dashboard grid 기준으로 정리
- surface language는 tinted 성향 우선
- typography mood는 utilitarian 축 유지
- density는 dense 기준으로 primitive spacing 조정
- palette temperature는 unknown 쪽을 우선
- Avoid: corporate navy dense table
- Avoid: bold saturated hero banner
- Avoid: magazine editorial pull-quote
- Avoid: commerce product grid

## 8. Component Strategy

- **Product primitives**: sidebar navigation, workspace switcher, dashboard card, kpi card, data table, filter chip, streak indicator, habit calendar, wellness score, mood check, session tracker, insight card, goal tracker, gentle toast, soft dialog, user list, cohort matrix, retention chart, activity feed, settings panel
- **Required families**: button, data-display, editorial, feedback, input, marketing, navigation, dashboard-growth, dashboard-wellness, overlay, social
- **Visual-reference archetypes**:

- **Dashboard insight module** (data-display / 0.94): stat-card, insight-card, chart-panel, section-header, filter-chip
- **Data review table** (data-display / 0.94): data-table, column-header, row-actions, filter-toolbar, pagination
- **Workspace shell** (navigation / 0.94): app-shell, sidebar-nav, workspace-switcher, breadcrumb, context-panel
- **Editorial content block** (editorial / 0.8): content-card, featured-story-card, section-header, content-meta, byline-row
- **Conversation sidecar** (overlay / 0.57): chat-panel, message-thread, message-composer, context-drawer

- **button**: primary-button, secondary-button, ghost-button, icon-button, cta-button, link-button, form-actions, follow-button
- **data-display**: stat-card, insight-card, activity-card, section-header, data-table, column-header, row-actions, tag / visual signals: Dashboard insight module (0.94), Data review table (0.94)
- **editorial**: editor-canvas, editor-toolbar, inline-format-menu, slash-command-menu, block-controls, content-card, featured-story-card, content-meta / visual signals: Editorial content block (0.8)
- **feedback**: inline-alert, empty-state, toast, status-badge, empty-feed-illustration, gentle-toast, banner, step-progress
- **input**: text-field, search-field, segmented-control, filter-chip, textarea, select, checkbox, radio-group
- **marketing**: hero-container, hero-eyebrow, hero-headline, hero-subheadline, hero-visual, hero-trust-strip, logo-cloud, customer-logo
- **navigation**: mobile-topbar, mobile-tab-bar, back-button, section-tabs, pagination, filter-bar, app-shell, sidebar-nav / visual signals: Workspace shell (0.94)
- **dashboard-growth**: activation-funnel, cohort-matrix, referral-widget, retention-chart, conversion-funnel, experiment-panel, goal-tracker, user-list
- **dashboard-wellness**: dashboard-card, streak-indicator, habit-calendar, wellness-score, mood-check, mood-chart, session-tracker, session-timeline
- **overlay**: bottom-sheet, modal-dialog, autocomplete, share-sheet, soft-dialog, chart-tooltip, confirm-dialog, user-menu / visual signals: Conversation sidecar (0.57)
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

- Warning: visual_reference.sources is empty

## 14. Quick Start

이 문서는 **Meadow System**의 디자인 시스템 사양입니다.

### 시작하기

1. **토큰 적용**: Drop-in CSS(아래 섹션 16)의 CSS 변수를 프로젝트에 복사합니다.
2. **컬러 세팅**: Color Reference(섹션 6)의 semantic role을 기준으로 surface/text/border를 잡습니다.
3. **타이포 세팅**: Token Strategy(섹션 5)의 font family와 type scale을 적용합니다.
4. **시각 방향 확인**: Visual Reference Signals(섹션 7)에서 density/surface/layout cue를 먼저 확인합니다.
5. **컴포넌트 구현**: Component Strategy(섹션 8)의 family 순서대로 하나씩 빌드합니다.

### 우선순위

핵심 primitive: **sidebar navigation, workspace switcher, dashboard card, kpi card, data table**

이 primitive를 지원하는 컴포넌트부터 구현하고, 나머지는 필요에 따라 확장합니다.

## 15. DO / DON'T

### DO

- **Dashboard**: dashboard와 충돌하는 컴포넌트 변형은 만들지 않기
- **Admin**: admin와 충돌하는 컴포넌트 변형은 만들지 않기
- **Consumer**: consumer와 충돌하는 컴포넌트 변형은 만들지 않기
- **Wellness**: wellness와 충돌하는 컴포넌트 변형은 만들지 않기
- 모든 시각적 선택에서 **dashboard, admin, consumer** 기준을 적용
- semantic token을 통해 컬러를 적용 (하드코딩 금지)
- 접근성 기준을 모든 text/surface 조합에서 먼저 검증
- 컴포넌트 변형 추가 전 기존 variant로 해결 가능한지 먼저 확인
- 아이콘은 SVG 컴포넌트 또는 Lucide/Heroicons/Phosphor/Tabler 등 라이브러리로 구현
- component_specs.md의 anatomy/states/token binding을 그대로 따라 완전히 구현

### DON'T

- **minimal-tech-cool** 방향의 디자인 결정을 하지 않음
- **corporate-navy** 방향의 디자인 결정을 하지 않음
- **bold-saturated** 방향의 디자인 결정을 하지 않음
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
  --font-heading: 'Noto Sans KR', serif;
  --font-body: 'Noto Sans KR', sans-serif;
  --font-mono: 'Fira Code', monospace;
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
  --color-primary: #8E9AF1;
  --color-accent: #FFDAB9;
  --color-surface-tint: #E0B0FF;

  /* --- Semantic roles (expanded) --- */
  --color-brand-primary: #8E9AF1;
  --color-brand-accent: #FFDAB9;
  --color-surface-tint: #E0B0FF;
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
  --color-primary-support: #E0B0FF;
  --color-accent-support: #FFB27F;
  --color-info: #B0E0E6;
  --color-success: #ACE1AF;
  --color-warning: #FFDAB9;
  --color-danger: #FA8072;
  --color-link: #8E9AF1;
  --color-link-hover: #6A7AED;

  /* --- Button — primary --- */
  --color-button-primary-surface-default: #8E9AF1;
  --color-button-primary-surface-hover: #7382EE;
  --color-button-primary-surface-active: #6171EB;
  --color-button-primary-surface-disabled: #CDD2F6;
  --color-button-primary-text-default: #111111;
  --color-button-primary-text-disabled: #848486;
  --color-button-primary-border-default: #8E9AF1;
  --color-button-primary-focus-ring: #8E9AF1;

  /* --- Button — secondary --- */
  --color-button-secondary-surface-default: #FFFFFF;
  --color-button-secondary-surface-hover: #F1F1F1;
  --color-button-secondary-surface-active: #E7E7E7;
  --color-button-secondary-surface-disabled: #F7F8FA;
  --color-button-secondary-text-default: #111111;
  --color-button-secondary-text-disabled: #909091;
  --color-button-secondary-border-default: #BDC8D7;
  --color-button-secondary-border-hover: #A3B3C7;
  --color-button-secondary-focus-ring: #8E9AF1;

  /* --- Button — ghost --- */
  --color-button-ghost-surface-default: transparent;
  --color-button-ghost-surface-hover: #F3F3F3;
  --color-button-ghost-surface-active: #EAEAEA;
  --color-button-ghost-surface-disabled: transparent;
  --color-button-ghost-text-default: #4B5563;
  --color-button-ghost-text-hover: #111111;
  --color-button-ghost-text-disabled: #AAAFB6;
  --color-button-ghost-border-default: transparent;
  --color-button-ghost-focus-ring: #8E9AF1;

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
  --color-input-border-focus: #8E9AF1;
  --color-input-border-error: #FA8072;
  --color-input-border-disabled: #E6EAF0;

  /* --- Card --- */
  --color-card-surface-default: #FFFFFF;
  --color-card-surface-hover: #FAFAFA;
  --color-card-surface-muted: #F7F8FA;
  --color-card-border-default: #D6DDE6;
  --color-card-border-hover: #B6C3D3;
  --color-card-border-focus: #8E9AF1;

  /* --- Nav link --- */
  --color-nav-link-text-default: #4B5563;
  --color-nav-link-text-hover: #111111;
  --color-nav-link-text-active: #8E9AF1;
  --color-nav-link-surface-hover: #F5F5F5;
  --color-nav-link-indicator: #FFDAB9;

  /* --- Link --- */
  --color-link-text-default: #8E9AF1;
  --color-link-text-hover: #6171EB;
  --color-link-text-visited: #8791DF;

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
| activation-funnel | `color.Mauve→background`, `spacing.12→padding`, `radius.md→radius`, `font:Noto Sans KR` |
| activity-card | `color.Mauve→background`, `spacing.12→padding`, `radius.md→radius`, `font:Noto Sans KR` |
| alert-list | `color.Mauve→background`, `spacing.12→padding`, `radius.md→radius`, `font:Noto Sans KR` |
| app-shell | `color.Periwinkle→surface`, `color.Peach Puff→emphasis`, `color.Mauve→background`, `spacing.12→padding`, `radius.md→radius`, `font:Noto Sans KR` |
| autocomplete | `color.Periwinkle→surface`, `color.Peach Puff→emphasis`, `color.Mauve→background`, `spacing.12→padding`, `radius.md→radius`, `font:Noto Sans KR` |
| avatar | `color.Mauve→background`, `spacing.12→padding`, `radius.md→radius`, `font:Noto Sans KR` |
| avatar-cluster | `color.Mauve→background`, `spacing.12→padding`, `radius.md→radius`, `font:Noto Sans KR` |
| back-button | `color.Periwinkle→surface`, `color.Peach Puff→emphasis`, `color.Mauve→background`, `spacing.12→padding`, `radius.md→radius`, `font:Noto Sans KR` |
| banner | `color.Mauve→background`, `spacing.12→padding`, `radius.md→radius`, `font:Noto Sans KR` |
| block-controls | `color.Mauve→background`, `spacing.12→padding`, `radius.md→radius`, `font:Noto Sans KR` |
| bottom-sheet | `color.Periwinkle→surface`, `color.Peach Puff→emphasis`, `color.Mauve→background`, `spacing.12→padding`, `radius.md→radius`, `font:Noto Sans KR` |
| breadcrumb | `color.Periwinkle→surface`, `color.Peach Puff→emphasis`, `color.Mauve→background`, `spacing.12→padding`, `radius.md→radius`, `font:Noto Sans KR` |
| byline-row | `color.Mauve→background`, `spacing.12→padding`, `radius.md→radius`, `font:Noto Sans KR` |
| calendar-grid | `color.Mauve→background`, `spacing.12→padding`, `radius.md→radius`, `font:Noto Sans KR` |
| chart-container | `color.Mauve→background`, `spacing.12→padding`, `radius.md→radius`, `font:Noto Sans KR` |
| chart-legend | `color.Mauve→background`, `spacing.12→padding`, `radius.md→radius`, `font:Noto Sans KR` |
| chart-panel | `color.Mauve→background`, `spacing.12→padding`, `radius.md→radius`, `font:Noto Sans KR` |
| chart-tooltip | `color.Periwinkle→surface`, `color.Peach Puff→emphasis`, `color.Mauve→background`, `spacing.12→padding`, `radius.md→radius`, `font:Noto Sans KR` |
| chat-input | `color.Periwinkle→surface`, `color.Peach Puff→emphasis`, `color.Mauve→background`, `spacing.12→padding`, `radius.md→radius`, `font:Noto Sans KR` |
| chat-message | `color.Mauve→background`, `spacing.12→padding`, `radius.md→radius`, `font:Noto Sans KR` |
| chat-panel | `color.Periwinkle→surface`, `color.Peach Puff→emphasis`, `color.Mauve→background`, `spacing.12→padding`, `radius.md→radius`, `font:Noto Sans KR` |
| chat-thread | `color.Mauve→background`, `spacing.12→padding`, `radius.md→radius`, `font:Noto Sans KR` |
| checkbox | `color.Periwinkle→surface`, `color.Peach Puff→emphasis`, `color.Mauve→background`, `spacing.12→padding`, `radius.md→radius`, `font:Noto Sans KR` |
| chip | `color.Periwinkle→surface`, `color.Peach Puff→emphasis`, `color.Mauve→background`, `spacing.12→padding`, `radius.md→radius`, `font:Noto Sans KR` |
| cohort-matrix | `color.Mauve→background`, `spacing.12→padding`, `radius.md→radius`, `font:Noto Sans KR` |
| column-header | `color.Mauve→background`, `spacing.12→padding`, `radius.md→radius`, `font:Noto Sans KR` |
| command-palette | `color.Periwinkle→surface`, `color.Peach Puff→emphasis`, `color.Mauve→background`, `spacing.12→padding`, `radius.md→radius`, `font:Noto Sans KR` |
| command-result-item | `color.Periwinkle→surface`, `color.Peach Puff→emphasis`, `color.Mauve→background`, `spacing.12→padding`, `radius.md→radius`, `font:Noto Sans KR` |
| comment-input | `color.Periwinkle→surface`, `color.Peach Puff→emphasis`, `color.Mauve→background`, `spacing.12→padding`, `radius.md→radius`, `font:Noto Sans KR` |
| comment-thread | `color.Mauve→background`, `spacing.12→padding`, `radius.md→radius`, `font:Noto Sans KR` |
| confirm-dialog | `color.Periwinkle→surface`, `color.Peach Puff→emphasis`, `color.Mauve→background`, `spacing.12→padding`, `radius.md→radius`, `font:Noto Sans KR` |
| content-card | `color.Mauve→background`, `spacing.12→padding`, `radius.md→radius`, `font:Noto Sans KR` |
| content-meta | `color.Mauve→background`, `spacing.12→padding`, `radius.md→radius`, `font:Noto Sans KR` |
| context-drawer | `color.Periwinkle→surface`, `color.Peach Puff→emphasis`, `color.Mauve→background`, `spacing.12→padding`, `radius.md→radius`, `font:Noto Sans KR` |
| context-panel | `color.Periwinkle→surface`, `color.Peach Puff→emphasis`, `color.Mauve→background`, `spacing.12→padding`, `radius.md→radius`, `font:Noto Sans KR` |
| conversion-funnel | `color.Mauve→background`, `spacing.12→padding`, `radius.md→radius`, `font:Noto Sans KR` |
| cta-button | `color.Periwinkle→surface`, `color.Peach Puff→emphasis`, `color.Mauve→background`, `spacing.12→padding`, `radius.md→radius`, `font:Noto Sans KR` |
| customer-logo | `color.Mauve→background`, `spacing.12→padding`, `radius.md→radius`, `font:Noto Sans KR` |
| dashboard-card | `color.Mauve→background`, `spacing.12→padding`, `radius.md→radius`, `font:Noto Sans KR` |
| data-table | `color.Mauve→background`, `spacing.12→padding`, `radius.md→radius`, `font:Noto Sans KR` |
| date-picker | `color.Periwinkle→surface`, `color.Peach Puff→emphasis`, `color.Mauve→background`, `spacing.12→padding`, `radius.md→radius`, `font:Noto Sans KR` |
| date-range-picker | `color.Periwinkle→surface`, `color.Peach Puff→emphasis`, `color.Mauve→background`, `spacing.12→padding`, `radius.md→radius`, `font:Noto Sans KR` |
| editor-canvas | `color.Mauve→background`, `spacing.12→padding`, `radius.md→radius`, `font:Noto Sans KR` |
| editor-toolbar | `color.Mauve→background`, `spacing.12→padding`, `radius.md→radius`, `font:Noto Sans KR` |
| empty-feed-illustration | `color.Mauve→background`, `spacing.12→padding`, `radius.md→radius`, `font:Noto Sans KR` |
| empty-state | `color.Mauve→background`, `spacing.12→padding`, `radius.md→radius`, `font:Noto Sans KR` |
| experiment-panel | `color.Mauve→background`, `spacing.12→padding`, `radius.md→radius`, `font:Noto Sans KR` |
| featured-story-card | `color.Mauve→background`, `spacing.12→padding`, `radius.md→radius`, `font:Noto Sans KR` |
| feed-item | `color.Mauve→background`, `spacing.12→padding`, `radius.md→radius`, `font:Noto Sans KR` |
| filter-bar | `color.Periwinkle→surface`, `color.Peach Puff→emphasis`, `color.Mauve→background`, `spacing.12→padding`, `radius.md→radius`, `font:Noto Sans KR` |
| filter-chip | `color.Periwinkle→surface`, `color.Peach Puff→emphasis`, `color.Mauve→background`, `spacing.12→padding`, `radius.md→radius`, `font:Noto Sans KR` |
| filter-panel | `color.Periwinkle→surface`, `color.Peach Puff→emphasis`, `color.Mauve→background`, `spacing.12→padding`, `radius.md→radius`, `font:Noto Sans KR` |
| filter-toolbar | `color.Mauve→background`, `spacing.12→padding`, `radius.md→radius`, `font:Noto Sans KR` |
| follow-button | `color.Periwinkle→surface`, `color.Peach Puff→emphasis`, `color.Mauve→background`, `spacing.12→padding`, `radius.md→radius`, `font:Noto Sans KR` |
| form-actions | `color.Periwinkle→surface`, `color.Peach Puff→emphasis`, `color.Mauve→background`, `spacing.12→padding`, `radius.md→radius`, `font:Noto Sans KR` |
| form-section | `color.Periwinkle→surface`, `color.Peach Puff→emphasis`, `color.Mauve→background`, `spacing.12→padding`, `radius.md→radius`, `font:Noto Sans KR` |
| gentle-toast | `color.Mauve→background`, `spacing.12→padding`, `radius.md→radius`, `font:Noto Sans KR` |
| ghost-button | `color.Periwinkle→surface`, `color.Peach Puff→emphasis`, `color.Mauve→background`, `spacing.12→padding`, `radius.md→radius`, `font:Noto Sans KR` |
| goal-grid | `color.Mauve→background`, `spacing.12→padding`, `radius.md→radius`, `font:Noto Sans KR` |
| goal-tracker | `color.Mauve→background`, `spacing.12→padding`, `radius.md→radius`, `font:Noto Sans KR` |
| habit-calendar | `color.Mauve→background`, `spacing.12→padding`, `radius.md→radius`, `font:Noto Sans KR` |
| hero-container | `color.Mauve→background`, `spacing.12→padding`, `radius.md→radius`, `font:Noto Sans KR` |
| hero-cta-group | `color.Periwinkle→surface`, `color.Peach Puff→emphasis`, `color.Mauve→background`, `spacing.12→padding`, `radius.md→radius`, `font:Noto Sans KR` |
| hero-eyebrow | `color.Mauve→background`, `spacing.12→padding`, `radius.md→radius`, `font:Noto Sans KR` |
| hero-headline | `color.Mauve→background`, `spacing.12→padding`, `radius.md→radius`, `font:Noto Sans KR` |
| hero-subheadline | `color.Mauve→background`, `spacing.12→padding`, `radius.md→radius`, `font:Noto Sans KR` |
| hero-trust-strip | `color.Mauve→background`, `spacing.12→padding`, `radius.md→radius`, `font:Noto Sans KR` |
| hero-visual | `color.Mauve→background`, `spacing.12→padding`, `radius.md→radius`, `font:Noto Sans KR` |
| icon-button | `color.Periwinkle→surface`, `color.Peach Puff→emphasis`, `color.Mauve→background`, `spacing.12→padding`, `radius.md→radius`, `font:Noto Sans KR` |
| inline-alert | `color.Mauve→background`, `spacing.12→padding`, `radius.md→radius`, `font:Noto Sans KR` |
| inline-format-menu | `color.Mauve→background`, `spacing.12→padding`, `radius.md→radius`, `font:Noto Sans KR` |
| insight-card | `color.Mauve→background`, `spacing.12→padding`, `radius.md→radius`, `font:Noto Sans KR` |
| kanban-board | `color.Mauve→background`, `spacing.12→padding`, `radius.md→radius`, `font:Noto Sans KR` |
| kanban-card | `color.Mauve→background`, `spacing.12→padding`, `radius.md→radius`, `font:Noto Sans KR` |
| kanban-column | `color.Mauve→background`, `spacing.12→padding`, `radius.md→radius`, `font:Noto Sans KR` |
| link-button | `color.Periwinkle→surface`, `color.Peach Puff→emphasis`, `color.Mauve→background`, `spacing.12→padding`, `radius.md→radius`, `font:Noto Sans KR` |
| logo-cloud | `color.Mauve→background`, `spacing.12→padding`, `radius.md→radius`, `font:Noto Sans KR` |
| mention-popup | `color.Periwinkle→surface`, `color.Peach Puff→emphasis`, `color.Mauve→background`, `spacing.12→padding`, `radius.md→radius`, `font:Noto Sans KR` |
| message-composer | `color.Periwinkle→surface`, `color.Peach Puff→emphasis`, `color.Mauve→background`, `spacing.12→padding`, `radius.md→radius`, `font:Noto Sans KR` |
| message-thread | `color.Periwinkle→surface`, `color.Peach Puff→emphasis`, `color.Mauve→background`, `spacing.12→padding`, `radius.md→radius`, `font:Noto Sans KR` |
| metric-highlight | `color.Mauve→background`, `spacing.12→padding`, `radius.md→radius`, `font:Noto Sans KR` |
| mobile-tab-bar | `color.Periwinkle→surface`, `color.Peach Puff→emphasis`, `color.Mauve→background`, `spacing.12→padding`, `radius.md→radius`, `font:Noto Sans KR` |
| mobile-topbar | `color.Periwinkle→surface`, `color.Peach Puff→emphasis`, `color.Mauve→background`, `spacing.12→padding`, `radius.md→radius`, `font:Noto Sans KR` |
| modal-dialog | `color.Periwinkle→surface`, `color.Peach Puff→emphasis`, `color.Mauve→background`, `spacing.12→padding`, `radius.md→radius`, `font:Noto Sans KR` |
| mood-chart | `color.Mauve→background`, `spacing.12→padding`, `radius.md→radius`, `font:Noto Sans KR` |
| mood-check | `color.Mauve→background`, `spacing.12→padding`, `radius.md→radius`, `font:Noto Sans KR` |
| pagination | `color.Periwinkle→surface`, `color.Peach Puff→emphasis`, `color.Mauve→background`, `spacing.12→padding`, `radius.md→radius`, `font:Noto Sans KR` |
| post-card | `color.Mauve→background`, `spacing.12→padding`, `radius.md→radius`, `font:Noto Sans KR` |
| press-quote | `color.Mauve→background`, `spacing.12→padding`, `radius.md→radius`, `font:Noto Sans KR` |
| primary-button | `color.Periwinkle→surface`, `color.Peach Puff→emphasis`, `color.Mauve→background`, `spacing.12→padding`, `radius.md→radius`, `font:Noto Sans KR` |
| profile-card | `color.Mauve→background`, `spacing.12→padding`, `radius.md→radius`, `font:Noto Sans KR` |
| radio-group | `color.Periwinkle→surface`, `color.Peach Puff→emphasis`, `color.Mauve→background`, `spacing.12→padding`, `radius.md→radius`, `font:Noto Sans KR` |
| reaction-bar | `color.Mauve→background`, `spacing.12→padding`, `radius.md→radius`, `font:Noto Sans KR` |
| referral-widget | `color.Mauve→background`, `spacing.12→padding`, `radius.md→radius`, `font:Noto Sans KR` |
| reply-composer | `color.Periwinkle→surface`, `color.Peach Puff→emphasis`, `color.Mauve→background`, `spacing.12→padding`, `radius.md→radius`, `font:Noto Sans KR` |
| retention-chart | `color.Mauve→background`, `spacing.12→padding`, `radius.md→radius`, `font:Noto Sans KR` |
| row-actions | `color.Mauve→background`, `spacing.12→padding`, `radius.md→radius`, `font:Noto Sans KR` |
| search-field | `color.Periwinkle→surface`, `color.Peach Puff→emphasis`, `color.Mauve→background`, `spacing.12→padding`, `radius.md→radius`, `font:Noto Sans KR` |
| search-results | `color.Mauve→background`, `spacing.12→padding`, `radius.md→radius`, `font:Noto Sans KR` |
| secondary-button | `color.Periwinkle→surface`, `color.Peach Puff→emphasis`, `color.Mauve→background`, `spacing.12→padding`, `radius.md→radius`, `font:Noto Sans KR` |
| section-header | `color.Mauve→background`, `spacing.12→padding`, `radius.md→radius`, `font:Noto Sans KR` |
| section-tabs | `color.Periwinkle→surface`, `color.Peach Puff→emphasis`, `color.Mauve→background`, `spacing.12→padding`, `radius.md→radius`, `font:Noto Sans KR` |
| segment-filter | `color.Periwinkle→surface`, `color.Peach Puff→emphasis`, `color.Mauve→background`, `spacing.12→padding`, `radius.md→radius`, `font:Noto Sans KR` |
| segmented-control | `color.Periwinkle→surface`, `color.Peach Puff→emphasis`, `color.Mauve→background`, `spacing.12→padding`, `radius.md→radius`, `font:Noto Sans KR` |
| select | `color.Periwinkle→surface`, `color.Peach Puff→emphasis`, `color.Mauve→background`, `spacing.12→padding`, `radius.md→radius`, `font:Noto Sans KR` |
| session-timeline | `color.Mauve→background`, `spacing.12→padding`, `radius.md→radius`, `font:Noto Sans KR` |
| session-tracker | `color.Mauve→background`, `spacing.12→padding`, `radius.md→radius`, `font:Noto Sans KR` |
| share-sheet | `color.Periwinkle→surface`, `color.Peach Puff→emphasis`, `color.Mauve→background`, `spacing.12→padding`, `radius.md→radius`, `font:Noto Sans KR` |
| shortcut-hint | `color.Mauve→background`, `spacing.12→padding`, `radius.md→radius`, `font:Noto Sans KR` |
| sidebar-nav | `color.Periwinkle→surface`, `color.Peach Puff→emphasis`, `color.Mauve→background`, `spacing.12→padding`, `radius.md→radius`, `font:Noto Sans KR` |
| slash-command-menu | `color.Mauve→background`, `spacing.12→padding`, `radius.md→radius`, `font:Noto Sans KR` |
| soft-dialog | `color.Periwinkle→surface`, `color.Peach Puff→emphasis`, `color.Mauve→background`, `spacing.12→padding`, `radius.md→radius`, `font:Noto Sans KR` |
| stat-card | `color.Mauve→background`, `spacing.12→padding`, `radius.md→radius`, `font:Noto Sans KR` |
| status-badge | `color.Mauve→background`, `spacing.12→padding`, `radius.md→radius`, `font:Noto Sans KR` |
| step-progress | `color.Mauve→background`, `spacing.12→padding`, `radius.md→radius`, `font:Noto Sans KR` |
| streak-indicator | `color.Mauve→background`, `spacing.12→padding`, `radius.md→radius`, `font:Noto Sans KR` |
| tab-bar | `color.Periwinkle→surface`, `color.Peach Puff→emphasis`, `color.Mauve→background`, `spacing.12→padding`, `radius.md→radius`, `font:Noto Sans KR` |
| tag | `color.Mauve→background`, `spacing.12→padding`, `radius.md→radius`, `font:Noto Sans KR` |
| tag-pill | `color.Mauve→background`, `spacing.12→padding`, `radius.md→radius`, `font:Noto Sans KR` |
| text-field | `color.Periwinkle→surface`, `color.Peach Puff→emphasis`, `color.Mauve→background`, `spacing.12→padding`, `radius.md→radius`, `font:Noto Sans KR` |
| textarea | `color.Periwinkle→surface`, `color.Peach Puff→emphasis`, `color.Mauve→background`, `spacing.12→padding`, `radius.md→radius`, `font:Noto Sans KR` |
| thread-view | `color.Mauve→background`, `spacing.12→padding`, `radius.md→radius`, `font:Noto Sans KR` |
| ticket-queue | `color.Mauve→background`, `spacing.12→padding`, `radius.md→radius`, `font:Noto Sans KR` |
| time-picker | `color.Periwinkle→surface`, `color.Peach Puff→emphasis`, `color.Mauve→background`, `spacing.12→padding`, `radius.md→radius`, `font:Noto Sans KR` |
| timeline-stream | `color.Mauve→background`, `spacing.12→padding`, `radius.md→radius`, `font:Noto Sans KR` |
| toast | `color.Mauve→background`, `spacing.12→padding`, `radius.md→radius`, `font:Noto Sans KR` |
| tooltip-guide | `color.Periwinkle→surface`, `color.Peach Puff→emphasis`, `color.Mauve→background`, `spacing.12→padding`, `radius.md→radius`, `font:Noto Sans KR` |
| topbar | `color.Periwinkle→surface`, `color.Peach Puff→emphasis`, `color.Mauve→background`, `spacing.12→padding`, `radius.md→radius`, `font:Noto Sans KR` |
| user-list | `color.Mauve→background`, `spacing.12→padding`, `radius.md→radius`, `font:Noto Sans KR` |
| user-menu | `color.Periwinkle→surface`, `color.Peach Puff→emphasis`, `color.Mauve→background`, `spacing.12→padding`, `radius.md→radius`, `font:Noto Sans KR` |
| wellness-score | `color.Mauve→background`, `spacing.12→padding`, `radius.md→radius`, `font:Noto Sans KR` |
| wizard-layout | `color.Periwinkle→surface`, `color.Peach Puff→emphasis`, `color.Mauve→background`, `spacing.12→padding`, `radius.md→radius`, `font:Noto Sans KR` |
| workspace-switcher | `color.Periwinkle→surface`, `color.Peach Puff→emphasis`, `color.Mauve→background`, `spacing.12→padding`, `radius.md→radius`, `font:Noto Sans KR` |

## 19. Contrast Audit

| Background | Foreground | Ratio | Level |
|------------|------------|-------|-------|
| Peach Puff | Ink | 14.37:1 | AAA (pass) |
| Mauve | Ink | 10.63:1 | AAA (pass) |
| Periwinkle | Ink | 7.23:1 | AAA (pass) |
| Periwinkle | Paper | 2.61:1 | fail (FAIL) |
| Periwinkle | Peach Puff | 1.99:1 | fail (FAIL) |
| Mauve | Paper | 1.78:1 | fail (FAIL) |
| Periwinkle | Mauve | 1.47:1 | fail (FAIL) |
| Peach Puff | Mauve | 1.35:1 | fail (FAIL) |
| Peach Puff | Paper | 1.31:1 | fail (FAIL) |

## 20. Pattern Catalog

### Layout Patterns

- **sidebar navigation**: —
- **workspace switcher**: —
- **dashboard card**: —
- **kpi card**: —
- **data table**: —
- **streak indicator**: —
- **habit calendar**: —
- **wellness score**: —
- **mood check**: —
- **session tracker**: —
- **insight card**: —
- **goal tracker**: —
- **gentle toast**: —
- **soft dialog**: —
- **user list**: —
- **cohort matrix**: —
- **retention chart**: —
- **activity feed**: —
- **settings panel**: —
- **workspace navigation**: app-shell, sidebar-nav, topbar, breadcrumb, workspace-switcher, tab-bar, context-panel
- **dashboard cards**: stat-card, insight-card, activity-card, section-header, chart-panel
- **data tables**: data-table, column-header, filter-chip, row-actions, pagination, filter-toolbar

### Interaction Patterns

- **filter chip**: —
- **command palette**: command-palette, command-result-item, shortcut-hint
- **forms**: text-field, select, checkbox, textarea, form-section, radio-group, form-actions
- **notifications**: toast, inline-alert, empty-state, banner
