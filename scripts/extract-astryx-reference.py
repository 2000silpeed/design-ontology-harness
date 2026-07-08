#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import html
import json
import re
from collections import defaultdict
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any
from urllib.parse import urljoin, urlparse

import httpx
from bs4 import BeautifulSoup


BASE_URL = "https://astryx.atmeta.com"
ASTRYX_INDEX_URL = "https://astryx.atmeta.com/components"

FAMILY_SLUGS: dict[str, set[str]] = {
    "action": {
        "button",
        "button-group",
        "icon-button",
        "toggle-button",
        "toggle-button-group",
        "dropdown-menu",
        "dropdown-menu-item",
        "link",
        "more-menu",
        "segmented-control",
        "segmented-control-item",
        "toolbar",
    },
    "chat": {
        "chat-composer",
        "chat-composer-drawer",
        "chat-composer-input",
        "chat-composer-token-element",
        "chat-dictation-button",
        "chat-layout",
        "chat-layout-scroll-button",
        "chat-message",
        "chat-message-bubble",
        "chat-message-list",
        "chat-message-metadata",
        "chat-send-button",
        "chat-system-message",
        "chat-tokenized-text",
        "chat-tool-calls",
    },
    "surface": {"card", "clickable-card", "selectable-card", "carousel", "collapsible", "collapsible-group"},
    "content": {
        "avatar",
        "avatar-group",
        "avatar-group-overflow",
        "avatar-status-dot",
        "blockquote",
        "citation",
        "code",
        "code-block",
        "empty-state",
        "heading",
        "icon",
        "item",
        "kbd",
        "markdown",
        "text",
        "thumbnail",
        "timestamp",
        "token",
    },
    "input": {
        "calendar",
        "checkbox-input",
        "checkbox-list",
        "checkbox-list-item",
        "date-input",
        "date-range-input",
        "date-time-input",
        "field",
        "field-label",
        "field-status",
        "file-input",
        "input-group",
        "input-group-text",
        "multi-selector",
        "number-input",
        "power-search",
        "radio-list",
        "radio-list-item",
        "selector",
        "selector-option",
        "slider",
        "switch",
        "text-area",
        "text-input",
        "time-input",
        "tokenizer",
        "typeahead",
        "typeahead-item",
    },
    "feedback": {"badge", "banner", "progress-bar", "skeleton", "spinner", "status-dot"},
    "layout": {
        "app-shell",
        "aspect-ratio",
        "center",
        "divider",
        "form-layout",
        "grid",
        "grid-span",
        "h-stack",
        "layout",
        "layout-content",
        "layout-footer",
        "layout-header",
        "layout-panel",
        "resize-handle",
        "section",
        "stack-item",
        "v-stack",
    },
    "navigation": {
        "breadcrumbs",
        "breadcrumb-item",
        "mobile-nav",
        "mobile-nav-toggle",
        "nav-heading-menu",
        "nav-icon",
        "outline",
        "overflow-list",
        "pagination",
        "side-nav",
        "side-nav-collapse-button",
        "side-nav-heading",
        "side-nav-item",
        "side-nav-section",
        "tab",
        "tab-list",
        "tab-menu",
        "top-nav",
        "top-nav-heading",
        "top-nav-item",
        "top-nav-mega-menu",
        "top-nav-mega-menu-featured-card",
        "top-nav-mega-menu-item",
        "top-nav-menu",
        "tree-list",
    },
    "overlay": {
        "alert-dialog",
        "command-palette",
        "command-palette-empty",
        "command-palette-footer",
        "command-palette-group",
        "command-palette-input",
        "command-palette-item",
        "command-palette-list",
        "context-menu",
        "context-menu-item",
        "dialog",
        "dialog-header",
        "hover-card",
        "lightbox",
        "overlay",
        "popover",
        "toast",
        "tooltip",
    },
    "data-display": {
        "list",
        "list-item",
        "metadata-list",
        "metadata-list-item",
        "table",
        "table-cell",
        "table-header-cell",
        "table-row",
    },
    "utility": {
        "layer-provider",
        "link-provider",
        "media-theme",
        "syntax-theme",
        "theme",
        "visuallyhidden",
    },
}

