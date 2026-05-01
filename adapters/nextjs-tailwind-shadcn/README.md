# nextjs-tailwind-shadcn adapter — v0.1.0

Design-ontology MVP adapter (Phase 10A). Targets Next.js 14+ App Router + Tailwind
CSS + shadcn/ui.

Python implementation: `design_ontology_harness/adapters/nextjs_tailwind_shadcn.py`.
Plugin repo currently ships only `adapter.json` + this README. When the plugin
runtime is built out (Phase 11+) it will call back into the harness CLI.

## Outputs

- `tailwind.config.ts` — `theme.extend` with color tokens routed through CSS
  variables, radius/spacing/type scales derived from `token_schema.json`, and
  `darkMode: ["class", "[data-theme='dark']"]` when the preset declares a
  dark mode.
- `app/globals.css` — `:root` tokens + `[data-theme='dark']` block + a
  `prefers-color-scheme: dark` fallback. Wrapped in a
  `/* design-ontology:START … END */` managed block so re-runs are idempotent.
- `components.json` — shadcn config with `cssVariables: true` and aliases
  suitable for the App Router default layout.
- `design-system/` — full copy of the preset artifacts (manifest, blueprint,
  token_schema, component_inventory, system_spec, component_specs, STYLE.md,
  DESIGN.md) plus generated `IMPLEMENTATION_CONTRACT.md`.
- **locale=ko**: `public/fonts/PretendardVariable.placeholder` + `LICENSE-FONTS`
  (SIL OFL 1.1) + `scripts/fetch-pretendard.mjs` (install-time fetch).

## Merge policy

- Managed-block files (tailwind / globals.css) are idempotently replaced in
  place when the markers are present. If markers are missing on an existing
  file, the new content is written to `<path>.ds-proposed` with a warning.
- `components.json` is deep-merged. Scalar conflicts fall back to
  `.ds-proposed`.
- `design-system/` and font assets are generator-owned and are overwritten.
- All other path collisions default to `.ds-proposed` — the adapter never
  silently overwrites user code.

## Agent usage

After install, agents should read files in this order:

1. `design-system/IMPLEMENTATION_CONTRACT.md`
2. `design-system/STYLE.md` or `design-system/DESIGN.md`
3. `design-system/token_schema.json`
4. `design-system/components/component_specs.md`

External visual references may inform morphology, density, proportions, and
hierarchy rhythm only. Color palettes, type scale, product copy, navigation
labels, and domain IA remain ontology/token-led.

## Detect

`detect(target_repo)` returns a `[0, 1]` score based on `package.json`,
`tailwind.config.*`, and `components.json`. Used by `/design-start` to pick the
highest-scoring adapter in the user's target repo.
