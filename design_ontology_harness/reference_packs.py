from __future__ import annotations

import hashlib
import html as html_lib
import json
import os
import shutil
import sqlite3
from pathlib import Path
from typing import Any
from urllib.parse import urljoin, urlparse

import httpx
from bs4 import BeautifulSoup

from .models import utc_now_iso
from .utils import ensure_dir, slugify

DEFAULT_REFERENCE_PACK_ROOT = Path.home() / ".design-ontology" / "reference-packs"
DEFAULT_REFERENCE_DIR = "build/visuals/reference-pack-selected"
PACK_SCHEMA_VERSION = "visual-reference-pack/v1"
SELECTION_SCHEMA_VERSION = "visual-reference-pack-selection/v1"
MANAGED_PROVIDER_ID = "visual-reference-pack"

IMAGE_EXTENSIONS = {".png", ".jpg", ".jpeg", ".webp", ".gif", ".bmp", ".svg"}

ASSET_COLUMNS = (
    "asset_id",
    "provider_id",
    "category",
    "label",
    "tags",
    "source_url",
    "download_url",
    "local_path",
    "thumb_path",
    "width",
    "height",
    "bytes",
    "sha256",
    "mime_type",
    "usage_scope",
    "redistribution_allowed",
    "provenance_level",
    "created_at",
    "metadata_json",
)


def build_reference_pack(
    *,
    pack_id: str,
    output_dir: Path | str,
    source_dirs: list[Path | str] | None = None,
    source_urls: list[str] | None = None,
    asset_manifest: Path | str | None = None,
    provider_id: str = "local-folder",
    category: str | None = None,
    tags: list[str] | None = None,
    materialize: str = "metadata",
    crawl_depth: int = 0,
    max_pages: int = 16,
    max_assets: int = 500,
) -> dict[str, Any]:
    """Build a portable visual reference pack index.

    The default materialization mode is metadata-only. Use ``copy`` or
    ``symlink`` for local folders, and ``download`` for web image URLs, when the
    pack should carry local assets. Regardless of materialization, every asset is
    reference-analysis-only unless explicit license metadata says otherwise.
    """

    normalized_pack_id = slugify(pack_id)
    if not normalized_pack_id:
        raise ValueError("pack_id is required")
    normalized_materialize = _normalize_materialize(materialize)
    pack_dir = ensure_dir(Path(output_dir).expanduser())
    asset_tags = _normalize_tags(tags)
    records: list[dict[str, Any]] = []

    for source_dir in source_dirs or []:
        records.extend(
            _records_from_source_dir(
                source_dir=Path(source_dir).expanduser(),
                pack_dir=pack_dir,
                provider_id=provider_id,
                category=category or "local-images",
                tags=asset_tags,
                materialize=normalized_materialize,
                remaining=max_assets - len(records),
            )
        )
        if len(records) >= max_assets:
            break

    if len(records) < max_assets and asset_manifest:
        records.extend(
            _records_from_manifest(
                manifest_path=Path(asset_manifest).expanduser(),
                pack_dir=pack_dir,
                default_provider_id=provider_id,
                default_category=category,
                default_tags=asset_tags,
                materialize=normalized_materialize,
                remaining=max_assets - len(records),
            )
        )

    if len(records) < max_assets and source_urls:
        records.extend(
            _records_from_source_urls(
                source_urls=source_urls,
                pack_dir=pack_dir,
                category=category or "web-crawl",
                tags=asset_tags,
                materialize=normalized_materialize,
                crawl_depth=crawl_depth,
                max_pages=max_pages,
                remaining=max_assets - len(records),
            )
        )

    records = _dedupe_assets(records)[:max_assets]
    created_at = utc_now_iso()
    for index, record in enumerate(records, start=1):
        record.setdefault("asset_id", f"{normalized_pack_id}-{index:04d}")
        record.setdefault("created_at", created_at)

    pack = {
        "schema_version": PACK_SCHEMA_VERSION,
        "pack_id": normalized_pack_id,
        "version": created_at[:10].replace("-", "."),
        "created_at": created_at,
        "kind": "visual-reference-pack",
        "asset_count": len(records),
        "provider_ids": sorted({str(record.get("provider_id") or MANAGED_PROVIDER_ID) for record in records}),
        "categories": sorted({str(record.get("category") or "reference") for record in records}),
        "usage_scope": "reference-analysis-only",
        "redistribution_allowed": False,
        "materialization": normalized_materialize,
        "files": {
            "assets": "assets.jsonl",
            "index": "index.sqlite",
            "checksums": "checksums.json",
        },
    }

    _write_pack_files(pack_dir=pack_dir, pack=pack, records=records)
    return pack


