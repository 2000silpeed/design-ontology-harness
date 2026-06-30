# LookMe Try-On System Spec

## 1. Positioning

- **Brand**: LookMe Toss In-App
- **Product**: Toss 인앱 환경에서 얼굴 사진, 바디 샘플, 실제 Colorfit 의류/소품 이미지 세트를 조합해 무료 얼굴 착장샷을 만들고, 크레딧 구매 후 내 아이템 착장샷을 생성하는 모바일 퍼널
- **Audience**: Toss 안에서 짧은 시간 안에 AI 얼굴 착장샷을 시험해보고 싶은 모바일 사용자, 자신의 옷과 소품 이미지를 등록해 착장샷을 만들어보고 싶은 유료 사용자, 개인정보와 얼굴 사진 처리에 민감하며 명확한 동의와 삭제 정책을 기대하는 사용자
- **Platforms**: mobile web, desktop browser preview
- **Accessibility floor**: WCAG 2.2 AA, 44px minimum touch target, 16px minimum form text, reduced motion friendly

## 2. Identity Guardrails

- **Brand keywords**: clear, fast, trustworthy, personal, curated, mobile-first
- **Anti-keywords**: shopping-mall, generic-fashion-commerce, overdecorated, dashboard-heavy, playful, luxury-editorial, neon, glassmorphism
- **Tone of voice**: concise, reassuring, direct, privacy-aware
- **Visual direction**: compact mobile funnel, real item image evidence, quiet financial-app trust, scan-first cards, clear step hierarchy, low elevation surfaces
- **Interaction direction**: single-primary-action, predictable forward flow, explicit paid boundary, fast selection, recoverable errors, touch-safe controls

## 3. Design Principles

- **Clear**: `clear`를 시각적 선택과 인터랙션 선택의 기본 기준으로 삼습니다.
- **Fast**: `fast`를 시각적 선택과 인터랙션 선택의 기본 기준으로 삼습니다.
- **Trust Through Consistency**: 예측 가능한 인터랙션과 안정적인 시각 언어로 신뢰를 쌓습니다.
- **Personal**: `personal`를 시각적 선택과 인터랙션 선택의 기본 기준으로 삼습니다.

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
- **Product type detected**: mobile
- **Pairing source**: auto-scored
- **Line height**: comfortable
- **Type scale**: base 14px, ratio 1.2 (xs=11px, sm=12px, md=14px, lg=17px, xl=20px, 2xl=24px, 3xl=29px)
- **Strategy**:
  - 단일 서체(Pretendard)로 weight 대비 위계 — 일관성 우선
  - 한글 서체: Pretendard — 라틴과 x-height/weight 조화
- **Heading note**: 한글 UI 서체의 사실상 표준. Apple SD Gothic Neo 기반이지만 더 정교함. 라틴은 Inter 계열.
- **Body note**: 한글 UI 서체의 사실상 표준. Apple SD Gothic Neo 기반이지만 더 정교함. 라틴은 Inter 계열.
- **Korean rationale**: Pretendard — 한글 UI 서체의 사실상 표준. 토스, 당근, 리디 등 국내 주요 서비스에서 사용. 자간이 자연스럽고 weight 전 구간에서 안정적.
- **Heading tracking**: xl=-0.01em, 2xl=-0.01em, 3xl=-0.01em
- **Primary script**: korean
- **Hangul headline defaults**: Pretendard | line-height 1.25-1.35 | tracking 0em
- **Hangul body defaults**: Pretendard | line-height 1.6-1.7 | label line-height 1.4-1.5
- **Wrap defaults**: headline word-break=keep-all, headline text-wrap=balance, body word-break=keep-all
- **Scale guidance**: 기본 스케일을 사용할 수 있지만 한글 문장 기준으로 실제 wrap을 먼저 검증한다.
- **Loading**: Pretendard(preload) | display: swap

## 6. Color Reference

- **Source**: REFERENCE X Vol.1 - Color Reference (/Users/sungwoon/ai-projects/design-ontology-harness/docs/color-reference.md)
- **Selection mode**: brand-guided
- **Preferred families**: Deep Blues, Standard Blues, Natural Greens, Pastel Blues
- **Palette strategy**: temperature=mixed, contrast=balanced, diversity=balanced, surface_style=tinted
- **Palette expansion**: supporting_color_count=8, combination_count=3, prefer_pairings=True
- **Active palette**: signature-1
- **Active roles**:
  - `primary` -> Navy Blue #000080 / Deep Blues
  - `accent` -> Ochre #CC7722 / Standard Oranges
  - `surface_tint` -> Wheat #F5DEB3 / Natural Yellows
