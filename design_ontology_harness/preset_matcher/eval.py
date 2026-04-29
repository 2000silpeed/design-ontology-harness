"""Phase 15-6: matcher quality evaluation.

Runs a labeled dataset against the matcher, reports top-1 accuracy, and
surfaces a confusion matrix so keywords.json / engine tie-break logic can be
tuned against actual miss patterns.

The labeled dataset lives here (not in tests/) so it can be imported from
both test code and the CLI. Adding cases here automatically updates both.
"""

from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass, field
from pathlib import Path
from typing import Iterable

from .engine import MatchQuery, match_presets


# (free_text | MatchQuery kwargs, expected top-1 preset_id)
#
# 58 cases as of Phase 13-11-B. Covers 18 presets across 8 app_modes × 5
# brand_tones, plus ambiguity / tag-dominated / Korean-English mixed /
# adversarial "editor" substring edge cases.
LABELED_CASES: list[tuple[dict, str]] = [
    # P0 baseline — unambiguous natural queries.
    ({"free_text": "한국어 SaaS 대시보드"}, "dashboard--minimal-tech"),
    ({"free_text": "AI 챗봇, 다크 기본"}, "conversation-copilot--minimal-tech"),
    ({"free_text": "에디토리얼 매거진"}, "document-content--editorial-warm"),
    ({"free_text": "관리자 대시보드 미니멀"}, "dashboard--minimal-tech"),
    ({"free_text": "스포츠 랜딩 페이지 bold"}, "marketing-landing--bold-confident"),
    ({"free_text": "fashion 쇼핑몰 editorial"}, "commerce--editorial-warm"),
    ({"free_text": "document reading blog, warm"}, "document-content--editorial-warm"),
    ({"free_text": "copilot chat dark"}, "conversation-copilot--minimal-tech"),
    (
        {"free_text": "한글 SaaS 관리자 콘솔 minimal 중립"},
        "dashboard--minimal-tech",
    ),
    ({"free_text": "admin panel console neutral minimal"}, "dashboard--minimal-tech"),
    # P1 coverage.
    (
        {"free_text": "fintech 대시보드, 보수적, 신뢰, 한글"},
        "dashboard--corporate-trust",
    ),
    ({"free_text": "enterprise banking admin conservative"}, "dashboard--corporate-trust"),
    (
        {"free_text": "SRE 모니터링, alert, observability, 다크"},
        "monitoring-ops--minimal-tech",
    ),
    (
        {"free_text": "grafana observability devtools console"},
        "monitoring-ops--minimal-tech",
    ),
    (
        {"free_text": "API 레퍼런스 개발자 문서 미니멀 devtools"},
        "document-content--minimal-tech",
    ),
    (
        {"free_text": "technical docs reference minimal developer"},
        "document-content--minimal-tech",
    ),
    (
        {"free_text": "소셜 피드 친근 커뮤니티 playful 파스텔"},
        "community-feed--playful-soft",
    ),
    (
        {"free_text": "social feed thread friendly rounded soft"},
        "community-feed--playful-soft",
    ),
    (
        {"free_text": "피그마 캔버스 에디터 디자인 도구 미니멀 creative"},
        "canvas-tool--minimal-tech",
    ),
    (
        {"free_text": "figma canvas editor design tool minimal creative"},
        "canvas-tool--minimal-tech",
    ),
    # P2 coverage.
    (
        {"free_text": "B2B SaaS 마케팅 랜딩 미니멀 깔끔 devtools"},
        "marketing-landing--minimal-tech",
    ),
    (
        {"free_text": "minimal saas landing hero pricing clean devtools"},
        "marketing-landing--minimal-tech",
    ),
    (
        {"free_text": "스트리트웨어 드롭 커머스 bold ecommerce 강렬"},
        "commerce--bold-confident",
    ),
    (
        {"free_text": "bold streetwear drop shop energetic saturated"},
        "commerce--bold-confident",
    ),
    (
        {"free_text": "AI 글쓰기 코파일럿 차분 에디토리얼 editorial 한글"},
        "conversation-copilot--editorial-warm",
    ),
    (
        {"free_text": "writing copilot editorial warm serif calm essay drafting"},
        "conversation-copilot--editorial-warm",
    ),
    (
        {"free_text": "대담한 매거진 에디토리얼 opinion bold 강렬 한글"},
        "document-content--bold-confident",
    ),
    (
        {"free_text": "bold magazine editorial opinion zine saturated feature"},
        "document-content--bold-confident",
    ),
    (
        {"free_text": "편집 매거진 운영 대시보드 차분한 warm 한글"},
        "dashboard--editorial-warm",
    ),
    (
        {"free_text": "editorial publishing dashboard newsroom curation calm warm"},
        "dashboard--editorial-warm",
    ),
    # Phase 15-6 +20: ambiguity, tag-dominated, mixed locale, adversarial.
    ({"free_text": "대시보드"}, "dashboard--minimal-tech"),
    ({"free_text": "blog"}, "document-content--editorial-warm"),
    (
        {"free_text": "디자인 도구 캔버스 레이어 패널"},
        "canvas-tool--minimal-tech",
    ),
    ({"free_text": "핀테크 은행 콘솔"}, "dashboard--corporate-trust"),
    ({"free_text": "magazine"}, "document-content--bold-confident"),
    ({"free_text": "AI dashboard 한국어"}, "dashboard--minimal-tech"),
    (
        {"free_text": "한국어 chatbot assistant prompt artifact ai"},
        "conversation-copilot--minimal-tech",
    ),
    (
        {"free_text": "ai 채팅 어시스턴트 다크 미니멀"},
        "conversation-copilot--minimal-tech",
    ),
    (
        {"free_text": "랜딩 페이지 깔끔"},
        "marketing-landing--minimal-tech",
    ),
    (
        {"free_text": "startup landing clean modern"},
        "marketing-landing--minimal-tech",
    ),
    (
        {"free_text": "축구 리그 팬 랜딩 강렬"},
        "marketing-landing--bold-confident",
    ),
    (
        {"free_text": "패션 쇼핑몰 차분한 에디토리얼 ko"},
        "commerce--editorial-warm",
    ),
    (
        {"free_text": "드롭 shop ecommerce 대담한 강렬"},
        "commerce--bold-confident",
    ),
    (
        {"free_text": "essay writing assistant calm editorial warm"},
        "conversation-copilot--editorial-warm",
    ),
    (
        {"free_text": "온콜 알람 metrics 다크 관측"},
        "monitoring-ops--minimal-tech",
    ),
    (
        {"free_text": "datadog prometheus alerting incident response"},
        "monitoring-ops--minimal-tech",
    ),
    (
        {"free_text": "친근한 팔로우 피드 알림 커뮤니티"},
        "community-feed--playful-soft",
    ),
    (
        {"free_text": "community social thread presence notifications soft"},
        "community-feed--playful-soft",
    ),
    (
        {"free_text": "에디터 editor blog article reading magazine 에디토리얼"},
        "document-content--editorial-warm",
    ),
    (
        {"free_text": "편집부 대시보드 차분한 warm"},
        "dashboard--editorial-warm",
    ),
    # Phase 13-11-A +4: new P3 dashboard presets (bold-confident / playful-soft).
    (
        {"free_text": "B2C 스타트업 대시보드 vivid bold 강렬"},
        "dashboard--bold-confident",
    ),
    (
        {"free_text": "startup admin bold-confident vivid activation retention"},
        "dashboard--bold-confident",
    ),
    (
        {"free_text": "consumer wellness habit tracker playful 친근"},
        "dashboard--playful-soft",
    ),
    (
        {"free_text": "soft wellness dashboard pastel friendly rounded"},
        "dashboard--playful-soft",
    ),
    # Phase 13-11-B +4: new P3 commerce--playful-soft preset (Orchard).
    (
        {"free_text": "크래프트 D2C 커머스 친근 pastel"},
        "commerce--playful-soft",
    ),
    (
        {"free_text": "rounded consumer playful commerce soft d2c"},
        "commerce--playful-soft",
    ),
    (
        {"free_text": "귀여운 D2C 스낵 쇼핑몰 친근"},
        "commerce--playful-soft",
    ),
    (
        {"free_text": "pastel craft ecommerce playful d2c consumer rounded"},
        "commerce--playful-soft",
    ),
    # Phase 13-11-C +8: new P3 marketing-landing--editorial-warm (Loom) + conversation-copilot--corporate-trust (Mercer).
    (
        {"free_text": "독립 뉴스레터 editorial 랜딩 퍼블리셔 warm"},
        "marketing-landing--editorial-warm",
    ),
    (
        {"free_text": "independent newsletter publisher landing editorial reading"},
        "marketing-landing--editorial-warm",
    ),
    (
        {"free_text": "1인 매거진 퍼블리셔 랜딩 editorial 구독 pricing warm ko"},
        "marketing-landing--editorial-warm",
    ),
    (
        {"free_text": "newsletter publisher landing page editorial warm subscribe pricing testimonial"},
        "marketing-landing--editorial-warm",
    ),
    (
        {"free_text": "금융 보험 AI 챗봇 엔터프라이즈 신뢰 한글"},
        "conversation-copilot--corporate-trust",
    ),
    (
        {"free_text": "enterprise finance ai chatbot compliance audit corporate"},
        "conversation-copilot--corporate-trust",
    ),
    (
        {"free_text": "보험 상담 ai copilot 규제 감사 엔터프라이즈 신뢰"},
        "conversation-copilot--corporate-trust",
    ),
    (
        {"free_text": "insurance finance copilot enterprise compliance audit regulatory trust chat"},
        "conversation-copilot--corporate-trust",
    ),
]


