# Agent Org Network Harness Agent Brief

This project uses `design-ontology-harness` as a reusable system-authoring harness.

## Product Boundary

Agent Org Network is an operational console for AI agent programs. It is not a
single-chatbot demo and it is not a decorative network graph. The system must
make ownership, handoffs, tool permissions, policy gates, run health, incidents,
and audit trails visible.

## What The Agent Should Do

1. Read `brand_profile.json`
2. Read `spec.md`
3. Curate Omnigen references when local vault access is available
4. Load the configured knowledge base
5. Produce custom system outputs into `build/`
6. Avoid copying any single reference system or generated image directly

## Success Criteria

- The outputs reflect this project's own identity
- The system spec is useful for a real product team
- Tokens and components are grounded in the product primitives
- Graph, table, timeline, drawer, policy, and audit surfaces are treated as first-class components
- Status and risk states are legible without relying on color alone
- Visual references are used for density, morphology, and workflow structure only

## Avoid

- Decorative AI glow backgrounds
- Full-screen chat UI as the primary product surface
- Unlabeled graph nodes or edges
- Marketing-page hero composition inside the app
- Autonomous action states without owner, policy, or audit context
