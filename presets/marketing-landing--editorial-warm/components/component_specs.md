# Loom Component Specs

총 128개 컴포넌트 | 패밀리: button, commerce, data-display, document, feedback, input, magazine, marketing, navigation, overlay

## 구현 원칙 (Non-negotiable)

이 스펙의 모든 컴포넌트를 구현할 때 반드시 지킨다:

1. **이모지를 UI로 쓰지 않는다** — 🎨 ✅ 🔥 ⚡ 🚀 ❌ ⭐ 📊 등 이모지를 아이콘, 상태 표시, 버튼 장식, 네비게이션 지표 자리에 절대 넣지 않는다. 리팩토링 중 카드/버튼/배지/탭/상태 UI에서 이모지를 발견하면 SVG 파일, SVG 컴포넌트, 또는 Lucide/Heroicons/Phosphor/Tabler 같은 아이콘 라이브러리로 교체한다.
2. **컴포넌트를 직접 구현한다** — 아래 각 컴포넌트의 anatomy(구조), states(상태), 토큰 바인딩, 접근성 규칙을 그대로 따라 완전하게 구현한다. '임시', 'TODO', '플레이스홀더' 같은 반쪽 구현을 남기지 않는다.
3. **라이브러리 기본 스타일 금지** — 라이브러리 컴포넌트를 그대로 import해서 쓰지 않는다. 반드시 디자인 토큰(--color-*, --space-*, --radius-*, --font-*)으로 스타일을 명시적으로 바인딩한다.
4. **접근성은 옵션이 아니다** — 각 컴포넌트의 '접근성' 섹션에 정의된 role, aria-*, label, focus 관리 규칙을 전부 적용한다.
5. **hex 값 하드코딩 금지** — 색상은 반드시 semantic token을 경유한다 (예: `color: var(--color-ink)` not `color: #2C2C2C`).
6. **모바일 overflow 금지** — 버튼, CTA, 탭, 필터칩, 툴바 액션은 320px viewport에서 화면 밖으로 나가면 안 된다. fixed/min-width px 값으로 폭을 고정하지 말고 wrap/stack fallback을 제공한다.

## 브랜드 적용 규칙

- **hover**: 텍스트 underline 또는 color shift, 장식적 효과 없음 + opacity 변화 (0.08-0.12), elevation 변화 없음
- **motion**: 콘텐츠 전환 위주, UI chrome 모션 최소화 + 150-200ms ease-out, bounce/spring 없음
- **color**: 타이포그래피로 위계 형성, 컬러보다 weight/size 활용 + 중성 톤 위주, accent는 최소한으로
- **density**: 넉넉한 line-height와 margin, 읽기 편한 간격 + comfortable 모드 기본, 여유로운 padding
- **feedback**: 콘텐츠 맥락 안에서 인라인 표시, 토스트보다 인라인 선호 + subtle inline alert 선호, 과한 컬러 블록 지양

## Visual-reference 적용 원칙

- anatomy / states / accessibility는 설계서(spec)와 KB 근거를 유지하고, visual adaptation은 elevation / framing / prominence / density 같은 표현 계층에만 advisory signal로 적용한다.
- Active visual signals: surface_style=tinted, density=airy, corner_style=medium, top_layout_cue=landing-narrative
- Connected component hints: cards, data_display, hero, navigation, typography

## Typography Guardrails

- 한글 기반 제품은 line-break / scale / tracking을 영문 랜딩 기본값으로 처리하지 않고, 아래 가드레일을 구현 기본값으로 사용한다.
- Headline: Pretendard | line-height 1.25-1.35 | tracking 0em
- Body: Pretendard | line-height 1.6-1.7 | label line-height 1.4-1.5
- Wrap defaults: headline word-break=keep-all, headline text-wrap=balance, body word-break=keep-all
- Scale guidance: 한글 hero/section heading은 영문 시안보다 한 단계 작은 스케일에서 시작해 wrap을 확인한 뒤 확장한다.
- Hangul display safety: line-height >= 1.02 | tracking -0.02em to 0.01em | forced <br /> 금지 until breakpoint QA
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

- [editorial+calm] hover: 텍스트 underline 또는 color shift, 장식적 효과 없음 + opacity 변화 (0.08-0.12), elevation 변화 없음
- [editorial+calm] motion: 콘텐츠 전환 위주, UI chrome 모션 최소화 + 150-200ms ease-out, bounce/spring 없음
- [editorial+calm] color: 타이포그래피로 위계 형성, 컬러보다 weight/size 활용 + 중성 톤 위주, accent는 최소한으로

### Visual Adaptation Hints

- **cta_prominence**: CTA prominence는 strong이다. 섹션당 primary CTA 1개만 fill/accent로 강하게 띄우고 secondary는 조용하게 후퇴시킨다. (source=hero; confidence=0.29; provenance=inferred; direction=대형 hero와 trust strip, CTA cluster를 허용하되 과장된 glass/gradient 효과는 지양한다.; evidence=Narrative landing flow, layout=landing-narrative, density=airy)

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
- 애니메이션은 상태 설명용으로만 사용, 장식 효과 금지
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

- [editorial+calm] hover: 텍스트 underline 또는 color shift, 장식적 효과 없음 + opacity 변화 (0.08-0.12), elevation 변화 없음
- [editorial+calm] motion: 콘텐츠 전환 위주, UI chrome 모션 최소화 + 150-200ms ease-out, bounce/spring 없음
- [editorial+calm] color: 타이포그래피로 위계 형성, 컬러보다 weight/size 활용 + 중성 톤 위주, accent는 최소한으로

### Visual Adaptation Hints

- **cta_prominence**: CTA prominence는 strong이다. 섹션당 primary CTA 1개만 fill/accent로 강하게 띄우고 secondary는 조용하게 후퇴시킨다. (source=hero; confidence=0.29; provenance=inferred; direction=대형 hero와 trust strip, CTA cluster를 허용하되 과장된 glass/gradient 효과는 지양한다.; evidence=Narrative landing flow, layout=landing-narrative, density=airy)

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
- 애니메이션은 상태 설명용으로만 사용, 장식 효과 금지
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

- [editorial+calm] hover: 텍스트 underline 또는 color shift, 장식적 효과 없음 + opacity 변화 (0.08-0.12), elevation 변화 없음
- [editorial+calm] motion: 콘텐츠 전환 위주, UI chrome 모션 최소화 + 150-200ms ease-out, bounce/spring 없음
- [editorial+calm] color: 타이포그래피로 위계 형성, 컬러보다 weight/size 활용 + 중성 톤 위주, accent는 최소한으로

### Visual Adaptation Hints

- **cta_prominence**: CTA prominence는 strong이다. 섹션당 primary CTA 1개만 fill/accent로 강하게 띄우고 secondary는 조용하게 후퇴시킨다. (source=hero; confidence=0.29; provenance=inferred; direction=대형 hero와 trust strip, CTA cluster를 허용하되 과장된 glass/gradient 효과는 지양한다.; evidence=Narrative landing flow, layout=landing-narrative, density=airy)

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

- [editorial+calm] density: 넉넉한 line-height와 margin, 읽기 편한 간격 + comfortable 모드 기본, 여유로운 padding
- [editorial+calm] color: 타이포그래피로 위계 형성, 컬러보다 weight/size 활용 + 중성 톤 위주, accent는 최소한으로

### Visual Adaptation Hints

- **card_elevation_tendency**: 카드는 낮은 elevation만 허용하고 색면 차이로 그룹을 구분한다. 내부 여백은 넉넉하게 두고 card breathing room을 확보한다. (source=cards; confidence=0.29; provenance=inferred; direction=low-elevation tinted cards를 기본으로 하고, 넓은 내부 여백과 강한 section breathing room. 중간 반경으로 제품 UI 절제 유지.; evidence=surface=tinted, density=airy, corner=medium)
- **border_vs_fill_emphasis**: fill 중심이다. tint surface로 성격을 만들고 border는 아주 얇게 보조한다. (source=cards; confidence=0.29; provenance=inferred; direction=low-elevation tinted cards를 기본으로 하고, 넓은 내부 여백과 강한 section breathing room. 중간 반경으로 제품 UI 절제 유지.; evidence=surface=tinted, density=airy, corner=medium)
- **chart_panel_framing**: 차트 패널은 soft tint frame과 restrained divider로 프레이밍한다. 헤더 메타데이터와 본문 visualization 사이의 breathing room을 충분히 둔다. (source=data_display; confidence=0.29; provenance=inferred; direction=정보 밀도를 유지하되 thin dividers와 restrained accent로 hierarchy를 만든다.; evidence=layout=dashboard-grid, density=airy, layout=landing-narrative, surface=tinted)

### 구현 노트

- 기존에 같은 역할의 컴포넌트가 있으면 토큰 교체부터 시작
- variant prop으로 시각적 변형을 관리 (하드코딩 금지)
- 빈 상태(empty-state)와 에러 상태를 반드시 처리
- 좁은 UI 텍스트는 Pretendard 기준 label line-height 1.4-1.5를 참고해 뭉침을 방지
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

- [editorial+calm] density: 넉넉한 line-height와 margin, 읽기 편한 간격 + comfortable 모드 기본, 여유로운 padding
- [editorial+calm] color: 타이포그래피로 위계 형성, 컬러보다 weight/size 활용 + 중성 톤 위주, accent는 최소한으로

### Visual Adaptation Hints

- **card_elevation_tendency**: 카드는 낮은 elevation만 허용하고 색면 차이로 그룹을 구분한다. 내부 여백은 넉넉하게 두고 card breathing room을 확보한다. (source=cards; confidence=0.29; provenance=inferred; direction=low-elevation tinted cards를 기본으로 하고, 넓은 내부 여백과 강한 section breathing room. 중간 반경으로 제품 UI 절제 유지.; evidence=surface=tinted, density=airy, corner=medium)
- **border_vs_fill_emphasis**: fill 중심이다. tint surface로 성격을 만들고 border는 아주 얇게 보조한다. (source=cards; confidence=0.29; provenance=inferred; direction=low-elevation tinted cards를 기본으로 하고, 넓은 내부 여백과 강한 section breathing room. 중간 반경으로 제품 UI 절제 유지.; evidence=surface=tinted, density=airy, corner=medium)
- **chart_panel_framing**: 차트 패널은 soft tint frame과 restrained divider로 프레이밍한다. 헤더 메타데이터와 본문 visualization 사이의 breathing room을 충분히 둔다. (source=data_display; confidence=0.29; provenance=inferred; direction=정보 밀도를 유지하되 thin dividers와 restrained accent로 hierarchy를 만든다.; evidence=layout=dashboard-grid, density=airy, layout=landing-narrative, surface=tinted)

### 구현 노트

- 기존에 같은 역할의 컴포넌트가 있으면 토큰 교체부터 시작
- variant prop으로 시각적 변형을 관리 (하드코딩 금지)
- 빈 상태(empty-state)와 에러 상태를 반드시 처리
- 좁은 UI 텍스트는 Pretendard 기준 label line-height 1.4-1.5를 참고해 뭉침을 방지
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

- [editorial+calm] feedback: 콘텐츠 맥락 안에서 인라인 표시, 토스트보다 인라인 선호 + subtle inline alert 선호, 과한 컬러 블록 지양
- [editorial+calm] motion: 콘텐츠 전환 위주, UI chrome 모션 최소화 + 150-200ms ease-out, bounce/spring 없음
- [editorial+calm] color: 타이포그래피로 위계 형성, 컬러보다 weight/size 활용 + 중성 톤 위주, accent는 최소한으로

### Visual Adaptation Hints

- **card_elevation_tendency**: 카드는 낮은 elevation만 허용하고 색면 차이로 그룹을 구분한다. 내부 여백은 넉넉하게 두고 card breathing room을 확보한다. (source=cards; confidence=0.29; provenance=inferred; direction=low-elevation tinted cards를 기본으로 하고, 넓은 내부 여백과 강한 section breathing room. 중간 반경으로 제품 UI 절제 유지.; evidence=surface=tinted, density=airy, corner=medium)
- **border_vs_fill_emphasis**: fill 중심이다. tint surface로 성격을 만들고 border는 아주 얇게 보조한다. (source=cards; confidence=0.29; provenance=inferred; direction=low-elevation tinted cards를 기본으로 하고, 넓은 내부 여백과 강한 section breathing room. 중간 반경으로 제품 UI 절제 유지.; evidence=surface=tinted, density=airy, corner=medium)
- **cta_prominence**: CTA prominence는 strong이다. 섹션당 primary CTA 1개만 fill/accent로 강하게 띄우고 secondary는 조용하게 후퇴시킨다. (source=hero; confidence=0.29; provenance=inferred; direction=대형 hero와 trust strip, CTA cluster를 허용하되 과장된 glass/gradient 효과는 지양한다.; evidence=Narrative landing flow, layout=landing-narrative, density=airy)

### 레퍼런스 근거

- **Carbon Design System**: We welcome all feedback, designs, or ideas in order to produce the best possible experience for our users. If you're interested in contributing, ch...
- **Primer**: Messaging components are used to provide important and relevant information to the user, including feedback, contextual information, product update...

### 구현 노트

- 기존에 같은 역할의 컴포넌트가 있으면 토큰 교체부터 시작
- variant prop으로 시각적 변형을 관리 (하드코딩 금지)
- auto-dismiss 시간은 내용 길이에 비례 (기본 5초)
- 반응형 검증: 320px, 360px, 390px, 430px에서 control overflow와 viewport horizontal scroll이 없어야 함
- action row는 narrow viewport에서 `flex-wrap: wrap` 또는 세로 stack으로 전환하고, overflow-x 숨김으로 문제를 덮지 않음
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

- [editorial+calm] color: 타이포그래피로 위계 형성, 컬러보다 weight/size 활용 + 중성 톤 위주, accent는 최소한으로
- [editorial+calm] motion: 콘텐츠 전환 위주, UI chrome 모션 최소화 + 150-200ms ease-out, bounce/spring 없음
- [editorial+calm] density: 넉넉한 line-height와 margin, 읽기 편한 간격 + comfortable 모드 기본, 여유로운 padding

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
- 좁은 UI 텍스트는 Pretendard 기준 label line-height 1.4-1.5를 참고해 뭉침을 방지
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

- [editorial+calm] color: 타이포그래피로 위계 형성, 컬러보다 weight/size 활용 + 중성 톤 위주, accent는 최소한으로
- [editorial+calm] motion: 콘텐츠 전환 위주, UI chrome 모션 최소화 + 150-200ms ease-out, bounce/spring 없음
- [editorial+calm] density: 넉넉한 line-height와 margin, 읽기 편한 간격 + comfortable 모드 기본, 여유로운 padding

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
- 좁은 UI 텍스트는 Pretendard 기준 label line-height 1.4-1.5를 참고해 뭉침을 방지
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

- [editorial+calm] color: 타이포그래피로 위계 형성, 컬러보다 weight/size 활용 + 중성 톤 위주, accent는 최소한으로
- [editorial+calm] motion: 콘텐츠 전환 위주, UI chrome 모션 최소화 + 150-200ms ease-out, bounce/spring 없음
- [editorial+calm] density: 넉넉한 line-height와 margin, 읽기 편한 간격 + comfortable 모드 기본, 여유로운 padding

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
- 좁은 UI 텍스트는 Pretendard 기준 label line-height 1.4-1.5를 참고해 뭉침을 방지
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

- [editorial+calm] color: 타이포그래피로 위계 형성, 컬러보다 weight/size 활용 + 중성 톤 위주, accent는 최소한으로
- [editorial+calm] motion: 콘텐츠 전환 위주, UI chrome 모션 최소화 + 150-200ms ease-out, bounce/spring 없음
- [editorial+calm] density: 넉넉한 line-height와 margin, 읽기 편한 간격 + comfortable 모드 기본, 여유로운 padding

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
- 좁은 UI 텍스트는 Pretendard 기준 label line-height 1.4-1.5를 참고해 뭉침을 방지
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

- [editorial+calm] hover: 텍스트 underline 또는 color shift, 장식적 효과 없음 + opacity 변화 (0.08-0.12), elevation 변화 없음
- [editorial+calm] motion: 콘텐츠 전환 위주, UI chrome 모션 최소화 + 150-200ms ease-out, bounce/spring 없음
- [editorial+calm] color: 타이포그래피로 위계 형성, 컬러보다 weight/size 활용 + 중성 톤 위주, accent는 최소한으로

### Visual Adaptation Hints

- **cta_prominence**: CTA prominence는 strong이다. 섹션당 primary CTA 1개만 fill/accent로 강하게 띄우고 secondary는 조용하게 후퇴시킨다. (source=hero; confidence=0.29; provenance=inferred; direction=대형 hero와 trust strip, CTA cluster를 허용하되 과장된 glass/gradient 효과는 지양한다.; evidence=Narrative landing flow, layout=landing-narrative, density=airy)

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

- [editorial+calm] color: 타이포그래피로 위계 형성, 컬러보다 weight/size 활용 + 중성 톤 위주, accent는 최소한으로
- [editorial+calm] motion: 콘텐츠 전환 위주, UI chrome 모션 최소화 + 150-200ms ease-out, bounce/spring 없음
- [editorial+calm] density: 넉넉한 line-height와 margin, 읽기 편한 간격 + comfortable 모드 기본, 여유로운 padding

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
- 좁은 UI 텍스트는 Pretendard 기준 label line-height 1.4-1.5를 참고해 뭉침을 방지
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

- [editorial+calm] color: 타이포그래피로 위계 형성, 컬러보다 weight/size 활용 + 중성 톤 위주, accent는 최소한으로
- [editorial+calm] motion: 콘텐츠 전환 위주, UI chrome 모션 최소화 + 150-200ms ease-out, bounce/spring 없음
- [editorial+calm] density: 넉넉한 line-height와 margin, 읽기 편한 간격 + comfortable 모드 기본, 여유로운 padding

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
- 좁은 UI 텍스트는 Pretendard 기준 label line-height 1.4-1.5를 참고해 뭉침을 방지
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

- [editorial+calm] color: 타이포그래피로 위계 형성, 컬러보다 weight/size 활용 + 중성 톤 위주, accent는 최소한으로
- [editorial+calm] motion: 콘텐츠 전환 위주, UI chrome 모션 최소화 + 150-200ms ease-out, bounce/spring 없음
- [editorial+calm] density: 넉넉한 line-height와 margin, 읽기 편한 간격 + comfortable 모드 기본, 여유로운 padding

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
- 좁은 UI 텍스트는 Pretendard 기준 label line-height 1.4-1.5를 참고해 뭉침을 방지
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

- [editorial+calm] color: 타이포그래피로 위계 형성, 컬러보다 weight/size 활용 + 중성 톤 위주, accent는 최소한으로
- [editorial+calm] motion: 콘텐츠 전환 위주, UI chrome 모션 최소화 + 150-200ms ease-out, bounce/spring 없음
- [editorial+calm] density: 넉넉한 line-height와 margin, 읽기 편한 간격 + comfortable 모드 기본, 여유로운 padding

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
- 좁은 UI 텍스트는 Pretendard 기준 label line-height 1.4-1.5를 참고해 뭉침을 방지
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

- [editorial+calm] color: 타이포그래피로 위계 형성, 컬러보다 weight/size 활용 + 중성 톤 위주, accent는 최소한으로
- [editorial+calm] motion: 콘텐츠 전환 위주, UI chrome 모션 최소화 + 150-200ms ease-out, bounce/spring 없음
- [editorial+calm] density: 넉넉한 line-height와 margin, 읽기 편한 간격 + comfortable 모드 기본, 여유로운 padding

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
- 좁은 UI 텍스트는 Pretendard 기준 label line-height 1.4-1.5를 참고해 뭉침을 방지
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

