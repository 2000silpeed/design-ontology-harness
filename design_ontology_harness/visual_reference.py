from __future__ import annotations

import colorsys
import hashlib
import re
import struct
from collections import Counter, defaultdict
from pathlib import Path
from typing import Iterable
from xml.etree import ElementTree

try:
    from PIL import Image
except ImportError:  # pragma: no cover - optional dependency
    Image = None


DEFAULT_VISUAL_REFERENCE = {
    "mode": "local-images",
    "query": [],
    "preferred_count": 12,
    "weights": {
        "layout": 0.3,
        "component_shape": 0.25,
        "color_balance": 0.2,
        "typography_mood": 0.15,
        "surface_style": 0.1,
    },
    "extraction_policy": "advisory-only",
    "notes": [],
    "must_include": [],
    "avoid_patterns": [],
}

IMAGE_EXTENSIONS = {
    ".png",
    ".jpg",
    ".jpeg",
    ".webp",
    ".svg",
    ".gif",
    ".bmp",
}

MIME_BY_EXTENSION = {
    ".png": "image/png",
    ".jpg": "image/jpeg",
    ".jpeg": "image/jpeg",
    ".webp": "image/webp",
    ".svg": "image/svg+xml",
    ".gif": "image/gif",
    ".bmp": "image/bmp",
}

RASTER_MIME_SIGNATURES = (
    (b"\x89PNG\r\n\x1a\n", "image/png"),
    (b"\xff\xd8\xff", "image/jpeg"),
    (b"GIF87a", "image/gif"),
    (b"GIF89a", "image/gif"),
    (b"BM", "image/bmp"),
)

WEIGHT_KEYS = (
    "layout",
    "component_shape",
    "color_balance",
    "typography_mood",
    "surface_style",
)

COLOR_HEX_RE = re.compile(r"#(?:[0-9A-Fa-f]{6}|[0-9A-Fa-f]{3})")
TEXT_TOKEN_RE = re.compile(r"[A-Za-z0-9]+|[가-힣]+")

LAYOUT_CUE_DEFINITIONS = [
    {
        "id": "split-pane-workspace",
        "label": "Split-pane workspace",
        "keywords": {
            "workspace": 3,
            "sidebar": 3,
            "app": 1,
            "shell": 3,
            "editor": 2,
            "navigation": 1,
            "command": 1,
            "topbar": 1,
            "breadcrumb": 1,
        },
        "aspect_buckets": {"16:9-ish": 1, "3:2-ish": 1},
    },
    {
        "id": "dashboard-grid",
        "label": "Dashboard grid",
        "keywords": {
            "dashboard": 3,
            "analytics": 3,
            "metric": 2,
            "kpi": 2,
            "chart": 2,
            "stat": 2,
            "table": 2,
            "monitoring": 2,
            "ops": 2,
        },
        "aspect_buckets": {"3:2-ish": 1, "4:3-ish": 1, "1:1": 1},
    },
    {
        "id": "editorial-feed",
        "label": "Editorial feed",
        "keywords": {
            "editorial": 3,
            "article": 2,
            "content": 2,
            "feed": 2,
            "story": 2,
            "magazine": 2,
            "review": 2,
            "critique": 1,
            "spotlight": 1,
            "poster": 1,
            "publish": 1,
            "journal": 1,
        },
        "aspect_buckets": {"4:5-ish": 1, "2:3-ish": 1},
    },
    {
        "id": "landing-narrative",
        "label": "Narrative landing flow",
        "keywords": {
            "landing": 3,
            "hero": 3,
            "pricing": 2,
            "testimonial": 2,
            "cta": 2,
            "faq": 1,
            "marketing": 2,
            "brand": 1,
            "spotlight": 2,
            "feature": 1,
            "launch": 1,
            "poster": 1,
        },
        "aspect_buckets": {"16:9-ish": 1, "3:2-ish": 1},
    },
    {
        "id": "data-review-surface",
        "label": "Data review surface",
        "keywords": {
            "table": 3,
            "grid": 2,
            "records": 2,
            "audit": 2,
            "log": 2,
            "data": 2,
            "filter": 1,
            "timeline": 1,
            "comparison": 3,
            "ranking": 2,
            "review": 2,
            "score": 2,
            "verdict": 2,
        },
        "aspect_buckets": {"3:2-ish": 1, "4:3-ish": 1},
    },
    {
        "id": "conversation-panel",
        "label": "Conversation side panel",
        "keywords": {
            "chat": 3,
            "assistant": 3,
            "message": 2,
            "thread": 2,
            "prompt": 1,
            "conversation": 2,
            "inbox": 1,
        },
        "aspect_buckets": {"4:5-ish": 1, "2:3-ish": 1},
    },
]

SURFACE_STYLE_DEFINITIONS = {
    "outlined": {"border": 3, "outlined": 3, "outline": 3, "frame": 2, "stroke": 2},
    "elevated": {"shadow": 3, "raised": 2, "elevated": 3, "floating": 2, "overlay": 2, "modal": 1},
    "tinted": {"warm": 1, "editorial": 1, "paper": 2, "tinted": 3, "cream": 2, "soft": 1},
    "flat": {"flat": 3, "minimal": 2, "clean": 2, "utilitarian": 2},
    "glassy": {"glass": 3, "glassy": 3, "blur": 2, "translucent": 2},
}

TYPOGRAPHY_MOOD_DEFINITIONS = {
    "editorial": {"editorial": 3, "article": 2, "magazine": 2, "content": 2, "serif": 2, "story": 1},
    "utilitarian": {"dashboard": 3, "admin": 2, "enterprise": 2, "ops": 2, "control": 2, "table": 1},
    "premium": {"premium": 3, "luxury": 3, "finance": 2, "elegant": 2, "brand": 1},
    "playful": {"playful": 3, "fun": 2, "bright": 2, "kids": 2, "friendly": 1},
}

CORNER_STYLE_DEFINITIONS = {
    "pill": {"pill": 4, "capsule": 3},
    "round": {"rounded": 3, "soft": 2, "curved": 2},
    "medium": {"radius": 2, "card": 1},
    "sharp": {"sharp": 3, "angular": 2, "square": 2},
}

DENSITY_DEFINITIONS = {
    "airy": {"editorial": 2, "landing": 2, "hero": 2, "whitespace": 3, "spacious": 3, "calm": 1},
    "balanced": {"balanced": 3, "workspace": 1, "product": 1},
    "dense": {"dashboard": 3, "table": 3, "analytics": 2, "monitoring": 2, "ops": 2, "control": 2},
}

