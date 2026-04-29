#!/usr/bin/env python3
"""Phase 13-12-3: community preset PR validator.

Runs the existing preset_validator + preview_linter, then layers three
community-specific checks:

1. HEX overlap — if >= 2 of (primary, accent, surface_tint) match any
   existing preset's Core HEX set, emit a WARNING.
2. Cell duplicate — if the {app_mode, brand_tone} cell is already taken at
   P0/P1/P2, emit a WARNING. (P3 is allowed to duplicate, but we surface it.)
3. Self-match — run the matcher with the preset's own (app_mode, brand_tone,
   tags) and require Top-1 to be the preset itself. Else ERROR.

Exit codes:
    0 — pass (no errors; warnings allowed)
    1 — error (one of the critical checks failed)
    2 — usage error

Stdlib only. Reuses design_ontology_harness.preset_validator /
preview_linter / preset_matcher.engine so behavior stays in sync with the
rest of the harness.

Usage:
    python3 scripts/validate-community-preset.py --preset-id <id>
    python3 scripts/validate-community-preset.py --diff-mode  # CI: detect
                                                               # new preset
                                                               # from git diff
"""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Iterable

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT))

from design_ontology_harness.preset_matcher.engine import (  # noqa: E402
    MatchQuery,
    match_presets,
)
from design_ontology_harness.preset_validator import (  # noqa: E402
    validate_all,
)
from design_ontology_harness.preview_linter import lint_preview  # noqa: E402


CORE_HEX_PATTERN = re.compile(
    r"^\s*-\s*(primary|accent|surface_tint)\s*:\s*`(#[0-9a-fA-F]{3,8})`",
    re.IGNORECASE | re.MULTILINE,
)


@dataclass
class CheckReport:
    preset_id: str
    errors: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
    notes: list[str] = field(default_factory=list)

    @property
    def ok(self) -> bool:
        return not self.errors


def _find_presets_root(presets_dir: Path | None) -> Path:
    return presets_dir or (REPO_ROOT / "presets")


def _extract_core_hex(preview_path: Path) -> dict[str, str]:
    """Return {role: hex} for primary/accent/surface_tint parsed from the
    '### Core' block of preview.md. Missing roles are simply absent from
    the dict."""

    if not preview_path.exists():
        return {}
    text = preview_path.read_text(encoding="utf-8")
    # Narrow to the '### Core' subsection if present, so Semantic HEXes
    # don't pollute the match.
    core_start = text.find("### Core")
    if core_start >= 0:
        next_section = text.find("\n### ", core_start + 1)
        scope = text[core_start: next_section if next_section > 0 else len(text)]
    else:
        scope = text
    hits: dict[str, str] = {}
    for match in CORE_HEX_PATTERN.finditer(scope):
        role = match.group(1).lower()
        hex_value = match.group(2).lower()
        hits.setdefault(role, hex_value)
    return hits


def _collect_existing_core_hexes(
    presets_root: Path, exclude_id: str
) -> dict[str, set[str]]:
    """Map preset_id -> set of its core HEX values (lowercase)."""

    result: dict[str, set[str]] = {}
    for preset_dir in sorted(presets_root.iterdir()):
        if not preset_dir.is_dir() or preset_dir.name == exclude_id:
            continue
        preview_path = preset_dir / "preview.md"
        if not preview_path.exists():
            continue
        core = _extract_core_hex(preview_path)
        if core:
            result[preset_dir.name] = {v.lower() for v in core.values()}
    return result


def _load_manifest(preset_dir: Path) -> dict:
    path = preset_dir / "manifest.json"
    if not path.exists():
        return {}
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return {}


def _load_matrix(presets_root: Path) -> dict:
    path = presets_root / "matrix.json"
    if not path.exists():
        return {}
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return {}


