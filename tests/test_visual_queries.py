import unittest

from design_ontology_harness.visual_queries import generate_visual_queries


class VisualQueryGenerationTests(unittest.TestCase):
    def test_generate_visual_queries_with_spec_bias(self) -> None:
        brand_profile = {
            "brand_keywords": ["calm", "precise", "editorial", "trustworthy"],
            "anti_keywords": ["generic", "playful"],
            "visual_keywords": ["structured whitespace", "measured contrast", "text-first hierarchy"],
            "interaction_keywords": ["predictable states", "low-noise motion"],
            "product_primitives": [
                "workspace navigation",
                "dashboard cards",
                "data tables",
                "hero section",
                "pricing and plans",
            ],
            "color_reference": {
                "palette_strategy": {
                    "temperature": "warm",
                    "surface_style": "tinted",
                }
            },
        }
        spec_text = """
        이 제품은 대시보드와 데이터 테이블, 검색/필터, 차트 패널이 핵심입니다.
        랜딩 상단에는 hero 섹션과 pricing 비교가 필요합니다.
        """

        report = generate_visual_queries(brand_profile=brand_profile, spec_text=spec_text, limit=12)

        self.assertGreaterEqual(report["query_count"], 8)
        self.assertLessEqual(report["query_count"], 12)
        queries = [item["query"] for item in report["queries"]]
        self.assertTrue(any("dashboard" in query or "control panel" in query for query in queries))
        self.assertTrue(any("hero" in query or "landing" in query for query in queries))
        self.assertIn("generic", report["avoid_terms"])
        self.assertEqual(report["style_axes"]["temperature_hint"], "warm")

    def test_generate_visual_queries_without_spec_uses_primitives(self) -> None:
        brand_profile = {
            "brand_keywords": ["minimal", "trustworthy"],
            "anti_keywords": [],
            "visual_keywords": ["quiet contrast"],
            "interaction_keywords": [],
            "product_primitives": ["site header", "feature grid", "landing cta section"],
        }

        report = generate_visual_queries(brand_profile=brand_profile, spec_text=None, limit=8)

        self.assertGreater(report["query_count"], 0)
        self.assertIn("site header", report["active_primitives"])
        self.assertTrue(any(item["intent"] == "marketing" for item in report["queries"]))


if __name__ == "__main__":
    unittest.main()
