"""Implementation linting for installed design-system contracts.

This linter guards the failure mode where an external visual reference leaks
into implementation files as hard-coded palette, font, or radius decisions.
Generated design-system artifacts remain allowed to contain raw token values;
application code should bind back to `--ds-*` variables.
"""

from __future__ import annotations

import json
import re
from dataclasses import asdict, dataclass, field
from pathlib import Path

from .adapters.base import DS_BLOCK_END, DS_BLOCK_START


DEFAULT_INCLUDE_EXTENSIONS = {
    ".css",
    ".scss",
    ".sass",
    ".less",
    ".html",
    ".tsx",
    ".jsx",
    ".ts",
    ".js",
    ".vue",
    ".svelte",
}

UI_MARKUP_EXTENSIONS = {
    ".html",
    ".tsx",
    ".jsx",
    ".vue",
    ".svelte",
}

DEFAULT_EXCLUDED_DIRS = {
    ".git",
    ".next",
    ".nuxt",
    ".svelte-kit",
    ".turbo",
    ".venv",
    "build",
    "coverage",
    "dist",
    "node_modules",
    "screenshots",
}

COLOR_LITERAL_RE = re.compile(r"(?<![\w-])#[0-9a-fA-F]{3,8}\b")
COLOR_FUNCTION_RE = re.compile(
    r"\b(?:rgba?|hsla?|hwb|lab|lch|oklab|oklch|color)\s*\(",
    re.IGNORECASE,
)
FONT_FAMILY_RE = re.compile(r"\bfont-family\s*:\s*([^;]+)", re.IGNORECASE)
RADIUS_RE = re.compile(
    r"\bborder(?:-(?:top|right|bottom|left|start|end))?(?:-(?:left|right|start|end))?-radius\s*:\s*([^;]+)",
    re.IGNORECASE,
)
CUSTOM_PROPERTY_RE = re.compile(r"(?P<name>--[a-zA-Z0-9_-]+)\s*:\s*(?P<value>[^;]+)")
COLOR_MIX_RE = re.compile(r"\bcolor-mix\s*\(", re.IGNORECASE)
DS_COLOR_TOKEN_RE = re.compile(r"var\(\s*(--ds-color-[a-z0-9-]+)", re.IGNORECASE)

NAMED_COLOR_RE = re.compile(
    r"\b(?:black|white|red|green|blue|yellow|purple|orange|gray|grey|slate|teal|cyan|magenta|pink|brown)\b",
    re.IGNORECASE,
)

COLOR_PROPERTY_RE = re.compile(
    r"\b(?:color|background|background-color|border|border-color|outline|outline-color|box-shadow|text-shadow|fill|stroke)\s*:",
    re.IGNORECASE,
)

ALLOWED_RADIUS_VALUES = {"0", "0px", "50%", "999px", "inherit", "initial", "unset"}

NEUTRAL_COLOR_TOKENS = {
    "--ds-color-canvas",
    "--ds-color-surface",
    "--ds-color-surface-muted",
    "--ds-color-surface-elevated",
    "--ds-color-border",
    "--ds-color-border-strong",
    "--ds-color-ink",
    "--ds-color-ink-muted",
    "--ds-color-ink-subtle",
    "--ds-color-ink-inverse",
}

REFERENCE_RISK_COLOR_TOKENS = {
    "--ds-color-info",
    "--ds-color-surface-tint",
}

