# EKOS Static Prototype Implementation Plan

Status: implementation planning document
Primary project: `design-ontology-harness`
Reference repositories: `2000silpeed/north-star`, `2000silpeed/ekos-sap-knowledge-os`
Snapshot date: 2026-07-08

This document defines where and how to build the first EKOS static UI prototype
inside `design-ontology-harness`.

It does not implement the prototype, modify the EKOS backend, connect to live
SAP, create a chatbot UI, make RAG the core, or claim production readiness.

## 1. Executive Summary

The first EKOS UI prototype should demonstrate the main governed workflow
journey:

```text
Workflow selection
-> source package validation
-> missing data resolution
-> decision report
-> evidence/policy trace
-> review request
```

The prototype should be static and artifact-backed. It should use fixture JSON
derived from existing EKOS outputs rather than a live backend.

The UI should use the existing `design-ontology-harness` structure and
patterns:

- operational app shell;
- dashboard/data-review layout;
- source cards;
- status badges;
- exception queue;
- decision record card;
- evidence trace;
- audit timeline;
- approval rail;
- design tokens installed from a harness preset.

The main EKOS product surface is source package status and governed decision
boundary. It should not open as a chat interface.

## 2. Existing Harness Inventory

### App / Framework Structure

`design-ontology-harness` is primarily a Python package and design-system
generation harness. The root package lives under:

```text
design_ontology_harness/
```

Important modules include:

- `cli.py`
- `scaffold.py`
- `synthesis.py`
- `authoring.py`
- `component_specs.py`
- `advanced_components.py`
- `preset_builder.py`
- `preset_installer.py`
- `implementation_linter.py`
- `graph_schema.py`
- `graph_builders.py`

The repository also contains self-contained prototype projects under:

```text
projects/
```

Existing examples include:

- `projects/faircite-harness-console/`
- `projects/agent-org-network/`
- `projects/omnigen-crm-demo/`
- `projects/world-cup-hub/`
- `projects/seoul-alley-mood-map/`

Most current prototypes are static HTML projects with local CSS and optional
small JavaScript files. Some project subdirectories use Next.js, but the common
static prototype convention is a self-contained folder under `projects/`.

### Routing Or Page Structure

The common static pattern is:

```text
projects/<project-name>/
  index.html
  styles.css
  app.js
```

or:

```text
projects/<project-name>/
  mockup/index.html
```

`projects/faircite-harness-console/` is the best implementation reference for
EKOS because it has:

- `index.html`;
- `styles.css`;
- `app.js`;
- `design-system/tokens.css`;
- `design-system/fonts.css`;
- local assets;
- a README with preview and lint commands.

The current routing style is single-page static navigation using buttons and
`data-*` attributes, not a routed application framework.

### Design Token Location

Installed design-system tokens appear in:

```text
projects/<project-name>/design-system/tokens.css
```

Example token roles seen in installed projects include:

- `--ds-color-canvas`
- `--ds-color-surface`
- `--ds-color-surface-muted`
- `--ds-color-surface-elevated`
- `--ds-color-border`
- `--ds-color-border-strong`
- `--ds-color-ink`
- `--ds-color-ink-muted`
- `--ds-color-primary`
- `--ds-color-success`
- `--ds-color-warning`
- `--ds-color-danger`
- `--ds-radius-sm`
- `--ds-radius-md`
- `--ds-radius-lg`

The prototype should consume tokens from `design-system/tokens.css`, not invent
a disconnected visual system.

### Component Location

Generated component contracts live under installed design-system folders:

```text
projects/<project-name>/design-system/component_inventory.json
projects/<project-name>/design-system/components/component_specs.md
projects/<project-name>/design-system/DESIGN.md
projects/<project-name>/design-system/STYLE.md
projects/<project-name>/design-system/IMPLEMENTATION_CONTRACT.md
```

The reusable component language is generated from preset artifacts under:

```text
presets/<preset-id>/
```

For EKOS, the most relevant preset is:

```text
presets/dashboard--corporate-trust/
```

Secondary reference:

```text
presets/monitoring-ops--corporate-trust/
```

### Layout Primitives

