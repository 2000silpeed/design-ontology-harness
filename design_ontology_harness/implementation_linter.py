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

# \u2500\u2500 LLM-default UI tells (DS090+) \u2500\u2500
# \uBB38\uC11C/\uBE14\uB85C\uADF8 \uBB38\uBC95\uC774 \uC571 UI\uB85C \uC0C8\uB294 \uD328\uD134\uACFC, \uAD6C\uD604 LLM\uC774 \uAE30\uBCF8\uAC12\uC73C\uB85C \uBC18\uBCF5\uD558\uB294 \uC870\uD615 \uC2B5\uAD00.
DOC_CALLOUT_SELECTOR_RE = re.compile(
    r"(?:note|callout|quote|hint|tip|banner|admonition|notice|caution|info-box|infobox)",
    re.IGNORECASE,
)
DOC_CALLOUT_BORDER_RE = re.compile(
    r"\bborder-(?:left|inline-start)\s*:\s*(?P<width>\d+(?:\.\d+)?)px\s+solid\b",
    re.IGNORECASE,
)
RADIUS_TOKEN_USAGE_RE = re.compile(r"var\(\s*(--ds-radius-[a-z0-9-]+)\s*\)", re.IGNORECASE)
FONT_WEIGHT_DECL_RE = re.compile(r"\bfont-weight\s*:\s*(?P<value>\d{3})\b", re.IGNORECASE)
FONT_SIZE_DECL_RE = re.compile(
    r"\bfont-size\s*:\s*(?P<value>\d+(?:\.\d+)?)(?P<unit>rem|px)\b", re.IGNORECASE
)
PLACEHOLDER_COPY_RE = re.compile(
    r"(?:\blorem\b|\bipsum\b|\uD56D\uBAA9\s*\d|\bItem\s+\d\b|\uC5EC\uAE30\uC5D0\s*(?:\uB0B4\uC6A9|\uD14D\uC2A4\uD2B8)|\uC0D8\uD50C\s*\uD14D\uC2A4\uD2B8|placeholder\s+text)",
    re.IGNORECASE,
)
CSS_PAINTED_GRIDFIELD_RE = re.compile(
    r"background\s*:[^;]*linear-gradient\([^;]*?1px[^;]*?transparent[^;]*?"
    r"linear-gradient\([^;]*?1px[^;]*?transparent[^;]*?;[^}]*?background-size\s*:",
    re.IGNORECASE | re.DOTALL,
)
CSS_RULE_BLOCK_RE = re.compile(r"(?P<selector>[^{}]+)\{(?P<body>[^{}]*)\}")
EDGE_BAR_EDGE_RE = re.compile(r"\b(?:left|right)\s*:\s*0(?:px)?(?![\w.%])", re.IGNORECASE)
EDGE_BAR_WIDTH_RE = re.compile(r"\bwidth\s*:\s*[1-5](?:\.\d+)?px\b", re.IGNORECASE)
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
ICON_SPRITE_RE = re.compile(
    r"<svg\b(?P<attrs>[^>]*class(?:Name)?=['\"][^'\"]*icon-sprite[^'\"]*['\"][^>]*)>(?P<body>.*?)</svg>",
    re.IGNORECASE | re.DOTALL,
)
APPROVED_ICON_SET_RE = re.compile(
    r"(?:data-icon-set\s*=\s*['\"](?:lucide|heroicons|phosphor|tabler|material|approved-custom)[^'\"]*['\"]|lucide-|heroicon|phosphor|tabler|material-symbol)",
    re.IGNORECASE,
)
ICON_SYMBOL_RE = re.compile(r"<symbol\b[^>]*id=['\"]icon-[^'\"]+['\"]", re.IGNORECASE)
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
AD_HOC_NODE_LINK_CLASS_RE = re.compile(
    r"\b(?:trace-canvas|trace-node|trace-line|graph-node|graph-edge|mock-graph|placeholder-graph|node-link-mini(?:map)?|mini-?map)\b",
    re.IGNORECASE,
)
AD_HOC_NODE_LINK_LAYOUT_RE = re.compile(
    r"(?:\.(?:trace-node|graph-node|node-link-node)[^{]*\{[^}]*\bposition\s*:\s*absolute\b|"
    r"\.(?:trace-line|graph-edge|node-link-edge)[^{]*\{[^}]*\btransform\s*:\s*rotate\s*\(|"
    r"\.(?:trace-line|graph-edge|node-link-edge)[^{]*\{[^}]*\bheight\s*:\s*2px\b)",
    re.IGNORECASE | re.DOTALL,
)
AD_HOC_NODE_LINK_LABEL_RE = re.compile(
    r"\b(?:Answer|CH-\d{2,3}|DOC-[a-z0-9-]+-CH-\d+|별표\s*\d+|하도급법|공정거래법|법령)\b",
    re.IGNORECASE,
)
FREEHAND_SVG_CONNECTOR_RE = re.compile(
    r"<svg\b(?P<attrs>[^>]*(?:class|className)=['\"][^'\"]*(?:wires|connector-layer|flow-lines|graph-wires|workflow-wires|node-links)[^'\"]*['\"][^>]*)>(?P<body>.*?)</svg>",
    re.IGNORECASE | re.DOTALL,
)
POSITIONED_GRAPH_NODE_RE = re.compile(
    r"(?:class(?:Name)?=['\"][^'\"]*(?:flow-node|canvas-node|graph-node|trace-node|node-link-node)[^'\"]*['\"]|"
    r"style=['\"][^'\"]*\b(?:left|top)\s*:|"
    r"\.(?:flow-node|canvas-node|graph-node|trace-node|node-link-node)[^{]*\{[^}]*\bposition\s*:\s*absolute\b)",
    re.IGNORECASE | re.DOTALL,
)
SEMANTIC_GRAPH_EDGE_ID_RE = re.compile(r"\bdata-edge-id\s*=", re.IGNORECASE)
SEMANTIC_GRAPH_FROM_RE = re.compile(r"\bdata-from\s*=", re.IGNORECASE)
SEMANTIC_GRAPH_TO_RE = re.compile(r"\bdata-to\s*=", re.IGNORECASE)
SEMANTIC_GRAPH_DIRECTION_RE = re.compile(
    r"(?:\bmarker-end\s*=|\bdata-direction\s*=|\baria-label\s*=)",
    re.IGNORECASE,
)
SEMANTIC_GRAPH_LABEL_RE = re.compile(
    r"(?:<text\b|\bdata-label\s*=|\baria-label\s*=)",
    re.IGNORECASE,
)
COMPLEX_SURFACE_ATTR_RE = re.compile(
    r"<(?P<tag>section|main|div|article|aside|figure)\b(?P<attrs>[^>]*(?:class|className|role|aria-label)\s*=\s*['\"][^'\"]*(?:chart|graph|map|calendar|kanban|gantt|spreadsheet|workflow|board|timeline|table|ledger|inspector|canvas)[^'\"]*['\"][^>]*)>",
    re.IGNORECASE | re.DOTALL,
)
MOCK_SURFACE_HINT_RE = re.compile(
    r"\b(?:mock|placeholder|fake|static|demo|sample|dummy|wireframe|목업|플레이스홀더|샘플|더미|가짜|임시)\b",
    re.IGNORECASE,
)
SURFACE_CONTRACT_RE = re.compile(
    r"(?:data-(?:runtime-surface|product-surface|model|source|collection|schema|state|row-id|item-id|node-id|edge-id|event-id|from|to|value|label)\s*=|"
    r"<table\b|role\s*=\s*['\"](?:table|grid|treegrid|listbox)['\"])",
    re.IGNORECASE,
)
HTML_PROTOTYPE_MARKER_RE = re.compile(
    r"(?:data-(?:product-)?prototype\s*=|class(?:Name)?\s*=\s*['\"][^'\"]*(?:html-mockup|product-mockup|app-mockup|prototype)[^'\"]*['\"])",
    re.IGNORECASE,
)
PROTOTYPE_STATE_SET_RE = re.compile(
    r"(?:data-(?:prototype-)?state-set\s*=|data-scenario\s*=|data-view-state\s*=)",
    re.IGNORECASE,
)
STATE_VARIANT_RE = re.compile(
    r"(?:data-state\s*=\s*['\"](?P<data>[^'\"]+)['\"]|"
    r"aria-(?:selected|current|busy|disabled|expanded)\s*=|"
    r"class(?:Name)?\s*=\s*['\"][^'\"]*(?:is-|state-|selected|active|empty|loading|error|disabled|pending|approved|blocked|success|warning)[^'\"]*['\"])",
    re.IGNORECASE,
)
PROTOTYPE_STYLE_DECL_RE = re.compile(
    r"\b(?:display|grid-template-columns|grid-template-rows|flex-wrap|gap|padding|border|background|border-radius|font-family|min-height|align-items|justify-content|overflow|color)\s*:",
    re.IGNORECASE,
)
TAILWIND_SURFACE_CLASS_RE = re.compile(
    r"\b(?:grid|flex|gap-\d|p-\d|px-\d|py-\d|rounded|border|bg-|text-|min-h-|items-|justify-)\b",
    re.IGNORECASE,
)
DS_TOKEN_USAGE_RE = re.compile(r"var\(\s*--ds-", re.IGNORECASE)
RUNTIME_SURFACE_MARKER_RE = re.compile(r"\bdata-runtime-surface\s*=", re.IGNORECASE)
MEDIA_RUNTIME_SURFACE_RE = re.compile(
    r"\bdata-runtime-surface\s*=\s*['\"][^'\"]*(?:media|photo|thumbnail|image|generated|sourced)[^'\"]*['\"]",
    re.IGNORECASE,
)
MEDIA_ASSET_RE = re.compile(
    r"(?:<(?:img|picture|video|source)\b|url\(\s*['\"]?[^'\"\)]*\.(?:png|jpe?g|webp|avif|gif))",
    re.IGNORECASE,
)
SVG_MEDIA_ASSET_RE = re.compile(
    r"<(?P<tag>img|source)\b(?P<attrs>[^>]*(?:src|srcset)\s*=\s*['\"][^'\"]+\.svg(?:#[^'\"]*)?[^'\"]*['\"][^>]*)>",
    re.IGNORECASE | re.DOTALL,
)
NARRATIVE_MEDIA_CONTEXT_RE = re.compile(
    r"(?:comic|manga|webtoon|toon|cover|panel|strip|episode|chapter|story|character|poster|editorial|article|magazine|issue|reader|만화|웹툰|표지|컷|회차|연재|캐릭터|잡지)",
    re.IGNORECASE,
)
SVG_MEDIUM_ALLOWED_CONTEXT_RE = re.compile(
    r"(?:app-icon|favicon|logo|brand-mark|icon|flag|diagram|chart|map|schematic|glyph|ui-icon|mask-icon|rel=['\"]icon)",
    re.IGNORECASE,
)
RASTER_ONLY_DIRECTIVE_RE = re.compile(
    # 명시적 지시문만 매칭한다. bare "png"/"jpg" 토큰까지 잡으면 사진 URL(fm=jpg)이
    # 있는 모든 프로젝트가 래스터 전용으로 오판되어 정상적인 사진+SVG 혼용을 막는다.
    r"(?:no[-_\s]?svg|svg\s*(?:금지|없이|만들지\s*말고)|raster[-_\s]?only"
    r"|래스터\s*(?:전용|만)|비트맵\s*(?:전용|만)|실제\s*(?:그림|이미지)\s*파일"
    r"|(?:png|webp|jpe?g)[-\s]?(?:only|전용|만\b))",
    re.IGNORECASE,
)
SVG_USAGE_RE = re.compile(
    r"(?:<svg\b|</svg>|<symbol\b|<use\b|use\s+href=|image/svg\+xml|(?:src|href|url\()\s*=\s*['\"]?[^'\"\)]*\.svg\b|\.svg\b)",
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
    "comic",
    "editorial",
    "manga",
    "webtoon",
    "magazine",
    "story",
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
    "만화",
    "웹툰",
    "잡지",
    "표지",
    "연재",
    "회차",
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

        callout_border = DOC_CALLOUT_BORDER_RE.search(line)
        if (
            callout_border
            and float(callout_border.group("width")) >= 2
            and selector_for_line
            and DOC_CALLOUT_SELECTOR_RE.search(selector_for_line)
        ):
            issues.append(
                _issue(
                    "DS090",
                    rel_path,
                    line_no,
                    callout_border.start() + 1,
                    "Doc-grammar callout (border-left quote bar) leaking into app UI; app guidance copy is an undecorated muted caption — emphasize with placement, not decoration.",
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

    issues.extend(_lint_llm_default_tells(file_texts, first_ui_path, combined))

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

    if RASTER_ONLY_DIRECTIVE_RE.search(combined):
        svg_usage = _find_svg_usage_under_raster_directive(combined)
        if svg_usage:
            issues.append(
                _issue(
                    "DS081",
                    first_ui_path,
                    1,
                    1,
                    "Raster-only/no-SVG medium directive is active, but the implementation still contains SVG usage; replace affected assets with project-local PNG/WebP/JPEG files and record the medium decision.",
                    svg_usage[0],
                )
            )

    ad_hoc_node_link = _find_ad_hoc_node_link_placeholder(combined)
    if ad_hoc_node_link:
        issues.append(
            _issue(
                "DS082",
                first_ui_path,
                1,
                1,
                "Ad-hoc node-link placeholder graph detected; replace hand-positioned nodes/rotated lines with a real chart/graph library, a semantic table/ledger, or a polished data visualization with labels and runtime data.",
                ad_hoc_node_link[0],
            )
        )

    freehand_connector_graph = _find_freehand_svg_connector_graph(combined)
    if freehand_connector_graph:
        issues.append(
            _issue(
                "DS083",
                first_ui_path,
                1,
                1,
                "Freehand SVG connector graph detected; keep nodes and edges in one semantic coordinate system with data-node/data-edge ids, arrowheads, labels, and runtime data, or replace the graph with a table/ledger.",
                freehand_connector_graph[0],
            )
        )

    uncontracted_surface = _find_complex_mock_surface_without_contract(combined)
    if uncontracted_surface:
        issues.append(
            _issue(
                "DS084",
                first_ui_path,
                1,
                1,
                "Complex HTML mock surface lacks a product/runtime contract; add data-runtime-surface or data-product-surface plus model/source/id/state metadata, or replace the surface with a simpler table/ledger.",
                uncontracted_surface[0],
            )
        )

    single_state_prototype = _find_single_state_html_prototype(combined)
    if single_state_prototype:
        issues.append(
            _issue(
                "DS085",
                first_ui_path,
                1,
                1,
                "HTML prototype is marked as a product prototype but exposes no state set; include default/selected/loading/empty/error or equivalent data-state scenarios before visual QA.",
                single_state_prototype[0],
            )
        )

    metadata_only_prototype = _find_metadata_only_html_prototype(combined)
    if metadata_only_prototype:
        issues.append(
            _issue(
                "DS086",
                first_ui_path,
                1,
                1,
                "HTML prototype has product/runtime metadata but no product-surface styling; add token-bound layout, surface, typography, state, and affordance styling before review.",
                metadata_only_prototype[0],
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
        wrong_medium_media = _find_wrong_medium_svg_media(combined)
        if wrong_medium_media:
            issues.append(
                _issue(
                    "DS079",
                    first_ui_path,
                    1,
                    1,
                    "Narrative/content media slot uses an SVG asset; comic, manga, webtoon, story, character, editorial-cover, and panel-preview slots need image_gen, user-supplied, sourced, or approved high-fidelity artwork.",
                    wrong_medium_media[0],
                )
            )
        handmade_icon_sprite = _find_undeclared_icon_sprite(combined)
        if handmade_icon_sprite:
            issues.append(
                _issue(
                    "DS080",
                    first_ui_path,
                    1,
                    1,
                    "Inline icon sprite does not declare an approved icon set or custom icon grammar; use a known icon library such as Lucide/Heroicons/Phosphor/Tabler/Material or document the sprite as approved-custom.",
                    handmade_icon_sprite[0],
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


def _lint_llm_default_tells(
    file_texts: dict[str, str],
    first_ui_path: str,
    combined: str,
) -> list[ImplementationIssue]:
    """Aggregate checks for shapes the implementing LLM repeats by default.

    These are taste failures that survive token binding: the palette can be
    correct while the surface still reads as generated. Each rule targets one
    measurable habit with a threshold high enough to avoid false positives.
    """

    issues: list[ImplementationIssue] = []
    css_text = "\n".join(
        text for rel, text in file_texts.items() if rel.lower().endswith(".css")
    )

    # DS091 — radius monoculture: 모든 요소에 같은 라운딩 토큰 하나만 바르는 습관
    radius_usages = [
        token.lower()
        for token in RADIUS_TOKEN_USAGE_RE.findall(css_text)
        if not token.lower().endswith(("-pill", "-none"))
    ]
    distinct_radius = set(radius_usages)
    if len(radius_usages) >= 8 and len(distinct_radius) == 1:
        issues.append(
            _issue(
                "DS091",
                first_ui_path,
                1,
                1,
                "Radius monoculture: one radius token applied everywhere reads as a default theme; reserve rounding for interactive/elevated surfaces (max 2 steps per screen, 0 is a valid choice).",
                f"radius_usages={len(radius_usages)}, distinct={sorted(distinct_radius)}",
            )
        )

    # DS092 — hedging weights: 500과 600을 함께 쓰는 중간 굵기 회피 습관
    weights = {match.group("value") for match in FONT_WEIGHT_DECL_RE.finditer(css_text)}
    if {"500", "600"} <= weights:
        issues.append(
            _issue(
                "DS092",
                first_ui_path,
                1,
                1,
                "Hedging font weights: both 500 and 600 in one surface flattens hierarchy; commit to two anchored weights (e.g. 400/700) and express the rest with size and spacing.",
                f"font_weights={sorted(weights)}",
            )
        )

    # DS093 — compressed type scale: 프로토타입인데 디스플레이 스케일이 없음
    if HTML_PROTOTYPE_MARKER_RE.search(combined):
        sizes_rem: list[float] = []
        for match in FONT_SIZE_DECL_RE.finditer(css_text):
            value = float(match.group("value"))
            sizes_rem.append(value / 16 if match.group("unit").lower() == "px" else value)
        if len(set(sizes_rem)) >= 6 and sizes_rem and max(sizes_rem) < 1.5:
            issues.append(
                _issue(
                    "DS093",
                    first_ui_path,
                    1,
                    1,
                    "Compressed type scale: many sizes but no display tier (max < 1.5rem) reads as a settings page; give the screen one hero-scale element and drop intermediate sizes.",
                    f"distinct_sizes={len(set(sizes_rem))}, max={max(sizes_rem):.3g}rem",
                )
            )

    # DS095 — CSS로 그림 흉내 낸 격자 필드: 계기/차트 표면은 실제 렌더링 매체가 필요
    painted_grid = CSS_PAINTED_GRIDFIELD_RE.search(css_text)
    if painted_grid and HTML_PROTOTYPE_MARKER_RE.search(combined):
        issues.append(
            _issue(
                "DS095",
                first_ui_path,
                1,
                1,
                "CSS-painted grid field: instrument/chart/coordinate surfaces need a real rendering medium (inline SVG with grid, ticks, and crosshair in one coordinate system, or canvas/chart library); dual linear-gradient grids with a positioned dot read as box art.",
                _single_line_snippet(painted_grid.group(0), limit=200),
            )
        )

    # DS096 — 엣지 세로 바 장식: 상태/강조를 화면 가장자리 세로 바로 표시하는 습관.
    # DS090(callout 셀렉터의 border-left)을 셀렉터명을 바꿔 우회하는 pseudo-element 변형을 잡는다.
    for block in CSS_RULE_BLOCK_RE.finditer(css_text):
        body = block.group("body")
        if (
            "absolute" in body
            and EDGE_BAR_EDGE_RE.search(body)
            and EDGE_BAR_WIDTH_RE.search(body)
            and re.search(r"\btop\s*:", body)
            and re.search(r"\bbottom\s*:", body)
            and re.search(r"\bbackground\s*:", body)
        ):
            issues.append(
                _issue(
                    "DS096",
                    first_ui_path,
                    1,
                    1,
                    "Edge vertical bar decoration: status/emphasis rendered as a thin full-height bar at the container edge is doc-callout grammar in disguise; use a dot, a short label, or a subtle background tint instead.",
                    _single_line_snippet(block.group(0), limit=200),
                )
            )
            break

    # DS094 — placeholder copy: 실데이터 대신 채움말
    placeholder = PLACEHOLDER_COPY_RE.search(combined)
    if placeholder:
        issues.append(
            _issue(
                "DS094",
                first_ui_path,
                1,
                1,
                "Placeholder copy in the surface; replace with realistic domain data (real garment/product/user names and values) before visual QA.",
                _single_line_snippet(
                    combined[max(0, placeholder.start() - 60) : placeholder.end() + 60]
                ),
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


def _find_ad_hoc_node_link_placeholder(text: str) -> list[str]:
    """Detect hand-drawn node/edge diagrams that read as placeholder graphs.

    This intentionally requires both graph-like class names and absolute/rotated
    layout mechanics so real tables, ledgers, SVG charts, canvas charts, or
    library-rendered graph containers are not blocked by a generic "graph" word.
    """

    class_hits = {hit.lower() for hit in AD_HOC_NODE_LINK_CLASS_RE.findall(text)}
    if len(class_hits) < 2:
        return []
    layout_match = AD_HOC_NODE_LINK_LAYOUT_RE.search(text)
    if not layout_match:
        return []
    label_match = AD_HOC_NODE_LINK_LABEL_RE.search(text)
    snippet_start = layout_match.start()
    snippet_end = min(len(text), layout_match.end() + 220)
    snippet = _single_line_snippet(text[snippet_start:snippet_end], limit=240)
    if label_match:
        label_context_start = max(0, label_match.start() - 80)
        label_context_end = min(len(text), label_match.end() + 80)
        snippet = _single_line_snippet(
            f"{text[label_context_start:label_context_end]} {text[snippet_start:snippet_end]}",
            limit=240,
        )
    return [snippet]


def _find_freehand_svg_connector_graph(text: str) -> list[str]:
    """Detect SVG connector layers laid over separately positioned HTML nodes.

    These often look plausible in one screenshot but have no shared graph model:
    edges are path art, nodes are independent DOM boxes, and responsive changes
    break the relationship. A legitimate workflow graph should use a graph
    library, or a single SVG/canvas coordinate system with node/edge metadata.
    """

    snippets: list[str] = []
    for match in FREEHAND_SVG_CONNECTOR_RE.finditer(text):
        body = match.group("body")
        if len(re.findall(r"<path\b", body, flags=re.IGNORECASE)) < 2:
            continue

        context_start = max(0, match.start() - 1400)
        context_end = min(len(text), match.end() + 1400)
        context = text[context_start:context_end]
        if not POSITIONED_GRAPH_NODE_RE.search(context):
            continue
        if _has_semantic_graph_edge_model(body):
            continue
        snippets.append(_single_line_snippet(context, limit=260))
    return snippets


def _has_semantic_graph_edge_model(svg_body: str) -> bool:
    return all(
        pattern.search(svg_body)
        for pattern in (
            SEMANTIC_GRAPH_EDGE_ID_RE,
            SEMANTIC_GRAPH_FROM_RE,
            SEMANTIC_GRAPH_TO_RE,
            SEMANTIC_GRAPH_DIRECTION_RE,
            SEMANTIC_GRAPH_LABEL_RE,
        )
    )


def _find_complex_mock_surface_without_contract(text: str) -> list[str]:
    """Detect static-looking complex surfaces that do not expose product intent.

    HTML mockups can represent maps, charts, calendars, boards, and editors, but
    those surfaces need a visible runtime/data contract. This check stays narrow:
    it only fires when a complex surface is also described as mock/sample/fake/
    placeholder/static and the nearby markup has no runtime, model, source, id,
    state, table, or grid contract.
    """

    snippets: list[str] = []
    for match in COMPLEX_SURFACE_ATTR_RE.finditer(text):
        context_start = max(0, match.start() - 220)
        context_end = min(len(text), match.end() + 900)
        context = text[context_start:context_end]
        if not MOCK_SURFACE_HINT_RE.search(context):
            continue
        if SURFACE_CONTRACT_RE.search(context):
            continue
        snippets.append(_single_line_snippet(context, limit=260))
    return snippets


def _find_single_state_html_prototype(text: str) -> list[str]:
    if not HTML_PROTOTYPE_MARKER_RE.search(text):
        return []

    surface_count = len(COMPLEX_SURFACE_ATTR_RE.findall(text))
    interaction_count = len(INTERACTIVE_UI_RE.findall(text))
    if surface_count < 1 and interaction_count < 4:
        return []
    if PROTOTYPE_STATE_SET_RE.search(text):
        return []

    state_values = set()
    generic_state_markers = 0
    for match in STATE_VARIANT_RE.finditer(text):
        data_value = match.groupdict().get("data")
        if data_value:
            state_values.add(data_value.lower())
        else:
            generic_state_markers += 1

    if len(state_values) + generic_state_markers >= 2:
        return []

    prototype_match = HTML_PROTOTYPE_MARKER_RE.search(text)
    if not prototype_match:
        return []
    context_start = max(0, prototype_match.start() - 220)
    context_end = min(len(text), prototype_match.end() + 900)
    return [_single_line_snippet(text[context_start:context_end], limit=260)]


def _find_metadata_only_html_prototype(text: str) -> list[str]:
    """Detect prototypes that satisfy metadata gates but still render as raw HTML."""

    prototype_match = HTML_PROTOTYPE_MARKER_RE.search(text)
    if not prototype_match:
        return []

    surface_count = len(COMPLEX_SURFACE_ATTR_RE.findall(text))
    interaction_count = len(INTERACTIVE_UI_RE.findall(text))
    if surface_count < 1 and interaction_count < 4:
        return []
    if _prototype_has_surface_styling(text):
        return []

    context_start = max(0, prototype_match.start() - 220)
    context_end = min(len(text), prototype_match.end() + 900)
    return [_single_line_snippet(text[context_start:context_end], limit=260)]


def _prototype_has_surface_styling(text: str) -> bool:
    style_decl_count = len(PROTOTYPE_STYLE_DECL_RE.findall(text))
    token_count = len(DS_TOKEN_USAGE_RE.findall(text))
    utility_count = len(TAILWIND_SURFACE_CLASS_RE.findall(text))
    return style_decl_count >= 8 or token_count >= 6 or utility_count >= 10


def _find_svg_usage_under_raster_directive(text: str) -> list[str]:
    snippets: list[str] = []
    for match in SVG_USAGE_RE.finditer(text):
        snippets.append(_single_line_snippet(match.group(0)))
    return snippets


def _find_wrong_medium_svg_media(text: str) -> list[str]:
    snippets: list[str] = []
    for match in SVG_MEDIA_ASSET_RE.finditer(text):
        attrs = match.group("attrs")
        context_start = max(0, match.start() - 220)
        context_end = min(len(text), match.end() + 220)
        context = f"{attrs} {text[context_start:context_end]}"
        if SVG_MEDIUM_ALLOWED_CONTEXT_RE.search(context):
            continue
        if not NARRATIVE_MEDIA_CONTEXT_RE.search(context):
            continue
        snippets.append(_single_line_snippet(match.group(0)))
    return snippets


def _find_undeclared_icon_sprite(text: str) -> list[str]:
    snippets: list[str] = []
    for match in ICON_SPRITE_RE.finditer(text):
        block = match.group(0)
        attrs = match.group("attrs")
        symbol_count = len(ICON_SYMBOL_RE.findall(block))
        if symbol_count < 4:
            continue
        if APPROVED_ICON_SET_RE.search(attrs) or APPROVED_ICON_SET_RE.search(block):
            continue
        snippets.append(_single_line_snippet(block, limit=220))
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
