# Contextual Interaction Pattern Resolution

## 목적

하네스는 하나의 고정된 시각 템플릿을 모든 프로젝트에 적용하지 않는다.
제품 의미, 컴포넌트 상태, 브랜드 컨텍스트, 접근성 목표, 밀도, motion budget을
사용해 여러 `InteractionPattern` 후보를 만들고 그중 적합한 조합을 선택한다.

```text
request intent
→ component states
→ compatible candidates
→ accessibility / motion / density constraints
→ contextual variation
→ implementation binding
→ audit evidence
```

## 선택 방식

`design_ontology_harness.interaction_resolver.resolve_interaction_patterns()`가
다음 계약을 반환한다.

- `selection_mode`: `contextual-variation`
- `selected`: 현재 구현에 사용할 후보
- `candidates_considered`: 조건을 통과한 후보와 점수
- `rejected`: 상태·컴포넌트·motion budget 때문에 제외된 후보
- `constraints`: 접근성·밀도·motion·reference policy
- `variation_seed`: 선택 재현이 필요한 경우에만 지정

seed가 없으면 실행마다 후보 동률 해소가 달라질 수 있다. seed가 있으면 같은
입력에 대해 재현된다. 어느 경우에도 부적합 후보를 선택하지 않는다.

## 전역 규칙

1. 제품 brief와 component contract가 외부 레퍼런스보다 우선한다.
2. 외부 motion reference는 `advisory-only`다.
3. `reduced-motion` 목표가 있으면 static 또는 opacity-only fallback을 우선한다.
4. motion budget을 초과하는 후보는 선택하지 않는다.
5. 패턴 선택은 컴포넌트와 상태가 실제로 일치해야 한다.
6. 선택 결과와 탈락 사유를 `interaction_selection.json`으로 남긴다.
7. 구현은 선택 결과를 `data-interaction`에 연결하고, 컴포넌트는
   `data-component`와 `data-state`로 contract를 드러낸다.
8. 무작위성은 미감의 근거가 아니라 동등 후보 사이의 다양성 확보에만 사용한다.

## 프로젝트 연결

`run-project` 실행 시 blueprint에 다음 산출물이 생성된다.

```text
build/system/blueprint/interaction_selection.json
```

preview 또는 실제 구현은 이 파일을 읽어 현재 선택된 패턴을 연결할 수 있다.
Memory Garden preview는 다음처럼 사용한다.

```html
<main data-system="memory-garden">
  <section data-component="living-timeline" data-state="focused">
```

그리고 build 결과의 selected pattern ID를 `data-interaction`에 주입한다.
따라서 다음 프로젝트는 같은 resolver를 사용하되, 자기 brand profile과
component contract에 따라 다른 후보 조합을 얻는다.

## 검증

```bash
uv run pytest -q tests/test_interaction_resolver.py
uv run design-ontology run-project \
  --project-dir projects/memory-garden \
  --kb-dir projects/memory-garden/build/kb
python3 -m json.tool \
  projects/memory-garden/build/system/blueprint/interaction_selection.json
```
