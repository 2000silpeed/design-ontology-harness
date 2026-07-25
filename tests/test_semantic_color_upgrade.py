from copy import deepcopy
import json
from pathlib import Path

from design_ontology_harness.adapters.base import _ensure_base_roles
from design_ontology_harness.color_reference import (
    build_component_color_sets,
    resolve_color_reference,
    resolve_semantic_color_reference,
)
from design_ontology_harness.semantic_color_markdown import (
    load_runtime_color_policy,
    runtime_role_values,
)
from design_ontology_harness.semantic_color_ontology import load_semantic_color_ontology
from design_ontology_harness.semantic_color_selector import (
    _candidate_accent_bucket,
    _hue_pressure_penalty,
    _reorder_by_hue_pressure,
    build_ontology_supporting_colors,
    ontology_keyword_lookup,
    ontology_keyword_lookup_details,
)


def test_ontology_keyword_lookup_resolves_manual_names():
    lookup = ontology_keyword_lookup()
    royal = lookup.get("royal purple")
    assert royal is not None
    assert royal["hex"] == "#6C3BAA"
    assert royal["source_type"] == "semantic-os-synced-markdown"
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


def test_coy_unique_aliases_and_colliding_names_preserve_exact_identity():
    ontology = load_semantic_color_ontology()
    forward = ontology_keyword_lookup_details(ontology)
    reversed_ontology = deepcopy(ontology)
    reversed_ontology["nodes"] = list(reversed(reversed_ontology["nodes"]))
    reverse = ontology_keyword_lookup_details(reversed_ontology)

    queries = {
        "Fuchsia Rose": ("#C94476", "color-keyword-pantone-coy-2001-fuchsia-rose"),
        "Viva Magenta": ("#BB2649", "color-keyword-pantone-coy-2023-viva-magenta"),
        "Cerulean": ("#2A52BE", "color-keyword-cerulean"),
        "Cerulean (Pantone COY 2000)": (
            "#9BB7D6",
            "color-keyword-pantone-coy-2000-cerulean",
        ),
        "color-keyword-pantone-coy-2000-cerulean": (
            "#9BB7D6",
            "color-keyword-pantone-coy-2000-cerulean",
        ),
        "Marsala": ("#964F4C", "color-keyword-marsala"),
        "Marsala (Pantone COY 2015)": (
            "#955251",
            "color-keyword-pantone-coy-2015-marsala",
        ),
    }
    for query, expected in queries.items():
        actual = forward["lookup"][query.casefold()]
        reordered = reverse["lookup"][query.casefold()]
        assert (actual["hex"], actual["semantic_node_id"]) == expected
        assert reordered == actual

    for query in ("cerulean", "marsala"):
        evidence = forward["ambiguities"][query]
        assert evidence == reverse["ambiguities"][query]
        assert evidence["requires_qualified_label_or_id"] is True
        assert len({item["hex"] for item in evidence["candidates"]}) == 2
        assert len({item["semantic_node_id"] for item in evidence["candidates"]}) == 2


def test_manual_roles_accept_unique_coy_name_and_semantic_id_with_ambiguity_evidence():
    reference = resolve_semantic_color_reference(
        {"brand_name": "COY Test", "product_summary": "color identity test"},
        {
            "palette_roles": {
                "primary": "Viva Magenta",
                "accent": "color-keyword-pantone-coy-2000-cerulean",
                "support": "Marsala",
            }
        },
    )

    assert reference["palette_roles"]["primary"]["semantic_node_id"] == (
        "color-keyword-pantone-coy-2023-viva-magenta"
    )
    assert reference["palette_roles"]["accent"]["hex"] == "#9BB7D6"
    assert reference["palette_roles"]["support"]["semantic_node_id"] == (
        "color-keyword-marsala"
    )
    assert reference["manual_lookup_ambiguities"]["support"]["query"] == "marsala"


def test_runtime_role_policy_fills_gaps_without_overriding_project_roles():
    policy = load_runtime_color_policy()
    defaults = runtime_role_values()
    explicit = {"primary": "#123456", "surface": "#FEFEFE"}
    resolved = _ensure_base_roles(explicit)

    assert resolved["primary"] == "#123456"
    assert resolved["surface"] == "#FEFEFE"
    assert resolved["link"] == "#123456"
    for role, value in defaults.items():
        if role not in {"primary", "surface", "link"}:
            assert resolved[role] == value
    assert all(
        item["kind"] in {"runtime-role-default", "derived-runtime-role"}
        for item in policy["light_roles"].values()
    )


