# PL Stats Component Specs

총 56개 컴포넌트 | 패밀리: button, data-display, feedback, input, marketing, navigation, overlay

## 구현 원칙 (Non-negotiable)

이 스펙의 모든 컴포넌트를 구현할 때 반드시 지킨다:

1. **이모지를 UI로 쓰지 않는다** — 🎨 ✅ 🔥 ⚡ 🚀 ❌ ⭐ 📊 등 이모지를 아이콘, 상태 표시, 버튼 장식, 네비게이션 지표 자리에 절대 넣지 않는다. 아이콘 자리에는 SVG 컴포넌트 또는 Lucide/Heroicons/Phosphor/Tabler 라이브러리를 사용한다.
2. **컴포넌트를 직접 구현한다** — 아래 각 컴포넌트의 anatomy(구조), states(상태), 토큰 바인딩, 접근성 규칙을 그대로 따라 완전하게 구현한다. '임시', 'TODO', '플레이스홀더' 같은 반쪽 구현을 남기지 않는다.
3. **라이브러리 기본 스타일 금지** — 라이브러리 컴포넌트를 그대로 import해서 쓰지 않는다. 반드시 디자인 토큰(--color-*, --space-*, --radius-*, --font-*)으로 스타일을 명시적으로 바인딩한다.
4. **접근성은 옵션이 아니다** — 각 컴포넌트의 '접근성' 섹션에 정의된 role, aria-*, label, focus 관리 규칙을 전부 적용한다.
5. **hex 값 하드코딩 금지** — 색상은 반드시 semantic token을 경유한다 (예: `color: var(--color-ink)` not `color: #2C2C2C`).

## 브랜드 적용 규칙

- **hover**: 확실한 색상 변화 또는 scale 변화 + 정확한 border/outline 변화
- **motion**: 200-300ms, 시각적으로 확실한 전환 + 120-180ms, 군더더기 없는 전환
- **color**: 대비가 강한 accent, primary에 집중 + 정확한 semantic 분리, 모호한 중간 톤 지양
- **density**: 큰 터치 영역, 핵심 요소 강조 + 엄격한 spacing scale 준수, 임의 값 금지
- **feedback**: 눈에 띄는 성공/에러 표시, 컬러 블록 활용 + 명확한 상태 구분, 진행률/결과를 수치로 표시

## Typography Guardrails

- 한글 기반 제품은 line-break / scale / tracking을 영문 랜딩 기본값으로 처리하지 않고, 아래 가드레일을 구현 기본값으로 사용한다.
- Headline: Spoqa Han Sans Neo | line-height 1.2-1.3 | tracking -0.02em
- Body: Spoqa Han Sans Neo | line-height 1.5-1.6 | label line-height 1.4-1.5
- Wrap defaults: headline word-break=keep-all, headline text-wrap=balance, body word-break=keep-all
- Scale guidance: 한글 hero/section heading은 영문 시안보다 한 단계 작은 스케일에서 시작해 wrap을 확인한 뒤 확장한다.
- 한글 카피는 `word-break: keep-all`과 `overflow-wrap: normal`을 기본값으로 두고, 주요 헤딩에서 지원되면 `text-wrap: balance`를 사용한다.
- 한글 헤딩에는 breakpoint 검증 전 강제 `<br />`를 넣지 않는다. 줄바꿈이 필요하면 먼저 컨테이너 폭과 type scale을 조정한다.
- 한글 화면은 영문 시안의 `ch` 기준이나 single-line slogan 가정에 맞추지 말고, 실제 한글 문장으로 wrap을 검증한다.
- 폭이 넓은 한글 또는 명조 헤딩은 영문 hero보다 한 단계 작은 display scale에서 시작하고, 줄바꿈이 안정적일 때만 키운다.

---

## button / primary-button

**역할**: 주요 행동을 유도하는 CTA 버튼

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

### 브랜드 적용

- [bold+precise] hover: 확실한 색상 변화 또는 scale 변화 + 정확한 border/outline 변화
- [bold+precise] motion: 200-300ms, 시각적으로 확실한 전환 + 120-180ms, 군더더기 없는 전환
- [bold+precise] color: 대비가 강한 accent, primary에 집중 + 정확한 semantic 분리, 모호한 중간 톤 지양

### 레퍼런스 근거

- **Carbon Design System**: These components can toggle between the AI variant and the default variant depending on the user’s interaction. If the user manually overrides the ...
- **Primer**: I get so much joy from writing HTML and CSS, and design systems are one level up - systematically making UIs accessible and consistent. I love conc...

### 구현 노트

- 기존에 같은 역할의 컴포넌트가 있으면 토큰 교체부터 시작
- variant prop으로 시각적 변형을 관리 (하드코딩 금지)
- size prop: sm / md / lg (터치 영역은 항상 최소 44px 보장)

---

## button / secondary-button

**역할**: 보조 행동 버튼

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

### 브랜드 적용

- [bold+precise] hover: 확실한 색상 변화 또는 scale 변화 + 정확한 border/outline 변화
- [bold+precise] motion: 200-300ms, 시각적으로 확실한 전환 + 120-180ms, 군더더기 없는 전환
- [bold+precise] color: 대비가 강한 accent, primary에 집중 + 정확한 semantic 분리, 모호한 중간 톤 지양

### 레퍼런스 근거

- **Carbon Design System**: These components can toggle between the AI variant and the default variant depending on the user’s interaction. If the user manually overrides the ...
- **Primer**: I get so much joy from writing HTML and CSS, and design systems are one level up - systematically making UIs accessible and consistent. I love conc...

### 구현 노트

- 기존에 같은 역할의 컴포넌트가 있으면 토큰 교체부터 시작
- variant prop으로 시각적 변형을 관리 (하드코딩 금지)
- size prop: sm / md / lg (터치 영역은 항상 최소 44px 보장)

---

## button / ghost-button

**역할**: 최소한의 시각적 무게를 가진 버튼

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

### 브랜드 적용

- [bold+precise] hover: 확실한 색상 변화 또는 scale 변화 + 정확한 border/outline 변화
- [bold+precise] motion: 200-300ms, 시각적으로 확실한 전환 + 120-180ms, 군더더기 없는 전환
- [bold+precise] color: 대비가 강한 accent, primary에 집중 + 정확한 semantic 분리, 모호한 중간 톤 지양

### 레퍼런스 근거

- **Carbon Design System**: These components can toggle between the AI variant and the default variant depending on the user’s interaction. If the user manually overrides the ...
- **Primer**: I get so much joy from writing HTML and CSS, and design systems are one level up - systematically making UIs accessible and consistent. I love conc...

### 구현 노트

- 기존에 같은 역할의 컴포넌트가 있으면 토큰 교체부터 시작
- variant prop으로 시각적 변형을 관리 (하드코딩 금지)
- size prop: sm / md / lg (터치 영역은 항상 최소 44px 보장)

---

## button / icon-button

**역할**: 아이콘만 있는 액션 버튼

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

### 브랜드 적용

