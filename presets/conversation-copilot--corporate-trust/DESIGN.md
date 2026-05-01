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
| heading | Pretendard | `--ds-font-heading` | 한글 UI 서체의 사실상 표준. Apple SD Gothic Neo 기반이지만 더 정교함. 라틴은 Inter 계열. |
| body | Pretendard | `--ds-font-body` | 한글 UI 서체의 사실상 표준. Apple SD Gothic Neo 기반이지만 더 정교함. 라틴은 Inter 계열. |
| mono | IBM Plex Mono | `--ds-font-mono` | data, code, shortcuts only |
| korean | Pretendard | `--ds-font-ko` | primary script support |

- type scale: `xs`=12, `sm`=13, `md`=15, `lg`=19, `xl`=24, `2xl`=30, `3xl`=37
- line heights: `tight`=1.25, `normal`=1.45, `comfortable`=1.55, `relaxed`=1.65
- headline wrap: `word_break`=keep-all, `overflow_wrap`=normal, `text_wrap`=balance
- body wrap: `word_break`=keep-all, `overflow_wrap`=normal

## Spacing And Shape
- spacing scale: `0`, `2`, `4`, `8`, `12`, `16`, `24`, `32`, `48`, `64`, `96`
- density bias: `airy`
- radius scale: `none`, `sm`, `md`, `lg`, `xl`, `pill`
- corner bias: `round`

## Component Priorities
| Family | Priority | States | Components |
| --- | --- | --- | --- |
| button | high | `default`, `hover`, `active`, `disabled`, `loading` | `primary-button`, `secondary-button`, `ghost-button`, `icon-button`, `cta-button`, `link-button`, +8 more |
| data-display | high | `default`, `sorted`, `filtered`, `empty` | `chat-message`, `chat-thread`, `comment-thread`, `tag`, `data-table`, `column-header`, +20 more |
| editorial | high | `default`, `selected`, `editing` | `editor-canvas`, `editor-toolbar`, `inline-format-menu`, `slash-command-menu`, `block-controls`, `content-card`, +3 more |
| feedback | high | `info`, `success`, `warning`, `danger` | `inline-alert`, `empty-state`, `toast`, `status-badge`, `empty-conversation-state`, `banner`, +7 more |
| input | high | `default`, `focus`, `error`, `disabled` | `text-field`, `search-field`, `segmented-control`, `chat-input`, `comment-input`, `chip`, +20 more |
| marketing | high | `default`, `hover`, `in-view` | `logo-cloud`, `customer-logo`, `metric-highlight`, `press-quote`, `faq-section`, `faq-item`, +7 more |

## Signature Components
| Component | Family | Anatomy | Token Binding |
| --- | --- | --- | --- |
| `message-artifact` | copilot-artifact | parts: container, header, content-area, footer(optional), action(optional); states: default, loading, empty, error | slots: surface, text, border, radius, padding |
| `chat-message` | data-display | parts: container, header, content-area, footer(optional), action(optional); states: default, loading, empty, error | slots: surface, text, border, radius, padding |
| `chat-thread` | data-display | parts: container, header, content-area, footer(optional), action(optional); states: default, loading, empty, error | slots: surface, text, border, radius, padding |
| `mention-chip` | copilot-chat | parts: container, header, content-area, footer(optional), action(optional); states: default, loading, empty, error | slots: surface, text, border, radius, padding |
| `suggestion-card` | copilot-chat | parts: container, inner-content; states: default, hover, focus-visible | slots: surface, border, radius, padding |
| `prompt-composer` | input | parts: container, label, input-area, helper-text(optional), leading-icon(optional), +1 more; states: default, focus,... | slots: surface, text, border, radius, padding, font |

## Reference Governance
- allowed from references: `component morphology`, `layout density`, `panel/card proportions`, `hierarchy rhythm`, `interaction affordance patterns`
- denied from references: `color palette`, `palette composition or derived secondary palettes`, `typography family or scale`, `semantic status colors`, `product copy`, `product data model`, `navigation labels`, `domain information architecture`, `redistributable imagery unless explicitly licensed`
- implementation guardrails:
  - 기존 핵심 화면, 진입점, 작업 흐름은 명시적 승인 없이 제거하거나 숨기지 않음.
  - 전면 셸 리라이트보다 토큰 -> primitive -> feature surface 순서의 점진적 롤아웃을 우선.
  - 새 시각 규칙은 지원 대상 테마와 breakpoint 전체에서 먼저 검증.
  - 기존 데이터 밀도와 업무 완료 경로를 유지한 상태에서 시각 품질을 높이는 방향을 우선.
  - 기능 위치 변경, 정보 구조 변경, 패널 제거는 별도의 migration plan이 있을 때만 수행.
  - 아이콘 자리에 이모지(🎨 ✅ 🔥 등)를 넣지 않음 — SVG 아이콘 또는 아이콘 라이브러리만 사용.
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
