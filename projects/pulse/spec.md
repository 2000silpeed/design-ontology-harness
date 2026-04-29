# Pulse — 실시간 Observability 운영 콘솔 Spec

## 제품 개요
Pulse는 SRE / DevOps / 플랫폼 팀을 위한 **minimal-tech 톤 실시간 observability 콘솔**이다.
Grafana / Datadog / Honeycomb 계열의 운영 도구를 지향하며, metric / log / trace / alert 를
한 화면에서 고밀도로 들여다보는 **realtime ops** 환경을 제공한다. 다크 모드가 기본이며
한국어 UI 를 1급으로 지원한다. 이 프리셋은 "관리 대시보드"가 아니라 **"실시간 운영/알람"**
콘솔에 특화된다.

## 사용자
- SRE / 인프라 엔지니어: SLO / 에러 버짓 / 용량 관찰
- DevOps / 플랫폼 엔지니어: 파이프라인·서비스 헬스 모니터링
- 온콜 엔지니어 / 인시던트 커맨더: alert ack, 인시던트 타임라인, 즉시 드릴다운

## 핵심 화면
1. **Incidents** — 활성 인시던트 리스트 + severity badge + 타임라인 + 빠른 ack/mute
2. **Alerts** — rule 기반 alert list, severity / status / route 필터, threshold editor
3. **Metrics Dashboard** — chart grid (line/bar/sparkline) + kpi card + time range picker
4. **Traces** — trace flamegraph + span detail + service dependency view
5. **Services** — service status board + SLO 카드 + error rate / latency 요약
6. **Settings** — alert routing, notification, integration, 멤버 권한

## UI 컴포넌트 (도출)
- sidebar navigation (2-level, collapsible)
- chart grid (line chart, bar chart, sparkline, heatmap tile)
- kpi card (numeric emphasis, trend sparkline)
- alert list (severity badge + ack/mute inline action)
- severity badge (critical / high / medium / low + 텍스트 라벨)
- metric table (dense, sortable, sticky header, numeric right-align)
- status board (service × region grid, color + label)
- incident timeline (time-grouped, actor + action + severity)
- time range picker (relative + absolute, zoom/pan)
- filter chrome (chips + saved views)
- search input (⌘K, fuzzy, recent)
- log viewer (virtualized, timestamp mono, highlight severity)
- trace flamegraph (span bars, tooltip latency)
- threshold editor (numeric + operator + preview)
- toast (low-noise, 운영 소음 최소)
- dialog (ack/mute 확인, 파괴적 편집)
- tabs (service / rule level)
- breadcrumbs
- dropdown menu (keyboard-first)
- empty state
- pagination

## 인터랙션 원칙
- 키보드 우선: ⌘K 검색, j/k 리스트 이동, a=ack, m=mute, g=go
- **live-update 일관성**: 초 단위 갱신이어도 레이아웃 jitter 금지, 자리 고정
- drilldown: chart → metric table → log viewer / trace 한 흐름
- 시간 축: zoom / pan / relative(1h, 24h) / absolute 모두 지원
- saved view / query 저장 가능
- 모션 최소화: 120–200ms, ease-standard — alert blink 금지, 상태는 텍스트 + 색
- 파괴적 액션(인시던트 close, rule 삭제)은 2단계 confirm + audit

## 색상 전략
- surface: cool neutral + 미묘한 blue tint, **dark mode 1급**
- primary: **Azure Blue** — realtime/live 상태 강조 1종
- accent: **Emerald Green** — healthy / success 상태
- surface_tint: **Ice Blue** — chart 배경·row hover 피로감 최소화
- semantic: success / warning / danger / info 4 role, severity 에 매핑
- **alert 는 항상 색상 + 라벨 이중 표기** — 색맹 대응
- dark surface: 순수 #000 대신 deep cool neutral (눈 피로)

## 타이포그래피
- heading / body: **Inter** (영문) / **Pretendard** (한글)
- mono: **JetBrains Mono** — metric value, log line, trace id, timestamp 핵심
- scale: xs/sm/md/lg/xl/2xl/3xl — 12–26px 중심 (dense 우선)
- line-height: tight(1.2) / normal(1.45) / relaxed(1.6)
- tabular-nums 항상 활성화 (시계열 / 통계)

## 접근성
- WCAG 2.2 AA (본문 대비 4.5:1, UI 3:1)
- severity 는 색 + 텍스트 라벨 이중 (색맹 대응 필수)
- aria-live 로 critical alert 알림
- focus ring 항상 표시, 키보드 trap 금지
- live-update 동안 스크린리더 과도 알림 방지 — throttle

## 한글 대응
- Pretendard variable (woff2) 번들
- 숫자는 JetBrains Mono 고정 — tabular-nums
- 자간: 한글 -1%, 영문 0
- 한국어 severity 라벨: "치명/심각/주의/정보" + 영문 병기 허용

## 주의사항
- 이 프리셋은 **monitoring-ops--minimal-tech (P1, devtools/ko)** — 실시간 운영 특화
- "관리 대시보드" 제품(프로젝트/이슈 관리)은 `dashboard--minimal-tech` 사용
- 마케팅/커머스/문서 제품에는 부적합
- 이미지 기반 힌트는 advisory, 구조적 결정은 spec + KB 우선
- 실제 모니터링 백엔드 / 시계열 DB / alert 라우팅은 프리셋 범위 외 — 시각 시스템만 다룸