- [editorial+calm] color: 타이포그래피로 위계 형성, 컬러보다 weight/size 활용 + 중성 톤 위주, accent는 최소한으로
- [editorial+calm] motion: 콘텐츠 전환 위주, UI chrome 모션 최소화 + 150-200ms ease-out, bounce/spring 없음
- [editorial+calm] density: 넉넉한 line-height와 margin, 읽기 편한 간격 + comfortable 모드 기본, 여유로운 padding

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
- 좁은 UI 텍스트는 Pretendard 기준 label line-height 1.4-1.5를 참고해 뭉침을 방지
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

- [editorial+calm] color: 타이포그래피로 위계 형성, 컬러보다 weight/size 활용 + 중성 톤 위주, accent는 최소한으로
- [editorial+calm] motion: 콘텐츠 전환 위주, UI chrome 모션 최소화 + 150-200ms ease-out, bounce/spring 없음
- [editorial+calm] density: 넉넉한 line-height와 margin, 읽기 편한 간격 + comfortable 모드 기본, 여유로운 padding

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
- 좁은 UI 텍스트는 Pretendard 기준 label line-height 1.4-1.5를 참고해 뭉침을 방지
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

- [editorial+calm] color: 타이포그래피로 위계 형성, 컬러보다 weight/size 활용 + 중성 톤 위주, accent는 최소한으로
- [editorial+calm] motion: 콘텐츠 전환 위주, UI chrome 모션 최소화 + 150-200ms ease-out, bounce/spring 없음
- [editorial+calm] density: 넉넉한 line-height와 margin, 읽기 편한 간격 + comfortable 모드 기본, 여유로운 padding

### Visual Adaptation Hints

- **card_elevation_tendency**: 카드는 낮은 elevation만 허용하고 색면 차이로 그룹을 구분한다. 내부 여백은 넉넉하게 두고 card breathing room을 확보한다. (source=cards; confidence=0.29; provenance=inferred; direction=low-elevation tinted cards를 기본으로 하고, 넓은 내부 여백과 강한 section breathing room. 중간 반경으로 제품 UI 절제 유지.; evidence=surface=tinted, density=airy, corner=medium)
- **border_vs_fill_emphasis**: fill 중심이다. tint surface로 성격을 만들고 border는 아주 얇게 보조한다. (source=cards; confidence=0.29; provenance=inferred; direction=low-elevation tinted cards를 기본으로 하고, 넓은 내부 여백과 강한 section breathing room. 중간 반경으로 제품 UI 절제 유지.; evidence=surface=tinted, density=airy, corner=medium)

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
- 좁은 UI 텍스트는 Pretendard 기준 label line-height 1.4-1.5를 참고해 뭉침을 방지
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

- [editorial+calm] color: 타이포그래피로 위계 형성, 컬러보다 weight/size 활용 + 중성 톤 위주, accent는 최소한으로
- [editorial+calm] motion: 콘텐츠 전환 위주, UI chrome 모션 최소화 + 150-200ms ease-out, bounce/spring 없음
- [editorial+calm] density: 넉넉한 line-height와 margin, 읽기 편한 간격 + comfortable 모드 기본, 여유로운 padding

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
- 좁은 UI 텍스트는 Pretendard 기준 label line-height 1.4-1.5를 참고해 뭉침을 방지
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

- [editorial+calm] color: 타이포그래피로 위계 형성, 컬러보다 weight/size 활용 + 중성 톤 위주, accent는 최소한으로
- [editorial+calm] motion: 콘텐츠 전환 위주, UI chrome 모션 최소화 + 150-200ms ease-out, bounce/spring 없음
- [editorial+calm] density: 넉넉한 line-height와 margin, 읽기 편한 간격 + comfortable 모드 기본, 여유로운 padding

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
- 좁은 UI 텍스트는 Pretendard 기준 label line-height 1.4-1.5를 참고해 뭉침을 방지
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

- [editorial+calm] color: 타이포그래피로 위계 형성, 컬러보다 weight/size 활용 + 중성 톤 위주, accent는 최소한으로
- [editorial+calm] motion: 콘텐츠 전환 위주, UI chrome 모션 최소화 + 150-200ms ease-out, bounce/spring 없음
- [editorial+calm] density: 넉넉한 line-height와 margin, 읽기 편한 간격 + comfortable 모드 기본, 여유로운 padding

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
- 좁은 UI 텍스트는 Pretendard 기준 label line-height 1.4-1.5를 참고해 뭉침을 방지
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

- [editorial+calm] color: 타이포그래피로 위계 형성, 컬러보다 weight/size 활용 + 중성 톤 위주, accent는 최소한으로
- [editorial+calm] motion: 콘텐츠 전환 위주, UI chrome 모션 최소화 + 150-200ms ease-out, bounce/spring 없음
- [editorial+calm] density: 넉넉한 line-height와 margin, 읽기 편한 간격 + comfortable 모드 기본, 여유로운 padding

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
- 좁은 UI 텍스트는 Pretendard 기준 label line-height 1.4-1.5를 참고해 뭉침을 방지
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

- [editorial+calm] color: 타이포그래피로 위계 형성, 컬러보다 weight/size 활용 + 중성 톤 위주, accent는 최소한으로
- [editorial+calm] motion: 콘텐츠 전환 위주, UI chrome 모션 최소화 + 150-200ms ease-out, bounce/spring 없음
- [editorial+calm] density: 넉넉한 line-height와 margin, 읽기 편한 간격 + comfortable 모드 기본, 여유로운 padding

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
- 좁은 UI 텍스트는 Pretendard 기준 label line-height 1.4-1.5를 참고해 뭉침을 방지
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

- [editorial+calm] color: 타이포그래피로 위계 형성, 컬러보다 weight/size 활용 + 중성 톤 위주, accent는 최소한으로
- [editorial+calm] motion: 콘텐츠 전환 위주, UI chrome 모션 최소화 + 150-200ms ease-out, bounce/spring 없음
- [editorial+calm] density: 넉넉한 line-height와 margin, 읽기 편한 간격 + comfortable 모드 기본, 여유로운 padding

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
- 좁은 UI 텍스트는 Pretendard 기준 label line-height 1.4-1.5를 참고해 뭉침을 방지
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

- [editorial+calm] color: 타이포그래피로 위계 형성, 컬러보다 weight/size 활용 + 중성 톤 위주, accent는 최소한으로
- [editorial+calm] motion: 콘텐츠 전환 위주, UI chrome 모션 최소화 + 150-200ms ease-out, bounce/spring 없음
- [editorial+calm] density: 넉넉한 line-height와 margin, 읽기 편한 간격 + comfortable 모드 기본, 여유로운 padding

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
- 좁은 UI 텍스트는 Pretendard 기준 label line-height 1.4-1.5를 참고해 뭉침을 방지
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

- [editorial+calm] hover: 텍스트 underline 또는 color shift, 장식적 효과 없음 + opacity 변화 (0.08-0.12), elevation 변화 없음
- [editorial+calm] density: 넉넉한 line-height와 margin, 읽기 편한 간격 + comfortable 모드 기본, 여유로운 padding
- [editorial+calm] feedback: 콘텐츠 맥락 안에서 인라인 표시, 토스트보다 인라인 선호 + subtle inline alert 선호, 과한 컬러 블록 지양

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

- [editorial+calm] hover: 텍스트 underline 또는 color shift, 장식적 효과 없음 + opacity 변화 (0.08-0.12), elevation 변화 없음
- [editorial+calm] density: 넉넉한 line-height와 margin, 읽기 편한 간격 + comfortable 모드 기본, 여유로운 padding
- [editorial+calm] feedback: 콘텐츠 맥락 안에서 인라인 표시, 토스트보다 인라인 선호 + subtle inline alert 선호, 과한 컬러 블록 지양

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

- [editorial+calm] hover: 텍스트 underline 또는 color shift, 장식적 효과 없음 + opacity 변화 (0.08-0.12), elevation 변화 없음
- [editorial+calm] density: 넉넉한 line-height와 margin, 읽기 편한 간격 + comfortable 모드 기본, 여유로운 padding
- [editorial+calm] feedback: 콘텐츠 맥락 안에서 인라인 표시, 토스트보다 인라인 선호 + subtle inline alert 선호, 과한 컬러 블록 지양

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

- [editorial+calm] hover: 텍스트 underline 또는 color shift, 장식적 효과 없음 + opacity 변화 (0.08-0.12), elevation 변화 없음
- [editorial+calm] density: 넉넉한 line-height와 margin, 읽기 편한 간격 + comfortable 모드 기본, 여유로운 padding
- [editorial+calm] feedback: 콘텐츠 맥락 안에서 인라인 표시, 토스트보다 인라인 선호 + subtle inline alert 선호, 과한 컬러 블록 지양

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

- [editorial+calm] hover: 텍스트 underline 또는 color shift, 장식적 효과 없음 + opacity 변화 (0.08-0.12), elevation 변화 없음
- [editorial+calm] density: 넉넉한 line-height와 margin, 읽기 편한 간격 + comfortable 모드 기본, 여유로운 padding
- [editorial+calm] feedback: 콘텐츠 맥락 안에서 인라인 표시, 토스트보다 인라인 선호 + subtle inline alert 선호, 과한 컬러 블록 지양

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

- [editorial+calm] hover: 텍스트 underline 또는 color shift, 장식적 효과 없음 + opacity 변화 (0.08-0.12), elevation 변화 없음
- [editorial+calm] density: 넉넉한 line-height와 margin, 읽기 편한 간격 + comfortable 모드 기본, 여유로운 padding
- [editorial+calm] feedback: 콘텐츠 맥락 안에서 인라인 표시, 토스트보다 인라인 선호 + subtle inline alert 선호, 과한 컬러 블록 지양

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

- [editorial+calm] hover: 텍스트 underline 또는 color shift, 장식적 효과 없음 + opacity 변화 (0.08-0.12), elevation 변화 없음
- [editorial+calm] motion: 콘텐츠 전환 위주, UI chrome 모션 최소화 + 150-200ms ease-out, bounce/spring 없음
- [editorial+calm] color: 타이포그래피로 위계 형성, 컬러보다 weight/size 활용 + 중성 톤 위주, accent는 최소한으로

### Visual Adaptation Hints

- **cta_prominence**: CTA prominence는 strong이다. 섹션당 primary CTA 1개만 fill/accent로 강하게 띄우고 secondary는 조용하게 후퇴시킨다. (source=hero; confidence=0.29; provenance=inferred; direction=대형 hero와 trust strip, CTA cluster를 허용하되 과장된 glass/gradient 효과는 지양한다.; evidence=Narrative landing flow, layout=landing-narrative, density=airy)

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

- [editorial+calm] density: 넉넉한 line-height와 margin, 읽기 편한 간격 + comfortable 모드 기본, 여유로운 padding
- [editorial+calm] color: 타이포그래피로 위계 형성, 컬러보다 weight/size 활용 + 중성 톤 위주, accent는 최소한으로

### Visual Adaptation Hints

- **card_elevation_tendency**: 카드는 낮은 elevation만 허용하고 색면 차이로 그룹을 구분한다. 내부 여백은 넉넉하게 두고 card breathing room을 확보한다. (source=cards; confidence=0.29; provenance=inferred; direction=low-elevation tinted cards를 기본으로 하고, 넓은 내부 여백과 강한 section breathing room. 중간 반경으로 제품 UI 절제 유지.; evidence=surface=tinted, density=airy, corner=medium)
- **border_vs_fill_emphasis**: fill 중심이다. tint surface로 성격을 만들고 border는 아주 얇게 보조한다. (source=cards; confidence=0.29; provenance=inferred; direction=low-elevation tinted cards를 기본으로 하고, 넓은 내부 여백과 강한 section breathing room. 중간 반경으로 제품 UI 절제 유지.; evidence=surface=tinted, density=airy, corner=medium)
- **chart_panel_framing**: 차트 패널은 soft tint frame과 restrained divider로 프레이밍한다. 헤더 메타데이터와 본문 visualization 사이의 breathing room을 충분히 둔다. (source=data_display; confidence=0.29; provenance=inferred; direction=정보 밀도를 유지하되 thin dividers와 restrained accent로 hierarchy를 만든다.; evidence=layout=dashboard-grid, density=airy, layout=landing-narrative, surface=tinted)

### 레퍼런스 근거

- **Carbon Design System**: Tag Date picker
- **Primer**: Primer color design tokens are made available within data-attribute selectors on the body tag or other high level dom element. There are three dist...

### 구현 노트

- 기존에 같은 역할의 컴포넌트가 있으면 토큰 교체부터 시작
- variant prop으로 시각적 변형을 관리 (하드코딩 금지)
- 빈 상태(empty-state)와 에러 상태를 반드시 처리
- 좁은 UI 텍스트는 Pretendard 기준 label line-height 1.4-1.5를 참고해 뭉침을 방지
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

- [editorial+calm] feedback: 콘텐츠 맥락 안에서 인라인 표시, 토스트보다 인라인 선호 + subtle inline alert 선호, 과한 컬러 블록 지양
- [editorial+calm] motion: 콘텐츠 전환 위주, UI chrome 모션 최소화 + 150-200ms ease-out, bounce/spring 없음
- [editorial+calm] color: 타이포그래피로 위계 형성, 컬러보다 weight/size 활용 + 중성 톤 위주, accent는 최소한으로

### Visual Adaptation Hints

- **card_elevation_tendency**: 카드는 낮은 elevation만 허용하고 색면 차이로 그룹을 구분한다. 내부 여백은 넉넉하게 두고 card breathing room을 확보한다. (source=cards; confidence=0.29; provenance=inferred; direction=low-elevation tinted cards를 기본으로 하고, 넓은 내부 여백과 강한 section breathing room. 중간 반경으로 제품 UI 절제 유지.; evidence=surface=tinted, density=airy, corner=medium)
- **border_vs_fill_emphasis**: fill 중심이다. tint surface로 성격을 만들고 border는 아주 얇게 보조한다. (source=cards; confidence=0.29; provenance=inferred; direction=low-elevation tinted cards를 기본으로 하고, 넓은 내부 여백과 강한 section breathing room. 중간 반경으로 제품 UI 절제 유지.; evidence=surface=tinted, density=airy, corner=medium)
- **chart_panel_framing**: 차트 패널은 soft tint frame과 restrained divider로 프레이밍한다. 헤더 메타데이터와 본문 visualization 사이의 breathing room을 충분히 둔다. (source=data_display; confidence=0.29; provenance=inferred; direction=정보 밀도를 유지하되 thin dividers와 restrained accent로 hierarchy를 만든다.; evidence=layout=dashboard-grid, density=airy, layout=landing-narrative, surface=tinted)

### 레퍼런스 근거

- **Carbon Design System**: We welcome all feedback, designs, or ideas in order to produce the best possible experience for our users. If you're interested in contributing, ch...
- **Primer**: Messaging components are used to provide important and relevant information to the user, including feedback, contextual information, product update...

### 구현 노트

- 기존에 같은 역할의 컴포넌트가 있으면 토큰 교체부터 시작
- variant prop으로 시각적 변형을 관리 (하드코딩 금지)
- auto-dismiss 시간은 내용 길이에 비례 (기본 5초)
- 반응형 검증: 320px, 360px, 390px, 430px에서 control overflow와 viewport horizontal scroll이 없어야 함
- action row는 narrow viewport에서 `flex-wrap: wrap` 또는 세로 stack으로 전환하고, overflow-x 숨김으로 문제를 덮지 않음
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

- [editorial+calm] hover: 텍스트 underline 또는 color shift, 장식적 효과 없음 + opacity 변화 (0.08-0.12), elevation 변화 없음
- [editorial+calm] density: 넉넉한 line-height와 margin, 읽기 편한 간격 + comfortable 모드 기본, 여유로운 padding
- [editorial+calm] feedback: 콘텐츠 맥락 안에서 인라인 표시, 토스트보다 인라인 선호 + subtle inline alert 선호, 과한 컬러 블록 지양

### Visual Adaptation Hints

- **filter_nav_density**: filter/nav density는 low다. top nav는 가볍게 유지하고 filter controls는 별도 섹션 또는 로컬 toolbar로 분리한다. (source=navigation; confidence=0.29; provenance=inferred; direction=top navigation은 가볍게 유지하고 CTA와 section anchors를 분명하게 분리한다.; evidence=Narrative landing flow, layout=landing-narrative, density=airy)

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

- [editorial+calm] density: 넉넉한 line-height와 margin, 읽기 편한 간격 + comfortable 모드 기본, 여유로운 padding
- [editorial+calm] color: 타이포그래피로 위계 형성, 컬러보다 weight/size 활용 + 중성 톤 위주, accent는 최소한으로

### Visual Adaptation Hints

- **operational_surface_role**: 주 작업 표면은 card wall이 아니라 table/list/rail/canvas 계열로 설계한다. 행 간격은 읽기 편하게 두되 반복 항목은 같은 카드 껍질로 감싸지 않는다. (source=data_display; confidence=0.29; provenance=inferred; direction=정보 밀도를 유지하되 thin dividers와 restrained accent로 hierarchy를 만든다.; evidence=layout=dashboard-grid, density=airy, layout=landing-narrative)
- **filter_nav_density**: filter/nav density는 low다. top nav는 가볍게 유지하고 filter controls는 별도 섹션 또는 로컬 toolbar로 분리한다. (source=navigation; confidence=0.29; provenance=inferred; direction=top navigation은 가볍게 유지하고 CTA와 section anchors를 분명하게 분리한다.; evidence=Narrative landing flow, layout=landing-narrative, density=airy)
- **chart_panel_framing**: 차트 패널은 soft tint frame과 restrained divider로 프레이밍한다. 헤더 메타데이터와 본문 visualization 사이의 breathing room을 충분히 둔다. (source=data_display; confidence=0.29; provenance=inferred; direction=정보 밀도를 유지하되 thin dividers와 restrained accent로 hierarchy를 만든다.; evidence=layout=dashboard-grid, density=airy, layout=landing-narrative, surface=tinted)

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

- [editorial+calm] density: 넉넉한 line-height와 margin, 읽기 편한 간격 + comfortable 모드 기본, 여유로운 padding
- [editorial+calm] color: 타이포그래피로 위계 형성, 컬러보다 weight/size 활용 + 중성 톤 위주, accent는 최소한으로

### Visual Adaptation Hints

- **operational_surface_role**: 주 작업 표면은 card wall이 아니라 table/list/rail/canvas 계열로 설계한다. 행 간격은 읽기 편하게 두되 반복 항목은 같은 카드 껍질로 감싸지 않는다. (source=data_display; confidence=0.29; provenance=inferred; direction=정보 밀도를 유지하되 thin dividers와 restrained accent로 hierarchy를 만든다.; evidence=layout=dashboard-grid, density=airy, layout=landing-narrative)
- **chart_panel_framing**: 차트 패널은 soft tint frame과 restrained divider로 프레이밍한다. 헤더 메타데이터와 본문 visualization 사이의 breathing room을 충분히 둔다. (source=data_display; confidence=0.29; provenance=inferred; direction=정보 밀도를 유지하되 thin dividers와 restrained accent로 hierarchy를 만든다.; evidence=layout=dashboard-grid, density=airy, layout=landing-narrative, surface=tinted)

### 구현 노트

- 기존에 같은 역할의 컴포넌트가 있으면 토큰 교체부터 시작
- variant prop으로 시각적 변형을 관리 (하드코딩 금지)
- 빈 상태(empty-state)와 에러 상태를 반드시 처리
- 좁은 UI 텍스트는 Pretendard 기준 label line-height 1.4-1.5를 참고해 뭉침을 방지
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

- [editorial+calm] density: 넉넉한 line-height와 margin, 읽기 편한 간격 + comfortable 모드 기본, 여유로운 padding
- [editorial+calm] color: 타이포그래피로 위계 형성, 컬러보다 weight/size 활용 + 중성 톤 위주, accent는 최소한으로

### Visual Adaptation Hints

