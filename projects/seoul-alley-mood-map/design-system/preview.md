# monitoring-ops--corporate-trust

## 어떤 제품에 맞나
- Mobile-first sensory place curation system for Seoul alley mood mapping

- app_mode: `monitoring-ops` / brand_tone: `corporate-trust`

## Color Tokens (light + dark)
### Core
- primary: `#4F97A3`
- accent: `#4F7942`
- surface_tint: `#FADA5E`

### Semantic
- success: `#4F7942`
- warning: `#CC7722`
- danger: `#8B2252`
- info: `#000080`

> light/dark 변형은 어댑터(`nextjs-tailwind-shadcn` 등)가 파생. 원본 팔레트는 위 HEX 1세트.

## Typography
- heading: Pretendard
- body: Pretendard
- mono: n/a
- korean: Pretendard

## 대표 컴포넌트
- **status-badge** — parts: container, icon, message, action(optional), close-button(optional) | states: info, success, warning, danger
- **data-table** — parts: container, header, content-area, footer(optional), action(optional) | states: default, loading, empty, error
- **inline-alert** — parts: container, icon, message, action(optional), close-button(optional) | states: info, success, warning, danger

## 주의사항
- image-derived hints는 advisory (truth source: system_spec.md, token_schema.json)
- 이 프리셋과 맞지 않으면 `brand_tone` 축을 바꿔 재시도
