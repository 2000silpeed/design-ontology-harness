# Lattice Component Specs

총 99개 컴포넌트 | 패밀리: button, copilot-artifact, data-display, document, editorial, feedback, input, marketing, navigation, overlay, workflow

## 구현 원칙 (Non-negotiable)

이 스펙의 모든 컴포넌트를 구현할 때 반드시 지킨다:

1. **이모지를 UI로 쓰지 않는다** — 🎨 ✅ 🔥 ⚡ 🚀 ❌ ⭐ 📊 등 이모지를 아이콘, 상태 표시, 버튼 장식, 네비게이션 지표 자리에 절대 넣지 않는다. 리팩토링 중 카드/버튼/배지/탭/상태 UI에서 이모지를 발견하면 SVG 파일, SVG 컴포넌트, 또는 Lucide/Heroicons/Phosphor/Tabler 같은 아이콘 라이브러리로 교체한다.
2. **컴포넌트를 직접 구현한다** — 아래 각 컴포넌트의 anatomy(구조), states(상태), 토큰 바인딩, 접근성 규칙을 그대로 따라 완전하게 구현한다. '임시', 'TODO', '플레이스홀더' 같은 반쪽 구현을 남기지 않는다.
3. **라이브러리 기본 스타일 금지** — 라이브러리 컴포넌트를 그대로 import해서 쓰지 않는다. 반드시 디자인 토큰(--color-*, --space-*, --radius-*, --font-*)으로 스타일을 명시적으로 바인딩한다.
4. **접근성은 옵션이 아니다** — 각 컴포넌트의 '접근성' 섹션에 정의된 role, aria-*, label, focus 관리 규칙을 전부 적용한다.
5. **hex 값 하드코딩 금지** — 색상은 반드시 semantic token을 경유한다 (예: `color: var(--color-ink)` not `color: #2C2C2C`).
6. **모바일 overflow 금지** — 버튼, CTA, 탭, 필터칩, 툴바 액션은 320px viewport에서 화면 밖으로 나가면 안 된다. fixed/min-width px 값으로 폭을 고정하지 말고 wrap/stack fallback을 제공한다.

## 브랜드 적용 규칙

- **hover**: 미세한 opacity 또는 underline만 + 정확한 border/outline 변화
- **motion**: 80-120ms, 거의 즉각적 + 120-180ms, 군더더기 없는 전환
- **color**: monochrome 기반, accent 최소화 + 정확한 semantic 분리, 모호한 중간 톤 지양
- **density**: compact 가능, 불필요한 여백 제거 + 엄격한 spacing scale 준수, 임의 값 금지
- **feedback**: 아이콘+텍스트 조합, 색상 배경 최소화 + 명확한 상태 구분, 진행률/결과를 수치로 표시

## Visual-reference 적용 원칙

- anatomy / states / accessibility는 설계서(spec)와 KB 근거를 유지하고, visual adaptation은 elevation / framing / prominence / density 같은 표현 계층에만 advisory signal로 적용한다.
- Active visual signals: surface_style=flat, density=dense, corner_style=medium, top_layout_cue=data-review-surface
- Connected component hints: cards, data_display, navigation, typography

## Typography Guardrails

- 한글 기반 제품은 line-break / scale / tracking을 영문 랜딩 기본값으로 처리하지 않고, 아래 가드레일을 구현 기본값으로 사용한다.
- Headline: Pretendard | line-height 1.25-1.35 | tracking 0em
- Body: Pretendard | line-height 1.6-1.7 | label line-height 1.4-1.5
- Wrap defaults: headline word-break=keep-all, headline text-wrap=balance, body word-break=keep-all
- Scale guidance: 기본 스케일을 사용할 수 있지만 한글 문장 기준으로 실제 wrap을 먼저 검증한다.
- Hangul display safety: line-height >= 1.02 | tracking -0.02em to 0.01em | forced <br /> 금지 until breakpoint QA
- 한글 카피는 `word-break: keep-all`과 `overflow-wrap: normal`을 기본값으로 두고, 주요 헤딩에서 지원되면 `text-wrap: balance`를 사용한다.
- 한글 헤딩에는 breakpoint 검증 전 강제 `<br />`를 넣지 않는다. 줄바꿈이 필요하면 먼저 컨테이너 폭과 type scale을 조정한다.
- 한글 화면은 영문 시안의 `ch` 기준이나 single-line slogan 가정에 맞추지 말고, 실제 한글 문장으로 wrap을 검증한다.
- Pretendard 같은 한글 display 헤딩은 line-height를 1.02 미만으로 낮추지 않는다.

## Responsive Resilience

- 모바일에서 horizontal scroll이 생기거나 primary action이 화면 밖으로 나가면 컴포넌트 구현이 완료된 것이 아니다.
- Required viewport checks: 320px, 360px, 390px, 430px, 768px, 1024px, 1440px
- Buttons, CTA groups, tabs, filter chips, and toolbar actions must not rely on fixed px widths or mobile-hostile min-width values.
- Every button-like control needs max-inline-size: 100%; controls inside flex/grid parents need min-inline-size: 0 so labels can shrink or wrap.
- Action rows must wrap or stack at narrow widths; two-button rows need a <=480px fallback before implementation is complete.
- Long Korean CTA labels must be tested with real copy. Prefer wrapping/stacking over clipping, overflow hidden, or forcing white-space: nowrap.
- Horizontal rails, tickers, score strips, and carousels must not reveal partially clipped text. Either size cards so visible items are complete, or use compact labels such as icon+code in the rail and move full names to the detailed surface.

---

## button / primary-button

**역할**: Primary action button for the most important local action.

**탐지 출처**: baseline

### 구조 (Anatomy)

- container
- label
- leading-icon(optional)
- trailing-icon(optional)

### 상태 (States)

| 상태 | 설명 |
|------|------|
| `default` | 기본 상태 |
| `hover` | 마우스 오버 시 |
| `active` | 클릭/탭 중 |
| `disabled` | 비활성 (상호작용 불가) |
| `loading` | 로딩 중 (스피너 표시) |

### 토큰 바인딩

```
surface: var(--color-brand-primary)
text: var(--color-text-inverse)
border: var(--color-brand-primary)
radius: var(--radius-md)
padding: var(--space-12) var(--space-24)
max-inline-size: 100%
min-inline-size: 0
label-wrap: white-space: normal
font: var(--font-body) / var(--text-md) / semibold
hover-surface: var(--color-link-hover)
focus-ring: box-shadow: 0 0 0 2px var(--color-surface), 0 0 0 4px var(--color-brand-primary)
motion: background var(--duration-180) var(--ease-standard)
```

### 접근성

- role="button"
- aria-disabled="true" when disabled
- aria-busy="true" when loading
- 최소 44x44 터치 영역
- 텍스트 대비 4.5:1 이상
- 320px viewport에서도 버튼 전체와 focus ring이 화면 밖으로 나가지 않아야 함

### 브랜드 적용

- [minimal+precise] hover: 미세한 opacity 또는 underline만 + 정확한 border/outline 변화
- [minimal+precise] motion: 80-120ms, 거의 즉각적 + 120-180ms, 군더더기 없는 전환
- [minimal+precise] color: monochrome 기반, accent 최소화 + 정확한 semantic 분리, 모호한 중간 톤 지양
- [금지] (editorial) hover: 텍스트 underline 또는 color shift, 장식적 효과 없음 — 이것을 피할 것
- [금지] (editorial) motion: 콘텐츠 전환 위주, UI chrome 모션 최소화 — 이것을 피할 것

### Visual Adaptation Hints

- **cta_prominence**: CTA prominence는 restrained이다. 데이터 작업 흐름을 가리지 않도록 primary만 선명하게 두고 나머지는 text/ghost로 낮춘다. (source=cards; confidence=0.29; provenance=inferred; direction=flat card planes를 기본으로 하고, 압축된 spacing과 얇은 divider 중심의 hierarchy. 중간 반경으로 제품 UI 절제 유지.; evidence=surface=flat, density=dense, corner=medium, layout=data-review-surface)

### 레퍼런스 근거

- **Carbon Design System**: These components can toggle between the AI variant and the default variant depending on the user’s interaction. If the user manually overrides the ...
- **Primer**: I get so much joy from writing HTML and CSS, and design systems are one level up - systematically making UIs accessible and consistent. I love conc...

### 구현 노트

- 기존에 같은 역할의 컴포넌트가 있으면 토큰 교체부터 시작
- variant prop으로 시각적 변형을 관리 (하드코딩 금지)
- size prop: sm / md / lg (터치 영역은 항상 최소 44px 보장)
- 모든 버튼은 `max-inline-size: 100%`와 `min-inline-size: 0`을 기본 보호값으로 갖고, 긴 라벨은 모바일에서 wrap 또는 action-group stack으로 처리
- fixed `width`/`min-width` px 값으로 CTA 폭을 고정하지 않음 — 필요하면 container query 또는 <=480px stack fallback을 함께 정의
- 반응형 검증: 320px, 360px, 390px, 430px에서 control overflow와 viewport horizontal scroll이 없어야 함
- action row는 narrow viewport에서 `flex-wrap: wrap` 또는 세로 stack으로 전환하고, overflow-x 숨김으로 문제를 덮지 않음

---

## button / secondary-button

**역할**: Secondary action button with lower emphasis than the primary action.

**탐지 출처**: baseline

### 구조 (Anatomy)

- container
- label
- leading-icon(optional)
- trailing-icon(optional)

### 상태 (States)

| 상태 | 설명 |
|------|------|
| `default` | 기본 상태 |
| `hover` | 마우스 오버 시 |
| `active` | 클릭/탭 중 |
| `disabled` | 비활성 (상호작용 불가) |
| `loading` | 로딩 중 (스피너 표시) |

### 토큰 바인딩

```
surface: var(--color-brand-primary)
text: var(--color-text-inverse)
border: var(--color-brand-primary)
radius: var(--radius-md)
padding: var(--space-12) var(--space-24)
max-inline-size: 100%
min-inline-size: 0
label-wrap: white-space: normal
font: var(--font-body) / var(--text-md) / semibold
hover-surface: var(--color-link-hover)
focus-ring: box-shadow: 0 0 0 2px var(--color-surface), 0 0 0 4px var(--color-brand-primary)
motion: background var(--duration-180) var(--ease-standard)
```

### 접근성

- role="button"
- aria-disabled="true" when disabled
- aria-busy="true" when loading
- 최소 44x44 터치 영역
- 텍스트 대비 4.5:1 이상
- 320px viewport에서도 버튼 전체와 focus ring이 화면 밖으로 나가지 않아야 함

### 브랜드 적용

- [minimal+precise] hover: 미세한 opacity 또는 underline만 + 정확한 border/outline 변화
- [minimal+precise] motion: 80-120ms, 거의 즉각적 + 120-180ms, 군더더기 없는 전환
- [minimal+precise] color: monochrome 기반, accent 최소화 + 정확한 semantic 분리, 모호한 중간 톤 지양
- [금지] (editorial) hover: 텍스트 underline 또는 color shift, 장식적 효과 없음 — 이것을 피할 것
- [금지] (editorial) motion: 콘텐츠 전환 위주, UI chrome 모션 최소화 — 이것을 피할 것

### Visual Adaptation Hints

- **cta_prominence**: CTA prominence는 restrained이다. 데이터 작업 흐름을 가리지 않도록 primary만 선명하게 두고 나머지는 text/ghost로 낮춘다. (source=cards; confidence=0.29; provenance=inferred; direction=flat card planes를 기본으로 하고, 압축된 spacing과 얇은 divider 중심의 hierarchy. 중간 반경으로 제품 UI 절제 유지.; evidence=surface=flat, density=dense, corner=medium, layout=data-review-surface)

### 레퍼런스 근거

- **Carbon Design System**: These components can toggle between the AI variant and the default variant depending on the user’s interaction. If the user manually overrides the ...
- **Primer**: I get so much joy from writing HTML and CSS, and design systems are one level up - systematically making UIs accessible and consistent. I love conc...

### 구현 노트

- 기존에 같은 역할의 컴포넌트가 있으면 토큰 교체부터 시작
- variant prop으로 시각적 변형을 관리 (하드코딩 금지)
- size prop: sm / md / lg (터치 영역은 항상 최소 44px 보장)
- 모든 버튼은 `max-inline-size: 100%`와 `min-inline-size: 0`을 기본 보호값으로 갖고, 긴 라벨은 모바일에서 wrap 또는 action-group stack으로 처리
- fixed `width`/`min-width` px 값으로 CTA 폭을 고정하지 않음 — 필요하면 container query 또는 <=480px stack fallback을 함께 정의
- 반응형 검증: 320px, 360px, 390px, 430px에서 control overflow와 viewport horizontal scroll이 없어야 함
- action row는 narrow viewport에서 `flex-wrap: wrap` 또는 세로 stack으로 전환하고, overflow-x 숨김으로 문제를 덮지 않음

---

## button / icon-button

**역할**: Icon-only action with explicit accessible name and stable hit target.

**탐지 출처**: baseline

### 구조 (Anatomy)

- container
- label
- leading-icon(optional)
- trailing-icon(optional)

### 상태 (States)

| 상태 | 설명 |
|------|------|
| `default` | 기본 상태 |
| `hover` | 마우스 오버 시 |
| `active` | 클릭/탭 중 |
| `disabled` | 비활성 (상호작용 불가) |
| `loading` | 로딩 중 (스피너 표시) |

### 토큰 바인딩

```
surface: var(--color-brand-primary)
text: var(--color-text-inverse)
border: var(--color-brand-primary)
radius: var(--radius-md)
padding: var(--space-12) var(--space-24)
max-inline-size: 100%
min-inline-size: 0
label-wrap: white-space: normal
font: var(--font-body) / var(--text-md) / semibold
hover-surface: var(--color-link-hover)
focus-ring: box-shadow: 0 0 0 2px var(--color-surface), 0 0 0 4px var(--color-brand-primary)
motion: background var(--duration-180) var(--ease-standard)
```

### 접근성

- role="button"
- aria-disabled="true" when disabled
- aria-busy="true" when loading
- 최소 44x44 터치 영역
- 텍스트 대비 4.5:1 이상
- 320px viewport에서도 버튼 전체와 focus ring이 화면 밖으로 나가지 않아야 함

### 브랜드 적용

- [minimal+precise] hover: 미세한 opacity 또는 underline만 + 정확한 border/outline 변화
- [minimal+precise] motion: 80-120ms, 거의 즉각적 + 120-180ms, 군더더기 없는 전환
- [minimal+precise] color: monochrome 기반, accent 최소화 + 정확한 semantic 분리, 모호한 중간 톤 지양
- [금지] (editorial) hover: 텍스트 underline 또는 color shift, 장식적 효과 없음 — 이것을 피할 것
- [금지] (editorial) motion: 콘텐츠 전환 위주, UI chrome 모션 최소화 — 이것을 피할 것

### Visual Adaptation Hints

- **cta_prominence**: CTA prominence는 restrained이다. 데이터 작업 흐름을 가리지 않도록 primary만 선명하게 두고 나머지는 text/ghost로 낮춘다. (source=cards; confidence=0.29; provenance=inferred; direction=flat card planes를 기본으로 하고, 압축된 spacing과 얇은 divider 중심의 hierarchy. 중간 반경으로 제품 UI 절제 유지.; evidence=surface=flat, density=dense, corner=medium, layout=data-review-surface)

### 레퍼런스 근거

- **Carbon Design System**: These components can toggle between the AI variant and the default variant depending on the user’s interaction. If the user manually overrides the ...
- **Primer**: I get so much joy from writing HTML and CSS, and design systems are one level up - systematically making UIs accessible and consistent. I love conc...

### 구현 노트

- 기존에 같은 역할의 컴포넌트가 있으면 토큰 교체부터 시작
- variant prop으로 시각적 변형을 관리 (하드코딩 금지)
- size prop: sm / md / lg (터치 영역은 항상 최소 44px 보장)
- 모든 버튼은 `max-inline-size: 100%`와 `min-inline-size: 0`을 기본 보호값으로 갖고, 긴 라벨은 모바일에서 wrap 또는 action-group stack으로 처리
- fixed `width`/`min-width` px 값으로 CTA 폭을 고정하지 않음 — 필요하면 container query 또는 <=480px stack fallback을 함께 정의
- 반응형 검증: 320px, 360px, 390px, 430px에서 control overflow와 viewport horizontal scroll이 없어야 함
- action row는 narrow viewport에서 `flex-wrap: wrap` 또는 세로 stack으로 전환하고, overflow-x 숨김으로 문제를 덮지 않음

---

## document / article-body

**역할**: long-form article body — prose block + heading anchor

**탐지 출처**: reference documentation

### 구조 (Anatomy)

- container
- header
- content-area
- footer(optional)
- action(optional)

### 상태 (States)

| 상태 | 설명 |
|------|------|
| `default` | 기본 상태 |
| `loading` | 로딩 중 (스피너 표시) |
| `empty` | 데이터 없음 |
| `error` | 유효성 검증 실패 |

### 토큰 바인딩

```
surface: var(--color-surface)
border: var(--color-border)
radius: var(--radius-md)
padding: var(--space-16) var(--space-20)
heading-font: var(--font-heading) / var(--text-md) / semibold
body-font: var(--font-body) / var(--text-sm) / regular
text: var(--color-text)
text-muted: var(--color-text-muted)
```

### 접근성

- 적절한 heading level 사용
- 데이터 테이블은 scope와 caption 필수
- 빈 상태에서 안내 텍스트 제공

### 브랜드 적용

- [minimal+precise] hover: 미세한 opacity 또는 underline만 + 정확한 border/outline 변화
- [minimal+precise] motion: 80-120ms, 거의 즉각적 + 120-180ms, 군더더기 없는 전환
- [minimal+precise] color: monochrome 기반, accent 최소화 + 정확한 semantic 분리, 모호한 중간 톤 지양
- [금지] (editorial) hover: 텍스트 underline 또는 color shift, 장식적 효과 없음 — 이것을 피할 것
- [금지] (editorial) motion: 콘텐츠 전환 위주, UI chrome 모션 최소화 — 이것을 피할 것

### 레퍼런스 근거

- **Carbon Design System**: AI chat is a conversational framework between a user and an AI that can aid in creating tasks, finding insights, tracking documents, and more. For ...
- **Primer**: The GitHub Design Infrastructure and Design Engineering teams build and maintain Primer — this includes our CSS framework, style guide documentatio...

### 구현 노트

- 기존에 같은 역할의 컴포넌트가 있으면 토큰 교체부터 시작
- variant prop으로 시각적 변형을 관리 (하드코딩 금지)

---

## document / table-of-contents

**역할**: TOC sidebar with anchor-linked heading outline

**탐지 출처**: reference documentation

### 구조 (Anatomy)

- container
- header
- content-area
- footer(optional)
- action(optional)

### 상태 (States)

| 상태 | 설명 |
|------|------|
| `default` | 기본 상태 |
| `loading` | 로딩 중 (스피너 표시) |
| `empty` | 데이터 없음 |
| `error` | 유효성 검증 실패 |

### 토큰 바인딩

```
surface: var(--color-surface)
border: var(--color-border)
radius: var(--radius-md)
padding: var(--space-16) var(--space-20)
heading-font: var(--font-heading) / var(--text-md) / semibold
body-font: var(--font-body) / var(--text-sm) / regular
text: var(--color-text)
text-muted: var(--color-text-muted)
```

### 접근성

- 적절한 heading level 사용
- 데이터 테이블은 scope와 caption 필수
- 빈 상태에서 안내 텍스트 제공

### 브랜드 적용

- [minimal+precise] hover: 미세한 opacity 또는 underline만 + 정확한 border/outline 변화
- [minimal+precise] motion: 80-120ms, 거의 즉각적 + 120-180ms, 군더더기 없는 전환
- [minimal+precise] color: monochrome 기반, accent 최소화 + 정확한 semantic 분리, 모호한 중간 톤 지양
- [금지] (editorial) hover: 텍스트 underline 또는 color shift, 장식적 효과 없음 — 이것을 피할 것
- [금지] (editorial) motion: 콘텐츠 전환 위주, UI chrome 모션 최소화 — 이것을 피할 것

### Visual Adaptation Hints

- **operational_surface_role**: 주 작업 표면은 card wall이 아니라 table/list/rail/canvas 계열로 설계한다. 압축된 표면에서는 row height, column rhythm, sticky toolbar, source/update label을 우선한다. (source=data_display; confidence=0.29; provenance=inferred; direction=정보 밀도를 유지하되 thin dividers와 restrained accent로 hierarchy를 만든다.; evidence=layout=dashboard-grid, density=dense, layout=data-review-surface)
- **filter_nav_density**: filter/nav density는 compact하다. chip, scope, pagination을 촘촘하게 묶되 의미 단위별 group은 분리한다. (source=navigation; confidence=0.23; provenance=inferred; direction=고정 sidebar 또는 split-pane navigation을 우선하고, 현재 위치와 scope를 항상 명시한다.; evidence=Split-pane workspace, layout=data-review-surface, density=dense)
- **chart_panel_framing**: 차트 패널은 flush surface와 thin divider 중심으로 프레이밍한다. 헤더의 metric, controls, plot 영역을 분리하고 내부 여백은 촘촘하게 관리한다. (source=data_display; confidence=0.29; provenance=inferred; direction=정보 밀도를 유지하되 thin dividers와 restrained accent로 hierarchy를 만든다.; evidence=layout=dashboard-grid, density=dense, layout=data-review-surface, surface=flat)

### 레퍼런스 근거

- **Carbon Design System**: AI chat is a conversational framework between a user and an AI that can aid in creating tasks, finding insights, tracking documents, and more. For ...
- **Primer**: The GitHub Design Infrastructure and Design Engineering teams build and maintain Primer — this includes our CSS framework, style guide documentatio...

### 구현 노트

- 기존에 같은 역할의 컴포넌트가 있으면 토큰 교체부터 시작
- variant prop으로 시각적 변형을 관리 (하드코딩 금지)
- 반응형 검증: 320px, 360px, 390px, 430px에서 control overflow와 viewport horizontal scroll이 없어야 함
- action row는 narrow viewport에서 `flex-wrap: wrap` 또는 세로 stack으로 전환하고, overflow-x 숨김으로 문제를 덮지 않음

---

## document / heading-anchor

**역할**: h1~h6 heading with #id anchor and copy-link

**탐지 출처**: reference documentation

### 구조 (Anatomy)

- container
- header
- content-area
- footer(optional)
- action(optional)

### 상태 (States)

| 상태 | 설명 |
|------|------|
| `default` | 기본 상태 |
| `loading` | 로딩 중 (스피너 표시) |
| `empty` | 데이터 없음 |
| `error` | 유효성 검증 실패 |

### 토큰 바인딩

```
surface: var(--color-surface)
border: var(--color-border)
radius: var(--radius-md)
padding: var(--space-16) var(--space-20)
heading-font: var(--font-heading) / var(--text-md) / semibold
body-font: var(--font-body) / var(--text-sm) / regular
text: var(--color-text)
text-muted: var(--color-text-muted)
```

### 접근성

- 적절한 heading level 사용
- 데이터 테이블은 scope와 caption 필수
- 빈 상태에서 안내 텍스트 제공

### 브랜드 적용

- [minimal+precise] hover: 미세한 opacity 또는 underline만 + 정확한 border/outline 변화
- [minimal+precise] motion: 80-120ms, 거의 즉각적 + 120-180ms, 군더더기 없는 전환
- [minimal+precise] color: monochrome 기반, accent 최소화 + 정확한 semantic 분리, 모호한 중간 톤 지양
- [금지] (editorial) hover: 텍스트 underline 또는 color shift, 장식적 효과 없음 — 이것을 피할 것
- [금지] (editorial) motion: 콘텐츠 전환 위주, UI chrome 모션 최소화 — 이것을 피할 것

### 레퍼런스 근거

- **Carbon Design System**: AI chat is a conversational framework between a user and an AI that can aid in creating tasks, finding insights, tracking documents, and more. For ...
- **Primer**: The GitHub Design Infrastructure and Design Engineering teams build and maintain Primer — this includes our CSS framework, style guide documentatio...

### 구현 노트

- 기존에 같은 역할의 컴포넌트가 있으면 토큰 교체부터 시작
- variant prop으로 시각적 변형을 관리 (하드코딩 금지)

---

## document / prose-block

**역할**: prose reading block rendering markdown article content

**탐지 출처**: reference documentation

### 구조 (Anatomy)

- container
- header
- content-area
- footer(optional)
- action(optional)

### 상태 (States)

| 상태 | 설명 |
|------|------|
| `default` | 기본 상태 |
| `loading` | 로딩 중 (스피너 표시) |
| `empty` | 데이터 없음 |
| `error` | 유효성 검증 실패 |

### 토큰 바인딩

```
surface: var(--color-surface)
border: var(--color-border)
radius: var(--radius-md)
padding: var(--space-16) var(--space-20)
heading-font: var(--font-heading) / var(--text-md) / semibold
body-font: var(--font-body) / var(--text-sm) / regular
text: var(--color-text)
text-muted: var(--color-text-muted)
```

### 접근성

- 적절한 heading level 사용
- 데이터 테이블은 scope와 caption 필수
- 빈 상태에서 안내 텍스트 제공

### 브랜드 적용

- [minimal+precise] hover: 미세한 opacity 또는 underline만 + 정확한 border/outline 변화
- [minimal+precise] motion: 80-120ms, 거의 즉각적 + 120-180ms, 군더더기 없는 전환
- [minimal+precise] color: monochrome 기반, accent 최소화 + 정확한 semantic 분리, 모호한 중간 톤 지양
- [금지] (editorial) hover: 텍스트 underline 또는 color shift, 장식적 효과 없음 — 이것을 피할 것
- [금지] (editorial) motion: 콘텐츠 전환 위주, UI chrome 모션 최소화 — 이것을 피할 것

### 레퍼런스 근거

- **Carbon Design System**: AI chat is a conversational framework between a user and an AI that can aid in creating tasks, finding insights, tracking documents, and more. For ...
- **Primer**: The GitHub Design Infrastructure and Design Engineering teams build and maintain Primer — this includes our CSS framework, style guide documentatio...

### 구현 노트

- 기존에 같은 역할의 컴포넌트가 있으면 토큰 교체부터 시작
- variant prop으로 시각적 변형을 관리 (하드코딩 금지)

---

## document / reading-pane

**역할**: main reading column, measured width 65–75ch

**탐지 출처**: reference documentation

### 구조 (Anatomy)

- container
- header
- content-area
- footer(optional)
- action(optional)

### 상태 (States)

| 상태 | 설명 |
|------|------|
| `default` | 기본 상태 |
| `loading` | 로딩 중 (스피너 표시) |
| `empty` | 데이터 없음 |
| `error` | 유효성 검증 실패 |

### 토큰 바인딩

```
surface: var(--color-surface)
border: var(--color-border)
radius: var(--radius-md)
padding: var(--space-16) var(--space-20)
heading-font: var(--font-heading) / var(--text-md) / semibold
body-font: var(--font-body) / var(--text-sm) / regular
text: var(--color-text)
text-muted: var(--color-text-muted)
```

### 접근성

- 적절한 heading level 사용
- 데이터 테이블은 scope와 caption 필수
- 빈 상태에서 안내 텍스트 제공

### 브랜드 적용

- [minimal+precise] hover: 미세한 opacity 또는 underline만 + 정확한 border/outline 변화
- [minimal+precise] motion: 80-120ms, 거의 즉각적 + 120-180ms, 군더더기 없는 전환
- [minimal+precise] color: monochrome 기반, accent 최소화 + 정확한 semantic 분리, 모호한 중간 톤 지양
- [금지] (editorial) hover: 텍스트 underline 또는 color shift, 장식적 효과 없음 — 이것을 피할 것
- [금지] (editorial) motion: 콘텐츠 전환 위주, UI chrome 모션 최소화 — 이것을 피할 것

### Visual Adaptation Hints

- **operational_surface_role**: 주 작업 표면은 card wall이 아니라 table/list/rail/canvas 계열로 설계한다. 압축된 표면에서는 row height, column rhythm, sticky toolbar, source/update label을 우선한다. (source=data_display; confidence=0.29; provenance=inferred; direction=정보 밀도를 유지하되 thin dividers와 restrained accent로 hierarchy를 만든다.; evidence=layout=dashboard-grid, density=dense, layout=data-review-surface)

### 레퍼런스 근거

- **Carbon Design System**: AI chat is a conversational framework between a user and an AI that can aid in creating tasks, finding insights, tracking documents, and more. For ...
- **Primer**: The GitHub Design Infrastructure and Design Engineering teams build and maintain Primer — this includes our CSS framework, style guide documentatio...

### 구현 노트

- 기존에 같은 역할의 컴포넌트가 있으면 토큰 교체부터 시작
- variant prop으로 시각적 변형을 관리 (하드코딩 금지)

---

## document / footnote

**역할**: numbered reference footnote inside article body

**탐지 출처**: reference documentation

### 구조 (Anatomy)

- container
- header
- content-area
- footer(optional)
- action(optional)

### 상태 (States)

| 상태 | 설명 |
|------|------|
| `default` | 기본 상태 |
| `loading` | 로딩 중 (스피너 표시) |
| `empty` | 데이터 없음 |
| `error` | 유효성 검증 실패 |

### 토큰 바인딩

```
surface: var(--color-surface)
border: var(--color-border)
radius: var(--radius-md)
padding: var(--space-16) var(--space-20)
heading-font: var(--font-heading) / var(--text-md) / semibold
body-font: var(--font-body) / var(--text-sm) / regular
text: var(--color-text)
text-muted: var(--color-text-muted)
```

### 접근성

- 적절한 heading level 사용
- 데이터 테이블은 scope와 caption 필수
- 빈 상태에서 안내 텍스트 제공

### 브랜드 적용

- [minimal+precise] hover: 미세한 opacity 또는 underline만 + 정확한 border/outline 변화
- [minimal+precise] motion: 80-120ms, 거의 즉각적 + 120-180ms, 군더더기 없는 전환
- [minimal+precise] color: monochrome 기반, accent 최소화 + 정확한 semantic 분리, 모호한 중간 톤 지양
- [금지] (editorial) hover: 텍스트 underline 또는 color shift, 장식적 효과 없음 — 이것을 피할 것
- [금지] (editorial) motion: 콘텐츠 전환 위주, UI chrome 모션 최소화 — 이것을 피할 것

### 레퍼런스 근거

- **Carbon Design System**: AI chat is a conversational framework between a user and an AI that can aid in creating tasks, finding insights, tracking documents, and more. For ...
- **Primer**: The GitHub Design Infrastructure and Design Engineering teams build and maintain Primer — this includes our CSS framework, style guide documentatio...

### 구현 노트

- 기존에 같은 역할의 컴포넌트가 있으면 토큰 교체부터 시작
- variant prop으로 시각적 변형을 관리 (하드코딩 금지)

---

## navigation / prev-next-pager

**역할**: bottom-of-article prev/next reference link

**탐지 출처**: reference documentation

### 구조 (Anatomy)

- container
- nav-item
- icon(optional)
- label
- indicator(active)
- badge(optional)

### 상태 (States)

| 상태 | 설명 |
|------|------|
| `default` | 기본 상태 |
| `hover` | 마우스 오버 시 |
| `active` | 클릭/탭 중 |
| `collapsed` | 접힌 상태 |

### 토큰 바인딩

```
surface: var(--color-surface)
text: var(--color-text-muted)
text-active: var(--color-text)
indicator: var(--color-brand-accent)
padding: var(--space-8) var(--space-16)
font: var(--font-body) / var(--text-sm) / medium
```

### 접근성

- nav landmark (role="navigation")
- aria-current="page" for active item
- 키보드 화살표 탐색 지원

### 브랜드 적용

- [minimal+precise] hover: 미세한 opacity 또는 underline만 + 정확한 border/outline 변화
- [minimal+precise] density: compact 가능, 불필요한 여백 제거 + 엄격한 spacing scale 준수, 임의 값 금지
- [minimal+precise] motion: 80-120ms, 거의 즉각적 + 120-180ms, 군더더기 없는 전환
- [금지] (editorial) hover: 텍스트 underline 또는 color shift, 장식적 효과 없음 — 이것을 피할 것
- [금지] (editorial) motion: 콘텐츠 전환 위주, UI chrome 모션 최소화 — 이것을 피할 것

### Visual Adaptation Hints

- **filter_nav_density**: filter/nav density는 compact하다. chip, scope, pagination을 촘촘하게 묶되 의미 단위별 group은 분리한다. (source=navigation; confidence=0.23; provenance=inferred; direction=고정 sidebar 또는 split-pane navigation을 우선하고, 현재 위치와 scope를 항상 명시한다.; evidence=Split-pane workspace, layout=data-review-surface, density=dense)

### 레퍼런스 근거

- **Carbon Design System**: Library menu navigation There are two kinds of symbols — library symbols and document symbols. Library symbols are available in any Sketch document...
- **Primer**: Octicon nav items navigation 12 px

### 구현 노트

- 기존에 같은 역할의 컴포넌트가 있으면 토큰 교체부터 시작
- variant prop으로 시각적 변형을 관리 (하드코딩 금지)
- active 상태는 URL/라우터와 자동 동기화
- 좁은 UI 텍스트는 Pretendard 기준 label line-height 1.4-1.5를 참고해 뭉침을 방지
- 반응형 검증: 320px, 360px, 390px, 430px에서 control overflow와 viewport horizontal scroll이 없어야 함
- action row는 narrow viewport에서 `flex-wrap: wrap` 또는 세로 stack으로 전환하고, overflow-x 숨김으로 문제를 덮지 않음

---

## document / link-card

**역할**: related article card with title + summary

**탐지 출처**: reference documentation

**Slot archetype**: `surface-card`

### 구조 (Anatomy)

- container
- inner-content

### 상태 (States)

| 상태 | 설명 |
|------|------|
| `default` | 기본 상태 |
| `hover` | 마우스 오버 시 |
| `focus-visible` | focus-visible |

### 토큰 바인딩

```
surface: var(--color-surface)
border: var(--color-border)
border-hover: var(--color-border-strong)
radius: var(--radius-lg)
padding: var(--space-32)
gap: var(--space-16)
motion: border-color var(--duration-180) var(--ease-standard)
```

### 접근성

- 카드 자체가 링크/버튼이면 <a>/<button> 래퍼 사용
- 장식적 카드는 단순 <article> 또는 <div>

### 브랜드 적용

- [minimal+precise] hover: 미세한 opacity 또는 underline만 + 정확한 border/outline 변화
- [minimal+precise] motion: 80-120ms, 거의 즉각적 + 120-180ms, 군더더기 없는 전환
- [minimal+precise] color: monochrome 기반, accent 최소화 + 정확한 semantic 분리, 모호한 중간 톤 지양
- [금지] (editorial) hover: 텍스트 underline 또는 color shift, 장식적 효과 없음 — 이것을 피할 것
- [금지] (editorial) motion: 콘텐츠 전환 위주, UI chrome 모션 최소화 — 이것을 피할 것

