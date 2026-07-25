---
name: design-system-implement
description: Implement or refactor UI code to match the project's design-system artifacts. Use when building tokens, components, styles, or screens based on the generated design-system outputs.
allowed-tools: Read Glob Grep Bash Edit Write
paths:
  - "agent-team/**"
  - "src/**"
  - "app/**"
  - "components/**"
  - "styles/**"
---

Before making changes:

1. Read `agent-team/IMPLEMENTATION_CONTRACT.md` when present.
2. Read `agent-team/STYLE.md` or `agent-team/DESIGN.md` when present.
3. Read `agent-team/system_spec.md`.
4. Read `agent-team/token_schema.json`.
5. Read `agent-team/component_inventory.json`.

Implementation rules:

- Treat the design-system artifacts as the source of truth.
- Keep implementation aligned with the product's brand keywords and anti-keywords.
- Implement high-priority component families before medium-priority families.
- Reuse or extend primitives before adding net-new components.
- Preserve existing features, navigation entry points, and data flows unless removal is explicitly requested.
- Keep supported themes, breakpoints, and critical interaction states working while refactoring.
- Use semantic tokens only; raw color values belong in `agent-team` token artifacts, not implementation files.
- Always include both normal light mode and dark mode unless the task explicitly asks for one mode only.
- Default to the smallest viable surface refactor; do not rewrite the whole shell unless the task explicitly calls for it.
- If `token_schema.json` includes a curated color reference or palette roles, align color decisions to that input before inventing a new palette.
- Visual references are morphology inputs only. Do not absorb reference palettes, type scales, navigation labels, domain IA, or product copy.
- Token binding is necessary but not sufficient: never recombine `--ds-*` roles into a new reference-like palette.
- If user/reviewer feedback exposes a repeatable failure pattern, promote it into governance docs or lint rules before calling the screen complete.
- For dashboards, tools, sports/data products, and community products, lead with operational substance instead of pitch-deck hero composition.
- Update nearby documentation or tests when implementation meaningfully changes.
- NEVER change layout properties (display, flex-direction, grid-template, position, width, height).
- NEVER change font-size or line-height to "fit the token scale." Existing sizes are tuned to the layout. Only replace when the token resolves to the exact same px. If no match, keep original + TODO.
- NEVER round spacing values to the nearest token — if no exact match, leave as-is with a TODO.
- **NEVER use emojis as UI icons, state indicators, button decorations, or navigation markers** (no 🎨 ✅ 🔥 ⚡ 🚀 ❌ ⭐ 📊 etc.). Always implement proper SVG icon components or import from Lucide / Heroicons / Phosphor / Tabler. Emojis are only allowed inside user-generated content (blog text, user input) — never as part of the design system itself.
- **NEVER leave half-finished components** like "TODO component", "placeholder card", "temp button". Read `agent-team/components/component_specs.md` and implement the full anatomy, states, and token bindings defined there.
- **NEVER use bare library components (e.g., default `<Button>` from a UI lib) without binding design tokens.** Every component must have its colors, spacing, radius, and typography wired to the token system. If you import from a library, wrap it and override styles with CSS variables from the token schema.


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


When finishing:

- State which artifact files guided the implementation.
- Mention any gaps between the requested UI and the current system artifacts.
- Mention any feature, theme, or layout risks that still need manual verification.
