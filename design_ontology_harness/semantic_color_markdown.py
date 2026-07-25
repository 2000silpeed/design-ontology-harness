from __future__ import annotations

import hashlib
import json
import re
from copy import deepcopy
from functools import lru_cache
from importlib.resources import files
from pathlib import Path
from typing import Any


COLOR_HEX_RE = re.compile(r"#(?:[0-9A-Fa-f]{6}|[0-9A-Fa-f]{3})")
BEGIN_RE = re.compile(
    r"<!-- semantic-os-color-ontology:begin sha256=(?P<sha>[0-9a-f]{64}) -->"
)
ONTOLOGY_BEGIN_PREFIX = "<!-- semantic-os-color-ontology:begin"
END_MARKER = "<!-- semantic-os-color-ontology:end -->"
ONTOLOGY_FENCE_PREFIX = "```semantic-color-ontology+json"
FENCED_PAYLOAD_RE = re.compile(
    r"```semantic-color-ontology\+json\s*\n(?P<payload>.*?)\n```",
    re.DOTALL,
)
CATALOG_BEGIN_RE = re.compile(
    r"<!-- semantic-os-color-catalog:begin sha256=(?P<sha>[0-9a-f]{64}) -->"
)
CATALOG_BEGIN_PREFIX = "<!-- semantic-os-color-catalog:begin"
CATALOG_END_MARKER = "<!-- semantic-os-color-catalog:end -->"
RUNTIME_POLICY_BEGIN_RE = re.compile(
    r"<!-- design-ontology-runtime-color-policy:begin sha256=(?P<sha>[0-9a-f]{64}) -->"
)
RUNTIME_POLICY_BEGIN_PREFIX = "<!-- design-ontology-runtime-color-policy:begin"
RUNTIME_POLICY_END_MARKER = "<!-- design-ontology-runtime-color-policy:end -->"
RUNTIME_POLICY_FENCE_PREFIX = "```design-ontology-runtime-color-policy+json"
RUNTIME_POLICY_PAYLOAD_RE = re.compile(
    r"```design-ontology-runtime-color-policy\+json\s*\n(?P<payload>.*?)\n```",
    re.DOTALL,
)

REPO_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_COLOR_REFERENCE_PATH = REPO_ROOT / "docs" / "color-reference.md"
DEFAULT_ONTOLOGY_SNAPSHOT_PATH = (
    REPO_ROOT / "design_ontology_harness" / "resources" / "semantic_color_ontology.json"
)
DEFAULT_SEMANTIC_OS_SOURCE = (
    Path.home()
    / "ai-projects"
    / "semantic-os"
    / "domains"
    / "color"
    / "ontology"
    / "build"
    / "graph.json"
)

DROPPED_PROPERTY_KEYS = {"source_path", "source_file", "local_path"}


class SemanticColorMarkdownError(ValueError):
    """Raised when the embedded Semantic OS snapshot is missing or corrupt."""


LOCAL_EXTENSION_REFERENCE_ID = "ref-docs-color-reference-local-extensions"


