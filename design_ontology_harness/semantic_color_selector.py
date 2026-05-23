from __future__ import annotations

import re
from typing import Any

from .semantic_color_ontology import load_semantic_color_ontology


TEXT_TOKEN_RE = re.compile(r"[A-Za-z가-힣0-9]+")
HEX_RE = re.compile(r"#(?:[0-9A-Fa-f]{6}|[0-9A-Fa-f]{3})")
PALETTE_ROLE_RE = re.compile(
    r"^(?P<role>[A-Za-z0-9_-]+):\s*(?P<keyword>.*?)\s*(?P<hex>#[0-9A-Fa-f]{6})?\s*(?:[—-]\s*(?P<behavior>.*))?$"
)

DEFAULT_ROLE_MODEL = [
    {
        "role": "anchor_surface",
        "behavior": "primary application surface, brand depth, and first visual anchor",
    },
    {
        "role": "structural_support",
        "behavior": "navigation, frame, panels, and persistent structure",
    },
    {
        "role": "reading_field",
        "behavior": "main canvas, dense content field, and repeated reading surface",
    },
    {
        "role": "action_signal",
        "behavior": "selected state, call to action, issue stamp, or progress signal",
    },
    {
        "role": "proof_accent",
        "behavior": "limited contrast proof, tag, chart detail, or attention flash",
    },
]

ROLE_VARIANTS = [
    {
        "id": "best-fit",
        "label": "Best Fit",
        "surface_bias": "balanced",
        "contrast_bias": "balanced",
        "diversity_bias": "balanced",
    },
    {
        "id": "quiet-surface",
        "label": "Quiet Surface",
        "surface_bias": "airy",
        "contrast_bias": "soft",
        "diversity_bias": "cohesive",
    },
    {
        "id": "clear-structure",
        "label": "Clear Structure",
        "surface_bias": "grounded",
        "contrast_bias": "balanced",
        "diversity_bias": "cohesive",
    },
    {
        "id": "strong-signal",
        "label": "Strong Signal",
        "surface_bias": "balanced",
        "contrast_bias": "vivid",
        "diversity_bias": "balanced",
    },
    {
        "id": "cross-family",
        "label": "Cross Family",
        "surface_bias": "airy",
        "contrast_bias": "balanced",
        "diversity_bias": "exploratory",
    },
    {
        "id": "deep-frame",
        "label": "Deep Frame",
        "surface_bias": "grounded",
        "contrast_bias": "vivid",
        "diversity_bias": "cohesive",
    },
    {
        "id": "light-canvas",
        "label": "Light Canvas",
        "surface_bias": "airy",
        "contrast_bias": "soft",
        "diversity_bias": "balanced",
    },
    {
        "id": "editorial-pulse",
        "label": "Editorial Pulse",
        "surface_bias": "balanced",
        "contrast_bias": "vivid",
        "diversity_bias": "exploratory",
    },
]