COMPONENT_ARCHETYPE_DEFINITIONS = [
    {
        "id": "workspace-shell",
        "label": "Workspace shell",
        "family": "navigation",
        "suggested_components": [
            "app-shell",
            "sidebar-nav",
            "workspace-switcher",
            "breadcrumb",
            "context-panel",
        ],
        "layout_matches": ["split-pane-workspace"],
        "keywords": {"workspace": 3, "sidebar": 3, "navigation": 2, "panel": 2, "shell": 2},
        "primitive_matches": ["workspace navigation"],
    },
    {
        "id": "dashboard-insight-module",
        "label": "Dashboard insight module",
        "family": "data-display",
        "suggested_components": [
            "metric-strip",
            "status-summary-row",
            "chart-panel",
            "section-header",
            "filter-chip",
        ],
        "layout_matches": ["dashboard-grid"],
        "keywords": {"dashboard": 3, "analytics": 2, "metric": 2, "kpi": 2, "chart": 2, "insight": 2},
        "primitive_matches": ["operational overview", "dashboard cards", "charts and visualization"],
    },
    {
        "id": "data-review-table",
        "label": "Data review table",
        "family": "data-display",
        "suggested_components": [
            "data-table",
            "column-header",
            "row-actions",
            "filter-toolbar",
            "pagination",
        ],
        "layout_matches": ["data-review-surface", "dashboard-grid"],
        "keywords": {"table": 3, "data": 2, "grid": 2, "audit": 2, "log": 2, "records": 2, "filter": 1},
        "primitive_matches": ["data tables", "search and filter"],
    },
    {
        "id": "editorial-content-block",
        "label": "Editorial content block",
        "family": "editorial",
        "suggested_components": [
            "content-card",
            "featured-story-card",
            "section-header",
            "content-meta",
            "byline-row",
        ],
        "layout_matches": ["editorial-feed"],
        "keywords": {"editorial": 3, "article": 2, "content": 2, "story": 2, "magazine": 2},
        "primitive_matches": ["rich text editor"],
    },
    {
        "id": "review-coverage-system",
        "label": "Review coverage system",
        "family": "editorial",
        "suggested_components": [
            "review-card",
            "score-badge",
            "comparison-table",
            "ranking-list",
            "filter-chip",
        ],
        "layout_matches": ["data-review-surface", "editorial-feed", "landing-narrative"],
        "keywords": {
            "review": 3,
            "score": 3,
            "comparison": 3,
            "ranking": 2,
            "verdict": 2,
            "poster": 1,
        },
        "primitive_matches": ["comparison and ranking", "search and filter", "tags and labels"],
    },
    {
        "id": "conversation-sidecar",
        "label": "Conversation sidecar",
        "family": "overlay",
        "suggested_components": [
            "chat-panel",
            "message-thread",
            "message-composer",
            "context-drawer",
        ],
        "layout_matches": ["conversation-panel", "split-pane-workspace"],
        "keywords": {"chat": 3, "assistant": 3, "message": 2, "conversation": 2, "panel": 1},
        "primitive_matches": ["chat and messaging"],
    },
    {
        "id": "marketing-hero-stack",
        "label": "Marketing hero stack",
        "family": "marketing",
        "suggested_components": [
            "hero-section",
            "hero-headline",
            "hero-visual",
            "cta-button-group",
            "trust-strip",
        ],
        "layout_matches": ["landing-narrative"],
        "keywords": {"hero": 3, "landing": 3, "pricing": 2, "testimonial": 2, "cta": 2, "marketing": 2},
        "primitive_matches": ["hero section", "pricing and plans", "social proof"],
    },
]


def resolve_visual_reference(
    reference_config: dict,
    base_dir: Path,
    brand_profile: dict | None = None,
) -> tuple[dict | None, list[str]]:
    if not isinstance(reference_config, dict):
        return None, []

    issues: list[str] = []
    config = _normalize_visual_reference_config(reference_config)
    source_entries = _normalize_source_entries(reference_config.get("sources", []))

    if not source_entries:
        issues.append("visual_reference.sources is empty")

    source_records: list[dict] = []
    image_records: list[dict] = []

    for index, source in enumerate(source_entries, start=1):
        source_record, images = _resolve_source_entry(
            index=index,
            source=source,
            base_dir=base_dir,
            issues=issues,
        )
        source_records.append(source_record)
        image_records.extend(images)

    image_records.sort(key=lambda item: (item["source_id"], item["file_name"].lower()))
    duplicate_groups = _detect_duplicate_groups(image_records)
    similar_groups = _detect_similar_groups(image_records)

    selected_images = image_records[: config["preferred_count"]]
    coverage = _build_coverage_summary(source_records, image_records, selected_images)
    visual_motifs = _build_visual_motifs(
        selected_images=selected_images,
        image_records=image_records,
        config=config,
        brand_profile=brand_profile or {},
    )
    layout_cues = _build_layout_cues(
        selected_images=selected_images,
        image_records=image_records,
        config=config,
        brand_profile=brand_profile or {},
    )
    component_style_hints = _build_component_style_hints(
        visual_motifs=visual_motifs,
        layout_cues=layout_cues,
        brand_profile=brand_profile or {},
        image_records=image_records,
    )
    candidate_component_archetypes = _build_candidate_component_archetypes(
        selected_images=selected_images,
        image_records=image_records,
        layout_cues=layout_cues,
        visual_motifs=visual_motifs,
        config=config,
        brand_profile=brand_profile or {},
    )
    reference_mood_summary = _build_reference_mood_summary(
        visual_motifs=visual_motifs,
        layout_cues=layout_cues,
        component_style_hints=component_style_hints,
        config=config,
        brand_profile=brand_profile or {},
    )

    summary = {
        "mode": config["mode"],
        "query": config["query"],
        "preferred_count": config["preferred_count"],
        "weights": config["weights"],
        "extraction_policy": config["extraction_policy"],
        "notes": config["notes"],
        "must_include": config["must_include"],
        "avoid_patterns": config["avoid_patterns"],
        "sources": source_records,
        "images": image_records,
        "selected_images": selected_images,
        "duplicate_groups": duplicate_groups,
        "similar_groups": similar_groups,
        "coverage": coverage,
        "visual_motifs": visual_motifs,
        "layout_cues": layout_cues,
        "component_style_hints": component_style_hints,
        "candidate_component_archetypes": candidate_component_archetypes,
        "reference_mood_summary": reference_mood_summary,
        "brand_context": _build_brand_context(brand_profile or {}),
    }
    return summary, issues


def _normalize_visual_reference_config(raw_config: dict) -> dict:
    config = dict(DEFAULT_VISUAL_REFERENCE)
    config.update(
        {
            key: raw_config.get(key, config[key])
            for key in DEFAULT_VISUAL_REFERENCE
        }
    )

    config["mode"] = _pick_enum(config["mode"], {"local-images", "pinterest-assisted"}, "local-images")
    config["query"] = _normalize_text_list(config.get("query", []))
    config["preferred_count"] = max(1, min(48, int(config.get("preferred_count", 12) or 12)))
    config["weights"] = _normalize_weight_map(config.get("weights", {}))
    config["extraction_policy"] = _pick_enum(
        config["extraction_policy"],
        {"advisory-only", "allow-token-suggestions"},
        "advisory-only",
    )
    config["notes"] = _normalize_text_list(config.get("notes", []))
    config["must_include"] = _normalize_text_list(config.get("must_include", []))
    config["avoid_patterns"] = _normalize_text_list(config.get("avoid_patterns", []))
    return config


