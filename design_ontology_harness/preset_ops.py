"""Preset lifecycle operations — rebuild / promote / deprecate.

Three independent entry points live here:

- ``rebuild_all(projects_root)``
    Walk ``matrix.json`` and rebuild every preset from its source_project
    (Phase 7-8 / 15-5 path).

- ``promote_preset(preset_id, target_tier, ...)`` (Phase 15-2)
    Move a preset up the tier ladder (P3 → P2 → P1 → P0). Runs five gates
    (validate-presets, lint-previews, adapter round-trip, sources.json
    presence, self-match Top-1). Writes ``promoted_at`` / ``promoted_from``
    on the manifest and updates ``matrix.json``. ``dry_run=True`` runs all
    gates without touching disk.

- ``deprecate_preset(preset_id, *, reason, replacement=None, force=False)``
    (Phase 15-3)
    Mark a preset deprecated on its manifest (``deprecated_at`` /
    ``deprecation_reason`` / ``deprecated_replacement``). The matcher hides
    deprecated presets by default; ``eval.py`` / ``validate-community-preset``
    keep them visible via ``include_deprecated=True``.

Stdlib only. Adapter round-trip reuses the existing installer helpers.
"""

from __future__ import annotations

import json
import re
import shutil
import tempfile
from dataclasses import dataclass, field
from datetime import datetime, timedelta, timezone
from pathlib import Path

from .preset_builder import (
    MATRIX_PATH,
    PRESETS_ROOT,
    BuildRequest,
    build_preset,
)
from .utils import write_json


TIER_ORDER: tuple[str, ...] = ("P3", "P2", "P1", "P0")
TIER_RANK: dict[str, int] = {tier: idx for idx, tier in enumerate(TIER_ORDER)}

DEPRECATION_REASONS: tuple[str, ...] = (
    "zero_hits",
    "version_lag",
    "snapshot_drift",
    "owner_abandoned",
    "manual",
)
_MANUAL_REASON_RE = re.compile(r"^manual(:.+)?$")

# Adapters exercised by the promote round-trip gate. Kept narrow on purpose:
# Next + Raw cover the two shipping adapters; Vite is still beta so skipping
# it here keeps the gate fast while still proving multi-adapter compatibility.
_ROUND_TRIP_ADAPTERS: tuple[str, ...] = (
    "nextjs-tailwind-shadcn",
    "raw-css-variables",
)


# ---------------------------------------------------------------------------
# rebuild-all (Phase 7-8)


@dataclass
class RebuildReport:
    succeeded: list[str] = field(default_factory=list)
    failed: list[tuple[str, str]] = field(default_factory=list)

    @property
    def ok(self) -> bool:
        return not self.failed


def rebuild_all(projects_root: Path) -> RebuildReport:
    if not MATRIX_PATH.exists():
        raise FileNotFoundError(f"matrix.json not found at {MATRIX_PATH}")
    matrix = json.loads(MATRIX_PATH.read_text(encoding="utf-8"))
    report = RebuildReport()

    for entry in matrix.get("presets", []):
        preset_id = entry["id"]
        try:
            source = projects_root / entry["source_project"]
            if not source.exists():
                raise FileNotFoundError(f"source_project directory not found: {source}")
            request = BuildRequest(
                project_dir=source,
                preset_id=preset_id,
                color_modes=list(entry["color_modes"]),
                default_color_mode=entry["default_color_mode"],
                tags=list(entry.get("tags", [])),
                owner=entry["owner"],
                tier=entry["tier"],
                description=entry.get("description"),
                locale_pairings=entry.get("locale_pairings") or None,
            )
            build_preset(request)
            report.succeeded.append(preset_id)
        except Exception as exc:  # noqa: BLE001 — collect all failures
            report.failed.append((preset_id, f"{type(exc).__name__}: {exc}"))

    return report


def format_rebuild_report(report: RebuildReport) -> str:
    lines = [f"Succeeded ({len(report.succeeded)}):"]
    for pid in report.succeeded:
        lines.append(f"  + {pid}")
    if report.failed:
        lines.append(f"\nFailed ({len(report.failed)}):")
        for pid, reason in report.failed:
            lines.append(f"  - {pid}: {reason}")
    else:
        lines.append("\nAll presets rebuilt successfully.")
    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Shared helpers


def _now_iso() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def _load_manifest(preset_dir: Path) -> dict:
    path = preset_dir / "manifest.json"
    if not path.exists():
        raise FileNotFoundError(f"manifest.json not found: {path}")
    return json.loads(path.read_text(encoding="utf-8"))


def _write_manifest(preset_dir: Path, manifest: dict) -> None:
    write_json(preset_dir / "manifest.json", manifest)


