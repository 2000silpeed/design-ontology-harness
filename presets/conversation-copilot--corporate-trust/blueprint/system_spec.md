# Mercer System Spec

## 1. Positioning

- **Brand**: Mercer
- **Product**: 금융·보험 기업의 고객 상담 AI 챗봇 builder — conversation-copilot--corporate-trust 톤 enterprise chat + prompt + compliance-artifact(draft) + audit-trail + policy-check + thread · workspace, 신뢰감 있는 super-sonic blue primary + copper accent + powder blue surface, 규제·감사 맥락 한국어 1급
- **Audience**: 금융·보험 고객 상담팀 — 규제 내 AI 상담 응답을 검토·배포하는 operations 담당자, 컴플라이언스 · 감사 담당자 — AI 상담 응답의 policy-check / audit-trail / retention 기록이 명확해야 하는 규제 대응 팀, 엔터프라이즈 IT/플랫폼팀 — 금융·보험 도메인 AI 챗봇을 사내 툴체인 / SSO / DLP 와 연결해 배포하는 IT 관리자
- **Platforms**: web, desktop-web
- **Accessibility floor**: WCAG 2.2 AA

## 2. Identity Guardrails

- **Brand keywords**: conversation-copilot, enterprise-chatbot, corporate-trust, finance, insurance, compliance, audit, regulatory, policy-check, super-sonic-blue, copper, powder-blue, calm-enterprise, reliable
- **Anti-keywords**: playful-pastel, streetwear-drop, editorial-warm-serif, bold-saturated-marketing, consumer-d2c-commerce, social-feed-casual, magazine-cover-heavy
- **Tone of voice**: calm, precise, trustworthy, professional, reassuring, compliant
- **Visual direction**: calm enterprise surface, super-sonic blue primary conversation, copper accent indicator, powder blue soft surface tint, neutral chat bubbles, compliance sidebar panel, audit trail timeline, policy check badge, enterprise workspace header
- **Interaction direction**: calm streaming cursor, policy-check inline badge reveal, audit-trail side panel expand, compliance warning modal, enterprise toast, keyboard-friendly chat, sso login redirect, reviewer handoff

## 3. Design Principles

- **Conversation-Copilot**: `conversation-copilot`를 시각적 선택과 인터랙션 선택의 기본 기준으로 삼습니다.
- **Enterprise-Chatbot**: `enterprise-chatbot`를 시각적 선택과 인터랙션 선택의 기본 기준으로 삼습니다.
- **Corporate-Trust**: `corporate-trust`를 시각적 선택과 인터랙션 선택의 기본 기준으로 삼습니다.
- **Finance**: `finance`를 시각적 선택과 인터랙션 선택의 기본 기준으로 삼습니다.

## 4. Foundation Priorities

- **Grid, container, and page rhythm** (high): signal 42
- **Content design and microcopy rules** (high): signal 36
- **Accessibility rules and contrast baseline** (high): signal 35
- **Color tokens and semantic color policy** (high): signal 35
- **Icon family and stroke policy** (high): signal 30

## 5. Token Strategy

- **Layering**: core -> semantic -> component
- **Core categories**: color, spacing, radius, typography, motion, elevation
- **Semantic categories**: surface, text, border, focus, feedback
- **Component categories**: button, input, navigation, overlay, editor
- **Typography families**: brand, text, mono
- **Spacing scale**: 0, 2, 4, 8, 12, 16, 24, 32, 48, 64, 96

### Typography System (auto-resolved)

- **Heading**: Pretendard
- **Body**: Pretendard
- **Korean**: Pretendard
- **Mono**: IBM Plex Mono
- **Product type detected**: enterprise
- **Pairing source**: auto-scored
- **Line height**: normal
- **Type scale**: base 15px, ratio 1.25 (xs=12px, sm=13px, md=15px, lg=19px, xl=24px, 2xl=30px, 3xl=37px)
- **Strategy**:
  - 단일 서체(Pretendard)로 weight 대비 위계 — 일관성 우선
  - 한글 서체: Pretendard — 라틴과 x-height/weight 조화
  - 모노스페이스: IBM Plex Mono — 코드/데이터 영역 전용
- **Heading note**: 한글 UI 서체의 사실상 표준. Apple SD Gothic Neo 기반이지만 더 정교함. 라틴은 Inter 계열.
- **Body note**: 한글 UI 서체의 사실상 표준. Apple SD Gothic Neo 기반이지만 더 정교함. 라틴은 Inter 계열.
- **Korean rationale**: Pretendard — 한글 UI 서체의 사실상 표준. 토스, 당근, 리디 등 국내 주요 서비스에서 사용. 자간이 자연스럽고 weight 전 구간에서 안정적.
- **Heading tracking**: xl=-0.01em, 2xl=-0.02em, 3xl=-0.02em
- **Primary script**: korean
- **Hangul headline defaults**: Pretendard | line-height 1.25-1.35 | tracking 0em
- **Hangul body defaults**: Pretendard | line-height 1.6-1.7 | label line-height 1.4-1.5
- **Wrap defaults**: headline word-break=keep-all, headline text-wrap=balance, body word-break=keep-all
- **Scale guidance**: 기본 스케일을 사용할 수 있지만 한글 문장 기준으로 실제 wrap을 먼저 검증한다.
- **Loading**: Pretendard(preload), IBM Plex Mono(lazy) | display: swap

## 6. Color Reference

- **Source**: REFERENCE X Vol.1 - Color Reference (/Users/sungwoon/ai-projects/design-ontology-harness/docs/color-reference.md)
- **Selection mode**: manual
- **Preferred families**: Pantone Trend Blues, Standard Blues, Standard Oranges, Pastel Blues
- **Palette strategy**: temperature=mixed, contrast=balanced, diversity=balanced, surface_style=tinted
- **Palette expansion**: supporting_color_count=10, combination_count=3, prefer_pairings=True
- **Palette roles**:
  - `primary` -> Super Sonic #0071A8 / Pantone Trend Blues
  - `accent` -> Copper #B87333 / Deep Oranges
  - `surface_tint` -> Powder Blue #B0E0E6 / Pastel Blues
- **Selected colors**:
  - Classic Blue #0F4C81 / Pantone Trend Blues / 중명도, 중채도, 클래식한 딥 블루 톤 / 신뢰, 평온함, 지성, 안정감
  - Ochre #CC7722 / Standard Oranges / 중명도, 중채도, 흙기 섞인 따뜻한 오렌지 / 안정감, 내추럴, 신뢰감, 지속성
  - Misty Blue #B5C7EB / Pastel Blues / 중명도, 저채도, 보라색이 섞인 뉴트럴 블루 톤 / 차분함, 사색적, 몽환적, 잔잔함, 감정의 여운
- **Palette candidates**:
  - signature-1 (Signature): primary=Classic Blue, accent=Ochre, surface_tint=Misty Blue / Classic Blue is inside preferred families.; Ochre is inside preferred families.
- **Expanded supporting colors**:
  - Pairing #2C3E50 #2C3E50 / Derived Pairing / pairing-swatch / Pairing #2C3E50 comes from the seed pairing references.; Pairing #2C3E50 is explicitly paired with Powder Blue.
  - Pairing #F6F1E7 #F6F1E7 / Derived Pairing / pairing-swatch / Pairing #F6F1E7 comes from the seed pairing references.; Pairing #F6F1E7 is explicitly paired with Copper.
  - Pairing #F7F3E9 #F7F3E9 / Derived Pairing / pairing-swatch / Pairing #F7F3E9 comes from the seed pairing references.; Pairing #F7F3E9 is explicitly paired with Powder Blue.
  - Pairing #D7BA99 #D7BA99 / Derived Pairing / pairing-swatch / Pairing #D7BA99 comes from the seed pairing references.; Pairing #D7BA99 is explicitly paired with Copper.
  - Pairing #D7C4A3 #D7C4A3 / Derived Pairing / pairing-swatch / Pairing #D7C4A3 comes from the seed pairing references.; Pairing #D7C4A3 is explicitly paired with Powder Blue.
  - Pairing #C0C0C0 #C0C0C0 / Derived Pairing / pairing-swatch / Pairing #C0C0C0 comes from the seed pairing references.; Pairing #C0C0C0 is explicitly paired with Super Sonic.
  - Pairing #C4C4C4 #C4C4C4 / Derived Pairing / pairing-swatch / Pairing #C4C4C4 comes from the seed pairing references.; Pairing #C4C4C4 is explicitly paired with Powder Blue.
  - Pairing #D3D3D3 #D3D3D3 / Derived Pairing / pairing-swatch / Pairing #D3D3D3 comes from the seed pairing references.; Pairing #D3D3D3 is explicitly paired with Super Sonic.
