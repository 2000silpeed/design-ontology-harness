# VibeCoding Motion Reference Pack

## Purpose

`vibecoding-motion-reference.json` is a small semantic fixture for turning visual
VibeCoding references into design-system evidence. It is not a collection of
copied CSS, screenshots, prompts, or redistributable assets.

The pack uses existing harness concepts:

```text
SourceReference
  → InteractionPattern
  → ComponentState
  → MotionToken
  → AccessibilityRule / GovernanceRule
```

## Current status

- `status`: `reviewed` (2026-08-12)
- Provenance: `inspected` — every URL confirmed by the user

| Source | URL | License status |
|---|---|---|
| Originkit | https://www.originkit.dev | `reference-only` |
| Magic UI (Border Beam) | https://magicui.design | `verified` (MIT) |
| MotionSites | https://motionsites.ai | `reference-only` · **paid product** |
| Dot Matrix | https://dotmatrix.zzzzshawn.cloud | `reference-only` |
| VibeHub | https://vibe-hub.org | `reference-only` |

"Border Beam" turned out to be a component of **Magic UI** rather than a
standalone library, which is why that source points at the library root. Magic
UI is MIT, so it is the one `verified` entry; the rest stay `reference-only`
because their licence text was not read.

**MotionSites sells its prompts.** Never copy prompt text, prompt fragments, or
preview media into this repository — only the interaction morphology.

`stable` is still unclaimed. It would require reading each licence rather than
applying a conservative reference-only boundary.

## Pattern routing

| Pattern | Default use | Dashboard rule |
|---|---|---|
| `interaction:result-reveal` | New result/content enters | 180ms enter motion; no layout-critical movement |
| `interaction:attention-border` | Selected or attention-required state | Never a default card decoration |
| `interaction:dot-progress` | Loading, agent-working, refresh | Persistent accessible status text required |
| `interaction:prompt-vocabulary` | AI-facing UI terminology | Vocabulary cannot replace domain contracts |
| `interaction:showcase-morphology` | Landing/showcase composition | Advisory only; not a dense workspace default |

## Dashboard pilot contract

The `dashboard--minimal-tech` preset already defines the compatible motion
scale: `80/120/180/240/320ms` and `standard/enter/exit/emphasized` easing. The
fixture test confirms every pack pattern stays inside that scale and retains the
preset's `low-noise motion` interaction keyword.

## Verification

```bash
uv run pytest tests/test_motion_reference.py -q
```

This verifies source provenance fields, pattern ontology type, token-scale
compatibility, reduced-motion coverage, and required governance rules.