- [bold+precise] hover: 확실한 색상 변화 또는 scale 변화 + 정확한 border/outline 변화
- [bold+precise] motion: 200-300ms, 시각적으로 확실한 전환 + 120-180ms, 군더더기 없는 전환
- [bold+precise] color: 대비가 강한 accent, primary에 집중 + 정확한 semantic 분리, 모호한 중간 톤 지양

### 레퍼런스 근거

- **Carbon Design System**: These components can toggle between the AI variant and the default variant depending on the user’s interaction. If the user manually overrides the ...
- **Primer**: I get so much joy from writing HTML and CSS, and design systems are one level up - systematically making UIs accessible and consistent. I love conc...

### 구현 노트

- 기존에 같은 역할의 컴포넌트가 있으면 토큰 교체부터 시작
- variant prop으로 시각적 변형을 관리 (하드코딩 금지)
- size prop: sm / md / lg (터치 영역은 항상 최소 44px 보장)

---

## button / link-button

**역할**: 텍스트 링크 스타일 버튼

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

### 브랜드 적용

- [bold+precise] hover: 확실한 색상 변화 또는 scale 변화 + 정확한 border/outline 변화
- [bold+precise] motion: 200-300ms, 시각적으로 확실한 전환 + 120-180ms, 군더더기 없는 전환
- [bold+precise] color: 대비가 강한 accent, primary에 집중 + 정확한 semantic 분리, 모호한 중간 톤 지양

### 레퍼런스 근거

- **Carbon Design System**: These components can toggle between the AI variant and the default variant depending on the user’s interaction. If the user manually overrides the ...
- **Primer**: I get so much joy from writing HTML and CSS, and design systems are one level up - systematically making UIs accessible and consistent. I love conc...

### 구현 노트

- 기존에 같은 역할의 컴포넌트가 있으면 토큰 교체부터 시작
- variant prop으로 시각적 변형을 관리 (하드코딩 금지)
- size prop: sm / md / lg (터치 영역은 항상 최소 44px 보장)

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

- [bold+precise] density: 큰 터치 영역, 핵심 요소 강조 + 엄격한 spacing scale 준수, 임의 값 금지
- [bold+precise] color: 대비가 강한 accent, primary에 집중 + 정확한 semantic 분리, 모호한 중간 톤 지양

### 레퍼런스 근거

- **Carbon Design System**: Data table Modal
- **Primer**: DataTable DataTable is a 2-dimensional data structure where each row is an item, and each column is a data point about the item.

### 구현 노트

- 기존에 같은 역할의 컴포넌트가 있으면 토큰 교체부터 시작
- variant prop으로 시각적 변형을 관리 (하드코딩 금지)
- 빈 상태(empty-state)와 에러 상태를 반드시 처리
- 좁은 UI 텍스트는 Spoqa Han Sans Neo 기준 label line-height 1.4-1.5를 참고해 뭉침을 방지

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

- [bold+precise] density: 큰 터치 영역, 핵심 요소 강조 + 엄격한 spacing scale 준수, 임의 값 금지
- [bold+precise] color: 대비가 강한 accent, primary에 집중 + 정확한 semantic 분리, 모호한 중간 톤 지양

### 구현 노트

- 기존에 같은 역할의 컴포넌트가 있으면 토큰 교체부터 시작
- variant prop으로 시각적 변형을 관리 (하드코딩 금지)
- 빈 상태(empty-state)와 에러 상태를 반드시 처리
- 좁은 UI 텍스트는 Spoqa Han Sans Neo 기준 label line-height 1.4-1.5를 참고해 뭉침을 방지

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

- [bold+precise] density: 큰 터치 영역, 핵심 요소 강조 + 엄격한 spacing scale 준수, 임의 값 금지
- [bold+precise] color: 대비가 강한 accent, primary에 집중 + 정확한 semantic 분리, 모호한 중간 톤 지양

### 구현 노트

- 기존에 같은 역할의 컴포넌트가 있으면 토큰 교체부터 시작
- variant prop으로 시각적 변형을 관리 (하드코딩 금지)
- 빈 상태(empty-state)와 에러 상태를 반드시 처리
- 좁은 UI 텍스트는 Spoqa Han Sans Neo 기준 label line-height 1.4-1.5를 참고해 뭉침을 방지

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

- [bold+precise] hover: 확실한 색상 변화 또는 scale 변화 + 정확한 border/outline 변화
- [bold+precise] density: 큰 터치 영역, 핵심 요소 강조 + 엄격한 spacing scale 준수, 임의 값 금지
- [bold+precise] motion: 200-300ms, 시각적으로 확실한 전환 + 120-180ms, 군더더기 없는 전환

### 레퍼런스 근거

- **Carbon Design System**: Library menu navigation There are two kinds of symbols — library symbols and document symbols. Library symbols are available in any Sketch document...
- **Primer**: Octicon nav items navigation 12 px

### 구현 노트

- 기존에 같은 역할의 컴포넌트가 있으면 토큰 교체부터 시작
- variant prop으로 시각적 변형을 관리 (하드코딩 금지)
- active 상태는 URL/라우터와 자동 동기화
- 좁은 UI 텍스트는 Spoqa Han Sans Neo 기준 label line-height 1.4-1.5를 참고해 뭉침을 방지

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

- [bold+precise] hover: 확실한 색상 변화 또는 scale 변화 + 정확한 border/outline 변화
- [bold+precise] density: 큰 터치 영역, 핵심 요소 강조 + 엄격한 spacing scale 준수, 임의 값 금지
- [bold+precise] feedback: 눈에 띄는 성공/에러 표시, 컬러 블록 활용 + 명확한 상태 구분, 진행률/결과를 수치로 표시

### 레퍼런스 근거

- **Carbon Design System**: Number input Text input
- **Primer**: I worked in data visualization and map-making for most of my career, and solving design problems with data is my jam. To me there's something uniqu...

### 구현 노트

- 기존에 같은 역할의 컴포넌트가 있으면 토큰 교체부터 시작
- variant prop으로 시각적 변형을 관리 (하드코딩 금지)
- error 상태에서 helper text → error message로 자동 전환
- label은 항상 visible (placeholder만으로 대체 금지)

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

- [bold+precise] hover: 확실한 색상 변화 또는 scale 변화 + 정확한 border/outline 변화
- [bold+precise] density: 큰 터치 영역, 핵심 요소 강조 + 엄격한 spacing scale 준수, 임의 값 금지
- [bold+precise] feedback: 눈에 띄는 성공/에러 표시, 컬러 블록 활용 + 명확한 상태 구분, 진행률/결과를 수치로 표시

### 레퍼런스 근거

- **Carbon Design System**: Number input Text input
- **Primer**: I worked in data visualization and map-making for most of my career, and solving design problems with data is my jam. To me there's something uniqu...

### 구현 노트

- 기존에 같은 역할의 컴포넌트가 있으면 토큰 교체부터 시작
- variant prop으로 시각적 변형을 관리 (하드코딩 금지)
- error 상태에서 helper text → error message로 자동 전환
- label은 항상 visible (placeholder만으로 대체 금지)

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

