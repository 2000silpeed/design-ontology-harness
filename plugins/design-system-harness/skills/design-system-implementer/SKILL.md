---
name: design-system-implementer
description: Implement UI changes that must follow the repository's design-system artifacts. Use when editing tokens, components, styles, or screens so implementation stays aligned with the generated system.
---

# Design System Implementer

Use this skill when making code changes in the implementation repository.

## Required Inputs

Read these files first when they exist:

- `agent-team/IMPLEMENTATION_CONTRACT.md`
- `agent-team/STYLE.md` or `agent-team/DESIGN.md`
- `agent-team/system_spec.md`
- `agent-team/token_schema.json`
- `agent-team/component_inventory.json`

## Implementation Rules

1. Treat the design-system artifacts as the source of truth.
2. Keep implementation aligned with brand keywords and anti-keywords.
3. Implement high-priority families before medium-priority families.
4. Reuse or extend primitives before adding net-new components.
5. Preserve existing features, entry points, and task flows unless removal is explicitly requested.
6. Keep supported themes and responsive layouts working during refactors.
7. Use semantic tokens only; keep raw surface or text color values in design-system artifacts.
8. Update nearby documentation or tests when behavior or structure changes.
9. Respect curated palette roles and reference colors recorded in the token schema when choosing UI colors.
10. Visual references are morphology inputs only; do not absorb reference palettes, type scales, navigation labels, domain IA, or product copy.
11. Token binding is necessary but not sufficient: never recombine `--ds-*` roles into a new reference-like palette.
12. Promote repeatable user/reviewer feedback into governance docs or lint rules before calling a screen complete.
13. **ALWAYS ship normal light mode and dark mode together** unless the user explicitly asks for one mode only. Light mode is the default token set; dark mode is an override.
14. **NEVER use emojis as UI icons, state indicators, or button decorations** (no 🎨 ✅ 🔥 ⚡ 🚀 ❌ ⭐ 📊). Always implement SVG icon components or import from Lucide / Heroicons / Phosphor / Tabler. Emojis only belong in user-generated content, never in system UI.
15. **NEVER leave half-finished components** ("TODO", "placeholder", "temp"). Read `agent-team/components/component_specs.md` and implement the full anatomy, states, and token bindings.
16. **NEVER use bare library components without token binding.** If you import from a UI library, wrap it and override colors, spacing, radius, and typography using tokens from the schema.
17. **NEVER ship generic initials tiles as final app icons.** Favicon, app-shell marks, and web manifests need brand-specific SVG identity assets.
18. **NEVER let dashboard/tool/data/community products open like pitch decks** unless the user explicitly asks for a landing page. Lead with operational state, filters, tables/lists, and source/update context.
19. **NEVER treat image-free commercial mockups as complete** when the product, place, object, article, game, venue, or content model naturally needs visual assets. Use generated, sourced, user-provided, or deterministic identity imagery with manifest records.
20. **NEVER implement an authored component marked `needs-authoring`.** Run `design-ontology validate-component-contracts --project-dir <project>` before implementation and preserve every domain state, prop/data field, interaction, accessibility rule, responsive mode, and `--ds-*` token binding.
21. **Do not claim production readiness from one lint or one screenshot.** Record matching light/dark mobile/desktop evidence for the same route, state, and implementation SHA; add human or multimodal-review evidence for semantic industry-fit metrics; then run `design-ontology verify-production-ui --project-dir <project> --target-repo .`.


## Script-aware typography

If `system_spec.md` or `token_schema.json` contains typography `script_guardrails`, treat that as the default-safe implementation baseline, not optional polish.

- For Korean-first UI or marketing copy, default to `word-break: keep-all` plus `overflow-wrap: normal`.
- Use `text-wrap: balance` on major headings when browser support allows it.
- Avoid forced `<br/>` in Korean headlines until desktop/mobile wrapping is verified with real copy.
- For wide or serif Hangul display fonts, start one type step smaller than English-first hero comps and only scale up after wrap review.
- Respect font-specific line-height and letter-spacing guidance from the artifacts instead of reusing English defaults.
- Never set Hangul display line-height below the artifact safety minimum, and never tighten tracking past the allowed min/max range.



## UI base rules

These are the readability floors `lint-implementation` enforces as `DS100`-`DS107`. Token binding proves where a value came from; these rules decide whether the bound value is readable. Treat every one as blocking, not as polish.

