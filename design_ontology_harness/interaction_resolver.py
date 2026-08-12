"""Contextual interaction-pattern selection for generated design systems.

The resolver deliberately avoids a single global visual recipe. It ranks semantic
candidates against product intent, component states, density, accessibility, and
motion budget, then chooses among equally suitable candidates. A seed can be
provided for reproducible builds; without one, the choice varies per run while
remaining bounded by the same contract and audit evidence.
"""

from __future__ import annotations

import random
import re
from dataclasses import dataclass
from typing import Any, Mapping, Sequence

from .motion_reference import (
    INTERACTION_AXES,
    INTERACTION_ROLES,
    load_candidate_patterns,
)


@dataclass(frozen=True)
class InteractionCandidate:
    id: str
    axis: str
    roles: tuple[str, ...]
    intents: tuple[str, ...]
    states: tuple[str, ...]
    motion_cost: int
    reduced_motion: str
    rationale: str
    pack_id: str
    duration_ms: int
    easing: str
    motion_kind: str
    guardrails: tuple[str, ...] = ()
    license_status: tuple[str, ...] = ()


#: Component-name substrings that imply an interaction role. Matching is
#: substring-based and ordered, mirroring how component slots are classified
#: elsewhere in the harness.
ROLE_NAME_PATTERNS: tuple[tuple[str, str], ...] = (
    ("timeline", "list-surface"),
    ("feed", "list-surface"),
    ("list", "list-surface"),
    ("table", "list-surface"),
    ("grid", "list-surface"),
    ("inbox", "list-surface"),
    ("results", "list-surface"),
    ("drawer", "detail-panel"),
    ("sheet", "detail-panel"),
    ("modal", "detail-panel"),
    ("dialog", "detail-panel"),
    ("detail", "detail-panel"),
    ("inspector", "detail-panel"),
    ("panel", "detail-panel"),
    ("composer", "async-action"),
    ("editor", "async-action"),
    ("upload", "async-action"),
    ("form", "async-action"),
    ("prompt", "async-action"),
    ("submit", "async-action"),
    ("status", "status-region"),
    ("toast", "status-region"),
    ("alert", "status-region"),
    ("badge", "status-region"),
    ("notification", "status-region"),
    ("nav", "navigation-surface"),
    ("tab", "navigation-surface"),
    ("filter", "navigation-surface"),
    ("lens", "navigation-surface"),
    ("switcher", "navigation-surface"),
    ("hero", "showcase-surface"),
    ("showcase", "showcase-surface"),
    ("landing", "showcase-surface"),
    ("card", "selection-target"),
    ("item", "selection-target"),
    ("row", "selection-target"),
    ("entry", "selection-target"),
    ("option", "selection-target"),
    ("stone", "selection-target"),
)

#: Fallback when a component name carries no role signal at all.
DEFAULT_ROLE = "list-surface"

_STATE_PREFIX_RE = re.compile(r"^state:")

#: Projects name the same underlying state differently ("saving" / "processing"
#: / "agent-working"). Candidates are written against the canonical name, so
#: both sides are normalised before they are compared.
STATE_SYNONYMS: dict[str, str] = {
    "saving": "loading",
    "busy": "loading",
    "processing": "loading",
    "refreshing": "loading",
    "data-refreshing": "loading",
    "agent-working": "loading",
    "pending": "loading",
    "result-ready": "content-enter",
    "loaded": "content-enter",
    "returned": "content-enter",
    "ready": "content-enter",
    "attention-required": "attention",
    "due": "attention",
    "error": "attention",
    "warning": "attention",
    "committed": "selected",
    "active": "selected",
    "checked": "selected",
    "expanded": "open",
    "opened": "open",
}


def infer_component_role(name: str) -> str:
    """Map a project-specific component name onto a shared interaction role."""
    low = str(name).lower()
    for needle, role in ROLE_NAME_PATTERNS:
        if needle in low:
            return role
    return DEFAULT_ROLE


def _normalize_state(state: str) -> str:
    raw = _STATE_PREFIX_RE.sub("", str(state).strip().lower())
    return STATE_SYNONYMS.get(raw, raw)


def _motion_cost(duration_ms: int, kind: str) -> int:
    """Score how much attention a pattern spends, on the resolver's 0-3 scale."""
    if kind == "loop":
        return 2
    if duration_ms <= 80:
        return 0
    if duration_ms <= 180:
        return 1
    return 2


def load_candidates() -> tuple[InteractionCandidate, ...]:
    """Build the selectable candidate pool from the reference packs."""
    candidates: list[InteractionCandidate] = []
    for pattern in load_candidate_patterns():
        motion = pattern.get("motion") or {}
        kind = motion.get("kind", "transition")
        duration = int(motion.get("duration_ms", 0))
        candidates.append(
            InteractionCandidate(
                id=pattern["id"],
                axis=pattern["axis"],
                roles=tuple(pattern.get("applies_to_roles") or ()),
                intents=tuple(pattern.get("intents") or ()),
                states=tuple(
                    _normalize_state(state) for state in pattern.get("component_states") or ()
                ),
                motion_cost=_motion_cost(duration, kind),
                reduced_motion=str(motion.get("reduced_motion", "static")),
                rationale=str(pattern.get("rationale") or pattern.get("label") or pattern["id"]),
                pack_id=str(pattern.get("pack_id", "")),
                duration_ms=duration,
                easing=str(motion.get("easing", "standard")),
                motion_kind=kind,
                guardrails=tuple(pattern.get("guardrails") or ()),
                license_status=tuple(pattern.get("license_status") or ()),
            )
        )
    return tuple(candidates)


