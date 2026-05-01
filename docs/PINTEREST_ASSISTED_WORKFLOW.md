# Pinterest-assisted Visual Collection

## 목적

Pinterest-assisted 모드는 Pinterest를 직접 truth source로 삼는 기능이 아니라, visual reference를 더 빨리 찾기 위한 **검색 보조 + 선택 보조 레이어**입니다.

핵심 원칙:

- 공식 KB / `spec.md` / `brand_profile.json` / `color_reference`는 구조적 source of truth
- Pinterest는 조형 언어 탐색용 검색 채널
- 최종 분석 입력은 언제나 로컬 파일 기반 `visual_reference.sources`
- 보드/핀 URL은 분석 대상이 아니라 provenance 또는 캡처 메모
- manifest와 visual outputs는 `observed` / `inferred` / `unverified` provenance 문맥을 유지
- 구현 repo에서는 `STYLE.md` / `DESIGN.md`와 `IMPLEMENTATION_CONTRACT.md`가 Pinterest reference의 흡수 범위를 제한합니다. 색상, 폰트, IA, copy는 Pinterest에서 가져오지 않습니다.

## 권장 운영 흐름

1. `generate-visual-queries`로 query set 생성
2. query별로 Pinterest에서 보드/핀 후보를 탐색
3. 스크린샷 또는 저장 이미지를 로컬 `capture_dir`에 수집
4. `pinterest_candidate_manifest.json`에 후보를 채움
5. 사람 또는 에이전트가 명시적으로 선택
6. 선택된 캡처만 `visual_reference.sources`로 승격
7. `analyze-visuals` -> `run-project`
8. `build-preset` -> `install-preset`으로 `STYLE.md` / `DESIGN.md`를 구현 repo에 배포

## 산출물

`generate-visual-queries` 실행 시 아래 파일이 함께 생성됩니다.

- `build/visuals/visual_query_suggestions.json`
- `build/visuals/pinterest_assist_plan.json`
- `build/visuals/pinterest_candidate_manifest.json`
- `build/visuals/pinterest_selection_manifest.json`

### `pinterest_assist_plan.json`

검색/수집 작업을 위한 운영 계획입니다.

- query별 `query_id`
- query intent / primitive
- 후보 수집 슬롯 수
- selection 슬롯 수
- 권장 캡처 경로 prefix
- preferred source order (`pins`, `boards`, `adjacent-search`)
- `risk_guardrails` 섹션으로 로그인/동적 로딩/결과 변경성/저작권/접근 제약 정책 명시

### `pinterest_candidate_manifest.json`

query별 후보 캡처를 적는 작업용 파일입니다.

후보 항목 예:

```json
{
  "candidate_id": "q01-c01",
  "status": "open",
  "source_type": null,
  "platform": "pinterest",
  "board_url": null,
  "pin_url": null,
  "reference_url": null,
  "capture_path": null,
  "thumbnail_path": null,
  "capture_method": "screenshot",
  "usage_scope": "reference-analysis-only",
  "redistribution_allowed": false,
  "access_notes": null,
  "notes": null,
  "selected": false
}
```

이 단계에서는 아직 `visual_reference.sources`에 연결하지 않습니다.

### `pinterest_selection_manifest.json`

명시적으로 채택한 캡처만 기록합니다.

- `candidate_id`
- `reference_url`
- `capture_path`
- 선택 이유
- 후속 분석에 포함할지 여부

이 파일의 선택 항목만 `visual_reference.sources`로 승격하는 것을 권장합니다.

선택 기록 예:

```bash
uv run design-ontology select-pinterest-candidates \
  --project-dir projects/checkpoint \
  --candidate q03-c02 \
  --candidate q05-c02 \
  --candidate q13-c05
```

선택과 동시에 `visual_reference.sources`까지 반영하려면:

```bash
uv run design-ontology select-pinterest-candidates \
  --project-dir projects/checkpoint \
  --candidate q03-c02 \
  --candidate q05-c02 \
  --candidate q13-c05 \
  --sync-sources
```

