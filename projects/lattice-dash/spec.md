# Lattice-Dash — B2C Startup Admin Dashboard Spec

## 제품 개요
Lattice-Dash 는 B2C 스타트업 운영팀을 위한 **bold-confident 톤 admin console (대시보드/관리자)** 이다.
Retool / Appsmith / Stripe Radar / PostHog / Plausible / Mixpanel 계열의 **sidebar-nav · workspace-switcher ·
data-table · kpi-card · filter-chip · command-palette · activity-feed · activation-funnel · cohort-matrix ·
retention-chart · conversion-funnel · referral-widget · experiment-panel · goal-tracker · user-list ·
ticket-queue · alert-list · segment-filter** 를 vivid Ultra Violet primary + Illuminating yellow accent
impact typography 로 한 화면에 모은다. 이 프리셋은 "fintech enterprise 신뢰 관리자"(dashboard--corporate-trust)
도 아니고 "editorial 큐레이션 대시보드"(dashboard--editorial-warm) 도 아니며 "SRE observability"
(monitoring-ops--minimal-tech) 도 아닌, **"젊은 B2C 스타트업 그로스 admin"** 정체성이다. 한국어 UI 를 1급으로 지원한다.

## 사용자
- **B2C 스타트업 그로스 매니저 / 프로덕트 매니저**: activation funnel · cohort retention · A/B 실험 결과 · 전환율
- **스타트업 CEO / 파운더**: 주간 MAU / DAU / ARPU / goal-tracker · 투자자 리포트용 impact KPI
- **커뮤니티 / 지원 리드**: user-list · ticket-queue · alert-list · incident 운영 큐

## 핵심 화면
1. **Workspace Home (그로스 홈)** — sidebar-nav + workspace-switcher + kpi-card grid (MAU/DAU/Activation%/Retention%/ARPU/Conversion%) + activity-feed + goal-tracker
2. **Activation (활성화)** — activation-funnel (4–6 stage, vivid Ultra Violet primary active stage + Illuminating yellow complete + drop-off muted) + segment-filter + filter-chip + experiment-panel
3. **Cohort Retention (코호트 리텐션)** — cohort-matrix (heat-scale Ultra Violet deepest → Creamsicle lightest) + retention-chart + segment-filter + data-table
4. **Referral (레퍼럴)** — referral-widget (share CTA saturated Illuminating + referral-link copy + reward tracker) + kpi-card (referrals / viral coefficient / k-factor)
5. **Experiments (실험)** — experiment-panel (A/B variant card + uplift + confidence + winner Illuminating badge) + goal-tracker + data-table
6. **Users (유저 리스트)** — user-list + segment-filter + filter-chip + row-actions + ticket-queue 진입
7. **Tickets / Alerts (운영 큐)** — ticket-queue + alert-list + data-table row-actions + command-palette 진입
8. **Conversion (전환)** — conversion-funnel + kpi-card + segment-filter + filter-chip
9. **Settings / Team** — sidebar-nav 2-level + workspace-switcher + member-roster + settings-panel

