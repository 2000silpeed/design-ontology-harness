---
name: design-system-reference-inspect
description: Use website reference inspection outputs safely while implementing local design-system screens. This skill translates inspect-reference-site artifacts into advisory morphology, density, hierarchy, and interaction guidance without cloning protected site assets.
---

# Design System Reference Inspect

Use this skill when the repository has outputs from `inspect-reference-site` and the implementation should learn from a reference website without copying it.

Read `agent-team/agent-team.json` and the latest file under `agent-team/handoffs/` first. Return the advisory plan to the Team Lead; do not change stage ownership yourself.

## Required Inputs

Read these files first when they exist:

- `agent-team/IMPLEMENTATION_CONTRACT.md`
- `agent-team/STYLE.md` or `agent-team/DESIGN.md`
- `agent-team/system_spec.md`
- `agent-team/token_schema.json`
- `agent-team/components/component_specs.md`
- `agent-team/components/component_specs.json`
- `agent-team/design_context_pack.json`
- `agent-team/website_research/design_context_pack.json`
- `build/website_research/design_context_pack.json`
- `docs/website_research/design_context_pack.json`
- `build/website_research/PAGE_TOPOLOGY.md`
- `build/website_research/BEHAVIORS.md`
- `build/website_research/website_reference_report.json`

If no website inspection artifact exists, ask the user to generate one from the harness:

```bash
uv run design-ontology inspect-reference-site --project-dir <project> --url <url> --sync-brand-profile
```

## Authority Order

The local design system wins:

1. Product task flow and existing feature behavior
2. `agent-team/token_schema.json`
3. `agent-team/components/component_specs.*`
4. `agent-team/system_spec.md` and `agent-team/system_ontology.json`
5. Website reference inspection context

## Allowed Absorption

You may use reference inspection for:

- component morphology
- layout density
- panel/card proportions
- hierarchy rhythm
- interaction affordance patterns
- flow pattern labels
- scroll-aware vs click/input-driven interaction modeling

## Denied Absorption

Never copy from the reference website:

- color palette or palette composition
- typography scale or font choices
- domain information architecture
- product copy, navigation labels, marketing copy, or legal copy
- logos, icons, favicons, screenshots, photos, videos, or other runtime assets unless explicit license metadata exists
- raw CSS values as implementation tokens
- pixel-perfect layout intent unless the user owns the original and explicitly changes scope

## Implementation Workflow

1. Summarize observed sections from `PAGE_TOPOLOGY.md`.
2. Summarize behaviors from `BEHAVIORS.md`: static, click/input-driven, scroll-aware, time-driven.
3. Check component specs for `Observed Reference Evidence`.
4. Map each relevant observation to local component families and states.
5. Implement using local semantic tokens and component anatomy.
6. Reject any reference trait that violates denied absorption.
7. Verify with `lint-implementation`, desktop/mobile screenshots, overflow checks, and light/dark mode checks.

## Output Expectations

- State which reference inspection files were used.
- List absorbed advisory traits.
- List rejected traits and why.
- State which local design-system artifacts stayed authoritative.
- Mention any screenshot or behavior QA still needed.
