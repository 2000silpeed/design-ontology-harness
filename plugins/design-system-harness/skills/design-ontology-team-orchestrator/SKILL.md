---
name: design-ontology-team-orchestrator
description: Coordinate the complete design-ontology harness team from product brief through production verification. Use when starting or resuming a harness project, assigning specialist agents, choosing the next stage, writing handoffs, recovering from a failed gate, or operating the same workflow in Codex and Claude Code.
---

# Design Ontology Team Orchestrator

Read `agent-team/agent-team.json` and `agent-team/TEAM_RUNBOOK.md` before dispatching work.

1. Inspect current artifacts and gate evidence.
2. Select the earliest incomplete stage.
3. Dispatch only its owner; parallelize only read-only research or the file-separated token/component pair.
4. Require the owner to return changed paths, decisions, gate commands, results, and remaining risks.
5. Write a schema-valid handoff to `agent-team/handoffs/` before changing stage owner.
6. On gate failure, return work to the same owner with the failed evidence. Do not weaken the gate.
7. After implementation freeze, require the reference fidelity stage before Production QA. A failed paired review returns to implementation with fresh correction evidence.
8. Finish only when the release governor independently runs `verify-production-ui` successfully.

Never let the lead silently perform specialist implementation or let implementation start while component contracts are `needs-authoring`. Read colors from the synchronized Semantic OS graph in `docs/color-reference.md`, not from screenshots. Use Codex `image_gen` for required raster generation; a runtime without an image tool must write a handoff instead of claiming the asset exists. Approved references can govern only explicitly authored composition, morphology, density, hierarchy, task-visibility, responsive-translation, and context-linkage invariants; they never govern palette, typography, IA, copy, logos, or redistributable assets.
