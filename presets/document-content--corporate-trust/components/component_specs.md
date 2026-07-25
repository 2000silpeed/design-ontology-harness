# EKOS Knowledge Intake Component Specs

총 24개 컴포넌트 | 패밀리: approval, concept-proposal, evidence, fact-review, feedback-and-empty-states, intake-input, knowledge-detail, link-workspace, navigation, operations, progress-and-failure, search

## 구현 원칙 (Non-negotiable)

이 스펙의 모든 컴포넌트를 구현할 때 반드시 지킨다:

1. **이모지를 UI로 쓰지 않는다** — 🎨 ✅ 🔥 ⚡ 🚀 ❌ ⭐ 📊 등 이모지를 아이콘, 상태 표시, 버튼 장식, 네비게이션 지표 자리에 절대 넣지 않는다. 리팩토링 중 카드/버튼/배지/탭/상태 UI에서 이모지를 발견하면 SVG 파일, SVG 컴포넌트, 또는 Lucide/Heroicons/Phosphor/Tabler 같은 아이콘 라이브러리로 교체한다.
2. **컴포넌트를 직접 구현한다** — 아래 각 컴포넌트의 anatomy(구조), states(상태), 토큰 바인딩, 접근성 규칙을 그대로 따라 완전하게 구현한다. '임시', 'TODO', '플레이스홀더' 같은 반쪽 구현을 남기지 않는다.
3. **라이브러리 기본 스타일 금지** — 라이브러리 컴포넌트를 그대로 import해서 쓰지 않는다. 반드시 디자인 토큰(--color-*, --space-*, --radius-*, --font-*)으로 스타일을 명시적으로 바인딩한다.
4. **접근성은 옵션이 아니다** — 각 컴포넌트의 '접근성' 섹션에 정의된 role, aria-*, label, focus 관리 규칙을 전부 적용한다.
5. **hex 값 하드코딩 금지** — 색상은 반드시 semantic token을 경유한다 (예: `color: var(--ds-color-ink)` not `color: #2C2C2C`).
6. **모바일 overflow 금지** — 버튼, CTA, 탭, 필터칩, 툴바 액션은 320px viewport에서 화면 밖으로 나가면 안 된다. fixed/min-width px 값으로 폭을 고정하지 말고 wrap/stack fallback을 제공한다.

## 브랜드 적용 규칙

- **hover**: 예측 가능하고 일관된 hover 패턴 + opacity 변화 (0.08-0.12), elevation 변화 없음
- **motion**: 모든 전환에 동일한 easing/duration + 150-200ms ease-out, bounce/spring 없음
- **color**: 안정적인 neutral 기반, 과한 accent 변화 없음 + 중성 톤 위주, accent는 최소한으로
- **density**: 기존 레이아웃 유지, 갑작스런 위치 변경 없음 + comfortable 모드 기본, 여유로운 padding
- **feedback**: 결과를 반드시 확인, 실패 시 복구 방법 안내 + subtle inline alert 선호, 과한 컬러 블록 지양

## Visual-reference 적용 원칙

- anatomy / states / accessibility는 설계서(spec)와 KB 근거를 유지하고, visual adaptation은 elevation / framing / prominence / density 같은 표현 계층에만 advisory signal로 적용한다.
- Active visual signals: surface_style=tinted, density=airy, corner_style=medium, top_layout_cue=data-review-surface
- Connected component hints: cards, data_display, navigation, typography

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

## navigation / left-nav

**역할**: 홈/검색/지식 추가/검토함/영향과 원인/관리 6항목 좌측 메뉴

**Component contract**: `component-contract/v1` / `complete` / provenance `llm-authored`

**Domain primitive**: workspace navigation

**탐지 출처**: llm-authored-component-decision

### 구조 (Anatomy)

- nav-rail
- nav-item
- nav-label
- active-indicator

### 상태 (States)

| 상태 | 설명 |
|------|------|
| `default` | 기본 상태 |
| `active` | 클릭/탭 중 |
| `keyboard-focus` | keyboard-focus |
| `collapsed` | 접힌 상태 |

### 구조화된 구현 계약

- Props: `{'state': {'type': 'enum', 'values': ['default', 'active', 'keyboard-focus', 'collapsed'], 'required': False, 'default': 'default'}, 'data': {'type': 'domain-object', 'object': 'workspace navigation', 'required': True}}`
- Variants: `{'axes': [], 'default': 'default', 'constraints': ['Only variants declared by this contract may be implemented.']}`
- Interaction: `{'events': ['navigate', 'toggle-collapse'], 'state_transitions': [], 'focus_behavior': 'Preserve visible focus and logical DOM order.', 'state_coverage': ['default', 'active', 'keyboard-focus', 'collapsed']}`
- Data: `{'domain_object': 'workspace navigation', 'required_fields': ['menu_items', 'active_item', 'permissions'], 'provenance_required': False, 'empty_state_required': True}`
- Responsive: `{'required_widths_px': [320, 360, 390, 430, 768, 1024, 1440], 'control_rules': ['Buttons, CTA groups, tabs, filter chips, and toolbar actions must not rely on fixed px widths or mobile-hostile min-width values.', 'Every button-like control needs max-inline-size: 100%; controls inside flex/grid parents need min-inline-size: 0 so labels can shrink or wrap.', 'Action rows must wrap or stack at narrow widths; two-button rows need a <=480px fallback before implementation is complete.', 'Long Korean CTA labels must be tested with real copy. Prefer wrapping/stacking over clipping, overflow hidden, or forcing white-space: nowrap.', 'Horizontal rails, tickers, score strips, and carousels must not reveal partially clipped text. Either size cards so visible items are complete, or use compact labels such as icon+code in the rail and move full names to the detailed surface.', 'Do not use width: 100vw inside padded containers; it commonly creates horizontal scroll. Use width: 100%, max-width: 100%, or a documented full-bleed pattern.', 'Never hide body overflow-x as the fix for a layout bug; remove the overflowing width/min-width instead.'], 'container_behavior': 'wrap, stack, or reflow without hiding product state'}`
- Content rules: 메뉴 라벨은 업무 어휘만 사용한다: 홈·검색·지식 추가·검토함·영향과 원인·관리; 내부 기술 어휘(ontology·graph·Pack)를 라벨에 쓰지 않는다

### 토큰 바인딩

```
component.container.background: var(--ds-color-surface-muted)
part.nav-item.color: var(--ds-color-ink-muted)
part.nav-label.font-family: var(--ds-font-body)
part.active-indicator.background: var(--ds-color-primary)
state.active.color: var(--ds-color-primary)
state.keyboard-focus.outline: 2px solid var(--ds-color-link)
```

### 접근성

- nav landmark (role="navigation")
- aria-current="page" for active item
- 키보드 화살표 탐색 지원
- nav landmark와 aria-current로 현재 위치를 보조기기에 알린다
- 모든 항목을 Tab과 화살표 키로 이동할 수 있다

### 브랜드 적용

- [trustworthy+calm] hover: 예측 가능하고 일관된 hover 패턴 + opacity 변화 (0.08-0.12), elevation 변화 없음
- [trustworthy+calm] density: 기존 레이아웃 유지, 갑작스런 위치 변경 없음 + comfortable 모드 기본, 여유로운 padding
- [trustworthy+calm] motion: 모든 전환에 동일한 easing/duration + 150-200ms ease-out, bounce/spring 없음

### Visual Adaptation Hints

- **filter_nav_density**: filter/nav density는 compact하다. chip, scope, pagination을 촘촘하게 묶되 의미 단위별 group은 분리한다. (source=navigation; confidence=0.26; provenance=inferred; direction=고정 sidebar 또는 split-pane navigation을 우선하고, 현재 위치와 scope를 항상 명시한다.; evidence=Split-pane workspace, layout=data-review-surface, density=airy)

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

---

## search / global-search-input

**역할**: 업무 질문·찾을 내용을 받는 대형 통합 검색

**Component contract**: `component-contract/v1` / `complete` / provenance `llm-authored`

**Domain primitive**: 통합 검색

**탐지 출처**: llm-authored-component-decision

### 구조 (Anatomy)

- input-field
- placeholder
- search-icon
- results-popover

### 상태 (States)

| 상태 | 설명 |
|------|------|
| `empty` | 데이터 없음 |
| `typing` | typing |
| `results` | results |
| `no-results` | no-results |
| `keyboard-focus` | keyboard-focus |

### 구조화된 구현 계약

- Props: `{'state': {'type': 'enum', 'values': ['empty', 'typing', 'results', 'no-results', 'keyboard-focus'], 'required': False, 'default': 'empty'}, 'data': {'type': 'domain-object', 'object': '통합 검색', 'required': True}}`
- Variants: `{'axes': [], 'default': 'empty', 'constraints': ['Only variants declared by this contract may be implemented.']}`
- Interaction: `{'events': ['input', 'submit', 'select-result', 'clear'], 'state_transitions': [], 'focus_behavior': 'Preserve visible focus and logical DOM order.', 'state_coverage': ['empty', 'typing', 'results', 'no-results', 'keyboard-focus']}`
- Data: `{'domain_object': '통합 검색', 'required_fields': ['query', 'results', 'result_status'], 'provenance_required': False, 'empty_state_required': True}`
- Responsive: `{'required_widths_px': [320, 360, 390, 430, 768, 1024, 1440], 'control_rules': ['Buttons, CTA groups, tabs, filter chips, and toolbar actions must not rely on fixed px widths or mobile-hostile min-width values.', 'Every button-like control needs max-inline-size: 100%; controls inside flex/grid parents need min-inline-size: 0 so labels can shrink or wrap.', 'Action rows must wrap or stack at narrow widths; two-button rows need a <=480px fallback before implementation is complete.', 'Long Korean CTA labels must be tested with real copy. Prefer wrapping/stacking over clipping, overflow hidden, or forcing white-space: nowrap.', 'Horizontal rails, tickers, score strips, and carousels must not reveal partially clipped text. Either size cards so visible items are complete, or use compact labels such as icon+code in the rail and move full names to the detailed surface.', 'Do not use width: 100vw inside padded containers; it commonly creates horizontal scroll. Use width: 100%, max-width: 100%, or a documented full-bleed pattern.', 'Never hide body overflow-x as the fix for a layout bug; remove the overflowing width/min-width instead.'], 'container_behavior': 'wrap, stack, or reflow without hiding product state'}`
- Content rules: placeholder는 '업무 질문이나 찾을 내용을 입력하세요'로 고정한다; 결과 없음 문구는 다음 행동(지식 추가)을 제안한다

### 토큰 바인딩

```
component.container.border: 1px solid var(--ds-color-border)
part.input-field.font-family: var(--ds-font-body)
part.placeholder.color: var(--ds-color-ink-subtle)
part.results-popover.background: var(--ds-color-surface-elevated)
state.keyboard-focus.border-color: var(--ds-color-link)
state.no-results.color: var(--ds-color-ink-muted)
```

### 접근성

- 상호작용 카드/행은 <a> 또는 <button>으로 구현
- 선택 상태는 aria-selected 또는 aria-pressed로 노출
- 장식용 elevation만으로 계층을 만들지 않고 heading/label을 제공
- combobox 패턴(aria-expanded, aria-activedescendant)을 따른다
- 결과 갱신을 aria-live로 알린다

### 브랜드 적용

- [trustworthy+calm] hover: 예측 가능하고 일관된 hover 패턴 + opacity 변화 (0.08-0.12), elevation 변화 없음
- [trustworthy+calm] motion: 모든 전환에 동일한 easing/duration + 150-200ms ease-out, bounce/spring 없음
- [trustworthy+calm] color: 안정적인 neutral 기반, 과한 accent 변화 없음 + 중성 톤 위주, accent는 최소한으로

### Visual Adaptation Hints

- **filter_nav_density**: filter/nav density는 compact하다. chip, scope, pagination을 촘촘하게 묶되 의미 단위별 group은 분리한다. (source=navigation; confidence=0.26; provenance=inferred; direction=고정 sidebar 또는 split-pane navigation을 우선하고, 현재 위치와 scope를 항상 명시한다.; evidence=Split-pane workspace, layout=data-review-surface, density=airy)

### 레퍼런스 근거

- **Carbon Design System**: Carbon puts the user first. Using rigorous research into users’ needs and desires, Carbon is laser-focused on real people. Carbon builds consistenc...
- **Primer**: More than anything, the people I’ve worked with over the years. I learned something from everyone: being generous with my knowledge, being serious ...

### 구현 노트

- 기존에 같은 역할의 컴포넌트가 있으면 토큰 교체부터 시작
- variant prop으로 시각적 변형을 관리 (하드코딩 금지)
- 애니메이션은 상태 설명용으로만 사용, 장식 효과 금지

---

## intake-input / intake-method-list

**역할**: 직접 설명/자료 올리기/SAP 가져오기/시스템 연결의 큰 선택 목록

**Component contract**: `component-contract/v1` / `complete` / provenance `llm-authored`

**Domain primitive**: 지식 추가 첫 선택

**탐지 출처**: llm-authored-component-decision

### 구조 (Anatomy)

- method-row
- method-icon
- method-title
- method-description

### 상태 (States)

| 상태 | 설명 |
|------|------|
| `default` | 기본 상태 |
| `hover` | 마우스 오버 시 |
| `keyboard-focus` | keyboard-focus |
| `disabled-by-permission` | disabled-by-permission |

### 구조화된 구현 계약

- Props: `{'state': {'type': 'enum', 'values': ['default', 'hover', 'keyboard-focus', 'disabled-by-permission'], 'required': False, 'default': 'default'}, 'data': {'type': 'domain-object', 'object': '지식 추가 첫 선택', 'required': True}}`
- Variants: `{'axes': [], 'default': 'default', 'constraints': ['Only variants declared by this contract may be implemented.']}`
- Interaction: `{'events': ['select-method', 'focus-method'], 'state_transitions': [], 'focus_behavior': 'Preserve visible focus and logical DOM order.', 'state_coverage': ['default', 'hover', 'keyboard-focus', 'disabled-by-permission']}`
- Data: `{'domain_object': '지식 추가 첫 선택', 'required_fields': ['methods', 'permissions'], 'provenance_required': False, 'empty_state_required': True}`
- Responsive: `{'required_widths_px': [320, 360, 390, 430, 768, 1024, 1440], 'control_rules': ['Buttons, CTA groups, tabs, filter chips, and toolbar actions must not rely on fixed px widths or mobile-hostile min-width values.', 'Every button-like control needs max-inline-size: 100%; controls inside flex/grid parents need min-inline-size: 0 so labels can shrink or wrap.', 'Action rows must wrap or stack at narrow widths; two-button rows need a <=480px fallback before implementation is complete.', 'Long Korean CTA labels must be tested with real copy. Prefer wrapping/stacking over clipping, overflow hidden, or forcing white-space: nowrap.', 'Horizontal rails, tickers, score strips, and carousels must not reveal partially clipped text. Either size cards so visible items are complete, or use compact labels such as icon+code in the rail and move full names to the detailed surface.', 'Do not use width: 100vw inside padded containers; it commonly creates horizontal scroll. Use width: 100%, max-width: 100%, or a documented full-bleed pattern.', 'Never hide body overflow-x as the fix for a layout bug; remove the overflowing width/min-width instead.'], 'container_behavior': 'wrap, stack, or reflow without hiding product state'}`
- Content rules: 각 방식은 이름 + 한 줄 설명 + 예시를 함께 보여준다; 방식 이름은 행동형 동사구(직접 설명하기, 자료 올리기)로 쓴다