- [bold+precise] density: 큰 터치 영역, 핵심 요소 강조 + 엄격한 spacing scale 준수, 임의 값 금지
- [bold+precise] color: 대비가 강한 accent, primary에 집중 + 정확한 semantic 분리, 모호한 중간 톤 지양

### 구현 노트

- 기존에 같은 역할의 컴포넌트가 있으면 토큰 교체부터 시작
- variant prop으로 시각적 변형을 관리 (하드코딩 금지)
- 빈 상태(empty-state)와 에러 상태를 반드시 처리
- 좁은 UI 텍스트는 Spoqa Han Sans Neo 기준 label line-height 1.4-1.5를 참고해 뭉침을 방지

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

- [bold+precise] hover: 확실한 색상 변화 또는 scale 변화 + 정확한 border/outline 변화
- [bold+precise] density: 큰 터치 영역, 핵심 요소 강조 + 엄격한 spacing scale 준수, 임의 값 금지
- [bold+precise] feedback: 눈에 띄는 성공/에러 표시, 컬러 블록 활용 + 명확한 상태 구분, 진행률/결과를 수치로 표시

### 레퍼런스 근거

- **Carbon Design System**: Number input Text input
- **Primer**: I worked in data visualization and map-making for most of my career, and solving design problems with data is my jam. To me there's something uniqu...

### 구현 노트

- 기존에 같은 역할의 컴포넌트가 있으면 토큰 교체부터 시작
- variant prop으로 시각적 변형을 관리 (하드코딩 금지)
- error 상태에서 helper text → error message로 자동 전환
- label은 항상 visible (placeholder만으로 대체 금지)

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

- [bold+precise] motion: 200-300ms, 시각적으로 확실한 전환 + 120-180ms, 군더더기 없는 전환
- [bold+precise] density: 큰 터치 영역, 핵심 요소 강조 + 엄격한 spacing scale 준수, 임의 값 금지

### 레퍼런스 근거

- **Primer**: Autocomplete Autocomplete allows users to quickly filter through a list of options and pick one or more values for a field.

### 구현 노트

- 기존에 같은 역할의 컴포넌트가 있으면 토큰 교체부터 시작
- variant prop으로 시각적 변형을 관리 (하드코딩 금지)
- Escape / backdrop click으로 닫기, 열 때 첫 focusable 요소로 이동

---

## data-display / stat-card

**역할**: 주요 수치를 표시하는 통계 카드

**탐지 출처**: dashboard cards

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

- [bold+precise] density: 큰 터치 영역, 핵심 요소 강조 + 엄격한 spacing scale 준수, 임의 값 금지
- [bold+precise] color: 대비가 강한 accent, primary에 집중 + 정확한 semantic 분리, 모호한 중간 톤 지양

### 구현 노트

- 기존에 같은 역할의 컴포넌트가 있으면 토큰 교체부터 시작
- variant prop으로 시각적 변형을 관리 (하드코딩 금지)
- 빈 상태(empty-state)와 에러 상태를 반드시 처리
- 좁은 UI 텍스트는 Spoqa Han Sans Neo 기준 label line-height 1.4-1.5를 참고해 뭉침을 방지

---

## data-display / insight-card

**역할**: 인사이트나 트렌드를 요약하는 카드

**탐지 출처**: dashboard cards

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

- [bold+precise] density: 큰 터치 영역, 핵심 요소 강조 + 엄격한 spacing scale 준수, 임의 값 금지
- [bold+precise] color: 대비가 강한 accent, primary에 집중 + 정확한 semantic 분리, 모호한 중간 톤 지양

### 구현 노트

- 기존에 같은 역할의 컴포넌트가 있으면 토큰 교체부터 시작
- variant prop으로 시각적 변형을 관리 (하드코딩 금지)
- 빈 상태(empty-state)와 에러 상태를 반드시 처리
- 좁은 UI 텍스트는 Spoqa Han Sans Neo 기준 label line-height 1.4-1.5를 참고해 뭉침을 방지

---

## data-display / activity-card

**역할**: 최근 활동 피드 카드

**탐지 출처**: dashboard cards

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

- [bold+precise] density: 큰 터치 영역, 핵심 요소 강조 + 엄격한 spacing scale 준수, 임의 값 금지
- [bold+precise] color: 대비가 강한 accent, primary에 집중 + 정확한 semantic 분리, 모호한 중간 톤 지양

### 구현 노트

- 기존에 같은 역할의 컴포넌트가 있으면 토큰 교체부터 시작
- variant prop으로 시각적 변형을 관리 (하드코딩 금지)
- 빈 상태(empty-state)와 에러 상태를 반드시 처리
- 좁은 UI 텍스트는 Spoqa Han Sans Neo 기준 label line-height 1.4-1.5를 참고해 뭉침을 방지

---

## data-display / section-header

**역할**: 대시보드 섹션 구분 헤더

**탐지 출처**: dashboard cards

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

- [bold+precise] density: 큰 터치 영역, 핵심 요소 강조 + 엄격한 spacing scale 준수, 임의 값 금지
- [bold+precise] color: 대비가 강한 accent, primary에 집중 + 정확한 semantic 분리, 모호한 중간 톤 지양

### 구현 노트

- 기존에 같은 역할의 컴포넌트가 있으면 토큰 교체부터 시작
- variant prop으로 시각적 변형을 관리 (하드코딩 금지)
- 빈 상태(empty-state)와 에러 상태를 반드시 처리
- 좁은 UI 텍스트는 Spoqa Han Sans Neo 기준 label line-height 1.4-1.5를 참고해 뭉침을 방지

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

- [bold+precise] hover: 확실한 색상 변화 또는 scale 변화 + 정확한 border/outline 변화
- [bold+precise] density: 큰 터치 영역, 핵심 요소 강조 + 엄격한 spacing scale 준수, 임의 값 금지
- [bold+precise] feedback: 눈에 띄는 성공/에러 표시, 컬러 블록 활용 + 명확한 상태 구분, 진행률/결과를 수치로 표시

### 레퍼런스 근거

- **Carbon Design System**: Number input Text input
- **Primer**: I worked in data visualization and map-making for most of my career, and solving design problems with data is my jam. To me there's something uniqu...

### 구현 노트

- 기존에 같은 역할의 컴포넌트가 있으면 토큰 교체부터 시작
- variant prop으로 시각적 변형을 관리 (하드코딩 금지)
- error 상태에서 helper text → error message로 자동 전환
- label은 항상 visible (placeholder만으로 대체 금지)

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

- [bold+precise] hover: 확실한 색상 변화 또는 scale 변화 + 정확한 border/outline 변화
- [bold+precise] density: 큰 터치 영역, 핵심 요소 강조 + 엄격한 spacing scale 준수, 임의 값 금지
- [bold+precise] feedback: 눈에 띄는 성공/에러 표시, 컬러 블록 활용 + 명확한 상태 구분, 진행률/결과를 수치로 표시