def _normalize_source_entries(raw_sources: object) -> list[dict]:
    if not isinstance(raw_sources, list):
        return []

    entries: list[dict] = []
    for source in raw_sources:
        if isinstance(source, str):
            path = source.strip()
            if path:
                entries.append({"kind": "image", "path": path})
            continue

        if not isinstance(source, dict):
            continue

        kind = str(source.get("kind", "image")).strip() or "image"
        path = str(source.get("path", "")).strip()
        url = str(source.get("url", "")).strip()
        label = str(source.get("label", "")).strip()
        tags = _normalize_text_list(source.get("tags", []))
        if path or url:
            entries.append(
                {
                    "kind": kind,
                    "path": path,
                    "url": url,
                    "label": label,
                    "tags": tags,
                }
            )
    return entries


def _resolve_source_entry(
    index: int,
    source: dict,
    base_dir: Path,
    issues: list[str],
) -> tuple[dict, list[dict]]:
    source_id = f"source-{index:02d}"
    label = source.get("label") or source.get("path") or source.get("url") or source_id
    url = str(source.get("url", "")).strip()
    raw_path = str(source.get("path", "")).strip()
    tags = list(source.get("tags", []))

    if url:
        issues.append(
            f"visual_reference URL source is not fetched automatically yet: {url} "
            f"(download locally and pass it via sources[].path)"
        )
        return (
            {
                "source_id": source_id,
                "kind": source.get("kind", "image"),
                "label": label,
                "status": "unsupported-url",
                "original_path": raw_path or None,
                "resolved_path": None,
                "url": url,
                "tags": tags,
                "image_count": 0,
            },
            [],
        )

    if not raw_path:
        issues.append(f"visual_reference source missing path: {source_id}")
        return (
            {
                "source_id": source_id,
                "kind": source.get("kind", "image"),
                "label": label,
                "status": "missing-path",
                "original_path": None,
                "resolved_path": None,
                "url": None,
                "tags": tags,
                "image_count": 0,
            },
            [],
        )

    resolved_path = Path(raw_path)
    if not resolved_path.is_absolute():
        resolved_path = (base_dir / resolved_path).resolve()

    if not resolved_path.exists():
        issues.append(f"visual_reference.path not found: {resolved_path}")
        return (
            {
                "source_id": source_id,
                "kind": source.get("kind", "image"),
                "label": label,
                "status": "not-found",
                "original_path": raw_path,
                "resolved_path": str(resolved_path),
                "url": None,
                "tags": tags,
                "image_count": 0,
            },
            [],
        )

    image_paths = list(_discover_image_paths(resolved_path))
    if not image_paths:
        issues.append(f"visual_reference.path has no supported images: {resolved_path}")

    images = [
        _build_image_record(
            source_id=source_id,
            index=image_index,
            path=image_path,
            base_dir=base_dir,
            label=label,
            tags=tags,
        )
        for image_index, image_path in enumerate(image_paths, start=1)
    ]

    source_record = {
        "source_id": source_id,
        "kind": "directory" if resolved_path.is_dir() else source.get("kind", "image"),
        "label": label,
        "status": "resolved" if image_paths else "empty",
        "original_path": raw_path,
        "resolved_path": str(resolved_path),
        "url": None,
        "tags": tags,
        "image_count": len(images),
    }
    return source_record, images


def _discover_image_paths(path: Path) -> Iterable[Path]:
    if path.is_file():
        if path.suffix.lower() in IMAGE_EXTENSIONS:
            yield path
        return

    if not path.is_dir():
        return

    for candidate in sorted(path.rglob("*")):
        if candidate.is_file() and candidate.suffix.lower() in IMAGE_EXTENSIONS:
            yield candidate


def _build_image_record(
    source_id: str,
    index: int,
    path: Path,
    base_dir: Path,
    label: str,
    tags: list[str],
) -> dict:
    metadata = _read_image_metadata(path)
    width = metadata.get("width")
    height = metadata.get("height")
    orientation = _classify_orientation(width, height)
    aspect_ratio = round(width / height, 4) if width and height else None
    sha256 = _sha256(path)
    signal_terms = _extract_signal_terms(path, label, tags)
    observed_colors = _extract_observed_colors(path)
    svg_features = _extract_svg_features(path)

    return {
        "image_id": f"{source_id}-image-{index:02d}",
        "source_id": source_id,
        "source_label": label,
        "label": path.stem,
        "tags": tags,
        "path": str(path),
        "relative_path": _relative_display_path(path, base_dir),
        "file_name": path.name,
        "extension": path.suffix.lower(),
        "mime_type": metadata.get("mime_type"),
        "file_size_bytes": path.stat().st_size,
        "width": width,
        "height": height,
        "aspect_ratio": aspect_ratio,
        "aspect_ratio_bucket": _bucket_aspect_ratio(width, height),
        "orientation": orientation,
        "signal_terms": signal_terms,
        "observed_colors": observed_colors,
        "svg_features": svg_features,
        "sha256": sha256,
    }


def _build_coverage_summary(
    source_records: list[dict],
    image_records: list[dict],
    selected_images: list[dict],
) -> dict:
    format_counts = Counter(record["extension"] for record in image_records)
    orientation_counts = Counter(record["orientation"] for record in image_records)
    aspect_ratio_counts = Counter(record["aspect_ratio_bucket"] for record in image_records)

    return {
        "source_count": len(source_records),
        "resolved_source_count": sum(1 for record in source_records if record["status"] == "resolved"),
        "image_count": len(image_records),
        "selected_image_count": len(selected_images),
        "format_counts": dict(sorted(format_counts.items())),
        "orientation_counts": dict(sorted(orientation_counts.items())),
        "aspect_ratio_buckets": dict(sorted(aspect_ratio_counts.items())),
    }


def _build_visual_motifs(
    selected_images: list[dict],
    image_records: list[dict],
    config: dict,
    brand_profile: dict,
) -> dict:
    query_only = not image_records
    term_counts = _collect_term_counts(selected_images, config, brand_profile)
    selected_aspect_counts = Counter(item.get("aspect_ratio_bucket", "unknown") for item in selected_images)
    selected_orientation_counts = Counter(item.get("orientation", "unknown") for item in selected_images)
    color_balance = _summarize_color_balance(selected_images)

    density = _score_named_choice(
        definitions=DENSITY_DEFINITIONS,
        term_counts=term_counts,
        fallback="balanced",
        weight=config["weights"]["layout"],
        aspect_counts=selected_aspect_counts,
        orientation_counts=selected_orientation_counts,
    )
    surface_style = _score_named_choice(
        definitions=SURFACE_STYLE_DEFINITIONS,
        term_counts=term_counts,
        fallback="tinted" if color_balance.get("temperature") == "warm" else "flat",
        weight=config["weights"]["surface_style"],
    )
    typography_mood = _score_named_choice(
        definitions=TYPOGRAPHY_MOOD_DEFINITIONS,
        term_counts=term_counts,
        fallback="editorial" if "editorial" in term_counts else "utilitarian",
        weight=config["weights"]["typography_mood"],
    )
    corner_style = _score_corner_style(
        selected_images=selected_images,
        term_counts=term_counts,
        weight=config["weights"]["component_shape"],
    )

    color_provenance = "observed" if color_balance.get("observed") else "unverified"

    return {
        "density": _with_provenance(
            _adjust_inferred_choice(density, query_only=query_only, ceiling=0.52),
            level="inferred",
            detail=(
                "Derived from query and brand context only because no local image selection was available."
                if query_only
                else "Derived from selected image signals plus query and brand context."
            ),
        ),
        "surface_style": _with_provenance(
            _adjust_inferred_choice(surface_style, query_only=query_only, ceiling=0.5),
            level="inferred",
            detail=(
                "Derived from query and brand context only because no local image selection was available."
                if query_only
                else "Derived from selected image signals plus query and brand context."
            ),
        ),
        "typography_mood": _with_provenance(
            _adjust_inferred_choice(typography_mood, query_only=query_only, ceiling=0.5),
            level="inferred",
            detail=(
                "Derived from query and brand context only because no local image selection was available."
                if query_only
                else "Derived from selected image signals plus query and brand context."
            ),
        ),
        "corner_style": _with_provenance(
            _adjust_inferred_choice(corner_style, query_only=query_only, ceiling=0.48),
            level="inferred",
            detail=(
                "Derived from query and brand context only because no local image geometry was available."
                if query_only
                else "Derived from selected image geometry and supporting signal terms."
            ),
        ),
        "color_balance": _with_provenance(
            color_balance,
            level=color_provenance,
            detail=(
                "Observed directly from sampled image colors."
                if color_provenance == "observed"
                else "No reliable pixel-color sample was available from the current selection."
            ),
        ),
        "image_selection": {
            "selected_image_count": len(selected_images),
            "available_image_count": len(image_records),
            "provenance": {
                "level": "observed" if image_records else "unverified",
                "detail": (
                    "Selection is grounded in resolved local image files."
                    if image_records
                    else "No local image files were available for selection."
                ),
            },
        },
    }


