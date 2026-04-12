from __future__ import annotations

import colorsys
import re
from pathlib import Path


COLOR_HEX_RE = re.compile(r"#(?:[0-9A-Fa-f]{6}|[0-9A-Fa-f]{3})")
TEXT_TOKEN_RE = re.compile(r"[A-Za-z]+|[가-힣]+")

DEFAULT_PALETTE_STRATEGY = {
    "mode": "brand-guided",
    "candidate_count": 3,
    "active_candidate": 1,
    "temperature": "mixed",
    "contrast": "balanced",
    "diversity": "balanced",
    "surface_style": "tinted",
    "prefer_moods": [],
    "avoid_moods": [],
}

DEFAULT_PALETTE_EXPANSION = {
    "enabled": True,
    "supporting_color_count": 12,
    "combination_count": 4,
    "prefer_pairings": True,
    "prefer_related_families": True,
}

KEYWORD_SIGNAL_MAP = {
    "analytical": {
        "prefer": {
            "안정감": 2,
            "신뢰감": 2,
            "지속성": 2,
            "고급스러움": 1,
            "성숙함": 1,
            "deep": 1,
            "natural": 1,
        },
        "avoid": {"달콤함": 2, "playful": 2, "sweet": 2, "cute": 2},
    },
    "bold": {
        "prefer": {
            "강렬함": 3,
            "활기": 2,
            "생동감": 2,
            "열정": 2,
            "주목성": 2,
            "pure": 2,
            "standard": 1,
        },
        "avoid": {"부드러움": 1, "pastel": 2},
    },
    "calm": {
        "prefer": {
            "안정감": 2,
            "부드러움": 2,
            "자연스러움": 2,
            "따뜻함": 1,
            "pastel": 2,
            "natural": 2,
        },
        "avoid": {"강렬함": 2, "주목성": 2, "dynamic": 1, "pure": 1},
    },
    "decisive": {
        "prefer": {
            "상징적": 2,
            "강렬함": 2,
            "주목성": 2,
            "고급스러움": 1,
            "strong": 1,
        },
        "avoid": {"ambiguous": 2, "soft": 1},
    },
    "editorial": {
        "prefer": {
            "고급스러움": 2,
            "고전적": 2,
            "성숙함": 2,
            "세련됨": 2,
            "품격": 2,
            "classic": 2,
            "deep": 2,
        },
        "avoid": {"달콤함": 2, "playful": 2, "cute": 2},
    },
    "energetic": {
        "prefer": {
            "활기": 3,
            "생동감": 3,
            "열정": 2,
            "낙관": 1,
            "주목성": 2,
            "bright": 2,
            "pure": 1,
            "standard": 1,
        },
        "avoid": {"성숙함": 1, "muted": 1},
    },
    "friendly": {
        "prefer": {
            "친근함": 3,
            "부드러움": 2,
            "자연스러움": 2,
            "따뜻함": 1,
            "pastel": 2,
        },
        "avoid": {"강렬함": 2, "고전적": 1},
    },
    "luxury": {
        "prefer": {
            "고급스러움": 3,
            "품격": 3,
            "관능적": 1,
            "성숙함": 2,
            "클래식": 2,
            "deep": 2,
            "trend": 1,
        },
        "avoid": {"달콤함": 2, "cute": 2, "친근함": 1},
    },
    "playful": {
        "prefer": {
            "경쾌함": 3,
            "달콤함": 2,
            "친근함": 2,
            "생기": 2,
            "pastel": 2,
            "bright": 2,
        },
        "avoid": {"성숙함": 2, "고전적": 2, "deep": 2},
    },
    "precise": {
        "prefer": {
            "신뢰감": 2,
            "지속성": 2,
            "안정감": 2,
            "세련됨": 1,
            "measured": 1,
            "natural": 1,
        },
        "avoid": {"playful": 2, "달콤함": 2},
    },
    "trustworthy": {
        "prefer": {
            "신뢰감": 3,
            "안정감": 3,
            "지속성": 2,
            "자연스러움": 1,
            "성숙함": 1,
            "classic": 1,
            "deep": 1,
            "natural": 1,
        },
        "avoid": {"강렬함": 1, "주목성": 1, "달콤함": 2},
    },
    "warm": {
        "prefer": {
            "따뜻함": 3,
            "온기": 2,
            "자연스러움": 1,
            "orange": 1,
            "red": 1,
            "natural": 1,
        },
        "avoid": {"cold": 2},
    },
}

ROLE_TONE_WEIGHTS = {
    "primary": {"deep": 3, "standard": 2, "trend": 2, "natural": 1, "pure": 1, "pastel": -3},
    "accent": {"standard": 3, "trend": 2, "pure": 2, "natural": 1, "pastel": 1, "deep": 0},
    "surface_tint": {"pastel": 4, "natural": 3, "standard": 1, "trend": 0, "pure": -3, "deep": -4},
}


def parse_color_reference_markdown(path: Path) -> dict:
    title = path.stem
    current_family: str | None = None
    current_color: dict | None = None
    colors: list[dict] = []

    for raw_line in path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line:
            continue

        if line.startswith("# "):
            title = line[2:].strip()
            continue

        if line.startswith("## "):
            current_family = line[3:].strip()
            continue

        if line.startswith("### "):
            current_color = {
                "name": line[4:].strip(),
                "family": current_family,
                "hex": None,
                "cmyk": None,
                "mood": None,
                "usage": None,
                "pairings": [],
            }
            colors.append(current_color)
            continue

        if not current_color or not line.startswith("- **"):
            continue

        try:
            label_part, value = line[2:].split("**:", 1)
        except ValueError:
            continue

        label = label_part.replace("**", "").strip().lower()
        value = value.strip()

        if label == "hex":
            match = COLOR_HEX_RE.search(value)
            current_color["hex"] = match.group(0).upper() if match else value
        elif label == "cmyk":
            current_color["cmyk"] = value
        elif label in {"톤/무드", "tone/mood"}:
            current_color["mood"] = value
        elif label == "활용":
            current_color["usage"] = value
        elif label == "배색":
            current_color["pairings"] = [item.upper() for item in COLOR_HEX_RE.findall(value)]

    return {
        "title": title,
        "source_path": str(path),
        "families": sorted({color["family"] for color in colors if color.get("family")}),
        "colors": colors,
    }


