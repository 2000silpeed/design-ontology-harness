# Pulse System Spec

## 1. Positioning

- **Brand**: Pulse
- **Product**: 실시간 observability 콘솔 — metric/log/trace/alert 를 한 화면에서 운영하는 SRE/DevOps 운영 도구
- **Audience**: SRE / 인프라 엔지니어, DevOps / 플랫폼 엔지니어, 온콜 엔지니어 / 인시던트 커맨더
- **Platforms**: web, desktop
- **Accessibility floor**: WCAG 2.2 AA

## 2. Identity Guardrails

- **Brand keywords**: sre, devops, observability, monitoring, realtime, operations, alerting, metric, incident
- **Anti-keywords**: playful, decorative, marketing-heavy, skeuomorphic, ornamental
- **Tone of voice**: precise, operational, matter-of-fact, calm-under-pressure
- **Visual direction**: dense chart grid, status board, high-density table, alert-first hierarchy, cool neutral surfaces, hairline borders, monochrome + single accent, numeric emphasis
- **Interaction direction**: keyboard-first, live-update, drilldown, zoom/pan time range, saved views, quick mute/ack, severity-routed focus

## 3. Design Principles

- **Sre**: `sre`를 시각적 선택과 인터랙션 선택의 기본 기준으로 삼습니다.
- **Devops**: `devops`를 시각적 선택과 인터랙션 선택의 기본 기준으로 삼습니다.
- **Observability**: `observability`를 시각적 선택과 인터랙션 선택의 기본 기준으로 삼습니다.
- **Monitoring**: `monitoring`를 시각적 선택과 인터랙션 선택의 기본 기준으로 삼습니다.

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
- **Product type detected**: dashboard
- **Pairing source**: auto-scored
- **Line height**: normal
- **Type scale**: base 14px, ratio 1.2 (xs=11px, sm=12px, md=14px, lg=17px, xl=20px, 2xl=24px, 3xl=29px)
- **Strategy**:
  - 단일 서체(Spoqa Han Sans Neo)로 weight 대비 위계 — 일관성 우선
  - 한글 서체: Spoqa Han Sans Neo — 라틴과 x-height/weight 조화
  - 모노스페이스: JetBrains Mono — 코드/데이터 영역 전용
- **Heading note**: 스포카에서 만든 한글 산세리프. Source Sans Pro 기반. 깔끔한 데이터 UI에 적합.
- **Body note**: 스포카에서 만든 한글 산세리프. Source Sans Pro 기반. 깔끔한 데이터 UI에 적합.
- **Korean rationale**: Spoqa Han Sans Neo — Pretendard 이전 시대의 한글 UI 표준. 요기요, 여기어때 등에서 사용. 깔끔하지만 weight 범위와 Variable 미지원이 아쉬움. 신규 프로젝트에서는 Pretendard 추천.
- **Heading tracking**: xl=-0.01em, 2xl=-0.01em, 3xl=-0.01em
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
- **Preferred families**: Deep Blues, Standard Blues, Natural Blues, Pastel Blues
- **Palette strategy**: temperature=mixed, contrast=balanced, diversity=balanced, surface_style=tinted
- **Palette expansion**: supporting_color_count=10, combination_count=3, prefer_pairings=True
- **Palette roles**:
  - `primary` -> Azure Blue #007FFF / Standard Blues
  - `accent` -> Emerald Green #50C878 / Standard Greens
  - `surface_tint` -> Ice Blue #D6EAF8 / Pastel Blues
- **Selected colors**:
  - Kelly Green #4CBB17 / Standard Greens / 고명도, 고채도, 전통적인 순녹색 계열 / 활력, 생동감, 긍정성, 에너지, 명료함
  - Cerulean #2A52BE / Standard Blues / 중명도, 중채도, 스탠다드한 청색 계열 / 안정감, 명료함, 신뢰, 여유, 시각적 청량감
  - Sky Blue #87CEEB / Natural Blues / 고명도, 중채도의 밝은 쿨톤 / 청량함, 평화, 유연함, 긍정, 맑음
