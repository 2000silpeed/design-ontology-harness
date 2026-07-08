# ColorFit Component Specs

총 70개 컴포넌트 | 패밀리: button, data-display, document, feedback, input, navigation, overlay, workflow

## 구현 원칙 (Non-negotiable)

이 스펙의 모든 컴포넌트를 구현할 때 반드시 지킨다:

1. **이모지를 UI로 쓰지 않는다** — 🎨 ✅ 🔥 ⚡ 🚀 ❌ ⭐ 📊 등 이모지를 아이콘, 상태 표시, 버튼 장식, 네비게이션 지표 자리에 절대 넣지 않는다. 리팩토링 중 카드/버튼/배지/탭/상태 UI에서 이모지를 발견하면 SVG 파일, SVG 컴포넌트, 또는 Lucide/Heroicons/Phosphor/Tabler 같은 아이콘 라이브러리로 교체한다.
2. **컴포넌트를 직접 구현한다** — 아래 각 컴포넌트의 anatomy(구조), states(상태), 토큰 바인딩, 접근성 규칙을 그대로 따라 완전하게 구현한다. '임시', 'TODO', '플레이스홀더' 같은 반쪽 구현을 남기지 않는다.
3. **라이브러리 기본 스타일 금지** — 라이브러리 컴포넌트를 그대로 import해서 쓰지 않는다. 반드시 디자인 토큰(--color-*, --space-*, --radius-*, --font-*)으로 스타일을 명시적으로 바인딩한다.
4. **접근성은 옵션이 아니다** — 각 컴포넌트의 '접근성' 섹션에 정의된 role, aria-*, label, focus 관리 규칙을 전부 적용한다.
5. **hex 값 하드코딩 금지** — 색상은 반드시 semantic token을 경유한다 (예: `color: var(--color-ink)` not `color: #2C2C2C`).
6. **모바일 overflow 금지** — 버튼, CTA, 탭, 필터칩, 툴바 액션은 320px viewport에서 화면 밖으로 나가면 안 된다. fixed/min-width px 값으로 폭을 고정하지 말고 wrap/stack fallback을 제공한다.

## 브랜드 적용 규칙

- **hover**: 텍스트 underline 또는 color shift, 장식적 효과 없음 + 정확한 border/outline 변화 + 예측 가능하고 일관된 hover 패턴
- **motion**: 콘텐츠 전환 위주, UI chrome 모션 최소화 + 120-180ms, 군더더기 없는 전환 + 모든 전환에 동일한 easing/duration
- **color**: 타이포그래피로 위계 형성, 컬러보다 weight/size 활용 + 정확한 semantic 분리, 모호한 중간 톤 지양 + 안정적인 neutral 기반, 과한 accent 변화 없음
- **density**: 넉넉한 line-height와 margin, 읽기 편한 간격 + 엄격한 spacing scale 준수, 임의 값 금지 + 기존 레이아웃 유지, 갑작스런 위치 변경 없음
- **feedback**: 콘텐츠 맥락 안에서 인라인 표시, 토스트보다 인라인 선호 + 명확한 상태 구분, 진행률/결과를 수치로 표시 + 결과를 반드시 확인, 실패 시 복구 방법 안내

## Typography Guardrails

- 한글 기반 제품은 line-break / scale / tracking을 영문 랜딩 기본값으로 처리하지 않고, 아래 가드레일을 구현 기본값으로 사용한다.
- Headline: Noto Serif KR | line-height 1.2-1.4 | tracking -0.02em
- Body: Pretendard | line-height 1.6-1.7 | label line-height 1.4-1.5
- Wrap defaults: headline word-break=keep-all, headline text-wrap=balance, body word-break=keep-all
- Scale guidance: 한글 hero/section heading은 영문 시안보다 한 단계 작은 스케일에서 시작해 wrap을 확인한 뒤 확장한다.
- Hangul display safety: line-height >= 1.08 | tracking -0.03em to 0em | forced <br /> 금지 until breakpoint QA
- 한글 카피는 `word-break: keep-all`과 `overflow-wrap: normal`을 기본값으로 두고, 주요 헤딩에서 지원되면 `text-wrap: balance`를 사용한다.
- 한글 헤딩에는 breakpoint 검증 전 강제 `<br />`를 넣지 않는다. 줄바꿈이 필요하면 먼저 컨테이너 폭과 type scale을 조정한다.
- 한글 화면은 영문 시안의 `ch` 기준이나 single-line slogan 가정에 맞추지 말고, 실제 한글 문장으로 wrap을 검증한다.
- 폭이 넓은 한글 또는 명조 헤딩은 영문 hero보다 한 단계 작은 display scale에서 시작하고, 줄바꿈이 안정적일 때만 키운다.

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

- [editorial+precise+trustworthy] hover: 텍스트 underline 또는 color shift, 장식적 효과 없음 + 정확한 border/outline 변화 + 예측 가능하고 일관된 hover 패턴
- [editorial+precise+trustworthy] motion: 콘텐츠 전환 위주, UI chrome 모션 최소화 + 120-180ms, 군더더기 없는 전환 + 모든 전환에 동일한 easing/duration
- [editorial+precise+trustworthy] color: 타이포그래피로 위계 형성, 컬러보다 weight/size 활용 + 정확한 semantic 분리, 모호한 중간 톤 지양 + 안정적인 neutral 기반, 과한 accent 변화 없음

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
- 텍스트 위계가 핵심 — 컬러보다 weight/size로 구분

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

- [editorial+precise+trustworthy] hover: 텍스트 underline 또는 color shift, 장식적 효과 없음 + 정확한 border/outline 변화 + 예측 가능하고 일관된 hover 패턴
- [editorial+precise+trustworthy] motion: 콘텐츠 전환 위주, UI chrome 모션 최소화 + 120-180ms, 군더더기 없는 전환 + 모든 전환에 동일한 easing/duration
- [editorial+precise+trustworthy] color: 타이포그래피로 위계 형성, 컬러보다 weight/size 활용 + 정확한 semantic 분리, 모호한 중간 톤 지양 + 안정적인 neutral 기반, 과한 accent 변화 없음

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
- 텍스트 위계가 핵심 — 컬러보다 weight/size로 구분

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

- [editorial+precise+trustworthy] hover: 텍스트 underline 또는 color shift, 장식적 효과 없음 + 정확한 border/outline 변화 + 예측 가능하고 일관된 hover 패턴
- [editorial+precise+trustworthy] motion: 콘텐츠 전환 위주, UI chrome 모션 최소화 + 120-180ms, 군더더기 없는 전환 + 모든 전환에 동일한 easing/duration
- [editorial+precise+trustworthy] color: 타이포그래피로 위계 형성, 컬러보다 weight/size 활용 + 정확한 semantic 분리, 모호한 중간 톤 지양 + 안정적인 neutral 기반, 과한 accent 변화 없음

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
- 텍스트 위계가 핵심 — 컬러보다 weight/size로 구분

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

- [editorial+precise+trustworthy] density: 넉넉한 line-height와 margin, 읽기 편한 간격 + 엄격한 spacing scale 준수, 임의 값 금지 + 기존 레이아웃 유지, 갑작스런 위치 변경 없음
- [editorial+precise+trustworthy] color: 타이포그래피로 위계 형성, 컬러보다 weight/size 활용 + 정확한 semantic 분리, 모호한 중간 톤 지양 + 안정적인 neutral 기반, 과한 accent 변화 없음

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
- 텍스트 위계가 핵심 — 컬러보다 weight/size로 구분

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

- [editorial+precise+trustworthy] density: 넉넉한 line-height와 margin, 읽기 편한 간격 + 엄격한 spacing scale 준수, 임의 값 금지 + 기존 레이아웃 유지, 갑작스런 위치 변경 없음
- [editorial+precise+trustworthy] color: 타이포그래피로 위계 형성, 컬러보다 weight/size 활용 + 정확한 semantic 분리, 모호한 중간 톤 지양 + 안정적인 neutral 기반, 과한 accent 변화 없음

### 구현 노트

- 기존에 같은 역할의 컴포넌트가 있으면 토큰 교체부터 시작
- variant prop으로 시각적 변형을 관리 (하드코딩 금지)
- 빈 상태(empty-state)와 에러 상태를 반드시 처리
- 좁은 UI 텍스트는 Pretendard 기준 label line-height 1.4-1.5를 참고해 뭉침을 방지
- 텍스트 위계가 핵심 — 컬러보다 weight/size로 구분

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

- [editorial+precise+trustworthy] density: 넉넉한 line-height와 margin, 읽기 편한 간격 + 엄격한 spacing scale 준수, 임의 값 금지 + 기존 레이아웃 유지, 갑작스런 위치 변경 없음
- [editorial+precise+trustworthy] color: 타이포그래피로 위계 형성, 컬러보다 weight/size 활용 + 정확한 semantic 분리, 모호한 중간 톤 지양 + 안정적인 neutral 기반, 과한 accent 변화 없음

### 구현 노트

- 기존에 같은 역할의 컴포넌트가 있으면 토큰 교체부터 시작
- variant prop으로 시각적 변형을 관리 (하드코딩 금지)
- 빈 상태(empty-state)와 에러 상태를 반드시 처리
- 좁은 UI 텍스트는 Pretendard 기준 label line-height 1.4-1.5를 참고해 뭉침을 방지
- 텍스트 위계가 핵심 — 컬러보다 weight/size로 구분

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

- [editorial+precise+trustworthy] hover: 텍스트 underline 또는 color shift, 장식적 효과 없음 + 정확한 border/outline 변화 + 예측 가능하고 일관된 hover 패턴
- [editorial+precise+trustworthy] density: 넉넉한 line-height와 margin, 읽기 편한 간격 + 엄격한 spacing scale 준수, 임의 값 금지 + 기존 레이아웃 유지, 갑작스런 위치 변경 없음
- [editorial+precise+trustworthy] motion: 콘텐츠 전환 위주, UI chrome 모션 최소화 + 120-180ms, 군더더기 없는 전환 + 모든 전환에 동일한 easing/duration

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
- 텍스트 위계가 핵심 — 컬러보다 weight/size로 구분

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

