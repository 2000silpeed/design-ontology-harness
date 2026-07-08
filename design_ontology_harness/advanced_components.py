"""Advanced component catalog and recommendation helpers.

The baseline analyzer is intentionally broad and safe. This catalog gives
implementation agents a richer menu of professional UI structures without
requiring the user to already know component names.
"""

from __future__ import annotations

from typing import Any


ADVANCED_COMPONENTS: dict[str, dict[str, Any]] = {
    "resizable-split-pane": {
        "family": "layout",
        "role": "Resizable two/three-pane workspace shell for dense tools",
        "use_when": [
            "primary work happens between list, canvas/chat, and detail panels",
            "users need to compare or inspect adjacent information without navigation",
        ],
        "avoid_when": ["single linear form or landing page is enough"],
        "pairs_with": ["thread-list", "artifact-preview-panel", "inspector-drawer"],
        "recommended_for": ["conversation-copilot", "dashboard", "canvas-tool", "monitoring-ops"],
        "keyword_triggers": ["workspace", "thread", "panel", "artifact", "inspector"],
        "primitive_triggers": ["thread list sidebar", "compliance-artifact panel", "workspace header"],
        "anatomy": {
            "parts": ["container", "pane", "resize-handle", "collapse-button(optional)", "keyboard-resize affordance"],
            "states": ["default", "resizing", "collapsed", "focus"],
        },
        "tokens": {
            "surface": "var(--color-canvas)",
            "pane-surface": "var(--color-surface)",
            "divider": "var(--color-border)",
            "handle-focus": "var(--color-brand-primary)",
            "radius": "var(--radius-lg)",
            "gap": "var(--space-16)",
        },
        "accessibility": [
            "resize handle uses role=\"separator\" with aria-orientation",
            "aria-valuemin / aria-valuemax / aria-valuenow describe pane size",
            "Arrow keys resize focused handle; Enter toggles collapsed state",
        ],
    },
    "command-palette": {
        "family": "overlay",
        "role": "Keyboard-first command launcher and cross-surface search",
        "use_when": [
            "the product has many actions or navigation targets",
            "expert users benefit from quick action search",
        ],
        "avoid_when": ["there are fewer than five meaningful commands"],
        "pairs_with": ["shortcut-hint", "saved-view-bar", "filter-builder"],
        "recommended_for": ["conversation-copilot", "dashboard", "canvas-tool", "monitoring-ops"],
        "keyword_triggers": ["command", "shortcut", "quick action", "search", "keyboard"],
        "primitive_triggers": ["project switcher", "reviewer assignment chip"],
        "anatomy": {
            "parts": ["backdrop", "dialog", "search-input", "result-list", "result-item", "shortcut-hint"],
            "states": ["closed", "open", "loading", "empty", "keyboard-active"],
        },
        "tokens": {
            "surface": "var(--color-surface-elevated)",
            "backdrop": "color-mix(in srgb, var(--color-text) 45%, transparent)",
            "border": "var(--color-border)",
            "selected-surface": "var(--color-surface-tint)",
            "radius": "var(--radius-lg)",
            "elevation": "var(--elevation-lg)",
        },
        "accessibility": [
            "role=\"dialog\" with aria-modal=\"true\"",
            "combobox input controls listbox results",
            "Escape closes and restores focus to trigger",
        ],
    },
    "inspector-drawer": {
        "family": "overlay",
        "role": "Contextual detail drawer for properties, policy facts, or record metadata",
        "use_when": [
            "a selected item needs rich detail without leaving the main workflow",
            "users need source facts, owners, versions, or retention metadata",
        ],
        "avoid_when": ["the detail is short enough for an inline disclosure"],
        "pairs_with": ["policy-matrix", "citation-drawer", "decision-record-card"],
        "recommended_for": ["conversation-copilot", "dashboard", "canvas-tool", "monitoring-ops"],
        "keyword_triggers": ["detail", "metadata", "drawer", "inspect", "retention", "record"],
        "primitive_triggers": ["data retention indicator", "source reference card", "policy-check badge"],
        "anatomy": {
            "parts": ["drawer", "header", "section-list", "property-row", "action-row", "close-button"],
            "states": ["closed", "open", "loading", "dirty"],
        },
        "tokens": {
            "surface": "var(--color-surface-elevated)",
            "border": "var(--color-border)",
            "section-surface": "var(--color-surface-muted)",
            "radius": "var(--radius-lg)",
            "padding": "var(--space-24)",
        },
        "accessibility": [
            "role=\"dialog\" or complementary region depending on modality",
            "aria-labelledby connects drawer title",
            "focus moves into drawer when modal and returns to trigger on close",
        ],
    },
    "diff-viewer": {
        "family": "document",
        "role": "Before/after document comparison with inline additions and removals",
        "use_when": [
            "AI rewrites, policy edits, or reviewer changes need auditability",
            "users must approve what changed before publishing",
        ],
        "avoid_when": ["only a short status message changed"],
        "pairs_with": ["redline-viewer", "revision-timeline", "approval-rail"],
        "recommended_for": ["conversation-copilot", "document-content"],
        "keyword_triggers": ["diff", "revision", "redline", "rewrite", "approve", "draft"],
        "primitive_triggers": ["compliance-artifact panel", "audit-trail timeline", "citation footnote"],
        "anatomy": {
            "parts": ["container", "version-header", "line-list", "change-marker", "gutter", "summary-footer"],
            "states": ["default", "side-by-side", "inline", "collapsed-context"],
        },
        "tokens": {
            "surface": "var(--color-surface)",
            "border": "var(--color-border)",
            "added": "var(--color-success)",
            "removed": "var(--color-danger)",
            "muted-surface": "var(--color-surface-muted)",
            "font": "var(--font-body)",
            "mono": "var(--font-mono)",
        },
        "accessibility": [
            "changes are announced with text labels, not color alone",
            "line numbers are decorative unless referenced by controls",
            "keyboard shortcuts have visible command alternatives",
        ],
    },
    "redline-viewer": {
        "family": "document",
        "role": "Review-oriented prose surface with suggested insertions, deletions, and comments",
        "use_when": [
            "legal, compliance, or editorial text needs reviewer markup",
            "comments must stay anchored to exact text ranges",
        ],
        "avoid_when": ["structured rows are more important than prose"],
        "pairs_with": ["diff-viewer", "comment-thread", "approval-rail"],
        "recommended_for": ["conversation-copilot", "document-content"],
        "keyword_triggers": ["redline", "comment", "review", "legal", "policy"],
        "primitive_triggers": ["compliance-artifact panel", "reviewer assignment chip"],
        "anatomy": {
            "parts": ["reading-pane", "marked-text", "comment-anchor", "comment-margin", "resolve-action"],
            "states": ["default", "selected", "commenting", "resolved"],
        },
        "tokens": {
            "surface": "var(--color-surface)",
            "mark-surface": "var(--color-surface-tint)",
            "comment-border": "var(--color-border)",
            "accent": "var(--color-brand-accent)",
            "radius": "var(--radius-md)",
        },
        "accessibility": [
            "marked ranges expose aria-describedby to comment text",
            "resolved comments remain reachable from audit history",
            "keyboard can move between comment anchors",
        ],
    },
    "citation-drawer": {
        "family": "copilot-artifact",
        "role": "Source and citation drawer for AI answers, policies, and quoted evidence",
        "use_when": [
            "answers must show supporting policy, document, or source records",
            "users need to inspect evidence without losing conversation context",
        ],
        "avoid_when": ["citations are static footnotes only"],
        "pairs_with": ["inline-citation", "source-card", "evidence-graph"],
        "recommended_for": ["conversation-copilot", "document-content"],
        "keyword_triggers": ["citation", "source", "evidence", "policy", "grounding"],
        "primitive_triggers": ["citation footnote", "source reference card", "policy-check badge"],
        "anatomy": {
            "parts": ["drawer", "source-list", "source-card", "quote-snippet", "metadata-row", "open-source-action"],
            "states": ["closed", "open", "loading", "empty", "verified"],
        },
        "tokens": {
            "surface": "var(--color-surface-elevated)",
            "source-surface": "var(--color-surface)",
            "border": "var(--color-border)",
            "verified": "var(--color-success)",
            "radius": "var(--radius-lg)",
        },
        "accessibility": [
            "each citation has a stable label and source title",
            "snippets are summaries unless licensing permits direct quote",
            "drawer focus order follows source ranking",
        ],
    },
    "evidence-graph": {
        "family": "data-display",
        "role": "Node-link evidence map connecting claims, sources, policies, and decisions",
        "use_when": [
            "trust depends on seeing relationships between claims and sources",
            "auditors need to trace why an answer or decision was made",
        ],
        "avoid_when": ["a simple source list communicates the relationship"],
        "pairs_with": ["citation-drawer", "decision-record-card", "policy-matrix"],
        "recommended_for": ["conversation-copilot", "monitoring-ops"],
        "keyword_triggers": ["evidence", "graph", "trace", "audit", "decision"],
        "primitive_triggers": ["source reference card", "audit-trail timeline"],
        "anatomy": {
            "parts": ["graph-canvas", "node", "edge", "legend", "selection-detail", "zoom-control"],
            "states": ["default", "focused", "filtered", "empty"],
        },
        "tokens": {
            "surface": "var(--color-surface)",
            "node-surface": "var(--color-surface-muted)",
            "edge": "var(--color-border-strong)",
            "active": "var(--color-brand-primary)",
            "radius": "var(--radius-md)",
        },
        "accessibility": [
            "graph has a table/list fallback with the same relationships",
            "selected node detail is announced in a live region",
            "zoom controls are buttons with visible labels",
        ],
    },
    "policy-matrix": {
        "family": "data-display",
        "role": "Policy requirement by answer/field matrix with pass, warning, and exception states",
        "use_when": [
            "multiple policy rules must be checked against multiple claims or fields",
            "reviewers need dense scan-and-drill compliance status",
        ],
        "avoid_when": ["there is only one policy outcome"],
        "pairs_with": ["risk-summary-card", "exception-queue", "approval-rail"],
        "recommended_for": ["conversation-copilot", "dashboard", "monitoring-ops"],
        "keyword_triggers": ["policy", "compliance", "matrix", "rule", "requirement"],
        "primitive_triggers": ["policy-check badge", "compliance warning modal", "compliance-artifact panel"],
        "anatomy": {
            "parts": ["table", "rule-column", "target-column", "status-cell", "evidence-link", "row-action"],
            "states": ["default", "filtered", "sorted", "exception", "empty"],
        },
        "tokens": {
            "surface": "var(--color-surface)",
            "border": "var(--color-border)",
            "pass": "var(--color-success)",
            "warning": "var(--color-warning)",
            "danger": "var(--color-danger)",
            "font": "var(--font-body)",
        },
        "accessibility": [
            "caption describes policy scope",
            "table headers use scope for rows and columns",
            "status cells include text labels in addition to icons or color",
        ],
    },
    "audit-timeline": {
        "family": "data-display",
        "role": "Chronological audit trail with actor, action, timestamp, and linked artifact",
        "use_when": [
            "regulated workflows require traceable user and AI actions",
            "reviewers need to reconstruct what happened before approval",
        ],
        "avoid_when": ["events are not user-facing or not actionable"],
        "pairs_with": ["decision-record-card", "approval-rail", "tool-call-trace"],
        "recommended_for": ["conversation-copilot", "monitoring-ops", "dashboard"],
        "keyword_triggers": ["audit", "timeline", "history", "trace", "retention"],
        "primitive_triggers": ["audit-trail timeline", "data retention indicator"],
        "anatomy": {
            "parts": ["list", "event-item", "timestamp", "actor", "event-summary", "artifact-link"],
            "states": ["default", "filtered", "expanded", "empty"],
        },
        "tokens": {
            "surface": "var(--color-surface)",
            "border": "var(--color-border)",
            "timestamp": "var(--color-brand-primary)",
            "muted": "var(--color-text-muted)",
            "mono": "var(--font-mono)",
        },
        "accessibility": [
            "timeline is an ordered list when chronology matters",
            "timestamps use machine-readable datetime when possible",
            "expanded details are reachable by keyboard",
        ],
    },
    "approval-rail": {
        "family": "workflow",
        "role": "Persistent approval state rail with owners, blockers, and next action",
        "use_when": [
            "work requires review, approval, rejection, or handoff",
            "users need to know who owns the next decision",
        ],
        "avoid_when": ["there is no explicit workflow owner or state"],
        "pairs_with": ["policy-matrix", "risk-summary-card", "diff-viewer"],
        "recommended_for": ["conversation-copilot", "dashboard", "document-content"],
        "keyword_triggers": ["approval", "reviewer", "handoff", "workflow", "decision"],
        "primitive_triggers": ["reviewer assignment chip", "compliance warning modal"],
        "anatomy": {
            "parts": ["rail", "stage-item", "owner-chip", "blocker-list", "primary-action", "secondary-action"],
            "states": ["pending", "active", "blocked", "approved", "rejected"],
        },
        "tokens": {
            "surface": "var(--color-surface)",
            "border": "var(--color-border)",
            "active": "var(--color-brand-primary)",
            "blocked": "var(--color-warning)",
            "approved": "var(--color-success)",
            "radius": "var(--radius-lg)",
        },
        "accessibility": [
            "current stage uses aria-current=\"step\"",
            "actions are real buttons with disabled/loading states",
            "blocked reasons are visible text, not color alone",
        ],
    },
    "risk-summary-card": {
        "family": "data-display",
        "role": "Compact risk score card with drivers, confidence, and recommended mitigation",
        "use_when": [
            "users need a fast read of risk before drilling into policy details",
            "AI confidence or compliance severity must be visible",
        ],
        "avoid_when": ["score cannot be explained with drivers"],
        "pairs_with": ["policy-matrix", "confidence-meter", "exception-queue"],
        "recommended_for": ["conversation-copilot", "dashboard", "monitoring-ops"],
        "keyword_triggers": ["risk", "confidence", "severity", "compliance", "warning"],
        "primitive_triggers": ["policy-check badge", "compliance warning modal"],
        "anatomy": {
            "parts": ["card", "score", "severity-label", "driver-list", "confidence-meter", "mitigation-action"],
            "states": ["low", "medium", "high", "loading"],
        },
        "tokens": {
            "surface": "var(--color-surface)",
            "border": "var(--color-border)",
            "low": "var(--color-success)",
            "medium": "var(--color-warning)",
            "high": "var(--color-danger)",
            "radius": "var(--radius-lg)",
        },
        "accessibility": [
            "score includes label and scale, not only number",
            "severity is text plus icon/color",
            "mitigation action is keyboard reachable",
        ],
    },
    "exception-queue": {
        "family": "data-display",
        "role": "Work queue for unresolved policy, data, or workflow exceptions",
        "use_when": [
            "multiple issues require triage, assignment, and resolution",
            "reviewers need to batch handle exceptions",
        ],
        "avoid_when": ["exceptions are rare and single-item"],
        "pairs_with": ["bulk-action-table", "policy-matrix", "approval-rail"],
        "recommended_for": ["conversation-copilot", "dashboard", "monitoring-ops"],
        "keyword_triggers": ["exception", "queue", "triage", "assign", "resolve"],
        "primitive_triggers": ["compliance warning modal", "reviewer assignment chip"],
        "anatomy": {
            "parts": ["queue-list", "queue-item", "priority", "assignee", "due-state", "bulk-action-bar"],
            "states": ["default", "selected", "assigned", "resolved", "empty"],
        },
        "tokens": {
            "surface": "var(--color-surface)",
            "selected-surface": "var(--color-surface-tint)",
            "border": "var(--color-border)",
            "priority": "var(--color-warning)",
            "radius": "var(--radius-md)",
        },
        "accessibility": [
            "multi-select state is announced with aria-selected",
            "bulk actions disclose affected count",
            "empty state explains how exceptions appear",
        ],
    },
    "saved-view-bar": {
        "family": "navigation",
        "role": "Saved view and scope switcher for repeated operational filters",
        "use_when": [
            "teams revisit the same filtered views often",
            "dense tools need stable scope memory",
        ],
        "avoid_when": ["filters are one-off and simple"],
        "pairs_with": ["filter-builder", "bulk-action-table", "exception-queue"],
        "recommended_for": ["dashboard", "monitoring-ops", "conversation-copilot"],
        "keyword_triggers": ["saved view", "filter", "scope", "segment", "view"],
        "primitive_triggers": ["thread list sidebar", "project switcher"],
        "anatomy": {
            "parts": ["tab-list", "saved-view-tab", "count-badge", "overflow-menu", "save-action"],
            "states": ["default", "active", "dirty", "overflow"],
        },
        "tokens": {
            "surface": "var(--color-surface)",
            "active-surface": "var(--color-surface-tint)",
            "border": "var(--color-border)",
            "active": "var(--color-brand-primary)",
            "radius": "var(--radius-md)",
        },
        "accessibility": [
            "tabs use role=\"tablist\" / role=\"tab\" when switching panels",
            "dirty state is text-announced",
            "overflow menu has keyboard navigation",
        ],
    },
    "filter-builder": {
        "family": "input",
        "role": "Advanced condition builder for multi-field filtering",
        "use_when": [
            "users need AND/OR logic across several fields",
            "filters should be saved, shared, or audited",
        ],
        "avoid_when": ["a few filter chips are sufficient"],
        "pairs_with": ["saved-view-bar", "bulk-action-table", "exception-queue"],
        "recommended_for": ["dashboard", "monitoring-ops", "conversation-copilot"],
        "keyword_triggers": ["filter", "condition", "segment", "query", "advanced search"],
        "primitive_triggers": ["thread item", "source reference card"],
        "anatomy": {
            "parts": ["condition-group", "field-select", "operator-select", "value-input", "logic-toggle", "remove-button"],
            "states": ["default", "focus", "invalid", "empty", "saved"],
        },
        "tokens": {
            "surface": "var(--color-surface)",
            "group-surface": "var(--color-surface-muted)",
            "border": "var(--color-border)",
            "focus": "var(--color-brand-primary)",
            "radius": "var(--radius-md)",
        },
        "accessibility": [
            "each condition has a visible label or aria-label",
            "invalid conditions explain the missing field/value",
            "logic groups are announced as AND/OR groups",
        ],
    },
    "bulk-action-table": {
        "family": "data-display",
        "role": "Selectable data table with sticky bulk action affordances",
        "use_when": [
            "users handle many records at once",
            "selection count and destructive actions must stay visible",
        ],
        "avoid_when": ["records are read-only or single-action"],
        "pairs_with": ["saved-view-bar", "filter-builder", "exception-queue"],
        "recommended_for": ["dashboard", "monitoring-ops", "conversation-copilot"],
        "keyword_triggers": ["bulk", "table", "queue", "records", "select"],
        "primitive_triggers": ["audit-trail timeline", "source reference card"],
        "anatomy": {
            "parts": ["table", "selection-cell", "column-header", "row", "bulk-action-bar", "pagination"],
            "states": ["default", "selected", "filtered", "sorted", "empty"],
        },
        "tokens": {
            "surface": "var(--color-surface)",
            "row-hover": "var(--color-surface-muted)",
            "selected": "var(--color-surface-tint)",
            "border": "var(--color-border)",
            "font": "var(--font-body)",
        },
        "accessibility": [
            "header checkbox exposes mixed state when partially selected",
            "selection count is announced when it changes",
            "bulk action bar appears after selection in logical focus order",
        ],
    },
    "tool-call-trace": {
        "family": "copilot-chat",
        "role": "Expandable trace of AI tool calls, inputs, outputs, and latency",
        "use_when": [
            "AI actions need explainability or debugging",
            "operators need to audit retrieval, policy checks, or workflow calls",
        ],
        "avoid_when": ["trace data is sensitive and cannot be summarized"],
        "pairs_with": ["audit-timeline", "citation-drawer", "decision-record-card"],
        "recommended_for": ["conversation-copilot", "monitoring-ops"],
        "keyword_triggers": ["tool call", "trace", "retrieval", "latency", "audit"],
        "primitive_triggers": ["audit-trail timeline", "policy-check badge"],
        "anatomy": {
            "parts": ["trace-list", "trace-step", "tool-name", "input-summary", "output-summary", "latency"],
            "states": ["collapsed", "expanded", "running", "failed", "complete"],
        },
        "tokens": {
            "surface": "var(--color-surface-muted)",
            "border": "var(--color-border)",
            "running": "var(--color-brand-primary)",
            "failed": "var(--color-danger)",
            "mono": "var(--font-mono)",
        },
        "accessibility": [
            "each trace step is expandable with aria-expanded",
            "running state uses aria-live=\"polite\"",
            "sensitive payloads are summarized or redacted",
        ],
    },
    "source-card": {
        "family": "copilot-artifact",
        "role": "Compact source record card with title, excerpt, metadata, and verification state",
        "use_when": [
            "AI output depends on external or internal source records",
            "users need a repeatable citation preview component",
        ],
        "avoid_when": ["source metadata is unavailable"],
        "pairs_with": ["citation-drawer", "evidence-graph", "inline-citation"],
        "recommended_for": ["conversation-copilot", "document-content"],
        "keyword_triggers": ["source", "citation", "reference", "evidence", "document"],
        "primitive_triggers": ["source reference card", "citation footnote"],
        "anatomy": {
            "parts": ["card", "source-title", "excerpt", "metadata-row", "verification-badge", "open-action"],
            "states": ["default", "hover", "verified", "stale", "unavailable"],
        },
        "tokens": {
            "surface": "var(--color-surface)",
            "border": "var(--color-border)",
            "verified": "var(--color-success)",
            "stale": "var(--color-warning)",
            "radius": "var(--radius-md)",
        },
        "accessibility": [
            "source title is a heading or labelled link",
            "excerpt length is bounded and not a full copyrighted passage",
            "verification state includes text",
        ],
    },
    "confidence-meter": {
        "family": "feedback",
        "role": "Confidence or certainty meter with explanation and threshold labels",
        "use_when": [
            "AI or policy outcome includes uncertainty",
            "users must decide whether to trust, edit, or escalate",
        ],
        "avoid_when": ["confidence cannot be explained or calibrated"],
        "pairs_with": ["risk-summary-card", "policy-matrix", "tool-call-trace"],
        "recommended_for": ["conversation-copilot", "monitoring-ops", "dashboard"],
        "keyword_triggers": ["confidence", "certainty", "risk", "threshold", "score"],
        "primitive_triggers": ["policy-check badge"],
        "anatomy": {
            "parts": ["meter", "value-label", "threshold-labels", "driver-summary", "tooltip(optional)"],
            "states": ["low", "medium", "high", "unknown"],
        },
        "tokens": {
            "track": "var(--color-surface-muted)",
            "fill": "var(--color-brand-primary)",
            "low": "var(--color-danger)",
            "medium": "var(--color-warning)",
            "high": "var(--color-success)",
            "radius": "var(--radius-pill)",
        },
        "accessibility": [
            "role=\"meter\" with aria-valuemin / aria-valuemax / aria-valuenow",
            "visible text explains what the score means",
            "do not encode trust solely with color",
        ],
    },
    "decision-record-card": {
        "family": "data-display",
        "role": "Auditable decision record summarizing decision, actor, evidence, and retention",
        "use_when": [
            "a reviewer or AI-assisted workflow reaches a durable decision",
            "regulated teams need record ids and retention status",
        ],
        "avoid_when": ["the action is transient and not auditable"],
        "pairs_with": ["audit-timeline", "approval-rail", "citation-drawer"],
        "recommended_for": ["conversation-copilot", "dashboard", "monitoring-ops"],
        "keyword_triggers": ["decision", "record", "retention", "audit", "approval"],
        "primitive_triggers": ["data retention indicator", "audit-trail timeline", "reviewer assignment chip"],
        "anatomy": {
            "parts": ["card", "record-id", "decision-summary", "actor-row", "evidence-links", "retention-state"],
            "states": ["draft", "recorded", "locked", "expired"],
        },
        "tokens": {
            "surface": "var(--color-surface)",
            "border": "var(--color-border)",
            "locked": "var(--color-brand-primary)",
            "expired": "var(--color-warning)",
            "mono": "var(--font-mono)",
        },
        "accessibility": [
            "record id is selectable text",
            "locked and expired states include text labels",
            "evidence links are grouped under an accessible heading",
        ],
    },
    "reviewer-assignment-picker": {
        "family": "input",
        "role": "Reviewer picker with role, availability, and escalation hints",
        "use_when": [
            "workflows require human approval or reassignment",
            "reviewer choice depends on policy ownership or availability",
        ],
        "avoid_when": ["there is only one fixed reviewer"],
        "pairs_with": ["approval-rail", "exception-queue", "presence-indicator"],
        "recommended_for": ["conversation-copilot", "dashboard", "document-content"],
        "keyword_triggers": ["reviewer", "assignment", "owner", "handoff", "escalation"],
        "primitive_triggers": ["reviewer assignment chip"],
        "anatomy": {
            "parts": ["field", "selected-reviewer-chip", "candidate-list", "availability", "role-label", "escalation-note"],
            "states": ["default", "searching", "selected", "unavailable", "error"],
        },
        "tokens": {
            "surface": "var(--color-surface)",
            "chip-surface": "var(--color-surface-tint)",
            "border": "var(--color-border)",
            "focus": "var(--color-brand-primary)",
            "radius": "var(--radius-md)",
        },
        "accessibility": [
            "combobox pattern for searchable reviewer list",
            "selected reviewers can be removed by keyboard",
            "availability is announced as text",
        ],
    },
    "retention-indicator": {
        "family": "feedback",
        "role": "Retention and recordkeeping status indicator for regulated content",
        "use_when": [
            "users need to know whether a record is retained, pending, or expired",
            "policy requires retention visibility near decisions",
        ],
        "avoid_when": ["retention is not relevant to user workflow"],
        "pairs_with": ["decision-record-card", "audit-timeline", "inspector-drawer"],
        "recommended_for": ["conversation-copilot", "monitoring-ops"],
        "keyword_triggers": ["retention", "recordkeeping", "archive", "expiry", "audit"],
        "primitive_triggers": ["data retention indicator"],
        "anatomy": {
            "parts": ["indicator", "status-label", "expiry-date", "policy-link", "tooltip(optional)"],
            "states": ["retained", "pending", "expired", "not-required"],
        },
        "tokens": {
            "surface": "var(--color-surface-muted)",
            "retained": "var(--color-success)",
            "pending": "var(--color-warning)",
            "expired": "var(--color-danger)",
            "border": "var(--color-border)",
        },
        "accessibility": [
            "status and expiry date are readable text",
            "tooltip content is also reachable via focus",
            "policy link text names the target policy",
        ],
    },
}


