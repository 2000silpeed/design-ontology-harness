# FairCite Harness Console

This folder is a self-contained harness project built on top of `design-ontology-harness`.

## Files

- `brand_profile.json`: your system identity and product context
- `spec.md`: FairCite dual-mode service screen and governance requirements
- `seeds/seed_urls.txt`: curated reference entry points
- `project_manifest.json`: project metadata
- `agent_brief.md`: instructions for human or agent collaborators
- `build/`: generated harness outputs from `run-project`
- `design-system/`: installed design system artifacts from the generated preset
- `index.html`, `styles.css`, `app.js`: implementation consuming `design-system/tokens.css`
- `assets/evidence-workspace-hero.png`: generated commercial product visual used in the hero
- `assets/faircite-mark.png`: project-local raster brand mark used for favicon and app shell

## Commercial Redesign Notes

- The first viewport is now a commercial SaaS-style product entry with a generated evidence-review workspace visual.
- The product demo remains directly on the page: mode switching, diagnosis, sanction anatomy, pattern catalog, paired case, and evidence map are still reachable from the header.
- The primary demo scenario is the Hyundai Heavy Industries technical-materials case, with chunk citation and source labels visible in the evidence review surface.
- Raster-only implementation guardrail is respected: the visible app icon and favicon use project-local PNG assets.

## Harness Flow Used

```bash
uv run design-ontology run-project --project-dir projects/faircite-harness-console
uv run design-ontology build-preset \
  --project projects/faircite-harness-console \
  --preset-id monitoring-ops--bold-confident \
  --owner codex \
  --tier P3 \
  --color-modes light \
  --default-color-mode light
uv run design-ontology install-preset \
  --preset-id monitoring-ops--bold-confident \
  --target-repo projects/faircite-harness-console \
  --adapter raw-css-variables \
  --color-mode light \
  --locale ko \
  --force
```

## Preview

```bash
cd projects/faircite-harness-console
python3 -m http.server 4173 --bind 127.0.0.1
```

Open `http://127.0.0.1:4173/`.

## Verification

```bash
uv run design-ontology lint-implementation --target-repo projects/faircite-harness-console
```

Current result: `Implementation lint: OK (3 files checked, 0 issues)`.
