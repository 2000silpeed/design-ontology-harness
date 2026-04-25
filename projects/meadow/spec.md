# Meadow — Consumer Wellness / Habit Admin Dashboard Spec

## 제품 개요
Meadow 는 consumer wellness · habit · 가계부 · 명상 · 수면 tracking 앱을 운영하는 운영팀을 위한
**playful-soft 톤 admin console (대시보드/관리자)** 이다. Cal.com / Notion / Flo / Finch / Calm / Headspace
계열의 **sidebar-nav · workspace-switcher · dashboard-card · kpi-card · data-table · filter-chip ·
streak-indicator · habit-calendar · wellness-score · mood-check · session-tracker · insight-card ·
goal-tracker · gentle-toast · soft-dialog · user-list · cohort-matrix · retention-chart · activity-feed ·
settings-panel** 을 warm Periwinkle primary + Peach Puff accent + Mauve dreamy surface 로 엮어
"부드럽게 habit/wellness 를 관찰" 하는 admin 경험을 제공한다. 이 프리셋은 "bold startup 그로스 admin"
(dashboard--bold-confident) 도 아니고 "fintech 신뢰 관리자"(dashboard--corporate-trust) 도 아니며
"SaaS 미니멀 콘솔"(dashboard--minimal-tech) 도 아닌, **"컨슈머 wellness mindful admin"** 정체성이다.
한국어 UI 를 1급으로 지원한다.

## 사용자
- **Consumer wellness / habit 앱 운영 PM**: 유저 streak · mood · session · 수면 시간 · 명상 분 관찰
- **웰니스 스타트업 운영자 / 커뮤니티 리드**: cohort retention + wellness score + habit calendar 관리
- **가계부 · 저축 · 목표 트래킹 앱 admin**: goal tracker + streak indicator + gentle nudge 운영

## 핵심 화면
1. **Workspace Home (웰니스 홈)** — sidebar-nav + workspace-switcher + dashboard-card grid (wellness-score / streak 상위 / mood 평균 / session 합계 / goal 달성률) + insight-card + activity-feed
2. **Habits (습관 관리)** — habit-calendar grid (week × day, streak heat-scale Periwinkle lightest → Mauve deepest) + streak-indicator + filter-chip + goal-tracker + data-table
3. **Mood / Check-in (기분 체크인)** — mood-check quick-select (emoji or color gradient Peach Puff → Periwinkle) + retention-chart + insight-card + cohort-matrix
4. **Wellness Score (웰니스 스코어)** — wellness-score gauge/ring (Periwinkle base + Peach Puff highlight) + session-tracker + kpi-card + filter-chip
5. **Sessions (명상/수면 세션)** — session-tracker + data-table + filter-chip + goal-tracker + retention-chart
6. **Users (유저 리스트)** — user-list + soft filter-chip + row-actions + profile-card drawer
7. **Goals (목표 트래킹)** — goal-tracker grid + habit-calendar 진입 + celebration 모션
8. **Insights (인사이트)** — insight-card stack + retention-chart + cohort-matrix + activity-feed
9. **Settings / Team** — sidebar-nav 2-level + workspace-switcher + member-roster + settings-panel