STRUCTURAL_CUSTOM_PROPERTY_RE = re.compile(
    r"--(?:.*(?:app|shell|sidebar|rail|nav|chrome|layout|panel|card|chart|graph|data|secondary|tertiary|surface|bg|background).*)",
    re.IGNORECASE,
)
WIDTH_DECLARATION_RE = re.compile(
    r"\b(?P<prop>width|inline-size|min-width|min-inline-size)\s*:\s*(?P<value>[^;}{]+)",
    re.IGNORECASE,
)
FLEX_WRAP_NOWRAP_RE = re.compile(r"\bflex-wrap\s*:\s*nowrap\b", re.IGNORECASE)
WHITE_SPACE_NOWRAP_RE = re.compile(r"\bwhite-space\s*:\s*nowrap\b", re.IGNORECASE)
TAILWIND_FIXED_WIDTH_RE = re.compile(r"\b(?P<class>(?:min-w|w)-\[(?P<value>\d+)px\])")
TAILWIND_SCREEN_WIDTH_RE = re.compile(r"\bw-screen\b")
TAILWIND_NOWRAP_RE = re.compile(r"\bwhitespace-nowrap\b")
EMOJI_RE = re.compile(r"[\U0001F300-\U0001FAFF\u2600-\u27BF]")
COLOR_SCHEME_DARK_RE = re.compile(r"\bcolor-scheme\s*:\s*dark\b", re.IGNORECASE)
COLOR_SCHEME_LIGHT_RE = re.compile(r"\bcolor-scheme\s*:\s*light\b", re.IGNORECASE)
DARK_MODE_MARKER_RE = re.compile(r"(?:data-theme=['\"]dark['\"]|prefers-color-scheme\s*:\s*dark|\bcolor-scheme\s*:\s*dark\b)", re.IGNORECASE)
LIGHT_MODE_MARKER_RE = re.compile(r"(?:data-theme=['\"]light['\"]|\bcolor-scheme\s*:\s*light\b)", re.IGNORECASE)
BUTTON_LIKE_CONTEXT_RE = re.compile(
    r"(?:^|[\s.#:'\"`_\-/])(?:button|btn|cta|tab|chip|filter-chip|toolbar|action-button|primary-action)(?:$|[\s.#:'\"`_\-/\]])",
    re.IGNORECASE,
)
ACTION_GROUP_CONTEXT_RE = re.compile(
    r"(?:^|[\s.#:'\"`_\-/])(?:actions?|action-row|button-group|button-row|cta-row|toolbar|control-row|form-actions)(?:$|[\s.#:'\"`_\-/\]])",
    re.IGNORECASE,
)
EMOJI_UI_CONTEXT_RE = re.compile(
    r"(?:^|[\s.#<:'\"`_\-/])(?:button|btn|cta|card|tile|badge|chip|tab|nav|status|state|toast|banner|alert|empty-state|icon|marker)(?:$|[\s.#>:'\"`_\-/\]])",
    re.IGNORECASE,
)
EMOJI_CONTENT_CONTEXT_RE = re.compile(
    r"(?:emoji[-_]?picker|emojiPicker|reaction-data|user-generated|user-content|chat-message|comment-body|blog-body|article-body|markdown|prose)",
    re.IGNORECASE,
)
CARD_PANEL_TOKEN_RE = re.compile(r"\b[a-z0-9_-]*(?:card|panel)[a-z0-9_-]*\b", re.IGNORECASE)
LAYOUT_DIVERSITY_TOKEN_RE = re.compile(
    r"\b(?:row|table|rail|canvas|map-zone|map-visual|sketch|illustration|figure|media|timeline|split|inspector-rail|list-row|data-table|toolbar|strip|sheet|scene)\b",
    re.IGNORECASE,
)
INTERACTIVE_UI_RE = re.compile(
    r"(?:<(?:button|select|input|nav|a)\b|role=['\"](?:button|tab|navigation|switch|checkbox)['\"]|class(?:Name)?=['\"][^'\"]*(?:button|btn|cta|chip|tab|filter|nav|toolbar|action|status|badge)[^'\"]*)",
    re.IGNORECASE,
)
VISUAL_AFFORDANCE_RE = re.compile(
    r"(?:<svg\b|<img\b|<picture\b|<video\b|<canvas\b|<use\b|use\s+href=|href=['\"]#icon-|lucide-|heroicon|icon-|Icon[A-Z]|background-image|mask-image)",
    re.IGNORECASE,
)
DOMAIN_VISUAL_RE = re.compile(
    r"(?:<img\b|<picture\b|<video\b|<canvas\b|class(?:Name)?=['\"][^'\"]*(?:sketch|illustration|map|visual|media|figure|thumbnail|photo|image|texture|scene|sprite)[^'\"]*)",
    re.IGNORECASE,
)
DOMAIN_INLINE_SVG_RE = re.compile(r"<svg\b(?P<attrs>[^>]*)>(?P<body>.*?)</svg>", re.IGNORECASE | re.DOTALL)
DOMAIN_VISUAL_SVG_HINT_RE = re.compile(
    r"(?:class(?:Name)?=['\"][^'\"]*(?:sketch|illustration|map|visual|scene|diagram)[^'\"]*|aria-label=['\"][^'\"]*(?:그림|지도|일러스트|스케치|image|map|sketch|illustration|diagram)[^'\"]*)",
    re.IGNORECASE,
)
SVG_SHAPE_RE = re.compile(r"<(?:path|circle|rect|line|polyline|polygon|ellipse)\b", re.IGNORECASE)
SEMANTIC_DOMAIN_VISUAL_ANCHOR_RE = re.compile(
    r"(?:<title\b|<desc\b|<text\b|data-(?:subject|landmark|evidence|visual|place|slot)=|aria-labelledby=)",
    re.IGNORECASE,
)
AD_HOC_ILLUSTRATION_RE = re.compile(
    r"\b(?:sketch|doodle|hand-?drawn|rough-illustration|placeholder-illustration)\b",
    re.IGNORECASE,
)
AMBIGUOUS_MOCK_SURFACE_RE = re.compile(
    r"\b(?:schematic|mock-map|mock-visual|placeholder-visual|placeholder-map|도식)\b",
    re.IGNORECASE,
)
RUNTIME_SURFACE_MARKER_RE = re.compile(r"\bdata-runtime-surface\s*=", re.IGNORECASE)
MEDIA_RUNTIME_SURFACE_RE = re.compile(
    r"\bdata-runtime-surface\s*=\s*['\"][^'\"]*(?:media|photo|thumbnail|image|generated|sourced)[^'\"]*['\"]",
    re.IGNORECASE,
)
MEDIA_ASSET_RE = re.compile(
    r"(?:<(?:img|picture|video|source)\b|url\(\s*['\"]?[^'\"\)]*\.(?:png|jpe?g|webp|avif|gif))",
    re.IGNORECASE,
)
MEDIA_TILE_RE = re.compile(
    r"<(?P<tag>figure|div|span)\b(?P<attrs>[^>]*class(?:Name)?=['\"][^'\"]*(?:place-photo|texture-card|media-card|evidence-card|thumbnail-card)[^'\"]*['\"][^>]*)>(?P<body>.*?)</(?P=tag)>",
    re.IGNORECASE | re.DOTALL,
)
EXPLICIT_EMPTY_STATE_RE = re.compile(r"(?:\bdata-state=['\"](?:empty|loading|pending)['\"]|\b(?:empty-state|loading-state|pending-state)\b)", re.IGNORECASE)
GENERIC_APP_MARK_RE = re.compile(
    r"class(?:Name)?=['\"][^'\"]*(?:brand-mark|app-icon|favicon)[^'\"]*['\"][^>]*>\s*[A-Z]{1,3}\s*<",
    re.IGNORECASE | re.DOTALL,
)
APP_ICON_ASSET_RE = re.compile(
    r"(?:rel=['\"]icon['\"][^>]+href=['\"][^'\"]*(?:app-icon|favicon)\.svg|src=['\"][^'\"]*app-icon\.svg|manifest\.webmanifest|assets/app-icon\.svg)",
    re.IGNORECASE,
)
VISUAL_SUBJECT_KEYWORDS = {
    "place",
    "places",
    "venue",
    "travel",
    "food",
    "restaurant",
    "map",
    "location",
    "product",
    "commerce",
    "portfolio",
    "article",
    "editorial",
    "game",
    "sports",
    "team",
    "content",
    "image",
    "diagram",
    "photo",
    "visual",
    "장소",
    "골목",
    "지도",
    "여행",
    "음식",
    "식당",
    "상품",
    "제품",
    "이미지",
    "사진",
    "도식",
    "콘텐츠",
    "경기",
    "팀",
}
CONTROL_MIN_WIDTH_LIMIT_PX = 240
CONTROL_WIDTH_LIMIT_PX = 280