DEFAULT_STATES_BY_FAMILY = {
    "action": ["default", "hover", "active", "disabled", "loading", "focus"],
    "chat": ["default", "focused", "streaming", "error", "disabled"],
    "surface": ["default", "hover", "selected", "disabled"],
    "content": ["default", "hover", "selected"],
    "input": ["default", "hover", "focus", "disabled", "error", "selected"],
    "feedback": ["info", "success", "warning", "error", "loading"],
    "layout": ["default", "responsive", "collapsed"],
    "navigation": ["default", "hover", "active", "focus", "disabled"],
    "overlay": ["closed", "opening", "open", "dismissed"],
    "data-display": ["default", "loading", "empty", "error", "selected"],
    "utility": ["default"],
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


def clean_text(value: str) -> str:
    return " ".join(html.unescape(value).split())


def slug_from_href(href: str) -> str:
    path = urlparse(href).path.rstrip("/")
    return path.split("/")[-1].lower() if path else "astryx"


def normalize_href(href: str) -> str | None:
    clean = href.split("#", 1)[0].rstrip("/")
    if not clean or clean == "/components":
        return None
    if not clean.startswith("/components/"):
        return None
    return clean


def title_from_slug(slug: str) -> str:
    exceptions = {
        "kbd": "Kbd",
        "visuallyhidden": "VisuallyHidden",
    }
    if slug in exceptions:
        return exceptions[slug]
    return " ".join(part.capitalize() for part in slug.split("-"))


def family_for_slug(slug: str) -> str:
    for family, slugs in FAMILY_SLUGS.items():
        if slug in slugs:
            return family
    if slug.startswith("use"):
        return "utility"
    return "component"


def page_kind(slug: str) -> str:
    if slug.startswith("use"):
        return "hook"
    if family_for_slug(slug) == "utility":
        return "utility"
    return "component"


def extract_page_links(index_html: str) -> list[PageLink]:
    soup = BeautifulSoup(index_html, "html.parser")
    by_href: dict[str, str] = {}
    for anchor in soup.find_all("a", href=True):
        href = normalize_href(str(anchor["href"]))
        if not href or href in by_href:
            continue
        label = clean_text(anchor.get_text(" ", strip=True))
        by_href[href] = label or title_from_slug(slug_from_href(href))

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


def extract_symbol_metadata(page_html: str) -> dict[str, Any]:
    imports: list[str] = []
    import_sources: list[str] = []
    jsx_tags: list[str] = []
    prop_names: list[str] = []
    for match in re.finditer(r"import\s+\{([^}]+)\}\s+from\s+['\"]([^'\"]+)['\"]", page_html):
        symbols = [clean_text(part.split(" as ", 1)[0]) for part in match.group(1).split(",")]
        imports.extend(symbol for symbol in symbols if symbol)
        import_sources.append(match.group(2))
    for tag in re.findall(r"<([A-Z][A-Za-z0-9.]*)\b", page_html):
        jsx_tags.append(tag)
    for prop in re.findall(r"\s([A-Za-z][A-Za-z0-9_-]*)=", page_html):
        if prop not in {"className", "style", "children"}:
            prop_names.append(prop)
    return {
        "import_symbols": dedupe(imports),
        "import_sources": dedupe(import_sources),
        "jsx_tags": dedupe(jsx_tags),
        "prop_names": dedupe(prop_names),
    }


def extract_page(link: PageLink, final_url: str, response_html: str) -> dict[str, Any]:
    soup = BeautifulSoup(response_html, "html.parser")
    h1 = soup.find("h1")
    title_tag = soup.find("title")
    title = clean_text(h1.get_text(" ", strip=True)) if h1 else ""
    if not title and title_tag:
        title = clean_text(title_tag.get_text(" ", strip=True))
    title = title or link.title
    headings = [
        {"level": heading.name, "text": clean_text(heading.get_text(" ", strip=True))}
        for heading in soup.find_all(["h2", "h3"])
        if clean_text(heading.get_text(" ", strip=True))
    ]
    paragraphs = [
        clean_text(p.get_text(" ", strip=True))
        for p in soup.find_all("p")
        if clean_text(p.get_text(" ", strip=True))
    ]
    description = meta_content(soup, "description") or (paragraphs[0] if paragraphs else "")
    css_vars = sorted(set(re.findall(r"--[a-zA-Z0-9_-]+", response_html)))
    access_terms = sorted(
        set(re.findall(r"\b(?:aria-[a-z-]+|role|keyboard|focus|screen-reader|assistive)\b", response_html, re.I))
    )
    return {
        "schema_version": "astryx-reference-page/v1",
        "slug": link.slug,
        "kind": link.kind,
        "title": title,
        "url": link.url,
        "final_url": final_url,
        "canonical_url": canonical_url(soup, final_url),
        "family": family_for_slug(link.slug),
        "description": description,
        "source_hash": "sha256:" + hashlib.sha256(response_html.encode("utf-8")).hexdigest(),
        "body_text_length": len(soup.get_text(" ", strip=True)),
        "sections": dedupe([heading["text"] for heading in headings]),
        "symbol_metadata": extract_symbol_metadata(response_html),
        "token_refs": {"css_var_count": len(css_vars), "css_vars": css_vars[:80]},
        "accessibility_terms": access_terms[:40],
        "absorption": "metadata-only",
    }


def component_entry(page: dict[str, Any]) -> dict[str, Any]:
    family = page["family"]
    symbols = page["symbol_metadata"]
    return {
        "slug": page["slug"],
        "name": page["title"],
        "family": family,
        "url": page["url"],
        "description": page["description"],
        "sections": page["sections"],
        "states_required": DEFAULT_STATES_BY_FAMILY.get(family, ["default"]),
        "import_symbols": symbols["import_symbols"],
        "jsx_tags": symbols["jsx_tags"],
        "prop_names": symbols["prop_names"],
        "token_refs_count": page["token_refs"]["css_var_count"],
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
        "layout": "medium",
        "surface": "medium",
        "data-display": "medium",
        "content": "medium",
        "chat": "medium",
        "utility": "low",
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
                "source": ASTRYX_INDEX_URL,
                "visual_reference_signals": [
                    {
                        "id": f"astryx-{family}-metadata",
                        "label": f"Astryx {family} component metadata",
                        "confidence": 0.95,
                        "evidence": [f"{len(entries)} pages", "public docs nav", "metadata-only extraction"],
                    }
                ],
            }
        )
    return {
        "schema_version": "astryx-component-inventory/v1",
        "source": ASTRYX_INDEX_URL,
        "component_count": len(components),
        "families": families,
    }


