# marketing-landing--bold-confident

## 어떤 제품에 맞나
- 프리미어리그 팬 허브 — 대담한 고대비 랜딩/마케팅, 팀·경기 시각 임팩트

- app_mode: `marketing-landing` / brand_tone: `bold-confident`

## Color Tokens (light + dark)
### Core
- primary: `#E90052`
- accent: `#00FF85`
- surface_tint: `#FFD700`

### Semantic
- success: `#00C853`
- warning: `#FF8C00`
- danger: `#E90052`
- info: `#1A1A2E`

> light/dark 변형은 어댑터(`nextjs-tailwind-shadcn` 등)가 파생. 원본 팔레트는 위 HEX 1세트.

## Typography
- heading: Spoqa Han Sans Neo
- body: Spoqa Han Sans Neo
- mono: JetBrains Mono
- korean: Spoqa Han Sans Neo

## 대표 컴포넌트
- **hero-cta-group** — parts: container, label, leading-icon(optional), trailing-icon(optional) | states: default, hover, active, disabled
- **primary-button** — parts: container, label, leading-icon(optional), trailing-icon(optional) | states: default, hover, active, disabled
- **hero-container** — parts: section-container, inner-max-width, content | states: default, in-view, hover

## 주의사항
- image-derived hints는 advisory (truth source: system_spec.md, token_schema.json)
- 이 프리셋과 맞지 않으면 `brand_tone` 축을 바꿔 재시도