@dataclass
class ImplementationIssue:
    code: str
    path: str
    line: int
    column: int
    message: str
    snippet: str
    severity: str = "error"

    def to_dict(self) -> dict:
        return asdict(self)


@dataclass
class ImplementationLintReport:
    target_repo: str
    artifact_dir: str
    checked_files: list[str] = field(default_factory=list)
    issues: list[ImplementationIssue] = field(default_factory=list)

    @property
    def ok(self) -> bool:
        return not self.issues

    def to_dict(self) -> dict:
        return {
            "target_repo": self.target_repo,
            "artifact_dir": self.artifact_dir,
            "checked_files": self.checked_files,
            "ok": self.ok,
            "issues": [issue.to_dict() for issue in self.issues],
        }


def lint_implementation(
    target_repo: Path,
    *,
    artifact_dir: str = "design-system",
    include_extensions: set[str] | None = None,
) -> ImplementationLintReport:
    target = target_repo.resolve()
    extensions = include_extensions or DEFAULT_INCLUDE_EXTENSIONS
    report = ImplementationLintReport(
        target_repo=str(target),
        artifact_dir=artifact_dir,
    )
    file_texts: dict[str, str] = {}

    for path in _iter_candidate_files(target, artifact_dir=artifact_dir, extensions=extensions):
        rel = path.relative_to(target).as_posix()
        report.checked_files.append(rel)
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        file_texts[rel] = text
        report.issues.extend(_lint_text(text, rel))

    report.issues.extend(
        _lint_project_composition(
            file_texts,
            target=target,
            artifact_dir=artifact_dir,
        )
    )
    report.checked_files.sort()
    report.issues.sort(key=lambda issue: (issue.path, issue.line, issue.column, issue.code))
    return report