def resolve_color_reference(
    reference_config: dict,
    base_dir: Path,
    brand_profile: dict | None = None,
) -> tuple[dict | None, list[str]]:
    if not isinstance(reference_config, dict):
        return None, []

    issues: list[str] = []
    raw_path = str(reference_config.get("path", "")).strip()
    if not raw_path:
        issues.append("color_reference.path is missing")
        return None, issues

    source_path = Path(raw_path)
    if not source_path.is_absolute():
        source_path = (base_dir / source_path).resolve()

    if not source_path.exists():
        issues.append(f"color_reference.path not found: {source_path}")
        return None, issues

    parsed = parse_color_reference_markdown(source_path)
    colors_by_name = {color["name"].lower(): color for color in parsed["colors"]}
    selected_names = [
        str(item).strip()
        for item in reference_config.get("selected_colors", [])
        if str(item).strip()
    ]
    preferred_families = [
        str(item).strip()
        for item in reference_config.get("preferred_families", [])
        if str(item).strip()
    ]
    palette_roles = reference_config.get("palette_roles", {}) or {}
    strategy = _normalize_palette_strategy(reference_config.get("palette_strategy", {}))
    expansion = _normalize_palette_expansion(reference_config.get("palette_expansion", {}))

    resolved_selected: list[dict] = []
    for name in selected_names:
        color = colors_by_name.get(name.lower())
        if color:
            resolved_selected.append(color)
        else:
            issues.append(f"color_reference.selected_colors entry not found: {name}")

    resolved_roles: dict[str, dict] = {}
    for role, name in palette_roles.items():
        color = colors_by_name.get(str(name).lower())
        if color:
            resolved_roles[str(role)] = color
        else:
            issues.append(f"color_reference.palette_roles entry not found: {role} -> {name}")

    profile = brand_profile or {}
    palette_candidates = _build_palette_candidates(
        colors=parsed["colors"],
        preferred_families=preferred_families,
        strategy=strategy,
        brand_profile=profile,
    )

    selection_mode = "manual" if selected_names or palette_roles else strategy["mode"]

    if resolved_selected and not resolved_roles:
        resolved_roles = _infer_palette_roles(resolved_selected, strategy, profile)

    active_candidate = _pick_active_candidate(palette_candidates, strategy)
    if not resolved_roles and active_candidate:
        resolved_roles = active_candidate["roles"]
    if not resolved_selected and active_candidate:
        resolved_selected = _ordered_unique_colors_from_roles(active_candidate["roles"])

    if not resolved_selected and preferred_families:
        preferred_lookup = {item.lower() for item in preferred_families}
        resolved_selected = [
            color
            for color in parsed["colors"]
            if (color.get("family") or "").lower() in preferred_lookup
        ][:8]
        if not resolved_selected:
            issues.append("color_reference.preferred_families did not match any parsed family")
        elif not resolved_roles:
            resolved_roles = _infer_palette_roles(resolved_selected, strategy, profile)

    active_palette = {
        "selection_mode": selection_mode,
        "roles": resolved_roles,
        "selected_colors": resolved_selected,
        "candidate_id": active_candidate.get("id") if active_candidate and selection_mode != "manual" else None,
    }

    if not resolved_roles:
        issues.append("color_reference did not resolve an active palette")

    expanded_palette = _build_expanded_palette(
        colors=parsed["colors"],
        active_palette=active_palette,
        preferred_families=preferred_families,
        strategy=strategy,
        expansion=expansion,
        brand_profile=profile,
    )

    summary = {
        "title": parsed["title"],
        "source_path": parsed["source_path"],
        "families": parsed["families"],
        "selected_colors": resolved_selected,
        "palette_roles": resolved_roles,
        "preferred_families": preferred_families,
        "selection_mode": selection_mode,
        "strategy": strategy,
        "expansion": expansion,
        "active_palette": active_palette,
        "palette_candidates": palette_candidates,
        "expanded_palette": expanded_palette,
        "notes": reference_config.get("notes", []),
    }
    return summary, issues


def _normalize_palette_strategy(raw_strategy: dict | None) -> dict:
    strategy = dict(DEFAULT_PALETTE_STRATEGY)
    if isinstance(raw_strategy, dict):
        strategy.update(
            {
                key: raw_strategy.get(key, strategy[key])
                for key in DEFAULT_PALETTE_STRATEGY
            }
        )

    strategy["mode"] = _pick_enum(strategy["mode"], {"manual", "brand-guided", "exploratory"}, "brand-guided")
    strategy["temperature"] = _pick_enum(strategy["temperature"], {"warm", "neutral", "mixed"}, "mixed")
    strategy["contrast"] = _pick_enum(strategy["contrast"], {"soft", "balanced", "vivid"}, "balanced")
    strategy["diversity"] = _pick_enum(strategy["diversity"], {"cohesive", "balanced", "exploratory"}, "balanced")
    strategy["surface_style"] = _pick_enum(strategy["surface_style"], {"airy", "tinted", "grounded"}, "tinted")
    strategy["candidate_count"] = max(1, min(5, int(strategy.get("candidate_count", 3) or 3)))
    strategy["active_candidate"] = strategy.get("active_candidate", 1)
    strategy["prefer_moods"] = _normalize_text_list(strategy.get("prefer_moods", []))
    strategy["avoid_moods"] = _normalize_text_list(strategy.get("avoid_moods", []))
    return strategy


