# community-feed--playful-soft

## 어떤 제품에 맞나
- 친근한 소셜 피드 · 스레드 · 프레즌스 · 알림 — playful-soft 톤, 한국어 1급

- app_mode: `community-feed` / brand_tone: `playful-soft`

## Color Tokens (light + dark)
### Core
- primary: `#F88379`
- accent: `#98FF98`
- surface_tint: `#FFF8DC`

### Semantic
- success: `#ACE1AF`
- warning: `#FFDAB9`
- danger: `#FA8072`
- info: `#4A6B8A`

> light/dark 변형은 어댑터(`nextjs-tailwind-shadcn` 등)가 파생. 원본 팔레트는 위 HEX 1세트.

## Typography
- heading: Nunito
- body: Inter
- mono: JetBrains Mono
- korean: Pretendard

## 대표 컴포넌트
- **feed-item** — parts: container, header, content-area, footer(optional), action(optional) | states: default, loading, empty, error
- **thread-view** — parts: container, header, content-area, footer(optional), action(optional) | states: default, loading, empty, error
- **comment-thread** — parts: container, header, content-area, footer(optional), action(optional) | states: default, loading, empty, error

## Locale Pairings
- ko: heading=Pretendard / body=Pretendard

## 주의사항
- image-derived hints는 advisory (truth source: system_spec.md, token_schema.json)
- 이 프리셋과 맞지 않으면 `brand_tone` 축을 바꿔 재시도