- **Selected colors**:
  - Navy Blue #000080 / Deep Blues / 저명도, 중채도, 차가운 온도감이 강한 블루 계열 / 신뢰, 권위, 집중, 전문성, 절제된 우아함
  - Ochre #CC7722 / Standard Oranges / 중명도, 중채도, 흙기 섞인 따뜻한 오렌지 / 안정감, 내추럴, 신뢰감, 지속성
  - Wheat #F5DEB3 / Natural Yellows / 중명도, 저채도, 베이지 옐로 계열의 따뜻한 톤 / 따뜻함, 자연스러움, 부드러움, 안정감
- **Palette candidates**:
  - signature-1 (Signature): primary=Navy Blue, accent=Ochre, surface_tint=Wheat / Navy Blue is inside preferred families.; Ochre matches brand tone keywords.
  - assertive-3 (Assertive): primary=Navy Blue, accent=Ochre, surface_tint=Sky Blue / Navy Blue is inside preferred families.; Ochre matches brand tone keywords.
- **Expanded supporting colors**:
  - Classic Blue #0F4C81 / Pantone Trend Blues / reference-color / Classic Blue reinforces the brand mood signals.
  - Pairing #708090 #708090 / Derived Pairing / pairing-swatch / Pairing #708090 comes from the seed pairing references.; Pairing #708090 is explicitly paired with Navy Blue.
  - Pairing #FAF8F2 #FAF8F2 / Derived Pairing / pairing-swatch / Pairing #FAF8F2 comes from the seed pairing references.; Pairing #FAF8F2 is explicitly paired with Wheat.
  - Pairing #AFC8D9 #AFC8D9 / Derived Pairing / pairing-swatch / Pairing #AFC8D9 comes from the seed pairing references.; Pairing #AFC8D9 is explicitly paired with Wheat.
  - Pairing #B0C4DE #B0C4DE / Derived Pairing / pairing-swatch / Pairing #B0C4DE comes from the seed pairing references.; Pairing #B0C4DE is explicitly paired with Navy Blue.
  - Pairing #1C2E4A #1C2E4A / Derived Pairing / pairing-swatch / Pairing #1C2E4A comes from the seed pairing references.; Pairing #1C2E4A is explicitly paired with Ochre.
  - Pairing #4C7A77 #4C7A77 / Derived Pairing / pairing-swatch / Pairing #4C7A77 comes from the seed pairing references.; Pairing #4C7A77 is explicitly paired with Ochre.
  - Pairing #B6B995 #B6B995 / Derived Pairing / pairing-swatch / Pairing #B6B995 comes from the seed pairing references.; Pairing #B6B995 is explicitly paired with Ochre.
- **Expanded semantic roles**:
  - `brand_primary` -> Navy Blue #000080 / Deep Blues
  - `brand_accent` -> Ochre #CC7722 / Standard Oranges
  - `surface_tint` -> Wheat #F5DEB3 / Natural Yellows
  - `canvas` -> Canvas White #F7F8FA / Generated Fallback
  - `surface` -> Paper #FFFFFF / Generated Fallback
  - `surface_muted` -> Surface Muted #EEF1F6 / Generated Fallback
  - `surface_elevated` -> Paper #FFFFFF / Generated Fallback
  - `border` -> Border Neutral #D6DDE6 / Generated Fallback
  - `border_strong` -> Pairing #B6B995 #B6B995 / Derived Pairing
  - `ink` -> Pairing #1C2E4A #1C2E4A / Derived Pairing
- **Combination lists**:
  - Seed Core: primary=Navy Blue, accent=Ochre, surface_tint=Wheat
  - Surface System: canvas=Canvas White, surface=Paper, surface_tint=Wheat, border=Border Neutral, ink=Pairing #1C2E4A, ink_muted=Pairing #708090
  - Support Spectrum: support=Classic Blue, support=Pairing #708090, support=Pairing #FAF8F2, support=Pairing #AFC8D9, support=Pairing #B0C4DE, support=Pairing #1C2E4A
- **Notes**: Primary action should feel Toss-adjacent and trustworthy without copying Toss brand assets., Colorfit item photos carry fashion texture; UI chrome must stay quiet and legible., Avoid beige-only editorial palettes and purple-blue gradients.
- **Application rule**: 레퍼런스 컬러는 semantic token으로 번역해서 사용하고, 접근성과 theme 호환성을 우선합니다.

