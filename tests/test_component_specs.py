import unittest

from design_ontology_harness.authoring import build_component_inventory
from design_ontology_harness.advanced_components import recommend_advanced_components
from design_ontology_harness.cli import _component_specs_source_from_inventory
from design_ontology_harness.component_specs import generate_component_specs
from design_ontology_harness.spec_analyzer import build_component_list
from design_ontology_harness.synthesis import RESPONSIVE_RESILIENCE_POLICY


class ComponentSpecsVisualAdaptationTests(unittest.TestCase):
    def test_visual_reference_hints_flow_into_component_specs(self) -> None:
        brand_profile = {
            "brand_name": "Signal Desk",
            "brand_keywords": ["precise"],
            "anti_keywords": [],
        }
        blueprint = {
            "visual_reference": {"extraction_policy": "advisory-only"},
            "component_style_hints": {
                "cards": {
                    "direction": "outlined cards with thin framing",
                    "confidence": 0.73,
                    "evidence": ["surface=outlined", "density=dense"],
                },
                "navigation": {
                    "direction": "compact navigation with stable scope controls",
                    "confidence": 0.68,
                    "evidence": ["Split-pane workspace"],
                },
                "data_display": {
                    "direction": "thin dividers with restrained accent hierarchy",
                    "confidence": 0.71,
                    "evidence": ["layout=dashboard-grid"],
                },
                "hero": {
                    "direction": "single dominant CTA with quiet secondary actions",
                    "confidence": 0.66,
                    "evidence": ["Narrative landing flow"],
                },
            },
            "visual_language": {
                "surface_style": {"value": "outlined", "confidence": 0.76},
                "density": {"value": "dense", "confidence": 0.72},
                "corner_style": {"value": "sharp", "confidence": 0.64},
                "typography_mood": {"value": "utilitarian", "confidence": 0.61},
            },
            "layout_cues": [
                {"id": "dashboard-grid", "label": "Dashboard grid", "confidence": 0.79},
                {"id": "landing-narrative", "label": "Narrative landing flow", "confidence": 0.67},
            ],
        }
        component_list = [
            {"name": "insight-card", "family": "data-display", "role": "Insight summary", "source": "spec"},
            {"name": "primary-button", "family": "button", "role": "Primary CTA", "source": "spec"},
            {"name": "site-nav", "family": "navigation", "role": "Primary nav", "source": "spec"},
            {"name": "filter-chip", "family": "feedback", "role": "Filter chip", "source": "spec"},
            {"name": "chart-panel", "family": "data-display", "role": "Chart panel", "source": "spec"},
            {"name": "metric-strip", "family": "data-display", "role": "Operational metric strip", "source": "spec"},
            {"name": "policy-matrix", "family": "data-display", "role": "Policy matrix", "source": "spec"},
            {"name": "diff-viewer", "family": "document", "role": "Diff viewer", "source": "spec"},
            {"name": "column-header", "family": "data-display", "role": "Column header", "source": "spec"},
        ]

        specs_data = generate_component_specs(
            brand_profile=brand_profile,
            blueprint=blueprint,
            component_list=component_list,
            documents=[],
        )

        by_name = {spec["name"]: spec for spec in specs_data["specs"]}

        self.assertTrue(specs_data["visual_guidance"]["connected"])
        self.assertEqual(specs_data["visual_guidance"]["surface_style"], "outlined")

        card_aspects = {note["aspect"] for note in by_name["insight-card"]["visual_adaptation"]}
        self.assertIn("card_elevation_tendency", card_aspects)
        self.assertIn("border_vs_fill_emphasis", card_aspects)

        button_aspects = {note["aspect"] for note in by_name["primary-button"]["visual_adaptation"]}
        self.assertIn("cta_prominence", button_aspects)
        self.assertEqual(by_name["primary-button"]["anatomy"]["parts"][0], "container")
        self.assertEqual(by_name["primary-button"]["tokens"]["max-inline-size"], "100%")
        self.assertEqual(by_name["primary-button"]["tokens"]["min-inline-size"], "0")

        nav_aspects = {note["aspect"] for note in by_name["site-nav"]["visual_adaptation"]}
        self.assertIn("filter_nav_density", nav_aspects)
        self.assertIn("nav-bar", by_name["site-nav"]["archetype"])

        chip_aspects = {note["aspect"] for note in by_name["filter-chip"]["visual_adaptation"]}
        self.assertIn("filter_nav_density", chip_aspects)

        panel_aspects = {note["aspect"] for note in by_name["chart-panel"]["visual_adaptation"]}
        self.assertIn("chart_panel_framing", panel_aspects)
        self.assertIn("loading", by_name["chart-panel"]["anatomy"]["states"])
        self.assertIn("데이터 테이블은 scope와 caption 필수", by_name["chart-panel"]["accessibility"])

        strip_aspects = {note["aspect"] for note in by_name["metric-strip"]["visual_adaptation"]}
        self.assertIn("operational_surface_role", strip_aspects)
        self.assertNotIn("card_elevation_tendency", strip_aspects)

        for surface_name in ["policy-matrix", "diff-viewer", "column-header"]:
            surface_aspects = {note["aspect"] for note in by_name[surface_name]["visual_adaptation"]}
            self.assertIn("operational_surface_role", surface_aspects)
            self.assertNotIn("card_elevation_tendency", surface_aspects)

    def test_missing_visual_reference_keeps_visual_adaptation_empty(self) -> None:
        brand_profile = {
            "brand_name": "Glacier",
            "brand_keywords": ["minimal"],
            "anti_keywords": [],
        }
        component_list = [
            {"name": "primary-button", "family": "button", "role": "Primary action", "source": "spec"},
        ]

        specs_data = generate_component_specs(
            brand_profile=brand_profile,
            blueprint={},
            component_list=component_list,
            documents=[],
        )

        self.assertFalse(specs_data["visual_guidance"]["connected"])
        self.assertEqual(specs_data["specs"][0]["visual_adaptation"], [])

    def test_advanced_components_are_recommended_and_specified(self) -> None:
        brand_profile = {
            "brand_name": "Mercer",
            "brand_keywords": ["conversation-copilot", "compliance", "audit", "regulatory"],
            "tone_of_voice": ["calm", "precise"],
            "product_summary": "Enterprise copilot for policy-check, audit-trail, citation, and reviewer handoff.",
            "product_primitives": [
                "chat message",
                "prompt composer",
                "policy-check badge",
                "audit-trail timeline",
                "citation footnote",
                "reviewer assignment chip",
                "data retention indicator",
            ],
        }
        blueprint = {
            "component_strategy": {
                "required_component_families": ["button", "input", "navigation", "feedback", "overlay"],
                "product_primitives": [
                    "compliance-artifact panel",
                    "source reference card",
                    "compliance warning modal",
                ],
            }
        }

        recommendations = recommend_advanced_components(
            brand_profile=brand_profile,
            blueprint=blueprint,
            existing_components=[],
        )
        names = {item["name"] for item in recommendations}
        self.assertIn("policy-matrix", names)
        self.assertIn("citation-drawer", names)
        self.assertIn("approval-rail", names)

        inventory = build_component_inventory(brand_profile, blueprint)
        inventory_names = {item["name"] for item in inventory["components"]}
        self.assertIn("policy-matrix", inventory_names)
        self.assertTrue(inventory["advanced_component_catalog"])
        self.assertTrue(inventory["advanced_recommendations"])

        specs_data = generate_component_specs(
            brand_profile=brand_profile,
            blueprint=blueprint,
            component_list=inventory["components"],
            documents=[],
        )
        by_name = {spec["name"]: spec for spec in specs_data["specs"]}
        policy_matrix = by_name["policy-matrix"]
        self.assertTrue(policy_matrix["advanced_component"])
        self.assertEqual(policy_matrix["archetype"], "advanced:policy-matrix")
        self.assertIn("status-cell", policy_matrix["anatomy"]["parts"])
        self.assertIn("caption describes policy scope", policy_matrix["accessibility"])

    def test_astryx_geist_baseline_replaces_legacy_contextual_defaults(self) -> None:
        brand_profile = {
            "brand_name": "Lean Console",
            "brand_keywords": ["minimal", "precise"],
            "anti_keywords": [],
            "product_primitives": [],
        }
        blueprint = {
            "component_strategy": {
                "required_component_families": ["button", "input", "navigation", "feedback", "overlay"],
            }
        }

        inventory = build_component_inventory(brand_profile, blueprint)
        inventory_names = {item["name"] for item in inventory["components"]}
        analyzer_names = {item["name"] for item in build_component_list([])}

        self.assertTrue({"primary-button", "secondary-button", "icon-button"} <= inventory_names)
        self.assertTrue({"text-field", "select", "checkbox", "switch", "segmented-control"} <= inventory_names)
        self.assertTrue({"breadcrumbs", "tabs", "pagination"} <= inventory_names)
        self.assertTrue({"dialog", "popover", "tooltip"} <= inventory_names)

        legacy_defaults = {
            "ghost-button",
            "link-button",
            "cta-button",
            "mobile-topbar",
            "mobile-tab-bar",
            "back-button",
            "bottom-sheet",
            "modal-dialog",
        }
        self.assertFalse(legacy_defaults & inventory_names)
        self.assertFalse({"ghost-button", "link-button", "cta-button"} & analyzer_names)

        reference_systems = {item["id"] for item in inventory["reference_baseline"]["systems"]}
        self.assertEqual(reference_systems, {"astryx", "geist"})
        self.assertIn("ghost-button", inventory["reference_baseline"]["contextual_not_baseline"])

    def test_authored_component_decision_is_the_implementation_source_of_truth(self) -> None:
        brand_profile = {
            "brand_name": "Foldline",
            "brand_keywords": ["editorial", "personal", "tactile", "decisive"],
            "anti_keywords": ["generic", "dashboard-like", "infinite-card-wall"],
            "product_summary": "Korean-first mobile fashion curation app for shoppable outfit decisions.",
            "application_concept": {
                "primary_job": "사용자가 오늘의 상황과 취향 신호를 바탕으로 하나의 착장 보드를 확정한다.",
                "domain_objects": ["daily brief", "signal spine", "look board", "garment item"],
            },
            "layout_skeleton": {
                "composition": "signal spine plus look board with contextual shop sheet",
                "avoid_layouts": [
                    "generic hero plus card grid",
                    "uniform product card wall",
                    "dashboard metric cards",
                ],
            },
            "product_primitives": [
                "taste signal chip rail",
                "outfit edit canvas",
                "shop drawer",
            ],
            "component_decision": {
                "mode": "llm-authored",
                "rationale": "Implement the outfit decision surface directly.",
                "coverage_families": ["button", "input", "navigation", "feedback", "overlay"],
                "core_components": [
                    {
                        "name": "daily-brief",
                        "family": "content",
                        "role": "Summarizes today's styling context.",
                        "supports_primitive": "daily style brief",
                        "decision_reason": "This replaces generic filter chips.",
                        "states": ["default", "adjusting"],
                    },
                    {
                        "name": "signal-spine",
                        "family": "input",
                        "role": "Shows active recommendation signals vertically.",
                        "supports_primitive": "vertical signal spine",
                        "decision_reason": "This replaces a generic chip rail.",
                        "states": ["default", "active"],
                    },
                    {
                        "name": "look-board",
                        "family": "content",
                        "role": "Shows the selected outfit decision.",
                        "supports_primitive": "single look board",
                        "decision_reason": "This replaces ecommerce product cards.",
                        "states": ["default", "selected"],
                    },
                    {
                        "name": "shop-sheet",
                        "family": "overlay",
                        "role": "Handles selected garment commerce in context.",
                        "supports_primitive": "contextual shop sheet",
                        "decision_reason": "This replaces a generic modal or catalog page.",
                        "states": ["collapsed", "expanded"],
                    },
                ],
                "rejected_components": [
                    {
                        "name": "product-grid",
                        "family": "commerce",
                        "reason": "Conflicts with the authored look-board skeleton.",
                    }
                ],
            },
            "_spec_components": [
                {"name": "product-grid", "family": "commerce", "source": "spec"},
                {"name": "hero-cta-group", "family": "button", "source": "spec"},
                {"name": "data-table", "family": "data-display", "source": "spec"},
            ],
        }
        blueprint = {
            "component_strategy": {
                "required_component_families": ["button", "input", "navigation", "feedback", "overlay"],
                "product_primitives": brand_profile["product_primitives"],
            },
        }

        inventory = build_component_inventory(brand_profile, blueprint)
        inventory_names = [item["name"] for item in inventory["components"]]
        coverage_names = {item["name"] for item in inventory["baseline_coverage_components"]}
        rejected_names = {item["name"] for item in inventory["rejected_components"]}

        self.assertEqual(
            inventory["decision_model"]["implementation_basis"],
            "llm-authored-component-decision",
        )
        self.assertEqual(inventory["decision_model"]["baseline_policy"], "coverage-only")
        self.assertFalse(inventory["decision_model"]["fallback_allowed"])
        self.assertEqual(
            inventory_names,
            ["daily-brief", "signal-spine", "look-board", "shop-sheet"],
        )
        self.assertFalse({"taste-signal-rail", "outfit-edit-canvas", "shop-drawer"} & set(inventory_names))
        self.assertFalse({"hero-cta-group", "data-table"} & set(inventory_names))
        self.assertEqual(inventory["advanced_recommendations"], [])
        self.assertTrue({"primary-button", "segmented-control", "toast"} <= coverage_names)
        self.assertEqual(rejected_names, {"product-grid"})
        self.assertEqual(inventory["component_decision"]["component_count"], 4)

        specs_data = generate_component_specs(
            brand_profile=brand_profile,
            blueprint=blueprint,
            component_list=inventory["components"],
            documents=[],
        )
        specs_by_name = {spec["name"]: spec for spec in specs_data["specs"]}
        self.assertEqual(specs_by_name["daily-brief"]["anatomy"]["states"], ["default", "adjusting"])
        self.assertEqual(specs_by_name["signal-spine"]["anatomy"]["states"], ["default", "active"])
        self.assertEqual(specs_by_name["look-board"]["anatomy"]["states"], ["default", "selected"])
        self.assertEqual(specs_by_name["shop-sheet"]["anatomy"]["states"], ["collapsed", "expanded"])
        self.assertEqual(specs_by_name["signal-spine"]["state_model"]["domain_states"], ["default", "active"])
        self.assertEqual(specs_by_name["look-board"]["supports_primitive"], "single look board")
        self.assertEqual(specs_by_name["shop-sheet"]["contract_provenance"], "llm-authored")
        for spec in specs_data["specs"]:
            for value in spec["tokens"].values():
                self.assertNotIn("var(--color-", str(value))
                self.assertNotIn("var(--space-", str(value))
                self.assertNotIn("var(--font-", str(value))
                self.assertNotIn("var(--radius-", str(value))

    def test_product_specific_primitives_keep_baseline_as_coverage_only(self) -> None:
        brand_profile = {
            "brand_name": "ThreadSense",
            "brand_keywords": ["editorial", "personal", "tactile", "decisive"],
            "anti_keywords": ["generic", "dashboard-like", "infinite-card-wall"],
            "product_summary": "Korean-first mobile fashion curation app for shoppable outfit edits.",
            "application_concept": {
                "primary_job": "사용자가 오늘의 상황과 취향 신호를 바탕으로 하나의 착장 에디트를 확정한다.",
                "domain_objects": ["taste signal", "outfit edit", "garment item", "saved closet"],
            },
            "layout_skeleton": {
                "composition": "taste-signal rail with outfit edit canvas and shop drawer",
                "avoid_layouts": [
                    "generic hero plus card grid",
                    "uniform product card wall",
                    "dashboard metric cards",
                    "infinite feed without curation decision",
                ],
            },
            "product_primitives": [
                "taste signal chip rail",
                "outfit edit canvas",
                "garment stack",
                "why-this-works note",
                "fit and size note",
                "save edit action",
                "shop drawer",
                "alternative item carousel",
                "closet compatibility indicator",
            ],
            "_spec_components": [
                {"name": "product-grid", "family": "commerce", "source": "spec"},
                {"name": "data-table", "family": "data-display", "source": "spec"},
                {"name": "hero-cta-group", "family": "button", "source": "spec"},
                {"name": "dashboard-card", "family": "dashboard-wellness", "source": "spec"},
                {"name": "command-palette", "family": "overlay", "source": "command palette"},
                {"name": "search-field", "family": "input", "source": "search and filter"},
                {"name": "pricing-card", "family": "data-display", "source": "pricing and plans"},
                {"name": "activation-funnel", "family": "dashboard-growth", "source": "growth analytics admin"},
            ],
        }
        blueprint = {
            "component_strategy": {
                "required_component_families": ["button", "input", "navigation", "feedback", "overlay"],
                "product_primitives": brand_profile["product_primitives"],
            },
        }

        inventory = build_component_inventory(brand_profile, blueprint)
        inventory_names = {item["name"] for item in inventory["components"]}
        coverage_names = {item["name"] for item in inventory["baseline_coverage_components"]}
        rejected_names = {item["name"] for item in inventory["rejected_components"]}
        advanced_names = {item["name"] for item in inventory["advanced_recommendations"]}

        self.assertEqual(inventory["decision_model"]["implementation_basis"], "legacy-product-primitive-fallback")
        self.assertEqual(inventory["decision_model"]["baseline_policy"], "coverage-only")
        self.assertTrue({
            "taste-signal-rail",
            "outfit-edit-canvas",
            "garment-row",
            "why-this-works-note",
            "shop-drawer",
            "alternative-item-rail",
        } <= inventory_names)
        self.assertTrue({"primary-button", "segmented-control", "toast"} <= coverage_names)
        self.assertFalse({"primary-button", "segmented-control", "data-table"} & inventory_names)
        self.assertTrue({
            "product-grid",
            "data-table",
            "hero-cta-group",
            "dashboard-card",
            "command-palette",
            "search-field",
            "pricing-card",
            "activation-funnel",
        } <= rejected_names)
        self.assertFalse({"inspector-drawer", "resizable-split-pane", "command-palette"} & advanced_names)

    def test_component_specs_use_pruned_inventory_when_available(self) -> None:
        raw_spec_components = [
            {"name": "product-grid", "family": "commerce", "source": "spec"},
            {"name": "hero-container", "family": "marketing", "source": "spec"},
        ]
        inventory = {
            "components": [
                {
                    "name": "outfit-edit-canvas",
                    "family": "content",
                    "supports_primitive": "outfit edit canvas",
                },
                {
                    "name": "shop-drawer",
                    "family": "overlay",
                    "supports_primitive": "shop drawer",
                },
            ],
            "rejected_components": raw_spec_components,
        }

        source = _component_specs_source_from_inventory(raw_spec_components, inventory)
        names = {item["name"] for item in source}

        self.assertEqual(names, {"outfit-edit-canvas", "shop-drawer"})

    def test_operational_surfaces_suppress_card_named_advanced_recommendations(self) -> None:
        brand_profile = {
            "brand_name": "Northline Ops",
            "brand_keywords": ["operations", "dashboard", "risk", "workflow"],
            "anti_keywords": ["card wall", "decorative dashboard"],
            "product_summary": "운영팀이 SLA 위험, 예외 queue, source ledger를 처리하는 operational overview.",
            "product_primitives": [
                "operational overview",
                "metric strip",
                "status summary row",
                "source ledger",
                "data tables",
                "operational rail",
            ],
        }
        blueprint = {
            "app_mode": "dashboard",
            "component_strategy": {
                "product_primitives": [
                    "operational overview",
                    "data tables",
                    "source ledger",
                ],
            },
        }

        recommendations = recommend_advanced_components(
            brand_profile=brand_profile,
            blueprint=blueprint,
            existing_components=[],
            limit=12,
        )
        names = {item["name"] for item in recommendations}

        self.assertIn("bulk-action-table", names)
        self.assertIn("saved-view-bar", names)
        self.assertFalse({name for name in names if name.endswith("-card")})

    def test_responsive_guidance_flows_into_button_specs(self) -> None:
        brand_profile = {
            "brand_name": "TacticLens",
            "brand_keywords": ["precise"],
            "anti_keywords": [],
        }
        blueprint = {
            "governance": {
                "responsive_resilience_policy": RESPONSIVE_RESILIENCE_POLICY,
            }
        }
        component_list = [
            {"name": "primary-button", "family": "button", "role": "Primary CTA", "source": "spec"},
        ]

        specs_data = generate_component_specs(
            brand_profile=brand_profile,
            blueprint=blueprint,
            component_list=component_list,
            documents=[],
        )

        self.assertTrue(specs_data["responsive_guidance"]["active"])
        self.assertIn(320, specs_data["responsive_guidance"]["required_widths_px"])
        button = specs_data["specs"][0]
        notes = " ".join(button["implementation_notes"])
        self.assertIn("max-inline-size: 100%", notes)
        self.assertIn("fixed `width`/`min-width`", notes)


if __name__ == "__main__":
    unittest.main()