def _resolve_matrix_path(presets_root: Path | None) -> Path:
    if presets_root is None or presets_root == PRESETS_ROOT:
        return MATRIX_PATH
    return presets_root / "matrix.json"


def _load_matrix(matrix_path: Path) -> dict:
    return json.loads(matrix_path.read_text(encoding="utf-8"))


def _save_matrix(matrix: dict, matrix_path: Path) -> None:
    write_json(matrix_path, matrix)


def _update_matrix_tier(preset_id: str, new_tier: str, matrix_path: Path) -> None:
    matrix = _load_matrix(matrix_path)
    presets = matrix.get("presets", [])
    updated = False
    for entry in presets:
        if entry.get("id") == preset_id:
            entry["tier"] = new_tier
            updated = True
            break
    if not updated:
        raise ValueError(
            f"preset '{preset_id}' not found in matrix.json — rebuild first"
        )
    matrix["presets"] = presets
    _save_matrix(matrix, matrix_path)


# ---------------------------------------------------------------------------
# Promotion (Phase 15-2)


@dataclass
class GateResult:
    name: str
    passed: bool
    detail: str = ""


@dataclass
class PromoteReport:
    preset_id: str
    from_tier: str
    target_tier: str
    gates: list[GateResult] = field(default_factory=list)
    promoted_at: str | None = None
    dry_run: bool = False
    error: str | None = None

    @property
    def ok(self) -> bool:
        return self.error is None and all(g.passed for g in self.gates)


def _next_tier_up(current: str) -> str:
    rank = TIER_RANK.get(current)
    if rank is None:
        raise ValueError(f"tier must be one of {TIER_ORDER}, got {current}")
    if rank == len(TIER_ORDER) - 1:
        raise ValueError(f"preset already at top tier '{current}' — nothing to promote")
    return TIER_ORDER[rank + 1]


def _validate_gate(preset_id: str, presets_root: Path) -> GateResult:
    from .preset_validator import validate_all

    report = validate_all(presets_root)
    tagged = [e for e in report.errors if f"[{preset_id}]" in e]
    if tagged:
        detail = "; ".join(tagged[:3])
        return GateResult("validate-presets", False, detail)
    return GateResult("validate-presets", True, f"{len(report.checked_presets)} preset(s) OK")


def _lint_gate(preset_id: str, presets_root: Path) -> GateResult:
    from .preview_linter import lint_preview

    preset_dir = presets_root / preset_id
    report = lint_preview(preset_dir)
    if report.errors:
        detail = "; ".join(f"{e.code} {e.message}" for e in report.errors[:3])
        return GateResult("lint-previews", False, detail)
    warn_suffix = f" ({len(report.warnings)} warnings)" if report.warnings else ""
    return GateResult("lint-previews", True, f"preview.md clean{warn_suffix}")


def _sources_gate(preset_id: str, presets_root: Path, *, strict: bool) -> GateResult:
    """sources.json presence gate.

    PLAN §11.1 requires ``sources.json`` for presets promoted off the
    community P3 track. Legacy P0/P1/P2 presets predate the rule, so their
    further promotions (P2→P1 / P1→P0) log a pass-with-note instead of
    blocking. ``strict=True`` (set by the caller when ``from_tier == 'P3'``)
    enforces the rule for new contributions.
    """

    path = presets_root / preset_id / "sources.json"
    if path.exists():
        return GateResult("sources.json", True, f"{path.name} present")
    if strict:
        return GateResult(
            "sources.json", False, f"{path} missing (required for P3 → P2 promotion)"
        )
    return GateResult(
        "sources.json", True, "missing (legacy preset — warning only)"
    )


def _self_match_gate(
    preset_id: str,
    preset_dir: Path,
    *,
    matrix_path: Path | None = None,
) -> GateResult:
    from .preset_matcher.engine import MatchQuery, match_presets

    manifest = _load_manifest(preset_dir)
    query = MatchQuery(
        app_mode=manifest.get("app_mode"),
        brand_tone=manifest.get("brand_tone"),
        tags=list(manifest.get("tags") or []),
    )
    results = match_presets(
        query,
        top_k=3,
        include_deprecated=True,
        matrix_path=matrix_path,
    )
    if not results:
        return GateResult("self-match", False, "matcher returned no results")
    top = results[0]
    if top.preset_id != preset_id:
        return GateResult(
            "self-match",
            False,
            f"Top-1 is {top.preset_id} (expected {preset_id}, "
            f"score={top.raw_score:.3f}, bucket={top.bucket})",
        )
    return GateResult(
        "self-match",
        True,
        f"Top-1 = {preset_id} (score={top.raw_score:.3f}, bucket={top.bucket})",
    )


