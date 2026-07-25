from __future__ import annotations

import json
import re
from datetime import datetime, timezone
from hashlib import sha256
from pathlib import Path
from typing import Any


TEAM_SCHEMA_VERSION = "design-ontology-agent-team/v1"
HANDOFF_SCHEMA_VERSION = "design-ontology-handoff/v1"


ROLE_ORDER = (
    "team-lead",
    "brief-author",
    "token-curator",
    "component-author",
    "ontology-compiler",
    "visual-asset-producer",
    "ui-implementer",
    "reference-fidelity-auditor",
    "production-qa",
    "release-governor",
)

STAGE_ORDER = (
    "concept",
    "tokens-and-components",
    "system",
    "visual",
    "implementation",
    "fidelity",
    "qa",
    "release",
)

CONDITIONAL_CODEX_SKILLS = {
    "reference-inspector": "design-system-reference-inspect",
    "ui-refactor": "design-system-refactor",
    "ui-rebuild": "design-system-rebuild",
}

CONDITIONAL_CLAUDE_AGENTS = {
    "reference-inspector": "design-system-reference-inspect.md",
    "ui-refactor": "design-system-refactor.md",
    "ui-rebuild": "design-system-rebuild.md",
}

STAGE_SPECIALISTS = {
    "concept": {"brief-author"},
    "tokens-and-components": {"token-curator", "component-author"},
    "system": {"ontology-compiler"},
    "visual": {"visual-asset-producer"},
    "implementation": {"ui-implementer"},
    "fidelity": {"reference-fidelity-auditor"},
    "qa": {"production-qa"},
    "release": {"release-governor"},
}

DIRECT_STAGE_TRANSITIONS = {
    "concept": set(),
    "tokens-and-components": {
        ("brief-author", "token-curator"),
        ("brief-author", "component-author"),
        ("ontology-compiler", "token-curator"),
        ("ontology-compiler", "component-author"),
    },
    "system": {
        ("token-curator", "ontology-compiler"),
        ("component-author", "ontology-compiler"),
        ("visual-asset-producer", "ontology-compiler"),
    },
    "visual": {
        ("ontology-compiler", "visual-asset-producer"),
        ("ui-implementer", "visual-asset-producer"),
    },
    "implementation": {
        ("visual-asset-producer", "ui-implementer"),
        ("reference-fidelity-auditor", "ui-implementer"),
        ("production-qa", "ui-implementer"),
    },
    "fidelity": {("ui-implementer", "reference-fidelity-auditor")},
    "qa": {
        ("reference-fidelity-auditor", "production-qa"),
        ("release-governor", "production-qa"),
    },
    "release": {("production-qa", "release-governor")},
}


