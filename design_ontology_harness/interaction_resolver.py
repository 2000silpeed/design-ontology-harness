"""Contextual interaction-pattern selection for generated design systems.

The resolver deliberately avoids a single global visual recipe. It ranks semantic
candidates against product intent, component states, density, accessibility, and
motion budget, then chooses among equally suitable candidates. A seed can be
provided for reproducible builds; without one, the choice varies per run while
remaining bounded by the same contract and audit evidence.
"""

from __future__ import annotations

import random
from dataclasses import dataclass
from typing import Any, Mapping, Sequence


@dataclass(frozen=True)
class InteractionCandidate:
    id: str
    applies_to: tuple[str, ...]
    intents: tuple[str, ...]
    states: tuple[str, ...]
    motion_cost: int
    reduced_motion: str
    rationale: str
    advisory_reference: str | None = None


CANDIDATES: tuple[InteractionCandidate, ...] = (
    InteractionCandidate(
        "timeline-focus",
        ("living-timeline",),
        ("remember", "review", "trace", "decide"),
        ("focused", "filtered"),
        1,
        "static-indicator",
        "Use a visible chronological focus state when the user is tracing a record.",
    ),
    InteractionCandidate(
        "contextual-reveal",
        ("context-drawer", "living-timeline"),
        ("review", "understand", "compare"),
        ("focused", "open"),
        2,
        "opacity-only",
        "Reveal supporting context only when information changes, not as decoration.",
        "interaction:result-reveal",
    ),
    InteractionCandidate(
        "care-emphasis",
        ("return-ritual-prompt", "decision-stone-editor"),
        ("return", "care", "decide"),
        ("due", "committed", "attention"),
        1,
        "static-border",
        "Use restrained emphasis when a care action or decision needs attention.",
        "interaction:attention-border",
    ),
    InteractionCandidate(
        "season-transition",
        ("season-lens", "living-timeline"),
        ("orient", "remember", "review"),
        ("current", "filtered"),
        2,
        "static-or-opacity",
        "Use a low-motion transition when the temporal context changes.",
        "interaction:result-reveal",
    ),
    InteractionCandidate(
        "async-care-progress",
        ("memory-seed-composer", "return-ritual-prompt"),
        ("save", "capture", "return"),
        ("saving", "loading"),
        1,
        "static-status",
        "Use explicit progress semantics when a record is being saved or prepared.",
        "interaction:dot-progress",
    ),
)


def resolve_interaction_patterns(
    *,
    product_intent: str,
    component_states: Mapping[str, Sequence[str]],
    accessibility_targets: Sequence[str] = (),
    motion_budget: int = 2,
    density: str = "balanced",
    variation_seed: int | None = None,
    candidates: Sequence[InteractionCandidate] = CANDIDATES,
) -> dict[str, Any]:
    """Select a contextual set of interaction patterns and return audit evidence."""
    intent = product_intent.strip().lower()
    target_states = {state for states in component_states.values() for state in states}
    reduced_required = any(
        "reduced" in str(target).lower() or "motion" in str(target).lower()
        for target in accessibility_targets
    )
    scored: list[dict[str, Any]] = []
    for candidate in candidates:
        covered_components = sorted(set(candidate.applies_to) & set(component_states))
        covered_states = sorted(set(candidate.states) & target_states)
        if not covered_components or not covered_states or candidate.motion_cost > motion_budget:
            continue
        score = 0
        if any(keyword in intent for keyword in candidate.intents):
            score += 5
        score += len(covered_components) * 2 + len(covered_states)
        if reduced_required and candidate.reduced_motion.startswith("static"):
            score += 2
        if density in {"dense", "operational"} and candidate.id == "contextual-reveal":
            score -= 1
        scored.append({
            "candidate": candidate,
            "score": score,
            "covered_components": covered_components,
            "covered_states": covered_states,
        })

    if not scored:
        return {
            "schema_version": "interaction-selection/v1",
            "selection_mode": "no-compatible-candidate",
            "product_intent": product_intent,
            "selected": [],
            "candidates_considered": [],
            "constraints": _constraints(accessibility_targets, motion_budget, density),
        }

    highest = max(item["score"] for item in scored)
    finalists = [item for item in scored if item["score"] >= highest - 1]
    rng = random.Random(variation_seed) if variation_seed is not None else random.SystemRandom()
    rng.shuffle(finalists)
    selected = finalists[: min(2, len(finalists))]
    selected_ids = {item["candidate"].id for item in selected}

    return {
        "schema_version": "interaction-selection/v1",
        "selection_mode": "contextual-variation",
        "variation_seed": variation_seed,
        "product_intent": product_intent,
        "selected": [_serialize(item) for item in selected],
        "candidates_considered": [
            _serialize(item) for item in sorted(scored, key=lambda item: (-item["score"], item["candidate"].id))
        ],
        "rejected": [
            {"id": candidate.id, "reason": _rejection_reason(candidate, component_states, target_states, motion_budget)}
            for candidate in candidates
            if candidate.id not in selected_ids and candidate.id not in {item["candidate"].id for item in scored}
        ],
        "constraints": _constraints(accessibility_targets, motion_budget, density),
    }




