# canvas-tool--corporate-trust

## 어떤 제품에 맞나
- LookMe Toss In-App custom mobile try-on system: trusted face try-on utility with real Colorfit item image sets and paid wardrobe generation

- app_mode: `canvas-tool` / brand_tone: `corporate-trust`

## Color Tokens (light)

### Semantic
- success: `#4F7942`
- warning: `#CC7722`
- danger: `#E2725B`
- info: `#000080`

> 추가 color mode 변형은 어댑터(`nextjs-tailwind-shadcn` 등)가 파생. 원본 팔레트는 위 HEX 1세트.

## Typography
- heading: Pretendard
- body: Pretendard
- mono: n/a
- korean: Pretendard

## 대표 컴포넌트
- **tabs** — parts: container, nav-item, icon(optional), label, indicator(active) | states: default, hover, active, collapsed
- **primary-button** — parts: container, label, leading-icon(optional), trailing-icon(optional) | states: default, hover, active, disabled
- **secondary-button** — parts: container, label, leading-icon(optional), trailing-icon(optional) | states: default, hover, active, disabled

## 주의사항
- image-derived hints는 advisory (truth source: system_spec.md, token_schema.json)
- 이 프리셋과 맞지 않으면 `brand_tone` 축을 바꿔 재시도
