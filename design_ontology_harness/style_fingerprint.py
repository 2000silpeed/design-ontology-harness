"""Cross-project style fingerprint registry and anti-convergence gate.

The harness already produces diverse blueprints per project, but the final
mockup implementation step tends to collapse back into the implementing
LLM's default aesthetic (warm paper surface + oxblood/teal/citron accents +
serif display accent + the same font pairing). This module gives the harness
memory across projects:

1. ``extract_style_fingerprint`` reads the *final* HTML/CSS of a project and
   distills it into a comparable fingerprint (surface tone, accent hue
   buckets, font families, serif-accent usage, radius profile).
2. ``registry/style_fingerprints.json`` stores one fingerprint per project.
3. ``check_style_divergence`` compares a new implementation against recent
   registry entries and against known convergence attractors, and fails when
   the new surface is too close to what was already shipped.

The gate is intentionally applied to implementation output, not blueprints:
blueprint tokens were already diverse, the repetition happens in CSS.
"""

from __future__ import annotations

import colorsys
import hashlib
import json
import os
import re
import tempfile
from contextlib import contextmanager
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterator

try:
    import fcntl
except ImportError:  # pragma: no cover - Windows uses msvcrt below.
    fcntl = None

try:
    import msvcrt
except ImportError:  # pragma: no cover - POSIX uses fcntl.
    msvcrt = None

FINGERPRINT_SCHEMA_VERSION = "style-fingerprint/v1"
REGISTRY_SCHEMA_VERSION = "style-fingerprint-registry/v1"
DEFAULT_REGISTRY_RELATIVE_PATH = Path("registry") / "style_fingerprints.json"
DEFAULT_SIMILARITY_THRESHOLD = 0.62
DEFAULT_COMPARE_LIMIT = 10

HUE_BUCKET_NAMES = [
    "red",
    "orange",
    "amber",
    "yellow",
    "lime",
    "green",
    "teal",
    "cyan",
    "blue",
    "indigo",
    "violet",
    "magenta",
]

GENERIC_FONT_TOKENS = {
    "system-ui",
    "sans-serif",
    "serif",
    "monospace",
    "ui-monospace",
    "ui-serif",
    "ui-sans-serif",
    "ui-rounded",
    "-apple-system",
    "blinkmacsystemfont",
    "segoe ui",
    "apple sd gothic neo",
    "malgun gothic",
    "sfmono-regular",
    "menlo",
    "monaco",
    "consolas",
    "helvetica",
    "helvetica neue",
    "arial",
    "roboto",
    "inherit",
    "initial",
    "emoji",
    "apple color emoji",
    "segoe ui emoji",
    "noto color emoji",
}

HEX_RE = re.compile(r"#(?P<hex>[0-9a-fA-F]{3}|[0-9a-fA-F]{6})\b")
RGB_RE = re.compile(
    r"rgba?\(\s*(?P<r>\d{1,3})\s*[, ]\s*(?P<g>\d{1,3})\s*[, ]\s*(?P<b>\d{1,3})"
)
FONT_FAMILY_DECL_RE = re.compile(r"font-family\s*:\s*(?P<value>[^;{}]+)", re.IGNORECASE)
GOOGLE_FONTS_FAMILY_RE = re.compile(r"family=(?P<family>[A-Za-z0-9+ _-]+)")
CUSTOM_PROP_RE = re.compile(
    r"(?P<name>--[\w-]+)\s*:\s*(?P<value>#[0-9a-fA-F]{3,8}|rgba?\([^)]*\))"
)
BACKGROUND_DECL_RE = re.compile(
    r"(?:^|[;{\s])background(?:-color)?\s*:\s*(?P<value>[^;{}]+)", re.IGNORECASE
)
BORDER_RADIUS_RE = re.compile(r"border-radius\s*:\s*(?P<value>[^;{}]+)", re.IGNORECASE)
RADIUS_PX_RE = re.compile(r"(\d+(?:\.\d+)?)px")
#: Colours the brand actually chose. Status roles (red = danger everywhere),
#: link roles, and text/surface neutrals are excluded: sharing those is meaning
#: or legibility, not a converged aesthetic.
BRAND_ACCENT_DECL_RE = re.compile(
    r"--ds-color-(?:primary|accent|brand-[\w-]+|support-[\w-]+)\s*:\s*"
    r"(?P<value>#[0-9a-fA-F]{3,8}|rgba?\([^)]*\))",
    re.IGNORECASE,
)
#: Only the light block. Dark values are derived from it, so counting both
#: doubles every hue and washes out the difference between projects.
ROOT_BLOCK_RE = re.compile(r":root\s*\{(?P<body>[^}]*)\}", re.IGNORECASE)

KNOWN_ATTRACTORS: list[dict[str, Any]] = [
    {
        "id": "warm-editorial-default",
        "label": "웜 페이퍼 + 딥 레드/틸 액센트 + 세리프 디스플레이",
        "description": (
            "구현 LLM이 브랜드와 무관하게 반복 생산하는 기본 미감: 크림/페이퍼 배경, "
            "옥스블러드·버건디 계열 primary, 틸 secondary, 시트론 하이라이트, 세리프 디스플레이 서체."
        ),
        "surface_tones": {"warm-paper"},
        "required_hue_groups": [{"red", "magenta"}, {"teal", "cyan", "green"}],
        "requires_serif_accent": True,
    },
    {
        "id": "indigo-saas-default",
        "label": "뉴트럴 라이트 + 인디고/바이올렛 단일 액센트 SaaS 기본형",
        "description": (
            "흰 배경에 인디고~바이올렛 계열 primary 하나로 끝나는 범용 SaaS 대시보드 미감."
        ),
        "surface_tones": {"neutral-light"},
        "required_hue_groups": [{"blue", "indigo", "violet"}],
        "restrict_to_hues": {"blue", "indigo", "violet"},
        "requires_serif_accent": False,
    },
]


