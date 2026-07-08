# ThreadSense Design System

## 1. Brand Concept

ThreadSense는 패션 큐레이션 모바일 앱이다. 사용자가 오늘의 상황, 취향, 보유 옷, 예산을 신호로 넘기면 상품 목록이 아니라 하나의 착장 에디트를 먼저 제안한다.

핵심 톤은 editorial, personal, tactile, decisive, refined다. 고급스러움을 검정/금색 클리셰로 처리하지 않고, 소재와 레이어, 추천 근거가 만져지는 화면으로 만든다.

## 2. Skeleton UI

첫 화면은 다음 순서를 유지한다.

1. Compact top bar: 위치, 날씨, 프로필 진입.
2. Taste signal rail: 상황, 날씨, 피하고 싶은 요소, 무드.
3. Outfit edit canvas: 실제 의류 이미지와 하나의 착장 결정.
4. Why this works: 소재, 실루엣, 보유 옷 연결 근거.
5. Garment stack: outer, top, bottom처럼 착장을 이루는 아이템.
6. Shop drawer: 착장 문맥에서 열리는 가격, 사이즈, 저장, 구매 후보 액션.
7. Bottom navigation: 오늘, 클로젯, 에딧, 쇼핑.

상품 그리드, 대시보드 카드, 마케팅 히어로는 첫 화면에서 금지한다.

## 3. Visual Tokens

Color roles:

- Canvas: `#f8f3ed`
- Paper: `#fffaf5`
- Surface muted: `#eee5dc`
- Ink: `#24191d`
- Muted ink: `#685d61`
- Primary claret: `#7f1734`
- Prussian blue: `#003153`
- Sage support: `#8fa38b`
- Flax accent: `#eedc82`

Typography:

- Display: `Noto Serif KR`
- Body/UI: `Pretendard`
- Letter spacing: `0`
- Korean wrapping: `word-break: keep-all`

Shape and spacing:

- Cards and panels use `8px` radius or less.
- Taste chips and segmented controls may use pill radius because they are controls, not content cards.
- Fixed mobile controls must keep stable hit targets: 36px minimum for chips, 44px for primary actions.

## 4. Component Set

Keep these as the first implementation surface:

- app shell
- compact top bar
- taste signal chip rail
- segmented control
- outfit edit canvas
- reason note
- garment row
- fabric swatch
- alternative rail
- shop drawer
- size chip group
- bottom navigation
- toast

Remove or defer generic dashboard, marketing, data table, hero CTA, and ecommerce grid components unless the app flow explicitly asks for them.

## 5. LLM Invocation Contract

This system should not select a preset. The calling LLM must derive the visual direction from the brand profile, domain objects, and skeleton UI.

Required decisions on every new app:

- Name the primary user job before choosing layout.
- Extract domain objects before choosing components.
- Define the first viewport contract before choosing visual polish.
- Translate colors into semantic roles instead of copying a palette.
- Keep component coverage from Astryx and Vercel Geist, but rewrite the visual identity for the product.
- Reject outputs that converge into the same card grid, dashboard, or landing-page hero.

## 6. Mock UI

The static mock lives in:

- `index.html`
- `styles.css`
- `app.js`

It implements the first-screen contract with a 390px-class mobile layout, real garment imagery, interactive taste chips, garment selection, a shop drawer preview, and a save toast.
