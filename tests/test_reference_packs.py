import json
import tempfile
import unittest
from pathlib import Path

from design_ontology_harness.reference_packs import (
    build_reference_pack,
    list_reference_packs,
    select_visual_references,
    sync_reference_pack_sources,
)


class ReferencePackTests(unittest.TestCase):
    def test_build_pack_from_local_folder_and_selects_references(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            source_dir = root / "screens"
            project_dir = root / "project"
            pack_dir = root / "packs" / "crm-pack"
            source_dir.mkdir()
            project_dir.mkdir()
            _write_image(source_dir / "crm-dashboard-table.png", b"crm dashboard bytes")
            _write_image(source_dir / "checkout-mobile.png", b"checkout mobile bytes")

            pack = build_reference_pack(
                pack_id="crm-pack",
                output_dir=pack_dir,
                source_dirs=[source_dir],
                provider_id="local-screenshots",
                category="dashboard",
                tags=["crm", "analytics"],
                materialize="copy",
            )

            self.assertEqual(pack["pack_id"], "crm-pack")
            self.assertEqual(pack["asset_count"], 2)
            self.assertTrue((pack_dir / "pack.json").exists())
            self.assertTrue((pack_dir / "assets.jsonl").exists())
            self.assertTrue((pack_dir / "index.sqlite").exists())

            selection = select_visual_references(
                pack=pack_dir,
                project_dir=project_dir,
                query="crm dashboard table",
                count=1,
                link_mode="symlink",
            )

            self.assertEqual(selection["selected_count"], 1)
            self.assertEqual(selection["selected"][0]["label"], "crm-dashboard-table")
            selected_path = project_dir / selection["selected"][0]["selected_relative_path"]
            self.assertTrue(selected_path.is_symlink())
            self.assertTrue(selected_path.exists())

    def test_manifest_pack_supports_lazy_url_records_and_syncs_sources(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            pack_dir = root / "packs" / "web-pack"
            project_dir = root / "project"
            project_dir.mkdir()
            manifest_path = root / "assets.jsonl"
            manifest_path.write_text(
                json.dumps(
                    {
                        "asset_id": "remote-crm-dashboard",
                        "provider_id": "web-crawl",
                        "category": "dashboard",
                        "label": "Remote CRM dashboard",
                        "source_url": "https://example.com/case-study",
                        "download_url": "https://cdn.example.com/crm-dashboard.png",
                        "tags": ["crm", "dashboard", "table"],
                    }
                )
                + "\n",
                encoding="utf-8",
            )

            build_reference_pack(
                pack_id="web-pack",
                output_dir=pack_dir,
                asset_manifest=manifest_path,
                materialize="metadata",
            )
            selection = select_visual_references(
                pack="web-pack",
                pack_root=root / "packs",
                project_dir=project_dir,
                query="crm dashboard",
                count=1,
            )

            self.assertEqual(selection["selected_count"], 1)
            self.assertEqual(selection["selected"][0]["materialization"], "lazy-reference")
            profile = {"visual_reference": {"sources": ["references/manual.png"]}}
            result = sync_reference_pack_sources(
                raw_brand_profile=profile,
                selection_manifest=selection,
                base_dir=project_dir,
            )

            self.assertEqual(result["managed_source_count"], 1)
            sources = profile["visual_reference"]["sources"]
            self.assertEqual(sources[0], "references/manual.png")
            self.assertEqual(sources[1]["kind"], "external-reference")
            self.assertEqual(sources[1]["provider_id"], "web-crawl")
            self.assertEqual(sources[1]["url"], "https://example.com/case-study")
            self.assertEqual(profile["visual_reference"]["reference_pack"]["pack_id"], "web-pack")

    def test_list_reference_packs_reads_pack_metadata(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            source_dir = root / "screens"
            source_dir.mkdir()
            _write_image(source_dir / "dashboard.png", b"dashboard bytes")
            build_reference_pack(
                pack_id="dashboard-pack",
                output_dir=root / "dashboard-pack",
                source_dirs=[source_dir],
            )

            packs = list_reference_packs(root)

            self.assertEqual(len(packs), 1)
            self.assertEqual(packs[0]["pack_id"], "dashboard-pack")
            self.assertEqual(packs[0]["asset_count"], 1)


def _write_image(path: Path, payload: bytes) -> None:
    path.write_bytes(payload)


if __name__ == "__main__":
    unittest.main()