- **Expanded semantic roles**:
  - `brand_primary` -> Super Sonic #0071A8 / Pantone Trend Blues
  - `brand_accent` -> Copper #B87333 / Deep Oranges
  - `surface_tint` -> Powder Blue #B0E0E6 / Pastel Blues
  - `canvas` -> Canvas White #F7F8FA / Generated Fallback
  - `surface` -> Paper #FFFFFF / Generated Fallback
  - `surface_muted` -> Surface Muted #EEF1F6 / Generated Fallback
  - `surface_elevated` -> Paper #FFFFFF / Generated Fallback
  - `border` -> Pairing #C4C4C4 #C4C4C4 / Derived Pairing
  - `border_strong` -> Pairing #C0C0C0 #C0C0C0 / Derived Pairing
  - `ink` -> Ink #111111 / Generated Fallback
- **Combination lists**:
  - Seed Core: primary=Super Sonic, accent=Copper, surface_tint=Powder Blue
  - Surface System: canvas=Canvas White, surface=Paper, surface_tint=Powder Blue, border=Pairing #C4C4C4, ink=Ink, ink_muted=Pairing #6B6F74
  - Support Spectrum: support=Pairing #2C3E50, support=Pairing #F6F1E7, support=Pairing #F7F3E9, support=Pairing #D7BA99, support=Pairing #D7C4A3, support=Pairing #C0C0C0
- **Notes**: Super Sonic #0071A8 primary — bright enterprise blue, prompt-composer send-button / AI message accent / policy-check badge / workspace header primary, Copper #B87333 accent — warm enterprise copper, audit-trail step / reviewer-assignment chip / compliance warning subtle indicator / citation link, Powder Blue #B0E0E6 surface_tint — soft enterprise blue wash, thread sidebar surface / compliance-artifact panel tint / empty state, light mode 기본 — 금융·보험 엔터프라이즈 관례 (신뢰·정돈), dark 옵션 제공 (deep navy + 채도 낮춘 Super Sonic / Copper + Powder Blue 대체는 Misty Blue deep variant), HEX 겹침 현황: beacon (marketing-landing--minimal-tech) 의 surface_tint Powder Blue #B0E0E6 와 1 role 겹침 — marketing-landing 과 conversation-copilot 의 app_mode 축 분기 + minimal-tech 와 corporate-trust 의 brand_tone 축 분기로 제품 구조/감성 완전 차별화 (SaaS 랜딩 hero-pricing vs enterprise chat workspace), ledger (dashboard--corporate-trust) 와 corporate-trust 톤 공유하지만 primary/accent/surface_tint 전부 다름 — Prussian Blue/Bronze Gold/Ice Blue 의 dashboard fintech 운영 톤 vs Super Sonic/Copper/Powder Blue 의 conversation copilot enterprise 톤, glacier (conversation-copilot--minimal-tech) 와 같은 conversation-copilot app_mode 이지만 primary/accent/surface_tint 전부 다름 — Navy Blue/Ochre/Sky Blue neutral AI workspace vs Super Sonic/Copper/Powder Blue enterprise compliance tone, quill (conversation-copilot--editorial-warm) 와도 HEX 겹침 0 — warm Marsala/Moss Green/Flax editorial writing vs enterprise Super Sonic/Copper/Powder Blue compliance
- **Application rule**: 레퍼런스 컬러는 semantic token으로 번역해서 사용하고, 접근성과 theme 호환성을 우선합니다.

## 7. Visual Reference Signals

- **Mode**: local-images
- **Coverage**: source 0 / image 0 / selected 0
- **Rule**: visual references are advisory signals for motif and layout direction; official KB/spec remain the structural source of truth.
- **Provenance**: `observed` = directly measured from local pixels, `inferred` = synthesized from image/query/brand signals, `unverified` = reliable visual evidence not yet available.
- **Query seeds**: chatgpt enterprise admin console, anthropic claude enterprise workspace, stripe dialog documentation, salesforce einstein assistant, intercom fin ai copilot
### Visual Direction

- **Density**: airy (confidence 0.82, provenance inferred) / editorial x2, landing x1, hero x1
- **Surface Style**: tinted (confidence 0.45, provenance inferred) / warm x2, editorial x2, soft x1
- **Corner Style**: round (confidence 0.34, provenance inferred) / soft x1
- **Typography Mood**: utilitarian (confidence 0.94, provenance inferred) / admin x1, enterprise x12
- **Color balance**: temperature=unknown, contrast=unknown, neutral_bias=unknown, provenance=unverified

### Layout Rhythm

- **Conversation side panel**: confidence 0.94 / provenance inferred / chat x6, assistant x1, message x5, thread x3
- **Data review surface**: confidence 0.94 / provenance inferred / grid x1, audit x6, data x1, timeline x3
- **Editorial feed**: confidence 0.94 / provenance inferred / editorial x2, feed x2, magazine x2
- **Split-pane workspace**: confidence 0.94 / provenance inferred / workspace x5, sidebar x3, panel x4

### Image-derived Component Hints

- **Cards**: low-elevation tinted cards를 기본으로 하고, 넓은 내부 여백과 강한 section breathing room. soft round corner를 기본값으로 유지. / provenance inferred / surface=tinted, density=airy, corner=round
- **Navigation**: 고정 sidebar 또는 split-pane navigation을 우선하고, 현재 위치와 scope를 항상 명시한다. / provenance inferred / Split-pane workspace
- **Typography**: utilitarian hierarchy를 유지하되 중요한 heading만 선택적으로 크게 만든다. / provenance inferred / typography_mood=utilitarian
- **Data Display**: 정보 밀도를 유지하되 thin dividers와 restrained accent로 hierarchy를 만든다. / provenance inferred / layout=data-review-surface, density=airy
- **Panel**: 보조 패널은 메인 표면보다 한 단계 더 조용한 tint와 명확한 section framing으로 구분한다. / provenance inferred / Conversation side panel

### Synthesis Notes

- layout는 Conversation side panel 기준으로 정리
- surface language는 tinted 성향 우선
- typography mood는 utilitarian 축 유지
- density는 airy 기준으로 primitive spacing 조정
- palette temperature는 unknown 쪽을 우선
- Avoid: playful pastel consumer chat
- Avoid: streetwear drop hero
- Avoid: editorial magazine cover
- Avoid: d2c product grid

## 8. Component Strategy

- **Product primitives**: workspace header, project switcher, thread list sidebar, thread item, chat message, ai message, user message, prompt composer, streaming cursor, regenerate button, stop generation button, compliance-artifact panel, audit-trail timeline, policy-check badge, compliance warning modal, citation footnote, source reference card, reviewer assignment chip, data retention indicator, empty conversation state
- **Required families**: button, data-display, editorial, feedback, input, marketing, navigation, commerce, copilot-artifact, copilot-chat, document, overlay, social, layout, workflow
- **Advanced component recommendations**:

