# EKOS Static Prototype

This prototype demonstrates the first EKOS governed workflow UI using static fixture data.

It is not a chatbot. The main surface is source package status and the governed decision boundary:

Workflow selection -> case input -> source package status -> missing data resolution -> decision report -> evidence trace -> review request.

## Preview

```bash
cd projects/ekos-static-prototype
python3 -m http.server 4173 --bind 127.0.0.1
```

Open:

```text
http://127.0.0.1:4173/
```

The local server is required because the prototype loads JSON fixtures with `fetch`.

## Design System

The prototype uses the local `dashboard--corporate-trust` preset installed through Design Ontology:

```bash
uv run design-ontology install-preset \
  --preset-id dashboard--corporate-trust \
  --target-repo projects/ekos-static-prototype \
  --adapter raw-css-variables \
  --color-mode light \
  --locale ko
```

The implementation consumes tokens from `design-system/tokens.css`. It adapts the dashboard and monitoring operations patterns for EKOS workflow cards, source package status, evidence trace, audit rail, and review actions.

## Screens

- Workflow Selection
- Case Input
- Source Package Failed State
- Missing Data Resolution
- Source Package Passed State
- Decision Report
- Evidence / Policy Trace
- Review Request

## Fixtures

Static data lives in `fixtures/`:

- `workflows.json`
- `source-package-failed.json`
- `source-package-passed.json`
- `decision-report-delivery-delay.json`
- `evidence-trace-delivery-delay.json`
- `review-request.json`

The content is based on EKOS output concepts: source package validation, source package readiness, decision packets, evidence objects, and human-readable governance reports.

## Claim Boundaries

- Static prototype only.
- No EKOS backend integration.
- No live SAP integration.
- No production approval.
- No autonomous execution.
- No provider calls.
- No human validation claim.
- RAG is not the core decision authority.
- Raw JSON is intentionally not shown by default.

## Validation

From the repository root:

```bash
uv run design-ontology lint-implementation --target-repo projects/ekos-static-prototype
uv build
uv run --with pytest pytest tests/ -q
git diff --check
```
