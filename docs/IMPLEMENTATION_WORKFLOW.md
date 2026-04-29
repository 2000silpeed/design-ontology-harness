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
- 선택적으로 `visual_reference.sources`에 로컬 스크린샷 / 레퍼런스 이미지

를 작성합니다.

### 4. 시각 레퍼런스 준비 (선택)

이 단계는 필수는 아니지만, 공식 KB만으로 잡기 어려운 density / surface language / CTA emphasis를 보강하고 싶을 때 권장합니다.

핵심 원칙:

- 공식 KB / spec / brand profile / color reference는 구조적 truth source
- visual reference는 조형 언어를 보강하는 advisory signal
- image-derived 결과에는 `observed` / `inferred` / `unverified` provenance 레벨을 함께 남김
- Pinterest는 필수 의존성이 아니라 검색 보조 채널
- 직접 크롤링보다 query 생성 -> 사용자의 로컬 저장 -> 로컬 이미지 분석 흐름을 우선
- raw asset 다운로드보다 screenshot/reference URL provenance 기록을 우선하고, 재배포 가능한 에셋으로 간주하지 않음

예:

```bash
# 설계서 + 브랜드 프로필 기반 query set 생성
uv run design-ontology generate-visual-queries \
  --project-dir projects/my-app \
  --spec projects/my-app/spec.md \
  --sync-brand-profile

# Pinterest-assisted shortlist를 실제 visual sources로 반영
uv run design-ontology select-pinterest-candidates \
  --project-dir projects/my-app \
  --candidate q03-c02 \
  --candidate q05-c02 \
  --sync-sources

# 로컬 이미지가 연결된 뒤 visual layer만 별도 분석
uv run design-ontology analyze-visuals \
  --project-dir projects/my-app
```

생성 파일:

- `build/visuals/visual_query_suggestions.json`
- `build/visuals/pinterest_assist_plan.json`
- `build/visuals/pinterest_candidate_manifest.json`
- `build/visuals/pinterest_selection_manifest.json`
- `build/visuals/visual_reference_report.json`
- `build/visuals/visual_motifs.json`
- `build/visuals/layout_cues.json`
- `build/visuals/component_style_hints.json`

세부 운영 규칙과 manifest 구조는 [docs/PINTEREST_ASSISTED_WORKFLOW.md](./PINTEREST_ASSISTED_WORKFLOW.md)를 참고합니다.

### 5. 프로젝트 산출물 생성

```bash
uv run design-ontology run-project --project-dir projects/my-app
```

생성 파일:

- `build/system/blueprint/system_spec.md`
- `build/system/blueprint/token_schema.json`
- `build/system/blueprint/component_inventory.json`
- `build/system/blueprint/system_ontology.json`

