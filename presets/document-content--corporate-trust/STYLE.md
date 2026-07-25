# EKOS Knowledge Intake Design System Style Capsule

- preset: `document-content--corporate-trust`
- brand: EKOS Knowledge Intake
- mode: `document-content` / `corporate-trust`
- capsule_version: `1.0.0`
- companion files: `STYLE.md` is the human brief; `DESIGN.md` is the agent-ready copy.

## Taste Summary
EKOS Knowledge Intake — 온톨로지 어휘를 번역한 업무 문장 중심의 지식 등록·검토 워크벤치 (Prussian/Ocean/Cornsilk 아카이브 톤).

## Authority Order
1. Product task flow and information architecture
2. `token_schema.json` and generated CSS variables
3. `components/component_specs.*` and `component_inventory.json`
4. `system_spec.md` and `system_ontology.json`
5. External visual references

Visual references are morphology inputs only. They may inform component shape, density, proportion, hierarchy rhythm, and affordance patterns; they must not override tokens, typography, domain IA, product copy, or palette composition.

## Voice And Boundaries
- brand keywords: `archive`, `evidence-first`, `sentence-first`, `trustworthy`, `calm`, `editorial-operational`, `reviewable`, `korean-first`
- tone: `업무 문장으로 말한다 (기술 어휘 번역)`, `행동의 결과와 영향 범위를 미리 알려준다`, `실패를 숨기지 않고 복구 행동과 함께 보여준다`, `차분하고 사무적이되 딱딱하지 않다`
- visual cues: `prussian blue archive authority`, `cornsilk warm paper surfaces flattened for reading`, `ocean blue trust accents for focus and links`, `hunter green success, goldenrod warning, marsala failure`, `rust as rare editorial emphasis only`, `sentence-first fact rows with status tags`, `split review workbench with evidence panel`, `long-form korean text at comfortable measure`, +2 more
- avoid: `graph-tech jargon`, `decorative node graph`, `sci-fi glow`, `generic dashboard metric cards`, `numeric-score-only ranking`, `spinner-only progress`, `marketing hero`, `paper texture over legibility`

## Color Roles
| Role | Token | Value | Source | Use |
| --- | --- | --- | --- | --- |
| `primary` | `--ds-color-primary` | `#003153` | Prussian Blue | 저명도, 저채도, 녹색 기가 약하게 섞인 중성 쿨톤 / 고전, 예술, 집중, 권위, 깊이감 |
| `accent` | `--ds-color-accent` | `#B7410E` | Rust | 저명도, 중채도, 오렌지와 브라운의 중간 영역 / 빈티지, 견고함, 따뜻한 노스탤지어, 공예적 감성 |
| `surface_tint` | `--ds-color-surface-tint` | `#FFF8DC` | Cornsilk | 고명도, 저채도, 크리미한 옐로 베이스 계열의 톤 / 따뜻함, 부드러움, 내추럴함, 포근함 |
| `canvas` | `--ds-color-canvas` | `#F7F8FA` | Canvas | typed runtime fallback |
| `surface` | `--ds-color-surface` | `#FFFFFF` | Surface | typed runtime fallback |
| `surface_muted` | `--ds-color-surface-muted` | `#EEF1F6` | Surface Muted | typed runtime fallback |
| `surface_elevated` | `--ds-color-surface-elevated` | `#FFFFFF` | Surface | typed runtime fallback |
| `border` | `--ds-color-border` | `#D6DDE6` | Border | typed runtime fallback |
| `border_strong` | `--ds-color-border-strong` | `#9AA6B2` | Border Strong | typed runtime fallback |
| `ink` | `--ds-color-ink` | `#003153` | Prussian Blue | 저명도, 저채도, 녹색 기가 약하게 섞인 중성 쿨톤 / 고전, 예술, 집중, 권위, 깊이감 |
| `ink_muted` | `--ds-color-ink-muted` | `#475569` | Ink Muted | typed runtime fallback |
| `ink_subtle` | `--ds-color-ink-subtle` | `#64748B` | Ink Subtle | typed runtime fallback |
| `info` | `--ds-color-info` | `#4F97A3` | Ocean Blue | 중명도, 중채도, 매트한 청록색 계열 / 신뢰, 정화, 깊이감, 유연함, 안정감 |
| `success` | `--ds-color-success` | `#355E3B` | Hunter Green | 저명도, 중고채도의 다크 그린 계열 / 중후함, 신뢰, 클래식, 깊이감, 균형감 |
| `warning` | `--ds-color-warning` | `#DAA520` | Goldenrod | 중명도, 중채도, 옐로 오렌지 계열 / 따뜻함, 안정감, 고급스러움, 빈티지 감성 |
| `danger` | `--ds-color-danger` | `#964F4C` | Marsala | 적갈색 계열, 와인과 브라운 사이의 중후한 톤 / 성숙함, 안정감, 관능적, 가을/겨울, 클래식 |
| `link` | `--ds-color-link` | `#4F97A3` | Ocean Blue | 중명도, 중채도, 매트한 청록색 계열 / 신뢰, 정화, 깊이감, 유연함, 안정감 |

