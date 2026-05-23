# Seoul Alley Mood Map

Design ontology harness smoke project for a mobile-first sensory place curation app.

## Files

- `brand_profile.json`: your system identity and product context
- `seeds/seed_urls.txt`: curated reference entry points
- `project_manifest.json`: project metadata
- `agent_brief.md`: instructions for human or agent collaborators
- `build/`: generated harness outputs
- `design-system/`: installed preset artifacts and raw CSS variables
- `index.html`, `styles.css`, `app.js`: static ontology-bound UI mock

## How To Run

```bash
uv run design-ontology run-project --project-dir projects/seoul-alley-mood-map
```

To preview the mock:

```bash
python3 -m http.server 8042
```

Open `http://127.0.0.1:8042/` from this folder.

## Recommended Flow

1. Fill in `brand_profile.json`
2. Set or override the KB path if needed
3. Run the project
4. Review `build/system/blueprint/system_spec.md`
