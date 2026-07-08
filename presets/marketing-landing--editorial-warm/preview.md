# marketing-landing--editorial-warm

## 어떤 제품에 맞나
- 독립 뉴스레터·매거진 발행인용 editorial-warm 톤 마케팅 랜딩 — hero + featured issue + issue archive + subscribe pricing + testimonial + author profile + faq + cta, warm ochre + rust + wheat palette, reading-first, 한국어 1급

- app_mode: `marketing-landing` / brand_tone: `editorial-warm`

## Color Tokens (light + dark)
### Core
- primary: `#CB9D06`
- accent: `#B7410E`
- surface_tint: `#F5DEB3`

### Semantic
- success: `#4A7C59`
- warning: `#B7410E`
- danger: `#E2725B`
- info: `#4A6B8A`

> light/dark 변형은 어댑터(`nextjs-tailwind-shadcn` 등)가 파생. 원본 팔레트는 위 HEX 1세트.

## Typography
- heading: Fraunces
- body: Inter
- mono: JetBrains Mono
- korean: Pretendard

## 대표 컴포넌트
- **hero-cta-group** — parts: container, label, leading-icon(optional), trailing-icon(optional) | states: default, hover, active, disabled
- **cover-story** — parts: container, header, content-area, footer(optional), action(optional) | states: default, loading, empty, error
- **drop-banner** — parts: container, header, content-area, footer(optional), action(optional) | states: default, loading, empty, error

## Locale Pairings
- ko: heading=Pretendard / body=Pretendard

## 주의사항
- image-derived hints는 advisory (truth source: system_spec.md, token_schema.json)
- 이 프리셋과 맞지 않으면 `brand_tone` 축을 바꿔 재시도