## UI 컴포넌트 (도출)
- **app-shell** — 전체 admin layout, sidebar + topbar + workspace
- **sidebar-nav** — 2-level collapsible, active state vivid Ultra Violet fill + Illuminating underline
- **workspace-switcher** — top-left workspace picker, team / env / app 전환
- **topbar** — 검색 + command-palette shortcut + 알림 + 유저 메뉴
- **breadcrumb** — 현재 위치 hierarchical
- **tab-bar** — 섹션 내 sub-tab 전환
- **command-palette** — ⌘K 글로벌, fuzzy search + recent, Ultra Violet focus ring
- **data-table** — dense admin table, sticky header, sortable column, row-actions, activation/retention row hover
- **column-header** — sortable column, filter-chip 진입
- **row-actions** — 행별 ... 메뉴 (view / edit / archive / ticket)
- **pagination** — prev/next + page input, mono tabular-nums
- **filter-chip** — active filter chip, Ultra Violet outline + Illuminating chip bg active
- **filter-bar** — 상단 sticky filter bar, segment-filter 통합
- **segment-filter** — 코호트/유저 세그먼트 필터, saved-segment dropdown + new-segment
- **search-field** — dashboard 내 검색 field, autocomplete
- **kpi-card** — MAU/DAU/Activation/Retention/ARPU, 큰 impact metric + delta + sparkline, Illuminating positive + muted negative
- **insight-card** — 주요 인사이트 요약 카드 (e.g. "Activation up 12% WoW")
- **activity-card** — 최근 활동 피드 카드
- **activity-feed** — time-grouped activity stream, avatar + action + diff
- **activation-funnel** — 4–6 stage funnel, vivid Ultra Violet primary active + Illuminating complete + muted drop-off + stage 퍼센트 mono
- **cohort-matrix** — week/day cohort retention matrix, heat-scale Ultra Violet deepest → Creamsicle lightest
- **retention-chart** — line/area chart for retention curve, Illuminating baseline + Ultra Violet active
- **conversion-funnel** — marketing/commerce conversion funnel, 4 stage + drop-off rate
- **referral-widget** — share CTA + referral-link copy + reward tracker, saturated Illuminating primary CTA
- **experiment-panel** — A/B variant card grid, variant + uplift + confidence + Illuminating winner badge + Ultra Violet confidence ring
- **goal-tracker** — 목표 progress bar + 완료 checkmark + Illuminating complete fill + kpi delta
- **user-list** — user data-table, avatar + email + signup + segment tag-pill + last-active
- **ticket-queue** — 지원 티켓 queue, status-badge + priority + assignee + last-activity
- **alert-list** — incident / alert list, severity + source + ack button + saturated danger
- **stat-card** — 단일 수치 card variant
- **section-header** — 대시보드 section header (workspace-header 계열), Space Grotesk 700 impact
- **workspace-header** — 상단 workspace name + action group + share
- **status-badge** — semantic badge (success/warning/danger/info) + saturated primary variant
- **tag-pill** — 세그먼트/카테고리 tag pill row
- **toast** — 일시적 성공/에러 toast, impact entry, Illuminating 성공 + danger 에러
- **inline-alert** — 페이지 내 banner (공지/경고), saturated accent outline
- **empty-state** — 데이터 없을 때 illustration + "세그먼트를 만들어 보세요" CTA, Creamsicle warm surface
- **banner** — 전역 상단 공지 banner, Ultra Violet outline
- **modal-dialog** — 확인 / 생성 / 설정 modal
- **bottom-sheet** — 모바일용 하단 sheet
- **confirm-dialog** — 삭제/위험 작업 confirm, saturated danger
- **text-field** — 단일 줄 입력
- **textarea** — 여러 줄 입력
- **select** — 드롭다운 select
- **checkbox** — 체크박스
- **radio-group** — 라디오 그룹
- **form-section** — 폼 section 그룹 + label
- **form-actions** — 폼 하단 제출/취소 영역
- **text-input-with-unit** — 값 + unit (%, days) input
- **date-picker** — 날짜 선택, 코호트/리텐션 기간
- **date-range-picker** — 기간 선택, 대시보드 전역 필터
- **calendar-grid** — 월간 캘린더, 이벤트 표시
- **time-picker** — 시간 선택
- **chart-container** — 차트 래퍼 (타이틀 + 범례)
- **chart-tooltip** — 데이터 포인트 호버 상세
- **chart-legend** — 차트 범례
- **avatar** — 멤버 프로필 이미지/이니셜
- **user-menu** — 사용자 드롭다운 메뉴
- **profile-card** — 사용자 프로필 요약 (drawer 미리보기)
- **comment-thread** — ticket 댓글 스레드
- **comment-input** — 댓글 입력 + mention autocomplete
- **mention-popup** — @멘션 popup
- **primary-button** — saturated Ultra Violet primary CTA, impact label, white text, 4.5:1 대비
- **secondary-button** — hairline Ultra Violet outline, ghost hover
- **ghost-button** — 텍스트 링크 스타일, Illuminating hover underline
- **icon-button** — 아이콘 전용 (star / archive / share / more)
- **link-button** — 텍스트 링크 CTA
- **chip** — 선택/해제 chip