### Visual Adaptation Hints

- **card_elevation_tendency**: 카드는 거의 무그림자 평면으로 유지하고 tint/divider로 계층을 만든다. 압축된 spacing에서도 header/body/footer 구획은 divider나 tint로 유지한다. (source=cards; confidence=0.29; provenance=inferred; direction=flat card planes를 기본으로 하고, 압축된 spacing과 얇은 divider 중심의 hierarchy. 중간 반경으로 제품 UI 절제 유지.; evidence=surface=flat, density=dense, corner=medium)
- **border_vs_fill_emphasis**: fill 중심이다. neutral surface를 기본으로 하고 border는 상태 변화나 구획 보조에만 쓴다. (source=cards; confidence=0.29; provenance=inferred; direction=flat card planes를 기본으로 하고, 압축된 spacing과 얇은 divider 중심의 hierarchy. 중간 반경으로 제품 UI 절제 유지.; evidence=surface=flat, density=dense, corner=medium)

### 레퍼런스 근거

- **Carbon Design System**: AI chat is a conversational framework between a user and an AI that can aid in creating tasks, finding insights, tracking documents, and more. For ...
- **Primer**: The GitHub Design Infrastructure and Design Engineering teams build and maintain Primer — this includes our CSS framework, style guide documentatio...

### 구현 노트

- 기존에 같은 역할의 컴포넌트가 있으면 토큰 교체부터 시작
- variant prop으로 시각적 변형을 관리 (하드코딩 금지)

---

## document / api-reference-table

**역할**: endpoint/method/status/type API reference table

**탐지 출처**: api reference

### 구조 (Anatomy)

- container
- header
- content-area
- footer(optional)
- action(optional)

### 상태 (States)

| 상태 | 설명 |
|------|------|
| `default` | 기본 상태 |
| `loading` | 로딩 중 (스피너 표시) |
| `empty` | 데이터 없음 |
| `error` | 유효성 검증 실패 |

### 토큰 바인딩

```
surface: var(--color-surface)
border: var(--color-border)
radius: var(--radius-md)
padding: var(--space-16) var(--space-20)
heading-font: var(--font-heading) / var(--text-md) / semibold
body-font: var(--font-body) / var(--text-sm) / regular
text: var(--color-text)
text-muted: var(--color-text-muted)
```

### 접근성

- 적절한 heading level 사용
- 데이터 테이블은 scope와 caption 필수
- 빈 상태에서 안내 텍스트 제공

### 브랜드 적용

- [minimal+precise] hover: 미세한 opacity 또는 underline만 + 정확한 border/outline 변화
- [minimal+precise] motion: 80-120ms, 거의 즉각적 + 120-180ms, 군더더기 없는 전환
- [minimal+precise] color: monochrome 기반, accent 최소화 + 정확한 semantic 분리, 모호한 중간 톤 지양
- [금지] (editorial) hover: 텍스트 underline 또는 color shift, 장식적 효과 없음 — 이것을 피할 것
- [금지] (editorial) motion: 콘텐츠 전환 위주, UI chrome 모션 최소화 — 이것을 피할 것

### Visual Adaptation Hints

- **operational_surface_role**: 주 작업 표면은 card wall이 아니라 table/list/rail/canvas 계열로 설계한다. 압축된 표면에서는 row height, column rhythm, sticky toolbar, source/update label을 우선한다. (source=data_display; confidence=0.29; provenance=inferred; direction=정보 밀도를 유지하되 thin dividers와 restrained accent로 hierarchy를 만든다.; evidence=layout=dashboard-grid, density=dense, layout=data-review-surface)
- **filter_nav_density**: filter/nav density는 compact하다. chip, scope, pagination을 촘촘하게 묶되 의미 단위별 group은 분리한다. (source=navigation; confidence=0.23; provenance=inferred; direction=고정 sidebar 또는 split-pane navigation을 우선하고, 현재 위치와 scope를 항상 명시한다.; evidence=Split-pane workspace, layout=data-review-surface, density=dense)
- **chart_panel_framing**: 차트 패널은 flush surface와 thin divider 중심으로 프레이밍한다. 헤더의 metric, controls, plot 영역을 분리하고 내부 여백은 촘촘하게 관리한다. (source=data_display; confidence=0.29; provenance=inferred; direction=정보 밀도를 유지하되 thin dividers와 restrained accent로 hierarchy를 만든다.; evidence=layout=dashboard-grid, density=dense, layout=data-review-surface, surface=flat)

### 레퍼런스 근거

- **Carbon Design System**: AI chat is a conversational framework between a user and an AI that can aid in creating tasks, finding insights, tracking documents, and more. For ...
- **Primer**: The GitHub Design Infrastructure and Design Engineering teams build and maintain Primer — this includes our CSS framework, style guide documentatio...

### 구현 노트

- 기존에 같은 역할의 컴포넌트가 있으면 토큰 교체부터 시작
- variant prop으로 시각적 변형을 관리 (하드코딩 금지)
- 반응형 검증: 320px, 360px, 390px, 430px에서 control overflow와 viewport horizontal scroll이 없어야 함
- action row는 narrow viewport에서 `flex-wrap: wrap` 또는 세로 stack으로 전환하고, overflow-x 숨김으로 문제를 덮지 않음

---

## document / parameter-table

**역할**: parameter list (name/type/required/description)

**탐지 출처**: api reference

### 구조 (Anatomy)

- container
- header
- content-area
- footer(optional)
- action(optional)

### 상태 (States)

| 상태 | 설명 |
|------|------|
| `default` | 기본 상태 |
| `loading` | 로딩 중 (스피너 표시) |
| `empty` | 데이터 없음 |
| `error` | 유효성 검증 실패 |

### 토큰 바인딩

```
surface: var(--color-surface)
border: var(--color-border)
radius: var(--radius-md)
padding: var(--space-16) var(--space-20)
heading-font: var(--font-heading) / var(--text-md) / semibold
body-font: var(--font-body) / var(--text-sm) / regular
text: var(--color-text)
text-muted: var(--color-text-muted)
```

### 접근성

- 적절한 heading level 사용
- 데이터 테이블은 scope와 caption 필수
- 빈 상태에서 안내 텍스트 제공

### 브랜드 적용

- [minimal+precise] hover: 미세한 opacity 또는 underline만 + 정확한 border/outline 변화
- [minimal+precise] motion: 80-120ms, 거의 즉각적 + 120-180ms, 군더더기 없는 전환
- [minimal+precise] color: monochrome 기반, accent 최소화 + 정확한 semantic 분리, 모호한 중간 톤 지양
- [금지] (editorial) hover: 텍스트 underline 또는 color shift, 장식적 효과 없음 — 이것을 피할 것
- [금지] (editorial) motion: 콘텐츠 전환 위주, UI chrome 모션 최소화 — 이것을 피할 것

### Visual Adaptation Hints

- **operational_surface_role**: 주 작업 표면은 card wall이 아니라 table/list/rail/canvas 계열로 설계한다. 압축된 표면에서는 row height, column rhythm, sticky toolbar, source/update label을 우선한다. (source=data_display; confidence=0.29; provenance=inferred; direction=정보 밀도를 유지하되 thin dividers와 restrained accent로 hierarchy를 만든다.; evidence=layout=dashboard-grid, density=dense, layout=data-review-surface)
- **filter_nav_density**: filter/nav density는 compact하다. chip, scope, pagination을 촘촘하게 묶되 의미 단위별 group은 분리한다. (source=navigation; confidence=0.23; provenance=inferred; direction=고정 sidebar 또는 split-pane navigation을 우선하고, 현재 위치와 scope를 항상 명시한다.; evidence=Split-pane workspace, layout=data-review-surface, density=dense)
- **chart_panel_framing**: 차트 패널은 flush surface와 thin divider 중심으로 프레이밍한다. 헤더의 metric, controls, plot 영역을 분리하고 내부 여백은 촘촘하게 관리한다. (source=data_display; confidence=0.29; provenance=inferred; direction=정보 밀도를 유지하되 thin dividers와 restrained accent로 hierarchy를 만든다.; evidence=layout=dashboard-grid, density=dense, layout=data-review-surface, surface=flat)

### 레퍼런스 근거

- **Carbon Design System**: AI chat is a conversational framework between a user and an AI that can aid in creating tasks, finding insights, tracking documents, and more. For ...
- **Primer**: The GitHub Design Infrastructure and Design Engineering teams build and maintain Primer — this includes our CSS framework, style guide documentatio...

### 구현 노트

- 기존에 같은 역할의 컴포넌트가 있으면 토큰 교체부터 시작
- variant prop으로 시각적 변형을 관리 (하드코딩 금지)
- 반응형 검증: 320px, 360px, 390px, 430px에서 control overflow와 viewport horizontal scroll이 없어야 함
- action row는 narrow viewport에서 `flex-wrap: wrap` 또는 세로 stack으로 전환하고, overflow-x 숨김으로 문제를 덮지 않음

---

## navigation / version-switcher

**역할**: dropdown to switch doc version (v1/v2/latest)

**탐지 출처**: api reference

### 구조 (Anatomy)

- container
- nav-item
- icon(optional)
- label
- indicator(active)
- badge(optional)

### 상태 (States)

| 상태 | 설명 |
|------|------|
| `default` | 기본 상태 |
| `hover` | 마우스 오버 시 |
| `active` | 클릭/탭 중 |
| `collapsed` | 접힌 상태 |

### 토큰 바인딩

```
surface: var(--color-surface)
text: var(--color-text-muted)
text-active: var(--color-text)
indicator: var(--color-brand-accent)
padding: var(--space-8) var(--space-16)
font: var(--font-body) / var(--text-sm) / medium
```

### 접근성

- nav landmark (role="navigation")
- aria-current="page" for active item
- 키보드 화살표 탐색 지원

### 브랜드 적용

- [minimal+precise] hover: 미세한 opacity 또는 underline만 + 정확한 border/outline 변화
- [minimal+precise] density: compact 가능, 불필요한 여백 제거 + 엄격한 spacing scale 준수, 임의 값 금지
- [minimal+precise] motion: 80-120ms, 거의 즉각적 + 120-180ms, 군더더기 없는 전환
- [금지] (editorial) hover: 텍스트 underline 또는 color shift, 장식적 효과 없음 — 이것을 피할 것
- [금지] (editorial) motion: 콘텐츠 전환 위주, UI chrome 모션 최소화 — 이것을 피할 것

### Visual Adaptation Hints

- **filter_nav_density**: filter/nav density는 compact하다. chip, scope, pagination을 촘촘하게 묶되 의미 단위별 group은 분리한다. (source=navigation; confidence=0.23; provenance=inferred; direction=고정 sidebar 또는 split-pane navigation을 우선하고, 현재 위치와 scope를 항상 명시한다.; evidence=Split-pane workspace, layout=data-review-surface, density=dense)

### 레퍼런스 근거

- **Carbon Design System**: Library menu navigation There are two kinds of symbols — library symbols and document symbols. Library symbols are available in any Sketch document...
- **Primer**: Octicon nav items navigation 12 px

### 구현 노트

- 기존에 같은 역할의 컴포넌트가 있으면 토큰 교체부터 시작
- variant prop으로 시각적 변형을 관리 (하드코딩 금지)
- active 상태는 URL/라우터와 자동 동기화
- 좁은 UI 텍스트는 Pretendard 기준 label line-height 1.4-1.5를 참고해 뭉침을 방지
- 반응형 검증: 320px, 360px, 390px, 430px에서 control overflow와 viewport horizontal scroll이 없어야 함
- action row는 narrow viewport에서 `flex-wrap: wrap` 또는 세로 stack으로 전환하고, overflow-x 숨김으로 문제를 덮지 않음

---

## data-display / data-table

**역할**: 정렬·필터 가능한 데이터 테이블

**탐지 출처**: data tables

### 구조 (Anatomy)

- container
- header
- content-area
- footer(optional)
- action(optional)

### 상태 (States)

| 상태 | 설명 |
|------|------|
| `default` | 기본 상태 |
| `loading` | 로딩 중 (스피너 표시) |
| `empty` | 데이터 없음 |
| `error` | 유효성 검증 실패 |

### 토큰 바인딩

```
surface: var(--color-surface)
border: var(--color-border)
radius: var(--radius-md)
padding: var(--space-16) var(--space-20)
heading-font: var(--font-heading) / var(--text-md) / semibold
body-font: var(--font-body) / var(--text-sm) / regular
text: var(--color-text)
text-muted: var(--color-text-muted)
```

### 접근성

- 적절한 heading level 사용
- 데이터 테이블은 scope와 caption 필수
- 빈 상태에서 안내 텍스트 제공

### 브랜드 적용

- [minimal+precise] density: compact 가능, 불필요한 여백 제거 + 엄격한 spacing scale 준수, 임의 값 금지
- [minimal+precise] color: monochrome 기반, accent 최소화 + 정확한 semantic 분리, 모호한 중간 톤 지양
- [금지] (editorial) hover: 텍스트 underline 또는 color shift, 장식적 효과 없음 — 이것을 피할 것
- [금지] (editorial) motion: 콘텐츠 전환 위주, UI chrome 모션 최소화 — 이것을 피할 것

### Visual Adaptation Hints

- **operational_surface_role**: 주 작업 표면은 card wall이 아니라 table/list/rail/canvas 계열로 설계한다. 압축된 표면에서는 row height, column rhythm, sticky toolbar, source/update label을 우선한다. (source=data_display; confidence=0.29; provenance=inferred; direction=정보 밀도를 유지하되 thin dividers와 restrained accent로 hierarchy를 만든다.; evidence=layout=dashboard-grid, density=dense, layout=data-review-surface)
- **filter_nav_density**: filter/nav density는 compact하다. chip, scope, pagination을 촘촘하게 묶되 의미 단위별 group은 분리한다. (source=navigation; confidence=0.23; provenance=inferred; direction=고정 sidebar 또는 split-pane navigation을 우선하고, 현재 위치와 scope를 항상 명시한다.; evidence=Split-pane workspace, layout=data-review-surface, density=dense)
- **chart_panel_framing**: 차트 패널은 flush surface와 thin divider 중심으로 프레이밍한다. 헤더의 metric, controls, plot 영역을 분리하고 내부 여백은 촘촘하게 관리한다. (source=data_display; confidence=0.29; provenance=inferred; direction=정보 밀도를 유지하되 thin dividers와 restrained accent로 hierarchy를 만든다.; evidence=layout=dashboard-grid, density=dense, layout=data-review-surface, surface=flat)

### 레퍼런스 근거

- **Carbon Design System**: Data table Modal
- **Primer**: DataTable DataTable is a 2-dimensional data structure where each row is an item, and each column is a data point about the item.

### 구현 노트

- 기존에 같은 역할의 컴포넌트가 있으면 토큰 교체부터 시작
- variant prop으로 시각적 변형을 관리 (하드코딩 금지)
- 빈 상태(empty-state)와 에러 상태를 반드시 처리
- 좁은 UI 텍스트는 Pretendard 기준 label line-height 1.4-1.5를 참고해 뭉침을 방지
- 반응형 검증: 320px, 360px, 390px, 430px에서 control overflow와 viewport horizontal scroll이 없어야 함
- action row는 narrow viewport에서 `flex-wrap: wrap` 또는 세로 stack으로 전환하고, overflow-x 숨김으로 문제를 덮지 않음

---

## data-display / column-header

**역할**: 테이블 컬럼 헤더 (정렬 토글)

**탐지 출처**: data tables

### 구조 (Anatomy)

- container
- header
- content-area
- footer(optional)
- action(optional)

### 상태 (States)

| 상태 | 설명 |
|------|------|
| `default` | 기본 상태 |
| `loading` | 로딩 중 (스피너 표시) |
| `empty` | 데이터 없음 |
| `error` | 유효성 검증 실패 |

### 토큰 바인딩

```
surface: var(--color-surface)
border: var(--color-border)
radius: var(--radius-md)
padding: var(--space-16) var(--space-20)
heading-font: var(--font-heading) / var(--text-md) / semibold
body-font: var(--font-body) / var(--text-sm) / regular
text: var(--color-text)
text-muted: var(--color-text-muted)
```

### 접근성

- 적절한 heading level 사용
- 데이터 테이블은 scope와 caption 필수
- 빈 상태에서 안내 텍스트 제공

### 브랜드 적용

- [minimal+precise] density: compact 가능, 불필요한 여백 제거 + 엄격한 spacing scale 준수, 임의 값 금지
- [minimal+precise] color: monochrome 기반, accent 최소화 + 정확한 semantic 분리, 모호한 중간 톤 지양
- [금지] (editorial) hover: 텍스트 underline 또는 color shift, 장식적 효과 없음 — 이것을 피할 것
- [금지] (editorial) motion: 콘텐츠 전환 위주, UI chrome 모션 최소화 — 이것을 피할 것

### Visual Adaptation Hints

- **operational_surface_role**: 주 작업 표면은 card wall이 아니라 table/list/rail/canvas 계열로 설계한다. 압축된 표면에서는 row height, column rhythm, sticky toolbar, source/update label을 우선한다. (source=data_display; confidence=0.29; provenance=inferred; direction=정보 밀도를 유지하되 thin dividers와 restrained accent로 hierarchy를 만든다.; evidence=layout=dashboard-grid, density=dense, layout=data-review-surface)
- **chart_panel_framing**: 차트 패널은 flush surface와 thin divider 중심으로 프레이밍한다. 헤더의 metric, controls, plot 영역을 분리하고 내부 여백은 촘촘하게 관리한다. (source=data_display; confidence=0.29; provenance=inferred; direction=정보 밀도를 유지하되 thin dividers와 restrained accent로 hierarchy를 만든다.; evidence=layout=dashboard-grid, density=dense, layout=data-review-surface, surface=flat)

### 구현 노트

- 기존에 같은 역할의 컴포넌트가 있으면 토큰 교체부터 시작
- variant prop으로 시각적 변형을 관리 (하드코딩 금지)
- 빈 상태(empty-state)와 에러 상태를 반드시 처리
- 좁은 UI 텍스트는 Pretendard 기준 label line-height 1.4-1.5를 참고해 뭉침을 방지

---

## data-display / row-actions

**역할**: 행별 액션 메뉴

**탐지 출처**: data tables

### 구조 (Anatomy)

- container
- header
- content-area
- footer(optional)
- action(optional)

### 상태 (States)

| 상태 | 설명 |
|------|------|
| `default` | 기본 상태 |
| `loading` | 로딩 중 (스피너 표시) |
| `empty` | 데이터 없음 |
| `error` | 유효성 검증 실패 |

### 토큰 바인딩

```
surface: var(--color-surface)
border: var(--color-border)
radius: var(--radius-md)
padding: var(--space-16) var(--space-20)
heading-font: var(--font-heading) / var(--text-md) / semibold
body-font: var(--font-body) / var(--text-sm) / regular
text: var(--color-text)
text-muted: var(--color-text-muted)
```

### 접근성

- 적절한 heading level 사용
- 데이터 테이블은 scope와 caption 필수
- 빈 상태에서 안내 텍스트 제공

### 브랜드 적용

- [minimal+precise] density: compact 가능, 불필요한 여백 제거 + 엄격한 spacing scale 준수, 임의 값 금지
- [minimal+precise] color: monochrome 기반, accent 최소화 + 정확한 semantic 분리, 모호한 중간 톤 지양
- [금지] (editorial) hover: 텍스트 underline 또는 color shift, 장식적 효과 없음 — 이것을 피할 것
- [금지] (editorial) motion: 콘텐츠 전환 위주, UI chrome 모션 최소화 — 이것을 피할 것

### Visual Adaptation Hints

- **operational_surface_role**: 주 작업 표면은 card wall이 아니라 table/list/rail/canvas 계열로 설계한다. 압축된 표면에서는 row height, column rhythm, sticky toolbar, source/update label을 우선한다. (source=data_display; confidence=0.29; provenance=inferred; direction=정보 밀도를 유지하되 thin dividers와 restrained accent로 hierarchy를 만든다.; evidence=layout=dashboard-grid, density=dense, layout=data-review-surface)
- **chart_panel_framing**: 차트 패널은 flush surface와 thin divider 중심으로 프레이밍한다. 헤더의 metric, controls, plot 영역을 분리하고 내부 여백은 촘촘하게 관리한다. (source=data_display; confidence=0.29; provenance=inferred; direction=정보 밀도를 유지하되 thin dividers와 restrained accent로 hierarchy를 만든다.; evidence=layout=dashboard-grid, density=dense, layout=data-review-surface, surface=flat)

### 구현 노트

- 기존에 같은 역할의 컴포넌트가 있으면 토큰 교체부터 시작
- variant prop으로 시각적 변형을 관리 (하드코딩 금지)
- 빈 상태(empty-state)와 에러 상태를 반드시 처리
- 좁은 UI 텍스트는 Pretendard 기준 label line-height 1.4-1.5를 참고해 뭉침을 방지

---

## navigation / pagination

**역할**: 페이지 이동 컨트롤

**탐지 출처**: data tables

### 구조 (Anatomy)

- container
- nav-item
- icon(optional)
- label
- indicator(active)
- badge(optional)

### 상태 (States)

| 상태 | 설명 |
|------|------|
| `default` | 기본 상태 |
| `hover` | 마우스 오버 시 |
| `active` | 클릭/탭 중 |
| `collapsed` | 접힌 상태 |

### 토큰 바인딩

```
surface: var(--color-surface)
text: var(--color-text-muted)
text-active: var(--color-text)
indicator: var(--color-brand-accent)
padding: var(--space-8) var(--space-16)
font: var(--font-body) / var(--text-sm) / medium
```

### 접근성

- nav landmark (role="navigation")
- aria-current="page" for active item
- 키보드 화살표 탐색 지원

### 브랜드 적용

- [minimal+precise] hover: 미세한 opacity 또는 underline만 + 정확한 border/outline 변화
- [minimal+precise] density: compact 가능, 불필요한 여백 제거 + 엄격한 spacing scale 준수, 임의 값 금지
- [minimal+precise] motion: 80-120ms, 거의 즉각적 + 120-180ms, 군더더기 없는 전환
- [금지] (editorial) hover: 텍스트 underline 또는 color shift, 장식적 효과 없음 — 이것을 피할 것
- [금지] (editorial) motion: 콘텐츠 전환 위주, UI chrome 모션 최소화 — 이것을 피할 것

### Visual Adaptation Hints

- **filter_nav_density**: filter/nav density는 compact하다. chip, scope, pagination을 촘촘하게 묶되 의미 단위별 group은 분리한다. (source=navigation; confidence=0.23; provenance=inferred; direction=고정 sidebar 또는 split-pane navigation을 우선하고, 현재 위치와 scope를 항상 명시한다.; evidence=Split-pane workspace, layout=data-review-surface, density=dense)

### 레퍼런스 근거

- **Carbon Design System**: Library menu navigation There are two kinds of symbols — library symbols and document symbols. Library symbols are available in any Sketch document...
- **Primer**: Octicon nav items navigation 12 px

### 구현 노트

- 기존에 같은 역할의 컴포넌트가 있으면 토큰 교체부터 시작
- variant prop으로 시각적 변형을 관리 (하드코딩 금지)
- active 상태는 URL/라우터와 자동 동기화
- 좁은 UI 텍스트는 Pretendard 기준 label line-height 1.4-1.5를 참고해 뭉침을 방지
- 반응형 검증: 320px, 360px, 390px, 430px에서 control overflow와 viewport horizontal scroll이 없어야 함
- action row는 narrow viewport에서 `flex-wrap: wrap` 또는 세로 stack으로 전환하고, overflow-x 숨김으로 문제를 덮지 않음

---

## input / filter-chip

**역할**: 활성 필터를 칩으로 표시/해제

**탐지 출처**: data tables

### 구조 (Anatomy)

- container
- label
- input-area
- helper-text(optional)
- leading-icon(optional)
- clear-button(optional)

### 상태 (States)

| 상태 | 설명 |
|------|------|
| `default` | 기본 상태 |
| `focus` | 키보드 포커스 시 |
| `filled` | 값이 입력된 상태 |
| `error` | 유효성 검증 실패 |
| `disabled` | 비활성 (상호작용 불가) |
| `readonly` | 읽기 전용 |

### 토큰 바인딩

```
surface: var(--color-surface)
text: var(--color-text)
placeholder: var(--color-text-subtle)
border: var(--color-border)
border-focus: var(--color-brand-primary)
border-error: var(--color-danger)
radius: var(--radius-sm)
padding: var(--space-8) var(--space-12)
font: var(--font-body) / var(--text-md) / regular
```

### 접근성

- label과 input을 for/id로 연결
- aria-describedby로 helper/error text 연결
- aria-invalid="true" when error
- aria-required="true" when required

### 브랜드 적용

- [minimal+precise] hover: 미세한 opacity 또는 underline만 + 정확한 border/outline 변화
- [minimal+precise] density: compact 가능, 불필요한 여백 제거 + 엄격한 spacing scale 준수, 임의 값 금지
- [minimal+precise] feedback: 아이콘+텍스트 조합, 색상 배경 최소화 + 명확한 상태 구분, 진행률/결과를 수치로 표시
- [금지] (editorial) hover: 텍스트 underline 또는 color shift, 장식적 효과 없음 — 이것을 피할 것
- [금지] (editorial) motion: 콘텐츠 전환 위주, UI chrome 모션 최소화 — 이것을 피할 것

### Visual Adaptation Hints

- **filter_nav_density**: filter/nav density는 compact하다. chip, scope, pagination을 촘촘하게 묶되 의미 단위별 group은 분리한다. (source=navigation; confidence=0.23; provenance=inferred; direction=고정 sidebar 또는 split-pane navigation을 우선하고, 현재 위치와 scope를 항상 명시한다.; evidence=Split-pane workspace, layout=data-review-surface, density=dense)

### 레퍼런스 근거

- **Carbon Design System**: Number input Text input
- **Primer**: I worked in data visualization and map-making for most of my career, and solving design problems with data is my jam. To me there's something uniqu...

### 구현 노트

- 기존에 같은 역할의 컴포넌트가 있으면 토큰 교체부터 시작
- variant prop으로 시각적 변형을 관리 (하드코딩 금지)
- error 상태에서 helper text → error message로 자동 전환
- label은 항상 visible (placeholder만으로 대체 금지)
- 반응형 검증: 320px, 360px, 390px, 430px에서 control overflow와 viewport horizontal scroll이 없어야 함
- action row는 narrow viewport에서 `flex-wrap: wrap` 또는 세로 stack으로 전환하고, overflow-x 숨김으로 문제를 덮지 않음

---

## document / code-block

**역할**: syntax-highlighted code block with copy button + language tab

**탐지 출처**: code documentation

### 구조 (Anatomy)

- container
- header
- content-area
- footer(optional)
- action(optional)

### 상태 (States)

| 상태 | 설명 |
|------|------|
| `default` | 기본 상태 |
| `loading` | 로딩 중 (스피너 표시) |
| `empty` | 데이터 없음 |
| `error` | 유효성 검증 실패 |

### 토큰 바인딩

```
surface: var(--color-surface)
border: var(--color-border)
radius: var(--radius-md)
padding: var(--space-16) var(--space-20)
heading-font: var(--font-heading) / var(--text-md) / semibold
body-font: var(--font-body) / var(--text-sm) / regular
text: var(--color-text)
text-muted: var(--color-text-muted)
```

### 접근성

- 적절한 heading level 사용
- 데이터 테이블은 scope와 caption 필수
- 빈 상태에서 안내 텍스트 제공

### 브랜드 적용

- [minimal+precise] hover: 미세한 opacity 또는 underline만 + 정확한 border/outline 변화
- [minimal+precise] motion: 80-120ms, 거의 즉각적 + 120-180ms, 군더더기 없는 전환
- [minimal+precise] color: monochrome 기반, accent 최소화 + 정확한 semantic 분리, 모호한 중간 톤 지양
- [금지] (editorial) hover: 텍스트 underline 또는 color shift, 장식적 효과 없음 — 이것을 피할 것
- [금지] (editorial) motion: 콘텐츠 전환 위주, UI chrome 모션 최소화 — 이것을 피할 것

### 레퍼런스 근거

- **Carbon Design System**: AI chat is a conversational framework between a user and an AI that can aid in creating tasks, finding insights, tracking documents, and more. For ...
- **Primer**: The GitHub Design Infrastructure and Design Engineering teams build and maintain Primer — this includes our CSS framework, style guide documentatio...

### 구현 노트

- 기존에 같은 역할의 컴포넌트가 있으면 토큰 교체부터 시작
- variant prop으로 시각적 변형을 관리 (하드코딩 금지)

---

## document / inline-code

**역할**: inline code span with mono font and subtle background

**탐지 출처**: code documentation

### 구조 (Anatomy)

- container
- header
- content-area
- footer(optional)
- action(optional)

### 상태 (States)

| 상태 | 설명 |
|------|------|
| `default` | 기본 상태 |
| `loading` | 로딩 중 (스피너 표시) |
| `empty` | 데이터 없음 |
| `error` | 유효성 검증 실패 |

### 토큰 바인딩

```
surface: var(--color-surface)
border: var(--color-border)
radius: var(--radius-md)
padding: var(--space-16) var(--space-20)
heading-font: var(--font-heading) / var(--text-md) / semibold
body-font: var(--font-body) / var(--text-sm) / regular
text: var(--color-text)
text-muted: var(--color-text-muted)
```

### 접근성

- 적절한 heading level 사용
- 데이터 테이블은 scope와 caption 필수
- 빈 상태에서 안내 텍스트 제공

### 브랜드 적용

- [minimal+precise] hover: 미세한 opacity 또는 underline만 + 정확한 border/outline 변화
- [minimal+precise] motion: 80-120ms, 거의 즉각적 + 120-180ms, 군더더기 없는 전환
- [minimal+precise] color: monochrome 기반, accent 최소화 + 정확한 semantic 분리, 모호한 중간 톤 지양
- [금지] (editorial) hover: 텍스트 underline 또는 color shift, 장식적 효과 없음 — 이것을 피할 것
- [금지] (editorial) motion: 콘텐츠 전환 위주, UI chrome 모션 최소화 — 이것을 피할 것

### 레퍼런스 근거

- **Carbon Design System**: AI chat is a conversational framework between a user and an AI that can aid in creating tasks, finding insights, tracking documents, and more. For ...
- **Primer**: The GitHub Design Infrastructure and Design Engineering teams build and maintain Primer — this includes our CSS framework, style guide documentatio...

### 구현 노트

- 기존에 같은 역할의 컴포넌트가 있으면 토큰 교체부터 시작
- variant prop으로 시각적 변형을 관리 (하드코딩 금지)

---

## document / language-tab

**역할**: code block language switcher (ts/python/curl/go)

**탐지 출처**: code documentation

### 구조 (Anatomy)

- container
- header
- content-area
- footer(optional)
- action(optional)

### 상태 (States)

| 상태 | 설명 |
|------|------|
| `default` | 기본 상태 |
| `loading` | 로딩 중 (스피너 표시) |
| `empty` | 데이터 없음 |
| `error` | 유효성 검증 실패 |

### 토큰 바인딩

```
surface: var(--color-surface)
border: var(--color-border)
radius: var(--radius-md)
padding: var(--space-16) var(--space-20)
heading-font: var(--font-heading) / var(--text-md) / semibold
body-font: var(--font-body) / var(--text-sm) / regular
text: var(--color-text)
text-muted: var(--color-text-muted)
```

### 접근성

- 적절한 heading level 사용
- 데이터 테이블은 scope와 caption 필수
- 빈 상태에서 안내 텍스트 제공

### 브랜드 적용

- [minimal+precise] hover: 미세한 opacity 또는 underline만 + 정확한 border/outline 변화
- [minimal+precise] motion: 80-120ms, 거의 즉각적 + 120-180ms, 군더더기 없는 전환
- [minimal+precise] color: monochrome 기반, accent 최소화 + 정확한 semantic 분리, 모호한 중간 톤 지양
- [금지] (editorial) hover: 텍스트 underline 또는 color shift, 장식적 효과 없음 — 이것을 피할 것
- [금지] (editorial) motion: 콘텐츠 전환 위주, UI chrome 모션 최소화 — 이것을 피할 것

### Visual Adaptation Hints

- **filter_nav_density**: filter/nav density는 compact하다. chip, scope, pagination을 촘촘하게 묶되 의미 단위별 group은 분리한다. (source=navigation; confidence=0.23; provenance=inferred; direction=고정 sidebar 또는 split-pane navigation을 우선하고, 현재 위치와 scope를 항상 명시한다.; evidence=Split-pane workspace, layout=data-review-surface, density=dense)

### 레퍼런스 근거

- **Carbon Design System**: AI chat is a conversational framework between a user and an AI that can aid in creating tasks, finding insights, tracking documents, and more. For ...
- **Primer**: The GitHub Design Infrastructure and Design Engineering teams build and maintain Primer — this includes our CSS framework, style guide documentatio...

### 구현 노트

- 기존에 같은 역할의 컴포넌트가 있으면 토큰 교체부터 시작
- variant prop으로 시각적 변형을 관리 (하드코딩 금지)
- 반응형 검증: 320px, 360px, 390px, 430px에서 control overflow와 viewport horizontal scroll이 없어야 함
- action row는 narrow viewport에서 `flex-wrap: wrap` 또는 세로 stack으로 전환하고, overflow-x 숨김으로 문제를 덮지 않음

---

## button / copy-code-button

**역할**: copy-to-clipboard button for code block

**탐지 출처**: code documentation

### 구조 (Anatomy)

- container
- label
- leading-icon(optional)
- trailing-icon(optional)

### 상태 (States)

| 상태 | 설명 |
|------|------|
| `default` | 기본 상태 |
| `hover` | 마우스 오버 시 |
| `active` | 클릭/탭 중 |
| `disabled` | 비활성 (상호작용 불가) |
| `loading` | 로딩 중 (스피너 표시) |

### 토큰 바인딩

```
surface: var(--color-brand-primary)
text: var(--color-text-inverse)
border: var(--color-brand-primary)
radius: var(--radius-md)
padding: var(--space-12) var(--space-24)
max-inline-size: 100%
min-inline-size: 0
label-wrap: white-space: normal
font: var(--font-body) / var(--text-md) / semibold
hover-surface: var(--color-link-hover)
focus-ring: box-shadow: 0 0 0 2px var(--color-surface), 0 0 0 4px var(--color-brand-primary)
motion: background var(--duration-180) var(--ease-standard)
```

### 접근성

- role="button"
- aria-disabled="true" when disabled
- aria-busy="true" when loading
- 최소 44x44 터치 영역
- 텍스트 대비 4.5:1 이상
- 320px viewport에서도 버튼 전체와 focus ring이 화면 밖으로 나가지 않아야 함

### 브랜드 적용

