# Implementation Contract

Preset: `conversation-copilot--corporate-trust`
System: Mercer System

## Authority Order

1. Existing product task flow and information architecture
2. `design-system/token_schema.json`
3. `design-system/tokens.css` or host adapter token variables
4. `design-system/components/component_specs.*`
5. `design-system/system_spec.md`
6. External visual references

External references never outrank product IA, tokens, component specs, or semantic
state rules.

## Reference Absorption Scope

Allowed from visual references:

- component morphology
- layout density
- panel/card proportions
- hierarchy rhythm
- interaction affordance patterns

Denied from visual references:

- color palette
- typography family or scale
- semantic status colors
- product copy
- product data model
- navigation labels
- domain information architecture
- redistributable imagery unless explicitly licensed

## Token Binding Rules

- Use `var(--ds-color-*)` for color, surface, border, and feedback states.
- Use `var(--ds-font-*)` for explicit font-family declarations.
- Use `var(--ds-radius-*)` for component radii; only fully circular affordances may use `999px`.
- Do not hard-code hex/rgb/hsl colors in implementation files outside generated managed blocks.
- Do not add reference-derived local palette variables such as teal/gold/slate unless they alias `--ds-*` tokens.

## Preflight

Run this before considering an implementation aligned:

```bash
uv run design-ontology lint-implementation --target-repo .
```
