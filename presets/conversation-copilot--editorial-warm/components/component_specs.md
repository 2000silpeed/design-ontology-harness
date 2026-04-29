# Quill Component Specs

총 125개 컴포넌트 | 패밀리: button, copilot-artifact, copilot-chat, data-display, document, editorial, feedback, input, marketing, navigation, overlay, social

## 구현 원칙 (Non-negotiable)

이 스펙의 모든 컴포넌트를 구현할 때 반드시 지킨다:

1. **이모지를 UI로 쓰지 않는다** — 🎨 ✅ 🔥 ⚡ 🚀 ❌ ⭐ 📊 등 이모지를 아이콘, 상태 표시, 버튼 장식, 네비게이션 지표 자리에 절대 넣지 않는다. 아이콘 자리에는 SVG 컴포넌트 또는 Lucide/Heroicons/Phosphor/Tabler 라이브러리를 사용한다.
2. **컴포넌트를 직접 구현한다** — 아래 각 컴포넌트의 anatomy(구조), states(상태), 토큰 바인딩, 접근성 규칙을 그대로 따라 완전하게 구현한다. '임시', 'TODO', '플레이스홀더' 같은 반쪽 구현을 남기지 않는다.
3. **라이브러리 기본 스타일 금지** — 라이브러리 컴포넌트를 그대로 import해서 쓰지 않는다. 반드시 디자인 토큰(--color-*, --space-*, --radius-*, --font-*)으로 스타일을 명시적으로 바인딩한다.
4. **접근성은 옵션이 아니다** — 각 컴포넌트의 '접근성' 섹션에 정의된 role, aria-*, label, focus 관리 규칙을 전부 적용한다.
5. **hex 값 하드코딩 금지** — 색상은 반드시 semantic token을 경유한다 (예: `color: var(--color-ink)` not `color: #2C2C2C`).

## 브랜드 적용 규칙

- **hover**: opacity 변화 (0.08-0.12), elevation 변화 없음 + 텍스트 underline 또는 color shift, 장식적 효과 없음
- **motion**: 150-200ms ease-out, bounce/spring 없음 + 콘텐츠 전환 위주, UI chrome 모션 최소화
- **color**: 중성 톤 위주, accent는 최소한으로 + 타이포그래피로 위계 형성, 컬러보다 weight/size 활용
- **density**: comfortable 모드 기본, 여유로운 padding + 넉넉한 line-height와 margin, 읽기 편한 간격
- **feedback**: subtle inline alert 선호, 과한 컬러 블록 지양 + 콘텐츠 맥락 안에서 인라인 표시, 토스트보다 인라인 선호

## Visual-reference 적용 원칙

- anatomy / states / accessibility는 설계서(spec)와 KB 근거를 유지하고, visual adaptation은 elevation / framing / prominence / density 같은 표현 계층에만 advisory signal로 적용한다.
- Active visual signals: surface_style=tinted, density=airy, corner_style=medium, top_layout_cue=conversation-panel
- Connected component hints: cards, data_display, navigation, panel, typography

## Typography Guardrails

- 한글 기반 제품은 line-break / scale / tracking을 영문 랜딩 기본값으로 처리하지 않고, 아래 가드레일을 구현 기본값으로 사용한다.
- Headline: Noto Serif KR | line-height 1.2-1.4 | tracking -0.02em
- Body: Pretendard | line-height 1.6-1.7 | label line-height 1.4-1.5
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

- [calm+editorial] hover: opacity 변화 (0.08-0.12), elevation 변화 없음 + 텍스트 underline 또는 color shift, 장식적 효과 없음
- [calm+editorial] motion: 150-200ms ease-out, bounce/spring 없음 + 콘텐츠 전환 위주, UI chrome 모션 최소화
- [calm+editorial] color: 중성 톤 위주, accent는 최소한으로 + 타이포그래피로 위계 형성, 컬러보다 weight/size 활용

### Visual Adaptation Hints

- **cta_prominence**: CTA prominence는 medium이다. primary action은 분명하게 보이되 화면 전체를 지배하지 않게 유지한다. (source=cards; confidence=0.94; provenance=inferred; direction=low-elevation tinted cards를 기본으로 하고, 넓은 내부 여백과 강한 section breathing room. 중간 반경으로 제품 UI 절제 유지.; evidence=surface=tinted, density=airy, corner=medium, layout=conversation-panel)

### 레퍼런스 근거

- **Carbon Design System**: These components can toggle between the AI variant and the default variant depending on the user’s interaction. If the user manually overrides the ...
- **Primer**: I get so much joy from writing HTML and CSS, and design systems are one level up - systematically making UIs accessible and consistent. I love conc...

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

- [calm+editorial] hover: opacity 변화 (0.08-0.12), elevation 변화 없음 + 텍스트 underline 또는 color shift, 장식적 효과 없음
- [calm+editorial] motion: 150-200ms ease-out, bounce/spring 없음 + 콘텐츠 전환 위주, UI chrome 모션 최소화
- [calm+editorial] color: 중성 톤 위주, accent는 최소한으로 + 타이포그래피로 위계 형성, 컬러보다 weight/size 활용

### Visual Adaptation Hints

- **cta_prominence**: CTA prominence는 medium이다. primary action은 분명하게 보이되 화면 전체를 지배하지 않게 유지한다. (source=cards; confidence=0.94; provenance=inferred; direction=low-elevation tinted cards를 기본으로 하고, 넓은 내부 여백과 강한 section breathing room. 중간 반경으로 제품 UI 절제 유지.; evidence=surface=tinted, density=airy, corner=medium, layout=conversation-panel)

### 레퍼런스 근거

- **Carbon Design System**: These components can toggle between the AI variant and the default variant depending on the user’s interaction. If the user manually overrides the ...
- **Primer**: I get so much joy from writing HTML and CSS, and design systems are one level up - systematically making UIs accessible and consistent. I love conc...

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

- [calm+editorial] hover: opacity 변화 (0.08-0.12), elevation 변화 없음 + 텍스트 underline 또는 color shift, 장식적 효과 없음
- [calm+editorial] motion: 150-200ms ease-out, bounce/spring 없음 + 콘텐츠 전환 위주, UI chrome 모션 최소화
- [calm+editorial] color: 중성 톤 위주, accent는 최소한으로 + 타이포그래피로 위계 형성, 컬러보다 weight/size 활용

### Visual Adaptation Hints

- **cta_prominence**: CTA prominence는 medium이다. primary action은 분명하게 보이되 화면 전체를 지배하지 않게 유지한다. (source=cards; confidence=0.94; provenance=inferred; direction=low-elevation tinted cards를 기본으로 하고, 넓은 내부 여백과 강한 section breathing room. 중간 반경으로 제품 UI 절제 유지.; evidence=surface=tinted, density=airy, corner=medium, layout=conversation-panel)

### 레퍼런스 근거

- **Carbon Design System**: These components can toggle between the AI variant and the default variant depending on the user’s interaction. If the user manually overrides the ...
- **Primer**: I get so much joy from writing HTML and CSS, and design systems are one level up - systematically making UIs accessible and consistent. I love conc...

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

- [calm+editorial] hover: opacity 변화 (0.08-0.12), elevation 변화 없음 + 텍스트 underline 또는 color shift, 장식적 효과 없음
- [calm+editorial] motion: 150-200ms ease-out, bounce/spring 없음 + 콘텐츠 전환 위주, UI chrome 모션 최소화
- [calm+editorial] color: 중성 톤 위주, accent는 최소한으로 + 타이포그래피로 위계 형성, 컬러보다 weight/size 활용

### Visual Adaptation Hints

- **cta_prominence**: CTA prominence는 medium이다. primary action은 분명하게 보이되 화면 전체를 지배하지 않게 유지한다. (source=cards; confidence=0.94; provenance=inferred; direction=low-elevation tinted cards를 기본으로 하고, 넓은 내부 여백과 강한 section breathing room. 중간 반경으로 제품 UI 절제 유지.; evidence=surface=tinted, density=airy, corner=medium, layout=conversation-panel)

### 레퍼런스 근거

- **Carbon Design System**: These components can toggle between the AI variant and the default variant depending on the user’s interaction. If the user manually overrides the ...
- **Primer**: I get so much joy from writing HTML and CSS, and design systems are one level up - systematically making UIs accessible and consistent. I love conc...

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

- [calm+editorial] hover: opacity 변화 (0.08-0.12), elevation 변화 없음 + 텍스트 underline 또는 color shift, 장식적 효과 없음
- [calm+editorial] motion: 150-200ms ease-out, bounce/spring 없음 + 콘텐츠 전환 위주, UI chrome 모션 최소화
- [calm+editorial] color: 중성 톤 위주, accent는 최소한으로 + 타이포그래피로 위계 형성, 컬러보다 weight/size 활용

### Visual Adaptation Hints

- **cta_prominence**: CTA prominence는 medium이다. primary action은 분명하게 보이되 화면 전체를 지배하지 않게 유지한다. (source=cards; confidence=0.94; provenance=inferred; direction=low-elevation tinted cards를 기본으로 하고, 넓은 내부 여백과 강한 section breathing room. 중간 반경으로 제품 UI 절제 유지.; evidence=surface=tinted, density=airy, corner=medium, layout=conversation-panel)

### 레퍼런스 근거

- **Carbon Design System**: These components can toggle between the AI variant and the default variant depending on the user’s interaction. If the user manually overrides the ...
- **Primer**: I get so much joy from writing HTML and CSS, and design systems are one level up - systematically making UIs accessible and consistent. I love conc...

### 구현 노트

- 기존에 같은 역할의 컴포넌트가 있으면 토큰 교체부터 시작
- variant prop으로 시각적 변형을 관리 (하드코딩 금지)
- size prop: sm / md / lg (터치 영역은 항상 최소 44px 보장)
- 애니메이션은 상태 설명용으로만 사용, 장식 효과 금지
- 텍스트 위계가 핵심 — 컬러보다 weight/size로 구분

---

## copilot-artifact / message-artifact

**역할**: chat message 내 artifact 진입 카드 — 드래프트 미리보기 + 열기 CTA

**탐지 출처**: writing artifact

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

- [calm+editorial] hover: opacity 변화 (0.08-0.12), elevation 변화 없음 + 텍스트 underline 또는 color shift, 장식적 효과 없음
- [calm+editorial] motion: 150-200ms ease-out, bounce/spring 없음 + 콘텐츠 전환 위주, UI chrome 모션 최소화
- [calm+editorial] color: 중성 톤 위주, accent는 최소한으로 + 타이포그래피로 위계 형성, 컬러보다 weight/size 활용

### 구현 노트

- 기존에 같은 역할의 컴포넌트가 있으면 토큰 교체부터 시작
- variant prop으로 시각적 변형을 관리 (하드코딩 금지)
- 애니메이션은 상태 설명용으로만 사용, 장식 효과 금지
- 텍스트 위계가 핵심 — 컬러보다 weight/size로 구분

---

## copilot-artifact / artifact-preview-panel

**역할**: 우측 아티팩트 미리보기 패널 — draft document + outline + revision timeline

**탐지 출처**: writing artifact

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

- [calm+editorial] hover: opacity 변화 (0.08-0.12), elevation 변화 없음 + 텍스트 underline 또는 color shift, 장식적 효과 없음
- [calm+editorial] motion: 150-200ms ease-out, bounce/spring 없음 + 콘텐츠 전환 위주, UI chrome 모션 최소화
- [calm+editorial] color: 중성 톤 위주, accent는 최소한으로 + 타이포그래피로 위계 형성, 컬러보다 weight/size 활용

### Visual Adaptation Hints

- **card_elevation_tendency**: 카드는 낮은 elevation만 허용하고 색면 차이로 그룹을 구분한다. 내부 여백은 넉넉하게 두고 card breathing room을 확보한다. (source=cards; confidence=0.94; provenance=inferred; direction=low-elevation tinted cards를 기본으로 하고, 넓은 내부 여백과 강한 section breathing room. 중간 반경으로 제품 UI 절제 유지.; evidence=surface=tinted, density=airy, corner=medium)
- **border_vs_fill_emphasis**: fill 중심이다. tint surface로 성격을 만들고 border는 아주 얇게 보조한다. (source=cards; confidence=0.94; provenance=inferred; direction=low-elevation tinted cards를 기본으로 하고, 넓은 내부 여백과 강한 section breathing room. 중간 반경으로 제품 UI 절제 유지.; evidence=surface=tinted, density=airy, corner=medium)
- **chart_panel_framing**: 차트 패널은 soft tint frame과 restrained divider로 프레이밍한다. 헤더 메타데이터와 본문 visualization 사이의 breathing room을 충분히 둔다. (source=data_display; confidence=0.94; provenance=inferred; direction=정보 밀도를 유지하되 thin dividers와 restrained accent로 hierarchy를 만든다.; evidence=layout=dashboard-grid, density=airy, layout=conversation-panel, surface=tinted)

### 구현 노트

- 기존에 같은 역할의 컴포넌트가 있으면 토큰 교체부터 시작
- variant prop으로 시각적 변형을 관리 (하드코딩 금지)
- 애니메이션은 상태 설명용으로만 사용, 장식 효과 금지
- 텍스트 위계가 핵심 — 컬러보다 weight/size로 구분

---

## copilot-artifact / draft-document

**역할**: 에세이/뉴스레터/저널 드래프트 문서 본체 — reading-first 65–75ch

**탐지 출처**: writing artifact

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

- [calm+editorial] hover: opacity 변화 (0.08-0.12), elevation 변화 없음 + 텍스트 underline 또는 color shift, 장식적 효과 없음
- [calm+editorial] motion: 150-200ms ease-out, bounce/spring 없음 + 콘텐츠 전환 위주, UI chrome 모션 최소화
- [calm+editorial] color: 중성 톤 위주, accent는 최소한으로 + 타이포그래피로 위계 형성, 컬러보다 weight/size 활용

### 구현 노트

- 기존에 같은 역할의 컴포넌트가 있으면 토큰 교체부터 시작
- variant prop으로 시각적 변형을 관리 (하드코딩 금지)
- 애니메이션은 상태 설명용으로만 사용, 장식 효과 금지
- 텍스트 위계가 핵심 — 컬러보다 weight/size로 구분

---

## copilot-artifact / outline-sidebar

**역할**: heading anchor 기반 outline 목차 — 접기/펼치기

**탐지 출처**: writing artifact

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

- [calm+editorial] hover: opacity 변화 (0.08-0.12), elevation 변화 없음 + 텍스트 underline 또는 color shift, 장식적 효과 없음
- [calm+editorial] motion: 150-200ms ease-out, bounce/spring 없음 + 콘텐츠 전환 위주, UI chrome 모션 최소화
- [calm+editorial] color: 중성 톤 위주, accent는 최소한으로 + 타이포그래피로 위계 형성, 컬러보다 weight/size 활용

### Visual Adaptation Hints

- **filter_nav_density**: filter/nav density는 balanced다. global nav와 local filter를 섞지 말고 계층별 간격 차이로 구조를 드러낸다. (source=navigation; confidence=0.94; provenance=inferred; direction=고정 sidebar 또는 split-pane navigation을 우선하고, 현재 위치와 scope를 항상 명시한다.; evidence=Split-pane workspace, layout=conversation-panel, density=airy)

### 구현 노트

- 기존에 같은 역할의 컴포넌트가 있으면 토큰 교체부터 시작
- variant prop으로 시각적 변형을 관리 (하드코딩 금지)
- 애니메이션은 상태 설명용으로만 사용, 장식 효과 금지
- 텍스트 위계가 핵심 — 컬러보다 weight/size로 구분

---

## copilot-artifact / revision-timeline

**역할**: 드래프트 리비전 세로 타임라인 — 시간 순 diff preview 진입

**탐지 출처**: writing artifact

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

- [calm+editorial] hover: opacity 변화 (0.08-0.12), elevation 변화 없음 + 텍스트 underline 또는 color shift, 장식적 효과 없음
- [calm+editorial] motion: 150-200ms ease-out, bounce/spring 없음 + 콘텐츠 전환 위주, UI chrome 모션 최소화
- [calm+editorial] color: 중성 톤 위주, accent는 최소한으로 + 타이포그래피로 위계 형성, 컬러보다 weight/size 활용

### 구현 노트

- 기존에 같은 역할의 컴포넌트가 있으면 토큰 교체부터 시작
- variant prop으로 시각적 변형을 관리 (하드코딩 금지)
- 애니메이션은 상태 설명용으로만 사용, 장식 효과 금지
- 텍스트 위계가 핵심 — 컬러보다 weight/size로 구분

---

## input / tone-slider

**역할**: calm↔warm / formal↔casual tone slider — 아티팩트 재작성 트리거

**탐지 출처**: writing artifact

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

- [calm+editorial] hover: opacity 변화 (0.08-0.12), elevation 변화 없음 + 텍스트 underline 또는 color shift, 장식적 효과 없음
- [calm+editorial] density: comfortable 모드 기본, 여유로운 padding + 넉넉한 line-height와 margin, 읽기 편한 간격
- [calm+editorial] feedback: subtle inline alert 선호, 과한 컬러 블록 지양 + 콘텐츠 맥락 안에서 인라인 표시, 토스트보다 인라인 선호

### 레퍼런스 근거

- **Carbon Design System**: Number input Text input
- **Primer**: I worked in data visualization and map-making for most of my career, and solving design problems with data is my jam. To me there's something uniqu...

### 구현 노트

- 기존에 같은 역할의 컴포넌트가 있으면 토큰 교체부터 시작
- variant prop으로 시각적 변형을 관리 (하드코딩 금지)
- error 상태에서 helper text → error message로 자동 전환
- label은 항상 visible (placeholder만으로 대체 금지)
- 애니메이션은 상태 설명용으로만 사용, 장식 효과 금지
- 텍스트 위계가 핵심 — 컬러보다 weight/size로 구분

---

## copilot-artifact / reading-mode-toggle

**역할**: reading mode 토글 — wide/narrow · serif/sans · line-height

**탐지 출처**: writing artifact

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

- [calm+editorial] hover: opacity 변화 (0.08-0.12), elevation 변화 없음 + 텍스트 underline 또는 color shift, 장식적 효과 없음
- [calm+editorial] motion: 150-200ms ease-out, bounce/spring 없음 + 콘텐츠 전환 위주, UI chrome 모션 최소화
- [calm+editorial] color: 중성 톤 위주, accent는 최소한으로 + 타이포그래피로 위계 형성, 컬러보다 weight/size 활용

### 구현 노트

- 기존에 같은 역할의 컴포넌트가 있으면 토큰 교체부터 시작
- variant prop으로 시각적 변형을 관리 (하드코딩 금지)
- 애니메이션은 상태 설명용으로만 사용, 장식 효과 금지
- 텍스트 위계가 핵심 — 컬러보다 weight/size로 구분

---

## copilot-artifact / citation-footnote

**역할**: 아티팩트 하단 주석 · 인용 출처 목록

**탐지 출처**: writing artifact

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

- [calm+editorial] hover: opacity 변화 (0.08-0.12), elevation 변화 없음 + 텍스트 underline 또는 color shift, 장식적 효과 없음
- [calm+editorial] motion: 150-200ms ease-out, bounce/spring 없음 + 콘텐츠 전환 위주, UI chrome 모션 최소화
- [calm+editorial] color: 중성 톤 위주, accent는 최소한으로 + 타이포그래피로 위계 형성, 컬러보다 weight/size 활용

### 구현 노트

- 기존에 같은 역할의 컴포넌트가 있으면 토큰 교체부터 시작
- variant prop으로 시각적 변형을 관리 (하드코딩 금지)
- 애니메이션은 상태 설명용으로만 사용, 장식 효과 금지
- 텍스트 위계가 핵심 — 컬러보다 weight/size로 구분

---

## copilot-artifact / quote-block

**역할**: 인용문 블록 — serif italic, muted vertical rule

**탐지 출처**: writing artifact

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

- [calm+editorial] hover: opacity 변화 (0.08-0.12), elevation 변화 없음 + 텍스트 underline 또는 color shift, 장식적 효과 없음
- [calm+editorial] motion: 150-200ms ease-out, bounce/spring 없음 + 콘텐츠 전환 위주, UI chrome 모션 최소화
- [calm+editorial] color: 중성 톤 위주, accent는 최소한으로 + 타이포그래피로 위계 형성, 컬러보다 weight/size 활용

### 구현 노트

- 기존에 같은 역할의 컴포넌트가 있으면 토큰 교체부터 시작
- variant prop으로 시각적 변형을 관리 (하드코딩 금지)
- 애니메이션은 상태 설명용으로만 사용, 장식 효과 금지
- 텍스트 위계가 핵심 — 컬러보다 weight/size로 구분

---

## copilot-artifact / paragraph-block

**역할**: 본문 문단 블록 — reading pane line-height 1.6–1.7

**탐지 출처**: writing artifact

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

- [calm+editorial] hover: opacity 변화 (0.08-0.12), elevation 변화 없음 + 텍스트 underline 또는 color shift, 장식적 효과 없음
- [calm+editorial] motion: 150-200ms ease-out, bounce/spring 없음 + 콘텐츠 전환 위주, UI chrome 모션 최소화
- [calm+editorial] color: 중성 톤 위주, accent는 최소한으로 + 타이포그래피로 위계 형성, 컬러보다 weight/size 활용

