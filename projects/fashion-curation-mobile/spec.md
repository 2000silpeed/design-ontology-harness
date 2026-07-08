# ThreadSense Fashion Curation Mobile App

## Product Concept

ThreadSense is a Korean-first mobile fashion curation app. It helps users turn taste signals, daily context, closet memory, and budget boundaries into one shoppable outfit edit.

The app should not feel like a generic marketplace or a fashion magazine landing page. The first screen must feel like an active styling decision surface: the user adjusts taste signals, sees a complete outfit edit, understands why it works, and can save or shop without leaving the context.

## Primary User Job

The user opens the app before going out or browsing fashion. They want one practical answer:

> "오늘 내 상황과 취향에 맞는 착장 하나를 빠르게 정하고, 필요한 아이템만 저장하거나 구매 후보로 넘긴다."

## Core Domain Objects

- taste signal: occasion, mood, weather, color preference, avoid condition
- outfit edit: one curated outfit composition with a title, confidence, reason, and items
- garment item: product or closet item with material, silhouette, price, brand, size, and replacement candidates
- fit note: why an item works for body/comfort/context
- saved closet: items the user owns or saved before
- shop drawer: contextual purchase surface attached to an outfit edit

## Mobile Screen Skeleton

### Home / Today Edit

First viewport contract:

- compact top identity row with location/weather hint and profile entry
- taste signal chip rail directly below the top row
- one large outfit edit canvas with a real fashion/garment image
- confidence and "why this works" notes visible before product list
- thumb-zone actions: Save Edit, Alternatives, Shop Drawer

Composition:

- top app bar is quiet and compact
- taste rail is sticky-looking and horizontal
- outfit canvas is dominant but not a generic hero
- product items appear as supporting pieces inside the edit, not as a marketplace grid

### Outfit Detail

Purpose:

- inspect the selected outfit edit
- compare the main garment stack and alternatives
- show why this edit fits the user's taste signals

Required regions:

- edit title and context
- garment stack
- material/silhouette notes
- closet compatibility
- size and price summary
- alternatives carousel

### Shop Drawer

Purpose:

- keep commerce attached to the curation decision
- let the user check size, price, shipping, and alternatives without losing the edit

Required regions:

- selected garment
- size chips
- price and delivery note
- save to closet
- add to cart

### Closet Memory

Purpose:

- show saved items and recent edits
- help future recommendations avoid duplicate purchases

Required regions:

- saved edits
- closet tags
- color/material coverage
- items that can complete today's edit

## Design System Goals

- Mobile-first, Korean-first.
- Editorial but operational: image-led, but the user must see a decision surface immediately.
- Tactile: fabrics, layers, and item relationships should feel inspectable.
- Low-pressure commerce: shopping actions are present, but not loud.
- Avoid black/gold luxury cliche, pastel card wall, and endless ecommerce grids.
- Use Astryx and Vercel Geist only for component taxonomy/state coverage, not visual identity.

## Component Expectations

- app shell
- compact top bar
- taste signal chip rail
- segmented control for mode changes
- outfit edit canvas
- garment item row
- item stack
- material note
- fit note
- closet compatibility badge
- save edit action
- alternatives carousel
- shop drawer
- size chip group
- bottom navigation
- toast for saved state

## Mock UI Requirement

Create a static mobile mock at `projects/fashion-curation-mobile/index.html`.

The mock must include:

- 390px-class mobile viewport layout
- real fashion/garment imagery
- first screen with taste signal rail and outfit edit canvas
- bottom navigation
- contextual shop drawer preview
- accessible labels for primary controls
- no emoji as UI icons
- no generic dashboard cards
- no marketing hero before the task surface
