# Signal Desk Component Specs

총 106개 컴포넌트 | 패밀리: button, data-display, editorial, feedback, input, marketing, navigation, overlay

## 구현 원칙 (Non-negotiable)

이 스펙의 모든 컴포넌트를 구현할 때 반드시 지킨다:

1. **이모지를 UI로 쓰지 않는다** — 🎨 ✅ 🔥 ⚡ 🚀 ❌ ⭐ 📊 등 이모지를 아이콘, 상태 표시, 버튼 장식, 네비게이션 지표 자리에 절대 넣지 않는다. 아이콘 자리에는 SVG 컴포넌트 또는 Lucide/Heroicons/Phosphor/Tabler 라이브러리를 사용한다.
2. **컴포넌트를 직접 구현한다** — 아래 각 컴포넌트의 anatomy(구조), states(상태), 토큰 바인딩, 접근성 규칙을 그대로 따라 완전하게 구현한다. '임시', 'TODO', '플레이스홀더' 같은 반쪽 구현을 남기지 않는다.
3. **라이브러리 기본 스타일 금지** — 라이브러리 컴포넌트를 그대로 import해서 쓰지 않는다. 반드시 디자인 토큰(--color-*, --space-*, --radius-*, --font-*)으로 스타일을 명시적으로 바인딩한다.
4. **접근성은 옵션이 아니다** — 각 컴포넌트의 '접근성' 섹션에 정의된 role, aria-*, label, focus 관리 규칙을 전부 적용한다.
5. **hex 값 하드코딩 금지** — 색상은 반드시 semantic token을 경유한다 (예: `color: var(--color-ink)` not `color: #2C2C2C`).

## 브랜드 적용 규칙

- **hover**: opacity 변화 (0.08-0.12), elevation 변화 없음 + 정확한 border/outline 변화 + 텍스트 underline 또는 color shift, 장식적 효과 없음 + 예측 가능하고 일관된 hover 패턴
- **motion**: 150-200ms ease-out, bounce/spring 없음 + 120-180ms, 군더더기 없는 전환 + 콘텐츠 전환 위주, UI chrome 모션 최소화 + 모든 전환에 동일한 easing/duration
- **color**: 중성 톤 위주, accent는 최소한으로 + 정확한 semantic 분리, 모호한 중간 톤 지양 + 타이포그래피로 위계 형성, 컬러보다 weight/size 활용 + 안정적인 neutral 기반, 과한 accent 변화 없음
- **density**: comfortable 모드 기본, 여유로운 padding + 엄격한 spacing scale 준수, 임의 값 금지 + 넉넉한 line-height와 margin, 읽기 편한 간격 + 기존 레이아웃 유지, 갑작스런 위치 변경 없음
- **feedback**: subtle inline alert 선호, 과한 컬러 블록 지양 + 명확한 상태 구분, 진행률/결과를 수치로 표시 + 콘텐츠 맥락 안에서 인라인 표시, 토스트보다 인라인 선호 + 결과를 반드시 확인, 실패 시 복구 방법 안내

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

- [calm+precise+editorial+trustworthy] hover: opacity 변화 (0.08-0.12), elevation 변화 없음 + 정확한 border/outline 변화 + 텍스트 underline 또는 color shift, 장식적 효과 없음 + 예측 가능하고 일관된 hover 패턴
- [calm+precise+editorial+trustworthy] motion: 150-200ms ease-out, bounce/spring 없음 + 120-180ms, 군더더기 없는 전환 + 콘텐츠 전환 위주, UI chrome 모션 최소화 + 모든 전환에 동일한 easing/duration
- [calm+precise+editorial+trustworthy] color: 중성 톤 위주, accent는 최소한으로 + 정확한 semantic 분리, 모호한 중간 톤 지양 + 타이포그래피로 위계 형성, 컬러보다 weight/size 활용 + 안정적인 neutral 기반, 과한 accent 변화 없음

### 레퍼런스 근거

- **Carbon Design System**: These components can toggle between the AI variant and the default variant depending on the user’s interaction. If the user manually overrides the ...
- **Elastic UI Framework | Elastic UI Framework**: Button Variety of buttons and button groups with different styles and colours Button
- **Workday Canvas Design System**: New AI Ingress Button in Labs AI Ingress Button with open and close CTA will be available in Labs.

### 구현 노트

- 기존에 같은 역할의 컴포넌트가 있으면 토큰 교체부터 시작
- variant prop으로 시각적 변형을 관리 (하드코딩 금지)
- size prop: sm / md / lg (터치 영역은 항상 최소 44px 보장)
- 애니메이션은 상태 설명용으로만 사용, 장식 효과 금지
- 텍스트 위계가 핵심 — 컬러보다 weight/size로 구분

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

- [calm+precise+editorial+trustworthy] hover: opacity 변화 (0.08-0.12), elevation 변화 없음 + 정확한 border/outline 변화 + 텍스트 underline 또는 color shift, 장식적 효과 없음 + 예측 가능하고 일관된 hover 패턴
- [calm+precise+editorial+trustworthy] motion: 150-200ms ease-out, bounce/spring 없음 + 120-180ms, 군더더기 없는 전환 + 콘텐츠 전환 위주, UI chrome 모션 최소화 + 모든 전환에 동일한 easing/duration
- [calm+precise+editorial+trustworthy] color: 중성 톤 위주, accent는 최소한으로 + 정확한 semantic 분리, 모호한 중간 톤 지양 + 타이포그래피로 위계 형성, 컬러보다 weight/size 활용 + 안정적인 neutral 기반, 과한 accent 변화 없음

### 레퍼런스 근거

- **Carbon Design System**: These components can toggle between the AI variant and the default variant depending on the user’s interaction. If the user manually overrides the ...
- **Elastic UI Framework | Elastic UI Framework**: Button Variety of buttons and button groups with different styles and colours Button
- **Workday Canvas Design System**: New AI Ingress Button in Labs AI Ingress Button with open and close CTA will be available in Labs.

### 구현 노트

- 기존에 같은 역할의 컴포넌트가 있으면 토큰 교체부터 시작
- variant prop으로 시각적 변형을 관리 (하드코딩 금지)
- size prop: sm / md / lg (터치 영역은 항상 최소 44px 보장)
- 애니메이션은 상태 설명용으로만 사용, 장식 효과 금지
- 텍스트 위계가 핵심 — 컬러보다 weight/size로 구분

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

- [calm+precise+editorial+trustworthy] hover: opacity 변화 (0.08-0.12), elevation 변화 없음 + 정확한 border/outline 변화 + 텍스트 underline 또는 color shift, 장식적 효과 없음 + 예측 가능하고 일관된 hover 패턴
- [calm+precise+editorial+trustworthy] motion: 150-200ms ease-out, bounce/spring 없음 + 120-180ms, 군더더기 없는 전환 + 콘텐츠 전환 위주, UI chrome 모션 최소화 + 모든 전환에 동일한 easing/duration
- [calm+precise+editorial+trustworthy] color: 중성 톤 위주, accent는 최소한으로 + 정확한 semantic 분리, 모호한 중간 톤 지양 + 타이포그래피로 위계 형성, 컬러보다 weight/size 활용 + 안정적인 neutral 기반, 과한 accent 변화 없음

### 레퍼런스 근거

- **Carbon Design System**: These components can toggle between the AI variant and the default variant depending on the user’s interaction. If the user manually overrides the ...
- **Elastic UI Framework | Elastic UI Framework**: Button Variety of buttons and button groups with different styles and colours Button
- **Workday Canvas Design System**: New AI Ingress Button in Labs AI Ingress Button with open and close CTA will be available in Labs.

### 구현 노트

- 기존에 같은 역할의 컴포넌트가 있으면 토큰 교체부터 시작
- variant prop으로 시각적 변형을 관리 (하드코딩 금지)
- size prop: sm / md / lg (터치 영역은 항상 최소 44px 보장)
- 애니메이션은 상태 설명용으로만 사용, 장식 효과 금지
- 텍스트 위계가 핵심 — 컬러보다 weight/size로 구분

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

- [calm+precise+editorial+trustworthy] hover: opacity 변화 (0.08-0.12), elevation 변화 없음 + 정확한 border/outline 변화 + 텍스트 underline 또는 color shift, 장식적 효과 없음 + 예측 가능하고 일관된 hover 패턴
- [calm+precise+editorial+trustworthy] motion: 150-200ms ease-out, bounce/spring 없음 + 120-180ms, 군더더기 없는 전환 + 콘텐츠 전환 위주, UI chrome 모션 최소화 + 모든 전환에 동일한 easing/duration
- [calm+precise+editorial+trustworthy] color: 중성 톤 위주, accent는 최소한으로 + 정확한 semantic 분리, 모호한 중간 톤 지양 + 타이포그래피로 위계 형성, 컬러보다 weight/size 활용 + 안정적인 neutral 기반, 과한 accent 변화 없음

### 레퍼런스 근거

- **Carbon Design System**: These components can toggle between the AI variant and the default variant depending on the user’s interaction. If the user manually overrides the ...
- **Elastic UI Framework | Elastic UI Framework**: Button Variety of buttons and button groups with different styles and colours Button
- **Workday Canvas Design System**: The following Canvas components will be updated to reflect the new brand: Breadcrumbs, Buttons, Card, ColorPicker, Loading Dots, SearchForm, Segmen...

### 구현 노트

- 기존에 같은 역할의 컴포넌트가 있으면 토큰 교체부터 시작
- variant prop으로 시각적 변형을 관리 (하드코딩 금지)
- size prop: sm / md / lg (터치 영역은 항상 최소 44px 보장)
- 애니메이션은 상태 설명용으로만 사용, 장식 효과 금지
- 텍스트 위계가 핵심 — 컬러보다 weight/size로 구분

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

- [calm+precise+editorial+trustworthy] hover: opacity 변화 (0.08-0.12), elevation 변화 없음 + 정확한 border/outline 변화 + 텍스트 underline 또는 color shift, 장식적 효과 없음 + 예측 가능하고 일관된 hover 패턴
- [calm+precise+editorial+trustworthy] motion: 150-200ms ease-out, bounce/spring 없음 + 120-180ms, 군더더기 없는 전환 + 콘텐츠 전환 위주, UI chrome 모션 최소화 + 모든 전환에 동일한 easing/duration
- [calm+precise+editorial+trustworthy] color: 중성 톤 위주, accent는 최소한으로 + 정확한 semantic 분리, 모호한 중간 톤 지양 + 타이포그래피로 위계 형성, 컬러보다 weight/size 활용 + 안정적인 neutral 기반, 과한 accent 변화 없음

### 레퍼런스 근거

- **Carbon Design System**: These components can toggle between the AI variant and the default variant depending on the user’s interaction. If the user manually overrides the ...
- **Elastic UI Framework | Elastic UI Framework**: Button Variety of buttons and button groups with different styles and colours Button
- **Workday Canvas Design System**: New AI Ingress Button in Labs AI Ingress Button with open and close CTA will be available in Labs.

### 구현 노트

- 기존에 같은 역할의 컴포넌트가 있으면 토큰 교체부터 시작
- variant prop으로 시각적 변형을 관리 (하드코딩 금지)
- size prop: sm / md / lg (터치 영역은 항상 최소 44px 보장)
- 애니메이션은 상태 설명용으로만 사용, 장식 효과 금지
- 텍스트 위계가 핵심 — 컬러보다 weight/size로 구분

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

- [calm+precise+editorial+trustworthy] density: comfortable 모드 기본, 여유로운 padding + 엄격한 spacing scale 준수, 임의 값 금지 + 넉넉한 line-height와 margin, 읽기 편한 간격 + 기존 레이아웃 유지, 갑작스런 위치 변경 없음
- [calm+precise+editorial+trustworthy] color: 중성 톤 위주, accent는 최소한으로 + 정확한 semantic 분리, 모호한 중간 톤 지양 + 타이포그래피로 위계 형성, 컬러보다 weight/size 활용 + 안정적인 neutral 기반, 과한 accent 변화 없음
- [calm+precise+editorial+trustworthy] motion: 150-200ms ease-out, bounce/spring 없음 + 120-180ms, 군더더기 없는 전환 + 콘텐츠 전환 위주, UI chrome 모션 최소화 + 모든 전환에 동일한 easing/duration

### 구현 노트

- 기존에 같은 역할의 컴포넌트가 있으면 토큰 교체부터 시작
- variant prop으로 시각적 변형을 관리 (하드코딩 금지)
- 블록 단위 데이터 모델, JSON 직렬화 가능한 구조
- 애니메이션은 상태 설명용으로만 사용, 장식 효과 금지
- 텍스트 위계가 핵심 — 컬러보다 weight/size로 구분

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

- [calm+precise+editorial+trustworthy] density: comfortable 모드 기본, 여유로운 padding + 엄격한 spacing scale 준수, 임의 값 금지 + 넉넉한 line-height와 margin, 읽기 편한 간격 + 기존 레이아웃 유지, 갑작스런 위치 변경 없음
- [calm+precise+editorial+trustworthy] color: 중성 톤 위주, accent는 최소한으로 + 정확한 semantic 분리, 모호한 중간 톤 지양 + 타이포그래피로 위계 형성, 컬러보다 weight/size 활용 + 안정적인 neutral 기반, 과한 accent 변화 없음
- [calm+precise+editorial+trustworthy] motion: 150-200ms ease-out, bounce/spring 없음 + 120-180ms, 군더더기 없는 전환 + 콘텐츠 전환 위주, UI chrome 모션 최소화 + 모든 전환에 동일한 easing/duration

### 구현 노트

- 기존에 같은 역할의 컴포넌트가 있으면 토큰 교체부터 시작
- variant prop으로 시각적 변형을 관리 (하드코딩 금지)
- 블록 단위 데이터 모델, JSON 직렬화 가능한 구조
- 애니메이션은 상태 설명용으로만 사용, 장식 효과 금지
- 텍스트 위계가 핵심 — 컬러보다 weight/size로 구분

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

- [calm+precise+editorial+trustworthy] density: comfortable 모드 기본, 여유로운 padding + 엄격한 spacing scale 준수, 임의 값 금지 + 넉넉한 line-height와 margin, 읽기 편한 간격 + 기존 레이아웃 유지, 갑작스런 위치 변경 없음
- [calm+precise+editorial+trustworthy] color: 중성 톤 위주, accent는 최소한으로 + 정확한 semantic 분리, 모호한 중간 톤 지양 + 타이포그래피로 위계 형성, 컬러보다 weight/size 활용 + 안정적인 neutral 기반, 과한 accent 변화 없음
- [calm+precise+editorial+trustworthy] motion: 150-200ms ease-out, bounce/spring 없음 + 120-180ms, 군더더기 없는 전환 + 콘텐츠 전환 위주, UI chrome 모션 최소화 + 모든 전환에 동일한 easing/duration

### 구현 노트

- 기존에 같은 역할의 컴포넌트가 있으면 토큰 교체부터 시작
- variant prop으로 시각적 변형을 관리 (하드코딩 금지)
- 블록 단위 데이터 모델, JSON 직렬화 가능한 구조
- 애니메이션은 상태 설명용으로만 사용, 장식 효과 금지
- 텍스트 위계가 핵심 — 컬러보다 weight/size로 구분

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

- [calm+precise+editorial+trustworthy] density: comfortable 모드 기본, 여유로운 padding + 엄격한 spacing scale 준수, 임의 값 금지 + 넉넉한 line-height와 margin, 읽기 편한 간격 + 기존 레이아웃 유지, 갑작스런 위치 변경 없음
- [calm+precise+editorial+trustworthy] color: 중성 톤 위주, accent는 최소한으로 + 정확한 semantic 분리, 모호한 중간 톤 지양 + 타이포그래피로 위계 형성, 컬러보다 weight/size 활용 + 안정적인 neutral 기반, 과한 accent 변화 없음
- [calm+precise+editorial+trustworthy] motion: 150-200ms ease-out, bounce/spring 없음 + 120-180ms, 군더더기 없는 전환 + 콘텐츠 전환 위주, UI chrome 모션 최소화 + 모든 전환에 동일한 easing/duration

### 구현 노트

- 기존에 같은 역할의 컴포넌트가 있으면 토큰 교체부터 시작
- variant prop으로 시각적 변형을 관리 (하드코딩 금지)
- 블록 단위 데이터 모델, JSON 직렬화 가능한 구조
- 애니메이션은 상태 설명용으로만 사용, 장식 효과 금지
- 텍스트 위계가 핵심 — 컬러보다 weight/size로 구분

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

- [calm+precise+editorial+trustworthy] density: comfortable 모드 기본, 여유로운 padding + 엄격한 spacing scale 준수, 임의 값 금지 + 넉넉한 line-height와 margin, 읽기 편한 간격 + 기존 레이아웃 유지, 갑작스런 위치 변경 없음
- [calm+precise+editorial+trustworthy] color: 중성 톤 위주, accent는 최소한으로 + 정확한 semantic 분리, 모호한 중간 톤 지양 + 타이포그래피로 위계 형성, 컬러보다 weight/size 활용 + 안정적인 neutral 기반, 과한 accent 변화 없음
- [calm+precise+editorial+trustworthy] motion: 150-200ms ease-out, bounce/spring 없음 + 120-180ms, 군더더기 없는 전환 + 콘텐츠 전환 위주, UI chrome 모션 최소화 + 모든 전환에 동일한 easing/duration

### 구현 노트

- 기존에 같은 역할의 컴포넌트가 있으면 토큰 교체부터 시작
- variant prop으로 시각적 변형을 관리 (하드코딩 금지)
- 블록 단위 데이터 모델, JSON 직렬화 가능한 구조
- 애니메이션은 상태 설명용으로만 사용, 장식 효과 금지
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

- [calm+precise+editorial+trustworthy] hover: opacity 변화 (0.08-0.12), elevation 변화 없음 + 정확한 border/outline 변화 + 텍스트 underline 또는 color shift, 장식적 효과 없음 + 예측 가능하고 일관된 hover 패턴
- [calm+precise+editorial+trustworthy] density: comfortable 모드 기본, 여유로운 padding + 엄격한 spacing scale 준수, 임의 값 금지 + 넉넉한 line-height와 margin, 읽기 편한 간격 + 기존 레이아웃 유지, 갑작스런 위치 변경 없음
- [calm+precise+editorial+trustworthy] feedback: subtle inline alert 선호, 과한 컬러 블록 지양 + 명확한 상태 구분, 진행률/결과를 수치로 표시 + 콘텐츠 맥락 안에서 인라인 표시, 토스트보다 인라인 선호 + 결과를 반드시 확인, 실패 시 복구 방법 안내

### 레퍼런스 근거

- **Carbon Design System**: Number input Text input
- **Elastic UI Framework | Elastic UI Framework**: Forms Inputs with validation, grouped into a flexible form layout Forms
- **Thumbprint**: A design system only works when there’s input from a wider team. We encourage contributions both big and small from designers and developers. We’re...

### 구현 노트

- 기존에 같은 역할의 컴포넌트가 있으면 토큰 교체부터 시작
- variant prop으로 시각적 변형을 관리 (하드코딩 금지)
- error 상태에서 helper text → error message로 자동 전환
- label은 항상 visible (placeholder만으로 대체 금지)
- 애니메이션은 상태 설명용으로만 사용, 장식 효과 금지
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

- [calm+precise+editorial+trustworthy] hover: opacity 변화 (0.08-0.12), elevation 변화 없음 + 정확한 border/outline 변화 + 텍스트 underline 또는 color shift, 장식적 효과 없음 + 예측 가능하고 일관된 hover 패턴
- [calm+precise+editorial+trustworthy] density: comfortable 모드 기본, 여유로운 padding + 엄격한 spacing scale 준수, 임의 값 금지 + 넉넉한 line-height와 margin, 읽기 편한 간격 + 기존 레이아웃 유지, 갑작스런 위치 변경 없음
- [calm+precise+editorial+trustworthy] feedback: subtle inline alert 선호, 과한 컬러 블록 지양 + 명확한 상태 구분, 진행률/결과를 수치로 표시 + 콘텐츠 맥락 안에서 인라인 표시, 토스트보다 인라인 선호 + 결과를 반드시 확인, 실패 시 복구 방법 안내

### 레퍼런스 근거

- **Carbon Design System**: Number input Text input
- **Elastic UI Framework | Elastic UI Framework**: Forms Inputs with validation, grouped into a flexible form layout Forms
- **Thumbprint**: A design system only works when there’s input from a wider team. We encourage contributions both big and small from designers and developers. We’re...

### 구현 노트

- 기존에 같은 역할의 컴포넌트가 있으면 토큰 교체부터 시작
- variant prop으로 시각적 변형을 관리 (하드코딩 금지)
- error 상태에서 helper text → error message로 자동 전환
- label은 항상 visible (placeholder만으로 대체 금지)
- 애니메이션은 상태 설명용으로만 사용, 장식 효과 금지
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

- [calm+precise+editorial+trustworthy] hover: opacity 변화 (0.08-0.12), elevation 변화 없음 + 정확한 border/outline 변화 + 텍스트 underline 또는 color shift, 장식적 효과 없음 + 예측 가능하고 일관된 hover 패턴
- [calm+precise+editorial+trustworthy] density: comfortable 모드 기본, 여유로운 padding + 엄격한 spacing scale 준수, 임의 값 금지 + 넉넉한 line-height와 margin, 읽기 편한 간격 + 기존 레이아웃 유지, 갑작스런 위치 변경 없음
- [calm+precise+editorial+trustworthy] feedback: subtle inline alert 선호, 과한 컬러 블록 지양 + 명확한 상태 구분, 진행률/결과를 수치로 표시 + 콘텐츠 맥락 안에서 인라인 표시, 토스트보다 인라인 선호 + 결과를 반드시 확인, 실패 시 복구 방법 안내

### 레퍼런스 근거

- **Carbon Design System**: Select Data table
- **Elastic UI Framework | Elastic UI Framework**: Table Flexible tables with sorting, pagination, selection and actions Table
- **Thumbprint**: A design system only works when there’s input from a wider team. We encourage contributions both big and small from designers and developers. We’re...

### 구현 노트

- 기존에 같은 역할의 컴포넌트가 있으면 토큰 교체부터 시작
- variant prop으로 시각적 변형을 관리 (하드코딩 금지)
- error 상태에서 helper text → error message로 자동 전환
- label은 항상 visible (placeholder만으로 대체 금지)
- 애니메이션은 상태 설명용으로만 사용, 장식 효과 금지
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

