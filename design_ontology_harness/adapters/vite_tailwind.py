"""Vite + Tailwind adapter — Phase 10C.

Targets pure Vite + React + Tailwind repos (no shadcn, no Next). Users who
already run shadcn on Next.js should pick the `nextjs-tailwind-shadcn` adapter
instead — this one does NOT emit `components.json` or `app/globals.css`.

Outputs (PLUGIN_PLAN §7.1):
    tailwind.config.ts      — theme.extend + content = ./index.html + ./src/**
    src/index.css           — @tailwind directives + :root tokens + (dark blocks)
                              + html/body base styles (wrapped in managed block)
    public/fonts/...        — Pretendard placeholder + LICENSE-FONTS (when locale=ko)
    scripts/fetch-pretendard.mjs — helper to download Pretendard (ko)
    design-system/          — shared preset mirror (manifest/system_spec/...)

Merge rules (§7.4):
    * tailwind.config.ts        → managed-block replace; no marker ⇒ .ds-proposed
    * src/index.css             → managed-block replace (includes @tailwind lines
                                  so the block is self-contained); no marker ⇒ .ds-proposed
    * public/fonts/** / scripts/fetch-pretendard.mjs → generator-owned → overwrite
    * design-system/**          → overwrite
    * anything else             → .ds-proposed
"""

from __future__ import annotations

import json
from pathlib import Path

from .base import (
    DS_BLOCK_END,
    DS_BLOCK_START,
    FileOp,
    LocalePairing,
    PresetBundle,
    StackAdapter,
    TypographyPlan,
    build_tailwind_config_body,
    css_var_declarations,
    design_system_mirror_ops,
    pretendard_asset_ops,
    pretendard_font_face_block,
    replace_managed_block,
    resolve_locale_pairing,
    tokens_for_mode,
    typography_plan,
    wrap_managed_css,
)


ADAPTER_ID = "vite-tailwind"
ADAPTER_VERSION = "0.1.0"
SUPPORTED_PRESET_API = ">=1.0.0 <2.0.0"


_CONTENT_PATHS = [
    "./index.html",
    "./src/**/*.{ts,tsx,js,jsx,mdx}",
]


# ---------------------------------------------------------------------------
# File builders


def _build_index_css(
    bundle: PresetBundle,
    color_modes: list[str],
    locale: str,
    pairing: LocalePairing | None,
    typography: TypographyPlan,
) -> str:
    """Single self-contained managed block for src/index.css.

    Includes the three @tailwind directives at the top so that installing the
    adapter into a fresh Vite project wires Tailwind correctly without forcing
    the user to hand-edit the file. On re-apply the entire block (including the
    directives) is replaced atomically.
    """

    lines: list[str] = []
    lines.append(f"/* preset: {bundle.id} — locale: {locale} */")
    lines.append("@tailwind base;")
    lines.append("@tailwind components;")
    lines.append("@tailwind utilities;")

    if locale == "ko" and pairing:
        lines.append("")
        lines.append(pretendard_font_face_block())

    light_tokens = tokens_for_mode(bundle, "light")
    lines.append("")
    lines.append(":root {")
    lines.extend(css_var_declarations(light_tokens))
    lines.append(f"  --ds-font-heading: {typography.heading_stack};")
    lines.append(f"  --ds-font-body: {typography.body_stack};")
    lines.append(f"  --ds-font-mono: {typography.mono_stack};")
    lines.append("  --ds-radius-sm: 4px;")
    lines.append("  --ds-radius-md: 8px;")
    lines.append("  --ds-radius-lg: 12px;")
    lines.append("}")

    if "dark" in color_modes:
        dark_tokens = tokens_for_mode(bundle, "dark")
        lines.append("")
        lines.append("[data-theme='dark'] {")
        lines.extend(css_var_declarations(dark_tokens))
        lines.append("}")

        lines.append("")
        lines.append("@media (prefers-color-scheme: dark) {")
        lines.append("  :root:not([data-theme='light']) {")
        for decl in css_var_declarations(dark_tokens):
            lines.append("  " + decl)
        lines.append("  }")
        lines.append("}")

    lines.append("")
    lines.append("html, body {")
    lines.append("  background: var(--ds-color-canvas);")
    lines.append("  color: var(--ds-color-ink);")
    lines.append("  font-family: var(--ds-font-body);")
    lines.append("}")

    return wrap_managed_css("\n".join(lines))


# ---------------------------------------------------------------------------
# Adapter class


