from __future__ import annotations

import re
from collections import deque
from dataclasses import dataclass
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


@dataclass(slots=True)
class CrawlConfig:
    output_dir: Path
    max_pages_per_source: int = 3
    max_depth: int = 1
    user_agent: str = "DesignOntologyHarness/0.1 (+https://spacebar310.tistory.com/86)"


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
            response = client.get(current_url, timeout=30.0, follow_redirects=True)
            status_code = response.status_code
            final_url = str(response.url)
            final_host = urlparse(final_url).netloc.lower()
            source_host = urlparse(reference.href).netloc.lower()
            allowed_hosts.update({source_host, final_host})
            content_type = response.headers.get("content-type", "")
            if "text/html" not in content_type:
                raise ValueError(f"Unsupported content type: {content_type}")
            document = _parse_document(
                html=response.text,
                request_url=current_url,
                final_url=final_url,
                source_label=reference.curated_title,
                slug=slug,
                depth=depth,
                status_code=status_code,
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
