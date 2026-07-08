# Foldline Design System

## 1. Brand Concept

Foldline is a Korean-first mobile fashion curation app. It turns a daily style brief and closet memory into one outfit decision before shopping.

The product should feel quiet, tactile, and decisive. It should not feel like a marketplace grid, a magazine landing page, or a dashboard. The first screen is a wardrobe work surface: brief, signal spine, look board, rationale, and contextual shop sheet.

## 2. Skeleton UI

The first screen keeps this order:

1. Compact topbar with brand, date, and profile entry.
2. Daily brief row for occasion, weather, comfort, and avoid condition.
3. Signal spine beside the look board.
4. Look board with one assembled outfit decision.
5. Why-it-works strip with material, silhouette, and closet fit.
6. Garment stack with owned and candidate items.
7. Contextual shop sheet attached to the selected garment.
8. Bottom tab bar.

The first screen must not include a marketing hero, product grid, dashboard card set, generic command palette, or generic data table.

## 3. Visual Tokens

Color roles:

- Canvas: `#f7efe7`
- Paper: `#fffaf4`
- Surface muted: `#ebe0d5`
- Ink: `#24191d`
- Muted ink: `#6a5d61`
- Primary claret: `#7f1734`
- Prussian blue: `#003153`
- Sage support: `#879c7d`
- Fold accent: `#dccb9a`

Typography:

- Display: `Noto Serif KR`
- Body/UI: `Pretendard`
- Letter spacing: `0`
- Korean wrapping: `word-break: keep-all`

Shape and spacing:

- Repeated framed items use `8px` radius or less.
- Control chips may use pill radius because they are controls.
- Primary mobile actions use at least `44px` height.
- No section-level nested cards.

## 4. Component Set

Core implementation components:

- app shell
- topbar
- tab bar
- taste signal rail
- taste signal chip
- outfit edit canvas
- edit confidence badge
- garment stack
- garment row
- fabric swatch
- why-this-works note
- reason note
- fit note
- size chip group
- save edit button
- saved state toast
- shop drawer
- price size summary
- alternative item rail
- alternative item tile
- closet compatibility badge

Astryx and Vercel Geist are `coverage-only` references for state, anatomy, and accessibility. They must not repopulate Foldline with generic buttons, dashboards, product grids, command palettes, or marketing hero components.

## 5. LLM Invocation Contract

The calling LLM must derive the UI from brand profile, domain objects, and first-screen skeleton. It must not select a preset.

Required decisions on every new app:

- Name the primary user job before choosing layout.
- Extract domain objects before choosing components.
- Define the first viewport contract before visual polish.
- Translate colors into semantic roles.
- Keep Astryx/Geist as coverage references only.
- Reject outputs that converge into card grid, dashboard, marketplace feed, or landing-page hero.

## 6. Mock UI

The static mock lives in:

- `index.html`
- `styles.css`
- `app.js`

It implements a 390px-class mobile layout with real garment imagery, a vertical signal spine, look board, rationale strip, garment stack, contextual shop sheet, bottom navigation, and small interactive states.