- **Palette candidates**:
  - signature-1 (Signature): primary=Kelly Green, accent=Cerulean, surface_tint=Sky Blue / Kelly Green matches preferred mood '명료함'.; Cerulean is inside preferred families.
  - soft-spread-2 (Soft Spread): primary=Cerulean, accent=Sky Blue, surface_tint=Ice Blue / Cerulean is inside preferred families.; Sky Blue is inside preferred families.
- **Expanded supporting colors**:
  - Pairing #FFFFFF #FFFFFF / Derived Pairing / pairing-swatch / Pairing #FFFFFF comes from the seed pairing references.; Pairing #FFFFFF is explicitly paired with Azure Blue, Ice Blue.
  - Pairing #444C57 #444C57 / Derived Pairing / pairing-swatch / Pairing #444C57 comes from the seed pairing references.; Pairing #444C57 is explicitly paired with Azure Blue.
  - Pairing #BCE0EE #BCE0EE / Derived Pairing / pairing-swatch / Pairing #BCE0EE comes from the seed pairing references.; Pairing #BCE0EE is explicitly paired with Azure Blue.
  - Pairing #C0C0C0 #C0C0C0 / Derived Pairing / pairing-swatch / Pairing #C0C0C0 comes from the seed pairing references.; Pairing #C0C0C0 is explicitly paired with Ice Blue.
  - Pairing #1A2E45 #1A2E45 / Derived Pairing / pairing-swatch / Pairing #1A2E45 comes from the seed pairing references.; Pairing #1A2E45 is explicitly paired with Emerald Green.
  - Pairing #2E4E68 #2E4E68 / Derived Pairing / pairing-swatch / Pairing #2E4E68 comes from the seed pairing references.; Pairing #2E4E68 is explicitly paired with Ice Blue.
  - Pairing #3C3C3C #3C3C3C / Derived Pairing / pairing-swatch / Pairing #3C3C3C comes from the seed pairing references.; Pairing #3C3C3C is explicitly paired with Emerald Green.
  - Pairing #3E3E3E #3E3E3E / Derived Pairing / pairing-swatch / Pairing #3E3E3E comes from the seed pairing references.; Pairing #3E3E3E is explicitly paired with Ice Blue.
- **Expanded semantic roles**:
  - `brand_primary` -> Azure Blue #007FFF / Standard Blues
  - `brand_accent` -> Emerald Green #50C878 / Standard Greens
  - `surface_tint` -> Ice Blue #D6EAF8 / Pastel Blues
  - `canvas` -> Pairing #FFFFFF #FFFFFF / Derived Pairing
  - `surface` -> Pairing #FFFFFF #FFFFFF / Derived Pairing
  - `surface_muted` -> Surface Muted #EEF1F6 / Generated Fallback
  - `surface_elevated` -> Pairing #FFFFFF #FFFFFF / Derived Pairing
  - `border` -> Border Neutral #D6DDE6 / Generated Fallback
  - `border_strong` -> Pairing #C0C0C0 #C0C0C0 / Derived Pairing
  - `ink` -> Pairing #1A2E45 #1A2E45 / Derived Pairing
- **Combination lists**:
  - Seed Core: primary=Azure Blue, accent=Emerald Green, surface_tint=Ice Blue
  - Surface System: canvas=Pairing #FFFFFF, surface=Pairing #FFFFFF, surface_tint=Ice Blue, border=Border Neutral, ink=Pairing #1A2E45, ink_muted=Pairing #444C57
  - Support Spectrum: support=Pairing #FFFFFF, support=Pairing #444C57, support=Pairing #BCE0EE, support=Pairing #C0C0C0, support=Pairing #1A2E45, support=Pairing #2E4E68
- **Notes**: Azure Blue 를 primary 로 — 실시간 강조/라이브 상태 신호, Emerald Green 액센트로 성공/healthy 상태 긍정 시그널, Ice Blue 는 surface_tint — 장시간 관찰하는 데이터 캔버스 피로감 최소화, dark mode 가 기본 — 온콜/야간 운영 환경, Grafana/Datadog 관례, semantic(success/warning/danger/info) 별도 role — severity 는 색 + 라벨 이중
- **Application rule**: 레퍼런스 컬러는 semantic token으로 번역해서 사용하고, 접근성과 theme 호환성을 우선합니다.