def _normalize_palette_expansion(raw_expansion: dict | None) -> dict:
    expansion = dict(DEFAULT_PALETTE_EXPANSION)
    if isinstance(raw_expansion, dict):
        expansion.update(
            {
                key: raw_expansion.get(key, expansion[key])
                for key in DEFAULT_PALETTE_EXPANSION
            }
        )

    expansion["enabled"] = bool(expansion.get("enabled", True))
    expansion["supporting_color_count"] = max(
        4,
        min(24, int(expansion.get("supporting_color_count", 12) or 12)),
    )
    expansion["combination_count"] = max(
        2,
        min(6, int(expansion.get("combination_count", 4) or 4)),
    )
    expansion["prefer_pairings"] = bool(expansion.get("prefer_pairings", True))
    expansion["prefer_related_families"] = bool(expansion.get("prefer_related_families", True))
    return expansion


def _build_palette_candidates(
    colors: list[dict],
    preferred_families: list[str],
    strategy: dict,
    brand_profile: dict,
) -> list[dict]:
    if not colors:
        return []

    preferred_lookup = {item.lower() for item in preferred_families}
    pool = list(colors)

    candidates: list[dict] = []
    variants = _build_candidate_variants(strategy)

    for index, variant in enumerate(variants, start=1):
        candidate = _build_candidate(pool, preferred_lookup, variant, brand_profile, index)
        if candidate:
            candidates.append(candidate)

    deduped: list[dict] = []
    seen: set[tuple[str, str, str]] = set()
    for candidate in candidates:
        signature = tuple(candidate["roles"][role]["name"] for role in ["primary", "accent", "surface_tint"])
        if signature in seen:
            continue
        seen.add(signature)
        deduped.append(candidate)

    return deduped[: strategy["candidate_count"]]


def _build_candidate_variants(strategy: dict) -> list[dict]:
    variants = [
        {
            "id": "signature",
            "label": "Signature",
            "temperature": strategy["temperature"],
            "contrast": strategy["contrast"],
            "diversity": strategy["diversity"],
            "surface_style": strategy["surface_style"],
            "prefer_moods": strategy["prefer_moods"],
            "avoid_moods": strategy["avoid_moods"],
        }
    ]

    if strategy["candidate_count"] >= 2:
        variants.append(
            {
                "id": "soft-spread",
                "label": "Soft Spread",
                "temperature": strategy["temperature"],
                "contrast": "soft",
                "diversity": "balanced",
                "surface_style": "airy",
                "prefer_moods": strategy["prefer_moods"],
                "avoid_moods": strategy["avoid_moods"],
            }
        )

    if strategy["candidate_count"] >= 3:
        variants.append(
            {
                "id": "assertive",
                "label": "Assertive",
                "temperature": strategy["temperature"],
                "contrast": "vivid" if strategy["contrast"] != "soft" else "balanced",
                "diversity": "exploratory" if strategy["mode"] == "exploratory" else "balanced",
                "surface_style": "grounded",
                "prefer_moods": strategy["prefer_moods"],
                "avoid_moods": strategy["avoid_moods"],
            }
        )

    if strategy["candidate_count"] >= 4:
        variants.append(
            {
                "id": "grounded",
                "label": "Grounded",
                "temperature": "neutral" if strategy["temperature"] == "mixed" else strategy["temperature"],
                "contrast": "balanced",
                "diversity": "cohesive",
                "surface_style": "grounded",
                "prefer_moods": strategy["prefer_moods"],
                "avoid_moods": strategy["avoid_moods"],
            }
        )

    if strategy["candidate_count"] >= 5:
        variants.append(
            {
                "id": "playful-edge",
                "label": "Playful Edge",
                "temperature": "warm",
                "contrast": "vivid",
                "diversity": "exploratory",
                "surface_style": "airy",
                "prefer_moods": strategy["prefer_moods"],
                "avoid_moods": strategy["avoid_moods"],
            }
        )

    return variants[: strategy["candidate_count"]]


def _build_candidate(
    pool: list[dict],
    preferred_lookup: set[str],
    variant: dict,
    brand_profile: dict,
    index: int,
) -> dict | None:
    primary_rank = _rank_colors(pool, "primary", variant, brand_profile, preferred_lookup)
    if not primary_rank:
        return None

    best_candidate: dict | None = None

    for primary_color, primary_score, primary_reasons in primary_rank[:6]:
        accent_rank = _rank_colors(
            [color for color in pool if color["name"] != primary_color["name"]],
            "accent",
            variant,
            brand_profile,
            preferred_lookup,
            primary=primary_color,
        )
        surface_rank = _rank_colors(
            [color for color in pool if color["name"] != primary_color["name"]],
            "surface_tint",
            variant,
            brand_profile,
            preferred_lookup,
            primary=primary_color,
        )
        if not accent_rank or not surface_rank:
            continue

        for accent_color, accent_score, accent_reasons in accent_rank[:6]:
            for surface_color, surface_score, surface_reasons in surface_rank[:6]:
                if surface_color["name"] in {primary_color["name"], accent_color["name"]}:
                    continue
                combo_score = primary_score + accent_score + surface_score
                combo_score += _pairing_bonus(primary_color, accent_color, surface_color, variant)
                rationale = [
                    primary_reasons[0],
                    accent_reasons[0],
                    surface_reasons[0],
                ]
                candidate = {
                    "id": f"{variant['id']}-{index}",
                    "label": variant["label"],
                    "score": round(combo_score, 2),
                    "roles": {
                        "primary": primary_color,
                        "accent": accent_color,
                        "surface_tint": surface_color,
                    },
                    "rationale": [reason for reason in rationale if reason],
                    "strategy_snapshot": {
                        "temperature": variant["temperature"],
                        "contrast": variant["contrast"],
                        "diversity": variant["diversity"],
                        "surface_style": variant["surface_style"],
                    },
                }
                if not best_candidate or candidate["score"] > best_candidate["score"]:
                    best_candidate = candidate

    return best_candidate


