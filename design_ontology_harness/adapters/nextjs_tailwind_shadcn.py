"""Next.js + Tailwind + shadcn adapter — MVP (Phase 10A).

Outputs (PLUGIN_PLAN §7.3):
    tailwind.config.ts      — theme.extend (colors via CSS vars, radius, fonts)
    app/globals.css         — :root tokens + [data-theme='dark'] + fonts
    components.json         — shadcn token mapping
    design-system/          — raw preset artifacts copied for agent-pack use
    public/fonts/...        — Pretendard placeholder + LICENSE-FONTS (when locale=ko)
    scripts/fetch-pretendard.mjs — helper to download Pretendard on-demand

Merge rules (§7.4):
    * tailwind.config.ts        → managed block `/* design-ontology:START */`
    * app/globals.css           → managed block, idempotent replace
    * components.json           → deep-merge; conflicts dropped to .ds-proposed
    * design-system/, fonts     → overwrite (generator-owned, not user code)
    * anything else, on conflict that cannot be merged: `<path>.ds-proposed`
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
    deep_merge_json,
    design_system_mirror_ops,
    pretendard_asset_ops,
    pretendard_font_face_block,
    replace_managed_block,
    resolve_locale_pairing,
    tokens_for_mode,
    typography_plan,
    wrap_managed_css,
)


ADAPTER_ID = "nextjs-tailwind-shadcn"
ADAPTER_VERSION = "0.1.0"
SUPPORTED_PRESET_API = ">=1.0.0 <2.0.0"


_CONTENT_PATHS = [
    "./app/**/*.{ts,tsx,js,jsx,mdx}",
    "./components/**/*.{ts,tsx,js,jsx,mdx}",
    "./design-system/**/*.{ts,tsx,js,jsx,mdx}",
]


# ---------------------------------------------------------------------------
# File builders


def _build_globals_css(
    bundle: PresetBundle,
    color_modes: list[str],
    locale: str,
    pairing: LocalePairing | None,
    typography: TypographyPlan,
) -> str:
    lines: list[str] = []
    lines.append(f"/* preset: {bundle.id} — locale: {locale} */")

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


def _build_components_json(bundle: PresetBundle) -> str:
    payload = {
        "$schema": "https://ui.shadcn.com/schema.json",
        "style": "default",
        "rsc": True,
        "tsx": True,
        "tailwind": {
            "config": "tailwind.config.ts",
            "css": "app/globals.css",
            "baseColor": "slate",
            "cssVariables": True,
            "prefix": "",
        },
        "aliases": {
            "components": "@/components",
            "utils": "@/lib/utils",
            "ui": "@/components/ui",
            "hooks": "@/hooks",
            "lib": "@/lib",
        },
        "x-design-ontology": {
            "preset": bundle.id,
            "adapter": f"{ADAPTER_ID}@{ADAPTER_VERSION}",
            "color_modes": bundle.color_modes,
            "locale_pairings": list(bundle.locale_pairings.keys()),
        },
    }
    return json.dumps(payload, ensure_ascii=False, indent=2) + "\n"


# ---------------------------------------------------------------------------
# Adapter class


class NextjsTailwindShadcnAdapter(StackAdapter):
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
                if "next" in deps:
                    score += 0.4
                if "tailwindcss" in deps:
                    score += 0.2
                if any(k in deps for k in ("@radix-ui/react-slot", "class-variance-authority")):
                    score += 0.1
            except json.JSONDecodeError:
                pass
        for ext in ("ts", "mts", "cts", "js", "mjs", "cjs"):
            if (target_repo / f"tailwind.config.{ext}").exists():
                score += 0.15
                break
        if (target_repo / "components.json").exists():
            score += 0.15
        return round(min(score, 1.0), 3)

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
                path="app/globals.css",
                content=_build_globals_css(
                    preset,
                    supported_modes,
                    locale,
                    pairing,
                    typography,
                ),
                action="create",
            )
        )
        ops.append(
            FileOp(
                path="components.json",
                content=_build_components_json(preset),
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

        # design-system/ is generator-owned; overwrite freely.
        if path.startswith("design-system/"):
            return FileOp(path=path, content=op.content, action="overwrite")

        # Pretendard scaffolding is generator-owned.
        if path.startswith("public/fonts/") or path == "scripts/fetch-pretendard.mjs":
            return FileOp(path=path, content=op.content, action="overwrite")

        if path == "app/globals.css":
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
            updated, _replaced = replace_managed_block(existing, new_body)
            return FileOp(path=path, content=updated, action="merge")

        if path == "tailwind.config.ts":
            if DS_BLOCK_START in existing and DS_BLOCK_END in existing:
                updated, _ = replace_managed_block(
                    existing,
                    op.content.replace(DS_BLOCK_START, "").replace(DS_BLOCK_END, "").strip(),
                )
                return FileOp(path=path, content=updated, action="merge")
            return FileOp(
                path=f"{path}.ds-proposed",
                content=op.content,
                action="proposed",
                reason="existing tailwind.config.ts has no design-ontology managed block",
                original_path=path,
            )

        if path == "components.json":
            try:
                base = json.loads(existing)
                overlay = json.loads(op.content)
            except json.JSONDecodeError as exc:
                return FileOp(
                    path=f"{path}.ds-proposed",
                    content=op.content,
                    action="proposed",
                    reason=f"existing components.json is not valid JSON: {exc.msg}",
                    original_path=path,
                )
            merged, conflicts = deep_merge_json(base, overlay)
            if conflicts:
                return FileOp(
                    path=f"{path}.ds-proposed",
                    content=op.content,
                    action="proposed",
                    reason=f"components.json conflicts at: {', '.join(conflicts)}",
                    original_path=path,
                )
            return FileOp(
                path=path,
                content=json.dumps(merged, ensure_ascii=False, indent=2) + "\n",
                action="merge",
            )

        # Fallback: don't overwrite user files silently.
        return FileOp(
            path=f"{path}.ds-proposed",
            content=op.content,
            action="proposed",
            reason="no merge strategy for this path",
            original_path=path,
        )
