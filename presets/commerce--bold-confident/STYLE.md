# Drop System Style Capsule

- preset: `commerce--bold-confident`
- brand: Drop
- mode: `commerce` / `bold-confident`
- capsule_version: `1.0.0`
- companion files: `STYLE.md` is the human brief; `DESIGN.md` is the agent-ready copy.

## Taste Summary
젊은 B2C 커머스 — bold-confident 톤 드롭·제품 그리드·장바구니·체크아웃, 한국어 1급.

## Authority Order
1. Product task flow and information architecture
2. `token_schema.json` and generated CSS variables
3. `components/component_specs.*` and `component_inventory.json`
4. `system_spec.md` and `system_ontology.json`
5. External visual references

Visual references are morphology inputs only. They may inform component shape, density, proportion, hierarchy rhythm, and affordance patterns; they must not override tokens, typography, domain IA, product copy, or palette composition.

## Voice And Boundaries
- brand keywords: `commerce`, `ecommerce`, `shop`, `store`, `product-grid`, `product-detail`, `cart`, `checkout`, `drop`, `merchandise`, +4 more
- tone: `confident`, `energetic`, `direct`, `hype`, `street`
- visual cues: `saturated primary hero`, `high-contrast headline`, `dense product grid`, `large product hero image`, `impact typography`, `purple accent callout`, `full-bleed drop banner`, `bold price tag`, +1 more
- avoid: `editorial-warm`, `magazine-serif`, `minimal`, `playful-pastel`, `corporate-conservative`, `dashboard-heavy`, `document-heavy`

## Color Roles
| Role | Token | Value | Source | Use |
| --- | --- | --- | --- | --- |
| `primary` | `--ds-color-primary` | `#BD2E4A` | Crimson | 짙은 레드 계열, 중채도와 저명도의 깊은 톤 / 고급스러움, 강렬함, 감정적, 웅장함, 고전적 |
| `accent` | `--ds-color-accent` | `#6C3BAA` | Royal Purple | 중명도, 고채도의 따뜻한 웜 퍼플 톤 / 장엄함, 품격, 권위, 카리스마 |
| `surface_tint` | `--ds-color-surface-tint` | `#F3E5AB` | Buttercream | 고명도, 저채도, 크리미한 웜 옐로 톤 / 부드러움, 따뜻함, 포근함, 달콤함 |
| `canvas` | `--ds-color-canvas` | `#F7F8FA` | Canvas White | Generated fallback support color |
| `surface` | `--ds-color-surface` | `#FFFFFF` | Paper | Generated fallback support color |
| `surface_muted` | `--ds-color-surface-muted` | `#EEF1F6` | Surface Muted | Generated fallback support color |
| `surface_elevated` | `--ds-color-surface-elevated` | `#FFFFFF` | Paper | Generated fallback support color |
| `border` | `--ds-color-border` | `#D6DDE6` | Border Neutral | Generated fallback support color |
| `border_strong` | `--ds-color-border-strong` | `#C4B8A2` | Pairing #C4B8A2 | Seed pairing support |
| `ink` | `--ds-color-ink` | `#111111` | Ink | Generated fallback support color |
| `ink_muted` | `--ds-color-ink-muted` | `#4B5563` | Muted Ink | Generated fallback support color |
| `ink_subtle` | `--ds-color-ink-subtle` | `#6B7280` | Subtle Ink | Generated fallback support color |
| `info` | `--ds-color-info` | `#6C3BAA` | Royal Purple | 중명도, 고채도의 따뜻한 웜 퍼플 톤 / 장엄함, 품격, 권위, 카리스마 |
| `success` | `--ds-color-success` | `#4A7C59` | Success | Generated fallback support color |
| `warning` | `--ds-color-warning` | `#EC5800` | Persimmon | 명도, 고채도, 오렌지와 레드 사이의 진한 웜톤 / 생동감, 따뜻함, 안정감, 자연의 활기 |
| `danger` | `--ds-color-danger` | `#BD2E4A` | Crimson | 짙은 레드 계열, 중채도와 저명도의 깊은 톤 / 고급스러움, 강렬함, 감정적, 웅장함, 고전적 |
| `link` | `--ds-color-link` | `#BD2E4A` | Crimson | 짙은 레드 계열, 중채도와 저명도의 깊은 톤 / 고급스러움, 강렬함, 감정적, 웅장함, 고전적 |

Color rule: Token binding is necessary but not sufficient. Do not recombine `--ds-*` color roles into a new reference-like palette.