def _rank_colors(
    colors: list[dict],
    role: str,
    variant: dict,
    brand_profile: dict,
    preferred_lookup: set[str],
    primary: dict | None = None,
) -> list[tuple[dict, float, list[str]]]:
    ranked: list[tuple[dict, float, list[str]]] = []
    for color in colors:
        score, reasons = _score_color(color, role, variant, brand_profile, preferred_lookup, primary)
        ranked.append((color, score, reasons))
    return sorted(ranked, key=lambda item: (-item[1], item[0]["name"]))


def _score_color(
    color: dict,
    role: str,
    variant: dict,
    brand_profile: dict,
    preferred_lookup: set[str],
    primary: dict | None = None,
) -> tuple[float, list[str]]:
    tokens = _color_tokens(color)
    searchable = _color_text(color)
    family = (color.get("family") or "").lower()
    tone = _family_tone(color)
    hue = _family_hue(color)
    lightness = _hex_lightness(color.get("hex"))

    score = 0.0
    reasons: list[str] = []

    if preferred_lookup and family in preferred_lookup:
        score += 2.0
        reasons.append(f"{color['name']} is inside preferred families.")

    keyword_score, matched_brand_signal = _brand_keyword_signal_score(searchable, tokens, brand_profile)
    score += keyword_score
    if matched_brand_signal:
        reasons.append(f"{color['name']} matches brand tone keywords.")

    for mood in variant.get("prefer_moods", []) or []:
        if mood in searchable:
            score += 2.0
            reasons.append(f"{color['name']} matches preferred mood '{mood}'.")
    for mood in variant.get("avoid_moods", []) or []:
        if mood in searchable:
            score -= 2.0

    score += ROLE_TONE_WEIGHTS.get(role, {}).get(tone, 0)
    if ROLE_TONE_WEIGHTS.get(role, {}).get(tone, 0):
        reasons.append(f"{color['name']} fits the {role} tone bias.")

    score += _temperature_bonus(hue, variant["temperature"])
    score += _contrast_bonus(role, tone, lightness, variant["contrast"])
    score += _surface_style_bonus(role, lightness, tone, variant["surface_style"])

    if role == "accent" and primary:
        score += _diversity_bonus(primary, color, variant["diversity"])
    if role == "surface_tint" and primary:
        score += _surface_pairing_bonus(primary, color)

    return score, reasons or [f"{color['name']} is viable as {role}."]


def _pairing_bonus(primary: dict, accent: dict, surface: dict, variant: dict) -> float:
    score = 0.0
    if _diversity_signature(primary) != _diversity_signature(accent):
        score += 1.0
    elif variant["diversity"] == "cohesive":
        score += 0.5
    else:
        score -= 0.75

    if surface.get("hex") and surface.get("hex") in primary.get("pairings", []):
        score += 1.5
    if surface.get("hex") and surface.get("hex") in accent.get("pairings", []):
        score += 1.0
    if _hex_lightness(surface.get("hex")) >= 72:
        score += 1.0
    return score


def _infer_palette_roles(colors: list[dict], strategy: dict, brand_profile: dict) -> dict[str, dict]:
    available = list(colors)
    resolved: dict[str, dict] = {}
    for role in ["primary", "accent", "surface_tint"]:
        ranked = _rank_colors(
            colors=available,
            role=role,
            variant=_build_candidate_variants(strategy)[0],
            brand_profile=brand_profile,
            preferred_lookup=set(),
            primary=resolved.get("primary"),
        )
        if not ranked:
            continue
        resolved[role] = ranked[0][0]
        available = [color for color in available if color["name"] != ranked[0][0]["name"]]
    return resolved


def _pick_active_candidate(candidates: list[dict], strategy: dict) -> dict | None:
    if not candidates:
        return None

    requested = strategy.get("active_candidate")
    if isinstance(requested, str) and requested.strip():
        requested_value = requested.strip().lower()
        for candidate in candidates:
            if candidate["id"].lower() == requested_value or candidate["label"].lower() == requested_value:
                return candidate

    try:
        index = int(requested) - 1
    except (TypeError, ValueError):
        index = 0
    index = max(0, min(len(candidates) - 1, index))
    return candidates[index]


def _ordered_unique_colors_from_roles(roles: dict[str, dict]) -> list[dict]:
    ordered: list[dict] = []
    seen: set[str] = set()
    for role in ["primary", "accent", "surface_tint"]:
        item = roles.get(role)
        if not item:
            continue
        name = item.get("name", "")
        if name in seen:
            continue
        seen.add(name)
        ordered.append(item)
    return ordered


