from __future__ import annotations

import colorsys
import re
from pathlib import Path

from .semantic_color_ontology import build_semantic_color_context
from .semantic_color_selector import (
    build_ontology_supporting_colors,
    build_semantic_color_selection,
    colors_from_semantic_palette,
    ontology_keyword_lookup,
)


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
    "chrome_strategy": "chromatic",
    "prefer_moods": [],
    "avoid_moods": [],
}

# 사진이 컬러를 담당하는 제품(패션, 갤러리, 커머스 등)을 위한 무채색 크롬 램프.
# UI 크롬은 상품 이미지와 색으로 경쟁하지 않고, 유채색은 restrained_accent 하나만 남긴다.
ACHROMATIC_CHROME_ROLES = {
    "chrome_ink": {
        "name": "Chrome Ink",
        "family": "Chrome Strategy",
        "hex": "#141414",
        "mood": "무채색 크롬 잉크. 텍스트와 primary action을 담당",
        "usage": "본문, 헤딩, 블랙 CTA. 상품 이미지가 컬러를 담당하므로 크롬은 무채색을 유지한다.",
        "source_type": "chrome-strategy",
    },
    "chrome_paper": {
        "name": "Chrome Paper",
        "family": "Chrome Strategy",
        "hex": "#FFFFFF",
        "mood": "순백 표면",
        "usage": "카드/시트 표면. 사진의 색이 그대로 읽히는 바탕.",
        "source_type": "chrome-strategy",
    },
    "chrome_canvas": {
        "name": "Chrome Canvas",
        "family": "Chrome Strategy",
        "hex": "#FAFAFA",
        "mood": "미세 그레이 캔버스",
        "usage": "앱 배경. 표면과 1단계 분리.",
        "source_type": "chrome-strategy",
    },
    "chrome_line": {
        "name": "Chrome Line",
        "family": "Chrome Strategy",
        "hex": "#E5E5E5",
        "mood": "헤어라인",
        "usage": "구분선, 보더. 그림자보다 라인 분리를 우선.",
        "source_type": "chrome-strategy",
    },
    "chrome_muted": {
        "name": "Chrome Muted",
        "family": "Chrome Strategy",
        "hex": "#737373",
        "mood": "보조 텍스트 그레이",
        "usage": "메타 정보, 캡션, 비활성 라벨.",
        "source_type": "chrome-strategy",
    },
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
        return resolve_semantic_color_reference(brand_profile or {}, reference_config), issues

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

    ontology_lookup = ontology_keyword_lookup()
    resolved_roles: dict[str, dict] = {}
    for role, name in palette_roles.items():
        color = colors_by_name.get(str(name).lower()) or ontology_lookup.get(str(name).lower())
        if color:
            resolved_roles[str(role)] = color
        else:
            issues.append(
                f"color_reference.palette_roles entry not found in markdown or semantic ontology: {role} -> {name}"
            )

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

    # ── Pitfall #3 리브랜딩 지체 경고 ──
    # 팔레트 내 동일 hue 계열에서 명도/채도가 크게 다른 색이 공존하면
    # 구 브랜드 hex가 섞여있을 가능성 경고
    pitfall_warnings = _detect_rebrand_remnants(resolved_selected)
    for warning in pitfall_warnings:
        issues.append(f"[pitfall#3-rebrand] {warning}")

    semantic_color_selection = build_semantic_color_selection(
        brand_profile=profile,
        strategy=strategy,
        candidate_count=strategy.get("candidate_count"),
    )
    if selection_mode != "manual":
        semantic_roles = colors_from_semantic_palette(semantic_color_selection.get("active_palette"))
        if semantic_roles:
            resolved_roles = semantic_roles
            resolved_selected = _ordered_unique_colors_any_roles(semantic_roles)
            active_palette = {
                "selection_mode": "semantic-ontology",
                "roles": resolved_roles,
                "selected_colors": resolved_selected,
                "candidate_id": (semantic_color_selection.get("active_palette") or {}).get("id"),
            }
            selection_mode = "semantic-ontology"
            # 팔레트가 온톨로지에서 왔으면 supporting 확장도 온톨로지에서 가져온다.
            # md 문서는 무드/패밀리 참고용 advisory로만 남는다.
            ontology_supporting = build_ontology_supporting_colors(
                brand_profile=profile,
                strategy=strategy,
                active_palette=active_palette,
                count=expansion.get("supporting_color_count", 8),
            )
            expanded_palette = {
                "enabled": bool(ontology_supporting),
                "search_strategy": {
                    "source": "semantic-color-ontology",
                    "selection_method": "ontology-search-per-run",
                },
                "supporting_colors": ontology_supporting,
                "semantic_roles": resolved_roles,
                "combination_lists": [],
            }

    active_palette, resolved_roles, resolved_selected = _apply_chrome_strategy(
        active_palette, strategy
    )

    semantic_ontology = build_semantic_color_context(
        parsed_reference=parsed,
        active_palette=active_palette,
        brand_profile=profile,
        strategy=strategy,
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
        "semantic_color_selection": semantic_color_selection,
        "expanded_palette": expanded_palette,
        "semantic_ontology": semantic_ontology,
        "notes": reference_config.get("notes", []),
    }
    return summary, issues


def resolve_semantic_color_reference(
    brand_profile: dict,
    reference_config: dict | None = None,
) -> dict:
    reference_config = reference_config or {}
    strategy = _normalize_palette_strategy(reference_config.get("palette_strategy", {}))
    semantic_color_selection = build_semantic_color_selection(
        brand_profile=brand_profile,
        strategy=strategy,
        candidate_count=strategy.get("candidate_count"),
    )
    selection_mode = "semantic-ontology"
    resolved_roles = colors_from_semantic_palette(semantic_color_selection.get("active_palette"))

    # 수동 palette_roles는 md 파일 없이도 온톨로지 키워드 이름으로 해석한다.
    manual_roles = reference_config.get("palette_roles") or {}
    if manual_roles:
        lookup = ontology_keyword_lookup()
        manual_resolved: dict[str, dict] = {}
        for role, name in manual_roles.items():
            color = lookup.get(str(name).lower())
            if color:
                manual_resolved[str(role)] = color
        if manual_resolved:
            resolved_roles = manual_resolved
            selection_mode = "manual"

    resolved_selected = _ordered_unique_colors_any_roles(resolved_roles)
    active_palette = {
        "selection_mode": selection_mode,
        "roles": resolved_roles,
        "selected_colors": resolved_selected,
        "candidate_id": (
            (semantic_color_selection.get("active_palette") or {}).get("id")
            if selection_mode != "manual"
            else None
        ),
    }
    active_palette, resolved_roles, resolved_selected = _apply_chrome_strategy(
        active_palette, strategy
    )
    supporting_colors = build_ontology_supporting_colors(
        brand_profile=brand_profile,
        strategy=strategy,
        active_palette=active_palette,
        count=_normalize_palette_expansion(reference_config.get("palette_expansion", {})).get(
            "supporting_color_count", 8
        ),
    )
    semantic_ontology = build_semantic_color_context(
        parsed_reference={"title": "Semantic OS color ontology", "colors": []},
        active_palette=active_palette,
        brand_profile=brand_profile,
        strategy=strategy,
    )

    return {
        "title": "Semantic OS color ontology",
        "source_path": None,
        "families": sorted(
            {
                item.get("family")
                for item in resolved_selected
                if item.get("family")
            }
        ),
        "selected_colors": resolved_selected,
        "palette_roles": resolved_roles,
        "preferred_families": [],
        "selection_mode": selection_mode,
        "strategy": strategy,
        "expansion": _normalize_palette_expansion(reference_config.get("palette_expansion", {})),
        "active_palette": active_palette,
        "palette_candidates": [],
        "semantic_color_selection": semantic_color_selection,
        "expanded_palette": {
            "enabled": bool(supporting_colors),
            "search_strategy": {
                "source": "semantic-color-ontology",
                "selection_method": "ontology-search-per-run",
            },
            "supporting_colors": supporting_colors,
            "semantic_roles": resolved_roles,
            "combination_lists": [],
        },
        "semantic_ontology": semantic_ontology,
        "notes": reference_config.get("notes", []),
    }


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
    strategy["chrome_strategy"] = _pick_enum(
        strategy.get("chrome_strategy"), {"chromatic", "achromatic-photographic"}, "chromatic"
    )
    strategy["candidate_count"] = max(1, min(8, int(strategy.get("candidate_count", 3) or 3)))
    strategy["active_candidate"] = strategy.get("active_candidate", 1)
    strategy["prefer_moods"] = _normalize_text_list(strategy.get("prefer_moods", []))
    strategy["avoid_moods"] = _normalize_text_list(strategy.get("avoid_moods", []))
    return strategy


def _apply_chrome_strategy(
    active_palette: dict,
    strategy: dict,
) -> tuple[dict, dict, list[dict]]:
    """Rewrite the active palette for the configured chrome strategy.

    ``achromatic-photographic``: the ontology-selected palette is demoted to a
    single ``restrained_accent``; every other UI role becomes an achromatic
    chrome ramp so product imagery carries the color. Returns
    (active_palette, roles, selected_colors) — unchanged for ``chromatic``.
    """

    if strategy.get("chrome_strategy") != "achromatic-photographic":
        return active_palette, active_palette.get("roles", {}), active_palette.get("selected_colors", [])

    source_roles = active_palette.get("roles") or {}
    accent_pick: dict | None = None
    best_score = -1.0
    for color in source_roles.values():
        if not isinstance(color, dict) or not color.get("hex"):
            continue
        saturation = _hex_saturation(color.get("hex"))
        lightness = _hex_lightness(color.get("hex"))
        # 액센트는 충분히 유채색이고 중간 명도일 것
        if saturation < 20 or not 18 <= lightness <= 78:
            continue
        score = saturation - abs(lightness - 48)
        if score > best_score:
            best_score = score
            accent_pick = color

    roles: dict[str, dict] = {key: dict(value) for key, value in ACHROMATIC_CHROME_ROLES.items()}
    if accent_pick:
        accent = dict(accent_pick)
        accent["usage"] = (
            "유일한 유채색 액센트. 세일/알림/포커스처럼 정말 시선이 필요한 지점 하나에만 쓴다. "
            "버튼 기본색은 chrome_ink."
        )
        roles["restrained_accent"] = accent

    selected = _ordered_unique_colors_any_roles(roles)
    rewritten = dict(active_palette)
    rewritten["roles"] = roles
    rewritten["selected_colors"] = selected
    rewritten["chrome_strategy"] = "achromatic-photographic"
    rewritten["chrome_notes"] = [
        "UI 크롬은 무채색 램프로 유지하고 상품/도메인 이미지가 컬러를 담당한다.",
        "유채색은 restrained_accent 하나만 허용된다.",
        "온톨로지가 고른 원 팔레트는 accent 선정 근거로만 쓰였다.",
    ]
    return rewritten, roles, selected


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

    # ── Pitfall guardrails ──

    # #2 브랜드키트≠UI색 / #12 Logo wall 오염: 과포화 색상은 로고/일러스트 전용일 가능성
    saturation = _hex_saturation(color.get("hex"))
    if saturation > 90 and role in ("primary", "surface_tint"):
        score -= 2.0
        reasons.append(f"{color['name']} penalized: oversaturated ({saturation:.0f}%) — likely brand-kit/logo color, not UI color.")
    elif saturation > 90 and role == "accent":
        score -= 0.5
        reasons.append(f"{color['name']} mildly penalized: oversaturated ({saturation:.0f}%) for accent.")

    # #12 Logo wall: usage/mood에 logo/brand-kit 키워드가 있으면 UI 용도 감점
    _logo_keywords = {"logo", "로고", "brand kit", "브랜드키트", "illustration", "일러스트"}
    usage_text = (color.get("usage") or "").lower()
    mood_text = (color.get("mood") or "").lower()
    if any(kw in usage_text or kw in mood_text for kw in _logo_keywords):
        score -= 3.0
        reasons.append(f"{color['name']} penalized: tagged as logo/brand-kit color, not for UI.")

    # #10 Warm/Cool neutral: neutral 색의 온도 감지 (순흑/순백이 아닌 warm/cool 구분)
    if hue == "neutral":
        _warm_cool = _neutral_temperature(color.get("hex"))
        if _warm_cool != "achromatic":
            tokens.add(f"neutral-{_warm_cool}")

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


def _ordered_unique_colors_any_roles(roles: dict[str, dict]) -> list[dict]:
    ordered: list[dict] = []
    seen: set[str] = set()
    preferred = [
        "primary",
        "accent",
        "surface_tint",
        "anchor_surface",
        "anchor_background",
        "depth_support",
        "structural_support",
        "interface_surface",
        "reading_field",
        "quiet_background",
        "paper_field",
        "action_signal",
        "fresh_accent",
        "attention_flash",
        "proof_accent",
        "proof_light",
    ]
    for role in [*preferred, *roles.keys()]:
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
    component_sets = build_component_color_sets(semantic_roles)
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
        "component_sets": component_sets,
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
        max_saturation=18,
        prefer_source_types={"pairing-reference", "pairing-swatch"},
    ) or _fallback_color("Canvas White", "#F7F8FA")
    # Surface should be near-white, NOT the branded surface_tint. Previously the
    # fallback returned surface_tint which produced Sky Blue as surface in Glacier.
    semantic_roles["surface"] = _choose_palette_entry(
        pool,
        min_lightness=95,
        max_saturation=10,
        prefer_source_types={"pairing-reference", "pairing-swatch"},
    ) or _fallback_color("Paper", "#FFFFFF")
    semantic_roles["surface_muted"] = _choose_palette_entry(
        pool,
        min_lightness=88,
        max_lightness=95,
        max_saturation=14,
        prefer_source_types={"pairing-reference", "pairing-swatch"},
    ) or _fallback_color("Surface Muted", "#EEF1F6")
    semantic_roles["surface_elevated"] = semantic_roles.get("surface") or _fallback_color("Surface Elevated", "#FFFFFF")
    semantic_roles["border"] = _choose_palette_entry(
        pool,
        min_lightness=76,
        max_lightness=92,
        max_saturation=20,
        prefer_source_types={"pairing-reference", "pairing-swatch"},
    ) or _fallback_color("Border Neutral", "#D6DDE6")
    semantic_roles["border_strong"] = _choose_palette_entry(
        pool,
        min_lightness=58,
        max_lightness=78,
        max_saturation=24,
        prefer_source_types={"pairing-reference", "pairing-swatch"},
    ) or _fallback_color("Border Strong", "#B0BAC7")
    semantic_roles["ink"] = _choose_palette_entry(
        pool,
        max_lightness=20,
        prefer_source_types={"pairing-reference", "pairing-swatch", "reference-color"},
    ) or _fallback_color("Ink", "#111111")
    semantic_roles["ink_muted"] = _choose_palette_entry(
        pool,
        min_lightness=30,
        max_lightness=52,
        max_saturation=32,
    ) or _fallback_color("Muted Ink", "#4B5563")
    semantic_roles["ink_subtle"] = _choose_palette_entry(
        pool,
        min_lightness=46,
        max_lightness=66,
        max_saturation=28,
    ) or _fallback_color("Subtle Ink", "#6B7280")
    semantic_roles["ink_inverse"] = _fallback_color("Ink Inverse", "#FFFFFF")

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

    semantic_roles["info"] = _choose_palette_entry(pool, prefer_hues={"blue", "purple"}, strict_hue_match=True) or _fallback_color("Info", "#4A6B8A")
    semantic_roles["success"] = _choose_palette_entry(pool, prefer_hues={"green"}, strict_hue_match=True) or _fallback_color("Success", "#4A7C59")
    semantic_roles["warning"] = (
        accent
        if accent and _family_hue(accent) in {"orange", "yellow"}
        else _choose_palette_entry(pool, prefer_hues={"orange", "yellow"}, strict_hue_match=True)
    ) or _fallback_color("Warning", "#B8860B")
    semantic_roles["danger"] = (
        primary
        if primary and _family_hue(primary) == "red"
        else _choose_palette_entry(pool, prefer_hues={"red"}, strict_hue_match=True)
    ) or _fallback_color("Danger", "#8B2252")

    link_source = primary or accent
    if link_source:
        link_hex = link_source.get("hex")
        semantic_roles["link"] = link_source
        if link_hex:
            semantic_roles["link_hover"] = _fallback_color("Link Hover", _shift_hex(link_hex, dl=-0.08) or link_hex)

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
    # Derived pairing swatches carry cross-reference text ("pairing for Sky Blue")
    # in their usage field that would otherwise trick the token map. For those
    # items, rely purely on the hex so a neutral #333333 pairing isn't classified
    # as "blue" just because the seed it's paired with happens to be blue.
    source_type = str(color.get("source_type") or "")
    if source_type in {"pairing-swatch", "pairing-reference"}:
        return _hex_family_hue(color.get("hex"))

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

    return _hex_family_hue(color.get("hex"))