- [editorial+precise+trustworthy] hover: 텍스트 underline 또는 color shift, 장식적 효과 없음 + 정확한 border/outline 변화 + 예측 가능하고 일관된 hover 패턴
- [editorial+precise+trustworthy] density: 넉넉한 line-height와 margin, 읽기 편한 간격 + 엄격한 spacing scale 준수, 임의 값 금지 + 기존 레이아웃 유지, 갑작스런 위치 변경 없음
- [editorial+precise+trustworthy] feedback: 콘텐츠 맥락 안에서 인라인 표시, 토스트보다 인라인 선호 + 명확한 상태 구분, 진행률/결과를 수치로 표시 + 결과를 반드시 확인, 실패 시 복구 방법 안내

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
- 텍스트 위계가 핵심 — 컬러보다 weight/size로 구분

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

- [editorial+precise+trustworthy] hover: 텍스트 underline 또는 color shift, 장식적 효과 없음 + 정확한 border/outline 변화 + 예측 가능하고 일관된 hover 패턴
- [editorial+precise+trustworthy] density: 넉넉한 line-height와 margin, 읽기 편한 간격 + 엄격한 spacing scale 준수, 임의 값 금지 + 기존 레이아웃 유지, 갑작스런 위치 변경 없음
- [editorial+precise+trustworthy] feedback: 콘텐츠 맥락 안에서 인라인 표시, 토스트보다 인라인 선호 + 명확한 상태 구분, 진행률/결과를 수치로 표시 + 결과를 반드시 확인, 실패 시 복구 방법 안내

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
- 텍스트 위계가 핵심 — 컬러보다 weight/size로 구분

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

- [editorial+precise+trustworthy] hover: 텍스트 underline 또는 color shift, 장식적 효과 없음 + 정확한 border/outline 변화 + 예측 가능하고 일관된 hover 패턴
- [editorial+precise+trustworthy] density: 넉넉한 line-height와 margin, 읽기 편한 간격 + 엄격한 spacing scale 준수, 임의 값 금지 + 기존 레이아웃 유지, 갑작스런 위치 변경 없음
- [editorial+precise+trustworthy] feedback: 콘텐츠 맥락 안에서 인라인 표시, 토스트보다 인라인 선호 + 명확한 상태 구분, 진행률/결과를 수치로 표시 + 결과를 반드시 확인, 실패 시 복구 방법 안내

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
- 텍스트 위계가 핵심 — 컬러보다 weight/size로 구분

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

- [editorial+precise+trustworthy] hover: 텍스트 underline 또는 color shift, 장식적 효과 없음 + 정확한 border/outline 변화 + 예측 가능하고 일관된 hover 패턴
- [editorial+precise+trustworthy] density: 넉넉한 line-height와 margin, 읽기 편한 간격 + 엄격한 spacing scale 준수, 임의 값 금지 + 기존 레이아웃 유지, 갑작스런 위치 변경 없음
- [editorial+precise+trustworthy] feedback: 콘텐츠 맥락 안에서 인라인 표시, 토스트보다 인라인 선호 + 명확한 상태 구분, 진행률/결과를 수치로 표시 + 결과를 반드시 확인, 실패 시 복구 방법 안내

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
- 텍스트 위계가 핵심 — 컬러보다 weight/size로 구분

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

- [editorial+precise+trustworthy] hover: 텍스트 underline 또는 color shift, 장식적 효과 없음 + 정확한 border/outline 변화 + 예측 가능하고 일관된 hover 패턴
- [editorial+precise+trustworthy] density: 넉넉한 line-height와 margin, 읽기 편한 간격 + 엄격한 spacing scale 준수, 임의 값 금지 + 기존 레이아웃 유지, 갑작스런 위치 변경 없음
- [editorial+precise+trustworthy] feedback: 콘텐츠 맥락 안에서 인라인 표시, 토스트보다 인라인 선호 + 명확한 상태 구분, 진행률/결과를 수치로 표시 + 결과를 반드시 확인, 실패 시 복구 방법 안내

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
- 텍스트 위계가 핵심 — 컬러보다 weight/size로 구분

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

- [editorial+precise+trustworthy] hover: 텍스트 underline 또는 color shift, 장식적 효과 없음 + 정확한 border/outline 변화 + 예측 가능하고 일관된 hover 패턴
- [editorial+precise+trustworthy] density: 넉넉한 line-height와 margin, 읽기 편한 간격 + 엄격한 spacing scale 준수, 임의 값 금지 + 기존 레이아웃 유지, 갑작스런 위치 변경 없음
- [editorial+precise+trustworthy] feedback: 콘텐츠 맥락 안에서 인라인 표시, 토스트보다 인라인 선호 + 명확한 상태 구분, 진행률/결과를 수치로 표시 + 결과를 반드시 확인, 실패 시 복구 방법 안내

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
- 텍스트 위계가 핵심 — 컬러보다 weight/size로 구분

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

- [editorial+precise+trustworthy] hover: 텍스트 underline 또는 color shift, 장식적 효과 없음 + 정확한 border/outline 변화 + 예측 가능하고 일관된 hover 패턴
- [editorial+precise+trustworthy] density: 넉넉한 line-height와 margin, 읽기 편한 간격 + 엄격한 spacing scale 준수, 임의 값 금지 + 기존 레이아웃 유지, 갑작스런 위치 변경 없음
- [editorial+precise+trustworthy] feedback: 콘텐츠 맥락 안에서 인라인 표시, 토스트보다 인라인 선호 + 명확한 상태 구분, 진행률/결과를 수치로 표시 + 결과를 반드시 확인, 실패 시 복구 방법 안내

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
- 텍스트 위계가 핵심 — 컬러보다 weight/size로 구분

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

- [editorial+precise+trustworthy] hover: 텍스트 underline 또는 color shift, 장식적 효과 없음 + 정확한 border/outline 변화 + 예측 가능하고 일관된 hover 패턴
- [editorial+precise+trustworthy] motion: 콘텐츠 전환 위주, UI chrome 모션 최소화 + 120-180ms, 군더더기 없는 전환 + 모든 전환에 동일한 easing/duration
- [editorial+precise+trustworthy] color: 타이포그래피로 위계 형성, 컬러보다 weight/size 활용 + 정확한 semantic 분리, 모호한 중간 톤 지양 + 안정적인 neutral 기반, 과한 accent 변화 없음

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
- 텍스트 위계가 핵심 — 컬러보다 weight/size로 구분

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

- [editorial+precise+trustworthy] density: 넉넉한 line-height와 margin, 읽기 편한 간격 + 엄격한 spacing scale 준수, 임의 값 금지 + 기존 레이아웃 유지, 갑작스런 위치 변경 없음
- [editorial+precise+trustworthy] color: 타이포그래피로 위계 형성, 컬러보다 weight/size 활용 + 정확한 semantic 분리, 모호한 중간 톤 지양 + 안정적인 neutral 기반, 과한 accent 변화 없음

### 레퍼런스 근거

- **Carbon Design System**: Tag Date picker
- **Primer**: Primer color design tokens are made available within data-attribute selectors on the body tag or other high level dom element. There are three dist...

### 구현 노트

- 기존에 같은 역할의 컴포넌트가 있으면 토큰 교체부터 시작
- variant prop으로 시각적 변형을 관리 (하드코딩 금지)
- 빈 상태(empty-state)와 에러 상태를 반드시 처리
- 좁은 UI 텍스트는 Pretendard 기준 label line-height 1.4-1.5를 참고해 뭉침을 방지
- 텍스트 위계가 핵심 — 컬러보다 weight/size로 구분

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

- [editorial+precise+trustworthy] feedback: 콘텐츠 맥락 안에서 인라인 표시, 토스트보다 인라인 선호 + 명확한 상태 구분, 진행률/결과를 수치로 표시 + 결과를 반드시 확인, 실패 시 복구 방법 안내
- [editorial+precise+trustworthy] motion: 콘텐츠 전환 위주, UI chrome 모션 최소화 + 120-180ms, 군더더기 없는 전환 + 모든 전환에 동일한 easing/duration
- [editorial+precise+trustworthy] color: 타이포그래피로 위계 형성, 컬러보다 weight/size 활용 + 정확한 semantic 분리, 모호한 중간 톤 지양 + 안정적인 neutral 기반, 과한 accent 변화 없음

### 레퍼런스 근거

- **Carbon Design System**: We welcome all feedback, designs, or ideas in order to produce the best possible experience for our users. If you're interested in contributing, ch...
- **Primer**: Messaging components are used to provide important and relevant information to the user, including feedback, contextual information, product update...

### 구현 노트

- 기존에 같은 역할의 컴포넌트가 있으면 토큰 교체부터 시작
- variant prop으로 시각적 변형을 관리 (하드코딩 금지)
- auto-dismiss 시간은 내용 길이에 비례 (기본 5초)
- 반응형 검증: 320px, 360px, 390px, 430px에서 control overflow와 viewport horizontal scroll이 없어야 함
- action row는 narrow viewport에서 `flex-wrap: wrap` 또는 세로 stack으로 전환하고, overflow-x 숨김으로 문제를 덮지 않음
- 텍스트 위계가 핵심 — 컬러보다 weight/size로 구분

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

- [editorial+precise+trustworthy] hover: 텍스트 underline 또는 color shift, 장식적 효과 없음 + 정확한 border/outline 변화 + 예측 가능하고 일관된 hover 패턴
- [editorial+precise+trustworthy] density: 넉넉한 line-height와 margin, 읽기 편한 간격 + 엄격한 spacing scale 준수, 임의 값 금지 + 기존 레이아웃 유지, 갑작스런 위치 변경 없음
- [editorial+precise+trustworthy] feedback: 콘텐츠 맥락 안에서 인라인 표시, 토스트보다 인라인 선호 + 명확한 상태 구분, 진행률/결과를 수치로 표시 + 결과를 반드시 확인, 실패 시 복구 방법 안내

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
- 텍스트 위계가 핵심 — 컬러보다 weight/size로 구분

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

