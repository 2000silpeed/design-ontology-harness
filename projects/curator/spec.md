# Curator — Editorial-Warm Publishing Dashboard Spec

## 제품 개요
Curator 는 매거진/뉴스룸 편집부 · 출판사 편집팀 · content studio 운영자를
위한 **editorial-warm 톤 dashboard (대시보드/관리자 — sidebar · data table ·
KPI card · filter chrome)** 이다.
Ghost / Substack / Medium / Readwise / Notion / Buttondown 계열의
**editorial curation dashboard · publishing workflow** 패턴을 묶어
"오늘의 큐 → 이슈 플래너 → 발행 파이프라인 → 기고자 로스터 → 리딩 애널리틱스 →
아카이브" 의 editorial 운영 흐름을 sidebar-nav · topbar · data-table ·
kpi-card · filter-chip · curation-queue · editorial-calendar ·
publishing-pipeline · contributor-roster · article-preview-pane ·
editorial-analytics-kpi · reading-analytics-kpi · archive-shelf ·
tag-taxonomy-manager · draft-status-pill · issue-planner · schedule-cell 로
구현한다.
이 프리셋은 "minimal-tech 개발자 SaaS 운영 콘솔 (orbit)" 이나 "fintech 신뢰
대시보드 (ledger)" 가 아니라 **"warm neutral + muted accent + serif heading
+ reading-first calm chrome"** 의 editorial 큐레이션/퍼블리싱 dashboard
성향으로, warm neutral sidebar · serif heading pair · muted editorial
accent · reading-first data table · calm kpi card · soft cream surface ·
restrained editorial chrome · long-form article preview drawer 를 시각
정체성으로 고정한다. 한국어 UI 를 1급으로 지원한다.

## 사용자
- **매거진/뉴스룸 에디터**: sidebar-nav · curation-queue · filter-chip · data-table · draft-status-pill · contributor avatar · comment-thread 를 통해 오늘의 큐 검토 · 피어 리뷰 · 스케줄 확정
- **출판사 편집장/편집자**: editorial-calendar 그리드 · schedule-cell · issue-planner · publishing-pipeline stage · contributor-roster · tag-taxonomy-manager 로 분기/연간 호 플래닝과 파이프라인 감독
- **Content Studio 운영자**: editorial-analytics-kpi · reading-analytics-kpi · archive-shelf · kpi-card · activity-card 로 리딩 지표 · 메일 오픈 · 큐레이션 품질 모니터링

## 핵심 화면
1. **Home Overview** — sidebar-nav + topbar + workspace-header + kpi-card row + activity-card + curation-queue preview + issue-planner preview + editorial-analytics-kpi 요약
2. **Curation Queue** — sidebar-nav + filter-sidebar + filter-chip + sort-dropdown + data-table + column-header + row-actions + draft-status-pill + contributor avatar + pagination + search-field
3. **Editorial Calendar** — sidebar-nav + editorial-calendar grid + schedule-cell + issue-planner + publishing-pipeline stage link + contributor-roster preview + date-picker
4. **Publishing Pipeline** — sidebar-nav + publishing-pipeline horizontal board + pipeline-stage card + data-table + status-badge + article-preview-pane drawer + comment-thread
5. **Contributor Roster** — sidebar-nav + data-table + profile-card drawer + comment-thread + tag-taxonomy-manager + avatar cluster + filter-chip
6. **Editorial Analytics** — sidebar-nav + kpi-card + editorial-analytics-kpi + reading-analytics-kpi + chart-container + chart-legend + archive-shelf filter
7. **Archive / Settings** — sidebar-nav + archive-shelf + filter-sidebar + tag-taxonomy-manager + modal-dialog + toast + empty-state