def build_semantic_color_selection(
    *,
    brand_profile: dict[str, Any],
    strategy: dict[str, Any] | None = None,
    candidate_count: int | None = None,
) -> dict[str, Any]:
    """Search the packaged Semantic OS color ontology for this app's palette.

    This deliberately does not contain pre-authored palette sets. It uses the
    current application brief, product primitives, and detected spec components
    to rank ontology ColorPattern and ColorKeyword nodes every time the harness
    synthesizes a design system.
    """

    ontology = load_semantic_color_ontology()
    nodes = ontology.get("nodes", [])
    keyword_nodes = [node for node in nodes if node.get("type") == "ColorKeyword"]
    pattern_nodes = [node for node in nodes if node.get("type") == "ColorPattern"]

    search_profile = _build_search_profile(brand_profile=brand_profile, strategy=strategy or {})
    matched_pattern = _select_pattern(pattern_nodes, search_profile)
    role_model = _role_model_from_pattern(matched_pattern)
    if len(role_model) < 5:
        role_model.extend(DEFAULT_ROLE_MODEL[len(role_model):])
    role_model = role_model[:5]

    count = candidate_count or (strategy or {}).get("candidate_count") or 5
    count = max(5, min(8, int(count)))
    variants = ROLE_VARIANTS[:count]

    keyword_pool = [_compact_keyword_node(node) for node in keyword_nodes]
    candidates = [
        _build_candidate_palette(
            keyword_pool=keyword_pool,
            role_model=role_model,
            search_profile=search_profile,
            variant=variant,
            index=index,
        )
        for index, variant in enumerate(variants, start=1)
    ]
    candidates = [candidate for candidate in candidates if candidate]
    candidates = _dedupe_candidates(candidates)[:count]
    active_palette = candidates[0] if candidates else None

    return {
        "schema_version": "design-ontology-harness/semantic-color-selection-v1",
        "selection_method": "ontology-search-per-run",
        "source": ontology.get("source", {}),
        "node_count": ontology.get("node_count", 0),
        "edge_count": ontology.get("edge_count", 0),
        "query": {
            "terms": sorted(search_profile["terms"])[:80],
            "source_fields": search_profile["source_fields"],
        },
        "matched_pattern": _compact_pattern(matched_pattern) if matched_pattern else None,
        "role_model": role_model,
        "candidate_palettes": candidates,
        "active_palette": active_palette,
        "rules": [
            "Search Semantic OS ColorPattern and ColorKeyword nodes for every app brief.",
            "Do not ship pre-authored palette sets as fixed presets.",
            "Use ColorPattern role language as a role model, not as a copied palette table.",
            "Publish colors as role, reason, caveat, and proof conditions.",
        ],
    }


def colors_from_semantic_palette(candidate: dict[str, Any] | None) -> dict[str, dict[str, Any]]:
    if not candidate:
        return {}

    roles: dict[str, dict[str, Any]] = {}
    for role, item in (candidate.get("roles") or {}).items():
        roles[role] = {
            "name": item.get("name"),
            "family": ".".join(part for part in [item.get("spectrum"), item.get("family")] if part),
            "hex": item.get("hex"),
            "mood": ", ".join(item.get("mood_tags") or []),
            "usage": item.get("behavior") or item.get("reason"),
            "pairings": [],
            "semantic_node_id": item.get("id"),
            "source_type": "semantic-color-ontology",
        }
    return roles


def _build_search_profile(*, brand_profile: dict[str, Any], strategy: dict[str, Any]) -> dict[str, Any]:
    source_fields: dict[str, list[str]] = {}
    raw_values: list[str] = []
    for key in [
        "brand_name",
        "system_name",
        "product_summary",
        "brand_keywords",
        "anti_keywords",
        "tone_of_voice",
        "visual_keywords",
        "interaction_keywords",
        "platforms",
        "audiences",
        "product_primitives",
    ]:
        values = _flatten_text(brand_profile.get(key))
        if values:
            source_fields[key] = values
            raw_values.extend(values)

    for component in brand_profile.get("_spec_components") or []:
        if not isinstance(component, dict):
            continue
        values = _flatten_text([
            component.get("name"),
            component.get("family"),
            component.get("role"),
            component.get("supports_primitive"),
        ])
        if values:
            raw_values.extend(values)
            source_fields.setdefault("spec_components", []).extend(values)

    for pattern in brand_profile.get("_spec_detected_patterns") or []:
        if not isinstance(pattern, dict):
            continue
        values = _flatten_text(pattern)
        if values:
            raw_values.extend(values)
            source_fields.setdefault("spec_detected_patterns", []).extend(values[:8])

    raw_values.extend(_flatten_text(strategy.get("prefer_moods")))
    raw_values.extend(_flatten_text(strategy.get("temperature")))
    raw_values.extend(_flatten_text(strategy.get("contrast")))

    terms = _tokenize_values(raw_values)
    expanded = set(terms)
    for term in list(terms):
        expanded.update(_semantic_expansions(term))

    avoid_terms = _tokenize_values(_flatten_text(brand_profile.get("anti_keywords")) + _flatten_text(strategy.get("avoid_moods")))
    return {
        "raw_values": raw_values,
        "terms": {term.lower() for term in expanded if term},
        "avoid_terms": {term.lower() for term in avoid_terms if term},
        "source_fields": {key: values[:12] for key, values in source_fields.items()},
    }