Relevant layout patterns already exist in the harness examples:

- app shell;
- sidebar navigation;
- topbar;
- status strip;
- dashboard grid;
- data review table;
- split workspace;
- inspector drawer;
- modal/dialog;
- review queue;
- audit log table.

EKOS should reuse these patterns with EKOS-specific content and state.

### Card / Panel Patterns

Useful existing patterns:

- metric cards;
- status pills;
- source badges;
- evidence/source cards;
- document review surfaces;
- panel headers;
- work stacks;
- review cards;
- row-based tables;
- compact metadata strips.

EKOS should avoid a generic card wall. Repeated workflow cards are acceptable,
but the primary surface should be source package status, table/list state, and
decision boundary.

### Dashboard Patterns

The `dashboard--corporate-trust` preset is the best fit because it emphasizes:

- operational state;
- governance;
- source attribution;
- review queues;
- owner and trust state chips;
- audit logs;
- dense data review;
- non-color status encoding.

### Monitoring / Ops Patterns

`monitoring-ops--corporate-trust` is useful for:

- source cards;
- status badges;
- inspector drawers;
- confidence/risk summary;
- evidence graph;
- exception queue;
- saved view/filter patterns.

### Evidence Graph Or Audit Timeline Patterns

`design_ontology_harness/advanced_components.py` already defines advanced
component contracts relevant to EKOS:

- `source-card`
- `citation-drawer`
- `evidence-graph`
- `policy-matrix`
- `audit-timeline`
- `approval-rail`
- `risk-summary-card`
- `exception-queue`
- `decision-record-card`

These should be reused as design-system primitives. Evidence graph should not
be decorative. Use it only when relationships are clearer than a ledger/table.

### Styles / CSS / Tailwind Usage

The root project is Python-based. Static examples commonly use plain HTML, CSS,
and JavaScript. Some generated or installed projects consume:

```text
design-system/tokens.css
design-system/fonts.css
styles.css
app.js
```

The harness also includes an adapter for Next.js/Tailwind/shadcn:

```text
adapters/nextjs-tailwind-shadcn/
```

For the first EKOS prototype, the safer path is static HTML/CSS/JS in
`projects/`, following the existing static prototype convention. Next.js should
not be introduced until the static flow is accepted.

### Build / Run Commands

The root CLI is available through:

```bash
uv run design-ontology --help
```

Common harness commands:

```bash
uv run design-ontology run-project --project-dir projects/<name>
uv run design-ontology build-preset --project projects/<name> --preset-id <id> ...
uv run design-ontology install-preset --preset-id <id> --target-repo projects/<name> --adapter raw-css-variables
uv run design-ontology lint-implementation --target-repo projects/<name>
```

Static preview convention:

```bash
cd projects/<name>
python3 -m http.server 4173 --bind 127.0.0.1
```

Repository validation commands:

```bash
uv run ruff check .
uv run --with pytest pytest tests/ -q
uv build
```

## 3. Recommended Prototype Location

Recommended location:

```text
projects/ekos-static-prototype/
```

Recommended future file layout:

```text
projects/ekos-static-prototype/
  README.md
  brand_profile.json
  spec.md
  project_manifest.json
  agent_brief.md
  seeds/seed_urls.txt
  design-system/
  fixtures/
    ekos-workflows.json
    ekos-source-package-failed.json
    ekos-source-package-passed.json
    ekos-decision-report-delivery-delay.json
    ekos-evidence-trace.json
  index.html
  styles.css
  app.js
```

Rationale:

- `projects/` is the existing convention for runnable harness projects.
- Static examples already use this structure.
- The prototype can consume installed design-system tokens.
- The project can later be promoted to a preset if useful.
- It keeps prototype implementation separate from root harness code.
- It avoids modifying EKOS backend code.

Why not `docs/prototypes/ekos/`:

- `docs/` is used for durable harness documentation.
- Runnable examples live under `projects/`.
- The requested plan belongs in `docs/`, but the future prototype should live
  in `projects/`.

## 4. Reusable Design System Assets

