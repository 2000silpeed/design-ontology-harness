from __future__ import annotations

import argparse
import json
import shutil
from copy import deepcopy
from pathlib import Path

from .agent_packs import scaffold_agent_pack
from .benchmark_kb import get_benchmark_systems, get_benchmark_by_keywords, save_benchmark_report
from .component_specs import generate_component_specs, write_component_specs
from .css_pipeline import run_and_save as run_css_extraction
from .kb import build_knowledge_base, load_knowledge_base
from .models import DocumentRecord, ReferenceLink
from .pinterest_capture import capture_pinterest_candidates
from .scaffold import load_project, resolve_kb_dir, scaffold_project
from .pinterest_assist import build_pinterest_assist_bundle
from .preset_builder import BuildRequest, PRESETS_ROOT, build_preset
from .preset_matcher.engine import MatchQuery, format_results, match_presets
from .preset_ops import (
    build_sources_for_all,
    build_sources_json,
    format_deprecate_report,
    format_promote_report,
    format_prune_report,
    format_rebuild_report,
    format_sources_result,
    deprecate_preset,
    find_prune_eligible,
    promote_preset,
    prune_preset,
    rebuild_all,
)
from .preset_validator import format_report as format_preset_report, validate_all
from .reference_context import build_design_context_pack
from .spec_analyzer import analyze_spec_file, build_component_list, detected_to_primitives
from .synthesis import build_blueprint, load_brand_profile
from .utils import ensure_dir, write_json, write_jsonl
from .visual_queries import generate_visual_queries


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Design ontology harness")
    subparsers = parser.add_subparsers(dest="command", required=True)

    run_parser = subparsers.add_parser("run", help="Run the full pipeline")
    run_parser.add_argument("--seed-url", required=True, help="Seed URL. Can be a curated article or a direct design-system URL.")
    run_parser.add_argument("--output-dir", default="data", help="Directory for outputs")
    run_parser.add_argument(
        "--brand-profile",
        default=None,
        help="Optional path to a JSON brand profile for custom blueprint synthesis",
    )
    run_parser.add_argument("--max-sources", type=int, default=None, help="Optional cap")
    run_parser.add_argument("--max-pages-per-source", type=int, default=3)
    run_parser.add_argument("--max-depth", type=int, default=1)

    kb_parser = subparsers.add_parser("build-kb", help="Build a reusable knowledge base from one or more seed URLs")
    kb_parser.add_argument("--kb-dir", required=True, help="Output directory for the knowledge base")
    kb_parser.add_argument(
        "--seed-url",
        action="append",
        dest="seed_urls",
        default=[],
        help="Seed URL to ingest. Can be a curated article or a direct design-system URL. Can be passed multiple times.",
    )
    kb_parser.add_argument("--seeds-file", default=None, help="Optional file containing seed URLs")
    kb_parser.add_argument("--max-sources", type=int, default=None)
    kb_parser.add_argument("--max-pages-per-source", type=int, default=2)
    kb_parser.add_argument("--max-depth", type=int, default=1)

    init_parser = subparsers.add_parser("init", help="Scaffold a reusable harness project")
    init_parser.add_argument("--project-dir", required=True, help="Directory for the new project")
    init_parser.add_argument("--brand-name", required=True, help="Brand or product name")
    init_parser.add_argument("--system-name", default=None, help="Optional system name")
    init_parser.add_argument("--product-summary", default=None, help="Optional one-line product summary")
    init_parser.add_argument(
        "--seed-url",
        action="append",
        dest="seed_urls",
        default=[],
        help="Optional initial seed URL. Can be a curated article or a direct design-system URL. Can be passed multiple times.",
    )
    init_parser.add_argument("--kb-dir", default=None, help="Optional default knowledge base path to store in the project manifest")
    init_parser.add_argument("--force", action="store_true", help="Allow writing into a non-empty directory")

    agent_pack_parser = subparsers.add_parser("init-agent-pack", help="Scaffold Codex and/or Claude Code integrations into an implementation repo")
    agent_pack_parser.add_argument("--target-repo", required=True, help="Implementation repository path")
    agent_pack_parser.add_argument("--artifact-dir", default="design-system", help="Directory inside the target repo where synced design-system artifacts live")
    agent_pack_parser.add_argument(
        "--targets",
        default="codex,claude",
        help="Comma-separated targets: codex, claude, or both",
    )
    agent_pack_parser.add_argument("--force", action="store_true", help="Overwrite existing integration files")

    seed_parser = subparsers.add_parser("extract-seed", help="Only extract references")
    seed_parser.add_argument("--seed-url", required=True, help="Seed URL. Can be a curated article or a direct design-system URL.")
    seed_parser.add_argument("--output-dir", default="data", help="Directory for outputs")

    synth_parser = subparsers.add_parser("synthesize", help="Build a custom blueprint from existing crawl outputs")
    synth_parser.add_argument("--output-dir", default="data", help="Directory for outputs")
    synth_parser.add_argument("--brand-profile", required=True, help="Path to a JSON brand profile")

    project_parser = subparsers.add_parser("run-project", help="Run a scaffolded harness project against an existing KB")
    project_parser.add_argument("--project-dir", required=True, help="Project directory created by init")
    project_parser.add_argument("--kb-dir", default=None, help="Optional override for the knowledge base path")

    visual_parser = subparsers.add_parser("analyze-visuals", help="Analyze local visual references independently from the KB flow")
    visual_target = visual_parser.add_mutually_exclusive_group(required=True)
    visual_target.add_argument("--brand-profile", default=None, help="Path to a JSON brand profile")
    visual_target.add_argument("--project-dir", default=None, help="Optional project directory created by init")
    visual_parser.add_argument("--output-dir", default=None, help="Optional directory to write visual analysis outputs")

    query_parser = subparsers.add_parser("generate-visual-queries", help="Generate Pinterest/image-search query candidates from brand profile and spec")
    query_target = query_parser.add_mutually_exclusive_group(required=True)
    query_target.add_argument("--brand-profile", default=None, help="Path to a JSON brand profile")
    query_target.add_argument("--project-dir", default=None, help="Optional project directory created by init")
    query_parser.add_argument("--spec", "--spec-file", dest="spec_file", default=None, help="Optional spec file used to bias the query set")
    query_parser.add_argument("--limit", type=int, default=16, help="Maximum number of query suggestions to generate")
    query_parser.add_argument("--output-dir", default=None, help="Optional directory to write query suggestions")
    query_parser.add_argument("--sync-brand-profile", action="store_true", help="Write generated queries back into brand_profile.visual_reference.query")

    capture_parser = subparsers.add_parser("capture-pinterest", help="Capture Pinterest search result tiles into the local pinterest_assist capture_dir")
    capture_target = capture_parser.add_mutually_exclusive_group(required=True)
    capture_target.add_argument("--brand-profile", default=None, help="Path to a JSON brand profile")
    capture_target.add_argument("--project-dir", default=None, help="Optional project directory created by init")
    capture_parser.add_argument("--spec", "--spec-file", dest="spec_file", default=None, help="Optional spec file used to regenerate query suggestions before capture")
    capture_parser.add_argument("--limit-queries", type=int, default=None, help="Optional cap on how many query groups to capture")
    capture_parser.add_argument("--max-candidates-per-query", type=int, default=None, help="Optional override for the per-query candidate cap")
    capture_parser.add_argument("--timeout-ms", type=int, default=90000, help="Page navigation timeout in milliseconds")
    capture_parser.add_argument("--wait-ms", type=int, default=7000, help="Initial wait after navigation in milliseconds")
    capture_parser.add_argument("--scroll-rounds", type=int, default=2, help="How many additional scroll passes to run per query")
    capture_parser.add_argument("--scroll-wait-ms", type=int, default=1500, help="Wait time after each scroll in milliseconds")
    capture_parser.add_argument("--headed", action="store_true", help="Run the browser visibly instead of headless mode")
    capture_parser.add_argument("--refresh-queries", action="store_true", help="Regenerate the query report before capturing")
    capture_parser.add_argument("--output-dir", default=None, help="Optional directory to write refreshed manifests")

    select_parser = subparsers.add_parser("select-pinterest-candidates", help="Explicitly lock captured Pinterest-assisted candidates into the selection manifest")
    select_target = select_parser.add_mutually_exclusive_group(required=True)
    select_target.add_argument("--brand-profile", default=None, help="Path to a JSON brand profile")
    select_target.add_argument("--project-dir", default=None, help="Optional project directory created by init")
    select_parser.add_argument("--candidate", action="append", required=True, help="Candidate id to select (for example q01-c03). Can be passed multiple times.")
    select_parser.add_argument("--reason", default=None, help="Optional selection reason applied to the provided candidates")
    select_parser.add_argument("--note", default=None, help="Optional note applied to the provided candidates")
    select_parser.add_argument("--sync-sources", action="store_true", help="Immediately copy the selected captures into visual_reference.sources")
    select_parser.add_argument("--output-dir", default=None, help="Optional directory containing the pinterest manifests")

    sync_parser = subparsers.add_parser("sync-pinterest-selection", help="Copy selected Pinterest-assisted captures into visual_reference.sources")
    sync_target = sync_parser.add_mutually_exclusive_group(required=True)
    sync_target.add_argument("--brand-profile", default=None, help="Path to a JSON brand profile")
    sync_target.add_argument("--project-dir", default=None, help="Optional project directory created by init")
    sync_parser.add_argument("--output-dir", default=None, help="Optional directory containing the pinterest manifests")

    analyze_parser = subparsers.add_parser("analyze-spec", help="Analyze a product spec to auto-detect needed UI components")
    analyze_parser.add_argument("--spec-file", required=True, help="Path to a product spec file (markdown, text)")
    analyze_parser.add_argument("--project-dir", default=None, help="Optional: update this project's brand_profile with detected primitives")
    analyze_parser.add_argument("--output-dir", default=None, help="Optional: write analysis results to this directory")

    css_parser = subparsers.add_parser("extract-css", help="Extract design tokens from CSS files (var resolution, brand colors, typography)")
    css_parser.add_argument("--css-dir", required=True, help="Directory containing .css files")
    css_parser.add_argument("--html-file", default=None, help="Optional HTML file for frequency/logo-wall analysis")
    css_parser.add_argument("--output-dir", default="data", help="Directory for outputs")

    comp_parser = subparsers.add_parser("build-components", help="Generate detailed component specs from spec + KB + brand profile")
    comp_parser.add_argument("--spec-file", required=True, help="Product spec file to analyze")
    comp_parser.add_argument("--project-dir", required=True, help="Project directory with brand_profile.json")
    comp_parser.add_argument("--kb-dir", default=None, help="Optional override for the knowledge base path")

    bench_parser = subparsers.add_parser("benchmark", help="Show benchmark references matching brand keywords")
    bench_parser.add_argument("--keywords", nargs="+", default=[], help="Brand keywords to match against 35 real-world design systems")
    bench_parser.add_argument("--brand-profile", default=None, help="Optional brand profile JSON to auto-extract keywords")
    bench_parser.add_argument("--output-dir", default=None, help="Optional directory to save benchmark report")

    build_preset_parser = subparsers.add_parser(
        "build-preset",
        help="Promote a project's build/system output into presets/<id>/ with manifest + preview",
    )
    build_preset_parser.add_argument("--project", required=True, help="Path to project directory (e.g. projects/signal-desk)")
    build_preset_parser.add_argument("--preset-id", required=True, help="{app_mode}--{brand_tone}")
    build_preset_parser.add_argument(
        "--color-modes",
        default="light,dark",
        help="Comma-separated: subset of light,dark",
    )
    build_preset_parser.add_argument("--default-color-mode", default="light", choices=["light", "dark"])
    build_preset_parser.add_argument("--tags", default="", help="Comma-separated tags")
    build_preset_parser.add_argument("--owner", required=True, help="Preset owner (maintainer handle)")
    build_preset_parser.add_argument("--tier", default="P0", choices=["P0", "P1", "P2", "P3"])
    build_preset_parser.add_argument("--description", default=None)
    build_preset_parser.add_argument("--source-commit", default=None)
    build_preset_parser.add_argument("--locale-pairings", default=None, help="Path to a JSON file with locale_pairings")

    validate_preset_parser = subparsers.add_parser(
        "validate-presets",
        help="Validate presets/ against version contract + structural invariants",
    )
    validate_preset_parser.add_argument("--presets-dir", default=None, help="Override presets/ root")
    validate_preset_parser.add_argument(
        "--include-preview-lint",
        action="store_true",
        help="Also run preview.md linter (Phase 12A-2). Errors join exit-code gate.",
    )

    lint_preview_parser = subparsers.add_parser(
        "lint-previews",
        help="Lint preset preview.md files for PLAN §9.3 template compliance",
    )
    lint_preview_parser.add_argument("--presets-dir", default=None, help="Override presets/ root")
    lint_preview_parser.add_argument(
        "--preset-id",
        default=None,
        help="Lint a single preset (default: all presets under presets/)",
    )

    lint_impl_parser = subparsers.add_parser(
        "lint-implementation",
        help="Lint an implementation repo for ontology token binding violations",
    )
    lint_impl_parser.add_argument("--target-repo", required=True, help="Implementation repository path")
    lint_impl_parser.add_argument(
        "--artifact-dir",
        default="design-system",
        help="Installed artifact directory to exclude from implementation linting",
    )
    lint_impl_parser.add_argument("--json", action="store_true", help="Emit JSON report")

    rebuild_parser = subparsers.add_parser(
        "rebuild-all-presets",
        help="Walk matrix.json and rebuild every preset from its source_project",
    )
    rebuild_parser.add_argument("--projects-root", default="projects", help="Root directory containing source projects")

    match_parser = subparsers.add_parser(
        "match-preset",
        help="Rank presets against user signals (question answers or free text)",
    )
    match_parser.add_argument("--app-mode", default=None, help="One of 8 app_modes (dashboard, ...)")
    match_parser.add_argument("--brand-tone", default=None, help="One of 5 brand_tones (minimal-tech, ...)")
    match_parser.add_argument(
        "--color-mode",
        default=None,
        choices=["light", "dark", "both", None],
        help="Requested color mode (light, dark, both)",
    )
    match_parser.add_argument("--tags", default="", help="Comma-separated tags (ko, saas, ai, ...)")
    match_parser.add_argument("--stack", default=None, help="Optional target stack (e.g. nextjs-tailwind-shadcn)")
    match_parser.add_argument("--locale", default=None, help="Optional locale (ko, en)")
    match_parser.add_argument("--free-text", default=None, help="Natural-language description")
    match_parser.add_argument("--top", type=int, default=3, help="Return top-N results (default 3)")
    match_parser.add_argument("--json", action="store_true", help="Emit JSON for scripting")
    match_parser.add_argument(
        "--include-deprecated",
        action="store_true",
        help="Include deprecated presets in results (default: hidden)",
    )

    install_parser = subparsers.add_parser(
        "install-preset",
        help="Render a preset via an adapter into a target repo + record INSTALLED.json",
    )
    install_parser.add_argument("--preset-id", required=True)
    install_parser.add_argument("--target-repo", required=True, help="Target repo directory")
    install_parser.add_argument(
        "--adapter",
        default="nextjs-tailwind-shadcn",
        help="Adapter id (default: nextjs-tailwind-shadcn)",
    )
    install_parser.add_argument("--color-mode", default=None, help="light | dark (defaults to preset default_color_mode)")
    install_parser.add_argument("--locale", default="en", help="Locale for font pairing (ko/en)")
    install_parser.add_argument(
        "--force",
        action="store_true",
        help="Re-apply even if content_hash matches existing INSTALLED.json",
    )
    install_parser.add_argument("--json", action="store_true", help="Emit JSON summary")

    eval_parser = subparsers.add_parser(
        "eval-matcher",
        help="Run labeled queries and report top-1 accuracy + confusion matrix",
    )
    eval_parser.add_argument(
        "--verbose",
        action="store_true",
        help="Also list every miss (expected vs predicted)",
    )
    eval_parser.add_argument(
        "--threshold",
        type=float,
        default=0.85,
        help="Minimum top-1 accuracy; exit non-zero if below (default 0.85)",
    )

    health_parser = subparsers.add_parser(
        "catalog-health",
        help="Aggregate catalog metrics (tier coverage, drift, deprecation candidates)",
    )
    health_parser.add_argument(
        "--presets-dir",
        default=None,
        help="Override presets/ root (default: harness repo presets/)",
    )
    health_parser.add_argument(
        "--metrics-dir",
        default=None,
        help="Override metrics root (default: <presets-dir>/.metrics)",
    )
    health_parser.add_argument(
        "--snapshot-fixture",
        default=None,
        help="Override snapshot fixture path (default: tests/fixtures/preset_snapshots.json)",
    )
    health_parser.add_argument(
        "--output",
        default=None,
        help="Override CATALOG_HEALTH.md output path (default: <presets-dir>/CATALOG_HEALTH.md). Use '-' to skip writing.",
    )
    health_parser.add_argument(
        "--json",
        action="store_true",
        help="Emit full report as JSON to stdout instead of summary.",
    )

    promote_parser = subparsers.add_parser(
        "promote-preset",
        help="Bump a preset's tier after running 5 lifecycle gates (Phase 15-2)",
    )
    promote_parser.add_argument("preset_id", help="Preset id to promote")
    promote_parser.add_argument(
        "--target",
        default=None,
        choices=["P0", "P1", "P2"],
        help="Target tier (default: one step up from current).",
    )
    promote_parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Run all gates but do not mutate manifest/matrix",
    )
    promote_parser.add_argument(
        "--projects-root",
        default="projects",
        help="Root directory for source projects (reserved for future rebuild integration)",
    )
    promote_parser.add_argument(
        "--presets-dir",
        default=None,
        help="Override presets/ root",
    )

    deprecate_parser = subparsers.add_parser(
        "deprecate-preset",
        help="Mark a preset deprecated on its manifest (Phase 15-3)",
    )
    deprecate_parser.add_argument("preset_id", help="Preset id to deprecate")
    deprecate_parser.add_argument(
        "--reason",
        required=True,
        help=(
            "One of zero_hits | version_lag | snapshot_drift | owner_abandoned | manual, "
            "or 'manual:<free text>'"
        ),
    )
    deprecate_parser.add_argument(
        "--replacement",
        default=None,
        help="Optional replacement preset_id (surfaced in matcher rationale)",
    )
    deprecate_parser.add_argument(
        "--force",
        action="store_true",
        help="Allow updating an already-deprecated preset's reason/replacement",
    )
    deprecate_parser.add_argument(
        "--presets-dir",
        default=None,
        help="Override presets/ root",
    )

    prune_parser = subparsers.add_parser(
        "prune-preset",
        help="Physically remove a deprecated preset after safety gates (Phase 15-4)",
    )
    prune_parser.add_argument(
        "preset_id",
        nargs="?",
        default=None,
        help="Preset id to prune (omit with --all)",
    )
    prune_parser.add_argument(
        "--confirm",
        action="store_true",
        help="Required for actual deletion (pruning is irreversible)",
    )
    prune_parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Run gates only, do not delete anything (default when --confirm absent)",
    )
    prune_parser.add_argument(
        "--all",
        dest="all_eligible",
        action="store_true",
        help="Prune every catalog_health.prune_eligible preset (dry-run by default)",
    )
    prune_parser.add_argument(
        "--min-age-days",
        type=int,
        default=None,
        help="Override minimum deprecated_at age (days). Default 90.",
    )
    prune_parser.add_argument(
        "--presets-dir",
        default=None,
        help="Override presets/ root",
    )
    prune_parser.add_argument(
        "--metrics-dir",
        default=None,
        help="Override metrics root (default: <presets-dir>/.metrics)",
    )
    prune_parser.add_argument(
        "--snapshot-fixture",
        default=None,
        help="Override snapshot fixture path",
    )

    sources_parser = subparsers.add_parser(
        "build-sources",
        help="Generate presets/<id>/sources.json from project KB seeds (Phase 15-9)",
    )
    sources_parser.add_argument(
        "--preset-id",
        default=None,
        help="Single preset id. Omit together with --all to process every catalog entry.",
    )
    sources_parser.add_argument(
        "--all",
        dest="all_presets",
        action="store_true",
        help="Build sources.json for every preset in matrix.json",
    )
    sources_parser.add_argument(
        "--force",
        action="store_true",
        help="Overwrite existing sources.json",
    )
    sources_parser.add_argument(
        "--presets-dir",
        default=None,
        help="Override presets/ root",
    )
    sources_parser.add_argument(
        "--projects-root",
        default="projects",
        help="Root directory for source projects",
    )

    customize_parser = subparsers.add_parser(
        "customize-preset",
        help="Copy a preset under projects/<name>/ for brand_profile editing + re-synthesis",
    )
    customize_parser.add_argument("--preset-id", required=True)
    customize_parser.add_argument("--project-name", default=None, help="Directory name under projects/ (default: derived from preset-id)")
    customize_parser.add_argument("--projects-root", default="projects", help="Root for project copies")
    customize_parser.add_argument("--force", action="store_true", help="Overwrite existing projects/<name>/")
    customize_parser.add_argument("--json", action="store_true", help="Emit JSON summary")

    return parser


