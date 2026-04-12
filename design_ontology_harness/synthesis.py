from __future__ import annotations

import json
from collections import Counter, defaultdict
from pathlib import Path

from .authoring import generate_system_pack
from .color_reference import resolve_color_reference
from .font_reference import resolve_font_system
from .models import DocumentRecord, ReferenceLink
from .utils import ensure_dir, write_json

KEYWORD_PRINCIPLES = {
    "calm": {
        "name": "Calm by Default",
        "rule": "기본 상태는 조용해야 하고, 강조는 정말 필요할 때만 사용합니다.",
        "implications": ["채도 낮은 기본 팔레트", "모션은 짧고 낮은 진폭", "화면당 핵심 액션 수 제한"],
    },
    "precise": {
        "name": "Precision Over Ornament",
        "rule": "장식보다 정보의 정렬, 상태의 정확성, 반응의 일관성을 우선합니다.",
        "implications": ["명확한 상태 규칙", "촘촘한 spacing scale", "컴포넌트 변형 최소화"],
    },
    "editorial": {
        "name": "Editorial Hierarchy",
        "rule": "타이포그래피와 여백으로 위계를 만들고, 장식은 의미를 돕는 범위에서만 사용합니다.",
        "implications": ["텍스트 중심 레이아웃", "강한 heading rhythm", "콘텐츠 읽기 흐름 우선"],
    },
    "trustworthy": {
        "name": "Trust Through Consistency",
        "rule": "예측 가능한 인터랙션과 안정적인 시각 언어로 신뢰를 쌓습니다.",
        "implications": ["일관된 disabled/error/success 패턴", "접근성 기준 우선", "위험 액션 명시적 구분"],
    },
    "bold": {
        "name": "Bold with Discipline",
        "rule": "강한 개성은 허용하되 구조를 해치지 않는 선에서 통제합니다.",
        "implications": ["강한 accent 색상 1개 중심", "대형 헤드라인 제한적 사용", "캠페인성 요소와 제품 UI 분리"],
    },
}


def load_brand_profile(path: Path) -> dict:
    profile = json.loads(path.read_text(encoding="utf-8"))
    reference_config = profile.get("color_reference")
    if reference_config:
        resolved_reference, issues = resolve_color_reference(reference_config, path.parent, profile)
        if resolved_reference:
            profile["_resolved_color_reference"] = resolved_reference
        if issues:
            profile["_color_reference_issues"] = issues

    font_config = profile.get("font_reference")
    if font_config is None or font_config is True:
        profile["_resolved_font_system"] = resolve_font_system(profile)

    return profile


def build_blueprint(
    output_dir: Path,
    brand_profile: dict,
    references: list[ReferenceLink],
    documents: list[DocumentRecord],
) -> dict:
    blueprint_dir = ensure_dir(output_dir / "blueprint")
    concept_counts = _count_concepts(output_dir / "ontology" / "evidence.jsonl")
    source_coverage = _count_source_coverage(output_dir / "ontology" / "evidence.jsonl")
    prioritized_concepts = [
        {"concept_id": concept_id, "count": count}
        for concept_id, count in concept_counts.most_common(8)
    ]
    principle_keywords = brand_profile.get("brand_keywords", [])[:4]
    principles = [
        _principle_from_keyword(keyword)
        for keyword in principle_keywords
    ]

    blueprint = {
        "brand_name": brand_profile.get("brand_name", "Unnamed Brand"),
        "system_name": brand_profile.get("system_name", "Unnamed System"),
        "product_summary": brand_profile.get("product_summary", ""),
        "positioning": {
            "audiences": brand_profile.get("audiences", []),
            "brand_keywords": brand_profile.get("brand_keywords", []),
            "anti_keywords": brand_profile.get("anti_keywords", []),
            "tone_of_voice": brand_profile.get("tone_of_voice", []),
            "platforms": brand_profile.get("platforms", []),
            "accessibility_targets": brand_profile.get("accessibility_targets", []),
        },
        "principles": principles,
        "reference_strategy": {
            "seed_article": references[0].source_article_url if references else None,
            "top_sources_by_concept_coverage": [
                {"source_label": label, "covered_concepts": sorted(list(concepts))}
                for label, concepts in sorted(
                    source_coverage.items(),
                    key=lambda item: (-len(item[1]), item[0]),
                )[:8]
            ],
            "rule": "레퍼런스는 그대로 복제하지 않고, 원칙과 구조만 가져와 브랜드 아이덴티티에 맞게 재구성합니다.",
        },
        "token_strategy": _build_token_strategy(brand_profile, prioritized_concepts),
        "component_strategy": _build_component_strategy(brand_profile, prioritized_concepts),
        "color_reference": brand_profile.get("_resolved_color_reference"),
        "governance": {
            "source_of_truth": [
                "brand profile",
                "design tokens",
                "component specs",
                "usage rules",
                "existing product surfaces and task flows"
            ],
            "change_policy": [
                "새 컴포넌트보다 기존 primitive 확장을 우선",
                "예외 케이스는 variant로 흡수 가능한지 먼저 검토",
                "브랜드 키워드와 anti-keyword를 위반하면 추가하지 않음"
            ],
            "implementation_guardrails": [
                "기존 핵심 화면, 진입점, 작업 흐름은 명시적 승인 없이 제거하거나 숨기지 않음",
                "전면 셸 리라이트보다 토큰 -> primitive -> feature surface 순서의 점진적 롤아웃을 우선",
                "새 시각 규칙은 지원 대상 테마와 breakpoint 전체에서 먼저 검증",
                "기존 데이터 밀도와 업무 완료 경로를 유지한 상태에서 시각 품질을 높이는 방향을 우선",
                "기능 위치 변경, 정보 구조 변경, 패널 제거는 별도의 migration plan이 있을 때만 수행"
            ],
        },
        "ontology_targets": prioritized_concepts,
    }

    write_json(blueprint_dir / "design_system_blueprint.json", blueprint)
    generate_system_pack(output_dir, brand_profile, blueprint, references, documents)
    return blueprint