- [editorial+precise+trustworthy] motion: 콘텐츠 전환 위주, UI chrome 모션 최소화 + 120-180ms, 군더더기 없는 전환 + 모든 전환에 동일한 easing/duration
- [editorial+precise+trustworthy] density: 넉넉한 line-height와 margin, 읽기 편한 간격 + 엄격한 spacing scale 준수, 임의 값 금지 + 기존 레이아웃 유지, 갑작스런 위치 변경 없음

### 레퍼런스 근거

- **Primer**: ConfirmationDialog ConfirmationDialog is a specialized dialog component used to confirm user actions. It provides a simple way to ask users to conf...

### 구현 노트

- 기존에 같은 역할의 컴포넌트가 있으면 토큰 교체부터 시작
- variant prop으로 시각적 변형을 관리 (하드코딩 금지)
- Escape / backdrop click으로 닫기, 열 때 첫 focusable 요소로 이동
- 텍스트 위계가 핵심 — 컬러보다 weight/size로 구분

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

- [editorial+precise+trustworthy] motion: 콘텐츠 전환 위주, UI chrome 모션 최소화 + 120-180ms, 군더더기 없는 전환 + 모든 전환에 동일한 easing/duration
- [editorial+precise+trustworthy] density: 넉넉한 line-height와 margin, 읽기 편한 간격 + 엄격한 spacing scale 준수, 임의 값 금지 + 기존 레이아웃 유지, 갑작스런 위치 변경 없음

### 레퍼런스 근거

- **Carbon Design System**: The AI label is also the trigger for the explainability popover which serves as the first layer of explainability. It provides a consistent, up-fro...
- **Primer**: Popover Popover is used to bring attention to specific user interface elements.

### 구현 노트

- 기존에 같은 역할의 컴포넌트가 있으면 토큰 교체부터 시작
- variant prop으로 시각적 변형을 관리 (하드코딩 금지)
- Escape / backdrop click으로 닫기, 열 때 첫 focusable 요소로 이동
- 텍스트 위계가 핵심 — 컬러보다 weight/size로 구분

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

- [editorial+precise+trustworthy] motion: 콘텐츠 전환 위주, UI chrome 모션 최소화 + 120-180ms, 군더더기 없는 전환 + 모든 전환에 동일한 easing/duration
- [editorial+precise+trustworthy] density: 넉넉한 line-height와 margin, 읽기 편한 간격 + 엄격한 spacing scale 준수, 임의 값 금지 + 기존 레이아웃 유지, 갑작스런 위치 변경 없음

### 레퍼런스 근거

- **Primer**: ActionMenu is composed of ActionList and Overlay patterns used for quick actions and selections. AnchoredOverlay

### 구현 노트

- 기존에 같은 역할의 컴포넌트가 있으면 토큰 교체부터 시작
- variant prop으로 시각적 변형을 관리 (하드코딩 금지)
- Escape / backdrop click으로 닫기, 열 때 첫 focusable 요소로 이동
- 텍스트 위계가 핵심 — 컬러보다 weight/size로 구분

---

## data-display / feature-comparison

**역할**: 항목 간 속성/가격/점수를 나란히 비교하는 표

**탐지 출처**: comparison and ranking

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

- [editorial+precise+trustworthy] density: 넉넉한 line-height와 margin, 읽기 편한 간격 + 엄격한 spacing scale 준수, 임의 값 금지 + 기존 레이아웃 유지, 갑작스런 위치 변경 없음
- [editorial+precise+trustworthy] color: 타이포그래피로 위계 형성, 컬러보다 weight/size 활용 + 정확한 semantic 분리, 모호한 중간 톤 지양 + 안정적인 neutral 기반, 과한 accent 변화 없음

### 구현 노트

- 기존에 같은 역할의 컴포넌트가 있으면 토큰 교체부터 시작
- variant prop으로 시각적 변형을 관리 (하드코딩 금지)
- 빈 상태(empty-state)와 에러 상태를 반드시 처리
- 좁은 UI 텍스트는 Pretendard 기준 label line-height 1.4-1.5를 참고해 뭉침을 방지
- 텍스트 위계가 핵심 — 컬러보다 weight/size로 구분

---

## data-display / section-header

**역할**: 랭킹/비교 섹션의 정렬 및 설명 헤더

**탐지 출처**: comparison and ranking

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

- [editorial+precise+trustworthy] density: 넉넉한 line-height와 margin, 읽기 편한 간격 + 엄격한 spacing scale 준수, 임의 값 금지 + 기존 레이아웃 유지, 갑작스런 위치 변경 없음
- [editorial+precise+trustworthy] color: 타이포그래피로 위계 형성, 컬러보다 weight/size 활용 + 정확한 semantic 분리, 모호한 중간 톤 지양 + 안정적인 neutral 기반, 과한 accent 변화 없음

### 구현 노트

- 기존에 같은 역할의 컴포넌트가 있으면 토큰 교체부터 시작
- variant prop으로 시각적 변형을 관리 (하드코딩 금지)
- 빈 상태(empty-state)와 에러 상태를 반드시 처리
- 좁은 UI 텍스트는 Pretendard 기준 label line-height 1.4-1.5를 참고해 뭉침을 방지
- 텍스트 위계가 핵심 — 컬러보다 weight/size로 구분

---

## data-display / avatar

**역할**: 사용자 프로필 이미지/이니셜

**탐지 출처**: user profile and avatar

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

- [editorial+precise+trustworthy] density: 넉넉한 line-height와 margin, 읽기 편한 간격 + 엄격한 spacing scale 준수, 임의 값 금지 + 기존 레이아웃 유지, 갑작스런 위치 변경 없음
- [editorial+precise+trustworthy] color: 타이포그래피로 위계 형성, 컬러보다 weight/size 활용 + 정확한 semantic 분리, 모호한 중간 톤 지양 + 안정적인 neutral 기반, 과한 accent 변화 없음

### 레퍼런스 근거

- **Primer**: Avatar Avatar is an image that represents a user or organization.

### 구현 노트

- 기존에 같은 역할의 컴포넌트가 있으면 토큰 교체부터 시작
- variant prop으로 시각적 변형을 관리 (하드코딩 금지)
- 빈 상태(empty-state)와 에러 상태를 반드시 처리
- 좁은 UI 텍스트는 Pretendard 기준 label line-height 1.4-1.5를 참고해 뭉침을 방지
- 텍스트 위계가 핵심 — 컬러보다 weight/size로 구분

---

## overlay / user-menu

**역할**: 사용자 드롭다운 메뉴

**탐지 출처**: user profile and avatar

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

- [editorial+precise+trustworthy] motion: 콘텐츠 전환 위주, UI chrome 모션 최소화 + 120-180ms, 군더더기 없는 전환 + 모든 전환에 동일한 easing/duration
- [editorial+precise+trustworthy] density: 넉넉한 line-height와 margin, 읽기 편한 간격 + 엄격한 spacing scale 준수, 임의 값 금지 + 기존 레이아웃 유지, 갑작스런 위치 변경 없음

### 레퍼런스 근거

- **Primer**: ActionMenu is composed of ActionList and Overlay patterns used for quick actions and selections. AnchoredOverlay

### 구현 노트

- 기존에 같은 역할의 컴포넌트가 있으면 토큰 교체부터 시작
- variant prop으로 시각적 변형을 관리 (하드코딩 금지)
- Escape / backdrop click으로 닫기, 열 때 첫 focusable 요소로 이동
- 텍스트 위계가 핵심 — 컬러보다 weight/size로 구분

---

## data-display / profile-card

**역할**: 사용자 프로필 요약 카드

**탐지 출처**: user profile and avatar

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

- [editorial+precise+trustworthy] density: 넉넉한 line-height와 margin, 읽기 편한 간격 + 엄격한 spacing scale 준수, 임의 값 금지 + 기존 레이아웃 유지, 갑작스런 위치 변경 없음
- [editorial+precise+trustworthy] color: 타이포그래피로 위계 형성, 컬러보다 weight/size 활용 + 정확한 semantic 분리, 모호한 중간 톤 지양 + 안정적인 neutral 기반, 과한 accent 변화 없음

### 구현 노트

- 기존에 같은 역할의 컴포넌트가 있으면 토큰 교체부터 시작
- variant prop으로 시각적 변형을 관리 (하드코딩 금지)
- 빈 상태(empty-state)와 에러 상태를 반드시 처리
- 좁은 UI 텍스트는 Pretendard 기준 label line-height 1.4-1.5를 참고해 뭉침을 방지
- 텍스트 위계가 핵심 — 컬러보다 weight/size로 구분

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

- [editorial+precise+trustworthy] feedback: 콘텐츠 맥락 안에서 인라인 표시, 토스트보다 인라인 선호 + 명확한 상태 구분, 진행률/결과를 수치로 표시 + 결과를 반드시 확인, 실패 시 복구 방법 안내
- [editorial+precise+trustworthy] motion: 콘텐츠 전환 위주, UI chrome 모션 최소화 + 120-180ms, 군더더기 없는 전환 + 모든 전환에 동일한 easing/duration
- [editorial+precise+trustworthy] color: 타이포그래피로 위계 형성, 컬러보다 weight/size 활용 + 정확한 semantic 분리, 모호한 중간 톤 지양 + 안정적인 neutral 기반, 과한 accent 변화 없음

### 레퍼런스 근거

- **Carbon Design System**: We welcome all feedback, designs, or ideas in order to produce the best possible experience for our users. If you're interested in contributing, ch...
- **Primer**: Messaging components are used to provide important and relevant information to the user, including feedback, contextual information, product update...

### 구현 노트

- 기존에 같은 역할의 컴포넌트가 있으면 토큰 교체부터 시작
- variant prop으로 시각적 변형을 관리 (하드코딩 금지)
- auto-dismiss 시간은 내용 길이에 비례 (기본 5초)
- 반응형 검증: 320px, 360px, 390px, 430px에서 control overflow와 viewport horizontal scroll이 없어야 함
- action row는 narrow viewport에서 `flex-wrap: wrap` 또는 세로 stack으로 전환하고, overflow-x 숨김으로 문제를 덮지 않음
- 텍스트 위계가 핵심 — 컬러보다 weight/size로 구분

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

