# Hallmark reference study

This note records how [`Nutlope/hallmark`](https://github.com/Nutlope/hallmark)
was evaluated and which ideas were translated into the harness.

## Source and boundary

- Studied revision: [`13ac0ec7e148655948100b6396439e481361d690`](https://github.com/Nutlope/hallmark/commit/13ac0ec7e148655948100b6396439e481361d690)
- Studied on: 2026-08-10
- Upstream license: MIT
- Integration form: independent Python implementation informed by the upstream
  taxonomy; no Hallmark runtime, npm package, theme catalog, or copied rulebook
  is shipped by this repository.

Hallmark is a Markdown skill for AI coding agents. Its `audit` verb is an agent
instruction that asks for a read-only, severity-ranked report; it is not an
executable CLI, linter, or CI engine. The repository has no analyzer binary or
automated gate suite. Its strongest contribution is therefore the review model,
not reusable audit code.

## What transferred

Four ideas improve the existing harness without creating a second design
authority:

1. **Named, ranked findings.** Machine-facing `checks[].issues` remain the CI
   source of truth. `audit-implementation` now derives a human-facing
   `punch_list` with tell, category, impact severity, location, evidence, fix,
   and a stable finding fingerprint.
2. **Structural sameness is a defect.** Existing style fingerprints remain the
   executable mechanism. Attractor and repeated-fingerprint failures are now
   normalized as real audit findings instead of being hidden in check details.
3. **Bound motion explicitly.** Three high-confidence static rules were added:
   `DS109` unbounded transitions, `DS110` layout-property transitions, and
   `DS111` CSS animation without a substantive reduced-motion reset. These are
   evaluated in authored stylesheets and embedded `<style>` blocks; the
   `transition-all` utility is also recognized in class attributes. Reduced
   motion coverage must match the animated selector or be a validated universal
   reset. The rules are versioned as `design-ontology.implementation-lint/v2`;
   they intentionally affect the existing strict `lint-implementation` gate as
   well as the unified audit.
4. **Do not fake review coverage.** Philosophy, hierarchy, fold, overflow,
   clickable wrapping, state behavior, and reference fidelity are listed as
   deferred coverage and routed to the existing aesthetic, browser,
   component-runtime, fidelity, and production gates.

The unified audit was also hardened around those ideas: enabled-check execution
errors fail closed; cross-project comparison uses the shared registry by
default; a separate harness `project_dir` supplies blueprint context; registry
mutation happens only after the complete audit passes; inputs and rule versions
are SHA-bound in report provenance, with source read hashes and auxiliary input
pre/post checks rejecting mid-run drift; and invalid or repository-wide
suppressions are rejected. Shared registry reads are schema-validated and
registrations use an OS-backed file lock on POSIX and Windows plus atomic
replacement so parallel passing audits cannot corrupt or silently overwrite one
another.

## What did not transfer

The following Hallmark artifacts are intentionally not adopted:

- `.hallmark/log.json` and CSS stamps: the harness already has a validated
  style-fingerprint registry, authored product briefs, handoffs, and runtime
  evidence.
- `design.md` as a new source of truth: `spec.md`, `brand_profile.json`, the
  Semantic OS graph, emitted tokens, and component contracts keep their current
  precedence.
- the 21-theme and macrostructure catalogs: a catalog choice cannot replace an
  authored product concept or layout skeleton.
- global bans on particular fonts, pure white, italic headings, accent area, or
  eyebrow placement: these are taste rules that can conflict with the brief,
  Semantic OS, localization, or an approved reference.
- a claim that every upstream gate ran: static code cannot establish rendered
  hierarchy, viewport behavior, computed contrast inheritance, or interaction
  state quality.

## Workflow mapping

| Hallmark concept | Harness owner |
| --- | --- |
| Build a new surface | concept author → ontology compiler → UI implementer |
| Read-only audit | `audit-implementation` |
| Redesign | existing refactor/rebuild approval boundary |
| Study a reference | advisory reference inspection and reference packs |
| Structural memory | `registry/style_fingerprints.json` |
| Design-system authority | brief/profile → Semantic OS → generated system/contracts |
| Visual judgment | aesthetic review + browser evidence |
| Release decision | `verify-production-ui` by Release Governor |

## Upstream caveats

The studied repository is useful editorial guidance but not a stable executable
specification. At the studied revision its README says 57 gates while the gate
document describes 58 by numbering 1–57 plus 38a, and some examples lag the
current skill version. This harness therefore uses its own stable DS rule IDs,
regression fixtures, report schema, and source revision instead of importing an
upstream gate count.

Conceptual borrowing is documented here. If future work copies substantial
upstream prose, recipes, or examples, preserve the upstream MIT copyright and
license notice in a third-party notice before merging.