def _hex_family_hue(hex_value: str | None) -> str:
    hue_value = _hex_hue(hex_value)
    saturation = _hex_saturation(hex_value)
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


def _detect_rebrand_remnants(colors: list[dict]) -> list[str]:
    """Pitfall #3: detect potential old-brand hex remnants.

    If two colors share the same hue bucket but differ significantly in
    lightness (>25) or saturation (>30), one may be a legacy brand color
    that wasn't fully removed after rebranding.
    """
    warnings: list[str] = []
    by_hue: dict[str, list[dict]] = {}
    for color in colors:
        hue = _family_hue(color)
        if hue == "neutral":
            continue
        by_hue.setdefault(hue, []).append(color)

    for hue, group in by_hue.items():
        if len(group) < 2:
            continue
        for i, a in enumerate(group):
            for b in group[i + 1:]:
                l_diff = abs(_hex_lightness(a.get("hex")) - _hex_lightness(b.get("hex")))
                s_diff = abs(_hex_saturation(a.get("hex")) - _hex_saturation(b.get("hex")))
                if l_diff > 25 or s_diff > 30:
                    warnings.append(
                        f"{a['name']} vs {b['name']} ({hue}): lightness diff {l_diff:.0f}, "
                        f"saturation diff {s_diff:.0f} — possible rebrand remnant"
                    )
    return warnings