`visual_reference`가 연결돼 있으면 위 산출물 안에 visual direction, layout rhythm, image-derived component hints도 함께 반영됩니다.

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
2. 앱 팀은 기본적으로 `run-project`만 실행하고, 필요하면 `analyze-visuals`를 선행
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
- `system_spec.md`와 `component_specs.md`의 visual hints는 구조 변경이 아니라 표현 계층 결정에만 사용
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
    "preferred_families": ["Deep Reds", "Standard Oranges", "Pastel Oranges"],
    "palette_strategy": {
      "mode": "brand-guided",
      "candidate_count": 3,
      "temperature": "warm",
      "contrast": "balanced",
      "diversity": "balanced",
      "surface_style": "tinted",
      "prefer_moods": ["세련됨", "신뢰감"],
      "avoid_moods": ["달콤함", "귀여움"]
    },
    "palette_expansion": {
      "enabled": true,
      "supporting_color_count": 12,
      "combination_count": 4,
      "prefer_pairings": true,
      "prefer_related_families": true
    }
  }
}
```

이 값이 있으면 하네스는:

- markdown 색상 문서를 파싱하고
- 브랜드 키워드와 색상 문서의 mood/usage를 함께 보고 palette candidate를 만들고
- active palette를 semantic role 힌트와 함께 고정하고
- seed color pairings와 관련 family를 추가 검색해 support / neutral / state color를 확장하고
- `system_spec.md`와 `token_schema.json`에 색상 기준으로 기록합니다.

특정 팔레트를 직접 고정하고 싶으면 `selected_colors`와 `palette_roles`를 추가하면 됩니다. 그 경우 selection mode는 `manual`로 기록됩니다.
`preferred_families`는 hard filter가 아니라 우선순위 bias로 동작하므로, 자동 모드에서도 다른 family 후보가 대안으로 남을 수 있습니다.

## Adding More Reference Sites

기존 `seed-url` 하나만 쓰지 않아도 됩니다. 새 디자인 시스템 참고 사이트를 찾았다면 KB에 추가해서 다시 빌드하면 됩니다.

### 추천 입력 방식

- 공식 디자인 시스템 문서의 메인 페이지
- overview, foundations, components를 함께 링크하는 index 페이지
- 브랜드 쇼케이스 글보다 실제 시스템 문서 쪽을 우선
- seed는 블로그형 큐레이션 글일 수도 있고, 직접 디자인 시스템 URL일 수도 있음

### 방법 1. `--seed-url` 여러 개 사용

```bash
uv run design-ontology build-kb \
  --kb-dir kb/default \
  --seed-url https://spacebar310.tistory.com/86 \
  --seed-url https://example.com/design-system \
  --seed-url https://another-example.com/system
```

### 방법 2. seeds 파일 사용

```text
# seeds/design-systems.txt
https://spacebar310.tistory.com/86
https://example.com/design-system
https://another-example.com/system
```

```bash
uv run design-ontology build-kb \
  --kb-dir kb/default \
  --seeds-file seeds/design-systems.txt
```

### 중요한 구분

- 새 참고 사이트를 반영하려면 `build-kb`를 다시 실행해야 합니다.
- `projects/<name>/seeds/seed_urls.txt`는 provenance와 메모용입니다.
- visual reference 이미지를 바꾸면 `analyze-visuals`로 먼저 확인한 뒤 `run-project`를 다시 실행하면 됩니다.
- 프로젝트 결과물만 다시 만들고 싶을 때는 `run-project`만 실행하면 됩니다.

즉:

- reference source 변경 -> `build-kb`
- brand/profile 변경 -> `run-project`
- visual query / visual sources 변경 -> `analyze-visuals` -> `run-project`

### Direct Seed Mode

이 하네스는 이제 seed URL을 두 가지 방식으로 해석합니다.

1. curated article seed
   - 블로그 글이나 링크 모음 페이지
   - 내부의 레퍼런스 링크를 추출해 여러 reference로 확장

2. direct reference seed
   - 실제 디자인 시스템 사이트 URL 자체
   - 그 URL 하나를 곧바로 reference로 사용

예:

```bash
uv run design-ontology build-kb \
  --kb-dir kb/default \
  --seed-url https://carbondesignsystem.com \
  --seed-url https://primer.style \
  --seed-url https://design-system.service.gov.uk
```

이 방식은 특정 블로그 글에 의존하지 않고, 공식 디자인 시스템 사이트들을 KB의 1급 입력으로 삼고 싶을 때 더 적합합니다.

## Safe Refactor Policy

이 프레임워크의 산출물은 "전체 UI를 한 번에 갈아엎으라"는 신호가 아닙니다.

기본 원칙:

- 기존 핵심 기능, 진입점, 작업 흐름은 명시적 요청 없이 제거하거나 숨기지 않기
- 전체 셸 리디자인보다 `token -> primitive -> feature surface` 순서의 점진적 적용 우선
- 지원 대상 theme와 breakpoint에서 동시에 성립하는 semantic token부터 먼저 적용
- 시각 개선보다 기능 회귀 방지가 우선
- 패널 위치 변경, 내비게이션 구조 변경, 기본 상호작용 변경은 별도 migration decision으로 다루기
- image-derived hints는 advisory signal이며, anatomy / states / accessibility의 structural source를 대체하지 않기

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