def team_contract(artifact_dir: str = "design-system") -> dict[str, Any]:
    return {
        "schema_version": TEAM_SCHEMA_VERSION,
        "artifact_dir": artifact_dir,
        "mission": (
            "Turn a product brief into an ontology-grounded, production-verifiable UI without "
            "letting reference imagery or a single model silently become the source of truth."
        ),
        "dispatch_policy": {
            "default": "stage-owner-only",
            "max_parallel_specialists": 2,
            "rules": [
                "The team lead owns sequencing and handoffs; it does not duplicate specialist work.",
                "Dispatch only the role that owns the next missing artifact or failed gate.",
                "Only read-only research and the file-separated token/component authoring pair may run in parallel.",
                "Never let two writing agents edit the same file set concurrently.",
                "Visual asset production must finish before UI implementation starts.",
                "Approved-reference fidelity review starts only after the implementation tree is frozen.",
                "Production QA starts only after the approved-reference fidelity gate passes.",
                "A later role may reject a handoff, but it must cite a concrete missing artifact or failed command.",
            ],
        },
        "roles": [
            {
                "id": "team-lead",
                "title": "Team Lead / Orchestrator",
                "owns": ["stage selection", "work assignment", "handoff ledger", "scope control"],
                "writes": [f"{artifact_dir}/handoffs/*.json"],
                "must_not": ["invent design decisions owned by specialists", "declare release readiness"],
                "exit_when": "The next owner has one schema-valid handoff with reproducible gate evidence.",
            },
            {
                "id": "brief-author",
                "title": "Product Brief Author",
                "owns": ["application concept", "layout skeleton", "product primitives", "component scope"],
                "writes": ["projects/*/spec.md", "projects/*/brand_profile.json"],
                "must_not": [
                    "choose a preset as a substitute for product structure",
                    "author detailed component contracts",
                    "implement UI code",
                ],
                "workflow_skills": {
                    "codex": "design-system-concept-author",
                    "claude": "design-system-concept-author",
                },
                "exit_when": (
                    "application_concept, layout_skeleton, design_differentiation, and a concrete component scope "
                    "exist; component_decision_path reserves the external contract file."
                ),
            },
            {
                "id": "token-curator",
                "title": "Token & Color Curator",
                "owns": [
                    "Semantic OS Markdown color authority",
                    "brand_profile color_reference and font_system",
                    "palette strategy",
                    "emitted token integrity",
                ],
                "writes": ["projects/*/brand_profile.json color_reference/font_system", "projects/*/design-system/runtime-theme.css"],
                "must_not": [
                    "edit generated tokens.css by hand",
                    "edit the component contract file",
                    "sample authoritative colors from advisory screenshots",
                    "hand-edit the embedded Semantic OS graph in docs/color-reference.md",
                ],
                "workflow_skills": {
                    "codex": "design-system-architect",
                    "claude": "design-system-architect",
                },
                "required_commands": [
                    "uv run design-ontology sync-semantic-colors --source <semantic-os-graph.json> --color-reference-output docs/color-reference.md --check --json",
                ],
                "exit_when": (
                    "docs/color-reference.md contains the current checksum-verified Semantic OS graph, "
                    "the selected semantic roles resolve from that Markdown, and color_reference/font_system inputs are complete."
                ),
            },
            {
                "id": "component-author",
                "title": "Component Contract Author",
                "owns": ["component inventory decision", "anatomy", "states", "interaction/data/accessibility contracts"],
                "writes": ["projects/*/design-system/component-contracts.json"],
                "must_not": [
                    "accept family defaults as domain contracts",
                    "edit brand_profile.json while Token Curator is running",
                    "implement UI code",
                ],
                "workflow_skills": {
                    "codex": "design-system-concept-author",
                    "claude": "design-system-concept-author",
                },
                "required_commands": [
                    "python -m json.tool <project>/design-system/component-contracts.json",
                ],
                "exit_when": (
                    "The external JSON parses and every scoped domain component has authored anatomy, states, "
                    "variants, props, interaction, data, responsive, content, token, and accessibility fields. "
                    "The Ontology Compiler owns the generated strict gate."
                ),
            },
            {
                "id": "ontology-compiler",
                "title": "Ontology Compiler",
                "owns": ["run-project synthesis", "blueprint", "generated token and component artifacts"],
                "writes": [f"{artifact_dir}/**", "projects/*/build/system/**", "projects/*/design-system/tokens.css"],
                "must_not": ["rewrite authored source decisions", "continue after strict profile or component validation fails"],
                "workflow_skills": {
                    "codex": "design-system-architect",
                    "claude": "design-system-architect",
                },
                "required_commands": [
                    "uv run design-ontology run-project --project-dir <project> --kb-dir <kb-dir>",
                    "uv run design-ontology emit-tokens --project-dir <project>",
                    "uv run design-ontology validate-component-contracts --project-dir <project> --json",
                ],
                "exit_when": (
                    "The generated profile report is valid, emitted tokens are reproducible, and strict component "
                    "validation passes."
                ),
            },
            {
                "id": "visual-asset-producer",
                "title": "Visual Director / Asset Producer",
                "owns": ["ontology-derived mockups", "image prompts", "visual asset review", "asset manifest"],
                "writes": [
                    "assets/**",
                    "public/generated/design-system/**",
                    "projects/*/assets/**",
                    "projects/*/design-system/reference-fidelity-contract.json",
                ],
                "must_not": ["copy reference UI", "hotlink assets", "bypass asset review and provenance"],
                "workflow_skills": {
                    "codex": "design-system-visual-assets",
                    "claude": "design-system-visual-assets",
                },
                "required_commands": [
                    "uv run design-ontology build-image-prompts --project-dir <project> --candidates-per-slot 3",
                    "uv run design-ontology register-image-asset <reviewed-candidate-args>",
                    "uv run design-ontology validate-image-assets --project-dir <project> --json",
                ],
                "exit_when": (
                    "The chosen mockup direction is ontology-derived, and each required raster asset is accepted "
                    "and traceable. When a direction is approved, its allowed preserve invariants and prohibited "
                    "similarity scopes are frozen in reference-fidelity-contract.json. Codex image_gen is preferred "
                    "when generation is needed; runtime integration belongs to UI Implementer."
                ),
            },
            {
                "id": "ui-implementer",
                "title": "UI Implementer",
                "owns": ["responsive application code", "token binding", "component behavior", "theme parity"],
                "writes": ["src/**", "app/**", "components/**", "styles/**", "public/**"],
                "must_not": ["change ontology inputs to hide implementation drift", "claim production readiness"],
                "workflow_skills": {
                    "codex": "design-system-implementer",
                    "claude": "design-system-implement",
                },
                "required_commands": [
                    "uv run design-ontology promote-image-asset <wired-asset-args>",
                    "uv run design-ontology validate-image-assets --project-dir <project> --require-integrated --json",
                    "uv run design-ontology lint-implementation --target-repo <implementation-repo> --json",
                    "uv run design-ontology check-style-divergence --project-dir <implementation-repo>",
                ],
                "exit_when": (
                    "Core interactions work, required assets are wired and integrated, and implementation lint plus "
                    "style-divergence checks pass."
                ),
            },
            {
                "id": "reference-fidelity-auditor",
                "title": "Approved-Reference Fidelity Auditor",
                "owns": [
                    "paired approved-reference review",
                    "composition and morphology fidelity",
                    "density and hierarchy fidelity",
                    "context linkage fidelity",
                    "correction brief",
                ],
                "writes": [
                    "projects/*/screenshots/reference-fidelity/**",
                    "projects/*/build/system/production/reference-fidelity/**",
                ],
                "must_not": [
                    "edit implementation code",
                    "edit the approved fidelity contract or reference",
                    "sample palette or typography from advisory references",
                    "score information architecture, product copy, logos, or redistributable assets by similarity",
                    "reuse a runtime tree or screenshot SHA set for a claimed correction iteration",
                    "claim production readiness",
                ],
                "required_commands": [
                    "uv run design-ontology reference-fidelity-loop --project-dir <project> --target-repo <implementation-repo> --review-artifact <paired-review.json>",
                ],
                "exit_when": (
                    "A paired multimodal review binds the unchanged approved contract/reference SHA, current "
                    "runtime-tree SHA, and fresh screenshot SHA set; every critical invariant passes. A failed "
                    "review returns an exact correction brief to the UI Implementer without changing the contract."
                ),
            },
            {
                "id": "production-qa",
                "title": "Visual & Runtime QA Auditor",
                "owns": ["browser evidence", "interaction checks", "accessibility checks", "aesthetic review"],
                "writes": [
                    "projects/*/screenshots/production/**",
                    "projects/*/build/system/production/screenshots.json",
                    "projects/*/build/system/production/aesthetic/**",
                    "projects/*/build/system/production/browser-observations/**",
                    "projects/*/build/system/production/browser-evidence-bundle.json",
                    "projects/*/build/system/production/component-runtime/**",
                    "projects/*/design-qa.md",
                ],
                "must_not": ["approve from code inspection alone", "reuse stale screenshots after runtime changes"],
                "required_commands": [
                    "uv run design-ontology record-screenshot-evidence <args>",
                    "uv run design-ontology apply-aesthetic-review <args>",
                ],
                "exit_when": (
                    "Fresh desktop/mobile and light/dark evidence matches the frozen runtime tree, and one "
                    "versioned Codex Desktop browser evidence bundle binds screenshots, DOM/state/console, "
                    "interaction, overflow, accessibility, and component-runtime observations to the same "
                    "in-app Browser session."
                ),
            },
            {
                "id": "release-governor",
                "title": "Release Governor",
                "owns": ["completion audit", "gate verification", "release decision"],
                "writes": [f"{artifact_dir}/handoffs/release-decision.json"],
                "must_not": ["fix implementation while auditing", "waive a required gate without user approval"],
                "required_commands": [
                    "uv run design-ontology verify-production-ui --project-dir <project> --target-repo <implementation-repo> --json",
                ],
                "exit_when": "Every requested outcome is evidenced and verify-production-ui passes against current files.",
            },
        ],
        "conditional_specialists": [
            {
                "id": "reference-inspector",
                "use_when": "A website or screenshot reference must be translated into advisory morphology without copying it.",
                "returns_to": "brief-author or ui-implementer",
            },
            {
                "id": "ui-refactor",
                "use_when": "An existing UI must adopt tokens and contracts without changing its layout or behavior.",
                "returns_to": "ui-implementer",
            },
            {
                "id": "ui-rebuild",
                "use_when": "The user explicitly approved a structural rebuild after concept and component gates passed.",
                "returns_to": "ui-implementer",
            },
        ],
        "stages": [
            {
                "id": "concept",
                "owner": "brief-author",
                "required_outputs": [
                    "brand_profile.json with application_concept, layout_skeleton, design_differentiation, component scope, and component_decision_path",
                ],
                "exit_gate": "The concept fields and component scope are concrete; component_decision_path reserves a separate contract file.",
            },
            {
                "id": "tokens-and-components",
                "owner": "team-lead",
                "parallel_owners": ["token-curator", "component-author"],
                "required_outputs": [
                    "color/font decisions resolved from docs/color-reference.md",
                    "fully authored design-system/component-contracts.json",
                ],
                "exit_gate": "Semantic OS Markdown authority is current and every scoped component input is fully authored for compiler validation.",
            },
            {
                "id": "system",
                "owner": "ontology-compiler",
                "required_outputs": ["system_spec.md", "token_schema.json", "component_inventory.json", "component_specs.json", "tokens.css"],
                "exit_gate": "run-project and emit-tokens complete, then validate-component-contracts passes without --allow-needs-authoring.",
            },
            {
                "id": "visual",
                "owner": "visual-asset-producer",
                "required_outputs": ["selected visual target when building a new UI", "reviewed and registered assets when imagery is required"],
                "exit_gate": (
                    "Every required raster candidate is accepted and traceable to its prompt or licensed source; "
                    "an approved direction has a hashed reference-fidelity contract; if Claude lacks an image tool, "
                    "its prompt packet is handed to Codex image_gen instead of faking completion."
                ),
            },
            {
                "id": "implementation",
                "owner": "ui-implementer",
                "required_outputs": [
                    "responsive implementation",
                    "working core interactions",
                    "accepted assets wired and promoted to integrated",
                    "light/dark parity unless explicitly scoped otherwise",
                ],
                "exit_gate": "Integrated asset validation, lint-implementation, and check-style-divergence pass.",
            },
            {
                "id": "fidelity",
                "owner": "reference-fidelity-auditor",
                "required_outputs": [
                    "hashed approved-reference fidelity contract",
                    "paired multimodal review bound to the current runtime tree and screenshot SHA set",
                    "correction brief for every failed invariant",
                ],
                "exit_gate": (
                    "reference-fidelity-loop passes every critical composition, morphology, density, hierarchy, "
                    "task-visibility, and context-linkage invariant without scoring prohibited palette, type, IA, "
                    "copy, logo, or asset similarity."
                ),
            },
            {
                "id": "qa",
                "owner": "production-qa",
                "required_outputs": ["matching route/state screenshots", "runtime checks", "multimodal aesthetic review"],
                "exit_gate": "Current implementation tree has fresh desktop/mobile and light/dark evidence.",
            },
            {
                "id": "release",
                "owner": "release-governor",
                "required_outputs": ["release-decision.json"],
                "exit_gate": "verify-production-ui passes for the actual target repository.",
            },
        ],
        "handoff": {
            "directory": f"{artifact_dir}/handoffs",
            "schema": f"{artifact_dir}/handoffs/handoff.schema.json",
            "rule": "No stage changes owner without a written handoff containing current gate evidence.",
        },
        "runtime_adapters": {
            "codex": {
                "orchestrator_skill": "$design-ontology-team-orchestrator",
                "specialist_surface": "plugin skills plus Codex sub-agents when parallel work is useful",
            },
            "claude": {
                "orchestrator_agent": "design-team-lead",
                "specialist_surface": ".claude/agents/*.md and .claude/skills/*/SKILL.md",
            },
        },
    }