- [editorial+precise+trustworthy] hover: 텍스트 underline 또는 color shift, 장식적 효과 없음 + 정확한 border/outline 변화 + 예측 가능하고 일관된 hover 패턴
- [editorial+precise+trustworthy] density: 넉넉한 line-height와 margin, 읽기 편한 간격 + 엄격한 spacing scale 준수, 임의 값 금지 + 기존 레이아웃 유지, 갑작스런 위치 변경 없음
- [editorial+precise+trustworthy] motion: 콘텐츠 전환 위주, UI chrome 모션 최소화 + 120-180ms, 군더더기 없는 전환 + 모든 전환에 동일한 easing/duration

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
- 텍스트 위계가 핵심 — 컬러보다 weight/size로 구분

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

- [editorial+precise+trustworthy] motion: 콘텐츠 전환 위주, UI chrome 모션 최소화 + 120-180ms, 군더더기 없는 전환 + 모든 전환에 동일한 easing/duration
- [editorial+precise+trustworthy] density: 넉넉한 line-height와 margin, 읽기 편한 간격 + 엄격한 spacing scale 준수, 임의 값 금지 + 기존 레이아웃 유지, 갑작스런 위치 변경 없음

### 레퍼런스 근거

- **Primer**: ActionMenu is composed of ActionList and Overlay patterns used for quick actions and selections. AnchoredOverlay

### 구현 노트

- 기존에 같은 역할의 컴포넌트가 있으면 토큰 교체부터 시작
- variant prop으로 시각적 변형을 관리 (하드코딩 금지)
- Escape / backdrop click으로 닫기, 열 때 첫 focusable 요소로 이동
- 텍스트 위계가 핵심 — 컬러보다 weight/size로 구분

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

- [editorial+precise+trustworthy] hover: 텍스트 underline 또는 color shift, 장식적 효과 없음 + 정확한 border/outline 변화 + 예측 가능하고 일관된 hover 패턴
- [editorial+precise+trustworthy] density: 넉넉한 line-height와 margin, 읽기 편한 간격 + 엄격한 spacing scale 준수, 임의 값 금지 + 기존 레이아웃 유지, 갑작스런 위치 변경 없음
- [editorial+precise+trustworthy] motion: 콘텐츠 전환 위주, UI chrome 모션 최소화 + 120-180ms, 군더더기 없는 전환 + 모든 전환에 동일한 easing/duration

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
- 텍스트 위계가 핵심 — 컬러보다 weight/size로 구분

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

- [editorial+precise+trustworthy] hover: 텍스트 underline 또는 color shift, 장식적 효과 없음 + 정확한 border/outline 변화 + 예측 가능하고 일관된 hover 패턴
- [editorial+precise+trustworthy] density: 넉넉한 line-height와 margin, 읽기 편한 간격 + 엄격한 spacing scale 준수, 임의 값 금지 + 기존 레이아웃 유지, 갑작스런 위치 변경 없음
- [editorial+precise+trustworthy] motion: 콘텐츠 전환 위주, UI chrome 모션 최소화 + 120-180ms, 군더더기 없는 전환 + 모든 전환에 동일한 easing/duration

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
- 텍스트 위계가 핵심 — 컬러보다 weight/size로 구분

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

- [editorial+precise+trustworthy] hover: 텍스트 underline 또는 color shift, 장식적 효과 없음 + 정확한 border/outline 변화 + 예측 가능하고 일관된 hover 패턴
- [editorial+precise+trustworthy] density: 넉넉한 line-height와 margin, 읽기 편한 간격 + 엄격한 spacing scale 준수, 임의 값 금지 + 기존 레이아웃 유지, 갑작스런 위치 변경 없음
- [editorial+precise+trustworthy] motion: 콘텐츠 전환 위주, UI chrome 모션 최소화 + 120-180ms, 군더더기 없는 전환 + 모든 전환에 동일한 easing/duration

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
- 텍스트 위계가 핵심 — 컬러보다 weight/size로 구분

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

- [editorial+precise+trustworthy] hover: 텍스트 underline 또는 color shift, 장식적 효과 없음 + 정확한 border/outline 변화 + 예측 가능하고 일관된 hover 패턴
- [editorial+precise+trustworthy] density: 넉넉한 line-height와 margin, 읽기 편한 간격 + 엄격한 spacing scale 준수, 임의 값 금지 + 기존 레이아웃 유지, 갑작스런 위치 변경 없음
- [editorial+precise+trustworthy] motion: 콘텐츠 전환 위주, UI chrome 모션 최소화 + 120-180ms, 군더더기 없는 전환 + 모든 전환에 동일한 easing/duration

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
- 텍스트 위계가 핵심 — 컬러보다 weight/size로 구분

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

- [editorial+precise+trustworthy] hover: 텍스트 underline 또는 color shift, 장식적 효과 없음 + 정확한 border/outline 변화 + 예측 가능하고 일관된 hover 패턴
- [editorial+precise+trustworthy] density: 넉넉한 line-height와 margin, 읽기 편한 간격 + 엄격한 spacing scale 준수, 임의 값 금지 + 기존 레이아웃 유지, 갑작스런 위치 변경 없음
- [editorial+precise+trustworthy] motion: 콘텐츠 전환 위주, UI chrome 모션 최소화 + 120-180ms, 군더더기 없는 전환 + 모든 전환에 동일한 easing/duration

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
- 텍스트 위계가 핵심 — 컬러보다 weight/size로 구분

---

## data-display / chart-container

**역할**: 차트 래퍼 (타이틀, 범례 포함)

**탐지 출처**: charts and visualization

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

- [editorial+precise+trustworthy] density: 넉넉한 line-height와 margin, 읽기 편한 간격 + 엄격한 spacing scale 준수, 임의 값 금지 + 기존 레이아웃 유지, 갑작스런 위치 변경 없음
- [editorial+precise+trustworthy] color: 타이포그래피로 위계 형성, 컬러보다 weight/size 활용 + 정확한 semantic 분리, 모호한 중간 톤 지양 + 안정적인 neutral 기반, 과한 accent 변화 없음

### 구현 노트

- 기존에 같은 역할의 컴포넌트가 있으면 토큰 교체부터 시작
- variant prop으로 시각적 변형을 관리 (하드코딩 금지)
- 빈 상태(empty-state)와 에러 상태를 반드시 처리
- 좁은 UI 텍스트는 Pretendard 기준 label line-height 1.4-1.5를 참고해 뭉침을 방지
- 텍스트 위계가 핵심 — 컬러보다 weight/size로 구분

---

## overlay / chart-tooltip

**역할**: 데이터 포인트 호버 시 상세 정보

**탐지 출처**: charts and visualization

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

- [editorial+precise+trustworthy] motion: 콘텐츠 전환 위주, UI chrome 모션 최소화 + 120-180ms, 군더더기 없는 전환 + 모든 전환에 동일한 easing/duration
- [editorial+precise+trustworthy] density: 넉넉한 line-height와 margin, 읽기 편한 간격 + 엄격한 spacing scale 준수, 임의 값 금지 + 기존 레이아웃 유지, 갑작스런 위치 변경 없음

### 레퍼런스 근거

- **Primer**: ActionMenu is composed of ActionList and Overlay patterns used for quick actions and selections. AnchoredOverlay

### 구현 노트

- 기존에 같은 역할의 컴포넌트가 있으면 토큰 교체부터 시작
- variant prop으로 시각적 변형을 관리 (하드코딩 금지)
- Escape / backdrop click으로 닫기, 열 때 첫 focusable 요소로 이동
- 텍스트 위계가 핵심 — 컬러보다 weight/size로 구분

---

## data-display / chart-legend

**역할**: 차트 범례

**탐지 출처**: charts and visualization

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

- [editorial+precise+trustworthy] density: 넉넉한 line-height와 margin, 읽기 편한 간격 + 엄격한 spacing scale 준수, 임의 값 금지 + 기존 레이아웃 유지, 갑작스런 위치 변경 없음
- [editorial+precise+trustworthy] color: 타이포그래피로 위계 형성, 컬러보다 weight/size 활용 + 정확한 semantic 분리, 모호한 중간 톤 지양 + 안정적인 neutral 기반, 과한 accent 변화 없음

### 구현 노트

- 기존에 같은 역할의 컴포넌트가 있으면 토큰 교체부터 시작
- variant prop으로 시각적 변형을 관리 (하드코딩 금지)
- 빈 상태(empty-state)와 에러 상태를 반드시 처리
- 좁은 UI 텍스트는 Pretendard 기준 label line-height 1.4-1.5를 참고해 뭉침을 방지
- 텍스트 위계가 핵심 — 컬러보다 weight/size로 구분

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

- [editorial+precise+trustworthy] hover: 텍스트 underline 또는 color shift, 장식적 효과 없음 + 정확한 border/outline 변화 + 예측 가능하고 일관된 hover 패턴
- [editorial+precise+trustworthy] density: 넉넉한 line-height와 margin, 읽기 편한 간격 + 엄격한 spacing scale 준수, 임의 값 금지 + 기존 레이아웃 유지, 갑작스런 위치 변경 없음
- [editorial+precise+trustworthy] feedback: 콘텐츠 맥락 안에서 인라인 표시, 토스트보다 인라인 선호 + 명확한 상태 구분, 진행률/결과를 수치로 표시 + 결과를 반드시 확인, 실패 시 복구 방법 안내

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
- 텍스트 위계가 핵심 — 컬러보다 weight/size로 구분

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

- [editorial+precise+trustworthy] density: 넉넉한 line-height와 margin, 읽기 편한 간격 + 엄격한 spacing scale 준수, 임의 값 금지 + 기존 레이아웃 유지, 갑작스런 위치 변경 없음
- [editorial+precise+trustworthy] color: 타이포그래피로 위계 형성, 컬러보다 weight/size 활용 + 정확한 semantic 분리, 모호한 중간 톤 지양 + 안정적인 neutral 기반, 과한 accent 변화 없음