_APP_MODE_DEFAULTS: dict[str, tuple[str, ...]] = {
    "conversation-copilot": (
        "resizable-split-pane",
        "policy-matrix",
        "citation-drawer",
        "audit-timeline",
        "approval-rail",
        "risk-summary-card",
        "diff-viewer",
        "tool-call-trace",
        "decision-record-card",
        "reviewer-assignment-picker",
    ),
    "dashboard": (
        "saved-view-bar",
        "filter-builder",
        "bulk-action-table",
        "risk-summary-card",
        "exception-queue",
        "command-palette",
    ),
    "document-content": (
        "diff-viewer",
        "redline-viewer",
        "citation-drawer",
        "approval-rail",
        "source-card",
    ),
    "canvas-tool": (
        "resizable-split-pane",
        "command-palette",
        "inspector-drawer",
    ),
    "monitoring-ops": (
        "audit-timeline",
        "exception-queue",
        "saved-view-bar",
        "filter-builder",
        "tool-call-trace",
    ),
}


def get_advanced_component(name: str) -> dict[str, Any] | None:
    """Return an advanced component definition by name."""

    return ADVANCED_COMPONENTS.get(name)


def is_advanced_component(name: str) -> bool:
    return name in ADVANCED_COMPONENTS


def catalog_entries() -> list[dict[str, Any]]:
    """Return a compact serializable catalog for artifact output."""

    entries: list[dict[str, Any]] = []
    for name, spec in ADVANCED_COMPONENTS.items():
        entries.append(
            {
                "name": name,
                "family": spec["family"],
                "role": spec["role"],
                "use_when": spec.get("use_when", []),
                "avoid_when": spec.get("avoid_when", []),
                "pairs_with": spec.get("pairs_with", []),
                "recommended_for": spec.get("recommended_for", []),
            }
        )
    return entries


