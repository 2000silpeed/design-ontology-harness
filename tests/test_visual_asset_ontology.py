import unittest

from design_ontology_harness.graph_builders import build_full_ontology_graph
from design_ontology_harness.graph_schema import EdgeType, NodeType
from design_ontology_harness.graph_spec_sections import build_graph_spec_sections


class VisualAssetOntologyTests(unittest.TestCase):
    def test_generated_visual_assets_are_modeled_for_codex_imagine2(self) -> None:
        graph = build_full_ontology_graph(
            brand_profile={
                "brand_name": "Checkpoint",
                "visual_keywords": ["measured", "editorial"],
                "_resolved_visual_reference": {
                    "mode": "local-images",
                },
            },
            blueprint={
                "principles": [
                    {
                        "keyword": "measured",
                        "name": "Measured proof",
                    },
                ],
                "visual_reference": {"extraction_policy": "advisory-only"},
            },
            component_inventory={
                "families": [
                    {
                        "family": "marketing",
                        "components": ["hero-section", "feature-card"],
                    },
                    {
                        "family": "feedback",
                        "components": ["empty-state"],
                    },
                ],
                "components": [
                    {
                        "name": "hero-section",
                        "family": "marketing",
                        "role": "Landing hero",
                        "supports_primitive": "landing narrative",
                    },
                    {
                        "name": "feature-card",
                        "family": "marketing",
                        "role": "Feature card",
                        "supports_primitive": "card grid",
                    },
                    {
                        "name": "empty-state",
                        "family": "feedback",
                        "role": "No results panel",
                        "supports_primitive": "notifications",
                    },
                ],
            },
            token_schema={"categories": {}},
        )

        model = graph.get_node("image-model:imagine2")
        self.assertIsNotNone(model)
        self.assertEqual(model.type, NodeType.ImageGenerationModel)

        assets = graph.get_nodes_by_type(NodeType.GeneratedVisualAsset)
        asset_ids = {asset.id for asset in assets}
        self.assertIn("visual-asset:brand-aligned-raster", asset_ids)
        self.assertIn("visual-asset:hero-image", asset_ids)
        self.assertIn("visual-asset:card-thumbnail", asset_ids)
        self.assertIn("visual-asset:empty-state-illustration", asset_ids)

        hero = graph.get_node("visual-asset:hero-image")
        self.assertEqual(hero.meta["model"], "imagine2")
        self.assertIn("visual_reference_report.json", hero.meta["prompt_basis"])
        self.assertEqual(hero.meta["manifest_path"], "public/generated/design-system/manifest.json")

        model_edges = graph.get_edges_from("visual-asset:hero-image", EdgeType.generated_with)
        self.assertEqual(model_edges[0].target, "image-model:imagine2")

        target_edges = graph.get_edges_from("visual-asset:hero-image", EdgeType.intended_for)
        self.assertIn("component:hero-section", {edge.target for edge in target_edges})

    def test_generated_visual_asset_plan_is_rendered_in_system_spec_sections(self) -> None:
        graph = build_full_ontology_graph(
            brand_profile={"brand_name": "Checkpoint"},
            blueprint={"principles": []},
            component_inventory={
                "families": [{"family": "marketing", "components": ["hero-section"]}],
                "components": [
                    {
                        "name": "hero-section",
                        "family": "marketing",
                        "role": "Landing hero",
                        "supports_primitive": "landing narrative",
                    }
                ],
            },
            token_schema={"categories": {}},
        )

        sections = build_graph_spec_sections(graph)

        self.assertIn("Generated Visual Asset Plan", sections)
        self.assertIn("imagine2", sections)
        self.assertIn("public/generated/design-system/manifest.json", sections)


if __name__ == "__main__":
    unittest.main()
