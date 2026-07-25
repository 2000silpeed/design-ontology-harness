# Packaged Resources

This directory contains data files that must travel with the
`design_ontology_harness` Python package.

## `semantic_color_ontology.json`

Compatibility snapshot imported from the local `semantic-os` color domain.

- Source snapshot: `semantic-os/domains/color/ontology/build/graph.json`
- Imported as abstracted ontology data, not as raw OCR or page images.
- Contains color keyword metadata, semantic spectrum/family/tone axes, color
  guidelines, heuristics, metrics, and palette-abstraction patterns.
- Does not contain absolute local filesystem paths.
- Does not contain reconstructable paid-source palette table structure.

This JSON is retained as a deprecated transport and compatibility artifact. It
is not the runtime source of truth and is not used as a fallback.

The sole runtime color authority is `docs/color-reference.md`, which is
force-included in the wheel. The document keeps its 87 visible color cards
byte-for-byte and appends the sanitized full graph in a
`semantic-color-ontology+json` fenced block. Runtime parsing verifies the
embedded checksum, then merges the visible cards—including explicitly marked
Markdown-only local colors—with the embedded graph in memory.

Update both artifacts from the same source snapshot with:

```bash
uv run design-ontology sync-semantic-colors \
  --source ../semantic-os/domains/color/ontology/build/graph.json \
  --color-reference-output docs/color-reference.md \
  --ontology-output design_ontology_harness/resources/semantic_color_ontology.json
```

Use the same command with `--check --json` in CI. Do not hand-edit the embedded
graph block. Shared colors belong upstream in Semantic OS; project-only colors
must remain clearly sourced Markdown-only extensions.
