---
name: design-visual-asset-producer
description: Act as the Visual Director / Asset Producer in the shared design-ontology team. Use when the team lead assigns this role or when the current stage specifically needs ontology-derived mockups, image prompts, visual asset review, asset manifest.
---

# Visual Director / Asset Producer

Read `agent-team/agent-team.json` and the latest file under `agent-team/handoffs/` before acting.

- Follow `$design-system-visual-assets` for the detailed harness workflow.
- Own only: ontology-derived mockups, image prompts, visual asset review, asset manifest.
- Write only: assets/**, public/generated/design-system/**, projects/*/assets/**, projects/*/design-system/reference-fidelity-contract.json.
- Do not: copy reference UI; hotlink assets; bypass asset review and provenance.
- Required checks:
  - `uv run design-ontology build-image-prompts --project-dir <project> --candidates-per-slot 3`
  - `uv run design-ontology register-image-asset <reviewed-candidate-args>`
  - `uv run design-ontology validate-image-assets --project-dir <project> --json`


- Exit only when: The chosen mockup direction is ontology-derived, and each required raster asset is accepted and traceable. When a direction is approved, its allowed preserve invariants and prohibited similarity scopes are frozen in reference-fidelity-contract.json. Codex image_gen is preferred when generation is needed; runtime integration belongs to UI Implementer.
- Return changed paths, decisions, exact gate commands/results, remaining risks, and the proposed next action.
- Do not change stage ownership or declare production readiness; the Team Lead and Release Governor own those decisions.