### 토큰 바인딩

```
part.method-row.background: var(--ds-color-surface)
part.method-title.color: var(--ds-color-ink)
part.method-description.color: var(--ds-color-ink-muted)
state.hover.background: var(--ds-color-surface-muted)
state.keyboard-focus.outline: 2px solid var(--ds-color-link)
state.disabled-by-permission.color: var(--ds-color-ink-subtle)
```

### 접근성

- 상호작용 카드/행은 <a> 또는 <button>으로 구현
- 선택 상태는 aria-selected 또는 aria-pressed로 노출
- 장식용 elevation만으로 계층을 만들지 않고 heading/label을 제공
- 목록은 단일 Tab 스톱 + 화살표 탐색으로 조작한다
- 비활성 사유를 aria-describedby로 제공한다

### 브랜드 적용

- [trustworthy+calm] hover: 예측 가능하고 일관된 hover 패턴 + opacity 변화 (0.08-0.12), elevation 변화 없음
- [trustworthy+calm] motion: 모든 전환에 동일한 easing/duration + 150-200ms ease-out, bounce/spring 없음
- [trustworthy+calm] color: 안정적인 neutral 기반, 과한 accent 변화 없음 + 중성 톤 위주, accent는 최소한으로

### 구현 노트

- 기존에 같은 역할의 컴포넌트가 있으면 토큰 교체부터 시작
- variant prop으로 시각적 변형을 관리 (하드코딩 금지)
- 애니메이션은 상태 설명용으로만 사용, 장식 효과 금지

---

## intake-input / describe-composer

**역할**: 자유문장 대형 입력창 + 도움 틀 칩 + 유도 질문 줄

**Component contract**: `component-contract/v1` / `complete` / provenance `llm-authored`

**Domain primitive**: 직접 설명하기

**탐지 출처**: llm-authored-component-decision

### 구조 (Anatomy)

- textarea
- help-frame-chips
- guided-question-strip
- submit-button

### 상태 (States)

| 상태 | 설명 |
|------|------|
| `empty` | 데이터 없음 |
| `with-help-frame` | with-help-frame |
| `with-guided-questions` | with-guided-questions |
| `filled` | 값이 입력된 상태 |
| `submitting` | submitting |

### 구조화된 구현 계약

- Props: `{'state': {'type': 'enum', 'values': ['empty', 'with-help-frame', 'with-guided-questions', 'filled', 'submitting'], 'required': False, 'default': 'empty'}, 'data': {'type': 'domain-object', 'object': '직접 설명하기', 'required': True}}`
- Variants: `{'axes': [], 'default': 'empty', 'constraints': ['Only variants declared by this contract may be implemented.']}`
- Interaction: `{'events': ['input', 'select-help-frame', 'submit', 'cancel'], 'state_transitions': [], 'focus_behavior': 'Preserve visible focus and logical DOM order.', 'state_coverage': ['empty', 'with-help-frame', 'with-guided-questions', 'filled', 'submitting']}`
- Data: `{'domain_object': '직접 설명하기', 'required_fields': ['draft_text', 'help_frame', 'submit_state'], 'provenance_required': False, 'empty_state_required': True}`
- Responsive: `{'required_widths_px': [320, 360, 390, 430, 768, 1024, 1440], 'control_rules': ['Buttons, CTA groups, tabs, filter chips, and toolbar actions must not rely on fixed px widths or mobile-hostile min-width values.', 'Every button-like control needs max-inline-size: 100%; controls inside flex/grid parents need min-inline-size: 0 so labels can shrink or wrap.', 'Action rows must wrap or stack at narrow widths; two-button rows need a <=480px fallback before implementation is complete.', 'Long Korean CTA labels must be tested with real copy. Prefer wrapping/stacking over clipping, overflow hidden, or forcing white-space: nowrap.', 'Horizontal rails, tickers, score strips, and carousels must not reveal partially clipped text. Either size cards so visible items are complete, or use compact labels such as icon+code in the rail and move full names to the detailed surface.', 'Do not use width: 100vw inside padded containers; it commonly creates horizontal scroll. Use width: 100%, max-width: 100%, or a documented full-bleed pattern.', 'Never hide body overflow-x as the fix for a layout bug; remove the overflowing width/min-width instead.'], 'container_behavior': 'wrap, stack, or reflow without hiding product state'}`
- Content rules: 도움 틀은 제안일 뿐이며 자유문장 입력을 강제 필드로 바꾸지 않는다; 업무 규칙 선택 시 유도 질문 3종을 입력창 위에 짧게 표시한다

### 토큰 바인딩

```
part.textarea.background: var(--ds-color-surface)
part.help-frame-chips.background: var(--ds-color-surface-tint)
part.guided-question-strip.color: var(--ds-color-ink-muted)
part.submit-button.background: var(--ds-color-primary)
state.with-guided-questions.border-color: var(--ds-color-info)
state.submitting.background: var(--ds-color-surface-muted)
```

### 접근성

- 상호작용 카드/행은 <a> 또는 <button>으로 구현
- 선택 상태는 aria-selected 또는 aria-pressed로 노출
- 장식용 elevation만으로 계층을 만들지 않고 heading/label을 제공
- textarea에 레이블과 안내를 연결한다
- 한글 IME 조합 중 Enter 제출을 방지한다

### 브랜드 적용

- [trustworthy+calm] hover: 예측 가능하고 일관된 hover 패턴 + opacity 변화 (0.08-0.12), elevation 변화 없음
- [trustworthy+calm] motion: 모든 전환에 동일한 easing/duration + 150-200ms ease-out, bounce/spring 없음
- [trustworthy+calm] color: 안정적인 neutral 기반, 과한 accent 변화 없음 + 중성 톤 위주, accent는 최소한으로

### 구현 노트

- 기존에 같은 역할의 컴포넌트가 있으면 토큰 교체부터 시작
- variant prop으로 시각적 변형을 관리 (하드코딩 금지)
- 애니메이션은 상태 설명용으로만 사용, 장식 효과 금지

---

## intake-input / upload-manifest-card

**역할**: 파일 메타(이름·형식·크기·보안 범위) + 원문 보존/비공식/격리 3줄 안내

**Component contract**: `component-contract/v1` / `complete` / provenance `llm-authored`

**Domain primitive**: 자료 올리기

**탐지 출처**: llm-authored-component-decision

**Slot archetype**: `surface-card`

### 구조 (Anatomy)

- file-meta
- trust-notice
- progress-line
- action-row

### 상태 (States)

| 상태 | 설명 |
|------|------|
| `pending` | pending |
| `uploading` | uploading |
| `uploaded` | uploaded |
| `sensitive-quarantine-warning` | sensitive-quarantine-warning |
| `failed` | failed |

### 구조화된 구현 계약

- Props: `{'state': {'type': 'enum', 'values': ['pending', 'uploading', 'uploaded', 'sensitive-quarantine-warning', 'failed'], 'required': False, 'default': 'pending'}, 'data': {'type': 'domain-object', 'object': '자료 올리기', 'required': True}}`
- Variants: `{'axes': [], 'default': 'pending', 'constraints': ['Only variants declared by this contract may be implemented.']}`
- Interaction: `{'events': ['select-file', 'upload', 'cancel-upload', 'retry'], 'state_transitions': [], 'focus_behavior': 'Preserve visible focus and logical DOM order.', 'state_coverage': ['pending', 'uploading', 'uploaded', 'sensitive-quarantine-warning', 'failed']}`
- Data: `{'domain_object': '자료 올리기', 'required_fields': ['file_name', 'file_type', 'file_size', 'security_scope', 'upload_state'], 'provenance_required': False, 'empty_state_required': True}`
- Responsive: `{'required_widths_px': [320, 360, 390, 430, 768, 1024, 1440], 'control_rules': ['Buttons, CTA groups, tabs, filter chips, and toolbar actions must not rely on fixed px widths or mobile-hostile min-width values.', 'Every button-like control needs max-inline-size: 100%; controls inside flex/grid parents need min-inline-size: 0 so labels can shrink or wrap.', 'Action rows must wrap or stack at narrow widths; two-button rows need a <=480px fallback before implementation is complete.', 'Long Korean CTA labels must be tested with real copy. Prefer wrapping/stacking over clipping, overflow hidden, or forcing white-space: nowrap.', 'Horizontal rails, tickers, score strips, and carousels must not reveal partially clipped text. Either size cards so visible items are complete, or use compact labels such as icon+code in the rail and move full names to the detailed surface.', 'Do not use width: 100vw inside padded containers; it commonly creates horizontal scroll. Use width: 100%, max-width: 100%, or a documented full-bleed pattern.', 'Never hide body overflow-x as the fix for a layout bug; remove the overflowing width/min-width instead.'], 'container_behavior': 'wrap, stack, or reflow without hiding product state'}`
- Content rules: 원문 보존·자동 공식화 없음·민감정보 격리 가능 3줄 안내를 업로드 전에 보여준다; 파일 메타는 이름·형식·크기·보안 범위 순으로 표기한다

### 토큰 바인딩

```
part.file-meta.font-family: var(--ds-font-mono)
part.trust-notice.color: var(--ds-color-ink-muted)
part.progress-line.background: var(--ds-color-info)
part.action-row.color: var(--ds-color-link)
state.sensitive-quarantine-warning.border-color: var(--ds-color-warning)
state.failed.color: var(--ds-color-danger)
state.uploaded.color: var(--ds-color-success)
```

### 접근성

- 카드 자체가 링크/버튼이면 <a>/<button> 래퍼 사용
- 장식적 카드는 단순 <article> 또는 <div>
- 업로드 진행을 aria-live=polite로 알린다
- 실패 사유를 색이 아닌 텍스트로 제공한다

### 브랜드 적용

- [trustworthy+calm] hover: 예측 가능하고 일관된 hover 패턴 + opacity 변화 (0.08-0.12), elevation 변화 없음
- [trustworthy+calm] motion: 모든 전환에 동일한 easing/duration + 150-200ms ease-out, bounce/spring 없음
- [trustworthy+calm] color: 안정적인 neutral 기반, 과한 accent 변화 없음 + 중성 톤 위주, accent는 최소한으로

### Visual Adaptation Hints

- **card_elevation_tendency**: 카드는 낮은 elevation만 허용하고 색면 차이로 그룹을 구분한다. 내부 여백은 넉넉하게 두고 card breathing room을 확보한다. (source=cards; confidence=0.19; provenance=inferred; direction=low-elevation tinted cards를 기본으로 하고, 넓은 내부 여백과 강한 section breathing room. 중간 반경으로 제품 UI 절제 유지.; evidence=surface=tinted, density=airy, corner=medium)
- **border_vs_fill_emphasis**: fill 중심이다. tint surface로 성격을 만들고 border는 아주 얇게 보조한다. (source=cards; confidence=0.19; provenance=inferred; direction=low-elevation tinted cards를 기본으로 하고, 넓은 내부 여백과 강한 section breathing room. 중간 반경으로 제품 UI 절제 유지.; evidence=surface=tinted, density=airy, corner=medium)

### 구현 노트

- 기존에 같은 역할의 컴포넌트가 있으면 토큰 교체부터 시작
- variant prop으로 시각적 변형을 관리 (하드코딩 금지)
- 애니메이션은 상태 설명용으로만 사용, 장식 효과 금지

---

## progress-and-failure / analysis-stage-list

**역할**: 원문 보관→읽기→비교→확인 탐지→초안 준비 5단계 문장형 진행 표시

**Component contract**: `component-contract/v1` / `complete` / provenance `llm-authored`

**Domain primitive**: 분석 진행

**탐지 출처**: llm-authored-component-decision

### 구조 (Anatomy)

- stage-row
- stage-sentence
- stage-marker
- cancel-note

### 상태 (States)

| 상태 | 설명 |
|------|------|
| `stage-done` | stage-done |
| `stage-active` | stage-active |
| `stage-pending` | stage-pending |
| `cancelled` | cancelled |
| `background` | background |

### 구조화된 구현 계약

- Props: `{'state': {'type': 'enum', 'values': ['stage-done', 'stage-active', 'stage-pending', 'cancelled', 'background'], 'required': False, 'default': 'stage-done'}, 'data': {'type': 'domain-object', 'object': '분석 진행', 'required': True}}`
- Variants: `{'axes': [], 'default': 'stage-done', 'constraints': ['Only variants declared by this contract may be implemented.']}`
- Interaction: `{'events': ['cancel', 'move-to-background', 'stage-change'], 'state_transitions': [], 'focus_behavior': 'Preserve visible focus and logical DOM order.', 'state_coverage': ['stage-done', 'stage-active', 'stage-pending', 'cancelled', 'background']}`
- Data: `{'domain_object': '분석 진행', 'required_fields': ['stages', 'current_stage', 'cancellable'], 'provenance_required': False, 'empty_state_required': True}`
- Responsive: `{'required_widths_px': [320, 360, 390, 430, 768, 1024, 1440], 'control_rules': ['Buttons, CTA groups, tabs, filter chips, and toolbar actions must not rely on fixed px widths or mobile-hostile min-width values.', 'Every button-like control needs max-inline-size: 100%; controls inside flex/grid parents need min-inline-size: 0 so labels can shrink or wrap.', 'Action rows must wrap or stack at narrow widths; two-button rows need a <=480px fallback before implementation is complete.', 'Long Korean CTA labels must be tested with real copy. Prefer wrapping/stacking over clipping, overflow hidden, or forcing white-space: nowrap.', 'Horizontal rails, tickers, score strips, and carousels must not reveal partially clipped text. Either size cards so visible items are complete, or use compact labels such as icon+code in the rail and move full names to the detailed surface.', 'Do not use width: 100vw inside padded containers; it commonly creates horizontal scroll. Use width: 100%, max-width: 100%, or a documented full-bleed pattern.', 'Never hide body overflow-x as the fix for a layout bug; remove the overflowing width/min-width instead.'], 'container_behavior': 'wrap, stack, or reflow without hiding product state'}`
- Content rules: 5단계 각각을 완료/진행/대기 문장으로 표시한다; 취소 시 원문 보존 여부를 알려준다

### 토큰 바인딩

```
part.stage-sentence.color: var(--ds-color-ink)
part.stage-marker.background: var(--ds-color-info)
part.cancel-note.color: var(--ds-color-ink-muted)
state.stage-done.color: var(--ds-color-success)
state.stage-pending.color: var(--ds-color-ink-subtle)
state.cancelled.color: var(--ds-color-warning)
```

### 접근성