def _build_layout_cues(
    selected_images: list[dict],
    image_records: list[dict],
    config: dict,
    brand_profile: dict,
) -> list[dict]:
    query_only = not image_records
    term_counts = _collect_term_counts(selected_images, config, brand_profile)
    aspect_counts = Counter(item.get("aspect_ratio_bucket", "unknown") for item in selected_images)
    orientation_counts = Counter(item.get("orientation", "unknown") for item in selected_images)

    cues: list[dict] = []
    for definition in LAYOUT_CUE_DEFINITIONS:
        score = 0.0
        evidence: list[str] = []
        for keyword, weight in definition.get("keywords", {}).items():
            hits = term_counts.get(keyword, 0)
            if hits:
                score += hits * weight
                evidence.append(f"{keyword} x{hits}")
        for bucket, weight in definition.get("aspect_buckets", {}).items():
            hits = aspect_counts.get(bucket, 0)
            if hits:
                score += hits * weight
                evidence.append(f"{bucket} x{hits}")
        if definition["id"] == "dashboard-grid" and orientation_counts.get("landscape"):
            score += 1
        if definition["id"] == "editorial-feed" and orientation_counts.get("portrait"):
            score += 1
        if definition["id"] == "landing-narrative" and orientation_counts.get("landscape"):
            score += 1
        if score <= 0 or (query_only and score < 2.0):
            continue
        cues.append(
            _with_provenance(
                {
                "id": definition["id"],
                "label": definition["label"],
                "confidence": _query_only_confidence(
                    _confidence_from_score(score, config["weights"]["layout"]),
                    query_only=query_only,
                    ceiling=0.56,
                ),
                "evidence": evidence[:6],
                },
                level="inferred",
                detail=(
                    "Layout cue inferred from query and brand context only; local image grounding was unavailable."
                    if query_only
                    else "Layout cue inferred from selected image signals and reference context."
                ),
            )
        )

    cues.sort(key=lambda item: (-item["confidence"], item["label"]))
    return cues[:4]


def _build_component_style_hints(
    visual_motifs: dict,
    layout_cues: list[dict],
    brand_profile: dict,
    image_records: list[dict],
) -> dict:
    query_only = not image_records
    density = (visual_motifs.get("density") or {}).get("value", "balanced")
    surface_style = (visual_motifs.get("surface_style") or {}).get("value", "flat")
    corner_style = (visual_motifs.get("corner_style") or {}).get("value", "medium")
    typography_mood = (visual_motifs.get("typography_mood") or {}).get("value", "utilitarian")
    top_layout = layout_cues[0]["id"] if layout_cues else None
    cue_by_id = {cue["id"]: cue for cue in layout_cues}
    navigation_layout = "split-pane-workspace" if "split-pane-workspace" in cue_by_id else top_layout
    data_layout = (
        "dashboard-grid"
        if "dashboard-grid" in cue_by_id
        else "data-review-surface"
        if "data-review-surface" in cue_by_id
        else top_layout
    )
    primitives = {item.lower() for item in brand_profile.get("product_primitives", [])}

    hints = {
        "cards": {
            "direction": _describe_card_direction(surface_style, density, corner_style),
            "confidence": round(max(
                (visual_motifs.get("surface_style") or {}).get("confidence", 0.0),
                (visual_motifs.get("density") or {}).get("confidence", 0.0),
            ), 2),
            "evidence": [
                f"surface={surface_style}",
                f"density={density}",
                f"corner={corner_style}",
            ],
        },
        "navigation": {
            "direction": _describe_navigation_direction(navigation_layout, density),
            "confidence": round(max(
                0.24 if query_only else 0.45,
                cue_by_id.get(navigation_layout, {}).get("confidence", 0.0),
            ), 2),
            "evidence": [cue_by_id[navigation_layout]["label"]] if navigation_layout in cue_by_id else [cue["label"] for cue in layout_cues[:2]] or ["No strong layout cue"],
        },
        "typography": {
            "direction": _describe_typography_direction(typography_mood, density),
            "confidence": round((visual_motifs.get("typography_mood") or {}).get("confidence", 0.45), 2),
            "evidence": [f"typography_mood={typography_mood}"],
        },
    }

    if primitives & {"operational overview", "dashboard cards"} or data_layout in {"dashboard-grid", "data-review-surface"}:
        hints["data_display"] = {
            "direction": "정보 밀도를 유지하되 thin dividers와 restrained accent로 hierarchy를 만든다.",
            "confidence": round(max(0.3 if query_only else 0.52, (visual_motifs.get("density") or {}).get("confidence", 0.0)), 2),
            "evidence": [f"layout={data_layout or 'n/a'}", f"density={density}"],
        }

    if top_layout == "conversation-panel" or "chat" in primitives:
        hints["panel"] = {
            "direction": "보조 패널은 메인 표면보다 한 단계 더 조용한 tint와 명확한 section framing으로 구분한다.",
            "confidence": round(max(0.3 if query_only else 0.5, layout_cues[0]["confidence"] if layout_cues else 0.0), 2),
            "evidence": [cue["label"] for cue in layout_cues[:1]] or ["Conversation signal"],
        }

    if top_layout == "landing-narrative":
        hints["hero"] = {
            "direction": "대형 hero와 trust strip, CTA cluster를 허용하되 과장된 glass/gradient 효과는 지양한다.",
            "confidence": round(layout_cues[0]["confidence"], 2),
            "evidence": [cue["label"] for cue in layout_cues[:1]],
        }

    return {
        name: _with_provenance(
            _adjust_inferred_choice(hint, query_only=query_only, ceiling=0.46),
            level="inferred",
            detail=(
                "Component styling hint synthesized from query and brand context only; local image grounding was unavailable."
                if query_only
                else "Component styling hint synthesized from visual motifs and layout cues."
            ),
        )
        for name, hint in hints.items()
    }


