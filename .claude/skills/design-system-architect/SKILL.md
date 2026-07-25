---
name: design-system-architect
description: Align implementation plans and UI decisions with the project's design-system artifacts. Use when deciding token structure, component families, primitives, or rollout order.
allowed-tools: Read Glob Grep Bash
paths:
  - "agent-team/**"
  - "src/**"
  - "app/**"
  - "components/**"
  - "styles/**"
---

When this skill is active:

1. Read `agent-team/STYLE.md` or `agent-team/DESIGN.md` first when present.
2. Read `agent-team/system_spec.md`.
3. Read `agent-team/token_schema.json` and `agent-team/component_inventory.json`.
4. If present, use `agent-team/system_ontology.json` to understand relations between principles, token categories, and component families.
5. Translate user requests into:
   - affected principles
   - affected token categories
   - affected component families
   - required implementation order
6. Favor extending existing primitives over inventing new components.
7. Explicitly guard against anti-keywords from the system spec.
8. Preserve existing user-facing entry points and feature surfaces unless the user explicitly asks for a structural change.
9. Prefer incremental rollout plans over full-shell rewrites.
10. If `token_schema.json` contains a curated color reference or palette roles, treat that as the starting point for semantic color decisions.
11. If typography artifacts include script guardrails, account for their line-break and type-scale rules before proposing hero or landing compositions.
12. Treat responsive resilience as a planning constraint: buttons and action groups need a mobile wrap/stack strategy before implementation begins.
13. For dashboard/tool/data/community products, plan the first viewport around the operational task surface before considering hero imagery or feature cards.

If any artifact file is missing, say exactly which file is missing and recommend syncing artifacts from the harness repo before implementation.
