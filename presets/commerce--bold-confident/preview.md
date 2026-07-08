# commerce--bold-confident

## 어떤 제품에 맞나
- 젊은 B2C 커머스 — bold-confident 톤 드롭·제품 그리드·장바구니·체크아웃, 한국어 1급

- app_mode: `commerce` / brand_tone: `bold-confident`

## Color Tokens (light + dark)
### Core
- primary: `#BD2E4A`
- accent: `#6C3BAA`
- surface_tint: `#F3E5AB`

### Semantic
- success: `#4A7C59`
- warning: `#EC5800`
- danger: `#BD2E4A`
- info: `#6C3BAA`

> light/dark 변형은 어댑터(`nextjs-tailwind-shadcn` 등)가 파생. 원본 팔레트는 위 HEX 1세트.

## Typography
- heading: Space Grotesk
- body: Inter
- mono: JetBrains Mono
- korean: Pretendard

## 대표 컴포넌트
- **product-detail** — parts: container, header, content-area, footer(optional), action(optional) | states: default, loading, empty, error
- **quick-view-modal** — parts: backdrop, container, header, content, footer(optional) | states: closed, opening, open, closing
- **product-grid** — parts: grid-container | states: default

## Locale Pairings
- ko: heading=Pretendard / body=Pretendard

## 주의사항
- image-derived hints는 advisory (truth source: system_spec.md, token_schema.json)
- 이 프리셋과 맞지 않으면 `brand_tone` 축을 바꿔 재시도