def handoff_schema() -> dict[str, Any]:
    return {
        "$schema": "https://json-schema.org/draft/2020-12/schema",
        "$id": "https://example.com/design-ontology-handoff.schema.json",
        "title": "Design Ontology Agent Handoff",
        "type": "object",
        "additionalProperties": False,
        "required": [
            "schema_version", "run_id", "created_at", "project", "from_role", "to_role", "stage", "status",
            "summary", "input_artifacts", "output_artifacts", "changed_paths", "decisions",
            "gate_results", "blockers", "risks", "next_action",
        ],
        "properties": {
            "schema_version": {"const": HANDOFF_SCHEMA_VERSION},
            "run_id": {"type": "string", "minLength": 1},
            "created_at": {"type": "string", "format": "date-time"},
            "project": {"type": "string", "minLength": 1},
            "from_role": {"enum": list(ROLE_ORDER)},
            "to_role": {"enum": list(ROLE_ORDER)},
            "stage": {"enum": list(STAGE_ORDER)},
            "status": {"enum": ["ready", "needs-work", "blocked"]},
            "summary": {"type": "string", "minLength": 1},
            "input_artifacts": {
                "type": "array",
                "minItems": 1,
                "items": {"$ref": "#/$defs/artifact"},
            },
            "output_artifacts": {
                "type": "array",
                "minItems": 1,
                "items": {"$ref": "#/$defs/artifact"},
            },
            "changed_paths": {"type": "array", "items": {"type": "string"}},
            "decisions": {"type": "array", "items": {"type": "string"}},
            "gate_results": {
                "type": "array",
                "minItems": 1,
                "items": {
                    "type": "object",
                    "additionalProperties": False,
                    "required": ["command", "status", "exit_code", "evidence"],
                    "properties": {
                        "command": {"type": "string", "minLength": 1},
                        "status": {"enum": ["passed", "failed", "not-run"]},
                        "exit_code": {"type": ["integer", "null"]},
                        "evidence": {"type": "string", "minLength": 1},
                    },
                },
            },
            "blockers": {"type": "array", "items": {"type": "string"}},
            "risks": {"type": "array", "items": {"type": "string"}},
            "next_action": {"type": "string", "minLength": 1},
        },
        "$defs": {
            "artifact": {
                "type": "object",
                "additionalProperties": False,
                "required": ["path", "sha256"],
                "properties": {
                    "path": {"type": "string", "minLength": 1},
                    "sha256": {"type": "string", "pattern": "^[a-f0-9]{64}$"},
                },
            }
        },
    }