- 상호작용 카드/행은 <a> 또는 <button>으로 구현
- 선택 상태는 aria-selected 또는 aria-pressed로 노출
- 장식용 elevation만으로 계층을 만들지 않고 heading/label을 제공
- 진행 변경을 aria-live로 알린다
- 회전 표시를 단독으로 쓰지 않고 항상 텍스트를 병기한다

### 브랜드 적용

- [trustworthy+calm] hover: 예측 가능하고 일관된 hover 패턴 + opacity 변화 (0.08-0.12), elevation 변화 없음
- [trustworthy+calm] motion: 모든 전환에 동일한 easing/duration + 150-200ms ease-out, bounce/spring 없음
- [trustworthy+calm] color: 안정적인 neutral 기반, 과한 accent 변화 없음 + 중성 톤 위주, accent는 최소한으로

### 구현 노트

- 기존에 같은 역할의 컴포넌트가 있으면 토큰 교체부터 시작
- variant prop으로 시각적 변형을 관리 (하드코딩 금지)
- 애니메이션은 상태 설명용으로만 사용, 장식 효과 금지

---

## progress-and-failure / analysis-failure-panel

**역할**: 실패 파일·구간 + 다시 시도/항목 제외/직접 작성/운영 이관 4행동 + 기술 예외 접기

**Component contract**: `component-contract/v1` / `complete` / provenance `llm-authored`

**Domain primitive**: 실패 상태

**탐지 출처**: llm-authored-component-decision

### 구조 (Anatomy)

- failure-list
- recovery-actions
- technical-details

### 상태 (States)

| 상태 | 설명 |
|------|------|
| `partial-failure` | partial-failure |
| `full-failure` | full-failure |
| `retrying` | retrying |
| `details-expanded` | details-expanded |

### 구조화된 구현 계약

- Props: `{'state': {'type': 'enum', 'values': ['partial-failure', 'full-failure', 'retrying', 'details-expanded'], 'required': False, 'default': 'partial-failure'}, 'data': {'type': 'domain-object', 'object': '실패 상태', 'required': True}}`
- Variants: `{'axes': [], 'default': 'partial-failure', 'constraints': ['Only variants declared by this contract may be implemented.']}`
- Interaction: `{'events': ['retry', 'exclude-item', 'write-manually', 'escalate', 'toggle-details'], 'state_transitions': [], 'focus_behavior': 'Preserve visible focus and logical DOM order.', 'state_coverage': ['partial-failure', 'full-failure', 'retrying', 'details-expanded']}`
- Data: `{'domain_object': '실패 상태', 'required_fields': ['failed_items', 'recovery_actions', 'technical_detail'], 'provenance_required': False, 'empty_state_required': True}`
- Responsive: `{'required_widths_px': [320, 360, 390, 430, 768, 1024, 1440], 'control_rules': ['Buttons, CTA groups, tabs, filter chips, and toolbar actions must not rely on fixed px widths or mobile-hostile min-width values.', 'Every button-like control needs max-inline-size: 100%; controls inside flex/grid parents need min-inline-size: 0 so labels can shrink or wrap.', 'Action rows must wrap or stack at narrow widths; two-button rows need a <=480px fallback before implementation is complete.', 'Long Korean CTA labels must be tested with real copy. Prefer wrapping/stacking over clipping, overflow hidden, or forcing white-space: nowrap.', 'Horizontal rails, tickers, score strips, and carousels must not reveal partially clipped text. Either size cards so visible items are complete, or use compact labels such as icon+code in the rail and move full names to the detailed surface.', 'Do not use width: 100vw inside padded containers; it commonly creates horizontal scroll. Use width: 100%, max-width: 100%, or a documented full-bleed pattern.', 'Never hide body overflow-x as the fix for a layout bug; remove the overflowing width/min-width instead.'], 'container_behavior': 'wrap, stack, or reflow without hiding product state'}`
- Content rules: 실패 원인은 업무 문장으로 쓰고 기술 예외는 '자세히 보기' 안에 둔다; 복구 행동 4종(다시 시도·항목 제외·직접 작성·운영 이관)을 항상 함께 제시한다

### 토큰 바인딩

```
component.container.border: 1px solid var(--ds-color-danger)
part.failure-list.color: var(--ds-color-ink)
part.recovery-actions.color: var(--ds-color-link)
part.technical-details.font-family: var(--ds-font-mono)
state.retrying.color: var(--ds-color-info)
state.details-expanded.background: var(--ds-color-surface-muted)
```

### 접근성

- 상호작용 카드/행은 <a> 또는 <button>으로 구현
- 선택 상태는 aria-selected 또는 aria-pressed로 노출
- 장식용 elevation만으로 계층을 만들지 않고 heading/label을 제공
- 실패 알림은 role=alert로 전달한다
- 펼침 상태를 aria-expanded로 표시한다

### 브랜드 적용

- [trustworthy+calm] hover: 예측 가능하고 일관된 hover 패턴 + opacity 변화 (0.08-0.12), elevation 변화 없음
- [trustworthy+calm] motion: 모든 전환에 동일한 easing/duration + 150-200ms ease-out, bounce/spring 없음
- [trustworthy+calm] color: 안정적인 neutral 기반, 과한 accent 변화 없음 + 중성 톤 위주, accent는 최소한으로

### Visual Adaptation Hints

- **card_elevation_tendency**: 카드는 낮은 elevation만 허용하고 색면 차이로 그룹을 구분한다. 내부 여백은 넉넉하게 두고 card breathing room을 확보한다. (source=cards; confidence=0.19; provenance=inferred; direction=low-elevation tinted cards를 기본으로 하고, 넓은 내부 여백과 강한 section breathing room. 중간 반경으로 제품 UI 절제 유지.; evidence=surface=tinted, density=airy, corner=medium)
- **border_vs_fill_emphasis**: fill 중심이다. tint surface로 성격을 만들고 border는 아주 얇게 보조한다. (source=cards; confidence=0.19; provenance=inferred; direction=low-elevation tinted cards를 기본으로 하고, 넓은 내부 여백과 강한 section breathing room. 중간 반경으로 제품 UI 절제 유지.; evidence=surface=tinted, density=airy, corner=medium)
- **chart_panel_framing**: 차트 패널은 soft tint frame과 restrained divider로 프레이밍한다. 헤더의 metric, controls, plot 영역을 분리하고 내부 여백은 촘촘하게 관리한다. (source=data_display; confidence=0.19; provenance=inferred; direction=정보 밀도를 유지하되 thin dividers와 restrained accent로 hierarchy를 만든다.; evidence=layout=dashboard-grid, density=airy, layout=data-review-surface, surface=tinted)

### 구현 노트

- 기존에 같은 역할의 컴포넌트가 있으면 토큰 교체부터 시작
- variant prop으로 시각적 변형을 관리 (하드코딩 금지)
- 애니메이션은 상태 설명용으로만 사용, 장식 효과 금지

---

## fact-review / fact-list-row

**역할**: 업무 문장 요약 + 상태 태그 + 근거 개수의 한 줄

**Component contract**: `component-contract/v1` / `complete` / provenance `llm-authored`

**Domain primitive**: 추출된 사실 목록

**탐지 출처**: llm-authored-component-decision

### 구조 (Anatomy)

- fact-sentence
- status-tag-slot
- evidence-count

### 상태 (States)

| 상태 | 설명 |
|------|------|
| `default` | 기본 상태 |
| `selected` | selected |
| `edited-unsaved` | edited-unsaved |
| `approved` | approved |
| `excluded` | excluded |
| `conflict` | conflict |

### 구조화된 구현 계약

- Props: `{'state': {'type': 'enum', 'values': ['default', 'selected', 'edited-unsaved', 'approved', 'excluded', 'conflict'], 'required': False, 'default': 'default'}, 'data': {'type': 'domain-object', 'object': '추출된 사실 목록', 'required': True}}`
- Variants: `{'axes': [], 'default': 'default', 'constraints': ['Only variants declared by this contract may be implemented.']}`
- Interaction: `{'events': ['select', 'open-editor', 'toggle-check'], 'state_transitions': [], 'focus_behavior': 'Preserve visible focus and logical DOM order.', 'state_coverage': ['default', 'selected', 'edited-unsaved', 'approved', 'excluded', 'conflict']}`
- Data: `{'domain_object': '추출된 사실 목록', 'required_fields': ['fact_sentence', 'status', 'evidence_count'], 'provenance_required': True, 'empty_state_required': True}`
- Responsive: `{'required_widths_px': [320, 360, 390, 430, 768, 1024, 1440], 'control_rules': ['Buttons, CTA groups, tabs, filter chips, and toolbar actions must not rely on fixed px widths or mobile-hostile min-width values.', 'Every button-like control needs max-inline-size: 100%; controls inside flex/grid parents need min-inline-size: 0 so labels can shrink or wrap.', 'Action rows must wrap or stack at narrow widths; two-button rows need a <=480px fallback before implementation is complete.', 'Long Korean CTA labels must be tested with real copy. Prefer wrapping/stacking over clipping, overflow hidden, or forcing white-space: nowrap.', 'Horizontal rails, tickers, score strips, and carousels must not reveal partially clipped text. Either size cards so visible items are complete, or use compact labels such as icon+code in the rail and move full names to the detailed surface.', 'Do not use width: 100vw inside padded containers; it commonly creates horizontal scroll. Use width: 100%, max-width: 100%, or a documented full-bleed pattern.', 'Never hide body overflow-x as the fix for a layout bug; remove the overflowing width/min-width instead.'], 'container_behavior': 'wrap, stack, or reflow without hiding product state'}`
- Content rules: 첫 줄은 항상 업무 문장 요약이다; 상태 태그와 근거 개수를 문장 뒤에 붙인다

### 토큰 바인딩

```
part.fact-sentence.font-family: var(--ds-font-body)
part.status-tag-slot.background: var(--ds-color-surface)
part.evidence-count.color: var(--ds-color-ink-subtle)
state.selected.background: var(--ds-color-surface-tint)
state.conflict.border-color: var(--ds-color-danger)
state.approved.color: var(--ds-color-success)
```

### 접근성

- 상호작용 카드/행은 <a> 또는 <button>으로 구현
- 선택 상태는 aria-selected 또는 aria-pressed로 노출
- 장식용 elevation만으로 계층을 만들지 않고 heading/label을 제공
- 행 선택 상태를 aria-selected로 표시한다
- 상태는 색+아이콘+텍스트로 병기한다

### 브랜드 적용

- [trustworthy+calm] hover: 예측 가능하고 일관된 hover 패턴 + opacity 변화 (0.08-0.12), elevation 변화 없음
- [trustworthy+calm] motion: 모든 전환에 동일한 easing/duration + 150-200ms ease-out, bounce/spring 없음
- [trustworthy+calm] color: 안정적인 neutral 기반, 과한 accent 변화 없음 + 중성 톤 위주, accent는 최소한으로

### 구현 노트

- 기존에 같은 역할의 컴포넌트가 있으면 토큰 교체부터 시작
- variant prop으로 시각적 변형을 관리 (하드코딩 금지)
- 애니메이션은 상태 설명용으로만 사용, 장식 효과 금지

---

## fact-review / fact-status-tag

**역할**: 바로 확인 가능/선택 필요/새 개념 제안/충돌 확인/제외됨 5상태 태그

**Component contract**: `component-contract/v1` / `complete` / provenance `llm-authored`

**Domain primitive**: 목록 상태

**탐지 출처**: llm-authored-component-decision

### 구조 (Anatomy)

- tag-icon
- tag-label

### 상태 (States)

| 상태 | 설명 |
|------|------|
| `ready` | ready |
| `needs-choice` | needs-choice |
| `new-concept` | new-concept |
| `conflict` | conflict |
| `excluded` | excluded |

### 구조화된 구현 계약

- Props: `{'state': {'type': 'enum', 'values': ['ready', 'needs-choice', 'new-concept', 'conflict', 'excluded'], 'required': False, 'default': 'ready'}, 'data': {'type': 'domain-object', 'object': '목록 상태', 'required': True}}`
- Variants: `{'axes': [], 'default': 'ready', 'constraints': ['Only variants declared by this contract may be implemented.']}`
- Interaction: `{'events': ['filter-by-status'], 'state_transitions': [], 'focus_behavior': 'Preserve visible focus and logical DOM order.', 'state_coverage': ['ready', 'needs-choice', 'new-concept', 'conflict', 'excluded']}`
- Data: `{'domain_object': '목록 상태', 'required_fields': ['status', 'label'], 'provenance_required': False, 'empty_state_required': True}`
- Responsive: `{'required_widths_px': [320, 360, 390, 430, 768, 1024, 1440], 'control_rules': ['Buttons, CTA groups, tabs, filter chips, and toolbar actions must not rely on fixed px widths or mobile-hostile min-width values.', 'Every button-like control needs max-inline-size: 100%; controls inside flex/grid parents need min-inline-size: 0 so labels can shrink or wrap.', 'Action rows must wrap or stack at narrow widths; two-button rows need a <=480px fallback before implementation is complete.', 'Long Korean CTA labels must be tested with real copy. Prefer wrapping/stacking over clipping, overflow hidden, or forcing white-space: nowrap.', 'Horizontal rails, tickers, score strips, and carousels must not reveal partially clipped text. Either size cards so visible items are complete, or use compact labels such as icon+code in the rail and move full names to the detailed surface.', 'Do not use width: 100vw inside padded containers; it commonly creates horizontal scroll. Use width: 100%, max-width: 100%, or a documented full-bleed pattern.', 'Never hide body overflow-x as the fix for a layout bug; remove the overflowing width/min-width instead.'], 'container_behavior': 'wrap, stack, or reflow without hiding product state'}`
- Content rules: 라벨은 5상태 업무 어휘를 그대로 쓴다: 바로 확인 가능·선택 필요·새 개념 제안·충돌 확인·제외됨; 상태 의미를 바꾸는 커스텀 색을 만들지 않는다

### 토큰 바인딩

```
component.container.border-radius: var(--ds-radius-sm)
part.tag-label.font-family: var(--ds-font-body)
part.tag-icon.color: var(--ds-color-ink-muted)
state.ready.color: var(--ds-color-success)
state.needs-choice.color: var(--ds-color-warning)
state.conflict.color: var(--ds-color-danger)
state.new-concept.color: var(--ds-color-info)
state.excluded.color: var(--ds-color-ink-subtle)
```

### 접근성

- 상호작용 카드/행은 <a> 또는 <button>으로 구현
- 선택 상태는 aria-selected 또는 aria-pressed로 노출
- 장식용 elevation만으로 계층을 만들지 않고 heading/label을 제공
- 아이콘과 텍스트를 병기해 색맹에 대응한다
- sr-only로 상태 전체 문구를 제공한다

### 브랜드 적용

- [trustworthy+calm] hover: 예측 가능하고 일관된 hover 패턴 + opacity 변화 (0.08-0.12), elevation 변화 없음
- [trustworthy+calm] motion: 모든 전환에 동일한 easing/duration + 150-200ms ease-out, bounce/spring 없음
- [trustworthy+calm] color: 안정적인 neutral 기반, 과한 accent 변화 없음 + 중성 톤 위주, accent는 최소한으로

