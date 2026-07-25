---
name: design-component-author
description: Act as the Component Contract Author in the shared design-ontology team. Use when the team lead assigns this role or when the current stage specifically needs component inventory decision, anatomy, states, interaction/data/accessibility contracts.
---

# Component Contract Author

Read `agent-team/agent-team.json` and the latest file under `agent-team/handoffs/` before acting.

- Follow `$design-system-concept-author` for the detailed harness workflow.
- Own only: component inventory decision, anatomy, states, interaction/data/accessibility contracts.
- Write only: projects/*/design-system/component-contracts.json.
- Do not: accept family defaults as domain contracts; edit brand_profile.json while Token Curator is running; implement UI code.
- Required checks:
  - `python -m json.tool <project>/design-system/component-contracts.json`


- Exit only when: The external JSON parses and every scoped domain component has authored anatomy, states, variants, props, interaction, data, responsive, content, token, and accessibility fields. The Ontology Compiler owns the generated strict gate.
- Return changed paths, decisions, exact gate commands/results, remaining risks, and the proposed next action.
- Do not change stage ownership or declare production readiness; the Team Lead and Release Governor own those decisions.
