# Agent Org Network Product Spec

## 1. Product Frame

Agent Org Network is an operational workspace for teams that run multiple AI agents across product, support, engineering, data, and governance workflows. The product shows which agents exist, who owns them, what tools they can call, how they hand work off, and whether current runs are healthy.

The primary screen must feel like an operated console, not a marketing visualization. The graph is important, but every visible node, edge, status badge, table row, and timeline event needs enough context to support a real decision.

## 2. Core Screens

### 2.1 Network Overview

The default view combines an agent org graph canvas with a right-side inspection drawer and a bottom run table.

- Left sidebar navigation: Overview, Agents, Teams, Tools, Policies, Runs, Incidents, Audit Log, Settings
- Topbar with workspace switcher, global search, command palette, environment selector, and user profile menu
- Zoomable graph with team clusters, agent node cards, handoff edges, owner badges, model badges, and risk indicators
- Graph filters for team, owner, model, tool, permission scope, health status, and incident state
- Selected node opens a drawer with owner, purpose, model, prompt version, tool permissions, last run, open incidents, and policy gates
- Bottom data table lists active runs with sortable columns for agent, task, queue age, owner, risk, policy status, and last event

### 2.2 Agent Detail

The agent detail page explains what an agent does and whether it is safe to keep running.

- Header summary card with agent name, owner avatar, team, health score, model, environment, and release version
- Capability matrix showing tasks, allowed tools, approval requirements, and blocked scopes
- Prompt and tool diff drawer for comparing the current version against the previous release
- Run replay timeline with tool calls, handoff events, policy checks, warnings, and human approvals
- Incident feed with open alerts, muted alerts, linked audit records, and owner comments
- Forms for owner assignment, risk tier, policy override, and deprecation schedule

### 2.3 Team Cluster View

The team cluster view focuses on one department or function.

- Cluster header with team owner, active agents, weekly runs, failed handoffs, and pending approvals
- Agent roster table with filters, status badges, model badges, and row actions
- Handoff path visualization showing upstream and downstream teams
- Tool usage heatmap for Slack, GitHub, Jira, CRM, data warehouse, browser, and internal APIs
- Governance checklist with required reviews, missing docs, expired approvals, and exceptions

### 2.4 Runs And Queue

The runs screen is a dense operations table for active and historical automation work.

- Saved view tabs: Live, Blocked, Waiting for human, High risk, Regression watch, Archived
- Filter toolbar with search, date range, team, agent, model, tool, policy state, and risk tier
- Sortable data grid with sticky column headers and compact row density
- Detail drawer for each run with task input, agent path, tool timeline, handoff chain, result, and audit trail
- Empty state for filtered searches, with a clear reset action
- Toast and alert banner for failed refresh, stale data, or policy sync errors

### 2.5 Policy And Permissions

The policy screen makes automation boundaries explicit.

- Policy rule table with name, scope, owner, enforced state, last edited time, and linked incidents
- Permission matrix mapping agents to tools, data scopes, write actions, and human approval requirements
- Modal dialog for creating a policy exception with reason, expiry, reviewer, and blast-radius note
- Review queue for pending approvals, with approve, reject, request changes, and assign reviewer actions
- Audit log timeline for policy changes and permission grants

### 2.6 Tool Registry

The tool registry shows every integration an agent can call.

- Tool cards grouped by category: communication, code, tickets, CRM, data, browser, internal API
- Tool detail drawer with allowed agents, scopes, rate limits, recent failures, and owner
- Integration health chart with success rate, latency, timeout count, and permission errors
- Configuration forms with text fields, dropdowns, checkboxes, token status, and test connection action

### 2.7 Onboarding Flow

New teams need a guided setup flow that does not hide governance requirements.

- Stepper for connect tools, define teams, add agents, assign owners, set policies, and verify first run
- Import wizard for CSV or existing agent manifest
- Progress checklist with blocked states and required reviewer actions
- Final review screen summarizing graph changes, policy exceptions, and owners before activation

## 3. Interaction Requirements

- Keyboard-first navigation: slash command or command palette opens global search and quick actions
- Graph traversal must not depend only on pointer hover; selected nodes and edges need visible focus states
- Status must never rely on color alone. Pair color with icon, label, and tooltip
- Tables must support sorting, filtering, sticky headers, compact density, and row detail drawers
- Drawers and modals must trap focus, support escape to close, and return focus to the triggering element
- Long-running operations need progress, retry, and explicit failure states
- The product must support both light and dark modes, with light mode as the default

## 4. Data Objects

- Agent: id, name, owner, team, model, purpose, health, risk tier, version, active tools, policy state
- Team: id, name, owner, active agents, run volume, incident count, pending approvals
- Tool: id, category, owner, scopes, rate limits, allowed agents, health, last failure
- Run: id, agent, task, status, queue age, started at, handoff chain, tool calls, result, risk, policy checks
- Policy: id, name, scope, owner, enforcement state, exceptions, reviewer, expiry, audit history
- Incident: id, severity, agent, tool, run, owner, status, mitigation, linked audit record

## 5. Design System Needs

- App shell, sidebar navigation, topbar, breadcrumb, command palette
- Agent node card, handoff edge label, team cluster badge, owner avatar, model badge
- Dashboard stat card, health summary card, risk indicator, status badge
- Data table, filter toolbar, saved view tabs, pagination, row actions
- Timeline, run replay item, audit log item, incident feed item
- Drawer, modal dialog, alert banner, toast, empty state
- Permission matrix, capability matrix, policy rule table, tool registry card
- Stepper, import dropzone, form field, dropdown, checkbox, segmented control

## 6. Visual Direction

The visual language should be neutral, dense, and legible. It should use restrained accents for ownership, risk, health, and selected graph paths. Avoid decorative AI motifs, glowing gradient backgrounds, unlabeled node-link diagrams, and oversized hero-style panels inside the product surface.

The first viewport should show real operational state: graph, active runs, filters, ownership, health, and policy context. A user should be able to answer three questions quickly: what agents are running, which handoffs are risky, and who owns the next action.