### Visual Adaptation Hints

- **card_elevation_tendency**: 카드는 낮은 elevation만 허용하고 색면 차이로 그룹을 구분한다. 내부 여백은 넉넉하게 두고 card breathing room을 확보한다. (source=cards; confidence=0.19; provenance=inferred; direction=low-elevation tinted cards를 기본으로 하고, 넓은 내부 여백과 강한 section breathing room. 중간 반경으로 제품 UI 절제 유지.; evidence=surface=tinted, density=airy, corner=medium)
- **border_vs_fill_emphasis**: fill 중심이다. tint surface로 성격을 만들고 border는 아주 얇게 보조한다. (source=cards; confidence=0.19; provenance=inferred; direction=low-elevation tinted cards를 기본으로 하고, 넓은 내부 여백과 강한 section breathing room. 중간 반경으로 제품 UI 절제 유지.; evidence=surface=tinted, density=airy, corner=medium)
- **chart_panel_framing**: 차트 패널은 soft tint frame과 restrained divider로 프레이밍한다. 헤더의 metric, controls, plot 영역을 분리하고 내부 여백은 촘촘하게 관리한다. (source=data_display; confidence=0.19; provenance=inferred; direction=정보 밀도를 유지하되 thin dividers와 restrained accent로 hierarchy를 만든다.; evidence=layout=dashboard-grid, density=airy, layout=data-review-surface, surface=tinted)

### 구현 노트

- 기존에 같은 역할의 컴포넌트가 있으면 토큰 교체부터 시작
- variant prop으로 시각적 변형을 관리 (하드코딩 금지)
- 애니메이션은 상태 설명용으로만 사용, 장식 효과 금지

---

## fact-review / fact-sentence-editor

**역할**: 한 문장 기본 표시 아래 대상/조건/결과/적용 범위/유효기간 편집

**Component contract**: `component-contract/v1` / `complete` / provenance `llm-authored`

**Domain primitive**: 사실 편집

**탐지 출처**: llm-authored-component-decision

### 구조 (Anatomy)

- sentence-display
- scoped-fields
- field-label
- validity-note

### 상태 (States)

| 상태 | 설명 |
|------|------|
| `read` | read |
| `editing` | 편집 모드 활성 |
| `dirty` | dirty |
| `saved` | saved |
| `validation-blocked` | validation-blocked |

### 구조화된 구현 계약

- Props: `{'state': {'type': 'enum', 'values': ['read', 'editing', 'dirty', 'saved', 'validation-blocked'], 'required': False, 'default': 'read'}, 'data': {'type': 'domain-object', 'object': '사실 편집', 'required': True}}`
- Variants: `{'axes': [], 'default': 'read', 'constraints': ['Only variants declared by this contract may be implemented.']}`
- Interaction: `{'events': ['edit', 'save', 'revert', 'validation-fail'], 'state_transitions': [], 'focus_behavior': 'Preserve visible focus and logical DOM order.', 'state_coverage': ['read', 'editing', 'dirty', 'saved', 'validation-blocked']}`
- Data: `{'domain_object': '사실 편집', 'required_fields': ['sentence', 'target', 'condition', 'result', 'scope', 'valid_period'], 'provenance_required': True, 'empty_state_required': True}`
- Responsive: `{'required_widths_px': [320, 360, 390, 430, 768, 1024, 1440], 'control_rules': ['Buttons, CTA groups, tabs, filter chips, and toolbar actions must not rely on fixed px widths or mobile-hostile min-width values.', 'Every button-like control needs max-inline-size: 100%; controls inside flex/grid parents need min-inline-size: 0 so labels can shrink or wrap.', 'Action rows must wrap or stack at narrow widths; two-button rows need a <=480px fallback before implementation is complete.', 'Long Korean CTA labels must be tested with real copy. Prefer wrapping/stacking over clipping, overflow hidden, or forcing white-space: nowrap.', 'Horizontal rails, tickers, score strips, and carousels must not reveal partially clipped text. Either size cards so visible items are complete, or use compact labels such as icon+code in the rail and move full names to the detailed surface.', 'Do not use width: 100vw inside padded containers; it commonly creates horizontal scroll. Use width: 100%, max-width: 100%, or a documented full-bleed pattern.', 'Never hide body overflow-x as the fix for a layout bug; remove the overflowing width/min-width instead.'], 'container_behavior': 'wrap, stack, or reflow without hiding product state'}`
- Content rules: 기본 표시는 한 문장이고 구조 필드는 그 아래에 종속된다; 내부 관계 종류는 업무 문장으로 번역해 보여준다

### 토큰 바인딩

```
part.sentence-display.font-family: var(--ds-font-heading)
part.scoped-fields.background: var(--ds-color-surface)
part.field-label.color: var(--ds-color-ink-muted)
part.validity-note.color: var(--ds-color-danger)
state.editing.border-color: var(--ds-color-link)
state.saved.color: var(--ds-color-success)
state.validation-blocked.border-color: var(--ds-color-danger)
```

### 접근성

- 상호작용 카드/행은 <a> 또는 <button>으로 구현
- 선택 상태는 aria-selected 또는 aria-pressed로 노출
- 장식용 elevation만으로 계층을 만들지 않고 heading/label을 제공
- 필드 레이블과 오류를 aria-describedby로 연결한다
- 저장·차단 상태 변경을 보조기기에 알린다

### 브랜드 적용

- [trustworthy+calm] hover: 예측 가능하고 일관된 hover 패턴 + opacity 변화 (0.08-0.12), elevation 변화 없음
- [trustworthy+calm] motion: 모든 전환에 동일한 easing/duration + 150-200ms ease-out, bounce/spring 없음
- [trustworthy+calm] color: 안정적인 neutral 기반, 과한 accent 변화 없음 + 중성 톤 위주, accent는 최소한으로

### 구현 노트

- 기존에 같은 역할의 컴포넌트가 있으면 토큰 교체부터 시작
- variant prop으로 시각적 변형을 관리 (하드코딩 금지)
- 애니메이션은 상태 설명용으로만 사용, 장식 효과 금지

---

## fact-review / relation-candidate-card

**역할**: 관계 후보를 업무 문장 + '왜 이 후보인가' 근거 줄로 비교

**Component contract**: `component-contract/v1` / `complete` / provenance `llm-authored`

**Domain primitive**: 애매한 관계

**탐지 출처**: llm-authored-component-decision

**Slot archetype**: `surface-card`

### 구조 (Anatomy)

- candidate-sentence
- reason-line
- select-control

### 상태 (States)

| 상태 | 설명 |
|------|------|
| `default` | 기본 상태 |
| `selected` | selected |
| `keyboard-focus` | keyboard-focus |
| `insufficient-evidence` | insufficient-evidence |

### 구조화된 구현 계약

- Props: `{'state': {'type': 'enum', 'values': ['default', 'selected', 'keyboard-focus', 'insufficient-evidence'], 'required': False, 'default': 'default'}, 'data': {'type': 'domain-object', 'object': '애매한 관계', 'required': True}}`
- Variants: `{'axes': [], 'default': 'default', 'constraints': ['Only variants declared by this contract may be implemented.']}`
- Interaction: `{'events': ['select-candidate', 'expand-reason'], 'state_transitions': [], 'focus_behavior': 'Preserve visible focus and logical DOM order.', 'state_coverage': ['default', 'selected', 'keyboard-focus', 'insufficient-evidence']}`
- Data: `{'domain_object': '애매한 관계', 'required_fields': ['candidates', 'selected_candidate', 'reasons'], 'provenance_required': True, 'empty_state_required': True}`
- Responsive: `{'required_widths_px': [320, 360, 390, 430, 768, 1024, 1440], 'control_rules': ['Buttons, CTA groups, tabs, filter chips, and toolbar actions must not rely on fixed px widths or mobile-hostile min-width values.', 'Every button-like control needs max-inline-size: 100%; controls inside flex/grid parents need min-inline-size: 0 so labels can shrink or wrap.', 'Action rows must wrap or stack at narrow widths; two-button rows need a <=480px fallback before implementation is complete.', 'Long Korean CTA labels must be tested with real copy. Prefer wrapping/stacking over clipping, overflow hidden, or forcing white-space: nowrap.', 'Horizontal rails, tickers, score strips, and carousels must not reveal partially clipped text. Either size cards so visible items are complete, or use compact labels such as icon+code in the rail and move full names to the detailed surface.', 'Do not use width: 100vw inside padded containers; it commonly creates horizontal scroll. Use width: 100%, max-width: 100%, or a documented full-bleed pattern.', 'Never hide body overflow-x as the fix for a layout bug; remove the overflowing width/min-width instead.'], 'container_behavior': 'wrap, stack, or reflow without hiding product state'}`
- Content rules: 후보는 비교 가능한 업무 문장으로 표기한다; '왜 이 후보인가' 근거 줄을 반드시 포함한다

### 토큰 바인딩

```
part.candidate-sentence.color: var(--ds-color-ink)
part.reason-line.color: var(--ds-color-ink-muted)
part.select-control.color: var(--ds-color-primary)
state.selected.border-color: var(--ds-color-primary)
state.keyboard-focus.outline: 2px solid var(--ds-color-link)
state.insufficient-evidence.color: var(--ds-color-warning)
```

### 접근성

- 카드 자체가 링크/버튼이면 <a>/<button> 래퍼 사용
- 장식적 카드는 단순 <article> 또는 <div>
- radiogroup 패턴으로 후보를 선택한다
- 근거 줄을 후보와 함께 낭독하게 한다

### 브랜드 적용

- [trustworthy+calm] hover: 예측 가능하고 일관된 hover 패턴 + opacity 변화 (0.08-0.12), elevation 변화 없음
- [trustworthy+calm] motion: 모든 전환에 동일한 easing/duration + 150-200ms ease-out, bounce/spring 없음
- [trustworthy+calm] color: 안정적인 neutral 기반, 과한 accent 변화 없음 + 중성 톤 위주, accent는 최소한으로

### Visual Adaptation Hints

- **card_elevation_tendency**: 카드는 낮은 elevation만 허용하고 색면 차이로 그룹을 구분한다. 내부 여백은 넉넉하게 두고 card breathing room을 확보한다. (source=cards; confidence=0.19; provenance=inferred; direction=low-elevation tinted cards를 기본으로 하고, 넓은 내부 여백과 강한 section breathing room. 중간 반경으로 제품 UI 절제 유지.; evidence=surface=tinted, density=airy, corner=medium)
- **border_vs_fill_emphasis**: fill 중심이다. tint surface로 성격을 만들고 border는 아주 얇게 보조한다. (source=cards; confidence=0.19; provenance=inferred; direction=low-elevation tinted cards를 기본으로 하고, 넓은 내부 여백과 강한 section breathing room. 중간 반경으로 제품 UI 절제 유지.; evidence=surface=tinted, density=airy, corner=medium)

### 구현 노트

- 기존에 같은 역할의 컴포넌트가 있으면 토큰 교체부터 시작
- variant prop으로 시각적 변형을 관리 (하드코딩 금지)
- 애니메이션은 상태 설명용으로만 사용, 장식 효과 금지

---

## evidence / evidence-panel

**역할**: 원문 발췌+위치, 매칭 키, 추론 규칙, 사람 수정 이력의 접이식 우측 패널

**Component contract**: `component-contract/v1` / `complete` / provenance `llm-authored`

**Domain primitive**: 근거 패널

**탐지 출처**: llm-authored-component-decision

### 구조 (Anatomy)

- source-excerpt
- source-compare-view
- match-keys
- inference-rules
- edit-history

### 상태 (States)

| 상태 | 설명 |
|------|------|
| `collapsed` | 접힌 상태 |
| `open` | 열린 상태 |
| `source-compare` | source-compare |
| `pinned` | pinned |

### 구조화된 구현 계약

- Props: `{'state': {'type': 'enum', 'values': ['collapsed', 'open', 'source-compare', 'pinned'], 'required': False, 'default': 'collapsed'}, 'data': {'type': 'domain-object', 'object': '근거 패널', 'required': True}}`
- Variants: `{'axes': [], 'default': 'collapsed', 'constraints': ['Only variants declared by this contract may be implemented.']}`
- Interaction: `{'events': ['open', 'collapse', 'pin', 'open-source-compare'], 'state_transitions': [], 'focus_behavior': 'Preserve visible focus and logical DOM order.', 'state_coverage': ['collapsed', 'open', 'source-compare', 'pinned']}`
- Data: `{'domain_object': '근거 패널', 'required_fields': ['source_excerpt', 'source_location', 'match_keys', 'inference_rules', 'edit_history'], 'provenance_required': True, 'empty_state_required': True}`
- Responsive: `{'required_widths_px': [320, 360, 390, 430, 768, 1024, 1440], 'control_rules': ['Buttons, CTA groups, tabs, filter chips, and toolbar actions must not rely on fixed px widths or mobile-hostile min-width values.', 'Every button-like control needs max-inline-size: 100%; controls inside flex/grid parents need min-inline-size: 0 so labels can shrink or wrap.', 'Action rows must wrap or stack at narrow widths; two-button rows need a <=480px fallback before implementation is complete.', 'Long Korean CTA labels must be tested with real copy. Prefer wrapping/stacking over clipping, overflow hidden, or forcing white-space: nowrap.', 'Horizontal rails, tickers, score strips, and carousels must not reveal partially clipped text. Either size cards so visible items are complete, or use compact labels such as icon+code in the rail and move full names to the detailed surface.', 'Do not use width: 100vw inside padded containers; it commonly creates horizontal scroll. Use width: 100%, max-width: 100%, or a documented full-bleed pattern.', 'Never hide body overflow-x as the fix for a layout bug; remove the overflowing width/min-width instead.'], 'container_behavior': 'wrap, stack, or reflow without hiding product state'}`
- Content rules: 근거 4종(원문 발췌·매칭 키·추론 규칙·수정 이력)을 항상 같은 순서로 보여준다; 원문 위치(문서·화면·코드)를 발췌와 함께 표기한다

### 토큰 바인딩

```
part.source-excerpt.background: var(--ds-color-surface-tint)
part.source-compare-view.background: var(--ds-color-surface-muted)
part.match-keys.font-family: var(--ds-font-mono)
part.edit-history.color: var(--ds-color-ink-muted)
state.open.background: var(--ds-color-surface-elevated)
state.pinned.border-color: var(--ds-color-info)
```

### 접근성

- 상호작용 카드/행은 <a> 또는 <button>으로 구현
- 선택 상태는 aria-selected 또는 aria-pressed로 노출
- 장식용 elevation만으로 계층을 만들지 않고 heading/label을 제공
- complementary landmark로 마크업한다
- 패널 열림·고정 상태를 보조기기에 알린다

### 브랜드 적용

