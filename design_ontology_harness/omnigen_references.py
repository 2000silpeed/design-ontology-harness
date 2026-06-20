from __future__ import annotations

import json
import os
import shutil
import sqlite3
from pathlib import Path
from typing import Any

from .models import utc_now_iso
from .utils import ensure_dir, slugify

DEFAULT_OMNIGEN_VAULT_DIR = Path.home() / ".omnigen-vault"
DEFAULT_CATEGORIES = ("web-design", "app-design", "mobile-design")
DEFAULT_REFERENCE_DIR = "build/visuals/omnigen-selected"
MANAGED_PROVIDER_ID = "omnigen-vault"

IMAGE_COLUMNS = (
    "id",
    "category",
    "subject",
    "style",
    "lighting",
    "palette",
    "composition",
    "mood",
    "variant",
    "prompt",
    "revised_prompt",
    "rel_path",
    "abs_path",
    "width",
    "height",
    "size_label",
    "bytes",
    "sha256",
    "bucket",
    "phash",
    "thumb_rel",
    "thumb_abs",
    "rating",
    "ocr_char_count",
    "ocr_text",
    "status",
    "tags",
    "created_at",
)


def select_omnigen_references(
    *,
    vault_dir: Path | str = DEFAULT_OMNIGEN_VAULT_DIR,
    project_dir: Path | str | None = None,
    query: str | None = None,
    categories: list[str] | None = None,
    count: int = 12,
    orientation: str = "any",
    max_per_subject: int = 2,
    min_rating: int | None = None,
    max_ocr_chars: int | None = None,
    link_mode: str = "symlink",
    reference_dir: str | Path = DEFAULT_REFERENCE_DIR,
) -> dict[str, Any]:
    """Select a small, local-only visual reference set from an Omnigen vault.

    The selector intentionally writes only manifest metadata plus optional local
    symlinks/copies. It never makes the vault a packaged dependency of the
    harness.
    """

    vault_path = Path(vault_dir).expanduser().resolve()
    index_path = vault_path / "index.sqlite"
    if not index_path.exists():
        raise FileNotFoundError(f"Omnigen index not found: {index_path}")

    normalized_categories = _normalize_categories(categories)
    requested_count = max(1, min(48, int(count or 12)))
    normalized_orientation = _normalize_orientation(orientation)
    normalized_link_mode = _normalize_link_mode(link_mode)
    normalized_max_per_subject = max(1, int(max_per_subject or 2))
    query_terms = _tokenize(query or "")

    candidates = _load_candidates(
        index_path=index_path,
        categories=normalized_categories,
        orientation=normalized_orientation,
        min_rating=min_rating,
        max_ocr_chars=max_ocr_chars,
    )
    scored_candidates = [
        _score_candidate(candidate, query_terms=query_terms, vault_dir=vault_path)
        for candidate in candidates
    ]
    scored_candidates = [candidate for candidate in scored_candidates if candidate["exists"]]
    selected = _select_diverse_candidates(
        scored_candidates,
        count=requested_count,
        max_per_subject=normalized_max_per_subject,
    )

    project_path = Path(project_dir).resolve() if project_dir else None
    reference_root = _resolve_reference_root(project_path, reference_dir)
    materialized = _materialize_selected(
        selected,
        reference_root=reference_root,
        project_dir=project_path,
        link_mode=normalized_link_mode,
    )

    return {
        "schema_version": "omnigen-reference-selection/v1",
        "created_at": utc_now_iso(),
        "provider_id": MANAGED_PROVIDER_ID,
        "vault_dir": str(vault_path),
        "index_path": str(index_path),
        "query": query or "",
        "query_terms": query_terms,
        "categories": normalized_categories,
        "requested_count": requested_count,
        "selected_count": len(materialized),
        "available_candidate_count": len(candidates),
        "scored_candidate_count": len(scored_candidates),
        "selection_policy": {
            "orientation": normalized_orientation,
            "max_per_subject": normalized_max_per_subject,
            "min_rating": min_rating,
            "max_ocr_chars": max_ocr_chars,
            "link_mode": normalized_link_mode,
            "reference_dir": str(reference_dir),
            "redistribution_allowed": False,
            "usage_scope": "reference-analysis-only",
        },
        "selected": materialized,
    }