- [calm+precise+editorial+trustworthy] hover: opacity 변화 (0.08-0.12), elevation 변화 없음 + 정확한 border/outline 변화 + 텍스트 underline 또는 color shift, 장식적 효과 없음 + 예측 가능하고 일관된 hover 패턴
- [calm+precise+editorial+trustworthy] density: comfortable 모드 기본, 여유로운 padding + 엄격한 spacing scale 준수, 임의 값 금지 + 넉넉한 line-height와 margin, 읽기 편한 간격 + 기존 레이아웃 유지, 갑작스런 위치 변경 없음
- [calm+precise+editorial+trustworthy] feedback: subtle inline alert 선호, 과한 컬러 블록 지양 + 명확한 상태 구분, 진행률/결과를 수치로 표시 + 콘텐츠 맥락 안에서 인라인 표시, 토스트보다 인라인 선호 + 결과를 반드시 확인, 실패 시 복구 방법 안내

### 레퍼런스 근거

- **Carbon Design System**: Checkbox Form
- **Elastic UI Framework | Elastic UI Framework**: Forms Inputs with validation, grouped into a flexible form layout Forms
- **Thumbprint**: A design system only works when there’s input from a wider team. We encourage contributions both big and small from designers and developers. We’re...

### 구현 노트

- 기존에 같은 역할의 컴포넌트가 있으면 토큰 교체부터 시작
- variant prop으로 시각적 변형을 관리 (하드코딩 금지)
- error 상태에서 helper text → error message로 자동 전환
- label은 항상 visible (placeholder만으로 대체 금지)
- 애니메이션은 상태 설명용으로만 사용, 장식 효과 금지
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

- [calm+precise+editorial+trustworthy] hover: opacity 변화 (0.08-0.12), elevation 변화 없음 + 정확한 border/outline 변화 + 텍스트 underline 또는 color shift, 장식적 효과 없음 + 예측 가능하고 일관된 hover 패턴
- [calm+precise+editorial+trustworthy] density: comfortable 모드 기본, 여유로운 padding + 엄격한 spacing scale 준수, 임의 값 금지 + 넉넉한 line-height와 margin, 읽기 편한 간격 + 기존 레이아웃 유지, 갑작스런 위치 변경 없음
- [calm+precise+editorial+trustworthy] feedback: subtle inline alert 선호, 과한 컬러 블록 지양 + 명확한 상태 구분, 진행률/결과를 수치로 표시 + 콘텐츠 맥락 안에서 인라인 표시, 토스트보다 인라인 선호 + 결과를 반드시 확인, 실패 시 복구 방법 안내

### 레퍼런스 근거

- **Carbon Design System**: Number input Text input
- **Elastic UI Framework | Elastic UI Framework**: Forms Inputs with validation, grouped into a flexible form layout Forms
- **Thumbprint**: A design system only works when there’s input from a wider team. We encourage contributions both big and small from designers and developers. We’re...

### 구현 노트

- 기존에 같은 역할의 컴포넌트가 있으면 토큰 교체부터 시작
- variant prop으로 시각적 변형을 관리 (하드코딩 금지)
- error 상태에서 helper text → error message로 자동 전환
- label은 항상 visible (placeholder만으로 대체 금지)
- 애니메이션은 상태 설명용으로만 사용, 장식 효과 금지
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

- [calm+precise+editorial+trustworthy] hover: opacity 변화 (0.08-0.12), elevation 변화 없음 + 정확한 border/outline 변화 + 텍스트 underline 또는 color shift, 장식적 효과 없음 + 예측 가능하고 일관된 hover 패턴
- [calm+precise+editorial+trustworthy] density: comfortable 모드 기본, 여유로운 padding + 엄격한 spacing scale 준수, 임의 값 금지 + 넉넉한 line-height와 margin, 읽기 편한 간격 + 기존 레이아웃 유지, 갑작스런 위치 변경 없음
- [calm+precise+editorial+trustworthy] feedback: subtle inline alert 선호, 과한 컬러 블록 지양 + 명확한 상태 구분, 진행률/결과를 수치로 표시 + 콘텐츠 맥락 안에서 인라인 표시, 토스트보다 인라인 선호 + 결과를 반드시 확인, 실패 시 복구 방법 안내

### 레퍼런스 근거

- **Carbon Design System**: Number input Text input
- **Elastic UI Framework | Elastic UI Framework**: Forms Inputs with validation, grouped into a flexible form layout Forms
- **Thumbprint**: A design system only works when there’s input from a wider team. We encourage contributions both big and small from designers and developers. We’re...

### 구현 노트

- 기존에 같은 역할의 컴포넌트가 있으면 토큰 교체부터 시작
- variant prop으로 시각적 변형을 관리 (하드코딩 금지)
- error 상태에서 helper text → error message로 자동 전환
- label은 항상 visible (placeholder만으로 대체 금지)
- 애니메이션은 상태 설명용으로만 사용, 장식 효과 금지
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

- [calm+precise+editorial+trustworthy] hover: opacity 변화 (0.08-0.12), elevation 변화 없음 + 정확한 border/outline 변화 + 텍스트 underline 또는 color shift, 장식적 효과 없음 + 예측 가능하고 일관된 hover 패턴
- [calm+precise+editorial+trustworthy] motion: 150-200ms ease-out, bounce/spring 없음 + 120-180ms, 군더더기 없는 전환 + 콘텐츠 전환 위주, UI chrome 모션 최소화 + 모든 전환에 동일한 easing/duration
- [calm+precise+editorial+trustworthy] color: 중성 톤 위주, accent는 최소한으로 + 정확한 semantic 분리, 모호한 중간 톤 지양 + 타이포그래피로 위계 형성, 컬러보다 weight/size 활용 + 안정적인 neutral 기반, 과한 accent 변화 없음

### 레퍼런스 근거

- **Carbon Design System**: These components can toggle between the AI variant and the default variant depending on the user’s interaction. If the user manually overrides the ...
- **Elastic UI Framework | Elastic UI Framework**: Button Variety of buttons and button groups with different styles and colours Button
- **Workday Canvas Design System**: New AI Ingress Button in Labs AI Ingress Button with open and close CTA will be available in Labs.

### 구현 노트

- 기존에 같은 역할의 컴포넌트가 있으면 토큰 교체부터 시작
- variant prop으로 시각적 변형을 관리 (하드코딩 금지)
- size prop: sm / md / lg (터치 영역은 항상 최소 44px 보장)
- 애니메이션은 상태 설명용으로만 사용, 장식 효과 금지
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

- [calm+precise+editorial+trustworthy] density: comfortable 모드 기본, 여유로운 padding + 엄격한 spacing scale 준수, 임의 값 금지 + 넉넉한 line-height와 margin, 읽기 편한 간격 + 기존 레이아웃 유지, 갑작스런 위치 변경 없음
- [calm+precise+editorial+trustworthy] color: 중성 톤 위주, accent는 최소한으로 + 정확한 semantic 분리, 모호한 중간 톤 지양 + 타이포그래피로 위계 형성, 컬러보다 weight/size 활용 + 안정적인 neutral 기반, 과한 accent 변화 없음

### 레퍼런스 근거

- **Carbon Design System**: Data table Modal
- **The Foundation for your Design System - shadcn/ui**: Data Table Date Picker

### 구현 노트

- 기존에 같은 역할의 컴포넌트가 있으면 토큰 교체부터 시작
- variant prop으로 시각적 변형을 관리 (하드코딩 금지)
- 빈 상태(empty-state)와 에러 상태를 반드시 처리
- 애니메이션은 상태 설명용으로만 사용, 장식 효과 금지
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

- [calm+precise+editorial+trustworthy] density: comfortable 모드 기본, 여유로운 padding + 엄격한 spacing scale 준수, 임의 값 금지 + 넉넉한 line-height와 margin, 읽기 편한 간격 + 기존 레이아웃 유지, 갑작스런 위치 변경 없음
- [calm+precise+editorial+trustworthy] color: 중성 톤 위주, accent는 최소한으로 + 정확한 semantic 분리, 모호한 중간 톤 지양 + 타이포그래피로 위계 형성, 컬러보다 weight/size 활용 + 안정적인 neutral 기반, 과한 accent 변화 없음

### 구현 노트

- 기존에 같은 역할의 컴포넌트가 있으면 토큰 교체부터 시작
- variant prop으로 시각적 변형을 관리 (하드코딩 금지)
- 빈 상태(empty-state)와 에러 상태를 반드시 처리
- 애니메이션은 상태 설명용으로만 사용, 장식 효과 금지
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

- [calm+precise+editorial+trustworthy] density: comfortable 모드 기본, 여유로운 padding + 엄격한 spacing scale 준수, 임의 값 금지 + 넉넉한 line-height와 margin, 읽기 편한 간격 + 기존 레이아웃 유지, 갑작스런 위치 변경 없음
- [calm+precise+editorial+trustworthy] color: 중성 톤 위주, accent는 최소한으로 + 정확한 semantic 분리, 모호한 중간 톤 지양 + 타이포그래피로 위계 형성, 컬러보다 weight/size 활용 + 안정적인 neutral 기반, 과한 accent 변화 없음

### 구현 노트

- 기존에 같은 역할의 컴포넌트가 있으면 토큰 교체부터 시작
- variant prop으로 시각적 변형을 관리 (하드코딩 금지)
- 빈 상태(empty-state)와 에러 상태를 반드시 처리
- 애니메이션은 상태 설명용으로만 사용, 장식 효과 금지
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

- [calm+precise+editorial+trustworthy] hover: opacity 변화 (0.08-0.12), elevation 변화 없음 + 정확한 border/outline 변화 + 텍스트 underline 또는 color shift, 장식적 효과 없음 + 예측 가능하고 일관된 hover 패턴
- [calm+precise+editorial+trustworthy] density: comfortable 모드 기본, 여유로운 padding + 엄격한 spacing scale 준수, 임의 값 금지 + 넉넉한 line-height와 margin, 읽기 편한 간격 + 기존 레이아웃 유지, 갑작스런 위치 변경 없음
- [calm+precise+editorial+trustworthy] motion: 150-200ms ease-out, bounce/spring 없음 + 120-180ms, 군더더기 없는 전환 + 콘텐츠 전환 위주, UI chrome 모션 최소화 + 모든 전환에 동일한 easing/duration

### 레퍼런스 근거

- **Elastic UI Framework | Elastic UI Framework**: Table Flexible tables with sorting, pagination, selection and actions Table
- **Cedar Design System | REI Co-op**: Don’t reuse bespoke UI intended for other message or navigation types Options
- **Mantine**: Navigation progress Install dependencies:

### 구현 노트

- 기존에 같은 역할의 컴포넌트가 있으면 토큰 교체부터 시작
- variant prop으로 시각적 변형을 관리 (하드코딩 금지)
- active 상태는 URL/라우터와 자동 동기화
- 애니메이션은 상태 설명용으로만 사용, 장식 효과 금지
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

- [calm+precise+editorial+trustworthy] hover: opacity 변화 (0.08-0.12), elevation 변화 없음 + 정확한 border/outline 변화 + 텍스트 underline 또는 color shift, 장식적 효과 없음 + 예측 가능하고 일관된 hover 패턴
- [calm+precise+editorial+trustworthy] density: comfortable 모드 기본, 여유로운 padding + 엄격한 spacing scale 준수, 임의 값 금지 + 넉넉한 line-height와 margin, 읽기 편한 간격 + 기존 레이아웃 유지, 갑작스런 위치 변경 없음
- [calm+precise+editorial+trustworthy] feedback: subtle inline alert 선호, 과한 컬러 블록 지양 + 명확한 상태 구분, 진행률/결과를 수치로 표시 + 콘텐츠 맥락 안에서 인라인 표시, 토스트보다 인라인 선호 + 결과를 반드시 확인, 실패 시 복구 방법 안내

### 레퍼런스 근거

- **Carbon Design System**: Number input Text input
- **Elastic UI Framework | Elastic UI Framework**: Forms Inputs with validation, grouped into a flexible form layout Forms
- **Thumbprint**: A design system only works when there’s input from a wider team. We encourage contributions both big and small from designers and developers. We’re...

### 구현 노트

- 기존에 같은 역할의 컴포넌트가 있으면 토큰 교체부터 시작
- variant prop으로 시각적 변형을 관리 (하드코딩 금지)
- error 상태에서 helper text → error message로 자동 전환
- label은 항상 visible (placeholder만으로 대체 금지)
- 애니메이션은 상태 설명용으로만 사용, 장식 효과 금지
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

- [calm+precise+editorial+trustworthy] density: comfortable 모드 기본, 여유로운 padding + 엄격한 spacing scale 준수, 임의 값 금지 + 넉넉한 line-height와 margin, 읽기 편한 간격 + 기존 레이아웃 유지, 갑작스런 위치 변경 없음
- [calm+precise+editorial+trustworthy] color: 중성 톤 위주, accent는 최소한으로 + 정확한 semantic 분리, 모호한 중간 톤 지양 + 타이포그래피로 위계 형성, 컬러보다 weight/size 활용 + 안정적인 neutral 기반, 과한 accent 변화 없음

### 구현 노트

- 기존에 같은 역할의 컴포넌트가 있으면 토큰 교체부터 시작
- variant prop으로 시각적 변형을 관리 (하드코딩 금지)
- 빈 상태(empty-state)와 에러 상태를 반드시 처리
- 애니메이션은 상태 설명용으로만 사용, 장식 효과 금지
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

- [calm+precise+editorial+trustworthy] density: comfortable 모드 기본, 여유로운 padding + 엄격한 spacing scale 준수, 임의 값 금지 + 넉넉한 line-height와 margin, 읽기 편한 간격 + 기존 레이아웃 유지, 갑작스런 위치 변경 없음
- [calm+precise+editorial+trustworthy] color: 중성 톤 위주, accent는 최소한으로 + 정확한 semantic 분리, 모호한 중간 톤 지양 + 타이포그래피로 위계 형성, 컬러보다 weight/size 활용 + 안정적인 neutral 기반, 과한 accent 변화 없음

### 구현 노트

- 기존에 같은 역할의 컴포넌트가 있으면 토큰 교체부터 시작
- variant prop으로 시각적 변형을 관리 (하드코딩 금지)
- 빈 상태(empty-state)와 에러 상태를 반드시 처리
- 애니메이션은 상태 설명용으로만 사용, 장식 효과 금지
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

- [calm+precise+editorial+trustworthy] density: comfortable 모드 기본, 여유로운 padding + 엄격한 spacing scale 준수, 임의 값 금지 + 넉넉한 line-height와 margin, 읽기 편한 간격 + 기존 레이아웃 유지, 갑작스런 위치 변경 없음
- [calm+precise+editorial+trustworthy] color: 중성 톤 위주, accent는 최소한으로 + 정확한 semantic 분리, 모호한 중간 톤 지양 + 타이포그래피로 위계 형성, 컬러보다 weight/size 활용 + 안정적인 neutral 기반, 과한 accent 변화 없음

### 구현 노트

- 기존에 같은 역할의 컴포넌트가 있으면 토큰 교체부터 시작
- variant prop으로 시각적 변형을 관리 (하드코딩 금지)
- 빈 상태(empty-state)와 에러 상태를 반드시 처리
- 애니메이션은 상태 설명용으로만 사용, 장식 효과 금지
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

- [calm+precise+editorial+trustworthy] density: comfortable 모드 기본, 여유로운 padding + 엄격한 spacing scale 준수, 임의 값 금지 + 넉넉한 line-height와 margin, 읽기 편한 간격 + 기존 레이아웃 유지, 갑작스런 위치 변경 없음
- [calm+precise+editorial+trustworthy] color: 중성 톤 위주, accent는 최소한으로 + 정확한 semantic 분리, 모호한 중간 톤 지양 + 타이포그래피로 위계 형성, 컬러보다 weight/size 활용 + 안정적인 neutral 기반, 과한 accent 변화 없음

### 구현 노트

- 기존에 같은 역할의 컴포넌트가 있으면 토큰 교체부터 시작
- variant prop으로 시각적 변형을 관리 (하드코딩 금지)
- 빈 상태(empty-state)와 에러 상태를 반드시 처리
- 애니메이션은 상태 설명용으로만 사용, 장식 효과 금지
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

- [calm+precise+editorial+trustworthy] hover: opacity 변화 (0.08-0.12), elevation 변화 없음 + 정확한 border/outline 변화 + 텍스트 underline 또는 color shift, 장식적 효과 없음 + 예측 가능하고 일관된 hover 패턴
- [calm+precise+editorial+trustworthy] density: comfortable 모드 기본, 여유로운 padding + 엄격한 spacing scale 준수, 임의 값 금지 + 넉넉한 line-height와 margin, 읽기 편한 간격 + 기존 레이아웃 유지, 갑작스런 위치 변경 없음
- [calm+precise+editorial+trustworthy] feedback: subtle inline alert 선호, 과한 컬러 블록 지양 + 명확한 상태 구분, 진행률/결과를 수치로 표시 + 콘텐츠 맥락 안에서 인라인 표시, 토스트보다 인라인 선호 + 결과를 반드시 확인, 실패 시 복구 방법 안내

### 레퍼런스 근거

- **Carbon Design System**: Number input Text input
- **Elastic UI Framework | Elastic UI Framework**: Forms Inputs with validation, grouped into a flexible form layout Forms
- **Thumbprint**: A design system only works when there’s input from a wider team. We encourage contributions both big and small from designers and developers. We’re...

### 구현 노트

- 기존에 같은 역할의 컴포넌트가 있으면 토큰 교체부터 시작
- variant prop으로 시각적 변형을 관리 (하드코딩 금지)
- error 상태에서 helper text → error message로 자동 전환
- label은 항상 visible (placeholder만으로 대체 금지)
- 애니메이션은 상태 설명용으로만 사용, 장식 효과 금지
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

- [calm+precise+editorial+trustworthy] motion: 150-200ms ease-out, bounce/spring 없음 + 120-180ms, 군더더기 없는 전환 + 콘텐츠 전환 위주, UI chrome 모션 최소화 + 모든 전환에 동일한 easing/duration
- [calm+precise+editorial+trustworthy] density: comfortable 모드 기본, 여유로운 padding + 엄격한 spacing scale 준수, 임의 값 금지 + 넉넉한 line-height와 margin, 읽기 편한 간격 + 기존 레이아웃 유지, 갑작스런 위치 변경 없음

### 레퍼런스 근거

- **Cedar Design System | REI Co-op**: Overlay, typically in the middle of the page Components
- **Workday Canvas Design System**: Interaction overlays for hover/pressed states Semantic foreground colors for info, danger, warning, success states
- **Mantine**: Core components library: inputs, buttons, overlays, etc. @mantine/form

### 구현 노트

- 기존에 같은 역할의 컴포넌트가 있으면 토큰 교체부터 시작
- variant prop으로 시각적 변형을 관리 (하드코딩 금지)
- Escape / backdrop click으로 닫기, 열 때 첫 focusable 요소로 이동
- 애니메이션은 상태 설명용으로만 사용, 장식 효과 금지
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

- [calm+precise+editorial+trustworthy] hover: opacity 변화 (0.08-0.12), elevation 변화 없음 + 정확한 border/outline 변화 + 텍스트 underline 또는 color shift, 장식적 효과 없음 + 예측 가능하고 일관된 hover 패턴
- [calm+precise+editorial+trustworthy] density: comfortable 모드 기본, 여유로운 padding + 엄격한 spacing scale 준수, 임의 값 금지 + 넉넉한 line-height와 margin, 읽기 편한 간격 + 기존 레이아웃 유지, 갑작스런 위치 변경 없음
- [calm+precise+editorial+trustworthy] motion: 150-200ms ease-out, bounce/spring 없음 + 120-180ms, 군더더기 없는 전환 + 콘텐츠 전환 위주, UI chrome 모션 최소화 + 모든 전환에 동일한 easing/duration

### 레퍼런스 근거

- **Cedar Design System | REI Co-op**: Don’t reuse bespoke UI intended for other message or navigation types Options
- **Mantine**: Navigation progress Install dependencies:
- **Chakra UI**: Here's an example of customizing the header layout with RangeText and navigation buttons. Month and Year Select

### 구현 노트

- 기존에 같은 역할의 컴포넌트가 있으면 토큰 교체부터 시작
- variant prop으로 시각적 변형을 관리 (하드코딩 금지)
- active 상태는 URL/라우터와 자동 동기화
- 애니메이션은 상태 설명용으로만 사용, 장식 효과 금지
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

- [calm+precise+editorial+trustworthy] hover: opacity 변화 (0.08-0.12), elevation 변화 없음 + 정확한 border/outline 변화 + 텍스트 underline 또는 color shift, 장식적 효과 없음 + 예측 가능하고 일관된 hover 패턴
- [calm+precise+editorial+trustworthy] density: comfortable 모드 기본, 여유로운 padding + 엄격한 spacing scale 준수, 임의 값 금지 + 넉넉한 line-height와 margin, 읽기 편한 간격 + 기존 레이아웃 유지, 갑작스런 위치 변경 없음
- [calm+precise+editorial+trustworthy] motion: 150-200ms ease-out, bounce/spring 없음 + 120-180ms, 군더더기 없는 전환 + 콘텐츠 전환 위주, UI chrome 모션 최소화 + 모든 전환에 동일한 easing/duration

### 레퍼런스 근거

- **Cedar Design System | REI Co-op**: Don’t reuse bespoke UI intended for other message or navigation types Options
- **Mantine**: Navigation progress Install dependencies:
- **Chakra UI**: Here's an example of customizing the header layout with RangeText and navigation buttons. Month and Year Select

### 구현 노트

- 기존에 같은 역할의 컴포넌트가 있으면 토큰 교체부터 시작
- variant prop으로 시각적 변형을 관리 (하드코딩 금지)
- active 상태는 URL/라우터와 자동 동기화
- 애니메이션은 상태 설명용으로만 사용, 장식 효과 금지
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

- [calm+precise+editorial+trustworthy] hover: opacity 변화 (0.08-0.12), elevation 변화 없음 + 정확한 border/outline 변화 + 텍스트 underline 또는 color shift, 장식적 효과 없음 + 예측 가능하고 일관된 hover 패턴
- [calm+precise+editorial+trustworthy] density: comfortable 모드 기본, 여유로운 padding + 엄격한 spacing scale 준수, 임의 값 금지 + 넉넉한 line-height와 margin, 읽기 편한 간격 + 기존 레이아웃 유지, 갑작스런 위치 변경 없음
- [calm+precise+editorial+trustworthy] motion: 150-200ms ease-out, bounce/spring 없음 + 120-180ms, 군더더기 없는 전환 + 콘텐츠 전환 위주, UI chrome 모션 최소화 + 모든 전환에 동일한 easing/duration

