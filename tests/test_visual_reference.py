import tempfile
import unittest
from pathlib import Path

from design_ontology_harness.visual_reference import resolve_visual_reference


class VisualReferenceProvenanceTests(unittest.TestCase):
    def test_resolve_visual_reference_marks_inferred_and_unverified_signals(self) -> None:
        config = {
            "mode": "pinterest-assisted",
            "query": ["editorial dashboard", "warm premium onboarding flow"],
            "sources": [],
            "must_include": ["split-pane workspace"],
            "avoid_patterns": ["glassmorphism-heavy surfaces"],
            "notes": ["advisory-only visual exploration"],
        }
        brand_profile = {
            "brand_name": "Signal Desk",
            "brand_keywords": ["calm", "editorial"],
            "anti_keywords": ["noisy"],
            "product_primitives": ["dashboard cards", "workspace navigation"],
        }

        with tempfile.TemporaryDirectory() as tmpdir:
            summary, issues = resolve_visual_reference(config, Path(tmpdir), brand_profile)

        self.assertIn("visual_reference.sources is empty", issues)
        self.assertEqual(summary["visual_motifs"]["density"]["provenance"]["level"], "inferred")
        self.assertEqual(summary["visual_motifs"]["color_balance"]["provenance"]["level"], "unverified")
        self.assertEqual(summary["layout_cues"][0]["provenance"]["level"], "inferred")
        self.assertEqual(summary["component_style_hints"]["cards"]["provenance"]["level"], "inferred")
        self.assertEqual(summary["candidate_component_archetypes"][0]["provenance"]["level"], "inferred")


if __name__ == "__main__":
    unittest.main()