def _build_expanded_palette(
    colors: list[dict],
    active_palette: dict,
    preferred_families: list[str],
    strategy: dict,
    expansion: dict,
    brand_profile: dict,
) -> dict | None:
    roles = active_palette.get("roles", {}) or {}
    if not expansion.get("enabled") or not roles:
        return None

    seeds = _ordered_unique_colors_from_roles(roles)
    colors_by_hex = {
        str(color.get("hex", "")).upper(): color
        for color in colors
        if color.get("hex")
    }

    base_candidates = [
        _annotate_palette_entry(color, source_type="reference-color")
        for color in colors
        if color.get("name") not in {seed.get("name") for seed in seeds}
    ]
    pairing_candidates = _build_pairing_swatches(seeds, colors_by_hex)
    support_candidates = _rank_supporting_colors(
        candidates=base_candidates + pairing_candidates,
        seeds=seeds,
        preferred_families=preferred_families,
        strategy=strategy,
        expansion=expansion,
        brand_profile=brand_profile,
    )[: expansion["supporting_color_count"]]

    semantic_roles = _build_semantic_roles(active_palette, support_candidates)
    combination_lists = _build_combination_lists(
        active_palette=active_palette,
        supporting_colors=support_candidates,
        semantic_roles=semantic_roles,
        limit=expansion["combination_count"],
    )

    search_sources = ["brand keywords", "family tone", "hue compatibility"]
    if expansion.get("prefer_pairings"):
        search_sources.insert(0, "seed pairings")
    if expansion.get("prefer_related_families"):
        search_sources.append("related families")

    return {
        "search_strategy": {
            "sources": search_sources,
            "supporting_color_count": expansion["supporting_color_count"],
            "combination_count": expansion["combination_count"],
            "seed_roles": {
                role: {
                    "name": item.get("name"),
                    "hex": item.get("hex"),
                    "family": item.get("family"),
                }
                for role, item in roles.items()
            },
            "preferred_families": preferred_families,
        },
        "supporting_colors": support_candidates,
        "semantic_roles": semantic_roles,
        "combination_lists": combination_lists,
    }


def _annotate_palette_entry(
    color: dict,
    *,
    source_type: str,
    source_seed_names: list[str] | None = None,
) -> dict:
    annotated = dict(color)
    if annotated.get("hex"):
        annotated["hex"] = str(annotated["hex"]).upper()
    annotated["source_type"] = source_type
    if source_seed_names:
        annotated["source_seed_names"] = sorted({name for name in source_seed_names if name})
    return annotated


def _build_pairing_swatches(seeds: list[dict], colors_by_hex: dict[str, dict]) -> list[dict]:
    swatches_by_hex: dict[str, dict] = {}
    for seed in seeds:
        for hex_value in seed.get("pairings", []) or []:
            normalized_hex = str(hex_value).upper()
            if not normalized_hex or normalized_hex == str(seed.get("hex", "")).upper():
                continue
            item = swatches_by_hex.get(normalized_hex)
            if not item:
                base = colors_by_hex.get(normalized_hex)
                if base:
                    item = _annotate_palette_entry(base, source_type="pairing-reference", source_seed_names=[seed.get("name", "")])
                else:
                    item = {
                        "name": f"Pairing {normalized_hex}",
                        "family": "Derived Pairing",
                        "hex": normalized_hex,
                        "mood": "Seed pairing support",
                        "usage": f"Referenced as a compatible pairing for {seed.get('name', 'seed color')}.",
                        "pairings": [],
                        "source_type": "pairing-swatch",
                        "source_seed_names": [seed.get("name", "")],
                    }
                swatches_by_hex[normalized_hex] = item
                continue

            source_seed_names = set(item.get("source_seed_names", []))
            source_seed_names.add(seed.get("name", ""))
            item["source_seed_names"] = sorted(name for name in source_seed_names if name)

    return list(swatches_by_hex.values())


def _rank_supporting_colors(
    candidates: list[dict],
    seeds: list[dict],
    preferred_families: list[str],
    strategy: dict,
    expansion: dict,
    brand_profile: dict,
) -> list[dict]:
    preferred_lookup = {item.lower() for item in preferred_families}
    ranked: list[dict] = []
    for candidate in candidates:
        score, reasons = _score_support_color(
            candidate,
            seeds=seeds,
            preferred_lookup=preferred_lookup,
            strategy=strategy,
            expansion=expansion,
            brand_profile=brand_profile,
        )
        item = dict(candidate)
        item["search_score"] = round(score, 2)
        item["search_reasons"] = reasons[:4]
        ranked.append(item)

    ranked.sort(
        key=lambda item: (
            -float(item.get("search_score", 0)),
            0 if item.get("source_type", "").startswith("pairing") else 1,
            item.get("name", ""),
        )
    )

    deduped: list[dict] = []
    seen: set[tuple[str, str]] = set()
    for item in ranked:
        signature = (str(item.get("hex", "")).upper(), str(item.get("name", "")).lower())
        if signature in seen:
            continue
        seen.add(signature)
        deduped.append(item)
    return deduped