def check_structure_and_preview(
    report: CheckReport, preset_dir: Path, presets_root: Path
) -> None:
    """Delegate to preset_validator + preview_linter."""

    val_report = validate_all(presets_root)
    preset_id = report.preset_id
    tagged_errors = [e for e in val_report.errors if f"[{preset_id}]" in e]
    tagged_warnings = [w for w in val_report.warnings if f"[{preset_id}]" in w]
    for err in tagged_errors:
        report.errors.append(f"validate-presets: {err}")
    for warn in tagged_warnings:
        report.warnings.append(f"validate-presets: {warn}")

    lint_report = lint_preview(preset_dir)
    for err in lint_report.errors:
        report.errors.append(f"preview-lint: {err.code} {err.message}")
    for warn in lint_report.warnings:
        report.warnings.append(f"preview-lint: {warn.code} {warn.message}")


def check_hex_overlap(
    report: CheckReport, preset_dir: Path, presets_root: Path
) -> None:
    """Warn if >=2 of (primary, accent, surface_tint) collide with any
    existing preset's Core HEX set."""

    own_core = _extract_core_hex(preset_dir / "preview.md")
    if len(own_core) < 3:
        report.notes.append(
            f"HEX check skipped — Core block missing roles "
            f"(found: {sorted(own_core.keys())})."
        )
        return
    existing = _collect_existing_core_hexes(presets_root, preset_dir.name)
    own_values = {v.lower() for v in own_core.values()}
    for other_id, other_values in existing.items():
        overlap = own_values & other_values
        if len(overlap) >= 2:
            report.warnings.append(
                f"HEX overlap: {len(overlap)} core HEX(es) overlap with "
                f"{other_id} → {sorted(overlap)}. Consider differentiating "
                f"primary/accent/surface_tint."
            )
    report.notes.append(
        f"Core HEX: {', '.join(f'{k}={v}' for k, v in sorted(own_core.items()))}"
    )


def check_cell_duplicate(
    report: CheckReport, manifest: dict, matrix: dict, preset_id: str
) -> None:
    """Warn if the same {app_mode, brand_tone} cell is already occupied by
    a P0/P1/P2 preset."""

    app_mode = manifest.get("app_mode")
    brand_tone = manifest.get("brand_tone")
    if not (app_mode and brand_tone):
        report.notes.append("cell check skipped — manifest incomplete.")
        return
    existing_cell: list[tuple[str, str]] = []
    for entry in matrix.get("presets", []):
        if entry.get("id") == preset_id:
            continue
        if entry.get("app_mode") == app_mode and entry.get("brand_tone") == brand_tone:
            tier = entry.get("tier", "P?")
            existing_cell.append((entry["id"], tier))
    if not existing_cell:
        return
    p0p1p2 = [
        (pid, tier) for pid, tier in existing_cell if tier in {"P0", "P1", "P2"}
    ]
    if p0p1p2:
        listing = ", ".join(f"{pid} ({tier})" for pid, tier in p0p1p2)
        report.warnings.append(
            f"Cell duplicate: {{{app_mode}, {brand_tone}}} already covered by "
            f"{listing}. P3 can duplicate, but differentiate via tags."
        )
    else:
        # Only other P3s exist — note but don't warn.
        listing = ", ".join(f"{pid} ({tier})" for pid, tier in existing_cell)
        report.notes.append(
            f"Other P3 in same cell: {listing}."
        )


def check_self_match(
    report: CheckReport, manifest: dict, preset_id: str
) -> None:
    """Top-1 of a direct explicit-field query must be the preset itself."""

    app_mode = manifest.get("app_mode")
    brand_tone = manifest.get("brand_tone")
    tags = list(manifest.get("tags") or [])
    if not (app_mode and brand_tone):
        report.errors.append("self-match skipped — manifest incomplete.")
        return
    query = MatchQuery(app_mode=app_mode, brand_tone=brand_tone, tags=tags)
    results = match_presets(query, top_k=3, include_deprecated=True)
    if not results:
        report.errors.append("self-match: matcher returned no results.")
        return
    top = results[0]
    if top.preset_id != preset_id:
        report.errors.append(
            f"self-match: Top-1 is {top.preset_id} (score={top.raw_score:.3f}, "
            f"bucket={top.bucket}); expected {preset_id}. "
            f"Check tags / matrix.json entry."
        )
    else:
        report.notes.append(
            f"self-match Top-1 = {preset_id} "
            f"(score={top.raw_score:.3f}, bucket={top.bucket})"
        )


