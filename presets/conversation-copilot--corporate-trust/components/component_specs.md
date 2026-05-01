# Mercer Component Specs

총 182개 컴포넌트 | 패밀리: button, commerce, copilot-artifact, copilot-chat, data-display, document, editorial, feedback, input, layout, marketing, navigation, overlay, social, workflow

## 구현 원칙 (Non-negotiable)

이 스펙의 모든 컴포넌트를 구현할 때 반드시 지킨다:

1. **이모지를 UI로 쓰지 않는다** — 🎨 ✅ 🔥 ⚡ 🚀 ❌ ⭐ 📊 등 이모지를 아이콘, 상태 표시, 버튼 장식, 네비게이션 지표 자리에 절대 넣지 않는다. 아이콘 자리에는 SVG 컴포넌트 또는 Lucide/Heroicons/Phosphor/Tabler 라이브러리를 사용한다.
2. **컴포넌트를 직접 구현한다** — 아래 각 컴포넌트의 anatomy(구조), states(상태), 토큰 바인딩, 접근성 규칙을 그대로 따라 완전하게 구현한다. '임시', 'TODO', '플레이스홀더' 같은 반쪽 구현을 남기지 않는다.
3. **라이브러리 기본 스타일 금지** — 라이브러리 컴포넌트를 그대로 import해서 쓰지 않는다. 반드시 디자인 토큰(--color-*, --space-*, --radius-*, --font-*)으로 스타일을 명시적으로 바인딩한다.
4. **접근성은 옵션이 아니다** — 각 컴포넌트의 '접근성' 섹션에 정의된 role, aria-*, label, focus 관리 규칙을 전부 적용한다.
5. **hex 값 하드코딩 금지** — 색상은 반드시 semantic token을 경유한다 (예: `color: var(--color-ink)` not `color: #2C2C2C`).

## 브랜드 적용 규칙


## Visual-reference 적용 원칙

- anatomy / states / accessibility는 설계서(spec)와 KB 근거를 유지하고, visual adaptation은 elevation / framing / prominence / density 같은 표현 계층에만 advisory signal로 적용한다.
- Active visual signals: surface_style=tinted, density=airy, corner_style=round, top_layout_cue=conversation-panel
- Connected component hints: cards, data_display, navigation, panel, typography

---

## button / primary-button

**역할**: —

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

- 브랜드 기본 규칙을 따릅니다.

### Visual Adaptation Hints

- **cta_prominence**: CTA prominence는 medium이다. primary action은 분명하게 보이되 화면 전체를 지배하지 않게 유지한다. (source=cards; confidence=0.82; provenance=inferred; direction=low-elevation tinted cards를 기본으로 하고, 넓은 내부 여백과 강한 section breathing room. soft round corner를 기본값으로 유지.; evidence=surface=tinted, density=airy, corner=round, layout=conversation-panel)

### 레퍼런스 근거

- **Carbon Design System**: These components can toggle between the AI variant and the default variant depending on the user’s interaction. If the user manually overrides the ...
- **Primer**: I get so much joy from writing HTML and CSS, and design systems are one level up - systematically making UIs accessible and consistent. I love conc...

### 구현 노트

- 기존에 같은 역할의 컴포넌트가 있으면 토큰 교체부터 시작
- variant prop으로 시각적 변형을 관리 (하드코딩 금지)
- size prop: sm / md / lg (터치 영역은 항상 최소 44px 보장)

---

## button / secondary-button

**역할**: —

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

- 브랜드 기본 규칙을 따릅니다.

### Visual Adaptation Hints

- **cta_prominence**: CTA prominence는 medium이다. primary action은 분명하게 보이되 화면 전체를 지배하지 않게 유지한다. (source=cards; confidence=0.82; provenance=inferred; direction=low-elevation tinted cards를 기본으로 하고, 넓은 내부 여백과 강한 section breathing room. soft round corner를 기본값으로 유지.; evidence=surface=tinted, density=airy, corner=round, layout=conversation-panel)

### 레퍼런스 근거

- **Carbon Design System**: These components can toggle between the AI variant and the default variant depending on the user’s interaction. If the user manually overrides the ...
- **Primer**: I get so much joy from writing HTML and CSS, and design systems are one level up - systematically making UIs accessible and consistent. I love conc...

### 구현 노트

- 기존에 같은 역할의 컴포넌트가 있으면 토큰 교체부터 시작
- variant prop으로 시각적 변형을 관리 (하드코딩 금지)
- size prop: sm / md / lg (터치 영역은 항상 최소 44px 보장)

---

## button / ghost-button

**역할**: —

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

- 브랜드 기본 규칙을 따릅니다.

### Visual Adaptation Hints

- **cta_prominence**: CTA prominence는 medium이다. primary action은 분명하게 보이되 화면 전체를 지배하지 않게 유지한다. (source=cards; confidence=0.82; provenance=inferred; direction=low-elevation tinted cards를 기본으로 하고, 넓은 내부 여백과 강한 section breathing room. soft round corner를 기본값으로 유지.; evidence=surface=tinted, density=airy, corner=round, layout=conversation-panel)

### 레퍼런스 근거

- **Carbon Design System**: These components can toggle between the AI variant and the default variant depending on the user’s interaction. If the user manually overrides the ...
- **Primer**: I get so much joy from writing HTML and CSS, and design systems are one level up - systematically making UIs accessible and consistent. I love conc...

### 구현 노트

- 기존에 같은 역할의 컴포넌트가 있으면 토큰 교체부터 시작
- variant prop으로 시각적 변형을 관리 (하드코딩 금지)
- size prop: sm / md / lg (터치 영역은 항상 최소 44px 보장)

---

## button / icon-button

**역할**: —

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

- 브랜드 기본 규칙을 따릅니다.

### Visual Adaptation Hints

- **cta_prominence**: CTA prominence는 medium이다. primary action은 분명하게 보이되 화면 전체를 지배하지 않게 유지한다. (source=cards; confidence=0.82; provenance=inferred; direction=low-elevation tinted cards를 기본으로 하고, 넓은 내부 여백과 강한 section breathing room. soft round corner를 기본값으로 유지.; evidence=surface=tinted, density=airy, corner=round, layout=conversation-panel)

### 레퍼런스 근거

- **Carbon Design System**: These components can toggle between the AI variant and the default variant depending on the user’s interaction. If the user manually overrides the ...
- **Primer**: I get so much joy from writing HTML and CSS, and design systems are one level up - systematically making UIs accessible and consistent. I love conc...

### 구현 노트

- 기존에 같은 역할의 컴포넌트가 있으면 토큰 교체부터 시작
- variant prop으로 시각적 변형을 관리 (하드코딩 금지)
- size prop: sm / md / lg (터치 영역은 항상 최소 44px 보장)

---

## button / cta-button

**역할**: —

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

- 브랜드 기본 규칙을 따릅니다.

### Visual Adaptation Hints

- **cta_prominence**: CTA prominence는 strong이다. 섹션당 primary CTA 1개만 fill/accent로 강하게 띄우고 secondary는 조용하게 후퇴시킨다. (source=cards; confidence=0.82; provenance=inferred; direction=low-elevation tinted cards를 기본으로 하고, 넓은 내부 여백과 강한 section breathing room. soft round corner를 기본값으로 유지.; evidence=surface=tinted, density=airy, corner=round, layout=conversation-panel)

### 레퍼런스 근거

- **Carbon Design System**: These components can toggle between the AI variant and the default variant depending on the user’s interaction. If the user manually overrides the ...
- **Primer**: I get so much joy from writing HTML and CSS, and design systems are one level up - systematically making UIs accessible and consistent. I love conc...

### 구현 노트

- 기존에 같은 역할의 컴포넌트가 있으면 토큰 교체부터 시작
- variant prop으로 시각적 변형을 관리 (하드코딩 금지)
- size prop: sm / md / lg (터치 영역은 항상 최소 44px 보장)

---

## navigation / mobile-topbar

**역할**: —

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

- 브랜드 기본 규칙을 따릅니다.

### Visual Adaptation Hints

- **filter_nav_density**: filter/nav density는 balanced다. global nav와 local filter를 섞지 말고 계층별 간격 차이로 구조를 드러낸다. (source=navigation; confidence=0.94; provenance=inferred; direction=고정 sidebar 또는 split-pane navigation을 우선하고, 현재 위치와 scope를 항상 명시한다.; evidence=Split-pane workspace, layout=conversation-panel, density=airy)

### 레퍼런스 근거

- **Carbon Design System**: Library menu navigation There are two kinds of symbols — library symbols and document symbols. Library symbols are available in any Sketch document...
- **Primer**: Octicon nav items navigation 12 px

### 구현 노트

- 기존에 같은 역할의 컴포넌트가 있으면 토큰 교체부터 시작
- variant prop으로 시각적 변형을 관리 (하드코딩 금지)
- active 상태는 URL/라우터와 자동 동기화

---

## navigation / mobile-tab-bar

**역할**: —

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

- 브랜드 기본 규칙을 따릅니다.

### Visual Adaptation Hints

- **filter_nav_density**: filter/nav density는 balanced다. global nav와 local filter를 섞지 말고 계층별 간격 차이로 구조를 드러낸다. (source=navigation; confidence=0.94; provenance=inferred; direction=고정 sidebar 또는 split-pane navigation을 우선하고, 현재 위치와 scope를 항상 명시한다.; evidence=Split-pane workspace, layout=conversation-panel, density=airy)

### 레퍼런스 근거

- **Carbon Design System**: Library menu navigation There are two kinds of symbols — library symbols and document symbols. Library symbols are available in any Sketch document...
- **Primer**: Octicon nav items navigation 12 px

### 구현 노트

- 기존에 같은 역할의 컴포넌트가 있으면 토큰 교체부터 시작
- variant prop으로 시각적 변형을 관리 (하드코딩 금지)
- active 상태는 URL/라우터와 자동 동기화

---

## navigation / back-button

**역할**: —

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

- 브랜드 기본 규칙을 따릅니다.

### Visual Adaptation Hints

- **cta_prominence**: CTA prominence는 medium이다. primary action은 분명하게 보이되 화면 전체를 지배하지 않게 유지한다. (source=cards; confidence=0.82; provenance=inferred; direction=low-elevation tinted cards를 기본으로 하고, 넓은 내부 여백과 강한 section breathing room. soft round corner를 기본값으로 유지.; evidence=surface=tinted, density=airy, corner=round, layout=conversation-panel)
- **filter_nav_density**: filter/nav density는 balanced다. global nav와 local filter를 섞지 말고 계층별 간격 차이로 구조를 드러낸다. (source=navigation; confidence=0.94; provenance=inferred; direction=고정 sidebar 또는 split-pane navigation을 우선하고, 현재 위치와 scope를 항상 명시한다.; evidence=Split-pane workspace, layout=conversation-panel, density=airy)

### 레퍼런스 근거

- **Carbon Design System**: Library menu navigation There are two kinds of symbols — library symbols and document symbols. Library symbols are available in any Sketch document...
- **Primer**: Octicon nav items navigation 12 px

### 구현 노트

- 기존에 같은 역할의 컴포넌트가 있으면 토큰 교체부터 시작
- variant prop으로 시각적 변형을 관리 (하드코딩 금지)
- active 상태는 URL/라우터와 자동 동기화

---

## navigation / section-tabs

**역할**: —

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

- 브랜드 기본 규칙을 따릅니다.

### Visual Adaptation Hints

- **filter_nav_density**: filter/nav density는 balanced다. global nav와 local filter를 섞지 말고 계층별 간격 차이로 구조를 드러낸다. (source=navigation; confidence=0.94; provenance=inferred; direction=고정 sidebar 또는 split-pane navigation을 우선하고, 현재 위치와 scope를 항상 명시한다.; evidence=Split-pane workspace, layout=conversation-panel, density=airy)

### 레퍼런스 근거

- **Carbon Design System**: Library menu navigation There are two kinds of symbols — library symbols and document symbols. Library symbols are available in any Sketch document...
- **Primer**: Octicon nav items navigation 12 px

### 구현 노트

- 기존에 같은 역할의 컴포넌트가 있으면 토큰 교체부터 시작
- variant prop으로 시각적 변형을 관리 (하드코딩 금지)
- active 상태는 URL/라우터와 자동 동기화

---

## feedback / inline-alert

**역할**: —

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

- 브랜드 기본 규칙을 따릅니다.

### 레퍼런스 근거

- **Carbon Design System**: We welcome all feedback, designs, or ideas in order to produce the best possible experience for our users. If you're interested in contributing, ch...
- **Primer**: Messaging components are used to provide important and relevant information to the user, including feedback, contextual information, product update...

### 구현 노트

- 기존에 같은 역할의 컴포넌트가 있으면 토큰 교체부터 시작
- variant prop으로 시각적 변형을 관리 (하드코딩 금지)
- auto-dismiss 시간은 내용 길이에 비례 (기본 5초)

---

## feedback / empty-state

**역할**: —

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

- 브랜드 기본 규칙을 따릅니다.

### Visual Adaptation Hints

- **card_elevation_tendency**: 카드는 낮은 elevation만 허용하고 색면 차이로 그룹을 구분한다. 내부 여백은 넉넉하게 두고 card breathing room을 확보한다. (source=cards; confidence=0.82; provenance=inferred; direction=low-elevation tinted cards를 기본으로 하고, 넓은 내부 여백과 강한 section breathing room. soft round corner를 기본값으로 유지.; evidence=surface=tinted, density=airy, corner=round)
- **border_vs_fill_emphasis**: fill 중심이다. tint surface로 성격을 만들고 border는 아주 얇게 보조한다. (source=cards; confidence=0.82; provenance=inferred; direction=low-elevation tinted cards를 기본으로 하고, 넓은 내부 여백과 강한 section breathing room. soft round corner를 기본값으로 유지.; evidence=surface=tinted, density=airy, corner=round)
- **chart_panel_framing**: 차트 패널은 soft tint frame과 restrained divider로 프레이밍한다. 헤더 메타데이터와 본문 visualization 사이의 breathing room을 충분히 둔다. (source=data_display; confidence=0.82; provenance=inferred; direction=정보 밀도를 유지하되 thin dividers와 restrained accent로 hierarchy를 만든다.; evidence=layout=data-review-surface, density=airy, layout=conversation-panel, surface=tinted)

### 레퍼런스 근거

- **Carbon Design System**: We welcome all feedback, designs, or ideas in order to produce the best possible experience for our users. If you're interested in contributing, ch...
- **Primer**: Empty states Empty states are used to fill spaces when no content has been added yet, or is temporarily empty due to the nature of the feature.

### 구현 노트

- 기존에 같은 역할의 컴포넌트가 있으면 토큰 교체부터 시작
- variant prop으로 시각적 변형을 관리 (하드코딩 금지)
- auto-dismiss 시간은 내용 길이에 비례 (기본 5초)

---

## feedback / toast

**역할**: —

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

- 브랜드 기본 규칙을 따릅니다.

### 레퍼런스 근거

- **Carbon Design System**: We welcome all feedback, designs, or ideas in order to produce the best possible experience for our users. If you're interested in contributing, ch...
- **Primer**: Messaging components are used to provide important and relevant information to the user, including feedback, contextual information, product update...

### 구현 노트

- 기존에 같은 역할의 컴포넌트가 있으면 토큰 교체부터 시작
- variant prop으로 시각적 변형을 관리 (하드코딩 금지)
- auto-dismiss 시간은 내용 길이에 비례 (기본 5초)

---

## overlay / bottom-sheet

**역할**: —

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

- 브랜드 기본 규칙을 따릅니다.

### 레퍼런스 근거

- **Primer**: ActionMenu is composed of ActionList and Overlay patterns used for quick actions and selections. AnchoredOverlay

### 구현 노트

- 기존에 같은 역할의 컴포넌트가 있으면 토큰 교체부터 시작
- variant prop으로 시각적 변형을 관리 (하드코딩 금지)
- Escape / backdrop click으로 닫기, 열 때 첫 focusable 요소로 이동

---

## overlay / modal-dialog

**역할**: —

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

- 브랜드 기본 규칙을 따릅니다.

### 레퍼런스 근거

- **Primer**: ActionMenu is composed of ActionList and Overlay patterns used for quick actions and selections. AnchoredOverlay

### 구현 노트

- 기존에 같은 역할의 컴포넌트가 있으면 토큰 교체부터 시작
- variant prop으로 시각적 변형을 관리 (하드코딩 금지)
- Escape / backdrop click으로 닫기, 열 때 첫 focusable 요소로 이동

---

## input / text-field

**역할**: —

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

- 브랜드 기본 규칙을 따릅니다.

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

**역할**: —

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

- 브랜드 기본 규칙을 따릅니다.

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

---

## input / segmented-control

**역할**: —

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

- 브랜드 기본 규칙을 따릅니다.

### 레퍼런스 근거

- **Carbon Design System**: Number input Text input
- **Primer**: I worked in data visualization and map-making for most of my career, and solving design problems with data is my jam. To me there's something uniqu...

### 구현 노트

- 기존에 같은 역할의 컴포넌트가 있으면 토큰 교체부터 시작
- variant prop으로 시각적 변형을 관리 (하드코딩 금지)
- error 상태에서 helper text → error message로 자동 전환
- label은 항상 visible (placeholder만으로 대체 금지)

---

## button / link-button

**역할**: —

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

- 브랜드 기본 규칙을 따릅니다.

### Visual Adaptation Hints

- **cta_prominence**: CTA prominence는 medium이다. primary action은 분명하게 보이되 화면 전체를 지배하지 않게 유지한다. (source=cards; confidence=0.82; provenance=inferred; direction=low-elevation tinted cards를 기본으로 하고, 넓은 내부 여백과 강한 section breathing room. soft round corner를 기본값으로 유지.; evidence=surface=tinted, density=airy, corner=round, layout=conversation-panel)

### 레퍼런스 근거

- **Carbon Design System**: These components can toggle between the AI variant and the default variant depending on the user’s interaction. If the user manually overrides the ...
- **Primer**: I get so much joy from writing HTML and CSS, and design systems are one level up - systematically making UIs accessible and consistent. I love conc...

### 구현 노트

- 기존에 같은 역할의 컴포넌트가 있으면 토큰 교체부터 시작
- variant prop으로 시각적 변형을 관리 (하드코딩 금지)
- size prop: sm / md / lg (터치 영역은 항상 최소 44px 보장)

---

## data-display / chat-message

**역할**: —

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

- 브랜드 기본 규칙을 따릅니다.

### Visual Adaptation Hints

- **card_elevation_tendency**: 카드는 낮은 elevation만 허용하고 색면 차이로 그룹을 구분한다. 내부 여백은 넉넉하게 두고 card breathing room을 확보한다. (source=cards; confidence=0.82; provenance=inferred; direction=low-elevation tinted cards를 기본으로 하고, 넓은 내부 여백과 강한 section breathing room. soft round corner를 기본값으로 유지.; evidence=surface=tinted, density=airy, corner=round)
- **border_vs_fill_emphasis**: fill 중심이다. tint surface로 성격을 만들고 border는 아주 얇게 보조한다. (source=cards; confidence=0.82; provenance=inferred; direction=low-elevation tinted cards를 기본으로 하고, 넓은 내부 여백과 강한 section breathing room. soft round corner를 기본값으로 유지.; evidence=surface=tinted, density=airy, corner=round)
- **chart_panel_framing**: 차트 패널은 soft tint frame과 restrained divider로 프레이밍한다. 헤더 메타데이터와 본문 visualization 사이의 breathing room을 충분히 둔다. (source=data_display; confidence=0.82; provenance=inferred; direction=정보 밀도를 유지하되 thin dividers와 restrained accent로 hierarchy를 만든다.; evidence=layout=data-review-surface, density=airy, layout=conversation-panel, surface=tinted)

### 구현 노트

- 기존에 같은 역할의 컴포넌트가 있으면 토큰 교체부터 시작
- variant prop으로 시각적 변형을 관리 (하드코딩 금지)
- 빈 상태(empty-state)와 에러 상태를 반드시 처리

---

## input / chat-input

**역할**: —

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

- 브랜드 기본 규칙을 따릅니다.

### 레퍼런스 근거

- **Carbon Design System**: Number input Text input
- **Primer**: I worked in data visualization and map-making for most of my career, and solving design problems with data is my jam. To me there's something uniqu...

### 구현 노트

- 기존에 같은 역할의 컴포넌트가 있으면 토큰 교체부터 시작
- variant prop으로 시각적 변형을 관리 (하드코딩 금지)
- error 상태에서 helper text → error message로 자동 전환
- label은 항상 visible (placeholder만으로 대체 금지)

---

## data-display / chat-thread

**역할**: —

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

- 브랜드 기본 규칙을 따릅니다.

### Visual Adaptation Hints

