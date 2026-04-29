#!/usr/bin/env python3
"""Verify plugin DEMO_SCRIPTS.md expected Top-1 matcher results."""

from __future__ import annotations

import argparse
import re
import sys
from dataclasses import dataclass
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT))

from design_ontology_harness.preset_matcher.engine import MatchQuery, match_presets  # noqa: E402


APP_MODES = (
    "dashboard",
    "document-content",
    "marketing-landing",
    "commerce",
    "conversation-copilot",
    "canvas-tool",
    "community-feed",
    "monitoring-ops",
)
BRAND_TONES = (
    "minimal-tech",
    "editorial-warm",
    "bold-confident",
    "playful-soft",
    "corporate-trust",
)
COLOR_MODES = ("light", "dark", "both")


@dataclass(slots=True)
class DemoScenario:
    title: str
    expected_preset: str
    expected_bucket: str | None
    query: MatchQuery


def _section_spans(text: str) -> list[tuple[str, str]]:
    matches = list(re.finditer(r"^### .+$", text, flags=re.MULTILINE))
    sections: list[tuple[str, str]] = []
    for index, match in enumerate(matches):
        start = match.start()
        end = matches[index + 1].start() if index + 1 < len(matches) else len(text)
        sections.append((match.group(0).strip(), text[start:end]))
    return sections


def _first_expected(section: str, title: str) -> tuple[str | None, str | None]:
    expected = re.search(
        r"1\.\s+.*?([a-z0-9-]+--[a-z0-9-]+)\s+\[(High|Medium|Low)\]",
        section,
    )
    if expected:
        return expected.group(1), expected.group(2)

    heading = re.search(r"`([a-z0-9-]+--[a-z0-9-]+)`", title)
    if heading:
        return heading.group(1), None
    return None, None


def _parse_explicit_query(section: str) -> MatchQuery | None:
    def _line_value(label: str, options: tuple[str, ...]) -> str | None:
        pattern = rf"\?\s*{label}.*?→[^\n]*({'|'.join(map(re.escape, options))})"
        match = re.search(pattern, section, flags=re.IGNORECASE)
        return match.group(1) if match else None

    app_mode = _line_value("뭘", APP_MODES)
    brand_tone = _line_value("분위기", BRAND_TONES)
    color_mode = _line_value("색상 모드", COLOR_MODES)
    if not app_mode and not brand_tone:
        return None

    stack = None
    if "nextjs-tailwind-shadcn" in section or "Next+shadcn" in section:
        stack = "nextjs-tailwind-shadcn"
    elif "raw-css-variables" in section:
        stack = "raw-css-variables"
    locale = "ko" if re.search(r"한글 UI.*→\s*Y", section) else None
    return MatchQuery(
        app_mode=app_mode,
        brand_tone=brand_tone,
        color_mode=color_mode,
        stack=stack,
        locale=locale,
    )


def parse_scenarios(text: str) -> list[DemoScenario]:
    scenarios: list[DemoScenario] = []
    for title, section in _section_spans(text):
        expected_preset, expected_bucket = _first_expected(section, title)
        if not expected_preset:
            continue

        free_text = re.search(r"/design-start\s+\"([^\"]+)\"", section)
        query = MatchQuery(free_text=free_text.group(1)) if free_text else _parse_explicit_query(section)
        if query is None:
            raise ValueError(f"could not parse query for {title}")

        scenarios.append(DemoScenario(title, expected_preset, expected_bucket, query))
    return scenarios


def verify(path: Path) -> tuple[list[str], list[str]]:
    text = path.read_text(encoding="utf-8")
    failures: list[str] = []
    notes: list[str] = []
    scenarios = parse_scenarios(text)
    if not scenarios:
        failures.append(f"no demo scenarios parsed from {path}")
        return failures, notes

    for scenario in scenarios:
        results = match_presets(scenario.query, top_k=3)
        if not results:
            failures.append(f"{scenario.title}: matcher returned no results")
            continue
        top = results[0]
        if top.preset_id != scenario.expected_preset:
            failures.append(
                f"{scenario.title}: expected {scenario.expected_preset}, got {top.preset_id}"
            )
            continue
        if scenario.expected_bucket and top.bucket != scenario.expected_bucket:
            failures.append(
                f"{scenario.title}: expected bucket {scenario.expected_bucket}, got {top.bucket}"
            )
            continue
        notes.append(f"{scenario.title}: {top.preset_id} [{top.bucket}]")
    return failures, notes


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--demo-path",
        type=Path,
        default=REPO_ROOT.parent / "design-ontology-plugin" / "docs" / "DEMO_SCRIPTS.md",
    )
    args = parser.parse_args()

    failures, notes = verify(args.demo_path)
    for note in notes:
        print(f"[verify-demo-scripts] OK {note}")
    if failures:
        print("[verify-demo-scripts] FAIL", file=sys.stderr)
        for failure in failures:
            print(f"  - {failure}", file=sys.stderr)
        return 1
    print(f"[verify-demo-scripts] all {len(notes)} scenarios matched")
    return 0


if __name__ == "__main__":
    sys.exit(main())