- [trustworthy+calm] hover: 예측 가능하고 일관된 hover 패턴 + opacity 변화 (0.08-0.12), elevation 변화 없음
- [trustworthy+calm] motion: 모든 전환에 동일한 easing/duration + 150-200ms ease-out, bounce/spring 없음
- [trustworthy+calm] color: 안정적인 neutral 기반, 과한 accent 변화 없음 + 중성 톤 위주, accent는 최소한으로

### Visual Adaptation Hints

- **card_elevation_tendency**: 카드는 낮은 elevation만 허용하고 색면 차이로 그룹을 구분한다. 내부 여백은 넉넉하게 두고 card breathing room을 확보한다. (source=cards; confidence=0.19; provenance=inferred; direction=low-elevation tinted cards를 기본으로 하고, 넓은 내부 여백과 강한 section breathing room. 중간 반경으로 제품 UI 절제 유지.; evidence=surface=tinted, density=airy, corner=medium)
- **border_vs_fill_emphasis**: fill 중심이다. tint surface로 성격을 만들고 border는 아주 얇게 보조한다. (source=cards; confidence=0.19; provenance=inferred; direction=low-elevation tinted cards를 기본으로 하고, 넓은 내부 여백과 강한 section breathing room. 중간 반경으로 제품 UI 절제 유지.; evidence=surface=tinted, density=airy, corner=medium)
- **chart_panel_framing**: 차트 패널은 soft tint frame과 restrained divider로 프레이밍한다. 헤더의 metric, controls, plot 영역을 분리하고 내부 여백은 촘촘하게 관리한다. (source=data_display; confidence=0.19; provenance=inferred; direction=정보 밀도를 유지하되 thin dividers와 restrained accent로 hierarchy를 만든다.; evidence=layout=dashboard-grid, density=airy, layout=data-review-surface, surface=tinted)

### 구현 노트

- 기존에 같은 역할의 컴포넌트가 있으면 토큰 교체부터 시작
- variant prop으로 시각적 변형을 관리 (하드코딩 금지)
- 애니메이션은 상태 설명용으로만 사용, 장식 효과 금지

---

## approval / review-action-bar

**역할**: 보류/제외/수정 저장/선택 승인/전체 승인 + 반영 범위·개수 + 불가 사유

**Component contract**: `component-contract/v1` / `complete` / provenance `llm-authored`

**Domain primitive**: 하단 행동

**탐지 출처**: llm-authored-component-decision

### 구조 (Anatomy)

- scope-count
- approve-button
- secondary-actions
- blocked-reason

### 상태 (States)

| 상태 | 설명 |
|------|------|
| `idle` | idle |
| `selection-active` | selection-active |
| `approve-enabled` | approve-enabled |
| `approve-blocked-with-reason` | approve-blocked-with-reason |
| `submitting` | submitting |

### 구조화된 구현 계약

- Props: `{'state': {'type': 'enum', 'values': ['idle', 'selection-active', 'approve-enabled', 'approve-blocked-with-reason', 'submitting'], 'required': False, 'default': 'idle'}, 'data': {'type': 'domain-object', 'object': '하단 행동', 'required': True}}`
- Variants: `{'axes': [], 'default': 'idle', 'constraints': ['Only variants declared by this contract may be implemented.']}`
- Interaction: `{'events': ['hold', 'exclude', 'save-edit', 'approve-selected', 'approve-all-reviewable'], 'state_transitions': [], 'focus_behavior': 'Preserve visible focus and logical DOM order.', 'state_coverage': ['idle', 'selection-active', 'approve-enabled', 'approve-blocked-with-reason', 'submitting']}`
- Data: `{'domain_object': '하단 행동', 'required_fields': ['selection_count', 'approve_scope', 'blocked_reasons'], 'provenance_required': False, 'empty_state_required': True}`
- Responsive: `{'required_widths_px': [320, 360, 390, 430, 768, 1024, 1440], 'control_rules': ['Buttons, CTA groups, tabs, filter chips, and toolbar actions must not rely on fixed px widths or mobile-hostile min-width values.', 'Every button-like control needs max-inline-size: 100%; controls inside flex/grid parents need min-inline-size: 0 so labels can shrink or wrap.', 'Action rows must wrap or stack at narrow widths; two-button rows need a <=480px fallback before implementation is complete.', 'Long Korean CTA labels must be tested with real copy. Prefer wrapping/stacking over clipping, overflow hidden, or forcing white-space: nowrap.', 'Horizontal rails, tickers, score strips, and carousels must not reveal partially clipped text. Either size cards so visible items are complete, or use compact labels such as icon+code in the rail and move full names to the detailed surface.', 'Do not use width: 100vw inside padded containers; it commonly creates horizontal scroll. Use width: 100%, max-width: 100%, or a documented full-bleed pattern.', 'Never hide body overflow-x as the fix for a layout bug; remove the overflowing width/min-width instead.'], 'container_behavior': 'wrap, stack, or reflow without hiding product state'}`
- Content rules: 승인 버튼 옆에 반영 범위와 개수를 상시 표기한다; 승인 불가는 이유와 해결 행동을 함께 보여준다

### 토큰 바인딩

```
part.scope-count.color: var(--ds-color-ink-muted)
part.approve-button.background: var(--ds-color-primary)
part.secondary-actions.color: var(--ds-color-link)
part.blocked-reason.color: var(--ds-color-danger)
state.approve-blocked-with-reason.background: var(--ds-color-surface-muted)
state.submitting.background: var(--ds-color-surface-muted)
```

### 접근성

- 상호작용 카드/행은 <a> 또는 <button>으로 구현
- 선택 상태는 aria-selected 또는 aria-pressed로 노출
- 장식용 elevation만으로 계층을 만들지 않고 heading/label을 제공
- 버튼의 결과와 영향 범위를 버튼 근처 텍스트로 명시한다
- 차단 사유를 aria-describedby로 연결한다

### 브랜드 적용

- [trustworthy+calm] hover: 예측 가능하고 일관된 hover 패턴 + opacity 변화 (0.08-0.12), elevation 변화 없음
- [trustworthy+calm] motion: 모든 전환에 동일한 easing/duration + 150-200ms ease-out, bounce/spring 없음
- [trustworthy+calm] color: 안정적인 neutral 기반, 과한 accent 변화 없음 + 중성 톤 위주, accent는 최소한으로

### 구현 노트

- 기존에 같은 역할의 컴포넌트가 있으면 토큰 교체부터 시작
- variant prop으로 시각적 변형을 관리 (하드코딩 금지)
- 애니메이션은 상태 설명용으로만 사용, 장식 효과 금지

---

## concept-proposal / new-concept-form

**역할**: 현업 이름/뜻·예시/유사 용어/사용 업무 입력 + 대기 지식 목록

**Component contract**: `component-contract/v1` / `complete` / provenance `llm-authored`

**Domain primitive**: 새 개념 제안

**탐지 출처**: llm-authored-component-decision

### 구조 (Anatomy)

- field-group
- waiting-knowledge-list
- review-status-line

### 상태 (States)

| 상태 | 설명 |
|------|------|
| `empty` | 데이터 없음 |
| `filled` | 값이 입력된 상태 |
| `submitted` | submitted |
| `in-official-review` | in-official-review |
| `approved` | approved |
| `rejected` | rejected |

### 구조화된 구현 계약

- Props: `{'state': {'type': 'enum', 'values': ['empty', 'filled', 'submitted', 'in-official-review', 'approved', 'rejected'], 'required': False, 'default': 'empty'}, 'data': {'type': 'domain-object', 'object': '새 개념 제안', 'required': True}}`
- Variants: `{'axes': [], 'default': 'empty', 'constraints': ['Only variants declared by this contract may be implemented.']}`
- Interaction: `{'events': ['submit', 'save-draft', 'view-waiting-knowledge'], 'state_transitions': [], 'focus_behavior': 'Preserve visible focus and logical DOM order.', 'state_coverage': ['empty', 'filled', 'submitted', 'in-official-review', 'approved', 'rejected']}`
- Data: `{'domain_object': '새 개념 제안', 'required_fields': ['business_name', 'meaning_example', 'similar_terms', 'business_area', 'waiting_knowledge'], 'provenance_required': False, 'empty_state_required': True}`
- Responsive: `{'required_widths_px': [320, 360, 390, 430, 768, 1024, 1440], 'control_rules': ['Buttons, CTA groups, tabs, filter chips, and toolbar actions must not rely on fixed px widths or mobile-hostile min-width values.', 'Every button-like control needs max-inline-size: 100%; controls inside flex/grid parents need min-inline-size: 0 so labels can shrink or wrap.', 'Action rows must wrap or stack at narrow widths; two-button rows need a <=480px fallback before implementation is complete.', 'Long Korean CTA labels must be tested with real copy. Prefer wrapping/stacking over clipping, overflow hidden, or forcing white-space: nowrap.', 'Horizontal rails, tickers, score strips, and carousels must not reveal partially clipped text. Either size cards so visible items are complete, or use compact labels such as icon+code in the rail and move full names to the detailed surface.', 'Do not use width: 100vw inside padded containers; it commonly creates horizontal scroll. Use width: 100%, max-width: 100%, or a documented full-bleed pattern.', 'Never hide body overflow-x as the fix for a layout bug; remove the overflowing width/min-width instead.'], 'container_behavior': 'wrap, stack, or reflow without hiding product state'}`
- Content rules: 입력 항목은 현업 어휘 5종만 받는다: 이름·뜻과 예시·비슷한 용어·사용 업무·대기 지식; Core 종류·Pack·제약 후보는 고급 보기로 격리한다

### 토큰 바인딩

```
part.field-group.background: var(--ds-color-surface)
part.waiting-knowledge-list.color: var(--ds-color-ink-muted)
part.review-status-line.color: var(--ds-color-info)
state.in-official-review.color: var(--ds-color-info)
state.approved.color: var(--ds-color-success)
state.rejected.color: var(--ds-color-danger)
```

### 접근성

- 상호작용 카드/행은 <a> 또는 <button>으로 구현
- 선택 상태는 aria-selected 또는 aria-pressed로 노출
- 장식용 elevation만으로 계층을 만들지 않고 heading/label을 제공
- 필수 항목을 시각과 텍스트로 함께 표시한다
- 제출 후 상태 변화를 알림으로 전달한다

### 브랜드 적용

- [trustworthy+calm] hover: 예측 가능하고 일관된 hover 패턴 + opacity 변화 (0.08-0.12), elevation 변화 없음
- [trustworthy+calm] motion: 모든 전환에 동일한 easing/duration + 150-200ms ease-out, bounce/spring 없음
- [trustworthy+calm] color: 안정적인 neutral 기반, 과한 accent 변화 없음 + 중성 톤 위주, accent는 최소한으로

### 구현 노트

- 기존에 같은 역할의 컴포넌트가 있으면 토큰 교체부터 시작
- variant prop으로 시각적 변형을 관리 (하드코딩 금지)
- 애니메이션은 상태 설명용으로만 사용, 장식 효과 금지

---

## link-workspace / link-workspace-canvas

**역할**: 검색 결과 배치 + 선 연결 + 점선 분석 중 표시의 작업 공간

**Component contract**: `component-contract/v1` / `complete` / provenance `llm-authored`

**Domain primitive**: 관계 연결 작업실

**탐지 출처**: llm-authored-component-decision

### 구조 (Anatomy)

- work-surface
- item-node
- link-line
- keyboard-path-bar

### 상태 (States)

| 상태 | 설명 |
|------|------|
| `empty` | 데이터 없음 |
| `items-placed` | items-placed |
| `linking` | linking |
| `analyzing-dashed` | analyzing-dashed |
| `verdict-shown` | verdict-shown |

### 구조화된 구현 계약

- Props: `{'state': {'type': 'enum', 'values': ['empty', 'items-placed', 'linking', 'analyzing-dashed', 'verdict-shown'], 'required': False, 'default': 'empty'}, 'data': {'type': 'domain-object', 'object': '관계 연결 작업실', 'required': True}}`
- Variants: `{'axes': [], 'default': 'empty', 'constraints': ['Only variants declared by this contract may be implemented.']}`
- Interaction: `{'events': ['place-item', 'start-link', 'draw-link', 'keyboard-link', 'remove-item'], 'state_transitions': [], 'focus_behavior': 'Preserve visible focus and logical DOM order.', 'state_coverage': ['empty', 'items-placed', 'linking', 'analyzing-dashed', 'verdict-shown']}`
- Data: `{'domain_object': '관계 연결 작업실', 'required_fields': ['items', 'links', 'analysis_state'], 'provenance_required': False, 'empty_state_required': True}`
- Responsive: `{'required_widths_px': [320, 360, 390, 430, 768, 1024, 1440], 'control_rules': ['Buttons, CTA groups, tabs, filter chips, and toolbar actions must not rely on fixed px widths or mobile-hostile min-width values.', 'Every button-like control needs max-inline-size: 100%; controls inside flex/grid parents need min-inline-size: 0 so labels can shrink or wrap.', 'Action rows must wrap or stack at narrow widths; two-button rows need a <=480px fallback before implementation is complete.', 'Long Korean CTA labels must be tested with real copy. Prefer wrapping/stacking over clipping, overflow hidden, or forcing white-space: nowrap.', 'Horizontal rails, tickers, score strips, and carousels must not reveal partially clipped text. Either size cards so visible items are complete, or use compact labels such as icon+code in the rail and move full names to the detailed surface.', 'Do not use width: 100vw inside padded containers; it commonly creates horizontal scroll. Use width: 100%, max-width: 100%, or a documented full-bleed pattern.', 'Never hide body overflow-x as the fix for a layout bug; remove the overflowing width/min-width instead.'], 'container_behavior': 'wrap, stack, or reflow without hiding product state'}`
- Content rules: 분석 중 연결은 점선과 '분석 중' 라벨로 표시한다; 승인 전에는 본 그래프에 아무것도 쓰지 않는다

### 토큰 바인딩

```
part.work-surface.background: var(--ds-color-canvas)
part.item-node.background: var(--ds-color-surface)
part.link-line.color: var(--ds-color-info)
part.keyboard-path-bar.color: var(--ds-color-link)
state.analyzing-dashed.border-color: var(--ds-color-info)
state.empty.color: var(--ds-color-ink-subtle)
```

### 접근성

- 상호작용 카드/행은 <a> 또는 <button>으로 구현
- 선택 상태는 aria-selected 또는 aria-pressed로 노출
- 장식용 elevation만으로 계층을 만들지 않고 heading/label을 제공
- 캔버스와 같은 내용을 목록·표로 제공한다
- 키보드 경로(연결 시작→대상 검색→연결 후보 보기)를 완비한다

### 브랜드 적용

- [trustworthy+calm] hover: 예측 가능하고 일관된 hover 패턴 + opacity 변화 (0.08-0.12), elevation 변화 없음
- [trustworthy+calm] motion: 모든 전환에 동일한 easing/duration + 150-200ms ease-out, bounce/spring 없음
- [trustworthy+calm] color: 안정적인 neutral 기반, 과한 accent 변화 없음 + 중성 톤 위주, accent는 최소한으로

### 구현 노트

