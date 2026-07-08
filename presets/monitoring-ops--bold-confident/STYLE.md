# FairCite Evidence Console System Style Capsule

- preset: `monitoring-ops--bold-confident`
- brand: FairCite
- mode: `monitoring-ops` / `bold-confident`
- capsule_version: `1.0.0`
- companion files: `STYLE.md` is the human brief; `DESIGN.md` is the agent-ready copy.

## Taste Summary
FairCite dual-mode evidence traceability console.

## Authority Order
1. Product task flow and information architecture
2. `token_schema.json` and generated CSS variables
3. `components/component_specs.*` and `component_inventory.json`
4. `system_spec.md` and `system_ontology.json`
5. External visual references

Visual references are morphology inputs only. They may inform component shape, density, proportion, hierarchy rhythm, and affordance patterns; they must not override tokens, typography, domain IA, product copy, or palette composition.

## Voice And Boundaries
- brand keywords: `fair-trade`, `evidence-traceability`, `decision-document`, `chunk-citation`, `dual-mode-console`, `compliance`, `rights-protection`, `legal-reference`, `law-diff`, `sanction-anatomy`, +5 more
- tone: `정확한`, `차분한`, `근거 중심`, `법률 자문이 아닌 참고 판단`, `평이하지만 단정하지 않는`, `공공 서비스처럼 신뢰감 있는`
- visual cues: `dense evidence console`, `public-sector trust`, `split-pane workflow`, `citation drawer`, `source label badges`, `legal document snippets`, `structured risk matrix`, `paired case comparison`, +4 more
- avoid: `marketing-landing`, `hero-heavy`, `decorative-gradient`, `cartoon-legal`, `one-note-purple`, `one-note-blue`, `beige-law-office`, `black-box-ai`, +4 more

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
| `ink_muted` | `--ds-color-ink-muted` | `#4B5563` | Muted Ink | Generated fallback support color |
| `ink_subtle` | `--ds-color-ink-subtle` | `#6B7280` | Subtle Ink | Generated fallback support color |
| `info` | `--ds-color-info` | `#007FFF` | Azure Blue | 고명도, 고채도, 쿨톤의 청량한 블루 / 개방감, 에너지, 명료함, 신선함, 혁신 |
| `success` | `--ds-color-success` | `#50C878` | Emerald Green | 중명도, 중채도의 대중적인 청록 계열 / 고급스러움, 생명력, 세련된 안정감, 청량한 자연성 |
| `warning` | `--ds-color-warning` | `#CC7722` | Ochre | 중명도, 중채도, 흙기 섞인 따뜻한 오렌지 / 안정감, 내추럴, 신뢰감, 지속성 |
| `danger` | `--ds-color-danger` | `#8B2252` | Danger | Generated fallback support color |
| `anchor_surface` | `--ds-color-anchor-surface` | `#27503D` | Forest Green | 묵직함, 안정감, 신뢰, 자연적 깊이 |

Color rule: Token binding is necessary but not sufficient. Do not recombine `--ds-*` color roles into a new reference-like palette.

## Typography
| Role | Font | Token | Notes |
| --- | --- | --- | --- |
| heading | Pretendard | `--ds-font-heading` | Korean public-service dashboard heading. 영문/숫자와 한글 혼합에서도 안정적인 professional tone. |
| body | Pretendard | `--ds-font-body` | 의결서 요약, 법령 안내, 카드 설명에 사용. keep-all line wrapping과 1.45~1.6 line-height 권장. |
| mono | JetBrains Mono | `--ds-font-mono` | data, code, shortcuts only |
| korean | Pretendard | `--ds-font-ko` | primary script support |

- type scale: `xs`=12, `sm`=13, `md`=15, `lg`=19, `xl`=24, `2xl`=30, `3xl`=37
- line heights: `tight`=1.25, `normal`=1.45, `comfortable`=1.55, `relaxed`=1.65
- headline wrap: `word_break`=keep-all, `overflow_wrap`=normal, `text_wrap`=balance
- body wrap: `word_break`=keep-all, `overflow_wrap`=normal

## Spacing And Shape
- spacing scale: `0`, `2`, `4`, `8`, `12`, `16`, `24`, `32`, `48`, `64`, `96`
- density bias: `dense`
- radius scale: `none`, `sm`, `md`, `lg`, `xl`, `pill`
- corner bias: `medium`