### 레퍼런스 근거

- **Carbon Design System**: Number input Text input
- **Primer**: I worked in data visualization and map-making for most of my career, and solving design problems with data is my jam. To me there's something uniqu...

### 구현 노트

- 기존에 같은 역할의 컴포넌트가 있으면 토큰 교체부터 시작
- variant prop으로 시각적 변형을 관리 (하드코딩 금지)
- error 상태에서 helper text → error message로 자동 전환
- label은 항상 visible (placeholder만으로 대체 금지)

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

- [bold+precise] hover: 확실한 색상 변화 또는 scale 변화 + 정확한 border/outline 변화
- [bold+precise] density: 큰 터치 영역, 핵심 요소 강조 + 엄격한 spacing scale 준수, 임의 값 금지
- [bold+precise] feedback: 눈에 띄는 성공/에러 표시, 컬러 블록 활용 + 명확한 상태 구분, 진행률/결과를 수치로 표시

### 레퍼런스 근거

- **Carbon Design System**: Select Data table
- **Primer**: Primer color design tokens are made available within data-attribute selectors on the body tag or other high level dom element. There are three dist...

### 구현 노트

- 기존에 같은 역할의 컴포넌트가 있으면 토큰 교체부터 시작
- variant prop으로 시각적 변형을 관리 (하드코딩 금지)
- error 상태에서 helper text → error message로 자동 전환
- label은 항상 visible (placeholder만으로 대체 금지)

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

- [bold+precise] hover: 확실한 색상 변화 또는 scale 변화 + 정확한 border/outline 변화
- [bold+precise] density: 큰 터치 영역, 핵심 요소 강조 + 엄격한 spacing scale 준수, 임의 값 금지
- [bold+precise] feedback: 눈에 띄는 성공/에러 표시, 컬러 블록 활용 + 명확한 상태 구분, 진행률/결과를 수치로 표시

### 레퍼런스 근거

- **Carbon Design System**: Checkbox Form
- **Primer**: I worked in data visualization and map-making for most of my career, and solving design problems with data is my jam. To me there's something uniqu...

### 구현 노트

- 기존에 같은 역할의 컴포넌트가 있으면 토큰 교체부터 시작
- variant prop으로 시각적 변형을 관리 (하드코딩 금지)
- error 상태에서 helper text → error message로 자동 전환
- label은 항상 visible (placeholder만으로 대체 금지)

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

- [bold+precise] hover: 확실한 색상 변화 또는 scale 변화 + 정확한 border/outline 변화
- [bold+precise] density: 큰 터치 영역, 핵심 요소 강조 + 엄격한 spacing scale 준수, 임의 값 금지
- [bold+precise] feedback: 눈에 띄는 성공/에러 표시, 컬러 블록 활용 + 명확한 상태 구분, 진행률/결과를 수치로 표시

### 레퍼런스 근거

- **Carbon Design System**: Number input Text input
- **Primer**: I worked in data visualization and map-making for most of my career, and solving design problems with data is my jam. To me there's something uniqu...

### 구현 노트

- 기존에 같은 역할의 컴포넌트가 있으면 토큰 교체부터 시작
- variant prop으로 시각적 변형을 관리 (하드코딩 금지)
- error 상태에서 helper text → error message로 자동 전환
- label은 항상 visible (placeholder만으로 대체 금지)

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

- [bold+precise] hover: 확실한 색상 변화 또는 scale 변화 + 정확한 border/outline 변화
- [bold+precise] density: 큰 터치 영역, 핵심 요소 강조 + 엄격한 spacing scale 준수, 임의 값 금지
- [bold+precise] feedback: 눈에 띄는 성공/에러 표시, 컬러 블록 활용 + 명확한 상태 구분, 진행률/결과를 수치로 표시

### 레퍼런스 근거

- **Carbon Design System**: Number input Text input
- **Primer**: I worked in data visualization and map-making for most of my career, and solving design problems with data is my jam. To me there's something uniqu...

### 구현 노트

- 기존에 같은 역할의 컴포넌트가 있으면 토큰 교체부터 시작
- variant prop으로 시각적 변형을 관리 (하드코딩 금지)
- error 상태에서 helper text → error message로 자동 전환
- label은 항상 visible (placeholder만으로 대체 금지)

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

### 브랜드 적용

- [bold+precise] hover: 확실한 색상 변화 또는 scale 변화 + 정확한 border/outline 변화
- [bold+precise] motion: 200-300ms, 시각적으로 확실한 전환 + 120-180ms, 군더더기 없는 전환
- [bold+precise] color: 대비가 강한 accent, primary에 집중 + 정확한 semantic 분리, 모호한 중간 톤 지양

### 레퍼런스 근거

- **Carbon Design System**: These components can toggle between the AI variant and the default variant depending on the user’s interaction. If the user manually overrides the ...
- **Primer**: I get so much joy from writing HTML and CSS, and design systems are one level up - systematically making UIs accessible and consistent. I love conc...

### 구현 노트

- 기존에 같은 역할의 컴포넌트가 있으면 토큰 교체부터 시작
- variant prop으로 시각적 변형을 관리 (하드코딩 금지)
- size prop: sm / md / lg (터치 영역은 항상 최소 44px 보장)

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

- [bold+precise] density: 큰 터치 영역, 핵심 요소 강조 + 엄격한 spacing scale 준수, 임의 값 금지
- [bold+precise] color: 대비가 강한 accent, primary에 집중 + 정확한 semantic 분리, 모호한 중간 톤 지양

### 레퍼런스 근거

- **Carbon Design System**: Tag Date picker
- **Primer**: Primer color design tokens are made available within data-attribute selectors on the body tag or other high level dom element. There are three dist...

### 구현 노트

- 기존에 같은 역할의 컴포넌트가 있으면 토큰 교체부터 시작
- variant prop으로 시각적 변형을 관리 (하드코딩 금지)
- 빈 상태(empty-state)와 에러 상태를 반드시 처리
- 좁은 UI 텍스트는 Spoqa Han Sans Neo 기준 label line-height 1.4-1.5를 참고해 뭉침을 방지

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

- [bold+precise] feedback: 눈에 띄는 성공/에러 표시, 컬러 블록 활용 + 명확한 상태 구분, 진행률/결과를 수치로 표시
- [bold+precise] motion: 200-300ms, 시각적으로 확실한 전환 + 120-180ms, 군더더기 없는 전환
- [bold+precise] color: 대비가 강한 accent, primary에 집중 + 정확한 semantic 분리, 모호한 중간 톤 지양

### 레퍼런스 근거

- **Carbon Design System**: We welcome all feedback, designs, or ideas in order to produce the best possible experience for our users. If you're interested in contributing, ch...
- **Primer**: Messaging components are used to provide important and relevant information to the user, including feedback, contextual information, product update...

### 구현 노트

- 기존에 같은 역할의 컴포넌트가 있으면 토큰 교체부터 시작
- variant prop으로 시각적 변형을 관리 (하드코딩 금지)
- auto-dismiss 시간은 내용 길이에 비례 (기본 5초)

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

