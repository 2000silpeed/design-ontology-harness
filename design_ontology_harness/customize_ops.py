"""Customize ops — Phase 11-4.

`/design-customize <preset-id>` makes a preset editable under
`projects/<name>/`. The user edits `brand_profile.json`, then re-runs
`uv run design-ontology run-project --project-dir projects/<name>` to
regenerate the system outputs with their own brand.

This module is the harness-side helper invoked by the plugin skill — the
skill itself just shells out here and prints the next-step guide.
"""

from __future__ import annotations

import json
import re
import shutil
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path

from .preset_builder import PRESETS_ROOT
from .utils import ensure_dir, slugify, write_json


_PROJECT_NAME_RE = re.compile(r"^[a-z][a-z0-9-]{1,60}$")


@dataclass
class CustomizeRequest:
    preset_id: str
    project_name: str | None = None
    projects_root: Path | None = None
    force: bool = False


@dataclass
class CustomizeOutcome:
    preset_id: str
    project_name: str
    project_dir: str
    copied_files: list[str] = field(default_factory=list)
    next_steps: list[str] = field(default_factory=list)

    def to_dict(self) -> dict:
        return {
            "preset_id": self.preset_id,
            "project_name": self.project_name,
            "project_dir": self.project_dir,
            "copied_files": list(self.copied_files),
            "next_steps": list(self.next_steps),
        }

    def format_human(self) -> str:
        lines = [
            f"[design-customize] {self.preset_id} → {self.project_dir}",
            f"  복사된 파일 ({len(self.copied_files)}개):",
        ]
        for path in self.copied_files[:12]:
            lines.append(f"    - {path}")
        if len(self.copied_files) > 12:
            lines.append(f"    … 외 {len(self.copied_files) - 12}개")
        lines.append("")
        lines.append("다음 단계:")
        for step in self.next_steps:
            lines.append(f"  • {step}")
        return "\n".join(lines)


def _default_project_name(preset_id: str) -> str:
    return slugify(preset_id.replace("--", "-")) or "design-custom"


def copy_preset_for_customization(request: CustomizeRequest) -> CustomizeOutcome:
    """Copy a preset bundle under projects/<name>/ for editing.

    Layout produced:
        projects/<name>/
          brand_profile.json           (from preset, user-editable)
          project_manifest.json
          seeds/seed_urls.txt           (empty stub)
          build/                        (empty; filled by run-project)
          _source/                      (read-only reference copy)
            manifest.json
            system_spec.md
            token_schema.json
            preview.md
            blueprint/
            components/
    """

    root = (request.projects_root or Path("projects")).resolve()
    preset_dir = (PRESETS_ROOT / request.preset_id).resolve()

    if not preset_dir.exists() or not (preset_dir / "manifest.json").exists():
        raise FileNotFoundError(
            f"preset '{request.preset_id}' not found at {preset_dir}"
        )

    project_name = request.project_name or _default_project_name(request.preset_id)
    if not _PROJECT_NAME_RE.match(project_name):
        raise ValueError(
            f"project_name '{project_name}' must match ^[a-z][a-z0-9-]{{1,60}}$"
        )

    project_dir = root / project_name
    if project_dir.exists() and any(project_dir.iterdir()) and not request.force:
        raise FileExistsError(
            f"projects/{project_name}/ already exists and is not empty. "
            f"Use force=True to overwrite."
        )

    ensure_dir(project_dir)
    ensure_dir(project_dir / "seeds")
    ensure_dir(project_dir / "build")
    source_dir = ensure_dir(project_dir / "_source")

    copied: list[str] = []

    bp_src = preset_dir / "brand_profile.json"
    if bp_src.exists():
        dest = project_dir / "brand_profile.json"
        shutil.copy2(bp_src, dest)
        copied.append("brand_profile.json")
    else:
        # Fallback: seed a minimal brand_profile anchored on the preset manifest.
        manifest = json.loads((preset_dir / "manifest.json").read_text(encoding="utf-8"))
        stub = {
            "brand_name": project_name.replace("-", " ").title(),
            "system_name": f"{project_name} system",
            "product_summary": manifest.get("description") or "Describe the product this system serves.",
            "brand_keywords": [],
            "anti_keywords": [],
            "visual_keywords": [],
        }
        write_json(project_dir / "brand_profile.json", stub)
        copied.append("brand_profile.json (stub)")

    # Mirror seed urls if the preset bundled any (rare — preset is output, not input).
    preset_seeds = preset_dir / "seeds" / "seed_urls.txt"
    if preset_seeds.exists():
        shutil.copy2(preset_seeds, project_dir / "seeds" / "seed_urls.txt")
        copied.append("seeds/seed_urls.txt")
    else:
        (project_dir / "seeds" / "seed_urls.txt").write_text(
            "# Add reference URLs, one per line. Lines starting with # are ignored.\n",
            encoding="utf-8",
        )
        copied.append("seeds/seed_urls.txt (stub)")

    # Read-only reference copy of the preset output so users can diff after editing.
    for name in ("manifest.json", "system_spec.md", "token_schema.json",
                 "preview.md", "component_inventory.json", "system_ontology.json"):
        src = preset_dir / name
        if src.exists():
            shutil.copy2(src, source_dir / name)
            copied.append(f"_source/{name}")
    for dirname in ("blueprint", "components", "ontology"):
        src = preset_dir / dirname
        if src.is_dir():
            dest = source_dir / dirname
            if dest.exists():
                shutil.rmtree(dest)
            shutil.copytree(src, dest)
            copied.append(f"_source/{dirname}/")

    manifest = {
        "project_slug": slugify(project_name),
        "brand_profile": "brand_profile.json",
        "seed_urls_file": "seeds/seed_urls.txt",
        "build_dir": "build",
        "kb_dir": None,
        "derived_from_preset": request.preset_id,
        "created_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
    }
    write_json(project_dir / "project_manifest.json", manifest)
    copied.append("project_manifest.json")

    next_steps = [
        f"`projects/{project_name}/brand_profile.json` 을 편집해서 자신의 브랜드 정보를 입력하세요.",
        f"필요하면 `projects/{project_name}/seeds/seed_urls.txt` 에 참고 URL을 추가하세요.",
        f"재합성: `uv run design-ontology run-project --project-dir projects/{project_name}`",
        f"그 결과를 프리셋으로 승격하려면: "
        f"`uv run design-ontology build-preset --project projects/{project_name} "
        f"--preset-id {request.preset_id} --owner <handle>`",
    ]

    return CustomizeOutcome(
        preset_id=request.preset_id,
        project_name=project_name,
        project_dir=str(project_dir),
        copied_files=copied,
        next_steps=next_steps,
    )