def build_component_specs(components: list[dict[str, Any]]) -> dict[str, Any]:
    specs = []
    for component in sorted(components, key=lambda item: item["name"].lower()):
        specs.append(
            {
                "name": component["slug"],
                "display_name": component["name"],
                "family": component["family"],
                "role": component["description"],
                "source_url": component["url"],
                "source_pattern": "astryx-public-docs-metadata",
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
                    "note": "Identifiers only; implementation source is not vendored.",
                },
                "accessibility": [
                    "Keep focus visibility explicit.",
                    "Expose icon-only controls with aria-label.",
                    "Tokenize disabled, loading, selected, empty, and error states.",
                ],
                "implementation_notes": [
                    "Recreate with local primitives and local design tokens.",
                    "Use the source URL as evidence for behavior and state coverage.",
                    "Do not copy Meta brand assets, full documentation text, or product-specific demo copy.",
                ],
            }
        )
    return {
        "schema_version": "astryx-component-specs/v1",
        "brand": "Astryx Reference",
        "total_components": len(components),
        "families": sorted({component["family"] for component in components}),
        "global_adaptation": {
            "density": "themeable spacing with explicit compact/comfortable decisions",
            "surface": "token-driven surfaces, cards, tables, navigation, and overlays",
            "motion": "short state transitions with accessible focus handling",
            "policy": "metadata-only reference; local implementation required",
        },
        "specs": specs,
    }