- [bold+precise] hover: 확실한 색상 변화 또는 scale 변화 + 정확한 border/outline 변화
- [bold+precise] density: 큰 터치 영역, 핵심 요소 강조 + 엄격한 spacing scale 준수, 임의 값 금지
- [bold+precise] feedback: 눈에 띄는 성공/에러 표시, 컬러 블록 활용 + 명확한 상태 구분, 진행률/결과를 수치로 표시

### 레퍼런스 근거

- **Carbon Design System**: Number input Text input
- **Primer**: I worked in data visualization and map-making for most of my career, and solving design problems with data is my jam. To me there's something uniqu...

### 구현 노트

- 기존에 같은 역할의 컴포넌트가 있으면 토큰 교체부터 시작
- variant prop으로 시각적 변형을 관리 (하드코딩 금지)
- error 상태에서 helper text → error message로 자동 전환
- label은 항상 visible (placeholder만으로 대체 금지)

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

- [bold+precise] density: 큰 터치 영역, 핵심 요소 강조 + 엄격한 spacing scale 준수, 임의 값 금지
- [bold+precise] color: 대비가 강한 accent, primary에 집중 + 정확한 semantic 분리, 모호한 중간 톤 지양

### 구현 노트

- 기존에 같은 역할의 컴포넌트가 있으면 토큰 교체부터 시작
- variant prop으로 시각적 변형을 관리 (하드코딩 금지)
- 빈 상태(empty-state)와 에러 상태를 반드시 처리
- 좁은 UI 텍스트는 Spoqa Han Sans Neo 기준 label line-height 1.4-1.5를 참고해 뭉침을 방지

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

- [bold+precise] motion: 200-300ms, 시각적으로 확실한 전환 + 120-180ms, 군더더기 없는 전환
- [bold+precise] density: 큰 터치 영역, 핵심 요소 강조 + 엄격한 spacing scale 준수, 임의 값 금지

### 레퍼런스 근거

- **Primer**: ActionMenu is composed of ActionList and Overlay patterns used for quick actions and selections. AnchoredOverlay

### 구현 노트

- 기존에 같은 역할의 컴포넌트가 있으면 토큰 교체부터 시작
- variant prop으로 시각적 변형을 관리 (하드코딩 금지)
- Escape / backdrop click으로 닫기, 열 때 첫 focusable 요소로 이동

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

- [bold+precise] density: 큰 터치 영역, 핵심 요소 강조 + 엄격한 spacing scale 준수, 임의 값 금지
- [bold+precise] color: 대비가 강한 accent, primary에 집중 + 정확한 semantic 분리, 모호한 중간 톤 지양

### 구현 노트

- 기존에 같은 역할의 컴포넌트가 있으면 토큰 교체부터 시작
- variant prop으로 시각적 변형을 관리 (하드코딩 금지)
- 빈 상태(empty-state)와 에러 상태를 반드시 처리
- 좁은 UI 텍스트는 Spoqa Han Sans Neo 기준 label line-height 1.4-1.5를 참고해 뭉침을 방지

---

## input / date-picker

**역할**: 날짜 선택기

**탐지 출처**: calendar and dates

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

- [bold+precise] hover: 확실한 색상 변화 또는 scale 변화 + 정확한 border/outline 변화
- [bold+precise] density: 큰 터치 영역, 핵심 요소 강조 + 엄격한 spacing scale 준수, 임의 값 금지
- [bold+precise] feedback: 눈에 띄는 성공/에러 표시, 컬러 블록 활용 + 명확한 상태 구분, 진행률/결과를 수치로 표시

### 레퍼런스 근거

- **Carbon Design System**: Date picker Number input
- **Primer**: I worked in data visualization and map-making for most of my career, and solving design problems with data is my jam. To me there's something uniqu...

### 구현 노트

- 기존에 같은 역할의 컴포넌트가 있으면 토큰 교체부터 시작
- variant prop으로 시각적 변형을 관리 (하드코딩 금지)
- error 상태에서 helper text → error message로 자동 전환
- label은 항상 visible (placeholder만으로 대체 금지)

---

## data-display / calendar-grid

**역할**: 월간 캘린더 그리드

**탐지 출처**: calendar and dates

**Slot archetype**: `layout-grid`

### 구조 (Anatomy)

- grid-container

### 상태 (States)

| 상태 | 설명 |
|------|------|
| `default` | 기본 상태 |

### 토큰 바인딩

```
display: grid
gap: var(--space-24)
grid-1: 1 column <768px
grid-2: 2 columns 768-1039px
grid-3: 3 columns ≥1040px
```

### 접근성

- 장식적 컨테이너 — 시맨틱은 자식 요소에 위임

### 브랜드 적용

- [bold+precise] density: 큰 터치 영역, 핵심 요소 강조 + 엄격한 spacing scale 준수, 임의 값 금지
- [bold+precise] color: 대비가 강한 accent, primary에 집중 + 정확한 semantic 분리, 모호한 중간 톤 지양

### 구현 노트

- 기존에 같은 역할의 컴포넌트가 있으면 토큰 교체부터 시작
- variant prop으로 시각적 변형을 관리 (하드코딩 금지)
- 빈 상태(empty-state)와 에러 상태를 반드시 처리
- 좁은 UI 텍스트는 Spoqa Han Sans Neo 기준 label line-height 1.4-1.5를 참고해 뭉침을 방지

---

## input / time-picker

**역할**: 시간 선택기

**탐지 출처**: calendar and dates

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

- [bold+precise] hover: 확실한 색상 변화 또는 scale 변화 + 정확한 border/outline 변화
- [bold+precise] density: 큰 터치 영역, 핵심 요소 강조 + 엄격한 spacing scale 준수, 임의 값 금지
- [bold+precise] feedback: 눈에 띄는 성공/에러 표시, 컬러 블록 활용 + 명확한 상태 구분, 진행률/결과를 수치로 표시

### 레퍼런스 근거

- **Carbon Design System**: Number input Text input
- **Primer**: I worked in data visualization and map-making for most of my career, and solving design problems with data is my jam. To me there's something uniqu...

### 구현 노트

- 기존에 같은 역할의 컴포넌트가 있으면 토큰 교체부터 시작
- variant prop으로 시각적 변형을 관리 (하드코딩 금지)
- error 상태에서 helper text → error message로 자동 전환
- label은 항상 visible (placeholder만으로 대체 금지)

---

## input / date-range-picker

**역할**: 기간 선택기

**탐지 출처**: calendar and dates

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

- [bold+precise] hover: 확실한 색상 변화 또는 scale 변화 + 정확한 border/outline 변화
- [bold+precise] density: 큰 터치 영역, 핵심 요소 강조 + 엄격한 spacing scale 준수, 임의 값 금지
- [bold+precise] feedback: 눈에 띄는 성공/에러 표시, 컬러 블록 활용 + 명확한 상태 구분, 진행률/결과를 수치로 표시

