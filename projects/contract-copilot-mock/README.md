# Contract Copilot Mock

End-to-end smoke mockup for `conversation-copilot--corporate-trust`.

The current visual direction keeps the original contract review product model and the installed
ontology tokens as the source of truth. External references are only used for component morphology:
dense rectangular cards, a fixed workspace rail, compact KPI rhythm, and chart-card proportions.
Color, typography, surface, radius, and semantic states are bound to `design-system/tokens.css`.

## Run

```bash
python3 -m http.server 8031
```

Open `http://127.0.0.1:8031/`.

## Screenshots

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
