"""Agent-ready style capsules derived from ontology artifacts.

The capsule is intentionally narrower than ``system_spec.md``. It gives coding
agents a short, copyable DESIGN.md-style brief while preserving the harness
authority order: tokens, component specs, product IA, then visual references.
"""

from __future__ import annotations

from typing import Any


STYLE_CAPSULE_VERSION = "1.0.0"


_COLOR_TOKEN_BY_ROLE = {
    "primary": "--ds-color-primary",
    "brand_primary": "--ds-color-primary",
    "accent": "--ds-color-accent",
    "brand_accent": "--ds-color-accent",
    "surface_tint": "--ds-color-surface-tint",
    "canvas": "--ds-color-canvas",
    "surface": "--ds-color-surface",
    "surface_muted": "--ds-color-surface-muted",
    "surface_elevated": "--ds-color-surface-elevated",
    "border": "--ds-color-border",
    "border_strong": "--ds-color-border-strong",
    "ink": "--ds-color-ink",
    "ink_muted": "--ds-color-ink-muted",
    "ink_subtle": "--ds-color-ink-subtle",
    "ink_inverse": "--ds-color-ink-inverse",
    "info": "--ds-color-info",
    "success": "--ds-color-success",
    "warning": "--ds-color-warning",
    "danger": "--ds-color-danger",
    "link": "--ds-color-link",
    "link_hover": "--ds-color-link-hover",
}


_COLOR_ROLE_ORDER = (
    "primary",
    "accent",
    "surface_tint",
    "canvas",
    "surface",
    "surface_muted",
    "surface_elevated",
    "border",
    "border_strong",
    "ink",
    "ink_muted",
    "ink_subtle",
    "info",
    "success",
    "warning",
    "danger",
    "link",
)


_APP_MODE_SIGNATURES: dict[str, tuple[str, ...]] = {
    "dashboard": ("table", "kpi", "sidebar", "filter", "nav", "card"),
    "document-content": ("article", "toc", "reading", "prose", "heading", "footnote"),
    "marketing-landing": ("hero", "pricing", "cta", "testimonial", "feature", "footer"),
    "commerce": ("product", "cart", "checkout", "grid", "detail", "price"),
    "conversation-copilot": (
        "chat",
        "prompt",
        "thread",
        "message",
        "artifact",
        "composer",
        "policy",
        "audit",
        "compliance",
    ),
    "canvas-tool": ("canvas", "layer", "inspector", "toolbar", "panel"),
    "community-feed": ("feed", "thread", "post", "comment", "presence", "notification"),
    "monitoring-ops": ("chart", "alert", "status", "table", "metric", "timeline"),
}


def render_style_markdown(
    *,
    preset_id: str,
    manifest: dict[str, Any] | None = None,
    brand_profile: dict[str, Any] | None = None,
    blueprint: dict[str, Any] | None = None,
    token_schema: dict[str, Any] | None = None,
    component_inventory: dict[str, Any] | None = None,
    component_specs: dict[str, Any] | None = None,
) -> str:
    """Render an agent-friendly Style Capsule markdown document."""

    manifest = manifest or {}
    brand_profile = brand_profile or {}
    blueprint = blueprint or {}
    token_schema = token_schema or {}
    component_inventory = component_inventory or {}
    component_specs = component_specs or {}

    system_name = _first_str(
        manifest.get("name"),
        blueprint.get("system_name"),
        brand_profile.get("system_name"),
        preset_id,
    )
    brand_name = _first_str(
        blueprint.get("brand_name"),
        brand_profile.get("brand_name"),
        system_name,
    )
    app_mode = _first_str(manifest.get("app_mode"), _app_mode_from_id(preset_id), "unknown")
    brand_tone = _first_str(manifest.get("brand_tone"), _brand_tone_from_id(preset_id), "unknown")
    summary = _first_str(
        manifest.get("description"),
        blueprint.get("product_summary"),
        brand_profile.get("product_summary"),
        "",
    )

    lines: list[str] = [
        f"# {system_name} Style Capsule",
        "",
        f"- preset: `{preset_id}`",
        f"- brand: {brand_name}",
        f"- mode: `{app_mode}` / `{brand_tone}`",
        f"- capsule_version: `{STYLE_CAPSULE_VERSION}`",
        "- companion files: `STYLE.md` is the human brief; `DESIGN.md` is the agent-ready copy.",
        "",
    ]
    if summary:
        lines += ["## Taste Summary", _sentence(summary), ""]

    lines.extend(_authority_section())
    lines.extend(_keywords_section(brand_profile=brand_profile, blueprint=blueprint))
    lines.extend(_color_section(blueprint=blueprint, token_schema=token_schema))
    lines.extend(_typography_section(blueprint=blueprint, token_schema=token_schema))
    lines.extend(_spacing_shape_section(token_schema=token_schema))
    lines.extend(
        _component_section(
            component_inventory=component_inventory,
            component_specs=component_specs,
            app_mode=app_mode,
        )
    )
    lines.extend(_reference_governance_section(blueprint=blueprint))
    lines.extend(_agent_preflight_section())
    return "\n".join(lines).rstrip() + "\n"


