"""Preset matcher — natural-language → axes/tags mapping + coarse-bucket scoring.

Engine (Phase 11-2) uses the keywords dictionary in `keywords.json`.
This package is intentionally thin: data lives in JSON, logic in `engine.py`.
"""

from __future__ import annotations

import json
from pathlib import Path

_KEYWORDS_PATH = Path(__file__).parent / "keywords.json"


def load_keywords() -> dict:
    return json.loads(_KEYWORDS_PATH.read_text(encoding="utf-8"))


__all__ = ["load_keywords"]
