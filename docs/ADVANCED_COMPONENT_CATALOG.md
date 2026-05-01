# Advanced Component Catalog

The baseline component analyzer answers: “what primitives are required?”
The advanced component catalog answers: “what professional structures could make this workflow stronger?”

It is intentionally ontology-led. Agents may use these components freely only when
the product context calls for them, and every component still follows the same
token, typography, accessibility, and reference-governance rules.

## Why It Exists

Users should not need to know component names like `policy-matrix`,
`citation-drawer`, or `resizable-split-pane` before the system can produce mature
interfaces. The harness now recommends advanced components from:

- `brand_profile.product_summary`
- `brand_profile.brand_keywords`
- `brand_profile.product_primitives`
- `brand_profile.visual_keywords`
- `brand_profile.interaction_keywords`
- `blueprint.component_strategy.product_primitives`
- existing component pairs

## Output Artifacts

Generated component inventory may include:

- `advanced_component_catalog`: compact menu of ontology-approved advanced components
- `advanced_recommendations`: ranked components for this preset/project context
- component entries marked with `advanced_component: true`
- `component_specs.*` sections with Advanced Usage guidance
- `STYLE.md` / `DESIGN.md` section: **Advanced Component Menu**

## Current Families

| Family | Examples |
| --- | --- |
| Layout | `resizable-split-pane` |
| Overlay | `command-palette`, `inspector-drawer` |
| Document | `diff-viewer`, `redline-viewer` |
| Copilot artifact | `citation-drawer`, `source-card` |
| Data display | `policy-matrix`, `audit-timeline`, `risk-summary-card`, `exception-queue`, `evidence-graph`, `decision-record-card` |
| Workflow | `approval-rail` |
| Input | `filter-builder`, `reviewer-assignment-picker` |
| Navigation | `saved-view-bar` |
| Feedback | `confidence-meter`, `retention-indicator` |
| Copilot chat | `tool-call-trace` |

## Agent Rule

Advanced components are not decoration. Use them when they improve real work:

- comparison
- review
- compliance
- evidence inspection
- auditability
- approval or handoff
- repeatable operational filters
- bulk triage
- AI traceability

Do not add them merely to make a screen look complex.

## Conversation Copilot Example

For `conversation-copilot--corporate-trust`, the catalog naturally recommends:

- `policy-matrix`
- `citation-drawer`
- `audit-timeline`
- `approval-rail`
- `risk-summary-card`
- `diff-viewer`
- `tool-call-trace`
- `decision-record-card`
- `reviewer-assignment-picker`

This lets a mock move beyond “chat + cards” into a real regulated workflow while
still keeping color, type, IA, copy, and status semantics bound to the ontology.
