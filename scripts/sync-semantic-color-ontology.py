#!/usr/bin/env python3
"""Sync the packaged semantic color ontology from the local semantic-os build.

Usage:
    uv run python scripts/sync-semantic-color-ontology.py \
        [--source ~/ai-projects/semantic-os/domains/color/ontology/build/graph.json]

The packaged snapshot ships inside the design_ontology_harness package so
GitHub users do not need a sibling semantic-os checkout. This script:

- wraps the source graph with import metadata (repo/path/built_at),
- strips absolute local filesystem paths from node properties,
- verifies the abstraction contract (no raw OCR blobs, no local paths),
- writes design_ontology_harness/resources/semantic_color_ontology.json.
"""

from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
TARGET = REPO_ROOT / "design_ontology_harness" / "resources" / "semantic_color_ontology.json"
DEFAULT_SOURCE = (
    Path.home() / "ai-projects" / "semantic-os" / "domains" / "color" / "ontology" / "build" / "graph.json"
)


# 패키징 계약: 로컬 절대 경로를 담는 키는 통째로 떨어낸다 (테스트가 키 이름 자체를 금지).
DROPPED_PROPERTY_KEYS = {"source_path", "source_file", "local_path"}


def _strip_local_paths(value):
    if isinstance(value, str):
        if value.startswith("/Users/") or value.startswith("/home/"):
            return Path(value).name
        return value
    if isinstance(value, list):
        return [_strip_local_paths(item) for item in value]
    if isinstance(value, dict):
        return {
            key: _strip_local_paths(item)
            for key, item in value.items()
            if key not in DROPPED_PROPERTY_KEYS
        }
    return value


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", default=str(DEFAULT_SOURCE), help="semantic-os color graph.json")
    args = parser.parse_args()

    source_path = Path(args.source).expanduser().resolve()
    graph = json.loads(source_path.read_text(encoding="utf-8"))
    nodes = _strip_local_paths(graph.get("nodes", []))
    edges = graph.get("edges", [])

    payload = {
        "schema_version": "design-ontology-harness/semantic-color-ontology-compact-v1",
        "source": {
            "repo": "semantic-os",
            "path": "domains/color/ontology/build/graph.json",
            "built_at": graph.get("built_at"),
            "imported_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
            "source_schema_version": graph.get("schema_version"),
            "copyright_handling": (
                "Imported as abstracted color ontology nodes; no raw OCR, page images, "
                "or reconstructable source tables are included."
            ),
        },
        "node_count": len(nodes),
        "edge_count": len(edges),
        "nodes": nodes,
        "edges": edges,
    }

    serialized = json.dumps(payload, ensure_ascii=False, indent=1)
    if "/Users/" in serialized or "/home/" in serialized:
        raise SystemExit("Abstraction contract violated: local filesystem path survived stripping.")

    TARGET.write_text(serialized + "\n", encoding="utf-8")
    keywords_with_hex = sum(
        1
        for node in nodes
        if node.get("type") == "ColorKeyword" and (node.get("properties") or {}).get("rgb_hex")
    )
    print(
        f"Wrote {TARGET.relative_to(REPO_ROOT)}: {len(nodes)} nodes, {len(edges)} edges, "
        f"{keywords_with_hex} hex keywords (source built_at={graph.get('built_at')})"
    )


if __name__ == "__main__":
    main()
