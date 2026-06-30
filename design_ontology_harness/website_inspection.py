from __future__ import annotations

from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any
from urllib.parse import urlparse

from .models import utc_now_iso
from .utils import ensure_dir, slugify, write_json


WEBSITE_INSPECTION_SCHEMA_VERSION = "website-reference-inspection/v1"

DEFAULT_VIEWPORTS = {
    "desktop": {"width": 1440, "height": 1200},
    "tablet": {"width": 768, "height": 1024},
    "mobile": {"width": 390, "height": 844},
}


@dataclass(frozen=True)
class WebsiteInspectionResult:
    report: dict[str, Any]
    output_dir: str
    report_path: str
    design_context_source: dict[str, Any]

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def inspect_reference_site(
    url: str,
    output_dir: Path,
    *,
    label: str | None = None,
    timeout_ms: int = 30_000,
    viewports: dict[str, dict[str, int]] | None = None,
) -> WebsiteInspectionResult:
    """Capture an ontology-safe reference inspection for a live website.

    The output is intentionally research-oriented. It records screenshots,
    topology, interactions, assets, and computed style evidence, but does not
    treat palette, typography, copy, or imagery as implementation authority.
    """

    resolved_viewports = viewports or DEFAULT_VIEWPORTS
    out = ensure_dir(output_dir)
    screenshots_dir = ensure_dir(out / "screenshots")
    normalized_url = _normalize_target_url(url)

    try:
        from playwright.sync_api import TimeoutError as PlaywrightTimeoutError
        from playwright.sync_api import sync_playwright
    except ImportError as exc:  # pragma: no cover - exercised by env setup, not unit tests
        raise RuntimeError(
            "Playwright is required for inspect-reference-site. Install project dependencies first."
        ) from exc

    captured_at = utc_now_iso()
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(headless=True)
        page = browser.new_page(
            viewport={
                "width": resolved_viewports["desktop"]["width"],
                "height": resolved_viewports["desktop"]["height"],
            }
        )
        try:
            response = page.goto(normalized_url, wait_until="networkidle", timeout=timeout_ms)
        except PlaywrightTimeoutError:
            response = page.goto(normalized_url, wait_until="domcontentloaded", timeout=timeout_ms)

        final_url = page.url
        title = page.title()
        status_code = response.status if response else None

        screenshots: list[dict[str, Any]] = []
        for viewport_name, viewport in resolved_viewports.items():
            page.set_viewport_size({"width": viewport["width"], "height": viewport["height"]})
            page.wait_for_timeout(250)
            screenshot_path = screenshots_dir / f"{viewport_name}.png"
            page.screenshot(path=str(screenshot_path), full_page=True)
            screenshots.append(
                {
                    "viewport": viewport_name,
                    "width": viewport["width"],
                    "height": viewport["height"],
                    "path": _relative_to_output(screenshot_path, out),
                }
            )

        page.set_viewport_size(
            {
                "width": resolved_viewports["desktop"]["width"],
                "height": resolved_viewports["desktop"]["height"],
            }
        )
        page.wait_for_timeout(250)

        page_data = page.evaluate(_INSPECTION_SCRIPT)
        browser.close()

    topology = page_data.get("topology", [])
    behavior_summary = page_data.get("behavior_summary", {})
    assets = page_data.get("assets", {})
    computed_styles = page_data.get("computed_styles", {})

    source_label = label or title or urlparse(final_url).netloc or normalized_url
    report = {
        "schema_version": WEBSITE_INSPECTION_SCHEMA_VERSION,
        "captured_at": captured_at,
        "url": normalized_url,
        "final_url": final_url,
        "status_code": status_code,
        "title": title,
        "label": source_label,
        "absorption_policy": {
            "allowed": [
                "component morphology",
                "layout density",
                "panel/card proportions",
                "hierarchy rhythm",
                "interaction affordance patterns",
                "flow pattern labels",
            ],
            "denied": [
                "color palette",
                "palette composition",
                "typography scale",
                "domain information architecture",
                "product copy",
                "redistributable imagery unless explicitly licensed",
            ],
            "rule": "Use this inspection as reference research only. Do not clone copy, brand assets, palette, or typography into implementation outputs.",
        },
        "screenshots": screenshots,
        "topology": topology,
        "behavior_summary": behavior_summary,
        "assets": assets,
        "computed_styles": computed_styles,
    }

    write_json(out / "website_reference_report.json", report)
    write_json(out / "assets_manifest.json", assets)
    write_json(out / "computed_styles.json", computed_styles)
    (out / "PAGE_TOPOLOGY.md").write_text(_render_topology_markdown(report), encoding="utf-8")
    (out / "BEHAVIORS.md").write_text(_render_behaviors_markdown(report), encoding="utf-8")

    source = build_design_context_source(report, out)
    write_json(out / "design_context_source.json", source)

    return WebsiteInspectionResult(
        report=report,
        output_dir=str(out),
        report_path=str(out / "website_reference_report.json"),
        design_context_source=source,
    )


