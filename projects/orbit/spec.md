# Orbit — SaaS 운영 대시보드 Spec

## 제품 개요
Orbit은 SaaS 팀이 프로젝트, 이슈, KPI, 문서, 멤버를 하나의 고밀도 관리자 콘솔에서
운영하기 위한 **미니멀 테크 대시보드**다. Linear/Height/Notion 계열의 키보드 중심 워크플로우를
지향하고, 한국어 UI를 1급으로 지원한다.

## 사용자
- SaaS 프로덕트 매니저: 스프린트 플래닝, KPI 리뷰
- 엔지니어링 리드: 이슈 트리아지, 릴리스 관리
- 운영/CS 리드: 인시던트·고객 계정 추적

## 핵심 화면
1. **Workspace Home** — KPI 카드 그리드 + 최근 활동 피드 + 팀별 요약
2. **Projects** — 프로젝트 목록(테이블) + 필터 chrome + 상태/우선순위 배지
3. **Issue Table** — 정렬/필터/그룹화 가능한 dense data table, inline 상태 메뉴
4. **Issue Detail** — 좌측 2단 메타 + 중앙 rich text + 우측 activity thread
5. **Command Palette** — 글로벌 액션/검색/네비게이션 (⌘K)
6. **Settings** — 멤버/권한/통합/billing 2-level 네비게이션

## UI 컴포넌트 (도출)
- sidebar navigation (2-level, collapsible)
- workspace switcher
- data table (sticky header, dense density, sortable columns, inline menu)
- kpi card (numeric emphasis, trend indicator)
- status badge (semantic color tokens)
- filter chrome (chips + popover filters)
- command palette (⌘K modal, fuzzy search, recent)
- activity feed (time-grouped, avatar + action + diff)
- breadcrumbs
- tabs (workspace section-level)
- dialog (destructive action confirm)
- toast (low-noise, auto-dismiss)
- dropdown menu (keyboard-first)
- empty state
- pagination
- avatar + member roster

## 인터랙션 원칙
- 키보드 우선: ⌘K, ⌘/, j/k 네비게이션
- 모션 최소화: 200ms 이내, ease-standard
- 상태는 항상 예측 가능: hover/focus/active/selected/disabled 5상태 명시
- dense density 기본, comfortable 토글 옵션

## 색상 전략
- surface/text는 무채색 (cool gray 계열)
- primary accent는 blue 1종 제한
- semantic: success / warning / danger / info 4 role
- **라이트 + 다크 모두 1급**, 다크는 순수 #000 대신 deep cool gray

## 타이포그래피
- heading / body: **Inter** (영문) / **Pretendard** (한글)
- mono: **JetBrains Mono** (data, shortcut)
- scale: xs/sm/md/lg/xl/2xl/3xl/4xl — 13–32px 중심
- line-height: tight(1.25) / normal(1.5) / relaxed(1.625)

## 접근성
- WCAG 2.2 AA (본문 대비 4.5:1, UI 3:1)
- 모든 interactive에 focus ring
- aria-live로 토스트/업데이트 알림
- 키보드 trap 금지

## 한글 대응
- Pretendard variable (woff2) 번들
- 한글/영문 혼용 시 font-feature "palt" off, "ss01" 미사용
- 자간: 한글 -1%, 영문 0

## 주의사항
- 이 프리셋은 dashboard--minimal-tech (P0) 용
- 마케팅/커머스/문서 중심 제품에는 부적합
- 이미지 기반 힌트는 advisory, 구조적 결정은 spec + KB 우선