- **operational_surface_role**: 주 작업 표면은 card wall이 아니라 table/list/rail/canvas 계열로 설계한다. 행 간격은 읽기 편하게 두되 반복 항목은 같은 카드 껍질로 감싸지 않는다. (source=data_display; confidence=0.29; provenance=inferred; direction=정보 밀도를 유지하되 thin dividers와 restrained accent로 hierarchy를 만든다.; evidence=layout=dashboard-grid, density=airy, layout=landing-narrative)
- **chart_panel_framing**: 차트 패널은 soft tint frame과 restrained divider로 프레이밍한다. 헤더 메타데이터와 본문 visualization 사이의 breathing room을 충분히 둔다. (source=data_display; confidence=0.29; provenance=inferred; direction=정보 밀도를 유지하되 thin dividers와 restrained accent로 hierarchy를 만든다.; evidence=layout=dashboard-grid, density=airy, layout=landing-narrative, surface=tinted)

### 구현 노트

- 기존에 같은 역할의 컴포넌트가 있으면 토큰 교체부터 시작
- variant prop으로 시각적 변형을 관리 (하드코딩 금지)
- 빈 상태(empty-state)와 에러 상태를 반드시 처리
- 좁은 UI 텍스트는 Pretendard 기준 label line-height 1.4-1.5를 참고해 뭉침을 방지
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

- [editorial+calm] hover: 텍스트 underline 또는 color shift, 장식적 효과 없음 + opacity 변화 (0.08-0.12), elevation 변화 없음
- [editorial+calm] density: 넉넉한 line-height와 margin, 읽기 편한 간격 + comfortable 모드 기본, 여유로운 padding
- [editorial+calm] motion: 콘텐츠 전환 위주, UI chrome 모션 최소화 + 150-200ms ease-out, bounce/spring 없음

### Visual Adaptation Hints

- **filter_nav_density**: filter/nav density는 low다. top nav는 가볍게 유지하고 filter controls는 별도 섹션 또는 로컬 toolbar로 분리한다. (source=navigation; confidence=0.29; provenance=inferred; direction=top navigation은 가볍게 유지하고 CTA와 section anchors를 분명하게 분리한다.; evidence=Narrative landing flow, layout=landing-narrative, density=airy)

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

- [editorial+calm] hover: 텍스트 underline 또는 color shift, 장식적 효과 없음 + opacity 변화 (0.08-0.12), elevation 변화 없음
- [editorial+calm] density: 넉넉한 line-height와 margin, 읽기 편한 간격 + comfortable 모드 기본, 여유로운 padding
- [editorial+calm] feedback: 콘텐츠 맥락 안에서 인라인 표시, 토스트보다 인라인 선호 + subtle inline alert 선호, 과한 컬러 블록 지양

### Visual Adaptation Hints

- **filter_nav_density**: filter/nav density는 low다. top nav는 가볍게 유지하고 filter controls는 별도 섹션 또는 로컬 toolbar로 분리한다. (source=navigation; confidence=0.29; provenance=inferred; direction=top navigation은 가볍게 유지하고 CTA와 section anchors를 분명하게 분리한다.; evidence=Narrative landing flow, layout=landing-narrative, density=airy)

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
- 애니메이션은 상태 설명용으로만 사용, 장식 효과 금지
- 텍스트 위계가 핵심 — 컬러보다 weight/size로 구분

---

## magazine / opinion-byline

**역할**: opinion 필자 byline — 필자 이름 + 직함 + 사진 + SNS 링크

**탐지 출처**: opinion long-form

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

- [editorial+calm] hover: 텍스트 underline 또는 color shift, 장식적 효과 없음 + opacity 변화 (0.08-0.12), elevation 변화 없음
- [editorial+calm] motion: 콘텐츠 전환 위주, UI chrome 모션 최소화 + 150-200ms ease-out, bounce/spring 없음
- [editorial+calm] color: 타이포그래피로 위계 형성, 컬러보다 weight/size 활용 + 중성 톤 위주, accent는 최소한으로

### 레퍼런스 근거

- **Primer**: Alla Kholmatova’s Design Systems book was one of the first resources I came across in this area and it broadened my understanding greatly. The work...

### 구현 노트

- 기존에 같은 역할의 컴포넌트가 있으면 토큰 교체부터 시작
- variant prop으로 시각적 변형을 관리 (하드코딩 금지)
- 애니메이션은 상태 설명용으로만 사용, 장식 효과 금지
- 텍스트 위계가 핵심 — 컬러보다 weight/size로 구분

---

## magazine / manifesto-section

**역할**: 매니페스토/선언 섹션 — bold declaration 문단 + saturated accent surface

**탐지 출처**: opinion long-form

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

- [editorial+calm] hover: 텍스트 underline 또는 color shift, 장식적 효과 없음 + opacity 변화 (0.08-0.12), elevation 변화 없음
- [editorial+calm] motion: 콘텐츠 전환 위주, UI chrome 모션 최소화 + 150-200ms ease-out, bounce/spring 없음
- [editorial+calm] color: 타이포그래피로 위계 형성, 컬러보다 weight/size 활용 + 중성 톤 위주, accent는 최소한으로

### 레퍼런스 근거

- **Primer**: Alla Kholmatova’s Design Systems book was one of the first resources I came across in this area and it broadened my understanding greatly. The work...

### 구현 노트

- 기존에 같은 역할의 컴포넌트가 있으면 토큰 교체부터 시작
- variant prop으로 시각적 변형을 관리 (하드코딩 금지)
- 애니메이션은 상태 설명용으로만 사용, 장식 효과 금지
- 텍스트 위계가 핵심 — 컬러보다 weight/size로 구분

---

## magazine / feature-grid-index

**역할**: issue feature 목차 그리드 — number-heavy tile + kicker + title + byline

**탐지 출처**: opinion long-form

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

- [editorial+calm] hover: 텍스트 underline 또는 color shift, 장식적 효과 없음 + opacity 변화 (0.08-0.12), elevation 변화 없음
- [editorial+calm] motion: 콘텐츠 전환 위주, UI chrome 모션 최소화 + 150-200ms ease-out, bounce/spring 없음
- [editorial+calm] color: 타이포그래피로 위계 형성, 컬러보다 weight/size 활용 + 중성 톤 위주, accent는 최소한으로

### Visual Adaptation Hints

- **card_elevation_tendency**: 카드는 낮은 elevation만 허용하고 색면 차이로 그룹을 구분한다. 내부 여백은 넉넉하게 두고 card breathing room을 확보한다. (source=cards; confidence=0.29; provenance=inferred; direction=low-elevation tinted cards를 기본으로 하고, 넓은 내부 여백과 강한 section breathing room. 중간 반경으로 제품 UI 절제 유지.; evidence=surface=tinted, density=airy, corner=medium)
- **border_vs_fill_emphasis**: fill 중심이다. tint surface로 성격을 만들고 border는 아주 얇게 보조한다. (source=cards; confidence=0.29; provenance=inferred; direction=low-elevation tinted cards를 기본으로 하고, 넓은 내부 여백과 강한 section breathing room. 중간 반경으로 제품 UI 절제 유지.; evidence=surface=tinted, density=airy, corner=medium)
- **chart_panel_framing**: 차트 패널은 soft tint frame과 restrained divider로 프레이밍한다. 헤더 메타데이터와 본문 visualization 사이의 breathing room을 충분히 둔다. (source=data_display; confidence=0.29; provenance=inferred; direction=정보 밀도를 유지하되 thin dividers와 restrained accent로 hierarchy를 만든다.; evidence=layout=dashboard-grid, density=airy, layout=landing-narrative, surface=tinted)

### 레퍼런스 근거

- **Primer**: Alla Kholmatova’s Design Systems book was one of the first resources I came across in this area and it broadened my understanding greatly. The work...

### 구현 노트

- 기존에 같은 역할의 컴포넌트가 있으면 토큰 교체부터 시작
- variant prop으로 시각적 변형을 관리 (하드코딩 금지)
- 애니메이션은 상태 설명용으로만 사용, 장식 효과 금지
- 텍스트 위계가 핵심 — 컬러보다 weight/size로 구분

---

## magazine / archive-index

**역할**: 전체 아카이브 인덱스 — year/issue 필터 + list

**탐지 출처**: opinion long-form

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

- [editorial+calm] hover: 텍스트 underline 또는 color shift, 장식적 효과 없음 + opacity 변화 (0.08-0.12), elevation 변화 없음
- [editorial+calm] motion: 콘텐츠 전환 위주, UI chrome 모션 최소화 + 150-200ms ease-out, bounce/spring 없음
- [editorial+calm] color: 타이포그래피로 위계 형성, 컬러보다 weight/size 활용 + 중성 톤 위주, accent는 최소한으로

### 레퍼런스 근거

- **Primer**: Alla Kholmatova’s Design Systems book was one of the first resources I came across in this area and it broadened my understanding greatly. The work...

### 구현 노트

- 기존에 같은 역할의 컴포넌트가 있으면 토큰 교체부터 시작
- variant prop으로 시각적 변형을 관리 (하드코딩 금지)
- 애니메이션은 상태 설명용으로만 사용, 장식 효과 금지
- 텍스트 위계가 핵심 — 컬러보다 weight/size로 구분

---

## magazine / issue-archive

**역할**: 과거 이슈 아카이브 — cover thumbnail + issue number + publish date

**탐지 출처**: opinion long-form

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

- [editorial+calm] hover: 텍스트 underline 또는 color shift, 장식적 효과 없음 + opacity 변화 (0.08-0.12), elevation 변화 없음
- [editorial+calm] motion: 콘텐츠 전환 위주, UI chrome 모션 최소화 + 150-200ms ease-out, bounce/spring 없음
- [editorial+calm] color: 타이포그래피로 위계 형성, 컬러보다 weight/size 활용 + 중성 톤 위주, accent는 최소한으로

### 레퍼런스 근거

- **Primer**: Alla Kholmatova’s Design Systems book was one of the first resources I came across in this area and it broadened my understanding greatly. The work...

### 구현 노트

- 기존에 같은 역할의 컴포넌트가 있으면 토큰 교체부터 시작
- variant prop으로 시각적 변형을 관리 (하드코딩 금지)
- 애니메이션은 상태 설명용으로만 사용, 장식 효과 금지
- 텍스트 위계가 핵심 — 컬러보다 weight/size로 구분

---

## feedback / reading-progress-bar

**역할**: article 상단 reading progress bar — long-form prose scroll 위치 추적, heading-anchor 진행 하이라이트

**탐지 출처**: opinion long-form

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

- [editorial+calm] feedback: 콘텐츠 맥락 안에서 인라인 표시, 토스트보다 인라인 선호 + subtle inline alert 선호, 과한 컬러 블록 지양
- [editorial+calm] motion: 콘텐츠 전환 위주, UI chrome 모션 최소화 + 150-200ms ease-out, bounce/spring 없음
- [editorial+calm] color: 타이포그래피로 위계 형성, 컬러보다 weight/size 활용 + 중성 톤 위주, accent는 최소한으로

### 레퍼런스 근거

- **Carbon Design System**: We welcome all feedback, designs, or ideas in order to produce the best possible experience for our users. If you're interested in contributing, ch...
- **Primer**: Messaging components are used to provide important and relevant information to the user, including feedback, contextual information, product update...

### 구현 노트

- 기존에 같은 역할의 컴포넌트가 있으면 토큰 교체부터 시작
- variant prop으로 시각적 변형을 관리 (하드코딩 금지)
- auto-dismiss 시간은 내용 길이에 비례 (기본 5초)
- 반응형 검증: 320px, 360px, 390px, 430px에서 control overflow와 viewport horizontal scroll이 없어야 함
- action row는 narrow viewport에서 `flex-wrap: wrap` 또는 세로 stack으로 전환하고, overflow-x 숨김으로 문제를 덮지 않음
- 애니메이션은 상태 설명용으로만 사용, 장식 효과 금지
- 텍스트 위계가 핵심 — 컬러보다 weight/size로 구분

---

## magazine / credit-line

**역할**: article 하단 credit line — 사진/일러스트/에디터 크레딧, mono

**탐지 출처**: opinion long-form

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

- [editorial+calm] hover: 텍스트 underline 또는 color shift, 장식적 효과 없음 + opacity 변화 (0.08-0.12), elevation 변화 없음
- [editorial+calm] motion: 콘텐츠 전환 위주, UI chrome 모션 최소화 + 150-200ms ease-out, bounce/spring 없음
- [editorial+calm] color: 타이포그래피로 위계 형성, 컬러보다 weight/size 활용 + 중성 톤 위주, accent는 최소한으로

### 레퍼런스 근거

- **Primer**: Alla Kholmatova’s Design Systems book was one of the first resources I came across in this area and it broadened my understanding greatly. The work...

### 구현 노트

- 기존에 같은 역할의 컴포넌트가 있으면 토큰 교체부터 시작
- variant prop으로 시각적 변형을 관리 (하드코딩 금지)
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

- [editorial+calm] density: 넉넉한 line-height와 margin, 읽기 편한 간격 + comfortable 모드 기본, 여유로운 padding
- [editorial+calm] color: 타이포그래피로 위계 형성, 컬러보다 weight/size 활용 + 중성 톤 위주, accent는 최소한으로

### Visual Adaptation Hints

- **card_elevation_tendency**: 카드는 낮은 elevation만 허용하고 색면 차이로 그룹을 구분한다. 내부 여백은 넉넉하게 두고 card breathing room을 확보한다. (source=cards; confidence=0.29; provenance=inferred; direction=low-elevation tinted cards를 기본으로 하고, 넓은 내부 여백과 강한 section breathing room. 중간 반경으로 제품 UI 절제 유지.; evidence=surface=tinted, density=airy, corner=medium)
- **border_vs_fill_emphasis**: fill 중심이다. tint surface로 성격을 만들고 border는 아주 얇게 보조한다. (source=cards; confidence=0.29; provenance=inferred; direction=low-elevation tinted cards를 기본으로 하고, 넓은 내부 여백과 강한 section breathing room. 중간 반경으로 제품 UI 절제 유지.; evidence=surface=tinted, density=airy, corner=medium)
- **chart_panel_framing**: 차트 패널은 soft tint frame과 restrained divider로 프레이밍한다. 헤더 메타데이터와 본문 visualization 사이의 breathing room을 충분히 둔다. (source=data_display; confidence=0.29; provenance=inferred; direction=정보 밀도를 유지하되 thin dividers와 restrained accent로 hierarchy를 만든다.; evidence=layout=dashboard-grid, density=airy, layout=landing-narrative, surface=tinted)

### 레퍼런스 근거

- **Primer**: Avatar Avatar is an image that represents a user or organization.

### 구현 노트

- 기존에 같은 역할의 컴포넌트가 있으면 토큰 교체부터 시작
- variant prop으로 시각적 변형을 관리 (하드코딩 금지)
- 빈 상태(empty-state)와 에러 상태를 반드시 처리
- 좁은 UI 텍스트는 Pretendard 기준 label line-height 1.4-1.5를 참고해 뭉침을 방지
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

- [editorial+calm] motion: 콘텐츠 전환 위주, UI chrome 모션 최소화 + 150-200ms ease-out, bounce/spring 없음
- [editorial+calm] density: 넉넉한 line-height와 margin, 읽기 편한 간격 + comfortable 모드 기본, 여유로운 padding

### Visual Adaptation Hints

- **filter_nav_density**: filter/nav density는 low다. top nav는 가볍게 유지하고 filter controls는 별도 섹션 또는 로컬 toolbar로 분리한다. (source=navigation; confidence=0.29; provenance=inferred; direction=top navigation은 가볍게 유지하고 CTA와 section anchors를 분명하게 분리한다.; evidence=Narrative landing flow, layout=landing-narrative, density=airy)

### 레퍼런스 근거

- **Primer**: ActionMenu is composed of ActionList and Overlay patterns used for quick actions and selections. AnchoredOverlay

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

- [editorial+calm] density: 넉넉한 line-height와 margin, 읽기 편한 간격 + comfortable 모드 기본, 여유로운 padding
- [editorial+calm] color: 타이포그래피로 위계 형성, 컬러보다 weight/size 활용 + 중성 톤 위주, accent는 최소한으로

### Visual Adaptation Hints

- **card_elevation_tendency**: 카드는 낮은 elevation만 허용하고 색면 차이로 그룹을 구분한다. 내부 여백은 넉넉하게 두고 card breathing room을 확보한다. (source=cards; confidence=0.29; provenance=inferred; direction=low-elevation tinted cards를 기본으로 하고, 넓은 내부 여백과 강한 section breathing room. 중간 반경으로 제품 UI 절제 유지.; evidence=surface=tinted, density=airy, corner=medium)
- **border_vs_fill_emphasis**: fill 중심이다. tint surface로 성격을 만들고 border는 아주 얇게 보조한다. (source=cards; confidence=0.29; provenance=inferred; direction=low-elevation tinted cards를 기본으로 하고, 넓은 내부 여백과 강한 section breathing room. 중간 반경으로 제품 UI 절제 유지.; evidence=surface=tinted, density=airy, corner=medium)
- **chart_panel_framing**: 차트 패널은 soft tint frame과 restrained divider로 프레이밍한다. 헤더 메타데이터와 본문 visualization 사이의 breathing room을 충분히 둔다. (source=data_display; confidence=0.29; provenance=inferred; direction=정보 밀도를 유지하되 thin dividers와 restrained accent로 hierarchy를 만든다.; evidence=layout=dashboard-grid, density=airy, layout=landing-narrative, surface=tinted)

### 구현 노트

- 기존에 같은 역할의 컴포넌트가 있으면 토큰 교체부터 시작
- variant prop으로 시각적 변형을 관리 (하드코딩 금지)
- 빈 상태(empty-state)와 에러 상태를 반드시 처리
- 좁은 UI 텍스트는 Pretendard 기준 label line-height 1.4-1.5를 참고해 뭉침을 방지
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

- [editorial+calm] feedback: 콘텐츠 맥락 안에서 인라인 표시, 토스트보다 인라인 선호 + subtle inline alert 선호, 과한 컬러 블록 지양
- [editorial+calm] motion: 콘텐츠 전환 위주, UI chrome 모션 최소화 + 150-200ms ease-out, bounce/spring 없음
- [editorial+calm] color: 타이포그래피로 위계 형성, 컬러보다 weight/size 활용 + 중성 톤 위주, accent는 최소한으로

### 레퍼런스 근거

- **Carbon Design System**: We welcome all feedback, designs, or ideas in order to produce the best possible experience for our users. If you're interested in contributing, ch...
- **Primer**: Messaging components are used to provide important and relevant information to the user, including feedback, contextual information, product update...

### 구현 노트

- 기존에 같은 역할의 컴포넌트가 있으면 토큰 교체부터 시작
- variant prop으로 시각적 변형을 관리 (하드코딩 금지)
- auto-dismiss 시간은 내용 길이에 비례 (기본 5초)
- 반응형 검증: 320px, 360px, 390px, 430px에서 control overflow와 viewport horizontal scroll이 없어야 함
- action row는 narrow viewport에서 `flex-wrap: wrap` 또는 세로 stack으로 전환하고, overflow-x 숨김으로 문제를 덮지 않음
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

- [editorial+calm] feedback: 콘텐츠 맥락 안에서 인라인 표시, 토스트보다 인라인 선호 + subtle inline alert 선호, 과한 컬러 블록 지양
- [editorial+calm] motion: 콘텐츠 전환 위주, UI chrome 모션 최소화 + 150-200ms ease-out, bounce/spring 없음
- [editorial+calm] color: 타이포그래피로 위계 형성, 컬러보다 weight/size 활용 + 중성 톤 위주, accent는 최소한으로

### 레퍼런스 근거

- **Carbon Design System**: We welcome all feedback, designs, or ideas in order to produce the best possible experience for our users. If you're interested in contributing, ch...
- **Primer**: Messaging components are used to provide important and relevant information to the user, including feedback, contextual information, product update...

### 구현 노트

- 기존에 같은 역할의 컴포넌트가 있으면 토큰 교체부터 시작
- variant prop으로 시각적 변형을 관리 (하드코딩 금지)
- auto-dismiss 시간은 내용 길이에 비례 (기본 5초)
- 반응형 검증: 320px, 360px, 390px, 430px에서 control overflow와 viewport horizontal scroll이 없어야 함
- action row는 narrow viewport에서 `flex-wrap: wrap` 또는 세로 stack으로 전환하고, overflow-x 숨김으로 문제를 덮지 않음
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

