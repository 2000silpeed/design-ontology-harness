from __future__ import annotations

import hashlib
import json
import re
import subprocess
from datetime import datetime, timezone
from html.parser import HTMLParser
from pathlib import Path
from typing import Any

from PIL import Image, UnidentifiedImageError

from .component_contracts import load_and_validate_component_contracts
from .component_runtime import (
    DEFAULT_COMPONENT_RUNTIME_MANIFEST,
    validate_component_runtime_conformance,
)
from .implementation_linter import lint_implementation
from .reference_fidelity import (
    DEFAULT_CONTRACT_PATH as DEFAULT_REFERENCE_FIDELITY_CONTRACT,
    DEFAULT_REPORT_PATH as DEFAULT_REFERENCE_FIDELITY_REPORT,
    validate_reference_fidelity_report,
)
from .screenshot_aesthetic import analyze_screenshot
from .style_fingerprint import check_style_divergence
from .utils import write_json
from .visual_evidence import (
    DEFAULT_BROWSER_EVIDENCE_BUNDLE,
    validate_browser_evidence_bundle,
)


SCREENSHOT_MANIFEST_SCHEMA = "production-ui-screenshots/v3"
IMPLEMENTATION_TREE_ALGORITHM = "sha256-runtime-tree-v1"
PRODUCTION_REVIEW_SCHEMA = "production-ui-review/v1"
REVIEW_ARTIFACT_SCHEMA = "production-ui-review-artifact/v1"
RUNTIME_CHECK_ARTIFACT_SCHEMA = "production-ui-runtime-check/v1"
REQUIRED_THEMES = {"light", "dark"}
REQUIRED_RUNTIME_CHECKS = {"interaction", "overflow", "accessibility"}
MIN_LUMINANCE_STD = 0.018
MIN_LUMINANCE_SPAN = 0.12
MIN_EDGE_DENSITY = 0.004
MIN_ACTIVE_CELL_SHARE = 0.035
SEMANTIC_REVIEW_METRICS = {
    "domain_fit",
    "keyword_alignment",
    "task_focus",
    "anti_keyword_avoidance",
    "reference_transformation",
}
SEMANTIC_REVIEW_PREFIXES = (
    "brand_keyword:",
    "brand_tone:",
    "anti_keyword:",
    "product_primitive:",
    "must_include:",
    "avoid_pattern:",
    "audience_need:",
)

RUNTIME_CODE_EXTENSIONS = {
    ".html",
    ".htm",
    ".css",
    ".scss",
    ".sass",
    ".less",
    ".js",
    ".mjs",
    ".cjs",
    ".ts",
    ".tsx",
    ".jsx",
    ".vue",
    ".svelte",
}
RUNTIME_REFERENCE_EXTENSIONS = RUNTIME_CODE_EXTENSIONS | {
    ".png",
    ".jpg",
    ".jpeg",
    ".webp",
    ".avif",
    ".gif",
    ".svg",
    ".ico",
    ".webmanifest",
    ".json",
    ".woff",
    ".woff2",
    ".ttf",
    ".otf",
}
RUNTIME_EXCLUDED_DIRS = {
    ".git",
    ".next",
    ".nuxt",
    ".pytest_cache",
    ".ruff_cache",
    "__pycache__",
    "coverage",
    "node_modules",
    "screenshots",
}
RUNTIME_EXCLUDED_PREFIXES = {
    ("build", "system"),
}
VISUAL_ASSET_MANIFEST_PATHS = (
    Path("public/generated/design-system/manifest.json"),
    Path("design-system/generated_visual_assets.json"),
)
QUOTED_RUNTIME_REFERENCE_RE = re.compile(
    r'''["'](?P<path>[^"'\s?#]+\.(?:html?|css|scss|sass|less|m?js|cjs|tsx?|jsx|vue|svelte|png|jpe?g|webp|avif|gif|svg|ico|webmanifest|json|woff2?|ttf|otf))(?:[?#][^"']*)?["']''',
    re.IGNORECASE,
)
UNQUOTED_URL_REFERENCE_RE = re.compile(
    r"url\(\s*(?P<path>[^)'\"\s?#]+\.(?:css|png|jpe?g|webp|avif|gif|svg|ico|woff2?|ttf|otf))(?:[?#][^)'\"\s]*)?\s*\)",
    re.IGNORECASE,
)


class _RuntimeHTMLReferenceParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.references: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        del tag
        for name, value in attrs:
            if not value:
                continue
            if name.lower() in {"src", "href"}:
                self.references.append(value.strip())
            elif name.lower() == "srcset":
                for candidate in value.split(","):
                    reference = candidate.strip().split(maxsplit=1)[0]
                    if reference:
                        self.references.append(reference)


def _html_runtime_references(text: str) -> list[str]:
    parser = _RuntimeHTMLReferenceParser()
    parser.feed(text)
    return parser.references