- **card_elevation_tendency**: 카드는 낮은 elevation만 허용하고 색면 차이로 그룹을 구분한다. 내부 여백은 넉넉하게 두고 card breathing room을 확보한다. (source=cards; confidence=0.82; provenance=inferred; direction=low-elevation tinted cards를 기본으로 하고, 넓은 내부 여백과 강한 section breathing room. soft round corner를 기본값으로 유지.; evidence=surface=tinted, density=airy, corner=round)
- **border_vs_fill_emphasis**: fill 중심이다. tint surface로 성격을 만들고 border는 아주 얇게 보조한다. (source=cards; confidence=0.82; provenance=inferred; direction=low-elevation tinted cards를 기본으로 하고, 넓은 내부 여백과 강한 section breathing room. soft round corner를 기본값으로 유지.; evidence=surface=tinted, density=airy, corner=round)
- **chart_panel_framing**: 차트 패널은 soft tint frame과 restrained divider로 프레이밍한다. 헤더 메타데이터와 본문 visualization 사이의 breathing room을 충분히 둔다. (source=data_display; confidence=0.82; provenance=inferred; direction=정보 밀도를 유지하되 thin dividers와 restrained accent로 hierarchy를 만든다.; evidence=layout=data-review-surface, density=airy, layout=conversation-panel, surface=tinted)

### 구현 노트

- 기존에 같은 역할의 컴포넌트가 있으면 토큰 교체부터 시작
- variant prop으로 시각적 변형을 관리 (하드코딩 금지)
- 빈 상태(empty-state)와 에러 상태를 반드시 처리

---

## data-display / comment-thread

**역할**: —

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

- 브랜드 기본 규칙을 따릅니다.

### Visual Adaptation Hints

- **card_elevation_tendency**: 카드는 낮은 elevation만 허용하고 색면 차이로 그룹을 구분한다. 내부 여백은 넉넉하게 두고 card breathing room을 확보한다. (source=cards; confidence=0.82; provenance=inferred; direction=low-elevation tinted cards를 기본으로 하고, 넓은 내부 여백과 강한 section breathing room. soft round corner를 기본값으로 유지.; evidence=surface=tinted, density=airy, corner=round)
- **border_vs_fill_emphasis**: fill 중심이다. tint surface로 성격을 만들고 border는 아주 얇게 보조한다. (source=cards; confidence=0.82; provenance=inferred; direction=low-elevation tinted cards를 기본으로 하고, 넓은 내부 여백과 강한 section breathing room. soft round corner를 기본값으로 유지.; evidence=surface=tinted, density=airy, corner=round)
- **chart_panel_framing**: 차트 패널은 soft tint frame과 restrained divider로 프레이밍한다. 헤더 메타데이터와 본문 visualization 사이의 breathing room을 충분히 둔다. (source=data_display; confidence=0.82; provenance=inferred; direction=정보 밀도를 유지하되 thin dividers와 restrained accent로 hierarchy를 만든다.; evidence=layout=data-review-surface, density=airy, layout=conversation-panel, surface=tinted)

### 구현 노트

- 기존에 같은 역할의 컴포넌트가 있으면 토큰 교체부터 시작
- variant prop으로 시각적 변형을 관리 (하드코딩 금지)
- 빈 상태(empty-state)와 에러 상태를 반드시 처리

---

## input / comment-input

**역할**: —

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

- 브랜드 기본 규칙을 따릅니다.

### 레퍼런스 근거

- **Carbon Design System**: Number input Text input
- **Primer**: I worked in data visualization and map-making for most of my career, and solving design problems with data is my jam. To me there's something uniqu...

### 구현 노트

- 기존에 같은 역할의 컴포넌트가 있으면 토큰 교체부터 시작
- variant prop으로 시각적 변형을 관리 (하드코딩 금지)
- error 상태에서 helper text → error message로 자동 전환
- label은 항상 visible (placeholder만으로 대체 금지)

---

## overlay / mention-popup

**역할**: —

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

- 브랜드 기본 규칙을 따릅니다.

### 레퍼런스 근거

- **Primer**: ActionMenu is composed of ActionList and Overlay patterns used for quick actions and selections. AnchoredOverlay

### 구현 노트

- 기존에 같은 역할의 컴포넌트가 있으면 토큰 교체부터 시작
- variant prop으로 시각적 변형을 관리 (하드코딩 금지)
- Escape / backdrop click으로 닫기, 열 때 첫 focusable 요소로 이동

---

## navigation / app-shell

**역할**: —

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

- 브랜드 기본 규칙을 따릅니다.

### Visual Adaptation Hints

- **filter_nav_density**: filter/nav density는 balanced다. global nav와 local filter를 섞지 말고 계층별 간격 차이로 구조를 드러낸다. (source=navigation; confidence=0.94; provenance=inferred; direction=고정 sidebar 또는 split-pane navigation을 우선하고, 현재 위치와 scope를 항상 명시한다.; evidence=Split-pane workspace, layout=conversation-panel, density=airy)

### 레퍼런스 근거

- **Carbon Design System**: Library menu navigation There are two kinds of symbols — library symbols and document symbols. Library symbols are available in any Sketch document...
- **Primer**: Octicon nav items navigation 12 px

### 구현 노트

- 기존에 같은 역할의 컴포넌트가 있으면 토큰 교체부터 시작
- variant prop으로 시각적 변형을 관리 (하드코딩 금지)
- active 상태는 URL/라우터와 자동 동기화

---

## navigation / sidebar-nav

**역할**: —

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

- 브랜드 기본 규칙을 따릅니다.

### Visual Adaptation Hints

- **filter_nav_density**: filter/nav density는 balanced다. global nav와 local filter를 섞지 말고 계층별 간격 차이로 구조를 드러낸다. (source=navigation; confidence=0.94; provenance=inferred; direction=고정 sidebar 또는 split-pane navigation을 우선하고, 현재 위치와 scope를 항상 명시한다.; evidence=Split-pane workspace, layout=conversation-panel, density=airy)

### 레퍼런스 근거

- **Carbon Design System**: Total panel width (“sidebar nav”) + Left outside margin + Right outside margin = Total margins Artboard width - Total margins = Total width
- **Primer**: Octicon nav items navigation 12 px

### 구현 노트

- 기존에 같은 역할의 컴포넌트가 있으면 토큰 교체부터 시작
- variant prop으로 시각적 변형을 관리 (하드코딩 금지)
- active 상태는 URL/라우터와 자동 동기화

---

## navigation / topbar

**역할**: —

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

- 브랜드 기본 규칙을 따릅니다.

### Visual Adaptation Hints

- **filter_nav_density**: filter/nav density는 balanced다. global nav와 local filter를 섞지 말고 계층별 간격 차이로 구조를 드러낸다. (source=navigation; confidence=0.94; provenance=inferred; direction=고정 sidebar 또는 split-pane navigation을 우선하고, 현재 위치와 scope를 항상 명시한다.; evidence=Split-pane workspace, layout=conversation-panel, density=airy)

### 레퍼런스 근거

- **Carbon Design System**: Library menu navigation There are two kinds of symbols — library symbols and document symbols. Library symbols are available in any Sketch document...
- **Primer**: Octicon nav items navigation 12 px

### 구현 노트

- 기존에 같은 역할의 컴포넌트가 있으면 토큰 교체부터 시작
- variant prop으로 시각적 변형을 관리 (하드코딩 금지)
- active 상태는 URL/라우터와 자동 동기화

---

## navigation / breadcrumb

**역할**: —

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

- 브랜드 기본 규칙을 따릅니다.

### Visual Adaptation Hints

- **filter_nav_density**: filter/nav density는 balanced다. global nav와 local filter를 섞지 말고 계층별 간격 차이로 구조를 드러낸다. (source=navigation; confidence=0.94; provenance=inferred; direction=고정 sidebar 또는 split-pane navigation을 우선하고, 현재 위치와 scope를 항상 명시한다.; evidence=Split-pane workspace, layout=conversation-panel, density=airy)

### 레퍼런스 근거

- **Carbon Design System**: Library menu navigation There are two kinds of symbols — library symbols and document symbols. Library symbols are available in any Sketch document...
- **Primer**: Octicon nav items navigation 12 px

### 구현 노트

- 기존에 같은 역할의 컴포넌트가 있으면 토큰 교체부터 시작
- variant prop으로 시각적 변형을 관리 (하드코딩 금지)
- active 상태는 URL/라우터와 자동 동기화

---

## navigation / tab-bar

**역할**: —

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

- 브랜드 기본 규칙을 따릅니다.

### Visual Adaptation Hints

- **filter_nav_density**: filter/nav density는 balanced다. global nav와 local filter를 섞지 말고 계층별 간격 차이로 구조를 드러낸다. (source=navigation; confidence=0.94; provenance=inferred; direction=고정 sidebar 또는 split-pane navigation을 우선하고, 현재 위치와 scope를 항상 명시한다.; evidence=Split-pane workspace, layout=conversation-panel, density=airy)

### 레퍼런스 근거

- **Carbon Design System**: Library menu navigation There are two kinds of symbols — library symbols and document symbols. Library symbols are available in any Sketch document...
- **Primer**: Octicon nav items navigation 12 px

### 구현 노트

- 기존에 같은 역할의 컴포넌트가 있으면 토큰 교체부터 시작
- variant prop으로 시각적 변형을 관리 (하드코딩 금지)
- active 상태는 URL/라우터와 자동 동기화

---

## data-display / tag

**역할**: —

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

- 브랜드 기본 규칙을 따릅니다.

### Visual Adaptation Hints

- **card_elevation_tendency**: 카드는 낮은 elevation만 허용하고 색면 차이로 그룹을 구분한다. 내부 여백은 넉넉하게 두고 card breathing room을 확보한다. (source=cards; confidence=0.82; provenance=inferred; direction=low-elevation tinted cards를 기본으로 하고, 넓은 내부 여백과 강한 section breathing room. soft round corner를 기본값으로 유지.; evidence=surface=tinted, density=airy, corner=round)
- **border_vs_fill_emphasis**: fill 중심이다. tint surface로 성격을 만들고 border는 아주 얇게 보조한다. (source=cards; confidence=0.82; provenance=inferred; direction=low-elevation tinted cards를 기본으로 하고, 넓은 내부 여백과 강한 section breathing room. soft round corner를 기본값으로 유지.; evidence=surface=tinted, density=airy, corner=round)
- **chart_panel_framing**: 차트 패널은 soft tint frame과 restrained divider로 프레이밍한다. 헤더 메타데이터와 본문 visualization 사이의 breathing room을 충분히 둔다. (source=data_display; confidence=0.82; provenance=inferred; direction=정보 밀도를 유지하되 thin dividers와 restrained accent로 hierarchy를 만든다.; evidence=layout=data-review-surface, density=airy, layout=conversation-panel, surface=tinted)

### 레퍼런스 근거

- **Carbon Design System**: Tag Date picker
- **Primer**: Primer color design tokens are made available within data-attribute selectors on the body tag or other high level dom element. There are three dist...

### 구현 노트

- 기존에 같은 역할의 컴포넌트가 있으면 토큰 교체부터 시작
- variant prop으로 시각적 변형을 관리 (하드코딩 금지)
- 빈 상태(empty-state)와 에러 상태를 반드시 처리

---

## feedback / status-badge

**역할**: —

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

- 브랜드 기본 규칙을 따릅니다.

### Visual Adaptation Hints

- **card_elevation_tendency**: 카드는 낮은 elevation만 허용하고 색면 차이로 그룹을 구분한다. 내부 여백은 넉넉하게 두고 card breathing room을 확보한다. (source=cards; confidence=0.82; provenance=inferred; direction=low-elevation tinted cards를 기본으로 하고, 넓은 내부 여백과 강한 section breathing room. soft round corner를 기본값으로 유지.; evidence=surface=tinted, density=airy, corner=round)
- **border_vs_fill_emphasis**: fill 중심이다. tint surface로 성격을 만들고 border는 아주 얇게 보조한다. (source=cards; confidence=0.82; provenance=inferred; direction=low-elevation tinted cards를 기본으로 하고, 넓은 내부 여백과 강한 section breathing room. soft round corner를 기본값으로 유지.; evidence=surface=tinted, density=airy, corner=round)
- **chart_panel_framing**: 차트 패널은 soft tint frame과 restrained divider로 프레이밍한다. 헤더 메타데이터와 본문 visualization 사이의 breathing room을 충분히 둔다. (source=data_display; confidence=0.82; provenance=inferred; direction=정보 밀도를 유지하되 thin dividers와 restrained accent로 hierarchy를 만든다.; evidence=layout=data-review-surface, density=airy, layout=conversation-panel, surface=tinted)

### 레퍼런스 근거

- **Carbon Design System**: We welcome all feedback, designs, or ideas in order to produce the best possible experience for our users. If you're interested in contributing, ch...
- **Primer**: Messaging components are used to provide important and relevant information to the user, including feedback, contextual information, product update...

### 구현 노트

- 기존에 같은 역할의 컴포넌트가 있으면 토큰 교체부터 시작
- variant prop으로 시각적 변형을 관리 (하드코딩 금지)
- auto-dismiss 시간은 내용 길이에 비례 (기본 5초)

---

## input / chip

**역할**: —

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

- 브랜드 기본 규칙을 따릅니다.

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

---

## input / prompt-composer

**역할**: —

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

- 브랜드 기본 규칙을 따릅니다.

### 레퍼런스 근거

- **Carbon Design System**: Number input Text input
- **Primer**: I worked in data visualization and map-making for most of my career, and solving design problems with data is my jam. To me there's something uniqu...

### 구현 노트

- 기존에 같은 역할의 컴포넌트가 있으면 토큰 교체부터 시작
- variant prop으로 시각적 변형을 관리 (하드코딩 금지)
- error 상태에서 helper text → error message로 자동 전환
- label은 항상 visible (placeholder만으로 대체 금지)

---

## copilot-chat / streaming-cursor

**역할**: —

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

- 브랜드 기본 규칙을 따릅니다.

### 구현 노트

- 기존에 같은 역할의 컴포넌트가 있으면 토큰 교체부터 시작
- variant prop으로 시각적 변형을 관리 (하드코딩 금지)

---

## copilot-chat / typing-indicator

**역할**: —

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

- 브랜드 기본 규칙을 따릅니다.

### 구현 노트

- 기존에 같은 역할의 컴포넌트가 있으면 토큰 교체부터 시작
- variant prop으로 시각적 변형을 관리 (하드코딩 금지)

---

## copilot-chat / inline-citation

**역할**: —

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

- 브랜드 기본 규칙을 따릅니다.

### 구현 노트

- 기존에 같은 역할의 컴포넌트가 있으면 토큰 교체부터 시작
- variant prop으로 시각적 변형을 관리 (하드코딩 금지)

---

## button / regenerate-button

**역할**: —

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

- 브랜드 기본 규칙을 따릅니다.

### Visual Adaptation Hints

- **cta_prominence**: CTA prominence는 medium이다. primary action은 분명하게 보이되 화면 전체를 지배하지 않게 유지한다. (source=cards; confidence=0.82; provenance=inferred; direction=low-elevation tinted cards를 기본으로 하고, 넓은 내부 여백과 강한 section breathing room. soft round corner를 기본값으로 유지.; evidence=surface=tinted, density=airy, corner=round, layout=conversation-panel)

### 레퍼런스 근거

- **Carbon Design System**: These components can toggle between the AI variant and the default variant depending on the user’s interaction. If the user manually overrides the ...
- **Primer**: I get so much joy from writing HTML and CSS, and design systems are one level up - systematically making UIs accessible and consistent. I love conc...

### 구현 노트

- 기존에 같은 역할의 컴포넌트가 있으면 토큰 교체부터 시작
- variant prop으로 시각적 변형을 관리 (하드코딩 금지)
- size prop: sm / md / lg (터치 영역은 항상 최소 44px 보장)

---

## button / stop-generation-button

**역할**: —

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

- 브랜드 기본 규칙을 따릅니다.

### Visual Adaptation Hints

- **cta_prominence**: CTA prominence는 medium이다. primary action은 분명하게 보이되 화면 전체를 지배하지 않게 유지한다. (source=cards; confidence=0.82; provenance=inferred; direction=low-elevation tinted cards를 기본으로 하고, 넓은 내부 여백과 강한 section breathing room. soft round corner를 기본값으로 유지.; evidence=surface=tinted, density=airy, corner=round, layout=conversation-panel)

### 레퍼런스 근거

- **Carbon Design System**: These components can toggle between the AI variant and the default variant depending on the user’s interaction. If the user manually overrides the ...
- **Primer**: I get so much joy from writing HTML and CSS, and design systems are one level up - systematically making UIs accessible and consistent. I love conc...

### 구현 노트

- 기존에 같은 역할의 컴포넌트가 있으면 토큰 교체부터 시작
- variant prop으로 시각적 변형을 관리 (하드코딩 금지)
- size prop: sm / md / lg (터치 영역은 항상 최소 44px 보장)

---

## copilot-chat / mention-chip

**역할**: —

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

- 브랜드 기본 규칙을 따릅니다.

### Visual Adaptation Hints

- **filter_nav_density**: filter/nav density는 balanced다. global nav와 local filter를 섞지 말고 계층별 간격 차이로 구조를 드러낸다. (source=navigation; confidence=0.94; provenance=inferred; direction=고정 sidebar 또는 split-pane navigation을 우선하고, 현재 위치와 scope를 항상 명시한다.; evidence=Split-pane workspace, layout=conversation-panel, density=airy)

### 구현 노트

- 기존에 같은 역할의 컴포넌트가 있으면 토큰 교체부터 시작
- variant prop으로 시각적 변형을 관리 (하드코딩 금지)

---

## copilot-chat / suggestion-card

**역할**: —

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

- 브랜드 기본 규칙을 따릅니다.

### Visual Adaptation Hints

- **card_elevation_tendency**: 카드는 낮은 elevation만 허용하고 색면 차이로 그룹을 구분한다. 내부 여백은 넉넉하게 두고 card breathing room을 확보한다. (source=cards; confidence=0.82; provenance=inferred; direction=low-elevation tinted cards를 기본으로 하고, 넓은 내부 여백과 강한 section breathing room. soft round corner를 기본값으로 유지.; evidence=surface=tinted, density=airy, corner=round)
- **border_vs_fill_emphasis**: fill 중심이다. tint surface로 성격을 만들고 border는 아주 얇게 보조한다. (source=cards; confidence=0.82; provenance=inferred; direction=low-elevation tinted cards를 기본으로 하고, 넓은 내부 여백과 강한 section breathing room. soft round corner를 기본값으로 유지.; evidence=surface=tinted, density=airy, corner=round)

### 구현 노트

- 기존에 같은 역할의 컴포넌트가 있으면 토큰 교체부터 시작
- variant prop으로 시각적 변형을 관리 (하드코딩 금지)

---

## copilot-chat / thread-header

**역할**: —

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

- 브랜드 기본 규칙을 따릅니다.

### 구현 노트

- 기존에 같은 역할의 컴포넌트가 있으면 토큰 교체부터 시작
- variant prop으로 시각적 변형을 관리 (하드코딩 금지)

---

## button / new-thread-button

**역할**: —

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

- 브랜드 기본 규칙을 따릅니다.

### Visual Adaptation Hints

- **cta_prominence**: CTA prominence는 medium이다. primary action은 분명하게 보이되 화면 전체를 지배하지 않게 유지한다. (source=cards; confidence=0.82; provenance=inferred; direction=low-elevation tinted cards를 기본으로 하고, 넓은 내부 여백과 강한 section breathing room. soft round corner를 기본값으로 유지.; evidence=surface=tinted, density=airy, corner=round, layout=conversation-panel)

### 레퍼런스 근거

- **Carbon Design System**: These components can toggle between the AI variant and the default variant depending on the user’s interaction. If the user manually overrides the ...
- **Primer**: I get so much joy from writing HTML and CSS, and design systems are one level up - systematically making UIs accessible and consistent. I love conc...

### 구현 노트

- 기존에 같은 역할의 컴포넌트가 있으면 토큰 교체부터 시작
- variant prop으로 시각적 변형을 관리 (하드코딩 금지)
- size prop: sm / md / lg (터치 영역은 항상 최소 44px 보장)

---

## feedback / empty-conversation-state

**역할**: —

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

- 브랜드 기본 규칙을 따릅니다.

### Visual Adaptation Hints

- **card_elevation_tendency**: 카드는 낮은 elevation만 허용하고 색면 차이로 그룹을 구분한다. 내부 여백은 넉넉하게 두고 card breathing room을 확보한다. (source=cards; confidence=0.82; provenance=inferred; direction=low-elevation tinted cards를 기본으로 하고, 넓은 내부 여백과 강한 section breathing room. soft round corner를 기본값으로 유지.; evidence=surface=tinted, density=airy, corner=round)
- **border_vs_fill_emphasis**: fill 중심이다. tint surface로 성격을 만들고 border는 아주 얇게 보조한다. (source=cards; confidence=0.82; provenance=inferred; direction=low-elevation tinted cards를 기본으로 하고, 넓은 내부 여백과 강한 section breathing room. soft round corner를 기본값으로 유지.; evidence=surface=tinted, density=airy, corner=round)
- **chart_panel_framing**: 차트 패널은 soft tint frame과 restrained divider로 프레이밍한다. 헤더 메타데이터와 본문 visualization 사이의 breathing room을 충분히 둔다. (source=data_display; confidence=0.82; provenance=inferred; direction=정보 밀도를 유지하되 thin dividers와 restrained accent로 hierarchy를 만든다.; evidence=layout=data-review-surface, density=airy, layout=conversation-panel, surface=tinted)

### 레퍼런스 근거

- **Carbon Design System**: We welcome all feedback, designs, or ideas in order to produce the best possible experience for our users. If you're interested in contributing, ch...
- **Primer**: Messaging components are used to provide important and relevant information to the user, including feedback, contextual information, product update...

### 구현 노트

