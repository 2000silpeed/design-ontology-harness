# Sprout Community Visual Ontology

This folder promotes the generated raster images in `projects/sprout-community-mock/assets/` into a small project-local ontology.

## Files

- `generated_visual_assets.json`: image asset manifest with paths, original Codex outputs, dimensions, hashes, alt text, and slot intent.
- `system_ontology.json`: graph representation using `GeneratedVisualAsset`, `ImageGenerationModel`, `SourceReference`, `Brand`, `Principle`, and `Component` nodes.

## Policy

- Generator: Codex built-in `image_gen` skill.
- API fallback: disabled.
- Original generated PNGs are preserved under `$CODEX_HOME/generated_images/019e1507-34d5-7792-a649-fce2980656b8`.
- Project-facing assets are optimized WebP files under `assets/`.
