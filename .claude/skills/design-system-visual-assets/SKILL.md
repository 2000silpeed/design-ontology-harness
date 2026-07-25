---
name: design-system-visual-assets
description: Generate or source professional brand-aligned imagery for Codex implementations. Use when a screen, landing page, empty state, editorial hero, or product section needs raster imagery that matches the local design-system artifacts.
---

# Design System Visual Assets

Use this skill when the implementation would look more professional with generated or sourced raster imagery instead of flat placeholder blocks, generic gradients, emoji, or stock-like decoration.

For website, app, landing, product, editorial, portfolio, venue, sports, game, commerce, or content-led mockups, treat relevant visual assets as part of completeness. Image-free card walls, gradient media blocks, empty framed placeholders, and purely atmospheric panels should be replaced with concrete product/place/object/state/content imagery unless the user explicitly requests a text-only wireframe.

## Required Inputs

Read these files first when they exist:

- `agent-team/STYLE.md` or `agent-team/DESIGN.md`
- `agent-team/system_spec.md`
- `agent-team/token_schema.json`
- `agent-team/component_inventory.json`
- `agent-team/visual_reference_report.json`
- `agent-team/components/component_specs.md`

If `visual_reference_report.json` is missing, infer image direction from `system_spec.md`, brand keywords, anti-keywords, palette roles, typography mood, and product domain. State that the image direction is ungrounded by visual references.

## When To Generate Images

Generate imagery for:

- landing or editorial heroes that need a first-viewport visual signal
- product, venue, object, or media cards that benefit from real visual substance
- empty states, onboarding panels, or feature sections where illustration clarifies the product
- case-study or article covers where the system spec calls for editorial treatment
- comic, manga, webtoon, story, character, cover, and panel-preview slots where readers expect polished artwork
- sports, travel, food, real-estate, portfolio, game, commerce, and brand/product mockups where visual subject matter makes the screen feel complete

Do not generate imagery for:

- icons, logos, button glyphs, tabs, toggles, or status markers
- app icons, favicons, or app-shell brand marks; these are deterministic brand identity assets, not generated raster imagery
- components that should be built with CSS, SVG primitives, or an icon library
- comic covers, manga/webtoon panel previews, story scenes, editorial covers, or inspectable content media that would be reduced to rough inline SVG geometry
- dashboard/tool/data-product first viewports where users need tables, schedules, filters, live state, or provenance before decorative visuals
- copyrighted characters, real brands, real people, or identifiable private locations unless the user explicitly provided licensed source material
- purely atmospheric blurred backgrounds that do not reveal the product, state, place, or object

## Acquisition Order

1. Prefer Codex built-in `image_gen` when a brand-specific synthetic image is appropriate.
2. Use sourced visual fallback when `image_gen` is unavailable, fails, or the screen needs real-world photographic evidence more than generated imagery.
3. Use user-supplied licensed imagery when provided and relevant.
4. Use deterministic SVG identity assets for app icons, logos, flags, diagrams, and UI glyphs.
5. If no image path can meet the manifest and license contract, leave a prompt/candidate pack and report why imagery was not integrated; do not silently ship an image-free mockup.

Never switch to CLI, SDK runner, or OpenAI image API fallback unless the user explicitly asks for that different path.

## Medium Selection Contract

- Classify each visual slot as identity/icon, control glyph, diagram/data, factual real-world media, narrative/content media, or decorative support before authoring an asset.
- Narrative/content media such as comic covers, manga/webtoon panels, character/story scenes, editorial covers, portfolio artwork, and game scenes should use `image_gen`, user-supplied art, sourced licensed art, or an already approved high-fidelity asset.
- Deterministic SVG is the right tool for app icons, logos, flags, UI glyphs, charts, diagrams, maps, schematics, and semantic product illustrations where vector geometry is the real runtime representation.
- Do not substitute inline SVG because it is faster. A geometric or rough SVG in a cover/panel/story-media slot is a wrong-medium failure, not a valid style variant.
- If a narrative/content slot intentionally uses vector artwork, document why it is production-grade artwork rather than a placeholder and record the medium decision.

