#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import html
import json
import re
from collections import Counter, defaultdict
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any
from urllib.parse import urljoin, urlparse

import httpx
from bs4 import BeautifulSoup


BASE_URL = "https://vercel.com"
GEIST_INDEX_URL = "https://vercel.com/geist/introduction"

FOUNDATION_SLUGS = {"introduction", "colors", "typography", "materials"}
ASSET_SLUGS = {"brands", "geistcn-icons"}

FAMILY_BY_SLUG = {
    "avatar": "identity",
    "badge": "feedback",
    "banner": "feedback",
    "book": "content",
    "breadcrumbs": "navigation",
    "browser": "content",
    "button": "action",
    "calendar": "input",
    "card": "surface",
    "checkbox": "input",
    "choicebox": "input",
    "clearable-input": "input",
    "code": "content",
    "code-block": "content",
    "collapse": "overlay",
    "combobox": "input",
    "command-menu": "overlay",
    "context-card": "surface",
    "context-menu": "overlay",
    "copy-button": "action",
    "description": "content",
    "destructive-action-modal": "overlay",
    "dots-menu": "action",
    "drawer": "overlay",
    "empty-state": "feedback",
    "entity": "identity",
    "error": "feedback",
    "error-card": "feedback",
    "feedback": "feedback",
    "fieldset": "form",
    "file-tree": "content",
    "gauge": "data-display",
    "grid": "layout",
    "input": "input",
    "keyboard-input": "input",
    "label": "form",
    "load-more-button": "action",
    "loading-dots": "feedback",
    "menu": "navigation",
    "middle-truncate": "content",
    "modal": "overlay",
    "multi-select": "input",
    "note": "feedback",
    "pagination": "navigation",
    "phone": "content",
    "progress": "feedback",
    "project-banner": "feedback",
    "radio": "input",
    "relative-time-card": "surface",
    "scroller": "navigation",
    "search-input": "input",
    "select": "input",
    "separator": "layout",
    "sheet": "overlay",
    "show-more": "content",
    "skeleton": "feedback",
    "slider": "input",
    "snippet": "content",
    "spinner": "feedback",
    "split-button": "action",
    "status-dot": "feedback",
    "switch": "input",
    "table": "data-display",
    "tabs": "navigation",
    "text-with-copy-button": "action",
    "textarea": "input",
    "theme-switcher": "input",
    "toast": "feedback",
    "toggle": "input",
    "tooltip": "overlay",
    "video": "content",
}

DEFAULT_STATES_BY_FAMILY = {
    "action": ["default", "hover", "active", "disabled", "loading", "focus"],
    "input": ["default", "hover", "focus", "disabled", "error", "selected"],
    "form": ["default", "focus", "disabled", "error"],
    "feedback": ["info", "success", "warning", "error", "loading"],
    "navigation": ["default", "hover", "active", "focus", "disabled"],
    "overlay": ["closed", "opening", "open", "dismissed"],
    "surface": ["default", "hover", "selected", "disabled"],
    "content": ["default", "hover", "selected"],
    "data-display": ["default", "loading", "empty", "error", "selected"],
    "identity": ["default", "loading", "empty"],
    "layout": ["default", "responsive"],
}


@dataclass(frozen=True)
class PageLink:
    slug: str
    title: str
    href: str
    url: str
    kind: str


def utc_now_iso() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds").replace("+00:00", "Z")