- [minimal+precise] hover: 미세한 opacity 또는 underline만 + 정확한 border/outline 변화
- [minimal+precise] motion: 80-120ms, 거의 즉각적 + 120-180ms, 군더더기 없는 전환
- [minimal+precise] color: monochrome 기반, accent 최소화 + 정확한 semantic 분리, 모호한 중간 톤 지양
- [금지] (editorial) hover: 텍스트 underline 또는 color shift, 장식적 효과 없음 — 이것을 피할 것
- [금지] (editorial) motion: 콘텐츠 전환 위주, UI chrome 모션 최소화 — 이것을 피할 것

### Visual Adaptation Hints

- **cta_prominence**: CTA prominence는 restrained이다. 데이터 작업 흐름을 가리지 않도록 primary만 선명하게 두고 나머지는 text/ghost로 낮춘다. (source=cards; confidence=0.29; provenance=inferred; direction=flat card planes를 기본으로 하고, 압축된 spacing과 얇은 divider 중심의 hierarchy. 중간 반경으로 제품 UI 절제 유지.; evidence=surface=flat, density=dense, corner=medium, layout=data-review-surface)

### 레퍼런스 근거

- **Carbon Design System**: These components can toggle between the AI variant and the default variant depending on the user’s interaction. If the user manually overrides the ...
- **Primer**: I get so much joy from writing HTML and CSS, and design systems are one level up - systematically making UIs accessible and consistent. I love conc...

### 구현 노트

- 기존에 같은 역할의 컴포넌트가 있으면 토큰 교체부터 시작
- variant prop으로 시각적 변형을 관리 (하드코딩 금지)
- size prop: sm / md / lg (터치 영역은 항상 최소 44px 보장)
- 모든 버튼은 `max-inline-size: 100%`와 `min-inline-size: 0`을 기본 보호값으로 갖고, 긴 라벨은 모바일에서 wrap 또는 action-group stack으로 처리
- fixed `width`/`min-width` px 값으로 CTA 폭을 고정하지 않음 — 필요하면 container query 또는 <=480px stack fallback을 함께 정의
- 반응형 검증: 320px, 360px, 390px, 430px에서 control overflow와 viewport horizontal scroll이 없어야 함
- action row는 narrow viewport에서 `flex-wrap: wrap` 또는 세로 stack으로 전환하고, overflow-x 숨김으로 문제를 덮지 않음

---

## document / callout

**역할**: article callout — info/warning/tip/danger variants

**탐지 출처**: callout and admonition

### 구조 (Anatomy)

- container
- header
- content-area
- footer(optional)
- action(optional)

### 상태 (States)

| 상태 | 설명 |
|------|------|
| `default` | 기본 상태 |
| `loading` | 로딩 중 (스피너 표시) |
| `empty` | 데이터 없음 |
| `error` | 유효성 검증 실패 |

### 토큰 바인딩

```
surface: var(--color-surface)
border: var(--color-border)
radius: var(--radius-md)
padding: var(--space-16) var(--space-20)
heading-font: var(--font-heading) / var(--text-md) / semibold
body-font: var(--font-body) / var(--text-sm) / regular
text: var(--color-text)
text-muted: var(--color-text-muted)
```

### 접근성

- 적절한 heading level 사용
- 데이터 테이블은 scope와 caption 필수
- 빈 상태에서 안내 텍스트 제공

### 브랜드 적용

- [minimal+precise] hover: 미세한 opacity 또는 underline만 + 정확한 border/outline 변화
- [minimal+precise] motion: 80-120ms, 거의 즉각적 + 120-180ms, 군더더기 없는 전환
- [minimal+precise] color: monochrome 기반, accent 최소화 + 정확한 semantic 분리, 모호한 중간 톤 지양
- [금지] (editorial) hover: 텍스트 underline 또는 color shift, 장식적 효과 없음 — 이것을 피할 것
- [금지] (editorial) motion: 콘텐츠 전환 위주, UI chrome 모션 최소화 — 이것을 피할 것

### 레퍼런스 근거

- **Carbon Design System**: AI chat is a conversational framework between a user and an AI that can aid in creating tasks, finding insights, tracking documents, and more. For ...
- **Primer**: The GitHub Design Infrastructure and Design Engineering teams build and maintain Primer — this includes our CSS framework, style guide documentatio...

### 구현 노트

- 기존에 같은 역할의 컴포넌트가 있으면 토큰 교체부터 시작
- variant prop으로 시각적 변형을 관리 (하드코딩 금지)

---

## document / admonition-block

**역할**: admonition block with icon + label + body

**탐지 출처**: callout and admonition

### 구조 (Anatomy)

- container
- header
- content-area
- footer(optional)
- action(optional)

### 상태 (States)

| 상태 | 설명 |
|------|------|
| `default` | 기본 상태 |
| `loading` | 로딩 중 (스피너 표시) |
| `empty` | 데이터 없음 |
| `error` | 유효성 검증 실패 |

### 토큰 바인딩

```
surface: var(--color-surface)
border: var(--color-border)
radius: var(--radius-md)
padding: var(--space-16) var(--space-20)
heading-font: var(--font-heading) / var(--text-md) / semibold
body-font: var(--font-body) / var(--text-sm) / regular
text: var(--color-text)
text-muted: var(--color-text-muted)
```

### 접근성

- 적절한 heading level 사용
- 데이터 테이블은 scope와 caption 필수
- 빈 상태에서 안내 텍스트 제공

### 브랜드 적용

- [minimal+precise] hover: 미세한 opacity 또는 underline만 + 정확한 border/outline 변화
- [minimal+precise] motion: 80-120ms, 거의 즉각적 + 120-180ms, 군더더기 없는 전환
- [minimal+precise] color: monochrome 기반, accent 최소화 + 정확한 semantic 분리, 모호한 중간 톤 지양
- [금지] (editorial) hover: 텍스트 underline 또는 color shift, 장식적 효과 없음 — 이것을 피할 것
- [금지] (editorial) motion: 콘텐츠 전환 위주, UI chrome 모션 최소화 — 이것을 피할 것

### 레퍼런스 근거

- **Carbon Design System**: AI chat is a conversational framework between a user and an AI that can aid in creating tasks, finding insights, tracking documents, and more. For ...
- **Primer**: The GitHub Design Infrastructure and Design Engineering teams build and maintain Primer — this includes our CSS framework, style guide documentatio...

### 구현 노트

- 기존에 같은 역할의 컴포넌트가 있으면 토큰 교체부터 시작
- variant prop으로 시각적 변형을 관리 (하드코딩 금지)

---

## input / search-field

**역할**: 검색 입력 필드

**탐지 출처**: search and filter

### 구조 (Anatomy)

- container
- label
- input-area
- helper-text(optional)
- leading-icon(optional)
- clear-button(optional)

### 상태 (States)

| 상태 | 설명 |
|------|------|
| `default` | 기본 상태 |
| `focus` | 키보드 포커스 시 |
| `filled` | 값이 입력된 상태 |
| `error` | 유효성 검증 실패 |
| `disabled` | 비활성 (상호작용 불가) |
| `readonly` | 읽기 전용 |

### 토큰 바인딩

```
surface: var(--color-surface)
text: var(--color-text)
placeholder: var(--color-text-subtle)
border: var(--color-border)
border-focus: var(--color-brand-primary)
border-error: var(--color-danger)
radius: var(--radius-sm)
padding: var(--space-8) var(--space-12)
font: var(--font-body) / var(--text-md) / regular
```

### 접근성

- label과 input을 for/id로 연결
- aria-describedby로 helper/error text 연결
- aria-invalid="true" when error
- aria-required="true" when required

### 브랜드 적용

- [minimal+precise] hover: 미세한 opacity 또는 underline만 + 정확한 border/outline 변화
- [minimal+precise] density: compact 가능, 불필요한 여백 제거 + 엄격한 spacing scale 준수, 임의 값 금지
- [minimal+precise] feedback: 아이콘+텍스트 조합, 색상 배경 최소화 + 명확한 상태 구분, 진행률/결과를 수치로 표시
- [금지] (editorial) hover: 텍스트 underline 또는 color shift, 장식적 효과 없음 — 이것을 피할 것
- [금지] (editorial) motion: 콘텐츠 전환 위주, UI chrome 모션 최소화 — 이것을 피할 것

### Visual Adaptation Hints

- **filter_nav_density**: filter/nav density는 compact하다. chip, scope, pagination을 촘촘하게 묶되 의미 단위별 group은 분리한다. (source=navigation; confidence=0.23; provenance=inferred; direction=고정 sidebar 또는 split-pane navigation을 우선하고, 현재 위치와 scope를 항상 명시한다.; evidence=Split-pane workspace, layout=data-review-surface, density=dense)

### 레퍼런스 근거

- **Carbon Design System**: Number input Text input
- **Primer**: I worked in data visualization and map-making for most of my career, and solving design problems with data is my jam. To me there's something uniqu...

### 구현 노트

- 기존에 같은 역할의 컴포넌트가 있으면 토큰 교체부터 시작
- variant prop으로 시각적 변형을 관리 (하드코딩 금지)
- error 상태에서 helper text → error message로 자동 전환
- label은 항상 visible (placeholder만으로 대체 금지)
- 반응형 검증: 320px, 360px, 390px, 430px에서 control overflow와 viewport horizontal scroll이 없어야 함
- action row는 narrow viewport에서 `flex-wrap: wrap` 또는 세로 stack으로 전환하고, overflow-x 숨김으로 문제를 덮지 않음

---

## data-display / search-results

**역할**: 검색 결과 목록

**탐지 출처**: search and filter

### 구조 (Anatomy)

- container
- header
- content-area
- footer(optional)
- action(optional)

### 상태 (States)

| 상태 | 설명 |
|------|------|
| `default` | 기본 상태 |
| `loading` | 로딩 중 (스피너 표시) |
| `empty` | 데이터 없음 |
| `error` | 유효성 검증 실패 |

### 토큰 바인딩

```
surface: var(--color-surface)
border: var(--color-border)
radius: var(--radius-md)
padding: var(--space-16) var(--space-20)
heading-font: var(--font-heading) / var(--text-md) / semibold
body-font: var(--font-body) / var(--text-sm) / regular
text: var(--color-text)
text-muted: var(--color-text-muted)
```

### 접근성

- 적절한 heading level 사용
- 데이터 테이블은 scope와 caption 필수
- 빈 상태에서 안내 텍스트 제공

### 브랜드 적용

- [minimal+precise] density: compact 가능, 불필요한 여백 제거 + 엄격한 spacing scale 준수, 임의 값 금지
- [minimal+precise] color: monochrome 기반, accent 최소화 + 정확한 semantic 분리, 모호한 중간 톤 지양
- [금지] (editorial) hover: 텍스트 underline 또는 color shift, 장식적 효과 없음 — 이것을 피할 것
- [금지] (editorial) motion: 콘텐츠 전환 위주, UI chrome 모션 최소화 — 이것을 피할 것

### Visual Adaptation Hints

- **card_elevation_tendency**: 카드는 거의 무그림자 평면으로 유지하고 tint/divider로 계층을 만든다. 압축된 spacing에서도 header/body/footer 구획은 divider나 tint로 유지한다. (source=cards; confidence=0.29; provenance=inferred; direction=flat card planes를 기본으로 하고, 압축된 spacing과 얇은 divider 중심의 hierarchy. 중간 반경으로 제품 UI 절제 유지.; evidence=surface=flat, density=dense, corner=medium)
- **border_vs_fill_emphasis**: fill 중심이다. neutral surface를 기본으로 하고 border는 상태 변화나 구획 보조에만 쓴다. (source=cards; confidence=0.29; provenance=inferred; direction=flat card planes를 기본으로 하고, 압축된 spacing과 얇은 divider 중심의 hierarchy. 중간 반경으로 제품 UI 절제 유지.; evidence=surface=flat, density=dense, corner=medium)
- **filter_nav_density**: filter/nav density는 compact하다. chip, scope, pagination을 촘촘하게 묶되 의미 단위별 group은 분리한다. (source=navigation; confidence=0.23; provenance=inferred; direction=고정 sidebar 또는 split-pane navigation을 우선하고, 현재 위치와 scope를 항상 명시한다.; evidence=Split-pane workspace, layout=data-review-surface, density=dense)
- **chart_panel_framing**: 차트 패널은 flush surface와 thin divider 중심으로 프레이밍한다. 헤더의 metric, controls, plot 영역을 분리하고 내부 여백은 촘촘하게 관리한다. (source=data_display; confidence=0.29; provenance=inferred; direction=정보 밀도를 유지하되 thin dividers와 restrained accent로 hierarchy를 만든다.; evidence=layout=dashboard-grid, density=dense, layout=data-review-surface, surface=flat)

### 구현 노트

- 기존에 같은 역할의 컴포넌트가 있으면 토큰 교체부터 시작
- variant prop으로 시각적 변형을 관리 (하드코딩 금지)
- 빈 상태(empty-state)와 에러 상태를 반드시 처리
- 좁은 UI 텍스트는 Pretendard 기준 label line-height 1.4-1.5를 참고해 뭉침을 방지

---

## input / filter-panel

**역할**: 필터 옵션 패널

**탐지 출처**: search and filter

### 구조 (Anatomy)

- container
- label
- input-area
- helper-text(optional)
- leading-icon(optional)
- clear-button(optional)

### 상태 (States)

| 상태 | 설명 |
|------|------|
| `default` | 기본 상태 |
| `focus` | 키보드 포커스 시 |
| `filled` | 값이 입력된 상태 |
| `error` | 유효성 검증 실패 |
| `disabled` | 비활성 (상호작용 불가) |
| `readonly` | 읽기 전용 |

### 토큰 바인딩

```
surface: var(--color-surface)
text: var(--color-text)
placeholder: var(--color-text-subtle)
border: var(--color-border)
border-focus: var(--color-brand-primary)
border-error: var(--color-danger)
radius: var(--radius-sm)
padding: var(--space-8) var(--space-12)
font: var(--font-body) / var(--text-md) / regular
```

### 접근성

- label과 input을 for/id로 연결
- aria-describedby로 helper/error text 연결
- aria-invalid="true" when error
- aria-required="true" when required

### 브랜드 적용

- [minimal+precise] hover: 미세한 opacity 또는 underline만 + 정확한 border/outline 변화
- [minimal+precise] density: compact 가능, 불필요한 여백 제거 + 엄격한 spacing scale 준수, 임의 값 금지
- [minimal+precise] feedback: 아이콘+텍스트 조합, 색상 배경 최소화 + 명확한 상태 구분, 진행률/결과를 수치로 표시
- [금지] (editorial) hover: 텍스트 underline 또는 color shift, 장식적 효과 없음 — 이것을 피할 것
- [금지] (editorial) motion: 콘텐츠 전환 위주, UI chrome 모션 최소화 — 이것을 피할 것

### Visual Adaptation Hints

- **card_elevation_tendency**: 카드는 거의 무그림자 평면으로 유지하고 tint/divider로 계층을 만든다. 압축된 spacing에서도 header/body/footer 구획은 divider나 tint로 유지한다. (source=cards; confidence=0.29; provenance=inferred; direction=flat card planes를 기본으로 하고, 압축된 spacing과 얇은 divider 중심의 hierarchy. 중간 반경으로 제품 UI 절제 유지.; evidence=surface=flat, density=dense, corner=medium)
- **border_vs_fill_emphasis**: fill 중심이다. neutral surface를 기본으로 하고 border는 상태 변화나 구획 보조에만 쓴다. (source=cards; confidence=0.29; provenance=inferred; direction=flat card planes를 기본으로 하고, 압축된 spacing과 얇은 divider 중심의 hierarchy. 중간 반경으로 제품 UI 절제 유지.; evidence=surface=flat, density=dense, corner=medium)
- **filter_nav_density**: filter/nav density는 compact하다. chip, scope, pagination을 촘촘하게 묶되 의미 단위별 group은 분리한다. (source=navigation; confidence=0.23; provenance=inferred; direction=고정 sidebar 또는 split-pane navigation을 우선하고, 현재 위치와 scope를 항상 명시한다.; evidence=Split-pane workspace, layout=data-review-surface, density=dense)
- **chart_panel_framing**: 차트 패널은 flush surface와 thin divider 중심으로 프레이밍한다. 헤더의 metric, controls, plot 영역을 분리하고 내부 여백은 촘촘하게 관리한다. (source=data_display; confidence=0.29; provenance=inferred; direction=정보 밀도를 유지하되 thin dividers와 restrained accent로 hierarchy를 만든다.; evidence=layout=dashboard-grid, density=dense, layout=data-review-surface, surface=flat)

### 레퍼런스 근거

- **Carbon Design System**: Number input Text input
- **Primer**: I worked in data visualization and map-making for most of my career, and solving design problems with data is my jam. To me there's something uniqu...

### 구현 노트

- 기존에 같은 역할의 컴포넌트가 있으면 토큰 교체부터 시작
- variant prop으로 시각적 변형을 관리 (하드코딩 금지)
- error 상태에서 helper text → error message로 자동 전환
- label은 항상 visible (placeholder만으로 대체 금지)
- 반응형 검증: 320px, 360px, 390px, 430px에서 control overflow와 viewport horizontal scroll이 없어야 함
- action row는 narrow viewport에서 `flex-wrap: wrap` 또는 세로 stack으로 전환하고, overflow-x 숨김으로 문제를 덮지 않음

---

## overlay / autocomplete

**역할**: 자동완성 드롭다운

**탐지 출처**: search and filter

### 구조 (Anatomy)

- backdrop
- container
- header
- content
- footer(optional)
- close-button

### 상태 (States)

| 상태 | 설명 |
|------|------|
| `closed` | 닫힌 상태 |
| `opening` | 열리는 중 (전환 애니메이션) |
| `open` | 열린 상태 |
| `closing` | 닫히는 중 |

### 토큰 바인딩

```
surface: var(--color-surface-elevated)
backdrop: rgb(0 0 0 / 0.5)
radius: var(--radius-lg)
padding: var(--space-24)
border: var(--color-border)
motion: opacity var(--duration-180) var(--ease-standard)
```

### 접근성

- role="dialog" with aria-modal="true"
- focus trap (Tab 순환)
- Escape로 닫기
- aria-labelledby로 제목 연결
- 닫은 후 trigger 요소로 포커스 복귀

### 브랜드 적용

- [minimal+precise] motion: 80-120ms, 거의 즉각적 + 120-180ms, 군더더기 없는 전환
- [minimal+precise] density: compact 가능, 불필요한 여백 제거 + 엄격한 spacing scale 준수, 임의 값 금지
- [금지] (editorial) hover: 텍스트 underline 또는 color shift, 장식적 효과 없음 — 이것을 피할 것
- [금지] (editorial) motion: 콘텐츠 전환 위주, UI chrome 모션 최소화 — 이것을 피할 것

### 레퍼런스 근거

- **Primer**: Autocomplete Autocomplete allows users to quickly filter through a list of options and pick one or more values for a field.

### 구현 노트

- 기존에 같은 역할의 컴포넌트가 있으면 토큰 교체부터 시작
- variant prop으로 시각적 변형을 관리 (하드코딩 금지)
- Escape / backdrop click으로 닫기, 열 때 첫 focusable 요소로 이동

---

## input / text-field

**역할**: 단일 줄 텍스트 입력

**탐지 출처**: forms

### 구조 (Anatomy)

- container
- label
- input-area
- helper-text(optional)
- leading-icon(optional)
- clear-button(optional)

### 상태 (States)

| 상태 | 설명 |
|------|------|
| `default` | 기본 상태 |
| `focus` | 키보드 포커스 시 |
| `filled` | 값이 입력된 상태 |
| `error` | 유효성 검증 실패 |
| `disabled` | 비활성 (상호작용 불가) |
| `readonly` | 읽기 전용 |

### 토큰 바인딩

```
surface: var(--color-surface)
text: var(--color-text)
placeholder: var(--color-text-subtle)
border: var(--color-border)
border-focus: var(--color-brand-primary)
border-error: var(--color-danger)
radius: var(--radius-sm)
padding: var(--space-8) var(--space-12)
font: var(--font-body) / var(--text-md) / regular
```

### 접근성

- label과 input을 for/id로 연결
- aria-describedby로 helper/error text 연결
- aria-invalid="true" when error
- aria-required="true" when required

### 브랜드 적용

- [minimal+precise] hover: 미세한 opacity 또는 underline만 + 정확한 border/outline 변화
- [minimal+precise] density: compact 가능, 불필요한 여백 제거 + 엄격한 spacing scale 준수, 임의 값 금지
- [minimal+precise] feedback: 아이콘+텍스트 조합, 색상 배경 최소화 + 명확한 상태 구분, 진행률/결과를 수치로 표시
- [금지] (editorial) hover: 텍스트 underline 또는 color shift, 장식적 효과 없음 — 이것을 피할 것
- [금지] (editorial) motion: 콘텐츠 전환 위주, UI chrome 모션 최소화 — 이것을 피할 것

### 레퍼런스 근거

- **Carbon Design System**: Number input Text input
- **Primer**: I worked in data visualization and map-making for most of my career, and solving design problems with data is my jam. To me there's something uniqu...

### 구현 노트

- 기존에 같은 역할의 컴포넌트가 있으면 토큰 교체부터 시작
- variant prop으로 시각적 변형을 관리 (하드코딩 금지)
- error 상태에서 helper text → error message로 자동 전환
- label은 항상 visible (placeholder만으로 대체 금지)
- 반응형 검증: 320px, 360px, 390px, 430px에서 control overflow와 viewport horizontal scroll이 없어야 함
- action row는 narrow viewport에서 `flex-wrap: wrap` 또는 세로 stack으로 전환하고, overflow-x 숨김으로 문제를 덮지 않음

---

## input / textarea

**역할**: 여러 줄 텍스트 입력

**탐지 출처**: forms

### 구조 (Anatomy)

- container
- label
- input-area
- helper-text(optional)
- leading-icon(optional)
- clear-button(optional)

### 상태 (States)

| 상태 | 설명 |
|------|------|
| `default` | 기본 상태 |
| `focus` | 키보드 포커스 시 |
| `filled` | 값이 입력된 상태 |
| `error` | 유효성 검증 실패 |
| `disabled` | 비활성 (상호작용 불가) |
| `readonly` | 읽기 전용 |

### 토큰 바인딩

```
surface: var(--color-surface)
text: var(--color-text)
placeholder: var(--color-text-subtle)
border: var(--color-border)
border-focus: var(--color-brand-primary)
border-error: var(--color-danger)
radius: var(--radius-sm)
padding: var(--space-8) var(--space-12)
font: var(--font-body) / var(--text-md) / regular
```

### 접근성

- label과 input을 for/id로 연결
- aria-describedby로 helper/error text 연결
- aria-invalid="true" when error
- aria-required="true" when required

### 브랜드 적용

- [minimal+precise] hover: 미세한 opacity 또는 underline만 + 정확한 border/outline 변화
- [minimal+precise] density: compact 가능, 불필요한 여백 제거 + 엄격한 spacing scale 준수, 임의 값 금지
- [minimal+precise] feedback: 아이콘+텍스트 조합, 색상 배경 최소화 + 명확한 상태 구분, 진행률/결과를 수치로 표시
- [금지] (editorial) hover: 텍스트 underline 또는 color shift, 장식적 효과 없음 — 이것을 피할 것
- [금지] (editorial) motion: 콘텐츠 전환 위주, UI chrome 모션 최소화 — 이것을 피할 것

### 레퍼런스 근거

- **Carbon Design System**: Number input Text input
- **Primer**: I worked in data visualization and map-making for most of my career, and solving design problems with data is my jam. To me there's something uniqu...

### 구현 노트

- 기존에 같은 역할의 컴포넌트가 있으면 토큰 교체부터 시작
- variant prop으로 시각적 변형을 관리 (하드코딩 금지)
- error 상태에서 helper text → error message로 자동 전환
- label은 항상 visible (placeholder만으로 대체 금지)
- 반응형 검증: 320px, 360px, 390px, 430px에서 control overflow와 viewport horizontal scroll이 없어야 함
- action row는 narrow viewport에서 `flex-wrap: wrap` 또는 세로 stack으로 전환하고, overflow-x 숨김으로 문제를 덮지 않음

---

## input / select

**역할**: 드롭다운 선택

**탐지 출처**: forms

### 구조 (Anatomy)

- container
- label
- input-area
- helper-text(optional)
- leading-icon(optional)
- clear-button(optional)

### 상태 (States)

| 상태 | 설명 |
|------|------|
| `default` | 기본 상태 |
| `focus` | 키보드 포커스 시 |
| `filled` | 값이 입력된 상태 |
| `error` | 유효성 검증 실패 |
| `disabled` | 비활성 (상호작용 불가) |
| `readonly` | 읽기 전용 |

### 토큰 바인딩

```
surface: var(--color-surface)
text: var(--color-text)
placeholder: var(--color-text-subtle)
border: var(--color-border)
border-focus: var(--color-brand-primary)
border-error: var(--color-danger)
radius: var(--radius-sm)
padding: var(--space-8) var(--space-12)
font: var(--font-body) / var(--text-md) / regular
```

### 접근성

- label과 input을 for/id로 연결
- aria-describedby로 helper/error text 연결
- aria-invalid="true" when error
- aria-required="true" when required

### 브랜드 적용

- [minimal+precise] hover: 미세한 opacity 또는 underline만 + 정확한 border/outline 변화
- [minimal+precise] density: compact 가능, 불필요한 여백 제거 + 엄격한 spacing scale 준수, 임의 값 금지
- [minimal+precise] feedback: 아이콘+텍스트 조합, 색상 배경 최소화 + 명확한 상태 구분, 진행률/결과를 수치로 표시
- [금지] (editorial) hover: 텍스트 underline 또는 color shift, 장식적 효과 없음 — 이것을 피할 것
- [금지] (editorial) motion: 콘텐츠 전환 위주, UI chrome 모션 최소화 — 이것을 피할 것

### 레퍼런스 근거

- **Carbon Design System**: Select Data table
- **Primer**: Primer color design tokens are made available within data-attribute selectors on the body tag or other high level dom element. There are three dist...

### 구현 노트

- 기존에 같은 역할의 컴포넌트가 있으면 토큰 교체부터 시작
- variant prop으로 시각적 변형을 관리 (하드코딩 금지)
- error 상태에서 helper text → error message로 자동 전환
- label은 항상 visible (placeholder만으로 대체 금지)
- 반응형 검증: 320px, 360px, 390px, 430px에서 control overflow와 viewport horizontal scroll이 없어야 함
- action row는 narrow viewport에서 `flex-wrap: wrap` 또는 세로 stack으로 전환하고, overflow-x 숨김으로 문제를 덮지 않음

---

## input / checkbox

**역할**: 체크박스

**탐지 출처**: forms

### 구조 (Anatomy)

- container
- label
- input-area
- helper-text(optional)
- leading-icon(optional)
- clear-button(optional)

### 상태 (States)

| 상태 | 설명 |
|------|------|
| `default` | 기본 상태 |
| `focus` | 키보드 포커스 시 |
| `filled` | 값이 입력된 상태 |
| `error` | 유효성 검증 실패 |
| `disabled` | 비활성 (상호작용 불가) |
| `readonly` | 읽기 전용 |

### 토큰 바인딩

```
surface: var(--color-surface)
text: var(--color-text)
placeholder: var(--color-text-subtle)
border: var(--color-border)
border-focus: var(--color-brand-primary)
border-error: var(--color-danger)
radius: var(--radius-sm)
padding: var(--space-8) var(--space-12)
font: var(--font-body) / var(--text-md) / regular
```

### 접근성

- label과 input을 for/id로 연결
- aria-describedby로 helper/error text 연결
- aria-invalid="true" when error
- aria-required="true" when required

### 브랜드 적용

- [minimal+precise] hover: 미세한 opacity 또는 underline만 + 정확한 border/outline 변화
- [minimal+precise] density: compact 가능, 불필요한 여백 제거 + 엄격한 spacing scale 준수, 임의 값 금지
- [minimal+precise] feedback: 아이콘+텍스트 조합, 색상 배경 최소화 + 명확한 상태 구분, 진행률/결과를 수치로 표시
- [금지] (editorial) hover: 텍스트 underline 또는 color shift, 장식적 효과 없음 — 이것을 피할 것
- [금지] (editorial) motion: 콘텐츠 전환 위주, UI chrome 모션 최소화 — 이것을 피할 것

### 레퍼런스 근거

- **Carbon Design System**: Checkbox Form
- **Primer**: I worked in data visualization and map-making for most of my career, and solving design problems with data is my jam. To me there's something uniqu...

### 구현 노트

- 기존에 같은 역할의 컴포넌트가 있으면 토큰 교체부터 시작
- variant prop으로 시각적 변형을 관리 (하드코딩 금지)
- error 상태에서 helper text → error message로 자동 전환
- label은 항상 visible (placeholder만으로 대체 금지)
- 반응형 검증: 320px, 360px, 390px, 430px에서 control overflow와 viewport horizontal scroll이 없어야 함
- action row는 narrow viewport에서 `flex-wrap: wrap` 또는 세로 stack으로 전환하고, overflow-x 숨김으로 문제를 덮지 않음

---

## input / radio-group

**역할**: 라디오 버튼 그룹

**탐지 출처**: forms

### 구조 (Anatomy)

- container
- label
- input-area
- helper-text(optional)
- leading-icon(optional)
- clear-button(optional)

### 상태 (States)

| 상태 | 설명 |
|------|------|
| `default` | 기본 상태 |
| `focus` | 키보드 포커스 시 |
| `filled` | 값이 입력된 상태 |
| `error` | 유효성 검증 실패 |
| `disabled` | 비활성 (상호작용 불가) |
| `readonly` | 읽기 전용 |

### 토큰 바인딩

```
surface: var(--color-surface)
text: var(--color-text)
placeholder: var(--color-text-subtle)
border: var(--color-border)
border-focus: var(--color-brand-primary)
border-error: var(--color-danger)
radius: var(--radius-sm)
padding: var(--space-8) var(--space-12)
font: var(--font-body) / var(--text-md) / regular
```

### 접근성

- label과 input을 for/id로 연결
- aria-describedby로 helper/error text 연결
- aria-invalid="true" when error
- aria-required="true" when required

### 브랜드 적용

- [minimal+precise] hover: 미세한 opacity 또는 underline만 + 정확한 border/outline 변화
- [minimal+precise] density: compact 가능, 불필요한 여백 제거 + 엄격한 spacing scale 준수, 임의 값 금지
- [minimal+precise] feedback: 아이콘+텍스트 조합, 색상 배경 최소화 + 명확한 상태 구분, 진행률/결과를 수치로 표시
- [금지] (editorial) hover: 텍스트 underline 또는 color shift, 장식적 효과 없음 — 이것을 피할 것
- [금지] (editorial) motion: 콘텐츠 전환 위주, UI chrome 모션 최소화 — 이것을 피할 것

### 레퍼런스 근거

- **Carbon Design System**: Number input Text input
- **Primer**: I worked in data visualization and map-making for most of my career, and solving design problems with data is my jam. To me there's something uniqu...

### 구현 노트

- 기존에 같은 역할의 컴포넌트가 있으면 토큰 교체부터 시작
- variant prop으로 시각적 변형을 관리 (하드코딩 금지)
- error 상태에서 helper text → error message로 자동 전환
- label은 항상 visible (placeholder만으로 대체 금지)
- 반응형 검증: 320px, 360px, 390px, 430px에서 control overflow와 viewport horizontal scroll이 없어야 함
- action row는 narrow viewport에서 `flex-wrap: wrap` 또는 세로 stack으로 전환하고, overflow-x 숨김으로 문제를 덮지 않음

---

## input / form-section

**역할**: 폼 섹션 그룹핑과 레이블

**탐지 출처**: forms

### 구조 (Anatomy)

- container
- label
- input-area
- helper-text(optional)
- leading-icon(optional)
- clear-button(optional)

### 상태 (States)

| 상태 | 설명 |
|------|------|
| `default` | 기본 상태 |
| `focus` | 키보드 포커스 시 |
| `filled` | 값이 입력된 상태 |
| `error` | 유효성 검증 실패 |
| `disabled` | 비활성 (상호작용 불가) |
| `readonly` | 읽기 전용 |

### 토큰 바인딩

```
surface: var(--color-surface)
text: var(--color-text)
placeholder: var(--color-text-subtle)
border: var(--color-border)
border-focus: var(--color-brand-primary)
border-error: var(--color-danger)
radius: var(--radius-sm)
padding: var(--space-8) var(--space-12)
font: var(--font-body) / var(--text-md) / regular
```

### 접근성

- label과 input을 for/id로 연결
- aria-describedby로 helper/error text 연결
- aria-invalid="true" when error
- aria-required="true" when required

### 브랜드 적용

- [minimal+precise] hover: 미세한 opacity 또는 underline만 + 정확한 border/outline 변화
- [minimal+precise] density: compact 가능, 불필요한 여백 제거 + 엄격한 spacing scale 준수, 임의 값 금지
- [minimal+precise] feedback: 아이콘+텍스트 조합, 색상 배경 최소화 + 명확한 상태 구분, 진행률/결과를 수치로 표시
- [금지] (editorial) hover: 텍스트 underline 또는 color shift, 장식적 효과 없음 — 이것을 피할 것
- [금지] (editorial) motion: 콘텐츠 전환 위주, UI chrome 모션 최소화 — 이것을 피할 것

### 레퍼런스 근거

- **Carbon Design System**: Number input Text input
- **Primer**: I worked in data visualization and map-making for most of my career, and solving design problems with data is my jam. To me there's something uniqu...

### 구현 노트

- 기존에 같은 역할의 컴포넌트가 있으면 토큰 교체부터 시작
- variant prop으로 시각적 변형을 관리 (하드코딩 금지)
- error 상태에서 helper text → error message로 자동 전환
- label은 항상 visible (placeholder만으로 대체 금지)
- 반응형 검증: 320px, 360px, 390px, 430px에서 control overflow와 viewport horizontal scroll이 없어야 함
- action row는 narrow viewport에서 `flex-wrap: wrap` 또는 세로 stack으로 전환하고, overflow-x 숨김으로 문제를 덮지 않음

---

## button / form-actions

**역할**: 폼 하단 제출/취소 버튼 영역

**탐지 출처**: forms

### 구조 (Anatomy)

- container
- label
- leading-icon(optional)
- trailing-icon(optional)

### 상태 (States)

| 상태 | 설명 |
|------|------|
| `default` | 기본 상태 |
| `hover` | 마우스 오버 시 |
| `active` | 클릭/탭 중 |
| `disabled` | 비활성 (상호작용 불가) |
| `loading` | 로딩 중 (스피너 표시) |

### 토큰 바인딩