def sync_omnigen_sources(
    *,
    raw_brand_profile: dict[str, Any],
    selection_manifest: dict[str, Any],
    base_dir: Path,
) -> dict[str, int]:
    visual_reference = raw_brand_profile.setdefault("visual_reference", {})
    if not isinstance(visual_reference, dict):
        visual_reference = {}
        raw_brand_profile["visual_reference"] = visual_reference

    visual_reference.setdefault("mode", "local-images")
    visual_reference.setdefault("extraction_policy", "advisory-only")
    visual_reference["preferred_count"] = max(
        int(visual_reference.get("preferred_count", 0) or 0),
        int(selection_manifest.get("selected_count", 0) or 0),
    )

    existing_sources = visual_reference.get("sources", [])
    if not isinstance(existing_sources, list):
        existing_sources = []

    preserved_sources = [
        source
        for source in existing_sources
        if not _is_managed_omnigen_source(source)
    ]
    merged_sources = list(preserved_sources)
    existing_keys = {
        _source_entry_identity(source, base_dir=base_dir)
        for source in merged_sources
    }

    for item in selection_manifest.get("selected", []) or []:
        source = _source_entry_from_selection(item, base_dir=base_dir)
        identity = _source_entry_identity(source, base_dir=base_dir)
        if identity in existing_keys:
            continue
        merged_sources.append(source)
        existing_keys.add(identity)

    visual_reference["sources"] = merged_sources
    return {
        "selected_count": int(selection_manifest.get("selected_count", 0) or 0),
        "managed_source_count": len(merged_sources) - len(preserved_sources),
        "total_source_count": len(merged_sources),
    }


def _load_candidates(
    *,
    index_path: Path,
    categories: list[str],
    orientation: str,
    min_rating: int | None,
    max_ocr_chars: int | None,
) -> list[dict[str, Any]]:
    placeholders = ",".join("?" for _ in categories)
    conditions = ["status = 'active'", f"category in ({placeholders})"]
    params: list[Any] = list(categories)

    if orientation == "landscape":
        conditions.append("width >= height")
    elif orientation == "portrait":
        conditions.append("height > width")

    if min_rating is not None:
        conditions.append("rating >= ?")
        params.append(int(min_rating))

    if max_ocr_chars is not None:
        conditions.append("(ocr_char_count is null or ocr_char_count <= ?)")
        params.append(int(max_ocr_chars))

    sql = (
        f"select {', '.join(IMAGE_COLUMNS)} from images "
        f"where {' and '.join(conditions)}"
    )
    with sqlite3.connect(index_path) as connection:
        connection.row_factory = sqlite3.Row
        rows = connection.execute(sql, params).fetchall()
    return [dict(row) for row in rows]


def _score_candidate(
    candidate: dict[str, Any],
    *,
    query_terms: list[str],
    vault_dir: Path,
) -> dict[str, Any]:
    abs_path = _resolve_candidate_path(candidate, vault_dir)
    haystacks = {
        "category": str(candidate.get("category") or "").lower(),
        "subject": str(candidate.get("subject") or "").lower(),
        "style": str(candidate.get("style") or "").lower(),
        "palette": str(candidate.get("palette") or "").lower(),
        "composition": str(candidate.get("composition") or "").lower(),
        "mood": str(candidate.get("mood") or "").lower(),
        "tags": str(candidate.get("tags") or "").lower(),
        "prompt": " ".join(
            [
                str(candidate.get("prompt") or ""),
                str(candidate.get("revised_prompt") or ""),
                str(candidate.get("ocr_text") or ""),
            ]
        ).lower(),
    }
    weights = {
        "subject": 10,
        "tags": 7,
        "style": 5,
        "palette": 3,
        "composition": 4,
        "mood": 4,
        "category": 3,
        "prompt": 2,
    }
    matches: list[dict[str, Any]] = []
    score = 0
    for term in query_terms:
        for field, text in haystacks.items():
            if term in text:
                weight = weights[field]
                score += weight
                matches.append({"term": term, "field": field, "weight": weight})

    rating = int(candidate.get("rating") or 0)
    score += rating * 5
    score += _dimension_bonus(candidate)

    result = dict(candidate)
    result["abs_path"] = str(abs_path)
    result["exists"] = abs_path.exists()
    result["score"] = score
    result["matched_terms"] = matches[:24]
    result["orientation"] = _orientation_for_dimensions(candidate.get("width"), candidate.get("height"))
    return result


