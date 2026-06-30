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
| `primary` | `--ds-color-primary` | `#000080` | Navy Blue | 저명도, 중채도, 차가운 온도감이 강한 블루 계열 / 신뢰, 권위, 집중, 전문성, 절제된 우아함 |
| `accent` | `--ds-color-accent` | `#CC7722` | Ochre | 중명도, 중채도, 흙기 섞인 따뜻한 오렌지 / 안정감, 내추럴, 신뢰감, 지속성 |
| `surface_tint` | `--ds-color-surface-tint` | `#F5DEB3` | Wheat | 중명도, 저채도, 베이지 옐로 계열의 따뜻한 톤 / 따뜻함, 자연스러움, 부드러움, 안정감 |
| `canvas` | `--ds-color-canvas` | `#F7F8FA` | Canvas White | Generated fallback support color |
| `surface` | `--ds-color-surface` | `#FFFFFF` | Paper | Generated fallback support color |
| `surface_muted` | `--ds-color-surface-muted` | `#EEF1F6` | Surface Muted | Generated fallback support color |
| `surface_elevated` | `--ds-color-surface-elevated` | `#FFFFFF` | Paper | Generated fallback support color |
| `border` | `--ds-color-border` | `#D6DDE6` | Border Neutral | Generated fallback support color |
| `border_strong` | `--ds-color-border-strong` | `#B6B995` | Pairing #B6B995 | Seed pairing support |
| `ink` | `--ds-color-ink` | `#1C2E4A` | Pairing #1C2E4A | Seed pairing support |
| `ink_muted` | `--ds-color-ink-muted` | `#708090` | Pairing #708090 | Seed pairing support |
| `ink_subtle` | `--ds-color-ink-subtle` | `#708090` | Pairing #708090 | Seed pairing support |
| `info` | `--ds-color-info` | `#0F4C81` | Classic Blue | 중명도, 중채도, 클래식한 딥 블루 톤 / 신뢰, 평온함, 지성, 안정감 |
| `success` | `--ds-color-success` | `#4A7C59` | Success | Generated fallback support color |
| `warning` | `--ds-color-warning` | `#CC7722` | Ochre | 중명도, 중채도, 흙기 섞인 따뜻한 오렌지 / 안정감, 내추럴, 신뢰감, 지속성 |
| `danger` | `--ds-color-danger` | `#8B2252` | Danger | Generated fallback support color |
| `link` | `--ds-color-link` | `#000080` | Navy Blue | 저명도, 중채도, 차가운 온도감이 강한 블루 계열 / 신뢰, 권위, 집중, 전문성, 절제된 우아함 |

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
| button | high | `default`, `hover`, `active`, `disabled`, `loading` | `primary-button`, `secondary-button`, `ghost-button`, `icon-button`, `cta-button`, `link-button`, +4 more |
| copilot-artifact | high | `default`, `loading`, `verified`, `error` | `citation-drawer`, `source-card` |
| data-display | high | `default`, `sorted`, `filtered`, `empty` | `tag`, `data-table`, `column-header`, `row-actions`, `pricing-card`, `feature-comparison`, +14 more |
| document | high | `default`, `selected`, `commenting`, `resolved` | `redline-viewer` |
| editorial | high | `default`, `selected`, `editing` | `review-card`, `score-badge`, `comparison-table`, `ranking-list` |
| feedback | high | `info`, `success`, `warning`, `danger` | `inline-alert`, `empty-state`, `toast`, `status-badge`, `step-progress`, `banner`, +3 more |

## Signature Components
| Component | Family | Anatomy | Token Binding |
| --- | --- | --- | --- |
| `form-actions` | button | parts: container, label, leading-icon(optional), trailing-icon(optional); states: default, hover, active, disabled, l... | slots: surface, text, border, radius, padding, font |
| `tag` | data-display | parts: container, header, content-area, footer(optional), action(optional); states: default, loading, empty, error | slots: surface, text, border, radius, padding |
| `status-badge` | feedback | parts: container, icon, message, action(optional), close-button(optional); states: info, success, warning, danger | slots: surface, text, border, radius, padding |
| `chip` | input | parts: container, label, input-area, helper-text(optional), leading-icon(optional), +1 more; states: default, focus,... | slots: surface, text, border, radius, padding, font |
| `data-table` | data-display | parts: container, header, content-area, footer(optional), action(optional); states: default, loading, empty, error | slots: surface, text, border, radius, padding |
| `column-header` | data-display | parts: container, header, content-area, footer(optional), action(optional); states: default, loading, empty, error | slots: surface, text, border, radius, padding |

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
  - 기존 데이터 밀도와 업무 완료 경로를 유지한 상태에서 시각 품질을 높이는 방향을 우선.
  - 기능 위치 변경, 정보 구조 변경, 패널 제거는 별도의 migration plan이 있을 때만 수행.
  - 레퍼런스는 형태·밀도·컴포넌트 비례만 흡수하고, 색 조합·폰트 스케일·도메인 IA는 토큰과 제품 온톨로지를 따른다.
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