### 구현 노트

- 기존에 같은 역할의 컴포넌트가 있으면 토큰 교체부터 시작
- variant prop으로 시각적 변형을 관리 (하드코딩 금지)
- 빈 상태(empty-state)와 에러 상태를 반드시 처리
- 좁은 UI 텍스트는 Pretendard 기준 label line-height 1.4-1.5를 참고해 뭉침을 방지
- 텍스트 위계가 핵심 — 컬러보다 weight/size로 구분

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

- [editorial+precise+trustworthy] hover: 텍스트 underline 또는 color shift, 장식적 효과 없음 + 정확한 border/outline 변화 + 예측 가능하고 일관된 hover 패턴
- [editorial+precise+trustworthy] density: 넉넉한 line-height와 margin, 읽기 편한 간격 + 엄격한 spacing scale 준수, 임의 값 금지 + 기존 레이아웃 유지, 갑작스런 위치 변경 없음
- [editorial+precise+trustworthy] feedback: 콘텐츠 맥락 안에서 인라인 표시, 토스트보다 인라인 선호 + 명확한 상태 구분, 진행률/결과를 수치로 표시 + 결과를 반드시 확인, 실패 시 복구 방법 안내

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
- 텍스트 위계가 핵심 — 컬러보다 weight/size로 구분

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

- [editorial+precise+trustworthy] motion: 콘텐츠 전환 위주, UI chrome 모션 최소화 + 120-180ms, 군더더기 없는 전환 + 모든 전환에 동일한 easing/duration
- [editorial+precise+trustworthy] density: 넉넉한 line-height와 margin, 읽기 편한 간격 + 엄격한 spacing scale 준수, 임의 값 금지 + 기존 레이아웃 유지, 갑작스런 위치 변경 없음

### 레퍼런스 근거

- **Primer**: Autocomplete Autocomplete allows users to quickly filter through a list of options and pick one or more values for a field.

### 구현 노트

- 기존에 같은 역할의 컴포넌트가 있으면 토큰 교체부터 시작
- variant prop으로 시각적 변형을 관리 (하드코딩 금지)
- Escape / backdrop click으로 닫기, 열 때 첫 focusable 요소로 이동
- 텍스트 위계가 핵심 — 컬러보다 weight/size로 구분

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

- [editorial+precise+trustworthy] density: 넉넉한 line-height와 margin, 읽기 편한 간격 + 엄격한 spacing scale 준수, 임의 값 금지 + 기존 레이아웃 유지, 갑작스런 위치 변경 없음
- [editorial+precise+trustworthy] color: 타이포그래피로 위계 형성, 컬러보다 weight/size 활용 + 정확한 semantic 분리, 모호한 중간 톤 지양 + 안정적인 neutral 기반, 과한 accent 변화 없음

### 구현 노트

- 기존에 같은 역할의 컴포넌트가 있으면 토큰 교체부터 시작
- variant prop으로 시각적 변형을 관리 (하드코딩 금지)
- 빈 상태(empty-state)와 에러 상태를 반드시 처리
- 좁은 UI 텍스트는 Pretendard 기준 label line-height 1.4-1.5를 참고해 뭉침을 방지
- 텍스트 위계가 핵심 — 컬러보다 weight/size로 구분

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

- [editorial+precise+trustworthy] density: 넉넉한 line-height와 margin, 읽기 편한 간격 + 엄격한 spacing scale 준수, 임의 값 금지 + 기존 레이아웃 유지, 갑작스런 위치 변경 없음
- [editorial+precise+trustworthy] color: 타이포그래피로 위계 형성, 컬러보다 weight/size 활용 + 정확한 semantic 분리, 모호한 중간 톤 지양 + 안정적인 neutral 기반, 과한 accent 변화 없음

### 구현 노트

- 기존에 같은 역할의 컴포넌트가 있으면 토큰 교체부터 시작
- variant prop으로 시각적 변형을 관리 (하드코딩 금지)
- 빈 상태(empty-state)와 에러 상태를 반드시 처리
- 좁은 UI 텍스트는 Pretendard 기준 label line-height 1.4-1.5를 참고해 뭉침을 방지
- 텍스트 위계가 핵심 — 컬러보다 weight/size로 구분

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

- [editorial+precise+trustworthy] density: 넉넉한 line-height와 margin, 읽기 편한 간격 + 엄격한 spacing scale 준수, 임의 값 금지 + 기존 레이아웃 유지, 갑작스런 위치 변경 없음
- [editorial+precise+trustworthy] color: 타이포그래피로 위계 형성, 컬러보다 weight/size 활용 + 정확한 semantic 분리, 모호한 중간 톤 지양 + 안정적인 neutral 기반, 과한 accent 변화 없음

### 구현 노트

- 기존에 같은 역할의 컴포넌트가 있으면 토큰 교체부터 시작
- variant prop으로 시각적 변형을 관리 (하드코딩 금지)
- 빈 상태(empty-state)와 에러 상태를 반드시 처리
- 좁은 UI 텍스트는 Pretendard 기준 label line-height 1.4-1.5를 참고해 뭉침을 방지
- 텍스트 위계가 핵심 — 컬러보다 weight/size로 구분

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

- [editorial+precise+trustworthy] feedback: 콘텐츠 맥락 안에서 인라인 표시, 토스트보다 인라인 선호 + 명확한 상태 구분, 진행률/결과를 수치로 표시 + 결과를 반드시 확인, 실패 시 복구 방법 안내
- [editorial+precise+trustworthy] motion: 콘텐츠 전환 위주, UI chrome 모션 최소화 + 120-180ms, 군더더기 없는 전환 + 모든 전환에 동일한 easing/duration
- [editorial+precise+trustworthy] color: 타이포그래피로 위계 형성, 컬러보다 weight/size 활용 + 정확한 semantic 분리, 모호한 중간 톤 지양 + 안정적인 neutral 기반, 과한 accent 변화 없음

### 레퍼런스 근거

- **Carbon Design System**: We welcome all feedback, designs, or ideas in order to produce the best possible experience for our users. If you're interested in contributing, ch...
- **Primer**: Messaging components are used to provide important and relevant information to the user, including feedback, contextual information, product update...

### 구현 노트

- 기존에 같은 역할의 컴포넌트가 있으면 토큰 교체부터 시작
- variant prop으로 시각적 변형을 관리 (하드코딩 금지)
- auto-dismiss 시간은 내용 길이에 비례 (기본 5초)
- 반응형 검증: 320px, 360px, 390px, 430px에서 control overflow와 viewport horizontal scroll이 없어야 함
- action row는 narrow viewport에서 `flex-wrap: wrap` 또는 세로 stack으로 전환하고, overflow-x 숨김으로 문제를 덮지 않음
- 텍스트 위계가 핵심 — 컬러보다 weight/size로 구분

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

- [editorial+precise+trustworthy] feedback: 콘텐츠 맥락 안에서 인라인 표시, 토스트보다 인라인 선호 + 명확한 상태 구분, 진행률/결과를 수치로 표시 + 결과를 반드시 확인, 실패 시 복구 방법 안내
- [editorial+precise+trustworthy] motion: 콘텐츠 전환 위주, UI chrome 모션 최소화 + 120-180ms, 군더더기 없는 전환 + 모든 전환에 동일한 easing/duration
- [editorial+precise+trustworthy] color: 타이포그래피로 위계 형성, 컬러보다 weight/size 활용 + 정확한 semantic 분리, 모호한 중간 톤 지양 + 안정적인 neutral 기반, 과한 accent 변화 없음

### 레퍼런스 근거

- **Carbon Design System**: We welcome all feedback, designs, or ideas in order to produce the best possible experience for our users. If you're interested in contributing, ch...
- **Primer**: Messaging components are used to provide important and relevant information to the user, including feedback, contextual information, product update...

### 구현 노트

- 기존에 같은 역할의 컴포넌트가 있으면 토큰 교체부터 시작
- variant prop으로 시각적 변형을 관리 (하드코딩 금지)
- auto-dismiss 시간은 내용 길이에 비례 (기본 5초)
- 반응형 검증: 320px, 360px, 390px, 430px에서 control overflow와 viewport horizontal scroll이 없어야 함
- action row는 narrow viewport에서 `flex-wrap: wrap` 또는 세로 stack으로 전환하고, overflow-x 숨김으로 문제를 덮지 않음
- 텍스트 위계가 핵심 — 컬러보다 weight/size로 구분

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

- [editorial+precise+trustworthy] feedback: 콘텐츠 맥락 안에서 인라인 표시, 토스트보다 인라인 선호 + 명확한 상태 구분, 진행률/결과를 수치로 표시 + 결과를 반드시 확인, 실패 시 복구 방법 안내
- [editorial+precise+trustworthy] motion: 콘텐츠 전환 위주, UI chrome 모션 최소화 + 120-180ms, 군더더기 없는 전환 + 모든 전환에 동일한 easing/duration
- [editorial+precise+trustworthy] color: 타이포그래피로 위계 형성, 컬러보다 weight/size 활용 + 정확한 semantic 분리, 모호한 중간 톤 지양 + 안정적인 neutral 기반, 과한 accent 변화 없음

### 레퍼런스 근거

- **Carbon Design System**: We welcome all feedback, designs, or ideas in order to produce the best possible experience for our users. If you're interested in contributing, ch...
- **Primer**: Empty states Empty states are used to fill spaces when no content has been added yet, or is temporarily empty due to the nature of the feature.

### 구현 노트

- 기존에 같은 역할의 컴포넌트가 있으면 토큰 교체부터 시작
- variant prop으로 시각적 변형을 관리 (하드코딩 금지)
- auto-dismiss 시간은 내용 길이에 비례 (기본 5초)
- 반응형 검증: 320px, 360px, 390px, 430px에서 control overflow와 viewport horizontal scroll이 없어야 함
- action row는 narrow viewport에서 `flex-wrap: wrap` 또는 세로 stack으로 전환하고, overflow-x 숨김으로 문제를 덮지 않음
- 텍스트 위계가 핵심 — 컬러보다 weight/size로 구분

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