def _select_diverse_candidates(
    candidates: list[dict[str, Any]],
    *,
    count: int,
    max_per_subject: int,
) -> list[dict[str, Any]]:
    sorted_candidates = sorted(
        candidates,
        key=lambda item: (
            -int(item.get("score") or 0),
            -int(item.get("rating") or 0),
            str(item.get("subject") or ""),
            str(item.get("sha256") or ""),
        ),
    )

    selected: list[dict[str, Any]] = []
    seen_hashes: set[str] = set()
    seen_phashes: set[str] = set()
    subject_counts: dict[str, int] = {}

    def can_select(candidate: dict[str, Any], *, enforce_subject_limit: bool) -> bool:
        sha = str(candidate.get("sha256") or "")
        phash = str(candidate.get("phash") or "")
        subject = _subject_key(candidate)
        if sha and sha in seen_hashes:
            return False
        if phash and phash in seen_phashes:
            return False
        if enforce_subject_limit and subject_counts.get(subject, 0) >= max_per_subject:
            return False
        return True

    def add(candidate: dict[str, Any]) -> None:
        selected.append(candidate)
        sha = str(candidate.get("sha256") or "")
        phash = str(candidate.get("phash") or "")
        if sha:
            seen_hashes.add(sha)
        if phash:
            seen_phashes.add(phash)
        subject = _subject_key(candidate)
        subject_counts[subject] = subject_counts.get(subject, 0) + 1

    for candidate in sorted_candidates:
        if len(selected) >= count:
            break
        if can_select(candidate, enforce_subject_limit=True):
            add(candidate)

    if len(selected) < count:
        for candidate in sorted_candidates:
            if len(selected) >= count:
                break
            if candidate in selected:
                continue
            if can_select(candidate, enforce_subject_limit=False):
                add(candidate)

    return selected


def _materialize_selected(
    selected: list[dict[str, Any]],
    *,
    reference_root: Path | None,
    project_dir: Path | None,
    link_mode: str,
) -> list[dict[str, Any]]:
    if link_mode != "absolute" and reference_root is not None:
        ensure_dir(reference_root)

    materialized: list[dict[str, Any]] = []
    for rank, candidate in enumerate(selected, start=1):
        source_path = Path(str(candidate["abs_path"]))
        materialized_path: Path | None = None
        if link_mode != "absolute" and reference_root is not None:
            materialized_path = reference_root / _materialized_file_name(rank, candidate, source_path)
            _write_link_or_copy(source_path, materialized_path, link_mode)

        selected_path = materialized_path or source_path
        entry = _public_candidate_fields(candidate)
        entry.update(
            {
                "rank": rank,
                "source_path": str(source_path),
                "selected_path": str(selected_path),
                "selected_relative_path": _relative_to_project(selected_path, project_dir),
                "materialization": link_mode,
                "redistribution_allowed": False,
                "usage_scope": "reference-analysis-only",
            }
        )
        materialized.append(entry)
    return materialized


def _write_link_or_copy(source_path: Path, target_path: Path, link_mode: str) -> None:
    if target_path.exists() or target_path.is_symlink():
        if target_path.is_symlink() and Path(os.readlink(target_path)) == source_path:
            return
        target_path.unlink()

    if link_mode == "symlink":
        target_path.symlink_to(source_path)
        return
    if link_mode == "copy":
        shutil.copy2(source_path, target_path)
        return
    raise ValueError(f"Unsupported link mode for materialization: {link_mode}")


def _source_entry_from_selection(item: dict[str, Any], *, base_dir: Path) -> dict[str, Any]:
    path = str(item.get("selected_relative_path") or item.get("selected_path") or item.get("source_path") or "")
    return {
        "kind": "image",
        "provider_id": MANAGED_PROVIDER_ID,
        "label": f"Omnigen {item.get('category', 'ui')} reference {item.get('rank', '')}".strip(),
        "path": path,
        "tags": _source_tags_from_selection(item),
        "source_url": None,
        "usage_scope": "reference-analysis-only",
        "redistribution_allowed": False,
        "omnigen": {
            "id": item.get("id"),
            "subject": item.get("subject"),
            "style": item.get("style"),
            "palette": item.get("palette"),
            "mood": item.get("mood"),
            "score": item.get("score"),
            "source_path": _relative_or_absolute(Path(str(item.get("source_path") or "")), base_dir),
            "thumb_path": item.get("thumb_abs"),
        },
    }


def _source_tags_from_selection(item: dict[str, Any]) -> list[str]:
    tags = [
        "omnigen-vault",
        "synthetic-ui",
        str(item.get("category") or ""),
        str(item.get("subject") or ""),
        str(item.get("style") or ""),
        str(item.get("palette") or ""),
        str(item.get("mood") or ""),
    ]
    return [slugify(tag) for tag in tags if tag]