## 7. Visual Reference Signals

- **Mode**: local-images
- **Coverage**: source 0 / image 0 / selected 0
- **Rule**: visual references are advisory signals for motif and layout direction; official KB/spec remain the structural source of truth.
- **Provenance**: `observed` = directly measured from local pixels, `inferred` = synthesized from image/query/brand signals, `unverified` = reliable visual evidence not yet available.
- **Query seeds**: grafana dashboard dark, datadog monitoring console, honeycomb observability traces, prometheus alert list
### Visual Direction

- **Density**: dense (confidence 0.94, provenance inferred) / dashboard x1, table x3, monitoring x2
- **Surface Style**: flat (confidence 0.24, provenance inferred) / fallback=flat
- **Corner Style**: medium (confidence 0.29, provenance inferred) / card x1
- **Typography Mood**: playful (confidence 0.49, provenance inferred) / playful x2
- **Color balance**: temperature=unknown, contrast=unknown, neutral_bias=unknown, provenance=unverified

### Layout Rhythm

- **Dashboard grid**: confidence 0.94 / provenance inferred / dashboard x1, metric x3, kpi x1, chart x3
- **Data review surface**: confidence 0.94 / provenance inferred / table x3, grid x3, log x1, filter x1
- **Split-pane workspace**: confidence 0.7 / provenance inferred / sidebar x1, editor x1, navigation x1, dashboard x1
- **Narrative landing flow**: confidence 0.35 / provenance inferred / marketing x1

### Image-derived Component Hints

- **Cards**: flat card planes를 기본으로 하고, 압축된 spacing과 얇은 divider 중심의 hierarchy. 중간 반경으로 제품 UI 절제 유지. / provenance inferred / surface=flat, density=dense, corner=medium
- **Navigation**: 고정 sidebar 또는 split-pane navigation을 우선하고, 현재 위치와 scope를 항상 명시한다. / provenance inferred / Split-pane workspace
- **Typography**: 표현력은 허용하되 제품 UI에서는 heading 수와 accent를 엄격히 제한한다. / provenance inferred / typography_mood=playful
- **Data Display**: 정보 밀도를 유지하되 thin dividers와 restrained accent로 hierarchy를 만든다. / provenance inferred / layout=dashboard-grid, density=dense

### Synthesis Notes

- layout는 Dashboard grid 기준으로 정리
- surface language는 flat 성향 우선
- typography mood는 playful 축 유지
- density는 dense 기준으로 primitive spacing 조정
- palette temperature는 unknown 쪽을 우선
- Avoid: glassmorphism
- Avoid: gradient-heavy surfaces
- Avoid: playful illustrations

## 8. Component Strategy

- **Product primitives**: chart grid, sparkline, kpi card, alert list, severity badge, metric table, time range picker, status board, incident timeline, sidebar navigation, search filter chrome, log viewer, trace flamegraph, threshold editor
- **Required families**: button, data-display, editorial, feedback, input, navigation, overlay
- **Visual-reference archetypes**:

- **Dashboard insight module** (data-display / 0.94): stat-card, insight-card, chart-panel, section-header, filter-chip
- **Data review table** (data-display / 0.94): data-table, column-header, row-actions, filter-toolbar, pagination
- **Workspace shell** (navigation / 0.75): app-shell, sidebar-nav, workspace-switcher, breadcrumb, context-panel

- **button**: primary-button, secondary-button, ghost-button, icon-button, cta-button, link-button, form-actions
- **data-display**: stat-card, insight-card, activity-card, section-header, chart-container, chart-legend, data-table, column-header / visual signals: Dashboard insight module (0.94), Data review table (0.94)
- **editorial**: editor-canvas, editor-toolbar, inline-format-menu, slash-command-menu, block-controls
- **feedback**: inline-alert, empty-state, toast, banner, status-badge, step-progress
- **input**: text-field, search-field, segmented-control, filter-chip, chip, textarea, select, checkbox
- **navigation**: mobile-topbar, mobile-tab-bar, back-button, section-tabs, pagination, app-shell, sidebar-nav, topbar / visual signals: Workspace shell (0.75)
- **overlay**: bottom-sheet, modal-dialog, chart-tooltip, autocomplete, mention-popup, confirm-dialog, tooltip-guide

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