### 레퍼런스 근거

- **Cedar Design System | REI Co-op**: Don’t reuse bespoke UI intended for other message or navigation types Options
- **Mantine**: Navigation progress Install dependencies:
- **Chakra UI**: Here's an example of customizing the header layout with RangeText and navigation buttons. Month and Year Select

### 구현 노트

- 기존에 같은 역할의 컴포넌트가 있으면 토큰 교체부터 시작
- variant prop으로 시각적 변형을 관리 (하드코딩 금지)
- active 상태는 URL/라우터와 자동 동기화
- 애니메이션은 상태 설명용으로만 사용, 장식 효과 금지
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

- [calm+precise+editorial+trustworthy] hover: opacity 변화 (0.08-0.12), elevation 변화 없음 + 정확한 border/outline 변화 + 텍스트 underline 또는 color shift, 장식적 효과 없음 + 예측 가능하고 일관된 hover 패턴
- [calm+precise+editorial+trustworthy] density: comfortable 모드 기본, 여유로운 padding + 엄격한 spacing scale 준수, 임의 값 금지 + 넉넉한 line-height와 margin, 읽기 편한 간격 + 기존 레이아웃 유지, 갑작스런 위치 변경 없음
- [calm+precise+editorial+trustworthy] motion: 150-200ms ease-out, bounce/spring 없음 + 120-180ms, 군더더기 없는 전환 + 콘텐츠 전환 위주, UI chrome 모션 최소화 + 모든 전환에 동일한 easing/duration

### 레퍼런스 근거

- **Cedar Design System | REI Co-op**: Don’t reuse bespoke UI intended for other message or navigation types Options
- **Workday Canvas Design System**: The following Canvas components will be updated to reflect the new brand: Breadcrumbs, Buttons, Card, ColorPicker, Loading Dots, SearchForm, Segmen...
- **Mantine**: Navigation progress Install dependencies:

### 구현 노트

- 기존에 같은 역할의 컴포넌트가 있으면 토큰 교체부터 시작
- variant prop으로 시각적 변형을 관리 (하드코딩 금지)
- active 상태는 URL/라우터와 자동 동기화
- 애니메이션은 상태 설명용으로만 사용, 장식 효과 금지
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

- [calm+precise+editorial+trustworthy] hover: opacity 변화 (0.08-0.12), elevation 변화 없음 + 정확한 border/outline 변화 + 텍스트 underline 또는 color shift, 장식적 효과 없음 + 예측 가능하고 일관된 hover 패턴
- [calm+precise+editorial+trustworthy] density: comfortable 모드 기본, 여유로운 padding + 엄격한 spacing scale 준수, 임의 값 금지 + 넉넉한 line-height와 margin, 읽기 편한 간격 + 기존 레이아웃 유지, 갑작스런 위치 변경 없음
- [calm+precise+editorial+trustworthy] motion: 150-200ms ease-out, bounce/spring 없음 + 120-180ms, 군더더기 없는 전환 + 콘텐츠 전환 위주, UI chrome 모션 최소화 + 모든 전환에 동일한 easing/duration

### 레퍼런스 근거

- **Cedar Design System | REI Co-op**: Don’t reuse bespoke UI intended for other message or navigation types Options
- **Mantine**: Navigation progress Install dependencies:
- **Chakra UI**: Here's an example of customizing the header layout with RangeText and navigation buttons. Month and Year Select

### 구현 노트

- 기존에 같은 역할의 컴포넌트가 있으면 토큰 교체부터 시작
- variant prop으로 시각적 변형을 관리 (하드코딩 금지)
- active 상태는 URL/라우터와 자동 동기화
- 애니메이션은 상태 설명용으로만 사용, 장식 효과 금지
- 텍스트 위계가 핵심 — 컬러보다 weight/size로 구분

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

- [calm+precise+editorial+trustworthy] hover: opacity 변화 (0.08-0.12), elevation 변화 없음 + 정확한 border/outline 변화 + 텍스트 underline 또는 color shift, 장식적 효과 없음 + 예측 가능하고 일관된 hover 패턴
- [calm+precise+editorial+trustworthy] density: comfortable 모드 기본, 여유로운 padding + 엄격한 spacing scale 준수, 임의 값 금지 + 넉넉한 line-height와 margin, 읽기 편한 간격 + 기존 레이아웃 유지, 갑작스런 위치 변경 없음
- [calm+precise+editorial+trustworthy] feedback: subtle inline alert 선호, 과한 컬러 블록 지양 + 명확한 상태 구분, 진행률/결과를 수치로 표시 + 콘텐츠 맥락 안에서 인라인 표시, 토스트보다 인라인 선호 + 결과를 반드시 확인, 실패 시 복구 방법 안내

### 레퍼런스 근거

- **Carbon Design System**: Date picker Number input
- **Elastic UI Framework | Elastic UI Framework**: Forms Inputs with validation, grouped into a flexible form layout Forms
- **Thumbprint**: A design system only works when there’s input from a wider team. We encourage contributions both big and small from designers and developers. We’re...

### 구현 노트

- 기존에 같은 역할의 컴포넌트가 있으면 토큰 교체부터 시작
- variant prop으로 시각적 변형을 관리 (하드코딩 금지)
- error 상태에서 helper text → error message로 자동 전환
- label은 항상 visible (placeholder만으로 대체 금지)
- 애니메이션은 상태 설명용으로만 사용, 장식 효과 금지
- 텍스트 위계가 핵심 — 컬러보다 weight/size로 구분

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

- [calm+precise+editorial+trustworthy] density: comfortable 모드 기본, 여유로운 padding + 엄격한 spacing scale 준수, 임의 값 금지 + 넉넉한 line-height와 margin, 읽기 편한 간격 + 기존 레이아웃 유지, 갑작스런 위치 변경 없음
- [calm+precise+editorial+trustworthy] color: 중성 톤 위주, accent는 최소한으로 + 정확한 semantic 분리, 모호한 중간 톤 지양 + 타이포그래피로 위계 형성, 컬러보다 weight/size 활용 + 안정적인 neutral 기반, 과한 accent 변화 없음

### 구현 노트

- 기존에 같은 역할의 컴포넌트가 있으면 토큰 교체부터 시작
- variant prop으로 시각적 변형을 관리 (하드코딩 금지)
- 빈 상태(empty-state)와 에러 상태를 반드시 처리
- 애니메이션은 상태 설명용으로만 사용, 장식 효과 금지
- 텍스트 위계가 핵심 — 컬러보다 weight/size로 구분

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

- [calm+precise+editorial+trustworthy] hover: opacity 변화 (0.08-0.12), elevation 변화 없음 + 정확한 border/outline 변화 + 텍스트 underline 또는 color shift, 장식적 효과 없음 + 예측 가능하고 일관된 hover 패턴
- [calm+precise+editorial+trustworthy] density: comfortable 모드 기본, 여유로운 padding + 엄격한 spacing scale 준수, 임의 값 금지 + 넉넉한 line-height와 margin, 읽기 편한 간격 + 기존 레이아웃 유지, 갑작스런 위치 변경 없음
- [calm+precise+editorial+trustworthy] feedback: subtle inline alert 선호, 과한 컬러 블록 지양 + 명확한 상태 구분, 진행률/결과를 수치로 표시 + 콘텐츠 맥락 안에서 인라인 표시, 토스트보다 인라인 선호 + 결과를 반드시 확인, 실패 시 복구 방법 안내

### 레퍼런스 근거

- **Carbon Design System**: Number input Text input
- **Elastic UI Framework | Elastic UI Framework**: Forms Inputs with validation, grouped into a flexible form layout Forms
- **Thumbprint**: A design system only works when there’s input from a wider team. We encourage contributions both big and small from designers and developers. We’re...

### 구현 노트

- 기존에 같은 역할의 컴포넌트가 있으면 토큰 교체부터 시작
- variant prop으로 시각적 변형을 관리 (하드코딩 금지)
- error 상태에서 helper text → error message로 자동 전환
- label은 항상 visible (placeholder만으로 대체 금지)
- 애니메이션은 상태 설명용으로만 사용, 장식 효과 금지
- 텍스트 위계가 핵심 — 컬러보다 weight/size로 구분

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

- [calm+precise+editorial+trustworthy] hover: opacity 변화 (0.08-0.12), elevation 변화 없음 + 정확한 border/outline 변화 + 텍스트 underline 또는 color shift, 장식적 효과 없음 + 예측 가능하고 일관된 hover 패턴
- [calm+precise+editorial+trustworthy] density: comfortable 모드 기본, 여유로운 padding + 엄격한 spacing scale 준수, 임의 값 금지 + 넉넉한 line-height와 margin, 읽기 편한 간격 + 기존 레이아웃 유지, 갑작스런 위치 변경 없음
- [calm+precise+editorial+trustworthy] feedback: subtle inline alert 선호, 과한 컬러 블록 지양 + 명확한 상태 구분, 진행률/결과를 수치로 표시 + 콘텐츠 맥락 안에서 인라인 표시, 토스트보다 인라인 선호 + 결과를 반드시 확인, 실패 시 복구 방법 안내

### 레퍼런스 근거

- **Carbon Design System**: Number input Text input
- **Elastic UI Framework | Elastic UI Framework**: Forms Inputs with validation, grouped into a flexible form layout Forms
- **Thumbprint**: A design system only works when there’s input from a wider team. We encourage contributions both big and small from designers and developers. We’re...

### 구현 노트

- 기존에 같은 역할의 컴포넌트가 있으면 토큰 교체부터 시작
- variant prop으로 시각적 변형을 관리 (하드코딩 금지)
- error 상태에서 helper text → error message로 자동 전환
- label은 항상 visible (placeholder만으로 대체 금지)
- 애니메이션은 상태 설명용으로만 사용, 장식 효과 금지
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

- [calm+precise+editorial+trustworthy] feedback: subtle inline alert 선호, 과한 컬러 블록 지양 + 명확한 상태 구분, 진행률/결과를 수치로 표시 + 콘텐츠 맥락 안에서 인라인 표시, 토스트보다 인라인 선호 + 결과를 반드시 확인, 실패 시 복구 방법 안내
- [calm+precise+editorial+trustworthy] motion: 150-200ms ease-out, bounce/spring 없음 + 120-180ms, 군더더기 없는 전환 + 콘텐츠 전환 위주, UI chrome 모션 최소화 + 모든 전환에 동일한 easing/duration
- [calm+precise+editorial+trustworthy] color: 중성 톤 위주, accent는 최소한으로 + 정확한 semantic 분리, 모호한 중간 톤 지양 + 타이포그래피로 위계 형성, 컬러보다 weight/size 활용 + 안정적인 neutral 기반, 과한 accent 변화 없음

### 레퍼런스 근거

- **Atlassian Design**: We finish what we start before starting something new. We're informed by continuous feedback. 3. Bring people on the journey before helping for the...
- **Carbon Design System**: We welcome all feedback, designs, or ideas in order to produce the best possible experience for our users. If you're interested in contributing, ch...
- **Clarity Design System**: Clarity firmly believes that the best products are built by those who form a rich, varied community. We invite all forms of feedback or ideas that ...

### 구현 노트

- 기존에 같은 역할의 컴포넌트가 있으면 토큰 교체부터 시작
- variant prop으로 시각적 변형을 관리 (하드코딩 금지)
- auto-dismiss 시간은 내용 길이에 비례 (기본 5초)
- 애니메이션은 상태 설명용으로만 사용, 장식 효과 금지
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

- [calm+precise+editorial+trustworthy] feedback: subtle inline alert 선호, 과한 컬러 블록 지양 + 명확한 상태 구분, 진행률/결과를 수치로 표시 + 콘텐츠 맥락 안에서 인라인 표시, 토스트보다 인라인 선호 + 결과를 반드시 확인, 실패 시 복구 방법 안내
- [calm+precise+editorial+trustworthy] motion: 150-200ms ease-out, bounce/spring 없음 + 120-180ms, 군더더기 없는 전환 + 콘텐츠 전환 위주, UI chrome 모션 최소화 + 모든 전환에 동일한 easing/duration
- [calm+precise+editorial+trustworthy] color: 중성 톤 위주, accent는 최소한으로 + 정확한 semantic 분리, 모호한 중간 톤 지양 + 타이포그래피로 위계 형성, 컬러보다 weight/size 활용 + 안정적인 neutral 기반, 과한 accent 변화 없음

### 레퍼런스 근거

- **Atlassian Design**: We finish what we start before starting something new. We're informed by continuous feedback. 3. Bring people on the journey before helping for the...
- **Carbon Design System**: We welcome all feedback, designs, or ideas in order to produce the best possible experience for our users. If you're interested in contributing, ch...
- **Clarity Design System**: Clarity firmly believes that the best products are built by those who form a rich, varied community. We invite all forms of feedback or ideas that ...

### 구현 노트

- 기존에 같은 역할의 컴포넌트가 있으면 토큰 교체부터 시작
- variant prop으로 시각적 변형을 관리 (하드코딩 금지)
- auto-dismiss 시간은 내용 길이에 비례 (기본 5초)
- 애니메이션은 상태 설명용으로만 사용, 장식 효과 금지
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

- [calm+precise+editorial+trustworthy] feedback: subtle inline alert 선호, 과한 컬러 블록 지양 + 명확한 상태 구분, 진행률/결과를 수치로 표시 + 콘텐츠 맥락 안에서 인라인 표시, 토스트보다 인라인 선호 + 결과를 반드시 확인, 실패 시 복구 방법 안내
- [calm+precise+editorial+trustworthy] motion: 150-200ms ease-out, bounce/spring 없음 + 120-180ms, 군더더기 없는 전환 + 콘텐츠 전환 위주, UI chrome 모션 최소화 + 모든 전환에 동일한 easing/duration
- [calm+precise+editorial+trustworthy] color: 중성 톤 위주, accent는 최소한으로 + 정확한 semantic 분리, 모호한 중간 톤 지양 + 타이포그래피로 위계 형성, 컬러보다 weight/size 활용 + 안정적인 neutral 기반, 과한 accent 변화 없음

### 레퍼런스 근거

- **Atlassian Design**: We finish what we start before starting something new. We're informed by continuous feedback. 3. Bring people on the journey before helping for the...
- **Carbon Design System**: We welcome all feedback, designs, or ideas in order to produce the best possible experience for our users. If you're interested in contributing, ch...
- **Clarity Design System**: Clarity firmly believes that the best products are built by those who form a rich, varied community. We invite all forms of feedback or ideas that ...

### 구현 노트

- 기존에 같은 역할의 컴포넌트가 있으면 토큰 교체부터 시작
- variant prop으로 시각적 변형을 관리 (하드코딩 금지)
- auto-dismiss 시간은 내용 길이에 비례 (기본 5초)
- 애니메이션은 상태 설명용으로만 사용, 장식 효과 금지
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

- [calm+precise+editorial+trustworthy] feedback: subtle inline alert 선호, 과한 컬러 블록 지양 + 명확한 상태 구분, 진행률/결과를 수치로 표시 + 콘텐츠 맥락 안에서 인라인 표시, 토스트보다 인라인 선호 + 결과를 반드시 확인, 실패 시 복구 방법 안내
- [calm+precise+editorial+trustworthy] motion: 150-200ms ease-out, bounce/spring 없음 + 120-180ms, 군더더기 없는 전환 + 콘텐츠 전환 위주, UI chrome 모션 최소화 + 모든 전환에 동일한 easing/duration
- [calm+precise+editorial+trustworthy] color: 중성 톤 위주, accent는 최소한으로 + 정확한 semantic 분리, 모호한 중간 톤 지양 + 타이포그래피로 위계 형성, 컬러보다 weight/size 활용 + 안정적인 neutral 기반, 과한 accent 변화 없음

### 레퍼런스 근거

- **Atlassian Design**: We finish what we start before starting something new. We're informed by continuous feedback. 3. Bring people on the journey before helping for the...
- **Carbon Design System**: We welcome all feedback, designs, or ideas in order to produce the best possible experience for our users. If you're interested in contributing, ch...
- **Clarity Design System**: Clarity firmly believes that the best products are built by those who form a rich, varied community. We invite all forms of feedback or ideas that ...

### 구현 노트

- 기존에 같은 역할의 컴포넌트가 있으면 토큰 교체부터 시작
- variant prop으로 시각적 변형을 관리 (하드코딩 금지)
- auto-dismiss 시간은 내용 길이에 비례 (기본 5초)
- 애니메이션은 상태 설명용으로만 사용, 장식 효과 금지
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

- [calm+precise+editorial+trustworthy] hover: opacity 변화 (0.08-0.12), elevation 변화 없음 + 정확한 border/outline 변화 + 텍스트 underline 또는 color shift, 장식적 효과 없음 + 예측 가능하고 일관된 hover 패턴
- [calm+precise+editorial+trustworthy] density: comfortable 모드 기본, 여유로운 padding + 엄격한 spacing scale 준수, 임의 값 금지 + 넉넉한 line-height와 margin, 읽기 편한 간격 + 기존 레이아웃 유지, 갑작스런 위치 변경 없음
- [calm+precise+editorial+trustworthy] feedback: subtle inline alert 선호, 과한 컬러 블록 지양 + 명확한 상태 구분, 진행률/결과를 수치로 표시 + 콘텐츠 맥락 안에서 인라인 표시, 토스트보다 인라인 선호 + 결과를 반드시 확인, 실패 시 복구 방법 안내

### 레퍼런스 근거

- **Carbon Design System**: Number input Text input
- **Elastic UI Framework | Elastic UI Framework**: Forms Inputs with validation, grouped into a flexible form layout Forms
- **Thumbprint**: A design system only works when there’s input from a wider team. We encourage contributions both big and small from designers and developers. We’re...

### 구현 노트

- 기존에 같은 역할의 컴포넌트가 있으면 토큰 교체부터 시작
- variant prop으로 시각적 변형을 관리 (하드코딩 금지)
- error 상태에서 helper text → error message로 자동 전환
- label은 항상 visible (placeholder만으로 대체 금지)
- 애니메이션은 상태 설명용으로만 사용, 장식 효과 금지
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

- [calm+precise+editorial+trustworthy] density: comfortable 모드 기본, 여유로운 padding + 엄격한 spacing scale 준수, 임의 값 금지 + 넉넉한 line-height와 margin, 읽기 편한 간격 + 기존 레이아웃 유지, 갑작스런 위치 변경 없음
- [calm+precise+editorial+trustworthy] color: 중성 톤 위주, accent는 최소한으로 + 정확한 semantic 분리, 모호한 중간 톤 지양 + 타이포그래피로 위계 형성, 컬러보다 weight/size 활용 + 안정적인 neutral 기반, 과한 accent 변화 없음

### 구현 노트

- 기존에 같은 역할의 컴포넌트가 있으면 토큰 교체부터 시작
- variant prop으로 시각적 변형을 관리 (하드코딩 금지)
- 빈 상태(empty-state)와 에러 상태를 반드시 처리
- 애니메이션은 상태 설명용으로만 사용, 장식 효과 금지
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

- [calm+precise+editorial+trustworthy] hover: opacity 변화 (0.08-0.12), elevation 변화 없음 + 정확한 border/outline 변화 + 텍스트 underline 또는 color shift, 장식적 효과 없음 + 예측 가능하고 일관된 hover 패턴
- [calm+precise+editorial+trustworthy] density: comfortable 모드 기본, 여유로운 padding + 엄격한 spacing scale 준수, 임의 값 금지 + 넉넉한 line-height와 margin, 읽기 편한 간격 + 기존 레이아웃 유지, 갑작스런 위치 변경 없음
- [calm+precise+editorial+trustworthy] feedback: subtle inline alert 선호, 과한 컬러 블록 지양 + 명확한 상태 구분, 진행률/결과를 수치로 표시 + 콘텐츠 맥락 안에서 인라인 표시, 토스트보다 인라인 선호 + 결과를 반드시 확인, 실패 시 복구 방법 안내

### 레퍼런스 근거

- **Carbon Design System**: Number input Text input
- **Elastic UI Framework | Elastic UI Framework**: Forms Inputs with validation, grouped into a flexible form layout Forms
- **Thumbprint**: A design system only works when there’s input from a wider team. We encourage contributions both big and small from designers and developers. We’re...

### 구현 노트

- 기존에 같은 역할의 컴포넌트가 있으면 토큰 교체부터 시작
- variant prop으로 시각적 변형을 관리 (하드코딩 금지)
- error 상태에서 helper text → error message로 자동 전환
- label은 항상 visible (placeholder만으로 대체 금지)
- 애니메이션은 상태 설명용으로만 사용, 장식 효과 금지
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

- [calm+precise+editorial+trustworthy] motion: 150-200ms ease-out, bounce/spring 없음 + 120-180ms, 군더더기 없는 전환 + 콘텐츠 전환 위주, UI chrome 모션 최소화 + 모든 전환에 동일한 easing/duration
- [calm+precise+editorial+trustworthy] density: comfortable 모드 기본, 여유로운 padding + 엄격한 spacing scale 준수, 임의 값 금지 + 넉넉한 line-height와 margin, 읽기 편한 간격 + 기존 레이아웃 유지, 갑작스런 위치 변경 없음

### 레퍼런스 근거

- **Cedar Design System | REI Co-op**: Overlay, typically in the middle of the page Components
- **Workday Canvas Design System**: Interaction overlays for hover/pressed states Semantic foreground colors for info, danger, warning, success states
- **Mantine**: Combobox is a composable component which can be used to create custom select, multiselect, autocomplete, tags input and other similar components. I...

### 구현 노트

- 기존에 같은 역할의 컴포넌트가 있으면 토큰 교체부터 시작
- variant prop으로 시각적 변형을 관리 (하드코딩 금지)
- Escape / backdrop click으로 닫기, 열 때 첫 focusable 요소로 이동
- 애니메이션은 상태 설명용으로만 사용, 장식 효과 금지
- 텍스트 위계가 핵심 — 컬러보다 weight/size로 구분

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

- [calm+precise+editorial+trustworthy] motion: 150-200ms ease-out, bounce/spring 없음 + 120-180ms, 군더더기 없는 전환 + 콘텐츠 전환 위주, UI chrome 모션 최소화 + 모든 전환에 동일한 easing/duration
- [calm+precise+editorial+trustworthy] density: comfortable 모드 기본, 여유로운 padding + 엄격한 spacing scale 준수, 임의 값 금지 + 넉넉한 line-height와 margin, 읽기 편한 간격 + 기존 레이아웃 유지, 갑작스런 위치 변경 없음