## UI 컴포넌트 (도출)
- **sidebar-nav** — 2단 네비게이션 (워크스페이스 · 큐 · 캘린더 · 파이프라인 · 로스터 · 애널리틱스 · 아카이브 · 설정), warm neutral surface + EB Garamond 섹션 heading, 한글 Pretendard 600
- **topbar** — 상단 바 — workspace switcher · 전역 search-field · quick-filter chip · user-menu · avatar · notification bell, calm 톤
- **workspace-header** — 현재 화면 타이틀 + breadcrumb + primary-button (예: 새 이슈 / 새 초안 / 새 기고자)
- **breadcrumb** — 계층 경로 — 아카이브 > 2026 이슈 > 03월 호 > 피처 초안
- **data-table** — reading-first 톤의 dense 표 — column-header · row hover · row-actions · sortable · filterable · paginated, Naples Yellow row-hover tint · tabular-nums 숫자
- **column-header** — 테이블 컬럼 헤더 — 정렬 토글, muted warm divider
- **row-actions** — 행별 kebab 메뉴 — 초안 편집 · 리뷰어 지정 · 스케줄 · 아카이브
- **pagination** — 페이지 이동 — mono tabular-nums, ghost-button 스타일
- **filter-sidebar** — 좌측 필터 사이드바 — 섹션 · 상태 · 기고자 · 태그 · 이슈 · 날짜 범위, calm 톤 label
- **filter-chip** — 활성 필터 chip — Aubergine outline · Blush resting fill · Naples Yellow focus glow
- **sort-dropdown** — 정렬 dropdown — 최신/오래된/읽힘순/우선순, restrained sort indicator
- **search-field** — 전역/로컬 검색 필드 — autocomplete 동반, muted warm border
- **kpi-card** — sidebar-nav 상단 kpi-card row — 오늘의 초안 수 · 발행 예정 수 · 활성 기고자 수 · 읽기 완독률, mono 숫자 tabular-nums + Naples Yellow trend indicator
- **stat-card** — kpi-card 변형 — 단일 수치 강조 (월간 큐레이션 수 등)
- **insight-card** — 큐레이션 인사이트 카드 — "이번 주 최다 읽힘" · "편집 파이프라인 체증 구간" 같은 insight
- **activity-card** — 최근 activity feed 카드 — 초안 제출 / 리뷰 완료 / 스케줄 확정 / 발행
- **section-header** — 대시보드 섹션 구분 heading — EB Garamond 600 / Pretendard 700
- **tag** — 분류 태그 — 섹션/카테고리/시리즈 (muted Aubergine fill)
- **status-badge** — 초안 상태 뱃지 — 아이디어 / 초안 / 리뷰 / 스케줄 / 발행 / 보류 / 아카이브
- **chip** — filter-chip 공용 — 기고자 / 시리즈 / 태그
- **comment-thread** — article-preview-pane drawer 내 에디터 간 코멘트 thread — mention-chip + muted warm divider
- **avatar** — 기고자/에디터 프로필 이미지 — 원형, Blush fallback
- **user-menu** — topbar 우측 user 드롭다운 — 프로필 / 워크스페이스 전환 / 설정 / 로그아웃
- **profile-card** — contributor-roster drawer 내 기고자 프로필 카드 — 기고 기사 · 최근 활동 · 구독자 수
- **date-picker** — editorial-calendar / schedule-cell 동반 날짜 선택
- **modal-dialog** — 새 이슈 / 새 초안 / 태그 체계 편집 — focus trap, ESC 닫힘
- **toast** — soft toast — 스케줄 확정 · 발행 완료 · 태그 변경 저장, gentle fade-out
- **empty-state** — 빈 상태 안내 — 일러스트 + gentle 온보딩 copy + suggestion
- **primary-button** — Aubergine primary CTA — 새 이슈 · 새 초안 · 스케줄 확정 · 발행
- **secondary-button** — ghost/secondary CTA — 임시 저장 · 리뷰어 지정 · 보류
- **ghost-button** — 텍스트 링크형 tertiary — 아카이브 이동 · 미리 보기
- **icon-button** — 아이콘 전용 (별표/아카이브/공유/복사)
- **curation-queue** — sidebar-nav + data-table + filter-chip + kpi-card 를 엮는 핵심 큐레이션 큐 — 초안 후보 row · draft-status-pill · 기고자 avatar · 예정 스케줄 · row-actions, warm neutral row · Naples Yellow hover · muted warm divider
- **editorial-calendar** — 주간/월간 편집 캘린더 그리드 — schedule-cell · 이슈/호 · 섹션 라벨 · 발행 일정 · 편집 마감, 한글 요일 라벨 keep-all
- **draft-status-pill** — 초안 상태 pill — 아이디어 / 초안 / 리뷰 / 스케줄 / 발행 / 보류, muted Aubergine / Naples Yellow / Blush 변형
- **publishing-pipeline** — 수평 publishing 파이프라인 보드 — pipeline-stage column (아이디어 → 초안 → 리뷰 → 스케줄 → 발행 → 아카이브), data-table 연계
- **issue-planner** — 분기/연간 호 플래너 — 이슈 row · 섹션 cell · 책임 편집자 avatar · 발행 예정, sidebar-nav + data-table + filter-chip 진입
- **contributor-roster** — 기고자 명단 data-table — 프로필 avatar · 소속 · 기고 섹션 · 최근 활동 · 읽기 수, profile-card drawer 진입
- **article-preview-pane** — row/schedule-cell 클릭 시 우측 슬라이드 reading drawer — article-body 미리보기 · kicker · byline · draft-status-pill · comment-thread, long-form Pretendard line-height 1.6–1.7
- **editorial-analytics-kpi** — 편집 운영 KPI — 이슈 리드 타임 · 리뷰 처리 시간 · 발행 지연율 · 기고자당 발행 수 · 보류 카운트, mono tabular-nums
- **reading-analytics-kpi** — 리딩 KPI — 평균 체류 · 완독률 · 스크롤 심도 · 메일 오픈 · 재방문, mono tabular-nums · Naples Yellow trend indicator
- **archive-shelf** — 과거 이슈 / 발행 기사 아카이브 — filter-sidebar + data-table + kpi-card 조합, issue-number chip + 태그
- **tag-taxonomy-manager** — 섹션/카테고리/태그 체계 편집 — tree + data-table + modal-dialog, muted warm divider

