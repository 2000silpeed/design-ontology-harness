# Design Ontology Agent Team

This repository uses one shared team contract for Codex and Claude Code. The models may differ; role ownership, handoffs, artifacts, and release gates do not.

## Start here

1. Read `agent-team/agent-team.json`.
2. Ask the team lead to identify the first missing stage output.
3. Dispatch only that stage owner.
4. Save every stage transition under `agent-team/handoffs/` using `handoff.schema.json`.
5. Stop on a failed gate. Never route around it by changing the success criteria.

## Runtime entry points

### Codex

Install the generated local plugin once, then start with the orchestrator skill:

```bash
codex plugin marketplace add .
codex plugin add design-system-harness --marketplace local-plugins
codex 'Use $design-ontology-team-orchestrator to inspect the current project and run the next required stage.'
```

### Claude Code

Start the generated team lead directly:

```bash
claude --agent design-team-lead
```

Then ask: `Inspect agent-team/agent-team.json and run the next required stage.`

## Team operating rule

The team is a gated pipeline, not a panel of agents all editing at once. The lead dispatches the minimum role set. Read-only research may run in parallel. The only parallel writers are the Token Curator and Component Contract Author after their files are separated. Visual asset production finishes before UI implementation starts. After implementation freeze, the Approved-Reference Fidelity Auditor runs before Production QA. A failed fidelity gate returns to the UI Implementer with a correction brief; it never changes the approved contract.

The Token Curator reads the checksum-verified Semantic OS graph embedded in `docs/color-reference.md`. It owns `color_reference` and `font_system` in the project profile. The Component Contract Author writes a separate `design-system/component-contracts.json`, so those two roles can run safely in parallel after the Brief Author reserves `component_decision_path`.

When raster generation is needed, the Visual Asset Producer prefers Codex `image_gen`. A Claude Code run may prepare the prompt packet and review criteria, but if no image tool is available it must hand generation to Codex and keep the asset gate open.

## Release sequence

```bash
uv run design-ontology validate-component-contracts --project-dir <project>
uv run design-ontology emit-tokens --project-dir <project>
uv run design-ontology lint-implementation --target-repo <implementation-repo>
uv run design-ontology check-style-divergence --project-dir <implementation-repo> --register-on-pass
uv run design-ontology reference-fidelity-loop --project-dir <project> --target-repo <implementation-repo> --review-artifact <paired-review.json>
uv run design-ontology verify-production-ui --project-dir <project> --target-repo <implementation-repo>
```

Only the release governor may report production readiness, and only after the final command passes against current runtime evidence.