def recommend_advanced_components(
    *,
    brand_profile: dict[str, Any],
    blueprint: dict[str, Any],
    existing_components: list[str] | None = None,
    limit: int = 10,
) -> list[dict[str, Any]]:
    """Recommend advanced components from product context and existing primitives."""

    existing = {item.lower() for item in (existing_components or [])}
    signals = _context_signals(brand_profile, blueprint)
    app_modes = _app_mode_signals(signals)
    explicit_card_request = _explicit_card_requested(brand_profile, blueprint)
    suppress_card_named_components = (
        _operational_surface_requested(signals) or _card_wall_avoidance_requested(brand_profile)
    ) and not explicit_card_request
    rows: list[dict[str, Any]] = []

    for name, spec in ADVANCED_COMPONENTS.items():
        if name.lower() in existing:
            continue
        if suppress_card_named_components and _is_card_named_component(name, spec):
            continue

        score = 0
        matched: list[str] = []

        for app_mode in app_modes:
            if app_mode in spec.get("recommended_for", []):
                score += 4
                matched.append(f"mode:{app_mode}")

        if name in _defaults_for_modes(app_modes):
            score += 2
            matched.append("mode-default")

        for trigger in spec.get("keyword_triggers", []):
            if _contains_signal(signals, trigger):
                score += 2
                matched.append(trigger)

        for trigger in spec.get("primitive_triggers", []):
            if _contains_signal(signals, trigger):
                score += 3
                matched.append(trigger)

        for pair in spec.get("pairs_with", []):
            if pair.lower() in existing:
                score += 1
                matched.append(f"pairs:{pair}")

        if score <= 0:
            continue

        rows.append(
            {
                "name": name,
                "family": spec["family"],
                "role": spec["role"],
                "use_when": spec.get("use_when", []),
                "avoid_when": spec.get("avoid_when", []),
                "pairs_with": spec.get("pairs_with", []),
                "score": score,
                "matched_signals": sorted(set(matched)),
                "source": "advanced-component-catalog",
                "status": "recommended-advanced",
            }
        )

    rows.sort(key=lambda item: (-int(item["score"]), item["name"]))
    return rows[:limit]