def test_component_color_sets_use_runtime_policy_for_sparse_roles():
    defaults = runtime_role_values()
    sets = build_component_color_sets({})

    assert sets["button_secondary"]["surface_default"] == defaults["surface"]
    assert sets["button_secondary"]["text_default"] == defaults["ink"]
    assert sets["input"]["border_default"] == defaults["border"]
    assert sets["input"]["border_error"] == defaults["danger"]


def test_existing_project_palette_roles_keep_base_keyword_identity_and_hex():
    repo_root = Path(__file__).resolve().parents[1]
    expectations = {
        "document-content--minimal-tech": {
            "accent": ("color-keyword-cerulean", "#2A52BE"),
        },
        "conversation-copilot--editorial-warm": {
            "primary": ("color-keyword-marsala", "#964F4C"),
        },
        "document-content--bold-confident": {
            "primary": ("color-keyword-classic-blue", "#0F4C81"),
        },
        "dashboard--bold-confident": {
            "primary": ("color-keyword-ultra-violet", "#5F4B8B"),
            "accent": ("color-keyword-illuminating", "#F5DF4D"),
        },
        "document-content--playful-soft": {
            "accent": ("color-keyword-living-coral", "#FF6F61"),
        },
    }

    for preset_id, role_expectations in expectations.items():
        preset_dir = repo_root / "presets" / preset_id
        profile = json.loads((preset_dir / "brand_profile.json").read_text(encoding="utf-8"))
        profile["color_reference"] = deepcopy(profile["color_reference"])
        profile["color_reference"]["path"] = str(repo_root / "docs" / "color-reference.md")
        resolved, issues = resolve_color_reference(
            profile["color_reference"],
            preset_dir,
            profile,
        )
        assert resolved is not None
        assert not [issue for issue in issues if "entry not found" in issue]
        for role, (semantic_node_id, hex_value) in role_expectations.items():
            actual = resolved["palette_roles"][role]
            assert actual["semantic_node_id"] == semantic_node_id
            assert actual["hex"] == hex_value


def test_current_project_manual_roles_keep_local_and_domain_identity():
    repo_root = Path(__file__).resolve().parents[1]
    expectations = {
        "lattice": {
            "primary": ("color-keyword-iris-violet", "#5A4FCF"),
            "accent": ("color-keyword-cerulean", "#2A52BE"),
            "surface_tint": ("color-keyword-lavender-mist", "#E6E6FA"),
        },
        "quill": {
            "primary": ("color-keyword-marsala", "#964F4C"),
            "accent": ("color-keyword-moss-green", "#8A9A5B"),
            "surface_tint": ("color-keyword-flax", "#EEDC82"),
        },
        "broadside": {
            "primary": ("color-keyword-classic-blue", "#0F4C81"),
            "accent": ("color-keyword-goji-berry", "#CC142F"),
            "surface_tint": ("color-keyword-flame", "#F2552C"),
        },
        "lattice-dash": {
            "primary": ("color-keyword-ultra-violet", "#5F4B8B"),
            "accent": ("color-keyword-illuminating", "#F5DF4D"),
            "surface_tint": ("color-keyword-creamsicle", "#FFD7A0"),
        },
        "panel-pop": {
            "primary": ("color-keyword-periwinkle", "#8E9AF1"),
            "accent": ("color-keyword-living-coral", "#FF6F61"),
            "surface_tint": ("color-keyword-buttercream", "#F3E5AB"),
        },
        "orchard": {
            "primary": ("color-keyword-pantone-coy-2016-rose-quartz", "#F7CAC9"),
            "accent": ("color-keyword-local-dark-salmon", "#E9967A"),
            "surface_tint": ("color-keyword-local-blanched-almond", "#FFEBCD"),
        },
        "world-cup-hub": {
            "primary": ("color-keyword-classic-blue", "#0F4C81"),
            "accent": ("color-keyword-emerald-green", "#50C878"),
            "surface_tint": ("color-keyword-amber", "#FFBF00"),
            "danger": ("color-keyword-crimson", "#BD2E4A"),
            "neutral_anchor": ("color-keyword-prussian-blue", "#003153"),
        },
    }

    for project_id, role_expectations in expectations.items():
        project_dir = repo_root / "projects" / project_id
        profile = json.loads((project_dir / "brand_profile.json").read_text(encoding="utf-8"))
        profile["color_reference"] = deepcopy(profile["color_reference"])
        profile["color_reference"]["path"] = str(repo_root / "docs" / "color-reference.md")
        resolved, issues = resolve_color_reference(
            profile["color_reference"],
            project_dir,
            profile,
        )
        assert resolved is not None
        assert not [issue for issue in issues if "entry not found" in issue]
        for role, (semantic_node_id, hex_value) in role_expectations.items():
            actual = resolved["palette_roles"][role]
            assert (actual["semantic_node_id"], actual["hex"]) == (
                semantic_node_id,
                hex_value,
            )
