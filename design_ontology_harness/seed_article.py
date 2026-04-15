from __future__ import annotations

import re
from typing import Iterable
from urllib.parse import urlparse

from bs4 import BeautifulSoup

from .models import ReferenceLink, SeedArticle, utc_now_iso
from .utils import clean_text


def fetch_seed_article(client: httpx.Client, url: str) -> SeedArticle:
    response = client.get(url, timeout=30.0, follow_redirects=True)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, "html.parser")
    final_url = str(response.url)
    title = (
        _meta_content(soup, "property", "og:title")
        or _meta_content(soup, "name", "title")
        or clean_text(soup.title.get_text(" ", strip=True) if soup.title else "")
    )
    category = clean_text(
        soup.select_one("span.category").get_text(" ", strip=True)
        if soup.select_one("span.category")
        else ""
    )
    published_at = _meta_content(soup, "property", "article:published_time")
    content_root = soup.select_one(".entry-content .contents_style")
    if content_root is not None:
        references = list(_extract_reference_links(content_root, final_url, title or ""))
        if references:
            return SeedArticle(
                url=final_url,
                title=title or "",
                category=category,
                published_at=published_at,
                extracted_at=utc_now_iso(),
                seed_kind="curated-article",
                references=references,
            )

    return _build_direct_reference_seed(
        url=final_url,
        title=title,
        category=category,
        published_at=published_at,
    )


def _extract_reference_links(
    content_root: BeautifulSoup,
    article_url: str,
    article_title: str,
) -> Iterable[ReferenceLink]:
    order = 0
    seen: set[str] = set()
    for heading in content_root.select("h1, h2, h3, h4, h5, h6"):
        link = heading.find("a", href=True)
        if link is None:
            continue
        href = link["href"].strip()
        if not href.startswith("http"):
            continue
        if href in seen:
            continue
        seen.add(href)
        order += 1
        curated_title = clean_text(heading.get_text(" ", strip=True))
        curated_title = re.sub(r"\(\s*Click(?:\s+Figma)?\s*\)", "", curated_title, flags=re.I)
        curated_title = clean_text(curated_title)
        yield ReferenceLink(
            order=order,
            curated_title=curated_title,
            href=href,
            anchor_text=clean_text(link.get_text(" ", strip=True)),
            source_article_url=article_url,
            source_article_title=article_title,
        )


def _meta_content(soup: BeautifulSoup, attr_name: str, attr_value: str) -> str | None:
    tag = soup.find("meta", attrs={attr_name: attr_value})
    content = tag.get("content") if tag else None
    return clean_text(content) if content else None


def _build_direct_reference_seed(
    url: str,
    title: str | None,
    category: str,
    published_at: str | None,
) -> SeedArticle:
    parsed = urlparse(url)
    fallback_title = _label_from_url(url)
    reference_title = clean_text(title or fallback_title)
    return SeedArticle(
        url=url,
        title=reference_title,
        category=category or "direct-reference",
        published_at=published_at,
        extracted_at=utc_now_iso(),
        seed_kind="direct-reference",
        references=[
            ReferenceLink(
                order=1,
                curated_title=reference_title,
                href=url,
                anchor_text=reference_title,
                source_article_url=url,
                source_article_title=reference_title,
            )
        ],
    )


def _label_from_url(url: str) -> str:
    parsed = urlparse(url)
    host = parsed.netloc.replace("www.", "")
    path = parsed.path.strip("/")
    if not path:
        return host
    last_segment = path.split("/")[-1].replace("-", " ")
    return clean_text(f"{host} {last_segment}")
