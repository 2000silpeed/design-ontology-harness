from __future__ import annotations

import json
import re
from functools import lru_cache
from importlib.resources import files
from typing import Any


TEXT_TOKEN_RE = re.compile(r"[A-Za-z가-힣0-9]+")

BRAND_SIGNAL_TERMS = {
    "analytical": {"신뢰", "안정", "집중", "전문성", "절제", "clarity", "deep", "natural"},
    "bold": {"강렬함", "에너지", "주목성", "상징적", "활기", "pure", "standard"},
    "calm": {"고요", "안정", "부드러움", "자연스러움", "절제", "pastel", "low_chroma"},
    "editorial": {"고급스러움", "고전적", "성숙함", "세련", "품격", "classic", "deep"},
    "energetic": {"에너지", "생동감", "활기", "주목성", "bright", "pure"},
    "friendly": {"친근함", "부드러움", "따뜻함", "자연스러움", "pastel"},
    "luxury": {"고급스러움", "권위", "우아함", "품격", "성숙함", "deep"},
    "minimal": {"절제", "고요", "안정", "low_chroma", "neutral"},
    "playful": {"경쾌함", "달콤함", "생기", "친근함", "bright", "pastel"},
    "precise": {"신뢰", "안정", "전문성", "집중", "명료", "measured"},
    "trustworthy": {"신뢰", "안정", "권위", "전문성", "지속성", "classic", "deep"},
    "warm": {"따뜻함", "온기", "자연스러움", "orange", "red"},
}

DEFAULT_GUIDELINE_IDS = [
    "guideline-rgb-cmyk-split-by-output-medium",
    "guideline-color-values-are-reference-not-absolute",
    "guideline-mood-tags-before-palette-expansion",
    "guideline-no-palette-table-reconstruction",
    "guideline-palette-pair-edges-require-transformative-brief",
]

DEFAULT_PATTERN_IDS = [
    "pattern-spectrum-family-keyword-stack",
    "pattern-color-card-triad-swatch-reading-metrics",
    "pattern-color-keyword-to-design-brief",
    "pattern-palette-by-role-and-contrast-not-table-row",
    "pattern-safe-palette-output-contract",
]


@lru_cache(maxsize=1)
def load_semantic_color_ontology() -> dict[str, Any]:
    """Load the compact color ontology imported from semantic-os."""

    path = files("design_ontology_harness").joinpath("resources/semantic_color_ontology.json")
    return json.loads(path.read_text(encoding="utf-8"))


def build_semantic_color_context(
    *,
    parsed_reference: dict,
    active_palette: dict,
    brand_profile: dict,
    strategy: dict | None = None,
) -> dict[str, Any]:
    ontology = load_semantic_color_ontology()
    nodes = ontology.get("nodes", [])
    node_by_id = {node["id"]: node for node in nodes}
    keyword_nodes = [node for node in nodes if node.get("type") == "ColorKeyword"]

    matched_keywords = _match_active_palette_keywords(keyword_nodes, active_palette)
    recommended_keywords = _recommend_keywords(
        keyword_nodes=keyword_nodes,
        brand_profile=brand_profile,
        strategy=strategy or {},
        matched_ids={item["id"] for item in matched_keywords},
    )

    guidelines = [
        _compact_policy_node(node_by_id[node_id])
        for node_id in DEFAULT_GUIDELINE_IDS
        if node_id in node_by_id
    ]
    heuristics = [
        _compact_policy_node(node)
        for node in nodes
        if node.get("type") == "ColorHeuristic"
    ]
    metrics = [
        _compact_metric_node(node)
        for node in nodes
        if node.get("type") == "ColorMetric"
    ]
    patterns = [
        _compact_pattern_node(node_by_id[node_id])
        for node_id in DEFAULT_PATTERN_IDS
        if node_id in node_by_id
    ]

    return {
        "schema_version": "design-ontology-harness/semantic-color-context-v1",
        "source": ontology.get("source", {}),
        "node_count": ontology.get("node_count", 0),
        "edge_count": ontology.get("edge_count", 0),
        "copyright_handling": ontology.get("source", {}).get("copyright_handling", ""),
        "matched_keywords": matched_keywords,
        "recommended_keywords": recommended_keywords,
        "guidelines": guidelines,
        "heuristics": heuristics,
        "metrics": metrics,
        "patterns": patterns,
        "rules": [
            "Treat RGB/HEX as digital reference values, not absolute reproduction guarantees.",
            "Split RGB/sRGB and CMYK/print-profile decisions by output medium.",
            "Choose mood tags and semantic roles before expanding support colors.",
            "Do not reconstruct paid-source palette tables, page order, or row/column structures.",
            "Publish palette candidates as role, contrast, caveat, and proof conditions.",
        ],
        "matched_color_count": len(matched_keywords),
        "reference_color_count": len(parsed_reference.get("colors", [])),
    }