- [editorial+calm] feedback: 콘텐츠 맥락 안에서 인라인 표시, 토스트보다 인라인 선호 + subtle inline alert 선호, 과한 컬러 블록 지양
- [editorial+calm] motion: 콘텐츠 전환 위주, UI chrome 모션 최소화 + 150-200ms ease-out, bounce/spring 없음
- [editorial+calm] color: 타이포그래피로 위계 형성, 컬러보다 weight/size 활용 + 중성 톤 위주, accent는 최소한으로

### Visual Adaptation Hints

- **card_elevation_tendency**: 카드는 낮은 elevation만 허용하고 색면 차이로 그룹을 구분한다. 내부 여백은 넉넉하게 두고 card breathing room을 확보한다. (source=cards; confidence=0.29; provenance=inferred; direction=low-elevation tinted cards를 기본으로 하고, 넓은 내부 여백과 강한 section breathing room. 중간 반경으로 제품 UI 절제 유지.; evidence=surface=tinted, density=airy, corner=medium)
- **border_vs_fill_emphasis**: fill 중심이다. tint surface로 성격을 만들고 border는 아주 얇게 보조한다. (source=cards; confidence=0.29; provenance=inferred; direction=low-elevation tinted cards를 기본으로 하고, 넓은 내부 여백과 강한 section breathing room. 중간 반경으로 제품 UI 절제 유지.; evidence=surface=tinted, density=airy, corner=medium)
- **chart_panel_framing**: 차트 패널은 soft tint frame과 restrained divider로 프레이밍한다. 헤더 메타데이터와 본문 visualization 사이의 breathing room을 충분히 둔다. (source=data_display; confidence=0.29; provenance=inferred; direction=정보 밀도를 유지하되 thin dividers와 restrained accent로 hierarchy를 만든다.; evidence=layout=dashboard-grid, density=airy, layout=landing-narrative, surface=tinted)

### 레퍼런스 근거

- **Carbon Design System**: We welcome all feedback, designs, or ideas in order to produce the best possible experience for our users. If you're interested in contributing, ch...
- **Primer**: Empty states Empty states are used to fill spaces when no content has been added yet, or is temporarily empty due to the nature of the feature.

### 구현 노트

- 기존에 같은 역할의 컴포넌트가 있으면 토큰 교체부터 시작
- variant prop으로 시각적 변형을 관리 (하드코딩 금지)
- auto-dismiss 시간은 내용 길이에 비례 (기본 5초)
- 반응형 검증: 320px, 360px, 390px, 430px에서 control overflow와 viewport horizontal scroll이 없어야 함
- action row는 narrow viewport에서 `flex-wrap: wrap` 또는 세로 stack으로 전환하고, overflow-x 숨김으로 문제를 덮지 않음
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

- [editorial+calm] feedback: 콘텐츠 맥락 안에서 인라인 표시, 토스트보다 인라인 선호 + subtle inline alert 선호, 과한 컬러 블록 지양
- [editorial+calm] motion: 콘텐츠 전환 위주, UI chrome 모션 최소화 + 150-200ms ease-out, bounce/spring 없음
- [editorial+calm] color: 타이포그래피로 위계 형성, 컬러보다 weight/size 활용 + 중성 톤 위주, accent는 최소한으로

### Visual Adaptation Hints

- **card_elevation_tendency**: 카드는 낮은 elevation만 허용하고 색면 차이로 그룹을 구분한다. 내부 여백은 넉넉하게 두고 card breathing room을 확보한다. (source=cards; confidence=0.29; provenance=inferred; direction=low-elevation tinted cards를 기본으로 하고, 넓은 내부 여백과 강한 section breathing room. 중간 반경으로 제품 UI 절제 유지.; evidence=surface=tinted, density=airy, corner=medium)
- **border_vs_fill_emphasis**: fill 중심이다. tint surface로 성격을 만들고 border는 아주 얇게 보조한다. (source=cards; confidence=0.29; provenance=inferred; direction=low-elevation tinted cards를 기본으로 하고, 넓은 내부 여백과 강한 section breathing room. 중간 반경으로 제품 UI 절제 유지.; evidence=surface=tinted, density=airy, corner=medium)

### 레퍼런스 근거

- **Carbon Design System**: We welcome all feedback, designs, or ideas in order to produce the best possible experience for our users. If you're interested in contributing, ch...
- **Primer**: Banner Banner is used to highlight important information.

### 구현 노트

- 기존에 같은 역할의 컴포넌트가 있으면 토큰 교체부터 시작
- variant prop으로 시각적 변형을 관리 (하드코딩 금지)
- auto-dismiss 시간은 내용 길이에 비례 (기본 5초)
- 반응형 검증: 320px, 360px, 390px, 430px에서 control overflow와 viewport horizontal scroll이 없어야 함
- action row는 narrow viewport에서 `flex-wrap: wrap` 또는 세로 stack으로 전환하고, overflow-x 숨김으로 문제를 덮지 않음
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

- [editorial+calm] density: 넉넉한 line-height와 margin, 읽기 편한 간격 + comfortable 모드 기본, 여유로운 padding
- [editorial+calm] color: 타이포그래피로 위계 형성, 컬러보다 weight/size 활용 + 중성 톤 위주, accent는 최소한으로

### Visual Adaptation Hints

- **card_elevation_tendency**: 카드는 낮은 elevation만 허용하고 색면 차이로 그룹을 구분한다. 내부 여백은 넉넉하게 두고 card breathing room을 확보한다. (source=cards; confidence=0.29; provenance=inferred; direction=low-elevation tinted cards를 기본으로 하고, 넓은 내부 여백과 강한 section breathing room. 중간 반경으로 제품 UI 절제 유지.; evidence=surface=tinted, density=airy, corner=medium)
- **border_vs_fill_emphasis**: fill 중심이다. tint surface로 성격을 만들고 border는 아주 얇게 보조한다. (source=cards; confidence=0.29; provenance=inferred; direction=low-elevation tinted cards를 기본으로 하고, 넓은 내부 여백과 강한 section breathing room. 중간 반경으로 제품 UI 절제 유지.; evidence=surface=tinted, density=airy, corner=medium)
- **chart_panel_framing**: 차트 패널은 soft tint frame과 restrained divider로 프레이밍한다. 헤더 메타데이터와 본문 visualization 사이의 breathing room을 충분히 둔다. (source=data_display; confidence=0.29; provenance=inferred; direction=정보 밀도를 유지하되 thin dividers와 restrained accent로 hierarchy를 만든다.; evidence=layout=dashboard-grid, density=airy, layout=landing-narrative, surface=tinted)

### 구현 노트

- 기존에 같은 역할의 컴포넌트가 있으면 토큰 교체부터 시작
- variant prop으로 시각적 변형을 관리 (하드코딩 금지)
- 빈 상태(empty-state)와 에러 상태를 반드시 처리
- 좁은 UI 텍스트는 Pretendard 기준 label line-height 1.4-1.5를 참고해 뭉침을 방지
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

- [editorial+calm] density: 넉넉한 line-height와 margin, 읽기 편한 간격 + comfortable 모드 기본, 여유로운 padding
- [editorial+calm] color: 타이포그래피로 위계 형성, 컬러보다 weight/size 활용 + 중성 톤 위주, accent는 최소한으로

### Visual Adaptation Hints

- **card_elevation_tendency**: 카드는 낮은 elevation만 허용하고 색면 차이로 그룹을 구분한다. 내부 여백은 넉넉하게 두고 card breathing room을 확보한다. (source=cards; confidence=0.29; provenance=inferred; direction=low-elevation tinted cards를 기본으로 하고, 넓은 내부 여백과 강한 section breathing room. 중간 반경으로 제품 UI 절제 유지.; evidence=surface=tinted, density=airy, corner=medium)
- **border_vs_fill_emphasis**: fill 중심이다. tint surface로 성격을 만들고 border는 아주 얇게 보조한다. (source=cards; confidence=0.29; provenance=inferred; direction=low-elevation tinted cards를 기본으로 하고, 넓은 내부 여백과 강한 section breathing room. 중간 반경으로 제품 UI 절제 유지.; evidence=surface=tinted, density=airy, corner=medium)
- **chart_panel_framing**: 차트 패널은 soft tint frame과 restrained divider로 프레이밍한다. 헤더 메타데이터와 본문 visualization 사이의 breathing room을 충분히 둔다. (source=data_display; confidence=0.29; provenance=inferred; direction=정보 밀도를 유지하되 thin dividers와 restrained accent로 hierarchy를 만든다.; evidence=layout=dashboard-grid, density=airy, layout=landing-narrative, surface=tinted)

### 구현 노트

- 기존에 같은 역할의 컴포넌트가 있으면 토큰 교체부터 시작
- variant prop으로 시각적 변형을 관리 (하드코딩 금지)
- 빈 상태(empty-state)와 에러 상태를 반드시 처리
- 좁은 UI 텍스트는 Pretendard 기준 label line-height 1.4-1.5를 참고해 뭉침을 방지
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

- [editorial+calm] density: 넉넉한 line-height와 margin, 읽기 편한 간격 + comfortable 모드 기본, 여유로운 padding
- [editorial+calm] color: 타이포그래피로 위계 형성, 컬러보다 weight/size 활용 + 중성 톤 위주, accent는 최소한으로

### Visual Adaptation Hints

- **card_elevation_tendency**: 카드는 낮은 elevation만 허용하고 색면 차이로 그룹을 구분한다. 내부 여백은 넉넉하게 두고 card breathing room을 확보한다. (source=cards; confidence=0.29; provenance=inferred; direction=low-elevation tinted cards를 기본으로 하고, 넓은 내부 여백과 강한 section breathing room. 중간 반경으로 제품 UI 절제 유지.; evidence=surface=tinted, density=airy, corner=medium)
- **border_vs_fill_emphasis**: fill 중심이다. tint surface로 성격을 만들고 border는 아주 얇게 보조한다. (source=cards; confidence=0.29; provenance=inferred; direction=low-elevation tinted cards를 기본으로 하고, 넓은 내부 여백과 강한 section breathing room. 중간 반경으로 제품 UI 절제 유지.; evidence=surface=tinted, density=airy, corner=medium)
- **chart_panel_framing**: 차트 패널은 soft tint frame과 restrained divider로 프레이밍한다. 헤더 메타데이터와 본문 visualization 사이의 breathing room을 충분히 둔다. (source=data_display; confidence=0.29; provenance=inferred; direction=정보 밀도를 유지하되 thin dividers와 restrained accent로 hierarchy를 만든다.; evidence=layout=dashboard-grid, density=airy, layout=landing-narrative, surface=tinted)

### 구현 노트

- 기존에 같은 역할의 컴포넌트가 있으면 토큰 교체부터 시작
- variant prop으로 시각적 변형을 관리 (하드코딩 금지)
- 빈 상태(empty-state)와 에러 상태를 반드시 처리
- 좁은 UI 텍스트는 Pretendard 기준 label line-height 1.4-1.5를 참고해 뭉침을 방지
- 애니메이션은 상태 설명용으로만 사용, 장식 효과 금지
- 텍스트 위계가 핵심 — 컬러보다 weight/size로 구분

---

## magazine / masthead

**역할**: issue masthead — 잡지 제호 · 로고 · issue 번호 · 표지 링크

**탐지 출처**: bold editorial magazine

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

- [editorial+calm] hover: 텍스트 underline 또는 color shift, 장식적 효과 없음 + opacity 변화 (0.08-0.12), elevation 변화 없음
- [editorial+calm] motion: 콘텐츠 전환 위주, UI chrome 모션 최소화 + 150-200ms ease-out, bounce/spring 없음
- [editorial+calm] color: 타이포그래피로 위계 형성, 컬러보다 weight/size 활용 + 중성 톤 위주, accent는 최소한으로

### 레퍼런스 근거

- **Primer**: Alla Kholmatova’s Design Systems book was one of the first resources I came across in this area and it broadened my understanding greatly. The work...

### 구현 노트

- 기존에 같은 역할의 컴포넌트가 있으면 토큰 교체부터 시작
- variant prop으로 시각적 변형을 관리 (하드코딩 금지)
- 애니메이션은 상태 설명용으로만 사용, 장식 효과 금지
- 텍스트 위계가 핵심 — 컬러보다 weight/size로 구분

---

## magazine / issue-header

**역할**: 이슈 헤더 — issue title · 발행일 · 권/호 · 주요 섹션 jump

**탐지 출처**: bold editorial magazine

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

- [editorial+calm] hover: 텍스트 underline 또는 color shift, 장식적 효과 없음 + opacity 변화 (0.08-0.12), elevation 변화 없음
- [editorial+calm] motion: 콘텐츠 전환 위주, UI chrome 모션 최소화 + 150-200ms ease-out, bounce/spring 없음
- [editorial+calm] color: 타이포그래피로 위계 형성, 컬러보다 weight/size 활용 + 중성 톤 위주, accent는 최소한으로

### 레퍼런스 근거

- **Primer**: Alla Kholmatova’s Design Systems book was one of the first resources I came across in this area and it broadened my understanding greatly. The work...

### 구현 노트

- 기존에 같은 역할의 컴포넌트가 있으면 토큰 교체부터 시작
- variant prop으로 시각적 변형을 관리 (하드코딩 금지)
- 애니메이션은 상태 설명용으로만 사용, 장식 효과 금지
- 텍스트 위계가 핵심 — 컬러보다 weight/size로 구분

---

## magazine / issue-number

**역할**: issue 번호 칩 — mono tabular-nums, bold accent

**탐지 출처**: bold editorial magazine

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

- [editorial+calm] hover: 텍스트 underline 또는 color shift, 장식적 효과 없음 + opacity 변화 (0.08-0.12), elevation 변화 없음
- [editorial+calm] motion: 콘텐츠 전환 위주, UI chrome 모션 최소화 + 150-200ms ease-out, bounce/spring 없음
- [editorial+calm] color: 타이포그래피로 위계 형성, 컬러보다 weight/size 활용 + 중성 톤 위주, accent는 최소한으로

### 레퍼런스 근거

- **Primer**: Alla Kholmatova’s Design Systems book was one of the first resources I came across in this area and it broadened my understanding greatly. The work...

### 구현 노트

- 기존에 같은 역할의 컴포넌트가 있으면 토큰 교체부터 시작
- variant prop으로 시각적 변형을 관리 (하드코딩 금지)
- 애니메이션은 상태 설명용으로만 사용, 장식 효과 금지
- 텍스트 위계가 핵심 — 컬러보다 weight/size로 구분

---

## magazine / cover-story

**역할**: 표지 feature cover story — full-bleed hero + kicker + headline + byline

**탐지 출처**: bold editorial magazine

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

- [editorial+calm] hover: 텍스트 underline 또는 color shift, 장식적 효과 없음 + opacity 변화 (0.08-0.12), elevation 변화 없음
- [editorial+calm] motion: 콘텐츠 전환 위주, UI chrome 모션 최소화 + 150-200ms ease-out, bounce/spring 없음
- [editorial+calm] color: 타이포그래피로 위계 형성, 컬러보다 weight/size 활용 + 중성 톤 위주, accent는 최소한으로

### 레퍼런스 근거

- **Primer**: Alla Kholmatova’s Design Systems book was one of the first resources I came across in this area and it broadened my understanding greatly. The work...

### 구현 노트

- 기존에 같은 역할의 컴포넌트가 있으면 토큰 교체부터 시작
- variant prop으로 시각적 변형을 관리 (하드코딩 금지)
- 애니메이션은 상태 설명용으로만 사용, 장식 효과 금지
- 텍스트 위계가 핵심 — 컬러보다 weight/size로 구분

---

## magazine / opening-spread

**역할**: 기사 opening spread — drop cap 시작 · pull quote · 여백 많은 bold 레이아웃

**탐지 출처**: bold editorial magazine

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

- [editorial+calm] hover: 텍스트 underline 또는 color shift, 장식적 효과 없음 + opacity 변화 (0.08-0.12), elevation 변화 없음
- [editorial+calm] motion: 콘텐츠 전환 위주, UI chrome 모션 최소화 + 150-200ms ease-out, bounce/spring 없음
- [editorial+calm] color: 타이포그래피로 위계 형성, 컬러보다 weight/size 활용 + 중성 톤 위주, accent는 최소한으로

### 레퍼런스 근거

- **Primer**: Alla Kholmatova’s Design Systems book was one of the first resources I came across in this area and it broadened my understanding greatly. The work...

### 구현 노트

- 기존에 같은 역할의 컴포넌트가 있으면 토큰 교체부터 시작
- variant prop으로 시각적 변형을 관리 (하드코딩 금지)
- 애니메이션은 상태 설명용으로만 사용, 장식 효과 금지
- 텍스트 위계가 핵심 — 컬러보다 weight/size로 구분

---

## magazine / feature-article

**역할**: feature article 본체 — article-body + pull-quote + drop-cap + section-break + heading-anchor + prose-block + reading-pane long-form

**탐지 출처**: bold editorial magazine

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

- [editorial+calm] hover: 텍스트 underline 또는 color shift, 장식적 효과 없음 + opacity 변화 (0.08-0.12), elevation 변화 없음
- [editorial+calm] motion: 콘텐츠 전환 위주, UI chrome 모션 최소화 + 150-200ms ease-out, bounce/spring 없음
- [editorial+calm] color: 타이포그래피로 위계 형성, 컬러보다 weight/size 활용 + 중성 톤 위주, accent는 최소한으로

### 레퍼런스 근거

- **Primer**: Alla Kholmatova’s Design Systems book was one of the first resources I came across in this area and it broadened my understanding greatly. The work...

### 구현 노트

- 기존에 같은 역할의 컴포넌트가 있으면 토큰 교체부터 시작
- variant prop으로 시각적 변형을 관리 (하드코딩 금지)
- 애니메이션은 상태 설명용으로만 사용, 장식 효과 금지
- 텍스트 위계가 핵심 — 컬러보다 weight/size로 구분

---

## magazine / kicker-eyebrow

**역할**: 기사 kicker eyebrow — headline 위 카테고리/섹션 라벨, letter-spacing tight

**탐지 출처**: bold editorial magazine

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

- [editorial+calm] hover: 텍스트 underline 또는 color shift, 장식적 효과 없음 + opacity 변화 (0.08-0.12), elevation 변화 없음
- [editorial+calm] motion: 콘텐츠 전환 위주, UI chrome 모션 최소화 + 150-200ms ease-out, bounce/spring 없음
- [editorial+calm] color: 타이포그래피로 위계 형성, 컬러보다 weight/size 활용 + 중성 톤 위주, accent는 최소한으로

### 레퍼런스 근거

- **Primer**: Alla Kholmatova’s Design Systems book was one of the first resources I came across in this area and it broadened my understanding greatly. The work...

### 구현 노트

- 기존에 같은 역할의 컴포넌트가 있으면 토큰 교체부터 시작
- variant prop으로 시각적 변형을 관리 (하드코딩 금지)
- 애니메이션은 상태 설명용으로만 사용, 장식 효과 금지
- 텍스트 위계가 핵심 — 컬러보다 weight/size로 구분

---

## magazine / pull-quote

**역할**: bold pull quote block — oversized serif/sans, saturated accent rule

**탐지 출처**: bold editorial magazine

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

- [editorial+calm] hover: 텍스트 underline 또는 color shift, 장식적 효과 없음 + opacity 변화 (0.08-0.12), elevation 변화 없음
- [editorial+calm] motion: 콘텐츠 전환 위주, UI chrome 모션 최소화 + 150-200ms ease-out, bounce/spring 없음
- [editorial+calm] color: 타이포그래피로 위계 형성, 컬러보다 weight/size 활용 + 중성 톤 위주, accent는 최소한으로

### 레퍼런스 근거

- **Primer**: Alla Kholmatova’s Design Systems book was one of the first resources I came across in this area and it broadened my understanding greatly. The work...