- 기존에 같은 역할의 컴포넌트가 있으면 토큰 교체부터 시작
- variant prop으로 시각적 변형을 관리 (하드코딩 금지)
- 애니메이션은 상태 설명용으로만 사용, 장식 효과 금지

---

## link-workspace / link-verdict-card

**역할**: 동일 대상/동일 후보/기존 경로/직접 후보/중간 필요/근거 부족 6결과 카드

**Component contract**: `component-contract/v1` / `complete` / provenance `llm-authored`

**Domain primitive**: 분석 결과

**탐지 출처**: llm-authored-component-decision

**Slot archetype**: `surface-card`

### 구조 (Anatomy)

- verdict-sentence
- evidence-line
- next-action

### 상태 (States)

| 상태 | 설명 |
|------|------|
| `same-entity` | same-entity |
| `possible-duplicate` | possible-duplicate |
| `already-connected` | already-connected |
| `direct-candidate` | direct-candidate |
| `needs-intermediate` | needs-intermediate |
| `insufficient-evidence` | insufficient-evidence |

### 구조화된 구현 계약

- Props: `{'state': {'type': 'enum', 'values': ['same-entity', 'possible-duplicate', 'already-connected', 'direct-candidate', 'needs-intermediate', 'insufficient-evidence'], 'required': False, 'default': 'same-entity'}, 'data': {'type': 'domain-object', 'object': '분석 결과', 'required': True}}`
- Variants: `{'axes': [], 'default': 'same-entity', 'constraints': ['Only variants declared by this contract may be implemented.']}`
- Interaction: `{'events': ['accept-verdict', 'edit-relation', 'send-to-review'], 'state_transitions': [], 'focus_behavior': 'Preserve visible focus and logical DOM order.', 'state_coverage': ['same-entity', 'possible-duplicate', 'already-connected', 'direct-candidate', 'needs-intermediate', 'insufficient-evidence']}`
- Data: `{'domain_object': '분석 결과', 'required_fields': ['verdict_type', 'verdict_sentence', 'evidence_refs'], 'provenance_required': True, 'empty_state_required': True}`
- Responsive: `{'required_widths_px': [320, 360, 390, 430, 768, 1024, 1440], 'control_rules': ['Buttons, CTA groups, tabs, filter chips, and toolbar actions must not rely on fixed px widths or mobile-hostile min-width values.', 'Every button-like control needs max-inline-size: 100%; controls inside flex/grid parents need min-inline-size: 0 so labels can shrink or wrap.', 'Action rows must wrap or stack at narrow widths; two-button rows need a <=480px fallback before implementation is complete.', 'Long Korean CTA labels must be tested with real copy. Prefer wrapping/stacking over clipping, overflow hidden, or forcing white-space: nowrap.', 'Horizontal rails, tickers, score strips, and carousels must not reveal partially clipped text. Either size cards so visible items are complete, or use compact labels such as icon+code in the rail and move full names to the detailed surface.', 'Do not use width: 100vw inside padded containers; it commonly creates horizontal scroll. Use width: 100%, max-width: 100%, or a documented full-bleed pattern.', 'Never hide body overflow-x as the fix for a layout bug; remove the overflowing width/min-width instead.'], 'container_behavior': 'wrap, stack, or reflow without hiding product state'}`
- Content rules: 6종 결과를 각각 고정 문구 틀로 표기한다; 다음 행동(수정·검토함 보내기)을 결과와 함께 제시한다

### 토큰 바인딩

```
part.verdict-sentence.color: var(--ds-color-ink)
part.evidence-line.color: var(--ds-color-ink-muted)
part.next-action.color: var(--ds-color-link)
state.same-entity.color: var(--ds-color-success)
state.needs-intermediate.color: var(--ds-color-warning)
state.insufficient-evidence.color: var(--ds-color-ink-subtle)
```

### 접근성

- 카드 자체가 링크/버튼이면 <a>/<button> 래퍼 사용
- 장식적 카드는 단순 <article> 또는 <div>
- 결과 유형을 텍스트로 먼저 낭독하게 한다
- 카드 간 이동을 화살표 키로 지원한다

### 브랜드 적용

- [trustworthy+calm] hover: 예측 가능하고 일관된 hover 패턴 + opacity 변화 (0.08-0.12), elevation 변화 없음
- [trustworthy+calm] motion: 모든 전환에 동일한 easing/duration + 150-200ms ease-out, bounce/spring 없음
- [trustworthy+calm] color: 안정적인 neutral 기반, 과한 accent 변화 없음 + 중성 톤 위주, accent는 최소한으로

### Visual Adaptation Hints

- **card_elevation_tendency**: 카드는 낮은 elevation만 허용하고 색면 차이로 그룹을 구분한다. 내부 여백은 넉넉하게 두고 card breathing room을 확보한다. (source=cards; confidence=0.19; provenance=inferred; direction=low-elevation tinted cards를 기본으로 하고, 넓은 내부 여백과 강한 section breathing room. 중간 반경으로 제품 UI 절제 유지.; evidence=surface=tinted, density=airy, corner=medium)
- **border_vs_fill_emphasis**: fill 중심이다. tint surface로 성격을 만들고 border는 아주 얇게 보조한다. (source=cards; confidence=0.19; provenance=inferred; direction=low-elevation tinted cards를 기본으로 하고, 넓은 내부 여백과 강한 section breathing room. 중간 반경으로 제품 UI 절제 유지.; evidence=surface=tinted, density=airy, corner=medium)

### 구현 노트

- 기존에 같은 역할의 컴포넌트가 있으면 토큰 교체부터 시작
- variant prop으로 시각적 변형을 관리 (하드코딩 금지)
- 애니메이션은 상태 설명용으로만 사용, 장식 효과 금지

---

## knowledge-detail / knowledge-status-badge

**역할**: 초안/확인 필요/팀 확인/공식/철회됨 수명주기 배지

**Component contract**: `component-contract/v1` / `complete` / provenance `llm-authored`

**Domain primitive**: 현재 상태

**탐지 출처**: llm-authored-component-decision

### 구조 (Anatomy)

- badge-icon
- badge-label

### 상태 (States)

| 상태 | 설명 |
|------|------|
| `draft` | draft |
| `needs-check` | needs-check |
| `team-confirmed` | team-confirmed |
| `official` | official |
| `retracted` | retracted |

### 구조화된 구현 계약

- Props: `{'state': {'type': 'enum', 'values': ['draft', 'needs-check', 'team-confirmed', 'official', 'retracted'], 'required': False, 'default': 'draft'}, 'data': {'type': 'domain-object', 'object': '현재 상태', 'required': True}}`
- Variants: `{'axes': [], 'default': 'draft', 'constraints': ['Only variants declared by this contract may be implemented.']}`
- Interaction: `{'events': ['view-status-history'], 'state_transitions': [], 'focus_behavior': 'Preserve visible focus and logical DOM order.', 'state_coverage': ['draft', 'needs-check', 'team-confirmed', 'official', 'retracted']}`
- Data: `{'domain_object': '현재 상태', 'required_fields': ['status'], 'provenance_required': True, 'empty_state_required': True}`
- Responsive: `{'required_widths_px': [320, 360, 390, 430, 768, 1024, 1440], 'control_rules': ['Buttons, CTA groups, tabs, filter chips, and toolbar actions must not rely on fixed px widths or mobile-hostile min-width values.', 'Every button-like control needs max-inline-size: 100%; controls inside flex/grid parents need min-inline-size: 0 so labels can shrink or wrap.', 'Action rows must wrap or stack at narrow widths; two-button rows need a <=480px fallback before implementation is complete.', 'Long Korean CTA labels must be tested with real copy. Prefer wrapping/stacking over clipping, overflow hidden, or forcing white-space: nowrap.', 'Horizontal rails, tickers, score strips, and carousels must not reveal partially clipped text. Either size cards so visible items are complete, or use compact labels such as icon+code in the rail and move full names to the detailed surface.', 'Do not use width: 100vw inside padded containers; it commonly creates horizontal scroll. Use width: 100%, max-width: 100%, or a documented full-bleed pattern.', 'Never hide body overflow-x as the fix for a layout bug; remove the overflowing width/min-width instead.'], 'container_behavior': 'wrap, stack, or reflow without hiding product state'}`
- Content rules: 5상태 라벨을 고정한다: 초안·확인 필요·팀 확인·공식·철회됨

### 토큰 바인딩

```
component.container.border-radius: var(--ds-radius-sm)
part.badge-label.font-family: var(--ds-font-body)
part.badge-icon.color: var(--ds-color-ink-muted)
state.official.color: var(--ds-color-success)
state.needs-check.color: var(--ds-color-warning)
state.retracted.color: var(--ds-color-danger)
state.draft.color: var(--ds-color-ink-subtle)
```

### 접근성

- 상호작용 카드/행은 <a> 또는 <button>으로 구현
- 선택 상태는 aria-selected 또는 aria-pressed로 노출
- 장식용 elevation만으로 계층을 만들지 않고 heading/label을 제공
- 상태를 색+아이콘+텍스트로 병기한다

### 브랜드 적용

- [trustworthy+calm] hover: 예측 가능하고 일관된 hover 패턴 + opacity 변화 (0.08-0.12), elevation 변화 없음
- [trustworthy+calm] motion: 모든 전환에 동일한 easing/duration + 150-200ms ease-out, bounce/spring 없음
- [trustworthy+calm] color: 안정적인 neutral 기반, 과한 accent 변화 없음 + 중성 톤 위주, accent는 최소한으로

### Visual Adaptation Hints

- **card_elevation_tendency**: 카드는 낮은 elevation만 허용하고 색면 차이로 그룹을 구분한다. 내부 여백은 넉넉하게 두고 card breathing room을 확보한다. (source=cards; confidence=0.19; provenance=inferred; direction=low-elevation tinted cards를 기본으로 하고, 넓은 내부 여백과 강한 section breathing room. 중간 반경으로 제품 UI 절제 유지.; evidence=surface=tinted, density=airy, corner=medium)
- **border_vs_fill_emphasis**: fill 중심이다. tint surface로 성격을 만들고 border는 아주 얇게 보조한다. (source=cards; confidence=0.19; provenance=inferred; direction=low-elevation tinted cards를 기본으로 하고, 넓은 내부 여백과 강한 section breathing room. 중간 반경으로 제품 UI 절제 유지.; evidence=surface=tinted, density=airy, corner=medium)
- **chart_panel_framing**: 차트 패널은 soft tint frame과 restrained divider로 프레이밍한다. 헤더의 metric, controls, plot 영역을 분리하고 내부 여백은 촘촘하게 관리한다. (source=data_display; confidence=0.19; provenance=inferred; direction=정보 밀도를 유지하되 thin dividers와 restrained accent로 hierarchy를 만든다.; evidence=layout=dashboard-grid, density=airy, layout=data-review-surface, surface=tinted)

### 구현 노트

- 기존에 같은 역할의 컴포넌트가 있으면 토큰 교체부터 시작
- variant prop으로 시각적 변형을 관리 (하드코딩 금지)
- 애니메이션은 상태 설명용으로만 사용, 장식 효과 금지

---

## knowledge-detail / provenance-timeline

**역할**: 변경·승인 이력 (누가·언제·무엇을·왜)

**Component contract**: `component-contract/v1` / `complete` / provenance `llm-authored`

**Domain primitive**: 변경·승인 이력

**탐지 출처**: llm-authored-component-decision

### 구조 (Anatomy)

- timeline-entry
- actor-name
- change-reason
- timestamp

### 상태 (States)

| 상태 | 설명 |
|------|------|
| `default` | 기본 상태 |
| `entry-expanded` | entry-expanded |
| `empty` | 데이터 없음 |

### 구조화된 구현 계약

- Props: `{'state': {'type': 'enum', 'values': ['default', 'entry-expanded', 'empty'], 'required': False, 'default': 'default'}, 'data': {'type': 'domain-object', 'object': '변경·승인 이력', 'required': True}}`
- Variants: `{'axes': [], 'default': 'default', 'constraints': ['Only variants declared by this contract may be implemented.']}`
- Interaction: `{'events': ['expand-entry', 'open-evidence'], 'state_transitions': [], 'focus_behavior': 'Preserve visible focus and logical DOM order.', 'state_coverage': ['default', 'entry-expanded', 'empty']}`
- Data: `{'domain_object': '변경·승인 이력', 'required_fields': ['entries', 'actors', 'timestamps'], 'provenance_required': True, 'empty_state_required': True}`
- Responsive: `{'required_widths_px': [320, 360, 390, 430, 768, 1024, 1440], 'control_rules': ['Buttons, CTA groups, tabs, filter chips, and toolbar actions must not rely on fixed px widths or mobile-hostile min-width values.', 'Every button-like control needs max-inline-size: 100%; controls inside flex/grid parents need min-inline-size: 0 so labels can shrink or wrap.', 'Action rows must wrap or stack at narrow widths; two-button rows need a <=480px fallback before implementation is complete.', 'Long Korean CTA labels must be tested with real copy. Prefer wrapping/stacking over clipping, overflow hidden, or forcing white-space: nowrap.', 'Horizontal rails, tickers, score strips, and carousels must not reveal partially clipped text. Either size cards so visible items are complete, or use compact labels such as icon+code in the rail and move full names to the detailed surface.', 'Do not use width: 100vw inside padded containers; it commonly creates horizontal scroll. Use width: 100%, max-width: 100%, or a documented full-bleed pattern.', 'Never hide body overflow-x as the fix for a layout bug; remove the overflowing width/min-width instead.'], 'container_behavior': 'wrap, stack, or reflow without hiding product state'}`
- Content rules: 각 항목은 누가·언제·무엇을·왜 순으로 쓴다; 승인자는 실명 또는 역할로 표기한다

### 토큰 바인딩

```
part.timeline-entry.border: 1px solid var(--ds-color-border)
part.actor-name.color: var(--ds-color-ink)
part.change-reason.color: var(--ds-color-ink-muted)
part.timestamp.font-family: var(--ds-font-mono)
state.entry-expanded.background: var(--ds-color-surface-muted)
state.empty.color: var(--ds-color-ink-subtle)
```

### 접근성

- 상호작용 카드/행은 <a> 또는 <button>으로 구현
- 선택 상태는 aria-selected 또는 aria-pressed로 노출
- 장식용 elevation만으로 계층을 만들지 않고 heading/label을 제공
- 시간순 리스트 시맨틱(ol)을 사용한다
- 펼침 상태를 aria-expanded로 표시한다

### 브랜드 적용

- [trustworthy+calm] hover: 예측 가능하고 일관된 hover 패턴 + opacity 변화 (0.08-0.12), elevation 변화 없음
- [trustworthy+calm] motion: 모든 전환에 동일한 easing/duration + 150-200ms ease-out, bounce/spring 없음
- [trustworthy+calm] color: 안정적인 neutral 기반, 과한 accent 변화 없음 + 중성 톤 위주, accent는 최소한으로

### 구현 노트

- 기존에 같은 역할의 컴포넌트가 있으면 토큰 교체부터 시작
- variant prop으로 시각적 변형을 관리 (하드코딩 금지)
- 애니메이션은 상태 설명용으로만 사용, 장식 효과 금지

