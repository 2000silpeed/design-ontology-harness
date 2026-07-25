#!/usr/bin/env python3
"""Backward-compatible Semantic OS color migration wrapper.

The canonical command is now ``design-ontology sync-semantic-colors``. This
wrapper updates both the packaged transport snapshot and the embedded ontology
inside ``docs/color-reference.md``.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from design_ontology_harness.semantic_color_markdown import (
    DEFAULT_COLOR_REFERENCE_PATH,
    DEFAULT_ONTOLOGY_SNAPSHOT_PATH,
    DEFAULT_SEMANTIC_OS_SOURCE,
    sync_semantic_colors,
)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", default=str(DEFAULT_SEMANTIC_OS_SOURCE))
    parser.add_argument("--target", default=str(DEFAULT_COLOR_REFERENCE_PATH))
    parser.add_argument("--ontology-output", default=str(DEFAULT_ONTOLOGY_SNAPSHOT_PATH))
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()

    result = sync_semantic_colors(
        source_path=Path(args.source),
        color_reference_output=Path(args.target),
        ontology_output=Path(args.ontology_output) if args.ontology_output else None,
        check=args.check,
    )
    print(json.dumps(result, ensure_ascii=False, indent=2))
    if args.check and not result["ok"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
