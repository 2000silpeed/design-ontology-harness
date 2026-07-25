from __future__ import annotations

import colorsys
import hashlib
import json
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

from PIL import Image, ImageFilter

from .aesthetic_loop import DEFAULT_METRICS, build_brand_aesthetic_contract


@dataclass(frozen=True)
class ScreenshotFeatures:
    path: str
    sha256: str
    width: int
    height: int
    orientation: str
    luminance_mean: float
    luminance_std: float
    luminance_span: float
    saturation_mean: float
    saturation_std: float
    neutral_share: float
    light_neutral_share: float
    dark_share: float
    accent_share: float
    edge_density: float
    active_cell_share: float
    photo_cell_share: float
    dominant_colors: list[dict[str, Any]]

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def score_screenshots(
    screenshot_paths: list[Path],
    *,
    brand_profile: dict[str, Any] | None = None,
    design_id: str | None = None,
) -> dict[str, Any]:
    if not screenshot_paths:
        raise ValueError("At least one screenshot path is required.")

    features = [analyze_screenshot(path) for path in screenshot_paths]
    aggregate = _aggregate_features(features)
    brand_profile = brand_profile or {}
    metrics, notes = _score_metrics(aggregate, brand_profile)
    resolved_design_id = (
        design_id
        or brand_profile.get("system_name")
        or brand_profile.get("brand_name")
        or screenshot_paths[0].stem
    )

    return {
        "schema_version": "aesthetic-candidate/v1",
        "design_id": resolved_design_id,
        "score_scale": 10,
        "source_screenshots": [str(path) for path in screenshot_paths],
        "measurement_protocol": {
            "method": "automated screenshot heuristic v1",
            "note": (
                "Scores are generated from pixel-level visual proxies such as palette control, contrast, "
                "edge density, layout activity, photo/asset signal, and responsive screenshot coverage. "
                "Semantic claims still need human or model review."
            ),
        },
        "metrics": metrics,
        "metric_evidence": {
            metric_id: [{
                "source": "automated",
                "method": "automated screenshot heuristic v1",
                "artifacts": [str(path) for path in screenshot_paths],
                "note": notes.get(metric_id),
            }]
            for metric_id in metrics
        },
        "automated_metric_notes": notes,
        "automated_feature_report": {
            "aggregate": aggregate,
            "screenshots": [feature.to_dict() for feature in features],
        },
    }


def analyze_screenshot(path: Path) -> ScreenshotFeatures:
    image_path = path.resolve()
    with Image.open(image_path) as raw_image:
        original = raw_image.convert("RGB")
        width, height = original.size
        sample = original.copy()
        sample.thumbnail((420, 420))
        pixels = list(_pixel_data(sample))

        luminances: list[float] = []
        saturations: list[float] = []
        neutral_count = 0
        light_neutral_count = 0
        dark_count = 0
        accent_count = 0
        for red, green, blue in pixels:
            luminance = _relative_luminance((red, green, blue))
            _, saturation, _ = colorsys.rgb_to_hsv(red / 255, green / 255, blue / 255)
            luminances.append(luminance)
            saturations.append(saturation)
            if saturation < 0.12:
                neutral_count += 1
            if saturation < 0.15 and luminance > 0.85:
                light_neutral_count += 1
            if luminance < 0.18:
                dark_count += 1
            if saturation > 0.22 and 0.2 < luminance < 0.85:
                accent_count += 1

        pixel_count = len(pixels) or 1
        luminance_mean = _mean(luminances)
        saturation_mean = _mean(saturations)
        edge_density = _edge_density(sample)
        active_cell_share, photo_cell_share = _tile_activity(sample)

    return ScreenshotFeatures(
        path=str(image_path),
        sha256=_sha256(image_path),
        width=width,
        height=height,
        orientation=_orientation(width, height),
        luminance_mean=round(luminance_mean, 4),
        luminance_std=round(_stddev(luminances, luminance_mean), 4),
        luminance_span=round((max(luminances) - min(luminances)) if luminances else 0.0, 4),
        saturation_mean=round(saturation_mean, 4),
        saturation_std=round(_stddev(saturations, saturation_mean), 4),
        neutral_share=round(neutral_count / pixel_count, 4),
        light_neutral_share=round(light_neutral_count / pixel_count, 4),
        dark_share=round(dark_count / pixel_count, 4),
        accent_share=round(accent_count / pixel_count, 4),
        edge_density=round(edge_density, 4),
        active_cell_share=round(active_cell_share, 4),
        photo_cell_share=round(photo_cell_share, 4),
        dominant_colors=_dominant_colors(image_path),
    )