## 7. Visual Reference Signals

- **Mode**: local-images
- **Coverage**: source 3 / image 3 / selected 3
- **Rule**: visual references are advisory signals for motif and layout direction; official KB/spec remain the structural source of truth.
- **Provenance**: `observed` = directly measured from local pixels, `inferred` = synthesized from image/query/brand signals, `unverified` = reliable visual evidence not yet available.
- **Query seeds**: mobile fintech onboarding funnel, compact image selection cards, privacy consent mobile flow, mobile AI generation result viewer
### Visual Direction

- **Density**: airy (confidence 0.53, provenance inferred) / editorial x0.1, landing x2.4, hero x0.15
- **Surface Style**: tinted (confidence 0.24, provenance inferred) / editorial x0.1
- **Corner Style**: medium (confidence 0.24, provenance inferred) / fallback=medium
- **Typography Mood**: editorial (confidence 0.25, provenance inferred) / editorial x0.1
- **Color balance**: temperature=cool, contrast=high, neutral_bias=high, provenance=observed / dominant #FFFFFF, #F5F7FA, #4976D9

### Layout Rhythm

- **Narrative landing flow**: confidence 0.78 / provenance inferred / landing x2.4, hero x0.15, cta x0.9, marketing x0.15
- **Data review surface**: confidence 0.36 / provenance inferred / grid x0.9, audit x0.2
- **Editorial feed**: confidence 0.31 / provenance inferred / editorial x0.1
- **Split-pane workspace**: confidence 0.28 / provenance inferred / app x0.8

### Image-derived Component Hints

- **Cards**: low-elevation tinted cards를 기본으로 하고, 넓은 내부 여백과 강한 section breathing room. 중간 반경으로 제품 UI 절제 유지. / provenance inferred / surface=tinted, density=airy, corner=medium
- **Navigation**: 고정 sidebar 또는 split-pane navigation을 우선하고, 현재 위치와 scope를 항상 명시한다. / provenance inferred / Split-pane workspace
- **Typography**: headline rhythm과 본문 리듬의 대비를 키우고, label/metadata는 조용하게 유지한다. / provenance inferred / typography_mood=editorial
- **Data Display**: 정보 밀도를 유지하되 thin dividers와 restrained accent로 hierarchy를 만든다. / provenance inferred / layout=data-review-surface, density=airy
- **Hero**: 대형 hero와 trust strip, CTA cluster를 허용하되 과장된 glass/gradient 효과는 지양한다. / provenance inferred / Narrative landing flow

### Synthesis Notes

- layout는 Narrative landing flow 기준으로 정리
- surface language는 tinted 성향 우선
- typography mood는 editorial 축 유지
- density는 airy 기준으로 primitive spacing 조정
- palette temperature는 cool 쪽을 우선
- Avoid: marketing hero dominance after entry
- Avoid: nested cards
- Avoid: large decorative gradients
- Avoid: shopping price cards

### Design Context Pack

- **Activation**: grounded
- **Schema**: design-context-pack/v1
- **Rule**: Reference context is research input only; it never overrides product IA, tokens, component specs, or governance.
- **Providers**:
  - `local-images`: active / local-files / observed morphology evidence
  - `pinterest`: preview / manual-or-playwright-capture / search assist and shortlist support
  - `lazyweb`: suggested / mcp-or-manual-export / real app flow and screen corpus provider
- **Flow coverage**:
  - general-product-ui: covered (6 context cards; lazyweb, local-images)
  - onboarding: covered (1 context cards; lazyweb)
  - data-review: gap (0 context cards; no selected provider evidence)
  - empty-state: gap (0 context cards; no selected provider evidence)
  - pricing: gap (0 context cards; no selected provider evidence)
- **Context cards**:
  - `source-01-image-01` (visual-screen, observed): landing-mobile / flows: general-product-ui / morphology: general-interface-composition
  - `source-02-image-01` (visual-screen, observed): style-mobile / flows: general-product-ui / morphology: general-interface-composition
  - `source-03-image-01` (visual-screen, observed): result-mobile / flows: general-product-ui / morphology: general-interface-composition
  - `research-query-01` (research-query, planned): mobile fintech onboarding funnel / flows: onboarding / morphology: general-interface-composition
  - `research-query-02` (research-query, planned): compact image selection cards / flows: general-product-ui / morphology: general-interface-composition
- **Research gaps**:
  - real-app-corpus-provider-not-connected (medium): Connect Lazyweb MCP or export selected Lazyweb screens into visual_reference.sources with provenance.
  - flow-coverage-gaps (medium): Search corpus/provider screens by these flows before mock generation.

