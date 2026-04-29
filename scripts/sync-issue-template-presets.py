#!/usr/bin/env python3
"""Sync plugin preset-feedback dropdown options from presets/matrix.json."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parent.parent


def load_preset_ids(presets_dir: Path) -> list[str]:
    matrix_path = presets_dir / "matrix.json"
    matrix = json.loads(matrix_path.read_text(encoding="utf-8"))
    return [entry["id"] for entry in matrix.get("presets", [])]


def render_options(preset_ids: list[str]) -> str:
    lines = ["      options:"]
    lines.extend(f"        - {preset_id}" for preset_id in preset_ids)
    lines.append("        - other (specify in body)")
    return "\n".join(lines) + "\n"


def sync_template(template_path: Path, preset_ids: list[str], *, write: bool) -> bool:
    text = template_path.read_text(encoding="utf-8")
    description = (
        f"      description: 카탈로그 {len(preset_ids)}종 중에서 선택하세요. "
        '목록은 `presets/matrix.json` 기준입니다.'
    )
    text = re.sub(
        r"      description: 카탈로그 \d+종 중에서 선택하세요\..*",
        description,
        text,
    )

    pattern = re.compile(r"      options:\n(?:        - .+\n)+(?=    validations:)", re.MULTILINE)
    updated, count = pattern.subn(render_options(preset_ids), text, count=1)
    if count != 1:
        raise ValueError(f"could not find preset_id options block in {template_path}")

    changed = updated != template_path.read_text(encoding="utf-8")
    if changed and write:
        template_path.write_text(updated, encoding="utf-8")
    return changed


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--plugin-repo",
        type=Path,
        default=REPO_ROOT.parent / "design-ontology-plugin",
        help="Path to design-ontology-plugin (default: sibling directory)",
    )
    parser.add_argument(
        "--presets-dir",
        type=Path,
        default=REPO_ROOT / "presets",
        help="Path to harness presets directory",
    )
    parser.add_argument(
        "--check",
        action="store_true",
        help="Exit 1 if the template would change",
    )
    args = parser.parse_args()

    template_path = args.plugin_repo / ".github" / "ISSUE_TEMPLATE" / "preset-feedback.yml"
    if not template_path.exists():
        print(f"missing template: {template_path}", file=sys.stderr)
        return 2

    preset_ids = load_preset_ids(args.presets_dir)
    changed = sync_template(template_path, preset_ids, write=not args.check)
    if args.check and changed:
        print(f"preset-feedback.yml is out of sync with {args.presets_dir / 'matrix.json'}")
        return 1

    action = "would update" if args.check and changed else "updated" if changed else "already synced"
    print(f"[sync-issue-template-presets] {action}: {len(preset_ids)} presets")
    return 0


if __name__ == "__main__":
    sys.exit(main())
