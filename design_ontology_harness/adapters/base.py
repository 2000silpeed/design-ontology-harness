"""StackAdapter base — common contract + helpers for all stack adapters.

Contract (PLUGIN_PLAN §7.2):

    class StackAdapter(ABC):
        id: str
        version: str
        supported_preset_api: str
        def detect(self, target_repo: Path) -> float
        def render(self, preset: PresetBundle, target: Path,
                   color_mode: str, locale: str = "en") -> list[FileOp]
        def merge(self, op: FileOp, existing: Path) -> FileOp

Helpers:
- PresetBundle: loaded manifest + blueprint + token_schema + component_specs.
- tokens_for_mode(): semantic role → hex for light OR dark. For presets without
  explicit dark palette, derives a deterministic dark variant via HSL.
- font_face_block(): @font-face CSS snippet for a locale's Pretendard pairing.
"""

from __future__ import annotations

import colorsys
import json
import re
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Literal

FileAction = Literal["create", "overwrite", "merge", "proposed", "skip"]


@dataclass
class FileOp:
    """A single file write targeting a repo-relative path.

    When merge() falls back, the path is rewritten to `<path>.ds-proposed` and
    reason is populated so the caller can surface it.
    """

    path: str
    content: str
    action: FileAction = "create"
    reason: str | None = None
    original_path: str | None = None
    binary: bool = False


@dataclass
class ApplyReport:
    created: list[str] = field(default_factory=list)
    overwritten: list[str] = field(default_factory=list)
    merged: list[str] = field(default_factory=list)
    proposed: list[tuple[str, str]] = field(default_factory=list)
    skipped: list[str] = field(default_factory=list)


@dataclass
class PresetBundle:
    preset_dir: Path
    manifest: dict
    blueprint: dict
    token_schema: dict
    component_specs: dict
    brand_profile: dict

    @property
    def id(self) -> str:
        return self.manifest["id"]

    @property
    def color_modes(self) -> list[str]:
        return list(self.manifest.get("color_modes") or [])

    @property
    def default_color_mode(self) -> str:
        return self.manifest.get("default_color_mode") or "light"

    @property
    def locale_pairings(self) -> dict:
        return self.manifest.get("locale_pairings") or {}

    @property
    def font_system(self) -> dict:
        return self.blueprint.get("font_system") or {}


def _read_json(path: Path) -> dict:
    if not path.exists():
        return {}
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return {}


def load_preset_bundle(preset_dir: Path) -> PresetBundle:
    manifest = _read_json(preset_dir / "manifest.json")
    if not manifest:
        raise FileNotFoundError(f"manifest.json missing or invalid: {preset_dir}")
    blueprint = _read_json(preset_dir / "blueprint" / "design_system_blueprint.json")
    token_schema = _read_json(preset_dir / "token_schema.json")
    component_specs = _read_json(preset_dir / "components" / "component_specs.json")
    brand_profile = _read_json(preset_dir / "brand_profile.json")
    return PresetBundle(
        preset_dir=preset_dir,
        manifest=manifest,
        blueprint=blueprint,
        token_schema=token_schema,
        component_specs=component_specs,
        brand_profile=brand_profile,
    )


_SEMANTIC_ROLE_MAP: dict[str, str] = {
    "brand_primary": "primary",
    "brand_accent": "accent",
    "surface_tint": "surface-tint",
    "canvas": "canvas",
    "surface": "surface",
    "surface_muted": "surface-muted",
    "surface_elevated": "surface-elevated",
    "border": "border",
    "border_strong": "border-strong",
    "ink": "ink",
    "ink_muted": "ink-muted",
    "ink_subtle": "ink-subtle",
    "ink_inverse": "ink-inverse",
    "info": "info",
    "success": "success",
    "warning": "warning",
    "danger": "danger",
    "link": "link",
    "link_hover": "link-hover",
}


_HEX_RE = re.compile(r"^#?[0-9a-fA-F]{6}$")