- **resizable-split-pane** (layout, score 28): primary work happens between list, canvas/chat, and detail panels; users need to compare or inspect adjacent information without navigation / pairs with: thread-list, artifact-preview-panel, inspector-drawer
- **citation-drawer** (copilot-artifact, score 26): answers must show supporting policy, document, or source records; users need to inspect evidence without losing conversation context / pairs with: inline-citation, source-card, evidence-graph
- **decision-record-card** (data-display, score 23): a reviewer or AI-assisted workflow reaches a durable decision; regulated teams need record ids and retention status / pairs with: audit-timeline, approval-rail, citation-drawer
- **policy-matrix** (data-display, score 23): multiple policy rules must be checked against multiple claims or fields; reviewers need dense scan-and-drill compliance status / pairs with: risk-summary-card, exception-queue, approval-rail
- **source-card** (copilot-artifact, score 23): AI output depends on external or internal source records; users need a repeatable citation preview component / pairs with: citation-drawer, evidence-graph, inline-citation
- **audit-timeline** (data-display, score 22): regulated workflows require traceable user and AI actions; reviewers need to reconstruct what happened before approval / pairs with: decision-record-card, approval-rail, tool-call-trace
- **diff-viewer** (document, score 22): AI rewrites, policy edits, or reviewer changes need auditability; users must approve what changed before publishing / pairs with: redline-viewer, revision-timeline, approval-rail
- **redline-viewer** (document, score 21): legal, compliance, or editorial text needs reviewer markup; comments must stay anchored to exact text ranges / pairs with: diff-viewer, comment-thread, approval-rail

- **Visual-reference archetypes**:

- **Conversation sidecar** (overlay / 0.94): chat-panel, message-thread, message-composer, context-drawer
- **Data review table** (data-display / 0.94): data-table, column-header, row-actions, filter-toolbar, pagination
- **Editorial content block** (editorial / 0.94): content-card, featured-story-card, section-header, content-meta, byline-row
- **Workspace shell** (navigation / 0.94): app-shell, sidebar-nav, workspace-switcher, breadcrumb, context-panel
- **Marketing hero stack** (marketing / 0.84): hero-section, hero-headline, hero-visual, cta-button-group, trust-strip

- **button**: primary-button, secondary-button, ghost-button, icon-button, cta-button, link-button, regenerate-button, stop-generation-button
- **data-display**: chat-message, chat-thread, comment-thread, tag, data-table, column-header, row-actions, stat-card / visual signals: Data review table (0.94)
- **editorial**: editor-canvas, editor-toolbar, inline-format-menu, slash-command-menu, block-controls, content-card, featured-story-card, content-meta / visual signals: Editorial content block (0.94)
- **feedback**: inline-alert, empty-state, toast, status-badge, empty-conversation-state, banner, step-progress, shortcut-hint
- **input**: text-field, search-field, segmented-control, chat-input, comment-input, chip, prompt-composer, textarea
- **marketing**: logo-cloud, customer-logo, metric-highlight, press-quote, faq-section, faq-item, faq-question, faq-answer / visual signals: Marketing hero stack (0.84)
- **navigation**: mobile-topbar, mobile-tab-bar, back-button, section-tabs, app-shell, sidebar-nav, topbar, breadcrumb / visual signals: Workspace shell (0.94)
- **commerce**: product-grid, product-card, product-detail, product-gallery, product-hero-image, image-thumbnail, price-tag, original-price-strikethrough
- **copilot-artifact**: message-artifact, artifact-preview-panel, draft-document, outline-sidebar, revision-timeline, reading-mode-toggle, citation-footnote, quote-block
- **copilot-chat**: streaming-cursor, typing-indicator, inline-citation, mention-chip, suggestion-card, thread-header
- **document**: article-body, table-of-contents, heading-anchor, prose-block, reading-pane, footnote, link-card, diff-viewer
- **overlay**: bottom-sheet, modal-dialog, mention-popup, confirm-dialog, user-menu, autocomplete, tooltip-guide, command-palette / visual signals: Conversation sidecar (0.94)
- **social**: feed-item, post-card, thread-view, reaction-bar, timeline-stream, avatar-cluster
- **layout**: resizable-split-pane
- **workflow**: approval-rail

## 9. Implementation Guardrails

- 기존 핵심 화면, 진입점, 작업 흐름은 명시적 승인 없이 제거하거나 숨기지 않음
- 전면 셸 리라이트보다 토큰 -> primitive -> feature surface 순서의 점진적 롤아웃을 우선
- 새 시각 규칙은 지원 대상 테마와 breakpoint 전체에서 먼저 검증
- 기존 데이터 밀도와 업무 완료 경로를 유지한 상태에서 시각 품질을 높이는 방향을 우선
- 기능 위치 변경, 정보 구조 변경, 패널 제거는 별도의 migration plan이 있을 때만 수행
- 레퍼런스는 형태·밀도·컴포넌트 비례만 흡수하고, 색 조합·폰트 스케일·도메인 IA는 토큰과 제품 온톨로지를 따른다
- 토큰을 사용하더라도 status/tint/info 역할을 섞어 레퍼런스처럼 보이는 새 팔레트를 만들지 않는다
- 구현 중 사용자·리뷰어가 반복 가능한 실패 패턴을 지적하면 현재 화면 수정에 그치지 않고 governance/contract/linter로 승격한다
- 아이콘 자리에 이모지(🎨 ✅ 🔥 등)를 넣지 않음 — SVG 아이콘 또는 아이콘 라이브러리만 사용
- 컴포넌트는 component_specs.md의 anatomy/states/token binding을 그대로 따라 완전히 구현
- 'TODO 컴포넌트', '임시 버튼', '플레이스홀더 카드' 같은 반쪽 구현을 남기지 않음

## 10. Reference Absorption Rule

- Analysed live reference sources: 3
- Rule: copy visuals from no single source; absorb patterns only when they reinforce brand keywords and avoid anti-keywords.
- Use references to validate structure, accessibility, token discipline, and documentation quality.
- Scope rule: Visual references are morphology inputs only; tokens, component specs, and product IA remain authoritative.
- Allowed from references:
  - component morphology
  - layout density
  - panel/card proportions
  - hierarchy rhythm
  - interaction affordance patterns
- Denied from references:
  - color palette
  - palette composition or derived secondary palettes
  - typography family or scale
  - semantic status colors
  - product copy
  - product data model
  - navigation labels
  - domain information architecture
  - redistributable imagery unless explicitly licensed
- Promoted failure patterns:
  - **token-bound-reference-palette-mixing**: Token binding is necessary but not sufficient; color role composition must still follow the ontology palette roles. Prevention: Derived colors may alias a semantic token or mix one semantic role with a neutral surface/transparent value. Do not mix multiple chromatic roles to create a local palette.
- Feedback promotion: When implementation review identifies a repeatable design-system failure, promote it into governance, generated artifacts, and lint checks before treating the current screen as complete. Outputs: design_system_blueprint.governance, system_spec.md, system_ontology.json, IMPLEMENTATION_CONTRACT.md

## 11. AI Synthesis Principles