def team_runbook(artifact_dir: str = "design-system") -> str:
    return f"""# Design Ontology Agent Team

This repository uses one shared team contract for Codex and Claude Code. The models may differ; role ownership, handoffs, artifacts, and release gates do not.

## Start here

1. Read `{artifact_dir}/agent-team.json`.
2. Ask the team lead to identify the first missing stage output.
3. Dispatch only that stage owner.
4. Save every stage transition under `{artifact_dir}/handoffs/` using `handoff.schema.json`.
5. Stop on a failed gate. Never route around it by changing the success criteria.

## Runtime entry points

### Codex

Install the generated local plugin once, then start with the orchestrator skill:

```bash
codex plugin marketplace add .
codex plugin add design-system-harness --marketplace local-plugins
codex 'Use $design-ontology-team-orchestrator to inspect the current project and run the next required stage.'
```

### Claude Code

Start the generated team lead directly:

```bash
claude --agent design-team-lead
```

Then ask: `Inspect {artifact_dir}/agent-team.json and run the next required stage.`

## Team operating rule

The team is a gated pipeline, not a panel of agents all editing at once. The lead dispatches the minimum role set. Read-only research may run in parallel. The only parallel writers are the Token Curator and Component Contract Author after their files are separated. Visual asset production finishes before UI implementation starts. After implementation freeze, the Approved-Reference Fidelity Auditor runs before Production QA. A failed fidelity gate returns to the UI Implementer with a correction brief; it never changes the approved contract.

The Token Curator reads the checksum-verified Semantic OS graph embedded in `docs/color-reference.md`. It owns `color_reference` and `font_system` in the project profile. The Component Contract Author writes a separate `design-system/component-contracts.json`, so those two roles can run safely in parallel after the Brief Author reserves `component_decision_path`.

When raster generation is needed, the Visual Asset Producer prefers Codex `image_gen`. A Claude Code run may prepare the prompt packet and review criteria, but if no image tool is available it must hand generation to Codex and keep the asset gate open.

## Release sequence

```bash
uv run design-ontology validate-component-contracts --project-dir <project>
uv run design-ontology emit-tokens --project-dir <project>
uv run design-ontology lint-implementation --target-repo <implementation-repo>
uv run design-ontology check-style-divergence --project-dir <implementation-repo> --register-on-pass
uv run design-ontology reference-fidelity-loop --project-dir <project> --target-repo <implementation-repo> --review-artifact <paired-review.json>
uv run design-ontology verify-production-ui --project-dir <project> --target-repo <implementation-repo>
```

Only the release governor may report production readiness, and only after the final command passes against current runtime evidence.
"""


def team_skill(artifact_dir: str = "design-system") -> str:
    return f"""---
name: design-ontology-team-orchestrator
description: Coordinate the complete design-ontology harness team from product brief through production verification. Use when starting or resuming a harness project, assigning specialist agents, choosing the next stage, writing handoffs, recovering from a failed gate, or operating the same workflow in Codex and Claude Code.
---

# Design Ontology Team Orchestrator

Read `{artifact_dir}/agent-team.json` and `{artifact_dir}/TEAM_RUNBOOK.md` before dispatching work.

1. Inspect current artifacts and gate evidence.
2. Select the earliest incomplete stage.
3. Dispatch only its owner; parallelize only read-only research or the file-separated token/component pair.
4. Require the owner to return changed paths, decisions, gate commands, results, and remaining risks.
5. Write a schema-valid handoff to `{artifact_dir}/handoffs/` before changing stage owner.
6. On gate failure, return work to the same owner with the failed evidence. Do not weaken the gate.
7. After implementation freeze, require the reference fidelity stage before Production QA. A failed paired review returns to implementation with fresh correction evidence.
8. Finish only when the release governor independently runs `verify-production-ui` successfully.

Never let the lead silently perform specialist implementation or let implementation start while component contracts are `needs-authoring`. Read colors from the synchronized Semantic OS graph in `docs/color-reference.md`, not from screenshots. Use Codex `image_gen` for required raster generation; a runtime without an image tool must write a handoff instead of claiming the asset exists. Approved references can govern only explicitly authored composition, morphology, density, hierarchy, task-visibility, responsive-translation, and context-linkage invariants; they never govern palette, typography, IA, copy, logos, or redistributable assets.
"""


def claude_team_lead_agent(artifact_dir: str = "design-system") -> str:
    return f"""---
name: design-team-lead
description: Orchestrates the design-ontology team, assigns only the next required specialist, records handoffs, and enforces release gates.
tools: Read, Glob, Grep, Bash, Edit, Write, Agent
model: opus
color: blue
---

You are the Design Ontology Team Lead.

Read `{artifact_dir}/agent-team.json` and `{artifact_dir}/TEAM_RUNBOOK.md` first. Inspect evidence, choose the earliest incomplete stage, and delegate it to the matching `.claude/agents` specialist. Do not duplicate specialist work. Do not run overlapping write agents. Record every transition under `{artifact_dir}/handoffs/` using the schema. A failed gate returns to the same owner. Only delegate the final completion audit to `design-release-governor`, and never claim readiness unless `verify-production-ui` passes against current evidence.
"""


def claude_specialist_agent(role_id: str, artifact_dir: str = "design-system") -> str:
    role = next(item for item in team_contract(artifact_dir)["roles"] if item["id"] == role_id)
    tools = "Read, Glob, Grep, Bash, Write" if role_id in {"reference-fidelity-auditor", "production-qa", "release-governor"} else "Read, Glob, Grep, Bash, Edit, Write"
    model = "opus" if role_id in {"brief-author", "visual-asset-producer", "release-governor"} else "sonnet"
    workflow = role.get("workflow_skills", {}).get("claude")
    workflow_line = (
        f"Follow `.claude/skills/{workflow}/SKILL.md` for the detailed workflow. " if workflow else ""
    )
    commands = role.get("required_commands", [])
    command_line = f"Required checks: {'; '.join(commands)}. " if commands else ""
    return f"""---
name: design-{role_id}
description: {role['title']} for the shared design-ontology team contract.
tools: {tools}
model: {model}
color: green
---

You are the {role['title']}.

Read `{artifact_dir}/agent-team.json` and the latest file under `{artifact_dir}/handoffs/` before acting. {workflow_line}Own only: {', '.join(role['owns'])}. Write only: {', '.join(role['writes'])}. Do not: {'; '.join(role['must_not'])}. {command_line}Exit only when: {role['exit_when']} Return changed paths, decisions, exact gate commands and results, risks, and a proposed next action. Do not change stage ownership yourself; the team lead writes the handoff.
"""


