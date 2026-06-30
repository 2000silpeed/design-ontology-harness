from __future__ import annotations

from collections import Counter
from typing import Any


DESIGN_CONTEXT_SCHEMA_VERSION = "design-context-pack/v1"

REFERENCE_ABSORPTION_POLICY = {
    "authority_order": [
        "product task flow and information architecture",
        "token_schema.json and generated CSS variables",
        "components/component_specs.* and component_inventory.json",
        "system_spec.md and system_ontology.json",
        "external reference context",
    ],
    "allowed": [
        "component morphology",
        "layout density",
        "panel/card proportions",
        "hierarchy rhythm",
        "interaction affordance patterns",
        "flow pattern labels",
    ],
    "denied": [
        "color palette",
        "palette composition",
        "typography scale",
        "domain information architecture",
        "product copy",
        "redistributable imagery unless explicitly licensed",
    ],
    "rule": "Reference context is research input only; it never overrides product IA, tokens, component specs, or governance.",
}

PROVIDER_REGISTRY = {
    "local-images": {
        "label": "Local visual references",
        "kind": "local-images",
        "access_mode": "local-files",
        "default_status": "active",
        "truth_role": "observed morphology evidence",
    },
    "pinterest": {
        "label": "Pinterest-assisted capture",
        "kind": "pinterest",
        "access_mode": "manual-or-playwright-capture",
        "default_status": "preview",
        "truth_role": "search assist and shortlist support",
    },
    "lazyweb": {
        "label": "Lazyweb MCP real-app corpus",
        "kind": "lazyweb",
        "access_mode": "mcp-or-manual-export",
        "default_status": "suggested",
        "truth_role": "real app flow and screen corpus provider",
    },
    "figma": {
        "label": "Figma reference file",
        "kind": "figma",
        "access_mode": "mcp-or-exported-screens",
        "default_status": "suggested",
        "truth_role": "approved design source or competitive analysis export",
    },
    "uploaded-screenshots": {
        "label": "Uploaded screenshots",
        "kind": "uploaded-screenshots",
        "access_mode": "local-files",
        "default_status": "active",
        "truth_role": "human-selected screenshot evidence",
    },
    "website-inspection": {
        "label": "Website reference inspection",
        "kind": "website-inspection",
        "access_mode": "playwright-capture",
        "default_status": "active",
        "truth_role": "observed web page topology, behavior, and morphology evidence",
    },
}

FLOW_KEYWORDS = {
    "onboarding": {"onboarding", "welcome", "signup", "profile", "setup", "tutorial", "permission"},
    "pricing": {"pricing", "paywall", "subscription", "checkout", "plan", "billing"},
    "messaging": {"chat", "message", "conversation", "assistant", "thread", "inbox"},
    "dashboard": {"dashboard", "analytics", "metric", "chart", "kpi", "monitoring", "ops"},
    "data-review": {"table", "grid", "audit", "log", "records", "comparison", "review", "policy"},
    "document": {"document", "editor", "article", "content", "writing", "redline", "citation"},
    "settings": {"settings", "account", "profile", "preferences", "admin", "security"},
    "empty-state": {"empty", "blank", "no-results", "success", "error", "loading"},
    "navigation": {"workspace", "sidebar", "shell", "navigation", "topbar", "breadcrumb"},
}

MORPHOLOGY_KEYWORDS = {
    "split-pane": {"split", "pane", "sidebar", "sidecar", "drawer", "inspector"},
    "dense-table": {"table", "grid", "matrix", "audit", "records", "policy"},
    "card-stack": {"card", "panel", "module", "tile", "summary"},
    "timeline": {"timeline", "activity", "history", "audit", "log"},
    "composer": {"composer", "prompt", "input", "message", "command"},
    "evidence": {"citation", "source", "evidence", "reference", "proof"},
}