def _serialize(item: dict[str, Any]) -> dict[str, Any]:
    candidate: InteractionCandidate = item["candidate"]
    return {
        "id": candidate.id,
        "score": item["score"],
        "covered_components": item["covered_components"],
        "covered_states": item["covered_states"],
        "motion_cost": candidate.motion_cost,
        "reduced_motion": candidate.reduced_motion,
        "rationale": candidate.rationale,
        "advisory_reference": candidate.advisory_reference,
    }


def resolve_design_language(
    *,
    visual_keywords: Sequence[str] = (),
    interaction_keywords: Sequence[str] = (),
    composition: str = "",
    density: str = "balanced",
    variation_seed: int | None = None,
) -> dict[str, Any]:
    """Choose independent composition, surface, and typography directions."""
    words = {str(item).lower() for item in [*visual_keywords, *interaction_keywords, composition]}
    axes = {
        "composition": (
            ("timeline-field", {"timeline", "temporal", "seasonal", "chronology"}, "A continuous field keeps chronology primary."),
            ("annotated-ledger", {"annotation", "field notes", "honest"}, "Annotations keep context attached to each record."),
            ("seasonal-archive", {"seasonal", "archive", "return"}, "Seasonal framing makes return a change of context."),
        ),
        "surface": (
            ("paper-strata", {"paper", "field notes", "quiet"}, "Layered reading surfaces support reflective content."),
            ("mineral-canvas", {"mineral", "deep dusk", "topographic"}, "Mineral contrast separates memory states without card walls."),
            ("ink-trace", {"ink", "annotation", "honest"}, "Ink-like marks preserve the feeling of authored traces."),
        ),
        "typography": (
            ("field-note", {"field notes", "observant", "specific"}, "A readable note rhythm keeps context ahead of display drama."),
            ("editorial-ko", {"editorial", "temporal", "quietly vivid"}, "Editorial Korean hierarchy supports long-form reflection."),
            ("quiet-sans", {"calm", "accessible", "screen-reader"}, "A restrained sans system protects scanability and access."),
        ),
    }
    rng = random.Random(variation_seed) if variation_seed is not None else random.SystemRandom()
    selected: dict[str, dict[str, Any]] = {}
    for axis, options in axes.items():
        ranked = []
        for option_id, signals, rationale in options:
            score = len(signals & words)
            if axis == "composition" and density == "spacious":
                score += 1 if option_id != "annotated-ledger" else 0
            ranked.append((score, option_id, rationale))
        top_score = max(item[0] for item in ranked)
        finalists = [item for item in ranked if item[0] == top_score]
        selected_score, option_id, rationale = rng.choice(finalists)
        selected[axis] = {"id": option_id, "score": selected_score, "rationale": rationale}
    return {
        "schema_version": "design-language-selection/v1",
        "selection_mode": "axis-wise-contextual-variation",
        "variation_seed": variation_seed,
        "selected": selected,
        "constraints": {"density": density, "source_policy": "product-profile-first"},
    }


def _constraints(targets: Sequence[str], motion_budget: int, density: str) -> dict[str, Any]:
    return {
        "accessibility_targets": list(targets),
        "motion_budget": motion_budget,
        "density": density,
        "reference_policy": "advisory-only",
    }


def _rejection_reason(
    candidate: InteractionCandidate,
    component_states: Mapping[str, Sequence[str]],
    target_states: set[str],
    motion_budget: int,
) -> str:
    if not set(candidate.applies_to) & set(component_states):
        return "no-component-match"
    if not set(candidate.states) & target_states:
        return "no-state-match"
    if candidate.motion_cost > motion_budget:
        return "motion-budget"
    return "lower-context-score"
