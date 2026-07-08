# Output Contract

Use this reference when editing `brand_profile.json` for a harness project.

## `application_concept`

```json
{
  "primary_job": "The task the user must complete first.",
  "domain_objects": ["Objects the product is really about."],
  "operating_mode": "review | monitoring | authoring | transaction | exploration | coordination | custom phrase",
  "success_moment": "The visible state that proves the workflow succeeded.",
  "differentiation": ["Structural differences from a generic app."]
}
```

Write domain objects as nouns users would recognize: `claim`, `evidence item`, `draft`, `shipment`, `venue`, `match`, `order`, `candidate`, `case`, `thread`.

## `layout_skeleton`

```json
{
  "composition": "A compact phrase for the first-screen grammar.",
  "navigation_model": "sidebar | topbar | task-rail | local-tabs | command-palette | stage-flow | none | custom phrase",
  "density": "dense | balanced | spacious",
  "primary_regions": [
    {
      "name": "Region name",
      "role": "What the user does here",
      "priority": "primary | secondary | tertiary"
    }
  ],
  "first_screen_contract": [
    "Concrete above-the-fold requirement that an implementation can pass or fail."
  ],
  "avoid_layouts": [
    "Generic layout failures this product must not collapse into."
  ]
}
```

Good `composition` examples:

- `split evidence workbench`
- `queue-led review console`
- `document canvas with inspector rail`
- `map-first local discovery surface`
- `timeline ledger with decision drawer`
- `feed-detail moderation cockpit`
- `marketplace comparison grid`
- `wizard flow with persistent summary`

Bad `composition` examples:

- `dashboard`
- `modern app`
- `clean SaaS`
- `professional layout`
- `cards`

## `design_differentiation`

```json
{
  "must_feel_different_from": ["generic SaaS dashboard", "template landing page"],
  "signature_moves": [
    "A workflow-specific structural move that must survive implementation."
  ],
  "repetition_risks": [
    "Specific failure modes that made previous apps look similar."
  ]
}
```

Signature moves must change structure or interaction, not decoration.

Good:

- `Queue and selected case remain co-present on desktop.`
- `The first viewport starts with a map and time filter, not a hero headline.`
- `Every recommendation row exposes source trail and confidence before CTA.`
- `The editor canvas is primary; assistant suggestions stay in a narrow inspector rail.`

Weak:

- `Use a fresh color palette.`
- `Make it premium.`
- `Use rounded cards.`
- `Add microinteractions.`

## Supporting Fields

Update these if they are still generic:

```json
{
  "product_primitives": [
    "domain-object queue",
    "detail inspector",
    "source ledger",
    "decision action bar"
  ],
  "visual_keywords": [
    "inspectable",
    "structured",
    "evidence-led"
  ],
  "interaction_keywords": [
    "compare",
    "triage",
    "commit decision"
  ]
}
```

`product_primitives` should describe product surfaces, not only generic components. Use `table`, `button`, and `card` only when the product object actually calls for them.

## Anti-Convergence Checklist

Reject or revise the profile if:

- `first_screen_contract` could apply to five unrelated apps.
- `signature_moves` describe visual styling instead of screen structure.
- `domain_objects` are missing or generic (`data`, `content`, `users`) when the product has specific nouns.
- `avoid_layouts` does not mention the failure pattern the user complained about.
- `product_primitives` is only generic UI components.
