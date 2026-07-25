---
name: design-system-architect
description: Plan token structure, component architecture, and rollout order using the repository's design-system artifacts. Use when the task requires alignment decisions before implementation.
---

# Design System Architect

Use this skill when working on planning or architectural questions related to the local design system.

## Required Inputs

Read these files first when they exist:

- `agent-team/IMPLEMENTATION_CONTRACT.md`
- `agent-team/STYLE.md` or `agent-team/DESIGN.md`
- `agent-team/system_spec.md`
- `agent-team/token_schema.json`
- `agent-team/component_inventory.json`
- `agent-team/components/component_specs.json`
- `agent-team/components/component_contract_validation.json`
- `agent-team/system_ontology.json`

## Workflow

1. Identify the relevant principles from `system_spec.md`.
2. Map the request to token categories and component families.
3. Prefer extending an existing primitive over introducing a new abstraction.
4. Call out any conflict with anti-keywords or missing system coverage.
5. Preserve existing surface structure and user flows unless the task explicitly asks to replace them.
6. Produce a concise, incremental implementation plan the coding agent can follow.
7. Use curated palette roles from the token schema as the default color direction when available.
8. If typography script guardrails exist, incorporate them into headline scale, measure, and Korean copy wrapping decisions up front.
9. Plan button/action-group mobile behavior up front: wrap, stack, or prove it fits at 320px without horizontal scroll.
10. Plan light/default and dark mode token coverage up front; light is the default mode.
11. Treat the app icon as a required brand identity asset, not a generic initials tile.
12. For dashboard/tool/data/community products, plan the first viewport around operational state, filters, data rows, and provenance before hero imagery.
