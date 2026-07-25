"""Preset builder — promote a project's build/system output into presets/<id>/.

Produces a content-addressed, version-stamped preset bundle consumable by the
design-ontology plugin. Pair this with preset_validator.py to enforce the
version contract before sync.
"""

from __future__ import annotations

import hashlib
import json
import re
import shutil
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterable

from .style_capsule import render_style_markdown
from .utils import ensure_dir, write_json

REPO_ROOT = Path(__file__).resolve().parent.parent
PRESETS_ROOT = REPO_ROOT / "presets"
MATRIX_PATH = PRESETS_ROOT / "matrix.json"
COMPATIBILITY_PATH = PRESETS_ROOT / "compatibility.json"

APP_MODES = {
    "dashboard", "document-content", "marketing-landing", "commerce",
    "conversation-copilot", "canvas-tool", "community-feed", "monitoring-ops",
}
BRAND_TONES = {
    "minimal-tech", "editorial-warm", "bold-confident", "playful-soft", "corporate-trust",
}
ID_RE = re.compile(r"^([a-z-]+)--([a-z-]+)$")

DEFAULT_SCHEMA_VERSION = "1.0.0"
DEFAULT_PREVIEW_VERSION = "1.0.0"


@dataclass
class BuildRequest:
    project_dir: Path
    preset_id: str
    color_modes: list[str]
    default_color_mode: str
    tags: list[str]
    owner: str
    tier: str
    description: str | None = None
    source_commit: str | None = None
    locale_pairings: dict | None = None
    harness_version: str | None = None


def _parse_preset_id(preset_id: str) -> tuple[str, str]:
    match = ID_RE.match(preset_id)
    if not match:
        raise ValueError(f"Preset id must match '{{app_mode}}--{{brand_tone}}': {preset_id}")
    app_mode, brand_tone = match.group(1), match.group(2)
    if app_mode not in APP_MODES:
        raise ValueError(f"Unknown app_mode '{app_mode}' in preset id '{preset_id}'")
    if brand_tone not in BRAND_TONES:
        raise ValueError(f"Unknown brand_tone '{brand_tone}' in preset id '{preset_id}'")
    return app_mode, brand_tone


def _compatibility() -> dict:
    return json.loads(COMPATIBILITY_PATH.read_text(encoding="utf-8"))


def _detect_harness_version() -> str:
    pyproject = REPO_ROOT / "pyproject.toml"
    if pyproject.exists():
        for line in pyproject.read_text(encoding="utf-8").splitlines():
            stripped = line.strip()
            if stripped.startswith("version"):
                parts = stripped.split("=", 1)
                if len(parts) == 2:
                    return parts[1].strip().strip('"').strip("'")
    return "0.0.0"


def _iter_files(root: Path) -> Iterable[Path]:
    for path in sorted(root.rglob("*")):
        if path.is_file():
            yield path


def _compute_content_hash(preset_dir: Path) -> str:
    hasher = hashlib.sha256()
    for path in _iter_files(preset_dir):
        if path.name == "manifest.json":
            continue
        rel = path.relative_to(preset_dir).as_posix()
        hasher.update(rel.encode("utf-8"))
        hasher.update(b"\0")
        hasher.update(path.read_bytes())
        hasher.update(b"\0")
    return f"sha256:{hasher.hexdigest()}"


