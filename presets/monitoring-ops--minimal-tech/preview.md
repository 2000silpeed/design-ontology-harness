# monitoring-ops--minimal-tech

## 어떤 제품에 맞나
- SRE/DevOps 실시간 observability 콘솔 — metric/alert/trace, 다크 기본, 한국어 1급

- app_mode: `monitoring-ops` / brand_tone: `minimal-tech`

## Color Tokens (light + dark)
### Core
- primary: `#007FFF`
- accent: `#50C878`
- surface_tint: `#D6EAF8`

### Semantic
- success: `#50C878`
- warning: `#F8F8F4`
- danger: `#8B2252`
- info: `#444C57`

> light/dark 변형은 어댑터(`nextjs-tailwind-shadcn` 등)가 파생. 원본 팔레트는 위 HEX 1세트.

## Typography
- heading: Inter
- body: Inter
- mono: JetBrains Mono
- korean: Pretendard

## 대표 컴포넌트
- **ticket-queue** — parts: container, header, content-area, footer(optional), action(optional) | states: default, loading, empty, error
- **alert-list** — parts: container, header, content-area, footer(optional), action(optional) | states: default, loading, empty, error
- **icon-button** — parts: container, label, leading-icon(optional), trailing-icon(optional) | states: default, hover, active, disabled

## Locale Pairings
- ko: heading=Pretendard / body=Pretendard

## 주의사항
- image-derived hints는 advisory (truth source: system_spec.md, token_schema.json)
- 이 프리셋과 맞지 않으면 `brand_tone` 축을 바꿔 재시도
