# Meadow System Style Capsule

- preset: `dashboard--playful-soft`
- brand: Meadow
- mode: `dashboard` / `playful-soft`
- capsule_version: `1.0.0`
- companion files: `STYLE.md` is the human brief; `DESIGN.md` is the agent-ready copy.

## Taste Summary
consumer wellness/habit admin — playful-soft 톤 pastel 팔레트, 한국어 1급.

## Authority Order
1. Product task flow and information architecture
2. `token_schema.json` and generated CSS variables
3. `components/component_specs.*` and `component_inventory.json`
4. `system_spec.md` and `system_ontology.json`
5. External visual references

Visual references are morphology inputs only. They may inform component shape, density, proportion, hierarchy rhythm, and affordance patterns; they must not override tokens, typography, domain IA, product copy, or palette composition.

## Voice And Boundaries
- brand keywords: `dashboard`, `admin`, `consumer`, `wellness`, `habit`, `tracking`, `mindful`, `calm`, `soft`, `rounded`, +5 more
- tone: `friendly`, `warm`, `encouraging`, `gentle`, `approachable`, `mindful`
- visual cues: `rounded corners`, `pastel surfaces`, `soft shadow`, `gentle card`, `warm periwinkle primary`, `peach puff accent`, `mauve dreamy surface`, `habit streak flame`, +3 more
- avoid: `minimal-tech-cool`, `corporate-navy`, `bold-saturated`, `magazine-serif`, `high-contrast`, `dense-only`, `enterprise-sharp`

## Color Roles
| Role | Token | Value | Source | Use |
| --- | --- | --- | --- | --- |
| `primary` | `--ds-color-primary` | `#8E9AF1` | Periwinkle | 중명도, 저채도, 푸른빛이 감도는 웜 퍼플 톤 / 부드러움, 몽환, 순수함, 세련된 차분함 |
| `accent` | `--ds-color-accent` | `#FFDAB9` | Peach Puff | 고명도, 저채도, 오렌지와 핑크 사이의 파스텔 계열 / 따뜻함, 부드러움, 순수함, 친근함, 생기 |
| `surface_tint` | `--ds-color-surface-tint` | `#E0B0FF` | Mauve | 중명도, 저채도, 웜과 쿨 중간 베이스 퍼플 톤 / 낭만적, 세련됨, 회상적, 빈티지 무드 |
| `canvas` | `--ds-color-canvas` | `#F7F8FA` | Canvas White | Generated fallback support color |
| `surface` | `--ds-color-surface` | `#FFFFFF` | Paper | Generated fallback support color |
| `surface_muted` | `--ds-color-surface-muted` | `#EEF1F6` | Surface Muted | Generated fallback support color |
| `surface_elevated` | `--ds-color-surface-elevated` | `#FFFFFF` | Paper | Generated fallback support color |
| `border` | `--ds-color-border` | `#D6DDE6` | Border Neutral | Generated fallback support color |
| `border_strong` | `--ds-color-border-strong` | `#B0BAC7` | Border Strong | Generated fallback support color |
| `ink` | `--ds-color-ink` | `#111111` | Ink | Generated fallback support color |
| `ink_muted` | `--ds-color-ink-muted` | `#4B5563` | Muted Ink | Generated fallback support color |
| `ink_subtle` | `--ds-color-ink-subtle` | `#6B7280` | Subtle Ink | Generated fallback support color |
| `info` | `--ds-color-info` | `#8E9AF1` | Periwinkle | 중명도, 저채도, 푸른빛이 감도는 웜 퍼플 톤 / 부드러움, 몽환, 순수함, 세련된 차분함 |
| `success` | `--ds-color-success` | `#4A7C59` | Success | Generated fallback support color |
| `warning` | `--ds-color-warning` | `#FFDAB9` | Peach Puff | 고명도, 저채도, 오렌지와 핑크 사이의 파스텔 계열 / 따뜻함, 부드러움, 순수함, 친근함, 생기 |
| `danger` | `--ds-color-danger` | `#FA8072` | Salmon | 밝고 따뜻한 핑크 오렌지 톤 / 따뜻함, 부드러움, 친근함, 자연스러움 |
| `link` | `--ds-color-link` | `#8E9AF1` | Periwinkle | 중명도, 저채도, 푸른빛이 감도는 웜 퍼플 톤 / 부드러움, 몽환, 순수함, 세련된 차분함 |

Color rule: Token binding is necessary but not sufficient. Do not recombine `--ds-*` color roles into a new reference-like palette.

