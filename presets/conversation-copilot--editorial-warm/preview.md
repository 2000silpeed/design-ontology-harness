# conversation-copilot--editorial-warm

## 어떤 제품에 맞나
- writing/editorial AI copilot — editorial-warm 톤, chat·prompt·artifact(draft)·thread·composer, 차분한 warm neutral + serif-ish pairing, 한국어 1급

- app_mode: `conversation-copilot` / brand_tone: `editorial-warm`

## Color Tokens (light + dark)
### Core
- primary: `#964F4C`
- accent: `#8A9A5B`
- surface_tint: `#EEDC82`

### Semantic
- success: `#8A9A5B`
- warning: `#F5DEB3`
- danger: `#964F4C`
- info: `#4A6B8A`

> light/dark 변형은 어댑터(`nextjs-tailwind-shadcn` 등)가 파생. 원본 팔레트는 위 HEX 1세트.

## Typography
- heading: Source Serif Pro
- body: Inter
- mono: JetBrains Mono
- korean: Pretendard

## 대표 컴포넌트
- **message-artifact** — parts: container, header, content-area, footer(optional), action(optional) | states: default, loading, empty, error
- **prompt-composer** — parts: container, label, input-area, helper-text(optional), leading-icon(optional) | states: default, focus, filled, error
- **chat-message** — parts: container, header, content-area, footer(optional), action(optional) | states: default, loading, empty, error

## Locale Pairings
- ko: heading=Pretendard / body=Pretendard

## 주의사항
- image-derived hints는 advisory (truth source: system_spec.md, token_schema.json)
- 이 프리셋과 맞지 않으면 `brand_tone` 축을 바꿔 재시도
