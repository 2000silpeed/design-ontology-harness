from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from .models import utc_now_iso
from .omnigen_references import (
    DEFAULT_OMNIGEN_VAULT_DIR,
    DEFAULT_REFERENCE_DIR,
    build_omnigen_query_from_profile,
    export_omnigen_selection_gallery,
    select_omnigen_references,
    sync_omnigen_sources,
)
from .reference_context import build_design_context_pack
from .synthesis import load_brand_profile
from .utils import ensure_dir, write_json


def curate_omnigen_reference_artifacts(
    *,
    brand_profile_path: Path | str,
    project_dir: Path | str | None = None,
    output_dir: Path | str | None = None,
    vault_dir: Path | str = DEFAULT_OMNIGEN_VAULT_DIR,
    query: str | None = None,
    categories: list[str] | None = None,
    count: int = 12,
    orientation: str = "any",
    max_per_subject: int = 2,
    min_rating: int | None = None,
    max_ocr_chars: int | None = None,
    link_mode: str = "symlink",
    reference_dir: str | Path = DEFAULT_REFERENCE_DIR,
    export_gallery: bool = True,
    gallery_output: Path | str | None = None,
) -> dict[str, Any]:
    """Select Omnigen images, sync them into the profile, and write analysis artifacts."""

    profile_path = Path(brand_profile_path)
    base_dir = Path(project_dir).resolve() if project_dir else profile_path.parent.resolve()
    visuals_dir = ensure_dir(Path(output_dir) if output_dir else base_dir / "build" / "visuals")

    raw_profile = json.loads(profile_path.read_text(encoding="utf-8"))
    selection_query = query or build_omnigen_query_from_profile(raw_profile)
    selection_manifest = select_omnigen_references(
        vault_dir=vault_dir,
        project_dir=base_dir,
        query=selection_query,
        categories=categories,
        count=count,
        orientation=orientation,
        max_per_subject=max_per_subject,
        min_rating=min_rating,
        max_ocr_chars=max_ocr_chars,
        link_mode=link_mode,
        reference_dir=reference_dir,
    )
    selection_path = visuals_dir / "omnigen_reference_selection.json"
    write_json(selection_path, selection_manifest)

    gallery_path: Path | None = None
    if export_gallery:
        gallery_path = Path(gallery_output) if gallery_output else visuals_dir / "omnigen_reference_gallery.html"
        export_omnigen_selection_gallery(
            selection_manifest,
            gallery_path,
            title=f"Omnigen references for {raw_profile.get('brand_name', 'project')}",
        )

    sync_result = sync_omnigen_sources(
        raw_brand_profile=raw_profile,
        selection_manifest=selection_manifest,
        base_dir=base_dir,
    )
    write_json(profile_path, raw_profile)

    analyzed_profile = load_brand_profile(profile_path)
    visual_report = analyzed_profile.get("_resolved_visual_reference") or {}
    issues = analyzed_profile.get("_visual_reference_issues", [])
    design_context_pack = analyzed_profile.get("_design_context_pack") or build_design_context_pack(
        analyzed_profile,
        visual_report,
    )
    _write_visual_analysis_outputs(
        visuals_dir,
        profile_path,
        visual_report,
        issues,
        design_context_pack=design_context_pack,
    )

    workflow_summary = _build_workflow_summary(
        profile_path=profile_path,
        project_dir=base_dir,
        visuals_dir=visuals_dir,
        selection_path=selection_path,
        gallery_path=gallery_path,
        selection_manifest=selection_manifest,
        sync_result=sync_result,
        visual_report=visual_report,
        issues=issues,
        design_context_pack=design_context_pack,
    )
    workflow_path = visuals_dir / "omnigen_reference_workflow.json"
    write_json(workflow_path, workflow_summary)

    return {
        "brand_profile_path": profile_path,
        "project_dir": base_dir,
        "output_dir": visuals_dir,
        "selection_manifest_path": selection_path,
        "gallery_path": gallery_path,
        "workflow_summary_path": workflow_path,
        "selection_manifest": selection_manifest,
        "sync_result": sync_result,
        "visual_report": visual_report,
        "issues": issues,
        "design_context_pack": design_context_pack,
        "workflow_summary": workflow_summary,
    }