## UI 컴포넌트 (도출)
- **app-shell** — 전체 admin layout, sidebar + topbar + workspace, rounded 12–16 surface
- **sidebar-nav** — 2-level collapsible, active state Periwinkle soft fill + rounded pill highlight
- **workspace-switcher** — top-left workspace picker (team / app / env)
- **topbar** — 검색 + command-palette shortcut + 알림 + 유저 메뉴, soft border
- **breadcrumb** — hierarchical 현재 위치, soft chevron
- **tab-bar** — 섹션 sub-tab 전환, rounded pill tab
- **command-palette** — ⌘K, fuzzy search + recent, Periwinkle focus ring
- **data-table** — soft admin table, soft row divider (hairline Mauve), row hover Mauve surface + Periwinkle left-rule, column sort
- **column-header** — sortable column, Nunito 600
- **row-actions** — 행별 ... (view / edit / nudge / archive), soft-dialog 진입
- **pagination** — prev/next + page dot, mono tabular-nums
- **filter-chip** — rounded pill chip, active Periwinkle soft fill + Peach Puff border
- **filter-bar** — 상단 soft filter bar, segment filter 통합
- **segment-filter** — 코호트/유저 세그먼트 필터, saved-segment dropdown
- **search-field** — dashboard 내 검색 field + autocomplete
- **dashboard-card** — soft rounded card, Periwinkle hairline + Mauve hover, 주요 섹션 카드 wrap
- **kpi-card** — wellness-score / streak / mood 평균 / session 합 / goal%, Nunito 700 metric + Peach Puff delta positive
- **insight-card** — 주요 인사이트 ("이번 주 평균 수면이 20분 늘었어요") illustration + soft Mauve surface
- **activity-card** — 최근 유저 활동 카드 (signup / streak break / goal reach)
- **activity-feed** — time-grouped activity stream, rounded avatar + soft divider
- **streak-indicator** — 연속 일수 indicator, Peach Puff flame + mono days + Periwinkle ring
- **habit-calendar** — week × day grid, 완료/미완료/streak-break 시각화, heat-scale Periwinkle lightest → Mauve deepest, today cell Peach Puff ring
- **wellness-score** — gauge or ring, Periwinkle base + Peach Puff highlight + mono score text, soft radial gradient
- **mood-check** — quick-select emoji or color gradient (Peach Puff happy → Periwinkle calm → Mauve thoughtful → deep neutral low)
- **mood-chart** — mood 시계열 line/area chart, Periwinkle primary
- **session-tracker** — session card (명상/수면/운동), 지속 시간 mono + Peach Puff complete pill
- **session-timeline** — 하루 session stack, 시간대별 블록, rounded
- **goal-tracker** — 목표 progress bar + Peach Puff complete fill + celebration 모션 (prefers-reduced-motion 존중)
- **goal-grid** — 여러 목표 card grid, rounded
- **cohort-matrix** — cohort retention matrix, heat-scale Periwinkle lightest → Mauve deepest, rounded cell, cell hover soft tooltip
- **retention-chart** — retention 곡선 line/area, Periwinkle primary + Peach Puff baseline
- **user-list** — user data-table, rounded avatar + email + signup + segment tag-pill + last-active
- **stat-card** — 단일 수치 card variant
- **section-header** — Nunito 700 section header + soft divider
- **workspace-header** — 상단 workspace name + action group + share, soft shadow
- **status-badge** — semantic badge (success/warning/danger/info) + soft variant
- **tag-pill** — 세그먼트/카테고리 rounded tag pill
- **gentle-toast** — low-noise 성공/완료 toast, playful-soft 모션 (120–200ms), Peach Puff 성공 · soft danger 실패
- **inline-alert** — 페이지 내 banner, rounded Mauve outline
- **empty-state** — 데이터 없을 때 illustration + 친근 카피 ("첫 습관을 추가해 보세요") + Mauve warm surface
- **banner** — 전역 상단 banner, rounded Mauve soft fill
- **soft-dialog** — rounded-16 dialog, 파괴적 액션도 부드럽게 confirm
- **bottom-sheet** — 모바일용 하단 sheet, rounded-top
- **confirm-dialog** — 삭제/위험 작업 confirm, soft danger
- **text-field** — 단일 줄 입력, rounded 12
- **textarea** — 여러 줄 입력, rounded 12
- **select** — 드롭다운 select
- **checkbox** — 체크박스
- **radio-group** — 라디오 그룹
- **form-section** — 폼 section 그룹 + label
- **form-actions** — 폼 하단 제출/취소 영역
- **date-picker** — 날짜 선택, habit/session 기간
- **date-range-picker** — 기간 선택
- **calendar-grid** — 월간 캘린더 grid, habit-calendar 기반
- **time-picker** — 시간 선택
- **chart-container** — 차트 래퍼 (타이틀 + 범례)
- **chart-tooltip** — 데이터 포인트 호버 soft tooltip
- **chart-legend** — 차트 범례
- **avatar** — 친근 rounded avatar, illustration fallback
- **user-menu** — 사용자 드롭다운, soft border
- **profile-card** — 사용자 프로필 요약 drawer
- **comment-thread** — 운영 노트 / ticket 스레드
- **comment-input** — 댓글 입력 + mention autocomplete
- **mention-popup** — @멘션 popup, soft shadow
- **primary-button** — Periwinkle soft fill primary CTA, rounded-full, gentle hover 2% 상승
- **secondary-button** — Periwinkle hairline outline, soft hover
- **ghost-button** — 텍스트 링크, soft hover underline
- **icon-button** — 아이콘 전용 (heart / archive / nudge / more), rounded
- **link-button** — 텍스트 링크 CTA
- **chip** — 선택/해제 rounded chip

