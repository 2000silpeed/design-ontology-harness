# Pulse System Style Capsule

- preset: `monitoring-ops--minimal-tech`
- brand: Pulse
- mode: `monitoring-ops` / `minimal-tech`
- capsule_version: `1.0.0`
- companion files: `STYLE.md` is the human brief; `DESIGN.md` is the agent-ready copy.

## Taste Summary
SRE/DevOps 실시간 observability 콘솔 — metric/alert/trace, 다크 기본, 한국어 1급.

## Authority Order
1. Product task flow and information architecture
2. `token_schema.json` and generated CSS variables
3. `components/component_specs.*` and `component_inventory.json`
4. `system_spec.md` and `system_ontology.json`
5. External visual references

Visual references are morphology inputs only. They may inform component shape, density, proportion, hierarchy rhythm, and affordance patterns; they must not override tokens, typography, domain IA, product copy, or palette composition.

## Voice And Boundaries
- brand keywords: `sre`, `devops`, `observability`, `monitoring`, `realtime`, `operations`, `alerting`, `metric`, `incident`
- tone: `precise`, `operational`, `matter-of-fact`, `calm-under-pressure`
- visual cues: `dense chart grid`, `status board`, `high-density table`, `alert-first hierarchy`, `cool neutral surfaces`, `hairline borders`, `monochrome + single accent`, `numeric emphasis`
- avoid: `playful`, `decorative`, `marketing-heavy`, `skeuomorphic`, `ornamental`

## Color Roles
| Role | Token | Value | Source | Use |
| --- | --- | --- | --- | --- |
| `primary` | `--ds-color-primary` | `#007FFF` | Azure Blue | 고명도, 고채도, 쿨톤의 청량한 블루 / 개방감, 에너지, 명료함, 신선함, 혁신 |
| `accent` | `--ds-color-accent` | `#50C878` | Emerald Green | 중명도, 중채도의 대중적인 청록 계열 / 고급스러움, 생명력, 세련된 안정감, 청량한 자연성 |
| `surface_tint` | `--ds-color-surface-tint` | `#D6EAF8` | Ice Blue | 고명도, 저채도, 밝고 청량한 블루 계열 / 정제됨, 청결함, 섬세함, 평온, 투명 |
| `canvas` | `--ds-color-canvas` | `#FFFFFF` | Pairing #FFFFFF | Seed pairing support |
| `surface` | `--ds-color-surface` | `#FFFFFF` | Pairing #FFFFFF | Seed pairing support |
| `surface_muted` | `--ds-color-surface-muted` | `#EEF1F6` | Surface Muted | Generated fallback support color |
| `surface_elevated` | `--ds-color-surface-elevated` | `#FFFFFF` | Pairing #FFFFFF | Seed pairing support |
| `border` | `--ds-color-border` | `#D6DDE6` | Border Neutral | Generated fallback support color |
| `border_strong` | `--ds-color-border-strong` | `#C0C0C0` | Pairing #C0C0C0 | Seed pairing support |
| `ink` | `--ds-color-ink` | `#1A2E45` | Pairing #1A2E45 | Seed pairing support |
| `ink_muted` | `--ds-color-ink-muted` | `#444C57` | Pairing #444C57 | Seed pairing support |
| `ink_subtle` | `--ds-color-ink-subtle` | `#6B7280` | Subtle Ink | Generated fallback support color |
| `info` | `--ds-color-info` | `#444C57` | Pairing #444C57 | Seed pairing support |
| `success` | `--ds-color-success` | `#50C878` | Emerald Green | 중명도, 중채도의 대중적인 청록 계열 / 고급스러움, 생명력, 세련된 안정감, 청량한 자연성 |
| `warning` | `--ds-color-warning` | `#F8F8F4` | Pairing #F8F8F4 | Seed pairing support |
| `danger` | `--ds-color-danger` | `#8B2252` | Danger | Generated fallback support color |
| `link` | `--ds-color-link` | `#007FFF` | Azure Blue | 고명도, 고채도, 쿨톤의 청량한 블루 / 개방감, 에너지, 명료함, 신선함, 혁신 |

Color rule: Token binding is necessary but not sufficient. Do not recombine `--ds-*` color roles into a new reference-like palette.

## Typography
| Role | Font | Token | Notes |
| --- | --- | --- | --- |
| heading | Inter | `--ds-font-heading` | geometric sans, 숫자/영문 가독성 |
| body | Inter | `--ds-font-body` | UI 라벨/본문 공용 |
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
- corner bias: `medium`

