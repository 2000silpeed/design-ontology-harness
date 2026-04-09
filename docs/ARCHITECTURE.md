# Architecture

## Core Idea

이 저장소는 `reference ingestion -> reusable knowledge base -> project-specific synthesis -> implementation outputs` 흐름을 갖는 디자인 시스템 하네스 프레임워크입니다.

## Layers

1. Seed extraction
   - 큐레이션 문서에서 외부 레퍼런스 링크를 추출합니다.

2. Crawl layer
   - 각 외부 레퍼런스를 제한적으로 수집하고 정제합니다.

3. Ontology layer
   - 개념어, 근거 문장, 관계를 JSONL로 추출합니다.

4. Knowledge base layer
   - 수집 결과를 재사용 가능한 KB로 저장합니다.
   - 프로젝트 실행 시에는 이 KB를 재사용하고 외부 링크를 다시 읽지 않아도 됩니다.

5. Synthesis layer
   - 브랜드 프로필과 레퍼런스 근거를 바탕으로 자체 시스템 블루프린트를 만듭니다.

6. Authoring layer
   - 시스템 스펙, 토큰 스키마, 컴포넌트 인벤토리, 온톨로지 그래프를 생성합니다.

7. Project scaffold layer
   - 사용자가 자신의 프로젝트 폴더를 만들고, 같은 워크플로를 반복적으로 사용할 수 있게 합니다.

## Public Repo Shape

- `design_ontology_harness/`
  코어 로직
- `schemas/`
  입력 스키마
- `config/`
  예시 프로필
- `docs/`
  아키텍처와 사용법
- `kb/<name>/`
  재사용 가능한 지식베이스
- `projects/<your-project>/`
  사용자가 생성한 개별 하네스 프로젝트

## Extension Points

- 새로운 source adapter 추가
- ontology concept set 교체 또는 확장
- synthesis 전략 교체
- output pack 종류 추가
- agent prompt template 추가
