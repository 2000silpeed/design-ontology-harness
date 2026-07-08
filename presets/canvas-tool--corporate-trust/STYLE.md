# LookMe Try-On System Style Capsule

- preset: `canvas-tool--corporate-trust`
- brand: LookMe Toss In-App
- mode: `canvas-tool` / `corporate-trust`
- capsule_version: `1.0.0`
- companion files: `STYLE.md` is the human brief; `DESIGN.md` is the agent-ready copy.

## Taste Summary
LookMe Toss In-App custom mobile try-on system: trusted face try-on utility with real Colorfit item image sets and paid wardrobe generation.

## Authority Order
1. Product task flow and information architecture
2. `token_schema.json` and generated CSS variables
3. `components/component_specs.*` and `component_inventory.json`
4. `system_spec.md` and `system_ontology.json`
5. External visual references

Visual references are morphology inputs only. They may inform component shape, density, proportion, hierarchy rhythm, and affordance patterns; they must not override tokens, typography, domain IA, product copy, or palette composition.

## Voice And Boundaries
- brand keywords: `clear`, `fast`, `trustworthy`, `personal`, `curated`, `mobile-first`
- tone: `concise`, `reassuring`, `direct`, `privacy-aware`
- visual cues: `compact mobile funnel`, `real item image evidence`, `quiet financial-app trust`, `scan-first cards`, `clear step hierarchy`, `low elevation surfaces`
- avoid: `shopping-mall`, `generic-fashion-commerce`, `overdecorated`, `dashboard-heavy`, `playful`, `luxury-editorial`, `neon`, `glassmorphism`

## Color Roles
| Role | Token | Value | Source | Use |
| --- | --- | --- | --- | --- |
| `canvas` | `--ds-color-canvas` | `#F7F8FA` | Canvas White | Generated fallback support color |
| `surface` | `--ds-color-surface` | `#FFFFFF` | Paper | Generated fallback support color |
| `surface_muted` | `--ds-color-surface-muted` | `#EEF1F6` | Surface Muted | Generated fallback support color |
| `surface_elevated` | `--ds-color-surface-elevated` | `#FFFFFF` | Paper | Generated fallback support color |
| `border` | `--ds-color-border` | `#D6DDE6` | Border Neutral | Generated fallback support color |
| `border_strong` | `--ds-color-border-strong` | `#B0BAC7` | Border Strong | Generated fallback support color |
| `ink` | `--ds-color-ink` | `#111111` | Ink | Generated fallback support color |
| `ink_muted` | `--ds-color-ink-muted` | `#4F7942` | Fern Green | 중명도, 중채도의 내추럴 그린 / 차분함, 안정감, 유연함 |
| `ink_subtle` | `--ds-color-ink-subtle` | `#6B7280` | Subtle Ink | Generated fallback support color |
| `info` | `--ds-color-info` | `#000080` | Navy Blue | 저명도, 중채도, 차가운 온도감이 강한 블루 계열 / 신뢰, 권위, 집중, 전문성, 절제된 우아함 |
| `success` | `--ds-color-success` | `#4F7942` | Fern Green | 중명도, 중채도의 내추럴 그린 / 차분함, 안정감, 유연함 |
| `warning` | `--ds-color-warning` | `#CC7722` | Ochre | 중명도, 중채도, 흙기 섞인 따뜻한 오렌지 / 안정감, 내추럴, 신뢰감, 지속성 |
| `danger` | `--ds-color-danger` | `#E2725B` | Terracotta | 붉은 흙빛 계열, 오렌지 브라운이 섞인 따뜻한 중채 레드 / 안정감, 따뜻함, 자연스러움, 감성적 |
| `anchor_surface` | `--ds-color-anchor-surface` | `#27503D` | Forest Green | 묵직함, 안정감, 신뢰, 자연적 깊이 |

Color rule: Token binding is necessary but not sufficient. Do not recombine `--ds-*` color roles into a new reference-like palette.

## Typography
| Role | Font | Token | Notes |
| --- | --- | --- | --- |
| heading | Pretendard | `--ds-font-heading` | 한글 UI 서체의 사실상 표준. Apple SD Gothic Neo 기반이지만 더 정교함. 라틴은 Inter 계열. |
| body | Pretendard | `--ds-font-body` | 한글 UI 서체의 사실상 표준. Apple SD Gothic Neo 기반이지만 더 정교함. 라틴은 Inter 계열. |
| mono | n/a | `--ds-font-mono` | data, code, shortcuts only |
| korean | Pretendard | `--ds-font-ko` | primary script support |

