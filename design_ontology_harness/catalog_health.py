"""Catalog health report — Phase 15-1.

Aggregates preset-level + catalog-level signals into a JSON-serializable
report, then renders a Markdown summary suitable for `presets/CATALOG_HEALTH.md`.

Inputs:
- `presets/matrix.json` (axis definitions + preset index)
- `presets/<preset-id>/manifest.json` (per-preset 4-version contract)
- `presets/.metrics/install_hits.json` (manual scoreboard, may be missing)
- `presets/.metrics/match_hits.json` (manual scoreboard, may be missing)
- `tests/fixtures/preset_snapshots.json` (Phase 15-5 snapshot baseline)
- harness `pyproject.toml` (dynamic version detection)

Outputs:
- `compute_health(...)` → dict (full report, json-safe)
- `format_markdown(report)` → str (CATALOG_HEALTH.md content)
- `format_summary(report)` → str (~10-line stdout brief)

Stdlib only. Reuses preview_linter for preview_lint_status.
"""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterable

from .preset_builder import APP_MODES, BRAND_TONES, MATRIX_PATH, PRESETS_ROOT
from .preview_linter import lint_preview

REPO_ROOT = Path(__file__).resolve().parent.parent
METRICS_DIR_NAME = ".metrics"
INSTALL_HITS_FILE = "install_hits.json"
MATCH_HITS_FILE = "match_hits.json"
SNAPSHOT_FIXTURE = REPO_ROOT / "tests" / "fixtures" / "preset_snapshots.json"

# PLAN §11.4 — after the first quarter in `deprecated` state, presets are
# pruned from the catalog. Keep this threshold in sync with
# preset_ops.DEFAULT_MIN_DEPRECATED_AGE_DAYS.
PRUNE_MIN_DEPRECATED_AGE_DAYS = 90

# PLAN §4.8 + CONTRIBUTING §4.2 priority order (top-10 expected demand cells).
PRIORITY_EMPTY_CELLS: tuple[tuple[str, str], ...] = (
    ("dashboard", "bold-confident"),
    ("dashboard", "playful-soft"),
    ("commerce", "minimal-tech"),
    ("commerce", "playful-soft"),
    ("marketing-landing", "editorial-warm"),
    ("marketing-landing", "playful-soft"),
    ("conversation-copilot", "corporate-trust"),
    ("document-content", "corporate-trust"),
    ("monitoring-ops", "corporate-trust"),
    ("canvas-tool", "bold-confident"),
)


def _detect_harness_version(pyproject_path: Path | None = None) -> str:
    path = pyproject_path or (REPO_ROOT / "pyproject.toml")
    if not path.exists():
        return "0.0.0"
    for line in path.read_text(encoding="utf-8").splitlines():
        stripped = line.strip()
        if stripped.startswith("version"):
            parts = stripped.split("=", 1)
            if len(parts) == 2:
                return parts[1].strip().strip('"').strip("'")
    return "0.0.0"


def _parse_version(value: str | None) -> tuple[int, int, int] | None:
    if not value:
        return None
    parts = value.strip().split(".")
    if len(parts) != 3:
        return None
    try:
        return int(parts[0]), int(parts[1]), int(parts[2])
    except ValueError:
        return None


def _minor_drift(preset_version: str | None, current_version: str) -> int:
    """Return how many minor versions behind a preset is.

    - Same major + same/newer preset minor → 0
    - Same major, older preset minor → (current_minor - preset_minor)
    - Major newer than preset → ((Δmajor) * 10) + current_minor (large)
    - Preset major newer than current → 0 (treat as future, no drift)
    - Unparseable → 99 sentinel
    """

    p = _parse_version(preset_version)
    c = _parse_version(current_version)
    if p is None or c is None:
        return 99
    p_major, p_minor, _ = p
    c_major, c_minor, _ = c
    if c_major < p_major:
        return 0
    if c_major > p_major:
        return (c_major - p_major) * 10 + c_minor
    return max(0, c_minor - p_minor)


def _load_json(path: Path) -> dict:
    if not path.exists():
        return {}
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
        return data if isinstance(data, dict) else {}
    except json.JSONDecodeError:
        return {}


def _load_metrics(metrics_dir: Path) -> tuple[dict, dict]:
    install = _load_json(metrics_dir / INSTALL_HITS_FILE)
    match = _load_json(metrics_dir / MATCH_HITS_FILE)
    return install, match


