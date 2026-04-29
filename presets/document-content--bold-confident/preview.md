# document-content--bold-confident

## 어떤 제품에 맞나
- bold-confident magazine/opinion long-form — saturated primary + high-contrast + impact typography, article · TOC · pull-quote · masthead, 한국어 1급

- app_mode: `document-content` / brand_tone: `bold-confident`

## Color Tokens (light + dark)
### Core
- primary: `#0F4C81`
- accent: `#CC142F`
- surface_tint: `#F2552C`

### Semantic
- success: `#4A7C59`
- warning: `#EC5800`
- danger: `#FF2400`
- info: `#0F4C81`

> light/dark 변형은 어댑터(`nextjs-tailwind-shadcn` 등)가 파생. 원본 팔레트는 위 HEX 1세트.

## Typography
- heading: Pretendard
- body: Pretendard
- mono: n/a
- korean: Pretendard

## 대표 컴포넌트
- **feature-article** — parts: container, header, content-area, footer(optional), action(optional) | states: default, loading, empty, error
- **reading-progress-bar** — parts: container, icon, message, action(optional), close-button(optional) | states: info, success, warning, danger
- **article-body** — parts: container, header, content-area, footer(optional), action(optional) | states: default, loading, empty, error

## Locale Pairings
- ko: heading=Pretendard / body=Pretendard

## 주의사항
- image-derived hints는 advisory (truth source: system_spec.md, token_schema.json)
- 이 프리셋과 맞지 않으면 `brand_tone` 축을 바꿔 재시도