def _parse_hex(value: str) -> tuple[float, float, float] | None:
    if not isinstance(value, str):
        return None
    match = _HEX_RE.match(value.strip())
    if not match:
        return None
    raw = value.strip().lstrip("#")
    r = int(raw[0:2], 16) / 255.0
    g = int(raw[2:4], 16) / 255.0
    b = int(raw[4:6], 16) / 255.0
    return r, g, b


def _to_hex(rgb: tuple[float, float, float]) -> str:
    r, g, b = rgb
    return "#" + "".join(
        f"{int(round(max(0.0, min(1.0, c)) * 255)):02X}" for c in (r, g, b)
    )


# Lightness targets for dark-mode derivation per semantic role family.
_DARK_L_TARGETS: dict[str, float] = {
    "canvas": 0.06,
    "surface": 0.09,
    "surface-muted": 0.13,
    "surface-elevated": 0.11,
    "surface-tint": 0.22,
    "border": 0.20,
    "border-strong": 0.28,
    "ink": 0.94,
    "ink-muted": 0.72,
    "ink-subtle": 0.56,
    "ink-inverse": 0.10,
}


def _hsl_from_rgb(r: float, g: float, b: float) -> tuple[float, float, float]:
    hue, lightness, saturation = colorsys.rgb_to_hls(r, g, b)
    return hue, saturation, lightness


def _rgb_from_hsl(h: float, s: float, lightness: float) -> tuple[float, float, float]:
    return colorsys.hls_to_rgb(h, lightness, s)


def _derive_dark(role: str, light_hex: str) -> str:
    """Derive a dark-mode swatch from a light-mode hex using HSL targets.

    For surface/ink family roles we pin lightness; for chromatic roles (primary,
    accent, feedback) we nudge saturation/lightness toward a dark-bg-friendly
    value while preserving hue.
    """

    parsed = _parse_hex(light_hex)
    if parsed is None:
        return light_hex
    r, g, b = parsed
    h, s, lightness = _hsl_from_rgb(r, g, b)

    target_l = _DARK_L_TARGETS.get(role)
    if target_l is not None:
        # Pull saturation down slightly for surface/ink neutrals.
        neutral_s = min(s, 0.12)
        return _to_hex(_rgb_from_hsl(h, neutral_s, target_l))

    # Chromatic roles (primary/accent/info/success/warning/danger/link): keep
    # hue, raise lightness a touch so they pop on a dark canvas, cap saturation.
    new_l = max(0.42, min(0.72, lightness + 0.18))
    new_s = min(1.0, max(s, 0.45))
    return _to_hex(_rgb_from_hsl(h, new_s, new_l))


def _extract_semantic_roles(bundle: PresetBundle) -> dict[str, str]:
    """Collect semantic role → hex from blueprint.color_reference.

    Fallback chain: expanded_palette.semantic_roles → palette_roles → empty.
    """

    reference = (bundle.blueprint.get("color_reference") or {})
    expanded = reference.get("expanded_palette") or {}
    semantic = expanded.get("semantic_roles") or {}
    palette_roles = reference.get("palette_roles") or {}

    out: dict[str, str] = {}
    for source_key, token_key in _SEMANTIC_ROLE_MAP.items():
        entry = semantic.get(source_key)
        hex_value: str | None = None
        if isinstance(entry, dict):
            hex_value = entry.get("hex") or entry.get("value")
        elif isinstance(entry, str):
            hex_value = entry
        if not hex_value:
            # palette_roles fallback (only defines primary/accent/surface_tint)
            pr_key = {
                "brand_primary": "primary",
                "brand_accent": "accent",
                "surface_tint": "surface_tint",
            }.get(source_key)
            if pr_key and isinstance(palette_roles.get(pr_key), dict):
                hex_value = palette_roles[pr_key].get("hex")
        if hex_value and _parse_hex(hex_value):
            out[token_key] = hex_value.upper() if hex_value.startswith("#") else f"#{hex_value.upper()}"
    return out