def run_checks(preset_id: str, presets_root: Path) -> CheckReport:
    report = CheckReport(preset_id=preset_id)
    preset_dir = presets_root / preset_id
    if not preset_dir.is_dir():
        report.errors.append(f"preset directory not found: {preset_dir}")
        return report

    manifest = _load_manifest(preset_dir)
    matrix = _load_matrix(presets_root)

    check_structure_and_preview(report, preset_dir, presets_root)
    check_hex_overlap(report, preset_dir, presets_root)
    check_cell_duplicate(report, manifest, matrix, preset_id)
    check_self_match(report, manifest, preset_id)
    return report


def detect_new_presets_from_diff() -> list[str]:
    """Parse `git diff --name-status origin/main...HEAD` for new preset
    directories. Returns list of preset ids."""

    try:
        proc = subprocess.run(
            ["git", "diff", "--name-status", "origin/main...HEAD"],
            cwd=REPO_ROOT,
            capture_output=True,
            text=True,
            check=False,
        )
    except FileNotFoundError:
        return []
    if proc.returncode != 0:
        # Fallback: list untracked presets/ dirs if git diff is unavailable.
        return []
    new_ids: set[str] = set()
    for line in proc.stdout.splitlines():
        parts = line.split("\t")
        if len(parts) < 2 or parts[0] not in {"A", "M"}:
            continue
        path = parts[-1]
        match = re.match(r"presets/([^/]+)/manifest\.json$", path)
        if match:
            new_ids.add(match.group(1))
    return sorted(new_ids)


def format_report(report: CheckReport) -> str:
    lines = [f"[validate-community-preset] {report.preset_id}"]
    if report.errors:
        lines.append(f"  ERRORS ({len(report.errors)}):")
        for err in report.errors:
            lines.append(f"    ✗ {err}")
    if report.warnings:
        lines.append(f"  WARNINGS ({len(report.warnings)}):")
        for warn in report.warnings:
            lines.append(f"    ⚠ {warn}")
    if report.notes:
        lines.append(f"  NOTES ({len(report.notes)}):")
        for note in report.notes:
            lines.append(f"    · {note}")
    if report.ok and not report.warnings:
        lines.append("  ✓ all checks passed")
    elif report.ok:
        lines.append("  ✓ no errors (warnings above — review before merge)")
    return "\n".join(lines)


def main(argv: Iterable[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--preset-id",
        default=None,
        help="Explicit preset id to check. Mutually exclusive with --diff-mode.",
    )
    parser.add_argument(
        "--diff-mode",
        action="store_true",
        help="Detect new preset(s) from git diff vs origin/main (CI usage).",
    )
    parser.add_argument(
        "--presets-dir",
        default=None,
        help="Override presets/ root (default: harness repo presets/).",
    )
    args = parser.parse_args(list(argv) if argv is not None else None)

    if bool(args.preset_id) == bool(args.diff_mode):
        print(
            "usage: pass exactly one of --preset-id or --diff-mode",
            file=sys.stderr,
        )
        return 2

    presets_root = _find_presets_root(
        Path(args.presets_dir) if args.presets_dir else None
    )

    if args.preset_id:
        targets = [args.preset_id]
    else:
        targets = detect_new_presets_from_diff()
        if not targets:
            print("[validate-community-preset] no new preset manifests detected")
            return 0

    overall_ok = True
    for preset_id in targets:
        report = run_checks(preset_id, presets_root)
        print(format_report(report))
        if not report.ok:
            overall_ok = False
    return 0 if overall_ok else 1


if __name__ == "__main__":
    sys.exit(main())
