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

NAMED_COLOR_RE = re.compile(
    r"\b(?:black|white|red|green|blue|yellow|purple|orange|gray|grey|slate|teal|cyan|magenta|pink|brown)\b",
    re.IGNORECASE,
)

COLOR_PROPERTY_RE = re.compile(
    r"\b(?:color|background|background-color|border|border-color|outline|outline-color|box-shadow|text-shadow|fill|stroke)\s*:",
    re.IGNORECASE,
)

ALLOWED_RADIUS_VALUES = {"0", "0px", "50%", "999px", "inherit", "initial", "unset"}


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

    for path in _iter_candidate_files(target, artifact_dir=artifact_dir, extensions=extensions):
        rel = path.relative_to(target).as_posix()
        report.checked_files.append(rel)
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        report.issues.extend(_lint_text(text, rel))

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

    for line_no, raw_line in enumerate(text.splitlines(), start=1):
        if DS_BLOCK_START in raw_line:
            in_managed_block = True
        if in_managed_block:
            if DS_BLOCK_END in raw_line:
                in_managed_block = False
            continue

        line, in_block_comment = _strip_comment_segments(raw_line, in_block_comment)
        if not line.strip():
            continue

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
