# Packaged Resources

This directory contains data files that must travel with the
`design_ontology_harness` Python package.

## `semantic_color_ontology.json`

Compact color ontology imported from the local `semantic-os` color domain.

- Source snapshot: `semantic-os/domains/color/ontology/build/graph.json`
- Imported as abstracted ontology data, not as raw OCR or page images.
- Contains color keyword metadata, semantic spectrum/family/tone axes, color
  guidelines, heuristics, metrics, and palette-abstraction patterns.
- Does not contain absolute local filesystem paths.
- Does not contain reconstructable paid-source palette table structure.

The runtime loader in `design_ontology_harness.semantic_color_ontology` reads this
file from package resources, so GitHub users do not need a sibling
`semantic-os` checkout.