- **hex를 만들지 않는다**: AI는 색상 hex 값을 임의로 생성하지 않는다. 반드시 color_reference, CSS 추출, 브랜드 가이드 등 실증 소스에서 가져온 값만 사용한다.
- **토큰명을 만들지 않는다**: AI는 토큰 이름을 임의로 발명하지 않는다. 네이밍 패턴(core/semantic/component 레이어 규칙)은 정의하되, 구체적 토큰명은 실제 컴포넌트와 역할에서 도출한다.
- **팩트 위에 해석만**: AI는 수집된 레퍼런스, 프로필, 온톨로지 증거 위에 해석과 구조화만 수행한다. 증거 없는 추론, 존재하지 않는 패턴 서술, 가상의 사용 사례 생성을 금지한다.
- **이모지를 UI 요소로 쓰지 않는다**: AI는 아이콘, 상태 표시, 버튼 장식, 네비게이션 지표 등 UI 컴포넌트 자리에 이모지(🎨 ✅ 🔥 ⚡ 🚀 ❌ ⭐ 📊 등)를 절대 넣지 않는다. 반드시 SVG 아이콘 컴포넌트를 직접 구현하거나, 아이콘 라이브러리(Lucide, Heroicons, Phosphor, Tabler 등)를 import해서 사용한다. 이모지는 본문 콘텐츠(예: 블로그 텍스트, 사용자 입력)에서만 허용되며, 시스템 UI 요소로는 금지한다. 이 규칙은 AI가 UI를 만들 때 가장 자주 저지르는 실수이므로 엄격히 적용한다.
- **컴포넌트를 직접 구현한다**: AI는 '임시 버튼', '플레이스홀더 카드', 'TODO 컴포넌트' 같은 반쪽 구현을 남기지 않는다. system_spec.md의 Component Strategy와 component_specs.md에 정의된 구조(anatomy), 상태(states), 토큰 바인딩, 접근성 규칙을 그대로 따라 완전한 컴포넌트를 구현한다. 기존 라이브러리 컴포넌트를 그냥 import해서 쓰는 대신, 디자인 시스템 토큰으로 스타일을 명시적으로 바인딩한다.

## 12. Ontology Targets

- **component**: 121
- **design_system**: 68
- **layout**: 42
- **content**: 36
- **accessibility**: 35
- **color**: 35
- **pattern**: 35
- **iconography**: 30

## 13. Profile Validation

