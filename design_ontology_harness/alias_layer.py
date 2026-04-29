"""Semantic token tier classification — core → util → action → component.

Adapted from fivetaku/insane-design alias_layer concept.

Takes resolved CSS custom properties (from var_resolver) and classifies each
into a 4-tier hierarchy:
  - core: raw primitives (color scales, spacing values, radius, base typography)
  - util: reusable utility aliases (size tokens, shadow presets, z-index)
  - action: semantic/intent tokens (primary, surface, text-default, feedback)
  - component: component-scoped slots (button-bg, input-border, nav-item)

Maps to token_schema.json 3-layer structure:
  core      → core layer
  util      → core layer (utility subset)
  action    → semantic layer
  component → component layer
"""

from __future__ import annotations

import re
from collections import Counter


CORE_PATTERNS: list[re.Pattern] = [
    re.compile(r"--.*color-(?:neutral|gray|grey|slate|zinc|stone|red|orange|amber|yellow|lime|green|emerald|teal|cyan|sky|blue|indigo|violet|purple|fuchsia|pink|rose)-?\d", re.IGNORECASE),
    re.compile(r"--.*(?:spacing|space|gap)-?\d", re.IGNORECASE),
    re.compile(r"--.*(?:radius|rounded)-?(?:none|xs|sm|md|lg|xl|2xl|3xl|full|pill|\d)", re.IGNORECASE),
    re.compile(r"--.*(?:font-size|fontSize|type-size)-?\d", re.IGNORECASE),
    re.compile(r"--.*(?:font-weight|fontWeight)-?\d", re.IGNORECASE),
    re.compile(r"--.*(?:line-height|lineHeight)-?\d", re.IGNORECASE),
    re.compile(r"--.*(?:letter-spacing|letterSpacing)-?\d", re.IGNORECASE),
    re.compile(r"--.*(?:duration|timing|easing)-?\d", re.IGNORECASE),
    re.compile(r"--.*(?:shadow|elevation)-?\d", re.IGNORECASE),
    re.compile(r"--.*(?:opacity)-?\d", re.IGNORECASE),
    re.compile(r"--.*(?:breakpoint|screen)-?(?:xs|sm|md|lg|xl|2xl)", re.IGNORECASE),
    re.compile(r"--.*(?:z-index|zIndex)-?\d", re.IGNORECASE),
]

UTIL_PATTERNS: list[re.Pattern] = [
    re.compile(r"--.*(?:size|width|height)-?(?:xs|sm|md|lg|xl|2xl|3xl|\d)", re.IGNORECASE),
    re.compile(r"--.*(?:icon-size|iconSize)", re.IGNORECASE),
    re.compile(r"--.*(?:border-width|borderWidth)", re.IGNORECASE),
    re.compile(r"--.*(?:ring|outline)-?(?:width|offset|color)", re.IGNORECASE),
    re.compile(r"--.*(?:transition|animate)", re.IGNORECASE),
    re.compile(r"--.*(?:container|max-width|maxWidth)", re.IGNORECASE),
    re.compile(r"--.*(?:font-family|fontFamily)", re.IGNORECASE),
]

ACTION_KEYWORDS: list[str] = [
    "primary", "secondary", "tertiary",
    "accent", "brand",
    "surface", "canvas", "background", "bg",
    "foreground", "fg", "text", "ink",
    "border", "separator", "divider", "outline",
    "muted", "subtle", "disabled", "placeholder",
    "hover", "active", "focus", "pressed", "selected",
    "destructive", "danger", "error", "warning", "success", "info",
    "link", "visited",
    "highlight", "emphasis",
    "overlay", "backdrop", "scrim",
    "on-primary", "on-secondary", "on-surface",
    "inverse",
]

COMPONENT_KEYWORDS: list[str] = [
    "button", "btn",
    "input", "textarea", "select", "checkbox", "radio", "switch", "toggle",
    "card", "panel", "sheet",
    "modal", "dialog", "drawer", "popover", "tooltip", "dropdown",
    "nav", "navbar", "sidebar", "header", "footer", "menu", "menubar",
    "tab", "tabs", "pill",
    "badge", "tag", "chip", "avatar",
    "alert", "toast", "banner", "notification",
    "table", "list", "grid",
    "progress", "spinner", "skeleton",
    "breadcrumb", "pagination",
    "accordion", "collapse",
    "slider", "range",
    "calendar", "datepicker",
    "editor", "code-block",
]

SCHEMA_LAYER_MAP = {
    "core": "core",
    "util": "core",
    "action": "semantic",
    "component": "component",
}


def _classify_by_name(name: str) -> str:
    """Classify a CSS custom property name into a tier based on naming patterns."""
    lowered = name.lower()

    for pattern in COMPONENT_KEYWORDS:
        if pattern in lowered:
            return "component"

    action_hits = 0
    for keyword in ACTION_KEYWORDS:
        if keyword in lowered:
            action_hits += 1
    if action_hits > 0:
        for pattern in CORE_PATTERNS:
            if pattern.search(name):
                return "core"
        return "action"

    for pattern in CORE_PATTERNS:
        if pattern.search(name):
            return "core"

    for pattern in UTIL_PATTERNS:
        if pattern.search(name):
            return "util"

    return "core"


