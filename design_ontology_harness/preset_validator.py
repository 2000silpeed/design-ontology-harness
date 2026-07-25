"""Preset validator — enforce version contract + structural invariants.

Checks:
  1. Required files exist per preset
  2. id == f"{app_mode}--{brand_tone}"
  3. 4 version fields present + valid semver
  4. preset_api_version within supported_preset_api_range
  5. adapter_compatibility references only adapters known in compatibility.json
  6. adapter_compatibility range contains the adapter's current version
     (Phase 15-7 — catches drift between shipped adapter code and preset
     declared ranges before sync)
  7. matrix.json entries ↔ presets/<id>/ tree round-trip
  8. default_color_mode ∈ color_modes
  9. deprecation fields are internally consistent (reason matches enum /
     manual:<text>, replacement points to a real preset)
"""

from __future__ import annotations

import json
import re
from dataclasses import dataclass, field
from pathlib import Path

from .preset_builder import (
    APP_MODES,
    BRAND_TONES,
    COMPATIBILITY_PATH,
    ID_RE,
    MATRIX_PATH,
    PRESETS_ROOT,
)
from .semver_range import is_valid_range, is_valid_version, satisfies


_DEPRECATION_ENUM = {
    "zero_hits",
    "version_lag",
    "snapshot_drift",
    "owner_abandoned",
    "manual",
}
_MANUAL_REASON_RE = re.compile(r"^manual(:.+)?$")


def _current_adapter_versions() -> dict[str, str]:
    """Return ``{adapter_id: version}`` for every registered adapter.

    Imported lazily to avoid pulling the adapter package into validator-only
    call sites (and to side-step any import-order surprises during tests that
    build the adapter registry on demand).
    """

    try:
        from .adapters import list_adapters, get_adapter
    except Exception:  # pragma: no cover — tolerate adapter module failures
        return {}
    versions: dict[str, str] = {}
    for adapter_id in list_adapters():
        try:
            cls = get_adapter(adapter_id)
        except KeyError:
            continue
        version = getattr(cls, "version", None)
        if isinstance(version, str) and is_valid_version(version):
            versions[adapter_id] = version
    return versions

REQUIRED_FILES = ["manifest.json", "preview.md", "system_spec.md", "token_schema.json"]
VERSION_FIELDS = [
    "schema_version",
    "preset_api_version",
    "generated_by_harness_version",
    "preview_version",
]


@dataclass
class ValidationReport:
    errors: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
    checked_presets: list[str] = field(default_factory=list)

    @property
    def ok(self) -> bool:
        return not self.errors

    def extend(self, other: "ValidationReport") -> None:
        self.errors.extend(other.errors)
        self.warnings.extend(other.warnings)
        self.checked_presets.extend(other.checked_presets)


def validate_all(
    presets_root: Path | None = None,
    *,
    adapter_versions: dict[str, str] | None = None,
) -> ValidationReport:
    root = presets_root or PRESETS_ROOT
    report = ValidationReport()

    if not root.exists():
        report.errors.append(f"presets/ directory not found: {root}")
        return report

    compat = _load_compatibility(root, report)
    if compat is None:
        return report

    known_adapters = _known_adapters(compat)
    supported_range = compat["supported_preset_api_range"]
    matrix = _load_matrix(root, report)
    versions = (
        adapter_versions if adapter_versions is not None else _current_adapter_versions()
    )

    preset_dirs = sorted(
        p
        for p in root.iterdir()
        if p.is_dir() and p.name != "__pycache__" and not p.name.startswith(".")
    )
    known_preset_ids = {p.name for p in preset_dirs if ID_RE.match(p.name)}
    for preset_dir in preset_dirs:
        report.extend(
            _validate_preset_dir(
                preset_dir=preset_dir,
                supported_range=supported_range,
                known_adapters=known_adapters,
                adapter_versions=versions,
                known_preset_ids=known_preset_ids,
            )
        )

    if matrix is not None:
        report.extend(_validate_matrix_consistency(matrix=matrix, preset_dirs=preset_dirs))

    return report


def _load_compatibility(root: Path, report: ValidationReport) -> dict | None:
    path = COMPATIBILITY_PATH if root == PRESETS_ROOT else root / "compatibility.json"
    if not path.exists():
        report.errors.append(f"compatibility.json not found at {path}")
        return None
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        report.errors.append(f"compatibility.json parse error: {exc}")
        return None

    if not is_valid_version(data.get("current_preset_api_version", "")):
        report.errors.append("compatibility.json.current_preset_api_version is not valid semver")
    if not is_valid_range(data.get("supported_preset_api_range", "")):
        report.errors.append("compatibility.json.supported_preset_api_range is not a valid range")
    return data


def _known_adapters(compat: dict) -> set[str]:
    adapters: set[str] = set()
    for entry in compat.get("entries", []):
        adapters.update(entry.get("adapter_ranges", {}).keys())
    return adapters