def _component_specs_source_from_inventory(component_list: list[dict], component_inventory: dict | None) -> list[dict]:
    """Merge spec-detected components with generated inventory components.

    `run-project` first detects components from spec.md, then `build_blueprint`
    may add ontology-recommended advanced components. Component specs should cover
    both sets so agents can implement the richer inventory directly.
    """

    by_name: dict[str, dict] = {}
    for component in component_list:
        name = component.get("name")
        if name:
            by_name[name] = dict(component)

    if not isinstance(component_inventory, dict):
        return list(by_name.values())

    for component in component_inventory.get("components", []):
        if not isinstance(component, dict):
            continue
        name = component.get("name")
        if not name:
            continue
        if name in by_name:
            merged = dict(by_name[name])
            for key, value in component.items():
                if key not in merged or merged[key] in (None, "", []):
                    merged[key] = value
            by_name[name] = merged
        else:
            by_name[name] = dict(component)

    return list(by_name.values())


def main() -> None:
    args = build_parser().parse_args()
    raw_output = getattr(args, "output_dir", None)
    output_dir = ensure_dir(Path(raw_output)) if raw_output else None

    if args.command == "build-preset":
        color_modes = [m.strip() for m in args.color_modes.split(",") if m.strip()]
        tags = [t.strip() for t in args.tags.split(",") if t.strip()]
        locale_pairings = None
        if args.locale_pairings:
            locale_pairings = json.loads(Path(args.locale_pairings).read_text(encoding="utf-8"))
        request = BuildRequest(
            project_dir=Path(args.project),
            preset_id=args.preset_id,
            color_modes=color_modes,
            default_color_mode=args.default_color_mode,
            tags=tags,
            owner=args.owner,
            tier=args.tier,
            description=args.description,
            source_commit=args.source_commit,
            locale_pairings=locale_pairings,
        )
        manifest = build_preset(request)
        print(f"[build-preset] 프리셋 빌드 완료: presets/{manifest['id']}/")
        print(f"  -> preset_api_version={manifest['preset_api_version']}")
        print(f"  -> content_hash={manifest['content_hash']}")
        return

    if args.command == "validate-presets":
        presets_dir = Path(args.presets_dir) if args.presets_dir else None
        report = validate_all(presets_dir)
        print(format_preset_report(report))
        preview_ok = True
        if getattr(args, "include_preview_lint", False):
            from .preview_linter import format_reports as format_preview_reports, lint_all_previews

            root = presets_dir or PRESETS_ROOT
            preview_reports = lint_all_previews(root)
            print()
            print("Preview lint:")
            print(format_preview_reports(preview_reports))
            preview_ok = all(r.ok for r in preview_reports)
        if not report.ok or not preview_ok:
            raise SystemExit(1)
        return

    if args.command == "lint-previews":
        from .preview_linter import (
            format_report as format_preview_report,
            format_reports as format_preview_reports,
            lint_all_previews,
            lint_preview,
        )

        root = Path(args.presets_dir) if args.presets_dir else PRESETS_ROOT
        if args.preset_id:
            preset_dir = root / args.preset_id
            if not preset_dir.is_dir():
                raise SystemExit(f"preset not found: {preset_dir}")
            preview_report = lint_preview(preset_dir)
            print(format_preview_report(preview_report))
            if not preview_report.ok:
                raise SystemExit(1)
            return
        reports = lint_all_previews(root)
        print(format_preview_reports(reports))
        if any(not r.ok for r in reports):
            raise SystemExit(1)
        return

    if args.command == "lint-implementation":
        from .implementation_linter import format_json, format_report, lint_implementation

        report = lint_implementation(
            Path(args.target_repo),
            artifact_dir=args.artifact_dir,
        )
        print(format_json(report) if args.json else format_report(report))
        if not report.ok:
            raise SystemExit(1)
        return

    if args.command == "rebuild-all-presets":
        projects_root = Path(args.projects_root)
        if not projects_root.is_dir():
            raise SystemExit(f"projects-root not a directory: {projects_root}")
        report = rebuild_all(projects_root)
        print(format_rebuild_report(report))
        if not report.ok:
            raise SystemExit(1)
        return

    if args.command == "match-preset":
        tags = [t.strip() for t in (args.tags or "").split(",") if t.strip()]
        query = MatchQuery(
            app_mode=args.app_mode,
            brand_tone=args.brand_tone,
            color_mode=args.color_mode,
            tags=tags,
            stack=args.stack,
            locale=args.locale,
            free_text=args.free_text,
        )
        results = match_presets(
            query,
            top_k=args.top,
            include_deprecated=bool(getattr(args, "include_deprecated", False)),
        )
        if args.json:
            payload = {
                "query": {
                    "app_mode": query.app_mode,
                    "brand_tone": query.brand_tone,
                    "color_mode": query.color_mode,
                    "tags": query.tags,
                    "stack": query.stack,
                    "locale": query.locale,
                    "free_text": query.free_text,
                },
                "results": [r.to_dict() for r in results],
                "fallback": bool(results) and all(r.bucket == "Low" for r in results),
            }
            print(json.dumps(payload, ensure_ascii=False, indent=2))
        else:
            print(format_results(results))
        return

    if args.command == "install-preset":
        from .preset_installer import InstallRequest, install_preset

        request = InstallRequest(
            preset_id=args.preset_id,
            target_repo=Path(args.target_repo),
            adapter_id=args.adapter,
            color_mode=args.color_mode,
            locale=args.locale,
            force=args.force,
        )
        outcome = install_preset(request)
        if args.json:
            print(json.dumps(outcome.to_dict(), ensure_ascii=False, indent=2))
        else:
            print(outcome.format_human())
        return

    if args.command == "eval-matcher":
        from .preset_matcher.eval import format_eval, run_eval

        result = run_eval()
        print(format_eval(result, verbose=args.verbose))
        if result.accuracy < args.threshold:
            raise SystemExit(1)
        return

    if args.command == "catalog-health":
        from .catalog_health import compute_health, format_markdown, format_summary

        presets_root = Path(args.presets_dir) if args.presets_dir else None
        metrics_dir = Path(args.metrics_dir) if args.metrics_dir else None
        snapshot_fixture = Path(args.snapshot_fixture) if args.snapshot_fixture else None
        report = compute_health(
            presets_root=presets_root,
            metrics_dir=metrics_dir,
            snapshot_fixture_path=snapshot_fixture,
        )
        if args.json:
            print(json.dumps(report, ensure_ascii=False, indent=2))
        else:
            print(format_summary(report))

        if args.output != "-":
            if args.output:
                output_path = Path(args.output)
            else:
                root = presets_root or PRESETS_ROOT
                output_path = root / "CATALOG_HEALTH.md"
            output_path.parent.mkdir(parents=True, exist_ok=True)
            output_path.write_text(format_markdown(report), encoding="utf-8")
            if not args.json:
                print(f"  -> {output_path}")
        return

    if args.command == "promote-preset":
        presets_dir = Path(args.presets_dir) if args.presets_dir else None
        report = promote_preset(
            args.preset_id,
            target_tier=args.target,
            dry_run=args.dry_run,
            projects_root=Path(args.projects_root) if args.projects_root else None,
            presets_root=presets_dir,
        )
        print(format_promote_report(report))
        if not report.ok:
            raise SystemExit(1)
        return

    if args.command == "deprecate-preset":
        presets_dir = Path(args.presets_dir) if args.presets_dir else None
        report = deprecate_preset(
            args.preset_id,
            reason=args.reason,
            replacement=args.replacement,
            force=args.force,
            presets_root=presets_dir,
        )
        print(format_deprecate_report(report))
        if not report.ok:
            raise SystemExit(1)
        return

    if args.command == "prune-preset":
        presets_dir = Path(args.presets_dir) if args.presets_dir else None
        metrics_dir = Path(args.metrics_dir) if args.metrics_dir else None
        snapshot_fixture = Path(args.snapshot_fixture) if args.snapshot_fixture else None
        kwargs: dict = {
            "presets_root": presets_dir,
            "metrics_dir": metrics_dir,
            "snapshot_fixture_path": snapshot_fixture,
        }
        if args.min_age_days is not None:
            kwargs["min_deprecated_age_days"] = args.min_age_days

        dry_run = args.dry_run or not args.confirm
        targets: list[str]
        if args.all_eligible:
            find_kwargs: dict = {
                "presets_root": presets_dir,
                "metrics_dir": metrics_dir,
            }
            if args.min_age_days is not None:
                find_kwargs["min_deprecated_age_days"] = args.min_age_days
            targets = find_prune_eligible(**find_kwargs)
            if not targets:
                print("[prune-preset] 조건을 충족하는 프리셋 없음 — 종료")
                return
            print(f"[prune-preset] --all 대상 {len(targets)}건: {', '.join(targets)}")
        elif args.preset_id:
            targets = [args.preset_id]
        else:
            raise SystemExit("preset_id 또는 --all 플래그가 필요합니다.")

        any_failed = False
        for preset_id in targets:
            report = prune_preset(
                preset_id,
                confirm=args.confirm,
                dry_run=dry_run,
                **kwargs,
            )
            print(format_prune_report(report))
            if not report.ok:
                any_failed = True
        if any_failed:
            raise SystemExit(1)
        return

    if args.command == "build-sources":
        presets_dir = Path(args.presets_dir) if args.presets_dir else None
        projects_root = Path(args.projects_root)
        if args.all_presets:
            results = build_sources_for_all(
                presets_root=presets_dir,
                projects_root=projects_root,
                force=args.force,
            )
        elif args.preset_id:
            results = [
                build_sources_json(
                    args.preset_id,
                    presets_root=presets_dir,
                    projects_root=projects_root,
                    force=args.force,
                )
            ]
        else:
            raise SystemExit("--preset-id 또는 --all 플래그가 필요합니다.")
        written = 0
        skipped = 0
        warned = 0
        errored = 0
        for result in results:
            print(format_sources_result(result))
            if result.written_path:
                written += 1
            if result.skipped:
                skipped += 1
            if result.warnings:
                warned += 1
            if result.reason and not result.skipped:
                errored += 1
        print(
            f"\n[build-sources] 요약: {len(results)}종 처리 / "
            f"작성 {written}종 · skip {skipped}종 · warn {warned}종 · error {errored}종"
        )
        if errored:
            raise SystemExit(1)
        return

    if args.command == "customize-preset":
        from .customize_ops import CustomizeRequest, copy_preset_for_customization

        outcome = copy_preset_for_customization(
            CustomizeRequest(
                preset_id=args.preset_id,
                project_name=args.project_name,
                projects_root=Path(args.projects_root),
                force=args.force,
            )
        )
        if args.json:
            print(json.dumps(outcome.to_dict(), ensure_ascii=False, indent=2))
        else:
            print(outcome.format_human())
        return

    if args.command == "benchmark":
        keywords = list(args.keywords)
        if args.brand_profile:
            bp = json.loads(Path(args.brand_profile).read_text(encoding="utf-8"))
            keywords.extend(bp.get("brand_keywords", []))
        if not keywords:
            systems = get_benchmark_systems()
            print(f"[benchmark] 전체 {len(systems)}개 실서비스 디자인 시스템 레퍼런스:")
            for s in systems:
                print(f"  - {s['name']} ({s['category']}): {', '.join(s['keywords'])}")
            return
        matched = get_benchmark_by_keywords(keywords)
        print(f"[benchmark] '{', '.join(keywords)}' 키워드와 매칭되는 시스템 ({len(matched)}개):")
        for s in matched[:10]:
            overlap = set(kw.lower() for kw in keywords) & set(s["keywords"])
            print(f"  - {s['name']} ({s['category']})")
            print(f"    키워드: {', '.join(s['keywords'])} | 매칭: {', '.join(overlap)}")
            print(f"    컬러: {s['color_strategy']}")
            print(f"    특징: {', '.join(s['notable'][:3])}")
        if args.output_dir:
            out = ensure_dir(Path(args.output_dir))
            bp = {"brand_keywords": keywords}
            if args.brand_profile:
                bp = json.loads(Path(args.brand_profile).read_text(encoding="utf-8"))
            report = save_benchmark_report(out, bp)
            print(f"\n  -> {out}/benchmark/ 저장 완료")
        return

    if args.command == "analyze-spec":
        spec_path = Path(args.spec_file)
        if not spec_path.exists():
            raise SystemExit(f"파일을 찾을 수 없습니다: {spec_path}")
        detected = analyze_spec_file(spec_path)
        if not detected:
            print("[analyze-spec] UI 패턴을 감지하지 못했습니다.")
            return
        print(f"[analyze-spec] {len(detected)}개 UI 패턴 감지:")
        for item in detected:
            terms = ", ".join(item["matched_terms"][:4])
            print(f"  [{item['confidence']:2d}] {item['pattern']}: {item['description']}")
            print(f"       매칭: {terms}")
            print(f"       컴포넌트: {', '.join(c['name'] for c in item['components'][:5])}")
        component_list = build_component_list(detected)
        print(f"\n  총 {len(component_list)}개 컴포넌트 도출")
        if args.project_dir:
            project_dir = Path(args.project_dir)
            bp_path = project_dir / "brand_profile.json"
            if bp_path.exists():
                bp = json.loads(bp_path.read_text(encoding="utf-8"))
                bp["product_primitives"] = detected_to_primitives(detected)
                write_json(bp_path, bp)
                print(f"\n  -> {bp_path} 의 product_primitives를 업데이트했습니다.")
        if args.output_dir:
            out = ensure_dir(Path(args.output_dir))
            write_json(out / "spec_analysis.json", {
                "spec_file": str(spec_path),
                "detected_patterns": detected,
                "component_list": component_list,
            })
            print(f"  -> {out}/spec_analysis.json 저장 완료")
        return

    if args.command == "extract-css":
        css_dir = Path(args.css_dir)
        if not css_dir.is_dir():
            raise SystemExit(f"CSS 디렉토리를 찾을 수 없습니다: {css_dir}")
        html_path = Path(args.html_file) if args.html_file else None
        result = run_css_extraction(css_dir, output_dir, html_path)
        var_info = result["var_resolution"]
        brand_info = result["brand_colors"]["summary"]
        typo_info = result["typography"]["stats"]
        print(f"[extract-css] CSS 추출 완료 ({output_dir}/css_extraction/)")
        print(f"  -> var 해석: {var_info['resolved_count']}/{var_info['total_vars']}개 해결")
        print(f"  -> 브랜드 색상: {brand_info['total_candidates']}개 후보")
        print(f"  -> 타이포그래피: {typo_info['scale_entries']}개 스케일, {typo_info['unique_families']}개 폰트 패밀리")
        return

    if args.command == "build-components":
        spec_path = Path(args.spec_file)
        project_dir = Path(args.project_dir)
        if not spec_path.exists():
            raise SystemExit(f"파일을 찾을 수 없습니다: {spec_path}")
        manifest = load_project(project_dir)
        kb_dir = resolve_kb_dir(project_dir, manifest, args.kb_dir)
        references, documents, kb_manifest = load_knowledge_base(kb_dir)
        brand_profile_path = project_dir / manifest["brand_profile"]
        brand_profile = load_brand_profile(brand_profile_path)
        detected = analyze_spec_file(spec_path)
        component_list = build_component_list(detected)
        print(f"[build-components] {len(detected)}개 UI 패턴에서 {len(component_list)}개 컴포넌트 도출")
        build_root = ensure_dir(project_dir / manifest.get("build_dir", "build"))
        output_dir = ensure_dir(build_root / "system")
        blueprint = {}
        component_inventory = {}
        bp_path = output_dir / "blueprint" / "design_system_blueprint.json"
        if bp_path.exists():
            blueprint = json.loads(bp_path.read_text(encoding="utf-8"))
        inventory_path = output_dir / "blueprint" / "component_inventory.json"
        if inventory_path.exists():
            component_inventory = json.loads(inventory_path.read_text(encoding="utf-8"))
        specs_source = _component_specs_source_from_inventory(component_list, component_inventory)
        specs_data = generate_component_specs(
            brand_profile=brand_profile,
            blueprint=blueprint,
            component_list=specs_source,
            documents=documents,
        )
        write_component_specs(output_dir, specs_data)
        print("[build-components] 컴포넌트 스펙 생성 완료:")
        print(f"  -> {output_dir}/components/component_specs.md")
        print(f"  -> {output_dir}/components/component_specs.json")
        return

    if args.command == "analyze-visuals":
        brand_profile_path, project_dir, manifest = _resolve_brand_profile_target(
            brand_profile_arg=args.brand_profile,
            project_dir_arg=args.project_dir,
        )
        brand_profile = load_brand_profile(brand_profile_path)
        if not isinstance(brand_profile.get("visual_reference"), dict):
            raise SystemExit("brand_profile.visual_reference 가 설정되지 않았습니다.")

        visuals_dir = _resolve_support_output_dir(
            raw_output=args.output_dir,
            project_dir=project_dir,
            manifest=manifest,
            folder_name="visuals",
        )
        visual_report = brand_profile.get("_resolved_visual_reference") or {}
        issues = brand_profile.get("_visual_reference_issues", [])
        design_context_pack = brand_profile.get("_design_context_pack") or build_design_context_pack(
            brand_profile,
            visual_report,
        )
        _write_visual_analysis_outputs(
            visuals_dir,
            brand_profile_path,
            visual_report,
            issues,
            design_context_pack=design_context_pack,
        )

        coverage = visual_report.get("coverage", {}) or {}
        motifs = visual_report.get("visual_motifs", {}) or {}
        layout_cues = visual_report.get("layout_cues", []) or []
        top_layout = layout_cues[0]["id"] if layout_cues else "n/a"
        print(f"[analyze-visuals] 시각 레퍼런스 분석 완료: {visuals_dir}")
        print(
            f"  -> 소스 {coverage.get('source_count', 0)}개 | "
            f"이미지 {coverage.get('image_count', 0)}개 | "
            f"selected {coverage.get('selected_image_count', 0)}개"
        )
        print(
            f"  -> density {(motifs.get('density') or {}).get('value', 'n/a')} | "
            f"surface {(motifs.get('surface_style') or {}).get('value', 'n/a')} | "
            f"layout {top_layout}"
        )
        print("  -> visual_reference_report.json, visual_motifs.json, layout_cues.json, design_context_pack.json 저장")
        if issues:
            print("  -> 이슈:")
            for issue in issues[:5]:
                print(f"     - {issue}")
        return

    if args.command == "generate-visual-queries":
        brand_profile_path, project_dir, manifest = _resolve_brand_profile_target(
            brand_profile_arg=args.brand_profile,
            project_dir_arg=args.project_dir,
        )
        brand_profile = load_brand_profile(brand_profile_path)
        spec_path = _resolve_spec_path(project_dir, args.spec_file)
        if args.spec_file and not spec_path.exists():
            raise SystemExit(f"파일을 찾을 수 없습니다: {spec_path}")

        spec_text = spec_path.read_text(encoding="utf-8") if spec_path and spec_path.exists() else None
        report = generate_visual_queries(brand_profile=brand_profile, spec_text=spec_text, limit=args.limit)
        visuals_dir = _resolve_support_output_dir(
            raw_output=args.output_dir,
            project_dir=project_dir,
            manifest=manifest,
            folder_name="visuals",
        )
        write_json(visuals_dir / "visual_query_suggestions.json", report)
        if args.sync_brand_profile:
            raw_profile = json.loads(brand_profile_path.read_text(encoding="utf-8"))
            visual_reference = raw_profile.setdefault("visual_reference", {})
            visual_reference["query"] = [item["query"] for item in report["queries"]]
            write_json(brand_profile_path, raw_profile)
            brand_profile = load_brand_profile(brand_profile_path)
        assist_bundle = _refresh_pinterest_assist_outputs(
            visuals_dir=visuals_dir,
            brand_profile=brand_profile,
            query_report=report,
            project_dir=project_dir,
        )
        design_context_pack = build_design_context_pack(
            brand_profile,
            brand_profile.get("_resolved_visual_reference") or {},
            report,
        )
        write_json(visuals_dir / "design_context_pack.json", design_context_pack)

        print(f"[generate-visual-queries] {report['query_count']}개 query 생성 완료: {visuals_dir}/visual_query_suggestions.json")
        print(f"  -> Pinterest assist plan: {visuals_dir}/pinterest_assist_plan.json")
        print(f"  -> Design context pack: {visuals_dir}/design_context_pack.json")
        print(f"  -> Candidate manifest: {visuals_dir}/pinterest_candidate_manifest.json")
        print(f"  -> Selection manifest: {visuals_dir}/pinterest_selection_manifest.json")
        if spec_path and spec_path.exists():
            print(f"  -> spec 반영: {spec_path}")
        else:
            print("  -> spec 미사용: brand_profile.product_primitives 기준")
        for index, item in enumerate(report["queries"][: min(10, len(report["queries"]))], start=1):
            print(f"  {index:2d}. {item['query']} [{item['intent']}]")

        if args.sync_brand_profile:
            print(f"  -> {brand_profile_path} 의 visual_reference.query 를 업데이트했습니다.")

        pinterest_config = (brand_profile.get("visual_reference") or {}).get("pinterest_assist") or {}
        auto_capture = (
            (brand_profile.get("visual_reference") or {}).get("mode") == "pinterest-assisted"
            and pinterest_config.get("enabled")
            and str(pinterest_config.get("capture_mode", "")).strip().lower() == "playwright-capture"
        )
        if auto_capture:
            capture_report = capture_pinterest_candidates(
                brand_profile=brand_profile,
                query_report=report,
                project_dir=project_dir,
                headless=True,
            )
            assist_bundle = _refresh_pinterest_assist_outputs(
                visuals_dir=visuals_dir,
                brand_profile=brand_profile,
                query_report=report,
                project_dir=project_dir,
                captured_candidates=_capture_map_from_report(capture_report),
            )
            print(
                f"  -> Pinterest Playwright capture: {capture_report['captured_count']}개 candidate 저장 "
                f"({assist_bundle['plan']['capture_progress']['capture_root']})"
            )
            for query_result in capture_report["queries"][: min(5, len(capture_report["queries"]))]:
                print(f"     - {query_result['query_id']}: {len(query_result['captured_candidates'])} captured")
        return

    if args.command == "capture-pinterest":
        brand_profile_path, project_dir, manifest = _resolve_brand_profile_target(
            brand_profile_arg=args.brand_profile,
            project_dir_arg=args.project_dir,
        )
        brand_profile = load_brand_profile(brand_profile_path)
        visuals_dir = _resolve_support_output_dir(
            raw_output=args.output_dir,
            project_dir=project_dir,
            manifest=manifest,
            folder_name="visuals",
        )
        spec_path = _resolve_spec_path(project_dir, args.spec_file)
        report = _load_or_build_query_report(
            brand_profile=brand_profile,
            visuals_dir=visuals_dir,
            project_dir=project_dir,
            spec_path=spec_path,
            refresh=args.refresh_queries,
        )
        write_json(visuals_dir / "visual_query_suggestions.json", report)
        capture_report = capture_pinterest_candidates(
            brand_profile=brand_profile,
            query_report=report,
            project_dir=project_dir,
            limit_queries=args.limit_queries,
            max_candidates_per_query=args.max_candidates_per_query,
            headless=not args.headed,
            timeout_ms=args.timeout_ms,
            initial_wait_ms=args.wait_ms,
            scroll_rounds=args.scroll_rounds,
            scroll_wait_ms=args.scroll_wait_ms,
        )
        assist_bundle = _refresh_pinterest_assist_outputs(
            visuals_dir=visuals_dir,
            brand_profile=brand_profile,
            query_report=report,
            project_dir=project_dir,
            captured_candidates=_capture_map_from_report(capture_report),
        )
        print(
            f"[capture-pinterest] {capture_report['captured_count']}개 candidate 저장 완료 "
            f"({assist_bundle['plan']['capture_progress']['capture_root']})"
        )
        for query_result in capture_report["queries"][: min(10, len(capture_report["queries"]))]:
            print(f"  {query_result['query_id']}: {len(query_result['captured_candidates'])} captured | {query_result['search_url']}")
            for warning in query_result["warnings"][:2]:
                print(f"     - {warning}")
        print(f"  -> Candidate manifest: {visuals_dir}/pinterest_candidate_manifest.json")
        print(f"  -> Selection manifest: {visuals_dir}/pinterest_selection_manifest.json")
        return

    if args.command == "select-pinterest-candidates":
        brand_profile_path, project_dir, manifest = _resolve_brand_profile_target(
            brand_profile_arg=args.brand_profile,
            project_dir_arg=args.project_dir,
        )
        brand_profile = load_brand_profile(brand_profile_path)
        visuals_dir = _resolve_support_output_dir(
            raw_output=args.output_dir,
            project_dir=project_dir,
            manifest=manifest,
            folder_name="visuals",
        )
        query_report = _read_json_if_exists(visuals_dir / "visual_query_suggestions.json")
        candidate_manifest = _read_json_if_exists(visuals_dir / "pinterest_candidate_manifest.json")
        selection_manifest = _read_json_if_exists(visuals_dir / "pinterest_selection_manifest.json")
        if not isinstance(query_report, dict):
            raise SystemExit(f"visual_query_suggestions.json 을 찾을 수 없습니다: {visuals_dir}")
        if not isinstance(candidate_manifest, dict):
            raise SystemExit(f"pinterest_candidate_manifest.json 을 찾을 수 없습니다: {visuals_dir}")
        if not isinstance(selection_manifest, dict):
            raise SystemExit(f"pinterest_selection_manifest.json 을 찾을 수 없습니다: {visuals_dir}")

        updated_selection_manifest = _apply_pinterest_candidate_selection_updates(
            candidate_manifest=candidate_manifest,
            existing_selection_manifest=selection_manifest,
            candidate_ids=args.candidate,
            reason=args.reason,
            note=args.note,
        )
        assist_bundle = _refresh_pinterest_assist_outputs(
            visuals_dir=visuals_dir,
            brand_profile=brand_profile,
            query_report=query_report,
            project_dir=project_dir,
            existing_candidate_manifest=candidate_manifest,
            existing_selection_manifest=updated_selection_manifest,
        )
        print(f"[select-pinterest-candidates] {len(_dedupe_preserve_order(args.candidate))}개 candidate 선택 완료")
        print(f"  -> Selection manifest: {visuals_dir}/pinterest_selection_manifest.json")
        print(f"  -> selected {assist_bundle['plan']['capture_progress']['selected_count']} / promoted {assist_bundle['plan']['capture_progress']['promoted_count']}")

        if args.sync_sources:
            raw_profile = json.loads(brand_profile_path.read_text(encoding="utf-8"))
            sync_result = _sync_pinterest_selected_sources(
                raw_brand_profile=raw_profile,
                selection_manifest=assist_bundle["selection_manifest"],
                base_dir=project_dir or brand_profile_path.parent,
            )
            write_json(brand_profile_path, raw_profile)
            brand_profile = load_brand_profile(brand_profile_path)
            assist_bundle = _refresh_pinterest_assist_outputs(
                visuals_dir=visuals_dir,
                brand_profile=brand_profile,
                query_report=query_report,
                project_dir=project_dir,
                existing_candidate_manifest=assist_bundle["candidate_manifest"],
                existing_selection_manifest=assist_bundle["selection_manifest"],
            )
            print(
                f"  -> visual_reference.sources 동기화: {sync_result['selected_count']}개 선택 / "
                f"{sync_result['managed_source_count']}개 Pinterest source 반영"
            )
            print(f"  -> {brand_profile_path} 업데이트 완료")
        return

    if args.command == "sync-pinterest-selection":
        brand_profile_path, project_dir, manifest = _resolve_brand_profile_target(
            brand_profile_arg=args.brand_profile,
            project_dir_arg=args.project_dir,
        )
        brand_profile = load_brand_profile(brand_profile_path)
        visuals_dir = _resolve_support_output_dir(
            raw_output=args.output_dir,
            project_dir=project_dir,
            manifest=manifest,
            folder_name="visuals",
        )
        spec_path = _resolve_spec_path(project_dir, None)
        query_report = _load_or_build_query_report(
            brand_profile=brand_profile,
            visuals_dir=visuals_dir,
            project_dir=project_dir,
            spec_path=spec_path,
            refresh=False,
        )
        write_json(visuals_dir / "visual_query_suggestions.json", query_report)
        selection_manifest = _read_json_if_exists(visuals_dir / "pinterest_selection_manifest.json")
        candidate_manifest = _read_json_if_exists(visuals_dir / "pinterest_candidate_manifest.json")
        if not isinstance(selection_manifest, dict):
            raise SystemExit(f"pinterest_selection_manifest.json 을 찾을 수 없습니다: {visuals_dir}")

        raw_profile = json.loads(brand_profile_path.read_text(encoding="utf-8"))
        sync_result = _sync_pinterest_selected_sources(
            raw_brand_profile=raw_profile,
            selection_manifest=selection_manifest,
            base_dir=project_dir or brand_profile_path.parent,
        )
        write_json(brand_profile_path, raw_profile)
        brand_profile = load_brand_profile(brand_profile_path)
        assist_bundle = _refresh_pinterest_assist_outputs(
            visuals_dir=visuals_dir,
            brand_profile=brand_profile,
            query_report=query_report,
            project_dir=project_dir,
            existing_candidate_manifest=candidate_manifest,
            existing_selection_manifest=selection_manifest,
        )
        print(
            f"[sync-pinterest-selection] visual_reference.sources 동기화 완료: "
            f"selected {sync_result['selected_count']} / managed {sync_result['managed_source_count']}"
        )
        print(f"  -> {brand_profile_path}")
        print(f"  -> promoted {assist_bundle['plan']['capture_progress']['promoted_count']}")
        return

    if args.command == "init":
        result = scaffold_project(
            project_dir=Path(args.project_dir),
            brand_name=args.brand_name,
            system_name=args.system_name,
            product_summary=args.product_summary,
            seed_urls=args.seed_urls,
            kb_dir=args.kb_dir,
            force=args.force,
        )
        print(f"[init] 프로젝트 생성 완료: {result['project_dir']}")
        print("  -> brand_profile.json 을 열어 브랜드 정보를 입력하세요.")
        return

    if args.command == "init-agent-pack":
        scaffold_agent_pack(
            target_repo=Path(args.target_repo),
            artifact_dir=args.artifact_dir,
            targets=[item.strip() for item in args.targets.split(",") if item.strip()],
            force=args.force,
        )
        print(f"[init-agent-pack] 에이전트 팩 생성 완료: {args.target_repo}")
        return

    if args.command == "synthesize":
        brand_profile = load_brand_profile(Path(args.brand_profile))
        references_path = output_dir / "references.jsonl"
        documents_path = output_dir / "all_documents.jsonl"
        if not references_path.exists() or not documents_path.exists():
            raise SystemExit("Run the crawl pipeline first so references and documents exist.")

        references = [
            ReferenceLink(**json.loads(line))
            for line in references_path.read_text(encoding="utf-8").splitlines()
            if line.strip()
        ]
        documents = [
            DocumentRecord(**json.loads(line))
            for line in documents_path.read_text(encoding="utf-8").splitlines()
            if line.strip()
        ]
        build_blueprint(output_dir, brand_profile, references, documents)
        print(f"[synthesize] 블루프린트 재생성 완료 ({output_dir}/blueprint/)")
        return

    if args.command == "run-project":
        project_dir = Path(args.project_dir)
        manifest = load_project(project_dir)
        kb_dir = resolve_kb_dir(project_dir, manifest, args.kb_dir)
        references, documents, kb_manifest = load_knowledge_base(kb_dir)
        brand_profile_path = project_dir / manifest["brand_profile"]
        brand_profile = load_brand_profile(brand_profile_path)
        _warn_placeholder_profile(brand_profile)
        build_root = ensure_dir(project_dir / manifest.get("build_dir", "build"))
        output_dir = ensure_dir(build_root / "system")
        write_jsonl(output_dir / "references.jsonl", [reference.to_dict() for reference in references])
        write_jsonl(output_dir / "all_documents.jsonl", [document.to_dict() for document in documents])
        if (kb_dir / "ontology").exists():
            shutil.copytree(kb_dir / "ontology", output_dir / "ontology", dirs_exist_ok=True)
        if (kb_dir / "css_extraction").exists():
            shutil.copytree(kb_dir / "css_extraction", output_dir / "css_extraction", dirs_exist_ok=True)
            css_summary_path = kb_dir / "css_extraction" / "extraction_summary.json"
            if css_summary_path.exists():
                css_summary = json.loads(css_summary_path.read_text(encoding="utf-8"))
                var_info = css_summary.get("var_resolution", {})
                brand_info = css_summary.get("brand_colors", {})
                typo_info = css_summary.get("typography", {})
                print(
                    f"  CSS 추출 (KB): {css_summary.get('css_file_count', 0)}개 파일 | "
                    f"var {var_info.get('resolved_count', 0)}/{var_info.get('total_vars', 0)}개 | "
                    f"브랜드색 {brand_info.get('total_candidates', 0)}개 | "
                    f"타이포 {typo_info.get('scale_entries', 0)}개"
                )
        else:
            print("  CSS 추출 (KB): 없음 — KB를 재빌드하면 자동 수집됩니다")
        print(f"  폰트 결정: {', '.join([role for role in ['heading', 'body', 'mono'] if brand_profile.get('_resolved_font_system', {}).get(role)])}")
        color_ref = brand_profile.get('_resolved_color_reference')
        if color_ref:
            active_roles = color_ref.get('palette_roles', {})
            print(f"  색상 결정: {len(active_roles)}개 role 활성화")
        else:
            print("  색상 결정: 실행 안 됨 (brand_profile.color_reference가 설정되지 않음)")
        visual_ref = brand_profile.get('_resolved_visual_reference')
        if visual_ref:
            coverage = visual_ref.get("coverage", {})
            motifs = visual_ref.get("visual_motifs", {}) or {}
            layout_cues = visual_ref.get("layout_cues", []) or []
            top_layout = layout_cues[0]["id"] if layout_cues else "n/a"
            print(
                f"  시각 레퍼런스: 소스 {coverage.get('source_count', 0)}개 | "
                f"이미지 {coverage.get('image_count', 0)}개 | "
                f"density {(motifs.get('density') or {}).get('value', 'n/a')} | "
                f"layout {top_layout}"
            )
        elif brand_profile.get("visual_reference"):
            print("  시각 레퍼런스: 설정됨, 하지만 유효한 로컬 이미지가 아직 해석되지 않음")
        visual_asset_manifests = brand_profile.get("_generated_visual_asset_manifests", [])
        if visual_asset_manifests:
            asset_count = sum(len(manifest.get("assets", []) or []) for manifest in visual_asset_manifests)
            print(f"  생성 이미지 manifest: {len(visual_asset_manifests)}개 | asset {asset_count}개 자동 승격")
        identity_assets = brand_profile.get("_identity_assets", [])
        if identity_assets:
            print(f"  브랜드 identity asset: {len(identity_assets)}개 자동 승격")

        spec_file = project_dir / "spec.md"
        if not spec_file.exists():
            spec_file = project_dir / "PRD.md"
        detected_patterns: list[dict] = []
        component_list: list[dict] = []
        if spec_file.exists():
            detected_patterns = analyze_spec_file(spec_file)
            if detected_patterns:
                component_list = build_component_list(detected_patterns)
                brand_profile["_spec_components"] = component_list
                brand_profile["_spec_detected_patterns"] = detected_patterns

        build_blueprint(
            output_dir=output_dir,
            brand_profile=brand_profile,
            references=references,
            documents=documents,
        )
        write_json(
            build_root / "project_summary.json",
            {
                "project_dir": str(project_dir),
                "kb_dir": str(kb_dir),
                "reference_count": len(references),
                "document_count": len(documents),
                "kb_built_at": kb_manifest.get("built_at"),
                "output_dir": str(output_dir),
            },
        )
        inventory_path = output_dir / "blueprint" / "component_inventory.json"
        inventory_data = json.loads(inventory_path.read_text(encoding="utf-8")) if inventory_path.exists() else {}
        specs_source = _component_specs_source_from_inventory(component_list, inventory_data)
        if specs_source:
            bp_path = output_dir / "blueprint" / "design_system_blueprint.json"
            blueprint_data = {}
            if bp_path.exists():
                blueprint_data = json.loads(bp_path.read_text(encoding="utf-8"))
            specs_data = generate_component_specs(
                brand_profile=brand_profile,
                blueprint=blueprint_data,
                component_list=specs_source,
                documents=documents,
            )
            write_component_specs(output_dir, specs_data)
            print(f"  -> 설계서({spec_file.name}) + inventory에서 {len(specs_source)}개 컴포넌트 스펙 자동 생성")

        print(f"[run-project] 시스템 산출물 생성 완료: {output_dir}/blueprint/")
        print(f"  -> 레퍼런스: {len(references)}개 | 문서: {len(documents)}개")
        print("  -> system_spec.md 를 확인하세요.")
        return

    import httpx

    headers = {
        "User-Agent": "Mozilla/5.0 (compatible; DesignOntologyHarness/0.1)",
    }
    with httpx.Client(headers=headers, follow_redirects=True) as client:
        if args.command == "build-kb":
            seed_urls = list(args.seed_urls)
            if args.seeds_file:
                seeds_file = Path(args.seeds_file)
                seed_urls.extend(
                    [
                        line.strip()
                        for line in seeds_file.read_text(encoding="utf-8").splitlines()
                        if line.strip() and not line.strip().startswith("#")
                    ]
                )
            if not seed_urls:
                raise SystemExit("Provide at least one --seed-url or a --seeds-file.")
            print(f"[build-kb] {len(seed_urls)}개 시드 URL에서 KB 빌드 시작...")
            manifest = build_knowledge_base(
                client=client,
                seed_urls=seed_urls,
                kb_dir=Path(args.kb_dir),
                max_sources=args.max_sources,
                max_pages_per_source=args.max_pages_per_source,
                max_depth=args.max_depth,
            )
            print(f"[build-kb] KB 빌드 완료: {args.kb_dir}")
            print(f"  -> 시드: {manifest['seed_count']}개 | 레퍼런스: {manifest['reference_count']}개 | 문서: {manifest['document_count']}개")
            return

        if args.command == "extract-seed":
            from .seed_article import fetch_seed_article

            seed_article = fetch_seed_article(client, args.seed_url)
            write_json(output_dir / "seed_article.json", seed_article.to_dict())
            write_jsonl(
                output_dir / "references.jsonl",
                [reference.to_dict() for reference in seed_article.references],
            )
            print(f"[extract-seed] 시드 추출 완료: {seed_article.title}")
            print(f"  -> 레퍼런스 {len(seed_article.references)}개 발견 ({output_dir})")
            return

        from .cli_shared import run_pipeline

        result = run_pipeline(
            client=client,
            seed_url=args.seed_url,
            output_dir=output_dir,
            brand_profile_path=Path(args.brand_profile) if args.brand_profile else None,
            max_sources=args.max_sources,
            max_pages_per_source=args.max_pages_per_source,
            max_depth=args.max_depth,
        )
        print(f"[run] 파이프라인 완료: {output_dir}")
        print(f"  -> 레퍼런스: {len(result['references'])}개 | 문서: {len(result['documents'])}개")
        if args.brand_profile:
            print(f"  -> 블루프린트: {output_dir}/blueprint/")


