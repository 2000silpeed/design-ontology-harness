# memory-garden — 인터랙션 계약

`design-system/interactions.css`가 이 계약의 실행 가능한 형태입니다.
선택되지 않은 패턴을 구현하거나 여기 없는 모션을 추가하면 린터가 막습니다.

- 선택 방식: `contextual-variation`
- 변동 시드: `None`

## 선택된 패턴

### enter · `immediate-swap`

Dense operational surfaces read faster when new content simply appears; motion costs attention the operator needs elsewhere.

- 마크업: `data-interaction="immediate-swap"`
- 모션: 80ms · `standard` · reduced-motion `skip`
- 적용 역할: detail-panel, list-surface
- 근거 팩: `harness-interaction-candidates`
- 가드레일:
  - Preferred when the user is scanning or comparing many rows at once.
  - Never animate position; only the content itself changes.
  - Keep a visible non-motion cue for what changed.

### emphasis · `weight-shift`

Editorial surfaces carry emphasis through type weight and contrast, so selection reads without adding a coloured frame.

- 마크업: `data-interaction="weight-shift"`
- 모션: 120ms · `standard` · reduced-motion `static`
- 적용 역할: list-surface, navigation-surface
- 근거 팩: `harness-interaction-candidates`
- 가드레일:
  - Do not rely on weight alone where the state is critical; pair with a non-typographic cue.
  - Keep the layout stable — reserve the heavier metrics so nothing reflows.
  - Focus visibility stays independent of this emphasis.

### progress · `skeleton-placeholder`

Reserving the shape of the incoming content prevents the layout shift that a centred spinner invites.

- 마크업: `data-interaction="skeleton-placeholder"`
- 모션: 1600ms · `standard` · reduced-motion `static`
- 적용 역할: detail-panel, list-surface
- 근거 팩: `harness-interaction-candidates`
- 가드레일:
  - The skeleton must match the real content's geometry, not a generic grey block.
  - Expose an accessible loading status; the shimmer is not an announcement.
  - Hold the shimmer to the loop budget and stop it as soon as content lands.

### transition · `context-crossfade`

A brief crossfade marks that the frame of reference changed while the surrounding chrome stayed put.

- 마크업: `data-interaction="context-crossfade"`
- 모션: 180ms · `standard` · reduced-motion `opacity-only`
- 적용 역할: detail-panel, list-surface, navigation-surface
- 근거 팩: `harness-interaction-candidates`
- 가드레일:
  - Chrome and navigation must not move during the fade.
  - Do not crossfade when the underlying data is identical.
  - Keep the outgoing and incoming content from overlapping legibly.

## 검토했지만 선택하지 않은 후보

- `anchored-shift` (transition, 점수 6)
- `inline-expand` (enter, 점수 6)
- `surface-lift` (emphasis, 점수 6)
- `determinate-bar` (progress, 점수 5)
- `dot-progress` (progress, 점수 5)
- `result-reveal` (enter, 점수 4)
- `staged-enter` (enter, 점수 3)

