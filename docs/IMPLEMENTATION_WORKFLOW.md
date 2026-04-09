# Implementation Workflow

## 목적

이 프레임워크는 레퍼런스를 매번 직접 읽게 하는 도구가 아니라, 공용 KB를 만들어 두고 실제 제품 프로젝트에서는 그 KB를 이용해 자기만의 디자인 시스템 산출물을 생성하는 워크플로를 제공합니다.

## Recommended Setup

### A. 프레임워크 저장소

이 저장소에서는:

- KB 구축
- 입력 스키마 관리
- 공용 생성 로직 관리
- 프로젝트 스캐폴드 제공

### B. 실제 제품 저장소

실제 앱/서비스 저장소에서는:

- `brand_profile.json` 혹은 이와 동등한 제품 정체성 입력값 유지
- 생성된 `system_spec.md`, `token_schema.json`, `component_inventory.json` 소비
- 실제 토큰, 컴포넌트, 문서, 테스트 구현

## Workflow

### 1. 공용 KB 구축

```bash
uv run design-ontology build-kb \
  --kb-dir kb/default \
  --seed-url https://spacebar310.tistory.com/86
```

이 단계는 가끔만 수행합니다.

### 2. 프로젝트 스캐폴드

```bash
uv run design-ontology init \
  --project-dir projects/my-app \
  --brand-name "My App" \
  --product-summary "What this product is for" \
  --kb-dir ../../kb/default
```

### 3. 프로젝트 브랜드 프로필 작성

수정 파일:

- `projects/my-app/brand_profile.json`

여기에는:

- 브랜드 키워드
- 피하고 싶은 키워드
- 플랫폼
- 접근성 기준
- 핵심 product primitive

를 작성합니다.

### 4. 프로젝트 산출물 생성

```bash
uv run design-ontology run-project --project-dir projects/my-app
```

생성 파일:

- `build/system/blueprint/system_spec.md`
- `build/system/blueprint/token_schema.json`
- `build/system/blueprint/component_inventory.json`
- `build/system/blueprint/system_ontology.json`

## How To Use In A Real Implementation Repo

### Option 1. Separate harness repo + product repo

가장 추천하는 방식입니다.

1. 이 저장소에서 KB와 시스템 산출물 생성
2. 생성된 결과를 실제 제품 저장소로 복사하거나 서브모듈/서브트리/CI artifact로 전달
3. 제품 저장소에서 토큰과 컴포넌트 구현

이때 연결 포인트는 보통 아래와 같습니다.

- `token_schema.json` -> CSS variables / Tailwind theme / design token pipeline
- `component_inventory.json` -> 구현 우선순위와 컴포넌트 backlog
- `system_spec.md` -> 디자이너/개발자 공통 기준 문서
- `system_ontology.json` -> agent prompt context 또는 graph DB 입력

원하면 implementation repo에 바로 Codex / Claude Code integration pack도 생성할 수 있습니다.

```bash
uv run design-ontology init-agent-pack \
  --target-repo /path/to/implementation-repo \
  --artifact-dir design-system \
  --targets codex,claude
```

자세한 파일 구조는 `docs/AGENT_INTEGRATIONS.md`를 참고하세요.

### Option 2. 제품 저장소 내부 tools 폴더에 포함

제품 저장소 내부에 `tools/design-ontology-harness` 형태로 포함시키고:

1. KB는 별도 버전 디렉터리로 유지
2. 앱 팀은 `run-project`만 실행
3. 결과를 `design-system/` 또는 `docs/design-system/` 아래에 반영

## Suggested Agent Usage

실제 구현용 에이전트는 아래 순서로 입력을 받는 것이 좋습니다.

1. `brand_profile.json`
2. `build/system/blueprint/system_spec.md`
3. `build/system/blueprint/token_schema.json`
4. `build/system/blueprint/component_inventory.json`
5. 구현 대상 코드베이스

그 다음 에이전트에게 아래처럼 지시합니다.

- `token_schema.json`에 맞춰 CSS 변수와 theme object 생성
- `component_inventory.json`의 high priority family부터 구현
- `system_spec.md`의 anti-keyword를 위반하지 않게 UI 의사결정
- 새 컴포넌트 추가보다 기존 primitive 확장을 우선

## Practical Rollout Order

실제 제품에 붙일 때 추천 순서:

1. color / typography / spacing 토큰
2. button / input / navigation
3. feedback / overlay
4. 제품 특화 primitive
5. 문서화와 테스트

## Versioning Advice

- KB는 날짜 또는 semantic version으로 버전 관리
- 프로젝트는 어떤 KB 버전을 사용했는지 `project_summary.json`에 기록
- 브랜드 프로필이 바뀌면 KB를 다시 만들 필요 없이 `run-project`만 다시 수행
- 레퍼런스 소스가 크게 바뀌었을 때만 `build-kb`를 다시 수행