### 레퍼런스 근거

- **Cedar Design System | REI Co-op**: Overlay, typically in the middle of the page Components
- **Workday Canvas Design System**: Interaction overlays for hover/pressed states Semantic foreground colors for info, danger, warning, success states
- **Mantine**: Ctrl + K command palette, can be used for search or common actions Carousel

### 구현 노트

- 기존에 같은 역할의 컴포넌트가 있으면 토큰 교체부터 시작
- variant prop으로 시각적 변형을 관리 (하드코딩 금지)
- Escape / backdrop click으로 닫기, 열 때 첫 focusable 요소로 이동
- 애니메이션은 상태 설명용으로만 사용, 장식 효과 금지
- 텍스트 위계가 핵심 — 컬러보다 weight/size로 구분

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

- [calm+precise+editorial+trustworthy] motion: 150-200ms ease-out, bounce/spring 없음 + 120-180ms, 군더더기 없는 전환 + 콘텐츠 전환 위주, UI chrome 모션 최소화 + 모든 전환에 동일한 easing/duration
- [calm+precise+editorial+trustworthy] density: comfortable 모드 기본, 여유로운 padding + 엄격한 spacing scale 준수, 임의 값 금지 + 넉넉한 line-height와 margin, 읽기 편한 간격 + 기존 레이아웃 유지, 갑작스런 위치 변경 없음

### 레퍼런스 근거

- **Cedar Design System | REI Co-op**: Overlay, typically in the middle of the page Components
- **Workday Canvas Design System**: Interaction overlays for hover/pressed states Semantic foreground colors for info, danger, warning, success states
- **Mantine**: Core components library: inputs, buttons, overlays, etc. @mantine/form

### 구현 노트

- 기존에 같은 역할의 컴포넌트가 있으면 토큰 교체부터 시작
- variant prop으로 시각적 변형을 관리 (하드코딩 금지)
- Escape / backdrop click으로 닫기, 열 때 첫 focusable 요소로 이동
- 애니메이션은 상태 설명용으로만 사용, 장식 효과 금지
- 텍스트 위계가 핵심 — 컬러보다 weight/size로 구분

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

- [calm+precise+editorial+trustworthy] feedback: subtle inline alert 선호, 과한 컬러 블록 지양 + 명확한 상태 구분, 진행률/결과를 수치로 표시 + 콘텐츠 맥락 안에서 인라인 표시, 토스트보다 인라인 선호 + 결과를 반드시 확인, 실패 시 복구 방법 안내
- [calm+precise+editorial+trustworthy] motion: 150-200ms ease-out, bounce/spring 없음 + 120-180ms, 군더더기 없는 전환 + 콘텐츠 전환 위주, UI chrome 모션 최소화 + 모든 전환에 동일한 easing/duration
- [calm+precise+editorial+trustworthy] color: 중성 톤 위주, accent는 최소한으로 + 정확한 semantic 분리, 모호한 중간 톤 지양 + 타이포그래피로 위계 형성, 컬러보다 weight/size 활용 + 안정적인 neutral 기반, 과한 accent 변화 없음

### 레퍼런스 근거

- **Atlassian Design**: We finish what we start before starting something new. We're informed by continuous feedback. 3. Bring people on the journey before helping for the...
- **Carbon Design System**: We welcome all feedback, designs, or ideas in order to produce the best possible experience for our users. If you're interested in contributing, ch...
- **Clarity Design System**: Clarity firmly believes that the best products are built by those who form a rich, varied community. We invite all forms of feedback or ideas that ...

### 구현 노트

- 기존에 같은 역할의 컴포넌트가 있으면 토큰 교체부터 시작
- variant prop으로 시각적 변형을 관리 (하드코딩 금지)
- auto-dismiss 시간은 내용 길이에 비례 (기본 5초)
- 애니메이션은 상태 설명용으로만 사용, 장식 효과 금지
- 텍스트 위계가 핵심 — 컬러보다 weight/size로 구분

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

- [calm+precise+editorial+trustworthy] density: comfortable 모드 기본, 여유로운 padding + 엄격한 spacing scale 준수, 임의 값 금지 + 넉넉한 line-height와 margin, 읽기 편한 간격 + 기존 레이아웃 유지, 갑작스런 위치 변경 없음
- [calm+precise+editorial+trustworthy] color: 중성 톤 위주, accent는 최소한으로 + 정확한 semantic 분리, 모호한 중간 톤 지양 + 타이포그래피로 위계 형성, 컬러보다 weight/size 활용 + 안정적인 neutral 기반, 과한 accent 변화 없음

### 구현 노트

- 기존에 같은 역할의 컴포넌트가 있으면 토큰 교체부터 시작
- variant prop으로 시각적 변형을 관리 (하드코딩 금지)
- 빈 상태(empty-state)와 에러 상태를 반드시 처리
- 애니메이션은 상태 설명용으로만 사용, 장식 효과 금지
- 텍스트 위계가 핵심 — 컬러보다 weight/size로 구분

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

- [calm+precise+editorial+trustworthy] density: comfortable 모드 기본, 여유로운 padding + 엄격한 spacing scale 준수, 임의 값 금지 + 넉넉한 line-height와 margin, 읽기 편한 간격 + 기존 레이아웃 유지, 갑작스런 위치 변경 없음
- [calm+precise+editorial+trustworthy] color: 중성 톤 위주, accent는 최소한으로 + 정확한 semantic 분리, 모호한 중간 톤 지양 + 타이포그래피로 위계 형성, 컬러보다 weight/size 활용 + 안정적인 neutral 기반, 과한 accent 변화 없음

### 구현 노트

- 기존에 같은 역할의 컴포넌트가 있으면 토큰 교체부터 시작
- variant prop으로 시각적 변형을 관리 (하드코딩 금지)
- 빈 상태(empty-state)와 에러 상태를 반드시 처리
- 애니메이션은 상태 설명용으로만 사용, 장식 효과 금지
- 텍스트 위계가 핵심 — 컬러보다 weight/size로 구분

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

- [calm+precise+editorial+trustworthy] density: comfortable 모드 기본, 여유로운 padding + 엄격한 spacing scale 준수, 임의 값 금지 + 넉넉한 line-height와 margin, 읽기 편한 간격 + 기존 레이아웃 유지, 갑작스런 위치 변경 없음
- [calm+precise+editorial+trustworthy] color: 중성 톤 위주, accent는 최소한으로 + 정확한 semantic 분리, 모호한 중간 톤 지양 + 타이포그래피로 위계 형성, 컬러보다 weight/size 활용 + 안정적인 neutral 기반, 과한 accent 변화 없음

### 구현 노트

- 기존에 같은 역할의 컴포넌트가 있으면 토큰 교체부터 시작
- variant prop으로 시각적 변형을 관리 (하드코딩 금지)
- 빈 상태(empty-state)와 에러 상태를 반드시 처리
- 애니메이션은 상태 설명용으로만 사용, 장식 효과 금지
- 텍스트 위계가 핵심 — 컬러보다 weight/size로 구분

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

- [calm+precise+editorial+trustworthy] density: comfortable 모드 기본, 여유로운 padding + 엄격한 spacing scale 준수, 임의 값 금지 + 넉넉한 line-height와 margin, 읽기 편한 간격 + 기존 레이아웃 유지, 갑작스런 위치 변경 없음
- [calm+precise+editorial+trustworthy] color: 중성 톤 위주, accent는 최소한으로 + 정확한 semantic 분리, 모호한 중간 톤 지양 + 타이포그래피로 위계 형성, 컬러보다 weight/size 활용 + 안정적인 neutral 기반, 과한 accent 변화 없음

### 구현 노트

- 기존에 같은 역할의 컴포넌트가 있으면 토큰 교체부터 시작
- variant prop으로 시각적 변형을 관리 (하드코딩 금지)
- 빈 상태(empty-state)와 에러 상태를 반드시 처리
- 애니메이션은 상태 설명용으로만 사용, 장식 효과 금지
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

- [calm+precise+editorial+trustworthy] density: comfortable 모드 기본, 여유로운 padding + 엄격한 spacing scale 준수, 임의 값 금지 + 넉넉한 line-height와 margin, 읽기 편한 간격 + 기존 레이아웃 유지, 갑작스런 위치 변경 없음
- [calm+precise+editorial+trustworthy] color: 중성 톤 위주, accent는 최소한으로 + 정확한 semantic 분리, 모호한 중간 톤 지양 + 타이포그래피로 위계 형성, 컬러보다 weight/size 활용 + 안정적인 neutral 기반, 과한 accent 변화 없음

### 구현 노트

- 기존에 같은 역할의 컴포넌트가 있으면 토큰 교체부터 시작
- variant prop으로 시각적 변형을 관리 (하드코딩 금지)
- 빈 상태(empty-state)와 에러 상태를 반드시 처리
- 애니메이션은 상태 설명용으로만 사용, 장식 효과 금지
- 텍스트 위계가 핵심 — 컬러보다 weight/size로 구분

---

## data-display / feature-comparison

**역할**: 플랜 간 기능 비교 테이블

**탐지 출처**: pricing and plans

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

- [calm+precise+editorial+trustworthy] density: comfortable 모드 기본, 여유로운 padding + 엄격한 spacing scale 준수, 임의 값 금지 + 넉넉한 line-height와 margin, 읽기 편한 간격 + 기존 레이아웃 유지, 갑작스런 위치 변경 없음
- [calm+precise+editorial+trustworthy] color: 중성 톤 위주, accent는 최소한으로 + 정확한 semantic 분리, 모호한 중간 톤 지양 + 타이포그래피로 위계 형성, 컬러보다 weight/size 활용 + 안정적인 neutral 기반, 과한 accent 변화 없음

### 구현 노트

- 기존에 같은 역할의 컴포넌트가 있으면 토큰 교체부터 시작
- variant prop으로 시각적 변형을 관리 (하드코딩 금지)
- 빈 상태(empty-state)와 에러 상태를 반드시 처리
- 애니메이션은 상태 설명용으로만 사용, 장식 효과 금지
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

- [calm+precise+editorial+trustworthy] feedback: subtle inline alert 선호, 과한 컬러 블록 지양 + 명확한 상태 구분, 진행률/결과를 수치로 표시 + 콘텐츠 맥락 안에서 인라인 표시, 토스트보다 인라인 선호 + 결과를 반드시 확인, 실패 시 복구 방법 안내
- [calm+precise+editorial+trustworthy] motion: 150-200ms ease-out, bounce/spring 없음 + 120-180ms, 군더더기 없는 전환 + 콘텐츠 전환 위주, UI chrome 모션 최소화 + 모든 전환에 동일한 easing/duration
- [calm+precise+editorial+trustworthy] color: 중성 톤 위주, accent는 최소한으로 + 정확한 semantic 분리, 모호한 중간 톤 지양 + 타이포그래피로 위계 형성, 컬러보다 weight/size 활용 + 안정적인 neutral 기반, 과한 accent 변화 없음

### 레퍼런스 근거

- **Atlassian Design**: We finish what we start before starting something new. We're informed by continuous feedback. 3. Bring people on the journey before helping for the...
- **Carbon Design System**: We welcome all feedback, designs, or ideas in order to produce the best possible experience for our users. If you're interested in contributing, ch...
- **Clarity Design System**: Clarity firmly believes that the best products are built by those who form a rich, varied community. We invite all forms of feedback or ideas that ...

### 구현 노트

- 기존에 같은 역할의 컴포넌트가 있으면 토큰 교체부터 시작
- variant prop으로 시각적 변형을 관리 (하드코딩 금지)
- auto-dismiss 시간은 내용 길이에 비례 (기본 5초)
- 애니메이션은 상태 설명용으로만 사용, 장식 효과 금지
- 텍스트 위계가 핵심 — 컬러보다 weight/size로 구분

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

- [calm+precise+editorial+trustworthy] color: 중성 톤 위주, accent는 최소한으로 + 정확한 semantic 분리, 모호한 중간 톤 지양 + 타이포그래피로 위계 형성, 컬러보다 weight/size 활용 + 안정적인 neutral 기반, 과한 accent 변화 없음
- [calm+precise+editorial+trustworthy] motion: 150-200ms ease-out, bounce/spring 없음 + 120-180ms, 군더더기 없는 전환 + 콘텐츠 전환 위주, UI chrome 모션 최소화 + 모든 전환에 동일한 easing/duration
- [calm+precise+editorial+trustworthy] density: comfortable 모드 기본, 여유로운 padding + 엄격한 spacing scale 준수, 임의 값 금지 + 넉넉한 line-height와 margin, 읽기 편한 간격 + 기존 레이아웃 유지, 갑작스런 위치 변경 없음

### 레퍼런스 근거

- **Primer**: Design digital marketing experiences with Primer Brand UI Shared Foundations
- **Mozilla Protocol**: Protocol is still an evolving project. Currently it’s used primarily by the Mozilla Marketing Websites team as the front-end for www.mozilla.org . ...
- **Pajamas Design System**: creative agency or vendor collaborating with us on our marketing efforts. partner or customer that is interested in representing our brand on digit...

### 구현 노트

- 기존에 같은 역할의 컴포넌트가 있으면 토큰 교체부터 시작
- variant prop으로 시각적 변형을 관리 (하드코딩 금지)
- 섹션에 <h2 id="...">과 aria-labelledby 필수
- CSS 변수(var(--color-*))를 그대로 쓰고 hex 하드코딩 금지
- 다크 모드는 globals.css의 prefers-color-scheme 블록에 위임
- 애니메이션은 상태 설명용으로만 사용, 장식 효과 금지
- 텍스트 위계가 핵심 — 컬러보다 weight/size로 구분

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

- [calm+precise+editorial+trustworthy] color: 중성 톤 위주, accent는 최소한으로 + 정확한 semantic 분리, 모호한 중간 톤 지양 + 타이포그래피로 위계 형성, 컬러보다 weight/size 활용 + 안정적인 neutral 기반, 과한 accent 변화 없음
- [calm+precise+editorial+trustworthy] motion: 150-200ms ease-out, bounce/spring 없음 + 120-180ms, 군더더기 없는 전환 + 콘텐츠 전환 위주, UI chrome 모션 최소화 + 모든 전환에 동일한 easing/duration
- [calm+precise+editorial+trustworthy] density: comfortable 모드 기본, 여유로운 padding + 엄격한 spacing scale 준수, 임의 값 금지 + 넉넉한 line-height와 margin, 읽기 편한 간격 + 기존 레이아웃 유지, 갑작스런 위치 변경 없음

### 레퍼런스 근거

- **Primer**: Design digital marketing experiences with Primer Brand UI Shared Foundations
- **Mozilla Protocol**: Protocol is still an evolving project. Currently it’s used primarily by the Mozilla Marketing Websites team as the front-end for www.mozilla.org . ...
- **Pajamas Design System**: creative agency or vendor collaborating with us on our marketing efforts. partner or customer that is interested in representing our brand on digit...

### 구현 노트

- 기존에 같은 역할의 컴포넌트가 있으면 토큰 교체부터 시작
- variant prop으로 시각적 변형을 관리 (하드코딩 금지)
- 섹션에 <h2 id="...">과 aria-labelledby 필수
- CSS 변수(var(--color-*))를 그대로 쓰고 hex 하드코딩 금지
- 다크 모드는 globals.css의 prefers-color-scheme 블록에 위임
- 애니메이션은 상태 설명용으로만 사용, 장식 효과 금지
- 텍스트 위계가 핵심 — 컬러보다 weight/size로 구분

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

- [calm+precise+editorial+trustworthy] color: 중성 톤 위주, accent는 최소한으로 + 정확한 semantic 분리, 모호한 중간 톤 지양 + 타이포그래피로 위계 형성, 컬러보다 weight/size 활용 + 안정적인 neutral 기반, 과한 accent 변화 없음
- [calm+precise+editorial+trustworthy] motion: 150-200ms ease-out, bounce/spring 없음 + 120-180ms, 군더더기 없는 전환 + 콘텐츠 전환 위주, UI chrome 모션 최소화 + 모든 전환에 동일한 easing/duration
- [calm+precise+editorial+trustworthy] density: comfortable 모드 기본, 여유로운 padding + 엄격한 spacing scale 준수, 임의 값 금지 + 넉넉한 line-height와 margin, 읽기 편한 간격 + 기존 레이아웃 유지, 갑작스런 위치 변경 없음

### 레퍼런스 근거

- **Primer**: Design digital marketing experiences with Primer Brand UI Shared Foundations
- **Mozilla Protocol**: Protocol is still an evolving project. Currently it’s used primarily by the Mozilla Marketing Websites team as the front-end for www.mozilla.org . ...
- **Pajamas Design System**: creative agency or vendor collaborating with us on our marketing efforts. partner or customer that is interested in representing our brand on digit...

### 구현 노트

- 기존에 같은 역할의 컴포넌트가 있으면 토큰 교체부터 시작
- variant prop으로 시각적 변형을 관리 (하드코딩 금지)
- 섹션에 <h2 id="...">과 aria-labelledby 필수
- CSS 변수(var(--color-*))를 그대로 쓰고 hex 하드코딩 금지
- 다크 모드는 globals.css의 prefers-color-scheme 블록에 위임
- 애니메이션은 상태 설명용으로만 사용, 장식 효과 금지
- 텍스트 위계가 핵심 — 컬러보다 weight/size로 구분

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

- [calm+precise+editorial+trustworthy] color: 중성 톤 위주, accent는 최소한으로 + 정확한 semantic 분리, 모호한 중간 톤 지양 + 타이포그래피로 위계 형성, 컬러보다 weight/size 활용 + 안정적인 neutral 기반, 과한 accent 변화 없음
- [calm+precise+editorial+trustworthy] motion: 150-200ms ease-out, bounce/spring 없음 + 120-180ms, 군더더기 없는 전환 + 콘텐츠 전환 위주, UI chrome 모션 최소화 + 모든 전환에 동일한 easing/duration
- [calm+precise+editorial+trustworthy] density: comfortable 모드 기본, 여유로운 padding + 엄격한 spacing scale 준수, 임의 값 금지 + 넉넉한 line-height와 margin, 읽기 편한 간격 + 기존 레이아웃 유지, 갑작스런 위치 변경 없음

### 레퍼런스 근거

- **Primer**: Design digital marketing experiences with Primer Brand UI Shared Foundations
- **Mozilla Protocol**: Protocol is still an evolving project. Currently it’s used primarily by the Mozilla Marketing Websites team as the front-end for www.mozilla.org . ...
- **Pajamas Design System**: creative agency or vendor collaborating with us on our marketing efforts. partner or customer that is interested in representing our brand on digit...

### 구현 노트

- 기존에 같은 역할의 컴포넌트가 있으면 토큰 교체부터 시작
- variant prop으로 시각적 변형을 관리 (하드코딩 금지)
- 섹션에 <h2 id="...">과 aria-labelledby 필수
- CSS 변수(var(--color-*))를 그대로 쓰고 hex 하드코딩 금지
- 다크 모드는 globals.css의 prefers-color-scheme 블록에 위임
- 애니메이션은 상태 설명용으로만 사용, 장식 효과 금지
- 텍스트 위계가 핵심 — 컬러보다 weight/size로 구분

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

- [calm+precise+editorial+trustworthy] hover: opacity 변화 (0.08-0.12), elevation 변화 없음 + 정확한 border/outline 변화 + 텍스트 underline 또는 color shift, 장식적 효과 없음 + 예측 가능하고 일관된 hover 패턴
- [calm+precise+editorial+trustworthy] motion: 150-200ms ease-out, bounce/spring 없음 + 120-180ms, 군더더기 없는 전환 + 콘텐츠 전환 위주, UI chrome 모션 최소화 + 모든 전환에 동일한 easing/duration
- [calm+precise+editorial+trustworthy] color: 중성 톤 위주, accent는 최소한으로 + 정확한 semantic 분리, 모호한 중간 톤 지양 + 타이포그래피로 위계 형성, 컬러보다 weight/size 활용 + 안정적인 neutral 기반, 과한 accent 변화 없음

### 레퍼런스 근거

- **Carbon Design System**: These components can toggle between the AI variant and the default variant depending on the user’s interaction. If the user manually overrides the ...
- **Elastic UI Framework | Elastic UI Framework**: Button Variety of buttons and button groups with different styles and colours Button
- **Workday Canvas Design System**: New AI Ingress Button in Labs AI Ingress Button with open and close CTA will be available in Labs.

### 구현 노트

- 기존에 같은 역할의 컴포넌트가 있으면 토큰 교체부터 시작
- variant prop으로 시각적 변형을 관리 (하드코딩 금지)
- size prop: sm / md / lg (터치 영역은 항상 최소 44px 보장)
- 애니메이션은 상태 설명용으로만 사용, 장식 효과 금지
- 텍스트 위계가 핵심 — 컬러보다 weight/size로 구분

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

- [calm+precise+editorial+trustworthy] color: 중성 톤 위주, accent는 최소한으로 + 정확한 semantic 분리, 모호한 중간 톤 지양 + 타이포그래피로 위계 형성, 컬러보다 weight/size 활용 + 안정적인 neutral 기반, 과한 accent 변화 없음
- [calm+precise+editorial+trustworthy] motion: 150-200ms ease-out, bounce/spring 없음 + 120-180ms, 군더더기 없는 전환 + 콘텐츠 전환 위주, UI chrome 모션 최소화 + 모든 전환에 동일한 easing/duration
- [calm+precise+editorial+trustworthy] density: comfortable 모드 기본, 여유로운 padding + 엄격한 spacing scale 준수, 임의 값 금지 + 넉넉한 line-height와 margin, 읽기 편한 간격 + 기존 레이아웃 유지, 갑작스런 위치 변경 없음

### 레퍼런스 근거

- **Primer**: Design digital marketing experiences with Primer Brand UI Shared Foundations
- **Mozilla Protocol**: Protocol is still an evolving project. Currently it’s used primarily by the Mozilla Marketing Websites team as the front-end for www.mozilla.org . ...
- **Pajamas Design System**: creative agency or vendor collaborating with us on our marketing efforts. partner or customer that is interested in representing our brand on digit...

### 구현 노트