| Asset or pattern | EKOS use | Reuse / Extend / Avoid | Notes |
| --- | --- | --- | --- |
| `dashboard--corporate-trust` preset | Primary visual and component foundation | Reuse | Best match for governed operational workflow UI. |
| `monitoring-ops--corporate-trust` preset | Secondary ops/evidence reference | Extend | Useful for source status, evidence, risk, and inspector patterns. |
| App shell | Workflow navigation and case context | Reuse | Sidebar plus topbar fits workflow selection and trace navigation. |
| Dashboard layout | Source package status and operational panels | Reuse | Use data-first surfaces, not landing-page hero composition. |
| Trust/corporate visual theme | Enterprise credibility and governance tone | Reuse | Adapt to EKOS identity. Do not copy Agent Org Network branding. |
| Source cards | Missing source and evidence source display | Reuse | Map to EKOS source aliases and lineage. |
| Status badges | Source readiness, freshness, and governance states | Reuse | Must include text, not color alone. |
| Decision record card | Decision report summary | Reuse | Use for allowed/blocked action and packet identity. |
| Exception queue | Missing data resolution and blockers | Extend | Rename in UI as missing source queue or source gaps. |
| Evidence graph | Evidence/policy trace | Extend | Use only when relationships need graph display; otherwise use ledger/table. |
| Audit timeline | Review trail and provenance events | Reuse | Useful for review request and packet history. |
| Approval rail | Human review stage and reviewer action | Extend | Must make `review_required` distinct from approved. |
| Data review table | Source package status table | Reuse | Central screen for EKOS. |
| Token categories | EKOS status, risk, evidence, policy, governance tokens | Reuse | Add EKOS semantic aliases only through project CSS, not raw hard-coded colors. |
| Copilot/chat patterns | Optional context lookup side panel | Avoid as primary | Do not create a chat-first EKOS interface. |
| Decorative network graph | None | Avoid | Trace visuals must explain lineage, not decorate. |

## 5. EKOS-specific Components To Build

### WorkflowCard

Purpose:

Represent one governed business workflow.

Props/data needed:

- `workflow_id`
- `name`
- `description`
- `process_owner`
- `config_version`
- `required_aliases`
- `supported_action_boundary`
- `status`

Design-system primitives:

- data-display card;
- status badge;
- compact metadata rows;
- primary button.

Example state:

```text
Delivery Delay / Carrier Confirmation
status: configured
CTA: Start check
```

### CaseObjectHeader

Purpose:

Show the selected workflow and primary business object.

Props/data needed:

- `workflow_name`
- `case_object_type`
- `case_object_id`
- `case_status`
- `source_package_status`
- `governance_status`

Design-system primitives:

- app shell header;
- breadcrumb;
- status badge;
- metadata strip.

Example state:

```text
Delivery 80001241 / source package failed / review not started
```

### SourcePackageStatusPanel

Purpose:

Make required source readiness visually central.

Props/data needed:

- `workflow_id`
- `validation_result`
- `aliases[]`
- `missing_critical_aliases[]`
- `decision_packet_generated`
- `recommended_next_action`

Design-system primitives:

- data review table;
- inline alert;
- status badges;
- exception queue;
- disabled/enabled CTA.

Example state:

```text
carrier_updates: missing
approval_matrix: missing
final result: fail
Generate decision packet: disabled
```

### SourceAliasStatusRow

Purpose:

Represent one required source alias in the source package table.

Props/data needed:

- `alias`
- `readiness`
- `policy`
- `source_origin`
- `record_count`
- `owner`
- `last_updated_at`
- `passes`

Design-system primitives:

- data table row;
- status badge;
- source chip;
- row action.

Example state:

```text
policies / needs_manual_mapping / allowed / pass with warning
```

### MissingSourceCard

Purpose:

Explain why a missing source blocks evaluation and how to close the gap.

Props/data needed:

- `alias`
- `why_needed`
- `accepted_sources`
- `required_fields`
- `suggested_owner`
- `trust_level`
- `example_source_path`

Design-system primitives:

- source-card;
- inline alert;
- action row;
- form section.

Example state:

```text
carrier_updates missing because EKOS cannot determine whether carrier
confirmation is current.
```

### DecisionBoundaryCard

Purpose:

