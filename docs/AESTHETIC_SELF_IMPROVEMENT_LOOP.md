# Aesthetic Self-Improvement Loop

이 문서는 디자인 후보를 심미성 온톨로지로 평가하고, 기준점 통과 전 실행을 막는 게이트 절차를 설명합니다.

## 목적

`aesthetic-loop`는 아름다움의 절대값을 판정하지 않습니다. 대신 특정 브랜드, 사용자, 제품 맥락에서 관찰 가능한 심미성 프록시를 점수화하고, 기준 미달이면 다음 반복에서 고칠 항목을 구조화합니다.

이 루프의 중심은 **우리 브랜드의 디자인 시스템다움**입니다. 기본 시각 품질 점수만 쓰지 않고 `brand_profile.json`에서 브랜드 전용 평가 contract를 생성합니다.

사용하는 연구 기반은 다음처럼 시스템 지표로 변환됩니다.

| 연구/척도 | 여기서 쓰는 방식 |
| --- | --- |
| VisAWI | 웹/UI 심미성을 `simplicity`, `diversity`, `colorfulness`, `craftsmanship` 계열의 visual system coherence로 변환 |
| APiD | designed artifact의 직접적인 aesthetic pleasure를 `desirability`, `emotional_appeal` 쪽에 반영 |
| BeauVis | 점수를 절대 미가 아니라 비교 가능한 context-bound visual representation 평가로 취급 |
| AESTHEMOS | 브랜드 tone과 목표 정서를 `brand_semantic_fit`, `emotional_appeal` 지표로 변환 |
| Kansei / semantic differential | `brand_keywords`, `anti_keywords`를 사람이 느끼는 인상 목표/경계로 변환 |

흐름은 다음과 같습니다.

```text
design candidate metrics
-> aesthetic ontology
-> weighted score + per-dimension floor
-> improvement actions
-> next candidate iteration
-> execution gate opens only after pass
```

## 후보 입력

가장 작은 입력은 다음 형태입니다.

```json
{
  "design_id": "landing-v3",
  "score_scale": 10,
  "metrics": {
    "color_harmony": 8,
    "spacing_consistency": 8,
    "typography_balance": 8,
    "composition_order": 8,
    "hierarchy_clarity": 7,
    "contrast_legibility": 8,
    "content_density_control": 7,
    "task_focus": 8,
    "keyword_alignment": 8,
    "tone_alignment": 8,
    "domain_fit": 8,
    "anti_keyword_avoidance": 9,
    "desirability": 8,
    "confidence_signal": 8,
    "warmth_or_energy": 7,
    "responsive_fit": 8,
    "token_binding": 9,
    "accessibility_baseline": 8,
    "interaction_affordance": 8,
    "asset_completeness": 8,
    "distinctiveness": 7,
    "reference_transformation": 8,
    "memorability": 7
  }
}
```

실제 자기 개선 루프에서는 여러 후보를 같은 파일에 넣을 수 있습니다.

```json
{
  "design_id": "landing-v3",
  "score_scale": 10,
  "iterations": [
    { "iteration_id": "v1", "metrics": { "color_harmony": 6 } },
    { "iteration_id": "v2", "metrics": { "color_harmony": 8 } }
  ]
}
```

## 실행

`run-project`를 실행하면 아래 파일이 자동으로 생성됩니다.

- `build/system/blueprint/aesthetic_ontology.json`
- `build/system/aesthetic/candidate_template.json`
- `build/system/aesthetic/loop_policy.json`

`aesthetic_ontology.json`에는 공통 지표와 브랜드 전용 지표가 함께 들어갑니다.

공통 지표:

- `visual_harmony`
- `clarity`
- `brand_fit`
- `emotional_appeal`
- `craft_quality`
- `novelty`

브랜드 전용 지표:

- `brand_semantic_fit`: `brand_keywords`, `tone_of_voice`를 실제 인상 목표로 평가
- `brand_boundary_fit`: `anti_keywords`, `visual_reference.avoid_patterns`를 피했는지 평가
- `product_ontology_fit`: `product_primitives`, `visual_reference.must_include`가 화면 구조에 드러나는지 평가
- `audience_context_fit`: `audiences`, `accessibility_targets`에 맞는 밀도/명료성/반응형성을 평가

프로젝트 기본 산출물을 쓰는 경우:

```bash
uv run design-ontology aesthetic-loop \
  --project-dir projects/my-app \
  --candidate projects/my-app/build/system/aesthetic/candidate.json \
  --threshold 0.82
```

`--candidate`를 생략하면 `build/system/aesthetic/candidate.json`을 찾습니다. 통과/차단 리포트는 기본적으로 `build/system/aesthetic/latest_loop_report.json`에 저장됩니다.

독립 파일을 직접 지정하는 경우:

```bash
uv run design-ontology aesthetic-loop \
  --candidate build/aesthetic/candidate.json \
  --brand-profile projects/my-app/brand_profile.json \
  --threshold 0.82 \
  --min-dimension-score 0.70 \
  --max-iterations 3 \
  --output build/aesthetic/report.json
```

## 스크린샷 자동 채점

저장된 화면 스크린샷에서 1차 candidate JSON을 자동 생성하려면:

```bash
uv run design-ontology score-screenshot \
  --screenshot projects/my-app/screenshots/desktop.png \
  --screenshot projects/my-app/screenshots/mobile.png \
  --brand-profile projects/my-app/brand_profile.json \
  --output projects/my-app/build/system/aesthetic/candidate.json \
  --run-loop \
  --threshold 0.82
```

이 명령은 픽셀 기반 프록시를 사용합니다.

- 팔레트 통제: 중립/밝은 면, accent 비율, 채도
- 명료성: 명암 범위, 엣지 밀도, 정보 밀도
- 구성 질서: 활성 셀 비율, 구조적 복잡도
- 시각 자산 신호: 사진/텍스처처럼 보이는 영역
- 반응형 커버리지: 모바일/데스크톱 스크린샷 동시 제공 여부

한계도 분명합니다. `score-screenshot`은 이미지 안의 의미를 완전히 이해하지 못하므로 `token_binding`, `domain_fit`, `keyword_alignment` 같은 항목은 프록시 점수입니다. 최종 판단에는 사람/모델 리뷰 또는 구현 lint를 함께 써야 합니다.

프로덕션 판정에서는 멀티모달 리뷰를 별도 JSON으로 남긴 뒤 candidate에 합칩니다.

```bash
uv run design-ontology apply-aesthetic-review \
  --candidate projects/my-app/build/system/aesthetic/candidate.json \
  --review-artifact projects/my-app/build/system/production/reviews/multimodal-review.json \
  --output projects/my-app/build/system/aesthetic/reviewed-candidate.json \
  --reviewer codex-visual-qa \
  --model gpt-5-codex \
  --method "Structured light/dark mobile/desktop review"
```

review artifact의 스키마는 `production-ui-review-artifact/v1`입니다. 기록된 모든 스크린샷 SHA-256과 선택 metric별 점수·구체적인 관찰을 포함해야 합니다. 명령은 artifact 파일의 SHA-256을 두 번째 iteration에 고정하고, 화면 해시가 다르거나 알 수 없는 metric·허용 범위 밖의 점수가 있으면 병합하지 않습니다. 이후 `aesthetic-loop`에는 `reviewed-candidate.json`을 전달합니다.

게이트가 닫히면 종료코드 1을 반환합니다. 그래서 CI나 에이전트 루프에서 다음 작업을 막는 데 바로 쓸 수 있습니다.

통과한 경우에만 후속 명령을 실행하려면:

```bash
uv run design-ontology aesthetic-loop \
  --candidate build/aesthetic/candidate.json \
  --threshold 0.82 \
  --execute-command "uv run pytest"
```

## 판정 조건

기본 통과 조건은 두 가지입니다.

- 전체 가중 점수 `>= 0.82`
- 모든 심미 차원 점수 `>= 0.70`

차원은 `visual_harmony`, `clarity`, `brand_fit`, `emotional_appeal`, `craft_quality`, `novelty`로 구성됩니다. 커스텀 온톨로지가 필요하면 `--ontology custom_ontology.json`으로 교체할 수 있습니다.

## 산출물

리포트는 다음 정보를 포함합니다.

- `ready_to_execute`: 후속 실행 가능 여부
- `execution_gate`: `open` 또는 `blocked`
- `iterations`: 각 후보 반복의 점수와 차원별 세부 점수
- `next_iteration_brief`: 기준 미달 시 다음 반복의 수정 지시
- `ontology`: 평가에 사용한 심미성 온톨로지와 브랜드 맥락