def format_report(report: ImplementationLintReport) -> str:
    header = (
        f"Implementation lint: {'OK' if report.ok else 'FAIL'} "
        f"({len(report.checked_files)} files checked, {len(report.issues)} issues)"
    )
    if report.ok:
        return header

    lines = [header]
    for issue in report.issues:
        location = f"{issue.path}:{issue.line}:{issue.column}"
        lines.append(f"[{issue.code}] {location} {issue.message}")
        lines.append(f"  {issue.snippet}")
    return "\n".join(lines)


def format_json(report: ImplementationLintReport) -> str:
    return json.dumps(report.to_dict(), ensure_ascii=False, indent=2)


def _iter_candidate_files(
    target: Path,
    *,
    artifact_dir: str,
    extensions: set[str],
) -> list[Path]:
    artifact_parts = tuple(part for part in artifact_dir.split("/") if part)
    out: list[Path] = []
    for path in target.rglob("*"):
        if not path.is_file():
            continue
        rel_parts = path.relative_to(target).parts
        if _is_excluded(rel_parts, artifact_parts):
            continue
        if path.suffix.lower() not in extensions:
            continue
        if path.name.endswith(".ds-proposed"):
            continue
        out.append(path)
    return sorted(out)


def _is_excluded(rel_parts: tuple[str, ...], artifact_parts: tuple[str, ...]) -> bool:
    if not rel_parts:
        return True
    if artifact_parts and rel_parts[: len(artifact_parts)] == artifact_parts:
        return True
    return any(part in DEFAULT_EXCLUDED_DIRS for part in rel_parts)