```
surface: var(--color-brand-primary)
text: var(--color-text-inverse)
border: var(--color-brand-primary)
radius: var(--radius-md)
padding: var(--space-12) var(--space-24)
max-inline-size: 100%
min-inline-size: 0
label-wrap: white-space: normal
font: var(--font-body) / var(--text-md) / semibold
hover-surface: var(--color-link-hover)
focus-ring: box-shadow: 0 0 0 2px var(--color-surface), 0 0 0 4px var(--color-brand-primary)
motion: background var(--duration-180) var(--ease-standard)
```

### 접근성

- role="button"
- aria-disabled="true" when disabled
- aria-busy="true" when loading
- 최소 44x44 터치 영역
- 텍스트 대비 4.5:1 이상
- 320px viewport에서도 버튼 전체와 focus ring이 화면 밖으로 나가지 않아야 함

### 브랜드 적용

- [minimal+precise] hover: 미세한 opacity 또는 underline만 + 정확한 border/outline 변화
- [minimal+precise] motion: 80-120ms, 거의 즉각적 + 120-180ms, 군더더기 없는 전환
- [minimal+precise] color: monochrome 기반, accent 최소화 + 정확한 semantic 분리, 모호한 중간 톤 지양
- [금지] (editorial) hover: 텍스트 underline 또는 color shift, 장식적 효과 없음 — 이것을 피할 것
- [금지] (editorial) motion: 콘텐츠 전환 위주, UI chrome 모션 최소화 — 이것을 피할 것

### Visual Adaptation Hints

- **cta_prominence**: CTA prominence는 restrained이다. 데이터 작업 흐름을 가리지 않도록 primary만 선명하게 두고 나머지는 text/ghost로 낮춘다. (source=cards; confidence=0.29; provenance=inferred; direction=flat card planes를 기본으로 하고, 압축된 spacing과 얇은 divider 중심의 hierarchy. 중간 반경으로 제품 UI 절제 유지.; evidence=surface=flat, density=dense, corner=medium, layout=data-review-surface)

### 레퍼런스 근거

- **Carbon Design System**: These components can toggle between the AI variant and the default variant depending on the user’s interaction. If the user manually overrides the ...
- **Primer**: I get so much joy from writing HTML and CSS, and design systems are one level up - systematically making UIs accessible and consistent. I love conc...

### 구현 노트

- 기존에 같은 역할의 컴포넌트가 있으면 토큰 교체부터 시작
- variant prop으로 시각적 변형을 관리 (하드코딩 금지)
- size prop: sm / md / lg (터치 영역은 항상 최소 44px 보장)
- 모든 버튼은 `max-inline-size: 100%`와 `min-inline-size: 0`을 기본 보호값으로 갖고, 긴 라벨은 모바일에서 wrap 또는 action-group stack으로 처리
- fixed `width`/`min-width` px 값으로 CTA 폭을 고정하지 않음 — 필요하면 container query 또는 <=480px stack fallback을 함께 정의
- 반응형 검증: 320px, 360px, 390px, 430px에서 control overflow와 viewport horizontal scroll이 없어야 함
- action row는 narrow viewport에서 `flex-wrap: wrap` 또는 세로 stack으로 전환하고, overflow-x 숨김으로 문제를 덮지 않음

---

## data-display / kanban-board

**역할**: 칸반 보드 레이아웃

**탐지 출처**: kanban and board

### 구조 (Anatomy)

- container
- header
- content-area
- footer(optional)
- action(optional)

### 상태 (States)

| 상태 | 설명 |
|------|------|
| `default` | 기본 상태 |
| `loading` | 로딩 중 (스피너 표시) |
| `empty` | 데이터 없음 |
| `error` | 유효성 검증 실패 |

### 토큰 바인딩

```
surface: var(--color-surface)
border: var(--color-border)
radius: var(--radius-md)
padding: var(--space-16) var(--space-20)
heading-font: var(--font-heading) / var(--text-md) / semibold
body-font: var(--font-body) / var(--text-sm) / regular
text: var(--color-text)
text-muted: var(--color-text-muted)
```

### 접근성

- 적절한 heading level 사용
- 데이터 테이블은 scope와 caption 필수
- 빈 상태에서 안내 텍스트 제공

### 브랜드 적용

- [minimal+precise] density: compact 가능, 불필요한 여백 제거 + 엄격한 spacing scale 준수, 임의 값 금지
- [minimal+precise] color: monochrome 기반, accent 최소화 + 정확한 semantic 분리, 모호한 중간 톤 지양
- [금지] (editorial) hover: 텍스트 underline 또는 color shift, 장식적 효과 없음 — 이것을 피할 것
- [금지] (editorial) motion: 콘텐츠 전환 위주, UI chrome 모션 최소화 — 이것을 피할 것

### Visual Adaptation Hints

- **card_elevation_tendency**: 카드는 거의 무그림자 평면으로 유지하고 tint/divider로 계층을 만든다. 압축된 spacing에서도 header/body/footer 구획은 divider나 tint로 유지한다. (source=cards; confidence=0.29; provenance=inferred; direction=flat card planes를 기본으로 하고, 압축된 spacing과 얇은 divider 중심의 hierarchy. 중간 반경으로 제품 UI 절제 유지.; evidence=surface=flat, density=dense, corner=medium)
- **border_vs_fill_emphasis**: fill 중심이다. neutral surface를 기본으로 하고 border는 상태 변화나 구획 보조에만 쓴다. (source=cards; confidence=0.29; provenance=inferred; direction=flat card planes를 기본으로 하고, 압축된 spacing과 얇은 divider 중심의 hierarchy. 중간 반경으로 제품 UI 절제 유지.; evidence=surface=flat, density=dense, corner=medium)
- **chart_panel_framing**: 차트 패널은 flush surface와 thin divider 중심으로 프레이밍한다. 헤더의 metric, controls, plot 영역을 분리하고 내부 여백은 촘촘하게 관리한다. (source=data_display; confidence=0.29; provenance=inferred; direction=정보 밀도를 유지하되 thin dividers와 restrained accent로 hierarchy를 만든다.; evidence=layout=dashboard-grid, density=dense, layout=data-review-surface, surface=flat)

### 구현 노트

- 기존에 같은 역할의 컴포넌트가 있으면 토큰 교체부터 시작
- variant prop으로 시각적 변형을 관리 (하드코딩 금지)
- 빈 상태(empty-state)와 에러 상태를 반드시 처리
- 좁은 UI 텍스트는 Pretendard 기준 label line-height 1.4-1.5를 참고해 뭉침을 방지

---

## data-display / kanban-column

**역할**: 칸반 컬럼 (상태별)

**탐지 출처**: kanban and board

### 구조 (Anatomy)

- container
- header
- content-area
- footer(optional)
- action(optional)

### 상태 (States)

| 상태 | 설명 |
|------|------|
| `default` | 기본 상태 |
| `loading` | 로딩 중 (스피너 표시) |
| `empty` | 데이터 없음 |
| `error` | 유효성 검증 실패 |

### 토큰 바인딩

```
surface: var(--color-surface)
border: var(--color-border)
radius: var(--radius-md)
padding: var(--space-16) var(--space-20)
heading-font: var(--font-heading) / var(--text-md) / semibold
body-font: var(--font-body) / var(--text-sm) / regular
text: var(--color-text)
text-muted: var(--color-text-muted)
```

### 접근성

- 적절한 heading level 사용
- 데이터 테이블은 scope와 caption 필수
- 빈 상태에서 안내 텍스트 제공

### 브랜드 적용

- [minimal+precise] density: compact 가능, 불필요한 여백 제거 + 엄격한 spacing scale 준수, 임의 값 금지
- [minimal+precise] color: monochrome 기반, accent 최소화 + 정확한 semantic 분리, 모호한 중간 톤 지양
- [금지] (editorial) hover: 텍스트 underline 또는 color shift, 장식적 효과 없음 — 이것을 피할 것
- [금지] (editorial) motion: 콘텐츠 전환 위주, UI chrome 모션 최소화 — 이것을 피할 것

### Visual Adaptation Hints

- **card_elevation_tendency**: 카드는 거의 무그림자 평면으로 유지하고 tint/divider로 계층을 만든다. 압축된 spacing에서도 header/body/footer 구획은 divider나 tint로 유지한다. (source=cards; confidence=0.29; provenance=inferred; direction=flat card planes를 기본으로 하고, 압축된 spacing과 얇은 divider 중심의 hierarchy. 중간 반경으로 제품 UI 절제 유지.; evidence=surface=flat, density=dense, corner=medium)
- **border_vs_fill_emphasis**: fill 중심이다. neutral surface를 기본으로 하고 border는 상태 변화나 구획 보조에만 쓴다. (source=cards; confidence=0.29; provenance=inferred; direction=flat card planes를 기본으로 하고, 압축된 spacing과 얇은 divider 중심의 hierarchy. 중간 반경으로 제품 UI 절제 유지.; evidence=surface=flat, density=dense, corner=medium)
- **chart_panel_framing**: 차트 패널은 flush surface와 thin divider 중심으로 프레이밍한다. 헤더의 metric, controls, plot 영역을 분리하고 내부 여백은 촘촘하게 관리한다. (source=data_display; confidence=0.29; provenance=inferred; direction=정보 밀도를 유지하되 thin dividers와 restrained accent로 hierarchy를 만든다.; evidence=layout=dashboard-grid, density=dense, layout=data-review-surface, surface=flat)

### 구현 노트

- 기존에 같은 역할의 컴포넌트가 있으면 토큰 교체부터 시작
- variant prop으로 시각적 변형을 관리 (하드코딩 금지)
- 빈 상태(empty-state)와 에러 상태를 반드시 처리
- 좁은 UI 텍스트는 Pretendard 기준 label line-height 1.4-1.5를 참고해 뭉침을 방지

---

## data-display / kanban-card

**역할**: 드래그 가능한 작업 카드

**탐지 출처**: kanban and board

**Slot archetype**: `surface-card`

### 구조 (Anatomy)

- container
- inner-content

### 상태 (States)

| 상태 | 설명 |
|------|------|
| `default` | 기본 상태 |
| `hover` | 마우스 오버 시 |
| `focus-visible` | focus-visible |

### 토큰 바인딩

```
surface: var(--color-surface)
border: var(--color-border)
border-hover: var(--color-border-strong)
radius: var(--radius-lg)
padding: var(--space-32)
gap: var(--space-16)
motion: border-color var(--duration-180) var(--ease-standard)
```

### 접근성

- 카드 자체가 링크/버튼이면 <a>/<button> 래퍼 사용
- 장식적 카드는 단순 <article> 또는 <div>

### 브랜드 적용

- [minimal+precise] density: compact 가능, 불필요한 여백 제거 + 엄격한 spacing scale 준수, 임의 값 금지
- [minimal+precise] color: monochrome 기반, accent 최소화 + 정확한 semantic 분리, 모호한 중간 톤 지양
- [금지] (editorial) hover: 텍스트 underline 또는 color shift, 장식적 효과 없음 — 이것을 피할 것
- [금지] (editorial) motion: 콘텐츠 전환 위주, UI chrome 모션 최소화 — 이것을 피할 것

### Visual Adaptation Hints

- **card_elevation_tendency**: 카드는 거의 무그림자 평면으로 유지하고 tint/divider로 계층을 만든다. 압축된 spacing에서도 header/body/footer 구획은 divider나 tint로 유지한다. (source=cards; confidence=0.29; provenance=inferred; direction=flat card planes를 기본으로 하고, 압축된 spacing과 얇은 divider 중심의 hierarchy. 중간 반경으로 제품 UI 절제 유지.; evidence=surface=flat, density=dense, corner=medium)
- **border_vs_fill_emphasis**: fill 중심이다. neutral surface를 기본으로 하고 border는 상태 변화나 구획 보조에만 쓴다. (source=cards; confidence=0.29; provenance=inferred; direction=flat card planes를 기본으로 하고, 압축된 spacing과 얇은 divider 중심의 hierarchy. 중간 반경으로 제품 UI 절제 유지.; evidence=surface=flat, density=dense, corner=medium)
- **chart_panel_framing**: 차트 패널은 flush surface와 thin divider 중심으로 프레이밍한다. 헤더의 metric, controls, plot 영역을 분리하고 내부 여백은 촘촘하게 관리한다. (source=data_display; confidence=0.29; provenance=inferred; direction=정보 밀도를 유지하되 thin dividers와 restrained accent로 hierarchy를 만든다.; evidence=layout=dashboard-grid, density=dense, layout=data-review-surface, surface=flat)

### 구현 노트

- 기존에 같은 역할의 컴포넌트가 있으면 토큰 교체부터 시작
- variant prop으로 시각적 변형을 관리 (하드코딩 금지)
- 빈 상태(empty-state)와 에러 상태를 반드시 처리
- 좁은 UI 텍스트는 Pretendard 기준 label line-height 1.4-1.5를 참고해 뭉침을 방지

---

## navigation / app-shell

**역할**: 전체 앱 레이아웃과 네비게이션 컨테이너

**탐지 출처**: workspace navigation

### 구조 (Anatomy)

- container
- nav-item
- icon(optional)
- label
- indicator(active)
- badge(optional)

### 상태 (States)

| 상태 | 설명 |
|------|------|
| `default` | 기본 상태 |
| `hover` | 마우스 오버 시 |
| `active` | 클릭/탭 중 |
| `collapsed` | 접힌 상태 |

### 토큰 바인딩

```
surface: var(--color-surface)
text: var(--color-text-muted)
text-active: var(--color-text)
indicator: var(--color-brand-accent)
padding: var(--space-8) var(--space-16)
font: var(--font-body) / var(--text-sm) / medium
```

### 접근성

- nav landmark (role="navigation")
- aria-current="page" for active item
- 키보드 화살표 탐색 지원

### 브랜드 적용

- [minimal+precise] hover: 미세한 opacity 또는 underline만 + 정확한 border/outline 변화
- [minimal+precise] density: compact 가능, 불필요한 여백 제거 + 엄격한 spacing scale 준수, 임의 값 금지
- [minimal+precise] motion: 80-120ms, 거의 즉각적 + 120-180ms, 군더더기 없는 전환
- [금지] (editorial) hover: 텍스트 underline 또는 color shift, 장식적 효과 없음 — 이것을 피할 것
- [금지] (editorial) motion: 콘텐츠 전환 위주, UI chrome 모션 최소화 — 이것을 피할 것

### Visual Adaptation Hints

- **filter_nav_density**: filter/nav density는 compact하다. chip, scope, pagination을 촘촘하게 묶되 의미 단위별 group은 분리한다. (source=navigation; confidence=0.23; provenance=inferred; direction=고정 sidebar 또는 split-pane navigation을 우선하고, 현재 위치와 scope를 항상 명시한다.; evidence=Split-pane workspace, layout=data-review-surface, density=dense)

### 레퍼런스 근거

- **Carbon Design System**: Library menu navigation There are two kinds of symbols — library symbols and document symbols. Library symbols are available in any Sketch document...
- **Primer**: Octicon nav items navigation 12 px

### 구현 노트

- 기존에 같은 역할의 컴포넌트가 있으면 토큰 교체부터 시작
- variant prop으로 시각적 변형을 관리 (하드코딩 금지)
- active 상태는 URL/라우터와 자동 동기화
- 좁은 UI 텍스트는 Pretendard 기준 label line-height 1.4-1.5를 참고해 뭉침을 방지
- 반응형 검증: 320px, 360px, 390px, 430px에서 control overflow와 viewport horizontal scroll이 없어야 함
- action row는 narrow viewport에서 `flex-wrap: wrap` 또는 세로 stack으로 전환하고, overflow-x 숨김으로 문제를 덮지 않음

---

## navigation / sidebar-nav

**역할**: 주요 섹션 간 이동을 위한 사이드 네비게이션

**탐지 출처**: workspace navigation

### 구조 (Anatomy)

- container
- nav-item
- icon(optional)
- label
- indicator(active)
- badge(optional)

### 상태 (States)

| 상태 | 설명 |
|------|------|
| `default` | 기본 상태 |
| `hover` | 마우스 오버 시 |
| `active` | 클릭/탭 중 |
| `collapsed` | 접힌 상태 |

### 토큰 바인딩

```
surface: var(--color-surface)
text: var(--color-text-muted)
text-active: var(--color-text)
indicator: var(--color-brand-accent)
padding: var(--space-8) var(--space-16)
font: var(--font-body) / var(--text-sm) / medium
```

### 접근성

- nav landmark (role="navigation")
- aria-current="page" for active item
- 키보드 화살표 탐색 지원

### 브랜드 적용

- [minimal+precise] hover: 미세한 opacity 또는 underline만 + 정확한 border/outline 변화
- [minimal+precise] density: compact 가능, 불필요한 여백 제거 + 엄격한 spacing scale 준수, 임의 값 금지
- [minimal+precise] motion: 80-120ms, 거의 즉각적 + 120-180ms, 군더더기 없는 전환
- [금지] (editorial) hover: 텍스트 underline 또는 color shift, 장식적 효과 없음 — 이것을 피할 것
- [금지] (editorial) motion: 콘텐츠 전환 위주, UI chrome 모션 최소화 — 이것을 피할 것

### Visual Adaptation Hints

- **filter_nav_density**: filter/nav density는 compact하다. chip, scope, pagination을 촘촘하게 묶되 의미 단위별 group은 분리한다. (source=navigation; confidence=0.23; provenance=inferred; direction=고정 sidebar 또는 split-pane navigation을 우선하고, 현재 위치와 scope를 항상 명시한다.; evidence=Split-pane workspace, layout=data-review-surface, density=dense)

### 레퍼런스 근거

- **Carbon Design System**: Total panel width (“sidebar nav”) + Left outside margin + Right outside margin = Total margins Artboard width - Total margins = Total width
- **Primer**: Octicon nav items navigation 12 px

### 구현 노트

- 기존에 같은 역할의 컴포넌트가 있으면 토큰 교체부터 시작
- variant prop으로 시각적 변형을 관리 (하드코딩 금지)
- active 상태는 URL/라우터와 자동 동기화
- 좁은 UI 텍스트는 Pretendard 기준 label line-height 1.4-1.5를 참고해 뭉침을 방지
- 반응형 검증: 320px, 360px, 390px, 430px에서 control overflow와 viewport horizontal scroll이 없어야 함
- action row는 narrow viewport에서 `flex-wrap: wrap` 또는 세로 stack으로 전환하고, overflow-x 숨김으로 문제를 덮지 않음

---

## navigation / topbar

**역할**: 앱 상단 바 (로고, 검색, 사용자 메뉴)

**탐지 출처**: workspace navigation

### 구조 (Anatomy)

- container
- nav-item
- icon(optional)
- label
- indicator(active)
- badge(optional)

### 상태 (States)

| 상태 | 설명 |
|------|------|
| `default` | 기본 상태 |
| `hover` | 마우스 오버 시 |
| `active` | 클릭/탭 중 |
| `collapsed` | 접힌 상태 |

### 토큰 바인딩

```
surface: var(--color-surface)
text: var(--color-text-muted)
text-active: var(--color-text)
indicator: var(--color-brand-accent)
padding: var(--space-8) var(--space-16)
font: var(--font-body) / var(--text-sm) / medium
```

### 접근성

- nav landmark (role="navigation")
- aria-current="page" for active item
- 키보드 화살표 탐색 지원

### 브랜드 적용

- [minimal+precise] hover: 미세한 opacity 또는 underline만 + 정확한 border/outline 변화
- [minimal+precise] density: compact 가능, 불필요한 여백 제거 + 엄격한 spacing scale 준수, 임의 값 금지
- [minimal+precise] motion: 80-120ms, 거의 즉각적 + 120-180ms, 군더더기 없는 전환
- [금지] (editorial) hover: 텍스트 underline 또는 color shift, 장식적 효과 없음 — 이것을 피할 것
- [금지] (editorial) motion: 콘텐츠 전환 위주, UI chrome 모션 최소화 — 이것을 피할 것

### Visual Adaptation Hints

- **filter_nav_density**: filter/nav density는 compact하다. chip, scope, pagination을 촘촘하게 묶되 의미 단위별 group은 분리한다. (source=navigation; confidence=0.23; provenance=inferred; direction=고정 sidebar 또는 split-pane navigation을 우선하고, 현재 위치와 scope를 항상 명시한다.; evidence=Split-pane workspace, layout=data-review-surface, density=dense)

### 레퍼런스 근거

- **Carbon Design System**: Library menu navigation There are two kinds of symbols — library symbols and document symbols. Library symbols are available in any Sketch document...
- **Primer**: Octicon nav items navigation 12 px

### 구현 노트

- 기존에 같은 역할의 컴포넌트가 있으면 토큰 교체부터 시작
- variant prop으로 시각적 변형을 관리 (하드코딩 금지)
- active 상태는 URL/라우터와 자동 동기화
- 좁은 UI 텍스트는 Pretendard 기준 label line-height 1.4-1.5를 참고해 뭉침을 방지
- 반응형 검증: 320px, 360px, 390px, 430px에서 control overflow와 viewport horizontal scroll이 없어야 함
- action row는 narrow viewport에서 `flex-wrap: wrap` 또는 세로 stack으로 전환하고, overflow-x 숨김으로 문제를 덮지 않음

---

## navigation / breadcrumb

**역할**: 현재 위치를 계층적으로 표시

**탐지 출처**: workspace navigation

### 구조 (Anatomy)

- container
- nav-item
- icon(optional)
- label
- indicator(active)
- badge(optional)

### 상태 (States)

| 상태 | 설명 |
|------|------|
| `default` | 기본 상태 |
| `hover` | 마우스 오버 시 |
| `active` | 클릭/탭 중 |
| `collapsed` | 접힌 상태 |

### 토큰 바인딩

```
surface: var(--color-surface)
text: var(--color-text-muted)
text-active: var(--color-text)
indicator: var(--color-brand-accent)
padding: var(--space-8) var(--space-16)
font: var(--font-body) / var(--text-sm) / medium
```

### 접근성

- nav landmark (role="navigation")
- aria-current="page" for active item
- 키보드 화살표 탐색 지원

### 브랜드 적용

- [minimal+precise] hover: 미세한 opacity 또는 underline만 + 정확한 border/outline 변화
- [minimal+precise] density: compact 가능, 불필요한 여백 제거 + 엄격한 spacing scale 준수, 임의 값 금지
- [minimal+precise] motion: 80-120ms, 거의 즉각적 + 120-180ms, 군더더기 없는 전환
- [금지] (editorial) hover: 텍스트 underline 또는 color shift, 장식적 효과 없음 — 이것을 피할 것
- [금지] (editorial) motion: 콘텐츠 전환 위주, UI chrome 모션 최소화 — 이것을 피할 것

### Visual Adaptation Hints

- **filter_nav_density**: filter/nav density는 compact하다. chip, scope, pagination을 촘촘하게 묶되 의미 단위별 group은 분리한다. (source=navigation; confidence=0.23; provenance=inferred; direction=고정 sidebar 또는 split-pane navigation을 우선하고, 현재 위치와 scope를 항상 명시한다.; evidence=Split-pane workspace, layout=data-review-surface, density=dense)

### 레퍼런스 근거

- **Carbon Design System**: Library menu navigation There are two kinds of symbols — library symbols and document symbols. Library symbols are available in any Sketch document...
- **Primer**: Octicon nav items navigation 12 px

### 구현 노트

- 기존에 같은 역할의 컴포넌트가 있으면 토큰 교체부터 시작
- variant prop으로 시각적 변형을 관리 (하드코딩 금지)
- active 상태는 URL/라우터와 자동 동기화
- 좁은 UI 텍스트는 Pretendard 기준 label line-height 1.4-1.5를 참고해 뭉침을 방지
- 반응형 검증: 320px, 360px, 390px, 430px에서 control overflow와 viewport horizontal scroll이 없어야 함
- action row는 narrow viewport에서 `flex-wrap: wrap` 또는 세로 stack으로 전환하고, overflow-x 숨김으로 문제를 덮지 않음

---

## navigation / tab-bar

**역할**: 섹션 내 하위 탭 전환

**탐지 출처**: workspace navigation

### 구조 (Anatomy)

- container
- nav-item
- icon(optional)
- label
- indicator(active)
- badge(optional)

### 상태 (States)

| 상태 | 설명 |
|------|------|
| `default` | 기본 상태 |
| `hover` | 마우스 오버 시 |
| `active` | 클릭/탭 중 |
| `collapsed` | 접힌 상태 |

### 토큰 바인딩

```
surface: var(--color-surface)
text: var(--color-text-muted)
text-active: var(--color-text)
indicator: var(--color-brand-accent)
padding: var(--space-8) var(--space-16)
font: var(--font-body) / var(--text-sm) / medium
```

### 접근성

- nav landmark (role="navigation")
- aria-current="page" for active item
- 키보드 화살표 탐색 지원

### 브랜드 적용

- [minimal+precise] hover: 미세한 opacity 또는 underline만 + 정확한 border/outline 변화
- [minimal+precise] density: compact 가능, 불필요한 여백 제거 + 엄격한 spacing scale 준수, 임의 값 금지
- [minimal+precise] motion: 80-120ms, 거의 즉각적 + 120-180ms, 군더더기 없는 전환
- [금지] (editorial) hover: 텍스트 underline 또는 color shift, 장식적 효과 없음 — 이것을 피할 것
- [금지] (editorial) motion: 콘텐츠 전환 위주, UI chrome 모션 최소화 — 이것을 피할 것

### Visual Adaptation Hints

- **filter_nav_density**: filter/nav density는 compact하다. chip, scope, pagination을 촘촘하게 묶되 의미 단위별 group은 분리한다. (source=navigation; confidence=0.23; provenance=inferred; direction=고정 sidebar 또는 split-pane navigation을 우선하고, 현재 위치와 scope를 항상 명시한다.; evidence=Split-pane workspace, layout=data-review-surface, density=dense)

### 레퍼런스 근거

- **Carbon Design System**: Library menu navigation There are two kinds of symbols — library symbols and document symbols. Library symbols are available in any Sketch document...
- **Primer**: Octicon nav items navigation 12 px

### 구현 노트

- 기존에 같은 역할의 컴포넌트가 있으면 토큰 교체부터 시작
- variant prop으로 시각적 변형을 관리 (하드코딩 금지)
- active 상태는 URL/라우터와 자동 동기화
- 좁은 UI 텍스트는 Pretendard 기준 label line-height 1.4-1.5를 참고해 뭉침을 방지
- 반응형 검증: 320px, 360px, 390px, 430px에서 control overflow와 viewport horizontal scroll이 없어야 함
- action row는 narrow viewport에서 `flex-wrap: wrap` 또는 세로 stack으로 전환하고, overflow-x 숨김으로 문제를 덮지 않음

---

## feedback / toast

**역할**: 일시적 성공/에러 알림

**탐지 출처**: notifications

### 구조 (Anatomy)

- container
- icon
- message
- action(optional)
- close-button(optional)

### 상태 (States)

| 상태 | 설명 |
|------|------|
| `info` | 정보 알림 |
| `success` | 성공 알림 |
| `warning` | 경고 알림 |
| `danger` | 에러/위험 알림 |

### 토큰 바인딩

```
surface: var(--color-surface-muted)
text: var(--color-text)
icon: var(--color-info)
border: var(--color-border)
radius: var(--radius-sm)
padding: var(--space-12) var(--space-16)
severity-info: var(--color-info)
severity-success: var(--color-success)
severity-warning: var(--color-warning)
severity-danger: var(--color-danger)
```

### 접근성

- role="alert" for urgent messages
- role="status" for non-urgent
- aria-live="polite" or "assertive"
- 닫기 버튼에 aria-label 필수

### 브랜드 적용

- [minimal+precise] feedback: 아이콘+텍스트 조합, 색상 배경 최소화 + 명확한 상태 구분, 진행률/결과를 수치로 표시
- [minimal+precise] motion: 80-120ms, 거의 즉각적 + 120-180ms, 군더더기 없는 전환
- [minimal+precise] color: monochrome 기반, accent 최소화 + 정확한 semantic 분리, 모호한 중간 톤 지양
- [금지] (editorial) hover: 텍스트 underline 또는 color shift, 장식적 효과 없음 — 이것을 피할 것
- [금지] (editorial) motion: 콘텐츠 전환 위주, UI chrome 모션 최소화 — 이것을 피할 것

### 레퍼런스 근거

- **Carbon Design System**: We welcome all feedback, designs, or ideas in order to produce the best possible experience for our users. If you're interested in contributing, ch...
- **Primer**: Messaging components are used to provide important and relevant information to the user, including feedback, contextual information, product update...

### 구현 노트

- 기존에 같은 역할의 컴포넌트가 있으면 토큰 교체부터 시작
- variant prop으로 시각적 변형을 관리 (하드코딩 금지)
- auto-dismiss 시간은 내용 길이에 비례 (기본 5초)
- 반응형 검증: 320px, 360px, 390px, 430px에서 control overflow와 viewport horizontal scroll이 없어야 함
- action row는 narrow viewport에서 `flex-wrap: wrap` 또는 세로 stack으로 전환하고, overflow-x 숨김으로 문제를 덮지 않음

---

## feedback / inline-alert

**역할**: 페이지 내 알림 배너

**탐지 출처**: notifications

### 구조 (Anatomy)

- container
- icon
- message
- action(optional)
- close-button(optional)

### 상태 (States)

| 상태 | 설명 |
|------|------|
| `info` | 정보 알림 |
| `success` | 성공 알림 |
| `warning` | 경고 알림 |
| `danger` | 에러/위험 알림 |

### 토큰 바인딩

```
surface: var(--color-surface-muted)
text: var(--color-text)
icon: var(--color-info)
border: var(--color-border)
radius: var(--radius-sm)
padding: var(--space-12) var(--space-16)
severity-info: var(--color-info)
severity-success: var(--color-success)
severity-warning: var(--color-warning)
severity-danger: var(--color-danger)
```

### 접근성

- role="alert" for urgent messages
- role="status" for non-urgent
- aria-live="polite" or "assertive"
- 닫기 버튼에 aria-label 필수

### 브랜드 적용

- [minimal+precise] feedback: 아이콘+텍스트 조합, 색상 배경 최소화 + 명확한 상태 구분, 진행률/결과를 수치로 표시
- [minimal+precise] motion: 80-120ms, 거의 즉각적 + 120-180ms, 군더더기 없는 전환
- [minimal+precise] color: monochrome 기반, accent 최소화 + 정확한 semantic 분리, 모호한 중간 톤 지양
- [금지] (editorial) hover: 텍스트 underline 또는 color shift, 장식적 효과 없음 — 이것을 피할 것
- [금지] (editorial) motion: 콘텐츠 전환 위주, UI chrome 모션 최소화 — 이것을 피할 것

### 레퍼런스 근거

- **Carbon Design System**: We welcome all feedback, designs, or ideas in order to produce the best possible experience for our users. If you're interested in contributing, ch...
- **Primer**: Messaging components are used to provide important and relevant information to the user, including feedback, contextual information, product update...

### 구현 노트

- 기존에 같은 역할의 컴포넌트가 있으면 토큰 교체부터 시작
- variant prop으로 시각적 변형을 관리 (하드코딩 금지)
- auto-dismiss 시간은 내용 길이에 비례 (기본 5초)
- 반응형 검증: 320px, 360px, 390px, 430px에서 control overflow와 viewport horizontal scroll이 없어야 함
- action row는 narrow viewport에서 `flex-wrap: wrap` 또는 세로 stack으로 전환하고, overflow-x 숨김으로 문제를 덮지 않음

---

## feedback / empty-state

**역할**: 데이터가 없을 때 안내 화면

**탐지 출처**: notifications

### 구조 (Anatomy)

- container
- icon
- message
- action(optional)
- close-button(optional)

### 상태 (States)

| 상태 | 설명 |
|------|------|
| `info` | 정보 알림 |
| `success` | 성공 알림 |
| `warning` | 경고 알림 |
| `danger` | 에러/위험 알림 |

### 토큰 바인딩

```
surface: var(--color-surface-muted)
text: var(--color-text)
icon: var(--color-info)
border: var(--color-border)
radius: var(--radius-sm)
padding: var(--space-12) var(--space-16)
severity-info: var(--color-info)
severity-success: var(--color-success)
severity-warning: var(--color-warning)
severity-danger: var(--color-danger)
```

### 접근성

- role="alert" for urgent messages
- role="status" for non-urgent
- aria-live="polite" or "assertive"
- 닫기 버튼에 aria-label 필수

### 브랜드 적용

- [minimal+precise] feedback: 아이콘+텍스트 조합, 색상 배경 최소화 + 명확한 상태 구분, 진행률/결과를 수치로 표시
- [minimal+precise] motion: 80-120ms, 거의 즉각적 + 120-180ms, 군더더기 없는 전환
- [minimal+precise] color: monochrome 기반, accent 최소화 + 정확한 semantic 분리, 모호한 중간 톤 지양
- [금지] (editorial) hover: 텍스트 underline 또는 color shift, 장식적 효과 없음 — 이것을 피할 것
- [금지] (editorial) motion: 콘텐츠 전환 위주, UI chrome 모션 최소화 — 이것을 피할 것

### Visual Adaptation Hints

- **card_elevation_tendency**: 카드는 거의 무그림자 평면으로 유지하고 tint/divider로 계층을 만든다. 압축된 spacing에서도 header/body/footer 구획은 divider나 tint로 유지한다. (source=cards; confidence=0.29; provenance=inferred; direction=flat card planes를 기본으로 하고, 압축된 spacing과 얇은 divider 중심의 hierarchy. 중간 반경으로 제품 UI 절제 유지.; evidence=surface=flat, density=dense, corner=medium)
- **border_vs_fill_emphasis**: fill 중심이다. neutral surface를 기본으로 하고 border는 상태 변화나 구획 보조에만 쓴다. (source=cards; confidence=0.29; provenance=inferred; direction=flat card planes를 기본으로 하고, 압축된 spacing과 얇은 divider 중심의 hierarchy. 중간 반경으로 제품 UI 절제 유지.; evidence=surface=flat, density=dense, corner=medium)
- **chart_panel_framing**: 차트 패널은 flush surface와 thin divider 중심으로 프레이밍한다. 헤더의 metric, controls, plot 영역을 분리하고 내부 여백은 촘촘하게 관리한다. (source=data_display; confidence=0.29; provenance=inferred; direction=정보 밀도를 유지하되 thin dividers와 restrained accent로 hierarchy를 만든다.; evidence=layout=dashboard-grid, density=dense, layout=data-review-surface, surface=flat)

### 레퍼런스 근거

- **Carbon Design System**: We welcome all feedback, designs, or ideas in order to produce the best possible experience for our users. If you're interested in contributing, ch...
- **Primer**: Empty states Empty states are used to fill spaces when no content has been added yet, or is temporarily empty due to the nature of the feature.

### 구현 노트

- 기존에 같은 역할의 컴포넌트가 있으면 토큰 교체부터 시작
- variant prop으로 시각적 변형을 관리 (하드코딩 금지)
- auto-dismiss 시간은 내용 길이에 비례 (기본 5초)
- 반응형 검증: 320px, 360px, 390px, 430px에서 control overflow와 viewport horizontal scroll이 없어야 함
- action row는 narrow viewport에서 `flex-wrap: wrap` 또는 세로 stack으로 전환하고, overflow-x 숨김으로 문제를 덮지 않음

