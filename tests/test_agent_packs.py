from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from design_ontology_harness.agent_packs import (
    _codex_implementer_skill,
    _codex_reference_inspect_skill,
    _codex_visual_asset_skill,
    scaffold_agent_pack,
)


class AgentPackTests(unittest.TestCase):
    def test_codex_visual_asset_skill_uses_builtin_imagegen_without_api_fallback(self) -> None:
        skill_text = _codex_visual_asset_skill("design-system")

        self.assertIn("STYLE.md", skill_text)
        self.assertIn("DESIGN.md", skill_text)
        self.assertIn("image_gen", skill_text)
        self.assertIn("do not call an API fallback", skill_text)
        self.assertIn("visual_reference_report.json", skill_text)
        self.assertIn("public/generated/design-system/manifest.json", skill_text)
        self.assertIn("public/generated/design-system/imagegen-prompts.md", skill_text)
        self.assertIn("Sourced Visual Fallback", skill_text)
        self.assertIn("license-verified sourced visual fallback", skill_text)
        self.assertIn("Free sourced providers", skill_text)
        self.assertIn("Licensed providers", skill_text)
        self.assertIn("Reference-only providers", skill_text)
        self.assertIn("Adobe Stock", skill_text)
        self.assertIn("Lazyweb", skill_text)
        self.assertIn("public/generated/design-system/sourced-visual-candidates.json", skill_text)
        self.assertIn("source_url", skill_text)
        self.assertIn("Do not hotlink", skill_text)
        self.assertIn("Image-free card walls", skill_text)
        self.assertIn("visual assets as part of completeness", skill_text)
        self.assertIn("Medium Selection Contract", skill_text)
        self.assertIn("comic covers", skill_text)
        self.assertIn("alt_text", skill_text)

    def test_codex_implementer_reads_style_capsule_first(self) -> None:
        skill_text = _codex_implementer_skill("design-system")

        self.assertIn("IMPLEMENTATION_CONTRACT.md", skill_text)
        self.assertIn("STYLE.md", skill_text)
        self.assertIn("DESIGN.md", skill_text)
        self.assertIn("Token binding is necessary but not sufficient", skill_text)
        self.assertIn("Commercial product realism", skill_text)
        self.assertIn("pitch decks", skill_text)
        self.assertIn("image-free commercial mockups", skill_text)
        self.assertIn("approved icon systems", skill_text)
        self.assertIn("data-icon-set", skill_text)

    def test_codex_reference_inspect_skill_keeps_references_advisory(self) -> None:
        skill_text = _codex_reference_inspect_skill("design-system")

        self.assertIn("inspect-reference-site", skill_text)
        self.assertIn("PAGE_TOPOLOGY.md", skill_text)
        self.assertIn("BEHAVIORS.md", skill_text)
        self.assertIn("Observed Reference Evidence", skill_text)
        self.assertIn("component morphology", skill_text)
        self.assertIn("layout density", skill_text)
        self.assertIn("interaction affordance", skill_text)
        self.assertIn("Never copy", skill_text)
        self.assertIn("color palette", skill_text)
        self.assertIn("product copy", skill_text)
        self.assertIn("logos", skill_text)
        self.assertIn("raw CSS values", skill_text)

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
            reference_skill_path = (
                Path(tmp)
                / "plugins"
                / "design-system-harness"
                / "skills"
                / "design-system-reference-inspect"
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
            self.assertTrue(reference_skill_path.exists())
            self.assertIn(str(skill_path), result["created"])
            self.assertIn(str(reference_skill_path), result["created"])
            self.assertIn("image_gen", skill_path.read_text(encoding="utf-8"))
            self.assertIn("do not call an API fallback", skill_path.read_text(encoding="utf-8"))
            self.assertIn("sourced visual fallback", skill_path.read_text(encoding="utf-8"))
            self.assertIn("inspect-reference-site", reference_skill_path.read_text(encoding="utf-8"))
            self.assertIn("Never copy", reference_skill_path.read_text(encoding="utf-8"))

            plugin_manifest = json.loads(plugin_manifest_path.read_text(encoding="utf-8"))
            self.assertIn("imagery", plugin_manifest["keywords"])
            self.assertIn("reference-inspection", plugin_manifest["keywords"])
            self.assertIn("image_gen", plugin_manifest["interface"]["longDescription"])
            self.assertIn("website reference inspections", plugin_manifest["interface"]["longDescription"])
            self.assertIn("license-verified sourced visual fallback", plugin_manifest["interface"]["longDescription"])
            self.assertIn("light mode", " ".join(plugin_manifest["interface"]["defaultPrompt"]))
            self.assertIn("advisory morphology", " ".join(plugin_manifest["interface"]["defaultPrompt"]))
            self.assertIn("operational product surfaces", " ".join(plugin_manifest["interface"]["defaultPrompt"]))
            self.assertIn("fallbacks are disabled", plugin_manifest["interface"]["longDescription"])


if __name__ == "__main__":
    unittest.main()
