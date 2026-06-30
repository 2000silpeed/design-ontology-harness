# Agent Org Network Product Spec

## 1. Product Frame

Agent Org Network is a question-routing organization layer. People ask a question in plain language; the system finds the human owner accountable for that knowledge, lets that owner answer from their own knowledge, and returns an answer stamped with who answered, the trust state of that answer, and its sources. It is not a single chatbot and it is not an agent-graph monitoring tool. The product makes ownership, accountability, trust state, sources, handoff, and audit visible — while hiding the internal routing machinery from the person asking.

Three kinds of people use it, and each sees a different surface:

- A person asking a question sees only a calm chat with the answer, its owner, its trust state, and its sources. The routing internals are never shown.
- A knowledge owner authors their own knowledge (an OKF bundle) with LLM help, reviews staged drafts step by step, and handles what arrives for them: contested ownership, backup answers made in their absence, and re-review of past answers when knowledge changes.
- An operator watches the whole organization: questions arriving, routing decisions, answers sent, workers connecting, and admits new workers.

The primary screen for a question-asker must feel like a trustworthy assistant, not a dashboard. The owner and operator screens are operated consoles — dense, audit-friendly, every status legible without color alone.

## 2. Core Screens

### 2.1 Ask — question chat (question-asker)

A calm conversational surface. The person asks; the answer comes back with accountability attached.

- Centered chat thread, generous whitespace, one question and one answer at a time in context
- Question bubble (the person), answer bubble (the organization)
- Staged routing trace shown as a quiet, collapsing progress line while the answer is prepared: "finding the owner" then "handed to cs_ops" then "drafting the answer" — checkmarks for done, a subtle spinner for the active step
- Answer bubble carries trust chips beneath the text: owner chip (who answered), trust-state chip (approved, draft pending approval, or backup), and source chips (which knowledge documents grounded it)
- Special answer states: "draft, awaiting approval" when a human must sign off, and "no owner found — escalated" when nothing matched
- Bottom composer input with send control
- The internal routing decision, candidate scores, and any machinery are never rendered here — only owner, trust state, and sources

### 2.2 Author — OKF knowledge authoring (knowledge owner)

The owner turns raw material into reviewed, published knowledge with staged LLM help. This runs in the owner's own environment; raw material and drafts never leave it, and only the approved index of topics is shared centrally.

- Page header with an ownership badge and a privacy note: runs in the owner's environment, raw and drafts stay local, only the approved table of contents is shared
- A staged pipeline indicator across the top: ingest, split into concepts, derive the routing question, link related concepts, index and publish — the current stage highlighted, earlier stages checked
- A raw-source summary strip listing the inputs that were ingested (documents, exports, pasted text), with a re-run control
- Concept draft cards, one per extracted concept, each carrying: a concept identifier, a domain tag, a review-state badge (unreviewed, edited, rejected), a title, the derived routing question, and a body preview
- Each unreviewed card offers three dispositions: approve, edit, reject — approve and edit move the concept forward, reject drops it from publication
- An edited card shows a small before-and-after diff of the changed field (for example, the routing question)
- A rejected card is dimmed and labeled with the reason (for example, a domain outside the owner's authority, automatically excluded from publication)
- A bottom action bar summarizing the dispositions ("2 approved, 1 edited, 1 rejected — rejected items are not published") and a single commit-and-publish action

### 2.3 Inbox — owner handling queue (knowledge owner)

Everything that needs the owner's first-person decision, in one place, across three tabs.

- Tab one, contested ownership: cases where more than one owner could be accountable. Each case shows the question, the candidate owners, what knowledge each candidate holds that matched (coverage), the specific matched concepts, an on-demand pull of the actual document content, and an assign control to settle ownership
- Tab two, backup answers: answers a backup worker sent in the owner's name while the owner was away, presented for review with approve, correct, or dismiss
- Tab three, re-review: past answers and precedents flagged stale because the underlying knowledge changed, queued for the owner to keep, re-answer, or invalidate
- Each row carries the question, the trust state, a timestamp, and a clear first-person action set
- A notification affordance for newly arrived items

### 2.4 Console — operator monitoring (operator)

The whole organization at a glance, live.

- A live-connection indicator (real-time feed is on)
- A row of summary metrics: questions per minute, share routed cleanly, contested cases waiting, workers connected
- A real-time event feed, newest first, each event with a timestamp, an icon, a one-line description, and a status tag: a question arriving, a routing decision (routed cleanly, contested with candidate count, or no owner found and escalated), an answer sent with its trust state, a worker connecting and publishing its topic index
- A worker-admission panel listing workers requesting access, each with its owner and approve or revoke controls, and a token affordance
- A light organization view: owners and their knowledge domains, who maintains what — a reference map, not a decorative graph
- An audit log table: every question's path from arrival through routing to answer, sortable, with trust state and source on each row

## 3. Identity And Constraints

- Voice: direct, operational, audit-friendly, low-drama, specific. Calm and trustworthy on the asker surface; dense and legible on the owner and operator surfaces.
- Every status must be legible without relying on color alone — pair an icon and a word with any color.
- Trust state and source must travel with every answer, everywhere an answer appears.
- Internal routing machinery (scores, candidate math, decision internals) is operator-and-owner context only; it is never shown to the question-asker.
- Authoring and review of knowledge happen in the owner's environment; the center holds only the published table of contents, never raw material, drafts, or document bodies.
- Restrained multi-accent: a small set of semantic accents for trust state, routing outcome, and review disposition — never decorative.

## 4. Platforms And Accessibility

- Platforms: web, desktop-web. Dark mode is the default; light mode supported.
- Accessibility floor: WCAG 2.2 AA, full keyboard operation, non-color status encoding, legible dense tables and feeds.
- Korean-first product copy; typography must carry Korean and Latin and a monospace for identifiers and timestamps.

## 5. What This Is Not

- Not a single full-screen chatbot with no accountability.
- Not an agent-orchestration graph, DAG builder, or run-replay tool.
- Not a marketing visualization. No decorative network graph, no sci-fi glow, no unexplained automation, no opaque status.
