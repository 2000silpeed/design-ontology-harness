"""Phase 11-5: preset installer smoke tests.

Exercises install_preset against temp target repos:
- Full install emits INSTALLED.json with expected contract fields.
- Re-install with unchanged inputs becomes a noop (idempotent).
- `force=True` re-applies and produces status='reinstalled'.
- Unsupported color_mode / unknown adapter / unknown preset id all raise
  with clear error types the CLI can surface.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from design_ontology_harness.preset_installer import (
    INSTALLED_FILENAME,
    InstallRequest,
    install_preset,
)


def _read_installed(target_repo: Path) -> dict:
    return json.loads((target_repo / INSTALLED_FILENAME).read_text(encoding="utf-8"))


def test_install_writes_INSTALLED_json_with_contract_fields(tmp_path: Path):
    outcome = install_preset(
        InstallRequest(
            preset_id="dashboard--minimal-tech",
            target_repo=tmp_path,
            adapter_id="nextjs-tailwind-shadcn",
            color_mode="light",
            locale="ko",
        )
    )
    assert outcome.status == "installed"
    assert outcome.preset_id == "dashboard--minimal-tech"
    assert outcome.adapter_id == "nextjs-tailwind-shadcn"
    assert outcome.color_mode == "light"
    assert outcome.locale == "ko"
    assert outcome.content_hash.startswith("sha256:")
    assert outcome.created, "expected at least one created file on a fresh install"
    assert not outcome.proposed, f"unexpected .ds-proposed on fresh target: {outcome.proposed}"

    installed_path = tmp_path / INSTALLED_FILENAME
    assert installed_path.exists(), "INSTALLED.json must be written"

    installed = _read_installed(tmp_path)
    for field in (
        "preset_id",
        "preset_api_version",
        "adapter_id",
        "adapter_version",
        "harness_version",
        "color_mode",
        "locale",
        "installed_at",
        "content_hash",
        "proposed_files",
        "counts",
    ):
        assert field in installed, f"INSTALLED.json missing {field}"

    assert installed["preset_id"] == "dashboard--minimal-tech"
    assert installed["preset_api_version"].startswith("1.")
    assert installed["content_hash"].startswith("sha256:")
    assert installed["counts"]["created"] >= 1

    # The adapter must have dropped a design-system/ mirror for agent-pack skills.
    assert (tmp_path / "design-system" / "manifest.json").exists()
    assert (tmp_path / "tailwind.config.ts").exists()
    assert (tmp_path / "app" / "globals.css").exists()
    assert (tmp_path / "components.json").exists()


def test_reinstall_is_noop_when_nothing_changed(tmp_path: Path):
    first = install_preset(
        InstallRequest(
            preset_id="dashboard--minimal-tech",
            target_repo=tmp_path,
            color_mode="light",
            locale="ko",
        )
    )
    assert first.status == "installed"
    first_installed = _read_installed(tmp_path)

    second = install_preset(
        InstallRequest(
            preset_id="dashboard--minimal-tech",
            target_repo=tmp_path,
            color_mode="light",
            locale="ko",
        )
    )
    assert second.status == "noop", (
        "second install with identical inputs must be a noop"
    )
    # INSTALLED.json must not be rewritten on noop (timestamp stays).
    second_installed = _read_installed(tmp_path)
    assert second_installed["installed_at"] == first_installed["installed_at"]


def test_force_reinstall_rewrites(tmp_path: Path):
    install_preset(
        InstallRequest(
            preset_id="dashboard--minimal-tech",
            target_repo=tmp_path,
            color_mode="light",
            locale="ko",
        )
    )
    forced = install_preset(
        InstallRequest(
            preset_id="dashboard--minimal-tech",
            target_repo=tmp_path,
            color_mode="light",
            locale="ko",
            force=True,
        )
    )
    assert forced.status == "reinstalled"


def test_unsupported_color_mode_raises(tmp_path: Path):
    # commerce--editorial-warm is declared light-only.
    with pytest.raises(ValueError):
        install_preset(
            InstallRequest(
                preset_id="commerce--editorial-warm",
                target_repo=tmp_path,
                color_mode="dark",
                locale="ko",
            )
        )


def test_unknown_preset_raises(tmp_path: Path):
    with pytest.raises(FileNotFoundError):
        install_preset(
            InstallRequest(
                preset_id="nonexistent--minimal-tech",
                target_repo=tmp_path,
            )
        )


def test_unknown_adapter_raises(tmp_path: Path):
    with pytest.raises(KeyError):
        install_preset(
            InstallRequest(
                preset_id="dashboard--minimal-tech",
                target_repo=tmp_path,
                adapter_id="ghost-adapter",
            )
        )


def test_default_color_mode_when_omitted(tmp_path: Path):
    # Preset default is 'light'. Omitting --color-mode must fall back to it.
    outcome = install_preset(
        InstallRequest(
            preset_id="dashboard--minimal-tech",
            target_repo=tmp_path,
            color_mode=None,
            locale="en",
        )
    )
    assert outcome.color_mode == "light"


def test_both_color_mode_falls_back_to_default(tmp_path: Path):
    # 'both' is valid in MatchQuery but ambiguous at install-time.
    outcome = install_preset(
        InstallRequest(
            preset_id="conversation-copilot--minimal-tech",
            target_repo=tmp_path,
            color_mode="both",
            locale="ko",
        )
    )
    # conversation-copilot--minimal-tech has default_color_mode='light'.
    assert outcome.color_mode == "light"
