from __future__ import annotations

from .spec_analyzer import analyze_spec
from .utils import clean_text

STYLE_KEYWORD_ALIASES = {
    "calm": "calm quiet",
    "precise": "precise structured",
    "editorial": "editorial text-first",
    "trustworthy": "trustworthy measured",
    "bold": "bold high-contrast",
    "minimal": "minimal clean",
    "premium": "premium refined",
    "playful": "playful expressive",
    "warm": "warm",
    "cool": "cool",
}

PRIMITIVE_QUERY_TEMPLATES: dict[str, list[dict[str, str]]] = {
    "workspace navigation": [
        {"phrase": "workspace app shell ui", "intent": "layout"},
        {"phrase": "split pane workspace navigation", "intent": "navigation"},
    ],
    "rich text editor": [
        {"phrase": "content authoring editor ui", "intent": "editor"},
        {"phrase": "document writing interface", "intent": "editor"},
    ],
    "command palette": [
        {"phrase": "command palette overlay ui", "intent": "overlay"},
        {"phrase": "spotlight quick action interface", "intent": "interaction"},
    ],
    "dashboard cards": [
        {"phrase": "analytics dashboard cards", "intent": "data-display"},
        {"phrase": "operations insight panel ui", "intent": "data-display"},
    ],
    "data tables": [
        {"phrase": "data review table ui", "intent": "data-display"},
        {"phrase": "operations control panel", "intent": "data-display"},
    ],
    "forms": [
        {"phrase": "settings form ui", "intent": "input"},
        {"phrase": "structured form layout", "intent": "input"},
    ],
    "notifications": [
        {"phrase": "product feedback banner ui", "intent": "feedback"},
        {"phrase": "toast and alert system ui", "intent": "feedback"},
    ],
    "file upload": [
        {"phrase": "file upload dropzone ui", "intent": "input"},
        {"phrase": "media upload interface", "intent": "input"},
    ],
    "calendar and dates": [
        {"phrase": "calendar scheduling interface", "intent": "date"},
        {"phrase": "date range picker ui", "intent": "date"},
    ],
    "charts and visualization": [
        {"phrase": "analytics chart panel ui", "intent": "data-display"},
        {"phrase": "dashboard data visualization", "intent": "data-display"},
    ],
    "user profile and avatar": [
        {"phrase": "profile card ui", "intent": "profile"},
        {"phrase": "account menu interface", "intent": "profile"},
    ],
    "comments and discussion": [
        {"phrase": "comment thread interface", "intent": "discussion"},
        {"phrase": "collaboration feedback panel", "intent": "discussion"},
    ],
    "tags and labels": [
        {"phrase": "status tag chip ui", "intent": "feedback"},
        {"phrase": "filter chip interface", "intent": "input"},
    ],
    "search and filter": [
        {"phrase": "faceted search interface", "intent": "input"},
        {"phrase": "filter toolbar ui", "intent": "input"},
    ],
    "modal and dialog": [
        {"phrase": "modal drawer interface", "intent": "overlay"},
        {"phrase": "confirmation dialog ui", "intent": "overlay"},
    ],
    "onboarding and stepper": [
        {"phrase": "onboarding flow ui", "intent": "flow"},
        {"phrase": "stepper wizard interface", "intent": "flow"},
    ],
    "pricing and plans": [
        {"phrase": "pricing comparison cards", "intent": "marketing"},
        {"phrase": "subscription plans ui", "intent": "marketing"},
    ],
    "kanban and board": [
        {"phrase": "kanban board ui", "intent": "data-display"},
        {"phrase": "project board interface", "intent": "data-display"},
    ],
    "chat and messaging": [
        {"phrase": "chat side panel ui", "intent": "discussion"},
        {"phrase": "messaging thread interface", "intent": "discussion"},
    ],
    "media player": [
        {"phrase": "video player controls ui", "intent": "media"},
        {"phrase": "streaming playback interface", "intent": "media"},
    ],
    "hero section": [
        {"phrase": "saas landing hero", "intent": "marketing"},
        {"phrase": "product hero layout", "intent": "marketing"},
    ],
    "feature grid": [
        {"phrase": "feature grid landing page", "intent": "marketing"},
        {"phrase": "product capability cards", "intent": "marketing"},
    ],
    "social proof": [
        {"phrase": "logo cloud social proof", "intent": "marketing"},
        {"phrase": "trusted by strip ui", "intent": "marketing"},
    ],
    "testimonial": [
        {"phrase": "testimonial card section", "intent": "marketing"},
        {"phrase": "customer quote layout", "intent": "marketing"},
    ],
    "faq accordion": [
        {"phrase": "faq accordion ui", "intent": "marketing"},
        {"phrase": "question answer section", "intent": "marketing"},
    ],
    "landing cta section": [
        {"phrase": "conversion cta section", "intent": "marketing"},
        {"phrase": "signup banner ui", "intent": "marketing"},
    ],
    "site footer": [
        {"phrase": "marketing footer ui", "intent": "marketing"},
        {"phrase": "site footer link layout", "intent": "marketing"},
    ],
    "site header": [
        {"phrase": "marketing top navigation", "intent": "marketing"},
        {"phrase": "landing header nav ui", "intent": "marketing"},
    ],
}