### 구현 노트

- 기존에 같은 역할의 컴포넌트가 있으면 토큰 교체부터 시작
- variant prop으로 시각적 변형을 관리 (하드코딩 금지)
- 애니메이션은 상태 설명용으로만 사용, 장식 효과 금지
- 텍스트 위계가 핵심 — 컬러보다 weight/size로 구분

---

## magazine / drop-cap

**역할**: 기사 첫 문단 drop cap — 3–4 line initial letter, impact

**탐지 출처**: bold editorial magazine

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

- [editorial+calm] hover: 텍스트 underline 또는 color shift, 장식적 효과 없음 + opacity 변화 (0.08-0.12), elevation 변화 없음
- [editorial+calm] motion: 콘텐츠 전환 위주, UI chrome 모션 최소화 + 150-200ms ease-out, bounce/spring 없음
- [editorial+calm] color: 타이포그래피로 위계 형성, 컬러보다 weight/size 활용 + 중성 톤 위주, accent는 최소한으로

### 레퍼런스 근거

- **Primer**: Alla Kholmatova’s Design Systems book was one of the first resources I came across in this area and it broadened my understanding greatly. The work...

### 구현 노트

- 기존에 같은 역할의 컴포넌트가 있으면 토큰 교체부터 시작
- variant prop으로 시각적 변형을 관리 (하드코딩 금지)
- 애니메이션은 상태 설명용으로만 사용, 장식 효과 금지
- 텍스트 위계가 핵심 — 컬러보다 weight/size로 구분

---

## magazine / section-break

**역할**: article 내 section break — chunky divider rule + ornament glyph

**탐지 출처**: bold editorial magazine

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

- [editorial+calm] hover: 텍스트 underline 또는 color shift, 장식적 효과 없음 + opacity 변화 (0.08-0.12), elevation 변화 없음
- [editorial+calm] motion: 콘텐츠 전환 위주, UI chrome 모션 최소화 + 150-200ms ease-out, bounce/spring 없음
- [editorial+calm] color: 타이포그래피로 위계 형성, 컬러보다 weight/size 활용 + 중성 톤 위주, accent는 최소한으로

### 레퍼런스 근거

- **Primer**: Alla Kholmatova’s Design Systems book was one of the first resources I came across in this area and it broadened my understanding greatly. The work...

### 구현 노트

- 기존에 같은 역할의 컴포넌트가 있으면 토큰 교체부터 시작
- variant prop으로 시각적 변형을 관리 (하드코딩 금지)
- 애니메이션은 상태 설명용으로만 사용, 장식 효과 금지
- 텍스트 위계가 핵심 — 컬러보다 weight/size로 구분

---

## magazine / article-gallery

**역할**: 기사 내 이미지 갤러리 — full-bleed / caption / credit-line

**탐지 출처**: bold editorial magazine

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

- [editorial+calm] hover: 텍스트 underline 또는 color shift, 장식적 효과 없음 + opacity 변화 (0.08-0.12), elevation 변화 없음
- [editorial+calm] motion: 콘텐츠 전환 위주, UI chrome 모션 최소화 + 150-200ms ease-out, bounce/spring 없음
- [editorial+calm] color: 타이포그래피로 위계 형성, 컬러보다 weight/size 활용 + 중성 톤 위주, accent는 최소한으로

### 레퍼런스 근거

- **Primer**: Alla Kholmatova’s Design Systems book was one of the first resources I came across in this area and it broadened my understanding greatly. The work...

### 구현 노트

- 기존에 같은 역할의 컴포넌트가 있으면 토큰 교체부터 시작
- variant prop으로 시각적 변형을 관리 (하드코딩 금지)
- 애니메이션은 상태 설명용으로만 사용, 장식 효과 금지
- 텍스트 위계가 핵심 — 컬러보다 weight/size로 구분

---

## magazine / subscription-callout

**역할**: 구독 유도 callout — bold offer copy + CTA, article 하단 / sidebar

**탐지 출처**: bold editorial magazine

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

- [editorial+calm] hover: 텍스트 underline 또는 color shift, 장식적 효과 없음 + opacity 변화 (0.08-0.12), elevation 변화 없음
- [editorial+calm] motion: 콘텐츠 전환 위주, UI chrome 모션 최소화 + 150-200ms ease-out, bounce/spring 없음
- [editorial+calm] color: 타이포그래피로 위계 형성, 컬러보다 weight/size 활용 + 중성 톤 위주, accent는 최소한으로

### 레퍼런스 근거

- **Primer**: Alla Kholmatova’s Design Systems book was one of the first resources I came across in this area and it broadened my understanding greatly. The work...

### 구현 노트

- 기존에 같은 역할의 컴포넌트가 있으면 토큰 교체부터 시작
- variant prop으로 시각적 변형을 관리 (하드코딩 금지)
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

- [editorial+calm] hover: 텍스트 underline 또는 color shift, 장식적 효과 없음 + opacity 변화 (0.08-0.12), elevation 변화 없음
- [editorial+calm] density: 넉넉한 line-height와 margin, 읽기 편한 간격 + comfortable 모드 기본, 여유로운 padding
- [editorial+calm] motion: 콘텐츠 전환 위주, UI chrome 모션 최소화 + 150-200ms ease-out, bounce/spring 없음

### Visual Adaptation Hints

- **filter_nav_density**: filter/nav density는 low다. top nav는 가볍게 유지하고 filter controls는 별도 섹션 또는 로컬 toolbar로 분리한다. (source=navigation; confidence=0.29; provenance=inferred; direction=top navigation은 가볍게 유지하고 CTA와 section anchors를 분명하게 분리한다.; evidence=Narrative landing flow, layout=landing-narrative, density=airy)

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

- [editorial+calm] hover: 텍스트 underline 또는 color shift, 장식적 효과 없음 + opacity 변화 (0.08-0.12), elevation 변화 없음
- [editorial+calm] density: 넉넉한 line-height와 margin, 읽기 편한 간격 + comfortable 모드 기본, 여유로운 padding
- [editorial+calm] motion: 콘텐츠 전환 위주, UI chrome 모션 최소화 + 150-200ms ease-out, bounce/spring 없음

### Visual Adaptation Hints

- **filter_nav_density**: filter/nav density는 low다. top nav는 가볍게 유지하고 filter controls는 별도 섹션 또는 로컬 toolbar로 분리한다. (source=navigation; confidence=0.29; provenance=inferred; direction=top navigation은 가볍게 유지하고 CTA와 section anchors를 분명하게 분리한다.; evidence=Narrative landing flow, layout=landing-narrative, density=airy)

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

- [editorial+calm] hover: 텍스트 underline 또는 color shift, 장식적 효과 없음 + opacity 변화 (0.08-0.12), elevation 변화 없음
- [editorial+calm] density: 넉넉한 line-height와 margin, 읽기 편한 간격 + comfortable 모드 기본, 여유로운 padding
- [editorial+calm] motion: 콘텐츠 전환 위주, UI chrome 모션 최소화 + 150-200ms ease-out, bounce/spring 없음

### Visual Adaptation Hints

- **filter_nav_density**: filter/nav density는 low다. top nav는 가볍게 유지하고 filter controls는 별도 섹션 또는 로컬 toolbar로 분리한다. (source=navigation; confidence=0.29; provenance=inferred; direction=top navigation은 가볍게 유지하고 CTA와 section anchors를 분명하게 분리한다.; evidence=Narrative landing flow, layout=landing-narrative, density=airy)

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

- [editorial+calm] hover: 텍스트 underline 또는 color shift, 장식적 효과 없음 + opacity 변화 (0.08-0.12), elevation 변화 없음
- [editorial+calm] density: 넉넉한 line-height와 margin, 읽기 편한 간격 + comfortable 모드 기본, 여유로운 padding
- [editorial+calm] motion: 콘텐츠 전환 위주, UI chrome 모션 최소화 + 150-200ms ease-out, bounce/spring 없음

### Visual Adaptation Hints

- **filter_nav_density**: filter/nav density는 low다. top nav는 가볍게 유지하고 filter controls는 별도 섹션 또는 로컬 toolbar로 분리한다. (source=navigation; confidence=0.29; provenance=inferred; direction=top navigation은 가볍게 유지하고 CTA와 section anchors를 분명하게 분리한다.; evidence=Narrative landing flow, layout=landing-narrative, density=airy)

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

- [editorial+calm] hover: 텍스트 underline 또는 color shift, 장식적 효과 없음 + opacity 변화 (0.08-0.12), elevation 변화 없음
- [editorial+calm] density: 넉넉한 line-height와 margin, 읽기 편한 간격 + comfortable 모드 기본, 여유로운 padding
- [editorial+calm] motion: 콘텐츠 전환 위주, UI chrome 모션 최소화 + 150-200ms ease-out, bounce/spring 없음

### Visual Adaptation Hints

- **filter_nav_density**: filter/nav density는 low다. top nav는 가볍게 유지하고 filter controls는 별도 섹션 또는 로컬 toolbar로 분리한다. (source=navigation; confidence=0.29; provenance=inferred; direction=top navigation은 가볍게 유지하고 CTA와 section anchors를 분명하게 분리한다.; evidence=Narrative landing flow, layout=landing-narrative, density=airy)

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

- [editorial+calm] color: 타이포그래피로 위계 형성, 컬러보다 weight/size 활용 + 중성 톤 위주, accent는 최소한으로
- [editorial+calm] motion: 콘텐츠 전환 위주, UI chrome 모션 최소화 + 150-200ms ease-out, bounce/spring 없음
- [editorial+calm] density: 넉넉한 line-height와 margin, 읽기 편한 간격 + comfortable 모드 기본, 여유로운 padding

### Visual Adaptation Hints

- **filter_nav_density**: filter/nav density는 low다. top nav는 가볍게 유지하고 filter controls는 별도 섹션 또는 로컬 toolbar로 분리한다. (source=navigation; confidence=0.29; provenance=inferred; direction=top navigation은 가볍게 유지하고 CTA와 section anchors를 분명하게 분리한다.; evidence=Narrative landing flow, layout=landing-narrative, density=airy)

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
- 좁은 UI 텍스트는 Pretendard 기준 label line-height 1.4-1.5를 참고해 뭉침을 방지
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

- [editorial+calm] color: 타이포그래피로 위계 형성, 컬러보다 weight/size 활용 + 중성 톤 위주, accent는 최소한으로
- [editorial+calm] motion: 콘텐츠 전환 위주, UI chrome 모션 최소화 + 150-200ms ease-out, bounce/spring 없음
- [editorial+calm] density: 넉넉한 line-height와 margin, 읽기 편한 간격 + comfortable 모드 기본, 여유로운 padding

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
- 좁은 UI 텍스트는 Pretendard 기준 label line-height 1.4-1.5를 참고해 뭉침을 방지
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

- [editorial+calm] color: 타이포그래피로 위계 형성, 컬러보다 weight/size 활용 + 중성 톤 위주, accent는 최소한으로
- [editorial+calm] motion: 콘텐츠 전환 위주, UI chrome 모션 최소화 + 150-200ms ease-out, bounce/spring 없음
- [editorial+calm] density: 넉넉한 line-height와 margin, 읽기 편한 간격 + comfortable 모드 기본, 여유로운 padding

### Visual Adaptation Hints

- **filter_nav_density**: filter/nav density는 low다. top nav는 가볍게 유지하고 filter controls는 별도 섹션 또는 로컬 toolbar로 분리한다. (source=navigation; confidence=0.29; provenance=inferred; direction=top navigation은 가볍게 유지하고 CTA와 section anchors를 분명하게 분리한다.; evidence=Narrative landing flow, layout=landing-narrative, density=airy)

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
- 좁은 UI 텍스트는 Pretendard 기준 label line-height 1.4-1.5를 참고해 뭉침을 방지
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

- [editorial+calm] hover: 텍스트 underline 또는 color shift, 장식적 효과 없음 + opacity 변화 (0.08-0.12), elevation 변화 없음
- [editorial+calm] motion: 콘텐츠 전환 위주, UI chrome 모션 최소화 + 150-200ms ease-out, bounce/spring 없음
- [editorial+calm] color: 타이포그래피로 위계 형성, 컬러보다 weight/size 활용 + 중성 톤 위주, accent는 최소한으로

### Visual Adaptation Hints

- **cta_prominence**: CTA prominence는 strong이다. 섹션당 primary CTA 1개만 fill/accent로 강하게 띄우고 secondary는 조용하게 후퇴시킨다. (source=hero; confidence=0.29; provenance=inferred; direction=대형 hero와 trust strip, CTA cluster를 허용하되 과장된 glass/gradient 효과는 지양한다.; evidence=Narrative landing flow, layout=landing-narrative, density=airy)
- **filter_nav_density**: filter/nav density는 low다. top nav는 가볍게 유지하고 filter controls는 별도 섹션 또는 로컬 toolbar로 분리한다. (source=navigation; confidence=0.29; provenance=inferred; direction=top navigation은 가볍게 유지하고 CTA와 section anchors를 분명하게 분리한다.; evidence=Narrative landing flow, layout=landing-narrative, density=airy)

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

- [editorial+calm] hover: 텍스트 underline 또는 color shift, 장식적 효과 없음 + opacity 변화 (0.08-0.12), elevation 변화 없음
- [editorial+calm] motion: 콘텐츠 전환 위주, UI chrome 모션 최소화 + 150-200ms ease-out, bounce/spring 없음
- [editorial+calm] color: 타이포그래피로 위계 형성, 컬러보다 weight/size 활용 + 중성 톤 위주, accent는 최소한으로

### Visual Adaptation Hints

- **cta_prominence**: CTA prominence는 strong이다. 섹션당 primary CTA 1개만 fill/accent로 강하게 띄우고 secondary는 조용하게 후퇴시킨다. (source=hero; confidence=0.29; provenance=inferred; direction=대형 hero와 trust strip, CTA cluster를 허용하되 과장된 glass/gradient 효과는 지양한다.; evidence=Narrative landing flow, layout=landing-narrative, density=airy)
- **filter_nav_density**: filter/nav density는 low다. top nav는 가볍게 유지하고 filter controls는 별도 섹션 또는 로컬 toolbar로 분리한다. (source=navigation; confidence=0.29; provenance=inferred; direction=top navigation은 가볍게 유지하고 CTA와 section anchors를 분명하게 분리한다.; evidence=Narrative landing flow, layout=landing-narrative, density=airy)

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
- 애니메이션은 상태 설명용으로만 사용, 장식 효과 금지
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

- [editorial+calm] density: 넉넉한 line-height와 margin, 읽기 편한 간격 + comfortable 모드 기본, 여유로운 padding
- [editorial+calm] color: 타이포그래피로 위계 형성, 컬러보다 weight/size 활용 + 중성 톤 위주, accent는 최소한으로

### Visual Adaptation Hints

- **card_elevation_tendency**: 카드는 낮은 elevation만 허용하고 색면 차이로 그룹을 구분한다. 내부 여백은 넉넉하게 두고 card breathing room을 확보한다. (source=cards; confidence=0.29; provenance=inferred; direction=low-elevation tinted cards를 기본으로 하고, 넓은 내부 여백과 강한 section breathing room. 중간 반경으로 제품 UI 절제 유지.; evidence=surface=tinted, density=airy, corner=medium)
- **border_vs_fill_emphasis**: fill 중심이다. tint surface로 성격을 만들고 border는 아주 얇게 보조한다. (source=cards; confidence=0.29; provenance=inferred; direction=low-elevation tinted cards를 기본으로 하고, 넓은 내부 여백과 강한 section breathing room. 중간 반경으로 제품 UI 절제 유지.; evidence=surface=tinted, density=airy, corner=medium)
- **chart_panel_framing**: 차트 패널은 soft tint frame과 restrained divider로 프레이밍한다. 헤더 메타데이터와 본문 visualization 사이의 breathing room을 충분히 둔다. (source=data_display; confidence=0.29; provenance=inferred; direction=정보 밀도를 유지하되 thin dividers와 restrained accent로 hierarchy를 만든다.; evidence=layout=dashboard-grid, density=airy, layout=landing-narrative, surface=tinted)

### 구현 노트

- 기존에 같은 역할의 컴포넌트가 있으면 토큰 교체부터 시작
- variant prop으로 시각적 변형을 관리 (하드코딩 금지)
- 빈 상태(empty-state)와 에러 상태를 반드시 처리
- 좁은 UI 텍스트는 Pretendard 기준 label line-height 1.4-1.5를 참고해 뭉침을 방지
- 애니메이션은 상태 설명용으로만 사용, 장식 효과 금지
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

- [editorial+calm] motion: 콘텐츠 전환 위주, UI chrome 모션 최소화 + 150-200ms ease-out, bounce/spring 없음
- [editorial+calm] density: 넉넉한 line-height와 margin, 읽기 편한 간격 + comfortable 모드 기본, 여유로운 padding

### Visual Adaptation Hints

- **card_elevation_tendency**: 카드는 낮은 elevation만 허용하고 색면 차이로 그룹을 구분한다. 내부 여백은 넉넉하게 두고 card breathing room을 확보한다. (source=cards; confidence=0.29; provenance=inferred; direction=low-elevation tinted cards를 기본으로 하고, 넓은 내부 여백과 강한 section breathing room. 중간 반경으로 제품 UI 절제 유지.; evidence=surface=tinted, density=airy, corner=medium)
- **border_vs_fill_emphasis**: fill 중심이다. tint surface로 성격을 만들고 border는 아주 얇게 보조한다. (source=cards; confidence=0.29; provenance=inferred; direction=low-elevation tinted cards를 기본으로 하고, 넓은 내부 여백과 강한 section breathing room. 중간 반경으로 제품 UI 절제 유지.; evidence=surface=tinted, density=airy, corner=medium)
- **chart_panel_framing**: 차트 패널은 soft tint frame과 restrained divider로 프레이밍한다. 헤더 메타데이터와 본문 visualization 사이의 breathing room을 충분히 둔다. (source=data_display; confidence=0.29; provenance=inferred; direction=정보 밀도를 유지하되 thin dividers와 restrained accent로 hierarchy를 만든다.; evidence=layout=dashboard-grid, density=airy, layout=landing-narrative, surface=tinted)

### 레퍼런스 근거

- **Primer**: ActionMenu is composed of ActionList and Overlay patterns used for quick actions and selections. AnchoredOverlay

### 구현 노트

- 기존에 같은 역할의 컴포넌트가 있으면 토큰 교체부터 시작
- variant prop으로 시각적 변형을 관리 (하드코딩 금지)
- Escape / backdrop click으로 닫기, 열 때 첫 focusable 요소로 이동
- 애니메이션은 상태 설명용으로만 사용, 장식 효과 금지
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

- [editorial+calm] density: 넉넉한 line-height와 margin, 읽기 편한 간격 + comfortable 모드 기본, 여유로운 padding
- [editorial+calm] color: 타이포그래피로 위계 형성, 컬러보다 weight/size 활용 + 중성 톤 위주, accent는 최소한으로

### Visual Adaptation Hints

- **card_elevation_tendency**: 카드는 낮은 elevation만 허용하고 색면 차이로 그룹을 구분한다. 내부 여백은 넉넉하게 두고 card breathing room을 확보한다. (source=cards; confidence=0.29; provenance=inferred; direction=low-elevation tinted cards를 기본으로 하고, 넓은 내부 여백과 강한 section breathing room. 중간 반경으로 제품 UI 절제 유지.; evidence=surface=tinted, density=airy, corner=medium)
- **border_vs_fill_emphasis**: fill 중심이다. tint surface로 성격을 만들고 border는 아주 얇게 보조한다. (source=cards; confidence=0.29; provenance=inferred; direction=low-elevation tinted cards를 기본으로 하고, 넓은 내부 여백과 강한 section breathing room. 중간 반경으로 제품 UI 절제 유지.; evidence=surface=tinted, density=airy, corner=medium)
- **chart_panel_framing**: 차트 패널은 soft tint frame과 restrained divider로 프레이밍한다. 헤더 메타데이터와 본문 visualization 사이의 breathing room을 충분히 둔다. (source=data_display; confidence=0.29; provenance=inferred; direction=정보 밀도를 유지하되 thin dividers와 restrained accent로 hierarchy를 만든다.; evidence=layout=dashboard-grid, density=airy, layout=landing-narrative, surface=tinted)