def _count_concepts(evidence_path: Path) -> Counter:
    counts: Counter = Counter()
    if not evidence_path.exists():
        return counts
    for line in evidence_path.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        row = json.loads(line)
        counts[row["concept_id"]] += 1
    return counts


def _count_source_coverage(evidence_path: Path) -> dict[str, set[str]]:
    coverage: dict[str, set[str]] = defaultdict(set)
    if not evidence_path.exists():
        return coverage
    for line in evidence_path.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        row = json.loads(line)
        coverage[row["source_label"]].add(row["concept_id"])
    return coverage


def _principle_from_keyword(keyword: str) -> dict:
    normalized = keyword.lower().strip()
    if normalized in KEYWORD_PRINCIPLES:
        principle = KEYWORD_PRINCIPLES[normalized]
        return {
            "keyword": keyword,
            "name": principle["name"],
            "rule": principle["rule"],
            "implications": principle["implications"],
        }
    return {
        "keyword": keyword,
        "name": keyword.title(),
        "rule": f"`{keyword}`를 시각적 선택과 인터랙션 선택의 기본 기준으로 삼습니다.",
        "implications": [
            f"{keyword}와 충돌하는 컴포넌트 변형은 만들지 않기",
            f"{keyword}를 토큰 네이밍과 문서화 기준에 반영하기",
        ],
    }


def _build_token_strategy(brand_profile: dict, prioritized_concepts: list[dict]) -> dict:
    visual_keywords = brand_profile.get("visual_keywords", [])
    interaction_keywords = brand_profile.get("interaction_keywords", [])
    concept_ids = {item["concept_id"] for item in prioritized_concepts}

    return {
        "color": {
            "goal": "브랜드 개성을 드러내되 UI 전체를 지배하지 않는 팔레트",
            "rules": [
                "brand color는 1개의 primary accent를 중심으로 설계",
                "semantic color는 brand color와 분리해서 유지",
                "contrast ratio는 접근성 목표를 우선",
                "지원하는 theme 모드마다 semantic surface/text/border 쌍을 함께 정의",
                "하드코딩 색상보다 semantic token 적용을 우선"
            ],
        },
        "typography": {
            "goal": "정보 구조와 브랜드 톤을 동시에 전달하는 타입 시스템",
            "rules": [
                "heading/body/caption 역할을 토큰으로 고정",
                "텍스트 길이가 긴 화면에서 리듬이 무너지지 않도록 line-height를 계층별로 정의",
                "편집형 제품이면 typography scale을 먼저 확정"
            ],
            "signal": "typography" in concept_ids or "editorial" in [kw.lower() for kw in brand_profile.get("brand_keywords", [])],
        },
        "spacing": {
            "goal": "밀도와 여백의 성격을 제품 전반에서 일관되게 유지",
            "rules": [
                "4pt 또는 8pt 기반 scale을 정하고 예외 사용을 제한",
                "컴포넌트 내부 spacing과 레이아웃 spacing을 분리",
            ],
        },
        "motion": {
            "goal": "상태 변화를 설명하는 수준의 모션만 허용",
            "rules": [
                "transition duration/easing을 토큰화",
                "주의 환기용 모션과 구조적 모션을 구분"
            ],
            "brand_signal": interaction_keywords,
        },
        "visual_keywords": visual_keywords,
    }


def _build_component_strategy(brand_profile: dict, prioritized_concepts: list[dict]) -> dict:
    primitives = brand_profile.get("product_primitives", [])
    concept_ids = {item["concept_id"] for item in prioritized_concepts}
    required_families = ["button", "input", "navigation", "feedback", "overlay"]
    if "data tables" in [primitive.lower() for primitive in primitives]:
        required_families.append("data-display")
    if "rich text editor" in [primitive.lower() for primitive in primitives]:
        required_families.append("editorial")

    return {
        "product_primitives": primitives,
        "required_component_families": required_families,
        "rules": [
            "primitive 단위로 책임을 먼저 정의하고 컴포넌트는 그 위에 매핑",
            "variant proliferation을 막기 위해 상태와 강조 레벨을 먼저 표준화",
            "브랜드 표현은 surface, emphasis, typography에서 주고 구조는 안정적으로 유지",
            "기존 기능 진입점은 유지한 채 내부 구현과 시각 언어부터 교체",
            "전체 셸을 한 번에 다시 그리기보다 feature surface 단위로 순차 적용"
        ],
        "concept_alignment": sorted(concept_ids),
    }