def write_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def write_text(path: Path, payload: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(payload.rstrip() + "\n", encoding="utf-8")


def slug_from_href(href: str) -> str:
    path = urlparse(href).path.rstrip("/")
    return path.split("/")[-1] if path else "geist"


def normalize_href(href: str) -> str | None:
    clean = href.split("#", 1)[0].rstrip("/")
    if clean in {"", "/geist"}:
        return None
    if not clean.startswith("/geist/"):
        return None
    return clean


def clean_text(value: str) -> str:
    return " ".join(html.unescape(value).split())


def page_kind(slug: str) -> str:
    if slug in FOUNDATION_SLUGS:
        return "foundation"
    if slug in ASSET_SLUGS:
        return "asset"
    return "component"


def extract_page_links(index_html: str) -> list[PageLink]:
    soup = BeautifulSoup(index_html, "html.parser")
    by_href: dict[str, str] = {}
    for anchor in soup.find_all("a", href=True):
        href = normalize_href(str(anchor["href"]))
        if not href:
            continue
        if href in by_href:
            continue
        label = clean_text(anchor.get_text(" ", strip=True))
        slug = slug_from_href(href)
        title = label or title_from_slug(slug)
        by_href[href] = title

    links: list[PageLink] = []
    for href, title in by_href.items():
        slug = slug_from_href(href)
        links.append(
            PageLink(
                slug=slug,
                title=title_from_slug(slug) if title.lower().startswith("npx ") else title,
                href=href,
                url=urljoin(BASE_URL, href),
                kind=page_kind(slug),
            )
        )
    return links


def title_from_slug(slug: str) -> str:
    exceptions = {
        "geistcn-icons": "Geist Icons",
        "middle-truncate": "MiddleTruncate",
    }
    if slug in exceptions:
        return exceptions[slug]
    return " ".join(part.capitalize() for part in slug.split("-"))


def meta_content(soup: BeautifulSoup, name: str) -> str:
    tag = soup.find("meta", attrs={"name": name})
    return clean_text(str(tag.get("content", ""))) if tag else ""


def canonical_url(soup: BeautifulSoup, fallback: str) -> str:
    tag = soup.find("link", rel="canonical")
    href = str(tag.get("href", "")) if tag else ""
    return href or fallback


def dedupe(values: list[str]) -> list[str]:
    seen: set[str] = set()
    result: list[str] = []
    for value in values:
        if value and value not in seen:
            seen.add(value)
            result.append(value)
    return result


def normalized_raw_code(raw: str) -> str:
    return (
        raw.replace("\\u003c", "<")
        .replace("\\u003e", ">")
        .replace("\\u0026", "&")
        .replace("\\n", "\n")
        .replace("\\t", "\t")
    )


def extract_raw_code_blocks(page_html: str) -> list[str]:
    blocks = re.findall(r"__rawString__:`(.*?)`", page_html, flags=re.DOTALL)
    return [normalized_raw_code(block) for block in blocks]


def extract_symbol_metadata(code_blocks: list[str]) -> dict[str, Any]:
    imports: list[str] = []
    import_sources: list[str] = []
    jsx_tags: list[str] = []
    prop_names: list[str] = []

    for block in code_blocks:
        for match in re.finditer(r"import\s+\{([^}]+)\}\s+from\s+['\"]([^'\"]+)['\"]", block):
            symbols = [clean_text(part.split(" as ", 1)[0]) for part in match.group(1).split(",")]
            imports.extend(symbol for symbol in symbols if symbol)
            import_sources.append(match.group(2))
        for tag in re.findall(r"<([A-Z][A-Za-z0-9.]*)\b", block):
            jsx_tags.append(tag)
        for prop in re.findall(r"\s([A-Za-z][A-Za-z0-9_-]*)=", block):
            if prop not in {"className", "style", "children"}:
                prop_names.append(prop)

    return {
        "code_example_count": len(code_blocks),
        "import_symbols": dedupe(imports),
        "import_sources": dedupe(import_sources),
        "jsx_tags": dedupe(jsx_tags),
        "prop_names": dedupe(prop_names),
    }


def extract_token_refs(page_html: str) -> dict[str, Any]:
    css_vars = sorted(set(re.findall(r"--[a-zA-Z0-9_-]+", page_html)))
    geist_data_attrs = sorted(set(re.findall(r"data-geist-[a-zA-Z0-9_-]+", page_html)))
    return {
        "css_var_count": len(css_vars),
        "css_vars": css_vars[:80],
        "geist_data_attrs": geist_data_attrs[:40],
    }


def extract_page(
    requested_url: str,
    final_url: str,
    response_html: str,
    fallback_title: str,
    slug: str,
    kind: str,
) -> dict[str, Any]:
    soup = BeautifulSoup(response_html, "html.parser")
    h1 = soup.find("h1")
    title_tag = soup.find("title")
    headings = []
    for heading in soup.find_all(["h2", "h3"]):
        text = clean_text(heading.get_text(" ", strip=True))
        if text:
            headings.append({"level": heading.name, "text": text})
    paragraphs = [
        clean_text(p.get_text(" ", strip=True))
        for p in soup.find_all("p")
        if clean_text(p.get_text(" ", strip=True))
    ]
    description = meta_content(soup, "description")
    lead = description or (paragraphs[0] if paragraphs else "")
    code_blocks = extract_raw_code_blocks(response_html)
    symbol_metadata = extract_symbol_metadata(code_blocks)

    title = clean_text(h1.get_text(" ", strip=True)) if h1 else ""
    if not title and title_tag:
        title = clean_text(title_tag.get_text(" ", strip=True))
    title = title or fallback_title

    access_terms = sorted(set(re.findall(r"\b(?:aria-[a-z-]+|role|keyboard|focus|screen-reader|assistive)\b", response_html, re.I)))
    return {
        "schema_version": "geist-reference-page/v1",
        "slug": slug,
        "kind": kind,
        "title": title,
        "url": requested_url,
        "final_url": final_url,
        "canonical_url": canonical_url(soup, final_url),
        "redirected": requested_url.rstrip("/") != final_url.rstrip("/"),
        "description": lead,
        "source_hash": "sha256:" + hashlib.sha256(response_html.encode("utf-8")).hexdigest(),
        "body_text_length": len(soup.get_text(" ", strip=True)),
        "sections": dedupe_headings(headings),
        "section_count": len(dedupe_headings(headings)),
        "symbol_metadata": symbol_metadata,
        "token_refs": extract_token_refs(response_html),
        "accessibility_terms": access_terms[:40],
        "absorption_policy": absorption_policy(),
    }


def dedupe_headings(headings: list[dict[str, str]]) -> list[dict[str, str]]:
    seen: set[tuple[str, str]] = set()
    result: list[dict[str, str]] = []
    for heading in headings:
        key = (heading["level"], heading["text"])
        if key in seen:
            continue
        seen.add(key)
        result.append(heading)
    return result


def absorption_policy() -> dict[str, Any]:
    return {
        "allowed": [
            "component names",
            "component taxonomy",
            "state coverage hints",
            "section headings",
            "import and JSX symbol references",
            "token identifiers",
            "accessibility and interaction evidence labels",
        ],
        "denied": [
            "verbatim product copy beyond short labels",
            "brand logos or protected imagery",
            "unlicensed implementation source code",
            "full documentation text",
            "Vercel-specific IA as product IA",
        ],
        "rule": "Store structured reference metadata for local reimplementation; keep source URLs as evidence.",
    }


def component_entry(page: dict[str, Any]) -> dict[str, Any]:
    family = FAMILY_BY_SLUG.get(page["slug"], "component")
    symbols = page["symbol_metadata"]
    return {
        "slug": page["slug"],
        "name": page["title"],
        "family": family,
        "url": page["url"],
        "description": page["description"],
        "sections": [section["text"] for section in page["sections"]],
        "states_required": DEFAULT_STATES_BY_FAMILY.get(family, ["default"]),
        "import_symbols": symbols["import_symbols"],
        "jsx_tags": symbols["jsx_tags"],
        "prop_names": symbols["prop_names"],
        "token_refs_count": page["token_refs"]["css_var_count"],
        "code_example_count": symbols["code_example_count"],
        "absorption": "metadata-only",
    }


def build_component_inventory(components: list[dict[str, Any]]) -> dict[str, Any]:
    grouped: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for component in components:
        grouped[component["family"]].append(component)

    priority_order = {
        "action": "high",
        "input": "high",
        "feedback": "high",
        "navigation": "high",
        "overlay": "high",
        "surface": "medium",
        "data-display": "medium",
        "content": "medium",
        "form": "medium",
        "identity": "medium",
        "layout": "medium",
    }
    families = []
    for family in sorted(grouped):
        entries = sorted(grouped[family], key=lambda item: item["name"].lower())
        families.append(
            {
                "family": family,
                "priority": priority_order.get(family, "medium"),
                "required_states": DEFAULT_STATES_BY_FAMILY.get(family, ["default"]),
                "components": [entry["slug"] for entry in entries],
                "source": "https://vercel.com/geist/introduction",
                "visual_reference_signals": [
                    {
                        "id": f"geist-{family}-metadata",
                        "label": f"Geist {family} component metadata",
                        "confidence": 0.95,
                        "evidence": [
                            f"{len(entries)} pages",
                            "public docs nav",
                            "metadata-only extraction",
                        ],
                    }
                ],
            }
        )

    return {
        "schema_version": "geist-component-inventory/v1",
        "source": "https://vercel.com/geist/introduction",
        "component_count": len(components),
        "families": families,
    }


def build_component_specs(components: list[dict[str, Any]]) -> dict[str, Any]:
    families = sorted({component["family"] for component in components})
    specs = []
    for component in sorted(components, key=lambda item: item["name"].lower()):
        specs.append(
            {
                "name": component["slug"],
                "display_name": component["name"],
                "family": component["family"],
                "role": component["description"],
                "source_url": component["url"],
                "source_pattern": "geist-public-docs-metadata",
                "anatomy": {
                    "parts": component["jsx_tags"][:12] or [component["name"]],
                    "states": component["states_required"],
                    "sections": component["sections"],
                },
                "tokens": {
                    "token_ref_count": component["token_refs_count"],
                    "token_source": "page-level CSS custom property references",
                },
                "api_surface": {
                    "import_symbols": component["import_symbols"],
                    "jsx_tags": component["jsx_tags"],
                    "prop_names": component["prop_names"],
                    "code_example_count": component["code_example_count"],
                    "note": "Identifiers only; implementation source is not vendored.",
                },
                "accessibility": [
                    "Preserve keyboard focus visibility.",
                    "Map icon-only controls to explicit aria-labels.",
                    "Keep disabled, loading, selected, and error states tokenized.",
                ],
                "implementation_notes": [
                    "Recreate with local primitives such as Radix UI, shadcn/ui, or existing app components.",
                    "Use the source URL as evidence for behavior and state coverage.",
                    "Do not copy Vercel logos, brand assets, full documentation text, or private package source.",
                ],
            }
        )
    return {
        "schema_version": "geist-component-specs/v1",
        "brand": "Geist Reference",
        "total_components": len(components),
        "families": families,
        "global_adaptation": {
            "density": "compact spacing, thin borders, minimal decoration",
            "surface": "flat or subtle elevated surfaces with 1px separators",
            "motion": "short, utilitarian state transitions",
            "accessibility": "visible focus states and explicit ARIA for icon-only or async controls",
            "policy": "metadata-only reference; local implementation required",
        },
        "specs": specs,
    }


def build_component_specs_markdown(component_specs: dict[str, Any]) -> str:
    lines = [
        "# Geist Component Specs",
        "",
        f"- Total components: {component_specs['total_components']}",
        f"- Families: {', '.join(component_specs['families'])}",
        "- Policy: metadata-only reference; implementation source is not vendored.",
        "",
    ]
    for spec in component_specs["specs"]:
        props = ", ".join(spec["api_surface"]["prop_names"][:8]) or "none extracted"
        sections = ", ".join(spec["anatomy"]["sections"][:6]) or "none extracted"
        lines.extend(
            [
                f"## {spec['display_name']}",
                "",
                f"- Slug: `{spec['name']}`",
                f"- Family: `{spec['family']}`",
                f"- Source: {spec['source_url']}",
                f"- Role: {spec['role']}",
                f"- States: {', '.join(spec['anatomy']['states'])}",
                f"- Props observed: {props}",
                f"- Sections: {sections}",
                "",
            ]
        )
    return "\n".join(lines)


def build_markdown_summary(
    pages: list[dict[str, Any]],
    components: list[dict[str, Any]],
    foundations: list[dict[str, Any]],
    assets: list[dict[str, Any]],
    captured_at: str,
) -> str:
    family_counts = Counter(component["family"] for component in components)
    lines = [
        "# Geist Reference Extraction",
        "",
        f"- Captured at: {captured_at}",
        f"- Source: {GEIST_INDEX_URL}",
        f"- Total pages: {len(pages)}",
        f"- Components: {len(components)}",
        f"- Foundations: {len(foundations)}",
        f"- Asset/reference pages: {len(assets)}",
        "- Policy: metadata-only; no full documentation text or implementation source is vendored.",
        "",
        "## Families",
        "",
    ]
    for family, count in sorted(family_counts.items()):
        lines.append(f"- {family}: {count}")
    lines.extend(["", "## Components", ""])
    for component in sorted(components, key=lambda item: item["name"].lower()):
        sections = ", ".join(component["sections"][:5]) if component["sections"] else "no extracted sections"
        lines.append(
            f"- [{component['name']}]({component['url']}) — `{component['family']}`; "
            f"{component['code_example_count']} examples; sections: {sections}"
        )
    lines.extend(["", "## Foundations", ""])
    for page in sorted(foundations, key=lambda item: item["title"].lower()):
        lines.append(f"- [{page['title']}]({page['url']})")
    if assets:
        lines.extend(["", "## Asset/Reference Pages", ""])
        for page in sorted(assets, key=lambda item: item["title"].lower()):
            lines.append(f"- [{page['title']}]({page['url']})")
    return "\n".join(lines)


def build_sources(pages: list[dict[str, Any]], captured_at: str) -> dict[str, Any]:
    return {
        "schema_version": "geist-reference-sources/v1",
        "created_at": captured_at,
        "policy": absorption_policy(),
        "sources": [
            {
                "url": page["url"],
                "kind": "design-system-doc",
                "title": page["title"],
                "notes": f"{page['kind']} page; metadata-only extraction",
            }
            for page in pages
        ],
    }


def mirror_build_system(output_dir: Path, inventory: dict[str, Any], component_specs: dict[str, Any], manifest: dict[str, Any]) -> None:
    if output_dir.parent.name != "research":
        raise ValueError("--mirror-build-system expects an output directory like <project>/research/<name>.")
    project_dir = output_dir.parent.parent
    build_system_dir = project_dir / "build" / "system"
    write_json(build_system_dir / "blueprint" / "component_inventory.json", inventory)
    write_json(build_system_dir / "blueprint" / "geist_reference_manifest.json", manifest)
    write_json(build_system_dir / "components" / "component_specs.json", component_specs)
    write_text(build_system_dir / "components" / "component_specs.md", build_component_specs_markdown(component_specs))


def run(output_dir: Path, timeout: float, mirror_build: bool = False) -> dict[str, Any]:
    captured_at = utc_now_iso()
    output_dir.mkdir(parents=True, exist_ok=True)
    pages_dir = output_dir / "pages"

    with httpx.Client(follow_redirects=True, timeout=timeout, headers={"User-Agent": "design-ontology-harness/0.2"}) as client:
        index_response = client.get(GEIST_INDEX_URL)
        index_response.raise_for_status()
        links = extract_page_links(index_response.text)

        page_records: list[dict[str, Any]] = []
        for index, link in enumerate(links, start=1):
            response = client.get(link.url)
            response.raise_for_status()
            page = extract_page(link.url, str(response.url), response.text, link.title, link.slug, link.kind)
            page["nav_index"] = index
            page_records.append(page)
            write_json(pages_dir / f"{link.slug}.json", page)

    components = [component_entry(page) for page in page_records if page["kind"] == "component"]
    foundations = [page for page in page_records if page["kind"] == "foundation"]
    assets = [page for page in page_records if page["kind"] == "asset"]
    inventory = build_component_inventory(components)
    component_specs = build_component_specs(components)
    all_css_vars = sorted({var for page in page_records for var in page["token_refs"]["css_vars"]})
    package_refs = sorted(
        {
            source
            for page in page_records
            for source in page["symbol_metadata"]["import_sources"]
            if source
        }
    )

    manifest = {
        "schema_version": "geist-reference-manifest/v1",
        "captured_at": captured_at,
        "source": GEIST_INDEX_URL,
        "output_dir": str(output_dir),
        "page_count": len(page_records),
        "component_count": len(components),
        "foundation_count": len(foundations),
        "asset_page_count": len(assets),
        "package_refs": package_refs,
        "policy": absorption_policy(),
    }

    write_json(output_dir / "manifest.json", manifest)
    write_json(output_dir / "site_index.json", {"items": page_records})
    write_json(output_dir / "component_catalog.json", {"components": components})
    write_json(output_dir / "component_inventory.json", inventory)
    write_json(output_dir / "components" / "component_specs.json", component_specs)
    write_text(output_dir / "components" / "component_specs.md", build_component_specs_markdown(component_specs))
    write_json(output_dir / "token_refs.json", {"css_vars": all_css_vars, "count": len(all_css_vars)})
    write_json(output_dir / "sources.json", build_sources(page_records, captured_at))
    write_text(output_dir / "README.md", build_markdown_summary(page_records, components, foundations, assets, captured_at))
    if mirror_build:
        mirror_build_system(output_dir, inventory, component_specs, manifest)
    return manifest


def main() -> None:
    parser = argparse.ArgumentParser(description="Extract metadata-only Vercel Geist reference artifacts.")
    parser.add_argument(
        "--output-dir",
        default="projects/geist-reference/research/geist",
        help="Directory for extracted metadata artifacts.",
    )
    parser.add_argument("--timeout", type=float, default=30.0)
    parser.add_argument(
        "--mirror-build-system",
        action="store_true",
        help="Also write component inventory/specs into <project>/build/system for harness-compatible consumption.",
    )
    args = parser.parse_args()
    manifest = run(Path(args.output_dir), args.timeout, mirror_build=args.mirror_build_system)
    print(json.dumps(manifest, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
