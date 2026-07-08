# Curator System Style Capsule

- preset: `dashboard--editorial-warm`
- brand: Curator
- mode: `dashboard` / `editorial-warm`
- capsule_version: `1.0.0`
- companion files: `STYLE.md` is the human brief; `DESIGN.md` is the agent-ready copy.

## Taste Summary
editorial-warm 운영/큐레이션 대시보드 — sidebar-nav · data-table · kpi-card · filter-chip · editorial-calendar · curation-queue · publishing-pipeline, warm neutral + serif heading + muted accent, 한국어 1급.

## Authority Order
1. Product task flow and information architecture
2. `token_schema.json` and generated CSS variables
3. `components/component_specs.*` and `component_inventory.json`
4. `system_spec.md` and `system_ontology.json`
5. External visual references

Visual references are morphology inputs only. They may inform component shape, density, proportion, hierarchy rhythm, and affordance patterns; they must not override tokens, typography, domain IA, product copy, or palette composition.

## Voice And Boundaries
- brand keywords: `dashboard`, `admin`, `console`, `editorial`, `publishing`, `curation`, `newsroom`, `magazine-admin`, `content-studio`, `editor-dashboard`, +5 more
- tone: `calm`, `thoughtful`, `editorial`, `warm`, `measured`
- visual cues: `warm neutral sidebar`, `serif heading pair`, `muted editorial accent`, `reading-first data table`, `calm kpi card`, `soft cream surface`, `restrained editorial chrome`, `muted warm divider`, +1 more
- avoid: `minimal-tech`, `bold-confident`, `saturated`, `playful-pastel`, `corporate-conservative`, `streetwear`, `high-contrast`, `neon`, +1 more

## Color Roles
| Role | Token | Value | Source | Use |
| --- | --- | --- | --- | --- |
| `primary` | `--ds-color-primary` | `#614051` | Aubergine | 저명도, 중채도, 뉴트럴 베이스의 퍼플 톤 / 고혹적, 성숙함, 미스터리, 예술적, 긴장감 |
| `accent` | `--ds-color-accent` | `#FADA5E` | Naples Yellow | 고명도, 저채도, 크리미한 라이트 옐로 톤 / 부드러움, 따뜻함, 온화함, 예술적 감성 |
| `surface_tint` | `--ds-color-surface-tint` | `#F9C0C4` | Blush | 아주 연한 핑크 톤, 미세한 살구빛이 섞인 고명도 파스텔 / 섬세함, 순수함, 따뜻한 감정, 부드러움 |
| `canvas` | `--ds-color-canvas` | `#F7F8FA` | Canvas White | Generated fallback support color |
| `surface` | `--ds-color-surface` | `#FFFFFF` | Paper | Generated fallback support color |
| `surface_muted` | `--ds-color-surface-muted` | `#EEF1F6` | Surface Muted | Generated fallback support color |
| `surface_elevated` | `--ds-color-surface-elevated` | `#FFFFFF` | Paper | Generated fallback support color |
| `border` | `--ds-color-border` | `#D6DDE6` | Border Neutral | Generated fallback support color |
| `border_strong` | `--ds-color-border-strong` | `#B0BAC7` | Border Strong | Generated fallback support color |
| `ink` | `--ds-color-ink` | `#111111` | Ink | Generated fallback support color |
| `ink_muted` | `--ds-color-ink-muted` | `#614051` | Aubergine | 저명도, 중채도, 뉴트럴 베이스의 퍼플 톤 / 고혹적, 성숙함, 미스터리, 예술적, 긴장감 |
| `ink_subtle` | `--ds-color-ink-subtle` | `#6B7280` | Subtle Ink | Generated fallback support color |
| `info` | `--ds-color-info` | `#614051` | Aubergine | 저명도, 중채도, 뉴트럴 베이스의 퍼플 톤 / 고혹적, 성숙함, 미스터리, 예술적, 긴장감 |
| `success` | `--ds-color-success` | `#4A7C59` | Success | Generated fallback support color |
| `warning` | `--ds-color-warning` | `#FADA5E` | Naples Yellow | 고명도, 저채도, 크리미한 라이트 옐로 톤 / 부드러움, 따뜻함, 온화함, 예술적 감성 |
| `danger` | `--ds-color-danger` | `#FA8072` | Salmon | 밝고 따뜻한 핑크 오렌지 톤 / 따뜻함, 부드러움, 친근함, 자연스러움 |
| `link` | `--ds-color-link` | `#614051` | Aubergine | 저명도, 중채도, 뉴트럴 베이스의 퍼플 톤 / 고혹적, 성숙함, 미스터리, 예술적, 긴장감 |

Color rule: Token binding is necessary but not sufficient. Do not recombine `--ds-*` color roles into a new reference-like palette.

## Typography
| Role | Font | Token | Notes |
| --- | --- | --- | --- |
| heading | EB Garamond | `--ds-font-heading` | classic book-feel editorial serif heading — masthead / issue-header / section-header / article-pr... |
| body | Inter | `--ds-font-body` | dashboard 본문 공용 — data-table cell / kpi-card label / filter-chip / comment-thread / editorial-ana... |
| mono | JetBrains Mono | `--ds-font-mono` | data, code, shortcuts only |
| korean | Pretendard | `--ds-font-ko` | primary script support |