### 레퍼런스 근거

- **Carbon Design System**: Number input Text input
- **Primer**: I worked in data visualization and map-making for most of my career, and solving design problems with data is my jam. To me there's something uniqu...

### 구현 노트

- 기존에 같은 역할의 컴포넌트가 있으면 토큰 교체부터 시작
- variant prop으로 시각적 변형을 관리 (하드코딩 금지)
- error 상태에서 helper text → error message로 자동 전환
- label은 항상 visible (placeholder만으로 대체 금지)

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

- [bold+precise] hover: 확실한 색상 변화 또는 scale 변화 + 정확한 border/outline 변화
- [bold+precise] density: 큰 터치 영역, 핵심 요소 강조 + 엄격한 spacing scale 준수, 임의 값 금지
- [bold+precise] motion: 200-300ms, 시각적으로 확실한 전환 + 120-180ms, 군더더기 없는 전환

### 레퍼런스 근거

- **Carbon Design System**: Library menu navigation There are two kinds of symbols — library symbols and document symbols. Library symbols are available in any Sketch document...
- **Primer**: Octicon nav items navigation 12 px

### 구현 노트

- 기존에 같은 역할의 컴포넌트가 있으면 토큰 교체부터 시작
- variant prop으로 시각적 변형을 관리 (하드코딩 금지)
- active 상태는 URL/라우터와 자동 동기화
- 좁은 UI 텍스트는 Spoqa Han Sans Neo 기준 label line-height 1.4-1.5를 참고해 뭉침을 방지

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

- [bold+precise] hover: 확실한 색상 변화 또는 scale 변화 + 정확한 border/outline 변화
- [bold+precise] density: 큰 터치 영역, 핵심 요소 강조 + 엄격한 spacing scale 준수, 임의 값 금지
- [bold+precise] motion: 200-300ms, 시각적으로 확실한 전환 + 120-180ms, 군더더기 없는 전환

### 레퍼런스 근거

- **Carbon Design System**: Total panel width (“sidebar nav”) + Left outside margin + Right outside margin = Total margins Artboard width - Total margins = Total width
- **Primer**: Octicon nav items navigation 12 px

### 구현 노트

- 기존에 같은 역할의 컴포넌트가 있으면 토큰 교체부터 시작
- variant prop으로 시각적 변형을 관리 (하드코딩 금지)
- active 상태는 URL/라우터와 자동 동기화
- 좁은 UI 텍스트는 Spoqa Han Sans Neo 기준 label line-height 1.4-1.5를 참고해 뭉침을 방지

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

- [bold+precise] hover: 확실한 색상 변화 또는 scale 변화 + 정확한 border/outline 변화
- [bold+precise] density: 큰 터치 영역, 핵심 요소 강조 + 엄격한 spacing scale 준수, 임의 값 금지
- [bold+precise] motion: 200-300ms, 시각적으로 확실한 전환 + 120-180ms, 군더더기 없는 전환

### 레퍼런스 근거

- **Carbon Design System**: Library menu navigation There are two kinds of symbols — library symbols and document symbols. Library symbols are available in any Sketch document...
- **Primer**: Octicon nav items navigation 12 px

### 구현 노트

- 기존에 같은 역할의 컴포넌트가 있으면 토큰 교체부터 시작
- variant prop으로 시각적 변형을 관리 (하드코딩 금지)
- active 상태는 URL/라우터와 자동 동기화
- 좁은 UI 텍스트는 Spoqa Han Sans Neo 기준 label line-height 1.4-1.5를 참고해 뭉침을 방지

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

- [bold+precise] hover: 확실한 색상 변화 또는 scale 변화 + 정확한 border/outline 변화
- [bold+precise] density: 큰 터치 영역, 핵심 요소 강조 + 엄격한 spacing scale 준수, 임의 값 금지
- [bold+precise] motion: 200-300ms, 시각적으로 확실한 전환 + 120-180ms, 군더더기 없는 전환

### 레퍼런스 근거

- **Carbon Design System**: Library menu navigation There are two kinds of symbols — library symbols and document symbols. Library symbols are available in any Sketch document...
- **Primer**: Octicon nav items navigation 12 px

### 구현 노트

- 기존에 같은 역할의 컴포넌트가 있으면 토큰 교체부터 시작
- variant prop으로 시각적 변형을 관리 (하드코딩 금지)
- active 상태는 URL/라우터와 자동 동기화
- 좁은 UI 텍스트는 Spoqa Han Sans Neo 기준 label line-height 1.4-1.5를 참고해 뭉침을 방지

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

- [bold+precise] hover: 확실한 색상 변화 또는 scale 변화 + 정확한 border/outline 변화
- [bold+precise] density: 큰 터치 영역, 핵심 요소 강조 + 엄격한 spacing scale 준수, 임의 값 금지
- [bold+precise] motion: 200-300ms, 시각적으로 확실한 전환 + 120-180ms, 군더더기 없는 전환

### 레퍼런스 근거

- **Carbon Design System**: Library menu navigation There are two kinds of symbols — library symbols and document symbols. Library symbols are available in any Sketch document...
- **Primer**: Octicon nav items navigation 12 px

### 구현 노트

- 기존에 같은 역할의 컴포넌트가 있으면 토큰 교체부터 시작
- variant prop으로 시각적 변형을 관리 (하드코딩 금지)
- active 상태는 URL/라우터와 자동 동기화
- 좁은 UI 텍스트는 Spoqa Han Sans Neo 기준 label line-height 1.4-1.5를 참고해 뭉침을 방지

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

- [bold+precise] density: 큰 터치 영역, 핵심 요소 강조 + 엄격한 spacing scale 준수, 임의 값 금지
- [bold+precise] color: 대비가 강한 accent, primary에 집중 + 정확한 semantic 분리, 모호한 중간 톤 지양

### 구현 노트

- 기존에 같은 역할의 컴포넌트가 있으면 토큰 교체부터 시작
- variant prop으로 시각적 변형을 관리 (하드코딩 금지)
- 빈 상태(empty-state)와 에러 상태를 반드시 처리
- 좁은 UI 텍스트는 Spoqa Han Sans Neo 기준 label line-height 1.4-1.5를 참고해 뭉침을 방지

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

- [bold+precise] density: 큰 터치 영역, 핵심 요소 강조 + 엄격한 spacing scale 준수, 임의 값 금지
- [bold+precise] color: 대비가 강한 accent, primary에 집중 + 정확한 semantic 분리, 모호한 중간 톤 지양

### 구현 노트

- 기존에 같은 역할의 컴포넌트가 있으면 토큰 교체부터 시작
- variant prop으로 시각적 변형을 관리 (하드코딩 금지)
- 빈 상태(empty-state)와 에러 상태를 반드시 처리
- 좁은 UI 텍스트는 Spoqa Han Sans Neo 기준 label line-height 1.4-1.5를 참고해 뭉침을 방지

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