def _preview_lint_status(preset_dir: Path) -> str:
    report = lint_preview(preset_dir)
    if report.errors:
        return "ERROR"
    if report.warnings:
        return "WARN"
    return "OK"


def _is_deprecation_candidate(
    *,
    install_hits: int,
    match_hits: int,
    version_drift_minor: int,
    preview_lint_status: str,
) -> tuple[bool, list[str]]:
    """PLAN §11.2 / CONTRIBUTING §8 deprecation triggers."""

    reasons: list[str] = []
    if install_hits == 0 and match_hits == 0:
        reasons.append("zero_hits")
    if version_drift_minor >= 2:
        reasons.append(f"version_drift_minor={version_drift_minor}")
    if preview_lint_status == "ERROR":
        reasons.append("preview_lint_error")
    return (bool(reasons), reasons)


def _parse_deprecated_iso(value: str) -> datetime | None:
    if not value:
        return None
    stripped = value.rstrip("Z")
    try:
        dt = datetime.fromisoformat(stripped)
    except ValueError:
        return None
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    return dt


def _build_preset_entry(
    *,
    preset_id: str,
    preset_dir: Path,
    install_hits: dict,
    match_hits: dict,
    snapshot_fixture: dict,
    current_harness_version: str,
    now: datetime,
    min_deprecated_age_days: int,
) -> dict:
    manifest_path = preset_dir / "manifest.json"
    manifest = _load_json(manifest_path)

    generated_by = manifest.get("generated_by_harness_version")
    drift = _minor_drift(generated_by, current_harness_version)
    lint_status = _preview_lint_status(preset_dir) if preset_dir.is_dir() else "ERROR"
    install_count = int(install_hits.get(preset_id, 0) or 0)
    match_count = int(match_hits.get(preset_id, 0) or 0)
    content_hash = manifest.get("content_hash") or ""
    snapshot_hash = snapshot_fixture.get(preset_id) or ""
    snapshot_drift = bool(snapshot_hash) and snapshot_hash != content_hash

    deprecated_at = manifest.get("deprecated_at") or ""
    deprecation_reason = manifest.get("deprecation_reason") or ""
    deprecated_replacement = manifest.get("deprecated_replacement") or ""
    is_deprecated = bool(deprecated_at)

    # Active-catalog candidate flag applies only to presets that are NOT yet
    # deprecated; once marked, the entry moves to the separate Deprecated
    # section (no further "candidate" surfacing needed).
    if is_deprecated:
        is_deprecation_candidate = False
        reasons: list[str] = []
    else:
        is_deprecation_candidate, reasons = _is_deprecation_candidate(
            install_hits=install_count,
            match_hits=match_count,
            version_drift_minor=drift,
            preview_lint_status=lint_status,
        )

    deprecated_age_days: int | None = None
    prune_eligible = False
    prune_blocked_reasons: list[str] = []
    if is_deprecated:
        parsed = _parse_deprecated_iso(deprecated_at)
        if parsed is not None:
            deprecated_age_days = (now - parsed).days
            if deprecated_age_days < min_deprecated_age_days:
                prune_blocked_reasons.append(
                    f"age={deprecated_age_days}d<{min_deprecated_age_days}d"
                )
            if install_count > 0 or match_count > 0:
                prune_blocked_reasons.append(
                    f"hits={install_count + match_count}>0"
                )
            if not prune_blocked_reasons:
                prune_eligible = True
        else:
            prune_blocked_reasons.append("invalid deprecated_at")

    return {
        "preset_id": preset_id,
        "tier": manifest.get("tier", "P?"),
        "app_mode": manifest.get("app_mode", ""),
        "brand_tone": manifest.get("brand_tone", ""),
        "tags": list(manifest.get("tags") or []),
        "owner": manifest.get("owner", ""),
        "generated_by_harness_version": generated_by or "",
        "version_drift_minor": drift,
        "content_hash": content_hash,
        "last_rebuilt_at": manifest.get("generated_at", ""),
        "preview_lint_status": lint_status,
        "install_hits": install_count,
        "match_hits": match_count,
        "snapshot_drift": snapshot_drift,
        "is_deprecation_candidate": is_deprecation_candidate,
        "deprecation_reasons": reasons,
        "deprecated_at": deprecated_at,
        "deprecation_reason": deprecation_reason,
        "deprecated_replacement": deprecated_replacement,
        "is_deprecated": is_deprecated,
        "deprecated_age_days": deprecated_age_days,
        "prune_eligible": prune_eligible,
        "prune_blocked_reasons": prune_blocked_reasons,
    }


