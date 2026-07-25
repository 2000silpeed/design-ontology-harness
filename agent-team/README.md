# Design System Artifacts

Place generated artifacts from `design-ontology-harness` in this directory.

Expected files:

- `system_spec.md`
- `STYLE.md` / `DESIGN.md`
- `token_schema.json`
- `component_inventory.json`
- `system_ontology.json`
- `components/component_specs.json` (optional, from build-components)
- `components/component_specs.md` (optional, human-readable version)

Important usage rule:

- treat these artifacts as alignment inputs, not a license for a full-shell rewrite
- preserve existing product features and entry points unless an explicit migration is requested
- validate supported themes and responsive states when applying visual refactors

Recommended sync source:

- a harness project output such as `build/system/blueprint/*`

Recommended mapping:

- `build/system/blueprint/system_spec.md` -> `agent-team/system_spec.md`
- `presets/<id>/STYLE.md` -> `agent-team/STYLE.md`
- `presets/<id>/DESIGN.md` -> `agent-team/DESIGN.md`
- `build/system/blueprint/token_schema.json` -> `agent-team/token_schema.json`
- `build/system/blueprint/component_inventory.json` -> `agent-team/component_inventory.json`
- `build/system/blueprint/system_ontology.json` -> `agent-team/system_ontology.json`
- `build/system/components/` -> `agent-team/components/`
