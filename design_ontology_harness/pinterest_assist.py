from __future__ import annotations

from pathlib import Path

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
CAPTURE_IMAGE_EXTENSIONS = {
    ".png",
    ".jpg",
    ".jpeg",
    ".webp",
    ".gif",
    ".bmp",
}
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


def build_pinterest_assist_bundle(
    brand_profile: dict,
    query_report: dict,
    project_dir: Path | None = None,
    captured_candidates: dict[str, list[dict]] | None = None,
    existing_candidate_manifest: dict | None = None,
    existing_selection_manifest: dict | None = None,
) -> dict:
    visual_reference = brand_profile.get("visual_reference") or {}
    config = _normalize_pinterest_assist_config(visual_reference)
    query_entries = _normalize_query_entries(query_report)
    progress = _discover_capture_progress(
        visual_reference=visual_reference,
        config=config,
        query_entries=query_entries,
        project_dir=project_dir,
        existing_selection_manifest=existing_selection_manifest,
    )

    return {
        "config": config,
        "plan": _build_plan(brand_profile, config, query_entries, progress),
        "candidate_manifest": _build_candidate_manifest(
            config,
            query_entries,
            progress,
            captured_candidates=captured_candidates,
            existing_candidate_manifest=existing_candidate_manifest,
        ),
        "selection_manifest": _build_selection_manifest(
            config,
            query_entries,
            progress,
            existing_selection_manifest=existing_selection_manifest,
        ),
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


def _build_plan(brand_profile: dict, config: dict, query_entries: list[dict], progress: dict) -> dict:
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
        "capture_progress": {
            "status": progress["status"],
            "capture_root": progress["capture_root"],
            "captured_count": progress["captured_count"],
            "selected_count": progress["selected_count"],
            "promoted_count": progress["promoted_count"],
        },
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


def _build_candidate_manifest(
    config: dict,
    query_entries: list[dict],
    progress: dict,
    *,
    captured_candidates: dict[str, list[dict]] | None = None,
    existing_candidate_manifest: dict | None = None,
) -> dict:
    return {
        "mode": "pinterest-assisted",
        "status": progress["status"],
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
                "candidates": _candidate_slots_for_query(
                    item,
                    config,
                    progress,
                    captured_candidates=captured_candidates,
                    existing_candidate_manifest=existing_candidate_manifest,
                ),
            }
            for item in query_entries
        ],
    }


def _build_selection_manifest(
    config: dict,
    query_entries: list[dict],
    progress: dict,
    *,
    existing_selection_manifest: dict | None = None,
) -> dict:
    return {
        "mode": "pinterest-assisted",
        "status": "selected" if progress["selected_count"] else "ready-for-selection" if progress["captured_count"] else "awaiting-selection",
        "selection_rule": "Only explicitly selected captures may be copied into visual_reference.sources.",
        "capture_dir": config["capture_dir"],
        "usage_scope": "reference-analysis-only",
        "risk_guardrails": PINTEREST_RISK_GUARDRAILS,
        "queries": [
            {
                "query_id": item["query_id"],
                "query": item["query"],
                "selected": _selected_slots_for_query(
                    item,
                    config,
                    progress,
                    existing_selection_manifest=existing_selection_manifest,
                ),
            }
            for item in query_entries
        ],
    }