## Component Priorities
| Family | Priority | States | Components |
| --- | --- | --- | --- |
| button | high | `default`, `hover`, `active`, `disabled`, `loading` | `primary-button`, `secondary-button`, `icon-button`, `form-actions`, `hero-cta-group` |
| copilot-artifact | high | `default`, `loading`, `verified`, `error` | `citation-drawer` |
| data-display | high | `default`, `sorted`, `filtered`, `empty`, `loading` | `data-table`, `column-header`, `row-actions`, `tag`, `metric-strip`, `status-summary-row`, +13 more |
| document | high | `default`, `selected`, `commenting`, `resolved` | `redline-viewer` |
| feedback | high | `info`, `success`, `warning`, `danger`, `loading` | `badge`, `inline-alert`, `empty-state`, `toast`, `status-dot`, `status-badge`, +3 more |
| input | high | `default`, `focus`, `error`, `disabled`, `selected` | `text-field`, `select`, `checkbox`, `switch`, `segmented-control`, `filter-chip`, +6 more |

## Signature Components
| Component | Family | Anatomy | Token Binding |
| --- | --- | --- | --- |
| `data-table` | data-display | parts: container, header, content-area, footer(optional), action(optional); states: default, loading, empty, error | slots: surface, text, border, radius, padding |
| `status-badge` | feedback | parts: container, icon, message, action(optional), close-button(optional); states: info, success, warning, danger | slots: surface, text, border, radius, padding |
| `metric-strip` | data-display | parts: container, header, content-area, footer(optional), action(optional); states: default, loading, empty, error | slots: surface, text, border, radius, padding |
| `status-summary-row` | data-display | parts: container, header, content-area, footer(optional), action(optional); states: default, loading, empty, error | slots: surface, text, border, radius, padding |
| `chart-container` | data-display | parts: container, header, content-area, footer(optional), action(optional); states: default, loading, empty, error | slots: surface, text, border, radius, padding |
| `chart-tooltip` | overlay | parts: backdrop, container, header, content, footer(optional), +1 more; states: closed, opening, open, closing | slots: surface, border, radius, padding |

## Advanced Component Menu
| Component | Use When | Pairs With |
| --- | --- | --- |
| `approval-rail` | work requires review, approval, rejection, or handoff; users need to know who owns the next decision | `policy-matrix`, `risk-summary-card`, `diff-viewer` |
| `audit-timeline` | regulated workflows require traceable user and AI actions; reviewers need to reconstruct what happened before approval | `decision-record-card`, `approval-rail`, `tool-call-trace` |
| `citation-drawer` | answers must show supporting policy, document, or source records; users need to inspect evidence without losing conversation context | `inline-citation`, `source-card`, `evidence-graph` |
| `evidence-graph` | trust depends on seeing relationships between claims and sources; auditors need to trace why an answer or decision was made | `citation-drawer`, `decision-record-card`, `policy-matrix` |
| `policy-matrix` | multiple policy rules must be checked against multiple claims or fields; reviewers need dense scan-and-drill compliance status | `risk-summary-card`, `exception-queue`, `approval-rail` |
| `saved-view-bar` | teams revisit the same filtered views often; dense tools need stable scope memory | `filter-builder`, `bulk-action-table`, `exception-queue` |
| `bulk-action-table` | users handle many records at once; selection count and destructive actions must stay visible | `saved-view-bar`, `filter-builder`, `exception-queue` |
| `command-palette` | the product has many actions or navigation targets; expert users benefit from quick action search | `shortcut-hint`, `saved-view-bar`, `filter-builder` |

Use these as ontology-approved building blocks when the workflow calls for richer professional UI. They still inherit token, typography, accessibility, and reference-governance rules.

## Design Context Pack
- activation: `planned`
- providers: `pinterest`=preview, `lazyweb`=suggested
- flow coverage: dashboard(covered), document(covered), data-review(covered), general-product-ui(covered), navigation(gap)
| Context | Provider | Allowed Use |
| --- | --- | --- |
| government evidence dashboard split pane | `lazyweb` | morphology: `split-pane`, `evidence`; flows: `dashboard` |
| legal research citation drawer | `lazyweb` | morphology: `evidence`, `split-pane`; flows: `document` |
| compliance risk matrix enterprise console | `lazyweb` | morphology: `dense-table`; flows: `general-product-ui` |
| public service data dashboard korean | `lazyweb` | morphology: `general-interface-composition`; flows: `dashboard` |
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