이 문서는 **Pulse System**의 디자인 시스템 사양입니다.

### 시작하기

1. **토큰 적용**: Drop-in CSS(아래 섹션 16)의 CSS 변수를 프로젝트에 복사합니다.
2. **컬러 세팅**: Color Reference(섹션 6)의 semantic role을 기준으로 surface/text/border를 잡습니다.
3. **타이포 세팅**: Token Strategy(섹션 5)의 font family와 type scale을 적용합니다.
4. **시각 방향 확인**: Visual Reference Signals(섹션 7)에서 density/surface/layout cue를 먼저 확인합니다.
5. **컴포넌트 구현**: Component Strategy(섹션 8)의 family 순서대로 하나씩 빌드합니다.

### 우선순위

핵심 primitive: **chart grid, sparkline, kpi card, alert list, severity badge**

이 primitive를 지원하는 컴포넌트부터 구현하고, 나머지는 필요에 따라 확장합니다.

## 15. DO / DON'T

### DO

- **Sre**: sre와 충돌하는 컴포넌트 변형은 만들지 않기
- **Devops**: devops와 충돌하는 컴포넌트 변형은 만들지 않기
- **Observability**: observability와 충돌하는 컴포넌트 변형은 만들지 않기
- **Monitoring**: monitoring와 충돌하는 컴포넌트 변형은 만들지 않기
- 모든 시각적 선택에서 **sre, devops, observability** 기준을 적용
- semantic token을 통해 컬러를 적용 (하드코딩 금지)
- 접근성 기준을 모든 text/surface 조합에서 먼저 검증
- 컴포넌트 변형 추가 전 기존 variant로 해결 가능한지 먼저 확인
- 아이콘은 SVG 컴포넌트 또는 Lucide/Heroicons/Phosphor/Tabler 등 라이브러리로 구현
- component_specs.md의 anatomy/states/token binding을 그대로 따라 완전히 구현

### DON'T