def _runtime_implementation_tree(target_repo: Path) -> dict[str, Any]:
    """Hash the runtime source graph without hashing production evidence itself."""

    target = target_repo.resolve()
    if not target.is_dir():
        raise ValueError(f"target repository does not exist: {target}")

    runtime_files: set[Path] = set()
    pending: list[Path] = []

    def excluded(relative: Path) -> bool:
        return (
            any(part in RUNTIME_EXCLUDED_DIRS for part in relative.parts)
            or any(relative.parts[: len(prefix)] == prefix for prefix in RUNTIME_EXCLUDED_PREFIXES)
        )

    def add(path: Path, *, required: bool, source: str) -> None:
        candidate = path.resolve()
        try:
            relative = candidate.relative_to(target)
        except ValueError as exc:
            if required:
                raise ValueError(
                    f"runtime reference escapes the target repository: {source} -> {path}"
                ) from exc
            return
        if excluded(relative):
            if required:
                raise ValueError(f"runtime reference points into excluded evidence/cache data: {source} -> {path}")
            return
        if not candidate.is_file():
            if required:
                raise ValueError(f"runtime reference does not exist: {source} -> {path}")
            return
        if candidate in runtime_files:
            return
        runtime_files.add(candidate)
        pending.append(candidate)

    for path in target.rglob("*"):
        if not path.is_file() or path.suffix.lower() not in RUNTIME_CODE_EXTENSIONS:
            continue
        relative = path.relative_to(target)
        if excluded(relative):
            continue
        add(path, required=True, source="runtime source scan")

    for relative in VISUAL_ASSET_MANIFEST_PATHS:
        manifest_path = target / relative
        if manifest_path.exists():
            add(manifest_path, required=True, source="visual asset manifest")

    while pending:
        source_path = pending.pop()
        try:
            text = source_path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        source_relative = source_path.relative_to(target)
        is_visual_manifest = source_relative in VISUAL_ASSET_MANIFEST_PATHS
        references = [] if is_visual_manifest else [
            match.group("path")
            for pattern in (QUOTED_RUNTIME_REFERENCE_RE, UNQUOTED_URL_REFERENCE_RE)
            for match in pattern.finditer(text)
        ]
        if not is_visual_manifest and source_path.suffix.lower() in {".html", ".htm"}:
            references.extend(_html_runtime_references(text))
        for raw_reference in references:
            reference = raw_reference.strip()
            if not reference:
                continue
            if reference.startswith(("http://", "https://", "//")):
                raise ValueError(
                    "remote runtime reference cannot be content-bound; copy it into the target repository "
                    f"or replace it with a separately verified local asset: {source_relative.as_posix()} -> {reference}"
                )
            if reference.startswith("data:"):
                continue
            reference = reference.split("#", 1)[0].split("?", 1)[0]
            if Path(reference).suffix.lower() not in RUNTIME_REFERENCE_EXTENSIONS:
                continue
            referenced = (
                target / reference.lstrip("/")
                if reference.startswith("/")
                else source_path.parent / reference
            )
            add(referenced, required=True, source=source_path.relative_to(target).as_posix())

        if is_visual_manifest:
            try:
                manifest = json.loads(text)
            except json.JSONDecodeError as exc:
                raise ValueError(
                    f"visual asset manifest is unreadable: {source_relative}"
                ) from exc
            for record in manifest.get("assets", []) if isinstance(manifest, dict) else []:
                if not isinstance(record, dict) or not record.get("asset_path"):
                    continue
                add(
                    target / str(record["asset_path"]),
                    required=record.get("status") in {"accepted", "integrated"},
                    source=source_relative.as_posix(),
                )

    if not runtime_files:
        raise ValueError("no runtime implementation files were found in the target repository")

    files: list[dict[str, Any]] = []
    latest_path: str | None = None
    latest_mtime_ns = -1
    for path in sorted(runtime_files, key=lambda item: item.relative_to(target).as_posix()):
        stat = path.stat()
        relative = path.relative_to(target).as_posix()
        files.append(
            {
                "path": relative,
                "sha256": _sha256(path),
                "size_bytes": stat.st_size,
            }
        )
        if stat.st_mtime_ns > latest_mtime_ns:
            latest_mtime_ns = stat.st_mtime_ns
            latest_path = relative

    canonical = json.dumps(
        files,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")
    return {
        "algorithm": IMPLEMENTATION_TREE_ALGORITHM,
        "sha256": hashlib.sha256(canonical).hexdigest(),
        "file_count": len(files),
        "files": files,
        "latest_runtime_path": latest_path,
        "latest_runtime_mtime_ns": latest_mtime_ns,
        "latest_runtime_modified_at": datetime.fromtimestamp(
            latest_mtime_ns / 1_000_000_000,
            timezone.utc,
        ).isoformat(timespec="microseconds"),
    }


def _assert_screenshot_freshness(screenshot: Path, implementation_tree: dict[str, Any]) -> None:
    screenshot_mtime_ns = screenshot.stat().st_mtime_ns
    latest_runtime_mtime_ns = int(implementation_tree.get("latest_runtime_mtime_ns") or 0)
    if screenshot_mtime_ns < latest_runtime_mtime_ns:
        raise ValueError(
            "screenshot is older than the runtime implementation; recapture after the latest runtime change "
            f"({implementation_tree.get('latest_runtime_path')})"
        )


def record_screenshot_evidence(
    *,
    manifest_path: Path,
    project: str,
    target_repo: Path,
    screenshot_path: Path,
    route: str,
    state: str,
    theme: str,
    implementation_sha: str,
    required_themes: list[str] | None = None,
) -> dict[str, Any]:
    if theme not in {"light", "dark"}:
        raise ValueError("theme must be light or dark")
    if not route.strip() or not state.strip():
        raise ValueError("route and state are required")
    if not implementation_sha.strip():
        raise ValueError("implementation_sha is required")
    if required_themes is not None and (
        not isinstance(required_themes, list)
        or any(not isinstance(item, str) for item in required_themes)
        or set(required_themes) != REQUIRED_THEMES
    ):
        raise ValueError("required_themes must contain both light and dark")
    screenshot = screenshot_path.resolve()
    if not screenshot.is_file():
        raise ValueError(f"screenshot not found: {screenshot}")
    try:
        with Image.open(screenshot) as image:
            width, height = image.size
    except (UnidentifiedImageError, OSError) as exc:
        raise ValueError(f"invalid screenshot: {screenshot}") from exc
    visual_signal = _visual_signal(screenshot)
    signal_errors = _visual_signal_errors(visual_signal)
    if signal_errors:
        raise ValueError("screenshot lacks minimum visual information: " + "; ".join(signal_errors))
    implementation_tree = _runtime_implementation_tree(target_repo)
    _assert_screenshot_freshness(screenshot, implementation_tree)

    target = target_repo.resolve()
    try:
        stored_path = screenshot.relative_to(target).as_posix()
    except ValueError:
        stored_path = str(screenshot)
    manifest = _load_optional_manifest(manifest_path) or {
        "schema_version": SCREENSHOT_MANIFEST_SCHEMA,
        "project": project,
        "implementation_sha": implementation_sha,
        "implementation_tree": implementation_tree,
        "required_themes": required_themes or ["light", "dark"],
        "screenshots": [],
    }
    if manifest.get("schema_version") != SCREENSHOT_MANIFEST_SCHEMA:
        raise ValueError(
            f"existing screenshot manifest must use {SCREENSHOT_MANIFEST_SCHEMA}; re-record the evidence"
        )
    if manifest.get("project") != project:
        raise ValueError("existing screenshot manifest belongs to a different project")
    if manifest.get("implementation_sha") != implementation_sha:
        raise ValueError("all screenshot evidence must use the same implementation_sha")
    manifest_tree = manifest.get("implementation_tree")
    if not isinstance(manifest_tree, dict):
        raise ValueError("existing screenshot manifest has no implementation_tree; re-record the evidence")
    if manifest_tree.get("sha256") != implementation_tree["sha256"]:
        raise ValueError(
            "runtime implementation changed after screenshot evidence recording; "
            "start a new manifest and recapture every screenshot"
        )
    screenshot_stat = screenshot.stat()
    entry = {
        "path": stored_path,
        "route": route.strip(),
        "state": state.strip(),
        "theme": theme,
        "implementation_sha": implementation_sha,
        "implementation_tree_sha256": implementation_tree["sha256"],
        "runtime_latest_mtime_ns": implementation_tree["latest_runtime_mtime_ns"],
        "viewport": {"width": width, "height": height},
        "sha256": _sha256(screenshot),
        "screenshot_mtime_ns": screenshot_stat.st_mtime_ns,
        "visual_signal": visual_signal,
        "captured_at": datetime.fromtimestamp(
            screenshot_stat.st_mtime,
            timezone.utc,
        ).isoformat(timespec="microseconds"),
    }
    key = (entry["route"], entry["state"], entry["theme"], width, height)
    entries = [item for item in manifest.get("screenshots", []) if isinstance(item, dict)]
    entries = [
        item
        for item in entries
        if (item.get("route"), item.get("state"), item.get("theme"), (item.get("viewport") or {}).get("width"), (item.get("viewport") or {}).get("height")) != key
    ]
    entries.append(entry)
    manifest["screenshots"] = entries
    manifest["required_themes"] = required_themes or manifest.get("required_themes") or ["light", "dark"]
    manifest_path.parent.mkdir(parents=True, exist_ok=True)
    write_json(manifest_path, manifest)
    return entry


def validate_screenshot_manifest(
    manifest_path: Path,
    *,
    project: str,
    target_repo: Path,
) -> dict[str, Any]:
    errors: list[str] = []
    try:
        manifest = _load_required_manifest(manifest_path)
    except (ValueError, json.JSONDecodeError) as exc:
        return {"ok": False, "errors": [str(exc)], "screenshot_count": 0, "resolved_paths": []}
    if manifest.get("schema_version") != SCREENSHOT_MANIFEST_SCHEMA:
        errors.append(f"schema_version must be {SCREENSHOT_MANIFEST_SCHEMA}")
    if manifest.get("project") != project:
        errors.append(f"manifest project must be {project}")
    implementation_sha = str(manifest.get("implementation_sha") or "")
    if not implementation_sha:
        errors.append("implementation_sha is required")
    resolved_implementation_sha = _verify_git_sha(target_repo, implementation_sha, errors)
    declared_tree = manifest.get("implementation_tree")
    if not isinstance(declared_tree, dict):
        errors.append("implementation_tree is required; re-record screenshots with the v3 recorder")
        declared_tree = {}
    if declared_tree.get("algorithm") != IMPLEMENTATION_TREE_ALGORITHM:
        errors.append(f"implementation_tree.algorithm must be {IMPLEMENTATION_TREE_ALGORITHM}")
    try:
        current_tree = _runtime_implementation_tree(target_repo)
    except (OSError, ValueError) as exc:
        errors.append(str(exc))
        current_tree = {}
    if declared_tree.get("sha256") != current_tree.get("sha256"):
        errors.append("implementation_tree.sha256 does not match the current runtime implementation")
    if declared_tree.get("file_count") != current_tree.get("file_count"):
        errors.append("implementation_tree.file_count does not match the current runtime implementation")
    if declared_tree.get("files") != current_tree.get("files"):
        errors.append("implementation_tree.files do not match the current runtime implementation")

    entries = manifest.get("screenshots") if isinstance(manifest.get("screenshots"), list) else []
    if not isinstance(manifest.get("screenshots"), list) or not entries:
        errors.append("screenshots must be a non-empty list")
    resolved_paths: list[str] = []
    validated_entries: list[dict[str, Any]] = []
    coverage: dict[tuple[str, str, str], set[str]] = {}
    signature_themes: dict[tuple[str, str, int, int], set[str]] = {}
    seen_keys: set[tuple[Any, ...]] = set()
    seen_hashes: dict[str, tuple[str, str, str, int, int]] = {}
    for index, entry in enumerate(entries):
        prefix = f"screenshots[{index}]"
        if not isinstance(entry, dict):
            errors.append(f"{prefix} must be an object")
            continue
        for field in (
            "path",
            "route",
            "state",
            "theme",
            "implementation_sha",
            "implementation_tree_sha256",
            "runtime_latest_mtime_ns",
            "viewport",
            "sha256",
            "screenshot_mtime_ns",
            "captured_at",
        ):
            if not entry.get(field):
                errors.append(f"{prefix}.{field} is required")
        route = str(entry.get("route") or "").strip()
        state = str(entry.get("state") or "").strip()
        if not route:
            errors.append(f"{prefix}.route must not be blank")
        if not state:
            errors.append(f"{prefix}.state must not be blank")
        theme = entry.get("theme")
        if theme not in {"light", "dark"}:
            errors.append(f"{prefix}.theme must be light or dark")
        if entry.get("implementation_sha") != implementation_sha:
            errors.append(f"{prefix}.implementation_sha must match the manifest implementation_sha")
        if entry.get("implementation_tree_sha256") != declared_tree.get("sha256"):
            errors.append(
                f"{prefix}.implementation_tree_sha256 must match the manifest implementation_tree"
            )
        if entry.get("runtime_latest_mtime_ns") != declared_tree.get("latest_runtime_mtime_ns"):
            errors.append(
                f"{prefix}.runtime_latest_mtime_ns must match the manifest implementation_tree"
            )
        if not _is_timezone_timestamp(entry.get("captured_at")):
            errors.append(f"{prefix}.captured_at must be an ISO-8601 timestamp with a timezone")
        path = Path(str(entry.get("path") or ""))
        resolved = path.resolve() if path.is_absolute() else (target_repo / path).resolve()
        try:
            with Image.open(resolved) as image:
                actual_size = image.size
        except (FileNotFoundError, UnidentifiedImageError, OSError):
            errors.append(f"{prefix}.path is not a readable screenshot: {path}")
            continue
        resolved_paths.append(str(resolved))
        actual_screenshot_mtime_ns = resolved.stat().st_mtime_ns
        if entry.get("screenshot_mtime_ns") != actual_screenshot_mtime_ns:
            errors.append(f"{prefix}.screenshot_mtime_ns does not match the screenshot file")
        latest_runtime_mtime_ns = int(current_tree.get("latest_runtime_mtime_ns") or 0)
        if actual_screenshot_mtime_ns < latest_runtime_mtime_ns:
            errors.append(
                f"{prefix}.path is older than the current runtime implementation "
                f"({current_tree.get('latest_runtime_path')}); recapture it"
            )
        viewport = entry.get("viewport")
        if not isinstance(viewport, dict):
            errors.append(f"{prefix}.viewport must be an object")
            viewport = {}
        declared_size = (viewport.get("width"), viewport.get("height"))
        if declared_size != actual_size:
            errors.append(f"{prefix}.viewport does not match the screenshot dimensions")
        if entry.get("sha256") != _sha256(resolved):
            errors.append(f"{prefix}.sha256 does not match the screenshot")
        visual_signal = _visual_signal(resolved)
        for signal_error in _visual_signal_errors(visual_signal):
            errors.append(f"{prefix} lacks minimum visual information: {signal_error}")
        declared_signal = entry.get("visual_signal")
        if not isinstance(declared_signal, dict):
            errors.append(f"{prefix}.visual_signal is required")
        elif any(declared_signal.get(key) != value for key, value in visual_signal.items()):
            errors.append(f"{prefix}.visual_signal does not match the screenshot")
        size_class = "mobile" if actual_size[0] <= 480 else "desktop" if actual_size[0] >= 1024 else "intermediate"
        key = (route, state, theme, actual_size[0], actual_size[1])
        if key in seen_keys:
            errors.append(f"{prefix} duplicates an existing route/state/theme/viewport entry")
        seen_keys.add(key)
        coverage.setdefault((route, state, str(theme)), set()).add(size_class)
        signature_themes.setdefault((route, state, actual_size[0], actual_size[1]), set()).add(str(theme))
        sha = str(entry.get("sha256") or "")
        if sha in seen_hashes:
            previous = seen_hashes[sha]
            errors.append(
                f"{prefix}.sha256 duplicates screenshot content from "
                f"{previous[0]} / {previous[1]} / {previous[2]} / {previous[3]}x{previous[4]}"
            )
        else:
            seen_hashes[sha] = (route, state, str(theme), actual_size[0], actual_size[1])
        validated_entries.append(
            {
                "path": str(resolved),
                "route": route,
                "state": state,
                "theme": theme,
                "viewport": {"width": actual_size[0], "height": actual_size[1]},
                "sha256": sha,
                "visual_signal": visual_signal,
            }
        )

    required_themes = manifest.get("required_themes") or ["light", "dark"]
    if (
        not isinstance(required_themes, list)
        or any(not isinstance(theme, str) for theme in required_themes)
        or set(required_themes) != REQUIRED_THEMES
    ):
        errors.append("required_themes must contain exactly light and dark")
        required_theme_set = REQUIRED_THEMES
    else:
        required_theme_set = set(required_themes)
    route_states = sorted({(route, state) for route, state, _theme in coverage})
    for route, state in route_states:
        for theme in sorted(required_theme_set):
            classes = coverage.get((route, state, theme), set())
            if not {"mobile", "desktop"} <= classes:
                errors.append(
                    f"{route} / {state} / {theme} needs both mobile and desktop screenshots"
                )
    for signature, themes in sorted(signature_themes.items()):
        if themes != required_theme_set:
            route, state, width, height = signature
            missing = ", ".join(sorted(required_theme_set - themes))
            errors.append(
                f"{route} / {state} / {width}x{height} lacks symmetric theme coverage: {missing}"
            )
    return {
        "ok": not errors,
        "errors": errors,
        "screenshot_count": len(entries),
        "resolved_paths": resolved_paths,
        "implementation_sha": implementation_sha,
        "resolved_implementation_sha": resolved_implementation_sha,
        "implementation_tree_sha256": current_tree.get("sha256"),
        "implementation_tree_file_count": current_tree.get("file_count", 0),
        "latest_runtime_path": current_tree.get("latest_runtime_path"),
        "latest_runtime_mtime_ns": current_tree.get("latest_runtime_mtime_ns"),
        "screenshots": validated_entries,
        "route_states": [
            {"route": route, "state": state}
            for route, state in route_states
        ],
    }


def verify_production_ui(
    *,
    project_dir: Path,
    target_repo: Path,
    screenshot_manifest_path: Path,
    aesthetic_report_path: Path,
    registry_path: Path,
    artifact_dir: str = "design-system",
    component_runtime_manifest_path: Path | None = None,
    browser_evidence_bundle_path: Path | None = None,
    reference_fidelity_contract_path: Path | None = None,
    reference_fidelity_report_path: Path | None = None,
) -> dict[str, Any]:
    project = project_dir.resolve()
    target = target_repo.resolve()
    gates: list[dict[str, Any]] = []

    def add_gate(name: str, ok: bool, errors: list[str], evidence: dict[str, Any] | None = None) -> None:
        gates.append({"name": name, "ok": ok, "errors": errors, "evidence": evidence or {}})

    implementation_tree: dict[str, Any] = {}
    component_runtime_report: dict[str, Any] = {}
    resolved_component_runtime_manifest = (
        component_runtime_manifest_path.resolve()
        if component_runtime_manifest_path is not None
        else project / DEFAULT_COMPONENT_RUNTIME_MANIFEST
    )
    resolved_browser_evidence_bundle = (
        browser_evidence_bundle_path.resolve()
        if browser_evidence_bundle_path is not None
        else project / DEFAULT_BROWSER_EVIDENCE_BUNDLE
    )
    resolved_reference_fidelity_contract = (
        reference_fidelity_contract_path.resolve()
        if reference_fidelity_contract_path is not None
        else project / DEFAULT_REFERENCE_FIDELITY_CONTRACT
    )
    resolved_reference_fidelity_report = (
        reference_fidelity_report_path.resolve()
        if reference_fidelity_report_path is not None
        else project / DEFAULT_REFERENCE_FIDELITY_REPORT
    )

    try:
        component_report = load_and_validate_component_contracts(
            project / "build" / "system" / "components" / "component_specs.json",
            tokens_path=project / "design-system" / "tokens.css",
            strict_authored=True,
        )
        add_gate("component_contracts", component_report["ok"], component_report["errors"], component_report)
    except (ValueError, json.JSONDecodeError) as exc:
        add_gate("component_contracts", False, [str(exc)])

    try:
        implementation_tree = _runtime_implementation_tree(target)
        component_runtime_report = validate_component_runtime_conformance(
            project_dir=project,
            target_repo=target,
            implementation_tree=implementation_tree,
            manifest_path=resolved_component_runtime_manifest,
            production_claim=True,
        )
        runtime_errors = list(component_runtime_report["errors"])
        if (
            component_runtime_report["ok"]
            and not component_runtime_report["production_eligible"]
        ):
            runtime_errors.append(
                "component runtime evidence is not eligible for a production claim"
            )
        add_gate(
            "component_runtime_conformance",
            not runtime_errors,
            runtime_errors,
            component_runtime_report,
        )
    except (ValueError, json.JSONDecodeError, OSError) as exc:
        add_gate("component_runtime_conformance", False, [str(exc)])

    try:
        lint_report = lint_implementation(target, artifact_dir=artifact_dir)
        add_gate(
            "implementation_lint",
            lint_report.ok,
            [f"{issue.code} {issue.path}:{issue.line} {issue.message}" for issue in lint_report.issues],
            {"checked_files": lint_report.checked_files, "issue_count": len(lint_report.issues)},
        )
    except (ValueError, OSError) as exc:
        add_gate("implementation_lint", False, [str(exc)])

    screenshot_report = validate_screenshot_manifest(
        screenshot_manifest_path,
        project=project.name,
        target_repo=target,
    )
    add_gate("screenshot_evidence", screenshot_report["ok"], screenshot_report["errors"], screenshot_report)

    browser_evidence_report = validate_browser_evidence_bundle(
        resolved_browser_evidence_bundle,
        project_dir=project,
        target_repo=target,
        implementation_tree=implementation_tree,
        screenshot_manifest_path=screenshot_manifest_path,
        screenshot_report=screenshot_report,
        component_runtime_manifest_path=resolved_component_runtime_manifest,
        component_runtime_report=component_runtime_report,
    )
    add_gate(
        "browser_evidence_bundle",
        browser_evidence_report["ok"],
        browser_evidence_report["errors"],
        browser_evidence_report,
    )

    aesthetic_errors, aesthetic_evidence = _validate_aesthetic_report(
        aesthetic_report_path,
        screenshot_paths=set(screenshot_report.get("resolved_paths") or []),
        screenshot_records=screenshot_report.get("screenshots") or [],
        target_repo=target,
    )
    add_gate("aesthetic_evidence", not aesthetic_errors, aesthetic_errors, aesthetic_evidence)

    # Reference imagery remains advisory unless the visual stage authors an
    # explicit fidelity contract. Once that contract exists, release fails
    # closed until a paired review binds it to the current runtime/screenshots.
    approved_direction_marker = project / "design-system" / "references" / "selected-direction.md"
    if approved_direction_marker.exists() and not resolved_reference_fidelity_contract.exists():
        add_gate(
            "reference_fidelity",
            False,
            [
                "an approved selected direction exists but design-system/reference-fidelity-contract.json is missing"
            ],
            {"approved_direction_marker": str(approved_direction_marker)},
        )
    elif resolved_reference_fidelity_contract.exists():
        fidelity_errors, fidelity_evidence = validate_reference_fidelity_report(
            resolved_reference_fidelity_report,
            contract_path=resolved_reference_fidelity_contract,
            project_dir=project,
            screenshot_sha256={
                str(record.get("sha256") or "")
                for record in screenshot_report.get("screenshots") or []
                if isinstance(record, dict) and record.get("sha256")
            },
            implementation_tree_sha256=str(implementation_tree.get("sha256") or ""),
        )
        add_gate(
            "reference_fidelity",
            not fidelity_errors,
            fidelity_errors,
            fidelity_evidence,
        )

    try:
        divergence = check_style_divergence(target, registry_path=registry_path)
        fingerprint = divergence.get("fingerprint") or {}
        divergence_errors: list[str] = []
        if divergence.get("verdict") != "ok":
            divergence_errors.append("style divergence verdict is not ok")
        if not fingerprint.get("source_files") or fingerprint.get("surface_tone") == "unknown":
            divergence_errors.append("style fingerprint lacks implementation signal")
        add_gate("style_divergence", not divergence_errors, divergence_errors, divergence)
    except (ValueError, json.JSONDecodeError, OSError) as exc:
        add_gate("style_divergence", False, [str(exc)])

    errors = [f"{gate['name']}: {error}" for gate in gates for error in gate["errors"]]
    return {
        "schema_version": "production-ui-verification/v1",
        "project": project.name,
        "target_repo": str(target),
        "ok": not errors,
        "gates": gates,
        "errors": errors,
    }


def _validate_aesthetic_report(
    report_path: Path,
    *,
    screenshot_paths: set[str],
    screenshot_records: list[dict[str, Any]] | None = None,
    target_repo: Path | None = None,
) -> tuple[list[str], dict[str, Any]]:
    errors: list[str] = []
    resolved_target = (target_repo or report_path.parent).resolve()
    try:
        implementation_tree = _runtime_implementation_tree(resolved_target)
    except (OSError, ValueError) as exc:
        errors.append(str(exc))
        implementation_tree = {}
    try:
        report = _load_required_manifest(report_path)
    except (ValueError, json.JSONDecodeError) as exc:
        return [str(exc)], {}
    if not report.get("ready_to_execute") or not report.get("passed"):
        errors.append("aesthetic report execution gate is not open")
    iterations = report.get("iterations") if isinstance(report.get("iterations"), list) else []
    selected_id = report.get("selected_iteration")
    selected = next(
        (
            item
            for item in iterations
            if isinstance(item, dict) and item.get("iteration_id") == selected_id
        ),
        None,
    )
    if not isinstance(selected, dict):
        errors.append("selected aesthetic iteration is missing")
        selected = {}
    if selected.get("coverage_ratio") != 1.0:
        errors.append("selected aesthetic iteration lacks complete metric coverage")
    if selected.get("unsubstantiated_metrics"):
        errors.append("selected aesthetic iteration contains metrics without evidence")
    if selected.get("gate_failures"):
        errors.append("selected aesthetic iteration contains gate failures")

    metric_records: dict[str, dict[str, Any]] = {}
    semantic_without_review: list[str] = []
    dimensions = selected.get("dimension_scores")
    if not isinstance(dimensions, list):
        errors.append("selected aesthetic iteration dimension_scores must be a list")
        dimensions = []
    for dimension in dimensions:
        if not isinstance(dimension, dict):
            errors.append("selected aesthetic iteration contains an invalid dimension score")
            continue
        metrics = dimension.get("metric_scores")
        if not isinstance(metrics, list):
            errors.append("selected aesthetic dimension metric_scores must be a list")
            continue
        for metric in metrics:
            if not isinstance(metric, dict):
                errors.append("selected aesthetic dimension contains an invalid metric score")
                continue
            metric_id = str(metric.get("metric_id") or "")
            if metric_id:
                metric_records[metric_id] = metric
            if not _is_semantic_review_metric(metric_id):
                continue
            sources = set(metric.get("evidence_sources") or [])
            if not sources.intersection({"human", "multimodal-review"}):
                semantic_without_review.append(metric_id)
    if semantic_without_review:
        errors.append(
            "semantic industry-fit metrics require human or multimodal review: "
            + ", ".join(sorted(set(semantic_without_review)))
        )

    source_screenshots = report.get("source_screenshots")
    if not isinstance(source_screenshots, list):
        source_screenshots = []
    aesthetic_paths = {
        str(Path(path).resolve()) for path in source_screenshots if isinstance(path, str) and path
    }
    if not aesthetic_paths:
        errors.append("aesthetic report has no source_screenshots")
    elif aesthetic_paths != screenshot_paths:
        errors.append("aesthetic report screenshots do not match the screenshot evidence manifest")

    records = screenshot_records or []
    expected_hashes = {
        str(record.get("sha256") or "")
        for record in records
        if isinstance(record, dict) and record.get("sha256")
    }
    if len(expected_hashes) != len(screenshot_paths):
        errors.append("aesthetic verification requires screenshot hashes from the validated manifest")
    measurement_protocol = report.get("measurement_protocol")
    if not isinstance(measurement_protocol, dict):
        errors.append("measurement_protocol must be an object")
        measurement_protocol = {}
    production_review = measurement_protocol.get("production_review")
    review_errors, review_evidence = _validate_production_review(
        production_review,
        metric_records=metric_records,
        screenshot_hashes=expected_hashes,
        screenshot_records=records,
        target_repo=resolved_target,
        implementation_tree_sha256=str(implementation_tree.get("sha256") or ""),
        latest_runtime_mtime_ns=int(implementation_tree.get("latest_runtime_mtime_ns") or 0),
    )
    errors.extend(review_errors)
    return errors, {
        "report_path": str(report_path),
        "selected_iteration": selected_id,
        "semantic_review_metric_count": sum(
            1 for metric_id in metric_records if _is_semantic_review_metric(metric_id)
        ),
        "source_screenshots": sorted(aesthetic_paths),
        "production_review": review_evidence,
    }


def _validate_production_review(
    review: Any,
    *,
    metric_records: dict[str, dict[str, Any]],
    screenshot_hashes: set[str],
    screenshot_records: list[dict[str, Any]],
    target_repo: Path,
    implementation_tree_sha256: str,
    latest_runtime_mtime_ns: int,
) -> tuple[list[str], dict[str, Any]]:
    errors: list[str] = []
    if not isinstance(review, dict):
        return ["measurement_protocol.production_review is required"], {}
    if review.get("schema_version") != PRODUCTION_REVIEW_SCHEMA:
        errors.append(f"production_review.schema_version must be {PRODUCTION_REVIEW_SCHEMA}")

    review_runs = review.get("review_runs")
    if not isinstance(review_runs, list) or not review_runs:
        errors.append("production_review.review_runs must be a non-empty list")
        review_runs = []
    valid_metric_sources: dict[str, set[str]] = {}
    covered_hashes: set[str] = set()
    valid_multimodal_runs = 0
    seen_run_ids: set[str] = set()
    for index, run in enumerate(review_runs):
        prefix = f"production_review.review_runs[{index}]"
        if not isinstance(run, dict):
            errors.append(f"{prefix} must be an object")
            continue
        run_id = str(run.get("run_id") or "").strip()
        source = str(run.get("source") or "").strip()
        reviewer = str(run.get("reviewer") or "").strip()
        method = str(run.get("method") or "").strip()
        if not run_id:
            errors.append(f"{prefix}.run_id is required")
        elif run_id in seen_run_ids:
            errors.append(f"{prefix}.run_id must be unique")
        seen_run_ids.add(run_id)
        if source not in {"automated", "human", "multimodal-review"}:
            errors.append(f"{prefix}.source is invalid")
        if len(reviewer) < 3:
            errors.append(f"{prefix}.reviewer must identify the reviewer or tool")
        if len(method) < 16:
            errors.append(f"{prefix}.method must describe the review procedure")
        if not _is_timezone_timestamp(run.get("reviewed_at")):
            errors.append(f"{prefix}.reviewed_at must be an ISO-8601 timestamp with a timezone")
        if source == "multimodal-review" and len(str(run.get("model") or "").strip()) < 3:
            errors.append(f"{prefix}.model is required for multimodal review")

        run_hashes = _string_set(run.get("screenshot_sha256"))
        if not run_hashes:
            errors.append(f"{prefix}.screenshot_sha256 must not be empty")
        unknown_hashes = run_hashes - screenshot_hashes
        if unknown_hashes:
            errors.append(f"{prefix}.screenshot_sha256 contains hashes outside the manifest")
        covered_hashes.update(run_hashes & screenshot_hashes)

        artifact = _load_hashed_json_artifact(
            run.get("artifact"),
            target_repo=target_repo,
            prefix=f"{prefix}.artifact",
            errors=errors,
        )
        if not artifact:
            continue
        if artifact.get("schema_version") != REVIEW_ARTIFACT_SCHEMA:
            errors.append(f"{prefix}.artifact schema_version must be {REVIEW_ARTIFACT_SCHEMA}")
        if artifact.get("run_id") != run_id:
            errors.append(f"{prefix}.artifact run_id does not match")
        if _string_set(artifact.get("screenshot_sha256")) != run_hashes:
            errors.append(f"{prefix}.artifact screenshot hashes do not match the run")
        findings = artifact.get("metric_findings")
        if not isinstance(findings, dict) or not findings:
            errors.append(f"{prefix}.artifact metric_findings must be a non-empty object")
            continue
        notes: set[str] = set()
        for metric_id, finding in findings.items():
            finding_prefix = f"{prefix}.artifact.metric_findings.{metric_id}"
            metric = metric_records.get(str(metric_id))
            if metric is None:
                errors.append(f"{finding_prefix} does not correspond to a selected metric")
                continue
            if not isinstance(finding, dict):
                errors.append(f"{finding_prefix} must be an object")
                continue
            if not _scores_match(finding.get("score"), metric.get("raw_value")):
                errors.append(f"{finding_prefix}.score does not match the selected metric score")
                continue
            note = str(finding.get("note") or "").strip()
            if len(note) < 24:
                errors.append(f"{finding_prefix}.note must record a substantive finding")
                continue
            notes.add(note)
            if source in set(metric.get("evidence_sources") or []):
                valid_metric_sources.setdefault(str(metric_id), set()).add(source)
        if len(findings) >= 3 and len(notes) < 3:
            errors.append(f"{prefix}.artifact must contain distinct metric findings")
        if source == "multimodal-review" and run_hashes == screenshot_hashes:
            valid_multimodal_runs += 1

    if screenshot_hashes and covered_hashes != screenshot_hashes:
        errors.append("production review runs do not cover every screenshot SHA")
    uncovered_metrics = [
        metric_id
        for metric_id, metric in metric_records.items()
        if not (valid_metric_sources.get(metric_id, set()) & set(metric.get("evidence_sources") or []))
    ]
    if uncovered_metrics:
        errors.append(
            "selected metric scores lack hashed review findings: "
            + ", ".join(sorted(uncovered_metrics))
        )
    if not valid_multimodal_runs:
        errors.append("at least one multimodal review run must cover every screenshot SHA")

    runtime_errors, runtime_evidence = _validate_runtime_checks(
        review.get("runtime_checks"),
        screenshot_records=screenshot_records,
        target_repo=target_repo,
        implementation_tree_sha256=implementation_tree_sha256,
        latest_runtime_mtime_ns=latest_runtime_mtime_ns,
    )
    errors.extend(runtime_errors)
    return errors, {
        "schema_version": review.get("schema_version"),
        "review_run_count": len(review_runs),
        "valid_multimodal_run_count": valid_multimodal_runs,
        "covered_screenshot_sha_count": len(covered_hashes),
        "metric_finding_count": len(valid_metric_sources),
        "runtime_checks": runtime_evidence,
    }


def _validate_runtime_checks(
    checks: Any,
    *,
    screenshot_records: list[dict[str, Any]],
    target_repo: Path,
    implementation_tree_sha256: str,
    latest_runtime_mtime_ns: int,
) -> tuple[list[str], dict[str, Any]]:
    errors: list[str] = []
    if not isinstance(checks, list) or not checks:
        return ["production_review.runtime_checks must be a non-empty list"], {}
    expected_route_states = {
        (str(record.get("route") or ""), str(record.get("state") or ""))
        for record in screenshot_records
    }
    expected_viewports = {
        (
            int((record.get("viewport") or {}).get("width") or 0),
            int((record.get("viewport") or {}).get("height") or 0),
        )
        for record in screenshot_records
    }
    found: set[str] = set()
    evidence: dict[str, Any] = {}
    for index, check in enumerate(checks):
        prefix = f"production_review.runtime_checks[{index}]"
        if not isinstance(check, dict):
            errors.append(f"{prefix} must be an object")
            continue
        kind = str(check.get("kind") or "")
        run_id = str(check.get("run_id") or "").strip()
        method = str(check.get("method") or "").strip()
        if kind not in REQUIRED_RUNTIME_CHECKS:
            errors.append(f"{prefix}.kind must be interaction, overflow, or accessibility")
            continue
        if kind in found:
            errors.append(f"{prefix}.kind duplicates {kind}")
        found.add(kind)
        if not run_id:
            errors.append(f"{prefix}.run_id is required")
        if check.get("status") != "passed":
            errors.append(f"{prefix}.status must be passed")
        if len(method) < 16:
            errors.append(f"{prefix}.method must describe the verification procedure")
        artifact = _load_hashed_json_artifact(
            check.get("artifact"),
            target_repo=target_repo,
            prefix=f"{prefix}.artifact",
            errors=errors,
        )
        if not artifact:
            continue
        if artifact.get("schema_version") != RUNTIME_CHECK_ARTIFACT_SCHEMA:
            errors.append(
                f"{prefix}.artifact schema_version must be {RUNTIME_CHECK_ARTIFACT_SCHEMA}"
            )
        if artifact.get("kind") != kind:
            errors.append(f"{prefix}.artifact kind does not match")
        if artifact.get("run_id") != run_id:
            errors.append(f"{prefix}.artifact run_id does not match")
        if artifact.get("implementation_tree_sha256") != implementation_tree_sha256:
            errors.append(
                f"{prefix}.artifact implementation_tree_sha256 does not match the runtime implementation"
            )
        checked_at = artifact.get("checked_at")
        if not _is_timezone_timestamp(checked_at):
            errors.append(f"{prefix}.artifact checked_at must be an ISO-8601 timestamp with a timezone")
        else:
            checked_ns = int(
                datetime.fromisoformat(str(checked_at).replace("Z", "+00:00")).timestamp()
                * 1_000_000_000
            )
            if checked_ns < latest_runtime_mtime_ns:
                errors.append(f"{prefix}.artifact checked_at is older than the runtime implementation")
        artifact_mtime_ns = int(artifact.get("_artifact_mtime_ns") or 0)
        if artifact_mtime_ns < latest_runtime_mtime_ns:
            errors.append(f"{prefix}.artifact file is older than the runtime implementation")
        assertions = artifact.get("assertions")
        if not _all_assertions_pass(assertions):
            errors.append(f"{prefix}.artifact assertions must be non-empty and all pass")

        if kind == "interaction":
            raw_coverage = artifact.get("route_state_coverage")
            if not isinstance(raw_coverage, list):
                raw_coverage = []
            coverage = {
                (str(item.get("route") or ""), str(item.get("state") or ""))
                for item in raw_coverage
                if isinstance(item, dict)
            }
            if coverage != expected_route_states:
                errors.append(f"{prefix}.artifact route/state coverage does not match the screenshots")
        elif kind == "overflow":
            raw_coverage = artifact.get("viewport_coverage")
            if not isinstance(raw_coverage, list):
                raw_coverage = []
            coverage = {
                (int(item.get("width") or 0), int(item.get("height") or 0))
                for item in raw_coverage
                if isinstance(item, dict)
                and isinstance(item.get("width"), int)
                and not isinstance(item.get("width"), bool)
                and isinstance(item.get("height"), int)
                and not isinstance(item.get("height"), bool)
            }
            if coverage != expected_viewports:
                errors.append(f"{prefix}.artifact viewport coverage does not match the screenshots")
            overflow = artifact.get("max_horizontal_overflow_px")
            if not isinstance(overflow, int | float) or isinstance(overflow, bool) or overflow > 0:
                errors.append(f"{prefix}.artifact max_horizontal_overflow_px must be zero")
        elif kind == "accessibility":
            if "wcag" not in str(artifact.get("standard") or "").lower():
                errors.append(f"{prefix}.artifact standard must declare a WCAG target")
            violations = artifact.get("automated_violations")
            if not isinstance(violations, int) or isinstance(violations, bool) or violations != 0:
                errors.append(f"{prefix}.artifact automated_violations must be zero")
            if not _all_assertions_pass(artifact.get("keyboard_assertions")):
                errors.append(f"{prefix}.artifact keyboard_assertions must be non-empty and all pass")
        evidence[kind] = {
            "run_id": run_id,
            "assertion_count": len(assertions) if isinstance(assertions, list) else 0,
        }
    missing = REQUIRED_RUNTIME_CHECKS - found
    if missing:
        errors.append("production review is missing runtime checks: " + ", ".join(sorted(missing)))
    return errors, evidence


def _is_semantic_review_metric(metric_id: str) -> bool:
    return metric_id in SEMANTIC_REVIEW_METRICS or metric_id.startswith(SEMANTIC_REVIEW_PREFIXES)


def _visual_signal(path: Path) -> dict[str, float]:
    features = analyze_screenshot(path)
    return {
        "luminance_std": features.luminance_std,
        "luminance_span": features.luminance_span,
        "edge_density": features.edge_density,
        "active_cell_share": features.active_cell_share,
    }


def _visual_signal_errors(signal: dict[str, float]) -> list[str]:
    errors: list[str] = []
    if signal["luminance_std"] < MIN_LUMINANCE_STD:
        errors.append(
            f"luminance_std {signal['luminance_std']:.4f} is below {MIN_LUMINANCE_STD:.4f}"
        )
    if signal["luminance_span"] < MIN_LUMINANCE_SPAN:
        errors.append(
            f"luminance_span {signal['luminance_span']:.4f} is below {MIN_LUMINANCE_SPAN:.4f}"
        )
    if (
        signal["edge_density"] < MIN_EDGE_DENSITY
        and signal["active_cell_share"] < MIN_ACTIVE_CELL_SHARE
    ):
        errors.append(
            "both edge density and active-cell coverage are below the production screenshot floor"
        )
    return errors


def _load_hashed_json_artifact(
    record: Any,
    *,
    target_repo: Path,
    prefix: str,
    errors: list[str],
) -> dict[str, Any] | None:
    if not isinstance(record, dict):
        errors.append(f"{prefix} must contain path and sha256")
        return None
    raw_path = str(record.get("path") or "").strip()
    declared_sha = str(record.get("sha256") or "").strip()
    if not raw_path or not declared_sha:
        errors.append(f"{prefix} must contain path and sha256")
        return None
    path = Path(raw_path)
    resolved = path.resolve() if path.is_absolute() else (target_repo / path).resolve()
    try:
        resolved.relative_to(target_repo.resolve())
    except ValueError:
        errors.append(f"{prefix}.path must stay inside the target repository")
        return None
    if not resolved.is_file():
        errors.append(f"{prefix}.path does not exist: {raw_path}")
        return None
    if _sha256(resolved) != declared_sha:
        errors.append(f"{prefix}.sha256 does not match the artifact")
        return None
    try:
        payload = json.loads(resolved.read_text(encoding="utf-8"))
    except (OSError, UnicodeDecodeError, json.JSONDecodeError):
        errors.append(f"{prefix}.path must be a readable JSON artifact")
        return None
    if not isinstance(payload, dict):
        errors.append(f"{prefix}.path JSON root must be an object")
        return None
    payload = dict(payload)
    payload["_artifact_path"] = str(resolved)
    payload["_artifact_mtime_ns"] = resolved.stat().st_mtime_ns
    return payload


def _all_assertions_pass(assertions: Any) -> bool:
    return (
        isinstance(assertions, list)
        and bool(assertions)
        and all(isinstance(item, dict) and item.get("passed") is True for item in assertions)
    )


def _scores_match(left: Any, right: Any) -> bool:
    if isinstance(left, bool) or isinstance(right, bool):
        return False
    if not isinstance(left, int | float) or not isinstance(right, int | float):
        return False
    return abs(float(left) - float(right)) <= 0.0001


def _string_set(value: Any) -> set[str]:
    if not isinstance(value, list):
        return set()
    return {item.strip() for item in value if isinstance(item, str) and item.strip()}


def _is_timezone_timestamp(value: Any) -> bool:
    if not isinstance(value, str) or not value.strip():
        return False
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        return False
    return parsed.tzinfo is not None


def _verify_git_sha(target_repo: Path, declared_sha: str, errors: list[str]) -> str | None:
    if not declared_sha:
        return None
    try:
        head_result = subprocess.run(
            ["git", "-C", str(target_repo), "rev-parse", "HEAD"],
            text=True,
            capture_output=True,
            check=False,
        )
    except OSError:
        errors.append("git is unavailable; implementation_sha cannot be verified")
        return None
    if head_result.returncode != 0:
        errors.append("target repository has no Git HEAD; implementation_sha cannot be verified")
        return None
    declared_result = subprocess.run(
        ["git", "-C", str(target_repo), "rev-parse", "--verify", f"{declared_sha}^{{commit}}"],
        text=True,
        capture_output=True,
        check=False,
    )
    if declared_result.returncode != 0:
        errors.append("implementation_sha is not a verifiable Git commit")
        return None
    actual = head_result.stdout.strip()
    resolved_declared = declared_result.stdout.strip()
    if actual != resolved_declared:
        errors.append("implementation_sha does not match the current git HEAD")
    return resolved_declared


def _load_optional_manifest(path: Path) -> dict[str, Any] | None:
    if not path.exists():
        return None
    return _load_required_manifest(path)


def _load_required_manifest(path: Path) -> dict[str, Any]:
    if not path.is_file():
        raise ValueError(f"required JSON evidence not found: {path}")
    payload = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ValueError(f"JSON evidence must be an object: {path}")
    return payload


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()