Show allowed action and blocked action in business language.

Props/data needed:

- `primary_object`
- `allowed_action_label`
- `blocked_action_label`
- `requested_action_label`
- `why_blocked`
- `blocking_risks[]`
- `governance_status`
- `required_next_actions[]`

Design-system primitives:

- decision-record-card;
- risk-summary-card;
- status badge;
- source/evidence links.

Example state:

```text
Allowed: Recommendation only
Blocked: Prepare approval-ready correction workflow
Status: review_required
```

### EvidenceSummaryCard

Purpose:

Summarize evidence used in the decision report.

Props/data needed:

- `evidence_id`
- `type`
- `summary`
- `freshness_state`
- `source_alias`
- `source_kind`
- `supports_or_blocks`
- `lineage`

Design-system primitives:

- source-card;
- evidence status badge;
- metadata row;
- trace link.

Example state:

```text
carrier_update_stale / stale / blocks approval-ready preparation
```

### PolicyAuthorityCard

Purpose:

Show policy, approval matrix, and authority boundary.

Props/data needed:

- `policy_ids[]`
- `policy_version`
- `sop_reference`
- `required_approver_role`
- `approval_matrix_version`
- `can_prepare`
- `can_execute`
- `authority_boundary`

Design-system primitives:

- policy-matrix;
- approval-rail;
- metadata table;
- inline alert.

Example state:

```text
delay_confirmation_policy requires current external confirmation before
approval-ready preparation.
```

### GovernanceStatusBadge

Purpose:

Display governance state without implying false approval.

Props/data needed:

- `status`
- `label`
- `meaning`
- `severity`

Design-system primitives:

- status-badge;
- icon plus text;
- accessible label.

Example state:

```text
review_required: This result is not an approval.
```

### TraceDrawer

Purpose:

Expose source-to-evidence lineage and packet provenance for advanced users.

Props/data needed:

- `source_records[]`
- `evidence_lineage[]`
- `blocking_risk_provenance[]`
- `packet_provenance`
- `config_path`
- `source_provider`

Design-system primitives:

- inspector drawer;
- citation drawer;
- audit timeline;
- evidence ledger/table.

Example state:

```text
carrier_update_stale came from supplemental carrier update source
CARRIER_PORTAL_EXPORT:CU-80001241-SUP-01.
```

### ReviewActionPanel

Purpose:

Route the packet to a human reviewer.

Props/data needed:

- `required_approver_role`
- `assigned_reviewer`
- `review_status`
- `available_actions[]`
- `review_note`
- `packet_id`

Design-system primitives:

- approval-rail;
- form section;
- action buttons;
- audit timeline.

Example state:

```text
No explicit review artifact available.
Action: Request human review.
Final status remains review_required.
```

## 6. Data Contract For Static Prototype

Use static JSON fixtures. Do not call the EKOS backend from the first
prototype.

Recommended fixture directory:

```text
projects/ekos-static-prototype/fixtures/
```

Recommended files:

```text
ekos-workflows.json
ekos-source-package-failed.json
ekos-source-package-passed.json
ekos-decision-report-delivery-delay.json
ekos-evidence-trace.json
```

### `ekos-workflows.json`

Purpose:

Drive Workflow Selection.

Minimum shape:

```json
{
  "workflows": [
    {
      "workflow_id": "delivery_delay_confirmation",
      "name": "Delivery Delay / Carrier Confirmation",
      "description": "Check whether EKOS can prepare a correction workflow packet.",
      "process_owner": "SAP logistics operations",
      "config_version": "delivery_delay_confirmation_source_package.yaml",
      "required_aliases": ["deliveries", "tracking_events", "carrier_updates", "policies", "approval_matrix"],
      "status": "configured"
    }
  ]
}
```

### `ekos-source-package-failed.json`

Purpose:

Show Check Mode when critical aliases are missing.

Base source:

- `out/ekos-source-package-validation-delivery-delay-r1/source_package_validation.json`
- `out/ekos-source-package-validation-delivery-delay-r1/source_package_validation_report.md`

Expected state:

```text
carrier_updates: missing
approval_matrix: missing
final result: fail
decision_packet_generated: false
```

