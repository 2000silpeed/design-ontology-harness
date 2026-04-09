from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Iterable
from urllib.parse import urlsplit, urlunsplit


def ensure_dir(path: Path) -> Path:
    path.mkdir(parents=True, exist_ok=True)
    return path


def write_json(path: Path, payload: object) -> None:
    path.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )


def write_jsonl(path: Path, rows: Iterable[dict]) -> None:
    with path.open("w", encoding="utf-8") as handle:
        for row in rows:
            handle.write(json.dumps(row, ensure_ascii=False) + "\n")


def slugify(value: str) -> str:
    slug = re.sub(r"[^a-zA-Z0-9]+", "-", value).strip("-").lower()
    return slug or "source"


def normalize_url(url: str) -> str:
    split = urlsplit(url)
    path = split.path or "/"
    normalized = urlunsplit(
        (split.scheme.lower(), split.netloc.lower(), path, split.query, "")
    )
    if normalized.endswith("/") and path != "/":
        normalized = normalized.rstrip("/")
    return normalized


def clean_text(value: str) -> str:
    return re.sub(r"\s+", " ", value).strip()


def guess_file_safe_name(value: str) -> str:
    safe = re.sub(r"[^a-zA-Z0-9._-]+", "_", value).strip("_")
    return safe or "document"
