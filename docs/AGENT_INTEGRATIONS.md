# Agent Integrations

## Goal

이 프레임워크는 KB와 디자인 시스템 산출물을 만드는 데서 끝나지 않고, 실제 구현 저장소에서 바로 사용할 수 있는 Codex / Claude Code 에이전트 설정까지 스캐폴드할 수 있습니다.

중요한 포지션 정리:

- 이 저장소의 본체는 GitHub에서 clone해서 쓰는 하네스 코어입니다.
- Codex / Claude Code integration은 선택적 부가 레이어입니다.
- 즉 이 repo는 "Claude plugin product"라기보다 "plugin-friendly harness"에 가깝습니다.

## AI 도구로 보는 방식

이 하네스는 디자인 시스템 문서를 많이 만드는 도구가 아니라, AI가 구현할 수 있는
계약을 컴파일하는 도구입니다.

```text
brand_profile.json / spec.md / visual references
  -> run-project
  -> system_spec.md / token_schema.json / component_specs.md / system_ontology.json
  -> build-preset
  -> STYLE.md / DESIGN.md / preset manifest
  -> install-preset + init-agent-pack
  -> Codex / Claude Code가 읽는 구현 계약
```

AI 도구로 사용할 때의 역할은 세 가지로 나뉩니다.

| 역할 | 언제 사용 | 핵심 명령 |
|------|-----------|-----------|
| 하네스 관리자 | 새 브랜드나 제품군의 상위 온톨로지를 만들 때 | `run-project`, `build-preset` |
| 구현 repo 사용자 | 이미 만든 프리셋을 앱 코드에 적용할 때 | `install-preset`, `lint-implementation` |
| AI 에이전트 사용자 | Codex/Claude가 계약을 읽고 화면을 고치게 할 때 | `init-agent-pack`, `/design-refactor`, `/design-rebuild` |

즉 에이전트에게 "예쁘게 만들어줘"라고 맡기는 흐름이 아닙니다. 먼저
`design-system/`에 계약을 설치하고, 에이전트가 그 계약을 읽은 뒤 구현하게
만드는 흐름입니다.

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
- Codex의 내장 `image_gen` 스킬이 가능할 때 브랜드에 맞는 히어로/카드/에디토리얼 이미지를 생성하고 통합하는 visual asset skill 제공. 실패해도 CLI/API fallback은 호출하지 않음

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

- `design-system/IMPLEMENTATION_CONTRACT.md`
- `design-system/STYLE.md`
- `design-system/DESIGN.md`
- `design-system/system_spec.md`
- `design-system/token_schema.json`
- `design-system/component_inventory.json`
- `design-system/system_ontology.json`
- `design-system/components/component_specs.md`

If a curated color reference is connected through the harness project, the generated `system_spec.md` and `token_schema.json` will also carry the active palette, alternative palette candidates, and semantic role hints that agents should follow.

The recommended path is to install a preset into the implementation repo:

```bash
uv run design-ontology install-preset \
  --preset-id conversation-copilot--corporate-trust \
  --target-repo /path/to/implementation-repo \
  --adapter raw-css-variables \
  --color-mode light \
  --locale ko
```

This writes the design-system mirror plus `IMPLEMENTATION_CONTRACT.md`, `STYLE.md`, `DESIGN.md`, adapter CSS files, and `INSTALLED.json`.

If you are syncing manually, copy them from a harness project/preset output:

- `presets/<id>/STYLE.md`
- `presets/<id>/DESIGN.md`
- `presets/<id>/system_spec.md`
- `presets/<id>/token_schema.json`
- `presets/<id>/component_inventory.json`
- `presets/<id>/system_ontology.json`
- `presets/<id>/components/`

## Agent Operating Loop

Codex나 Claude Code가 이 하네스를 AI 도구로 사용할 때는 아래 루프를 따릅니다.

1. **Preflight**: `IMPLEMENTATION_CONTRACT.md`, `STYLE.md`, `DESIGN.md`,
   `token_schema.json`, `component_specs.md`, `system_ontology.json`을 먼저 읽습니다.
2. **Screen mapping**: 작업 화면을 기존 컴포넌트 패밀리와 product primitive에
   매핑합니다. 필요한 컴포넌트가 없으면 임시 UI를 만들기보다 하네스 산출물을
   먼저 갱신합니다.
3. **Implementation**: semantic token, component anatomy, state, accessibility
   contract를 기준으로 구현합니다. raw hex, 독자 팔레트 재조합, 이모지 UI,
   generic initials app icon은 금지합니다.