def _candidate_slots_for_query(
    item: dict,
    config: dict,
    progress: dict,
    *,
    captured_candidates: dict[str, list[dict]] | None = None,
    existing_candidate_manifest: dict | None = None,
) -> list[dict]:
    captures = progress["captures_by_query"].get(item["query_id"], [])
    selected_candidate_ids = progress["selected_candidate_ids"]
    captured_lookup = _index_query_candidates(captured_candidates or {}, item["query_id"])
    existing_lookup = _index_existing_candidates(existing_candidate_manifest, item["query_id"])
    candidates: list[dict] = []
    for slot in range(1, config["max_candidates_per_query"] + 1):
        capture = captures[slot - 1] if slot - 1 < len(captures) else None
        candidate_id = f"{item['query_id']}-c{slot:02d}"
        if capture:
            existing = captured_lookup.get(candidate_id) or existing_lookup.get(candidate_id) or existing_lookup.get(capture["relative_path"]) or {}
            candidates.append(
                {
                    "candidate_id": candidate_id,
                    "status": "captured",
                    "source_type": existing.get("source_type", "local-capture"),
                    "platform": existing.get("platform", "pinterest-assisted"),
                    "board_url": existing.get("board_url"),
                    "pin_url": existing.get("pin_url"),
                    "reference_url": existing.get("reference_url"),
                    "search_url": existing.get("search_url"),
                    "capture_path": capture["relative_path"],
                    "thumbnail_path": capture["relative_path"],
                    "capture_method": existing.get("capture_method", "screenshot"),
                    "usage_scope": "reference-analysis-only",
                    "redistribution_allowed": False,
                    "access_notes": existing.get("access_notes", "Discovered from the local Pinterest-assisted capture directory."),
                    "notes": existing.get("notes"),
                    "selected": capture["candidate_id"] in selected_candidate_ids,
                    "preview_url": existing.get("preview_url"),
                    "alt_text": existing.get("alt_text"),
                    "tile_box": existing.get("tile_box"),
                }
            )
            continue
        candidates.append(
            {
                "candidate_id": candidate_id,
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
        )
    return candidates


def _selected_slots_for_query(
    item: dict,
    config: dict,
    progress: dict,
    *,
    existing_selection_manifest: dict | None = None,
) -> list[dict]:
    captures = progress["captures_by_query"].get(item["query_id"], [])
    existing_entries = _selection_entries_for_query(existing_selection_manifest, item["query_id"])
    selected_captures = [
        capture
        for capture in captures
        if capture["candidate_id"] in progress["selected_candidate_ids"]
    ]
    promoted_paths = progress["promoted_paths"]
    used_candidate_ids: set[str] = set()

    selections: list[dict] = []
    for slot in range(1, config["max_selected_per_query"] + 1):
        selection_id = f"{item['query_id']}-s{slot:02d}"
        existing = existing_entries[slot - 1] if slot - 1 < len(existing_entries) else {}
        if str(existing.get("status", "")).strip().lower() == "selected":
            capture = _match_selection_to_capture(existing, captures)
            if capture:
                used_candidate_ids.add(capture["candidate_id"])
                selections.append(
                    _build_selected_selection_entry(
                        selection_id=selection_id,
                        capture=capture,
                        existing=existing,
                        promoted_to_sources=capture["resolved_path"] in promoted_paths,
                    )
                )
                continue
            selections.append(_build_missing_capture_selection_entry(selection_id=selection_id, existing=existing))
            continue

        capture = next(
            (candidate for candidate in selected_captures if candidate["candidate_id"] not in used_candidate_ids),
            None,
        )
        if capture:
            used_candidate_ids.add(capture["candidate_id"])
            selections.append(
                _build_selected_selection_entry(
                    selection_id=selection_id,
                    capture=capture,
                    existing={},
                    promoted_to_sources=capture["resolved_path"] in promoted_paths,
                )
            )
            continue

        selections.append(_build_open_selection_entry(selection_id))
    return selections


def _discover_capture_progress(
    visual_reference: dict,
    config: dict,
    query_entries: list[dict],
    project_dir: Path | None,
    existing_selection_manifest: dict | None = None,
) -> dict:
    capture_root = _resolve_capture_root(project_dir, config["capture_dir"])
    promoted_paths = _resolve_selected_paths(visual_reference, project_dir)

    captures_by_query: dict[str, list[dict]] = {item["query_id"]: [] for item in query_entries}
    if capture_root and capture_root.exists():
        for path in sorted(capture_root.rglob("*")):
            if not path.is_file() or path.suffix.lower() not in CAPTURE_IMAGE_EXTENSIONS:
                continue
            query_entry = _match_capture_to_query(path, capture_root, query_entries)
            if not query_entry:
                continue
            capture_index = len(captures_by_query[query_entry["query_id"]]) + 1
            candidate_id = _candidate_id_from_path(path, query_entry["query_id"], capture_index)
            captures_by_query[query_entry["query_id"]].append(
                {
                    "candidate_id": candidate_id,
                    "resolved_path": str(path.resolve()),
                    "relative_path": str(path.resolve().relative_to(project_dir.resolve())) if project_dir else str(path.resolve()),
                }
            )

    captured_count = sum(len(items) for items in captures_by_query.values())
    promoted_candidate_ids = {
        capture["candidate_id"]
        for captures in captures_by_query.values()
        for capture in captures
        if capture["resolved_path"] in promoted_paths
    }
    selected_candidate_ids = set(promoted_candidate_ids)
    selected_paths = set(promoted_paths)

    for query_entry in query_entries:
        for selection in _selection_entries_for_query(existing_selection_manifest, query_entry["query_id"]):
            if str(selection.get("status", "")).strip().lower() != "selected":
                continue
            capture = _match_selection_to_capture(selection, captures_by_query.get(query_entry["query_id"], []))
            if not capture:
                continue
            selected_candidate_ids.add(capture["candidate_id"])
            selected_paths.add(capture["resolved_path"])

    selected_count = len(selected_candidate_ids)
    promoted_count = len(promoted_candidate_ids)

    if selected_count:
        status = "selected"
    elif captured_count:
        status = "ready-for-selection"
    else:
        status = "draft"

    return {
        "capture_root": str(capture_root.relative_to(project_dir.resolve())) if capture_root and project_dir else str(capture_root) if capture_root else config["capture_dir"],
        "captures_by_query": captures_by_query,
        "captured_count": captured_count,
        "selected_count": selected_count,
        "promoted_count": promoted_count,
        "selected_paths": selected_paths,
        "selected_candidate_ids": selected_candidate_ids,
        "promoted_paths": promoted_paths,
        "promoted_candidate_ids": promoted_candidate_ids,
        "status": status,
    }


def _resolve_capture_root(project_dir: Path | None, capture_dir: str) -> Path | None:
    if not capture_dir:
        return None
    root = Path(capture_dir)
    if root.is_absolute() or not project_dir:
        return root.resolve()
    return (project_dir / root).resolve()


def _resolve_selected_paths(visual_reference: dict, project_dir: Path | None) -> set[str]:
    selected_paths: set[str] = set()
    for source in visual_reference.get("sources", []) if isinstance(visual_reference.get("sources", []), list) else []:
        if isinstance(source, str):
            raw_path = source.strip()
        elif isinstance(source, dict):
            raw_path = str(source.get("path", "")).strip()
        else:
            raw_path = ""
        if not raw_path:
            continue
        path = Path(raw_path)
        if not path.is_absolute() and project_dir:
            path = (project_dir / path).resolve()
        selected_paths.add(str(path.resolve()))
    return selected_paths


def _match_capture_to_query(path: Path, capture_root: Path, query_entries: list[dict]) -> dict | None:
    relative_text = str(path.relative_to(capture_root)).lower()
    for item in query_entries:
        if item["query_slug"].lower() in relative_text or item["query_id"].lower() in relative_text:
            return item
    return None


def _candidate_id_from_path(path: Path, query_id: str, fallback_index: int) -> str:
    stem = path.stem.lower()
    prefix = f"{query_id.lower()}-c"
    if stem.startswith(prefix):
        return path.stem
    return f"{query_id}-c{fallback_index:02d}"


def _index_query_candidates(captured_candidates: dict[str, list[dict]], query_id: str) -> dict[str, dict]:
    return {
        str(item.get("candidate_id", "")).strip(): item
        for item in captured_candidates.get(query_id, [])
        if str(item.get("candidate_id", "")).strip()
    }


def _index_existing_candidates(existing_candidate_manifest: dict | None, query_id: str) -> dict[str, dict]:
    if not isinstance(existing_candidate_manifest, dict):
        return {}
    lookup: dict[str, dict] = {}
    for query in existing_candidate_manifest.get("queries", []):
        if str(query.get("query_id", "")).strip() != query_id:
            continue
        for candidate in query.get("candidates", []):
            candidate_id = str(candidate.get("candidate_id", "")).strip()
            capture_path = str(candidate.get("capture_path", "")).strip()
            if candidate_id:
                lookup[candidate_id] = candidate
            if capture_path:
                lookup[capture_path] = candidate
    return lookup


def _index_existing_selections(existing_selection_manifest: dict | None, query_id: str) -> dict[str, dict]:
    if not isinstance(existing_selection_manifest, dict):
        return {}
    lookup: dict[str, dict] = {}
    for query in existing_selection_manifest.get("queries", []):
        if str(query.get("query_id", "")).strip() != query_id:
            continue
        for selection in query.get("selected", []):
            selection_id = str(selection.get("selection_id", "")).strip()
            if selection_id:
                lookup[selection_id] = selection
    return lookup


def _selection_entries_for_query(existing_selection_manifest: dict | None, query_id: str) -> list[dict]:
    if not isinstance(existing_selection_manifest, dict):
        return []
    for query in existing_selection_manifest.get("queries", []):
        if str(query.get("query_id", "")).strip() == query_id:
            return list(query.get("selected", []))
    return []


def _match_selection_to_capture(selection: dict, captures: list[dict]) -> dict | None:
    candidate_id = str(selection.get("candidate_id", "")).strip()
    if candidate_id:
        for capture in captures:
            if capture["candidate_id"] == candidate_id:
                return capture

    capture_path = str(selection.get("capture_path", "")).strip()
    if capture_path:
        for capture in captures:
            if capture_path in {capture["relative_path"], capture["resolved_path"]}:
                return capture

    return None


def _build_selected_selection_entry(
    selection_id: str,
    capture: dict,
    existing: dict,
    *,
    promoted_to_sources: bool,
) -> dict:
    return {
        "selection_id": selection_id,
        "status": "selected",
        "candidate_id": capture["candidate_id"],
        "reference_url": existing.get("reference_url"),
        "capture_path": capture["relative_path"],
        "usage_scope": "reference-analysis-only",
        "redistribution_allowed": False,
        "selection_reason": existing.get(
            "selection_reason",
            "Already promoted into visual_reference.sources."
            if promoted_to_sources
            else "Explicitly selected for promotion to visual_reference.sources.",
        ),
        "notes": existing.get("notes"),
        "promoted_to_sources": promoted_to_sources,
    }


def _build_missing_capture_selection_entry(selection_id: str, existing: dict) -> dict:
    return {
        "selection_id": selection_id,
        "status": "missing-capture",
        "candidate_id": existing.get("candidate_id"),
        "reference_url": existing.get("reference_url"),
        "capture_path": existing.get("capture_path"),
        "usage_scope": "reference-analysis-only",
        "redistribution_allowed": False,
        "selection_reason": existing.get("selection_reason"),
        "notes": existing.get("notes"),
        "promoted_to_sources": False,
    }


def _build_open_selection_entry(selection_id: str) -> dict:
    return {
        "selection_id": selection_id,
        "status": "open",
        "candidate_id": None,
        "reference_url": None,
        "capture_path": None,
        "usage_scope": "reference-analysis-only",
        "redistribution_allowed": False,
        "selection_reason": None,
        "notes": None,
        "promoted_to_sources": False,
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