Color rule: Token binding is necessary but not sufficient. Do not recombine `--ds-*` color roles into a new reference-like palette.

## Typography
| Role | Font | Token | Notes |
| --- | --- | --- | --- |
| heading | Pretendard | `--ds-font-heading` | 한글 UI 서체의 사실상 표준. Apple SD Gothic Neo 기반이지만 더 정교함. 라틴은 Inter 계열. |
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
- corner bias: `medium`

## Component Priorities
| Family | Priority | States | Components |
| --- | --- | --- | --- |
| navigation | high | `default`, `active`, `hover`, `collapsed` | `left-nav`, `workspace-topbar` |
| approval | medium | `default` | `review-action-bar` |
| concept-proposal | medium | `default` | `new-concept-form` |
| evidence | medium | `default` | `evidence-panel` |
| fact-review | medium | `default` | `fact-list-row`, `fact-status-tag`, `fact-sentence-editor`, `relation-candidate-card` |
| feedback-and-empty-states | medium | `default` | `empty-state-guide` |

## Signature Components
| Component | Family | Anatomy | Token Binding |
| --- | --- | --- | --- |
| `left-nav` | navigation | parts: nav-rail, nav-item, nav-label, active-indicator; states: default, active, keyboard-focus, collapsed | read component spec |
| `global-search-input` | search | parts: input-field, placeholder, search-icon, results-popover; states: empty, typing, results, no-results, keyboard-f... | read component spec |
| `upload-manifest-card` | intake-input | parts: file-meta, trust-notice, progress-line, action-row; states: pending, uploading, uploaded, sensitive-quarantine... | read component spec |
| `analysis-failure-panel` | progress-and-failure | parts: failure-list, recovery-actions, technical-details; states: partial-failure, full-failure, retrying, details-ex... | read component spec |
| `fact-status-tag` | fact-review | parts: tag-icon, tag-label; states: ready, needs-choice, new-concept, conflict, excluded | read component spec |
| `relation-candidate-card` | fact-review | parts: candidate-sentence, reason-line, select-control; states: default, selected, keyboard-focus, insufficient-evidence | read component spec |

## Advanced Component Menu
- No advanced recommendations for this preset. Read `component_inventory.json` before adding one.

## Design Context Pack
- activation: `planned`
- providers: `pinterest`=preview, `lazyweb`=suggested
- flow coverage: data-review(covered), document(covered), general-product-ui(covered), empty-state(gap), navigation(gap)
| Context | Provider | Allowed Use |
| --- | --- | --- |
| split review workbench with fact list and detail editor | `lazyweb` | morphology: `split-pane`; flows: `data-review`, `document` |
| evidence panel with source excerpt comparison | `lazyweb` | morphology: `evidence`, `card-stack`; flows: `data-review` |
| korean enterprise knowledge intake form calm archive tone | `lazyweb` | morphology: `general-interface-composition`; flows: `general-product-ui` |
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
