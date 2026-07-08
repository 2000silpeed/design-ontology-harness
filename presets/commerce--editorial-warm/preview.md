# commerce--editorial-warm

## 어떤 제품에 맞나
- 퍼스널컬러 기반 모바일 패션 커머스 — 에디토리얼 웜 톤, 코디/가격 비교 UX

- app_mode: `commerce` / brand_tone: `editorial-warm`

## Color Tokens (light)
- (color_reference 미설정 — brand_profile.color_reference를 채우면 자동 추출)

## Typography
- heading: Noto Serif KR
- body: Pretendard
- mono: n/a
- korean: Pretendard

## 대표 컴포넌트
- **breadcrumbs** — parts: container, nav-item, icon(optional), label, indicator(active) | states: default, hover, active, collapsed
- **inspector-drawer** — parts: drawer, header, section-list, property-row, action-row | states: closed, open, loading, dirty
- **primary-button** — parts: container, label, leading-icon(optional), trailing-icon(optional) | states: default, hover, active, disabled

## Locale Pairings
- ko: heading=Pretendard / body=Pretendard

## 주의사항
- image-derived hints는 advisory (truth source: system_spec.md, token_schema.json)
- 이 프리셋과 맞지 않으면 `brand_tone` 축을 바꿔 재시도