- 기존에 같은 역할의 컴포넌트가 있으면 토큰 교체부터 시작
- variant prop으로 시각적 변형을 관리 (하드코딩 금지)
- 섹션에 <h2 id="...">과 aria-labelledby 필수
- CSS 변수(var(--color-*))를 그대로 쓰고 hex 하드코딩 금지
- 다크 모드는 globals.css의 prefers-color-scheme 블록에 위임
- 애니메이션은 상태 설명용으로만 사용, 장식 효과 금지
- 텍스트 위계가 핵심 — 컬러보다 weight/size로 구분

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

- [calm+precise+editorial+trustworthy] color: 중성 톤 위주, accent는 최소한으로 + 정확한 semantic 분리, 모호한 중간 톤 지양 + 타이포그래피로 위계 형성, 컬러보다 weight/size 활용 + 안정적인 neutral 기반, 과한 accent 변화 없음
- [calm+precise+editorial+trustworthy] motion: 150-200ms ease-out, bounce/spring 없음 + 120-180ms, 군더더기 없는 전환 + 콘텐츠 전환 위주, UI chrome 모션 최소화 + 모든 전환에 동일한 easing/duration
- [calm+precise+editorial+trustworthy] density: comfortable 모드 기본, 여유로운 padding + 엄격한 spacing scale 준수, 임의 값 금지 + 넉넉한 line-height와 margin, 읽기 편한 간격 + 기존 레이아웃 유지, 갑작스런 위치 변경 없음

### 레퍼런스 근거

- **Primer**: Design digital marketing experiences with Primer Brand UI Shared Foundations
- **Mozilla Protocol**: Protocol is still an evolving project. Currently it’s used primarily by the Mozilla Marketing Websites team as the front-end for www.mozilla.org . ...
- **Pajamas Design System**: creative agency or vendor collaborating with us on our marketing efforts. partner or customer that is interested in representing our brand on digit...

### 구현 노트

- 기존에 같은 역할의 컴포넌트가 있으면 토큰 교체부터 시작
- variant prop으로 시각적 변형을 관리 (하드코딩 금지)
- 섹션에 <h2 id="...">과 aria-labelledby 필수
- CSS 변수(var(--color-*))를 그대로 쓰고 hex 하드코딩 금지
- 다크 모드는 globals.css의 prefers-color-scheme 블록에 위임
- 애니메이션은 상태 설명용으로만 사용, 장식 효과 금지
- 텍스트 위계가 핵심 — 컬러보다 weight/size로 구분

---

## marketing / logo-cloud

**역할**: 고객/파트너 로고를 나열하는 영역

**탐지 출처**: social proof

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

- [calm+precise+editorial+trustworthy] color: 중성 톤 위주, accent는 최소한으로 + 정확한 semantic 분리, 모호한 중간 톤 지양 + 타이포그래피로 위계 형성, 컬러보다 weight/size 활용 + 안정적인 neutral 기반, 과한 accent 변화 없음
- [calm+precise+editorial+trustworthy] motion: 150-200ms ease-out, bounce/spring 없음 + 120-180ms, 군더더기 없는 전환 + 콘텐츠 전환 위주, UI chrome 모션 최소화 + 모든 전환에 동일한 easing/duration
- [calm+precise+editorial+trustworthy] density: comfortable 모드 기본, 여유로운 padding + 엄격한 spacing scale 준수, 임의 값 금지 + 넉넉한 line-height와 margin, 읽기 편한 간격 + 기존 레이아웃 유지, 갑작스런 위치 변경 없음

### 레퍼런스 근거

- **Primer**: Design digital marketing experiences with Primer Brand UI Shared Foundations
- **Mozilla Protocol**: Protocol is still an evolving project. Currently it’s used primarily by the Mozilla Marketing Websites team as the front-end for www.mozilla.org . ...
- **Pajamas Design System**: creative agency or vendor collaborating with us on our marketing efforts. partner or customer that is interested in representing our brand on digit...

### 구현 노트

- 기존에 같은 역할의 컴포넌트가 있으면 토큰 교체부터 시작
- variant prop으로 시각적 변형을 관리 (하드코딩 금지)
- 섹션에 <h2 id="...">과 aria-labelledby 필수
- CSS 변수(var(--color-*))를 그대로 쓰고 hex 하드코딩 금지
- 다크 모드는 globals.css의 prefers-color-scheme 블록에 위임
- 애니메이션은 상태 설명용으로만 사용, 장식 효과 금지
- 텍스트 위계가 핵심 — 컬러보다 weight/size로 구분

---

## marketing / customer-logo

**역할**: 개별 고객사 로고 아이템

**탐지 출처**: social proof

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

- [calm+precise+editorial+trustworthy] color: 중성 톤 위주, accent는 최소한으로 + 정확한 semantic 분리, 모호한 중간 톤 지양 + 타이포그래피로 위계 형성, 컬러보다 weight/size 활용 + 안정적인 neutral 기반, 과한 accent 변화 없음
- [calm+precise+editorial+trustworthy] motion: 150-200ms ease-out, bounce/spring 없음 + 120-180ms, 군더더기 없는 전환 + 콘텐츠 전환 위주, UI chrome 모션 최소화 + 모든 전환에 동일한 easing/duration
- [calm+precise+editorial+trustworthy] density: comfortable 모드 기본, 여유로운 padding + 엄격한 spacing scale 준수, 임의 값 금지 + 넉넉한 line-height와 margin, 읽기 편한 간격 + 기존 레이아웃 유지, 갑작스런 위치 변경 없음

### 레퍼런스 근거

- **Primer**: Design digital marketing experiences with Primer Brand UI Shared Foundations
- **Mozilla Protocol**: Protocol is still an evolving project. Currently it’s used primarily by the Mozilla Marketing Websites team as the front-end for www.mozilla.org . ...
- **Pajamas Design System**: creative agency or vendor collaborating with us on our marketing efforts. partner or customer that is interested in representing our brand on digit...

### 구현 노트

- 기존에 같은 역할의 컴포넌트가 있으면 토큰 교체부터 시작
- variant prop으로 시각적 변형을 관리 (하드코딩 금지)
- 섹션에 <h2 id="...">과 aria-labelledby 필수
- CSS 변수(var(--color-*))를 그대로 쓰고 hex 하드코딩 금지
- 다크 모드는 globals.css의 prefers-color-scheme 블록에 위임
- 애니메이션은 상태 설명용으로만 사용, 장식 효과 금지
- 텍스트 위계가 핵심 — 컬러보다 weight/size로 구분

---

## marketing / metric-highlight

**역할**: 주요 지표를 크게 강조하는 숫자 카드

**탐지 출처**: social proof

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

- [calm+precise+editorial+trustworthy] color: 중성 톤 위주, accent는 최소한으로 + 정확한 semantic 분리, 모호한 중간 톤 지양 + 타이포그래피로 위계 형성, 컬러보다 weight/size 활용 + 안정적인 neutral 기반, 과한 accent 변화 없음
- [calm+precise+editorial+trustworthy] motion: 150-200ms ease-out, bounce/spring 없음 + 120-180ms, 군더더기 없는 전환 + 콘텐츠 전환 위주, UI chrome 모션 최소화 + 모든 전환에 동일한 easing/duration
- [calm+precise+editorial+trustworthy] density: comfortable 모드 기본, 여유로운 padding + 엄격한 spacing scale 준수, 임의 값 금지 + 넉넉한 line-height와 margin, 읽기 편한 간격 + 기존 레이아웃 유지, 갑작스런 위치 변경 없음

### 레퍼런스 근거

- **Primer**: Design digital marketing experiences with Primer Brand UI Shared Foundations
- **Mozilla Protocol**: Protocol is still an evolving project. Currently it’s used primarily by the Mozilla Marketing Websites team as the front-end for www.mozilla.org . ...
- **Pajamas Design System**: creative agency or vendor collaborating with us on our marketing efforts. partner or customer that is interested in representing our brand on digit...

### 구현 노트

- 기존에 같은 역할의 컴포넌트가 있으면 토큰 교체부터 시작
- variant prop으로 시각적 변형을 관리 (하드코딩 금지)
- 섹션에 <h2 id="...">과 aria-labelledby 필수
- CSS 변수(var(--color-*))를 그대로 쓰고 hex 하드코딩 금지
- 다크 모드는 globals.css의 prefers-color-scheme 블록에 위임
- 애니메이션은 상태 설명용으로만 사용, 장식 효과 금지
- 텍스트 위계가 핵심 — 컬러보다 weight/size로 구분

---

## marketing / press-quote

**역할**: 언론 인용 또는 어워드 스트립

**탐지 출처**: social proof

**Slot archetype**: `quote-block`

### 구조 (Anatomy)

- blockquote
- quote-text
- attribution

### 상태 (States)

| 상태 | 설명 |
|------|------|
| `default` | 기본 상태 |

### 토큰 바인딩

```
border-left: 2px solid var(--color-border-strong)
padding-left: var(--space-16)
text: var(--color-text)
text-muted: var(--color-text-muted)
font: var(--font-body)
size: var(--text-lg)
line-height: var(--leading-relaxed)
```

### 접근성

- <blockquote>과 <cite> 사용
- 인용부호는 CSS content 또는 장식 SVG로 처리

### 브랜드 적용

- [calm+precise+editorial+trustworthy] color: 중성 톤 위주, accent는 최소한으로 + 정확한 semantic 분리, 모호한 중간 톤 지양 + 타이포그래피로 위계 형성, 컬러보다 weight/size 활용 + 안정적인 neutral 기반, 과한 accent 변화 없음
- [calm+precise+editorial+trustworthy] motion: 150-200ms ease-out, bounce/spring 없음 + 120-180ms, 군더더기 없는 전환 + 콘텐츠 전환 위주, UI chrome 모션 최소화 + 모든 전환에 동일한 easing/duration
- [calm+precise+editorial+trustworthy] density: comfortable 모드 기본, 여유로운 padding + 엄격한 spacing scale 준수, 임의 값 금지 + 넉넉한 line-height와 margin, 읽기 편한 간격 + 기존 레이아웃 유지, 갑작스런 위치 변경 없음

### 레퍼런스 근거

- **Primer**: Design digital marketing experiences with Primer Brand UI Shared Foundations
- **Mozilla Protocol**: Protocol is still an evolving project. Currently it’s used primarily by the Mozilla Marketing Websites team as the front-end for www.mozilla.org . ...
- **Pajamas Design System**: creative agency or vendor collaborating with us on our marketing efforts. partner or customer that is interested in representing our brand on digit...

### 구현 노트

- 기존에 같은 역할의 컴포넌트가 있으면 토큰 교체부터 시작
- variant prop으로 시각적 변형을 관리 (하드코딩 금지)
- 섹션에 <h2 id="...">과 aria-labelledby 필수
- CSS 변수(var(--color-*))를 그대로 쓰고 hex 하드코딩 금지
- 다크 모드는 globals.css의 prefers-color-scheme 블록에 위임
- 애니메이션은 상태 설명용으로만 사용, 장식 효과 금지
- 텍스트 위계가 핵심 — 컬러보다 weight/size로 구분

---

## marketing / cta-section

**역할**: 전환 유도 CTA 섹션 컨테이너

**탐지 출처**: landing cta section

**Slot archetype**: `cta-inverse`

### 구조 (Anatomy)

- section-container
- headline
- supporting-text
- button-group

### 상태 (States)

| 상태 | 설명 |
|------|------|
| `default` | 기본 상태 |

### 토큰 바인딩

```
surface: var(--color-brand-primary)
text: var(--color-text-inverse)
text-supporting: var(--color-surface-tint)
radius: var(--radius-xl)
padding: var(--space-96) var(--space-48)
button-primary-surface: var(--color-surface)
button-primary-text: var(--color-brand-primary)
button-secondary-border: var(--color-text-inverse)
```

### 접근성

- aria-labelledby로 cta-headline id 연결
- primary CTA는 페이지당 1-2개로 제한

### 브랜드 적용

- [calm+precise+editorial+trustworthy] color: 중성 톤 위주, accent는 최소한으로 + 정확한 semantic 분리, 모호한 중간 톤 지양 + 타이포그래피로 위계 형성, 컬러보다 weight/size 활용 + 안정적인 neutral 기반, 과한 accent 변화 없음
- [calm+precise+editorial+trustworthy] motion: 150-200ms ease-out, bounce/spring 없음 + 120-180ms, 군더더기 없는 전환 + 콘텐츠 전환 위주, UI chrome 모션 최소화 + 모든 전환에 동일한 easing/duration
- [calm+precise+editorial+trustworthy] density: comfortable 모드 기본, 여유로운 padding + 엄격한 spacing scale 준수, 임의 값 금지 + 넉넉한 line-height와 margin, 읽기 편한 간격 + 기존 레이아웃 유지, 갑작스런 위치 변경 없음

### 레퍼런스 근거

- **Primer**: Design digital marketing experiences with Primer Brand UI Shared Foundations
- **Mozilla Protocol**: Protocol is still an evolving project. Currently it’s used primarily by the Mozilla Marketing Websites team as the front-end for www.mozilla.org . ...
- **Pajamas Design System**: creative agency or vendor collaborating with us on our marketing efforts. partner or customer that is interested in representing our brand on digit...

### 구현 노트

- 기존에 같은 역할의 컴포넌트가 있으면 토큰 교체부터 시작
- variant prop으로 시각적 변형을 관리 (하드코딩 금지)
- 섹션에 <h2 id="...">과 aria-labelledby 필수
- CSS 변수(var(--color-*))를 그대로 쓰고 hex 하드코딩 금지
- 다크 모드는 globals.css의 prefers-color-scheme 블록에 위임
- 애니메이션은 상태 설명용으로만 사용, 장식 효과 금지
- 텍스트 위계가 핵심 — 컬러보다 weight/size로 구분

---

## marketing / cta-headline

**역할**: 전환을 유도하는 헤드라인

**탐지 출처**: landing cta section

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

- [calm+precise+editorial+trustworthy] color: 중성 톤 위주, accent는 최소한으로 + 정확한 semantic 분리, 모호한 중간 톤 지양 + 타이포그래피로 위계 형성, 컬러보다 weight/size 활용 + 안정적인 neutral 기반, 과한 accent 변화 없음
- [calm+precise+editorial+trustworthy] motion: 150-200ms ease-out, bounce/spring 없음 + 120-180ms, 군더더기 없는 전환 + 콘텐츠 전환 위주, UI chrome 모션 최소화 + 모든 전환에 동일한 easing/duration
- [calm+precise+editorial+trustworthy] density: comfortable 모드 기본, 여유로운 padding + 엄격한 spacing scale 준수, 임의 값 금지 + 넉넉한 line-height와 margin, 읽기 편한 간격 + 기존 레이아웃 유지, 갑작스런 위치 변경 없음

### 레퍼런스 근거

- **Primer**: Design digital marketing experiences with Primer Brand UI Shared Foundations
- **Mozilla Protocol**: Protocol is still an evolving project. Currently it’s used primarily by the Mozilla Marketing Websites team as the front-end for www.mozilla.org . ...
- **Pajamas Design System**: creative agency or vendor collaborating with us on our marketing efforts. partner or customer that is interested in representing our brand on digit...

### 구현 노트

- 기존에 같은 역할의 컴포넌트가 있으면 토큰 교체부터 시작
- variant prop으로 시각적 변형을 관리 (하드코딩 금지)
- 섹션에 <h2 id="...">과 aria-labelledby 필수
- CSS 변수(var(--color-*))를 그대로 쓰고 hex 하드코딩 금지
- 다크 모드는 globals.css의 prefers-color-scheme 블록에 위임
- 애니메이션은 상태 설명용으로만 사용, 장식 효과 금지
- 텍스트 위계가 핵심 — 컬러보다 weight/size로 구분

---

## marketing / cta-supporting-text

**역할**: CTA를 보강하는 서포팅 카피

**탐지 출처**: landing cta section

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

- [calm+precise+editorial+trustworthy] color: 중성 톤 위주, accent는 최소한으로 + 정확한 semantic 분리, 모호한 중간 톤 지양 + 타이포그래피로 위계 형성, 컬러보다 weight/size 활용 + 안정적인 neutral 기반, 과한 accent 변화 없음
- [calm+precise+editorial+trustworthy] motion: 150-200ms ease-out, bounce/spring 없음 + 120-180ms, 군더더기 없는 전환 + 콘텐츠 전환 위주, UI chrome 모션 최소화 + 모든 전환에 동일한 easing/duration
- [calm+precise+editorial+trustworthy] density: comfortable 모드 기본, 여유로운 padding + 엄격한 spacing scale 준수, 임의 값 금지 + 넉넉한 line-height와 margin, 읽기 편한 간격 + 기존 레이아웃 유지, 갑작스런 위치 변경 없음

### 레퍼런스 근거

- **Primer**: Design digital marketing experiences with Primer Brand UI Shared Foundations
- **Mozilla Protocol**: Protocol is still an evolving project. Currently it’s used primarily by the Mozilla Marketing Websites team as the front-end for www.mozilla.org . ...
- **Pajamas Design System**: creative agency or vendor collaborating with us on our marketing efforts. partner or customer that is interested in representing our brand on digit...

### 구현 노트

- 기존에 같은 역할의 컴포넌트가 있으면 토큰 교체부터 시작
- variant prop으로 시각적 변형을 관리 (하드코딩 금지)
- 섹션에 <h2 id="...">과 aria-labelledby 필수
- CSS 변수(var(--color-*))를 그대로 쓰고 hex 하드코딩 금지
- 다크 모드는 globals.css의 prefers-color-scheme 블록에 위임
- 애니메이션은 상태 설명용으로만 사용, 장식 효과 금지
- 텍스트 위계가 핵심 — 컬러보다 weight/size로 구분

---

## button / cta-button-group

**역할**: primary/secondary CTA 묶음

**탐지 출처**: landing cta section

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

- [calm+precise+editorial+trustworthy] hover: opacity 변화 (0.08-0.12), elevation 변화 없음 + 정확한 border/outline 변화 + 텍스트 underline 또는 color shift, 장식적 효과 없음 + 예측 가능하고 일관된 hover 패턴
- [calm+precise+editorial+trustworthy] motion: 150-200ms ease-out, bounce/spring 없음 + 120-180ms, 군더더기 없는 전환 + 콘텐츠 전환 위주, UI chrome 모션 최소화 + 모든 전환에 동일한 easing/duration
- [calm+precise+editorial+trustworthy] color: 중성 톤 위주, accent는 최소한으로 + 정확한 semantic 분리, 모호한 중간 톤 지양 + 타이포그래피로 위계 형성, 컬러보다 weight/size 활용 + 안정적인 neutral 기반, 과한 accent 변화 없음

### 레퍼런스 근거

- **Carbon Design System**: These components can toggle between the AI variant and the default variant depending on the user’s interaction. If the user manually overrides the ...
- **Elastic UI Framework | Elastic UI Framework**: Button Variety of buttons and button groups with different styles and colours Button
- **Workday Canvas Design System**: New AI Ingress Button in Labs AI Ingress Button with open and close CTA will be available in Labs.

### 구현 노트

- 기존에 같은 역할의 컴포넌트가 있으면 토큰 교체부터 시작
- variant prop으로 시각적 변형을 관리 (하드코딩 금지)
- size prop: sm / md / lg (터치 영역은 항상 최소 44px 보장)
- 애니메이션은 상태 설명용으로만 사용, 장식 효과 금지
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

- [calm+precise+editorial+trustworthy] density: comfortable 모드 기본, 여유로운 padding + 엄격한 spacing scale 준수, 임의 값 금지 + 넉넉한 line-height와 margin, 읽기 편한 간격 + 기존 레이아웃 유지, 갑작스런 위치 변경 없음
- [calm+precise+editorial+trustworthy] color: 중성 톤 위주, accent는 최소한으로 + 정확한 semantic 분리, 모호한 중간 톤 지양 + 타이포그래피로 위계 형성, 컬러보다 weight/size 활용 + 안정적인 neutral 기반, 과한 accent 변화 없음

### 레퍼런스 근거

- **Carbon Design System**: Tag Date picker
- **Clarity Design System**: When Clarity customers speak, we listen. One of our most requested components, datagrid, can support more than a dozen features and handle thousand...
- **Cedar Design System | REI Co-op**: Use the HTML aside tag, denoting the section that, though related to the main element, doesn't belong to the main flow 2. Message

### 구현 노트

- 기존에 같은 역할의 컴포넌트가 있으면 토큰 교체부터 시작
- variant prop으로 시각적 변형을 관리 (하드코딩 금지)
- 빈 상태(empty-state)와 에러 상태를 반드시 처리
- 애니메이션은 상태 설명용으로만 사용, 장식 효과 금지
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

- [calm+precise+editorial+trustworthy] feedback: subtle inline alert 선호, 과한 컬러 블록 지양 + 명확한 상태 구분, 진행률/결과를 수치로 표시 + 콘텐츠 맥락 안에서 인라인 표시, 토스트보다 인라인 선호 + 결과를 반드시 확인, 실패 시 복구 방법 안내
- [calm+precise+editorial+trustworthy] motion: 150-200ms ease-out, bounce/spring 없음 + 120-180ms, 군더더기 없는 전환 + 콘텐츠 전환 위주, UI chrome 모션 최소화 + 모든 전환에 동일한 easing/duration
- [calm+precise+editorial+trustworthy] color: 중성 톤 위주, accent는 최소한으로 + 정확한 semantic 분리, 모호한 중간 톤 지양 + 타이포그래피로 위계 형성, 컬러보다 weight/size 활용 + 안정적인 neutral 기반, 과한 accent 변화 없음

### 레퍼런스 근거

- **Atlassian Design**: We finish what we start before starting something new. We're informed by continuous feedback. 3. Bring people on the journey before helping for the...
- **Carbon Design System**: We welcome all feedback, designs, or ideas in order to produce the best possible experience for our users. If you're interested in contributing, ch...
- **Clarity Design System**: Clarity firmly believes that the best products are built by those who form a rich, varied community. We invite all forms of feedback or ideas that ...

### 구현 노트

- 기존에 같은 역할의 컴포넌트가 있으면 토큰 교체부터 시작
- variant prop으로 시각적 변형을 관리 (하드코딩 금지)
- auto-dismiss 시간은 내용 길이에 비례 (기본 5초)
- 애니메이션은 상태 설명용으로만 사용, 장식 효과 금지
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

