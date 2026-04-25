"""Preview linter — static checks for preset preview.md quality.

Phase 12A-2. Validates that preview.md files produced by preset_builder follow
the template defined in PLUGIN_PLAN.md §9.3 and stay consistent with
manifest.json. Stdlib only (re, pathlib, json).

Public API:
    lint_preview(preset_dir: Path) -> PreviewLintReport
    lint_all_previews(presets_root: Path) -> list[PreviewLintReport]

Rule codes:
    E001 missing_file            preview.md does not exist
    E002 empty_file              preview.md is empty / whitespace-only
    E003 missing_section         one of the 5 required sections is absent
    E004 missing_color_swatches  Color Tokens section has < 4 HEX swatches
                                 and no builder fallback sentinel
    E005 dark_palette_missing    manifest.color_modes contains "dark" but
                                 Color Tokens section never mentions "dark"
    E006 light_only_has_dark     manifest.color_modes is light-only but
                                 Color Tokens section mentions "dark" (drift)
    E007 typography_missing      Typography section lacks any heading/body
                                 font bullet and has no fallback sentinel
    E008 component_count         대표 컴포넌트 section has < 3 bullets and
                                 no fallback sentinel
    W001 hex_invalid             token that looks like HEX but is malformed
    W002 ko_locale_untagged      manifest.locale_pairings has "ko" but
                                 Typography section never mentions
                                 Pretendard/korean
    W003 caution_empty           주의사항 section exists but has no bullets
"""

from __future__ import annotations

import json
import re
from dataclasses import dataclass, field
from pathlib import Path


REQUIRED_SECTIONS: tuple[str, ...] = (
    "어떤 제품에 맞나",
    "Color Tokens",
    "Typography",
    "대표 컴포넌트",
    "주의사항",
)

SECTION_ALIASES: dict[str, tuple[str, ...]] = {
    "어떤 제품에 맞나": ("어떤 제품에 맞나", "when to use", "recommended for"),
    "Color Tokens": ("color tokens", "색상 토큰", "colors"),
    "Typography": ("typography", "서체"),
    "대표 컴포넌트": ("대표 컴포넌트", "key components"),
    "주의사항": ("주의사항", "caveats", "notes"),
}

COLOR_FALLBACK_SENTINELS: tuple[str, ...] = (
    "color_reference 미설정",
    "color_reference가 설정되지",
)
TYPOGRAPHY_FALLBACK_SENTINELS: tuple[str, ...] = (
    "font_system 미해석",
    "font_system 미설정",
)
COMPONENT_FALLBACK_SENTINELS: tuple[str, ...] = (
    "component_specs.json 비어있음",
)

_HEX_IN_BACKTICKS = re.compile(r"`(#[0-9a-zA-Z]+)`")
_VALID_HEX = re.compile(r"^#[0-9a-fA-F]{6}$")
_BULLET_LINE = re.compile(r"^\s*-\s+\S")


@dataclass
class PreviewIssue:
    code: str
    message: str
    line: int | None = None


@dataclass
class PreviewLintReport:
    preset_id: str
    errors: list[PreviewIssue] = field(default_factory=list)
    warnings: list[PreviewIssue] = field(default_factory=list)

    @property
    def ok(self) -> bool:
        return not self.errors


@dataclass
class _Section:
    header: str
    canonical: str | None
    header_line: int
    body: str
    body_start_line: int


def lint_preview(preset_dir: Path) -> PreviewLintReport:
    preset_id = preset_dir.name
    report = PreviewLintReport(preset_id=preset_id)
    preview_path = preset_dir / "preview.md"

    if not preview_path.exists():
        report.errors.append(
            PreviewIssue(code="E001", message="preview.md missing", line=None)
        )
        return report

    text = preview_path.read_text(encoding="utf-8")
    if not text.strip():
        report.errors.append(
            PreviewIssue(code="E002", message="preview.md is empty", line=1)
        )
        return report

    sections = _parse_sections(text)
    canonical_map: dict[str, _Section] = {}
    for section in sections:
        if section.canonical and section.canonical not in canonical_map:
            canonical_map[section.canonical] = section

    for required in REQUIRED_SECTIONS:
        if required not in canonical_map:
            report.errors.append(
                PreviewIssue(
                    code="E003",
                    message=f'required section "{required}" missing',
                    line=None,
                )
            )

    manifest = _load_manifest(preset_dir)

    color_section = canonical_map.get("Color Tokens")
    if color_section is not None:
        _check_color_tokens(color_section, manifest, report)

    typography_section = canonical_map.get("Typography")
    if typography_section is not None:
        _check_typography(typography_section, manifest, report)

    component_section = canonical_map.get("대표 컴포넌트")
    if component_section is not None:
        _check_components(component_section, report)

    caveat_section = canonical_map.get("주의사항")
    if caveat_section is not None:
        _check_caveats(caveat_section, report)

    return report


def lint_all_previews(presets_root: Path) -> list[PreviewLintReport]:
    reports: list[PreviewLintReport] = []
    for entry in sorted(presets_root.iterdir()):
        if not entry.is_dir():
            continue
        if entry.name.startswith(".") or entry.name == "__pycache__":
            continue
        reports.append(lint_preview(entry))
    return reports


def _parse_sections(text: str) -> list[_Section]:
    lines = text.splitlines()
    sections: list[_Section] = []
    header: str | None = None
    header_line: int = 0
    body_start: int = 0
    body_lines: list[str] = []

    def _flush() -> None:
        if header is None:
            return
        sections.append(
            _Section(
                header=header,
                canonical=_match_section(header),
                header_line=header_line,
                body="\n".join(body_lines),
                body_start_line=body_start,
            )
        )

    for idx, line in enumerate(lines, start=1):
        if line.startswith("## ") and not line.startswith("### "):
            _flush()
            header = line[3:].strip()
            header_line = idx
            body_start = idx + 1
            body_lines = []
        elif header is not None:
            body_lines.append(line)
    _flush()
    return sections


