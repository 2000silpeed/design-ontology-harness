"""Image-first site design workflow scaffolding and consistency checks.

This module backs the `init-site-design` and `check-site-design` CLI commands.
It does NOT generate images itself — image generation is performed by the agent
through the built-in GPT Image 2 skill (`generate_image`, model `gpt_image_2`).
The harness only scaffolds the project structure and validates that the
generated screens, the color set, and the derived design system stay consistent
— and that the derived tokens were not copied verbatim from any existing preset,
project, or test fixture (the "do not follow our test cases" rule).

See docs/SITE_DESIGN_WORKFLOW.md for the full 6-step workflow.
"""

from __future__ import annotations

import json
import re
from dataclasses import dataclass, field
from pathlib import Path

from .models import utc_now_iso
from .utils import ensure_dir, slugify, write_json

REPO_ROOT = Path(__file__).resolve().parent.parent
WORKFLOW_ID = "site-design-image-first"
HEX_RE = re.compile(r"#[0-9a-fA-F]{6}\b")
IMAGE_MODEL = "gpt_image_2"


# --------------------------------------------------------------------------- #
# Scaffolding
# --------------------------------------------------------------------------- #

def scaffold_site_design_project(
    project_dir: Path,
    brand_name: str,
    product_summary: str | None = None,
    concept: str | None = None,
    surfaces: list[str] | None = None,
    force: bool = False,
) -> dict:
    """Create an image-first site-design project skeleton."""
    if project_dir.exists() and any(project_dir.iterdir()) and not force:
        raise ValueError(
            f"Project directory already exists and is not empty: {project_dir}. "
            "Use --force to continue."
        )

    surfaces = [s.strip() for s in (surfaces or []) if s.strip()] or [
        "landing",
        "dashboard",
        "detail",
    ]
    product_summary = product_summary or "Describe the product this site serves."
    concept = concept or "Name one design concept (e.g. 'Field Guide Naturalism')."

    ensure_dir(project_dir)
    ensure_dir(project_dir / "generated")
    ensure_dir(project_dir / "design-system")
    (project_dir / "generated" / ".gitkeep").write_text("", encoding="utf-8")
    (project_dir / "design-system" / ".gitkeep").write_text("", encoding="utf-8")

    brand_profile = {
        "brand_name": brand_name,
        "system_name": f"{brand_name} System",
        "product_summary": product_summary,
        "audiences": ["Describe your primary users"],
        "brand_keywords": ["clear", "distinctive", "trustworthy"],
        "anti_keywords": ["generic", "noisy", "default-tailwind"],
        "tone_of_voice": ["clear", "confident"],
        "feature_surfaces": surfaces,
        "platforms": ["web"],
        "accessibility_targets": ["WCAG 2.2 AA"],
    }

    manifest = {
        "project_slug": slugify(project_dir.name),
        "workflow": WORKFLOW_ID,
        "brand_profile": "brand_profile.json",
        "concept_brief": "concept_brief.md",
        "color_set": "color_set.json",
        "screen_plan": "screen_plan.json",
        "generated_dir": "generated",
        "design_system_dir": "design-system",
        "image_model": IMAGE_MODEL,
        "created_at": utc_now_iso(),
    }

    color_set = {
        "selection_method": "ontology-search-per-run",
        "derived_from": "concept + product mood (NOT a prebuilt palette)",
        "candidates": [
            {
                "id": "candidate-1",
                "active": True,
                "roles": {
                    "dominant": {"hex": "#000000", "intent": "primary brand surface/action"},
                    "supporting": {"hex": "#000000", "intent": "secondary surfaces / accents"},
                    "neutral": {"hex": "#000000", "intent": "text / borders / base surfaces"},
                    "accent": {"hex": "#000000", "intent": "highlights / focus"},
                    "success": {"hex": "#000000", "intent": "positive state"},
                    "warning": {"hex": "#000000", "intent": "caution state"},
                    "danger": {"hex": "#000000", "intent": "destructive / error state"},
                },
                "wcag_notes": "Document text-on-surface contrast pairs here.",
            }
        ],
    }

    screen_plan = {
        "concept": concept,
        "image_model": IMAGE_MODEL,
        "image_params": {"aspect_ratio": "16:9", "resolution": "2k", "quality": "high"},
        "screens": [
            {
                "surface": surface,
                "file": f"generated/{slugify(surface)}.png",
                "components": ["List the components/regions that must appear"],
                "prompt": "",
                "job_id": "",
                "status": "planned",
            }
            for surface in surfaces
        ],
    }

    surface_lines = "\n".join(f"- `{s}`" for s in surfaces)
    concept_brief = f"""# {brand_name} — Concept Brief

> Image-first site design. Follow `docs/SITE_DESIGN_WORKFLOW.md`. Do NOT copy
> colors/fonts/tokens/layouts from `presets/*`, existing `projects/*`, or
> `tests/fixtures/*`. The ontology is grounding only.

## 1. Project understanding

- **Product (one line):** {product_summary}
- **Primary users:** _fill in_
- **Tone:** _fill in_
- **Anti-keywords:** _fill in_

### Feature surfaces (one image per surface)

{surface_lines}

## 2. Design concept

- **Concept name:** {concept}
- **One sentence:** _fill in_
- **Adjectives (3–5):** _fill in_
- **Anti-patterns:** _fill in_

(Validate the wording against the ontology keyword/mood vocabulary.
Do not pick a concept from a preset.)

## 3. Color set

See `color_set.json`. Build dominant / supporting / neutral / accent + state
colors grounded in `semantic_color_selector` (ontology-search-per-run). These
colors become the color spec for the image prompts in step 4.

## 4–6

- 4: generate each surface with GPT Image 2 → `generated/` + `screen_plan.json`
- 5: derive `design-system/` (tokens, components, fonts) from the screens
- 6: ground/validate with the ontology, then run `check-site-design`
"""

    readme = f"""# {brand_name}

Image-first site design project (`workflow: {WORKFLOW_ID}`).

## Flow

1. Fill `concept_brief.md` (project + concept) and `color_set.json`.
2. For each surface, generate a screen with the GPT Image 2 skill
   (`generate_image`, model `{IMAGE_MODEL}`), save to `generated/<surface>.png`,
   and record the prompt + job_id in `screen_plan.json`.
3. Derive the design system from the screens into `design-system/`.
4. Validate:

```bash
uv run design-ontology check-site-design --project-dir {project_dir}
```

Rules: images first, system second. Ontology for grounding only. Never copy
presets / existing projects / fixtures.
"""

    write_json(project_dir / "brand_profile.json", brand_profile)
    write_json(project_dir / "project_manifest.json", manifest)
    write_json(project_dir / "color_set.json", color_set)
    write_json(project_dir / "screen_plan.json", screen_plan)
    (project_dir / "concept_brief.md").write_text(concept_brief, encoding="utf-8")
    (project_dir / "README.md").write_text(readme, encoding="utf-8")

    return {
        "project_dir": str(project_dir),
        "workflow": WORKFLOW_ID,
        "surfaces": surfaces,
        "manifest": manifest,
    }