_PLACEHOLDER_PATTERNS = [
    "Describe your",
    "Describe the",
    "List the core",
]


def _warn_placeholder_profile(profile: dict) -> None:
    found = []
    for key, value in profile.items():
        if key.startswith("_"):
            continue
        texts = []
        if isinstance(value, str):
            texts = [value]
        elif isinstance(value, list):
            texts = [item for item in value if isinstance(item, str)]
        for text in texts:
            if any(pattern in text for pattern in _PLACEHOLDER_PATTERNS):
                found.append(key)
                break
    if found:
        print(f"[warning] brand_profile.json에 아직 기본값이 남아 있는 항목: {', '.join(found)}")
        print("  -> 실제 브랜드 정보를 입력해야 의미 있는 산출물이 나옵니다.")


def _resolve_brand_profile_target(
    brand_profile_arg: str | None,
    project_dir_arg: str | None,
) -> tuple[Path, Path | None, dict | None]:
    if project_dir_arg:
        project_dir = Path(project_dir_arg)
        manifest = load_project(project_dir)
        brand_profile_path = project_dir / manifest["brand_profile"]
        if not brand_profile_path.exists():
            raise SystemExit(f"brand_profile.json 을 찾을 수 없습니다: {brand_profile_path}")
        return brand_profile_path, project_dir, manifest

    if not brand_profile_arg:
        raise SystemExit("Provide either --brand-profile or --project-dir.")

    brand_profile_path = Path(brand_profile_arg)
    if not brand_profile_path.exists():
        raise SystemExit(f"파일을 찾을 수 없습니다: {brand_profile_path}")
    return brand_profile_path, None, None


