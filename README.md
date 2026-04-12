# Design Ontology Harness

디자인 시스템 레퍼런스를 수집해 KB로 저장하고, 그 근거를 바탕으로 각자 자신의 디자인 시스템 하네스 프로젝트를 만들 수 있게 해주는 GitHub 배포형 오픈소스 프레임워크입니다.

즉 이 저장소의 기본 정체성은:

- Claude/Codex 전용 플러그인 자체
- 하나의 앱을 대신 디자인해주는 생성기

가 아니라

- 재사용 가능한 디자인 시스템 하네스 코어
- 프로젝트별 시스템 산출물 생성기
- 필요하면 Claude/Codex가 읽을 수 있는 integration pack 생성기

입니다.

레퍼런스를 "매번 다시 읽는 크롤러"가 아니라:

- 공용 KB를 만들고
- 그 KB를 프로젝트별로 재사용하고
- 각 제품의 브랜드 정체성에 맞는 시스템 산출물을 생성하는

재사용 가능한 디자인 시스템 authoring framework를 목표로 합니다.

## What This Is

- GitHub에서 배포하고 각자가 clone해서 쓰는 하네스
- KB build -> brand-driven synthesis -> implementation handoff 흐름의 프레임워크
- `system_spec`, `token_schema`, `component_inventory`, `system_ontology`를 만드는 코어 엔진

## What This Is Not

- Claude Code 전용 marketplace plugin 제품
- 레퍼런스를 그대로 복제하는 스크래퍼
- 기존 앱을 한 번에 갈아엎는 리디자인 도구

## Why

대부분의 디자인 시스템 작업은 아래 문제를 반복합니다.

- 참고자료는 많은데, 내 제품에 맞는 기준으로 정리되지 않음
- 레퍼런스를 그대로 베끼면 브랜드 아이덴티티가 사라짐
- 에이전트나 팀원이 같은 설계 맥락을 반복해서 다시 이해해야 함

이 저장소는 그 문제를:

1. `KB build`
2. `brand-driven synthesis`
3. `implementation-ready outputs`

의 흐름으로 해결하려고 합니다.

중요하게, 이 산출물들은 "전면 UI 리라이트 허가서"가 아닙니다. 기본 철학은 기존 제품의 기능과 진입점을 보존한 채, 토큰과 primitive부터 점진적으로 시스템화하는 것입니다.

핵심은 "남의 시스템을 복제"하는 것이 아니라:

1. 레퍼런스를 수집하고
2. 구조를 해체하고
3. 자기 브랜드/제품 정체성을 입력한 뒤
4. 자신의 시스템 스펙과 토큰 구조를 생성하는 것입니다.

## What It Does

1. 시드 글에서 외부 레퍼런스 링크를 추출합니다.
2. 각 레퍼런스의 문서 페이지를 제한적으로 크롤링합니다.
3. 제목, 설명, 헤딩, 본문 텍스트, 내부 링크를 정제해서 저장합니다.
4. 디자인 시스템 개념어를 기준으로 온톨로지 후보와 근거 문장을 JSONL로 저장합니다.
5. 브랜드 아이덴티티 프로필을 주입하면, 레퍼런스를 참고하되 복제하지 않는 자체 디자인 시스템 블루프린트를 생성합니다.
6. 블루프린트에서 끝나지 않고 실제 시스템 스펙, 토큰 스키마, 컴포넌트 인벤토리, 시스템 온톨로지 그래프 초안을 함께 생성합니다.
7. 필요하면 로컬의 curated color reference markdown을 읽어 색상 방향을 시스템 산출물에 반영합니다.

## TL;DR

```bash
uv sync

# 1) build shared knowledge
uv run design-ontology build-kb \
  --kb-dir kb/default \
  --seed-url https://spacebar310.tistory.com/86

# 2) create your project workspace
uv run design-ontology init \
  --project-dir projects/my-app \
  --brand-name "My App" \
  --product-summary "What this product is for" \
  --kb-dir ../../kb/default

# 3) generate brand-specific system outputs
uv run design-ontology run-project --project-dir projects/my-app
```

