# Signal System Style Capsule

- preset: `document-content--editorial-warm`
- brand: Signal Desk
- mode: `document-content` / `editorial-warm`
- capsule_version: `1.0.0`
- companion files: `STYLE.md` is the human brief; `DESIGN.md` is the agent-ready copy.

## Taste Summary
작은 팀·제작자용 에디토리얼 워크스페이스 — 문서/콘텐츠 reading flow, split-pane, warm serif 페어링.

## Authority Order
1. Product task flow and information architecture
2. `token_schema.json` and generated CSS variables
3. `components/component_specs.*` and `component_inventory.json`
4. `system_spec.md` and `system_ontology.json`
5. External visual references

Visual references are morphology inputs only. They may inform component shape, density, proportion, hierarchy rhythm, and affordance patterns; they must not override tokens, typography, domain IA, product copy, or palette composition.

## Voice And Boundaries
- brand keywords: `calm`, `precise`, `editorial`, `trustworthy`
- tone: `clear`, `warm`, `confident`
- visual cues: `structured whitespace`, `measured contrast`, `text-first hierarchy`
- avoid: `generic`, `noisy`, `overdecorated`, `playful`

## Color Roles
| Role | Token | Value | Source | Use |
| --- | --- | --- | --- | --- |
| `canvas` | `--ds-color-canvas` | `#F7F8FA` | Canvas White | Generated fallback support color |
| `surface` | `--ds-color-surface` | `#FFFFFF` | Paper | Generated fallback support color |
| `surface_muted` | `--ds-color-surface-muted` | `#EEF1F6` | Surface Muted | Generated fallback support color |
| `surface_elevated` | `--ds-color-surface-elevated` | `#FFFFFF` | Paper | Generated fallback support color |
| `border` | `--ds-color-border` | `#D6DDE6` | Border Neutral | Generated fallback support color |
| `border_strong` | `--ds-color-border-strong` | `#B0BAC7` | Border Strong | Generated fallback support color |
| `ink` | `--ds-color-ink` | `#003153` | Prussian Blue | 고전, 예술, 집중, 권위, 깊이감 |
| `ink_muted` | `--ds-color-ink-muted` | `#4B5563` | Muted Ink | Generated fallback support color |
| `ink_subtle` | `--ds-color-ink-subtle` | `#6B7280` | Subtle Ink | Generated fallback support color |
| `info` | `--ds-color-info` | `#967BB6` | Lavender Violet | 고명도, 중저채도, 베이직 퍼플 계열 / 부드러움, 평온함, 세련, 낭만, 안정감 |
| `success` | `--ds-color-success` | `#27503D` | Forest Green | 저명도, 고채도의 딥 그린 계열 / 묵직함, 안정감, 신뢰, 자연적 깊이 |
| `warning` | `--ds-color-warning` | `#F5DEB3` | Wheat | 중명도, 저채도, 베이지 옐로 계열의 따뜻한 톤 / 따뜻함, 자연스러움, 부드러움, 안정감 |
| `danger` | `--ds-color-danger` | `#E2725B` | Terracotta | 붉은 흙빛 계열, 오렌지 브라운이 섞인 따뜻한 중채 레드 / 안정감, 따뜻함, 자연스러움, 감성적 |
| `anchor_background` | `--ds-color-anchor-background` | `#000080` | Navy Blue | 신뢰, 권위, 집중, 전문성, 절제된 우아함 |

Color rule: Token binding is necessary but not sufficient. Do not recombine `--ds-*` color roles into a new reference-like palette.

## Typography
| Role | Font | Token | Notes |
| --- | --- | --- | --- |
| heading | Noto Serif KR | `--ds-font-heading` | 한글 세리프의 사실상 유일한 고품질 웹폰트. 에디토리얼 한글에 필수. |
| body | Pretendard | `--ds-font-body` | 한글 UI 서체의 사실상 표준. Apple SD Gothic Neo 기반이지만 더 정교함. 라틴은 Inter 계열. |
| mono | Source Code Pro | `--ds-font-mono` | data, code, shortcuts only |
| korean | Pretendard | `--ds-font-ko` | primary script support |

- type scale: `xs`=12, `sm`=14, `md`=16, `lg`=21, `xl`=28, `2xl`=38, `3xl`=50
- line heights: `tight`=1.2, `normal`=1.5, `comfortable`=1.6, `relaxed`=1.75
- headline wrap: `word_break`=keep-all, `overflow_wrap`=normal, `text_wrap`=balance
- body wrap: `word_break`=keep-all, `overflow_wrap`=normal

