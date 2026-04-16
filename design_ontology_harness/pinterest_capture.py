from __future__ import annotations

from pathlib import Path
from urllib.parse import quote

from playwright.sync_api import Locator, Page, sync_playwright

from .pinterest_assist import _normalize_pinterest_assist_config, _normalize_query_entries, _resolve_capture_root
from .utils import ensure_dir

MIN_TILE_WIDTH = 120
MIN_TILE_HEIGHT = 120


def capture_pinterest_candidates(
    brand_profile: dict,
    query_report: dict,
    project_dir: Path | None,
    *,
    limit_queries: int | None = None,
    max_candidates_per_query: int | None = None,
    headless: bool = True,
    timeout_ms: int = 90_000,
    initial_wait_ms: int = 7_000,
    scroll_rounds: int = 2,
    scroll_wait_ms: int = 1_500,
) -> dict:
    visual_reference = brand_profile.get("visual_reference") or {}
    config = _normalize_pinterest_assist_config(visual_reference)
    query_entries = _normalize_query_entries(query_report)
    if limit_queries is not None:
        query_entries = query_entries[: max(1, int(limit_queries))]

    capture_root = _resolve_capture_root(project_dir, config["capture_dir"])
    if capture_root is None:
        raise ValueError("Pinterest capture requires a valid capture directory.")
    ensure_dir(capture_root)

    candidate_limit = max_candidates_per_query or config["max_candidates_per_query"]
    query_results: list[dict] = []

    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(headless=headless)
        context = browser.new_context(
            viewport={"width": 1440, "height": 2200},
            device_scale_factor=1,
            locale="en-US",
        )
        page = context.new_page()

        for query_entry in query_entries:
            query_results.append(
                _capture_query_candidates(
                    page=page,
                    capture_root=capture_root,
                    project_dir=project_dir,
                    query_entry=query_entry,
                    candidate_limit=max(1, int(candidate_limit)),
                    timeout_ms=timeout_ms,
                    initial_wait_ms=initial_wait_ms,
                    scroll_rounds=scroll_rounds,
                    scroll_wait_ms=scroll_wait_ms,
                )
            )

        browser.close()

    return {
        "capture_mode": "playwright-capture",
        "capture_root": (
            str(capture_root.relative_to(project_dir.resolve()))
            if project_dir and capture_root.is_absolute()
            else str(capture_root)
        ),
        "query_count": len(query_results),
        "captured_count": sum(len(item["captured_candidates"]) for item in query_results),
        "queries": query_results,
    }


def _capture_query_candidates(
    page: Page,
    capture_root: Path,
    project_dir: Path | None,
    query_entry: dict,
    *,
    candidate_limit: int,
    timeout_ms: int,
    initial_wait_ms: int,
    scroll_rounds: int,
    scroll_wait_ms: int,
) -> dict:
    search_url = _build_pinterest_search_url(query_entry["query"])
    query_dir = ensure_dir(capture_root / query_entry["query_slug"])
    warnings: list[str] = []
    captured_candidates: list[dict] = []
    seen_pin_urls: set[str] = set()

    page.goto(search_url, wait_until="domcontentloaded", timeout=timeout_ms)
    page.wait_for_timeout(initial_wait_ms)

    for _ in range(max(0, scroll_rounds) + 1):
        anchors = page.locator('a[href*="/pin/"]')
        total = anchors.count()
        for index in range(total):
            if len(captured_candidates) >= candidate_limit:
                break
            locator = anchors.nth(index)
            candidate = _capture_single_candidate(
                page=page,
                locator=locator,
                query_dir=query_dir,
                query_id=query_entry["query_id"],
                slot=len(captured_candidates) + 1,
                project_dir=project_dir,
                search_url=search_url,
                seen_pin_urls=seen_pin_urls,
            )
            if candidate:
                captured_candidates.append(candidate)
        if len(captured_candidates) >= candidate_limit:
            break
        page.mouse.wheel(0, 1800)
        page.wait_for_timeout(scroll_wait_ms)

    if not captured_candidates:
        warnings.append("No visible pin tiles were captured from the Pinterest search results page.")

    return {
        "query_id": query_entry["query_id"],
        "query": query_entry["query"],
        "query_slug": query_entry["query_slug"],
        "search_url": search_url,
        "capture_dir": _relative_path(query_dir, project_dir),
        "captured_candidates": captured_candidates,
        "warnings": warnings,
    }


def _capture_single_candidate(
    page: Page,
    locator: Locator,
    query_dir: Path,
    query_id: str,
    slot: int,
    project_dir: Path | None,
    search_url: str,
    seen_pin_urls: set[str],
) -> dict | None:
    href = locator.get_attribute("href")
    if not href:
        return None

    pin_url = _normalize_pin_url(href)
    if pin_url in seen_pin_urls:
        return None

    box = locator.bounding_box()
    if not box or box["width"] < MIN_TILE_WIDTH or box["height"] < MIN_TILE_HEIGHT:
        return None

    seen_pin_urls.add(pin_url)
    locator.scroll_into_view_if_needed(timeout=5_000)
    page.wait_for_timeout(250)

    aria_label = _clean_text(locator.get_attribute("aria-label"))
    image_locator = locator.locator("img").first
    image_url = None
    image_alt = None
    if image_locator.count():
        image_url = image_locator.evaluate("img => img.currentSrc || img.src || null")
        image_alt = _clean_text(image_locator.get_attribute("alt"))

    candidate_id = f"{query_id}-c{slot:02d}"
    capture_path = query_dir / f"{candidate_id}.png"
    locator.screenshot(path=str(capture_path))

    label = aria_label or image_alt or f"Pinterest result {slot}"
    return {
        "candidate_id": candidate_id,
        "status": "captured",
        "source_type": "pin",
        "platform": "pinterest",
        "board_url": None,
        "pin_url": pin_url,
        "reference_url": pin_url,
        "search_url": search_url,
        "capture_path": _relative_path(capture_path, project_dir),
        "thumbnail_path": _relative_path(capture_path, project_dir),
        "capture_method": "playwright-screenshot",
        "usage_scope": "reference-analysis-only",
        "redistribution_allowed": False,
        "access_notes": "Captured from visible Pinterest search results without bypassing auth or access controls.",
        "notes": label,
        "selected": False,
        "preview_url": image_url,
        "alt_text": image_alt,
        "tile_box": {
            "x": round(box["x"], 2),
            "y": round(box["y"], 2),
            "width": round(box["width"], 2),
            "height": round(box["height"], 2),
        },
    }


def _build_pinterest_search_url(query: str) -> str:
    return f"https://www.pinterest.com/search/pins/?q={quote(query)}"


def _normalize_pin_url(href: str) -> str:
    value = str(href).strip()
    if value.startswith("http://") or value.startswith("https://"):
        return value
    if not value.startswith("/"):
        value = "/" + value
    return "https://www.pinterest.com" + value


def _clean_text(value: str | None) -> str | None:
    if not value:
        return None
    cleaned = " ".join(value.split()).strip()
    return cleaned or None


def _relative_path(path: Path, project_dir: Path | None) -> str:
    if project_dir:
        try:
            return str(path.resolve().relative_to(project_dir.resolve()))
        except ValueError:
            return str(path.resolve())
    return str(path.resolve())
