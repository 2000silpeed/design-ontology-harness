# Component runtime conformance

Component contracts are not production evidence by themselves. A production
claim must bind every complete component contract to current runtime source,
explicit DOM markers, and hashed scenario evidence.

`verify-production-ui` reads the manifest at:

```text
<project>/build/system/production/component-runtime-manifest.json
```

The gate is fail-closed. A missing manifest, stale evidence, an unknown schema,
or incomplete component coverage fails `component_runtime_conformance`.

## Manifest v1

The current schema is `component-runtime-manifest/v1`:

```json
{
  "schema_version": "component-runtime-manifest/v1",
  "production_claim": true,
  "legacy_policy": "fail-closed",
  "implementation_tree_sha256": "<current sha256-runtime-tree-v1 digest>",
  "checked_at": "2026-07-13T16:45:12.123456+00:00",
  "components": [
    {
      "component_id": "evidence-review",
      "source_paths": [
        {"path": "src/EvidenceReview.tsx", "sha256": "<source sha256>"}
      ],
      "component_marker": {
        "source_path": "src/EvidenceReview.tsx",
        "attribute": "data-component-id",
        "value": "evidence-review"
      },
      "part_markers": [
        {
          "part": "root",
          "source_path": "src/EvidenceReview.tsx",
          "attribute": "data-component-part",
          "value": "root"
        }
      ],
      "evidence": {
        "path": "build/system/production/component-runtime/evidence-review.json",
        "sha256": "<evidence sha256>"
      }
    }
  ]
}
```

The component set must exactly match the complete contracts in
`build/system/components/component_specs.json`. Every source path is relative
to the implementation repository, content-hashed, and restricted to runtime
component source formats. Markers must appear in source as exact quoted
attributes. CSS classes and visual similarity are not accepted as component
identity. A source file excluded from the current runtime implementation tree,
including a file placed under `build/system`, cannot serve as component source
evidence.

Each contract anatomy part must use an explicit marker:

```html
<section data-component-id="evidence-review" data-component-part="root">
  <ul data-component-part="evidence-list"></ul>
</section>
```

## Evidence v1

Each manifest component references one hashed
`component-runtime-evidence/v1` artifact under
`build/system/production/component-runtime/`. The artifact must contain:

- the same component and anatomy DOM markers as the manifest;
- one passing state scenario for every `state_model.all_states` value, with an
  observed `data-component-state` marker;
- passing interaction and focus assertions for every declared event, plus
  exact coverage of every declared state transition;
- passing responsive scenarios for every required width, with exact coverage
  of the component's control rules and container behavior;
- explicit coverage of props, data fields, content rules, accessibility rules,
  do/don't rules, variant axes, and the default variant;
- observed provenance and empty-state behavior when the component contract
  requires them;
- the current runtime implementation-tree digest and a timezone-aware
  `checked_at` timestamp.

Both the timestamp and evidence file modification time must be newer than the
latest runtime source. Any runtime change therefore invalidates the evidence
until the component scenarios are rerun and the manifest is regenerated.

Scenario assertions use non-empty records with stable IDs:

```json
{
  "scenario_id": "responsive-390",
  "width_px": 390,
  "covered_rules": ["Keep the primary action in document flow."],
  "container_behavior": "Reflow the side rail into one column.",
  "assertions": [
    {"id": "no-component-overflow", "passed": true}
  ]
}
```

### Minimum static HTML example

For a small static implementation, the runtime source still needs component,
part, and current-state markers. For example:

```html
<article
  data-component-id="match-card"
  data-component-part="root"
  data-component-state="scheduled"
>
  <h2 data-component-part="fixture-heading">Korea Republic vs Mexico</h2>
</article>
```

If its contract has one `scheduled` state, one `open-match` event, one 390px
responsive target, and no state transition, the smallest corresponding
evidence artifact has this shape:

```json
{
  "schema_version": "component-runtime-evidence/v1",
  "component_id": "match-card",
  "implementation_tree_sha256": "<current sha256-runtime-tree-v1 digest>",
  "checked_at": "2026-07-13T16:45:12.123456+00:00",
  "dom": {
    "component_marker": {
      "source_path": "index.html",
      "attribute": "data-component-id",
      "value": "match-card"
    },
    "part_markers": [
      {
        "part": "root",
        "source_path": "index.html",
        "attribute": "data-component-part",
        "value": "root"
      },
      {
        "part": "fixture-heading",
        "source_path": "index.html",
        "attribute": "data-component-part",
        "value": "fixture-heading"
      }
    ]
  },
  "state_scenarios": [
    {
      "scenario_id": "match-card-scheduled",
      "state": "scheduled",
      "route": "/schedule",
      "observed_marker": {
        "attribute": "data-component-state",
        "value": "scheduled"
      },
      "assertions": [{"id": "scheduled-state-visible", "passed": true}]
    }
  ],
  "interaction_scenarios": [
    {
      "scenario_id": "match-card-open",
      "event": "open-match",
      "route": "/schedule",
      "assertions": [{"id": "detail-opened", "passed": true}],
      "focus_assertions": [{"id": "focus-remains-visible", "passed": true}]
    }
  ],
  "responsive_scenarios": [
    {
      "scenario_id": "match-card-390",
      "width_px": 390,
      "covered_rules": ["Keep both team names visible."],
      "container_behavior": "Stack metadata below the fixture heading.",
      "assertions": [{"id": "no-card-overflow", "passed": true}]
    }
  ],
  "contract_coverage": {
    "props": ["match"],
    "data_fields": ["match_id", "home_team", "away_team"],
    "content_rules": ["Show the kickoff timezone."],
    "accessibility_rules": ["Use a descriptive accessible name."],
    "do_rules": ["Keep status beside the fixture."],
    "dont_rules": ["Do not use color as the only status cue."],
    "variant_axes": ["state"],
    "default_variant": "scheduled",
    "provenance_observed": true,
    "empty_state_observed": false
  }
}
```

This is only minimal for that hypothetical contract. Every additional anatomy
part, state, event, transition, width, rule, prop, or data field in the real
contract requires matching evidence; there are no wildcard coverage records.

Evidence should be emitted from the browser or component-test run that made the
observations. A manually written `passed: true` record satisfies the JSON shape
but is not an acceptable team review practice; production QA remains
responsible for checking the generating command and raw test artifacts.

## Legacy policy

`component-runtime-manifest/v0` is an explicit compatibility marker only:

```json
{
  "schema_version": "component-runtime-manifest/v0",
  "mode": "legacy-unverified",
  "production_eligible": false
}
```

Callers that are not making a production claim may validate missing or v0
evidence in legacy mode. The report remains `verified: false` and
`production_eligible: false`. `verify-production-ui` always makes a production
claim, so missing evidence and v0 manifests are blocking failures.

| Runtime evidence | Non-production compatibility check | `verify-production-ui` |
| --- | --- | --- |
| Missing | `ok: true`, `verified: false` | Fails |
| Explicit v0 `legacy-unverified` | `ok: true`, `verified: false` | Fails |
| Complete, current v1 | Verified | Eligible to pass this gate |