---

## feedback / banner

**역할**: 전체 화면 상단 공지 배너

**탐지 출처**: notifications

### 구조 (Anatomy)

- container
- icon
- message
- action(optional)
- close-button(optional)

### 상태 (States)

| 상태 | 설명 |
|------|------|
| `info` | 정보 알림 |
| `success` | 성공 알림 |
| `warning` | 경고 알림 |
| `danger` | 에러/위험 알림 |

### 토큰 바인딩

```
surface: var(--color-surface-muted)
text: var(--color-text)
icon: var(--color-info)
border: var(--color-border)
radius: var(--radius-sm)
padding: var(--space-12) var(--space-16)
severity-info: var(--color-info)
severity-success: var(--color-success)
severity-warning: var(--color-warning)
severity-danger: var(--color-danger)
```

### 접근성

- role="alert" for urgent messages
- role="status" for non-urgent
- aria-live="polite" or "assertive"
- 닫기 버튼에 aria-label 필수

### 브랜드 적용

- [minimal+precise] feedback: 아이콘+텍스트 조합, 색상 배경 최소화 + 명확한 상태 구분, 진행률/결과를 수치로 표시
- [minimal+precise] motion: 80-120ms, 거의 즉각적 + 120-180ms, 군더더기 없는 전환
- [minimal+precise] color: monochrome 기반, accent 최소화 + 정확한 semantic 분리, 모호한 중간 톤 지양
- [금지] (editorial) hover: 텍스트 underline 또는 color shift, 장식적 효과 없음 — 이것을 피할 것
- [금지] (editorial) motion: 콘텐츠 전환 위주, UI chrome 모션 최소화 — 이것을 피할 것

### Visual Adaptation Hints

- **card_elevation_tendency**: 카드는 거의 무그림자 평면으로 유지하고 tint/divider로 계층을 만든다. 압축된 spacing에서도 header/body/footer 구획은 divider나 tint로 유지한다. (source=cards; confidence=0.29; provenance=inferred; direction=flat card planes를 기본으로 하고, 압축된 spacing과 얇은 divider 중심의 hierarchy. 중간 반경으로 제품 UI 절제 유지.; evidence=surface=flat, density=dense, corner=medium)
- **border_vs_fill_emphasis**: fill 중심이다. neutral surface를 기본으로 하고 border는 상태 변화나 구획 보조에만 쓴다. (source=cards; confidence=0.29; provenance=inferred; direction=flat card planes를 기본으로 하고, 압축된 spacing과 얇은 divider 중심의 hierarchy. 중간 반경으로 제품 UI 절제 유지.; evidence=surface=flat, density=dense, corner=medium)

### 레퍼런스 근거

- **Carbon Design System**: We welcome all feedback, designs, or ideas in order to produce the best possible experience for our users. If you're interested in contributing, ch...
- **Primer**: Banner Banner is used to highlight important information.

### 구현 노트

- 기존에 같은 역할의 컴포넌트가 있으면 토큰 교체부터 시작
- variant prop으로 시각적 변형을 관리 (하드코딩 금지)
- auto-dismiss 시간은 내용 길이에 비례 (기본 5초)
- 반응형 검증: 320px, 360px, 390px, 430px에서 control overflow와 viewport horizontal scroll이 없어야 함
- action row는 narrow viewport에서 `flex-wrap: wrap` 또는 세로 stack으로 전환하고, overflow-x 숨김으로 문제를 덮지 않음

---

## data-display / metric-strip

**역할**: 핵심 지표를 한 줄 스캔 표면으로 압축하는 요약 스트립

**탐지 출처**: operational overview

### 구조 (Anatomy)

- container
- header
- content-area
- footer(optional)
- action(optional)

### 상태 (States)

| 상태 | 설명 |
|------|------|
| `default` | 기본 상태 |
| `loading` | 로딩 중 (스피너 표시) |
| `empty` | 데이터 없음 |
| `error` | 유효성 검증 실패 |

### 토큰 바인딩

```
surface: var(--color-surface)
border: var(--color-border)
radius: var(--radius-md)
padding: var(--space-16) var(--space-20)
heading-font: var(--font-heading) / var(--text-md) / semibold
body-font: var(--font-body) / var(--text-sm) / regular
text: var(--color-text)
text-muted: var(--color-text-muted)
```

### 접근성

- 적절한 heading level 사용
- 데이터 테이블은 scope와 caption 필수
- 빈 상태에서 안내 텍스트 제공

### 브랜드 적용

- [minimal+precise] density: compact 가능, 불필요한 여백 제거 + 엄격한 spacing scale 준수, 임의 값 금지
- [minimal+precise] color: monochrome 기반, accent 최소화 + 정확한 semantic 분리, 모호한 중간 톤 지양
- [금지] (editorial) hover: 텍스트 underline 또는 color shift, 장식적 효과 없음 — 이것을 피할 것
- [금지] (editorial) motion: 콘텐츠 전환 위주, UI chrome 모션 최소화 — 이것을 피할 것

### Visual Adaptation Hints

- **operational_surface_role**: 주 작업 표면은 card wall이 아니라 table/list/rail/canvas 계열로 설계한다. 압축된 표면에서는 row height, column rhythm, sticky toolbar, source/update label을 우선한다. (source=data_display; confidence=0.29; provenance=inferred; direction=정보 밀도를 유지하되 thin dividers와 restrained accent로 hierarchy를 만든다.; evidence=layout=dashboard-grid, density=dense, layout=data-review-surface)
- **chart_panel_framing**: 차트 패널은 flush surface와 thin divider 중심으로 프레이밍한다. 헤더의 metric, controls, plot 영역을 분리하고 내부 여백은 촘촘하게 관리한다. (source=data_display; confidence=0.29; provenance=inferred; direction=정보 밀도를 유지하되 thin dividers와 restrained accent로 hierarchy를 만든다.; evidence=layout=dashboard-grid, density=dense, layout=data-review-surface, surface=flat)

### 구현 노트

- 기존에 같은 역할의 컴포넌트가 있으면 토큰 교체부터 시작
- variant prop으로 시각적 변형을 관리 (하드코딩 금지)
- 빈 상태(empty-state)와 에러 상태를 반드시 처리
- 좁은 UI 텍스트는 Pretendard 기준 label line-height 1.4-1.5를 참고해 뭉침을 방지

---

## data-display / status-summary-row

**역할**: 상태, 변경량, 담당자, 업데이트 시각을 행 단위로 보여주는 운영 요약

**탐지 출처**: operational overview

### 구조 (Anatomy)

- container
- header
- content-area
- footer(optional)
- action(optional)

### 상태 (States)

| 상태 | 설명 |
|------|------|
| `default` | 기본 상태 |
| `loading` | 로딩 중 (스피너 표시) |
| `empty` | 데이터 없음 |
| `error` | 유효성 검증 실패 |

### 토큰 바인딩

```
surface: var(--color-surface)
border: var(--color-border)
radius: var(--radius-md)
padding: var(--space-16) var(--space-20)
heading-font: var(--font-heading) / var(--text-md) / semibold
body-font: var(--font-body) / var(--text-sm) / regular
text: var(--color-text)
text-muted: var(--color-text-muted)
```

### 접근성

- 적절한 heading level 사용
- 데이터 테이블은 scope와 caption 필수
- 빈 상태에서 안내 텍스트 제공

### 브랜드 적용

- [minimal+precise] density: compact 가능, 불필요한 여백 제거 + 엄격한 spacing scale 준수, 임의 값 금지
- [minimal+precise] color: monochrome 기반, accent 최소화 + 정확한 semantic 분리, 모호한 중간 톤 지양
- [금지] (editorial) hover: 텍스트 underline 또는 color shift, 장식적 효과 없음 — 이것을 피할 것
- [금지] (editorial) motion: 콘텐츠 전환 위주, UI chrome 모션 최소화 — 이것을 피할 것

### Visual Adaptation Hints

- **operational_surface_role**: 주 작업 표면은 card wall이 아니라 table/list/rail/canvas 계열로 설계한다. 압축된 표면에서는 row height, column rhythm, sticky toolbar, source/update label을 우선한다. (source=data_display; confidence=0.29; provenance=inferred; direction=정보 밀도를 유지하되 thin dividers와 restrained accent로 hierarchy를 만든다.; evidence=layout=dashboard-grid, density=dense, layout=data-review-surface)
- **chart_panel_framing**: 차트 패널은 flush surface와 thin divider 중심으로 프레이밍한다. 헤더의 metric, controls, plot 영역을 분리하고 내부 여백은 촘촘하게 관리한다. (source=data_display; confidence=0.29; provenance=inferred; direction=정보 밀도를 유지하되 thin dividers와 restrained accent로 hierarchy를 만든다.; evidence=layout=dashboard-grid, density=dense, layout=data-review-surface, surface=flat)

### 구현 노트

- 기존에 같은 역할의 컴포넌트가 있으면 토큰 교체부터 시작
- variant prop으로 시각적 변형을 관리 (하드코딩 금지)
- 빈 상태(empty-state)와 에러 상태를 반드시 처리
- 좁은 UI 텍스트는 Pretendard 기준 label line-height 1.4-1.5를 참고해 뭉침을 방지

---

## data-display / task-surface-header

**역할**: 현재 업무 범위, 필터, 주요 액션을 묶는 작업 표면 헤더

**탐지 출처**: operational overview

### 구조 (Anatomy)

- container
- header
- content-area
- footer(optional)
- action(optional)

### 상태 (States)

| 상태 | 설명 |
|------|------|
| `default` | 기본 상태 |
| `loading` | 로딩 중 (스피너 표시) |
| `empty` | 데이터 없음 |
| `error` | 유효성 검증 실패 |

### 토큰 바인딩

```
surface: var(--color-surface)
border: var(--color-border)
radius: var(--radius-md)
padding: var(--space-16) var(--space-20)
heading-font: var(--font-heading) / var(--text-md) / semibold
body-font: var(--font-body) / var(--text-sm) / regular
text: var(--color-text)
text-muted: var(--color-text-muted)
```

### 접근성

- 적절한 heading level 사용
- 데이터 테이블은 scope와 caption 필수
- 빈 상태에서 안내 텍스트 제공

### 브랜드 적용

- [minimal+precise] density: compact 가능, 불필요한 여백 제거 + 엄격한 spacing scale 준수, 임의 값 금지
- [minimal+precise] color: monochrome 기반, accent 최소화 + 정확한 semantic 분리, 모호한 중간 톤 지양
- [금지] (editorial) hover: 텍스트 underline 또는 color shift, 장식적 효과 없음 — 이것을 피할 것
- [금지] (editorial) motion: 콘텐츠 전환 위주, UI chrome 모션 최소화 — 이것을 피할 것

### Visual Adaptation Hints

- **card_elevation_tendency**: 카드는 거의 무그림자 평면으로 유지하고 tint/divider로 계층을 만든다. 압축된 spacing에서도 header/body/footer 구획은 divider나 tint로 유지한다. (source=cards; confidence=0.29; provenance=inferred; direction=flat card planes를 기본으로 하고, 압축된 spacing과 얇은 divider 중심의 hierarchy. 중간 반경으로 제품 UI 절제 유지.; evidence=surface=flat, density=dense, corner=medium)
- **border_vs_fill_emphasis**: fill 중심이다. neutral surface를 기본으로 하고 border는 상태 변화나 구획 보조에만 쓴다. (source=cards; confidence=0.29; provenance=inferred; direction=flat card planes를 기본으로 하고, 압축된 spacing과 얇은 divider 중심의 hierarchy. 중간 반경으로 제품 UI 절제 유지.; evidence=surface=flat, density=dense, corner=medium)
- **chart_panel_framing**: 차트 패널은 flush surface와 thin divider 중심으로 프레이밍한다. 헤더의 metric, controls, plot 영역을 분리하고 내부 여백은 촘촘하게 관리한다. (source=data_display; confidence=0.29; provenance=inferred; direction=정보 밀도를 유지하되 thin dividers와 restrained accent로 hierarchy를 만든다.; evidence=layout=dashboard-grid, density=dense, layout=data-review-surface, surface=flat)

### 구현 노트

- 기존에 같은 역할의 컴포넌트가 있으면 토큰 교체부터 시작
- variant prop으로 시각적 변형을 관리 (하드코딩 금지)
- 빈 상태(empty-state)와 에러 상태를 반드시 처리
- 좁은 UI 텍스트는 Pretendard 기준 label line-height 1.4-1.5를 참고해 뭉침을 방지

---

## data-display / source-ledger

**역할**: 수치와 판단의 출처, 업데이트 시각, 샘플 여부를 기록하는 출처 레저

**탐지 출처**: operational overview

### 구조 (Anatomy)

- container
- header
- content-area
- footer(optional)
- action(optional)

### 상태 (States)

| 상태 | 설명 |
|------|------|
| `default` | 기본 상태 |
| `loading` | 로딩 중 (스피너 표시) |
| `empty` | 데이터 없음 |
| `error` | 유효성 검증 실패 |

### 토큰 바인딩

```
surface: var(--color-surface)
border: var(--color-border)
radius: var(--radius-md)
padding: var(--space-16) var(--space-20)
heading-font: var(--font-heading) / var(--text-md) / semibold
body-font: var(--font-body) / var(--text-sm) / regular
text: var(--color-text)
text-muted: var(--color-text-muted)
```

### 접근성

- 적절한 heading level 사용
- 데이터 테이블은 scope와 caption 필수
- 빈 상태에서 안내 텍스트 제공

### 브랜드 적용

- [minimal+precise] density: compact 가능, 불필요한 여백 제거 + 엄격한 spacing scale 준수, 임의 값 금지
- [minimal+precise] color: monochrome 기반, accent 최소화 + 정확한 semantic 분리, 모호한 중간 톤 지양
- [금지] (editorial) hover: 텍스트 underline 또는 color shift, 장식적 효과 없음 — 이것을 피할 것
- [금지] (editorial) motion: 콘텐츠 전환 위주, UI chrome 모션 최소화 — 이것을 피할 것

### Visual Adaptation Hints

- **operational_surface_role**: 주 작업 표면은 card wall이 아니라 table/list/rail/canvas 계열로 설계한다. 압축된 표면에서는 row height, column rhythm, sticky toolbar, source/update label을 우선한다. (source=data_display; confidence=0.29; provenance=inferred; direction=정보 밀도를 유지하되 thin dividers와 restrained accent로 hierarchy를 만든다.; evidence=layout=dashboard-grid, density=dense, layout=data-review-surface)
- **chart_panel_framing**: 차트 패널은 flush surface와 thin divider 중심으로 프레이밍한다. 헤더의 metric, controls, plot 영역을 분리하고 내부 여백은 촘촘하게 관리한다. (source=data_display; confidence=0.29; provenance=inferred; direction=정보 밀도를 유지하되 thin dividers와 restrained accent로 hierarchy를 만든다.; evidence=layout=dashboard-grid, density=dense, layout=data-review-surface, surface=flat)

### 구현 노트

- 기존에 같은 역할의 컴포넌트가 있으면 토큰 교체부터 시작
- variant prop으로 시각적 변형을 관리 (하드코딩 금지)
- 빈 상태(empty-state)와 에러 상태를 반드시 처리
- 좁은 UI 텍스트는 Pretendard 기준 label line-height 1.4-1.5를 참고해 뭉침을 방지

---

## navigation / operational-rail

**역할**: 보조 상태와 다음 작업을 압축해 보여주는 측면 또는 상단 레일

**탐지 출처**: operational overview

### 구조 (Anatomy)

- container
- nav-item
- icon(optional)
- label
- indicator(active)
- badge(optional)

### 상태 (States)

| 상태 | 설명 |
|------|------|
| `default` | 기본 상태 |
| `hover` | 마우스 오버 시 |
| `active` | 클릭/탭 중 |
| `collapsed` | 접힌 상태 |

### 토큰 바인딩

```
surface: var(--color-surface)
text: var(--color-text-muted)
text-active: var(--color-text)
indicator: var(--color-brand-accent)
padding: var(--space-8) var(--space-16)
font: var(--font-body) / var(--text-sm) / medium
```

### 접근성

- nav landmark (role="navigation")
- aria-current="page" for active item
- 키보드 화살표 탐색 지원

### 브랜드 적용

- [minimal+precise] hover: 미세한 opacity 또는 underline만 + 정확한 border/outline 변화
- [minimal+precise] density: compact 가능, 불필요한 여백 제거 + 엄격한 spacing scale 준수, 임의 값 금지
- [minimal+precise] motion: 80-120ms, 거의 즉각적 + 120-180ms, 군더더기 없는 전환
- [금지] (editorial) hover: 텍스트 underline 또는 color shift, 장식적 효과 없음 — 이것을 피할 것
- [금지] (editorial) motion: 콘텐츠 전환 위주, UI chrome 모션 최소화 — 이것을 피할 것

### Visual Adaptation Hints

- **operational_surface_role**: 주 작업 표면은 card wall이 아니라 table/list/rail/canvas 계열로 설계한다. 압축된 표면에서는 row height, column rhythm, sticky toolbar, source/update label을 우선한다. (source=data_display; confidence=0.29; provenance=inferred; direction=정보 밀도를 유지하되 thin dividers와 restrained accent로 hierarchy를 만든다.; evidence=layout=dashboard-grid, density=dense, layout=data-review-surface)
- **filter_nav_density**: filter/nav density는 compact하다. chip, scope, pagination을 촘촘하게 묶되 의미 단위별 group은 분리한다. (source=navigation; confidence=0.23; provenance=inferred; direction=고정 sidebar 또는 split-pane navigation을 우선하고, 현재 위치와 scope를 항상 명시한다.; evidence=Split-pane workspace, layout=data-review-surface, density=dense)

### 레퍼런스 근거

- **Carbon Design System**: Library menu navigation There are two kinds of symbols — library symbols and document symbols. Library symbols are available in any Sketch document...
- **Primer**: Octicon nav items navigation 12 px

### 구현 노트

- 기존에 같은 역할의 컴포넌트가 있으면 토큰 교체부터 시작
- variant prop으로 시각적 변형을 관리 (하드코딩 금지)
- active 상태는 URL/라우터와 자동 동기화
- 좁은 UI 텍스트는 Pretendard 기준 label line-height 1.4-1.5를 참고해 뭉침을 방지
- 반응형 검증: 320px, 360px, 390px, 430px에서 control overflow와 viewport horizontal scroll이 없어야 함
- action row는 narrow viewport에서 `flex-wrap: wrap` 또는 세로 stack으로 전환하고, overflow-x 숨김으로 문제를 덮지 않음

---

## data-display / section-header

**역할**: 운영 표면의 구획과 정렬 맥락을 표시하는 헤더

**탐지 출처**: operational overview

### 구조 (Anatomy)

- container
- header
- content-area
- footer(optional)
- action(optional)

### 상태 (States)

| 상태 | 설명 |
|------|------|
| `default` | 기본 상태 |
| `loading` | 로딩 중 (스피너 표시) |
| `empty` | 데이터 없음 |
| `error` | 유효성 검증 실패 |

### 토큰 바인딩

```
surface: var(--color-surface)
border: var(--color-border)
radius: var(--radius-md)
padding: var(--space-16) var(--space-20)
heading-font: var(--font-heading) / var(--text-md) / semibold
body-font: var(--font-body) / var(--text-sm) / regular
text: var(--color-text)
text-muted: var(--color-text-muted)
```

### 접근성

- 적절한 heading level 사용
- 데이터 테이블은 scope와 caption 필수
- 빈 상태에서 안내 텍스트 제공

### 브랜드 적용

- [minimal+precise] density: compact 가능, 불필요한 여백 제거 + 엄격한 spacing scale 준수, 임의 값 금지
- [minimal+precise] color: monochrome 기반, accent 최소화 + 정확한 semantic 분리, 모호한 중간 톤 지양
- [금지] (editorial) hover: 텍스트 underline 또는 color shift, 장식적 효과 없음 — 이것을 피할 것
- [금지] (editorial) motion: 콘텐츠 전환 위주, UI chrome 모션 최소화 — 이것을 피할 것

### Visual Adaptation Hints

- **card_elevation_tendency**: 카드는 거의 무그림자 평면으로 유지하고 tint/divider로 계층을 만든다. 압축된 spacing에서도 header/body/footer 구획은 divider나 tint로 유지한다. (source=cards; confidence=0.29; provenance=inferred; direction=flat card planes를 기본으로 하고, 압축된 spacing과 얇은 divider 중심의 hierarchy. 중간 반경으로 제품 UI 절제 유지.; evidence=surface=flat, density=dense, corner=medium)
- **border_vs_fill_emphasis**: fill 중심이다. neutral surface를 기본으로 하고 border는 상태 변화나 구획 보조에만 쓴다. (source=cards; confidence=0.29; provenance=inferred; direction=flat card planes를 기본으로 하고, 압축된 spacing과 얇은 divider 중심의 hierarchy. 중간 반경으로 제품 UI 절제 유지.; evidence=surface=flat, density=dense, corner=medium)
- **chart_panel_framing**: 차트 패널은 flush surface와 thin divider 중심으로 프레이밍한다. 헤더의 metric, controls, plot 영역을 분리하고 내부 여백은 촘촘하게 관리한다. (source=data_display; confidence=0.29; provenance=inferred; direction=정보 밀도를 유지하되 thin dividers와 restrained accent로 hierarchy를 만든다.; evidence=layout=dashboard-grid, density=dense, layout=data-review-surface, surface=flat)

### 구현 노트

- 기존에 같은 역할의 컴포넌트가 있으면 토큰 교체부터 시작
- variant prop으로 시각적 변형을 관리 (하드코딩 금지)
- 빈 상태(empty-state)와 에러 상태를 반드시 처리
- 좁은 UI 텍스트는 Pretendard 기준 label line-height 1.4-1.5를 참고해 뭉침을 방지

---

## data-display / tag

**역할**: 분류/라벨 태그

**탐지 출처**: tags and labels

### 구조 (Anatomy)

- container
- header
- content-area
- footer(optional)
- action(optional)

### 상태 (States)

| 상태 | 설명 |
|------|------|
| `default` | 기본 상태 |
| `loading` | 로딩 중 (스피너 표시) |
| `empty` | 데이터 없음 |
| `error` | 유효성 검증 실패 |

### 토큰 바인딩

```
surface: var(--color-surface)
border: var(--color-border)
radius: var(--radius-md)
padding: var(--space-16) var(--space-20)
heading-font: var(--font-heading) / var(--text-md) / semibold
body-font: var(--font-body) / var(--text-sm) / regular
text: var(--color-text)
text-muted: var(--color-text-muted)
```

### 접근성

- 적절한 heading level 사용
- 데이터 테이블은 scope와 caption 필수
- 빈 상태에서 안내 텍스트 제공

### 브랜드 적용

- [minimal+precise] density: compact 가능, 불필요한 여백 제거 + 엄격한 spacing scale 준수, 임의 값 금지
- [minimal+precise] color: monochrome 기반, accent 최소화 + 정확한 semantic 분리, 모호한 중간 톤 지양
- [금지] (editorial) hover: 텍스트 underline 또는 color shift, 장식적 효과 없음 — 이것을 피할 것
- [금지] (editorial) motion: 콘텐츠 전환 위주, UI chrome 모션 최소화 — 이것을 피할 것

### Visual Adaptation Hints

- **card_elevation_tendency**: 카드는 거의 무그림자 평면으로 유지하고 tint/divider로 계층을 만든다. 압축된 spacing에서도 header/body/footer 구획은 divider나 tint로 유지한다. (source=cards; confidence=0.29; provenance=inferred; direction=flat card planes를 기본으로 하고, 압축된 spacing과 얇은 divider 중심의 hierarchy. 중간 반경으로 제품 UI 절제 유지.; evidence=surface=flat, density=dense, corner=medium)
- **border_vs_fill_emphasis**: fill 중심이다. neutral surface를 기본으로 하고 border는 상태 변화나 구획 보조에만 쓴다. (source=cards; confidence=0.29; provenance=inferred; direction=flat card planes를 기본으로 하고, 압축된 spacing과 얇은 divider 중심의 hierarchy. 중간 반경으로 제품 UI 절제 유지.; evidence=surface=flat, density=dense, corner=medium)
- **chart_panel_framing**: 차트 패널은 flush surface와 thin divider 중심으로 프레이밍한다. 헤더의 metric, controls, plot 영역을 분리하고 내부 여백은 촘촘하게 관리한다. (source=data_display; confidence=0.29; provenance=inferred; direction=정보 밀도를 유지하되 thin dividers와 restrained accent로 hierarchy를 만든다.; evidence=layout=dashboard-grid, density=dense, layout=data-review-surface, surface=flat)

### 레퍼런스 근거

- **Carbon Design System**: Tag Date picker
- **Primer**: Primer color design tokens are made available within data-attribute selectors on the body tag or other high level dom element. There are three dist...

### 구현 노트

- 기존에 같은 역할의 컴포넌트가 있으면 토큰 교체부터 시작
- variant prop으로 시각적 변형을 관리 (하드코딩 금지)
- 빈 상태(empty-state)와 에러 상태를 반드시 처리
- 좁은 UI 텍스트는 Pretendard 기준 label line-height 1.4-1.5를 참고해 뭉침을 방지

---

## feedback / status-badge

**역할**: 상태를 색상으로 표시하는 뱃지

**탐지 출처**: tags and labels

### 구조 (Anatomy)

- container
- icon
- message
- action(optional)
- close-button(optional)

### 상태 (States)

| 상태 | 설명 |
|------|------|
| `info` | 정보 알림 |
| `success` | 성공 알림 |
| `warning` | 경고 알림 |
| `danger` | 에러/위험 알림 |

### 토큰 바인딩

```
surface: var(--color-surface-muted)
text: var(--color-text)
icon: var(--color-info)
border: var(--color-border)
radius: var(--radius-sm)
padding: var(--space-12) var(--space-16)
severity-info: var(--color-info)
severity-success: var(--color-success)
severity-warning: var(--color-warning)
severity-danger: var(--color-danger)
```

### 접근성

- role="alert" for urgent messages
- role="status" for non-urgent
- aria-live="polite" or "assertive"
- 닫기 버튼에 aria-label 필수

### 브랜드 적용

- [minimal+precise] feedback: 아이콘+텍스트 조합, 색상 배경 최소화 + 명확한 상태 구분, 진행률/결과를 수치로 표시
- [minimal+precise] motion: 80-120ms, 거의 즉각적 + 120-180ms, 군더더기 없는 전환
- [minimal+precise] color: monochrome 기반, accent 최소화 + 정확한 semantic 분리, 모호한 중간 톤 지양
- [금지] (editorial) hover: 텍스트 underline 또는 color shift, 장식적 효과 없음 — 이것을 피할 것
- [금지] (editorial) motion: 콘텐츠 전환 위주, UI chrome 모션 최소화 — 이것을 피할 것

### Visual Adaptation Hints

- **card_elevation_tendency**: 카드는 거의 무그림자 평면으로 유지하고 tint/divider로 계층을 만든다. 압축된 spacing에서도 header/body/footer 구획은 divider나 tint로 유지한다. (source=cards; confidence=0.29; provenance=inferred; direction=flat card planes를 기본으로 하고, 압축된 spacing과 얇은 divider 중심의 hierarchy. 중간 반경으로 제품 UI 절제 유지.; evidence=surface=flat, density=dense, corner=medium)
- **border_vs_fill_emphasis**: fill 중심이다. neutral surface를 기본으로 하고 border는 상태 변화나 구획 보조에만 쓴다. (source=cards; confidence=0.29; provenance=inferred; direction=flat card planes를 기본으로 하고, 압축된 spacing과 얇은 divider 중심의 hierarchy. 중간 반경으로 제품 UI 절제 유지.; evidence=surface=flat, density=dense, corner=medium)
- **chart_panel_framing**: 차트 패널은 flush surface와 thin divider 중심으로 프레이밍한다. 헤더의 metric, controls, plot 영역을 분리하고 내부 여백은 촘촘하게 관리한다. (source=data_display; confidence=0.29; provenance=inferred; direction=정보 밀도를 유지하되 thin dividers와 restrained accent로 hierarchy를 만든다.; evidence=layout=dashboard-grid, density=dense, layout=data-review-surface, surface=flat)

### 레퍼런스 근거

- **Carbon Design System**: We welcome all feedback, designs, or ideas in order to produce the best possible experience for our users. If you're interested in contributing, ch...
- **Primer**: Messaging components are used to provide important and relevant information to the user, including feedback, contextual information, product update...

### 구현 노트

- 기존에 같은 역할의 컴포넌트가 있으면 토큰 교체부터 시작
- variant prop으로 시각적 변형을 관리 (하드코딩 금지)
- auto-dismiss 시간은 내용 길이에 비례 (기본 5초)
- 반응형 검증: 320px, 360px, 390px, 430px에서 control overflow와 viewport horizontal scroll이 없어야 함
- action row는 narrow viewport에서 `flex-wrap: wrap` 또는 세로 stack으로 전환하고, overflow-x 숨김으로 문제를 덮지 않음

---

## input / chip

**역할**: 선택/해제 가능한 칩

**탐지 출처**: tags and labels

### 구조 (Anatomy)

- container
- label
- input-area
- helper-text(optional)
- leading-icon(optional)
- clear-button(optional)

### 상태 (States)

| 상태 | 설명 |
|------|------|
| `default` | 기본 상태 |
| `focus` | 키보드 포커스 시 |
| `filled` | 값이 입력된 상태 |
| `error` | 유효성 검증 실패 |
| `disabled` | 비활성 (상호작용 불가) |
| `readonly` | 읽기 전용 |

### 토큰 바인딩

```
surface: var(--color-surface)
text: var(--color-text)
placeholder: var(--color-text-subtle)
border: var(--color-border)
border-focus: var(--color-brand-primary)
border-error: var(--color-danger)
radius: var(--radius-sm)
padding: var(--space-8) var(--space-12)
font: var(--font-body) / var(--text-md) / regular
```

### 접근성

- label과 input을 for/id로 연결
- aria-describedby로 helper/error text 연결
- aria-invalid="true" when error
- aria-required="true" when required

### 브랜드 적용

- [minimal+precise] hover: 미세한 opacity 또는 underline만 + 정확한 border/outline 변화
- [minimal+precise] density: compact 가능, 불필요한 여백 제거 + 엄격한 spacing scale 준수, 임의 값 금지
- [minimal+precise] feedback: 아이콘+텍스트 조합, 색상 배경 최소화 + 명확한 상태 구분, 진행률/결과를 수치로 표시
- [금지] (editorial) hover: 텍스트 underline 또는 color shift, 장식적 효과 없음 — 이것을 피할 것
- [금지] (editorial) motion: 콘텐츠 전환 위주, UI chrome 모션 최소화 — 이것을 피할 것

### Visual Adaptation Hints

- **filter_nav_density**: filter/nav density는 compact하다. chip, scope, pagination을 촘촘하게 묶되 의미 단위별 group은 분리한다. (source=navigation; confidence=0.23; provenance=inferred; direction=고정 sidebar 또는 split-pane navigation을 우선하고, 현재 위치와 scope를 항상 명시한다.; evidence=Split-pane workspace, layout=data-review-surface, density=dense)

### 레퍼런스 근거

- **Carbon Design System**: Number input Text input
- **Primer**: I worked in data visualization and map-making for most of my career, and solving design problems with data is my jam. To me there's something uniqu...

### 구현 노트

- 기존에 같은 역할의 컴포넌트가 있으면 토큰 교체부터 시작
- variant prop으로 시각적 변형을 관리 (하드코딩 금지)
- error 상태에서 helper text → error message로 자동 전환
- label은 항상 visible (placeholder만으로 대체 금지)
- 반응형 검증: 320px, 360px, 390px, 430px에서 control overflow와 viewport horizontal scroll이 없어야 함
- action row는 narrow viewport에서 `flex-wrap: wrap` 또는 세로 stack으로 전환하고, overflow-x 숨김으로 문제를 덮지 않음

---

## overlay / dialog

**역할**: 확인/입력을 받는 표준 다이얼로그

**탐지 출처**: modal and dialog

### 구조 (Anatomy)

- backdrop
- container
- header
- content
- footer(optional)
- close-button

### 상태 (States)

| 상태 | 설명 |
|------|------|
| `closed` | 닫힌 상태 |
| `opening` | 열리는 중 (전환 애니메이션) |
| `open` | 열린 상태 |
| `closing` | 닫히는 중 |

### 토큰 바인딩

```
surface: var(--color-surface-elevated)
backdrop: rgb(0 0 0 / 0.5)
radius: var(--radius-lg)
padding: var(--space-24)
border: var(--color-border)
motion: opacity var(--duration-180) var(--ease-standard)
```

### 접근성

- role="dialog" with aria-modal="true"
- focus trap (Tab 순환)
- Escape로 닫기
- aria-labelledby로 제목 연결
- 닫은 후 trigger 요소로 포커스 복귀

### 브랜드 적용

- [minimal+precise] motion: 80-120ms, 거의 즉각적 + 120-180ms, 군더더기 없는 전환
- [minimal+precise] density: compact 가능, 불필요한 여백 제거 + 엄격한 spacing scale 준수, 임의 값 금지
- [금지] (editorial) hover: 텍스트 underline 또는 color shift, 장식적 효과 없음 — 이것을 피할 것
- [금지] (editorial) motion: 콘텐츠 전환 위주, UI chrome 모션 최소화 — 이것을 피할 것

### 레퍼런스 근거

- **Primer**: ConfirmationDialog ConfirmationDialog is a specialized dialog component used to confirm user actions. It provides a simple way to ask users to conf...

### 구현 노트

- 기존에 같은 역할의 컴포넌트가 있으면 토큰 교체부터 시작
- variant prop으로 시각적 변형을 관리 (하드코딩 금지)
- Escape / backdrop click으로 닫기, 열 때 첫 focusable 요소로 이동

---

## overlay / popover

**역할**: 트리거에 붙는 짧은 보조 입력/정보 표면

**탐지 출처**: modal and dialog

### 구조 (Anatomy)

- backdrop
- container
- header
- content
- footer(optional)
- close-button

### 상태 (States)

| 상태 | 설명 |
|------|------|
| `closed` | 닫힌 상태 |
| `opening` | 열리는 중 (전환 애니메이션) |
| `open` | 열린 상태 |
| `closing` | 닫히는 중 |

### 토큰 바인딩

```
surface: var(--color-surface-elevated)
backdrop: rgb(0 0 0 / 0.5)
radius: var(--radius-lg)
padding: var(--space-24)
border: var(--color-border)
motion: opacity var(--duration-180) var(--ease-standard)
```

### 접근성

