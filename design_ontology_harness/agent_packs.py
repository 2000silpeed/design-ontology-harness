from __future__ import annotations

import json
from pathlib import Path

from .utils import ensure_dir, write_json


def scaffold_agent_pack(
    target_repo: Path,
    artifact_dir: str = "design-system",
    targets: list[str] | None = None,
    force: bool = False,
) -> dict:
    targets = targets or ["codex", "claude"]
    normalized_targets = sorted({target.strip().lower() for target in targets if target.strip()})
    supported = {"codex", "claude"}
    unsupported = [target for target in normalized_targets if target not in supported]
    if unsupported:
        raise ValueError(f"Unsupported targets: {unsupported}")

    ensure_dir(target_repo)
    created: list[str] = []

    artifact_path = target_repo / artifact_dir
    ensure_dir(artifact_path)
    _write_if_allowed(
        artifact_path / "README.md",
        _artifact_readme(artifact_dir),
        force=force,
        created=created,
    )

    if "claude" in normalized_targets:
        _scaffold_claude_pack(target_repo, artifact_dir, force, created)
    if "codex" in normalized_targets:
        _scaffold_codex_pack(target_repo, artifact_dir, force, created)

    return {
        "target_repo": str(target_repo),
        "artifact_dir": artifact_dir,
        "targets": normalized_targets,
        "created": created,
    }


def _scaffold_claude_pack(target_repo: Path, artifact_dir: str, force: bool, created: list[str]) -> None:
    claude_dir = ensure_dir(target_repo / ".claude")
    skills_dir = ensure_dir(claude_dir / "skills")
    agents_dir = ensure_dir(claude_dir / "agents")

    implement_skill_dir = ensure_dir(skills_dir / "design-system-implement")
    architect_skill_dir = ensure_dir(skills_dir / "design-system-architect")

    _write_if_allowed(
        implement_skill_dir / "SKILL.md",
        _claude_implement_skill(artifact_dir),
        force=force,
        created=created,
    )
    _write_if_allowed(
        architect_skill_dir / "SKILL.md",
        _claude_architect_skill(artifact_dir),
        force=force,
        created=created,
    )
    _write_if_allowed(
        agents_dir / "design-system-architect.md",
        _claude_architect_agent(artifact_dir),
        force=force,
        created=created,
    )
    _write_if_allowed(
        agents_dir / "design-system-implementer.md",
        _claude_implementer_agent(artifact_dir),
        force=force,
        created=created,
    )


def _scaffold_codex_pack(target_repo: Path, artifact_dir: str, force: bool, created: list[str]) -> None:
    plugin_root = ensure_dir(target_repo / "plugins" / "design-system-harness")
    ensure_dir(plugin_root / ".codex-plugin")
    skills_root = ensure_dir(plugin_root / "skills")
    architect_dir = ensure_dir(skills_root / "design-system-architect")
    implementer_dir = ensure_dir(skills_root / "design-system-implementer")
    plugin_agents_dir = ensure_dir(plugin_root / "agents")
    marketplace_dir = ensure_dir(target_repo / ".agents" / "plugins")

    plugin_manifest = {
        "name": "design-system-harness",
        "version": "0.1.0",
        "description": "Skills for applying design-system-harness outputs inside an implementation repository.",
        "author": {
            "name": "Design Ontology Harness",
        },
        "license": "MIT",
        "keywords": [
            "design-system",
            "tokens",
            "ui",
            "codex",
            "skills",
        ],
        "skills": "./skills/",
        "interface": {
            "displayName": "Design System Harness",
            "shortDescription": "Apply design-system artifacts inside a real implementation repo",
            "longDescription": "Provides Codex skills for reading design-system artifacts and implementing tokens, components, and UI changes that stay aligned with your system spec.",
            "developerName": "Design Ontology Harness",
            "category": "Coding",
            "capabilities": ["Interactive", "Write"],
            "defaultPrompt": [
                "Implement UI changes using the local design-system artifacts and component inventory"
            ],
            "screenshots": [],
            "brandColor": "#6B7B8D",
        },
    }

    marketplace = {
        "name": "Local Plugins",
        "interface": {"displayName": "Local Plugins"},
        "plugins": [
            {
                "name": "design-system-harness",
                "source": {
                    "source": "local",
                    "path": "./plugins/design-system-harness",
                },
                "policy": {
                    "installation": "AVAILABLE",
                    "authentication": "ON_INSTALL",
                },
                "category": "Coding",
            }
        ],
    }

    _write_if_allowed(
        plugin_root / ".codex-plugin" / "plugin.json",
        json.dumps(plugin_manifest, ensure_ascii=False, indent=2) + "\n",
        force=force,
        created=created,
    )
    _write_if_allowed(
        architect_dir / "SKILL.md",
        _codex_architect_skill(artifact_dir),
        force=force,
        created=created,
    )
    _write_if_allowed(
        implementer_dir / "SKILL.md",
        _codex_implementer_skill(artifact_dir),
        force=force,
        created=created,
    )
    _write_if_allowed(
        plugin_agents_dir / "openai.yaml",
        _codex_plugin_openai_yaml(),
        force=force,
        created=created,
    )
    _write_if_allowed(
        marketplace_dir / "marketplace.json",
        json.dumps(marketplace, ensure_ascii=False, indent=2) + "\n",
        force=force,
        created=created,
    )