def _resolve_support_output_dir(
    raw_output: str | None,
    project_dir: Path | None,
    manifest: dict | None,
    folder_name: str,
) -> Path:
    if raw_output:
        return ensure_dir(Path(raw_output))
    if project_dir and manifest:
        build_root = ensure_dir(project_dir / manifest.get("build_dir", "build"))
        return ensure_dir(build_root / folder_name)
    return ensure_dir(Path("data") / folder_name)


def _resolve_spec_path(project_dir: Path | None, explicit_spec: str | None) -> Path | None:
    if explicit_spec:
        return Path(explicit_spec)
    if not project_dir:
        return None
    for candidate in [project_dir / "spec.md", project_dir / "PRD.md"]:
        if candidate.exists():
            return candidate
    return None


def _load_or_build_query_report(
    brand_profile: dict,
    visuals_dir: Path,
    project_dir: Path | None,
    spec_path: Path | None,
    refresh: bool,
) -> dict:
    query_report_path = visuals_dir / "visual_query_suggestions.json"
    if query_report_path.exists() and not refresh:
        return json.loads(query_report_path.read_text(encoding="utf-8"))
    spec_text = spec_path.read_text(encoding="utf-8") if spec_path and spec_path.exists() else None
    return generate_visual_queries(brand_profile=brand_profile, spec_text=spec_text)


