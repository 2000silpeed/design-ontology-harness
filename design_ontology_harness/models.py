from __future__ import annotations

from dataclasses import asdict, dataclass, field
from datetime import datetime
from typing import Any


@dataclass(slots=True)
class SeedArticle:
    url: str
    title: str
    category: str
    published_at: str | None
    extracted_at: str
    seed_kind: str = "curated-article"
    references: list["ReferenceLink"] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        data = asdict(self)
        data["references"] = [reference.to_dict() for reference in self.references]
        return data


@dataclass(slots=True)
class ReferenceLink:
    order: int
    curated_title: str
    href: str
    anchor_text: str
    source_article_url: str
    source_article_title: str

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(slots=True)
class DocumentRecord:
    reference_slug: str
    source_label: str
    url: str
    final_url: str
    depth: int
    status_code: int | None
    title: str
    description: str
    headings: list[str]
    text: str
    internal_links: list[str]
    fetched_at: str
    error: str | None = None
    fetch_tier: str = "default"
    css_count: int = 0

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(slots=True)
class CrawlManifest:
    reference_slug: str
    source_label: str
    seed_url: str
    started_at: str
    finished_at: str
    fetched_count: int
    ok_count: int
    error_count: int
    errors: list[dict[str, str]]

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def utc_now_iso() -> str:
    return datetime.utcnow().replace(microsecond=0).isoformat() + "Z"
