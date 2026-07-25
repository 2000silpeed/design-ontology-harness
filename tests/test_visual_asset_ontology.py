import unittest
import tempfile
import json
import hashlib
from pathlib import Path

from PIL import Image

from design_ontology_harness.graph_builders import build_full_ontology_graph
from design_ontology_harness.graph_schema import EdgeType, NodeType
from design_ontology_harness.graph_spec_sections import build_graph_spec_sections
from design_ontology_harness.synthesis import (
    APP_ICON_IDENTITY_POLICY,
    COLOR_MODE_PARITY_POLICY,
    COMMERCIAL_PRODUCT_REALISM_POLICY,
    ICON_REFACTOR_POLICY,
    MOCKUP_VISUAL_SUBSTANCE_POLICY,
    REFERENCE_ABSORPTION_SCOPE,
    RESPONSIVE_RESILIENCE_POLICY,
    VISUAL_ASSET_MEDIUM_SELECTION_POLICY,
    discover_brand_identity_assets,
    discover_generated_visual_asset_manifests,
    load_brand_profile,
)


class VisualAssetOntologyTests(unittest.TestCase):
    def test_generated_visual_assets_are_modeled_for_codex_imagegen_without_api_fallback(self) -> None:
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

        model = graph.get_node("image-model:codex-imagegen")
        self.assertIsNotNone(model)
        self.assertEqual(model.type, NodeType.ImageGenerationModel)
        self.assertEqual(model.label, "Codex image_gen skill")
        self.assertEqual(model.meta["api_fallback"], "disabled")
        self.assertTrue(model.meta["workspace_copy_required"])
        self.assertEqual(model.meta["contract_id"], "governance:generated-visual-asset-contract")

        contract = graph.get_node("governance:generated-visual-asset-contract")
        self.assertIsNotNone(contract)
        self.assertEqual(contract.type, NodeType.GovernanceRule)
        self.assertEqual(contract.meta["schema_version"], "visual-asset-manifest/v2")
        self.assertIn("design-system/generated_visual_assets.json", contract.meta["compatible_manifest_paths"])
        self.assertIn("sha256", contract.meta["asset_record_required_fields"])
        self.assertIn("generation_run_id", contract.meta["asset_record_required_fields"])
        self.assertIn("candidate_id", contract.meta["asset_record_required_fields"])
        self.assertTrue(contract.meta["preserve_originals"])

        assets = graph.get_nodes_by_type(NodeType.GeneratedVisualAsset)
        asset_ids = {asset.id for asset in assets}
        self.assertIn("visual-asset:brand-aligned-raster", asset_ids)
        self.assertIn("visual-asset:hero-image", asset_ids)
        self.assertIn("visual-asset:card-thumbnail", asset_ids)
        self.assertIn("visual-asset:empty-state-illustration", asset_ids)

        hero = graph.get_node("visual-asset:hero-image")
        self.assertEqual(hero.meta["model"], "Codex image_gen skill")
        self.assertEqual(hero.meta["api_fallback"], "disabled")
        self.assertEqual(hero.meta["fallback_policy"], "no API fallback")
        self.assertIn("visual_reference_report.json", hero.meta["prompt_basis"])
        self.assertEqual(hero.meta["manifest_path"], "public/generated/design-system/manifest.json")
        self.assertEqual(hero.meta["prompt_pack_path"], "public/generated/design-system/imagegen-prompts.md")
        self.assertEqual(hero.meta["manifest_schema"], "visual-asset-manifest/v2")
        self.assertIn("original_png_path", hero.meta["asset_record_required_fields"])
        self.assertTrue(hero.meta["workspace_copy_required"])
        self.assertTrue(hero.meta["original_preservation_required"])

        model_edges = graph.get_edges_from("visual-asset:hero-image", EdgeType.generated_with)
        self.assertEqual(model_edges[0].target, "image-model:codex-imagegen")

        target_edges = graph.get_edges_from("visual-asset:hero-image", EdgeType.intended_for)
        self.assertIn("component:hero-section", {edge.target for edge in target_edges})

        governance_edges = graph.get_edges_from("governance:generated-visual-asset-contract", EdgeType.governs)
        self.assertIn("visual-asset:hero-image", {edge.target for edge in governance_edges})
        prevention_edges = graph.get_edges_from("governance:generated-visual-asset-contract", EdgeType.prevents)
        self.assertIn("failure-pattern:generated-image-untracked-asset", {edge.target for edge in prevention_edges})
        self.assertIn("failure-pattern:wrong-medium-svg-for-narrative-media", {edge.target for edge in prevention_edges})

    def test_fixture_led_product_gets_only_fixture_specific_promptable_slots(self) -> None:
        graph = build_full_ontology_graph(
            brand_profile={
                "brand_name": "World Cup Hub",
                "application_concept": {
                    "operating_mode": "fixture-monitoring-and-fan-participation",
                },
                "layout_skeleton": {
                    "composition": "fixture-led-command-desk-with-synchronized-match-rail",
                    "avoid_layouts": ["generic hero plus card grid"],
                },
            },
            blueprint={"principles": []},
            component_inventory={
                "families": [
                    {
                        "family": "navigation",
                        "components": ["app-shell"],
                    },
                    {
                        "family": "data-display",
                        "components": [
                            "schedule-table",
                            "match-detail-panel",
                            "generated-visual-context",
                            "result-summary-card",
                        ],
                    },
                ],
                "components": [
                    {"name": "app-shell", "family": "navigation"},
                    {"name": "schedule-table", "family": "data-display"},
                    {"name": "match-detail-panel", "family": "data-display"},
                    {
                        "name": "generated-visual-context",
                        "family": "data-display",
                    },
                    {"name": "result-summary-card", "family": "data-display"},
                ],
            },
            token_schema={"categories": {}},
        )

        promptable = {
            node.id: node
            for node in graph.get_nodes_by_type(NodeType.GeneratedVisualAsset)
            if node.meta.get("status") == "promptable"
        }
        self.assertEqual(
            set(promptable),
            {
                "visual-asset:fixture-led-ui-direction-mockup",
                "visual-asset:fixture-context-raster",
            },
        )
        direction = promptable["visual-asset:fixture-led-ui-direction-mockup"]
        context = promptable["visual-asset:fixture-context-raster"]
        self.assertEqual(direction.meta["visual_scope"], "design-reference-only")
        self.assertEqual(context.meta["visual_scope"], "secondary-runtime-support")
        self.assertIn("first viewport must", direction.meta["usage"])
        self.assertIn("may not contain a fake interface", context.meta["usage"])

        direction_targets = {
            edge.target
            for edge in graph.get_edges_from(direction.id, EdgeType.intended_for)
        }
        context_targets = {
            edge.target
            for edge in graph.get_edges_from(context.id, EdgeType.intended_for)
        }
        self.assertEqual(
            direction_targets,
            {
                "component:app-shell",
                "component:schedule-table",
                "component:match-detail-panel",
            },
        )
        self.assertEqual(context_targets, {"component:generated-visual-context"})

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
        self.assertIn("Codex image_gen skill", sections)
        self.assertIn("no API fallback", sections)
        self.assertIn("public/generated/design-system/manifest.json", sections)
        self.assertIn("visual-asset-manifest/v2", sections)
        self.assertIn("design-system/generated_visual_assets.json", sections)
        self.assertIn("workspace copy required", sections)

    def test_comic_visual_asset_slots_require_raster_medium(self) -> None:
        graph = build_full_ontology_graph(
            brand_profile={"brand_name": "Panel Pop"},
            blueprint={
                "principles": [],
                "governance": {
                    "visual_asset_medium_selection_policy": VISUAL_ASSET_MEDIUM_SELECTION_POLICY,
                },
            },
            component_inventory={
                "families": [{"family": "editorial", "components": ["comic-cover", "panel-preview"]}],
                "components": [
                    {
                        "name": "comic-cover",
                        "family": "editorial",
                        "role": "Comic magazine cover",
                        "supports_primitive": "webtoon cover art",
                    },
                    {
                        "name": "panel-preview",
                        "family": "editorial",
                        "role": "Manga panel preview",
                        "supports_primitive": "episode strip",
                    },
                ],
            },
            token_schema={"categories": {}},
        )

        cover = graph.get_node("visual-asset:comic-cover")
        panel = graph.get_node("visual-asset:comic-panel-preview")
        self.assertIsNotNone(cover)
        self.assertIsNotNone(panel)
        self.assertEqual(cover.meta["medium_role"], "high-fidelity-narrative-media")
        self.assertIn("image_gen", cover.meta["default_acquisition_modes"])
        self.assertIn("denied", cover.meta["deterministic_svg_allowed"])
        self.assertEqual(cover.meta["medium_selection_policy_id"], "governance:visual-asset-medium-selection")

        policy = graph.get_node("governance:visual-asset-medium-selection")
        self.assertIsNotNone(policy)
        self.assertTrue(any("Comic" in item or "comic" in item for item in policy.meta["implementation_rules"]))

        policy_edges = graph.get_edges_from("governance:visual-asset-medium-selection", EdgeType.enforces)
        self.assertIn("visual-asset:comic-cover", {edge.target for edge in policy_edges})
        self.assertIn("visual-asset:comic-panel-preview", {edge.target for edge in policy_edges})

        sections = build_graph_spec_sections(graph)
        self.assertIn("Medium selection", sections)
        self.assertIn("high-fidelity-narrative-media", sections)
        self.assertIn("Comic/manga cover art", sections)

    def test_sourced_visual_asset_fallback_is_modeled_with_license_policy(self) -> None:
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

        contract = graph.get_node("governance:sourced-visual-asset-fallback-contract")
        self.assertIsNotNone(contract)
        self.assertEqual(contract.type, NodeType.GovernanceRule)
        self.assertEqual(contract.meta["fallback_policy"], "license-verified sourced visual fallback")
        self.assertFalse(contract.meta["hotlinking_allowed"])
        self.assertIn("source_url", contract.meta["asset_record_required_fields"])
        self.assertIn("openverse", contract.meta["provider_allowlist"])

        provider = graph.get_node("visual-asset-provider:openverse")
        self.assertIsNotNone(provider)
        self.assertEqual(provider.type, NodeType.FreeSourcedVisualProvider)
        self.assertEqual(provider.meta["tier"], "free-sourced")
        self.assertTrue(provider.meta["license_metadata_required"])

        licensed_provider = graph.get_node("visual-asset-provider:adobe-stock")
        self.assertIsNotNone(licensed_provider)
        self.assertEqual(licensed_provider.type, NodeType.LicensedVisualProvider)
        self.assertTrue(licensed_provider.meta["license_proof_required"])

        reference_provider = graph.get_node("visual-asset-provider:lazyweb")
        self.assertIsNotNone(reference_provider)
        self.assertEqual(reference_provider.type, NodeType.ReferenceOnlyProvider)
        self.assertFalse(reference_provider.meta["asset_copy_allowed"])

        license_policy = graph.get_node("license-policy:verified-free-visual-asset")
        self.assertIsNotNone(license_policy)
        self.assertEqual(license_policy.type, NodeType.LicensePolicy)
        self.assertIn("unknown license", license_policy.meta["denied"])

        paid_policy = graph.get_node("license-policy:paid-visual-provider-proof")
        self.assertIsNotNone(paid_policy)
        self.assertIn("license_proof", paid_policy.meta["required_metadata"])

        reference_policy = graph.get_node("license-policy:reference-only-provider-no-runtime-assets")
        self.assertIsNotNone(reference_policy)
        self.assertIn("runtime image asset", reference_policy.meta["denied"])

        sourced = graph.get_node("sourced-visual-asset:hero-image-fallback")
        self.assertIsNotNone(sourced)
        self.assertEqual(sourced.type, NodeType.SourcedVisualAsset)
        self.assertEqual(sourced.meta["acquisition_mode"], "sourced")
        self.assertFalse(sourced.meta["hotlinking_allowed"])
        self.assertEqual(sourced.meta["candidate_manifest_path"], "public/generated/design-system/sourced-visual-candidates.json")

        provider_edges = graph.get_edges_from("sourced-visual-asset:hero-image-fallback", EdgeType.sourced_from)
        self.assertIn("visual-asset-provider:openverse", {edge.target for edge in provider_edges})

        license_edges = graph.get_edges_from("sourced-visual-asset:hero-image-fallback", EdgeType.licensed_under)
        self.assertIn("license-policy:verified-free-visual-asset", {edge.target for edge in license_edges})

        failure = graph.get_node("failure-pattern:unverified-search-image")
        self.assertIsNotNone(failure)
        self.assertEqual(failure.type, NodeType.ImplementationFailurePattern)

        sections = build_graph_spec_sections(graph)
        self.assertIn("Sourced fallback", sections)
        self.assertIn("Openverse", sections)
        self.assertIn("Licensed providers require proof", sections)
        self.assertIn("Reference-only providers", sections)
        self.assertIn("license metadata required", sections)
        self.assertIn("stock/search images are not valid identity assets", sections)

    def test_project_visual_asset_manifest_is_auto_discovered_from_brand_profile_path(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            project_dir = Path(tmp)
            generation_run_id = "019e2de5-941b-7971-98e3-6ed84372f36b"
            candidate_id = "ig_05e8553d24da513b016a07d77edabc8191bf7569ff5368de06"
            original_path = (
                project_dir
                / ".codex"
                / "generated_images"
                / generation_run_id
                / f"{candidate_id}.png"
            )
            original_path.parent.mkdir(parents=True)
            Image.new("RGB", (16, 9), "#20344a").save(original_path)
            (project_dir / "public" / "generated" / "design-system").mkdir(parents=True)
            (project_dir / "brand_profile.json").write_text(
                json.dumps({
                    "brand_name": "World Cup Hub",
                    "system_name": "World Cup Hub System",
                    "product_summary": "월드컵 허브",
                    "audiences": [],
                    "brand_keywords": [],
                    "anti_keywords": [],
                    "tone_of_voice": [],
                    "visual_keywords": [],
                    "interaction_keywords": [],
                    "platforms": ["web"],
                    "accessibility_targets": [],
                    "product_primitives": [],
                }),
                encoding="utf-8",
            )
            manifest = {
                "schema_version": "visual-asset-manifest/v2",
                "project": "world-cup-hub",
                "brand": "World Cup Hub",
                "generator": {"id": "image-model:codex-imagegen"},
                "source_session": {
                    "id": generation_run_id,
                    "default_directory": str(original_path.parent),
                    "preserve_originals": True,
                },
                "assets": [
                    {
                        "id": "visual-asset:world-cup-command-center",
                        "label": "World Cup command center",
                        "slot": "hero-image",
                        "status": "integrated",
                        "asset_path": "assets/world-cup-command-center.webp",
                        "original_png_path": str(original_path),
                        "original_sha256": hashlib.sha256(original_path.read_bytes()).hexdigest(),
                        "format": "webp",
                        "dimensions": {"width": 16, "height": 9, "aspect_ratio": "16:9"},
                        "size_kb": 1,
                        "sha256": "pending",
                        "intended_for": ["component:hero-board"],
                        "alt_text": "야간 경기장 커맨드 센터",
                        "prompt_summary": "World Cup dashboard hero image",
                        "generation_provenance_version": "visual-asset-generation-provenance/v1",
                        "generator": "image-model:codex-imagegen",
                        "generation_run_id": generation_run_id,
                        "candidate_id": candidate_id,
                    }
                ],
            }
            asset_path = project_dir / "assets" / "world-cup-command-center.webp"
            asset_path.parent.mkdir()
            Image.new("RGB", (16, 9), "#20344a").save(asset_path)
            manifest["assets"][0]["sha256"] = hashlib.sha256(asset_path.read_bytes()).hexdigest()
            manifest["assets"][0]["size_kb"] = round(asset_path.stat().st_size / 1024, 2)
            (project_dir / "public" / "generated" / "design-system" / "manifest.json").write_text(
                json.dumps(manifest),
                encoding="utf-8",
            )

            discovered = discover_generated_visual_asset_manifests(project_dir)
            self.assertEqual(len(discovered), 1)
            self.assertEqual(discovered[0]["path"], "public/generated/design-system/manifest.json")
            self.assertEqual(discovered[0]["assets"][0]["asset_path"], "assets/world-cup-command-center.webp")

            profile = load_brand_profile(project_dir / "brand_profile.json")
            self.assertIn("_generated_visual_asset_manifests", profile)
            self.assertEqual(
                profile["_generated_visual_asset_manifests"][0]["source_session"]["id"],
                generation_run_id,
            )

    def test_project_app_icon_is_auto_discovered_as_identity_asset(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            project_dir = Path(tmp)
            (project_dir / "assets").mkdir()
            (project_dir / "assets" / "app-icon.svg").write_text("<svg></svg>", encoding="utf-8")
            (project_dir / "site.webmanifest").write_text(
                json.dumps({"icons": [{"src": "./assets/app-icon.svg", "sizes": "any", "type": "image/svg+xml"}]}),
                encoding="utf-8",
            )

            discovered = discover_brand_identity_assets(project_dir)
            self.assertEqual(len(discovered), 1)
            self.assertEqual(discovered[0]["id"], "identity-asset:app-icon")
            self.assertEqual(discovered[0]["asset_path"], "assets/app-icon.svg")
            self.assertIn("web app manifest", discovered[0]["targets"])

            (project_dir / "brand_profile.json").write_text(
                json.dumps({
                    "brand_name": "World Cup Hub",
                    "system_name": "World Cup Hub System",
                    "product_summary": "월드컵 허브",
                    "audiences": [],
                    "brand_keywords": [],
                    "anti_keywords": [],
                    "tone_of_voice": [],
                    "visual_keywords": [],
                    "interaction_keywords": [],
                    "platforms": ["web"],
                    "accessibility_targets": [],
                    "product_primitives": [],
                }),
                encoding="utf-8",
            )
            profile = load_brand_profile(project_dir / "brand_profile.json")
            self.assertEqual(profile["_identity_assets"][0]["asset_path"], "assets/app-icon.svg")

    def test_invalid_visual_manifest_exposes_discovery_issues(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            project_dir = Path(tmp)
            manifest_path = project_dir / "public" / "generated" / "design-system" / "manifest.json"
            manifest_path.parent.mkdir(parents=True)
            manifest_path.write_text("{invalid", encoding="utf-8")
            (project_dir / "brand_profile.json").write_text(
                json.dumps({
                    "brand_name": "Fieldnote",
                    "brand_keywords": [],
                    "anti_keywords": [],
                    "product_primitives": [],
                }),
                encoding="utf-8",
            )

            profile = load_brand_profile(project_dir / "brand_profile.json")

            self.assertNotIn("_generated_visual_asset_manifests", profile)
            self.assertTrue(profile["_generated_visual_asset_manifest_issues"])
            self.assertIn("invalid JSON", profile["_generated_visual_asset_manifest_issues"][0])

    def test_discovered_manifest_assets_are_promoted_to_graph_and_spec(self) -> None:
        manifest = {
            "path": "public/generated/design-system/manifest.json",
            "schema_version": "visual-asset-manifest/v1",
            "project": "world-cup-hub",
            "brand": "World Cup Hub",
            "source_session": {"id": "session-1", "default_directory": "/Users/example/.codex/generated_images/session-1"},
            "assets": [
                {
                    "id": "visual-asset:world-cup-command-center",
                    "label": "World Cup command center",
                    "slot": "hero-image",
                    "status": "integrated",
                    "asset_path": "assets/world-cup-command-center.webp",
                    "original_png_path": "/Users/example/.codex/generated_images/session-1/source.png",
                    "format": "webp",
                    "dimensions": {"width": 1672, "height": 941, "aspect_ratio": "16:9"},
                    "size_kb": 188,
                    "sha256": "abc123",
                    "intended_for": ["component:hero-board"],
                    "alt_text": "야간 경기장 커맨드 센터",
                    "prompt_summary": "World Cup dashboard hero image",
                    "visual_scope": "legacy-supporting-asset",
                    "active_generation": False,
                    "lifecycle_role": "legacy-supporting-asset",
                    "prompt_contract_migrations": [{"schema_version": "visual-asset-prompt-contract-migration/v1"}],
                }
            ],
        }
        graph = build_full_ontology_graph(
            brand_profile={
                "brand_name": "World Cup Hub",
                "_generated_visual_asset_manifests": [manifest],
            },
            blueprint={"principles": [], "generated_visual_assets": [manifest]},
            component_inventory={
                "families": [{"family": "marketing", "components": ["hero-board"]}],
                "components": [{"name": "hero-board", "family": "marketing", "role": "Hero board"}],
            },
            token_schema={"categories": {}},
        )

        asset = graph.get_node("visual-asset:world-cup-command-center")
        self.assertIsNotNone(asset)
        self.assertEqual(asset.type, NodeType.GeneratedVisualAsset)
        self.assertTrue(asset.meta["integrated"])
        self.assertEqual(asset.meta["asset_path"], "assets/world-cup-command-center.webp")
        self.assertEqual(asset.meta["alt_text"], "야간 경기장 커맨드 센터")
        self.assertEqual(asset.meta["source_session_id"], "session-1")
        self.assertEqual(asset.meta["visual_scope"], "legacy-supporting-asset")
        self.assertFalse(asset.meta["active_generation"])
        self.assertEqual(asset.meta["lifecycle_role"], "legacy-supporting-asset")
        self.assertEqual(
            asset.meta["prompt_contract_migrations"][0]["schema_version"],
            "visual-asset-prompt-contract-migration/v1",
        )

        target_edges = graph.get_edges_from("visual-asset:world-cup-command-center", EdgeType.intended_for)
        self.assertIn("component:hero-board", {edge.target for edge in target_edges})

        sections = build_graph_spec_sections(graph)
        self.assertIn("Integrated Assets", sections)
        self.assertIn("assets/world-cup-command-center.webp", sections)
        self.assertIn("야간 경기장 커맨드 센터", sections)

    def test_planned_manifest_assets_are_not_promoted_as_integrated(self) -> None:
        manifest = {
            "path": "public/generated/design-system/manifest.json",
            "schema_version": "visual-asset-manifest/v1",
            "project": "fieldnote",
            "brand": "Fieldnote",
            "assets": [{
                "id": "visual-asset:planned-only",
                "label": "Planned only",
                "slot": "hero-image",
                "status": "planned",
                "asset_path": None,
            }],
        }
        graph = build_full_ontology_graph(
            brand_profile={"brand_name": "Fieldnote", "_generated_visual_asset_manifests": [manifest]},
            blueprint={"principles": [], "generated_visual_assets": [manifest]},
            component_inventory={"families": [], "components": []},
            token_schema={"categories": {}},
        )

        self.assertIsNone(graph.get_node("visual-asset:planned-only"))

    def test_sourced_manifest_assets_are_promoted_to_graph_and_spec(self) -> None:
        manifest = {
            "path": "public/generated/design-system/manifest.json",
            "schema_version": "visual-asset-manifest/v1",
            "project": "world-cup-hub",
            "brand": "World Cup Hub",
            "assets": [
                {
                    "id": "sourced-visual-asset:stadium-entrance-photo",
                    "label": "Stadium entrance photo",
                    "slot": "card-thumbnail",
                    "status": "integrated",
                    "acquisition_mode": "sourced",
                    "asset_path": "assets/stadium-entrance.webp",
                    "source_url": "https://openverse.org/image/example",
                    "download_url": "https://images.example/stadium.jpg",
                    "provider": "openverse",
                    "author": "Example Photographer",
                    "license": {"id": "cc0", "label": "CC0"},
                    "attribution_required": False,
                    "retrieved_at": "2026-05-17",
                    "format": "webp",
                    "dimensions": {"width": 1200, "height": 900, "aspect_ratio": "4:3"},
                    "size_kb": 144,
                    "sha256": "def456",
                    "intended_for": ["component:venue-card"],
                    "alt_text": "경기장 출입구 외부 사진",
                    "selection_reason": "Real-world venue texture for a match card.",
                }
            ],
        }
        graph = build_full_ontology_graph(
            brand_profile={
                "brand_name": "World Cup Hub",
                "_generated_visual_asset_manifests": [manifest],
            },
            blueprint={"principles": [], "generated_visual_assets": [manifest]},
            component_inventory={
                "families": [{"family": "marketing", "components": ["venue-card"]}],
                "components": [{"name": "venue-card", "family": "marketing", "role": "Venue card"}],
            },
            token_schema={"categories": {}},
        )

        asset = graph.get_node("sourced-visual-asset:stadium-entrance-photo")
        self.assertIsNotNone(asset)
        self.assertEqual(asset.type, NodeType.SourcedVisualAsset)
        self.assertTrue(asset.meta["integrated"])
        self.assertEqual(asset.meta["acquisition_mode"], "sourced")
        self.assertEqual(asset.meta["asset_path"], "assets/stadium-entrance.webp")
        self.assertEqual(asset.meta["source_url"], "https://openverse.org/image/example")
        self.assertEqual(asset.meta["provider"], "openverse")
        self.assertEqual(asset.meta["license"], "CC0")
        self.assertFalse(asset.meta["hotlinking_allowed"])

        provider_edges = graph.get_edges_from("sourced-visual-asset:stadium-entrance-photo", EdgeType.sourced_from)
        self.assertIn("visual-asset-provider:openverse", {edge.target for edge in provider_edges})

        license_edges = graph.get_edges_from("sourced-visual-asset:stadium-entrance-photo", EdgeType.licensed_under)
        self.assertIn("license-policy:verified-free-visual-asset", {edge.target for edge in license_edges})
        self.assertIn("license-policy:cc0", {edge.target for edge in license_edges})

        target_edges = graph.get_edges_from("sourced-visual-asset:stadium-entrance-photo", EdgeType.intended_for)
        self.assertIn("component:venue-card", {edge.target for edge in target_edges})

        sections = build_graph_spec_sections(graph)
        self.assertIn("Integrated Assets", sections)
        self.assertIn("sourced", sections)
        self.assertIn("assets/stadium-entrance.webp", sections)
        self.assertIn("https://openverse.org/image/example", sections)
        self.assertIn("경기장 출입구 외부 사진", sections)

    def test_paid_provider_manifest_requires_license_proof_policy(self) -> None:
        manifest = {
            "path": "public/generated/design-system/manifest.json",
            "schema_version": "visual-asset-manifest/v1",
            "project": "brand-site",
            "brand": "Brand Site",
            "assets": [
                {
                    "id": "sourced-visual-asset:licensed-hero-photo",
                    "label": "Licensed hero photo",
                    "slot": "hero-image",
                    "status": "integrated",
                    "acquisition_mode": "sourced",
                    "asset_path": "assets/licensed-hero.webp",
                    "source_url": "https://stock.adobe.com/images/example",
                    "download_url": "https://stock.adobe.com/download/example",
                    "provider": "adobe-stock",
                    "author": "Stock Photographer",
                    "license": "Adobe Stock Standard License",
                    "license_proof": "adobe-stock-license-123",
                    "usage_scope": "website mockup",
                    "licensed_to": "Brand Site",
                    "attribution_required": False,
                    "retrieved_at": "2026-05-17",
                    "sha256": "abc456",
                    "intended_for": ["component:hero-section"],
                    "alt_text": "브랜드 사이트 히어로 이미지",
                    "selection_reason": "Production-grade licensed stock for a hero.",
                }
            ],
        }
        graph = build_full_ontology_graph(
            brand_profile={"brand_name": "Brand Site", "_generated_visual_asset_manifests": [manifest]},
            blueprint={"principles": [], "generated_visual_assets": [manifest]},
            component_inventory={
                "families": [{"family": "marketing", "components": ["hero-section"]}],
                "components": [{"name": "hero-section", "family": "marketing", "role": "Hero"}],
            },
            token_schema={"categories": {}},
        )

        asset = graph.get_node("sourced-visual-asset:licensed-hero-photo")
        self.assertIsNotNone(asset)
        self.assertEqual(asset.type, NodeType.SourcedVisualAsset)
        self.assertEqual(asset.meta["provider_tier"], "licensed")
        self.assertTrue(asset.meta["license_proof_required"])
        self.assertEqual(asset.meta["license_proof"], "adobe-stock-license-123")

        provider = graph.get_node("visual-asset-provider:adobe-stock")
        self.assertIsNotNone(provider)
        self.assertEqual(provider.type, NodeType.LicensedVisualProvider)

        license_edges = graph.get_edges_from("sourced-visual-asset:licensed-hero-photo", EdgeType.licensed_under)
        self.assertIn("license-policy:paid-visual-provider-proof", {edge.target for edge in license_edges})

    def test_feedback_failure_patterns_are_promoted_to_governance_nodes(self) -> None:
        graph = build_full_ontology_graph(
            brand_profile={
                "brand_name": "Mercer",
                "_identity_assets": [
                    {
                        "id": "identity-asset:app-icon",
                        "label": "Mercer app icon",
                        "slot": "app-icon",
                        "asset_path": "assets/app-icon.svg",
                        "format": "svg",
                        "targets": ["favicon", "app shell brand mark", "web app manifest"],
                        "integrated": True,
                    }
                ],
            },
            blueprint={
                "principles": [],
                "governance": {
                    "reference_absorption_scope": REFERENCE_ABSORPTION_SCOPE,
                    "color_mode_parity_policy": COLOR_MODE_PARITY_POLICY,
                    "responsive_resilience_policy": RESPONSIVE_RESILIENCE_POLICY,
                    "icon_refactor_policy": ICON_REFACTOR_POLICY,
                    "app_icon_identity_policy": APP_ICON_IDENTITY_POLICY,
                    "mockup_visual_substance_policy": MOCKUP_VISUAL_SUBSTANCE_POLICY,
                    "visual_asset_medium_selection_policy": VISUAL_ASSET_MEDIUM_SELECTION_POLICY,
                    "commercial_product_realism_policy": COMMERCIAL_PRODUCT_REALISM_POLICY,
                    "feedback_promotion_policy": REFERENCE_ABSORPTION_SCOPE["promotion_policy"],
                },
            },
            component_inventory={"families": [], "components": []},
            token_schema={"categories": {}},
        )

        scope = graph.get_node("governance:reference-absorption-scope")
        self.assertIsNotNone(scope)
        self.assertEqual(scope.type, NodeType.GovernanceRule)
        self.assertIn("palette composition or derived secondary palettes", scope.meta["denied"])

        failure = graph.get_node("failure-pattern:token-bound-reference-palette-mixing")
        self.assertIsNotNone(failure)
        self.assertEqual(failure.type, NodeType.ImplementationFailurePattern)
        self.assertTrue(any("DS030" in item for item in failure.meta["technical_controls"]))

        prevention_edges = graph.get_edges_from("governance:reference-absorption-scope", EdgeType.prevents)
        self.assertIn("failure-pattern:token-bound-reference-palette-mixing", {edge.target for edge in prevention_edges})

        responsive = graph.get_node("governance:responsive-resilience")
        self.assertIsNotNone(responsive)
        self.assertEqual(responsive.type, NodeType.GovernanceRule)
        self.assertIn(320, responsive.meta["viewport_contract"]["required_widths_px"])
        self.assertTrue(any("Horizontal rails" in item for item in responsive.meta["control_rules"]))

        mobile_overflow = graph.get_node("failure-pattern:mobile-control-overflow")
        self.assertIsNotNone(mobile_overflow)
        self.assertEqual(mobile_overflow.type, NodeType.ImplementationFailurePattern)
        self.assertTrue(any("DS040" in item for item in mobile_overflow.meta["technical_controls"]))

        rail_clipping = graph.get_node("failure-pattern:horizontal-rail-label-clipping")
        self.assertIsNotNone(rail_clipping)
        self.assertEqual(rail_clipping.type, NodeType.ImplementationFailurePattern)
        self.assertTrue(any("scrollWidth<=clientWidth" in item for item in rail_clipping.meta["technical_controls"]))

        responsive_edges = graph.get_edges_from("governance:responsive-resilience", EdgeType.prevents)
        self.assertIn("failure-pattern:mobile-control-overflow", {edge.target for edge in responsive_edges})
        self.assertIn("failure-pattern:horizontal-rail-label-clipping", {edge.target for edge in responsive_edges})

        color_mode_policy = graph.get_node("governance:color-mode-parity")
        self.assertIsNotNone(color_mode_policy)
        self.assertEqual(color_mode_policy.type, NodeType.GovernanceRule)
        self.assertEqual(color_mode_policy.meta["default_mode"], "light")

        light_mode = graph.get_node("color-mode:light")
        dark_mode = graph.get_node("color-mode:dark")
        self.assertIsNotNone(light_mode)
        self.assertIsNotNone(dark_mode)
        self.assertEqual(light_mode.type, NodeType.ColorMode)
        self.assertTrue(light_mode.meta["default"])
        self.assertFalse(dark_mode.meta["default"])

        dark_only_failure = graph.get_node("failure-pattern:dark-only-implementation")
        self.assertIsNotNone(dark_only_failure)
        self.assertEqual(dark_only_failure.type, NodeType.ImplementationFailurePattern)

        color_mode_edges = graph.get_edges_from("governance:color-mode-parity", EdgeType.prevents)
        self.assertIn("failure-pattern:dark-only-implementation", {edge.target for edge in color_mode_edges})

        icon_policy = graph.get_node("governance:emoji-to-svg-refactor")
        self.assertIsNotNone(icon_policy)
        self.assertEqual(icon_policy.type, NodeType.GovernanceRule)
        self.assertIn("button", icon_policy.meta["targets"])
        self.assertIn("Lucide", icon_policy.meta["quality_floor"]["approved_sources"])

        emoji_failure = graph.get_node("failure-pattern:emoji-ui-affordance")
        self.assertIsNotNone(emoji_failure)
        self.assertEqual(emoji_failure.type, NodeType.ImplementationFailurePattern)
        self.assertTrue(any("DS050" in item for item in emoji_failure.meta["technical_controls"]))

        handmade_icon_failure = graph.get_node("failure-pattern:amateur-custom-svg-icon-set")
        self.assertIsNotNone(handmade_icon_failure)
        self.assertEqual(handmade_icon_failure.type, NodeType.ImplementationFailurePattern)
        self.assertTrue(any("DS080" in item for item in handmade_icon_failure.meta["technical_controls"]))

        icon_edges = graph.get_edges_from("governance:emoji-to-svg-refactor", EdgeType.prevents)
        self.assertIn("failure-pattern:emoji-ui-affordance", {edge.target for edge in icon_edges})
        self.assertIn("failure-pattern:amateur-custom-svg-icon-set", {edge.target for edge in icon_edges})

        app_icon_policy = graph.get_node("governance:brand-app-icon-identity")
        self.assertIsNotNone(app_icon_policy)
        self.assertEqual(app_icon_policy.type, NodeType.GovernanceRule)
        self.assertTrue(any("deterministic SVG" in item for item in app_icon_policy.meta["implementation_rules"]))

        app_icon = graph.get_node("identity-asset:app-icon")
        self.assertIsNotNone(app_icon)
        self.assertEqual(app_icon.type, NodeType.BrandIdentityAsset)
        self.assertTrue(app_icon.meta["required"])
        self.assertTrue(app_icon.meta["integrated"])
        self.assertEqual(app_icon.meta["asset_path"], "assets/app-icon.svg")
        self.assertIn("favicon", app_icon.meta["targets"])

        app_icon_failure = graph.get_node("failure-pattern:generic-initials-app-icon")
        self.assertIsNotNone(app_icon_failure)
        self.assertEqual(app_icon_failure.type, NodeType.ImplementationFailurePattern)

        app_icon_edges = graph.get_edges_from("governance:brand-app-icon-identity", EdgeType.prevents)
        self.assertIn("failure-pattern:generic-initials-app-icon", {edge.target for edge in app_icon_edges})

        visual_policy = graph.get_node("governance:mockup-visual-substance")
        self.assertIsNotNone(visual_policy)
        self.assertEqual(visual_policy.type, NodeType.GovernanceRule)
        self.assertTrue(any("visual asset" in item for item in visual_policy.meta["required_signals"]))
        self.assertTrue(any("image_gen" in item for item in visual_policy.meta["image_acquisition_order"]))

        image_free_failure = graph.get_node("failure-pattern:image-free-commercial-mockup")
        self.assertIsNotNone(image_free_failure)
        self.assertEqual(image_free_failure.type, NodeType.ImplementationFailurePattern)
        self.assertTrue(any("Mockup Visual Substance" in item for item in image_free_failure.meta["technical_controls"]))

        placeholder_failure = graph.get_node("failure-pattern:placeholder-gradient-as-image")
        self.assertIsNotNone(placeholder_failure)
        self.assertEqual(placeholder_failure.type, NodeType.ImplementationFailurePattern)

        visual_edges = graph.get_edges_from("governance:mockup-visual-substance", EdgeType.prevents)
        self.assertIn("failure-pattern:image-free-commercial-mockup", {edge.target for edge in visual_edges})
        self.assertIn("failure-pattern:placeholder-gradient-as-image", {edge.target for edge in visual_edges})

        visual_medium_policy = graph.get_node("governance:visual-asset-medium-selection")
        self.assertIsNotNone(visual_medium_policy)
        self.assertEqual(visual_medium_policy.type, NodeType.GovernanceRule)
        self.assertTrue(any(item["id"] == "user-raster-asset-directive" for item in visual_medium_policy.meta["directive_overrides"]))
        raster_override = next(
            item for item in visual_medium_policy.meta["directive_overrides"]
            if item["id"] == "user-raster-asset-directive"
        )
        self.assertEqual(raster_override["required_medium"], "project-local raster image asset")
        self.assertIn("svg", raster_override["denied_formats"])
        self.assertTrue(any("Classify the slot" in item for item in visual_medium_policy.meta["decision_sequence"]))
        self.assertTrue(any(item["id"] == "high-fidelity-narrative-media" for item in visual_medium_policy.meta["slot_families"]))
        self.assertTrue(any(item["id"] == "user-specified-raster-assets" for item in visual_medium_policy.meta["slot_families"]))

        wrong_medium_failure = graph.get_node("failure-pattern:wrong-medium-svg-for-narrative-media")
        self.assertIsNotNone(wrong_medium_failure)
        self.assertEqual(wrong_medium_failure.type, NodeType.ImplementationFailurePattern)
        self.assertTrue(any("DS079" in item for item in wrong_medium_failure.meta["technical_controls"]))

        raster_directive_failure = graph.get_node("failure-pattern:user-raster-directive-svg-violation")
        self.assertIsNotNone(raster_directive_failure)
        self.assertEqual(raster_directive_failure.type, NodeType.ImplementationFailurePattern)
        self.assertTrue(any("DS081" in item for item in raster_directive_failure.meta["technical_controls"]))

        medium_edges = graph.get_edges_from("governance:visual-asset-medium-selection", EdgeType.prevents)
        self.assertIn("failure-pattern:wrong-medium-svg-for-narrative-media", {edge.target for edge in medium_edges})
        self.assertIn("failure-pattern:user-raster-directive-svg-violation", {edge.target for edge in medium_edges})

        realism_policy = graph.get_node("governance:commercial-product-realism")
        self.assertIsNotNone(realism_policy)
        self.assertEqual(realism_policy.type, NodeType.GovernanceRule)
        self.assertIn("first-viewport task surface", realism_policy.meta["required_signals"])
        self.assertTrue(any("national flag identity marks" in item for item in realism_policy.meta["required_signals"]))
        self.assertTrue(any("reference-backed domain morphology" in item for item in realism_policy.meta["required_signals"]))
        successful_pattern_ids = {item["id"] for item in realism_policy.meta["successful_patterns"]}
        self.assertIn("same-domain-reference-before-redesign", successful_pattern_ids)
        self.assertIn("score-ticker-as-scan-surface", successful_pattern_ids)
        self.assertIn("national-flag-code-identity", successful_pattern_ids)
        self.assertIn("source-ledger-and-sample-labeling", successful_pattern_ids)
        self.assertIn("editorial-insight-side-rail", successful_pattern_ids)
        self.assertIn("dual-mode-screenshot-qa", successful_pattern_ids)
        self.assertIn("brand-app-icon-as-required-identity", successful_pattern_ids)
        self.assertTrue(any("country-based sports competitions" in item for item in realism_policy.meta["implementation_rules"]))
        self.assertTrue(any("Flag colors and domain identity marks" in item for item in realism_policy.meta["implementation_rules"]))
        self.assertTrue(any("same-domain commercial references" in item for item in realism_policy.meta["implementation_rules"]))

        pitch_deck_failure = graph.get_node("failure-pattern:pitch-deck-dashboard-shell")
        self.assertIsNotNone(pitch_deck_failure)
        self.assertEqual(pitch_deck_failure.type, NodeType.ImplementationFailurePattern)
        self.assertTrue(any("Commercial Product Realism" in item for item in pitch_deck_failure.meta["technical_controls"]))

        reference_free_failure = graph.get_node("failure-pattern:reference-free-realism-refactor")
        self.assertIsNotNone(reference_free_failure)
        self.assertEqual(reference_free_failure.type, NodeType.ImplementationFailurePattern)
        self.assertTrue(any("Reference Intelligence" in item for item in reference_free_failure.meta["technical_controls"]))

        generic_badge_failure = graph.get_node("failure-pattern:generic-national-team-badges")
        self.assertIsNotNone(generic_badge_failure)
        self.assertEqual(generic_badge_failure.type, NodeType.ImplementationFailurePattern)
        self.assertTrue(any("icon_refactor_policy" in item for item in generic_badge_failure.meta["technical_controls"]))

        untokenized_identity_failure = graph.get_node("failure-pattern:untokenized-domain-identity-colors")
        self.assertIsNotNone(untokenized_identity_failure)
        self.assertEqual(untokenized_identity_failure.type, NodeType.ImplementationFailurePattern)
        self.assertTrue(any("DS003" in item for item in untokenized_identity_failure.meta["technical_controls"]))

        realism_edges = graph.get_edges_from("governance:commercial-product-realism", EdgeType.prevents)
        self.assertIn("failure-pattern:pitch-deck-dashboard-shell", {edge.target for edge in realism_edges})
        self.assertIn("failure-pattern:reference-free-realism-refactor", {edge.target for edge in realism_edges})
        self.assertIn("failure-pattern:generic-national-team-badges", {edge.target for edge in realism_edges})
        self.assertIn("failure-pattern:untokenized-domain-identity-colors", {edge.target for edge in realism_edges})

        sections = build_graph_spec_sections(graph)
        self.assertIn("Color Mode Parity", sections)
        self.assertIn("dark-only-implementation", sections)
        self.assertIn("Brand Identity Assets", sections)
        self.assertIn("Mercer app icon", sections)
        self.assertIn("assets/app-icon.svg", sections)
        self.assertIn("generic-initials-app-icon", sections)
        self.assertIn("Mockup Visual Substance", sections)
        self.assertIn("image-free-commercial-mockup", sections)
        self.assertIn("placeholder-gradient-as-image", sections)
        self.assertIn("Visual Asset Medium Selection", sections)
        self.assertIn("wrong-medium-svg-for-narrative-media", sections)
        self.assertIn("user-raster-asset-directive", sections)
        self.assertIn("user-raster-directive-svg-violation", sections)
        self.assertIn("Commercial Product Realism", sections)
        self.assertIn("pitch-deck-dashboard-shell", sections)
        self.assertIn("reference-free-realism-refactor", sections)
        self.assertIn("generic-national-team-badges", sections)
        self.assertIn("Successful reusable patterns", sections)
        self.assertIn("score-ticker-as-scan-surface", sections)
        self.assertIn("national-flag-code-identity", sections)
        self.assertIn("untokenized-domain-identity-colors", sections)


if __name__ == "__main__":
    unittest.main()