def _context_signals(brand_profile: dict[str, Any], blueprint: dict[str, Any]) -> list[str]:
    values: list[str] = []

    def collect(value: Any) -> None:
        if isinstance(value, str):
            values.append(value.lower())
        elif isinstance(value, list):
            for item in value:
                collect(item)
        elif isinstance(value, dict):
            for item in value.values():
                collect(item)

    for key in (
        "product_summary",
        "brand_keywords",
        "tone_of_voice",
        "visual_keywords",
        "interaction_keywords",
        "product_primitives",
    ):
        collect(brand_profile.get(key))

    component_strategy = blueprint.get("component_strategy") or {}
    collect(component_strategy.get("product_primitives"))
    collect(component_strategy.get("concept_alignment"))
    collect(blueprint.get("app_mode"))
    collect(blueprint.get("product_archetype"))
    return values


def _positive_context_signals(brand_profile: dict[str, Any], blueprint: dict[str, Any]) -> list[str]:
    values: list[str] = []

    def collect(value: Any) -> None:
        if isinstance(value, str):
            values.append(value.lower())
        elif isinstance(value, list):
            for item in value:
                collect(item)
        elif isinstance(value, dict):
            for item in value.values():
                collect(item)

    for key in (
        "product_summary",
        "brand_keywords",
        "tone_of_voice",
        "visual_keywords",
        "interaction_keywords",
        "product_primitives",
    ):
        collect(brand_profile.get(key))

    component_strategy = blueprint.get("component_strategy") or {}
    collect(component_strategy.get("product_primitives"))
    collect(component_strategy.get("concept_alignment"))
    collect(blueprint.get("app_mode"))
    collect(blueprint.get("product_archetype"))
    return values


