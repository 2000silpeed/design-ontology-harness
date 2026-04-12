"""CSS extraction pipeline — runs var_resolver, brand_candidates, and typo_extractor.

Sits after crawler in the pipeline. Takes raw CSS (and optionally HTML)
and produces structured extraction results for synthesis.
"""

from __future__ import annotations

import json
from pathlib import Path

from .alias_layer import extract_alias_layer
from .brand_candidates import extract_brand_colors
from .typo_extractor import extract_typography
from .utils import ensure_dir, write_json
from .var_resolver import resolve_css


def run_css_extraction(css: str, html: str = "") -> dict:
    """Run all three CSS extractors on raw CSS and HTML strings.

    Returns combined extraction result:
        {
            "var_resolution": {total_vars, resolved_count, unresolved_count, resolved},
            "brand_colors": {semantic_vars, selector_role, frequency_candidates, summary},
            "typography": {scale, families, weights_used, stats},
        }
    """
    var_result = resolve_css(css)
    brand_result = extract_brand_colors(css, html)
    typo_result = extract_typography(css)
    alias_result = extract_alias_layer(var_result.get("resolved", {}))

    return {
        "var_resolution": var_result,
        "brand_colors": brand_result,
        "typography": typo_result,
        "alias_layer": alias_result,
    }


def run_css_extraction_from_files(
    css_paths: list[Path],
    html_path: Path | None = None,
) -> dict:
    """Read CSS/HTML files and run extraction."""
    css_parts: list[str] = []
    for path in css_paths:
        if path.exists():
            css_parts.append(path.read_text(encoding="utf-8", errors="replace"))
    css = "\n".join(css_parts)

    html = ""
    if html_path and html_path.exists():
        html = html_path.read_text(encoding="utf-8", errors="replace")

    return run_css_extraction(css, html)


def run_css_extraction_from_dir(css_dir: Path, html_path: Path | None = None) -> dict:
    """Read all .css files from a directory and run extraction."""
    css_paths = sorted(css_dir.glob("*.css")) if css_dir.exists() else []
    return run_css_extraction_from_files(css_paths, html_path)


def run_and_save(
    css_dir: Path,
    output_dir: Path,
    html_path: Path | None = None,
) -> dict:
    """Run extraction and save results to output_dir/css_extraction/.

    Saves:
        - resolved_tokens.json
        - brand_candidates.json
        - typography.json
        - extraction_summary.json
    """
    result = run_css_extraction_from_dir(css_dir, html_path)
    out = ensure_dir(output_dir / "css_extraction")

    write_json(out / "resolved_tokens.json", result["var_resolution"])
    write_json(out / "brand_candidates.json", result["brand_colors"])
    write_json(out / "typography.json", result["typography"])
    write_json(out / "alias_layer.json", result["alias_layer"])

    summary = {
        "var_resolution": {
            "total_vars": result["var_resolution"]["total_vars"],
            "resolved_count": result["var_resolution"]["resolved_count"],
            "unresolved_count": result["var_resolution"]["unresolved_count"],
        },
        "brand_colors": result["brand_colors"]["summary"],
        "typography": result["typography"]["stats"],
        "alias_layer": result["alias_layer"]["stats"],
    }
    write_json(out / "extraction_summary.json", summary)

    return result


def load_css_extraction(output_dir: Path) -> dict | None:
    """Load previously saved CSS extraction results from output_dir/css_extraction/."""
    extraction_dir = output_dir / "css_extraction"
    summary_path = extraction_dir / "extraction_summary.json"
    if not summary_path.exists():
        return None

    result = {}
    for key, filename in [
        ("var_resolution", "resolved_tokens.json"),
        ("brand_colors", "brand_candidates.json"),
        ("typography", "typography.json"),
        ("alias_layer", "alias_layer.json"),
    ]:
        path = extraction_dir / filename
        if path.exists():
            result[key] = json.loads(path.read_text(encoding="utf-8"))
    return result if result else None