def format_candidate_summary(candidate: dict[str, Any]) -> str:
    metrics = candidate.get("metrics", {})
    metric_values = [float(value) for value in metrics.values() if isinstance(value, int | float)]
    average = sum(metric_values) / len(metric_values) if metric_values else 0.0
    lines = [
        "Screenshot aesthetic candidate generated",
        f"- design_id: {candidate.get('design_id')}",
        f"- screenshots: {len(candidate.get('source_screenshots', []))}",
        f"- average_metric_score: {average:.2f}/10",
    ]
    weakest = sorted(
        ((metric_id, float(value)) for metric_id, value in metrics.items() if isinstance(value, int | float)),
        key=lambda item: item[1],
    )[:5]
    if weakest:
        lines.append("- weakest metrics:")
        for metric_id, value in weakest:
            lines.append(f"  - {metric_id}: {value:.2f}")
    return "\n".join(lines)


def format_candidate_json(candidate: dict[str, Any]) -> str:
    return json.dumps(candidate, ensure_ascii=False, indent=2)


def _score_metrics(aggregate: dict[str, Any], brand_profile: dict[str, Any]) -> tuple[dict[str, float], dict[str, str]]:
    palette_score = _palette_score(aggregate)
    contrast_score = _contrast_score(aggregate)
    density_score = _density_score(aggregate)
    structure_score = _structure_score(aggregate)
    asset_score = _asset_score(aggregate, brand_profile)
    responsive_score = _responsive_score(aggregate)
    brand_fit_score = _brand_fit_score(aggregate, brand_profile)
    anti_keyword_score = _anti_keyword_score(aggregate, brand_profile)
    memorability_score = _memorability_score(aggregate, brand_profile)

    metrics = {
        "color_harmony": _round_score(palette_score),
        "spacing_consistency": _round_score((density_score * 0.45) + (structure_score * 0.35) + (palette_score * 0.20)),
        "typography_balance": _round_score((contrast_score * 0.48) + (density_score * 0.32) + (structure_score * 0.20)),
        "composition_order": _round_score((structure_score * 0.55) + (density_score * 0.30) + (asset_score * 0.15)),
        "hierarchy_clarity": _round_score((contrast_score * 0.42) + (structure_score * 0.36) + (density_score * 0.22)),
        "contrast_legibility": _round_score(contrast_score),
        "content_density_control": _round_score(density_score),
        "task_focus": _round_score((structure_score * 0.45) + (density_score * 0.35) + (anti_keyword_score * 0.20)),
        "keyword_alignment": _round_score(brand_fit_score),
        "tone_alignment": _round_score((brand_fit_score * 0.45) + (palette_score * 0.35) + (density_score * 0.20)),
        "domain_fit": _round_score((asset_score * 0.42) + (structure_score * 0.36) + (brand_fit_score * 0.22)),
        "anti_keyword_avoidance": _round_score(anti_keyword_score),
        "desirability": _round_score((palette_score * 0.28) + (asset_score * 0.30) + (structure_score * 0.24) + (memorability_score * 0.18)),
        "confidence_signal": _round_score((contrast_score * 0.34) + (structure_score * 0.38) + (brand_fit_score * 0.28)),
        "warmth_or_energy": _round_score((asset_score * 0.36) + (palette_score * 0.34) + (memorability_score * 0.30)),
        "responsive_fit": _round_score(responsive_score),
        "token_binding": _round_score((palette_score * 0.50) + (structure_score * 0.30) + 7.4 * 0.20),
        "accessibility_baseline": _round_score((contrast_score * 0.70) + (responsive_score * 0.30)),
        "interaction_affordance": _round_score((contrast_score * 0.36) + (structure_score * 0.44) + (density_score * 0.20)),
        "asset_completeness": _round_score(asset_score),
        "distinctiveness": _round_score((memorability_score * 0.56) + (asset_score * 0.24) + (palette_score * 0.20)),
        "reference_transformation": _round_score((structure_score * 0.40) + (anti_keyword_score * 0.32) + (palette_score * 0.28)),
        "memorability": _round_score(memorability_score),
    }

    notes = {
        metric_id: _metric_note(metric_id)
        for metric_id in DEFAULT_METRICS
    }
    brand_contract = build_brand_aesthetic_contract(brand_profile)
    for metric_id, spec in brand_contract.get("metrics", {}).items():
        metrics[metric_id] = _round_score(_score_brand_contract_metric(metric_id, spec, aggregate, brand_profile))
        notes[metric_id] = (
            f"Brand contract metric from {spec.get('source')}; automated score uses screenshot proxies "
            "and should be confirmed with semantic review."
        )
    notes["token_binding"] = "Screenshot proxy only; confirm with lint-implementation for code-level token binding."
    notes["keyword_alignment"] = "Pixel proxy plus brand keyword matching; semantic review is still recommended."
    notes["domain_fit"] = "Pixel proxy for structured product surface and visual asset evidence; does not identify domain objects semantically."
    return metrics, notes


