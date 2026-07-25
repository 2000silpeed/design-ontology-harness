# Mercer System Style Capsule

- preset: `conversation-copilot--corporate-trust`
- brand: Mercer
- mode: `conversation-copilot` / `corporate-trust`
- capsule_version: `1.0.0`
- companion files: `STYLE.md` is the human brief; `DESIGN.md` is the agent-ready copy.

## Taste Summary
금융·보험 enterprise AI 챗봇 builder — conversation-copilot--corporate-trust 톤, workspace + thread + chat + compliance-artifact + audit-trail + policy-check + citation, super-sonic blue + copper + powder blue palette, 규제·감사 맥락 한국어 1급.

## Authority Order
1. Product task flow and information architecture
2. `token_schema.json` and generated CSS variables
3. `components/component_specs.*` and `component_inventory.json`
4. `system_spec.md` and `system_ontology.json`
5. External visual references

Visual references are morphology inputs only. They may inform component shape, density, proportion, hierarchy rhythm, and affordance patterns; they must not override tokens, typography, domain IA, product copy, or palette composition.

## Voice And Boundaries
- brand keywords: `conversation-copilot`, `enterprise-chatbot`, `corporate-trust`, `finance`, `insurance`, `compliance`, `audit`, `regulatory`, `policy-check`, `super-sonic-blue`, +4 more
- tone: `calm`, `precise`, `trustworthy`, `professional`, `reassuring`, `compliant`
- visual cues: `calm enterprise surface`, `super-sonic blue primary conversation`, `copper accent indicator`, `powder blue soft surface tint`, `neutral chat bubbles`, `compliance sidebar panel`, `audit trail timeline`, `policy check badge`, +1 more
- avoid: `playful-pastel`, `streetwear-drop`, `editorial-warm-serif`, `bold-saturated-marketing`, `consumer-d2c-commerce`, `social-feed-casual`, `magazine-cover-heavy`

## Color Roles
| Role | Token | Value | Source | Use |
| --- | --- | --- | --- | --- |
| `primary` | `--ds-color-primary` | `#0071A8` | Super Sonic | 고명도, 중고채도, 브라이트 블루(Bright Blue) 톤 / 혁신적, 미래지향적, 역동적, 청량감, 에너지 |
| `accent` | `--ds-color-accent` | `#B87333` | Copper | 저명도, 중채도, 오렌지와 레드 브라운 사이의 금속성 톤 / 고급스러움, 따뜻함, 전통적 질감, 세련된 무게감 |
| `surface_tint` | `--ds-color-surface-tint` | `#B0E0E6` | Powder Blue | 중명도, 저채도, 뉴트럴 톤 / 부드러움, 균형감, 온화함, 정제된 따뜻함 |
| `canvas` | `--ds-color-canvas` | `#F7F8FA` | Canvas White | Generated fallback support color |
| `surface` | `--ds-color-surface` | `#FFFFFF` | Paper | Generated fallback support color |
| `surface_muted` | `--ds-color-surface-muted` | `#EEF1F6` | Surface Muted | Generated fallback support color |
| `surface_elevated` | `--ds-color-surface-elevated` | `#FFFFFF` | Paper | Generated fallback support color |
| `border` | `--ds-color-border` | `#C4C4C4` | Pairing #C4C4C4 | Seed pairing support |
| `border_strong` | `--ds-color-border-strong` | `#C0C0C0` | Pairing #C0C0C0 | Seed pairing support |
| `ink` | `--ds-color-ink` | `#111111` | Ink | Generated fallback support color |
| `ink_muted` | `--ds-color-ink-muted` | `#6B6F74` | Pairing #6B6F74 | Seed pairing support |
| `ink_subtle` | `--ds-color-ink-subtle` | `#6B7280` | Subtle Ink | Generated fallback support color |
| `info` | `--ds-color-info` | `#2C3E50` | Pairing #2C3E50 | Seed pairing support |
| `success` | `--ds-color-success` | `#4A7C59` | Success | Generated fallback support color |
| `warning` | `--ds-color-warning` | `#B87333` | Copper | 저명도, 중채도, 오렌지와 레드 브라운 사이의 금속성 톤 / 고급스러움, 따뜻함, 전통적 질감, 세련된 무게감 |
| `danger` | `--ds-color-danger` | `#8B2252` | Danger | Generated fallback support color |
| `link` | `--ds-color-link` | `#0071A8` | Super Sonic | 고명도, 중고채도, 브라이트 블루(Bright Blue) 톤 / 혁신적, 미래지향적, 역동적, 청량감, 에너지 |

Color rule: Token binding is necessary but not sufficient. Do not recombine `--ds-*` color roles into a new reference-like palette.

## Typography
| Role | Font | Token | Notes |
| --- | --- | --- | --- |
| heading | Inter | `--ds-font-heading` | enterprise neutral sans — workspace-header / thread-title / policy-check 라벨 / compliance-artifact... |
| body | Inter | `--ds-font-body` | chat-message body / compliance-artifact paragraph / audit-trail description 공용 본문, line-height 1.... |
| mono | JetBrains Mono | `--ds-font-mono` | data, code, shortcuts only |
| korean | Pretendard | `--ds-font-ko` | primary script support |