- role="dialog" with aria-modal="true"
- focus trap (Tab 순환)
- Escape로 닫기
- aria-labelledby로 제목 연결
- 닫은 후 trigger 요소로 포커스 복귀

### 브랜드 적용

- [minimal+precise] motion: 80-120ms, 거의 즉각적 + 120-180ms, 군더더기 없는 전환
- [minimal+precise] density: compact 가능, 불필요한 여백 제거 + 엄격한 spacing scale 준수, 임의 값 금지
- [금지] (editorial) hover: 텍스트 underline 또는 color shift, 장식적 효과 없음 — 이것을 피할 것
- [금지] (editorial) motion: 콘텐츠 전환 위주, UI chrome 모션 최소화 — 이것을 피할 것

### 레퍼런스 근거

- **Carbon Design System**: The AI label is also the trigger for the explainability popover which serves as the first layer of explainability. It provides a consistent, up-fro...
- **Primer**: Popover Popover is used to bring attention to specific user interface elements.

### 구현 노트

- 기존에 같은 역할의 컴포넌트가 있으면 토큰 교체부터 시작
- variant prop으로 시각적 변형을 관리 (하드코딩 금지)
- Escape / backdrop click으로 닫기, 열 때 첫 focusable 요소로 이동

---

## overlay / confirm-dialog

**역할**: 삭제/위험 작업 확인 다이얼로그

**탐지 출처**: modal and dialog

### 구조 (Anatomy)

- backdrop
- container
- header
- content
- footer(optional)
- close-button

### 상태 (States)

| 상태 | 설명 |
|------|------|
| `closed` | 닫힌 상태 |
| `opening` | 열리는 중 (전환 애니메이션) |
| `open` | 열린 상태 |
| `closing` | 닫히는 중 |

### 토큰 바인딩

```
surface: var(--color-surface-elevated)
backdrop: rgb(0 0 0 / 0.5)
radius: var(--radius-lg)
padding: var(--space-24)
border: var(--color-border)
motion: opacity var(--duration-180) var(--ease-standard)
```

### 접근성

- role="dialog" with aria-modal="true"
- focus trap (Tab 순환)
- Escape로 닫기
- aria-labelledby로 제목 연결
- 닫은 후 trigger 요소로 포커스 복귀

### 브랜드 적용

- [minimal+precise] motion: 80-120ms, 거의 즉각적 + 120-180ms, 군더더기 없는 전환
- [minimal+precise] density: compact 가능, 불필요한 여백 제거 + 엄격한 spacing scale 준수, 임의 값 금지
- [금지] (editorial) hover: 텍스트 underline 또는 color shift, 장식적 효과 없음 — 이것을 피할 것
- [금지] (editorial) motion: 콘텐츠 전환 위주, UI chrome 모션 최소화 — 이것을 피할 것

### 레퍼런스 근거

- **Primer**: ActionMenu is composed of ActionList and Overlay patterns used for quick actions and selections. AnchoredOverlay

### 구현 노트

- 기존에 같은 역할의 컴포넌트가 있으면 토큰 교체부터 시작
- variant prop으로 시각적 변형을 관리 (하드코딩 금지)
- Escape / backdrop click으로 닫기, 열 때 첫 focusable 요소로 이동

---

## feedback / step-progress

**역할**: 단계별 진행 표시

**탐지 출처**: onboarding and stepper

### 구조 (Anatomy)

- container
- icon
- message
- action(optional)
- close-button(optional)

### 상태 (States)

| 상태 | 설명 |
|------|------|
| `info` | 정보 알림 |
| `success` | 성공 알림 |
| `warning` | 경고 알림 |
| `danger` | 에러/위험 알림 |

### 토큰 바인딩

```
surface: var(--color-surface-muted)
text: var(--color-text)
icon: var(--color-info)
border: var(--color-border)
radius: var(--radius-sm)
padding: var(--space-12) var(--space-16)
severity-info: var(--color-info)
severity-success: var(--color-success)
severity-warning: var(--color-warning)
severity-danger: var(--color-danger)
```

### 접근성

- role="alert" for urgent messages
- role="status" for non-urgent
- aria-live="polite" or "assertive"
- 닫기 버튼에 aria-label 필수

### 브랜드 적용

- [minimal+precise] feedback: 아이콘+텍스트 조합, 색상 배경 최소화 + 명확한 상태 구분, 진행률/결과를 수치로 표시
- [minimal+precise] motion: 80-120ms, 거의 즉각적 + 120-180ms, 군더더기 없는 전환
- [minimal+precise] color: monochrome 기반, accent 최소화 + 정확한 semantic 분리, 모호한 중간 톤 지양
- [금지] (editorial) hover: 텍스트 underline 또는 color shift, 장식적 효과 없음 — 이것을 피할 것
- [금지] (editorial) motion: 콘텐츠 전환 위주, UI chrome 모션 최소화 — 이것을 피할 것

### 레퍼런스 근거

- **Carbon Design System**: We welcome all feedback, designs, or ideas in order to produce the best possible experience for our users. If you're interested in contributing, ch...
- **Primer**: Messaging components are used to provide important and relevant information to the user, including feedback, contextual information, product update...

### 구현 노트

- 기존에 같은 역할의 컴포넌트가 있으면 토큰 교체부터 시작
- variant prop으로 시각적 변형을 관리 (하드코딩 금지)
- auto-dismiss 시간은 내용 길이에 비례 (기본 5초)
- 반응형 검증: 320px, 360px, 390px, 430px에서 control overflow와 viewport horizontal scroll이 없어야 함
- action row는 narrow viewport에서 `flex-wrap: wrap` 또는 세로 stack으로 전환하고, overflow-x 숨김으로 문제를 덮지 않음

---

## navigation / wizard-layout

**역할**: 위저드 레이아웃 (이전/다음)

**탐지 출처**: onboarding and stepper

### 구조 (Anatomy)

- container
- nav-item
- icon(optional)
- label
- indicator(active)
- badge(optional)

### 상태 (States)

| 상태 | 설명 |
|------|------|
| `default` | 기본 상태 |
| `hover` | 마우스 오버 시 |
| `active` | 클릭/탭 중 |
| `collapsed` | 접힌 상태 |

### 토큰 바인딩

```
surface: var(--color-surface)
text: var(--color-text-muted)
text-active: var(--color-text)
indicator: var(--color-brand-accent)
padding: var(--space-8) var(--space-16)
font: var(--font-body) / var(--text-sm) / medium
```

### 접근성

- nav landmark (role="navigation")
- aria-current="page" for active item
- 키보드 화살표 탐색 지원

### 브랜드 적용

- [minimal+precise] hover: 미세한 opacity 또는 underline만 + 정확한 border/outline 변화
- [minimal+precise] density: compact 가능, 불필요한 여백 제거 + 엄격한 spacing scale 준수, 임의 값 금지
- [minimal+precise] motion: 80-120ms, 거의 즉각적 + 120-180ms, 군더더기 없는 전환
- [금지] (editorial) hover: 텍스트 underline 또는 color shift, 장식적 효과 없음 — 이것을 피할 것
- [금지] (editorial) motion: 콘텐츠 전환 위주, UI chrome 모션 최소화 — 이것을 피할 것

### Visual Adaptation Hints

- **filter_nav_density**: filter/nav density는 compact하다. chip, scope, pagination을 촘촘하게 묶되 의미 단위별 group은 분리한다. (source=navigation; confidence=0.23; provenance=inferred; direction=고정 sidebar 또는 split-pane navigation을 우선하고, 현재 위치와 scope를 항상 명시한다.; evidence=Split-pane workspace, layout=data-review-surface, density=dense)

### 레퍼런스 근거

- **Carbon Design System**: Library menu navigation There are two kinds of symbols — library symbols and document symbols. Library symbols are available in any Sketch document...
- **Primer**: Octicon nav items navigation 12 px

### 구현 노트

- 기존에 같은 역할의 컴포넌트가 있으면 토큰 교체부터 시작
- variant prop으로 시각적 변형을 관리 (하드코딩 금지)
- active 상태는 URL/라우터와 자동 동기화
- 좁은 UI 텍스트는 Pretendard 기준 label line-height 1.4-1.5를 참고해 뭉침을 방지
- 반응형 검증: 320px, 360px, 390px, 430px에서 control overflow와 viewport horizontal scroll이 없어야 함
- action row는 narrow viewport에서 `flex-wrap: wrap` 또는 세로 stack으로 전환하고, overflow-x 숨김으로 문제를 덮지 않음

---

## overlay / tooltip-guide

**역할**: 기능 안내 툴팁

**탐지 출처**: onboarding and stepper

### 구조 (Anatomy)

- backdrop
- container
- header
- content
- footer(optional)
- close-button

### 상태 (States)

| 상태 | 설명 |
|------|------|
| `closed` | 닫힌 상태 |
| `opening` | 열리는 중 (전환 애니메이션) |
| `open` | 열린 상태 |
| `closing` | 닫히는 중 |

### 토큰 바인딩

```
surface: var(--color-surface-elevated)
backdrop: rgb(0 0 0 / 0.5)
radius: var(--radius-lg)
padding: var(--space-24)
border: var(--color-border)
motion: opacity var(--duration-180) var(--ease-standard)
```

### 접근성

- role="dialog" with aria-modal="true"
- focus trap (Tab 순환)
- Escape로 닫기
- aria-labelledby로 제목 연결
- 닫은 후 trigger 요소로 포커스 복귀

### 브랜드 적용

- [minimal+precise] motion: 80-120ms, 거의 즉각적 + 120-180ms, 군더더기 없는 전환
- [minimal+precise] density: compact 가능, 불필요한 여백 제거 + 엄격한 spacing scale 준수, 임의 값 금지
- [금지] (editorial) hover: 텍스트 underline 또는 color shift, 장식적 효과 없음 — 이것을 피할 것
- [금지] (editorial) motion: 콘텐츠 전환 위주, UI chrome 모션 최소화 — 이것을 피할 것

### 레퍼런스 근거

- **Primer**: ActionMenu is composed of ActionList and Overlay patterns used for quick actions and selections. AnchoredOverlay

### 구현 노트

- 기존에 같은 역할의 컴포넌트가 있으면 토큰 교체부터 시작
- variant prop으로 시각적 변형을 관리 (하드코딩 금지)
- Escape / backdrop click으로 닫기, 열 때 첫 focusable 요소로 이동

---

## data-display / chat-message

**역할**: 채팅 메시지 말풍선

**탐지 출처**: chat and messaging

### 구조 (Anatomy)

- container
- header
- content-area
- footer(optional)
- action(optional)

### 상태 (States)

| 상태 | 설명 |
|------|------|
| `default` | 기본 상태 |
| `loading` | 로딩 중 (스피너 표시) |
| `empty` | 데이터 없음 |
| `error` | 유효성 검증 실패 |

### 토큰 바인딩

```
surface: var(--color-surface)
border: var(--color-border)
radius: var(--radius-md)
padding: var(--space-16) var(--space-20)
heading-font: var(--font-heading) / var(--text-md) / semibold
body-font: var(--font-body) / var(--text-sm) / regular
text: var(--color-text)
text-muted: var(--color-text-muted)
```

### 접근성

- 적절한 heading level 사용
- 데이터 테이블은 scope와 caption 필수
- 빈 상태에서 안내 텍스트 제공

### 브랜드 적용

- [minimal+precise] density: compact 가능, 불필요한 여백 제거 + 엄격한 spacing scale 준수, 임의 값 금지
- [minimal+precise] color: monochrome 기반, accent 최소화 + 정확한 semantic 분리, 모호한 중간 톤 지양
- [금지] (editorial) hover: 텍스트 underline 또는 color shift, 장식적 효과 없음 — 이것을 피할 것
- [금지] (editorial) motion: 콘텐츠 전환 위주, UI chrome 모션 최소화 — 이것을 피할 것

### Visual Adaptation Hints

- **card_elevation_tendency**: 카드는 거의 무그림자 평면으로 유지하고 tint/divider로 계층을 만든다. 압축된 spacing에서도 header/body/footer 구획은 divider나 tint로 유지한다. (source=cards; confidence=0.29; provenance=inferred; direction=flat card planes를 기본으로 하고, 압축된 spacing과 얇은 divider 중심의 hierarchy. 중간 반경으로 제품 UI 절제 유지.; evidence=surface=flat, density=dense, corner=medium)
- **border_vs_fill_emphasis**: fill 중심이다. neutral surface를 기본으로 하고 border는 상태 변화나 구획 보조에만 쓴다. (source=cards; confidence=0.29; provenance=inferred; direction=flat card planes를 기본으로 하고, 압축된 spacing과 얇은 divider 중심의 hierarchy. 중간 반경으로 제품 UI 절제 유지.; evidence=surface=flat, density=dense, corner=medium)
- **chart_panel_framing**: 차트 패널은 flush surface와 thin divider 중심으로 프레이밍한다. 헤더의 metric, controls, plot 영역을 분리하고 내부 여백은 촘촘하게 관리한다. (source=data_display; confidence=0.29; provenance=inferred; direction=정보 밀도를 유지하되 thin dividers와 restrained accent로 hierarchy를 만든다.; evidence=layout=dashboard-grid, density=dense, layout=data-review-surface, surface=flat)

### 구현 노트

- 기존에 같은 역할의 컴포넌트가 있으면 토큰 교체부터 시작
- variant prop으로 시각적 변형을 관리 (하드코딩 금지)
- 빈 상태(empty-state)와 에러 상태를 반드시 처리
- 좁은 UI 텍스트는 Pretendard 기준 label line-height 1.4-1.5를 참고해 뭉침을 방지

---

## input / chat-input

**역할**: 메시지 입력 영역

**탐지 출처**: chat and messaging

### 구조 (Anatomy)

- container
- label
- input-area
- helper-text(optional)
- leading-icon(optional)
- clear-button(optional)

### 상태 (States)

| 상태 | 설명 |
|------|------|
| `default` | 기본 상태 |
| `focus` | 키보드 포커스 시 |
| `filled` | 값이 입력된 상태 |
| `error` | 유효성 검증 실패 |
| `disabled` | 비활성 (상호작용 불가) |
| `readonly` | 읽기 전용 |

### 토큰 바인딩

```
surface: var(--color-surface)
text: var(--color-text)
placeholder: var(--color-text-subtle)
border: var(--color-border)
border-focus: var(--color-brand-primary)
border-error: var(--color-danger)
radius: var(--radius-sm)
padding: var(--space-8) var(--space-12)
font: var(--font-body) / var(--text-md) / regular
```

### 접근성

- label과 input을 for/id로 연결
- aria-describedby로 helper/error text 연결
- aria-invalid="true" when error
- aria-required="true" when required

### 브랜드 적용

- [minimal+precise] hover: 미세한 opacity 또는 underline만 + 정확한 border/outline 변화
- [minimal+precise] density: compact 가능, 불필요한 여백 제거 + 엄격한 spacing scale 준수, 임의 값 금지
- [minimal+precise] feedback: 아이콘+텍스트 조합, 색상 배경 최소화 + 명확한 상태 구분, 진행률/결과를 수치로 표시
- [금지] (editorial) hover: 텍스트 underline 또는 color shift, 장식적 효과 없음 — 이것을 피할 것
- [금지] (editorial) motion: 콘텐츠 전환 위주, UI chrome 모션 최소화 — 이것을 피할 것

### 레퍼런스 근거

- **Carbon Design System**: Number input Text input
- **Primer**: I worked in data visualization and map-making for most of my career, and solving design problems with data is my jam. To me there's something uniqu...

### 구현 노트

- 기존에 같은 역할의 컴포넌트가 있으면 토큰 교체부터 시작
- variant prop으로 시각적 변형을 관리 (하드코딩 금지)
- error 상태에서 helper text → error message로 자동 전환
- label은 항상 visible (placeholder만으로 대체 금지)
- 반응형 검증: 320px, 360px, 390px, 430px에서 control overflow와 viewport horizontal scroll이 없어야 함
- action row는 narrow viewport에서 `flex-wrap: wrap` 또는 세로 stack으로 전환하고, overflow-x 숨김으로 문제를 덮지 않음

---

## data-display / chat-thread

**역할**: 대화 스레드 목록

**탐지 출처**: chat and messaging

### 구조 (Anatomy)

- container
- header
- content-area
- footer(optional)
- action(optional)

### 상태 (States)

| 상태 | 설명 |
|------|------|
| `default` | 기본 상태 |
| `loading` | 로딩 중 (스피너 표시) |
| `empty` | 데이터 없음 |
| `error` | 유효성 검증 실패 |

### 토큰 바인딩

```
surface: var(--color-surface)
border: var(--color-border)
radius: var(--radius-md)
padding: var(--space-16) var(--space-20)
heading-font: var(--font-heading) / var(--text-md) / semibold
body-font: var(--font-body) / var(--text-sm) / regular
text: var(--color-text)
text-muted: var(--color-text-muted)
```

### 접근성

- 적절한 heading level 사용
- 데이터 테이블은 scope와 caption 필수
- 빈 상태에서 안내 텍스트 제공

### 브랜드 적용

- [minimal+precise] density: compact 가능, 불필요한 여백 제거 + 엄격한 spacing scale 준수, 임의 값 금지
- [minimal+precise] color: monochrome 기반, accent 최소화 + 정확한 semantic 분리, 모호한 중간 톤 지양
- [금지] (editorial) hover: 텍스트 underline 또는 color shift, 장식적 효과 없음 — 이것을 피할 것
- [금지] (editorial) motion: 콘텐츠 전환 위주, UI chrome 모션 최소화 — 이것을 피할 것

### Visual Adaptation Hints

- **card_elevation_tendency**: 카드는 거의 무그림자 평면으로 유지하고 tint/divider로 계층을 만든다. 압축된 spacing에서도 header/body/footer 구획은 divider나 tint로 유지한다. (source=cards; confidence=0.29; provenance=inferred; direction=flat card planes를 기본으로 하고, 압축된 spacing과 얇은 divider 중심의 hierarchy. 중간 반경으로 제품 UI 절제 유지.; evidence=surface=flat, density=dense, corner=medium)
- **border_vs_fill_emphasis**: fill 중심이다. neutral surface를 기본으로 하고 border는 상태 변화나 구획 보조에만 쓴다. (source=cards; confidence=0.29; provenance=inferred; direction=flat card planes를 기본으로 하고, 압축된 spacing과 얇은 divider 중심의 hierarchy. 중간 반경으로 제품 UI 절제 유지.; evidence=surface=flat, density=dense, corner=medium)
- **chart_panel_framing**: 차트 패널은 flush surface와 thin divider 중심으로 프레이밍한다. 헤더의 metric, controls, plot 영역을 분리하고 내부 여백은 촘촘하게 관리한다. (source=data_display; confidence=0.29; provenance=inferred; direction=정보 밀도를 유지하되 thin dividers와 restrained accent로 hierarchy를 만든다.; evidence=layout=dashboard-grid, density=dense, layout=data-review-surface, surface=flat)

### 구현 노트

- 기존에 같은 역할의 컴포넌트가 있으면 토큰 교체부터 시작
- variant prop으로 시각적 변형을 관리 (하드코딩 금지)
- 빈 상태(empty-state)와 에러 상태를 반드시 처리
- 좁은 UI 텍스트는 Pretendard 기준 label line-height 1.4-1.5를 참고해 뭉침을 방지

---

## editorial / editor-canvas

**역할**: 텍스트 편집 영역

**탐지 출처**: rich text editor

### 구조 (Anatomy)

- canvas
- toolbar
- content-blocks
- selection-handle(optional)

### 상태 (States)

| 상태 | 설명 |
|------|------|
| `default` | 기본 상태 |
| `editing` | 편집 모드 활성 |
| `selecting` | 텍스트/블록 선택 중 |
| `readonly` | 읽기 전용 |

### 토큰 바인딩

```
surface: var(--color-surface)
text: var(--color-text)
font: var(--font-body) / var(--text-md) / regular
heading-font: var(--font-heading) / var(--text-2xl) / bold
padding: var(--space-24) var(--space-32)
line-height: var(--leading-relaxed)
```

### 접근성

- contenteditable 영역에 role="textbox"
- aria-multiline="true"
- 도구 모음에 role="toolbar"
- 서식 버튼에 aria-pressed 상태

### 브랜드 적용

- [minimal+precise] density: compact 가능, 불필요한 여백 제거 + 엄격한 spacing scale 준수, 임의 값 금지
- [minimal+precise] color: monochrome 기반, accent 최소화 + 정확한 semantic 분리, 모호한 중간 톤 지양
- [minimal+precise] motion: 80-120ms, 거의 즉각적 + 120-180ms, 군더더기 없는 전환
- [금지] (editorial) hover: 텍스트 underline 또는 color shift, 장식적 효과 없음 — 이것을 피할 것
- [금지] (editorial) motion: 콘텐츠 전환 위주, UI chrome 모션 최소화 — 이것을 피할 것

### 구현 노트

- 기존에 같은 역할의 컴포넌트가 있으면 토큰 교체부터 시작
- variant prop으로 시각적 변형을 관리 (하드코딩 금지)
- 블록 단위 데이터 모델, JSON 직렬화 가능한 구조
- 한글 헤딩은 `word-break: keep-all` / `overflow-wrap: normal`을 기본값으로 두고, 강제 `<br />`는 breakpoint 검증 전 넣지 않음
- 기본 스케일을 사용할 수 있지만 한글 문장 기준으로 실제 wrap을 먼저 검증한다.
- 좁은 UI 텍스트는 Pretendard 기준 label line-height 1.4-1.5를 참고해 뭉침을 방지

---

## editorial / editor-toolbar

**역할**: 서식 도구 모음

**탐지 출처**: rich text editor

### 구조 (Anatomy)

- canvas
- toolbar
- content-blocks
- selection-handle(optional)

### 상태 (States)

| 상태 | 설명 |
|------|------|
| `default` | 기본 상태 |
| `editing` | 편집 모드 활성 |
| `selecting` | 텍스트/블록 선택 중 |
| `readonly` | 읽기 전용 |

### 토큰 바인딩

```
surface: var(--color-surface)
text: var(--color-text)
font: var(--font-body) / var(--text-md) / regular
heading-font: var(--font-heading) / var(--text-2xl) / bold
padding: var(--space-24) var(--space-32)
line-height: var(--leading-relaxed)
```

### 접근성

- contenteditable 영역에 role="textbox"
- aria-multiline="true"
- 도구 모음에 role="toolbar"
- 서식 버튼에 aria-pressed 상태

### 브랜드 적용

- [minimal+precise] density: compact 가능, 불필요한 여백 제거 + 엄격한 spacing scale 준수, 임의 값 금지
- [minimal+precise] color: monochrome 기반, accent 최소화 + 정확한 semantic 분리, 모호한 중간 톤 지양
- [minimal+precise] motion: 80-120ms, 거의 즉각적 + 120-180ms, 군더더기 없는 전환
- [금지] (editorial) hover: 텍스트 underline 또는 color shift, 장식적 효과 없음 — 이것을 피할 것
- [금지] (editorial) motion: 콘텐츠 전환 위주, UI chrome 모션 최소화 — 이것을 피할 것

### Visual Adaptation Hints

- **filter_nav_density**: filter/nav density는 compact하다. chip, scope, pagination을 촘촘하게 묶되 의미 단위별 group은 분리한다. (source=navigation; confidence=0.23; provenance=inferred; direction=고정 sidebar 또는 split-pane navigation을 우선하고, 현재 위치와 scope를 항상 명시한다.; evidence=Split-pane workspace, layout=data-review-surface, density=dense)

### 구현 노트

- 기존에 같은 역할의 컴포넌트가 있으면 토큰 교체부터 시작
- variant prop으로 시각적 변형을 관리 (하드코딩 금지)
- 블록 단위 데이터 모델, JSON 직렬화 가능한 구조
- 한글 헤딩은 `word-break: keep-all` / `overflow-wrap: normal`을 기본값으로 두고, 강제 `<br />`는 breakpoint 검증 전 넣지 않음
- 기본 스케일을 사용할 수 있지만 한글 문장 기준으로 실제 wrap을 먼저 검증한다.
- 좁은 UI 텍스트는 Pretendard 기준 label line-height 1.4-1.5를 참고해 뭉침을 방지
- 반응형 검증: 320px, 360px, 390px, 430px에서 control overflow와 viewport horizontal scroll이 없어야 함
- action row는 narrow viewport에서 `flex-wrap: wrap` 또는 세로 stack으로 전환하고, overflow-x 숨김으로 문제를 덮지 않음

---

## editorial / inline-format-menu

**역할**: 텍스트 선택 시 나타나는 인라인 포맷 메뉴

**탐지 출처**: rich text editor

### 구조 (Anatomy)

- canvas
- toolbar
- content-blocks
- selection-handle(optional)

### 상태 (States)

| 상태 | 설명 |
|------|------|
| `default` | 기본 상태 |
| `editing` | 편집 모드 활성 |
| `selecting` | 텍스트/블록 선택 중 |
| `readonly` | 읽기 전용 |

### 토큰 바인딩

```
surface: var(--color-surface)
text: var(--color-text)
font: var(--font-body) / var(--text-md) / regular
heading-font: var(--font-heading) / var(--text-2xl) / bold
padding: var(--space-24) var(--space-32)
line-height: var(--leading-relaxed)
```

### 접근성

- contenteditable 영역에 role="textbox"
- aria-multiline="true"
- 도구 모음에 role="toolbar"
- 서식 버튼에 aria-pressed 상태

### 브랜드 적용

- [minimal+precise] density: compact 가능, 불필요한 여백 제거 + 엄격한 spacing scale 준수, 임의 값 금지
- [minimal+precise] color: monochrome 기반, accent 최소화 + 정확한 semantic 분리, 모호한 중간 톤 지양
- [minimal+precise] motion: 80-120ms, 거의 즉각적 + 120-180ms, 군더더기 없는 전환
- [금지] (editorial) hover: 텍스트 underline 또는 color shift, 장식적 효과 없음 — 이것을 피할 것
- [금지] (editorial) motion: 콘텐츠 전환 위주, UI chrome 모션 최소화 — 이것을 피할 것

### Visual Adaptation Hints

- **filter_nav_density**: filter/nav density는 compact하다. chip, scope, pagination을 촘촘하게 묶되 의미 단위별 group은 분리한다. (source=navigation; confidence=0.23; provenance=inferred; direction=고정 sidebar 또는 split-pane navigation을 우선하고, 현재 위치와 scope를 항상 명시한다.; evidence=Split-pane workspace, layout=data-review-surface, density=dense)

### 구현 노트

- 기존에 같은 역할의 컴포넌트가 있으면 토큰 교체부터 시작
- variant prop으로 시각적 변형을 관리 (하드코딩 금지)
- 블록 단위 데이터 모델, JSON 직렬화 가능한 구조
- 한글 헤딩은 `word-break: keep-all` / `overflow-wrap: normal`을 기본값으로 두고, 강제 `<br />`는 breakpoint 검증 전 넣지 않음
- 기본 스케일을 사용할 수 있지만 한글 문장 기준으로 실제 wrap을 먼저 검증한다.
- 좁은 UI 텍스트는 Pretendard 기준 label line-height 1.4-1.5를 참고해 뭉침을 방지

---

## editorial / slash-command-menu

**역할**: / 입력으로 블록 타입 선택

**탐지 출처**: rich text editor

### 구조 (Anatomy)

- canvas
- toolbar
- content-blocks
- selection-handle(optional)

### 상태 (States)

| 상태 | 설명 |
|------|------|
| `default` | 기본 상태 |
| `editing` | 편집 모드 활성 |
| `selecting` | 텍스트/블록 선택 중 |
| `readonly` | 읽기 전용 |

### 토큰 바인딩

```
surface: var(--color-surface)
text: var(--color-text)
font: var(--font-body) / var(--text-md) / regular
heading-font: var(--font-heading) / var(--text-2xl) / bold
padding: var(--space-24) var(--space-32)
line-height: var(--leading-relaxed)
```

### 접근성

- contenteditable 영역에 role="textbox"
- aria-multiline="true"
- 도구 모음에 role="toolbar"
- 서식 버튼에 aria-pressed 상태

### 브랜드 적용

- [minimal+precise] density: compact 가능, 불필요한 여백 제거 + 엄격한 spacing scale 준수, 임의 값 금지
- [minimal+precise] color: monochrome 기반, accent 최소화 + 정확한 semantic 분리, 모호한 중간 톤 지양
- [minimal+precise] motion: 80-120ms, 거의 즉각적 + 120-180ms, 군더더기 없는 전환
- [금지] (editorial) hover: 텍스트 underline 또는 color shift, 장식적 효과 없음 — 이것을 피할 것
- [금지] (editorial) motion: 콘텐츠 전환 위주, UI chrome 모션 최소화 — 이것을 피할 것

### Visual Adaptation Hints

- **filter_nav_density**: filter/nav density는 compact하다. chip, scope, pagination을 촘촘하게 묶되 의미 단위별 group은 분리한다. (source=navigation; confidence=0.23; provenance=inferred; direction=고정 sidebar 또는 split-pane navigation을 우선하고, 현재 위치와 scope를 항상 명시한다.; evidence=Split-pane workspace, layout=data-review-surface, density=dense)

### 구현 노트

- 기존에 같은 역할의 컴포넌트가 있으면 토큰 교체부터 시작
- variant prop으로 시각적 변형을 관리 (하드코딩 금지)
- 블록 단위 데이터 모델, JSON 직렬화 가능한 구조
- 한글 헤딩은 `word-break: keep-all` / `overflow-wrap: normal`을 기본값으로 두고, 강제 `<br />`는 breakpoint 검증 전 넣지 않음
- 기본 스케일을 사용할 수 있지만 한글 문장 기준으로 실제 wrap을 먼저 검증한다.
- 좁은 UI 텍스트는 Pretendard 기준 label line-height 1.4-1.5를 참고해 뭉침을 방지

---

## editorial / block-controls

**역할**: 블록 이동/삭제/타입 변경 컨트롤

**탐지 출처**: rich text editor

### 구조 (Anatomy)

- canvas
- toolbar
- content-blocks
- selection-handle(optional)

### 상태 (States)

| 상태 | 설명 |
|------|------|
| `default` | 기본 상태 |
| `editing` | 편집 모드 활성 |
| `selecting` | 텍스트/블록 선택 중 |
| `readonly` | 읽기 전용 |

### 토큰 바인딩

```
surface: var(--color-surface)
text: var(--color-text)
font: var(--font-body) / var(--text-md) / regular
heading-font: var(--font-heading) / var(--text-2xl) / bold
padding: var(--space-24) var(--space-32)
line-height: var(--leading-relaxed)
```

### 접근성

- contenteditable 영역에 role="textbox"
- aria-multiline="true"
- 도구 모음에 role="toolbar"
- 서식 버튼에 aria-pressed 상태

### 브랜드 적용

- [minimal+precise] density: compact 가능, 불필요한 여백 제거 + 엄격한 spacing scale 준수, 임의 값 금지
- [minimal+precise] color: monochrome 기반, accent 최소화 + 정확한 semantic 분리, 모호한 중간 톤 지양
- [minimal+precise] motion: 80-120ms, 거의 즉각적 + 120-180ms, 군더더기 없는 전환
- [금지] (editorial) hover: 텍스트 underline 또는 color shift, 장식적 효과 없음 — 이것을 피할 것
- [금지] (editorial) motion: 콘텐츠 전환 위주, UI chrome 모션 최소화 — 이것을 피할 것

### 구현 노트

- 기존에 같은 역할의 컴포넌트가 있으면 토큰 교체부터 시작
- variant prop으로 시각적 변형을 관리 (하드코딩 금지)
- 블록 단위 데이터 모델, JSON 직렬화 가능한 구조
- 한글 헤딩은 `word-break: keep-all` / `overflow-wrap: normal`을 기본값으로 두고, 강제 `<br />`는 breakpoint 검증 전 넣지 않음
- 기본 스케일을 사용할 수 있지만 한글 문장 기준으로 실제 wrap을 먼저 검증한다.
- 좁은 UI 텍스트는 Pretendard 기준 label line-height 1.4-1.5를 참고해 뭉침을 방지

---

## overlay / command-palette

**역할**: 글로벌 커맨드 팔레트 오버레이

**탐지 출처**: command palette

**Slot archetype**: `advanced:command-palette`

### Advanced Usage

Use when:
- the product has many actions or navigation targets
- expert users benefit from quick action search
Avoid when:
- there are fewer than five meaningful commands
Pairs with: shortcut-hint, saved-view-bar, filter-builder

### 구조 (Anatomy)

- backdrop
- dialog
- search-input
- result-list
- result-item
- shortcut-hint

### 상태 (States)

| 상태 | 설명 |
|------|------|
| `closed` | 닫힌 상태 |
| `open` | 열린 상태 |
| `loading` | 로딩 중 (스피너 표시) |
| `empty` | 데이터 없음 |
| `keyboard-active` | keyboard-active |

### 토큰 바인딩

```
surface: var(--color-surface-elevated)
backdrop: color-mix(in srgb, var(--color-text) 45%, transparent)
border: var(--color-border)
selected-surface: var(--color-surface-tint)
radius: var(--radius-lg)
elevation: var(--elevation-lg)
```

### 접근성

- role="dialog" with aria-modal="true"
- combobox input controls listbox results
- Escape closes and restores focus to trigger

### 브랜드 적용

- [minimal+precise] motion: 80-120ms, 거의 즉각적 + 120-180ms, 군더더기 없는 전환
- [minimal+precise] density: compact 가능, 불필요한 여백 제거 + 엄격한 spacing scale 준수, 임의 값 금지
- [금지] (editorial) hover: 텍스트 underline 또는 color shift, 장식적 효과 없음 — 이것을 피할 것
- [금지] (editorial) motion: 콘텐츠 전환 위주, UI chrome 모션 최소화 — 이것을 피할 것

### 레퍼런스 근거

- **Primer**: ActionMenu is composed of ActionList and Overlay patterns used for quick actions and selections. AnchoredOverlay

### 구현 노트

- 기존에 같은 역할의 컴포넌트가 있으면 토큰 교체부터 시작
- variant prop으로 시각적 변형을 관리 (하드코딩 금지)
- Escape / backdrop click으로 닫기, 열 때 첫 focusable 요소로 이동

---

## overlay / command-result-item

**역할**: 검색/명령 결과 항목

**탐지 출처**: command palette

### 구조 (Anatomy)

- backdrop
- container
- header
- content
- footer(optional)
- close-button

### 상태 (States)

| 상태 | 설명 |
|------|------|
| `closed` | 닫힌 상태 |
| `opening` | 열리는 중 (전환 애니메이션) |
| `open` | 열린 상태 |
| `closing` | 닫히는 중 |

### 토큰 바인딩

```
surface: var(--color-surface-elevated)
backdrop: rgb(0 0 0 / 0.5)
radius: var(--radius-lg)
padding: var(--space-24)
border: var(--color-border)
motion: opacity var(--duration-180) var(--ease-standard)
```