def generate_visual_queries(
    brand_profile: dict,
    spec_text: str | None = None,
    limit: int = 16,
) -> dict:
    limit = max(6, min(24, int(limit or 16)))
    detected_patterns = analyze_spec(spec_text) if spec_text else []
    active_primitives = _collect_active_primitives(brand_profile, detected_patterns)
    density_hint = _infer_density_hint(brand_profile, active_primitives)
    style_phrases = _collect_style_phrases(brand_profile, density_hint)
    avoid_terms = [str(item).strip().lower() for item in brand_profile.get("anti_keywords", []) if str(item).strip()]

    queries: list[dict] = []
    seen_queries: set[str] = set()

    for primitive in active_primitives:
        for template in _templates_for_primitive(primitive)[:2]:
            style_entry = style_phrases[len(queries) % len(style_phrases)] if style_phrases else None
            parts: list[str] = []
            sources = [f"primitive:{primitive}"]
            if style_entry:
                parts.append(style_entry["phrase"])
                sources.extend(style_entry["sources"])
            parts.append(template["phrase"])
            query = _merge_query_parts(parts)
            _push_query(
                queries=queries,
                seen_queries=seen_queries,
                query=query,
                primitive=primitive,
                intent=template["intent"],
                sources=sources,
                limit=limit,
            )
            if len(queries) >= limit:
                break
        if len(queries) >= limit:
            break

    for fallback in _build_crosscutting_queries(style_phrases, active_primitives, density_hint):
        _push_query(
            queries=queries,
            seen_queries=seen_queries,
            query=fallback["query"],
            primitive=fallback["primitive"],
            intent=fallback["intent"],
            sources=fallback["sources"],
            limit=limit,
        )
        if len(queries) >= limit:
            break

    return {
        "query_count": len(queries),
        "queries": queries,
        "style_axes": {
            "brand_keywords": brand_profile.get("brand_keywords", []),
            "visual_keywords": brand_profile.get("visual_keywords", []),
            "interaction_keywords": brand_profile.get("interaction_keywords", []),
            "temperature_hint": _extract_palette_temperature(brand_profile),
            "surface_hint": _extract_surface_style(brand_profile),
            "density_hint": density_hint,
        },
        "active_primitives": active_primitives,
        "avoid_terms": avoid_terms,
        "detected_patterns": [
            {
                "pattern": item["pattern"],
                "confidence": item["confidence"],
                "matched_terms": item["matched_terms"][:6],
            }
            for item in detected_patterns[:8]
        ],
    }


def _collect_active_primitives(brand_profile: dict, detected_patterns: list[dict]) -> list[str]:
    ordered: list[str] = []
    seen: set[str] = set()

    for item in detected_patterns:
        pattern = str(item.get("pattern", "")).strip().lower()
        if pattern and pattern not in seen:
            seen.add(pattern)
            ordered.append(pattern)

    for primitive in brand_profile.get("product_primitives", []):
        normalized = str(primitive).strip().lower()
        if normalized and normalized not in seen:
            seen.add(normalized)
            ordered.append(normalized)

    if ordered:
        return ordered[:10]

    return [
        "workspace navigation",
        "dashboard cards",
        "hero section",
    ]


def _collect_style_phrases(brand_profile: dict, density_hint: str | None) -> list[dict]:
    phrases: list[dict] = []
    seen: set[str] = set()
    brand_keywords = [str(item).strip().lower() for item in brand_profile.get("brand_keywords", []) if str(item).strip()]
    visual_keywords = [clean_text(str(item)).lower() for item in brand_profile.get("visual_keywords", []) if str(item).strip()]

    def add(phrase: str, sources: list[str]) -> None:
        normalized = clean_text(phrase).lower()
        if not normalized or normalized in seen:
            return
        seen.add(normalized)
        phrases.append({"phrase": normalized, "sources": sources})

    if "editorial" in brand_keywords and "precise" in brand_keywords:
        add("editorial precise", ["brand_keyword:editorial", "brand_keyword:precise"])
    if "calm" in brand_keywords and "trustworthy" in brand_keywords:
        add("calm trustworthy", ["brand_keyword:calm", "brand_keyword:trustworthy"])

    for keyword in brand_keywords:
        if keyword in STYLE_KEYWORD_ALIASES:
            add(STYLE_KEYWORD_ALIASES[keyword], [f"brand_keyword:{keyword}"])

    for keyword in visual_keywords[:3]:
        add(keyword, [f"visual_keyword:{keyword}"])

    temperature = _extract_palette_temperature(brand_profile)
    surface_style = _extract_surface_style(brand_profile)
    if temperature or surface_style:
        combined = clean_text(" ".join(part for part in [temperature, surface_style] if part))
        sources = []
        if temperature:
            sources.append(f"palette_temperature:{temperature}")
        if surface_style:
            sources.append(f"surface_style:{surface_style}")
        add(combined, sources)

    if density_hint == "dense":
        add("dense operations", ["density_hint:dense"])
    elif density_hint == "airy":
        add("airy editorial", ["density_hint:airy"])
    else:
        add("balanced product", ["density_hint:balanced"])

    return phrases[:6]