def _classify_by_chain(chain: list[str], prop_tiers: dict[str, str]) -> str | None:
    """Infer tier from what a token references in its var() chain.

    If a token references a core token, it's likely util or higher.
    If it references an action token, it's likely component.
    """
    if len(chain) < 2:
        return None

    for ref in chain[1:]:
        if ref.startswith("--"):
            ref_tier = prop_tiers.get(ref)
            if ref_tier == "core":
                return "util"
            if ref_tier in ("util", "action"):
                return "action"
    return None


def classify_tokens(resolved: dict[str, dict]) -> dict[str, dict]:
    """Classify each resolved CSS custom property into a tier.

    Args:
        resolved: Output from var_resolver.resolve_all() —
                  {var_name: {raw, resolved_terminal, chain}}

    Returns:
        {var_name: {tier, schema_layer, chain_length, references}}
    """
    name_tiers: dict[str, str] = {}
    for name in resolved:
        name_tiers[name] = _classify_by_name(name)

    result: dict[str, dict] = {}
    for name, details in resolved.items():
        chain = details.get("chain", [])
        name_tier = name_tiers[name]

        chain_tier = _classify_by_chain(chain, name_tiers)
        if chain_tier and _tier_rank(chain_tier) > _tier_rank(name_tier):
            tier = chain_tier
        else:
            tier = name_tier

        references = [ref for ref in chain[1:] if ref.startswith("--")] if len(chain) > 1 else []

        result[name] = {
            "tier": tier,
            "schema_layer": SCHEMA_LAYER_MAP[tier],
            "chain_length": len(chain),
            "references": references,
        }

    return result


def _tier_rank(tier: str) -> int:
    return {"core": 0, "util": 1, "action": 2, "component": 3}.get(tier, 0)


def build_alias_map(classified: dict[str, dict], resolved: dict[str, dict]) -> dict:
    """Build a structured alias map showing tier membership, hierarchy, and chains.

    Returns:
        {
            "tokens_by_tier": {tier: [{name, raw, resolved_terminal, chain_length, references}]},
            "tier_hierarchy": [{from_tier, to_tier, from_name, to_name}],
            "schema_layer_summary": {layer: {count, tiers}},
            "stats": {total, by_tier, by_schema_layer, avg_chain_length, max_chain_length},
        }
    """
    tokens_by_tier: dict[str, list[dict]] = {
        "core": [], "util": [], "action": [], "component": [],
    }
    hierarchy: list[dict] = []

    for name, info in sorted(classified.items()):
        details = resolved.get(name, {})
        entry = {
            "name": name,
            "raw": details.get("raw", ""),
            "resolved_terminal": details.get("resolved_terminal"),
            "chain_length": info["chain_length"],
            "references": info["references"],
        }
        tokens_by_tier[info["tier"]].append(entry)

        for ref in info["references"]:
            ref_info = classified.get(ref, {})
            if ref_info:
                hierarchy.append({
                    "from_tier": ref_info.get("tier", "unknown"),
                    "to_tier": info["tier"],
                    "from_name": ref,
                    "to_name": name,
                })

    tier_counts = Counter(info["tier"] for info in classified.values())
    layer_counts = Counter(info["schema_layer"] for info in classified.values())
    chain_lengths = [info["chain_length"] for info in classified.values()]

    layer_summary: dict[str, dict] = {}
    for layer in ("core", "semantic", "component"):
        tiers_in_layer = [
            tier for tier, schema_layer in SCHEMA_LAYER_MAP.items() if schema_layer == layer
        ]
        layer_summary[layer] = {
            "count": sum(tier_counts.get(t, 0) for t in tiers_in_layer),
            "tiers": {t: tier_counts.get(t, 0) for t in tiers_in_layer if tier_counts.get(t, 0)},
        }

    return {
        "tokens_by_tier": tokens_by_tier,
        "tier_hierarchy": hierarchy,
        "schema_layer_summary": layer_summary,
        "stats": {
            "total": len(classified),
            "by_tier": dict(sorted(tier_counts.items())),
            "by_schema_layer": dict(sorted(layer_counts.items())),
            "avg_chain_length": round(sum(chain_lengths) / len(chain_lengths), 2) if chain_lengths else 0,
            "max_chain_length": max(chain_lengths) if chain_lengths else 0,
        },
    }


def extract_alias_layer(resolved: dict[str, dict]) -> dict:
    """Pipeline entry point: classify tokens and build alias map.

    Args:
        resolved: Output from var_resolver.resolve_all() —
                  {var_name: {raw, resolved_terminal, chain}}

    Returns:
        {
            "tokens_by_tier": {tier: [...]},
            "tier_hierarchy": [...],
            "schema_layer_summary": {...},
            "stats": {...},
        }
    """
    if not resolved:
        return {
            "tokens_by_tier": {"core": [], "util": [], "action": [], "component": []},
            "tier_hierarchy": [],
            "schema_layer_summary": {
                "core": {"count": 0, "tiers": {}},
                "semantic": {"count": 0, "tiers": {}},
                "component": {"count": 0, "tiers": {}},
            },
            "stats": {
                "total": 0,
                "by_tier": {},
                "by_schema_layer": {},
                "avg_chain_length": 0,
                "max_chain_length": 0,
            },
        }

    classified = classify_tokens(resolved)
    return build_alias_map(classified, resolved)