## 인터랙션 원칙
- **키보드 우선**: ⌘K, ⌘/, j/k 행 네비게이션, s 세그먼트 바로가기, a activation 바로가기
- **saturated primary CTA**: primary-button / add-to-cart-like / referral share CTA 는 Ultra Violet 포화색 fill, hover 시 2% 상승
- **impact toast**: 성공 / 완료 / 승리 toast 는 Illuminating 배경 + impact ease-out, 에러는 saturated danger
- **activation funnel drill**: stage hover 시 drop-off 상세 tooltip + 클릭 시 해당 user-list drill-down
- **cohort matrix hover**: cell hover 시 해당 코호트 user count + retention% tooltip, click 시 user-list 진입
- **referral share action**: share CTA 클릭 시 referral-link 복사 + Illuminating flash + toast 성공
- **filter chip active**: active filter-chip 은 Illuminating fill + Ultra Violet text, 제거 X 아이콘
- **hover-emphasis row**: data-table row hover 시 Creamsicle warm surface + Ultra Violet left-border rule
- **goal-tracker complete**: 100% 도달 시 Illuminating fill + confetti 모션 (prefers-reduced-motion 존중)
- **experiment winner**: winner variant card 상단 Illuminating badge + Ultra Violet confidence ring
- **motion**: 전반 150–220ms ease-out-expo (bold-confident 특유 에너제틱 모션), prefers-reduced-motion 존중
- **bold hover**: 버튼 hover 는 saturated 색상 강화 + 그림자 강조, 1–2px 상승

