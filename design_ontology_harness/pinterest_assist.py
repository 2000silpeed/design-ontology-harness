from __future__ import annotations

from .utils import guess_file_safe_name

DEFAULT_PINTEREST_ASSIST = {
    "enabled": False,
    "capture_mode": "manual-save",
    "capture_dir": "references/visual/pinterest-assisted",
    "max_candidates_per_query": 6,
    "max_selected_per_query": 2,
    "preferred_sources": ["pins", "boards", "adjacent-search"],
    "notes": [],
}

VALID_CAPTURE_MODES = {"manual-save", "playwright-capture"}
VALID_PREFERRED_SOURCES = {"pins", "boards", "adjacent-search"}
PINTEREST_RISK_GUARDRAILS = [
    {
        "id": "auth-and-dynamic-loading",
        "title": "Login walls and dynamic loading",
        "detail": "Pinterest surfaces may require login, throttle scrolling, or change DOM structure at any time.",
        "policy": "Treat automation as best-effort only and keep manual-save as the default capture path.",
        "fallback": "If automation cannot access stable results, use manual screenshots or curated local references.",
    },
    {
        "id": "volatile-search-results",
        "title": "Search result volatility",
        "detail": "Search results can differ by session, geography, time, and account state.",
        "policy": "Record reference URLs as provenance only; do not expect exact reproducibility from a query alone.",
        "fallback": "Promote only explicit local captures into visual_reference.sources.",
    },
    {
        "id": "copyright-and-redistribution",
        "title": "Copyright and redistribution",
        "detail": "Captured boards or pins are reference material, not assets cleared for redistribution.",
        "policy": "Prefer screenshots and reference URLs over raw asset download, and mark usage as reference-analysis-only.",
        "fallback": "If reuse rights are unclear, keep the material out of shipped assets and documents intended for redistribution.",
    },
    {
        "id": "robots-and-access-constraints",
        "title": "Robots and access constraints",
        "detail": "When robots rules, auth prompts, or access restrictions block collection, the workflow must degrade gracefully.",
        "policy": "Do not bypass access controls; stop automated capture and continue with manual or alternate reference gathering.",
        "fallback": "Use official sites, existing local screenshots, or general image-search notes without scraping.",
    },
]


def build_pinterest_assist_bundle(brand_profile: dict, query_report: dict) -> dict:
    visual_reference = brand_profile.get("visual_reference") or {}
    config = _normalize_pinterest_assist_config(visual_reference)
    query_entries = _normalize_query_entries(query_report)

    return {
        "config": config,
        "plan": _build_plan(brand_profile, config, query_entries),
        "candidate_manifest": _build_candidate_manifest(config, query_entries),
        "selection_manifest": _build_selection_manifest(config, query_entries),
    }


def _normalize_pinterest_assist_config(visual_reference: dict) -> dict:
    raw = visual_reference.get("pinterest_assist") or {}
    config = dict(DEFAULT_PINTEREST_ASSIST)
    if isinstance(raw, dict):
        config["enabled"] = bool(raw.get("enabled", config["enabled"]))
        config["capture_mode"] = _pick_enum(raw.get("capture_mode"), VALID_CAPTURE_MODES, config["capture_mode"])
        capture_dir = str(raw.get("capture_dir", config["capture_dir"])).strip()
        config["capture_dir"] = capture_dir or config["capture_dir"]
        config["max_candidates_per_query"] = _clamp_int(raw.get("max_candidates_per_query"), 1, 12, config["max_candidates_per_query"])
        config["max_selected_per_query"] = _clamp_int(raw.get("max_selected_per_query"), 1, 4, config["max_selected_per_query"])
        preferred_sources = raw.get("preferred_sources")
        if isinstance(preferred_sources, list):
            normalized_sources = []
            for item in preferred_sources:
                source = str(item).strip().lower()
                if source in VALID_PREFERRED_SOURCES and source not in normalized_sources:
                    normalized_sources.append(source)
            if normalized_sources:
                config["preferred_sources"] = normalized_sources
        notes = raw.get("notes")
        if isinstance(notes, list):
            config["notes"] = [str(item).strip() for item in notes if str(item).strip()]

    mode = str(visual_reference.get("mode", "")).strip().lower()
    config["activation_state"] = "active" if config["enabled"] or mode == "pinterest-assisted" else "preview"
    config["mode"] = mode or "local-images"
    return config


def _normalize_query_entries(query_report: dict) -> list[dict]:
    entries = []
    for index, item in enumerate(query_report.get("queries", []), start=1):
        query = str(item.get("query", "")).strip()
        if not query:
            continue
        query_id = f"q{index:02d}"
        entries.append(
            {
                "query_id": query_id,
                "query": query,
                "intent": str(item.get("intent", "general")).strip() or "general",
                "primitive": str(item.get("primitive", "unknown")).strip() or "unknown",
                "sources": [str(source).strip() for source in item.get("sources", []) if str(source).strip()],
                "query_slug": guess_file_safe_name(query_id + "-" + query)[:80],
            }
        )
    return entries