- 기존에 같은 역할의 컴포넌트가 있으면 토큰 교체부터 시작
- variant prop으로 시각적 변형을 관리 (하드코딩 금지)
- auto-dismiss 시간은 내용 길이에 비례 (기본 5초)

---

## overlay / confirm-dialog

**역할**: —

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

- 브랜드 기본 규칙을 따릅니다.

### 레퍼런스 근거

- **Primer**: ActionMenu is composed of ActionList and Overlay patterns used for quick actions and selections. AnchoredOverlay

### 구현 노트

- 기존에 같은 역할의 컴포넌트가 있으면 토큰 교체부터 시작
- variant prop으로 시각적 변형을 관리 (하드코딩 금지)
- Escape / backdrop click으로 닫기, 열 때 첫 focusable 요소로 이동

---

## input / textarea

**역할**: —

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

- 브랜드 기본 규칙을 따릅니다.

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

**역할**: —

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

- 브랜드 기본 규칙을 따릅니다.

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

**역할**: —

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

- 브랜드 기본 규칙을 따릅니다.

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

**역할**: —

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

- 브랜드 기본 규칙을 따릅니다.

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

**역할**: —

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

- 브랜드 기본 규칙을 따릅니다.

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

**역할**: —

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

- 브랜드 기본 규칙을 따릅니다.

### Visual Adaptation Hints

- **cta_prominence**: CTA prominence는 medium이다. primary action은 분명하게 보이되 화면 전체를 지배하지 않게 유지한다. (source=cards; confidence=0.82; provenance=inferred; direction=low-elevation tinted cards를 기본으로 하고, 넓은 내부 여백과 강한 section breathing room. soft round corner를 기본값으로 유지.; evidence=surface=tinted, density=airy, corner=round, layout=conversation-panel)

### 레퍼런스 근거

- **Carbon Design System**: These components can toggle between the AI variant and the default variant depending on the user’s interaction. If the user manually overrides the ...
- **Primer**: I get so much joy from writing HTML and CSS, and design systems are one level up - systematically making UIs accessible and consistent. I love conc...

### 구현 노트

- 기존에 같은 역할의 컴포넌트가 있으면 토큰 교체부터 시작
- variant prop으로 시각적 변형을 관리 (하드코딩 금지)
- size prop: sm / md / lg (터치 영역은 항상 최소 44px 보장)

---

## editorial / editor-canvas

**역할**: —

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

- 브랜드 기본 규칙을 따릅니다.

### 구현 노트

- 기존에 같은 역할의 컴포넌트가 있으면 토큰 교체부터 시작
- variant prop으로 시각적 변형을 관리 (하드코딩 금지)
- 블록 단위 데이터 모델, JSON 직렬화 가능한 구조

---

## editorial / editor-toolbar

**역할**: —

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

- 브랜드 기본 규칙을 따릅니다.

### Visual Adaptation Hints

- **filter_nav_density**: filter/nav density는 balanced다. global nav와 local filter를 섞지 말고 계층별 간격 차이로 구조를 드러낸다. (source=navigation; confidence=0.94; provenance=inferred; direction=고정 sidebar 또는 split-pane navigation을 우선하고, 현재 위치와 scope를 항상 명시한다.; evidence=Split-pane workspace, layout=conversation-panel, density=airy)

### 구현 노트

- 기존에 같은 역할의 컴포넌트가 있으면 토큰 교체부터 시작
- variant prop으로 시각적 변형을 관리 (하드코딩 금지)
- 블록 단위 데이터 모델, JSON 직렬화 가능한 구조

---

## editorial / inline-format-menu

**역할**: —

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

- 브랜드 기본 규칙을 따릅니다.

### Visual Adaptation Hints

- **filter_nav_density**: filter/nav density는 balanced다. global nav와 local filter를 섞지 말고 계층별 간격 차이로 구조를 드러낸다. (source=navigation; confidence=0.94; provenance=inferred; direction=고정 sidebar 또는 split-pane navigation을 우선하고, 현재 위치와 scope를 항상 명시한다.; evidence=Split-pane workspace, layout=conversation-panel, density=airy)

### 구현 노트

- 기존에 같은 역할의 컴포넌트가 있으면 토큰 교체부터 시작
- variant prop으로 시각적 변형을 관리 (하드코딩 금지)
- 블록 단위 데이터 모델, JSON 직렬화 가능한 구조

---

## editorial / slash-command-menu

**역할**: —

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

- 브랜드 기본 규칙을 따릅니다.

### Visual Adaptation Hints

- **filter_nav_density**: filter/nav density는 balanced다. global nav와 local filter를 섞지 말고 계층별 간격 차이로 구조를 드러낸다. (source=navigation; confidence=0.94; provenance=inferred; direction=고정 sidebar 또는 split-pane navigation을 우선하고, 현재 위치와 scope를 항상 명시한다.; evidence=Split-pane workspace, layout=conversation-panel, density=airy)

### 구현 노트

- 기존에 같은 역할의 컴포넌트가 있으면 토큰 교체부터 시작
- variant prop으로 시각적 변형을 관리 (하드코딩 금지)
- 블록 단위 데이터 모델, JSON 직렬화 가능한 구조

---

## editorial / block-controls

**역할**: —

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

- 브랜드 기본 규칙을 따릅니다.

### 구현 노트

- 기존에 같은 역할의 컴포넌트가 있으면 토큰 교체부터 시작
- variant prop으로 시각적 변형을 관리 (하드코딩 금지)
- 블록 단위 데이터 모델, JSON 직렬화 가능한 구조

---

## feedback / banner

**역할**: —

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

- 브랜드 기본 규칙을 따릅니다.

### Visual Adaptation Hints

- **card_elevation_tendency**: 카드는 낮은 elevation만 허용하고 색면 차이로 그룹을 구분한다. 내부 여백은 넉넉하게 두고 card breathing room을 확보한다. (source=cards; confidence=0.82; provenance=inferred; direction=low-elevation tinted cards를 기본으로 하고, 넓은 내부 여백과 강한 section breathing room. soft round corner를 기본값으로 유지.; evidence=surface=tinted, density=airy, corner=round)
- **border_vs_fill_emphasis**: fill 중심이다. tint surface로 성격을 만들고 border는 아주 얇게 보조한다. (source=cards; confidence=0.82; provenance=inferred; direction=low-elevation tinted cards를 기본으로 하고, 넓은 내부 여백과 강한 section breathing room. soft round corner를 기본값으로 유지.; evidence=surface=tinted, density=airy, corner=round)

### 레퍼런스 근거

- **Carbon Design System**: We welcome all feedback, designs, or ideas in order to produce the best possible experience for our users. If you're interested in contributing, ch...
- **Primer**: Banner Banner is used to highlight important information.

### 구현 노트

- 기존에 같은 역할의 컴포넌트가 있으면 토큰 교체부터 시작
- variant prop으로 시각적 변형을 관리 (하드코딩 금지)
- auto-dismiss 시간은 내용 길이에 비례 (기본 5초)

---

## data-display / data-table

**역할**: —

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

- 브랜드 기본 규칙을 따릅니다.

### Visual Adaptation Hints

- **card_elevation_tendency**: 카드는 낮은 elevation만 허용하고 색면 차이로 그룹을 구분한다. 내부 여백은 넉넉하게 두고 card breathing room을 확보한다. (source=cards; confidence=0.82; provenance=inferred; direction=low-elevation tinted cards를 기본으로 하고, 넓은 내부 여백과 강한 section breathing room. soft round corner를 기본값으로 유지.; evidence=surface=tinted, density=airy, corner=round)
- **border_vs_fill_emphasis**: fill 중심이다. tint surface로 성격을 만들고 border는 아주 얇게 보조한다. (source=cards; confidence=0.82; provenance=inferred; direction=low-elevation tinted cards를 기본으로 하고, 넓은 내부 여백과 강한 section breathing room. soft round corner를 기본값으로 유지.; evidence=surface=tinted, density=airy, corner=round)
- **filter_nav_density**: filter/nav density는 balanced다. global nav와 local filter를 섞지 말고 계층별 간격 차이로 구조를 드러낸다. (source=navigation; confidence=0.94; provenance=inferred; direction=고정 sidebar 또는 split-pane navigation을 우선하고, 현재 위치와 scope를 항상 명시한다.; evidence=Split-pane workspace, layout=conversation-panel, density=airy)
- **chart_panel_framing**: 차트 패널은 soft tint frame과 restrained divider로 프레이밍한다. 헤더 메타데이터와 본문 visualization 사이의 breathing room을 충분히 둔다. (source=data_display; confidence=0.82; provenance=inferred; direction=정보 밀도를 유지하되 thin dividers와 restrained accent로 hierarchy를 만든다.; evidence=layout=data-review-surface, density=airy, layout=conversation-panel, surface=tinted)

### 레퍼런스 근거

- **Carbon Design System**: Data table Modal
- **Primer**: DataTable DataTable is a 2-dimensional data structure where each row is an item, and each column is a data point about the item.

### 구현 노트

- 기존에 같은 역할의 컴포넌트가 있으면 토큰 교체부터 시작
- variant prop으로 시각적 변형을 관리 (하드코딩 금지)
- 빈 상태(empty-state)와 에러 상태를 반드시 처리

---

## data-display / column-header

**역할**: —

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

- 브랜드 기본 규칙을 따릅니다.

### Visual Adaptation Hints

- **card_elevation_tendency**: 카드는 낮은 elevation만 허용하고 색면 차이로 그룹을 구분한다. 내부 여백은 넉넉하게 두고 card breathing room을 확보한다. (source=cards; confidence=0.82; provenance=inferred; direction=low-elevation tinted cards를 기본으로 하고, 넓은 내부 여백과 강한 section breathing room. soft round corner를 기본값으로 유지.; evidence=surface=tinted, density=airy, corner=round)
- **border_vs_fill_emphasis**: fill 중심이다. tint surface로 성격을 만들고 border는 아주 얇게 보조한다. (source=cards; confidence=0.82; provenance=inferred; direction=low-elevation tinted cards를 기본으로 하고, 넓은 내부 여백과 강한 section breathing room. soft round corner를 기본값으로 유지.; evidence=surface=tinted, density=airy, corner=round)
- **chart_panel_framing**: 차트 패널은 soft tint frame과 restrained divider로 프레이밍한다. 헤더 메타데이터와 본문 visualization 사이의 breathing room을 충분히 둔다. (source=data_display; confidence=0.82; provenance=inferred; direction=정보 밀도를 유지하되 thin dividers와 restrained accent로 hierarchy를 만든다.; evidence=layout=data-review-surface, density=airy, layout=conversation-panel, surface=tinted)

### 구현 노트

- 기존에 같은 역할의 컴포넌트가 있으면 토큰 교체부터 시작
- variant prop으로 시각적 변형을 관리 (하드코딩 금지)
- 빈 상태(empty-state)와 에러 상태를 반드시 처리

---

## data-display / row-actions

**역할**: —

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

- 브랜드 기본 규칙을 따릅니다.

### Visual Adaptation Hints

- **card_elevation_tendency**: 카드는 낮은 elevation만 허용하고 색면 차이로 그룹을 구분한다. 내부 여백은 넉넉하게 두고 card breathing room을 확보한다. (source=cards; confidence=0.82; provenance=inferred; direction=low-elevation tinted cards를 기본으로 하고, 넓은 내부 여백과 강한 section breathing room. soft round corner를 기본값으로 유지.; evidence=surface=tinted, density=airy, corner=round)
- **border_vs_fill_emphasis**: fill 중심이다. tint surface로 성격을 만들고 border는 아주 얇게 보조한다. (source=cards; confidence=0.82; provenance=inferred; direction=low-elevation tinted cards를 기본으로 하고, 넓은 내부 여백과 강한 section breathing room. soft round corner를 기본값으로 유지.; evidence=surface=tinted, density=airy, corner=round)
- **chart_panel_framing**: 차트 패널은 soft tint frame과 restrained divider로 프레이밍한다. 헤더 메타데이터와 본문 visualization 사이의 breathing room을 충분히 둔다. (source=data_display; confidence=0.82; provenance=inferred; direction=정보 밀도를 유지하되 thin dividers와 restrained accent로 hierarchy를 만든다.; evidence=layout=data-review-surface, density=airy, layout=conversation-panel, surface=tinted)

### 구현 노트

- 기존에 같은 역할의 컴포넌트가 있으면 토큰 교체부터 시작
- variant prop으로 시각적 변형을 관리 (하드코딩 금지)
- 빈 상태(empty-state)와 에러 상태를 반드시 처리

---

## navigation / pagination

**역할**: —

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

- 브랜드 기본 규칙을 따릅니다.

### Visual Adaptation Hints

- **filter_nav_density**: filter/nav density는 balanced다. global nav와 local filter를 섞지 말고 계층별 간격 차이로 구조를 드러낸다. (source=navigation; confidence=0.94; provenance=inferred; direction=고정 sidebar 또는 split-pane navigation을 우선하고, 현재 위치와 scope를 항상 명시한다.; evidence=Split-pane workspace, layout=conversation-panel, density=airy)

### 레퍼런스 근거

- **Carbon Design System**: Library menu navigation There are two kinds of symbols — library symbols and document symbols. Library symbols are available in any Sketch document...
- **Primer**: Octicon nav items navigation 12 px

### 구현 노트

- 기존에 같은 역할의 컴포넌트가 있으면 토큰 교체부터 시작
- variant prop으로 시각적 변형을 관리 (하드코딩 금지)
- active 상태는 URL/라우터와 자동 동기화

---

## input / filter-chip

**역할**: —

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

- 브랜드 기본 규칙을 따릅니다.

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

---

## data-display / stat-card

**역할**: —

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

- 브랜드 기본 규칙을 따릅니다.

### Visual Adaptation Hints

- **card_elevation_tendency**: 카드는 낮은 elevation만 허용하고 색면 차이로 그룹을 구분한다. 내부 여백은 넉넉하게 두고 card breathing room을 확보한다. (source=cards; confidence=0.82; provenance=inferred; direction=low-elevation tinted cards를 기본으로 하고, 넓은 내부 여백과 강한 section breathing room. soft round corner를 기본값으로 유지.; evidence=surface=tinted, density=airy, corner=round)
- **border_vs_fill_emphasis**: fill 중심이다. tint surface로 성격을 만들고 border는 아주 얇게 보조한다. (source=cards; confidence=0.82; provenance=inferred; direction=low-elevation tinted cards를 기본으로 하고, 넓은 내부 여백과 강한 section breathing room. soft round corner를 기본값으로 유지.; evidence=surface=tinted, density=airy, corner=round)
- **chart_panel_framing**: 차트 패널은 soft tint frame과 restrained divider로 프레이밍한다. 헤더 메타데이터와 본문 visualization 사이의 breathing room을 충분히 둔다. (source=data_display; confidence=0.82; provenance=inferred; direction=정보 밀도를 유지하되 thin dividers와 restrained accent로 hierarchy를 만든다.; evidence=layout=data-review-surface, density=airy, layout=conversation-panel, surface=tinted)

### 구현 노트

- 기존에 같은 역할의 컴포넌트가 있으면 토큰 교체부터 시작
- variant prop으로 시각적 변형을 관리 (하드코딩 금지)
- 빈 상태(empty-state)와 에러 상태를 반드시 처리

---

## data-display / insight-card

**역할**: —

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

- 브랜드 기본 규칙을 따릅니다.

### Visual Adaptation Hints

- **card_elevation_tendency**: 카드는 낮은 elevation만 허용하고 색면 차이로 그룹을 구분한다. 내부 여백은 넉넉하게 두고 card breathing room을 확보한다. (source=cards; confidence=0.82; provenance=inferred; direction=low-elevation tinted cards를 기본으로 하고, 넓은 내부 여백과 강한 section breathing room. soft round corner를 기본값으로 유지.; evidence=surface=tinted, density=airy, corner=round)
- **border_vs_fill_emphasis**: fill 중심이다. tint surface로 성격을 만들고 border는 아주 얇게 보조한다. (source=cards; confidence=0.82; provenance=inferred; direction=low-elevation tinted cards를 기본으로 하고, 넓은 내부 여백과 강한 section breathing room. soft round corner를 기본값으로 유지.; evidence=surface=tinted, density=airy, corner=round)
- **chart_panel_framing**: 차트 패널은 soft tint frame과 restrained divider로 프레이밍한다. 헤더 메타데이터와 본문 visualization 사이의 breathing room을 충분히 둔다. (source=data_display; confidence=0.82; provenance=inferred; direction=정보 밀도를 유지하되 thin dividers와 restrained accent로 hierarchy를 만든다.; evidence=layout=data-review-surface, density=airy, layout=conversation-panel, surface=tinted)

### 구현 노트

- 기존에 같은 역할의 컴포넌트가 있으면 토큰 교체부터 시작
- variant prop으로 시각적 변형을 관리 (하드코딩 금지)
- 빈 상태(empty-state)와 에러 상태를 반드시 처리

---

## data-display / activity-card

**역할**: —

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

- 브랜드 기본 규칙을 따릅니다.

### Visual Adaptation Hints

- **card_elevation_tendency**: 카드는 낮은 elevation만 허용하고 색면 차이로 그룹을 구분한다. 내부 여백은 넉넉하게 두고 card breathing room을 확보한다. (source=cards; confidence=0.82; provenance=inferred; direction=low-elevation tinted cards를 기본으로 하고, 넓은 내부 여백과 강한 section breathing room. soft round corner를 기본값으로 유지.; evidence=surface=tinted, density=airy, corner=round)
- **border_vs_fill_emphasis**: fill 중심이다. tint surface로 성격을 만들고 border는 아주 얇게 보조한다. (source=cards; confidence=0.82; provenance=inferred; direction=low-elevation tinted cards를 기본으로 하고, 넓은 내부 여백과 강한 section breathing room. soft round corner를 기본값으로 유지.; evidence=surface=tinted, density=airy, corner=round)
- **chart_panel_framing**: 차트 패널은 soft tint frame과 restrained divider로 프레이밍한다. 헤더 메타데이터와 본문 visualization 사이의 breathing room을 충분히 둔다. (source=data_display; confidence=0.82; provenance=inferred; direction=정보 밀도를 유지하되 thin dividers와 restrained accent로 hierarchy를 만든다.; evidence=layout=data-review-surface, density=airy, layout=conversation-panel, surface=tinted)

### 구현 노트

- 기존에 같은 역할의 컴포넌트가 있으면 토큰 교체부터 시작
- variant prop으로 시각적 변형을 관리 (하드코딩 금지)
- 빈 상태(empty-state)와 에러 상태를 반드시 처리

---

## data-display / section-header

**역할**: —

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

- 브랜드 기본 규칙을 따릅니다.

### Visual Adaptation Hints

- **card_elevation_tendency**: 카드는 낮은 elevation만 허용하고 색면 차이로 그룹을 구분한다. 내부 여백은 넉넉하게 두고 card breathing room을 확보한다. (source=cards; confidence=0.82; provenance=inferred; direction=low-elevation tinted cards를 기본으로 하고, 넓은 내부 여백과 강한 section breathing room. soft round corner를 기본값으로 유지.; evidence=surface=tinted, density=airy, corner=round)
- **border_vs_fill_emphasis**: fill 중심이다. tint surface로 성격을 만들고 border는 아주 얇게 보조한다. (source=cards; confidence=0.82; provenance=inferred; direction=low-elevation tinted cards를 기본으로 하고, 넓은 내부 여백과 강한 section breathing room. soft round corner를 기본값으로 유지.; evidence=surface=tinted, density=airy, corner=round)
- **chart_panel_framing**: 차트 패널은 soft tint frame과 restrained divider로 프레이밍한다. 헤더 메타데이터와 본문 visualization 사이의 breathing room을 충분히 둔다. (source=data_display; confidence=0.82; provenance=inferred; direction=정보 밀도를 유지하되 thin dividers와 restrained accent로 hierarchy를 만든다.; evidence=layout=data-review-surface, density=airy, layout=conversation-panel, surface=tinted)

### 구현 노트

- 기존에 같은 역할의 컴포넌트가 있으면 토큰 교체부터 시작
- variant prop으로 시각적 변형을 관리 (하드코딩 금지)
- 빈 상태(empty-state)와 에러 상태를 반드시 처리

---

## document / article-body

**역할**: —

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

- 브랜드 기본 규칙을 따릅니다.

### 레퍼런스 근거

- **Carbon Design System**: AI chat is a conversational framework between a user and an AI that can aid in creating tasks, finding insights, tracking documents, and more. For ...
- **Primer**: The GitHub Design Infrastructure and Design Engineering teams build and maintain Primer — this includes our CSS framework, style guide documentatio...

### 구현 노트

- 기존에 같은 역할의 컴포넌트가 있으면 토큰 교체부터 시작
- variant prop으로 시각적 변형을 관리 (하드코딩 금지)

---

## document / table-of-contents

**역할**: —

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

- 브랜드 기본 규칙을 따릅니다.

### Visual Adaptation Hints

