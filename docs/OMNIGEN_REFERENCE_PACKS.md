# Omnigen Reference Packs

Omnigen vault images are useful as local visual evidence, but they should not be
bundled into the public harness or plugin distribution. Treat them as an
optional reference pack: users can connect their own vault, or install a
separate image corpus if they want a richer starting point.

## Distribution Rule

- Keep `design-ontology-harness` light: code, schemas, docs, presets, and
  metadata only.
- Do not commit full-size Omnigen images into this repo.
- Use `build/visuals/omnigen-selected/` for local symlinks or copies. Project
  `build/` directories are ignored by git.
- The generated selection manifest is metadata and can be inspected, regenerated,
  or attached to internal workflows.
- Selected Omnigen images are `reference-analysis-only`; they are not
  redistributable product assets.

## Select References From A Local Vault

```bash
uv run design-ontology select-omnigen-references \
  --project-dir projects/my-app \
  --query "analytics dashboard crm settings" \
  --category app-design \
  --category web-design \
  --count 12 \
  --sync-sources
```

The command writes:

- `projects/my-app/build/visuals/omnigen_reference_selection.json`
- `projects/my-app/build/visuals/omnigen-selected/*` symlinks by default
- updated `projects/my-app/brand_profile.json` when `--sync-sources` is passed

Then run:

```bash
uv run design-ontology analyze-visuals --project-dir projects/my-app
uv run design-ontology run-project --project-dir projects/my-app
```

## Link Modes

```bash
# Default: local symlinks, lightest for development
--link-mode symlink

# Copy selected files into build/ for an isolated local experiment
--link-mode copy

# Do not create project-local files; point visual_reference directly at vault paths
--link-mode absolute
```

Prefer `symlink` for normal local work. Use `copy` only for a temporary local
experiment where the selected set needs to survive vault changes. Avoid committing
copied image files.

## Query Strategy

Use project-shaped words, not style-only words:

- Good: `analytics dashboard crm contacts settings table`
- Good: `mobile banking wallet cards onboarding`
- Good: `commerce product grid checkout cart detail`
- Less useful: `beautiful minimal modern clean`

If `--query` is omitted, the CLI builds one from `brand_profile.json` fields such
as `product_summary`, `brand_keywords`, `visual_keywords`, and
`product_primitives`.

## Why This Shape

The harness already treats visual references as advisory evidence. Omnigen fits
that model well: it can influence density, panel proportions, surface language,
layout rhythm, and component morphology. It should not decide the final palette,
typography scale, IA, copy, or product content.
