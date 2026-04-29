# Agent Integrations

## Goal

이 프레임워크는 KB와 디자인 시스템 산출물을 만드는 데서 끝나지 않고, 실제 구현 저장소에서 바로 사용할 수 있는 Codex / Claude Code 에이전트 설정까지 스캐폴드할 수 있습니다.

중요한 포지션 정리:

- 이 저장소의 본체는 GitHub에서 clone해서 쓰는 하네스 코어입니다.
- Codex / Claude Code integration은 선택적 부가 레이어입니다.
- 즉 이 repo는 "Claude plugin product"라기보다 "plugin-friendly harness"에 가깝습니다.

## Supported Targets

### Codex

생성 위치:

- `plugins/design-system-harness/.codex-plugin/plugin.json`
- `plugins/design-system-harness/skills/design-system-architect/SKILL.md`
- `plugins/design-system-harness/skills/design-system-implementer/SKILL.md`
- `plugins/design-system-harness/skills/design-system-visual-assets/SKILL.md`
- `.agents/plugins/marketplace.json`

용도:

- 로컬 Codex plugin bundle
- implementation repo에서 system artifacts를 읽는 skill 제공
- Codex에서 이미지 생성 기능이 가능할 때 `imagine2` 모델로 브랜드에 맞는 히어로/카드/에디토리얼 이미지를 생성하고 통합하는 visual asset skill 제공

### Claude Code

생성 위치:

- `.claude/skills/design-system-architect/SKILL.md`
- `.claude/skills/design-system-implement/SKILL.md`
- `.claude/agents/design-system-architect.md`
- `.claude/agents/design-system-implementer.md`

용도:

- project-level skills
- project-level subagents

현재 Claude Code 쪽은 설치형 marketplace plugin 패키지보다 project-local 설정 생성에 더 가깝습니다. 즉 바로 `.claude/` 아래에 심어서 쓰는 흐름을 기본으로 합니다.

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

If a curated color reference is connected through the harness project, the generated `system_spec.md` and `token_schema.json` will also carry the active palette, alternative palette candidates, and semantic role hints that agents should follow.

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

If you do not need agent integrations, you can stop at step 2. The harness remains fully useful without any Codex or Claude-specific layer.

## Practical Example

In a frontend repo:

- ask the architect skill/agent to map a new screen to component families
- ask the implementer skill/agent to build the screen using existing tokens and primitives
- in Codex, ask the visual asset skill to generate `imagine2` imagery for hero, empty-state, editorial, or product sections when the screen needs real visual substance
- check `system_ontology.json` for `GeneratedVisualAsset` and `ImageGenerationModel` nodes before treating generated imagery as part of the system contract
- if the request falls outside the current artifacts, update the harness project first instead of improvising a new system

## Codex Visual Asset Workflow

`design-system-visual-assets`는 화면을 더 프로페셔널하게 만들기 위한 선택적 Codex 전용 스킬입니다.
온톨로지에는 `GeneratedVisualAsset` 슬롯과 `ImageGenerationModel`(`imagine2`) 노드가 함께 기록되어, 생성 이미지가 임시 장식이 아니라 브랜드/토큰/컴포넌트 관계에 묶인 산출물로 추적됩니다.

기본 흐름:

1. `design-system/system_spec.md`, `token_schema.json`, `component_inventory.json`, 가능하면 `visual_reference_report.json`을 읽습니다.
2. Codex에서 이미지 생성 모델 선택이 가능하면 `imagine2`를 선택합니다.
3. 브랜드 키워드, 안티 키워드, 팔레트, density/surface cue를 반영해 2-4개 후보 이미지를 만듭니다.
4. 승인한 이미지는 `public/generated/design-system/` 같은 정적 에셋 폴더에 넣고 `manifest.json`에 prompt, model, intended slot, alt text, source artifacts를 기록합니다.
5. 구현 코드에는 기존 프레임워크의 이미지 컴포넌트와 `alt` 텍스트, responsive crop 규칙을 적용합니다.

가드레일:

- 아이콘, 로고, 버튼 glyph, 상태 마커는 이미지 생성 대상이 아닙니다. SVG나 아이콘 라이브러리를 사용합니다.
- 저작권 캐릭터, 실제 브랜드, 실제 인물, 권리가 불분명한 장소는 사용하지 않습니다.
- 이미지 생성 도구가 없으면 생성했다고 말하지 않고 `imagine2-prompts.md` 프롬프트 팩만 남깁니다.

## Refactor Safety Expectation

생성되는 Codex / Claude Code skills는 기본적으로 아래 원칙을 따르도록 설계되어 있습니다.

- 기존 기능과 진입점 보존
- 전체 셸 리라이트보다 점진적 적용
- theme / breakpoint 호환성 유지
- semantic token 우선, 하드코딩 색상 지양

즉 이 integration pack은 "멋있게 다시 만들어라"보다 "기존 제품을 깨지 않으면서 시스템적으로 개선하라"에 더 가깝습니다.