### `ekos-source-package-passed.json`

Purpose:

Show Check Mode after supplemental sources are added.

Base source:

- `out/ekos-source-package-delivery-delay-r1/source_package.json`
- `out/ekos-source-package-delivery-delay-r1/source_package_readiness.json`
- `out/ekos-source-package-delivery-delay-r1/source_package_report.md`

Expected state:

```text
deliveries: partial accepted
tracking_events: partial accepted
policies: curated mapping
carrier_updates: ready
approval_matrix: ready
final result: pass
```

### `ekos-decision-report-delivery-delay.json`

Purpose:

Drive Decision Report and Review Request.

Base source:

- `out/ekos-configured-onboarding-delivery-delay-source-package-r1/decision_packet.json`
- `out/ekos-enterprise-workflow-from-source-package-r1/enterprise_workflow.json`
- `out/ekos-enterprise-workflow-from-source-package-r1/governance_decision_log.json`
- `out/ekos-enterprise-workflow-from-source-package-r1/human_readable_report.md`

Expected state:

```text
Primary object: Delivery 80001241
Allowed action: Recommendation only
Blocked action: Prepare approval-ready correction workflow
Governance status: review_required
Review status: not_available_for_synthetic_onboarding_demo
```

### `ekos-evidence-trace.json`

Purpose:

Drive Evidence / Policy Trace.

Base source:

- `out/ekos-configured-onboarding-delivery-delay-source-package-r1/evidence_objects.json`
- `decision_packet.evidence_lineage`
- `decision_packet.provenance`

Expected evidence:

- `delivery_status_event`
- `carrier_update_stale`
- `policy_confirmation_required`

The fixture should preserve source kind and provenance, including projected and
supplemental source usage.

## 7. Prototype Screens

### Screen 1: Workflow Selection

User goal:

Choose a governed EKOS workflow.

Visible content:

- workflow cards;
- required source package summary;
- workflow owner;
- config version;
- status badge.

Primary action:

```text
Start check
```

Secondary action:

```text
View required sources
```

Component composition:

- app shell;
- WorkflowCard;
- GovernanceStatusBadge;
- compact metadata rows.

Source data fixture:

- `ekos-workflows.json`

### Screen 2: Case Input

User goal:

Identify the case object before EKOS checks data availability.

Visible content:

- selected workflow;
- Delivery ID input;
- optional plant/carrier/date fields;
- copy explaining that EKOS checks required inputs before judgment.

Primary action:

```text
Check required data
```

Secondary action:

```text
Back to workflows
```

Component composition:

- CaseObjectHeader;
- form section;
- helper alert.

Source data fixture:

- `ekos-workflows.json`

### Screen 3A: Source Package Failed State

User goal:

Understand why EKOS cannot safely evaluate the case yet.

Visible content:

- source alias table;
- `carrier_updates` missing;
- `approval_matrix` missing;
- failed validation result;
- disabled Generate decision packet CTA.

Primary action:

```text
Add missing source
```

Secondary action:

```text
Export validation report
```

Component composition:

- SourcePackageStatusPanel;
- SourceAliasStatusRow;
- MissingSourceCard preview;
- inline alert.

Source data fixture:

- `ekos-source-package-failed.json`

### Screen 3B: Source Package Passed State

User goal:

Confirm that EKOS has enough input data to generate a decision packet.

Visible content:

- all required aliases present or accepted;
- projected vs supplemental source labels;
- warning list for partial records;
- Generate decision packet CTA enabled.

Primary action:

```text
Generate decision packet
```

Secondary action:

```text
View source package
```

Component composition:

- SourcePackageStatusPanel;
- SourceAliasStatusRow;
- status badges;
- source package summary.

Source data fixture:

- `ekos-source-package-passed.json`

### Screen 4: Missing Data Resolution

User goal:

Learn what missing data must be supplied and who should own it.

Visible content:

- Missing Source Card for `carrier_updates`;
- Missing Source Card for `approval_matrix`;
- accepted source types;
- required fields;
- suggested owner/steward;
- trust level;
- upload/connect placeholder action.

Primary action:

```text
Use supplemental source package
```

