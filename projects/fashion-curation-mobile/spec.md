# Foldline Fashion Curation Mobile App

## Product Concept

Foldline is a Korean-first mobile fashion curation app. It helps users turn a daily style brief, taste signals, closet memory, and budget boundaries into one outfit decision.

The app should not open like a product marketplace, a fashion magazine landing page, or a dashboard. It should feel like a compact wardrobe work surface: the user sees today's brief, understands the outfit logic, saves the look, and only then opens a contextual shop sheet for the missing garment.

## Primary User Job

The user opens the app before leaving home or while browsing clothes. They want one practical answer:

> "오늘 내 상황과 보유 옷에 맞는 한 벌을 정하고, 부족한 아이템만 구매 후보로 넘긴다."

## Core Domain Objects

- daily style brief: occasion, weather, time, comfort boundary, avoid condition
- taste signal: tone, silhouette, texture, logo tolerance, color preference
- outfit edit: one assembled look with rationale and confidence
- garment item: closet item or product candidate with material, silhouette, size, price, and replacement options
- closet memory: items the user owns or saved before
- fit note: size and comfort reason
- shop sheet: contextual bottom sheet attached to one garment inside the look board

## First Screen Skeleton

The first viewport must include:

- compact brand and daily brief row
- vertical signal spine, not a generic horizontal filter bar
- large look board with real garment imagery and layered item relationships
- "why it works" rationale before any product catalog behavior
- closet compatibility signal before price
- save look and shop sheet actions inside thumb range
- bottom navigation

The first viewport must not include:

- marketing hero section
- product grid
- dashboard metric cards
- generic card wall
- black/gold luxury styling
- explanatory onboarding copy before the actual outfit decision

## Required Surfaces

### Today Board

Purpose:

- show the daily brief and one decisive outfit
- let the user adjust taste signals without leaving the decision surface
- show the reason and closet compatibility before shopping

Required regions:

- Daily brief row
- Signal spine
- Look board
- Reason strip
- Garment stack
- Closet compatibility badge
- Save look action
- Contextual shop sheet preview

### Look Detail

Purpose:

- inspect why the look works
- compare garment layers and alternatives
- keep the recommendation explainable

Required regions:

- edit title and context
- material and silhouette notes
- garment stack
- closet compatibility
- size and price summary
- alternative rail

### Shop Sheet

Purpose:

- keep commerce attached to the outfit decision
- let the user check size, price, delivery, and alternatives without losing the look board

Required regions:

- selected garment
- size chips
- price and delivery note
- save to closet
- add candidate

### Closet Memory

Purpose:

- show what the user already owns
- reduce duplicate purchases
- feed future recommendations

Required regions:

- saved looks
- closet tags
- color/material coverage
- items that complete today's look

## Design System Goals

- Mobile-first, Korean-first.
- Editorial but operational: visual, tactile, and useful before decorative.
- No preset palette; choose semantic color roles from product context.
- Use Astryx and Vercel Geist as state/anatomy/accessibility coverage only.
- Implement product primitives first; reject generic marketing, dashboard, product-grid, and data-table components unless explicitly requested by the app flow.
- Text must fit at 320, 360, 390, and 430px widths.

## Component Expectations

Core implementation components:

- app shell
- compact topbar
- daily brief row
- taste signal spine
- taste signal chip
- look board
- outfit edit canvas
- garment stack
- garment row
- fabric swatch
- why-this-works note
- fit and size note
- closet compatibility badge
- save look action
- contextual shop sheet
- size chip group
- alternative item rail
- bottom tab bar
- saved state toast

Rejected by default:

- product grid
- product card wall
- data table
- dashboard cards
- marketing hero
- generic modal dialog
- generic command palette
- split pane
- inspector drawer

## Mock UI Requirement

Create a static mobile mock at `projects/fashion-curation-mobile/index.html`.

The mock must include:

- 390px-class mobile viewport layout
- real fashion/garment imagery
- daily brief row
- signal spine
- look board
- why-it-works rationale
- garment stack
- closet compatibility signal
- bottom navigation
- contextual shop sheet preview
- accessible labels for primary controls
- no emoji as UI icons
- no dashboard cards
- no generic product grid
- no marketing hero before the task surface