CANDIDATES: tuple[InteractionCandidate, ...] = load_candidates()


def resolve_interaction_patterns(
    *,
    product_intent: str,
    component_states: Mapping[str, Sequence[str]],
    accessibility_targets: Sequence[str] = (),
    motion_budget: int = 2,
    density: str = "balanced",
    variation_seed: int | None = None,
    candidates: Sequence[InteractionCandidate] = CANDIDATES,
    preference_prior: Mapping[str, float] | None = None,
) -> dict[str, Any]:
    """Select a contextual set of interaction patterns and return audit evidence."""
    intent = product_intent.strip().lower()
    target_states = {
        _normalize_state(state) for states in component_states.values() for state in states
    }
    component_roles = {
        str(name): infer_component_role(name) for name in component_states
    }
    present_roles = set(component_roles.values())
    reduced_required = any(
        "reduced" in str(target).lower() or "motion" in str(target).lower()
        for target in accessibility_targets
    )
    dense = density in {"dense", "operational", "compact"}

    scored: list[dict[str, Any]] = []
    for candidate in candidates:
        covered_roles = sorted(set(candidate.roles) & present_roles)
        covered_states = sorted(set(candidate.states) & target_states)
        if not covered_roles or candidate.motion_cost > motion_budget:
            continue
        # Progress affordances are only meaningful when the product actually
        # reports an async state. Elsewhere a state match strengthens a
        # candidate but is not a precondition, since state vocabularies differ
        # per project far more than roles do.
        if candidate.axis == "progress" and not covered_states:
            continue
        covered_components = sorted(
            name for name, role in component_roles.items() if role in set(covered_roles)
        )
        score = 0
        if any(keyword in intent for keyword in candidate.intents):
            score += 5
        score += len(covered_roles) * 2 + len(covered_states)
        if reduced_required and candidate.reduced_motion in {"static", "skip"}:
            score += 2
        # Dense operational surfaces pay a real attention cost for movement.
        if dense:
            score += 2 - candidate.motion_cost
        scored.append({
            "candidate": candidate,
            "score": score,
            "covered_roles": covered_roles,
            "covered_components": covered_components,
            "covered_states": covered_states,
        })

    if not scored:
        return {
            "schema_version": "interaction-selection/v2",
            "selection_mode": "no-compatible-candidate",
            "product_intent": product_intent,
            "component_roles": component_roles,
            "selected": [],
            "candidates_considered": [],
            "rejected": [
                {
                    "id": candidate.id,
                    "reason": _rejection_reason(
                        candidate, present_roles, target_states, motion_budget
                    ),
                }
                for candidate in candidates
            ],
            "constraints": _constraints(accessibility_targets, motion_budget, density),
        }

    rng = random.Random(variation_seed) if variation_seed is not None else random.SystemRandom()

    # One pattern per axis at most. This is what makes "one primary motion plus
    # subordinate response" a structural property of the selection rather than a
    # note in a guideline nobody reads.
    selected: list[dict[str, Any]] = []
    for axis in INTERACTION_AXES:
        in_axis = [item for item in scored if item["candidate"].axis == axis]
        if not in_axis:
            continue
        highest = max(item["score"] for item in in_axis)
        finalists = [item for item in in_axis if item["score"] >= highest - 1]
        prior = preference_prior or {}
        if prior:
            # A recorded outcome breaks ties before chance does, so good choices
            # accumulate instead of being re-rolled every run.
            best_prior = max(
                (float(prior.get(item["candidate"].id, 0.0)) for item in finalists),
                default=0.0,
            )
            if best_prior > 0:
                finalists = [
                    item
                    for item in finalists
                    if float(prior.get(item["candidate"].id, 0.0)) >= best_prior
                ]
        selected.append(rng.choice(finalists))

    selected_ids = {item["candidate"].id for item in selected}
    considered_ids = {item["candidate"].id for item in scored}

    return {
        "schema_version": "interaction-selection/v2",
        "selection_mode": "contextual-variation",
        "variation_seed": variation_seed,
        "product_intent": product_intent,
        "component_roles": component_roles,
        "selected": [_serialize(item) for item in selected],
        "candidates_considered": [
            _serialize(item)
            for item in sorted(scored, key=lambda item: (-item["score"], item["candidate"].id))
        ],
        "rejected": [
            {
                "id": candidate.id,
                "reason": _rejection_reason(
                    candidate, present_roles, target_states, motion_budget
                ),
            }
            for candidate in candidates
            if candidate.id not in selected_ids and candidate.id not in considered_ids
        ],
        "constraints": _constraints(accessibility_targets, motion_budget, density),
    }




def _serialize(item: dict[str, Any]) -> dict[str, Any]:
    candidate: InteractionCandidate = item["candidate"]
    return {
        "id": candidate.id,
        "axis": candidate.axis,
        "score": item["score"],
        "covered_roles": item["covered_roles"],
        "covered_components": item["covered_components"],
        "covered_states": item["covered_states"],
        "motion_cost": candidate.motion_cost,
        "motion_kind": candidate.motion_kind,
        "duration_ms": candidate.duration_ms,
        "easing": candidate.easing,
        "reduced_motion": candidate.reduced_motion,
        "rationale": candidate.rationale,
        "guardrails": list(candidate.guardrails),
        "pack_id": candidate.pack_id,
        "license_status": list(candidate.license_status),
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
    present_roles: set[str],
    target_states: set[str],
    motion_budget: int,
) -> str:
    if not set(candidate.roles) & present_roles:
        return "no-role-match"
    if not set(candidate.states) & target_states:
        return "no-state-match"
    if candidate.motion_cost > motion_budget:
        return "motion-budget"
    return "lower-context-score"