def _empty_cells(presets: list[dict]) -> list[dict]:
    occupied = {(p["app_mode"], p["brand_tone"]) for p in presets if p.get("app_mode")}
    cells: list[dict] = []
    for app_mode in sorted(APP_MODES):
        for brand_tone in sorted(BRAND_TONES):
            if (app_mode, brand_tone) in occupied:
                continue
            try:
                priority = PRIORITY_EMPTY_CELLS.index((app_mode, brand_tone)) + 1
            except ValueError:
                priority = 0
            cells.append(
                {
                    "app_mode": app_mode,
                    "brand_tone": brand_tone,
                    "priority": priority,
                }
            )
    cells.sort(key=lambda c: (0 if c["priority"] else 1, c["priority"] or 99, c["app_mode"], c["brand_tone"]))
    return cells


def compute_health(
    *,
    presets_root: Path | None = None,
    metrics_dir: Path | None = None,
    snapshot_fixture_path: Path | None = None,
    pyproject_path: Path | None = None,
    min_deprecated_age_days: int = PRUNE_MIN_DEPRECATED_AGE_DAYS,
    now: datetime | None = None,
) -> dict:
    """Walk matrix.json + per-preset manifests + .metrics + snapshot fixture
    and produce a JSON-safe report dict."""

    root = presets_root or PRESETS_ROOT
    matrix_path = root / "matrix.json" if root != PRESETS_ROOT else MATRIX_PATH
    matrix = _load_json(matrix_path)
    matrix_presets = list(matrix.get("presets") or [])

    metrics_root = metrics_dir if metrics_dir is not None else (root / METRICS_DIR_NAME)
    install_hits, match_hits = _load_metrics(metrics_root)
    snapshot_fixture = _load_json(snapshot_fixture_path or SNAPSHOT_FIXTURE)
    harness_version = _detect_harness_version(pyproject_path)
    current_now = now or datetime.now(timezone.utc)

    preset_entries: list[dict] = []
    for entry in matrix_presets:
        preset_id = entry.get("id")
        if not preset_id:
            continue
        preset_dir = root / preset_id
        preset_entries.append(
            _build_preset_entry(
                preset_id=preset_id,
                preset_dir=preset_dir,
                install_hits=install_hits,
                match_hits=match_hits,
                snapshot_fixture=snapshot_fixture,
                current_harness_version=harness_version,
                now=current_now,
                min_deprecated_age_days=min_deprecated_age_days,
            )
        )
    preset_entries.sort(key=lambda p: p["preset_id"])

    tier_counts: dict[str, int] = {tier: 0 for tier in ("P0", "P1", "P2", "P3")}
    for p in preset_entries:
        tier_counts[p["tier"]] = tier_counts.get(p["tier"], 0) + 1

    empty_cells = _empty_cells(preset_entries)
    total_cells = len(APP_MODES) * len(BRAND_TONES)
    occupied_cells = total_cells - len(empty_cells)

    deprecation_candidates = [p for p in preset_entries if p["is_deprecation_candidate"]]
    deprecated_presets = [p for p in preset_entries if p.get("is_deprecated")]
    prune_eligible_presets = [p for p in preset_entries if p.get("prune_eligible")]
    snapshot_drift_count = sum(1 for p in preset_entries if p["snapshot_drift"])

    return {
        "generated_at": current_now.strftime("%Y-%m-%dT%H:%M:%SZ"),
        "harness_version": harness_version,
        "preset_total": len(preset_entries),
        "tier_counts": tier_counts,
        "cell_coverage": {
            "occupied": occupied_cells,
            "total": total_cells,
            "ratio": round(occupied_cells / total_cells, 3) if total_cells else 0.0,
        },
        "empty_cells": empty_cells,
        "priority_empty_cells_top10": [
            {"app_mode": m, "brand_tone": t, "priority": idx + 1}
            for idx, (m, t) in enumerate(PRIORITY_EMPTY_CELLS)
            if (m, t) not in {(p["app_mode"], p["brand_tone"]) for p in preset_entries}
        ],
        "deprecation_candidates": deprecation_candidates,
        "deprecated_count": len(deprecated_presets),
        "deprecated_presets": deprecated_presets,
        "prune_eligible_count": len(prune_eligible_presets),
        "prune_eligible_presets": prune_eligible_presets,
        "prune_min_deprecated_age_days": min_deprecated_age_days,
        "snapshot_drift_count": snapshot_drift_count,
        "metrics_sources": {
            "install_hits_file": str((metrics_root / INSTALL_HITS_FILE).resolve()),
            "match_hits_file": str((metrics_root / MATCH_HITS_FILE).resolve()),
            "snapshot_fixture": str((snapshot_fixture_path or SNAPSHOT_FIXTURE).resolve()),
        },
        "presets": preset_entries,
    }


