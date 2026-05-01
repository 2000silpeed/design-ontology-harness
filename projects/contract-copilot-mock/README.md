# Contract Copilot Mock

End-to-end smoke mockup for `conversation-copilot--corporate-trust`.

The current visual direction keeps the original contract review product model and the installed
ontology tokens as the source of truth. External references are only used for component morphology:
dense rectangular cards, a fixed workspace rail, compact KPI rhythm, and chart-card proportions.
Color, typography, surface, radius, and semantic states are bound to `design-system/tokens.css`.

Before further UI edits, read:

1. `design-system/IMPLEMENTATION_CONTRACT.md`
2. `design-system/STYLE.md` or `design-system/DESIGN.md`
3. `design-system/token_schema.json`
4. `design-system/components/component_specs.md`

Reference images are allowed to influence morphology and density only. Do not copy their palette,
font scale, navigation labels, IA, or content model.

## Run

```bash
python3 -m http.server 8031
```

Open `http://127.0.0.1:8031/`.

## Screenshots

- `screenshots/ontology-redo-desktop.png`
- `screenshots/ontology-redo-mobile.png`
- `screenshots/ontology-bound-desktop.png`
- `screenshots/ontology-bound-mobile.png`

## Design System

The design system was installed with:

```bash
uv run design-ontology install-preset \
  --preset-id conversation-copilot--corporate-trust \
  --target-repo projects/contract-copilot-mock \
  --adapter raw-css-variables \
  --color-mode light \
  --locale ko \
  --force
```

Pretendard is fetched at runtime:

```bash
node design-system/fonts/fetch-pretendard.mjs
```

## Agent Prompt

```text
design-system/IMPLEMENTATION_CONTRACT.md,
design-system/STYLE.md,
design-system/token_schema.json,
design-system/components/component_specs.md 기준으로 이 mock을 리팩해줘.

외부 참고 이미지는 형태, 밀도, 컴포넌트 비례만 반영하고
색상, 폰트, IA, 카피는 온톨로지와 토큰을 우선해.
작업 후 lint-implementation까지 돌려줘.
```

```bash
uv run design-ontology lint-implementation --target-repo projects/contract-copilot-mock
```