def canonical_json_bytes(value: Any) -> bytes:
    return json.dumps(
        value,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")


def payload_sha256(payload: dict[str, Any]) -> str:
    return hashlib.sha256(canonical_json_bytes(payload)).hexdigest()


def _strip_local_paths(value: Any) -> Any:
    if isinstance(value, str):
        if value.startswith("/Users/") or value.startswith("/home/"):
            return Path(value).name
        return value
    if isinstance(value, list):
        return [_strip_local_paths(item) for item in value]
    if isinstance(value, dict):
        return {
            key: _strip_local_paths(item)
            for key, item in value.items()
            if key not in DROPPED_PROPERTY_KEYS
        }
    return value


def build_semantic_color_payload(
    graph: dict[str, Any],
    *,
    source_path: str = "domains/color/ontology/build/graph.json",
) -> dict[str, Any]:
    """Create the deterministic, distributable Semantic OS color snapshot."""

    nodes = _strip_local_paths(graph.get("nodes", []))
    edges = _strip_local_paths(graph.get("edges", []))
    source_projection = {
        "built_at": graph.get("built_at"),
        "schema_version": graph.get("schema_version"),
        "nodes": nodes,
        "edges": edges,
    }
    payload = {
        "schema_version": "design-ontology-harness/semantic-color-ontology-compact-v1",
        "source": {
            "repo": "semantic-os",
            "path": source_path,
            "built_at": graph.get("built_at"),
            "source_schema_version": graph.get("schema_version"),
            "source_graph_sha256": hashlib.sha256(
                canonical_json_bytes(source_projection)
            ).hexdigest(),
            "transport": "docs/color-reference.md",
            "copyright_handling": (
                "Imported as abstracted color ontology nodes; no raw OCR, page images, "
                "or reconstructable source tables are included."
            ),
        },
        "node_count": len(nodes),
        "edge_count": len(edges),
        "nodes": nodes,
        "edges": edges,
    }
    serialized = json.dumps(payload, ensure_ascii=False)
    if "/Users/" in serialized or "/home/" in serialized:
        raise SemanticColorMarkdownError(
            "Abstraction contract violated: a local filesystem path survived sanitization."
        )
    return payload


def render_semantic_color_block(payload: dict[str, Any]) -> str:
    digest = payload_sha256(payload)
    source = payload.get("source", {})
    keyword_nodes = [
        node for node in payload.get("nodes", []) if node.get("type") == "ColorKeyword"
    ]
    usable = sum(
        1
        for node in keyword_nodes
        if (node.get("properties") or {}).get("rgb_hex")
    )
    serialized = json.dumps(payload, ensure_ascii=False, indent=1, sort_keys=True)
    summary = (
        f"Semantic OS 컬러 온톨로지 스냅샷 — {payload.get('node_count', 0)} nodes, "
        f"{payload.get('edge_count', 0)} edges, {len(keyword_nodes)} keywords "
        f"({usable} with HEX)"
    )
    return "\n".join(
        [
            f"<!-- semantic-os-color-ontology:begin sha256={digest} -->",
            "<details>",
            f"<summary>{summary}</summary>",
            "",
            "이 블록은 `sync-semantic-colors`가 생성합니다. 직접 수정하지 마세요.",
            f"원본: `{source.get('repo', 'semantic-os')}/{source.get('path', '')}` · "
            f"built_at: `{source.get('built_at') or 'unknown'}` · sha256: `{digest}`",
            "",
            "```semantic-color-ontology+json",
            serialized,
            "```",
            "",
            "</details>",
            END_MARKER,
        ]
    )


def pantone_coy_index(payload: dict[str, Any]) -> list[dict[str, Any]]:
    """Return the stable, identity-preserving Pantone COY public-fact index."""

    entries: list[dict[str, Any]] = []
    for node in payload.get("nodes", []):
        props = node.get("properties") or {}
        if (
            node.get("type") != "ColorKeyword"
            or props.get("category") != "Pantone Color of the Year"
        ):
            continue
        year = props.get("coy_year")
        hex_value = _normalized_hex(props.get("rgb_hex"))
        if not isinstance(year, int) or not hex_value:
            continue
        entries.append(
            {
                "semantic_node_id": str(node.get("id")),
                "name": props.get("color_name") or props.get("label"),
                "label": props.get("label"),
                "year": year,
                "hex": hex_value,
                "spectrum": props.get("spectrum"),
                "pantone_code": props.get("pantone_code"),
                "source_reference_id": props.get("source_reference_id"),
                "source_type": "semantic-os-generated-index",
                "identity_coverage": "generated-visible-index",
            }
        )
    return sorted(entries, key=lambda item: (item["year"], item["semantic_node_id"]))


def render_semantic_color_catalog(payload: dict[str, Any]) -> str:
    """Render a deterministic visible index without duplicating Markdown cards."""

    digest = payload_sha256(payload)
    entries = pantone_coy_index(payload)
    lines = [
        f"<!-- semantic-os-color-catalog:begin sha256={digest} -->",
        "<details>",
        f"<summary>Pantone Color of the Year identity index — {len(entries)} nodes</summary>",
        "",
        "이 표는 `sync-semantic-colors`가 내장 그래프에서 생성합니다. "
        "HEX 중복 여부와 무관하게 각 Semantic ID를 하나의 독립된 색상 정체성으로 다룹니다.",
        "",
        "| Year | Color | HEX | Spectrum | Pantone | Semantic ID | Source |",
        "| ---: | --- | --- | --- | --- | --- | --- |",
    ]
    for entry in entries:
        lines.append(
            "| {year} | {label} | `{hex}` | {spectrum} | {pantone} | `{node_id}` | `{source}` |".format(
                year=entry["year"],
                label=str(entry["label"]).replace("|", "\\|"),
                hex=entry["hex"],
                spectrum=entry.get("spectrum") or "—",
                pantone=entry.get("pantone_code") or "—",
                node_id=entry["semantic_node_id"],
                source=entry.get("source_reference_id") or "—",
            )
        )
    lines.extend(["", "</details>", CATALOG_END_MARKER])
    return "\n".join(lines)


def _generated_block_bounds(
    text: str,
    begin_re: re.Pattern[str],
    end_marker: str,
) -> tuple[int, int] | None:
    begin = begin_re.search(text)
    if not begin:
        return None
    end_index = text.find(end_marker, begin.end())
    if end_index < 0:
        raise SemanticColorMarkdownError(
            f"Generated color block has a begin marker but no {end_marker!r} end marker."
        )
    return begin.start(), end_index + len(end_marker)


def _has_semantic_color_catalog_namespace(text: str) -> bool:
    return any(
        sentinel in text
        for sentinel in (CATALOG_BEGIN_PREFIX, CATALOG_END_MARKER)
    )


def _semantic_color_catalog_bounds(text: str) -> tuple[int, int] | None:
    if not _has_semantic_color_catalog_namespace(text):
        return None
    if text.count(CATALOG_BEGIN_PREFIX) != 1:
        raise SemanticColorMarkdownError(
            "Semantic OS color catalog namespace is present but needs exactly one "
            "begin marker."
        )
    if text.count(CATALOG_END_MARKER) != 1:
        raise SemanticColorMarkdownError(
            "Semantic OS color catalog namespace is present but needs exactly one "
            "end marker."
        )
    if not CATALOG_BEGIN_RE.search(text):
        raise SemanticColorMarkdownError(
            "Semantic OS color catalog begin marker has a malformed SHA-256 "
            "checksum token."
        )
    bounds = _generated_block_bounds(text, CATALOG_BEGIN_RE, CATALOG_END_MARKER)
    if not bounds:
        raise SemanticColorMarkdownError(
            "Semantic OS color catalog namespace is present but its block is incomplete."
        )
    return bounds


def strip_semantic_color_catalog(text: str) -> str:
    bounds = _semantic_color_catalog_bounds(text)
    if not bounds:
        return text
    start, end = bounds
    begin = CATALOG_BEGIN_RE.search(text, start, end)
    embedded = extract_semantic_color_payload(text)
    if not begin or embedded is None:
        raise SemanticColorMarkdownError(
            "Semantic OS color catalog requires a checksum-verified embedded ontology "
            "payload."
        )
    expected = payload_sha256(embedded)
    actual = begin.group("sha")
    if actual != expected:
        raise SemanticColorMarkdownError(
            "Semantic OS color catalog checksum mismatch with embedded ontology: "
            f"expected {expected}, got {actual}."
        )
    return (text[:start].rstrip() + text[end:]).rstrip() + "\n"


def replace_semantic_color_catalog(text: str, payload: dict[str, Any]) -> str:
    without_catalog = strip_semantic_color_catalog(text).rstrip()
    bounds = _block_bounds(without_catalog)
    if bounds:
        start, _ = bounds
        prefix = without_catalog[:start].rstrip()
        ontology_block = without_catalog[start:].lstrip()
        return (
            prefix
            + "\n\n"
            + render_semantic_color_catalog(payload)
            + "\n\n"
            + ontology_block
            + "\n"
        )
    return without_catalog + "\n\n" + render_semantic_color_catalog(payload) + "\n"


def extract_runtime_color_policy(text: str) -> dict[str, Any] | None:
    if not _has_runtime_policy_namespace(text):
        return None
    if text.count(RUNTIME_POLICY_BEGIN_PREFIX) != 1:
        raise SemanticColorMarkdownError(
            "Runtime color policy namespace is present but needs exactly one begin marker."
        )
    if text.count(RUNTIME_POLICY_END_MARKER) != 1:
        raise SemanticColorMarkdownError(
            "Runtime color policy namespace is present but needs exactly one end marker."
        )
    if text.count(RUNTIME_POLICY_FENCE_PREFIX) != 1:
        raise SemanticColorMarkdownError(
            "Runtime color policy namespace is present but needs exactly one typed JSON fence."
        )
    if not RUNTIME_POLICY_BEGIN_RE.search(text):
        raise SemanticColorMarkdownError(
            "Runtime color policy begin marker has a malformed SHA-256 checksum token."
        )
    bounds = _generated_block_bounds(
        text,
        RUNTIME_POLICY_BEGIN_RE,
        RUNTIME_POLICY_END_MARKER,
    )
    if not bounds:
        return None
    start, end = bounds
    block = text[start:end]
    begin = RUNTIME_POLICY_BEGIN_RE.search(block)
    fenced = RUNTIME_POLICY_PAYLOAD_RE.search(block)
    if not begin or not fenced:
        raise SemanticColorMarkdownError(
            "Runtime color policy block does not contain its typed JSON payload."
        )
    try:
        policy = json.loads(fenced.group("payload"))
    except json.JSONDecodeError as exc:
        raise SemanticColorMarkdownError(
            f"Runtime color policy block contains invalid JSON: {exc}"
        ) from exc
    actual = payload_sha256(policy)
    if actual != begin.group("sha"):
        raise SemanticColorMarkdownError(
            "Runtime color policy checksum mismatch: "
            f"expected {begin.group('sha')}, got {actual}."
        )
    _validate_runtime_color_policy(policy)
    return policy


def _has_runtime_policy_namespace(text: str) -> bool:
    return any(
        sentinel in text
        for sentinel in (
            RUNTIME_POLICY_BEGIN_PREFIX,
            RUNTIME_POLICY_END_MARKER,
            RUNTIME_POLICY_FENCE_PREFIX,
        )
    )


def _validate_runtime_color_policy(policy: dict[str, Any]) -> None:
    if policy.get("schema_version") != "design-ontology-harness/runtime-color-policy-v1":
        raise SemanticColorMarkdownError("Unsupported runtime color policy schema_version.")
    required = {
        "primary",
        "accent",
        "surface-tint",
        "canvas",
        "surface",
        "surface-muted",
        "surface-elevated",
        "border",
        "border-strong",
        "ink",
        "ink-muted",
        "ink-subtle",
        "ink-inverse",
        "info",
        "success",
        "warning",
        "danger",
        "link",
        "link-hover",
    }
    roles = policy.get("light_roles") or {}
    missing = sorted(required - set(roles))
    if missing:
        raise SemanticColorMarkdownError(
            "Runtime color policy is missing required roles: " + ", ".join(missing)
        )
    for role, entry in roles.items():
        if not isinstance(entry, dict) or entry.get("kind") not in {
            "runtime-role-default",
            "derived-runtime-role",
        }:
            raise SemanticColorMarkdownError(
                f"Runtime role {role!r} must declare a runtime role kind."
            )
        if not isinstance(entry.get("source_reference_id"), str):
            raise SemanticColorMarkdownError(
                f"Runtime role {role!r} must declare source_reference_id."
            )
        value = entry.get("value")
        derived_from = entry.get("derived_from")
        if value is None and derived_from is None:
            raise SemanticColorMarkdownError(
                f"Runtime role {role!r} needs value or derived_from."
            )
        if value is not None and not _normalized_hex(value):
            raise SemanticColorMarkdownError(
                f"Runtime role {role!r} has invalid HEX value {value!r}."
            )
    chrome_roles = policy.get("chrome_roles") or {}
    required_chrome = {
        "chrome_ink",
        "chrome_paper",
        "chrome_canvas",
        "chrome_line",
        "chrome_muted",
    }
    missing_chrome = sorted(required_chrome - set(chrome_roles))
    if missing_chrome:
        raise SemanticColorMarkdownError(
            "Runtime color policy is missing chrome roles: " + ", ".join(missing_chrome)
        )
    for role, entry in chrome_roles.items():
        if (
            not isinstance(entry, dict)
            or entry.get("kind") != "runtime-chrome-role"
            or not _normalized_hex(entry.get("value"))
            or not isinstance(entry.get("source_reference_id"), str)
        ):
            raise SemanticColorMarkdownError(
                f"Runtime chrome role {role!r} is incomplete or invalid."
            )
    derivation = policy.get("dark_derivation") or {}
    if (
        derivation.get("kind") != "derived-runtime-role-policy"
        or derivation.get("method") != "hsl-role-targets"
    ):
        raise SemanticColorMarkdownError(
            "Runtime color policy needs typed dark_derivation rules."
        )
    for key in (
        "neutral_max_saturation",
        "chromatic_min_saturation",
        "chromatic_lightness_delta",
    ):
        value = derivation.get(key)
        if not _is_unit_number(value):
            raise SemanticColorMarkdownError(
                f"Runtime dark_derivation.{key} must be numeric in the 0..1 range."
            )
    lightness_range = derivation.get("chromatic_lightness_range")
    if (
        not isinstance(lightness_range, list)
        or len(lightness_range) != 2
        or not all(_is_unit_number(value) for value in lightness_range)
        or not 0 <= lightness_range[0] <= lightness_range[1] <= 1
    ):
        raise SemanticColorMarkdownError(
            "Runtime dark_derivation.chromatic_lightness_range must be an ordered 0..1 pair."
        )
    required_targets = {
        "canvas",
        "surface",
        "surface-muted",
        "surface-elevated",
        "surface-tint",
        "border",
        "border-strong",
        "ink",
        "ink-muted",
        "ink-subtle",
        "ink-inverse",
    }
    targets = derivation.get("role_lightness_targets") or {}
    missing_targets = sorted(required_targets - set(targets))
    if missing_targets:
        raise SemanticColorMarkdownError(
            "Runtime dark_derivation is missing role targets: "
            + ", ".join(missing_targets)
        )
    if any(
        not _is_unit_number(value)
        for value in targets.values()
    ):
        raise SemanticColorMarkdownError(
            "Runtime dark_derivation role targets must be numeric in the 0..1 range."
        )
    _validate_contrast_floor(
        derivation.get("contrast_floor"),
        roles,
        label="Runtime dark_derivation",
    )
    _validate_contrast_floor(
        policy.get("light_contrast_floor"),
        roles,
        label="Runtime light_contrast_floor",
    )
    # WCAG 1.4.11 비텍스트 대비. 텍스트 하한과 같은 구조이지만 대상 역할과 비율이 다르다.
    _validate_contrast_floor(
        derivation.get("non_text_contrast_floor"),
        roles,
        label="Runtime dark_derivation non_text_contrast_floor",
    )
    _validate_contrast_floor(
        policy.get("non_text_contrast_floor"),
        roles,
        label="Runtime non_text_contrast_floor",
    )


def _validate_contrast_floor(
    contrast_floor: object,
    roles: dict[str, Any],
    *,
    label: str,
) -> None:
    if not isinstance(contrast_floor, dict) or contrast_floor.get("kind") != "wcag-contrast-floor":
        raise SemanticColorMarkdownError(
            f"{label} needs a typed WCAG contrast floor."
        )
    minimum_ratio = contrast_floor.get("minimum_ratio")
    if (
        not isinstance(minimum_ratio, (int, float))
        or isinstance(minimum_ratio, bool)
        or not 1 <= minimum_ratio <= 21
    ):
        raise SemanticColorMarkdownError(
            f"{label} contrast floor must use a 1..21 ratio."
        )
    target_role = contrast_floor.get("adjustment_target_role")
    if not isinstance(target_role, str) or target_role not in roles:
        raise SemanticColorMarkdownError(
            f"{label} contrast floor needs a known adjustment_target_role."
        )
    # 조정 대상 목록은 `adjusted_roles`가 정식 이름이다. 텍스트 하한은 유채색 역할만
    # 조정해서 `chromatic_roles`로 남아 있고, 비텍스트 하한은 중립색 역할을 조정한다.
    adjusted_field = "adjusted_roles" if "adjusted_roles" in contrast_floor else "chromatic_roles"
    for field in ("background_roles", adjusted_field):
        values = contrast_floor.get(field)
        if (
            not isinstance(values, list)
            or not values
            or any(not isinstance(value, str) or not value for value in values)
        ):
            raise SemanticColorMarkdownError(
                f"{label} contrast_floor.{field} must be a non-empty string list."
            )
        unknown = sorted(set(values) - set(roles))
        if unknown:
            raise SemanticColorMarkdownError(
                f"{label} contrast_floor.{field} has unknown roles: "
                + ", ".join(unknown)
            )


def _is_unit_number(value: Any) -> bool:
    return (
        isinstance(value, (int, float))
        and not isinstance(value, bool)
        and 0 <= value <= 1
    )


@lru_cache(maxsize=4)
def _load_runtime_color_policy_cached(
    source_id: str,
    content_sha256: str,
    text: str,
) -> dict[str, Any]:
    del content_sha256  # cache-key only; makes edits invalidate cached parsing.
    policy = extract_runtime_color_policy(text)
    if policy is None:
        raise SemanticColorMarkdownError(
            f"Runtime color policy is missing from the Markdown authority: {source_id}"
        )
    return policy


def load_runtime_color_policy(path: Path | None = None) -> dict[str, Any]:
    """Load typed runtime role defaults from the Markdown authority."""

    if path is None:
        text, source_id = read_default_color_reference()
    else:
        resolved = path.expanduser().resolve()
        text = resolved.read_text(encoding="utf-8")
        source_id = str(resolved)
        # A custom reference may focus only on curated cards. In that case it
        # explicitly inherits the bundled typed policy. A present-but-corrupt
        # block still fails above rather than silently falling back.
        if not _has_runtime_policy_namespace(text):
            inherited = load_runtime_color_policy()
            inherited["inheritance"] = {
                "mode": "package-default",
                "requested_reference_path": _portable_reference_path(source_id),
            }
            return inherited
    digest = hashlib.sha256(text.encode("utf-8")).hexdigest()
    return deepcopy(_load_runtime_color_policy_cached(source_id, digest, text))


def runtime_role_values(path: Path | None = None) -> dict[str, str]:
    policy = load_runtime_color_policy(path)
    entries = policy["light_roles"]
    resolved: dict[str, str] = {}
    pending = dict(entries)
    while pending:
        progressed = False
        for role, entry in list(pending.items()):
            value = _normalized_hex(entry.get("value"))
            if value:
                resolved[role] = value
                pending.pop(role)
                progressed = True
                continue
            source_role = entry.get("derived_from")
            if source_role in resolved:
                resolved[role] = resolved[source_role]
                pending.pop(role)
                progressed = True
        if not progressed:
            raise SemanticColorMarkdownError(
                "Runtime color policy contains unresolved derived roles: "
                + ", ".join(sorted(pending))
            )
    return resolved


def _has_semantic_color_ontology_namespace(text: str) -> bool:
    return any(
        sentinel in text
        for sentinel in (ONTOLOGY_BEGIN_PREFIX, END_MARKER, ONTOLOGY_FENCE_PREFIX)
    )


def _block_bounds(text: str) -> tuple[int, int] | None:
    if not _has_semantic_color_ontology_namespace(text):
        return None
    if text.count(ONTOLOGY_BEGIN_PREFIX) != 1:
        raise SemanticColorMarkdownError(
            "Semantic OS color ontology namespace is present but needs exactly one "
            "begin marker."
        )
    if text.count(END_MARKER) != 1:
        raise SemanticColorMarkdownError(
            "Semantic OS color ontology namespace is present but needs exactly one "
            "end marker."
        )
    if text.count(ONTOLOGY_FENCE_PREFIX) != 1:
        raise SemanticColorMarkdownError(
            "Semantic OS color ontology namespace is present but needs exactly one "
            "typed JSON fence."
        )
    begin = BEGIN_RE.search(text)
    if not begin:
        raise SemanticColorMarkdownError(
            "Semantic OS color ontology begin marker has a malformed SHA-256 "
            "checksum token."
        )
    end_index = text.find(END_MARKER, begin.end())
    if end_index < 0:
        raise SemanticColorMarkdownError(
            "Semantic OS color ontology markers are out of order or incomplete."
        )
    block = text[begin.start() : end_index + len(END_MARKER)]
    if not FENCED_PAYLOAD_RE.search(block):
        raise SemanticColorMarkdownError(
            "Semantic OS color ontology block does not contain one complete typed JSON "
            "payload fence."
        )
    return begin.start(), end_index + len(END_MARKER)


def strip_semantic_color_block(text: str) -> str:
    bounds = _block_bounds(text)
    if not bounds:
        return text
    start, end = bounds
    return (text[:start].rstrip() + text[end:]).rstrip() + "\n"


def replace_semantic_color_block(text: str, payload: dict[str, Any]) -> str:
    visible = strip_semantic_color_block(text).rstrip()
    return visible + "\n\n" + render_semantic_color_block(payload) + "\n"


def extract_semantic_color_payload(text: str) -> dict[str, Any] | None:
    bounds = _block_bounds(text)
    if not bounds:
        return None
    start, end = bounds
    block = text[start:end]
    begin = BEGIN_RE.search(block)
    fenced = FENCED_PAYLOAD_RE.search(block)
    if not begin or not fenced:
        raise SemanticColorMarkdownError(
            "Semantic OS color block does not contain a semantic-color-ontology+json payload."
        )
    try:
        payload = json.loads(fenced.group("payload"))
    except json.JSONDecodeError as exc:
        raise SemanticColorMarkdownError(
            f"Semantic OS color block contains invalid JSON: {exc}"
        ) from exc
    actual = payload_sha256(payload)
    expected = begin.group("sha")
    if actual != expected:
        raise SemanticColorMarkdownError(
            f"Semantic OS color block checksum mismatch: expected {expected}, got {actual}."
        )
    return payload


def parse_color_reference_text(text: str, *, source_path: str | None = None) -> dict[str, Any]:
    """Parse the visible Markdown color cards without reading the embedded JSON as prose."""

    embedded = extract_semantic_color_payload(text)
    runtime_policy = extract_runtime_color_policy(text)
    # The catalog checksum is bound to the embedded payload, so validate and remove
    # the catalog while that payload is still present.
    visible = strip_semantic_color_block(strip_semantic_color_catalog(text))
    title = Path(source_path).stem if source_path else "color-reference"
    current_family: str | None = None
    current_color: dict[str, Any] | None = None
    colors: list[dict[str, Any]] = []

    for raw_line in visible.splitlines():
        line = raw_line.strip()
        if not line:
            continue

        if line.startswith("# "):
            title = line[2:].strip()
            continue
        if line.startswith("## "):
            current_family = line[3:].strip()
            continue
        if line.startswith("### "):
            current_color = {
                "name": line[4:].strip(),
                "family": current_family,
                "hex": None,
                "cmyk": None,
                "mood": None,
                "usage": None,
                "pairings": [],
                "aliases": [],
                "mood_tags": [],
                "tone_axes": [],
                "semantic_node_id": None,
                "source_type": "markdown-color-card",
                "source_reference_id": None,
                "source_reference_ids": [],
                "source_citations": [],
                "source_provenance": [],
                "spectrum": None,
                "ontology_family": None,
                "ontology_category": None,
            }
            colors.append(current_color)
            continue

        if not current_color or not line.startswith("- **"):
            continue
        try:
            label_part, value = line[2:].split("**:", 1)
        except ValueError:
            continue
        label = label_part.replace("**", "").strip().lower()
        value = value.strip()

        if label == "hex":
            match = COLOR_HEX_RE.search(value)
            current_color["hex"] = match.group(0).upper() if match else value
        elif label == "cmyk":
            current_color["cmyk"] = value
        elif label in {"톤/무드", "tone/mood"}:
            current_color["mood"] = value
        elif label in {"활용", "usage", "summary"}:
            current_color["usage"] = value
        elif label in {"배색", "pairings"}:
            current_color["pairings"] = [
                item.upper() for item in COLOR_HEX_RE.findall(value)
            ]
        elif label in {"별칭", "aliases"}:
            current_color["aliases"] = _parse_inline_list(value)
        elif label in {"mood tags", "무드 태그"}:
            current_color["mood_tags"] = _parse_inline_list(value)
        elif label in {"tone axes", "톤 축"}:
            current_color["tone_axes"] = _parse_inline_list(value)
        elif label in {"semantic id", "ontology id", "semantic node id"}:
            current_color["semantic_node_id"] = value.strip("` ")
        elif label in {"source type", "소스 유형"}:
            current_color["source_type"] = value.strip("` ")
        elif label in {"source", "source reference", "출처", "출처 id", "source id"}:
            citations = _parse_source_citations(value)
            current_color["source_citations"].extend(citations)
            explicit_ids = [
                item for item in re.findall(r"\bref-[a-z0-9-]+\b", value.casefold())
            ]
            for reference_id in explicit_ids:
                if reference_id not in current_color["source_reference_ids"]:
                    current_color["source_reference_ids"].append(reference_id)
        elif label == "spectrum":
            current_color["spectrum"] = value.strip("` ")
        elif label in {"ontology family", "semantic family"}:
            current_color["ontology_family"] = value.strip("` ")
        elif label in {"ontology category", "semantic category"}:
            current_color["ontology_category"] = value.strip("` ")

    provenance_by_id = _provenance_by_id(embedded, runtime_policy)
    citation_aliases = (runtime_policy or {}).get("citation_aliases") or {}
    for color in colors:
        resolved_ids = list(color.get("source_reference_ids") or [])
        for citation in color.get("source_citations") or []:
            reference_id = citation_aliases.get(citation)
            if isinstance(reference_id, str) and reference_id not in resolved_ids:
                resolved_ids.append(reference_id)
        color["source_reference_ids"] = resolved_ids
        color["source_reference_id"] = resolved_ids[0] if resolved_ids else None
        color["source_provenance"] = [
            provenance_by_id[reference_id]
            for reference_id in resolved_ids
            if reference_id in provenance_by_id
        ]

    return {
        "title": title,
        "source_path": source_path,
        "families": sorted(
            {color["family"] for color in colors if color.get("family")}
        ),
        "colors": colors,
        "color_index": [*colors, *pantone_coy_index(embedded or {})],
        "pantone_coy_index": pantone_coy_index(embedded or {}),
        "semantic_ontology": embedded,
        "semantic_ontology_sha256": payload_sha256(embedded) if embedded else None,
        "runtime_color_policy": runtime_policy,
        "runtime_color_policy_sha256": payload_sha256(runtime_policy) if runtime_policy else None,
        "source_registry": provenance_by_id,
    }


def _parse_inline_list(value: str) -> list[str]:
    cleaned = value.replace("`", "")
    return [item.strip() for item in re.split(r"[,;]", cleaned) if item.strip()]


def _parse_source_citations(value: str) -> list[str]:
    citations: list[str] = []
    for group in re.findall(r"\[([^\]]+)\]", value):
        for item in re.split(r"[,;]", group):
            normalized = item.strip()
            if normalized and normalized not in citations:
                citations.append(normalized)
    return citations


def _provenance_by_id(
    ontology: dict[str, Any] | None,
    runtime_policy: dict[str, Any] | None = None,
) -> dict[str, dict[str, Any]]:
    registry = {
        str(node.get("id")): {
            "id": str(node.get("id")),
            "type": node.get("type"),
            **deepcopy(node.get("properties") or {}),
        }
        for node in (ontology or {}).get("nodes", [])
        if node.get("type") == "ColorReference" and node.get("id")
    }
    registry[LOCAL_EXTENSION_REFERENCE_ID] = {
        "id": LOCAL_EXTENSION_REFERENCE_ID,
        "type": "ColorReference",
        **_local_extension_reference_properties(),
    }
    authority = (runtime_policy or {}).get("authority") or {}
    runtime_reference_id = authority.get("source_reference_id")
    if runtime_reference_id:
        registry[str(runtime_reference_id)] = {
            "id": str(runtime_reference_id),
            "type": "RuntimeColorPolicyReference",
            **deepcopy(authority),
        }
    return registry


def merge_visible_cards_into_ontology(
    ontology: dict[str, Any],
    colors: list[dict[str, Any]],
) -> dict[str, Any]:
    """Overlay visible Markdown curation and add explicit Markdown-only colors."""

    merged = deepcopy(ontology)
    nodes = merged.setdefault("nodes", [])
    edges = merged.setdefault("edges", [])
    keyword_nodes = [node for node in nodes if node.get("type") == "ColorKeyword"]
    by_id = {str(node.get("id")): node for node in keyword_nodes}
    by_label = {
        str((node.get("properties") or {}).get("label", "")).casefold(): node
        for node in keyword_nodes
        if (node.get("properties") or {}).get("label")
    }

    local_count = 0
    local_reference: dict[str, Any] | None = None
    known_node_spaces = {
        str(node.get("id")): str(node.get("space") or "concept")
        for node in nodes
        if node.get("id")
    }
    for color in colors:
        name = str(color.get("name") or "").strip()
        hex_value = _normalized_hex(color.get("hex"))
        if not name or not hex_value:
            continue
        node = None
        semantic_id = str(color.get("semantic_node_id") or "").strip()
        if semantic_id:
            node = by_id.get(semantic_id)
        if node is None:
            node = by_label.get(name.casefold())
        if node is None:
            node = _find_color_name_alias(keyword_nodes, name, hex_value)

        if node is None:
            local_count += 1
            if local_reference is None:
                local_reference = _ensure_local_extension_reference(nodes)
                known_node_spaces[LOCAL_EXTENSION_REFERENCE_ID] = str(
                    local_reference.get("space") or "resource"
                )
            local_id = semantic_id or f"color-keyword-local-{_slugify(name)}"
            source_reference_ids = list(color.get("source_reference_ids") or [])
            if LOCAL_EXTENSION_REFERENCE_ID not in source_reference_ids:
                source_reference_ids.append(LOCAL_EXTENSION_REFERENCE_ID)
            node = {
                "space": "concept",
                "type": "ColorKeyword",
                "id": local_id,
                "properties": {
                    "label": name,
                    "summary": color.get("usage") or color.get("mood") or name,
                    "spectrum": color.get("spectrum") or _spectrum_from_family(color.get("family")),
                    "family": color.get("ontology_family") or "local_extension",
                    "category": color.get("ontology_category") or color.get("family") or "Local Extensions",
                    "rgb_hex": hex_value,
                    "cmyk": color.get("cmyk"),
                    "mood_tags": color.get("mood_tags") or [],
                    "tone_axes": color.get("tone_axes") or [],
                    "source_reference_id": source_reference_ids[0],
                    "source_reference_ids": source_reference_ids,
                    "curation_reference_id": LOCAL_EXTENSION_REFERENCE_ID,
                    "status": "local_extension",
                    "identity_scope": "design-ontology-harness-local-extension",
                    "not_a_rule": True,
                    "applies_when": {"medium": ["any"], "spectrum": ["any"]},
                    "source_type": "markdown-local-extension",
                },
            }
            nodes.append(node)
            keyword_nodes.append(node)
            by_id[local_id] = node
            by_label[name.casefold()] = node
            known_node_spaces[local_id] = "concept"
            _append_edge(
                edges,
                from_id=LOCAL_EXTENSION_REFERENCE_ID,
                from_space=(local_reference or {}).get("space") or "resource",
                relation="contains",
                to_id=local_id,
                to_space="concept",
            )
            spectrum = color.get("spectrum") or _spectrum_from_family(color.get("family"))
            topic_id = f"topic-color-{spectrum}-spectrum" if spectrum else None
            if topic_id and topic_id in known_node_spaces:
                _append_edge(
                    edges,
                    from_id=local_id,
                    from_space="concept",
                    relation="belongs_to_topic",
                    to_id=topic_id,
                    to_space=known_node_spaces[topic_id],
                )
            for reference_id in source_reference_ids:
                if reference_id in known_node_spaces:
                    _append_edge(
                        edges,
                        from_id=local_id,
                        from_space="concept",
                        relation="cites",
                        to_id=reference_id,
                        to_space=known_node_spaces[reference_id],
                    )

        props = node.setdefault("properties", {})
        imported_hex = _normalized_hex(props.get("rgb_hex"))
        if imported_hex and imported_hex != hex_value:
            props["semantic_os_rgb_hex"] = imported_hex
        props["rgb_hex"] = hex_value
        if color.get("cmyk"):
            props["cmyk"] = color["cmyk"]
        props.setdefault("source_type", "semantic-os-synced-markdown")
        aliases = list(props.get("aliases") or [])
        if name.casefold() != str(props.get("label") or "").casefold() and name not in aliases:
            aliases.append(name)
        if aliases:
            props["aliases"] = aliases
        if color.get("usage"):
            props["curated_usage"] = color["usage"]
        if color.get("mood"):
            props["curated_mood"] = color["mood"]
        if color.get("pairings"):
            props["curated_pairings"] = color["pairings"]
        props["markdown_family"] = color.get("family")
        if color.get("ontology_family"):
            props["curated_ontology_family"] = color["ontology_family"]
        if color.get("ontology_category"):
            props["curated_ontology_category"] = color["ontology_category"]
        if color.get("source_reference_ids"):
            props.setdefault("source_reference_id", color["source_reference_ids"][0])
            props["curated_source_reference_ids"] = list(color["source_reference_ids"])

    merged["node_count"] = len(nodes)
    merged["edge_count"] = len(edges)
    source = merged.setdefault("source", {})
    source["authority"] = "semantic-os-synced-markdown"
    source["visible_color_card_count"] = len(colors)
    source["local_extension_count"] = local_count
    return merged


def _ensure_local_extension_reference(nodes: list[dict[str, Any]]) -> dict[str, Any]:
    for node in nodes:
        if node.get("id") == LOCAL_EXTENSION_REFERENCE_ID:
            return node
    reference = {
        "space": "resource",
        "type": "ColorReference",
        "id": LOCAL_EXTENSION_REFERENCE_ID,
        "properties": _local_extension_reference_properties(),
    }
    nodes.append(reference)
    return reference


def _local_extension_reference_properties() -> dict[str, Any]:
    return {
        "label": "docs/color-reference.md local color extensions",
        "source_format": "checksum-verified-markdown-curation",
        "source_path": "docs/color-reference.md",
        "status": "authored-local-extension-authority",
        "copyright_handling": (
            "Stores explicit local identities and abstract color coordinates only; "
            "the embedded Semantic OS graph remains unchanged."
        ),
    }


def _append_edge(
    edges: list[dict[str, Any]],
    *,
    from_id: str,
    from_space: str,
    relation: str,
    to_id: str,
    to_space: str,
) -> None:
    edge = {
        "from": {"id": from_id, "space": from_space},
        "relation": relation,
        "to": {"id": to_id, "space": to_space},
    }
    if edge not in edges:
        edges.append(edge)


def _find_color_name_alias(
    keyword_nodes: list[dict[str, Any]],
    name: str,
    hex_value: str,
) -> dict[str, Any] | None:
    matches = []
    for node in keyword_nodes:
        props = node.get("properties") or {}
        if str(props.get("color_name") or "").casefold() != name.casefold():
            continue
        if _normalized_hex(props.get("rgb_hex")) != hex_value:
            continue
        matches.append(node)
    return matches[0] if len(matches) == 1 else None


def _normalized_hex(value: Any) -> str | None:
    if not isinstance(value, str):
        return None
    match = COLOR_HEX_RE.fullmatch(value.strip())
    return match.group(0).upper() if match else None


def _slugify(value: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", value.casefold()).strip("-")
    return slug or "unnamed"


def _spectrum_from_family(value: Any) -> str | None:
    text = str(value or "").casefold()
    for spectrum in ("red", "orange", "yellow", "green", "blue", "violet", "neutral"):
        if spectrum in text:
            return spectrum
    return None


def read_default_color_reference() -> tuple[str, str]:
    if DEFAULT_COLOR_REFERENCE_PATH.exists():
        return (
            DEFAULT_COLOR_REFERENCE_PATH.read_text(encoding="utf-8"),
            str(DEFAULT_COLOR_REFERENCE_PATH),
        )
    resource = files("design_ontology_harness").joinpath("resources/color-reference.md")
    if resource.is_file():
        return resource.read_text(encoding="utf-8"), "package:resources/color-reference.md"
    raise SemanticColorMarkdownError(
        "Default color reference is unavailable. Run sync-semantic-colors or reinstall "
        "the package with resources/color-reference.md included."
    )


def load_ontology_from_color_reference(
    path: Path | None = None,
) -> tuple[dict[str, Any], dict[str, Any]]:
    if path is None:
        text, source_path = read_default_color_reference()
    else:
        source_path = str(path)
        text = path.read_text(encoding="utf-8")
    parsed = parse_color_reference_text(text, source_path=source_path)
    ontology = parsed.get("semantic_ontology")
    if ontology is None:
        ontology = {
            "schema_version": "design-ontology-harness/semantic-color-ontology-markdown-v1",
            "source": {
                "repo": "local-markdown",
                "path": source_path,
                "transport": "color-reference.md",
            },
            "node_count": 0,
            "edge_count": 0,
            "nodes": [],
            "edges": [],
        }
    merged = merge_visible_cards_into_ontology(ontology, parsed["colors"])
    _bind_visible_card_identities(parsed["colors"], merged)
    merged.setdefault("source", {})["reference_path"] = _portable_reference_path(source_path)
    parsed["semantic_ontology"] = merged
    return merged, parsed


def _bind_visible_card_identities(
    colors: list[dict[str, Any]],
    ontology: dict[str, Any],
) -> None:
    """Attach unambiguous merged node identity to the backward-compatible cards."""

    keyword_nodes = [
        node for node in ontology.get("nodes", []) if node.get("type") == "ColorKeyword"
    ]
    for color in colors:
        if color.get("semantic_node_id"):
            continue
        name = str(color.get("name") or "").casefold()
        hex_value = _normalized_hex(color.get("hex"))
        exact_matches = []
        alias_matches = []
        for node in keyword_nodes:
            props = node.get("properties") or {}
            if _normalized_hex(props.get("rgb_hex")) != hex_value:
                continue
            if name == str(props.get("label") or "").casefold():
                exact_matches.append(node)
                continue
            node_aliases = {
                str(props.get("color_name") or "").casefold(),
                *(str(item).casefold() for item in props.get("aliases", []) or []),
            }
            if name in node_aliases:
                alias_matches.append(node)
        matches = exact_matches or alias_matches
        if len(matches) == 1:
            node = matches[0]
            props = node.get("properties") or {}
            color["semantic_node_id"] = node.get("id")
            color["ontology_family"] = color.get("ontology_family") or props.get("family")
            color["ontology_category"] = color.get("ontology_category") or props.get("category")


def _portable_reference_path(value: str) -> str:
    try:
        return str(Path(value).resolve().relative_to(REPO_ROOT))
    except (ValueError, OSError):
        return value if value.startswith("package:") else Path(value).name


def sync_semantic_colors(
    *,
    source_path: Path = DEFAULT_SEMANTIC_OS_SOURCE,
    color_reference_output: Path = DEFAULT_COLOR_REFERENCE_PATH,
    ontology_output: Path | None = DEFAULT_ONTOLOGY_SNAPSHOT_PATH,
    check: bool = False,
) -> dict[str, Any]:
    source_path = source_path.expanduser().resolve()
    color_reference_output = color_reference_output.expanduser().resolve()
    if not source_path.is_file():
        raise FileNotFoundError(f"Semantic OS color graph not found: {source_path}")
    graph = json.loads(source_path.read_text(encoding="utf-8"))
    payload = build_semantic_color_payload(graph)
    existing = (
        color_reference_output.read_text(encoding="utf-8")
        if color_reference_output.exists()
        else "# Semantic OS Color Reference\n"
    )
    # Validate the existing catalog against the existing embedded payload before
    # replacing either block. This fails closed on corrupt/stale marker metadata while
    # still allowing a legitimate source graph update to replace both generated blocks.
    expected_markdown = replace_semantic_color_catalog(existing, payload)
    expected_markdown = replace_semantic_color_block(expected_markdown, payload)

    snapshot_text = json.dumps(payload, ensure_ascii=False, indent=1) + "\n"
    markdown_current = color_reference_output.exists() and existing == expected_markdown
    snapshot_current = True
    if ontology_output is not None:
        ontology_output = ontology_output.expanduser().resolve()
        snapshot_current = (
            ontology_output.exists()
            and _snapshot_equivalent(ontology_output, payload)
        )
    policy = extract_runtime_color_policy(existing)
    default_authority = color_reference_output == DEFAULT_COLOR_REFERENCE_PATH.resolve()
    if default_authority and policy is None:
        raise SemanticColorMarkdownError(
            "The default Markdown color authority is missing its typed runtime color policy."
        )
    policy_current = policy is not None or not default_authority
    current = markdown_current and snapshot_current and policy_current

    if not check:
        color_reference_output.parent.mkdir(parents=True, exist_ok=True)
        color_reference_output.write_text(expected_markdown, encoding="utf-8")
        if ontology_output is not None:
            ontology_output.parent.mkdir(parents=True, exist_ok=True)
            ontology_output.write_text(snapshot_text, encoding="utf-8")

    keywords = [
        node for node in payload["nodes"] if node.get("type") == "ColorKeyword"
    ]
    return {
        "ok": current if check else True,
        "check": check,
        "changed": not current,
        "source": str(source_path),
        "color_reference_output": str(color_reference_output),
        "ontology_output": str(ontology_output) if ontology_output is not None else None,
        "payload_sha256": payload_sha256(payload),
        "node_count": payload["node_count"],
        "edge_count": payload["edge_count"],
        "keyword_count": len(keywords),
        "hex_keyword_count": sum(
            1 for node in keywords if (node.get("properties") or {}).get("rgb_hex")
        ),
        "pantone_coy_identity_count": len(pantone_coy_index(payload)),
        "runtime_policy_sha256": payload_sha256(policy) if policy else None,
        "runtime_policy_valid": policy_current,
    }


def _snapshot_equivalent(path: Path, payload: dict[str, Any]) -> bool:
    try:
        current = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return False
    current = deepcopy(current)
    if isinstance(current.get("source"), dict):
        current["source"].pop("imported_at", None)
    return current == payload
