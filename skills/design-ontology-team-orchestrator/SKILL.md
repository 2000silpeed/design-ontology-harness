---
name: design-ontology-team-orchestrator
description: Coordinate the complete design-ontology harness team from product brief through production verification. Use when starting or resuming a harness project, assigning Codex or Claude Code specialists, choosing the next stage, writing handoffs, recovering from a failed gate, or auditing whether the UI is actually ready to release.
---

# Design Ontology Team Orchestrator

Read the project's `design-system/agent-team.json` and `design-system/TEAM_RUNBOOK.md` before dispatching work. If they do not exist, run `design-ontology init-agent-pack --targets codex,claude` first.

## Operate the team

1. Inspect current inputs, outputs, and gate evidence.
2. Select the earliest incomplete stage.
3. Dispatch only its owner. Run Token Curator and Component Contract Author in parallel only when they edit separate files.
4. Require changed paths, decisions, exact gate commands/results, risks, and next action.
5. Write a schema-valid handoff under `design-system/handoffs/` before changing owner.
6. Return failed work to the same owner with concrete evidence. Never weaken the gate.
7. Ask the Release Governor to run the final completion audit independently.

## Hard boundaries

- Do not let two writing agents edit the same file set concurrently.
- Do not let implementation begin while a component is `needs-authoring`.
- Read color authority from the checksum-verified Semantic OS graph embedded in `docs/color-reference.md`; do not infer final color values from screenshots.
- Do not treat visual references as palette, typography, IA, copy, or asset authority.
- Prefer Codex `image_gen` for required raster generation. If the active runtime has no image tool, write a prompt-packet handoff to Codex instead of claiming the asset exists.
- Do not accept screenshots captured before the current runtime tree.
- Do not claim production readiness unless `verify-production-ui` passes.

Read [references/team-contract.md](references/team-contract.md) when assigning roles or resolving an ownership conflict.