def _ensure_base_roles(tokens: dict[str, str]) -> dict[str, str]:
    """Backfill roles commonly required by shadcn with sensible defaults.

    Only fills gaps; never overrides values already present.
    """

    defaults_light = {
        "primary": "#2563EB",
        "accent": "#F59E0B",
        "surface-tint": "#E0E7FF",
        "canvas": "#F7F8FA",
        "surface": "#FFFFFF",
        "surface-muted": "#EEF1F6",
        "surface-elevated": "#FFFFFF",
        "border": "#D6DDE6",
        "border-strong": "#9AA6B2",
        "ink": "#0F172A",
        "ink-muted": "#475569",
        "ink-subtle": "#64748B",
        "ink-inverse": "#FFFFFF",
        "info": "#2F6FEB",
        "success": "#15803D",
        "warning": "#B45309",
        "danger": "#B91C1C",
        "link": tokens.get("primary", "#2563EB"),
    }
    out = dict(tokens)
    for role, default in defaults_light.items():
        out.setdefault(role, default)
    return out


def tokens_for_mode(bundle: PresetBundle, color_mode: str) -> dict[str, str]:
    """Return {token-name: #HEX} for the requested color mode.

    Token names are the CSS-var suffix (e.g. "primary", "surface-muted"), not
    full variable names. Caller wraps with the `--ds-color-` prefix.
    """

    if color_mode not in ("light", "dark"):
        raise ValueError(f"color_mode must be 'light' or 'dark', got {color_mode}")

    light_tokens = _ensure_base_roles(_extract_semantic_roles(bundle))
    if color_mode == "light":
        return light_tokens

    # Look for an explicit dark palette hook on the blueprint first.
    explicit_dark = (
        bundle.blueprint.get("color_reference", {})
        .get("expanded_palette", {})
        .get("dark_semantic_roles")
    ) or {}
    derived: dict[str, str] = {}
    for role, value in light_tokens.items():
        if role in explicit_dark and isinstance(explicit_dark[role], dict):
            override = explicit_dark[role].get("hex")
            if override and _parse_hex(override):
                derived[role] = override.upper()
                continue
        derived[role] = _derive_dark(role, value)
    return derived


def css_var_declarations(tokens: dict[str, str], prefix: str = "--ds-color-") -> list[str]:
    """Render `  --ds-color-foo: #FFF;` lines, sorted for stable output."""

    return [f"  {prefix}{role}: {value};" for role, value in sorted(tokens.items())]


# ---------------------------------------------------------------------------
# Font pairing / locale


@dataclass
class LocalePairing:
    locale: str
    heading_font: str
    body_font: str
    mono_font: str | None = None
    notes: str | None = None


def resolve_locale_pairing(bundle: PresetBundle, locale: str) -> LocalePairing | None:
    entry = bundle.locale_pairings.get(locale)
    if not isinstance(entry, dict):
        return None
    heading = entry.get("heading_font")
    body = entry.get("body_font")
    if not heading or not body:
        return None
    return LocalePairing(
        locale=locale,
        heading_font=heading,
        body_font=body,
        mono_font=entry.get("mono_font"),
        notes=entry.get("notes"),
    )


# ---------------------------------------------------------------------------
# Adapter ABC


