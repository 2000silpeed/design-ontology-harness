from design_ontology_harness.color_reference import resolve_semantic_color_reference
from design_ontology_harness.semantic_color_selector import (
    _candidate_accent_bucket,
    _hue_pressure_penalty,
    _reorder_by_hue_pressure,
    build_ontology_supporting_colors,
    ontology_keyword_lookup,
)


def test_ontology_keyword_lookup_resolves_manual_names():
    lookup = ontology_keyword_lookup()
    royal = lookup.get("royal purple")
    assert royal is not None
    assert royal["hex"] == "#6C3BAA"
    assert royal["source_type"] == "semantic-color-ontology"
    assert len(lookup) >= 100, "refreshed snapshot should expose 100+ hex keywords"


def test_hue_pressure_penalty_targets_repeated_hues():
    teal_keyword = {"hex": "#00A591"}
    fresh_keyword = {"hex": "#6C3BAA"}
    pressure = {"green": 5, "teal": 5}
    assert _hue_pressure_penalty(teal_keyword, pressure) > 0
    assert _hue_pressure_penalty(fresh_keyword, pressure) == 0.0
    assert _hue_pressure_penalty(teal_keyword, {}) == 0.0


def test_reorder_prefers_fresh_accent_candidate():
    repeated = {"roles": {"fresh_accent": {"hex": "#00A591"}}}  # green bucket
    fresh = {"roles": {"fresh_accent": {"hex": "#6C3BAA"}}}  # violet bucket
    pressure = {"green": 6}

    reordered, moved = _reorder_by_hue_pressure([repeated, fresh], pressure)
    assert moved is True
    assert reordered[0] is fresh

    untouched, moved_low = _reorder_by_hue_pressure([repeated, fresh], {"green": 1})
    assert moved_low is False
    assert untouched[0] is repeated


def test_candidate_accent_bucket_reads_accent_role():
    # #6C3BAA sits at 266° — the blue/violet bin boundary resolves to "blue"
    candidate = {"roles": {"anchor": {"hex": "#141414"}, "fresh_accent": {"hex": "#6C3BAA"}}}
    assert _candidate_accent_bucket(candidate) == "blue"


def test_ontology_supporting_colors_are_diverse_and_hexed():
    profile = {
        "brand_name": "Test",
        "product_summary": "calm operational console",
        "brand_keywords": ["calm", "precise"],
    }
    supporting = build_ontology_supporting_colors(brand_profile=profile, count=8)
    assert len(supporting) == 8
    assert all(item["hex"].startswith("#") for item in supporting)
    spectrums = {item.get("family") for item in supporting}
    assert len(spectrums) >= 3, "supporting picks should span multiple families"


def test_pathless_manual_roles_resolve_from_ontology():
    profile = {"brand_name": "Test", "product_summary": "arbitration console"}
    reference = resolve_semantic_color_reference(
        profile,
        {"palette_roles": {"primary": "Royal Purple"}},
    )
    assert reference["selection_mode"] == "manual"
    assert reference["active_palette"]["roles"]["primary"]["hex"] == "#6C3BAA"
    assert reference["expanded_palette"]["supporting_colors"], (
        "semantic path must ship ontology-based supporting colors"
    )
