# dashboard--minimal-tech

## 어떤 제품에 맞나
- SaaS 팀을 위한 미니멀 테크 운영 대시보드 — 데이터 테이블·KPI·command palette 중심, 한국어 1급

- app_mode: `dashboard` / brand_tone: `minimal-tech`

## Color Tokens (light + dark)
### Core
- primary: `#000080`
- accent: `#CC7722`
- surface_tint: `#87CEEB`

### Semantic
- success: `#4A7C59`
- warning: `#CC7722`
- danger: `#8B2252`
- info: `#708090`

> light/dark 변형은 어댑터(`nextjs-tailwind-shadcn` 등)가 파생. 원본 팔레트는 위 HEX 1세트.

## Typography
- heading: Spoqa Han Sans Neo
- body: Spoqa Han Sans Neo
- mono: JetBrains Mono
- korean: Spoqa Han Sans Neo

## 대표 컴포넌트
- **sidebar-nav** — parts: container, nav-item, icon(optional), label, indicator(active) | states: default, hover, active, collapsed
- **stat-card** — parts: container, inner-content | states: default, hover, focus-visible
- **insight-card** — parts: container, inner-content | states: default, hover, focus-visible

## Locale Pairings
- ko: heading=Pretendard / body=Pretendard

## 주의사항
- image-derived hints는 advisory (truth source: system_spec.md, token_schema.json)
- 이 프리셋과 맞지 않으면 `brand_tone` 축을 바꿔 재시도