def _neutral_temperature(hex_value: str | None) -> str:
    """Detect warm/cool bias in neutral colors (pitfall #10).

    Notion uses warm ink (#37352F), Retool uses cream (#E9EBDF).
    Pure black/white are achromatic; biased neutrals carry brand identity.
    """
    rgb = _hex_rgb(hex_value)
    if not rgb:
        return "achromatic"
    red, green, blue = rgb
    if red == green == blue:
        return "achromatic"
    _, _, sat = colorsys.rgb_to_hls(red / 255, green / 255, blue / 255)
    if sat * 100 > 12:
        return "achromatic"  # not neutral enough
    hue = _hex_hue(hex_value)
    if 15 <= hue <= 70:
        return "warm"
    if 170 <= hue <= 290:
        return "cool"
    return "achromatic"


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


def _rgb_hex(rgb: tuple[int, int, int]) -> str:
    r, g, b = (max(0, min(255, int(round(c)))) for c in rgb)
    return f"#{r:02X}{g:02X}{b:02X}"


def _hsl_to_hex(hue: float, sat: float, lightness: float) -> str:
    h = (hue % 360) / 360
    s = max(0.0, min(1.0, sat))
    normalized_lightness = max(0.0, min(1.0, lightness))
    r, g, b = colorsys.hls_to_rgb(h, normalized_lightness, s)
    return _rgb_hex((r * 255, g * 255, b * 255))


