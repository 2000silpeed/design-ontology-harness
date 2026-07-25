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


class FontLoadabilityTests(unittest.TestCase):
    """자동 선택은 로드할 수 있는 서체만 고른다.

    배포 경로가 없는 서체를 고르면 화면은 조용히 system-ui로 떨어지고 서체 결정
    자체가 무효가 된다. 점수를 매길 대상이 아니라 후보에서 빼야 한다.
    """

    def test_unloadable_fonts_are_not_selectable(self) -> None:
        from design_ontology_harness.font_reference import (
            FONT_DB,
            is_loadable_font,
            selectable_fonts,
        )

        pool = {font["name"] for font in selectable_fonts()}
        self.assertTrue(pool)
        for name in pool:
            self.assertTrue(is_loadable_font(name), f"{name} 로딩 경로 없음")
        excluded = {font["name"] for font in FONT_DB} - pool
        for name in excluded:
            self.assertFalse(is_loadable_font(name))

    def test_every_resolved_slot_is_loadable(self) -> None:
        """여러 브랜드 성격으로 돌려도 선택 결과가 항상 로드 가능해야 한다.

        점수 경로 말고도 korean_pair 체인과 PROVEN_PAIRINGS가 서체를 끌어온다.
        그 경로가 후보 필터를 우회하면 로드 불가 서체가 다시 들어온다.
        """
        from design_ontology_harness.font_reference import is_loadable_font, resolve_font_system

        keyword_sets = [
            ["calm", "editorial", "precise"],
            ["playful", "warm", "friendly"],
            ["precise", "operational", "exacting"],
            ["luxury", "fashion", "elegant"],
            ["technical", "minimal", "clear"],
        ]
        for keywords in keyword_sets:
            for summary in ("한국어 번역 검수 대기열", "An English-only analytics console"):
                profile = {
                    "brand_name": "Probe",
                    "system_name": "Probe System",
                    "product_summary": summary,
                    "audiences": ["a"],
                    "brand_keywords": keywords,
                    "anti_keywords": ["generic"],
                    "tone_of_voice": ["clear"],
                    "visual_keywords": ["clean"],
                    "interaction_keywords": ["steady"],
                    "platforms": ["web"],
                    "accessibility_targets": ["WCAG 2.2 AA"],
                    "product_primitives": ["dashboard cards"],
                }
                resolved = resolve_font_system(profile)
                for slot in ("display", "heading", "body", "korean", "mono"):
                    entry = resolved.get(slot)
                    if not isinstance(entry, dict) or not entry.get("name"):
                        continue
                    with self.subTest(keywords=keywords, summary=summary[:12], slot=slot):
                        self.assertTrue(
                            is_loadable_font(entry["name"]),
                            f"{slot}={entry['name']} 는 로드 경로가 없다",
                        )


if __name__ == "__main__":
    unittest.main()