def _artifact_readme(artifact_dir: str) -> str:
    return f"""# Design System Artifacts

Place generated artifacts from `design-ontology-harness` in this directory.

Expected files:

- `system_spec.md`
- `token_schema.json`
- `component_inventory.json`
- `system_ontology.json`

Recommended sync source:

- a harness project output such as `build/system/blueprint/*`

Recommended mapping:

- `build/system/blueprint/system_spec.md` -> `{artifact_dir}/system_spec.md`
- `build/system/blueprint/token_schema.json` -> `{artifact_dir}/token_schema.json`
- `build/system/blueprint/component_inventory.json` -> `{artifact_dir}/component_inventory.json`
- `build/system/blueprint/system_ontology.json` -> `{artifact_dir}/system_ontology.json`
"""


def _claude_architect_skill(artifact_dir: str) -> str:
    return f"""---
name: design-system-architect
description: Align implementation plans and UI decisions with the project's design-system artifacts. Use when deciding token structure, component families, primitives, or rollout order.
allowed-tools: Read Glob Grep Bash
paths:
  - "{artifact_dir}/**"
  - "src/**"
  - "app/**"
  - "components/**"
  - "styles/**"
---

When this skill is active:

1. Read `{artifact_dir}/system_spec.md` first.
2. Read `{artifact_dir}/token_schema.json` and `{artifact_dir}/component_inventory.json`.
3. If present, use `{artifact_dir}/system_ontology.json` to understand relations between principles, token categories, and component families.
4. Translate user requests into:
   - affected principles
   - affected token categories
   - affected component families
   - required implementation order
5. Favor extending existing primitives over inventing new components.
6. Explicitly guard against anti-keywords from the system spec.

If any artifact file is missing, say exactly which file is missing and recommend syncing artifacts from the harness repo before implementation.
"""


def _claude_implement_skill(artifact_dir: str) -> str:
    return f"""---
name: design-system-implement
description: Implement or refactor UI code to match the project's design-system artifacts. Use when building tokens, components, styles, or screens based on the generated design-system outputs.
allowed-tools: Read Glob Grep Bash Edit Write
paths:
  - "{artifact_dir}/**"
  - "src/**"
  - "app/**"
  - "components/**"
  - "styles/**"
---

Before making changes:

1. Read `{artifact_dir}/system_spec.md`.
2. Read `{artifact_dir}/token_schema.json`.
3. Read `{artifact_dir}/component_inventory.json`.

Implementation rules:

- Treat the design-system artifacts as the source of truth.
- Keep implementation aligned with the product's brand keywords and anti-keywords.
- Implement high-priority component families before medium-priority families.
- Reuse or extend primitives before adding net-new components.
- Update nearby documentation or tests when implementation meaningfully changes.

When finishing:

- State which artifact files guided the implementation.
- Mention any gaps between the requested UI and the current system artifacts.
"""


