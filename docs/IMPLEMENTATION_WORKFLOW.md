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
- 선택적으로 curated color reference 경로와 palette role

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

## Optional Curated Color Input

색상 방향이 이미 별도 문서로 정리되어 있다면 `brand_profile.json`의 `color_reference`로 연결할 수 있습니다.

예:

```json
{
  "color_reference": {
    "path": "/absolute/path/to/color-reference.md",
    "preferred_families": ["Deep Reds", "Standard Oranges"],
    "selected_colors": ["Claret", "Tangerine", "Creamsicle"],
    "palette_roles": {
      "primary": "Claret",
      "accent": "Tangerine",
      "surface_tint": "Creamsicle"
    }
  }
}
```

이 값이 있으면 하네스는:

- markdown 색상 문서를 파싱하고
- 선택한 색상 이름을 실제 HEX/mood/pairing과 연결하고
- `system_spec.md`와 `token_schema.json`에 색상 기준으로 기록합니다.

## Safe Refactor Policy

이 프레임워크의 산출물은 "전체 UI를 한 번에 갈아엎으라"는 신호가 아닙니다.

기본 원칙:

- 기존 핵심 기능, 진입점, 작업 흐름은 명시적 요청 없이 제거하거나 숨기지 않기
- 전체 셸 리디자인보다 `token -> primitive -> feature surface` 순서의 점진적 적용 우선
- 지원 대상 theme와 breakpoint에서 동시에 성립하는 semantic token부터 먼저 적용
- 시각 개선보다 기능 회귀 방지가 우선
- 패널 위치 변경, 내비게이션 구조 변경, 기본 상호작용 변경은 별도 migration decision으로 다루기

## Safe Refactor Checklist

실제 구현 저장소에서 리팩터 전후로 최소한 아래를 확인하는 것을 권장합니다.

1. 기존에 보이던 핵심 패널, 버튼, 입력창이 그대로 노출되는가
2. light/dark 또는 지원하는 theme 조합에서 텍스트와 surface 대비가 유지되는가
3. desktop/tablet/mobile 또는 지원 breakpoint에서 주요 패널이 화면 밖으로 밀리지 않는가
4. 기존 데이터 밀도와 핵심 업무 흐름이 악화되지 않았는가
5. build/lint/test가 통과하는가

## What To Avoid

- 디자인 시스템을 핑계로 한 전면 셸 재작성
- semantic token 없이 하드코딩 색상으로 화면 전체를 덮는 방식
- 기존 기능을 없애거나 숨긴 뒤 "더 깔끔해졌다"고 판단하는 방식
- 한 번의 리팩터에서 정보 구조와 시각 구조를 동시에 크게 바꾸는 방식

## Versioning Advice

- KB는 날짜 또는 semantic version으로 버전 관리
- 프로젝트는 어떤 KB 버전을 사용했는지 `project_summary.json`에 기록
- 브랜드 프로필이 바뀌면 KB를 다시 만들 필요 없이 `run-project`만 다시 수행
- 레퍼런스 소스가 크게 바뀌었을 때만 `build-kb`를 다시 수행
