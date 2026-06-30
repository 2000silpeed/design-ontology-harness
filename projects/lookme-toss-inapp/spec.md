# LookMe Toss In-App UI Design System Input Spec

## 1. Product Definition

LookMe Toss In-App is a mobile-first personal try-on funnel. It is not a clothing purchase app and must not feel like a fashion commerce storefront. The first value moment is a free AI outfit image on the user's face using a selected body sample and a real Colorfit item image set. The premium value is paid wardrobe generation: users register their own clothing and accessory images, combine them, and create outfit shots with credits.

Primary promise:

```text
내 얼굴에 먼저 입혀보고, 내 아이템 착장샷까지 만들어보세요.
```

The design system must communicate:

- face/photo privacy and AI processing clarity
- short Toss in-app funnel speed
- real item image evidence from Colorfit
- explicit free vs paid boundaries
- mobile touch ergonomics

## 2. Current Implementation Audit

Target repo path:

```text
/Users/sungwoon/ai-projects/lookme-toss-inapp
```

Runtime:

- `server.py`: standard-library HTTP server, SQLite API state, static SPA serving.
- `web/index.html`: one-page app shell.
- `web/app.js`: route rendering and API calls.
- `web/styles.css`: CSS variable tokens and component classes.
- `seeds/style_sets.json`: Colorfit item image set catalog with `items[]`.
- `seeds/body_sample_templates.json`: body sample catalog.

Current routes:

- `/toss`: landing and free CTA
- `/toss/consent`: required/optional consent groups
- `/toss/face`: camera/gallery upload and preview
- `/toss/body-sample`: body sample selection
- `/toss/style-set`: Colorfit item set selection
- `/toss/generating`: progress state
- `/toss/result`: AI result, save/share, upsell
- `/toss/credits`: credit products and placeholder payment
- `/toss/wardrobe`: paid item upload, item selection, wardrobe generation

Current component primitives:

- app shell
- sticky topbar
- wallet pill
- stepper
- bottom fixed CTA bar
- consent row
- upload zone
- body sample card
- style item set card
- result viewer
- credit product card
- wardrobe item card
- toast
- error panel

Observed issues to improve:

- The landing visual is too decorative for a Toss in-app utility and pushes the product action downward.
- Several card groups are visually heavy and can read like nested marketing cards.
- Style cards show real items, but long product names dominate the hierarchy.
- Body sample cards use placeholder silhouettes without enough selection affordance.
- The topbar and bottom CTA work, but the screen rhythm needs a stronger task header/status model.
- Credit and wardrobe flows need a clearer paid boundary without making the whole app feel commerce-led.

## 3. Design Direction

Design mode:

- mobile utility, not landing-page marketing
- compact, scan-first, task-progress oriented
- quiet financial-app trust with real item images as the visual focus
- cards only for repeated selectable objects, not page-level containers
- restrained color, high text contrast, low elevation

Visual hierarchy:

- Every screen starts with a compact task header: title, one-line purpose, progress or status where relevant.
- One primary action per screen, fixed bottom on mobile.
- Secondary actions remain quiet and inline.
- Real images should carry the visual richness; chrome should stay flat and calm.
- Long product names should be truncated in chips and card metadata; full item evidence comes from image thumbnails.

Do not:

- copy `contract-copilot-mock`
- use commerce checkout IA or price-forward product cards as the main pattern
- use large decorative gradient heroes after the landing entry
- create nested cards
- dominate the UI with one hue family, purple-blue gradients, beige editorial palettes, or shopping mall red/orange emphasis
- use visible help text explaining UI mechanics or keyboard shortcuts

## 4. Screen Requirements

### 4.1 Landing

Purpose:

- Start the free face try-on with immediate trust.

Required anatomy:

- compact brand/status row
- direct headline
- one-sentence value proposition
- small evidence strip showing real Colorfit item images
- privacy trust note
- primary CTA: `무료로 1회 만들어보기`

Layout:

- first viewport must show the CTA and a hint of item image evidence
- no app dashboard navigation
- hero should feel like the first screen of a utility, not a marketing page

### 4.2 Consent

Purpose:

- Separate required consent and optional consent.

Required anatomy:

- screen title
- required group list with checkboxes
- optional group list visually separated
- privacy note about face/photo processing and retention
- fixed bottom CTA

States:

- CTA available but validation blocks submission if required items are missing
- error state for missing required consent

### 4.3 Face Upload

Purpose:

- Capture or upload the user's face photo.

Required anatomy:

- photo preview or empty upload control
- guidance copy
- file validation error state
- fixed bottom CTA

Visual behavior:

- Empty state should be plain and trustworthy.
- Preview should be large enough for user confidence.

### 4.4 Body Sample Selection

Purpose:

- Choose a similar body sample for pose/body reference.

Required anatomy:

- body sample cards
- safe wording: `비슷한 체형 샘플`, `착장 미리보기용 바디 템플릿`
- selected state with strong border/ring and check affordance

Layout:

- one-column list on mobile
- cards use consistent minimum height and no layout shift

### 4.5 Colorfit Item Set Selection

Purpose:

- Choose a real Colorfit clothing/accessory image set.

Required anatomy:

- item image collage
- item set name and description
- small item category/name chips
- premium/free badge
- selected state

Rules:

- Images are primary evidence.
- Long source product names should not crowd the selection task.
- No price, mall link, product-card CTA, or shopping language.

### 4.6 Generation Progress

Purpose:

- Confirm processing and prevent user uncertainty.

Required anatomy:

- compact progress indicator
- short status copy
- selected item set/body summary when available

Motion:

- subtle, reduced-motion safe

### 4.7 Result

Purpose:

- Show generated outfit image and convert to save/share/paid next action.

Required anatomy:

- large result image
- generation state summary
- save/share secondary actions
- `다른 스타일로 만들기`
- wardrobe paid CTA
- free generation used message when applicable

### 4.8 Credits

Purpose:

- Charge credits in a placeholder/test mode.

Required anatomy:

- current balance
- credit product rows
- cost rules summary: style set generation 1 credit, wardrobe generation 2 credits
- payment state feedback

Rules:

- It may include payment UX, but must not visually become clothing commerce.

### 4.9 Wardrobe

Purpose:

- Paid registration of user-owned clothing/accessory images and wardrobe generation.

Required anatomy:

- paid boundary state if balance is zero
- upload form with category and name
- item grid
- selected item count
- generation CTA with 2-credit cost

Rules:

- User-owned item images are the focus.
- The paid boundary must be clear before upload.

## 5. Component Families

Core components:

- AppShell
- TopBar
- TaskHeader
- StepProgress
- BottomActionBar
- PrimaryButton
- SecondaryButton
- IconButton
- WalletBadge
- ConsentRow
- UploadField
- BodySampleCard
- ItemSetCard
- ItemImageCollage
- Chip
- Badge
- ResultImageFrame
- CreditProductRow
- WardrobeUploadForm
- WardrobeItemTile
- Toast
- ErrorBanner
- EmptyState

Component morphology:

- Cards: radius 8px or less, flat border, selected ring.
- Buttons: 44-52px height, no pill except small status badges/chips.
- Image collages: fixed aspect ratio and object-fit cover.
- Chips: compact and truncating.
- Topbar: sticky, 52-56px, no heavy blur or large shadows.
- Bottom bar: fixed, safe-area aware, one primary action.

## 6. Token Requirements

Color roles:

- `surface.canvas`: app background
- `surface.base`: screen surface
- `surface.subtle`: quiet controls and grouped rows
- `text.primary`
- `text.secondary`
- `border.default`
- `action.primary`
- `action.primaryText`
- `action.subtle`
- `state.success`
- `state.warning`
- `state.danger`
- `focus.ring`

Typography:

- Korean-first sans stack.
- No viewport-width font scaling.
- No negative letter spacing.
- Hero-scale type only on landing; compact panels use smaller headings.
- Body and form text minimum 16px on mobile.
- Tabular figures for credit balance.

Spacing:

- 4px base grid.
- mobile page padding 16px.
- vertical rhythm: 8/12/16/24/32.
- repeated selectable cards gap 10-12px.

Radii and elevation:

- default radius 8px.
- small radius 6px.
- avoid large rounded card-heavy styling.
- elevation only for overlay/toast; repeated cards use border + fill.

## 7. Accessibility And Verification

Requirements:

- WCAG 2.2 AA contrast for text and controls.
- Touch target minimum 44px.
- Keyboard focus visible.
- Buttons and file inputs have accessible names.
- No text overflow outside buttons/cards on 390px mobile and desktop preview.
- Result and item images include useful alt text where user-facing.

Verification:

- Run API smoke test.
- Use Playwright mobile and desktop screenshots.
- Check console errors.
- Inspect image natural sizes for key result/item images.

## 8. Implementation Contract Hints

Generated docs are authority for UI decisions.

Allowed reference absorption:

- component morphology
- layout density
- hierarchy rhythm
- touch target ergonomics

Forbidden absorption:

- external color palettes
- external fonts
- external copy
- external IA
- `contract-copilot-mock` visual style

Implementation should update:

- `web/styles.css` tokens and component CSS
- `web/app.js` markup/anatomy where needed
- design-system docs in target repo

Implementation should preserve:

- API endpoints
- route names
- free generation rule
- credit rules
- Colorfit real item image set usage
- paid wardrobe item registration/generation