def _refresh_pinterest_assist_outputs(
    visuals_dir: Path,
    brand_profile: dict,
    query_report: dict,
    project_dir: Path | None,
    captured_candidates: dict[str, list[dict]] | None = None,
    existing_candidate_manifest: dict | None = None,
    existing_selection_manifest: dict | None = None,
) -> dict:
    if existing_candidate_manifest is None:
        existing_candidate_manifest = _read_json_if_exists(visuals_dir / "pinterest_candidate_manifest.json")
    if existing_selection_manifest is None:
        existing_selection_manifest = _read_json_if_exists(visuals_dir / "pinterest_selection_manifest.json")
    assist_bundle = build_pinterest_assist_bundle(
        brand_profile=brand_profile,
        query_report=query_report,
        project_dir=project_dir,
        captured_candidates=captured_candidates,
        existing_candidate_manifest=existing_candidate_manifest,
        existing_selection_manifest=existing_selection_manifest,
    )
    write_json(visuals_dir / "pinterest_assist_plan.json", assist_bundle["plan"])
    write_json(visuals_dir / "pinterest_candidate_manifest.json", assist_bundle["candidate_manifest"])
    write_json(visuals_dir / "pinterest_selection_manifest.json", assist_bundle["selection_manifest"])
    return assist_bundle


