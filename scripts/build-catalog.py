#!/usr/bin/env python3
"""Build docs/CATALOG.md from harness presets/ sources.

Walks matrix.json + each preset manifest.json + preview.md, emits a grouped
markdown catalog (axis matrix + 15 preset cards). stdlib only.

Usage:
    scripts/build-catalog.py --output docs/CATALOG.md
    scripts/build-catalog.py --output /path/to/plugin/docs/CATALOG.md
    scripts/build-catalog.py --presets-dir presets --output docs/CATALOG.md
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Optional

REPO_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_PRESETS_DIR = REPO_ROOT / "presets"
DEFAULT_OUTPUT = REPO_ROOT / "docs" / "CATALOG.md"

TIER_ORDER = {"P0": 0, "P1": 1, "P2": 2, "P3": 3}

HEX_RE = re.compile(r"`(#[0-9A-Fa-f]{3,8})`")


@dataclass
class PreviewBlock:
    summary: Optional[str]
    core_colors: dict[str, str]
    semantic_colors: dict[str, str]
    typography: dict[str, str]
    components: list[tuple[str, str]]  # (name, parts/states summary)
    cautions: list[str]


def _strip_heading(line: str) -> str:
    return line.lstrip("#").strip()


def parse_preview(text: str) -> PreviewBlock:
    lines = text.splitlines()
    summary: Optional[str] = None
    core: dict[str, str] = {}
    semantic: dict[str, str] = {}
    typography: dict[str, str] = {}
    components: list[tuple[str, str]] = []
    cautions: list[str] = []

    section: Optional[str] = None
    subsection: Optional[str] = None

    for raw in lines:
        line = raw.rstrip()
        if line.startswith("## "):
            heading = _strip_heading(line).lower()
            if "어떤 제품" in heading or "어떤 제품에 맞나" in heading:
                section = "summary"
            elif heading.startswith("color tokens"):
                section = "color"
                subsection = None
            elif heading.startswith("typography"):
                section = "typography"
            elif heading.startswith("대표 컴포넌트"):
                section = "components"
            elif heading.startswith("주의사항"):
                section = "cautions"
            else:
                section = None
            subsection = None
            continue
        if line.startswith("### "):
            subsection = _strip_heading(line).lower()
            continue

        if section == "summary" and summary is None:
            if line.startswith("- "):
                summary = line[2:].strip()
        elif section == "color":
            m = re.match(r"- (\w[\w_-]*):\s+`(#[0-9A-Fa-f]{3,8})`", line)
            if m:
                role, value = m.group(1), m.group(2)
                if subsection and subsection.startswith("semantic"):
                    semantic[role] = value
                else:
                    core[role] = value
        elif section == "typography":
            m = re.match(r"- (\w[\w_-]*):\s*(.+)", line)
            if m:
                role, value = m.group(1).strip(), m.group(2).strip()
                typography[role] = value
        elif section == "components":
            m = re.match(r"- \*\*([\w-]+)\*\*\s*—\s*(.+)", line)
            if m:
                name, rest = m.group(1).strip(), m.group(2).strip()
                components.append((name, rest))
        elif section == "cautions":
            if line.startswith("- "):
                cautions.append(line[2:].strip())

    return PreviewBlock(
        summary=summary,
        core_colors=core,
        semantic_colors=semantic,
        typography=typography,
        components=components,
        cautions=cautions,
    )


def _swatch_for_hex(hex_value: str) -> str:
    """Return a text swatch: ⬛ for dark, ⬜ for light, by perceived luminance."""
    h = hex_value.lstrip("#")
    if len(h) == 3:
        h = "".join(c * 2 for c in h)
    if len(h) < 6:
        return "◼"
    try:
        r = int(h[0:2], 16) / 255
        g = int(h[2:4], 16) / 255
        b = int(h[4:6], 16) / 255
    except ValueError:
        return "◼"
    luminance = 0.2126 * r + 0.7152 * g + 0.0722 * b
    return "⬜" if luminance >= 0.5 else "⬛"


def _load_matrix(presets_dir: Path) -> dict:
    return json.loads((presets_dir / "matrix.json").read_text(encoding="utf-8"))


def _load_preset(presets_dir: Path, preset_id: str) -> tuple[dict, PreviewBlock]:
    preset_dir = presets_dir / preset_id
    manifest = json.loads((preset_dir / "manifest.json").read_text(encoding="utf-8"))
    preview_text = (preset_dir / "preview.md").read_text(encoding="utf-8")
    preview = parse_preview(preview_text)
    return manifest, preview


def _tier_rank(entry: dict) -> tuple[int, str]:
    tier = entry.get("tier", "P3")
    return (TIER_ORDER.get(tier, 99), entry.get("id", ""))


def _format_tags(tags: list[str]) -> str:
    if not tags:
        return "_none_"
    return ", ".join(f"`{t}`" for t in tags)


def _format_core_swatch(colors: dict[str, str]) -> list[str]:
    lines: list[str] = []
    for role in ("primary", "accent", "surface_tint"):
        if role in colors:
            hex_value = colors[role]
            swatch = _swatch_for_hex(hex_value)
            lines.append(f"  - {role}: `{hex_value}` {swatch}")
    return lines


def _format_components(components: list[tuple[str, str]], limit: int = 3) -> list[str]:
    lines: list[str] = []
    for name, rest in components[:limit]:
        lines.append(f"  - `{name}` — {rest}")
    return lines


def _format_typography(typography: dict[str, str]) -> list[str]:
    lines: list[str] = []
    for role in ("heading", "body", "mono", "korean"):
        if role in typography:
            lines.append(f"  - {role}: {typography[role]}")
    return lines


def _format_locale(locale_pairings: dict) -> str:
    if not locale_pairings:
        return "_none_"
    available = sorted(locale_pairings.keys())
    parts = []
    for lang in available:
        pairing = locale_pairings[lang] or {}
        heading = pairing.get("heading_font") or "?"
        body = pairing.get("body_font") or "?"
        parts.append(f"`{lang}` (heading={heading} / body={body})")
    return ", ".join(parts)


def _rel_preset_path(preset_id: str) -> str:
    return f"../presets/{preset_id}/"


def _rel_preview_path(preset_id: str) -> str:
    return f"../presets/{preset_id}/preview.md"


def _rel_sources_path(preset_id: str) -> str:
    return f"../presets/{preset_id}/sources.json"


def _load_sources(presets_dir: Path, preset_id: str) -> dict | None:
    """Load sources.json for a preset if present (Phase 15-9)."""
    path = presets_dir / preset_id / "sources.json"
    if not path.exists():
        return None
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return None


def _render_credits_section(presets_dir: Path, presets: list[dict]) -> list[str]:
    """Render the `## KB Sources & Credits` section (Phase 15-9-6).

    Groups seeds by URL so references shared across presets are aggregated.
    Appends a font-license subsection at the bottom.
    """

    lines: list[str] = []
    lines.append("## KB Sources & Credits")
    lines.append("")
    lines.append(
        "각 프리셋은 공개 디자인 시스템 / 매거진 / 커머스 레퍼런스를 KB 시드로 기록합니다. "
        "아래는 `presets/<id>/sources.json` 에서 집계한 원본 참조 링크입니다."
    )
    lines.append("")

    # Aggregate URL → {title, kind, notes?, presets[]}
    aggregated: dict[str, dict] = {}
    preset_summaries: list[tuple[str, list[dict]]] = []
    for entry in sorted(presets, key=lambda e: e.get("id", "")):
        preset_id = entry.get("id", "")
        sources = _load_sources(presets_dir, preset_id) or {}
        seeds = list(sources.get("seeds") or [])
        preset_summaries.append((preset_id, seeds))
        for seed in seeds:
            url = (seed.get("url") or "").strip()
            if not url:
                continue
            record = aggregated.setdefault(
                url,
                {
                    "url": url,
                    "title": seed.get("title") or url,
                    "kind": seed.get("kind") or "article",
                    "presets": [],
                },
            )
            if preset_id not in record["presets"]:
                record["presets"].append(preset_id)

    # Per-preset breakdown table.
    lines.append("### Per-preset seed index")
    lines.append("")
    if not preset_summaries:
        lines.append("_No `sources.json` found — run `uv run design-ontology build-sources --all` in the harness repo._")
        lines.append("")
    else:
        lines.append("| Preset | Seeds | Kinds |")
        lines.append("|---|---|---|")
        for preset_id, seeds in preset_summaries:
            if not seeds:
                lines.append(
                    f"| [`{preset_id}`]({_rel_sources_path(preset_id)}) | 0 | _none — needs seeds_ |"
                )
                continue
            kind_counts: dict[str, int] = {}
            for s in seeds:
                k = s.get("kind") or "article"
                kind_counts[k] = kind_counts.get(k, 0) + 1
            kind_summary = " · ".join(f"{k}={v}" for k, v in sorted(kind_counts.items()))
            lines.append(
                f"| [`{preset_id}`]({_rel_sources_path(preset_id)}) | {len(seeds)} | {kind_summary} |"
            )
        lines.append("")

    # Aggregated sources (URL → presets that cite it)
    lines.append("### Aggregated references")
    lines.append("")
    if not aggregated:
        lines.append("_No seeds recorded yet._")
        lines.append("")
    else:
        lines.append("| Source | Kind | Referenced by |")
        lines.append("|---|---|---|")
        # Sort by multi-cite first, then alphabetical
        items = sorted(
            aggregated.values(),
            key=lambda rec: (-len(rec["presets"]), rec["title"].lower()),
        )
        for rec in items:
            presets_cell = (
                f"{len(rec['presets'])}+ presets"
                if len(rec["presets"]) >= 2
                else ", ".join(f"`{p}`" for p in rec["presets"])
            )
            if len(rec["presets"]) >= 2:
                preset_tags = ", ".join(f"`{p}`" for p in rec["presets"])
                presets_cell = f"{presets_cell} — {preset_tags}"
            lines.append(
                f"| [{rec['title']}]({rec['url']}) | `{rec['kind']}` | {presets_cell} |"
            )
        lines.append("")

    # Font license credits
    lines.append("### Bundled fonts")
    lines.append("")
    lines.append(
        "- **Pretendard Variable** — SIL OFL 1.1 © Kil Hyung-jin "
        "([orioncactus/pretendard](https://github.com/orioncactus/pretendard) · "
        "[OFL text](https://scripts.sil.org/OFL)) — runtime fetch via "
        "`scripts/fetch-pretendard.mjs`, not bundled in the repo. "
        "Redistribution must preserve the OFL notice ([`LICENSE-FONTS`](../LICENSE-FONTS))."
    )
    lines.append(
        "- **Inter** — SIL OFL 1.1 (Google Fonts / [rsms/inter](https://rsms.me/inter/)) — default Latin heading/body."
    )
    lines.append(
        "- **JetBrains Mono** — SIL OFL 1.1 ([JetBrains/JetBrainsMono](https://github.com/JetBrains/JetBrainsMono)) — mono pairing when selected."
    )
    lines.append("")

    return lines


def render_catalog(presets_dir: Path) -> str:
    matrix = _load_matrix(presets_dir)
    presets = sorted(matrix.get("presets", []), key=_tier_rank)

    app_modes = [m["id"] for m in matrix.get("app_modes", [])]
    brand_tones = [t["id"] for t in matrix.get("brand_tones", [])]

    by_axis: dict[tuple[str, str], list[dict]] = {}
    for entry in presets:
        key = (entry["app_mode"], entry["brand_tone"])
        by_axis.setdefault(key, []).append(entry)

    tier_counts: dict[str, int] = {}
    for entry in presets:
        tier_counts[entry.get("tier", "P?")] = tier_counts.get(entry.get("tier", "P?"), 0) + 1

    all_tags: set[str] = set()
    for entry in presets:
        for tag in entry.get("tags", []):
            all_tags.add(tag)

    lines: list[str] = []
    append = lines.append

    append("# Preset Catalog")
    append("")
    append(
        "> Auto-generated from `presets/matrix.json` + each preset's `manifest.json` "
        "+ `preview.md`. Do not edit by hand. Regenerate with "
        "`python3 scripts/build-catalog.py --output docs/CATALOG.md` in the harness repo."
    )
    append("")
    append(
        "The design-ontology plugin ships with a curated catalog of presets, each a complete "
        "design-system bundle (tokens, components, preview, adapter hints). Pick one, install "
        "it with `/design-start`, or browse the axis matrix below."
    )
    append("")

    # Overview counts
    append("## At a glance")
    append("")
    append(f"- Total presets: **{len(presets)}**")
    tier_parts = [f"{tier}={tier_counts.get(tier, 0)}" for tier in ("P0", "P1", "P2", "P3")]
    append(f"- Tiers: {' · '.join(tier_parts)}")
    append(f"- Axes: app_mode (×{len(app_modes)}) × brand_tone (×{len(brand_tones)})")
    append(f"- Tags in use: {_format_tags(sorted(all_tags))}")
    append("")

    # Filter guide
    append("## Filter axes")
    append("")
    append(
        "Use `/design-start` (4-question flow or natural-language one-liner) to pick a preset. "
        "Internally the matcher scores on these axes:"
    )
    append("")
    append("| Axis | Cardinality | Source |")
    append("|------|-------------|--------|")
    append(f"| `app_mode` | {len(app_modes)} ({', '.join(app_modes)}) | matrix.json |")
    append(f"| `brand_tone` | {len(brand_tones)} ({', '.join(brand_tones)}) | matrix.json |")
    append("| `color_mode` | `light` / `dark` / `both` | manifest.color_modes |")
    append("| `tier` | `P0` / `P1` / `P2` / `P3` | manifest.tier |")
    append("| `tags` | open set (`ko`, `saas`, `fintech`, ...) | manifest.tags |")
    append("")

    # Matrix view
    append("## Matrix — app_mode × brand_tone")
    append("")
    header = "| app_mode \\ brand_tone | " + " | ".join(brand_tones) + " |"
    divider = "|" + "---|" * (len(brand_tones) + 1)
    append(header)
    append(divider)
    for app_mode in app_modes:
        row_cells = [f"**{app_mode}**"]
        for tone in brand_tones:
            entries = by_axis.get((app_mode, tone), [])
            if not entries:
                row_cells.append("—")
            else:
                cell_parts = []
                for entry in entries:
                    cell_parts.append(
                        f"[{entry['id']}](#{entry['id'].replace('--', '--')}) · `{entry.get('tier', 'P?')}`"
                    )
                row_cells.append("<br>".join(cell_parts))
        append("| " + " | ".join(row_cells) + " |")
    append("")

    # Tier-grouped cards
    append("## Cards")
    append("")
    append(
        "Each card is derived from the preset's `manifest.json` + `preview.md`. "
        "`Core HEX` are the brand palette primaries (derived via `brand_profile.color_reference`). "
        "`⬛` / `⬜` swatches reflect perceived luminance."
    )
    append("")

    for tier in ("P0", "P1", "P2", "P3"):
        tier_group = [e for e in presets if e.get("tier") == tier]
        if not tier_group:
            continue
        append(f"### {tier} · {len(tier_group)} preset(s)")
        append("")

        for entry in tier_group:
            preset_id = entry["id"]
            manifest, preview = _load_preset(presets_dir, preset_id)

            append(f"#### `{preset_id}`")
            append("")
            description = entry.get("description") or manifest.get("description") or ""
            if description:
                append(f"> {description}")
                append("")

            append(
                "- **tier**: `{tier}` · **app_mode**: `{am}` · **brand_tone**: `{bt}` · "
                "**default_color_mode**: `{dcm}`".format(
                    tier=entry.get("tier", "P?"),
                    am=entry["app_mode"],
                    bt=entry["brand_tone"],
                    dcm=entry.get("default_color_mode", "?"),
                )
            )
            color_modes = ", ".join(f"`{c}`" for c in entry.get("color_modes", [])) or "_none_"
            append(f"- **color_modes**: {color_modes}")
            append(f"- **tags**: {_format_tags(entry.get('tags', []))}")
            append(
                "- **source_project**: `{sp}` · **owner**: `{ow}`".format(
                    sp=entry.get("source_project", "?"),
                    ow=manifest.get("owner", entry.get("owner", "?")),
                )
            )

            if preview.core_colors:
                append("- **Core HEX**:")
                for line in _format_core_swatch(preview.core_colors):
                    append(line)
            else:
                append(
                    "- **Core HEX**: _color_reference not configured — set "
                    "`brand_profile.color_reference` in the source project to populate_"
                )

            if preview.typography:
                append("- **Typography**:")
                for line in _format_typography(preview.typography):
                    append(line)

            append(f"- **locale_pairings**: {_format_locale(entry.get('locale_pairings', {}))}")

            if preview.components:
                append("- **Representative components** (top 3):")
                for line in _format_components(preview.components, limit=3):
                    append(line)

            if preview.summary:
                append(f"- **추천 용도**: {preview.summary}")

            if preview.cautions:
                append("- **주의사항**:")
                for caution in preview.cautions[:2]:
                    append(f"  - {caution}")

            append(
                "- **links**: [preview.md]({preview_path}) · [preset dir]({preset_path})".format(
                    preview_path=_rel_preview_path(preset_id),
                    preset_path=_rel_preset_path(preset_id),
                )
            )
            append("")

    # Credits section (Phase 15-9-6)
    lines.extend(_render_credits_section(presets_dir, presets))

    return "\n".join(lines).rstrip() + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--presets-dir",
        default=str(DEFAULT_PRESETS_DIR),
        help="Path to harness presets/ (default: %(default)s)",
    )
    parser.add_argument(
        "--output",
        default=str(DEFAULT_OUTPUT),
        help="Output markdown path (default: %(default)s)",
    )
    args = parser.parse_args()

    presets_dir = Path(args.presets_dir).resolve()
    output_path = Path(args.output).resolve()

    if not presets_dir.is_dir():
        print(f"error: presets-dir not a directory: {presets_dir}", file=sys.stderr)
        return 2
    matrix_path = presets_dir / "matrix.json"
    if not matrix_path.exists():
        print(f"error: {matrix_path} not found", file=sys.stderr)
        return 2

    catalog_md = render_catalog(presets_dir)

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(catalog_md, encoding="utf-8")
    preset_count = len(_load_matrix(presets_dir).get("presets", []))
    print(f"[build-catalog] wrote {output_path} ({preset_count} presets)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
