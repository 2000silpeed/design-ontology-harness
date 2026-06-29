# Website Reference Inspection

`inspect-reference-site`는 공개 웹페이지를 그대로 복제하기 위한 명령이 아닙니다.
브라우저로 화면을 열어 스크린샷, 페이지 구조, 상호작용 단서, 에셋 레이어,
computed style 근거를 수집한 뒤, 이를 `Design Context Pack`에 넣을 수 있는
advisory reference로 정리합니다.

## 원칙

- 참고 사이트의 형태, 밀도, 섹션 리듬, 상호작용 affordance만 흡수합니다.
- 색상 팔레트, 타이포그래피 스케일, IA, 문구, 로고, 이미지 에셋은 복사하지 않습니다.
- 구현 기준은 항상 `brand_profile.json`, `spec.md`, `token_schema.json`,
  `component_specs.md`, `system_spec.md`입니다.

## 사용

```bash
uv run design-ontology inspect-reference-site \
  --project-dir projects/my-app \
  --url https://example.com/product \
  --label "Example product page"
```

기본 출력 위치:

```text
projects/my-app/build/website_research/
  website_reference_report.json
  design_context_source.json
  design_context_pack.json
  PAGE_TOPOLOGY.md
  BEHAVIORS.md
  assets_manifest.json
  computed_styles.json
  screenshots/
    desktop.png
    tablet.png
    mobile.png
```

`brand_profile.visual_reference.sources`에 이 inspection source를 바로 추가하려면
명령 끝에 `--sync-brand-profile`을 붙입니다.

```bash
uv run design-ontology inspect-reference-site \
  --project-dir projects/my-app \
  --url https://example.com/product \
  --sync-brand-profile
```

그 다음 일반 visual analysis 또는 project build 흐름으로 넘길 수 있습니다.

```bash
uv run design-ontology analyze-visuals --project-dir projects/my-app
uv run design-ontology run-project --project-dir projects/my-app
```

## 산출물 해석

- `PAGE_TOPOLOGY.md`: 섹션 순서, 역할, 레이아웃 힌트, interaction model.
- `BEHAVIORS.md`: sticky/fixed, transition, animation, 클릭/입력 affordance.
- `assets_manifest.json`: 이미지, 비디오, background image, inline SVG 개수와 위치.
- `computed_styles.json`: 주요 요소의 `getComputedStyle()` 근거. 그대로 토큰으로
  흡수하지 말고, 형태와 상태 해석의 근거로만 씁니다.
- `design_context_pack.json`: provider-neutral reference layer. `website-inspection`
  provider는 active로 기록되지만, absorption policy의 denied 항목을 항상 함께 가집니다.

## 구현 에이전트에 넘길 때

구현 레포에는 원본 사이트를 복제하라고 지시하지 말고, 아래처럼 지시합니다.

```text
design-system/STYLE.md, token_schema.json, component_specs.md를 우선해.
website_research/design_context_pack.json은 형태, 밀도, interaction affordance 참고로만 써.
색상, 폰트, IA, 카피, 외부 이미지는 가져오지 마.
작업 후 lint-implementation과 desktop/mobile screenshot QA를 실행해.
```