def _capture_map_from_report(capture_report: dict) -> dict[str, list[dict]]:
    captured: dict[str, list[dict]] = {}
    for query_result in capture_report.get("queries", []):
        query_id = str(query_result.get("query_id", "")).strip()
        if not query_id:
            continue
        captured[query_id] = list(query_result.get("captured_candidates", []))
    return captured


def _read_json_if_exists(path: Path) -> dict | None:
    if not path.exists():
        return None
    return json.loads(path.read_text(encoding="utf-8"))


def _apply_pinterest_candidate_selection_updates(
    *,
    candidate_manifest: dict,
    existing_selection_manifest: dict,
    candidate_ids: list[str],
    reason: str | None,
    note: str | None,
) -> dict:
    selected_candidate_ids = _dedupe_preserve_order(candidate_ids)
    candidate_lookup: dict[str, tuple[str, dict]] = {}
    captured_count = 0
    for query in candidate_manifest.get("queries", []):
        query_id = str(query.get("query_id", "")).strip()
        for candidate in query.get("candidates", []):
            candidate_id = str(candidate.get("candidate_id", "")).strip()
            if candidate.get("status") == "captured":
                captured_count += 1
            if candidate_id:
                candidate_lookup[candidate_id] = (query_id, candidate)

    missing_candidate_ids = [candidate_id for candidate_id in selected_candidate_ids if candidate_id not in candidate_lookup]
    if missing_candidate_ids:
        raise SystemExit(f"선택할 candidate_id 를 찾을 수 없습니다: {', '.join(missing_candidate_ids)}")

    updated_selection_manifest = deepcopy(existing_selection_manifest)
    query_lookup = {
        str(query.get("query_id", "")).strip(): query
        for query in updated_selection_manifest.get("queries", [])
        if str(query.get("query_id", "")).strip()
    }
    selected_by_query: dict[str, list[dict]] = {}
    for candidate_id in selected_candidate_ids:
        query_id, candidate = candidate_lookup[candidate_id]
        if candidate.get("status") != "captured" or not str(candidate.get("capture_path", "")).strip():
            raise SystemExit(f"candidate 가 아직 캡처되지 않았습니다: {candidate_id}")
        if query_id not in query_lookup:
            raise SystemExit(f"selection manifest 에 query 가 없습니다: {query_id}")
        selected_by_query.setdefault(query_id, []).append(candidate)

    for query_id, selected_candidates in selected_by_query.items():
        query_entry = query_lookup[query_id]
        existing_selected_by_candidate = {
            str(item.get("candidate_id", "")).strip(): item
            for item in query_entry.get("selected", [])
            if str(item.get("status", "")).strip().lower() == "selected" and str(item.get("candidate_id", "")).strip()
        }
        slot_count = len(query_entry.get("selected", []))
        if len(selected_candidates) > slot_count:
            raise SystemExit(
                f"{query_id} 는 최대 {slot_count}개까지 선택할 수 있습니다 "
                f"(요청 {len(selected_candidates)}개)."
            )

        updated_selected_entries: list[dict] = []
        for slot in range(1, slot_count + 1):
            selection_id = f"{query_id}-s{slot:02d}"
            if slot <= len(selected_candidates):
                candidate = selected_candidates[slot - 1]
                candidate_id = str(candidate.get("candidate_id", "")).strip()
                existing_selected = existing_selected_by_candidate.get(candidate_id, {})
                updated_selected_entries.append(
                    {
                        "selection_id": selection_id,
                        "status": "selected",
                        "candidate_id": candidate_id,
                        "reference_url": candidate.get("reference_url"),
                        "capture_path": candidate.get("capture_path"),
                        "usage_scope": "reference-analysis-only",
                        "redistribution_allowed": False,
                        "selection_reason": reason
                        or existing_selected.get("selection_reason")
                        or "Explicitly selected for promotion to visual_reference.sources.",
                        "notes": note if note is not None else existing_selected.get("notes") or candidate.get("notes"),
                        "promoted_to_sources": bool(existing_selected.get("promoted_to_sources", False)),
                    }
                )
                continue
            updated_selected_entries.append(_build_open_selection_manifest_entry(selection_id))
        query_entry["selected"] = updated_selected_entries

    has_selected_entries = any(
        str(item.get("status", "")).strip().lower() == "selected"
        for query in updated_selection_manifest.get("queries", [])
        for item in query.get("selected", [])
    )
    updated_selection_manifest["status"] = (
        "selected"
        if has_selected_entries
        else "ready-for-selection"
        if captured_count
        else "awaiting-selection"
    )
    return updated_selection_manifest