### 구현 노트

- 기존에 같은 역할의 컴포넌트가 있으면 토큰 교체부터 시작
- variant prop으로 시각적 변형을 관리 (하드코딩 금지)
- 빈 상태(empty-state)와 에러 상태를 반드시 처리
- 좁은 UI 텍스트는 Pretendard 기준 label line-height 1.4-1.5를 참고해 뭉침을 방지
- 애니메이션은 상태 설명용으로만 사용, 장식 효과 금지
- 텍스트 위계가 핵심 — 컬러보다 weight/size로 구분

---

## data-display / video-player

**역할**: 비디오 재생기

**탐지 출처**: media player

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

- [editorial+calm] density: 넉넉한 line-height와 margin, 읽기 편한 간격 + comfortable 모드 기본, 여유로운 padding
- [editorial+calm] color: 타이포그래피로 위계 형성, 컬러보다 weight/size 활용 + 중성 톤 위주, accent는 최소한으로

### Visual Adaptation Hints

- **card_elevation_tendency**: 카드는 낮은 elevation만 허용하고 색면 차이로 그룹을 구분한다. 내부 여백은 넉넉하게 두고 card breathing room을 확보한다. (source=cards; confidence=0.29; provenance=inferred; direction=low-elevation tinted cards를 기본으로 하고, 넓은 내부 여백과 강한 section breathing room. 중간 반경으로 제품 UI 절제 유지.; evidence=surface=tinted, density=airy, corner=medium)
- **border_vs_fill_emphasis**: fill 중심이다. tint surface로 성격을 만들고 border는 아주 얇게 보조한다. (source=cards; confidence=0.29; provenance=inferred; direction=low-elevation tinted cards를 기본으로 하고, 넓은 내부 여백과 강한 section breathing room. 중간 반경으로 제품 UI 절제 유지.; evidence=surface=tinted, density=airy, corner=medium)
- **chart_panel_framing**: 차트 패널은 soft tint frame과 restrained divider로 프레이밍한다. 헤더 메타데이터와 본문 visualization 사이의 breathing room을 충분히 둔다. (source=data_display; confidence=0.29; provenance=inferred; direction=정보 밀도를 유지하되 thin dividers와 restrained accent로 hierarchy를 만든다.; evidence=layout=dashboard-grid, density=airy, layout=landing-narrative, surface=tinted)

### 구현 노트

- 기존에 같은 역할의 컴포넌트가 있으면 토큰 교체부터 시작
- variant prop으로 시각적 변형을 관리 (하드코딩 금지)
- 빈 상태(empty-state)와 에러 상태를 반드시 처리
- 좁은 UI 텍스트는 Pretendard 기준 label line-height 1.4-1.5를 참고해 뭉침을 방지
- 애니메이션은 상태 설명용으로만 사용, 장식 효과 금지
- 텍스트 위계가 핵심 — 컬러보다 weight/size로 구분

---

## button / player-controls

**역할**: 재생/일시정지/시크 컨트롤

**탐지 출처**: media player

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

- [editorial+calm] hover: 텍스트 underline 또는 color shift, 장식적 효과 없음 + opacity 변화 (0.08-0.12), elevation 변화 없음
- [editorial+calm] motion: 콘텐츠 전환 위주, UI chrome 모션 최소화 + 150-200ms ease-out, bounce/spring 없음
- [editorial+calm] color: 타이포그래피로 위계 형성, 컬러보다 weight/size 활용 + 중성 톤 위주, accent는 최소한으로

### Visual Adaptation Hints

- **cta_prominence**: CTA prominence는 strong이다. 섹션당 primary CTA 1개만 fill/accent로 강하게 띄우고 secondary는 조용하게 후퇴시킨다. (source=hero; confidence=0.29; provenance=inferred; direction=대형 hero와 trust strip, CTA cluster를 허용하되 과장된 glass/gradient 효과는 지양한다.; evidence=Narrative landing flow, layout=landing-narrative, density=airy)

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
- 애니메이션은 상태 설명용으로만 사용, 장식 효과 금지
- 텍스트 위계가 핵심 — 컬러보다 weight/size로 구분

---

## input / volume-slider

**역할**: 볼륨 조절 슬라이더

**탐지 출처**: media player

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

- [editorial+calm] hover: 텍스트 underline 또는 color shift, 장식적 효과 없음 + opacity 변화 (0.08-0.12), elevation 변화 없음
- [editorial+calm] density: 넉넉한 line-height와 margin, 읽기 편한 간격 + comfortable 모드 기본, 여유로운 padding
- [editorial+calm] feedback: 콘텐츠 맥락 안에서 인라인 표시, 토스트보다 인라인 선호 + subtle inline alert 선호, 과한 컬러 블록 지양

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

- [editorial+calm] color: 타이포그래피로 위계 형성, 컬러보다 weight/size 활용 + 중성 톤 위주, accent는 최소한으로
- [editorial+calm] motion: 콘텐츠 전환 위주, UI chrome 모션 최소화 + 150-200ms ease-out, bounce/spring 없음
- [editorial+calm] density: 넉넉한 line-height와 margin, 읽기 편한 간격 + comfortable 모드 기본, 여유로운 padding

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
- 좁은 UI 텍스트는 Pretendard 기준 label line-height 1.4-1.5를 참고해 뭉침을 방지
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

- [editorial+calm] color: 타이포그래피로 위계 형성, 컬러보다 weight/size 활용 + 중성 톤 위주, accent는 최소한으로
- [editorial+calm] motion: 콘텐츠 전환 위주, UI chrome 모션 최소화 + 150-200ms ease-out, bounce/spring 없음
- [editorial+calm] density: 넉넉한 line-height와 margin, 읽기 편한 간격 + comfortable 모드 기본, 여유로운 padding

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
- 좁은 UI 텍스트는 Pretendard 기준 label line-height 1.4-1.5를 참고해 뭉침을 방지
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

- [editorial+calm] color: 타이포그래피로 위계 형성, 컬러보다 weight/size 활용 + 중성 톤 위주, accent는 최소한으로
- [editorial+calm] motion: 콘텐츠 전환 위주, UI chrome 모션 최소화 + 150-200ms ease-out, bounce/spring 없음
- [editorial+calm] density: 넉넉한 line-height와 margin, 읽기 편한 간격 + comfortable 모드 기본, 여유로운 padding

### Visual Adaptation Hints

- **card_elevation_tendency**: 카드는 낮은 elevation만 허용하고 색면 차이로 그룹을 구분한다. 내부 여백은 넉넉하게 두고 card breathing room을 확보한다. (source=cards; confidence=0.29; provenance=inferred; direction=low-elevation tinted cards를 기본으로 하고, 넓은 내부 여백과 강한 section breathing room. 중간 반경으로 제품 UI 절제 유지.; evidence=surface=tinted, density=airy, corner=medium)
- **border_vs_fill_emphasis**: fill 중심이다. tint surface로 성격을 만들고 border는 아주 얇게 보조한다. (source=cards; confidence=0.29; provenance=inferred; direction=low-elevation tinted cards를 기본으로 하고, 넓은 내부 여백과 강한 section breathing room. 중간 반경으로 제품 UI 절제 유지.; evidence=surface=tinted, density=airy, corner=medium)
- **chart_panel_framing**: 차트 패널은 soft tint frame과 restrained divider로 프레이밍한다. 헤더 메타데이터와 본문 visualization 사이의 breathing room을 충분히 둔다. (source=data_display; confidence=0.29; provenance=inferred; direction=정보 밀도를 유지하되 thin dividers와 restrained accent로 hierarchy를 만든다.; evidence=layout=dashboard-grid, density=airy, layout=landing-narrative, surface=tinted)

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
- 좁은 UI 텍스트는 Pretendard 기준 label line-height 1.4-1.5를 참고해 뭉침을 방지
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

- [editorial+calm] color: 타이포그래피로 위계 형성, 컬러보다 weight/size 활용 + 중성 톤 위주, accent는 최소한으로
- [editorial+calm] motion: 콘텐츠 전환 위주, UI chrome 모션 최소화 + 150-200ms ease-out, bounce/spring 없음
- [editorial+calm] density: 넉넉한 line-height와 margin, 읽기 편한 간격 + comfortable 모드 기본, 여유로운 padding

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
- 좁은 UI 텍스트는 Pretendard 기준 label line-height 1.4-1.5를 참고해 뭉침을 방지
- 애니메이션은 상태 설명용으로만 사용, 장식 효과 금지
- 텍스트 위계가 핵심 — 컬러보다 weight/size로 구분

---

## commerce / product-grid

**역할**: dense product grid — 카테고리/검색/홈에서 여러 제품 카드를 배치

**탐지 출처**: product catalog

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

- [editorial+calm] hover: 텍스트 underline 또는 color shift, 장식적 효과 없음 + opacity 변화 (0.08-0.12), elevation 변화 없음
- [editorial+calm] motion: 콘텐츠 전환 위주, UI chrome 모션 최소화 + 150-200ms ease-out, bounce/spring 없음
- [editorial+calm] color: 타이포그래피로 위계 형성, 컬러보다 weight/size 활용 + 중성 톤 위주, accent는 최소한으로

### Visual Adaptation Hints

- **card_elevation_tendency**: 카드는 낮은 elevation만 허용하고 색면 차이로 그룹을 구분한다. 내부 여백은 넉넉하게 두고 card breathing room을 확보한다. (source=cards; confidence=0.29; provenance=inferred; direction=low-elevation tinted cards를 기본으로 하고, 넓은 내부 여백과 강한 section breathing room. 중간 반경으로 제품 UI 절제 유지.; evidence=surface=tinted, density=airy, corner=medium)
- **border_vs_fill_emphasis**: fill 중심이다. tint surface로 성격을 만들고 border는 아주 얇게 보조한다. (source=cards; confidence=0.29; provenance=inferred; direction=low-elevation tinted cards를 기본으로 하고, 넓은 내부 여백과 강한 section breathing room. 중간 반경으로 제품 UI 절제 유지.; evidence=surface=tinted, density=airy, corner=medium)
- **chart_panel_framing**: 차트 패널은 soft tint frame과 restrained divider로 프레이밍한다. 헤더 메타데이터와 본문 visualization 사이의 breathing room을 충분히 둔다. (source=data_display; confidence=0.29; provenance=inferred; direction=정보 밀도를 유지하되 thin dividers와 restrained accent로 hierarchy를 만든다.; evidence=layout=dashboard-grid, density=airy, layout=landing-narrative, surface=tinted)

### 구현 노트

- 기존에 같은 역할의 컴포넌트가 있으면 토큰 교체부터 시작
- variant prop으로 시각적 변형을 관리 (하드코딩 금지)
- 애니메이션은 상태 설명용으로만 사용, 장식 효과 금지
- 텍스트 위계가 핵심 — 컬러보다 weight/size로 구분

---

## commerce / product-card

**역할**: 개별 product card — thumbnail + 제품 title + price tag + discount badge + quick-view trigger

**탐지 출처**: product catalog

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

- [editorial+calm] hover: 텍스트 underline 또는 color shift, 장식적 효과 없음 + opacity 변화 (0.08-0.12), elevation 변화 없음
- [editorial+calm] motion: 콘텐츠 전환 위주, UI chrome 모션 최소화 + 150-200ms ease-out, bounce/spring 없음
- [editorial+calm] color: 타이포그래피로 위계 형성, 컬러보다 weight/size 활용 + 중성 톤 위주, accent는 최소한으로

### Visual Adaptation Hints

- **card_elevation_tendency**: 카드는 낮은 elevation만 허용하고 색면 차이로 그룹을 구분한다. 내부 여백은 넉넉하게 두고 card breathing room을 확보한다. (source=cards; confidence=0.29; provenance=inferred; direction=low-elevation tinted cards를 기본으로 하고, 넓은 내부 여백과 강한 section breathing room. 중간 반경으로 제품 UI 절제 유지.; evidence=surface=tinted, density=airy, corner=medium)
- **border_vs_fill_emphasis**: fill 중심이다. tint surface로 성격을 만들고 border는 아주 얇게 보조한다. (source=cards; confidence=0.29; provenance=inferred; direction=low-elevation tinted cards를 기본으로 하고, 넓은 내부 여백과 강한 section breathing room. 중간 반경으로 제품 UI 절제 유지.; evidence=surface=tinted, density=airy, corner=medium)

### 구현 노트

- 기존에 같은 역할의 컴포넌트가 있으면 토큰 교체부터 시작
- variant prop으로 시각적 변형을 관리 (하드코딩 금지)
- 애니메이션은 상태 설명용으로만 사용, 장식 효과 금지
- 텍스트 위계가 핵심 — 컬러보다 weight/size로 구분

---

## commerce / product-detail

**역할**: product detail 화면 컨테이너 — gallery + selectors + add-to-cart + cross-sell

**탐지 출처**: product catalog

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

- [editorial+calm] hover: 텍스트 underline 또는 color shift, 장식적 효과 없음 + opacity 변화 (0.08-0.12), elevation 변화 없음
- [editorial+calm] motion: 콘텐츠 전환 위주, UI chrome 모션 최소화 + 150-200ms ease-out, bounce/spring 없음
- [editorial+calm] color: 타이포그래피로 위계 형성, 컬러보다 weight/size 활용 + 중성 톤 위주, accent는 최소한으로

### 구현 노트

- 기존에 같은 역할의 컴포넌트가 있으면 토큰 교체부터 시작
- variant prop으로 시각적 변형을 관리 (하드코딩 금지)
- 애니메이션은 상태 설명용으로만 사용, 장식 효과 금지
- 텍스트 위계가 핵심 — 컬러보다 weight/size로 구분

---

## commerce / product-gallery

**역할**: 제품 상세 gallery — main image + thumbnail rail, swipe/keyboard 지원

**탐지 출처**: product catalog

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

- [editorial+calm] hover: 텍스트 underline 또는 color shift, 장식적 효과 없음 + opacity 변화 (0.08-0.12), elevation 변화 없음
- [editorial+calm] motion: 콘텐츠 전환 위주, UI chrome 모션 최소화 + 150-200ms ease-out, bounce/spring 없음
- [editorial+calm] color: 타이포그래피로 위계 형성, 컬러보다 weight/size 활용 + 중성 톤 위주, accent는 최소한으로

### 구현 노트

- 기존에 같은 역할의 컴포넌트가 있으면 토큰 교체부터 시작
- variant prop으로 시각적 변형을 관리 (하드코딩 금지)
- 애니메이션은 상태 설명용으로만 사용, 장식 효과 금지
- 텍스트 위계가 핵심 — 컬러보다 weight/size로 구분

---

## commerce / product-hero-image

**역할**: 제품 상세 상단 full-bleed hero image

**탐지 출처**: product catalog

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

- [editorial+calm] hover: 텍스트 underline 또는 color shift, 장식적 효과 없음 + opacity 변화 (0.08-0.12), elevation 변화 없음
- [editorial+calm] motion: 콘텐츠 전환 위주, UI chrome 모션 최소화 + 150-200ms ease-out, bounce/spring 없음
- [editorial+calm] color: 타이포그래피로 위계 형성, 컬러보다 weight/size 활용 + 중성 톤 위주, accent는 최소한으로

### 구현 노트

- 기존에 같은 역할의 컴포넌트가 있으면 토큰 교체부터 시작
- variant prop으로 시각적 변형을 관리 (하드코딩 금지)
- 애니메이션은 상태 설명용으로만 사용, 장식 효과 금지
- 텍스트 위계가 핵심 — 컬러보다 weight/size로 구분

---

## commerce / image-thumbnail

**역할**: 제품 썸네일 이미지 — aspect-ratio fixed, hover zoom

**탐지 출처**: product catalog

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

- [editorial+calm] hover: 텍스트 underline 또는 color shift, 장식적 효과 없음 + opacity 변화 (0.08-0.12), elevation 변화 없음
- [editorial+calm] motion: 콘텐츠 전환 위주, UI chrome 모션 최소화 + 150-200ms ease-out, bounce/spring 없음
- [editorial+calm] color: 타이포그래피로 위계 형성, 컬러보다 weight/size 활용 + 중성 톤 위주, accent는 최소한으로

### 구현 노트

- 기존에 같은 역할의 컴포넌트가 있으면 토큰 교체부터 시작
- variant prop으로 시각적 변형을 관리 (하드코딩 금지)
- 애니메이션은 상태 설명용으로만 사용, 장식 효과 금지
- 텍스트 위계가 핵심 — 컬러보다 weight/size로 구분

---

## input / variant-selector

**역할**: variant (색상/사이즈/모델) 선택기 — segmented chip group

**탐지 출처**: product catalog

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

- [editorial+calm] hover: 텍스트 underline 또는 color shift, 장식적 효과 없음 + opacity 변화 (0.08-0.12), elevation 변화 없음
- [editorial+calm] density: 넉넉한 line-height와 margin, 읽기 편한 간격 + comfortable 모드 기본, 여유로운 padding
- [editorial+calm] feedback: 콘텐츠 맥락 안에서 인라인 표시, 토스트보다 인라인 선호 + subtle inline alert 선호, 과한 컬러 블록 지양

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
- 애니메이션은 상태 설명용으로만 사용, 장식 효과 금지
- 텍스트 위계가 핵심 — 컬러보다 weight/size로 구분

---

## input / size-selector

**역할**: size selector chip (S/M/L/XL) — 품절 state 포함

**탐지 출처**: product catalog

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

- [editorial+calm] hover: 텍스트 underline 또는 color shift, 장식적 효과 없음 + opacity 변화 (0.08-0.12), elevation 변화 없음
- [editorial+calm] density: 넉넉한 line-height와 margin, 읽기 편한 간격 + comfortable 모드 기본, 여유로운 padding
- [editorial+calm] feedback: 콘텐츠 맥락 안에서 인라인 표시, 토스트보다 인라인 선호 + subtle inline alert 선호, 과한 컬러 블록 지양

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
- 애니메이션은 상태 설명용으로만 사용, 장식 효과 금지
- 텍스트 위계가 핵심 — 컬러보다 weight/size로 구분

---

## input / color-swatch-selector

**역할**: color swatch chip 선택기 — 선택 ring 강조

**탐지 출처**: product catalog

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

- [editorial+calm] hover: 텍스트 underline 또는 color shift, 장식적 효과 없음 + opacity 변화 (0.08-0.12), elevation 변화 없음
- [editorial+calm] density: 넉넉한 line-height와 margin, 읽기 편한 간격 + comfortable 모드 기본, 여유로운 padding
- [editorial+calm] feedback: 콘텐츠 맥락 안에서 인라인 표시, 토스트보다 인라인 선호 + subtle inline alert 선호, 과한 컬러 블록 지양

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
- 애니메이션은 상태 설명용으로만 사용, 장식 효과 금지
- 텍스트 위계가 핵심 — 컬러보다 weight/size로 구분

---

## button / add-to-cart-button

**역할**: primary CTA add-to-cart — saturated fill + impact label + bump animation

**탐지 출처**: product catalog

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

- [editorial+calm] hover: 텍스트 underline 또는 color shift, 장식적 효과 없음 + opacity 변화 (0.08-0.12), elevation 변화 없음
- [editorial+calm] motion: 콘텐츠 전환 위주, UI chrome 모션 최소화 + 150-200ms ease-out, bounce/spring 없음
- [editorial+calm] color: 타이포그래피로 위계 형성, 컬러보다 weight/size 활용 + 중성 톤 위주, accent는 최소한으로

### Visual Adaptation Hints