- [calm+precise+editorial+trustworthy] hover: opacity 변화 (0.08-0.12), elevation 변화 없음 + 정확한 border/outline 변화 + 텍스트 underline 또는 color shift, 장식적 효과 없음 + 예측 가능하고 일관된 hover 패턴
- [calm+precise+editorial+trustworthy] density: comfortable 모드 기본, 여유로운 padding + 엄격한 spacing scale 준수, 임의 값 금지 + 넉넉한 line-height와 margin, 읽기 편한 간격 + 기존 레이아웃 유지, 갑작스런 위치 변경 없음
- [calm+precise+editorial+trustworthy] feedback: subtle inline alert 선호, 과한 컬러 블록 지양 + 명확한 상태 구분, 진행률/결과를 수치로 표시 + 콘텐츠 맥락 안에서 인라인 표시, 토스트보다 인라인 선호 + 결과를 반드시 확인, 실패 시 복구 방법 안내

### 레퍼런스 근거

- **Carbon Design System**: Number input Text input
- **Elastic UI Framework | Elastic UI Framework**: Forms Inputs with validation, grouped into a flexible form layout Forms
- **Thumbprint**: A design system only works when there’s input from a wider team. We encourage contributions both big and small from designers and developers. We’re...

### 구현 노트

- 기존에 같은 역할의 컴포넌트가 있으면 토큰 교체부터 시작
- variant prop으로 시각적 변형을 관리 (하드코딩 금지)
- error 상태에서 helper text → error message로 자동 전환
- label은 항상 visible (placeholder만으로 대체 금지)
- 애니메이션은 상태 설명용으로만 사용, 장식 효과 금지
- 텍스트 위계가 핵심 — 컬러보다 weight/size로 구분

---

## marketing / faq-section

**역할**: FAQ 섹션 컨테이너와 섹션 헤더

**탐지 출처**: faq accordion

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

- [calm+precise+editorial+trustworthy] color: 중성 톤 위주, accent는 최소한으로 + 정확한 semantic 분리, 모호한 중간 톤 지양 + 타이포그래피로 위계 형성, 컬러보다 weight/size 활용 + 안정적인 neutral 기반, 과한 accent 변화 없음
- [calm+precise+editorial+trustworthy] motion: 150-200ms ease-out, bounce/spring 없음 + 120-180ms, 군더더기 없는 전환 + 콘텐츠 전환 위주, UI chrome 모션 최소화 + 모든 전환에 동일한 easing/duration
- [calm+precise+editorial+trustworthy] density: comfortable 모드 기본, 여유로운 padding + 엄격한 spacing scale 준수, 임의 값 금지 + 넉넉한 line-height와 margin, 읽기 편한 간격 + 기존 레이아웃 유지, 갑작스런 위치 변경 없음

### 레퍼런스 근거

- **Primer**: Design digital marketing experiences with Primer Brand UI Shared Foundations
- **Mozilla Protocol**: Protocol is still an evolving project. Currently it’s used primarily by the Mozilla Marketing Websites team as the front-end for www.mozilla.org . ...
- **Pajamas Design System**: creative agency or vendor collaborating with us on our marketing efforts. partner or customer that is interested in representing our brand on digit...

### 구현 노트

- 기존에 같은 역할의 컴포넌트가 있으면 토큰 교체부터 시작
- variant prop으로 시각적 변형을 관리 (하드코딩 금지)
- 섹션에 <h2 id="...">과 aria-labelledby 필수
- CSS 변수(var(--color-*))를 그대로 쓰고 hex 하드코딩 금지
- 다크 모드는 globals.css의 prefers-color-scheme 블록에 위임
- 애니메이션은 상태 설명용으로만 사용, 장식 효과 금지
- 텍스트 위계가 핵심 — 컬러보다 weight/size로 구분

---

## marketing / faq-item

**역할**: 접고 펼 수 있는 개별 FAQ 항목

**탐지 출처**: faq accordion

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

- [calm+precise+editorial+trustworthy] color: 중성 톤 위주, accent는 최소한으로 + 정확한 semantic 분리, 모호한 중간 톤 지양 + 타이포그래피로 위계 형성, 컬러보다 weight/size 활용 + 안정적인 neutral 기반, 과한 accent 변화 없음
- [calm+precise+editorial+trustworthy] motion: 150-200ms ease-out, bounce/spring 없음 + 120-180ms, 군더더기 없는 전환 + 콘텐츠 전환 위주, UI chrome 모션 최소화 + 모든 전환에 동일한 easing/duration
- [calm+precise+editorial+trustworthy] density: comfortable 모드 기본, 여유로운 padding + 엄격한 spacing scale 준수, 임의 값 금지 + 넉넉한 line-height와 margin, 읽기 편한 간격 + 기존 레이아웃 유지, 갑작스런 위치 변경 없음

### 레퍼런스 근거

- **Primer**: Design digital marketing experiences with Primer Brand UI Shared Foundations
- **Mozilla Protocol**: Protocol is still an evolving project. Currently it’s used primarily by the Mozilla Marketing Websites team as the front-end for www.mozilla.org . ...
- **Pajamas Design System**: creative agency or vendor collaborating with us on our marketing efforts. partner or customer that is interested in representing our brand on digit...

### 구현 노트

- 기존에 같은 역할의 컴포넌트가 있으면 토큰 교체부터 시작
- variant prop으로 시각적 변형을 관리 (하드코딩 금지)
- 섹션에 <h2 id="...">과 aria-labelledby 필수
- CSS 변수(var(--color-*))를 그대로 쓰고 hex 하드코딩 금지
- 다크 모드는 globals.css의 prefers-color-scheme 블록에 위임
- 애니메이션은 상태 설명용으로만 사용, 장식 효과 금지
- 텍스트 위계가 핵심 — 컬러보다 weight/size로 구분

---

## marketing / faq-question

**역할**: FAQ 질문 헤더 (클릭 가능한 트리거)

**탐지 출처**: faq accordion

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

- [calm+precise+editorial+trustworthy] color: 중성 톤 위주, accent는 최소한으로 + 정확한 semantic 분리, 모호한 중간 톤 지양 + 타이포그래피로 위계 형성, 컬러보다 weight/size 활용 + 안정적인 neutral 기반, 과한 accent 변화 없음
- [calm+precise+editorial+trustworthy] motion: 150-200ms ease-out, bounce/spring 없음 + 120-180ms, 군더더기 없는 전환 + 콘텐츠 전환 위주, UI chrome 모션 최소화 + 모든 전환에 동일한 easing/duration
- [calm+precise+editorial+trustworthy] density: comfortable 모드 기본, 여유로운 padding + 엄격한 spacing scale 준수, 임의 값 금지 + 넉넉한 line-height와 margin, 읽기 편한 간격 + 기존 레이아웃 유지, 갑작스런 위치 변경 없음

### 레퍼런스 근거

- **Primer**: Design digital marketing experiences with Primer Brand UI Shared Foundations
- **Mozilla Protocol**: Protocol is still an evolving project. Currently it’s used primarily by the Mozilla Marketing Websites team as the front-end for www.mozilla.org . ...
- **Pajamas Design System**: creative agency or vendor collaborating with us on our marketing efforts. partner or customer that is interested in representing our brand on digit...

### 구현 노트

- 기존에 같은 역할의 컴포넌트가 있으면 토큰 교체부터 시작
- variant prop으로 시각적 변형을 관리 (하드코딩 금지)
- 섹션에 <h2 id="...">과 aria-labelledby 필수
- CSS 변수(var(--color-*))를 그대로 쓰고 hex 하드코딩 금지
- 다크 모드는 globals.css의 prefers-color-scheme 블록에 위임
- 애니메이션은 상태 설명용으로만 사용, 장식 효과 금지
- 텍스트 위계가 핵심 — 컬러보다 weight/size로 구분

---

## marketing / faq-answer

**역할**: FAQ 답변 본문

**탐지 출처**: faq accordion

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

- [calm+precise+editorial+trustworthy] color: 중성 톤 위주, accent는 최소한으로 + 정확한 semantic 분리, 모호한 중간 톤 지양 + 타이포그래피로 위계 형성, 컬러보다 weight/size 활용 + 안정적인 neutral 기반, 과한 accent 변화 없음
- [calm+precise+editorial+trustworthy] motion: 150-200ms ease-out, bounce/spring 없음 + 120-180ms, 군더더기 없는 전환 + 콘텐츠 전환 위주, UI chrome 모션 최소화 + 모든 전환에 동일한 easing/duration
- [calm+precise+editorial+trustworthy] density: comfortable 모드 기본, 여유로운 padding + 엄격한 spacing scale 준수, 임의 값 금지 + 넉넉한 line-height와 margin, 읽기 편한 간격 + 기존 레이아웃 유지, 갑작스런 위치 변경 없음

### 레퍼런스 근거

- **Primer**: Design digital marketing experiences with Primer Brand UI Shared Foundations
- **Mozilla Protocol**: Protocol is still an evolving project. Currently it’s used primarily by the Mozilla Marketing Websites team as the front-end for www.mozilla.org . ...
- **Pajamas Design System**: creative agency or vendor collaborating with us on our marketing efforts. partner or customer that is interested in representing our brand on digit...

### 구현 노트

- 기존에 같은 역할의 컴포넌트가 있으면 토큰 교체부터 시작
- variant prop으로 시각적 변형을 관리 (하드코딩 금지)
- 섹션에 <h2 id="...">과 aria-labelledby 필수
- CSS 변수(var(--color-*))를 그대로 쓰고 hex 하드코딩 금지
- 다크 모드는 globals.css의 prefers-color-scheme 블록에 위임
- 애니메이션은 상태 설명용으로만 사용, 장식 효과 금지
- 텍스트 위계가 핵심 — 컬러보다 weight/size로 구분

---

## marketing / site-footer

**역할**: 사이트 전역 하단 컨테이너

**탐지 출처**: site footer

**Slot archetype**: `footer-bar`

### 구조 (Anatomy)

- container
- column-grid
- legal-strip
- social-strip

### 상태 (States)

| 상태 | 설명 |
|------|------|
| `default` | 기본 상태 |

### 토큰 바인딩

```
surface: var(--color-surface-muted)
border-top: var(--color-border)
padding: var(--space-64) var(--space-24) var(--space-32)
column-gap: var(--space-48)
inner-max-width: 1120px
text: var(--color-text-muted)
```

### 접근성

- <footer role="contentinfo">
- 링크 그룹에 의미 있는 heading 제공

### 브랜드 적용

- [calm+precise+editorial+trustworthy] color: 중성 톤 위주, accent는 최소한으로 + 정확한 semantic 분리, 모호한 중간 톤 지양 + 타이포그래피로 위계 형성, 컬러보다 weight/size 활용 + 안정적인 neutral 기반, 과한 accent 변화 없음
- [calm+precise+editorial+trustworthy] motion: 150-200ms ease-out, bounce/spring 없음 + 120-180ms, 군더더기 없는 전환 + 콘텐츠 전환 위주, UI chrome 모션 최소화 + 모든 전환에 동일한 easing/duration
- [calm+precise+editorial+trustworthy] density: comfortable 모드 기본, 여유로운 padding + 엄격한 spacing scale 준수, 임의 값 금지 + 넉넉한 line-height와 margin, 읽기 편한 간격 + 기존 레이아웃 유지, 갑작스런 위치 변경 없음

### 레퍼런스 근거

- **Primer**: Design digital marketing experiences with Primer Brand UI Shared Foundations
- **Mozilla Protocol**: Protocol is still an evolving project. Currently it’s used primarily by the Mozilla Marketing Websites team as the front-end for www.mozilla.org . ...
- **Pajamas Design System**: creative agency or vendor collaborating with us on our marketing efforts. partner or customer that is interested in representing our brand on digit...

### 구현 노트

- 기존에 같은 역할의 컴포넌트가 있으면 토큰 교체부터 시작
- variant prop으로 시각적 변형을 관리 (하드코딩 금지)
- 섹션에 <h2 id="...">과 aria-labelledby 필수
- CSS 변수(var(--color-*))를 그대로 쓰고 hex 하드코딩 금지
- 다크 모드는 globals.css의 prefers-color-scheme 블록에 위임
- 애니메이션은 상태 설명용으로만 사용, 장식 효과 금지
- 텍스트 위계가 핵심 — 컬러보다 weight/size로 구분

---

## marketing / footer-column

**역할**: 링크 그룹을 담는 세로 컬럼

**탐지 출처**: site footer

**Slot archetype**: `footer-bar`

### 구조 (Anatomy)

- container
- column-grid
- legal-strip
- social-strip

### 상태 (States)

| 상태 | 설명 |
|------|------|
| `default` | 기본 상태 |

### 토큰 바인딩

```
surface: var(--color-surface-muted)
border-top: var(--color-border)
padding: var(--space-64) var(--space-24) var(--space-32)
column-gap: var(--space-48)
inner-max-width: 1120px
text: var(--color-text-muted)
```

### 접근성

- <footer role="contentinfo">
- 링크 그룹에 의미 있는 heading 제공

### 브랜드 적용

- [calm+precise+editorial+trustworthy] color: 중성 톤 위주, accent는 최소한으로 + 정확한 semantic 분리, 모호한 중간 톤 지양 + 타이포그래피로 위계 형성, 컬러보다 weight/size 활용 + 안정적인 neutral 기반, 과한 accent 변화 없음
- [calm+precise+editorial+trustworthy] motion: 150-200ms ease-out, bounce/spring 없음 + 120-180ms, 군더더기 없는 전환 + 콘텐츠 전환 위주, UI chrome 모션 최소화 + 모든 전환에 동일한 easing/duration
- [calm+precise+editorial+trustworthy] density: comfortable 모드 기본, 여유로운 padding + 엄격한 spacing scale 준수, 임의 값 금지 + 넉넉한 line-height와 margin, 읽기 편한 간격 + 기존 레이아웃 유지, 갑작스런 위치 변경 없음

### 레퍼런스 근거

- **Primer**: Design digital marketing experiences with Primer Brand UI Shared Foundations
- **Mozilla Protocol**: Protocol is still an evolving project. Currently it’s used primarily by the Mozilla Marketing Websites team as the front-end for www.mozilla.org . ...
- **Pajamas Design System**: creative agency or vendor collaborating with us on our marketing efforts. partner or customer that is interested in representing our brand on digit...

### 구현 노트

- 기존에 같은 역할의 컴포넌트가 있으면 토큰 교체부터 시작
- variant prop으로 시각적 변형을 관리 (하드코딩 금지)
- 섹션에 <h2 id="...">과 aria-labelledby 필수
- CSS 변수(var(--color-*))를 그대로 쓰고 hex 하드코딩 금지
- 다크 모드는 globals.css의 prefers-color-scheme 블록에 위임
- 애니메이션은 상태 설명용으로만 사용, 장식 효과 금지
- 텍스트 위계가 핵심 — 컬러보다 weight/size로 구분

---

## marketing / footer-link

**역할**: 푸터 내 개별 링크

**탐지 출처**: site footer

**Slot archetype**: `link`

### 구조 (Anatomy)

- anchor

### 상태 (States)

| 상태 | 설명 |
|------|------|
| `default` | 기본 상태 |
| `hover` | 마우스 오버 시 |
| `focus-visible` | focus-visible |
| `visited` | visited |

### 토큰 바인딩

```
color: var(--color-text-muted)
color-hover: var(--color-text)
underline-hover: 1px solid currentColor
motion: color var(--duration-120) var(--ease-standard)
```

### 접근성

- 의미 있는 링크 텍스트 ("여기 클릭" 금지)
- 외부 링크는 aria-label에 명시
- focus ring은 전역 :focus-visible 규칙 사용

### 브랜드 적용

- [calm+precise+editorial+trustworthy] color: 중성 톤 위주, accent는 최소한으로 + 정확한 semantic 분리, 모호한 중간 톤 지양 + 타이포그래피로 위계 형성, 컬러보다 weight/size 활용 + 안정적인 neutral 기반, 과한 accent 변화 없음
- [calm+precise+editorial+trustworthy] motion: 150-200ms ease-out, bounce/spring 없음 + 120-180ms, 군더더기 없는 전환 + 콘텐츠 전환 위주, UI chrome 모션 최소화 + 모든 전환에 동일한 easing/duration
- [calm+precise+editorial+trustworthy] density: comfortable 모드 기본, 여유로운 padding + 엄격한 spacing scale 준수, 임의 값 금지 + 넉넉한 line-height와 margin, 읽기 편한 간격 + 기존 레이아웃 유지, 갑작스런 위치 변경 없음

### 레퍼런스 근거

- **Primer**: Design digital marketing experiences with Primer Brand UI Shared Foundations
- **Mozilla Protocol**: Protocol is still an evolving project. Currently it’s used primarily by the Mozilla Marketing Websites team as the front-end for www.mozilla.org . ...
- **Pajamas Design System**: creative agency or vendor collaborating with us on our marketing efforts. partner or customer that is interested in representing our brand on digit...

### 구현 노트

- 기존에 같은 역할의 컴포넌트가 있으면 토큰 교체부터 시작
- variant prop으로 시각적 변형을 관리 (하드코딩 금지)
- 섹션에 <h2 id="...">과 aria-labelledby 필수
- CSS 변수(var(--color-*))를 그대로 쓰고 hex 하드코딩 금지
- 다크 모드는 globals.css의 prefers-color-scheme 블록에 위임
- 애니메이션은 상태 설명용으로만 사용, 장식 효과 금지
- 텍스트 위계가 핵심 — 컬러보다 weight/size로 구분

---

## marketing / footer-legal

**역할**: 저작권·법적 고지 영역

**탐지 출처**: site footer

**Slot archetype**: `footer-bar`

### 구조 (Anatomy)

- container
- column-grid
- legal-strip
- social-strip

### 상태 (States)

| 상태 | 설명 |
|------|------|
| `default` | 기본 상태 |

### 토큰 바인딩

```
surface: var(--color-surface-muted)
border-top: var(--color-border)
padding: var(--space-64) var(--space-24) var(--space-32)
column-gap: var(--space-48)
inner-max-width: 1120px
text: var(--color-text-muted)
```

### 접근성

- <footer role="contentinfo">
- 링크 그룹에 의미 있는 heading 제공

### 브랜드 적용

- [calm+precise+editorial+trustworthy] color: 중성 톤 위주, accent는 최소한으로 + 정확한 semantic 분리, 모호한 중간 톤 지양 + 타이포그래피로 위계 형성, 컬러보다 weight/size 활용 + 안정적인 neutral 기반, 과한 accent 변화 없음
- [calm+precise+editorial+trustworthy] motion: 150-200ms ease-out, bounce/spring 없음 + 120-180ms, 군더더기 없는 전환 + 콘텐츠 전환 위주, UI chrome 모션 최소화 + 모든 전환에 동일한 easing/duration
- [calm+precise+editorial+trustworthy] density: comfortable 모드 기본, 여유로운 padding + 엄격한 spacing scale 준수, 임의 값 금지 + 넉넉한 line-height와 margin, 읽기 편한 간격 + 기존 레이아웃 유지, 갑작스런 위치 변경 없음

### 레퍼런스 근거

- **Primer**: Design digital marketing experiences with Primer Brand UI Shared Foundations
- **Mozilla Protocol**: Protocol is still an evolving project. Currently it’s used primarily by the Mozilla Marketing Websites team as the front-end for www.mozilla.org . ...
- **Pajamas Design System**: creative agency or vendor collaborating with us on our marketing efforts. partner or customer that is interested in representing our brand on digit...

### 구현 노트

- 기존에 같은 역할의 컴포넌트가 있으면 토큰 교체부터 시작
- variant prop으로 시각적 변형을 관리 (하드코딩 금지)
- 섹션에 <h2 id="...">과 aria-labelledby 필수
- CSS 변수(var(--color-*))를 그대로 쓰고 hex 하드코딩 금지
- 다크 모드는 globals.css의 prefers-color-scheme 블록에 위임
- 애니메이션은 상태 설명용으로만 사용, 장식 효과 금지
- 텍스트 위계가 핵심 — 컬러보다 weight/size로 구분

---

## marketing / footer-social

**역할**: 소셜 링크 아이콘 그룹

**탐지 출처**: site footer

**Slot archetype**: `footer-bar`

### 구조 (Anatomy)

- container
- column-grid
- legal-strip
- social-strip

### 상태 (States)

| 상태 | 설명 |
|------|------|
| `default` | 기본 상태 |

### 토큰 바인딩

```
surface: var(--color-surface-muted)
border-top: var(--color-border)
padding: var(--space-64) var(--space-24) var(--space-32)
column-gap: var(--space-48)
inner-max-width: 1120px
text: var(--color-text-muted)
```

### 접근성

- <footer role="contentinfo">
- 링크 그룹에 의미 있는 heading 제공

### 브랜드 적용

- [calm+precise+editorial+trustworthy] color: 중성 톤 위주, accent는 최소한으로 + 정확한 semantic 분리, 모호한 중간 톤 지양 + 타이포그래피로 위계 형성, 컬러보다 weight/size 활용 + 안정적인 neutral 기반, 과한 accent 변화 없음
- [calm+precise+editorial+trustworthy] motion: 150-200ms ease-out, bounce/spring 없음 + 120-180ms, 군더더기 없는 전환 + 콘텐츠 전환 위주, UI chrome 모션 최소화 + 모든 전환에 동일한 easing/duration
- [calm+precise+editorial+trustworthy] density: comfortable 모드 기본, 여유로운 padding + 엄격한 spacing scale 준수, 임의 값 금지 + 넉넉한 line-height와 margin, 읽기 편한 간격 + 기존 레이아웃 유지, 갑작스런 위치 변경 없음

### 레퍼런스 근거

- **Primer**: Design digital marketing experiences with Primer Brand UI Shared Foundations
- **Mozilla Protocol**: Protocol is still an evolving project. Currently it’s used primarily by the Mozilla Marketing Websites team as the front-end for www.mozilla.org . ...
- **Pajamas Design System**: creative agency or vendor collaborating with us on our marketing efforts. partner or customer that is interested in representing our brand on digit...

### 구현 노트

- 기존에 같은 역할의 컴포넌트가 있으면 토큰 교체부터 시작
- variant prop으로 시각적 변형을 관리 (하드코딩 금지)
- 섹션에 <h2 id="...">과 aria-labelledby 필수
- CSS 변수(var(--color-*))를 그대로 쓰고 hex 하드코딩 금지
- 다크 모드는 globals.css의 prefers-color-scheme 블록에 위임
- 애니메이션은 상태 설명용으로만 사용, 장식 효과 금지
- 텍스트 위계가 핵심 — 컬러보다 weight/size로 구분

---

## input / upload-dropzone

**역할**: 드래그앤드롭 파일 업로드 영역

**탐지 출처**: file upload

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

