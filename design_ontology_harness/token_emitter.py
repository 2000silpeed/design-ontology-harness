"""Project-local design token emission.

``run-project`` already produces a diverse, per-project palette and font
system inside ``build/system/blueprint``, but mockup implementations kept
ignoring those artifacts and re-inventing colors and fonts by hand — which is
exactly where the repeated default aesthetic came from.

``emit_project_tokens`` closes that gap: it renders the blueprint's active
palette, semantic roles, font system, radius, and spacing scale into
``<project>/design-system/tokens.css`` as ``--ds-*`` CSS variables. The
mockup HTML links this file and consumes only ``var(--ds-*)`` values, so
``lint-implementation`` can enforce the binding.
"""

from __future__ import annotations

import json
import re
from pathlib import Path

from .adapters.base import (
    DS_BLOCK_END,
    DS_BLOCK_START,
    PresetBundle,
    _ensure_base_roles,
    _extract_semantic_roles,
    css_var_declarations,
)

SANS_FALLBACK = 'system-ui, -apple-system, "Segoe UI", sans-serif'
SERIF_FALLBACK = 'ui-serif, Georgia, serif'
MONO_FALLBACK = 'ui-monospace, SFMono-Regular, Menlo, monospace'

_RADIUS_BY_BIAS = {
    "low": {"sm": 2, "md": 4, "lg": 8, "xl": 12},
    "medium": {"sm": 4, "md": 8, "lg": 12, "xl": 16},
    "high": {"sm": 6, "md": 10, "lg": 16, "xl": 24},
}


