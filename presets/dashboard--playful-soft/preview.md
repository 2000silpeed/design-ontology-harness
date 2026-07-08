# dashboard--playful-soft

## 어떤 제품에 맞나
- consumer wellness/habit admin — playful-soft 톤 pastel 팔레트, 한국어 1급

- app_mode: `dashboard` / brand_tone: `playful-soft`

## Color Tokens (light + dark)
### Core
- primary: `#8E9AF1`
- accent: `#FFDAB9`
- surface_tint: `#E0B0FF`

### Semantic
- success: `#4A7C59`
- warning: `#FFDAB9`
- danger: `#FA8072`
- info: `#8E9AF1`

> light/dark 변형은 어댑터(`nextjs-tailwind-shadcn` 등)가 파생. 원본 팔레트는 위 HEX 1세트.

## Typography
- heading: Nunito
- body: Inter
- mono: JetBrains Mono
- korean: Pretendard

## 대표 컴포넌트
- **dashboard-card** — parts: container, inner-content | states: default, hover, focus-visible
- **streak-indicator** — parts: container, header, content-area, footer(optional), action(optional) | states: default, loading, empty, error
- **habit-calendar** — parts: container, header, content-area, footer(optional), action(optional) | states: default, loading, empty, error

## Locale Pairings
- ko: heading=Pretendard / body=Pretendard

## 주의사항
- image-derived hints는 advisory (truth source: system_spec.md, token_schema.json)
- 이 프리셋과 맞지 않으면 `brand_tone` 축을 바꿔 재시도