### 구현 노트

- 기존에 같은 역할의 컴포넌트가 있으면 토큰 교체부터 시작
- variant prop으로 시각적 변형을 관리 (하드코딩 금지)
- 애니메이션은 상태 설명용으로만 사용, 장식 효과 금지
- 텍스트 위계가 핵심 — 컬러보다 weight/size로 구분

---

## input / prompt-composer

**역할**: 멀티라인 prompt composer — 수납형 grow, 한글 IME keep-all, 제출/개행 규칙

**탐지 출처**: conversation copilot chrome

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

- [calm+editorial] hover: opacity 변화 (0.08-0.12), elevation 변화 없음 + 텍스트 underline 또는 color shift, 장식적 효과 없음
- [calm+editorial] density: comfortable 모드 기본, 여유로운 padding + 넉넉한 line-height와 margin, 읽기 편한 간격
- [calm+editorial] feedback: subtle inline alert 선호, 과한 컬러 블록 지양 + 콘텐츠 맥락 안에서 인라인 표시, 토스트보다 인라인 선호

### 레퍼런스 근거

- **Carbon Design System**: Number input Text input
- **Primer**: I worked in data visualization and map-making for most of my career, and solving design problems with data is my jam. To me there's something uniqu...

### 구현 노트

- 기존에 같은 역할의 컴포넌트가 있으면 토큰 교체부터 시작
- variant prop으로 시각적 변형을 관리 (하드코딩 금지)
- error 상태에서 helper text → error message로 자동 전환
- label은 항상 visible (placeholder만으로 대체 금지)
- 애니메이션은 상태 설명용으로만 사용, 장식 효과 금지
- 텍스트 위계가 핵심 — 컬러보다 weight/size로 구분

---

## copilot-chat / streaming-cursor

**역할**: 응답 생성 중 calm blinking cursor — slow fade, prefers-reduced-motion 존중

**탐지 출처**: conversation copilot chrome

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

- [calm+editorial] hover: opacity 변화 (0.08-0.12), elevation 변화 없음 + 텍스트 underline 또는 color shift, 장식적 효과 없음
- [calm+editorial] motion: 150-200ms ease-out, bounce/spring 없음 + 콘텐츠 전환 위주, UI chrome 모션 최소화
- [calm+editorial] color: 중성 톤 위주, accent는 최소한으로 + 타이포그래피로 위계 형성, 컬러보다 weight/size 활용

### 구현 노트

- 기존에 같은 역할의 컴포넌트가 있으면 토큰 교체부터 시작
- variant prop으로 시각적 변형을 관리 (하드코딩 금지)
- 애니메이션은 상태 설명용으로만 사용, 장식 효과 금지
- 텍스트 위계가 핵심 — 컬러보다 weight/size로 구분

---

## copilot-chat / typing-indicator

**역할**: 'copilot is thinking…' typing dots — low-noise 상태

**탐지 출처**: conversation copilot chrome

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

- [calm+editorial] hover: opacity 변화 (0.08-0.12), elevation 변화 없음 + 텍스트 underline 또는 color shift, 장식적 효과 없음
- [calm+editorial] motion: 150-200ms ease-out, bounce/spring 없음 + 콘텐츠 전환 위주, UI chrome 모션 최소화
- [calm+editorial] color: 중성 톤 위주, accent는 최소한으로 + 타이포그래피로 위계 형성, 컬러보다 weight/size 활용

### 구현 노트

- 기존에 같은 역할의 컴포넌트가 있으면 토큰 교체부터 시작
- variant prop으로 시각적 변형을 관리 (하드코딩 금지)
- 애니메이션은 상태 설명용으로만 사용, 장식 효과 금지
- 텍스트 위계가 핵심 — 컬러보다 weight/size로 구분

---

## copilot-chat / inline-citation

**역할**: 본문 내 citation 번호/괄호 링크 — hover tooltip + footnote 연결

**탐지 출처**: conversation copilot chrome

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

- [calm+editorial] hover: opacity 변화 (0.08-0.12), elevation 변화 없음 + 텍스트 underline 또는 color shift, 장식적 효과 없음
- [calm+editorial] motion: 150-200ms ease-out, bounce/spring 없음 + 콘텐츠 전환 위주, UI chrome 모션 최소화
- [calm+editorial] color: 중성 톤 위주, accent는 최소한으로 + 타이포그래피로 위계 형성, 컬러보다 weight/size 활용

### 구현 노트

- 기존에 같은 역할의 컴포넌트가 있으면 토큰 교체부터 시작
- variant prop으로 시각적 변형을 관리 (하드코딩 금지)
- 애니메이션은 상태 설명용으로만 사용, 장식 효과 금지
- 텍스트 위계가 핵심 — 컬러보다 weight/size로 구분

---

## button / regenerate-button

**역할**: 응답 재생성 버튼 — ghost serif label, 생성 완료 후 활성

**탐지 출처**: conversation copilot chrome

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

- [calm+editorial] hover: opacity 변화 (0.08-0.12), elevation 변화 없음 + 텍스트 underline 또는 color shift, 장식적 효과 없음
- [calm+editorial] motion: 150-200ms ease-out, bounce/spring 없음 + 콘텐츠 전환 위주, UI chrome 모션 최소화
- [calm+editorial] color: 중성 톤 위주, accent는 최소한으로 + 타이포그래피로 위계 형성, 컬러보다 weight/size 활용

### Visual Adaptation Hints

- **cta_prominence**: CTA prominence는 medium이다. primary action은 분명하게 보이되 화면 전체를 지배하지 않게 유지한다. (source=cards; confidence=0.94; provenance=inferred; direction=low-elevation tinted cards를 기본으로 하고, 넓은 내부 여백과 강한 section breathing room. 중간 반경으로 제품 UI 절제 유지.; evidence=surface=tinted, density=airy, corner=medium, layout=conversation-panel)

### 레퍼런스 근거

- **Carbon Design System**: These components can toggle between the AI variant and the default variant depending on the user’s interaction. If the user manually overrides the ...
- **Primer**: I get so much joy from writing HTML and CSS, and design systems are one level up - systematically making UIs accessible and consistent. I love conc...

### 구현 노트

- 기존에 같은 역할의 컴포넌트가 있으면 토큰 교체부터 시작
- variant prop으로 시각적 변형을 관리 (하드코딩 금지)
- size prop: sm / md / lg (터치 영역은 항상 최소 44px 보장)
- 애니메이션은 상태 설명용으로만 사용, 장식 효과 금지
- 텍스트 위계가 핵심 — 컬러보다 weight/size로 구분

---

## button / stop-generation-button

**역할**: 응답 중단 버튼 — muted danger ghost, 생성 중에만 활성

**탐지 출처**: conversation copilot chrome

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

- [calm+editorial] hover: opacity 변화 (0.08-0.12), elevation 변화 없음 + 텍스트 underline 또는 color shift, 장식적 효과 없음
- [calm+editorial] motion: 150-200ms ease-out, bounce/spring 없음 + 콘텐츠 전환 위주, UI chrome 모션 최소화
- [calm+editorial] color: 중성 톤 위주, accent는 최소한으로 + 타이포그래피로 위계 형성, 컬러보다 weight/size 활용

### Visual Adaptation Hints

- **cta_prominence**: CTA prominence는 medium이다. primary action은 분명하게 보이되 화면 전체를 지배하지 않게 유지한다. (source=cards; confidence=0.94; provenance=inferred; direction=low-elevation tinted cards를 기본으로 하고, 넓은 내부 여백과 강한 section breathing room. 중간 반경으로 제품 UI 절제 유지.; evidence=surface=tinted, density=airy, corner=medium, layout=conversation-panel)

### 레퍼런스 근거

- **Carbon Design System**: These components can toggle between the AI variant and the default variant depending on the user’s interaction. If the user manually overrides the ...
- **Primer**: I get so much joy from writing HTML and CSS, and design systems are one level up - systematically making UIs accessible and consistent. I love conc...

### 구현 노트

- 기존에 같은 역할의 컴포넌트가 있으면 토큰 교체부터 시작
- variant prop으로 시각적 변형을 관리 (하드코딩 금지)
- size prop: sm / md / lg (터치 영역은 항상 최소 44px 보장)
- 애니메이션은 상태 설명용으로만 사용, 장식 효과 금지
- 텍스트 위계가 핵심 — 컬러보다 weight/size로 구분

---

## copilot-chat / mention-chip

**역할**: @thread/@citation/@note mention 칩 — muted accent fill

**탐지 출처**: conversation copilot chrome

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

- [calm+editorial] hover: opacity 변화 (0.08-0.12), elevation 변화 없음 + 텍스트 underline 또는 color shift, 장식적 효과 없음
- [calm+editorial] motion: 150-200ms ease-out, bounce/spring 없음 + 콘텐츠 전환 위주, UI chrome 모션 최소화
- [calm+editorial] color: 중성 톤 위주, accent는 최소한으로 + 타이포그래피로 위계 형성, 컬러보다 weight/size 활용

### Visual Adaptation Hints

- **filter_nav_density**: filter/nav density는 balanced다. global nav와 local filter를 섞지 말고 계층별 간격 차이로 구조를 드러낸다. (source=navigation; confidence=0.94; provenance=inferred; direction=고정 sidebar 또는 split-pane navigation을 우선하고, 현재 위치와 scope를 항상 명시한다.; evidence=Split-pane workspace, layout=conversation-panel, density=airy)

### 구현 노트

- 기존에 같은 역할의 컴포넌트가 있으면 토큰 교체부터 시작
- variant prop으로 시각적 변형을 관리 (하드코딩 금지)
- 애니메이션은 상태 설명용으로만 사용, 장식 효과 금지
- 텍스트 위계가 핵심 — 컬러보다 weight/size로 구분

---

## copilot-chat / suggestion-card

**역할**: prompt 시작 suggestion card — 에세이/뉴스레터/저널 editorial 스타터

**탐지 출처**: conversation copilot chrome

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

- [calm+editorial] hover: opacity 변화 (0.08-0.12), elevation 변화 없음 + 텍스트 underline 또는 color shift, 장식적 효과 없음
- [calm+editorial] motion: 150-200ms ease-out, bounce/spring 없음 + 콘텐츠 전환 위주, UI chrome 모션 최소화
- [calm+editorial] color: 중성 톤 위주, accent는 최소한으로 + 타이포그래피로 위계 형성, 컬러보다 weight/size 활용

### Visual Adaptation Hints

- **card_elevation_tendency**: 카드는 낮은 elevation만 허용하고 색면 차이로 그룹을 구분한다. 내부 여백은 넉넉하게 두고 card breathing room을 확보한다. (source=cards; confidence=0.94; provenance=inferred; direction=low-elevation tinted cards를 기본으로 하고, 넓은 내부 여백과 강한 section breathing room. 중간 반경으로 제품 UI 절제 유지.; evidence=surface=tinted, density=airy, corner=medium)
- **border_vs_fill_emphasis**: fill 중심이다. tint surface로 성격을 만들고 border는 아주 얇게 보조한다. (source=cards; confidence=0.94; provenance=inferred; direction=low-elevation tinted cards를 기본으로 하고, 넓은 내부 여백과 강한 section breathing room. 중간 반경으로 제품 UI 절제 유지.; evidence=surface=tinted, density=airy, corner=medium)

### 구현 노트

- 기존에 같은 역할의 컴포넌트가 있으면 토큰 교체부터 시작
- variant prop으로 시각적 변형을 관리 (하드코딩 금지)
- 애니메이션은 상태 설명용으로만 사용, 장식 효과 금지
- 텍스트 위계가 핵심 — 컬러보다 weight/size로 구분

---

## copilot-chat / thread-header

**역할**: 현재 thread 제목 · 작성 시점 · 아카이브 토글 — restrained editorial chrome

**탐지 출처**: conversation copilot chrome

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

- [calm+editorial] hover: opacity 변화 (0.08-0.12), elevation 변화 없음 + 텍스트 underline 또는 color shift, 장식적 효과 없음
- [calm+editorial] motion: 150-200ms ease-out, bounce/spring 없음 + 콘텐츠 전환 위주, UI chrome 모션 최소화
- [calm+editorial] color: 중성 톤 위주, accent는 최소한으로 + 타이포그래피로 위계 형성, 컬러보다 weight/size 활용

### 구현 노트

- 기존에 같은 역할의 컴포넌트가 있으면 토큰 교체부터 시작
- variant prop으로 시각적 변형을 관리 (하드코딩 금지)
- 애니메이션은 상태 설명용으로만 사용, 장식 효과 금지
- 텍스트 위계가 핵심 — 컬러보다 weight/size로 구분

---

## button / new-thread-button

**역할**: 새 대화 시작 버튼 — warm accent primary

**탐지 출처**: conversation copilot chrome

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

- [calm+editorial] hover: opacity 변화 (0.08-0.12), elevation 변화 없음 + 텍스트 underline 또는 color shift, 장식적 효과 없음
- [calm+editorial] motion: 150-200ms ease-out, bounce/spring 없음 + 콘텐츠 전환 위주, UI chrome 모션 최소화
- [calm+editorial] color: 중성 톤 위주, accent는 최소한으로 + 타이포그래피로 위계 형성, 컬러보다 weight/size 활용

### Visual Adaptation Hints

- **cta_prominence**: CTA prominence는 medium이다. primary action은 분명하게 보이되 화면 전체를 지배하지 않게 유지한다. (source=cards; confidence=0.94; provenance=inferred; direction=low-elevation tinted cards를 기본으로 하고, 넓은 내부 여백과 강한 section breathing room. 중간 반경으로 제품 UI 절제 유지.; evidence=surface=tinted, density=airy, corner=medium, layout=conversation-panel)

### 레퍼런스 근거

- **Carbon Design System**: These components can toggle between the AI variant and the default variant depending on the user’s interaction. If the user manually overrides the ...
- **Primer**: I get so much joy from writing HTML and CSS, and design systems are one level up - systematically making UIs accessible and consistent. I love conc...

### 구현 노트

- 기존에 같은 역할의 컴포넌트가 있으면 토큰 교체부터 시작
- variant prop으로 시각적 변형을 관리 (하드코딩 금지)
- size prop: sm / md / lg (터치 영역은 항상 최소 44px 보장)
- 애니메이션은 상태 설명용으로만 사용, 장식 효과 금지
- 텍스트 위계가 핵심 — 컬러보다 weight/size로 구분

---

## feedback / empty-conversation-state

**역할**: empty conversation 안내 — 일러스트 + gentle 온보딩 카피 + suggestion card

**탐지 출처**: conversation copilot chrome

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

- [calm+editorial] feedback: subtle inline alert 선호, 과한 컬러 블록 지양 + 콘텐츠 맥락 안에서 인라인 표시, 토스트보다 인라인 선호
- [calm+editorial] motion: 150-200ms ease-out, bounce/spring 없음 + 콘텐츠 전환 위주, UI chrome 모션 최소화
- [calm+editorial] color: 중성 톤 위주, accent는 최소한으로 + 타이포그래피로 위계 형성, 컬러보다 weight/size 활용

### Visual Adaptation Hints

- **card_elevation_tendency**: 카드는 낮은 elevation만 허용하고 색면 차이로 그룹을 구분한다. 내부 여백은 넉넉하게 두고 card breathing room을 확보한다. (source=cards; confidence=0.94; provenance=inferred; direction=low-elevation tinted cards를 기본으로 하고, 넓은 내부 여백과 강한 section breathing room. 중간 반경으로 제품 UI 절제 유지.; evidence=surface=tinted, density=airy, corner=medium)
- **border_vs_fill_emphasis**: fill 중심이다. tint surface로 성격을 만들고 border는 아주 얇게 보조한다. (source=cards; confidence=0.94; provenance=inferred; direction=low-elevation tinted cards를 기본으로 하고, 넓은 내부 여백과 강한 section breathing room. 중간 반경으로 제품 UI 절제 유지.; evidence=surface=tinted, density=airy, corner=medium)
- **chart_panel_framing**: 차트 패널은 soft tint frame과 restrained divider로 프레이밍한다. 헤더 메타데이터와 본문 visualization 사이의 breathing room을 충분히 둔다. (source=data_display; confidence=0.94; provenance=inferred; direction=정보 밀도를 유지하되 thin dividers와 restrained accent로 hierarchy를 만든다.; evidence=layout=dashboard-grid, density=airy, layout=conversation-panel, surface=tinted)

### 레퍼런스 근거

- **Carbon Design System**: We welcome all feedback, designs, or ideas in order to produce the best possible experience for our users. If you're interested in contributing, ch...
- **Primer**: Messaging components are used to provide important and relevant information to the user, including feedback, contextual information, product update...

### 구현 노트

- 기존에 같은 역할의 컴포넌트가 있으면 토큰 교체부터 시작
- variant prop으로 시각적 변형을 관리 (하드코딩 금지)
- auto-dismiss 시간은 내용 길이에 비례 (기본 5초)
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

- [calm+editorial] density: comfortable 모드 기본, 여유로운 padding + 넉넉한 line-height와 margin, 읽기 편한 간격
- [calm+editorial] color: 중성 톤 위주, accent는 최소한으로 + 타이포그래피로 위계 형성, 컬러보다 weight/size 활용
- [calm+editorial] motion: 150-200ms ease-out, bounce/spring 없음 + 콘텐츠 전환 위주, UI chrome 모션 최소화

### 구현 노트

- 기존에 같은 역할의 컴포넌트가 있으면 토큰 교체부터 시작
- variant prop으로 시각적 변형을 관리 (하드코딩 금지)
- 블록 단위 데이터 모델, JSON 직렬화 가능한 구조
- 한글 헤딩은 `word-break: keep-all` / `overflow-wrap: normal`을 기본값으로 두고, 강제 `<br />`는 breakpoint 검증 전 넣지 않음
- 한글 hero/section heading은 영문 시안보다 한 단계 작은 스케일에서 시작해 wrap을 확인한 뒤 확장한다.
- 좁은 UI 텍스트는 Pretendard 기준 label line-height 1.4-1.5를 참고해 뭉침을 방지
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

- [calm+editorial] density: comfortable 모드 기본, 여유로운 padding + 넉넉한 line-height와 margin, 읽기 편한 간격
- [calm+editorial] color: 중성 톤 위주, accent는 최소한으로 + 타이포그래피로 위계 형성, 컬러보다 weight/size 활용
- [calm+editorial] motion: 150-200ms ease-out, bounce/spring 없음 + 콘텐츠 전환 위주, UI chrome 모션 최소화

### Visual Adaptation Hints

- **filter_nav_density**: filter/nav density는 balanced다. global nav와 local filter를 섞지 말고 계층별 간격 차이로 구조를 드러낸다. (source=navigation; confidence=0.94; provenance=inferred; direction=고정 sidebar 또는 split-pane navigation을 우선하고, 현재 위치와 scope를 항상 명시한다.; evidence=Split-pane workspace, layout=conversation-panel, density=airy)

### 구현 노트

- 기존에 같은 역할의 컴포넌트가 있으면 토큰 교체부터 시작
- variant prop으로 시각적 변형을 관리 (하드코딩 금지)
- 블록 단위 데이터 모델, JSON 직렬화 가능한 구조
- 한글 헤딩은 `word-break: keep-all` / `overflow-wrap: normal`을 기본값으로 두고, 강제 `<br />`는 breakpoint 검증 전 넣지 않음
- 한글 hero/section heading은 영문 시안보다 한 단계 작은 스케일에서 시작해 wrap을 확인한 뒤 확장한다.
- 좁은 UI 텍스트는 Pretendard 기준 label line-height 1.4-1.5를 참고해 뭉침을 방지
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

- [calm+editorial] density: comfortable 모드 기본, 여유로운 padding + 넉넉한 line-height와 margin, 읽기 편한 간격
- [calm+editorial] color: 중성 톤 위주, accent는 최소한으로 + 타이포그래피로 위계 형성, 컬러보다 weight/size 활용
- [calm+editorial] motion: 150-200ms ease-out, bounce/spring 없음 + 콘텐츠 전환 위주, UI chrome 모션 최소화

### Visual Adaptation Hints

- **filter_nav_density**: filter/nav density는 balanced다. global nav와 local filter를 섞지 말고 계층별 간격 차이로 구조를 드러낸다. (source=navigation; confidence=0.94; provenance=inferred; direction=고정 sidebar 또는 split-pane navigation을 우선하고, 현재 위치와 scope를 항상 명시한다.; evidence=Split-pane workspace, layout=conversation-panel, density=airy)

### 구현 노트

- 기존에 같은 역할의 컴포넌트가 있으면 토큰 교체부터 시작
- variant prop으로 시각적 변형을 관리 (하드코딩 금지)
- 블록 단위 데이터 모델, JSON 직렬화 가능한 구조
- 한글 헤딩은 `word-break: keep-all` / `overflow-wrap: normal`을 기본값으로 두고, 강제 `<br />`는 breakpoint 검증 전 넣지 않음
- 한글 hero/section heading은 영문 시안보다 한 단계 작은 스케일에서 시작해 wrap을 확인한 뒤 확장한다.
- 좁은 UI 텍스트는 Pretendard 기준 label line-height 1.4-1.5를 참고해 뭉침을 방지
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