def _app_mode_signals(signals: list[str]) -> set[str]:
    modes = set()
    known = {
        "conversation-copilot",
        "dashboard",
        "document-content",
        "canvas-tool",
        "monitoring-ops",
        "commerce",
        "marketing-landing",
        "community-feed",
    }
    joined = " ".join(signals)
    for mode in known:
        if mode in joined:
            modes.add(mode)
    if "chat" in joined or "copilot" in joined or "prompt" in joined:
        modes.add("conversation-copilot")
    if "audit" in joined or "incident" in joined or "ops" in joined:
        modes.add("monitoring-ops")
    if "document" in joined or "draft" in joined or "redline" in joined:
        modes.add("document-content")
    if "canvas" in joined or "inspector" in joined:
        modes.add("canvas-tool")
    return modes


def _defaults_for_modes(app_modes: set[str]) -> set[str]:
    defaults: set[str] = set()
    for mode in app_modes:
        defaults.update(_APP_MODE_DEFAULTS.get(mode, ()))
    return defaults


def _contains_signal(signals: list[str], needle: str) -> bool:
    normalized = needle.lower()
    dashed = normalized.replace(" ", "-")
    spaced = normalized.replace("-", " ")
    return any(normalized in signal or dashed in signal or spaced in signal for signal in signals)


