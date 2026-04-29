# Atelier — 크리에이티브 캔버스 · 레이어 · 인스펙터 도구 Spec

## 제품 개요
Atelier 는 디자이너를 위한 **minimal-tech 톤 캔버스 도구 (canvas-tool)** 다.
Figma / Framer / Excalidraw / tldraw / Rive / Spline 계열의 **canvas workspace + layer panel +
inspector panel + toolbar + ruler + snap guide** 를 한 화면에서 정밀하게 조합해
디자이너가 keyboard-first 로 빠르게 캔버스를 조작하고 픽셀 단위로 인스펙트할 수 있게 한다.
이 프리셋은 "관리 대시보드"나 "에디토리얼 매거진"이 아니라 **"creative canvas tool"** 성향으로,
hairline borders · 무채색 surface · monochrome + single accent · keyboard-first toolbar 를
시각 정체성으로 고정한다. 한국어 UI 를 1급으로 지원한다.

## 사용자
- **프로덕트 디자이너**: 화면 디자인, 컴포넌트 정의, 프로토타입 — canvas workspace 중심
- **디자인 시스템 메인테이너**: 토큰 인스펙트, 레이어 구조 정리, 컴포넌트 export
- **프로토타이퍼 / 인터랙션 디자이너**: 화면 흐름, 캔버스 조작, snap guide 정밀 정렬

## 핵심 화면
1. **Canvas Workspace** — canvas + toolbar + toolbar group + contextual toolbar + layer panel + inspector panel + ruler + snap guide + grid overlay + selection handle + zoom control + minimap
2. **Layer Panel** — layer panel + layer item + layer thumbnail + depth indent + visibility lock toggle + drag reorder
3. **Inspector** — inspector panel + property row + number input scrub + color picker + constraint editor + alignment chrome
4. **Asset Library** — asset library + asset card + asset grid + asset drag-to-canvas + tag filter + search field
5. **Export Panel** — export panel + format selector + scale selector + preview + export queue
6. **Shortcuts Cheatsheet** — keyboard shortcut cheatsheet + shortcut grid + search field + section filter

## UI 컴포넌트 (도출)
- **canvas-workspace** — neutral canvas surface, ruler chrome, grid overlay, snap guide, infinite zoom/pan
- **layer-panel** — dense layer tree, depth indent, drag reorder, visibility/lock toggle, search filter
- **layer-item** — layer panel 의 단위 — thumbnail + name + visibility/lock + depth chevron
- **layer-thumbnail** — 16–24px 미니 미리보기 thumbnail, 빈 레이어는 muted 아이콘
- **inspector-panel** — thin inspector panel, property row 들의 컨테이너, section collapse
- **property-row** — 라벨 + 입력(숫자/색/select) + unit, mono-font 숫자 input, drag-to-scrub 지원
- **toolbar** — keyboard-first 메인 toolbar, 좌측 selection / shape / text / asset 도구 그룹
- **toolbar-group** — toolbar 안의 도구 묶음 — active state 는 single accent 강조
- **contextual-toolbar** — 선택 상태에 따라 canvas 위에 부드럽게 떠오르는 toolbar
- **ruler** — canvas 좌/상단 ruler chrome, px / pt / % 단위, drag 로 guide 생성
- **snap-guide** — selection handle 정렬 시 나타나는 amber accent 가이드 라인
- **grid-overlay** — pixel-precise grid 오버레이, 8px / 16px / custom toggle
- **selection-handle** — 선택된 객체의 8 handle (corner + edge), shift 비례 스케일
- **zoom-control** — canvas 우하단 zoom 입력 + 100% / fit 버튼
- **minimap** — 큰 캔버스용 minimap, 현재 viewport 박스 표시
- **keyboard-shortcut-cheatsheet** — `?` 단축키로 호출되는 shortcut grid + 검색
- **command-palette** — ⌘K 글로벌 커맨드 팔레트, layer/file/action 검색
- **asset-library** — 좌측 패널, asset grid + drag-to-canvas, 태그/검색 필터
- **asset-card** — asset library 의 단위 — thumbnail + name + tag pill
- **export-panel** — 우측 sheet, format / scale / preview / export queue
- **format-selector** — png / svg / pdf / webp 토글 + 스케일 (1x / 2x / 3x)
- **search-field** — assets / layers / commands 공용 search field, ⌘K 와 연동
- **dropdown-menu** — keyboard-first 메뉴 — file / edit / view / arrange
- **dialog** — 파괴적 액션 (delete layer, reset canvas) confirm dialog
- **toast** — 저장 완료 / export 완료 / 오류 low-noise toast
- **tabs** — inspector 안의 탭 (Design / Prototype / Inspect) 전환

