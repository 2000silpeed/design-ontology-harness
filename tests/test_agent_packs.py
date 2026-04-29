from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from design_ontology_harness.agent_packs import _codex_visual_asset_skill, scaffold_agent_pack


class AgentPackTests(unittest.TestCase):
    def test_codex_visual_asset_skill_uses_imagine2_and_artifacts(self) -> None:
        skill_text = _codex_visual_asset_skill("design-system")

        self.assertIn("imagine2", skill_text)
        self.assertIn("visual_reference_report.json", skill_text)
        self.assertIn("public/generated/design-system/manifest.json", skill_text)
        self.assertIn("alt_text", skill_text)

    def test_codex_scaffold_includes_visual_asset_skill(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            result = scaffold_agent_pack(
                Path(tmp),
                artifact_dir="design-system",
                targets=["codex"],
            )

            skill_path = (
                Path(tmp)
                / "plugins"
                / "design-system-harness"
                / "skills"
                / "design-system-visual-assets"
                / "SKILL.md"
            )
            plugin_manifest_path = (
                Path(tmp)
                / "plugins"
                / "design-system-harness"
                / ".codex-plugin"
                / "plugin.json"
            )

            self.assertTrue(skill_path.exists())
            self.assertIn(str(skill_path), result["created"])
            self.assertIn("imagine2", skill_path.read_text(encoding="utf-8"))

            plugin_manifest = json.loads(plugin_manifest_path.read_text(encoding="utf-8"))
            self.assertIn("imagery", plugin_manifest["keywords"])
            self.assertIn("imagine2", plugin_manifest["interface"]["longDescription"])


if __name__ == "__main__":
    unittest.main()
