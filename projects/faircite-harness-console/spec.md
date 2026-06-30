# FairCite Dual Mode Console 상세 설계서

## 핵심 메시지

FairCite는 공정거래위원회 의결서 500건을 chunk 단위까지 추적 가능한 형태로 재구성한 근거추적 서비스다. 본사·원청은 사전 예방용으로, 가맹점주·수급사업자는 사후 인지·대응용으로 같은 데이터를 다른 시점에서 활용한다.

## 첫 화면: 듀얼 모드 콘솔

- 첫 화면은 마케팅 랜딩이 아니라 실제 서비스 콘솔이어야 한다.
- 상단에는 제품명, `/predict` 자동지표 보호 상태, baseline `main_score 0.7295`, 서비스 버전 `v0.2`를 표시한다.
- 좌측에는 주요 모듈 내비게이션을 둔다: 진단 콘솔, 산정 구조, 패턴 카탈로그, 쌍대 케이스, 근거 맵.
- 중앙 첫 viewport에는 컴플라이언스 모드, 권익보호 모드, 쌍대 케이스 모드 선택 버튼을 둔다.
- 우측에는 Evidence Map drawer를 고정해 현재 답변의 chunk, 법제처 조문, 모델 요약 근거를 보여준다.

## 공통 거버넌스

- 모든 출력 필드는 `[원문 추출]`, `[모델 요약]`, `[사람 분류]`, `[통계 집계]` 중 하나의 source label badge를 가져야 한다.
- 카드 우측 상단 또는 표 caption 옆에 source label을 둔다.
- chunk_id, doc_id, score, 조회 시점은 mono typography로 표시한다.
- 권익보호 모드에서는 금지 표현을 쓰지 않는다: "위반입니다", "위반 가능성 [높음]", "고발 가능", "예상 과징금", "신고서 초안".
- 의무 문구: "유사사례 비교", "참고 판단·자문 아님", "확인 필요사항", "근거 chunk_id".
- 민감정보 banner와 "내 입력 지우기" 버튼은 항상 노출한다.

## 컴플라이언스 모드: 자사 리스크 진단

- 입력 필드: 산업·업종, 거래구조, 자사 위치, 주요 행위 textarea.
- 주요 행위 textarea에는 하도급·기술자료 제공 사례 샘플을 보여준다.
- 결과는 리스크 매트릭스로 표시한다: 위반유형, 유사 의결서 건수, severity meter.
- 유사 의결서 카드에는 사건명, chunk_id, section, source label, retrieval score를 표시한다.
- 관련 현행 조문은 법제처 조회 시점과 함께 Evidence drawer에 표시한다.
- 결과 상단에는 "참고용 진단·법률 자문 아님" label을 둔다.

## 권익보호 모드: 상황 진단

- 입력 필드는 자연어 상황 textarea 중심이다.
- 설명 톤은 평이하고 단계적이어야 한다.
- 출력 제목은 "공정위가 인정한 유사 패턴"이어야 한다.
- 결과 등급은 "매우 유사", "유사", "약하게 유사", "판단 어려움"만 사용한다.
- 다음 단계 가이드는 사실관계 정리, 증거 확인, 신고 채널 확인으로 나뉜다.
- 모든 결과 카드에는 "유사사례 비교"와 "참고 판단·자문 아님"이 보이게 한다.

## 과징금 산정 구조 분석기

- 이 모듈은 과징금을 예측하지 않는다.
- 제목은 "과징금 산정 구조 분석기"로 고정한다.
- 상단 notice box에 "예측 아님. 산정 구조와 유사 의결서 비교 자료"를 표시한다.
- 단계형 UI를 사용한다: 부과기준율, 관련매출액, 가중·감경, 의결서 사례 범위.
- 최종 금액 단정 대신 "의결서 사례 범위"와 "분포"를 표시한다.

## 갑질 패턴 카탈로그

- 카드 갤러리로 표현한다.
- 카드 예시: 기술자료 부당 요구, 단가 후려치기, 필수품목 강매, 입찰 들러리.
- 각 카드에는 평이한 설명, 공정위 인정 사례 수, source label, 관련 조문 hover affordance를 둔다.

## 쌍대 케이스 데모

- 한 사건을 컴플라이언스 관점과 권익보호 관점에서 동시에 보여준다.
- 대표 케이스는 현대중공업 기술자료 유용 사건이다.
- 컴플라이언스 side는 예방 체크리스트로 변환한다.
- 권익보호 side는 사실관계 정리 항목으로 변환한다.
- 같은 chunk_id가 두 관점에 모두 연결되는 것을 시각적으로 강조한다.

## Evidence Map

- 우측 drawer 또는 별도 패널에 retrieved chunks 5개를 카드로 표시한다.
- 각 카드에는 doc_title, section, snippet, chunk_id, score, source label을 포함한다.
- 법제처 조문 card는 조회 시점과 live/cache/snapshot 상태를 표시한다.
- Evidence Map 그래프는 answer, chunk, law, statistic node를 연결하는 간단한 관계도로 표현한다.

## 데이터 상태와 지표

- 의결서 500건, chunks 31,879개, graph schema `faircite.track2.graph_retrieval.v1`, baseline `0.7295`를 상태 카드로 표시한다.
- 자동 4지표 보호 메시지는 서비스 UI와 분리된 status pill로 보여준다.

## 반응형 요구

- desktop: 좌측 navigation, 중앙 workbench, 우측 evidence drawer의 3열 콘솔.
- tablet: evidence drawer는 아래로 내려가되 출처 라벨 legend를 유지한다.
- mobile 390px: 가로 스크롤 없이 mode card, form, result, evidence drawer가 순서대로 쌓인다.
- 버튼과 카드 텍스트는 줄바꿈 fallback을 가져야 한다.

## 컴포넌트 후보

- app shell
- mode selector
- sidebar navigation
- privacy banner
- diagnosis form
- textarea
- select
- primary button
- secondary button
- icon button
- status pill
- source label badge
- risk matrix
- risk meter row
- case result card
- evidence drawer
- source card
- law lookup card
- sanction anatomy stepper
- pattern card grid
- paired case comparison panel
- data status card
- proof strip for five evaluation axes