def build_design_context_source(report: dict[str, Any], output_dir: Path | None = None) -> dict[str, Any]:
    final_url = str(report.get("final_url") or report.get("url") or "")
    host = urlparse(final_url).netloc or "website"
    topology = report.get("topology") if isinstance(report.get("topology"), list) else []
    behavior = report.get("behavior_summary") if isinstance(report.get("behavior_summary"), dict) else {}
    screenshots = report.get("screenshots") if isinstance(report.get("screenshots"), list) else []
    report_path = "website_reference_report.json"
    if output_dir:
        report_path = str((output_dir / "website_reference_report.json").resolve())

    terms = _terms_from_inspection(report)
    return {
        "source_id": f"website-inspection-{slugify(host)}",
        "kind": "website-inspection",
        "provider_id": "website-inspection",
        "label": report.get("label") or report.get("title") or host,
        "status": "selected",
        "url": final_url,
        "path": report_path,
        "tags": terms[:16],
        "category": "website-reference",
        "visionDescription": _inspection_description(topology, behavior, screenshots),
        "website_inspection": {
            "schema_version": report.get("schema_version"),
            "section_count": len(topology),
            "screenshots": screenshots,
            "interaction_models": behavior.get("interaction_models", []),
            "asset_counts": behavior.get("asset_counts", {}),
        },
        "absorption_policy": report.get("absorption_policy", {}),
    }


def _normalize_target_url(url: str) -> str:
    raw = str(url).strip()
    if not raw:
        raise ValueError("URL is required.")
    parsed = urlparse(raw)
    if parsed.scheme in {"http", "https", "file"}:
        return raw
    if parsed.scheme:
        raise ValueError(f"Unsupported URL scheme: {parsed.scheme}")
    return f"https://{raw}"


def _relative_to_output(path: Path, output_dir: Path) -> str:
    try:
        return str(path.relative_to(output_dir))
    except ValueError:
        return str(path)


def _terms_from_inspection(report: dict[str, Any]) -> list[str]:
    terms: list[str] = []
    title = str(report.get("title") or report.get("label") or "")
    terms.extend(_tokenize(title))
    for section in report.get("topology", [])[:12]:
        if not isinstance(section, dict):
            continue
        terms.extend(_tokenize(section.get("role")))
        terms.extend(_tokenize(section.get("label")))
        terms.extend(_tokenize(section.get("interaction_model")))
        terms.extend(_tokenize(section.get("layout_hint")))
    behavior = report.get("behavior_summary") or {}
    for item in behavior.get("interaction_models", []) if isinstance(behavior, dict) else []:
        terms.extend(_tokenize(item))
    return _dedupe(terms)


def _tokenize(value: Any) -> list[str]:
    text = str(value or "").lower()
    return ["".join(ch if ch.isalnum() else " " for ch in text).strip()][0].split()


def _dedupe(values: list[str]) -> list[str]:
    seen: set[str] = set()
    result: list[str] = []
    for value in values:
        if value and value not in seen:
            seen.add(value)
            result.append(value)
    return result


def _inspection_description(topology: list[dict[str, Any]], behavior: dict[str, Any], screenshots: list[dict[str, Any]]) -> str:
    models = behavior.get("interaction_models", []) if isinstance(behavior, dict) else []
    asset_counts = behavior.get("asset_counts", {}) if isinstance(behavior, dict) else {}
    return (
        f"Website reference inspection with {len(topology)} observed sections, "
        f"{len(screenshots)} viewport screenshots, interaction models {models or ['static']}, "
        f"and asset counts {asset_counts or {}}."
    )


def _render_topology_markdown(report: dict[str, Any]) -> str:
    lines = [
        f"# Page Topology: {report.get('label') or report.get('title') or report.get('url')}",
        "",
        f"- URL: {report.get('final_url') or report.get('url')}",
        f"- Captured: {report.get('captured_at')}",
        "- Absorption: morphology, density, hierarchy, interaction affordance only.",
        "",
        "## Sections",
        "",
    ]
    for section in report.get("topology", []):
        lines.append(f"### {section.get('index')}. {section.get('label') or section.get('selector')}")
        lines.append(f"- selector: `{section.get('selector')}`")
        lines.append(f"- role: {section.get('role')}")
        lines.append(f"- interaction_model: {section.get('interaction_model')}")
        lines.append(f"- layout_hint: {section.get('layout_hint')}")
        if section.get("text_sample"):
            lines.append(f"- text_sample: {section.get('text_sample')}")
        lines.append("")
    return "\n".join(lines).rstrip() + "\n"