- [calm+editorial] density: comfortable 모드 기본, 여유로운 padding + 넉넉한 line-height와 margin, 읽기 편한 간격
- [calm+editorial] color: 중성 톤 위주, accent는 최소한으로 + 타이포그래피로 위계 형성, 컬러보다 weight/size 활용
- [calm+editorial] motion: 150-200ms ease-out, bounce/spring 없음 + 콘텐츠 전환 위주, UI chrome 모션 최소화

### Visual Adaptation Hints

- **filter_nav_density**: filter/nav density는 balanced다. global nav와 local filter를 섞지 말고 계층별 간격 차이로 구조를 드러낸다. (source=navigation; confidence=0.94; provenance=inferred; direction=고정 sidebar 또는 split-pane navigation을 우선하고, 현재 위치와 scope를 항상 명시한다.; evidence=Split-pane workspace, layout=conversation-panel, density=airy)

### 구현 노트

- 기존에 같은 역할의 컴포넌트가 있으면 토큰 교체부터 시작
- variant prop으로 시각적 변형을 관리 (하드코딩 금지)
- 블록 단위 데이터 모델, JSON 직렬화 가능한 구조
- 한글 헤딩은 `word-break: keep-all` / `overflow-wrap: normal`을 기본값으로 두고, 강제 `<br />`는 breakpoint 검증 전 넣지 않음
- 한글 hero/section heading은 영문 시안보다 한 단계 작은 스케일에서 시작해 wrap을 확인한 뒤 확장한다.
- 좁은 UI 텍스트는 Pretendard 기준 label line-height 1.4-1.5를 참고해 뭉침을 방지
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

- [calm+editorial] density: comfortable 모드 기본, 여유로운 padding + 넉넉한 line-height와 margin, 읽기 편한 간격
- [calm+editorial] color: 중성 톤 위주, accent는 최소한으로 + 타이포그래피로 위계 형성, 컬러보다 weight/size 활용
- [calm+editorial] motion: 150-200ms ease-out, bounce/spring 없음 + 콘텐츠 전환 위주, UI chrome 모션 최소화

### 구현 노트

- 기존에 같은 역할의 컴포넌트가 있으면 토큰 교체부터 시작
- variant prop으로 시각적 변형을 관리 (하드코딩 금지)
- 블록 단위 데이터 모델, JSON 직렬화 가능한 구조
- 한글 헤딩은 `word-break: keep-all` / `overflow-wrap: normal`을 기본값으로 두고, 강제 `<br />`는 breakpoint 검증 전 넣지 않음
- 한글 hero/section heading은 영문 시안보다 한 단계 작은 스케일에서 시작해 wrap을 확인한 뒤 확장한다.
- 좁은 UI 텍스트는 Pretendard 기준 label line-height 1.4-1.5를 참고해 뭉침을 방지
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

- [calm+editorial] density: comfortable 모드 기본, 여유로운 padding + 넉넉한 line-height와 margin, 읽기 편한 간격
- [calm+editorial] color: 중성 톤 위주, accent는 최소한으로 + 타이포그래피로 위계 형성, 컬러보다 weight/size 활용

### Visual Adaptation Hints

- **card_elevation_tendency**: 카드는 낮은 elevation만 허용하고 색면 차이로 그룹을 구분한다. 내부 여백은 넉넉하게 두고 card breathing room을 확보한다. (source=cards; confidence=0.94; provenance=inferred; direction=low-elevation tinted cards를 기본으로 하고, 넓은 내부 여백과 강한 section breathing room. 중간 반경으로 제품 UI 절제 유지.; evidence=surface=tinted, density=airy, corner=medium)
- **border_vs_fill_emphasis**: fill 중심이다. tint surface로 성격을 만들고 border는 아주 얇게 보조한다. (source=cards; confidence=0.94; provenance=inferred; direction=low-elevation tinted cards를 기본으로 하고, 넓은 내부 여백과 강한 section breathing room. 중간 반경으로 제품 UI 절제 유지.; evidence=surface=tinted, density=airy, corner=medium)
- **chart_panel_framing**: 차트 패널은 soft tint frame과 restrained divider로 프레이밍한다. 헤더 메타데이터와 본문 visualization 사이의 breathing room을 충분히 둔다. (source=data_display; confidence=0.94; provenance=inferred; direction=정보 밀도를 유지하되 thin dividers와 restrained accent로 hierarchy를 만든다.; evidence=layout=dashboard-grid, density=airy, layout=conversation-panel, surface=tinted)

### 구현 노트

- 기존에 같은 역할의 컴포넌트가 있으면 토큰 교체부터 시작
- variant prop으로 시각적 변형을 관리 (하드코딩 금지)
- 빈 상태(empty-state)와 에러 상태를 반드시 처리
- 좁은 UI 텍스트는 Pretendard 기준 label line-height 1.4-1.5를 참고해 뭉침을 방지
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

- [calm+editorial] hover: opacity 변화 (0.08-0.12), elevation 변화 없음 + 텍스트 underline 또는 color shift, 장식적 효과 없음
- [calm+editorial] density: comfortable 모드 기본, 여유로운 padding + 넉넉한 line-height와 margin, 읽기 편한 간격
- [calm+editorial] feedback: subtle inline alert 선호, 과한 컬러 블록 지양 + 콘텐츠 맥락 안에서 인라인 표시, 토스트보다 인라인 선호

### 레퍼런스 근거

- **Carbon Design System**: Number input Text input
- **Primer**: I worked in data visualization and map-making for most of my career, and solving design problems with data is my jam. To me there's something uniqu...

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

- [calm+editorial] motion: 150-200ms ease-out, bounce/spring 없음 + 콘텐츠 전환 위주, UI chrome 모션 최소화
- [calm+editorial] density: comfortable 모드 기본, 여유로운 padding + 넉넉한 line-height와 margin, 읽기 편한 간격

### 레퍼런스 근거

- **Primer**: ActionMenu is composed of ActionList and Overlay patterns used for quick actions and selections. AnchoredOverlay

### 구현 노트

- 기존에 같은 역할의 컴포넌트가 있으면 토큰 교체부터 시작
- variant prop으로 시각적 변형을 관리 (하드코딩 금지)
- Escape / backdrop click으로 닫기, 열 때 첫 focusable 요소로 이동
- 애니메이션은 상태 설명용으로만 사용, 장식 효과 금지
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

- [calm+editorial] density: comfortable 모드 기본, 여유로운 padding + 넉넉한 line-height와 margin, 읽기 편한 간격
- [calm+editorial] color: 중성 톤 위주, accent는 최소한으로 + 타이포그래피로 위계 형성, 컬러보다 weight/size 활용

### Visual Adaptation Hints

- **card_elevation_tendency**: 카드는 낮은 elevation만 허용하고 색면 차이로 그룹을 구분한다. 내부 여백은 넉넉하게 두고 card breathing room을 확보한다. (source=cards; confidence=0.94; provenance=inferred; direction=low-elevation tinted cards를 기본으로 하고, 넓은 내부 여백과 강한 section breathing room. 중간 반경으로 제품 UI 절제 유지.; evidence=surface=tinted, density=airy, corner=medium)
- **border_vs_fill_emphasis**: fill 중심이다. tint surface로 성격을 만들고 border는 아주 얇게 보조한다. (source=cards; confidence=0.94; provenance=inferred; direction=low-elevation tinted cards를 기본으로 하고, 넓은 내부 여백과 강한 section breathing room. 중간 반경으로 제품 UI 절제 유지.; evidence=surface=tinted, density=airy, corner=medium)
- **chart_panel_framing**: 차트 패널은 soft tint frame과 restrained divider로 프레이밍한다. 헤더 메타데이터와 본문 visualization 사이의 breathing room을 충분히 둔다. (source=data_display; confidence=0.94; provenance=inferred; direction=정보 밀도를 유지하되 thin dividers와 restrained accent로 hierarchy를 만든다.; evidence=layout=dashboard-grid, density=airy, layout=conversation-panel, surface=tinted)

### 구현 노트

- 기존에 같은 역할의 컴포넌트가 있으면 토큰 교체부터 시작
- variant prop으로 시각적 변형을 관리 (하드코딩 금지)
- 빈 상태(empty-state)와 에러 상태를 반드시 처리
- 좁은 UI 텍스트는 Pretendard 기준 label line-height 1.4-1.5를 참고해 뭉침을 방지
- 애니메이션은 상태 설명용으로만 사용, 장식 효과 금지
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

- [calm+editorial] hover: opacity 변화 (0.08-0.12), elevation 변화 없음 + 텍스트 underline 또는 color shift, 장식적 효과 없음
- [calm+editorial] density: comfortable 모드 기본, 여유로운 padding + 넉넉한 line-height와 margin, 읽기 편한 간격
- [calm+editorial] feedback: subtle inline alert 선호, 과한 컬러 블록 지양 + 콘텐츠 맥락 안에서 인라인 표시, 토스트보다 인라인 선호

### 레퍼런스 근거

- **Carbon Design System**: Number input Text input
- **Primer**: I worked in data visualization and map-making for most of my career, and solving design problems with data is my jam. To me there's something uniqu...

### 구현 노트

- 기존에 같은 역할의 컴포넌트가 있으면 토큰 교체부터 시작
- variant prop으로 시각적 변형을 관리 (하드코딩 금지)
- error 상태에서 helper text → error message로 자동 전환
- label은 항상 visible (placeholder만으로 대체 금지)
- 애니메이션은 상태 설명용으로만 사용, 장식 효과 금지
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

- [calm+editorial] density: comfortable 모드 기본, 여유로운 padding + 넉넉한 line-height와 margin, 읽기 편한 간격
- [calm+editorial] color: 중성 톤 위주, accent는 최소한으로 + 타이포그래피로 위계 형성, 컬러보다 weight/size 활용

### Visual Adaptation Hints

- **card_elevation_tendency**: 카드는 낮은 elevation만 허용하고 색면 차이로 그룹을 구분한다. 내부 여백은 넉넉하게 두고 card breathing room을 확보한다. (source=cards; confidence=0.94; provenance=inferred; direction=low-elevation tinted cards를 기본으로 하고, 넓은 내부 여백과 강한 section breathing room. 중간 반경으로 제품 UI 절제 유지.; evidence=surface=tinted, density=airy, corner=medium)
- **border_vs_fill_emphasis**: fill 중심이다. tint surface로 성격을 만들고 border는 아주 얇게 보조한다. (source=cards; confidence=0.94; provenance=inferred; direction=low-elevation tinted cards를 기본으로 하고, 넓은 내부 여백과 강한 section breathing room. 중간 반경으로 제품 UI 절제 유지.; evidence=surface=tinted, density=airy, corner=medium)
- **chart_panel_framing**: 차트 패널은 soft tint frame과 restrained divider로 프레이밍한다. 헤더 메타데이터와 본문 visualization 사이의 breathing room을 충분히 둔다. (source=data_display; confidence=0.94; provenance=inferred; direction=정보 밀도를 유지하되 thin dividers와 restrained accent로 hierarchy를 만든다.; evidence=layout=dashboard-grid, density=airy, layout=conversation-panel, surface=tinted)

### 구현 노트

- 기존에 같은 역할의 컴포넌트가 있으면 토큰 교체부터 시작
- variant prop으로 시각적 변형을 관리 (하드코딩 금지)
- 빈 상태(empty-state)와 에러 상태를 반드시 처리
- 좁은 UI 텍스트는 Pretendard 기준 label line-height 1.4-1.5를 참고해 뭉침을 방지
- 애니메이션은 상태 설명용으로만 사용, 장식 효과 금지
- 텍스트 위계가 핵심 — 컬러보다 weight/size로 구분

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

- [calm+editorial] hover: opacity 변화 (0.08-0.12), elevation 변화 없음 + 텍스트 underline 또는 color shift, 장식적 효과 없음
- [calm+editorial] motion: 150-200ms ease-out, bounce/spring 없음 + 콘텐츠 전환 위주, UI chrome 모션 최소화
- [calm+editorial] color: 중성 톤 위주, accent는 최소한으로 + 타이포그래피로 위계 형성, 컬러보다 weight/size 활용

### 레퍼런스 근거

- **Carbon Design System**: AI chat is a conversational framework between a user and an AI that can aid in creating tasks, finding insights, tracking documents, and more. For ...
- **Primer**: The GitHub Design Infrastructure and Design Engineering teams build and maintain Primer — this includes our CSS framework, style guide documentatio...

### 구현 노트

- 기존에 같은 역할의 컴포넌트가 있으면 토큰 교체부터 시작
- variant prop으로 시각적 변형을 관리 (하드코딩 금지)
- 애니메이션은 상태 설명용으로만 사용, 장식 효과 금지
- 텍스트 위계가 핵심 — 컬러보다 weight/size로 구분

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

- [calm+editorial] hover: opacity 변화 (0.08-0.12), elevation 변화 없음 + 텍스트 underline 또는 color shift, 장식적 효과 없음
- [calm+editorial] motion: 150-200ms ease-out, bounce/spring 없음 + 콘텐츠 전환 위주, UI chrome 모션 최소화
- [calm+editorial] color: 중성 톤 위주, accent는 최소한으로 + 타이포그래피로 위계 형성, 컬러보다 weight/size 활용

### Visual Adaptation Hints

- **card_elevation_tendency**: 카드는 낮은 elevation만 허용하고 색면 차이로 그룹을 구분한다. 내부 여백은 넉넉하게 두고 card breathing room을 확보한다. (source=cards; confidence=0.94; provenance=inferred; direction=low-elevation tinted cards를 기본으로 하고, 넓은 내부 여백과 강한 section breathing room. 중간 반경으로 제품 UI 절제 유지.; evidence=surface=tinted, density=airy, corner=medium)
- **border_vs_fill_emphasis**: fill 중심이다. tint surface로 성격을 만들고 border는 아주 얇게 보조한다. (source=cards; confidence=0.94; provenance=inferred; direction=low-elevation tinted cards를 기본으로 하고, 넓은 내부 여백과 강한 section breathing room. 중간 반경으로 제품 UI 절제 유지.; evidence=surface=tinted, density=airy, corner=medium)
- **filter_nav_density**: filter/nav density는 balanced다. global nav와 local filter를 섞지 말고 계층별 간격 차이로 구조를 드러낸다. (source=navigation; confidence=0.94; provenance=inferred; direction=고정 sidebar 또는 split-pane navigation을 우선하고, 현재 위치와 scope를 항상 명시한다.; evidence=Split-pane workspace, layout=conversation-panel, density=airy)
- **chart_panel_framing**: 차트 패널은 soft tint frame과 restrained divider로 프레이밍한다. 헤더 메타데이터와 본문 visualization 사이의 breathing room을 충분히 둔다. (source=data_display; confidence=0.94; provenance=inferred; direction=정보 밀도를 유지하되 thin dividers와 restrained accent로 hierarchy를 만든다.; evidence=layout=dashboard-grid, density=airy, layout=conversation-panel, surface=tinted)

### 레퍼런스 근거

- **Carbon Design System**: AI chat is a conversational framework between a user and an AI that can aid in creating tasks, finding insights, tracking documents, and more. For ...
- **Primer**: The GitHub Design Infrastructure and Design Engineering teams build and maintain Primer — this includes our CSS framework, style guide documentatio...

### 구현 노트

- 기존에 같은 역할의 컴포넌트가 있으면 토큰 교체부터 시작
- variant prop으로 시각적 변형을 관리 (하드코딩 금지)
- 애니메이션은 상태 설명용으로만 사용, 장식 효과 금지
- 텍스트 위계가 핵심 — 컬러보다 weight/size로 구분

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

- [calm+editorial] hover: opacity 변화 (0.08-0.12), elevation 변화 없음 + 텍스트 underline 또는 color shift, 장식적 효과 없음
- [calm+editorial] motion: 150-200ms ease-out, bounce/spring 없음 + 콘텐츠 전환 위주, UI chrome 모션 최소화
- [calm+editorial] color: 중성 톤 위주, accent는 최소한으로 + 타이포그래피로 위계 형성, 컬러보다 weight/size 활용

### 레퍼런스 근거

- **Carbon Design System**: AI chat is a conversational framework between a user and an AI that can aid in creating tasks, finding insights, tracking documents, and more. For ...
- **Primer**: The GitHub Design Infrastructure and Design Engineering teams build and maintain Primer — this includes our CSS framework, style guide documentatio...

### 구현 노트

- 기존에 같은 역할의 컴포넌트가 있으면 토큰 교체부터 시작
- variant prop으로 시각적 변형을 관리 (하드코딩 금지)
- 애니메이션은 상태 설명용으로만 사용, 장식 효과 금지
- 텍스트 위계가 핵심 — 컬러보다 weight/size로 구분

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

- [calm+editorial] hover: opacity 변화 (0.08-0.12), elevation 변화 없음 + 텍스트 underline 또는 color shift, 장식적 효과 없음
- [calm+editorial] motion: 150-200ms ease-out, bounce/spring 없음 + 콘텐츠 전환 위주, UI chrome 모션 최소화
- [calm+editorial] color: 중성 톤 위주, accent는 최소한으로 + 타이포그래피로 위계 형성, 컬러보다 weight/size 활용

### 레퍼런스 근거

- **Carbon Design System**: AI chat is a conversational framework between a user and an AI that can aid in creating tasks, finding insights, tracking documents, and more. For ...
- **Primer**: The GitHub Design Infrastructure and Design Engineering teams build and maintain Primer — this includes our CSS framework, style guide documentatio...

### 구현 노트

- 기존에 같은 역할의 컴포넌트가 있으면 토큰 교체부터 시작
- variant prop으로 시각적 변형을 관리 (하드코딩 금지)
- 애니메이션은 상태 설명용으로만 사용, 장식 효과 금지
- 텍스트 위계가 핵심 — 컬러보다 weight/size로 구분

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

- [calm+editorial] hover: opacity 변화 (0.08-0.12), elevation 변화 없음 + 텍스트 underline 또는 color shift, 장식적 효과 없음
- [calm+editorial] motion: 150-200ms ease-out, bounce/spring 없음 + 콘텐츠 전환 위주, UI chrome 모션 최소화
- [calm+editorial] color: 중성 톤 위주, accent는 최소한으로 + 타이포그래피로 위계 형성, 컬러보다 weight/size 활용

### 레퍼런스 근거

- **Carbon Design System**: AI chat is a conversational framework between a user and an AI that can aid in creating tasks, finding insights, tracking documents, and more. For ...
- **Primer**: The GitHub Design Infrastructure and Design Engineering teams build and maintain Primer — this includes our CSS framework, style guide documentatio...

### 구현 노트

- 기존에 같은 역할의 컴포넌트가 있으면 토큰 교체부터 시작
- variant prop으로 시각적 변형을 관리 (하드코딩 금지)
- 애니메이션은 상태 설명용으로만 사용, 장식 효과 금지
- 텍스트 위계가 핵심 — 컬러보다 weight/size로 구분

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

- [calm+editorial] hover: opacity 변화 (0.08-0.12), elevation 변화 없음 + 텍스트 underline 또는 color shift, 장식적 효과 없음
- [calm+editorial] motion: 150-200ms ease-out, bounce/spring 없음 + 콘텐츠 전환 위주, UI chrome 모션 최소화
- [calm+editorial] color: 중성 톤 위주, accent는 최소한으로 + 타이포그래피로 위계 형성, 컬러보다 weight/size 활용

### 레퍼런스 근거

- **Carbon Design System**: AI chat is a conversational framework between a user and an AI that can aid in creating tasks, finding insights, tracking documents, and more. For ...
- **Primer**: The GitHub Design Infrastructure and Design Engineering teams build and maintain Primer — this includes our CSS framework, style guide documentatio...

### 구현 노트

- 기존에 같은 역할의 컴포넌트가 있으면 토큰 교체부터 시작
- variant prop으로 시각적 변형을 관리 (하드코딩 금지)
- 애니메이션은 상태 설명용으로만 사용, 장식 효과 금지
- 텍스트 위계가 핵심 — 컬러보다 weight/size로 구분

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

- [calm+editorial] hover: opacity 변화 (0.08-0.12), elevation 변화 없음 + 텍스트 underline 또는 color shift, 장식적 효과 없음
- [calm+editorial] density: comfortable 모드 기본, 여유로운 padding + 넉넉한 line-height와 margin, 읽기 편한 간격
- [calm+editorial] motion: 150-200ms ease-out, bounce/spring 없음 + 콘텐츠 전환 위주, UI chrome 모션 최소화

### Visual Adaptation Hints

- **filter_nav_density**: filter/nav density는 balanced다. global nav와 local filter를 섞지 말고 계층별 간격 차이로 구조를 드러낸다. (source=navigation; confidence=0.94; provenance=inferred; direction=고정 sidebar 또는 split-pane navigation을 우선하고, 현재 위치와 scope를 항상 명시한다.; evidence=Split-pane workspace, layout=conversation-panel, density=airy)

### 레퍼런스 근거

- **Carbon Design System**: Library menu navigation There are two kinds of symbols — library symbols and document symbols. Library symbols are available in any Sketch document...
- **Primer**: Octicon nav items navigation 12 px

