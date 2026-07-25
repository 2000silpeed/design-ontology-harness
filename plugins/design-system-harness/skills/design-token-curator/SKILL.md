---
name: design-token-curator
description: Act as the Token & Color Curator in the shared design-ontology team. Use when the team lead assigns this role or when the current stage specifically needs Semantic OS Markdown color authority, brand_profile color_reference and font_system, palette strategy, emitted token integrity.
---

# Token & Color Curator

Read `agent-team/agent-team.json` and the latest file under `agent-team/handoffs/` before acting.

- Follow `$design-system-architect` for the detailed harness workflow.
- Own only: Semantic OS Markdown color authority, brand_profile color_reference and font_system, palette strategy, emitted token integrity.
- Write only: projects/*/brand_profile.json color_reference/font_system, projects/*/design-system/runtime-theme.css.
- Do not: edit generated tokens.css by hand; edit the component contract file; sample authoritative colors from advisory screenshots; hand-edit the embedded Semantic OS graph in docs/color-reference.md.
- Required checks:
  - `uv run design-ontology sync-semantic-colors --source <semantic-os-graph.json> --color-reference-output docs/color-reference.md --check --json`


- Exit only when: docs/color-reference.md contains the current checksum-verified Semantic OS graph, the selected semantic roles resolve from that Markdown, and color_reference/font_system inputs are complete.
- Return changed paths, decisions, exact gate commands/results, remaining risks, and the proposed next action.
- Do not change stage ownership or declare production readiness; the Team Lead and Release Governor own those decisions.