---

## knowledge-detail / impact-question-buttons

**역할**: 왜?/어디서 왔나?/무엇이 영향 받나? 즉시 실행 버튼, 결과는 문장·단계 목록 우선

**Component contract**: `component-contract/v1` / `complete` / provenance `llm-authored`

**Domain primitive**: 영향과 원인

**탐지 출처**: llm-authored-component-decision

### 구조 (Anatomy)

- question-button
- answer-list
- graph-toggle

### 상태 (States)

| 상태 | 설명 |
|------|------|
| `idle` | idle |
| `loading` | 로딩 중 (스피너 표시) |
| `answer-shown` | answer-shown |
| `graph-secondary-view` | graph-secondary-view |

### 구조화된 구현 계약

- Props: `{'state': {'type': 'enum', 'values': ['idle', 'loading', 'answer-shown', 'graph-secondary-view'], 'required': False, 'default': 'idle'}, 'data': {'type': 'domain-object', 'object': '영향과 원인', 'required': True}}`
- Variants: `{'axes': [], 'default': 'idle', 'constraints': ['Only variants declared by this contract may be implemented.']}`
- Interaction: `{'events': ['ask-why', 'ask-origin', 'ask-impact', 'toggle-graph-view'], 'state_transitions': [], 'focus_behavior': 'Preserve visible focus and logical DOM order.', 'state_coverage': ['idle', 'loading', 'answer-shown', 'graph-secondary-view']}`
- Data: `{'domain_object': '영향과 원인', 'required_fields': ['knowledge_id', 'answer_sentences', 'answer_steps'], 'provenance_required': True, 'empty_state_required': True}`
- Responsive: `{'required_widths_px': [320, 360, 390, 430, 768, 1024, 1440], 'control_rules': ['Buttons, CTA groups, tabs, filter chips, and toolbar actions must not rely on fixed px widths or mobile-hostile min-width values.', 'Every button-like control needs max-inline-size: 100%; controls inside flex/grid parents need min-inline-size: 0 so labels can shrink or wrap.', 'Action rows must wrap or stack at narrow widths; two-button rows need a <=480px fallback before implementation is complete.', 'Long Korean CTA labels must be tested with real copy. Prefer wrapping/stacking over clipping, overflow hidden, or forcing white-space: nowrap.', 'Horizontal rails, tickers, score strips, and carousels must not reveal partially clipped text. Either size cards so visible items are complete, or use compact labels such as icon+code in the rail and move full names to the detailed surface.', 'Do not use width: 100vw inside padded containers; it commonly creates horizontal scroll. Use width: 100%, max-width: 100%, or a documented full-bleed pattern.', 'Never hide body overflow-x as the fix for a layout bug; remove the overflowing width/min-width instead.'], 'container_behavior': 'wrap, stack, or reflow without hiding product state'}`
- Content rules: 버튼 라벨을 고정한다: 왜? · 어디서 왔나? · 무엇이 영향 받나?; 결과는 문장과 단계 목록을 우선하고 그래프는 보조 보기로 둔다

### 토큰 바인딩

```
part.question-button.border: 1px solid var(--ds-color-border-strong)
part.answer-list.color: var(--ds-color-ink)
part.graph-toggle.color: var(--ds-color-link)
state.loading.color: var(--ds-color-ink-subtle)
state.answer-shown.background: var(--ds-color-surface)
```

### 접근성

- 상호작용 카드/행은 <a> 또는 <button>으로 구현
- 선택 상태는 aria-selected 또는 aria-pressed로 노출
- 장식용 elevation만으로 계층을 만들지 않고 heading/label을 제공
- 결과 로딩을 aria-busy로 표시한다
- 그래프 보기에는 표 대체를 제공한다

### 브랜드 적용

- [trustworthy+calm] hover: 예측 가능하고 일관된 hover 패턴 + opacity 변화 (0.08-0.12), elevation 변화 없음
- [trustworthy+calm] motion: 모든 전환에 동일한 easing/duration + 150-200ms ease-out, bounce/spring 없음
- [trustworthy+calm] color: 안정적인 neutral 기반, 과한 accent 변화 없음 + 중성 톤 위주, accent는 최소한으로

### Visual Adaptation Hints

- **cta_prominence**: CTA prominence는 restrained이다. 데이터 작업 흐름을 가리지 않도록 primary만 선명하게 두고 나머지는 text/ghost로 낮춘다. (source=cards; confidence=0.19; provenance=inferred; direction=low-elevation tinted cards를 기본으로 하고, 넓은 내부 여백과 강한 section breathing room. 중간 반경으로 제품 UI 절제 유지.; evidence=surface=tinted, density=airy, corner=medium, layout=data-review-surface)

### 구현 노트

- 기존에 같은 역할의 컴포넌트가 있으면 토큰 교체부터 시작
- variant prop으로 시각적 변형을 관리 (하드코딩 금지)
- 반응형 검증: 320px, 360px, 390px, 430px에서 control overflow와 viewport horizontal scroll이 없어야 함
- action row는 narrow viewport에서 `flex-wrap: wrap` 또는 세로 stack으로 전환하고, overflow-x 숨김으로 문제를 덮지 않음
- 애니메이션은 상태 설명용으로만 사용, 장식 효과 금지

---

## knowledge-detail / advanced-drawer

**역할**: 그래프·IRI·Pack·SHACL 리포트 원문을 담는 고급 보기 서랍

**Component contract**: `component-contract/v1` / `complete` / provenance `llm-authored`

**Domain primitive**: 고급 정보

**탐지 출처**: llm-authored-component-decision

### 구조 (Anatomy)

- drawer-toggle
- raw-content
- vocabulary-warning

### 상태 (States)

| 상태 | 설명 |
|------|------|
| `closed` | 닫힌 상태 |
| `open` | 열린 상태 |
| `raw-report-view` | raw-report-view |

### 구조화된 구현 계약

- Props: `{'state': {'type': 'enum', 'values': ['closed', 'open', 'raw-report-view'], 'required': False, 'default': 'closed'}, 'data': {'type': 'domain-object', 'object': '고급 정보', 'required': True}}`
- Variants: `{'axes': [], 'default': 'closed', 'constraints': ['Only variants declared by this contract may be implemented.']}`
- Interaction: `{'events': ['open', 'close', 'copy-raw'], 'state_transitions': [], 'focus_behavior': 'Preserve visible focus and logical DOM order.', 'state_coverage': ['closed', 'open', 'raw-report-view']}`
- Data: `{'domain_object': '고급 정보', 'required_fields': ['raw_iri', 'pack_info', 'shacl_report'], 'provenance_required': True, 'empty_state_required': True}`
- Responsive: `{'required_widths_px': [320, 360, 390, 430, 768, 1024, 1440], 'control_rules': ['Buttons, CTA groups, tabs, filter chips, and toolbar actions must not rely on fixed px widths or mobile-hostile min-width values.', 'Every button-like control needs max-inline-size: 100%; controls inside flex/grid parents need min-inline-size: 0 so labels can shrink or wrap.', 'Action rows must wrap or stack at narrow widths; two-button rows need a <=480px fallback before implementation is complete.', 'Long Korean CTA labels must be tested with real copy. Prefer wrapping/stacking over clipping, overflow hidden, or forcing white-space: nowrap.', 'Horizontal rails, tickers, score strips, and carousels must not reveal partially clipped text. Either size cards so visible items are complete, or use compact labels such as icon+code in the rail and move full names to the detailed surface.', 'Do not use width: 100vw inside padded containers; it commonly creates horizontal scroll. Use width: 100%, max-width: 100%, or a documented full-bleed pattern.', 'Never hide body overflow-x as the fix for a layout bug; remove the overflowing width/min-width instead.'], 'container_behavior': 'wrap, stack, or reflow without hiding product state'}`
- Content rules: 서랍 밖에서는 내부 어휘를 쓰지 않는다; 서랍 내용이 내부 기술 정보의 원문임을 명시한다

### 토큰 바인딩

```
part.drawer-toggle.color: var(--ds-color-ink-muted)
part.raw-content.font-family: var(--ds-font-mono)
part.vocabulary-warning.color: var(--ds-color-warning)
state.open.background: var(--ds-color-surface-elevated)
state.raw-report-view.background: var(--ds-color-surface-muted)
```

### 접근성

- 상호작용 카드/행은 <a> 또는 <button>으로 구현
- 선택 상태는 aria-selected 또는 aria-pressed로 노출
- 장식용 elevation만으로 계층을 만들지 않고 heading/label을 제공
- drawer/dialog 패턴으로 포커스 트랩과 Esc 닫기를 지원한다

### 브랜드 적용

- [trustworthy+calm] hover: 예측 가능하고 일관된 hover 패턴 + opacity 변화 (0.08-0.12), elevation 변화 없음
- [trustworthy+calm] motion: 모든 전환에 동일한 easing/duration + 150-200ms ease-out, bounce/spring 없음
- [trustworthy+calm] color: 안정적인 neutral 기반, 과한 accent 변화 없음 + 중성 톤 위주, accent는 최소한으로

### 구현 노트

- 기존에 같은 역할의 컴포넌트가 있으면 토큰 교체부터 시작
- variant prop으로 시각적 변형을 관리 (하드코딩 금지)
- 애니메이션은 상태 설명용으로만 사용, 장식 효과 금지

---

## operations / ops-queue-table

**역할**: 입력 작업 대기/진행/성공/실패 테이블 + 재시도(기존 작업의 새 시도임을 구분)

**Component contract**: `component-contract/v1` / `complete` / provenance `llm-authored`

**Domain primitive**: 운영 상태

**탐지 출처**: llm-authored-component-decision

### 구조 (Anatomy)

- table-header
- job-row
- status-cell
- retry-control

### 상태 (States)

| 상태 | 설명 |
|------|------|
| `queued` | queued |
| `running` | running |
| `succeeded` | succeeded |
| `failed` | failed |
| `retry-of-existing` | retry-of-existing |
| `blocked-by-policy` | blocked-by-policy |

### 구조화된 구현 계약

- Props: `{'state': {'type': 'enum', 'values': ['queued', 'running', 'succeeded', 'failed', 'retry-of-existing', 'blocked-by-policy'], 'required': False, 'default': 'queued'}, 'data': {'type': 'domain-object', 'object': '운영 상태', 'required': True}}`
- Variants: `{'axes': [], 'default': 'queued', 'constraints': ['Only variants declared by this contract may be implemented.']}`
- Interaction: `{'events': ['retry-job', 'cancel-job', 'filter-status', 'open-job-detail'], 'state_transitions': [], 'focus_behavior': 'Preserve visible focus and logical DOM order.', 'state_coverage': ['queued', 'running', 'succeeded', 'failed', 'retry-of-existing', 'blocked-by-policy']}`
- Data: `{'domain_object': '운영 상태', 'required_fields': ['jobs', 'job_status', 'retry_lineage'], 'provenance_required': False, 'empty_state_required': True}`
- Responsive: `{'required_widths_px': [320, 360, 390, 430, 768, 1024, 1440], 'control_rules': ['Buttons, CTA groups, tabs, filter chips, and toolbar actions must not rely on fixed px widths or mobile-hostile min-width values.', 'Every button-like control needs max-inline-size: 100%; controls inside flex/grid parents need min-inline-size: 0 so labels can shrink or wrap.', 'Action rows must wrap or stack at narrow widths; two-button rows need a <=480px fallback before implementation is complete.', 'Long Korean CTA labels must be tested with real copy. Prefer wrapping/stacking over clipping, overflow hidden, or forcing white-space: nowrap.', 'Horizontal rails, tickers, score strips, and carousels must not reveal partially clipped text. Either size cards so visible items are complete, or use compact labels such as icon+code in the rail and move full names to the detailed surface.', 'Do not use width: 100vw inside padded containers; it commonly creates horizontal scroll. Use width: 100%, max-width: 100%, or a documented full-bleed pattern.', 'Never hide body overflow-x as the fix for a layout bug; remove the overflowing width/min-width instead.'], 'container_behavior': 'wrap, stack, or reflow without hiding product state'}`
- Content rules: 재시도는 기존 작업의 새 시도임을 행에 표기한다; 차단 사유(권한·정책)를 상태와 함께 보여준다

### 토큰 바인딩

```
part.table-header.background: var(--ds-color-surface-muted)
part.job-row.border: 1px solid var(--ds-color-border)
part.status-cell.font-family: var(--ds-font-mono)
part.retry-control.color: var(--ds-color-link)
state.failed.color: var(--ds-color-danger)
state.succeeded.color: var(--ds-color-success)
state.blocked-by-policy.color: var(--ds-color-warning)
```

### 접근성

- 상호작용 카드/행은 <a> 또는 <button>으로 구현
- 선택 상태는 aria-selected 또는 aria-pressed로 노출
- 장식용 elevation만으로 계층을 만들지 않고 heading/label을 제공
- 테이블 헤더에 scope를 지정한다
- 상태 변경을 aria-live로 알린다

### 브랜드 적용

- [trustworthy+calm] hover: 예측 가능하고 일관된 hover 패턴 + opacity 변화 (0.08-0.12), elevation 변화 없음
- [trustworthy+calm] motion: 모든 전환에 동일한 easing/duration + 150-200ms ease-out, bounce/spring 없음
- [trustworthy+calm] color: 안정적인 neutral 기반, 과한 accent 변화 없음 + 중성 톤 위주, accent는 최소한으로

### Visual Adaptation Hints

- **card_elevation_tendency**: 카드는 낮은 elevation만 허용하고 색면 차이로 그룹을 구분한다. 내부 여백은 넉넉하게 두고 card breathing room을 확보한다. (source=cards; confidence=0.19; provenance=inferred; direction=low-elevation tinted cards를 기본으로 하고, 넓은 내부 여백과 강한 section breathing room. 중간 반경으로 제품 UI 절제 유지.; evidence=surface=tinted, density=airy, corner=medium)
- **border_vs_fill_emphasis**: fill 중심이다. tint surface로 성격을 만들고 border는 아주 얇게 보조한다. (source=cards; confidence=0.19; provenance=inferred; direction=low-elevation tinted cards를 기본으로 하고, 넓은 내부 여백과 강한 section breathing room. 중간 반경으로 제품 UI 절제 유지.; evidence=surface=tinted, density=airy, corner=medium)
- **filter_nav_density**: filter/nav density는 compact하다. chip, scope, pagination을 촘촘하게 묶되 의미 단위별 group은 분리한다. (source=navigation; confidence=0.26; provenance=inferred; direction=고정 sidebar 또는 split-pane navigation을 우선하고, 현재 위치와 scope를 항상 명시한다.; evidence=Split-pane workspace, layout=data-review-surface, density=airy)
- **chart_panel_framing**: 차트 패널은 soft tint frame과 restrained divider로 프레이밍한다. 헤더의 metric, controls, plot 영역을 분리하고 내부 여백은 촘촘하게 관리한다. (source=data_display; confidence=0.19; provenance=inferred; direction=정보 밀도를 유지하되 thin dividers와 restrained accent로 hierarchy를 만든다.; evidence=layout=dashboard-grid, density=airy, layout=data-review-surface, surface=tinted)