def _lint_text(text: str, rel_path: str) -> list[ImplementationIssue]:
    issues: list[ImplementationIssue] = []
    in_managed_block = False
    in_block_comment = False
    current_selector: str | None = None

    for line_no, raw_line in enumerate(text.splitlines(), start=1):
        if DS_BLOCK_START in raw_line:
            issues.append(
                _issue(
                    "DS061",
                    rel_path,
                    line_no,
                    raw_line.find(DS_BLOCK_START) + 1,
                    "Design-token managed blocks belong in the artifact directory; implementation files should consume --ds-* tokens only.",
                    raw_line,
                )
            )
            in_managed_block = True
        if in_managed_block:
            if DS_BLOCK_END in raw_line:
                in_managed_block = False
            continue

        line, in_block_comment = _strip_comment_segments(raw_line, in_block_comment)
        if not line.strip():
            continue
        selector_for_line = _selector_for_line(line, current_selector)

        for match in COLOR_LITERAL_RE.finditer(line):
            issues.append(
                _issue(
                    "DS001",
                    rel_path,
                    line_no,
                    match.start() + 1,
                    "Hard-coded color literal; use var(--ds-color-*) or a derived color-mix using --ds tokens.",
                    raw_line,
                )
            )

        for match in COLOR_FUNCTION_RE.finditer(line):
            issues.append(
                _issue(
                    "DS002",
                    rel_path,
                    line_no,
                    match.start() + 1,
                    "Hard-coded color function; derive color through var(--ds-color-*) tokens.",
                    raw_line,
                )
            )

        if COLOR_PROPERTY_RE.search(line) and "var(--ds-color-" not in line:
            named_match = NAMED_COLOR_RE.search(line)
            if named_match:
                issues.append(
                    _issue(
                        "DS003",
                        rel_path,
                        line_no,
                        named_match.start() + 1,
                        "Named color in implementation CSS; bind semantic color through --ds-color-*.",
                        raw_line,
                    )
                )

        custom_prop_match = CUSTOM_PROPERTY_RE.search(line)
        if custom_prop_match:
            issues.extend(
                _lint_custom_color_property(
                    custom_prop_match.group("name"),
                    custom_prop_match.group("value"),
                    rel_path,
                    line_no,
                    custom_prop_match.start("value") + 1,
                    raw_line,
                )
            )

        font_match = FONT_FAMILY_RE.search(line)
        if font_match and "var(--ds-font" not in font_match.group(1) and "inherit" not in font_match.group(1):
            issues.append(
                _issue(
                    "DS010",
                    rel_path,
                    line_no,
                    font_match.start(1) + 1,
                    "Hard-coded font-family; use var(--ds-font-*) from the installed ontology.",
                    raw_line,
                )
            )

        for radius_match in RADIUS_RE.finditer(line):
            value = radius_match.group(1).strip()
            if _radius_value_is_token_bound(value):
                continue
            issues.append(
                _issue(
                    "DS020",
                    rel_path,
                    line_no,
                    radius_match.start(1) + 1,
                    "Hard-coded border radius; use var(--ds-radius-*) unless this is a full circle/pill.",
                    raw_line,
                )
            )

        issues.extend(_lint_responsive_overflow(line, selector_for_line, rel_path, line_no, raw_line))
        issues.extend(_lint_emoji_ui(line, selector_for_line, rel_path, line_no, raw_line))

        current_selector = _next_selector_context(line, selector_for_line, current_selector)

    issues.extend(_lint_color_mode_parity(text, rel_path))
    return issues


def _lint_color_mode_parity(text: str, rel_path: str) -> list[ImplementationIssue]:
    has_dark = bool(DARK_MODE_MARKER_RE.search(text))
    has_light = bool(LIGHT_MODE_MARKER_RE.search(text))
    if not has_dark or has_light:
        return []

    match = COLOR_SCHEME_DARK_RE.search(text) or DARK_MODE_MARKER_RE.search(text)
    line_no = text[:match.start()].count("\n") + 1 if match else 1
    line_start = text.rfind("\n", 0, match.start()) + 1 if match else 0
    line_end = text.find("\n", match.start()) if match else -1
    if line_end == -1:
        line_end = len(text)
    return [
        _issue(
            "DS060",
            rel_path,
            line_no,
            (match.start() - line_start + 1) if match else 1,
            "Dark mode is defined without an explicit light/default mode; define :root light tokens plus dark overrides.",
            text[line_start:line_end],
        )
    ]