## Component Priorities
| Family | Priority | States | Components |
| --- | --- | --- | --- |
| button | high | `default`, `hover`, `active`, `disabled`, `loading` | `primary-button`, `secondary-button`, `icon-button`, `form-actions` |
| copilot-chat | high | `default`, `loading`, `complete`, `error` | `tool-call-trace` |
| data-display | high | `default`, `sorted`, `filtered`, `empty`, `loading` | `metric-strip`, `status-summary-row`, `task-surface-header`, `source-ledger`, `section-header`, `chart-container`, +19 more |
| feedback | high | `info`, `success`, `warning`, `danger`, `loading` | `badge`, `inline-alert`, `empty-state`, `toast`, `status-dot`, `banner`, +3 more |
| input | high | `default`, `focus`, `error`, `disabled`, `selected` | `text-field`, `select`, `checkbox`, `switch`, `segmented-control`, `filter-chip`, +11 more |
| navigation | high | `default`, `active`, `hover`, `collapsed` | `breadcrumbs`, `tabs`, `pagination`, `operational-rail`, `app-shell`, `sidebar-nav`, +6 more |

## Signature Components
| Component | Family | Anatomy | Token Binding |
| --- | --- | --- | --- |
| `ticket-queue` | dashboard-growth | parts: container, header, content-area, footer(optional), action(optional); states: default, loading, empty, error | slots: surface, text, border, radius, padding |
| `alert-list` | dashboard-growth | parts: container, header, content-area, footer(optional), action(optional); states: default, loading, empty, error | slots: surface, text, border, radius, padding |
| `metric-strip` | data-display | parts: container, header, content-area, footer(optional), action(optional); states: default, loading, empty, error | slots: surface, text, border, radius, padding |
| `status-summary-row` | data-display | parts: container, header, content-area, footer(optional), action(optional); states: default, loading, empty, error | slots: surface, text, border, radius, padding |
| `chart-container` | data-display | parts: container, header, content-area, footer(optional), action(optional); states: default, loading, empty, error | slots: surface, text, border, radius, padding |
| `chart-tooltip` | overlay | parts: backdrop, container, header, content, footer(optional), +1 more; states: closed, opening, open, closing | slots: surface, border, radius, padding |

## Advanced Component Menu
| Component | Use When | Pairs With |
| --- | --- | --- |
| `saved-view-bar` | teams revisit the same filtered views often; dense tools need stable scope memory | `filter-builder`, `bulk-action-table`, `exception-queue` |
| `audit-timeline` | regulated workflows require traceable user and AI actions; reviewers need to reconstruct what happened before approval | `decision-record-card`, `approval-rail`, `tool-call-trace` |
| `command-palette` | the product has many actions or navigation targets; expert users benefit from quick action search | `shortcut-hint`, `saved-view-bar`, `filter-builder` |
| `evidence-graph` | trust depends on seeing relationships between claims and sources; auditors need to trace why an answer or decision was made | `citation-drawer`, `decision-record-card`, `policy-matrix` |
| `filter-builder` | users need AND/OR logic across several fields; filters should be saved, shared, or audited | `saved-view-bar`, `bulk-action-table`, `exception-queue` |
| `tool-call-trace` | AI actions need explainability or debugging; operators need to audit retrieval, policy checks, or workflow calls | `audit-timeline`, `citation-drawer`, `decision-record-card` |
| `bulk-action-table` | users handle many records at once; selection count and destructive actions must stay visible | `saved-view-bar`, `filter-builder`, `exception-queue` |
| `confidence-meter` | AI or policy outcome includes uncertainty; users must decide whether to trust, edit, or escalate | `risk-summary-card`, `policy-matrix`, `tool-call-trace` |

Use these as ontology-approved building blocks when the workflow calls for richer professional UI. They still inherit token, typography, accessibility, and reference-governance rules.

## Design Context Pack
- activation: `planned`
- providers: `pinterest`=preview, `lazyweb`=suggested
- flow coverage: dashboard(covered), general-product-ui(covered), data-review(gap), document(gap), navigation(gap)
| Context | Provider | Allowed Use |
| --- | --- | --- |
| grafana dashboard dark | `lazyweb` | morphology: `general-interface-composition`; flows: `dashboard` |
| datadog monitoring console | `lazyweb` | morphology: `general-interface-composition`; flows: `dashboard` |
| honeycomb observability traces | `lazyweb` | morphology: `general-interface-composition`; flows: `general-product-ui` |
| prometheus alert list | `lazyweb` | morphology: `general-interface-composition`; flows: `general-product-ui` |
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
