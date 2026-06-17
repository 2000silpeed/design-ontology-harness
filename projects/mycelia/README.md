# Mycelia

Image-first site design project (`workflow: site-design-image-first`).

## Flow

1. Fill `concept_brief.md` (project + concept) and `color_set.json`.
2. For each surface, generate a screen with the GPT Image 2 skill
   (`generate_image`, model `gpt_image_2`), save to `generated/<surface>.png`,
   and record the prompt + job_id in `screen_plan.json`.
3. Derive the design system from the screens into `design-system/`.
4. Validate:

```bash
uv run design-ontology check-site-design --project-dir projects/mycelia
```

Rules: images first, system second. Ontology for grounding only. Never copy
presets / existing projects / fixtures.
