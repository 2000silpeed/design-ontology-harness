# slowread-archive — 인터랙션 계약

`design-system/interactions.css`가 이 계약의 실행 가능한 형태입니다.
선택되지 않은 패턴을 구현하거나 여기 없는 모션을 추가하면 린터가 막습니다.

- 선택 방식: `contextual-variation`
- 변동 시드: `11`

## 선택된 패턴

### enter · `staged-enter`

A short stagger communicates that several items arrived together without implying they are ranked.

- 마크업: `data-interaction="staged-enter"`
- 모션: 180ms · `enter` · reduced-motion `opacity-only`
- 적용 역할: list-surface
- 근거 팩: `harness-interaction-candidates`
- 가드레일:
  - Cap the stagger so the last item is not perceptibly late.
  - Never stagger more than one screen of items.
  - Drop to a single opacity change when reduced motion is requested.

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

### transition · `anchored-shift`

Moving a single shared anchor between positions explains the relationship between two views better than fading both.

- 마크업: `data-interaction="anchored-shift"`
- 모션: 240ms · `emphasized` · reduced-motion `static`
- 적용 역할: navigation-surface
- 근거 팩: `harness-interaction-candidates`
- 가드레일:
  - Exactly one anchor element may move per transition.
  - The anchor must exist in both the outgoing and incoming state.
  - Snap the anchor into place immediately under reduced motion.

## 검토했지만 선택하지 않은 후보

- `context-crossfade` (transition, 점수 6)
- `immediate-swap` (enter, 점수 5)
- `inline-expand` (enter, 점수 4)
- `result-reveal` (enter, 점수 3)

