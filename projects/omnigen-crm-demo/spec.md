# Omnigen CRM — Product Spec

## 제품 개요

Omnigen CRM은 영업팀과 CS 리드가 고객 연락처, 파이프라인, KPI, 설정을 한 화면에서 빠르게 점검하는 운영형 CRM 분석 콘솔이다. 화면은 넓은 데스크톱을 기본으로 삼고, 고밀도 테이블과 카드형 지표를 함께 보여준다.

## 핵심 화면

1. **Workspace Overview** — KPI 카드 그리드, 파이프라인 요약, 최근 활동 피드
2. **Contacts** — 저장된 보기, 필터 툴바, 고정 헤더가 있는 연락처 테이블
3. **Pipeline** — 단계별 거래 현황, 확률, 담당자, 다음 액션
4. **Account Detail** — 연락처 정보, 활동 타임라인, 리스크 배지, 메모 패널
5. **Settings** — 팀원, 권한, 데이터 연동, 알림 정책을 다루는 탭 화면

## 주요 컴포넌트

- sidebar navigation
- workspace header
- saved view tabs
- filter toolbar
- kpi card
- contacts table
- status badge
- pipeline stage board
- activity feed
- detail side panel
- settings tabs
- command search

## 인터랙션 원칙

- 필터와 검색은 keyboard-first로 작동한다.
- 테이블은 dense density를 기본으로 하고, hover/focus/selected 상태를 분명히 둔다.
- 상태 배지는 색상만으로 의미를 전달하지 않고 텍스트 라벨을 함께 쓴다.
- 알림과 모션은 업무 흐름을 방해하지 않는 수준으로 제한한다.

## 시각 방향

- 카드와 패널은 flat surface와 thin divider를 기본으로 한다.
- 숫자는 빠르게 훑을 수 있도록 table label보다 한 단계 크게 둔다.
- CTA는 한 화면에 하나만 강하게 보이게 한다.
- 색상은 cool gray surface와 restrained blue accent를 중심으로 잡는다.

## 접근성

- WCAG 2.2 AA를 목표로 한다.
- 모든 interactive element에는 키보드 focus 상태가 필요하다.
- 테이블 헤더, 상태 배지, 필터 칩은 스크린리더에서 의미가 드러나야 한다.
