# Atelier System Style Capsule

- preset: `canvas-tool--minimal-tech`
- brand: Atelier
- mode: `canvas-tool` / `minimal-tech`
- capsule_version: `1.0.0`
- companion files: `STYLE.md` is the human brief; `DESIGN.md` is the agent-ready copy.

## Taste Summary
크리에이티브 팀을 위한 minimal-tech 톤 캔버스 · 레이어 · 인스펙터 도구 — keyboard-first, 한국어 1급.

## Authority Order
1. Product task flow and information architecture
2. `token_schema.json` and generated CSS variables
3. `components/component_specs.*` and `component_inventory.json`
4. `system_spec.md` and `system_ontology.json`
5. External visual references

Visual references are morphology inputs only. They may inform component shape, density, proportion, hierarchy rhythm, and affordance patterns; they must not override tokens, typography, domain IA, product copy, or palette composition.

## Voice And Boundaries
- brand keywords: `canvas-tool`, `creative`, `canvas`, `layer`, `inspector`, `toolbar`, `design-tool`, `vector`, `prototyping`, `whiteboard`, +2 more
- tone: `precise`, `neutral`, `matter-of-fact`, `keyboard-first`, `pixel-precise`
- visual cues: `neutral canvas surface`, `hairline borders`, `monochrome + single accent`, `thin inspector panels`, `dense layer tree`, `snap guide`, `ruler chrome`, `keyboard-first toolbar`, +3 more
- avoid: `playful`, `pastel`, `decorative`, `magazine-serif`, `marketing-heavy`, `cute`, `ornamental`, `dashboard-heavy`, +1 more

## Color Roles
| Role | Token | Value | Source | Use |
| --- | --- | --- | --- | --- |
| `primary` | `--ds-color-primary` | `#804AA8` | Cobalt Violet | 중명도, 중채도의 쿨 퍼플 톤 / 안정감, 차분함, 예술적, 신비감 |
| `accent` | `--ds-color-accent` | `#FFBF00` | Amber | 중명도, 중채도, 대중적인 옐로 오렌지 계열의 톤 / 따뜻함, 세련됨, 고급스러움, 안정감 |
| `surface_tint` | `--ds-color-surface-tint` | `#B5C7EB` | Misty Blue | 중명도, 저채도, 보라색이 섞인 뉴트럴 블루 톤 / 차분함, 사색적, 몽환적, 잔잔함, 감정의 여운 |
| `canvas` | `--ds-color-canvas` | `#F7F8FA` | Canvas White | Generated fallback support color |
| `surface` | `--ds-color-surface` | `#FFFFFF` | Paper | Generated fallback support color |
| `surface_muted` | `--ds-color-surface-muted` | `#EEF1F6` | Surface Muted | Generated fallback support color |
| `surface_elevated` | `--ds-color-surface-elevated` | `#FFFFFF` | Paper | Generated fallback support color |
| `border` | `--ds-color-border` | `#C4C3D0` | Pairing #C4C3D0 | Seed pairing support |
| `border_strong` | `--ds-color-border-strong` | `#BEB5A7` | Pairing #BEB5A7 | Seed pairing support |
| `ink` | `--ds-color-ink` | `#004E4E` | Pairing #004E4E | Seed pairing support |
| `ink_muted` | `--ds-color-ink-muted` | `#4B5563` | Muted Ink | Generated fallback support color |
| `ink_subtle` | `--ds-color-ink-subtle` | `#6A7BA2` | Pairing #6A7BA2 | Seed pairing support |
| `info` | `--ds-color-info` | `#C4C3D0` | Pairing #C4C3D0 | Seed pairing support |
| `success` | `--ds-color-success` | `#4A7C59` | Success | Generated fallback support color |
| `warning` | `--ds-color-warning` | `#FFBF00` | Amber | 중명도, 중채도, 대중적인 옐로 오렌지 계열의 톤 / 따뜻함, 세련됨, 고급스러움, 안정감 |
| `danger` | `--ds-color-danger` | `#8B2252` | Danger | Generated fallback support color |
| `link` | `--ds-color-link` | `#804AA8` | Cobalt Violet | 중명도, 중채도의 쿨 퍼플 톤 / 안정감, 차분함, 예술적, 신비감 |

Color rule: Token binding is necessary but not sufficient. Do not recombine `--ds-*` color roles into a new reference-like palette.