def _authority_section() -> list[str]:
    return [
        "## Authority Order",
        "1. Product task flow and information architecture",
        "2. `token_schema.json` and generated CSS variables",
        "3. `components/component_specs.*` and `component_inventory.json`",
        "4. `system_spec.md` and `system_ontology.json`",
        "5. External visual references",
        "",
        "Visual references are morphology inputs only. They may inform component shape, density, proportion, hierarchy rhythm, and affordance patterns; they must not override tokens, typography, domain IA, product copy, or palette composition.",
        "",
    ]


def _keywords_section(*, brand_profile: dict[str, Any], blueprint: dict[str, Any]) -> list[str]:
    positioning = blueprint.get("positioning") if isinstance(blueprint.get("positioning"), dict) else {}
    brand_keywords = _list_of_str(
        brand_profile.get("brand_keywords") or positioning.get("brand_keywords")
    )
    anti_keywords = _list_of_str(
        brand_profile.get("anti_keywords") or positioning.get("anti_keywords")
    )
    visual_keywords = _list_of_str(brand_profile.get("visual_keywords"))
    tone = _list_of_str(brand_profile.get("tone_of_voice") or positioning.get("tone_of_voice"))

    lines = ["## Voice And Boundaries"]
    if brand_keywords:
        lines.append(f"- brand keywords: {_inline_list(brand_keywords, 10)}")
    if tone:
        lines.append(f"- tone: {_inline_list(tone, 8)}")
    if visual_keywords:
        lines.append(f"- visual cues: {_inline_list(visual_keywords, 8)}")
    if anti_keywords:
        lines.append(f"- avoid: {_inline_list(anti_keywords, 8)}")
    if len(lines) == 1:
        lines.append("- No brand keyword data found; read `system_spec.md` before implementing.")
    lines.append("")
    return lines


def _color_section(*, blueprint: dict[str, Any], token_schema: dict[str, Any]) -> list[str]:
    rows = _color_rows(blueprint=blueprint, token_schema=token_schema)
    lines = [
        "## Color Roles",
        "| Role | Token | Value | Source | Use |",
        "| --- | --- | --- | --- | --- |",
    ]
    if rows:
        lines.extend(
            f"| `{role}` | `{token}` | `{value}` | {source} | {usage} |"
            for role, token, value, source, usage in rows
        )
    else:
        lines.append("| n/a | n/a | n/a | n/a | Color roles not found. |")
    lines += [
        "",
        "Color rule: Token binding is necessary but not sufficient. Do not recombine `--ds-*` color roles into a new reference-like palette.",
        "",
    ]
    return lines


def _color_rows(
    *, blueprint: dict[str, Any], token_schema: dict[str, Any]
) -> list[tuple[str, str, str, str, str]]:
    color_reference = blueprint.get("color_reference") if isinstance(blueprint.get("color_reference"), dict) else {}
    palette_roles = color_reference.get("palette_roles") if isinstance(color_reference.get("palette_roles"), dict) else {}
    expanded = color_reference.get("expanded_palette") if isinstance(color_reference.get("expanded_palette"), dict) else {}
    semantic_roles = expanded.get("semantic_roles") if isinstance(expanded.get("semantic_roles"), dict) else {}

    token_palette = (
        token_schema.get("categories", {})
        .get("color", {})
        .get("reference_palette", {})
        .get("palette_roles", {})
    )
    if not isinstance(token_palette, dict):
        token_palette = {}

    merged: dict[str, Any] = {}
    for source in (token_palette, semantic_roles, palette_roles):
        if isinstance(source, dict):
            merged.update(source)

    rows: list[tuple[str, str, str, str, str]] = []
    seen: set[str] = set()
    for role in _COLOR_ROLE_ORDER:
        item = merged.get(role) or merged.get(_alternate_role(role))
        if not item:
            continue
        value = _hex_of(item)
        if not value:
            continue
        token = _COLOR_TOKEN_BY_ROLE.get(role, f"--ds-color-{role.replace('_', '-')}")
        source = _first_str(_dict_get(item, "name"), _dict_get(item, "family"), "palette role")
        usage = _short(_first_str(_dict_get(item, "mood"), _dict_get(item, "usage"), "semantic role"), 96)
        rows.append((role, token, value, _escape_pipe(source), _escape_pipe(usage)))
        seen.add(role)

    for role, item in merged.items():
        if len(rows) >= 14:
            break
        if role in seen or role in {"primary_support", "accent_support", "link_hover"}:
            continue
        value = _hex_of(item)
        if not value:
            continue
        token = _COLOR_TOKEN_BY_ROLE.get(role, f"--ds-color-{role.replace('_', '-')}")
        source = _first_str(_dict_get(item, "name"), _dict_get(item, "family"), "palette role")
        usage = _short(_first_str(_dict_get(item, "mood"), _dict_get(item, "usage"), "semantic role"), 96)
        rows.append((role, token, value, _escape_pipe(source), _escape_pipe(usage)))
    return rows


