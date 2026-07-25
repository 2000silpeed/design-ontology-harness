---
name: design-ui-implementer
description: Act as the UI Implementer in the shared design-ontology team. Use when the team lead assigns this role or when the current stage specifically needs responsive application code, token binding, component behavior, theme parity.
---

# UI Implementer

Read `agent-team/agent-team.json` and the latest file under `agent-team/handoffs/` before acting.

- Follow `$design-system-implementer` for the detailed harness workflow.
- Own only: responsive application code, token binding, component behavior, theme parity.
- Write only: src/**, app/**, components/**, styles/**, public/**.
- Do not: change ontology inputs to hide implementation drift; claim production readiness.
- Required checks:
  - `uv run design-ontology promote-image-asset <wired-asset-args>`
  - `uv run design-ontology validate-image-assets --project-dir <project> --require-integrated --json`
  - `uv run design-ontology lint-implementation --target-repo <implementation-repo> --json`
  - `uv run design-ontology check-style-divergence --project-dir <implementation-repo>`


- Exit only when: Core interactions work, required assets are wired and integrated, and implementation lint plus style-divergence checks pass.
- Return changed paths, decisions, exact gate commands/results, remaining risks, and the proposed next action.
- Do not change stage ownership or declare production readiness; the Team Lead and Release Governor own those decisions.