## Codex Imagegen Workflow

When Codex exposes the built-in `image_gen` tool through the installed imagegen skill:

When `agent-team/agent-team.json` exists and you are assigned `visual-asset-producer`, stop at the `accepted` state after manifest validation without `--require-integrated`. The UI Implementer owns runtime wiring, promotion to `integrated`, and the strict integrated-asset gate. In standalone use, one agent may complete both halves, but it must still preserve the state transition.

1. Use the built-in `image_gen` path. Do not invoke CLI mode, SDK runners, or OpenAI API fallback.
2. Generate 2-4 candidates for each major image slot with one built-in call per candidate or variant.
3. Base prompts on the artifact files, not on generic style words.
4. Include concrete subject matter, composition, camera/illustration treatment, palette constraints, density, material language, and anti-keywords.
5. Prefer usable aspect ratios:
   - hero: `16:9`, `3:2`, or wide responsive crop
   - card thumbnail: `4:3` or `1:1`
   - editorial cover: `4:5` or `3:4`
6. Copy accepted project-bound assets into the workspace before code references them. Preserve the exact `$CODEX_HOME/generated_images/<generation-run-id>/<candidate-id>.png` output path in the manifest, but never make runtime code depend on that agent-local path. Do not rename or invent the run or candidate identity.
7. Register the reviewed candidate as `accepted`; do not hand-edit it directly to `integrated`. When the harness CLI is available, run `design-ontology register-image-asset --project-dir . --asset-id <id> --source <png> --alt-text <text> --selection-reason <reason> --reviewed-criterion <criterion> --session-id <generation-run-id>` and repeat `--reviewed-criterion` for every prompt-packet review gate. The registry derives `generator`, `generation_run_id`, and `candidate_id` from the verified original path; arbitrary caller-authored values are not provenance.
8. Hand accepted assets to the UI Implementer. The implementer wires each workspace copy into its intended component, then runs `design-ontology promote-image-asset --project-dir . --asset-id <id>`.
9. The UI Implementer runs `design-ontology validate-image-assets --project-dir . --require-integrated`, followed by `design-ontology lint-implementation --target-repo .`. Do not report the image as integrated while either command fails.
10. Use schema `visual-asset-manifest/v2`. If the CLI is unavailable, preserve the same `planned → accepted → integrated` lifecycle and all metadata fields manually, then state that CLI verification is still pending.

Preferred manifest path:

- `public/generated/design-system/manifest.json`

Compatible manifest paths:

   - `public/generated/design-system/manifest.json`
   - `design-system/generated_visual_assets.json`

Required top-level manifest fields:

   - `schema_version`
   - `project`
   - `brand`
   - `generator`
   - `source_session`
   - `assets`

Required asset record fields:

   - `id`
   - `label`
   - `slot`
   - `status`
   - `asset_path`
   - `original_png_path`
   - `format`
   - `dimensions`
   - `size_kb`
   - `sha256`
   - `intended_for`
   - `alt_text`
   - `prompt_summary`
   - `generation_provenance_version`
   - `generator`
   - `generation_run_id`
   - `candidate_id`

For generated records, `generation_provenance_version`, `generator`, `generation_run_id`, and `candidate_id` may be null only while `status=planned`. An `accepted` or `integrated` record is fail-closed unless those values match the preserved Codex `image_gen` output path under `$CODEX_HOME/generated_images/`. Do not fabricate them from prompt text, a copied derivative, or a manually chosen session label.

If the built-in imagegen path is unavailable or fails, do not pretend an image was generated and do not call an API fallback. Move to the sourced visual fallback below, or create a ready-to-run prompt pack at `public/generated/design-system/imagegen-prompts.md` or the nearest existing docs/assets directory, then report that generation was skipped.

## Sourced Visual Fallback

Use this fallback for free/rights-clear visual search, not for another image generation provider.

Provider tiers:

- Free sourced providers: `Openverse`, `Wikimedia Commons`, `Unsplash`, `Pexels`
- Licensed providers: `Adobe Stock`, `Shutterstock`, `Getty Images`, `iStock`, `Envato Elements`, `Local licensed file`
- Reference-only providers: `Lazyweb`, `Mobbin`, `Dribbble`, `Behance`, `Awwwards`