def _score_support_color(
    color: dict,
    *,
    seeds: list[dict],
    preferred_lookup: set[str],
    strategy: dict,
    expansion: dict,
    brand_profile: dict,
) -> tuple[float, list[str]]:
    searchable = _color_text(color)
    tokens = _color_tokens(color)
    family = (color.get("family") or "").lower()
    hue = _family_hue(color)
    tone = _family_tone(color)
    lightness = _hex_lightness(color.get("hex"))
    saturation = _hex_saturation(color.get("hex"))
    seed_hues = {_family_hue(seed) for seed in seeds}
    score = 0.0
    reasons: list[str] = []

    if preferred_lookup and family in preferred_lookup:
        score += 1.5
        reasons.append(f"{color.get('name')} stays inside the preferred families.")

    keyword_score, matched_brand_signal = _brand_keyword_signal_score(searchable, tokens, brand_profile)
    score += keyword_score
    if matched_brand_signal:
        reasons.append(f"{color.get('name')} reinforces the brand mood signals.")

    if expansion.get("prefer_pairings") and color.get("source_type", "").startswith("pairing"):
        score += 3.0
        reasons.append(f"{color.get('name')} comes from the seed pairing references.")

    pairing_hits = []
    for seed in seeds:
        if color.get("hex") and str(color["hex"]).upper() in {str(item).upper() for item in seed.get("pairings", []) or []}:
            score += 2.25
            pairing_hits.append(seed.get("name"))
        if expansion.get("prefer_related_families") and family and family == (seed.get("family") or "").lower():
            score += 0.8
        if hue != "neutral" and hue == _family_hue(seed):
            score += 1.15 if tone != _family_tone(seed) else 0.35

    if pairing_hits:
        joined = ", ".join(name for name in pairing_hits if name)
        reasons.append(f"{color.get('name')} is explicitly paired with {joined}.")

    if strategy.get("surface_style") == "airy" and lightness >= 86:
        score += 0.8
    elif strategy.get("surface_style") == "grounded" and 58 <= lightness <= 82:
        score += 0.8
    elif strategy.get("surface_style") == "tinted" and 72 <= lightness <= 90:
        score += 0.8

    if saturation <= 18 and 18 <= lightness <= 95:
        score += 1.2
        reasons.append(f"{color.get('name')} can act as a neutral support color.")
    if lightness >= 92:
        score += 0.9
    if lightness <= 18:
        score += 0.9

    if strategy.get("diversity") == "exploratory" and hue not in seed_hues and hue not in {"neutral", "brown"}:
        score += 1.0
    elif strategy.get("diversity") == "cohesive" and hue in seed_hues:
        score += 0.75
    elif strategy.get("diversity") == "balanced" and hue not in {"neutral", "brown"}:
        score += 0.3

    return score, reasons or [f"{color.get('name')} broadens the seed palette safely."]


def _build_semantic_roles(active_palette: dict, supporting_colors: list[dict]) -> dict[str, dict]:
    active_roles = active_palette.get("roles", {}) or {}
    pool = _dedupe_palette_entries(
        [
            _annotate_palette_entry(item, source_type=f"active-role:{role}")
            for role, item in active_roles.items()
        ] + supporting_colors
    )

    primary = active_roles.get("primary")
    accent = active_roles.get("accent")
    surface_tint = active_roles.get("surface_tint")

    semantic_roles: dict[str, dict] = {}
    if primary:
        semantic_roles["brand_primary"] = primary
    if accent:
        semantic_roles["brand_accent"] = accent
    if surface_tint:
        semantic_roles["surface_tint"] = surface_tint

    semantic_roles["canvas"] = _choose_palette_entry(
        pool,
        min_lightness=94,
        max_saturation=22,
        prefer_source_types={"pairing-reference", "pairing-swatch"},
    ) or _fallback_color("Canvas White", "#FAF7F2")
    semantic_roles["surface"] = _choose_palette_entry(
        pool,
        min_lightness=82,
        max_lightness=94,
        prefer_tones={"pastel", "natural"},
        prefer_source_types={"pairing-reference", "pairing-swatch"},
    ) or surface_tint or _fallback_color("Soft Surface", "#F3E9DA")
    semantic_roles["border"] = _choose_palette_entry(
        pool,
        min_lightness=60,
        max_lightness=84,
        max_saturation=38,
        prefer_source_types={"pairing-reference", "pairing-swatch"},
    ) or _fallback_color("Border Neutral", "#D8C4A5")
    semantic_roles["ink"] = _choose_palette_entry(
        pool,
        prefer_hues={_family_hue(primary)} if primary else {"neutral", "brown"},
        max_lightness=24,
        prefer_source_types={"pairing-reference", "pairing-swatch", "reference-color"},
    ) or primary or _fallback_color("Ink", "#2E2E2E")
    semantic_roles["ink_muted"] = _choose_palette_entry(
        pool,
        min_lightness=26,
        max_lightness=48,
        max_saturation=42,
    ) or _fallback_color("Muted Ink", "#6B6F74")

    if primary:
        primary_hue = _family_hue(primary)
        semantic_roles["primary_support"] = _choose_palette_entry(
            pool,
            prefer_hues={primary_hue},
            exclude_names={primary.get("name", "")},
            strict_hue_match=True,
        ) or primary
    if accent:
        accent_hue = _family_hue(accent)
        semantic_roles["accent_support"] = _choose_palette_entry(
            pool,
            prefer_hues={accent_hue},
            exclude_names={accent.get("name", "")},
            strict_hue_match=True,
        ) or accent

    semantic_roles["info"] = _choose_palette_entry(pool, prefer_hues={"blue", "purple"}, strict_hue_match=True)
    semantic_roles["success"] = _choose_palette_entry(pool, prefer_hues={"green"}, strict_hue_match=True)
    semantic_roles["warning"] = (
        accent
        if accent and _family_hue(accent) in {"orange", "yellow"}
        else _choose_palette_entry(pool, prefer_hues={"orange", "yellow"}, strict_hue_match=True)
    )
    semantic_roles["danger"] = (
        primary
        if primary and _family_hue(primary) == "red"
        else _choose_palette_entry(pool, prefer_hues={"red"}, strict_hue_match=True)
    )

    return {role: item for role, item in semantic_roles.items() if item}