## 색상 전략
- **primary**: **Ultra Violet (#5F4B8B)** — 2018 Pantone, vivid deep purple, sidebar-nav active / primary-button / activation-funnel active stage / cohort-matrix heat deepest / command-palette focus / KPI delta 강조
- **accent**: **Illuminating (#F5DF4D)** — 2021 Pantone, vivid yellow, activation callout / referral-widget share CTA / goal-tracker complete / experiment-panel winner / impact toast 성공 / filter-chip active fill
- **surface_tint**: **Creamsicle (#FFD7A0)** — warm cream surface, KPI card 보조 surface / empty-state illustration / filter-chip soft group bg / data-table row hover, admin dense row 는 near-white 기본 surface 유지
- **semantic**: success(Illuminating variant) / warning(Amber) / danger(saturated Crimson-ish) / info(Ultra Violet variant) 4 role
- **high-contrast headline** — KPI 숫자는 near-black, workspace-header 는 Space Grotesk 700 impact, saturated primary 위 텍스트는 화이트 4.5:1
- **dense admin density** — data-table row 48–56px, kpi-card padding 16–20px, admin dense 유지하면서 bold 정체성은 accent 에서 뽑음
- **full-bleed section header** — section-header 는 Ultra Violet 얇은 base rule + saturated primary accent
- **saturated primary CTA** — primary-button Ultra Violet fill, hover 2% 상승, Illuminating focus ring
- **dark mode**: deep cool neutral (not pure black) + tuned Ultra Violet/Illuminating 채도 낮춤, data-table row separator hairline
- **기존 15종 프리셋 HEX 와 겹침 0** — Ultra Violet #5F4B8B / Illuminating #F5DF4D / Creamsicle #FFD7A0 조합

## 타이포그래피
- **heading**: **Space Grotesk** (영문) / **Pretendard** (한글) — geometric sans with impact, workspace-header / section-header / KPI metric headline / activation-funnel stage label, serif 금지
- **body**: **Inter / Pretendard** — dense data-table cell / filter-chip / ticket row / referral copy / empty-state / tooltip 공용, line-height 1.4–1.5 (admin dense)
- **mono**: **JetBrains Mono** — MAU / DAU / activation% / retention% / ARPU / conversion% / row-id / timestamp / delta — tabular-nums 영문 고정
- **scale**: xs(11) / sm(12) / md(14) / lg(16) / xl(20) / 2xl(24) / 3xl(32) / 4xl(48)
- **workspace-header**: 2xl–3xl (24–32px), heading 700, letter-spacing tight
- **kpi metric headline**: 3xl–4xl (32–48px), heading 700 mono tabular-nums
- **section-header**: xl–2xl (20–24px), heading 600
- **data-table cell**: sm–md (12–14px), body 400–500, line-height 1.4 keep-all
- **filter-chip**: xs–sm (11–12px), body 500
- **activation-funnel stage label**: md–lg (14–16px), heading 600
- **cohort-matrix cell**: xs (11px), mono tabular-nums 500
- **한글 line-height**: 1.4 (data-table dense), 1.5 (kpi-card / referral copy), keep-all
- **tabular-nums**: MAU / DAU / retention / activation / conversion / ARPU / delta / row-id / timestamp 전용
- **impact headline** — workspace-header / kpi metric headline 은 letter-spacing -1%, 한글은 letter-spacing 0

## 접근성
- WCAG 2.2 AA (본문 대비 4.5:1, UI 3:1, saturated Ultra Violet 위 텍스트는 화이트 5:1)
- primary-button / add-to-cart-like CTA focus 는 Illuminating outline + 2px offset (키보드 가시성)
- data-table row 는 role="row", cell role="cell", keyboard j/k 네비
- command-palette 는 role="dialog" + aria-modal + focus trap + ESC 닫힘
- cohort-matrix 는 cell 별 aria-label (코호트 + 리텐션%)
- activation-funnel 은 stage 별 aria-label + 퍼센트 텍스트 대체
- toast 는 aria-live="polite" + impact entry 에도 focus 이동 금지
- prefers-reduced-motion 존중 — confetti, row hover slide, filter-chip bump 제거
- kbd shortcut 은 visible + role="kbd" 표시

## 한글 대응
- Pretendard variable (woff2) 번들, heading/body 공용
- 한글 data-table cell / filter-chip / empty-state / ticket row / activation stage label line-height **1.4–1.5**, letter-spacing 0
- workspace-header / section-header 는 Pretendard 700 letter-spacing -1%
- word-break: **keep-all**, overflow-wrap: break-word
- MAU/DAU/activation%/retention%/conversion%/ARPU/row-id/timestamp 는 mono 영문 고정 (한글 혼용 금지), tabular-nums
- 한국어 라벨: "활성화 / 리텐션 / 코호트 / 레퍼럴 / 세그먼트 / 전환 / 실험 / 승자 / 티켓 / 알람 / 목표" + 영문 "activation / retention / cohort / referral / segment / conversion / experiment / winner / ticket / alert / goal" 병기 허용

## 주의사항
- 이 프리셋은 **dashboard--bold-confident (P3)** — 젊은 B2C 스타트업 운영 대시보드 특화
- "fintech 보수 관리자" 는 `dashboard--corporate-trust`
- "SRE / DevOps observability 콘솔" 은 `monitoring-ops--minimal-tech`
- "editorial 큐레이션 운영 대시보드" 는 `dashboard--editorial-warm`
- "한국어 SaaS 관리자 콘솔 minimal" 은 `dashboard--minimal-tech`
- "소비자 wellness / habit admin playful" 은 `dashboard--playful-soft`
- "bold streetwear commerce" 는 `commerce--bold-confident`
- "bold magazine opinion" 은 `document-content--bold-confident`
- "bold sports marketing landing" 은 `marketing-landing--bold-confident`
- 이미지 기반 힌트는 advisory — 구조는 spec + KB 우선
- 실제 백엔드 (auth / user DB / event pipeline / experiment engine / push) 는 프리셋 범위 외 — admin chrome + visual system 만 다룸