4. **Domain realism**: 대시보드, 도구, 스포츠, 데이터, 커뮤니티 제품은 마케팅
   히어로보다 실제 조작면을 먼저 보여줍니다. 출처, 업데이트 시각, 상태, 필터,
   표/레일/리스트 같은 운영 UI가 첫 화면의 밀도를 만듭니다.
5. **Identity and assets**: 앱 아이콘, favicon, app-shell mark는
   `BrandIdentityAsset`으로 취급합니다. 일반 `WC`, `AI`, `DS` 이니셜 타일을
   최종 아이콘으로 남기지 않고 브랜드 특정 SVG/아이콘 자산을 만듭니다.
6. **Visuals**: 히어로/카드/에디토리얼 이미지는 Codex 내장 `image_gen` 경로를
   사용합니다. 버튼 glyph, 상태 마커, 앱 아이콘은 이미지 생성 대상이 아니라
   SVG나 아이콘 라이브러리 대상입니다.
7. **Mode parity**: 명시적으로 한 모드만 요구하지 않는 한 light mode와 dark mode를
   같은 semantic token 역할로 함께 구현하고 캡처합니다.
8. **Verification**: `lint-implementation`을 실행하고, 브라우저 캡처로 desktop,
   mobile, light, dark, overflow, label clipping을 확인합니다.

국가 대표팀이나 월드컵처럼 국가 식별이 핵심인 화면에서는 팀을 장식 이니셜보다
국기 마크 + FIFA/IOC 스타일 코드로 표현합니다. 단, 좁은 ticker나 horizontal rail은
전체 국가명을 억지로 넣지 않습니다. 스캔 surface는 `flag + code + status` 중심,
detail surface는 전체 이름과 설명 중심으로 분리합니다.

## Recommended Usage In An Implementation Repo

1. Generate artifacts from the harness project
2. Run `build-preset` if the project is not already in `presets/`
3. Run `install-preset` so `design-system/` receives the full mirror
4. Run `init-agent-pack`
5. Use:
   - Codex skills for implementation inside Codex
   - Claude Code skills and subagents inside Claude Code

If you do not need agent integrations, you can stop after `install-preset`. The harness remains fully useful without any Codex or Claude-specific layer.

## Practical Example

In a frontend repo:

- first ask the agent to read `design-system/IMPLEMENTATION_CONTRACT.md` and `design-system/STYLE.md`
- ask the architect skill/agent to map a new screen to component families
- ask the implementer skill/agent to build the screen using existing tokens and primitives
- require normal light mode and dark mode together unless the task explicitly asks for one mode only; light mode is the default surface
- in Codex, ask the visual asset skill to generate imagery through the built-in `image_gen` skill for hero, empty-state, editorial, or product sections when the screen needs real visual substance
- check `system_ontology.json` for `GeneratedVisualAsset` and `ImageGenerationModel` nodes before treating generated imagery as part of the system contract
- check `system_ontology.json` for `BrandIdentityAsset` before treating favicon, app-shell mark, or web manifest icon as complete
- if the request falls outside the current artifacts, update the harness project first instead of improvising a new system

Suggested prompt:

```text
design-system/IMPLEMENTATION_CONTRACT.md,
design-system/STYLE.md,
design-system/token_schema.json,
design-system/components/component_specs.md 기준으로 작업해줘.

외부 참고 이미지는 형태, 밀도, 컴포넌트 비례만 반영하고
색상, 폰트, IA, 카피는 온톨로지와 토큰을 우선해.
일반(light) 모드와 dark 모드를 같은 semantic token 역할로 함께 구현해.
대시보드/스포츠/데이터 제품은 실제 운영 surface를 첫 화면에 배치해.
국가 기반 경기 화면은 flag + code를 스캔 surface에 쓰고, 전체 이름은 detail surface에 둬.
앱 아이콘, favicon, app-shell mark는 브랜드 특정 BrandIdentityAsset으로 만들어줘.
작업 후 lint-implementation과 브라우저 캡처로 clipping/overflow를 확인해.
```

## Codex Visual Asset Workflow

`design-system-visual-assets`는 화면을 더 프로페셔널하게 만들기 위한 선택적 Codex 전용 스킬입니다.
온톨로지에는 `GeneratedVisualAsset` 슬롯과 `ImageGenerationModel`(`Codex image_gen skill`) 노드가 함께 기록되어, 생성 이미지가 임시 장식이 아니라 브랜드/토큰/컴포넌트 관계에 묶인 산출물로 추적됩니다. 이 노드는 `api_fallback: disabled` 정책도 함께 기록합니다.