# --------------------------------------------------------------------------- #
# Consistency check
# --------------------------------------------------------------------------- #

@dataclass
class CheckReport:
    project_dir: str
    ok: bool = True
    errors: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
    info: list[str] = field(default_factory=list)

    def error(self, msg: str) -> None:
        self.ok = False
        self.errors.append(msg)

    def warn(self, msg: str) -> None:
        self.warnings.append(msg)

    def note(self, msg: str) -> None:
        self.info.append(msg)


def _load_json(path: Path) -> dict | None:
    if not path.exists():
        return None
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return None


def _hex_values(obj) -> set[str]:
    """Collect all #RRGGBB hex values found anywhere in a JSON-ish structure."""
    found: set[str] = set()
    if isinstance(obj, str):
        found.update(m.group(0).lower() for m in HEX_RE.finditer(obj))
    elif isinstance(obj, dict):
        for value in obj.values():
            found |= _hex_values(value)
    elif isinstance(obj, list):
        for value in obj:
            found |= _hex_values(value)
    return found


def _existing_token_sources(repo_root: Path, skip: Path) -> list[tuple[str, set[str]]]:
    """Hex color sets from every preset / project / fixture token_schema.json."""
    sources: list[tuple[str, set[str]]] = []
    skip = skip.resolve()
    globs = [
        "presets/*/token_schema.json",
        "presets/*/blueprint/token_schema.json",
        "projects/*/**/token_schema.json",
        "tests/fixtures/**/token_schema.json",
    ]
    seen: set[Path] = set()
    for pattern in globs:
        for path in repo_root.glob(pattern):
            rp = path.resolve()
            if rp in seen or skip in rp.parents or rp == skip:
                continue
            seen.add(rp)
            data = _load_json(path)
            if data is None:
                continue
            hexes = _hex_values(data)
            if hexes:
                sources.append((str(path.relative_to(repo_root)), hexes))
    return sources