def _slug(value: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-")


def _read_json(path: Path) -> dict:
    if not path.exists():
        return {}
    return json.loads(path.read_text(encoding="utf-8"))


def _hex_saturation_lightness(value: str) -> tuple[float, float]:
    import colorsys

    raw = value.lstrip("#")
    r, g, b = (int(raw[i : i + 2], 16) / 255.0 for i in (0, 2, 4))
    _, l, s = colorsys.rgb_to_hls(r, g, b)
    return s, l


def _brand_role_overrides(active_roles: dict) -> dict[str, str]:
    """Derive primary/accent/canvas/border from project palette role names.

    Project blueprints often name roles by product meaning (anchor_surface,
    fresh_accent, quiet_background) instead of the standard semantic keys, so
    without this the emitted --ds-color-primary falls back to a generic blue
    that no blueprint actually chose.
    """

    named: dict[str, str] = {}
    colored: list[tuple[str, str, float, float]] = []
    for role, entry in active_roles.items():
        hex_value = entry.get("hex") if isinstance(entry, dict) else entry
        if not (isinstance(hex_value, str) and hex_value.startswith("#") and len(hex_value) == 7):
            continue
        s, l = _hex_saturation_lightness(hex_value)
        colored.append((role.lower(), hex_value.upper(), s, l))

    # achromatic-photographic chrome strategy: role names are exact
    chrome_map = {
        "chrome_ink": ("ink", "primary", "link"),
        "chrome_paper": ("surface", "surface-elevated"),
        "chrome_canvas": ("canvas",),
        "chrome_line": ("border",),
        "chrome_muted": ("ink-muted",),
        "restrained_accent": ("accent",),
    }
    if any(role in chrome_map for role, *_ in colored):
        for role, hex_value, _, _ in colored:
            for token in chrome_map.get(role, ()):
                named.setdefault(token, hex_value)
        return named

    for role, hex_value, _, l in colored:
        if "primary" in role or "anchor" in role:
            named.setdefault("primary", hex_value)
        elif "accent" in role:
            named.setdefault("accent", hex_value)
        elif "background" in role or "canvas" in role:
            if l >= 0.6:
                named.setdefault("canvas", hex_value)
        elif "border" in role:
            named.setdefault("border", hex_value)

    saturated = sorted(
        (item for item in colored if item[2] >= 0.15 and 0.12 <= item[3] <= 0.8),
        key=lambda item: item[2],
        reverse=True,
    )
    for _, hex_value, _, _ in saturated:
        if "primary" not in named:
            named["primary"] = hex_value
        elif "accent" not in named and hex_value != named["primary"]:
            named["accent"] = hex_value
    if "primary" in named:
        named.setdefault("link", named["primary"])
    return named


def _font_stack(entry: dict | None, *, fallback: str) -> str | None:
    if not isinstance(entry, dict):
        return None
    name = entry.get("name")
    if not name:
        return None
    family = (entry.get("family") or "").lower()
    chain = SERIF_FALLBACK if "serif" in family and "sans" not in family else fallback
    return f'"{name}", {chain}'


def emit_project_tokens(
    project_dir: Path,
    *,
    output_path: Path | None = None,
) -> Path:
    project_dir = project_dir.resolve()
    blueprint_dir = project_dir / "build" / "system" / "blueprint"
    blueprint = _read_json(blueprint_dir / "design_system_blueprint.json")
    token_schema = _read_json(blueprint_dir / "token_schema.json")
    brand_profile = _read_json(project_dir / "brand_profile.json")
    if not blueprint and not token_schema:
        raise FileNotFoundError(
            f"No blueprint artifacts under {blueprint_dir}. Run "
            "`design-ontology run-project --project-dir ...` first."
        )

    bundle = PresetBundle(
        preset_dir=project_dir,
        manifest={"id": project_dir.name},
        blueprint=blueprint,
        token_schema=token_schema,
        component_specs={},
        brand_profile=brand_profile,
    )
    categories_early = token_schema.get("categories") or {}
    active_roles_early = (
        ((categories_early.get("color") or {}).get("reference_palette") or {})
        .get("active_palette", {})
        .get("roles")
        or {}
    )
    semantic_tokens = _extract_semantic_roles(bundle)
    chrome_active = any(str(role).startswith("chrome_") for role in active_roles_early)
    for role, hex_value in _brand_role_overrides(active_roles_early).items():
        if chrome_active:
            # chrome strategy는 팔레트 파이프라인의 최종 결정 — 구 semantic role을 덮는다
            semantic_tokens[role] = hex_value
        else:
            semantic_tokens.setdefault(role, hex_value)
    if chrome_active:
        # 무채색 크롬에서 파생되는 나머지 역할도 정렬
        ink = semantic_tokens.get("ink", "#141414")
        semantic_tokens.setdefault("ink-subtle", semantic_tokens.get("ink-muted", "#737373"))
        semantic_tokens["ink-inverse"] = "#FFFFFF"
        semantic_tokens["surface-elevated"] = semantic_tokens.get("surface", "#FFFFFF")
        semantic_tokens["surface-muted"] = "#F5F5F5"
        semantic_tokens["surface-tint"] = "#F0F0F0"
        semantic_tokens["border-strong"] = "#C9C9C9"
        semantic_tokens["link"] = ink
    semantic_tokens = _ensure_base_roles(semantic_tokens)

    lines: list[str] = []
    lines.append(f"/* project: {project_dir.name} — generated by design-ontology emit-tokens */")
    lines.append("/* 이 파일이 색/서체/라운딩의 단일 진실 소스입니다. 구현 CSS는 var(--ds-*)만 사용하세요. */")
    lines.append("")
    lines.append(":root {")

    lines.append("  /* semantic roles */")
    lines.extend(css_var_declarations(semantic_tokens))

    categories = token_schema.get("categories") or {}
    reference_palette = (
        (categories.get("color") or {}).get("reference_palette") or {}
    )
    active_roles = (reference_palette.get("active_palette") or {}).get("roles") or {}
    if active_roles:
        lines.append("")
        lines.append("  /* project palette roles (blueprint active palette) */")
        for role, entry in sorted(active_roles.items()):
            hex_value = entry.get("hex") if isinstance(entry, dict) else entry
            if isinstance(hex_value, str) and hex_value.startswith("#"):
                lines.append(f"  --ds-color-brand-{_slug(role)}: {hex_value.upper()};")

    supporting = (
        (reference_palette.get("expanded_palette") or {}).get("supporting_colors") or []
    )
    if supporting:
        lines.append("")
        lines.append("  /* supporting colors */")
        for entry in supporting[:10]:
            name = entry.get("name")
            hex_value = entry.get("hex")
            if name and isinstance(hex_value, str) and hex_value.startswith("#"):
                lines.append(f"  --ds-color-support-{_slug(name)}: {hex_value.upper()};")

    font_system = blueprint.get("font_system") or {}
    heading_stack = _font_stack(font_system.get("heading"), fallback=SANS_FALLBACK)
    display_stack = _font_stack(font_system.get("display"), fallback=SERIF_FALLBACK)
    body_stack = _font_stack(font_system.get("body"), fallback=SANS_FALLBACK)
    korean_stack = _font_stack(font_system.get("korean"), fallback=SANS_FALLBACK)
    mono_stack = _font_stack(font_system.get("mono"), fallback=MONO_FALLBACK)
    lines.append("")
    lines.append("  /* typography (blueprint font_system) */")
    if display_stack:
        lines.append(f"  --ds-font-display: {display_stack};")
    if heading_stack:
        lines.append(f"  --ds-font-heading: {heading_stack};")
    if body_stack:
        lines.append(f"  --ds-font-body: {body_stack};")
    if korean_stack:
        lines.append(f"  --ds-font-ko: {korean_stack};")
    if mono_stack:
        lines.append(f"  --ds-font-mono: {mono_stack};")

    radius = categories.get("radius") or {}
    bias = radius.get("visual_corner_bias") or "medium"
    radius_map = _RADIUS_BY_BIAS.get(bias, _RADIUS_BY_BIAS["medium"])
    lines.append("")
    lines.append(f"  /* radius (corner bias: {bias}) */")
    lines.append("  --ds-radius-none: 0;")
    for key, value in radius_map.items():
        lines.append(f"  --ds-radius-{key}: {value}px;")
    lines.append("  --ds-radius-pill: 999px;")

    spacing_scale = (categories.get("spacing") or {}).get("scale") or []
    if spacing_scale:
        lines.append("")
        lines.append("  /* spacing scale */")
        for index, value in enumerate(spacing_scale):
            lines.append(f"  --ds-space-{index}: {value}px;")

    lines.append("}")

    body = "\n".join(lines)
    content = f"{DS_BLOCK_START}\n{body}\n{DS_BLOCK_END}\n"

    target = output_path or (project_dir / "design-system" / "tokens.css")
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(content, encoding="utf-8")
    return target
