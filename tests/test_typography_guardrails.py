import unittest

from design_ontology_harness.agent_packs import _codex_implementer_skill
from design_ontology_harness.authoring import build_system_spec_markdown, build_token_schema
from design_ontology_harness.component_specs import generate_component_specs
from design_ontology_harness.font_reference import (
    resolve_font_system,
    validate_headline_display_guardrails,
)


def _sample_brand_profile() -> dict:
    profile = {
        "brand_name": "Signal Desk",
        "system_name": "Signal Desk System",
        "product_summary": "독립 편집팀을 위한 에디토리얼 협업 작업 공간",
        "audiences": ["독립 편집자", "소규모 콘텐츠 팀"],
        "brand_keywords": ["calm", "editorial", "precise"],
        "anti_keywords": ["noisy"],
        "tone_of_voice": ["사려 깊은", "정제된"],
        "visual_keywords": ["editorial", "quiet contrast"],
        "interaction_keywords": ["steady", "predictable"],
        "platforms": ["web"],
        "accessibility_targets": ["WCAG 2.2 AA"],
        "product_primitives": ["workspace navigation", "rich text editor", "dashboard cards"],
    }
    profile["_resolved_font_system"] = resolve_font_system(profile)
    return profile


def _sample_blueprint() -> dict:
    return {
        "system_name": "Signal Desk System",
        "principles": [
            {
                "name": "Editorial rhythm",
                "rule": "Type and spacing should preserve reading rhythm before decorative impact.",
            }
        ],
        "governance": {
            "implementation_guardrails": [
                "Preserve wrap stability while aligning code to tokens.",
            ],
            "ai_synthesis_principles": [],
        },
        "ontology_targets": [
            {"concept_id": "typography", "count": 9},
            {"concept_id": "layout", "count": 6},
        ],
        "component_strategy": {
            "required_component_families": ["marketing", "editorial"],
        },
    }


class TypographyGuardrailTests(unittest.TestCase):
    def test_editorial_korean_heading_prefers_serif_pairing(self) -> None:
        font_system = resolve_font_system(_sample_brand_profile())

        self.assertEqual(font_system["product_type_detected"], "editorial")
        self.assertIn("serif", font_system["heading"]["family"])
        self.assertEqual(font_system["heading"]["name"], "Noto Serif KR")
        self.assertEqual(font_system["body"]["name"], "Pretendard")
        self.assertEqual(font_system["script_guardrails"]["headline_font"]["name"], "Noto Serif KR")
        self.assertEqual(font_system["script_guardrails"]["body_font"]["name"], "Pretendard")

    def test_font_resolution_exposes_korean_script_guardrails(self) -> None:
        font_system = resolve_font_system(_sample_brand_profile())

        self.assertTrue(font_system["needs_korean"])
        self.assertIsNotNone(font_system["script_guardrails"])
        self.assertEqual(font_system["script_guardrails"]["primary_script"], "korean")
        self.assertEqual(
            font_system["script_guardrails"]["implementation_constraints"]["headline_display"]["line_height_min"],
            "1.08",
        )
        self.assertEqual(
            font_system["script_guardrails"]["wrap"]["headline"]["word_break"],
            "keep-all",
        )
        self.assertIn(
            "<br />",
            " ".join(font_system["script_guardrails"]["rules"]),
        )

    def test_explicit_font_system_overrides_auto_resolution(self) -> None:
        profile = _sample_brand_profile()
        profile["font_system"] = {
            "heading": {"name": "Space Grotesk", "weights": [500, 600, 700]},
            "body": {"name": "Inter", "weights": [400, 500, 600]},
            "mono": {"name": "JetBrains Mono", "weights": [400, 500, 600]},
            "korean": {"name": "Pretendard", "weights": [400, 500, 600, 700]},
        }

        font_system = resolve_font_system(profile)

        self.assertEqual(font_system["heading"]["name"], "Space Grotesk")
        self.assertEqual(font_system["body"]["name"], "Inter")
        self.assertEqual(font_system["mono"]["name"], "JetBrains Mono")
        self.assertEqual(font_system["korean"]["name"], "Pretendard")
        self.assertEqual(font_system["pairing_source"], "manual font_system")

    def test_system_spec_and_component_specs_surface_guardrails(self) -> None:
        brand_profile = _sample_brand_profile()
        blueprint = _sample_blueprint()
        token_schema = build_token_schema(brand_profile, blueprint)

        self.assertIn("script_guardrails", token_schema["categories"]["typography"])
        self.assertIn(
            "word-break: keep-all",
            " ".join(token_schema["categories"]["typography"]["rules"]),
        )
        self.assertIn(
            "line_height_min",
            token_schema["categories"]["typography"]["script_guardrails"]["implementation_constraints"]["headline_display"],
        )

        spec_md = build_system_spec_markdown(
            brand_profile=brand_profile,
            blueprint=blueprint,
            validation={"errors": [], "warnings": []},
            foundations=[
                {
                    "concept_id": "typography",
                    "name": "Type scale and editorial hierarchy",
                    "priority": "high",
                    "signal_count": 9,
                }
            ],
            token_schema=token_schema,
            component_inventory={
                "families": [{"family": "marketing", "components": ["hero-section"]}],
                "candidate_component_archetypes": [],
            },
            documents=[],
        )
        self.assertIn("Hangul headline defaults", spec_md)
        self.assertIn("word-break=keep-all", spec_md)
        self.assertIn("Hangul display safety", spec_md)

        component_specs = generate_component_specs(
            brand_profile=brand_profile,
            blueprint=blueprint,
            component_list=[
                {
                    "name": "hero-section",
                    "family": "marketing",
                    "role": "Landing hero",
                    "source": "spec",
                }
            ],
            documents=[],
        )
        self.assertTrue(component_specs["typography_guidance"]["active"])
        self.assertIn(
            "keep-all",
            " ".join(component_specs["specs"][0]["implementation_notes"]),
        )
        self.assertIn(
            "line_height_min",
            component_specs["typography_guidance"]["implementation_constraints"]["headline_display"],
        )

    def test_validator_flags_unsafe_hangul_display_values(self) -> None:
        font_system = resolve_font_system(_sample_brand_profile())
        issues = validate_headline_display_guardrails(
            font_system["script_guardrails"],
            line_height=0.93,
            letter_spacing="-0.04em",
        )

        self.assertTrue(issues)
        self.assertIn("line-height 0.93", issues[0])
        self.assertTrue(any("letter-spacing -0.04em" in issue for issue in issues))

    def test_codex_skill_mentions_script_guardrails(self) -> None:
        skill_text = _codex_implementer_skill("design-system")
        self.assertIn("script_guardrails", skill_text)
        self.assertIn("word-break: keep-all", skill_text)
        self.assertIn("line-height below the artifact safety minimum", skill_text)


if __name__ == "__main__":
    unittest.main()
