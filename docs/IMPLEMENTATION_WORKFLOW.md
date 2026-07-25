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
- 생성된 `system_spec.md`, `token_schema.json`, `component_inventory.json`, `STYLE.md` / `DESIGN.md` 소비
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
- 컴포넌트별 anatomy, 상태, props/events, data contract, 반응형·접근성 계약
- 선택적으로 curated color reference 경로와 palette role
- 선택적으로 `visual_reference.sources`에 로컬 스크린샷 / 레퍼런스 이미지

를 작성합니다.

컴포넌트 계약이 길면 프로젝트 안의 별도 JSON으로 분리합니다.

```json
{
  "component_decision_path": "design-system/component-contracts.json"
}
```

외부 파일은 `component_decision` 객체를 감싸거나 그 객체 자체를 담을 수 있습니다. 이 경로는 프로젝트 상대 경로이며 JSON 파일만 허용합니다. 프로젝트 밖으로 벗어나는 경로와 인라인 `component_decision`을 함께 선언한 설정은 실패합니다.

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

### 5.5. 목업 구현: 토큰 방출과 발산 게이트 (필수)

blueprint는 프로젝트마다 다른 팔레트와 서체를 생성하지만, 구현 단계에서 이를 소비하지
않으면 구현 LLM의 기본 미감으로 회귀해 매번 같은 화면이 나온다. 목업/프로토타입을
직접 구현할 때는 아래 순서를 강제한다. 전체 규칙은
`skills/design-ontology-mockup-builder`를 사용한다.

```bash
# 1. blueprint의 active palette / font_system / radius를 프로젝트 로컬 토큰으로 방출
uv run design-ontology emit-tokens --project-dir projects/my-app
# -> projects/my-app/design-system/tokens.css (--ds-color-*, --ds-color-brand-*, --ds-font-*, --ds-radius-*, --ds-space-*)

# 2. 구현: HTML에서 tokens.css를 링크하고 구현 CSS는 var(--ds-*)만 사용
# 제품별 surface/theme 매핑이 필요하면 runtime-theme.css를 tokens.css 다음에 링크

# 3. 토큰 바인딩 강제 (하드코딩 hex/font-family/radius가 있으면 실패)
uv run design-ontology lint-implementation --target-repo projects/my-app

# 4. 교차 프로젝트 스타일 발산 게이트
uv run design-ontology check-style-divergence --project-dir projects/my-app --register-on-pass
```

`check-style-divergence`는 최종 HTML/CSS에서 스타일 지문(surface tone, accent hue
bucket, 폰트 페어링, serif accent, radius 프로파일)을 추출해
`registry/style_fingerprints.json`의 최근 프로젝트들과 비교하고, 아래 두 경우 실패한다.

1. 알려진 수렴 attractor와 일치 — 예: 크림/페이퍼 배경 + 딥 레드/틸 액센트 + 세리프
   디스플레이 (`warm-editorial-default`), 화이트 배경 + 인디고 단일 액센트
   (`indigo-saas-default`)
2. 최근 등록된 지문과 유사도가 임계값(기본 0.62) 이상

실패 리포트의 `[FIX]` 제안을 따르되, 구현 CSS에서 색을 즉흥 수정하지 말고
`brand_profile.json`의 `color_reference.palette_strategy`를 조정한 뒤
`run-project → emit-tokens`로 tokens.css 자체를 재생성한다.

게이트를 통과한 산출물은 `--register-on-pass` 또는 `fingerprint-style`로 레지스트리에
등록해, 다음 프로젝트가 같은 look으로 회귀하지 못하게 한다.

`tokens.css`는 Semantic OS graph가 내장된 Markdown을 바탕으로 `run-project` 또는
`emit-tokens` 때마다 다시 만들어지는 파일입니다. 제품별 light/dark surface와 고유 식별
토큰은 `design-system/runtime-theme.css` 같은 별도 파일에 두고 `tokens.css` 다음에
로드합니다. 이렇게 하면 생성 토큰을 갱신해도 제품별 테마 계약이 남습니다. 로컬 확장도
`lint-implementation` 대상이며, 실제 화면 CSS는 생성 토큰과 확장 토큰만 소비합니다.