- **card_elevation_tendency**: 카드는 낮은 elevation만 허용하고 색면 차이로 그룹을 구분한다. 내부 여백은 넉넉하게 두고 card breathing room을 확보한다. (source=cards; confidence=0.82; provenance=inferred; direction=low-elevation tinted cards를 기본으로 하고, 넓은 내부 여백과 강한 section breathing room. soft round corner를 기본값으로 유지.; evidence=surface=tinted, density=airy, corner=round)
- **border_vs_fill_emphasis**: fill 중심이다. tint surface로 성격을 만들고 border는 아주 얇게 보조한다. (source=cards; confidence=0.82; provenance=inferred; direction=low-elevation tinted cards를 기본으로 하고, 넓은 내부 여백과 강한 section breathing room. soft round corner를 기본값으로 유지.; evidence=surface=tinted, density=airy, corner=round)
- **filter_nav_density**: filter/nav density는 balanced다. global nav와 local filter를 섞지 말고 계층별 간격 차이로 구조를 드러낸다. (source=navigation; confidence=0.94; provenance=inferred; direction=고정 sidebar 또는 split-pane navigation을 우선하고, 현재 위치와 scope를 항상 명시한다.; evidence=Split-pane workspace, layout=conversation-panel, density=airy)
- **chart_panel_framing**: 차트 패널은 soft tint frame과 restrained divider로 프레이밍한다. 헤더 메타데이터와 본문 visualization 사이의 breathing room을 충분히 둔다. (source=data_display; confidence=0.82; provenance=inferred; direction=정보 밀도를 유지하되 thin dividers와 restrained accent로 hierarchy를 만든다.; evidence=layout=data-review-surface, density=airy, layout=conversation-panel, surface=tinted)

### 레퍼런스 근거

- **Carbon Design System**: AI chat is a conversational framework between a user and an AI that can aid in creating tasks, finding insights, tracking documents, and more. For ...
- **Primer**: The GitHub Design Infrastructure and Design Engineering teams build and maintain Primer — this includes our CSS framework, style guide documentatio...

### 구현 노트

- 기존에 같은 역할의 컴포넌트가 있으면 토큰 교체부터 시작
- variant prop으로 시각적 변형을 관리 (하드코딩 금지)

---

## document / heading-anchor

**역할**: —

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

- 브랜드 기본 규칙을 따릅니다.

### 레퍼런스 근거

- **Carbon Design System**: AI chat is a conversational framework between a user and an AI that can aid in creating tasks, finding insights, tracking documents, and more. For ...
- **Primer**: The GitHub Design Infrastructure and Design Engineering teams build and maintain Primer — this includes our CSS framework, style guide documentatio...

### 구현 노트

- 기존에 같은 역할의 컴포넌트가 있으면 토큰 교체부터 시작
- variant prop으로 시각적 변형을 관리 (하드코딩 금지)

---

## document / prose-block

**역할**: —

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

- 브랜드 기본 규칙을 따릅니다.

### 레퍼런스 근거

- **Carbon Design System**: AI chat is a conversational framework between a user and an AI that can aid in creating tasks, finding insights, tracking documents, and more. For ...
- **Primer**: The GitHub Design Infrastructure and Design Engineering teams build and maintain Primer — this includes our CSS framework, style guide documentatio...

### 구현 노트

- 기존에 같은 역할의 컴포넌트가 있으면 토큰 교체부터 시작
- variant prop으로 시각적 변형을 관리 (하드코딩 금지)

---

## document / reading-pane

**역할**: —

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

- 브랜드 기본 규칙을 따릅니다.

### 레퍼런스 근거

- **Carbon Design System**: AI chat is a conversational framework between a user and an AI that can aid in creating tasks, finding insights, tracking documents, and more. For ...
- **Primer**: The GitHub Design Infrastructure and Design Engineering teams build and maintain Primer — this includes our CSS framework, style guide documentatio...

### 구현 노트

- 기존에 같은 역할의 컴포넌트가 있으면 토큰 교체부터 시작
- variant prop으로 시각적 변형을 관리 (하드코딩 금지)

---

## document / footnote

**역할**: —

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

- 브랜드 기본 규칙을 따릅니다.

### 레퍼런스 근거

- **Carbon Design System**: AI chat is a conversational framework between a user and an AI that can aid in creating tasks, finding insights, tracking documents, and more. For ...
- **Primer**: The GitHub Design Infrastructure and Design Engineering teams build and maintain Primer — this includes our CSS framework, style guide documentatio...

### 구현 노트

- 기존에 같은 역할의 컴포넌트가 있으면 토큰 교체부터 시작
- variant prop으로 시각적 변형을 관리 (하드코딩 금지)

---

## navigation / prev-next-pager

**역할**: —

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

- 브랜드 기본 규칙을 따릅니다.

### Visual Adaptation Hints

- **filter_nav_density**: filter/nav density는 balanced다. global nav와 local filter를 섞지 말고 계층별 간격 차이로 구조를 드러낸다. (source=navigation; confidence=0.94; provenance=inferred; direction=고정 sidebar 또는 split-pane navigation을 우선하고, 현재 위치와 scope를 항상 명시한다.; evidence=Split-pane workspace, layout=conversation-panel, density=airy)

### 레퍼런스 근거

- **Carbon Design System**: Library menu navigation There are two kinds of symbols — library symbols and document symbols. Library symbols are available in any Sketch document...
- **Primer**: Octicon nav items navigation 12 px

### 구현 노트

- 기존에 같은 역할의 컴포넌트가 있으면 토큰 교체부터 시작
- variant prop으로 시각적 변형을 관리 (하드코딩 금지)
- active 상태는 URL/라우터와 자동 동기화

---

## document / link-card

**역할**: —

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

- 브랜드 기본 규칙을 따릅니다.

### Visual Adaptation Hints

- **card_elevation_tendency**: 카드는 낮은 elevation만 허용하고 색면 차이로 그룹을 구분한다. 내부 여백은 넉넉하게 두고 card breathing room을 확보한다. (source=cards; confidence=0.82; provenance=inferred; direction=low-elevation tinted cards를 기본으로 하고, 넓은 내부 여백과 강한 section breathing room. soft round corner를 기본값으로 유지.; evidence=surface=tinted, density=airy, corner=round)
- **border_vs_fill_emphasis**: fill 중심이다. tint surface로 성격을 만들고 border는 아주 얇게 보조한다. (source=cards; confidence=0.82; provenance=inferred; direction=low-elevation tinted cards를 기본으로 하고, 넓은 내부 여백과 강한 section breathing room. soft round corner를 기본값으로 유지.; evidence=surface=tinted, density=airy, corner=round)

### 레퍼런스 근거

- **Carbon Design System**: AI chat is a conversational framework between a user and an AI that can aid in creating tasks, finding insights, tracking documents, and more. For ...
- **Primer**: The GitHub Design Infrastructure and Design Engineering teams build and maintain Primer — this includes our CSS framework, style guide documentatio...

### 구현 노트

- 기존에 같은 역할의 컴포넌트가 있으면 토큰 교체부터 시작
- variant prop으로 시각적 변형을 관리 (하드코딩 금지)

---

## input / date-picker

**역할**: —

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

- 브랜드 기본 규칙을 따릅니다.

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

**역할**: —

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

- 브랜드 기본 규칙을 따릅니다.

### Visual Adaptation Hints

- **card_elevation_tendency**: 카드는 낮은 elevation만 허용하고 색면 차이로 그룹을 구분한다. 내부 여백은 넉넉하게 두고 card breathing room을 확보한다. (source=cards; confidence=0.82; provenance=inferred; direction=low-elevation tinted cards를 기본으로 하고, 넓은 내부 여백과 강한 section breathing room. soft round corner를 기본값으로 유지.; evidence=surface=tinted, density=airy, corner=round)
- **border_vs_fill_emphasis**: fill 중심이다. tint surface로 성격을 만들고 border는 아주 얇게 보조한다. (source=cards; confidence=0.82; provenance=inferred; direction=low-elevation tinted cards를 기본으로 하고, 넓은 내부 여백과 강한 section breathing room. soft round corner를 기본값으로 유지.; evidence=surface=tinted, density=airy, corner=round)
- **chart_panel_framing**: 차트 패널은 soft tint frame과 restrained divider로 프레이밍한다. 헤더 메타데이터와 본문 visualization 사이의 breathing room을 충분히 둔다. (source=data_display; confidence=0.82; provenance=inferred; direction=정보 밀도를 유지하되 thin dividers와 restrained accent로 hierarchy를 만든다.; evidence=layout=data-review-surface, density=airy, layout=conversation-panel, surface=tinted)

### 구현 노트

- 기존에 같은 역할의 컴포넌트가 있으면 토큰 교체부터 시작
- variant prop으로 시각적 변형을 관리 (하드코딩 금지)
- 빈 상태(empty-state)와 에러 상태를 반드시 처리

---

## input / time-picker

**역할**: —

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

- 브랜드 기본 규칙을 따릅니다.

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

**역할**: —

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

- 브랜드 기본 규칙을 따릅니다.

### 레퍼런스 근거

- **Carbon Design System**: Number input Text input
- **Primer**: I worked in data visualization and map-making for most of my career, and solving design problems with data is my jam. To me there's something uniqu...

### 구현 노트

- 기존에 같은 역할의 컴포넌트가 있으면 토큰 교체부터 시작
- variant prop으로 시각적 변형을 관리 (하드코딩 금지)
- error 상태에서 helper text → error message로 자동 전환
- label은 항상 visible (placeholder만으로 대체 금지)

---

## data-display / avatar

**역할**: —

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

- 브랜드 기본 규칙을 따릅니다.

### Visual Adaptation Hints

- **card_elevation_tendency**: 카드는 낮은 elevation만 허용하고 색면 차이로 그룹을 구분한다. 내부 여백은 넉넉하게 두고 card breathing room을 확보한다. (source=cards; confidence=0.82; provenance=inferred; direction=low-elevation tinted cards를 기본으로 하고, 넓은 내부 여백과 강한 section breathing room. soft round corner를 기본값으로 유지.; evidence=surface=tinted, density=airy, corner=round)
- **border_vs_fill_emphasis**: fill 중심이다. tint surface로 성격을 만들고 border는 아주 얇게 보조한다. (source=cards; confidence=0.82; provenance=inferred; direction=low-elevation tinted cards를 기본으로 하고, 넓은 내부 여백과 강한 section breathing room. soft round corner를 기본값으로 유지.; evidence=surface=tinted, density=airy, corner=round)
- **chart_panel_framing**: 차트 패널은 soft tint frame과 restrained divider로 프레이밍한다. 헤더 메타데이터와 본문 visualization 사이의 breathing room을 충분히 둔다. (source=data_display; confidence=0.82; provenance=inferred; direction=정보 밀도를 유지하되 thin dividers와 restrained accent로 hierarchy를 만든다.; evidence=layout=data-review-surface, density=airy, layout=conversation-panel, surface=tinted)

### 레퍼런스 근거

- **Primer**: Avatar Avatar is an image that represents a user or organization.

### 구현 노트

- 기존에 같은 역할의 컴포넌트가 있으면 토큰 교체부터 시작
- variant prop으로 시각적 변형을 관리 (하드코딩 금지)
- 빈 상태(empty-state)와 에러 상태를 반드시 처리

---

## overlay / user-menu

**역할**: —

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

- 브랜드 기본 규칙을 따릅니다.

### Visual Adaptation Hints

- **filter_nav_density**: filter/nav density는 balanced다. global nav와 local filter를 섞지 말고 계층별 간격 차이로 구조를 드러낸다. (source=navigation; confidence=0.94; provenance=inferred; direction=고정 sidebar 또는 split-pane navigation을 우선하고, 현재 위치와 scope를 항상 명시한다.; evidence=Split-pane workspace, layout=conversation-panel, density=airy)

### 레퍼런스 근거

- **Primer**: ActionMenu is composed of ActionList and Overlay patterns used for quick actions and selections. AnchoredOverlay

### 구현 노트

- 기존에 같은 역할의 컴포넌트가 있으면 토큰 교체부터 시작
- variant prop으로 시각적 변형을 관리 (하드코딩 금지)
- Escape / backdrop click으로 닫기, 열 때 첫 focusable 요소로 이동

---

## data-display / profile-card

**역할**: —

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

- 브랜드 기본 규칙을 따릅니다.

### Visual Adaptation Hints

- **card_elevation_tendency**: 카드는 낮은 elevation만 허용하고 색면 차이로 그룹을 구분한다. 내부 여백은 넉넉하게 두고 card breathing room을 확보한다. (source=cards; confidence=0.82; provenance=inferred; direction=low-elevation tinted cards를 기본으로 하고, 넓은 내부 여백과 강한 section breathing room. soft round corner를 기본값으로 유지.; evidence=surface=tinted, density=airy, corner=round)
- **border_vs_fill_emphasis**: fill 중심이다. tint surface로 성격을 만들고 border는 아주 얇게 보조한다. (source=cards; confidence=0.82; provenance=inferred; direction=low-elevation tinted cards를 기본으로 하고, 넓은 내부 여백과 강한 section breathing room. soft round corner를 기본값으로 유지.; evidence=surface=tinted, density=airy, corner=round)
- **chart_panel_framing**: 차트 패널은 soft tint frame과 restrained divider로 프레이밍한다. 헤더 메타데이터와 본문 visualization 사이의 breathing room을 충분히 둔다. (source=data_display; confidence=0.82; provenance=inferred; direction=정보 밀도를 유지하되 thin dividers와 restrained accent로 hierarchy를 만든다.; evidence=layout=data-review-surface, density=airy, layout=conversation-panel, surface=tinted)

### 구현 노트

- 기존에 같은 역할의 컴포넌트가 있으면 토큰 교체부터 시작
- variant prop으로 시각적 변형을 관리 (하드코딩 금지)
- 빈 상태(empty-state)와 에러 상태를 반드시 처리

---

## copilot-artifact / message-artifact

**역할**: —

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

- 브랜드 기본 규칙을 따릅니다.

### 구현 노트

- 기존에 같은 역할의 컴포넌트가 있으면 토큰 교체부터 시작
- variant prop으로 시각적 변형을 관리 (하드코딩 금지)

---

## copilot-artifact / artifact-preview-panel

**역할**: —

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

- 브랜드 기본 규칙을 따릅니다.

### Visual Adaptation Hints

- **card_elevation_tendency**: 카드는 낮은 elevation만 허용하고 색면 차이로 그룹을 구분한다. 내부 여백은 넉넉하게 두고 card breathing room을 확보한다. (source=cards; confidence=0.82; provenance=inferred; direction=low-elevation tinted cards를 기본으로 하고, 넓은 내부 여백과 강한 section breathing room. soft round corner를 기본값으로 유지.; evidence=surface=tinted, density=airy, corner=round)
- **border_vs_fill_emphasis**: fill 중심이다. tint surface로 성격을 만들고 border는 아주 얇게 보조한다. (source=cards; confidence=0.82; provenance=inferred; direction=low-elevation tinted cards를 기본으로 하고, 넓은 내부 여백과 강한 section breathing room. soft round corner를 기본값으로 유지.; evidence=surface=tinted, density=airy, corner=round)
- **chart_panel_framing**: 차트 패널은 soft tint frame과 restrained divider로 프레이밍한다. 헤더 메타데이터와 본문 visualization 사이의 breathing room을 충분히 둔다. (source=data_display; confidence=0.82; provenance=inferred; direction=정보 밀도를 유지하되 thin dividers와 restrained accent로 hierarchy를 만든다.; evidence=layout=data-review-surface, density=airy, layout=conversation-panel, surface=tinted)

### 구현 노트

- 기존에 같은 역할의 컴포넌트가 있으면 토큰 교체부터 시작
- variant prop으로 시각적 변형을 관리 (하드코딩 금지)

---

## copilot-artifact / draft-document

**역할**: —

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

- 브랜드 기본 규칙을 따릅니다.

### 구현 노트

- 기존에 같은 역할의 컴포넌트가 있으면 토큰 교체부터 시작
- variant prop으로 시각적 변형을 관리 (하드코딩 금지)

---

## copilot-artifact / outline-sidebar

**역할**: —

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

- 브랜드 기본 규칙을 따릅니다.

### Visual Adaptation Hints

- **filter_nav_density**: filter/nav density는 balanced다. global nav와 local filter를 섞지 말고 계층별 간격 차이로 구조를 드러낸다. (source=navigation; confidence=0.94; provenance=inferred; direction=고정 sidebar 또는 split-pane navigation을 우선하고, 현재 위치와 scope를 항상 명시한다.; evidence=Split-pane workspace, layout=conversation-panel, density=airy)

### 구현 노트

- 기존에 같은 역할의 컴포넌트가 있으면 토큰 교체부터 시작
- variant prop으로 시각적 변형을 관리 (하드코딩 금지)

---

## copilot-artifact / revision-timeline

**역할**: —

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

- 브랜드 기본 규칙을 따릅니다.

### 구현 노트

- 기존에 같은 역할의 컴포넌트가 있으면 토큰 교체부터 시작
- variant prop으로 시각적 변형을 관리 (하드코딩 금지)

---

## input / tone-slider

**역할**: —

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

- 브랜드 기본 규칙을 따릅니다.

### 레퍼런스 근거

- **Carbon Design System**: Number input Text input
- **Primer**: I worked in data visualization and map-making for most of my career, and solving design problems with data is my jam. To me there's something uniqu...

### 구현 노트

- 기존에 같은 역할의 컴포넌트가 있으면 토큰 교체부터 시작
- variant prop으로 시각적 변형을 관리 (하드코딩 금지)
- error 상태에서 helper text → error message로 자동 전환
- label은 항상 visible (placeholder만으로 대체 금지)

---

## copilot-artifact / reading-mode-toggle

**역할**: —

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

- 브랜드 기본 규칙을 따릅니다.

### 구현 노트

- 기존에 같은 역할의 컴포넌트가 있으면 토큰 교체부터 시작
- variant prop으로 시각적 변형을 관리 (하드코딩 금지)

---

## copilot-artifact / citation-footnote

**역할**: —

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

- 브랜드 기본 규칙을 따릅니다.

### 구현 노트

- 기존에 같은 역할의 컴포넌트가 있으면 토큰 교체부터 시작
- variant prop으로 시각적 변형을 관리 (하드코딩 금지)

---

## copilot-artifact / quote-block

**역할**: —

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

- 브랜드 기본 규칙을 따릅니다.

### 구현 노트

- 기존에 같은 역할의 컴포넌트가 있으면 토큰 교체부터 시작
- variant prop으로 시각적 변형을 관리 (하드코딩 금지)

---

## copilot-artifact / paragraph-block

**역할**: —

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

- 브랜드 기본 규칙을 따릅니다.

### 구현 노트

- 기존에 같은 역할의 컴포넌트가 있으면 토큰 교체부터 시작
- variant prop으로 시각적 변형을 관리 (하드코딩 금지)

---

## data-display / kanban-board

**역할**: —

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

- 브랜드 기본 규칙을 따릅니다.

### Visual Adaptation Hints

- **card_elevation_tendency**: 카드는 낮은 elevation만 허용하고 색면 차이로 그룹을 구분한다. 내부 여백은 넉넉하게 두고 card breathing room을 확보한다. (source=cards; confidence=0.82; provenance=inferred; direction=low-elevation tinted cards를 기본으로 하고, 넓은 내부 여백과 강한 section breathing room. soft round corner를 기본값으로 유지.; evidence=surface=tinted, density=airy, corner=round)
- **border_vs_fill_emphasis**: fill 중심이다. tint surface로 성격을 만들고 border는 아주 얇게 보조한다. (source=cards; confidence=0.82; provenance=inferred; direction=low-elevation tinted cards를 기본으로 하고, 넓은 내부 여백과 강한 section breathing room. soft round corner를 기본값으로 유지.; evidence=surface=tinted, density=airy, corner=round)
- **chart_panel_framing**: 차트 패널은 soft tint frame과 restrained divider로 프레이밍한다. 헤더 메타데이터와 본문 visualization 사이의 breathing room을 충분히 둔다. (source=data_display; confidence=0.82; provenance=inferred; direction=정보 밀도를 유지하되 thin dividers와 restrained accent로 hierarchy를 만든다.; evidence=layout=data-review-surface, density=airy, layout=conversation-panel, surface=tinted)

### 구현 노트

- 기존에 같은 역할의 컴포넌트가 있으면 토큰 교체부터 시작
- variant prop으로 시각적 변형을 관리 (하드코딩 금지)
- 빈 상태(empty-state)와 에러 상태를 반드시 처리

---

## data-display / kanban-column

**역할**: —

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

- 브랜드 기본 규칙을 따릅니다.

### Visual Adaptation Hints

- **card_elevation_tendency**: 카드는 낮은 elevation만 허용하고 색면 차이로 그룹을 구분한다. 내부 여백은 넉넉하게 두고 card breathing room을 확보한다. (source=cards; confidence=0.82; provenance=inferred; direction=low-elevation tinted cards를 기본으로 하고, 넓은 내부 여백과 강한 section breathing room. soft round corner를 기본값으로 유지.; evidence=surface=tinted, density=airy, corner=round)
- **border_vs_fill_emphasis**: fill 중심이다. tint surface로 성격을 만들고 border는 아주 얇게 보조한다. (source=cards; confidence=0.82; provenance=inferred; direction=low-elevation tinted cards를 기본으로 하고, 넓은 내부 여백과 강한 section breathing room. soft round corner를 기본값으로 유지.; evidence=surface=tinted, density=airy, corner=round)
- **chart_panel_framing**: 차트 패널은 soft tint frame과 restrained divider로 프레이밍한다. 헤더 메타데이터와 본문 visualization 사이의 breathing room을 충분히 둔다. (source=data_display; confidence=0.82; provenance=inferred; direction=정보 밀도를 유지하되 thin dividers와 restrained accent로 hierarchy를 만든다.; evidence=layout=data-review-surface, density=airy, layout=conversation-panel, surface=tinted)