def _build_reference_mood_summary(
    visual_motifs: dict,
    layout_cues: list[dict],
    component_style_hints: dict,
    config: dict,
    brand_profile: dict,
) -> dict:
    top_layout = layout_cues[0]["label"] if layout_cues else "No dominant layout cue"
    typography_mood = (visual_motifs.get("typography_mood") or {}).get("value")
    density = (visual_motifs.get("density") or {}).get("value")
    surface_style = (visual_motifs.get("surface_style") or {}).get("value")
    color_balance = visual_motifs.get("color_balance") or {}

    recommended = [
        f"layout는 {top_layout} 기준으로 정리",
        f"surface language는 {surface_style} 성향 우선",
        f"typography mood는 {typography_mood} 축 유지",
        f"density는 {density} 기준으로 primitive spacing 조정",
    ]
    if color_balance.get("temperature"):
        recommended.append(f"palette temperature는 {color_balance.get('temperature')} 쪽을 우선")

    avoid = list(config.get("avoid_patterns", []))
    if not avoid and brand_profile.get("anti_keywords"):
        avoid = [f"{keyword}하게 보이는 시각 패턴" for keyword in brand_profile.get("anti_keywords", [])[:3]]

    return _with_provenance(
        {
        "top_layout": top_layout,
        "recommended_direction": recommended,
        "avoidance": avoid,
        "component_focus": sorted(component_style_hints.keys()),
        },
        level="inferred",
        detail="Mood summary synthesized from visual motifs, layout cues, and component hints.",
    )


def _build_candidate_component_archetypes(
    selected_images: list[dict],
    image_records: list[dict],
    layout_cues: list[dict],
    visual_motifs: dict,
    config: dict,
    brand_profile: dict,
) -> list[dict]:
    query_only = not image_records
    term_counts = _collect_term_counts(selected_images, config, brand_profile)
    layout_confidence = {cue["id"]: cue["confidence"] for cue in layout_cues}
    primitives = {item.lower() for item in brand_profile.get("product_primitives", [])}

    candidates: list[dict] = []
    for definition in COMPONENT_ARCHETYPE_DEFINITIONS:
        score = 0.0
        evidence: list[str] = []

        for layout_id in definition.get("layout_matches", []):
            confidence = layout_confidence.get(layout_id, 0.0)
            if confidence:
                score += 6 * confidence
                evidence.append(f"layout={layout_id} ({confidence})")

        for keyword, keyword_weight in definition.get("keywords", {}).items():
            hits = term_counts.get(keyword, 0)
            if hits:
                score += hits * keyword_weight
                evidence.append(f"{keyword} x{hits}")

        for primitive in definition.get("primitive_matches", []):
            if primitive.lower() in primitives:
                score += 3
                evidence.append(f"primitive={primitive}")

        if definition["id"] == "workspace-shell":
            density = (visual_motifs.get("density") or {}).get("value")
            if density in {"balanced", "dense"}:
                score += 1
        if definition["id"] == "editorial-content-block":
            mood = (visual_motifs.get("typography_mood") or {}).get("value")
            if mood == "editorial":
                score += 2
        if definition["id"] == "dashboard-insight-module":
            if (visual_motifs.get("density") or {}).get("value") == "dense":
                score += 1.5

        if score < (5.5 if query_only else 4.5):
            continue

        candidates.append(
            _with_provenance(
                {
                "id": definition["id"],
                "label": definition["label"],
                "family": definition["family"],
                "confidence": _query_only_confidence(
                    _confidence_from_score(score, 0.25),
                    query_only=query_only,
                    ceiling=0.48,
                ),
                "suggested_components": definition["suggested_components"],
                "supports_primitives": definition.get("primitive_matches", []),
                "evidence": evidence[:6],
                },
                level="inferred",
                detail=(
                    "Archetype candidate inferred from query and brand context only; local image grounding was unavailable."
                    if query_only
                    else "Archetype candidate inferred from layout cues, image signals, and product primitives."
                ),
            )
        )

    candidates.sort(key=lambda item: (-item["confidence"], item["label"]))
    return candidates[:6]


def _build_brand_context(brand_profile: dict) -> dict:
    return {
        "brand_name": brand_profile.get("brand_name"),
        "system_name": brand_profile.get("system_name"),
        "brand_keywords": brand_profile.get("brand_keywords", []),
        "anti_keywords": brand_profile.get("anti_keywords", []),
        "visual_keywords": brand_profile.get("visual_keywords", []),
        "interaction_keywords": brand_profile.get("interaction_keywords", []),
        "product_primitives": brand_profile.get("product_primitives", []),
    }


def _with_provenance(payload: dict, level: str, detail: str) -> dict:
    enriched = dict(payload)
    enriched["provenance"] = {
        "level": level,
        "detail": detail,
    }
    return enriched


def _collect_term_counts(
    selected_images: list[dict],
    config: dict,
    brand_profile: dict,
) -> Counter:
    counts: Counter = Counter()

    for record in selected_images:
        _add_weighted_tokens(counts, record.get("signal_terms", []), weight=1.5)

    _add_weighted_tokens(counts, config.get("query", []), weight=0.45)
    _add_weighted_tokens(counts, config.get("must_include", []), weight=0.9)
    _add_weighted_tokens(counts, config.get("avoid_patterns", []), weight=0.15)
    _add_weighted_tokens(counts, config.get("notes", []), weight=0.2)

    _add_weighted_tokens(counts, brand_profile.get("brand_keywords", []), weight=0.75)
    _add_weighted_tokens(counts, brand_profile.get("anti_keywords", []), weight=0.1)
    _add_weighted_tokens(counts, brand_profile.get("visual_keywords", []), weight=0.8)
    _add_weighted_tokens(counts, brand_profile.get("interaction_keywords", []), weight=0.45)
    _add_weighted_tokens(counts, brand_profile.get("product_primitives", []), weight=0.9)

    return counts


def _add_weighted_tokens(counts: Counter, values: list[str], weight: float) -> None:
    if not values or weight <= 0:
        return
    for value in values:
        seen_tokens: set[str] = set()
        for token in _tokenize_text_list([value]):
            if token in seen_tokens:
                continue
            seen_tokens.add(token)
            counts[token] += weight


def _query_only_confidence(confidence: float, query_only: bool, ceiling: float) -> float:
    if not query_only:
        return round(confidence, 2)
    return round(min(confidence * 0.55, ceiling), 2)


def _adjust_inferred_choice(payload: dict, query_only: bool, ceiling: float) -> dict:
    adjusted = dict(payload)
    adjusted["confidence"] = _query_only_confidence(float(payload.get("confidence", 0.0)), query_only=query_only, ceiling=ceiling)
    return adjusted


def _extract_signal_terms(path: Path, label: str, tags: list[str]) -> list[str]:
    parts = [path.stem, path.parent.name, label, *tags]
    return sorted(set(_tokenize_text_list(parts)))