def list_reference_packs(pack_root: Path | str = DEFAULT_REFERENCE_PACK_ROOT) -> list[dict[str, Any]]:
    root = Path(pack_root).expanduser()
    if not root.exists():
        return []
    packs: list[dict[str, Any]] = []
    for pack_json in sorted(root.glob("*/pack.json")):
        try:
            pack = json.loads(pack_json.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            continue
        pack["path"] = str(pack_json.parent)
        packs.append(pack)
    return packs


def resolve_reference_pack(pack: str | Path, pack_root: Path | str = DEFAULT_REFERENCE_PACK_ROOT) -> Path:
    candidate = Path(pack).expanduser()
    if candidate.exists():
        return candidate if candidate.is_dir() else candidate.parent
    root_candidate = Path(pack_root).expanduser() / str(pack)
    if root_candidate.exists():
        return root_candidate
    raise FileNotFoundError(f"Reference pack not found: {pack}")


def load_reference_pack(pack_dir: Path | str) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    root = Path(pack_dir).expanduser()
    pack_path = root / "pack.json"
    assets_path = root / "assets.jsonl"
    if not pack_path.exists():
        raise FileNotFoundError(f"pack.json not found: {pack_path}")
    if not assets_path.exists():
        raise FileNotFoundError(f"assets.jsonl not found: {assets_path}")
    pack = json.loads(pack_path.read_text(encoding="utf-8"))
    assets = [
        json.loads(line)
        for line in assets_path.read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]
    return pack, assets


def export_reference_pack_gallery(
    *,
    pack: str | Path,
    output_path: Path | str,
    pack_root: Path | str = DEFAULT_REFERENCE_PACK_ROOT,
    selection_manifest: Path | str | None = None,
    title: str | None = None,
) -> dict[str, Any]:
    pack_dir = resolve_reference_pack(pack, pack_root=pack_root)
    pack_manifest, assets = load_reference_pack(pack_dir)
    output = Path(output_path).expanduser()
    ensure_dir(output.parent)
    selection = _load_selection_manifest(selection_manifest)
    selected = selection.get("selected", []) if selection else []
    selected_ids = {str(item.get("asset_id")) for item in selected if item.get("asset_id")}

    source_urls = sorted({
        str(asset.get("source_url"))
        for asset in assets
        if asset.get("source_url")
    })
    gallery_title = title or f"{pack_manifest.get('pack_id', 'Reference Pack')} preview"
    html_text = _render_reference_gallery_html(
        title=gallery_title,
        pack=pack_manifest,
        pack_dir=pack_dir,
        assets=assets,
        selection=selection,
        selected=selected,
        selected_ids=selected_ids,
        source_urls=source_urls,
        output_dir=output.parent,
    )
    output.write_text(html_text, encoding="utf-8")
    return {
        "output_path": str(output),
        "pack_id": pack_manifest.get("pack_id"),
        "asset_count": len(assets),
        "selected_count": len(selected),
        "source_url_count": len(source_urls),
    }


def select_visual_references(
    *,
    pack: str | Path,
    pack_root: Path | str = DEFAULT_REFERENCE_PACK_ROOT,
    project_dir: Path | str | None = None,
    query: str | None = None,
    categories: list[str] | None = None,
    count: int = 12,
    link_mode: str = "symlink",
    reference_dir: str | Path = DEFAULT_REFERENCE_DIR,
    local_only: bool = False,
) -> dict[str, Any]:
    pack_dir = resolve_reference_pack(pack, pack_root=pack_root)
    pack_manifest, assets = load_reference_pack(pack_dir)
    requested_count = max(1, min(48, int(count or 12)))
    normalized_categories = _normalize_categories(categories)
    normalized_link_mode = _normalize_link_mode(link_mode)
    query_terms = _tokenize(query or "")

    candidates = [
        _score_asset(asset, query_terms=query_terms, pack_dir=pack_dir)
        for asset in assets
        if _asset_matches_category(asset, normalized_categories)
    ]
    if local_only:
        candidates = [candidate for candidate in candidates if candidate.get("source_path")]

    selected = _select_diverse_assets(candidates, count=requested_count)
    project_path = Path(project_dir).resolve() if project_dir else None
    reference_root = _resolve_reference_root(project_path, reference_dir)
    materialized = _materialize_selected_assets(
        selected,
        pack=pack_manifest,
        pack_dir=pack_dir,
        reference_root=reference_root,
        project_dir=project_path,
        link_mode=normalized_link_mode,
    )

    return {
        "schema_version": SELECTION_SCHEMA_VERSION,
        "created_at": utc_now_iso(),
        "pack_id": pack_manifest.get("pack_id"),
        "pack_version": pack_manifest.get("version"),
        "pack_path": str(pack_dir),
        "query": query or "",
        "query_terms": query_terms,
        "categories": normalized_categories,
        "requested_count": requested_count,
        "selected_count": len(materialized),
        "available_candidate_count": len(assets),
        "scored_candidate_count": len(candidates),
        "selection_policy": {
            "link_mode": normalized_link_mode,
            "reference_dir": str(reference_dir),
            "local_only": local_only,
            "redistribution_allowed": False,
            "usage_scope": "reference-analysis-only",
        },
        "selected": materialized,
    }


def sync_reference_pack_sources(
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
        source for source in existing_sources
        if not _is_managed_reference_pack_source(source)
    ]
    merged_sources = list(preserved_sources)
    existing_keys = {
        _source_entry_identity(source, base_dir=base_dir)
        for source in merged_sources
    }

    for item in selection_manifest.get("selected", []) or []:
        source = _source_entry_from_selection(item, selection_manifest=selection_manifest, base_dir=base_dir)
        identity = _source_entry_identity(source, base_dir=base_dir)
        if identity in existing_keys:
            continue
        merged_sources.append(source)
        existing_keys.add(identity)

    visual_reference["sources"] = merged_sources
    visual_reference["reference_pack"] = {
        "pack_id": selection_manifest.get("pack_id"),
        "version": selection_manifest.get("pack_version"),
        "selected_count": selection_manifest.get("selected_count", 0),
    }
    return {
        "selected_count": int(selection_manifest.get("selected_count", 0) or 0),
        "managed_source_count": len(merged_sources) - len(preserved_sources),
        "total_source_count": len(merged_sources),
    }


def _load_selection_manifest(selection_manifest: Path | str | None) -> dict[str, Any] | None:
    if not selection_manifest:
        return None
    path = Path(selection_manifest).expanduser()
    if not path.exists():
        raise FileNotFoundError(f"selection manifest not found: {path}")
    return json.loads(path.read_text(encoding="utf-8"))


def _render_reference_gallery_html(
    *,
    title: str,
    pack: dict[str, Any],
    pack_dir: Path,
    assets: list[dict[str, Any]],
    selection: dict[str, Any] | None,
    selected: list[dict[str, Any]],
    selected_ids: set[str],
    source_urls: list[str],
    output_dir: Path,
) -> str:
    source_links = "\n".join(
        f'<li><a href="{_h(url)}" target="_blank" rel="noreferrer">{_h(url)}</a></li>'
        for url in source_urls
    ) or "<li>No source pages recorded.</li>"
    selected_cards = "\n".join(
        _gallery_card(item, output_dir=output_dir, pack_dir=pack_dir, selected=True)
        for item in selected
    )
    if not selected_cards:
        selected_cards = '<p class="empty-copy">No selection manifest supplied.</p>'
    asset_cards = "\n".join(
        _gallery_card(asset, output_dir=output_dir, pack_dir=pack_dir, selected=str(asset.get("asset_id")) in selected_ids)
        for asset in assets
    )
    selected_count = len(selected) if selection else 0
    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{_h(title)}</title>
  <style>
    :root {{
      color-scheme: light;
      --ink: #122033;
      --muted: #5d6979;
      --line: #d8e0ea;
      --surface: #ffffff;
      --soft: #f5f7fa;
      --accent: #0f5b7f;
      --accent-2: #28785f;
    }}
    * {{ box-sizing: border-box; }}
    body {{ margin: 0; font-family: Inter, ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif; background: var(--soft); color: var(--ink); }}
    header {{ padding: 32px 40px 24px; background: #0b2538; color: white; }}
    header h1 {{ margin: 0 0 10px; font-size: 30px; line-height: 1.2; letter-spacing: 0; }}
    header p {{ margin: 0; max-width: 920px; color: #c6d8e5; line-height: 1.7; }}
    main {{ padding: 24px 40px 48px; }}
    .stats {{ display: grid; grid-template-columns: repeat(4, minmax(160px, 1fr)); gap: 12px; margin-bottom: 18px; }}
    .stat {{ background: var(--surface); border: 1px solid var(--line); border-radius: 8px; padding: 16px; }}
    .stat strong {{ display: block; font-size: 24px; margin-bottom: 4px; overflow-wrap: anywhere; }}
    .stat span {{ color: var(--muted); font-size: 13px; }}
    section {{ margin-top: 24px; }}
    section > h2 {{ margin: 0 0 12px; font-size: 20px; letter-spacing: 0; }}
    .note {{ background: #eef6f3; border: 1px solid #c6ded4; border-radius: 8px; padding: 14px 16px; color: #214536; line-height: 1.6; }}
    .sources {{ background: var(--surface); border: 1px solid var(--line); border-radius: 8px; padding: 16px 18px; }}
    .sources ul {{ margin: 8px 0 0; padding-left: 20px; }}
    .grid {{ display: grid; grid-template-columns: repeat(auto-fill, minmax(260px, 1fr)); gap: 14px; }}
    .card {{ background: var(--surface); border: 1px solid var(--line); border-radius: 8px; overflow: hidden; min-width: 0; }}
    .card.selected {{ border-color: #95c7b5; box-shadow: inset 0 0 0 1px #95c7b5; }}
    .thumb {{ height: 176px; background: #e7edf4; display: flex; align-items: center; justify-content: center; overflow: hidden; }}
    .thumb img {{ width: 100%; height: 100%; object-fit: cover; display: block; }}
    .empty-copy {{ color: var(--muted); }}
    .empty-image {{ color: var(--muted); font-size: 13px; }}
    .meta {{ padding: 12px 14px 14px; }}
    .row {{ display: flex; justify-content: space-between; gap: 8px; align-items: center; color: var(--accent); font-size: 12px; }}
    .row span {{ color: var(--accent-2); }}
    h3 {{ margin: 8px 0 4px; font-size: 14px; line-height: 1.35; overflow-wrap: anywhere; letter-spacing: 0; }}
    .meta p {{ margin: 0 0 10px; color: var(--muted); font-size: 12px; }}
    .links {{ display: flex; gap: 10px; flex-wrap: wrap; }}
    a {{ color: #0c5c8a; text-decoration: none; font-weight: 650; }}
    a:hover {{ text-decoration: underline; }}
    @media (max-width: 760px) {{
      header, main {{ padding-left: 18px; padding-right: 18px; }}
      .stats {{ grid-template-columns: repeat(2, minmax(0, 1fr)); }}
      .thumb {{ height: 150px; }}
    }}
  </style>
</head>
<body>
  <header>
    <h1>{_h(title)}</h1>
    <p>Preview the visual references that entered this pack. Remote images remain reference-analysis-only unless you explicitly materialize licensed assets.</p>
  </header>
  <main>
    <div class="stats">
      <div class="stat"><strong>{_h(pack.get("asset_count", len(assets)))}</strong><span>assets in pack</span></div>
      <div class="stat"><strong>{_h(selected_count)}</strong><span>selected references</span></div>
      <div class="stat"><strong>{_h(pack.get("materialization"))}</strong><span>materialization</span></div>
      <div class="stat"><strong>{_h(pack.get("pack_id"))}</strong><span>pack id</span></div>
    </div>
    <div class="note">Use this gallery for review and curation. Do not redistribute remote search/gallery images as product assets unless license metadata permits it.</div>
    <section class="sources">
      <h2>Source Pages</h2>
      <ul>{source_links}</ul>
    </section>
    <section>
      <h2>Selected References</h2>
      <div class="grid">{selected_cards}</div>
    </section>
    <section>
      <h2>Pack Assets</h2>
      <div class="grid">{asset_cards}</div>
    </section>
  </main>
</body>
</html>
"""


def _gallery_card(item: dict[str, Any], *, output_dir: Path, pack_dir: Path, selected: bool) -> str:
    label = item.get("label") or item.get("asset_id") or "reference"
    image_url = _gallery_image_src(item, output_dir=output_dir, pack_dir=pack_dir)
    source_page = str(item.get("source_url") or "")
    direct_url = str(item.get("download_url") or image_url or "")
    rank = item.get("rank")
    badge = f"#{rank}" if rank else ("selected" if selected else "pack")
    score = item.get("score")
    score_html = f"<span>score {_h(score)}</span>" if score is not None else ""
    image_html = (
        f'<img src="{_h(image_url)}" alt="{_h(label)}" loading="lazy">'
        if image_url
        else '<div class="empty-image">no image url</div>'
    )
    source_link = (
        f'<a href="{_h(source_page)}" target="_blank" rel="noreferrer">source page</a>'
        if source_page
        else ""
    )
    image_link = (
        f'<a href="{_h(direct_url)}" target="_blank" rel="noreferrer">image url</a>'
        if direct_url
        else ""
    )
    selected_class = " selected" if selected else ""
    return f"""
      <article class="card{selected_class}">
        <div class="thumb">{image_html}</div>
        <div class="meta">
          <div class="row"><strong>{_h(badge)}</strong>{score_html}</div>
          <h3>{_h(label)}</h3>
          <p>{_h(item.get("category") or "reference")}</p>
          <div class="links">{image_link}{source_link}</div>
        </div>
      </article>
    """


def _gallery_image_src(item: dict[str, Any], *, output_dir: Path, pack_dir: Path) -> str | None:
    for key in ("selected_path", "local_path"):
        raw = item.get(key)
        if not raw:
            continue
        path = Path(str(raw)).expanduser()
        if not path.is_absolute():
            path = pack_dir / path if key == "local_path" else output_dir / path
        if path.exists():
            return _relative_or_absolute(path, output_dir)
    return _optional_str(item.get("download_url") or item.get("source_url") or item.get("url"))


def _h(value: Any) -> str:
    return html_lib.escape(str(value or ""), quote=True)


def _records_from_source_dir(
    *,
    source_dir: Path,
    pack_dir: Path,
    provider_id: str,
    category: str,
    tags: list[str],
    materialize: str,
    remaining: int,
) -> list[dict[str, Any]]:
    if remaining <= 0:
        return []
    if not source_dir.exists():
        raise FileNotFoundError(f"source directory not found: {source_dir}")
    image_paths = _discover_image_paths(source_dir)
    records: list[dict[str, Any]] = []
    for path in image_paths[:remaining]:
        local_path = _materialize_local_asset(
            source_path=path,
            pack_dir=pack_dir,
            provider_id=provider_id,
            materialize=materialize,
        )
        records.append(
            _asset_record(
                provider_id=provider_id,
                category=category,
                label=path.stem,
                tags=tags + _path_tags(path, source_dir),
                local_path=local_path,
                source_path=path,
                source_url=None,
                download_url=None,
                provenance_level="observed",
                metadata={"source_dir": str(source_dir)},
                pack_dir=pack_dir,
            )
        )
    return records


def _records_from_manifest(
    *,
    manifest_path: Path,
    pack_dir: Path,
    default_provider_id: str,
    default_category: str | None,
    default_tags: list[str],
    materialize: str,
    remaining: int,
) -> list[dict[str, Any]]:
    if remaining <= 0:
        return []
    raw_records = _read_manifest_records(manifest_path)
    records: list[dict[str, Any]] = []
    for raw in raw_records[:remaining]:
        if not isinstance(raw, dict):
            continue
        provider_id = str(raw.get("provider_id") or raw.get("provider") or default_provider_id)
        category = str(raw.get("category") or default_category or "manifest")
        label = str(raw.get("label") or raw.get("title") or raw.get("asset_id") or "reference")
        source_url = _optional_str(raw.get("source_url") or raw.get("url"))
        download_url = _optional_str(raw.get("download_url") or raw.get("image_url"))
        raw_path = _optional_str(raw.get("local_path") or raw.get("path"))
        source_path = _resolve_manifest_path(raw_path, manifest_path.parent) if raw_path else None
        if source_path and not source_path.exists():
            source_path = None
        local_path = None
        if source_path:
            local_path = _materialize_local_asset(
                source_path=source_path,
                pack_dir=pack_dir,
                provider_id=provider_id,
                materialize=materialize,
            )
        elif download_url and materialize == "download":
            local_path, source_path = _download_asset(
                url=download_url,
                pack_dir=pack_dir,
                provider_id=provider_id,
                fallback_name=label,
            )
        record = _asset_record(
            provider_id=provider_id,
            category=category,
            label=label,
            tags=default_tags + _normalize_tags(raw.get("tags")),
            local_path=local_path,
            source_path=source_path,
            source_url=source_url,
            download_url=download_url,
            provenance_level=str(raw.get("provenance_level") or ("observed" if source_path else "referenced")),
            metadata={k: v for k, v in raw.items() if k not in {"tags"}},
            pack_dir=pack_dir,
        )
        if raw.get("asset_id"):
            record["asset_id"] = str(raw["asset_id"])
        records.append(record)
    return records


def _records_from_source_urls(
    *,
    source_urls: list[str],
    pack_dir: Path,
    category: str,
    tags: list[str],
    materialize: str,
    crawl_depth: int,
    max_pages: int,
    remaining: int,
) -> list[dict[str, Any]]:
    if remaining <= 0:
        return []
    pages = _crawl_pages(source_urls, crawl_depth=max(0, crawl_depth), max_pages=max_pages)
    records: list[dict[str, Any]] = []
    for page_url, image_url in _iter_page_image_urls(pages):
        if len(records) >= remaining:
            break
        label = _label_from_url(image_url)
        source_path = None
        local_path = None
        if materialize == "download":
            try:
                local_path, source_path = _download_asset(
                    url=image_url,
                    pack_dir=pack_dir,
                    provider_id="web-crawl",
                    fallback_name=label,
                )
            except (httpx.HTTPError, OSError):
                local_path = None
                source_path = None
        records.append(
            _asset_record(
                provider_id="web-crawl",
                category=category,
                label=label,
                tags=tags + _path_tags(Path(urlparse(image_url).path), Path(".")),
                local_path=local_path,
                source_path=source_path,
                source_url=page_url,
                download_url=image_url,
                provenance_level="observed" if source_path else "referenced",
                metadata={"source_page": page_url},
                pack_dir=pack_dir,
            )
        )
    return records


def _asset_record(
    *,
    provider_id: str,
    category: str,
    label: str,
    tags: list[str],
    local_path: str | None,
    source_path: Path | None,
    source_url: str | None,
    download_url: str | None,
    provenance_level: str,
    metadata: dict[str, Any],
    pack_dir: Path,
) -> dict[str, Any]:
    width = height = None
    size = None
    sha256 = None
    mime_type = None
    if source_path and source_path.exists():
        size = source_path.stat().st_size
        sha256 = _sha256(source_path)
        mime_type = _mime_type(source_path)
    return {
        "asset_id": _asset_id(provider_id, label, source_url or download_url or local_path or str(source_path or "")),
        "provider_id": slugify(provider_id) or MANAGED_PROVIDER_ID,
        "category": slugify(category) or "reference",
        "label": label,
        "tags": _normalize_tags(tags),
        "source_url": source_url,
        "download_url": download_url,
        "local_path": local_path,
        "thumb_path": None,
        "width": width,
        "height": height,
        "bytes": size,
        "sha256": sha256,
        "mime_type": mime_type,
        "usage_scope": "reference-analysis-only",
        "redistribution_allowed": False,
        "provenance_level": provenance_level,
        "metadata": metadata,
        "source_path": _relative_or_absolute(source_path, pack_dir) if source_path else None,
    }


def _write_pack_files(*, pack_dir: Path, pack: dict[str, Any], records: list[dict[str, Any]]) -> None:
    ensure_dir(pack_dir)
    assets_path = pack_dir / "assets.jsonl"
    pack_path = pack_dir / "pack.json"
    index_path = pack_dir / "index.sqlite"

    pack_path.write_text(json.dumps(pack, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    assets_path.write_text(
        "\n".join(json.dumps(_asset_public_record(record), ensure_ascii=False) for record in records) + ("\n" if records else ""),
        encoding="utf-8",
    )
    _write_sqlite_index(index_path, records)
    checksums = _build_checksums(pack_dir, records)
    (pack_dir / "checksums.json").write_text(json.dumps(checksums, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def _write_sqlite_index(path: Path, records: list[dict[str, Any]]) -> None:
    with sqlite3.connect(path) as connection:
        connection.execute("drop table if exists assets")
        typed_columns = []
        for column in ASSET_COLUMNS:
            if column in {"width", "height", "bytes"}:
                typed_columns.append(f"{column} integer")
            elif column == "redistribution_allowed":
                typed_columns.append(f"{column} integer")
            else:
                typed_columns.append(f"{column} text")
        connection.execute(f"create table assets ({', '.join(typed_columns)})")
        placeholders = ",".join("?" for _ in ASSET_COLUMNS)
        for record in records:
            public = _asset_public_record(record)
            values = [
                json.dumps(public["tags"], ensure_ascii=False) if column == "tags"
                else json.dumps(public.get("metadata", {}), ensure_ascii=False) if column == "metadata_json"
                else int(bool(public.get(column))) if column == "redistribution_allowed"
                else public.get(column)
                for column in ASSET_COLUMNS
            ]
            connection.execute(
                f"insert into assets ({', '.join(ASSET_COLUMNS)}) values ({placeholders})",
                values,
            )


def _asset_public_record(record: dict[str, Any]) -> dict[str, Any]:
    public = {key: record.get(key) for key in ASSET_COLUMNS if key != "metadata_json"}
    public["tags"] = record.get("tags", [])
    public["metadata"] = record.get("metadata", {})
    public["source_path"] = record.get("source_path")
    return public


def _read_manifest_records(path: Path) -> list[Any]:
    text = path.read_text(encoding="utf-8")
    if path.suffix.lower() == ".jsonl":
        return [json.loads(line) for line in text.splitlines() if line.strip()]
    data = json.loads(text)
    if isinstance(data, list):
        return data
    if isinstance(data, dict):
        assets = data.get("assets") or data.get("records") or data.get("items")
        if isinstance(assets, list):
            return assets
    return []


def _crawl_pages(source_urls: list[str], *, crawl_depth: int, max_pages: int) -> dict[str, str]:
    queue = list(dict.fromkeys(source_urls))
    seen: set[str] = set()
    pages: dict[str, str] = {}
    origins = {_origin(url) for url in source_urls}
    with httpx.Client(timeout=10.0, follow_redirects=True) as client:
        depth_by_url = {url: 0 for url in queue}
        while queue and len(pages) < max_pages:
            url = queue.pop(0)
            if url in seen:
                continue
            seen.add(url)
            try:
                response = client.get(url)
                response.raise_for_status()
            except httpx.HTTPError:
                continue
            content_type = response.headers.get("content-type", "")
            if "html" not in content_type and "<html" not in response.text[:500].lower():
                continue
            pages[url] = response.text
            depth = depth_by_url.get(url, 0)
            if depth >= crawl_depth:
                continue
            for link in _extract_same_origin_links(response.text, url, origins):
                if link not in seen and link not in depth_by_url:
                    depth_by_url[link] = depth + 1
                    queue.append(link)
    return pages


def _iter_page_image_urls(pages: dict[str, str]) -> list[tuple[str, str]]:
    pairs: list[tuple[str, str]] = []
    seen: set[str] = set()
    for page_url, html in pages.items():
        soup = BeautifulSoup(html, "html.parser")
        candidates: list[str] = []
        for meta in soup.find_all("meta"):
            prop = str(meta.get("property") or meta.get("name") or "").lower()
            if prop in {"og:image", "twitter:image"} and meta.get("content"):
                candidates.append(str(meta["content"]))
        for image in soup.find_all("img"):
            raw = image.get("src") or image.get("data-src") or image.get("data-original")
            if not raw and image.get("srcset"):
                raw = str(image["srcset"]).split(",")[0].strip().split(" ")[0]
            if raw:
                candidates.append(str(raw))
        for raw in candidates:
            image_url = urljoin(page_url, raw)
            if image_url in seen:
                continue
            parsed = urlparse(image_url)
            if parsed.scheme not in {"http", "https"}:
                continue
            seen.add(image_url)
            pairs.append((page_url, image_url))
    return pairs


def _extract_same_origin_links(html: str, base_url: str, origins: set[str]) -> list[str]:
    soup = BeautifulSoup(html, "html.parser")
    links: list[str] = []
    for anchor in soup.find_all("a"):
        href = anchor.get("href")
        if not href:
            continue
        url = urljoin(base_url, str(href)).split("#", 1)[0]
        parsed = urlparse(url)
        if parsed.scheme in {"http", "https"} and _origin(url) in origins:
            links.append(url)
    return list(dict.fromkeys(links))


def _download_asset(*, url: str, pack_dir: Path, provider_id: str, fallback_name: str) -> tuple[str, Path]:
    assets_dir = ensure_dir(pack_dir / "assets" / slugify(provider_id))
    parsed = urlparse(url)
    suffix = Path(parsed.path).suffix.lower()
    if suffix not in IMAGE_EXTENSIONS:
        suffix = ".bin"
    file_name = f"{slugify(fallback_name)[:64] or 'asset'}__{hashlib.sha256(url.encode()).hexdigest()[:12]}{suffix}"
    target = assets_dir / file_name
    if not target.exists():
        with httpx.Client(timeout=20.0, follow_redirects=True) as client:
            response = client.get(url)
            response.raise_for_status()
            target.write_bytes(response.content)
    return _relative_or_absolute(target, pack_dir), target


def _materialize_local_asset(*, source_path: Path, pack_dir: Path, provider_id: str, materialize: str) -> str:
    source_path = source_path.expanduser().resolve()
    if materialize == "copy":
        target = _asset_target_path(source_path, pack_dir=pack_dir, provider_id=provider_id)
        if not target.exists():
            shutil.copy2(source_path, target)
        return _relative_or_absolute(target, pack_dir)
    if materialize == "symlink":
        target = _asset_target_path(source_path, pack_dir=pack_dir, provider_id=provider_id)
        if target.exists() or target.is_symlink():
            target.unlink()
        target.symlink_to(source_path)
        return _relative_or_absolute(target, pack_dir)
    return str(source_path)


def _asset_target_path(source_path: Path, *, pack_dir: Path, provider_id: str) -> Path:
    assets_dir = ensure_dir(pack_dir / "assets" / slugify(provider_id))
    digest = _sha256(source_path)[:12]
    return assets_dir / f"{slugify(source_path.stem)[:64] or 'asset'}__{digest}{source_path.suffix.lower()}"


def _score_asset(asset: dict[str, Any], *, query_terms: list[str], pack_dir: Path) -> dict[str, Any]:
    source_path = _resolve_asset_local_path(asset, pack_dir)
    fields = {
        "label": str(asset.get("label") or "").lower(),
        "tags": " ".join(_normalize_tags(asset.get("tags"))).lower(),
        "category": str(asset.get("category") or "").lower(),
        "provider": str(asset.get("provider_id") or "").lower(),
        "urls": " ".join(str(asset.get(key) or "") for key in ("source_url", "download_url")).lower(),
        "metadata": json.dumps(asset.get("metadata") or {}, ensure_ascii=False).lower(),
    }
    weights = {"label": 10, "tags": 8, "category": 5, "provider": 3, "urls": 2, "metadata": 2}
    score = 0
    matches: list[dict[str, Any]] = []
    for term in query_terms:
        for field, text in fields.items():
            if term in text:
                weight = weights[field]
                score += weight
                matches.append({"term": term, "field": field, "weight": weight})
    if source_path:
        score += 2
    result = dict(asset)
    result["source_path"] = str(source_path) if source_path else None
    result["score"] = score
    result["matched_terms"] = matches[:24]
    return result


def _select_diverse_assets(candidates: list[dict[str, Any]], *, count: int) -> list[dict[str, Any]]:
    sorted_candidates = sorted(
        candidates,
        key=lambda item: (
            -int(item.get("score") or 0),
            str(item.get("provider_id") or ""),
            str(item.get("category") or ""),
            str(item.get("asset_id") or ""),
        ),
    )
    selected: list[dict[str, Any]] = []
    seen: set[str] = set()
    provider_counts: dict[str, int] = {}
    max_per_provider = max(2, count // 2)

    for candidate in sorted_candidates:
        identity = str(candidate.get("sha256") or candidate.get("download_url") or candidate.get("source_url") or candidate.get("asset_id"))
        provider = str(candidate.get("provider_id") or MANAGED_PROVIDER_ID)
        if identity in seen:
            continue
        if provider_counts.get(provider, 0) >= max_per_provider and len(selected) < count - 1:
            continue
        selected.append(candidate)
        seen.add(identity)
        provider_counts[provider] = provider_counts.get(provider, 0) + 1
        if len(selected) >= count:
            break

    if len(selected) < count:
        for candidate in sorted_candidates:
            if len(selected) >= count:
                break
            identity = str(candidate.get("sha256") or candidate.get("download_url") or candidate.get("source_url") or candidate.get("asset_id"))
            if identity in seen:
                continue
            selected.append(candidate)
            seen.add(identity)

    return selected


def _materialize_selected_assets(
    selected: list[dict[str, Any]],
    *,
    pack: dict[str, Any],
    pack_dir: Path,
    reference_root: Path | None,
    project_dir: Path | None,
    link_mode: str,
) -> list[dict[str, Any]]:
    if link_mode != "absolute" and reference_root is not None:
        ensure_dir(reference_root)
    materialized: list[dict[str, Any]] = []
    for rank, asset in enumerate(selected, start=1):
        source_path = Path(str(asset["source_path"])) if asset.get("source_path") else None
        selected_path: Path | None = None
        if source_path and link_mode != "absolute" and reference_root is not None:
            selected_path = reference_root / _selected_file_name(rank, asset, source_path)
            _write_link_or_copy(source_path, selected_path, link_mode)
        elif source_path:
            selected_path = source_path
        entry = {
            "rank": rank,
            "asset_id": asset.get("asset_id"),
            "provider_id": asset.get("provider_id"),
            "category": asset.get("category"),
            "label": asset.get("label"),
            "tags": asset.get("tags", []),
            "source_url": asset.get("source_url"),
            "download_url": asset.get("download_url"),
            "source_path": str(source_path) if source_path else None,
            "selected_path": str(selected_path) if selected_path else None,
            "selected_relative_path": _relative_to_project(selected_path, project_dir) if selected_path else None,
            "materialization": link_mode if selected_path else "lazy-reference",
            "score": asset.get("score"),
            "matched_terms": asset.get("matched_terms", []),
            "usage_scope": asset.get("usage_scope") or "reference-analysis-only",
            "redistribution_allowed": bool(asset.get("redistribution_allowed")),
            "provenance_level": asset.get("provenance_level") or "referenced",
            "pack": {
                "pack_id": pack.get("pack_id"),
                "version": pack.get("version"),
            },
        }
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
    raise ValueError(f"Unsupported link mode: {link_mode}")


def _source_entry_from_selection(item: dict[str, Any], *, selection_manifest: dict[str, Any], base_dir: Path) -> dict[str, Any]:
    path = str(item.get("selected_relative_path") or item.get("selected_path") or "")
    source = {
        "kind": "image" if path else "external-reference",
        "provider_id": item.get("provider_id") or MANAGED_PROVIDER_ID,
        "label": item.get("label") or f"Reference pack asset {item.get('rank', '')}".strip(),
        "tags": _normalize_tags(["reference-pack", item.get("category"), *(item.get("tags") or [])]),
        "source_url": item.get("source_url"),
        "download_url": item.get("download_url"),
        "usage_scope": "reference-analysis-only",
        "redistribution_allowed": False,
        "reference_pack": {
            "pack_id": selection_manifest.get("pack_id"),
            "version": selection_manifest.get("pack_version"),
            "asset_id": item.get("asset_id"),
            "score": item.get("score"),
        },
    }
    if path:
        source["path"] = path
    else:
        source["url"] = item.get("download_url") or item.get("source_url")
    return source


def _is_managed_reference_pack_source(source: Any) -> bool:
    if not isinstance(source, dict):
        return False
    if source.get("reference_pack"):
        return True
    return str(source.get("provider_id") or "").strip().lower() == MANAGED_PROVIDER_ID


def _source_entry_identity(source: Any, *, base_dir: Path) -> str:
    if isinstance(source, str):
        raw = source
    elif isinstance(source, dict):
        raw = str(source.get("path") or source.get("download_url") or source.get("url") or source.get("source_url") or source.get("label") or "")
    else:
        raw = str(source)
    if raw.startswith(("http://", "https://")):
        return raw
    path = Path(raw)
    if not path.is_absolute():
        path = base_dir / path
    try:
        return str(path.resolve())
    except OSError:
        return str(path)


def _discover_image_paths(root: Path) -> list[Path]:
    if root.is_file():
        return [root] if root.suffix.lower() in IMAGE_EXTENSIONS else []
    return [
        path for path in sorted(root.rglob("*"))
        if path.is_file() and path.suffix.lower() in IMAGE_EXTENSIONS
    ]


def _normalize_materialize(value: str) -> str:
    normalized = str(value or "metadata").strip().lower()
    if normalized not in {"metadata", "copy", "symlink", "download"}:
        raise ValueError("materialize must be one of: metadata, copy, symlink, download")
    return normalized


def _normalize_link_mode(value: str) -> str:
    normalized = str(value or "symlink").strip().lower()
    if normalized not in {"symlink", "copy", "absolute"}:
        raise ValueError("link_mode must be one of: symlink, copy, absolute")
    return normalized


def _normalize_categories(categories: list[str] | None) -> list[str]:
    return [slugify(category) for category in categories or [] if slugify(category)]


def _asset_matches_category(asset: dict[str, Any], categories: list[str]) -> bool:
    if not categories:
        return True
    return slugify(str(asset.get("category") or "")) in categories


def _normalize_tags(values: object) -> list[str]:
    if values is None:
        return []
    if isinstance(values, str):
        raw_values = [part.strip() for part in values.split(",")]
    elif isinstance(values, list):
        raw_values = [str(value).strip() for value in values]
    else:
        raw_values = [str(values).strip()]
    return list(dict.fromkeys(slugify(value) for value in raw_values if slugify(value)))


def _path_tags(path: Path, root: Path) -> list[str]:
    try:
        parts = path.relative_to(root).parts
    except ValueError:
        parts = path.parts
    tags = []
    for part in parts:
        stem = Path(part).stem
        tags.extend(stem.replace("_", "-").split("-"))
    return _normalize_tags(tags)


def _tokenize(value: str) -> list[str]:
    tokens = [
        slug.replace("-", " ")
        for slug in (slugify(part) for part in value.split())
        if slug and len(slug) >= 2
    ]
    compact_tokens = [token.replace(" ", "-") for token in tokens]
    return list(dict.fromkeys(tokens + compact_tokens))


def _resolve_asset_local_path(asset: dict[str, Any], pack_dir: Path) -> Path | None:
    raw = str(asset.get("local_path") or "").strip()
    if not raw:
        return None
    path = Path(raw).expanduser()
    if not path.is_absolute():
        path = pack_dir / path
    return path.resolve() if path.exists() else None


def _resolve_manifest_path(raw_path: str, base_dir: Path) -> Path:
    path = Path(raw_path).expanduser()
    if not path.is_absolute():
        path = base_dir / path
    return path


def _resolve_reference_root(project_dir: Path | None, reference_dir: str | Path) -> Path | None:
    if project_dir is None:
        return None
    root = Path(reference_dir)
    if not root.is_absolute():
        root = project_dir / root
    return root.resolve()


def _selected_file_name(rank: int, asset: dict[str, Any], source_path: Path) -> str:
    label = slugify(str(asset.get("label") or "reference"))[:64]
    digest = str(asset.get("sha256") or _sha256(source_path))[0:12]
    return f"{rank:02d}-{label}__{digest}{source_path.suffix.lower()}"


def _relative_to_project(path: Path | None, project_dir: Path | None) -> str | None:
    if path is None:
        return None
    if project_dir is None:
        return str(path)
    return _relative_or_absolute(path, project_dir)


def _relative_or_absolute(path: Path | None, base_dir: Path) -> str | None:
    if path is None:
        return None
    candidate = path.expanduser()
    if not candidate.is_absolute():
        candidate = base_dir / candidate
    candidate = candidate.absolute()
    base = base_dir.expanduser().absolute()
    try:
        return str(candidate.relative_to(base))
    except ValueError:
        return str(candidate)


def _optional_str(value: Any) -> str | None:
    if value is None:
        return None
    text = str(value).strip()
    return text or None


def _asset_id(provider_id: str, label: str, identity: str) -> str:
    digest = hashlib.sha256(identity.encode("utf-8")).hexdigest()[:12]
    return f"{slugify(provider_id) or 'provider'}:{slugify(label)[:48] or 'asset'}:{digest}"


def _label_from_url(url: str) -> str:
    path = Path(urlparse(url).path)
    return path.stem or urlparse(url).netloc or "web-image"


def _origin(url: str) -> str:
    parsed = urlparse(url)
    return f"{parsed.scheme}://{parsed.netloc}"


def _mime_type(path: Path) -> str | None:
    suffix = path.suffix.lower()
    if suffix == ".png":
        return "image/png"
    if suffix in {".jpg", ".jpeg"}:
        return "image/jpeg"
    if suffix == ".webp":
        return "image/webp"
    if suffix == ".svg":
        return "image/svg+xml"
    if suffix == ".gif":
        return "image/gif"
    if suffix == ".bmp":
        return "image/bmp"
    return None


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(65536), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _build_checksums(pack_dir: Path, records: list[dict[str, Any]]) -> dict[str, Any]:
    files = {}
    for relative in ("pack.json", "assets.jsonl", "index.sqlite"):
        path = pack_dir / relative
        if path.exists():
            files[relative] = _sha256(path)
    for record in records:
        local_path = record.get("local_path")
        if not local_path:
            continue
        path = Path(str(local_path))
        if not path.is_absolute():
            path = pack_dir / path
        if path.exists() and path.is_file():
            files[_relative_or_absolute(path, pack_dir) or str(path)] = _sha256(path)
    return {"schema_version": "reference-pack-checksums/v1", "files": files}


def _dedupe_assets(records: list[dict[str, Any]]) -> list[dict[str, Any]]:
    deduped: list[dict[str, Any]] = []
    seen: set[str] = set()
    for record in records:
        identity = str(record.get("sha256") or record.get("download_url") or record.get("source_url") or record.get("local_path") or record.get("asset_id"))
        if identity in seen:
            continue
        seen.add(identity)
        deduped.append(record)
    return deduped