def _has_any_signal(signals: list[str], needles: tuple[str, ...]) -> bool:
    return any(_contains_signal(signals, needle) for needle in needles)


def _explicit_card_requested(brand_profile: dict[str, Any], blueprint: dict[str, Any]) -> bool:
    signals = _positive_context_signals(brand_profile, blueprint)
    return _has_any_signal(
        signals,
        (
            "dashboard cards",
            "card grid",
            "card layout",
            "kpi card",
            "stat card",
            "metric card",
            "summary card",
            "insight card",
            "source reference card",
            "product card",
            "asset card",
            "pricing card",
        ),
    )


def _operational_surface_requested(signals: list[str]) -> bool:
    return _has_any_signal(
        signals,
        (
            "operational overview",
            "operational surface",
            "data tables",
            "data table",
            "source ledger",
            "status summary row",
            "metric strip",
            "status rail",
            "operational rail",
            "policy matrix",
            "audit timeline",
            "diff viewer",
            "task queue",
            "account roster",
            "workspace",
        ),
    )


def _card_wall_avoidance_requested(brand_profile: dict[str, Any]) -> bool:
    anti_signals: list[str] = []
    for item in brand_profile.get("anti_keywords", []) or []:
        if isinstance(item, str):
            anti_signals.append(item.lower())
    return _has_any_signal(
        anti_signals,
        (
            "card wall",
            "generic card wall",
            "generic-card-wall",
            "homogeneous card",
            "dashboard cards",
        ),
    )


def _is_card_named_component(name: str, spec: dict[str, Any]) -> bool:
    low_name = name.lower()
    if low_name.endswith("-card") or low_name.endswith("_card") or low_name == "card":
        return True
    role = str(spec.get("role") or "").lower()
    return " card " in f" {role} "