- [editorial+precise+trustworthy] feedback: 콘텐츠 맥락 안에서 인라인 표시, 토스트보다 인라인 선호 + 명확한 상태 구분, 진행률/결과를 수치로 표시 + 결과를 반드시 확인, 실패 시 복구 방법 안내
- [editorial+precise+trustworthy] motion: 콘텐츠 전환 위주, UI chrome 모션 최소화 + 120-180ms, 군더더기 없는 전환 + 모든 전환에 동일한 easing/duration
- [editorial+precise+trustworthy] color: 타이포그래피로 위계 형성, 컬러보다 weight/size 활용 + 정확한 semantic 분리, 모호한 중간 톤 지양 + 안정적인 neutral 기반, 과한 accent 변화 없음

### 레퍼런스 근거

- **Carbon Design System**: We welcome all feedback, designs, or ideas in order to produce the best possible experience for our users. If you're interested in contributing, ch...
- **Primer**: Banner Banner is used to highlight important information.

### 구현 노트

- 기존에 같은 역할의 컴포넌트가 있으면 토큰 교체부터 시작
- variant prop으로 시각적 변형을 관리 (하드코딩 금지)
- auto-dismiss 시간은 내용 길이에 비례 (기본 5초)
- 반응형 검증: 320px, 360px, 390px, 430px에서 control overflow와 viewport horizontal scroll이 없어야 함
- action row는 narrow viewport에서 `flex-wrap: wrap` 또는 세로 stack으로 전환하고, overflow-x 숨김으로 문제를 덮지 않음
- 텍스트 위계가 핵심 — 컬러보다 weight/size로 구분

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

- [editorial+precise+trustworthy] density: 넉넉한 line-height와 margin, 읽기 편한 간격 + 엄격한 spacing scale 준수, 임의 값 금지 + 기존 레이아웃 유지, 갑작스런 위치 변경 없음
- [editorial+precise+trustworthy] color: 타이포그래피로 위계 형성, 컬러보다 weight/size 활용 + 정확한 semantic 분리, 모호한 중간 톤 지양 + 안정적인 neutral 기반, 과한 accent 변화 없음

### 구현 노트

- 기존에 같은 역할의 컴포넌트가 있으면 토큰 교체부터 시작
- variant prop으로 시각적 변형을 관리 (하드코딩 금지)
- 빈 상태(empty-state)와 에러 상태를 반드시 처리
- 좁은 UI 텍스트는 Pretendard 기준 label line-height 1.4-1.5를 참고해 뭉침을 방지
- 텍스트 위계가 핵심 — 컬러보다 weight/size로 구분

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

- [editorial+precise+trustworthy] hover: 텍스트 underline 또는 color shift, 장식적 효과 없음 + 정확한 border/outline 변화 + 예측 가능하고 일관된 hover 패턴
- [editorial+precise+trustworthy] density: 넉넉한 line-height와 margin, 읽기 편한 간격 + 엄격한 spacing scale 준수, 임의 값 금지 + 기존 레이아웃 유지, 갑작스런 위치 변경 없음
- [editorial+precise+trustworthy] feedback: 콘텐츠 맥락 안에서 인라인 표시, 토스트보다 인라인 선호 + 명확한 상태 구분, 진행률/결과를 수치로 표시 + 결과를 반드시 확인, 실패 시 복구 방법 안내

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
- 텍스트 위계가 핵심 — 컬러보다 weight/size로 구분

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

- [editorial+precise+trustworthy] motion: 콘텐츠 전환 위주, UI chrome 모션 최소화 + 120-180ms, 군더더기 없는 전환 + 모든 전환에 동일한 easing/duration
- [editorial+precise+trustworthy] density: 넉넉한 line-height와 margin, 읽기 편한 간격 + 엄격한 spacing scale 준수, 임의 값 금지 + 기존 레이아웃 유지, 갑작스런 위치 변경 없음

### 레퍼런스 근거

- **Primer**: ActionMenu is composed of ActionList and Overlay patterns used for quick actions and selections. AnchoredOverlay

### 구현 노트

- 기존에 같은 역할의 컴포넌트가 있으면 토큰 교체부터 시작
- variant prop으로 시각적 변형을 관리 (하드코딩 금지)
- Escape / backdrop click으로 닫기, 열 때 첫 focusable 요소로 이동
- 텍스트 위계가 핵심 — 컬러보다 weight/size로 구분

---

## data-display / pricing-card

**역할**: 플랜별 가격/기능 비교 카드

**탐지 출처**: pricing and plans

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

- [editorial+precise+trustworthy] density: 넉넉한 line-height와 margin, 읽기 편한 간격 + 엄격한 spacing scale 준수, 임의 값 금지 + 기존 레이아웃 유지, 갑작스런 위치 변경 없음
- [editorial+precise+trustworthy] color: 타이포그래피로 위계 형성, 컬러보다 weight/size 활용 + 정확한 semantic 분리, 모호한 중간 톤 지양 + 안정적인 neutral 기반, 과한 accent 변화 없음

### 구현 노트

- 기존에 같은 역할의 컴포넌트가 있으면 토큰 교체부터 시작
- variant prop으로 시각적 변형을 관리 (하드코딩 금지)
- 빈 상태(empty-state)와 에러 상태를 반드시 처리
- 좁은 UI 텍스트는 Pretendard 기준 label line-height 1.4-1.5를 참고해 뭉침을 방지
- 텍스트 위계가 핵심 — 컬러보다 weight/size로 구분

---

## feedback / upgrade-banner

**역할**: 업그레이드 유도 배너

**탐지 출처**: pricing and plans

**Slot archetype**: `badge`

### 구조 (Anatomy)

- container
- value
- label(optional)

### 상태 (States)

| 상태 | 설명 |
|------|------|
| `default` | 기본 상태 |

### 토큰 바인딩

```
surface: var(--color-surface-tint)
text: var(--color-brand-primary)
value-size: var(--text-4xl)
label-size: var(--text-sm)
label-color: var(--color-text-muted)
radius: var(--radius-md)
padding: var(--space-12) var(--space-16)
```

### 접근성

- 정보를 담으면 aria-label 제공
- 장식이면 aria-hidden="true"

### 브랜드 적용

- [editorial+precise+trustworthy] feedback: 콘텐츠 맥락 안에서 인라인 표시, 토스트보다 인라인 선호 + 명확한 상태 구분, 진행률/결과를 수치로 표시 + 결과를 반드시 확인, 실패 시 복구 방법 안내
- [editorial+precise+trustworthy] motion: 콘텐츠 전환 위주, UI chrome 모션 최소화 + 120-180ms, 군더더기 없는 전환 + 모든 전환에 동일한 easing/duration
- [editorial+precise+trustworthy] color: 타이포그래피로 위계 형성, 컬러보다 weight/size 활용 + 정확한 semantic 분리, 모호한 중간 톤 지양 + 안정적인 neutral 기반, 과한 accent 변화 없음

### 레퍼런스 근거

- **Carbon Design System**: We welcome all feedback, designs, or ideas in order to produce the best possible experience for our users. If you're interested in contributing, ch...
- **Primer**: Messaging components are used to provide important and relevant information to the user, including feedback, contextual information, product update...

### 구현 노트

- 기존에 같은 역할의 컴포넌트가 있으면 토큰 교체부터 시작
- variant prop으로 시각적 변형을 관리 (하드코딩 금지)
- auto-dismiss 시간은 내용 길이에 비례 (기본 5초)
- 반응형 검증: 320px, 360px, 390px, 430px에서 control overflow와 viewport horizontal scroll이 없어야 함
- action row는 narrow viewport에서 `flex-wrap: wrap` 또는 세로 stack으로 전환하고, overflow-x 숨김으로 문제를 덮지 않음
- 텍스트 위계가 핵심 — 컬러보다 weight/size로 구분

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

- [editorial+precise+trustworthy] density: 넉넉한 line-height와 margin, 읽기 편한 간격 + 엄격한 spacing scale 준수, 임의 값 금지 + 기존 레이아웃 유지, 갑작스런 위치 변경 없음
- [editorial+precise+trustworthy] color: 타이포그래피로 위계 형성, 컬러보다 weight/size 활용 + 정확한 semantic 분리, 모호한 중간 톤 지양 + 안정적인 neutral 기반, 과한 accent 변화 없음

### 구현 노트

- 기존에 같은 역할의 컴포넌트가 있으면 토큰 교체부터 시작
- variant prop으로 시각적 변형을 관리 (하드코딩 금지)
- 빈 상태(empty-state)와 에러 상태를 반드시 처리
- 좁은 UI 텍스트는 Pretendard 기준 label line-height 1.4-1.5를 참고해 뭉침을 방지
- 텍스트 위계가 핵심 — 컬러보다 weight/size로 구분

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

- [editorial+precise+trustworthy] hover: 텍스트 underline 또는 color shift, 장식적 효과 없음 + 정확한 border/outline 변화 + 예측 가능하고 일관된 hover 패턴
- [editorial+precise+trustworthy] density: 넉넉한 line-height와 margin, 읽기 편한 간격 + 엄격한 spacing scale 준수, 임의 값 금지 + 기존 레이아웃 유지, 갑작스런 위치 변경 없음
- [editorial+precise+trustworthy] feedback: 콘텐츠 맥락 안에서 인라인 표시, 토스트보다 인라인 선호 + 명확한 상태 구분, 진행률/결과를 수치로 표시 + 결과를 반드시 확인, 실패 시 복구 방법 안내

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
- 텍스트 위계가 핵심 — 컬러보다 weight/size로 구분

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

- [editorial+precise+trustworthy] density: 넉넉한 line-height와 margin, 읽기 편한 간격 + 엄격한 spacing scale 준수, 임의 값 금지 + 기존 레이아웃 유지, 갑작스런 위치 변경 없음
- [editorial+precise+trustworthy] color: 타이포그래피로 위계 형성, 컬러보다 weight/size 활용 + 정확한 semantic 분리, 모호한 중간 톤 지양 + 안정적인 neutral 기반, 과한 accent 변화 없음