@dataclass
class StyleFingerprint:
    project: str
    schema_version: str = FINGERPRINT_SCHEMA_VERSION
    source_files: list[str] = field(default_factory=list)
    source_snapshot_sha256: str | None = None
    surface_tone: str = "unknown"
    surface_hexes: list[str] = field(default_factory=list)
    accent_hue_buckets: list[str] = field(default_factory=list)
    accent_hexes: list[str] = field(default_factory=list)
    font_families: list[str] = field(default_factory=list)
    serif_accent: bool = False
    radius_values_px: list[float] = field(default_factory=list)
    uses_pill_shapes: bool = False
    color_count: int = 0
    separation_style: str = "unknown"
    composition_markers: list[str] = field(default_factory=list)
    # Motion axes. Without these, every project could share one duration and
    # one easing curve and the divergence gate would still pass them.
    duration_values_ms: list[float] = field(default_factory=list)
    easing_signatures: list[str] = field(default_factory=list)
    transition_properties: list[str] = field(default_factory=list)
    has_decorative_loop: bool = False
    enter_exit_asymmetry: bool = False
    supports_dark_theme: bool = False

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


# ---------------------------------------------------------------------------
# Color helpers


def _normalize_hex(value: str) -> str:
    raw = value.lstrip("#")
    if len(raw) == 3:
        raw = "".join(ch * 2 for ch in raw)
    return "#" + raw.upper()


def _hex_to_hls(value: str) -> tuple[float, float, float]:
    raw = value.lstrip("#")
    r = int(raw[0:2], 16) / 255.0
    g = int(raw[2:4], 16) / 255.0
    b = int(raw[4:6], 16) / 255.0
    return colorsys.rgb_to_hls(r, g, b)


