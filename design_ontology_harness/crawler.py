from __future__ import annotations

import concurrent.futures
import re
from collections import deque
from dataclasses import dataclass, field
from pathlib import Path
from typing import Iterable
from urllib.parse import urljoin, urlparse
from urllib.robotparser import RobotFileParser

import httpx
from bs4 import BeautifulSoup

from .models import CrawlManifest, DocumentRecord, ReferenceLink, utc_now_iso
from .utils import clean_text, ensure_dir, normalize_url, slugify, write_json, write_jsonl

DISALLOWED_SCHEMES = ("mailto:", "javascript:", "tel:", "sms:")
DISALLOWED_EXTENSIONS = (
    ".png",
    ".jpg",
    ".jpeg",
    ".gif",
    ".svg",
    ".webp",
    ".pdf",
    ".zip",
    ".mp4",
    ".mp3",
)
DISALLOWED_PATH_PARTS = (
    "/login",
    "/signin",
    "/signup",
    "/search",
    "/share",
    "/account",
    "/privacy",
    "/terms",
)


MOBILE_UA = (
    "Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) "
    "AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1"
)
JINA_READER_PREFIX = "https://r.jina.ai/"
CSS_PARALLEL_WORKERS = 8


@dataclass(slots=True)
class FetchResult:
    html: str
    status_code: int
    final_url: str
    tier: str
    css_urls: list[str] = field(default_factory=list)
    css_contents: dict[str, str] = field(default_factory=dict)


@dataclass(slots=True)
class CrawlConfig:
    output_dir: Path
    max_pages_per_source: int = 3
    max_depth: int = 1
    user_agent: str = "DesignOntologyHarness/0.1 (+https://spacebar310.tistory.com/86)"
    enable_fallback: bool = True
    enable_css_download: bool = True


class RobotsCache:
    def __init__(self, client: httpx.Client) -> None:
        self.client = client
        self._cache: dict[str, RobotFileParser] = {}

    def allowed(self, url: str, user_agent: str) -> bool:
        split = urlparse(url)
        key = f"{split.scheme}://{split.netloc}"
        parser = self._cache.get(key)
        if parser is None:
            parser = RobotFileParser()
            parser.set_url(f"{key}/robots.txt")
            try:
                response = self.client.get(parser.url, timeout=15.0, follow_redirects=True)
                if response.status_code >= 400:
                    parser.parse([])
                else:
                    parser.parse(response.text.splitlines())
            except httpx.HTTPError:
                parser.parse([])
            self._cache[key] = parser
        return parser.can_fetch(user_agent, url)


def _fetch_with_fallback(
    client: httpx.Client,
    url: str,
    config: CrawlConfig,
) -> FetchResult:
    """5-tier fallback: httpx 기본 → Mobile UA → Jina Reader → Playwright → 중단."""
    tiers = [
        ("default", {}),
        ("mobile_ua", {"headers": {"User-Agent": MOBILE_UA}}),
    ]
    if not config.enable_fallback:
        tiers = tiers[:1]

    for tier_name, extra_kwargs in tiers:
        try:
            response = client.get(url, timeout=30.0, follow_redirects=True, **extra_kwargs)
            content_type = response.headers.get("content-type", "")
            if "text/html" not in content_type:
                continue
            if response.status_code >= 400:
                continue
            text = response.text
            if len(text.strip()) < 200:
                continue
            return FetchResult(
                html=text,
                status_code=response.status_code,
                final_url=str(response.url),
                tier=tier_name,
            )
        except httpx.HTTPError:
            continue

    if config.enable_fallback:
        try:
            jina_url = JINA_READER_PREFIX + url
            response = client.get(
                jina_url,
                timeout=45.0,
                follow_redirects=True,
                headers={"Accept": "text/html"},
            )
            if response.status_code < 400 and len(response.text.strip()) >= 100:
                return FetchResult(
                    html=response.text,
                    status_code=response.status_code,
                    final_url=url,
                    tier="jina_reader",
                )
        except httpx.HTTPError:
            pass

        try:
            result = _fetch_with_playwright(url)
            if result:
                return result
        except Exception:
            pass

    raise RuntimeError(f"All fetch tiers exhausted for {url}")