def _alternate_role(role: str) -> str:
    if role == "primary":
        return "brand_primary"
    if role == "accent":
        return "brand_accent"
    return role


def _typography_section(*, blueprint: dict[str, Any], token_schema: dict[str, Any]) -> list[str]:
    font_system = blueprint.get("font_system") if isinstance(blueprint.get("font_system"), dict) else {}
    typography = token_schema.get("categories", {}).get("typography", {})
    if not isinstance(typography, dict):
        typography = {}
    recommended = typography.get("recommended_fonts") if isinstance(typography.get("recommended_fonts"), dict) else {}
    type_scale = typography.get("type_scale") if isinstance(typography.get("type_scale"), dict) else {}
    script_guardrails = typography.get("script_guardrails") if isinstance(typography.get("script_guardrails"), dict) else {}

    heading = _font_name(font_system.get("heading")) or _first_str(recommended.get("heading"), "n/a")
    body = _font_name(font_system.get("body")) or _first_str(recommended.get("body"), "n/a")
    mono = _font_name(font_system.get("mono")) or _first_str(recommended.get("mono"), "n/a")
    korean = _font_name(font_system.get("korean")) or _first_str(recommended.get("korean"), "n/a")
    sizes = type_scale.get("sizes") if isinstance(type_scale.get("sizes"), dict) else {}
    line_heights = type_scale.get("line_heights") if isinstance(type_scale.get("line_heights"), dict) else {}

    lines = [
        "## Typography",
        "| Role | Font | Token | Notes |",
        "| --- | --- | --- | --- |",
        f"| heading | {heading} | `--ds-font-heading` | {_typography_note(font_system.get('heading'), typography.get('heading_note'))} |",
        f"| body | {body} | `--ds-font-body` | {_typography_note(font_system.get('body'), typography.get('body_note'))} |",
        f"| mono | {mono} | `--ds-font-mono` | data, code, shortcuts only |",
        f"| korean | {korean} | `--ds-font-ko` | primary script support |",
        "",
    ]
    if sizes:
        lines.append(f"- type scale: {_inline_kv(sizes, 8)}")
    if line_heights:
        lines.append(f"- line heights: {_inline_kv(line_heights, 6)}")
    if script_guardrails:
        wrap = script_guardrails.get("wrap") if isinstance(script_guardrails.get("wrap"), dict) else {}
        headline = wrap.get("headline") if isinstance(wrap.get("headline"), dict) else {}
        body_wrap = wrap.get("body") if isinstance(wrap.get("body"), dict) else {}
        if headline:
            lines.append(f"- headline wrap: {_inline_kv(headline, 4)}")
        if body_wrap:
            lines.append(f"- body wrap: {_inline_kv(body_wrap, 4)}")
    lines.append("")
    return lines


def _spacing_shape_section(*, token_schema: dict[str, Any]) -> list[str]:
    categories = token_schema.get("categories", {})
    spacing = categories.get("spacing") if isinstance(categories.get("spacing"), dict) else {}
    radius = categories.get("radius") if isinstance(categories.get("radius"), dict) else {}
    spacing_scale = spacing.get("scale") or []
    radius_scale = radius.get("scale") or []
    lines = ["## Spacing And Shape"]
    if spacing_scale:
        lines.append(f"- spacing scale: {_inline_list([str(x) for x in spacing_scale], 12)}")
    if spacing.get("visual_density_bias"):
        lines.append(f"- density bias: `{spacing.get('visual_density_bias')}`")
    if radius_scale:
        lines.append(f"- radius scale: {_inline_list([str(x) for x in radius_scale], 8)}")
    if radius.get("visual_corner_bias"):
        lines.append(f"- corner bias: `{radius.get('visual_corner_bias')}`")
    if len(lines) == 1:
        lines.append("- Spacing/radius categories not found.")
    lines.append("")
    return lines