## 인터랙션 원칙
- **calm row hover**: curation-queue / data-table / contributor-roster row hover 시 Blush / Naples Yellow 10% tint, 150ms ease-out (prefers-reduced-motion 시 off)
- **gentle filter chip toggle**: filter-chip 토글 시 Aubergine outline → muted Aubergine fill, 120ms cross-fade
- **slow fade drawer**: article-preview-pane 우측 slide-in 220ms ease-out-expo, reading drawer 진입 (prefers-reduced-motion 시 instant)
- **warm focus ring**: 키보드 focus 시 Aubergine 2px outline + 2px offset (sidebar-nav · data-table · filter-chip · kpi-card)
- **muted mention chip**: comment-thread 내 @mention chip → muted Aubergine fill + profile-card hover 미리보기
- **soft toast**: 스케줄 확정 / 발행 완료 toast 는 gentle fade-in 150ms, 자동 dismiss 4s, Naples Yellow accent border
- **restrained sort indicator**: column-header 정렬 화살표 작고 muted — dashboard dense 유지하되 editorial calm 유지
- **editorial reading drawer transition**: article-preview-pane 에서 article-body 전환 시 line-height 1.5 → 1.6–1.7 로 expand (reading-mode 진입)
- **curation queue drag**: draft row 를 publishing-pipeline stage 로 drag — muted Aubergine ghost row, drop 시 soft spring (reduce-motion 시 instant)
- **schedule cell focus glow**: editorial-calendar schedule-cell focus 시 Naples Yellow glow, 키보드 진입 정확히 2px outline
- **calm motion**: 전반 150–220ms ease-out (editorial calm tempo), prefers-reduced-motion 존중
- **keyboard-first**: sidebar 단축키 · 큐 필터 빠른 전환 · 새 초안 단축키 · 스케줄 확정 단축키 — dashboard 관례 유지