이미 선택 manifest가 채워져 있다면, 나중에 별도로 동기화만 실행할 수도 있습니다.

```bash
uv run design-ontology sync-pinterest-selection \
  --project-dir projects/checkpoint
```

## Capture Modes

### 1. `manual-save`

현재 기본값이며 가장 안전한 방식입니다.

- 사용자가 Pinterest에서 검색
- 보드/핀을 눈으로 보고 선택
- 스크린샷 또는 저장 이미지를 로컬에 보관
- manifest에 provenance만 기록

### 2. `playwright-capture`

현재 구현된 자동 수집 모드입니다.

- query별 검색 페이지 또는 후보 목록을 브라우저로 열기
- 보이는 pin tile을 candidate 단위로 스크린샷 저장
- pin URL, aria-label/alt text, search URL을 manifest에 기록
- 최종 채택은 여전히 사용자 또는 에이전트가 명시적으로 고정

중요: Playwright 자동화는 후보 수집을 돕는 용도이지, 선택을 자동 확정하는 용도가 아닙니다.

실행 방법:

```bash
uv run design-ontology capture-pinterest \
  --project-dir projects/checkpoint
```

또는 `brand_profile.visual_reference.pinterest_assist.capture_mode`가 `playwright-capture`이고
`enabled: true`이면 `generate-visual-queries` 실행 직후 자동 캡처가 이어집니다.

## Risk Guardrails

이 모드에서는 아래 리스크를 기본 전제로 둡니다.

1. 로그인 필요 / 동적 로딩
   Pinterest는 로그인 벽, 무한 스크롤, DOM 변경으로 자동화가 불안정할 수 있습니다. 자동화가 불안정하면 즉시 `manual-save`로 폴백합니다.
2. 결과 변경성
   같은 query라도 계정 상태, 지역, 시점에 따라 결과가 달라질 수 있습니다. query만으로 재현성을 보장하지 말고 로컬 캡처를 기준으로 삼습니다.
3. 저작권 / 재배포
   보드/핀은 참고용 레퍼런스입니다. raw asset 다운로드보다 screenshot/reference URL 기록을 우선하고, 재배포 가능한 권리가 있다고 가정하지 않습니다.
4. robots / 접근 제약
   robots, 접근 제한, auth prompt가 있으면 우회하지 않습니다. 자동 수집을 중단하고 수동 캡처 또는 대체 레퍼런스로 전환합니다.

## brand_profile 설정

```json
{
  "visual_reference": {
    "mode": "pinterest-assisted",
    "query": [
      "editorial dashboard",
      "warm premium onboarding flow"
    ],
    "sources": [],
    "pinterest_assist": {
      "enabled": true,
      "capture_mode": "manual-save",
      "capture_dir": "references/visual/pinterest-assisted",
      "max_candidates_per_query": 6,
      "max_selected_per_query": 2,
      "preferred_sources": ["pins", "boards", "adjacent-search"]
    }
  }
}
```

설명:

- `query`: 검색어 후보
- `sources`: 최종적으로 확정된 로컬 파일
- `capture_dir`: 임시/후보 캡처를 저장할 로컬 디렉터리
- `max_candidates_per_query`: query별 수집 후보 수
- `max_selected_per_query`: query별 최종 채택 슬롯 수

## Explicit Selection Rule

이 모드의 핵심 규칙은 explicit selection입니다.

- candidate -> selected 전환은 사람이 하거나, 에이전트가 하더라도 명시적으로 기록되어야 합니다.
- `selected`로 승격되지 않은 보드/핀은 분석 입력으로 사용하지 않습니다.
- `visual_reference.sources`는 최종 선별된 로컬 파일만 포함합니다.

## 다음 단계

남은 확장 포인트:

- 보드 단위 수집 / 다중 viewport 캡처
- 캡처 실패 query만 재시도하는 retry CLI
