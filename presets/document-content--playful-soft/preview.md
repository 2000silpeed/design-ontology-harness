# document-content--playful-soft

## 어떤 제품에 맞나
- 모바일 만화 잡지 앱 — playful-soft 톤, 주간 이슈·표지·연재 회차·컷 미리보기·보관함 중심 한국어 UI

- app_mode: `document-content` / brand_tone: `playful-soft`

## Color Tokens (light + dark)
### Core
- primary: `#8E9AF1`
- accent: `#FF6F61`
- surface_tint: `#F3E5AB`

### Semantic
- success: `#4A7C59`
- warning: `#FF6F61`
- danger: `#8B2252`
- info: `#8E9AF1`

> light/dark 변형은 어댑터(`nextjs-tailwind-shadcn` 등)가 파생. 원본 팔레트는 위 HEX 1세트.

## Typography
- heading: Pretendard
- body: Pretendard
- mono: JetBrains Mono
- korean: Pretendard

## 대표 컴포넌트
- **feature-article** — parts: container, header, content-area, footer(optional), action(optional) | states: default, loading, empty, error
- **article-body** — parts: container, header, content-area, footer(optional), action(optional) | states: default, loading, empty, error
- **prose-block** — parts: container, header, content-area, footer(optional), action(optional) | states: default, loading, empty, error

## Locale Pairings
- ko: heading=Pretendard / body=Pretendard

## 주의사항
- image-derived hints는 advisory (truth source: system_spec.md, token_schema.json)
- 이 프리셋과 맞지 않으면 `brand_tone` 축을 바꿔 재시도