- type scale: `xs`=11, `sm`=12, `md`=14, `lg`=17, `xl`=20, `2xl`=24, `3xl`=29
- line heights: `tight`=1.25, `normal`=1.4, `comfortable`=1.5, `relaxed`=1.6
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
| button | high | `default`, `hover`, `active`, `disabled`, `loading` | `primary-button`, `secondary-button`, `icon-button`, `form-actions`, `hero-cta-group`, `add-to-cart-button`, +1 more |
| copilot-artifact | high | `default`, `loading`, `verified`, `error` | `citation-drawer`, `source-card` |
| data-display | high | `default`, `sorted`, `filtered`, `empty`, `loading` | `tag`, `data-table`, `column-header`, `row-actions`, `metric-strip`, `status-summary-row`, +15 more |
| document | high | `default`, `selected`, `commenting`, `resolved` | `redline-viewer` |
| editorial | high | `default`, `selected`, `editing` | `review-card`, `score-badge`, `comparison-table`, `ranking-list` |
| feedback | high | `info`, `success`, `warning`, `danger`, `loading` | `badge`, `inline-alert`, `empty-state`, `toast`, `status-dot`, `status-badge`, +5 more |

## Signature Components
| Component | Family | Anatomy | Token Binding |
| --- | --- | --- | --- |
| `tabs` | navigation | parts: container, nav-item, icon(optional), label, indicator(active), +1 more; states: default, hover, active, collapsed | slots: surface, text, padding, font |
| `form-actions` | button | parts: container, label, leading-icon(optional), trailing-icon(optional); states: default, hover, active, disabled, l... | slots: surface, text, border, radius, padding, font |
| `tag` | data-display | parts: container, header, content-area, footer(optional), action(optional); states: default, loading, empty, error | slots: surface, text, border, radius, padding |
| `status-badge` | feedback | parts: container, icon, message, action(optional), close-button(optional); states: info, success, warning, danger | slots: surface, text, border, radius, padding |
| `chip` | input | parts: container, label, input-area, helper-text(optional), leading-icon(optional), +1 more; states: default, focus,... | slots: surface, text, border, radius, padding, font |
| `data-table` | data-display | parts: container, header, content-area, footer(optional), action(optional); states: default, loading, empty, error | slots: surface, text, border, radius, padding |

## Advanced Component Menu
| Component | Use When | Pairs With |
| --- | --- | --- |
| `bulk-action-table` | users handle many records at once; selection count and destructive actions must stay visible | `saved-view-bar`, `filter-builder`, `exception-queue` |
| `evidence-graph` | trust depends on seeing relationships between claims and sources; auditors need to trace why an answer or decision was made | `citation-drawer`, `decision-record-card`, `policy-matrix` |
| `citation-drawer` | answers must show supporting policy, document, or source records; users need to inspect evidence without losing conversation context | `inline-citation`, `source-card`, `evidence-graph` |
| `saved-view-bar` | teams revisit the same filtered views often; dense tools need stable scope memory | `filter-builder`, `bulk-action-table`, `exception-queue` |
| `source-card` | AI output depends on external or internal source records; users need a repeatable citation preview component | `citation-drawer`, `evidence-graph`, `inline-citation` |
| `redline-viewer` | legal, compliance, or editorial text needs reviewer markup; comments must stay anchored to exact text ranges | `diff-viewer`, `comment-thread`, `approval-rail` |

Use these as ontology-approved building blocks when the workflow calls for richer professional UI. They still inherit token, typography, accessibility, and reference-governance rules.

## Design Context Pack
- activation: `grounded`
- providers: `local-images`=active, `pinterest`=preview, `lazyweb`=suggested
- flow coverage: general-product-ui(covered), onboarding(covered), data-review(gap), empty-state(gap), pricing(gap)
| Context | Provider | Allowed Use |
| --- | --- | --- |
| landing-mobile | `local-images` | morphology: `general-interface-composition`; flows: `general-product-ui` |
| style-mobile | `local-images` | morphology: `general-interface-composition`; flows: `general-product-ui` |
| result-mobile | `local-images` | morphology: `general-interface-composition`; flows: `general-product-ui` |
| mobile fintech onboarding funnel | `lazyweb` | morphology: `general-interface-composition`; flows: `onboarding` |
- research gap `real-app-corpus-provider-not-connected`: Connect Lazyweb MCP or export selected Lazyweb screens into visual_reference.sources with provenance.
- research gap `flow-coverage-gaps`: Search corpus/provider screens by these flows before mock generation.

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