def build_component_specs_markdown(component_specs: dict[str, Any]) -> str:
    lines = [
        "# Astryx Component Specs",
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


def build_markdown_summary(pages: list[dict[str, Any]], components: list[dict[str, Any]]) -> str:
    family_counts = defaultdict(int)
    for component in components:
        family_counts[component["family"]] += 1
    lines = [
        "# Astryx Reference Extraction",
        "",
        f"- Extracted at: {utc_now_iso()}",
        f"- Page records: {len(pages)}",
        f"- Component records: {len(components)}",
        f"- Source: {ASTRYX_INDEX_URL}",
        "",
        "## Families",
        "",
    ]
    for family, count in sorted(family_counts.items()):
        lines.append(f"- {family}: {count}")
    lines.extend(
        [
            "",
            "## Absorption Policy",
            "",
            "- Store component names, family grouping, state hints, tokens, and accessibility labels.",
            "- Do not vendor implementation source, full docs text, Meta brand assets, or demo product copy.",
        ]
    )
    return "\n".join(lines)


def mirror_build_system(output_dir: Path, inventory: dict[str, Any], component_specs: dict[str, Any], manifest: dict[str, Any]) -> None:
    build_system_dir = output_dir / "build" / "system"
    write_json(build_system_dir / "blueprint" / "component_inventory.json", inventory)
    write_json(build_system_dir / "blueprint" / "astryx_reference_manifest.json", manifest)
    write_json(build_system_dir / "components" / "component_specs.json", component_specs)
    write_text(build_system_dir / "components" / "component_specs.md", build_component_specs_markdown(component_specs))


def main() -> None:
    parser = argparse.ArgumentParser(description="Extract metadata-only Astryx reference artifacts.")
    parser.add_argument("--output-dir", type=Path, default=Path("projects/astryx-reference/research/astryx"))
    parser.add_argument("--timeout", type=float, default=20.0)
    parser.add_argument("--mirror-build-system", action="store_true")
    args = parser.parse_args()

    output_dir = args.output_dir
    client = httpx.Client(timeout=args.timeout, follow_redirects=True)
    index_response = client.get(ASTRYX_INDEX_URL)
    index_response.raise_for_status()
    links = extract_page_links(index_response.text)

    pages: list[dict[str, Any]] = []
    for link in links:
        response = client.get(link.url)
        response.raise_for_status()
        pages.append(extract_page(link, str(response.url), response.text))

    components = [component_entry(page) for page in pages if page["kind"] == "component"]
    inventory = build_component_inventory(components)
    component_specs = build_component_specs(components)
    manifest = {
        "schema_version": "astryx-reference-manifest/v1",
        "source": ASTRYX_INDEX_URL,
        "extracted_at": utc_now_iso(),
        "page_count": len(pages),
        "component_count": len(components),
        "absorption": "metadata-only",
    }

    write_json(output_dir / "manifest.json", manifest)
    write_json(output_dir / "pages.json", {"pages": pages})
    write_json(output_dir / "component_inventory.json", inventory)
    write_json(output_dir / "components" / "component_specs.json", component_specs)
    write_text(output_dir / "components" / "component_specs.md", build_component_specs_markdown(component_specs))
    write_text(output_dir / "README.md", build_markdown_summary(pages, components))
    if args.mirror_build_system:
        mirror_build_system(output_dir, inventory, component_specs, manifest)
    print(f"[extract-astryx-reference] wrote {output_dir} ({len(components)} components)")


if __name__ == "__main__":
    main()