def _fetch_with_playwright(url: str) -> FetchResult | None:
    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        return None

    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()
            response = page.goto(url, wait_until="domcontentloaded", timeout=30000)
            status = response.status if response else 0
            html = page.content()
            final_url = page.url
            browser.close()
            if status >= 400 or len(html.strip()) < 200:
                return None
            return FetchResult(
                html=html,
                status_code=status,
                final_url=final_url,
                tier="playwright",
            )
    except Exception:
        return None


def _extract_css_links(html: str, base_url: str) -> list[str]:
    soup = BeautifulSoup(html, "html.parser")
    urls: list[str] = []
    seen: set[str] = set()
    for link in soup.find_all("link", rel=lambda v: v and "stylesheet" in v):
        href = link.get("href", "").strip()
        if not href:
            continue
        absolute = urljoin(base_url, href)
        if absolute not in seen:
            seen.add(absolute)
            urls.append(absolute)
    return urls


def _download_css_parallel(
    client: httpx.Client,
    css_urls: list[str],
    max_workers: int = CSS_PARALLEL_WORKERS,
) -> dict[str, str]:
    results: dict[str, str] = {}
    if not css_urls:
        return results

    def fetch_one(url: str) -> tuple[str, str]:
        try:
            response = client.get(url, timeout=20.0, follow_redirects=True)
            if response.status_code < 400:
                return url, response.text
        except httpx.HTTPError:
            pass
        return url, ""

    with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = {executor.submit(fetch_one, url): url for url in css_urls}
        for future in concurrent.futures.as_completed(futures):
            url, content = future.result()
            if content:
                results[url] = content
    return results


def crawl_reference(
    client: httpx.Client,
    robots: RobotsCache,
    reference: ReferenceLink,
    config: CrawlConfig,
) -> tuple[list[DocumentRecord], CrawlManifest]:
    slug = slugify(f"{reference.order}-{reference.curated_title}-{urlparse(reference.href).netloc}")
    crawl_dir = ensure_dir(config.output_dir / "crawls" / slug)
    queue: deque[tuple[str, int]] = deque([(reference.href, 0)])
    visited: set[str] = set()
    documents: list[DocumentRecord] = []
    errors: list[dict[str, str]] = []
    started_at = utc_now_iso()

    allowed_hosts: set[str] = set()

    while queue and len(documents) < config.max_pages_per_source:
        current_url, depth = queue.popleft()
        normalized = normalize_url(current_url)
        if normalized in visited:
            continue
        visited.add(normalized)

        if not robots.allowed(current_url, config.user_agent):
            errors.append({"url": current_url, "error": "Blocked by robots.txt"})
            documents.append(
                DocumentRecord(
                    reference_slug=slug,
                    source_label=reference.curated_title,
                    url=current_url,
                    final_url=current_url,
                    depth=depth,
                    status_code=None,
                    title="",
                    description="",
                    headings=[],
                    text="",
                    internal_links=[],
                    fetched_at=utc_now_iso(),
                    error="Blocked by robots.txt",
                )
            )
            continue

        try:
            fetch = _fetch_with_fallback(client, current_url, config)
            status_code = fetch.status_code
            final_url = fetch.final_url
            final_host = urlparse(final_url).netloc.lower()
            source_host = urlparse(reference.href).netloc.lower()
            allowed_hosts.update({source_host, final_host})

            if config.enable_css_download and depth == 0:
                css_urls = _extract_css_links(fetch.html, final_url)
                fetch.css_urls = css_urls
                fetch.css_contents = _download_css_parallel(client, css_urls)
                if fetch.css_contents:
                    css_dir = ensure_dir(crawl_dir / "css")
                    for i, (css_url, css_text) in enumerate(fetch.css_contents.items()):
                        css_filename = f"{i:03d}_{urlparse(css_url).path.split('/')[-1] or 'style.css'}"
                        if not css_filename.endswith(".css"):
                            css_filename += ".css"
                        (css_dir / css_filename).write_text(css_text, encoding="utf-8")

            document = _parse_document(
                html=fetch.html,
                request_url=current_url,
                final_url=final_url,
                source_label=reference.curated_title,
                slug=slug,
                depth=depth,
                status_code=status_code,
                fetch_tier=fetch.tier,
                css_count=len(fetch.css_contents),
            )
            documents.append(document)
            if depth < config.max_depth:
                for link in document.internal_links:
                    if _should_follow(link, allowed_hosts):
                        queue.append((link, depth + 1))
        except Exception as exc:
            errors.append({"url": current_url, "error": str(exc)})
            documents.append(
                DocumentRecord(
                    reference_slug=slug,
                    source_label=reference.curated_title,
                    url=current_url,
                    final_url=current_url,
                    depth=depth,
                    status_code=None,
                    title="",
                    description="",
                    headings=[],
                    text="",
                    internal_links=[],
                    fetched_at=utc_now_iso(),
                    error=str(exc),
                )
            )

    manifest = CrawlManifest(
        reference_slug=slug,
        source_label=reference.curated_title,
        seed_url=reference.href,
        started_at=started_at,
        finished_at=utc_now_iso(),
        fetched_count=len(documents),
        ok_count=sum(1 for document in documents if not document.error),
        error_count=sum(1 for document in documents if document.error),
        errors=errors,
    )

    write_json(crawl_dir / "manifest.json", manifest.to_dict())
    write_jsonl(crawl_dir / "documents.jsonl", [document.to_dict() for document in documents])
    return documents, manifest


