"""Phase 15-5: pin every preset's manifest.content_hash to a snapshot.

When the hash drifts, the test fails with instructions on how to update the
fixture. Run with `--update-snapshots` to rewrite the fixture in place.
"""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from design_ontology_harness.preset_builder import MATRIX_PATH, PRESETS_ROOT

FIXTURE_PATH = Path(__file__).parent / "fixtures" / "preset_snapshots.json"


def _load_matrix_ids() -> list[str]:
    matrix = json.loads(MATRIX_PATH.read_text(encoding="utf-8"))
    return sorted(entry["id"] for entry in matrix.get("presets", []) if entry.get("id"))


def _current_hashes() -> dict[str, str]:
    hashes: dict[str, str] = {}
    for preset_id in _load_matrix_ids():
        manifest_path = PRESETS_ROOT / preset_id / "manifest.json"
        if not manifest_path.exists():
            continue
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        content_hash = manifest.get("content_hash")
        if content_hash:
            hashes[preset_id] = content_hash
    return hashes


def _load_snapshot() -> dict[str, str]:
    if not FIXTURE_PATH.exists():
        return {}
    try:
        data = json.loads(FIXTURE_PATH.read_text(encoding="utf-8"))
        return data if isinstance(data, dict) else {}
    except json.JSONDecodeError:
        return {}


def _write_snapshot(hashes: dict[str, str]) -> None:
    FIXTURE_PATH.parent.mkdir(parents=True, exist_ok=True)
    FIXTURE_PATH.write_text(
        json.dumps(hashes, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


def test_preset_snapshots_match(update_snapshots: bool):
    current = _current_hashes()
    if update_snapshots:
        _write_snapshot(current)
        return

    snapshot = _load_snapshot()
    if not snapshot:
        pytest.fail(
            f"snapshot fixture missing or empty: {FIXTURE_PATH}\n"
            "Run `pytest tests/test_preset_snapshots.py --update-snapshots` "
            "to seed it."
        )

    drifted = {
        pid: (snapshot.get(pid), current.get(pid))
        for pid in sorted(set(snapshot) | set(current))
        if snapshot.get(pid) != current.get(pid)
    }
    if drifted:
        details = "\n".join(
            f"  - {pid}: snapshot={old} current={new}"
            for pid, (old, new) in drifted.items()
        )
        pytest.fail(
            "preset content_hash drift detected:\n"
            f"{details}\n"
            "If this drift is intentional (preset_builder change, KB rebuild, "
            "manual edit), run:\n"
            "  pytest tests/test_preset_snapshots.py --update-snapshots\n"
            "to refresh the fixture."
        )
