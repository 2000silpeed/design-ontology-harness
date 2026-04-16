import unittest
from pathlib import Path

from design_ontology_harness.cli import (
    _apply_pinterest_candidate_selection_updates,
    _sync_pinterest_selected_sources,
)
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

    def test_existing_local_captures_are_reflected_in_manifests(self) -> None:
        import tempfile

        with tempfile.TemporaryDirectory() as tmpdir:
            project_dir = Path(tmpdir)
            capture_dir = project_dir / "references/visual/pinterest-assisted/q01-editorial_review_hub"
            capture_dir.mkdir(parents=True)
            capture_path = capture_dir / "hero.png"
            capture_path.write_bytes(b"png")

            brand_profile = {
                "brand_name": "Checkpoint",
                "visual_reference": {
                    "mode": "pinterest-assisted",
                    "sources": ["references/visual/pinterest-assisted/q01-editorial_review_hub/hero.png"],
                    "pinterest_assist": {
                        "enabled": True,
                        "capture_mode": "manual-save",
                        "capture_dir": "references/visual/pinterest-assisted",
                        "max_candidates_per_query": 2,
                        "max_selected_per_query": 1,
                    },
                },
            }
            query_report = {
                "queries": [
                    {
                        "query": "editorial review hub",
                        "intent": "layout",
                        "primitive": "comparison and ranking",
                        "sources": ["primitive:comparison and ranking"],
                    }
                ]
            }

            bundle = build_pinterest_assist_bundle(
                brand_profile=brand_profile,
                query_report=query_report,
                project_dir=project_dir,
            )

            self.assertEqual(bundle["plan"]["capture_progress"]["captured_count"], 1)
            self.assertEqual(bundle["plan"]["capture_progress"]["selected_count"], 1)
            self.assertEqual(bundle["candidate_manifest"]["status"], "selected")
            self.assertEqual(bundle["candidate_manifest"]["queries"][0]["candidates"][0]["status"], "captured")
            self.assertTrue(bundle["candidate_manifest"]["queries"][0]["candidates"][0]["selected"])
            self.assertEqual(bundle["selection_manifest"]["status"], "selected")
            self.assertEqual(bundle["selection_manifest"]["queries"][0]["selected"][0]["status"], "selected")

    def test_captured_candidate_metadata_is_merged_into_manifest(self) -> None:
        import tempfile

        with tempfile.TemporaryDirectory() as tmpdir:
            project_dir = Path(tmpdir)
            capture_path = project_dir / "references/visual/pinterest-assisted/q01-editorial_review_hub/q01-c01.png"
            capture_path.parent.mkdir(parents=True)
            capture_path.write_bytes(b"png")

            brand_profile = {
                "brand_name": "Checkpoint",
                "visual_reference": {
                    "mode": "pinterest-assisted",
                    "pinterest_assist": {
                        "enabled": True,
                        "capture_mode": "playwright-capture",
                        "capture_dir": "references/visual/pinterest-assisted",
                        "max_candidates_per_query": 2,
                        "max_selected_per_query": 1,
                    },
                },
            }
            query_report = {
                "queries": [
                    {
                        "query": "editorial review hub",
                        "intent": "layout",
                        "primitive": "comparison and ranking",
                        "sources": ["primitive:comparison and ranking"],
                    }
                ]
            }
            captured_candidates = {
                "q01": [
                    {
                        "candidate_id": "q01-c01",
                        "source_type": "pin",
                        "platform": "pinterest",
                        "pin_url": "https://www.pinterest.com/pin/123/",
                        "reference_url": "https://www.pinterest.com/pin/123/",
                        "search_url": "https://www.pinterest.com/search/pins/?q=editorial%20review%20hub",
                        "capture_method": "playwright-screenshot",
                        "notes": "editorial layout reference",
                        "preview_url": "https://example.com/preview.jpg",
                        "alt_text": "editorial magazine page",
                    }
                ]
            }
            existing_candidate_manifest = {
                "queries": [
                    {
                        "query_id": "q01",
                        "candidates": [
                            {
                                "candidate_id": "q01-c01",
                                "capture_path": "references/visual/pinterest-assisted/q01-editorial_review_hub/q01-c01.png",
                            }
                        ],
                    }
                ]
            }

            bundle = build_pinterest_assist_bundle(
                brand_profile=brand_profile,
                query_report=query_report,
                project_dir=project_dir,
                captured_candidates=captured_candidates,
                existing_candidate_manifest=existing_candidate_manifest,
            )

            first_candidate = bundle["candidate_manifest"]["queries"][0]["candidates"][0]
            self.assertEqual(first_candidate["source_type"], "pin")
            self.assertEqual(first_candidate["platform"], "pinterest")
            self.assertEqual(first_candidate["pin_url"], "https://www.pinterest.com/pin/123/")
            self.assertEqual(first_candidate["capture_method"], "playwright-screenshot")
            self.assertEqual(first_candidate["notes"], "editorial layout reference")
            self.assertEqual(first_candidate["preview_url"], "https://example.com/preview.jpg")

    def test_explicit_selection_manifest_is_preserved_before_source_sync(self) -> None:
        import tempfile

        with tempfile.TemporaryDirectory() as tmpdir:
            project_dir = Path(tmpdir)
            capture_path = project_dir / "references/visual/pinterest-assisted/q01-editorial_review_hub/q01-c01.png"
            capture_path.parent.mkdir(parents=True)
            capture_path.write_bytes(b"png")

            brand_profile = {
                "brand_name": "Checkpoint",
                "visual_reference": {
                    "mode": "local-images",
                    "sources": [],
                    "pinterest_assist": {
                        "enabled": True,
                        "capture_mode": "playwright-capture",
                        "capture_dir": "references/visual/pinterest-assisted",
                        "max_candidates_per_query": 2,
                        "max_selected_per_query": 1,
                    },
                },
            }
            query_report = {
                "queries": [
                    {
                        "query": "editorial review hub",
                        "intent": "layout",
                        "primitive": "comparison and ranking",
                        "sources": ["primitive:comparison and ranking"],
                    }
                ]
            }
            existing_selection_manifest = {
                "queries": [
                    {
                        "query_id": "q01",
                        "selected": [
                            {
                                "selection_id": "q01-s01",
                                "status": "selected",
                                "candidate_id": "q01-c01",
                                "reference_url": "https://www.pinterest.com/pin/123/",
                                "capture_path": "references/visual/pinterest-assisted/q01-editorial_review_hub/q01-c01.png",
                                "selection_reason": "Strong editorial hierarchy",
                                "notes": "keep for headline rhythm",
                            }
                        ],
                    }
                ]
            }

            bundle = build_pinterest_assist_bundle(
                brand_profile=brand_profile,
                query_report=query_report,
                project_dir=project_dir,
                existing_selection_manifest=existing_selection_manifest,
            )

            self.assertEqual(bundle["plan"]["capture_progress"]["selected_count"], 1)
            self.assertEqual(bundle["plan"]["capture_progress"]["promoted_count"], 0)
            self.assertTrue(bundle["candidate_manifest"]["queries"][0]["candidates"][0]["selected"])
            first_selection = bundle["selection_manifest"]["queries"][0]["selected"][0]
            self.assertEqual(first_selection["status"], "selected")
            self.assertEqual(first_selection["selection_reason"], "Strong editorial hierarchy")
            self.assertFalse(first_selection["promoted_to_sources"])

    def test_apply_pinterest_candidate_selection_updates_replaces_query_slots(self) -> None:
        candidate_manifest = {
            "queries": [
                {
                    "query_id": "q01",
                    "candidates": [
                        {
                            "candidate_id": "q01-c01",
                            "status": "captured",
                            "capture_path": "references/visual/pinterest-assisted/q01/q01-c01.png",
                            "reference_url": "https://www.pinterest.com/pin/101/",
                            "notes": "first option",
                        },
                        {
                            "candidate_id": "q01-c02",
                            "status": "captured",
                            "capture_path": "references/visual/pinterest-assisted/q01/q01-c02.png",
                            "reference_url": "https://www.pinterest.com/pin/102/",
                            "notes": "second option",
                        },
                    ],
                },
                {
                    "query_id": "q02",
                    "candidates": [
                        {
                            "candidate_id": "q02-c01",
                            "status": "captured",
                            "capture_path": "references/visual/pinterest-assisted/q02/q02-c01.png",
                            "reference_url": "https://www.pinterest.com/pin/201/",
                            "notes": "keep existing",
                        }
                    ],
                },
            ]
        }
        selection_manifest = {
            "queries": [
                {
                    "query_id": "q01",
                    "selected": [
                        {
                            "selection_id": "q01-s01",
                            "status": "selected",
                            "candidate_id": "q01-c01",
                            "reference_url": "https://www.pinterest.com/pin/101/",
                            "capture_path": "references/visual/pinterest-assisted/q01/q01-c01.png",
                            "selection_reason": "Previous pick",
                            "notes": "old",
                        },
                        {
                            "selection_id": "q01-s02",
                            "status": "open",
                            "candidate_id": None,
                            "reference_url": None,
                            "capture_path": None,
                            "selection_reason": None,
                            "notes": None,
                        },
                    ],
                },
                {
                    "query_id": "q02",
                    "selected": [
                        {
                            "selection_id": "q02-s01",
                            "status": "selected",
                            "candidate_id": "q02-c01",
                            "reference_url": "https://www.pinterest.com/pin/201/",
                            "capture_path": "references/visual/pinterest-assisted/q02/q02-c01.png",
                            "selection_reason": "Keep untouched query",
                            "notes": "existing",
                        }
                    ],
                },
            ]
        }

        updated = _apply_pinterest_candidate_selection_updates(
            candidate_manifest=candidate_manifest,
            existing_selection_manifest=selection_manifest,
            candidate_ids=["q01-c02"],
            reason="Better fit",
            note=None,
        )

        first_query_selected = updated["queries"][0]["selected"]
        self.assertEqual(first_query_selected[0]["candidate_id"], "q01-c02")
        self.assertEqual(first_query_selected[0]["selection_reason"], "Better fit")
        self.assertEqual(first_query_selected[0]["notes"], "second option")
        self.assertEqual(first_query_selected[1]["status"], "open")
        self.assertEqual(updated["queries"][1]["selected"][0]["candidate_id"], "q02-c01")
        self.assertEqual(updated["status"], "selected")

    def test_sync_pinterest_selected_sources_replaces_managed_sources_only(self) -> None:
        import tempfile

        with tempfile.TemporaryDirectory() as tmpdir:
            project_dir = Path(tmpdir)
            raw_brand_profile = {
                "visual_reference": {
                    "sources": [
                        "docs/reference/hero.png",
                        "references/visual/pinterest-assisted/old/q01-c01.png",
                    ],
                    "pinterest_assist": {
                        "capture_dir": "references/visual/pinterest-assisted",
                    },
                }
            }
            selection_manifest = {
                "capture_dir": "references/visual/pinterest-assisted",
                "queries": [
                    {
                        "query_id": "q01",
                        "selected": [
                            {
                                "selection_id": "q01-s01",
                                "status": "selected",
                                "capture_path": "references/visual/pinterest-assisted/q01/q01-c02.png",
                            }
                        ],
                    },
                    {
                        "query_id": "q02",
                        "selected": [
                            {
                                "selection_id": "q02-s01",
                                "status": "open",
                                "capture_path": None,
                            },
                            {
                                "selection_id": "q02-s02",
                                "status": "selected",
                                "capture_path": "references/visual/pinterest-assisted/q02/q02-c01.png",
                            },
                        ],
                    },
                ],
            }

            result = _sync_pinterest_selected_sources(
                raw_brand_profile=raw_brand_profile,
                selection_manifest=selection_manifest,
                base_dir=project_dir,
            )

            self.assertEqual(
                raw_brand_profile["visual_reference"]["sources"],
                [
                    "docs/reference/hero.png",
                    "references/visual/pinterest-assisted/q01/q01-c02.png",
                    "references/visual/pinterest-assisted/q02/q02-c01.png",
                ],
            )
            self.assertEqual(result["selected_count"], 2)
            self.assertEqual(result["managed_source_count"], 2)


if __name__ == "__main__":
    unittest.main()
