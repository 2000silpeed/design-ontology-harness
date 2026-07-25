---
name: design-system-reference-inspect
description: 웹사이트 reference inspection 산출물을 읽고 구현 계획에 안전하게 반영합니다. 원본 사이트 복제가 아니라 형태·밀도·상호작용 affordance만 흡수할 때 사용하세요.
allowed-tools: Read Glob Grep Bash Edit Write
paths:
  - "agent-team/**"
  - "build/website_research/**"
  - "docs/website_research/**"
  - "src/**"
  - "app/**"
  - "components/**"
  - "styles/**"
---

# Design System Reference Inspect

Use this skill when a screen should learn from `inspect-reference-site` outputs without cloning the referenced website.

Read `agent-team/agent-team.json` and the latest file under `agent-team/handoffs/` first. Return the advisory plan to the Team Lead; do not change stage ownership yourself.

## Required Inputs

Read these files first when they exist:

1. `agent-team/STYLE.md` or `agent-team/DESIGN.md`
2. `agent-team/system_spec.md`
3. `agent-team/token_schema.json`
4. `agent-team/components/component_specs.md` or `agent-team/components/component_specs.json`
5. `agent-team/design_context_pack.json`
6. `build/website_research/design_context_pack.json` or `docs/website_research/design_context_pack.json`
7. `build/website_research/PAGE_TOPOLOGY.md` and `build/website_research/BEHAVIORS.md` when available
8. `build/website_research/website_reference_report.json` when available

If no website inspection artifact exists, tell the user to run:

```bash
uv run design-ontology inspect-reference-site --project-dir <project> --url <url> --sync-brand-profile
```

## Absorption Rules

Allowed:
- component morphology
- layout density
- panel/card proportions
- hierarchy rhythm
- interaction affordance patterns
- flow pattern labels

Denied:
- color palette or palette composition
- typography scale
- domain IA
- product copy
- logos, brand marks, favicons, or unlicensed imagery
- any attempt to make a pixel-perfect clone unless the user owns the original and explicitly requests that scope

## Workflow

1. Map inspected sections from `PAGE_TOPOLOGY.md` to local component families.
2. Use `BEHAVIORS.md` to identify whether each surface is static, click/input-driven, scroll-aware, or time-driven.
3. Check `component_specs.md` for `Observed Reference Evidence`; use it only as advisory evidence.
4. Implement with local tokens and component anatomy from `agent-team`, not with reference-site CSS values.
5. Preserve existing product features and routing.
6. Verify desktop/mobile screenshots, overflow, clipping, light/dark mode, and `lint-implementation`.

When finishing, state which website inspection files were used and list any reference traits that were intentionally rejected because of the denied absorption rules.
