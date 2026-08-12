"""Load and validate the bundled VibeCoding motion reference pack.

The pack is intentionally a small, dependency-free semantic fixture. It converts
visual inspiration into existing design-ontology concepts without treating
third-party previews as executable code or redistribution permission.

This module also owns the project's **motion system**: the duration scale, loop
budget, easing set, and reduced-motion strategy that ``emit-tokens`` renders as
``--ds-duration-*`` / ``--ds-loop-*`` / ``--ds-ease-*`` custom properties.
Keeping the pack contract and the emitted scale in one place is deliberate — the
previous split let the pack declare one scale while the emitter hard-coded
another, so implementations had no single set of values to bind to.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

_RESOURCES = Path(__file__).with_name("resources")
PACK_PATH = _RESOURCES / "vibecoding-motion-reference.json"
HARNESS_CANDIDATES_PATH = _RESOURCES / "harness-interaction-candidates.json"

#: Every pack that contributes to the candidate pool. External references and
#: harness-authored baselines stay in separate files so provenance is never
#: blurred, but they share one schema and one selection path.
CANDIDATE_PACK_PATHS: tuple[Path, ...] = (HARNESS_CANDIDATES_PATH, PACK_PATH)

SUPPORTED_SCHEMA = "motion-reference-pack/v1"
_ALLOWED_EASINGS = {"standard", "enter", "exit", "emphasized"}
_ALLOWED_REDUCED = {"static", "opacity-only", "skip"}
_ALLOWED_MOTION_KINDS = {"transition", "loop"}
_REQUIRED_SOURCE_FIELDS = {"id", "label", "canonical_url", "provenance", "license_status"}
_ALLOWED_PROVENANCE = {"user-supplied", "inspected", "verified", "harness-authored"}
_ALLOWED_LICENSE_STATUS = {"unverified", "reference-only", "verified", "harness-owned"}

#: Selection axes. A surface may take at most one pattern per axis, which is
#: what keeps "one primary motion" enforceable.
INTERACTION_AXES: tuple[str, ...] = ("enter", "emphasis", "progress", "transition")

#: Interaction roles. Project components map onto these, so a candidate written
#: once applies to every project rather than to the one it was authored for.
INTERACTION_ROLES: tuple[str, ...] = (
    "list-surface",
    "detail-panel",
    "async-action",
    "selection-target",
    "status-region",
    "navigation-surface",
    "showcase-surface",
)

MOTION_SYSTEM_SCHEMA = "motion-system/v1"

#: Transition budget. A state change may not exceed the largest step; anything
#: longer reads as an effect rather than as feedback.
TRANSITION_SCALE_MS: tuple[int, ...] = (80, 120, 180, 240, 320)

#: Loop budget, kept in a separate namespace. Loading and progress affordances
#: legitimately cycle for over a second, which the transition scale must not
#: silently license for decorative movement.
LOOP_SCALE_MS: dict[str, int] = {"fast": 1200, "medium": 1600, "slow": 2400}

#: Easing set. Values match what the existing mockups already converged on, so
#: migrating literals to tokens does not change rendered motion.
EASING: dict[str, str] = {
    "standard": "cubic-bezier(0.2, 0, 0, 1)",
    "enter": "cubic-bezier(0, 0, 0.2, 1)",
    "exit": "cubic-bezier(0.4, 0, 1, 1)",
    "emphasized": "cubic-bezier(0.05, 0.7, 0.1, 1)",
}

DEFAULT_REDUCED_MOTION_STRATEGY = "opacity-only"

MAX_TRANSITION_MS = TRANSITION_SCALE_MS[-1]
MAX_LOOP_MS = max(LOOP_SCALE_MS.values())


class MotionReferencePackError(ValueError):
    """Raised when the bundled motion reference pack violates its contract."""


def default_motion_system() -> dict[str, Any]:
    """Return the motion system every project starts from."""
    return {
        "schema_version": MOTION_SYSTEM_SCHEMA,
        "transition_scale_ms": list(TRANSITION_SCALE_MS),
        "loop_scale_ms": dict(LOOP_SCALE_MS),
        "easing": dict(EASING),
        "reduced_motion_strategy": DEFAULT_REDUCED_MOTION_STRATEGY,
    }


def build_motion_system(source: dict[str, Any] | None = None) -> dict[str, Any]:
    """Resolve a project's motion system, overlaying any authored overrides.

    ``source`` is a brand profile or blueprint. Overrides are merged onto the
    default rather than replacing it, so a project can retune easing or the
    reduced-motion strategy without dropping scale steps that components and the
    linter expect to exist.
    """
    system = default_motion_system()
    override = (source or {}).get("motion_system")
    if not isinstance(override, dict):
        return system

    scale = override.get("transition_scale_ms")
    if isinstance(scale, (list, tuple)) and scale:
        steps = sorted({int(value) for value in scale if isinstance(value, (int, float))})
        if steps and steps[-1] <= MAX_TRANSITION_MS:
            system["transition_scale_ms"] = steps

    loops = override.get("loop_scale_ms")
    if isinstance(loops, dict) and loops:
        merged = dict(system["loop_scale_ms"])
        for name, value in loops.items():
            if isinstance(value, (int, float)) and 0 < int(value) <= MAX_LOOP_MS:
                merged[str(name)] = int(value)
        system["loop_scale_ms"] = merged

    easing = override.get("easing")
    if isinstance(easing, dict):
        merged_easing = dict(system["easing"])
        for name, value in easing.items():
            if str(name) in _ALLOWED_EASINGS and isinstance(value, str) and value.strip():
                merged_easing[str(name)] = value.strip()
        system["easing"] = merged_easing

    strategy = override.get("reduced_motion_strategy")
    if strategy in _ALLOWED_REDUCED:
        system["reduced_motion_strategy"] = strategy

    return system


def motion_token_declarations(motion_system: dict[str, Any] | None = None) -> list[str]:
    """Render the motion system as ``--ds-*`` CSS custom property declarations.

    These are the only motion values implementations may bind to. The linter
    treats a raw duration or easing literal the same way it treats a hard-coded
    colour.
    """
    system = motion_system or default_motion_system()
    lines: list[str] = []
    for step in system.get("transition_scale_ms") or TRANSITION_SCALE_MS:
        lines.append(f"  --ds-duration-{int(step)}: {int(step)}ms;")
    for name, value in sorted((system.get("loop_scale_ms") or LOOP_SCALE_MS).items()):
        lines.append(f"  --ds-loop-{name}: {int(value)}ms;")
    for name, value in sorted((system.get("easing") or EASING).items()):
        lines.append(f"  --ds-ease-{name}: {value};")
    strategy = system.get("reduced_motion_strategy") or DEFAULT_REDUCED_MOTION_STRATEGY
    lines.append(f"  --ds-motion-reduced-strategy: {strategy};")
    return lines


def load_motion_reference_pack(path: Path | str = PACK_PATH) -> dict[str, Any]:
    pack_path = Path(path)
    try:
        data = json.loads(pack_path.read_text(encoding="utf-8"))
    except OSError as exc:
        raise MotionReferencePackError(f"Cannot read motion reference pack: {pack_path}") from exc
    except json.JSONDecodeError as exc:
        raise MotionReferencePackError(f"Invalid JSON in motion reference pack: {pack_path}") from exc
    validate_motion_reference_pack(data)
    return data


def validate_motion_reference_pack(pack: dict[str, Any]) -> None:
    if not isinstance(pack, dict):
        raise MotionReferencePackError("Motion reference pack must be an object")
    if pack.get("schema_version") != SUPPORTED_SCHEMA:
        raise MotionReferencePackError("Unsupported motion reference pack schema")
    if pack.get("status") not in {"draft", "reviewed", "stable"}:
        raise MotionReferencePackError("Motion reference pack status is invalid")

    sources = pack.get("sources")
    if not isinstance(sources, list) or not sources:
        raise MotionReferencePackError("Motion reference pack needs at least one source")
    source_ids: set[str] = set()
    for source in sources:
        if not isinstance(source, dict) or not _REQUIRED_SOURCE_FIELDS <= source.keys():
            raise MotionReferencePackError("Every source needs provenance and license fields")
        source_id = source["id"]
        if source_id in source_ids:
            raise MotionReferencePackError(f"Duplicate source id: {source_id}")
        source_ids.add(source_id)
        if source["provenance"] not in _ALLOWED_PROVENANCE:
            raise MotionReferencePackError(f"Invalid provenance for {source_id}")
        if source["license_status"] not in _ALLOWED_LICENSE_STATUS:
            raise MotionReferencePackError(f"Invalid license status for {source_id}")
        if source["license_status"] == "verified" and not source.get("canonical_url"):
            raise MotionReferencePackError(f"Verified source needs canonical_url: {source_id}")

    pattern_ids: set[str] = set()
    patterns = pack.get("patterns")
    if not isinstance(patterns, list) or not patterns:
        raise MotionReferencePackError("Motion reference pack needs at least one pattern")
    for pattern in patterns:
        if not isinstance(pattern, dict):
            raise MotionReferencePackError("Motion pattern must be an object")
        pattern_id = pattern.get("id")
        if not pattern_id or pattern_id in pattern_ids:
            raise MotionReferencePackError(f"Duplicate or missing pattern id: {pattern_id}")
        pattern_ids.add(pattern_id)
        if pattern.get("ontology_type") != "InteractionPattern":
            raise MotionReferencePackError(f"Pattern is not an InteractionPattern: {pattern_id}")
        if not set(pattern.get("source_ids", ())) <= source_ids:
            raise MotionReferencePackError(f"Pattern references an unknown source: {pattern_id}")
        motion = pattern.get("motion", {})
        kind = motion.get("kind", "transition")
        if kind not in _ALLOWED_MOTION_KINDS:
            raise MotionReferencePackError(f"Unknown motion kind: {pattern_id}")
        duration = motion.get("duration_ms")
        # Loops legitimately run past a second; transitions may not. Sharing one
        # ceiling previously forced loading patterns to be authored outside the
        # pack, which is how the dashboard fixture ended up with its own scale.
        ceiling = MAX_LOOP_MS if kind == "loop" else MAX_TRANSITION_MS
        if not isinstance(duration, int) or not 0 <= duration <= ceiling:
            raise MotionReferencePackError(
                f"Motion duration is outside the {kind} budget: {pattern_id}"
            )
        if motion.get("easing") not in _ALLOWED_EASINGS:
            raise MotionReferencePackError(f"Unknown easing: {pattern_id}")
        if motion.get("reduced_motion") not in _ALLOWED_REDUCED:
            raise MotionReferencePackError(f"Missing reduced-motion behavior: {pattern_id}")
        if not pattern.get("guardrails"):
            raise MotionReferencePackError(f"Pattern needs guardrails: {pattern_id}")

        # A pattern without an axis stays in the pack as governance vocabulary
        # but never enters the candidate pool.
        axis = pattern.get("axis")
        if axis is not None:
            if axis not in INTERACTION_AXES:
                raise MotionReferencePackError(f"Unknown interaction axis: {pattern_id}")
            roles = pattern.get("applies_to_roles") or []
            if not roles:
                raise MotionReferencePackError(f"Selectable pattern needs roles: {pattern_id}")
            unknown_roles = sorted(set(roles) - set(INTERACTION_ROLES))
            if unknown_roles:
                raise MotionReferencePackError(
                    f"Unknown interaction roles on {pattern_id}: {unknown_roles}"
                )

    rules = pack.get("rules")
    if not isinstance(rules, list) or not rules:
        raise MotionReferencePackError("Motion reference pack needs governance/accessibility rules")
    required_rule_ids = {"a11y:motion-reduce", "governance:reference-is-advisory"}
    rule_ids = {rule.get("id") for rule in rules if isinstance(rule, dict)}
    if not required_rule_ids <= rule_ids:
        missing = sorted(required_rule_ids - rule_ids)
        raise MotionReferencePackError(f"Required motion governance rules missing: {missing}")


def motion_pattern_ids(pack: dict[str, Any] | None = None) -> tuple[str, ...]:
    pack = pack or load_motion_reference_pack()
    return tuple(pattern["id"] for pattern in pack["patterns"])


def load_candidate_patterns(
    paths: tuple[Path, ...] = CANDIDATE_PACK_PATHS,
) -> list[dict[str, Any]]:
    """Return every selectable pattern across the candidate packs.

    Each pattern is annotated with the pack it came from so selection evidence
    can state whether a choice rests on an external reference or on a
    harness-authored baseline.
    """
    patterns: list[dict[str, Any]] = []
    seen: set[str] = set()
    for path in paths:
        pack = load_motion_reference_pack(path)
        pack_id = pack.get("pack_id", path.stem)
        licenses = {
            source["id"]: source["license_status"] for source in pack["sources"]
        }
        for pattern in pack["patterns"]:
            if pattern.get("axis") is None:
                continue
            if pattern["id"] in seen:
                raise MotionReferencePackError(
                    f"Duplicate pattern id across packs: {pattern['id']}"
                )
            seen.add(pattern["id"])
            enriched = dict(pattern)
            enriched["pack_id"] = pack_id
            enriched["license_status"] = sorted(
                {licenses.get(source_id, "unverified") for source_id in pattern.get("source_ids", ())}
            )
            patterns.append(enriched)
    return patterns
