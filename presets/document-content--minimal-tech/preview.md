# document-content--minimal-tech

## 어떤 제품에 맞나
- 개발자용 API 레퍼런스 · 기술 문서 — TOC + article + code block + callout, 한국어 1급

- app_mode: `document-content` / brand_tone: `minimal-tech`

## Color Tokens (light + dark)
### Core
- primary: `#5A4FCF`
- accent: `#2A52BE`
- surface_tint: `#E6E6FA`

### Semantic
- success: `#4A7C59`
- warning: `#F7F5EB`
- danger: `#8B2252`
- info: `#CAB7E1`

> light/dark 변형은 어댑터(`nextjs-tailwind-shadcn` 등)가 파생. 원본 팔레트는 위 HEX 1세트.

## Typography
- heading: Spoqa Han Sans Neo
- body: Spoqa Han Sans Neo
- mono: JetBrains Mono
- korean: Spoqa Han Sans Neo

## 대표 컴포넌트
- **article-body** — parts: container, header, content-area, footer(optional), action(optional) | states: default, loading, empty, error
- **prose-block** — parts: container, header, content-area, footer(optional), action(optional) | states: default, loading, empty, error
- **table-of-contents** — parts: container, header, content-area, footer(optional), action(optional) | states: default, loading, empty, error

## Locale Pairings
- ko: heading=Pretendard / body=Pretendard

## 주의사항
- image-derived hints는 advisory (truth source: system_spec.md, token_schema.json)
- 이 프리셋과 맞지 않으면 `brand_tone` 축을 바꿔 재시도