class StackAdapter(ABC):
    """Abstract base for all stack adapters.

    Subclasses must set class attributes `id`, `version`, `supported_preset_api`
    and implement `detect()`, `render()`, `merge()`.
    """

    id: str = ""
    version: str = "0.0.0"
    supported_preset_api: str = ">=1.0.0 <2.0.0"

    @abstractmethod
    def detect(self, target_repo: Path) -> float:
        """Return a score in [0, 1] describing how well target_repo fits."""

    @abstractmethod
    def render(
        self,
        preset: PresetBundle,
        target_repo: Path,
        color_mode: str,
        locale: str = "en",
    ) -> list[FileOp]:
        """Produce the list of FileOps for a given preset/mode/locale."""

    @abstractmethod
    def merge(self, op: FileOp, existing_path: Path) -> FileOp:
        """Reconcile a FileOp with an existing file.

        Return a new FileOp: either action='overwrite' with merged content, or
        action='proposed' with `path` suffixed with `.ds-proposed` and `reason`
        populated. Never mutate user code silently.
        """

    def apply(
        self,
        target_repo: Path,
        ops: list[FileOp],
    ) -> ApplyReport:
        """Write ops to disk, invoking merge() for pre-existing paths."""

        report = ApplyReport()
        target_repo = target_repo.resolve()
        target_repo.mkdir(parents=True, exist_ok=True)

        for op in ops:
            dest = target_repo / op.path
            dest_parent = dest.parent

            if op.action == "skip":
                report.skipped.append(op.path)
                continue

            if dest.exists() and op.action == "create":
                op = self.merge(op, dest)

            if op.action == "proposed":
                dest = target_repo / op.path
                dest.parent.mkdir(parents=True, exist_ok=True)
                _write(dest, op)
                report.proposed.append((op.path, op.reason or "conflict"))
                continue

            dest_parent.mkdir(parents=True, exist_ok=True)
            _write(dest, op)
            if op.action == "overwrite":
                report.overwritten.append(op.path)
            elif op.action == "merge":
                report.merged.append(op.path)
            else:
                report.created.append(op.path)

        return report


def _write(dest: Path, op: FileOp) -> None:
    if op.binary:
        dest.write_bytes(op.content.encode("latin-1") if isinstance(op.content, str) else op.content)
        return
    dest.write_text(op.content, encoding="utf-8")


# ---------------------------------------------------------------------------
# Managed-block helpers (shared across adapters)


DS_BLOCK_START = "/* design-ontology:START */"
DS_BLOCK_END = "/* design-ontology:END */"


def wrap_managed_css(body: str) -> str:
    """Wrap a CSS fragment with managed markers for idempotent re-runs."""

    body = body.strip()
    return f"{DS_BLOCK_START}\n{body}\n{DS_BLOCK_END}\n"


def replace_managed_block(existing: str, new_body: str) -> tuple[str, bool]:
    """Swap an existing DS managed block, or append one. Returns (text, merged).

    `merged=True` iff the marker block was found and replaced in place.
    """

    start_idx = existing.find(DS_BLOCK_START)
    end_idx = existing.find(DS_BLOCK_END)
    if start_idx != -1 and end_idx != -1 and end_idx > start_idx:
        before = existing[:start_idx].rstrip() + ("\n\n" if existing[:start_idx].strip() else "")
        after = existing[end_idx + len(DS_BLOCK_END):].lstrip("\n")
        return before + wrap_managed_css(new_body) + after, True
    glue = "\n\n" if existing.strip() else ""
    return existing + glue + wrap_managed_css(new_body), False


# ---------------------------------------------------------------------------
# Shared: copy preset artifacts into design-system/ (generator-owned mirror)


_DS_COPY_FILES = (
    "manifest.json",
    "system_spec.md",
    "token_schema.json",
    "system_ontology.json",
    "component_inventory.json",
    "preview.md",
    "STYLE.md",
    "DESIGN.md",
    "brand_profile.json",
)

_DS_COPY_DIRS = ("blueprint", "components", "ontology")


