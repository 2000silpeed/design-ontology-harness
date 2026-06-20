# Omnigen CRM 목업 사용설명서

이 목업은 디자인 시스템 산출물이 실제 화면에서 어떻게 보이는지 확인하기 위한 프론트엔드 프로토타입입니다. 백엔드는 연결하지 않았지만, 주요 버튼과 필터는 브라우저 안에서 바로 반응합니다.

## 열기

```bash
python3 -m http.server 8765 --bind 127.0.0.1
```

브라우저에서 아래 주소를 엽니다.

```text
http://127.0.0.1:8765/projects/omnigen-crm-demo/mockup/index.html
```

파일을 직접 열어도 기본 화면은 보이지만, 브라우저 정책에 따라 일부 다운로드 동작은 HTTP 서버에서 더 안정적입니다.

## 눌러볼 수 있는 기능

| 영역 | 조작 | 동작 |
|---|---|---|
| 상단 액션 | `New contact` | 새 연락처를 테이블 맨 위에 추가하고 Contacts 카운트를 올립니다. |
| 상단 액션 | `Export` | 현재 화면에 보이는 연락처 행만 CSV로 저장합니다. |
| 상단 검색 | 검색어 입력 | 연락처, 회사, 담당자, 상태 텍스트를 기준으로 행을 거릅니다. |
| 테이블 툴바 | `Status`, `Owner`, `Stage` | 선택한 조건에 맞는 행만 보여줍니다. |
| 저장된 보기 | `Priority contacts`, `Renewals`, `At risk`, `New this week` | 보기 기준에 맞춰 테이블을 전환합니다. |
| 테이블 툴바 | `Save view` | 현재 필터 상태를 토스트 메시지로 확인합니다. |
| Pipeline stages | 기간 버튼 | `This month`, `Last 30 days`, `This quarter` 순서로 바뀝니다. |
| Data quality queue | `Open` | 숨겨진 다음 정리 시간을 보여주고, 다시 누르면 닫습니다. |
| Activity feed | `View all` | 활동 2개를 더 보여주고, 다시 누르면 접습니다. |
| Settings snapshot | 스위치 | 클릭하거나 Enter/Space 키로 켜고 끕니다. |
| 왼쪽 내비게이션 | 메뉴 클릭 | active 상태와 상단 제목이 바뀝니다. |

## 확인 포인트

- `dense dashboard grid`: KPI 카드, 테이블, 우측 보조 패널이 한 화면에 함께 들어옵니다.
- `flat card surfaces`: 카드와 패널은 약한 그림자와 얇은 border로 구분합니다.
- `split-pane workspace`: 왼쪽 사이드바, 중앙 업무 영역, 우측 보조 패널로 작업 흐름을 나눕니다.
- `restrained blue accent`: 강한 파란색은 현재 위치, 주요 버튼, 진행률에만 씁니다.
- `utilitarian typography`: 숫자와 테이블 라벨을 빠르게 훑을 수 있게 간격과 크기를 줄였습니다.

## 한계

이 목업은 로컬 상태만 사용합니다. 새로고침하면 추가한 연락처, 필터, 토글 상태가 초기화됩니다. 실제 제품에 넣으려면 CSV export, 저장된 보기, 설정 토글을 API와 연결해야 합니다.