def _render_table(rows: Iterable[Iterable[str]], header: list[str]) -> list[str]:
    rows_list = [list(r) for r in rows]
    lines = [
        "| " + " | ".join(header) + " |",
        "|" + "|".join(["---"] * len(header)) + "|",
    ]
    for row in rows_list:
        lines.append("| " + " | ".join(row) + " |")
    return lines


def format_markdown(report: dict) -> str:
    lines: list[str] = []
    lines.append("# Catalog Health Report")
    lines.append("")
    lines.append(f"> Generated at `{report['generated_at']}` · harness `{report['harness_version']}`")
    lines.append("")
    lines.append("## Overview")
    lines.append("")
    lines.append(f"- 누적 프리셋: **{report['preset_total']}**")
    counts = report["tier_counts"]
    tier_summary = " · ".join(f"{tier} {counts.get(tier, 0)}" for tier in ("P0", "P1", "P2", "P3"))
    lines.append(f"- Tier 분포: {tier_summary}")
    cov = report["cell_coverage"]
    lines.append(f"- 셀 커버리지: {cov['occupied']}/{cov['total']} (= {cov['ratio']:.0%})")
    lines.append(f"- Snapshot drift: {report['snapshot_drift_count']}건")
    lines.append(f"- Deprecation 후보: {len(report['deprecation_candidates'])}건")
    lines.append(f"- Deprecated 프리셋: {report.get('deprecated_count', 0)}건")
    lines.append(
        f"- Prune eligible: {report.get('prune_eligible_count', 0)}건 "
        f"(deprecated ≥ {report.get('prune_min_deprecated_age_days', 90)}일 + hits 0)"
    )
    lines.append("")

    lines.append("## Priority Empty Cells (Top-10)")
    lines.append("")
    if report["priority_empty_cells_top10"]:
        rows = [
            [str(item["priority"]), f"`{item['app_mode']}--{item['brand_tone']}`"]
            for item in report["priority_empty_cells_top10"]
        ]
        lines.extend(_render_table(rows, ["Priority", "Cell"]))
    else:
        lines.append("- ✅ Top-10 셀 모두 채움")
    lines.append("")

    lines.append("## Empty Cells (full list)")
    lines.append("")
    if report["empty_cells"]:
        rows = [
            [
                f"`{cell['app_mode']}--{cell['brand_tone']}`",
                str(cell["priority"]) if cell["priority"] else "—",
            ]
            for cell in report["empty_cells"]
        ]
        lines.extend(_render_table(rows, ["Cell", "Priority"]))
    else:
        lines.append("- ✅ 매트릭스 전부 채움")
    lines.append("")

    lines.append("## Deprecation Candidates")
    lines.append("")
    if report["deprecation_candidates"]:
        rows = [
            [
                f"`{p['preset_id']}`",
                p["tier"],
                str(p["install_hits"]),
                str(p["match_hits"]),
                str(p["version_drift_minor"]),
                p["preview_lint_status"],
                ", ".join(p["deprecation_reasons"]),
            ]
            for p in report["deprecation_candidates"]
        ]
        lines.extend(
            _render_table(
                rows,
                ["Preset", "Tier", "Install", "Match", "Drift", "Lint", "Reasons"],
            )
        )
    else:
        lines.append("- ✅ 현재 후보 없음")
    lines.append("")

    deprecated_list = report.get("deprecated_presets", [])
    lines.append("## Deprecated")
    lines.append("")
    if deprecated_list:
        rows = [
            [
                f"`{p['preset_id']}`",
                p.get("tier", "—"),
                p.get("deprecated_at", "—"),
                p.get("deprecation_reason") or "—",
                p.get("deprecated_replacement") or "—",
            ]
            for p in deprecated_list
        ]
        lines.extend(
            _render_table(
                rows,
                ["Preset", "Tier", "Deprecated at", "Reason", "Replacement"],
            )
        )
    else:
        lines.append("- ✅ 현재 deprecated 프리셋 없음")
    lines.append("")

    prune_list = report.get("prune_eligible_presets", [])
    age_threshold = report.get("prune_min_deprecated_age_days", PRUNE_MIN_DEPRECATED_AGE_DAYS)
    lines.append("## Prune Eligible")
    lines.append("")
    lines.append(
        f"> `deprecated_at` 이후 {age_threshold}일 이상 경과 + install/match hits 0 인 "
        f"프리셋. `uv run design-ontology prune-preset <id> --confirm` 으로 실삭제."
    )
    lines.append("")
    if prune_list:
        rows = [
            [
                f"`{p['preset_id']}`",
                p.get("tier", "—"),
                str(p.get("deprecated_age_days") if p.get("deprecated_age_days") is not None else "—"),
                p.get("deprecated_at", "—"),
                p.get("deprecation_reason") or "—",
            ]
            for p in prune_list
        ]
        lines.extend(
            _render_table(
                rows,
                ["Preset", "Tier", "Age (days)", "Deprecated at", "Reason"],
            )
        )
    else:
        lines.append("- ✅ 현재 prune 대상 없음")
    lines.append("")

    lines.append("## Per-Preset Metrics")
    lines.append("")
    rows = [
        [
            f"`{p['preset_id']}`"
            + (" 🗑️" if p.get("is_deprecated") else ""),
            p["tier"],
            p["owner"] or "—",
            p["generated_by_harness_version"] or "—",
            str(p["version_drift_minor"]),
            p["preview_lint_status"],
            str(p["install_hits"]),
            str(p["match_hits"]),
            "⚠️" if p["snapshot_drift"] else "·",
        ]
        for p in report["presets"]
    ]
    lines.extend(
        _render_table(
            rows,
            ["Preset", "Tier", "Owner", "Harness ver", "Drift", "Lint", "Install", "Match", "Snapshot"],
        )
    )
    lines.append("")
    if report["snapshot_drift_count"]:
        lines.append("> Snapshot drift detected — rebuild 후 `pytest tests/test_preset_snapshots.py --update-snapshots` 로 갱신.")
        lines.append("")

    lines.append("## Sources")
    lines.append("")
    src = report["metrics_sources"]
    lines.append(f"- install hits: `{src['install_hits_file']}`")
    lines.append(f"- match hits: `{src['match_hits_file']}`")
    lines.append(f"- snapshot fixture: `{src['snapshot_fixture']}`")
    lines.append("")

    return "\n".join(lines)


