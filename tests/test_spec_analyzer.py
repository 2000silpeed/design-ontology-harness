import unittest

from design_ontology_harness.spec_analyzer import analyze_spec, build_component_list


class SpecAnalyzerTests(unittest.TestCase):
    def test_dashboard_language_defaults_to_operational_overview(self) -> None:
        spec_text = """
        운영 대시보드에서 KPI, 메트릭, 현황, 활동 피드를 한 화면에 보여줍니다.
        사용자는 필터와 테이블을 함께 보며 오늘 처리할 업무를 빠르게 스캔합니다.
        """

        patterns = {item["pattern"] for item in analyze_spec(spec_text)}

        self.assertIn("operational overview", patterns)
        self.assertIn("data tables", patterns)
        self.assertNotIn("dashboard cards", patterns)

    def test_explicit_card_language_still_enables_dashboard_cards(self) -> None:
        spec_text = """
        상단에는 통계 카드와 요약 카드, KPI card를 배치해 빠른 요약을 제공합니다.
        """

        patterns = {item["pattern"] for item in analyze_spec(spec_text)}

        self.assertIn("dashboard cards", patterns)

    def test_game_review_spec_avoids_workspace_false_positives(self) -> None:
        spec_text = """
        콘솔과 PC 게임을 비평, 비교, 추천하는 에디토리얼 게임 리뷰 사이트입니다.
        리뷰 카드, 스코어 배지, 플랫폼 필터, 비교표, 랭킹 리스트, 검색 자동완성, 출시 캘린더가 필요합니다.
        총평과 장점/단점, 가격 비교, 에디터 코멘트 하이라이트도 함께 보여줍니다.
        """

        patterns = {item["pattern"] for item in analyze_spec(spec_text)}

        self.assertIn("comparison and ranking", patterns)
        self.assertIn("search and filter", patterns)
        self.assertIn("calendar and dates", patterns)
        self.assertNotIn("workspace navigation", patterns)
        self.assertNotIn("command palette", patterns)
        self.assertNotIn("rich text editor", patterns)
        self.assertNotIn("comments and discussion", patterns)
        self.assertNotIn("pricing and plans", patterns)
        self.assertNotIn("dashboard cards", patterns)

    def test_explicit_component_inventory_is_authoritative(self) -> None:
        spec_text = """
        # Tournament product

        ## 주요 컴포넌트
        - **schedule-table**: 킥오프, 팀, 조, 경기장, 상태를 표시한다.
        - **prediction-panel**: 팬의 승무패 선택과 집계를 보여준다.
        - `discussion-thread`: 경기별 의견과 신고 상태를 보여준다.

        ## 비범위
        실시간 중계 영상은 제공하지 않으며 운영자가 콘텐츠를 작성하는
        리치 텍스트 에디터도 만들지 않는다.
        """

        detected = analyze_spec(spec_text)
        component_list = build_component_list(detected)

        self.assertEqual(
            [component["name"] for component in component_list],
            ["schedule-table", "prediction-panel", "discussion-thread"],
        )
        self.assertTrue(detected[0]["authoritative"])
        self.assertEqual(component_list[0]["decision_layer"], "spec-explicit")


if __name__ == "__main__":
    unittest.main()