def _select_pattern(pattern_nodes: list[dict[str, Any]], search_profile: dict[str, Any]) -> dict[str, Any] | None:
    ranked: list[tuple[float, dict[str, Any]]] = []
    for node in pattern_nodes:
        props = node.get("properties", {})
        haystack = _node_haystack(props)
        score = _term_score(search_profile["terms"], haystack)
        if props.get("role_model") == "brief_specific_candidate_not_source_row":
            score += 3.0
        if props.get("palette_roles"):
            score += 1.0
        if score > 0:
            ranked.append((score, node))

    ranked.sort(key=lambda item: (-item[0], item[1].get("properties", {}).get("label", "")))
    return ranked[0][1] if ranked else None


def _role_model_from_pattern(pattern_node: dict[str, Any] | None) -> list[dict[str, Any]]:
    if not pattern_node:
        return list(DEFAULT_ROLE_MODEL)

    roles: list[dict[str, Any]] = []
    for raw_role in pattern_node.get("properties", {}).get("palette_roles", []) or []:
        if not isinstance(raw_role, str):
            continue
        match = PALETTE_ROLE_RE.match(raw_role.strip())
        if not match:
            continue
        role = match.group("role")
        keyword = (match.group("keyword") or "").strip()
        behavior = (match.group("behavior") or "").strip()
        roles.append(
            {
                "role": role,
                "behavior": behavior or keyword,
                "keyword_evidence": keyword,
                "source_pattern_role": raw_role,
            }
        )
    return roles


def _build_candidate_palette(
    *,
    keyword_pool: list[dict[str, Any]],
    role_model: list[dict[str, Any]],
    search_profile: dict[str, Any],
    variant: dict[str, Any],
    index: int,
) -> dict[str, Any] | None:
    selected: dict[str, dict[str, Any]] = {}
    selected_ids: set[str] = set()
    selected_spectrums: list[str] = []
    total_score = 0.0
    rationale: list[str] = []

    for role_index, role in enumerate(role_model):
        ranked = _rank_keywords_for_role(
            keyword_pool=keyword_pool,
            role=role,
            search_profile=search_profile,
            variant=variant,
            selected_ids=selected_ids,
            selected_spectrums=selected_spectrums,
        )
        if not ranked:
            return None

        offset = _variant_offset(variant, role_index, len(ranked))
        chosen_score, chosen, reasons = ranked[offset]
        selected_ids.add(chosen["id"])
        selected_spectrums.append(chosen.get("spectrum", ""))
        selected[role["role"]] = {
            **chosen,
            "score": round(chosen_score, 2),
            "reason": reasons[0] if reasons else f"{chosen['name']} fits {role['role']}.",
            "behavior": role.get("behavior"),
        }
        total_score += chosen_score
        rationale.extend(reasons[:2])

    return {
        "id": f"ontology-{variant['id']}-{index}",
        "label": variant["label"],
        "score": round(total_score, 2),
        "roles": selected,
        "rationale": _unique_strings(rationale)[:8],
        "caveats": [
            "Validate contrast per component before implementation.",
            "Do not reconstruct source palette tables or page order.",
            "Treat HEX values as sRGB digital references unless a print profile is separately provided.",
        ],
        "variant": variant,
    }


def _rank_keywords_for_role(
    *,
    keyword_pool: list[dict[str, Any]],
    role: dict[str, Any],
    search_profile: dict[str, Any],
    variant: dict[str, Any],
    selected_ids: set[str],
    selected_spectrums: list[str],
) -> list[tuple[float, dict[str, Any], list[str]]]:
    ranked: list[tuple[float, dict[str, Any], list[str]]] = []
    role_terms = _tokenize_values([role.get("role", ""), role.get("behavior", ""), role.get("keyword_evidence", "")])

    for keyword in keyword_pool:
        if keyword["id"] in selected_ids:
            continue

        haystack = _keyword_haystack(keyword)
        score = _term_score(search_profile["terms"], haystack)
        score += _term_score(set(role_terms), haystack) * 1.25
        evidence_score, evidence_reasons = _keyword_evidence_score(keyword, role)
        score += evidence_score
        score -= _term_score(search_profile["avoid_terms"], haystack) * 1.5
        role_bias, bias_reasons = _role_bias(keyword, role, variant)
        score += role_bias
        score += _diversity_score(keyword, selected_spectrums, variant)

        reasons = []
        if role.get("behavior"):
            reasons.append(f"{keyword['name']} supports {role['role']} behavior.")
        reasons.extend(evidence_reasons)
        if score > 0:
            reasons.extend(bias_reasons)
        ranked.append((score, keyword, reasons or [f"{keyword['name']} is viable for {role['role']}."]))

    ranked.sort(key=lambda item: (-item[0], item[1]["name"]))
    return ranked