def _render_behaviors_markdown(report: dict[str, Any]) -> str:
    behavior = report.get("behavior_summary") or {}
    lines = [
        f"# Behavior Sweep: {report.get('label') or report.get('title') or report.get('url')}",
        "",
        "- This file records observed affordances for reference research. It is not permission to clone original copy, assets, palette, or typography.",
        "",
        "## Summary",
        "",
    ]
    for key in [
        "interaction_models",
        "sticky_or_fixed_count",
        "animated_count",
        "clickable_count",
        "form_control_count",
        "asset_counts",
    ]:
        lines.append(f"- {key}: {behavior.get(key)}")
    lines.append("")
    lines.append("## Interactive Elements")
    lines.append("")
    for item in behavior.get("interactive_elements", [])[:24]:
        lines.append(f"- `{item.get('selector')}`: {item.get('label') or item.get('role') or item.get('tag')}")
    lines.append("")
    lines.append("## State/Animation Hints")
    lines.append("")
    for item in behavior.get("stateful_elements", [])[:24]:
        lines.append(
            f"- `{item.get('selector')}`: position={item.get('position')} "
            f"transition={item.get('transition')} animation={item.get('animationName')}"
        )
    return "\n".join(lines).rstrip() + "\n"


_INSPECTION_SCRIPT = r"""
(() => {
  const STYLE_PROPS = [
    'display','position','top','right','bottom','left','zIndex',
    'width','height','maxWidth','minWidth','padding','margin','gap',
    'gridTemplateColumns','flexDirection','justifyContent','alignItems',
    'fontSize','fontWeight','fontFamily','lineHeight','letterSpacing',
    'color','backgroundColor','border','borderRadius','boxShadow',
    'opacity','transform','transition','animationName','animationDuration',
    'overflow','scrollSnapType'
  ];

  function cssPath(el) {
    if (!el || !el.tagName) return '';
    if (el.id) return `${el.tagName.toLowerCase()}#${el.id}`;
    const parts = [];
    let node = el;
    while (node && node.nodeType === 1 && parts.length < 4) {
      let part = node.tagName.toLowerCase();
      if (node.classList && node.classList.length) {
        part += '.' + [...node.classList].slice(0, 2).join('.');
      }
      const parent = node.parentElement;
      if (parent) {
        const siblings = [...parent.children].filter(child => child.tagName === node.tagName);
        if (siblings.length > 1) part += `:nth-of-type(${siblings.indexOf(node) + 1})`;
      }
      parts.unshift(part);
      node = parent;
    }
    return parts.join(' > ');
  }

  function visible(el) {
    const rect = el.getBoundingClientRect();
    const cs = getComputedStyle(el);
    return rect.width > 1 && rect.height > 1 && cs.visibility !== 'hidden' && cs.display !== 'none';
  }

  function stylesFor(el) {
    const cs = getComputedStyle(el);
    const styles = {};
    for (const prop of STYLE_PROPS) {
      const value = cs[prop];
      if (value && value !== 'none' && value !== 'normal' && value !== 'auto' && value !== '0px' && value !== 'rgba(0, 0, 0, 0)') {
        styles[prop] = value;
      }
    }
    return styles;
  }

  function textSample(el) {
    return (el.innerText || el.textContent || '').replace(/\s+/g, ' ').trim().slice(0, 180);
  }

  function roleFor(el) {
    const tag = el.tagName.toLowerCase();
    const role = el.getAttribute('role');
    if (role) return role;
    if (tag === 'header') return 'header';
    if (tag === 'nav') return 'navigation';
    if (tag === 'main') return 'main';
    if (tag === 'footer') return 'footer';
    if (tag === 'section') return 'section';
    if (tag === 'form') return 'form';
    return tag;
  }

  function layoutHint(el) {
    const cs = getComputedStyle(el);
    if (cs.display === 'grid') return `grid:${cs.gridTemplateColumns}`;
    if (cs.display === 'flex') return `flex:${cs.flexDirection}`;
    if (cs.position === 'sticky' || cs.position === 'fixed') return `${cs.position}-layer`;
    return cs.display || 'block';
  }

  function interactionModel(el) {
    const interactive = el.querySelectorAll('a,button,input,select,textarea,[role="button"],[tabindex]').length;
    const cs = getComputedStyle(el);
    if (cs.position === 'sticky' || cs.position === 'fixed' || cs.scrollSnapType !== 'none') return 'scroll-aware';
    if (interactive > 0) return 'click-or-input';
    if (cs.animationName && cs.animationName !== 'none') return 'time-driven';
    return 'static';
  }

  const sectionCandidates = [
    ...document.querySelectorAll('header, nav, main > section, main > article, main > div, body > section, body > footer, footer')
  ].filter(visible);
  const sections = (sectionCandidates.length ? sectionCandidates : [...document.body.children].filter(visible))
    .slice(0, 24)
    .map((el, index) => ({
      index: index + 1,
      selector: cssPath(el),
      role: roleFor(el),
      label: el.getAttribute('aria-label') || el.getAttribute('data-section') || el.querySelector('h1,h2,h3')?.innerText?.trim() || roleFor(el),
      text_sample: textSample(el),
      interaction_model: interactionModel(el),
      layout_hint: layoutHint(el),
      child_count: el.children.length,
      rect: (() => {
        const r = el.getBoundingClientRect();
        return { x: Math.round(r.x), y: Math.round(r.y + window.scrollY), width: Math.round(r.width), height: Math.round(r.height) };
      })()
    }));

  const styleTargets = [
    ...document.querySelectorAll('body, header, nav, main, footer, h1, h2, h3, p, a, button, input, section, article')
  ].filter(visible).slice(0, 120);
  const computedStyles = styleTargets.map(el => ({
    selector: cssPath(el),
    tag: el.tagName.toLowerCase(),
    role: roleFor(el),
    text_sample: textSample(el),
    styles: stylesFor(el)
  }));

  const interactiveElements = [...document.querySelectorAll('a,button,input,select,textarea,[role="button"],[tabindex]')]
    .filter(visible)
    .slice(0, 80)
    .map(el => ({
      selector: cssPath(el),
      tag: el.tagName.toLowerCase(),
      role: el.getAttribute('role') || '',
      label: (el.getAttribute('aria-label') || el.innerText || el.getAttribute('placeholder') || '').replace(/\s+/g, ' ').trim().slice(0, 100)
    }));

  const statefulElements = [...document.querySelectorAll('*')]
    .filter(visible)
    .map(el => {
      const cs = getComputedStyle(el);
      return {
        selector: cssPath(el),
        position: cs.position,
        transition: cs.transition,
        animationName: cs.animationName,
        animationDuration: cs.animationDuration,
        scrollSnapType: cs.scrollSnapType
      };
    })
    .filter(item => ['sticky', 'fixed'].includes(item.position) || item.transition !== 'all 0s ease 0s' || item.animationName !== 'none' || item.scrollSnapType !== 'none')
    .slice(0, 80);

  const images = [...document.querySelectorAll('img')].map(img => ({
    src: img.currentSrc || img.src,
    alt: img.alt,
    width: img.naturalWidth,
    height: img.naturalHeight,
    selector: cssPath(img),
    parent_selector: cssPath(img.parentElement)
  })).filter(item => item.src);

  const videos = [...document.querySelectorAll('video')].map(video => ({
    src: video.currentSrc || video.src || video.querySelector('source')?.src || '',
    poster: video.poster || '',
    autoplay: video.autoplay,
    loop: video.loop,
    muted: video.muted,
    selector: cssPath(video)
  })).filter(item => item.src || item.poster);

  const backgroundImages = [...document.querySelectorAll('*')]
    .filter(visible)
    .map(el => ({ selector: cssPath(el), backgroundImage: getComputedStyle(el).backgroundImage }))
    .filter(item => item.backgroundImage && item.backgroundImage !== 'none')
    .slice(0, 80);

  const models = [...new Set(sections.map(section => section.interaction_model))];
  return {
    topology: sections,
    computed_styles: { elements: computedStyles },
    assets: {
      images,
      videos,
      background_images: backgroundImages,
      counts: {
        images: images.length,
        videos: videos.length,
        background_images: backgroundImages.length,
        inline_svgs: document.querySelectorAll('svg').length
      }
    },
    behavior_summary: {
      interaction_models: models,
      sticky_or_fixed_count: statefulElements.filter(item => ['sticky', 'fixed'].includes(item.position)).length,
      animated_count: statefulElements.filter(item => item.animationName !== 'none' || item.transition !== 'all 0s ease 0s').length,
      clickable_count: interactiveElements.length,
      form_control_count: document.querySelectorAll('input,select,textarea').length,
      asset_counts: {
        images: images.length,
        videos: videos.length,
        background_images: backgroundImages.length,
        inline_svgs: document.querySelectorAll('svg').length
      },
      interactive_elements: interactiveElements,
      stateful_elements: statefulElements
    }
  };
})()
"""