@dataclass
class EvalResult:
    total: int
    hits: int
    misses: list[tuple[dict, str, str]] = field(default_factory=list)
    confusion: dict[str, dict[str, int]] = field(default_factory=dict)

    @property
    def accuracy(self) -> float:
        return self.hits / self.total if self.total else 0.0

    def confusion_pairs(self, top_k: int = 5) -> list[tuple[str, str, int]]:
        """Flatten confusion matrix to (expected, predicted, count) tuples
        sorted by count desc, excluding correct predictions."""

        pairs: list[tuple[str, str, int]] = []
        for expected, predicted_map in self.confusion.items():
            for predicted, count in predicted_map.items():
                if predicted != expected:
                    pairs.append((expected, predicted, count))
        pairs.sort(key=lambda item: (-item[2], item[0], item[1]))
        return pairs[:top_k]


def run_eval(
    cases: Iterable[tuple[dict, str]] | None = None,
    *,
    matrix_path: Path | None = None,
) -> EvalResult:
    """Score every labeled case and collect confusion counts."""

    case_list = list(cases if cases is not None else LABELED_CASES)
    confusion: dict[str, dict[str, int]] = defaultdict(lambda: defaultdict(int))
    hits = 0
    misses: list[tuple[dict, str, str]] = []

    for query_kwargs, expected_id in case_list:
        query = MatchQuery(**query_kwargs)
        results = match_presets(
            query,
            matrix_path=matrix_path,
            top_k=1,
            include_deprecated=True,
        )
        predicted = results[0].preset_id if results else "<none>"
        confusion[expected_id][predicted] += 1
        if predicted == expected_id:
            hits += 1
        else:
            misses.append((query_kwargs, expected_id, predicted))

    return EvalResult(
        total=len(case_list),
        hits=hits,
        misses=misses,
        confusion={k: dict(v) for k, v in confusion.items()},
    )


def format_eval(result: EvalResult, *, verbose: bool = False) -> str:
    lines = [
        f"top-1 accuracy: {result.accuracy:.2f} ({result.hits}/{result.total})",
    ]
    pairs = result.confusion_pairs(top_k=5)
    if pairs:
        lines.append("confusion top-5:")
        for expected, predicted, count in pairs:
            lines.append(f"  {expected} → {predicted}  ({count})")
    else:
        lines.append("no confusion (perfect top-1)")

    if verbose and result.misses:
        lines.append("")
        lines.append("misses:")
        for query_kwargs, expected, predicted in result.misses:
            lines.append(
                f"  {query_kwargs} expected={expected} got={predicted}"
            )

    return "\n".join(lines)