def _parse_document(
    html: str,
    request_url: str,
    final_url: str,
    source_label: str,
    slug: str,
    depth: int,
    status_code: int,
    fetch_tier: str = "default",
    css_count: int = 0,
) -> DocumentRecord:
    soup = BeautifulSoup(html, "html.parser")
    for selector in ("script", "style", "noscript", "svg", "canvas", "footer", "nav", "aside", "form"):
        for node in soup.select(selector):
            node.decompose()

    title = (
        _meta_content(soup, "property", "og:title")
        or _meta_content(soup, "name", "title")
        or clean_text(soup.title.get_text(" ", strip=True) if soup.title else "")
    )
    description = _meta_content(soup, "name", "description") or _meta_content(
        soup, "property", "og:description"
    )

    container = (
        soup.select_one("main")
        or soup.select_one("article")
        or soup.select_one('[role="main"]')
        or soup.body
        or soup
    )
    headings = [
        clean_text(node.get_text(" ", strip=True))
        for node in container.select("h1, h2, h3")
        if clean_text(node.get_text(" ", strip=True))
    ][:40]
    text = _extract_text(container)
    internal_links = _extract_internal_links(container, final_url)

    return DocumentRecord(
        reference_slug=slug,
        source_label=source_label,
        url=request_url,
        final_url=final_url,
        depth=depth,
        status_code=status_code,
        title=title or "",
        description=description or "",
        headings=headings,
        text=text,
        internal_links=internal_links,
        fetched_at=utc_now_iso(),
        fetch_tier=fetch_tier,
        css_count=css_count,
    )


def _extract_text(container: BeautifulSoup) -> str:
    lines: list[str] = []
    for node in container.select("h1, h2, h3, h4, h5, h6, p, li, td, th, blockquote"):
        text = clean_text(node.get_text(" ", strip=True))
        if text and len(text) > 1:
            lines.append(text)
    deduped: list[str] = []
    seen: set[str] = set()
    for line in lines:
        if line in seen:
            continue
        seen.add(line)
        deduped.append(line)
    return "\n".join(deduped[:300])


def _extract_internal_links(container: BeautifulSoup, base_url: str) -> list[str]:
    links: list[str] = []
    seen: set[str] = set()
    for anchor in container.select("a[href]"):
        href = anchor.get("href", "").strip()
        if not href or href.startswith(DISALLOWED_SCHEMES):
            continue
        absolute = normalize_url(urljoin(base_url, href))
        if absolute in seen:
            continue
        seen.add(absolute)
        links.append(absolute)
    return links


def _should_follow(url: str, allowed_hosts: set[str]) -> bool:
    split = urlparse(url)
    if split.scheme not in {"http", "https"}:
        return False
    if allowed_hosts and split.netloc.lower() not in allowed_hosts:
        return False
    lowered = split.path.lower()
    if any(lowered.endswith(ext) for ext in DISALLOWED_EXTENSIONS):
        return False
    if any(part in lowered for part in DISALLOWED_PATH_PARTS):
        return False
    if re.search(r"/(cdn-cgi|_next|assets|static|images|media)/", lowered):
        return False
    return True


def _meta_content(soup: BeautifulSoup, attr_name: str, attr_value: str) -> str | None:
    tag = soup.find("meta", attrs={attr_name: attr_value})
    content = tag.get("content") if tag else None
    return clean_text(content) if content else None
