"""Record how selected interaction patterns actually scored, and feed it back.

Without this, selection is a fresh coin flip every run: the resolver varies
among tied candidates but never learns which of them produced a surface that
reviewed well. Recording the outcome turns variation into search — the pool
stays divergent, but evidence, not chance, breaks the tie.

The registry is deliberately small and additive. It stores a per-pattern rolling
score, never a verdict, and it only influences candidates the resolver already
considers equally suitable.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Iterable

from .utils import write_json

REGISTRY_SCHEMA_VERSION = "interaction-outcomes/v1"
DEFAULT_REGISTRY_RELATIVE_PATH = Path("registry") / "interaction_outcomes.json"


def default_registry_path(repo_root: Path) -> Path:
    return repo_root / DEFAULT_REGISTRY_RELATIVE_PATH


def load_outcomes(registry_path: Path) -> dict[str, Any]:
    if not registry_path.is_file():
        return {"schema_version": REGISTRY_SCHEMA_VERSION, "patterns": {}}
    try:
        data = json.loads(registry_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise ValueError(f"Interaction outcome registry is unreadable: {registry_path}") from exc
    if not isinstance(data, dict) or not isinstance(data.get("patterns"), dict):
        raise ValueError(f"Interaction outcome registry is malformed: {registry_path}")
    return data


def record_outcome(
    registry_path: Path,
    *,
    project: str,
    pattern_ids: Iterable[str],
    score: float,
    note: str | None = None,
) -> dict[str, Any]:
    """Attach a review score to the patterns a project shipped."""

    if not 0.0 <= float(score) <= 1.0:
        raise ValueError("Interaction outcome score must be between 0 and 1")

    registry = load_outcomes(registry_path)
    patterns: dict[str, Any] = registry["patterns"]

    for pattern_id in pattern_ids:
        entry = patterns.setdefault(
            str(pattern_id),
            {"observations": 0, "mean_score": 0.0, "projects": []},
        )
        observations = int(entry.get("observations", 0))
        mean = float(entry.get("mean_score", 0.0))
        entry["mean_score"] = round((mean * observations + float(score)) / (observations + 1), 4)
        entry["observations"] = observations + 1
        if project not in entry["projects"]:
            entry["projects"] = sorted({*entry["projects"], project})
        if note:
            entry["last_note"] = note

    registry["schema_version"] = REGISTRY_SCHEMA_VERSION
    registry_path.parent.mkdir(parents=True, exist_ok=True)
    write_json(registry_path, registry)
    return registry


def preference_prior(
    registry_path: Path,
    *,
    min_observations: int = 2,
) -> dict[str, float]:
    """Return per-pattern priors for the resolver's tie-break.

    A single good run is not evidence, so patterns below ``min_observations``
    are withheld. The prior only orders candidates that already tied.
    """

    try:
        registry = load_outcomes(registry_path)
    except ValueError:
        return {}

    prior: dict[str, float] = {}
    for pattern_id, entry in (registry.get("patterns") or {}).items():
        if not isinstance(entry, dict):
            continue
        if int(entry.get("observations", 0)) < min_observations:
            continue
        prior[str(pattern_id)] = float(entry.get("mean_score", 0.0))
    return prior
