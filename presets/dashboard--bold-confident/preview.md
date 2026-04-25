# dashboard--bold-confident

## 어떤 제품에 맞나
- B2C 스타트업 운영 대시보드 — bold-confident 톤 vivid 팔레트, 한국어 1급

- app_mode: `dashboard` / brand_tone: `bold-confident`

## Color Tokens (light + dark)
### Core
- primary: `#5F4B8B`
- accent: `#F5DF4D`
- surface_tint: `#FFD7A0`

### Semantic
- success: `#4A7C59`
- warning: `#F5DF4D`
- danger: `#5F4B8B`
- info: `#4A6B8A`

> light/dark 변형은 어댑터(`nextjs-tailwind-shadcn` 등)가 파생. 원본 팔레트는 위 HEX 1세트.

## Typography
- heading: Spoqa Han Sans Neo
- body: Spoqa Han Sans Neo
- mono: JetBrains Mono
- korean: Spoqa Han Sans Neo

## 대표 컴포넌트
- **activation-funnel** — parts: container, header, content-area, footer(optional), action(optional) | states: default, loading, empty, error
- **experiment-panel** — parts: container, header, content-area, footer(optional), action(optional) | states: default, loading, empty, error
- **goal-tracker** — parts: container, header, content-area, footer(optional), action(optional) | states: default, loading, empty, error

## Locale Pairings
- ko: heading=Pretendard / body=Pretendard

## 주의사항
- image-derived hints는 advisory (truth source: system_spec.md, token_schema.json)
- 이 프리셋과 맞지 않으면 `brand_tone` 축을 바꿔 재시도