### 구현 노트

- 기존에 같은 역할의 컴포넌트가 있으면 토큰 교체부터 시작
- variant prop으로 시각적 변형을 관리 (하드코딩 금지)
- active 상태는 URL/라우터와 자동 동기화
- 좁은 UI 텍스트는 Pretendard 기준 label line-height 1.4-1.5를 참고해 뭉침을 방지
- 애니메이션은 상태 설명용으로만 사용, 장식 효과 금지
- 텍스트 위계가 핵심 — 컬러보다 weight/size로 구분

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

- [calm+editorial] hover: opacity 변화 (0.08-0.12), elevation 변화 없음 + 텍스트 underline 또는 color shift, 장식적 효과 없음
- [calm+editorial] motion: 150-200ms ease-out, bounce/spring 없음 + 콘텐츠 전환 위주, UI chrome 모션 최소화
- [calm+editorial] color: 중성 톤 위주, accent는 최소한으로 + 타이포그래피로 위계 형성, 컬러보다 weight/size 활용

### Visual Adaptation Hints

- **card_elevation_tendency**: 카드는 낮은 elevation만 허용하고 색면 차이로 그룹을 구분한다. 내부 여백은 넉넉하게 두고 card breathing room을 확보한다. (source=cards; confidence=0.94; provenance=inferred; direction=low-elevation tinted cards를 기본으로 하고, 넓은 내부 여백과 강한 section breathing room. 중간 반경으로 제품 UI 절제 유지.; evidence=surface=tinted, density=airy, corner=medium)
- **border_vs_fill_emphasis**: fill 중심이다. tint surface로 성격을 만들고 border는 아주 얇게 보조한다. (source=cards; confidence=0.94; provenance=inferred; direction=low-elevation tinted cards를 기본으로 하고, 넓은 내부 여백과 강한 section breathing room. 중간 반경으로 제품 UI 절제 유지.; evidence=surface=tinted, density=airy, corner=medium)

### 레퍼런스 근거

- **Carbon Design System**: AI chat is a conversational framework between a user and an AI that can aid in creating tasks, finding insights, tracking documents, and more. For ...
- **Primer**: The GitHub Design Infrastructure and Design Engineering teams build and maintain Primer — this includes our CSS framework, style guide documentatio...

### 구현 노트

- 기존에 같은 역할의 컴포넌트가 있으면 토큰 교체부터 시작
- variant prop으로 시각적 변형을 관리 (하드코딩 금지)
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

- [calm+editorial] density: comfortable 모드 기본, 여유로운 padding + 넉넉한 line-height와 margin, 읽기 편한 간격
- [calm+editorial] color: 중성 톤 위주, accent는 최소한으로 + 타이포그래피로 위계 형성, 컬러보다 weight/size 활용

### Visual Adaptation Hints

- **card_elevation_tendency**: 카드는 낮은 elevation만 허용하고 색면 차이로 그룹을 구분한다. 내부 여백은 넉넉하게 두고 card breathing room을 확보한다. (source=cards; confidence=0.94; provenance=inferred; direction=low-elevation tinted cards를 기본으로 하고, 넓은 내부 여백과 강한 section breathing room. 중간 반경으로 제품 UI 절제 유지.; evidence=surface=tinted, density=airy, corner=medium)
- **border_vs_fill_emphasis**: fill 중심이다. tint surface로 성격을 만들고 border는 아주 얇게 보조한다. (source=cards; confidence=0.94; provenance=inferred; direction=low-elevation tinted cards를 기본으로 하고, 넓은 내부 여백과 강한 section breathing room. 중간 반경으로 제품 UI 절제 유지.; evidence=surface=tinted, density=airy, corner=medium)
- **chart_panel_framing**: 차트 패널은 soft tint frame과 restrained divider로 프레이밍한다. 헤더 메타데이터와 본문 visualization 사이의 breathing room을 충분히 둔다. (source=data_display; confidence=0.94; provenance=inferred; direction=정보 밀도를 유지하되 thin dividers와 restrained accent로 hierarchy를 만든다.; evidence=layout=dashboard-grid, density=airy, layout=conversation-panel, surface=tinted)

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

- [calm+editorial] feedback: subtle inline alert 선호, 과한 컬러 블록 지양 + 콘텐츠 맥락 안에서 인라인 표시, 토스트보다 인라인 선호
- [calm+editorial] motion: 150-200ms ease-out, bounce/spring 없음 + 콘텐츠 전환 위주, UI chrome 모션 최소화
- [calm+editorial] color: 중성 톤 위주, accent는 최소한으로 + 타이포그래피로 위계 형성, 컬러보다 weight/size 활용

### Visual Adaptation Hints

- **card_elevation_tendency**: 카드는 낮은 elevation만 허용하고 색면 차이로 그룹을 구분한다. 내부 여백은 넉넉하게 두고 card breathing room을 확보한다. (source=cards; confidence=0.94; provenance=inferred; direction=low-elevation tinted cards를 기본으로 하고, 넓은 내부 여백과 강한 section breathing room. 중간 반경으로 제품 UI 절제 유지.; evidence=surface=tinted, density=airy, corner=medium)
- **border_vs_fill_emphasis**: fill 중심이다. tint surface로 성격을 만들고 border는 아주 얇게 보조한다. (source=cards; confidence=0.94; provenance=inferred; direction=low-elevation tinted cards를 기본으로 하고, 넓은 내부 여백과 강한 section breathing room. 중간 반경으로 제품 UI 절제 유지.; evidence=surface=tinted, density=airy, corner=medium)
- **chart_panel_framing**: 차트 패널은 soft tint frame과 restrained divider로 프레이밍한다. 헤더 메타데이터와 본문 visualization 사이의 breathing room을 충분히 둔다. (source=data_display; confidence=0.94; provenance=inferred; direction=정보 밀도를 유지하되 thin dividers와 restrained accent로 hierarchy를 만든다.; evidence=layout=dashboard-grid, density=airy, layout=conversation-panel, surface=tinted)

### 레퍼런스 근거

- **Carbon Design System**: We welcome all feedback, designs, or ideas in order to produce the best possible experience for our users. If you're interested in contributing, ch...
- **Primer**: Messaging components are used to provide important and relevant information to the user, including feedback, contextual information, product update...

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

- [calm+editorial] hover: opacity 변화 (0.08-0.12), elevation 변화 없음 + 텍스트 underline 또는 color shift, 장식적 효과 없음
- [calm+editorial] density: comfortable 모드 기본, 여유로운 padding + 넉넉한 line-height와 margin, 읽기 편한 간격
- [calm+editorial] feedback: subtle inline alert 선호, 과한 컬러 블록 지양 + 콘텐츠 맥락 안에서 인라인 표시, 토스트보다 인라인 선호

### Visual Adaptation Hints

- **filter_nav_density**: filter/nav density는 balanced다. global nav와 local filter를 섞지 말고 계층별 간격 차이로 구조를 드러낸다. (source=navigation; confidence=0.94; provenance=inferred; direction=고정 sidebar 또는 split-pane navigation을 우선하고, 현재 위치와 scope를 항상 명시한다.; evidence=Split-pane workspace, layout=conversation-panel, density=airy)

### 레퍼런스 근거

- **Carbon Design System**: Number input Text input
- **Primer**: I worked in data visualization and map-making for most of my career, and solving design problems with data is my jam. To me there's something uniqu...

### 구현 노트

- 기존에 같은 역할의 컴포넌트가 있으면 토큰 교체부터 시작
- variant prop으로 시각적 변형을 관리 (하드코딩 금지)
- error 상태에서 helper text → error message로 자동 전환
- label은 항상 visible (placeholder만으로 대체 금지)
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

- [calm+editorial] hover: opacity 변화 (0.08-0.12), elevation 변화 없음 + 텍스트 underline 또는 color shift, 장식적 효과 없음
- [calm+editorial] density: comfortable 모드 기본, 여유로운 padding + 넉넉한 line-height와 margin, 읽기 편한 간격
- [calm+editorial] motion: 150-200ms ease-out, bounce/spring 없음 + 콘텐츠 전환 위주, UI chrome 모션 최소화

### Visual Adaptation Hints

- **filter_nav_density**: filter/nav density는 balanced다. global nav와 local filter를 섞지 말고 계층별 간격 차이로 구조를 드러낸다. (source=navigation; confidence=0.94; provenance=inferred; direction=고정 sidebar 또는 split-pane navigation을 우선하고, 현재 위치와 scope를 항상 명시한다.; evidence=Split-pane workspace, layout=conversation-panel, density=airy)

### 레퍼런스 근거

- **Carbon Design System**: Library menu navigation There are two kinds of symbols — library symbols and document symbols. Library symbols are available in any Sketch document...
- **Primer**: Octicon nav items navigation 12 px

### 구현 노트

- 기존에 같은 역할의 컴포넌트가 있으면 토큰 교체부터 시작
- variant prop으로 시각적 변형을 관리 (하드코딩 금지)
- active 상태는 URL/라우터와 자동 동기화
- 좁은 UI 텍스트는 Pretendard 기준 label line-height 1.4-1.5를 참고해 뭉침을 방지
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

- [calm+editorial] hover: opacity 변화 (0.08-0.12), elevation 변화 없음 + 텍스트 underline 또는 color shift, 장식적 효과 없음
- [calm+editorial] density: comfortable 모드 기본, 여유로운 padding + 넉넉한 line-height와 margin, 읽기 편한 간격
- [calm+editorial] motion: 150-200ms ease-out, bounce/spring 없음 + 콘텐츠 전환 위주, UI chrome 모션 최소화

### Visual Adaptation Hints

- **filter_nav_density**: filter/nav density는 balanced다. global nav와 local filter를 섞지 말고 계층별 간격 차이로 구조를 드러낸다. (source=navigation; confidence=0.94; provenance=inferred; direction=고정 sidebar 또는 split-pane navigation을 우선하고, 현재 위치와 scope를 항상 명시한다.; evidence=Split-pane workspace, layout=conversation-panel, density=airy)

### 레퍼런스 근거

- **Carbon Design System**: Total panel width (“sidebar nav”) + Left outside margin + Right outside margin = Total margins Artboard width - Total margins = Total width
- **Primer**: Octicon nav items navigation 12 px

### 구현 노트

- 기존에 같은 역할의 컴포넌트가 있으면 토큰 교체부터 시작
- variant prop으로 시각적 변형을 관리 (하드코딩 금지)
- active 상태는 URL/라우터와 자동 동기화
- 좁은 UI 텍스트는 Pretendard 기준 label line-height 1.4-1.5를 참고해 뭉침을 방지
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

- [calm+editorial] hover: opacity 변화 (0.08-0.12), elevation 변화 없음 + 텍스트 underline 또는 color shift, 장식적 효과 없음
- [calm+editorial] density: comfortable 모드 기본, 여유로운 padding + 넉넉한 line-height와 margin, 읽기 편한 간격
- [calm+editorial] motion: 150-200ms ease-out, bounce/spring 없음 + 콘텐츠 전환 위주, UI chrome 모션 최소화

### Visual Adaptation Hints

- **filter_nav_density**: filter/nav density는 balanced다. global nav와 local filter를 섞지 말고 계층별 간격 차이로 구조를 드러낸다. (source=navigation; confidence=0.94; provenance=inferred; direction=고정 sidebar 또는 split-pane navigation을 우선하고, 현재 위치와 scope를 항상 명시한다.; evidence=Split-pane workspace, layout=conversation-panel, density=airy)

### 레퍼런스 근거

- **Carbon Design System**: Library menu navigation There are two kinds of symbols — library symbols and document symbols. Library symbols are available in any Sketch document...
- **Primer**: Octicon nav items navigation 12 px

### 구현 노트

- 기존에 같은 역할의 컴포넌트가 있으면 토큰 교체부터 시작
- variant prop으로 시각적 변형을 관리 (하드코딩 금지)
- active 상태는 URL/라우터와 자동 동기화
- 좁은 UI 텍스트는 Pretendard 기준 label line-height 1.4-1.5를 참고해 뭉침을 방지
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

- [calm+editorial] hover: opacity 변화 (0.08-0.12), elevation 변화 없음 + 텍스트 underline 또는 color shift, 장식적 효과 없음
- [calm+editorial] density: comfortable 모드 기본, 여유로운 padding + 넉넉한 line-height와 margin, 읽기 편한 간격
- [calm+editorial] motion: 150-200ms ease-out, bounce/spring 없음 + 콘텐츠 전환 위주, UI chrome 모션 최소화

### Visual Adaptation Hints

- **filter_nav_density**: filter/nav density는 balanced다. global nav와 local filter를 섞지 말고 계층별 간격 차이로 구조를 드러낸다. (source=navigation; confidence=0.94; provenance=inferred; direction=고정 sidebar 또는 split-pane navigation을 우선하고, 현재 위치와 scope를 항상 명시한다.; evidence=Split-pane workspace, layout=conversation-panel, density=airy)

### 레퍼런스 근거

- **Carbon Design System**: Library menu navigation There are two kinds of symbols — library symbols and document symbols. Library symbols are available in any Sketch document...
- **Primer**: Octicon nav items navigation 12 px

### 구현 노트

- 기존에 같은 역할의 컴포넌트가 있으면 토큰 교체부터 시작
- variant prop으로 시각적 변형을 관리 (하드코딩 금지)
- active 상태는 URL/라우터와 자동 동기화
- 좁은 UI 텍스트는 Pretendard 기준 label line-height 1.4-1.5를 참고해 뭉침을 방지
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

- [calm+editorial] hover: opacity 변화 (0.08-0.12), elevation 변화 없음 + 텍스트 underline 또는 color shift, 장식적 효과 없음
- [calm+editorial] density: comfortable 모드 기본, 여유로운 padding + 넉넉한 line-height와 margin, 읽기 편한 간격
- [calm+editorial] motion: 150-200ms ease-out, bounce/spring 없음 + 콘텐츠 전환 위주, UI chrome 모션 최소화

### Visual Adaptation Hints

- **filter_nav_density**: filter/nav density는 balanced다. global nav와 local filter를 섞지 말고 계층별 간격 차이로 구조를 드러낸다. (source=navigation; confidence=0.94; provenance=inferred; direction=고정 sidebar 또는 split-pane navigation을 우선하고, 현재 위치와 scope를 항상 명시한다.; evidence=Split-pane workspace, layout=conversation-panel, density=airy)

### 레퍼런스 근거

- **Carbon Design System**: Library menu navigation There are two kinds of symbols — library symbols and document symbols. Library symbols are available in any Sketch document...
- **Primer**: Octicon nav items navigation 12 px

### 구현 노트

- 기존에 같은 역할의 컴포넌트가 있으면 토큰 교체부터 시작
- variant prop으로 시각적 변형을 관리 (하드코딩 금지)
- active 상태는 URL/라우터와 자동 동기화
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

- [calm+editorial] hover: opacity 변화 (0.08-0.12), elevation 변화 없음 + 텍스트 underline 또는 color shift, 장식적 효과 없음
- [calm+editorial] density: comfortable 모드 기본, 여유로운 padding + 넉넉한 line-height와 margin, 읽기 편한 간격
- [calm+editorial] feedback: subtle inline alert 선호, 과한 컬러 블록 지양 + 콘텐츠 맥락 안에서 인라인 표시, 토스트보다 인라인 선호

### 레퍼런스 근거

- **Carbon Design System**: Number input Text input
- **Primer**: I worked in data visualization and map-making for most of my career, and solving design problems with data is my jam. To me there's something uniqu...

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

- [calm+editorial] hover: opacity 변화 (0.08-0.12), elevation 변화 없음 + 텍스트 underline 또는 color shift, 장식적 효과 없음
- [calm+editorial] density: comfortable 모드 기본, 여유로운 padding + 넉넉한 line-height와 margin, 읽기 편한 간격
- [calm+editorial] feedback: subtle inline alert 선호, 과한 컬러 블록 지양 + 콘텐츠 맥락 안에서 인라인 표시, 토스트보다 인라인 선호

### 레퍼런스 근거

- **Carbon Design System**: Number input Text input
- **Primer**: I worked in data visualization and map-making for most of my career, and solving design problems with data is my jam. To me there's something uniqu...

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

- [calm+editorial] hover: opacity 변화 (0.08-0.12), elevation 변화 없음 + 텍스트 underline 또는 color shift, 장식적 효과 없음
- [calm+editorial] density: comfortable 모드 기본, 여유로운 padding + 넉넉한 line-height와 margin, 읽기 편한 간격
- [calm+editorial] feedback: subtle inline alert 선호, 과한 컬러 블록 지양 + 콘텐츠 맥락 안에서 인라인 표시, 토스트보다 인라인 선호

### 레퍼런스 근거

- **Carbon Design System**: Select Data table
- **Primer**: Primer color design tokens are made available within data-attribute selectors on the body tag or other high level dom element. There are three dist...

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

- [calm+editorial] hover: opacity 변화 (0.08-0.12), elevation 변화 없음 + 텍스트 underline 또는 color shift, 장식적 효과 없음
- [calm+editorial] density: comfortable 모드 기본, 여유로운 padding + 넉넉한 line-height와 margin, 읽기 편한 간격
- [calm+editorial] feedback: subtle inline alert 선호, 과한 컬러 블록 지양 + 콘텐츠 맥락 안에서 인라인 표시, 토스트보다 인라인 선호

### 레퍼런스 근거

- **Carbon Design System**: Checkbox Form
- **Primer**: I worked in data visualization and map-making for most of my career, and solving design problems with data is my jam. To me there's something uniqu...

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

- [calm+editorial] hover: opacity 변화 (0.08-0.12), elevation 변화 없음 + 텍스트 underline 또는 color shift, 장식적 효과 없음
- [calm+editorial] density: comfortable 모드 기본, 여유로운 padding + 넉넉한 line-height와 margin, 읽기 편한 간격
- [calm+editorial] feedback: subtle inline alert 선호, 과한 컬러 블록 지양 + 콘텐츠 맥락 안에서 인라인 표시, 토스트보다 인라인 선호

### 레퍼런스 근거

- **Carbon Design System**: Number input Text input
- **Primer**: I worked in data visualization and map-making for most of my career, and solving design problems with data is my jam. To me there's something uniqu...

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

- [calm+editorial] hover: opacity 변화 (0.08-0.12), elevation 변화 없음 + 텍스트 underline 또는 color shift, 장식적 효과 없음
- [calm+editorial] density: comfortable 모드 기본, 여유로운 padding + 넉넉한 line-height와 margin, 읽기 편한 간격
- [calm+editorial] feedback: subtle inline alert 선호, 과한 컬러 블록 지양 + 콘텐츠 맥락 안에서 인라인 표시, 토스트보다 인라인 선호

### 레퍼런스 근거

- **Carbon Design System**: Number input Text input
- **Primer**: I worked in data visualization and map-making for most of my career, and solving design problems with data is my jam. To me there's something uniqu...

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

- [calm+editorial] hover: opacity 변화 (0.08-0.12), elevation 변화 없음 + 텍스트 underline 또는 color shift, 장식적 효과 없음
- [calm+editorial] motion: 150-200ms ease-out, bounce/spring 없음 + 콘텐츠 전환 위주, UI chrome 모션 최소화
- [calm+editorial] color: 중성 톤 위주, accent는 최소한으로 + 타이포그래피로 위계 형성, 컬러보다 weight/size 활용

### Visual Adaptation Hints

- **cta_prominence**: CTA prominence는 medium이다. primary action은 분명하게 보이되 화면 전체를 지배하지 않게 유지한다. (source=cards; confidence=0.94; provenance=inferred; direction=low-elevation tinted cards를 기본으로 하고, 넓은 내부 여백과 강한 section breathing room. 중간 반경으로 제품 UI 절제 유지.; evidence=surface=tinted, density=airy, corner=medium, layout=conversation-panel)

### 레퍼런스 근거

- **Carbon Design System**: These components can toggle between the AI variant and the default variant depending on the user’s interaction. If the user manually overrides the ...
- **Primer**: I get so much joy from writing HTML and CSS, and design systems are one level up - systematically making UIs accessible and consistent. I love conc...

### 구현 노트

- 기존에 같은 역할의 컴포넌트가 있으면 토큰 교체부터 시작
- variant prop으로 시각적 변형을 관리 (하드코딩 금지)
- size prop: sm / md / lg (터치 영역은 항상 최소 44px 보장)
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

- [calm+editorial] hover: opacity 변화 (0.08-0.12), elevation 변화 없음 + 텍스트 underline 또는 color shift, 장식적 효과 없음
- [calm+editorial] density: comfortable 모드 기본, 여유로운 padding + 넉넉한 line-height와 margin, 읽기 편한 간격
- [calm+editorial] feedback: subtle inline alert 선호, 과한 컬러 블록 지양 + 콘텐츠 맥락 안에서 인라인 표시, 토스트보다 인라인 선호

### 레퍼런스 근거

- **Carbon Design System**: Date picker Number input
- **Primer**: I worked in data visualization and map-making for most of my career, and solving design problems with data is my jam. To me there's something uniqu...

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

- [calm+editorial] density: comfortable 모드 기본, 여유로운 padding + 넉넉한 line-height와 margin, 읽기 편한 간격
- [calm+editorial] color: 중성 톤 위주, accent는 최소한으로 + 타이포그래피로 위계 형성, 컬러보다 weight/size 활용