def implementation_contract(bundle: PresetBundle) -> str:
    """Human + agent contract for applying references without overriding tokens.

    This file is intentionally installed into every target repo. It turns the
    ontology's advisory reference language into an implementation-time checklist
    that Codex/Claude/humans can read before editing real UI files.
    """

    system_name = (
        bundle.manifest.get("name")
        or bundle.blueprint.get("system_name")
        or bundle.id
    )
    return f"""# Implementation Contract

Preset: `{bundle.id}`
System: {system_name}

## Authority Order

1. Existing product task flow and information architecture
2. `design-system/token_schema.json`
3. `design-system/tokens.css` or host adapter token variables
4. `design-system/components/component_specs.*`
5. `design-system/system_spec.md`
6. `design-system/STYLE.md` or `design-system/DESIGN.md` as a derived quick brief
7. External visual references

The style capsule is a derived summary and never overrides the source artifacts.
External references never outrank product IA, tokens, component specs, or semantic
state rules.

## Reference Absorption Scope

Allowed from visual references:

- component morphology
- layout density
- panel/card proportions
- hierarchy rhythm
- interaction affordance patterns

Denied from visual references:

- color palette
- palette composition or derived secondary palettes
- typography family or scale
- semantic status colors
- product copy
- product data model
- navigation labels
- domain information architecture
- redistributable imagery unless explicitly licensed

## Token Binding Rules

- Use `var(--ds-color-*)` for color, surface, border, and feedback states.
- Use `var(--ds-font-*)` for explicit font-family declarations.
- Use `var(--ds-radius-*)` for component radii; only fully circular affordances may use `999px`.
- Do not hard-code hex/rgb/hsl colors in implementation files outside generated managed blocks.
- Do not add reference-derived local palette variables such as teal/gold/slate unless they alias `--ds-*` tokens.
- Token binding is necessary but not sufficient: do not recombine `--ds-*` color roles into a new reference-like palette.
- Derived colors may alias one semantic token or mix one semantic role with a neutral surface/transparent value; do not mix multiple chromatic roles for local palette variables.

## Feedback Promotion Rule

If implementation review or user feedback exposes a repeatable design-system failure,
promote it into ontology governance, this contract, and `lint-implementation` before
calling the current screen complete. Current-screen fixes alone are not enough.

## Preflight

Run this before considering an implementation aligned:

```bash
uv run design-ontology lint-implementation --target-repo .
```
"""


def design_system_mirror_ops(bundle: PresetBundle) -> list[FileOp]:
    """FileOps that mirror the preset's raw artifacts into `design-system/`.

    Shared across adapters so every target repo gets the same bundle layout for
    downstream agent-pack skills (design-system-architect, etc.).
    """

    ops: list[FileOp] = []
    ops.append(
        FileOp(
            path="design-system/IMPLEMENTATION_CONTRACT.md",
            content=implementation_contract(bundle),
            action="create",
        )
    )
    for name in _DS_COPY_FILES:
        src = bundle.preset_dir / name
        if not src.exists():
            continue
        ops.append(
            FileOp(
                path=f"design-system/{name}",
                content=src.read_text(encoding="utf-8"),
                action="create",
            )
        )
    for dirname in _DS_COPY_DIRS:
        src_dir = bundle.preset_dir / dirname
        if not src_dir.is_dir():
            continue
        for child in sorted(src_dir.rglob("*")):
            if not child.is_file():
                continue
            rel = child.relative_to(bundle.preset_dir)
            ops.append(
                FileOp(
                    path=f"design-system/{rel.as_posix()}",
                    content=child.read_text(encoding="utf-8", errors="replace"),
                    action="create",
                )
            )
    return ops


# ---------------------------------------------------------------------------
# Shared typography + tailwind builders (used by Next and Vite adapters)


@dataclass
class TypographyPlan:
    font_heading: str
    font_body: str
    font_mono: str
    heading_stack: str
    body_stack: str
    mono_stack: str


def _pick_family(font_entry: object) -> str | None:
    if isinstance(font_entry, dict):
        name = font_entry.get("name")
        if isinstance(name, str) and name.strip():
            return name.strip()
        return None
    if isinstance(font_entry, str) and font_entry.strip():
        return font_entry.strip()
    return None


def typography_plan(bundle: PresetBundle, pairing: LocalePairing | None) -> TypographyPlan:
    font_system = bundle.font_system
    heading = _pick_family(font_system.get("heading")) or "Inter"
    body = _pick_family(font_system.get("body")) or heading
    mono = _pick_family(font_system.get("mono")) or "JetBrains Mono"

    if pairing:
        heading = pairing.heading_font or heading
        body = pairing.body_font or body
        if pairing.mono_font:
            mono = pairing.mono_font

    def _stack(primary: str, fallback_sans: bool = True) -> str:
        cleaned = primary.strip()
        quoted = f'"{cleaned}"' if " " in cleaned else cleaned
        tail = (
            'ui-sans-serif, system-ui, -apple-system, "Segoe UI", sans-serif'
            if fallback_sans
            else "ui-monospace, SFMono-Regular, Menlo, monospace"
        )
        return f"{quoted}, {tail}"

    return TypographyPlan(
        font_heading=heading,
        font_body=body,
        font_mono=mono,
        heading_stack=_stack(heading),
        body_stack=_stack(body),
        mono_stack=_stack(mono, fallback_sans=False),
    )