## 8. Component Strategy

- **Product primitives**: Toss short funnel landing, required and optional consent groups, face photo capture/upload, body sample selector, Colorfit real item image set selector, generation progress state, AI outfit result viewer, save and share actions, credit wallet and paywall, paid wardrobe item upload, wardrobe item grid, wardrobe generation flow, toast and error feedback
- **Required families**: button, copilot-artifact, data-display, document, editorial, feedback, input, marketing, navigation, commerce, overlay
- **Advanced component recommendations**:

- **bulk-action-table** (data-display, score 4): users handle many records at once; selection count and destructive actions must stay visible / pairs with: saved-view-bar, filter-builder, exception-queue
- **evidence-graph** (data-display, score 4): trust depends on seeing relationships between claims and sources; auditors need to trace why an answer or decision was made / pairs with: citation-drawer, decision-record-card, policy-matrix
- **citation-drawer** (copilot-artifact, score 2): answers must show supporting policy, document, or source records; users need to inspect evidence without losing conversation context / pairs with: inline-citation, source-card, evidence-graph
- **saved-view-bar** (navigation, score 2): teams revisit the same filtered views often; dense tools need stable scope memory / pairs with: filter-builder, bulk-action-table, exception-queue
- **source-card** (copilot-artifact, score 2): AI output depends on external or internal source records; users need a repeatable citation preview component / pairs with: citation-drawer, evidence-graph, inline-citation
- **redline-viewer** (document, score 1): legal, compliance, or editorial text needs reviewer markup; comments must stay anchored to exact text ranges / pairs with: diff-viewer, comment-thread, approval-rail

- **Visual-reference archetypes**:

- **Marketing hero stack** (marketing / 0.94): hero-section, hero-headline, hero-visual, cta-button-group, trust-strip
- **Review coverage system** (editorial / 0.67): review-card, score-badge, comparison-table, ranking-list, filter-chip

- **button**: primary-button, secondary-button, ghost-button, icon-button, cta-button, link-button, form-actions, hero-cta-group
- **copilot-artifact**: citation-drawer, source-card
- **data-display**: tag, data-table, column-header, row-actions, pricing-card, feature-comparison, kanban-board, kanban-column
- **document**: redline-viewer
- **editorial**: review-card, score-badge, comparison-table, ranking-list / visual signals: Review coverage system (0.67)
- **feedback**: inline-alert, empty-state, toast, status-badge, step-progress, banner, upgrade-banner, discount-badge
- **input**: text-field, search-field, segmented-control, textarea, select, checkbox, radio-group, form-section
- **marketing**: hero-container, hero-eyebrow, hero-headline, hero-subheadline, hero-visual, hero-trust-strip, hero-section, cta-button-group / visual signals: Marketing hero stack (0.94)
- **navigation**: mobile-topbar, mobile-tab-bar, back-button, section-tabs, pagination, app-shell, sidebar-nav, topbar
- **commerce**: product-grid, product-card, product-detail, product-gallery, product-hero-image, image-thumbnail, price-tag, original-price-strikethrough
- **overlay**: bottom-sheet, modal-dialog, tooltip-guide, quick-view-modal, command-palette, command-result-item, chart-tooltip, mention-popup

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

- No validation issues.

## 14. Quick Start

이 문서는 **LookMe Try-On System**의 디자인 시스템 사양입니다.

### 시작하기

1. **토큰 적용**: Drop-in CSS(아래 섹션 16)의 CSS 변수를 프로젝트에 복사합니다.
2. **컬러 세팅**: Color Reference(섹션 6)의 semantic role을 기준으로 surface/text/border를 잡습니다.
3. **타이포 세팅**: Token Strategy(섹션 5)의 font family와 type scale을 적용합니다.
4. **시각 방향 확인**: Visual Reference Signals(섹션 7)에서 density/surface/layout cue를 먼저 확인합니다.
5. **컴포넌트 구현**: Component Strategy(섹션 8)의 family 순서대로 하나씩 빌드합니다.

### 우선순위

핵심 primitive: **Toss short funnel landing, required and optional consent groups, face photo capture/upload, body sample selector, Colorfit real item image set selector**

이 primitive를 지원하는 컴포넌트부터 구현하고, 나머지는 필요에 따라 확장합니다.

## 15. DO / DON'T

### DO

