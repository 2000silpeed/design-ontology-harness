# Loom System Style Capsule

- preset: `marketing-landing--editorial-warm`
- brand: Loom
- mode: `marketing-landing` / `editorial-warm`
- capsule_version: `1.0.0`
- companion files: `STYLE.md` is the human brief; `DESIGN.md` is the agent-ready copy.

## Taste Summary
독립 뉴스레터·매거진 발행인용 editorial-warm 톤 마케팅 랜딩 — hero + featured issue + issue archive + subscribe pricing + testimonial + author profile + faq + cta, warm ochre + rust + wheat palette, reading-first, 한국어 1급.

## Authority Order
1. Product task flow and information architecture
2. `token_schema.json` and generated CSS variables
3. `components/component_specs.*` and `component_inventory.json`
4. `system_spec.md` and `system_ontology.json`
5. External visual references

Visual references are morphology inputs only. They may inform component shape, density, proportion, hierarchy rhythm, and affordance patterns; they must not override tokens, typography, domain IA, product copy, or palette composition.

## Voice And Boundaries
- brand keywords: `marketing-landing`, `editorial`, `newsletter`, `publisher`, `warm`, `calm`, `reading-first`, `serif-ish`, `ochre`, `rust`, +4 more
- tone: `calm`, `warm`, `thoughtful`, `literary`, `sincere`, `inviting`
- visual cues: `warm neutral backdrop`, `ochre-yellow primary emphasis`, `rust copper accent link`, `wheat cream surface tint`, `serif-ish heading pairing`, `reading-first hero`, `issue card archive strip`, `calm pricing table`, +2 more
- avoid: `bold-saturated`, `streetwear-drop`, `fintech-dense`, `playful-pastel`, `dashboard-only`, `corporate-navy`, `magazine-cover-heavy-illustration`

## Color Roles
| Role | Token | Value | Source | Use |
| --- | --- | --- | --- | --- |
| `primary` | `--ds-color-primary` | `#CB9D06` | Ochre Yellow | 중명도, 중채도, 골든 옐로 + 흙기 섞인 옐로 브라운 계열 / 따뜻함, 견고함, 전통미, 안정감, 고전적 깊이 |
| `accent` | `--ds-color-accent` | `#B7410E` | Rust | 저명도, 중채도, 오렌지와 브라운의 중간 영역 / 빈티지, 견고함, 따뜻한 노스탤지어, 공예적 감성 |
| `surface_tint` | `--ds-color-surface-tint` | `#F5DEB3` | Wheat | 중명도, 저채도, 베이지 옐로 계열의 따뜻한 톤 / 따뜻함, 자연스러움, 부드러움, 안정감 |
| `canvas` | `--ds-color-canvas` | `#F7F8FA` | Canvas White | Generated fallback support color |
| `surface` | `--ds-color-surface` | `#FFFFFF` | Paper | Generated fallback support color |
| `surface_muted` | `--ds-color-surface-muted` | `#EEF1F6` | Surface Muted | Generated fallback support color |
| `surface_elevated` | `--ds-color-surface-elevated` | `#FFFFFF` | Paper | Generated fallback support color |
| `border` | `--ds-color-border` | `#D6DDE6` | Border Neutral | Generated fallback support color |
| `border_strong` | `--ds-color-border-strong` | `#B0BAC7` | Border Strong | Generated fallback support color |
| `ink` | `--ds-color-ink` | `#111111` | Ink | Generated fallback support color |
| `ink_muted` | `--ds-color-ink-muted` | `#4B5563` | Muted Ink | Generated fallback support color |
| `ink_subtle` | `--ds-color-ink-subtle` | `#6B7280` | Subtle Ink | Generated fallback support color |
| `info` | `--ds-color-info` | `#4A6B8A` | Info | Generated fallback support color |
| `success` | `--ds-color-success` | `#4A7C59` | Success | Generated fallback support color |
| `warning` | `--ds-color-warning` | `#B7410E` | Rust | 저명도, 중채도, 오렌지와 브라운의 중간 영역 / 빈티지, 견고함, 따뜻한 노스탤지어, 공예적 감성 |
| `danger` | `--ds-color-danger` | `#E2725B` | Terracotta | 붉은 흙빛 계열, 오렌지 브라운이 섞인 따뜻한 중채 레드 / 안정감, 따뜻함, 자연스러움, 감성적 |
| `link` | `--ds-color-link` | `#CB9D06` | Ochre Yellow | 중명도, 중채도, 골든 옐로 + 흙기 섞인 옐로 브라운 계열 / 따뜻함, 견고함, 전통미, 안정감, 고전적 깊이 |

Color rule: Token binding is necessary but not sufficient. Do not recombine `--ds-*` color roles into a new reference-like palette.

## Typography
| Role | Font | Token | Notes |
| --- | --- | --- | --- |
| heading | Fraunces | `--ds-font-heading` | editorial serif-ish variable — hero-headline / featured-issue-title / pricing-tier-title / testim... |
| body | Inter | `--ds-font-body` | hero subheadline / pricing description / testimonial body / feature copy, line-height 1.6 reading... |
| mono | JetBrains Mono | `--ds-font-mono` | data, code, shortcuts only |
| korean | Pretendard | `--ds-font-ko` | primary script support |

