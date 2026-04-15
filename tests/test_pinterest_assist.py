import unittest

from design_ontology_harness.pinterest_assist import build_pinterest_assist_bundle


class PinterestAssistBundleTests(unittest.TestCase):
    def test_build_pinterest_assist_bundle_creates_plan_and_manifests(self) -> None:
        brand_profile = {
            "brand_name": "Signal Desk",
            "brand_keywords": ["calm", "editorial"],
            "anti_keywords": ["noisy"],
            "visual_reference": {
                "mode": "pinterest-assisted",
                "pinterest_assist": {
                    "enabled": True,
                    "capture_mode": "manual-save",
                    "capture_dir": "references/visual/pinterest-assisted",
                    "max_candidates_per_query": 4,
                    "max_selected_per_query": 2,
                    "preferred_sources": ["pins", "boards"],
                },
            },
        }
        query_report = {
            "queries": [
                {
                    "query": "editorial dashboard ui",
                    "intent": "data-display",
                    "primitive": "dashboard cards",
                    "sources": ["primitive:dashboard cards"],
                },
                {
                    "query": "warm onboarding flow",
                    "intent": "flow",
                    "primitive": "onboarding and stepper",
                    "sources": ["primitive:onboarding and stepper"],
                },
            ]
        }

        bundle = build_pinterest_assist_bundle(brand_profile=brand_profile, query_report=query_report)

        self.assertEqual(bundle["plan"]["activation_state"], "active")
        self.assertEqual(bundle["plan"]["query_count"], 2)
        self.assertEqual(bundle["plan"]["queries"][0]["candidate_slots"], 4)
        self.assertEqual(bundle["plan"]["queries"][0]["selection_slots"], 2)
        self.assertIn("build/visuals/pinterest_assist_plan.json", bundle["plan"]["artifact_outputs"])
        self.assertEqual(bundle["plan"]["risk_guardrails"][0]["id"], "auth-and-dynamic-loading")

        first_candidates = bundle["candidate_manifest"]["queries"][0]["candidates"]
        self.assertEqual(len(first_candidates), 4)
        self.assertEqual(first_candidates[0]["candidate_id"], "q01-c01")
        self.assertEqual(first_candidates[0]["usage_scope"], "reference-analysis-only")
        self.assertFalse(first_candidates[0]["redistribution_allowed"])

        first_selected = bundle["selection_manifest"]["queries"][0]["selected"]
        self.assertEqual(len(first_selected), 2)
        self.assertEqual(first_selected[0]["selection_id"], "q01-s01")
        self.assertEqual(first_selected[0]["usage_scope"], "reference-analysis-only")

    def test_preview_mode_when_pinterest_assist_not_enabled(self) -> None:
        brand_profile = {
            "brand_name": "Glacier",
            "visual_reference": {
                "mode": "local-images",
            },
        }
        query_report = {
            "queries": [
                {"query": "minimal landing hero", "intent": "marketing", "primitive": "hero section", "sources": []}
            ]
        }

        bundle = build_pinterest_assist_bundle(brand_profile=brand_profile, query_report=query_report)

        self.assertEqual(bundle["plan"]["activation_state"], "preview")
        self.assertEqual(bundle["config"]["capture_mode"], "manual-save")
        self.assertEqual(bundle["candidate_manifest"]["queries"][0]["query_id"], "q01")
        self.assertEqual(bundle["selection_manifest"]["risk_guardrails"][-1]["id"], "robots-and-access-constraints")


if __name__ == "__main__":
    unittest.main()
