import unittest

from design_ontology_harness.authoring import build_component_inventory
from design_ontology_harness.advanced_components import recommend_advanced_components
from design_ontology_harness.component_specs import generate_component_specs
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