- type scale: `xs`=12, `sm`=14, `md`=16, `lg`=21, `xl`=28, `2xl`=38, `3xl`=50
- line heights: `tight`=1.2, `normal`=1.5, `comfortable`=1.6, `relaxed`=1.75
- headline wrap: `word_break`=keep-all, `overflow_wrap`=normal, `text_wrap`=balance
- body wrap: `word_break`=keep-all, `overflow_wrap`=normal

## Spacing And Shape
- spacing scale: `0`, `2`, `4`, `8`, `12`, `16`, `24`, `32`, `48`, `64`, `96`
- density bias: `airy`
- radius scale: `none`, `sm`, `md`, `lg`, `xl`, `pill`
- corner bias: `medium`

## Component Priorities
| Family | Priority | States | Components |
| --- | --- | --- | --- |
| button | high | `default`, `hover`, `active`, `disabled`, `loading` | `primary-button`, `secondary-button`, `icon-button`, `hero-cta-group`, `form-actions`, `site-nav-cta`, +4 more |
| data-display | high | `default`, `sorted`, `filtered`, `empty`, `loading` | `pricing-card`, `feature-comparison`, `tag`, `data-table`, `column-header`, `row-actions`, +10 more |
| document | high | `default`, `selected`, `commenting`, `resolved` | `redline-viewer` |
| feedback | high | `info`, `success`, `warning`, `danger`, `loading` | `badge`, `inline-alert`, `empty-state`, `toast`, `status-dot`, `upgrade-banner`, +5 more |
| input | high | `default`, `focus`, `error`, `disabled`, `selected` | `text-field`, `select`, `checkbox`, `switch`, `segmented-control`, `textarea`, +10 more |
| marketing | high | `default`, `hover`, `in-view` | `hero-container`, `hero-eyebrow`, `hero-headline`, `hero-subheadline`, `hero-visual`, `hero-trust-strip`, +20 more |

## Signature Components
| Component | Family | Anatomy | Token Binding |
| --- | --- | --- | --- |
| `hero-cta-group` | button | parts: container, label, leading-icon(optional), trailing-icon(optional); states: default, hover, active, disabled, l... | slots: surface, text, border, radius, padding, font |
| `drop-banner` | commerce | parts: container, header, content-area, footer(optional), action(optional); states: default, loading, empty, error | slots: surface, text, border, radius, padding |
| `cover-story` | magazine | parts: container, header, content-area, footer(optional), action(optional); states: default, loading, empty, error | slots: surface, text, border, radius, padding |
| `pricing-card` | data-display | parts: container, inner-content; states: default, hover, focus-visible | slots: surface, border, radius, padding |
| `feature-comparison` | data-display | parts: container, header, content-area, footer(optional), action(optional); states: default, loading, empty, error | slots: surface, text, border, radius, padding |
| `testimonial-card` | marketing | parts: container, inner-content; states: default, hover, focus-visible | slots: surface, border, radius, padding |

## Advanced Component Menu
| Component | Use When | Pairs With |
| --- | --- | --- |
| `bulk-action-table` | users handle many records at once; selection count and destructive actions must stay visible | `saved-view-bar`, `filter-builder`, `exception-queue` |
| `evidence-graph` | trust depends on seeing relationships between claims and sources; auditors need to trace why an answer or decision was made | `citation-drawer`, `decision-record-card`, `policy-matrix` |
| `redline-viewer` | legal, compliance, or editorial text needs reviewer markup; comments must stay anchored to exact text ranges | `diff-viewer`, `comment-thread`, `approval-rail` |
| `retention-indicator` | users need to know whether a record is retained, pending, or expired; policy requires retention visibility near decisions | `decision-record-card`, `audit-timeline`, `inspector-drawer` |
| `saved-view-bar` | teams revisit the same filtered views often; dense tools need stable scope memory | `filter-builder`, `bulk-action-table`, `exception-queue` |

Use these as ontology-approved building blocks when the workflow calls for richer professional UI. They still inherit token, typography, accessibility, and reference-governance rules.

## Design Context Pack
- activation: `planned`
- providers: `pinterest`=preview, `lazyweb`=suggested
- flow coverage: general-product-ui(covered), pricing(covered), data-review(gap), onboarding(gap), settings(gap)
| Context | Provider | Allowed Use |
| --- | --- | --- |
| stratechery subscribe landing | `lazyweb` | morphology: `general-interface-composition`; flows: `general-product-ui` |
| ghost publisher hero pricing | `lazyweb` | morphology: `general-interface-composition`; flows: `pricing` |
| every newsletter landing | `lazyweb` | morphology: `general-interface-composition`; flows: `general-product-ui` |
| substack top publisher landing | `lazyweb` | morphology: `general-interface-composition`; flows: `general-product-ui` |
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
