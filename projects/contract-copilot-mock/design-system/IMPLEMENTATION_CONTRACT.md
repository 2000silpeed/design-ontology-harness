# Implementation Contract

Preset: `conversation-copilot--corporate-trust`
System: Mercer System

## Authority Order

1. Existing product task flow and information architecture
2. `design-system/token_schema.json`
3. `design-system/tokens.css` or host adapter token variables
4. `design-system/components/component_specs.*`
5. `design-system/system_spec.md`
6. `design-system/STYLE.md` or `design-system/DESIGN.md` as a derived quick brief
7. External visual references

The style capsule is a derived summary and never overrides the source artifacts.
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
- palette composition or derived secondary palettes
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
- Token binding is necessary but not sufficient: do not recombine `--ds-*` color roles into a new reference-like palette.
- Derived colors may alias one semantic token or mix one semantic role with a neutral surface/transparent value; do not mix multiple chromatic roles for local palette variables.

## Feedback Promotion Rule

If implementation review or user feedback exposes a repeatable design-system failure,
promote it into ontology governance, this contract, and `lint-implementation` before
calling the current screen complete. Current-screen fixes alone are not enough.

## Preflight

Run this before considering an implementation aligned:

```bash
uv run design-ontology lint-implementation --target-repo .
```
