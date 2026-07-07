# EKOS 정적 프로토타입

이 프로토타입은 한국 SAP 운영 사용자가 EKOS의 핵심 흐름을 빠르게 이해할 수 있도록 만든 정적 UI입니다.

EKOS는 업무 케이스를 검토해서 필요한 데이터가 충분한지 먼저 확인하고, 충분하면 지금 해도 되는 일과 하면 안 되는 일을 근거와 함께 보여주는 시스템입니다.

## 실행

```bash
cd projects/ekos-static-prototype
python3 -m http.server 4173 --bind 127.0.0.1
```

브라우저에서 엽니다.

```text
http://127.0.0.1:4173/
```

이 프로토타입은 JSON fixture를 `fetch`로 읽기 때문에 로컬 HTTP 서버가 필요합니다.

## 화면 흐름

- 업무 선택
- 케이스 입력
- 필요 데이터 확인
- 부족한 데이터 보강
- 필요 데이터 확인 완료
- 판단 결과
- 근거 및 정책 확인
- 검토 요청

## 주요 UX 원칙

- 영어와 내부 용어보다 한국어 업무 표현을 먼저 보여줍니다.
- 사용자가 무엇을 선택하고 입력해야 하는지 먼저 보여줍니다.
- 필수 데이터가 부족하면 판단 결과를 만들지 않습니다.
- 판단 결과는 “현재 해도 되는 일”과 “현재 막힌 일”로 표시합니다.
- `검토 필요`는 `승인`처럼 보이지 않게 구분합니다.
- 근거, 정책, provenance 같은 상세 정보는 감사/검토 화면으로 분리합니다.

## 정적 데이터

현재 화면 렌더링은 아래 두 fixture를 사용합니다.

- `workflows.json`
- `workflow-flows.json`

아래 파일은 초기 Delivery 단일 시나리오 fixture로 남아 있습니다.

- `source-package-failed.json`
- `source-package-passed.json`
- `decision-report-delivery-delay.json`
- `evidence-trace-delivery-delay.json`
- `review-request.json`

## 경계

- 정적 프로토타입입니다.
- EKOS 백엔드와 연결하지 않습니다.
- Live SAP 연동이 아닙니다.
- 운영 승인 또는 생산 승인 도구가 아닙니다.
- SAP 변경 작업을 실행하지 않습니다.
- provider 호출이 없습니다.
- 사람 검증을 주장하지 않습니다.
- RAG를 핵심 판단 권한으로 사용하지 않습니다.
- 기본 화면에서 raw JSON을 보여주지 않습니다.

## 검증

저장소 루트에서 실행합니다.

```bash
uv run design-ontology lint-implementation --target-repo projects/ekos-static-prototype
uv build
uv run --with pytest pytest tests/ -q
git diff --check
```
