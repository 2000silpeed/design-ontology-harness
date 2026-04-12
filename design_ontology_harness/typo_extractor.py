"""Extract typography metadata from CSS custom properties.

Adapted from fivetaku/insane-design typo_extractor.py.

Extracts:
  - Typography scale from semantic CSS custom properties (heading, text, display, etc.)
  - Font family declarations with frequency
  - Font weight usage distribution
"""

from __future__ import annotations

import re
from collections import Counter


CATEGORY_ORDER = {
    "heading": 0,
    "text": 1,
    "display": 2,
    "title": 3,
    "label": 4,
    "caption": 5,
    "input": 6,
    "quote": 7,
    "body": 8,
}

VARIANT_ORDER = {
    "base": 0,
    "xxs": 1,
    "xs": 2,
    "sm": 3,
    "md": 4,
    "lg": 5,
    "xl": 6,
    "xxl": 7,
    "xxxl": 8,
}


def group_typography_tokens(props: dict[str, str]) -> dict[str, dict]:
    """Group --*-font-<category>-<variant>-<prop> into {category-variant: {size, weight, lineHeight, letterSpacing}}.

    Recognized categories: heading, text, display, title, label, caption, input, quote, body.
    """
    grouped: dict[str, dict[str, str]] = {}
    for name, value in props.items():
        match = re.match(
            r"--(.*)font-(heading|text|display|title|label|caption|input|quote|body)-?([a-z0-9]*)-(size|weight|lineHeight|line-height|letterSpacing|letter-spacing)$",
            name,
        )
        if not match:
            continue
        category = match.group(2)
        variant = match.group(3) or "base"
        prop = match.group(4)
        if prop == "line-height":
            prop = "lineHeight"
        elif prop == "letter-spacing":
            prop = "letterSpacing"
        key = f"{category}-{variant}"
        if key not in grouped:
            grouped[key] = {}
        grouped[key][prop] = value.strip()

    result: dict[str, dict[str, str]] = {}
    for key in sorted(
        grouped,
        key=lambda item: (
            CATEGORY_ORDER.get(item.split("-", 1)[0], len(CATEGORY_ORDER)),
            VARIANT_ORDER.get(item.split("-", 1)[1], len(VARIANT_ORDER)),
            item,
        ),
    ):
        result[key] = {
            prop: grouped[key][prop]
            for prop in ("size", "weight", "lineHeight", "letterSpacing")
            if prop in grouped[key]
        }
    return result


def extract_font_families(css: str) -> list[dict]:
    """Return [{declaration, first_name, count}] from all font-family declarations. Skips bare var() references."""
    counts: Counter = Counter()
    for match in re.finditer(r"font-family\s*:\s*([^;{}]+)", css, re.IGNORECASE):
        declaration = match.group(1).strip()
        parse_target = re.sub(r"\s*!important\s*$", "", declaration, flags=re.IGNORECASE)
        if re.fullmatch(r"var\([^)]*\)", parse_target, re.IGNORECASE):
            continue
        counts[declaration] += 1

    result: list[dict] = []
    for declaration, count in sorted(counts.items(), key=lambda item: (-item[1], item[0])):
        first_name = (
            re.sub(r"\s*!important\s*$", "", declaration, flags=re.IGNORECASE)
            .split(",", 1)[0]
            .strip()
        )
        result.append({
            "declaration": declaration,
            "first_name": first_name.strip("\"'"),
            "count": count,
        })
    return result


def extract_font_weights_used(css: str) -> dict[str, int]:
    """Return {weight_value: count} for font-weight declarations."""
    counts = Counter(
        match.group(1).lower()
        for match in re.finditer(
            r"font-weight\s*:\s*(\d{3}|normal|bold|lighter|bolder)",
            css,
            re.IGNORECASE,
        )
    )
    return {
        weight: counts[weight]
        for weight in sorted(
            counts,
            key=lambda weight: (0, int(weight)) if weight.isdigit() else (1, weight),
        )
    }


def extract_typography(css: str) -> dict:
    """Pipeline entry point: extract typography metadata from CSS.

    Returns:
        {
            "scale": {category-variant: {size, weight, lineHeight, letterSpacing}},
            "families": [{declaration, first_name, count}],
            "weights_used": {weight: count},
            "stats": {scale_entries, unique_families, unique_weights},
        }
    """
    props: dict[str, str] = {}
    for name, value in re.findall(r"--([A-Za-z0-9_-]+)\s*:\s*([^;{}]+)", css):
        key = f"--{name}"
        if key not in props:
            props[key] = value.strip()

    scale = group_typography_tokens(props)
    families = extract_font_families(css)
    weights_used = extract_font_weights_used(css)

    return {
        "scale": scale,
        "families": families,
        "weights_used": weights_used,
        "stats": {
            "scale_entries": len(scale),
            "unique_families": len(families),
            "unique_weights": len(weights_used),
        },
    }