def format_summary(report: dict) -> str:
    cov = report["cell_coverage"]
    counts = report["tier_counts"]
    lines = [
        f"[catalog-health] 누적 {report['preset_total']}종 (P0 {counts.get('P0',0)} / P1 {counts.get('P1',0)} / P2 {counts.get('P2',0)} / P3 {counts.get('P3',0)})",
        f"  셀 커버리지: {cov['occupied']}/{cov['total']} ({cov['ratio']:.0%})",
        f"  Snapshot drift: {report['snapshot_drift_count']}건",
        f"  Deprecation 후보: {len(report['deprecation_candidates'])}건",
        f"  Deprecated: {report.get('deprecated_count', 0)}건",
        f"  Prune eligible: {report.get('prune_eligible_count', 0)}건",
        f"  harness version: {report['harness_version']}",
    ]
    top10 = report["priority_empty_cells_top10"]
    if top10:
        lines.append(f"  Priority 빈 셀 top-{len(top10)}:")
        for item in top10[:5]:
            lines.append(f"    {item['priority']}. {item['app_mode']}--{item['brand_tone']}")
        if len(top10) > 5:
            lines.append(f"    … (+{len(top10) - 5}건)")
    else:
        lines.append("  ✅ Top-10 priority 셀 모두 채움")
    if report["deprecation_candidates"]:
        ids = ", ".join(p["preset_id"] for p in report["deprecation_candidates"][:3])
        suffix = "" if len(report["deprecation_candidates"]) <= 3 else f" (+{len(report['deprecation_candidates']) - 3})"
        lines.append(f"  ⚠️ deprecation 후보: {ids}{suffix}")
    return "\n".join(lines)
