# Adapter base (plugin-distributed)

The canonical adapter contract (`StackAdapter`, `FileOp`, `PresetBundle`,
tokens → CSS vars helpers) lives in the harness repo under
`design_ontology_harness/adapters/base.py`.

Shared adapter behavior now includes `design_system_mirror_ops`, which copies
the preset's raw artifacts into the target repo's `design-system/` directory.
The mirror includes `STYLE.md` and `DESIGN.md` when present, plus a generated
`IMPLEMENTATION_CONTRACT.md` that fixes the authority order and reference
absorption rules for coding agents.

This directory is a plugin-side stub that currently ships only metadata. When
the plugin runtime is implemented (Phase 11+) it will either:

1. Re-implement the contract in TypeScript for edge runtimes, or
2. Invoke the harness Python CLI (`uv run design-ontology …`) under the hood.

Until then this README is the only artifact synced to the plugin repo.
