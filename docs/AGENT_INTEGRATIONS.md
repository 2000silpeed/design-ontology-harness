# Agent Integrations

## Goal

이 프레임워크는 KB와 디자인 시스템 산출물을 만드는 데서 끝나지 않고, 실제 구현 저장소에서 바로 사용할 수 있는 Codex / Claude Code 에이전트 설정까지 스캐폴드할 수 있습니다.

## Supported Targets

### Codex

생성 위치:

- `plugins/design-system-harness/.codex-plugin/plugin.json`
- `plugins/design-system-harness/skills/design-system-architect/SKILL.md`
- `plugins/design-system-harness/skills/design-system-implementer/SKILL.md`
- `.agents/plugins/marketplace.json`

용도:

- 로컬 Codex plugin bundle
- implementation repo에서 system artifacts를 읽는 skill 제공

### Claude Code

생성 위치:

- `.claude/skills/design-system-architect/SKILL.md`
- `.claude/skills/design-system-implement/SKILL.md`
- `.claude/agents/design-system-architect.md`
- `.claude/agents/design-system-implementer.md`

용도:

- project-level skills
- project-level subagents

Claude Code 공식 문서 기준으로 project skills는 `.claude/skills/<skill-name>/SKILL.md`, project subagents는 `.claude/agents/*.md` 위치를 사용합니다.

References:

- Claude Code skills: [code.claude.com/docs/en/slash-commands](https://code.claude.com/docs/en/slash-commands)
- Claude Code subagents: [code.claude.com/docs/en/sub-agents](https://code.claude.com/docs/en/sub-agents)

## Scaffold Command

```bash
uv run design-ontology init-agent-pack \
  --target-repo /path/to/implementation-repo \
  --artifact-dir design-system \
  --targets codex,claude
```

The generated Codex plugin manifest intentionally works without a public homepage or repository URL.
If you later publish your own repo, you can fill those values in then.

## Expected Artifact Sync

The generated skills and agents expect these files inside the implementation repo:

- `design-system/system_spec.md`
- `design-system/token_schema.json`
- `design-system/component_inventory.json`
- `design-system/system_ontology.json`

You should sync them from a harness project output such as:

- `build/system/blueprint/system_spec.md`
- `build/system/blueprint/token_schema.json`
- `build/system/blueprint/component_inventory.json`
- `build/system/blueprint/system_ontology.json`

## Recommended Usage In An Implementation Repo

1. Generate artifacts from the harness project
2. Copy or sync them into `design-system/`
3. Run `init-agent-pack`
4. Use:
   - Codex skills for implementation inside Codex
   - Claude Code skills and subagents inside Claude Code

## Practical Example

In a frontend repo:

- ask the architect skill/agent to map a new screen to component families
- ask the implementer skill/agent to build the screen using existing tokens and primitives
- if the request falls outside the current artifacts, update the harness project first instead of improvising a new system