## 인터랙션 원칙
- **keyboard-first**: 모든 도구는 단일 키 단축키 (V / R / T / L / I / H / Z), `?` 로 cheatsheet 호출
- **layer drag reorder**: layer panel 에서 드래그 시 depth 변경 + drop indicator 표시
- **inspector number scrub**: property row 숫자 input 라벨을 가로 드래그하면 값 증감 (⌥ 정밀, ⇧ 큰 스텝)
- **snap to grid / guide**: selection 이동 시 amber snap guide 표시, ⌘ 일시 비활성
- **zoom / pan canvas**: ⌘ + scroll zoom, space + drag pan, fit / 100% 단축키
- **multi-select drag handle**: shift 클릭 또는 marquee, 다중 선택 시 공통 selection handle
- **undo / redo stack**: ⌘Z / ⇧⌘Z, command palette 에서도 호출 가능
- **quick duplicate (⌥-drag)**: 객체 ⌥-drag 시 즉시 복제
- **contextual toolbar**: 선택 직후 객체 위에 부드럽게 fade-in (120ms)
- **command palette ⌘K**: 모든 명령은 ⌘K 안에서 검색 가능, 단축키 동기화
- **low-motion**: 전반 120–200ms ease-out, decorative animation 금지, 결정론적 transition
- **파괴적 액션**(delete layer, reset canvas)은 dialog + keyboard confirm

## 색상 전략
- **neutral canvas surface** — 무채색 베이스 + Misty Blue surface tint 로 차분한 chrome
- **primary**: **Cobalt Violet (#804AA8)** — 차분/예술적 cool purple, active toolbar group / inspector primary action
- **accent**: **Amber (#FFBF00)** — Figma-esque single vivid accent, snap guide / selection handle / active layer highlight
- **surface_tint**: **Misty Blue (#B5C7EB)** — 보라 섞인 뉴트럴 블루, ruler / grid overlay / property row hover
- **semantic**: success / warning / danger / info 4 role — toast / inline-alert 매핑
- **monochrome + single accent** — 캔버스 chrome 은 무채색, 강조는 accent 단일
- **hairline borders** — 1px subtle border, 깊은 elevation / drop shadow 금지
- **dark mode**: deep cool neutral surface (not pure black) + tuned cobalt + amber 채도 낮춤
- **기존 minimal-tech 4종 (Navy / Azure / Iris Violet / Bronze) 과 정체성 차별화**

## 타이포그래피
- **heading**: **Inter** (영문) / **Pretendard** (한글) — geometric sans, serif 금지
- **body**: **Inter / Pretendard** — inspector / property row 라벨 공용, line-height 1.5
- **mono**: **JetBrains Mono** — shortcut key / property row 숫자 input / px·% 값 필수, tabular-nums
- **scale**: xs(11) / sm(12) / md(13) / lg(14) / xl(16) / 2xl(20) / 3xl(28)
- **inspector scale**: property label sm(12), input md(13), section header lg(14 semibold)
- **layer name**: sm(12), 한글은 line-height 1.6 keep-all
- **shortcut key**: mono 11–12px, padding 2px 4px, subtle background
- **tabular-nums**: property row 숫자 / zoom 값 / shortcut 카운트
- **emoji 자제**: chrome 안에서 이모지 사용 최소

## 접근성
- WCAG 2.2 AA (본문 대비 4.5:1, UI 3:1)
- snap guide 는 amber 색 + 1px 강조 (색맹 대응 — 위치 + 시각 단서 이중)
- selection handle 은 keyboard 로도 이동 가능 (화살표 키 1px, ⇧ 화살표 10px)
- keyboard shortcut cheatsheet 는 검색 필드 focusable, esc 닫기
- contextual toolbar 는 focus trap 회피 — esc 시 canvas focus 복귀
- inspector property row 라벨 drag-to-scrub 은 키보드 대안 (focus + 화살표) 제공
- dialog 는 focus trap + esc 취소
- canvas zoom 은 ⌘+ / ⌘- 키보드 대안

## 한글 대응
- Pretendard variable (woff2) 번들, heading/body 공용
- 한글 layer name / asset name line-height **1.6**, letter-spacing -1%
- word-break: **keep-all**, overflow-wrap: break-word
- shortcut key / property row 숫자 input 은 mono 영문 고정 (한글 혼용 금지)
- tabular-nums 로 숫자 정렬
- 한국어 라벨: "레이어 / 인스펙터 / 캔버스 / 가이드 / 정렬" + 영문 "layer / inspector / canvas / guide / align" 병기 허용
- mention `@` 등은 사용 안 함 — chrome 안 한글 입력은 layer name 정도

## 주의사항
- 이 프리셋은 **canvas-tool--minimal-tech (P1, creative)** — 캔버스 / 레이어 / 인스펙터 특화
- "관리 대시보드 · 데이터 테이블" 은 `dashboard--minimal-tech`
- "API 레퍼런스 · 기술 문서" 는 `document-content--minimal-tech`
- "AI 코파일럿 채팅" 은 `conversation-copilot--minimal-tech`
- "운영 모니터링 · alert" 은 `monitoring-ops--minimal-tech`
- 친근한 소셜 피드는 `community-feed--playful-soft`
- 이미지 기반 힌트는 advisory, 구조적 결정은 spec + KB 우선
- 실제 백엔드 (file storage, realtime collaboration, version history) 는 프리셋 범위 외 — 시각 chrome 만 다룸