### 접근성

- role="dialog" with aria-modal="true"
- focus trap (Tab 순환)
- Escape로 닫기
- aria-labelledby로 제목 연결
- 닫은 후 trigger 요소로 포커스 복귀

### 브랜드 적용

- [minimal+precise] motion: 80-120ms, 거의 즉각적 + 120-180ms, 군더더기 없는 전환
- [minimal+precise] density: compact 가능, 불필요한 여백 제거 + 엄격한 spacing scale 준수, 임의 값 금지
- [금지] (editorial) hover: 텍스트 underline 또는 color shift, 장식적 효과 없음 — 이것을 피할 것
- [금지] (editorial) motion: 콘텐츠 전환 위주, UI chrome 모션 최소화 — 이것을 피할 것

### 레퍼런스 근거

- **Primer**: ActionMenu is composed of ActionList and Overlay patterns used for quick actions and selections. AnchoredOverlay

### 구현 노트

- 기존에 같은 역할의 컴포넌트가 있으면 토큰 교체부터 시작
- variant prop으로 시각적 변형을 관리 (하드코딩 금지)
- Escape / backdrop click으로 닫기, 열 때 첫 focusable 요소로 이동

---

## feedback / shortcut-hint

**역할**: 키보드 단축키 힌트 표시

**탐지 출처**: command palette

### 구조 (Anatomy)

- container
- icon
- message
- action(optional)
- close-button(optional)

### 상태 (States)

| 상태 | 설명 |
|------|------|
| `info` | 정보 알림 |
| `success` | 성공 알림 |
| `warning` | 경고 알림 |
| `danger` | 에러/위험 알림 |

### 토큰 바인딩

```
surface: var(--color-surface-muted)
text: var(--color-text)
icon: var(--color-info)
border: var(--color-border)
radius: var(--radius-sm)
padding: var(--space-12) var(--space-16)
severity-info: var(--color-info)
severity-success: var(--color-success)
severity-warning: var(--color-warning)
severity-danger: var(--color-danger)
```

### 접근성

- role="alert" for urgent messages
- role="status" for non-urgent
- aria-live="polite" or "assertive"
- 닫기 버튼에 aria-label 필수

### 브랜드 적용

- [minimal+precise] feedback: 아이콘+텍스트 조합, 색상 배경 최소화 + 명확한 상태 구분, 진행률/결과를 수치로 표시
- [minimal+precise] motion: 80-120ms, 거의 즉각적 + 120-180ms, 군더더기 없는 전환
- [minimal+precise] color: monochrome 기반, accent 최소화 + 정확한 semantic 분리, 모호한 중간 톤 지양
- [금지] (editorial) hover: 텍스트 underline 또는 color shift, 장식적 효과 없음 — 이것을 피할 것
- [금지] (editorial) motion: 콘텐츠 전환 위주, UI chrome 모션 최소화 — 이것을 피할 것

### 레퍼런스 근거

- **Carbon Design System**: We welcome all feedback, designs, or ideas in order to produce the best possible experience for our users. If you're interested in contributing, ch...
- **Primer**: Messaging components are used to provide important and relevant information to the user, including feedback, contextual information, product update...

### 구현 노트

- 기존에 같은 역할의 컴포넌트가 있으면 토큰 교체부터 시작
- variant prop으로 시각적 변형을 관리 (하드코딩 금지)
- auto-dismiss 시간은 내용 길이에 비례 (기본 5초)
- 반응형 검증: 320px, 360px, 390px, 430px에서 control overflow와 viewport horizontal scroll이 없어야 함
- action row는 narrow viewport에서 `flex-wrap: wrap` 또는 세로 stack으로 전환하고, overflow-x 숨김으로 문제를 덮지 않음

---

## data-display / comment-thread

**역할**: 댓글 스레드 목록

**탐지 출처**: comments and discussion

### 구조 (Anatomy)

- container
- header
- content-area
- footer(optional)
- action(optional)

### 상태 (States)

| 상태 | 설명 |
|------|------|
| `default` | 기본 상태 |
| `loading` | 로딩 중 (스피너 표시) |
| `empty` | 데이터 없음 |
| `error` | 유효성 검증 실패 |

### 토큰 바인딩

```
surface: var(--color-surface)
border: var(--color-border)
radius: var(--radius-md)
padding: var(--space-16) var(--space-20)
heading-font: var(--font-heading) / var(--text-md) / semibold
body-font: var(--font-body) / var(--text-sm) / regular
text: var(--color-text)
text-muted: var(--color-text-muted)
```

### 접근성

- 적절한 heading level 사용
- 데이터 테이블은 scope와 caption 필수
- 빈 상태에서 안내 텍스트 제공

### 브랜드 적용

- [minimal+precise] density: compact 가능, 불필요한 여백 제거 + 엄격한 spacing scale 준수, 임의 값 금지
- [minimal+precise] color: monochrome 기반, accent 최소화 + 정확한 semantic 분리, 모호한 중간 톤 지양
- [금지] (editorial) hover: 텍스트 underline 또는 color shift, 장식적 효과 없음 — 이것을 피할 것
- [금지] (editorial) motion: 콘텐츠 전환 위주, UI chrome 모션 최소화 — 이것을 피할 것

### Visual Adaptation Hints

- **card_elevation_tendency**: 카드는 거의 무그림자 평면으로 유지하고 tint/divider로 계층을 만든다. 압축된 spacing에서도 header/body/footer 구획은 divider나 tint로 유지한다. (source=cards; confidence=0.29; provenance=inferred; direction=flat card planes를 기본으로 하고, 압축된 spacing과 얇은 divider 중심의 hierarchy. 중간 반경으로 제품 UI 절제 유지.; evidence=surface=flat, density=dense, corner=medium)
- **border_vs_fill_emphasis**: fill 중심이다. neutral surface를 기본으로 하고 border는 상태 변화나 구획 보조에만 쓴다. (source=cards; confidence=0.29; provenance=inferred; direction=flat card planes를 기본으로 하고, 압축된 spacing과 얇은 divider 중심의 hierarchy. 중간 반경으로 제품 UI 절제 유지.; evidence=surface=flat, density=dense, corner=medium)
- **chart_panel_framing**: 차트 패널은 flush surface와 thin divider 중심으로 프레이밍한다. 헤더의 metric, controls, plot 영역을 분리하고 내부 여백은 촘촘하게 관리한다. (source=data_display; confidence=0.29; provenance=inferred; direction=정보 밀도를 유지하되 thin dividers와 restrained accent로 hierarchy를 만든다.; evidence=layout=dashboard-grid, density=dense, layout=data-review-surface, surface=flat)

### 구현 노트

- 기존에 같은 역할의 컴포넌트가 있으면 토큰 교체부터 시작
- variant prop으로 시각적 변형을 관리 (하드코딩 금지)
- 빈 상태(empty-state)와 에러 상태를 반드시 처리
- 좁은 UI 텍스트는 Pretendard 기준 label line-height 1.4-1.5를 참고해 뭉침을 방지

---

## input / comment-input

**역할**: 댓글 입력 영역

**탐지 출처**: comments and discussion

### 구조 (Anatomy)

- container
- label
- input-area
- helper-text(optional)
- leading-icon(optional)
- clear-button(optional)

### 상태 (States)

| 상태 | 설명 |
|------|------|
| `default` | 기본 상태 |
| `focus` | 키보드 포커스 시 |
| `filled` | 값이 입력된 상태 |
| `error` | 유효성 검증 실패 |
| `disabled` | 비활성 (상호작용 불가) |
| `readonly` | 읽기 전용 |

### 토큰 바인딩

```
surface: var(--color-surface)
text: var(--color-text)
placeholder: var(--color-text-subtle)
border: var(--color-border)
border-focus: var(--color-brand-primary)
border-error: var(--color-danger)
radius: var(--radius-sm)
padding: var(--space-8) var(--space-12)
font: var(--font-body) / var(--text-md) / regular
```

### 접근성

- label과 input을 for/id로 연결
- aria-describedby로 helper/error text 연결
- aria-invalid="true" when error
- aria-required="true" when required

### 브랜드 적용

- [minimal+precise] hover: 미세한 opacity 또는 underline만 + 정확한 border/outline 변화
- [minimal+precise] density: compact 가능, 불필요한 여백 제거 + 엄격한 spacing scale 준수, 임의 값 금지
- [minimal+precise] feedback: 아이콘+텍스트 조합, 색상 배경 최소화 + 명확한 상태 구분, 진행률/결과를 수치로 표시
- [금지] (editorial) hover: 텍스트 underline 또는 color shift, 장식적 효과 없음 — 이것을 피할 것
- [금지] (editorial) motion: 콘텐츠 전환 위주, UI chrome 모션 최소화 — 이것을 피할 것

### 레퍼런스 근거

- **Carbon Design System**: Number input Text input
- **Primer**: I worked in data visualization and map-making for most of my career, and solving design problems with data is my jam. To me there's something uniqu...

### 구현 노트

- 기존에 같은 역할의 컴포넌트가 있으면 토큰 교체부터 시작
- variant prop으로 시각적 변형을 관리 (하드코딩 금지)
- error 상태에서 helper text → error message로 자동 전환
- label은 항상 visible (placeholder만으로 대체 금지)
- 반응형 검증: 320px, 360px, 390px, 430px에서 control overflow와 viewport horizontal scroll이 없어야 함
- action row는 narrow viewport에서 `flex-wrap: wrap` 또는 세로 stack으로 전환하고, overflow-x 숨김으로 문제를 덮지 않음

---

## overlay / mention-popup

**역할**: @멘션 자동완성 팝업

**탐지 출처**: comments and discussion

### 구조 (Anatomy)

- backdrop
- container
- header
- content
- footer(optional)
- close-button

### 상태 (States)

| 상태 | 설명 |
|------|------|
| `closed` | 닫힌 상태 |
| `opening` | 열리는 중 (전환 애니메이션) |
| `open` | 열린 상태 |
| `closing` | 닫히는 중 |

### 토큰 바인딩

```
surface: var(--color-surface-elevated)
backdrop: rgb(0 0 0 / 0.5)
radius: var(--radius-lg)
padding: var(--space-24)
border: var(--color-border)
motion: opacity var(--duration-180) var(--ease-standard)
```

### 접근성

- role="dialog" with aria-modal="true"
- focus trap (Tab 순환)
- Escape로 닫기
- aria-labelledby로 제목 연결
- 닫은 후 trigger 요소로 포커스 복귀

### 브랜드 적용

- [minimal+precise] motion: 80-120ms, 거의 즉각적 + 120-180ms, 군더더기 없는 전환
- [minimal+precise] density: compact 가능, 불필요한 여백 제거 + 엄격한 spacing scale 준수, 임의 값 금지
- [금지] (editorial) hover: 텍스트 underline 또는 color shift, 장식적 효과 없음 — 이것을 피할 것
- [금지] (editorial) motion: 콘텐츠 전환 위주, UI chrome 모션 최소화 — 이것을 피할 것

### 레퍼런스 근거

- **Primer**: ActionMenu is composed of ActionList and Overlay patterns used for quick actions and selections. AnchoredOverlay

### 구현 노트

- 기존에 같은 역할의 컴포넌트가 있으면 토큰 교체부터 시작
- variant prop으로 시각적 변형을 관리 (하드코딩 금지)
- Escape / backdrop click으로 닫기, 열 때 첫 focusable 요소로 이동

---

## marketing / hero-container

**역할**: 랜딩 상단 히어로 섹션 컨테이너

**탐지 출처**: hero section

### 구조 (Anatomy)

- section-container
- inner-max-width
- content

### 상태 (States)

| 상태 | 설명 |
|------|------|
| `default` | 기본 상태 |
| `in-view` | in-view |
| `hover` | 마우스 오버 시 |

### 토큰 바인딩

```
section-background: var(--color-canvas)
inner-padding: var(--space-96) var(--space-24)
inner-max-width: 1120px
heading-font: var(--font-heading) / var(--text-3xl) / semibold
body-font: var(--font-body) / var(--text-md) / regular
text: var(--color-text)
text-muted: var(--color-text-muted)
```

### 접근성

- 의미 있는 <section> 또는 <header>/<footer> 랜드마크 사용
- aria-labelledby로 제목(<h1>/<h2>)과 연결
- 색상만으로 의미 전달 금지
- 키보드로 CTA와 링크 접근 가능

### 브랜드 적용

- [minimal+precise] color: monochrome 기반, accent 최소화 + 정확한 semantic 분리, 모호한 중간 톤 지양
- [minimal+precise] motion: 80-120ms, 거의 즉각적 + 120-180ms, 군더더기 없는 전환
- [minimal+precise] density: compact 가능, 불필요한 여백 제거 + 엄격한 spacing scale 준수, 임의 값 금지
- [금지] (editorial) hover: 텍스트 underline 또는 color shift, 장식적 효과 없음 — 이것을 피할 것
- [금지] (editorial) motion: 콘텐츠 전환 위주, UI chrome 모션 최소화 — 이것을 피할 것

### 레퍼런스 근거

- **Primer**: Design digital marketing experiences with Primer Brand UI Shared Foundations

### 구현 노트

- 기존에 같은 역할의 컴포넌트가 있으면 토큰 교체부터 시작
- variant prop으로 시각적 변형을 관리 (하드코딩 금지)
- 섹션에 <h2 id="...">과 aria-labelledby 필수
- CSS 변수(var(--color-*))를 그대로 쓰고 hex 하드코딩 금지
- 다크 모드는 globals.css의 prefers-color-scheme 블록에 위임
- 한글 헤딩은 `word-break: keep-all` / `overflow-wrap: normal`을 기본값으로 두고, 강제 `<br />`는 breakpoint 검증 전 넣지 않음
- 기본 스케일을 사용할 수 있지만 한글 문장 기준으로 실제 wrap을 먼저 검증한다.
- 좁은 UI 텍스트는 Pretendard 기준 label line-height 1.4-1.5를 참고해 뭉침을 방지

---

## marketing / hero-eyebrow

**역할**: 헤드라인 위 카테고리/레이블 텍스트

**탐지 출처**: hero section

**Slot archetype**: `text-eyebrow`

### 구조 (Anatomy)

- eyebrow-label

### 상태 (States)

| 상태 | 설명 |
|------|------|
| `default` | 기본 상태 |

### 토큰 바인딩

```
font: var(--font-mono)
size: var(--text-xs)
weight: medium (500)
color: var(--color-text-subtle)
letter-spacing: 0.08em
text-transform: uppercase
```

### 접근성

- 장식용 카테고리 레이블 — 스크린 리더가 건너뛸 수 있어야 함
- 의미가 필요하면 heading 위 <p> 또는 <span> 사용

### 브랜드 적용

- [minimal+precise] color: monochrome 기반, accent 최소화 + 정확한 semantic 분리, 모호한 중간 톤 지양
- [minimal+precise] motion: 80-120ms, 거의 즉각적 + 120-180ms, 군더더기 없는 전환
- [minimal+precise] density: compact 가능, 불필요한 여백 제거 + 엄격한 spacing scale 준수, 임의 값 금지
- [금지] (editorial) hover: 텍스트 underline 또는 color shift, 장식적 효과 없음 — 이것을 피할 것
- [금지] (editorial) motion: 콘텐츠 전환 위주, UI chrome 모션 최소화 — 이것을 피할 것

### 레퍼런스 근거

- **Primer**: Design digital marketing experiences with Primer Brand UI Shared Foundations

### 구현 노트

- 기존에 같은 역할의 컴포넌트가 있으면 토큰 교체부터 시작
- variant prop으로 시각적 변형을 관리 (하드코딩 금지)
- 섹션에 <h2 id="...">과 aria-labelledby 필수
- CSS 변수(var(--color-*))를 그대로 쓰고 hex 하드코딩 금지
- 다크 모드는 globals.css의 prefers-color-scheme 블록에 위임
- 한글 헤딩은 `word-break: keep-all` / `overflow-wrap: normal`을 기본값으로 두고, 강제 `<br />`는 breakpoint 검증 전 넣지 않음
- 기본 스케일을 사용할 수 있지만 한글 문장 기준으로 실제 wrap을 먼저 검증한다.
- 좁은 UI 텍스트는 Pretendard 기준 label line-height 1.4-1.5를 참고해 뭉침을 방지

---

## marketing / hero-headline

**역할**: 핵심 가치 제안 헤드라인

**탐지 출처**: hero section

**Slot archetype**: `text-heading`

### 구조 (Anatomy)

- heading-text

### 상태 (States)

| 상태 | 설명 |
|------|------|
| `default` | 기본 상태 |

### 토큰 바인딩

```
font: var(--font-heading)
size: var(--text-3xl)
weight: semibold (600)
line-height: var(--leading-tight)
color: var(--color-text)
letter-spacing: -0.01em
```

### 접근성

- 의미 있는 heading 태그 사용 (<h1>~<h3>)
- 페이지당 <h1>은 1개
- aria-labelledby의 id 타깃이 되어야 함

### 브랜드 적용

- [minimal+precise] color: monochrome 기반, accent 최소화 + 정확한 semantic 분리, 모호한 중간 톤 지양
- [minimal+precise] motion: 80-120ms, 거의 즉각적 + 120-180ms, 군더더기 없는 전환
- [minimal+precise] density: compact 가능, 불필요한 여백 제거 + 엄격한 spacing scale 준수, 임의 값 금지
- [금지] (editorial) hover: 텍스트 underline 또는 color shift, 장식적 효과 없음 — 이것을 피할 것
- [금지] (editorial) motion: 콘텐츠 전환 위주, UI chrome 모션 최소화 — 이것을 피할 것

### 레퍼런스 근거

- **Primer**: Design digital marketing experiences with Primer Brand UI Shared Foundations

### 구현 노트

- 기존에 같은 역할의 컴포넌트가 있으면 토큰 교체부터 시작
- variant prop으로 시각적 변형을 관리 (하드코딩 금지)
- 섹션에 <h2 id="...">과 aria-labelledby 필수
- CSS 변수(var(--color-*))를 그대로 쓰고 hex 하드코딩 금지
- 다크 모드는 globals.css의 prefers-color-scheme 블록에 위임
- 한글 헤딩은 `word-break: keep-all` / `overflow-wrap: normal`을 기본값으로 두고, 강제 `<br />`는 breakpoint 검증 전 넣지 않음
- 기본 스케일을 사용할 수 있지만 한글 문장 기준으로 실제 wrap을 먼저 검증한다.
- 좁은 UI 텍스트는 Pretendard 기준 label line-height 1.4-1.5를 참고해 뭉침을 방지

---

## marketing / hero-subheadline

**역할**: 헤드라인을 보강하는 서브 카피

**탐지 출처**: hero section

**Slot archetype**: `text-body`

### 구조 (Anatomy)

- body-text

### 상태 (States)

| 상태 | 설명 |
|------|------|
| `default` | 기본 상태 |

### 토큰 바인딩

```
font: var(--font-body)
size: var(--text-lg)
line-height: var(--leading-relaxed)
color: var(--color-text-muted)
max-width: 65ch
```

### 접근성

- 의미 있는 <p> 태그 사용
- line-length 75ch 이하 권장

### 브랜드 적용

- [minimal+precise] color: monochrome 기반, accent 최소화 + 정확한 semantic 분리, 모호한 중간 톤 지양
- [minimal+precise] motion: 80-120ms, 거의 즉각적 + 120-180ms, 군더더기 없는 전환
- [minimal+precise] density: compact 가능, 불필요한 여백 제거 + 엄격한 spacing scale 준수, 임의 값 금지
- [금지] (editorial) hover: 텍스트 underline 또는 color shift, 장식적 효과 없음 — 이것을 피할 것
- [금지] (editorial) motion: 콘텐츠 전환 위주, UI chrome 모션 최소화 — 이것을 피할 것

### 레퍼런스 근거

- **Primer**: Design digital marketing experiences with Primer Brand UI Shared Foundations

### 구현 노트

- 기존에 같은 역할의 컴포넌트가 있으면 토큰 교체부터 시작
- variant prop으로 시각적 변형을 관리 (하드코딩 금지)
- 섹션에 <h2 id="...">과 aria-labelledby 필수
- CSS 변수(var(--color-*))를 그대로 쓰고 hex 하드코딩 금지
- 다크 모드는 globals.css의 prefers-color-scheme 블록에 위임
- 한글 헤딩은 `word-break: keep-all` / `overflow-wrap: normal`을 기본값으로 두고, 강제 `<br />`는 breakpoint 검증 전 넣지 않음
- 기본 스케일을 사용할 수 있지만 한글 문장 기준으로 실제 wrap을 먼저 검증한다.
- 좁은 UI 텍스트는 Pretendard 기준 label line-height 1.4-1.5를 참고해 뭉침을 방지

---

## button / hero-cta-group

**역할**: primary/secondary CTA 버튼 묶음

**탐지 출처**: hero section

### 구조 (Anatomy)

- container
- label
- leading-icon(optional)
- trailing-icon(optional)

### 상태 (States)

| 상태 | 설명 |
|------|------|
| `default` | 기본 상태 |
| `hover` | 마우스 오버 시 |
| `active` | 클릭/탭 중 |
| `disabled` | 비활성 (상호작용 불가) |
| `loading` | 로딩 중 (스피너 표시) |

### 토큰 바인딩

```
surface: var(--color-brand-primary)
text: var(--color-text-inverse)
border: var(--color-brand-primary)
radius: var(--radius-md)
padding: var(--space-12) var(--space-24)
max-inline-size: 100%
min-inline-size: 0
label-wrap: white-space: normal
font: var(--font-body) / var(--text-md) / semibold
hover-surface: var(--color-link-hover)
focus-ring: box-shadow: 0 0 0 2px var(--color-surface), 0 0 0 4px var(--color-brand-primary)
motion: background var(--duration-180) var(--ease-standard)
```

### 접근성

- role="button"
- aria-disabled="true" when disabled
- aria-busy="true" when loading
- 최소 44x44 터치 영역
- 텍스트 대비 4.5:1 이상
- 320px viewport에서도 버튼 전체와 focus ring이 화면 밖으로 나가지 않아야 함

### 브랜드 적용

- [minimal+precise] hover: 미세한 opacity 또는 underline만 + 정확한 border/outline 변화
- [minimal+precise] motion: 80-120ms, 거의 즉각적 + 120-180ms, 군더더기 없는 전환
- [minimal+precise] color: monochrome 기반, accent 최소화 + 정확한 semantic 분리, 모호한 중간 톤 지양
- [금지] (editorial) hover: 텍스트 underline 또는 color shift, 장식적 효과 없음 — 이것을 피할 것
- [금지] (editorial) motion: 콘텐츠 전환 위주, UI chrome 모션 최소화 — 이것을 피할 것

### Visual Adaptation Hints

- **cta_prominence**: CTA prominence는 strong이다. 섹션당 primary CTA 1개만 fill/accent로 강하게 띄우고 secondary는 조용하게 후퇴시킨다. (source=cards; confidence=0.29; provenance=inferred; direction=flat card planes를 기본으로 하고, 압축된 spacing과 얇은 divider 중심의 hierarchy. 중간 반경으로 제품 UI 절제 유지.; evidence=surface=flat, density=dense, corner=medium, layout=data-review-surface)

### 레퍼런스 근거

- **Carbon Design System**: These components can toggle between the AI variant and the default variant depending on the user’s interaction. If the user manually overrides the ...
- **Primer**: I get so much joy from writing HTML and CSS, and design systems are one level up - systematically making UIs accessible and consistent. I love conc...

### 구현 노트

- 기존에 같은 역할의 컴포넌트가 있으면 토큰 교체부터 시작
- variant prop으로 시각적 변형을 관리 (하드코딩 금지)
- size prop: sm / md / lg (터치 영역은 항상 최소 44px 보장)
- 모든 버튼은 `max-inline-size: 100%`와 `min-inline-size: 0`을 기본 보호값으로 갖고, 긴 라벨은 모바일에서 wrap 또는 action-group stack으로 처리
- fixed `width`/`min-width` px 값으로 CTA 폭을 고정하지 않음 — 필요하면 container query 또는 <=480px stack fallback을 함께 정의
- 반응형 검증: 320px, 360px, 390px, 430px에서 control overflow와 viewport horizontal scroll이 없어야 함
- action row는 narrow viewport에서 `flex-wrap: wrap` 또는 세로 stack으로 전환하고, overflow-x 숨김으로 문제를 덮지 않음

---

## marketing / hero-visual

**역할**: 히어로 우측/하단의 제품 스크린샷 또는 일러스트

**탐지 출처**: hero section

**Slot archetype**: `media-frame`

### 구조 (Anatomy)

- frame-container
- visual

### 상태 (States)

| 상태 | 설명 |
|------|------|
| `default` | 기본 상태 |

### 토큰 바인딩

```
radius: var(--radius-xl)
border: var(--color-border)
surface: var(--color-surface-tint)
aspect-ratio: 4 / 3
padding: var(--space-24)
```

### 접근성

- 의미 있는 이미지면 alt 필수, 장식이면 alt=""
- SVG는 role="img"과 <title> 포함

### 브랜드 적용

- [minimal+precise] color: monochrome 기반, accent 최소화 + 정확한 semantic 분리, 모호한 중간 톤 지양
- [minimal+precise] motion: 80-120ms, 거의 즉각적 + 120-180ms, 군더더기 없는 전환
- [minimal+precise] density: compact 가능, 불필요한 여백 제거 + 엄격한 spacing scale 준수, 임의 값 금지
- [금지] (editorial) hover: 텍스트 underline 또는 color shift, 장식적 효과 없음 — 이것을 피할 것
- [금지] (editorial) motion: 콘텐츠 전환 위주, UI chrome 모션 최소화 — 이것을 피할 것

### 레퍼런스 근거

- **Primer**: Design digital marketing experiences with Primer Brand UI Shared Foundations

### 구현 노트

- 기존에 같은 역할의 컴포넌트가 있으면 토큰 교체부터 시작
- variant prop으로 시각적 변형을 관리 (하드코딩 금지)
- 섹션에 <h2 id="...">과 aria-labelledby 필수
- CSS 변수(var(--color-*))를 그대로 쓰고 hex 하드코딩 금지
- 다크 모드는 globals.css의 prefers-color-scheme 블록에 위임
- 한글 헤딩은 `word-break: keep-all` / `overflow-wrap: normal`을 기본값으로 두고, 강제 `<br />`는 breakpoint 검증 전 넣지 않음
- 기본 스케일을 사용할 수 있지만 한글 문장 기준으로 실제 wrap을 먼저 검증한다.
- 좁은 UI 텍스트는 Pretendard 기준 label line-height 1.4-1.5를 참고해 뭉침을 방지

---

## marketing / hero-trust-strip

**역할**: 히어로 바로 아래의 신뢰 라인 (사용자 수, 평가 등)

**탐지 출처**: hero section

**Slot archetype**: `trust-strip`

### 구조 (Anatomy)

- list-container
- item
- bullet-icon

### 상태 (States)

| 상태 | 설명 |
|------|------|
| `default` | 기본 상태 |

### 토큰 바인딩

```
text: var(--color-text-muted)
font: var(--font-mono)
size: var(--text-xs)
bullet-color: var(--color-brand-primary)
gap: var(--space-16)
```

### 접근성

- role="list"로 리스트 시맨틱 유지
- 불릿 SVG는 aria-hidden="true"

### 브랜드 적용

- [minimal+precise] color: monochrome 기반, accent 최소화 + 정확한 semantic 분리, 모호한 중간 톤 지양
- [minimal+precise] motion: 80-120ms, 거의 즉각적 + 120-180ms, 군더더기 없는 전환
- [minimal+precise] density: compact 가능, 불필요한 여백 제거 + 엄격한 spacing scale 준수, 임의 값 금지
- [금지] (editorial) hover: 텍스트 underline 또는 color shift, 장식적 효과 없음 — 이것을 피할 것
- [금지] (editorial) motion: 콘텐츠 전환 위주, UI chrome 모션 최소화 — 이것을 피할 것

### 레퍼런스 근거

- **Primer**: Design digital marketing experiences with Primer Brand UI Shared Foundations

### 구현 노트

- 기존에 같은 역할의 컴포넌트가 있으면 토큰 교체부터 시작
- variant prop으로 시각적 변형을 관리 (하드코딩 금지)
- 섹션에 <h2 id="...">과 aria-labelledby 필수
- CSS 변수(var(--color-*))를 그대로 쓰고 hex 하드코딩 금지
- 다크 모드는 globals.css의 prefers-color-scheme 블록에 위임
- 한글 헤딩은 `word-break: keep-all` / `overflow-wrap: normal`을 기본값으로 두고, 강제 `<br />`는 breakpoint 검증 전 넣지 않음
- 기본 스케일을 사용할 수 있지만 한글 문장 기준으로 실제 wrap을 먼저 검증한다.
- 좁은 UI 텍스트는 Pretendard 기준 label line-height 1.4-1.5를 참고해 뭉침을 방지

---

## input / switch

**역할**: Immediate on/off preference control.

**탐지 출처**: astryx-geist-reference-baseline

### 구조 (Anatomy)

- container
- label
- input-area
- helper-text(optional)
- leading-icon(optional)
- clear-button(optional)

### 상태 (States)

| 상태 | 설명 |
|------|------|
| `default` | 기본 상태 |
| `focus` | 키보드 포커스 시 |
| `filled` | 값이 입력된 상태 |
| `error` | 유효성 검증 실패 |
| `disabled` | 비활성 (상호작용 불가) |
| `readonly` | 읽기 전용 |

### 토큰 바인딩

```
surface: var(--color-surface)
text: var(--color-text)
placeholder: var(--color-text-subtle)
border: var(--color-border)
border-focus: var(--color-brand-primary)
border-error: var(--color-danger)
radius: var(--radius-sm)
padding: var(--space-8) var(--space-12)
font: var(--font-body) / var(--text-md) / regular
```

### 접근성

- label과 input을 for/id로 연결
- aria-describedby로 helper/error text 연결
- aria-invalid="true" when error
- aria-required="true" when required

### 브랜드 적용

- [minimal+precise] hover: 미세한 opacity 또는 underline만 + 정확한 border/outline 변화
- [minimal+precise] density: compact 가능, 불필요한 여백 제거 + 엄격한 spacing scale 준수, 임의 값 금지
- [minimal+precise] feedback: 아이콘+텍스트 조합, 색상 배경 최소화 + 명확한 상태 구분, 진행률/결과를 수치로 표시
- [금지] (editorial) hover: 텍스트 underline 또는 color shift, 장식적 효과 없음 — 이것을 피할 것
- [금지] (editorial) motion: 콘텐츠 전환 위주, UI chrome 모션 최소화 — 이것을 피할 것

### 레퍼런스 근거

- **Carbon Design System**: These components can toggle between the AI variant and the default variant depending on the user’s interaction. If the user manually overrides the ...
- **Primer**: Note: legacy variables in Primer React from the theme object all resolve to CSS variables under the hood. While the new naming convention is not av...

### 구현 노트

- 기존에 같은 역할의 컴포넌트가 있으면 토큰 교체부터 시작
- variant prop으로 시각적 변형을 관리 (하드코딩 금지)
- error 상태에서 helper text → error message로 자동 전환
- label은 항상 visible (placeholder만으로 대체 금지)
- 반응형 검증: 320px, 360px, 390px, 430px에서 control overflow와 viewport horizontal scroll이 없어야 함
- action row는 narrow viewport에서 `flex-wrap: wrap` 또는 세로 stack으로 전환하고, overflow-x 숨김으로 문제를 덮지 않음

---

## input / segmented-control

**역할**: Small mutually exclusive mode switcher.

**탐지 출처**: astryx-geist-reference-baseline

### 구조 (Anatomy)

- container
- label
- input-area
- helper-text(optional)
- leading-icon(optional)
- clear-button(optional)

### 상태 (States)

| 상태 | 설명 |
|------|------|
| `default` | 기본 상태 |
| `focus` | 키보드 포커스 시 |
| `filled` | 값이 입력된 상태 |
| `error` | 유효성 검증 실패 |
| `disabled` | 비활성 (상호작용 불가) |
| `readonly` | 읽기 전용 |

### 토큰 바인딩

```
surface: var(--color-surface)
text: var(--color-text)
placeholder: var(--color-text-subtle)
border: var(--color-border)
border-focus: var(--color-brand-primary)
border-error: var(--color-danger)
radius: var(--radius-sm)
padding: var(--space-8) var(--space-12)
font: var(--font-body) / var(--text-md) / regular
```

### 접근성

- label과 input을 for/id로 연결
- aria-describedby로 helper/error text 연결
- aria-invalid="true" when error
- aria-required="true" when required

### 브랜드 적용

- [minimal+precise] hover: 미세한 opacity 또는 underline만 + 정확한 border/outline 변화
- [minimal+precise] density: compact 가능, 불필요한 여백 제거 + 엄격한 spacing scale 준수, 임의 값 금지
- [minimal+precise] feedback: 아이콘+텍스트 조합, 색상 배경 최소화 + 명확한 상태 구분, 진행률/결과를 수치로 표시
- [금지] (editorial) hover: 텍스트 underline 또는 color shift, 장식적 효과 없음 — 이것을 피할 것
- [금지] (editorial) motion: 콘텐츠 전환 위주, UI chrome 모션 최소화 — 이것을 피할 것

### 레퍼런스 근거

- **Carbon Design System**: Number input Text input
- **Primer**: I worked in data visualization and map-making for most of my career, and solving design problems with data is my jam. To me there's something uniqu...

### 구현 노트

- 기존에 같은 역할의 컴포넌트가 있으면 토큰 교체부터 시작
- variant prop으로 시각적 변형을 관리 (하드코딩 금지)
- error 상태에서 helper text → error message로 자동 전환
- label은 항상 visible (placeholder만으로 대체 금지)
- 반응형 검증: 320px, 360px, 390px, 430px에서 control overflow와 viewport horizontal scroll이 없어야 함
- action row는 narrow viewport에서 `flex-wrap: wrap` 또는 세로 stack으로 전환하고, overflow-x 숨김으로 문제를 덮지 않음

---

## navigation / breadcrumbs

**역할**: Hierarchy trail for deep product areas.

**탐지 출처**: astryx-geist-reference-baseline

### 구조 (Anatomy)

- container
- nav-item
- icon(optional)
- label
- indicator(active)
- badge(optional)

### 상태 (States)

| 상태 | 설명 |
|------|------|
| `default` | 기본 상태 |
| `hover` | 마우스 오버 시 |
| `active` | 클릭/탭 중 |
| `collapsed` | 접힌 상태 |

### 토큰 바인딩

```
surface: var(--color-surface)
text: var(--color-text-muted)
text-active: var(--color-text)
indicator: var(--color-brand-accent)
padding: var(--space-8) var(--space-16)
font: var(--font-body) / var(--text-sm) / medium
```

### 접근성

- nav landmark (role="navigation")
- aria-current="page" for active item
- 키보드 화살표 탐색 지원

