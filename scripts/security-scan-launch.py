#!/usr/bin/env python3
"""Lightweight launch secret scan for harness + plugin worktrees.

This is intentionally high-signal: it scans for private-key blocks and common
token prefixes, not generic words like "token" that appear throughout docs.
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parent.parent

PATTERNS = {
    "private-key": re.compile(r"-----BEGIN (?:RSA |OPENSSH |EC |DSA |)?PRIVATE KEY-----"),
    "github-token": re.compile(r"\b(?:ghp|gho|ghu|ghs|ghr)_[A-Za-z0-9_]{30,}\b"),
    "github-pat": re.compile(r"\bgithub_pat_[A-Za-z0-9_]{50,}\b"),
    "openai-key": re.compile(r"\bsk-[A-Za-z0-9]{32,}\b"),
    "slack-token": re.compile(r"\bxox[baprs]-[A-Za-z0-9-]{20,}\b"),
    "aws-access-key": re.compile(r"\bAKIA[0-9A-Z]{16}\b"),
}

SKIP_DIRS = {
    ".git",
    ".next",
    ".venv",
    "__pycache__",
    "node_modules",
    "dist",
    "build",
}
SKIP_SUFFIXES = {
    ".png",
    ".jpg",
    ".jpeg",
    ".webp",
    ".woff",
    ".woff2",
    ".pdf",
    ".lock",
}


def _iter_files(root: Path):
    for path in root.rglob("*"):
        if not path.is_file():
            continue
        if any(part in SKIP_DIRS for part in path.parts):
            continue
        if path.suffix.lower() in SKIP_SUFFIXES:
            continue
        yield path


def scan_roots(roots: list[Path]) -> list[str]:
    findings: list[str] = []
    for root in roots:
        if not root.exists():
            findings.append(f"missing root: {root}")
            continue
        for path in _iter_files(root):
            try:
                text = path.read_text(encoding="utf-8")
            except UnicodeDecodeError:
                continue
            for line_no, line in enumerate(text.splitlines(), start=1):
                for name, pattern in PATTERNS.items():
                    if pattern.search(line):
                        findings.append(f"{path}:{line_no}: {name}")
    return findings


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--root",
        type=Path,
        action="append",
        default=[],
        help="Root to scan. May be provided multiple times.",
    )
    args = parser.parse_args()

    roots = args.root or [REPO_ROOT, REPO_ROOT.parent / "design-ontology-plugin"]
    findings = scan_roots(roots)
    if findings:
        print("[security-scan-launch] potential secrets found:", file=sys.stderr)
        for finding in findings:
            print(f"  - {finding}", file=sys.stderr)
        return 1
    print("[security-scan-launch] OK — no high-confidence secrets found")
    return 0


if __name__ == "__main__":
    sys.exit(main())