def _adapter_round_trip_gate(preset_id: str, presets_root: Path) -> GateResult:
    """Install the preset via each round-trip adapter into a temp dir.

    Success criterion: ``install_preset`` completes without raising and returns
    status in {installed, reinstalled}. At least one adapter must pass; every
    attempt is logged in ``detail``.
    """

    from .preset_installer import InstallRequest, install_preset

    outcomes: list[str] = []
    at_least_one_passed = False
    with tempfile.TemporaryDirectory(prefix=f"promote-{preset_id}-") as tmpdir:
        for adapter_id in _ROUND_TRIP_ADAPTERS:
            target = Path(tmpdir) / adapter_id
            try:
                outcome = install_preset(
                    InstallRequest(
                        preset_id=preset_id,
                        target_repo=target,
                        adapter_id=adapter_id,
                        presets_root=presets_root,
                    )
                )
            except Exception as exc:  # noqa: BLE001
                outcomes.append(f"{adapter_id}: {type(exc).__name__}: {exc}")
                continue
            if outcome.status in {"installed", "reinstalled"}:
                at_least_one_passed = True
                outcomes.append(
                    f"{adapter_id}@{outcome.adapter_version} {outcome.status} "
                    f"(created={len(outcome.created)})"
                )
            else:
                outcomes.append(f"{adapter_id}: unexpected status={outcome.status}")

    if not at_least_one_passed:
        return GateResult("adapter-round-trip", False, " | ".join(outcomes))
    return GateResult("adapter-round-trip", True, " | ".join(outcomes))


def promote_preset(
    preset_id: str,
    target_tier: str | None = None,
    *,
    dry_run: bool = False,
    projects_root: Path | None = None,
    presets_root: Path | None = None,
) -> PromoteReport:
    """Run promotion gates and, if all pass, bump the preset tier.

    Args:
        preset_id: existing preset id.
        target_tier: desired tier (``P0``/``P1``/``P2``). ``None`` bumps one
            step from the current tier.
        dry_run: skip manifest + matrix mutation even when all gates pass.
        projects_root: unused today (reserved for future "rebuild source
            before promoting" flows). Accepted for CLI symmetry.
        presets_root: override ``presets/`` (tests).
    """

    root = presets_root or PRESETS_ROOT
    preset_dir = root / preset_id
    if not preset_dir.is_dir():
        return PromoteReport(
            preset_id=preset_id,
            from_tier="?",
            target_tier=target_tier or "?",
            dry_run=dry_run,
            error=f"preset directory not found: {preset_dir}",
        )

    manifest = _load_manifest(preset_dir)
    from_tier = manifest.get("tier", "P?")
    if from_tier not in TIER_ORDER:
        return PromoteReport(
            preset_id=preset_id,
            from_tier=from_tier,
            target_tier=target_tier or "?",
            dry_run=dry_run,
            error=f"current tier '{from_tier}' not one of {TIER_ORDER}",
        )

    try:
        desired = target_tier or _next_tier_up(from_tier)
    except ValueError as exc:
        return PromoteReport(
            preset_id=preset_id,
            from_tier=from_tier,
            target_tier=target_tier or "?",
            dry_run=dry_run,
            error=str(exc),
        )

    if desired not in TIER_ORDER:
        return PromoteReport(
            preset_id=preset_id,
            from_tier=from_tier,
            target_tier=desired,
            dry_run=dry_run,
            error=f"target_tier must be one of {TIER_ORDER}, got {desired}",
        )
    if TIER_RANK[desired] <= TIER_RANK[from_tier]:
        return PromoteReport(
            preset_id=preset_id,
            from_tier=from_tier,
            target_tier=desired,
            dry_run=dry_run,
            error=(
                f"target_tier '{desired}' is not above current tier '{from_tier}' — "
                "use deprecate-preset to retire or edit the manifest manually"
            ),
        )

    # sources.json is strict only for the community P3 → P2 promotion.
    # Legacy P0/P1/P2 presets created before the rule keep passing with a
    # note so their upward moves are not blocked retroactively.
    sources_strict = from_tier == "P3"

    matrix_path = _resolve_matrix_path(presets_root)
    gates: list[GateResult] = [
        _validate_gate(preset_id, root),
        _lint_gate(preset_id, root),
        _adapter_round_trip_gate(preset_id, root),
        _sources_gate(preset_id, root, strict=sources_strict),
        _self_match_gate(preset_id, preset_dir, matrix_path=matrix_path),
    ]

    report = PromoteReport(
        preset_id=preset_id,
        from_tier=from_tier,
        target_tier=desired,
        gates=gates,
        dry_run=dry_run,
    )

    if not report.ok or dry_run:
        return report

    manifest["tier"] = desired
    manifest["promoted_at"] = _now_iso()
    manifest["promoted_from"] = from_tier
    _write_manifest(preset_dir, manifest)
    _update_matrix_tier(preset_id, desired, matrix_path)
    report.promoted_at = manifest["promoted_at"]
    return report