### 구현 노트

- 기존에 같은 역할의 컴포넌트가 있으면 토큰 교체부터 시작
- variant prop으로 시각적 변형을 관리 (하드코딩 금지)
- 빈 상태(empty-state)와 에러 상태를 반드시 처리
- 좁은 UI 텍스트는 Pretendard 기준 label line-height 1.4-1.5를 참고해 뭉침을 방지
- 텍스트 위계가 핵심 — 컬러보다 weight/size로 구분

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

- [editorial+precise+trustworthy] hover: 텍스트 underline 또는 color shift, 장식적 효과 없음 + 정확한 border/outline 변화 + 예측 가능하고 일관된 hover 패턴
- [editorial+precise+trustworthy] density: 넉넉한 line-height와 margin, 읽기 편한 간격 + 엄격한 spacing scale 준수, 임의 값 금지 + 기존 레이아웃 유지, 갑작스런 위치 변경 없음
- [editorial+precise+trustworthy] feedback: 콘텐츠 맥락 안에서 인라인 표시, 토스트보다 인라인 선호 + 명확한 상태 구분, 진행률/결과를 수치로 표시 + 결과를 반드시 확인, 실패 시 복구 방법 안내

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
- 텍스트 위계가 핵심 — 컬러보다 weight/size로 구분

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

- [editorial+precise+trustworthy] hover: 텍스트 underline 또는 color shift, 장식적 효과 없음 + 정확한 border/outline 변화 + 예측 가능하고 일관된 hover 패턴
- [editorial+precise+trustworthy] density: 넉넉한 line-height와 margin, 읽기 편한 간격 + 엄격한 spacing scale 준수, 임의 값 금지 + 기존 레이아웃 유지, 갑작스런 위치 변경 없음
- [editorial+precise+trustworthy] feedback: 콘텐츠 맥락 안에서 인라인 표시, 토스트보다 인라인 선호 + 명확한 상태 구분, 진행률/결과를 수치로 표시 + 결과를 반드시 확인, 실패 시 복구 방법 안내

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
- 텍스트 위계가 핵심 — 컬러보다 weight/size로 구분

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

- [editorial+precise+trustworthy] hover: 텍스트 underline 또는 color shift, 장식적 효과 없음 + 정확한 border/outline 변화 + 예측 가능하고 일관된 hover 패턴
- [editorial+precise+trustworthy] density: 넉넉한 line-height와 margin, 읽기 편한 간격 + 엄격한 spacing scale 준수, 임의 값 금지 + 기존 레이아웃 유지, 갑작스런 위치 변경 없음
- [editorial+precise+trustworthy] motion: 콘텐츠 전환 위주, UI chrome 모션 최소화 + 120-180ms, 군더더기 없는 전환 + 모든 전환에 동일한 easing/duration

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
- 텍스트 위계가 핵심 — 컬러보다 weight/size로 구분

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

- [editorial+precise+trustworthy] hover: 텍스트 underline 또는 color shift, 장식적 효과 없음 + 정확한 border/outline 변화 + 예측 가능하고 일관된 hover 패턴
- [editorial+precise+trustworthy] density: 넉넉한 line-height와 margin, 읽기 편한 간격 + 엄격한 spacing scale 준수, 임의 값 금지 + 기존 레이아웃 유지, 갑작스런 위치 변경 없음
- [editorial+precise+trustworthy] motion: 콘텐츠 전환 위주, UI chrome 모션 최소화 + 120-180ms, 군더더기 없는 전환 + 모든 전환에 동일한 easing/duration

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
- 텍스트 위계가 핵심 — 컬러보다 weight/size로 구분

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

- [editorial+precise+trustworthy] feedback: 콘텐츠 맥락 안에서 인라인 표시, 토스트보다 인라인 선호 + 명확한 상태 구분, 진행률/결과를 수치로 표시 + 결과를 반드시 확인, 실패 시 복구 방법 안내
- [editorial+precise+trustworthy] motion: 콘텐츠 전환 위주, UI chrome 모션 최소화 + 120-180ms, 군더더기 없는 전환 + 모든 전환에 동일한 easing/duration
- [editorial+precise+trustworthy] color: 타이포그래피로 위계 형성, 컬러보다 weight/size 활용 + 정확한 semantic 분리, 모호한 중간 톤 지양 + 안정적인 neutral 기반, 과한 accent 변화 없음

### 레퍼런스 근거

- **Carbon Design System**: We welcome all feedback, designs, or ideas in order to produce the best possible experience for our users. If you're interested in contributing, ch...
- **Primer**: CircleBadge CircleBadge visually connects logos of third-party services, eg. in the marketplace.

### 구현 노트

- 기존에 같은 역할의 컴포넌트가 있으면 토큰 교체부터 시작
- variant prop으로 시각적 변형을 관리 (하드코딩 금지)
- auto-dismiss 시간은 내용 길이에 비례 (기본 5초)
- 반응형 검증: 320px, 360px, 390px, 430px에서 control overflow와 viewport horizontal scroll이 없어야 함
- action row는 narrow viewport에서 `flex-wrap: wrap` 또는 세로 stack으로 전환하고, overflow-x 숨김으로 문제를 덮지 않음
- 텍스트 위계가 핵심 — 컬러보다 weight/size로 구분

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

- [editorial+precise+trustworthy] feedback: 콘텐츠 맥락 안에서 인라인 표시, 토스트보다 인라인 선호 + 명확한 상태 구분, 진행률/결과를 수치로 표시 + 결과를 반드시 확인, 실패 시 복구 방법 안내
- [editorial+precise+trustworthy] motion: 콘텐츠 전환 위주, UI chrome 모션 최소화 + 120-180ms, 군더더기 없는 전환 + 모든 전환에 동일한 easing/duration
- [editorial+precise+trustworthy] color: 타이포그래피로 위계 형성, 컬러보다 weight/size 활용 + 정확한 semantic 분리, 모호한 중간 톤 지양 + 안정적인 neutral 기반, 과한 accent 변화 없음

### 레퍼런스 근거

- **Carbon Design System**: We welcome all feedback, designs, or ideas in order to produce the best possible experience for our users. If you're interested in contributing, ch...
- **Primer**: Messaging components are used to provide important and relevant information to the user, including feedback, contextual information, product update...

### 구현 노트

- 기존에 같은 역할의 컴포넌트가 있으면 토큰 교체부터 시작
- variant prop으로 시각적 변형을 관리 (하드코딩 금지)
- auto-dismiss 시간은 내용 길이에 비례 (기본 5초)
- 반응형 검증: 320px, 360px, 390px, 430px에서 control overflow와 viewport horizontal scroll이 없어야 함
- action row는 narrow viewport에서 `flex-wrap: wrap` 또는 세로 stack으로 전환하고, overflow-x 숨김으로 문제를 덮지 않음
- 텍스트 위계가 핵심 — 컬러보다 weight/size로 구분

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

- [editorial+precise+trustworthy] motion: 콘텐츠 전환 위주, UI chrome 모션 최소화 + 120-180ms, 군더더기 없는 전환 + 모든 전환에 동일한 easing/duration
- [editorial+precise+trustworthy] density: 넉넉한 line-height와 margin, 읽기 편한 간격 + 엄격한 spacing scale 준수, 임의 값 금지 + 기존 레이아웃 유지, 갑작스런 위치 변경 없음

### 레퍼런스 근거

- **Carbon Design System**: We’re also using this release to address some of the outstanding accessibility issues for components like Notification and Tooltip along with consi...
- **Primer**: Tooltip Tooltips add additional context to interactive UI elements and appear on mouse hover or keyboard focus.

### 구현 노트

- 기존에 같은 역할의 컴포넌트가 있으면 토큰 교체부터 시작
- variant prop으로 시각적 변형을 관리 (하드코딩 금지)
- Escape / backdrop click으로 닫기, 열 때 첫 focusable 요소로 이동
- 텍스트 위계가 핵심 — 컬러보다 weight/size로 구분

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

- [editorial+precise+trustworthy] density: 넉넉한 line-height와 margin, 읽기 편한 간격 + 엄격한 spacing scale 준수, 임의 값 금지 + 기존 레이아웃 유지, 갑작스런 위치 변경 없음
- [editorial+precise+trustworthy] color: 타이포그래피로 위계 형성, 컬러보다 weight/size 활용 + 정확한 semantic 분리, 모호한 중간 톤 지양 + 안정적인 neutral 기반, 과한 accent 변화 없음

### 구현 노트

- 기존에 같은 역할의 컴포넌트가 있으면 토큰 교체부터 시작
- variant prop으로 시각적 변형을 관리 (하드코딩 금지)
- 빈 상태(empty-state)와 에러 상태를 반드시 처리
- 좁은 UI 텍스트는 Pretendard 기준 label line-height 1.4-1.5를 참고해 뭉침을 방지
- 텍스트 위계가 핵심 — 컬러보다 weight/size로 구분

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

- [editorial+precise+trustworthy] hover: 텍스트 underline 또는 color shift, 장식적 효과 없음 + 정확한 border/outline 변화 + 예측 가능하고 일관된 hover 패턴
- [editorial+precise+trustworthy] motion: 콘텐츠 전환 위주, UI chrome 모션 최소화 + 120-180ms, 군더더기 없는 전환 + 모든 전환에 동일한 easing/duration
- [editorial+precise+trustworthy] color: 타이포그래피로 위계 형성, 컬러보다 weight/size 활용 + 정확한 semantic 분리, 모호한 중간 톤 지양 + 안정적인 neutral 기반, 과한 accent 변화 없음

### 레퍼런스 근거

- **Carbon Design System**: Bringing IBM Carbon Design System Knowledge Into AI Workflows With Carbon MCP Will Scott, PhD
- **Primer**: Design guidelines covering common user workflows. Octicons

### 구현 노트

- 기존에 같은 역할의 컴포넌트가 있으면 토큰 교체부터 시작
- variant prop으로 시각적 변형을 관리 (하드코딩 금지)
- 텍스트 위계가 핵심 — 컬러보다 weight/size로 구분