Secondary action:

```text
View required fields
```

Component composition:

- MissingSourceCard;
- source-card;
- exception queue;
- action panel.

Source data fixture:

- `ekos-source-package-failed.json`
- `ekos-source-package-passed.json`

### Screen 5: Decision Report

User goal:

Understand what EKOS allows, what EKOS blocks, and why.

Visible content:

- primary object Delivery 80001241;
- allowed action: Recommendation only;
- blocked action: Prepare approval-ready correction workflow;
- why blocked;
- active blocking risks;
- required next actions;
- governance status `review_required`.

Primary action:

```text
Request human review
```

Secondary action:

```text
Open evidence trace
```

Component composition:

- DecisionBoundaryCard;
- EvidenceSummaryCard;
- PolicyAuthorityCard;
- GovernanceStatusBadge.

Source data fixture:

- `ekos-decision-report-delivery-delay.json`
- `ekos-evidence-trace.json`

### Screen 6: Evidence / Policy Trace

User goal:

Inspect source-to-evidence lineage and policy/authority mapping.

Visible content:

- evidence table or cards;
- source records;
- lineage fields;
- policy IDs;
- config path;
- source provider;
- blocking risk provenance.

Primary action:

```text
Return to decision report
```

Secondary action:

```text
Copy packet ID
```

Component composition:

- TraceDrawer;
- EvidenceSummaryCard;
- PolicyAuthorityCard;
- audit timeline;
- source ledger/table.

Source data fixture:

- `ekos-evidence-trace.json`

### Screen 7: Review Request

User goal:

Route the packet to a human reviewer without fabricating approval.

Visible content:

- required approver role;
- review status;
- no compatible review artifact available;
- available actions;
- reviewer note field;
- audit trail preview.

Primary action:

```text
Request review
```

Secondary action:

```text
Request more data
```

Component composition:

- ReviewActionPanel;
- approval-rail;
- audit timeline;
- GovernanceStatusBadge.

Source data fixture:

- `ekos-decision-report-delivery-delay.json`

## 8. Interaction Flow

Clickable flow:

```text
Workflow card click
-> Case input
-> Check required data
-> Failed source package state
-> Add missing source
-> Passed source package state
-> Generate decision packet
-> Decision report
-> Open evidence trace
-> Request review
```

Implementation guidance for the static prototype:

- Use one HTML page with stateful panels and `data-screen` or `data-view`
  attributes.
- Store current prototype state in a small JavaScript object.
- Load fixtures with static import/fetch if served over `http.server`, or embed
  a minimal `window.EKOS_FIXTURES` object for a no-build first pass.
- Keep all primary controls functional enough to move through the journey.
- Do not create a chat composer as a primary surface.

## 9. Visual / UX Requirements

Required:

- business language first;
- no raw JSON by default;
- source package status visually central;
- blocked actions visually distinct from allowed actions;
- `review_required` must not look like approved;
- missing source state clear and actionable;
- audit trace as drill-down, not default manager view;
- RAG, if shown, appears only as optional context lookup;
- internal delegation numbers secondary to business labels;
- no autonomous execution CTA;
- status labels include visible text, not color alone.

Recommended first-viewport structure:

```text
App shell
Case/workflow header
Source package status or decision boundary
Next action panel
```

Avoid:

- chat-first UI;
- generic AI assistant hero;
- decorative graph backgrounds;
- copied Agent Org Network branding;
- copied Agent Org Network product copy;
- raw JSON as the manager-facing view;
- approval-looking styling for synthetic `review_required` state.

## 10. Implementation Phases

### Phase 1: Static Prototype With Hard-coded Fixture Data

Build `projects/ekos-static-prototype/` with static fixtures.

Scope:

- delivery-delay flow only;
- failed and passed source package states;
- decision report;
- evidence trace;
- review request.

### Phase 2: Prototype Reads Exported EKOS JSON Artifacts

Replace hand-shaped fixture data with copies or normalized exports from EKOS
output directories.

Source examples:

- `source_package.json`
- `source_package_readiness.json`
- `decision_packet.json`
- `evidence_objects.json`
- `enterprise_workflow.json`
- `governance_decision_log.json`