### 5.6. 프로덕션 증거와 출고 판정 (필수)

같은 route/state를 light/dark × mobile/desktop으로 캡처해
`record-screenshot-evidence`로 기록합니다. v3 매니페스트는 실제 Git HEAD와 함께 런타임
HTML/CSS/JS 및 연결된 manifest·아이콘·폰트·이미지의 content tree SHA-256을 기록합니다.
스크린샷 크기, 시각 정보 신호, SHA-256도 다시 계산하며, 최신 런타임 파일보다 오래된
캡처는 거부합니다. 토큰·테마·에셋을 건드린 뒤에는 기존 매니페스트에 메타데이터만
다시 붙이지 말고 네 화면을 재캡처합니다.

`score-screenshot`으로 만든 candidate에는 `apply-aesthetic-review`로
`production-ui-review-artifact/v1` 멀티모달 리뷰를 병합합니다. 리뷰에는 매니페스트의
모든 스크린샷 SHA와 선택된 모든 metric의 점수·관찰이 있어야 합니다. 프로덕션 브라우저
증거는 별도의 `production-browser-evidence-bundle/v1`에 기록합니다. Production QA가 Codex
Desktop의 `browser:browser`로 실제 IAB 세션을 실행하고, screenshot·DOM·state·console·
interaction·overflow·accessibility 및 component-runtime 관찰을 같은 session ID와 현재
runtime tree SHA에 연결해야 합니다. 각 원시 관찰은 `production-browser-observation/v1` JSON과
SHA-256으로 보존합니다. 사람이 쓴 `passed: true` 중심의 `production-ui-runtime-check/v1`은
구형 호환 자료일 뿐이며 프로덕션 브라우저 증거로는 거부합니다. 전체 계약과 예시는
[Browser Evidence Bundle](BROWSER_EVIDENCE_BUNDLE.md)에 있습니다.

```bash
uv run design-ontology apply-aesthetic-review \
  --candidate projects/my-app/build/system/aesthetic/candidate.json \
  --review-artifact projects/my-app/build/system/production/reviews/multimodal-review.json \
  --output projects/my-app/build/system/aesthetic/reviewed-candidate.json \
  --reviewer codex-visual-qa \
  --model gpt-5-codex \
  --method "Structured light/dark mobile/desktop review"

uv run design-ontology aesthetic-loop \
  --project-dir projects/my-app \
  --candidate projects/my-app/build/system/aesthetic/reviewed-candidate.json

uv run design-ontology verify-production-ui \
  --project-dir projects/my-app \
  --target-repo projects/my-app \
  --browser-evidence-bundle projects/my-app/build/system/production/browser-evidence-bundle.json
```

`verify-production-ui`는 빈·중복 스크린샷, route/state/theme/viewport 비대칭, review 또는
browser artifact 해시 불일치, IAB producer/session 또는 runtime tree 불일치, 불완전한 metric
근거, 실제 브라우저 observation 실패를 모두 blocking 오류로 처리합니다.

### 6. 프리셋 승격과 Style Capsule 생성

구현 repo에 설치하려면 프로젝트 산출물을 프리셋으로 승격합니다. 이 단계에서 `STYLE.md`와 `DESIGN.md`가 생성됩니다.

```bash
uv run design-ontology build-preset \
  --project projects/my-app \
  --preset-id conversation-copilot--corporate-trust \
  --owner maintainer \
  --tier P3 \
  --color-modes light \
  --default-color-mode light \
  --tags ko,enterprise,copilot
```

생성 파일:

- `presets/<id>/STYLE.md`
- `presets/<id>/DESIGN.md`
- `presets/<id>/manifest.json`
- `presets/<id>/preview.md`
- `presets/<id>/token_schema.json`
- `presets/<id>/component_inventory.json`
- `presets/<id>/system_spec.md`

`STYLE.md` / `DESIGN.md`는 에이전트가 먼저 읽는 스타일 캡슐입니다. 자세한 규칙은 [STYLE_CAPSULE.md](./STYLE_CAPSULE.md)를 참고합니다.

## How To Use In A Real Implementation Repo

### Option 1. Separate harness repo + product repo

가장 추천하는 방식입니다.

