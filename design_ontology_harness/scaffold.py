from __future__ import annotations

import json
from pathlib import Path

from .models import utc_now_iso
from .utils import ensure_dir, slugify, write_json

REPO_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_COLOR_REFERENCE_PATH = REPO_ROOT / "docs" / "color-reference.md"


def scaffold_project(
    project_dir: Path,
    brand_name: str,
    system_name: str | None = None,
    product_summary: str | None = None,
    seed_urls: list[str] | None = None,
    kb_dir: str | None = None,
    force: bool = False,
) -> dict:
    if project_dir.exists() and any(project_dir.iterdir()) and not force:
        raise ValueError(
            f"Project directory already exists and is not empty: {project_dir}. Use --force to continue."
        )

    ensure_dir(project_dir)
    ensure_dir(project_dir / "seeds")
    ensure_dir(project_dir / "build")

    system_name = system_name or f"{brand_name} System"
    product_summary = product_summary or "Describe the product this design system serves."
    seed_urls = seed_urls or []

    brand_profile = {
        "brand_name": brand_name,
        "system_name": system_name,
        "product_summary": product_summary,
        "audiences": ["Describe your primary users"],
        "brand_keywords": ["clear", "distinctive", "trustworthy"],
        "anti_keywords": ["generic", "noisy", "confusing"],
        "tone_of_voice": ["clear", "warm", "confident"],
        "visual_keywords": ["Describe the visual qualities you want"],
        "interaction_keywords": ["Describe the interaction qualities you want"],
        "platforms": ["web"],
        "accessibility_targets": ["WCAG 2.2 AA"],
        "application_concept": {
            "primary_job": "The first job this product helps users complete",
            "domain_objects": ["Primary objects users inspect, create, compare, or decide on"],
            "operating_mode": "monitoring | authoring | transaction | exploration | review | coordination",
            "success_moment": "The visible state that proves the workflow succeeded",
            "differentiation": [
                "What should feel structurally different from a generic SaaS dashboard"
            ],
        },
        "layout_skeleton": {
            "composition": "command-center | split-workbench | document-canvas | feed-detail | marketplace-grid | wizard-flow | map-or-graph-canvas | timeline-ledger",
            "navigation_model": "sidebar | topbar | local-tabs | command-palette | task-rail | none",
            "density": "dense | balanced | spacious",
            "primary_regions": [
                {
                    "name": "Main work surface",
                    "role": "The region users operate most of the time",
                    "priority": "primary",
                }
            ],
            "first_screen_contract": [
                "Name the actual task surface that must appear above the fold",
                "Name the real controls or state indicators that must be visible before decoration",
            ],
            "avoid_layouts": [
                "generic hero plus card grid",
                "uniform dashboard metric cards",
                "nested cards as page sections",
            ],
        },
        "design_differentiation": {
            "must_feel_different_from": ["generic SaaS dashboard", "template card wall"],
            "signature_moves": [
                "A distinctive structural move tied to the product's workflow"
            ],
            "repetition_risks": [
                "same three-column cards",
                "oversized generic page header",
                "decorative panels before the real task surface",
            ],
        },
        "product_primitives": ["List the core UI building blocks of your product"],
        "reference_preferences": {
            "prioritize_sources_containing": ["components", "typography", "accessibility"],
            "avoid_sources_containing": ["brand-only"],
        },
        "seeds": [],
    }

    if DEFAULT_COLOR_REFERENCE_PATH.exists():
        brand_profile["color_reference"] = {
            "path": str(DEFAULT_COLOR_REFERENCE_PATH),
            "preferred_families": [],
            "palette_strategy": {
                "mode": "brand-guided",
                "candidate_count": 3,
                "active_candidate": 1,
                "temperature": "balanced",
                "contrast": "balanced",
                "diversity": "balanced",
                "surface_style": "flat",
                "prefer_moods": [],
                "avoid_moods": [],
            },
            "palette_expansion": {
                "enabled": True,
                "supporting_color_count": 8,
                "combination_count": 3,
                "prefer_pairings": True,
                "prefer_related_families": True,
            },
            "notes": [
                "docs/color-reference.md is the synchronized Semantic OS color authority",
                "preferred_families를 브랜드 방향에 맞춰 채우세요",
                "prefer_moods / avoid_moods로 mood 기반 팔레트 선택 가능",
            ],
        }

    brand_profile["visual_reference"] = {
        "mode": "local-images",
        "query": [],
        "sources": [],
        "preferred_count": 12,
        "weights": {
            "layout": 0.3,
            "component_shape": 0.25,
            "color_balance": 0.2,
            "typography_mood": 0.15,
            "surface_style": 0.1,
        },
        "extraction_policy": "advisory-only",
        "must_include": [],
        "avoid_patterns": [],
        "notes": [
            "로컬에 저장한 레퍼런스 이미지나 스크린샷 경로를 sources에 추가하세요",
            "generate-visual-queries 결과를 검토한 뒤 query를 확정하세요",
            "현재 단계에서는 Pinterest URL을 직접 수집하지 않고 로컬 파일 기준으로 분석합니다",
        ],
        "pinterest_assist": {
            "enabled": False,
            "capture_mode": "manual-save",
            "capture_dir": "references/visual/pinterest-assisted",
            "max_candidates_per_query": 6,
            "max_selected_per_query": 2,
            "preferred_sources": ["pins", "boards", "adjacent-search"],
            "notes": [
                "Pinterest는 query 생성과 후보 수집 보조에만 사용합니다",
                "최종 분석 입력은 항상 visual_reference.sources 의 로컬 파일로 고정합니다",
            ],
        },
    }

    manifest = {
        "project_slug": slugify(project_dir.name),
        "brand_profile": "brand_profile.json",
        "seed_urls_file": "seeds/seed_urls.txt",
        "build_dir": "build",
        "kb_dir": kb_dir,
        "created_at": utc_now_iso(),
    }

    agent_brief = f"""# {brand_name} Harness Agent Brief

This project uses `design-ontology-harness` as a reusable system-authoring harness.

## What The Agent Should Do

1. Read `brand_profile.json`
2. Read `seeds/seed_urls.txt`
3. Load the configured knowledge base
4. Produce custom system outputs into `build/`
5. Avoid copying any single reference system directly

## Success Criteria

- The outputs reflect this project's own identity
- The system spec is useful for a real product team
- Tokens and components are grounded in the product primitives
"""

    project_readme = f"""# {brand_name}

This folder is a self-contained harness project built on top of `design-ontology-harness`.

## Files

- `brand_profile.json`: your system identity and product context
- `seeds/seed_urls.txt`: curated reference entry points
- `project_manifest.json`: project metadata
- `agent_brief.md`: instructions for human or agent collaborators
- `build/`: generated outputs

## How To Run

```bash
uv run design-ontology run-project --project-dir {project_dir}
```

## Recommended Flow

1. Fill in `brand_profile.json`
2. Set or override the KB path if needed
3. Run the project
4. Review `build/system/blueprint/system_spec.md`
"""

    write_json(project_dir / "brand_profile.json", brand_profile)
    write_json(project_dir / "project_manifest.json", manifest)
    (project_dir / "agent_brief.md").write_text(agent_brief, encoding="utf-8")
    (project_dir / "README.md").write_text(project_readme, encoding="utf-8")
    (project_dir / "seeds" / "seed_urls.txt").write_text(
        "\n".join(seed_urls) + ("\n" if seed_urls else ""),
        encoding="utf-8",
    )

    return {
        "project_dir": str(project_dir),
        "manifest": manifest,
        "brand_profile_path": str(project_dir / "brand_profile.json"),
    }


def load_project(project_dir: Path) -> dict:
    manifest_path = project_dir / "project_manifest.json"
    if not manifest_path.exists():
        raise ValueError(f"Missing project_manifest.json in {project_dir}")
    return json.loads(manifest_path.read_text(encoding="utf-8"))


def load_seed_urls(project_dir: Path, manifest: dict) -> list[str]:
    seeds_path = project_dir / manifest["seed_urls_file"]
    if not seeds_path.exists():
        return []
    return [
        line.strip()
        for line in seeds_path.read_text(encoding="utf-8").splitlines()
        if line.strip() and not line.strip().startswith("#")
    ]


def resolve_kb_dir(project_dir: Path, manifest: dict, override: str | None = None) -> Path:
    if override:
        kb_path = Path(override)
        if not kb_path.is_absolute():
            kb_path = (Path.cwd() / kb_path).resolve()
        return kb_path
    kb_value = manifest.get("kb_dir")
    if not kb_value:
        raise ValueError("No kb_dir configured. Set it in project_manifest.json or pass --kb-dir.")
    kb_path = Path(kb_value)
    if not kb_path.is_absolute():
        kb_path = (project_dir / kb_path).resolve()
    return kb_path