## Typography
| Role | Font | Token | Notes |
| --- | --- | --- | --- |
| heading | Nunito | `--ds-font-heading` | rounded sans, playful-soft 시각 성격 핵심 — workspace-header / section-header / kpi-card label / insigh... |
| body | Inter | `--ds-font-body` | data-table cell / filter-chip / activity feed / mood-check 공용 본문, line-height 1.5–1.6 (dashboard... |
| mono | JetBrains Mono | `--ds-font-mono` | data, code, shortcuts only |
| korean | Pretendard | `--ds-font-ko` | primary script support |

- type scale: `xs`=11, `sm`=12, `md`=14, `lg`=17, `xl`=20, `2xl`=24, `3xl`=29
- line heights: `tight`=1.25, `normal`=1.4, `comfortable`=1.5, `relaxed`=1.6
- headline wrap: `word_break`=keep-all, `overflow_wrap`=normal, `text_wrap`=balance
- body wrap: `word_break`=keep-all, `overflow_wrap`=normal

## Spacing And Shape
- spacing scale: `0`, `2`, `4`, `8`, `12`, `16`, `24`, `32`, `48`, `64`, `96`
- density bias: `dense`
- radius scale: `none`, `sm`, `md`, `lg`, `xl`, `pill`
- corner bias: `round`

## Component Priorities
| Family | Priority | States | Components |
| --- | --- | --- | --- |
| button | high | `default`, `hover`, `active`, `disabled`, `loading` | `primary-button`, `secondary-button`, `icon-button`, `form-actions`, `follow-button`, `hero-cta-group` |
| data-display | high | `default`, `sorted`, `filtered`, `empty`, `loading` | `metric-strip`, `status-summary-row`, `task-surface-header`, `source-ledger`, `section-header`, `data-table`, +22 more |
| editorial | high | `default`, `selected`, `editing` | `editor-canvas`, `editor-toolbar`, `inline-format-menu`, `slash-command-menu`, `block-controls` |
| feedback | high | `info`, `success`, `warning`, `danger`, `loading` | `badge`, `inline-alert`, `empty-state`, `toast`, `status-dot`, `status-badge`, +6 more |
| input | high | `default`, `focus`, `error`, `disabled`, `selected` | `text-field`, `select`, `checkbox`, `switch`, `segmented-control`, `filter-chip`, +14 more |
| layout | high | `default`, `responsive` | `resizable-split-pane` |

## Signature Components
| Component | Family | Anatomy | Token Binding |
| --- | --- | --- | --- |
| `dashboard-card` | dashboard-wellness | parts: container, inner-content; states: default, hover, focus-visible | slots: surface, border, radius, padding |
| `mood-chart` | dashboard-wellness | parts: container, header, content-area, footer(optional), action(optional); states: default, loading, empty, error | slots: surface, text, border, radius, padding |
| `goal-grid` | dashboard-wellness | parts: grid-container; states: default | read component spec |
| `experiment-panel` | dashboard-growth | parts: container, header, content-area, footer(optional), action(optional); states: default, loading, empty, error | slots: surface, text, border, radius, padding |
| `streak-indicator` | dashboard-wellness | parts: container, header, content-area, footer(optional), action(optional); states: default, loading, empty, error | slots: surface, text, border, radius, padding |
| `habit-calendar` | dashboard-wellness | parts: container, header, content-area, footer(optional), action(optional); states: default, loading, empty, error | slots: surface, text, border, radius, padding |

## Advanced Component Menu
| Component | Use When | Pairs With |
| --- | --- | --- |
| `bulk-action-table` | users handle many records at once; selection count and destructive actions must stay visible | `saved-view-bar`, `filter-builder`, `exception-queue` |
| `filter-builder` | users need AND/OR logic across several fields; filters should be saved, shared, or audited | `saved-view-bar`, `bulk-action-table`, `exception-queue` |
| `resizable-split-pane` | primary work happens between list, canvas/chat, and detail panels; users need to compare or inspect adjacent information without navigation | `thread-list`, `artifact-preview-panel`, `inspector-drawer` |
| `saved-view-bar` | teams revisit the same filtered views often; dense tools need stable scope memory | `filter-builder`, `bulk-action-table`, `exception-queue` |
| `audit-timeline` | regulated workflows require traceable user and AI actions; reviewers need to reconstruct what happened before approval | `decision-record-card`, `approval-rail`, `tool-call-trace` |
| `confidence-meter` | AI or policy outcome includes uncertainty; users must decide whether to trust, edit, or escalate | `risk-summary-card`, `policy-matrix`, `tool-call-trace` |
| `decision-record-card` | a reviewer or AI-assisted workflow reaches a durable decision; regulated teams need record ids and retention status | `audit-timeline`, `approval-rail`, `citation-drawer` |
| `exception-queue` | multiple issues require triage, assignment, and resolution; reviewers need to batch handle exceptions | `bulk-action-table`, `policy-matrix`, `approval-rail` |

Use these as ontology-approved building blocks when the workflow calls for richer professional UI. They still inherit token, typography, accessibility, and reference-governance rules.

## Design Context Pack
- activation: `planned`
- providers: `pinterest`=preview, `lazyweb`=suggested
- flow coverage: dashboard(covered), general-product-ui(covered), settings(covered), data-review(gap), navigation(gap)
| Context | Provider | Allowed Use |
| --- | --- | --- |
| cal.com booking dashboard | `lazyweb` | morphology: `general-interface-composition`; flows: `dashboard` |
| notion habit tracker | `lazyweb` | morphology: `general-interface-composition`; flows: `general-product-ui` |
| flo wellness dashboard | `lazyweb` | morphology: `general-interface-composition`; flows: `dashboard` |
| finch self care dashboard | `lazyweb` | morphology: `general-interface-composition`; flows: `dashboard` |
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