def _shift_hex(hex_value: str | None, *, dl: float = 0.0, ds: float = 0.0) -> str | None:
    """Shift a hex color in HSL space. dl/ds are in [-1, 1]."""
    rgb = _hex_rgb(hex_value)
    if not rgb:
        return None
    r, g, b = rgb
    h, lightness, s = colorsys.rgb_to_hls(r / 255, g / 255, b / 255)
    new_l = max(0.0, min(1.0, lightness + dl))
    new_s = max(0.0, min(1.0, s + ds))
    nr, ng, nb = colorsys.hls_to_rgb(h, new_l, new_s)
    return _rgb_hex((nr * 255, ng * 255, nb * 255))


def _mix_hex(hex_a: str | None, hex_b: str | None, weight_b: float) -> str | None:
    """Linear RGB mix. weight_b in [0,1]; 0 returns a, 1 returns b."""
    ra = _hex_rgb(hex_a)
    rb = _hex_rgb(hex_b)
    if not ra or not rb:
        return None
    wa = max(0.0, min(1.0, 1 - weight_b))
    wb = 1 - wa
    return _rgb_hex(
        (
            ra[0] * wa + rb[0] * wb,
            ra[1] * wa + rb[1] * wb,
            ra[2] * wa + rb[2] * wb,
        )
    )