def _match_active_palette_keywords(keyword_nodes: list[dict], active_palette: dict) -> list[dict[str, Any]]:
    by_name = {
        _normalize_key(node.get("properties", {}).get("label", "")): node
        for node in keyword_nodes
    }
    by_hex = {
        str(node.get("properties", {}).get("rgb_hex", "")).upper(): node
        for node in keyword_nodes
        if node.get("properties", {}).get("rgb_hex")
    }

    matched: list[dict[str, Any]] = []
    seen: set[str] = set()
    roles = active_palette.get("roles", {}) or {}
    selected = active_palette.get("selected_colors", []) or []
    candidates = [(role, item) for role, item in roles.items()]
    if not candidates:
        candidates = [("selected", item) for item in selected]

    for role, color in candidates:
        if not isinstance(color, dict):
            continue
        node = by_name.get(_normalize_key(color.get("name", "")))
        if not node and color.get("hex"):
            node = by_hex.get(str(color.get("hex", "")).upper())
        if not node or node["id"] in seen:
            continue
        seen.add(node["id"])
        matched.append(_compact_keyword_node(node, role=role, score=None, reasons=["active palette role match"]))

    return matched


def _recommend_keywords(
    *,
    keyword_nodes: list[dict],
    brand_profile: dict,
    strategy: dict,
    matched_ids: set[str],
    limit: int = 8,
) -> list[dict[str, Any]]:
    query_terms = _profile_terms(brand_profile, strategy)
    if not query_terms:
        return []

    ranked: list[tuple[float, dict, list[str]]] = []
    for node in keyword_nodes:
        if node["id"] in matched_ids:
            continue
        score, reasons = _score_keyword_node(node, query_terms)
        if score > 0:
            ranked.append((score, node, reasons))

    ranked.sort(key=lambda item: (-item[0], item[1].get("properties", {}).get("label", "")))
    return [
        _compact_keyword_node(node, role="recommendation", score=round(score, 2), reasons=reasons[:3])
        for score, node, reasons in ranked[:limit]
    ]


def _profile_terms(brand_profile: dict, strategy: dict) -> set[str]:
    raw_terms: list[str] = []
    for key in [
        "brand_keywords",
        "visual_keywords",
        "interaction_keywords",
        "tone_of_voice",
        "product_primitives",
        "audiences",
    ]:
        value = brand_profile.get(key, [])
        if isinstance(value, str):
            raw_terms.append(value)
        else:
            raw_terms.extend(str(item) for item in value)
    raw_terms.extend(str(item) for item in strategy.get("prefer_moods", []) or [])

    terms: set[str] = set()
    for raw in raw_terms:
        for token in TEXT_TOKEN_RE.findall(raw.lower()):
            terms.add(token)
            terms.update(BRAND_SIGNAL_TERMS.get(token, set()))
    return {term.lower() for term in terms if term}


def _score_keyword_node(node: dict, query_terms: set[str]) -> tuple[float, list[str]]:
    props = node.get("properties", {})
    fields = [
        props.get("label", ""),
        props.get("summary", ""),
        props.get("spectrum", ""),
        props.get("family", ""),
        props.get("category", ""),
        " ".join(props.get("mood_tags", []) or []),
        " ".join(props.get("tone_axes", []) or []),
    ]
    haystack = " ".join(str(field).lower() for field in fields)

    score = 0.0
    reasons: list[str] = []
    for term in sorted(query_terms, key=len, reverse=True):
        if not term or term not in haystack:
            continue
        score += 2.0 if len(term) > 2 else 0.5
        if len(reasons) < 4:
            reasons.append(f"matches '{term}'")

    return score, reasons


def _compact_keyword_node(
    node: dict,
    *,
    role: str,
    score: float | None,
    reasons: list[str],
) -> dict[str, Any]:
    props = node.get("properties", {})
    out = {
        "id": node.get("id"),
        "role": role,
        "name": props.get("label"),
        "hex": props.get("rgb_hex"),
        "spectrum": props.get("spectrum"),
        "family": props.get("family"),
        "category": props.get("category"),
        "mood_tags": props.get("mood_tags", []),
        "tone_axes": props.get("tone_axes", []),
        "summary": props.get("summary"),
        "source_pages": {
            "swatch": props.get("swatch_page_pdf"),
            "reading": props.get("reference_reading_page_pdf"),
            "metrics": props.get("metrics_page_pdf"),
        },
        "reasons": reasons,
    }
    if score is not None:
        out["score"] = score
    return out


def _compact_policy_node(node: dict) -> dict[str, Any]:
    props = node.get("properties", {})
    return {
        "id": node.get("id"),
        "type": node.get("type"),
        "label": props.get("label"),
        "summary": props.get("summary"),
        "prompt_do": props.get("prompt_do", [])[:4],
        "prompt_avoid": props.get("prompt_avoid", [])[:4],
    }


def _compact_metric_node(node: dict) -> dict[str, Any]:
    props = node.get("properties", {})
    return {
        "id": node.get("id"),
        "label": props.get("label"),
        "summary": props.get("summary"),
    }


def _compact_pattern_node(node: dict) -> dict[str, Any]:
    props = node.get("properties", {})
    return {
        "id": node.get("id"),
        "label": props.get("label"),
        "summary": props.get("summary"),
        "prompt_do": props.get("prompt_do", [])[:3],
        "prompt_avoid": props.get("prompt_avoid", [])[:3],
    }


def _normalize_key(value: str) -> str:
    return re.sub(r"[^a-z0-9가-힣]+", "", str(value).lower())