- **cta_prominence**: CTA prominence는 strong이다. 섹션당 primary CTA 1개만 fill/accent로 강하게 띄우고 secondary는 조용하게 후퇴시킨다. (source=hero; confidence=0.29; provenance=inferred; direction=대형 hero와 trust strip, CTA cluster를 허용하되 과장된 glass/gradient 효과는 지양한다.; evidence=Narrative landing flow, layout=landing-narrative, density=airy)

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
- 애니메이션은 상태 설명용으로만 사용, 장식 효과 금지
- 텍스트 위계가 핵심 — 컬러보다 weight/size로 구분

---

## overlay / quick-view-modal

**역할**: product grid 위에서 뜨는 quick-view modal — gallery 축소 + add-to-cart

**탐지 출처**: product catalog

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

- [editorial+calm] motion: 콘텐츠 전환 위주, UI chrome 모션 최소화 + 150-200ms ease-out, bounce/spring 없음
- [editorial+calm] density: 넉넉한 line-height와 margin, 읽기 편한 간격 + comfortable 모드 기본, 여유로운 padding

### 레퍼런스 근거

- **Primer**: ActionMenu is composed of ActionList and Overlay patterns used for quick actions and selections. AnchoredOverlay

### 구현 노트

- 기존에 같은 역할의 컴포넌트가 있으면 토큰 교체부터 시작
- variant prop으로 시각적 변형을 관리 (하드코딩 금지)
- Escape / backdrop click으로 닫기, 열 때 첫 focusable 요소로 이동
- 애니메이션은 상태 설명용으로만 사용, 장식 효과 금지
- 텍스트 위계가 핵심 — 컬러보다 weight/size로 구분

---

## button / wishlist-toggle

**역할**: heart toggle — optimistic update, aria-pressed

**탐지 출처**: product catalog

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

- [editorial+calm] hover: 텍스트 underline 또는 color shift, 장식적 효과 없음 + opacity 변화 (0.08-0.12), elevation 변화 없음
- [editorial+calm] motion: 콘텐츠 전환 위주, UI chrome 모션 최소화 + 150-200ms ease-out, bounce/spring 없음
- [editorial+calm] color: 타이포그래피로 위계 형성, 컬러보다 weight/size 활용 + 중성 톤 위주, accent는 최소한으로

### Visual Adaptation Hints

- **cta_prominence**: CTA prominence는 strong이다. 섹션당 primary CTA 1개만 fill/accent로 강하게 띄우고 secondary는 조용하게 후퇴시킨다. (source=hero; confidence=0.29; provenance=inferred; direction=대형 hero와 trust strip, CTA cluster를 허용하되 과장된 glass/gradient 효과는 지양한다.; evidence=Narrative landing flow, layout=landing-narrative, density=airy)

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
- 애니메이션은 상태 설명용으로만 사용, 장식 효과 금지
- 텍스트 위계가 핵심 — 컬러보다 weight/size로 구분

---

## commerce / price-tag

**역할**: bold price tag — mono tabular-nums, 세일가 강조

**탐지 출처**: product catalog

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

- [editorial+calm] hover: 텍스트 underline 또는 color shift, 장식적 효과 없음 + opacity 변화 (0.08-0.12), elevation 변화 없음
- [editorial+calm] motion: 콘텐츠 전환 위주, UI chrome 모션 최소화 + 150-200ms ease-out, bounce/spring 없음
- [editorial+calm] color: 타이포그래피로 위계 형성, 컬러보다 weight/size 활용 + 중성 톤 위주, accent는 최소한으로

### 구현 노트

- 기존에 같은 역할의 컴포넌트가 있으면 토큰 교체부터 시작
- variant prop으로 시각적 변형을 관리 (하드코딩 금지)
- 애니메이션은 상태 설명용으로만 사용, 장식 효과 금지
- 텍스트 위계가 핵심 — 컬러보다 weight/size로 구분

---

## commerce / original-price-strikethrough

**역할**: 할인 시 원가 strikethrough — muted mono

**탐지 출처**: product catalog

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

- [editorial+calm] hover: 텍스트 underline 또는 color shift, 장식적 효과 없음 + opacity 변화 (0.08-0.12), elevation 변화 없음
- [editorial+calm] motion: 콘텐츠 전환 위주, UI chrome 모션 최소화 + 150-200ms ease-out, bounce/spring 없음
- [editorial+calm] color: 타이포그래피로 위계 형성, 컬러보다 weight/size 활용 + 중성 톤 위주, accent는 최소한으로

### 구현 노트

- 기존에 같은 역할의 컴포넌트가 있으면 토큰 교체부터 시작
- variant prop으로 시각적 변형을 관리 (하드코딩 금지)
- 애니메이션은 상태 설명용으로만 사용, 장식 효과 금지
- 텍스트 위계가 핵심 — 컬러보다 weight/size로 구분

---

## feedback / discount-badge

**역할**: 할인율 badge (-NN% / SALE / HOT / DROP)

**탐지 출처**: product catalog

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

- [editorial+calm] feedback: 콘텐츠 맥락 안에서 인라인 표시, 토스트보다 인라인 선호 + subtle inline alert 선호, 과한 컬러 블록 지양
- [editorial+calm] motion: 콘텐츠 전환 위주, UI chrome 모션 최소화 + 150-200ms ease-out, bounce/spring 없음
- [editorial+calm] color: 타이포그래피로 위계 형성, 컬러보다 weight/size 활용 + 중성 톤 위주, accent는 최소한으로

### 레퍼런스 근거

- **Carbon Design System**: We welcome all feedback, designs, or ideas in order to produce the best possible experience for our users. If you're interested in contributing, ch...
- **Primer**: Messaging components are used to provide important and relevant information to the user, including feedback, contextual information, product update...

### 구현 노트

- 기존에 같은 역할의 컴포넌트가 있으면 토큰 교체부터 시작
- variant prop으로 시각적 변형을 관리 (하드코딩 금지)
- auto-dismiss 시간은 내용 길이에 비례 (기본 5초)
- 반응형 검증: 320px, 360px, 390px, 430px에서 control overflow와 viewport horizontal scroll이 없어야 함
- action row는 narrow viewport에서 `flex-wrap: wrap` 또는 세로 stack으로 전환하고, overflow-x 숨김으로 문제를 덮지 않음
- 애니메이션은 상태 설명용으로만 사용, 장식 효과 금지
- 텍스트 위계가 핵심 — 컬러보다 weight/size로 구분

---

## commerce / cross-sell-grid

**역할**: 제품 상세 하단 추천 product grid (함께 구매 / 비슷한 상품)

**탐지 출처**: product catalog

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

- [editorial+calm] hover: 텍스트 underline 또는 color shift, 장식적 효과 없음 + opacity 변화 (0.08-0.12), elevation 변화 없음
- [editorial+calm] motion: 콘텐츠 전환 위주, UI chrome 모션 최소화 + 150-200ms ease-out, bounce/spring 없음
- [editorial+calm] color: 타이포그래피로 위계 형성, 컬러보다 weight/size 활용 + 중성 톤 위주, accent는 최소한으로

### Visual Adaptation Hints

- **card_elevation_tendency**: 카드는 낮은 elevation만 허용하고 색면 차이로 그룹을 구분한다. 내부 여백은 넉넉하게 두고 card breathing room을 확보한다. (source=cards; confidence=0.29; provenance=inferred; direction=low-elevation tinted cards를 기본으로 하고, 넓은 내부 여백과 강한 section breathing room. 중간 반경으로 제품 UI 절제 유지.; evidence=surface=tinted, density=airy, corner=medium)
- **border_vs_fill_emphasis**: fill 중심이다. tint surface로 성격을 만들고 border는 아주 얇게 보조한다. (source=cards; confidence=0.29; provenance=inferred; direction=low-elevation tinted cards를 기본으로 하고, 넓은 내부 여백과 강한 section breathing room. 중간 반경으로 제품 UI 절제 유지.; evidence=surface=tinted, density=airy, corner=medium)
- **chart_panel_framing**: 차트 패널은 soft tint frame과 restrained divider로 프레이밍한다. 헤더 메타데이터와 본문 visualization 사이의 breathing room을 충분히 둔다. (source=data_display; confidence=0.29; provenance=inferred; direction=정보 밀도를 유지하되 thin dividers와 restrained accent로 hierarchy를 만든다.; evidence=layout=dashboard-grid, density=airy, layout=landing-narrative, surface=tinted)

### 구현 노트

- 기존에 같은 역할의 컴포넌트가 있으면 토큰 교체부터 시작
- variant prop으로 시각적 변형을 관리 (하드코딩 금지)
- 애니메이션은 상태 설명용으로만 사용, 장식 효과 금지
- 텍스트 위계가 핵심 — 컬러보다 weight/size로 구분

---

## navigation / category-pill

**역할**: 카테고리 필터 pill row — New / 의류 / 신발 / 액세서리 / Sale

**탐지 출처**: product catalog

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

- [editorial+calm] hover: 텍스트 underline 또는 color shift, 장식적 효과 없음 + opacity 변화 (0.08-0.12), elevation 변화 없음
- [editorial+calm] density: 넉넉한 line-height와 margin, 읽기 편한 간격 + comfortable 모드 기본, 여유로운 padding
- [editorial+calm] motion: 콘텐츠 전환 위주, UI chrome 모션 최소화 + 150-200ms ease-out, bounce/spring 없음

### Visual Adaptation Hints

- **filter_nav_density**: filter/nav density는 low다. top nav는 가볍게 유지하고 filter controls는 별도 섹션 또는 로컬 toolbar로 분리한다. (source=navigation; confidence=0.29; provenance=inferred; direction=top navigation은 가볍게 유지하고 CTA와 section anchors를 분명하게 분리한다.; evidence=Narrative landing flow, layout=landing-narrative, density=airy)

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
- 애니메이션은 상태 설명용으로만 사용, 장식 효과 금지
- 텍스트 위계가 핵심 — 컬러보다 weight/size로 구분

---

## input / filter-sidebar

**역할**: 카테고리/가격/브랜드/사이즈/색상 필터 사이드바

**탐지 출처**: product catalog

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

- [editorial+calm] hover: 텍스트 underline 또는 color shift, 장식적 효과 없음 + opacity 변화 (0.08-0.12), elevation 변화 없음
- [editorial+calm] density: 넉넉한 line-height와 margin, 읽기 편한 간격 + comfortable 모드 기본, 여유로운 padding
- [editorial+calm] feedback: 콘텐츠 맥락 안에서 인라인 표시, 토스트보다 인라인 선호 + subtle inline alert 선호, 과한 컬러 블록 지양

### Visual Adaptation Hints

- **filter_nav_density**: filter/nav density는 low다. top nav는 가볍게 유지하고 filter controls는 별도 섹션 또는 로컬 toolbar로 분리한다. (source=navigation; confidence=0.29; provenance=inferred; direction=top navigation은 가볍게 유지하고 CTA와 section anchors를 분명하게 분리한다.; evidence=Narrative landing flow, layout=landing-narrative, density=airy)

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
- 애니메이션은 상태 설명용으로만 사용, 장식 효과 금지
- 텍스트 위계가 핵심 — 컬러보다 weight/size로 구분

---

## input / sort-dropdown

**역할**: 정렬 dropdown — 신상품 / 인기순 / 가격 낮은순 / 가격 높은순

**탐지 출처**: product catalog

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

- [editorial+calm] hover: 텍스트 underline 또는 color shift, 장식적 효과 없음 + opacity 변화 (0.08-0.12), elevation 변화 없음
- [editorial+calm] density: 넉넉한 line-height와 margin, 읽기 편한 간격 + comfortable 모드 기본, 여유로운 padding
- [editorial+calm] feedback: 콘텐츠 맥락 안에서 인라인 표시, 토스트보다 인라인 선호 + subtle inline alert 선호, 과한 컬러 블록 지양

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
- 애니메이션은 상태 설명용으로만 사용, 장식 효과 금지
- 텍스트 위계가 핵심 — 컬러보다 weight/size로 구분

---

## commerce / drop-banner

**역할**: hero drop 전용 banner — drop name + countdown + CTA + impact typography

**탐지 출처**: drop and merchandising

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

- [editorial+calm] hover: 텍스트 underline 또는 color shift, 장식적 효과 없음 + opacity 변화 (0.08-0.12), elevation 변화 없음
- [editorial+calm] motion: 콘텐츠 전환 위주, UI chrome 모션 최소화 + 150-200ms ease-out, bounce/spring 없음
- [editorial+calm] color: 타이포그래피로 위계 형성, 컬러보다 weight/size 활용 + 중성 톤 위주, accent는 최소한으로

### Visual Adaptation Hints

- **card_elevation_tendency**: 카드는 낮은 elevation만 허용하고 색면 차이로 그룹을 구분한다. 내부 여백은 넉넉하게 두고 card breathing room을 확보한다. (source=cards; confidence=0.29; provenance=inferred; direction=low-elevation tinted cards를 기본으로 하고, 넓은 내부 여백과 강한 section breathing room. 중간 반경으로 제품 UI 절제 유지.; evidence=surface=tinted, density=airy, corner=medium)
- **border_vs_fill_emphasis**: fill 중심이다. tint surface로 성격을 만들고 border는 아주 얇게 보조한다. (source=cards; confidence=0.29; provenance=inferred; direction=low-elevation tinted cards를 기본으로 하고, 넓은 내부 여백과 강한 section breathing room. 중간 반경으로 제품 UI 절제 유지.; evidence=surface=tinted, density=airy, corner=medium)

### 구현 노트

- 기존에 같은 역할의 컴포넌트가 있으면 토큰 교체부터 시작
- variant prop으로 시각적 변형을 관리 (하드코딩 금지)
- 애니메이션은 상태 설명용으로만 사용, 장식 효과 금지
- 텍스트 위계가 핵심 — 컬러보다 weight/size로 구분

---

## commerce / countdown-timer

**역할**: drop countdown timer chip — D/H/M/S mono tabular-nums, accent 강조

**탐지 출처**: drop and merchandising

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

- [editorial+calm] hover: 텍스트 underline 또는 color shift, 장식적 효과 없음 + opacity 변화 (0.08-0.12), elevation 변화 없음
- [editorial+calm] motion: 콘텐츠 전환 위주, UI chrome 모션 최소화 + 150-200ms ease-out, bounce/spring 없음
- [editorial+calm] color: 타이포그래피로 위계 형성, 컬러보다 weight/size 활용 + 중성 톤 위주, accent는 최소한으로

### 구현 노트

- 기존에 같은 역할의 컴포넌트가 있으면 토큰 교체부터 시작
- variant prop으로 시각적 변형을 관리 (하드코딩 금지)
- 애니메이션은 상태 설명용으로만 사용, 장식 효과 금지
- 텍스트 위계가 핵심 — 컬러보다 weight/size로 구분

---

## commerce / lookbook-hero

**역할**: 에디토리얼 lookbook tile — full-bleed image + overlay copy

**탐지 출처**: drop and merchandising

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

- [editorial+calm] hover: 텍스트 underline 또는 color shift, 장식적 효과 없음 + opacity 변화 (0.08-0.12), elevation 변화 없음
- [editorial+calm] motion: 콘텐츠 전환 위주, UI chrome 모션 최소화 + 150-200ms ease-out, bounce/spring 없음
- [editorial+calm] color: 타이포그래피로 위계 형성, 컬러보다 weight/size 활용 + 중성 톤 위주, accent는 최소한으로

### 구현 노트

- 기존에 같은 역할의 컴포넌트가 있으면 토큰 교체부터 시작
- variant prop으로 시각적 변형을 관리 (하드코딩 금지)
- 애니메이션은 상태 설명용으로만 사용, 장식 효과 금지
- 텍스트 위계가 핵심 — 컬러보다 weight/size로 구분

---

## commerce / featured-category-tile

**역할**: 홈 featured category tile — large product image + category label

**탐지 출처**: drop and merchandising

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

- [editorial+calm] hover: 텍스트 underline 또는 color shift, 장식적 효과 없음 + opacity 변화 (0.08-0.12), elevation 변화 없음
- [editorial+calm] motion: 콘텐츠 전환 위주, UI chrome 모션 최소화 + 150-200ms ease-out, bounce/spring 없음
- [editorial+calm] color: 타이포그래피로 위계 형성, 컬러보다 weight/size 활용 + 중성 톤 위주, accent는 최소한으로

### Visual Adaptation Hints

- **card_elevation_tendency**: 카드는 낮은 elevation만 허용하고 색면 차이로 그룹을 구분한다. 내부 여백은 넉넉하게 두고 card breathing room을 확보한다. (source=cards; confidence=0.29; provenance=inferred; direction=low-elevation tinted cards를 기본으로 하고, 넓은 내부 여백과 강한 section breathing room. 중간 반경으로 제품 UI 절제 유지.; evidence=surface=tinted, density=airy, corner=medium)
- **border_vs_fill_emphasis**: fill 중심이다. tint surface로 성격을 만들고 border는 아주 얇게 보조한다. (source=cards; confidence=0.29; provenance=inferred; direction=low-elevation tinted cards를 기본으로 하고, 넓은 내부 여백과 강한 section breathing room. 중간 반경으로 제품 UI 절제 유지.; evidence=surface=tinted, density=airy, corner=medium)

### 구현 노트

- 기존에 같은 역할의 컴포넌트가 있으면 토큰 교체부터 시작
- variant prop으로 시각적 변형을 관리 (하드코딩 금지)
- 애니메이션은 상태 설명용으로만 사용, 장식 효과 금지
- 텍스트 위계가 핵심 — 컬러보다 weight/size로 구분

---

## commerce / hero-banner

**역할**: full-bleed hero banner — saturated primary surface, large product hero image

**탐지 출처**: drop and merchandising

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

- [editorial+calm] hover: 텍스트 underline 또는 color shift, 장식적 효과 없음 + opacity 변화 (0.08-0.12), elevation 변화 없음
- [editorial+calm] motion: 콘텐츠 전환 위주, UI chrome 모션 최소화 + 150-200ms ease-out, bounce/spring 없음
- [editorial+calm] color: 타이포그래피로 위계 형성, 컬러보다 weight/size 활용 + 중성 톤 위주, accent는 최소한으로

### Visual Adaptation Hints

- **card_elevation_tendency**: 카드는 낮은 elevation만 허용하고 색면 차이로 그룹을 구분한다. 내부 여백은 넉넉하게 두고 card breathing room을 확보한다. (source=cards; confidence=0.29; provenance=inferred; direction=low-elevation tinted cards를 기본으로 하고, 넓은 내부 여백과 강한 section breathing room. 중간 반경으로 제품 UI 절제 유지.; evidence=surface=tinted, density=airy, corner=medium)
- **border_vs_fill_emphasis**: fill 중심이다. tint surface로 성격을 만들고 border는 아주 얇게 보조한다. (source=cards; confidence=0.29; provenance=inferred; direction=low-elevation tinted cards를 기본으로 하고, 넓은 내부 여백과 강한 section breathing room. 중간 반경으로 제품 UI 절제 유지.; evidence=surface=tinted, density=airy, corner=medium)

### 구현 노트

- 기존에 같은 역할의 컴포넌트가 있으면 토큰 교체부터 시작
- variant prop으로 시각적 변형을 관리 (하드코딩 금지)
- 애니메이션은 상태 설명용으로만 사용, 장식 효과 금지
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

- [editorial+calm] hover: 텍스트 underline 또는 color shift, 장식적 효과 없음 + opacity 변화 (0.08-0.12), elevation 변화 없음
- [editorial+calm] density: 넉넉한 line-height와 margin, 읽기 편한 간격 + comfortable 모드 기본, 여유로운 padding
- [editorial+calm] feedback: 콘텐츠 맥락 안에서 인라인 표시, 토스트보다 인라인 선호 + subtle inline alert 선호, 과한 컬러 블록 지양

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
- 애니메이션은 상태 설명용으로만 사용, 장식 효과 금지
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

