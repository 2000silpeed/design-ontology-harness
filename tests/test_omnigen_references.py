import json
import sqlite3
import tempfile
import unittest
from pathlib import Path

from design_ontology_harness.omnigen_references import (
    DEFAULT_CATEGORIES,
    IMAGE_COLUMNS,
    export_omnigen_selection_gallery,
    select_omnigen_references,
    sync_omnigen_sources,
)


class OmnigenReferenceSelectionTests(unittest.TestCase):
    def test_select_omnigen_references_scores_diversifies_and_symlinks(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            vault_dir = root / "vault"
            project_dir = root / "project"
            vault_dir.mkdir()
            project_dir.mkdir()
            index_path = vault_dir / "index.sqlite"
            _create_omnigen_index(index_path)

            dashboard = _write_image(vault_dir, "images/app-design/dashboard.png")
            crm = _write_image(vault_dir, "images/web-design/crm.png")
            checkout = _write_image(vault_dir, "images/mobile-design/checkout.png")
            _insert_image(
                index_path,
                id=1,
                category="app-design",
                subject="an analytics BI dashboard app",
                style="data-dense dashboard",
                palette="blue accent",
                mood="muted neutral theme",
                rel_path="images/app-design/dashboard.png",
                abs_path=str(dashboard),
                sha256="sha-dashboard",
                phash="phash-dashboard",
                rating=1,
            )
            _insert_image(
                index_path,
                id=2,
                category="web-design",
                subject="an admin CRM contacts table",
                style="corporate clean",
                palette="monochrome accent",
                mood="light theme",
                rel_path="images/web-design/crm.png",
                abs_path=str(crm),
                sha256="sha-crm",
                phash="phash-crm",
            )
            _insert_image(
                index_path,
                id=3,
                category="mobile-design",
                subject="a food delivery app checkout screen",
                style="playful colorful UI",
                palette="orange accent",
                mood="vibrant theme",
                rel_path="images/mobile-design/checkout.png",
                abs_path=str(checkout),
                sha256="sha-checkout",
                phash="phash-checkout",
            )

            manifest = select_omnigen_references(
                vault_dir=vault_dir,
                project_dir=project_dir,
                query="analytics dashboard crm",
                categories=["app-design", "web-design", "mobile-design"],
                count=2,
                link_mode="symlink",
            )

            self.assertEqual(manifest["selected_count"], 2)
            self.assertEqual(manifest["selected"][0]["subject"], "an analytics BI dashboard app")
            self.assertEqual(manifest["selected"][1]["subject"], "an admin CRM contacts table")
            for item in manifest["selected"]:
                selected_path = project_dir / item["selected_relative_path"]
                self.assertFalse(Path(item["selected_relative_path"]).is_absolute())
                self.assertTrue(selected_path.is_symlink())
                self.assertTrue(selected_path.exists())
                self.assertFalse(item["redistribution_allowed"])

    def test_default_categories_include_ai_agent_ui_and_gallery_export(self) -> None:
        self.assertIn("ai-agent-ui", DEFAULT_CATEGORIES)
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            vault_dir = root / "vault"
            project_dir = root / "project"
            vault_dir.mkdir()
            project_dir.mkdir()
            index_path = vault_dir / "index.sqlite"
            _create_omnigen_index(index_path)

            agent_ui = _write_image(vault_dir, "images/ai-agent-ui/agent.png")
            _insert_image(
                index_path,
                id=10,
                category="ai-agent-ui",
                subject="an agent task console with tool timeline",
                style="agentic workspace",
                palette="blue accent",
                mood="light theme",
                rel_path="images/ai-agent-ui/agent.png",
                abs_path=str(agent_ui),
                sha256="sha-agent",
                phash="phash-agent",
            )

            manifest = select_omnigen_references(
                vault_dir=vault_dir,
                project_dir=project_dir,
                query="agent task console",
                count=1,
                link_mode="symlink",
            )
            gallery_path = export_omnigen_selection_gallery(
                manifest,
                project_dir / "build" / "visuals" / "omnigen_reference_gallery.html",
            )

            self.assertEqual(manifest["selected"][0]["category"], "ai-agent-ui")
            self.assertTrue(gallery_path.exists())
            html = gallery_path.read_text(encoding="utf-8")
            self.assertIn("an agent task console", html)
            self.assertIn("ai-agent-ui", html)
            self.assertIn("<img", html)
            self.assertIn("omnigen-selected/01-an-agent-task-console-with-tool-timeline__sha-agent.png", html)
            self.assertNotIn(str(project_dir), html)

    def test_sync_omnigen_sources_replaces_managed_entries_and_preserves_other_sources(self) -> None:
        profile = {
            "visual_reference": {
                "sources": [
                    {
                        "kind": "image",
                        "provider_id": "omnigen-vault",
                        "path": "build/visuals/omnigen-selected/old.png",
                    },
                    "references/visual/manual.png",
                ]
            }
        }
        manifest = {
            "selected_count": 1,
            "selected": [
                {
                    "id": 1,
                    "rank": 1,
                    "category": "app-design",
                    "subject": "an analytics BI dashboard app",
                    "style": "data-dense dashboard",
                    "palette": "blue accent",
                    "mood": "muted neutral theme",
                    "score": 42,
                    "selected_relative_path": "build/visuals/omnigen-selected/01-dashboard.png",
                    "source_path": "/tmp/vault/images/app-design/dashboard.png",
                }
            ],
        }

        result = sync_omnigen_sources(
            raw_brand_profile=profile,
            selection_manifest=manifest,
            base_dir=Path("/tmp/project"),
        )

        self.assertEqual(result["managed_source_count"], 1)
        sources = profile["visual_reference"]["sources"]
        self.assertEqual(len(sources), 2)
        self.assertEqual(sources[0], "references/visual/manual.png")
        self.assertEqual(sources[1]["provider_id"], "omnigen-vault")
        self.assertEqual(sources[1]["path"], "build/visuals/omnigen-selected/01-dashboard.png")
        self.assertIn("synthetic-ui", sources[1]["tags"])
        self.assertFalse(sources[1]["redistribution_allowed"])


def _create_omnigen_index(path: Path) -> None:
    typed_columns = []
    for column in IMAGE_COLUMNS:
        if column in {"id", "width", "height", "bytes", "rating", "ocr_char_count"}:
            typed_columns.append(f"{column} integer")
        else:
            typed_columns.append(f"{column} text")
    with sqlite3.connect(path) as connection:
        connection.execute(f"create table images ({', '.join(typed_columns)})")


def _insert_image(path: Path, **overrides: object) -> None:
    row = {
        "id": 0,
        "category": "app-design",
        "subject": "",
        "style": "",
        "lighting": "",
        "palette": "",
        "composition": "",
        "mood": "",
        "variant": "",
        "prompt": "",
        "revised_prompt": "",
        "rel_path": "",
        "abs_path": "",
        "width": 1536,
        "height": 1024,
        "size_label": "1536x1024",
        "bytes": 4,
        "sha256": "",
        "bucket": "landscape",
        "phash": "",
        "thumb_rel": "",
        "thumb_abs": "",
        "rating": 0,
        "ocr_char_count": 0,
        "ocr_text": "",
        "status": "active",
        "tags": json.dumps(["ui", "dashboard"]),
        "created_at": "2026-06-20T00:00:00Z",
    }
    row.update(overrides)
    columns = list(IMAGE_COLUMNS)
    values = [row[column] for column in columns]
    placeholders = ",".join("?" for _ in columns)
    with sqlite3.connect(path) as connection:
        connection.execute(
            f"insert into images ({', '.join(columns)}) values ({placeholders})",
            values,
        )


def _write_image(root: Path, rel_path: str) -> Path:
    path = root / rel_path
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(b"fake image")
    return path
