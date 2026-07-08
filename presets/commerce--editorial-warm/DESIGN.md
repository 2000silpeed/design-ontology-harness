# ColorFit System Style Capsule

- preset: `commerce--editorial-warm`
- brand: ColorFit
- mode: `commerce` / `editorial-warm`
- capsule_version: `1.0.0`
- companion files: `STYLE.md` is the human brief; `DESIGN.md` is the agent-ready copy.

## Taste Summary
퍼스널컬러 기반 모바일 패션 커머스 — 에디토리얼 웜 톤, 코디/가격 비교 UX.

## Authority Order
1. Product task flow and information architecture
2. `token_schema.json` and generated CSS variables
3. `components/component_specs.*` and `component_inventory.json`
4. `system_spec.md` and `system_ontology.json`
5. External visual references

Visual references are morphology inputs only. They may inform component shape, density, proportion, hierarchy rhythm, and affordance patterns; they must not override tokens, typography, domain IA, product copy, or palette composition.

## Voice And Boundaries
- brand keywords: `editorial`, `precise`, `trustworthy`, `warm`
- tone: `clear`, `reassuring`, `curated`, `confident`
- visual cues: `warm neutrals`, `serif-sans contrast`, `measured whitespace`, `fashion editorial hierarchy`, `tonal accent cues`
- avoid: `generic`, `noisy`, `clinical`, `cheap`

## Color Roles
| Role | Token | Value | Source | Use |
| --- | --- | --- | --- | --- |
| `anchor_background` | `--ds-color-anchor-background` | `#000080` | Navy Blue | 신뢰, 권위, 집중, 전문성, 절제된 우아함 |
| `depth_support` | `--ds-color-depth-support` | `#003153` | Prussian Blue | 고전, 예술, 집중, 권위, 깊이감 |
| `interface_surface` | `--ds-color-interface-surface` | `#0F4C81` | Classic Blue | 신뢰, 평온함, 지성, 안정감 |
| `highlight_air` | `--ds-color-highlight-air` | `#D6EAF8` | Ice Blue | 정제됨, 청결함, 섬세함, 평온, 투명 |
| `proof_accent` | `--ds-color-proof-accent` | `#CC5500` | Burnt Orange | 따뜻함, 향수, 빈티지, 성숙함 |

Color rule: Token binding is necessary but not sufficient. Do not recombine `--ds-*` color roles into a new reference-like palette.

## Typography
| Role | Font | Token | Notes |
| --- | --- | --- | --- |
| heading | Noto Serif KR | `--ds-font-heading` | 한글 세리프의 사실상 유일한 고품질 웹폰트. 에디토리얼 한글에 필수. |
| body | Pretendard | `--ds-font-body` | 한글 UI 서체의 사실상 표준. Apple SD Gothic Neo 기반이지만 더 정교함. 라틴은 Inter 계열. |
| mono | n/a | `--ds-font-mono` | data, code, shortcuts only |
| korean | Pretendard | `--ds-font-ko` | primary script support |

- type scale: `xs`=12, `sm`=14, `md`=16, `lg`=21, `xl`=28, `2xl`=38, `3xl`=50
- line heights: `tight`=1.2, `normal`=1.5, `comfortable`=1.6, `relaxed`=1.75
- headline wrap: `word_break`=keep-all, `overflow_wrap`=normal, `text_wrap`=balance
- body wrap: `word_break`=keep-all, `overflow_wrap`=normal

## Spacing And Shape
- spacing scale: `0`, `2`, `4`, `8`, `12`, `16`, `24`, `32`, `48`, `64`, `96`
- radius scale: `none`, `sm`, `md`, `lg`, `xl`, `pill`

## Component Priorities
| Family | Priority | States | Components |
| --- | --- | --- | --- |
| button | high | `default`, `hover`, `active`, `disabled`, `loading` | `primary-button`, `secondary-button`, `icon-button`, `form-actions` |
| data-display | high | `default`, `sorted`, `filtered`, `empty`, `loading` | `data-table`, `column-header`, `row-actions`, `tag`, `feature-comparison`, `section-header`, +15 more |
| document | high | `default`, `selected`, `commenting`, `resolved` | `redline-viewer` |
| feedback | high | `info`, `success`, `warning`, `danger`, `loading` | `badge`, `inline-alert`, `empty-state`, `toast`, `status-dot`, `status-badge`, +4 more |
| input | high | `default`, `focus`, `error`, `disabled`, `selected` | `text-field`, `select`, `checkbox`, `switch`, `segmented-control`, `filter-chip`, +8 more |
| navigation | high | `default`, `active`, `hover`, `collapsed` | `breadcrumbs`, `tabs`, `pagination`, `wizard-layout`, `app-shell`, `sidebar-nav`, +3 more |

## Signature Components
| Component | Family | Anatomy | Token Binding |
| --- | --- | --- | --- |
| `breadcrumbs` | navigation | parts: container, nav-item, icon(optional), label, indicator(active), +1 more; states: default, hover, active, collapsed | slots: surface, text, padding, font |
| `inspector-drawer` | overlay | parts: drawer, header, section-list, property-row, action-row, +1 more; states: closed, open, loading, dirty | slots: surface, border, radius, padding |
| `data-table` | data-display | parts: container, header, content-area, footer(optional), action(optional); states: default, loading, empty, error | slots: surface, text, border, radius, padding |
| `column-header` | data-display | parts: container, header, content-area, footer(optional), action(optional); states: default, loading, empty, error | slots: surface, text, border, radius, padding |
| `row-actions` | data-display | parts: container, header, content-area, footer(optional), action(optional); states: default, loading, empty, error | slots: surface, text, border, radius, padding |
| `pagination` | navigation | parts: container, nav-item, icon(optional), label, indicator(active), +1 more; states: default, hover, active, collapsed | slots: surface, text, padding, font |

## Advanced Component Menu
| Component | Use When | Pairs With |
| --- | --- | --- |
| `evidence-graph` | trust depends on seeing relationships between claims and sources; auditors need to trace why an answer or decision was made | `citation-drawer`, `decision-record-card`, `policy-matrix` |
| `approval-rail` | work requires review, approval, rejection, or handoff; users need to know who owns the next decision | `policy-matrix`, `risk-summary-card`, `diff-viewer` |
| `confidence-meter` | AI or policy outcome includes uncertainty; users must decide whether to trust, edit, or escalate | `risk-summary-card`, `policy-matrix`, `tool-call-trace` |
| `decision-record-card` | a reviewer or AI-assisted workflow reaches a durable decision; regulated teams need record ids and retention status | `audit-timeline`, `approval-rail`, `citation-drawer` |
| `inspector-drawer` | a selected item needs rich detail without leaving the main workflow; users need source facts, owners, versions, or retention metadata | `policy-matrix`, `citation-drawer`, `decision-record-card` |
| `risk-summary-card` | users need a fast read of risk before drilling into policy details; AI confidence or compliance severity must be visible | `policy-matrix`, `confidence-meter`, `exception-queue` |
| `redline-viewer` | legal, compliance, or editorial text needs reviewer markup; comments must stay anchored to exact text ranges | `diff-viewer`, `comment-thread`, `approval-rail` |

Use these as ontology-approved building blocks when the workflow calls for richer professional UI. They still inherit token, typography, accessibility, and reference-governance rules.

## Design Context Pack
- No provider-neutral design context pack found. Use external references only after reading `system_spec.md`.

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
