# World Cup Orbit — ontology-to-mockup contract

This brief is derived from this project's generated `system_spec.md` and `tokens.css`. It does not use the existing World Cup Hub, any of its source files, or a visual reference image.

## Product state shown

Desktop web, 1440 × 1024. A viewer in Seoul is choosing a decisive 2026 World Cup knockout fixture. The screen must make the tournament consequence and the local kickoff legible before it asks for a follow action.

## Design-system bindings

| Ontology rule | Component in the mockup | Required visible expression |
| --- | --- | --- |
| `match orbit` is the primary primitive | `orbit-shell` + `match-orbit-node` | A central, stage-based orbital fixture canvas; not a grid of score cards. |
| Tournament progression is the primary hierarchy | `stage-rail` | A compact stage rail: Group Stage, Round of 32, Round of 16, Quarter-final, Semi-final, Final. |
| Explain why a match matters now | `attention-brief` | Selected fixture title, a short stakes sentence, and a single next consequence. |
| Local time is part of the decision | `local-time-ribbon` | “Sat, Jul 18 · 03:00 KST” in a high-contrast ribbon with UTC context. |
| Consequence needs a concrete destination | `knockout-path` | One drawn connector: “Winner → Quarter-final vs. Winner of …”. |
| Success ends in a follow decision | `follow-match-control` | A clear “Follow match” action with a small watch-circle presence count. |

## Token constraints

- Canvas: `#F7F8FA`; primary surface: `#FFFFFF`; quiet dividers: `#D6DDE6`.
- Ink: `#0F172A`; muted metadata: `#475569`.
- Brand role colors from Semantic OS: masthead energy `#FF0000`, cover signal `#708238`, paper field `#F3E5AB`, feature frame `#5F4B8B`, attention flash `#F5DF4D`.
- Typography: Spoqa Han Sans Neo-style crisp neo-grotesk for all UI; one restrained Playfair-style serif accent only for the selected fixture title.
- Corners: 8–16px; thin dividers; low elevation; never rounded, repeated sports-stat cards.

## Negative constraints

- No trophy hero, betting odds, casino cues, neon-esports glow, generic SaaS analytics, or score-card wall.
- No copied interface, logo, or styling from an existing World Cup product.
- No visual-reference image is used as an input.
