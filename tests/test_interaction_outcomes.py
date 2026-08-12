from __future__ import annotations

from pathlib import Path

import pytest

from design_ontology_harness.aesthetic_loop import DEFAULT_DIMENSIONS, DEFAULT_METRICS
from design_ontology_harness.interaction_outcomes import (
    load_outcomes,
    preference_prior,
    record_outcome,
)


def test_interaction_quality_dimension_is_registered_and_weighted():
    dimensions = {item["id"]: item for item in DEFAULT_DIMENSIONS}

    assert "interaction_quality" in dimensions
    assert round(sum(item["weight"] for item in DEFAULT_DIMENSIONS), 4) == 1.0
    for metric in dimensions["interaction_quality"]["metrics"]:
        assert metric in DEFAULT_METRICS, f"{metric} has no improvement guidance"


def test_outcome_registry_averages_repeated_observations(tmp_path: Path):
    registry = tmp_path / "interaction_outcomes.json"

    record_outcome(registry, project="alpha", pattern_ids=["interaction:staged-enter"], score=0.9)
    record_outcome(registry, project="beta", pattern_ids=["interaction:staged-enter"], score=0.7)

    entry = load_outcomes(registry)["patterns"]["interaction:staged-enter"]

    assert entry["observations"] == 2
    assert entry["mean_score"] == pytest.approx(0.8)
    assert entry["projects"] == ["alpha", "beta"]


def test_prior_withholds_patterns_with_a_single_observation(tmp_path: Path):
    """One good run is not evidence."""
    registry = tmp_path / "interaction_outcomes.json"
    record_outcome(registry, project="alpha", pattern_ids=["interaction:staged-enter"], score=0.95)

    assert preference_prior(registry) == {}

    record_outcome(registry, project="beta", pattern_ids=["interaction:staged-enter"], score=0.85)

    assert preference_prior(registry) == {"interaction:staged-enter": pytest.approx(0.9)}


def test_missing_registry_yields_an_empty_prior(tmp_path: Path):
    assert preference_prior(tmp_path / "absent.json") == {}


def test_score_must_be_a_normalised_review_value(tmp_path: Path):
    with pytest.raises(ValueError):
        record_outcome(
            tmp_path / "interaction_outcomes.json",
            project="alpha",
            pattern_ids=["interaction:staged-enter"],
            score=1.4,
        )
