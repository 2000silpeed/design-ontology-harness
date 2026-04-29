"""Phase 11-5: preset matcher smoke tests.

Targets top-1 accuracy ≥ 80% on 10 natural-language queries against the P0
catalog. The dataset is intentionally small and hand-picked so a regression
in `keywords.json` or `engine.py` surfaces immediately.
"""

from __future__ import annotations

import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from design_ontology_harness.preset_matcher.engine import (
    MatchQuery,
    extract_axes_from_text,
    match_presets,
)
from design_ontology_harness.preset_matcher.eval import (
    LABELED_CASES,
    run_eval,
)


@pytest.mark.parametrize("query_kwargs,expected_id", LABELED_CASES)
def test_top_1_for_each_case(query_kwargs: dict, expected_id: str):
    query = MatchQuery(**query_kwargs)
    results = match_presets(query, top_k=3)
    assert results, f"no results for {query_kwargs}"
    top = results[0]
    assert top.preset_id == expected_id, (
        f"expected top-1={expected_id} for {query_kwargs}, got {top.preset_id} "
        f"(score={top.raw_score}, rationale={top.rationale})"
    )


def test_top_1_accuracy_threshold():
    hits = 0
    misses: list[tuple[dict, str, str]] = []
    for query_kwargs, expected_id in LABELED_CASES:
        results = match_presets(MatchQuery(**query_kwargs), top_k=1)
        got = results[0].preset_id if results else "<none>"
        if got == expected_id:
            hits += 1
        else:
            misses.append((query_kwargs, expected_id, got))
    accuracy = hits / len(LABELED_CASES)
    assert accuracy >= 0.85, (
        f"top-1 accuracy {accuracy:.0%} below 85% target. Misses: {misses}"
    )


def test_bucket_is_high_only_with_clear_gap():
    query = MatchQuery(app_mode="dashboard", brand_tone="minimal-tech", tags=["ko", "saas"])
    results = match_presets(query, top_k=3)
    assert results[0].preset_id == "dashboard--minimal-tech"
    assert results[0].bucket == "High"
    # Runner-up must not also be High.
    assert results[1].bucket != "High"


def test_bucket_never_uses_decimal_strings():
    query = MatchQuery(free_text="관리자 대시보드")
    for result in match_presets(query, top_k=3):
        assert result.bucket in {"High", "Medium", "Low"}, (
            f"bucket must be one of High/Medium/Low, got {result.bucket!r}"
        )


def test_fallback_when_only_low_matches():
    # Specify an axis combo that does not exist in the P0 catalog.
    query = MatchQuery(app_mode="canvas-tool", brand_tone="playful-soft")
    results = match_presets(query, top_k=3)
    assert results, "matcher must still return the closest alternatives"
    assert all(r.bucket == "Low" for r in results), (
        f"expected all-Low fallback for a mismatched axis combo, got "
        f"{[(r.preset_id, r.bucket) for r in results]}"
    )


def test_unique_app_mode_infers_brand_tone_for_demo_query():
    query = MatchQuery(
        free_text="SRE observability dashboard, Grafana/Datadog style, dense tables, dark default, alert feed"
    )
    results = match_presets(query, top_k=3)

    assert results[0].preset_id == "monitoring-ops--minimal-tech"
    assert results[0].bucket == "High"
    assert results[0].missing_signals == []


def test_color_mode_filter_zeroes_unsupported():
    # commerce--editorial-warm is light-only; asking for dark should zero its score.
    query = MatchQuery(
        app_mode="commerce",
        brand_tone="editorial-warm",
        color_mode="dark",
        tags=["fashion"],
    )
    # top_k=10 keeps commerce--editorial-warm visible now that commerce--playful-soft
    # (light+dark) outranks it via partial brand_tone mismatch score (0.5) instead of 0.
    results = match_presets(query, top_k=10)
    commerce = next((r for r in results if r.preset_id == "commerce--editorial-warm"), None)
    assert commerce is not None
    assert commerce.raw_score == 0.0, (
        f"commerce--editorial-warm should score 0 when dark requested, got {commerce.raw_score}"
    )


def test_explicit_fields_override_free_text():
    # Free text says dashboard; explicit app_mode says commerce. Explicit wins.
    query = MatchQuery(
        app_mode="commerce",
        brand_tone="editorial-warm",
        free_text="대시보드 minimal",
    )
    results = match_presets(query, top_k=3)
    assert results[0].preset_id == "commerce--editorial-warm"


def test_extract_axes_from_text_basic():
    axes = extract_axes_from_text("한국어 SaaS 대시보드, 미니멀 테크")
    assert axes["app_mode"] == "dashboard"
    assert axes["brand_tone"] == "minimal-tech"
    assert "ko" in axes["tags"]
    assert "saas" in axes["tags"]


def test_extract_axes_english():
    axes = extract_axes_from_text("AI copilot chat, dark preferred")
    assert axes["app_mode"] == "conversation-copilot"
    assert axes["color_mode"] == "dark"
    assert "ai" in axes["tags"]


def test_run_eval_meets_threshold():
    result = run_eval()
    assert result.total == len(LABELED_CASES) == 66
    assert result.accuracy >= 0.85, (
        f"run_eval accuracy {result.accuracy:.2f} < 0.85. "
        f"Misses: {[(m[1], m[2]) for m in result.misses]}"
    )
    # confusion_pairs must exclude correct predictions and be sorted desc.
    pairs = result.confusion_pairs(top_k=5)
    for expected, predicted, _count in pairs:
        assert expected != predicted
    counts = [count for _, _, count in pairs]
    assert counts == sorted(counts, reverse=True)