def _templates_for_primitive(primitive: str) -> list[dict[str, str]]:
    templates = PRIMITIVE_QUERY_TEMPLATES.get(primitive.lower())
    if templates:
        return templates

    normalized = primitive.lower()
    if any(token in normalized for token in ["dashboard", "table", "chart", "analytics", "data"]):
        return [{"phrase": f"{normalized} ui", "intent": "data-display"}]
    if any(token in normalized for token in ["hero", "landing", "pricing", "testimonial", "faq", "footer", "header"]):
        return [{"phrase": f"{normalized} layout", "intent": "marketing"}]
    if any(token in normalized for token in ["nav", "sidebar", "menu", "breadcrumb", "toolbar"]):
        return [{"phrase": f"{normalized} interface", "intent": "navigation"}]
    return [{"phrase": f"{normalized} interface", "intent": "general"}]


def _build_crosscutting_queries(
    style_phrases: list[dict],
    active_primitives: list[str],
    density_hint: str | None,
) -> list[dict]:
    results: list[dict] = []
    if not style_phrases:
        return results

    primary_style = style_phrases[0]
    has_marketing = any(
        primitive in {
            "hero section",
            "feature grid",
            "social proof",
            "testimonial",
            "pricing and plans",
            "landing cta section",
            "site header",
            "site footer",
        }
        for primitive in active_primitives
    )
    has_data = any(
        primitive in {
            "workspace navigation",
            "dashboard cards",
            "data tables",
            "charts and visualization",
            "search and filter",
            "command palette",
        }
        for primitive in active_primitives
    )

    if has_data:
        results.append(
            {
                "query": clean_text(f"{primary_style['phrase']} data dense dashboard ui" if density_hint == "dense" else f"{primary_style['phrase']} product dashboard ui").lower(),
                "primitive": "crosscutting:data-workspace",
                "intent": "layout",
                "sources": primary_style["sources"] + [f"density_hint:{density_hint or 'balanced'}"],
            }
        )
    if has_marketing:
        results.append(
            {
                "query": clean_text(f"{primary_style['phrase']} saas landing page").lower(),
                "primitive": "crosscutting:marketing",
                "intent": "marketing",
                "sources": primary_style["sources"] + ["primitive_group:marketing"],
            }
        )

    return results


def _push_query(
    queries: list[dict],
    seen_queries: set[str],
    query: str,
    primitive: str,
    intent: str,
    sources: list[str],
    limit: int,
) -> None:
    normalized = clean_text(query).lower()
    if not normalized or normalized in seen_queries or len(queries) >= limit:
        return
    seen_queries.add(normalized)
    queries.append(
        {
            "query": normalized,
            "primitive": primitive,
            "intent": intent,
            "sources": list(dict.fromkeys(source for source in sources if source)),
        }
    )


def _infer_density_hint(brand_profile: dict, active_primitives: list[str]) -> str:
    brand_keywords = {str(item).strip().lower() for item in brand_profile.get("brand_keywords", [])}
    if "editorial" in brand_keywords and "calm" in brand_keywords:
        return "airy"

    dense_hits = sum(
        1
        for primitive in active_primitives
        if primitive in {
            "workspace navigation",
            "dashboard cards",
            "data tables",
            "charts and visualization",
            "search and filter",
            "command palette",
        }
    )
    marketing_hits = sum(
        1
        for primitive in active_primitives
        if primitive in {
            "hero section",
            "feature grid",
            "social proof",
            "testimonial",
            "landing cta section",
        }
    )
    if dense_hits >= 3:
        return "dense"
    if marketing_hits >= 3 and dense_hits <= 1:
        return "airy"
    return "balanced"


def _extract_palette_temperature(brand_profile: dict) -> str | None:
    color_reference = brand_profile.get("color_reference") or {}
    strategy = color_reference.get("palette_strategy") or {}
    temperature = str(strategy.get("temperature", "")).strip().lower()
    return temperature or None


def _extract_surface_style(brand_profile: dict) -> str | None:
    visual_reference = brand_profile.get("visual_reference") or {}
    surface = str(visual_reference.get("surface_style", "")).strip().lower()
    if surface:
        return surface
    color_reference = brand_profile.get("color_reference") or {}
    strategy = color_reference.get("palette_strategy") or {}
    surface = str(strategy.get("surface_style", "")).strip().lower()
    return surface or None


def _merge_query_parts(parts: list[str]) -> str:
    tokens: list[str] = []
    for part in parts:
        for token in clean_text(part).lower().split():
            if tokens and tokens[-1] == token:
                continue
            tokens.append(token)
    return " ".join(tokens)