기본 흐름:

1. `design-system/IMPLEMENTATION_CONTRACT.md`, `STYLE.md`, `token_schema.json`, `component_inventory.json`, 가능하면 `visual_reference_report.json`을 읽습니다.
2. Codex의 내장 `image_gen` 스킬을 사용합니다. CLI, SDK runner, OpenAI API fallback은 사용하지 않습니다.
3. 브랜드 키워드, 안티 키워드, 팔레트, density/surface cue를 반영해 2-4개 후보 이미지를 만듭니다.
4. 승인한 이미지는 `public/generated/design-system/` 같은 정적 에셋 폴더에 넣고 manifest에 prompt, model, intended slot, alt text, source artifacts를 기록합니다.
5. 구현 코드에는 기존 프레임워크의 이미지 컴포넌트와 `alt` 텍스트, responsive crop 규칙을 적용합니다.

가드레일:

- 아이콘, 로고, 버튼 glyph, 상태 마커는 이미지 생성 대상이 아닙니다. SVG나 아이콘 라이브러리를 사용합니다.
- 앱 아이콘, favicon, 앱 셸 브랜드 마크는 필수 `BrandIdentityAsset`입니다. 일반 이니셜 타일을 최종 아이콘으로 남기지 말고 브랜드 특정 SVG identity asset으로 연결합니다.
- 저작권 캐릭터, 실제 브랜드, 실제 인물, 권리가 불분명한 장소는 사용하지 않습니다.
- 이미지 생성 도구가 없거나 실패하면 생성했다고 말하지 않고 `imagegen-prompts.md` 프롬프트 팩만 남깁니다. 그래도 API fallback은 호출하지 않습니다.

Manifest contract:

- Preferred path: `public/generated/design-system/manifest.json`
- Compatible path: `design-system/generated_visual_assets.json`
- Top-level fields: `schema_version`, `project`, `brand`, `generator`, `source_session`, `assets`
- Asset fields: `id`, `label`, `slot`, `status`, `asset_path`, `original_png_path`, `format`, `dimensions`, `size_kb`, `sha256`, `intended_for`, `alt_text`, `prompt_summary`
- Runtime code must reference the workspace copy, never `$CODEX_HOME/generated_images/...`; the original PNG path is recorded only for provenance.

## Refactor Safety Expectation

생성되는 Codex / Claude Code skills는 기본적으로 아래 원칙을 따르도록 설계되어 있습니다.

- 기존 기능과 진입점 보존
- 전체 셸 리라이트보다 점진적 적용
- theme / breakpoint 호환성 유지
- semantic token 우선, 하드코딩 색상 지양

즉 이 integration pack은 "멋있게 다시 만들어라"보다 "기존 제품을 깨지 않으면서 시스템적으로 개선하라"에 더 가깝습니다.

## Feedback Promotion

AI 도구로 쓸 때 가장 중요한 운영 규칙은 피드백을 화면 수정으로 끝내지 않는 것입니다.

반복 가능한 실패가 발견되면 아래 순서로 승격합니다.

1. `synthesis.py`의 governance rule이나 관련 온톨로지 builder에 규칙을 추가합니다.
2. `IMPLEMENTATION_CONTRACT.md`, `system_spec.md`, `STYLE.md`/`DESIGN.md` 렌더링에
   같은 규칙이 노출되게 합니다.
3. 가능하면 `lint-implementation` 룰과 테스트로 고정합니다.
4. 구현 프로젝트에서 실제 화면을 다시 고치고, light/dark 및 viewport 캡처로 검증합니다.

이번 월드컵 허브 세션에서 상위 온톨로지로 승격된 대표 규칙은 다음입니다.

- 상용 제품처럼 보이게 하려면 같은 도메인의 실제 제품 레퍼런스를 먼저 보고,
  색상/카피/IA가 아니라 module order, density, status texture, rail/table morphology만 흡수합니다.
- 스포츠/토너먼트 화면은 국가 식별에 flag + code를 우선하고, 좁은 ticker에서 긴 이름을 강제로 노출하지 않습니다.
- horizontal rail, ticker, compact card는 label clipping 자체를 실패로 봅니다.
- 앱 아이콘과 favicon은 필수 브랜드 자산이며 일반 이니셜 타일로 대체하지 않습니다.
- light mode는 선택 기능이 아니라 기본 검증 대상이며 dark mode와 함께 semantic token parity를 유지합니다.