def _sync_pinterest_selected_sources(
    *,
    raw_brand_profile: dict,
    selection_manifest: dict,
    base_dir: Path,
) -> dict:
    visual_reference = raw_brand_profile.setdefault("visual_reference", {})
    capture_dir = str(selection_manifest.get("capture_dir", "")).strip() or "references/visual/pinterest-assisted"
    selected_paths = _dedupe_preserve_order(
        [
            str(selection.get("capture_path", "")).strip()
            for query in selection_manifest.get("queries", [])
            for selection in query.get("selected", [])
            if str(selection.get("status", "")).strip().lower() == "selected"
            and str(selection.get("capture_path", "")).strip()
        ]
    )

    preserved_sources: list[object] = []
    existing_sources = visual_reference.get("sources", [])
    if not isinstance(existing_sources, list):
        existing_sources = []
    for source in existing_sources:
        if _is_pinterest_managed_source_entry(source, capture_dir=capture_dir, base_dir=base_dir):
            continue
        preserved_sources.append(source)

    merged_sources = list(preserved_sources)
    existing_keys = {
        _source_entry_identity(source, base_dir=base_dir)
        for source in merged_sources
    }
    for capture_path in selected_paths:
        identity = _source_path_identity(capture_path, base_dir=base_dir)
        if identity in existing_keys:
            continue
        merged_sources.append(capture_path)
        existing_keys.add(identity)

    visual_reference["sources"] = merged_sources
    return {
        "selected_count": len(selected_paths),
        "managed_source_count": len(selected_paths),
        "total_source_count": len(merged_sources),
    }