### 구현 노트

- 기존에 같은 역할의 컴포넌트가 있으면 토큰 교체부터 시작
- variant prop으로 시각적 변형을 관리 (하드코딩 금지)
- 빈 상태(empty-state)와 에러 상태를 반드시 처리

---

## data-display / kanban-card

**역할**: —

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

- 브랜드 기본 규칙을 따릅니다.

### Visual Adaptation Hints

- **card_elevation_tendency**: 카드는 낮은 elevation만 허용하고 색면 차이로 그룹을 구분한다. 내부 여백은 넉넉하게 두고 card breathing room을 확보한다. (source=cards; confidence=0.82; provenance=inferred; direction=low-elevation tinted cards를 기본으로 하고, 넓은 내부 여백과 강한 section breathing room. soft round corner를 기본값으로 유지.; evidence=surface=tinted, density=airy, corner=round)
- **border_vs_fill_emphasis**: fill 중심이다. tint surface로 성격을 만들고 border는 아주 얇게 보조한다. (source=cards; confidence=0.82; provenance=inferred; direction=low-elevation tinted cards를 기본으로 하고, 넓은 내부 여백과 강한 section breathing room. soft round corner를 기본값으로 유지.; evidence=surface=tinted, density=airy, corner=round)
- **chart_panel_framing**: 차트 패널은 soft tint frame과 restrained divider로 프레이밍한다. 헤더 메타데이터와 본문 visualization 사이의 breathing room을 충분히 둔다. (source=data_display; confidence=0.82; provenance=inferred; direction=정보 밀도를 유지하되 thin dividers와 restrained accent로 hierarchy를 만든다.; evidence=layout=data-review-surface, density=airy, layout=conversation-panel, surface=tinted)

### 구현 노트

- 기존에 같은 역할의 컴포넌트가 있으면 토큰 교체부터 시작
- variant prop으로 시각적 변형을 관리 (하드코딩 금지)
- 빈 상태(empty-state)와 에러 상태를 반드시 처리

---

## data-display / search-results

**역할**: —

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

- 브랜드 기본 규칙을 따릅니다.

### Visual Adaptation Hints

- **card_elevation_tendency**: 카드는 낮은 elevation만 허용하고 색면 차이로 그룹을 구분한다. 내부 여백은 넉넉하게 두고 card breathing room을 확보한다. (source=cards; confidence=0.82; provenance=inferred; direction=low-elevation tinted cards를 기본으로 하고, 넓은 내부 여백과 강한 section breathing room. soft round corner를 기본값으로 유지.; evidence=surface=tinted, density=airy, corner=round)
- **border_vs_fill_emphasis**: fill 중심이다. tint surface로 성격을 만들고 border는 아주 얇게 보조한다. (source=cards; confidence=0.82; provenance=inferred; direction=low-elevation tinted cards를 기본으로 하고, 넓은 내부 여백과 강한 section breathing room. soft round corner를 기본값으로 유지.; evidence=surface=tinted, density=airy, corner=round)
- **filter_nav_density**: filter/nav density는 balanced다. global nav와 local filter를 섞지 말고 계층별 간격 차이로 구조를 드러낸다. (source=navigation; confidence=0.94; provenance=inferred; direction=고정 sidebar 또는 split-pane navigation을 우선하고, 현재 위치와 scope를 항상 명시한다.; evidence=Split-pane workspace, layout=conversation-panel, density=airy)
- **chart_panel_framing**: 차트 패널은 soft tint frame과 restrained divider로 프레이밍한다. 헤더 메타데이터와 본문 visualization 사이의 breathing room을 충분히 둔다. (source=data_display; confidence=0.82; provenance=inferred; direction=정보 밀도를 유지하되 thin dividers와 restrained accent로 hierarchy를 만든다.; evidence=layout=data-review-surface, density=airy, layout=conversation-panel, surface=tinted)

### 구현 노트

- 기존에 같은 역할의 컴포넌트가 있으면 토큰 교체부터 시작
- variant prop으로 시각적 변형을 관리 (하드코딩 금지)
- 빈 상태(empty-state)와 에러 상태를 반드시 처리

---

## input / filter-panel

**역할**: —

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

- 브랜드 기본 규칙을 따릅니다.

### Visual Adaptation Hints

- **card_elevation_tendency**: 카드는 낮은 elevation만 허용하고 색면 차이로 그룹을 구분한다. 내부 여백은 넉넉하게 두고 card breathing room을 확보한다. (source=cards; confidence=0.82; provenance=inferred; direction=low-elevation tinted cards를 기본으로 하고, 넓은 내부 여백과 강한 section breathing room. soft round corner를 기본값으로 유지.; evidence=surface=tinted, density=airy, corner=round)
- **border_vs_fill_emphasis**: fill 중심이다. tint surface로 성격을 만들고 border는 아주 얇게 보조한다. (source=cards; confidence=0.82; provenance=inferred; direction=low-elevation tinted cards를 기본으로 하고, 넓은 내부 여백과 강한 section breathing room. soft round corner를 기본값으로 유지.; evidence=surface=tinted, density=airy, corner=round)
- **filter_nav_density**: filter/nav density는 balanced다. global nav와 local filter를 섞지 말고 계층별 간격 차이로 구조를 드러낸다. (source=navigation; confidence=0.94; provenance=inferred; direction=고정 sidebar 또는 split-pane navigation을 우선하고, 현재 위치와 scope를 항상 명시한다.; evidence=Split-pane workspace, layout=conversation-panel, density=airy)
- **chart_panel_framing**: 차트 패널은 soft tint frame과 restrained divider로 프레이밍한다. 헤더 메타데이터와 본문 visualization 사이의 breathing room을 충분히 둔다. (source=data_display; confidence=0.82; provenance=inferred; direction=정보 밀도를 유지하되 thin dividers와 restrained accent로 hierarchy를 만든다.; evidence=layout=data-review-surface, density=airy, layout=conversation-panel, surface=tinted)

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

**역할**: —

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

- 브랜드 기본 규칙을 따릅니다.

### 레퍼런스 근거

- **Primer**: Autocomplete Autocomplete allows users to quickly filter through a list of options and pick one or more values for a field.

### 구현 노트

- 기존에 같은 역할의 컴포넌트가 있으면 토큰 교체부터 시작
- variant prop으로 시각적 변형을 관리 (하드코딩 금지)
- Escape / backdrop click으로 닫기, 열 때 첫 focusable 요소로 이동

---

## feedback / step-progress

**역할**: —

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

- 브랜드 기본 규칙을 따릅니다.

### 레퍼런스 근거

- **Carbon Design System**: We welcome all feedback, designs, or ideas in order to produce the best possible experience for our users. If you're interested in contributing, ch...
- **Primer**: Messaging components are used to provide important and relevant information to the user, including feedback, contextual information, product update...

### 구현 노트

- 기존에 같은 역할의 컴포넌트가 있으면 토큰 교체부터 시작
- variant prop으로 시각적 변형을 관리 (하드코딩 금지)
- auto-dismiss 시간은 내용 길이에 비례 (기본 5초)

---

## navigation / wizard-layout

**역할**: —

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

- 브랜드 기본 규칙을 따릅니다.

### Visual Adaptation Hints

- **filter_nav_density**: filter/nav density는 balanced다. global nav와 local filter를 섞지 말고 계층별 간격 차이로 구조를 드러낸다. (source=navigation; confidence=0.94; provenance=inferred; direction=고정 sidebar 또는 split-pane navigation을 우선하고, 현재 위치와 scope를 항상 명시한다.; evidence=Split-pane workspace, layout=conversation-panel, density=airy)

### 레퍼런스 근거

- **Carbon Design System**: Library menu navigation There are two kinds of symbols — library symbols and document symbols. Library symbols are available in any Sketch document...
- **Primer**: Octicon nav items navigation 12 px

### 구현 노트

- 기존에 같은 역할의 컴포넌트가 있으면 토큰 교체부터 시작
- variant prop으로 시각적 변형을 관리 (하드코딩 금지)
- active 상태는 URL/라우터와 자동 동기화

---

## overlay / tooltip-guide

**역할**: —

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

- 브랜드 기본 규칙을 따릅니다.

### 레퍼런스 근거

- **Primer**: ActionMenu is composed of ActionList and Overlay patterns used for quick actions and selections. AnchoredOverlay

### 구현 노트

- 기존에 같은 역할의 컴포넌트가 있으면 토큰 교체부터 시작
- variant prop으로 시각적 변형을 관리 (하드코딩 금지)
- Escape / backdrop click으로 닫기, 열 때 첫 focusable 요소로 이동

---

## overlay / command-palette

**역할**: —

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

- 브랜드 기본 규칙을 따릅니다.

### 레퍼런스 근거

- **Primer**: ActionMenu is composed of ActionList and Overlay patterns used for quick actions and selections. AnchoredOverlay

### 구현 노트

- 기존에 같은 역할의 컴포넌트가 있으면 토큰 교체부터 시작
- variant prop으로 시각적 변형을 관리 (하드코딩 금지)
- Escape / backdrop click으로 닫기, 열 때 첫 focusable 요소로 이동

---

## overlay / command-result-item

**역할**: —

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

- 브랜드 기본 규칙을 따릅니다.

### 레퍼런스 근거

- **Primer**: ActionMenu is composed of ActionList and Overlay patterns used for quick actions and selections. AnchoredOverlay

### 구현 노트

- 기존에 같은 역할의 컴포넌트가 있으면 토큰 교체부터 시작
- variant prop으로 시각적 변형을 관리 (하드코딩 금지)
- Escape / backdrop click으로 닫기, 열 때 첫 focusable 요소로 이동

---

## feedback / shortcut-hint

**역할**: —

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

- 브랜드 기본 규칙을 따릅니다.

### 레퍼런스 근거

- **Carbon Design System**: We welcome all feedback, designs, or ideas in order to produce the best possible experience for our users. If you're interested in contributing, ch...
- **Primer**: Messaging components are used to provide important and relevant information to the user, including feedback, contextual information, product update...

### 구현 노트

- 기존에 같은 역할의 컴포넌트가 있으면 토큰 교체부터 시작
- variant prop으로 시각적 변형을 관리 (하드코딩 금지)
- auto-dismiss 시간은 내용 길이에 비례 (기본 5초)

---

## data-display / video-player

**역할**: —

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

- 브랜드 기본 규칙을 따릅니다.

### Visual Adaptation Hints

- **card_elevation_tendency**: 카드는 낮은 elevation만 허용하고 색면 차이로 그룹을 구분한다. 내부 여백은 넉넉하게 두고 card breathing room을 확보한다. (source=cards; confidence=0.82; provenance=inferred; direction=low-elevation tinted cards를 기본으로 하고, 넓은 내부 여백과 강한 section breathing room. soft round corner를 기본값으로 유지.; evidence=surface=tinted, density=airy, corner=round)
- **border_vs_fill_emphasis**: fill 중심이다. tint surface로 성격을 만들고 border는 아주 얇게 보조한다. (source=cards; confidence=0.82; provenance=inferred; direction=low-elevation tinted cards를 기본으로 하고, 넓은 내부 여백과 강한 section breathing room. soft round corner를 기본값으로 유지.; evidence=surface=tinted, density=airy, corner=round)
- **chart_panel_framing**: 차트 패널은 soft tint frame과 restrained divider로 프레이밍한다. 헤더 메타데이터와 본문 visualization 사이의 breathing room을 충분히 둔다. (source=data_display; confidence=0.82; provenance=inferred; direction=정보 밀도를 유지하되 thin dividers와 restrained accent로 hierarchy를 만든다.; evidence=layout=data-review-surface, density=airy, layout=conversation-panel, surface=tinted)

### 구현 노트

- 기존에 같은 역할의 컴포넌트가 있으면 토큰 교체부터 시작
- variant prop으로 시각적 변형을 관리 (하드코딩 금지)
- 빈 상태(empty-state)와 에러 상태를 반드시 처리

---

## button / player-controls

**역할**: —

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

- 브랜드 기본 규칙을 따릅니다.

### Visual Adaptation Hints

- **cta_prominence**: CTA prominence는 medium이다. primary action은 분명하게 보이되 화면 전체를 지배하지 않게 유지한다. (source=cards; confidence=0.82; provenance=inferred; direction=low-elevation tinted cards를 기본으로 하고, 넓은 내부 여백과 강한 section breathing room. soft round corner를 기본값으로 유지.; evidence=surface=tinted, density=airy, corner=round, layout=conversation-panel)

### 레퍼런스 근거

- **Carbon Design System**: These components can toggle between the AI variant and the default variant depending on the user’s interaction. If the user manually overrides the ...
- **Primer**: I get so much joy from writing HTML and CSS, and design systems are one level up - systematically making UIs accessible and consistent. I love conc...

### 구현 노트

- 기존에 같은 역할의 컴포넌트가 있으면 토큰 교체부터 시작
- variant prop으로 시각적 변형을 관리 (하드코딩 금지)
- size prop: sm / md / lg (터치 영역은 항상 최소 44px 보장)

---

## input / volume-slider

**역할**: —

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

- 브랜드 기본 규칙을 따릅니다.

### 레퍼런스 근거

- **Carbon Design System**: Number input Text input
- **Primer**: I worked in data visualization and map-making for most of my career, and solving design problems with data is my jam. To me there's something uniqu...

### 구현 노트

- 기존에 같은 역할의 컴포넌트가 있으면 토큰 교체부터 시작
- variant prop으로 시각적 변형을 관리 (하드코딩 금지)
- error 상태에서 helper text → error message로 자동 전환
- label은 항상 visible (placeholder만으로 대체 금지)

---

## marketing / logo-cloud

**역할**: —

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

- 브랜드 기본 규칙을 따릅니다.

### 레퍼런스 근거

- **Primer**: Design digital marketing experiences with Primer Brand UI Shared Foundations

### 구현 노트

- 기존에 같은 역할의 컴포넌트가 있으면 토큰 교체부터 시작
- variant prop으로 시각적 변형을 관리 (하드코딩 금지)
- 섹션에 <h2 id="...">과 aria-labelledby 필수
- CSS 변수(var(--color-*))를 그대로 쓰고 hex 하드코딩 금지
- 다크 모드는 globals.css의 prefers-color-scheme 블록에 위임

---

## marketing / customer-logo

**역할**: —

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

- 브랜드 기본 규칙을 따릅니다.

### 레퍼런스 근거

- **Primer**: Design digital marketing experiences with Primer Brand UI Shared Foundations

### 구현 노트

- 기존에 같은 역할의 컴포넌트가 있으면 토큰 교체부터 시작
- variant prop으로 시각적 변형을 관리 (하드코딩 금지)
- 섹션에 <h2 id="...">과 aria-labelledby 필수
- CSS 변수(var(--color-*))를 그대로 쓰고 hex 하드코딩 금지
- 다크 모드는 globals.css의 prefers-color-scheme 블록에 위임

---

## marketing / metric-highlight

**역할**: —

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

- 브랜드 기본 규칙을 따릅니다.

### Visual Adaptation Hints

- **card_elevation_tendency**: 카드는 낮은 elevation만 허용하고 색면 차이로 그룹을 구분한다. 내부 여백은 넉넉하게 두고 card breathing room을 확보한다. (source=cards; confidence=0.82; provenance=inferred; direction=low-elevation tinted cards를 기본으로 하고, 넓은 내부 여백과 강한 section breathing room. soft round corner를 기본값으로 유지.; evidence=surface=tinted, density=airy, corner=round)
- **border_vs_fill_emphasis**: fill 중심이다. tint surface로 성격을 만들고 border는 아주 얇게 보조한다. (source=cards; confidence=0.82; provenance=inferred; direction=low-elevation tinted cards를 기본으로 하고, 넓은 내부 여백과 강한 section breathing room. soft round corner를 기본값으로 유지.; evidence=surface=tinted, density=airy, corner=round)
- **chart_panel_framing**: 차트 패널은 soft tint frame과 restrained divider로 프레이밍한다. 헤더 메타데이터와 본문 visualization 사이의 breathing room을 충분히 둔다. (source=data_display; confidence=0.82; provenance=inferred; direction=정보 밀도를 유지하되 thin dividers와 restrained accent로 hierarchy를 만든다.; evidence=layout=data-review-surface, density=airy, layout=conversation-panel, surface=tinted)

### 레퍼런스 근거

- **Primer**: Design digital marketing experiences with Primer Brand UI Shared Foundations

### 구현 노트

- 기존에 같은 역할의 컴포넌트가 있으면 토큰 교체부터 시작
- variant prop으로 시각적 변형을 관리 (하드코딩 금지)
- 섹션에 <h2 id="...">과 aria-labelledby 필수
- CSS 변수(var(--color-*))를 그대로 쓰고 hex 하드코딩 금지
- 다크 모드는 globals.css의 prefers-color-scheme 블록에 위임

---

## marketing / press-quote

**역할**: —

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

- 브랜드 기본 규칙을 따릅니다.

### 레퍼런스 근거

- **Primer**: Design digital marketing experiences with Primer Brand UI Shared Foundations

### 구현 노트

- 기존에 같은 역할의 컴포넌트가 있으면 토큰 교체부터 시작
- variant prop으로 시각적 변형을 관리 (하드코딩 금지)
- 섹션에 <h2 id="...">과 aria-labelledby 필수
- CSS 변수(var(--color-*))를 그대로 쓰고 hex 하드코딩 금지
- 다크 모드는 globals.css의 prefers-color-scheme 블록에 위임

---

## input / upload-dropzone

**역할**: —

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

- 브랜드 기본 규칙을 따릅니다.

### 레퍼런스 근거

- **Carbon Design System**: Number input Text input
- **Primer**: I worked in data visualization and map-making for most of my career, and solving design problems with data is my jam. To me there's something uniqu...

### 구현 노트

- 기존에 같은 역할의 컴포넌트가 있으면 토큰 교체부터 시작
- variant prop으로 시각적 변형을 관리 (하드코딩 금지)
- error 상태에서 helper text → error message로 자동 전환
- label은 항상 visible (placeholder만으로 대체 금지)

---

## data-display / file-preview

**역할**: —

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

- 브랜드 기본 규칙을 따릅니다.

### Visual Adaptation Hints

- **card_elevation_tendency**: 카드는 낮은 elevation만 허용하고 색면 차이로 그룹을 구분한다. 내부 여백은 넉넉하게 두고 card breathing room을 확보한다. (source=cards; confidence=0.82; provenance=inferred; direction=low-elevation tinted cards를 기본으로 하고, 넓은 내부 여백과 강한 section breathing room. soft round corner를 기본값으로 유지.; evidence=surface=tinted, density=airy, corner=round)
- **border_vs_fill_emphasis**: fill 중심이다. tint surface로 성격을 만들고 border는 아주 얇게 보조한다. (source=cards; confidence=0.82; provenance=inferred; direction=low-elevation tinted cards를 기본으로 하고, 넓은 내부 여백과 강한 section breathing room. soft round corner를 기본값으로 유지.; evidence=surface=tinted, density=airy, corner=round)
- **chart_panel_framing**: 차트 패널은 soft tint frame과 restrained divider로 프레이밍한다. 헤더 메타데이터와 본문 visualization 사이의 breathing room을 충분히 둔다. (source=data_display; confidence=0.82; provenance=inferred; direction=정보 밀도를 유지하되 thin dividers와 restrained accent로 hierarchy를 만든다.; evidence=layout=data-review-surface, density=airy, layout=conversation-panel, surface=tinted)

### 구현 노트

- 기존에 같은 역할의 컴포넌트가 있으면 토큰 교체부터 시작
- variant prop으로 시각적 변형을 관리 (하드코딩 금지)
- 빈 상태(empty-state)와 에러 상태를 반드시 처리

---

## feedback / upload-progress

**역할**: —

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

- 브랜드 기본 규칙을 따릅니다.

### 레퍼런스 근거

- **Carbon Design System**: We welcome all feedback, designs, or ideas in order to produce the best possible experience for our users. If you're interested in contributing, ch...
- **Primer**: Messaging components are used to provide important and relevant information to the user, including feedback, contextual information, product update...

### 구현 노트

- 기존에 같은 역할의 컴포넌트가 있으면 토큰 교체부터 시작
- variant prop으로 시각적 변형을 관리 (하드코딩 금지)
- auto-dismiss 시간은 내용 길이에 비례 (기본 5초)

---

## data-display / chart-container

**역할**: —

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

- 브랜드 기본 규칙을 따릅니다.

### Visual Adaptation Hints

- **card_elevation_tendency**: 카드는 낮은 elevation만 허용하고 색면 차이로 그룹을 구분한다. 내부 여백은 넉넉하게 두고 card breathing room을 확보한다. (source=cards; confidence=0.82; provenance=inferred; direction=low-elevation tinted cards를 기본으로 하고, 넓은 내부 여백과 강한 section breathing room. soft round corner를 기본값으로 유지.; evidence=surface=tinted, density=airy, corner=round)
- **border_vs_fill_emphasis**: fill 중심이다. tint surface로 성격을 만들고 border는 아주 얇게 보조한다. (source=cards; confidence=0.82; provenance=inferred; direction=low-elevation tinted cards를 기본으로 하고, 넓은 내부 여백과 강한 section breathing room. soft round corner를 기본값으로 유지.; evidence=surface=tinted, density=airy, corner=round)
- **chart_panel_framing**: 차트 패널은 soft tint frame과 restrained divider로 프레이밍한다. 헤더 메타데이터와 본문 visualization 사이의 breathing room을 충분히 둔다. (source=data_display; confidence=0.82; provenance=inferred; direction=정보 밀도를 유지하되 thin dividers와 restrained accent로 hierarchy를 만든다.; evidence=layout=data-review-surface, density=airy, layout=conversation-panel, surface=tinted)