- [calm+precise+editorial+trustworthy] hover: opacity 변화 (0.08-0.12), elevation 변화 없음 + 정확한 border/outline 변화 + 텍스트 underline 또는 color shift, 장식적 효과 없음 + 예측 가능하고 일관된 hover 패턴
- [calm+precise+editorial+trustworthy] density: comfortable 모드 기본, 여유로운 padding + 엄격한 spacing scale 준수, 임의 값 금지 + 넉넉한 line-height와 margin, 읽기 편한 간격 + 기존 레이아웃 유지, 갑작스런 위치 변경 없음
- [calm+precise+editorial+trustworthy] feedback: subtle inline alert 선호, 과한 컬러 블록 지양 + 명확한 상태 구분, 진행률/결과를 수치로 표시 + 콘텐츠 맥락 안에서 인라인 표시, 토스트보다 인라인 선호 + 결과를 반드시 확인, 실패 시 복구 방법 안내

### 레퍼런스 근거

- **Carbon Design System**: Number input Text input
- **Elastic UI Framework | Elastic UI Framework**: Forms Inputs with validation, grouped into a flexible form layout Forms
- **Thumbprint**: A design system only works when there’s input from a wider team. We encourage contributions both big and small from designers and developers. We’re...

### 구현 노트

- 기존에 같은 역할의 컴포넌트가 있으면 토큰 교체부터 시작
- variant prop으로 시각적 변형을 관리 (하드코딩 금지)
- error 상태에서 helper text → error message로 자동 전환
- label은 항상 visible (placeholder만으로 대체 금지)
- 애니메이션은 상태 설명용으로만 사용, 장식 효과 금지
- 텍스트 위계가 핵심 — 컬러보다 weight/size로 구분

---

## data-display / file-preview

**역할**: 업로드된 파일 미리보기

**탐지 출처**: file upload

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

- [calm+precise+editorial+trustworthy] density: comfortable 모드 기본, 여유로운 padding + 엄격한 spacing scale 준수, 임의 값 금지 + 넉넉한 line-height와 margin, 읽기 편한 간격 + 기존 레이아웃 유지, 갑작스런 위치 변경 없음
- [calm+precise+editorial+trustworthy] color: 중성 톤 위주, accent는 최소한으로 + 정확한 semantic 분리, 모호한 중간 톤 지양 + 타이포그래피로 위계 형성, 컬러보다 weight/size 활용 + 안정적인 neutral 기반, 과한 accent 변화 없음

### 구현 노트

- 기존에 같은 역할의 컴포넌트가 있으면 토큰 교체부터 시작
- variant prop으로 시각적 변형을 관리 (하드코딩 금지)
- 빈 상태(empty-state)와 에러 상태를 반드시 처리
- 애니메이션은 상태 설명용으로만 사용, 장식 효과 금지
- 텍스트 위계가 핵심 — 컬러보다 weight/size로 구분

---

## feedback / upload-progress

**역할**: 업로드 진행률 표시

**탐지 출처**: file upload

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

- [calm+precise+editorial+trustworthy] feedback: subtle inline alert 선호, 과한 컬러 블록 지양 + 명확한 상태 구분, 진행률/결과를 수치로 표시 + 콘텐츠 맥락 안에서 인라인 표시, 토스트보다 인라인 선호 + 결과를 반드시 확인, 실패 시 복구 방법 안내
- [calm+precise+editorial+trustworthy] motion: 150-200ms ease-out, bounce/spring 없음 + 120-180ms, 군더더기 없는 전환 + 콘텐츠 전환 위주, UI chrome 모션 최소화 + 모든 전환에 동일한 easing/duration
- [calm+precise+editorial+trustworthy] color: 중성 톤 위주, accent는 최소한으로 + 정확한 semantic 분리, 모호한 중간 톤 지양 + 타이포그래피로 위계 형성, 컬러보다 weight/size 활용 + 안정적인 neutral 기반, 과한 accent 변화 없음

### 레퍼런스 근거

- **Atlassian Design**: We finish what we start before starting something new. We're informed by continuous feedback. 3. Bring people on the journey before helping for the...
- **Carbon Design System**: We welcome all feedback, designs, or ideas in order to produce the best possible experience for our users. If you're interested in contributing, ch...
- **Clarity Design System**: Clarity firmly believes that the best products are built by those who form a rich, varied community. We invite all forms of feedback or ideas that ...

### 구현 노트

- 기존에 같은 역할의 컴포넌트가 있으면 토큰 교체부터 시작
- variant prop으로 시각적 변형을 관리 (하드코딩 금지)
- auto-dismiss 시간은 내용 길이에 비례 (기본 5초)
- 애니메이션은 상태 설명용으로만 사용, 장식 효과 금지
- 텍스트 위계가 핵심 — 컬러보다 weight/size로 구분

---

## marketing / testimonial-section

**역할**: 추천사 섹션 컨테이너

**탐지 출처**: testimonial

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

- [calm+precise+editorial+trustworthy] color: 중성 톤 위주, accent는 최소한으로 + 정확한 semantic 분리, 모호한 중간 톤 지양 + 타이포그래피로 위계 형성, 컬러보다 weight/size 활용 + 안정적인 neutral 기반, 과한 accent 변화 없음
- [calm+precise+editorial+trustworthy] motion: 150-200ms ease-out, bounce/spring 없음 + 120-180ms, 군더더기 없는 전환 + 콘텐츠 전환 위주, UI chrome 모션 최소화 + 모든 전환에 동일한 easing/duration
- [calm+precise+editorial+trustworthy] density: comfortable 모드 기본, 여유로운 padding + 엄격한 spacing scale 준수, 임의 값 금지 + 넉넉한 line-height와 margin, 읽기 편한 간격 + 기존 레이아웃 유지, 갑작스런 위치 변경 없음

### 레퍼런스 근거

- **Primer**: Design digital marketing experiences with Primer Brand UI Shared Foundations
- **Mozilla Protocol**: Protocol is still an evolving project. Currently it’s used primarily by the Mozilla Marketing Websites team as the front-end for www.mozilla.org . ...
- **Pajamas Design System**: creative agency or vendor collaborating with us on our marketing efforts. partner or customer that is interested in representing our brand on digit...

### 구현 노트

- 기존에 같은 역할의 컴포넌트가 있으면 토큰 교체부터 시작
- variant prop으로 시각적 변형을 관리 (하드코딩 금지)
- 섹션에 <h2 id="...">과 aria-labelledby 필수
- CSS 변수(var(--color-*))를 그대로 쓰고 hex 하드코딩 금지
- 다크 모드는 globals.css의 prefers-color-scheme 블록에 위임
- 애니메이션은 상태 설명용으로만 사용, 장식 효과 금지
- 텍스트 위계가 핵심 — 컬러보다 weight/size로 구분

---

## marketing / testimonial-card

**역할**: 고객 인용을 담는 카드

**탐지 출처**: testimonial

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

- [calm+precise+editorial+trustworthy] color: 중성 톤 위주, accent는 최소한으로 + 정확한 semantic 분리, 모호한 중간 톤 지양 + 타이포그래피로 위계 형성, 컬러보다 weight/size 활용 + 안정적인 neutral 기반, 과한 accent 변화 없음
- [calm+precise+editorial+trustworthy] motion: 150-200ms ease-out, bounce/spring 없음 + 120-180ms, 군더더기 없는 전환 + 콘텐츠 전환 위주, UI chrome 모션 최소화 + 모든 전환에 동일한 easing/duration
- [calm+precise+editorial+trustworthy] density: comfortable 모드 기본, 여유로운 padding + 엄격한 spacing scale 준수, 임의 값 금지 + 넉넉한 line-height와 margin, 읽기 편한 간격 + 기존 레이아웃 유지, 갑작스런 위치 변경 없음

### 레퍼런스 근거

- **Primer**: Design digital marketing experiences with Primer Brand UI Shared Foundations
- **Mozilla Protocol**: Protocol is still an evolving project. Currently it’s used primarily by the Mozilla Marketing Websites team as the front-end for www.mozilla.org . ...
- **Pajamas Design System**: creative agency or vendor collaborating with us on our marketing efforts. partner or customer that is interested in representing our brand on digit...

### 구현 노트

- 기존에 같은 역할의 컴포넌트가 있으면 토큰 교체부터 시작
- variant prop으로 시각적 변형을 관리 (하드코딩 금지)
- 섹션에 <h2 id="...">과 aria-labelledby 필수
- CSS 변수(var(--color-*))를 그대로 쓰고 hex 하드코딩 금지
- 다크 모드는 globals.css의 prefers-color-scheme 블록에 위임
- 애니메이션은 상태 설명용으로만 사용, 장식 효과 금지
- 텍스트 위계가 핵심 — 컬러보다 weight/size로 구분

---

## marketing / testimonial-quote

**역할**: 추천사 본문 텍스트

**탐지 출처**: testimonial

**Slot archetype**: `quote-block`

### 구조 (Anatomy)

- blockquote
- quote-text
- attribution

### 상태 (States)

| 상태 | 설명 |
|------|------|
| `default` | 기본 상태 |

### 토큰 바인딩

```
border-left: 2px solid var(--color-border-strong)
padding-left: var(--space-16)
text: var(--color-text)
text-muted: var(--color-text-muted)
font: var(--font-body)
size: var(--text-lg)
line-height: var(--leading-relaxed)
```

### 접근성

- <blockquote>과 <cite> 사용
- 인용부호는 CSS content 또는 장식 SVG로 처리

### 브랜드 적용

- [calm+precise+editorial+trustworthy] color: 중성 톤 위주, accent는 최소한으로 + 정확한 semantic 분리, 모호한 중간 톤 지양 + 타이포그래피로 위계 형성, 컬러보다 weight/size 활용 + 안정적인 neutral 기반, 과한 accent 변화 없음
- [calm+precise+editorial+trustworthy] motion: 150-200ms ease-out, bounce/spring 없음 + 120-180ms, 군더더기 없는 전환 + 콘텐츠 전환 위주, UI chrome 모션 최소화 + 모든 전환에 동일한 easing/duration
- [calm+precise+editorial+trustworthy] density: comfortable 모드 기본, 여유로운 padding + 엄격한 spacing scale 준수, 임의 값 금지 + 넉넉한 line-height와 margin, 읽기 편한 간격 + 기존 레이아웃 유지, 갑작스런 위치 변경 없음

### 레퍼런스 근거

- **Primer**: Design digital marketing experiences with Primer Brand UI Shared Foundations
- **Mozilla Protocol**: Protocol is still an evolving project. Currently it’s used primarily by the Mozilla Marketing Websites team as the front-end for www.mozilla.org . ...
- **Pajamas Design System**: creative agency or vendor collaborating with us on our marketing efforts. partner or customer that is interested in representing our brand on digit...

### 구현 노트

- 기존에 같은 역할의 컴포넌트가 있으면 토큰 교체부터 시작
- variant prop으로 시각적 변형을 관리 (하드코딩 금지)
- 섹션에 <h2 id="...">과 aria-labelledby 필수
- CSS 변수(var(--color-*))를 그대로 쓰고 hex 하드코딩 금지
- 다크 모드는 globals.css의 prefers-color-scheme 블록에 위임
- 애니메이션은 상태 설명용으로만 사용, 장식 효과 금지
- 텍스트 위계가 핵심 — 컬러보다 weight/size로 구분

---

## marketing / testimonial-author

**역할**: 추천사 작성자 정보 (이름/직책/회사)

**탐지 출처**: testimonial

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

- [calm+precise+editorial+trustworthy] color: 중성 톤 위주, accent는 최소한으로 + 정확한 semantic 분리, 모호한 중간 톤 지양 + 타이포그래피로 위계 형성, 컬러보다 weight/size 활용 + 안정적인 neutral 기반, 과한 accent 변화 없음
- [calm+precise+editorial+trustworthy] motion: 150-200ms ease-out, bounce/spring 없음 + 120-180ms, 군더더기 없는 전환 + 콘텐츠 전환 위주, UI chrome 모션 최소화 + 모든 전환에 동일한 easing/duration
- [calm+precise+editorial+trustworthy] density: comfortable 모드 기본, 여유로운 padding + 엄격한 spacing scale 준수, 임의 값 금지 + 넉넉한 line-height와 margin, 읽기 편한 간격 + 기존 레이아웃 유지, 갑작스런 위치 변경 없음

### 레퍼런스 근거

- **Primer**: Design digital marketing experiences with Primer Brand UI Shared Foundations
- **Mozilla Protocol**: Protocol is still an evolving project. Currently it’s used primarily by the Mozilla Marketing Websites team as the front-end for www.mozilla.org . ...
- **Pajamas Design System**: creative agency or vendor collaborating with us on our marketing efforts. partner or customer that is interested in representing our brand on digit...

### 구현 노트

- 기존에 같은 역할의 컴포넌트가 있으면 토큰 교체부터 시작
- variant prop으로 시각적 변형을 관리 (하드코딩 금지)
- 섹션에 <h2 id="...">과 aria-labelledby 필수
- CSS 변수(var(--color-*))를 그대로 쓰고 hex 하드코딩 금지
- 다크 모드는 globals.css의 prefers-color-scheme 블록에 위임
- 애니메이션은 상태 설명용으로만 사용, 장식 효과 금지
- 텍스트 위계가 핵심 — 컬러보다 weight/size로 구분

---

## marketing / site-header

**역할**: 랜딩 상단 고정 헤더

**탐지 출처**: site header

**Slot archetype**: `nav-bar`

### 구조 (Anatomy)

- sticky-container
- inner-max-width
- left-group
- right-group

### 상태 (States)

| 상태 | 설명 |
|------|------|
| `default` | 기본 상태 |
| `scrolled` | scrolled |

### 토큰 바인딩

```
surface: var(--color-surface)
border-bottom: var(--color-border)
height: 64px
padding: 0 var(--space-24)
inner-max-width: 1120px
z-index: 50
backdrop-filter: blur(8px)
```

### 접근성

- <header role="banner"> 또는 <nav aria-label="Primary">
- 키보드 탐색 시 논리적 탭 순서 유지
- 랜드마크가 중복되지 않도록 main 이외 영역에만 배치

### 브랜드 적용

- [calm+precise+editorial+trustworthy] color: 중성 톤 위주, accent는 최소한으로 + 정확한 semantic 분리, 모호한 중간 톤 지양 + 타이포그래피로 위계 형성, 컬러보다 weight/size 활용 + 안정적인 neutral 기반, 과한 accent 변화 없음
- [calm+precise+editorial+trustworthy] motion: 150-200ms ease-out, bounce/spring 없음 + 120-180ms, 군더더기 없는 전환 + 콘텐츠 전환 위주, UI chrome 모션 최소화 + 모든 전환에 동일한 easing/duration
- [calm+precise+editorial+trustworthy] density: comfortable 모드 기본, 여유로운 padding + 엄격한 spacing scale 준수, 임의 값 금지 + 넉넉한 line-height와 margin, 읽기 편한 간격 + 기존 레이아웃 유지, 갑작스런 위치 변경 없음

### 레퍼런스 근거

- **Primer**: Design digital marketing experiences with Primer Brand UI Shared Foundations
- **Mozilla Protocol**: Protocol is still an evolving project. Currently it’s used primarily by the Mozilla Marketing Websites team as the front-end for www.mozilla.org . ...
- **Pajamas Design System**: creative agency or vendor collaborating with us on our marketing efforts. partner or customer that is interested in representing our brand on digit...

### 구현 노트

- 기존에 같은 역할의 컴포넌트가 있으면 토큰 교체부터 시작
- variant prop으로 시각적 변형을 관리 (하드코딩 금지)
- 섹션에 <h2 id="...">과 aria-labelledby 필수
- CSS 변수(var(--color-*))를 그대로 쓰고 hex 하드코딩 금지
- 다크 모드는 globals.css의 prefers-color-scheme 블록에 위임
- 애니메이션은 상태 설명용으로만 사용, 장식 효과 금지
- 텍스트 위계가 핵심 — 컬러보다 weight/size로 구분

---

## marketing / site-logo

**역할**: 브랜드 로고 영역

**탐지 출처**: site header

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

- [calm+precise+editorial+trustworthy] color: 중성 톤 위주, accent는 최소한으로 + 정확한 semantic 분리, 모호한 중간 톤 지양 + 타이포그래피로 위계 형성, 컬러보다 weight/size 활용 + 안정적인 neutral 기반, 과한 accent 변화 없음
- [calm+precise+editorial+trustworthy] motion: 150-200ms ease-out, bounce/spring 없음 + 120-180ms, 군더더기 없는 전환 + 콘텐츠 전환 위주, UI chrome 모션 최소화 + 모든 전환에 동일한 easing/duration
- [calm+precise+editorial+trustworthy] density: comfortable 모드 기본, 여유로운 padding + 엄격한 spacing scale 준수, 임의 값 금지 + 넉넉한 line-height와 margin, 읽기 편한 간격 + 기존 레이아웃 유지, 갑작스런 위치 변경 없음

### 레퍼런스 근거

- **Primer**: Design digital marketing experiences with Primer Brand UI Shared Foundations
- **Mozilla Protocol**: Protocol is still an evolving project. Currently it’s used primarily by the Mozilla Marketing Websites team as the front-end for www.mozilla.org . ...
- **Pajamas Design System**: creative agency or vendor collaborating with us on our marketing efforts. partner or customer that is interested in representing our brand on digit...

### 구현 노트

- 기존에 같은 역할의 컴포넌트가 있으면 토큰 교체부터 시작
- variant prop으로 시각적 변형을 관리 (하드코딩 금지)
- 섹션에 <h2 id="...">과 aria-labelledby 필수
- CSS 변수(var(--color-*))를 그대로 쓰고 hex 하드코딩 금지
- 다크 모드는 globals.css의 prefers-color-scheme 블록에 위임
- 애니메이션은 상태 설명용으로만 사용, 장식 효과 금지
- 텍스트 위계가 핵심 — 컬러보다 weight/size로 구분

---

## marketing / site-nav

**역할**: 주요 섹션 내비게이션 링크

**탐지 출처**: site header

**Slot archetype**: `nav-bar`

### 구조 (Anatomy)

- sticky-container
- inner-max-width
- left-group
- right-group

### 상태 (States)

| 상태 | 설명 |
|------|------|
| `default` | 기본 상태 |
| `scrolled` | scrolled |

### 토큰 바인딩

```
surface: var(--color-surface)
border-bottom: var(--color-border)
height: 64px
padding: 0 var(--space-24)
inner-max-width: 1120px
z-index: 50
backdrop-filter: blur(8px)
```

### 접근성

- <header role="banner"> 또는 <nav aria-label="Primary">
- 키보드 탐색 시 논리적 탭 순서 유지
- 랜드마크가 중복되지 않도록 main 이외 영역에만 배치

### 브랜드 적용

- [calm+precise+editorial+trustworthy] color: 중성 톤 위주, accent는 최소한으로 + 정확한 semantic 분리, 모호한 중간 톤 지양 + 타이포그래피로 위계 형성, 컬러보다 weight/size 활용 + 안정적인 neutral 기반, 과한 accent 변화 없음
- [calm+precise+editorial+trustworthy] motion: 150-200ms ease-out, bounce/spring 없음 + 120-180ms, 군더더기 없는 전환 + 콘텐츠 전환 위주, UI chrome 모션 최소화 + 모든 전환에 동일한 easing/duration
- [calm+precise+editorial+trustworthy] density: comfortable 모드 기본, 여유로운 padding + 엄격한 spacing scale 준수, 임의 값 금지 + 넉넉한 line-height와 margin, 읽기 편한 간격 + 기존 레이아웃 유지, 갑작스런 위치 변경 없음

### 레퍼런스 근거

- **Primer**: Design digital marketing experiences with Primer Brand UI Shared Foundations
- **Mozilla Protocol**: Protocol is still an evolving project. Currently it’s used primarily by the Mozilla Marketing Websites team as the front-end for www.mozilla.org . ...
- **Pajamas Design System**: creative agency or vendor collaborating with us on our marketing efforts. partner or customer that is interested in representing our brand on digit...

### 구현 노트

- 기존에 같은 역할의 컴포넌트가 있으면 토큰 교체부터 시작
- variant prop으로 시각적 변형을 관리 (하드코딩 금지)
- 섹션에 <h2 id="...">과 aria-labelledby 필수
- CSS 변수(var(--color-*))를 그대로 쓰고 hex 하드코딩 금지
- 다크 모드는 globals.css의 prefers-color-scheme 블록에 위임
- 애니메이션은 상태 설명용으로만 사용, 장식 효과 금지
- 텍스트 위계가 핵심 — 컬러보다 weight/size로 구분

---

## button / site-nav-cta

**역할**: 헤더 우측 CTA 버튼 (로그인/시작하기)

**탐지 출처**: site header

**Slot archetype**: `nav-bar`

### 구조 (Anatomy)

- sticky-container
- inner-max-width
- left-group
- right-group

### 상태 (States)

| 상태 | 설명 |
|------|------|
| `default` | 기본 상태 |
| `scrolled` | scrolled |

### 토큰 바인딩

```
surface: var(--color-surface)
border-bottom: var(--color-border)
height: 64px
padding: 0 var(--space-24)
inner-max-width: 1120px
z-index: 50
backdrop-filter: blur(8px)
```

### 접근성

- <header role="banner"> 또는 <nav aria-label="Primary">
- 키보드 탐색 시 논리적 탭 순서 유지
- 랜드마크가 중복되지 않도록 main 이외 영역에만 배치

### 브랜드 적용

- [calm+precise+editorial+trustworthy] hover: opacity 변화 (0.08-0.12), elevation 변화 없음 + 정확한 border/outline 변화 + 텍스트 underline 또는 color shift, 장식적 효과 없음 + 예측 가능하고 일관된 hover 패턴
- [calm+precise+editorial+trustworthy] motion: 150-200ms ease-out, bounce/spring 없음 + 120-180ms, 군더더기 없는 전환 + 콘텐츠 전환 위주, UI chrome 모션 최소화 + 모든 전환에 동일한 easing/duration
- [calm+precise+editorial+trustworthy] color: 중성 톤 위주, accent는 최소한으로 + 정확한 semantic 분리, 모호한 중간 톤 지양 + 타이포그래피로 위계 형성, 컬러보다 weight/size 활용 + 안정적인 neutral 기반, 과한 accent 변화 없음

### 레퍼런스 근거

- **Carbon Design System**: These components can toggle between the AI variant and the default variant depending on the user’s interaction. If the user manually overrides the ...
- **Elastic UI Framework | Elastic UI Framework**: Button Variety of buttons and button groups with different styles and colours Button
- **Workday Canvas Design System**: New AI Ingress Button in Labs AI Ingress Button with open and close CTA will be available in Labs.