### Visual Adaptation Hints

- **card_elevation_tendency**: 카드는 낮은 elevation만 허용하고 색면 차이로 그룹을 구분한다. 내부 여백은 넉넉하게 두고 card breathing room을 확보한다. (source=cards; confidence=0.94; provenance=inferred; direction=low-elevation tinted cards를 기본으로 하고, 넓은 내부 여백과 강한 section breathing room. 중간 반경으로 제품 UI 절제 유지.; evidence=surface=tinted, density=airy, corner=medium)
- **border_vs_fill_emphasis**: fill 중심이다. tint surface로 성격을 만들고 border는 아주 얇게 보조한다. (source=cards; confidence=0.94; provenance=inferred; direction=low-elevation tinted cards를 기본으로 하고, 넓은 내부 여백과 강한 section breathing room. 중간 반경으로 제품 UI 절제 유지.; evidence=surface=tinted, density=airy, corner=medium)
- **chart_panel_framing**: 차트 패널은 soft tint frame과 restrained divider로 프레이밍한다. 헤더 메타데이터와 본문 visualization 사이의 breathing room을 충분히 둔다. (source=data_display; confidence=0.94; provenance=inferred; direction=정보 밀도를 유지하되 thin dividers와 restrained accent로 hierarchy를 만든다.; evidence=layout=dashboard-grid, density=airy, layout=conversation-panel, surface=tinted)

### 구현 노트

- 기존에 같은 역할의 컴포넌트가 있으면 토큰 교체부터 시작
- variant prop으로 시각적 변형을 관리 (하드코딩 금지)
- 빈 상태(empty-state)와 에러 상태를 반드시 처리
- 좁은 UI 텍스트는 Pretendard 기준 label line-height 1.4-1.5를 참고해 뭉침을 방지
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

- [calm+editorial] hover: opacity 변화 (0.08-0.12), elevation 변화 없음 + 텍스트 underline 또는 color shift, 장식적 효과 없음
- [calm+editorial] density: comfortable 모드 기본, 여유로운 padding + 넉넉한 line-height와 margin, 읽기 편한 간격
- [calm+editorial] feedback: subtle inline alert 선호, 과한 컬러 블록 지양 + 콘텐츠 맥락 안에서 인라인 표시, 토스트보다 인라인 선호

### 레퍼런스 근거

- **Carbon Design System**: Number input Text input
- **Primer**: I worked in data visualization and map-making for most of my career, and solving design problems with data is my jam. To me there's something uniqu...

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

- [calm+editorial] hover: opacity 변화 (0.08-0.12), elevation 변화 없음 + 텍스트 underline 또는 color shift, 장식적 효과 없음
- [calm+editorial] density: comfortable 모드 기본, 여유로운 padding + 넉넉한 line-height와 margin, 읽기 편한 간격
- [calm+editorial] feedback: subtle inline alert 선호, 과한 컬러 블록 지양 + 콘텐츠 맥락 안에서 인라인 표시, 토스트보다 인라인 선호

### 레퍼런스 근거

- **Carbon Design System**: Number input Text input
- **Primer**: I worked in data visualization and map-making for most of my career, and solving design problems with data is my jam. To me there's something uniqu...

### 구현 노트

- 기존에 같은 역할의 컴포넌트가 있으면 토큰 교체부터 시작
- variant prop으로 시각적 변형을 관리 (하드코딩 금지)
- error 상태에서 helper text → error message로 자동 전환
- label은 항상 visible (placeholder만으로 대체 금지)
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

- [calm+editorial] density: comfortable 모드 기본, 여유로운 padding + 넉넉한 line-height와 margin, 읽기 편한 간격
- [calm+editorial] color: 중성 톤 위주, accent는 최소한으로 + 타이포그래피로 위계 형성, 컬러보다 weight/size 활용

### Visual Adaptation Hints

- **card_elevation_tendency**: 카드는 낮은 elevation만 허용하고 색면 차이로 그룹을 구분한다. 내부 여백은 넉넉하게 두고 card breathing room을 확보한다. (source=cards; confidence=0.94; provenance=inferred; direction=low-elevation tinted cards를 기본으로 하고, 넓은 내부 여백과 강한 section breathing room. 중간 반경으로 제품 UI 절제 유지.; evidence=surface=tinted, density=airy, corner=medium)
- **border_vs_fill_emphasis**: fill 중심이다. tint surface로 성격을 만들고 border는 아주 얇게 보조한다. (source=cards; confidence=0.94; provenance=inferred; direction=low-elevation tinted cards를 기본으로 하고, 넓은 내부 여백과 강한 section breathing room. 중간 반경으로 제품 UI 절제 유지.; evidence=surface=tinted, density=airy, corner=medium)
- **chart_panel_framing**: 차트 패널은 soft tint frame과 restrained divider로 프레이밍한다. 헤더 메타데이터와 본문 visualization 사이의 breathing room을 충분히 둔다. (source=data_display; confidence=0.94; provenance=inferred; direction=정보 밀도를 유지하되 thin dividers와 restrained accent로 hierarchy를 만든다.; evidence=layout=dashboard-grid, density=airy, layout=conversation-panel, surface=tinted)

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

- [calm+editorial] hover: opacity 변화 (0.08-0.12), elevation 변화 없음 + 텍스트 underline 또는 color shift, 장식적 효과 없음
- [calm+editorial] motion: 150-200ms ease-out, bounce/spring 없음 + 콘텐츠 전환 위주, UI chrome 모션 최소화
- [calm+editorial] color: 중성 톤 위주, accent는 최소한으로 + 타이포그래피로 위계 형성, 컬러보다 weight/size 활용

### Visual Adaptation Hints

- **cta_prominence**: CTA prominence는 medium이다. primary action은 분명하게 보이되 화면 전체를 지배하지 않게 유지한다. (source=cards; confidence=0.94; provenance=inferred; direction=low-elevation tinted cards를 기본으로 하고, 넓은 내부 여백과 강한 section breathing room. 중간 반경으로 제품 UI 절제 유지.; evidence=surface=tinted, density=airy, corner=medium, layout=conversation-panel)

### 레퍼런스 근거

- **Carbon Design System**: These components can toggle between the AI variant and the default variant depending on the user’s interaction. If the user manually overrides the ...
- **Primer**: I get so much joy from writing HTML and CSS, and design systems are one level up - systematically making UIs accessible and consistent. I love conc...

### 구현 노트

- 기존에 같은 역할의 컴포넌트가 있으면 토큰 교체부터 시작
- variant prop으로 시각적 변형을 관리 (하드코딩 금지)
- size prop: sm / md / lg (터치 영역은 항상 최소 44px 보장)
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

- [calm+editorial] hover: opacity 변화 (0.08-0.12), elevation 변화 없음 + 텍스트 underline 또는 color shift, 장식적 효과 없음
- [calm+editorial] density: comfortable 모드 기본, 여유로운 padding + 넉넉한 line-height와 margin, 읽기 편한 간격
- [calm+editorial] feedback: subtle inline alert 선호, 과한 컬러 블록 지양 + 콘텐츠 맥락 안에서 인라인 표시, 토스트보다 인라인 선호

### 레퍼런스 근거

- **Carbon Design System**: Number input Text input
- **Primer**: I worked in data visualization and map-making for most of my career, and solving design problems with data is my jam. To me there's something uniqu...

### 구현 노트

- 기존에 같은 역할의 컴포넌트가 있으면 토큰 교체부터 시작
- variant prop으로 시각적 변형을 관리 (하드코딩 금지)
- error 상태에서 helper text → error message로 자동 전환
- label은 항상 visible (placeholder만으로 대체 금지)
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

- [calm+editorial] density: comfortable 모드 기본, 여유로운 padding + 넉넉한 line-height와 margin, 읽기 편한 간격
- [calm+editorial] color: 중성 톤 위주, accent는 최소한으로 + 타이포그래피로 위계 형성, 컬러보다 weight/size 활용

### Visual Adaptation Hints

- **card_elevation_tendency**: 카드는 낮은 elevation만 허용하고 색면 차이로 그룹을 구분한다. 내부 여백은 넉넉하게 두고 card breathing room을 확보한다. (source=cards; confidence=0.94; provenance=inferred; direction=low-elevation tinted cards를 기본으로 하고, 넓은 내부 여백과 강한 section breathing room. 중간 반경으로 제품 UI 절제 유지.; evidence=surface=tinted, density=airy, corner=medium)
- **border_vs_fill_emphasis**: fill 중심이다. tint surface로 성격을 만들고 border는 아주 얇게 보조한다. (source=cards; confidence=0.94; provenance=inferred; direction=low-elevation tinted cards를 기본으로 하고, 넓은 내부 여백과 강한 section breathing room. 중간 반경으로 제품 UI 절제 유지.; evidence=surface=tinted, density=airy, corner=medium)
- **chart_panel_framing**: 차트 패널은 soft tint frame과 restrained divider로 프레이밍한다. 헤더 메타데이터와 본문 visualization 사이의 breathing room을 충분히 둔다. (source=data_display; confidence=0.94; provenance=inferred; direction=정보 밀도를 유지하되 thin dividers와 restrained accent로 hierarchy를 만든다.; evidence=layout=dashboard-grid, density=airy, layout=conversation-panel, surface=tinted)

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

- [calm+editorial] motion: 150-200ms ease-out, bounce/spring 없음 + 콘텐츠 전환 위주, UI chrome 모션 최소화
- [calm+editorial] density: comfortable 모드 기본, 여유로운 padding + 넉넉한 line-height와 margin, 읽기 편한 간격

### Visual Adaptation Hints

- **card_elevation_tendency**: 카드는 낮은 elevation만 허용하고 색면 차이로 그룹을 구분한다. 내부 여백은 넉넉하게 두고 card breathing room을 확보한다. (source=cards; confidence=0.94; provenance=inferred; direction=low-elevation tinted cards를 기본으로 하고, 넓은 내부 여백과 강한 section breathing room. 중간 반경으로 제품 UI 절제 유지.; evidence=surface=tinted, density=airy, corner=medium)
- **border_vs_fill_emphasis**: fill 중심이다. tint surface로 성격을 만들고 border는 아주 얇게 보조한다. (source=cards; confidence=0.94; provenance=inferred; direction=low-elevation tinted cards를 기본으로 하고, 넓은 내부 여백과 강한 section breathing room. 중간 반경으로 제품 UI 절제 유지.; evidence=surface=tinted, density=airy, corner=medium)
- **chart_panel_framing**: 차트 패널은 soft tint frame과 restrained divider로 프레이밍한다. 헤더 메타데이터와 본문 visualization 사이의 breathing room을 충분히 둔다. (source=data_display; confidence=0.94; provenance=inferred; direction=정보 밀도를 유지하되 thin dividers와 restrained accent로 hierarchy를 만든다.; evidence=layout=dashboard-grid, density=airy, layout=conversation-panel, surface=tinted)

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

- [calm+editorial] density: comfortable 모드 기본, 여유로운 padding + 넉넉한 line-height와 margin, 읽기 편한 간격
- [calm+editorial] color: 중성 톤 위주, accent는 최소한으로 + 타이포그래피로 위계 형성, 컬러보다 weight/size 활용

### Visual Adaptation Hints

- **card_elevation_tendency**: 카드는 낮은 elevation만 허용하고 색면 차이로 그룹을 구분한다. 내부 여백은 넉넉하게 두고 card breathing room을 확보한다. (source=cards; confidence=0.94; provenance=inferred; direction=low-elevation tinted cards를 기본으로 하고, 넓은 내부 여백과 강한 section breathing room. 중간 반경으로 제품 UI 절제 유지.; evidence=surface=tinted, density=airy, corner=medium)
- **border_vs_fill_emphasis**: fill 중심이다. tint surface로 성격을 만들고 border는 아주 얇게 보조한다. (source=cards; confidence=0.94; provenance=inferred; direction=low-elevation tinted cards를 기본으로 하고, 넓은 내부 여백과 강한 section breathing room. 중간 반경으로 제품 UI 절제 유지.; evidence=surface=tinted, density=airy, corner=medium)
- **chart_panel_framing**: 차트 패널은 soft tint frame과 restrained divider로 프레이밍한다. 헤더 메타데이터와 본문 visualization 사이의 breathing room을 충분히 둔다. (source=data_display; confidence=0.94; provenance=inferred; direction=정보 밀도를 유지하되 thin dividers와 restrained accent로 hierarchy를 만든다.; evidence=layout=dashboard-grid, density=airy, layout=conversation-panel, surface=tinted)

### 구현 노트

- 기존에 같은 역할의 컴포넌트가 있으면 토큰 교체부터 시작
- variant prop으로 시각적 변형을 관리 (하드코딩 금지)
- 빈 상태(empty-state)와 에러 상태를 반드시 처리
- 좁은 UI 텍스트는 Pretendard 기준 label line-height 1.4-1.5를 참고해 뭉침을 방지
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

- [calm+editorial] density: comfortable 모드 기본, 여유로운 padding + 넉넉한 line-height와 margin, 읽기 편한 간격
- [calm+editorial] color: 중성 톤 위주, accent는 최소한으로 + 타이포그래피로 위계 형성, 컬러보다 weight/size 활용

### Visual Adaptation Hints

- **card_elevation_tendency**: 카드는 낮은 elevation만 허용하고 색면 차이로 그룹을 구분한다. 내부 여백은 넉넉하게 두고 card breathing room을 확보한다. (source=cards; confidence=0.94; provenance=inferred; direction=low-elevation tinted cards를 기본으로 하고, 넓은 내부 여백과 강한 section breathing room. 중간 반경으로 제품 UI 절제 유지.; evidence=surface=tinted, density=airy, corner=medium)
- **border_vs_fill_emphasis**: fill 중심이다. tint surface로 성격을 만들고 border는 아주 얇게 보조한다. (source=cards; confidence=0.94; provenance=inferred; direction=low-elevation tinted cards를 기본으로 하고, 넓은 내부 여백과 강한 section breathing room. 중간 반경으로 제품 UI 절제 유지.; evidence=surface=tinted, density=airy, corner=medium)
- **filter_nav_density**: filter/nav density는 balanced다. global nav와 local filter를 섞지 말고 계층별 간격 차이로 구조를 드러낸다. (source=navigation; confidence=0.94; provenance=inferred; direction=고정 sidebar 또는 split-pane navigation을 우선하고, 현재 위치와 scope를 항상 명시한다.; evidence=Split-pane workspace, layout=conversation-panel, density=airy)
- **chart_panel_framing**: 차트 패널은 soft tint frame과 restrained divider로 프레이밍한다. 헤더 메타데이터와 본문 visualization 사이의 breathing room을 충분히 둔다. (source=data_display; confidence=0.94; provenance=inferred; direction=정보 밀도를 유지하되 thin dividers와 restrained accent로 hierarchy를 만든다.; evidence=layout=dashboard-grid, density=airy, layout=conversation-panel, surface=tinted)

### 레퍼런스 근거

- **Carbon Design System**: Data table Modal
- **Primer**: DataTable DataTable is a 2-dimensional data structure where each row is an item, and each column is a data point about the item.

### 구현 노트

- 기존에 같은 역할의 컴포넌트가 있으면 토큰 교체부터 시작
- variant prop으로 시각적 변형을 관리 (하드코딩 금지)
- 빈 상태(empty-state)와 에러 상태를 반드시 처리
- 좁은 UI 텍스트는 Pretendard 기준 label line-height 1.4-1.5를 참고해 뭉침을 방지
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

- [calm+editorial] density: comfortable 모드 기본, 여유로운 padding + 넉넉한 line-height와 margin, 읽기 편한 간격
- [calm+editorial] color: 중성 톤 위주, accent는 최소한으로 + 타이포그래피로 위계 형성, 컬러보다 weight/size 활용

### Visual Adaptation Hints

- **card_elevation_tendency**: 카드는 낮은 elevation만 허용하고 색면 차이로 그룹을 구분한다. 내부 여백은 넉넉하게 두고 card breathing room을 확보한다. (source=cards; confidence=0.94; provenance=inferred; direction=low-elevation tinted cards를 기본으로 하고, 넓은 내부 여백과 강한 section breathing room. 중간 반경으로 제품 UI 절제 유지.; evidence=surface=tinted, density=airy, corner=medium)
- **border_vs_fill_emphasis**: fill 중심이다. tint surface로 성격을 만들고 border는 아주 얇게 보조한다. (source=cards; confidence=0.94; provenance=inferred; direction=low-elevation tinted cards를 기본으로 하고, 넓은 내부 여백과 강한 section breathing room. 중간 반경으로 제품 UI 절제 유지.; evidence=surface=tinted, density=airy, corner=medium)
- **chart_panel_framing**: 차트 패널은 soft tint frame과 restrained divider로 프레이밍한다. 헤더 메타데이터와 본문 visualization 사이의 breathing room을 충분히 둔다. (source=data_display; confidence=0.94; provenance=inferred; direction=정보 밀도를 유지하되 thin dividers와 restrained accent로 hierarchy를 만든다.; evidence=layout=dashboard-grid, density=airy, layout=conversation-panel, surface=tinted)

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

- [calm+editorial] density: comfortable 모드 기본, 여유로운 padding + 넉넉한 line-height와 margin, 읽기 편한 간격
- [calm+editorial] color: 중성 톤 위주, accent는 최소한으로 + 타이포그래피로 위계 형성, 컬러보다 weight/size 활용

### Visual Adaptation Hints

- **card_elevation_tendency**: 카드는 낮은 elevation만 허용하고 색면 차이로 그룹을 구분한다. 내부 여백은 넉넉하게 두고 card breathing room을 확보한다. (source=cards; confidence=0.94; provenance=inferred; direction=low-elevation tinted cards를 기본으로 하고, 넓은 내부 여백과 강한 section breathing room. 중간 반경으로 제품 UI 절제 유지.; evidence=surface=tinted, density=airy, corner=medium)
- **border_vs_fill_emphasis**: fill 중심이다. tint surface로 성격을 만들고 border는 아주 얇게 보조한다. (source=cards; confidence=0.94; provenance=inferred; direction=low-elevation tinted cards를 기본으로 하고, 넓은 내부 여백과 강한 section breathing room. 중간 반경으로 제품 UI 절제 유지.; evidence=surface=tinted, density=airy, corner=medium)
- **chart_panel_framing**: 차트 패널은 soft tint frame과 restrained divider로 프레이밍한다. 헤더 메타데이터와 본문 visualization 사이의 breathing room을 충분히 둔다. (source=data_display; confidence=0.94; provenance=inferred; direction=정보 밀도를 유지하되 thin dividers와 restrained accent로 hierarchy를 만든다.; evidence=layout=dashboard-grid, density=airy, layout=conversation-panel, surface=tinted)

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

- [calm+editorial] hover: opacity 변화 (0.08-0.12), elevation 변화 없음 + 텍스트 underline 또는 color shift, 장식적 효과 없음
- [calm+editorial] density: comfortable 모드 기본, 여유로운 padding + 넉넉한 line-height와 margin, 읽기 편한 간격
- [calm+editorial] motion: 150-200ms ease-out, bounce/spring 없음 + 콘텐츠 전환 위주, UI chrome 모션 최소화

### Visual Adaptation Hints

- **filter_nav_density**: filter/nav density는 balanced다. global nav와 local filter를 섞지 말고 계층별 간격 차이로 구조를 드러낸다. (source=navigation; confidence=0.94; provenance=inferred; direction=고정 sidebar 또는 split-pane navigation을 우선하고, 현재 위치와 scope를 항상 명시한다.; evidence=Split-pane workspace, layout=conversation-panel, density=airy)

### 레퍼런스 근거

- **Carbon Design System**: Library menu navigation There are two kinds of symbols — library symbols and document symbols. Library symbols are available in any Sketch document...
- **Primer**: Octicon nav items navigation 12 px

### 구현 노트

- 기존에 같은 역할의 컴포넌트가 있으면 토큰 교체부터 시작
- variant prop으로 시각적 변형을 관리 (하드코딩 금지)
- active 상태는 URL/라우터와 자동 동기화
- 좁은 UI 텍스트는 Pretendard 기준 label line-height 1.4-1.5를 참고해 뭉침을 방지
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

- [calm+editorial] hover: opacity 변화 (0.08-0.12), elevation 변화 없음 + 텍스트 underline 또는 color shift, 장식적 효과 없음
- [calm+editorial] density: comfortable 모드 기본, 여유로운 padding + 넉넉한 line-height와 margin, 읽기 편한 간격
- [calm+editorial] feedback: subtle inline alert 선호, 과한 컬러 블록 지양 + 콘텐츠 맥락 안에서 인라인 표시, 토스트보다 인라인 선호

### Visual Adaptation Hints

- **filter_nav_density**: filter/nav density는 balanced다. global nav와 local filter를 섞지 말고 계층별 간격 차이로 구조를 드러낸다. (source=navigation; confidence=0.94; provenance=inferred; direction=고정 sidebar 또는 split-pane navigation을 우선하고, 현재 위치와 scope를 항상 명시한다.; evidence=Split-pane workspace, layout=conversation-panel, density=airy)