def _tokenize_text_list(values: list[str]) -> list[str]:
    tokens: list[str] = []
    for value in values:
        tokens.extend(
            token.lower()
            for token in TEXT_TOKEN_RE.findall(str(value))
            if token.strip()
        )
    return tokens


def _score_named_choice(
    definitions: dict[str, dict[str, int]],
    term_counts: Counter,
    fallback: str,
    weight: float,
    aspect_counts: Counter | None = None,
    orientation_counts: Counter | None = None,
) -> dict:
    candidates: list[tuple[float, str, list[str]]] = []
    for label, mapping in definitions.items():
        score = 0.0
        evidence: list[str] = []
        for keyword, keyword_weight in mapping.items():
            hits = term_counts.get(keyword, 0)
            if hits:
                score += hits * keyword_weight
                evidence.append(f"{keyword} x{hits}")
        if label == "airy" and aspect_counts and aspect_counts.get("16:9-ish"):
            score += 0.8
        if label == "dense" and orientation_counts and orientation_counts.get("landscape"):
            score += 0.5
        candidates.append((score, label, evidence))

    candidates.sort(key=lambda item: (-item[0], item[1]))
    best_score, best_label, evidence = candidates[0] if candidates else (0.0, fallback, [])
    if best_score <= 0:
        best_label = fallback
        evidence = [f"fallback={fallback}"]

    return {
        "value": best_label,
        "confidence": _confidence_from_score(best_score, weight),
        "evidence": evidence[:6],
        "candidates": [
            {
                "value": label,
                "score": round(score, 2),
            }
            for score, label, _ in candidates[:4]
            if score > 0
        ],
    }


def _score_corner_style(
    selected_images: list[dict],
    term_counts: Counter,
    weight: float,
) -> dict:
    candidates = []
    svg_ratios = [
        record.get("svg_features", {}).get("max_rect_corner_ratio", 0.0)
        for record in selected_images
        if record.get("svg_features")
    ]
    max_ratio = max(svg_ratios) if svg_ratios else 0.0

    for label, mapping in CORNER_STYLE_DEFINITIONS.items():
        score = 0.0
        evidence: list[str] = []
        for keyword, keyword_weight in mapping.items():
            hits = term_counts.get(keyword, 0)
            if hits:
                score += hits * keyword_weight
                evidence.append(f"{keyword} x{hits}")

        if label == "pill" and max_ratio >= 0.35:
            score += 3
            evidence.append(f"svg corner ratio {max_ratio:.2f}")
        elif label == "round" and max_ratio >= 0.12:
            score += 2
            evidence.append(f"svg corner ratio {max_ratio:.2f}")
        elif label == "medium" and max_ratio >= 0.04:
            score += 1.5
            evidence.append(f"svg corner ratio {max_ratio:.2f}")
        elif label == "sharp" and 0 < max_ratio < 0.04:
            score += 1.5
            evidence.append(f"svg corner ratio {max_ratio:.2f}")

        candidates.append((score, label, evidence))

    candidates.sort(key=lambda item: (-item[0], item[1]))
    best_score, best_label, evidence = candidates[0] if candidates else (0.0, "medium", [])
    if best_score <= 0:
        best_label = "medium"
        evidence = ["fallback=medium"]

    return {
        "value": best_label,
        "confidence": _confidence_from_score(best_score, weight),
        "evidence": evidence[:6],
    }


def _summarize_color_balance(selected_images: list[dict]) -> dict:
    aggregated: list[dict] = []
    for record in selected_images:
        aggregated.extend(record.get("observed_colors", []))

    if not aggregated:
        return {
            "observed": False,
            "temperature": "unknown",
            "contrast_profile": "unknown",
            "neutral_bias": "unknown",
            "dominant": [],
            "supporting": [],
        }

    counter: dict[str, dict] = {}
    for item in aggregated:
        hex_value = item["hex"]
        entry = counter.setdefault(
            hex_value,
            {
                "hex": hex_value,
                "count": 0.0,
                "temperature": item.get("temperature"),
                "luminance": item.get("luminance"),
                "role_hint": item.get("role_hint"),
            },
        )
        entry["count"] += float(item.get("count", 0))

    colors = sorted(counter.values(), key=lambda item: (-item["count"], item["hex"]))
    total = sum(item["count"] for item in colors) or 1.0
    for item in colors:
        item["share"] = round(item["count"] / total, 4)

    temperature_score = 0.0
    luminances = []
    neutral_share = 0.0
    for item in colors:
        share = item["share"]
        luminance = float(item.get("luminance") or 0.5)
        luminances.append(luminance)
        if item.get("temperature") == "warm":
            temperature_score += share
        elif item.get("temperature") == "cool":
            temperature_score -= share
        if str(item.get("role_hint", "")).startswith("neutral"):
            neutral_share += share

    if temperature_score > 0.18:
        temperature = "warm"
    elif temperature_score < -0.18:
        temperature = "cool"
    else:
        temperature = "balanced"

    contrast_span = (max(luminances) - min(luminances)) if luminances else 0.0
    if contrast_span >= 0.65:
        contrast_profile = "high"
    elif contrast_span >= 0.35:
        contrast_profile = "balanced"
    else:
        contrast_profile = "soft"

    if neutral_share >= 0.55:
        neutral_bias = "high"
    elif neutral_share >= 0.3:
        neutral_bias = "moderate"
    else:
        neutral_bias = "low"

    return {
        "observed": True,
        "temperature": temperature,
        "contrast_profile": contrast_profile,
        "neutral_bias": neutral_bias,
        "dominant": colors[:3],
        "supporting": colors[3:8],
    }


def _describe_card_direction(surface_style: str, density: str, corner_style: str) -> str:
    base = {
        "flat": "flat card planes",
        "tinted": "low-elevation tinted cards",
        "outlined": "outlined cards with thin framing",
        "elevated": "raised cards with restrained depth",
        "glassy": "translucent cards with strict contrast guardrails",
    }.get(surface_style, "measured card surfaces")
    density_note = {
        "airy": "넓은 내부 여백과 강한 section breathing room",
        "balanced": "균형 잡힌 spacing과 명확한 slot hierarchy",
        "dense": "압축된 spacing과 얇은 divider 중심의 hierarchy",
    }.get(density, "균형 잡힌 spacing")
    corner_note = {
        "pill": "pill-like actions만 제한적으로 허용",
        "round": "soft round corner를 기본값으로 유지",
        "medium": "중간 반경으로 제품 UI 절제 유지",
        "sharp": "sharp edge와 얇은 framing으로 긴장감 유지",
    }.get(corner_style, "중간 반경 유지")
    return f"{base}를 기본으로 하고, {density_note}. {corner_note}."


def _describe_navigation_direction(top_layout: str | None, density: str) -> str:
    if top_layout == "split-pane-workspace":
        return "고정 sidebar 또는 split-pane navigation을 우선하고, 현재 위치와 scope를 항상 명시한다."
    if top_layout == "landing-narrative":
        return "top navigation은 가볍게 유지하고 CTA와 section anchors를 분명하게 분리한다."
    if density == "dense":
        return "navigation은 compact하게 유지하되 filter/scope controls와 혼합하지 않는다."
    return "navigation은 정보 구조를 안정적으로 고정하고 시각적 장식보다 위치 신호를 우선한다."


