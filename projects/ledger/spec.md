# Ledger — Fintech 운영 대시보드 Spec

## 제품 개요
Ledger는 기업 재무/핀테크 운영팀을 위한 **corporate-trust 톤 대시보드**다.
Stripe/Brex/Mercury/Ramp 계열의 B2B 금융 관리 콘솔을 지향하며, 거래·잔고·
컴플라이언스를 고밀도로 관리하는 keyboard-friendly 환경을 제공한다. 한국어
UI를 1급으로 지원한다.

## 사용자
- 기업 재무/회계 담당자: 입출금/대사/정산 관리
- 핀테크 운영·컴플라이언스 팀: 거래 이상 감지, KYC/AML 대응
- B2B SaaS 프로덕트 매니저: 파트너/계정 운영 리포팅

## 핵심 화면
1. **Workspace Home** — 잔고 KPI 카드 + alert list + 최근 거래 피드
2. **Transactions** — 거래 테이블(정렬/필터/그룹), 상태 배지, 검색, 엑스포트
3. **Transaction Detail** — 좌측 메타/계좌 + 중앙 상세 + 우측 감사 타임라인
4. **Compliance** — alert/flag 목록, KYC/AML 상태, 증빙 첨부 뷰
5. **Reports** — 기간 선택 + chart grid + 내역표 + 다운로드
6. **Settings** — 멤버/권한/통합/보안(MFA) 2-level 네비게이션

## UI 컴포넌트 (도출)
- sidebar navigation (2-level, collapsible)
- workspace switcher
- transactions data table (sticky header, dense, sortable, inline actions)
- balance kpi card (numeric emphasis, compare vs. prev period)
- compliance banner (critical alert)
- alert list (severity badge, audit link)
- audit timeline (immutable, with actor/ts)
- filter chrome (chips + popover + date range picker)
- status badge (semantic color tokens)
- breadcrumbs
- tabs (account/period level)
- dialog (destructive/정산 확인)
- toast (low-noise)
- dropdown menu
- empty state
- pagination
- avatar + member roster
- export button (CSV/PDF)

## 인터랙션 원칙
- 키보드 우선: ⌘K, ⌘F, j/k 네비게이션
- 모션 최소화: 150–200ms, ease-standard
- 상태 명시: hover/focus/active/selected/disabled 5상태
- dense density 기본, comfortable 토글
- 파괴적/금융 액션은 2단계 confirm + audit 기록

## 색상 전략
- surface/text는 cool neutral + 미묘한 blue tint
- primary accent는 Prussian Blue (#003153) 1종 제한
- secondary accent: Bronze Gold (클래식/프리미엄)
- semantic: success / warning / danger / info 4 role, 과포화 금지
- **라이트 + 다크 모두 1급**, 다크는 deep navy surface (#0A1628 계열)

## 타이포그래피
- heading / body: **Inter** (영문) / **Pretendard** (한글)
- mono: **JetBrains Mono** (거래 ID, 계좌번호, 감사 로그)
- scale: xs/sm/md/lg/xl/2xl/3xl — 13–28px 중심 (숫자 가독성)
- line-height: tight(1.25) / normal(1.5) / relaxed(1.6)
- tabular-nums 활성화 (금액 정렬)

## 접근성
- WCAG 2.2 AA (본문 대비 4.5:1, UI 3:1)
- 모든 interactive에 focus ring
- aria-live로 alert/상태 변경 알림
- 키보드 trap 금지
- 금액·상태는 색상 + 텍스트 라벨 이중 표기

## 한글 대응
- Pretendard variable (woff2) 번들
- 금액 표기: 천 단위 구분자 + 통화 기호 위치 locale 준수
- 자간: 한글 -1%, 영문 0

## 주의사항
- 이 프리셋은 dashboard--corporate-trust (P1, fintech) 용
- 마케팅/커머스/문서 중심 제품에는 부적합
- 이미지 기반 힌트는 advisory, 구조적 결정은 spec + KB 우선
- 실제 금융 로직/규제(PCI/ISO 27001 등)는 프리셋 범위 외 — 시각 시스템만 다룸
