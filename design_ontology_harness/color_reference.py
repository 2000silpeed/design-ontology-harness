from __future__ import annotations

import re
from pathlib import Path


COLOR_HEX_RE = re.compile(r"#(?:[0-9A-Fa-f]{6}|[0-9A-Fa-f]{3})")


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


def resolve_color_reference(reference_config: dict, base_dir: Path) -> tuple[dict | None, list[str]]:
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

    if not resolved_selected and preferred_families:
        preferred_lookup = {item.lower() for item in preferred_families}
        resolved_selected = [
            color
            for color in parsed["colors"]
            if (color.get("family") or "").lower() in preferred_lookup
        ][:8]
        if not resolved_selected:
            issues.append("color_reference.preferred_families did not match any parsed family")

    summary = {
        "title": parsed["title"],
        "source_path": parsed["source_path"],
        "families": parsed["families"],
        "selected_colors": resolved_selected,
        "palette_roles": resolved_roles,
        "preferred_families": preferred_families,
        "notes": reference_config.get("notes", []),
    }
    return summary, issues
