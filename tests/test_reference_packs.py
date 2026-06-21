import json
import tempfile
import unittest
from pathlib import Path

from design_ontology_harness.reference_packs import (
    build_reference_pack,
    export_reference_pack_gallery,
    list_reference_packs,
    select_visual_references,
    sync_reference_pack_sources,
)
from design_ontology_harness import reference_packs


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
                materialize="symlink",
            )

            self.assertEqual(pack["pack_id"], "crm-pack")
            self.assertEqual(pack["asset_count"], 2)
            self.assertTrue((pack_dir / "pack.json").exists())
            self.assertTrue((pack_dir / "assets.jsonl").exists())
            self.assertTrue((pack_dir / "index.sqlite").exists())
            first_asset = json.loads((pack_dir / "assets.jsonl").read_text(encoding="utf-8").splitlines()[0])
            self.assertFalse(Path(first_asset["local_path"]).is_absolute())

            selection = select_visual_references(
                pack=pack_dir,
                project_dir=project_dir,
                query="crm dashboard table",
                count=1,
                link_mode="symlink",
            )

            self.assertEqual(selection["selected_count"], 1)
            self.assertEqual(selection["selected"][0]["label"], "crm-dashboard-table")
            self.assertFalse(Path(selection["selected"][0]["selected_relative_path"]).is_absolute())
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
            (root / "selection.json").write_text(json.dumps(selection), encoding="utf-8")

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
            self.assertEqual(sources[1]["url"], "https://cdn.example.com/crm-dashboard.png")
            self.assertEqual(sources[1]["source_url"], "https://example.com/case-study")
            self.assertEqual(sources[1]["download_url"], "https://cdn.example.com/crm-dashboard.png")
            self.assertEqual(profile["visual_reference"]["reference_pack"]["pack_id"], "web-pack")

            gallery_path = root / "gallery.html"
            gallery = export_reference_pack_gallery(
                pack="web-pack",
                pack_root=root / "packs",
                selection_manifest=root / "selection.json",
                output_path=gallery_path,
            )

            self.assertEqual(gallery["asset_count"], 1)
            self.assertEqual(gallery["selected_count"], 1)
            gallery_text = gallery_path.read_text(encoding="utf-8")
            self.assertIn("Remote CRM dashboard", gallery_text)
            self.assertIn("https://cdn.example.com/crm-dashboard.png", gallery_text)

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

    def test_web_page_image_urls_round_robin_across_sources(self) -> None:
        pages = {
            "https://source-a.example/gallery": """
                <html><body>
                  <img src="/a-one.jpg">
                  <img src="/a-two.jpg">
                </body></html>
            """,
            "https://source-b.example/gallery": """
                <html><body>
                  <img src="/b-one.jpg">
                </body></html>
            """,
        }

        pairs = reference_packs._iter_page_image_urls(pages)

        self.assertEqual(
            pairs,
            [
                ("https://source-a.example/gallery", "https://source-a.example/a-one.jpg"),
                ("https://source-b.example/gallery", "https://source-b.example/b-one.jpg"),
                ("https://source-a.example/gallery", "https://source-a.example/a-two.jpg"),
            ],
        )

    def test_content_type_extension_inference(self) -> None:
        self.assertEqual(reference_packs._extension_from_content_type("image/jpeg; charset=utf-8"), ".jpg")
        self.assertEqual(reference_packs._extension_from_content_type("image/avif"), ".avif")
        self.assertIsNone(reference_packs._extension_from_content_type("text/html"))


def _write_image(path: Path, payload: bytes) -> None:
    path.write_bytes(payload)


if __name__ == "__main__":
    unittest.main()