- **Clear**: clear와 충돌하는 컴포넌트 변형은 만들지 않기
- **Fast**: fast와 충돌하는 컴포넌트 변형은 만들지 않기
- **Trust Through Consistency**: 일관된 disabled/error/success 패턴
- **Personal**: personal와 충돌하는 컴포넌트 변형은 만들지 않기
- 모든 시각적 선택에서 **clear, fast, trustworthy** 기준을 적용
- semantic token을 통해 컬러를 적용 (하드코딩 금지)
- 접근성 기준을 모든 text/surface 조합에서 먼저 검증
- 컴포넌트 변형 추가 전 기존 variant로 해결 가능한지 먼저 확인
- 아이콘은 SVG 컴포넌트 또는 Lucide/Heroicons/Phosphor/Tabler 등 라이브러리로 구현
- component_specs.md의 anatomy/states/token binding을 그대로 따라 완전히 구현

### DON'T

- **shopping-mall** 방향의 디자인 결정을 하지 않음
- **generic-fashion-commerce** 방향의 디자인 결정을 하지 않음
- **overdecorated** 방향의 디자인 결정을 하지 않음
- **dashboard-heavy** 방향의 디자인 결정을 하지 않음
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
  --text-xs: 11px;
  --text-sm: 12px;
  --text-md: 14px;
  --text-lg: 17px;
  --text-xl: 20px;
  --text-2xl: 24px;
  --text-3xl: 29px;

  --leading-tight: 1.25;
  --leading-normal: 1.4;
  --leading-comfortable: 1.5;
  --leading-relaxed: 1.6;

  /* --- Color (from reference) --- */
  --color-primary: #000080;
  --color-accent: #CC7722;
  --color-surface-tint: #F5DEB3;

  /* --- Semantic roles (expanded) --- */
  --color-brand-primary: #000080;
  --color-brand-accent: #CC7722;
  --color-surface-tint: #F5DEB3;
  --color-canvas: #F7F8FA;
  --color-surface: #FFFFFF;
  --color-surface-muted: #EEF1F6;
  --color-surface-elevated: #FFFFFF;
  --color-border: #D6DDE6;
  --color-border-strong: #B6B995;
  --color-ink: #1C2E4A;
  --color-ink-muted: #708090;
  --color-ink-subtle: #708090;
  --color-ink-inverse: #FFFFFF;
  --color-primary-support: #0F4C81;
  --color-accent-support: #CC7722;
  --color-info: #0F4C81;
  --color-success: #4A7C59;
  --color-warning: #CC7722;
  --color-danger: #8B2252;
  --color-link: #000080;
  --color-link-hover: #000057;

  /* --- Button — primary --- */
  --color-button-primary-surface-default: #000080;
  --color-button-primary-surface-hover: #000061;
  --color-button-primary-surface-active: #00004D;
  --color-button-primary-surface-disabled: #9495C9;
  --color-button-primary-text-default: #FFFFFF;
  --color-button-primary-text-disabled: #FBFCFC;
  --color-button-primary-border-default: #000080;
  --color-button-primary-focus-ring: #000080;

  /* --- Button — secondary --- */
  --color-button-secondary-surface-default: #FFFFFF;
  --color-button-secondary-surface-hover: #F1F2F4;
  --color-button-secondary-surface-active: #E8EAED;
  --color-button-secondary-surface-disabled: #F7F8FA;
  --color-button-secondary-text-default: #1C2E4A;
  --color-button-secondary-text-disabled: #949DAB;
  --color-button-secondary-border-default: #BDC8D7;
  --color-button-secondary-border-hover: #A3B3C7;
  --color-button-secondary-focus-ring: #000080;

  /* --- Button — ghost --- */
  --color-button-ghost-surface-default: transparent;
  --color-button-ghost-surface-hover: #F4F5F6;
  --color-button-ghost-surface-active: #EBECEF;
  --color-button-ghost-surface-disabled: transparent;
  --color-button-ghost-text-default: #708090;
  --color-button-ghost-text-hover: #1C2E4A;
  --color-button-ghost-text-disabled: #BAC2CA;
  --color-button-ghost-border-default: transparent;
  --color-button-ghost-focus-ring: #000080;

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
  --color-input-text-default: #1C2E4A;
  --color-input-text-placeholder: #A6B0BA;
  --color-input-text-disabled: #BAC2CA;
  --color-input-border-default: #D6DDE6;
  --color-input-border-hover: #B6C3D3;
  --color-input-border-focus: #000080;
  --color-input-border-error: #8B2252;
  --color-input-border-disabled: #E6EAF0;

  /* --- Card --- */
  --color-card-surface-default: #FFFFFF;
  --color-card-surface-hover: #FAFBFB;
  --color-card-surface-muted: #F7F8FA;
  --color-card-border-default: #D6DDE6;
  --color-card-border-hover: #B6C3D3;
  --color-card-border-focus: #000080;

  /* --- Nav link --- */
  --color-nav-link-text-default: #708090;
  --color-nav-link-text-hover: #1C2E4A;
  --color-nav-link-text-active: #000080;
  --color-nav-link-surface-hover: #F6F7F8;
  --color-nav-link-indicator: #CC7722;

  /* --- Link --- */
  --color-link-text-default: #000080;
  --color-link-text-hover: #00004D;
  --color-link-text-visited: #0A0A5C;

  /* --- Feedback — info --- */
  --color-feedback-info-surface: #E2EAF0;
  --color-feedback-info-text: #0F4C81;
  --color-feedback-info-border: #5580A5;
  --color-feedback-info-icon: #0F4C81;

  /* --- Feedback — success --- */
  --color-feedback-success-surface: #E9EFEB;
  --color-feedback-success-text: #4A7C59;
  --color-feedback-success-border: #7EA189;
  --color-feedback-success-icon: #4A7C59;

  /* --- Feedback — warning --- */
  --color-feedback-warning-surface: #F9EFE4;
  --color-feedback-warning-text: #CC7722;
  --color-feedback-warning-border: #D99E63;
  --color-feedback-warning-icon: #CC7722;

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
| activity-card | `color.Wheat→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| add-to-cart-button | `color.Navy Blue→surface`, `color.Ochre→emphasis`, `color.Wheat→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| app-shell | `color.Navy Blue→surface`, `color.Ochre→emphasis`, `color.Wheat→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| back-button | `color.Navy Blue→surface`, `color.Ochre→emphasis`, `color.Wheat→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| banner | `color.Wheat→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| bottom-sheet | `color.Navy Blue→surface`, `color.Ochre→emphasis`, `color.Wheat→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| breadcrumb | `color.Navy Blue→surface`, `color.Ochre→emphasis`, `color.Wheat→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| bulk-action-table | `color.Wheat→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| category-pill | `color.Navy Blue→surface`, `color.Ochre→emphasis`, `color.Wheat→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| chart-container | `color.Wheat→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| chart-legend | `color.Wheat→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| chart-tooltip | `color.Navy Blue→surface`, `color.Ochre→emphasis`, `color.Wheat→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| chat-input | `color.Navy Blue→surface`, `color.Ochre→emphasis`, `color.Wheat→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| chat-message | `color.Wheat→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| chat-thread | `color.Wheat→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| checkbox | `color.Navy Blue→surface`, `color.Ochre→emphasis`, `color.Wheat→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| chip | `color.Navy Blue→surface`, `color.Ochre→emphasis`, `color.Wheat→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| citation-drawer | `color.Wheat→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| color-swatch-selector | `color.Navy Blue→surface`, `color.Ochre→emphasis`, `color.Wheat→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| column-header | `color.Wheat→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| command-palette | `color.Navy Blue→surface`, `color.Ochre→emphasis`, `color.Wheat→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| command-result-item | `color.Navy Blue→surface`, `color.Ochre→emphasis`, `color.Wheat→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| comment-input | `color.Navy Blue→surface`, `color.Ochre→emphasis`, `color.Wheat→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| comment-thread | `color.Wheat→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| comparison-table | `color.Wheat→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| confirm-dialog | `color.Navy Blue→surface`, `color.Ochre→emphasis`, `color.Wheat→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| cross-sell-grid | `color.Wheat→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| cta-button | `color.Navy Blue→surface`, `color.Ochre→emphasis`, `color.Wheat→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| cta-button-group | `color.Wheat→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| data-table | `color.Wheat→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| discount-badge | `color.Wheat→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| empty-state | `color.Wheat→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| evidence-graph | `color.Wheat→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| feature-comparison | `color.Wheat→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| filter-chip | `color.Navy Blue→surface`, `color.Ochre→emphasis`, `color.Wheat→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| filter-sidebar | `color.Navy Blue→surface`, `color.Ochre→emphasis`, `color.Wheat→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| form-actions | `color.Navy Blue→surface`, `color.Ochre→emphasis`, `color.Wheat→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| form-section | `color.Navy Blue→surface`, `color.Ochre→emphasis`, `color.Wheat→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| ghost-button | `color.Navy Blue→surface`, `color.Ochre→emphasis`, `color.Wheat→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| hero-container | `color.Wheat→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| hero-cta-group | `color.Navy Blue→surface`, `color.Ochre→emphasis`, `color.Wheat→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| hero-eyebrow | `color.Wheat→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| hero-headline | `color.Wheat→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| hero-section | `color.Wheat→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| hero-subheadline | `color.Wheat→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| hero-trust-strip | `color.Wheat→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| hero-visual | `color.Wheat→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| icon-button | `color.Navy Blue→surface`, `color.Ochre→emphasis`, `color.Wheat→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| image-thumbnail | `color.Wheat→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| inline-alert | `color.Wheat→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| insight-card | `color.Wheat→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| kanban-board | `color.Wheat→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| kanban-card | `color.Wheat→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| kanban-column | `color.Wheat→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| link-button | `color.Navy Blue→surface`, `color.Ochre→emphasis`, `color.Wheat→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| mention-popup | `color.Navy Blue→surface`, `color.Ochre→emphasis`, `color.Wheat→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| mobile-tab-bar | `color.Navy Blue→surface`, `color.Ochre→emphasis`, `color.Wheat→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| mobile-topbar | `color.Navy Blue→surface`, `color.Ochre→emphasis`, `color.Wheat→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| modal-dialog | `color.Navy Blue→surface`, `color.Ochre→emphasis`, `color.Wheat→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| original-price-strikethrough | `color.Wheat→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| pagination | `color.Navy Blue→surface`, `color.Ochre→emphasis`, `color.Wheat→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| price-tag | `color.Wheat→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| pricing-card | `color.Wheat→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| primary-button | `color.Navy Blue→surface`, `color.Ochre→emphasis`, `color.Wheat→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| product-card | `color.Wheat→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| product-detail | `color.Wheat→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| product-gallery | `color.Wheat→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| product-grid | `color.Wheat→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| product-hero-image | `color.Wheat→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| quick-view-modal | `color.Navy Blue→surface`, `color.Ochre→emphasis`, `color.Wheat→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| radio-group | `color.Navy Blue→surface`, `color.Ochre→emphasis`, `color.Wheat→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| ranking-list | `color.Wheat→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| redline-viewer | `color.Wheat→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| review-card | `color.Wheat→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| row-actions | `color.Wheat→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| saved-view-bar | `color.Navy Blue→surface`, `color.Ochre→emphasis`, `color.Wheat→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| score-badge | `color.Wheat→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| search-field | `color.Navy Blue→surface`, `color.Ochre→emphasis`, `color.Wheat→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| secondary-button | `color.Navy Blue→surface`, `color.Ochre→emphasis`, `color.Wheat→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| section-header | `color.Wheat→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| section-tabs | `color.Navy Blue→surface`, `color.Ochre→emphasis`, `color.Wheat→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| segmented-control | `color.Navy Blue→surface`, `color.Ochre→emphasis`, `color.Wheat→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| select | `color.Navy Blue→surface`, `color.Ochre→emphasis`, `color.Wheat→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| shortcut-hint | `color.Wheat→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| sidebar-nav | `color.Navy Blue→surface`, `color.Ochre→emphasis`, `color.Wheat→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| size-selector | `color.Navy Blue→surface`, `color.Ochre→emphasis`, `color.Wheat→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| sort-dropdown | `color.Navy Blue→surface`, `color.Ochre→emphasis`, `color.Wheat→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| source-card | `color.Wheat→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| stat-card | `color.Wheat→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| status-badge | `color.Wheat→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| step-progress | `color.Wheat→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| tab-bar | `color.Navy Blue→surface`, `color.Ochre→emphasis`, `color.Wheat→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| tag | `color.Wheat→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| text-field | `color.Navy Blue→surface`, `color.Ochre→emphasis`, `color.Wheat→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| textarea | `color.Navy Blue→surface`, `color.Ochre→emphasis`, `color.Wheat→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| toast | `color.Wheat→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| tooltip-guide | `color.Navy Blue→surface`, `color.Ochre→emphasis`, `color.Wheat→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| topbar | `color.Navy Blue→surface`, `color.Ochre→emphasis`, `color.Wheat→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| trust-strip | `color.Wheat→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| upgrade-banner | `color.Wheat→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| variant-selector | `color.Navy Blue→surface`, `color.Ochre→emphasis`, `color.Wheat→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| wishlist-toggle | `color.Navy Blue→surface`, `color.Ochre→emphasis`, `color.Wheat→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |
| wizard-layout | `color.Navy Blue→surface`, `color.Ochre→emphasis`, `color.Wheat→background`, `spacing.12→padding`, `radius.md→radius`, `font:Pretendard` |