1. 이 저장소에서 KB와 시스템 산출물 생성
2. 생성된 결과를 실제 제품 저장소로 복사하거나 서브모듈/서브트리/CI artifact로 전달
3. 제품 저장소에서 토큰과 컴포넌트 구현

이때 연결 포인트는 보통 아래와 같습니다.

- `IMPLEMENTATION_CONTRACT.md` -> 외부 reference 흡수 범위와 구현 preflight
- `STYLE.md` / `DESIGN.md` -> 구현자가 먼저 읽는 짧은 스타일 캡슐
- `token_schema.json` -> CSS variables / Tailwind theme / design token pipeline
- `component_inventory.json` -> 구현 우선순위와 컴포넌트 backlog
- `system_spec.md` -> 디자이너/개발자 공통 기준 문서
- `system_ontology.json` -> agent prompt context 또는 graph DB 입력

프리셋은 adapter로 바로 설치할 수 있습니다.

```bash
uv run design-ontology install-preset \
  --preset-id conversation-copilot--corporate-trust \
  --target-repo /path/to/implementation-repo \
  --adapter raw-css-variables \
  --color-mode light \
  --locale ko
```

원하면 implementation repo에 Codex / Claude Code integration pack도 생성할 수 있습니다.

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

1. `design-system/IMPLEMENTATION_CONTRACT.md`
2. `design-system/STYLE.md` 또는 `design-system/DESIGN.md`
3. `design-system/system_spec.md`
4. `design-system/token_schema.json`
5. `design-system/component_inventory.json`
6. `design-system/components/component_specs.md`
7. 구현 대상 코드베이스

그 다음 에이전트에게 아래처럼 지시합니다.

- `token_schema.json`에 맞춰 CSS 변수와 theme object 생성
- `component_inventory.json`의 high priority family부터 구현
- `system_spec.md`의 anti-keyword를 위반하지 않게 UI 의사결정
- `STYLE.md`와 `component_specs.md`의 visual hints는 reference 형태·밀도 흡수에만 사용
- 외부 reference에서 색상, 폰트, IA, copy를 가져오지 않음
- 새 컴포넌트 추가보다 기존 primitive 확장을 우선

권장 프롬프트:

```text
design-system/IMPLEMENTATION_CONTRACT.md,
design-system/STYLE.md,
design-system/token_schema.json,
design-system/components/component_specs.md 기준으로 이 화면을 리팩해줘.

외부 참고 이미지는 형태, 밀도, 컴포넌트 비례만 반영하고
색상, 폰트, IA, 카피는 온톨로지와 토큰을 우선해.
작업 후 lint-implementation까지 돌려줘.
```

검증:

```bash
uv run design-ontology lint-implementation --target-repo /path/to/implementation-repo
```

## Practical Rollout Order

실제 제품에 붙일 때 추천 순서:

1. color / typography / spacing 토큰
2. button / input / navigation
3. feedback / overlay
4. 제품 특화 primitive
5. 문서화와 테스트

## `color-reference.md`가 단일 컬러 소스

컬러 파이프라인의 단일 런타임 기준은 `docs/color-reference.md`입니다. 이 파일은 사람이 읽는 87개 색상 카드와 기계가 읽는 Semantic OS graph를 함께 담습니다. 보이는 카드는 동기화 전후에도 바이트 단위로 보존되고, 로컬 경로·원문 복원 가능 데이터를 제거한 전체 graph는 문서 마지막의 `semantic-color-ontology+json` fenced block에 저장됩니다.

런타임은 embedded block의 checksum을 먼저 확인한 뒤 보이는 카드와 graph의 `ColorKeyword`를 메모리에서 합칩합니다. 자동 palette candidate, 수동 `palette_roles`, supporting color 선택은 모두 이 합쳐진 데이터를 사용합니다. `color_reference.path`를 생략하면 wheel에 포함된 기본 Markdown을 읽습니다.

`design_ontology_harness/resources/semantic_color_ontology.json`은 기존 사용자와 외부 운반 경로를 위해 남겨 둔 호환 산출물입니다. 런타임은 이 JSON을 진실 소스나 fallback으로 사용하지 않습니다.

### Semantic OS graph 동기화