## Typography
| Role | Font | Token | Notes |
| --- | --- | --- | --- |
| heading | Space Grotesk | `--ds-font-heading` | geometric sans with impact, drop banner / hero headline / product title / price tag — serif 금지 |
| body | Inter | `--ds-font-body` | product description / cart item / checkout step / filter label 본문 공용, line-height 1.4–1.5 (commer... |
| mono | JetBrains Mono | `--ds-font-mono` | data, code, shortcuts only |
| korean | Pretendard | `--ds-font-ko` | primary script support |

- type scale: `xs`=12, `sm`=13, `md`=15, `lg`=19, `xl`=24, `2xl`=30, `3xl`=37
- line heights: `tight`=1.25, `normal`=1.45, `comfortable`=1.55, `relaxed`=1.65
- headline wrap: `word_break`=keep-all, `overflow_wrap`=normal, `text_wrap`=balance
- body wrap: `word_break`=keep-all, `overflow_wrap`=normal

## Spacing And Shape
- spacing scale: `0`, `2`, `4`, `8`, `12`, `16`, `24`, `32`, `48`, `64`, `96`
- density bias: `balanced`
- radius scale: `none`, `sm`, `md`, `lg`, `xl`, `pill`
- corner bias: `pill`

## Component Priorities
| Family | Priority | States | Components |
| --- | --- | --- | --- |
| button | high | `default`, `hover`, `active`, `disabled`, `loading` | `primary-button`, `secondary-button`, `icon-button`, `add-to-cart-button`, `wishlist-toggle`, `form-actions`, +4 more |
| data-display | high | `default`, `sorted`, `filtered`, `empty`, `loading` | `tag`, `pricing-card`, `feature-comparison`, `metric-strip`, `status-summary-row`, `task-surface-header`, +19 more |
| document | high | `default`, `selected`, `commenting`, `resolved` | `callout`, `admonition-block`, `api-reference-table`, `parameter-table`, `redline-viewer` |
| feedback | high | `info`, `success`, `warning`, `danger`, `loading` | `badge`, `inline-alert`, `empty-state`, `toast`, `status-dot`, `discount-badge`, +8 more |
| input | high | `default`, `focus`, `error`, `disabled`, `selected` | `text-field`, `select`, `checkbox`, `switch`, `segmented-control`, `variant-selector`, +19 more |
| marketing | high | `default`, `hover`, `in-view` | `hero-container`, `hero-eyebrow`, `hero-headline`, `hero-subheadline`, `hero-visual`, `hero-trust-strip`, +8 more |

## Signature Components
| Component | Family | Anatomy | Token Binding |
| --- | --- | --- | --- |
| `product-detail` | commerce | parts: container, header, content-area, footer(optional), action(optional); states: default, loading, empty, error | slots: surface, text, border, radius, padding |
| `quick-view-modal` | overlay | parts: backdrop, container, header, content, footer(optional), +1 more; states: closed, opening, open, closing | slots: surface, border, radius, padding |
| `product-grid` | commerce | parts: grid-container; states: default | read component spec |
| `product-card` | commerce | parts: container, inner-content; states: default, hover, focus-visible | slots: surface, border, radius, padding |
| `cross-sell-grid` | commerce | parts: grid-container; states: default | read component spec |
| `cart-item` | commerce | parts: container, header, content-area, footer(optional), action(optional); states: default, loading, empty, error | slots: surface, text, border, radius, padding |

## Advanced Component Menu
| Component | Use When | Pairs With |
| --- | --- | --- |
| `inspector-drawer` | a selected item needs rich detail without leaving the main workflow; users need source facts, owners, versions, or retention metadata | `policy-matrix`, `citation-drawer`, `decision-record-card` |
| `saved-view-bar` | teams revisit the same filtered views often; dense tools need stable scope memory | `filter-builder`, `bulk-action-table`, `exception-queue` |
| `bulk-action-table` | users handle many records at once; selection count and destructive actions must stay visible | `saved-view-bar`, `filter-builder`, `exception-queue` |
| `command-palette` | the product has many actions or navigation targets; expert users benefit from quick action search | `shortcut-hint`, `saved-view-bar`, `filter-builder` |
| `evidence-graph` | trust depends on seeing relationships between claims and sources; auditors need to trace why an answer or decision was made | `citation-drawer`, `decision-record-card`, `policy-matrix` |
| `filter-builder` | users need AND/OR logic across several fields; filters should be saved, shared, or audited | `saved-view-bar`, `bulk-action-table`, `exception-queue` |
| `redline-viewer` | legal, compliance, or editorial text needs reviewer markup; comments must stay anchored to exact text ranges | `diff-viewer`, `comment-thread`, `approval-rail` |

Use these as ontology-approved building blocks when the workflow calls for richer professional UI. They still inherit token, typography, accessibility, and reference-governance rules.

## Design Context Pack
- activation: `planned`
- providers: `pinterest`=preview, `lazyweb`=suggested
- flow coverage: general-product-ui(covered), data-review(covered), pricing(covered), empty-state(gap), navigation(gap)
| Context | Provider | Allowed Use |
| --- | --- | --- |
| nike streetwear drop commerce | `lazyweb` | morphology: `general-interface-composition`; flows: `general-product-ui` |
| supreme product grid | `lazyweb` | morphology: `dense-table`; flows: `data-review` |
| kith product detail bold | `lazyweb` | morphology: `general-interface-composition`; flows: `general-product-ui` |
| ssense checkout flow | `lazyweb` | morphology: `general-interface-composition`; flows: `pricing` |
- research gap `no-observed-screens`: Capture or export 3-8 representative screens before treating morphology guidance as grounded.
- research gap `real-app-corpus-provider-not-connected`: Connect Lazyweb MCP or export selected Lazyweb screens into visual_reference.sources with provenance.

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
