# dashboard--corporate-trust

## 어떤 제품에 맞나
- 기업·금융팀을 위한 corporate-trust 톤 핀테크 운영 대시보드 — 거래/잔고/컴플라이언스 콘솔, 한국어 1급

- app_mode: `dashboard` / brand_tone: `corporate-trust`

## Color Tokens (light + dark)
### Core
- primary: `#003153`
- accent: `#A97132`
- surface_tint: `#D6EAF8`

### Semantic
- success: `#4A7C59`
- warning: `#A97132`
- danger: `#D4A6A6`
- info: `#B8CBD0`

> light/dark 변형은 어댑터(`nextjs-tailwind-shadcn` 등)가 파생. 원본 팔레트는 위 HEX 1세트.

## Typography
- heading: Pretendard
- body: Pretendard
- mono: IBM Plex Mono
- korean: Pretendard

## 대표 컴포넌트
- **sidebar-nav** — parts: container, nav-item, icon(optional), label, indicator(active) | states: default, hover, active, collapsed
- **data-table** — parts: container, header, content-area, footer(optional), action(optional) | states: default, loading, empty, error
- **filter-chip** — parts: container, label, input-area, helper-text(optional), leading-icon(optional) | states: default, focus, filled, error

## Locale Pairings
- ko: heading=Pretendard / body=Pretendard

## 주의사항
- image-derived hints는 advisory (truth source: system_spec.md, token_schema.json)
- 이 프리셋과 맞지 않으면 `brand_tone` 축을 바꿔 재시도