- Running text keeps `line-height: var(--ds-leading-body)`. The floor is 1.5 for Latin copy and 1.6 for Korean, because Hangul carries 받침 below the baseline. Tight leading belongs to display type only. (`DS100`)
- Text needs 4.5:1 contrast against its own background, or 3:1 above 24px regular / 18px bold. Check the resolved token values in both light and dark mode, not just the light default. (`DS101`)
- Form fields, buttons, and other control boundaries need 3:1 against their own fill. A 1.4:1 hairline border is decoration, not an affordance. A filled control whose border token equals its background is fine — its fill is the identifier. (`DS102`)
- Never let color be the only difference between states. A status dot needs a shape, glyph, or adjacent label so the state survives color blindness and grayscale. (`DS103`)
- Use at most two text typefaces. Hierarchy comes from size and weight. The Korean/Latin locale pairing does not count as a third family. (`DS104`)
- Korean reading text keeps tracking between -0.02em and 0 via `var(--ds-tracking-body)`. Positive letter-spacing dissolves 어절 grouping, which is the Hangul equivalent of the Latin all-caps failure. Wide tracking stays with Latin-only uppercase labels, wordmarks, dates, and numerals. (`DS105`)
- Korean surfaces need a wrap contract: `word-break: var(--ds-wrap-word-break)` plus `overflow-wrap: var(--ds-wrap-overflow)`. Without keep-all, Hangul breaks mid-어절. (`DS106`)
- Keep running text left aligned. Justified text opens word rivers and is worse in Korean, where 어절 gaps stretch. (`DS107`)

Two Latin conventions do not transfer to Hangul and must not be copied from English comps: x-height selection has no Hangul counterpart, so judge Korean body faces by 자소 balance and small-size legibility from the artifacts instead; and letter case does not exist, so `text-transform: uppercase` on Korean copy is a no-op that signals an English-first spec.



## Color mode parity

Normal light mode and dark mode travel together unless the user explicitly asks for a single-mode artifact.

- Use light mode as the default `:root` or app-default token set.
- Add dark mode as an override such as `[data-theme="dark"]`, a theme provider, or equivalent framework mode.
- Components consume the same semantic variables in both modes; only token values change.
- Do not ship dark-only dashboards, tools, landing pages, or prototypes.
- Verify both modes with screenshots or DOM checks when the implementation has a visible UI shell.



## Commercial product realism

For dashboards, tools, sports/data products, and community products, the first viewport should feel like an operated product, not a pitch deck.

- Lead with the active task surface: status strip, filters/date rail, table/list rows, next item, source/update label, or primary workflow.
- Do not open product UIs with an oversized marketing hero, generic slogan, and equally weighted feature cards unless the user explicitly asks for a landing page.
- Avoid homogeneous card walls. Promote one primary workflow module, compress secondary information into rows/tables/rails, and vary density only when the information architecture justifies it.
- Exact numbers, predictions, rankings, poll counts, odds, or operational claims need source/update context or a visible sample/demo label.
- Generated or decorative imagery must support the domain object, venue, person, product, or state; it must not outrank data, navigation, controls, or the first operational surface.
- Include realistic state texture: live/final/upcoming/delayed/empty/error/source-updated as appropriate for the domain.



## Responsive resilience

Treat mobile fit as a contract, not a final polish pass.

- Verify changed screens at 320, 360, 390, 430, 768, and desktop widths.
- A screen is not complete if `document.documentElement.scrollWidth > window.innerWidth`.
- Buttons, CTAs, tabs, chips, and toolbar actions must keep `max-inline-size: 100%`; controls inside flex/grid parents need `min-inline-size: 0`.
- Avoid fixed `width` / `min-width` px values on button-like controls. If a large CTA width is intentional, add a <=480px wrap or stack fallback.
- Action rows must use `flex-wrap: wrap` or switch to a vertical stack on narrow viewports.
- Do not use `width: 100vw` inside padded containers, and do not hide `overflow-x` on `body` as the fix for an overflowing control.
- Test Korean CTA labels with realistic copy; prefer wrapping or stacking over clipping and `white-space: nowrap`.



## Emoji-to-SVG refactor

When refactoring existing UI, do not merely report emoji UI affordances. Replace them.

- Scan buttons, cards, badges, tabs, nav items, status indicators, empty states, toasts, and banners for emoji-looking icons or visual markers.
- Prefer the project's existing icon library when it is already installed and visually compatible.
- Prefer approved icon systems such as Lucide, Heroicons, Phosphor, Tabler, Material Symbols, or the existing project icon library over handmade path sprites.
- Reuse existing local SVG/icon components when available.
- If no suitable icon exists, create a local SVG file or SVG component in the nearest existing icons/assets directory and document its icon grammar.
- A custom icon sprite must declare its source or approved grammar, such as `data-icon-set="lucide"` or `data-icon-set="approved-custom"`.
- Keep one icon grammar across the UI: consistent grid, stroke weight, caps, joins, optical size, and active/inactive treatment.
- Bind SVG stroke/fill to `currentColor` or design tokens, not hard-coded colors.
- Decorative icons use `aria-hidden="true"`; semantic icons need an accessible label or adjacent visible text.
- Do not replace user-generated emoji content, chat text, blog body, or emoji-picker data.


## Output Expectations

- State which artifact files informed the implementation.
- Mention any gap between the requested UI and the current system artifacts.
- Call out any remaining feature-regression or theme-regression risk.
- Report `verify-production-ui` as the final release gate and list any failed evidence category.