- [bold+precise] density: 큰 터치 영역, 핵심 요소 강조 + 엄격한 spacing scale 준수, 임의 값 금지
- [bold+precise] color: 대비가 강한 accent, primary에 집중 + 정확한 semantic 분리, 모호한 중간 톤 지양

### 구현 노트

- 기존에 같은 역할의 컴포넌트가 있으면 토큰 교체부터 시작
- variant prop으로 시각적 변형을 관리 (하드코딩 금지)
- 빈 상태(empty-state)와 에러 상태를 반드시 처리
- 좁은 UI 텍스트는 Spoqa Han Sans Neo 기준 label line-height 1.4-1.5를 참고해 뭉침을 방지

---

## overlay / command-palette

**역할**: 글로벌 커맨드 팔레트 오버레이

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

- [bold+precise] motion: 200-300ms, 시각적으로 확실한 전환 + 120-180ms, 군더더기 없는 전환
- [bold+precise] density: 큰 터치 영역, 핵심 요소 강조 + 엄격한 spacing scale 준수, 임의 값 금지

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

- [bold+precise] motion: 200-300ms, 시각적으로 확실한 전환 + 120-180ms, 군더더기 없는 전환
- [bold+precise] density: 큰 터치 영역, 핵심 요소 강조 + 엄격한 spacing scale 준수, 임의 값 금지

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

- [bold+precise] feedback: 눈에 띄는 성공/에러 표시, 컬러 블록 활용 + 명확한 상태 구분, 진행률/결과를 수치로 표시
- [bold+precise] motion: 200-300ms, 시각적으로 확실한 전환 + 120-180ms, 군더더기 없는 전환
- [bold+precise] color: 대비가 강한 accent, primary에 집중 + 정확한 semantic 분리, 모호한 중간 톤 지양

### 레퍼런스 근거

- **Carbon Design System**: We welcome all feedback, designs, or ideas in order to produce the best possible experience for our users. If you're interested in contributing, ch...
- **Primer**: Messaging components are used to provide important and relevant information to the user, including feedback, contextual information, product update...

### 구현 노트

- 기존에 같은 역할의 컴포넌트가 있으면 토큰 교체부터 시작
- variant prop으로 시각적 변형을 관리 (하드코딩 금지)
- auto-dismiss 시간은 내용 길이에 비례 (기본 5초)

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

- [bold+precise] density: 큰 터치 영역, 핵심 요소 강조 + 엄격한 spacing scale 준수, 임의 값 금지
- [bold+precise] color: 대비가 강한 accent, primary에 집중 + 정확한 semantic 분리, 모호한 중간 톤 지양

### 레퍼런스 근거

- **Primer**: Avatar Avatar is an image that represents a user or organization.

### 구현 노트

- 기존에 같은 역할의 컴포넌트가 있으면 토큰 교체부터 시작
- variant prop으로 시각적 변형을 관리 (하드코딩 금지)
- 빈 상태(empty-state)와 에러 상태를 반드시 처리
- 좁은 UI 텍스트는 Spoqa Han Sans Neo 기준 label line-height 1.4-1.5를 참고해 뭉침을 방지

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

- [bold+precise] motion: 200-300ms, 시각적으로 확실한 전환 + 120-180ms, 군더더기 없는 전환
- [bold+precise] density: 큰 터치 영역, 핵심 요소 강조 + 엄격한 spacing scale 준수, 임의 값 금지

### 레퍼런스 근거

- **Primer**: ActionMenu is composed of ActionList and Overlay patterns used for quick actions and selections. AnchoredOverlay

### 구현 노트

- 기존에 같은 역할의 컴포넌트가 있으면 토큰 교체부터 시작
- variant prop으로 시각적 변형을 관리 (하드코딩 금지)
- Escape / backdrop click으로 닫기, 열 때 첫 focusable 요소로 이동

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

- [bold+precise] density: 큰 터치 영역, 핵심 요소 강조 + 엄격한 spacing scale 준수, 임의 값 금지
- [bold+precise] color: 대비가 강한 accent, primary에 집중 + 정확한 semantic 분리, 모호한 중간 톤 지양

### 구현 노트

- 기존에 같은 역할의 컴포넌트가 있으면 토큰 교체부터 시작
- variant prop으로 시각적 변형을 관리 (하드코딩 금지)
- 빈 상태(empty-state)와 에러 상태를 반드시 처리
- 좁은 UI 텍스트는 Spoqa Han Sans Neo 기준 label line-height 1.4-1.5를 참고해 뭉침을 방지

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

- [bold+precise] color: 대비가 강한 accent, primary에 집중 + 정확한 semantic 분리, 모호한 중간 톤 지양
- [bold+precise] motion: 200-300ms, 시각적으로 확실한 전환 + 120-180ms, 군더더기 없는 전환
- [bold+precise] density: 큰 터치 영역, 핵심 요소 강조 + 엄격한 spacing scale 준수, 임의 값 금지

### 레퍼런스 근거

- **Primer**: Design digital marketing experiences with Primer Brand UI Shared Foundations

### 구현 노트

- 기존에 같은 역할의 컴포넌트가 있으면 토큰 교체부터 시작
- variant prop으로 시각적 변형을 관리 (하드코딩 금지)
- 섹션에 <h2 id="...">과 aria-labelledby 필수
- CSS 변수(var(--color-*))를 그대로 쓰고 hex 하드코딩 금지
- 다크 모드는 globals.css의 prefers-color-scheme 블록에 위임
- 한글 헤딩은 `word-break: keep-all` / `overflow-wrap: normal`을 기본값으로 두고, 강제 `<br />`는 breakpoint 검증 전 넣지 않음
- 한글 hero/section heading은 영문 시안보다 한 단계 작은 스케일에서 시작해 wrap을 확인한 뒤 확장한다.
- 좁은 UI 텍스트는 Spoqa Han Sans Neo 기준 label line-height 1.4-1.5를 참고해 뭉침을 방지

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

- [bold+precise] color: 대비가 강한 accent, primary에 집중 + 정확한 semantic 분리, 모호한 중간 톤 지양
- [bold+precise] motion: 200-300ms, 시각적으로 확실한 전환 + 120-180ms, 군더더기 없는 전환
- [bold+precise] density: 큰 터치 영역, 핵심 요소 강조 + 엄격한 spacing scale 준수, 임의 값 금지

### 레퍼런스 근거

- **Primer**: Design digital marketing experiences with Primer Brand UI Shared Foundations

### 구현 노트

- 기존에 같은 역할의 컴포넌트가 있으면 토큰 교체부터 시작
- variant prop으로 시각적 변형을 관리 (하드코딩 금지)
- 섹션에 <h2 id="...">과 aria-labelledby 필수
- CSS 변수(var(--color-*))를 그대로 쓰고 hex 하드코딩 금지
- 다크 모드는 globals.css의 prefers-color-scheme 블록에 위임
- 한글 헤딩은 `word-break: keep-all` / `overflow-wrap: normal`을 기본값으로 두고, 강제 `<br />`는 breakpoint 검증 전 넣지 않음
- 한글 hero/section heading은 영문 시안보다 한 단계 작은 스케일에서 시작해 wrap을 확인한 뒤 확장한다.
- 좁은 UI 텍스트는 Spoqa Han Sans Neo 기준 label line-height 1.4-1.5를 참고해 뭉침을 방지

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