- type scale: `xs`=12, `sm`=13, `md`=15, `lg`=19, `xl`=24, `2xl`=30, `3xl`=37
- line heights: `tight`=1.25, `normal`=1.45, `comfortable`=1.55, `relaxed`=1.65
- headline wrap: `word_break`=keep-all, `overflow_wrap`=normal, `text_wrap`=balance
- body wrap: `word_break`=keep-all, `overflow_wrap`=normal

## Spacing And Shape
- spacing scale: `0`, `2`, `4`, `8`, `12`, `16`, `24`, `32`, `48`, `64`, `96`
- density bias: `balanced`
- radius scale: `none`, `sm`, `md`, `lg`, `xl`, `pill`
- corner bias: `round`

## Component Priorities
| Family | Priority | States | Components |
| --- | --- | --- | --- |
| button | high | `default`, `hover`, `active`, `disabled`, `loading` | `primary-button`, `secondary-button`, `icon-button`, `regenerate-button`, `stop-generation-button`, `new-thread-button`, +5 more |
| copilot-artifact | high | `default`, `loading`, `verified`, `error` | `message-artifact`, `artifact-preview-panel`, `draft-document`, `outline-sidebar`, `revision-timeline`, `reading-mode-toggle`, +5 more |
| copilot-chat | high | `default`, `loading`, `complete`, `error` | `streaming-cursor`, `typing-indicator`, `inline-citation`, `mention-chip`, `suggestion-card`, `thread-header` |
| data-display | high | `default`, `sorted`, `filtered`, `empty`, `loading` | `chat-message`, `chat-thread`, `comment-thread`, `tag`, `metric-strip`, `status-summary-row`, +24 more |
| document | high | `default`, `selected`, `commenting`, `resolved` | `article-body`, `table-of-contents`, `heading-anchor`, `prose-block`, `reading-pane`, `footnote`, +3 more |
| editorial | high | `default`, `selected`, `editing` | `editor-canvas`, `editor-toolbar`, `inline-format-menu`, `slash-command-menu`, `block-controls` |

## Signature Components
| Component | Family | Anatomy | Token Binding |
| --- | --- | --- | --- |
| `message-artifact` | copilot-artifact | parts: container, header, content-area, footer(optional), action(optional); states: default, loading, empty, error | slots: surface, text, border, radius, padding |
| `chat-message` | data-display | parts: container, header, content-area, footer(optional), action(optional); states: default, loading, empty, error | slots: surface, text, border, radius, padding |
| `chat-thread` | data-display | parts: container, header, content-area, footer(optional), action(optional); states: default, loading, empty, error | slots: surface, text, border, radius, padding |
| `mention-chip` | copilot-chat | parts: container, header, content-area, footer(optional), action(optional); states: default, loading, empty, error | slots: surface, text, border, radius, padding |
| `suggestion-card` | copilot-chat | parts: container, inner-content; states: default, hover, focus-visible | slots: surface, border, radius, padding |
| `audit-timeline` | data-display | parts: list, event-item, timestamp, actor, event-summary, +1 more; states: default, filtered, expanded, empty | slots: surface, border |

## Advanced Component Menu
| Component | Use When | Pairs With |
| --- | --- | --- |
| `resizable-split-pane` | primary work happens between list, canvas/chat, and detail panels; users need to compare or inspect adjacent information without navigation | `thread-list`, `artifact-preview-panel`, `inspector-drawer` |
| `citation-drawer` | answers must show supporting policy, document, or source records; users need to inspect evidence without losing conversation context | `inline-citation`, `source-card`, `evidence-graph` |
| `decision-record-card` | a reviewer or AI-assisted workflow reaches a durable decision; regulated teams need record ids and retention status | `audit-timeline`, `approval-rail`, `citation-drawer` |
| `policy-matrix` | multiple policy rules must be checked against multiple claims or fields; reviewers need dense scan-and-drill compliance status | `risk-summary-card`, `exception-queue`, `approval-rail` |
| `source-card` | AI output depends on external or internal source records; users need a repeatable citation preview component | `citation-drawer`, `evidence-graph`, `inline-citation` |
| `audit-timeline` | regulated workflows require traceable user and AI actions; reviewers need to reconstruct what happened before approval | `decision-record-card`, `approval-rail`, `tool-call-trace` |
| `diff-viewer` | AI rewrites, policy edits, or reviewer changes need auditability; users must approve what changed before publishing | `redline-viewer`, `revision-timeline`, `approval-rail` |
| `redline-viewer` | legal, compliance, or editorial text needs reviewer markup; comments must stay anchored to exact text ranges | `diff-viewer`, `comment-thread`, `approval-rail` |

Use these as ontology-approved building blocks when the workflow calls for richer professional UI. They still inherit token, typography, accessibility, and reference-governance rules.

## Design Context Pack
- activation: `planned`
- providers: `pinterest`=preview, `lazyweb`=suggested
- flow coverage: general-product-ui(covered), messaging(covered), navigation(covered), settings(covered), data-review(gap), document(gap)
| Context | Provider | Allowed Use |
| --- | --- | --- |
| chatgpt enterprise admin console | `lazyweb` | morphology: `general-interface-composition`; flows: `settings` |
| anthropic claude enterprise workspace | `lazyweb` | morphology: `general-interface-composition`; flows: `navigation` |
| stripe dialog documentation | `lazyweb` | morphology: `general-interface-composition`; flows: `general-product-ui` |
| salesforce einstein assistant | `lazyweb` | morphology: `general-interface-composition`; flows: `messaging` |
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
