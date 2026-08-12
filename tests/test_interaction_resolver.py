from design_ontology_harness.interaction_resolver import (
    InteractionCandidate,
    resolve_design_language,
    resolve_interaction_patterns,
)


COMPONENT_STATES = {
    "living-timeline": ["default", "focused", "filtered"],
    "return-ritual-prompt": ["due", "completed"],
    "decision-stone-editor": ["committed", "attention"],
    "season-lens": ["current", "filtered"],
    "memory-seed-composer": ["saving", "loading"],
    "context-drawer": ["open", "closed"],
}


def test_resolver_selects_contextual_candidates_and_audit_evidence():
    result = resolve_interaction_patterns(
        product_intent="remember and return to decisions",
        component_states=COMPONENT_STATES,
        accessibility_targets=["reduced-motion", "keyboard-focus"],
        motion_budget=2,
        variation_seed=11,
    )

    assert result["schema_version"] == "interaction-selection/v2"
    assert result["selection_mode"] == "contextual-variation"
    assert result["selected"]
    assert all(item["covered_components"] for item in result["selected"])
    assert all(item["covered_roles"] for item in result["selected"])
    assert result["constraints"]["reference_policy"] == "advisory-only"


def test_at_most_one_pattern_per_axis_is_selected():
    """One primary motion plus subordinate response, enforced structurally."""
    result = resolve_interaction_patterns(
        product_intent="remember and return to decisions",
        component_states=COMPONENT_STATES,
        motion_budget=2,
        variation_seed=11,
    )

    axes = [item["axis"] for item in result["selected"]]
    assert len(axes) == len(set(axes))


def _tied_candidates() -> tuple[InteractionCandidate, ...]:
    """Two candidates that are genuinely equivalent for the same input."""
    common = {
        "axis": "enter",
        "roles": ("list-surface",),
        "intents": ("review",),
        "states": ("filtered",),
        "motion_cost": 1,
        "reduced_motion": "opacity-only",
        "pack_id": "test",
        "duration_ms": 180,
        "easing": "standard",
        "motion_kind": "transition",
    }
    return (
        InteractionCandidate(id="test:alpha", rationale="alpha", **common),
        InteractionCandidate(id="test:beta", rationale="beta", **common),
    )


def test_same_seed_is_reproducible():
    kwargs = {
        "product_intent": "review and return",
        "component_states": COMPONENT_STATES,
        "motion_budget": 2,
    }
    first = resolve_interaction_patterns(**kwargs, variation_seed=2)
    repeat = resolve_interaction_patterns(**kwargs, variation_seed=2)

    assert first["selected"] == repeat["selected"]


def test_a_clear_winner_stays_the_winner_across_seeds():
    """Variation exists to break ties, not to reroll a decided axis."""
    kwargs = {
        "product_intent": "review and return",
        "component_states": COMPONENT_STATES,
        "motion_budget": 2,
    }
    outcomes = {
        tuple(item["id"] for item in resolve_interaction_patterns(**kwargs, variation_seed=seed)["selected"])
        for seed in range(24)
    }

    assert len(outcomes) == 1


def test_tied_candidates_vary_across_seeds():
    kwargs = {
        "product_intent": "review",
        "component_states": {"record-list": ["filtered"]},
        "motion_budget": 2,
        "candidates": _tied_candidates(),
    }
    outcomes = {
        resolve_interaction_patterns(**kwargs, variation_seed=seed)["selected"][0]["id"]
        for seed in range(24)
    }

    assert outcomes == {"test:alpha", "test:beta"}


def test_recorded_preference_breaks_ties_before_chance():
    kwargs = {
        "product_intent": "review",
        "component_states": {"record-list": ["filtered"]},
        "motion_budget": 2,
        "candidates": _tied_candidates(),
    }
    outcomes = {
        resolve_interaction_patterns(
            **kwargs, variation_seed=seed, preference_prior={"test:beta": 0.9}
        )["selected"][0]["id"]
        for seed in range(24)
    }

    assert outcomes == {"test:beta"}


def test_design_language_is_axis_wise_and_reproducible():
    kwargs = {
        "visual_keywords": ["seasonal field notes", "soft mineral surfaces"],
        "interaction_keywords": ["contextual return", "time-aware transitions"],
        "composition": "timeline-ledger",
        "density": "spacious",
        "variation_seed": 3,
    }
    first = resolve_design_language(**kwargs)
    repeat = resolve_design_language(**kwargs)
    assert first == repeat
    assert set(first["selected"]) == {"composition", "surface", "typography"}
    assert first["selected"]["composition"]["id"] == "timeline-field"


def test_progress_patterns_require_a_real_async_state():
    result = resolve_interaction_patterns(
        product_intent="return",
        component_states={"return-ritual-prompt": ["due"]},
        motion_budget=2,
        variation_seed=1,
    )
    assert all(item["axis"] != "progress" for item in result["selected"])


def test_role_inference_makes_candidates_reusable_across_projects():
    """The pool must match a project it was not authored against."""
    result = resolve_interaction_patterns(
        product_intent="monitor and operate live orders",
        component_states={
            "order-table": ["loading", "filtered"],
            "filter-tabs": ["current", "selected"],
            "upload-form": ["loading"],
        },
        motion_budget=2,
        density="dense",
        variation_seed=1,
    )

    assert result["selection_mode"] == "contextual-variation"
    assert result["selected"]
    assert set(result["component_roles"].values()) >= {
        "list-surface",
        "navigation-surface",
        "async-action",
    }


def test_dense_surfaces_prefer_cheaper_motion_than_spacious_ones():
    shared = {
        "product_intent": "browse records",
        "component_states": {"record-list": ["content-enter", "filtered"]},
        "motion_budget": 2,
        "variation_seed": 5,
    }
    dense = resolve_interaction_patterns(**{**shared, "density": "dense"})
    spacious = resolve_interaction_patterns(**{**shared, "density": "spacious"})

    def _enter_cost(result):
        for item in result["selected"]:
            if item["axis"] == "enter":
                return item["motion_cost"]
        return None

    assert _enter_cost(dense) is not None
    assert _enter_cost(spacious) is not None
    assert _enter_cost(dense) <= _enter_cost(spacious)


def test_motion_budget_and_component_state_are_hard_constraints():
    result = resolve_interaction_patterns(
        product_intent="save",
        component_states={"memory-seed-composer": ["saving"]},
        motion_budget=0,
        variation_seed=4,
    )

    assert result["selected"] == []
    assert result["selection_mode"] == "no-compatible-candidate"