- [bold+precise] color: 대비가 강한 accent, primary에 집중 + 정확한 semantic 분리, 모호한 중간 톤 지양
- [bold+precise] motion: 200-300ms, 시각적으로 확실한 전환 + 120-180ms, 군더더기 없는 전환
- [bold+precise] density: 큰 터치 영역, 핵심 요소 강조 + 엄격한 spacing scale 준수, 임의 값 금지

### 레퍼런스 근거

- **Primer**: Design digital marketing experiences with Primer Brand UI Shared Foundations

### 구현 노트

- 기존에 같은 역할의 컴포넌트가 있으면 토큰 교체부터 시작
- variant prop으로 시각적 변형을 관리 (하드코딩 금지)
- 섹션에 <h2 id="...">과 aria-labelledby 필수
- CSS 변수(var(--color-*))를 그대로 쓰고 hex 하드코딩 금지
- 다크 모드는 globals.css의 prefers-color-scheme 블록에 위임
- 한글 헤딩은 `word-break: keep-all` / `overflow-wrap: normal`을 기본값으로 두고, 강제 `<br />`는 breakpoint 검증 전 넣지 않음
- 한글 hero/section heading은 영문 시안보다 한 단계 작은 스케일에서 시작해 wrap을 확인한 뒤 확장한다.
- 좁은 UI 텍스트는 Spoqa Han Sans Neo 기준 label line-height 1.4-1.5를 참고해 뭉침을 방지

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

- [bold+precise] color: 대비가 강한 accent, primary에 집중 + 정확한 semantic 분리, 모호한 중간 톤 지양
- [bold+precise] motion: 200-300ms, 시각적으로 확실한 전환 + 120-180ms, 군더더기 없는 전환
- [bold+precise] density: 큰 터치 영역, 핵심 요소 강조 + 엄격한 spacing scale 준수, 임의 값 금지

### 레퍼런스 근거

- **Primer**: Design digital marketing experiences with Primer Brand UI Shared Foundations

### 구현 노트

- 기존에 같은 역할의 컴포넌트가 있으면 토큰 교체부터 시작
- variant prop으로 시각적 변형을 관리 (하드코딩 금지)
- 섹션에 <h2 id="...">과 aria-labelledby 필수
- CSS 변수(var(--color-*))를 그대로 쓰고 hex 하드코딩 금지
- 다크 모드는 globals.css의 prefers-color-scheme 블록에 위임
- 한글 헤딩은 `word-break: keep-all` / `overflow-wrap: normal`을 기본값으로 두고, 강제 `<br />`는 breakpoint 검증 전 넣지 않음
- 한글 hero/section heading은 영문 시안보다 한 단계 작은 스케일에서 시작해 wrap을 확인한 뒤 확장한다.
- 좁은 UI 텍스트는 Spoqa Han Sans Neo 기준 label line-height 1.4-1.5를 참고해 뭉침을 방지

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

### 브랜드 적용

- [bold+precise] hover: 확실한 색상 변화 또는 scale 변화 + 정확한 border/outline 변화
- [bold+precise] motion: 200-300ms, 시각적으로 확실한 전환 + 120-180ms, 군더더기 없는 전환
- [bold+precise] color: 대비가 강한 accent, primary에 집중 + 정확한 semantic 분리, 모호한 중간 톤 지양

### 레퍼런스 근거

- **Carbon Design System**: These components can toggle between the AI variant and the default variant depending on the user’s interaction. If the user manually overrides the ...
- **Primer**: I get so much joy from writing HTML and CSS, and design systems are one level up - systematically making UIs accessible and consistent. I love conc...

### 구현 노트

- 기존에 같은 역할의 컴포넌트가 있으면 토큰 교체부터 시작
- variant prop으로 시각적 변형을 관리 (하드코딩 금지)
- size prop: sm / md / lg (터치 영역은 항상 최소 44px 보장)

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

- [bold+precise] color: 대비가 강한 accent, primary에 집중 + 정확한 semantic 분리, 모호한 중간 톤 지양
- [bold+precise] motion: 200-300ms, 시각적으로 확실한 전환 + 120-180ms, 군더더기 없는 전환
- [bold+precise] density: 큰 터치 영역, 핵심 요소 강조 + 엄격한 spacing scale 준수, 임의 값 금지

### 레퍼런스 근거

- **Primer**: Design digital marketing experiences with Primer Brand UI Shared Foundations

### 구현 노트

- 기존에 같은 역할의 컴포넌트가 있으면 토큰 교체부터 시작
- variant prop으로 시각적 변형을 관리 (하드코딩 금지)
- 섹션에 <h2 id="...">과 aria-labelledby 필수
- CSS 변수(var(--color-*))를 그대로 쓰고 hex 하드코딩 금지
- 다크 모드는 globals.css의 prefers-color-scheme 블록에 위임
- 한글 헤딩은 `word-break: keep-all` / `overflow-wrap: normal`을 기본값으로 두고, 강제 `<br />`는 breakpoint 검증 전 넣지 않음
- 한글 hero/section heading은 영문 시안보다 한 단계 작은 스케일에서 시작해 wrap을 확인한 뒤 확장한다.
- 좁은 UI 텍스트는 Spoqa Han Sans Neo 기준 label line-height 1.4-1.5를 참고해 뭉침을 방지

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

- [bold+precise] color: 대비가 강한 accent, primary에 집중 + 정확한 semantic 분리, 모호한 중간 톤 지양
- [bold+precise] motion: 200-300ms, 시각적으로 확실한 전환 + 120-180ms, 군더더기 없는 전환
- [bold+precise] density: 큰 터치 영역, 핵심 요소 강조 + 엄격한 spacing scale 준수, 임의 값 금지

### 레퍼런스 근거

- **Primer**: Design digital marketing experiences with Primer Brand UI Shared Foundations

### 구현 노트

- 기존에 같은 역할의 컴포넌트가 있으면 토큰 교체부터 시작
- variant prop으로 시각적 변형을 관리 (하드코딩 금지)
- 섹션에 <h2 id="...">과 aria-labelledby 필수
- CSS 변수(var(--color-*))를 그대로 쓰고 hex 하드코딩 금지
- 다크 모드는 globals.css의 prefers-color-scheme 블록에 위임
- 한글 헤딩은 `word-break: keep-all` / `overflow-wrap: normal`을 기본값으로 두고, 강제 `<br />`는 breakpoint 검증 전 넣지 않음
- 한글 hero/section heading은 영문 시안보다 한 단계 작은 스케일에서 시작해 wrap을 확인한 뒤 확장한다.
- 좁은 UI 텍스트는 Spoqa Han Sans Neo 기준 label line-height 1.4-1.5를 참고해 뭉침을 방지
