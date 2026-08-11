from design_ontology_harness.interaction_resolver import resolve_design_language, resolve_interaction_patterns


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

    assert result["schema_version"] == "interaction-selection/v1"
    assert result["selection_mode"] == "contextual-variation"
    assert result["selected"]
    assert all(item["covered_components"] for item in result["selected"])
    assert all(item["covered_states"] for item in result["selected"])
    assert result["constraints"]["reference_policy"] == "advisory-only"


def test_same_seed_is_reproducible_but_different_seeds_can_vary():
    kwargs = {
        "product_intent": "review and return",
        "component_states": COMPONENT_STATES,
        "motion_budget": 2,
    }
    first = resolve_interaction_patterns(**kwargs, variation_seed=2)
    repeat = resolve_interaction_patterns(**kwargs, variation_seed=2)
    other = resolve_interaction_patterns(**kwargs, variation_seed=7)

    assert first["selected"] == repeat["selected"]
    assert first["selected"] != other["selected"]


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


def test_async_progress_does_not_match_due_state():
    result = resolve_interaction_patterns(
        product_intent="return",
        component_states={"return-ritual-prompt": ["due"]},
        motion_budget=2,
        variation_seed=1,
    )
    assert all(item["id"] != "async-care-progress" for item in result["selected"])


def test_motion_budget_and_component_state_are_hard_constraints():
    result = resolve_interaction_patterns(
        product_intent="save",
        component_states={"memory-seed-composer": ["saving"]},
        motion_budget=0,
        variation_seed=4,
    )

    assert result["selected"] == []
    assert result["selection_mode"] == "no-compatible-candidate"
