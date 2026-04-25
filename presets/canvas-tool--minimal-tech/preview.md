# canvas-tool--minimal-tech

## 어떤 제품에 맞나
- 크리에이티브 팀을 위한 minimal-tech 톤 캔버스 · 레이어 · 인스펙터 도구 — keyboard-first, 한국어 1급

- app_mode: `canvas-tool` / brand_tone: `minimal-tech`

## Color Tokens (light + dark)
### Core
- primary: `#804AA8`
- accent: `#FFBF00`
- surface_tint: `#B5C7EB`

### Semantic
- success: `#4A7C59`
- warning: `#FFBF00`
- danger: `#8B2252`
- info: `#C4C3D0`

> light/dark 변형은 어댑터(`nextjs-tailwind-shadcn` 등)가 파생. 원본 팔레트는 위 HEX 1세트.

## Typography
- heading: Spoqa Han Sans Neo
- body: Spoqa Han Sans Neo
- mono: JetBrains Mono
- korean: Spoqa Han Sans Neo

## 대표 컴포넌트
- **layer-panel** — parts: container, header, content-area, footer(optional), action(optional) | states: default, loading, empty, error
- **layer-item** — parts: container, header, content-area, footer(optional), action(optional) | states: default, loading, empty, error
- **inspector-panel** — parts: container, header, content-area, footer(optional), action(optional) | states: default, loading, empty, error

## Locale Pairings
- ko: heading=Pretendard / body=Pretendard

## 주의사항
- image-derived hints는 advisory (truth source: system_spec.md, token_schema.json)
- 이 프리셋과 맞지 않으면 `brand_tone` 축을 바꿔 재시도
