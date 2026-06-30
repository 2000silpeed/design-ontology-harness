# TacticLens

This folder is a self-contained harness project built on top of `design-ontology-harness`.

타깃: **축구 영상 전술 분석 워크스페이스** — 업로드한 경기 영상에서 대상 팀의 빌드업, 압박, 전환, 수비 블록,
라인 간격, 전술 원칙 이행 여부를 타임라인·피치맵·클립·리포트로 검토하는 코칭/분석 제품.

## Files

- `brand_profile.json`: football analysis workspace identity, palette, typography, interaction primitives
- `spec.md`: MVP product plan, tactical-analysis workflow, domain model, screens, components
- `seeds/seed_urls.txt`: curated reference entry points
- `project_manifest.json`: project metadata
- `agent_brief.md`: instructions for human or agent collaborators
- `build/`: generated outputs

## How To Run

```bash
uv run design-ontology run-project --project-dir projects/tactic-lens
```

## Recommended Flow

1. Fill in `brand_profile.json`
2. Review `spec.md`
3. Set or override the KB path if needed
4. Run the project
5. Review `build/system/blueprint/system_spec.md`