```bash
uv run design-ontology sync-semantic-colors \
  --source ../semantic-os/domains/color/ontology/build/graph.json \
  --color-reference-output docs/color-reference.md \
  --ontology-output design_ontology_harness/resources/semantic_color_ontology.json

uv run design-ontology sync-semantic-colors \
  --source ../semantic-os/domains/color/ontology/build/graph.json \
  --color-reference-output docs/color-reference.md \
  --ontology-output design_ontology_harness/resources/semantic_color_ontology.json \
  --check \
  --json
```

기본 실행은 보이는 색상 카드를 수정하지 않고 embedded graph block과 checksum만 갱신합니다. `--ontology-output`은 호환 JSON도 함께 갱신합니다. `--check`는 파일을 쓰지 않고 source graph, fenced block, checksum이 같은 snapshot인지 확인하며, `--json`은 CI에서 읽을 수 있는 결과를 출력합니다.

Semantic OS에 없는 색은 보이는 카드의 Markdown-only 로컬 확장으로 유지할 수 있습니다. 출처와 사용 범위를 명시하고 Semantic OS 유래 색으로 표시하지 마세요. 동기화 명령은 이 카드를 지우지 않으며, 런타임은 내장 graph의 색과 함께 명시적 확장으로 합칩합니다.

- **레지스트리 인지 hue 감점**: 후보 키워드 스코어링은 `registry/style_fingerprints.json`의 최근 accent hue 사용 횟수를 읽어 반복 hue를 감점합니다. 재정렬 결과는 `semantic_color_selection.registry_hue_pressure`, `hue_pressure_reordered`에 남습니다.
- **수동 역할명**: `palette_roles`의 이름은 보이는 카드와 내장 `ColorKeyword`를 합친 이름 공간에서 해석합니다.
- **supporting 확장**: spectrum, family, mood, 반복 hue 조건은 같은 Markdown에 내장된 graph에서 찾고, 최종 색 값도 같은 파일에서 확정합니다.

주의: graph snapshot을 갱신하면 supporting color 구성이나 이름이 달라질 수 있습니다. 이미 방출된 프로젝트의 `tokens.css`를 다시 `emit-tokens`로 갱신할 때는 구현 CSS가 참조하는 `--ds-color-support-*` 이름이 유지되는지 확인하세요.

생성된 `tokens.css`는 직접 수정하지 않습니다. 제품별 light/dark surface 매핑과 프로젝트 고유 토큰은 `design-system/runtime-theme.css` 같은 로컬 확장 파일에 두고, `tokens.css` 다음에 로드합니다. 이 파일은 재생성 대상이 아니므로 Semantic OS snapshot이나 토큰을 갱신해도 보존됩니다.

## 프로젝트별 color reference 설정

`brand_profile.json`의 `color_reference.path`는 일반적으로 `docs/color-reference.md`를 가리킵니다. 다른 문서를 지정하려면 같은 visible-card + checksum-verified graph block 계약을 지켜야 합니다.

예:

```json
{
  "color_reference": {
    "path": "/absolute/path/to/color-reference.md",
    "preferred_families": ["Deep Reds", "Standard Oranges", "Pastel Oranges"],
    "palette_strategy": {
      "mode": "brand-guided",
      "candidate_count": 5,
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

- `brand_profile.json`과 `spec.md`에서 앱 주제, 작업 표면, 컴포넌트 신호를 모으고
- Markdown에 내장된 `ColorPattern`·관계·정책을 검색해 palette candidate 구조를 만들고
- 보이는 카드와 `ColorKeyword`를 합친 swatch, mood, usage, preferred family로 실제 후보 색을 확정하고
- active palette를 semantic role 힌트와 함께 고정하고
- seed color pairings와 관련 family를 추가 검색해 support / neutral / state color를 확장하고
- 내장 graph에서 spectrum / family / mood_tags / tone_axes와 팔레트 추상화 guardrail을 붙이고
- `system_spec.md`와 `token_schema.json`에 색상 기준으로 기록합니다.

중요: 자동 모드에서는 미리 만든 팔레트 세트를 그대로 사용하지 않습니다. 매 실행마다 앱 내용으로 내장 graph를 검색하고, 후보 팔레트에는 `selection_method=semantic-os-markdown-search-per-run`과 Markdown 출처가 모두 남아야 합니다.

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
