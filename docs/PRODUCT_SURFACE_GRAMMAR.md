# Product Surface Grammar

이 문서는 AI 구현물이 균일한 카드형 화면으로 수렴하지 않도록, 하네스가 기본으로 선택해야 하는 제품 표면 문법을 정의한다.

## 문제

카드는 만들기 쉽고 실패 가능성이 낮아서 AI가 자주 선택한다. 하지만 실제 운영형 제품에서는 첫 화면의 중심이 대개 카드 묶음이 아니다. 사용자는 표, 행 목록, 레일, 캔버스, 지도, 타임라인, 인스펙터, 시트, 툴바를 통해 상태를 훑고 조작한다.

하네스의 목표는 카드를 금지하는 것이 아니다. 카드를 반복 객체나 짧은 요약에 제한하고, 주 작업 표면은 도메인 구조로 먼저 만들게 하는 것이다.

## 기본 선택 순서

1. 작업이 스캔/비교/처리라면 `operational overview`, `data tables`, `row list`, `status rail`, `source-ledger`를 먼저 선택한다.
2. 작업이 편집/제작이라면 `canvas`, `editor-canvas`, `inspector-panel`, `toolbar`, `layer panel`을 먼저 선택한다.
3. 작업이 검토/감사라면 `policy-matrix`, `audit-timeline`, `approval-rail`, `diff-viewer`, `decision record`를 먼저 선택한다.
4. 작업이 탐색/구매/콘텐츠 브라우징이라면 카드가 가능하지만, 이미지/썸네일/상태/행동이 실제 콘텐츠와 연결되어야 한다.
5. `dashboard cards`는 사용자가 카드형 요약을 명시했거나, 독립된 단일 주제 요약이 필요한 경우에만 사용한다.

## 구현 규칙

- `dashboard`, `KPI`, `metric`, `status`, `overview` 같은 일반 대시보드 어휘는 `dashboard cards`가 아니라 `operational overview`로 해석한다.
- `stat card`, `summary card`, `metric card`, `카드형`, `통계 카드`처럼 카드 의도가 명시된 경우에만 카드 primitive를 활성화한다.
- 행/표/레일/ledger/타임라인/매트릭스/diff 계열은 `radius:none`, 촘촘한 spacing, divider, sticky toolbar, source/update label을 우선한다.
- 카드/패널/시트/배너 계열만 tint background, radius, framed surface token을 받는다.
- 운영형 표면 신호가 강하고 카드가 명시되지 않았다면 고급 컴포넌트 추천에서도 `*-card` 이름의 후보를 올리지 않는다.
- 워크플로/관계/근거 그래프는 장식용 곡선이 아니다. 노드와 엣지는 하나의 좌표계 안에서 `data-node-id`, `data-edge-id`, `data-from`, `data-to`, 방향, 조건 라벨, 상태를 가져야 한다. 이 기준을 못 채우면 그래프 대신 table, timeline, ledger를 쓴다.
- HTML 목업은 정적 스크린샷이 아니라 얇은 제품 프로토타입이다. `chart`, `graph`, `map`, `calendar`, `kanban`, `gantt`, `spreadsheet`, `timeline`, `canvas` 계열 표면은 `data-runtime-surface` 또는 `data-product-surface`와 함께 `data-model`, `data-source`, 항목/노드/이벤트 ID, 상태 정보를 드러낸다.
- `data-product-prototype` 또는 prototype/mockup 클래스로 표시한 HTML 목업은 `data-prototype-state-set`이나 `data-state` 시나리오로 기본, 선택, 로딩, 빈 상태, 오류, 비활성, 승인/차단 같은 상태 세트를 보여준다.
- 계약 메타데이터만 있고 브라우저 기본 HTML처럼 보이면 제품 프로토타입이 아니다. token-bound layout, surface, typography, state, affordance styling을 갖추거나 non-visual fixture로 명시한다.
- 구현 후 `DS070`이 발생하면 카드 수를 줄이는 데서 멈추지 말고, 주 작업 표면을 표/행/레일/캔버스/인스펙터 중 하나로 승격한다.
- 구현 후 `DS082` 또는 `DS083`이 발생하면 선을 다듬지 말고, 관계 모델을 먼저 정의한다. 좌표계가 분리된 HTML 노드 + SVG 곡선 조합은 금지한다.
- 구현 후 `DS084` 또는 `DS085`가 발생하면 표면을 꾸미지 말고, 런타임 의도·데이터 모델·출처·상태 세트를 먼저 채운다.
- 구현 후 `DS086`이 발생하면 데이터 속성을 더 붙이지 말고, 제품 표면 스타일과 시각 affordance를 구현한 뒤 다시 검수한다.

## 개선 Loop

1. 관찰: 리뷰어 지적, 현재 스크린샷/DOM, 대상 파일을 고정한다.
2. 분류: 구현 결함인지, 계약 누락인지, 시각 표면 누락인지, 관계 모델 오류인지, 반복 가능한 온톨로지 gap인지 나눈다.
3. 승격: 반복 가능한 실패면 governance, `IMPLEMENTATION_CONTRACT`, `lint-implementation`, 회귀 테스트로 올린다.
4. 수리: 색만 바꾸지 말고 주 작업 표면, 데이터 계약, 상태 세트, token-bound styling을 함께 고친다.
5. 검증: lint, targeted test, desktop/mobile visual QA를 돌리고 새 실패가 보이면 다시 분류한다.

## 좋은 대체 패턴

| 카드형 유혹 | 제품형 대체 |
| --- | --- |
| 4개 KPI 카드 | `metric-strip` + `source-ledger` |
| 기능 카드 그리드형 대시보드 | `task-surface-header` + `data-table` + `operational-rail` |
| 정책 체크 카드 묶음 | `policy-matrix` + `audit-timeline` |
| 검토 결과 카드 | `decision-record` + `approval-rail` |
| 활동 카드 목록 | `activity-feed` 또는 `event-timeline` |
| 필터 카드 | `filter-toolbar` 또는 `saved-view-bar` |

## 검증

새 UI 또는 프리셋은 아래 질문을 통과해야 한다.

- 첫 viewport에서 사용자가 실제로 조작하거나 판단할 표면이 보이는가?
- 카드가 독립된 단일 주제 요약이 아니라 섹션 전체를 감싸고 있지는 않은가?
- 같은 radius, shadow, padding, icon chip을 가진 모듈이 화면을 지배하지 않는가?
- 표/행/레일/인스펙터 같은 도메인 구조가 적어도 하나의 주 표면으로 승격되어 있는가?
- 그래프가 있다면 연결선이 노드 포트에 정확히 붙고, 방향·조건·상태·데이터 출처가 보이는가?
- 복합 HTML 표면이 있다면 그것이 실제 앱에서 무엇으로 구현될지, 어떤 데이터와 상태를 갖는지 마크업에서 확인할 수 있는가?
- 계약은 있는데 화면이 브라우저 기본 스타일처럼 보이지는 않는가?
- 수치, 상태, 예측, 순위에는 출처나 업데이트 시각, 샘플 라벨이 붙어 있는가?