def build_design_context_pack(
    brand_profile: dict[str, Any],
    visual_reference: dict[str, Any] | None = None,
    query_report: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Build a provider-neutral reference intelligence layer.

    The pack is deliberately conservative: it captures where reference signals
    came from and what they may influence, while keeping palette, type scale,
    copy, and product IA under ontology authority.
    """

    visual_reference = visual_reference or {}
    visual_config = brand_profile.get("visual_reference") if isinstance(brand_profile.get("visual_reference"), dict) else {}
    providers = _build_provider_plan(visual_config, visual_reference)
    context_cards = _build_context_cards(visual_reference, query_report, providers)
    flow_index = _build_flow_index(context_cards, brand_profile)
    morphology_index = _build_morphology_index(context_cards)
    research_gaps = _build_research_gaps(
        brand_profile=brand_profile,
        providers=providers,
        context_cards=context_cards,
        flow_index=flow_index,
    )

    observed_cards = [card for card in context_cards if card.get("provenance_level") == "observed"]
    active_corpus = [
        provider for provider in providers
        if provider.get("status") in {"active", "connected"}
        and provider.get("kind") in {"lazyweb", "local-images", "uploaded-screenshots"}
    ]

    return {
        "schema_version": DESIGN_CONTEXT_SCHEMA_VERSION,
        "activation_state": (
            "grounded" if observed_cards else "research-needed" if active_corpus else "planned"
        ),
        "purpose": "Unify local screenshots, curated exports, corpus providers, and search assists into ontology-safe design research context.",
        "artifact_outputs": [
            "build/visuals/design_context_pack.json",
            "build/system/blueprint/design_context_pack.json",
        ],
        "providers": providers,
        "context_cards": context_cards[:48],
        "flow_index": flow_index,
        "component_morphology_index": morphology_index,
        "absorption_policy": REFERENCE_ABSORPTION_POLICY,
        "research_gaps": research_gaps,
    }


def _build_provider_plan(visual_config: dict[str, Any], visual_reference: dict[str, Any]) -> list[dict[str, Any]]:
    configured = _configured_providers(visual_config)
    providers: dict[str, dict[str, Any]] = {}
    source_provider_ids = set()
    source_provider_ids.update(_provider_ids_from_sources(visual_config.get("sources", [])))
    source_provider_ids.update(_provider_ids_from_sources(visual_reference.get("sources", [])))

    coverage = visual_reference.get("coverage") if isinstance(visual_reference.get("coverage"), dict) else {}
    if coverage.get("image_count") or "local-images" in source_provider_ids:
        providers["local-images"] = _provider_entry("local-images", status="active")

    pinterest = visual_config.get("pinterest_assist") if isinstance(visual_config.get("pinterest_assist"), dict) else {}
    mode = str(visual_config.get("mode", visual_reference.get("mode", ""))).strip().lower()
    if pinterest or mode == "pinterest-assisted":
        status = "active" if pinterest.get("enabled") or mode == "pinterest-assisted" else "preview"
        providers["pinterest"] = _provider_entry(
            "pinterest",
            status=status,
            config={
                "capture_mode": pinterest.get("capture_mode", "manual-save"),
                "capture_dir": pinterest.get("capture_dir", "references/visual/pinterest-assisted"),
            },
        )

    for item in configured:
        provider_id = item["provider_id"]
        if item.get("status"):
            status = str(item.get("status"))
        elif provider_id in {"lazyweb", "figma"}:
            status = str((PROVIDER_REGISTRY.get(provider_id) or {}).get("default_status", "suggested"))
        else:
            status = "active" if item.get("enabled") else "suggested"
        providers[provider_id] = _provider_entry(
            provider_id,
            status=status,
            config=item,
        )

    for provider_id in sorted(source_provider_ids):
        if provider_id == "local-images" or provider_id in providers:
            continue
        providers[provider_id] = _provider_entry(
            provider_id,
            status="active",
            config={
                "provider_id": provider_id,
                "status": "active",
                "source": "visual_reference.sources",
            },
        )

    if "lazyweb" not in providers:
        providers["lazyweb"] = _provider_entry(
            "lazyweb",
            status="suggested",
            config={
                "activation_hint": "Connect Lazyweb MCP or export selected screens into visual_reference.sources.",
                "recommended_for": ["real app screens", "flow search", "competitive morphology"],
            },
        )

    return sorted(
        providers.values(),
        key=lambda item: (
            {"active": 0, "connected": 0, "preview": 1, "suggested": 2, "blocked": 3}.get(item["status"], 4),
            item["provider_id"],
        ),
    )


def _provider_ids_from_sources(raw_sources: object) -> set[str]:
    if not isinstance(raw_sources, list):
        return set()

    provider_ids: set[str] = set()
    for source in raw_sources:
        if isinstance(source, str):
            if source.strip():
                provider_ids.add("local-images")
            continue
        if not isinstance(source, dict):
            continue

        provider_id = str(
            source.get("provider_id")
            or source.get("provider")
            or source.get("source_provider")
            or source.get("kind")
            or ""
        ).strip().lower()
        if provider_id in {"", "image", "directory", "screenshot", "url", "web"}:
            if source.get("path") or source.get("resolved_path"):
                provider_ids.add("local-images")
            continue
        provider_ids.add(provider_id)
    return provider_ids


def _configured_providers(visual_config: dict[str, Any]) -> list[dict[str, Any]]:
    raw = (
        visual_config.get("reference_providers")
        or visual_config.get("design_context_providers")
        or visual_config.get("providers")
        or []
    )
    if isinstance(raw, dict):
        raw = [{"provider_id": key, **value} if isinstance(value, dict) else {"provider_id": key} for key, value in raw.items()]
    if not isinstance(raw, list):
        return []

    providers = []
    for item in raw:
        if isinstance(item, str):
            provider_id = item.strip().lower()
            raw_item = {"provider_id": provider_id, "enabled": True}
        elif isinstance(item, dict):
            provider_id = str(item.get("provider_id") or item.get("id") or item.get("kind") or "").strip().lower()
            raw_item = dict(item)
            raw_item["provider_id"] = provider_id
        else:
            continue
        if not provider_id:
            continue
        raw_item["provider_id"] = provider_id
        raw_item["kind"] = str(raw_item.get("kind") or provider_id).strip().lower()
        raw_item["enabled"] = bool(raw_item.get("enabled", True))
        providers.append(raw_item)
    return providers


def _provider_entry(provider_id: str, *, status: str, config: dict[str, Any] | None = None) -> dict[str, Any]:
    registry = PROVIDER_REGISTRY.get(provider_id) or {
        "label": provider_id,
        "kind": provider_id,
        "access_mode": "custom",
        "truth_role": "custom reference provider",
    }
    config = config or {}
    return {
        "provider_id": provider_id,
        "kind": str(config.get("kind") or registry.get("kind") or provider_id),
        "label": str(config.get("label") or registry.get("label") or provider_id),
        "status": _pick_status(str(config.get("status") or status or registry.get("default_status") or "suggested")),
        "access_mode": str(config.get("access_mode") or registry.get("access_mode") or "custom"),
        "truth_role": str(config.get("truth_role") or registry.get("truth_role") or "reference context"),
        "allowed_outputs": list(REFERENCE_ABSORPTION_POLICY["allowed"]),
        "denied_outputs": list(REFERENCE_ABSORPTION_POLICY["denied"]),
        "config": _public_config(config),
    }


def _pick_status(value: str) -> str:
    normalized = value.strip().lower()
    if normalized in {"active", "connected", "preview", "suggested", "blocked", "disabled"}:
        return normalized
    return "suggested"


def _public_config(config: dict[str, Any]) -> dict[str, Any]:
    hidden = {"token", "api_key", "secret", "password"}
    return {
        str(key): value
        for key, value in config.items()
        if str(key).lower() not in hidden
        and value not in (None, "", [], {})
    }


def _build_context_cards(
    visual_reference: dict[str, Any],
    query_report: dict[str, Any] | None,
    providers: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    cards: list[dict[str, Any]] = []
    provider_ids = {provider["provider_id"] for provider in providers}
    selected_images = visual_reference.get("selected_images") if isinstance(visual_reference.get("selected_images"), list) else []

    for index, image in enumerate(selected_images, start=1):
        if not isinstance(image, dict):
            continue
        terms = _normalize_terms(image.get("signal_terms", []))
        terms.extend(_normalize_terms(image.get("tags", [])))
        label = str(image.get("label") or image.get("file_name") or f"reference image {index}").strip()
        inferred_provider = _provider_for_image(image, provider_ids)
        cards.append(
            {
                "context_id": str(image.get("image_id") or f"visual-image-{index:02d}"),
                "kind": "visual-screen",
                "label": label,
                "provider_id": inferred_provider,
                "status": "selected",
                "provenance_level": "observed",
                "source_path": image.get("relative_path") or image.get("path"),
                "source_url": None,
                "flows": _infer_flows(terms),
                "morphology": _infer_morphology(terms),
                "absorbed_traits": _absorbed_traits_from_image(image, terms),
                "must_not_absorb": list(REFERENCE_ABSORPTION_POLICY["denied"]),
            }
        )

    for index, source in enumerate(_source_entries_for_context(visual_reference), start=1):
        provider_id = _provider_for_source(source, provider_ids)
        source_url = _safe_source_url(
            source.get("source_url")
            or source.get("page_url")
            or source.get("pageUrl")
            or source.get("url")
            or source.get("image_url")
            or source.get("imageUrl")
        )
        source_path = source.get("resolved_path") or source.get("path") or source.get("original_path")
        if provider_id == "local-images" and not source_url:
            continue

        source_terms = [
            source.get("label", ""),
            source.get("companyName", ""),
            source.get("company_name", ""),
            source.get("category", ""),
            source.get("visionDescription", ""),
            source.get("vision_description", ""),
            source.get("query", ""),
        ]
        tags = source.get("tags", [])
        source_terms.extend(tags if isinstance(tags, list) else [tags])
        terms = _normalize_terms(source_terms)
        cards.append(
            {
                "context_id": str(source.get("context_id") or source.get("source_id") or f"external-reference-{index:02d}"),
                "kind": "external-reference",
                "label": str(
                    source.get("label")
                    or source.get("companyName")
                    or source.get("company_name")
                    or f"External reference {index}"
                ),
                "provider_id": provider_id,
                "status": _source_card_status(source),
                "provenance_level": "observed" if source_url or source_path else "planned",
                "source_path": source_path,
                "source_url": source_url,
                "flows": _infer_flows(terms),
                "morphology": _infer_morphology(terms),
                "absorbed_traits": _absorbed_traits_from_source(source, terms),
                "must_not_absorb": list(REFERENCE_ABSORPTION_POLICY["denied"]),
            }
        )

    query_entries = _query_entries(visual_reference, query_report)
    for index, query in enumerate(query_entries, start=1):
        terms = _normalize_terms([query.get("query", ""), query.get("primitive", ""), query.get("intent", "")])
        cards.append(
            {
                "context_id": f"research-query-{index:02d}",
                "kind": "research-query",
                "label": str(query.get("query") or f"Research query {index}"),
                "provider_id": "lazyweb" if "lazyweb" in provider_ids else "pinterest" if "pinterest" in provider_ids else "local-images",
                "status": "research-needed",
                "provenance_level": "planned",
                "source_path": None,
                "source_url": None,
                "flows": _infer_flows(terms),
                "morphology": _infer_morphology(terms),
                "absorbed_traits": [
                    "Use as search intent only until real screenshots are selected.",
                    f"intent={query.get('intent', 'general')}",
                    f"primitive={query.get('primitive', 'unknown')}",
                ],
                "must_not_absorb": list(REFERENCE_ABSORPTION_POLICY["denied"]),
            }
        )

    return cards


def _source_entries_for_context(visual_reference: dict[str, Any]) -> list[dict[str, Any]]:
    raw_sources = visual_reference.get("sources")
    if not isinstance(raw_sources, list):
        return []
    return [source for source in raw_sources if isinstance(source, dict)]


def _provider_for_source(source: dict[str, Any], provider_ids: set[str]) -> str:
    explicit = str(
        source.get("provider_id")
        or source.get("provider")
        or source.get("source_provider")
        or source.get("kind")
        or ""
    ).strip().lower()
    if explicit in provider_ids:
        return explicit
    if explicit in PROVIDER_REGISTRY:
        return explicit

    source_text = " ".join(
        str(source.get(key) or "")
        for key in ("label", "source_label", "url", "source_url", "pageUrl", "page_url")
    ).lower()
    if "pinterest" in source_text:
        return "pinterest" if "pinterest" in provider_ids else "local-images"
    if "lazyweb" in source_text:
        return "lazyweb" if "lazyweb" in provider_ids else "local-images"
    return "local-images" if "local-images" in provider_ids else next(iter(provider_ids), "local-images")


def _source_card_status(source: dict[str, Any]) -> str:
    raw_status = str(source.get("status") or "selected").strip().lower()
    if raw_status in {"resolved", "unsupported-url", "connected", "active", "selected"}:
        return "selected"
    if raw_status in {"not-found", "missing-path", "empty"}:
        return "blocked"
    return raw_status or "selected"


def _safe_source_url(value: Any) -> str | None:
    raw = str(value or "").strip()
    if not raw:
        return None
    base, _, _ = raw.partition("?")
    base, _, _ = base.partition("#")
    return base or None


def _provider_for_image(image: dict[str, Any], provider_ids: set[str]) -> str:
    path = str(image.get("relative_path") or image.get("path") or "").lower()
    source_label = str(image.get("source_label") or "").lower()
    if "pinterest" in path or "pinterest" in source_label:
        return "pinterest" if "pinterest" in provider_ids else "local-images"
    if "uploaded-screenshots" in provider_ids and ("upload" in path or "download" in path):
        return "uploaded-screenshots"
    return "local-images" if "local-images" in provider_ids else next(iter(provider_ids), "local-images")


def _absorbed_traits_from_image(image: dict[str, Any], terms: list[str]) -> list[str]:
    traits: list[str] = []
    for key in ("orientation", "aspect_ratio_bucket", "mime_type"):
        if image.get(key):
            traits.append(f"{key}={image[key]}")
    for flow in _infer_flows(terms)[:3]:
        traits.append(f"flow={flow}")
    for morphology in _infer_morphology(terms)[:3]:
        traits.append(f"morphology={morphology}")
    return traits[:8]


def _absorbed_traits_from_source(source: dict[str, Any], terms: list[str]) -> list[str]:
    traits: list[str] = []
    for key in ("kind", "status", "category", "companyName", "company_name"):
        if source.get(key):
            normalized_key = "company" if key in {"companyName", "company_name"} else key
            traits.append(f"{normalized_key}={source[key]}")
    website_inspection = source.get("website_inspection")
    if isinstance(website_inspection, dict):
        if website_inspection.get("section_count") is not None:
            traits.append(f"sections={website_inspection['section_count']}")
        for model in _normalize_terms(website_inspection.get("interaction_models", []))[:4]:
            traits.append(f"interaction={model}")
        asset_counts = website_inspection.get("asset_counts")
        if isinstance(asset_counts, dict):
            for key in ("images", "videos", "background_images", "inline_svgs"):
                if asset_counts.get(key):
                    traits.append(f"{key}={asset_counts[key]}")
    for tag in _normalize_terms(source.get("tags", []))[:4]:
        traits.append(f"tag={tag}")
    for flow in _infer_flows(terms)[:3]:
        traits.append(f"flow={flow}")
    for morphology in _infer_morphology(terms)[:3]:
        traits.append(f"morphology={morphology}")
    if source.get("visionDescription") or source.get("vision_description"):
        traits.append("vision-description=available")
    return traits[:10]


def _query_entries(visual_reference: dict[str, Any], query_report: dict[str, Any] | None) -> list[dict[str, Any]]:
    entries: list[dict[str, Any]] = []
    if isinstance(query_report, dict):
        for item in query_report.get("queries", []) or []:
            if isinstance(item, dict) and str(item.get("query", "")).strip():
                entries.append(item)
    if entries:
        return entries[:24]

    for item in visual_reference.get("query", []) or []:
        query = str(item).strip()
        if query:
            entries.append({"query": query, "intent": "general", "primitive": "unknown"})
    return entries[:24]


def _build_flow_index(context_cards: list[dict[str, Any]], brand_profile: dict[str, Any]) -> list[dict[str, Any]]:
    counter: Counter[str] = Counter()
    provider_map: dict[str, set[str]] = {}
    for card in context_cards:
        for flow in card.get("flows", []):
            counter[flow] += 1
            provider_map.setdefault(flow, set()).add(str(card.get("provider_id", "")))

    primitive_terms = _normalize_terms(brand_profile.get("product_primitives", []))
    for flow in _infer_flows(primitive_terms):
        counter.setdefault(flow, 0)
        provider_map.setdefault(flow, set())

    return [
        {
            "flow": flow,
            "context_count": counter[flow],
            "providers": sorted(provider for provider in provider_map.get(flow, set()) if provider),
            "status": "covered" if counter[flow] else "gap",
        }
        for flow in sorted(counter.keys(), key=lambda key: (-counter[key], key))
    ][:16]


def _build_morphology_index(context_cards: list[dict[str, Any]]) -> list[dict[str, Any]]:
    counter: Counter[str] = Counter()
    examples: dict[str, list[str]] = {}
    for card in context_cards:
        for item in card.get("morphology", []):
            counter[item] += 1
            examples.setdefault(item, []).append(str(card.get("context_id", "")))
    return [
        {
            "morphology": item,
            "context_count": count,
            "examples": [example for example in examples.get(item, []) if example][:4],
        }
        for item, count in counter.most_common(12)
    ]


def _build_research_gaps(
    *,
    brand_profile: dict[str, Any],
    providers: list[dict[str, Any]],
    context_cards: list[dict[str, Any]],
    flow_index: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    gaps: list[dict[str, Any]] = []
    observed_count = sum(1 for card in context_cards if card.get("provenance_level") == "observed")
    if observed_count == 0:
        gaps.append(
            {
                "id": "no-observed-screens",
                "severity": "high",
                "detail": "No selected local screenshots are available; visual signals are query/planning-only.",
                "recommended_action": "Capture or export 3-8 representative screens before treating morphology guidance as grounded.",
            }
        )

    lazyweb = next((provider for provider in providers if provider.get("provider_id") == "lazyweb"), None)
    if lazyweb and lazyweb.get("status") == "suggested":
        gaps.append(
            {
                "id": "real-app-corpus-provider-not-connected",
                "severity": "medium",
                "detail": "A real-app corpus provider is only suggested, not connected.",
                "recommended_action": "Connect Lazyweb MCP or export selected Lazyweb screens into visual_reference.sources with provenance.",
            }
        )

    uncovered = [item["flow"] for item in flow_index if item.get("status") == "gap"]
    if uncovered:
        gaps.append(
            {
                "id": "flow-coverage-gaps",
                "severity": "medium",
                "detail": "Some product flows are not covered by selected reference screens.",
                "flows": uncovered[:8],
                "recommended_action": "Search corpus/provider screens by these flows before mock generation.",
            }
        )

    if not brand_profile.get("product_primitives"):
        gaps.append(
            {
                "id": "missing-product-primitives",
                "severity": "low",
                "detail": "product_primitives is empty, so provider queries cannot be flow-specific.",
                "recommended_action": "Add product_primitives before running visual query or corpus collection.",
            }
        )

    return gaps


def _infer_flows(terms: list[str]) -> list[str]:
    term_set = set(terms)
    scored = []
    for flow, keywords in FLOW_KEYWORDS.items():
        score = len(term_set & keywords)
        if score:
            scored.append((score, flow))
    scored.sort(key=lambda item: (-item[0], item[1]))
    return [flow for _, flow in scored[:4]] or ["general-product-ui"]


def _infer_morphology(terms: list[str]) -> list[str]:
    term_set = set(terms)
    scored = []
    for morphology, keywords in MORPHOLOGY_KEYWORDS.items():
        score = len(term_set & keywords)
        if score:
            scored.append((score, morphology))
    scored.sort(key=lambda item: (-item[0], item[1]))
    return [morphology for _, morphology in scored[:4]] or ["general-interface-composition"]


def _normalize_terms(value: Any) -> list[str]:
    raw_items: list[str] = []
    if isinstance(value, str):
        raw_items = [value]
    elif isinstance(value, list):
        raw_items = [str(item) for item in value if str(item).strip()]
    elif value is not None:
        raw_items = [str(value)]

    terms: list[str] = []
    for item in raw_items:
        normalized = "".join(ch.lower() if ch.isalnum() else " " for ch in item)
        terms.extend(part for part in normalized.split() if part)
    return terms