### 구현 노트

- 기존에 같은 역할의 컴포넌트가 있으면 토큰 교체부터 시작
- variant prop으로 시각적 변형을 관리 (하드코딩 금지)
- 빈 상태(empty-state)와 에러 상태를 반드시 처리

---

## overlay / chart-tooltip

**역할**: —

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

- 브랜드 기본 규칙을 따릅니다.

### Visual Adaptation Hints

- **card_elevation_tendency**: 카드는 낮은 elevation만 허용하고 색면 차이로 그룹을 구분한다. 내부 여백은 넉넉하게 두고 card breathing room을 확보한다. (source=cards; confidence=0.82; provenance=inferred; direction=low-elevation tinted cards를 기본으로 하고, 넓은 내부 여백과 강한 section breathing room. soft round corner를 기본값으로 유지.; evidence=surface=tinted, density=airy, corner=round)
- **border_vs_fill_emphasis**: fill 중심이다. tint surface로 성격을 만들고 border는 아주 얇게 보조한다. (source=cards; confidence=0.82; provenance=inferred; direction=low-elevation tinted cards를 기본으로 하고, 넓은 내부 여백과 강한 section breathing room. soft round corner를 기본값으로 유지.; evidence=surface=tinted, density=airy, corner=round)
- **chart_panel_framing**: 차트 패널은 soft tint frame과 restrained divider로 프레이밍한다. 헤더 메타데이터와 본문 visualization 사이의 breathing room을 충분히 둔다. (source=data_display; confidence=0.82; provenance=inferred; direction=정보 밀도를 유지하되 thin dividers와 restrained accent로 hierarchy를 만든다.; evidence=layout=data-review-surface, density=airy, layout=conversation-panel, surface=tinted)

### 레퍼런스 근거

- **Primer**: ActionMenu is composed of ActionList and Overlay patterns used for quick actions and selections. AnchoredOverlay

### 구현 노트

- 기존에 같은 역할의 컴포넌트가 있으면 토큰 교체부터 시작
- variant prop으로 시각적 변형을 관리 (하드코딩 금지)
- Escape / backdrop click으로 닫기, 열 때 첫 focusable 요소로 이동

---

## data-display / chart-legend

**역할**: —

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

- 브랜드 기본 규칙을 따릅니다.

### Visual Adaptation Hints

- **card_elevation_tendency**: 카드는 낮은 elevation만 허용하고 색면 차이로 그룹을 구분한다. 내부 여백은 넉넉하게 두고 card breathing room을 확보한다. (source=cards; confidence=0.82; provenance=inferred; direction=low-elevation tinted cards를 기본으로 하고, 넓은 내부 여백과 강한 section breathing room. soft round corner를 기본값으로 유지.; evidence=surface=tinted, density=airy, corner=round)
- **border_vs_fill_emphasis**: fill 중심이다. tint surface로 성격을 만들고 border는 아주 얇게 보조한다. (source=cards; confidence=0.82; provenance=inferred; direction=low-elevation tinted cards를 기본으로 하고, 넓은 내부 여백과 강한 section breathing room. soft round corner를 기본값으로 유지.; evidence=surface=tinted, density=airy, corner=round)
- **chart_panel_framing**: 차트 패널은 soft tint frame과 restrained divider로 프레이밍한다. 헤더 메타데이터와 본문 visualization 사이의 breathing room을 충분히 둔다. (source=data_display; confidence=0.82; provenance=inferred; direction=정보 밀도를 유지하되 thin dividers와 restrained accent로 hierarchy를 만든다.; evidence=layout=data-review-surface, density=airy, layout=conversation-panel, surface=tinted)

### 구현 노트

- 기존에 같은 역할의 컴포넌트가 있으면 토큰 교체부터 시작
- variant prop으로 시각적 변형을 관리 (하드코딩 금지)
- 빈 상태(empty-state)와 에러 상태를 반드시 처리

---

## social / feed-item

**역할**: —

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

- 브랜드 기본 규칙을 따릅니다.

### 레퍼런스 근거

- **Primer**: Onboarding is a virtual unboxing experience that helps users get started with a feature. This is a guide for designing onboarding for the product a...

### 구현 노트

- 기존에 같은 역할의 컴포넌트가 있으면 토큰 교체부터 시작
- variant prop으로 시각적 변형을 관리 (하드코딩 금지)

---

## social / post-card

**역할**: —

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

- 브랜드 기본 규칙을 따릅니다.

### Visual Adaptation Hints

- **card_elevation_tendency**: 카드는 낮은 elevation만 허용하고 색면 차이로 그룹을 구분한다. 내부 여백은 넉넉하게 두고 card breathing room을 확보한다. (source=cards; confidence=0.82; provenance=inferred; direction=low-elevation tinted cards를 기본으로 하고, 넓은 내부 여백과 강한 section breathing room. soft round corner를 기본값으로 유지.; evidence=surface=tinted, density=airy, corner=round)
- **border_vs_fill_emphasis**: fill 중심이다. tint surface로 성격을 만들고 border는 아주 얇게 보조한다. (source=cards; confidence=0.82; provenance=inferred; direction=low-elevation tinted cards를 기본으로 하고, 넓은 내부 여백과 강한 section breathing room. soft round corner를 기본값으로 유지.; evidence=surface=tinted, density=airy, corner=round)

### 레퍼런스 근거

- **Primer**: Onboarding is a virtual unboxing experience that helps users get started with a feature. This is a guide for designing onboarding for the product a...

### 구현 노트

- 기존에 같은 역할의 컴포넌트가 있으면 토큰 교체부터 시작
- variant prop으로 시각적 변형을 관리 (하드코딩 금지)

---

## social / thread-view

**역할**: —

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

- 브랜드 기본 규칙을 따릅니다.

### 레퍼런스 근거

- **Primer**: Onboarding is a virtual unboxing experience that helps users get started with a feature. This is a guide for designing onboarding for the product a...

### 구현 노트

- 기존에 같은 역할의 컴포넌트가 있으면 토큰 교체부터 시작
- variant prop으로 시각적 변형을 관리 (하드코딩 금지)

---

## input / reply-composer

**역할**: —

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

- 브랜드 기본 규칙을 따릅니다.

### 레퍼런스 근거

- **Carbon Design System**: Number input Text input
- **Primer**: I worked in data visualization and map-making for most of my career, and solving design problems with data is my jam. To me there's something uniqu...

### 구현 노트

- 기존에 같은 역할의 컴포넌트가 있으면 토큰 교체부터 시작
- variant prop으로 시각적 변형을 관리 (하드코딩 금지)
- error 상태에서 helper text → error message로 자동 전환
- label은 항상 visible (placeholder만으로 대체 금지)

---

## social / reaction-bar

**역할**: —

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

- 브랜드 기본 규칙을 따릅니다.

### 레퍼런스 근거

- **Primer**: Onboarding is a virtual unboxing experience that helps users get started with a feature. This is a guide for designing onboarding for the product a...

### 구현 노트

- 기존에 같은 역할의 컴포넌트가 있으면 토큰 교체부터 시작
- variant prop으로 시각적 변형을 관리 (하드코딩 금지)

---

## button / follow-button

**역할**: —

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

- 브랜드 기본 규칙을 따릅니다.

### Visual Adaptation Hints

- **cta_prominence**: CTA prominence는 medium이다. primary action은 분명하게 보이되 화면 전체를 지배하지 않게 유지한다. (source=cards; confidence=0.82; provenance=inferred; direction=low-elevation tinted cards를 기본으로 하고, 넓은 내부 여백과 강한 section breathing room. soft round corner를 기본값으로 유지.; evidence=surface=tinted, density=airy, corner=round, layout=conversation-panel)

### 레퍼런스 근거

- **Carbon Design System**: These components can toggle between the AI variant and the default variant depending on the user’s interaction. If the user manually overrides the ...
- **Primer**: I get so much joy from writing HTML and CSS, and design systems are one level up - systematically making UIs accessible and consistent. I love conc...

### 구현 노트

- 기존에 같은 역할의 컴포넌트가 있으면 토큰 교체부터 시작
- variant prop으로 시각적 변형을 관리 (하드코딩 금지)
- size prop: sm / md / lg (터치 영역은 항상 최소 44px 보장)

---

## social / timeline-stream

**역할**: —

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

- 브랜드 기본 규칙을 따릅니다.

### 레퍼런스 근거

- **Primer**: Onboarding is a virtual unboxing experience that helps users get started with a feature. This is a guide for designing onboarding for the product a...

### 구현 노트

- 기존에 같은 역할의 컴포넌트가 있으면 토큰 교체부터 시작
- variant prop으로 시각적 변형을 관리 (하드코딩 금지)

---

## social / avatar-cluster

**역할**: —

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

- 브랜드 기본 규칙을 따릅니다.

### 레퍼런스 근거

- **Primer**: Onboarding is a virtual unboxing experience that helps users get started with a feature. This is a guide for designing onboarding for the product a...

### 구현 노트

- 기존에 같은 역할의 컴포넌트가 있으면 토큰 교체부터 시작
- variant prop으로 시각적 변형을 관리 (하드코딩 금지)

---

## data-display / tag-pill

**역할**: —

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

- 브랜드 기본 규칙을 따릅니다.

### Visual Adaptation Hints

- **card_elevation_tendency**: 카드는 낮은 elevation만 허용하고 색면 차이로 그룹을 구분한다. 내부 여백은 넉넉하게 두고 card breathing room을 확보한다. (source=cards; confidence=0.82; provenance=inferred; direction=low-elevation tinted cards를 기본으로 하고, 넓은 내부 여백과 강한 section breathing room. soft round corner를 기본값으로 유지.; evidence=surface=tinted, density=airy, corner=round)
- **border_vs_fill_emphasis**: fill 중심이다. tint surface로 성격을 만들고 border는 아주 얇게 보조한다. (source=cards; confidence=0.82; provenance=inferred; direction=low-elevation tinted cards를 기본으로 하고, 넓은 내부 여백과 강한 section breathing room. soft round corner를 기본값으로 유지.; evidence=surface=tinted, density=airy, corner=round)
- **chart_panel_framing**: 차트 패널은 soft tint frame과 restrained divider로 프레이밍한다. 헤더 메타데이터와 본문 visualization 사이의 breathing room을 충분히 둔다. (source=data_display; confidence=0.82; provenance=inferred; direction=정보 밀도를 유지하되 thin dividers와 restrained accent로 hierarchy를 만든다.; evidence=layout=data-review-surface, density=airy, layout=conversation-panel, surface=tinted)

### 구현 노트

- 기존에 같은 역할의 컴포넌트가 있으면 토큰 교체부터 시작
- variant prop으로 시각적 변형을 관리 (하드코딩 금지)
- 빈 상태(empty-state)와 에러 상태를 반드시 처리

---

## overlay / share-sheet

**역할**: —

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

- 브랜드 기본 규칙을 따릅니다.

### 레퍼런스 근거

- **Primer**: ActionMenu is composed of ActionList and Overlay patterns used for quick actions and selections. AnchoredOverlay

### 구현 노트

- 기존에 같은 역할의 컴포넌트가 있으면 토큰 교체부터 시작
- variant prop으로 시각적 변형을 관리 (하드코딩 금지)
- Escape / backdrop click으로 닫기, 열 때 첫 focusable 요소로 이동

---

## feedback / empty-feed-illustration

**역할**: —

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

- 브랜드 기본 규칙을 따릅니다.

### 레퍼런스 근거

- **Carbon Design System**: We welcome all feedback, designs, or ideas in order to produce the best possible experience for our users. If you're interested in contributing, ch...
- **Primer**: Messaging components are used to provide important and relevant information to the user, including feedback, contextual information, product update...

### 구현 노트

- 기존에 같은 역할의 컴포넌트가 있으면 토큰 교체부터 시작
- variant prop으로 시각적 변형을 관리 (하드코딩 금지)
- auto-dismiss 시간은 내용 길이에 비례 (기본 5초)

---

## feedback / gentle-toast

**역할**: —

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

- 브랜드 기본 규칙을 따릅니다.

### 레퍼런스 근거

- **Carbon Design System**: We welcome all feedback, designs, or ideas in order to produce the best possible experience for our users. If you're interested in contributing, ch...
- **Primer**: Messaging components are used to provide important and relevant information to the user, including feedback, contextual information, product update...

### 구현 노트

- 기존에 같은 역할의 컴포넌트가 있으면 토큰 교체부터 시작
- variant prop으로 시각적 변형을 관리 (하드코딩 금지)
- auto-dismiss 시간은 내용 길이에 비례 (기본 5초)

---

## overlay / soft-dialog

**역할**: —

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

- 브랜드 기본 규칙을 따릅니다.

### 레퍼런스 근거

- **Primer**: ActionMenu is composed of ActionList and Overlay patterns used for quick actions and selections. AnchoredOverlay

### 구현 노트

- 기존에 같은 역할의 컴포넌트가 있으면 토큰 교체부터 시작
- variant prop으로 시각적 변형을 관리 (하드코딩 금지)
- Escape / backdrop click으로 닫기, 열 때 첫 focusable 요소로 이동

---

## data-display / pricing-card

**역할**: —

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

- 브랜드 기본 규칙을 따릅니다.

### Visual Adaptation Hints

- **card_elevation_tendency**: 카드는 낮은 elevation만 허용하고 색면 차이로 그룹을 구분한다. 내부 여백은 넉넉하게 두고 card breathing room을 확보한다. (source=cards; confidence=0.82; provenance=inferred; direction=low-elevation tinted cards를 기본으로 하고, 넓은 내부 여백과 강한 section breathing room. soft round corner를 기본값으로 유지.; evidence=surface=tinted, density=airy, corner=round)
- **border_vs_fill_emphasis**: fill 중심이다. tint surface로 성격을 만들고 border는 아주 얇게 보조한다. (source=cards; confidence=0.82; provenance=inferred; direction=low-elevation tinted cards를 기본으로 하고, 넓은 내부 여백과 강한 section breathing room. soft round corner를 기본값으로 유지.; evidence=surface=tinted, density=airy, corner=round)
- **chart_panel_framing**: 차트 패널은 soft tint frame과 restrained divider로 프레이밍한다. 헤더 메타데이터와 본문 visualization 사이의 breathing room을 충분히 둔다. (source=data_display; confidence=0.82; provenance=inferred; direction=정보 밀도를 유지하되 thin dividers와 restrained accent로 hierarchy를 만든다.; evidence=layout=data-review-surface, density=airy, layout=conversation-panel, surface=tinted)

### 구현 노트

- 기존에 같은 역할의 컴포넌트가 있으면 토큰 교체부터 시작
- variant prop으로 시각적 변형을 관리 (하드코딩 금지)
- 빈 상태(empty-state)와 에러 상태를 반드시 처리

---

## data-display / feature-comparison

**역할**: —

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

- 브랜드 기본 규칙을 따릅니다.

### Visual Adaptation Hints

- **card_elevation_tendency**: 카드는 낮은 elevation만 허용하고 색면 차이로 그룹을 구분한다. 내부 여백은 넉넉하게 두고 card breathing room을 확보한다. (source=cards; confidence=0.82; provenance=inferred; direction=low-elevation tinted cards를 기본으로 하고, 넓은 내부 여백과 강한 section breathing room. soft round corner를 기본값으로 유지.; evidence=surface=tinted, density=airy, corner=round)
- **border_vs_fill_emphasis**: fill 중심이다. tint surface로 성격을 만들고 border는 아주 얇게 보조한다. (source=cards; confidence=0.82; provenance=inferred; direction=low-elevation tinted cards를 기본으로 하고, 넓은 내부 여백과 강한 section breathing room. soft round corner를 기본값으로 유지.; evidence=surface=tinted, density=airy, corner=round)
- **chart_panel_framing**: 차트 패널은 soft tint frame과 restrained divider로 프레이밍한다. 헤더 메타데이터와 본문 visualization 사이의 breathing room을 충분히 둔다. (source=data_display; confidence=0.82; provenance=inferred; direction=정보 밀도를 유지하되 thin dividers와 restrained accent로 hierarchy를 만든다.; evidence=layout=data-review-surface, density=airy, layout=conversation-panel, surface=tinted)

### 구현 노트

- 기존에 같은 역할의 컴포넌트가 있으면 토큰 교체부터 시작
- variant prop으로 시각적 변형을 관리 (하드코딩 금지)
- 빈 상태(empty-state)와 에러 상태를 반드시 처리

---

## feedback / upgrade-banner

**역할**: —

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

- 브랜드 기본 규칙을 따릅니다.

### Visual Adaptation Hints

- **card_elevation_tendency**: 카드는 낮은 elevation만 허용하고 색면 차이로 그룹을 구분한다. 내부 여백은 넉넉하게 두고 card breathing room을 확보한다. (source=cards; confidence=0.82; provenance=inferred; direction=low-elevation tinted cards를 기본으로 하고, 넓은 내부 여백과 강한 section breathing room. soft round corner를 기본값으로 유지.; evidence=surface=tinted, density=airy, corner=round)
- **border_vs_fill_emphasis**: fill 중심이다. tint surface로 성격을 만들고 border는 아주 얇게 보조한다. (source=cards; confidence=0.82; provenance=inferred; direction=low-elevation tinted cards를 기본으로 하고, 넓은 내부 여백과 강한 section breathing room. soft round corner를 기본값으로 유지.; evidence=surface=tinted, density=airy, corner=round)
- **cta_prominence**: CTA prominence는 medium이다. primary action은 분명하게 보이되 화면 전체를 지배하지 않게 유지한다. (source=cards; confidence=0.82; provenance=inferred; direction=low-elevation tinted cards를 기본으로 하고, 넓은 내부 여백과 강한 section breathing room. soft round corner를 기본값으로 유지.; evidence=surface=tinted, density=airy, corner=round, layout=conversation-panel)

### 레퍼런스 근거

- **Carbon Design System**: We welcome all feedback, designs, or ideas in order to produce the best possible experience for our users. If you're interested in contributing, ch...
- **Primer**: Messaging components are used to provide important and relevant information to the user, including feedback, contextual information, product update...

### 구현 노트

- 기존에 같은 역할의 컴포넌트가 있으면 토큰 교체부터 시작
- variant prop으로 시각적 변형을 관리 (하드코딩 금지)
- auto-dismiss 시간은 내용 길이에 비례 (기본 5초)

---

## marketing / faq-section

**역할**: —

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

- 브랜드 기본 규칙을 따릅니다.

### 레퍼런스 근거

- **Primer**: Design digital marketing experiences with Primer Brand UI Shared Foundations

### 구현 노트

- 기존에 같은 역할의 컴포넌트가 있으면 토큰 교체부터 시작
- variant prop으로 시각적 변형을 관리 (하드코딩 금지)
- 섹션에 <h2 id="...">과 aria-labelledby 필수
- CSS 변수(var(--color-*))를 그대로 쓰고 hex 하드코딩 금지
- 다크 모드는 globals.css의 prefers-color-scheme 블록에 위임

---

## marketing / faq-item

**역할**: —

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

- 브랜드 기본 규칙을 따릅니다.

### 레퍼런스 근거

- **Primer**: Design digital marketing experiences with Primer Brand UI Shared Foundations

### 구현 노트

- 기존에 같은 역할의 컴포넌트가 있으면 토큰 교체부터 시작
- variant prop으로 시각적 변형을 관리 (하드코딩 금지)
- 섹션에 <h2 id="...">과 aria-labelledby 필수
- CSS 변수(var(--color-*))를 그대로 쓰고 hex 하드코딩 금지
- 다크 모드는 globals.css의 prefers-color-scheme 블록에 위임

---

## marketing / faq-question

**역할**: —

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

- 브랜드 기본 규칙을 따릅니다.

### 레퍼런스 근거

- **Primer**: Design digital marketing experiences with Primer Brand UI Shared Foundations

### 구현 노트

- 기존에 같은 역할의 컴포넌트가 있으면 토큰 교체부터 시작
- variant prop으로 시각적 변형을 관리 (하드코딩 금지)
- 섹션에 <h2 id="...">과 aria-labelledby 필수
- CSS 변수(var(--color-*))를 그대로 쓰고 hex 하드코딩 금지
- 다크 모드는 globals.css의 prefers-color-scheme 블록에 위임

---

## marketing / faq-answer

**역할**: —

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

- 브랜드 기본 규칙을 따릅니다.

### 레퍼런스 근거

- **Primer**: Design digital marketing experiences with Primer Brand UI Shared Foundations

### 구현 노트

- 기존에 같은 역할의 컴포넌트가 있으면 토큰 교체부터 시작
- variant prop으로 시각적 변형을 관리 (하드코딩 금지)
- 섹션에 <h2 id="...">과 aria-labelledby 필수
- CSS 변수(var(--color-*))를 그대로 쓰고 hex 하드코딩 금지
- 다크 모드는 globals.css의 prefers-color-scheme 블록에 위임

---

## commerce / product-grid