def codex_specialist_skill(role_id: str, artifact_dir: str = "design-system") -> str:
    role = next(item for item in team_contract(artifact_dir)["roles"] if item["id"] == role_id)
    workflow = role.get("workflow_skills", {}).get("codex")
    workflow_line = f"- Follow `${workflow}` for the detailed harness workflow.\n" if workflow else ""
    commands = role.get("required_commands", [])
    command_lines = "".join(f"  - `{command}`\n" for command in commands)
    checks_section = f"- Required checks:\n{command_lines}" if commands else ""
    browser_section = ""
    if role_id == "production-qa":
        browser_section = """## Codex Desktop in-app Browser evidence

1. Load and follow the installed `browser:browser` skill before the first browser action. Select the `iab` browser, give the run one stable session name, and reuse that browser session and tab handles for the complete QA matrix.
2. Test the frozen local runtime in the actual in-app Browser. Use `tab.screenshot(...)` for fresh desktop/mobile and light/dark captures, `tab.playwright.domSnapshot()` after navigation or state changes, scoped `tab.playwright.evaluate(...)` for visible state and document/body overflow measurements, and `tab.dev.logs(...)` for console output. Exercise pointer and keyboard/focus behavior through the Browser locators, then record WCAG-oriented DOM findings. Preserve the raw values returned by these calls.
3. Save the unedited observations under `build/system/production/browser-observations/` using `production-browser-observation/v1`. Every record must include the real Browser session id, this QA agent run id, observation timestamp, current runtime-tree SHA-256, and producer metadata for `codex-desktop-in-app-browser` / `in-app-browser` / `browser:browser`.
4. Register every screenshot with `record-screenshot-evidence`. Then write project evidence at `build/system/production/browser-evidence-bundle.json` using `production-browser-evidence-bundle/v1`. Bind the hashed screenshot manifest, every hashed raw observation, and the hashed v1 component-runtime manifest/evidence to the same session and current runtime tree.
5. Run `verify-production-ui --browser-evidence-bundle <path>`. `production-ui-runtime-check/v1` narrative `passed=true` files are legacy-unverified and cannot replace raw browser observations. If the IAB backend cannot capture a required viewport or observation, keep the gate blocked and report the missing capability.

The Python harness validates and ingests these files only. It does not launch, control, or attest the privileged Codex Desktop in-app Browser, so never describe a Python or shell-only run as browser evidence.
"""
    elif role_id == "reference-fidelity-auditor":
        browser_section = """## Paired approved-reference review

1. Inspect the immutable reference-fidelity contract, its authored brief evidence, and every approved reference SHA before looking at the implementation.
2. Compare the approved reference and fresh candidate screenshots side by side with a multimodal-capable reviewer. Score only contract metrics for composition, morphology, density, hierarchy, task visibility, responsive translation, and context linkage.
3. Never score palette, typography, information architecture, product copy, logos, or redistributable assets by similarity. Semantic OS and authored product artifacts remain authoritative.
4. Bind the review artifact to the current runtime-tree SHA, every candidate screenshot SHA, every approved reference SHA, and the contract SHA. Run `reference-fidelity-loop`.
5. If blocked, return the generated correction brief to UI Implementer. The next iteration must have a new runtime-tree SHA and fresh screenshot SHA set. If the runtime cannot perform paired multimodal review, hand the stage to Codex and keep the gate blocked.
"""
    return f"""---
name: design-{role_id}
description: Act as the {role['title']} in the shared design-ontology team. Use when the team lead assigns this role or when the current stage specifically needs {', '.join(role['owns'])}.
---

# {role['title']}

Read `{artifact_dir}/agent-team.json` and the latest file under `{artifact_dir}/handoffs/` before acting.

{workflow_line}- Own only: {', '.join(role['owns'])}.
- Write only: {', '.join(role['writes'])}.
- Do not: {'; '.join(role['must_not'])}.
{checks_section}
{browser_section}
- Exit only when: {role['exit_when']}
- Return changed paths, decisions, exact gate commands/results, remaining risks, and the proposed next action.
- Do not change stage ownership or declare production readiness; the Team Lead and Release Governor own those decisions.
"""


def codex_skill_openai_yaml(role_id: str | None = None) -> str:
    if role_id is None:
        return """interface:
  display_name: "Design Ontology Team"
  short_description: "Coordinate a verified design-system agent team"
  default_prompt: "Use $design-ontology-team-orchestrator to run the next incomplete harness stage."
"""
    role = next(item for item in team_contract()["roles"] if item["id"] == role_id)
    display_name = role["title"].replace('"', "'")
    return f"""interface:
  display_name: "{display_name}"
  short_description: "Run the {role_id} stage with evidence"
  default_prompt: "Use $design-{role_id} for the assigned team stage and return gate evidence."
"""


def codex_conditional_skill(specialist_id: str, artifact_dir: str = "design-system") -> str:
    specialist = next(
        item for item in team_contract(artifact_dir)["conditional_specialists"] if item["id"] == specialist_id
    )
    skill_name = CONDITIONAL_CODEX_SKILLS[specialist_id]
    boundaries = {
        "reference-inspector": (
            "Extract only morphology, density, hierarchy, and interaction affordances. Never copy palette, typography, "
            "information architecture, product copy, logos, or unlicensed assets."
        ),
        "ui-refactor": (
            "Preserve routes, content, features, layout structure, and behavior. Bind the existing UI to approved "
            "tokens and component contracts; use $design-system-implementer for the detailed workflow."
        ),
        "ui-rebuild": (
            "Proceed only with explicit user approval and completed concept/component gates. Rebuild from the new "
            "ontology and contracts, not from the old screen or an advisory reference."
        ),
    }
    return f"""---
name: {skill_name}
description: Conditional specialist for the shared design-ontology team. Use when {specialist['use_when']}
---

# {specialist_id.replace('-', ' ').title()}

Read `{artifact_dir}/agent-team.json` and the latest file under `{artifact_dir}/handoffs/` before acting. {boundaries[specialist_id]}

Return findings or changed paths, evidence, risks, and the next action to {specialist['returns_to']}. Do not change stage ownership or declare production readiness.
"""


