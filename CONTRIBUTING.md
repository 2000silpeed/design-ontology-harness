# Contributing

## Goal

이 저장소의 목표는 특정 앱 결과물을 대신 만들어주는 것이 아니라, 누구나 자신의 디자인 시스템 하네스를 정의하고 실행할 수 있는 재사용 가능한 프레임워크를 제공하는 것입니다.

## Contribution Priorities

1. 새로운 입력 스키마와 검증 개선
2. 더 나은 수집기와 source adapter
3. 온톨로지 추출 규칙 개선
4. 토큰/컴포넌트 산출물 품질 개선
5. 예제 프로젝트와 문서화

## Development

```bash
uv sync
uv run design-ontology --help
```

## Design Principles For This Repo

- 프로젝트 특화 로직보다 설정 기반 확장을 우선합니다.
- 예제는 포함하되 프레임워크 코어와 분리합니다.
- 출력물은 사람이 읽는 문서와 기계가 읽는 구조를 함께 제공합니다.
- 실패한 수집도 숨기지 않고 기록합니다.