def _load_matrix(root: Path, report: ValidationReport) -> dict | None:
    path = MATRIX_PATH if root == PRESETS_ROOT else root / "matrix.json"
    if not path.exists():
        report.errors.append(f"matrix.json not found at {path}")
        return None
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        report.errors.append(f"matrix.json parse error: {exc}")
        return None


def _validate_preset_dir(
    *,
    preset_dir: Path,
    supported_range: str,
    known_adapters: set[str],
    adapter_versions: dict[str, str] | None = None,
    known_preset_ids: set[str] | None = None,
) -> ValidationReport:
    report = ValidationReport()
    preset_id = preset_dir.name
    report.checked_presets.append(preset_id)

    id_match = ID_RE.match(preset_id)
    if not id_match:
        report.errors.append(f"[{preset_id}] directory name does not match {{app_mode}}--{{brand_tone}}")
        return report

    for required in REQUIRED_FILES:
        if not (preset_dir / required).exists():
            report.errors.append(f"[{preset_id}] missing required file: {required}")

    manifest_path = preset_dir / "manifest.json"
    if not manifest_path.exists():
        return report

    try:
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        report.errors.append(f"[{preset_id}] manifest.json parse error: {exc}")
        return report

    if manifest.get("id") != preset_id:
        report.errors.append(f"[{preset_id}] manifest.id '{manifest.get('id')}' != directory name")

    app_mode, brand_tone = id_match.group(1), id_match.group(2)
    if app_mode not in APP_MODES:
        report.errors.append(f"[{preset_id}] app_mode '{app_mode}' not in allowed set")
    if brand_tone not in BRAND_TONES:
        report.errors.append(f"[{preset_id}] brand_tone '{brand_tone}' not in allowed set")
    if manifest.get("app_mode") != app_mode:
        report.errors.append(
            f"[{preset_id}] manifest.app_mode '{manifest.get('app_mode')}' != id-derived '{app_mode}'"
        )
    if manifest.get("brand_tone") != brand_tone:
        report.errors.append(
            f"[{preset_id}] manifest.brand_tone '{manifest.get('brand_tone')}' != id-derived '{brand_tone}'"
        )

    for field_name in VERSION_FIELDS:
        value = manifest.get(field_name)
        if not value:
            report.errors.append(f"[{preset_id}] missing version field: {field_name}")
            continue
        if not is_valid_version(value):
            report.errors.append(f"[{preset_id}] {field_name}='{value}' is not valid semver")

    api_version = manifest.get("preset_api_version")
    if api_version and is_valid_version(api_version) and is_valid_range(supported_range):
        if not satisfies(api_version, supported_range):
            report.errors.append(
                f"[{preset_id}] preset_api_version {api_version} outside supported range {supported_range}"
            )

    adapter_compat = manifest.get("adapter_compatibility", {})
    versions = adapter_versions or {}
    if not isinstance(adapter_compat, dict) or not adapter_compat:
        report.errors.append(f"[{preset_id}] adapter_compatibility missing or empty")
    else:
        for adapter_id, range_expr in adapter_compat.items():
            if adapter_id not in known_adapters:
                report.warnings.append(
                    f"[{preset_id}] adapter_compatibility references unknown adapter '{adapter_id}'"
                )
            if not is_valid_range(range_expr):
                report.errors.append(
                    f"[{preset_id}] adapter_compatibility['{adapter_id}']='{range_expr}' invalid range"
                )
                continue
            current = versions.get(adapter_id)
            if current and not satisfies(current, range_expr):
                report.errors.append(
                    f"[{preset_id}] adapter '{adapter_id}' current={current} "
                    f"outside range {range_expr}"
                )

    color_modes = manifest.get("color_modes", [])
    default_mode = manifest.get("default_color_mode")
    if not isinstance(color_modes, list) or not color_modes:
        report.errors.append(f"[{preset_id}] color_modes must be non-empty list")
    elif default_mode not in color_modes:
        report.errors.append(
            f"[{preset_id}] default_color_mode '{default_mode}' not in color_modes {color_modes}"
        )

    if not manifest.get("content_hash", "").startswith("sha256:"):
        report.errors.append(f"[{preset_id}] content_hash missing or malformed")
    if not manifest.get("owner"):
        report.errors.append(f"[{preset_id}] owner missing")
    if manifest.get("tier") not in {"P0", "P1", "P2", "P3"}:
        report.errors.append(f"[{preset_id}] tier must be P0/P1/P2/P3")

    token_schema = preset_dir / "token_schema.json"
    if token_schema.exists():
        try:
            json.loads(token_schema.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            report.errors.append(f"[{preset_id}] token_schema.json parse error: {exc}")

    if manifest.get("component_contract_version"):
        if manifest.get("component_contract_version") != "component-contract/v1":
            report.errors.append(
                f"[{preset_id}] unsupported component_contract_version "
                f"'{manifest.get('component_contract_version')}'"
            )
        component_specs_path = preset_dir / "components" / "component_specs.json"
        if not component_specs_path.exists():
            report.errors.append(f"[{preset_id}] component contract metadata requires components/component_specs.json")
        else:
            try:
                component_specs = json.loads(component_specs_path.read_text(encoding="utf-8"))
                from .component_contracts import validate_component_contracts

                contract_report = validate_component_contracts(component_specs, strict_authored=True)
                for error in contract_report["errors"]:
                    report.errors.append(f"[{preset_id}] component contract: {error}")
            except json.JSONDecodeError as exc:
                report.errors.append(f"[{preset_id}] component_specs.json parse error: {exc}")

    sources_path = preset_dir / "sources.json"
    if sources_path.exists():
        report.extend(_validate_sources_file(preset_id=preset_id, path=sources_path))

    deprecated_at = manifest.get("deprecated_at")
    deprecation_reason = manifest.get("deprecation_reason")
    deprecated_replacement = manifest.get("deprecated_replacement")
    if deprecated_at or deprecation_reason or deprecated_replacement:
        if not deprecated_at:
            report.errors.append(
                f"[{preset_id}] deprecation metadata present without deprecated_at"
            )
        if not deprecation_reason:
            report.errors.append(
                f"[{preset_id}] deprecated_at set but deprecation_reason missing"
            )
        elif (
            deprecation_reason not in _DEPRECATION_ENUM
            and not _MANUAL_REASON_RE.match(deprecation_reason)
        ):
            report.errors.append(
                f"[{preset_id}] deprecation_reason '{deprecation_reason}' not in "
                f"{sorted(_DEPRECATION_ENUM)} or 'manual:<text>'"
            )
        if deprecated_replacement:
            if known_preset_ids and deprecated_replacement not in known_preset_ids:
                report.errors.append(
                    f"[{preset_id}] deprecated_replacement '{deprecated_replacement}' "
                    f"does not exist under presets/"
                )
            if deprecated_replacement == preset_id:
                report.errors.append(
                    f"[{preset_id}] deprecated_replacement cannot point to itself"
                )

    return report


_SOURCES_URL_RE = re.compile(r"^https?://.+", re.IGNORECASE)


def _validate_sources_file(*, preset_id: str, path: Path) -> ValidationReport:
    """sources.json shape check — Phase 15-9.

    Required keys: preset_id, source_project, seeds, pretendard_font_license,
    created_at. Each seed entry must have url/kind/title.
    """

    report = ValidationReport()
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        report.errors.append(f"[{preset_id}] sources.json parse error: {exc}")
        return report

    if not isinstance(data, dict):
        report.errors.append(f"[{preset_id}] sources.json must be a JSON object")
        return report

    for field_name in ("preset_id", "source_project", "seeds", "pretendard_font_license", "created_at"):
        if field_name not in data:
            report.errors.append(f"[{preset_id}] sources.json missing field: {field_name}")

    if data.get("preset_id") and data["preset_id"] != preset_id:
        report.errors.append(
            f"[{preset_id}] sources.json.preset_id '{data['preset_id']}' != directory name"
        )

    seeds = data.get("seeds")
    if seeds is None:
        return report
    if not isinstance(seeds, list):
        report.errors.append(f"[{preset_id}] sources.json.seeds must be an array")
        return report

    for idx, seed in enumerate(seeds):
        if not isinstance(seed, dict):
            report.errors.append(f"[{preset_id}] sources.json.seeds[{idx}] must be an object")
            continue
        for key in ("url", "kind", "title"):
            if key not in seed or not seed.get(key):
                report.errors.append(
                    f"[{preset_id}] sources.json.seeds[{idx}] missing field: {key}"
                )
        url = seed.get("url", "")
        if isinstance(url, str) and url and not _SOURCES_URL_RE.match(url):
            report.errors.append(
                f"[{preset_id}] sources.json.seeds[{idx}].url '{url}' must start with http(s)://"
            )

    return report


def _validate_matrix_consistency(*, matrix: dict, preset_dirs: list[Path]) -> ValidationReport:
    report = ValidationReport()
    matrix_ids = {entry["id"] for entry in matrix.get("presets", [])}
    disk_ids = {p.name for p in preset_dirs if ID_RE.match(p.name)}
    only_in_matrix = matrix_ids - disk_ids
    only_on_disk = disk_ids - matrix_ids
    for pid in sorted(only_in_matrix):
        report.errors.append(f"matrix.json lists '{pid}' but presets/{pid}/ does not exist")
    for pid in sorted(only_on_disk):
        report.errors.append(f"presets/{pid}/ exists but matrix.json does not list it")
    return report


def format_report(report: ValidationReport) -> str:
    lines = [f"Checked {len(report.checked_presets)} preset(s)."]
    if report.errors:
        lines.append(f"\nErrors ({len(report.errors)}):")
        for err in report.errors:
            lines.append(f"  - {err}")
    if report.warnings:
        lines.append(f"\nWarnings ({len(report.warnings)}):")
        for warn in report.warnings:
            lines.append(f"  - {warn}")
    if report.ok and not report.warnings:
        lines.append("\nAll checks passed.")
    elif report.ok:
        lines.append("\nNo errors (warnings above).")
    return "\n".join(lines)
