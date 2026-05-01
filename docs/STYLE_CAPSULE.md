# Style Capsule

## 목적

`STYLE.md`와 `DESIGN.md`는 프리셋을 실제 구현 repo에 설치할 때 함께 배포되는 짧은 실행 브리프입니다.

이 문서는 외부 reference를 새 기준으로 삼기 위한 문서가 아닙니다. `brand_profile.json`, `design_system_blueprint.json`, `token_schema.json`, `component_inventory.json`, `component_specs.json`, governance rule을 압축해서 Codex / Claude / 사람 구현자가 먼저 읽을 수 있게 만든 문서입니다.

## 왜 필요한가

기존 산출물은 정확하지만 길었습니다.

- `system_spec.md`: 전체 설계 원칙과 그래프 섹션까지 포함
- `token_schema.json`: 토큰 체계 전체
- `component_specs.md`: 컴포넌트별 anatomy, states, token binding
- `system_ontology.json`: 관계 그래프

구현자는 빠르게 화면을 고칠 때 이 전체를 매번 깊게 읽지 못합니다. 그래서 reference 이미지를 보고 “색상/폰트/레이아웃까지 따라가는” 실수가 생겼습니다.

Style Capsule은 이 실수를 막기 위한 첫 화면입니다.

## 생성 위치

`build-preset` 단계에서 프리셋 루트에 생성됩니다.

```text
presets/<preset-id>/
  STYLE.md
  DESIGN.md
  preview.md
  manifest.json
  token_schema.json
  component_inventory.json
  system_spec.md
  components/component_specs.md
```

`install-preset`을 실행하면 구현 repo로 복사됩니다.

```text
<target-repo>/design-system/
  IMPLEMENTATION_CONTRACT.md
  STYLE.md
  DESIGN.md
  tokens.css
  fonts.css
  system_spec.md
  token_schema.json
  component_inventory.json
  components/component_specs.md
```

## STYLE.md 와 DESIGN.md 차이

현재 두 파일은 같은 내용을 담습니다.

- `STYLE.md`: 사람이 읽기 쉬운 이름
- `DESIGN.md`: Refero류 도구와 에이전트가 기대하기 쉬운 이름

두 이름을 모두 배포하는 이유는 도구/에이전트마다 관습이 다르기 때문입니다. 내용의 source of truth는 동일한 렌더러(`style_capsule.py`)입니다.

## 포함 내용

Style Capsule은 아래 섹션으로 구성됩니다.

- Taste Summary
- Authority Order
- Voice And Boundaries
- Color Roles
- Typography
- Spacing And Shape
- Component Priorities
- Signature Components
- Reference Governance
- Agent Preflight

특히 `Reference Governance`와 `Agent Preflight`가 중요합니다.

## 권한 순서

구현자는 항상 아래 순서를 따릅니다.

1. 제품 task flow와 information architecture
2. `token_schema.json`과 generated CSS variables
3. `components/component_specs.*`와 `component_inventory.json`
4. `system_spec.md`와 `system_ontology.json`
5. 외부 visual references

외부 reference는 마지막입니다. reference가 멋있어 보여도 색상, 폰트, copy, navigation label, domain IA를 가져오면 실패입니다.

## Reference Absorption Rule

허용:

- component morphology
- layout density
- panel/card proportions
- hierarchy rhythm
- interaction affordance patterns

금지:

- color palette
- palette composition or derived secondary palettes
- typography family or scale
- semantic status colors
- product copy
- product data model
- navigation labels
- domain information architecture
- redistributable imagery unless explicitly licensed

## Token Binding Is Not Enough

이번 mock 테스트에서 확인한 중요한 실패 패턴입니다.

나쁜 예:

```css
:root {
  --local-dashboard-rail: color-mix(
    in srgb,
    var(--ds-color-info),
    var(--ds-color-surface-tint)
  );
}
```

`--ds-*` 토큰을 쓰고 있어도, 여러 chromatic role을 섞어서 reference 이미지처럼 보이는 새 팔레트를 만들면 온톨로지 위반입니다.

좋은 예:

```css
.review-panel {
  color: var(--ds-color-ink);
  background: var(--ds-color-surface);
  border-color: var(--ds-color-border);
}

.policy-badge {
  color: var(--ds-color-primary);
  background: color-mix(in srgb, var(--ds-color-primary) 10%, transparent);
}
```

한 semantic role을 neutral surface 또는 transparent와 섞는 것은 허용됩니다. 여러 chromatic role을 섞어 새로운 palette mood를 만드는 것은 금지입니다.

## 구현 repo에서 쓰는 법

프리셋 설치:

```bash
uv run design-ontology install-preset \
  --preset-id conversation-copilot--corporate-trust \
  --target-repo /path/to/implementation-repo \
  --adapter raw-css-variables \
  --color-mode light \
  --locale ko
```

에이전트 팩 설치:

```bash
uv run design-ontology init-agent-pack \
  --target-repo /path/to/implementation-repo \
  --artifact-dir design-system \
  --targets codex,claude
```

작업 프롬프트:

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

## 유지보수 규칙

반복 가능한 실패가 나오면 현재 화면만 고치지 않습니다.

1. ontology governance에 규칙을 추가합니다.
2. `IMPLEMENTATION_CONTRACT.md`에 반영합니다.
3. Style Capsule 렌더러에 반영합니다.
4. 가능하면 `lint-implementation` 룰로 승격합니다.
5. 테스트를 추가합니다.

이 원칙 때문에 Style Capsule은 단순 문서가 아니라 feedback promotion 경로의 일부입니다.