def _component_section(
    *,
    component_inventory: dict[str, Any],
    component_specs: dict[str, Any],
    app_mode: str,
) -> list[str]:
    lines = ["## Component Priorities"]
    families = _component_family_rows(component_inventory)
    if families:
        lines += [
            "| Family | Priority | States | Components |",
            "| --- | --- | --- | --- |",
            *families,
            "",
        ]
    else:
        lines += ["- Component family data not found.", ""]

    signature = _signature_component_rows(component_specs, app_mode)
    lines.append("## Signature Components")
    if signature:
        lines += [
            "| Component | Family | Anatomy | Token Binding |",
            "| --- | --- | --- | --- |",
            *signature,
            "",
        ]
    else:
        lines += ["- Read `component_inventory.json` before inventing a new component.", ""]
    return lines


def _component_family_rows(component_inventory: dict[str, Any]) -> list[str]:
    families = component_inventory.get("families")
    if not isinstance(families, list):
        return []
    priority_order = {"high": 0, "medium": 1, "low": 2}
    sorted_families = sorted(
        (item for item in families if isinstance(item, dict)),
        key=lambda item: (priority_order.get(str(item.get("priority")), 3), str(item.get("family"))),
    )
    rows: list[str] = []
    for item in sorted_families[:6]:
        family = _escape_pipe(_first_str(item.get("family"), "n/a"))
        priority = _escape_pipe(_first_str(item.get("priority"), "n/a"))
        states = _inline_list(_list_of_str(item.get("required_states")), 5)
        components = _inline_list(_list_of_str(item.get("components")), 6)
        rows.append(f"| {family} | {priority} | {states} | {components} |")
    return rows


def _signature_component_rows(component_specs: dict[str, Any], app_mode: str) -> list[str]:
    specs = component_specs.get("specs")
    if not isinstance(specs, list):
        specs = component_specs.get("components")
    if not isinstance(specs, list):
        return []
    keywords = _APP_MODE_SIGNATURES.get(app_mode, ())
    scored: list[tuple[int, dict[str, Any]]] = []
    for item in specs:
        if not isinstance(item, dict):
            continue
        haystack = " ".join(
            str(item.get(key) or "").lower()
            for key in ("name", "family", "archetype", "role", "supports_primitive")
        )
        score = sum(2 for keyword in keywords if keyword in haystack)
        if item.get("visual_adaptation"):
            score += 1
        if item.get("source_pattern") != "baseline":
            score += 1
        scored.append((score, item))
    scored.sort(key=lambda pair: pair[0], reverse=True)

    rows: list[str] = []
    for score, item in scored[:6]:
        if score <= 0 and rows:
            continue
        name = _escape_pipe(_first_str(item.get("name"), "component"))
        family = _escape_pipe(_first_str(item.get("family"), "n/a"))
        anatomy = _escape_pipe(_format_anatomy(item))
        token_binding = _escape_pipe(_format_token_binding(item))
        rows.append(f"| `{name}` | {family} | {anatomy} | {token_binding} |")
    return rows


def _reference_governance_section(*, blueprint: dict[str, Any]) -> list[str]:
    governance = blueprint.get("governance") if isinstance(blueprint.get("governance"), dict) else {}
    guardrails = _list_of_str(governance.get("implementation_guardrails"))
    scope = governance.get("reference_absorption_scope")
    if not isinstance(scope, dict):
        scope = {}
    allowed = _list_of_str(scope.get("allowed"))
    denied = _list_of_str(scope.get("denied"))
    failure_patterns = scope.get("failure_patterns") if isinstance(scope.get("failure_patterns"), list) else []

    lines = ["## Reference Governance"]
    if allowed:
        lines.append(f"- allowed from references: {_inline_list(allowed, 8)}")
    if denied:
        lines.append(f"- denied from references: {_inline_list(denied, 10)}")
    if guardrails:
        lines.append("- implementation guardrails:")
        for item in guardrails[:6]:
            lines.append(f"  - {_sentence(item)}")
    for pattern in failure_patterns[:2]:
        if not isinstance(pattern, dict):
            continue
        rule = _first_str(pattern.get("rule"), "")
        prevention = _first_str(pattern.get("prevention"), "")
        if rule:
            lines.append(f"- failure pattern `{pattern.get('id', 'unnamed')}`: {_sentence(rule)}")
        if prevention:
            lines.append(f"- prevention: {_sentence(prevention)}")
    if len(lines) == 1:
        lines.append("- No governance block found. Use `IMPLEMENTATION_CONTRACT.md` as the fallback.")
    lines.append("")
    return lines