### 레퍼런스 근거

- **Primer**: Design Systems gave me a unique opportunity to combine two of my passions: systems engineering with design operations. I find pleasure in the small...

### 구현 노트

- 기존에 같은 역할의 컴포넌트가 있으면 토큰 교체부터 시작
- variant prop으로 시각적 변형을 관리 (하드코딩 금지)
- 반응형 검증: 320px, 360px, 390px, 430px에서 control overflow와 viewport horizontal scroll이 없어야 함
- action row는 narrow viewport에서 `flex-wrap: wrap` 또는 세로 stack으로 전환하고, overflow-x 숨김으로 문제를 덮지 않음
- 애니메이션은 상태 설명용으로만 사용, 장식 효과 금지

---

## operations / quarantine-list

**역할**: 검증 실패·격리 항목 목록 + 실패 원인 + 재시도 가능 여부

**Component contract**: `component-contract/v1` / `complete` / provenance `llm-authored`

**Domain primitive**: 격리된 항목

**탐지 출처**: llm-authored-component-decision

### 구조 (Anatomy)

- quarantine-row
- failure-reason
- retry-flag

### 상태 (States)

| 상태 | 설명 |
|------|------|
| `quarantined` | quarantined |
| `reviewable` | reviewable |
| `released` | released |
| `permanently-excluded` | permanently-excluded |

### 구조화된 구현 계약

- Props: `{'state': {'type': 'enum', 'values': ['quarantined', 'reviewable', 'released', 'permanently-excluded'], 'required': False, 'default': 'quarantined'}, 'data': {'type': 'domain-object', 'object': '격리된 항목', 'required': True}}`
- Variants: `{'axes': [], 'default': 'quarantined', 'constraints': ['Only variants declared by this contract may be implemented.']}`
- Interaction: `{'events': ['release', 'exclude-permanently', 'retry-validation'], 'state_transitions': [], 'focus_behavior': 'Preserve visible focus and logical DOM order.', 'state_coverage': ['quarantined', 'reviewable', 'released', 'permanently-excluded']}`
- Data: `{'domain_object': '격리된 항목', 'required_fields': ['items', 'quarantine_reason', 'retry_available'], 'provenance_required': False, 'empty_state_required': True}`
- Responsive: `{'required_widths_px': [320, 360, 390, 430, 768, 1024, 1440], 'control_rules': ['Buttons, CTA groups, tabs, filter chips, and toolbar actions must not rely on fixed px widths or mobile-hostile min-width values.', 'Every button-like control needs max-inline-size: 100%; controls inside flex/grid parents need min-inline-size: 0 so labels can shrink or wrap.', 'Action rows must wrap or stack at narrow widths; two-button rows need a <=480px fallback before implementation is complete.', 'Long Korean CTA labels must be tested with real copy. Prefer wrapping/stacking over clipping, overflow hidden, or forcing white-space: nowrap.', 'Horizontal rails, tickers, score strips, and carousels must not reveal partially clipped text. Either size cards so visible items are complete, or use compact labels such as icon+code in the rail and move full names to the detailed surface.', 'Do not use width: 100vw inside padded containers; it commonly creates horizontal scroll. Use width: 100%, max-width: 100%, or a documented full-bleed pattern.', 'Never hide body overflow-x as the fix for a layout bug; remove the overflowing width/min-width instead.'], 'container_behavior': 'wrap, stack, or reflow without hiding product state'}`
- Content rules: 격리 사유를 업무 문장으로 표기한다; 해제·영구 제외의 영향 범위를 행동 버튼 근처에 명시한다

### 토큰 바인딩

```
part.quarantine-row.background: var(--ds-color-surface)
part.failure-reason.color: var(--ds-color-danger)
part.retry-flag.color: var(--ds-color-info)
state.released.color: var(--ds-color-success)
state.permanently-excluded.color: var(--ds-color-ink-subtle)
```

### 접근성

- 상호작용 카드/행은 <a> 또는 <button>으로 구현
- 선택 상태는 aria-selected 또는 aria-pressed로 노출
- 장식용 elevation만으로 계층을 만들지 않고 heading/label을 제공
- 행동 버튼에 결과 설명을 연결한다
- 위험 행동에는 확인 대화 상자를 둔다

### 브랜드 적용

- [trustworthy+calm] hover: 예측 가능하고 일관된 hover 패턴 + opacity 변화 (0.08-0.12), elevation 변화 없음
- [trustworthy+calm] motion: 모든 전환에 동일한 easing/duration + 150-200ms ease-out, bounce/spring 없음
- [trustworthy+calm] color: 안정적인 neutral 기반, 과한 accent 변화 없음 + 중성 톤 위주, accent는 최소한으로

### 레퍼런스 근거

- **Primer**: Design Systems gave me a unique opportunity to combine two of my passions: systems engineering with design operations. I find pleasure in the small...

### 구현 노트

- 기존에 같은 역할의 컴포넌트가 있으면 토큰 교체부터 시작
- variant prop으로 시각적 변형을 관리 (하드코딩 금지)
- 애니메이션은 상태 설명용으로만 사용, 장식 효과 금지

---

## feedback-and-empty-states / empty-state-guide

**역할**: 첫 사용 빈 상태 안내 + 샘플로 체험하기 + 샘플 데이터 구분 라벨

**Component contract**: `component-contract/v1` / `complete` / provenance `llm-authored`

**Domain primitive**: 빈 상태

**탐지 출처**: llm-authored-component-decision

### 구조 (Anatomy)

- guide-message
- sample-cta
- sample-badge

### 상태 (States)

| 상태 | 설명 |
|------|------|
| `first-use` | first-use |
| `sample-active` | sample-active |
| `no-permission` | no-permission |
| `offline` | offline |

### 구조화된 구현 계약

- Props: `{'state': {'type': 'enum', 'values': ['first-use', 'sample-active', 'no-permission', 'offline'], 'required': False, 'default': 'first-use'}, 'data': {'type': 'domain-object', 'object': '빈 상태', 'required': True}}`
- Variants: `{'axes': [], 'default': 'first-use', 'constraints': ['Only variants declared by this contract may be implemented.']}`
- Interaction: `{'events': ['start-sample', 'add-knowledge'], 'state_transitions': [], 'focus_behavior': 'Preserve visible focus and logical DOM order.', 'state_coverage': ['first-use', 'sample-active', 'no-permission', 'offline']}`
- Data: `{'domain_object': '빈 상태', 'required_fields': ['state_kind', 'sample_available'], 'provenance_required': False, 'empty_state_required': True}`
- Responsive: `{'required_widths_px': [320, 360, 390, 430, 768, 1024, 1440], 'control_rules': ['Buttons, CTA groups, tabs, filter chips, and toolbar actions must not rely on fixed px widths or mobile-hostile min-width values.', 'Every button-like control needs max-inline-size: 100%; controls inside flex/grid parents need min-inline-size: 0 so labels can shrink or wrap.', 'Action rows must wrap or stack at narrow widths; two-button rows need a <=480px fallback before implementation is complete.', 'Long Korean CTA labels must be tested with real copy. Prefer wrapping/stacking over clipping, overflow hidden, or forcing white-space: nowrap.', 'Horizontal rails, tickers, score strips, and carousels must not reveal partially clipped text. Either size cards so visible items are complete, or use compact labels such as icon+code in the rail and move full names to the detailed surface.', 'Do not use width: 100vw inside padded containers; it commonly creates horizontal scroll. Use width: 100%, max-width: 100%, or a documented full-bleed pattern.', 'Never hide body overflow-x as the fix for a layout bug; remove the overflowing width/min-width instead.'], 'container_behavior': 'wrap, stack, or reflow without hiding product state'}`
- Content rules: 빈 상태 문구는 다음 행동을 제안한다: 문서를 올리거나 알고 있는 업무를 설명해 주세요; 샘플 데이터는 색과 라벨로 회사 데이터와 구분한다

### 토큰 바인딩

```
part.guide-message.color: var(--ds-color-ink-muted)
part.sample-cta.background: var(--ds-color-primary)
part.sample-badge.background: var(--ds-color-surface-tint)
state.sample-active.border-color: var(--ds-color-accent)
state.no-permission.color: var(--ds-color-warning)
state.offline.color: var(--ds-color-ink-subtle)
```

### 접근성

- 상호작용 카드/행은 <a> 또는 <button>으로 구현
- 선택 상태는 aria-selected 또는 aria-pressed로 노출
- 장식용 elevation만으로 계층을 만들지 않고 heading/label을 제공
- 안내 문구를 heading 구조에 포함한다
- 샘플 배지를 텍스트로 병기한다

### 브랜드 적용

- [trustworthy+calm] hover: 예측 가능하고 일관된 hover 패턴 + opacity 변화 (0.08-0.12), elevation 변화 없음
- [trustworthy+calm] motion: 모든 전환에 동일한 easing/duration + 150-200ms ease-out, bounce/spring 없음
- [trustworthy+calm] color: 안정적인 neutral 기반, 과한 accent 변화 없음 + 중성 톤 위주, accent는 최소한으로

### Visual Adaptation Hints

- **card_elevation_tendency**: 카드는 낮은 elevation만 허용하고 색면 차이로 그룹을 구분한다. 내부 여백은 넉넉하게 두고 card breathing room을 확보한다. (source=cards; confidence=0.19; provenance=inferred; direction=low-elevation tinted cards를 기본으로 하고, 넓은 내부 여백과 강한 section breathing room. 중간 반경으로 제품 UI 절제 유지.; evidence=surface=tinted, density=airy, corner=medium)
- **border_vs_fill_emphasis**: fill 중심이다. tint surface로 성격을 만들고 border는 아주 얇게 보조한다. (source=cards; confidence=0.19; provenance=inferred; direction=low-elevation tinted cards를 기본으로 하고, 넓은 내부 여백과 강한 section breathing room. 중간 반경으로 제품 UI 절제 유지.; evidence=surface=tinted, density=airy, corner=medium)
- **chart_panel_framing**: 차트 패널은 soft tint frame과 restrained divider로 프레이밍한다. 헤더의 metric, controls, plot 영역을 분리하고 내부 여백은 촘촘하게 관리한다. (source=data_display; confidence=0.19; provenance=inferred; direction=정보 밀도를 유지하되 thin dividers와 restrained accent로 hierarchy를 만든다.; evidence=layout=dashboard-grid, density=airy, layout=data-review-surface, surface=tinted)

### 구현 노트

- 기존에 같은 역할의 컴포넌트가 있으면 토큰 교체부터 시작
- variant prop으로 시각적 변형을 관리 (하드코딩 금지)
- 애니메이션은 상태 설명용으로만 사용, 장식 효과 금지

---

## navigation / workspace-topbar

**역할**: 현재 작업공간 이름 + 통합 검색 슬롯 + 도움말 + 사용자 메뉴 상단 바

**Component contract**: `component-contract/v1` / `complete` / provenance `llm-authored`

**Domain primitive**: workspace topbar

**탐지 출처**: llm-authored-component-decision

### 구조 (Anatomy)

- workspace-name
- search-slot
- help-entry
- user-menu

### 상태 (States)

| 상태 | 설명 |
|------|------|
| `default` | 기본 상태 |
| `search-focus` | search-focus |
| `menu-open` | menu-open |

### 구조화된 구현 계약

- Props: `{'state': {'type': 'enum', 'values': ['default', 'search-focus', 'menu-open'], 'required': False, 'default': 'default'}, 'data': {'type': 'domain-object', 'object': 'workspace topbar', 'required': True}}`
- Variants: `{'axes': [], 'default': 'default', 'constraints': ['Only variants declared by this contract may be implemented.']}`
- Interaction: `{'events': ['open-search', 'open-help', 'open-user-menu', 'switch-workspace'], 'state_transitions': [], 'focus_behavior': 'Preserve visible focus and logical DOM order.', 'state_coverage': ['default', 'search-focus', 'menu-open']}`
- Data: `{'domain_object': 'workspace topbar', 'required_fields': ['workspace_name', 'user'], 'provenance_required': False, 'empty_state_required': True}`
- Responsive: `{'required_widths_px': [320, 360, 390, 430, 768, 1024, 1440], 'control_rules': ['Buttons, CTA groups, tabs, filter chips, and toolbar actions must not rely on fixed px widths or mobile-hostile min-width values.', 'Every button-like control needs max-inline-size: 100%; controls inside flex/grid parents need min-inline-size: 0 so labels can shrink or wrap.', 'Action rows must wrap or stack at narrow widths; two-button rows need a <=480px fallback before implementation is complete.', 'Long Korean CTA labels must be tested with real copy. Prefer wrapping/stacking over clipping, overflow hidden, or forcing white-space: nowrap.', 'Horizontal rails, tickers, score strips, and carousels must not reveal partially clipped text. Either size cards so visible items are complete, or use compact labels such as icon+code in the rail and move full names to the detailed surface.', 'Do not use width: 100vw inside padded containers; it commonly creates horizontal scroll. Use width: 100%, max-width: 100%, or a documented full-bleed pattern.', 'Never hide body overflow-x as the fix for a layout bug; remove the overflowing width/min-width instead.'], 'container_behavior': 'wrap, stack, or reflow without hiding product state'}`
- Content rules: 현재 작업공간 이름을 항상 표시한다; 검색 슬롯은 홈 통합 검색과 같은 동작을 한다

### 토큰 바인딩

```
component.container.border-bottom: 1px solid var(--ds-color-border)
part.workspace-name.font-family: var(--ds-font-heading)
part.search-slot.background: var(--ds-color-surface)
part.user-menu.color: var(--ds-color-ink-muted)
state.search-focus.border-color: var(--ds-color-link)
state.menu-open.background: var(--ds-color-surface-elevated)
```

### 접근성

- nav landmark (role="navigation")
- aria-current="page" for active item
- 키보드 화살표 탐색 지원
- banner landmark를 사용한다
- 메뉴 열림을 aria-expanded로 표시한다

### 브랜드 적용

- [trustworthy+calm] hover: 예측 가능하고 일관된 hover 패턴 + opacity 변화 (0.08-0.12), elevation 변화 없음
- [trustworthy+calm] density: 기존 레이아웃 유지, 갑작스런 위치 변경 없음 + comfortable 모드 기본, 여유로운 padding
- [trustworthy+calm] motion: 모든 전환에 동일한 easing/duration + 150-200ms ease-out, bounce/spring 없음

### Visual Adaptation Hints

- **filter_nav_density**: filter/nav density는 compact하다. chip, scope, pagination을 촘촘하게 묶되 의미 단위별 group은 분리한다. (source=navigation; confidence=0.26; provenance=inferred; direction=고정 sidebar 또는 split-pane navigation을 우선하고, 현재 위치와 scope를 항상 명시한다.; evidence=Split-pane workspace, layout=data-review-surface, density=airy)

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
