# Geist Reference

This folder is a self-contained harness project built on top of `design-ontology-harness`.

## Files

- `brand_profile.json`: your system identity and product context
- `seeds/seed_urls.txt`: curated reference entry points
- `project_manifest.json`: project metadata
- `agent_brief.md`: instructions for human or agent collaborators
- `build/`: generated outputs

## How To Refresh The Geist Extraction

```bash
uv run python scripts/extract-geist-reference.py \
  --output-dir projects/geist-reference/research/geist \
  --mirror-build-system
```

## Generated Artifacts

- `research/geist/manifest.json`: capture manifest and policy
- `research/geist/component_catalog.json`: all extracted Geist component pages
- `research/geist/pages/*.json`: one metadata-only record per Geist page
- `research/geist/token_refs.json`: observed CSS custom property identifiers
- `research/geist/components/component_specs.json`: local component specs derived from the public docs
- `build/system/blueprint/component_inventory.json`: harness-compatible component inventory
- `build/system/components/component_specs.json`: harness-compatible component specs

## Policy

This project stores metadata only: component names, taxonomy, section headings, import/JSX identifiers, token identifiers, state hints, and source URLs. It does not vendor Vercel implementation source, full documentation text, logos, or protected brand imagery.