class ViteTailwindAdapter(StackAdapter):
    id: str = ADAPTER_ID
    version: str = ADAPTER_VERSION
    supported_preset_api: str = SUPPORTED_PRESET_API

    def detect(self, target_repo: Path) -> float:
        score = 0.0
        pkg = target_repo / "package.json"
        if pkg.exists():
            try:
                data = json.loads(pkg.read_text(encoding="utf-8"))
                deps: dict = {}
                for key in ("dependencies", "devDependencies", "peerDependencies"):
                    value = data.get(key)
                    if isinstance(value, dict):
                        deps.update(value)
                if "vite" in deps:
                    score += 0.4
                if "tailwindcss" in deps:
                    score += 0.2
                if "react" in deps or "@vitejs/plugin-react" in deps:
                    score += 0.1
                if "next" in deps:
                    # Yield to the Next adapter in hybrid/monorepo setups.
                    score -= 0.3
            except json.JSONDecodeError:
                pass

        for ext in ("ts", "mts", "js", "mjs"):
            if (target_repo / f"vite.config.{ext}").exists():
                score += 0.15
                break

        for ext in ("ts", "mts", "cts", "js", "mjs", "cjs"):
            if (target_repo / f"tailwind.config.{ext}").exists():
                score += 0.15
                break

        return round(min(max(score, 0.0), 1.0), 3)

    def render(
        self,
        preset: PresetBundle,
        target_repo: Path,
        color_mode: str,
        locale: str = "en",
    ) -> list[FileOp]:
        supported_modes = preset.color_modes or [preset.default_color_mode]
        if color_mode not in supported_modes:
            raise ValueError(
                f"preset {preset.id} does not support color_mode='{color_mode}' "
                f"(supported: {supported_modes})"
            )

        pairing = resolve_locale_pairing(preset, locale) if locale != "en" else None
        typography = typography_plan(preset, pairing)

        ops: list[FileOp] = []
        ops.append(
            FileOp(
                path="tailwind.config.ts",
                content=build_tailwind_config_body(
                    preset,
                    color_modes=supported_modes,
                    typography=typography,
                    content_paths=_CONTENT_PATHS,
                    adapter_id=ADAPTER_ID,
                    adapter_version=ADAPTER_VERSION,
                ),
                action="create",
            )
        )
        ops.append(
            FileOp(
                path="src/index.css",
                content=_build_index_css(
                    preset,
                    supported_modes,
                    locale,
                    pairing,
                    typography,
                ),
                action="create",
            )
        )
        ops.extend(design_system_mirror_ops(preset))

        if locale == "ko" and pairing:
            ops.extend(
                pretendard_asset_ops(
                    assets_dir="public/fonts",
                    fetch_script_path="scripts/fetch-pretendard.mjs",
                )
            )

        return ops

    def merge(self, op: FileOp, existing_path: Path) -> FileOp:
        path = op.path
        try:
            existing = existing_path.read_text(encoding="utf-8")
        except (FileNotFoundError, UnicodeDecodeError):
            return FileOp(
                path=f"{path}.ds-proposed",
                content=op.content,
                action="proposed",
                reason="unreadable existing file",
                original_path=path,
            )

        if path.startswith("design-system/"):
            return FileOp(path=path, content=op.content, action="overwrite")

        if path.startswith("public/fonts/") or path == "scripts/fetch-pretendard.mjs":
            return FileOp(path=path, content=op.content, action="overwrite")

        if path in ("tailwind.config.ts", "src/index.css"):
            if DS_BLOCK_START not in existing or DS_BLOCK_END not in existing:
                return FileOp(
                    path=f"{path}.ds-proposed",
                    content=op.content,
                    action="proposed",
                    reason=f"existing {path} has no design-ontology managed block",
                    original_path=path,
                )
            start = op.content.find(DS_BLOCK_START)
            end = op.content.find(DS_BLOCK_END)
            if start == -1 or end == -1:
                return FileOp(
                    path=f"{path}.ds-proposed",
                    content=op.content,
                    action="proposed",
                    reason="generated block markers missing",
                    original_path=path,
                )
            new_body = op.content[start + len(DS_BLOCK_START) : end].strip()
            updated, _ = replace_managed_block(existing, new_body)
            return FileOp(path=path, content=updated, action="merge")

        return FileOp(
            path=f"{path}.ds-proposed",
            content=op.content,
            action="proposed",
            reason="no merge strategy for this path",
            original_path=path,
        )