def _lint_project_composition(
    file_texts: dict[str, str],
    *,
    target: Path,
    artifact_dir: str,
) -> list[ImplementationIssue]:
    """Catch repeatable composition failures that only appear at project scope."""

    ui_files = {
        rel: text
        for rel, text in file_texts.items()
        if Path(rel).suffix.lower() in UI_MARKUP_EXTENSIONS
    }
    if not ui_files:
        return []

    combined = "\n".join(file_texts.values())
    first_ui_path = sorted(ui_files)[0]
    issues: list[ImplementationIssue] = []

    card_panel_count = len(CARD_PANEL_TOKEN_RE.findall(combined))
    layout_diversity_count = len(LAYOUT_DIVERSITY_TOKEN_RE.findall(combined))
    if card_panel_count >= 10 and card_panel_count > max(8, layout_diversity_count * 2):
        issues.append(
            _issue(
                "DS070",
                first_ui_path,
                1,
                1,
                "Homogeneous card/panel wall risk; promote one primary workflow surface and compress secondary content into rows, rails, tables, canvas, or inspector surfaces.",
                f"card_or_panel_tokens={card_panel_count}, layout_diversity_tokens={layout_diversity_count}",
            )
        )

    if not (target / artifact_dir).exists():
        return issues

    interactive_count = len(INTERACTIVE_UI_RE.findall(combined))
    visual_affordance_count = len(VISUAL_AFFORDANCE_RE.findall(combined))
    if interactive_count >= 6 and visual_affordance_count < 3:
        issues.append(
            _issue(
                "DS071",
                first_ui_path,
                1,
                1,
                "Interactive UI has too few SVG/icon/visual affordances; use token-bound SVG icons for filters, status, actions, and scan surfaces.",
                f"interactive_markers={interactive_count}, visual_affordance_markers={visual_affordance_count}",
            )
        )

    if _profile_requires_domain_visuals(target, artifact_dir):
        domain_visual_count = len(DOMAIN_VISUAL_RE.findall(combined))
        if domain_visual_count < 2:
            issues.append(
                _issue(
                    "DS072",
                    first_ui_path,
                    1,
                    1,
                    "Domain visual substance is missing; add a real or deterministic product/place/object/content visual, not only text, borders, or generic controls.",
                    f"domain_visual_markers={domain_visual_count}",
                )
            )
        low_information_visuals = _find_low_information_domain_svgs(combined)
        if low_information_visuals:
            issues.append(
                _issue(
                    "DS073",
                    first_ui_path,
                    1,
                    1,
                    "Domain visual is a low-information inline SVG; add visible labels, a legend, title/desc, and data-subject anchors so the visual explains the product/place/object instead of acting as decoration.",
                    low_information_visuals[0],
                )
            )
        ad_hoc_match = AD_HOC_ILLUSTRATION_RE.search(combined)
        if ad_hoc_match:
            issues.append(
                _issue(
                    "DS074",
                    first_ui_path,
                    1,
                    1,
                    "Ad-hoc sketch/doodle illustration used as domain visual; replace it with an approved visual asset or a polished product schematic, not a rough path drawing.",
                    _single_line_snippet(ad_hoc_match.group(0)),
                )
            )
        ambiguous_surface_match = AMBIGUOUS_MOCK_SURFACE_RE.search(combined)
        if ambiguous_surface_match and not RUNTIME_SURFACE_MARKER_RE.search(combined):
            issues.append(
                _issue(
                    "DS075",
                    first_ui_path,
                    1,
                    1,
                    "Mock visual surface does not declare its real app representation; add data-runtime-surface for map SDK layers, generated/sourced media, charts, tables, or explicit empty/loading states.",
                    _single_line_snippet(ambiguous_surface_match.group(0)),
                )
            )
        if MEDIA_RUNTIME_SURFACE_RE.search(combined) and not MEDIA_ASSET_RE.search(combined):
            issues.append(
                _issue(
                    "DS076",
                    first_ui_path,
                    1,
                    1,
                    "Media/photo runtime surface has no image or video asset; place/product/content media slots must bind to generated, sourced, user-supplied, or explicit empty-state assets instead of CSS-only patterns.",
                    "data-runtime-surface media/photo without <img>, <picture>, <video>, or image url(...) asset",
                )
            )
        empty_media_tiles = _find_media_tiles_without_assets(combined)
        if empty_media_tiles:
            issues.append(
                _issue(
                    "DS078",
                    first_ui_path,
                    1,
                    1,
                    "Media/evidence tile has no asset; each place-photo, texture-card, media-card, evidence-card, or thumbnail-card needs an image/video asset or explicit empty/loading/pending state.",
                    empty_media_tiles[0],
                )
            )

    if GENERIC_APP_MARK_RE.search(combined) and not APP_ICON_ASSET_RE.search(combined):
        issues.append(
            _issue(
                "DS077",
                first_ui_path,
                1,
                1,
                "Generic initials used as app-shell brand mark without a wired app icon asset; create a brand-specific SVG app icon and connect favicon/manifest/app-shell surfaces.",
                _single_line_snippet(GENERIC_APP_MARK_RE.search(combined).group(0)),
            )
        )

    return issues


def _find_media_tiles_without_assets(text: str) -> list[str]:
    snippets: list[str] = []
    for match in MEDIA_TILE_RE.finditer(text):
        block = match.group(0)
        if MEDIA_ASSET_RE.search(block) or EXPLICIT_EMPTY_STATE_RE.search(block):
            continue
        snippets.append(_single_line_snippet(block))
    return snippets


def _find_low_information_domain_svgs(text: str) -> list[str]:
    snippets: list[str] = []
    for match in DOMAIN_INLINE_SVG_RE.finditer(text):
        block = match.group(0)
        if not DOMAIN_VISUAL_SVG_HINT_RE.search(block):
            continue
        if len(SVG_SHAPE_RE.findall(block)) < 4:
            continue
        if SEMANTIC_DOMAIN_VISUAL_ANCHOR_RE.search(block):
            continue
        snippets.append(_single_line_snippet(block))
    return snippets


