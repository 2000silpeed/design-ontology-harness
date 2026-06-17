---
name: site-design
description: >-
  Use when the user asks to design a site / 사이트 디자인 / product UI from scratch.
  Runs the image-first site design workflow: understand the project, decide one
  design concept, build a matching color set, generate per-feature screen images
  with the built-in GPT Image 2 skill (generate_image, model gpt_image_2), then DERIVE the design system
  (tokens, components, fonts) from those generated screens. The ontology is used
  only for grounding/validation — never copy presets, existing projects, or test
  fixtures.
---

# Site Design (Image-First)

When a user requests a site/product design, follow these 6 steps **in order**.
Full rationale: `docs/SITE_DESIGN_WORKFLOW.md`. Scaffolding: `init-site-design`.

## Hard rules

- **Images come first, the system comes second.** Never produce `token_schema.json`
  / `component_inventory.json` before the feature screens exist in `generated/`.
- **Use the ontology, never follow our test cases.** `semantic_color_ontology.json`
  and the graph schema are *vocabulary/relationship* grounding only. Do **not** copy
  colors/fonts/tokens/layouts from `presets/*`, existing `projects/*` (glacier,
  signal-desk, …), or `tests/fixtures/*`. Do not run the preset matcher to fill in
  output. Every run must yield a system unique to *this* project's generated images.
- Image generation uses the built-in GPT Image 2 skill: `generate_image`, model
  `gpt_image_2`, `aspect_ratio: "16:9"`, `resolution: "2k"`, `quality: "high"`.

## Steps

### 1. Understand the project
Read the request (+ `spec.md` / `brand_profile.json` if present). Write the top of
`concept_brief.md`: one-line product, primary users, **feature surfaces** (the list
of screens to generate), tone, anti-keywords.

### 2. Decide ONE design concept
Pick a single, named concept (e.g. "Field Guide Naturalism"): one sentence + 3–5
adjectives + explicit anti-patterns. Validate the wording against ontology
keyword/mood vocabulary. Do **not** pick a concept from a preset.

### 3. Build a matching color set
Create `color_set.json`: dominant / supporting / neutral / accent + state colors,
each with hex, intent, and a WCAG note. Ground role choices in
`semantic_color_selector` (ontology-search-per-run) but do **not** paste a prebuilt
palette. This set is the color spec for the image prompts.

### 4. Generate per-feature screen images
For **each** feature surface from step 1, call `generate_image` (model `gpt_image_2`). Each prompt must
include: the concept sentence + adjectives, the step-3 colors (role → hex), the
screen's functional layout (regions/components that must appear), an explicit "UI
product screen / interface mockup" instruction, and anti-keywords (e.g. "no
stock-photo collage, no emoji icons, no default Tailwind blue"). Keep header,
type, corners, and density consistent across screens. Save each result to
`generated/<surface>.png` and record prompt + job_id + intended components in
`screen_plan.json`.

### 5. Derive the design system from the images
Look at the generated screens and reverse-derive into the standard output formats
under `design-system/`:
- **colors** → semantic tokens (reconcile with the step-3 set) → `token_schema.json`
- **fonts** → display/heading/body moods → pick real families via `font_reference`
- **components** → what appears on screen + states/anatomy → `component_inventory.json`
- **form language** → corner/elevation/density/surface → `system_spec.md` + `STYLE.md`
Tag provenance `derived_from: generated-screens` and note the source screen per token.

### 6. Ground with the ontology (no test-case copying)
Validate/enrich against the ontology: color tokens ↔ semantic_color keywords/moods,
components ↔ graph ComponentFamily/has_state/requires, contrast_pair ↔ WCAG. Run
`check-site-design` to confirm screens↔plan↔tokens are consistent and that no tokens
were copied verbatim from presets/projects/fixtures. The result must be unique to
this project's generated images.

## Typical flow
```
uv run design-ontology init-site-design --project-dir projects/<slug> \
  --brand-name "…" --product-summary "…" --concept "…" \
  --surface <s1> --surface <s2> --surface <s3>
# steps 2–3: edit concept_brief.md + color_set.json
# step 4: generate_image per surface → generated/*.png + screen_plan.json
# steps 5–6: write design-system/* then:
uv run design-ontology check-site-design --project-dir projects/<slug>
```
