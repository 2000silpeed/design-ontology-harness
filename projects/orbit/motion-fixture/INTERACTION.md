# orbit-motion-fixture — 인터랙션 계약

`design-system/interactions.css`가 이 계약의 실행 가능한 형태입니다.
선택되지 않은 패턴을 구현하거나 여기 없는 모션을 추가하면 린터가 막습니다.

- 선택 방식: `contextual-variation`
- 변동 시드: `7`

## 선택된 패턴

### enter · `immediate-swap`

Dense operational surfaces read faster when new content simply appears; motion costs attention the operator needs elsewhere.

- 마크업: `data-interaction="immediate-swap"`
- 모션: 80ms · `standard` · reduced-motion `skip`
- 적용 역할: list-surface, status-region
- 근거 팩: `harness-interaction-candidates`
- 가드레일:
  - Preferred when the user is scanning or comparing many rows at once.
  - Never animate position; only the content itself changes.
  - Keep a visible non-motion cue for what changed.

### emphasis · `attention-border`

State-bound attention border

- 마크업: `data-interaction="attention-border"`
- 모션: 180ms · `standard` · reduced-motion `static`
- 적용 역할: selection-target, status-region
- 근거 팩: `vibecoding-motion`
- 가드레일:
  - Never apply the animated border to every card by default.
  - Use semantic accent tokens only; no hard-coded effect colors.
  - Focus visibility must remain stronger and independent from decoration.

### progress · `skeleton-placeholder`

Reserving the shape of the incoming content prevents the layout shift that a centred spinner invites.

- 마크업: `data-interaction="skeleton-placeholder"`
- 모션: 1600ms · `standard` · reduced-motion `static`
- 적용 역할: list-surface
- 근거 팩: `harness-interaction-candidates`
- 가드레일:
  - The skeleton must match the real content's geometry, not a generic grey block.
  - Expose an accessible loading status; the shimmer is not an announcement.
  - Hold the shimmer to the loop budget and stop it as soon as content lands.

### transition · `context-crossfade`

A brief crossfade marks that the frame of reference changed while the surrounding chrome stayed put.

- 마크업: `data-interaction="context-crossfade"`
- 모션: 180ms · `standard` · reduced-motion `opacity-only`
- 적용 역할: list-surface, navigation-surface
- 근거 팩: `harness-interaction-candidates`
- 가드레일:
  - Chrome and navigation must not move during the fade.
  - Do not crossfade when the underlying data is identical.
  - Keep the outgoing and incoming content from overlapping legibly.

## 검토했지만 선택하지 않은 후보

- `surface-lift` (emphasis, 점수 12)
- `weight-shift` (emphasis, 점수 11)
- `anchored-shift` (transition, 점수 6)
- `determinate-bar` (progress, 점수 6)
- `result-reveal` (enter, 점수 6)
- `dot-progress` (progress, 점수 5)
- `staged-enter` (enter, 점수 5)
- `inline-expand` (enter, 점수 2)