def _public_candidate_fields(candidate: dict[str, Any]) -> dict[str, Any]:
    return {
        "id": candidate.get("id"),
        "category": candidate.get("category"),
        "subject": candidate.get("subject"),
        "style": candidate.get("style"),
        "palette": candidate.get("palette"),
        "composition": candidate.get("composition"),
        "mood": candidate.get("mood"),
        "width": candidate.get("width"),
        "height": candidate.get("height"),
        "orientation": candidate.get("orientation"),
        "rating": candidate.get("rating"),
        "ocr_char_count": candidate.get("ocr_char_count"),
        "sha256": candidate.get("sha256"),
        "phash": candidate.get("phash"),
        "thumb_abs": candidate.get("thumb_abs"),
        "score": candidate.get("score"),
        "matched_terms": candidate.get("matched_terms", []),
    }


def _normalize_categories(categories: list[str] | None) -> list[str]:
    normalized = [
        str(category).strip()
        for category in categories or list(DEFAULT_CATEGORIES)
        if str(category).strip()
    ]
    return list(dict.fromkeys(normalized)) or list(DEFAULT_CATEGORIES)


def _normalize_orientation(value: str) -> str:
    normalized = str(value or "any").strip().lower()
    if normalized not in {"any", "landscape", "portrait"}:
        raise ValueError("orientation must be one of: any, landscape, portrait")
    return normalized


def _normalize_link_mode(value: str) -> str:
    normalized = str(value or "symlink").strip().lower()
    if normalized not in {"symlink", "copy", "absolute"}:
        raise ValueError("link_mode must be one of: symlink, copy, absolute")
    return normalized


def _tokenize(value: str) -> list[str]:
    tokens = [
        slug.replace("-", " ")
        for slug in (slugify(part) for part in value.split())
        if slug and len(slug) >= 2
    ]
    compact_tokens = [token.replace(" ", "-") for token in tokens]
    return list(dict.fromkeys(tokens + compact_tokens))


def _resolve_candidate_path(candidate: dict[str, Any], vault_dir: Path) -> Path:
    abs_path = str(candidate.get("abs_path") or "").strip()
    if abs_path:
        return Path(abs_path)
    rel_path = str(candidate.get("rel_path") or "").strip()
    return vault_dir / rel_path


def _resolve_reference_root(project_dir: Path | None, reference_dir: str | Path) -> Path | None:
    if project_dir is None:
        return None
    root = Path(reference_dir)
    if not root.is_absolute():
        root = project_dir / root
    return root.resolve()


def _materialized_file_name(rank: int, candidate: dict[str, Any], source_path: Path) -> str:
    subject = slugify(str(candidate.get("subject") or "ui-reference"))[:64]
    digest = str(candidate.get("sha256") or source_path.stem)[0:12]
    return f"{rank:02d}-{subject}__{digest}{source_path.suffix.lower()}"


def _relative_to_project(path: Path, project_dir: Path | None) -> str:
    if project_dir is None:
        return str(path)
    return _relative_or_absolute(path, project_dir)


def _relative_or_absolute(path: Path, base_dir: Path) -> str:
    try:
        return str(path.resolve().relative_to(base_dir.resolve()))
    except ValueError:
        return str(path)


def _is_managed_omnigen_source(source: Any) -> bool:
    if not isinstance(source, dict):
        return False
    provider = str(source.get("provider_id") or source.get("provider") or "").strip().lower()
    if provider == MANAGED_PROVIDER_ID:
        return True
    path = str(source.get("path") or "").lower()
    return "omnigen-selected" in path


def _source_entry_identity(source: Any, *, base_dir: Path) -> str:
    if isinstance(source, str):
        path = source
    elif isinstance(source, dict):
        path = str(source.get("path") or source.get("url") or source.get("label") or "")
    else:
        path = str(source)
    candidate = Path(path)
    if not candidate.is_absolute():
        candidate = base_dir / candidate
    try:
        return str(candidate.resolve())
    except OSError:
        return str(candidate)


def _subject_key(candidate: dict[str, Any]) -> str:
    return slugify(str(candidate.get("subject") or candidate.get("category") or "reference"))


def _dimension_bonus(candidate: dict[str, Any]) -> int:
    width = int(candidate.get("width") or 0)
    height = int(candidate.get("height") or 0)
    if width >= 1200 and height >= 800:
        return 3
    if width >= 800 and height >= 800:
        return 1
    return 0


def _orientation_for_dimensions(width: Any, height: Any) -> str:
    width_int = int(width or 0)
    height_int = int(height or 0)
    if not width_int or not height_int:
        return "unknown"
    if width_int == height_int:
        return "square"
    return "landscape" if width_int > height_int else "portrait"


def load_omnigen_selection_manifest(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))