**역할**: —

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

- 브랜드 기본 규칙을 따릅니다.

### Visual Adaptation Hints

- **card_elevation_tendency**: 카드는 낮은 elevation만 허용하고 색면 차이로 그룹을 구분한다. 내부 여백은 넉넉하게 두고 card breathing room을 확보한다. (source=cards; confidence=0.82; provenance=inferred; direction=low-elevation tinted cards를 기본으로 하고, 넓은 내부 여백과 강한 section breathing room. soft round corner를 기본값으로 유지.; evidence=surface=tinted, density=airy, corner=round)
- **border_vs_fill_emphasis**: fill 중심이다. tint surface로 성격을 만들고 border는 아주 얇게 보조한다. (source=cards; confidence=0.82; provenance=inferred; direction=low-elevation tinted cards를 기본으로 하고, 넓은 내부 여백과 강한 section breathing room. soft round corner를 기본값으로 유지.; evidence=surface=tinted, density=airy, corner=round)
- **chart_panel_framing**: 차트 패널은 soft tint frame과 restrained divider로 프레이밍한다. 헤더 메타데이터와 본문 visualization 사이의 breathing room을 충분히 둔다. (source=data_display; confidence=0.82; provenance=inferred; direction=정보 밀도를 유지하되 thin dividers와 restrained accent로 hierarchy를 만든다.; evidence=layout=data-review-surface, density=airy, layout=conversation-panel, surface=tinted)

### 구현 노트

- 기존에 같은 역할의 컴포넌트가 있으면 토큰 교체부터 시작
- variant prop으로 시각적 변형을 관리 (하드코딩 금지)

---

## commerce / product-card

**역할**: —

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

- 브랜드 기본 규칙을 따릅니다.

### Visual Adaptation Hints

- **card_elevation_tendency**: 카드는 낮은 elevation만 허용하고 색면 차이로 그룹을 구분한다. 내부 여백은 넉넉하게 두고 card breathing room을 확보한다. (source=cards; confidence=0.82; provenance=inferred; direction=low-elevation tinted cards를 기본으로 하고, 넓은 내부 여백과 강한 section breathing room. soft round corner를 기본값으로 유지.; evidence=surface=tinted, density=airy, corner=round)
- **border_vs_fill_emphasis**: fill 중심이다. tint surface로 성격을 만들고 border는 아주 얇게 보조한다. (source=cards; confidence=0.82; provenance=inferred; direction=low-elevation tinted cards를 기본으로 하고, 넓은 내부 여백과 강한 section breathing room. soft round corner를 기본값으로 유지.; evidence=surface=tinted, density=airy, corner=round)

### 구현 노트

- 기존에 같은 역할의 컴포넌트가 있으면 토큰 교체부터 시작
- variant prop으로 시각적 변형을 관리 (하드코딩 금지)

---

## commerce / product-detail

**역할**: —

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

- 브랜드 기본 규칙을 따릅니다.

### 구현 노트

- 기존에 같은 역할의 컴포넌트가 있으면 토큰 교체부터 시작
- variant prop으로 시각적 변형을 관리 (하드코딩 금지)

---

## commerce / product-gallery

**역할**: —

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

- 브랜드 기본 규칙을 따릅니다.

### 구현 노트

- 기존에 같은 역할의 컴포넌트가 있으면 토큰 교체부터 시작
- variant prop으로 시각적 변형을 관리 (하드코딩 금지)

---

## commerce / product-hero-image

**역할**: —

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

- 브랜드 기본 규칙을 따릅니다.

### 구현 노트

- 기존에 같은 역할의 컴포넌트가 있으면 토큰 교체부터 시작
- variant prop으로 시각적 변형을 관리 (하드코딩 금지)

---

## commerce / image-thumbnail

**역할**: —

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

- 브랜드 기본 규칙을 따릅니다.

### 구현 노트

- 기존에 같은 역할의 컴포넌트가 있으면 토큰 교체부터 시작
- variant prop으로 시각적 변형을 관리 (하드코딩 금지)

---

## input / variant-selector

**역할**: —

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

- 브랜드 기본 규칙을 따릅니다.

### 레퍼런스 근거

- **Carbon Design System**: Number input Text input
- **Primer**: I worked in data visualization and map-making for most of my career, and solving design problems with data is my jam. To me there's something uniqu...

### 구현 노트

- 기존에 같은 역할의 컴포넌트가 있으면 토큰 교체부터 시작
- variant prop으로 시각적 변형을 관리 (하드코딩 금지)
- error 상태에서 helper text → error message로 자동 전환
- label은 항상 visible (placeholder만으로 대체 금지)

---

## input / size-selector

**역할**: —

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

- 브랜드 기본 규칙을 따릅니다.

### 레퍼런스 근거

- **Carbon Design System**: Number input Text input
- **Primer**: I worked in data visualization and map-making for most of my career, and solving design problems with data is my jam. To me there's something uniqu...

### 구현 노트

- 기존에 같은 역할의 컴포넌트가 있으면 토큰 교체부터 시작
- variant prop으로 시각적 변형을 관리 (하드코딩 금지)
- error 상태에서 helper text → error message로 자동 전환
- label은 항상 visible (placeholder만으로 대체 금지)

---

## input / color-swatch-selector

**역할**: —

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

- 브랜드 기본 규칙을 따릅니다.

### 레퍼런스 근거

- **Carbon Design System**: Number input Text input
- **Primer**: I worked in data visualization and map-making for most of my career, and solving design problems with data is my jam. To me there's something uniqu...

### 구현 노트

- 기존에 같은 역할의 컴포넌트가 있으면 토큰 교체부터 시작
- variant prop으로 시각적 변형을 관리 (하드코딩 금지)
- error 상태에서 helper text → error message로 자동 전환
- label은 항상 visible (placeholder만으로 대체 금지)

---

## button / add-to-cart-button

**역할**: —

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

- 브랜드 기본 규칙을 따릅니다.

### Visual Adaptation Hints

- **cta_prominence**: CTA prominence는 medium이다. primary action은 분명하게 보이되 화면 전체를 지배하지 않게 유지한다. (source=cards; confidence=0.82; provenance=inferred; direction=low-elevation tinted cards를 기본으로 하고, 넓은 내부 여백과 강한 section breathing room. soft round corner를 기본값으로 유지.; evidence=surface=tinted, density=airy, corner=round, layout=conversation-panel)

### 레퍼런스 근거

- **Carbon Design System**: These components can toggle between the AI variant and the default variant depending on the user’s interaction. If the user manually overrides the ...
- **Primer**: I get so much joy from writing HTML and CSS, and design systems are one level up - systematically making UIs accessible and consistent. I love conc...

### 구현 노트

- 기존에 같은 역할의 컴포넌트가 있으면 토큰 교체부터 시작
- variant prop으로 시각적 변형을 관리 (하드코딩 금지)
- size prop: sm / md / lg (터치 영역은 항상 최소 44px 보장)

---

## overlay / quick-view-modal

**역할**: —

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

- 브랜드 기본 규칙을 따릅니다.

### 레퍼런스 근거

- **Primer**: ActionMenu is composed of ActionList and Overlay patterns used for quick actions and selections. AnchoredOverlay

### 구현 노트

- 기존에 같은 역할의 컴포넌트가 있으면 토큰 교체부터 시작
- variant prop으로 시각적 변형을 관리 (하드코딩 금지)
- Escape / backdrop click으로 닫기, 열 때 첫 focusable 요소로 이동

---

## button / wishlist-toggle

**역할**: —

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

- 브랜드 기본 규칙을 따릅니다.

### Visual Adaptation Hints

- **cta_prominence**: CTA prominence는 medium이다. primary action은 분명하게 보이되 화면 전체를 지배하지 않게 유지한다. (source=cards; confidence=0.82; provenance=inferred; direction=low-elevation tinted cards를 기본으로 하고, 넓은 내부 여백과 강한 section breathing room. soft round corner를 기본값으로 유지.; evidence=surface=tinted, density=airy, corner=round, layout=conversation-panel)

### 레퍼런스 근거

- **Carbon Design System**: These components can toggle between the AI variant and the default variant depending on the user’s interaction. If the user manually overrides the ...
- **Primer**: I get so much joy from writing HTML and CSS, and design systems are one level up - systematically making UIs accessible and consistent. I love conc...

### 구현 노트

- 기존에 같은 역할의 컴포넌트가 있으면 토큰 교체부터 시작
- variant prop으로 시각적 변형을 관리 (하드코딩 금지)
- size prop: sm / md / lg (터치 영역은 항상 최소 44px 보장)

---

## commerce / price-tag

**역할**: —

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

- 브랜드 기본 규칙을 따릅니다.

### 구현 노트

- 기존에 같은 역할의 컴포넌트가 있으면 토큰 교체부터 시작
- variant prop으로 시각적 변형을 관리 (하드코딩 금지)

---

## commerce / original-price-strikethrough

**역할**: —

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

- 브랜드 기본 규칙을 따릅니다.

### 구현 노트

- 기존에 같은 역할의 컴포넌트가 있으면 토큰 교체부터 시작
- variant prop으로 시각적 변형을 관리 (하드코딩 금지)

---

## feedback / discount-badge

**역할**: —

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

- 브랜드 기본 규칙을 따릅니다.

### 레퍼런스 근거

- **Carbon Design System**: We welcome all feedback, designs, or ideas in order to produce the best possible experience for our users. If you're interested in contributing, ch...
- **Primer**: Messaging components are used to provide important and relevant information to the user, including feedback, contextual information, product update...

### 구현 노트

- 기존에 같은 역할의 컴포넌트가 있으면 토큰 교체부터 시작
- variant prop으로 시각적 변형을 관리 (하드코딩 금지)
- auto-dismiss 시간은 내용 길이에 비례 (기본 5초)

---

## commerce / cross-sell-grid

**역할**: —

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

- 브랜드 기본 규칙을 따릅니다.

### Visual Adaptation Hints

- **card_elevation_tendency**: 카드는 낮은 elevation만 허용하고 색면 차이로 그룹을 구분한다. 내부 여백은 넉넉하게 두고 card breathing room을 확보한다. (source=cards; confidence=0.82; provenance=inferred; direction=low-elevation tinted cards를 기본으로 하고, 넓은 내부 여백과 강한 section breathing room. soft round corner를 기본값으로 유지.; evidence=surface=tinted, density=airy, corner=round)
- **border_vs_fill_emphasis**: fill 중심이다. tint surface로 성격을 만들고 border는 아주 얇게 보조한다. (source=cards; confidence=0.82; provenance=inferred; direction=low-elevation tinted cards를 기본으로 하고, 넓은 내부 여백과 강한 section breathing room. soft round corner를 기본값으로 유지.; evidence=surface=tinted, density=airy, corner=round)
- **chart_panel_framing**: 차트 패널은 soft tint frame과 restrained divider로 프레이밍한다. 헤더 메타데이터와 본문 visualization 사이의 breathing room을 충분히 둔다. (source=data_display; confidence=0.82; provenance=inferred; direction=정보 밀도를 유지하되 thin dividers와 restrained accent로 hierarchy를 만든다.; evidence=layout=data-review-surface, density=airy, layout=conversation-panel, surface=tinted)

### 구현 노트

- 기존에 같은 역할의 컴포넌트가 있으면 토큰 교체부터 시작
- variant prop으로 시각적 변형을 관리 (하드코딩 금지)

---

## navigation / category-pill

**역할**: —

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

- 브랜드 기본 규칙을 따릅니다.

### Visual Adaptation Hints

- **filter_nav_density**: filter/nav density는 balanced다. global nav와 local filter를 섞지 말고 계층별 간격 차이로 구조를 드러낸다. (source=navigation; confidence=0.94; provenance=inferred; direction=고정 sidebar 또는 split-pane navigation을 우선하고, 현재 위치와 scope를 항상 명시한다.; evidence=Split-pane workspace, layout=conversation-panel, density=airy)

### 레퍼런스 근거

- **Carbon Design System**: Library menu navigation There are two kinds of symbols — library symbols and document symbols. Library symbols are available in any Sketch document...
- **Primer**: Octicon nav items navigation 12 px

### 구현 노트

- 기존에 같은 역할의 컴포넌트가 있으면 토큰 교체부터 시작
- variant prop으로 시각적 변형을 관리 (하드코딩 금지)
- active 상태는 URL/라우터와 자동 동기화

---

## input / filter-sidebar

**역할**: —

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

- 브랜드 기본 규칙을 따릅니다.

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

---

## input / sort-dropdown

**역할**: —

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

- 브랜드 기본 규칙을 따릅니다.

### 레퍼런스 근거

- **Carbon Design System**: Number input Text input
- **Primer**: I worked in data visualization and map-making for most of my career, and solving design problems with data is my jam. To me there's something uniqu...

### 구현 노트

- 기존에 같은 역할의 컴포넌트가 있으면 토큰 교체부터 시작
- variant prop으로 시각적 변형을 관리 (하드코딩 금지)
- error 상태에서 helper text → error message로 자동 전환
- label은 항상 visible (placeholder만으로 대체 금지)

---

## overlay / chat-panel

**역할**: —

**탐지 출처**: visual-reference

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

- 브랜드 기본 규칙을 따릅니다.

### Visual Adaptation Hints

- **card_elevation_tendency**: 카드는 낮은 elevation만 허용하고 색면 차이로 그룹을 구분한다. 내부 여백은 넉넉하게 두고 card breathing room을 확보한다. (source=cards; confidence=0.82; provenance=inferred; direction=low-elevation tinted cards를 기본으로 하고, 넓은 내부 여백과 강한 section breathing room. soft round corner를 기본값으로 유지.; evidence=surface=tinted, density=airy, corner=round)
- **border_vs_fill_emphasis**: fill 중심이다. tint surface로 성격을 만들고 border는 아주 얇게 보조한다. (source=cards; confidence=0.82; provenance=inferred; direction=low-elevation tinted cards를 기본으로 하고, 넓은 내부 여백과 강한 section breathing room. soft round corner를 기본값으로 유지.; evidence=surface=tinted, density=airy, corner=round)
- **chart_panel_framing**: 차트 패널은 soft tint frame과 restrained divider로 프레이밍한다. 헤더 메타데이터와 본문 visualization 사이의 breathing room을 충분히 둔다. (source=data_display; confidence=0.82; provenance=inferred; direction=정보 밀도를 유지하되 thin dividers와 restrained accent로 hierarchy를 만든다.; evidence=layout=data-review-surface, density=airy, layout=conversation-panel, surface=tinted)

### 레퍼런스 근거

- **Primer**: ActionMenu is composed of ActionList and Overlay patterns used for quick actions and selections. AnchoredOverlay

### 구현 노트

- 기존에 같은 역할의 컴포넌트가 있으면 토큰 교체부터 시작
- variant prop으로 시각적 변형을 관리 (하드코딩 금지)
- Escape / backdrop click으로 닫기, 열 때 첫 focusable 요소로 이동

---

## overlay / message-thread

**역할**: —

**탐지 출처**: visual-reference

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

- 브랜드 기본 규칙을 따릅니다.

### 레퍼런스 근거

- **Primer**: ActionMenu is composed of ActionList and Overlay patterns used for quick actions and selections. AnchoredOverlay

### 구현 노트

- 기존에 같은 역할의 컴포넌트가 있으면 토큰 교체부터 시작
- variant prop으로 시각적 변형을 관리 (하드코딩 금지)
- Escape / backdrop click으로 닫기, 열 때 첫 focusable 요소로 이동

---

## overlay / message-composer

**역할**: —

**탐지 출처**: visual-reference

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

- 브랜드 기본 규칙을 따릅니다.

### 레퍼런스 근거

- **Primer**: ActionMenu is composed of ActionList and Overlay patterns used for quick actions and selections. AnchoredOverlay

### 구현 노트

- 기존에 같은 역할의 컴포넌트가 있으면 토큰 교체부터 시작
- variant prop으로 시각적 변형을 관리 (하드코딩 금지)
- Escape / backdrop click으로 닫기, 열 때 첫 focusable 요소로 이동

---

## overlay / context-drawer

**역할**: —

**탐지 출처**: visual-reference

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

- 브랜드 기본 규칙을 따릅니다.

### 레퍼런스 근거

- **Primer**: ActionMenu is composed of ActionList and Overlay patterns used for quick actions and selections. AnchoredOverlay

### 구현 노트

- 기존에 같은 역할의 컴포넌트가 있으면 토큰 교체부터 시작
- variant prop으로 시각적 변형을 관리 (하드코딩 금지)
- Escape / backdrop click으로 닫기, 열 때 첫 focusable 요소로 이동

---

## data-display / filter-toolbar

**역할**: —

**탐지 출처**: visual-reference

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

- 브랜드 기본 규칙을 따릅니다.

### Visual Adaptation Hints

- **card_elevation_tendency**: 카드는 낮은 elevation만 허용하고 색면 차이로 그룹을 구분한다. 내부 여백은 넉넉하게 두고 card breathing room을 확보한다. (source=cards; confidence=0.82; provenance=inferred; direction=low-elevation tinted cards를 기본으로 하고, 넓은 내부 여백과 강한 section breathing room. soft round corner를 기본값으로 유지.; evidence=surface=tinted, density=airy, corner=round)
- **border_vs_fill_emphasis**: fill 중심이다. tint surface로 성격을 만들고 border는 아주 얇게 보조한다. (source=cards; confidence=0.82; provenance=inferred; direction=low-elevation tinted cards를 기본으로 하고, 넓은 내부 여백과 강한 section breathing room. soft round corner를 기본값으로 유지.; evidence=surface=tinted, density=airy, corner=round)
- **filter_nav_density**: filter/nav density는 balanced다. global nav와 local filter를 섞지 말고 계층별 간격 차이로 구조를 드러낸다. (source=navigation; confidence=0.94; provenance=inferred; direction=고정 sidebar 또는 split-pane navigation을 우선하고, 현재 위치와 scope를 항상 명시한다.; evidence=Split-pane workspace, layout=conversation-panel, density=airy)
- **chart_panel_framing**: 차트 패널은 soft tint frame과 restrained divider로 프레이밍한다. 헤더 메타데이터와 본문 visualization 사이의 breathing room을 충분히 둔다. (source=data_display; confidence=0.82; provenance=inferred; direction=정보 밀도를 유지하되 thin dividers와 restrained accent로 hierarchy를 만든다.; evidence=layout=data-review-surface, density=airy, layout=conversation-panel, surface=tinted)

### 구현 노트

- 기존에 같은 역할의 컴포넌트가 있으면 토큰 교체부터 시작
- variant prop으로 시각적 변형을 관리 (하드코딩 금지)
- 빈 상태(empty-state)와 에러 상태를 반드시 처리

---

## editorial / content-card

**역할**: —

**탐지 출처**: visual-reference

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

- 브랜드 기본 규칙을 따릅니다.

### Visual Adaptation Hints

- **card_elevation_tendency**: 카드는 낮은 elevation만 허용하고 색면 차이로 그룹을 구분한다. 내부 여백은 넉넉하게 두고 card breathing room을 확보한다. (source=cards; confidence=0.82; provenance=inferred; direction=low-elevation tinted cards를 기본으로 하고, 넓은 내부 여백과 강한 section breathing room. soft round corner를 기본값으로 유지.; evidence=surface=tinted, density=airy, corner=round)
- **border_vs_fill_emphasis**: fill 중심이다. tint surface로 성격을 만들고 border는 아주 얇게 보조한다. (source=cards; confidence=0.82; provenance=inferred; direction=low-elevation tinted cards를 기본으로 하고, 넓은 내부 여백과 강한 section breathing room. soft round corner를 기본값으로 유지.; evidence=surface=tinted, density=airy, corner=round)

### 구현 노트

- 기존에 같은 역할의 컴포넌트가 있으면 토큰 교체부터 시작
- variant prop으로 시각적 변형을 관리 (하드코딩 금지)
- 블록 단위 데이터 모델, JSON 직렬화 가능한 구조

---

## editorial / featured-story-card

**역할**: —

**탐지 출처**: visual-reference

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

- 브랜드 기본 규칙을 따릅니다.

### Visual Adaptation Hints

- **card_elevation_tendency**: 카드는 낮은 elevation만 허용하고 색면 차이로 그룹을 구분한다. 내부 여백은 넉넉하게 두고 card breathing room을 확보한다. (source=cards; confidence=0.82; provenance=inferred; direction=low-elevation tinted cards를 기본으로 하고, 넓은 내부 여백과 강한 section breathing room. soft round corner를 기본값으로 유지.; evidence=surface=tinted, density=airy, corner=round)
- **border_vs_fill_emphasis**: fill 중심이다. tint surface로 성격을 만들고 border는 아주 얇게 보조한다. (source=cards; confidence=0.82; provenance=inferred; direction=low-elevation tinted cards를 기본으로 하고, 넓은 내부 여백과 강한 section breathing room. soft round corner를 기본값으로 유지.; evidence=surface=tinted, density=airy, corner=round)

### 구현 노트

- 기존에 같은 역할의 컴포넌트가 있으면 토큰 교체부터 시작
- variant prop으로 시각적 변형을 관리 (하드코딩 금지)
- 블록 단위 데이터 모델, JSON 직렬화 가능한 구조

---

## editorial / content-meta

**역할**: —

**탐지 출처**: visual-reference

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

- 브랜드 기본 규칙을 따릅니다.

### 구현 노트

