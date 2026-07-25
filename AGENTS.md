# Design Ontology Harness agent rules

## Team contract

- Read `agent-team/agent-team.json` and `agent-team/TEAM_RUNBOOK.md` before coordinating multi-stage product-design work.
- Use `$design-ontology-team-orchestrator` for a new run, a resumed run, a failed gate, or a release audit.
- Dispatch the minimum specialist set for the earliest incomplete stage.
- Token Curator and Component Contract Author may run in parallel only when they own separate files. The Brief Author must reserve `component_decision_path` first.
- Never run overlapping write agents on the same files.
- Record owner changes under `agent-team/handoffs/` with `handoff.schema.json`.

## Source-of-truth order

1. Product brief, `spec.md`, and `brand_profile.json`
2. Semantic OS graph embedded in `docs/color-reference.md`
3. Generated ontology, tokens, and authored component contracts
4. Reviewed visual assets and browser evidence
5. Advisory reference imagery

Reference images may influence morphology, density, hierarchy, and interaction affordances. They may not define final palette, typography, IA, product copy, logos, or redistributable assets.

## Required gates

```bash
uv run pytest tests/test_agent_team.py tests/test_agent_packs.py -q
uv run design-ontology validate-agent-team --target-repo . --artifact-dir agent-team --targets codex,claude
uv run design-ontology validate-component-contracts --project-dir projects/<name>
uv run design-ontology lint-implementation --target-repo <implementation-repo>
uv run design-ontology reference-fidelity-loop --project-dir projects/<name> --target-repo <implementation-repo> --review-artifact <paired-review.json>
uv run design-ontology verify-production-ui --project-dir projects/<name> --target-repo <implementation-repo>
```

- Do not implement components marked `needs-authoring`.
- Do not accept stale screenshots after implementation, token, theme, or asset changes.
- When an approved-reference fidelity contract exists, do not route directly from UI implementation to Production QA. Run the independent fidelity stage first; a failed review returns to UI implementation with a correction brief and fresh-evidence requirement.
- Do not claim production readiness unless the Release Governor independently confirms `verify-production-ui` passed.

## Repository hygiene

- Preserve unrelated user changes in this dirty worktree.
- Edit files with `apply_patch` when practical.
- Keep generated artifacts generated; change their authored source and rerun the generator instead of patching outputs by hand.