---

## feedback / confidence-meter

**역할**: Confidence or certainty meter with explanation and threshold labels

**Slot archetype**: `advanced:confidence-meter`

### Advanced Usage

Use when:
- AI or policy outcome includes uncertainty
- users must decide whether to trust, edit, or escalate
Avoid when:
- confidence cannot be explained or calibrated
Pairs with: risk-summary-card, policy-matrix, tool-call-trace

### 구조 (Anatomy)

- meter
- value-label
- threshold-labels
- driver-summary
- tooltip(optional)

### 상태 (States)

| 상태 | 설명 |
|------|------|
| `low` | low |
| `medium` | medium |
| `high` | high |
| `unknown` | unknown |

### 토큰 바인딩

```
track: var(--color-surface-muted)
fill: var(--color-brand-primary)
low: var(--color-danger)
medium: var(--color-warning)
high: var(--color-success)
radius: var(--radius-pill)
```

### 접근성

- role="meter" with aria-valuemin / aria-valuemax / aria-valuenow
- visible text explains what the score means
- do not encode trust solely with color

### 브랜드 적용

- [editorial+precise+trustworthy] feedback: 콘텐츠 맥락 안에서 인라인 표시, 토스트보다 인라인 선호 + 명확한 상태 구분, 진행률/결과를 수치로 표시 + 결과를 반드시 확인, 실패 시 복구 방법 안내
- [editorial+precise+trustworthy] motion: 콘텐츠 전환 위주, UI chrome 모션 최소화 + 120-180ms, 군더더기 없는 전환 + 모든 전환에 동일한 easing/duration
- [editorial+precise+trustworthy] color: 타이포그래피로 위계 형성, 컬러보다 weight/size 활용 + 정확한 semantic 분리, 모호한 중간 톤 지양 + 안정적인 neutral 기반, 과한 accent 변화 없음

### 레퍼런스 근거

- **Carbon Design System**: We welcome all feedback, designs, or ideas in order to produce the best possible experience for our users. If you're interested in contributing, ch...
- **Primer**: Messaging components are used to provide important and relevant information to the user, including feedback, contextual information, product update...

### 구현 노트

- 기존에 같은 역할의 컴포넌트가 있으면 토큰 교체부터 시작
- variant prop으로 시각적 변형을 관리 (하드코딩 금지)
- auto-dismiss 시간은 내용 길이에 비례 (기본 5초)
- 반응형 검증: 320px, 360px, 390px, 430px에서 control overflow와 viewport horizontal scroll이 없어야 함
- action row는 narrow viewport에서 `flex-wrap: wrap` 또는 세로 stack으로 전환하고, overflow-x 숨김으로 문제를 덮지 않음
- 텍스트 위계가 핵심 — 컬러보다 weight/size로 구분

---

## data-display / decision-record-card

**역할**: Auditable decision record summarizing decision, actor, evidence, and retention

**Slot archetype**: `advanced:decision-record-card`

### Advanced Usage

Use when:
- a reviewer or AI-assisted workflow reaches a durable decision
- regulated teams need record ids and retention status
Avoid when:
- the action is transient and not auditable
Pairs with: audit-timeline, approval-rail, citation-drawer

### 구조 (Anatomy)

- card
- record-id
- decision-summary
- actor-row
- evidence-links
- retention-state

### 상태 (States)

| 상태 | 설명 |
|------|------|
| `draft` | draft |
| `recorded` | recorded |
| `locked` | locked |
| `expired` | expired |

### 토큰 바인딩

```
surface: var(--color-surface)
border: var(--color-border)
locked: var(--color-brand-primary)
expired: var(--color-warning)
mono: var(--font-mono)
```

### 접근성

- record id is selectable text
- locked and expired states include text labels
- evidence links are grouped under an accessible heading

### 브랜드 적용

- [editorial+precise+trustworthy] density: 넉넉한 line-height와 margin, 읽기 편한 간격 + 엄격한 spacing scale 준수, 임의 값 금지 + 기존 레이아웃 유지, 갑작스런 위치 변경 없음
- [editorial+precise+trustworthy] color: 타이포그래피로 위계 형성, 컬러보다 weight/size 활용 + 정확한 semantic 분리, 모호한 중간 톤 지양 + 안정적인 neutral 기반, 과한 accent 변화 없음

### 구현 노트

- 기존에 같은 역할의 컴포넌트가 있으면 토큰 교체부터 시작
- variant prop으로 시각적 변형을 관리 (하드코딩 금지)
- 빈 상태(empty-state)와 에러 상태를 반드시 처리
- 좁은 UI 텍스트는 Pretendard 기준 label line-height 1.4-1.5를 참고해 뭉침을 방지
- 텍스트 위계가 핵심 — 컬러보다 weight/size로 구분

---

## overlay / inspector-drawer

**역할**: Contextual detail drawer for properties, policy facts, or record metadata

**Slot archetype**: `advanced:inspector-drawer`

### Advanced Usage

Use when:
- a selected item needs rich detail without leaving the main workflow
- users need source facts, owners, versions, or retention metadata
Avoid when:
- the detail is short enough for an inline disclosure
Pairs with: policy-matrix, citation-drawer, decision-record-card

### 구조 (Anatomy)

- drawer
- header
- section-list
- property-row
- action-row
- close-button

### 상태 (States)

| 상태 | 설명 |
|------|------|
| `closed` | 닫힌 상태 |
| `open` | 열린 상태 |
| `loading` | 로딩 중 (스피너 표시) |
| `dirty` | dirty |

### 토큰 바인딩

```
surface: var(--color-surface-elevated)
border: var(--color-border)
section-surface: var(--color-surface-muted)
radius: var(--radius-lg)
padding: var(--space-24)
```

### 접근성

- role="dialog" or complementary region depending on modality
- aria-labelledby connects drawer title
- focus moves into drawer when modal and returns to trigger on close

### 브랜드 적용

- [editorial+precise+trustworthy] motion: 콘텐츠 전환 위주, UI chrome 모션 최소화 + 120-180ms, 군더더기 없는 전환 + 모든 전환에 동일한 easing/duration
- [editorial+precise+trustworthy] density: 넉넉한 line-height와 margin, 읽기 편한 간격 + 엄격한 spacing scale 준수, 임의 값 금지 + 기존 레이아웃 유지, 갑작스런 위치 변경 없음

### 레퍼런스 근거

- **Primer**: ActionMenu is composed of ActionList and Overlay patterns used for quick actions and selections. AnchoredOverlay

### 구현 노트

- 기존에 같은 역할의 컴포넌트가 있으면 토큰 교체부터 시작
- variant prop으로 시각적 변형을 관리 (하드코딩 금지)
- Escape / backdrop click으로 닫기, 열 때 첫 focusable 요소로 이동
- 텍스트 위계가 핵심 — 컬러보다 weight/size로 구분

---

## data-display / risk-summary-card

**역할**: Compact risk score card with drivers, confidence, and recommended mitigation

**Slot archetype**: `advanced:risk-summary-card`

### Advanced Usage

Use when:
- users need a fast read of risk before drilling into policy details
- AI confidence or compliance severity must be visible
Avoid when:
- score cannot be explained with drivers
Pairs with: policy-matrix, confidence-meter, exception-queue

### 구조 (Anatomy)

- card
- score
- severity-label
- driver-list
- confidence-meter
- mitigation-action

### 상태 (States)

| 상태 | 설명 |
|------|------|
| `low` | low |
| `medium` | medium |
| `high` | high |
| `loading` | 로딩 중 (스피너 표시) |

### 토큰 바인딩

```
surface: var(--color-surface)
border: var(--color-border)
low: var(--color-success)
medium: var(--color-warning)
high: var(--color-danger)
radius: var(--radius-lg)
```

### 접근성

- score includes label and scale, not only number
- severity is text plus icon/color
- mitigation action is keyboard reachable

### 브랜드 적용

- [editorial+precise+trustworthy] density: 넉넉한 line-height와 margin, 읽기 편한 간격 + 엄격한 spacing scale 준수, 임의 값 금지 + 기존 레이아웃 유지, 갑작스런 위치 변경 없음
- [editorial+precise+trustworthy] color: 타이포그래피로 위계 형성, 컬러보다 weight/size 활용 + 정확한 semantic 분리, 모호한 중간 톤 지양 + 안정적인 neutral 기반, 과한 accent 변화 없음

### 구현 노트

- 기존에 같은 역할의 컴포넌트가 있으면 토큰 교체부터 시작
- variant prop으로 시각적 변형을 관리 (하드코딩 금지)
- 빈 상태(empty-state)와 에러 상태를 반드시 처리
- 좁은 UI 텍스트는 Pretendard 기준 label line-height 1.4-1.5를 참고해 뭉침을 방지
- 텍스트 위계가 핵심 — 컬러보다 weight/size로 구분

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

- [editorial+precise+trustworthy] hover: 텍스트 underline 또는 color shift, 장식적 효과 없음 + 정확한 border/outline 변화 + 예측 가능하고 일관된 hover 패턴
- [editorial+precise+trustworthy] motion: 콘텐츠 전환 위주, UI chrome 모션 최소화 + 120-180ms, 군더더기 없는 전환 + 모든 전환에 동일한 easing/duration
- [editorial+precise+trustworthy] color: 타이포그래피로 위계 형성, 컬러보다 weight/size 활용 + 정확한 semantic 분리, 모호한 중간 톤 지양 + 안정적인 neutral 기반, 과한 accent 변화 없음

### 레퍼런스 근거

- **Carbon Design System**: AI chat is a conversational framework between a user and an AI that can aid in creating tasks, finding insights, tracking documents, and more. For ...
- **Primer**: The GitHub Design Infrastructure and Design Engineering teams build and maintain Primer — this includes our CSS framework, style guide documentatio...

### 구현 노트

- 기존에 같은 역할의 컴포넌트가 있으면 토큰 교체부터 시작
- variant prop으로 시각적 변형을 관리 (하드코딩 금지)
- 텍스트 위계가 핵심 — 컬러보다 weight/size로 구분