def radius_scale(bundle: PresetBundle) -> dict[str, str]:
    schema = (bundle.token_schema.get("categories") or {}).get("radius") or {}
    scale = schema.get("scale") or []
    bias = (schema.get("visual_corner_bias") or "medium").lower()
    tight = {"none": "0px", "sm": "2px", "md": "4px", "lg": "8px", "xl": "12px", "pill": "999px"}
    medium = {"none": "0px", "sm": "4px", "md": "8px", "lg": "12px", "xl": "20px", "pill": "999px"}
    generous = {"none": "0px", "sm": "6px", "md": "12px", "lg": "20px", "xl": "28px", "pill": "999px"}
    table = {"tight": tight, "medium": medium, "generous": generous}.get(bias, medium)
    return {name: table.get(name, "0px") for name in (scale or list(medium.keys()))}


def spacing_scale(bundle: PresetBundle) -> dict[str, str]:
    schema = (bundle.token_schema.get("categories") or {}).get("spacing") or {}
    scale = schema.get("scale") or [0, 2, 4, 8, 12, 16, 24, 32, 48, 64, 96]
    return {f"ds-{value}": f"{value}px" for value in scale}


def type_scale(bundle: PresetBundle) -> dict[str, str]:
    schema = (bundle.token_schema.get("categories") or {}).get("typography") or {}
    ts = schema.get("type_scale") or {}
    sizes = ts.get("sizes") or {}
    return {
        name: f"{int(round(float(val)))}px"
        for name, val in sizes.items()
        if isinstance(val, (int, float))
    }


def build_tailwind_config_body(
    bundle: PresetBundle,
    *,
    color_modes: list[str],
    typography: TypographyPlan,
    content_paths: list[str],
    adapter_id: str,
    adapter_version: str,
) -> str:
    """Render tailwind.config.ts wrapped in the DS managed block.

    `content_paths` is the list of glob strings that each adapter's host layout
    needs (Next: ./app/**, Vite: ./index.html + ./src/**). Everything else —
    darkMode, theme.extend colors/fonts/radius/spacing/fontSize — is identical.
    """

    radius = radius_scale(bundle)
    spacing = spacing_scale(bundle)
    t_scale = type_scale(bundle)

    dark_mode_clause = (
        'darkMode: ["class", "[data-theme=\'dark\']"],'
        if "dark" in color_modes
        else 'darkMode: "class",'
    )

    color_roles = sorted(tokens_for_mode(bundle, "light").keys())
    tw_color_entries = ",\n".join(
        f'        "{role}": "var(--ds-color-{role})"' for role in color_roles
    )

    radius_entries = ",\n".join(f'        "{k}": "{v}"' for k, v in radius.items())
    spacing_entries = ",\n".join(f'        "{k}": "{v}"' for k, v in spacing.items())
    type_entries = (
        ",\n".join(f'        "{k}": "{v}"' for k, v in t_scale.items())
        if t_scale
        else ""
    )
    extra_fontSize = (
        f"      fontSize: {{\n{type_entries}\n      }},"
        if type_entries
        else ""
    )

    content_lines = ",\n".join(f'    "{p}"' for p in content_paths)

    body = (
        f"// preset: {bundle.id}\n"
        f"// adapter: {adapter_id}@{adapter_version}\n"
        'import type { Config } from "tailwindcss";\n'
        "\n"
        "const config: Config = {\n"
        "  content: [\n"
        f"{content_lines},\n"
        "  ],\n"
        f"  {dark_mode_clause}\n"
        "  theme: {\n"
        "    extend: {\n"
        "      colors: {\n"
        "        ds: {\n"
        f"{tw_color_entries}\n"
        "        },\n"
        '        "primary": "var(--ds-color-primary)",\n'
        '        "accent": "var(--ds-color-accent)",\n'
        '        "background": "var(--ds-color-canvas)",\n'
        '        "foreground": "var(--ds-color-ink)",\n'
        '        "border": "var(--ds-color-border)",\n'
        "      },\n"
        "      fontFamily: {\n"
        '        "heading": ["var(--ds-font-heading)"],\n'
        '        "sans": ["var(--ds-font-body)"],\n'
        '        "mono": ["var(--ds-font-mono)"],\n'
        "      },\n"
        "      borderRadius: {\n"
        f"{radius_entries}\n"
        "      },\n"
        "      spacing: {\n"
        f"{spacing_entries}\n"
        "      },\n"
        f"{extra_fontSize}\n"
        "    },\n"
        "  },\n"
        "  plugins: [],\n"
        "};\n"
        "\n"
        "export default config;\n"
    )
    return f"{DS_BLOCK_START}\n{body}{DS_BLOCK_END}\n"