def _load_system_spec_excerpt(system_dir: Path) -> dict:
    spec: dict = {}
    blueprint_path = system_dir / "blueprint" / "design_system_blueprint.json"
    if blueprint_path.exists():
        try:
            spec["blueprint"] = json.loads(blueprint_path.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            spec["blueprint"] = {}
    token_schema = system_dir / "token_schema.json"
    if token_schema.exists():
        try:
            spec["tokens"] = json.loads(token_schema.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            spec["tokens"] = {}
    component_specs = system_dir / "components" / "component_specs.json"
    if component_specs.exists():
        try:
            spec["components"] = json.loads(component_specs.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            spec["components"] = {}
    return spec


def _load_json_dict(path: Path) -> dict:
    if not path.exists():
        return {}
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return {}
    return data if isinstance(data, dict) else {}


def _validate_component_contract_source(system_dir: Path) -> dict:
    specs_path = system_dir / "components" / "component_specs.json"
    specs_data = _load_json_dict(specs_path)
    specs = specs_data.get("specs") if isinstance(specs_data, dict) else None
    if not isinstance(specs, list) or not any(
        isinstance(spec, dict) and spec.get("contract_version") == "component-contract/v1"
        for spec in specs
    ):
        return {}

    from .component_contracts import validate_component_contracts

    report = validate_component_contracts(specs_data, strict_authored=True)
    if not report["ok"]:
        raise ValueError(
            "Component contracts are not promotion-ready: "
            + "; ".join(report["errors"][:8])
        )
    return {
        "component_contract_version": "component-contract/v1",
        "component_contract_count": report["component_count"],
        "component_contract_needs_authoring": report["needs_authoring_count"],
    }


def _render_preview_md(
    *,
    preset_id: str,
    app_mode: str,
    brand_tone: str,
    color_modes: list[str],
    description: str,
    spec_excerpt: dict,
    locale_pairings: dict | None,
) -> str:
    blueprint = spec_excerpt.get("blueprint") or {}
    components = spec_excerpt.get("components") or {}

    color_reference = blueprint.get("color_reference") or {}
    palette_roles = color_reference.get("palette_roles") or {}
    expanded = color_reference.get("expanded_palette") or {}
    semantic_roles = expanded.get("semantic_roles") or {}

    def _hex_of(role: dict | str | None) -> str:
        if isinstance(role, dict):
            return role.get("hex") or role.get("value") or ""
        if isinstance(role, str):
            return role
        return ""

    def _core_swatches() -> list[str]:
        order = ("primary", "accent", "surface_tint")
        rows: list[str] = []
        for role in order:
            value = _hex_of(palette_roles.get(role))
            if value:
                rows.append(f"- {role}: `{value}`")
        return rows

    def _semantic_swatches() -> list[str]:
        keys = ("success", "warning", "danger", "info")
        rows: list[str] = []
        for key in keys:
            role = semantic_roles.get(key) or semantic_roles.get(f"{key}_role")
            value = _hex_of(role)
            if value:
                rows.append(f"- {key}: `{value}`")
        return rows

    def _component_rows() -> list[str]:
        specs = components.get("specs") if isinstance(components, dict) else None
        pool = specs if isinstance(specs, list) else (
            components.get("components") if isinstance(components, dict) else None
        )
        if not isinstance(pool, list):
            return []
        signature_keywords = _signature_keywords_for(app_mode)
        scored: list[tuple[int, dict]] = []
        for item in pool:
            if not isinstance(item, dict):
                continue
            name = (item.get("name") or item.get("id") or "").lower()
            archetype = (item.get("archetype") or "").lower()
            role = (item.get("role") or "").lower()
            haystack = " ".join([name, archetype, role])
            score = sum(1 for kw in signature_keywords if kw in haystack)
            scored.append((score, item))
        scored.sort(key=lambda pair: pair[0], reverse=True)
        rows: list[str] = []
        for _, item in scored[:3]:
            name = item.get("name") or item.get("id") or "component"
            rows.append(f"- **{name}** — {_format_anatomy(item)}")
        return rows

    font_system = blueprint.get("font_system") or {}

    def _font_name(key: str) -> str:
        value = font_system.get(key)
        if isinstance(value, dict):
            return value.get("name") or "n/a"
        return str(value) if value else "n/a"

    lines = [f"# {preset_id}", ""]
    if description:
        lines += ["## 어떤 제품에 맞나", f"- {description}", ""]
    lines += [f"- app_mode: `{app_mode}` / brand_tone: `{brand_tone}`", ""]

    core = _core_swatches()
    semantic = _semantic_swatches()
    mode_label = " + ".join(color_modes) if color_modes else "light"
    if core or semantic:
        lines += [f"## Color Tokens ({mode_label})"]
        if core:
            lines += ["### Core", *core]
        if semantic:
            lines += ["", "### Semantic", *semantic]
        adapter_note = (
            "> light/dark 변형은 어댑터(`nextjs-tailwind-shadcn` 등)가 파생. 원본 팔레트는 위 HEX 1세트."
            if "dark" in color_modes
            else "> 추가 color mode 변형은 어댑터(`nextjs-tailwind-shadcn` 등)가 파생. 원본 팔레트는 위 HEX 1세트."
        )
        lines += ["", adapter_note, ""]
    else:
        lines += [
            f"## Color Tokens ({mode_label})",
            "- (color_reference 미설정 — brand_profile.color_reference를 채우면 자동 추출)",
            "",
        ]

    heading = _font_name("heading")
    body = _font_name("body")
    mono = _font_name("mono")
    korean = _font_name("korean")
    if heading != "n/a" or body != "n/a":
        lines += [
            "## Typography",
            f"- heading: {heading}",
            f"- body: {body}",
            f"- mono: {mono}",
            f"- korean: {korean}",
            "",
        ]
    else:
        lines += ["## Typography", "- (font_system 미해석 — brand_profile 확인 필요)", ""]

    component_rows = _component_rows()
    if component_rows:
        lines += ["## 대표 컴포넌트", *component_rows, ""]
    else:
        lines += ["## 대표 컴포넌트", "- (component_specs.json 비어있음)", ""]

    if locale_pairings:
        lines.append("## Locale Pairings")
        for locale, pairing in locale_pairings.items():
            lines.append(
                f"- {locale}: heading={pairing.get('heading_font', 'n/a')} / body={pairing.get('body_font', 'n/a')}"
            )
        lines.append("")

    lines += [
        "## 주의사항",
        "- image-derived hints는 advisory (truth source: system_spec.md, token_schema.json)",
        "- 이 프리셋과 맞지 않으면 `brand_tone` 축을 바꿔 재시도",
        "",
    ]
    return "\n".join(lines)


_APP_MODE_SIGNATURES: dict[str, tuple[str, ...]] = {
    "dashboard": ("table", "kpi", "sidebar", "filter", "nav", "card"),
    "document-content": ("article", "toc", "reading", "prose", "heading", "footnote"),
    "marketing-landing": ("hero", "pricing", "cta", "testimonial", "feature", "footer"),
    "commerce": ("product", "cart", "checkout", "grid", "detail", "price"),
    "conversation-copilot": ("chat", "prompt", "thread", "message", "artifact", "composer"),
    "canvas-tool": ("canvas", "layer", "inspector", "toolbar", "panel"),
    "community-feed": ("feed", "thread", "post", "comment", "presence", "notification"),
    "monitoring-ops": ("chart", "alert", "status", "table", "metric", "timeline"),
}


def _signature_keywords_for(app_mode: str) -> tuple[str, ...]:
    return _APP_MODE_SIGNATURES.get(app_mode, ())


def _format_anatomy(item: dict) -> str:
    anatomy = item.get("anatomy")
    if isinstance(anatomy, dict):
        parts = anatomy.get("parts") or []
        states = anatomy.get("states") or []
        segments: list[str] = []
        if parts:
            segments.append("parts: " + ", ".join(str(p) for p in parts[:5]))
        if states:
            segments.append("states: " + ", ".join(str(s) for s in states[:4]))
        if segments:
            return " | ".join(segments)[:160]
    if isinstance(anatomy, list):
        return ", ".join(str(x) for x in anatomy[:4])[:160]
    if isinstance(anatomy, str) and anatomy.strip():
        return anatomy.strip().replace("\n", " ")[:160]
    role = item.get("role") or item.get("archetype") or ""
    return str(role)[:160] if role else "(anatomy n/a)"


def build_preset(request: BuildRequest) -> dict:
    app_mode, brand_tone = _parse_preset_id(request.preset_id)

    if request.default_color_mode not in request.color_modes:
        raise ValueError(
            f"default_color_mode '{request.default_color_mode}' must be one of color_modes {request.color_modes}"
        )
    for mode in request.color_modes:
        if mode not in {"light", "dark"}:
            raise ValueError(f"color_modes must be subset of {{light, dark}}, got {mode}")
    if request.tier not in {"P0", "P1", "P2", "P3"}:
        raise ValueError(f"tier must be one of P0/P1/P2/P3, got {request.tier}")

    project_dir = request.project_dir.resolve()
    system_dir = project_dir / "build" / "system"
    if not system_dir.exists():
        raise FileNotFoundError(
            f"build/system/ not found in {project_dir}. Run `design-ontology run-project` first."
        )
    component_contract_metadata = _validate_component_contract_source(system_dir)

    compat = _compatibility()
    preset_api_version = compat["current_preset_api_version"]
    adapter_ranges = {}
    for entry in compat["entries"]:
        if entry["preset_api_version"] == preset_api_version:
            adapter_ranges = entry["adapter_ranges"]
            break
    if not adapter_ranges:
        raise RuntimeError(
            f"compatibility.json has no entry for current_preset_api_version={preset_api_version}"
        )

    preset_dir = PRESETS_ROOT / request.preset_id
    if preset_dir.exists():
        shutil.rmtree(preset_dir)
    ensure_dir(preset_dir)

    for name in ("blueprint", "components", "ontology", "css_extraction"):
        src = system_dir / name
        if src.exists():
            shutil.copytree(src, preset_dir / name)

    for filename in ("system_spec.md", "token_schema.json", "system_ontology.json", "component_inventory.json"):
        for candidate in (system_dir / filename, system_dir / "blueprint" / filename):
            if candidate.exists():
                shutil.copy2(candidate, preset_dir / filename)
                break

    bp_source = project_dir / "brand_profile.json"
    if bp_source.exists():
        shutil.copy2(bp_source, preset_dir / "brand_profile.json")

    preview_md = _render_preview_md(
        preset_id=request.preset_id,
        app_mode=app_mode,
        brand_tone=brand_tone,
        color_modes=request.color_modes,
        description=request.description or "",
        spec_excerpt=_load_system_spec_excerpt(preset_dir),
        locale_pairings=request.locale_pairings,
    )
    (preset_dir / "preview.md").write_text(preview_md, encoding="utf-8")

    style_manifest = {
        "id": request.preset_id,
        "app_mode": app_mode,
        "brand_tone": brand_tone,
        "color_modes": request.color_modes,
        "default_color_mode": request.default_color_mode,
        "description": request.description or "",
        "locale_pairings": request.locale_pairings or {},
        "owner": request.owner,
        "tier": request.tier,
    }
    style_excerpt = _load_system_spec_excerpt(preset_dir)
    style_md = render_style_markdown(
        preset_id=request.preset_id,
        manifest=style_manifest,
        brand_profile=_load_json_dict(preset_dir / "brand_profile.json"),
        blueprint=style_excerpt.get("blueprint") or {},
        token_schema=style_excerpt.get("tokens") or {},
        component_inventory=_load_json_dict(preset_dir / "component_inventory.json"),
        component_specs=style_excerpt.get("components") or {},
    )
    (preset_dir / "STYLE.md").write_text(style_md, encoding="utf-8")
    (preset_dir / "DESIGN.md").write_text(style_md, encoding="utf-8")

    content_hash = _compute_content_hash(preset_dir)

    manifest = {
        "id": request.preset_id,
        "schema_version": DEFAULT_SCHEMA_VERSION,
        "preset_api_version": preset_api_version,
        "generated_by_harness_version": request.harness_version or _detect_harness_version(),
        "preview_version": DEFAULT_PREVIEW_VERSION,
        "adapter_compatibility": dict(adapter_ranges),
        "source_project": project_dir.name,
        "content_hash": content_hash,
        "app_mode": app_mode,
        "brand_tone": brand_tone,
        "color_modes": request.color_modes,
        "default_color_mode": request.default_color_mode,
        "tags": list(request.tags),
        "locale_pairings": request.locale_pairings or {},
        "owner": request.owner,
        "tier": request.tier,
        "generated_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        **component_contract_metadata,
    }
    if request.description:
        manifest["description"] = request.description
    if request.source_commit:
        manifest["source_commit"] = request.source_commit

    write_json(preset_dir / "manifest.json", manifest)
    _upsert_matrix_entry(manifest)
    return manifest


def _upsert_matrix_entry(manifest: dict) -> None:
    matrix = json.loads(MATRIX_PATH.read_text(encoding="utf-8"))
    entry = {
        "id": manifest["id"],
        "app_mode": manifest["app_mode"],
        "brand_tone": manifest["brand_tone"],
        "color_modes": manifest["color_modes"],
        "default_color_mode": manifest["default_color_mode"],
        "tags": manifest["tags"],
        "description": manifest.get("description") or f"{manifest['app_mode']} / {manifest['brand_tone']} preset",
        "source_project": manifest["source_project"],
        "owner": manifest["owner"],
        "preview_path": f"presets/{manifest['id']}/preview.md",
        "locale_pairings": manifest.get("locale_pairings") or {},
        "tier": manifest["tier"],
    }
    presets = matrix.get("presets", [])
    idx = next((i for i, p in enumerate(presets) if p["id"] == manifest["id"]), None)
    if idx is None:
        presets.append(entry)
    else:
        presets[idx] = entry
    presets.sort(key=lambda p: p["id"])
    matrix["presets"] = presets
    write_json(MATRIX_PATH, matrix)
