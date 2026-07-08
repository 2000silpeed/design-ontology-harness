# document-content--editorial-warm

## 어떤 제품에 맞나
- 작은 팀·제작자용 에디토리얼 워크스페이스 — 문서/콘텐츠 reading flow, split-pane, warm serif 페어링

- app_mode: `document-content` / brand_tone: `editorial-warm`

## Color Tokens (light + dark)

### Semantic
- success: `#27503D`
- warning: `#F5DEB3`
- danger: `#E2725B`
- info: `#967BB6`

> light/dark 변형은 어댑터(`nextjs-tailwind-shadcn` 등)가 파생. 원본 팔레트는 위 HEX 1세트.

## Typography
- heading: Noto Serif KR
- body: Pretendard
- mono: Source Code Pro
- korean: Pretendard

## 대표 컴포넌트
- **autocomplete** — parts: backdrop, container, header, content, footer(optional) | states: closed, opening, open, closing
- **hero-headline** — parts: heading-text | states: default
- **cta-headline** — parts: heading-text | states: default

## Locale Pairings
- ko: heading=Pretendard / body=Lora

## 주의사항
- image-derived hints는 advisory (truth source: system_spec.md, token_schema.json)
- 이 프리셋과 맞지 않으면 `brand_tone` 축을 바꿔 재시도