def _describe_typography_direction(typography_mood: str, density: str) -> str:
    if typography_mood == "editorial":
        return "headline rhythm과 본문 리듬의 대비를 키우고, label/metadata는 조용하게 유지한다."
    if typography_mood == "premium":
        return "headline은 절제된 대비와 넉넉한 spacing으로 품격을 만들고 과장된 장식은 피한다."
    if typography_mood == "playful":
        return "표현력은 허용하되 제품 UI에서는 heading 수와 accent를 엄격히 제한한다."
    if density == "dense":
        return "정보 밀도에 맞춰 type scale 차이를 줄이고 table/list label의 정렬 정확도를 우선한다."
    return "utilitarian hierarchy를 유지하되 중요한 heading만 선택적으로 크게 만든다."


def _confidence_from_score(score: float, weight: float) -> float:
    normalized = max(0.0, score) * (0.75 + weight)
    return round(min(0.94, 0.24 + normalized / 20.0), 2)

def _detect_duplicate_groups(image_records: list[dict]) -> list[dict]:
    by_hash: dict[str, list[dict]] = defaultdict(list)
    for record in image_records:
        by_hash[record["sha256"]].append(record)

    groups = []
    for digest, members in sorted(by_hash.items()):
        if len(members) < 2:
            continue
        groups.append(
            {
                "type": "exact",
                "signature": digest[:12],
                "image_ids": [member["image_id"] for member in members],
                "paths": [member["relative_path"] for member in members],
            }
        )
    return groups


def _detect_similar_groups(image_records: list[dict]) -> list[dict]:
    groups: list[dict] = []

    by_shape: dict[tuple[object, object, object], list[dict]] = defaultdict(list)
    for record in image_records:
        signature = (
            record.get("aspect_ratio_bucket"),
            record.get("orientation"),
            record.get("extension"),
        )
        by_shape[signature].append(record)

    for signature, members in sorted(by_shape.items()):
        if len(members) < 2:
            continue
        groups.append(
            {
                "type": "shape-family",
                "signature": " / ".join(str(item) for item in signature if item),
                "image_ids": [member["image_id"] for member in members],
                "paths": [member["relative_path"] for member in members],
            }
        )
    return groups


def _normalize_weight_map(raw_weights: object) -> dict:
    defaults = dict(DEFAULT_VISUAL_REFERENCE["weights"])
    if isinstance(raw_weights, dict):
        for key in WEIGHT_KEYS:
            value = raw_weights.get(key)
            if isinstance(value, (int, float)):
                defaults[key] = max(0.0, float(value))

    total = sum(defaults.values()) or 1.0
    return {
        key: round(defaults[key] / total, 4)
        for key in WEIGHT_KEYS
    }


def _normalize_text_list(values: object) -> list[str]:
    if not isinstance(values, list):
        return []
    return [str(item).strip() for item in values if str(item).strip()]


def _pick_enum(value: object, allowed: set[str], fallback: str) -> str:
    candidate = str(value).strip()
    return candidate if candidate in allowed else fallback


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        while True:
            chunk = handle.read(1024 * 1024)
            if not chunk:
                break
            digest.update(chunk)
    return digest.hexdigest()


def _relative_display_path(path: Path, base_dir: Path) -> str:
    try:
        return str(path.relative_to(base_dir))
    except ValueError:
        return str(path)


def _classify_orientation(width: int | None, height: int | None) -> str:
    if not width or not height:
        return "unknown"
    if 0.95 <= (width / height) <= 1.05:
        return "square"
    if width > height:
        return "landscape"
    return "portrait"


def _bucket_aspect_ratio(width: int | None, height: int | None) -> str:
    if not width or not height:
        return "unknown"

    ratio = width / height
    if 0.95 <= ratio <= 1.05:
        return "1:1"
    if 0.7 <= ratio < 0.95:
        return "4:5-ish"
    if 0.52 <= ratio < 0.7:
        return "2:3-ish"
    if 1.2 <= ratio < 1.5:
        return "4:3-ish"
    if 1.5 <= ratio < 1.9:
        return "3:2-ish"
    if 1.9 <= ratio < 2.3:
        return "16:9-ish"
    return "other"


def _extract_observed_colors(path: Path) -> list[dict]:
    suffix = path.suffix.lower()
    try:
        if suffix == ".svg":
            return _extract_svg_colors(path)
        if Image is not None and suffix in {".png", ".jpg", ".jpeg", ".webp", ".gif", ".bmp"}:
            return _extract_raster_colors(path)
    except Exception:
        return []
    return []


def _extract_svg_colors(path: Path) -> list[dict]:
    text = path.read_text(encoding="utf-8")
    counts = Counter(match.group(0).upper() for match in COLOR_HEX_RE.finditer(text))
    total = sum(counts.values()) or 1
    colors = []
    for hex_value, count in counts.most_common(8):
        colors.append(_build_color_observation(hex_value, float(count), float(count) / total))
    return colors


def _extract_raster_colors(path: Path) -> list[dict]:
    if Image is None:
        return []

    with Image.open(path) as image:
        image = image.convert("RGB")
        image.thumbnail((160, 160))
        quantized = image.quantize(colors=8, method=Image.Quantize.MEDIANCUT)
        palette = quantized.getpalette() or []
        total = sum(count for count, _ in (quantized.getcolors() or [])) or 1

        observations = []
        for count, palette_index in sorted(quantized.getcolors() or [], reverse=True)[:8]:
            offset = palette_index * 3
            rgb = tuple(palette[offset:offset + 3])
            if len(rgb) != 3:
                continue
            hex_value = "#{:02X}{:02X}{:02X}".format(*rgb)
            observations.append(_build_color_observation(hex_value, float(count), float(count) / total))
        return observations


def _build_color_observation(hex_value: str, count: float, share: float) -> dict:
    rgb = _hex_to_rgb(hex_value)
    if not rgb:
        return {
            "hex": hex_value,
            "count": count,
            "share": round(share, 4),
            "temperature": "unknown",
            "luminance": None,
            "role_hint": "unknown",
        }

    temperature = _classify_color_temperature(rgb)
    luminance = _relative_luminance(rgb)
    role_hint = _classify_color_role(rgb, luminance)
    return {
        "hex": hex_value,
        "count": count,
        "share": round(share, 4),
        "temperature": temperature,
        "luminance": round(luminance, 4),
        "role_hint": role_hint,
    }


def _hex_to_rgb(hex_value: str) -> tuple[int, int, int] | None:
    value = hex_value.lstrip("#")
    if len(value) == 3:
        value = "".join(ch * 2 for ch in value)
    if len(value) != 6:
        return None
    try:
        return tuple(int(value[index:index + 2], 16) for index in range(0, 6, 2))
    except ValueError:
        return None


def _classify_color_temperature(rgb: tuple[int, int, int]) -> str:
    hue, saturation, _ = colorsys.rgb_to_hsv(*(channel / 255 for channel in rgb))
    if saturation < 0.08:
        return "neutral"
    degrees = hue * 360
    if degrees <= 65 or degrees >= 320:
        return "warm"
    if 65 < degrees <= 170:
        return "natural"
    return "cool"