def _write_visual_analysis_outputs(
    output_dir: Path,
    brand_profile_path: Path,
    visual_report: dict[str, Any],
    issues: list[str],
    *,
    design_context_pack: dict[str, Any] | None = None,
) -> None:
    motifs = visual_report.get("visual_motifs", {}) or {}
    layout_cues = visual_report.get("layout_cues", []) or []
    component_hints = visual_report.get("component_style_hints", {}) or {}
    archetypes = visual_report.get("candidate_component_archetypes", []) or []
    mood_summary = visual_report.get("reference_mood_summary", {}) or {}

    write_json(output_dir / "visual_reference_report.json", visual_report)
    write_json(output_dir / "visual_motifs.json", motifs)
    write_json(output_dir / "layout_cues.json", layout_cues)
    write_json(output_dir / "component_style_hints.json", component_hints)
    write_json(output_dir / "candidate_component_archetypes.json", archetypes)
    write_json(output_dir / "reference_mood_summary.json", mood_summary)
    if design_context_pack:
        write_json(output_dir / "design_context_pack.json", design_context_pack)
    write_json(
        output_dir / "visual_analysis_summary.json",
        _visual_analysis_summary(
            brand_profile_path=brand_profile_path,
            visual_report=visual_report,
            issues=issues,
            design_context_pack=design_context_pack,
        ),
    )


def _visual_analysis_summary(
    *,
    brand_profile_path: Path,
    visual_report: dict[str, Any],
    issues: list[str],
    design_context_pack: dict[str, Any] | None,
) -> dict[str, Any]:
    motifs = visual_report.get("visual_motifs", {}) or {}
    layout_cues = visual_report.get("layout_cues", []) or []
    component_hints = visual_report.get("component_style_hints", {}) or {}
    return {
        "brand_profile": str(brand_profile_path),
        "issues": issues,
        "coverage": visual_report.get("coverage", {}),
        "design_context_activation": (
            (design_context_pack or {}).get("activation_state")
            if design_context_pack
            else None
        ),
        "top_layout_cue": layout_cues[0]["id"] if layout_cues else None,
        "density": (motifs.get("density") or {}).get("value"),
        "surface_style": (motifs.get("surface_style") or {}).get("value"),
        "component_hint_keys": sorted(component_hints.keys()),
    }


def _build_workflow_summary(
    *,
    profile_path: Path,
    project_dir: Path,
    visuals_dir: Path,
    selection_path: Path,
    gallery_path: Path | None,
    selection_manifest: dict[str, Any],
    sync_result: dict[str, int],
    visual_report: dict[str, Any],
    issues: list[str],
    design_context_pack: dict[str, Any] | None,
) -> dict[str, Any]:
    coverage = visual_report.get("coverage", {}) or {}
    layout_cues = visual_report.get("layout_cues", []) or []
    motifs = visual_report.get("visual_motifs", {}) or {}
    next_steps = [
        f"Review {gallery_path}" if gallery_path else "Review selected Omnigen references",
        f"Run `uv run design-ontology run-project --project-dir {project_dir}` when KB is configured",
    ]
    return {
        "schema_version": "omnigen-reference-workflow/v1",
        "created_at": utc_now_iso(),
        "brand_profile": str(profile_path),
        "project_dir": str(project_dir),
        "output_dir": str(visuals_dir),
        "selection_manifest": str(selection_path),
        "gallery": str(gallery_path) if gallery_path else None,
        "visual_reference_report": str(visuals_dir / "visual_reference_report.json"),
        "design_context_pack": str(visuals_dir / "design_context_pack.json"),
        "selected_count": int(selection_manifest.get("selected_count", 0) or 0),
        "scored_candidate_count": int(selection_manifest.get("scored_candidate_count", 0) or 0),
        "sync_result": sync_result,
        "coverage": coverage,
        "issues": issues,
        "top_layout_cue": layout_cues[0]["id"] if layout_cues else None,
        "density": (motifs.get("density") or {}).get("value"),
        "surface_style": (motifs.get("surface_style") or {}).get("value"),
        "design_context_activation": (
            (design_context_pack or {}).get("activation_state")
            if design_context_pack
            else None
        ),
        "next_steps": next_steps,
    }