### Phase 3: Local Bridge To EKOS Generated Output Directory

Add a local-only bridge script that copies or normalizes EKOS output files into
`projects/ekos-static-prototype/fixtures/`.

Boundary:

- no live EKOS server;
- no SAP connection;
- no provider calls.

### Phase 4: Internal Analyst Tool With Uploads

Turn static missing-source placeholders into local upload controls.

Scope:

- controlled source upload;
- source package validation view;
- no production writes.

### Phase 5: Read-only SAP-connected Pilot

Only after product and data validation:

- read-only SAP extracts;
- governed policy/approval mapping;
- explicit IAM/security model;
- audit logs;
- no autonomous execution.

## 11. Build / Run Plan

### Install / Environment

The repository uses Python 3.12+ and `uv`.

Recommended setup:

```bash
uv sync --dev
```

`uv run ...` also resolves dependencies on demand.

### Harness CLI Check

```bash
uv run design-ontology --help
```

### Generate Harness Project Artifacts

After the EKOS project folder exists:

```bash
uv run design-ontology run-project --project-dir projects/ekos-static-prototype
```

### Install Design System Into Prototype

For the first static prototype, install a corporate trust dashboard preset into
the project:

```bash
uv run design-ontology install-preset \
  --preset-id dashboard--corporate-trust \
  --target-repo projects/ekos-static-prototype \
  --adapter raw-css-variables \
  --color-mode light \
  --locale ko
```

If the project needs a more operations-specific preset, compare with:

```bash
uv run design-ontology install-preset \
  --preset-id monitoring-ops--corporate-trust \
  --target-repo projects/ekos-static-prototype \
  --adapter raw-css-variables \
  --color-mode light \
  --locale ko
```

### View Prototype

```bash
cd projects/ekos-static-prototype
python3 -m http.server 4173 --bind 127.0.0.1
```

Open:

```text
http://127.0.0.1:4173/
```

### Lint / Test / Build

Repository-level checks:

```bash
uv run ruff check .
uv run --with pytest pytest tests/ -q
uv build
```

Prototype implementation lint after the prototype exists:

```bash
uv run design-ontology lint-implementation --target-repo projects/ekos-static-prototype
```

Optional browser validation after prototype implementation:

- desktop viewport;
- mobile viewport;
- check no horizontal overflow;
- check all primary buttons move to the expected screen;
- check `review_required` never renders as approved.

## 12. Risks And Boundaries

Boundaries:

- no backend integration yet;
- no production readiness;
- no live SAP;
- no autonomous approval;
- static data only;
- no provider calls;
- no RAG core;
- no chatbot-first UI.

Risks:

- design-system reuse may require adaptation because the harness presets were
  created for other sample products;
- dashboard density could overwhelm SAP operations users if source package
  status is not prioritized;
- evidence graph could become decorative unless paired with a table/ledger
  fallback;
- static fixture data may drift from EKOS output schema;
- copying Agent Org Network examples too closely would create the wrong EKOS
  identity;
- making `review_required` visually too positive could imply false approval.

Mitigations:

- keep business labels first;
- use source package status as the central screen;
- use actual EKOS output keys when shaping fixtures;
- keep provenance and raw JSON in drill-down only;
- run `lint-implementation` after the prototype exists;
- review against North Star claim boundaries before sharing.

## 13. Recommended Next Codex Task

Implement the static EKOS prototype screens using static fixtures, following
this plan.

Recommended prompt:

```text
Implement projects/ekos-static-prototype as a static HTML/CSS/JS prototype
using design-ontology-harness patterns and fixture JSON. Cover workflow
selection, case input, source package failed state, missing data resolution,
source package passed state, decision report, evidence/policy trace, and review
request. Do not modify EKOS backend. Do not create a chat-first UI.
```

Validation for that task:

- run `uv run design-ontology lint-implementation --target-repo projects/ekos-static-prototype`;
- run `uv run ruff check .`;
- run `uv run --with pytest pytest tests/ -q`;
- serve locally with `python3 -m http.server`;
- verify the clickable flow manually;
- verify no approval is fabricated.
