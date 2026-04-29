# Lattice-Dash

This folder is a self-contained harness project built on top of `design-ontology-harness`.

타깃: **B2C 스타트업 운영 대시보드 (dashboard--bold-confident)** — Retool/Appsmith/PostHog/Plausible 스타일의
activation · retention · cohort · referral 지표를 bold-confident 톤으로 한 화면에 모은 admin 콘솔.

## Files

- `brand_profile.json`: Ultra Violet + Illuminating + Creamsicle 팔레트, Space Grotesk / Inter / Pretendard
- `seeds/seed_urls.txt`: Retool / Appsmith / Stripe Radar / PostHog / Plausible
- `project_manifest.json`: project metadata
- `agent_brief.md`: instructions for human or agent collaborators
- `build/`: generated outputs

## How To Run

```bash
uv run design-ontology run-project --project-dir projects/lattice-dash
```