- **playful** 방향의 디자인 결정을 하지 않음
- **decorative** 방향의 디자인 결정을 하지 않음
- **marketing-heavy** 방향의 디자인 결정을 하지 않음
- **skeuomorphic** 방향의 디자인 결정을 하지 않음
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
  --color-primary: #007FFF;
  --color-accent: #50C878;
  --color-surface-tint: #D6EAF8;

  /* --- Semantic roles (expanded) --- */
  --color-brand-primary: #007FFF;
  --color-brand-accent: #50C878;
  --color-surface-tint: #D6EAF8;
  --color-canvas: #FFFFFF;
  --color-surface: #FFFFFF;
  --color-surface-muted: #EEF1F6;
  --color-surface-elevated: #FFFFFF;
  --color-border: #D6DDE6;
  --color-border-strong: #C0C0C0;
  --color-ink: #1A2E45;
  --color-ink-muted: #444C57;
  --color-ink-subtle: #6B7280;
  --color-ink-inverse: #FFFFFF;
  --color-primary-support: #444C57;
  --color-accent-support: #50C878;
  --color-info: #444C57;
  --color-success: #50C878;
  --color-warning: #F8F8F4;
  --color-danger: #8B2252;
  --color-link: #007FFF;
  --color-link-hover: #006BD6;

  /* --- Button — primary --- */
  --color-button-primary-surface-default: #007FFF;
  --color-button-primary-surface-hover: #0070E0;
  --color-button-primary-surface-active: #0066CC;
  --color-button-primary-surface-disabled: #99CCFF;
  --color-button-primary-text-default: #FFFFFF;
  --color-button-primary-text-disabled: #FFFFFF;
  --color-button-primary-border-default: #007FFF;
  --color-button-primary-focus-ring: #007FFF;

  /* --- Button — secondary --- */
  --color-button-secondary-surface-default: #FFFFFF;
  --color-button-secondary-surface-hover: #F1F2F4;
  --color-button-secondary-surface-active: #E8EAEC;
  --color-button-secondary-surface-disabled: #FFFFFF;
  --color-button-secondary-text-default: #1A2E45;
  --color-button-secondary-text-disabled: #98A1AB;
  --color-button-secondary-border-default: #BDC8D7;
  --color-button-secondary-border-hover: #A3B3C7;
  --color-button-secondary-focus-ring: #007FFF;

  /* --- Button — ghost --- */
  --color-button-ghost-surface-default: transparent;
  --color-button-ghost-surface-hover: #F4F5F6;
  --color-button-ghost-surface-active: #EAECEE;
  --color-button-ghost-surface-disabled: transparent;
  --color-button-ghost-text-default: #444C57;
  --color-button-ghost-text-hover: #1A2E45;
  --color-button-ghost-text-disabled: #ABAEB3;
  --color-button-ghost-border-default: transparent;
  --color-button-ghost-focus-ring: #007FFF;

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
  --color-input-surface-disabled: #FFFFFF;
  --color-input-text-default: #1A2E45;
  --color-input-text-placeholder: #8F949A;
  --color-input-text-disabled: #ABAEB3;
  --color-input-border-default: #D6DDE6;
  --color-input-border-hover: #B6C3D3;
  --color-input-border-focus: #007FFF;
  --color-input-border-error: #8B2252;
  --color-input-border-disabled: #E6EAF0;

  /* --- Card --- */
  --color-card-surface-default: #FFFFFF;
  --color-card-surface-hover: #FAFBFB;
  --color-card-surface-muted: #FFFFFF;
  --color-card-border-default: #D6DDE6;
  --color-card-border-hover: #B6C3D3;
  --color-card-border-focus: #007FFF;

  /* --- Nav link --- */
  --color-nav-link-text-default: #444C57;
  --color-nav-link-text-hover: #1A2E45;
  --color-nav-link-text-active: #007FFF;
  --color-nav-link-surface-hover: #F6F7F8;
  --color-nav-link-indicator: #50C878;

  /* --- Link --- */
  --color-link-text-default: #007FFF;
  --color-link-text-hover: #0066CC;
  --color-link-text-visited: #1772CF;

  /* --- Feedback — info --- */
  --color-feedback-info-surface: #E9EAEB;
  --color-feedback-info-text: #444C57;
  --color-feedback-info-border: #7C8289;
  --color-feedback-info-icon: #444C57;

  /* --- Feedback — success --- */
  --color-feedback-success-surface: #EAF8EF;
  --color-feedback-success-text: #50C878;
  --color-feedback-success-border: #84D8A0;
  --color-feedback-success-icon: #50C878;

  /* --- Feedback — warning --- */
  --color-feedback-warning-surface: #FEFEFE;
  --color-feedback-warning-text: #F8F8F4;
  --color-feedback-warning-border: #FAFAF7;
  --color-feedback-warning-icon: #F8F8F4;

  /* --- Feedback — danger --- */
  --color-feedback-danger-surface: #F1E4EA;
  --color-feedback-danger-text: #8B2252;
  --color-feedback-danger-border: #AE6486;
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
| activity-card | `color.Ice Blue→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo` |
| app-shell | `color.Azure Blue→surface`, `color.Emerald Green→emphasis`, `color.Ice Blue→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo` |
| autocomplete | `color.Azure Blue→surface`, `color.Emerald Green→emphasis`, `color.Ice Blue→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo` |
| back-button | `color.Azure Blue→surface`, `color.Emerald Green→emphasis`, `color.Ice Blue→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo` |
| banner | `color.Ice Blue→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo` |
| block-controls | `color.Ice Blue→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo` |
| bottom-sheet | `color.Azure Blue→surface`, `color.Emerald Green→emphasis`, `color.Ice Blue→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo` |
| breadcrumb | `color.Azure Blue→surface`, `color.Emerald Green→emphasis`, `color.Ice Blue→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo` |
| calendar-grid | `color.Ice Blue→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo` |
| chart-container | `color.Ice Blue→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo` |
| chart-legend | `color.Ice Blue→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo` |
| chart-panel | `color.Ice Blue→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo` |
| chart-tooltip | `color.Azure Blue→surface`, `color.Emerald Green→emphasis`, `color.Ice Blue→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo` |
| checkbox | `color.Azure Blue→surface`, `color.Emerald Green→emphasis`, `color.Ice Blue→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo` |
| chip | `color.Azure Blue→surface`, `color.Emerald Green→emphasis`, `color.Ice Blue→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo` |
| column-header | `color.Ice Blue→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo` |
| comment-input | `color.Azure Blue→surface`, `color.Emerald Green→emphasis`, `color.Ice Blue→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo` |
| comment-thread | `color.Ice Blue→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo` |
| confirm-dialog | `color.Azure Blue→surface`, `color.Emerald Green→emphasis`, `color.Ice Blue→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo` |
| context-panel | `color.Azure Blue→surface`, `color.Emerald Green→emphasis`, `color.Ice Blue→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo` |
| cta-button | `color.Azure Blue→surface`, `color.Emerald Green→emphasis`, `color.Ice Blue→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo` |
| data-table | `color.Ice Blue→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo` |
| date-picker | `color.Azure Blue→surface`, `color.Emerald Green→emphasis`, `color.Ice Blue→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo` |
| date-range-picker | `color.Azure Blue→surface`, `color.Emerald Green→emphasis`, `color.Ice Blue→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo` |
| editor-canvas | `color.Ice Blue→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo` |
| editor-toolbar | `color.Ice Blue→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo` |
| empty-state | `color.Ice Blue→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo` |
| filter-chip | `color.Azure Blue→surface`, `color.Emerald Green→emphasis`, `color.Ice Blue→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo` |
| filter-panel | `color.Azure Blue→surface`, `color.Emerald Green→emphasis`, `color.Ice Blue→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo` |
| filter-toolbar | `color.Ice Blue→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo` |
| form-actions | `color.Azure Blue→surface`, `color.Emerald Green→emphasis`, `color.Ice Blue→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo` |
| form-section | `color.Azure Blue→surface`, `color.Emerald Green→emphasis`, `color.Ice Blue→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo` |
| ghost-button | `color.Azure Blue→surface`, `color.Emerald Green→emphasis`, `color.Ice Blue→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo` |
| icon-button | `color.Azure Blue→surface`, `color.Emerald Green→emphasis`, `color.Ice Blue→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo` |
| inline-alert | `color.Ice Blue→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo` |
| inline-format-menu | `color.Ice Blue→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo` |
| insight-card | `color.Ice Blue→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo` |
| kanban-board | `color.Ice Blue→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo` |
| kanban-card | `color.Ice Blue→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo` |
| kanban-column | `color.Ice Blue→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo` |
| link-button | `color.Azure Blue→surface`, `color.Emerald Green→emphasis`, `color.Ice Blue→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo` |
| mention-popup | `color.Azure Blue→surface`, `color.Emerald Green→emphasis`, `color.Ice Blue→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo` |
| mobile-tab-bar | `color.Azure Blue→surface`, `color.Emerald Green→emphasis`, `color.Ice Blue→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo` |
| mobile-topbar | `color.Azure Blue→surface`, `color.Emerald Green→emphasis`, `color.Ice Blue→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo` |
| modal-dialog | `color.Azure Blue→surface`, `color.Emerald Green→emphasis`, `color.Ice Blue→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo` |
| pagination | `color.Azure Blue→surface`, `color.Emerald Green→emphasis`, `color.Ice Blue→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo` |
| primary-button | `color.Azure Blue→surface`, `color.Emerald Green→emphasis`, `color.Ice Blue→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo` |
| radio-group | `color.Azure Blue→surface`, `color.Emerald Green→emphasis`, `color.Ice Blue→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo` |
| row-actions | `color.Ice Blue→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo` |
| search-field | `color.Azure Blue→surface`, `color.Emerald Green→emphasis`, `color.Ice Blue→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo` |
| search-results | `color.Ice Blue→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo` |
| secondary-button | `color.Azure Blue→surface`, `color.Emerald Green→emphasis`, `color.Ice Blue→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo` |
| section-header | `color.Ice Blue→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo` |
| section-tabs | `color.Azure Blue→surface`, `color.Emerald Green→emphasis`, `color.Ice Blue→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo` |
| segmented-control | `color.Azure Blue→surface`, `color.Emerald Green→emphasis`, `color.Ice Blue→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo` |
| select | `color.Azure Blue→surface`, `color.Emerald Green→emphasis`, `color.Ice Blue→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo` |
| sidebar-nav | `color.Azure Blue→surface`, `color.Emerald Green→emphasis`, `color.Ice Blue→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo` |
| slash-command-menu | `color.Ice Blue→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo` |
| stat-card | `color.Ice Blue→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo` |
| status-badge | `color.Ice Blue→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo` |
| step-progress | `color.Ice Blue→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo` |
| tab-bar | `color.Azure Blue→surface`, `color.Emerald Green→emphasis`, `color.Ice Blue→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo` |
| tag | `color.Ice Blue→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo` |
| text-field | `color.Azure Blue→surface`, `color.Emerald Green→emphasis`, `color.Ice Blue→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo` |
| textarea | `color.Azure Blue→surface`, `color.Emerald Green→emphasis`, `color.Ice Blue→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo` |
| time-picker | `color.Azure Blue→surface`, `color.Emerald Green→emphasis`, `color.Ice Blue→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo` |
| toast | `color.Ice Blue→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo` |
| tooltip-guide | `color.Azure Blue→surface`, `color.Emerald Green→emphasis`, `color.Ice Blue→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo` |
| topbar | `color.Azure Blue→surface`, `color.Emerald Green→emphasis`, `color.Ice Blue→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo` |
| wizard-layout | `color.Azure Blue→surface`, `color.Emerald Green→emphasis`, `color.Ice Blue→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo` |
| workspace-switcher | `color.Azure Blue→surface`, `color.Emerald Green→emphasis`, `color.Ice Blue→background`, `spacing.12→padding`, `radius.md→radius`, `font:Spoqa Han Sans Neo` |