def _agent_preflight_section() -> list[str]:
    return [
        "## Agent Preflight",
        "1. Read `design-system/IMPLEMENTATION_CONTRACT.md` before UI edits.",
        "2. Read this capsule, then `system_spec.md`, `token_schema.json`, and `components/component_specs.md`.",
        "3. Use external references only for morphology and density. Keep colors, fonts, IA, and copy ontology-led.",
        "4. Run implementation lint before calling the screen complete:",
        "",
        "```bash",
        "uv run design-ontology lint-implementation --target-repo .",
        "```",
        "",
    ]


def _format_anatomy(item: dict[str, Any]) -> str:
    anatomy = item.get("anatomy")
    if isinstance(anatomy, dict):
        parts = _list_of_str(anatomy.get("parts"))
        states = _list_of_str(anatomy.get("states"))
        segments: list[str] = []
        if parts:
            segments.append("parts: " + _plain_inline_list(parts, 5))
        if states:
            segments.append("states: " + _plain_inline_list(states, 5))
        if segments:
            return _short("; ".join(segments), 120)
    role = _first_str(item.get("role"), item.get("archetype"), "anatomy n/a")
    return _short(role, 120)


def _format_token_binding(item: dict[str, Any]) -> str:
    tokens = item.get("tokens")
    if not isinstance(tokens, dict):
        return "read component spec"
    slots = []
    for key in ("surface", "text", "border", "radius", "padding", "font"):
        if tokens.get(key):
            slots.append(key)
    if not slots:
        return "read component spec"
    return "slots: " + _plain_inline_list(slots, 8)


def _typography_note(entry: Any, fallback: Any) -> str:
    note = _dict_get(entry, "note") or fallback
    return _escape_pipe(_short(_first_str(note, "ontology font role"), 100))


def _font_name(entry: Any) -> str:
    if isinstance(entry, dict):
        return _first_str(entry.get("name"), "")
    if isinstance(entry, str):
        return entry
    return ""


def _hex_of(item: Any) -> str:
    if isinstance(item, dict):
        value = item.get("hex") or item.get("value")
        return str(value) if value else ""
    if isinstance(item, str):
        return item
    return ""


def _dict_get(item: Any, key: str) -> Any:
    if isinstance(item, dict):
        return item.get(key)
    return None


def _first_str(*values: Any) -> str:
    for value in values:
        if isinstance(value, str) and value.strip():
            return value.strip()
    return ""


def _list_of_str(value: Any) -> list[str]:
    if not isinstance(value, list):
        return []
    return [str(item).strip() for item in value if str(item).strip()]


def _inline_list(values: list[str], limit: int) -> str:
    sliced = values[:limit]
    rendered = ", ".join(f"`{_escape_backtick(value)}`" for value in sliced)
    if len(values) > limit:
        rendered += f", +{len(values) - limit} more"
    return rendered or "n/a"


def _plain_inline_list(values: list[str], limit: int) -> str:
    sliced = values[:limit]
    rendered = ", ".join(_escape_pipe(value) for value in sliced)
    if len(values) > limit:
        rendered += f", +{len(values) - limit} more"
    return rendered or "n/a"


def _inline_kv(values: dict[str, Any], limit: int) -> str:
    parts = []
    for key, value in list(values.items())[:limit]:
        parts.append(f"`{key}`={value}")
    if len(values) > limit:
        parts.append(f"+{len(values) - limit} more")
    return ", ".join(parts) or "n/a"


def _sentence(value: str) -> str:
    value = " ".join(value.strip().split())
    if not value:
        return ""
    if value.endswith((".", "!", "?")):
        return value
    return value + "."


def _short(value: str, limit: int) -> str:
    text = " ".join(value.strip().split())
    if len(text) <= limit:
        return text
    return text[: max(0, limit - 3)].rstrip() + "..."


def _escape_pipe(value: str) -> str:
    return value.replace("|", "\\|")


def _escape_backtick(value: str) -> str:
    return value.replace("`", "'")


def _app_mode_from_id(preset_id: str) -> str:
    if "--" not in preset_id:
        return ""
    return preset_id.split("--", 1)[0]


def _brand_tone_from_id(preset_id: str) -> str:
    if "--" not in preset_id:
        return ""
    return preset_id.split("--", 1)[1]