def scaffold_shared_team(
    target_repo: Path,
    artifact_dir: str,
    targets: list[str],
    force: bool,
    created: list[str],
) -> None:
    artifact_root = target_repo / artifact_dir
    _write_if_allowed(artifact_root / "agent-team.json", json.dumps(team_contract(artifact_dir), ensure_ascii=False, indent=2) + "\n", force, created)
    _write_if_allowed(artifact_root / "TEAM_RUNBOOK.md", team_runbook(artifact_dir), force, created)
    _write_if_allowed(artifact_root / "handoffs" / "handoff.schema.json", json.dumps(handoff_schema(), ensure_ascii=False, indent=2) + "\n", force, created)
    _write_if_allowed(artifact_root / "handoffs" / ".gitkeep", "", force, created)

    if "codex" in targets:
        skill_dir = target_repo / "plugins" / "design-system-harness" / "skills" / "design-ontology-team-orchestrator"
        _write_if_allowed(skill_dir / "SKILL.md", team_skill(artifact_dir), force, created)
        _write_if_allowed(skill_dir / "agents" / "openai.yaml", codex_skill_openai_yaml(), force, created)
        codex_skills_dir = target_repo / "plugins" / "design-system-harness" / "skills"
        for role_id in ROLE_ORDER[1:]:
            role_dir = codex_skills_dir / f"design-{role_id}"
            _write_if_allowed(role_dir / "SKILL.md", codex_specialist_skill(role_id, artifact_dir), force, created)
            _write_if_allowed(role_dir / "agents" / "openai.yaml", codex_skill_openai_yaml(role_id), force, created)
        for specialist_id, skill_name in CONDITIONAL_CODEX_SKILLS.items():
            if specialist_id == "reference-inspector":
                continue
            specialist_dir = codex_skills_dir / skill_name
            _write_if_allowed(
                specialist_dir / "SKILL.md",
                codex_conditional_skill(specialist_id, artifact_dir),
                force,
                created,
            )
    if "claude" in targets:
        agents_dir = target_repo / ".claude" / "agents"
        skill_dir = target_repo / ".claude" / "skills" / "design-ontology-team-orchestrator"
        _write_if_allowed(skill_dir / "SKILL.md", team_skill(artifact_dir), force, created)
        _write_if_allowed(agents_dir / "design-team-lead.md", claude_team_lead_agent(artifact_dir), force, created)
        for role_id in ROLE_ORDER[1:]:
            _write_if_allowed(agents_dir / f"design-{role_id}.md", claude_specialist_agent(role_id, artifact_dir), force, created)


def _handoff_created_at_order(payload: dict[str, Any]) -> datetime:
    earliest = datetime.min.replace(tzinfo=timezone.utc)
    created_at = payload.get("created_at")
    if not isinstance(created_at, str) or not created_at.strip():
        return earliest
    try:
        parsed_created_at = datetime.fromisoformat(created_at.replace("Z", "+00:00"))
    except ValueError:
        return earliest
    if parsed_created_at.tzinfo is None:
        return earliest
    return parsed_created_at.astimezone(timezone.utc)