### 레퍼런스 근거

- **Carbon Design System**: Number input Text input
- **Primer**: I worked in data visualization and map-making for most of my career, and solving design problems with data is my jam. To me there's something uniqu...

### 구현 노트

- 기존에 같은 역할의 컴포넌트가 있으면 토큰 교체부터 시작
- variant prop으로 시각적 변형을 관리 (하드코딩 금지)
- error 상태에서 helper text → error message로 자동 전환
- label은 항상 visible (placeholder만으로 대체 금지)
- 애니메이션은 상태 설명용으로만 사용, 장식 효과 금지
- 텍스트 위계가 핵심 — 컬러보다 weight/size로 구분

---

## overlay / modal-dialog

**역할**: 확인/입력을 받는 모달

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

- [calm+editorial] motion: 150-200ms ease-out, bounce/spring 없음 + 콘텐츠 전환 위주, UI chrome 모션 최소화
- [calm+editorial] density: comfortable 모드 기본, 여유로운 padding + 넉넉한 line-height와 margin, 읽기 편한 간격

### 레퍼런스 근거

- **Primer**: ActionMenu is composed of ActionList and Overlay patterns used for quick actions and selections. AnchoredOverlay

### 구현 노트

- 기존에 같은 역할의 컴포넌트가 있으면 토큰 교체부터 시작
- variant prop으로 시각적 변형을 관리 (하드코딩 금지)
- Escape / backdrop click으로 닫기, 열 때 첫 focusable 요소로 이동
- 애니메이션은 상태 설명용으로만 사용, 장식 효과 금지
- 텍스트 위계가 핵심 — 컬러보다 weight/size로 구분

---

## overlay / bottom-sheet

**역할**: 모바일용 하단 시트

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

- [calm+editorial] motion: 150-200ms ease-out, bounce/spring 없음 + 콘텐츠 전환 위주, UI chrome 모션 최소화
- [calm+editorial] density: comfortable 모드 기본, 여유로운 padding + 넉넉한 line-height와 margin, 읽기 편한 간격

### 레퍼런스 근거

- **Primer**: ActionMenu is composed of ActionList and Overlay patterns used for quick actions and selections. AnchoredOverlay

### 구현 노트

- 기존에 같은 역할의 컴포넌트가 있으면 토큰 교체부터 시작
- variant prop으로 시각적 변형을 관리 (하드코딩 금지)
- Escape / backdrop click으로 닫기, 열 때 첫 focusable 요소로 이동
- 애니메이션은 상태 설명용으로만 사용, 장식 효과 금지
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

- [calm+editorial] motion: 150-200ms ease-out, bounce/spring 없음 + 콘텐츠 전환 위주, UI chrome 모션 최소화
- [calm+editorial] density: comfortable 모드 기본, 여유로운 padding + 넉넉한 line-height와 margin, 읽기 편한 간격

### 레퍼런스 근거

- **Primer**: ActionMenu is composed of ActionList and Overlay patterns used for quick actions and selections. AnchoredOverlay

### 구현 노트

- 기존에 같은 역할의 컴포넌트가 있으면 토큰 교체부터 시작
- variant prop으로 시각적 변형을 관리 (하드코딩 금지)
- Escape / backdrop click으로 닫기, 열 때 첫 focusable 요소로 이동
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

- [calm+editorial] density: comfortable 모드 기본, 여유로운 padding + 넉넉한 line-height와 margin, 읽기 편한 간격
- [calm+editorial] color: 중성 톤 위주, accent는 최소한으로 + 타이포그래피로 위계 형성, 컬러보다 weight/size 활용

### Visual Adaptation Hints

- **card_elevation_tendency**: 카드는 낮은 elevation만 허용하고 색면 차이로 그룹을 구분한다. 내부 여백은 넉넉하게 두고 card breathing room을 확보한다. (source=cards; confidence=0.94; provenance=inferred; direction=low-elevation tinted cards를 기본으로 하고, 넓은 내부 여백과 강한 section breathing room. 중간 반경으로 제품 UI 절제 유지.; evidence=surface=tinted, density=airy, corner=medium)
- **border_vs_fill_emphasis**: fill 중심이다. tint surface로 성격을 만들고 border는 아주 얇게 보조한다. (source=cards; confidence=0.94; provenance=inferred; direction=low-elevation tinted cards를 기본으로 하고, 넓은 내부 여백과 강한 section breathing room. 중간 반경으로 제품 UI 절제 유지.; evidence=surface=tinted, density=airy, corner=medium)
- **chart_panel_framing**: 차트 패널은 soft tint frame과 restrained divider로 프레이밍한다. 헤더 메타데이터와 본문 visualization 사이의 breathing room을 충분히 둔다. (source=data_display; confidence=0.94; provenance=inferred; direction=정보 밀도를 유지하되 thin dividers와 restrained accent로 hierarchy를 만든다.; evidence=layout=dashboard-grid, density=airy, layout=conversation-panel, surface=tinted)

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

- [calm+editorial] density: comfortable 모드 기본, 여유로운 padding + 넉넉한 line-height와 margin, 읽기 편한 간격
- [calm+editorial] color: 중성 톤 위주, accent는 최소한으로 + 타이포그래피로 위계 형성, 컬러보다 weight/size 활용

### Visual Adaptation Hints

- **card_elevation_tendency**: 카드는 낮은 elevation만 허용하고 색면 차이로 그룹을 구분한다. 내부 여백은 넉넉하게 두고 card breathing room을 확보한다. (source=cards; confidence=0.94; provenance=inferred; direction=low-elevation tinted cards를 기본으로 하고, 넓은 내부 여백과 강한 section breathing room. 중간 반경으로 제품 UI 절제 유지.; evidence=surface=tinted, density=airy, corner=medium)
- **border_vs_fill_emphasis**: fill 중심이다. tint surface로 성격을 만들고 border는 아주 얇게 보조한다. (source=cards; confidence=0.94; provenance=inferred; direction=low-elevation tinted cards를 기본으로 하고, 넓은 내부 여백과 강한 section breathing room. 중간 반경으로 제품 UI 절제 유지.; evidence=surface=tinted, density=airy, corner=medium)
- **chart_panel_framing**: 차트 패널은 soft tint frame과 restrained divider로 프레이밍한다. 헤더 메타데이터와 본문 visualization 사이의 breathing room을 충분히 둔다. (source=data_display; confidence=0.94; provenance=inferred; direction=정보 밀도를 유지하되 thin dividers와 restrained accent로 hierarchy를 만든다.; evidence=layout=dashboard-grid, density=airy, layout=conversation-panel, surface=tinted)

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

- [calm+editorial] density: comfortable 모드 기본, 여유로운 padding + 넉넉한 line-height와 margin, 읽기 편한 간격
- [calm+editorial] color: 중성 톤 위주, accent는 최소한으로 + 타이포그래피로 위계 형성, 컬러보다 weight/size 활용

### Visual Adaptation Hints

- **card_elevation_tendency**: 카드는 낮은 elevation만 허용하고 색면 차이로 그룹을 구분한다. 내부 여백은 넉넉하게 두고 card breathing room을 확보한다. (source=cards; confidence=0.94; provenance=inferred; direction=low-elevation tinted cards를 기본으로 하고, 넓은 내부 여백과 강한 section breathing room. 중간 반경으로 제품 UI 절제 유지.; evidence=surface=tinted, density=airy, corner=medium)
- **border_vs_fill_emphasis**: fill 중심이다. tint surface로 성격을 만들고 border는 아주 얇게 보조한다. (source=cards; confidence=0.94; provenance=inferred; direction=low-elevation tinted cards를 기본으로 하고, 넓은 내부 여백과 강한 section breathing room. 중간 반경으로 제품 UI 절제 유지.; evidence=surface=tinted, density=airy, corner=medium)
- **chart_panel_framing**: 차트 패널은 soft tint frame과 restrained divider로 프레이밍한다. 헤더 메타데이터와 본문 visualization 사이의 breathing room을 충분히 둔다. (source=data_display; confidence=0.94; provenance=inferred; direction=정보 밀도를 유지하되 thin dividers와 restrained accent로 hierarchy를 만든다.; evidence=layout=dashboard-grid, density=airy, layout=conversation-panel, surface=tinted)

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

- [calm+editorial] feedback: subtle inline alert 선호, 과한 컬러 블록 지양 + 콘텐츠 맥락 안에서 인라인 표시, 토스트보다 인라인 선호
- [calm+editorial] motion: 150-200ms ease-out, bounce/spring 없음 + 콘텐츠 전환 위주, UI chrome 모션 최소화
- [calm+editorial] color: 중성 톤 위주, accent는 최소한으로 + 타이포그래피로 위계 형성, 컬러보다 weight/size 활용

### 레퍼런스 근거

- **Carbon Design System**: We welcome all feedback, designs, or ideas in order to produce the best possible experience for our users. If you're interested in contributing, ch...
- **Primer**: Messaging components are used to provide important and relevant information to the user, including feedback, contextual information, product update...

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

- [calm+editorial] feedback: subtle inline alert 선호, 과한 컬러 블록 지양 + 콘텐츠 맥락 안에서 인라인 표시, 토스트보다 인라인 선호
- [calm+editorial] motion: 150-200ms ease-out, bounce/spring 없음 + 콘텐츠 전환 위주, UI chrome 모션 최소화
- [calm+editorial] color: 중성 톤 위주, accent는 최소한으로 + 타이포그래피로 위계 형성, 컬러보다 weight/size 활용

### 레퍼런스 근거

- **Carbon Design System**: We welcome all feedback, designs, or ideas in order to produce the best possible experience for our users. If you're interested in contributing, ch...
- **Primer**: Messaging components are used to provide important and relevant information to the user, including feedback, contextual information, product update...

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

- [calm+editorial] feedback: subtle inline alert 선호, 과한 컬러 블록 지양 + 콘텐츠 맥락 안에서 인라인 표시, 토스트보다 인라인 선호
- [calm+editorial] motion: 150-200ms ease-out, bounce/spring 없음 + 콘텐츠 전환 위주, UI chrome 모션 최소화
- [calm+editorial] color: 중성 톤 위주, accent는 최소한으로 + 타이포그래피로 위계 형성, 컬러보다 weight/size 활용

### Visual Adaptation Hints

- **card_elevation_tendency**: 카드는 낮은 elevation만 허용하고 색면 차이로 그룹을 구분한다. 내부 여백은 넉넉하게 두고 card breathing room을 확보한다. (source=cards; confidence=0.94; provenance=inferred; direction=low-elevation tinted cards를 기본으로 하고, 넓은 내부 여백과 강한 section breathing room. 중간 반경으로 제품 UI 절제 유지.; evidence=surface=tinted, density=airy, corner=medium)
- **border_vs_fill_emphasis**: fill 중심이다. tint surface로 성격을 만들고 border는 아주 얇게 보조한다. (source=cards; confidence=0.94; provenance=inferred; direction=low-elevation tinted cards를 기본으로 하고, 넓은 내부 여백과 강한 section breathing room. 중간 반경으로 제품 UI 절제 유지.; evidence=surface=tinted, density=airy, corner=medium)
- **chart_panel_framing**: 차트 패널은 soft tint frame과 restrained divider로 프레이밍한다. 헤더 메타데이터와 본문 visualization 사이의 breathing room을 충분히 둔다. (source=data_display; confidence=0.94; provenance=inferred; direction=정보 밀도를 유지하되 thin dividers와 restrained accent로 hierarchy를 만든다.; evidence=layout=dashboard-grid, density=airy, layout=conversation-panel, surface=tinted)

### 레퍼런스 근거

- **Carbon Design System**: We welcome all feedback, designs, or ideas in order to produce the best possible experience for our users. If you're interested in contributing, ch...
- **Primer**: Empty states Empty states are used to fill spaces when no content has been added yet, or is temporarily empty due to the nature of the feature.

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

- [calm+editorial] feedback: subtle inline alert 선호, 과한 컬러 블록 지양 + 콘텐츠 맥락 안에서 인라인 표시, 토스트보다 인라인 선호
- [calm+editorial] motion: 150-200ms ease-out, bounce/spring 없음 + 콘텐츠 전환 위주, UI chrome 모션 최소화
- [calm+editorial] color: 중성 톤 위주, accent는 최소한으로 + 타이포그래피로 위계 형성, 컬러보다 weight/size 활용

### Visual Adaptation Hints

- **card_elevation_tendency**: 카드는 낮은 elevation만 허용하고 색면 차이로 그룹을 구분한다. 내부 여백은 넉넉하게 두고 card breathing room을 확보한다. (source=cards; confidence=0.94; provenance=inferred; direction=low-elevation tinted cards를 기본으로 하고, 넓은 내부 여백과 강한 section breathing room. 중간 반경으로 제품 UI 절제 유지.; evidence=surface=tinted, density=airy, corner=medium)
- **border_vs_fill_emphasis**: fill 중심이다. tint surface로 성격을 만들고 border는 아주 얇게 보조한다. (source=cards; confidence=0.94; provenance=inferred; direction=low-elevation tinted cards를 기본으로 하고, 넓은 내부 여백과 강한 section breathing room. 중간 반경으로 제품 UI 절제 유지.; evidence=surface=tinted, density=airy, corner=medium)

### 레퍼런스 근거

- **Carbon Design System**: We welcome all feedback, designs, or ideas in order to produce the best possible experience for our users. If you're interested in contributing, ch...
- **Primer**: Banner Banner is used to highlight important information.

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

- [calm+editorial] hover: opacity 변화 (0.08-0.12), elevation 변화 없음 + 텍스트 underline 또는 color shift, 장식적 효과 없음
- [calm+editorial] density: comfortable 모드 기본, 여유로운 padding + 넉넉한 line-height와 margin, 읽기 편한 간격
- [calm+editorial] feedback: subtle inline alert 선호, 과한 컬러 블록 지양 + 콘텐츠 맥락 안에서 인라인 표시, 토스트보다 인라인 선호

### Visual Adaptation Hints

- **filter_nav_density**: filter/nav density는 balanced다. global nav와 local filter를 섞지 말고 계층별 간격 차이로 구조를 드러낸다. (source=navigation; confidence=0.94; provenance=inferred; direction=고정 sidebar 또는 split-pane navigation을 우선하고, 현재 위치와 scope를 항상 명시한다.; evidence=Split-pane workspace, layout=conversation-panel, density=airy)

### 레퍼런스 근거

- **Carbon Design System**: Number input Text input
- **Primer**: I worked in data visualization and map-making for most of my career, and solving design problems with data is my jam. To me there's something uniqu...

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

- [calm+editorial] density: comfortable 모드 기본, 여유로운 padding + 넉넉한 line-height와 margin, 읽기 편한 간격
- [calm+editorial] color: 중성 톤 위주, accent는 최소한으로 + 타이포그래피로 위계 형성, 컬러보다 weight/size 활용

### Visual Adaptation Hints

- **card_elevation_tendency**: 카드는 낮은 elevation만 허용하고 색면 차이로 그룹을 구분한다. 내부 여백은 넉넉하게 두고 card breathing room을 확보한다. (source=cards; confidence=0.94; provenance=inferred; direction=low-elevation tinted cards를 기본으로 하고, 넓은 내부 여백과 강한 section breathing room. 중간 반경으로 제품 UI 절제 유지.; evidence=surface=tinted, density=airy, corner=medium)
- **border_vs_fill_emphasis**: fill 중심이다. tint surface로 성격을 만들고 border는 아주 얇게 보조한다. (source=cards; confidence=0.94; provenance=inferred; direction=low-elevation tinted cards를 기본으로 하고, 넓은 내부 여백과 강한 section breathing room. 중간 반경으로 제품 UI 절제 유지.; evidence=surface=tinted, density=airy, corner=medium)
- **filter_nav_density**: filter/nav density는 balanced다. global nav와 local filter를 섞지 말고 계층별 간격 차이로 구조를 드러낸다. (source=navigation; confidence=0.94; provenance=inferred; direction=고정 sidebar 또는 split-pane navigation을 우선하고, 현재 위치와 scope를 항상 명시한다.; evidence=Split-pane workspace, layout=conversation-panel, density=airy)
- **chart_panel_framing**: 차트 패널은 soft tint frame과 restrained divider로 프레이밍한다. 헤더 메타데이터와 본문 visualization 사이의 breathing room을 충분히 둔다. (source=data_display; confidence=0.94; provenance=inferred; direction=정보 밀도를 유지하되 thin dividers와 restrained accent로 hierarchy를 만든다.; evidence=layout=dashboard-grid, density=airy, layout=conversation-panel, surface=tinted)

### 구현 노트

- 기존에 같은 역할의 컴포넌트가 있으면 토큰 교체부터 시작
- variant prop으로 시각적 변형을 관리 (하드코딩 금지)
- 빈 상태(empty-state)와 에러 상태를 반드시 처리
- 좁은 UI 텍스트는 Pretendard 기준 label line-height 1.4-1.5를 참고해 뭉침을 방지
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

- [calm+editorial] hover: opacity 변화 (0.08-0.12), elevation 변화 없음 + 텍스트 underline 또는 color shift, 장식적 효과 없음
- [calm+editorial] density: comfortable 모드 기본, 여유로운 padding + 넉넉한 line-height와 margin, 읽기 편한 간격
- [calm+editorial] feedback: subtle inline alert 선호, 과한 컬러 블록 지양 + 콘텐츠 맥락 안에서 인라인 표시, 토스트보다 인라인 선호

### Visual Adaptation Hints

- **card_elevation_tendency**: 카드는 낮은 elevation만 허용하고 색면 차이로 그룹을 구분한다. 내부 여백은 넉넉하게 두고 card breathing room을 확보한다. (source=cards; confidence=0.94; provenance=inferred; direction=low-elevation tinted cards를 기본으로 하고, 넓은 내부 여백과 강한 section breathing room. 중간 반경으로 제품 UI 절제 유지.; evidence=surface=tinted, density=airy, corner=medium)
- **border_vs_fill_emphasis**: fill 중심이다. tint surface로 성격을 만들고 border는 아주 얇게 보조한다. (source=cards; confidence=0.94; provenance=inferred; direction=low-elevation tinted cards를 기본으로 하고, 넓은 내부 여백과 강한 section breathing room. 중간 반경으로 제품 UI 절제 유지.; evidence=surface=tinted, density=airy, corner=medium)
- **filter_nav_density**: filter/nav density는 balanced다. global nav와 local filter를 섞지 말고 계층별 간격 차이로 구조를 드러낸다. (source=navigation; confidence=0.94; provenance=inferred; direction=고정 sidebar 또는 split-pane navigation을 우선하고, 현재 위치와 scope를 항상 명시한다.; evidence=Split-pane workspace, layout=conversation-panel, density=airy)
- **chart_panel_framing**: 차트 패널은 soft tint frame과 restrained divider로 프레이밍한다. 헤더 메타데이터와 본문 visualization 사이의 breathing room을 충분히 둔다. (source=data_display; confidence=0.94; provenance=inferred; direction=정보 밀도를 유지하되 thin dividers와 restrained accent로 hierarchy를 만든다.; evidence=layout=dashboard-grid, density=airy, layout=conversation-panel, surface=tinted)

### 레퍼런스 근거

- **Carbon Design System**: Number input Text input
- **Primer**: I worked in data visualization and map-making for most of my career, and solving design problems with data is my jam. To me there's something uniqu...

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

- [calm+editorial] motion: 150-200ms ease-out, bounce/spring 없음 + 콘텐츠 전환 위주, UI chrome 모션 최소화
- [calm+editorial] density: comfortable 모드 기본, 여유로운 padding + 넉넉한 line-height와 margin, 읽기 편한 간격

### 레퍼런스 근거

- **Primer**: Autocomplete Autocomplete allows users to quickly filter through a list of options and pick one or more values for a field.

### 구현 노트

- 기존에 같은 역할의 컴포넌트가 있으면 토큰 교체부터 시작
- variant prop으로 시각적 변형을 관리 (하드코딩 금지)
- Escape / backdrop click으로 닫기, 열 때 첫 focusable 요소로 이동
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

- [calm+editorial] density: comfortable 모드 기본, 여유로운 padding + 넉넉한 line-height와 margin, 읽기 편한 간격
- [calm+editorial] color: 중성 톤 위주, accent는 최소한으로 + 타이포그래피로 위계 형성, 컬러보다 weight/size 활용

### Visual Adaptation Hints

- **card_elevation_tendency**: 카드는 낮은 elevation만 허용하고 색면 차이로 그룹을 구분한다. 내부 여백은 넉넉하게 두고 card breathing room을 확보한다. (source=cards; confidence=0.94; provenance=inferred; direction=low-elevation tinted cards를 기본으로 하고, 넓은 내부 여백과 강한 section breathing room. 중간 반경으로 제품 UI 절제 유지.; evidence=surface=tinted, density=airy, corner=medium)
- **border_vs_fill_emphasis**: fill 중심이다. tint surface로 성격을 만들고 border는 아주 얇게 보조한다. (source=cards; confidence=0.94; provenance=inferred; direction=low-elevation tinted cards를 기본으로 하고, 넓은 내부 여백과 강한 section breathing room. 중간 반경으로 제품 UI 절제 유지.; evidence=surface=tinted, density=airy, corner=medium)
- **chart_panel_framing**: 차트 패널은 soft tint frame과 restrained divider로 프레이밍한다. 헤더 메타데이터와 본문 visualization 사이의 breathing room을 충분히 둔다. (source=data_display; confidence=0.94; provenance=inferred; direction=정보 밀도를 유지하되 thin dividers와 restrained accent로 hierarchy를 만든다.; evidence=layout=dashboard-grid, density=airy, layout=conversation-panel, surface=tinted)