- Warning: [pitfall#3-rebrand] Classic Blue vs Misty Blue (blue): lightness diff 53, saturation diff 22 — possible rebrand remnant
- Warning: visual_reference.sources is empty

## 14. Quick Start

이 문서는 **Mercer System**의 디자인 시스템 사양입니다.

### 시작하기

1. **토큰 적용**: Drop-in CSS(아래 섹션 16)의 CSS 변수를 프로젝트에 복사합니다.
2. **컬러 세팅**: Color Reference(섹션 6)의 semantic role을 기준으로 surface/text/border를 잡습니다.
3. **타이포 세팅**: Token Strategy(섹션 5)의 font family와 type scale을 적용합니다.
4. **시각 방향 확인**: Visual Reference Signals(섹션 7)에서 density/surface/layout cue를 먼저 확인합니다.
5. **컴포넌트 구현**: Component Strategy(섹션 8)의 family 순서대로 하나씩 빌드합니다.

### 우선순위

핵심 primitive: **workspace header, project switcher, thread list sidebar, thread item, chat message**

이 primitive를 지원하는 컴포넌트부터 구현하고, 나머지는 필요에 따라 확장합니다.

## 15. DO / DON'T

### DO

- **Conversation-Copilot**: conversation-copilot와 충돌하는 컴포넌트 변형은 만들지 않기
- **Enterprise-Chatbot**: enterprise-chatbot와 충돌하는 컴포넌트 변형은 만들지 않기
- **Corporate-Trust**: corporate-trust와 충돌하는 컴포넌트 변형은 만들지 않기
- **Finance**: finance와 충돌하는 컴포넌트 변형은 만들지 않기
- 모든 시각적 선택에서 **conversation-copilot, enterprise-chatbot, corporate-trust** 기준을 적용
- semantic token을 통해 컬러를 적용 (하드코딩 금지)
- 접근성 기준을 모든 text/surface 조합에서 먼저 검증
- 컴포넌트 변형 추가 전 기존 variant로 해결 가능한지 먼저 확인
- 아이콘은 SVG 컴포넌트 또는 Lucide/Heroicons/Phosphor/Tabler 등 라이브러리로 구현
- component_specs.md의 anatomy/states/token binding을 그대로 따라 완전히 구현

### DON'T

- **playful-pastel** 방향의 디자인 결정을 하지 않음
- **streetwear-drop** 방향의 디자인 결정을 하지 않음
- **editorial-warm-serif** 방향의 디자인 결정을 하지 않음
- **bold-saturated-marketing** 방향의 디자인 결정을 하지 않음
- hex 값을 임의로 생성하지 않음 (반드시 레퍼런스에서 가져오기)
- 토큰명을 임의로 발명하지 않음 (네이밍 패턴에서 도출)
- 한 레퍼런스의 비주얼을 그대로 복제하지 않음
- 기존 기능 진입점을 승인 없이 제거하지 않음
- **이모지(🎨 ✅ 🔥 ⚡ 🚀 ❌ ⭐ 📊 등)를 아이콘/버튼/상태 표시로 절대 쓰지 않음** — 본문 콘텐츠에만 허용
- '임시 버튼', 'TODO 컴포넌트', '플레이스홀더 카드' 같은 반쪽 구현을 남기지 않음
- 라이브러리 컴포넌트를 기본 스타일로 그냥 쓰지 않음 — 반드시 디자인 토큰으로 스타일 바인딩

## 16. Drop-in CSS

아래 CSS 변수를 `:root`에 복사하여 즉시 사용할 수 있습니다.

```css
:root {
  /* --- Spacing --- */
  --space-0: 0px;
  --space-2: 2px;
  --space-4: 4px;
  --space-8: 8px;
  --space-12: 12px;
  --space-16: 16px;
  --space-24: 24px;
  --space-32: 32px;
  --space-48: 48px;
  --space-64: 64px;
  --space-96: 96px;

  /* --- Radius --- */
  --radius-none: 0;
  --radius-sm: 4px;
  --radius-md: 8px;
  --radius-lg: 12px;
  --radius-xl: 16px;
  --radius-pill: 9999px;

  /* --- Typography --- */
  --font-heading: 'Pretendard', serif;
  --font-body: 'Pretendard', sans-serif;
  --font-mono: 'IBM Plex Mono', monospace;
  --text-xs: 12px;
  --text-sm: 13px;
  --text-md: 15px;
  --text-lg: 19px;
  --text-xl: 24px;
  --text-2xl: 30px;
  --text-3xl: 37px;

  --leading-tight: 1.25;
  --leading-normal: 1.45;
  --leading-comfortable: 1.55;
  --leading-relaxed: 1.65;

  /* --- Color (from reference) --- */
  --color-primary: #0071A8;
  --color-accent: #B87333;
  --color-surface-tint: #B0E0E6;

  /* --- Semantic roles (expanded) --- */
  --color-brand-primary: #0071A8;
  --color-brand-accent: #B87333;
  --color-surface-tint: #B0E0E6;
  --color-canvas: #F7F8FA;
  --color-surface: #FFFFFF;
  --color-surface-muted: #EEF1F6;
  --color-surface-elevated: #FFFFFF;
  --color-border: #C4C4C4;
  --color-border-strong: #C0C0C0;
  --color-ink: #111111;
  --color-ink-muted: #6B6F74;
  --color-ink-subtle: #6B7280;
  --color-ink-inverse: #FFFFFF;
  --color-primary-support: #2C3E50;
  --color-accent-support: #F6F1E7;
  --color-info: #2C3E50;
  --color-success: #4A7C59;
  --color-warning: #B87333;
  --color-danger: #8B2252;
  --color-link: #0071A8;
  --color-link-hover: #00567F;

  /* --- Button — primary --- */
  --color-button-primary-surface-default: #0071A8;
  --color-button-primary-surface-hover: #005C89;
  --color-button-primary-surface-active: #004F75;
  --color-button-primary-surface-disabled: #94C2D9;
  --color-button-primary-text-default: #FFFFFF;
  --color-button-primary-text-disabled: #FBFCFC;
  --color-button-primary-border-default: #0071A8;
  --color-button-primary-focus-ring: #0071A8;

  /* --- Button — secondary --- */
  --color-button-secondary-surface-default: #FFFFFF;
  --color-button-secondary-surface-hover: #F1F1F1;
  --color-button-secondary-surface-active: #E7E7E7;
  --color-button-secondary-surface-disabled: #F7F8FA;
  --color-button-secondary-text-default: #111111;
  --color-button-secondary-text-disabled: #909091;
  --color-button-secondary-border-default: #B0B0B0;
  --color-button-secondary-border-hover: #9B9B9B;
  --color-button-secondary-focus-ring: #0071A8;

  /* --- Button — ghost --- */
  --color-button-ghost-surface-default: transparent;
  --color-button-ghost-surface-hover: #F3F3F3;
  --color-button-ghost-surface-active: #EAEAEA;
  --color-button-ghost-surface-disabled: transparent;
  --color-button-ghost-text-default: #6B6F74;
  --color-button-ghost-text-hover: #111111;
  --color-button-ghost-text-disabled: #B8BABE;
  --color-button-ghost-border-default: transparent;
  --color-button-ghost-focus-ring: #0071A8;

  /* --- Button — danger --- */
  --color-button-danger-surface-default: #8B2252;
  --color-button-danger-surface-hover: #721C43;
  --color-button-danger-surface-active: #62183A;
  --color-button-danger-text-default: #FFFFFF;
  --color-button-danger-border-default: #8B2252;
  --color-button-danger-focus-ring: #8B2252;

  /* --- Input --- */
  --color-input-surface-default: #FFFFFF;
  --color-input-surface-filled: #FFFFFF;
  --color-input-surface-disabled: #F7F8FA;
  --color-input-text-default: #111111;
  --color-input-text-placeholder: #A3A6AA;
  --color-input-text-disabled: #B8BABE;
  --color-input-border-default: #C4C4C4;
  --color-input-border-hover: #ABABAB;
  --color-input-border-focus: #0071A8;
  --color-input-border-error: #8B2252;
  --color-input-border-disabled: #D1D1D1;

  /* --- Card --- */
  --color-card-surface-default: #FFFFFF;
  --color-card-surface-hover: #FAFAFA;
  --color-card-surface-muted: #F7F8FA;
  --color-card-border-default: #C4C4C4;
  --color-card-border-hover: #ABABAB;
  --color-card-border-focus: #0071A8;

  /* --- Nav link --- */
  --color-nav-link-text-default: #6B6F74;
  --color-nav-link-text-hover: #111111;
  --color-nav-link-text-active: #0071A8;
  --color-nav-link-surface-hover: #F5F5F5;
  --color-nav-link-indicator: #B87333;

  /* --- Link --- */
  --color-link-text-default: #0071A8;
  --color-link-text-hover: #004F75;
  --color-link-text-visited: #0E5B80;

  /* --- Feedback — info --- */
  --color-feedback-info-surface: #E6E8EA;
  --color-feedback-info-text: #2C3E50;
  --color-feedback-info-border: #697683;
  --color-feedback-info-icon: #2C3E50;

  /* --- Feedback — success --- */
  --color-feedback-success-surface: #E9EFEB;
  --color-feedback-success-text: #4A7C59;
  --color-feedback-success-border: #7EA189;
  --color-feedback-success-icon: #4A7C59;

  /* --- Feedback — warning --- */
  --color-feedback-warning-surface: #F6EEE7;
  --color-feedback-warning-text: #B87333;
  --color-feedback-warning-border: #CB9B6F;
  --color-feedback-warning-icon: #B87333;

  /* --- Feedback — danger --- */
  --color-feedback-danger-surface: #F1E4EA;
  --color-feedback-danger-text: #8B2252;
  --color-feedback-danger-border: #AB6284;
  --color-feedback-danger-icon: #8B2252;

  /* --- Motion --- */
  --duration-0: 0ms;
  --duration-80: 80ms;
  --duration-120: 120ms;
  --duration-180: 180ms;
  --duration-240: 240ms;
  --duration-320: 320ms;
  --ease-standard: cubic-bezier(0.4, 0, 0.2, 1);
  --ease-enter: cubic-bezier(0, 0, 0.2, 1);
  --ease-exit: cubic-bezier(0.4, 0, 1, 1);
  --ease-emphasized: cubic-bezier(0.2, 0, 0, 1);
}
```

## 17. CSS Extraction Summary

- CSS 추출 데이터 없음 (크롤링 시 CSS가 수집되지 않았거나 extract-css가 실행되지 않음)

## 18. Component-Token Map

| Component | Tokens Used |
|-----------|-------------|
| activity-card | `color.Powder Blue→background`, `spacing.12→padding`, `radius.md→radius` |
| add-to-cart-button | `color.Super Sonic→surface`, `color.Copper→emphasis`, `color.Powder Blue→background`, `spacing.12→padding`, `radius.md→radius` |
| app-shell | `color.Super Sonic→surface`, `color.Copper→emphasis`, `color.Powder Blue→background`, `spacing.12→padding`, `radius.md→radius` |
| approval-rail | `color.Powder Blue→background`, `spacing.12→padding`, `radius.md→radius` |
| article-body | `color.Powder Blue→background`, `spacing.12→padding`, `radius.md→radius` |
| artifact-preview-panel | `color.Powder Blue→background`, `spacing.12→padding`, `radius.md→radius` |
| audit-timeline | `color.Powder Blue→background`, `spacing.12→padding`, `radius.md→radius` |
| autocomplete | `color.Super Sonic→surface`, `color.Copper→emphasis`, `color.Powder Blue→background`, `spacing.12→padding`, `radius.md→radius` |
| avatar | `color.Powder Blue→background`, `spacing.12→padding`, `radius.md→radius` |
| avatar-cluster | `color.Powder Blue→background`, `spacing.12→padding`, `radius.md→radius` |
| back-button | `color.Super Sonic→surface`, `color.Copper→emphasis`, `color.Powder Blue→background`, `spacing.12→padding`, `radius.md→radius` |
| banner | `color.Powder Blue→background`, `spacing.12→padding`, `radius.md→radius` |
| block-controls | `color.Powder Blue→background`, `spacing.12→padding`, `radius.md→radius` |
| bottom-sheet | `color.Super Sonic→surface`, `color.Copper→emphasis`, `color.Powder Blue→background`, `spacing.12→padding`, `radius.md→radius` |
| breadcrumb | `color.Super Sonic→surface`, `color.Copper→emphasis`, `color.Powder Blue→background`, `spacing.12→padding`, `radius.md→radius` |
| byline-row | `color.Powder Blue→background`, `spacing.12→padding`, `radius.md→radius` |
| calendar-grid | `color.Powder Blue→background`, `spacing.12→padding`, `radius.md→radius` |
| category-pill | `color.Super Sonic→surface`, `color.Copper→emphasis`, `color.Powder Blue→background`, `spacing.12→padding`, `radius.md→radius` |
| chart-container | `color.Powder Blue→background`, `spacing.12→padding`, `radius.md→radius` |
| chart-legend | `color.Powder Blue→background`, `spacing.12→padding`, `radius.md→radius` |
| chart-tooltip | `color.Super Sonic→surface`, `color.Copper→emphasis`, `color.Powder Blue→background`, `spacing.12→padding`, `radius.md→radius` |
| chat-input | `color.Super Sonic→surface`, `color.Copper→emphasis`, `color.Powder Blue→background`, `spacing.12→padding`, `radius.md→radius` |
| chat-message | `color.Powder Blue→background`, `spacing.12→padding`, `radius.md→radius` |
| chat-panel | `color.Super Sonic→surface`, `color.Copper→emphasis`, `color.Powder Blue→background`, `spacing.12→padding`, `radius.md→radius` |
| chat-thread | `color.Powder Blue→background`, `spacing.12→padding`, `radius.md→radius` |
| checkbox | `color.Super Sonic→surface`, `color.Copper→emphasis`, `color.Powder Blue→background`, `spacing.12→padding`, `radius.md→radius` |
| chip | `color.Super Sonic→surface`, `color.Copper→emphasis`, `color.Powder Blue→background`, `spacing.12→padding`, `radius.md→radius` |
| citation-drawer | `color.Powder Blue→background`, `spacing.12→padding`, `radius.md→radius` |
| citation-footnote | `color.Powder Blue→background`, `spacing.12→padding`, `radius.md→radius` |
| color-swatch-selector | `color.Super Sonic→surface`, `color.Copper→emphasis`, `color.Powder Blue→background`, `spacing.12→padding`, `radius.md→radius` |
| column-header | `color.Powder Blue→background`, `spacing.12→padding`, `radius.md→radius` |
| command-palette | `color.Super Sonic→surface`, `color.Copper→emphasis`, `color.Powder Blue→background`, `spacing.12→padding`, `radius.md→radius` |
| command-result-item | `color.Super Sonic→surface`, `color.Copper→emphasis`, `color.Powder Blue→background`, `spacing.12→padding`, `radius.md→radius` |
| comment-input | `color.Super Sonic→surface`, `color.Copper→emphasis`, `color.Powder Blue→background`, `spacing.12→padding`, `radius.md→radius` |
| comment-thread | `color.Powder Blue→background`, `spacing.12→padding`, `radius.md→radius` |
| confirm-dialog | `color.Super Sonic→surface`, `color.Copper→emphasis`, `color.Powder Blue→background`, `spacing.12→padding`, `radius.md→radius` |
| content-card | `color.Powder Blue→background`, `spacing.12→padding`, `radius.md→radius` |
| content-meta | `color.Powder Blue→background`, `spacing.12→padding`, `radius.md→radius` |
| context-drawer | `color.Super Sonic→surface`, `color.Copper→emphasis`, `color.Powder Blue→background`, `spacing.12→padding`, `radius.md→radius` |
| context-panel | `color.Super Sonic→surface`, `color.Copper→emphasis`, `color.Powder Blue→background`, `spacing.12→padding`, `radius.md→radius` |
| cross-sell-grid | `color.Powder Blue→background`, `spacing.12→padding`, `radius.md→radius` |
| cta-button | `color.Super Sonic→surface`, `color.Copper→emphasis`, `color.Powder Blue→background`, `spacing.12→padding`, `radius.md→radius` |
| cta-button-group | `color.Powder Blue→background`, `spacing.12→padding`, `radius.md→radius` |
| customer-logo | `color.Powder Blue→background`, `spacing.12→padding`, `radius.md→radius` |
| data-table | `color.Powder Blue→background`, `spacing.12→padding`, `radius.md→radius` |
| date-picker | `color.Super Sonic→surface`, `color.Copper→emphasis`, `color.Powder Blue→background`, `spacing.12→padding`, `radius.md→radius` |
| date-range-picker | `color.Super Sonic→surface`, `color.Copper→emphasis`, `color.Powder Blue→background`, `spacing.12→padding`, `radius.md→radius` |
| decision-record-card | `color.Powder Blue→background`, `spacing.12→padding`, `radius.md→radius` |
| diff-viewer | `color.Powder Blue→background`, `spacing.12→padding`, `radius.md→radius` |
| discount-badge | `color.Powder Blue→background`, `spacing.12→padding`, `radius.md→radius` |
| draft-document | `color.Powder Blue→background`, `spacing.12→padding`, `radius.md→radius` |
| editor-canvas | `color.Powder Blue→background`, `spacing.12→padding`, `radius.md→radius` |
| editor-toolbar | `color.Powder Blue→background`, `spacing.12→padding`, `radius.md→radius` |
| empty-conversation-state | `color.Powder Blue→background`, `spacing.12→padding`, `radius.md→radius` |
| empty-feed-illustration | `color.Powder Blue→background`, `spacing.12→padding`, `radius.md→radius` |
| empty-state | `color.Powder Blue→background`, `spacing.12→padding`, `radius.md→radius` |
| faq-answer | `color.Powder Blue→background`, `spacing.12→padding`, `radius.md→radius` |
| faq-item | `color.Powder Blue→background`, `spacing.12→padding`, `radius.md→radius` |
| faq-question | `color.Powder Blue→background`, `spacing.12→padding`, `radius.md→radius` |
| faq-section | `color.Powder Blue→background`, `spacing.12→padding`, `radius.md→radius` |
| feature-comparison | `color.Powder Blue→background`, `spacing.12→padding`, `radius.md→radius` |
| featured-story-card | `color.Powder Blue→background`, `spacing.12→padding`, `radius.md→radius` |
| feed-item | `color.Powder Blue→background`, `spacing.12→padding`, `radius.md→radius` |
| file-preview | `color.Powder Blue→background`, `spacing.12→padding`, `radius.md→radius` |
| filter-chip | `color.Super Sonic→surface`, `color.Copper→emphasis`, `color.Powder Blue→background`, `spacing.12→padding`, `radius.md→radius` |
| filter-panel | `color.Super Sonic→surface`, `color.Copper→emphasis`, `color.Powder Blue→background`, `spacing.12→padding`, `radius.md→radius` |
| filter-sidebar | `color.Super Sonic→surface`, `color.Copper→emphasis`, `color.Powder Blue→background`, `spacing.12→padding`, `radius.md→radius` |
| filter-toolbar | `color.Powder Blue→background`, `spacing.12→padding`, `radius.md→radius` |
| follow-button | `color.Super Sonic→surface`, `color.Copper→emphasis`, `color.Powder Blue→background`, `spacing.12→padding`, `radius.md→radius` |
| footnote | `color.Powder Blue→background`, `spacing.12→padding`, `radius.md→radius` |
| form-actions | `color.Super Sonic→surface`, `color.Copper→emphasis`, `color.Powder Blue→background`, `spacing.12→padding`, `radius.md→radius` |
| form-section | `color.Super Sonic→surface`, `color.Copper→emphasis`, `color.Powder Blue→background`, `spacing.12→padding`, `radius.md→radius` |
| gentle-toast | `color.Powder Blue→background`, `spacing.12→padding`, `radius.md→radius` |
| ghost-button | `color.Super Sonic→surface`, `color.Copper→emphasis`, `color.Powder Blue→background`, `spacing.12→padding`, `radius.md→radius` |
| heading-anchor | `color.Powder Blue→background`, `spacing.12→padding`, `radius.md→radius` |
| hero-headline | `color.Powder Blue→background`, `spacing.12→padding`, `radius.md→radius` |
| hero-section | `color.Powder Blue→background`, `spacing.12→padding`, `radius.md→radius` |
| hero-visual | `color.Powder Blue→background`, `spacing.12→padding`, `radius.md→radius` |
| icon-button | `color.Super Sonic→surface`, `color.Copper→emphasis`, `color.Powder Blue→background`, `spacing.12→padding`, `radius.md→radius` |
| image-thumbnail | `color.Powder Blue→background`, `spacing.12→padding`, `radius.md→radius` |
| inline-alert | `color.Powder Blue→background`, `spacing.12→padding`, `radius.md→radius` |
| inline-citation | `color.Powder Blue→background`, `spacing.12→padding`, `radius.md→radius` |
| inline-format-menu | `color.Powder Blue→background`, `spacing.12→padding`, `radius.md→radius` |
| insight-card | `color.Powder Blue→background`, `spacing.12→padding`, `radius.md→radius` |
| inspector-drawer | `color.Super Sonic→surface`, `color.Copper→emphasis`, `color.Powder Blue→background`, `spacing.12→padding`, `radius.md→radius` |
| kanban-board | `color.Powder Blue→background`, `spacing.12→padding`, `radius.md→radius` |
| kanban-card | `color.Powder Blue→background`, `spacing.12→padding`, `radius.md→radius` |
| kanban-column | `color.Powder Blue→background`, `spacing.12→padding`, `radius.md→radius` |
| link-button | `color.Super Sonic→surface`, `color.Copper→emphasis`, `color.Powder Blue→background`, `spacing.12→padding`, `radius.md→radius` |
| link-card | `color.Powder Blue→background`, `spacing.12→padding`, `radius.md→radius` |
| logo-cloud | `color.Powder Blue→background`, `spacing.12→padding`, `radius.md→radius` |
| mention-chip | `color.Powder Blue→background`, `spacing.12→padding`, `radius.md→radius` |
| mention-popup | `color.Super Sonic→surface`, `color.Copper→emphasis`, `color.Powder Blue→background`, `spacing.12→padding`, `radius.md→radius` |
| message-artifact | `color.Powder Blue→background`, `spacing.12→padding`, `radius.md→radius` |
| message-composer | `color.Super Sonic→surface`, `color.Copper→emphasis`, `color.Powder Blue→background`, `spacing.12→padding`, `radius.md→radius` |
| message-thread | `color.Super Sonic→surface`, `color.Copper→emphasis`, `color.Powder Blue→background`, `spacing.12→padding`, `radius.md→radius` |
| metric-highlight | `color.Powder Blue→background`, `spacing.12→padding`, `radius.md→radius` |
| mobile-tab-bar | `color.Super Sonic→surface`, `color.Copper→emphasis`, `color.Powder Blue→background`, `spacing.12→padding`, `radius.md→radius` |
| mobile-topbar | `color.Super Sonic→surface`, `color.Copper→emphasis`, `color.Powder Blue→background`, `spacing.12→padding`, `radius.md→radius` |
| modal-dialog | `color.Super Sonic→surface`, `color.Copper→emphasis`, `color.Powder Blue→background`, `spacing.12→padding`, `radius.md→radius` |
| new-thread-button | `color.Super Sonic→surface`, `color.Copper→emphasis`, `color.Powder Blue→background`, `spacing.12→padding`, `radius.md→radius` |
| original-price-strikethrough | `color.Powder Blue→background`, `spacing.12→padding`, `radius.md→radius` |
| outline-sidebar | `color.Powder Blue→background`, `spacing.12→padding`, `radius.md→radius` |
| pagination | `color.Super Sonic→surface`, `color.Copper→emphasis`, `color.Powder Blue→background`, `spacing.12→padding`, `radius.md→radius` |
| paragraph-block | `color.Powder Blue→background`, `spacing.12→padding`, `radius.md→radius` |
| player-controls | `color.Super Sonic→surface`, `color.Copper→emphasis`, `color.Powder Blue→background`, `spacing.12→padding`, `radius.md→radius` |
| policy-matrix | `color.Powder Blue→background`, `spacing.12→padding`, `radius.md→radius` |
| post-card | `color.Powder Blue→background`, `spacing.12→padding`, `radius.md→radius` |
| press-quote | `color.Powder Blue→background`, `spacing.12→padding`, `radius.md→radius` |
| prev-next-pager | `color.Super Sonic→surface`, `color.Copper→emphasis`, `color.Powder Blue→background`, `spacing.12→padding`, `radius.md→radius` |
| price-tag | `color.Powder Blue→background`, `spacing.12→padding`, `radius.md→radius` |
| pricing-card | `color.Powder Blue→background`, `spacing.12→padding`, `radius.md→radius` |
| primary-button | `color.Super Sonic→surface`, `color.Copper→emphasis`, `color.Powder Blue→background`, `spacing.12→padding`, `radius.md→radius` |
| product-card | `color.Powder Blue→background`, `spacing.12→padding`, `radius.md→radius` |
| product-detail | `color.Powder Blue→background`, `spacing.12→padding`, `radius.md→radius` |
| product-gallery | `color.Powder Blue→background`, `spacing.12→padding`, `radius.md→radius` |
| product-grid | `color.Powder Blue→background`, `spacing.12→padding`, `radius.md→radius` |
| product-hero-image | `color.Powder Blue→background`, `spacing.12→padding`, `radius.md→radius` |
| profile-card | `color.Powder Blue→background`, `spacing.12→padding`, `radius.md→radius` |
| prompt-composer | `color.Super Sonic→surface`, `color.Copper→emphasis`, `color.Powder Blue→background`, `spacing.12→padding`, `radius.md→radius` |
| prose-block | `color.Powder Blue→background`, `spacing.12→padding`, `radius.md→radius` |
| quick-view-modal | `color.Super Sonic→surface`, `color.Copper→emphasis`, `color.Powder Blue→background`, `spacing.12→padding`, `radius.md→radius` |
| quote-block | `color.Powder Blue→background`, `spacing.12→padding`, `radius.md→radius` |
| radio-group | `color.Super Sonic→surface`, `color.Copper→emphasis`, `color.Powder Blue→background`, `spacing.12→padding`, `radius.md→radius` |
| reaction-bar | `color.Powder Blue→background`, `spacing.12→padding`, `radius.md→radius` |
| reading-mode-toggle | `color.Powder Blue→background`, `spacing.12→padding`, `radius.md→radius` |
| reading-pane | `color.Powder Blue→background`, `spacing.12→padding`, `radius.md→radius` |
| redline-viewer | `color.Powder Blue→background`, `spacing.12→padding`, `radius.md→radius` |
| regenerate-button | `color.Super Sonic→surface`, `color.Copper→emphasis`, `color.Powder Blue→background`, `spacing.12→padding`, `radius.md→radius` |
| reply-composer | `color.Super Sonic→surface`, `color.Copper→emphasis`, `color.Powder Blue→background`, `spacing.12→padding`, `radius.md→radius` |
| resizable-split-pane | `color.Powder Blue→background`, `spacing.12→padding`, `radius.md→radius` |
| reviewer-assignment-picker | `color.Super Sonic→surface`, `color.Copper→emphasis`, `color.Powder Blue→background`, `spacing.12→padding`, `radius.md→radius` |
| revision-timeline | `color.Powder Blue→background`, `spacing.12→padding`, `radius.md→radius` |
| risk-summary-card | `color.Powder Blue→background`, `spacing.12→padding`, `radius.md→radius` |
| row-actions | `color.Powder Blue→background`, `spacing.12→padding`, `radius.md→radius` |
| search-field | `color.Super Sonic→surface`, `color.Copper→emphasis`, `color.Powder Blue→background`, `spacing.12→padding`, `radius.md→radius` |
| search-results | `color.Powder Blue→background`, `spacing.12→padding`, `radius.md→radius` |
| secondary-button | `color.Super Sonic→surface`, `color.Copper→emphasis`, `color.Powder Blue→background`, `spacing.12→padding`, `radius.md→radius` |
| section-header | `color.Powder Blue→background`, `spacing.12→padding`, `radius.md→radius` |
| section-tabs | `color.Super Sonic→surface`, `color.Copper→emphasis`, `color.Powder Blue→background`, `spacing.12→padding`, `radius.md→radius` |
| segmented-control | `color.Super Sonic→surface`, `color.Copper→emphasis`, `color.Powder Blue→background`, `spacing.12→padding`, `radius.md→radius` |
| select | `color.Super Sonic→surface`, `color.Copper→emphasis`, `color.Powder Blue→background`, `spacing.12→padding`, `radius.md→radius` |
| share-sheet | `color.Super Sonic→surface`, `color.Copper→emphasis`, `color.Powder Blue→background`, `spacing.12→padding`, `radius.md→radius` |
| shortcut-hint | `color.Powder Blue→background`, `spacing.12→padding`, `radius.md→radius` |
| sidebar-nav | `color.Super Sonic→surface`, `color.Copper→emphasis`, `color.Powder Blue→background`, `spacing.12→padding`, `radius.md→radius` |
| size-selector | `color.Super Sonic→surface`, `color.Copper→emphasis`, `color.Powder Blue→background`, `spacing.12→padding`, `radius.md→radius` |
| slash-command-menu | `color.Powder Blue→background`, `spacing.12→padding`, `radius.md→radius` |
| soft-dialog | `color.Super Sonic→surface`, `color.Copper→emphasis`, `color.Powder Blue→background`, `spacing.12→padding`, `radius.md→radius` |
| sort-dropdown | `color.Super Sonic→surface`, `color.Copper→emphasis`, `color.Powder Blue→background`, `spacing.12→padding`, `radius.md→radius` |
| source-card | `color.Powder Blue→background`, `spacing.12→padding`, `radius.md→radius` |
| stat-card | `color.Powder Blue→background`, `spacing.12→padding`, `radius.md→radius` |
| status-badge | `color.Powder Blue→background`, `spacing.12→padding`, `radius.md→radius` |
| step-progress | `color.Powder Blue→background`, `spacing.12→padding`, `radius.md→radius` |
| stop-generation-button | `color.Super Sonic→surface`, `color.Copper→emphasis`, `color.Powder Blue→background`, `spacing.12→padding`, `radius.md→radius` |
| streaming-cursor | `color.Powder Blue→background`, `spacing.12→padding`, `radius.md→radius` |
| suggestion-card | `color.Powder Blue→background`, `spacing.12→padding`, `radius.md→radius` |
| tab-bar | `color.Super Sonic→surface`, `color.Copper→emphasis`, `color.Powder Blue→background`, `spacing.12→padding`, `radius.md→radius` |
| table-of-contents | `color.Powder Blue→background`, `spacing.12→padding`, `radius.md→radius` |
| tag | `color.Powder Blue→background`, `spacing.12→padding`, `radius.md→radius` |
| tag-pill | `color.Powder Blue→background`, `spacing.12→padding`, `radius.md→radius` |
| text-field | `color.Super Sonic→surface`, `color.Copper→emphasis`, `color.Powder Blue→background`, `spacing.12→padding`, `radius.md→radius` |
| textarea | `color.Super Sonic→surface`, `color.Copper→emphasis`, `color.Powder Blue→background`, `spacing.12→padding`, `radius.md→radius` |
| thread-header | `color.Powder Blue→background`, `spacing.12→padding`, `radius.md→radius` |
| thread-view | `color.Powder Blue→background`, `spacing.12→padding`, `radius.md→radius` |
| time-picker | `color.Super Sonic→surface`, `color.Copper→emphasis`, `color.Powder Blue→background`, `spacing.12→padding`, `radius.md→radius` |
| timeline-stream | `color.Powder Blue→background`, `spacing.12→padding`, `radius.md→radius` |
| toast | `color.Powder Blue→background`, `spacing.12→padding`, `radius.md→radius` |
| tone-slider | `color.Super Sonic→surface`, `color.Copper→emphasis`, `color.Powder Blue→background`, `spacing.12→padding`, `radius.md→radius` |
| tooltip-guide | `color.Super Sonic→surface`, `color.Copper→emphasis`, `color.Powder Blue→background`, `spacing.12→padding`, `radius.md→radius` |
| topbar | `color.Super Sonic→surface`, `color.Copper→emphasis`, `color.Powder Blue→background`, `spacing.12→padding`, `radius.md→radius` |
| trust-strip | `color.Powder Blue→background`, `spacing.12→padding`, `radius.md→radius` |
| typing-indicator | `color.Powder Blue→background`, `spacing.12→padding`, `radius.md→radius` |
| upgrade-banner | `color.Powder Blue→background`, `spacing.12→padding`, `radius.md→radius` |
| upload-dropzone | `color.Super Sonic→surface`, `color.Copper→emphasis`, `color.Powder Blue→background`, `spacing.12→padding`, `radius.md→radius` |
| upload-progress | `color.Powder Blue→background`, `spacing.12→padding`, `radius.md→radius` |
| user-menu | `color.Super Sonic→surface`, `color.Copper→emphasis`, `color.Powder Blue→background`, `spacing.12→padding`, `radius.md→radius` |
| variant-selector | `color.Super Sonic→surface`, `color.Copper→emphasis`, `color.Powder Blue→background`, `spacing.12→padding`, `radius.md→radius` |
| video-player | `color.Powder Blue→background`, `spacing.12→padding`, `radius.md→radius` |
| volume-slider | `color.Super Sonic→surface`, `color.Copper→emphasis`, `color.Powder Blue→background`, `spacing.12→padding`, `radius.md→radius` |
| wishlist-toggle | `color.Super Sonic→surface`, `color.Copper→emphasis`, `color.Powder Blue→background`, `spacing.12→padding`, `radius.md→radius` |
| wizard-layout | `color.Super Sonic→surface`, `color.Copper→emphasis`, `color.Powder Blue→background`, `spacing.12→padding`, `radius.md→radius` |
| workspace-switcher | `color.Super Sonic→surface`, `color.Copper→emphasis`, `color.Powder Blue→background`, `spacing.12→padding`, `radius.md→radius` |

## 19. Contrast Audit

| Background | Foreground | Ratio | Level |
|------------|------------|-------|-------|
| Powder Blue | Ink | 13.17:1 | AAA (pass) |
| Super Sonic | Paper | 5.35:1 | AA (pass) |
| Copper | Ink | 4.98:1 | AA (pass) |
| Copper | Paper | 3.79:1 | AA-large (large-only) |
| Super Sonic | Powder Blue | 3.73:1 | AA-large (large-only) |
| Super Sonic | Ink | 3.53:1 | AA-large (large-only) |
| Copper | Powder Blue | 2.65:1 | fail (FAIL) |
| Powder Blue | Paper | 1.43:1 | fail (FAIL) |
| Super Sonic | Copper | 1.41:1 | fail (FAIL) |

## 20. Pattern Catalog

### Layout Patterns

- **workspace header**: —
- **project switcher**: —
- **thread list sidebar**: —
- **thread item**: —
- **chat message**: —
- **ai message**: —
- **user message**: —
- **prompt composer**: —
- **streaming cursor**: —
- **regenerate button**: —
- **stop generation button**: —
- **compliance-artifact panel**: —
- **audit-trail timeline**: —
- **policy-check badge**: —
- **compliance warning modal**: —
- **citation footnote**: —
- **source reference card**: —
- **reviewer assignment chip**: —
- **data retention indicator**: —
- **empty conversation state**: —
- **workspace navigation**: app-shell, sidebar-nav, topbar, breadcrumb, workspace-switcher, tab-bar, context-panel
- **dashboard cards**: stat-card, insight-card, activity-card, section-header
- **data tables**: data-table, column-header, filter-chip, row-actions, pagination, filter-toolbar

### Interaction Patterns

- **command palette**: command-palette, command-result-item, shortcut-hint
- **forms**: text-field, select, checkbox, textarea, form-section, radio-group, form-actions
- **notifications**: toast, inline-alert, empty-state, banner

## 21. Generated Visual Asset Plan

| Asset Slot | Model | Intended For | Manifest |
|------------|-------|--------------|----------|
| Brand-aligned raster image | imagine2 | only when the implementation surface would benefit from generated imagery | `public/generated/design-system/manifest.json` |
| Card thumbnail | imagine2 | activity-card, add-to-cart-button, category-pill, color-swatch-selector, content-card, cross-sell-grid | `public/generated/design-system/manifest.json` |
| Editorial cover | imagine2 | article-body, block-controls, byline-row, content-card, content-meta, editor-canvas | `public/generated/design-system/manifest.json` |
| Empty-state illustration | imagine2 | empty-state, step-progress, tooltip-guide, wizard-layout, feedback | `public/generated/design-system/manifest.json` |
| Hero image | imagine2 | cta-button-group, feature-comparison, featured-story-card, hero-headline, hero-section, hero-visual | `public/generated/design-system/manifest.json` |
