---
name: design-ontology-concept-author
description: Author the app concept, layout skeleton, and differentiation fields for a design-ontology-harness project before running synthesis. Use when creating or revising `brand_profile.json`/`spec.md`, when the user says the generated apps feel too similar, when the goal is not to pick a preset but to rewrite color, font, layout, and design system from the application's concept and screen structure, or before `design-ontology run-project` if `application_concept`, `layout_skeleton`, or `design_differentiation` are missing or generic.
---

# Design Ontology Concept Author

## Purpose

Use this skill to make the calling LLM an active design-system author. Do not let the harness infer the app shape from rules alone.

The LLM must read the product idea, existing `spec.md`, and `brand_profile.json`, then write the concept fields that steer synthesis:

- `application_concept`
- `layout_skeleton`
- `design_differentiation`
- supporting `product_primitives`, `visual_keywords`, and `interaction_keywords`

## Workflow

1. Read the available inputs:
   - User brief in the conversation
   - `projects/<name>/spec.md`
   - `projects/<name>/brand_profile.json`
   - Relevant screenshots, mockups, or visual references if the user provided them
2. Extract the product's actual job:
   - What is the user trying to finish?
   - What domain objects are inspected, created, compared, moved, approved, rejected, bought, published, or monitored?
   - What state proves the workflow succeeded?
3. Author the layout skeleton as a design judgment, not a preset lookup:
   - Use a custom `composition` phrase when needed. Do not restrict yourself to a fixed enum.
   - Choose the navigation model from the workflow, not from common SaaS templates.
   - Define primary regions by user attention and task order.
   - Write a concrete first-screen contract that can fail review if ignored.
4. Write differentiation pressure:
   - Name what this product must not collapse into.
   - Add one or more signature structural moves tied to the workflow.
   - Add repetition risks the implementation agent should actively avoid.
5. Patch `brand_profile.json`.
6. Run or recommend:

```bash
uv run design-ontology run-project --project-dir projects/<name> --kb-dir kb/default
```

7. Inspect the generated output:
   - `build/system/blueprint/design_system_blueprint.json`
   - `build/system/blueprint/system_spec.md`
   - `build/system/blueprint/token_schema.json`

## Output Contract

Read `references/output-contract.md` when writing or reviewing the fields.

Minimum shape:

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
    "primary_regions": [],
    "first_screen_contract": [],
    "avoid_layouts": []
  },
  "design_differentiation": {
    "must_feel_different_from": [],
    "signature_moves": [],
    "repetition_risks": []
  }
}
```

## Judgment Rules

- Do not pick a preset.
- Do not solve sameness by adding more colors, gradients, shadows, or card variants.
- Do not make every tool a dashboard. A dashboard is valid only when monitoring metrics is the user's real first job.
- Do not open with a marketing hero unless the product is actually a landing page.
- Do not let Astryx or Geist decide visual identity. Use them only as component taxonomy and state-coverage references.
- Prefer concrete screen grammar over adjectives. "split evidence workbench with queue and detail co-present" is better than "professional, clean, trustworthy".
- If the brief is vague, make the strongest reasonable interpretation and mark assumptions in `design_differentiation.repetition_risks` or in the final note.

## Review Gate

Before finishing, answer these internally:

- Would another app with the same `brand_keywords` produce the same first screen? If yes, sharpen `layout_skeleton`.
- Can an implementation agent tell what must appear above the fold? If no, rewrite `first_screen_contract`.
- Are `signature_moves` structural rather than decorative? If no, rewrite them.
- Did `product_primitives` follow from domain objects and jobs? If no, revise them.
- Could the result still become a generic hero plus card grid or uniform dashboard? If yes, add that failure to `avoid_layouts` and `repetition_risks`.