## Typography
| Role | Font | Token | Notes |
| --- | --- | --- | --- |
| heading | Inter | `--ds-font-heading` | geometric sans, 캔버스 도구 chrome 의 정밀한 라벨 — serif 금지 |
| body | Inter | `--ds-font-body` | inspector / layer panel 라벨, property row 본문 공용 |
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
| button | high | `default`, `hover`, `active`, `disabled`, `loading` | `primary-button`, `secondary-button`, `icon-button`, `form-actions`, `follow-button` |
| data-display | high | `default`, `sorted`, `filtered`, `empty`, `loading` | `kanban-board`, `kanban-column`, `kanban-card`, `data-table`, `column-header`, `row-actions`, +14 more |
| document | high | `default`, `selected`, `commenting`, `resolved` | `article-body`, `table-of-contents`, `heading-anchor`, `prose-block`, `reading-pane`, `footnote`, +4 more |
| feedback | high | `info`, `success`, `warning`, `danger`, `loading` | `badge`, `inline-alert`, `empty-state`, `toast`, `status-dot`, `shortcut-hint`, +5 more |
| input | high | `default`, `focus`, `error`, `disabled`, `selected` | `text-field`, `select`, `checkbox`, `switch`, `segmented-control`, `property-row`, +11 more |
| layout | high | `default`, `responsive` | `resizable-split-pane` |

## Signature Components
| Component | Family | Anatomy | Token Binding |
| --- | --- | --- | --- |
| `layer-panel` | tool-chrome | parts: container, header, content-area, footer(optional), action(optional); states: default, loading, empty, error | slots: surface, text, border, radius, padding |
| `inspector-panel` | tool-chrome | parts: container, header, content-area, footer(optional), action(optional); states: default, loading, empty, error | slots: surface, text, border, radius, padding |
| `contextual-toolbar` | tool-chrome | parts: container, header, content-area, footer(optional), action(optional); states: default, loading, empty, error | slots: surface, text, border, radius, padding |
| `layer-item` | tool-chrome | parts: container, header, content-area, footer(optional), action(optional); states: default, loading, empty, error | slots: surface, text, border, radius, padding |
| `toolbar-group` | tool-chrome | parts: container, header, content-area, footer(optional), action(optional); states: default, loading, empty, error | slots: surface, text, border, radius, padding |
| `export-panel` | tool-chrome | parts: container, header, content-area, footer(optional), action(optional); states: default, loading, empty, error | slots: surface, text, border, radius, padding |

## Advanced Component Menu
| Component | Use When | Pairs With |
| --- | --- | --- |
| `resizable-split-pane` | primary work happens between list, canvas/chat, and detail panels; users need to compare or inspect adjacent information without navigation | `thread-list`, `artifact-preview-panel`, `inspector-drawer` |
| `inspector-drawer` | a selected item needs rich detail without leaving the main workflow; users need source facts, owners, versions, or retention metadata | `policy-matrix`, `citation-drawer`, `decision-record-card` |
| `bulk-action-table` | users handle many records at once; selection count and destructive actions must stay visible | `saved-view-bar`, `filter-builder`, `exception-queue` |
| `evidence-graph` | trust depends on seeing relationships between claims and sources; auditors need to trace why an answer or decision was made | `citation-drawer`, `decision-record-card`, `policy-matrix` |
| `policy-matrix` | multiple policy rules must be checked against multiple claims or fields; reviewers need dense scan-and-drill compliance status | `risk-summary-card`, `exception-queue`, `approval-rail` |
| `redline-viewer` | legal, compliance, or editorial text needs reviewer markup; comments must stay anchored to exact text ranges | `diff-viewer`, `comment-thread`, `approval-rail` |

Use these as ontology-approved building blocks when the workflow calls for richer professional UI. They still inherit token, typography, accessibility, and reference-governance rules.

## Design Context Pack
- activation: `planned`
- providers: `pinterest`=preview, `lazyweb`=suggested
- flow coverage: general-product-ui(covered), document(covered), data-review(gap), navigation(gap)
| Context | Provider | Allowed Use |
| --- | --- | --- |
| figma canvas inspector layer panel | `lazyweb` | morphology: `card-stack`, `split-pane`; flows: `general-product-ui` |
| framer canvas tool | `lazyweb` | morphology: `general-interface-composition`; flows: `general-product-ui` |
| excalidraw whiteboard | `lazyweb` | morphology: `general-interface-composition`; flows: `general-product-ui` |
| tldraw canvas | `lazyweb` | morphology: `general-interface-composition`; flows: `general-product-ui` |
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
