# Adapter base (plugin-distributed)

The canonical adapter contract (`StackAdapter`, `FileOp`, `PresetBundle`,
tokens → CSS vars helpers) lives in the harness repo under
`design_ontology_harness/adapters/base.py`.

This directory is a plugin-side stub that currently ships only metadata. When
the plugin runtime is implemented (Phase 11+) it will either:

1. Re-implement the contract in TypeScript for edge runtimes, or
2. Invoke the harness Python CLI (`uv run design-ontology …`) under the hood.

Until then this README is the only artifact synced to the plugin repo.