def format_promote_report(report: PromoteReport) -> str:
    lines = [
        f"[promote-preset] {report.preset_id}: {report.from_tier} → {report.target_tier}"
        + ("  (dry-run)" if report.dry_run else "")
    ]
    if report.error:
        lines.append(f"  error: {report.error}")
        return "\n".join(lines)

    for gate in report.gates:
        marker = "✓" if gate.passed else "✗"
        suffix = f" — {gate.detail}" if gate.detail else ""
        lines.append(f"  {marker} {gate.name}{suffix}")

    if report.ok and not report.dry_run:
        lines.append(f"  promoted at {report.promoted_at}")
    elif report.ok and report.dry_run:
        lines.append("  all gates passed — manifest/matrix unchanged (dry-run)")
    else:
        lines.append("  one or more gates failed — preset not promoted")
    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Deprecation (Phase 15-3)


@dataclass
class DeprecateReport:
    preset_id: str
    reason: str
    replacement: str | None = None
    deprecated_at: str | None = None
    previous_reason: str | None = None
    error: str | None = None

    @property
    def ok(self) -> bool:
        return self.error is None


def _validate_reason(reason: str) -> None:
    if reason in DEPRECATION_REASONS:
        return
    if _MANUAL_REASON_RE.match(reason):
        return
    raise ValueError(
        f"deprecation_reason must be one of {DEPRECATION_REASONS} "
        f"or 'manual:<text>', got '{reason}'"
    )


def deprecate_preset(
    preset_id: str,
    *,
    reason: str,
    replacement: str | None = None,
    force: bool = False,
    presets_root: Path | None = None,
) -> DeprecateReport:
    root = presets_root or PRESETS_ROOT
    preset_dir = root / preset_id
    if not preset_dir.is_dir():
        return DeprecateReport(
            preset_id=preset_id,
            reason=reason,
            replacement=replacement,
            error=f"preset directory not found: {preset_dir}",
        )

    try:
        _validate_reason(reason)
    except ValueError as exc:
        return DeprecateReport(
            preset_id=preset_id,
            reason=reason,
            replacement=replacement,
            error=str(exc),
        )

    if replacement:
        replacement_dir = root / replacement
        if not replacement_dir.is_dir():
            return DeprecateReport(
                preset_id=preset_id,
                reason=reason,
                replacement=replacement,
                error=f"replacement preset not found: {replacement}",
            )

    manifest = _load_manifest(preset_dir)
    previous = manifest.get("deprecation_reason")
    if manifest.get("deprecated_at") and not force:
        return DeprecateReport(
            preset_id=preset_id,
            reason=reason,
            replacement=replacement,
            previous_reason=previous,
            error=(
                f"already deprecated at {manifest['deprecated_at']} "
                f"(reason: {previous}) — pass --force to update"
            ),
        )

    manifest["deprecated_at"] = _now_iso()
    manifest["deprecation_reason"] = reason
    if replacement:
        manifest["deprecated_replacement"] = replacement
    elif "deprecated_replacement" in manifest and not replacement:
        # Preserve existing replacement unless caller explicitly overrides;
        # to clear, pass replacement="" (not supported via CLI to avoid footgun).
        pass
    _write_manifest(preset_dir, manifest)

    return DeprecateReport(
        preset_id=preset_id,
        reason=reason,
        replacement=replacement,
        deprecated_at=manifest["deprecated_at"],
        previous_reason=previous,
    )


def format_deprecate_report(report: DeprecateReport) -> str:
    lines = [f"[deprecate-preset] {report.preset_id}"]
    if report.error:
        lines.append(f"  error: {report.error}")
        return "\n".join(lines)
    lines.append(f"  deprecated_at    = {report.deprecated_at}")
    lines.append(f"  deprecation_reason = {report.reason}")
    if report.replacement:
        lines.append(f"  deprecated_replacement = {report.replacement}")
    if report.previous_reason and report.previous_reason != report.reason:
        lines.append(f"  (previous reason: {report.previous_reason})")
    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Utility: enumerate deprecated preset ids (matcher + catalog_health use)