### 구현 노트

- 기존에 같은 역할의 컴포넌트가 있으면 토큰 교체부터 시작
- variant prop으로 시각적 변형을 관리 (하드코딩 금지)
- 빈 상태(empty-state)와 에러 상태를 반드시 처리
- 좁은 UI 텍스트는 Pretendard 기준 label line-height 1.4-1.5를 참고해 뭉침을 방지
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

- [calm+editorial] density: comfortable 모드 기본, 여유로운 padding + 넉넉한 line-height와 margin, 읽기 편한 간격
- [calm+editorial] color: 중성 톤 위주, accent는 최소한으로 + 타이포그래피로 위계 형성, 컬러보다 weight/size 활용

### Visual Adaptation Hints

- **card_elevation_tendency**: 카드는 낮은 elevation만 허용하고 색면 차이로 그룹을 구분한다. 내부 여백은 넉넉하게 두고 card breathing room을 확보한다. (source=cards; confidence=0.94; provenance=inferred; direction=low-elevation tinted cards를 기본으로 하고, 넓은 내부 여백과 강한 section breathing room. 중간 반경으로 제품 UI 절제 유지.; evidence=surface=tinted, density=airy, corner=medium)
- **border_vs_fill_emphasis**: fill 중심이다. tint surface로 성격을 만들고 border는 아주 얇게 보조한다. (source=cards; confidence=0.94; provenance=inferred; direction=low-elevation tinted cards를 기본으로 하고, 넓은 내부 여백과 강한 section breathing room. 중간 반경으로 제품 UI 절제 유지.; evidence=surface=tinted, density=airy, corner=medium)
- **chart_panel_framing**: 차트 패널은 soft tint frame과 restrained divider로 프레이밍한다. 헤더 메타데이터와 본문 visualization 사이의 breathing room을 충분히 둔다. (source=data_display; confidence=0.94; provenance=inferred; direction=정보 밀도를 유지하되 thin dividers와 restrained accent로 hierarchy를 만든다.; evidence=layout=dashboard-grid, density=airy, layout=conversation-panel, surface=tinted)

### 구현 노트

- 기존에 같은 역할의 컴포넌트가 있으면 토큰 교체부터 시작
- variant prop으로 시각적 변형을 관리 (하드코딩 금지)
- 빈 상태(empty-state)와 에러 상태를 반드시 처리
- 좁은 UI 텍스트는 Pretendard 기준 label line-height 1.4-1.5를 참고해 뭉침을 방지
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

- [calm+editorial] density: comfortable 모드 기본, 여유로운 padding + 넉넉한 line-height와 margin, 읽기 편한 간격
- [calm+editorial] color: 중성 톤 위주, accent는 최소한으로 + 타이포그래피로 위계 형성, 컬러보다 weight/size 활용

### Visual Adaptation Hints

- **card_elevation_tendency**: 카드는 낮은 elevation만 허용하고 색면 차이로 그룹을 구분한다. 내부 여백은 넉넉하게 두고 card breathing room을 확보한다. (source=cards; confidence=0.94; provenance=inferred; direction=low-elevation tinted cards를 기본으로 하고, 넓은 내부 여백과 강한 section breathing room. 중간 반경으로 제품 UI 절제 유지.; evidence=surface=tinted, density=airy, corner=medium)
- **border_vs_fill_emphasis**: fill 중심이다. tint surface로 성격을 만들고 border는 아주 얇게 보조한다. (source=cards; confidence=0.94; provenance=inferred; direction=low-elevation tinted cards를 기본으로 하고, 넓은 내부 여백과 강한 section breathing room. 중간 반경으로 제품 UI 절제 유지.; evidence=surface=tinted, density=airy, corner=medium)
- **chart_panel_framing**: 차트 패널은 soft tint frame과 restrained divider로 프레이밍한다. 헤더 메타데이터와 본문 visualization 사이의 breathing room을 충분히 둔다. (source=data_display; confidence=0.94; provenance=inferred; direction=정보 밀도를 유지하되 thin dividers와 restrained accent로 hierarchy를 만든다.; evidence=layout=dashboard-grid, density=airy, layout=conversation-panel, surface=tinted)

### 구현 노트

- 기존에 같은 역할의 컴포넌트가 있으면 토큰 교체부터 시작
- variant prop으로 시각적 변형을 관리 (하드코딩 금지)
- 빈 상태(empty-state)와 에러 상태를 반드시 처리
- 좁은 UI 텍스트는 Pretendard 기준 label line-height 1.4-1.5를 참고해 뭉침을 방지
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

- [calm+editorial] density: comfortable 모드 기본, 여유로운 padding + 넉넉한 line-height와 margin, 읽기 편한 간격
- [calm+editorial] color: 중성 톤 위주, accent는 최소한으로 + 타이포그래피로 위계 형성, 컬러보다 weight/size 활용

### Visual Adaptation Hints

- **card_elevation_tendency**: 카드는 낮은 elevation만 허용하고 색면 차이로 그룹을 구분한다. 내부 여백은 넉넉하게 두고 card breathing room을 확보한다. (source=cards; confidence=0.94; provenance=inferred; direction=low-elevation tinted cards를 기본으로 하고, 넓은 내부 여백과 강한 section breathing room. 중간 반경으로 제품 UI 절제 유지.; evidence=surface=tinted, density=airy, corner=medium)
- **border_vs_fill_emphasis**: fill 중심이다. tint surface로 성격을 만들고 border는 아주 얇게 보조한다. (source=cards; confidence=0.94; provenance=inferred; direction=low-elevation tinted cards를 기본으로 하고, 넓은 내부 여백과 강한 section breathing room. 중간 반경으로 제품 UI 절제 유지.; evidence=surface=tinted, density=airy, corner=medium)
- **chart_panel_framing**: 차트 패널은 soft tint frame과 restrained divider로 프레이밍한다. 헤더 메타데이터와 본문 visualization 사이의 breathing room을 충분히 둔다. (source=data_display; confidence=0.94; provenance=inferred; direction=정보 밀도를 유지하되 thin dividers와 restrained accent로 hierarchy를 만든다.; evidence=layout=dashboard-grid, density=airy, layout=conversation-panel, surface=tinted)

### 구현 노트

- 기존에 같은 역할의 컴포넌트가 있으면 토큰 교체부터 시작
- variant prop으로 시각적 변형을 관리 (하드코딩 금지)
- 빈 상태(empty-state)와 에러 상태를 반드시 처리
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

- [calm+editorial] color: 중성 톤 위주, accent는 최소한으로 + 타이포그래피로 위계 형성, 컬러보다 weight/size 활용
- [calm+editorial] motion: 150-200ms ease-out, bounce/spring 없음 + 콘텐츠 전환 위주, UI chrome 모션 최소화
- [calm+editorial] density: comfortable 모드 기본, 여유로운 padding + 넉넉한 line-height와 margin, 읽기 편한 간격

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

- [calm+editorial] color: 중성 톤 위주, accent는 최소한으로 + 타이포그래피로 위계 형성, 컬러보다 weight/size 활용
- [calm+editorial] motion: 150-200ms ease-out, bounce/spring 없음 + 콘텐츠 전환 위주, UI chrome 모션 최소화
- [calm+editorial] density: comfortable 모드 기본, 여유로운 padding + 넉넉한 line-height와 margin, 읽기 편한 간격

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

- [calm+editorial] color: 중성 톤 위주, accent는 최소한으로 + 타이포그래피로 위계 형성, 컬러보다 weight/size 활용
- [calm+editorial] motion: 150-200ms ease-out, bounce/spring 없음 + 콘텐츠 전환 위주, UI chrome 모션 최소화
- [calm+editorial] density: comfortable 모드 기본, 여유로운 padding + 넉넉한 line-height와 margin, 읽기 편한 간격

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

- [calm+editorial] color: 중성 톤 위주, accent는 최소한으로 + 타이포그래피로 위계 형성, 컬러보다 weight/size 활용
- [calm+editorial] motion: 150-200ms ease-out, bounce/spring 없음 + 콘텐츠 전환 위주, UI chrome 모션 최소화
- [calm+editorial] density: comfortable 모드 기본, 여유로운 padding + 넉넉한 line-height와 margin, 읽기 편한 간격

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

- [calm+editorial] color: 중성 톤 위주, accent는 최소한으로 + 타이포그래피로 위계 형성, 컬러보다 weight/size 활용
- [calm+editorial] motion: 150-200ms ease-out, bounce/spring 없음 + 콘텐츠 전환 위주, UI chrome 모션 최소화
- [calm+editorial] density: comfortable 모드 기본, 여유로운 padding + 넉넉한 line-height와 margin, 읽기 편한 간격

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

- [calm+editorial] feedback: subtle inline alert 선호, 과한 컬러 블록 지양 + 콘텐츠 맥락 안에서 인라인 표시, 토스트보다 인라인 선호
- [calm+editorial] motion: 150-200ms ease-out, bounce/spring 없음 + 콘텐츠 전환 위주, UI chrome 모션 최소화
- [calm+editorial] color: 중성 톤 위주, accent는 최소한으로 + 타이포그래피로 위계 형성, 컬러보다 weight/size 활용

### 레퍼런스 근거

- **Carbon Design System**: We welcome all feedback, designs, or ideas in order to produce the best possible experience for our users. If you're interested in contributing, ch...
- **Primer**: Messaging components are used to provide important and relevant information to the user, including feedback, contextual information, product update...

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

- [calm+editorial] hover: opacity 변화 (0.08-0.12), elevation 변화 없음 + 텍스트 underline 또는 color shift, 장식적 효과 없음
- [calm+editorial] density: comfortable 모드 기본, 여유로운 padding + 넉넉한 line-height와 margin, 읽기 편한 간격
- [calm+editorial] motion: 150-200ms ease-out, bounce/spring 없음 + 콘텐츠 전환 위주, UI chrome 모션 최소화

### Visual Adaptation Hints

- **filter_nav_density**: filter/nav density는 balanced다. global nav와 local filter를 섞지 말고 계층별 간격 차이로 구조를 드러낸다. (source=navigation; confidence=0.94; provenance=inferred; direction=고정 sidebar 또는 split-pane navigation을 우선하고, 현재 위치와 scope를 항상 명시한다.; evidence=Split-pane workspace, layout=conversation-panel, density=airy)

### 레퍼런스 근거

- **Carbon Design System**: Library menu navigation There are two kinds of symbols — library symbols and document symbols. Library symbols are available in any Sketch document...
- **Primer**: Octicon nav items navigation 12 px

### 구현 노트

- 기존에 같은 역할의 컴포넌트가 있으면 토큰 교체부터 시작
- variant prop으로 시각적 변형을 관리 (하드코딩 금지)
- active 상태는 URL/라우터와 자동 동기화
- 좁은 UI 텍스트는 Pretendard 기준 label line-height 1.4-1.5를 참고해 뭉침을 방지
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

- [calm+editorial] motion: 150-200ms ease-out, bounce/spring 없음 + 콘텐츠 전환 위주, UI chrome 모션 최소화
- [calm+editorial] density: comfortable 모드 기본, 여유로운 padding + 넉넉한 line-height와 margin, 읽기 편한 간격

### 레퍼런스 근거

- **Primer**: ActionMenu is composed of ActionList and Overlay patterns used for quick actions and selections. AnchoredOverlay

### 구현 노트

- 기존에 같은 역할의 컴포넌트가 있으면 토큰 교체부터 시작
- variant prop으로 시각적 변형을 관리 (하드코딩 금지)
- Escape / backdrop click으로 닫기, 열 때 첫 focusable 요소로 이동
- 애니메이션은 상태 설명용으로만 사용, 장식 효과 금지
- 텍스트 위계가 핵심 — 컬러보다 weight/size로 구분

---

## social / feed-item

**역할**: timeline stream 의 기본 단위 — avatar + post card wrap

**탐지 출처**: community feed

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

- [calm+editorial] hover: opacity 변화 (0.08-0.12), elevation 변화 없음 + 텍스트 underline 또는 color shift, 장식적 효과 없음
- [calm+editorial] motion: 150-200ms ease-out, bounce/spring 없음 + 콘텐츠 전환 위주, UI chrome 모션 최소화
- [calm+editorial] color: 중성 톤 위주, accent는 최소한으로 + 타이포그래피로 위계 형성, 컬러보다 weight/size 활용

### 레퍼런스 근거

- **Primer**: Onboarding is a virtual unboxing experience that helps users get started with a feature. This is a guide for designing onboarding for the product a...

### 구현 노트

- 기존에 같은 역할의 컴포넌트가 있으면 토큰 교체부터 시작
- variant prop으로 시각적 변형을 관리 (하드코딩 금지)
- 애니메이션은 상태 설명용으로만 사용, 장식 효과 금지
- 텍스트 위계가 핵심 — 컬러보다 weight/size로 구분

---

## social / post-card

**역할**: rounded post card — 본문 + 이미지 + 반응 + 스레드 미리보기

**탐지 출처**: community feed

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

- [calm+editorial] hover: opacity 변화 (0.08-0.12), elevation 변화 없음 + 텍스트 underline 또는 color shift, 장식적 효과 없음
- [calm+editorial] motion: 150-200ms ease-out, bounce/spring 없음 + 콘텐츠 전환 위주, UI chrome 모션 최소화
- [calm+editorial] color: 중성 톤 위주, accent는 최소한으로 + 타이포그래피로 위계 형성, 컬러보다 weight/size 활용

### Visual Adaptation Hints

- **card_elevation_tendency**: 카드는 낮은 elevation만 허용하고 색면 차이로 그룹을 구분한다. 내부 여백은 넉넉하게 두고 card breathing room을 확보한다. (source=cards; confidence=0.94; provenance=inferred; direction=low-elevation tinted cards를 기본으로 하고, 넓은 내부 여백과 강한 section breathing room. 중간 반경으로 제품 UI 절제 유지.; evidence=surface=tinted, density=airy, corner=medium)
- **border_vs_fill_emphasis**: fill 중심이다. tint surface로 성격을 만들고 border는 아주 얇게 보조한다. (source=cards; confidence=0.94; provenance=inferred; direction=low-elevation tinted cards를 기본으로 하고, 넓은 내부 여백과 강한 section breathing room. 중간 반경으로 제품 UI 절제 유지.; evidence=surface=tinted, density=airy, corner=medium)

### 레퍼런스 근거

- **Primer**: Onboarding is a virtual unboxing experience that helps users get started with a feature. This is a guide for designing onboarding for the product a...

### 구현 노트

- 기존에 같은 역할의 컴포넌트가 있으면 토큰 교체부터 시작
- variant prop으로 시각적 변형을 관리 (하드코딩 금지)
- 애니메이션은 상태 설명용으로만 사용, 장식 효과 금지
- 텍스트 위계가 핵심 — 컬러보다 weight/size로 구분

---

## social / thread-view

**역할**: 부모 post + reply list + composer 를 엮는 thread 페이지

**탐지 출처**: community feed

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

- [calm+editorial] hover: opacity 변화 (0.08-0.12), elevation 변화 없음 + 텍스트 underline 또는 color shift, 장식적 효과 없음
- [calm+editorial] motion: 150-200ms ease-out, bounce/spring 없음 + 콘텐츠 전환 위주, UI chrome 모션 최소화
- [calm+editorial] color: 중성 톤 위주, accent는 최소한으로 + 타이포그래피로 위계 형성, 컬러보다 weight/size 활용

### 레퍼런스 근거

- **Primer**: Onboarding is a virtual unboxing experience that helps users get started with a feature. This is a guide for designing onboarding for the product a...

### 구현 노트

- 기존에 같은 역할의 컴포넌트가 있으면 토큰 교체부터 시작
- variant prop으로 시각적 변형을 관리 (하드코딩 금지)
- 애니메이션은 상태 설명용으로만 사용, 장식 효과 금지
- 텍스트 위계가 핵심 — 컬러보다 weight/size로 구분

---

## input / reply-composer

**역할**: 친근한 quick reply 입력기 (이모지 picker + mention)

**탐지 출처**: community feed

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

- [calm+editorial] hover: opacity 변화 (0.08-0.12), elevation 변화 없음 + 텍스트 underline 또는 color shift, 장식적 효과 없음
- [calm+editorial] density: comfortable 모드 기본, 여유로운 padding + 넉넉한 line-height와 margin, 읽기 편한 간격
- [calm+editorial] feedback: subtle inline alert 선호, 과한 컬러 블록 지양 + 콘텐츠 맥락 안에서 인라인 표시, 토스트보다 인라인 선호

### 레퍼런스 근거

- **Carbon Design System**: Number input Text input
- **Primer**: I worked in data visualization and map-making for most of my career, and solving design problems with data is my jam. To me there's something uniqu...

### 구현 노트

- 기존에 같은 역할의 컴포넌트가 있으면 토큰 교체부터 시작
- variant prop으로 시각적 변형을 관리 (하드코딩 금지)
- error 상태에서 helper text → error message로 자동 전환
- label은 항상 visible (placeholder만으로 대체 금지)
- 애니메이션은 상태 설명용으로만 사용, 장식 효과 금지
- 텍스트 위계가 핵심 — 컬러보다 weight/size로 구분

---

## social / reaction-bar

**역할**: 이모지 reaction bubble — optimistic update, 좋아요/하트/축하

**탐지 출처**: community feed

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

- [calm+editorial] hover: opacity 변화 (0.08-0.12), elevation 변화 없음 + 텍스트 underline 또는 color shift, 장식적 효과 없음
- [calm+editorial] motion: 150-200ms ease-out, bounce/spring 없음 + 콘텐츠 전환 위주, UI chrome 모션 최소화
- [calm+editorial] color: 중성 톤 위주, accent는 최소한으로 + 타이포그래피로 위계 형성, 컬러보다 weight/size 활용

### 레퍼런스 근거

- **Primer**: Onboarding is a virtual unboxing experience that helps users get started with a feature. This is a guide for designing onboarding for the product a...

### 구현 노트

- 기존에 같은 역할의 컴포넌트가 있으면 토큰 교체부터 시작
- variant prop으로 시각적 변형을 관리 (하드코딩 금지)
- 애니메이션은 상태 설명용으로만 사용, 장식 효과 금지
- 텍스트 위계가 핵심 — 컬러보다 weight/size로 구분

---

## button / follow-button

**역할**: rounded follow toggle — presence 연동, 친근 micro-interaction

**탐지 출처**: community feed

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

- [calm+editorial] hover: opacity 변화 (0.08-0.12), elevation 변화 없음 + 텍스트 underline 또는 color shift, 장식적 효과 없음
- [calm+editorial] motion: 150-200ms ease-out, bounce/spring 없음 + 콘텐츠 전환 위주, UI chrome 모션 최소화
- [calm+editorial] color: 중성 톤 위주, accent는 최소한으로 + 타이포그래피로 위계 형성, 컬러보다 weight/size 활용

### Visual Adaptation Hints

- **cta_prominence**: CTA prominence는 medium이다. primary action은 분명하게 보이되 화면 전체를 지배하지 않게 유지한다. (source=cards; confidence=0.94; provenance=inferred; direction=low-elevation tinted cards를 기본으로 하고, 넓은 내부 여백과 강한 section breathing room. 중간 반경으로 제품 UI 절제 유지.; evidence=surface=tinted, density=airy, corner=medium, layout=conversation-panel)

### 레퍼런스 근거

- **Carbon Design System**: These components can toggle between the AI variant and the default variant depending on the user’s interaction. If the user manually overrides the ...
- **Primer**: I get so much joy from writing HTML and CSS, and design systems are one level up - systematically making UIs accessible and consistent. I love conc...

### 구현 노트

- 기존에 같은 역할의 컴포넌트가 있으면 토큰 교체부터 시작
- variant prop으로 시각적 변형을 관리 (하드코딩 금지)
- size prop: sm / md / lg (터치 영역은 항상 최소 44px 보장)
- 애니메이션은 상태 설명용으로만 사용, 장식 효과 금지
- 텍스트 위계가 핵심 — 컬러보다 weight/size로 구분

---

## social / timeline-stream

**역할**: infinite scroll feed stream, pull-to-refresh

**탐지 출처**: community feed

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

- [calm+editorial] hover: opacity 변화 (0.08-0.12), elevation 변화 없음 + 텍스트 underline 또는 color shift, 장식적 효과 없음
- [calm+editorial] motion: 150-200ms ease-out, bounce/spring 없음 + 콘텐츠 전환 위주, UI chrome 모션 최소화
- [calm+editorial] color: 중성 톤 위주, accent는 최소한으로 + 타이포그래피로 위계 형성, 컬러보다 weight/size 활용

### 레퍼런스 근거

- **Primer**: Onboarding is a virtual unboxing experience that helps users get started with a feature. This is a guide for designing onboarding for the product a...