def _build_plan(brand_profile: dict, config: dict, query_entries: list[dict]) -> dict:
    return {
        "mode": "pinterest-assisted",
        "activation_state": config["activation_state"],
        "capture_mode": config["capture_mode"],
        "capture_dir": config["capture_dir"],
        "query_count": len(query_entries),
        "brand_context": {
            "brand_name": brand_profile.get("brand_name"),
            "brand_keywords": brand_profile.get("brand_keywords", []),
            "anti_keywords": brand_profile.get("anti_keywords", []),
        },
        "purpose": "Pinterest-assisted search and shortlist support. Final visual analysis still consumes only explicit local files.",
        "artifact_outputs": [
            "build/visuals/pinterest_assist_plan.json",
            "build/visuals/pinterest_candidate_manifest.json",
            "build/visuals/pinterest_selection_manifest.json",
        ],
        "workflow": [
            {
                "step": 1,
                "title": "Generate search queries",
                "detail": "Use generate-visual-queries output as the canonical search prompt list.",
            },
            {
                "step": 2,
                "title": "Capture candidates",
                "detail": "Collect board/pin screenshots or saved reference images per query. Do not analyze URLs directly.",
            },
            {
                "step": 3,
                "title": "Explicitly lock selections",
                "detail": "A human or agent must explicitly choose which captures graduate from candidate -> selected.",
            },
            {
                "step": 4,
                "title": "Promote local files into visual_reference.sources",
                "detail": "Only selected local files should be connected to visual_reference.sources and analyzed by analyze-visuals.",
            },
        ],
        "review_rules": [
            "Pinterest is a search-assist layer, not the structural source of truth.",
            "Do not treat captured boards/pins as direct component specs or token sources.",
            "Prefer screenshot or saved-reference capture over raw asset download.",
            "Selections stay provisional until copied into local visual_reference.sources.",
        ],
        "risk_guardrails": PINTEREST_RISK_GUARDRAILS,
        "queries": [
            {
                "query_id": item["query_id"],
                "query": item["query"],
                "intent": item["intent"],
                "primitive": item["primitive"],
                "sources": item["sources"],
                "candidate_slots": config["max_candidates_per_query"],
                "selection_slots": config["max_selected_per_query"],
                "expected_capture_prefix": f"{config['capture_dir'].rstrip('/')}/{item['query_slug']}",
                "preferred_sources": config["preferred_sources"],
            }
            for item in query_entries
        ],
        "notes": config["notes"],
    }


def _build_candidate_manifest(config: dict, query_entries: list[dict]) -> dict:
    return {
        "mode": "pinterest-assisted",
        "status": "draft",
        "capture_mode": config["capture_mode"],
        "capture_dir": config["capture_dir"],
        "usage_scope": "reference-analysis-only",
        "risk_guardrails": PINTEREST_RISK_GUARDRAILS,
        "queries": [
            {
                "query_id": item["query_id"],
                "query": item["query"],
                "intent": item["intent"],
                "primitive": item["primitive"],
                "candidates": [
                    {
                        "candidate_id": f"{item['query_id']}-c{slot:02d}",
                        "status": "open",
                        "source_type": None,
                        "platform": "pinterest",
                        "board_url": None,
                        "pin_url": None,
                        "reference_url": None,
                        "capture_path": None,
                        "thumbnail_path": None,
                        "capture_method": "screenshot",
                        "usage_scope": "reference-analysis-only",
                        "redistribution_allowed": False,
                        "access_notes": None,
                        "notes": None,
                        "selected": False,
                    }
                    for slot in range(1, config["max_candidates_per_query"] + 1)
                ],
            }
            for item in query_entries
        ],
    }


def _build_selection_manifest(config: dict, query_entries: list[dict]) -> dict:
    return {
        "mode": "pinterest-assisted",
        "status": "awaiting-selection",
        "selection_rule": "Only explicitly selected captures may be copied into visual_reference.sources.",
        "capture_dir": config["capture_dir"],
        "usage_scope": "reference-analysis-only",
        "risk_guardrails": PINTEREST_RISK_GUARDRAILS,
        "queries": [
            {
                "query_id": item["query_id"],
                "query": item["query"],
                "selected": [
                    {
                        "selection_id": f"{item['query_id']}-s{slot:02d}",
                        "status": "open",
                        "candidate_id": None,
                        "reference_url": None,
                        "capture_path": None,
                        "usage_scope": "reference-analysis-only",
                        "redistribution_allowed": False,
                        "selection_reason": None,
                        "notes": None,
                    }
                    for slot in range(1, config["max_selected_per_query"] + 1)
                ],
            }
            for item in query_entries
        ],
    }


def _pick_enum(value: object, allowed: set[str], default: str) -> str:
    normalized = str(value).strip().lower()
    return normalized if normalized in allowed else default


def _clamp_int(value: object, minimum: int, maximum: int, default: int) -> int:
    if isinstance(value, bool):
        return default
    if isinstance(value, (int, float)):
        return max(minimum, min(maximum, int(value)))
    return default