def _claude_architect_agent(artifact_dir: str) -> str:
    return f"""---
name: design-system-architect
description: Design-system planning specialist. Use for token strategy, component architecture, rollout planning, and decisions that must stay aligned with `{artifact_dir}` artifacts.
tools: Read, Glob, Grep, Bash
model: sonnet
color: blue
---

You are a design-system architecture specialist.

Your job is to translate product work into a design-system implementation plan that respects the project's generated artifacts.

Always:

1. Read `{artifact_dir}/system_spec.md` first.
2. Then read `{artifact_dir}/token_schema.json` and `{artifact_dir}/component_inventory.json`.
3. Map the request to:
   - principles
   - token categories
   - component families
   - rollout order
4. Prefer extending existing primitives over introducing new abstractions.
5. Call out conflicts with anti-keywords or missing artifacts.

You are primarily a planning and alignment agent, not an implementation agent.
"""


def _claude_implementer_agent(artifact_dir: str) -> str:
    return f"""---
name: design-system-implementer
description: UI implementation specialist for code changes that must follow the project's design-system artifacts in `{artifact_dir}`.
tools: Read, Glob, Grep, Bash, Edit, Write
model: sonnet
color: green
---

You are a design-system implementation specialist.

Before editing code:

1. Read `{artifact_dir}/system_spec.md`.
2. Read `{artifact_dir}/token_schema.json`.
3. Read `{artifact_dir}/component_inventory.json`.

Implementation rules:

- Keep code aligned with system principles.
- Use the token schema to name and organize variables or theme values.
- Use the component inventory to decide whether to create, extend, or defer a component.
- If the request falls outside the current system artifacts, state the gap clearly instead of inventing an ungrounded pattern.
"""


def _codex_architect_skill(artifact_dir: str) -> str:
    return f"""---
name: design-system-architect
description: Plan token structure, component architecture, and rollout order using the repository's design-system artifacts. Use when the task requires alignment decisions before implementation.
---

# Design System Architect

Use this skill when working on planning or architectural questions related to the local design system.

## Required Inputs

Read these files first when they exist:

- `{artifact_dir}/system_spec.md`
- `{artifact_dir}/token_schema.json`
- `{artifact_dir}/component_inventory.json`
- `{artifact_dir}/system_ontology.json`

## Workflow

1. Identify the relevant principles from `system_spec.md`.
2. Map the request to token categories and component families.
3. Prefer extending an existing primitive over introducing a new abstraction.
4. Call out any conflict with anti-keywords or missing system coverage.
5. Produce a concise implementation plan the coding agent can follow.
"""


def _codex_implementer_skill(artifact_dir: str) -> str:
    return f"""---
name: design-system-implementer
description: Implement UI changes that must follow the repository's design-system artifacts. Use when editing tokens, components, styles, or screens so implementation stays aligned with the generated system.
---

# Design System Implementer

Use this skill when making code changes in the implementation repository.

## Required Inputs

Read these files first when they exist:

- `{artifact_dir}/system_spec.md`
- `{artifact_dir}/token_schema.json`
- `{artifact_dir}/component_inventory.json`

## Implementation Rules

1. Treat the design-system artifacts as the source of truth.
2. Keep implementation aligned with brand keywords and anti-keywords.
3. Implement high-priority families before medium-priority families.
4. Reuse or extend primitives before adding net-new components.
5. Update nearby documentation or tests when behavior or structure changes.

## Output Expectations

- State which artifact files informed the implementation.
- Mention any gap between the requested UI and the current system artifacts.
"""


def _codex_plugin_openai_yaml() -> str:
    return """display_name: Design System Harness
short_description: Apply local design-system artifacts inside implementation repos
default_prompt: Implement UI changes using the design-system artifacts in this repository
"""


def _write_if_allowed(path: Path, content: str, force: bool, created: list[str]) -> None:
    if path.exists() and not force:
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")
    created.append(str(path))
