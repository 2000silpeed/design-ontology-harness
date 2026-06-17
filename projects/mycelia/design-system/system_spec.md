# Mycelia Design System — Spec

> **Image-first.** This system was derived from three GPT Image 2 screens
> (`identify`, `field-map`, `logbook`), not synthesized from a KB and not copied
> from any preset/project/fixture. The ontology is used only to validate vocabulary
> and relationships (step 6).

## 1. Concept

**Field Guide Naturalism** — a vintage letterpress mycology field guide reinterpreted
as a calm, precise modern web interface. Adjectives: earthy, archival, precise,
tactile, calm. Anti-patterns: neon, glassmorphism, default Tailwind blue, emoji icons,
dark techy dashboard, heavy gradients.

## 2. Feature surfaces

| Surface | Purpose | Source screen |
|---|---|---|
| identify | photo → ranked species candidates + edibility safety | `ec548881…` |
| field-map | sighting map + filters + sighting detail | `ce923932…` |
| logbook | personal find timeline + species encyclopedia detail | `63e4f0e8…` |

## 3. Color

See `token_schema.json`. Base: ink `#2A2622`, paper `#F4EEE2`, paper-raised `#FBF7EE`,
bark `#8C6A4A`. Brand: forest `#2F4733` (action/data), spore `#C8742B` (single accent).
Semantic states: success `#3F7A4E`, warning `#B8832A`, danger `#A6402F`.

**Ontology grounding:** mood tags 자연/신뢰/전문성/안정; warm-earth + deep-green spectrum,
low-to-mid chroma. Edibility is encoded as a meaningful color relationship
(verified→success, unverified→warning, poisonous→danger).

### Contrast audit
- ink on paper ≈ 12.4:1 (AAA)
- paper-raised on forest ≈ 9.6:1 (AAA, primary button)
- danger on paper-raised ≈ 5.2:1 (AA, toxic warnings)

## 4. Typography

Spectral (humanist serif) — wordmark, species Latin names, titles. Source Sans 3 —
UI/body/tables. Mono — coordinates, dates, confidence %. The serif/sans pairing is an
archival field-guide voice, deliberately not a tech-sans voice.

## 5. Components

See `component_inventory.json`. Families: app-shell (AppHeader, PrimaryButton),
data-display (SpeciesCard, ConfidenceBar, EdibilityChip, SpeciesDetailPanel,
TaxonomyTable, SeasonalBarChart, FindTimelineRow), map (FieldMap, MushroomPin,
SightingCard), controls (FilterCheckbox, SegmentedChips, PhotoUploadPanel, Tabs).

Interactive components carry `requires` edges to accessibility rules
(keyboard-nav, label-association, contrast-aa) per the ontology graph.

## 6. Form language

- **Surface:** flat warm paper; cards are paper-raised with a 1px bark hairline.
- **Edge:** gently rounded (card radius 10px) — not sharp, not pill.
- **Elevation:** flat by default; only the floating map sighting card lifts.
- **Density:** balanced; field-guide breathing room, dense only in the taxonomy table.
- **Accent discipline:** spore amber appears once per screen (active nav/tab, selected pin).

## 7. Provenance & rules

- `derived_from: generated-screens`; every token names its source screen.
- Do **not** copy tokens/colors/fonts from `presets/*`, other `projects/*`, or
  `tests/fixtures/*`. Validated by `check-site-design`.
- Re-running the workflow for a different product must produce a different system —
  the ontology supplies *valid relationships*, not *the answer*.