### 구현 노트

- 기존에 같은 역할의 컴포넌트가 있으면 토큰 교체부터 시작
- variant prop으로 시각적 변형을 관리 (하드코딩 금지)
- size prop: sm / md / lg (터치 영역은 항상 최소 44px 보장)
- 애니메이션은 상태 설명용으로만 사용, 장식 효과 금지
- 텍스트 위계가 핵심 — 컬러보다 weight/size로 구분

---

## button / mobile-menu-trigger

**역할**: 모바일 햄버거 메뉴 버튼

**탐지 출처**: site header

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

- [calm+precise+editorial+trustworthy] hover: opacity 변화 (0.08-0.12), elevation 변화 없음 + 정확한 border/outline 변화 + 텍스트 underline 또는 color shift, 장식적 효과 없음 + 예측 가능하고 일관된 hover 패턴
- [calm+precise+editorial+trustworthy] motion: 150-200ms ease-out, bounce/spring 없음 + 120-180ms, 군더더기 없는 전환 + 콘텐츠 전환 위주, UI chrome 모션 최소화 + 모든 전환에 동일한 easing/duration
- [calm+precise+editorial+trustworthy] color: 중성 톤 위주, accent는 최소한으로 + 정확한 semantic 분리, 모호한 중간 톤 지양 + 타이포그래피로 위계 형성, 컬러보다 weight/size 활용 + 안정적인 neutral 기반, 과한 accent 변화 없음

### 레퍼런스 근거

- **Carbon Design System**: These components can toggle between the AI variant and the default variant depending on the user’s interaction. If the user manually overrides the ...
- **Elastic UI Framework | Elastic UI Framework**: Button Variety of buttons and button groups with different styles and colours Button
- **Workday Canvas Design System**: New AI Ingress Button in Labs AI Ingress Button with open and close CTA will be available in Labs.

### 구현 노트

- 기존에 같은 역할의 컴포넌트가 있으면 토큰 교체부터 시작
- variant prop으로 시각적 변형을 관리 (하드코딩 금지)
- size prop: sm / md / lg (터치 영역은 항상 최소 44px 보장)
- 애니메이션은 상태 설명용으로만 사용, 장식 효과 금지
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

- [calm+precise+editorial+trustworthy] density: comfortable 모드 기본, 여유로운 padding + 엄격한 spacing scale 준수, 임의 값 금지 + 넉넉한 line-height와 margin, 읽기 편한 간격 + 기존 레이아웃 유지, 갑작스런 위치 변경 없음
- [calm+precise+editorial+trustworthy] color: 중성 톤 위주, accent는 최소한으로 + 정확한 semantic 분리, 모호한 중간 톤 지양 + 타이포그래피로 위계 형성, 컬러보다 weight/size 활용 + 안정적인 neutral 기반, 과한 accent 변화 없음

### 레퍼런스 근거

- **Workday Canvas Design System**: New Avatar Component in Preview A new Avatar component will be available in Preview to reflect the updated brand guidelines.
- **The Foundation for your Design System - shadcn/ui**: Avatar Badge

### 구현 노트

- 기존에 같은 역할의 컴포넌트가 있으면 토큰 교체부터 시작
- variant prop으로 시각적 변형을 관리 (하드코딩 금지)
- 빈 상태(empty-state)와 에러 상태를 반드시 처리
- 애니메이션은 상태 설명용으로만 사용, 장식 효과 금지
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

- [calm+precise+editorial+trustworthy] motion: 150-200ms ease-out, bounce/spring 없음 + 120-180ms, 군더더기 없는 전환 + 콘텐츠 전환 위주, UI chrome 모션 최소화 + 모든 전환에 동일한 easing/duration
- [calm+precise+editorial+trustworthy] density: comfortable 모드 기본, 여유로운 padding + 엄격한 spacing scale 준수, 임의 값 금지 + 넉넉한 line-height와 margin, 읽기 편한 간격 + 기존 레이아웃 유지, 갑작스런 위치 변경 없음

### 레퍼런스 근거

- **Cedar Design System | REI Co-op**: Overlay, typically in the middle of the page Components
- **Workday Canvas Design System**: Interaction overlays for hover/pressed states Semantic foreground colors for info, danger, warning, success states
- **Mantine**: Core components library: inputs, buttons, overlays, etc. @mantine/form

### 구현 노트

- 기존에 같은 역할의 컴포넌트가 있으면 토큰 교체부터 시작
- variant prop으로 시각적 변형을 관리 (하드코딩 금지)
- Escape / backdrop click으로 닫기, 열 때 첫 focusable 요소로 이동
- 애니메이션은 상태 설명용으로만 사용, 장식 효과 금지
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

- [calm+precise+editorial+trustworthy] density: comfortable 모드 기본, 여유로운 padding + 엄격한 spacing scale 준수, 임의 값 금지 + 넉넉한 line-height와 margin, 읽기 편한 간격 + 기존 레이아웃 유지, 갑작스런 위치 변경 없음
- [calm+precise+editorial+trustworthy] color: 중성 톤 위주, accent는 최소한으로 + 정확한 semantic 분리, 모호한 중간 톤 지양 + 타이포그래피로 위계 형성, 컬러보다 weight/size 활용 + 안정적인 neutral 기반, 과한 accent 변화 없음

### 구현 노트

- 기존에 같은 역할의 컴포넌트가 있으면 토큰 교체부터 시작
- variant prop으로 시각적 변형을 관리 (하드코딩 금지)
- 빈 상태(empty-state)와 에러 상태를 반드시 처리
- 애니메이션은 상태 설명용으로만 사용, 장식 효과 금지
- 텍스트 위계가 핵심 — 컬러보다 weight/size로 구분

---

## marketing / feature-section

**역할**: 기능 섹션 컨테이너와 섹션 헤더

**탐지 출처**: feature grid

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

- [calm+precise+editorial+trustworthy] color: 중성 톤 위주, accent는 최소한으로 + 정확한 semantic 분리, 모호한 중간 톤 지양 + 타이포그래피로 위계 형성, 컬러보다 weight/size 활용 + 안정적인 neutral 기반, 과한 accent 변화 없음
- [calm+precise+editorial+trustworthy] motion: 150-200ms ease-out, bounce/spring 없음 + 120-180ms, 군더더기 없는 전환 + 콘텐츠 전환 위주, UI chrome 모션 최소화 + 모든 전환에 동일한 easing/duration
- [calm+precise+editorial+trustworthy] density: comfortable 모드 기본, 여유로운 padding + 엄격한 spacing scale 준수, 임의 값 금지 + 넉넉한 line-height와 margin, 읽기 편한 간격 + 기존 레이아웃 유지, 갑작스런 위치 변경 없음

### 레퍼런스 근거

- **Primer**: Design digital marketing experiences with Primer Brand UI Shared Foundations
- **Mozilla Protocol**: Protocol is still an evolving project. Currently it’s used primarily by the Mozilla Marketing Websites team as the front-end for www.mozilla.org . ...
- **Pajamas Design System**: creative agency or vendor collaborating with us on our marketing efforts. partner or customer that is interested in representing our brand on digit...

### 구현 노트

- 기존에 같은 역할의 컴포넌트가 있으면 토큰 교체부터 시작
- variant prop으로 시각적 변형을 관리 (하드코딩 금지)
- 섹션에 <h2 id="...">과 aria-labelledby 필수
- CSS 변수(var(--color-*))를 그대로 쓰고 hex 하드코딩 금지
- 다크 모드는 globals.css의 prefers-color-scheme 블록에 위임
- 애니메이션은 상태 설명용으로만 사용, 장식 효과 금지
- 텍스트 위계가 핵심 — 컬러보다 weight/size로 구분

---

## marketing / feature-grid

**역할**: 여러 개의 기능 카드를 배치하는 그리드

**탐지 출처**: feature grid

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

- [calm+precise+editorial+trustworthy] color: 중성 톤 위주, accent는 최소한으로 + 정확한 semantic 분리, 모호한 중간 톤 지양 + 타이포그래피로 위계 형성, 컬러보다 weight/size 활용 + 안정적인 neutral 기반, 과한 accent 변화 없음
- [calm+precise+editorial+trustworthy] motion: 150-200ms ease-out, bounce/spring 없음 + 120-180ms, 군더더기 없는 전환 + 콘텐츠 전환 위주, UI chrome 모션 최소화 + 모든 전환에 동일한 easing/duration
- [calm+precise+editorial+trustworthy] density: comfortable 모드 기본, 여유로운 padding + 엄격한 spacing scale 준수, 임의 값 금지 + 넉넉한 line-height와 margin, 읽기 편한 간격 + 기존 레이아웃 유지, 갑작스런 위치 변경 없음

### 레퍼런스 근거

- **Primer**: Design digital marketing experiences with Primer Brand UI Shared Foundations
- **Mozilla Protocol**: Protocol is still an evolving project. Currently it’s used primarily by the Mozilla Marketing Websites team as the front-end for www.mozilla.org . ...
- **Pajamas Design System**: creative agency or vendor collaborating with us on our marketing efforts. partner or customer that is interested in representing our brand on digit...

### 구현 노트

- 기존에 같은 역할의 컴포넌트가 있으면 토큰 교체부터 시작
- variant prop으로 시각적 변형을 관리 (하드코딩 금지)
- 섹션에 <h2 id="...">과 aria-labelledby 필수
- CSS 변수(var(--color-*))를 그대로 쓰고 hex 하드코딩 금지
- 다크 모드는 globals.css의 prefers-color-scheme 블록에 위임
- 애니메이션은 상태 설명용으로만 사용, 장식 효과 금지
- 텍스트 위계가 핵심 — 컬러보다 weight/size로 구분

---

## marketing / feature-card

**역할**: 개별 기능 카드 (아이콘+제목+설명)

**탐지 출처**: feature grid

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

- [calm+precise+editorial+trustworthy] color: 중성 톤 위주, accent는 최소한으로 + 정확한 semantic 분리, 모호한 중간 톤 지양 + 타이포그래피로 위계 형성, 컬러보다 weight/size 활용 + 안정적인 neutral 기반, 과한 accent 변화 없음
- [calm+precise+editorial+trustworthy] motion: 150-200ms ease-out, bounce/spring 없음 + 120-180ms, 군더더기 없는 전환 + 콘텐츠 전환 위주, UI chrome 모션 최소화 + 모든 전환에 동일한 easing/duration
- [calm+precise+editorial+trustworthy] density: comfortable 모드 기본, 여유로운 padding + 엄격한 spacing scale 준수, 임의 값 금지 + 넉넉한 line-height와 margin, 읽기 편한 간격 + 기존 레이아웃 유지, 갑작스런 위치 변경 없음

### 레퍼런스 근거

- **Primer**: Design digital marketing experiences with Primer Brand UI Shared Foundations
- **Mozilla Protocol**: Protocol is still an evolving project. Currently it’s used primarily by the Mozilla Marketing Websites team as the front-end for www.mozilla.org . ...
- **Pajamas Design System**: creative agency or vendor collaborating with us on our marketing efforts. partner or customer that is interested in representing our brand on digit...

### 구현 노트

- 기존에 같은 역할의 컴포넌트가 있으면 토큰 교체부터 시작
- variant prop으로 시각적 변형을 관리 (하드코딩 금지)
- 섹션에 <h2 id="...">과 aria-labelledby 필수
- CSS 변수(var(--color-*))를 그대로 쓰고 hex 하드코딩 금지
- 다크 모드는 globals.css의 prefers-color-scheme 블록에 위임
- 애니메이션은 상태 설명용으로만 사용, 장식 효과 금지
- 텍스트 위계가 핵심 — 컬러보다 weight/size로 구분

---

## marketing / feature-icon

**역할**: 기능을 상징하는 아이콘

**탐지 출처**: feature grid

**Slot archetype**: `icon-holder`

### 구조 (Anatomy)

- icon-container
- icon-svg

### 상태 (States)

| 상태 | 설명 |
|------|------|
| `default` | 기본 상태 |

### 토큰 바인딩

```
container-surface: var(--color-surface-tint)
container-size: 40px
container-radius: var(--radius-md)
icon-stroke: var(--color-brand-primary)
icon-size: 20px
icon-stroke-width: 1.75
```

### 접근성

- 장식용이면 aria-hidden="true"
- 의미가 있으면 <title> 포함

### 브랜드 적용

- [calm+precise+editorial+trustworthy] color: 중성 톤 위주, accent는 최소한으로 + 정확한 semantic 분리, 모호한 중간 톤 지양 + 타이포그래피로 위계 형성, 컬러보다 weight/size 활용 + 안정적인 neutral 기반, 과한 accent 변화 없음
- [calm+precise+editorial+trustworthy] motion: 150-200ms ease-out, bounce/spring 없음 + 120-180ms, 군더더기 없는 전환 + 콘텐츠 전환 위주, UI chrome 모션 최소화 + 모든 전환에 동일한 easing/duration
- [calm+precise+editorial+trustworthy] density: comfortable 모드 기본, 여유로운 padding + 엄격한 spacing scale 준수, 임의 값 금지 + 넉넉한 line-height와 margin, 읽기 편한 간격 + 기존 레이아웃 유지, 갑작스런 위치 변경 없음

### 레퍼런스 근거

- **Primer**: Design digital marketing experiences with Primer Brand UI Shared Foundations
- **Mozilla Protocol**: Protocol is still an evolving project. Currently it’s used primarily by the Mozilla Marketing Websites team as the front-end for www.mozilla.org . ...
- **Pajamas Design System**: creative agency or vendor collaborating with us on our marketing efforts. partner or customer that is interested in representing our brand on digit...

### 구현 노트

- 기존에 같은 역할의 컴포넌트가 있으면 토큰 교체부터 시작
- variant prop으로 시각적 변형을 관리 (하드코딩 금지)
- 섹션에 <h2 id="...">과 aria-labelledby 필수
- CSS 변수(var(--color-*))를 그대로 쓰고 hex 하드코딩 금지
- 다크 모드는 globals.css의 prefers-color-scheme 블록에 위임
- 애니메이션은 상태 설명용으로만 사용, 장식 효과 금지
- 텍스트 위계가 핵심 — 컬러보다 weight/size로 구분

---

## marketing / feature-title

**역할**: 기능 카드 제목

**탐지 출처**: feature grid

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

- [calm+precise+editorial+trustworthy] color: 중성 톤 위주, accent는 최소한으로 + 정확한 semantic 분리, 모호한 중간 톤 지양 + 타이포그래피로 위계 형성, 컬러보다 weight/size 활용 + 안정적인 neutral 기반, 과한 accent 변화 없음
- [calm+precise+editorial+trustworthy] motion: 150-200ms ease-out, bounce/spring 없음 + 120-180ms, 군더더기 없는 전환 + 콘텐츠 전환 위주, UI chrome 모션 최소화 + 모든 전환에 동일한 easing/duration
- [calm+precise+editorial+trustworthy] density: comfortable 모드 기본, 여유로운 padding + 엄격한 spacing scale 준수, 임의 값 금지 + 넉넉한 line-height와 margin, 읽기 편한 간격 + 기존 레이아웃 유지, 갑작스런 위치 변경 없음

### 레퍼런스 근거

- **Primer**: Design digital marketing experiences with Primer Brand UI Shared Foundations
- **Mozilla Protocol**: Protocol is still an evolving project. Currently it’s used primarily by the Mozilla Marketing Websites team as the front-end for www.mozilla.org . ...
- **Pajamas Design System**: creative agency or vendor collaborating with us on our marketing efforts. partner or customer that is interested in representing our brand on digit...

### 구현 노트

- 기존에 같은 역할의 컴포넌트가 있으면 토큰 교체부터 시작
- variant prop으로 시각적 변형을 관리 (하드코딩 금지)
- 섹션에 <h2 id="...">과 aria-labelledby 필수
- CSS 변수(var(--color-*))를 그대로 쓰고 hex 하드코딩 금지
- 다크 모드는 globals.css의 prefers-color-scheme 블록에 위임
- 애니메이션은 상태 설명용으로만 사용, 장식 효과 금지
- 텍스트 위계가 핵심 — 컬러보다 weight/size로 구분

---

## marketing / feature-description

**역할**: 기능 카드 본문 설명

**탐지 출처**: feature grid

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

- [calm+precise+editorial+trustworthy] color: 중성 톤 위주, accent는 최소한으로 + 정확한 semantic 분리, 모호한 중간 톤 지양 + 타이포그래피로 위계 형성, 컬러보다 weight/size 활용 + 안정적인 neutral 기반, 과한 accent 변화 없음
- [calm+precise+editorial+trustworthy] motion: 150-200ms ease-out, bounce/spring 없음 + 120-180ms, 군더더기 없는 전환 + 콘텐츠 전환 위주, UI chrome 모션 최소화 + 모든 전환에 동일한 easing/duration
- [calm+precise+editorial+trustworthy] density: comfortable 모드 기본, 여유로운 padding + 엄격한 spacing scale 준수, 임의 값 금지 + 넉넉한 line-height와 margin, 읽기 편한 간격 + 기존 레이아웃 유지, 갑작스런 위치 변경 없음

### 레퍼런스 근거

- **Primer**: Design digital marketing experiences with Primer Brand UI Shared Foundations
- **Mozilla Protocol**: Protocol is still an evolving project. Currently it’s used primarily by the Mozilla Marketing Websites team as the front-end for www.mozilla.org . ...
- **Pajamas Design System**: creative agency or vendor collaborating with us on our marketing efforts. partner or customer that is interested in representing our brand on digit...

### 구현 노트

- 기존에 같은 역할의 컴포넌트가 있으면 토큰 교체부터 시작
- variant prop으로 시각적 변형을 관리 (하드코딩 금지)
- 섹션에 <h2 id="...">과 aria-labelledby 필수
- CSS 변수(var(--color-*))를 그대로 쓰고 hex 하드코딩 금지
- 다크 모드는 globals.css의 prefers-color-scheme 블록에 위임
- 애니메이션은 상태 설명용으로만 사용, 장식 효과 금지
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

- [calm+precise+editorial+trustworthy] feedback: subtle inline alert 선호, 과한 컬러 블록 지양 + 명확한 상태 구분, 진행률/결과를 수치로 표시 + 콘텐츠 맥락 안에서 인라인 표시, 토스트보다 인라인 선호 + 결과를 반드시 확인, 실패 시 복구 방법 안내
- [calm+precise+editorial+trustworthy] motion: 150-200ms ease-out, bounce/spring 없음 + 120-180ms, 군더더기 없는 전환 + 콘텐츠 전환 위주, UI chrome 모션 최소화 + 모든 전환에 동일한 easing/duration
- [calm+precise+editorial+trustworthy] color: 중성 톤 위주, accent는 최소한으로 + 정확한 semantic 분리, 모호한 중간 톤 지양 + 타이포그래피로 위계 형성, 컬러보다 weight/size 활용 + 안정적인 neutral 기반, 과한 accent 변화 없음

### 레퍼런스 근거

- **Atlassian Design**: We finish what we start before starting something new. We're informed by continuous feedback. 3. Bring people on the journey before helping for the...
- **Carbon Design System**: We welcome all feedback, designs, or ideas in order to produce the best possible experience for our users. If you're interested in contributing, ch...
- **Clarity Design System**: Clarity firmly believes that the best products are built by those who form a rich, varied community. We invite all forms of feedback or ideas that ...

### 구현 노트

- 기존에 같은 역할의 컴포넌트가 있으면 토큰 교체부터 시작
- variant prop으로 시각적 변형을 관리 (하드코딩 금지)
- auto-dismiss 시간은 내용 길이에 비례 (기본 5초)
- 애니메이션은 상태 설명용으로만 사용, 장식 효과 금지
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

- [calm+precise+editorial+trustworthy] hover: opacity 변화 (0.08-0.12), elevation 변화 없음 + 정확한 border/outline 변화 + 텍스트 underline 또는 color shift, 장식적 효과 없음 + 예측 가능하고 일관된 hover 패턴
- [calm+precise+editorial+trustworthy] density: comfortable 모드 기본, 여유로운 padding + 엄격한 spacing scale 준수, 임의 값 금지 + 넉넉한 line-height와 margin, 읽기 편한 간격 + 기존 레이아웃 유지, 갑작스런 위치 변경 없음
- [calm+precise+editorial+trustworthy] motion: 150-200ms ease-out, bounce/spring 없음 + 120-180ms, 군더더기 없는 전환 + 콘텐츠 전환 위주, UI chrome 모션 최소화 + 모든 전환에 동일한 easing/duration

### 레퍼런스 근거

- **Cedar Design System | REI Co-op**: Don’t reuse bespoke UI intended for other message or navigation types Options
- **Mantine**: Navigation progress Install dependencies:
- **Chakra UI**: Here's an example of customizing the header layout with RangeText and navigation buttons. Month and Year Select

### 구현 노트

- 기존에 같은 역할의 컴포넌트가 있으면 토큰 교체부터 시작
- variant prop으로 시각적 변형을 관리 (하드코딩 금지)
- active 상태는 URL/라우터와 자동 동기화
- 애니메이션은 상태 설명용으로만 사용, 장식 효과 금지
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

- [calm+precise+editorial+trustworthy] motion: 150-200ms ease-out, bounce/spring 없음 + 120-180ms, 군더더기 없는 전환 + 콘텐츠 전환 위주, UI chrome 모션 최소화 + 모든 전환에 동일한 easing/duration
- [calm+precise+editorial+trustworthy] density: comfortable 모드 기본, 여유로운 padding + 엄격한 spacing scale 준수, 임의 값 금지 + 넉넉한 line-height와 margin, 읽기 편한 간격 + 기존 레이아웃 유지, 갑작스런 위치 변경 없음

### 레퍼런스 근거

- **Cedar Design System | REI Co-op**: Overlay, typically in the middle of the page Components
- **Workday Canvas Design System**: Interaction overlays for hover/pressed states Semantic foreground colors for info, danger, warning, success states
- **Mantine**: Core components library: inputs, buttons, overlays, etc. @mantine/form

### 구현 노트

- 기존에 같은 역할의 컴포넌트가 있으면 토큰 교체부터 시작
- variant prop으로 시각적 변형을 관리 (하드코딩 금지)
- Escape / backdrop click으로 닫기, 열 때 첫 focusable 요소로 이동
- 애니메이션은 상태 설명용으로만 사용, 장식 효과 금지
- 텍스트 위계가 핵심 — 컬러보다 weight/size로 구분