- [editorial+calm] hover: 텍스트 underline 또는 color shift, 장식적 효과 없음 + opacity 변화 (0.08-0.12), elevation 변화 없음
- [editorial+calm] density: 넉넉한 line-height와 margin, 읽기 편한 간격 + comfortable 모드 기본, 여유로운 padding
- [editorial+calm] feedback: 콘텐츠 맥락 안에서 인라인 표시, 토스트보다 인라인 선호 + subtle inline alert 선호, 과한 컬러 블록 지양

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
- 애니메이션은 상태 설명용으로만 사용, 장식 효과 금지
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

- [editorial+calm] hover: 텍스트 underline 또는 color shift, 장식적 효과 없음 + opacity 변화 (0.08-0.12), elevation 변화 없음
- [editorial+calm] density: 넉넉한 line-height와 margin, 읽기 편한 간격 + comfortable 모드 기본, 여유로운 padding
- [editorial+calm] motion: 콘텐츠 전환 위주, UI chrome 모션 최소화 + 150-200ms ease-out, bounce/spring 없음

### Visual Adaptation Hints

- **filter_nav_density**: filter/nav density는 low다. top nav는 가볍게 유지하고 filter controls는 별도 섹션 또는 로컬 toolbar로 분리한다. (source=navigation; confidence=0.29; provenance=inferred; direction=top navigation은 가볍게 유지하고 CTA와 section anchors를 분명하게 분리한다.; evidence=Narrative landing flow, layout=landing-narrative, density=airy)

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
- 애니메이션은 상태 설명용으로만 사용, 장식 효과 금지
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

- [editorial+calm] hover: 텍스트 underline 또는 color shift, 장식적 효과 없음 + opacity 변화 (0.08-0.12), elevation 변화 없음
- [editorial+calm] density: 넉넉한 line-height와 margin, 읽기 편한 간격 + comfortable 모드 기본, 여유로운 padding
- [editorial+calm] motion: 콘텐츠 전환 위주, UI chrome 모션 최소화 + 150-200ms ease-out, bounce/spring 없음

### Visual Adaptation Hints

- **filter_nav_density**: filter/nav density는 low다. top nav는 가볍게 유지하고 filter controls는 별도 섹션 또는 로컬 toolbar로 분리한다. (source=navigation; confidence=0.29; provenance=inferred; direction=top navigation은 가볍게 유지하고 CTA와 section anchors를 분명하게 분리한다.; evidence=Narrative landing flow, layout=landing-narrative, density=airy)

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
- 애니메이션은 상태 설명용으로만 사용, 장식 효과 금지
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

- [editorial+calm] feedback: 콘텐츠 맥락 안에서 인라인 표시, 토스트보다 인라인 선호 + subtle inline alert 선호, 과한 컬러 블록 지양
- [editorial+calm] motion: 콘텐츠 전환 위주, UI chrome 모션 최소화 + 150-200ms ease-out, bounce/spring 없음
- [editorial+calm] color: 타이포그래피로 위계 형성, 컬러보다 weight/size 활용 + 중성 톤 위주, accent는 최소한으로

### 레퍼런스 근거

- **Carbon Design System**: We welcome all feedback, designs, or ideas in order to produce the best possible experience for our users. If you're interested in contributing, ch...
- **Primer**: CircleBadge CircleBadge visually connects logos of third-party services, eg. in the marketplace.

### 구현 노트

- 기존에 같은 역할의 컴포넌트가 있으면 토큰 교체부터 시작
- variant prop으로 시각적 변형을 관리 (하드코딩 금지)
- auto-dismiss 시간은 내용 길이에 비례 (기본 5초)
- 반응형 검증: 320px, 360px, 390px, 430px에서 control overflow와 viewport horizontal scroll이 없어야 함
- action row는 narrow viewport에서 `flex-wrap: wrap` 또는 세로 stack으로 전환하고, overflow-x 숨김으로 문제를 덮지 않음
- 애니메이션은 상태 설명용으로만 사용, 장식 효과 금지
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

- [editorial+calm] feedback: 콘텐츠 맥락 안에서 인라인 표시, 토스트보다 인라인 선호 + subtle inline alert 선호, 과한 컬러 블록 지양
- [editorial+calm] motion: 콘텐츠 전환 위주, UI chrome 모션 최소화 + 150-200ms ease-out, bounce/spring 없음
- [editorial+calm] color: 타이포그래피로 위계 형성, 컬러보다 weight/size 활용 + 중성 톤 위주, accent는 최소한으로

### Visual Adaptation Hints

- **card_elevation_tendency**: 카드는 낮은 elevation만 허용하고 색면 차이로 그룹을 구분한다. 내부 여백은 넉넉하게 두고 card breathing room을 확보한다. (source=cards; confidence=0.29; provenance=inferred; direction=low-elevation tinted cards를 기본으로 하고, 넓은 내부 여백과 강한 section breathing room. 중간 반경으로 제품 UI 절제 유지.; evidence=surface=tinted, density=airy, corner=medium)
- **border_vs_fill_emphasis**: fill 중심이다. tint surface로 성격을 만들고 border는 아주 얇게 보조한다. (source=cards; confidence=0.29; provenance=inferred; direction=low-elevation tinted cards를 기본으로 하고, 넓은 내부 여백과 강한 section breathing room. 중간 반경으로 제품 UI 절제 유지.; evidence=surface=tinted, density=airy, corner=medium)
- **chart_panel_framing**: 차트 패널은 soft tint frame과 restrained divider로 프레이밍한다. 헤더 메타데이터와 본문 visualization 사이의 breathing room을 충분히 둔다. (source=data_display; confidence=0.29; provenance=inferred; direction=정보 밀도를 유지하되 thin dividers와 restrained accent로 hierarchy를 만든다.; evidence=layout=dashboard-grid, density=airy, layout=landing-narrative, surface=tinted)

### 레퍼런스 근거

- **Carbon Design System**: We welcome all feedback, designs, or ideas in order to produce the best possible experience for our users. If you're interested in contributing, ch...
- **Primer**: Messaging components are used to provide important and relevant information to the user, including feedback, contextual information, product update...

### 구현 노트

- 기존에 같은 역할의 컴포넌트가 있으면 토큰 교체부터 시작
- variant prop으로 시각적 변형을 관리 (하드코딩 금지)
- auto-dismiss 시간은 내용 길이에 비례 (기본 5초)
- 반응형 검증: 320px, 360px, 390px, 430px에서 control overflow와 viewport horizontal scroll이 없어야 함
- action row는 narrow viewport에서 `flex-wrap: wrap` 또는 세로 stack으로 전환하고, overflow-x 숨김으로 문제를 덮지 않음
- 애니메이션은 상태 설명용으로만 사용, 장식 효과 금지
- 텍스트 위계가 핵심 — 컬러보다 weight/size로 구분

---

## overlay / dialog

**역할**: Modal decision or focused task surface.

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

- [editorial+calm] motion: 콘텐츠 전환 위주, UI chrome 모션 최소화 + 150-200ms ease-out, bounce/spring 없음
- [editorial+calm] density: 넉넉한 line-height와 margin, 읽기 편한 간격 + comfortable 모드 기본, 여유로운 padding

### 레퍼런스 근거

- **Primer**: ConfirmationDialog ConfirmationDialog is a specialized dialog component used to confirm user actions. It provides a simple way to ask users to conf...

### 구현 노트

- 기존에 같은 역할의 컴포넌트가 있으면 토큰 교체부터 시작
- variant prop으로 시각적 변형을 관리 (하드코딩 금지)
- Escape / backdrop click으로 닫기, 열 때 첫 focusable 요소로 이동
- 애니메이션은 상태 설명용으로만 사용, 장식 효과 금지
- 텍스트 위계가 핵심 — 컬러보다 weight/size로 구분

---

## overlay / popover

**역할**: Anchored transient surface for short forms or contextual controls.

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

- [editorial+calm] motion: 콘텐츠 전환 위주, UI chrome 모션 최소화 + 150-200ms ease-out, bounce/spring 없음
- [editorial+calm] density: 넉넉한 line-height와 margin, 읽기 편한 간격 + comfortable 모드 기본, 여유로운 padding

### 레퍼런스 근거

- **Carbon Design System**: The AI label is also the trigger for the explainability popover which serves as the first layer of explainability. It provides a consistent, up-fro...
- **Primer**: Popover Popover is used to bring attention to specific user interface elements.

### 구현 노트

- 기존에 같은 역할의 컴포넌트가 있으면 토큰 교체부터 시작
- variant prop으로 시각적 변형을 관리 (하드코딩 금지)
- Escape / backdrop click으로 닫기, 열 때 첫 focusable 요소로 이동
- 애니메이션은 상태 설명용으로만 사용, 장식 효과 금지
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

- [editorial+calm] motion: 콘텐츠 전환 위주, UI chrome 모션 최소화 + 150-200ms ease-out, bounce/spring 없음
- [editorial+calm] density: 넉넉한 line-height와 margin, 읽기 편한 간격 + comfortable 모드 기본, 여유로운 padding

### 레퍼런스 근거

- **Carbon Design System**: We’re also using this release to address some of the outstanding accessibility issues for components like Notification and Tooltip along with consi...
- **Primer**: Tooltip Tooltips add additional context to interactive UI elements and appear on mouse hover or keyboard focus.

### 구현 노트

- 기존에 같은 역할의 컴포넌트가 있으면 토큰 교체부터 시작
- variant prop으로 시각적 변형을 관리 (하드코딩 금지)
- Escape / backdrop click으로 닫기, 열 때 첫 focusable 요소로 이동
- 애니메이션은 상태 설명용으로만 사용, 장식 효과 금지
- 텍스트 위계가 핵심 — 컬러보다 weight/size로 구분

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

- [editorial+calm] density: 넉넉한 line-height와 margin, 읽기 편한 간격 + comfortable 모드 기본, 여유로운 padding
- [editorial+calm] color: 타이포그래피로 위계 형성, 컬러보다 weight/size 활용 + 중성 톤 위주, accent는 최소한으로

### Visual Adaptation Hints

- **operational_surface_role**: 주 작업 표면은 card wall이 아니라 table/list/rail/canvas 계열로 설계한다. 행 간격은 읽기 편하게 두되 반복 항목은 같은 카드 껍질로 감싸지 않는다. (source=data_display; confidence=0.29; provenance=inferred; direction=정보 밀도를 유지하되 thin dividers와 restrained accent로 hierarchy를 만든다.; evidence=layout=dashboard-grid, density=airy, layout=landing-narrative)
- **filter_nav_density**: filter/nav density는 low다. top nav는 가볍게 유지하고 filter controls는 별도 섹션 또는 로컬 toolbar로 분리한다. (source=navigation; confidence=0.29; provenance=inferred; direction=top navigation은 가볍게 유지하고 CTA와 section anchors를 분명하게 분리한다.; evidence=Narrative landing flow, layout=landing-narrative, density=airy)
- **chart_panel_framing**: 차트 패널은 soft tint frame과 restrained divider로 프레이밍한다. 헤더 메타데이터와 본문 visualization 사이의 breathing room을 충분히 둔다. (source=data_display; confidence=0.29; provenance=inferred; direction=정보 밀도를 유지하되 thin dividers와 restrained accent로 hierarchy를 만든다.; evidence=layout=dashboard-grid, density=airy, layout=landing-narrative, surface=tinted)

### 구현 노트

- 기존에 같은 역할의 컴포넌트가 있으면 토큰 교체부터 시작
- variant prop으로 시각적 변형을 관리 (하드코딩 금지)
- 빈 상태(empty-state)와 에러 상태를 반드시 처리
- 좁은 UI 텍스트는 Pretendard 기준 label line-height 1.4-1.5를 참고해 뭉침을 방지
- 반응형 검증: 320px, 360px, 390px, 430px에서 control overflow와 viewport horizontal scroll이 없어야 함
- action row는 narrow viewport에서 `flex-wrap: wrap` 또는 세로 stack으로 전환하고, overflow-x 숨김으로 문제를 덮지 않음
- 애니메이션은 상태 설명용으로만 사용, 장식 효과 금지
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

- [editorial+calm] density: 넉넉한 line-height와 margin, 읽기 편한 간격 + comfortable 모드 기본, 여유로운 padding
- [editorial+calm] color: 타이포그래피로 위계 형성, 컬러보다 weight/size 활용 + 중성 톤 위주, accent는 최소한으로

### Visual Adaptation Hints

- **card_elevation_tendency**: 카드는 낮은 elevation만 허용하고 색면 차이로 그룹을 구분한다. 내부 여백은 넉넉하게 두고 card breathing room을 확보한다. (source=cards; confidence=0.29; provenance=inferred; direction=low-elevation tinted cards를 기본으로 하고, 넓은 내부 여백과 강한 section breathing room. 중간 반경으로 제품 UI 절제 유지.; evidence=surface=tinted, density=airy, corner=medium)
- **border_vs_fill_emphasis**: fill 중심이다. tint surface로 성격을 만들고 border는 아주 얇게 보조한다. (source=cards; confidence=0.29; provenance=inferred; direction=low-elevation tinted cards를 기본으로 하고, 넓은 내부 여백과 강한 section breathing room. 중간 반경으로 제품 UI 절제 유지.; evidence=surface=tinted, density=airy, corner=medium)
- **chart_panel_framing**: 차트 패널은 soft tint frame과 restrained divider로 프레이밍한다. 헤더 메타데이터와 본문 visualization 사이의 breathing room을 충분히 둔다. (source=data_display; confidence=0.29; provenance=inferred; direction=정보 밀도를 유지하되 thin dividers와 restrained accent로 hierarchy를 만든다.; evidence=layout=dashboard-grid, density=airy, layout=landing-narrative, surface=tinted)

### 구현 노트

- 기존에 같은 역할의 컴포넌트가 있으면 토큰 교체부터 시작
- variant prop으로 시각적 변형을 관리 (하드코딩 금지)
- 빈 상태(empty-state)와 에러 상태를 반드시 처리
- 좁은 UI 텍스트는 Pretendard 기준 label line-height 1.4-1.5를 참고해 뭉침을 방지
- 애니메이션은 상태 설명용으로만 사용, 장식 효과 금지
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

- [editorial+calm] hover: 텍스트 underline 또는 color shift, 장식적 효과 없음 + opacity 변화 (0.08-0.12), elevation 변화 없음
- [editorial+calm] motion: 콘텐츠 전환 위주, UI chrome 모션 최소화 + 150-200ms ease-out, bounce/spring 없음
- [editorial+calm] color: 타이포그래피로 위계 형성, 컬러보다 weight/size 활용 + 중성 톤 위주, accent는 최소한으로

### Visual Adaptation Hints

- **operational_surface_role**: 주 작업 표면은 card wall이 아니라 table/list/rail/canvas 계열로 설계한다. 행 간격은 읽기 편하게 두되 반복 항목은 같은 카드 껍질로 감싸지 않는다. (source=data_display; confidence=0.29; provenance=inferred; direction=정보 밀도를 유지하되 thin dividers와 restrained accent로 hierarchy를 만든다.; evidence=layout=dashboard-grid, density=airy, layout=landing-narrative)

### 레퍼런스 근거

- **Carbon Design System**: AI chat is a conversational framework between a user and an AI that can aid in creating tasks, finding insights, tracking documents, and more. For ...
- **Primer**: The GitHub Design Infrastructure and Design Engineering teams build and maintain Primer — this includes our CSS framework, style guide documentatio...

### 구현 노트

- 기존에 같은 역할의 컴포넌트가 있으면 토큰 교체부터 시작
- variant prop으로 시각적 변형을 관리 (하드코딩 금지)
- 애니메이션은 상태 설명용으로만 사용, 장식 효과 금지
- 텍스트 위계가 핵심 — 컬러보다 weight/size로 구분

---

## feedback / retention-indicator

**역할**: Retention and recordkeeping status indicator for regulated content

**Slot archetype**: `advanced:retention-indicator`

### Advanced Usage

Use when:
- users need to know whether a record is retained, pending, or expired
- policy requires retention visibility near decisions
Avoid when:
- retention is not relevant to user workflow
Pairs with: decision-record-card, audit-timeline, inspector-drawer

### 구조 (Anatomy)

- indicator
- status-label
- expiry-date
- policy-link
- tooltip(optional)

### 상태 (States)

| 상태 | 설명 |
|------|------|
| `retained` | retained |
| `pending` | pending |
| `expired` | expired |
| `not-required` | not-required |

### 토큰 바인딩

```
surface: var(--color-surface-muted)
retained: var(--color-success)
pending: var(--color-warning)
expired: var(--color-danger)
border: var(--color-border)
```

### 접근성

- status and expiry date are readable text
- tooltip content is also reachable via focus
- policy link text names the target policy

### 브랜드 적용

- [editorial+calm] feedback: 콘텐츠 맥락 안에서 인라인 표시, 토스트보다 인라인 선호 + subtle inline alert 선호, 과한 컬러 블록 지양
- [editorial+calm] motion: 콘텐츠 전환 위주, UI chrome 모션 최소화 + 150-200ms ease-out, bounce/spring 없음
- [editorial+calm] color: 타이포그래피로 위계 형성, 컬러보다 weight/size 활용 + 중성 톤 위주, accent는 최소한으로

### 레퍼런스 근거

- **Carbon Design System**: We welcome all feedback, designs, or ideas in order to produce the best possible experience for our users. If you're interested in contributing, ch...
- **Primer**: Messaging components are used to provide important and relevant information to the user, including feedback, contextual information, product update...

### 구현 노트

- 기존에 같은 역할의 컴포넌트가 있으면 토큰 교체부터 시작
- variant prop으로 시각적 변형을 관리 (하드코딩 금지)
- auto-dismiss 시간은 내용 길이에 비례 (기본 5초)
- 반응형 검증: 320px, 360px, 390px, 430px에서 control overflow와 viewport horizontal scroll이 없어야 함
- action row는 narrow viewport에서 `flex-wrap: wrap` 또는 세로 stack으로 전환하고, overflow-x 숨김으로 문제를 덮지 않음
- 애니메이션은 상태 설명용으로만 사용, 장식 효과 금지
- 텍스트 위계가 핵심 — 컬러보다 weight/size로 구분

---

## navigation / saved-view-bar

**역할**: Saved view and scope switcher for repeated operational filters

**Slot archetype**: `advanced:saved-view-bar`

### Advanced Usage

Use when:
- teams revisit the same filtered views often
- dense tools need stable scope memory
Avoid when:
- filters are one-off and simple
Pairs with: filter-builder, bulk-action-table, exception-queue

### 구조 (Anatomy)

- tab-list
- saved-view-tab
- count-badge
- overflow-menu
- save-action

### 상태 (States)

| 상태 | 설명 |
|------|------|
| `default` | 기본 상태 |
| `active` | 클릭/탭 중 |
| `dirty` | dirty |
| `overflow` | overflow |

### 토큰 바인딩

```
surface: var(--color-surface)
active-surface: var(--color-surface-tint)
border: var(--color-border)
active: var(--color-brand-primary)
radius: var(--radius-md)
```

### 접근성

- tabs use role="tablist" / role="tab" when switching panels
- dirty state is text-announced
- overflow menu has keyboard navigation

### 브랜드 적용

- [editorial+calm] hover: 텍스트 underline 또는 color shift, 장식적 효과 없음 + opacity 변화 (0.08-0.12), elevation 변화 없음
- [editorial+calm] density: 넉넉한 line-height와 margin, 읽기 편한 간격 + comfortable 모드 기본, 여유로운 padding
- [editorial+calm] motion: 콘텐츠 전환 위주, UI chrome 모션 최소화 + 150-200ms ease-out, bounce/spring 없음

### Visual Adaptation Hints

- **filter_nav_density**: filter/nav density는 low다. top nav는 가볍게 유지하고 filter controls는 별도 섹션 또는 로컬 toolbar로 분리한다. (source=navigation; confidence=0.29; provenance=inferred; direction=top navigation은 가볍게 유지하고 CTA와 section anchors를 분명하게 분리한다.; evidence=Narrative landing flow, layout=landing-narrative, density=airy)

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
- 애니메이션은 상태 설명용으로만 사용, 장식 효과 금지
- 텍스트 위계가 핵심 — 컬러보다 weight/size로 구분
