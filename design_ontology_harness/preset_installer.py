"""Preset installer — Phase 11-2.

Entry point for the plugin: given a preset id + target repo + adapter, render
the preset into the target and record `design-system/INSTALLED.json` so the
existing agent-pack skills (design-system-architect etc.) can verify the
contract via `Step 0`.

    install_preset(InstallRequest) -> InstallOutcome

Idempotency:
    If `design-system/INSTALLED.json` already exists and its recorded
    content_hash matches the preset's current hash, we no-op (unless
    `force=True`). Otherwise we re-apply.

INSTALLED.json schema (written next to the design-system bundle):

    {
      "preset_id": "...",
      "preset_api_version": "1.0.0",
      "adapter_id": "nextjs-tailwind-shadcn",
      "adapter_version": "0.1.0",
      "harness_version": "0.1.0",
      "color_mode": "light",
      "locale": "ko",
      "installed_at": "2026-04-18T...Z",
      "content_hash": "sha256:...",
      "proposed_files": ["tailwind.config.ts.ds-proposed", ...],
      "counts": {"created": 12, "merged": 0, "overwritten": 0, "proposed": 0, "skipped": 0}
    }
"""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from pathlib import Path

from .adapters import ApplyReport, FileOp, get_adapter, load_preset_bundle
from .adapters.base import PresetBundle
from .preset_builder import PRESETS_ROOT, _detect_harness_version


INSTALLED_FILENAME = "design-system/INSTALLED.json"


@dataclass
class InstallRequest:
    preset_id: str
    target_repo: Path
    adapter_id: str = "nextjs-tailwind-shadcn"
    color_mode: str | None = None
    locale: str = "en"
    force: bool = False
    presets_root: Path | None = None


@dataclass
class InstallOutcome:
    preset_id: str
    adapter_id: str
    adapter_version: str
    color_mode: str
    locale: str
    target_repo: str
    installed_path: str
    status: str  # "installed" | "reinstalled" | "noop"
    content_hash: str
    created: list[str] = field(default_factory=list)
    merged: list[str] = field(default_factory=list)
    overwritten: list[str] = field(default_factory=list)
    proposed: list[tuple[str, str]] = field(default_factory=list)
    skipped: list[str] = field(default_factory=list)

    def to_dict(self) -> dict:
        data = asdict(self)
        # tuple[str, str] → list[str, str] for JSON
        data["proposed"] = [[p, r] for p, r in self.proposed]
        return data

    def format_human(self) -> str:
        lines = [
            f"[install-preset] {self.status}  {self.preset_id} → {self.target_repo}",
            f"  adapter: {self.adapter_id}@{self.adapter_version} / "
            f"color_mode={self.color_mode} / locale={self.locale}",
        ]
        if self.status == "noop":
            lines.append("  (content_hash 변화 없음 — 설치 생략, --force 로 재적용)")
            return "\n".join(lines)

        lines.append(
            f"  파일: created={len(self.created)} merged={len(self.merged)} "
            f"overwritten={len(self.overwritten)} proposed={len(self.proposed)} "
            f"skipped={len(self.skipped)}"
        )
        for path in self.created[:10]:
            lines.append(f"    + {path}")
        for path in self.merged[:10]:
            lines.append(f"    ~ {path}")
        for path in self.overwritten[:10]:
            lines.append(f"    * {path}")
        for path, reason in self.proposed[:10]:
            lines.append(f"    ? {path}  ({reason})")
        total = len(self.created) + len(self.merged) + len(self.overwritten) + len(self.proposed)
        if total > 40:
            lines.append(f"    … 외 {total - 40}개")
        lines.append(f"  installed 기록: {self.installed_path}")
        return "\n".join(lines)


def _resolve_preset_dir(preset_id: str, presets_root: Path | None) -> Path:
    root = presets_root or PRESETS_ROOT
    preset_dir = root / preset_id
    if not preset_dir.exists() or not (preset_dir / "manifest.json").exists():
        raise FileNotFoundError(
            f"preset '{preset_id}' not found under {root} "
            f"(expected {preset_dir}/manifest.json)"
        )
    return preset_dir


def _read_existing_installed(target_repo: Path) -> dict | None:
    path = target_repo / INSTALLED_FILENAME
    if not path.exists():
        return None
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return None


def _resolve_color_mode(bundle: PresetBundle, requested: str | None) -> str:
    if requested is None:
        return bundle.default_color_mode
    if requested == "both":
        # "both" at install-time is ambiguous — pick the default.
        return bundle.default_color_mode
    if requested not in bundle.color_modes:
        raise ValueError(
            f"preset {bundle.id} does not support color_mode='{requested}' "
            f"(supported: {bundle.color_modes})"
        )
    return requested


def install_preset(request: InstallRequest) -> InstallOutcome:
    """Render + apply a preset into target_repo, writing INSTALLED.json."""

    preset_dir = _resolve_preset_dir(request.preset_id, request.presets_root)
    bundle = load_preset_bundle(preset_dir)

    adapter_cls = get_adapter(request.adapter_id)
    adapter = adapter_cls()

    color_mode = _resolve_color_mode(bundle, request.color_mode)
    locale = request.locale or "en"

    target_repo = request.target_repo.resolve()
    target_repo.mkdir(parents=True, exist_ok=True)

    existing = _read_existing_installed(target_repo)
    current_hash = bundle.manifest.get("content_hash", "")

    if (
        existing is not None
        and existing.get("preset_id") == request.preset_id
        and existing.get("content_hash") == current_hash
        and existing.get("adapter_id") == request.adapter_id
        and existing.get("color_mode") == color_mode
        and existing.get("locale") == locale
        and not request.force
    ):
        return InstallOutcome(
            preset_id=request.preset_id,
            adapter_id=request.adapter_id,
            adapter_version=getattr(adapter, "version", "0.0.0"),
            color_mode=color_mode,
            locale=locale,
            target_repo=str(target_repo),
            installed_path=str(target_repo / INSTALLED_FILENAME),
            status="noop",
            content_hash=current_hash,
        )

    ops: list[FileOp] = adapter.render(bundle, target_repo, color_mode, locale=locale)
    report: ApplyReport = adapter.apply(target_repo, ops)

    proposed_paths = [p for p, _ in report.proposed]
    status = "reinstalled" if existing is not None else "installed"

    installed = {
        "preset_id": request.preset_id,
        "preset_api_version": bundle.manifest.get("preset_api_version"),
        "adapter_id": request.adapter_id,
        "adapter_version": getattr(adapter, "version", "0.0.0"),
        "harness_version": _detect_harness_version(),
        "color_mode": color_mode,
        "locale": locale,
        "installed_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "content_hash": current_hash,
        "proposed_files": proposed_paths,
        "counts": {
            "created": len(report.created),
            "merged": len(report.merged),
            "overwritten": len(report.overwritten),
            "proposed": len(report.proposed),
            "skipped": len(report.skipped),
        },
    }

    installed_path = target_repo / INSTALLED_FILENAME
    installed_path.parent.mkdir(parents=True, exist_ok=True)
    installed_path.write_text(
        json.dumps(installed, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )

    return InstallOutcome(
        preset_id=request.preset_id,
        adapter_id=request.adapter_id,
        adapter_version=getattr(adapter, "version", "0.0.0"),
        color_mode=color_mode,
        locale=locale,
        target_repo=str(target_repo),
        installed_path=str(installed_path),
        status=status,
        content_hash=current_hash,
        created=list(report.created),
        merged=list(report.merged),
        overwritten=list(report.overwritten),
        proposed=list(report.proposed),
        skipped=list(report.skipped),
    )