- 기존에 같은 역할의 컴포넌트가 있으면 토큰 교체부터 시작
- variant prop으로 시각적 변형을 관리 (하드코딩 금지)
- 블록 단위 데이터 모델, JSON 직렬화 가능한 구조

---

## editorial / byline-row

**역할**: —

**탐지 출처**: visual-reference

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

- 브랜드 기본 규칙을 따릅니다.

### 구현 노트

- 기존에 같은 역할의 컴포넌트가 있으면 토큰 교체부터 시작
- variant prop으로 시각적 변형을 관리 (하드코딩 금지)
- 블록 단위 데이터 모델, JSON 직렬화 가능한 구조

---

## navigation / workspace-switcher

**역할**: —

**탐지 출처**: visual-reference

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

- 브랜드 기본 규칙을 따릅니다.

### Visual Adaptation Hints

- **filter_nav_density**: filter/nav density는 balanced다. global nav와 local filter를 섞지 말고 계층별 간격 차이로 구조를 드러낸다. (source=navigation; confidence=0.94; provenance=inferred; direction=고정 sidebar 또는 split-pane navigation을 우선하고, 현재 위치와 scope를 항상 명시한다.; evidence=Split-pane workspace, layout=conversation-panel, density=airy)

### 레퍼런스 근거

- **Carbon Design System**: Library menu navigation There are two kinds of symbols — library symbols and document symbols. Library symbols are available in any Sketch document...
- **Primer**: Octicon nav items navigation 12 px

### 구현 노트

- 기존에 같은 역할의 컴포넌트가 있으면 토큰 교체부터 시작
- variant prop으로 시각적 변형을 관리 (하드코딩 금지)
- active 상태는 URL/라우터와 자동 동기화

---

## navigation / context-panel

**역할**: —

**탐지 출처**: visual-reference

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

- 브랜드 기본 규칙을 따릅니다.

### Visual Adaptation Hints

- **card_elevation_tendency**: 카드는 낮은 elevation만 허용하고 색면 차이로 그룹을 구분한다. 내부 여백은 넉넉하게 두고 card breathing room을 확보한다. (source=cards; confidence=0.82; provenance=inferred; direction=low-elevation tinted cards를 기본으로 하고, 넓은 내부 여백과 강한 section breathing room. soft round corner를 기본값으로 유지.; evidence=surface=tinted, density=airy, corner=round)
- **border_vs_fill_emphasis**: fill 중심이다. tint surface로 성격을 만들고 border는 아주 얇게 보조한다. (source=cards; confidence=0.82; provenance=inferred; direction=low-elevation tinted cards를 기본으로 하고, 넓은 내부 여백과 강한 section breathing room. soft round corner를 기본값으로 유지.; evidence=surface=tinted, density=airy, corner=round)
- **filter_nav_density**: filter/nav density는 balanced다. global nav와 local filter를 섞지 말고 계층별 간격 차이로 구조를 드러낸다. (source=navigation; confidence=0.94; provenance=inferred; direction=고정 sidebar 또는 split-pane navigation을 우선하고, 현재 위치와 scope를 항상 명시한다.; evidence=Split-pane workspace, layout=conversation-panel, density=airy)
- **chart_panel_framing**: 차트 패널은 soft tint frame과 restrained divider로 프레이밍한다. 헤더 메타데이터와 본문 visualization 사이의 breathing room을 충분히 둔다. (source=data_display; confidence=0.82; provenance=inferred; direction=정보 밀도를 유지하되 thin dividers와 restrained accent로 hierarchy를 만든다.; evidence=layout=data-review-surface, density=airy, layout=conversation-panel, surface=tinted)

### 레퍼런스 근거

- **Carbon Design System**: Library menu navigation There are two kinds of symbols — library symbols and document symbols. Library symbols are available in any Sketch document...
- **Primer**: Octicon nav items navigation 12 px

### 구현 노트

- 기존에 같은 역할의 컴포넌트가 있으면 토큰 교체부터 시작
- variant prop으로 시각적 변형을 관리 (하드코딩 금지)
- active 상태는 URL/라우터와 자동 동기화

---

## marketing / hero-section

**역할**: —

**탐지 출처**: visual-reference

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

- 브랜드 기본 규칙을 따릅니다.

### 레퍼런스 근거

- **Primer**: Design digital marketing experiences with Primer Brand UI Shared Foundations

### 구현 노트

- 기존에 같은 역할의 컴포넌트가 있으면 토큰 교체부터 시작
- variant prop으로 시각적 변형을 관리 (하드코딩 금지)
- 섹션에 <h2 id="...">과 aria-labelledby 필수
- CSS 변수(var(--color-*))를 그대로 쓰고 hex 하드코딩 금지
- 다크 모드는 globals.css의 prefers-color-scheme 블록에 위임

---

## marketing / hero-headline

**역할**: —

**탐지 출처**: visual-reference

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

- 브랜드 기본 규칙을 따릅니다.

### 레퍼런스 근거

- **Primer**: Design digital marketing experiences with Primer Brand UI Shared Foundations

### 구현 노트

- 기존에 같은 역할의 컴포넌트가 있으면 토큰 교체부터 시작
- variant prop으로 시각적 변형을 관리 (하드코딩 금지)
- 섹션에 <h2 id="...">과 aria-labelledby 필수
- CSS 변수(var(--color-*))를 그대로 쓰고 hex 하드코딩 금지
- 다크 모드는 globals.css의 prefers-color-scheme 블록에 위임

---

## marketing / hero-visual

**역할**: —

**탐지 출처**: visual-reference

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

- 브랜드 기본 규칙을 따릅니다.

### 레퍼런스 근거

- **Primer**: Design digital marketing experiences with Primer Brand UI Shared Foundations

### 구현 노트

- 기존에 같은 역할의 컴포넌트가 있으면 토큰 교체부터 시작
- variant prop으로 시각적 변형을 관리 (하드코딩 금지)
- 섹션에 <h2 id="...">과 aria-labelledby 필수
- CSS 변수(var(--color-*))를 그대로 쓰고 hex 하드코딩 금지
- 다크 모드는 globals.css의 prefers-color-scheme 블록에 위임

---

## marketing / cta-button-group

**역할**: —

**탐지 출처**: visual-reference

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

- 브랜드 기본 규칙을 따릅니다.

### Visual Adaptation Hints

- **cta_prominence**: CTA prominence는 strong이다. 섹션당 primary CTA 1개만 fill/accent로 강하게 띄우고 secondary는 조용하게 후퇴시킨다. (source=cards; confidence=0.82; provenance=inferred; direction=low-elevation tinted cards를 기본으로 하고, 넓은 내부 여백과 강한 section breathing room. soft round corner를 기본값으로 유지.; evidence=surface=tinted, density=airy, corner=round, layout=conversation-panel)

### 레퍼런스 근거

- **Primer**: Design digital marketing experiences with Primer Brand UI Shared Foundations

### 구현 노트

- 기존에 같은 역할의 컴포넌트가 있으면 토큰 교체부터 시작
- variant prop으로 시각적 변형을 관리 (하드코딩 금지)
- 섹션에 <h2 id="...">과 aria-labelledby 필수
- CSS 변수(var(--color-*))를 그대로 쓰고 hex 하드코딩 금지
- 다크 모드는 globals.css의 prefers-color-scheme 블록에 위임

---

## marketing / trust-strip

**역할**: —

**탐지 출처**: visual-reference

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

- 브랜드 기본 규칙을 따릅니다.

### 레퍼런스 근거

- **Primer**: Design digital marketing experiences with Primer Brand UI Shared Foundations

### 구현 노트

- 기존에 같은 역할의 컴포넌트가 있으면 토큰 교체부터 시작
- variant prop으로 시각적 변형을 관리 (하드코딩 금지)
- 섹션에 <h2 id="...">과 aria-labelledby 필수
- CSS 변수(var(--color-*))를 그대로 쓰고 hex 하드코딩 금지
- 다크 모드는 globals.css의 prefers-color-scheme 블록에 위임

---

## layout / resizable-split-pane

**역할**: Resizable two/three-pane workspace shell for dense tools

**Slot archetype**: `advanced:resizable-split-pane`

### Advanced Usage

Use when:
- primary work happens between list, canvas/chat, and detail panels
- users need to compare or inspect adjacent information without navigation
Avoid when:
- single linear form or landing page is enough
Pairs with: thread-list, artifact-preview-panel, inspector-drawer

### 구조 (Anatomy)

- container
- pane
- resize-handle
- collapse-button(optional)
- keyboard-resize affordance

### 상태 (States)

| 상태 | 설명 |
|------|------|
| `default` | 기본 상태 |
| `resizing` | resizing |
| `collapsed` | 접힌 상태 |
| `focus` | 키보드 포커스 시 |

### 토큰 바인딩

```
surface: var(--color-canvas)
pane-surface: var(--color-surface)
divider: var(--color-border)
handle-focus: var(--color-brand-primary)
radius: var(--radius-lg)
gap: var(--space-16)
```

### 접근성

- resize handle uses role="separator" with aria-orientation
- aria-valuemin / aria-valuemax / aria-valuenow describe pane size
- Arrow keys resize focused handle; Enter toggles collapsed state

### 브랜드 적용

- 브랜드 기본 규칙을 따릅니다.

### 레퍼런스 근거

- **Carbon Design System**: The introduction of CSS Grid to build robust layouts on top of the 2x grid A 90% decrease in compilation for Styles from Carbon
- **Primer**: Use LabelGroup to add commonly used margins and other layout constraints to groups of Labels Link

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

- 브랜드 기본 규칙을 따릅니다.

### 구현 노트

- 기존에 같은 역할의 컴포넌트가 있으면 토큰 교체부터 시작
- variant prop으로 시각적 변형을 관리 (하드코딩 금지)

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

- 브랜드 기본 규칙을 따릅니다.

### Visual Adaptation Hints

- **card_elevation_tendency**: 카드는 낮은 elevation만 허용하고 색면 차이로 그룹을 구분한다. 내부 여백은 넉넉하게 두고 card breathing room을 확보한다. (source=cards; confidence=0.82; provenance=inferred; direction=low-elevation tinted cards를 기본으로 하고, 넓은 내부 여백과 강한 section breathing room. soft round corner를 기본값으로 유지.; evidence=surface=tinted, density=airy, corner=round)
- **border_vs_fill_emphasis**: fill 중심이다. tint surface로 성격을 만들고 border는 아주 얇게 보조한다. (source=cards; confidence=0.82; provenance=inferred; direction=low-elevation tinted cards를 기본으로 하고, 넓은 내부 여백과 강한 section breathing room. soft round corner를 기본값으로 유지.; evidence=surface=tinted, density=airy, corner=round)
- **chart_panel_framing**: 차트 패널은 soft tint frame과 restrained divider로 프레이밍한다. 헤더 메타데이터와 본문 visualization 사이의 breathing room을 충분히 둔다. (source=data_display; confidence=0.82; provenance=inferred; direction=정보 밀도를 유지하되 thin dividers와 restrained accent로 hierarchy를 만든다.; evidence=layout=data-review-surface, density=airy, layout=conversation-panel, surface=tinted)

### 구현 노트

- 기존에 같은 역할의 컴포넌트가 있으면 토큰 교체부터 시작
- variant prop으로 시각적 변형을 관리 (하드코딩 금지)
- 빈 상태(empty-state)와 에러 상태를 반드시 처리

---

## data-display / policy-matrix

**역할**: Policy requirement by answer/field matrix with pass, warning, and exception states

**Slot archetype**: `advanced:policy-matrix`

### Advanced Usage

Use when:
- multiple policy rules must be checked against multiple claims or fields
- reviewers need dense scan-and-drill compliance status
Avoid when:
- there is only one policy outcome
Pairs with: risk-summary-card, exception-queue, approval-rail

### 구조 (Anatomy)

- table
- rule-column
- target-column
- status-cell
- evidence-link
- row-action

### 상태 (States)

| 상태 | 설명 |
|------|------|
| `default` | 기본 상태 |
| `filtered` | 필터 적용됨 |
| `sorted` | 정렬 적용됨 |
| `exception` | exception |
| `empty` | 데이터 없음 |

### 토큰 바인딩

```
surface: var(--color-surface)
border: var(--color-border)
pass: var(--color-success)
warning: var(--color-warning)
danger: var(--color-danger)
font: var(--font-body)
```

### 접근성

- caption describes policy scope
- table headers use scope for rows and columns
- status cells include text labels in addition to icons or color

### 브랜드 적용

- 브랜드 기본 규칙을 따릅니다.

### Visual Adaptation Hints

- **card_elevation_tendency**: 카드는 낮은 elevation만 허용하고 색면 차이로 그룹을 구분한다. 내부 여백은 넉넉하게 두고 card breathing room을 확보한다. (source=cards; confidence=0.82; provenance=inferred; direction=low-elevation tinted cards를 기본으로 하고, 넓은 내부 여백과 강한 section breathing room. soft round corner를 기본값으로 유지.; evidence=surface=tinted, density=airy, corner=round)
- **border_vs_fill_emphasis**: fill 중심이다. tint surface로 성격을 만들고 border는 아주 얇게 보조한다. (source=cards; confidence=0.82; provenance=inferred; direction=low-elevation tinted cards를 기본으로 하고, 넓은 내부 여백과 강한 section breathing room. soft round corner를 기본값으로 유지.; evidence=surface=tinted, density=airy, corner=round)
- **chart_panel_framing**: 차트 패널은 soft tint frame과 restrained divider로 프레이밍한다. 헤더 메타데이터와 본문 visualization 사이의 breathing room을 충분히 둔다. (source=data_display; confidence=0.82; provenance=inferred; direction=정보 밀도를 유지하되 thin dividers와 restrained accent로 hierarchy를 만든다.; evidence=layout=data-review-surface, density=airy, layout=conversation-panel, surface=tinted)

### 구현 노트

- 기존에 같은 역할의 컴포넌트가 있으면 토큰 교체부터 시작
- variant prop으로 시각적 변형을 관리 (하드코딩 금지)
- 빈 상태(empty-state)와 에러 상태를 반드시 처리

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

- 브랜드 기본 규칙을 따릅니다.

### Visual Adaptation Hints

- **card_elevation_tendency**: 카드는 낮은 elevation만 허용하고 색면 차이로 그룹을 구분한다. 내부 여백은 넉넉하게 두고 card breathing room을 확보한다. (source=cards; confidence=0.82; provenance=inferred; direction=low-elevation tinted cards를 기본으로 하고, 넓은 내부 여백과 강한 section breathing room. soft round corner를 기본값으로 유지.; evidence=surface=tinted, density=airy, corner=round)
- **border_vs_fill_emphasis**: fill 중심이다. tint surface로 성격을 만들고 border는 아주 얇게 보조한다. (source=cards; confidence=0.82; provenance=inferred; direction=low-elevation tinted cards를 기본으로 하고, 넓은 내부 여백과 강한 section breathing room. soft round corner를 기본값으로 유지.; evidence=surface=tinted, density=airy, corner=round)

### 구현 노트

- 기존에 같은 역할의 컴포넌트가 있으면 토큰 교체부터 시작
- variant prop으로 시각적 변형을 관리 (하드코딩 금지)

---

## data-display / audit-timeline

**역할**: Chronological audit trail with actor, action, timestamp, and linked artifact

**Slot archetype**: `advanced:audit-timeline`

### Advanced Usage

Use when:
- regulated workflows require traceable user and AI actions
- reviewers need to reconstruct what happened before approval
Avoid when:
- events are not user-facing or not actionable
Pairs with: decision-record-card, approval-rail, tool-call-trace

### 구조 (Anatomy)

- list
- event-item
- timestamp
- actor
- event-summary
- artifact-link

### 상태 (States)

| 상태 | 설명 |
|------|------|
| `default` | 기본 상태 |
| `filtered` | 필터 적용됨 |
| `expanded` | expanded |
| `empty` | 데이터 없음 |

### 토큰 바인딩

```
surface: var(--color-surface)
border: var(--color-border)
timestamp: var(--color-brand-primary)
muted: var(--color-text-muted)
mono: var(--font-mono)
```

### 접근성

- timeline is an ordered list when chronology matters
- timestamps use machine-readable datetime when possible
- expanded details are reachable by keyboard

### 브랜드 적용

- 브랜드 기본 규칙을 따릅니다.

### Visual Adaptation Hints

- **card_elevation_tendency**: 카드는 낮은 elevation만 허용하고 색면 차이로 그룹을 구분한다. 내부 여백은 넉넉하게 두고 card breathing room을 확보한다. (source=cards; confidence=0.82; provenance=inferred; direction=low-elevation tinted cards를 기본으로 하고, 넓은 내부 여백과 강한 section breathing room. soft round corner를 기본값으로 유지.; evidence=surface=tinted, density=airy, corner=round)
- **border_vs_fill_emphasis**: fill 중심이다. tint surface로 성격을 만들고 border는 아주 얇게 보조한다. (source=cards; confidence=0.82; provenance=inferred; direction=low-elevation tinted cards를 기본으로 하고, 넓은 내부 여백과 강한 section breathing room. soft round corner를 기본값으로 유지.; evidence=surface=tinted, density=airy, corner=round)
- **chart_panel_framing**: 차트 패널은 soft tint frame과 restrained divider로 프레이밍한다. 헤더 메타데이터와 본문 visualization 사이의 breathing room을 충분히 둔다. (source=data_display; confidence=0.82; provenance=inferred; direction=정보 밀도를 유지하되 thin dividers와 restrained accent로 hierarchy를 만든다.; evidence=layout=data-review-surface, density=airy, layout=conversation-panel, surface=tinted)

### 구현 노트

- 기존에 같은 역할의 컴포넌트가 있으면 토큰 교체부터 시작
- variant prop으로 시각적 변형을 관리 (하드코딩 금지)
- 빈 상태(empty-state)와 에러 상태를 반드시 처리

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

- 브랜드 기본 규칙을 따릅니다.

### 레퍼런스 근거

- **Carbon Design System**: AI chat is a conversational framework between a user and an AI that can aid in creating tasks, finding insights, tracking documents, and more. For ...
- **Primer**: The GitHub Design Infrastructure and Design Engineering teams build and maintain Primer — this includes our CSS framework, style guide documentatio...

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

- 브랜드 기본 규칙을 따릅니다.

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

- 브랜드 기본 규칙을 따릅니다.

### 레퍼런스 근거

- **Carbon Design System**: Bringing IBM Carbon Design System Knowledge Into AI Workflows With Carbon MCP Will Scott, PhD
- **Primer**: Design guidelines covering common user workflows. Octicons

### 구현 노트

- 기존에 같은 역할의 컴포넌트가 있으면 토큰 교체부터 시작
- variant prop으로 시각적 변형을 관리 (하드코딩 금지)

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

- 브랜드 기본 규칙을 따릅니다.

### Visual Adaptation Hints

- **card_elevation_tendency**: 카드는 낮은 elevation만 허용하고 색면 차이로 그룹을 구분한다. 내부 여백은 넉넉하게 두고 card breathing room을 확보한다. (source=cards; confidence=0.82; provenance=inferred; direction=low-elevation tinted cards를 기본으로 하고, 넓은 내부 여백과 강한 section breathing room. soft round corner를 기본값으로 유지.; evidence=surface=tinted, density=airy, corner=round)
- **border_vs_fill_emphasis**: fill 중심이다. tint surface로 성격을 만들고 border는 아주 얇게 보조한다. (source=cards; confidence=0.82; provenance=inferred; direction=low-elevation tinted cards를 기본으로 하고, 넓은 내부 여백과 강한 section breathing room. soft round corner를 기본값으로 유지.; evidence=surface=tinted, density=airy, corner=round)
- **chart_panel_framing**: 차트 패널은 soft tint frame과 restrained divider로 프레이밍한다. 헤더 메타데이터와 본문 visualization 사이의 breathing room을 충분히 둔다. (source=data_display; confidence=0.82; provenance=inferred; direction=정보 밀도를 유지하되 thin dividers와 restrained accent로 hierarchy를 만든다.; evidence=layout=data-review-surface, density=airy, layout=conversation-panel, surface=tinted)

### 구현 노트

- 기존에 같은 역할의 컴포넌트가 있으면 토큰 교체부터 시작
- variant prop으로 시각적 변형을 관리 (하드코딩 금지)
- 빈 상태(empty-state)와 에러 상태를 반드시 처리

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

- 브랜드 기본 규칙을 따릅니다.

### 레퍼런스 근거

- **Primer**: ActionMenu is composed of ActionList and Overlay patterns used for quick actions and selections. AnchoredOverlay

### 구현 노트

- 기존에 같은 역할의 컴포넌트가 있으면 토큰 교체부터 시작
- variant prop으로 시각적 변형을 관리 (하드코딩 금지)
- Escape / backdrop click으로 닫기, 열 때 첫 focusable 요소로 이동

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

- 브랜드 기본 규칙을 따릅니다.

### 레퍼런스 근거

- **Carbon Design System**: Number input Text input
- **Primer**: I worked in data visualization and map-making for most of my career, and solving design problems with data is my jam. To me there's something uniqu...

### 구현 노트

- 기존에 같은 역할의 컴포넌트가 있으면 토큰 교체부터 시작
- variant prop으로 시각적 변형을 관리 (하드코딩 금지)
- error 상태에서 helper text → error message로 자동 전환
- label은 항상 visible (placeholder만으로 대체 금지)
