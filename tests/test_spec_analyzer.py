import unittest

from design_ontology_harness.spec_analyzer import analyze_spec


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


if __name__ == "__main__":
    unittest.main()
