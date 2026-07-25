from __future__ import annotations

import json
import tempfile
import unittest
from hashlib import sha256
from pathlib import Path

from design_ontology_harness.visual_asset_prompts import (
    PROMPT_PACKET_SCHEMA,
    build_visual_prompt_packet,
    write_visual_prompt_outputs,
)


class VisualAssetPromptTests(unittest.TestCase):
    def setUp(self) -> None:
        self.brand = {
            "brand_name": "Fieldnote",
            "product_summary": "field research evidence review",
            "anti_keywords": ["playful", "generic dashboard"],
        }
        self.blueprint = {
            "active_palette": {"surface": "#F4F1E8", "accent": "#315C4B"},
            "visual_reference": {
                "visual_motifs": {
                    "density": {"value": "dense"},
                    "surface_style": {"value": "tactile editorial"},
                }
            },
        }
        self.ontology = {
            "nodes": [
                {
                    "id": "visual-asset:editorial-hero",
                    "type": "GeneratedVisualAsset",
                    "label": "Evidence field hero",
                    "meta": {
                        "slot": "editorial-hero",
                        "status": "promptable",
                        "usage": "Show field evidence as a credible working artifact",
                        "aspect_ratios": ["16:9", "3:2"],
                    },
                },
                {
                    "id": "visual-asset:integrated",
                    "type": "GeneratedVisualAsset",
                    "label": "Already integrated",
                    "meta": {"status": "integrated"},
                },
                {
                    "id": "visual-asset:comic-cover",
                    "type": "GeneratedVisualAsset",
                    "label": "Comic cover",
                    "meta": {"slot": "comic-cover", "status": "promptable"},
                },
                {
                    "id": "visual-asset:editorial-cover",
                    "type": "GeneratedVisualAsset",
                    "label": "Editorial cover",
                    "meta": {"slot": "editorial-cover", "status": "promptable"},
                },
            ],
            "edges": [
                {
                    "type": "intended_for",
                    "source": "visual-asset:editorial-hero",
                    "target": "component:hero",
                }
            ],
        }

    def test_builds_grounded_prompt_for_promptable_slots(self) -> None:
        packet = build_visual_prompt_packet(
            brand_profile=self.brand,
            blueprint=self.blueprint,
            ontology=self.ontology,
            candidates_per_slot=2,
        )

        self.assertEqual(packet["schema_version"], PROMPT_PACKET_SCHEMA)
        self.assertEqual(len(packet["slots"]), 1)
        slot = packet["slots"][0]
        self.assertEqual(slot["candidate_count"], 2)
        self.assertEqual(slot["intended_for"], ["component:hero"])
        self.assertIn("field research evidence review", slot["prompt"])
        self.assertIn("#315C4B", slot["prompt"])
        self.assertIn("tactile editorial", slot["prompt"])
        self.assertIn("generic dashboard", slot["prompt"])
        self.assertEqual(slot["generation"]["api_fallback"], "disabled")

    def test_includes_specialized_slot_only_when_domain_matches(self) -> None:
        self.brand["product_summary"] = "웹툰 연재와 회차 표지를 관리하는 편집 도구"
        packet = build_visual_prompt_packet(
            brand_profile=self.brand,
            blueprint=self.blueprint,
            ontology=self.ontology,
        )

        self.assertEqual(
            [slot["slot"] for slot in packet["slots"]],
            ["editorial-hero", "comic-cover", "editorial-cover"],
        )

    def test_includes_editorial_cover_only_for_editorial_domain(self) -> None:
        self.brand["product_summary"] = "case study article publishing workspace"
        packet = build_visual_prompt_packet(
            brand_profile=self.brand,
            blueprint=self.blueprint,
            ontology=self.ontology,
        )

        self.assertEqual([slot["slot"] for slot in packet["slots"]], ["editorial-hero", "editorial-cover"])

    def test_writes_packet_markdown_and_manifest_template(self) -> None:
        packet = build_visual_prompt_packet(
            brand_profile=self.brand,
            blueprint=self.blueprint,
            ontology=self.ontology,
        )
        with tempfile.TemporaryDirectory() as tmp:
            result = write_visual_prompt_outputs(Path(tmp), packet)
            manifest = json.loads(result.manifest_path.read_text(encoding="utf-8"))
            markdown = result.markdown_path.read_text(encoding="utf-8")

            self.assertEqual(result.prompt_count, 1)
            self.assertTrue(result.packet_path.exists())
            self.assertIn("Evidence field hero", markdown)
            self.assertIn("Review gate", markdown)
            self.assertEqual(manifest["assets"][0]["status"], "planned")
            self.assertIsNone(manifest["assets"][0]["asset_path"])
            self.assertEqual(manifest["generator"]["id"], "image-model:codex-imagegen")
            self.assertEqual(manifest["schema_version"], "visual-asset-manifest/v2")
            self.assertIn("project", manifest)
            self.assertIn("brand", manifest)
            self.assertIn("source_session", manifest)
            self.assertEqual(manifest["prompt_packet"], "imagegen-prompt-packet.json")
            self.assertEqual(len(manifest["prompt_packet_sha256"]), 64)
            self.assertIn("label", manifest["assets"][0])
            self.assertIn("format", manifest["assets"][0])
            self.assertIn("size_kb", manifest["assets"][0])
            self.assertIsNone(manifest["assets"][0]["generation_provenance_version"])
            self.assertIsNone(manifest["assets"][0]["generator"])
            self.assertIsNone(manifest["assets"][0]["generation_run_id"])
            self.assertIsNone(manifest["assets"][0]["candidate_id"])
            self.assertEqual(
                manifest["assets"][0]["prompt_packet_sha256"],
                manifest["prompt_packet_sha256"],
            )
            self.assertEqual(
                manifest["assets"][0]["prompt_packet_slot_id"],
                "visual-asset:editorial-hero",
            )
            self.assertEqual(len(manifest["assets"][0]["prompt_slot_sha256"]), 64)

            manifest["assets"][0]["status"] = "accepted"
            manifest["assets"][0]["asset_path"] = "assets/accepted.png"
            result.manifest_path.write_text(json.dumps(manifest), encoding="utf-8")
            write_visual_prompt_outputs(Path(tmp), packet)
            rebuilt = json.loads(result.manifest_path.read_text(encoding="utf-8"))
            self.assertEqual(rebuilt["assets"][0]["status"], "accepted")
            self.assertEqual(rebuilt["assets"][0]["asset_path"], "assets/accepted.png")
            self.assertEqual(
                rebuilt["assets"][0]["prompt_packet_sha256"],
                rebuilt["prompt_packet_sha256"],
            )

    def test_rejects_candidate_counts_outside_supported_range(self) -> None:
        with self.assertRaises(ValueError):
            build_visual_prompt_packet(
                brand_profile=self.brand,
                blueprint=self.blueprint,
                ontology=self.ontology,
                candidates_per_slot=5,
            )

    def test_does_not_overwrite_invalid_existing_manifest(self) -> None:
        packet = build_visual_prompt_packet(
            brand_profile=self.brand,
            blueprint=self.blueprint,
            ontology=self.ontology,
        )
        with tempfile.TemporaryDirectory() as tmp:
            manifest_path = Path(tmp) / "manifest.json"
            manifest_path.write_text("{not valid json", encoding="utf-8")

            with self.assertRaisesRegex(ValueError, "was not overwritten"):
                write_visual_prompt_outputs(Path(tmp), packet)
            self.assertEqual(manifest_path.read_text(encoding="utf-8"), "{not valid json")

    def test_fixture_led_packet_uses_direction_and_context_slots_only(self) -> None:
        fixture_brand = {
            "brand_name": "World Cup Hub",
            "product_summary": "Korean fixture monitoring and fan participation product",
            "anti_keywords": ["generic dashboard"],
            "application_concept": {
                "primary_job": "find a fixture and continue into one selected match context",
                "operating_mode": "fixture-monitoring-and-fan-participation",
            },
            "layout_skeleton": {
                "composition": "fixture-led-command-desk-with-synchronized-match-rail",
                "first_screen_contract": [
                    "filters and a comparison table appear before imagery",
                ],
                "avoid_layouts": ["generic hero plus card grid"],
            },
            "design_differentiation": {
                "signature_moves": ["selectedMatchId connects table and rail"],
            },
        }
        fixture_ontology = {
            "nodes": [
                {
                    "id": "visual-asset:fixture-led-ui-direction-mockup",
                    "type": "GeneratedVisualAsset",
                    "label": "Fixture-led UI direction mockup",
                    "meta": {
                        "slot": "fixture-led-ui-direction-mockup",
                        "status": "promptable",
                        "usage": "Fixture filters, table, and selected-match rail.",
                        "aspect_ratios": ["16:10"],
                        "visual_scope": "design-reference-only",
                    },
                },
                {
                    "id": "visual-asset:fixture-context-raster",
                    "type": "GeneratedVisualAsset",
                    "label": "Fixture context raster",
                    "meta": {
                        "slot": "fixture-context-raster",
                        "status": "promptable",
                        "usage": "Secondary fixture context after the table.",
                        "aspect_ratios": ["3:2"],
                        "visual_scope": "secondary-runtime-support",
                    },
                },
                {
                    "id": "visual-asset:hero-image",
                    "type": "GeneratedVisualAsset",
                    "label": "Hero image",
                    "meta": {"slot": "hero-image", "status": "promptable"},
                },
                {
                    "id": "visual-asset:card-thumbnail",
                    "type": "GeneratedVisualAsset",
                    "label": "Card thumbnail",
                    "meta": {"slot": "card-thumbnail", "status": "promptable"},
                },
            ],
            "edges": [
                {
                    "type": "intended_for",
                    "source": "visual-asset:fixture-led-ui-direction-mockup",
                    "target": "component:schedule-table",
                },
                {
                    "type": "intended_for",
                    "source": "visual-asset:fixture-context-raster",
                    "target": "component:generated-visual-context",
                },
            ],
        }
        with tempfile.TemporaryDirectory() as tmp:
            project_dir = Path(tmp) / "world-cup-hub"
            reference_dir = project_dir / "design-system" / "references"
            reference_dir.mkdir(parents=True)
            reference = reference_dir / "selected-direction-03-fixture-compass.png"
            reference.write_bytes(b"fixture-direction-reference")

            packet = build_visual_prompt_packet(
                brand_profile=fixture_brand,
                blueprint=self.blueprint,
                ontology=fixture_ontology,
                project_dir=project_dir,
            )

        self.assertEqual(
            [slot["slot"] for slot in packet["slots"]],
            ["fixture-led-ui-direction-mockup", "fixture-context-raster"],
        )
        direction, context = packet["slots"]
        self.assertEqual(direction["visual_scope"], "design-reference-only")
        self.assertEqual(context["visual_scope"], "secondary-runtime-support")
        self.assertIn("fixture comparison table", direction["prompt"])
        self.assertIn("first viewport", direction["prompt"])
        self.assertIn("only after the fixture filters", context["prompt"])
        self.assertEqual(
            direction["design_references"][0]["path"],
            "design-system/references/selected-direction-03-fixture-compass.png",
        )
        self.assertEqual(
            direction["design_references"][0]["sha256"],
            sha256(b"fixture-direction-reference").hexdigest(),
        )

    def test_archives_and_migrates_final_prompt_contract_when_slot_becomes_legacy(self) -> None:
        old_packet = {
            "schema_version": PROMPT_PACKET_SCHEMA,
            "project": "fixture",
            "brand": "Fixture",
            "domain_context": "fixture monitoring",
            "slots": [{
                "id": "visual-asset:hero-image",
                "slot": "hero-image",
                "label": "Historic hero",
                "intended_for": ["component:generated-visual-context"],
                "aspect_ratios": ["16:9"],
                "candidate_count": 2,
                "prompt": "Historic command-center prompt",
                "review_criteria": ["subject is recognizable"],
                "generation": {"status": "ready", "api_fallback": "disabled"},
            }],
        }
        fixture_packet = {
            "schema_version": PROMPT_PACKET_SCHEMA,
            "project": "fixture",
            "brand": "Fixture",
            "domain_context": "fixture monitoring",
            "slots": [{
                "id": "visual-asset:fixture-led-ui-direction-mockup",
                "slot": "fixture-led-ui-direction-mockup",
                "label": "Fixture direction",
                "intended_for": ["component:schedule-table"],
                "aspect_ratios": ["16:10"],
                "candidate_count": 2,
                "prompt": "Fixture table and contextual rail prompt",
                "review_criteria": ["subject is recognizable"],
                "generation": {"status": "ready", "api_fallback": "disabled"},
                "visual_scope": "design-reference-only",
            }],
        }
        with tempfile.TemporaryDirectory() as tmp:
            output_dir = Path(tmp)
            old_result = write_visual_prompt_outputs(output_dir, old_packet)
            old_manifest = json.loads(old_result.manifest_path.read_text(encoding="utf-8"))
            hero = old_manifest["assets"][0]
            old_contract = {
                key: hero[key]
                for key in (
                    "prompt_packet_sha256",
                    "prompt_packet_slot_id",
                    "prompt_slot_sha256",
                    "prompt_summary",
                    "review_criteria",
                )
            }
            hero.update({
                "status": "accepted",
                "asset_path": "assets/historic.png",
                "original_png_path": "/tmp/historic.png",
                "format": "png",
                "dimensions": {"width": 1600, "height": 900},
                "size_kb": 1,
                "sha256": "a" * 64,
                "alt_text": "historic command center",
                "selection_reason": "reviewed historic asset",
                "reviewed_criteria": ["subject is recognizable"],
                "generation_provenance_version": "visual-asset-generation-provenance/v1",
                "generator": "image-model:codex-imagegen",
                "generation_run_id": "019e2de5-941b-7971-98e3-6ed84372f36b",
                "candidate_id": "ig_05e8553d24da513b016a07d77edabc8191bf7569ff5368de06",
            })
            old_manifest["assets"].append({
                "id": "visual-asset:card-thumbnail",
                "status": "planned",
                "acquisition_mode": "generated",
            })
            old_result.manifest_path.write_text(
                json.dumps(old_manifest), encoding="utf-8"
            )

            result = write_visual_prompt_outputs(output_dir, fixture_packet)
            manifest = json.loads(result.manifest_path.read_text(encoding="utf-8"))
            packet = json.loads(result.packet_path.read_text(encoding="utf-8"))
            migrated = next(
                item for item in manifest["assets"]
                if item["id"] == "visual-asset:hero-image"
            )

            self.assertEqual(
                [slot["id"] for slot in packet["slots"]],
                [
                    "visual-asset:fixture-led-ui-direction-mockup",
                    "visual-asset:hero-image",
                ],
            )
            legacy_slot = packet["slots"][1]
            self.assertFalse(legacy_slot["active_generation"])
            self.assertEqual(legacy_slot["visual_scope"], "legacy-supporting-asset")
            self.assertNotIn(
                "visual-asset:card-thumbnail",
                [item["id"] for item in manifest["assets"]],
            )
            self.assertEqual(migrated["lifecycle_role"], "legacy-supporting-asset")
            self.assertFalse(migrated["active_generation"])
            self.assertEqual(len(migrated["prompt_contract_migrations"]), 1)
            migration = migrated["prompt_contract_migrations"][0]
            self.assertEqual(migration["from"], old_contract)
            self.assertEqual(migration["to"]["prompt_packet_sha256"], manifest["prompt_packet_sha256"])
            archive = output_dir / migration["archive"]["path"]
            self.assertTrue(archive.is_file())
            self.assertEqual(
                sha256(archive.read_bytes()).hexdigest(),
                migration["archive"]["packet_sha256"],
            )

            write_visual_prompt_outputs(output_dir, fixture_packet)
            repeated = json.loads(result.manifest_path.read_text(encoding="utf-8"))
            repeated_hero = next(
                item for item in repeated["assets"]
                if item["id"] == "visual-asset:hero-image"
            )
            self.assertEqual(len(repeated_hero["prompt_contract_migrations"]), 1)

    def test_refuses_to_migrate_when_prior_packet_digest_is_not_truthful(self) -> None:
        old_packet = {
            "schema_version": PROMPT_PACKET_SCHEMA,
            "project": "fixture",
            "brand": "Fixture",
            "domain_context": "fixture monitoring",
            "slots": [{
                "id": "visual-asset:hero-image",
                "slot": "hero-image",
                "label": "Historic hero",
                "intended_for": ["component:generated-visual-context"],
                "aspect_ratios": ["16:9"],
                "candidate_count": 2,
                "prompt": "Historic command-center prompt",
                "review_criteria": ["subject is recognizable"],
            }],
        }
        fixture_packet = {**old_packet, "slots": []}
        with tempfile.TemporaryDirectory() as tmp:
            output_dir = Path(tmp)
            result = write_visual_prompt_outputs(output_dir, old_packet)
            manifest = json.loads(result.manifest_path.read_text(encoding="utf-8"))
            manifest["assets"][0]["status"] = "accepted"
            manifest["prompt_packet_sha256"] = "0" * 64
            result.manifest_path.write_text(json.dumps(manifest), encoding="utf-8")

            with self.assertRaisesRegex(ValueError, "does not match manifest.prompt_packet_sha256"):
                write_visual_prompt_outputs(output_dir, fixture_packet)


if __name__ == "__main__":
    unittest.main()
