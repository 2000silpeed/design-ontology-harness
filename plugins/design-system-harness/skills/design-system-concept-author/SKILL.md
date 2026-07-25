---
name: design-system-concept-author
description: Author product-specific application concept, layout skeleton, and differentiation fields before running design-ontology synthesis. Use when generated apps feel too similar, when the task is to create a new design system from the application concept rather than use a preset, or before run-project if brand_profile lacks application_concept, layout_skeleton, or design_differentiation.
---

# Design System Concept Author

Use this skill before running `design-ontology run-project`.

This is an LLM-authored step. Do not let deterministic defaults or a fixed rule table decide the product shape.

## Required Inputs

Read the user's brief, then read available project files:

- `projects/<name>/spec.md`
- `projects/<name>/brand_profile.json`
- `brand_profile.json`
- `spec.md`
- `agent-team/brand_profile.json`
- screenshots, mockups, or local visual references when provided

## Authoring Workflow

1. Extract the product's real first job.
2. Name the domain objects users inspect, create, compare, approve, move, buy, publish, or monitor.
3. Define the visible success moment.
4. Write `application_concept`.
5. Write `layout_skeleton` as a custom screen grammar, not a preset label.
6. Write `design_differentiation` with structural signature moves.
7. Author `component_decision.core_components` from the product primitives. Each component must define its own anatomy, domain states, content rules, accessibility contract, variants/props, interaction events, data contract, responsive behavior, and dos/don'ts. Family defaults are coverage references, not substitutes for domain contracts.
8. Update supporting fields when generic: `product_primitives`, `visual_keywords`, `interaction_keywords`.
9. Patch `brand_profile.json`.
10. Run or recommend:

```bash
uv run design-ontology run-project --project-dir projects/<name> --kb-dir kb/default
```

11. Verify the generated artifacts contain the authored decisions:
    - `build/system/blueprint/design_system_blueprint.json`
    - `build/system/blueprint/system_spec.md`
    - `build/system/blueprint/token_schema.json`
    - `build/system/blueprint/component_inventory.json`
    - `build/system/components/component_specs.json`
    - `build/system/components/component_contract_validation.json`
12. Run `design-ontology validate-component-contracts --project-dir projects/<name>`. Do not hand off to implementation while an authored contract is `needs-authoring`.

## Field Contract

```json
{
  "application_concept": {
    "primary_job": "",
    "domain_objects": [],
    "operating_mode": "",
    "success_moment": "",
    "differentiation": []
  },
  "layout_skeleton": {
    "composition": "",
    "navigation_model": "",
    "density": "",
    "primary_regions": [
      {"name": "", "role": "", "priority": "primary"}
    ],
    "first_screen_contract": [],
    "avoid_layouts": []
  },
  "design_differentiation": {
    "must_feel_different_from": [],
    "signature_moves": [],
    "repetition_risks": []
  },
  "component_decision": {
    "mode": "llm-authored",
    "rationale": "",
    "core_components": [
      {
        "name": "domain-component-name",
        "family": "content",
        "role": "",
        "supports_primitive": "",
        "decision_reason": "",
        "anatomy": ["root", "domain-content", "state-region", "action-slot"],
        "states": ["default", "domain-state"],
        "content_rules": [],
        "accessibility_notes": [],
        "variants": {"axes": [], "default": "default", "constraints": []},
        "props": {"state": {"type": "enum", "values": ["default", "domain-state"]}},
        "interaction": {"events": [], "state_transitions": [], "focus_behavior": "", "state_coverage": []},
        "data_contract": {"domain_object": "", "required_fields": [], "provenance_required": false, "empty_state_required": false},
        "responsive": {"required_widths_px": [320, 390, 768], "control_rules": [], "container_behavior": ""},
        "dos_and_donts": {"do": [], "dont": []}
      }
    ],
    "rejected_components": []
  }
}
```

## Anti-Convergence Gate

Before finishing, check:

- Would another unrelated app with similar brand keywords produce the same first viewport?
- Does `first_screen_contract` name actual above-the-fold regions, controls, state, or domain objects?
- Are `signature_moves` structural, not decorative?
- Did `product_primitives` follow from domain objects rather than generic components?
- Does every core component preserve a domain primitive, domain states, actual data fields, interaction events, and responsive behavior?
- Would `validate-component-contracts` pass without `--allow-needs-authoring`?
- Did you explicitly reject generic hero/card/dashboard layouts when they are not the user's real workflow?

## Rules

- Do not choose a preset.
- Do not solve sameness with more color, gradients, shadows, or component variants.
- Do not make every product a dashboard; dashboard is valid only when monitoring metrics is the first job.
- Do not open with a marketing hero unless the product is a landing page.
- Use Astryx and Geist only as component taxonomy and state-coverage references.
- Never let family defaults overwrite authored states or stand in for a missing domain component contract.
- Prefer concrete screen grammar over adjectives.