def _build_open_selection_manifest_entry(selection_id: str) -> dict:
    return {
        "selection_id": selection_id,
        "status": "open",
        "candidate_id": None,
        "reference_url": None,
        "capture_path": None,
        "usage_scope": "reference-analysis-only",
        "redistribution_allowed": False,
        "selection_reason": None,
        "notes": None,
        "promoted_to_sources": False,
    }


def _dedupe_preserve_order(values: list[str]) -> list[str]:
    seen: set[str] = set()
    result: list[str] = []
    for value in values:
        normalized = str(value).strip()
        if not normalized or normalized in seen:
            continue
        seen.add(normalized)
        result.append(normalized)
    return result


def _is_pinterest_managed_source_entry(source: object, *, capture_dir: str, base_dir: Path) -> bool:
    raw_path = _source_entry_path(source)
    if not raw_path:
        return False
    source_identity = _source_path_identity(raw_path, base_dir=base_dir)
    capture_root_identity = _source_path_identity(capture_dir, base_dir=base_dir)
    return source_identity == capture_root_identity or source_identity.startswith(capture_root_identity + "/")


def _source_entry_identity(source: object, *, base_dir: Path) -> str:
    return _source_path_identity(_source_entry_path(source), base_dir=base_dir)


def _source_entry_path(source: object) -> str:
    if isinstance(source, str):
        return source.strip()
    if isinstance(source, dict):
        return str(source.get("path", "")).strip()
    return ""


def _source_path_identity(raw_path: str, *, base_dir: Path) -> str:
    path_text = str(raw_path).strip()
    if not path_text:
        return ""
    path = Path(path_text)
    if not path.is_absolute():
        path = (base_dir / path).resolve()
    else:
        path = path.resolve()
    return str(path)


def _write_visual_analysis_outputs(
    output_dir: Path,
    brand_profile_path: Path,
    visual_report: dict,
    issues: list[str],
    *,
    design_context_pack: dict | None = None,
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
        {
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
        },
    )


if __name__ == "__main__":
    main()
