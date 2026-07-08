# PL Stats System Style Capsule

- preset: `marketing-landing--bold-confident`
- brand: PL Stats
- mode: `marketing-landing` / `bold-confident`
- capsule_version: `1.0.0`
- companion files: `STYLE.md` is the human brief; `DESIGN.md` is the agent-ready copy.

## Taste Summary
프리미어리그 팬 허브 — 대담한 고대비 랜딩/마케팅, 팀·경기 시각 임팩트.

## Authority Order
1. Product task flow and information architecture
2. `token_schema.json` and generated CSS variables
3. `components/component_specs.*` and `component_inventory.json`
4. `system_spec.md` and `system_ontology.json`
5. External visual references

Visual references are morphology inputs only. They may inform component shape, density, proportion, hierarchy rhythm, and affordance patterns; they must not override tokens, typography, domain IA, product copy, or palette composition.

## Voice And Boundaries
- brand keywords: `bold`, `precise`, `energetic`
- tone: `confident`, `data-driven`, `exciting`
- visual cues: `strong contrast`, `data-rich layout`, `sport editorial`, `dark mode first`
- avoid: `generic`, `cluttered`, `childish`

## Color Roles
| Role | Token | Value | Source | Use |
| --- | --- | --- | --- | --- |
| `canvas` | `--ds-color-canvas` | `#F7F8FA` | Canvas White | Generated fallback support color |
| `surface` | `--ds-color-surface` | `#FFFFFF` | Paper | Generated fallback support color |
| `surface_muted` | `--ds-color-surface-muted` | `#EEF1F6` | Surface Muted | Generated fallback support color |
| `surface_elevated` | `--ds-color-surface-elevated` | `#FFFFFF` | Paper | Generated fallback support color |
| `border` | `--ds-color-border` | `#D6DDE6` | Border Neutral | Generated fallback support color |
| `border_strong` | `--ds-color-border-strong` | `#B0BAC7` | Border Strong | Generated fallback support color |
| `ink` | `--ds-color-ink` | `#1A1A2E` | Midnight Navy | 신뢰감, 안정감, 집중 |
| `ink_muted` | `--ds-color-ink-muted` | `#4A4A5E` | Steel Gray | 안정감, 중립 |
| `ink_subtle` | `--ds-color-ink-subtle` | `#78909C` | Draw Gray | 중립, 안정감 |
| `info` | `--ds-color-info` | `#1A1A2E` | Midnight Navy | 신뢰감, 안정감, 집중 |
| `success` | `--ds-color-success` | `#00FF85` | Electric Green | 활기, 생동감, 주목성 |
| `warning` | `--ds-color-warning` | `#FFD700` | Golden Score | 열정, 주목성, 상징적 |
| `danger` | `--ds-color-danger` | `#E90052` | Matchday Red | 강렬함, 열정, 주목성 |
| `anchor_background` | `--ds-color-anchor-background` | `#000080` | Navy Blue | 신뢰, 권위, 집중, 전문성, 절제된 우아함 |

Color rule: Token binding is necessary but not sufficient. Do not recombine `--ds-*` color roles into a new reference-like palette.

## Typography
| Role | Font | Token | Notes |
| --- | --- | --- | --- |
| heading | Spoqa Han Sans Neo | `--ds-font-heading` | 스포카에서 만든 한글 산세리프. Source Sans Pro 기반. 깔끔한 데이터 UI에 적합. |
| body | Spoqa Han Sans Neo | `--ds-font-body` | 스포카에서 만든 한글 산세리프. Source Sans Pro 기반. 깔끔한 데이터 UI에 적합. |
| mono | JetBrains Mono | `--ds-font-mono` | data, code, shortcuts only |
| korean | Spoqa Han Sans Neo | `--ds-font-ko` | primary script support |

- type scale: `xs`=12, `sm`=14, `md`=16, `lg`=21, `xl`=28, `2xl`=38, `3xl`=50
- line heights: `tight`=1.2, `normal`=1.5, `comfortable`=1.6, `relaxed`=1.75
- headline wrap: `word_break`=keep-all, `overflow_wrap`=normal, `text_wrap`=balance
- body wrap: `word_break`=keep-all, `overflow_wrap`=normal

## Spacing And Shape
- spacing scale: `0`, `2`, `4`, `8`, `12`, `16`, `24`, `32`, `48`, `64`, `96`
- radius scale: `none`, `sm`, `md`, `lg`, `xl`, `pill`

## Component Priorities
| Family | Priority | States | Components |
| --- | --- | --- | --- |
| button | high | `default`, `hover`, `active`, `disabled`, `loading` | `primary-button`, `secondary-button`, `icon-button`, `form-actions`, `hero-cta-group` |
| data-display | high | `default`, `sorted`, `filtered`, `empty`, `loading` | `data-table`, `list`, `metadata-list`, `column-header`, `row-actions`, `search-results`, +23 more |
| feedback | high | `info`, `success`, `warning`, `danger`, `loading` | `filter-chip`, `badge`, `inline-alert`, `empty-state`, `toast`, `status-dot`, +2 more |
| input | high | `default`, `focus`, `error`, `disabled`, `selected` | `text-field`, `select`, `checkbox`, `switch`, `segmented-control`, `filter-chip`, +10 more |
| layout | high | `default`, `responsive` | `resizable-split-pane` |
| marketing | high | `default`, `hover`, `in-view` | `hero-container`, `hero-eyebrow`, `hero-headline`, `hero-subheadline`, `hero-visual`, `hero-trust-strip` |