Tier rules:

- Free sourced provider images can become runtime assets only when per-asset license metadata is recorded.
- Licensed provider images can become runtime assets only when user-supplied purchase/license proof, usage scope, and licensed-to metadata are recorded.
- Reference-only provider images are for morphology, density, hierarchy, and flow research only. Do not copy them into runtime assets.

Selection rules:

1. Search for 3-8 candidates that match the product domain, subject, crop, and visual role.
2. Reject any candidate without source URL, download URL, provider, author/creator, license label, and attribution requirement.
3. Reject paid-provider results unless the user supplied license proof or the asset is already licensed for this project.
4. Reject reference-only results as runtime assets; summarize their morphology only.
5. Reject results with unclear rights, recognizable private people, copyrighted characters, third-party logos, or brand endorsement risk unless the user supplied permission.
6. Copy the accepted asset into the workspace before implementation references it. Do not hotlink remote search/CDN URLs.
7. Record source metadata in `public/generated/design-system/manifest.json` with acquisition mode `sourced`.
8. Optionally keep reviewed-but-not-used candidates in `public/generated/design-system/sourced-visual-candidates.json`.

Sourced fallback policy:

- `license-verified sourced visual fallback`

Required sourced asset record fields:

   - `id`
   - `label`
   - `slot`
   - `status`
   - `acquisition_mode`
   - `asset_path`
   - `source_url`
   - `download_url`
   - `provider`
   - `author`
   - `license`
   - `attribution_required`
   - `sha256`
   - `intended_for`
   - `alt_text`
   - `selection_reason`

Sourced visual assets are still not valid replacements for icons, logos, app icons, favicons, button glyphs, status markers, or flags unless the exact asset license and identity use are explicitly approved.

## Prompt Recipe

Build prompts with this structure:

```text
Professional product image for [brand/product/screen], [specific subject], [composition], [visual material], [palette from token_schema], [density and surface cues from visual_reference_report], [lighting/camera or illustration treatment], no logos, no readable copyrighted UI, no stock-photo feel, no emoji, no generic gradient background.
```

For Korean-first products, include Hangul-safe composition constraints:

- leave quiet negative space where Korean headings may sit
- avoid dense texture behind text
- keep faces/objects away from likely text columns
- avoid tiny embedded text inside the generated image

## Integration Rules

- Add generated images through the framework's normal image component when one exists.
- Provide meaningful `alt` text for content images; use empty alt only for truly decorative images.
- Use CSS/object-fit and art direction so the important subject remains visible on mobile and desktop.
- Do not let images replace accessible text, data, controls, or navigation.
- Do not let images outrank the operational product surface in dashboards, tools, sports/data products, or community products.
- Keep palette and crop behavior aligned with tokens and responsive breakpoints.
- Keep generated and sourced assets in the same manifest, but distinguish them with `acquisition_mode`.
- For sourced assets, include visible or documented attribution whenever `attribution_required` is true.
- Every integrated raster image needs a manifest record before runtime code references it.
- `accepted` means the candidate passed every packet review criterion; `integrated` means application code references the verified workspace copy. Never skip this state transition.
- Generated `accepted` and `integrated` records must use the current manifest and generation-provenance versions. A legacy manifest, arbitrary generator label, or run/candidate value that does not match `original_png_path` is blocking.
- Treat DS087, DS088, and DS089 from `lint-implementation` as blocking: they indicate an invalid manifest, missing/unregistered file, unsafe hotlink/agent-local path, or missing runtime alt text.
- Define stable aspect ratios, object-fit/object-position, and mobile crop behavior so imagery does not obscure Korean text or controls.
- Verify desktop and mobile screenshots after integration; check that images render, crop cleanly, and do not obscure text.

## Output Expectations

- List generated and/or sourced assets and their intended slots.
- Mention the Codex `image_gen` prompt basis or the sourced visual query/provider basis.
- Mention any manual review needed for licensing, attribution, realism, or content fit.
