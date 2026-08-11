"""Project-local design token emission.

``run-project`` already produces a diverse, per-project palette and font
system inside ``build/system/blueprint``, but mockup implementations kept
ignoring those artifacts and re-inventing colors and fonts by hand — which is
exactly where the repeated default aesthetic came from.

``emit_project_tokens`` closes that gap: it renders the blueprint's active
palette, semantic roles, font system, radius, and spacing scale into
``<project>/design-system/tokens.css`` as ``--ds-*`` CSS variables. The
mockup HTML links this file and consumes only ``var(--ds-*)`` values, so
``lint-implementation`` can enforce the binding.
"""

from __future__ import annotations

import json
import re
from pathlib import Path

from .adapters.base import (
    DS_BLOCK_END,
    DS_BLOCK_START,
    PresetBundle,
    _ensure_base_roles,
    _extract_semantic_roles,
    apply_light_contrast_floor,
    css_var_declarations,
    derive_dark_tokens,
)
from .font_reference import webfont_recipe
from .implementation_linter import (
    BODY_LINE_HEIGHT_FLOOR,
    BODY_LINE_HEIGHT_FLOOR_HANGUL,
)
from .semantic_color_markdown import (
    load_runtime_color_policy,
    payload_sha256,
    runtime_role_values,
)

SANS_FALLBACK = 'system-ui, -apple-system, "Segoe UI", sans-serif'
SERIF_FALLBACK = 'ui-serif, Georgia, serif'
MONO_FALLBACK = 'ui-monospace, SFMono-Regular, Menlo, monospace'

_RADIUS_BY_BIAS = {
    "low": {"sm": 2, "md": 4, "lg": 8, "xl": 12},
    "medium": {"sm": 4, "md": 8, "lg": 12, "xl": 16},
    "high": {"sm": 6, "md": 10, "lg": 16, "xl": 24},
}