def _single_line_snippet(text: str, *, limit: int = 180) -> str:
    snippet = " ".join(text.split())
    return snippet if len(snippet) <= limit else f"{snippet[: limit - 1]}..."


def _profile_requires_domain_visuals(target: Path, artifact_dir: str) -> bool:
    for candidate in (
        target / artifact_dir / "brand_profile.json",
        target / "brand_profile.json",
    ):
        if not candidate.exists():
            continue
        try:
            profile = json.loads(candidate.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            continue
        searchable = json.dumps(profile, ensure_ascii=False).lower()
        if any(keyword.lower() in searchable for keyword in VISUAL_SUBJECT_KEYWORDS):
            return True
    return False


def _selector_for_line(line: str, current_selector: str | None) -> str | None:
    stripped = line.strip()
    if "{" not in stripped:
        return current_selector
    before = stripped.split("{", 1)[0].strip()
    if not before or before.startswith("@") or before.startswith("from ") or before.startswith("to "):
        return current_selector
    return before


def _next_selector_context(
    line: str,
    selector_for_line: str | None,
    current_selector: str | None,
) -> str | None:
    opens = line.count("{")
    closes = line.count("}")
    if opens and selector_for_line:
        if closes >= opens:
            return current_selector if current_selector != selector_for_line else None
        return selector_for_line
    if closes and closes >= opens:
        return None
    return current_selector


def _lint_responsive_overflow(
    line: str,
    selector: str | None,
    rel_path: str,
    line_no: int,
    raw_line: str,
) -> list[ImplementationIssue]:
    issues: list[ImplementationIssue] = []
    context = f"{selector or ''} {line}"
    button_like = bool(BUTTON_LIKE_CONTEXT_RE.search(context))
    action_group = bool(ACTION_GROUP_CONTEXT_RE.search(context))

    for match in WIDTH_DECLARATION_RE.finditer(line):
        prop = match.group("prop").lower()
        value = match.group("value").strip()
        lower_value = value.lower()

        if "100vw" in lower_value:
            issues.append(
                _issue(
                    "DS041",
                    rel_path,
                    line_no,
                    match.start("value") + 1,
                    "Viewport-width sizing can create mobile horizontal overflow inside padded containers; prefer width/max-width: 100% or a documented full-bleed pattern.",
                    raw_line,
                )
            )

        px_value = _first_px_value(value)
        if button_like and px_value is not None:
            limit = CONTROL_MIN_WIDTH_LIMIT_PX if prop.startswith("min-") else CONTROL_WIDTH_LIMIT_PX
            if px_value >= limit:
                issues.append(
                    _issue(
                        "DS040",
                        rel_path,
                        line_no,
                        match.start("value") + 1,
                        "Button-like control uses a mobile-hostile fixed width/min-width; use max-inline-size: 100%, min-inline-size: 0, and a wrap/stack fallback.",
                        raw_line,
                    )
                )

    for match in TAILWIND_FIXED_WIDTH_RE.finditer(line):
        if not button_like:
            continue
        px_value = int(match.group("value"))
        limit = CONTROL_MIN_WIDTH_LIMIT_PX if match.group("class").startswith("min-w") else CONTROL_WIDTH_LIMIT_PX
        if px_value >= limit:
            issues.append(
                _issue(
                    "DS040",
                    rel_path,
                    line_no,
                    match.start() + 1,
                    "Button-like Tailwind width class can overflow mobile; use responsive max-w-full/min-w-0 plus wrap/stack behavior.",
                    raw_line,
                )
            )

    for match in TAILWIND_SCREEN_WIDTH_RE.finditer(line):
        issues.append(
            _issue(
                "DS041",
                rel_path,
                line_no,
                match.start() + 1,
                "Tailwind w-screen commonly creates mobile horizontal overflow in padded layouts; prefer w-full/max-w-full unless this is a documented full-bleed element.",
                raw_line,
            )
        )

    nowrap_match = FLEX_WRAP_NOWRAP_RE.search(line)
    if action_group and nowrap_match:
        issues.append(
            _issue(
                "DS042",
                rel_path,
                line_no,
                nowrap_match.start() + 1,
                "Action/control row disables wrapping; provide flex-wrap: wrap or a <=480px stacked fallback so buttons stay onscreen.",
                raw_line,
            )
        )

    css_nowrap = WHITE_SPACE_NOWRAP_RE.search(line)
    tailwind_nowrap = TAILWIND_NOWRAP_RE.search(line)
    nowrap_column = css_nowrap.start() + 1 if css_nowrap else tailwind_nowrap.start() + 1 if tailwind_nowrap else None
    if button_like and nowrap_column is not None:
        issues.append(
            _issue(
                "DS043",
                rel_path,
                line_no,
                nowrap_column,
                "Button-like control prevents label wrapping; verify real mobile copy or pair it with a mobile stack/fallback.",
                raw_line,
            )
        )

    return issues


def _first_px_value(value: str) -> int | None:
    match = re.search(r"(-?\d+(?:\.\d+)?)px\b", value, re.IGNORECASE)
    if not match:
        return None
    try:
        return int(float(match.group(1)))
    except ValueError:
        return None


def _lint_emoji_ui(
    line: str,
    selector: str | None,
    rel_path: str,
    line_no: int,
    raw_line: str,
) -> list[ImplementationIssue]:
    if EMOJI_CONTENT_CONTEXT_RE.search(line):
        return []

    context = f"{selector or ''} {line}"
    if not EMOJI_UI_CONTEXT_RE.search(context):
        return []

    issues: list[ImplementationIssue] = []
    for match in EMOJI_RE.finditer(line):
        issues.append(
            _issue(
                "DS050",
                rel_path,
                line_no,
                match.start() + 1,
                "Emoji used as a UI affordance; replace it during refactor with an SVG file/component or approved icon library.",
                raw_line,
            )
        )
    return issues


def _lint_custom_color_property(
    name: str,
    value: str,
    rel_path: str,
    line_no: int,
    column: int,
    raw_line: str,
) -> list[ImplementationIssue]:
    if not COLOR_MIX_RE.search(value):
        return []

    tokens = {token.lower() for token in DS_COLOR_TOKEN_RE.findall(value)}
    chromatic_tokens = tokens - NEUTRAL_COLOR_TOKENS
    issues: list[ImplementationIssue] = []

    if len(chromatic_tokens) > 1:
        issues.append(
            _issue(
                "DS030",
                rel_path,
                line_no,
                column,
                "Derived local palette mixes multiple chromatic --ds-color roles; alias a single semantic token or mix one role with neutral/transparent.",
                raw_line,
            )
        )

    if STRUCTURAL_CUSTOM_PROPERTY_RE.fullmatch(name) and tokens & REFERENCE_RISK_COLOR_TOKENS:
        issues.append(
            _issue(
                "DS031",
                rel_path,
                line_no,
                column,
                "Structural palette variable derives from info/surface-tint roles; keep reference-like palette composition out of implementation chrome.",
                raw_line,
            )
        )

    return issues


def _radius_value_is_token_bound(value: str) -> bool:
    normalized = value.strip().rstrip(";").lower()
    if "var(--ds-radius" in normalized:
        return True
    if normalized in ALLOWED_RADIUS_VALUES:
        return True
    if normalized.startswith("calc(") and "var(--ds-radius" in normalized:
        return True
    return False


def _strip_comment_segments(line: str, in_block_comment: bool) -> tuple[str, bool]:
    out = []
    i = 0
    while i < len(line):
        if in_block_comment:
            end = line.find("*/", i)
            if end == -1:
                return "".join(out), True
            i = end + 2
            in_block_comment = False
            continue

        start = line.find("/*", i)
        slash = line.find("//", i)
        candidates = [idx for idx in (start, slash) if idx != -1]
        if not candidates:
            out.append(line[i:])
            break
        next_idx = min(candidates)
        out.append(line[i:next_idx])
        if next_idx == slash:
            break
        end = line.find("*/", next_idx + 2)
        if end == -1:
            in_block_comment = True
            break
        i = end + 2
    return "".join(out), in_block_comment


def _issue(
    code: str,
    rel_path: str,
    line_no: int,
    column: int,
    message: str,
    raw_line: str,
) -> ImplementationIssue:
    return ImplementationIssue(
        code=code,
        path=rel_path,
        line=line_no,
        column=column,
        message=message,
        snippet=raw_line.strip(),
    )
