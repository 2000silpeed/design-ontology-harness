#!/usr/bin/env python3
"""check-version-consistency.py — Phase 13-11-C-4 launch checklist item 5.

Verifies three-way version consistency between:

  - design-ontology-plugin/.claude-plugin/plugin.json       (canonical plugin version)
  - design-ontology-plugin/.claude-plugin/marketplace.json  (marketplace entry)
  - design-ontology-plugin/CHANGELOG.md                     (top-most release header)

Exit code:
  0 — all three versions match (including CHANGELOG top header after `## Unreleased`).
  1 — drift detected (prints each mismatch).
  2 — file missing or parse error.

Stdlib only. Intended for pre-tag manual run and CI gate before `gh release create`.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path


def _fail(msg: str) -> int:
    print(f"[check-version-consistency] ERROR: {msg}", file=sys.stderr)
    return 2


def _extract_latest_changelog_version(text: str) -> str | None:
    """Return the first version header after `## Unreleased` (if present)."""

    lines = text.splitlines()
    seen_unreleased = False
    for line in lines:
        stripped = line.strip()
        if stripped.lower().startswith("## unreleased"):
            seen_unreleased = True
            continue
        if stripped.startswith("## ") and (seen_unreleased or not seen_unreleased):
            # Match `## v0.1.0 — 2026-04-20` / `## 0.1.0 - ...`
            m = re.match(r"^##\s+v?(\d+\.\d+\.\d+)", stripped)
            if m:
                return m.group(1)
    return None


def check(plugin_repo: Path) -> int:
    plugin_json = plugin_repo / ".claude-plugin" / "plugin.json"
    marketplace_json = plugin_repo / ".claude-plugin" / "marketplace.json"
    changelog = plugin_repo / "CHANGELOG.md"

    for p in (plugin_json, marketplace_json, changelog):
        if not p.exists():
            return _fail(f"missing file: {p}")

    try:
        plugin_version = json.loads(plugin_json.read_text(encoding="utf-8"))["version"]
    except (json.JSONDecodeError, KeyError) as exc:
        return _fail(f"plugin.json parse: {exc}")

    try:
        marketplace_version = json.loads(marketplace_json.read_text(encoding="utf-8"))["version"]
    except (json.JSONDecodeError, KeyError) as exc:
        return _fail(f"marketplace.json parse: {exc}")

    changelog_version = _extract_latest_changelog_version(
        changelog.read_text(encoding="utf-8")
    )
    if changelog_version is None:
        return _fail("CHANGELOG.md has no `## vX.Y.Z` header after Unreleased")

    print(f"  plugin.json.version      = {plugin_version}")
    print(f"  marketplace.json.version = {marketplace_version}")
    print(f"  CHANGELOG latest release = {changelog_version}")

    drift = []
    if plugin_version != marketplace_version:
        drift.append(
            f"plugin.json ({plugin_version}) != marketplace.json ({marketplace_version})"
        )
    if plugin_version != changelog_version:
        drift.append(
            f"plugin.json ({plugin_version}) != CHANGELOG top ({changelog_version})"
        )

    if drift:
        print("\n[check-version-consistency] DRIFT:", file=sys.stderr)
        for d in drift:
            print(f"  - {d}", file=sys.stderr)
        return 1

    print(f"\n[check-version-consistency] OK — three-way match on {plugin_version}")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument(
        "--plugin-repo",
        type=Path,
        default=Path(__file__).resolve().parent.parent.parent / "design-ontology-plugin",
        help="Path to the design-ontology-plugin repo (default: sibling directory)",
    )
    args = parser.parse_args()
    return check(args.plugin_repo)


if __name__ == "__main__":
    sys.exit(main())