def _score_brand_contract_metric(
    metric_id: str,
    spec: dict[str, Any],
    features: dict[str, Any],
    brand_profile: dict[str, Any],
) -> float:
    target = str(spec.get("target_value") or "").lower()
    if metric_id.startswith(("anti_keyword:", "avoid_pattern:")):
        return _score_avoidance_target(target, features)
    if metric_id.startswith(("product_primitive:", "must_include:")):
        return _score_product_target(target, features, brand_profile)
    if metric_id.startswith("accessibility_target:"):
        return (_contrast_score(features) * 0.58) + (_responsive_score(features) * 0.42)
    if metric_id.startswith("audience_need:"):
        return (_responsive_score(features) * 0.34) + (_density_score(features) * 0.30) + (_brand_fit_score(features, brand_profile) * 0.36)
    if metric_id.startswith(("brand_keyword:", "brand_tone:")):
        return _score_semantic_target(target, features, brand_profile)
    return _brand_fit_score(features, brand_profile)


def _score_semantic_target(target: str, features: dict[str, Any], brand_profile: dict[str, Any]) -> float:
    quiet_terms = {"quiet", "calm", "warm", "observational", "non-salesy", "clear", "trustworthy", "local", "situated", "차분", "조용"}
    sensory_terms = {"sensory", "texture", "place", "walkable", "local", "map", "photo", "감각", "장소", "골목"}
    analytical_terms = {"analytical", "precise", "data", "evidence", "confidence", "specific", "신뢰"}
    expressive_terms = {"distinctive", "bold", "playful", "memorable"}
    tokens = _split_terms(target)
    if tokens & quiet_terms:
        return (_palette_score(features) * 0.46) + (_density_score(features) * 0.32) + (_contrast_score(features) * 0.22)
    if tokens & sensory_terms:
        return (_asset_score(features, brand_profile) * 0.48) + (_palette_score(features) * 0.24) + (_structure_score(features) * 0.28)
    if tokens & analytical_terms:
        return (_contrast_score(features) * 0.34) + (_structure_score(features) * 0.42) + (_density_score(features) * 0.24)
    if tokens & expressive_terms:
        return _memorability_score(features, brand_profile)
    return _brand_fit_score(features, brand_profile)


def _score_avoidance_target(target: str, features: dict[str, Any]) -> float:
    tokens = _split_terms(target)
    score = 8.1
    if tokens & {"neon", "overdecorated", "glassmorphism", "화려함"}:
        score += (0.16 - min(features["saturation_mean"], 0.16)) * 6.0
        score -= max(0.0, features["edge_density"] - 0.28) * 6.0
    if tokens & {"beige-only-editorial", "tourism-brochure", "photo-influencer-feed"}:
        score += min(features["accent_share"], 0.12) * 5.0
        score += min(features["photo_cell_share"], 0.22) * 2.0
    if tokens & {"generic-map", "generic"}:
        score += min(features["active_cell_share"], 0.90) * 1.0
        score += min(features["photo_cell_share"], 0.25) * 1.5
    if tokens & {"commerce-led", "real-estate"}:
        score += _palette_score(features) * 0.10
    return _clip_score(score)