# ---------------------------------------------------------------------------
# Shared Pretendard scaffolding (ko locale) — target paths are parameterised
# so Next/Vite (public/fonts/) and Raw (design-system/fonts/) share the code.


def _pretendard_placeholder(fetch_script_path: str) -> str:
    return (
        "# Pretendard Variable placeholder\n"
        f"# Run `node {fetch_script_path}` to populate this file.\n"
        "# The woff2 binary itself is NOT committed to the harness/plugin repo\n"
        "# to respect distribution preferences; it is fetched at install-time\n"
        "# under SIL Open Font License 1.1.\n"
    )


def _pretendard_license(fetch_script_path: str) -> str:
    return (
        "# Bundled Fonts — License Notices\n"
        "\n"
        "## Pretendard Variable (SIL Open Font License 1.1)\n"
        "\n"
        "- Source: https://github.com/orioncactus/pretendard\n"
        "- License: SIL OFL 1.1\n"
        "  (see https://scripts.sil.org/OFL)\n"
        f"- Redistribution is permitted under OFL. The woff2 binary is fetched at\n"
        f"  install-time by `{fetch_script_path}`; it is not committed to the\n"
        "  harness or plugin repositories.\n"
        "- The reserved font name \"Pretendard\" must not be removed or renamed in\n"
        "  derivatives. Modified glyph files must use a different family name.\n"
        "- **재배포 시 이 고지를 유지해야 합니다.** When redistributing the\n"
        "  bundle (or a derivative product), this notice and the OFL text must\n"
        "  travel with the font assets — removing it violates OFL §2.\n"
    )


def _pretendard_fetch_script(woff2_target: str, license_path: str) -> str:
    return (
        "#!/usr/bin/env node\n"
        "// fetch-pretendard.mjs — download Pretendard Variable (SIL OFL 1.1) on-demand.\n"
        "//\n"
        "// OFL permits redistribution, but we prefer to pull from upstream at\n"
        "// install-time so users always get the latest glyphs and license notices.\n"
        "\n"
        'import { mkdirSync, writeFileSync, existsSync } from "node:fs";\n'
        'import { join, dirname } from "node:path";\n'
        "\n"
        f'const TARGET = "{woff2_target}";\n'
        "const URL =\n"
        '  "https://cdn.jsdelivr.net/gh/orioncactus/pretendard@v1.3.9/packages/pretendard/dist/web/variable/woff2/PretendardVariable.woff2";\n'
        "\n"
        "async function main() {\n"
        "  const outPath = join(process.cwd(), TARGET);\n"
        "  mkdirSync(dirname(outPath), { recursive: true });\n"
        "\n"
        '  if (existsSync(outPath) && !process.argv.includes("--force")) {\n'
        "    console.log(`[pretendard] already present: ${TARGET}`);\n"
        "    return;\n"
        "  }\n"
        "\n"
        "  console.log(`[pretendard] fetching ${URL}`);\n"
        "  const res = await fetch(URL);\n"
        "  if (!res.ok) {\n"
        "    throw new Error(`fetch failed: ${res.status} ${res.statusText}`);\n"
        "  }\n"
        "  const buf = Buffer.from(await res.arrayBuffer());\n"
        "  writeFileSync(outPath, buf);\n"
        "  console.log(`[pretendard] wrote ${buf.byteLength} bytes → ${TARGET}`);\n"
        f'  console.log("[pretendard] see {license_path} for SIL OFL 1.1 notice.");\n'
        "}\n"
        "\n"
        "main().catch((err) => {\n"
        "  console.error(err);\n"
        "  process.exit(1);\n"
        "});\n"
    )