def _classify_color_role(rgb: tuple[int, int, int], luminance: float) -> str:
    _, saturation, _ = colorsys.rgb_to_hsv(*(channel / 255 for channel in rgb))
    if saturation < 0.12 and luminance >= 0.82:
        return "neutral-light"
    if saturation < 0.12 and luminance <= 0.2:
        return "neutral-dark"
    if saturation < 0.18:
        return "neutral-mid"
    if luminance < 0.28:
        return "accent-dark"
    if luminance > 0.78:
        return "accent-light"
    return "accent"


def _relative_luminance(rgb: tuple[int, int, int]) -> float:
    def _channel(value: int) -> float:
        value = value / 255
        if value <= 0.04045:
            return value / 12.92
        return ((value + 0.055) / 1.055) ** 2.4

    r, g, b = (_channel(channel) for channel in rgb)
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def _extract_svg_features(path: Path) -> dict:
    if path.suffix.lower() != ".svg":
        return {}
    try:
        root = ElementTree.fromstring(path.read_text(encoding="utf-8"))
    except Exception:
        return {}

    rect_corner_ratios: list[float] = []
    has_stroke = False
    for element in root.iter():
        if element.tag.endswith("rect"):
            width = _parse_svg_length(element.get("width")) or 0
            height = _parse_svg_length(element.get("height")) or 0
            rx = _parse_svg_length(element.get("rx")) or _parse_svg_length(element.get("ry")) or 0
            if width and height and rx:
                rect_corner_ratios.append(rx / min(width, height))
        stroke = element.get("stroke")
        if stroke and stroke.lower() not in {"none", "transparent"}:
            has_stroke = True

    return {
        "max_rect_corner_ratio": round(max(rect_corner_ratios), 4) if rect_corner_ratios else 0.0,
        "has_stroke": has_stroke,
    }


def _read_image_metadata(path: Path) -> dict:
    width, height = _read_image_dimensions(path)
    return {
        "width": width,
        "height": height,
        "mime_type": _detect_image_mime_type(path),
    }


def _detect_image_mime_type(path: Path) -> str | None:
    suffix = path.suffix.lower()
    if suffix == ".svg":
        return "image/svg+xml"

    try:
        header = path.read_bytes()[:16]
    except OSError:
        return MIME_BY_EXTENSION.get(suffix)

    for signature, mime_type in RASTER_MIME_SIGNATURES:
        if header.startswith(signature):
            return mime_type
    if header[:4] == b"RIFF" and header[8:12] == b"WEBP":
        return "image/webp"
    return MIME_BY_EXTENSION.get(suffix)


def _read_image_dimensions(path: Path) -> tuple[int | None, int | None]:
    suffix = path.suffix.lower()
    try:
        if suffix == ".png":
            return _read_png_dimensions(path)
        if suffix in {".jpg", ".jpeg"}:
            return _read_jpeg_dimensions(path)
        if suffix == ".webp":
            return _read_webp_dimensions(path)
        if suffix == ".gif":
            return _read_gif_dimensions(path)
        if suffix == ".bmp":
            return _read_bmp_dimensions(path)
        if suffix == ".svg":
            return _read_svg_dimensions(path)
    except Exception:
        return None, None
    return None, None


def _read_png_dimensions(path: Path) -> tuple[int | None, int | None]:
    with path.open("rb") as handle:
        header = handle.read(24)
    if len(header) < 24 or header[:8] != b"\x89PNG\r\n\x1a\n":
        return None, None
    return struct.unpack(">II", header[16:24])


def _read_gif_dimensions(path: Path) -> tuple[int | None, int | None]:
    with path.open("rb") as handle:
        header = handle.read(10)
    if len(header) < 10 or not header.startswith((b"GIF87a", b"GIF89a")):
        return None, None
    return struct.unpack("<HH", header[6:10])


def _read_bmp_dimensions(path: Path) -> tuple[int | None, int | None]:
    with path.open("rb") as handle:
        header = handle.read(26)
    if len(header) < 26 or header[:2] != b"BM":
        return None, None
    width, height = struct.unpack("<ii", header[18:26])
    return abs(width), abs(height)


def _read_jpeg_dimensions(path: Path) -> tuple[int | None, int | None]:
    with path.open("rb") as handle:
        if handle.read(2) != b"\xff\xd8":
            return None, None
        while True:
            byte = handle.read(1)
            if not byte:
                return None, None
            if byte != b"\xff":
                continue

            while byte == b"\xff":
                byte = handle.read(1)
            if not byte:
                return None, None

            marker = byte[0]
            if marker in {0xD8, 0xD9}:
                continue

            length_bytes = handle.read(2)
            if len(length_bytes) != 2:
                return None, None
            segment_length = struct.unpack(">H", length_bytes)[0]
            if segment_length < 2:
                return None, None

            if marker in {
                0xC0,
                0xC1,
                0xC2,
                0xC3,
                0xC5,
                0xC6,
                0xC7,
                0xC9,
                0xCA,
                0xCB,
                0xCD,
                0xCE,
                0xCF,
            }:
                data = handle.read(segment_length - 2)
                if len(data) < 5:
                    return None, None
                height, width = struct.unpack(">HH", data[1:5])
                return width, height

            handle.seek(segment_length - 2, 1)


def _read_webp_dimensions(path: Path) -> tuple[int | None, int | None]:
    with path.open("rb") as handle:
        header = handle.read(64)
    if len(header) < 30 or header[:4] != b"RIFF" or header[8:12] != b"WEBP":
        return None, None

    chunk = header[12:16]
    if chunk == b"VP8 " and len(header) >= 30:
        width, height = struct.unpack("<HH", header[26:30])
        return width & 0x3FFF, height & 0x3FFF

    if chunk == b"VP8L" and len(header) >= 25:
        b0, b1, b2, b3 = header[21:25]
        width = 1 + (((b1 & 0x3F) << 8) | b0)
        height = 1 + (((b3 & 0x0F) << 10) | (b2 << 2) | ((b1 & 0xC0) >> 6))
        return width, height

    if chunk == b"VP8X" and len(header) >= 30:
        width = 1 + int.from_bytes(header[24:27], "little")
        height = 1 + int.from_bytes(header[27:30], "little")
        return width, height

    return None, None


def _read_svg_dimensions(path: Path) -> tuple[int | None, int | None]:
    root = ElementTree.fromstring(path.read_text(encoding="utf-8"))
    width = _parse_svg_length(root.get("width"))
    height = _parse_svg_length(root.get("height"))

    if width and height:
        return width, height

    view_box = root.get("viewBox") or root.get("viewbox")
    if view_box:
        parts = re.split(r"[,\s]+", view_box.strip())
        if len(parts) == 4:
            try:
                return int(float(parts[2])), int(float(parts[3]))
            except ValueError:
                return None, None
    return None, None


def _parse_svg_length(value: str | None) -> int | None:
    if not value:
        return None
    match = re.search(r"([0-9]+(?:\.[0-9]+)?)", value)
    if not match:
        return None
    return int(float(match.group(1)))