def _build_combination_lists(
    *,
    active_palette: dict,
    supporting_colors: list[dict],
    semantic_roles: dict[str, dict],
    limit: int,
) -> list[dict]:
    active_roles = active_palette.get("roles", {}) or {}
    combinations = [
        {
            "id": "seed-core",
            "label": "Seed Core",
            "purpose": "기본 테마를 이루는 핵심 색",
            "colors": [
                _combination_entry(role, item)
                for role, item in active_roles.items()
                if item
            ],
        },
        {
            "id": "surface-system",
            "label": "Surface System",
            "purpose": "배경, 패널, 텍스트, 보더에 쓰는 기본 조합",
            "colors": [
                _combination_entry(role, semantic_roles.get(role))
                for role in ["canvas", "surface", "surface_tint", "border", "ink", "ink_muted"]
                if semantic_roles.get(role)
            ],
        },
        {
            "id": "support-spectrum",
            "label": "Support Spectrum",
            "purpose": "보조 하이라이트, 차트, 2차 액션에 쓰는 확장 리스트",
            "colors": [
                _combination_entry("support", item)
                for item in supporting_colors[:6]
            ],
        },
        {
            "id": "semantic-states",
            "label": "Semantic States",
            "purpose": "상태 표현용 색 역할 후보",
            "colors": [
                _combination_entry(role, semantic_roles.get(role))
                for role in ["info", "success", "warning", "danger"]
                if semantic_roles.get(role)
            ],
        },
    ]
    return [item for item in combinations if item["colors"]][:limit]


def _combination_entry(role: str, item: dict | None) -> dict:
    if not item:
        return {}
    return {
        "role": role,
        "name": item.get("name"),
        "hex": item.get("hex"),
        "family": item.get("family"),
        "source_type": item.get("source_type"),
    }


def _choose_palette_entry(
    pool: list[dict],
    *,
    prefer_hues: set[str] | None = None,
    prefer_tones: set[str] | None = None,
    prefer_source_types: set[str] | None = None,
    exclude_names: set[str] | None = None,
    strict_hue_match: bool = False,
    min_lightness: float | None = None,
    max_lightness: float | None = None,
    min_saturation: float | None = None,
    max_saturation: float | None = None,
) -> dict | None:
    best_item: dict | None = None
    best_score = float("-inf")
    for item in pool:
        name = str(item.get("name", ""))
        if exclude_names and name in exclude_names:
            continue

        lightness = _hex_lightness(item.get("hex"))
        saturation = _hex_saturation(item.get("hex"))
        hue = _family_hue(item)
        if min_lightness is not None and lightness < min_lightness:
            continue
        if max_lightness is not None and lightness > max_lightness:
            continue
        if min_saturation is not None and saturation < min_saturation:
            continue
        if max_saturation is not None and saturation > max_saturation:
            continue
        if strict_hue_match and prefer_hues and hue not in prefer_hues:
            continue

        score = float(item.get("search_score", 0))
        if prefer_hues and hue in prefer_hues:
            score += 2.2
        if prefer_tones and _family_tone(item) in prefer_tones:
            score += 1.1
        if prefer_source_types and item.get("source_type") in prefer_source_types:
            score += 0.9
        if best_item is None or score > best_score:
            best_item = item
            best_score = score
    return best_item


def _dedupe_palette_entries(items: list[dict]) -> list[dict]:
    deduped: list[dict] = []
    seen: set[tuple[str, str]] = set()
    for item in items:
        signature = (str(item.get("hex", "")).upper(), str(item.get("name", "")).lower())
        if signature in seen:
            continue
        seen.add(signature)
        deduped.append(item)
    return deduped


def _fallback_color(name: str, hex_value: str) -> dict:
    return {
        "name": name,
        "family": "Generated Fallback",
        "hex": hex_value.upper(),
        "mood": "Generated fallback support color",
        "usage": "Used when the reference file does not expose a suitable support swatch.",
        "pairings": [],
        "source_type": "generated-fallback",
    }


def _pick_enum(value: object, allowed: set[str], fallback: str) -> str:
    normalized = str(value or "").strip().lower()
    return normalized if normalized in allowed else fallback


def _normalize_text_list(values: object) -> list[str]:
    if not isinstance(values, list):
        return []
    return [str(item).strip().lower() for item in values if str(item).strip()]


def _color_text(color: dict) -> str:
    return " ".join(
        str(color.get(key, "")).lower()
        for key in ["name", "family", "mood", "usage"]
    )


def _brand_keyword_signal_score(searchable: str, tokens: set[str], brand_profile: dict) -> tuple[float, bool]:
    score = 0.0
    matched = False

    for keyword in brand_profile.get("brand_keywords", []):
        mapping = KEYWORD_SIGNAL_MAP.get(str(keyword).lower())
        if not mapping:
            continue
        for token, weight in mapping.get("prefer", {}).items():
            normalized = token.lower()
            if normalized in searchable or normalized in tokens:
                score += weight
                matched = True
        for token, weight in mapping.get("avoid", {}).items():
            normalized = token.lower()
            if normalized in searchable or normalized in tokens:
                score -= weight

    for keyword in brand_profile.get("anti_keywords", []):
        mapping = KEYWORD_SIGNAL_MAP.get(str(keyword).lower())
        if not mapping:
            continue
        for token, weight in mapping.get("prefer", {}).items():
            normalized = token.lower()
            if normalized in searchable or normalized in tokens:
                score -= weight

    return score, matched


def _color_tokens(color: dict) -> set[str]:
    tokens = {token.lower() for token in TEXT_TOKEN_RE.findall(_color_text(color))}
    tone = _family_tone(color)
    hue = _family_hue(color)
    if tone:
        tokens.add(tone)
    if hue:
        tokens.add(hue)
    lightness = _hex_lightness(color.get("hex"))
    if lightness >= 75:
        tokens.add("light")
    elif lightness <= 35:
        tokens.add("dark")
    return tokens


