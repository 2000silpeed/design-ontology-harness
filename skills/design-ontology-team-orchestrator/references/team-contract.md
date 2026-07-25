# Team contract reference

| Role | Owns | Exit evidence |
| --- | --- | --- |
| Team Lead | sequencing, assignment, handoff ledger | next owner has a written handoff |
| Product Brief Author | concept, layout skeleton, differentiation, component scope | concrete `brand_profile.json` inputs and reserved `component_decision_path` |
| Token & Color Curator | Semantic OS Markdown color authority, fonts, token inputs | checksum-current `docs/color-reference.md` and complete profile decisions |
| Component Contract Author | anatomy, states, props, events, data, accessibility | separate `design-system/component-contracts.json` is complete and ready for compiler validation |
| Ontology Compiler | deterministic harness synthesis | generated blueprint/spec/emitted tokens/components pass strict validation |
| Visual Asset Producer | mockups, prompts, accepted assets, provenance | accepted asset manifest or explicit no-asset decision |
| UI Implementer | runtime UI, asset integration, and core behavior | integrated asset validation, implementation lint, and style divergence pass |
| Approved-Reference Fidelity Auditor | paired reference review, allowed composition/morphology/density/hierarchy/context metrics, correction brief | current runtime and screenshot hashes pass every critical invariant without copying prohibited scopes |
| Production QA | fresh browser, interaction, accessibility, aesthetic evidence | evidence matches current implementation tree |
| Release Governor | requirement-by-requirement audit | `verify-production-ui` passes |

The Team Lead uses the minimum number of specialists for the current stage. Token and component authoring can run in parallel only when the Brief Author has reserved the external component contract path, leaving each role a separate file. All other writing roles run sequentially: asset production finishes before implementation, the Approved-Reference Fidelity Auditor runs after implementation freeze, and Production QA starts only after the fidelity gate passes. A failed fidelity review returns its correction brief to the UI Implementer and requires a fresh runtime tree and screenshot set.