## 19. Contrast Audit

| Background | Foreground | Ratio | Level |
|------------|------------|-------|-------|
| Navy Blue | Paper | 16.01:1 | AAA (pass) |
| Wheat | Ink | 14.37:1 | AAA (pass) |
| Navy Blue | Wheat | 12.18:1 | AAA (pass) |
| Ochre | Ink | 5.60:1 | AA (pass) |
| Navy Blue | Ochre | 4.75:1 | AA (pass) |
| Ochre | Paper | 3.37:1 | AA-large (large-only) |
| Ochre | Wheat | 2.57:1 | fail (FAIL) |
| Wheat | Paper | 1.31:1 | fail (FAIL) |
| Navy Blue | Ink | 1.18:1 | fail (FAIL) |

## 20. Pattern Catalog

### Layout Patterns

- **Toss short funnel landing**: —
- **required and optional consent groups**: —
- **face photo capture/upload**: —
- **body sample selector**: —
- **Colorfit real item image set selector**: —
- **generation progress state**: —
- **AI outfit result viewer**: —
- **save and share actions**: —
- **credit wallet and paywall**: —
- **paid wardrobe item upload**: —
- **wardrobe item grid**: —
- **wardrobe generation flow**: —
- **toast and error feedback**: —
- **workspace navigation**: app-shell, sidebar-nav, topbar, breadcrumb, tab-bar
- **dashboard cards**: stat-card, insight-card, activity-card, section-header
- **data tables**: data-table, column-header, filter-chip, row-actions, pagination