## Spacing And Shape
- spacing scale: `0`, `2`, `4`, `8`, `12`, `16`, `24`, `32`, `48`, `64`, `96`
- density bias: `airy`
- radius scale: `none`, `sm`, `md`, `lg`, `xl`, `pill`
- corner bias: `pill`

## Component Priorities
| Family | Priority | States | Components |
| --- | --- | --- | --- |
| button | high | `default`, `hover`, `active`, `disabled`, `loading` | `primary-button`, `secondary-button`, `icon-button`, `form-actions`, `hero-cta-group`, `cta-button-group`, +2 more |
| data-display | high | `default`, `sorted`, `filtered`, `empty`, `loading` | `data-table`, `list`, `metadata-list`, `column-header`, `row-actions`, `kanban-board`, +27 more |
| editorial | high | `default`, `selected`, `editing` | `editor-canvas`, `editor-toolbar`, `slash-command-menu`, `block-controls`, `inline-format-menu`, `content-card`, +7 more |
| feedback | high | `info`, `success`, `warning`, `danger`, `loading` | `filter-chip`, `badge`, `inline-alert`, `empty-state`, `toast`, `status-dot`, +7 more |
| input | high | `default`, `focus`, `error`, `disabled`, `selected` | `text-field`, `select`, `checkbox`, `switch`, `segmented-control`, `textarea`, +12 more |
| layout | high | `default`, `responsive` | `resizable-split-pane` |

## Signature Components
| Component | Family | Anatomy | Token Binding |
| --- | --- | --- | --- |
| `cta-headline` | marketing | parts: heading-text; states: default | slots: font |
| `autocomplete` | overlay | parts: backdrop, container, header, content, footer(optional), +1 more; states: closed, opening, open, closing | slots: surface, border, radius, padding |
| `hero-headline` | marketing | parts: heading-text; states: default | slots: font |
| `feature-title` | marketing | parts: heading-text; states: default | slots: font |
| `form-actions` | button | parts: container, label, leading-icon(optional), trailing-icon(optional); states: default, hover, active, disabled, l... | slots: surface, text, border, radius, padding, font |
| `data-table` | data-display | parts: container, header, content-area, footer(optional), action(optional); states: default, loading, empty, error | slots: surface, text, border, radius, padding |

## Advanced Component Menu
| Component | Use When | Pairs With |
| --- | --- | --- |
| `bulk-action-table` | users handle many records at once; selection count and destructive actions must stay visible | `saved-view-bar`, `filter-builder`, `exception-queue` |
| `exception-queue` | multiple issues require triage, assignment, and resolution; reviewers need to batch handle exceptions | `bulk-action-table`, `policy-matrix`, `approval-rail` |
| `filter-builder` | users need AND/OR logic across several fields; filters should be saved, shared, or audited | `saved-view-bar`, `bulk-action-table`, `exception-queue` |
| `resizable-split-pane` | primary work happens between list, canvas/chat, and detail panels; users need to compare or inspect adjacent information without navigation | `thread-list`, `artifact-preview-panel`, `inspector-drawer` |
| `risk-summary-card` | users need a fast read of risk before drilling into policy details; AI confidence or compliance severity must be visible | `policy-matrix`, `confidence-meter`, `exception-queue` |
| `saved-view-bar` | teams revisit the same filtered views often; dense tools need stable scope memory | `filter-builder`, `bulk-action-table`, `exception-queue` |
| `approval-rail` | work requires review, approval, rejection, or handoff; users need to know who owns the next decision | `policy-matrix`, `risk-summary-card`, `diff-viewer` |
| `audit-timeline` | regulated workflows require traceable user and AI actions; reviewers need to reconstruct what happened before approval | `decision-record-card`, `approval-rail`, `tool-call-trace` |

Use these as ontology-approved building blocks when the workflow calls for richer professional UI. They still inherit token, typography, accessibility, and reference-governance rules.

## Design Context Pack
- activation: `grounded`
- providers: `local-images`=active, `pinterest`=active, `lazyweb`=suggested
- flow coverage: dashboard(covered), general-product-ui(covered), onboarding(covered), data-review(gap), document(gap), navigation(gap)
| Context | Provider | Allowed Use |
| --- | --- | --- |
| editorial-dashboard-split-pane | `local-images` | morphology: `split-pane`; flows: `dashboard` |
| landing-hero-serif-trust-strip | `local-images` | morphology: `split-pane`; flows: `dashboard` |
| editorial dashboard ui | `lazyweb` | morphology: `general-interface-composition`; flows: `dashboard` |
| warm premium onboarding flow | `lazyweb` | morphology: `general-interface-composition`; flows: `onboarding` |
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