## 색상 전략
- **primary**: **Aubergine (#614051)** — Deep Violets, editorial warm violet-brown, sidebar-nav label · primary-button · filter-chip outline · draft-status-pill default · section-header accent
- **accent**: **Naples Yellow (#FADA5E)** — Pastel Yellows, editorial creamy warm yellow, kpi-card trend indicator · editorial-calendar schedule highlight · row hover tint · filter-chip focus glow · reading-analytics trend
- **surface_tint**: **Blush (#F9C0C4)** — Pastel Reds, connected cream-pink surface, article-preview-pane drawer surface · filter-chip resting fill · empty-state illustration base · toast accent stripe
- **semantic**: success(발행 완료) / warning(스케줄 지연) / danger(보류/철회) / info(편집 공지) 4 role, muted 변형 (과포화 금지)
- **warm neutral sidebar** — sidebar-nav surface 는 warm neutral + Aubergine label + Blush 활성 row tint
- **serif heading pair** — masthead/section-header/workspace-header 는 EB Garamond serif, 한글은 Pretendard 700
- **muted editorial accent** — Aubergine primary 는 절제된 사용, kpi-card / row hover / schedule cell 강조는 Naples Yellow 로 분산
- **reading-first data table** — data-table row line-height 1.5–1.6, column padding 넉넉, muted warm divider, sticky header warm neutral
- **calm kpi card** — kpi-card 는 대문자 이니셜 대신 mixed-case Pretendard/Inter 600, Naples Yellow 작은 trend indicator
- **soft cream surface** — workspace-header / article-preview-pane drawer 는 Blush 5–10% surface tint
- **restrained editorial chrome** — divider 는 hairline muted warm, border-radius 6–8px, shadow 는 12–16 소프트
- **long-form article preview drawer** — article-preview-pane 은 65–75ch reading pane, EB Garamond heading + Pretendard body, line-height 1.6–1.7
- **dark mode**: deep Aubergine surface + tuned Naples Yellow muted + Blush desaturated, data-table row-hover 는 Aubergine 15% tint
- **기존 14종 프리셋 HEX 와 HEX 겹침 0**

## 타이포그래피
- **heading**: **EB Garamond** (영문) / **Pretendard** (한글) — classic book-feel editorial serif — masthead / issue-header / workspace-header / section-header / article-preview-pane heading, Lora (signal-desk) / Source Serif Pro (quill) / Playfair Display (broadside) 와 차별화
- **body**: **Inter / Pretendard** — data-table cell / kpi-card label / filter-chip / row-actions / comment-thread / editorial-analytics / reading-analytics, line-height 1.5–1.6 (dashboard dense 유지)
- **mono**: **JetBrains Mono** — editorial-analytics-kpi 숫자 · reading-analytics-kpi 숫자 · editorial-calendar 날짜 · draft-status-pill timestamp · row ID / issue-number · pagination 숫자, tabular-nums 영문 고정
- **scale**: xs(11) / sm(12) / md(14) / lg(16) / xl(18) / 2xl(24) / 3xl(32)
- **workspace-header / section-header**: 2xl–3xl (24–32px), EB Garamond 700 / Pretendard 700
- **kpi-card label**: sm (12px), body 500 uppercase letter-spacing 0.06em 또는 한글 bold
- **kpi-card value**: 2xl (24px), mono 600 tabular-nums 영문 고정
- **data-table cell**: md (14px), body 400, line-height 1.5 reading-first dashboard
- **column-header**: sm (12px), body 600, letter-spacing 0.04em
- **draft-status-pill**: xs–sm (11–12px), body 600
- **filter-chip**: sm (12px), body 500
- **article-preview-pane heading**: xl–2xl (18–24px), EB Garamond 700 / 한글 Pretendard 700
- **article-preview-pane body**: md–lg (14–16px), line-height 1.6–1.7 (reading drawer 진입)
- **comment-thread body**: md (14px), body 400, line-height 1.55
- **editorial-calendar cell**: sm (12px), body 500, 날짜 는 mono tabular-nums
- **pagination / row id / timestamp**: xs (11px), mono tabular-nums
- **한글 line-height**: 1.5–1.6 (data-table · kpi-card · filter-chip · curation-queue · contributor-roster — dashboard dense), 1.6–1.7 (article-preview-pane drawer — editorial long-form reading), 1.4–1.5 (workspace-header · section-header), keep-all
- **tabular-nums**: kpi-card value · editorial-analytics-kpi · reading-analytics-kpi · editorial-calendar date · row id · issue-number · timestamp · pagination 전용
- **editorial letter-spacing** — 영문 section-header EB Garamond 은 기본, 한글 Pretendard heading 은 letter-spacing 0

## 접근성
- WCAG 2.2 AA (본문 대비 4.5:1, UI 3:1, Aubergine/Naples Yellow/Blush 위 텍스트는 near-black 또는 near-white 확보)
- sidebar-nav 는 role="navigation" + aria-label="워크스페이스 네비게이션"
- topbar 는 role="banner"
- workspace-header 는 role="heading" aria-level=1
- data-table 는 role="table" + column-header role="columnheader" aria-sort, row role="row"
- filter-sidebar 는 role="complementary" + aria-label="필터 사이드바"
- filter-chip 은 role="button" aria-pressed
- curation-queue 는 role="region" + aria-label="큐레이션 큐"
- editorial-calendar 는 role="grid" + aria-label="편집 캘린더", schedule-cell role="gridcell"
- publishing-pipeline 는 role="list" + aria-label="발행 파이프라인", pipeline-stage role="listitem"
- article-preview-pane 는 role="complementary" aria-label="기사 미리 보기 드로어" + focus trap 불필요 (비모달)
- modal-dialog 는 role="dialog" aria-modal focus trap + ESC 닫힘
- toast 는 role="status" 또는 aria-live="polite"
- kpi-card 숫자 는 aria-label 로 전체 문맥 전달 ("오늘 초안 12건, 전주 대비 +3")
- contributor-roster profile-card drawer 는 focusable, ESC 닫힘
- tag-taxonomy-manager tree 는 role="tree" + arrow-key 네비게이션
- comment-thread 는 role="log" + aria-live="polite"
- prefers-reduced-motion 존중 — slow fade drawer / row hover tint / schedule cell focus glow / curation queue drag 애니메이션 제거

## 한글 대응
- Pretendard variable (woff2) 번들, body/heading 공용, heading 은 Pretendard 700 letter-spacing 0
- 한글 data-table cell / kpi-card label / filter-chip / curation-queue row / contributor-roster cell line-height **1.5–1.6** (dashboard dense 유지), keep-all
- 한글 article-preview-pane drawer (reading drawer 진입 시) line-height **1.6–1.7** (editorial long-form reading), keep-all
- 한글 workspace-header / section-header line-height **1.4–1.5**, letter-spacing 0, keep-all
- word-break: **keep-all**, overflow-wrap: break-word
- 숫자/날짜/ID/issue-number/timestamp/pagination 은 mono 영문 고정 (한글 혼용 금지), tabular-nums
- 한국어 라벨: "큐레이션 / 편집 캘린더 / 발행 파이프라인 / 기고자 / 이슈 / 초안 / 스케줄 / 발행 / 보류 / 아카이브 / 태그 체계 / 편집 애널리틱스 / 리딩 애널리틱스" + 영문 "curation / editorial calendar / publishing pipeline / contributor / issue / draft / schedule / publish / hold / archive / tag taxonomy / editorial analytics / reading analytics" 병기 허용
- draft-status-pill 라벨 은 한글 단문 ("초안" / "리뷰" / "스케줄" / "발행" / "보류") + 영문 alias 병기 가능

## 주의사항
- 이 프리셋은 **dashboard--editorial-warm (P2)** — editorial 운영/큐레이션/퍼블리싱 dashboard 특화
- "일반 SaaS 관리자 대시보드 미니멀" 은 `dashboard--minimal-tech`
- "fintech 신뢰 대시보드" 는 `dashboard--corporate-trust`
- "차분한 에디토리얼 매거진 / 에세이 블로그" 는 `document-content--editorial-warm`
- "대담한 매거진 / opinion / manifesto" 는 `document-content--bold-confident`
- "개발자 API 레퍼런스 · 기술 문서" 는 `document-content--minimal-tech`
- "fashion editorial 커머스" 는 `commerce--editorial-warm`
- "streetwear 드롭 커머스 bold" 는 `commerce--bold-confident`
- "AI 글쓰기 코파일럿 차분 editorial" 은 `conversation-copilot--editorial-warm`
- "일반 AI 챗봇 미니멀" 은 `conversation-copilot--minimal-tech`
- "SRE/observability 모니터링" 은 `monitoring-ops--minimal-tech`
- "B2B SaaS 마케팅 랜딩 미니멀" 은 `marketing-landing--minimal-tech`
- "스포츠 랜딩 bold" 는 `marketing-landing--bold-confident`
- "소셜 피드 친근 파스텔" 은 `community-feed--playful-soft`
- "피그마 캔버스 에디터 미니멀 creative" 는 `canvas-tool--minimal-tech`
- 이미지 기반 힌트는 advisory, 구조적 결정은 spec + KB 우선
- 실제 CMS / 기고자 결제 / 구독 결제 게이트웨이 / 메일 발송 infrastructure 는 프리셋 범위 외 — editorial dashboard chrome 만 다룸