def _validate_handoff_directory(target_repo: Path, handoff_dir: Path) -> list[str]:
    errors: list[str] = []
    repo_root = target_repo.resolve()
    latest_artifacts: dict[
        str,
        tuple[tuple[datetime, str, int], Path, str, int, Any, str],
    ] = {}

    for handoff_path in sorted(handoff_dir.glob("*.json")):
        if handoff_path.name == "handoff.schema.json":
            continue
        relative_handoff = handoff_path.relative_to(target_repo).as_posix()
        try:
            payload = json.loads(handoff_path.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            errors.append(f"invalid handoff JSON {relative_handoff}: {exc}")
            continue

        errors.extend(
            f"invalid handoff {relative_handoff}: {issue}"
            for issue in validate_handoff_payload(payload)
        )
        if not isinstance(payload, dict):
            continue

        created_at_order = _handoff_created_at_order(payload)
        occurrence_order = 0
        for field in ("input_artifacts", "output_artifacts"):
            artifacts = payload.get(field)
            if not isinstance(artifacts, list):
                continue
            for index, artifact in enumerate(artifacts):
                current_occurrence = occurrence_order
                occurrence_order += 1
                if not isinstance(artifact, dict):
                    continue
                path = artifact.get("path")
                digest = artifact.get("sha256")
                if not isinstance(path, str) or not path.strip():
                    continue

                artifact_path = (repo_root / path).resolve()
                if not artifact_path.is_relative_to(repo_root):
                    errors.append(
                        f"invalid handoff {relative_handoff}: "
                        f"{field}[{index}].path escapes the target repository"
                    )
                    continue

                canonical_path = artifact_path.relative_to(repo_root).as_posix()
                order_key = (created_at_order, relative_handoff, current_occurrence)
                previous = latest_artifacts.get(canonical_path)
                if previous is None or order_key > previous[0]:
                    latest_artifacts[canonical_path] = (
                        order_key,
                        artifact_path,
                        field,
                        index,
                        digest,
                        relative_handoff,
                    )

    for canonical_path in sorted(latest_artifacts):
        _, artifact_path, field, index, digest, relative_handoff = latest_artifacts[canonical_path]
        if not artifact_path.is_file():
            errors.append(
                f"invalid handoff {relative_handoff}: "
                f"{field}[{index}].path does not exist: {canonical_path}"
            )
        elif isinstance(digest, str) and re.fullmatch(r"[a-f0-9]{64}", digest):
            current_digest = sha256(artifact_path.read_bytes()).hexdigest()
            if current_digest != digest:
                errors.append(
                    f"invalid handoff {relative_handoff}: "
                    f"{field}[{index}].sha256 does not match current file: {canonical_path}"
                )

    return errors


def validate_agent_team(target_repo: Path, artifact_dir: str = "design-system", targets: list[str] | None = None) -> dict[str, Any]:
    targets = targets or ["codex", "claude"]
    errors: list[str] = []
    expected_contract = team_contract(artifact_dir)
    unsupported_targets = sorted(set(targets) - {"codex", "claude"})
    if unsupported_targets:
        errors.append("unsupported targets: " + ", ".join(unsupported_targets))
    required = [
        target_repo / artifact_dir / "agent-team.json",
        target_repo / artifact_dir / "TEAM_RUNBOOK.md",
        target_repo / artifact_dir / "handoffs" / "handoff.schema.json",
    ]
    if "codex" in targets:
        codex_workflow_skills = sorted(
            {
                role["workflow_skills"]["codex"]
                for role in expected_contract["roles"]
                if role.get("workflow_skills", {}).get("codex")
            }
        )
        required.extend([
            target_repo / "plugins" / "design-system-harness" / "skills" / "design-ontology-team-orchestrator" / "SKILL.md",
            target_repo / "plugins" / "design-system-harness" / "skills" / "design-ontology-team-orchestrator" / "agents" / "openai.yaml",
            *[
                target_repo / "plugins" / "design-system-harness" / "skills" / f"design-{role}" / "SKILL.md"
                for role in ROLE_ORDER[1:]
            ],
            *[
                target_repo / "plugins" / "design-system-harness" / "skills" / f"design-{role}" / "agents" / "openai.yaml"
                for role in ROLE_ORDER[1:]
            ],
            *[
                target_repo / "plugins" / "design-system-harness" / "skills" / skill_name / "SKILL.md"
                for skill_name in CONDITIONAL_CODEX_SKILLS.values()
            ],
            *[
                target_repo / "plugins" / "design-system-harness" / "skills" / skill_name / "SKILL.md"
                for skill_name in codex_workflow_skills
            ],
        ])
    if "claude" in targets:
        claude_workflow_skills = sorted(
            {
                role["workflow_skills"]["claude"]
                for role in expected_contract["roles"]
                if role.get("workflow_skills", {}).get("claude")
            }
        )
        required.extend([
            target_repo / ".claude" / "skills" / "design-ontology-team-orchestrator" / "SKILL.md",
            target_repo / ".claude" / "agents" / "design-team-lead.md",
            *[target_repo / ".claude" / "agents" / f"design-{role}.md" for role in ROLE_ORDER[1:]],
            *[
                target_repo / ".claude" / "agents" / filename
                for filename in CONDITIONAL_CLAUDE_AGENTS.values()
            ],
            *[
                target_repo / ".claude" / "skills" / skill_name / "SKILL.md"
                for skill_name in claude_workflow_skills
            ],
        ])
    for path in required:
        if not path.is_file():
            errors.append(f"missing: {path.relative_to(target_repo)}")

    if "codex" in targets:
        for role in ROLE_ORDER[1:]:
            path = target_repo / "plugins" / "design-system-harness" / "skills" / f"design-{role}" / "SKILL.md"
            if path.is_file():
                text = path.read_text(encoding="utf-8")
                if any(
                    required_text not in text
                    for required_text in (
                        f"name: design-{role}",
                        f"{artifact_dir}/agent-team.json",
                        f"{artifact_dir}/handoffs/",
                    )
                ):
                    errors.append(f"invalid Codex role adapter: {path.relative_to(target_repo)}")
        for specialist_id, skill_name in CONDITIONAL_CODEX_SKILLS.items():
            path = target_repo / "plugins" / "design-system-harness" / "skills" / skill_name / "SKILL.md"
            if path.is_file():
                text = path.read_text(encoding="utf-8")
                if any(
                    required_text not in text
                    for required_text in (
                        f"name: {skill_name}",
                        f"{artifact_dir}/agent-team.json",
                        f"{artifact_dir}/handoffs/",
                    )
                ):
                    errors.append(
                        f"invalid Codex conditional adapter for {specialist_id}: {path.relative_to(target_repo)}"
                    )
    if "claude" in targets:
        lead_path = target_repo / ".claude" / "agents" / "design-team-lead.md"
        if lead_path.is_file():
            lead_text = lead_path.read_text(encoding="utf-8")
            if "name: design-team-lead" not in lead_text or f"{artifact_dir}/agent-team.json" not in lead_text:
                errors.append(f"invalid Claude team lead adapter: {lead_path.relative_to(target_repo)}")
        for role in ROLE_ORDER[1:]:
            path = target_repo / ".claude" / "agents" / f"design-{role}.md"
            if path.is_file():
                text = path.read_text(encoding="utf-8")
                if any(
                    required_text not in text
                    for required_text in (
                        f"name: design-{role}",
                        f"{artifact_dir}/agent-team.json",
                        f"{artifact_dir}/handoffs/",
                    )
                ):
                    errors.append(f"invalid Claude role adapter: {path.relative_to(target_repo)}")
        for specialist_id, filename in CONDITIONAL_CLAUDE_AGENTS.items():
            path = target_repo / ".claude" / "agents" / filename
            if path.is_file():
                text = path.read_text(encoding="utf-8")
                if any(
                    required_text not in text
                    for required_text in (
                        f"name: {filename.removesuffix('.md')}",
                        f"{artifact_dir}/agent-team.json",
                        f"{artifact_dir}/handoffs/",
                    )
                ):
                    errors.append(
                        f"invalid Claude conditional adapter for {specialist_id}: {path.relative_to(target_repo)}"
                    )

    contract_path = target_repo / artifact_dir / "agent-team.json"
    if contract_path.is_file():
        try:
            contract = json.loads(contract_path.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            errors.append(f"invalid agent-team.json: {exc}")
        else:
            if contract.get("schema_version") != TEAM_SCHEMA_VERSION:
                errors.append(f"unsupported schema_version: {contract.get('schema_version')}")
            if contract.get("artifact_dir") != artifact_dir:
                errors.append(
                    f"artifact_dir mismatch: expected {artifact_dir}, got {contract.get('artifact_dir')}"
                )
            role_ids = [role.get("id") for role in contract.get("roles", []) if isinstance(role, dict)]
            if role_ids != list(ROLE_ORDER):
                errors.append("role order or coverage differs from the shared runtime contract")
            for role in contract.get("roles", []):
                if not isinstance(role, dict):
                    continue
                missing_role_fields = [
                    field for field in ("owns", "writes", "must_not", "exit_when") if not role.get(field)
                ]
                if missing_role_fields:
                    errors.append(
                        f"role {role.get('id', '<unknown>')} missing operating fields: "
                        + ", ".join(missing_role_fields)
                    )
            owners = {stage.get("owner") for stage in contract.get("stages", []) if isinstance(stage, dict)}
            missing_owners = sorted(owners - set(role_ids))
            if missing_owners:
                errors.append("stage owners missing from roles: " + ", ".join(missing_owners))

    schema_path = target_repo / artifact_dir / "handoffs" / "handoff.schema.json"
    if schema_path.is_file():
        try:
            generated_schema = json.loads(schema_path.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            errors.append(f"invalid handoff.schema.json: {exc}")
        else:
            if generated_schema != handoff_schema():
                errors.append("handoff.schema.json differs from the current shared contract")

    handoff_dir = target_repo / artifact_dir / "handoffs"
    if handoff_dir.is_dir():
        errors.extend(_validate_handoff_directory(target_repo, handoff_dir))

    return {
        "ok": not errors,
        "schema_version": TEAM_SCHEMA_VERSION,
        "target_repo": str(target_repo),
        "artifact_dir": artifact_dir,
        "targets": targets,
        "role_count": len(ROLE_ORDER),
        "errors": errors,
    }


def validate_handoff_payload(payload: Any, target_repo: Path | None = None) -> list[str]:
    schema = handoff_schema()
    if not isinstance(payload, dict):
        return ["root must be an object"]

    errors: list[str] = []
    required = schema["required"]
    missing = [key for key in required if key not in payload]
    if missing:
        errors.append("missing required fields: " + ", ".join(missing))

    unexpected = sorted(set(payload) - set(schema["properties"]))
    if unexpected:
        errors.append("unexpected fields: " + ", ".join(unexpected))

    if payload.get("schema_version") != HANDOFF_SCHEMA_VERSION:
        errors.append(f"schema_version must be {HANDOFF_SCHEMA_VERSION}")
    if payload.get("from_role") not in ROLE_ORDER:
        errors.append("from_role is not a core team role")
    if payload.get("to_role") not in ROLE_ORDER:
        errors.append("to_role is not a core team role")
    if payload.get("stage") not in STAGE_ORDER:
        errors.append("stage is not recognized")
    if payload.get("status") not in {"ready", "needs-work", "blocked"}:
        errors.append("status is not recognized")

    from_role = payload.get("from_role")
    to_role = payload.get("to_role")
    stage = payload.get("stage")
    if from_role in ROLE_ORDER and to_role in ROLE_ORDER and stage in STAGE_ORDER:
        if from_role == to_role:
            errors.append("from_role and to_role must differ")
        stage_roles = STAGE_SPECIALISTS[stage]
        lead_transition = (
            from_role == "team-lead" and to_role in stage_roles
        ) or (
            to_role == "team-lead" and from_role in stage_roles
        )
        direct_transition = (from_role, to_role) in DIRECT_STAGE_TRANSITIONS[stage]
        if not lead_transition and not direct_transition:
            errors.append(
                f"roles {from_role} -> {to_role} are not an allowed transition for stage {stage}"
            )

    for field in ("run_id", "created_at", "project", "summary", "next_action"):
        value = payload.get(field)
        if not isinstance(value, str) or not value.strip():
            errors.append(f"{field} must be a non-empty string")

    created_at = payload.get("created_at")
    if isinstance(created_at, str) and created_at.strip():
        try:
            parsed_created_at = datetime.fromisoformat(created_at.replace("Z", "+00:00"))
        except ValueError:
            errors.append("created_at must be an ISO 8601 date-time")
        else:
            if parsed_created_at.tzinfo is None:
                errors.append("created_at must include a timezone")

    for field in ("input_artifacts", "output_artifacts"):
        value = payload.get(field)
        if not isinstance(value, list):
            errors.append(f"{field} must be an array")
            continue
        if not value:
            errors.append(f"{field} must contain at least one hashed artifact")
        for index, artifact in enumerate(value):
            if not isinstance(artifact, dict):
                errors.append(f"{field}[{index}] must be an object")
                continue
            unexpected_artifact = sorted(set(artifact) - {"path", "sha256"})
            if unexpected_artifact:
                errors.append(
                    f"{field}[{index}] has unexpected fields: {', '.join(unexpected_artifact)}"
                )
            path = artifact.get("path")
            if not isinstance(path, str) or not path.strip():
                errors.append(f"{field}[{index}].path must be a non-empty string")
            digest = artifact.get("sha256")
            if not isinstance(digest, str) or re.fullmatch(r"[a-f0-9]{64}", digest) is None:
                errors.append(f"{field}[{index}].sha256 must be a lowercase SHA-256 digest")
            if target_repo is not None and isinstance(path, str) and path.strip():
                repo_root = target_repo.resolve()
                artifact_path = (repo_root / path).resolve()
                if not artifact_path.is_relative_to(repo_root):
                    errors.append(f"{field}[{index}].path escapes the target repository")
                elif not artifact_path.is_file():
                    errors.append(f"{field}[{index}].path does not exist: {path}")
                elif isinstance(digest, str) and re.fullmatch(r"[a-f0-9]{64}", digest):
                    current_digest = sha256(artifact_path.read_bytes()).hexdigest()
                    if current_digest != digest:
                        errors.append(f"{field}[{index}].sha256 does not match current file: {path}")

    for field in ("changed_paths", "decisions", "blockers", "risks"):
        value = payload.get(field)
        if not isinstance(value, list) or any(not isinstance(item, str) for item in value):
            errors.append(f"{field} must be an array of strings")

    gate_results = payload.get("gate_results")
    if not isinstance(gate_results, list):
        errors.append("gate_results must be an array")
    else:
        if not gate_results:
            errors.append("gate_results must contain at least one reproducible gate result")
        for index, gate in enumerate(gate_results):
            if not isinstance(gate, dict):
                errors.append(f"gate_results[{index}] must be an object")
                continue
            required_gate = {"command", "status", "exit_code", "evidence"}
            missing_gate = sorted(required_gate - set(gate))
            if missing_gate:
                errors.append(
                    f"gate_results[{index}] missing fields: {', '.join(missing_gate)}"
                )
            unexpected_gate = sorted(set(gate) - required_gate)
            if unexpected_gate:
                errors.append(
                    f"gate_results[{index}] has unexpected fields: {', '.join(unexpected_gate)}"
                )
            if not isinstance(gate.get("command"), str) or not gate.get("command", "").strip():
                errors.append(f"gate_results[{index}].command must be a non-empty string")
            if gate.get("status") not in {"passed", "failed", "not-run"}:
                errors.append(f"gate_results[{index}].status is not recognized")
            exit_code = gate.get("exit_code")
            if exit_code is not None and not isinstance(exit_code, int):
                errors.append(f"gate_results[{index}].exit_code must be an integer or null")
            if gate.get("status") == "passed" and exit_code != 0:
                errors.append(f"gate_results[{index}] passed status requires exit_code 0")
            if gate.get("status") == "failed" and (not isinstance(exit_code, int) or exit_code == 0):
                errors.append(f"gate_results[{index}] failed status requires a non-zero exit_code")
            if gate.get("status") == "not-run" and exit_code is not None:
                errors.append(f"gate_results[{index}] not-run status requires exit_code null")
            if not isinstance(gate.get("evidence"), str) or not gate.get("evidence", "").strip():
                errors.append(f"gate_results[{index}].evidence must be a non-empty string")

        statuses = {
            gate.get("status") for gate in gate_results if isinstance(gate, dict)
        }
        status = payload.get("status")
        if status == "ready" and (statuses != {"passed"}):
            errors.append("ready handoff requires all recorded gates to be passed")
        if status == "needs-work" and "failed" not in statuses:
            errors.append("needs-work handoff requires at least one failed gate")

    blockers = payload.get("blockers")
    if payload.get("status") == "blocked" and isinstance(blockers, list) and not blockers:
        errors.append("blocked handoff requires at least one blocker")
    if payload.get("status") == "ready" and isinstance(blockers, list) and blockers:
        errors.append("ready handoff cannot contain blockers")

    return errors


def _write_if_allowed(path: Path, content: str, force: bool, created: list[str]) -> None:
    if path.exists() and not force:
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")
    created.append(str(path))