이 세 단계만으로도 이 저장소의 핵심 가치는 충분히 사용 가능합니다. Claude/Codex 연동은 선택 사항입니다.

## Public Repo Flow

### 0. 공용 KB 만들기

한 번 수집한 지식베이스를 여러 프로젝트가 재사용하도록 설계되어 있습니다.

```bash
uv sync
uv run design-ontology build-kb \
  --kb-dir kb/default \
  --seed-url https://spacebar310.tistory.com/86
```

이 단계는 가끔만 실행하면 됩니다. 프로젝트를 돌릴 때마다 외부 링크를 다시 읽을 필요는 없습니다.

### 1. 새 프로젝트 스캐폴드

```bash
uv sync
uv run design-ontology init \
  --project-dir projects/my-app \
  --brand-name "My App" \
  --product-summary "What this product is for" \
  --kb-dir ../../kb/default \
  --seed-url https://spacebar310.tistory.com/86
```

이 명령은 아래 파일을 만들어 줍니다.

- `projects/my-app/brand_profile.json`
- `projects/my-app/seeds/seed_urls.txt`
- `projects/my-app/project_manifest.json`
- `projects/my-app/agent_brief.md`
- `projects/my-app/README.md`

### 2. 프로젝트 입력값 수정

- `brand_profile.json`에 제품 정체성 입력
- 필요하면 `project_manifest.json`의 `kb_dir` 수정
- `seeds/seed_urls.txt`는 provenance 또는 차후 KB 갱신용 메모로 유지 가능

선택적으로 `brand_profile.json`에 `color_reference`를 넣으면 로컬 markdown 색상 문서를 읽어 system spec과 token schema에 반영할 수 있습니다.

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

`selected_colors`와 `palette_roles`를 넣으면 manual override로 동작합니다. 자동 모드에서는 브랜드 키워드와 색상 문서의 mood/usage를 바탕으로 여러 palette candidate를 만들고, 그중 active palette를 system outputs에 기록합니다. `preferred_families`는 hard filter가 아니라 우선순위 bias로 취급됩니다.

`palette_expansion`이 켜져 있으면 하네스는 active palette 3색에서 끝나지 않고:

- seed color의 `pairings`를 우선 검색하고
- 같은 hue의 다른 tone, 관련 family, 브랜드 mood 신호를 함께 점수화하고
- support / neutral / semantic state / surface-system까지 확장된 색상 리스트를 만듭니다.

### 3. 프로젝트 실행

```bash
uv run design-ontology run-project --project-dir projects/my-app
```

결과는 `projects/my-app/build/system/` 아래에 생성됩니다.

대표 산출물:

- `build/system/blueprint/system_spec.md`
- `build/system/blueprint/token_schema.json`
- `build/system/blueprint/component_inventory.json`
- `build/system/blueprint/system_ontology.json`

`color_reference`가 설정되어 있으면 위 산출물 안에:

- 색상 기준 source path
- active palette와 semantic role 힌트
- palette candidate 목록과 선택 전략
- expanded supporting colors와 combination lists
- surface/text/border/status까지 이어지는 semantic color roles

가 함께 들어갑니다.

## Direct Run

하나의 시드에 대해 바로 돌리고 싶으면 기존 CLI도 사용할 수 있습니다.

```bash
uv sync
uv run design-ontology run \
  --seed-url https://spacebar310.tistory.com/86 \
  --output-dir data \
  --brand-profile config/brand_profile.example.json \
  --max-pages-per-source 3 \
  --max-depth 1
```

샘플 실행 후 주요 산출물:

- `data/seed_article.json`
- `data/references.jsonl`
- `data/crawls/<source-slug>/manifest.json`
- `data/crawls/<source-slug>/documents.jsonl`
- `data/ontology/concepts.json`
- `data/ontology/evidence.jsonl`
- `data/ontology/relations.jsonl`
- `data/blueprint/design_system_blueprint.json`
- `data/blueprint/profile_validation.json`
- `data/blueprint/system_spec.md`
- `data/blueprint/token_schema.json`
- `data/blueprint/component_inventory.json`
- `data/blueprint/system_ontology.json`

## Notes

- 외부 링크 중 일부는 오래된 주소, 로그인 필요, JS 렌더링 의존, 혹은 접근 제한으로 인해 수집이 실패할 수 있습니다.
- 실패한 링크도 매니페스트에 상태와 이유를 남깁니다.
- 현재 온톨로지 추출은 규칙 기반 초기 버전입니다. 이후 LLM 기반 정규화나 그래프 DB 적재 단계로 확장하기 쉽게 만들어 두었습니다.
- `config/brand_profile.example.json`은 예시이므로 실제 브랜드 키워드와 제품 문맥으로 바꾸는 것이 좋습니다.

## Repo Layout

- `design_ontology_harness/`: framework core
- `schemas/`: input schemas
- `config/`: example brand profiles
- `docs/`: architecture and implementation docs
- `kb/`: reusable knowledge bases, usually generated locally and gitignored
- `projects/`: scaffolded project workspaces

## Agent Packs

Implementation repo에 바로 심을 수 있는 Codex / Claude Code integration pack도 생성할 수 있습니다. 다만 이건 이 저장소의 본체가 아니라, 생성된 산출물을 실제 구현 레포에서 더 잘 쓰기 위한 선택적 부가 레이어입니다.

```bash
uv run design-ontology init-agent-pack \
  --target-repo /path/to/implementation-repo \
  --artifact-dir design-system \
  --targets codex,claude
```

이 명령은:

- Codex plugin + skills
- Claude Code project skills + subagents

를 생성합니다. 자세한 내용은 `docs/AGENT_INTEGRATIONS.md`를 참고하세요.

생성되는 스킬들은 기본적으로:

- 기존 feature surface 보존
- theme / breakpoint 호환 유지
- semantic token 우선 적용
- 전면 셸 리라이트보다 점진적 리팩터 우선

원칙을 따르도록 설계되어 있습니다.

## Authoring Flow

1. `config/brand_profile.example.json`을 복사해 실제 브랜드 프로필을 작성합니다.
2. `uv run design-ontology run ... --brand-profile ...`로 레퍼런스 수집과 시스템 생성까지 한 번에 실행합니다.
3. `data/blueprint/system_spec.md`를 검토하면서 원칙, 토큰, 컴포넌트 정책을 다듬습니다.
4. 필요하면 `uv run design-ontology synthesize --output-dir data --brand-profile ...`만 다시 실행해 산출물을 재생성합니다.

## For GitHub Publishing

- 이 저장소는 프레임워크 코어입니다.
- 각 사용자는 `projects/<name>/` 아래에서 자신의 하네스 프로젝트를 독립적으로 만들 수 있습니다.
- 예제 프로필은 포함할 수 있지만, 코어 로직은 특정 앱에 종속되지 않게 유지하는 것이 좋습니다.
- 입력 스키마는 `schemas/brand_profile.schema.json` 기준으로 관리할 수 있습니다.
- 실제 구현 프로젝트 연결 방식은 `docs/IMPLEMENTATION_WORKFLOW.md`를 참고하면 됩니다.

## License

MIT. See `LICENSE`.

## Recommended Mental Model

- `build-kb`: 외부 레퍼런스를 수집해 공용 지식베이스 생성
- `run-project`: 저장된 KB를 읽어 특정 앱의 디자인 시스템 산출물 생성
- `synthesize`: 기존 출력 디렉터리에서 브랜드 프로필만 바꿔 재생성
