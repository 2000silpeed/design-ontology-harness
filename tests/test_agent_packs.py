from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from design_ontology_harness.agent_packs import (
    _claude_implement_skill,
    _claude_implementer_agent,
    _claude_rebuild_agent,
    _claude_rebuild_skill,
    _codex_concept_author_skill,
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
        self.assertIn("register-image-asset", skill_text)
        self.assertIn("promote-image-asset", skill_text)
        self.assertIn("validate-image-assets", skill_text)
        self.assertIn("planned → accepted → integrated", skill_text)
        self.assertIn("visual-asset-manifest/v2", skill_text)
        self.assertIn("generation_provenance_version", skill_text)
        self.assertIn("generation_run_id", skill_text)
        self.assertIn("candidate_id", skill_text)
        self.assertIn("arbitrary caller-authored values are not provenance", skill_text)
        self.assertIn("DS087", skill_text)

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
        self.assertIn("validate-component-contracts", skill_text)
        self.assertIn("needs-authoring", skill_text)
        self.assertIn("verify-production-ui", skill_text)
        self.assertIn("multimodal-review", skill_text)

    def test_ui_producing_skills_carry_the_ui_base_rules(self) -> None:
        for artifact_dir, skill_text in (
            ("design-system", _codex_implementer_skill("design-system")),
            ("design-system", _claude_implement_skill("design-system")),
            ("design-system", _claude_implementer_agent("design-system")),
            ("design-system", _claude_rebuild_skill("design-system")),
            ("design-system", _claude_rebuild_agent("design-system")),
        ):
            with self.subTest(artifact_dir=artifact_dir, skill=skill_text[:60]):
                self.assertIn("UI base rules", skill_text)
                for code in ("DS100", "DS101", "DS102", "DS103", "DS104", "DS105", "DS106", "DS107"):
                    self.assertIn(code, skill_text)
                self.assertIn("--ds-leading-body", skill_text)
                self.assertIn("--ds-tracking-body", skill_text)
                self.assertIn("--ds-wrap-word-break", skill_text)

    def test_korean_labels_do_not_inherit_the_latin_uppercase_convention(self) -> None:
        """대문자 + 넓은 자간 권고는 한글 라벨에 그대로 옮기면 안 된다."""
        skill_text = _claude_rebuild_skill("design-system")

        self.assertNotIn("uppercase + letter-spacing (optional)", skill_text)
        self.assertIn("라벨의 uppercase + 넓은 letter-spacing은 라틴 전용 관례", skill_text)
        self.assertIn("한글 라벨은 크기·굵기·색으로만 구분", skill_text)

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

    def test_codex_concept_author_skill_makes_llm_author_layout_skeleton(self) -> None:
        skill_text = _codex_concept_author_skill("design-system")

        self.assertIn("application_concept", skill_text)
        self.assertIn("layout_skeleton", skill_text)
        self.assertIn("design_differentiation", skill_text)
        self.assertIn("LLM-authored step", skill_text)
        self.assertIn("Do not choose a preset", skill_text)
        self.assertIn("first_screen_contract", skill_text)
        self.assertIn("signature_moves", skill_text)
        self.assertIn("Astryx and Geist only as component taxonomy", skill_text)
        self.assertIn("component_decision", skill_text)
        self.assertIn("validate-component-contracts", skill_text)
        self.assertIn("data_contract", skill_text)
        self.assertIn("needs-authoring", skill_text)

    def test_codex_scaffold_includes_visual_asset_and_concept_author_skills(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            result = scaffold_agent_pack(
                Path(tmp),
                artifact_dir="design-system",
                targets=["codex"],
            )

            concept_skill_path = (
                Path(tmp)
                / "plugins"
                / "design-system-harness"
                / "skills"
                / "design-system-concept-author"
                / "SKILL.md"
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

            self.assertTrue(concept_skill_path.exists())
            self.assertTrue(skill_path.exists())
            self.assertTrue(reference_skill_path.exists())
            team_skill_path = (
                Path(tmp)
                / "plugins"
                / "design-system-harness"
                / "skills"
                / "design-ontology-team-orchestrator"
                / "SKILL.md"
            )
            self.assertTrue(team_skill_path.exists())
            self.assertIn("verify-production-ui", team_skill_path.read_text(encoding="utf-8"))
            self.assertIn(str(concept_skill_path), result["created"])
            self.assertIn(str(skill_path), result["created"])
            self.assertIn(str(reference_skill_path), result["created"])
            self.assertIn("application_concept", concept_skill_path.read_text(encoding="utf-8"))
            self.assertIn("layout_skeleton", concept_skill_path.read_text(encoding="utf-8"))
            self.assertIn("image_gen", skill_path.read_text(encoding="utf-8"))
            self.assertIn("do not call an API fallback", skill_path.read_text(encoding="utf-8"))
            self.assertIn("sourced visual fallback", skill_path.read_text(encoding="utf-8"))
            self.assertIn("inspect-reference-site", reference_skill_path.read_text(encoding="utf-8"))
            self.assertIn("Never copy", reference_skill_path.read_text(encoding="utf-8"))

            plugin_manifest = json.loads(plugin_manifest_path.read_text(encoding="utf-8"))
            self.assertEqual("0.2.0", plugin_manifest["version"])
            self.assertIn("concept-authoring", plugin_manifest["keywords"])
            self.assertIn("layout-skeleton", plugin_manifest["keywords"])
            self.assertIn("imagery", plugin_manifest["keywords"])
            self.assertIn("reference-inspection", plugin_manifest["keywords"])
            self.assertIn("product concept", plugin_manifest["interface"]["longDescription"])
            self.assertIn("image_gen", plugin_manifest["interface"]["longDescription"])
            self.assertIn("website reference inspections", plugin_manifest["interface"]["longDescription"])
            self.assertIn("license-verified sourced visual fallback", plugin_manifest["interface"]["longDescription"])
            self.assertIn("application_concept", " ".join(plugin_manifest["interface"]["defaultPrompt"]))
            self.assertIn("light mode", " ".join(plugin_manifest["interface"]["defaultPrompt"]))
            self.assertIn("advisory morphology", " ".join(plugin_manifest["interface"]["defaultPrompt"]))
            self.assertIn("operational product surfaces", " ".join(plugin_manifest["interface"]["defaultPrompt"]))
            self.assertIn("fallbacks are disabled", plugin_manifest["interface"]["longDescription"])


if __name__ == "__main__":
    unittest.main()