## 19. Contrast Audit

| Background | Foreground | Ratio | Level |
|------------|------------|-------|-------|
| Ice Blue | Ink | 15.27:1 | AAA (pass) |
| Emerald Green | Ink | 8.88:1 | AAA (pass) |
| Azure Blue | Ink | 4.93:1 | AA (pass) |
| Azure Blue | Paper | 3.83:1 | AA-large (large-only) |
| Azure Blue | Ice Blue | 3.10:1 | AA-large (large-only) |
| Emerald Green | Paper | 2.13:1 | fail (FAIL) |
| Azure Blue | Emerald Green | 1.80:1 | fail (FAIL) |
| Emerald Green | Ice Blue | 1.72:1 | fail (FAIL) |
| Ice Blue | Paper | 1.24:1 | fail (FAIL) |

## 20. Pattern Catalog

### Layout Patterns

- **chart grid**: —
- **sparkline**: —
- **kpi card**: —
- **alert list**: —
- **severity badge**: —
- **metric table**: —
- **time range picker**: —
- **status board**: —
- **incident timeline**: —
- **sidebar navigation**: —
- **log viewer**: —
- **trace flamegraph**: —
- **workspace navigation**: app-shell, sidebar-nav, topbar, breadcrumb, workspace-switcher, tab-bar, context-panel
- **dashboard cards**: stat-card, insight-card, activity-card, section-header, chart-panel
- **data tables**: data-table, column-header, filter-chip, row-actions, pagination, filter-toolbar

### Interaction Patterns

- **search filter chrome**: —
- **threshold editor**: —
- **command palette**: —
- **forms**: text-field, select, checkbox, textarea, form-section, radio-group, form-actions
- **notifications**: toast, inline-alert, empty-state, banner
