# dashboard--editorial-warm

## 어떤 제품에 맞나
- editorial-warm 운영/큐레이션 대시보드 — sidebar-nav · data-table · kpi-card · filter-chip · editorial-calendar · curation-queue · publishing-pipeline, warm neutral + serif heading + muted accent, 한국어 1급

- app_mode: `dashboard` / brand_tone: `editorial-warm`

## Color Tokens (light + dark)
### Core
- primary: `#614051`
- accent: `#FADA5E`
- surface_tint: `#F9C0C4`

### Semantic
- success: `#4A7C59`
- warning: `#FADA5E`
- danger: `#FA8072`
- info: `#614051`

> light/dark 변형은 어댑터(`nextjs-tailwind-shadcn` 등)가 파생. 원본 팔레트는 위 HEX 1세트.

## Typography
- heading: Noto Serif KR
- body: Pretendard
- mono: Fira Code
- korean: Pretendard

## 대표 컴포넌트
- **curation-queue** — parts: container, header, content-area, footer(optional), action(optional) | states: default, loading, empty, error
- **archive-shelf** — parts: container, header, content-area, footer(optional), action(optional) | states: default, loading, empty, error
- **issue-planner** — parts: container, header, content-area, footer(optional), action(optional) | states: default, loading, empty, error

## Locale Pairings
- ko: heading=Pretendard / body=Pretendard

## 주의사항
- image-derived hints는 advisory (truth source: system_spec.md, token_schema.json)
- 이 프리셋과 맞지 않으면 `brand_tone` 축을 바꿔 재시도
