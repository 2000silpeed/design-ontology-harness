"""Minimal semver range parser — dependency-free.

Supports the subset we use in preset_api_version ranges:
- exact:        "1.0.0"
- comparators:  ">=1.0.0", ">1.0.0", "<=1.0.0", "<1.0.0", "==1.0.0"
- conjunction:  ">=1.0.0 <2.0.0"   (space-separated = AND)

Does NOT support: pre-release tags, ||, caret/tilde, x-ranges. Add when needed.
"""

from __future__ import annotations

import re
from dataclasses import dataclass

_VERSION_RE = re.compile(r"^(\d+)\.(\d+)\.(\d+)$")
_COMP_RE = re.compile(r"^(>=|<=|==|>|<|=)?\s*(\d+\.\d+\.\d+)$")


def _parse_version(text: str) -> tuple[int, int, int]:
    match = _VERSION_RE.match(text.strip())
    if not match:
        raise ValueError(f"Invalid semver: {text}")
    return int(match.group(1)), int(match.group(2)), int(match.group(3))


@dataclass(frozen=True)
class _Comparator:
    op: str
    version: tuple[int, int, int]

    def matches(self, v: tuple[int, int, int]) -> bool:
        if self.op in ("=", "=="):
            return v == self.version
        if self.op == ">=":
            return v >= self.version
        if self.op == ">":
            return v > self.version
        if self.op == "<=":
            return v <= self.version
        if self.op == "<":
            return v < self.version
        raise ValueError(f"Unknown operator: {self.op}")


def _parse_comparator(text: str) -> _Comparator:
    match = _COMP_RE.match(text.strip())
    if not match:
        raise ValueError(f"Invalid comparator: {text}")
    op = match.group(1) or "="
    return _Comparator(op=op, version=_parse_version(match.group(2)))


def parse_range(text: str) -> list[_Comparator]:
    if not text.strip():
        raise ValueError("Empty range")
    return [_parse_comparator(part) for part in re.split(r"\s+", text.strip()) if part]


def satisfies(version: str, range_expr: str) -> bool:
    v = _parse_version(version)
    return all(comp.matches(v) for comp in parse_range(range_expr))


def is_valid_version(text: str) -> bool:
    try:
        _parse_version(text)
        return True
    except ValueError:
        return False


def is_valid_range(text: str) -> bool:
    try:
        parse_range(text)
        return True
    except ValueError:
        return False