def _keyword_evidence_score(keyword: dict[str, Any], role: dict[str, Any]) -> tuple[float, list[str]]:
    evidence = str(role.get("keyword_evidence") or "").strip()
    if not evidence:
        return 0.0, []

    evidence = HEX_RE.sub("", evidence).strip().lower()
    keyword_name = str(keyword.get("name") or "").lower()
    haystack = _keyword_haystack(keyword)
    score = 0.0
    reasons: list[str] = []
    if evidence and (evidence == keyword_name or evidence in keyword_name or keyword_name in evidence):
        score += 8.0
        reasons.append(f"{keyword['name']} is direct ontology role evidence.")
    score += _term_score(_tokenize_values([evidence]), haystack) * 1.5
    return score, reasons


def _role_bias(keyword: dict[str, Any], role: dict[str, Any], variant: dict[str, Any]) -> tuple[float, list[str]]:
    text = " ".join([role.get("role", ""), role.get("behavior", "")]).lower()
    family = str(keyword.get("family", "")).lower()
    tone_axes = {str(axis).lower() for axis in keyword.get("tone_axes", [])}
    spectrum = str(keyword.get("spectrum", "")).lower()
    score = 0.0
    reasons: list[str] = []

    if any(term in text for term in ["anchor", "depth", "frame", "support", "background", "shell"]):
        if family == "deep" or "low_value" in tone_axes:
            score += 4.0
            reasons.append(f"{keyword['name']} has depth for structural roles.")
    if any(term in text for term in ["surface", "field", "paper", "quiet", "highlight", "air", "canvas"]):
        if family in {"pastel", "natural"} or "high_value" in tone_axes or "low_chroma" in tone_axes:
            score += 4.0
            reasons.append(f"{keyword['name']} can hold repeated surfaces.")
    if any(term in text for term in ["accent", "action", "signal", "flash", "energy", "masthead", "cover", "selected"]):
        if family in {"standard", "pantone_trend"} or "high_chroma" in tone_axes:
            score += 4.0
            reasons.append(f"{keyword['name']} can carry limited signal.")
    if any(term in text for term in ["border", "line", "separator", "edge"]):
        if "low_chroma" in tone_axes or family in {"pastel", "natural"}:
            score += 2.5
            reasons.append(f"{keyword['name']} is restrained enough for edges.")

    if variant["surface_bias"] == "airy" and (family == "pastel" or "high_value" in tone_axes):
        score += 1.4
    if variant["surface_bias"] == "grounded" and (family == "deep" or "low_value" in tone_axes):
        score += 1.4
    if variant["contrast_bias"] == "vivid" and ("high_chroma" in tone_axes or family in {"standard", "pantone_trend"}):
        score += 1.2
    if variant["contrast_bias"] == "soft" and ("low_chroma" in tone_axes or family in {"pastel", "natural"}):
        score += 1.2
    if spectrum == "neutral":
        score -= 0.5

    return score, reasons


def _diversity_score(keyword: dict[str, Any], selected_spectrums: list[str], variant: dict[str, Any]) -> float:
    if not selected_spectrums:
        return 0.0
    spectrum = keyword.get("spectrum")
    same_count = selected_spectrums.count(spectrum)
    if variant["diversity_bias"] == "cohesive":
        return 0.5 if same_count else 0.0
    if variant["diversity_bias"] == "exploratory":
        return 1.5 if not same_count else -1.0 * same_count
    return 0.75 if not same_count else -0.35 * same_count


def _variant_offset(variant: dict[str, Any], role_index: int, ranked_count: int) -> int:
    if ranked_count <= 1:
        return 0
    if variant["id"] == "best-fit":
        return 0
    return min((role_index + ROLE_VARIANTS.index(variant)) % min(ranked_count, 6), ranked_count - 1)