def _score_product_target(target: str, features: dict[str, Any], brand_profile: dict[str, Any]) -> float:
    tokens = _split_terms(target)
    map_terms = {"map", "pin", "place", "location", "neighborhood", "골목", "장소", "지도"}
    data_terms = {"score", "metadata", "evidence", "ontology", "graph", "confidence", "inspector", "관계", "감각"}
    control_terms = {"filter", "switcher", "segmented", "chip", "queue", "list", "card", "sheet", "form"}
    photo_terms = {"photo", "texture", "image", "visual", "사진", "텍스처"}
    if tokens & photo_terms:
        return _asset_score(features, brand_profile)
    if tokens & map_terms:
        return (_structure_score(features) * 0.44) + (_asset_score(features, brand_profile) * 0.28) + (_density_score(features) * 0.28)
    if tokens & data_terms:
        return (_structure_score(features) * 0.46) + (_contrast_score(features) * 0.34) + (_density_score(features) * 0.20)
    if tokens & control_terms:
        return (_contrast_score(features) * 0.34) + (_density_score(features) * 0.30) + (_structure_score(features) * 0.36)
    return (_structure_score(features) * 0.42) + (_asset_score(features, brand_profile) * 0.28) + (_brand_fit_score(features, brand_profile) * 0.30)


def _aggregate_features(features: list[ScreenshotFeatures]) -> dict[str, Any]:
    values = [feature.to_dict() for feature in features]
    orientations = sorted({feature.orientation for feature in features})
    widths = [feature.width for feature in features]
    heights = [feature.height for feature in features]
    return {
        "count": len(features),
        "orientations": orientations,
        "has_mobile_width": any(width <= 480 for width in widths),
        "has_desktop_width": any(width >= 900 for width in widths),
        "min_width": min(widths),
        "max_width": max(widths),
        "max_height": max(heights),
        "luminance_mean": _avg(values, "luminance_mean"),
        "luminance_std": _avg(values, "luminance_std"),
        "luminance_span": _avg(values, "luminance_span"),
        "saturation_mean": _avg(values, "saturation_mean"),
        "saturation_std": _avg(values, "saturation_std"),
        "neutral_share": _avg(values, "neutral_share"),
        "light_neutral_share": _avg(values, "light_neutral_share"),
        "dark_share": _avg(values, "dark_share"),
        "accent_share": _avg(values, "accent_share"),
        "edge_density": _avg(values, "edge_density"),
        "desktop_edge_density": _avg([item for item in values if item["orientation"] == "landscape"], "edge_density"),
        "mobile_edge_density": _avg([item for item in values if item["orientation"] == "portrait"], "edge_density"),
        "active_cell_share": _avg(values, "active_cell_share"),
        "photo_cell_share": _avg(values, "photo_cell_share"),
    }


def _palette_score(features: dict[str, Any]) -> float:
    neutral = _range_score(features["neutral_share"], 0.62, 0.94, 0.36)
    accent = _range_score(features["accent_share"], 0.02, 0.16, 0.18)
    saturation = _range_score(features["saturation_mean"], 0.035, 0.17, 0.16)
    dark_penalty = max(0.0, (features["dark_share"] - 0.22) * 4.0)
    return _clip_score((neutral * 0.38) + (accent * 0.28) + (saturation * 0.34) - dark_penalty)


def _contrast_score(features: dict[str, Any]) -> float:
    span = _range_score(features["luminance_span"], 0.70, 1.0, 0.35)
    std = _range_score(features["luminance_std"], 0.12, 0.34, 0.20)
    too_flat_penalty = 1.0 if features["luminance_std"] < 0.06 else 0.0
    return _clip_score((span * 0.48) + (std * 0.52) - too_flat_penalty)


def _density_score(features: dict[str, Any]) -> float:
    edge = _range_score(features["edge_density"], 0.08, 0.24, 0.20)
    light_surface = _range_score(features["light_neutral_share"], 0.55, 0.90, 0.24)
    active = _range_score(features["active_cell_share"], 0.42, 0.86, 0.28)
    mobile_edge = features.get("mobile_edge_density") or features["edge_density"]
    mobile_penalty = max(0.0, (mobile_edge - 0.30) * 8.0)
    return _clip_score((edge * 0.44) + (light_surface * 0.25) + (active * 0.31) - mobile_penalty)