### 구현 노트

- 기존에 같은 역할의 컴포넌트가 있으면 토큰 교체부터 시작
- variant prop으로 시각적 변형을 관리 (하드코딩 금지)
- 애니메이션은 상태 설명용으로만 사용, 장식 효과 금지
- 텍스트 위계가 핵심 — 컬러보다 weight/size로 구분

---

## social / avatar-cluster

**역할**: 여러 아바타를 겹쳐 보여주는 reaction/참여자 요약

**탐지 출처**: community feed

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

- [calm+editorial] hover: opacity 변화 (0.08-0.12), elevation 변화 없음 + 텍스트 underline 또는 color shift, 장식적 효과 없음
- [calm+editorial] motion: 150-200ms ease-out, bounce/spring 없음 + 콘텐츠 전환 위주, UI chrome 모션 최소화
- [calm+editorial] color: 중성 톤 위주, accent는 최소한으로 + 타이포그래피로 위계 형성, 컬러보다 weight/size 활용

### 레퍼런스 근거

- **Primer**: Onboarding is a virtual unboxing experience that helps users get started with a feature. This is a guide for designing onboarding for the product a...

### 구현 노트

- 기존에 같은 역할의 컴포넌트가 있으면 토큰 교체부터 시작
- variant prop으로 시각적 변형을 관리 (하드코딩 금지)
- 애니메이션은 상태 설명용으로만 사용, 장식 효과 금지
- 텍스트 위계가 핵심 — 컬러보다 weight/size로 구분

---

## data-display / tag-pill

**역할**: rounded tag pill — 해시태그/토픽/카테고리

**탐지 출처**: community feed

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

- [calm+editorial] density: comfortable 모드 기본, 여유로운 padding + 넉넉한 line-height와 margin, 읽기 편한 간격
- [calm+editorial] color: 중성 톤 위주, accent는 최소한으로 + 타이포그래피로 위계 형성, 컬러보다 weight/size 활용

### Visual Adaptation Hints

- **card_elevation_tendency**: 카드는 낮은 elevation만 허용하고 색면 차이로 그룹을 구분한다. 내부 여백은 넉넉하게 두고 card breathing room을 확보한다. (source=cards; confidence=0.94; provenance=inferred; direction=low-elevation tinted cards를 기본으로 하고, 넓은 내부 여백과 강한 section breathing room. 중간 반경으로 제품 UI 절제 유지.; evidence=surface=tinted, density=airy, corner=medium)
- **border_vs_fill_emphasis**: fill 중심이다. tint surface로 성격을 만들고 border는 아주 얇게 보조한다. (source=cards; confidence=0.94; provenance=inferred; direction=low-elevation tinted cards를 기본으로 하고, 넓은 내부 여백과 강한 section breathing room. 중간 반경으로 제품 UI 절제 유지.; evidence=surface=tinted, density=airy, corner=medium)
- **chart_panel_framing**: 차트 패널은 soft tint frame과 restrained divider로 프레이밍한다. 헤더 메타데이터와 본문 visualization 사이의 breathing room을 충분히 둔다. (source=data_display; confidence=0.94; provenance=inferred; direction=정보 밀도를 유지하되 thin dividers와 restrained accent로 hierarchy를 만든다.; evidence=layout=dashboard-grid, density=airy, layout=conversation-panel, surface=tinted)

### 구현 노트

- 기존에 같은 역할의 컴포넌트가 있으면 토큰 교체부터 시작
- variant prop으로 시각적 변형을 관리 (하드코딩 금지)
- 빈 상태(empty-state)와 에러 상태를 반드시 처리
- 좁은 UI 텍스트는 Pretendard 기준 label line-height 1.4-1.5를 참고해 뭉침을 방지
- 애니메이션은 상태 설명용으로만 사용, 장식 효과 금지
- 텍스트 위계가 핵심 — 컬러보다 weight/size로 구분

---

## overlay / share-sheet

**역할**: 친근한 bottom sheet 공유 패널

**탐지 출처**: community feed

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

- [calm+editorial] motion: 150-200ms ease-out, bounce/spring 없음 + 콘텐츠 전환 위주, UI chrome 모션 최소화
- [calm+editorial] density: comfortable 모드 기본, 여유로운 padding + 넉넉한 line-height와 margin, 읽기 편한 간격

### 레퍼런스 근거

- **Primer**: ActionMenu is composed of ActionList and Overlay patterns used for quick actions and selections. AnchoredOverlay

### 구현 노트

- 기존에 같은 역할의 컴포넌트가 있으면 토큰 교체부터 시작
- variant prop으로 시각적 변형을 관리 (하드코딩 금지)
- Escape / backdrop click으로 닫기, 열 때 첫 focusable 요소로 이동
- 애니메이션은 상태 설명용으로만 사용, 장식 효과 금지
- 텍스트 위계가 핵심 — 컬러보다 weight/size로 구분

---

## feedback / empty-feed-illustration

**역할**: empty state illustration — 친근 톤 copy

**탐지 출처**: community feed

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

- [calm+editorial] feedback: subtle inline alert 선호, 과한 컬러 블록 지양 + 콘텐츠 맥락 안에서 인라인 표시, 토스트보다 인라인 선호
- [calm+editorial] motion: 150-200ms ease-out, bounce/spring 없음 + 콘텐츠 전환 위주, UI chrome 모션 최소화
- [calm+editorial] color: 중성 톤 위주, accent는 최소한으로 + 타이포그래피로 위계 형성, 컬러보다 weight/size 활용

### 레퍼런스 근거

- **Carbon Design System**: We welcome all feedback, designs, or ideas in order to produce the best possible experience for our users. If you're interested in contributing, ch...
- **Primer**: Messaging components are used to provide important and relevant information to the user, including feedback, contextual information, product update...

### 구현 노트

- 기존에 같은 역할의 컴포넌트가 있으면 토큰 교체부터 시작
- variant prop으로 시각적 변형을 관리 (하드코딩 금지)
- auto-dismiss 시간은 내용 길이에 비례 (기본 5초)
- 애니메이션은 상태 설명용으로만 사용, 장식 효과 금지
- 텍스트 위계가 핵심 — 컬러보다 weight/size로 구분

---

## feedback / gentle-toast

**역할**: low-noise 성공/완료 toast — playful-soft 모션

**탐지 출처**: community feed

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

- [calm+editorial] feedback: subtle inline alert 선호, 과한 컬러 블록 지양 + 콘텐츠 맥락 안에서 인라인 표시, 토스트보다 인라인 선호
- [calm+editorial] motion: 150-200ms ease-out, bounce/spring 없음 + 콘텐츠 전환 위주, UI chrome 모션 최소화
- [calm+editorial] color: 중성 톤 위주, accent는 최소한으로 + 타이포그래피로 위계 형성, 컬러보다 weight/size 활용

### 레퍼런스 근거

- **Carbon Design System**: We welcome all feedback, designs, or ideas in order to produce the best possible experience for our users. If you're interested in contributing, ch...
- **Primer**: Messaging components are used to provide important and relevant information to the user, including feedback, contextual information, product update...

### 구현 노트

- 기존에 같은 역할의 컴포넌트가 있으면 토큰 교체부터 시작
- variant prop으로 시각적 변형을 관리 (하드코딩 금지)
- auto-dismiss 시간은 내용 길이에 비례 (기본 5초)
- 애니메이션은 상태 설명용으로만 사용, 장식 효과 금지
- 텍스트 위계가 핵심 — 컬러보다 weight/size로 구분

---

## overlay / soft-dialog

**역할**: rounded-16 dialog — 파괴적 액션도 부드럽게 confirm

**탐지 출처**: community feed

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

- [calm+editorial] motion: 150-200ms ease-out, bounce/spring 없음 + 콘텐츠 전환 위주, UI chrome 모션 최소화
- [calm+editorial] density: comfortable 모드 기본, 여유로운 padding + 넉넉한 line-height와 margin, 읽기 편한 간격

### 레퍼런스 근거

- **Primer**: ActionMenu is composed of ActionList and Overlay patterns used for quick actions and selections. AnchoredOverlay

### 구현 노트

- 기존에 같은 역할의 컴포넌트가 있으면 토큰 교체부터 시작
- variant prop으로 시각적 변형을 관리 (하드코딩 금지)
- Escape / backdrop click으로 닫기, 열 때 첫 focusable 요소로 이동
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

- [calm+editorial] density: comfortable 모드 기본, 여유로운 padding + 넉넉한 line-height와 margin, 읽기 편한 간격
- [calm+editorial] color: 중성 톤 위주, accent는 최소한으로 + 타이포그래피로 위계 형성, 컬러보다 weight/size 활용

### Visual Adaptation Hints

- **card_elevation_tendency**: 카드는 낮은 elevation만 허용하고 색면 차이로 그룹을 구분한다. 내부 여백은 넉넉하게 두고 card breathing room을 확보한다. (source=cards; confidence=0.94; provenance=inferred; direction=low-elevation tinted cards를 기본으로 하고, 넓은 내부 여백과 강한 section breathing room. 중간 반경으로 제품 UI 절제 유지.; evidence=surface=tinted, density=airy, corner=medium)
- **border_vs_fill_emphasis**: fill 중심이다. tint surface로 성격을 만들고 border는 아주 얇게 보조한다. (source=cards; confidence=0.94; provenance=inferred; direction=low-elevation tinted cards를 기본으로 하고, 넓은 내부 여백과 강한 section breathing room. 중간 반경으로 제품 UI 절제 유지.; evidence=surface=tinted, density=airy, corner=medium)
- **chart_panel_framing**: 차트 패널은 soft tint frame과 restrained divider로 프레이밍한다. 헤더 메타데이터와 본문 visualization 사이의 breathing room을 충분히 둔다. (source=data_display; confidence=0.94; provenance=inferred; direction=정보 밀도를 유지하되 thin dividers와 restrained accent로 hierarchy를 만든다.; evidence=layout=dashboard-grid, density=airy, layout=conversation-panel, surface=tinted)

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

- [calm+editorial] motion: 150-200ms ease-out, bounce/spring 없음 + 콘텐츠 전환 위주, UI chrome 모션 최소화
- [calm+editorial] density: comfortable 모드 기본, 여유로운 padding + 넉넉한 line-height와 margin, 읽기 편한 간격

### Visual Adaptation Hints

- **filter_nav_density**: filter/nav density는 balanced다. global nav와 local filter를 섞지 말고 계층별 간격 차이로 구조를 드러낸다. (source=navigation; confidence=0.94; provenance=inferred; direction=고정 sidebar 또는 split-pane navigation을 우선하고, 현재 위치와 scope를 항상 명시한다.; evidence=Split-pane workspace, layout=conversation-panel, density=airy)

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

- [calm+editorial] density: comfortable 모드 기본, 여유로운 padding + 넉넉한 line-height와 margin, 읽기 편한 간격
- [calm+editorial] color: 중성 톤 위주, accent는 최소한으로 + 타이포그래피로 위계 형성, 컬러보다 weight/size 활용

### Visual Adaptation Hints

- **card_elevation_tendency**: 카드는 낮은 elevation만 허용하고 색면 차이로 그룹을 구분한다. 내부 여백은 넉넉하게 두고 card breathing room을 확보한다. (source=cards; confidence=0.94; provenance=inferred; direction=low-elevation tinted cards를 기본으로 하고, 넓은 내부 여백과 강한 section breathing room. 중간 반경으로 제품 UI 절제 유지.; evidence=surface=tinted, density=airy, corner=medium)
- **border_vs_fill_emphasis**: fill 중심이다. tint surface로 성격을 만들고 border는 아주 얇게 보조한다. (source=cards; confidence=0.94; provenance=inferred; direction=low-elevation tinted cards를 기본으로 하고, 넓은 내부 여백과 강한 section breathing room. 중간 반경으로 제품 UI 절제 유지.; evidence=surface=tinted, density=airy, corner=medium)
- **chart_panel_framing**: 차트 패널은 soft tint frame과 restrained divider로 프레이밍한다. 헤더 메타데이터와 본문 visualization 사이의 breathing room을 충분히 둔다. (source=data_display; confidence=0.94; provenance=inferred; direction=정보 밀도를 유지하되 thin dividers와 restrained accent로 hierarchy를 만든다.; evidence=layout=dashboard-grid, density=airy, layout=conversation-panel, surface=tinted)

### 구현 노트

- 기존에 같은 역할의 컴포넌트가 있으면 토큰 교체부터 시작
- variant prop으로 시각적 변형을 관리 (하드코딩 금지)
- 빈 상태(empty-state)와 에러 상태를 반드시 처리
- 좁은 UI 텍스트는 Pretendard 기준 label line-height 1.4-1.5를 참고해 뭉침을 방지
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

- [calm+editorial] color: 중성 톤 위주, accent는 최소한으로 + 타이포그래피로 위계 형성, 컬러보다 weight/size 활용
- [calm+editorial] motion: 150-200ms ease-out, bounce/spring 없음 + 콘텐츠 전환 위주, UI chrome 모션 최소화
- [calm+editorial] density: comfortable 모드 기본, 여유로운 padding + 넉넉한 line-height와 margin, 읽기 편한 간격

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

- [calm+editorial] color: 중성 톤 위주, accent는 최소한으로 + 타이포그래피로 위계 형성, 컬러보다 weight/size 활용
- [calm+editorial] motion: 150-200ms ease-out, bounce/spring 없음 + 콘텐츠 전환 위주, UI chrome 모션 최소화
- [calm+editorial] density: comfortable 모드 기본, 여유로운 padding + 넉넉한 line-height와 margin, 읽기 편한 간격

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

- [calm+editorial] color: 중성 톤 위주, accent는 최소한으로 + 타이포그래피로 위계 형성, 컬러보다 weight/size 활용
- [calm+editorial] motion: 150-200ms ease-out, bounce/spring 없음 + 콘텐츠 전환 위주, UI chrome 모션 최소화
- [calm+editorial] density: comfortable 모드 기본, 여유로운 padding + 넉넉한 line-height와 margin, 읽기 편한 간격

### Visual Adaptation Hints

- **card_elevation_tendency**: 카드는 낮은 elevation만 허용하고 색면 차이로 그룹을 구분한다. 내부 여백은 넉넉하게 두고 card breathing room을 확보한다. (source=cards; confidence=0.94; provenance=inferred; direction=low-elevation tinted cards를 기본으로 하고, 넓은 내부 여백과 강한 section breathing room. 중간 반경으로 제품 UI 절제 유지.; evidence=surface=tinted, density=airy, corner=medium)
- **border_vs_fill_emphasis**: fill 중심이다. tint surface로 성격을 만들고 border는 아주 얇게 보조한다. (source=cards; confidence=0.94; provenance=inferred; direction=low-elevation tinted cards를 기본으로 하고, 넓은 내부 여백과 강한 section breathing room. 중간 반경으로 제품 UI 절제 유지.; evidence=surface=tinted, density=airy, corner=medium)
- **chart_panel_framing**: 차트 패널은 soft tint frame과 restrained divider로 프레이밍한다. 헤더 메타데이터와 본문 visualization 사이의 breathing room을 충분히 둔다. (source=data_display; confidence=0.94; provenance=inferred; direction=정보 밀도를 유지하되 thin dividers와 restrained accent로 hierarchy를 만든다.; evidence=layout=dashboard-grid, density=airy, layout=conversation-panel, surface=tinted)

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

- [calm+editorial] color: 중성 톤 위주, accent는 최소한으로 + 타이포그래피로 위계 형성, 컬러보다 weight/size 활용
- [calm+editorial] motion: 150-200ms ease-out, bounce/spring 없음 + 콘텐츠 전환 위주, UI chrome 모션 최소화
- [calm+editorial] density: comfortable 모드 기본, 여유로운 padding + 넉넉한 line-height와 margin, 읽기 편한 간격

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

- [calm+editorial] hover: opacity 변화 (0.08-0.12), elevation 변화 없음 + 텍스트 underline 또는 color shift, 장식적 효과 없음
- [calm+editorial] motion: 150-200ms ease-out, bounce/spring 없음 + 콘텐츠 전환 위주, UI chrome 모션 최소화
- [calm+editorial] color: 중성 톤 위주, accent는 최소한으로 + 타이포그래피로 위계 형성, 컬러보다 weight/size 활용

### 레퍼런스 근거

- **Carbon Design System**: AI chat is a conversational framework between a user and an AI that can aid in creating tasks, finding insights, tracking documents, and more. For ...
- **Primer**: The GitHub Design Infrastructure and Design Engineering teams build and maintain Primer — this includes our CSS framework, style guide documentatio...

### 구현 노트

- 기존에 같은 역할의 컴포넌트가 있으면 토큰 교체부터 시작
- variant prop으로 시각적 변형을 관리 (하드코딩 금지)
- 애니메이션은 상태 설명용으로만 사용, 장식 효과 금지
- 텍스트 위계가 핵심 — 컬러보다 weight/size로 구분

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

- [calm+editorial] hover: opacity 변화 (0.08-0.12), elevation 변화 없음 + 텍스트 underline 또는 color shift, 장식적 효과 없음
- [calm+editorial] motion: 150-200ms ease-out, bounce/spring 없음 + 콘텐츠 전환 위주, UI chrome 모션 최소화
- [calm+editorial] color: 중성 톤 위주, accent는 최소한으로 + 타이포그래피로 위계 형성, 컬러보다 weight/size 활용

### 레퍼런스 근거

- **Carbon Design System**: AI chat is a conversational framework between a user and an AI that can aid in creating tasks, finding insights, tracking documents, and more. For ...
- **Primer**: The GitHub Design Infrastructure and Design Engineering teams build and maintain Primer — this includes our CSS framework, style guide documentatio...

### 구현 노트

- 기존에 같은 역할의 컴포넌트가 있으면 토큰 교체부터 시작
- variant prop으로 시각적 변형을 관리 (하드코딩 금지)
- 애니메이션은 상태 설명용으로만 사용, 장식 효과 금지
- 텍스트 위계가 핵심 — 컬러보다 weight/size로 구분

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

- [calm+editorial] hover: opacity 변화 (0.08-0.12), elevation 변화 없음 + 텍스트 underline 또는 color shift, 장식적 효과 없음
- [calm+editorial] motion: 150-200ms ease-out, bounce/spring 없음 + 콘텐츠 전환 위주, UI chrome 모션 최소화
- [calm+editorial] color: 중성 톤 위주, accent는 최소한으로 + 타이포그래피로 위계 형성, 컬러보다 weight/size 활용

### Visual Adaptation Hints

- **filter_nav_density**: filter/nav density는 balanced다. global nav와 local filter를 섞지 말고 계층별 간격 차이로 구조를 드러낸다. (source=navigation; confidence=0.94; provenance=inferred; direction=고정 sidebar 또는 split-pane navigation을 우선하고, 현재 위치와 scope를 항상 명시한다.; evidence=Split-pane workspace, layout=conversation-panel, density=airy)

### 레퍼런스 근거

- **Carbon Design System**: AI chat is a conversational framework between a user and an AI that can aid in creating tasks, finding insights, tracking documents, and more. For ...
- **Primer**: The GitHub Design Infrastructure and Design Engineering teams build and maintain Primer — this includes our CSS framework, style guide documentatio...

### 구현 노트

- 기존에 같은 역할의 컴포넌트가 있으면 토큰 교체부터 시작
- variant prop으로 시각적 변형을 관리 (하드코딩 금지)
- 애니메이션은 상태 설명용으로만 사용, 장식 효과 금지
- 텍스트 위계가 핵심 — 컬러보다 weight/size로 구분

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

- [calm+editorial] hover: opacity 변화 (0.08-0.12), elevation 변화 없음 + 텍스트 underline 또는 color shift, 장식적 효과 없음
- [calm+editorial] motion: 150-200ms ease-out, bounce/spring 없음 + 콘텐츠 전환 위주, UI chrome 모션 최소화
- [calm+editorial] color: 중성 톤 위주, accent는 최소한으로 + 타이포그래피로 위계 형성, 컬러보다 weight/size 활용

### Visual Adaptation Hints

- **cta_prominence**: CTA prominence는 medium이다. primary action은 분명하게 보이되 화면 전체를 지배하지 않게 유지한다. (source=cards; confidence=0.94; provenance=inferred; direction=low-elevation tinted cards를 기본으로 하고, 넓은 내부 여백과 강한 section breathing room. 중간 반경으로 제품 UI 절제 유지.; evidence=surface=tinted, density=airy, corner=medium, layout=conversation-panel)

### 레퍼런스 근거

- **Carbon Design System**: These components can toggle between the AI variant and the default variant depending on the user’s interaction. If the user manually overrides the ...
- **Primer**: I get so much joy from writing HTML and CSS, and design systems are one level up - systematically making UIs accessible and consistent. I love conc...

### 구현 노트

- 기존에 같은 역할의 컴포넌트가 있으면 토큰 교체부터 시작
- variant prop으로 시각적 변형을 관리 (하드코딩 금지)
- size prop: sm / md / lg (터치 영역은 항상 최소 44px 보장)
- 애니메이션은 상태 설명용으로만 사용, 장식 효과 금지
- 텍스트 위계가 핵심 — 컬러보다 weight/size로 구분