## 인터랙션 원칙
- **gentle nudge**: 유저에게 nudge 발송 시 soft-dialog 로 확인 + gentle-toast 성공
- **habit streak celebration**: streak-indicator 도달 (7일/30일/100일) 시 Peach Puff flame 애니메이션 + gentle-toast (prefers-reduced-motion 존중)
- **mood-check quick-select**: emoji/color 한 번 탭으로 기록, 즉시 반영 optimistic + soft rollback
- **habit-calendar cell**: 완료 cell tap → Periwinkle fill bounce, 해제 → fade out
- **wellness-score animated**: score 변경 시 ring gradient 부드럽게 회전 (200–320ms ease-out)
- **goal complete**: goal-tracker 100% 도달 시 Peach Puff fill + confetti soft (prefers-reduced-motion 존중)
- **swipe archive**: 알림/ticket 좌스와이프 → archive, 우스와이프 → unread
- **pull-to-refresh**: 모바일 피드/리스트 상단 스와이프 → 새로고침 soft bounce
- **soft motion**: 전반 120–240ms ease-out, rounded bounce 살짝, decorative animation 최소
- **파괴적 액션**(유저 삭제, habit 제거)은 soft-dialog 로 부드럽게 confirm
- **이모지 혼용**: 한국어 본문 + 이모지 혼용 자연스럽게, mood-check 는 이모지 1급

