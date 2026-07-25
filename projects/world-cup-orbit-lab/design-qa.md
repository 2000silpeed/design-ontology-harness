# Design QA — blocked

- **Source visual truth:** `assets/watch-compass-reference.png`
- **Implementation target:** `index.html` served from `http://127.0.0.1:4173/`
- **Target viewport:** desktop, 1440 × 1024
- **Target state:** Japan v Morocco selected; Seoul local time; Follow match idle.

## Findings

- [P1] Browser-rendered visual comparison is unavailable.
  - Location: in-app browser session.
  - Evidence: the browser session reported no accessible tabs when opening the local prototype, so no implementation screenshot could be captured or placed beside the source visual.
  - Impact: typography, region proportions, responsive behavior, and generated-asset fidelity cannot be truthfully verified.
  - Fix: reconnect an in-app browser session, capture the target viewport, exercise stage/match/timezone/follow controls, then compare that capture with the source mockup.

- [P2] Production implementation lint is not yet green.
  - Location: `index.html`, `styles.css`, visual-asset manifest.
  - Evidence: `lint-implementation` reports unregistered runtime imagery and responsive-control constraints.
  - Impact: the harness cannot yet certify the prototype as a release-ready implementation.
  - Fix: finish visual-asset promotion against authored component contracts, remove non-token/fragile styling patterns, and rerun the linter.

## Open Questions

- The selected image is the sole visual target; the existing World Cup Hub is intentionally out of scope.

## Implementation Checklist

1. Restore browser capture access and take the desktop implementation screenshot.
2. Test fixture selection, stage selection, timezone selection, and Follow match state.
3. Resolve lint failures and run the same screenshot comparison again.

## Follow-up Polish

- Tune exact visual rhythm after the first rendered side-by-side comparison.

**final result: blocked**
