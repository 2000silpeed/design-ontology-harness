#!/usr/bin/env python3
"""Sync-time compatibility check: harness presets/ vs plugin plugin.json.

Parses `supported_preset_api` range from the plugin repo's `plugin.json`, then
verifies every harness preset's `preset_api_version` falls inside that range.
Emits a report; exits non-zero on mismatch so the sync script can block PR.

Usage:
    scripts/check-plugin-compatibility.py --plugin-repo <path> [--presets-dir <path>]
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT))

from design_ontology_harness.semver_range import (  # noqa: E402
    is_valid_range,
    is_valid_version,
    satisfies,
)


def _current_adapter_versions() -> dict[str, str]:
    try:
        from design_ontology_harness.adapters import list_adapters, get_adapter
    except Exception:  # pragma: no cover
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


def _find_plugin_manifest(plugin_repo: Path) -> Path:
    candidates = [
        plugin_repo / ".claude-plugin" / "plugin.json",
        plugin_repo / "plugin.json",
    ]
    for candidate in candidates:
        if candidate.exists():
            return candidate
    raise FileNotFoundError(
        f"plugin.json not found. Looked in: {', '.join(str(c) for c in candidates)}"
    )


def check(plugin_repo: Path, presets_dir: Path) -> tuple[int, list[str]]:
    messages: list[str] = []
    plugin_manifest_path = _find_plugin_manifest(plugin_repo)
    plugin_manifest = json.loads(plugin_manifest_path.read_text(encoding="utf-8"))
    supported = plugin_manifest.get("supported_preset_api")
    if not supported:
        return 2, [f"plugin.json missing 'supported_preset_api' field at {plugin_manifest_path}"]
    if not is_valid_range(supported):
        return 2, [f"plugin.json.supported_preset_api '{supported}' is not a valid range"]
    messages.append(f"plugin.json supported_preset_api = {supported}")

    compat_path = presets_dir / "compatibility.json"
    if not compat_path.exists():
        return 2, [f"{compat_path} not found"]
    compat = json.loads(compat_path.read_text(encoding="utf-8"))
    harness_range = compat.get("supported_preset_api_range", "")
    messages.append(f"harness supported_preset_api_range = {harness_range}")

    violations: list[str] = []
    adapter_drift: list[str] = []

    # Check harness's own current version against plugin supported range.
    current = compat.get("current_preset_api_version")
    if current and is_valid_version(current) and not satisfies(current, supported):
        violations.append(
            f"harness current_preset_api_version={current} outside plugin supported_preset_api={supported}"
        )

    adapter_versions = _current_adapter_versions()

    # Check every preset's preset_api_version + adapter_compatibility ranges.
    preset_count = 0
    for preset_dir in sorted(presets_dir.iterdir()):
        if not preset_dir.is_dir() or preset_dir.name.startswith("."):
            continue
        manifest_path = preset_dir / "manifest.json"
        if not manifest_path.exists():
            continue
        preset_count += 1
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        api_v = manifest.get("preset_api_version", "")
        if not is_valid_version(api_v):
            violations.append(f"[{preset_dir.name}] invalid preset_api_version: '{api_v}'")
            continue
        if not satisfies(api_v, supported):
            violations.append(
                f"[{preset_dir.name}] preset_api_version={api_v} outside plugin supported={supported}"
            )

        adapter_compat = manifest.get("adapter_compatibility") or {}
        if isinstance(adapter_compat, dict):
            for adapter_id, range_expr in adapter_compat.items():
                if not (isinstance(range_expr, str) and is_valid_range(range_expr)):
                    continue
                current_ver = adapter_versions.get(adapter_id)
                if current_ver and not satisfies(current_ver, range_expr):
                    adapter_drift.append(
                        f"[{preset_dir.name}] adapter '{adapter_id}' "
                        f"current={current_ver} outside range {range_expr}"
                    )

    messages.append(f"checked {preset_count} preset manifest(s)")
    if adapter_versions:
        ver_summary = ", ".join(f"{a}@{v}" for a, v in sorted(adapter_versions.items()))
        messages.append(f"adapter versions: {ver_summary}")

    messages.append("")
    messages.append("Adapter drift:")
    if adapter_drift:
        messages.extend(f"  - {item}" for item in adapter_drift)
    else:
        messages.append("  (none — every preset range covers the current adapter version)")

    if violations or adapter_drift:
        messages.append("")
        total = len(violations) + len(adapter_drift)
        messages.append(f"VIOLATIONS ({total}):")
        messages.extend(f"  - {v}" for v in violations)
        messages.extend(f"  - {v}" for v in adapter_drift)
        return 1, messages

    messages.append("")
    messages.append("compatibility OK")
    return 0, messages


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--plugin-repo", required=True, help="Path to design-ontology-plugin repo")
    parser.add_argument(
        "--presets-dir",
        default=str(REPO_ROOT / "presets"),
        help="Path to harness presets/ directory",
    )
    args = parser.parse_args()

    plugin_repo = Path(args.plugin_repo).resolve()
    presets_dir = Path(args.presets_dir).resolve()

    if not plugin_repo.is_dir():
        print(f"error: plugin-repo not a directory: {plugin_repo}", file=sys.stderr)
        return 2
    if not presets_dir.is_dir():
        print(f"error: presets-dir not a directory: {presets_dir}", file=sys.stderr)
        return 2

    exit_code, messages = check(plugin_repo, presets_dir)
    for line in messages:
        print(line)
    return exit_code


if __name__ == "__main__":
    sys.exit(main())
