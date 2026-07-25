# document-content--corporate-trust

## 어떤 제품에 맞나
- EKOS Knowledge Intake — 온톨로지 어휘를 번역한 업무 문장 중심의 지식 등록·검토 워크벤치 (Prussian/Ocean/Cornsilk 아카이브 톤)

- app_mode: `document-content` / brand_tone: `corporate-trust`

## Color Tokens (light + dark)
### Core
- primary: `#003153`
- accent: `#B7410E`
- surface_tint: `#FFF8DC`

### Semantic
- success: `#355E3B`
- warning: `#DAA520`
- danger: `#964F4C`
- info: `#4F97A3`

> light/dark 변형은 어댑터(`nextjs-tailwind-shadcn` 등)가 파생. 원본 팔레트는 위 HEX 1세트.

## Typography
- heading: Pretendard
- body: Pretendard
- mono: Source Code Pro
- korean: Pretendard

## 대표 컴포넌트
- **left-nav** — parts: nav-rail, nav-item, nav-label, active-indicator | states: default, active, keyboard-focus, collapsed
- **global-search-input** — parts: input-field, placeholder, search-icon, results-popover | states: empty, typing, results, no-results
- **intake-method-list** — parts: method-row, method-icon, method-title, method-description | states: default, hover, keyboard-focus, disabled-by-permission

## 주의사항
- image-derived hints는 advisory (truth source: system_spec.md, token_schema.json)
- 이 프리셋과 맞지 않으면 `brand_tone` 축을 바꿔 재시도