def _dedupe_candidates(candidates: list[dict[str, Any]]) -> list[dict[str, Any]]:
    deduped: list[dict[str, Any]] = []
    seen: set[tuple[str, ...]] = set()
    for candidate in candidates:
        signature = tuple(item["id"] for item in candidate.get("roles", {}).values())
        if signature in seen:
            continue
        seen.add(signature)
        deduped.append(candidate)
    return deduped


def _compact_keyword_node(node: dict[str, Any]) -> dict[str, Any]:
    props = node.get("properties", {})
    return {
        "id": node.get("id"),
        "name": props.get("label"),
        "hex": props.get("rgb_hex"),
        "spectrum": props.get("spectrum"),
        "family": props.get("family"),
        "category": props.get("category"),
        "mood_tags": props.get("mood_tags", []),
        "tone_axes": props.get("tone_axes", []),
        "summary": props.get("summary"),
    }


def _compact_pattern(node: dict[str, Any]) -> dict[str, Any]:
    props = node.get("properties", {})
    return {
        "id": node.get("id"),
        "label": props.get("label"),
        "summary": props.get("summary"),
        "brief_question": props.get("brief_question"),
        "output_medium": props.get("output_medium"),
        "role_model": props.get("role_model"),
    }


def _node_haystack(props: dict[str, Any]) -> str:
    values: list[str] = []
    for value in props.values():
        values.extend(_flatten_text(value))
    return " ".join(values).lower()


def _keyword_haystack(keyword: dict[str, Any]) -> str:
    return " ".join(_flatten_text(keyword)).lower()


def _term_score(terms: set[str], haystack: str) -> float:
    score = 0.0
    for term in sorted(terms, key=len, reverse=True):
        if not term or term not in haystack:
            continue
        score += 2.0 if len(term) > 2 else 0.5
    return score


def _tokenize_values(values: list[str]) -> set[str]:
    terms: set[str] = set()
    for value in values:
        for token in TEXT_TOKEN_RE.findall(str(value).lower()):
            terms.add(token)
    return terms


def _flatten_text(value: Any) -> list[str]:
    if value is None:
        return []
    if isinstance(value, str):
        return [value]
    if isinstance(value, dict):
        values: list[str] = []
        for nested in value.values():
            values.extend(_flatten_text(nested))
        return values
    if isinstance(value, (list, tuple, set)):
        values = []
        for nested in value:
            values.extend(_flatten_text(nested))
        return values
    return [str(value)]


def _semantic_expansions(term: str) -> set[str]:
    expansion_map = {
        "manga": {"editorial", "pop", "issue", "energy", "reading", "red", "yellow", "violet"},
        "만화": {"editorial", "pop", "issue", "energy", "reading", "red", "yellow", "violet"},
        "magazine": {"editorial", "issue", "reading", "masthead", "paper"},
        "매거진": {"editorial", "issue", "reading", "masthead", "paper"},
        "service": {"stable", "surface", "ui", "green", "calm", "operations"},
        "서비스": {"stable", "surface", "ui", "green", "calm", "operations"},
        "ui": {"surface", "interface", "selected", "state"},
        "dashboard": {"surface", "data", "table", "status", "operations"},
        "ops": {"operations", "status", "stable", "surface"},
        "green": {"stable", "surface", "calm", "trust"},
        "그린": {"stable", "surface", "calm", "trust"},
        "blue": {"trust", "focus", "deep", "cold", "brand"},
        "블루": {"trust", "focus", "deep", "cold", "brand"},
        "luxury": {"deep", "classic", "authority", "editorial"},
        "럭셔리": {"deep", "classic", "authority", "editorial"},
        "editorial": {"reading", "hierarchy", "classic", "feature"},
        "calm": {"stable", "soft", "low_chroma", "pastel"},
        "trustworthy": {"trust", "stable", "deep", "authority"},
        "bold": {"energy", "signal", "high_chroma", "standard"},
    }
    return expansion_map.get(term.lower(), set())


def _unique_strings(values: list[str]) -> list[str]:
    seen: set[str] = set()
    out: list[str] = []
    for value in values:
        if not value or value in seen:
            continue
        seen.add(value)
        out.append(value)
    return out
