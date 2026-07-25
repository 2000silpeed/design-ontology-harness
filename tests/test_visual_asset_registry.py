from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from PIL import Image

from design_ontology_harness.visual_asset_prompts import write_visual_prompt_outputs
from design_ontology_harness.visual_asset_registry import (
    promote_generated_visual_asset,
    register_generated_visual_asset,
    validate_visual_asset_manifest,
)


class VisualAssetRegistryTests(unittest.TestCase):
    generation_run_id = "019e2de5-941b-7971-98e3-6ed84372f36b"
    candidate_id = "ig_05e8553d24da513b016a07d77edabc8191bf7569ff5368de06"

    def _write_generated_png(
        self,
        root: Path,
        *,
        size: tuple[int, int] = (1600, 900),
        color: str = "#315c4b",
    ) -> Path:
        path = (
            root
            / ".codex"
            / "generated_images"
            / self.generation_run_id
            / f"{self.candidate_id}.png"
        )
        path.parent.mkdir(parents=True, exist_ok=True)
        Image.new("RGB", size, color).save(path)
        return path

    def _write_component_contracts(self, project_dir: Path, *names: str) -> None:
        inventory_path = project_dir / "build" / "system" / "blueprint" / "component_inventory.json"
        specs_path = project_dir / "build" / "system" / "components" / "component_specs.json"
        inventory_path.parent.mkdir(parents=True, exist_ok=True)
        specs_path.parent.mkdir(parents=True, exist_ok=True)
        inventory_path.write_text(
            json.dumps({"components": [{"name": name} for name in names]}),
            encoding="utf-8",
        )
        specs_path.write_text(
            json.dumps({
                "specs": [
                    {"name": name, "contract_status": "complete"}
                    for name in names
                ]
            }),
            encoding="utf-8",
        )

    def _packet(self) -> dict:
        return {
            "schema_version": "design-ontology.visual-prompt-packet.v1",
            "project": "fieldnote",
            "brand": "Fieldnote",
            "domain_context": "field evidence review",
            "slots": [{
                "id": "visual-asset:evidence-hero",
                "slot": "hero-image",
                "label": "Evidence hero",
                "intended_for": ["component:evidence-board"],
                "aspect_ratios": ["16:9"],
                "candidate_count": 2,
                "prompt": "Credible field evidence review scene",
                "review_criteria": ["domain subject is clear"],
            }],
        }

    def test_registers_workspace_copy_and_validates_metadata(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            project_dir = Path(tmp) / "fieldnote"
            output_dir = project_dir / "public" / "generated" / "design-system"
            result = write_visual_prompt_outputs(output_dir, self._packet())
            source = self._write_generated_png(Path(tmp))

            registered = register_generated_visual_asset(
                project_dir=project_dir,
                manifest_path=result.manifest_path,
                asset_id="visual-asset:evidence-hero",
                source_path=source,
                alt_text="현장 증거 자료를 검토하는 작업 화면",
                selection_reason="가장 명확한 현장 증거 구도",
                reviewed_criteria=["domain subject is clear", "responsive crop is safe"],
                session_id=self.generation_run_id,
            )
            self.assertEqual(registered.status, "accepted")
            self._write_component_contracts(project_dir, "evidence-board")
            (project_dir / "index.html").write_text(
                f'<main><img src="./{registered.asset_path.relative_to(project_dir).as_posix()}" '
                'alt="현장 증거 자료를 검토하는 작업 화면" /></main>',
                encoding="utf-8",
            )

            promoted = promote_generated_visual_asset(
                project_dir=project_dir,
                manifest_path=result.manifest_path,
                asset_id="visual-asset:evidence-hero",
            )
            report = validate_visual_asset_manifest(
                result.manifest_path,
                project_dir=project_dir,
                require_integrated=True,
            )
            manifest = json.loads(result.manifest_path.read_text(encoding="utf-8"))
            record = manifest["assets"][0]

            self.assertTrue(report["ok"], report["errors"])
            self.assertTrue(registered.asset_path.is_file())
            self.assertEqual(promoted.status, "integrated")
            self.assertEqual(record["status"], "integrated")
            self.assertEqual(record["dimensions"]["aspect_ratio"], "16:9")
            self.assertEqual(record["sha256"], registered.sha256)
            self.assertEqual(manifest["schema_version"], "visual-asset-manifest/v2")
            self.assertEqual(manifest["source_session"]["id"], self.generation_run_id)
            self.assertEqual(
                record["generation_provenance_version"],
                "visual-asset-generation-provenance/v1",
            )
            self.assertEqual(record["generator"], "image-model:codex-imagegen")
            self.assertEqual(record["generation_run_id"], self.generation_run_id)
            self.assertEqual(record["candidate_id"], self.candidate_id)
            self.assertEqual(record["runtime_integration"]["gate"], "implementation-reference/v1")
            self.assertTrue(record["runtime_integration"]["references"])
            self.assertFalse(Path(record["asset_path"]).is_absolute())

    def test_rejects_fabricated_generation_provenance(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            project_dir = Path(tmp) / "fieldnote"
            result = write_visual_prompt_outputs(
                project_dir / "public" / "generated" / "design-system",
                self._packet(),
            )
            source = self._write_generated_png(Path(tmp))
            register_generated_visual_asset(
                project_dir=project_dir,
                manifest_path=result.manifest_path,
                asset_id="visual-asset:evidence-hero",
                source_path=source,
                alt_text="현장 증거 자료",
                selection_reason="도메인 정보가 가장 선명함",
                reviewed_criteria=["domain subject is clear"],
                session_id=self.generation_run_id,
            )
            manifest = json.loads(result.manifest_path.read_text(encoding="utf-8"))
            record = manifest["assets"][0]
            record["generator"] = "user-authored:plausible-generator"
            record["generation_run_id"] = "019e2de5-941b-7971-98e3-000000000000"
            record["candidate_id"] = "ig_" + "0" * 50
            result.manifest_path.write_text(json.dumps(manifest), encoding="utf-8")

            report = validate_visual_asset_manifest(
                result.manifest_path,
                project_dir=project_dir,
            )

            self.assertFalse(report["ok"])
            self.assertTrue(any(".generator must be" in error for error in report["errors"]))
            self.assertTrue(any("generation_run_id does not match" in error for error in report["errors"]))
            self.assertTrue(any("candidate_id does not match" in error for error in report["errors"]))

    def test_legacy_generated_final_asset_fails_closed_without_provenance(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            project_dir = Path(tmp) / "fieldnote"
            result = write_visual_prompt_outputs(
                project_dir / "public" / "generated" / "design-system",
                self._packet(),
            )
            source = self._write_generated_png(Path(tmp))
            register_generated_visual_asset(
                project_dir=project_dir,
                manifest_path=result.manifest_path,
                asset_id="visual-asset:evidence-hero",
                source_path=source,
                alt_text="현장 증거 자료",
                selection_reason="도메인 정보가 가장 선명함",
                reviewed_criteria=["domain subject is clear"],
                session_id=self.generation_run_id,
            )
            manifest = json.loads(result.manifest_path.read_text(encoding="utf-8"))
            manifest["schema_version"] = "visual-asset-manifest/v1"
            for field in (
                "generation_provenance_version",
                "generator",
                "generation_run_id",
                "candidate_id",
            ):
                manifest["assets"][0].pop(field)
            result.manifest_path.write_text(json.dumps(manifest), encoding="utf-8")

            report = validate_visual_asset_manifest(
                result.manifest_path,
                project_dir=project_dir,
            )

            self.assertFalse(report["ok"])
            self.assertTrue(any("must use visual-asset-manifest/v2" in error for error in report["errors"]))
            self.assertTrue(any("generation_run_id is required" in error for error in report["errors"]))
            self.assertTrue(any("candidate_id is required" in error for error in report["errors"]))

    def test_registration_rejects_session_id_that_does_not_match_original_path(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            project_dir = Path(tmp) / "fieldnote"
            result = write_visual_prompt_outputs(
                project_dir / "public" / "generated" / "design-system",
                self._packet(),
            )
            source = self._write_generated_png(Path(tmp))

            with self.assertRaisesRegex(ValueError, "must match the generation run"):
                register_generated_visual_asset(
                    project_dir=project_dir,
                    manifest_path=result.manifest_path,
                    asset_id="visual-asset:evidence-hero",
                    source_path=source,
                    alt_text="현장 증거 자료",
                    selection_reason="도메인 정보가 가장 선명함",
                    reviewed_criteria=["domain subject is clear"],
                    session_id="019e2de5-941b-7971-98e3-000000000000",
                )

    def test_detects_tampered_workspace_asset(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            project_dir = Path(tmp) / "fieldnote"
            output_dir = project_dir / "public" / "generated" / "design-system"
            result = write_visual_prompt_outputs(output_dir, self._packet())
            source = Path(tmp) / "source.webp"
            Image.new("RGB", (1600, 900), "#315c4b").save(source)
            original = self._write_generated_png(Path(tmp))
            registered = register_generated_visual_asset(
                project_dir=project_dir,
                manifest_path=result.manifest_path,
                asset_id="visual-asset:evidence-hero",
                source_path=source,
                alt_text="현장 증거 자료",
                selection_reason="색과 구도가 설계 방향에 맞음",
                reviewed_criteria=["domain subject is clear"],
                original_png_path=str(original),
                session_id=self.generation_run_id,
            )
            Image.new("RGB", (640, 480), "#000000").save(registered.asset_path)

            report = validate_visual_asset_manifest(result.manifest_path, project_dir=project_dir)
            self.assertFalse(report["ok"])
            self.assertTrue(any("sha256" in error for error in report["errors"]))
            self.assertTrue(any("dimensions" in error for error in report["errors"]))

    def test_integrated_asset_requires_component_target(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            project_dir = Path(tmp) / "fieldnote"
            output_dir = project_dir / "public" / "generated" / "design-system"
            packet = self._packet()
            packet["slots"][0]["intended_for"] = []
            result = write_visual_prompt_outputs(output_dir, packet)
            source = self._write_generated_png(Path(tmp))

            register_generated_visual_asset(
                project_dir=project_dir,
                manifest_path=result.manifest_path,
                asset_id="visual-asset:evidence-hero",
                source_path=source,
                alt_text="현장 증거 자료",
                selection_reason="도메인 정보가 가장 선명함",
                reviewed_criteria=["domain subject is clear"],
                session_id=self.generation_run_id,
            )
            with self.assertRaisesRegex(ValueError, "intended_for"):
                promote_generated_visual_asset(
                    project_dir=project_dir,
                    manifest_path=result.manifest_path,
                    asset_id="visual-asset:evidence-hero",
                )

    def test_promotion_requires_runtime_reference_and_actual_component_contract(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            project_dir = Path(tmp) / "fieldnote"
            result = write_visual_prompt_outputs(
                project_dir / "public" / "generated" / "design-system",
                self._packet(),
            )
            source = self._write_generated_png(Path(tmp))
            registered = register_generated_visual_asset(
                project_dir=project_dir,
                manifest_path=result.manifest_path,
                asset_id="visual-asset:evidence-hero",
                source_path=source,
                alt_text="현장 증거 자료",
                selection_reason="도메인 정보가 가장 선명함",
                reviewed_criteria=["domain subject is clear"],
                session_id=self.generation_run_id,
            )

            self._write_component_contracts(project_dir, "different-component")
            (project_dir / "index.html").write_text(
                f'<img src="./{registered.asset_path.relative_to(project_dir).as_posix()}" alt="현장 증거 자료">',
                encoding="utf-8",
            )
            with self.assertRaisesRegex(ValueError, "actual component contract"):
                promote_generated_visual_asset(
                    project_dir=project_dir,
                    manifest_path=result.manifest_path,
                    asset_id="visual-asset:evidence-hero",
                )
            self.assertEqual(
                json.loads(result.manifest_path.read_text(encoding="utf-8"))["assets"][0]["status"],
                "accepted",
            )

            self._write_component_contracts(project_dir, "evidence-board")
            (project_dir / "index.html").unlink()
            with self.assertRaisesRegex(ValueError, "runtime implementation code"):
                promote_generated_visual_asset(
                    project_dir=project_dir,
                    manifest_path=result.manifest_path,
                    asset_id="visual-asset:evidence-hero",
                )
            self.assertEqual(
                json.loads(result.manifest_path.read_text(encoding="utf-8"))["assets"][0]["status"],
                "accepted",
            )

    def test_strict_validation_rejects_prompt_original_and_legacy_review_tampering(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            project_dir = Path(tmp) / "fieldnote"
            result = write_visual_prompt_outputs(
                project_dir / "public" / "generated" / "design-system",
                self._packet(),
            )
            source = self._write_generated_png(Path(tmp))
            register_generated_visual_asset(
                project_dir=project_dir,
                manifest_path=result.manifest_path,
                asset_id="visual-asset:evidence-hero",
                source_path=source,
                alt_text="현장 증거 자료",
                selection_reason="도메인 정보가 가장 선명함",
                reviewed_criteria=["domain subject is clear"],
                session_id=self.generation_run_id,
            )
            self._write_component_contracts(project_dir, "evidence-board")
            manifest = json.loads(result.manifest_path.read_text(encoding="utf-8"))
            record = manifest["assets"][0]
            record.pop("review_gate_version")
            record["original_sha256"] = "tampered"
            record["prompt_slot_sha256"] = "tampered"
            result.manifest_path.write_text(json.dumps(manifest), encoding="utf-8")
            result.packet_path.write_text(
                result.packet_path.read_text(encoding="utf-8") + "\n",
                encoding="utf-8",
            )

            report = validate_visual_asset_manifest(
                result.manifest_path,
                project_dir=project_dir,
                strict_production=True,
            )

            self.assertFalse(report["ok"])
            self.assertTrue(any("legacy generated asset" in error for error in report["errors"]))
            self.assertTrue(any("original_sha256" in error for error in report["errors"]))
            self.assertTrue(any("prompt_slot_sha256" in error for error in report["errors"]))
            self.assertTrue(any("manifest.prompt_packet_sha256" in error for error in report["errors"]))

            source.unlink()
            report = validate_visual_asset_manifest(
                result.manifest_path,
                project_dir=project_dir,
                strict_production=True,
            )
            self.assertTrue(any("original_png_path does not exist" in error for error in report["errors"]))

    def test_legacy_prompt_contract_migration_is_archived_and_fail_closed(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            project_dir = Path(tmp) / "fieldnote"
            output_dir = project_dir / "public" / "generated" / "design-system"
            result = write_visual_prompt_outputs(output_dir, self._packet())
            source = self._write_generated_png(Path(tmp))
            registered = register_generated_visual_asset(
                project_dir=project_dir,
                manifest_path=result.manifest_path,
                asset_id="visual-asset:evidence-hero",
                source_path=source,
                alt_text="현장 증거 자료를 검토하는 작업 화면",
                selection_reason="가장 명확한 현장 증거 구도",
                reviewed_criteria=["domain subject is clear"],
                session_id=self.generation_run_id,
            )
            self._write_component_contracts(project_dir, "evidence-board")
            (project_dir / "index.html").write_text(
                f'<img src="./{registered.asset_path.relative_to(project_dir).as_posix()}" '
                'alt="현장 증거 자료를 검토하는 작업 화면">',
                encoding="utf-8",
            )
            promote_generated_visual_asset(
                project_dir=project_dir,
                manifest_path=result.manifest_path,
                asset_id="visual-asset:evidence-hero",
            )

            fixture_packet = {
                **self._packet(),
                "slots": [{
                    "id": "visual-asset:fixture-led-ui-direction-mockup",
                    "slot": "fixture-led-ui-direction-mockup",
                    "label": "Fixture direction",
                    "intended_for": ["component:evidence-board"],
                    "aspect_ratios": ["16:10"],
                    "candidate_count": 2,
                    "prompt": "Fixture table and selected-match rail",
                    "review_criteria": ["domain subject is clear"],
                    "visual_scope": "design-reference-only",
                }],
            }
            result = write_visual_prompt_outputs(output_dir, fixture_packet)
            report = validate_visual_asset_manifest(
                result.manifest_path,
                project_dir=project_dir,
                strict_production=True,
            )
            manifest = json.loads(result.manifest_path.read_text(encoding="utf-8"))
            hero = next(
                item for item in manifest["assets"]
                if item["id"] == "visual-asset:evidence-hero"
            )

            self.assertTrue(report["ok"], report["errors"])
            self.assertFalse(hero["active_generation"])
            self.assertEqual(hero["lifecycle_role"], "legacy-supporting-asset")
            self.assertEqual(len(hero["prompt_contract_migrations"]), 1)
            archive = output_dir / hero["prompt_contract_migrations"][0]["archive"]["path"]
            self.assertTrue(archive.is_file())

            with self.assertRaisesRegex(ValueError, "only planned"):
                register_generated_visual_asset(
                    project_dir=project_dir,
                    manifest_path=result.manifest_path,
                    asset_id="visual-asset:evidence-hero",
                    source_path=source,
                    alt_text="다시 등록하려는 자산",
                    selection_reason="중복 등록 방지 검사",
                    reviewed_criteria=["domain subject is clear"],
                    session_id=self.generation_run_id,
                )

            archive.write_text("{}", encoding="utf-8")
            report = validate_visual_asset_manifest(
                result.manifest_path,
                project_dir=project_dir,
                strict_production=True,
            )
            self.assertFalse(report["ok"])
            self.assertTrue(any("prompt_contract_migrations" in error for error in report["errors"]))

    def test_registration_rejects_a_planned_inactive_legacy_slot(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            project_dir = Path(tmp) / "fieldnote"
            output_dir = project_dir / "public" / "generated" / "design-system"
            packet = self._packet()
            packet["slots"][0]["active_generation"] = False
            packet["slots"][0]["legacy_contract"] = {
                "schema_version": "visual-asset-prompt-contract-migration/v1",
                "reason": "retired test slot",
            }
            result = write_visual_prompt_outputs(output_dir, packet)
            source = self._write_generated_png(Path(tmp))

            with self.assertRaisesRegex(ValueError, "inactive legacy"):
                register_generated_visual_asset(
                    project_dir=project_dir,
                    manifest_path=result.manifest_path,
                    asset_id="visual-asset:evidence-hero",
                    source_path=source,
                    alt_text="비활성 슬롯 후보",
                    selection_reason="비활성 슬롯 거부 검사",
                    reviewed_criteria=["domain subject is clear"],
                    session_id=self.generation_run_id,
                )

    def test_rejects_candidate_with_wrong_slot_aspect_ratio(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            project_dir = Path(tmp) / "fieldnote"
            output_dir = project_dir / "public" / "generated" / "design-system"
            result = write_visual_prompt_outputs(output_dir, self._packet())
            source = self._write_generated_png(
                Path(tmp),
                size=(600, 1200),
            )

            with self.assertRaisesRegex(ValueError, "planned ratios"):
                register_generated_visual_asset(
                    project_dir=project_dir,
                    manifest_path=result.manifest_path,
                    asset_id="visual-asset:evidence-hero",
                    source_path=source,
                    alt_text="현장 증거 자료",
                    selection_reason="후보 검증",
                    reviewed_criteria=["domain subject is clear"],
                    session_id=self.generation_run_id,
                )

    def test_validates_sourced_assets_with_source_contract(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            project_dir = Path(tmp) / "fieldnote"
            asset_path = project_dir / "assets" / "field-photo.jpg"
            asset_path.parent.mkdir(parents=True)
            Image.new("RGB", (1200, 800), "#8b8068").save(asset_path)
            import hashlib

            manifest_path = project_dir / "public" / "generated" / "design-system" / "manifest.json"
            manifest_path.parent.mkdir(parents=True)
            manifest_path.write_text(json.dumps({
                "schema_version": "visual-asset-manifest/v1",
                "project": "fieldnote",
                "brand": "Fieldnote",
                "generator": {"id": "sourced-visual-fallback"},
                "source_session": {},
                "assets": [{
                    "id": "sourced-visual-asset:field-photo",
                    "label": "Field evidence photo",
                    "slot": "evidence-photo",
                    "status": "integrated",
                    "acquisition_mode": "sourced",
                    "asset_path": "assets/field-photo.jpg",
                    "source_url": "https://openverse.org/image/example",
                    "download_url": "https://images.example/field-photo.jpg",
                    "provider": "openverse",
                    "author": "Example Photographer",
                    "license": {"id": "cc0", "label": "CC0"},
                    "attribution_required": False,
                    "sha256": hashlib.sha256(asset_path.read_bytes()).hexdigest(),
                    "intended_for": ["component:evidence-card"],
                    "alt_text": "현장에서 수집한 표본 사진",
                    "selection_reason": "실제 증거 자료가 필요한 슬롯",
                }],
            }), encoding="utf-8")

            report = validate_visual_asset_manifest(manifest_path, project_dir=project_dir)
            self.assertTrue(report["ok"], report["errors"])

            manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
            manifest["assets"][0]["provider"] = "lazyweb"
            manifest_path.write_text(json.dumps(manifest), encoding="utf-8")
            report = validate_visual_asset_manifest(manifest_path, project_dir=project_dir)
            self.assertFalse(report["ok"])
            self.assertTrue(any("reference-only" in error for error in report["errors"]))

            manifest["assets"][0]["provider"] = "adobe-stock"
            manifest_path.write_text(json.dumps(manifest), encoding="utf-8")
            report = validate_visual_asset_manifest(manifest_path, project_dir=project_dir)
            self.assertFalse(report["ok"])
            self.assertTrue(any("license_proof" in error for error in report["errors"]))


if __name__ == "__main__":
    unittest.main()
