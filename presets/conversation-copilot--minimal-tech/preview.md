# conversation-copilot--minimal-tech

## 어떤 제품에 맞나
- AI 코파일럿/대화형 워크스페이스 — 미니멀 테크 톤, chat + artifact + thread

- app_mode: `conversation-copilot` / brand_tone: `minimal-tech`

## Color Tokens (light + dark)

### Semantic
- success: `#006A4E`
- warning: `#CC7722`
- danger: `#8B2252`
- info: `#000080`

> light/dark 변형은 어댑터(`nextjs-tailwind-shadcn` 등)가 파생. 원본 팔레트는 위 HEX 1세트.

## Typography
- heading: Spoqa Han Sans Neo
- body: Spoqa Han Sans Neo
- mono: JetBrains Mono
- korean: Spoqa Han Sans Neo

## 대표 컴포넌트
- **audit-timeline** — parts: list, event-item, timestamp, actor, event-summary | states: default, filtered, expanded, empty
- **primary-button** — parts: container, label, leading-icon(optional), trailing-icon(optional) | states: default, hover, active, disabled
- **secondary-button** — parts: container, label, leading-icon(optional), trailing-icon(optional) | states: default, hover, active, disabled

## Locale Pairings
- ko: heading=Pretendard / body=Pretendard

## 주의사항
- image-derived hints는 advisory (truth source: system_spec.md, token_schema.json)
- 이 프리셋과 맞지 않으면 `brand_tone` 축을 바꿔 재시도