def check_site_design(project_dir: Path, repo_root: Path | None = None) -> CheckReport:
    repo_root = repo_root or REPO_ROOT
    report = CheckReport(project_dir=str(project_dir))

    manifest = _load_json(project_dir / "project_manifest.json")
    if manifest is None:
        report.error("missing project_manifest.json")
        return report
    if manifest.get("workflow") != WORKFLOW_ID:
        report.warn(
            f"manifest workflow is {manifest.get('workflow')!r}, expected {WORKFLOW_ID!r}"
        )

    # screen_plan ↔ generated images
    plan = _load_json(project_dir / "screen_plan.json")
    if plan is None:
        report.error("missing or invalid screen_plan.json")
    else:
        screens = plan.get("screens", [])
        if not screens:
            report.error("screen_plan.json has no screens")
        for screen in screens:
            surface = screen.get("surface", "?")
            rel = screen.get("file")
            if not rel:
                report.error(f"screen '{surface}': missing file path")
                continue
            img = project_dir / rel
            has_remote = bool(screen.get("url")) and bool(screen.get("job_id"))
            if img.exists():
                report.note(f"screen '{surface}': image present ({rel})")
            elif has_remote:
                # Generated assets may live in a CDN/asset store rather than the
                # repo (e.g. when network egress blocks pulling the binary in).
                report.warn(
                    f"screen '{surface}': local image missing, using recorded "
                    f"remote provenance (job_id={screen.get('job_id')})"
                )
            else:
                report.error(f"screen '{surface}': no local image at {rel} and no remote provenance (url+job_id)")
            if not screen.get("prompt"):
                report.warn(f"screen '{surface}': empty prompt (record the prompt used)")
            if not screen.get("job_id"):
                report.warn(f"screen '{surface}': empty job_id (record the generation id)")

    # color_set hex validity
    color_set = _load_json(project_dir / "color_set.json")
    color_hexes: set[str] = set()
    if color_set is None:
        report.warn("missing color_set.json (step 3)")
    else:
        color_hexes = _hex_values(color_set)
        placeholders = {"#000000", "#ffffff"}
        meaningful = color_hexes - placeholders
        if not meaningful:
            report.warn("color_set.json has no real colors yet (only placeholders)")

    # derived design system
    ds_dir = project_dir / (manifest.get("design_system_dir") or "design-system")
    token_schema = _load_json(ds_dir / "token_schema.json")
    if token_schema is None:
        report.error(f"missing derived {ds_dir.name}/token_schema.json (step 5)")
        derived_hexes: set[str] = set()
    else:
        derived_hexes = _hex_values(token_schema)
        if not derived_hexes:
            report.error("token_schema.json contains no color values")
        # tokens should be grounded in the color set
        if color_hexes and derived_hexes:
            grounded = derived_hexes & color_hexes
            if not grounded:
                report.warn(
                    "no token color overlaps color_set.json — tokens may not be "
                    "derived from the chosen color set"
                )
            else:
                report.note(
                    f"{len(grounded)} token color(s) trace back to color_set.json"
                )

    for required in ("component_inventory.json", "system_spec.md", "STYLE.md"):
        if not (ds_dir / required).exists():
            report.warn(f"missing {ds_dir.name}/{required} (step 5)")

    # test-case copy detection
    if derived_hexes:
        for source_name, source_hexes in _existing_token_sources(repo_root, project_dir):
            overlap = derived_hexes & source_hexes
            if not overlap:
                continue
            ratio = len(overlap) / len(derived_hexes)
            if ratio >= 0.8:
                report.error(
                    f"derived tokens are {ratio:.0%} identical to {source_name} — "
                    "looks copied from a test case; design must come from this "
                    "project's generated screens"
                )
            elif ratio >= 0.5:
                report.warn(
                    f"derived tokens share {ratio:.0%} of colors with {source_name} — "
                    "verify these were derived from the screens, not borrowed"
                )

    return report


def format_check_report(report: CheckReport) -> str:
    lines = [f"[check-site-design] {report.project_dir}"]
    for msg in report.info:
        lines.append(f"  · {msg}")
    for msg in report.warnings:
        lines.append(f"  ⚠ {msg}")
    for msg in report.errors:
        lines.append(f"  ✗ {msg}")
    lines.append("  => OK" if report.ok else "  => FAILED")
    return "\n".join(lines)