def _hue_bucket(hue: float) -> str:
    index = int((hue * 360.0) // 30) % 12
    return HUE_BUCKET_NAMES[index]


def _classify_surface(hexes: list[str]) -> tuple[str, list[str]]:
    """Classify the dominant surface tone from candidate background colors."""

    if not hexes:
        return "unknown", []
    scored: list[tuple[str, float, float, float]] = []
    for value in hexes:
        hue, lightness, saturation = _hex_to_hls(value)
        scored.append((value, hue, lightness, saturation))

    darks = [item for item in scored if item[2] < 0.35]
    lights = [item for item in scored if item[2] >= 0.78]
    pool = lights or scored
    # Saturated component backgrounds (badges, chips) also appear as
    # background declarations, so only call the surface dark when dark
    # backgrounds actually outnumber light ones.
    if darks and len(darks) > len(lights):
        return "dark", [item[0] for item in darks[:4]]

    def tone_of(h: float, s: float) -> str:
        if s < 0.08:
            return "neutral-light"
        hue_deg = h * 360.0
        if 20.0 <= hue_deg <= 75.0:
            return "warm-paper"
        if 75.0 < hue_deg <= 260.0:
            return "cool-tinted"
        return "rose-tinted"

    votes: dict[str, int] = {}
    for _, h, _, s in pool:
        votes[tone_of(h, s)] = votes.get(tone_of(h, s), 0) + 1
    tone = max(votes, key=lambda key: votes[key])
    return tone, [item[0] for item in pool[:4]]


def _resolve_color_token(value: str, custom_props: dict[str, str]) -> str | None:
    value = value.strip()
    match = HEX_RE.search(value)
    if match:
        return _normalize_hex(match.group(0))
    rgb = RGB_RE.search(value)
    if rgb:
        r, g, b = (min(int(rgb.group(k)), 255) for k in ("r", "g", "b"))
        return _normalize_hex(f"#{r:02X}{g:02X}{b:02X}")
    var_match = re.search(r"var\(\s*(--[\w-]+)", value)
    if var_match:
        resolved = custom_props.get(var_match.group(1))
        if resolved:
            return _resolve_color_token(resolved, {})
    return None


# ---------------------------------------------------------------------------
# Extraction


def _collect_source_files(project_dir: Path) -> list[Path]:
    out: list[Path] = []
    extensions = {".html", ".css", ".scss", ".sass", ".less", ".tsx", ".jsx", ".ts", ".js", ".vue", ".svelte"}
    excluded = {".git", ".next", "build", "dist", "node_modules", "screenshots", "coverage"}
    for path in project_dir.rglob("*"):
        if not path.is_file() or path.suffix.lower() not in extensions:
            continue
        relative = path.relative_to(project_dir)
        if any(part in excluded for part in relative.parts):
            continue
        out.append(path)
    # Token-bound projects keep their actual palette in design-system/*.css.
    out.extend(sorted(project_dir.glob("design-system/*.css")))
    seen: set[Path] = set()
    unique: list[Path] = []
    for path in out:
        if path in seen:
            continue
        seen.add(path)
        unique.append(path)
    return unique


def _extract_fonts(text: str) -> tuple[list[str], bool]:
    families: list[str] = []
    serif_accent = False
    for match in FONT_FAMILY_DECL_RE.finditer(text):
        raw_value = match.group("value")
        if "var(--" in raw_value and not HEX_RE.search(raw_value):
            stripped = re.sub(r"var\([^)]*\)", "", raw_value)
        else:
            stripped = raw_value
        parts = [
            part.strip().strip("'\"").strip()
            for part in stripped.split(",")
            if part.strip()
        ]
        parts = [
            part
            for part in parts
            if part and "(" not in part and ")" not in part and not part.startswith("--")
        ]
        named = [part for part in parts if part.lower() not in GENERIC_FONT_TOKENS]
        generics = {part.lower() for part in parts} & {"serif", "ui-serif"}
        if generics and named:
            serif_accent = True
        for name in named:
            if name and name not in families:
                families.append(name)
    for match in re.finditer(r"--ds-font-[\w-]+\s*:\s*(?P<value>[^;{}]+)", text):
        for part in match.group("value").split(","):
            name = part.strip().strip("'\"").strip()
            if not name or "(" in name or ")" in name:
                continue
            if name.lower() in GENERIC_FONT_TOKENS:
                continue
            if name not in families:
                families.append(name)
    for match in GOOGLE_FONTS_FAMILY_RE.finditer(text):
        name = match.group("family").replace("+", " ").strip()
        name = re.sub(r":.*$", "", name)
        if name and name not in families and name.lower() not in GENERIC_FONT_TOKENS:
            families.append(name)
        if "serif" in name.lower():
            serif_accent = True
    return families, serif_accent


_CSS_BLOCK_RE = re.compile(r"[^{}]+\{(?P<body>[^{}]*)\}")


def _detect_separation_style(css_text: str) -> str:
    """Classify the surface's dominant separation grammar.

    Palette and fonts alone miss composition repetition: two projects with
    different colors can still share the same skeleton (hairline rows vs card
    wall vs pure whitespace). This axis feeds the divergence comparison.
    """

    card_blocks = 0
    hairline_decls = 0
    for match in _CSS_BLOCK_RE.finditer(css_text):
        body = match.group("body")
        has_border = re.search(r"\bborder\s*:\s*1px\s+solid", body, re.IGNORECASE)
        has_radius = re.search(r"\bborder-radius\s*:", body, re.IGNORECASE)
        if has_border and has_radius:
            card_blocks += 1
        hairline_decls += len(
            re.findall(r"\bborder-(?:bottom|top)\s*:\s*1px\s+solid", body, re.IGNORECASE)
        )
    card_tokens = len(re.findall(r"\b(?:card|panel|tile|rounded-(?:md|lg|xl|2xl)|shadow-(?:md|lg|xl))\b", css_text, re.IGNORECASE))
    row_tokens = len(re.findall(r"\b(?:table|ledger|list-row|data-row|border-b|divide-y)\b", css_text, re.IGNORECASE))
    spatial_tokens = len(re.findall(r"\b(?:canvas|map|graph|node|edge|timeline|spatial)\b", css_text, re.IGNORECASE))
    split_tokens = len(re.findall(r"\b(?:split|inspector|detail-pane|master-detail|grid-cols-[23])\b", css_text, re.IGNORECASE))
    operations_tokens = len(
        re.findall(
            r"\b(?:schedule|fixture|ticker|ledger|standings|scoreline|filter|table|rail|result|match-row)\b",
            css_text,
            re.IGNORECASE,
        )
    )
    # Dense operational products often use bordered/radiused containers while
    # their dominant grammar is still tables, ledgers and horizontal rails.
    # Count that product structure before treating every rounded boundary as a
    # generic card wall.
    if row_tokens >= 8 and operations_tokens >= 8 and card_tokens <= row_tokens * 2:
        return "operations-table-rail"
    if card_blocks >= 5 and (row_tokens == 0 or card_tokens > row_tokens * 2):
        return "card-wall"
    if row_tokens >= 4:
        return "table-ledger"
    if spatial_tokens >= 4:
        return "canvas-spatial"
    if split_tokens >= 3:
        return "split-workbench"
    if hairline_decls >= 4:
        return "hairline-rows"
    return "whitespace"


MOTION_DECL_RE = re.compile(
    r"(?<![-$@\w])(?:-webkit-)?(?P<prop>transition|animation)"
    r"(?P<sub>-duration|-delay|-timing-function|-property)?\s*:\s*(?P<value>[^;{}]+)",
    re.IGNORECASE,
)
_DURATION_LITERAL_RE = re.compile(r"(?<![\w.-])(?P<value>\d+(?:\.\d+)?)(?P<unit>ms|s)(?![\w-])", re.I)
_DURATION_TOKEN_RE = re.compile(r"var\(\s*--ds-duration-(?P<step>\d+)\s*\)", re.I)
_LOOP_TOKEN_RE = re.compile(r"var\(\s*--ds-loop-(?P<name>[a-z]+)\s*\)", re.I)
_EASE_TOKEN_RE = re.compile(r"var\(\s*--ds-ease-(?P<name>[a-z]+)\s*\)", re.I)
_EASE_LITERAL_RE = re.compile(
    r"(?<![-\w])(?:cubic-bezier\([^)]*\)|ease-in-out|ease-in|ease-out|ease|linear)(?![-\w])",
    re.IGNORECASE,
)
_LOOP_NAME_MS = {"fast": 1200.0, "medium": 1600.0, "slow": 2400.0}
_TRANSITION_PROPERTY_RE = re.compile(r"(?<![-\w])(?P<name>[a-z][a-z-]{2,})(?![-\w(])", re.IGNORECASE)
_NON_PROPERTY_WORDS = {
    "ease", "ease-in", "ease-out", "ease-in-out", "linear", "infinite", "alternate",
    "both", "forwards", "backwards", "normal", "reverse", "none", "step-start",
    "step-end", "important", "var", "cubic-bezier", "steps", "running", "paused",
}


def _extract_motion_signature(text: str) -> dict[str, Any]:
    """Read a stylesheet's motion character, resolving --ds-* tokens by name."""

    durations: set[float] = set()
    easings: set[str] = set()
    properties: set[str] = set()
    decorative_loop = False

    for decl in MOTION_DECL_RE.finditer(text):
        value = decl.group("value")
        sub = (decl.group("sub") or "").lower()
        is_loop = bool(re.search(r"(?<![-\w])infinite(?![-\w])", value, re.IGNORECASE))

        for token in _DURATION_TOKEN_RE.finditer(value):
            durations.add(float(token.group("step")))
        for token in _LOOP_TOKEN_RE.finditer(value):
            durations.add(_LOOP_NAME_MS.get(token.group("name").lower(), 1600.0))
        for literal in _DURATION_LITERAL_RE.finditer(value):
            amount = float(literal.group("value"))
            if literal.group("unit").lower() == "s":
                amount *= 1000
            if amount > 0:
                durations.add(amount)

        for token in _EASE_TOKEN_RE.finditer(value):
            easings.add(token.group("name").lower())
        for literal in _EASE_LITERAL_RE.finditer(value):
            easings.add(re.sub(r"\s+", "", literal.group(0).lower()))

        if sub in {"", "-property"} and decl.group("prop").lower() == "transition":
            for word in _TRANSITION_PROPERTY_RE.finditer(value):
                name = word.group("name").lower()
                if name not in _NON_PROPERTY_WORDS and not name.startswith("--"):
                    properties.add(name)

        # A loop spending the transition budget is decoration, not progress.
        if is_loop and not _LOOP_TOKEN_RE.search(value):
            decorative_loop = True

    return {
        "duration_values_ms": sorted(durations),
        "easing_signatures": sorted(easings),
        "transition_properties": sorted(properties),
        "has_decorative_loop": decorative_loop,
        # Distinct entry and exit curves mean the motion was designed rather
        # than applied uniformly.
        "enter_exit_asymmetry": len(easings & {"enter", "exit"}) == 2
        or len({e for e in easings if e.startswith("cubic-bezier")}) >= 2,
    }


def _composition_markers(text: str) -> list[str]:
    marker_terms = {
        "header": ("header", "topbar", "app-bar"),
        "sidebar": ("sidebar", "side-nav", "navigation-rail"),
        "hero": ("hero", "masthead"),
        "card-grid": ("card-grid", "grid-cols-3", "grid-cols-4", "feature-card", "metric-card"),
        "metric-strip": ("metric-strip", "stat-strip", "kpi-strip"),
        "filter-bar": ("filter-bar", "filter-row", "filter-toolbar"),
        "table": ("data-table", "table-row", "table-header", "<table"),
        "split-pane": ("split-pane", "split-workbench", "master-detail", "detail-pane"),
        "inspector": ("inspector", "property-panel", "context-panel"),
        "timeline": ("timeline", "activity-stream", "event-rail"),
        "canvas": ("canvas", "node-graph", "map-canvas", "spatial"),
        "feed": ("feed", "post-list", "stream-item"),
        "tabs": ("tab-list", "tablist", "segmented-control"),
        "drawer": ("drawer", "bottom-sheet", "side-sheet"),
        "bottom-nav": ("bottom-nav", "tab-bar", "mobile-nav"),
        "command-bar": ("command-bar", "command-palette", "omnibox"),
        "chart": ("chart", "plot", "sparkline"),
        "match-ticker": ("match-ticker", "ticker-rail", "score-ticker"),
        "source-ledger": ("source-ledger", "source ledger"),
        "status-strip": ("status-strip", "status strip"),
        "fixture-workspace": ("schedule-table", "fixture-review-workspace", "standings-table"),
        "footer": ("footer",),
    }
    lowered = text.lower()
    return sorted(
        marker
        for marker, terms in marker_terms.items()
        if any(term in lowered for term in terms)
    )


def extract_style_fingerprint(
    project_dir: Path,
    *,
    project_name: str | None = None,
    source_files: list[Path] | None = None,
    read_evidence: dict[str, dict[str, Any]] | None = None,
) -> StyleFingerprint:
    project_dir = project_dir.resolve()
    files = (
        list(source_files)
        if source_files is not None
        else _collect_source_files(project_dir)
    )
    files = sorted(files, key=lambda path: path.as_posix())
    if not files:
        raise FileNotFoundError(
            f"No HTML/CSS implementation files found under {project_dir}. "
            "Run this against the directory that holds the final mockup."
        )

    texts: dict[str, str] = {}
    source_records: list[dict[str, Any]] = []
    for path in files:
        resolved = path.resolve()
        if not resolved.is_relative_to(project_dir):
            raise ValueError(
                f"Style fingerprint source resolves outside {project_dir}: {path} -> {resolved}"
            )
        try:
            relative = path.relative_to(project_dir).as_posix()
        except ValueError as exc:
            raise ValueError(
                f"Style fingerprint source must stay inside {project_dir}: {path}"
            ) from exc
        try:
            raw = resolved.read_bytes()
            texts[relative] = raw.decode("utf-8")
        except (OSError, UnicodeDecodeError) as exc:
            raise ValueError(f"Style fingerprint source is unreadable: {relative}: {exc}") from exc
        record = {
            "path": relative,
            "sha256": hashlib.sha256(raw).hexdigest(),
            "size_bytes": len(raw),
        }
        source_records.append(record)
        if read_evidence is not None:
            read_evidence[relative] = dict(record)

    combined = "\n".join(texts.values())
    custom_props: dict[str, str] = {}
    for match in CUSTOM_PROP_RE.finditer(combined):
        custom_props.setdefault(match.group("name"), match.group("value"))

    color_counts: dict[str, int] = {}
    for match in HEX_RE.finditer(combined):
        value = _normalize_hex(match.group(0))
        color_counts[value] = color_counts.get(value, 0) + 1
    for match in RGB_RE.finditer(combined):
        r, g, b = (min(int(match.group(k)), 255) for k in ("r", "g", "b"))
        value = _normalize_hex(f"#{r:02X}{g:02X}{b:02X}")
        color_counts[value] = color_counts.get(value, 0) + 1

    background_hexes: list[str] = []
    for match in BACKGROUND_DECL_RE.finditer(combined):
        resolved = _resolve_color_token(match.group("value"), custom_props)
        if resolved:
            background_hexes.append(resolved)
    if not background_hexes:
        background_hexes = [
            value for value in color_counts if _hex_to_hls(value)[1] >= 0.78
        ]

    surface_tone, surface_hexes = _classify_surface(background_hexes)
    # Dark-mode support is a capability, not a surface tone. Overwriting the
    # measured tone with "dual-theme" made every emit-tokens project report the
    # same value, so the axis stopped separating anything while still adding to
    # the similarity score.
    supports_dark_theme = bool(
        re.search(r":root\s*\{", combined, re.IGNORECASE)
        and re.search(
            r"html\s*\[\s*data-theme\s*=\s*['\"]dark['\"]\s*\]",
            combined,
            re.IGNORECASE,
        )
    )

    # Prefer the brand's own colour choices. Falling back to every saturated
    # colour in the file (the old behaviour) swept in status, link and text
    # colours, so any two token-bound projects looked alike.
    brand_hexes: list[str] = []
    for block in ROOT_BLOCK_RE.finditer(combined):
        for match in BRAND_ACCENT_DECL_RE.finditer(block.group("body")):
            resolved = _resolve_color_token(match.group("value"), custom_props)
            if resolved and resolved not in brand_hexes:
                brand_hexes.append(resolved)

    accent_entries: list[tuple[str, str, int]] = []
    if brand_hexes:
        for value in brand_hexes:
            _, lightness, saturation = _hex_to_hls(value)
            if saturation >= 0.22 and 0.14 <= lightness <= 0.74:
                accent_entries.append(
                    (_hue_bucket(_hex_to_hls(value)[0]), value, color_counts.get(value, 1))
                )
    else:
        # No design-system tokens (hand-authored CSS): fall back to the old scan
        # so attractor detection still works on legacy surfaces.
        for value, count in color_counts.items():
            _, lightness, saturation = _hex_to_hls(value)
            if saturation >= 0.22 and 0.14 <= lightness <= 0.74:
                accent_entries.append((_hue_bucket(_hex_to_hls(value)[0]), value, count))
    accent_entries.sort(key=lambda item: item[2], reverse=True)
    accent_buckets: list[str] = []
    accent_hexes: list[str] = []
    for bucket, value, _ in accent_entries:
        if bucket not in accent_buckets:
            accent_buckets.append(bucket)
        if len(accent_hexes) < 8:
            accent_hexes.append(value)

    families, serif_accent = _extract_fonts(combined)

    radius_values: set[float] = set()
    uses_pill = False
    for match in BORDER_RADIUS_RE.finditer(combined):
        value = match.group("value")
        if "%" in value or "9999" in value or "999px" in value:
            uses_pill = True
        for px in RADIUS_PX_RE.finditer(value):
            number = float(px.group(1))
            if number >= 200:
                uses_pill = True
            else:
                radius_values.add(number)

    css_only = "\n".join(
        text for name, text in texts.items() if name.lower().endswith(".css")
    )
    return StyleFingerprint(
        project=project_name or project_dir.name,
        source_files=sorted(texts),
        source_snapshot_sha256=hashlib.sha256(
            json.dumps(
                source_records,
                ensure_ascii=False,
                sort_keys=True,
                separators=(",", ":"),
            ).encode("utf-8")
        ).hexdigest(),
        surface_tone=surface_tone,
        surface_hexes=surface_hexes,
        accent_hue_buckets=accent_buckets,
        accent_hexes=accent_hexes,
        font_families=families,
        serif_accent=serif_accent,
        radius_values_px=sorted(radius_values),
        uses_pill_shapes=uses_pill,
        color_count=len(color_counts),
        supports_dark_theme=supports_dark_theme,
        separation_style=_detect_separation_style(css_only or combined),
        composition_markers=_composition_markers(combined),
        **_extract_motion_signature(css_only or combined),
    )


# ---------------------------------------------------------------------------
# Registry


def default_registry_path(repo_root: Path) -> Path:
    return repo_root / DEFAULT_REGISTRY_RELATIVE_PATH


def load_registry(registry_path: Path) -> dict[str, Any]:
    if not registry_path.exists():
        return {"schema_version": REGISTRY_SCHEMA_VERSION, "entries": []}
    data = json.loads(registry_path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError(f"Style fingerprint registry must be a JSON object: {registry_path}")
    if data.get("schema_version") != REGISTRY_SCHEMA_VERSION:
        raise ValueError(
            f"Style fingerprint registry schema_version must be {REGISTRY_SCHEMA_VERSION}: "
            f"{registry_path}"
        )
    entries = data.get("entries")
    if not isinstance(entries, list):
        raise ValueError(f"Style fingerprint registry entries must be a list: {registry_path}")
    seen_projects: set[str] = set()
    for index, entry in enumerate(entries):
        prefix = f"registry entries[{index}]"
        if not isinstance(entry, dict):
            raise ValueError(f"{prefix} must be an object")
        if not isinstance(entry.get("project"), str) or not entry["project"].strip():
            raise ValueError(f"{prefix}.project must be a non-empty string")
        project = entry["project"].strip()
        if project in seen_projects:
            raise ValueError(f"{prefix}.project duplicates an earlier registry entry: {project}")
        seen_projects.add(project)
        fingerprint = entry.get("fingerprint")
        if not isinstance(fingerprint, dict):
            raise ValueError(f"{prefix}.fingerprint must be an object")
        if fingerprint.get("schema_version") != FINGERPRINT_SCHEMA_VERSION:
            raise ValueError(
                f"{prefix}.fingerprint.schema_version must be {FINGERPRINT_SCHEMA_VERSION}"
            )
        _validate_registry_fingerprint(fingerprint, project=project, prefix=prefix)
    return data


def _validate_registry_fingerprint(
    fingerprint: dict[str, Any],
    *,
    project: str,
    prefix: str,
) -> None:
    """Validate the comparison-bearing v1 fields without requiring newer additions."""

    string_fields = ("project", "surface_tone", "separation_style")
    string_list_fields = (
        "source_files",
        "surface_hexes",
        "accent_hue_buckets",
        "accent_hexes",
        "font_families",
    )
    for field_name in string_fields:
        value = fingerprint.get(field_name)
        if not isinstance(value, str) or not value.strip():
            raise ValueError(f"{prefix}.fingerprint.{field_name} must be a non-empty string")
    if fingerprint["project"].strip() != project:
        raise ValueError(f"{prefix}.fingerprint.project must match the registry project")
    for field_name in string_list_fields:
        value = fingerprint.get(field_name)
        if not isinstance(value, list) or any(not isinstance(item, str) for item in value):
            raise ValueError(f"{prefix}.fingerprint.{field_name} must be a string list")
    for field_name in ("serif_accent", "uses_pill_shapes"):
        if not isinstance(fingerprint.get(field_name), bool):
            raise ValueError(f"{prefix}.fingerprint.{field_name} must be boolean")
    radius_values = fingerprint.get("radius_values_px")
    if not isinstance(radius_values, list) or any(
        isinstance(item, bool) or not isinstance(item, (int, float))
        for item in radius_values
    ):
        raise ValueError(f"{prefix}.fingerprint.radius_values_px must be a number list")
    color_count = fingerprint.get("color_count")
    if isinstance(color_count, bool) or not isinstance(color_count, int) or color_count < 0:
        raise ValueError(f"{prefix}.fingerprint.color_count must be a non-negative integer")
    composition_markers = fingerprint.get("composition_markers")
    if composition_markers is not None and (
        not isinstance(composition_markers, list)
        or any(not isinstance(item, str) for item in composition_markers)
    ):
        raise ValueError(f"{prefix}.fingerprint.composition_markers must be a string list")
    source_snapshot = fingerprint.get("source_snapshot_sha256")
    if source_snapshot is not None and (
        not isinstance(source_snapshot, str)
        or not re.fullmatch(r"[a-f0-9]{64}", source_snapshot)
    ):
        raise ValueError(f"{prefix}.fingerprint.source_snapshot_sha256 must be a lowercase sha256")


def register_fingerprint(
    registry_path: Path,
    fingerprint: StyleFingerprint,
    *,
    note: str | None = None,
) -> dict[str, Any]:
    registry_path.parent.mkdir(parents=True, exist_ok=True)
    with _registry_lock(registry_path):
        registry = load_registry(registry_path)
        entry = _upsert_registry_fingerprint(registry, fingerprint, note=note)
        _write_registry_atomic(registry_path, registry)
    return entry


def _upsert_registry_fingerprint(
    registry: dict[str, Any],
    fingerprint: StyleFingerprint,
    *,
    note: str | None,
) -> dict[str, Any]:
    entries = registry["entries"]
    entry = {
        "project": fingerprint.project,
        "recorded_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "note": note,
        "fingerprint": fingerprint.to_dict(),
    }
    entries[:] = [item for item in entries if item.get("project") != fingerprint.project]
    entries.append(entry)
    return entry


@contextmanager
def _registry_lock(registry_path: Path) -> Iterator[None]:
    """Serialize shared registry read-modify-write operations across supported OSes."""

    lock_path = registry_path.with_name(f".{registry_path.name}.lock")
    with lock_path.open("a+", encoding="utf-8") as lock_handle:
        if fcntl is not None:
            fcntl.flock(lock_handle.fileno(), fcntl.LOCK_EX)
        elif msvcrt is not None:  # pragma: no cover - exercised on Windows.
            lock_handle.seek(0, os.SEEK_END)
            if lock_handle.tell() == 0:
                lock_handle.write("\0")
                lock_handle.flush()
            lock_handle.seek(0)
            msvcrt.locking(lock_handle.fileno(), msvcrt.LK_LOCK, 1)
        try:
            yield
        finally:
            if fcntl is not None:
                fcntl.flock(lock_handle.fileno(), fcntl.LOCK_UN)
            elif msvcrt is not None:  # pragma: no cover - exercised on Windows.
                lock_handle.seek(0)
                msvcrt.locking(lock_handle.fileno(), msvcrt.LK_UNLCK, 1)


def _write_registry_atomic(registry_path: Path, registry: dict[str, Any]) -> None:
    """Durably replace a validated registry without exposing a partial JSON file."""

    descriptor, temporary_name = tempfile.mkstemp(
        dir=registry_path.parent,
        prefix=f".{registry_path.name}.",
        suffix=".tmp",
    )
    temporary_path = Path(temporary_name)
    try:
        existing_mode = (
            registry_path.stat().st_mode & 0o777 if registry_path.exists() else 0o644
        )
        os.fchmod(descriptor, existing_mode)
        with os.fdopen(descriptor, "w", encoding="utf-8") as handle:
            json.dump(registry, handle, ensure_ascii=False, indent=2)
            handle.write("\n")
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temporary_path, registry_path)
        try:
            directory_descriptor = os.open(registry_path.parent, os.O_RDONLY)
            try:
                os.fsync(directory_descriptor)
            finally:
                os.close(directory_descriptor)
        except OSError:
            pass
    finally:
        temporary_path.unlink(missing_ok=True)


# ---------------------------------------------------------------------------
# Comparison / divergence gate


def compare_fingerprints(a: StyleFingerprint | dict, b: StyleFingerprint | dict) -> dict[str, Any]:
    fa = a.to_dict() if isinstance(a, StyleFingerprint) else a
    fb = b.to_dict() if isinstance(b, StyleFingerprint) else b

    reasons: list[str] = []
    score = 0.0

    if fa.get("surface_tone") == fb.get("surface_tone") and fa.get("surface_tone") != "unknown":
        score += 0.22
        reasons.append(f"surface tone 동일 ({fa.get('surface_tone')})")

    buckets_a = set(fa.get("accent_hue_buckets") or [])
    buckets_b = set(fb.get("accent_hue_buckets") or [])
    if buckets_a or buckets_b:
        jaccard = len(buckets_a & buckets_b) / max(len(buckets_a | buckets_b), 1)
        score += 0.30 * jaccard
        if jaccard >= 0.5:
            shared = ", ".join(sorted(buckets_a & buckets_b))
            reasons.append(f"accent hue 중복 {jaccard:.0%} ({shared})")

    fonts_a = {name.lower() for name in fa.get("font_families") or []}
    fonts_b = {name.lower() for name in fb.get("font_families") or []}
    if fonts_a or fonts_b:
        font_jaccard = len(fonts_a & fonts_b) / max(len(fonts_a | fonts_b), 1)
        score += 0.18 * font_jaccard
        if font_jaccard >= 0.5:
            reasons.append(
                "font pairing 중복 (" + ", ".join(sorted(fonts_a & fonts_b)) + ")"
            )

    if fa.get("serif_accent") and fb.get("serif_accent"):
        score += 0.08
        reasons.append("둘 다 serif display accent 사용")
    elif not fa.get("serif_accent") and not fb.get("serif_accent"):
        score += 0.03

    sep_a = fa.get("separation_style") or "unknown"
    sep_b = fb.get("separation_style") or "unknown"
    if sep_a != "unknown" and sep_a == sep_b:
        score += 0.12
        reasons.append(f"구성 문법 동일 ({sep_a})")

    markers_a = set(fa.get("composition_markers") or [])
    markers_b = set(fb.get("composition_markers") or [])
    structural_similarity = 0.0
    if markers_a or markers_b:
        structural_similarity = len(markers_a & markers_b) / max(len(markers_a | markers_b), 1)
        score += 0.25 * structural_similarity
        if structural_similarity >= 0.6:
            reasons.append(
                "구성 마커 중복 "
                f"{structural_similarity:.0%} ({', '.join(sorted(markers_a & markers_b))})"
            )

    radii_a = fa.get("radius_values_px") or []
    radii_b = fb.get("radius_values_px") or []
    if radii_a and radii_b:
        max_a, max_b = max(radii_a), max(radii_b)
        if abs(max_a - max_b) <= 4 and fa.get("uses_pill_shapes") == fb.get("uses_pill_shapes"):
            score += 0.10

    motion_similarity = 0.0
    durations_a = {float(value) for value in fa.get("duration_values_ms") or []}
    durations_b = {float(value) for value in fb.get("duration_values_ms") or []}
    easings_a = {str(value) for value in fa.get("easing_signatures") or []}
    easings_b = {str(value) for value in fb.get("easing_signatures") or []}
    if (durations_a or durations_b) and (easings_a or easings_b):
        duration_overlap = len(durations_a & durations_b) / max(len(durations_a | durations_b), 1)
        easing_overlap = len(easings_a & easings_b) / max(len(easings_a | easings_b), 1)
        motion_similarity = (duration_overlap + easing_overlap) / 2
        score += 0.12 * motion_similarity
        if duration_overlap >= 0.75 and easing_overlap >= 0.75:
            reasons.append(
                f"모션 문법 중복 {motion_similarity:.0%} "
                f"(duration {sorted(durations_a & durations_b)}, easing {sorted(easings_a & easings_b)})"
            )

    return {
        "project_a": fa.get("project"),
        "project_b": fb.get("project"),
        "similarity": round(min(score, 1.0), 4),
        "structural_similarity": round(structural_similarity, 4),
        "motion_similarity": round(motion_similarity, 4),
        "shared_composition_markers": sorted(markers_a & markers_b),
        "reasons": reasons,
    }


def detect_attractors(
    fingerprint: StyleFingerprint | dict,
    *,
    serif_sanctioned: bool = False,
) -> list[dict[str, Any]]:
    """Match known convergence attractors.

    ``serif_sanctioned=True`` means the project's blueprint font_system chose a
    serif display/heading on purpose (editorial, fashion, luxury domains). In
    that case serif-based attractors are waived — the ban targets improvised
    serif accents, not domain-appropriate token-bound ones.
    """

    fp = fingerprint.to_dict() if isinstance(fingerprint, StyleFingerprint) else fingerprint
    buckets = set(fp.get("accent_hue_buckets") or [])
    matches: list[dict[str, Any]] = []
    for attractor in KNOWN_ATTRACTORS:
        if attractor.get("requires_serif_accent") and serif_sanctioned:
            continue
        if fp.get("surface_tone") not in attractor["surface_tones"]:
            continue
        if attractor.get("requires_serif_accent") and not fp.get("serif_accent"):
            continue
        restrict = attractor.get("restrict_to_hues")
        if restrict is not None and (not buckets or not buckets <= restrict):
            continue
        groups_ok = all(buckets & group for group in attractor["required_hue_groups"])
        if not groups_ok:
            continue
        matches.append(
            {
                "id": attractor["id"],
                "label": attractor["label"],
                "description": attractor["description"],
            }
        )
    return matches


def _divergence_suggestions(
    fingerprint: StyleFingerprint,
    recent_entries: list[dict[str, Any]],
) -> list[str]:
    suggestions: list[str] = []
    used_buckets: dict[str, int] = {}
    used_tones: dict[str, int] = {}
    used_fonts: dict[str, int] = {}
    for entry in recent_entries:
        fp = entry.get("fingerprint") or {}
        for bucket in fp.get("accent_hue_buckets") or []:
            used_buckets[bucket] = used_buckets.get(bucket, 0) + 1
        tone = fp.get("surface_tone")
        if tone:
            used_tones[tone] = used_tones.get(tone, 0) + 1
        for font in fp.get("font_families") or []:
            used_fonts[font.lower()] = used_fonts.get(font.lower(), 0) + 1

    unused_buckets = [name for name in HUE_BUCKET_NAMES if name not in used_buckets]
    if recent_entries and unused_buckets:
        suggestions.append(
            "최근 프로젝트들이 쓰지 않은 accent hue 계열에서 primary를 고르세요: "
            + ", ".join(unused_buckets[:6])
        )
    overused = [name for name, count in used_buckets.items() if count >= 2]
    if overused:
        suggestions.append(
            "최근 2회 이상 반복된 accent hue는 피하세요: " + ", ".join(sorted(overused))
        )
    tone_counts = sorted(used_tones.items(), key=lambda item: item[1], reverse=True)
    if tone_counts and fingerprint.surface_tone == tone_counts[0][0]:
        suggestions.append(
            f"surface tone `{fingerprint.surface_tone}`이 최근 가장 많이 반복된 톤입니다. "
            "blueprint token_schema의 배경 토큰을 그대로 쓰거나 다른 톤 계열로 옮기세요."
        )
    used_separations: dict[str, int] = {}
    for entry in recent_entries:
        style = (entry.get("fingerprint") or {}).get("separation_style")
        if style and style != "unknown":
            used_separations[style] = used_separations.get(style, 0) + 1
    if (
        fingerprint.separation_style != "unknown"
        and used_separations.get(fingerprint.separation_style, 0) >= 2
    ):
        suggestions.append(
            f"구성 문법 `{fingerprint.separation_style}`이 최근 프로젝트들과 반복됩니다. "
            "분리 문법 자체를 바꾸세요 — hairline-rows ↔ whitespace(여백·스케일 분리) ↔ "
            "split-panel, dark instrument panel, 풀블리드 섹션 같은 다른 골격을 검토."
        )
    repeated_fonts = [
        name for name in (f.lower() for f in fingerprint.font_families)
        if used_fonts.get(name, 0) >= 2 and name != "pretendard"
    ]
    if repeated_fonts:
        suggestions.append(
            "display/accent 서체가 최근 프로젝트들과 중복됩니다: "
            + ", ".join(sorted(set(repeated_fonts)))
            + " — docs/font-reference.md에서 다른 계열을 고르세요."
        )
    suggestions.append(
        "색·서체를 임의로 정하지 말고 build/system/blueprint/token_schema.json의 "
        "active palette와 recommended_fonts를 tokens.css로 방출해 소비하세요 (emit-tokens)."
    )
    return suggestions


def _blueprint_sanctions_serif(project_dir: Path) -> bool:
    """True when the project blueprint's font_system chose a serif on purpose."""

    import json

    blueprint_path = (
        project_dir / "build" / "system" / "blueprint" / "design_system_blueprint.json"
    )
    if not blueprint_path.exists():
        return False
    try:
        blueprint = json.loads(blueprint_path.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return False
    font_system = blueprint.get("font_system") or {}
    for slot in ("display", "heading"):
        entry = font_system.get(slot)
        if isinstance(entry, dict) and "serif" in str(entry.get("family", "")).lower():
            return True
    return False


def check_style_divergence(
    project_dir: Path,
    *,
    registry_path: Path,
    threshold: float = DEFAULT_SIMILARITY_THRESHOLD,
    limit: int = DEFAULT_COMPARE_LIMIT,
    fingerprint: StyleFingerprint | None = None,
) -> dict[str, Any]:
    fingerprint = fingerprint or extract_style_fingerprint(project_dir)
    serif_sanctioned = _blueprint_sanctions_serif(Path(project_dir))
    registry = load_registry(registry_path)
    return _check_style_divergence_against_registry(
        fingerprint,
        registry=registry,
        threshold=threshold,
        limit=limit,
        serif_sanctioned=serif_sanctioned,
    )


def _check_style_divergence_against_registry(
    fingerprint: StyleFingerprint,
    *,
    registry: dict[str, Any],
    threshold: float,
    limit: int,
    serif_sanctioned: bool,
) -> dict[str, Any]:
    entries = [
        entry
        for entry in registry.get("entries", [])
        if entry.get("project") != fingerprint.project
    ]
    recent = entries[-limit:]

    comparisons = [
        {
            **compare_fingerprints(fingerprint, entry.get("fingerprint") or {}),
            "project_b": entry.get("project"),
        }
        for entry in recent
    ]
    comparisons.sort(key=lambda item: item["similarity"], reverse=True)
    too_similar = [
        item
        for item in comparisons
        if item["similarity"] >= threshold
        or (
            item.get("structural_similarity", 0.0) >= 0.85
            and len(item.get("shared_composition_markers") or []) >= 4
        )
    ]
    attractors = detect_attractors(fingerprint, serif_sanctioned=serif_sanctioned)

    verdict = "fail" if (too_similar or attractors) else "ok"

    warnings: list[str] = []
    if recent:
        last_fp = (recent[-1].get("fingerprint") or {})
        last_sep = last_fp.get("separation_style")
        if (
            fingerprint.separation_style != "unknown"
            and fingerprint.separation_style == last_sep
        ):
            warnings.append(
                f"직전 프로젝트({recent[-1].get('project')})와 구성 문법이 같습니다 "
                f"({fingerprint.separation_style}). 색·폰트가 달라도 골격이 같으면 "
                "비슷하게 읽힙니다 — 분리 문법이나 밀도 구조를 의도적으로 바꾸는 것을 검토하세요."
            )

    report: dict[str, Any] = {
        "schema_version": "style-divergence-report/v1",
        "project": fingerprint.project,
        "verdict": verdict,
        "threshold": threshold,
        "registry_snapshot_sha256": hashlib.sha256(
            json.dumps(
                registry,
                ensure_ascii=False,
                sort_keys=True,
                separators=(",", ":"),
            ).encode("utf-8")
        ).hexdigest(),
        "serif_sanctioned_by_blueprint": serif_sanctioned,
        "fingerprint": fingerprint.to_dict(),
        "attractor_matches": attractors,
        "too_similar_to": too_similar,
        "warnings": warnings,
        "comparisons": comparisons,
    }
    if verdict == "fail":
        report["suggestions"] = _divergence_suggestions(fingerprint, recent)
    return report


def check_and_register_fingerprint(
    project_dir: Path,
    *,
    registry_path: Path,
    fingerprint: StyleFingerprint,
    threshold: float = DEFAULT_SIMILARITY_THRESHOLD,
    limit: int = DEFAULT_COMPARE_LIMIT,
    note: str | None = None,
) -> tuple[dict[str, Any], dict[str, Any] | None]:
    """Recheck divergence and register under one shared-registry lock."""

    registry_path.parent.mkdir(parents=True, exist_ok=True)
    serif_sanctioned = _blueprint_sanctions_serif(Path(project_dir))
    with _registry_lock(registry_path):
        registry = load_registry(registry_path)
        report = _check_style_divergence_against_registry(
            fingerprint,
            registry=registry,
            threshold=threshold,
            limit=limit,
            serif_sanctioned=serif_sanctioned,
        )
        if report.get("verdict") != "ok":
            return report, None
        entry = _upsert_registry_fingerprint(registry, fingerprint, note=note)
        _write_registry_atomic(registry_path, registry)
    return report, entry


def format_divergence_report(report: dict[str, Any]) -> str:
    lines: list[str] = []
    verdict = report.get("verdict", "unknown").upper()
    lines.append(f"Style divergence: {verdict} (project={report.get('project')})")
    fp = report.get("fingerprint") or {}
    lines.append(
        "  fingerprint: "
        f"surface={fp.get('surface_tone')}, "
        f"accents={','.join(fp.get('accent_hue_buckets') or []) or '-'}, "
        f"fonts={','.join(fp.get('font_families') or []) or '-'}, "
        f"serif_accent={fp.get('serif_accent')}"
    )
    for attractor in report.get("attractor_matches") or []:
        lines.append(f"  [ATTRACTOR] {attractor['label']}")
        lines.append(f"    {attractor['description']}")
    for item in report.get("too_similar_to") or []:
        lines.append(
            f"  [TOO-SIMILAR] {item['project_b']} similarity={item['similarity']:.2f}"
        )
        for reason in item.get("reasons", []):
            lines.append(f"    - {reason}")
    for warning in report.get("warnings") or []:
        lines.append(f"  [WARN] {warning}")
    for suggestion in report.get("suggestions") or []:
        lines.append(f"  [FIX] {suggestion}")
    if verdict == "OK" and report.get("comparisons"):
        top = report["comparisons"][0]
        lines.append(
            f"  closest: {top['project_b']} similarity={top['similarity']:.2f}"
        )
    return "\n".join(lines)