def _slug(value: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-")


def _number(value: float) -> str:
    return f"{value:g}"


def _range_low(value: object) -> float | None:
    """`"1.6-1.7"` 같은 범위 문자열에서 하한을 읽는다."""
    if isinstance(value, bool):
        return None
    if isinstance(value, (int, float)):
        return float(value)
    if not isinstance(value, str):
        return None
    match = re.search(r"-?\d+(?:\.\d+)?", value)
    return float(match.group(0)) if match else None


def _korean_body_tracking(value: object) -> str:
    """한글 본문 자간. 양수는 어절 덩어리를 풀어버리므로 0으로 막는다."""
    amount = _range_low(value)
    if amount is None or amount > 0:
        return "0em"
    return f"{_number(amount)}em"


def reading_rhythm_declarations(
    font_system: dict,
    *,
    korean_locale: bool = False,
) -> list[str]:
    """본문 조판 기본값.

    행간 하한은 `lint-implementation`의 DS100과 같은 상수를 쓴다. 생성기가 게이트보다
    낮은 값을 내보내면 자기 산출물이 자기 린트에 걸린다. 한글 프로젝트는 서체별
    `script_guardrails`에서 행간·자간·줄바꿈 계약을 그대로 가져온다.

    `korean_locale`은 preset 설치처럼 로케일이 명시된 경로용이다. preset bundle의
    `font_system`에는 `needs_korean`이 없어서, 한글 프로젝트인데도 줄바꿈 계약이
    빠진 토큰이 나가는 일이 생긴다.
    """
    type_scale = font_system.get("type_scale") or {}
    line_heights = type_scale.get("line_heights") or {}
    guardrails = font_system.get("script_guardrails") or {}
    korean = korean_locale or (bool(font_system.get("needs_korean")) and bool(guardrails))
    body_font = guardrails.get("body_font") or {}

    if korean:
        floor = BODY_LINE_HEIGHT_FLOOR_HANGUL
        authored = _range_low(body_font.get("line_height"))
    else:
        floor = BODY_LINE_HEIGHT_FLOOR
        authored = _range_low(line_heights.get("normal"))
    body_leading = max(authored or 0.0, floor)

    lines = [
        f"  --ds-leading-tight: {line_heights.get('tight', 1.2)};",
        f"  --ds-leading-body: {_number(body_leading)};",
        f"  --ds-leading-relaxed: {line_heights.get('relaxed', 1.65)};",
    ]
    if not korean:
        lines.append("  --ds-tracking-body: normal;")
        return lines

    wrap = (guardrails.get("wrap") or {}).get("body") or {}
    lines.append(f"  --ds-tracking-body: {_korean_body_tracking(body_font.get('letter_spacing'))};")
    lines.append(f"  --ds-wrap-word-break: {wrap.get('word_break', 'keep-all')};")
    lines.append(f"  --ds-wrap-overflow: {wrap.get('overflow_wrap', 'normal')};")
    return lines


def _first_family(stack: str | None) -> str | None:
    """폰트 스택의 첫 서체 이름. 그게 의도한 서체다."""
    if not stack:
        return None
    first = stack.split(",")[0].strip().strip("\"'").strip()
    return first or None


def build_fonts_css(font_system: dict, project: str) -> tuple[str, list[str]]:
    """프로젝트가 실제로 쓰는 서체의 로딩을 방출한다.

    확인된 self-host 경로가 있으면 `@font-face`로 자체 호스팅하고, Google Fonts는
    `@import`로 받는다. 배포 경로를 확인하지 못한 서체는 주석으로 표시만 남기고
    추측 URL을 넣지 않는다. `lint-implementation`의 DS108이 그 표시를 잡는다.

    반환값의 두 번째 항목은 수동 설정이 필요한 서체 목록이다.
    """
    slots = ("display", "heading", "body", "korean", "mono")
    families: list[str] = []
    for slot in slots:
        entry = font_system.get(slot)
        name = entry.get("name") if isinstance(entry, dict) else None
        if name and name not in families:
            families.append(name)

    fetchable: list[dict] = []
    manual: list[str] = []
    for name in families:
        recipe = webfont_recipe(name)
        if recipe is None or recipe["kind"] == "generic":
            continue
        if recipe["kind"] == "manual":
            manual.append(name)
        else:
            fetchable.append(recipe)

    lines = [
        f"/* project: {project} — generated by design-ontology emit-tokens */",
        "/* 서체 로딩. 토큰이 선언한 서체가 실제로 렌더되도록 보장하는 파일입니다. */",
        "/* tokens.css 다음에 링크하세요. */",
        "",
    ]
    if fetchable:
        lines.extend([
            "/* 웹폰트는 자체 호스팅합니다. 원격 참조가 남으면 오프라인에서 렌더되지 않고",
            "   production 증거의 content tree도 검증할 수 없습니다.",
            "",
            "   내려받기:  node design-system/fonts/fetch-webfonts.mjs",
            "",
            "   스크립트가 제공자 CSS에서 woff2 URL을 해석해 fonts/ 에 저장하고",
            "   unicode-range 서브셋까지 보존한 fonts/local.css 를 만듭니다.",
            "   local.css 가 없으면 아무 서체도 로드되지 않습니다(DS108). */",
            '@import url("./fonts/local.css");',
            "",
            "/* 대상 서체 */",
        ])
        for recipe in fetchable:
            lines.append(f'/* - "{recipe["family"]}" ({recipe["kind"]}) */')
        lines.append("")
    if manual:
        lines.append(
            "/* 수동 설정 필요: 배포 경로가 확인되지 않은 서체입니다. "
            "@font-face를 직접 추가하거나 로드 가능한 서체로 교체하세요. */"
        )
        for name in manual:
            recipe = webfont_recipe(name) or {}
            lines.append(f'/* ds-font-manual: "{name}" (source: {recipe.get("source")}) */')
        lines.append("")
    if not fetchable and not manual:
        lines.append("/* 시스템 서체만 사용하므로 로딩이 필요하지 않습니다. */")
        lines.append("")

    body = "\n".join(lines).rstrip() + "\n"
    return f"{DS_BLOCK_START}\n{body}{DS_BLOCK_END}\n", manual


_FETCH_WEBFONTS_SCRIPT = '''// 웹폰트를 자체 호스팅으로 내려받습니다. 폰트 바이너리와 local.css 는 커밋하지 않습니다.
// 사용: node design-system/fonts/fetch-webfonts.mjs
//
// woff2 URL을 하드코딩하지 않습니다. 제공자 CSS를 받아서 그 안의 실제 URL을 해석하고,
// unicode-range 서브셋 구조를 그대로 보존한 채 로컬 경로로 다시 씁니다. 서브셋을
// 임의로 줄이면 한글 커버리지가 깨집니다.
import { readFile, writeFile } from "node:fs/promises";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const here = dirname(fileURLToPath(import.meta.url));
// woff2를 받기 위해 필요합니다. 구형 UA로 요청하면 제공자가 ttf를 내려줍니다.
const USER_AGENT =
  "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 " +
  "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36";

const manifest = JSON.parse(await readFile(join(here, "webfont-manifest.json"), "utf8"));

async function get(url, asText) {
  const response = await fetch(url, { headers: { "User-Agent": USER_AGENT } });
  if (!response.ok) {
    throw new Error(`${url}: ${response.status} ${response.statusText}`);
  }
  return asText ? response.text() : Buffer.from(await response.arrayBuffer());
}

function localName(family, absoluteUrl) {
  const slug = family.toLowerCase().replace(/[^a-z0-9]+/g, "-").replace(/^-|-$/g, "");
  const base = new URL(absoluteUrl).pathname.split("/").pop();
  return `${slug}__${base}`;
}

const blocks = [];
let files = 0;

for (const entry of manifest.families) {
  if (entry.woff2_url) {
    const file = localName(entry.family, entry.woff2_url);
    await writeFile(join(here, file), await get(entry.woff2_url, false));
    files += 1;
    blocks.push(
      `/* ${entry.family} — ${entry.woff2_url} */\\n` +
        "@font-face {\\n" +
        `  font-family: "${entry.family}";\\n` +
        "  font-style: normal;\\n" +
        `  font-weight: ${entry.weight_range ?? "400 700"};\\n` +
        "  font-display: swap;\\n" +
        `  src: url("./${file}") format("woff2-variations");\\n` +
        "}",
    );
    continue;
  }

  const css = await get(entry.css_url, true);
  const rewrites = new Map();
  for (const match of css.matchAll(/url\\((['"]?)([^'")]+\\.woff2[^'")]*)\\1\\)/gi)) {
    const raw = match[2];
    if (rewrites.has(raw)) continue;
    rewrites.set(raw, localName(entry.family, new URL(raw, entry.css_url).href));
  }
  if (rewrites.size === 0) {
    throw new Error(`${entry.family}: ${entry.css_url} 에서 woff2 URL을 찾지 못했습니다`);
  }
  for (const [raw, file] of rewrites) {
    await writeFile(join(here, file), await get(new URL(raw, entry.css_url).href, false));
    files += 1;
  }
  let rewritten = css;
  for (const [raw, file] of rewrites) {
    rewritten = rewritten.split(raw).join(`./${file}`);
  }
  blocks.push(`/* ${entry.family} — ${entry.css_url} */\\n${rewritten.trim()}`);
  console.log(`${entry.family}: ${rewrites.size} woff2`);
}

const header =
  "/* design-system/fonts/fetch-webfonts.mjs 가 생성한 파일입니다. 커밋하지 않습니다. */\\n" +
  "/* 제공자 CSS를 미러링했습니다. 다시 만들려면 스크립트를 실행하세요. */\\n";
await writeFile(join(here, "local.css"), `${header}\\n${blocks.join("\\n\\n")}\\n`);
console.log(`local.css 생성 — 서체 ${manifest.families.length}종, 파일 ${files}개`);
'''


def _fetch_webfonts_script() -> str:
    return _FETCH_WEBFONTS_SCRIPT


def _read_json(path: Path) -> dict:
    if not path.exists():
        return {}
    return json.loads(path.read_text(encoding="utf-8"))


def _hex_saturation_lightness(value: str) -> tuple[float, float]:
    import colorsys

    raw = value.lstrip("#")
    r, g, b = (int(raw[i : i + 2], 16) / 255.0 for i in (0, 2, 4))
    _, lightness, saturation = colorsys.rgb_to_hls(r, g, b)
    return saturation, lightness


def _brand_role_overrides(active_roles: dict) -> dict[str, str]:
    """Derive primary/accent/canvas/border from project palette role names.

    Project blueprints often name roles by product meaning (anchor_surface,
    fresh_accent, quiet_background) instead of the standard semantic keys, so
    without this the emitted --ds-color-primary falls back to a generic blue
    that no blueprint actually chose.
    """

    named: dict[str, str] = {}
    colored: list[tuple[str, str, float, float]] = []
    for role, entry in active_roles.items():
        hex_value = entry.get("hex") if isinstance(entry, dict) else entry
        if not (isinstance(hex_value, str) and hex_value.startswith("#") and len(hex_value) == 7):
            continue
        saturation, lightness = _hex_saturation_lightness(hex_value)
        colored.append((role.lower(), hex_value.upper(), saturation, lightness))

    # achromatic-photographic chrome strategy: role names are exact
    chrome_map = {
        "chrome_ink": ("ink", "primary", "link"),
        "chrome_paper": ("surface", "surface-elevated"),
        "chrome_canvas": ("canvas",),
        "chrome_line": ("border",),
        "chrome_muted": ("ink-muted",),
        "restrained_accent": ("accent",),
    }
    if any(role in chrome_map for role, *_ in colored):
        for role, hex_value, _, _ in colored:
            for token in chrome_map.get(role, ()):
                named.setdefault(token, hex_value)
        return named

    for role, hex_value, _, lightness in colored:
        if "primary" in role or "anchor" in role:
            named.setdefault("primary", hex_value)
        elif "accent" in role:
            named.setdefault("accent", hex_value)
        elif "background" in role or "canvas" in role:
            if lightness >= 0.6:
                named.setdefault("canvas", hex_value)
        elif "border" in role:
            named.setdefault("border", hex_value)

    saturated = sorted(
        (item for item in colored if item[2] >= 0.15 and 0.12 <= item[3] <= 0.8),
        key=lambda item: item[2],
        reverse=True,
    )
    for _, hex_value, _, _ in saturated:
        if "primary" not in named:
            named["primary"] = hex_value
        elif "accent" not in named and hex_value != named["primary"]:
            named["accent"] = hex_value
    if "primary" in named:
        named.setdefault("link", named["primary"])
    return named


def _font_stack(entry: dict | None, *, fallback: str) -> str | None:
    if not isinstance(entry, dict):
        return None
    name = entry.get("name")
    if not name:
        return None
    family = (entry.get("family") or "").lower()
    chain = SERIF_FALLBACK if "serif" in family and "sans" not in family else fallback
    return f'"{name}", {chain}'


def emit_project_tokens(
    project_dir: Path,
    *,
    output_path: Path | None = None,
) -> Path:
    project_dir = project_dir.resolve()
    blueprint_dir = project_dir / "build" / "system" / "blueprint"
    blueprint = _read_json(blueprint_dir / "design_system_blueprint.json")
    token_schema = _read_json(blueprint_dir / "token_schema.json")
    brand_profile = _read_json(project_dir / "brand_profile.json")
    if not blueprint and not token_schema:
        raise FileNotFoundError(
            f"No blueprint artifacts under {blueprint_dir}. Run "
            "`design-ontology run-project --project-dir ...` first."
        )

    bundle = PresetBundle(
        preset_dir=project_dir,
        manifest={"id": project_dir.name},
        blueprint=blueprint,
        token_schema=token_schema,
        component_specs={},
        brand_profile=brand_profile,
    )
    categories_early = token_schema.get("categories") or {}
    active_roles_early = (
        ((categories_early.get("color") or {}).get("reference_palette") or {})
        .get("active_palette", {})
        .get("roles")
        or {}
    )
    semantic_tokens = _extract_semantic_roles(bundle)
    chrome_active = any(str(role).startswith("chrome_") for role in active_roles_early)
    for role, hex_value in _brand_role_overrides(active_roles_early).items():
        if chrome_active:
            # chrome strategy는 팔레트 파이프라인의 최종 결정 — 구 semantic role을 덮는다
            semantic_tokens[role] = hex_value
        else:
            semantic_tokens.setdefault(role, hex_value)
    if chrome_active:
        # 무채색 크롬에서 파생되는 나머지 역할도 정렬
        runtime_defaults = runtime_role_values()
        ink = semantic_tokens.get("ink", runtime_defaults["ink"])
        semantic_tokens.setdefault(
            "ink-subtle", semantic_tokens.get("ink-muted", runtime_defaults["ink-subtle"])
        )
        semantic_tokens["ink-inverse"] = runtime_defaults["ink-inverse"]
        semantic_tokens["surface-elevated"] = semantic_tokens.get(
            "surface", runtime_defaults["surface-elevated"]
        )
        semantic_tokens["surface-muted"] = runtime_defaults["surface-muted"]
        semantic_tokens["surface-tint"] = runtime_defaults["surface-tint"]
        semantic_tokens["border-strong"] = runtime_defaults["border-strong"]
        semantic_tokens["link"] = ink
    semantic_tokens = apply_light_contrast_floor(_ensure_base_roles(semantic_tokens))
    color_reference = bundle.blueprint.get("color_reference") or {}
    explicit_dark = (
        (color_reference.get("expanded_palette") or {}).get("dark_semantic_roles")
    ) or {}
    dark_semantic_tokens = derive_dark_tokens(
        semantic_tokens,
        explicit_dark=explicit_dark,
    )
    runtime_policy = load_runtime_color_policy()

    lines: list[str] = []
    lines.append(f"/* project: {project_dir.name} — generated by design-ontology emit-tokens */")
    lines.append("/* 이 파일이 색/서체/라운딩의 단일 진실 소스입니다. 구현 CSS는 var(--ds-*)만 사용하세요. */")
    lines.append(
        "/* runtime-color-policy: "
        f"{runtime_policy['schema_version']} sha256={payload_sha256(runtime_policy)} */"
    )
    lines.append("")
    lines.append(":root {")
    lines.append("  color-scheme: light;")
    lines.append("")

    lines.append("  /* semantic roles */")
    lines.extend(css_var_declarations(semantic_tokens))

    categories = token_schema.get("categories") or {}
    reference_palette = (
        (categories.get("color") or {}).get("reference_palette") or {}
    )
    active_roles = (reference_palette.get("active_palette") or {}).get("roles") or {}
    if active_roles:
        lines.append("")
        lines.append("  /* project palette roles (blueprint active palette) */")
        for role, entry in sorted(active_roles.items()):
            hex_value = entry.get("hex") if isinstance(entry, dict) else entry
            if isinstance(hex_value, str) and hex_value.startswith("#"):
                lines.append(f"  --ds-color-brand-{_slug(role)}: {hex_value.upper()};")

    supporting = (
        (reference_palette.get("expanded_palette") or {}).get("supporting_colors") or []
    )
    if supporting:
        lines.append("")
        lines.append("  /* supporting colors */")
        for entry in supporting[:10]:
            name = entry.get("name")
            hex_value = entry.get("hex")
            if name and isinstance(hex_value, str) and hex_value.startswith("#"):
                lines.append(f"  --ds-color-support-{_slug(name)}: {hex_value.upper()};")

    font_system = blueprint.get("font_system") or {}
    heading_stack = _font_stack(font_system.get("heading"), fallback=SANS_FALLBACK)
    display_stack = _font_stack(font_system.get("display"), fallback=SERIF_FALLBACK)
    body_stack = _font_stack(font_system.get("body"), fallback=SANS_FALLBACK)
    korean_stack = _font_stack(font_system.get("korean"), fallback=SANS_FALLBACK)
    mono_stack = _font_stack(font_system.get("mono"), fallback=MONO_FALLBACK)
    lines.append("")
    lines.append("  /* typography (blueprint font_system) */")
    lines.append(f"  --ds-font-display: {display_stack or heading_stack or SERIF_FALLBACK};")
    lines.append(f"  --ds-font-heading: {heading_stack or body_stack or SANS_FALLBACK};")
    lines.append(f"  --ds-font-body: {body_stack or SANS_FALLBACK};")
    lines.append(f"  --ds-font-ko: {korean_stack or body_stack or SANS_FALLBACK};")
    lines.append(f"  --ds-font-mono: {mono_stack or MONO_FALLBACK};")
    default_type_sizes = {
        "xs": "0.75rem",
        "sm": "0.875rem",
        "md": "1rem",
        "lg": "1.125rem",
        "2xl": "1.5rem",
        "3xl": "1.875rem",
        "4xl": "2.25rem",
    }
    type_scale = font_system.get("type_scale") or {}
    authored_sizes = type_scale.get("sizes") or {}
    lines.append("  /* type scale */")
    for key, fallback in default_type_sizes.items():
        value = authored_sizes.get(key, fallback)
        css_value = f"{value}px" if isinstance(value, (int, float)) else str(value)
        lines.append(f"  --ds-text-{key}: {css_value};")
    lines.append("  /* reading rhythm */")
    lines.extend(reading_rhythm_declarations(font_system))

    radius = categories.get("radius") or {}
    bias = radius.get("visual_corner_bias") or "medium"
    radius_map = _RADIUS_BY_BIAS.get(bias, _RADIUS_BY_BIAS["medium"])
    lines.append("")
    lines.append(f"  /* radius (corner bias: {bias}) */")
    lines.append("  --ds-radius-none: 0;")
    for key, value in radius_map.items():
        lines.append(f"  --ds-radius-{key}: {value}px;")
    lines.append("  --ds-radius-pill: 999px;")

    spacing_scale = (categories.get("spacing") or {}).get("scale") or []
    if spacing_scale:
        lines.append("")
        lines.append("  /* spacing scale */")
        for index, value in enumerate(spacing_scale):
            lines.append(f"  --ds-space-{index}: {value}px;")
    lines.append("")
    lines.append("  /* pixel-addressable component spacing aliases */")
    spacing_aliases = {4, 8, 12, 16, 20, 24, 32, 48, 64, 96}
    spacing_aliases.update(
        int(value)
        for value in spacing_scale
        if isinstance(value, (int, float)) and float(value).is_integer()
    )
    for value in sorted(spacing_aliases):
        lines.append(f"  --ds-space-px-{value}: {value}px;")

    lines.extend([
        "",
        "  /* component motion contract */",
        "  --ds-duration-120: 120ms;",
        "  --ds-duration-180: 180ms;",
        "  --ds-ease-standard: cubic-bezier(0.2, 0, 0, 1);",
        "  --ds-elevation-lg: 0 18px 48px color-mix(in srgb, var(--ds-color-ink) 16%, transparent);",
    ])

    lines.append("}")
    lines.append("")
    lines.append('html[data-theme="dark"] {')
    lines.append("  color-scheme: dark;")
    lines.append("")
    lines.append("  /* semantic roles derived by the typed runtime color policy */")
    lines.extend(css_var_declarations(dark_semantic_tokens))
    lines.append("}")

    body = "\n".join(lines)
    content = f"{DS_BLOCK_START}\n{body}\n{DS_BLOCK_END}\n"

    target = output_path or (project_dir / "design-system" / "tokens.css")
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(content, encoding="utf-8")

    if output_path is None:
        _emit_font_loading(target.parent, font_system, project_dir.name)
    return target


def _emit_font_loading(artifact_dir: Path, font_system: dict, project: str) -> None:
    """`fonts.css`와 self-host fetch 스크립트를 방출한다.

    토큰이 선언한 서체가 로드되지 않으면 화면은 조용히 system-ui로 떨어지고 서체
    결정이 무효가 된다. `fonts.css`가 그 로딩을 담당한다.
    """
    fonts_css, _manual = build_fonts_css(font_system, project)
    (artifact_dir / "fonts.css").write_text(fonts_css, encoding="utf-8")

    recipes: dict[str, dict] = {}
    for slot in ("display", "heading", "body", "korean", "mono"):
        entry = font_system.get(slot)
        name = entry.get("name") if isinstance(entry, dict) else None
        recipe = webfont_recipe(name) if name else None
        if recipe and recipe["kind"] not in ("generic", "manual"):
            recipes.setdefault(recipe["family"], recipe)

    fonts_dir = artifact_dir / "fonts"
    script_path = fonts_dir / "fetch-webfonts.mjs"
    manifest_path = fonts_dir / "webfont-manifest.json"
    if not recipes:
        for stale in (script_path, manifest_path):
            if stale.exists():
                stale.unlink()
        return

    fonts_dir.mkdir(parents=True, exist_ok=True)
    manifest = {
        "kind": "design-ontology.webfont-manifest.v1",
        "project": project,
        "families": [
            {
                key: value
                for key, value in recipe.items()
                if key in ("family", "kind", "source", "css_url", "woff2_url", "weight_range")
            }
            for recipe in recipes.values()
        ],
    }
    manifest_path.write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    script_path.write_text(_fetch_webfonts_script(), encoding="utf-8")