def _alpha_over_white(hex_value: str | None, alpha: float) -> str | None:
    """Flatten a transparent color over white — used to fake alpha in CSS var outputs."""
    rgb = _hex_rgb(hex_value)
    if not rgb:
        return None
    r, g, b = rgb
    a = max(0.0, min(1.0, alpha))
    return _rgb_hex(
        (
            r * a + 255 * (1 - a),
            g * a + 255 * (1 - a),
            b * a + 255 * (1 - a),
        )
    )


def _is_dark(hex_value: str | None) -> bool:
    return _hex_lightness(hex_value or "") < 55


def build_component_color_sets(semantic_roles: dict[str, dict]) -> dict[str, dict[str, str]]:
    """Derive per-component state color sets from semantic role colors.

    Takes the resolved semantic_roles (brand_primary, brand_accent, surface,
    canvas, ink, ink_muted, etc.) and returns a nested dict:
        { "button_primary": {"surface_default": "#XXX", "surface_hover": "#YYY", ...},
          "input": {...}, "card": {...}, ... }

    The output is consumed by Section 15 Drop-in CSS renderer to emit
    component-specific CSS variables that agents and designers can copy directly.

    All derivations use simple HSL shifts so the brand identity is preserved
    and no new hues are invented. Disabled states mix against the canvas
    surface to simulate alpha without requiring rgba() in the output.
    """
    def _hex(role: str) -> str | None:
        item = semantic_roles.get(role)
        if isinstance(item, dict):
            return item.get("hex")
        return None

    brand_primary = _hex("brand_primary")
    brand_accent = _hex("brand_accent")
    surface = _hex("surface") or "#FFFFFF"
    canvas = _hex("canvas") or "#F7F8FA"
    ink = _hex("ink") or "#111111"
    ink_muted = _hex("ink_muted") or "#4B5563"
    border = _hex("border") or "#D6DDE6"
    info = _hex("info")
    success = _hex("success")
    warning = _hex("warning")
    danger = _hex("danger")

    primary_on_light = _is_dark(brand_primary)
    primary_text = "#FFFFFF" if primary_on_light else ink

    sets: dict[str, dict[str, str]] = {}

    if brand_primary:
        sets["button_primary"] = {
            "surface_default": brand_primary,
            "surface_hover": _shift_hex(brand_primary, dl=-0.06) or brand_primary,
            "surface_active": _shift_hex(brand_primary, dl=-0.1) or brand_primary,
            "surface_disabled": _mix_hex(brand_primary, canvas, 0.6) or brand_primary,
            "text_default": primary_text,
            "text_disabled": _mix_hex(primary_text, canvas, 0.5) or primary_text,
            "border_default": brand_primary,
            "focus_ring": brand_primary,
        }

    sets["button_secondary"] = {
        "surface_default": surface,
        "surface_hover": _mix_hex(surface, ink, 0.06) or surface,
        "surface_active": _mix_hex(surface, ink, 0.1) or surface,
        "surface_disabled": canvas,
        "text_default": ink,
        "text_disabled": _mix_hex(ink, canvas, 0.55) or ink_muted,
        "border_default": _shift_hex(border, dl=-0.08) or border,
        "border_hover": _shift_hex(border, dl=-0.16) or border,
        "focus_ring": brand_primary or ink,
    }

    sets["button_ghost"] = {
        "surface_default": "transparent",
        "surface_hover": _mix_hex(surface, ink, 0.05) or surface,
        "surface_active": _mix_hex(surface, ink, 0.09) or surface,
        "surface_disabled": "transparent",
        "text_default": ink_muted,
        "text_hover": ink,
        "text_disabled": _mix_hex(ink_muted, canvas, 0.55) or ink_muted,
        "border_default": "transparent",
        "focus_ring": brand_primary or ink,
    }

    if danger:
        sets["button_danger"] = {
            "surface_default": danger,
            "surface_hover": _shift_hex(danger, dl=-0.06) or danger,
            "surface_active": _shift_hex(danger, dl=-0.1) or danger,
            "text_default": "#FFFFFF" if _is_dark(danger) else ink,
            "border_default": danger,
            "focus_ring": danger,
        }

    sets["input"] = {
        "surface_default": surface,
        "surface_filled": surface,
        "surface_disabled": canvas,
        "text_default": ink,
        "text_placeholder": _mix_hex(ink_muted, canvas, 0.4) or ink_muted,
        "text_disabled": _mix_hex(ink_muted, canvas, 0.55) or ink_muted,
        "border_default": border,
        "border_hover": _shift_hex(border, dl=-0.1) or border,
        "border_focus": brand_primary or ink,
        "border_error": danger or "#B3261E",
        "border_disabled": _shift_hex(border, dl=0.05) or border,
    }

    sets["card"] = {
        "surface_default": surface,
        "surface_hover": _mix_hex(surface, ink, 0.02) or surface,
        "surface_muted": canvas,
        "border_default": border,
        "border_hover": _shift_hex(border, dl=-0.1) or border,
        "border_focus": brand_primary or ink,
    }

    sets["nav_link"] = {
        "text_default": ink_muted,
        "text_hover": ink,
        "text_active": brand_primary or ink,
        "surface_hover": _mix_hex(surface, ink, 0.04) or surface,
        "indicator": brand_accent or brand_primary or ink,
    }

    sets["link"] = {
        "text_default": brand_primary or ink,
        "text_hover": _shift_hex(brand_primary, dl=-0.1) if brand_primary else ink,
        "text_visited": _shift_hex(brand_primary, dl=-0.05, ds=-0.2) if brand_primary else ink_muted,
    }

    if info:
        sets["feedback_info"] = _feedback_set(info, surface, ink, canvas)
    if success:
        sets["feedback_success"] = _feedback_set(success, surface, ink, canvas)
    if warning:
        sets["feedback_warning"] = _feedback_set(warning, surface, ink, canvas)
    if danger:
        sets["feedback_danger"] = _feedback_set(danger, surface, ink, canvas)

    return {name: {k: v for k, v in entries.items() if v} for name, entries in sets.items()}


def _feedback_set(color: str, surface: str, ink: str, canvas: str) -> dict[str, str]:
    bg = _mix_hex(surface, color, 0.12) or surface
    border = _mix_hex(color, canvas, 0.3) or color
    text = color if not _is_dark(surface) else _shift_hex(color, dl=0.1) or color
    return {
        "surface": bg,
        "text": text,
        "border": border,
        "icon": color,
    }