def load_deprecated_ids(presets_root: Path | None = None) -> set[str]:
    root = presets_root or PRESETS_ROOT
    matrix_path = MATRIX_PATH if root == PRESETS_ROOT else root / "matrix.json"
    if not matrix_path.exists():
        return set()
    try:
        matrix = json.loads(matrix_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return set()
    deprecated: set[str] = set()
    for entry in matrix.get("presets", []):
        preset_id = entry.get("id")
        if not preset_id:
            continue
        manifest_path = root / preset_id / "manifest.json"
        if not manifest_path.exists():
            continue
        try:
            manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            continue
        if manifest.get("deprecated_at"):
            deprecated.add(preset_id)
    return deprecated


def load_preset_deprecation_info(preset_id: str, presets_root: Path | None = None) -> dict:
    root = presets_root or PRESETS_ROOT
    manifest_path = root / preset_id / "manifest.json"
    if not manifest_path.exists():
        return {}
    try:
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return {}
    if not manifest.get("deprecated_at"):
        return {}
    return {
        "deprecated_at": manifest.get("deprecated_at"),
        "deprecation_reason": manifest.get("deprecation_reason"),
        "deprecated_replacement": manifest.get("deprecated_replacement"),
    }


# ---------------------------------------------------------------------------
# Pruning (Phase 15-4)

DEFAULT_MIN_DEPRECATED_AGE_DAYS = 90
REPO_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_SNAPSHOT_FIXTURE = REPO_ROOT / "tests" / "fixtures" / "preset_snapshots.json"
METRICS_DIR_NAME = ".metrics"
INSTALL_HITS_FILE = "install_hits.json"
MATCH_HITS_FILE = "match_hits.json"


@dataclass
class PruneCheck:
    name: str
    passed: bool
    detail: str = ""


@dataclass
class PruneReport:
    preset_id: str
    checks: list[PruneCheck] = field(default_factory=list)
    dry_run: bool = True
    deleted: bool = False
    deleted_at: str | None = None
    error: str | None = None

    @property
    def ok(self) -> bool:
        return self.error is None and all(c.passed for c in self.checks)


def _parse_iso(value: str) -> datetime | None:
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


def _load_metrics_counters(metrics_dir: Path) -> tuple[dict, dict]:
    install_path = metrics_dir / INSTALL_HITS_FILE
    match_path = metrics_dir / MATCH_HITS_FILE
    install: dict = {}
    match: dict = {}
    if install_path.exists():
        try:
            payload = json.loads(install_path.read_text(encoding="utf-8"))
            if isinstance(payload, dict):
                install = payload
        except json.JSONDecodeError:
            install = {}
    if match_path.exists():
        try:
            payload = json.loads(match_path.read_text(encoding="utf-8"))
            if isinstance(payload, dict):
                match = payload
        except json.JSONDecodeError:
            match = {}
    return install, match


def _remove_matrix_entry(preset_id: str, matrix_path: Path) -> bool:
    if not matrix_path.exists():
        return False
    matrix = _load_matrix(matrix_path)
    presets = matrix.get("presets", [])
    new_presets = [entry for entry in presets if entry.get("id") != preset_id]
    if len(new_presets) == len(presets):
        return False
    matrix["presets"] = new_presets
    _save_matrix(matrix, matrix_path)
    return True


def _remove_snapshot_entry(preset_id: str, snapshot_path: Path) -> bool:
    if not snapshot_path.exists():
        return False
    try:
        data = json.loads(snapshot_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return False
    if not isinstance(data, dict) or preset_id not in data:
        return False
    del data[preset_id]
    write_json(snapshot_path, data)
    return True


def prune_preset(
    preset_id: str,
    *,
    confirm: bool = False,
    dry_run: bool = True,
    presets_root: Path | None = None,
    metrics_dir: Path | None = None,
    snapshot_fixture_path: Path | None = None,
    min_deprecated_age_days: int = DEFAULT_MIN_DEPRECATED_AGE_DAYS,
) -> PruneReport:
    """Physically remove a deprecated preset after all safety gates pass.

    Gates (all must pass):
      a. manifest.deprecated_at is present
      b. deprecated_at is at least ``min_deprecated_age_days`` old
      c. install_hits + match_hits are still 0
      d. ``confirm=True`` when ``dry_run=False`` (actual deletion)

    Side effects on success (non-dry-run):
      - presets/<id>/ directory removed (shutil.rmtree)
      - matrix.json entry removed
      - tests/fixtures/preset_snapshots.json entry removed
    """

    root = presets_root or PRESETS_ROOT
    preset_dir = root / preset_id
    report = PruneReport(preset_id=preset_id, dry_run=dry_run)

    if not preset_dir.is_dir():
        report.error = f"preset directory not found: {preset_dir}"
        return report

    manifest: dict = {}
    try:
        manifest = _load_manifest(preset_dir)
    except FileNotFoundError as exc:
        report.error = str(exc)
        return report

    # --- Gate a: manifest has deprecated_at ----------------------------------
    deprecated_at_raw = manifest.get("deprecated_at")
    if not deprecated_at_raw:
        report.checks.append(
            PruneCheck(
                "deprecated",
                False,
                "manifest has no deprecated_at — run deprecate-preset first",
            )
        )
        return report
    report.checks.append(
        PruneCheck(
            "deprecated",
            True,
            f"deprecated_at={deprecated_at_raw} "
            f"(reason: {manifest.get('deprecation_reason', '?')})",
        )
    )

    # --- Gate b: age >= min_deprecated_age_days ------------------------------
    deprecated_at = _parse_iso(deprecated_at_raw)
    if deprecated_at is None:
        report.checks.append(
            PruneCheck(
                "age",
                False,
                f"deprecated_at '{deprecated_at_raw}' is not valid ISO8601",
            )
        )
        return report
    age_delta = datetime.now(timezone.utc) - deprecated_at
    min_delta = timedelta(days=min_deprecated_age_days)
    if age_delta < min_delta:
        remaining = (min_delta - age_delta).days
        report.checks.append(
            PruneCheck(
                "age",
                False,
                f"age={age_delta.days}d, requires {min_deprecated_age_days}d "
                f"— {remaining}d remaining",
            )
        )
        return report
    report.checks.append(
        PruneCheck(
            "age",
            True,
            f"age={age_delta.days}d ≥ {min_deprecated_age_days}d",
        )
    )

    # --- Gate c: hits still 0 ------------------------------------------------
    mdir = metrics_dir if metrics_dir is not None else (root / METRICS_DIR_NAME)
    install_hits, match_hits = _load_metrics_counters(mdir)
    install_count = int(install_hits.get(preset_id, 0) or 0)
    match_count = int(match_hits.get(preset_id, 0) or 0)
    if install_count > 0 or match_count > 0:
        report.checks.append(
            PruneCheck(
                "zero-hits",
                False,
                f"install_hits={install_count}, match_hits={match_count} "
                "— preset is in use, refusing to prune",
            )
        )
        return report
    report.checks.append(
        PruneCheck(
            "zero-hits",
            True,
            "install_hits=0, match_hits=0",
        )
    )

    # --- Gate d: --confirm when not dry-run ----------------------------------
    if not dry_run and not confirm:
        report.checks.append(
            PruneCheck(
                "confirm",
                False,
                "--confirm required for actual deletion (pruning is irreversible)",
            )
        )
        return report
    report.checks.append(
        PruneCheck(
            "confirm",
            True,
            "dry-run mode" if dry_run else "--confirm supplied",
        )
    )

    if dry_run:
        return report

    # --- Perform deletion ----------------------------------------------------
    shutil.rmtree(preset_dir)
    matrix_path = _resolve_matrix_path(presets_root)
    _remove_matrix_entry(preset_id, matrix_path)
    snapshot_path = snapshot_fixture_path or DEFAULT_SNAPSHOT_FIXTURE
    _remove_snapshot_entry(preset_id, Path(snapshot_path))

    report.deleted = True
    report.deleted_at = _now_iso()
    return report


def format_prune_report(report: PruneReport) -> str:
    suffix = "  (dry-run)" if report.dry_run and not report.deleted else ""
    lines = [f"[prune-preset] {report.preset_id}{suffix}"]
    if report.error:
        lines.append(f"  error: {report.error}")
        return "\n".join(lines)
    for check in report.checks:
        marker = "✓" if check.passed else "✗"
        detail = f" — {check.detail}" if check.detail else ""
        lines.append(f"  {marker} {check.name}{detail}")
    if report.deleted:
        lines.append(f"  removed at {report.deleted_at}")
    elif report.ok and report.dry_run:
        lines.append("  all gates passed — pass --confirm (without --dry-run) to delete")
    elif not report.ok:
        lines.append("  one or more gates failed — preset not removed")
    return "\n".join(lines)


# ---------------------------------------------------------------------------
# KB sources (Phase 15-9)

PRETENDARD_FONT_LICENSE = "SIL OFL 1.1"
SOURCES_FILENAME = "sources.json"
PROJECTS_ROOT_DEFAULT = REPO_ROOT / "projects"

# Well-known domains → kind classification. Keep narrow on purpose; anything
# unknown falls back to "article".
_DOMAIN_KIND_HINTS: tuple[tuple[tuple[str, ...], str], ...] = (
    (
        (
            "linear.app", "stripe.com", "vercel.com", "shadcn", "material.io",
            "developer.apple.com", "m3.material.io", "carbondesignsystem.com",
            "polaris.shopify.com", "atlassian.design", "fluent2.microsoft.design",
            "primer.style", "spectrum.adobe.com", "base.uber.com", "ant.design",
            "chakra-ui.com", "radix-ui.com", "mui.com", "pretendard.com",
        ),
        "design-system",
    ),
    (
        (
            "figma.com", "framer.com", "excalidraw.com", "tldraw.com",
            "rive.app", "spline.design", "dribbble.com", "pinterest.com",
            "are.na", "behance.net",
        ),
        "visual-reference",
    ),
    (
        (
            "brand.uber.com", "brand.airbnb.com", "brand.slack.com",
            "brand.dropbox.com", "logo.clearbit.com", "brandpad.io",
        ),
        "brand-guide",
    ),
    (
        (
            "docs.stripe.com", "vercel.com/docs", "developer.mozilla.org",
            "docs.github.com", "docs.flutter.dev", "nextjs.org/docs",
            "react.dev", "tailwindcss.com/docs",
        ),
        "reference-docs",
    ),
)

_URL_RE = re.compile(r"^https?://", re.IGNORECASE)
_MD_LINK_RE = re.compile(r"\[([^\]]+)\]\(([^)]+)\)")


def _canonicalize_url(url: str) -> str:
    url = (url or "").strip()
    if not url:
        return ""
    while url.endswith("/"):
        url = url[:-1]
    return url


def _infer_kind(url: str) -> str:
    lowered = url.lower()
    for domains, kind in _DOMAIN_KIND_HINTS:
        for domain in domains:
            if domain in lowered:
                return kind
    return "article"


def _derive_title(url: str) -> str:
    """Fallback title: strip scheme + trailing slashes."""

    cleaned = re.sub(r"^https?://", "", url, flags=re.IGNORECASE)
    return cleaned.rstrip("/")


def _normalize_seed(raw: object) -> dict | None:
    """Normalize a seed entry into `{url, kind, title, notes}`.

    Accepts strings (URL) or dicts with {url, kind?, title?, notes?}.
    """

    if isinstance(raw, str):
        url = _canonicalize_url(raw)
        if not url or not _URL_RE.match(url):
            return None
        return {
            "url": url,
            "kind": _infer_kind(url),
            "title": _derive_title(url),
            "notes": "",
        }
    if isinstance(raw, dict):
        url = _canonicalize_url(str(raw.get("url") or ""))
        if not url or not _URL_RE.match(url):
            return None
        return {
            "url": url,
            "kind": str(raw.get("kind") or _infer_kind(url)),
            "title": str(raw.get("title") or _derive_title(url)),
            "notes": str(raw.get("notes") or ""),
        }
    return None


def _extract_markdown_links(text: str) -> list[dict]:
    seeds: list[dict] = []
    for match in _MD_LINK_RE.finditer(text or ""):
        title = match.group(1).strip()
        url = _canonicalize_url(match.group(2))
        if not _URL_RE.match(url):
            continue
        seeds.append({
            "url": url,
            "kind": _infer_kind(url),
            "title": title or _derive_title(url),
            "notes": "",
        })
    return seeds


@dataclass
class SourcesResult:
    preset_id: str
    source_project: str
    seeds: list[dict] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
    written_path: Path | None = None
    skipped: bool = False
    reason: str | None = None

    @property
    def ok(self) -> bool:
        return self.reason is None


def build_sources_json(
    preset_id: str,
    *,
    presets_root: Path | None = None,
    projects_root: Path | None = None,
    force: bool = False,
    write: bool = True,
) -> SourcesResult:
    """Generate ``presets/<preset_id>/sources.json`` from project KB seeds.

    Inputs (in priority order):
      1. ``projects/<source_project>/brand_profile.json.seeds`` (list[str] or
         list[dict])
      2. ``projects/<source_project>/brand_profile.json.visual_reference.source_references``
         (list[str] or list[dict])
      3. Markdown links inside ``projects/<source_project>/spec.md``
    """

    root = presets_root or PRESETS_ROOT
    projects = projects_root or PROJECTS_ROOT_DEFAULT
    preset_dir = root / preset_id
    sources_path = preset_dir / SOURCES_FILENAME

    result = SourcesResult(preset_id=preset_id, source_project="")
    if not preset_dir.is_dir():
        result.reason = f"preset directory not found: {preset_dir}"
        return result

    manifest_path = preset_dir / "manifest.json"
    if not manifest_path.exists():
        result.reason = f"manifest.json missing: {manifest_path}"
        return result
    try:
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        result.reason = f"manifest.json parse error: {exc}"
        return result
    source_project = manifest.get("source_project") or ""
    result.source_project = source_project

    if sources_path.exists() and not force:
        result.skipped = True
        result.reason = "sources.json already exists (pass --force to overwrite)"
        return result

    project_dir = projects / source_project if source_project else None
    brand_profile: dict = {}
    spec_text: str = ""
    if project_dir and project_dir.is_dir():
        bp_path = project_dir / "brand_profile.json"
        if bp_path.exists():
            try:
                brand_profile = json.loads(bp_path.read_text(encoding="utf-8"))
            except json.JSONDecodeError:
                result.warnings.append(f"brand_profile.json parse error: {bp_path}")
        spec_path = project_dir / "spec.md"
        if spec_path.exists():
            spec_text = spec_path.read_text(encoding="utf-8", errors="replace")
    else:
        result.warnings.append(
            f"projects/{source_project}/ not found — seeds will be empty"
        )

    raw_seeds = list(brand_profile.get("seeds") or [])
    visual_ref = brand_profile.get("visual_reference") or {}
    raw_seeds.extend(list(visual_ref.get("source_references") or []))

    seeds: list[dict] = []
    seen: set[str] = set()
    for raw in raw_seeds:
        normalized = _normalize_seed(raw)
        if normalized is None:
            continue
        if normalized["url"] in seen:
            continue
        seen.add(normalized["url"])
        seeds.append(normalized)

    for entry in _extract_markdown_links(spec_text):
        if entry["url"] in seen:
            continue
        seen.add(entry["url"])
        seeds.append(entry)

    if len(seeds) < 3:
        result.warnings.append(
            f"only {len(seeds)} seed(s) — "
            f"brand_profile.json.seeds 를 최소 3개 이상 채우면 커뮤니티 제출 gate 통과가 쉬워집니다"
        )

    payload = {
        "preset_id": preset_id,
        "source_project": source_project,
        "seeds": seeds,
        "pretendard_font_license": PRETENDARD_FONT_LICENSE,
        "created_at": _now_iso(),
    }
    result.seeds = seeds
    if write:
        write_json(sources_path, payload)
        result.written_path = sources_path
    return result


def build_sources_for_all(
    *,
    presets_root: Path | None = None,
    projects_root: Path | None = None,
    force: bool = False,
) -> list[SourcesResult]:
    root = presets_root or PRESETS_ROOT
    matrix_path = _resolve_matrix_path(presets_root)
    if not matrix_path.exists():
        return []
    matrix = _load_matrix(matrix_path)
    results: list[SourcesResult] = []
    for entry in matrix.get("presets", []):
        preset_id = entry.get("id")
        if not preset_id:
            continue
        results.append(
            build_sources_json(
                preset_id,
                presets_root=root,
                projects_root=projects_root,
                force=force,
            )
        )
    return results


def format_sources_result(result: SourcesResult) -> str:
    lines = [f"[build-sources] {result.preset_id} (source: {result.source_project})"]
    if result.reason:
        if result.skipped:
            lines.append(f"  skipped: {result.reason}")
        else:
            lines.append(f"  error: {result.reason}")
        return "\n".join(lines)
    kind_counts: dict[str, int] = {}
    for seed in result.seeds:
        kind_counts[seed["kind"]] = kind_counts.get(seed["kind"], 0) + 1
    kind_summary = ", ".join(f"{k}={v}" for k, v in sorted(kind_counts.items())) or "(none)"
    lines.append(f"  seeds: {len(result.seeds)} ({kind_summary})")
    if result.written_path:
        lines.append(f"  wrote: {result.written_path}")
    for warning in result.warnings:
        lines.append(f"  warn: {warning}")
    return "\n".join(lines)


def find_prune_eligible(
    *,
    presets_root: Path | None = None,
    metrics_dir: Path | None = None,
    min_deprecated_age_days: int = DEFAULT_MIN_DEPRECATED_AGE_DAYS,
) -> list[str]:
    """Return preset_ids eligible for pruning (deprecated ≥ N days + hits 0)."""

    root = presets_root or PRESETS_ROOT
    matrix_path = _resolve_matrix_path(presets_root)
    if not matrix_path.exists():
        return []
    try:
        matrix = json.loads(matrix_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return []
    mdir = metrics_dir if metrics_dir is not None else (root / METRICS_DIR_NAME)
    install_hits, match_hits = _load_metrics_counters(mdir)
    min_delta = timedelta(days=min_deprecated_age_days)
    now = datetime.now(timezone.utc)
    eligible: list[str] = []
    for entry in matrix.get("presets", []):
        preset_id = entry.get("id")
        if not preset_id:
            continue
        manifest_path = root / preset_id / "manifest.json"
        if not manifest_path.exists():
            continue
        try:
            manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            continue
        deprecated_at = _parse_iso(manifest.get("deprecated_at", ""))
        if deprecated_at is None:
            continue
        if now - deprecated_at < min_delta:
            continue
        if int(install_hits.get(preset_id, 0) or 0) > 0:
            continue
        if int(match_hits.get(preset_id, 0) or 0) > 0:
            continue
        eligible.append(preset_id)
    return eligible
