# marketing-landing--minimal-tech

## 어떤 제품에 맞나
- B2B/SaaS 팀을 위한 minimal-tech 톤 마케팅 랜딩 — hero·feature·pricing·social proof·testimonial·faq·cta, 한국어 1급

- app_mode: `marketing-landing` / brand_tone: `minimal-tech`

## Color Tokens (light + dark)
### Core
- primary: `#01889F`
- accent: `#DAA520`
- surface_tint: `#B0E0E6`

### Semantic
- success: `#4A7C59`
- warning: `#DAA520`
- danger: `#8B2252`
- info: `#0F4C81`

> light/dark 변형은 어댑터(`nextjs-tailwind-shadcn` 등)가 파생. 원본 팔레트는 위 HEX 1세트.

## Typography
- heading: Inter
- body: Inter
- mono: JetBrains Mono
- korean: Pretendard

## 대표 컴포넌트
- **hero-cta-group** — parts: container, label, leading-icon(optional), trailing-icon(optional) | states: default, hover, active, disabled
- **hero-container** — parts: section-container, inner-max-width, content | states: default, in-view, hover
- **hero-eyebrow** — parts: eyebrow-label | states: default

## Locale Pairings
- ko: heading=Pretendard / body=Pretendard

## 주의사항
- image-derived hints는 advisory (truth source: system_spec.md, token_schema.json)
- 이 프리셋과 맞지 않으면 `brand_tone` 축을 바꿔 재시도