def _structure_score(features: dict[str, Any]) -> float:
    active = _range_score(features["active_cell_share"], 0.48, 0.88, 0.28)
    edge = _range_score(features["edge_density"], 0.07, 0.22, 0.20)
    photo = _range_score(features["photo_cell_share"], 0.04, 0.34, 0.30)
    return _clip_score((active * 0.48) + (edge * 0.32) + (photo * 0.20))


def _asset_score(features: dict[str, Any], brand_profile: dict[str, Any]) -> float:
    photo_score = _range_score(features["photo_cell_share"], 0.05, 0.34, 0.30)
    visual_need = _visual_subject_need(brand_profile)
    if visual_need:
        return _clip_score((photo_score * 0.78) + (_structure_score(features) * 0.22))
    return _clip_score((photo_score * 0.35) + (_structure_score(features) * 0.65))


def _responsive_score(features: dict[str, Any]) -> float:
    coverage = 8.8 if features["has_mobile_width"] and features["has_desktop_width"] else 7.2
    density = _density_score(features)
    mobile_edge = features.get("mobile_edge_density") or 0.0
    edge_penalty = max(0.0, (mobile_edge - 0.32) * 10.0)
    return _clip_score((coverage * 0.55) + (density * 0.45) - edge_penalty)


def _brand_fit_score(features: dict[str, Any], brand_profile: dict[str, Any]) -> float:
    keywords = _profile_terms(brand_profile, "brand_keywords", "tone_of_voice", "visual_keywords")
    quiet_terms = {"quiet", "calm", "trustworthy", "observational", "local", "curated", "situated"}
    energetic_terms = {"bold", "playful", "vivid", "energetic"}
    sensory_terms = {"sensory", "place", "map", "local", "photo", "texture", "walkable"}
    quiet_match = bool(keywords & quiet_terms)
    energetic_match = bool(keywords & energetic_terms)
    sensory_match = bool(keywords & sensory_terms)

    score = 7.4
    if quiet_match:
        score += (_palette_score(features) - 7.0) * 0.45
        score += (_density_score(features) - 7.0) * 0.25
    if energetic_match:
        score += _range_score(features["accent_share"], 0.07, 0.24, 0.18) * 0.18
    if sensory_match:
        score += (_asset_score(features, brand_profile) - 7.0) * 0.40
    return _clip_score(score)


def _anti_keyword_score(features: dict[str, Any], brand_profile: dict[str, Any]) -> float:
    anti_terms = _profile_terms(brand_profile, "anti_keywords")
    score = 8.2
    if {"neon", "overdecorated", "glassmorphism"} & anti_terms:
        score += (0.16 - min(features["saturation_mean"], 0.16)) * 8.0
        score -= max(0.0, features["dark_share"] - 0.28) * 5.0
    if {"beige-only-editorial", "generic-map"} & anti_terms:
        score += (features["photo_cell_share"] * 1.2)
        score += (features["accent_share"] * 2.0)
    return _clip_score(score)


def _memorability_score(features: dict[str, Any], brand_profile: dict[str, Any]) -> float:
    asset = _asset_score(features, brand_profile)
    accent = _range_score(features["accent_share"], 0.03, 0.18, 0.20)
    structure = _structure_score(features)
    return _clip_score((asset * 0.38) + (accent * 0.22) + (structure * 0.40))


def _tile_activity(image: Image.Image, *, columns: int = 12, rows: int = 12) -> tuple[float, float]:
    width, height = image.size
    active_cells = 0
    photo_cells = 0
    total_cells = columns * rows
    for row in range(rows):
        for column in range(columns):
            box = (
                int(column * width / columns),
                int(row * height / rows),
                int((column + 1) * width / columns),
                int((row + 1) * height / rows),
            )
            crop = image.crop(box)
            pixels = list(_pixel_data(crop))
            if not pixels:
                continue
            luminances = []
            saturations = []
            for red, green, blue in pixels:
                luminances.append(_relative_luminance((red, green, blue)))
                _, saturation, _ = colorsys.rgb_to_hsv(red / 255, green / 255, blue / 255)
                saturations.append(saturation)
            luminance_std = _stddev(luminances, _mean(luminances))
            saturation_std = _stddev(saturations, _mean(saturations))
            if luminance_std > 0.035 or saturation_std > 0.035:
                active_cells += 1
            if luminance_std > 0.13 and saturation_std > 0.10:
                photo_cells += 1
    return active_cells / total_cells, photo_cells / total_cells