## 색상 전략
- **warm pastel surface** — Mauve 소프트 베이스 + Creamy highlights, 장시간 admin 열람 피로감 최소화
- **primary**: **Periwinkle (#8E9AF1)** — 푸른빛 웜 퍼플, sidebar-nav active / primary-button / streak-indicator ring / wellness-score base / habit-calendar today cell / goal-tracker progress fill / insight-card outline
- **accent**: **Peach Puff (#FFDAB9)** — warm pastel 오렌지, mood-check happy state / habit-streak flame / gentle-toast 성공 / goal-tracker complete fill / kpi delta positive
- **surface_tint**: **Mauve (#E0B0FF)** — dreamy pastel violet-rose, dashboard-card hover surface / empty-state illustration / filter-chip soft group bg / row hover / insight-card warm surface
- **semantic**: success(Peach Puff variant) / warning(soft amber) / danger(soft coral) / info(Periwinkle variant) 4 role — gentle-toast · badge 에 매핑
- **rounded-first** — 모든 컴포넌트 corner radius 12–16, button radius full 기본, dashboard-card radius 16
- **soft shadow** — 0 2px 8px rgba(0,0,0,0.04) / 0 4px 12px rgba(0,0,0,0.06), 깊은 elevation 금지
- **dark mode**: warm deep neutral (not pure black) + 채도 낮춘 Periwinkle / Peach Puff + Mauve soft border
- **minimal-tech · corporate-trust 의 cool 무채색 팔레트와 정반대** — warm + rounded + dreamy pastel
- **기존 15종 프리셋 HEX 와 겹침 0** — Periwinkle #8E9AF1 / Peach Puff #FFDAB9 / Mauve #E0B0FF 조합

## 타이포그래피
- **heading**: **Nunito** (영문, rounded sans) / **Pretendard** (한글) — geometric sans 금지, serif 금지, workspace-header / section-header / kpi-card label / insight-card title / goal-tracker label / mood-check label
- **body**: **Inter / Pretendard** — data-table cell / filter-chip / activity-feed / mood-check 본문, line-height 1.5–1.6 (dashboard soft) / ko 1.6
- **mono**: **JetBrains Mono** — streak days / wellness score / mood avg / session minutes / habit count / timestamp, tabular-nums 영문 고정, 최소 사용
- **scale**: xs(12) / sm(13) / md(14) / lg(16) / xl(20) / 2xl(24) / 3xl(32) / 4xl(40)
- **workspace-header**: 2xl–3xl (24–32px), Nunito 700, letter-spacing 0
- **kpi metric headline**: 3xl–4xl (32–40px), Nunito 700 mono tabular-nums
- **section-header**: xl–2xl (20–24px), Nunito 700
- **insight-card title**: lg–xl (16–20px), Nunito 600, 친근 카피 포함
- **data-table cell**: sm–md (13–14px), body 400–500, line-height 1.5 keep-all
- **filter-chip**: xs–sm (12–13px), body 500 rounded pill
- **habit-calendar cell**: xs (12px), mono tabular-nums 500
- **wellness-score number**: 3xl–4xl (32–40px), Nunito 700 mono tabular-nums
- **mood-check emoji**: xl–2xl (20–24px) emoji + sm (13px) label
- **한글 line-height**: 1.5 (data-table dense), 1.6 (insight-card / kpi-card / mood-check / habit-calendar), keep-all
- **tabular-nums**: streak / wellness-score / mood-avg / session-min / habit-count / timestamp / goal-% 전용
- **rounded warmth** — workspace-header / section-header 는 Nunito 700 letter-spacing 0 (impact 대신 warmth)

## 접근성
- WCAG 2.2 AA (본문 대비 4.5:1, UI 3:1)
- Periwinkle 위 텍스트는 화이트 대비 4.5:1 확보 (짙은 주요 영역에만 fill)
- Peach Puff 위 텍스트는 near-black (파스텔 위는 어두운 글자)
- primary-button focus 는 Periwinkle outline + 2px offset (키보드 가시성)
- mood-check 는 이모지 + 색상 + 텍스트 라벨 3중 (색 단독 금지)
- wellness-score gauge 는 role="progressbar" + aria-valuenow + 텍스트 대체
- habit-calendar cell 은 aria-label (날짜 + 완료 여부 + streak 상태)
- streak-indicator 는 mono days 외 "연속 N일" 텍스트 명시
- soft-dialog 는 focus trap + ESC 취소
- gentle-toast 는 aria-live="polite"
- prefers-reduced-motion 존중 — celebration, streak bounce, score gradient 회전 제거
- 이모지 picker 는 키보드 grid navigation 지원

## 한글 대응
- Pretendard variable (woff2) 번들, heading/body 공용
- 한글 data-table cell / filter-chip / mood-check / empty-state / insight-card / goal-tracker line-height **1.5–1.6**, letter-spacing 0
- workspace-header / section-header 는 Pretendard 700 letter-spacing 0 (rounded warmth)
- word-break: **keep-all**, overflow-wrap: break-word
- streak-days / wellness-score / mood-avg / session-minutes / habit-count / timestamp 는 mono 영문 고정 (한글 혼용 금지), tabular-nums
- 한국어 라벨: "습관 / 연속 / 웰니스 점수 / 기분 / 세션 / 명상 / 수면 / 목표 / 인사이트 / 팀" + 영문 "habit / streak / wellness score / mood / session / meditation / sleep / goal / insight / team" 병기 허용
- 친근 카피 톤: "좋은 하루 보내세요" / "첫 습관을 시작해 보세요" / "이번 주 평균이 조금 늘었어요" (enterprise 어휘 회피)

## 주의사항
- 이 프리셋은 **dashboard--playful-soft (P3)** — consumer wellness / habit admin 특화
- "B2C 스타트업 그로스 admin (vivid bold)" 은 `dashboard--bold-confident`
- "fintech 보수 관리자" 는 `dashboard--corporate-trust`
- "SRE / DevOps observability 콘솔" 은 `monitoring-ops--minimal-tech`
- "editorial 큐레이션 운영 대시보드" 는 `dashboard--editorial-warm`
- "한국어 SaaS 관리자 콘솔 minimal" 은 `dashboard--minimal-tech`
- "친근 커뮤니티 피드 · 쓰레드 · 알림" 은 `community-feed--playful-soft`
- "AI 코파일럿 채팅 writing" 은 `conversation-copilot--editorial-warm` 또는 `--minimal-tech`
- "매거진 reading / long-form" 은 `document-content--editorial-warm`
- 이미지 기반 힌트는 advisory — 구조는 spec + KB 우선
- 실제 백엔드 (auth / habit engine / notification / wellness ML / push) 는 프리셋 범위 외 — admin chrome + visual system 만 다룸