### Interaction Patterns

- **command palette**: command-palette, command-result-item, shortcut-hint
- **forms**: text-field, select, checkbox, textarea, form-section, radio-group, form-actions
- **notifications**: toast, inline-alert, empty-state, banner

## 21. Generated Visual Asset Plan

| Asset Slot | Model | Intended For | Manifest |
|------------|-------|--------------|----------|
| Brand-aligned raster image | imagine2 | only when the implementation surface would benefit from generated imagery | `public/generated/design-system/manifest.json` |
| Card thumbnail | imagine2 | activity-card, add-to-cart-button, category-pill, color-swatch-selector, cross-sell-grid, discount-badge | `public/generated/design-system/manifest.json` |
| Editorial cover | imagine2 | comparison-table, ranking-list, review-card, score-badge, editorial, marketing | `public/generated/design-system/manifest.json` |
| Empty-state illustration | imagine2 | empty-state, step-progress, tooltip-guide, wizard-layout, feedback | `public/generated/design-system/manifest.json` |
| Hero image | imagine2 | cta-button-group, feature-comparison, hero-container, hero-cta-group, hero-eyebrow, hero-headline | `public/generated/design-system/manifest.json` |

## 22. Reference Intelligence Pack

- **Activation**: grounded / research gaps: 2
- **Allowed from references**: component morphology, layout density, panel/card proportions, hierarchy rhythm, interaction affordance patterns, flow pattern labels
- **Denied from references**: color palette, palette composition, typography scale, domain information architecture, product copy, redistributable imagery unless explicitly licensed

| Provider | Status | Access | Role |
|----------|--------|--------|------|
| Lazyweb MCP real-app corpus | suggested | mcp-or-manual-export | real app flow and screen corpus provider |
| Local visual references | active | local-files | observed morphology evidence |
| Pinterest-assisted capture | preview | manual-or-playwright-capture | search assist and shortlist support |

| Context | Provider | Provenance | Allowed Use |
|---------|----------|------------|-------------|
| compact image selection cards | Lazyweb MCP real-app corpus | planned | flows: general-product-ui; morphology: general-interface-composition |
| landing-mobile | Local visual references | observed | flows: general-product-ui; morphology: general-interface-composition |
| mobile AI generation result viewer | Lazyweb MCP real-app corpus | planned | flows: general-product-ui; morphology: general-interface-composition |
| mobile fintech onboarding funnel | Lazyweb MCP real-app corpus | planned | flows: onboarding; morphology: general-interface-composition |
| privacy consent mobile flow | Lazyweb MCP real-app corpus | planned | flows: general-product-ui; morphology: general-interface-composition |
| result-mobile | Local visual references | observed | flows: general-product-ui; morphology: general-interface-composition |
| style-mobile | Local visual references | observed | flows: general-product-ui; morphology: general-interface-composition |