def _family_tone(color: dict) -> str:
    family = (color.get("family") or "").lower()
    if family.startswith("deep"):
        return "deep"
    if family.startswith("pastel"):
        return "pastel"
    if family.startswith("natural"):
        return "natural"
    if family.startswith("standard"):
        return "standard"
    if family.startswith("pure"):
        return "pure"
    if "trend" in family or "pantone" in family:
        return "trend"
    return "standard"


def _family_hue(color: dict) -> str:
    searchable = _color_text(color)

    token_map = {
        "red": ["red", "scarlet", "crimson", "ruby", "claret", "sangria", "marsala", "grenadine", "goji", "oxblood"],
        "orange": ["orange", "tangerine", "apricot", "pumpkin", "ochre", "copper", "coral", "persimmon", "peach", "cream", "rust", "terracotta"],
        "yellow": ["yellow", "gold", "ochre", "mustard", "amber", "wheat"],
        "green": ["green", "olive", "mint", "sage", "moss", "forest", "lime", "emerald"],
        "blue": ["blue", "navy", "cobalt", "azure", "sky", "teal", "cyan", "aqua", "indigo"],
        "purple": ["purple", "violet", "lavender", "plum", "mauve"],
        "pink": ["pink", "rose", "blush", "salmon"],
        "brown": ["brown", "beige", "taupe", "camel", "copper", "rust", "sand", "earth"],
        "neutral": ["gray", "grey", "white", "black", "charcoal", "ivory", "cream", "stone", "neutral"],
    }
    for hue, tokens in token_map.items():
        if any(token in searchable for token in tokens):
            return hue

    hue_value = _hex_hue(color.get("hex"))
    saturation = _hex_saturation(color.get("hex"))
    if saturation <= 12:
        return "neutral"
    if hue_value < 15 or hue_value >= 345:
        return "red"
    if hue_value < 45:
        return "orange"
    if hue_value < 70:
        return "yellow"
    if hue_value < 170:
        return "green"
    if hue_value < 255:
        return "blue"
    if hue_value < 320:
        return "purple"
    return "pink"


def _temperature_bonus(hue: str, temperature: str) -> float:
    if temperature == "mixed":
        return 0.0
    if temperature == "warm" and hue in {"red", "orange"}:
        return 1.0
    if temperature == "neutral" and hue == "neutral":
        return 1.0
    if temperature == "neutral" and hue in {"red", "orange"}:
        return -0.25
    return 0.0


def _contrast_bonus(role: str, tone: str, lightness: float, contrast: str) -> float:
    if contrast == "soft":
        target = 48 if role == "primary" else 78
    elif contrast == "vivid":
        target = 30 if role == "primary" else 70
    else:
        target = 38 if role == "primary" else 74

    if role == "accent" and tone in {"pure", "standard", "trend"} and contrast == "vivid":
        return 1.5
    if role == "surface_tint" and tone in {"pastel", "natural"} and contrast == "soft":
        return 1.5

    return max(-2.0, 2.0 - abs(lightness - target) / 12)


def _surface_style_bonus(role: str, lightness: float, tone: str, surface_style: str) -> float:
    if role != "surface_tint":
        return 0.0
    if surface_style == "airy":
        return 2.0 if lightness >= 78 else -1.0
    if surface_style == "grounded":
        return 1.5 if 60 <= lightness <= 75 and tone != "pastel" else -0.5
    return 1.5 if 68 <= lightness <= 84 else -0.5


def _diversity_bonus(primary: dict, accent: dict, diversity: str) -> float:
    primary_signature = _diversity_signature(primary)
    accent_signature = _diversity_signature(accent)
    if diversity == "cohesive":
        return 1.0 if primary_signature == accent_signature else 0.0
    if diversity == "exploratory":
        return 2.0 if primary_signature != accent_signature else -1.5
    return 1.0 if primary_signature != accent_signature else -0.5


def _surface_pairing_bonus(primary: dict, surface: dict) -> float:
    if surface.get("hex") and surface.get("hex") in primary.get("pairings", []):
        return 1.25
    if _family_tone(surface) in {"pastel", "natural"}:
        return 0.75
    return 0.0


def _diversity_signature(color: dict) -> str:
    return f"{_family_hue(color)}:{_family_tone(color)}"


def _hex_rgb(hex_value: str | None) -> tuple[int, int, int] | None:
    if not hex_value:
        return None
    value = hex_value.lstrip("#")
    if len(value) == 3:
        value = "".join(ch * 2 for ch in value)
    try:
        red = int(value[0:2], 16)
        green = int(value[2:4], 16)
        blue = int(value[4:6], 16)
    except ValueError:
        return None
    return red, green, blue


def _hex_hue(hex_value: str | None) -> float:
    rgb = _hex_rgb(hex_value)
    if not rgb:
        return 0.0
    red, green, blue = rgb
    hue, _, _ = colorsys.rgb_to_hls(red / 255, green / 255, blue / 255)
    return hue * 360


def _hex_saturation(hex_value: str | None) -> float:
    rgb = _hex_rgb(hex_value)
    if not rgb:
        return 0.0
    red, green, blue = rgb
    _, lightness, saturation = colorsys.rgb_to_hls(red / 255, green / 255, blue / 255)
    if lightness in {0.0, 1.0}:
        return 0.0
    return saturation * 100


def _hex_lightness(hex_value: str | None) -> float:
    rgb = _hex_rgb(hex_value)
    if not rgb:
        return 50.0
    red, green, blue = rgb
    return ((max(red, green, blue) + min(red, green, blue)) / 510) * 100