def _match_section(header: str) -> str | None:
    lower = header.lower().strip()
    for canonical, aliases in SECTION_ALIASES.items():
        for alias in aliases:
            if lower.startswith(alias.lower()):
                return canonical
    return None


def _load_manifest(preset_dir: Path) -> dict:
    path = preset_dir / "manifest.json"
    if not path.exists():
        return {}
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return {}


def _has_sentinel(body: str, sentinels: tuple[str, ...]) -> bool:
    return any(sentinel in body for sentinel in sentinels)


def _check_color_tokens(
    section: _Section, manifest: dict, report: PreviewLintReport
) -> None:
    body = section.body
    full_text = f"{section.header}\n{body}"
    has_sentinel = _has_sentinel(body, COLOR_FALLBACK_SENTINELS)

    candidates = _HEX_IN_BACKTICKS.findall(full_text)
    valid_hex = [c for c in candidates if _VALID_HEX.match(c)]

    if not has_sentinel and len(valid_hex) < 4:
        report.errors.append(
            PreviewIssue(
                code="E004",
                message=(
                    f'Color Tokens has {len(valid_hex)} valid HEX swatch(es); '
                    f"expected >= 4 (primary/surface/ink/border)."
                ),
                line=section.header_line,
            )
        )

    for candidate in candidates:
        if not _VALID_HEX.match(candidate):
            report.warnings.append(
                PreviewIssue(
                    code="W001",
                    message=f'malformed HEX "{candidate}" (expected #RRGGBB)',
                    line=section.header_line,
                )
            )

    color_modes = manifest.get("color_modes") or []
    mentions_dark = "dark" in full_text.lower()
    if "dark" in color_modes and not mentions_dark:
        report.errors.append(
            PreviewIssue(
                code="E005",
                message=(
                    'manifest.color_modes contains "dark" but Color Tokens '
                    "section never mentions dark."
                ),
                line=section.header_line,
            )
        )
    if color_modes and "dark" not in color_modes and mentions_dark:
        report.errors.append(
            PreviewIssue(
                code="E006",
                message=(
                    "manifest.color_modes is light-only but Color Tokens "
                    "section references dark (drift)."
                ),
                line=section.header_line,
            )
        )


def _check_typography(
    section: _Section, manifest: dict, report: PreviewLintReport
) -> None:
    body = section.body
    has_sentinel = _has_sentinel(body, TYPOGRAPHY_FALLBACK_SENTINELS)

    font_bullet = re.compile(
        r"^\s*-\s+(heading|body|mono|korean|serif|sans)\s*[:=]",
        re.IGNORECASE | re.MULTILINE,
    )
    has_font_bullet = bool(font_bullet.search(body))

    if not has_sentinel and not has_font_bullet:
        report.errors.append(
            PreviewIssue(
                code="E007",
                message="Typography section has no heading/body font bullet.",
                line=section.header_line,
            )
        )

    locale_pairings = manifest.get("locale_pairings") or {}
    if "ko" in locale_pairings and not has_sentinel:
        lower_body = body.lower()
        ko_mentioned = (
            "pretendard" in lower_body
            or "korean" in lower_body
            or "한국" in body
        )
        if not ko_mentioned:
            report.warnings.append(
                PreviewIssue(
                    code="W002",
                    message=(
                        'manifest.locale_pairings has "ko" but Typography '
                        "section never mentions Pretendard/korean."
                    ),
                    line=section.header_line,
                )
            )


def _check_components(section: _Section, report: PreviewLintReport) -> None:
    body = section.body
    if _has_sentinel(body, COMPONENT_FALLBACK_SENTINELS):
        return
    bullet_count = sum(1 for line in body.splitlines() if _BULLET_LINE.match(line))
    if bullet_count < 3:
        report.errors.append(
            PreviewIssue(
                code="E008",
                message=(
                    f"대표 컴포넌트 section has {bullet_count} bullet(s); "
                    "expected >= 3 (PLAN §9.3)."
                ),
                line=section.header_line,
            )
        )


def _check_caveats(section: _Section, report: PreviewLintReport) -> None:
    body = section.body
    bullet_count = sum(1 for line in body.splitlines() if _BULLET_LINE.match(line))
    if bullet_count == 0:
        report.warnings.append(
            PreviewIssue(
                code="W003",
                message="주의사항 section has no bullet content.",
                line=section.header_line,
            )
        )


def format_report(report: PreviewLintReport) -> str:
    status = "OK"
    if report.errors:
        status = f"ERROR({len(report.errors)})"
    elif report.warnings:
        status = f"WARN({len(report.warnings)})"
    lines = [f"[{report.preset_id}] {status}"]
    for issue in report.errors:
        loc = f":{issue.line}" if issue.line else ""
        lines.append(f"  ERROR {issue.code}{loc} {issue.message}")
    for issue in report.warnings:
        loc = f":{issue.line}" if issue.line else ""
        lines.append(f"  WARN  {issue.code}{loc} {issue.message}")
    return "\n".join(lines)


def format_reports(reports: list[PreviewLintReport]) -> str:
    if not reports:
        return "No presets checked."
    total_errors = sum(len(r.errors) for r in reports)
    total_warnings = sum(len(r.warnings) for r in reports)
    ok_count = sum(1 for r in reports if r.ok)
    blocks = [format_report(r) for r in reports]
    summary = (
        f"Checked {len(reports)} preset(s). "
        f"OK: {ok_count} / ERRORS: {total_errors} / WARNINGS: {total_warnings}"
    )
    return "\n".join(blocks + ["", summary])
