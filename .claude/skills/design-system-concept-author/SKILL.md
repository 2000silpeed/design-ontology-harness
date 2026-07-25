---
name: design-system-concept-author
description: 하네스 합성 전에 앱 컨셉, 레이아웃 스켈레톤, 차별화 전략을 LLM이 직접 작성합니다. generated apps가 비슷하게 나올 때, preset 선택이 아니라 제품 컨셉과 화면 뼈대 기준으로 디자인 시스템을 다시 쓰고 싶을 때 사용하세요.
allowed-tools: Read Glob Grep Bash Edit Write
paths:
  - "projects/**"
  - "agent-team/**"
  - "brand_profile.json"
  - "spec.md"
  - "README.md"
---

# Design System Concept Author

Use this skill before `design-ontology run-project`.

Your job is not to choose a preset. Your job is to author the product-specific decisions that the harness will synthesize:

1. `application_concept`
2. `layout_skeleton`
3. `design_differentiation`
4. supporting `product_primitives`, `visual_keywords`, and `interaction_keywords`

## Required inputs

Read the user's brief, then read these files when present:

- `projects/<name>/spec.md`
- `projects/<name>/brand_profile.json`
- `agent-team/brand_profile.json`
- local screenshots, mockups, or visual reference notes supplied by the user

## Workflow

1. Identify the real first job of the product.
2. Name the domain objects users inspect, create, compare, approve, move, buy, publish, or monitor.
3. Define the success moment as a visible workflow state.
4. Author a custom layout skeleton. Do not limit `composition` to a fixed enum.
5. Write a concrete first-screen contract that an implementation can pass or fail.
6. Add structural signature moves that make this app different from a generic dashboard or card wall.
7. Patch `brand_profile.json`.
8. Run or recommend:

```bash
uv run design-ontology run-project --project-dir projects/<name> --kb-dir kb/default
```

## Field contract

```json
{
  "application_concept": {
    "primary_job": "",
    "domain_objects": [],
    "operating_mode": "",
    "success_moment": "",
    "differentiation": []
  },
  "layout_skeleton": {
    "composition": "",
    "navigation_model": "",
    "density": "",
    "primary_regions": [
      {"name": "", "role": "", "priority": "primary"}
    ],
    "first_screen_contract": [],
    "avoid_layouts": []
  },
  "design_differentiation": {
    "must_feel_different_from": [],
    "signature_moves": [],
    "repetition_risks": []
  }
}
```

## Judgment rules

- Do not solve sameness with colors, gradients, shadows, or more component variants.
- Do not make every product a dashboard. Dashboard is valid only when monitoring metrics is the first job.
- Do not open with a marketing hero unless the product is a landing page.
- Use Astryx and Geist only as component taxonomy and state-coverage references, not as identity or layout sources.
- Prefer concrete screen grammar over adjectives.
- If two unrelated products could share the same first viewport, the skeleton is too generic.