## Signature Components
| Component | Family | Anatomy | Token Binding |
| --- | --- | --- | --- |
| `hero-cta-group` | button | parts: container, label, leading-icon(optional), trailing-icon(optional); states: default, hover, active, disabled, l... | slots: surface, text, border, radius, padding, font |
| `feature-comparison` | data-display | parts: container, header, content-area, footer(optional), action(optional); states: default, loading, empty, error | slots: surface, text, border, radius, padding |
| `hero-container` | marketing | parts: section-container, inner-max-width, content; states: default, in-view, hover | slots: text |
| `hero-eyebrow` | marketing | parts: eyebrow-label; states: default | slots: font |
| `hero-headline` | marketing | parts: heading-text; states: default | slots: font |
| `hero-subheadline` | marketing | parts: body-text; states: default | slots: font |

## Advanced Component Menu
| Component | Use When | Pairs With |
| --- | --- | --- |
| `bulk-action-table` | users handle many records at once; selection count and destructive actions must stay visible | `saved-view-bar`, `filter-builder`, `exception-queue` |
| `command-palette` | the product has many actions or navigation targets; expert users benefit from quick action search | `shortcut-hint`, `saved-view-bar`, `filter-builder` |
| `filter-builder` | users need AND/OR logic across several fields; filters should be saved, shared, or audited | `saved-view-bar`, `bulk-action-table`, `exception-queue` |
| `saved-view-bar` | teams revisit the same filtered views often; dense tools need stable scope memory | `filter-builder`, `bulk-action-table`, `exception-queue` |
| `exception-queue` | multiple issues require triage, assignment, and resolution; reviewers need to batch handle exceptions | `bulk-action-table`, `policy-matrix`, `approval-rail` |
| `resizable-split-pane` | primary work happens between list, canvas/chat, and detail panels; users need to compare or inspect adjacent information without navigation | `thread-list`, `artifact-preview-panel`, `inspector-drawer` |
| `risk-summary-card` | users need a fast read of risk before drilling into policy details; AI confidence or compliance severity must be visible | `policy-matrix`, `confidence-meter`, `exception-queue` |
| `approval-rail` | work requires review, approval, rejection, or handoff; users need to know who owns the next decision | `policy-matrix`, `risk-summary-card`, `diff-viewer` |

Use these as ontology-approved building blocks when the workflow calls for richer professional UI. They still inherit token, typography, accessibility, and reference-governance rules.

## Design Context Pack
- No provider-neutral design context pack found. Use external references only after reading `system_spec.md`.

## Reference Governance
- allowed from references: `component morphology`, `layout density`, `panel/card proportions`, `hierarchy rhythm`, `interaction affordance patterns`
- denied from references: `color palette`, `palette composition or derived secondary palettes`, `typography family or scale`, `semantic status colors`, `product copy`, `product data model`, `navigation labels`, `domain information architecture`, `redistributable imagery unless explicitly licensed`
- implementation guardrails:
  - 기존 핵심 화면, 진입점, 작업 흐름은 명시적 승인 없이 제거하거나 숨기지 않음.
  - 전면 셸 리라이트보다 토큰 -> primitive -> feature surface 순서의 점진적 롤아웃을 우선.
  - 새 시각 규칙은 지원 대상 테마와 breakpoint 전체에서 먼저 검증.
  - 일반(light) 모드와 dark 모드를 함께 제공하고, light를 기본 :root 또는 앱 기본값으로 둠.
  - 모바일 320/360/390/430px에서 horizontal scroll 또는 버튼/CTA 잘림이 있으면 완료로 보지 않음.
  - 버튼·CTA·탭·필터칩·툴바 액션은 fixed width/min-width에 의존하지 않고 wrap 또는 stack fallback을 가져야 함.
- visual asset medium selection: Visual asset slots must choose the medium that matches the subject and runtime role; narrative/content media needs high-fidelity raster or approved production artwork, not ad-hoc SVG sketches.
  - medium override `user-raster-asset-directive`: project-local raster image asset.; denied `svg`, `inline svg`, `deterministic svg placeholder`; triggers `SVG 만들지 말고`, `SVG 금지`, `실제 그림파일`, `실제 이미지 파일`, +6 more
  - A user/reviewer sentence such as 'SVG 만들지 말고 실제 그림파일로 만들거나 검색해서 넣어' is a binding medium override, not a preference. Store it in governance/system_ontology/IMPLEMENTATION_CONTRACT and satisfy it before visual QA.
  - When a raster-only/no-SVG directive is active, do not create SVG avatars, inline SVG sprites, SVG favicons, SVG placeholder art, or SVG UI icons for the affected scope; create or source project-local PNG/WebP/JPEG assets instead.
  - Comic, manga, and webtoon cover or panel-preview slots default to image_gen-generated raster, user-supplied artwork, or licensed/sourced artwork.
- failure pattern `token-bound-reference-palette-mixing`: Token binding is necessary but not sufficient; color role composition must still follow the ontology palette roles.
- prevention: Derived colors may alias a semantic token or mix one semantic role with a neutral surface/transparent value. Do not mix multiple chromatic roles to create a local palette.

## Agent Preflight
1. Read `design-system/IMPLEMENTATION_CONTRACT.md` before UI edits.
2. Read this capsule, then `system_spec.md`, `token_schema.json`, and `components/component_specs.md`.
3. Use external references only for morphology and density. Keep colors, fonts, IA, and copy ontology-led.
4. Run implementation lint before calling the screen complete:

```bash
uv run design-ontology lint-implementation --target-repo .
```