### 브랜드 적용

- [minimal+precise] hover: 미세한 opacity 또는 underline만 + 정확한 border/outline 변화
- [minimal+precise] density: compact 가능, 불필요한 여백 제거 + 엄격한 spacing scale 준수, 임의 값 금지
- [minimal+precise] motion: 80-120ms, 거의 즉각적 + 120-180ms, 군더더기 없는 전환
- [금지] (editorial) hover: 텍스트 underline 또는 color shift, 장식적 효과 없음 — 이것을 피할 것
- [금지] (editorial) motion: 콘텐츠 전환 위주, UI chrome 모션 최소화 — 이것을 피할 것

### Visual Adaptation Hints

- **filter_nav_density**: filter/nav density는 compact하다. chip, scope, pagination을 촘촘하게 묶되 의미 단위별 group은 분리한다. (source=navigation; confidence=0.23; provenance=inferred; direction=고정 sidebar 또는 split-pane navigation을 우선하고, 현재 위치와 scope를 항상 명시한다.; evidence=Split-pane workspace, layout=data-review-surface, density=dense)

### 레퍼런스 근거

- **Carbon Design System**: Library menu navigation There are two kinds of symbols — library symbols and document symbols. Library symbols are available in any Sketch document...
- **Primer**: Octicon nav items navigation 12 px

### 구현 노트

- 기존에 같은 역할의 컴포넌트가 있으면 토큰 교체부터 시작
- variant prop으로 시각적 변형을 관리 (하드코딩 금지)
- active 상태는 URL/라우터와 자동 동기화
- 좁은 UI 텍스트는 Pretendard 기준 label line-height 1.4-1.5를 참고해 뭉침을 방지
- 반응형 검증: 320px, 360px, 390px, 430px에서 control overflow와 viewport horizontal scroll이 없어야 함
- action row는 narrow viewport에서 `flex-wrap: wrap` 또는 세로 stack으로 전환하고, overflow-x 숨김으로 문제를 덮지 않음

---

## navigation / tabs

**역할**: Peer view switcher for related panels.

**탐지 출처**: astryx-geist-reference-baseline

### 구조 (Anatomy)

- container
- nav-item
- icon(optional)
- label
- indicator(active)
- badge(optional)

### 상태 (States)

| 상태 | 설명 |
|------|------|
| `default` | 기본 상태 |
| `hover` | 마우스 오버 시 |
| `active` | 클릭/탭 중 |
| `collapsed` | 접힌 상태 |

### 토큰 바인딩

```
surface: var(--color-surface)
text: var(--color-text-muted)
text-active: var(--color-text)
indicator: var(--color-brand-accent)
padding: var(--space-8) var(--space-16)
font: var(--font-body) / var(--text-sm) / medium
```

### 접근성

- nav landmark (role="navigation")
- aria-current="page" for active item
- 키보드 화살표 탐색 지원

### 브랜드 적용

- [minimal+precise] hover: 미세한 opacity 또는 underline만 + 정확한 border/outline 변화
- [minimal+precise] density: compact 가능, 불필요한 여백 제거 + 엄격한 spacing scale 준수, 임의 값 금지
- [minimal+precise] motion: 80-120ms, 거의 즉각적 + 120-180ms, 군더더기 없는 전환
- [금지] (editorial) hover: 텍스트 underline 또는 color shift, 장식적 효과 없음 — 이것을 피할 것
- [금지] (editorial) motion: 콘텐츠 전환 위주, UI chrome 모션 최소화 — 이것을 피할 것

### Visual Adaptation Hints

- **filter_nav_density**: filter/nav density는 compact하다. chip, scope, pagination을 촘촘하게 묶되 의미 단위별 group은 분리한다. (source=navigation; confidence=0.23; provenance=inferred; direction=고정 sidebar 또는 split-pane navigation을 우선하고, 현재 위치와 scope를 항상 명시한다.; evidence=Split-pane workspace, layout=data-review-surface, density=dense)

### 레퍼런스 근거

- **Carbon Design System**: Library menu navigation There are two kinds of symbols — library symbols and document symbols. Library symbols are available in any Sketch document...
- **Primer**: Octicon nav items navigation 12 px

### 구현 노트

- 기존에 같은 역할의 컴포넌트가 있으면 토큰 교체부터 시작
- variant prop으로 시각적 변형을 관리 (하드코딩 금지)
- active 상태는 URL/라우터와 자동 동기화
- 좁은 UI 텍스트는 Pretendard 기준 label line-height 1.4-1.5를 참고해 뭉침을 방지
- 반응형 검증: 320px, 360px, 390px, 430px에서 control overflow와 viewport horizontal scroll이 없어야 함
- action row는 narrow viewport에서 `flex-wrap: wrap` 또는 세로 stack으로 전환하고, overflow-x 숨김으로 문제를 덮지 않음

---

## feedback / badge

**역할**: Compact status, category, or count label.

**탐지 출처**: astryx-geist-reference-baseline

### 구조 (Anatomy)

- container
- icon
- message
- action(optional)
- close-button(optional)

### 상태 (States)

| 상태 | 설명 |
|------|------|
| `info` | 정보 알림 |
| `success` | 성공 알림 |
| `warning` | 경고 알림 |
| `danger` | 에러/위험 알림 |

### 토큰 바인딩

```
surface: var(--color-surface-muted)
text: var(--color-text)
icon: var(--color-info)
border: var(--color-border)
radius: var(--radius-sm)
padding: var(--space-12) var(--space-16)
severity-info: var(--color-info)
severity-success: var(--color-success)
severity-warning: var(--color-warning)
severity-danger: var(--color-danger)
```

### 접근성

- role="alert" for urgent messages
- role="status" for non-urgent
- aria-live="polite" or "assertive"
- 닫기 버튼에 aria-label 필수

### 브랜드 적용

- [minimal+precise] feedback: 아이콘+텍스트 조합, 색상 배경 최소화 + 명확한 상태 구분, 진행률/결과를 수치로 표시
- [minimal+precise] motion: 80-120ms, 거의 즉각적 + 120-180ms, 군더더기 없는 전환
- [minimal+precise] color: monochrome 기반, accent 최소화 + 정확한 semantic 분리, 모호한 중간 톤 지양
- [금지] (editorial) hover: 텍스트 underline 또는 color shift, 장식적 효과 없음 — 이것을 피할 것
- [금지] (editorial) motion: 콘텐츠 전환 위주, UI chrome 모션 최소화 — 이것을 피할 것

### 레퍼런스 근거

- **Carbon Design System**: We welcome all feedback, designs, or ideas in order to produce the best possible experience for our users. If you're interested in contributing, ch...
- **Primer**: CircleBadge CircleBadge visually connects logos of third-party services, eg. in the marketplace.

### 구현 노트

- 기존에 같은 역할의 컴포넌트가 있으면 토큰 교체부터 시작
- variant prop으로 시각적 변형을 관리 (하드코딩 금지)
- auto-dismiss 시간은 내용 길이에 비례 (기본 5초)
- 반응형 검증: 320px, 360px, 390px, 430px에서 control overflow와 viewport horizontal scroll이 없어야 함
- action row는 narrow viewport에서 `flex-wrap: wrap` 또는 세로 stack으로 전환하고, overflow-x 숨김으로 문제를 덮지 않음

---

## feedback / status-dot

**역할**: Small operational status indicator paired with visible text.

**탐지 출처**: astryx-geist-reference-baseline

### 구조 (Anatomy)

- container
- icon
- message
- action(optional)
- close-button(optional)

### 상태 (States)

| 상태 | 설명 |
|------|------|
| `info` | 정보 알림 |
| `success` | 성공 알림 |
| `warning` | 경고 알림 |
| `danger` | 에러/위험 알림 |

### 토큰 바인딩

```
surface: var(--color-surface-muted)
text: var(--color-text)
icon: var(--color-info)
border: var(--color-border)
radius: var(--radius-sm)
padding: var(--space-12) var(--space-16)
severity-info: var(--color-info)
severity-success: var(--color-success)
severity-warning: var(--color-warning)
severity-danger: var(--color-danger)
```

### 접근성

- role="alert" for urgent messages
- role="status" for non-urgent
- aria-live="polite" or "assertive"
- 닫기 버튼에 aria-label 필수

### 브랜드 적용

- [minimal+precise] feedback: 아이콘+텍스트 조합, 색상 배경 최소화 + 명확한 상태 구분, 진행률/결과를 수치로 표시
- [minimal+precise] motion: 80-120ms, 거의 즉각적 + 120-180ms, 군더더기 없는 전환
- [minimal+precise] color: monochrome 기반, accent 최소화 + 정확한 semantic 분리, 모호한 중간 톤 지양
- [금지] (editorial) hover: 텍스트 underline 또는 color shift, 장식적 효과 없음 — 이것을 피할 것
- [금지] (editorial) motion: 콘텐츠 전환 위주, UI chrome 모션 최소화 — 이것을 피할 것

### Visual Adaptation Hints

- **card_elevation_tendency**: 카드는 거의 무그림자 평면으로 유지하고 tint/divider로 계층을 만든다. 압축된 spacing에서도 header/body/footer 구획은 divider나 tint로 유지한다. (source=cards; confidence=0.29; provenance=inferred; direction=flat card planes를 기본으로 하고, 압축된 spacing과 얇은 divider 중심의 hierarchy. 중간 반경으로 제품 UI 절제 유지.; evidence=surface=flat, density=dense, corner=medium)
- **border_vs_fill_emphasis**: fill 중심이다. neutral surface를 기본으로 하고 border는 상태 변화나 구획 보조에만 쓴다. (source=cards; confidence=0.29; provenance=inferred; direction=flat card planes를 기본으로 하고, 압축된 spacing과 얇은 divider 중심의 hierarchy. 중간 반경으로 제품 UI 절제 유지.; evidence=surface=flat, density=dense, corner=medium)
- **chart_panel_framing**: 차트 패널은 flush surface와 thin divider 중심으로 프레이밍한다. 헤더의 metric, controls, plot 영역을 분리하고 내부 여백은 촘촘하게 관리한다. (source=data_display; confidence=0.29; provenance=inferred; direction=정보 밀도를 유지하되 thin dividers와 restrained accent로 hierarchy를 만든다.; evidence=layout=dashboard-grid, density=dense, layout=data-review-surface, surface=flat)

### 레퍼런스 근거

- **Carbon Design System**: We welcome all feedback, designs, or ideas in order to produce the best possible experience for our users. If you're interested in contributing, ch...
- **Primer**: Messaging components are used to provide important and relevant information to the user, including feedback, contextual information, product update...

### 구현 노트

- 기존에 같은 역할의 컴포넌트가 있으면 토큰 교체부터 시작
- variant prop으로 시각적 변형을 관리 (하드코딩 금지)
- auto-dismiss 시간은 내용 길이에 비례 (기본 5초)
- 반응형 검증: 320px, 360px, 390px, 430px에서 control overflow와 viewport horizontal scroll이 없어야 함
- action row는 narrow viewport에서 `flex-wrap: wrap` 또는 세로 stack으로 전환하고, overflow-x 숨김으로 문제를 덮지 않음

---

## overlay / tooltip

**역할**: Short accessible explanation for icon-only or compact controls.

**탐지 출처**: astryx-geist-reference-baseline

### 구조 (Anatomy)

- backdrop
- container
- header
- content
- footer(optional)
- close-button

### 상태 (States)

| 상태 | 설명 |
|------|------|
| `closed` | 닫힌 상태 |
| `opening` | 열리는 중 (전환 애니메이션) |
| `open` | 열린 상태 |
| `closing` | 닫히는 중 |

### 토큰 바인딩

```
surface: var(--color-surface-elevated)
backdrop: rgb(0 0 0 / 0.5)
radius: var(--radius-lg)
padding: var(--space-24)
border: var(--color-border)
motion: opacity var(--duration-180) var(--ease-standard)
```

### 접근성

- role="dialog" with aria-modal="true"
- focus trap (Tab 순환)
- Escape로 닫기
- aria-labelledby로 제목 연결
- 닫은 후 trigger 요소로 포커스 복귀

### 브랜드 적용

- [minimal+precise] motion: 80-120ms, 거의 즉각적 + 120-180ms, 군더더기 없는 전환
- [minimal+precise] density: compact 가능, 불필요한 여백 제거 + 엄격한 spacing scale 준수, 임의 값 금지
- [금지] (editorial) hover: 텍스트 underline 또는 color shift, 장식적 효과 없음 — 이것을 피할 것
- [금지] (editorial) motion: 콘텐츠 전환 위주, UI chrome 모션 최소화 — 이것을 피할 것

### 레퍼런스 근거

- **Carbon Design System**: We’re also using this release to address some of the outstanding accessibility issues for components like Notification and Tooltip along with consi...
- **Primer**: Tooltip Tooltips add additional context to interactive UI elements and appear on mouse hover or keyboard focus.

### 구현 노트

- 기존에 같은 역할의 컴포넌트가 있으면 토큰 교체부터 시작
- variant prop으로 시각적 변형을 관리 (하드코딩 금지)
- Escape / backdrop click으로 닫기, 열 때 첫 focusable 요소로 이동

---

## copilot-artifact / source-card

**역할**: Compact source record card with title, excerpt, metadata, and verification state

**Slot archetype**: `advanced:source-card`

### Advanced Usage

Use when:
- AI output depends on external or internal source records
- users need a repeatable citation preview component
Avoid when:
- source metadata is unavailable
Pairs with: citation-drawer, evidence-graph, inline-citation

### 구조 (Anatomy)

- card
- source-title
- excerpt
- metadata-row
- verification-badge
- open-action

### 상태 (States)

| 상태 | 설명 |
|------|------|
| `default` | 기본 상태 |
| `hover` | 마우스 오버 시 |
| `verified` | verified |
| `stale` | stale |
| `unavailable` | unavailable |

### 토큰 바인딩

```
surface: var(--color-surface)
border: var(--color-border)
verified: var(--color-success)
stale: var(--color-warning)
radius: var(--radius-md)
```

### 접근성

- source title is a heading or labelled link
- excerpt length is bounded and not a full copyrighted passage
- verification state includes text

### 브랜드 적용

- [minimal+precise] hover: 미세한 opacity 또는 underline만 + 정확한 border/outline 변화
- [minimal+precise] motion: 80-120ms, 거의 즉각적 + 120-180ms, 군더더기 없는 전환
- [minimal+precise] color: monochrome 기반, accent 최소화 + 정확한 semantic 분리, 모호한 중간 톤 지양
- [금지] (editorial) hover: 텍스트 underline 또는 color shift, 장식적 효과 없음 — 이것을 피할 것
- [금지] (editorial) motion: 콘텐츠 전환 위주, UI chrome 모션 최소화 — 이것을 피할 것

### Visual Adaptation Hints

- **card_elevation_tendency**: 카드는 거의 무그림자 평면으로 유지하고 tint/divider로 계층을 만든다. 압축된 spacing에서도 header/body/footer 구획은 divider나 tint로 유지한다. (source=cards; confidence=0.29; provenance=inferred; direction=flat card planes를 기본으로 하고, 압축된 spacing과 얇은 divider 중심의 hierarchy. 중간 반경으로 제품 UI 절제 유지.; evidence=surface=flat, density=dense, corner=medium)
- **border_vs_fill_emphasis**: fill 중심이다. neutral surface를 기본으로 하고 border는 상태 변화나 구획 보조에만 쓴다. (source=cards; confidence=0.29; provenance=inferred; direction=flat card planes를 기본으로 하고, 압축된 spacing과 얇은 divider 중심의 hierarchy. 중간 반경으로 제품 UI 절제 유지.; evidence=surface=flat, density=dense, corner=medium)

### 구현 노트

- 기존에 같은 역할의 컴포넌트가 있으면 토큰 교체부터 시작
- variant prop으로 시각적 변형을 관리 (하드코딩 금지)

---

## document / redline-viewer

**역할**: Review-oriented prose surface with suggested insertions, deletions, and comments

**Slot archetype**: `advanced:redline-viewer`

### Advanced Usage

Use when:
- legal, compliance, or editorial text needs reviewer markup
- comments must stay anchored to exact text ranges
Avoid when:
- structured rows are more important than prose
Pairs with: diff-viewer, comment-thread, approval-rail

### 구조 (Anatomy)

- reading-pane
- marked-text
- comment-anchor
- comment-margin
- resolve-action

### 상태 (States)

| 상태 | 설명 |
|------|------|
| `default` | 기본 상태 |
| `selected` | selected |
| `commenting` | commenting |
| `resolved` | resolved |

### 토큰 바인딩

```
surface: var(--color-surface)
mark-surface: var(--color-surface-tint)
comment-border: var(--color-border)
accent: var(--color-brand-accent)
radius: var(--radius-md)
```

### 접근성

- marked ranges expose aria-describedby to comment text
- resolved comments remain reachable from audit history
- keyboard can move between comment anchors

### 브랜드 적용

- [minimal+precise] hover: 미세한 opacity 또는 underline만 + 정확한 border/outline 변화
- [minimal+precise] motion: 80-120ms, 거의 즉각적 + 120-180ms, 군더더기 없는 전환
- [minimal+precise] color: monochrome 기반, accent 최소화 + 정확한 semantic 분리, 모호한 중간 톤 지양
- [금지] (editorial) hover: 텍스트 underline 또는 color shift, 장식적 효과 없음 — 이것을 피할 것
- [금지] (editorial) motion: 콘텐츠 전환 위주, UI chrome 모션 최소화 — 이것을 피할 것

### Visual Adaptation Hints

- **operational_surface_role**: 주 작업 표면은 card wall이 아니라 table/list/rail/canvas 계열로 설계한다. 압축된 표면에서는 row height, column rhythm, sticky toolbar, source/update label을 우선한다. (source=data_display; confidence=0.29; provenance=inferred; direction=정보 밀도를 유지하되 thin dividers와 restrained accent로 hierarchy를 만든다.; evidence=layout=dashboard-grid, density=dense, layout=data-review-surface)

### 레퍼런스 근거

- **Carbon Design System**: AI chat is a conversational framework between a user and an AI that can aid in creating tasks, finding insights, tracking documents, and more. For ...
- **Primer**: The GitHub Design Infrastructure and Design Engineering teams build and maintain Primer — this includes our CSS framework, style guide documentatio...

### 구현 노트

- 기존에 같은 역할의 컴포넌트가 있으면 토큰 교체부터 시작
- variant prop으로 시각적 변형을 관리 (하드코딩 금지)

---

## workflow / approval-rail

**역할**: Persistent approval state rail with owners, blockers, and next action

**Slot archetype**: `advanced:approval-rail`

### Advanced Usage

Use when:
- work requires review, approval, rejection, or handoff
- users need to know who owns the next decision
Avoid when:
- there is no explicit workflow owner or state
Pairs with: policy-matrix, risk-summary-card, diff-viewer

### 구조 (Anatomy)

- rail
- stage-item
- owner-chip
- blocker-list
- primary-action
- secondary-action

### 상태 (States)

| 상태 | 설명 |
|------|------|
| `pending` | pending |
| `active` | 클릭/탭 중 |
| `blocked` | blocked |
| `approved` | approved |
| `rejected` | rejected |

### 토큰 바인딩

```
surface: var(--color-surface)
border: var(--color-border)
active: var(--color-brand-primary)
blocked: var(--color-warning)
approved: var(--color-success)
radius: var(--radius-lg)
```

### 접근성

- current stage uses aria-current="step"
- actions are real buttons with disabled/loading states
- blocked reasons are visible text, not color alone

### 브랜드 적용

- [minimal+precise] hover: 미세한 opacity 또는 underline만 + 정확한 border/outline 변화
- [minimal+precise] motion: 80-120ms, 거의 즉각적 + 120-180ms, 군더더기 없는 전환
- [minimal+precise] color: monochrome 기반, accent 최소화 + 정확한 semantic 분리, 모호한 중간 톤 지양
- [금지] (editorial) hover: 텍스트 underline 또는 color shift, 장식적 효과 없음 — 이것을 피할 것
- [금지] (editorial) motion: 콘텐츠 전환 위주, UI chrome 모션 최소화 — 이것을 피할 것

### Visual Adaptation Hints

- **operational_surface_role**: 주 작업 표면은 card wall이 아니라 table/list/rail/canvas 계열로 설계한다. 압축된 표면에서는 row height, column rhythm, sticky toolbar, source/update label을 우선한다. (source=data_display; confidence=0.29; provenance=inferred; direction=정보 밀도를 유지하되 thin dividers와 restrained accent로 hierarchy를 만든다.; evidence=layout=dashboard-grid, density=dense, layout=data-review-surface)

### 레퍼런스 근거

- **Carbon Design System**: Bringing IBM Carbon Design System Knowledge Into AI Workflows With Carbon MCP Will Scott, PhD
- **Primer**: Design guidelines covering common user workflows. Octicons

### 구현 노트

- 기존에 같은 역할의 컴포넌트가 있으면 토큰 교체부터 시작
- variant prop으로 시각적 변형을 관리 (하드코딩 금지)

---

## copilot-artifact / citation-drawer

**역할**: Source and citation drawer for AI answers, policies, and quoted evidence

**Slot archetype**: `advanced:citation-drawer`

### Advanced Usage

Use when:
- answers must show supporting policy, document, or source records
- users need to inspect evidence without losing conversation context
Avoid when:
- citations are static footnotes only
Pairs with: inline-citation, source-card, evidence-graph

### 구조 (Anatomy)

- drawer
- source-list
- source-card
- quote-snippet
- metadata-row
- open-source-action

### 상태 (States)

| 상태 | 설명 |
|------|------|
| `closed` | 닫힌 상태 |
| `open` | 열린 상태 |
| `loading` | 로딩 중 (스피너 표시) |
| `empty` | 데이터 없음 |
| `verified` | verified |

### 토큰 바인딩

```
surface: var(--color-surface-elevated)
source-surface: var(--color-surface)
border: var(--color-border)
verified: var(--color-success)
radius: var(--radius-lg)
```

### 접근성

- each citation has a stable label and source title
- snippets are summaries unless licensing permits direct quote
- drawer focus order follows source ranking

### 브랜드 적용

- [minimal+precise] hover: 미세한 opacity 또는 underline만 + 정확한 border/outline 변화
- [minimal+precise] motion: 80-120ms, 거의 즉각적 + 120-180ms, 군더더기 없는 전환
- [minimal+precise] color: monochrome 기반, accent 최소화 + 정확한 semantic 분리, 모호한 중간 톤 지양
- [금지] (editorial) hover: 텍스트 underline 또는 color shift, 장식적 효과 없음 — 이것을 피할 것
- [금지] (editorial) motion: 콘텐츠 전환 위주, UI chrome 모션 최소화 — 이것을 피할 것

### 구현 노트

- 기존에 같은 역할의 컴포넌트가 있으면 토큰 교체부터 시작
- variant prop으로 시각적 변형을 관리 (하드코딩 금지)

---

## document / diff-viewer

**역할**: Before/after document comparison with inline additions and removals

**Slot archetype**: `advanced:diff-viewer`

### Advanced Usage

Use when:
- AI rewrites, policy edits, or reviewer changes need auditability
- users must approve what changed before publishing
Avoid when:
- only a short status message changed
Pairs with: redline-viewer, revision-timeline, approval-rail

### 구조 (Anatomy)

- container
- version-header
- line-list
- change-marker
- gutter
- summary-footer

### 상태 (States)

| 상태 | 설명 |
|------|------|
| `default` | 기본 상태 |
| `side-by-side` | side-by-side |
| `inline` | inline |
| `collapsed-context` | collapsed-context |

### 토큰 바인딩

```
surface: var(--color-surface)
border: var(--color-border)
added: var(--color-success)
removed: var(--color-danger)
muted-surface: var(--color-surface-muted)
font: var(--font-body)
mono: var(--font-mono)
```

### 접근성

- changes are announced with text labels, not color alone
- line numbers are decorative unless referenced by controls
- keyboard shortcuts have visible command alternatives

### 브랜드 적용

- [minimal+precise] hover: 미세한 opacity 또는 underline만 + 정확한 border/outline 변화
- [minimal+precise] motion: 80-120ms, 거의 즉각적 + 120-180ms, 군더더기 없는 전환
- [minimal+precise] color: monochrome 기반, accent 최소화 + 정확한 semantic 분리, 모호한 중간 톤 지양
- [금지] (editorial) hover: 텍스트 underline 또는 color shift, 장식적 효과 없음 — 이것을 피할 것
- [금지] (editorial) motion: 콘텐츠 전환 위주, UI chrome 모션 최소화 — 이것을 피할 것

### Visual Adaptation Hints

- **operational_surface_role**: 주 작업 표면은 card wall이 아니라 table/list/rail/canvas 계열로 설계한다. 압축된 표면에서는 row height, column rhythm, sticky toolbar, source/update label을 우선한다. (source=data_display; confidence=0.29; provenance=inferred; direction=정보 밀도를 유지하되 thin dividers와 restrained accent로 hierarchy를 만든다.; evidence=layout=dashboard-grid, density=dense, layout=data-review-surface)

### 레퍼런스 근거

- **Carbon Design System**: AI chat is a conversational framework between a user and an AI that can aid in creating tasks, finding insights, tracking documents, and more. For ...
- **Primer**: The GitHub Design Infrastructure and Design Engineering teams build and maintain Primer — this includes our CSS framework, style guide documentatio...

### 구현 노트

- 기존에 같은 역할의 컴포넌트가 있으면 토큰 교체부터 시작
- variant prop으로 시각적 변형을 관리 (하드코딩 금지)

---

## input / reviewer-assignment-picker

**역할**: Reviewer picker with role, availability, and escalation hints

**Slot archetype**: `advanced:reviewer-assignment-picker`

### Advanced Usage

Use when:
- workflows require human approval or reassignment
- reviewer choice depends on policy ownership or availability
Avoid when:
- there is only one fixed reviewer
Pairs with: approval-rail, exception-queue, presence-indicator

### 구조 (Anatomy)

- field
- selected-reviewer-chip
- candidate-list
- availability
- role-label
- escalation-note

### 상태 (States)

| 상태 | 설명 |
|------|------|
| `default` | 기본 상태 |
| `searching` | searching |
| `selected` | selected |
| `unavailable` | unavailable |
| `error` | 유효성 검증 실패 |

### 토큰 바인딩

```
surface: var(--color-surface)
chip-surface: var(--color-surface-tint)
border: var(--color-border)
focus: var(--color-brand-primary)
radius: var(--radius-md)
```

### 접근성

- combobox pattern for searchable reviewer list
- selected reviewers can be removed by keyboard
- availability is announced as text

### 브랜드 적용

- [minimal+precise] hover: 미세한 opacity 또는 underline만 + 정확한 border/outline 변화
- [minimal+precise] density: compact 가능, 불필요한 여백 제거 + 엄격한 spacing scale 준수, 임의 값 금지
- [minimal+precise] feedback: 아이콘+텍스트 조합, 색상 배경 최소화 + 명확한 상태 구분, 진행률/결과를 수치로 표시
- [금지] (editorial) hover: 텍스트 underline 또는 color shift, 장식적 효과 없음 — 이것을 피할 것
- [금지] (editorial) motion: 콘텐츠 전환 위주, UI chrome 모션 최소화 — 이것을 피할 것

### 레퍼런스 근거

- **Carbon Design System**: Number input Text input
- **Primer**: I worked in data visualization and map-making for most of my career, and solving design problems with data is my jam. To me there's something uniqu...

### 구현 노트

- 기존에 같은 역할의 컴포넌트가 있으면 토큰 교체부터 시작
- variant prop으로 시각적 변형을 관리 (하드코딩 금지)
- error 상태에서 helper text → error message로 자동 전환
- label은 항상 visible (placeholder만으로 대체 금지)
- 반응형 검증: 320px, 360px, 390px, 430px에서 control overflow와 viewport horizontal scroll이 없어야 함
- action row는 narrow viewport에서 `flex-wrap: wrap` 또는 세로 stack으로 전환하고, overflow-x 숨김으로 문제를 덮지 않음

---

## data-display / bulk-action-table

**역할**: Selectable data table with sticky bulk action affordances

**Slot archetype**: `advanced:bulk-action-table`

### Advanced Usage

Use when:
- users handle many records at once
- selection count and destructive actions must stay visible
Avoid when:
- records are read-only or single-action
Pairs with: saved-view-bar, filter-builder, exception-queue

### 구조 (Anatomy)

- table
- selection-cell
- column-header
- row
- bulk-action-bar
- pagination

### 상태 (States)

| 상태 | 설명 |
|------|------|
| `default` | 기본 상태 |
| `selected` | selected |
| `filtered` | 필터 적용됨 |
| `sorted` | 정렬 적용됨 |
| `empty` | 데이터 없음 |

### 토큰 바인딩

```
surface: var(--color-surface)
row-hover: var(--color-surface-muted)
selected: var(--color-surface-tint)
border: var(--color-border)
font: var(--font-body)
```

### 접근성

- header checkbox exposes mixed state when partially selected
- selection count is announced when it changes
- bulk action bar appears after selection in logical focus order

### 브랜드 적용

- [minimal+precise] density: compact 가능, 불필요한 여백 제거 + 엄격한 spacing scale 준수, 임의 값 금지
- [minimal+precise] color: monochrome 기반, accent 최소화 + 정확한 semantic 분리, 모호한 중간 톤 지양
- [금지] (editorial) hover: 텍스트 underline 또는 color shift, 장식적 효과 없음 — 이것을 피할 것
- [금지] (editorial) motion: 콘텐츠 전환 위주, UI chrome 모션 최소화 — 이것을 피할 것

### Visual Adaptation Hints

- **operational_surface_role**: 주 작업 표면은 card wall이 아니라 table/list/rail/canvas 계열로 설계한다. 압축된 표면에서는 row height, column rhythm, sticky toolbar, source/update label을 우선한다. (source=data_display; confidence=0.29; provenance=inferred; direction=정보 밀도를 유지하되 thin dividers와 restrained accent로 hierarchy를 만든다.; evidence=layout=dashboard-grid, density=dense, layout=data-review-surface)
- **filter_nav_density**: filter/nav density는 compact하다. chip, scope, pagination을 촘촘하게 묶되 의미 단위별 group은 분리한다. (source=navigation; confidence=0.23; provenance=inferred; direction=고정 sidebar 또는 split-pane navigation을 우선하고, 현재 위치와 scope를 항상 명시한다.; evidence=Split-pane workspace, layout=data-review-surface, density=dense)
- **chart_panel_framing**: 차트 패널은 flush surface와 thin divider 중심으로 프레이밍한다. 헤더의 metric, controls, plot 영역을 분리하고 내부 여백은 촘촘하게 관리한다. (source=data_display; confidence=0.29; provenance=inferred; direction=정보 밀도를 유지하되 thin dividers와 restrained accent로 hierarchy를 만든다.; evidence=layout=dashboard-grid, density=dense, layout=data-review-surface, surface=flat)

### 구현 노트

- 기존에 같은 역할의 컴포넌트가 있으면 토큰 교체부터 시작
- variant prop으로 시각적 변형을 관리 (하드코딩 금지)
- 빈 상태(empty-state)와 에러 상태를 반드시 처리
- 좁은 UI 텍스트는 Pretendard 기준 label line-height 1.4-1.5를 참고해 뭉침을 방지
- 반응형 검증: 320px, 360px, 390px, 430px에서 control overflow와 viewport horizontal scroll이 없어야 함
- action row는 narrow viewport에서 `flex-wrap: wrap` 또는 세로 stack으로 전환하고, overflow-x 숨김으로 문제를 덮지 않음

---

## data-display / evidence-graph

**역할**: Node-link evidence map connecting claims, sources, policies, and decisions

**Slot archetype**: `advanced:evidence-graph`

### Advanced Usage

Use when:
- trust depends on seeing relationships between claims and sources
- auditors need to trace why an answer or decision was made
Avoid when:
- a simple source list communicates the relationship
Pairs with: citation-drawer, decision-record-card, policy-matrix

### 구조 (Anatomy)

- graph-canvas
- node
- edge
- legend
- selection-detail
- zoom-control

### 상태 (States)

| 상태 | 설명 |
|------|------|
| `default` | 기본 상태 |
| `focused` | focused |
| `filtered` | 필터 적용됨 |
| `empty` | 데이터 없음 |

### 토큰 바인딩

```
surface: var(--color-surface)
node-surface: var(--color-surface-muted)
edge: var(--color-border-strong)
active: var(--color-brand-primary)
radius: var(--radius-md)
```

### 접근성

- graph has a table/list fallback with the same relationships
- selected node detail is announced in a live region
- zoom controls are buttons with visible labels

### 브랜드 적용

- [minimal+precise] density: compact 가능, 불필요한 여백 제거 + 엄격한 spacing scale 준수, 임의 값 금지
- [minimal+precise] color: monochrome 기반, accent 최소화 + 정확한 semantic 분리, 모호한 중간 톤 지양
- [금지] (editorial) hover: 텍스트 underline 또는 color shift, 장식적 효과 없음 — 이것을 피할 것
- [금지] (editorial) motion: 콘텐츠 전환 위주, UI chrome 모션 최소화 — 이것을 피할 것

### Visual Adaptation Hints

- **card_elevation_tendency**: 카드는 거의 무그림자 평면으로 유지하고 tint/divider로 계층을 만든다. 압축된 spacing에서도 header/body/footer 구획은 divider나 tint로 유지한다. (source=cards; confidence=0.29; provenance=inferred; direction=flat card planes를 기본으로 하고, 압축된 spacing과 얇은 divider 중심의 hierarchy. 중간 반경으로 제품 UI 절제 유지.; evidence=surface=flat, density=dense, corner=medium)
- **border_vs_fill_emphasis**: fill 중심이다. neutral surface를 기본으로 하고 border는 상태 변화나 구획 보조에만 쓴다. (source=cards; confidence=0.29; provenance=inferred; direction=flat card planes를 기본으로 하고, 압축된 spacing과 얇은 divider 중심의 hierarchy. 중간 반경으로 제품 UI 절제 유지.; evidence=surface=flat, density=dense, corner=medium)
- **chart_panel_framing**: 차트 패널은 flush surface와 thin divider 중심으로 프레이밍한다. 헤더의 metric, controls, plot 영역을 분리하고 내부 여백은 촘촘하게 관리한다. (source=data_display; confidence=0.29; provenance=inferred; direction=정보 밀도를 유지하되 thin dividers와 restrained accent로 hierarchy를 만든다.; evidence=layout=dashboard-grid, density=dense, layout=data-review-surface, surface=flat)

### 구현 노트

- 기존에 같은 역할의 컴포넌트가 있으면 토큰 교체부터 시작
- variant prop으로 시각적 변형을 관리 (하드코딩 금지)
- 빈 상태(empty-state)와 에러 상태를 반드시 처리
- 좁은 UI 텍스트는 Pretendard 기준 label line-height 1.4-1.5를 참고해 뭉침을 방지