def pretendard_font_face_block(woff2_url_path: str = "/fonts/PretendardVariable.woff2") -> str:
    """CSS `@font-face` snippet for the Pretendard Variable pairing.

    `woff2_url_path` is the URL the CSS references. For Next/Vite (public/fonts
    served at site root) the default "/fonts/..." is correct. Raw-css adapter
    uses a relative path and builds its own block.
    """

    return (
        "@font-face {\n"
        '  font-family: "Pretendard Variable";\n'
        "  font-style: normal;\n"
        "  font-weight: 45 920;\n"
        "  font-display: swap;\n"
        f'  src: url("{woff2_url_path}") format("woff2-variations");\n'
        "}\n"
        "\n"
        ":root {\n"
        '  --ds-font-ko: "Pretendard Variable", "Pretendard", system-ui, -apple-system, sans-serif;\n'
        "}\n"
        "\n"
        "html[lang='ko'], [data-locale='ko'] {\n"
        "  font-family: var(--ds-font-ko);\n"
        "}"
    )


def pretendard_asset_ops(
    *,
    assets_dir: str,
    fetch_script_path: str,
) -> list[FileOp]:
    """FileOps for Pretendard placeholder + LICENSE-FONTS + fetch script.

    `assets_dir` (no trailing slash) is where the placeholder and LICENSE-FONTS
    live (e.g. "public/fonts" or "design-system/fonts"). `fetch_script_path` is
    the repo-relative path of the fetch script (Next uses "scripts/...", Raw
    keeps it next to the assets).
    """

    woff2_target = f"{assets_dir}/PretendardVariable.woff2"
    license_path = f"{assets_dir}/LICENSE-FONTS"
    return [
        FileOp(
            path=f"{assets_dir}/PretendardVariable.placeholder",
            content=_pretendard_placeholder(fetch_script_path),
            action="create",
        ),
        FileOp(
            path=license_path,
            content=_pretendard_license(fetch_script_path),
            action="create",
        ),
        FileOp(
            path=fetch_script_path,
            content=_pretendard_fetch_script(woff2_target, license_path),
            action="create",
        ),
    ]


# ---------------------------------------------------------------------------
# Deep-merge helper


def deep_merge_json(base: dict, overlay: dict) -> tuple[dict, list[str]]:
    """Deep-merge overlay into base. Returns (merged, conflicts).

    Conflict = scalar-vs-scalar disagreement on the same leaf key. We prefer
    the *existing* base value and record the conflict; arrays use overlay (not
    concatenated) to keep outputs deterministic.
    """

    conflicts: list[str] = []

    def _merge(a: Any, b: Any, path: str) -> Any:
        if isinstance(a, dict) and isinstance(b, dict):
            out = dict(a)
            for key, value in b.items():
                if key in out:
                    out[key] = _merge(out[key], value, f"{path}.{key}" if path else key)
                else:
                    out[key] = value
            return out
        if isinstance(a, list) and isinstance(b, list):
            return list(b)
        if a == b:
            return a
        conflicts.append(path or "<root>")
        return a

    merged = _merge(base, overlay, "")
    return merged, conflicts
