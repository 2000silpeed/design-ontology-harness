# ThreadSense

This folder is a self-contained harness project built on top of `design-ontology-harness`.

## Files

- `brand_profile.json`: your system identity and product context
- `seeds/seed_urls.txt`: curated reference entry points
- `project_manifest.json`: project metadata
- `agent_brief.md`: instructions for human or agent collaborators
- `design-system.md`: persistent brand, skeleton, token, and component contract
- `index.html`, `styles.css`, `app.js`: static mobile mock UI
- `build/`: generated outputs

## How To Run

```bash
uv run design-ontology run-project --project-dir projects/fashion-curation-mobile
```

Open the mock directly:

```bash
open projects/fashion-curation-mobile/index.html
```

## Recommended Flow

1. Fill in `brand_profile.json`
2. Set or override the KB path if needed
3. Run the project
4. Review `build/system/blueprint/system_spec.md`
5. Use `design-system.md` and the static mock as the implementation baseline