def _edge_density(image: Image.Image) -> float:
    gray = image.convert("L")
    edges = gray.filter(ImageFilter.FIND_EDGES)
    edge_pixels = list(_pixel_data(edges))
    if not edge_pixels:
        return 0.0
    values = [pixel if isinstance(pixel, int) else pixel[0] for pixel in edge_pixels]
    return sum(1 for value in values if value > 35) / len(values)


def _dominant_colors(path: Path) -> list[dict[str, Any]]:
    with Image.open(path) as raw_image:
        image = raw_image.convert("RGB")
        image.thumbnail((180, 180))
        quantized = image.quantize(colors=8, method=Image.Quantize.MEDIANCUT)
        palette = quantized.getpalette() or []
        counts = quantized.getcolors() or []
        total = sum(count for count, _ in counts) or 1
        colors = []
        for count, palette_index in sorted(counts, reverse=True)[:8]:
            offset = palette_index * 3
            rgb = tuple(palette[offset:offset + 3])
            if len(rgb) != 3:
                continue
            colors.append(
                {
                    "hex": "#{:02X}{:02X}{:02X}".format(*rgb),
                    "share": round(count / total, 4),
                    "luminance": round(_relative_luminance(rgb), 4),
                }
            )
        return colors


def _pixel_data(image: Image.Image):
    if hasattr(image, "get_flattened_data"):
        return image.get_flattened_data()
    return image.getdata()


def _visual_subject_need(brand_profile: dict[str, Any]) -> bool:
    terms = _profile_terms(brand_profile, "product_summary", "product_primitives", "visual_keywords")
    return bool(
        terms
        & {
            "place",
            "places",
            "map",
            "photo",
            "texture",
            "local",
            "travel",
            "product",
            "portfolio",
            "sports",
            "장소",
            "골목",
            "지도",
            "사진",
            "감각",
        }
    )


def _profile_terms(brand_profile: dict[str, Any], *keys: str) -> set[str]:
    terms: set[str] = set()
    for key in keys:
        value = brand_profile.get(key)
        if isinstance(value, str):
            terms.update(_split_terms(value))
        elif isinstance(value, list):
            for item in value:
                terms.update(_split_terms(str(item)))
    return terms


def _split_terms(value: str) -> set[str]:
    return {
        part.strip().lower()
        for part in value.replace("_", "-").replace("/", "-").replace(",", " ").split()
        if part.strip()
    }


def _metric_note(metric_id: str) -> str:
    return f"Generated from screenshot visual proxies for {metric_id}; use as a first-pass gate signal."


def _range_score(value: float, ideal_min: float, ideal_max: float, tolerance: float) -> float:
    if ideal_min <= value <= ideal_max:
        return 8.35
    if value < ideal_min:
        distance = ideal_min - value
    else:
        distance = value - ideal_max
    return _clip_score(8.35 - (distance / max(tolerance, 0.0001)) * 4.0)


def _clip_score(value: float) -> float:
    return min(9.2, max(3.0, value))


def _round_score(value: float) -> float:
    return round(_clip_score(value), 2)


def _avg(values: list[dict[str, Any]], key: str) -> float:
    numbers = [float(item[key]) for item in values if isinstance(item.get(key), int | float)]
    return round(sum(numbers) / len(numbers), 4) if numbers else 0.0


def _mean(values: list[float]) -> float:
    return sum(values) / len(values) if values else 0.0


def _stddev(values: list[float], mean: float) -> float:
    return (sum((value - mean) ** 2 for value in values) / len(values)) ** 0.5 if values else 0.0


def _relative_luminance(rgb: tuple[int, int, int]) -> float:
    def _channel(value: int) -> float:
        value = value / 255
        if value <= 0.04045:
            return value / 12.92
        return ((value + 0.055) / 1.055) ** 2.4

    red, green, blue = (_channel(channel) for channel in rgb)
    return 0.2126 * red + 0.7152 * green + 0.0722 * blue


def _orientation(width: int, height: int) -> str:
    if width == height:
        return "square"
    return "landscape" if width > height else "portrait"


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()
