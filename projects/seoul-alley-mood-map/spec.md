# Seoul Alley Mood Map Design System Input Spec

## 1. Product Definition

Seoul Alley Mood Map is a mobile-first place curation tool for recording and finding small Seoul places through sensory attributes rather than popularity alone. The product treats an alley, cafe, bookshop, small park, or quiet bench as a place entity with observable qualities:

- light: morning shade, yellow evening light, neon spill, cloudy softness
- sound: quiet, conversation hum, traffic edge, footsteps, music leak
- crowding: empty, steady, seat-limited, queue-prone
- texture: brick, wood, concrete, plant, paper, water, signage
- emotion: calm, focused, nostalgic, open, tucked-away, alert
- time fit: morning, lunch, late afternoon, night, rainy day

Primary promise:

```text
오늘의 기분에 맞는 골목을 감각으로 찾아보세요.
```

The design system must communicate:

- local trust without becoming a tourism brochure
- sensory evidence before popularity metrics
- clear map/list parity for accessibility
- compact mobile scanning
- transparent ontology relations behind recommendations

## 2. Ontology-Driven Product Model

The UI must expose a product ontology, not merely a set of cards.

### Core Entities

- `Place`: named location or route segment. It can be a cafe, alley, bookshop, park, stair, bridge, or rest point.
- `SensorySignal`: light, sound, crowding, texture, scent, seating, weather sensitivity.
- `MoodTag`: calm, focus, nostalgic, bright, hidden, social, reflective.
- `TimeWindow`: morning, lunch, late afternoon, evening, night, rainy.
- `Neighborhood`: area grouping such as Seochon, Euljiro, Mangwon, Haebangchon.
- `RecommendationReason`: matched mood, matched time, low crowding, saved pattern, nearby relation.
- `Evidence`: user note, visit count, observed photo/texture, last updated time, confidence level.

### Required Relations

- `Place hasSensorySignal SensorySignal`
- `Place supportsMood MoodTag`
- `Place worksBestAt TimeWindow`
- `Place belongsTo Neighborhood`
- `RecommendationReason explains Place`
- `Evidence supports SensorySignal`
- `MoodTag conflictsWith SensorySignal` for states like calm vs traffic edge
- `Place near Place` for walking chains

### UI Translation Rules

- Every place card must show at least one sensory signal, one time fit, and one confidence or evidence state.
- Recommendation cards must show why the system selected the place.
- The ontology inspector must show selected entity, direct relations, and evidence status in a human-readable way.
- Map pins are not the only navigation source; every map state needs a list equivalent.
- Ambiguous evidence must be visible as `추정`, `최근 기록 없음`, or `사용자 기록 기반` rather than hidden.

## 3. Design Direction

Design mode:

- mobile utility with a map/list workspace
- calm local companion, not travel marketing
- sensory metadata first, photo feed second
- flat, low-elevation surfaces
- compact cards for repeated objects only

Visual hierarchy:

- A fixed or sticky top control area should expose neighborhood, time window, and mood filters.
- Main content should split between map context and ranked place cards.
- Detail content should prioritize sensory profile and evidence before long editorial copy.
- The ontology panel should be readable by non-technical users and feel like recommendation transparency.

Do not:

- use tourist itinerary cards, booking CTAs, prices, or influencer-like photo feeds
- create a full landing page before the usable product
- rely on color alone for mood or confidence state
- use nested cards or decorative orb backgrounds
- dominate the UI with one hue family, beige editorial tones, purple-blue gradients, or dark slate dashboards

## 4. Screen Requirements

### 4.1 Explore

Purpose:

- Let users find a place by neighborhood, mood, and time of day.

Required anatomy:

- compact product/status header
- neighborhood selector
- time-of-day segmented control
- mood and sensory filter chips
- map panel with pins and walking chain hints
- ranked place list with match score
- selected place preview

States:

- selected pin
- filtered results
- no matching place
- uncertain evidence
- reduced-motion map state

### 4.2 Place Detail

Purpose:

- Explain what the place feels like and why it was recommended.

Required anatomy:

- place title, neighborhood, place type
- sensory profile for light, sound, crowding, texture
- best time windows
- mood tags
- evidence strip with last update and confidence
- nearby chain suggestions
- save/edit actions

Rules:

- The place description should be short and concrete.
- Sensory information must be structured and scannable.
- Texture or thumbnail evidence may appear, but it must not overpower the data.

### 4.3 Recommendation Queue

Purpose:

- Compare suggested places for the user's current context.

Required anatomy:

- recommendation reason labels
- match score and confidence
- tradeoff note such as quieter but farther, better at night, crowded on weekends
- quick save and open detail actions

Rules:

- Do not show popularity as the primary ranking signal.
- Recommendation copy must mention the ontology relation that caused the match.

### 4.4 Ontology Inspector

Purpose:

- Make the design ontology visible as a product-facing transparency layer.

Required anatomy:

- selected entity summary
- relation rows grouped by Place, SensorySignal, MoodTag, TimeWindow, Evidence
- confidence and provenance status
- graph preview or compact node list

Rules:

- It must not read like a developer log.
- Relation labels should use plain Korean and retain enough precision for QA.
- It should reveal when a recommendation is based on missing, stale, or inferred evidence.

### 4.5 Add Place

Purpose:

- Allow a user to add or refine a place record.

Required anatomy:

- place name and neighborhood
- place type selector
- sensory signal inputs
- mood tags
- time window selector
- evidence note
- confidence state

States:

- draft
- saved
- validation error
- duplicate candidate

## 5. Component Requirements

High-priority components:

- `AppShell`: mobile-first frame with desktop preview constraints.
- `ControlBar`: neighborhood, time, mood, and sensory filters.
- `SegmentedControl`: fixed-width time-of-day selector with no layout shift.
- `FilterChip`: selected, unselected, disabled, and count states.
- `MapPanel`: pin layer, selected pin, relation path, list alternative.
- `PlaceCard`: match score, sensory metadata, time fit, evidence state.
- `SensoryMeter`: light/sound/crowding/texture profile with text labels.
- `EvidenceBadge`: observed, inferred, stale, user-note, low-confidence states.
- `RecommendationCard`: reason, tradeoff, confidence, actions.
- `OntologyPanel`: relation groups, node summary, provenance.
- `AddPlaceForm`: accessible form controls and validation.

Interaction constraints:

- Touch targets must be at least 44px.
- Long Korean labels must wrap or truncate without overlapping.
- Button text must not resize layout when state changes.
- Map information must remain available through list rows.
- The user should be able to understand a recommendation without opening a hidden tooltip.

## 6. Implementation Test Target

For this harness smoke test, the implementation should include:

- one static HTML/CSS/JS mock using installed design-system tokens
- desktop and mobile layouts
- a visible ontology inspector panel
- at least three sample places and one selected place
- no external product data or remote image dependency
- lint pass through `uv run design-ontology lint-implementation --target-repo projects/seoul-alley-mood-map`
