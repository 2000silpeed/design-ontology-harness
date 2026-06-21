# Mode Signal Fashion Pipeline Test

This project is a lightweight end-to-end test for the public-web Visual Reference Pack workflow.

It does not commit downloaded third-party fashion images. The mockup uses remote reference URLs, and the pack can be rebuilt locally when visual analysis needs local files.

## Flow

```bash
uv run design-ontology build-reference-pack \
  --pack-id fashion-magazine-public-web \
  --output-dir projects/fashion-magazine-pipeline-test/packs/fashion-magazine-public-web \
  --source-url https://www.vogue.com/fashion \
  --source-url https://www.vogue.com/fashion-shows \
  --source-url https://runwaymagazines.com/ \
  --source-url https://www.elle.com/fashion/ \
  --provider-id public-fashion-web \
  --category fashion-editorial \
  --tags public-web,reference-only \
  --materialize download \
  --max-assets 60
```

```bash
uv run design-ontology select-visual-references \
  --project-dir projects/fashion-magazine-pipeline-test \
  --pack projects/fashion-magazine-pipeline-test/packs/fashion-magazine-public-web \
  --query "fashion magazine editorial runway street style trend hero story serif gallery vogue elle" \
  --count 18 \
  --local-only \
  --sync-sources
```

```bash
uv run design-ontology analyze-visuals \
  --project-dir projects/fashion-magazine-pipeline-test

uv run design-ontology build-kb \
  --kb-dir projects/fashion-magazine-pipeline-test/build/kb \
  --seeds-file projects/fashion-magazine-pipeline-test/seeds/seed_urls.txt \
  --max-sources 4 \
  --max-pages-per-source 2 \
  --max-depth 0

uv run design-ontology run-project \
  --project-dir projects/fashion-magazine-pipeline-test \
  --kb-dir projects/fashion-magazine-pipeline-test/build/kb
```

## Outputs

- `mockup/index.html`: fashion magazine UI mockup using reference-only remote images.
- `brand_profile.json`: Mode Signal editorial brand profile.
- `spec.md`: product and interaction requirements.
- `build/`: local generated output, not required in source control.
- `packs/`: local generated reference pack, not required in source control.

## Local Check

The verified local run produced:

- 58 public-web reference candidates
- 18 selected fashion references
- visual analysis: `density airy`, `surface tinted`, `layout editorial-feed`
- mockup browser check: 15/15 images loaded, no desktop/mobile horizontal overflow
