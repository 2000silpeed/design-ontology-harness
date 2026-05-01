from __future__ import annotations

import subprocess
import sys
from pathlib import Path

from design_ontology_harness.adapters import load_preset_bundle
from design_ontology_harness.adapters.base import implementation_contract
from design_ontology_harness.implementation_linter import lint_implementation
from design_ontology_harness.synthesis import REFERENCE_ABSORPTION_SCOPE


REPO_ROOT = Path(__file__).resolve().parent.parent


def test_token_bound_css_passes(tmp_path: Path):
    (tmp_path / "design-system").mkdir()
    (tmp_path / "design-system" / "tokens.css").write_text(
        ":root { --ds-color-primary: #0071A8; --ds-radius-sm: 4px; }\n",
        encoding="utf-8",
    )
    (tmp_path / "styles.css").write_text(
        """
        .panel {
          color: var(--ds-color-ink);
          background: color-mix(in srgb, var(--ds-color-surface-tint) 24%, var(--ds-color-surface));
          border-color: var(--ds-color-border);
          border-radius: var(--ds-radius-sm);
          font-family: var(--ds-font-ko);
        }
        .dot { border-radius: 999px; }
        """,
        encoding="utf-8",
    )

    report = lint_implementation(tmp_path)

    assert report.ok
    assert report.checked_files == ["styles.css"]


def test_flags_hardcoded_visual_values(tmp_path: Path):
    (tmp_path / "styles.css").write_text(
        """
        .bad {
          color: #123456;
          background: rgb(10, 20, 30);
          border-color: teal;
          border-radius: 8px;
          font-family: Inter, sans-serif;
        }
        """,
        encoding="utf-8",
    )

    report = lint_implementation(tmp_path)
    codes = {issue.code for issue in report.issues}

    assert not report.ok
    assert {"DS001", "DS002", "DS003", "DS010", "DS020"} <= codes


def test_flags_token_bound_reference_palette_mixing(tmp_path: Path):
    (tmp_path / "styles.css").write_text(
        """
        :root {
          --chart-secondary: color-mix(in srgb, var(--ds-color-info) 52%, var(--ds-color-surface-tint));
          --sidebar-bg: color-mix(in srgb, var(--ds-color-info) 84%, var(--ds-color-ink) 16%);
          --panel-shadow: color-mix(in srgb, var(--ds-color-ink) 12%, transparent);
        }
        """,
        encoding="utf-8",
    )

    report = lint_implementation(tmp_path)
    codes = {issue.code for issue in report.issues}

    assert not report.ok
    assert {"DS030", "DS031"} <= codes


def test_ignores_design_system_and_managed_blocks(tmp_path: Path):
    (tmp_path / "design-system").mkdir()
    (tmp_path / "design-system" / "tokens.css").write_text(
        ":root { --ds-color-primary: #0071A8; }\n",
        encoding="utf-8",
    )
    (tmp_path / "app.css").write_text(
        """
        /* design-ontology:START */
        :root { --ds-color-primary: #0071A8; }
        body { font-family: Inter, sans-serif; color: #111111; border-radius: 8px; }
        /* design-ontology:END */

        .user {
          color: var(--ds-color-ink);
          border-radius: var(--ds-radius-sm);
          font-family: var(--ds-font-body);
        }
        """,
        encoding="utf-8",
    )

    report = lint_implementation(tmp_path)

    assert report.ok
    assert report.checked_files == ["app.css"]


def test_implementation_contract_declares_reference_scope():
    bundle = load_preset_bundle(REPO_ROOT / "presets" / "conversation-copilot--corporate-trust")
    contract = implementation_contract(bundle)

    assert "Reference Absorption Scope" in contract
    assert "Allowed from visual references" in contract
    assert "Denied from visual references" in contract
    assert "color palette" in contract
    assert "palette composition or derived secondary palettes" in contract
    assert "Feedback Promotion Rule" in contract
    assert "uv run design-ontology lint-implementation --target-repo ." in contract


def test_reference_absorption_scope_is_structured_for_ontology():
    assert "component morphology" in REFERENCE_ABSORPTION_SCOPE["allowed"]
    assert "layout density" in REFERENCE_ABSORPTION_SCOPE["allowed"]
    assert "color palette" in REFERENCE_ABSORPTION_SCOPE["denied"]
    assert "palette composition or derived secondary palettes" in REFERENCE_ABSORPTION_SCOPE["denied"]
    assert "typography family or scale" in REFERENCE_ABSORPTION_SCOPE["denied"]
    assert "product data model" in REFERENCE_ABSORPTION_SCOPE["denied"]
    assert REFERENCE_ABSORPTION_SCOPE["failure_patterns"][0]["id"] == "token-bound-reference-palette-mixing"
    assert REFERENCE_ABSORPTION_SCOPE["promotion_policy"]["id"] == "implementation-feedback-promotion"


def test_cli_exits_nonzero_on_implementation_violation(tmp_path: Path):
    (tmp_path / "styles.css").write_text(
        ".bad { color: #123456; }\n",
        encoding="utf-8",
    )

    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "design_ontology_harness.cli",
            "lint-implementation",
            "--target-repo",
            str(tmp_path),
        ],
        cwd=REPO_ROOT,
        text=True,
        capture_output=True,
        check=False,
    )

    assert result.returncode == 1
    assert "DS001" in result.stdout