- type scale: `xs`=12, `sm`=14, `md`=16, `lg`=21, `xl`=28, `2xl`=38, `3xl`=50
- line heights: `tight`=1.2, `normal`=1.5, `comfortable`=1.6, `relaxed`=1.75
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
| button | high | `default`, `hover`, `active`, `disabled`, `loading` | `primary-button`, `secondary-button`, `icon-button`, `form-actions`, `add-to-cart-button`, `wishlist-toggle`, +4 more |
| copilot-artifact | high | `default`, `loading`, `verified`, `error` | `message-artifact`, `artifact-preview-panel`, `draft-document`, `outline-sidebar`, `revision-timeline`, `reading-mode-toggle`, +5 more |
| copilot-chat | high | `default`, `loading`, `complete`, `error` | `streaming-cursor`, `typing-indicator`, `inline-citation`, `mention-chip`, `suggestion-card`, `thread-header` |
| data-display | high | `default`, `sorted`, `filtered`, `empty`, `loading` | `metric-strip`, `status-summary-row`, `task-surface-header`, `source-ledger`, `section-header`, `data-table`, +25 more |
| document | high | `default`, `selected`, `commenting`, `resolved` | `article-body`, `table-of-contents`, `heading-anchor`, `prose-block`, `reading-pane`, `footnote`, +5 more |
| editorial | high | `default`, `selected`, `editing` | `editor-canvas`, `editor-toolbar`, `inline-format-menu`, `slash-command-menu`, `block-controls` |

## Signature Components
| Component | Family | Anatomy | Token Binding |
| --- | --- | --- | --- |
| `curation-queue` | dashboard-editorial | parts: container, header, content-area, footer(optional), action(optional); states: default, loading, empty, error | slots: surface, text, border, radius, padding |
| `archive-shelf` | dashboard-editorial | parts: container, header, content-area, footer(optional), action(optional); states: default, loading, empty, error | slots: surface, text, border, radius, padding |
| `issue-planner` | dashboard-editorial | parts: container, header, content-area, footer(optional), action(optional); states: default, loading, empty, error | slots: surface, text, border, radius, padding |
| `contributor-roster` | dashboard-editorial | parts: container, header, content-area, footer(optional), action(optional); states: default, loading, empty, error | slots: surface, text, border, radius, padding |
| `editorial-calendar` | dashboard-editorial | parts: container, header, content-area, footer(optional), action(optional); states: default, loading, empty, error | slots: surface, text, border, radius, padding |
| `editorial-analytics-kpi` | dashboard-editorial | parts: container, header, content-area, footer(optional), action(optional); states: default, loading, empty, error | slots: surface, text, border, radius, padding |

## Advanced Component Menu
| Component | Use When | Pairs With |
| --- | --- | --- |
| `resizable-split-pane` | primary work happens between list, canvas/chat, and detail panels; users need to compare or inspect adjacent information without navigation | `thread-list`, `artifact-preview-panel`, `inspector-drawer` |
| `redline-viewer` | legal, compliance, or editorial text needs reviewer markup; comments must stay anchored to exact text ranges | `diff-viewer`, `comment-thread`, `approval-rail` |
| `approval-rail` | work requires review, approval, rejection, or handoff; users need to know who owns the next decision | `policy-matrix`, `risk-summary-card`, `diff-viewer` |
| `bulk-action-table` | users handle many records at once; selection count and destructive actions must stay visible | `saved-view-bar`, `filter-builder`, `exception-queue` |
| `saved-view-bar` | teams revisit the same filtered views often; dense tools need stable scope memory | `filter-builder`, `bulk-action-table`, `exception-queue` |
| `diff-viewer` | AI rewrites, policy edits, or reviewer changes need auditability; users must approve what changed before publishing | `redline-viewer`, `revision-timeline`, `approval-rail` |
| `exception-queue` | multiple issues require triage, assignment, and resolution; reviewers need to batch handle exceptions | `bulk-action-table`, `policy-matrix`, `approval-rail` |
| `filter-builder` | users need AND/OR logic across several fields; filters should be saved, shared, or audited | `saved-view-bar`, `bulk-action-table`, `exception-queue` |

Use these as ontology-approved building blocks when the workflow calls for richer professional UI. They still inherit token, typography, accessibility, and reference-governance rules.

## Design Context Pack
- activation: `planned`
- providers: `pinterest`=preview, `lazyweb`=suggested
- flow coverage: dashboard(covered), general-product-ui(covered), data-review(gap), document(gap), navigation(gap)
| Context | Provider | Allowed Use |
| --- | --- | --- |
| ghost editorial dashboard curation | `lazyweb` | morphology: `general-interface-composition`; flows: `dashboard` |
| substack writer dashboard publishing | `lazyweb` | morphology: `general-interface-composition`; flows: `dashboard` |
| medium creator dashboard editorial analytics | `lazyweb` | morphology: `general-interface-composition`; flows: `dashboard` |
| notion editorial calendar publishing pipeline | `lazyweb` | morphology: `general-interface-composition`; flows: `general-product-ui` |
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
