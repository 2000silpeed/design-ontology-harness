"""Load and validate the bundled VibeCoding motion reference pack.

The pack is intentionally a small, dependency-free semantic fixture. It converts
visual inspiration into existing design-ontology concepts without treating
third-party previews as executable code or redistribution permission.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

PACK_PATH = Path(__file__).with_name("resources") / "vibecoding-motion-reference.json"
SUPPORTED_SCHEMA = "motion-reference-pack/v1"
_ALLOWED_EASINGS = {"standard", "enter", "exit", "emphasized"}
_ALLOWED_REDUCED = {"static", "opacity-only", "skip"}
_REQUIRED_SOURCE_FIELDS = {"id", "label", "canonical_url", "provenance", "license_status"}


class MotionReferencePackError(ValueError):
    """Raised when the bundled motion reference pack violates its contract."""


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
        if source["provenance"] not in {"user-supplied", "inspected", "verified"}:
            raise MotionReferencePackError(f"Invalid provenance for {source_id}")
        if source["license_status"] not in {"unverified", "reference-only", "verified"}:
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
        duration = motion.get("duration_ms")
        if not isinstance(duration, int) or not 0 <= duration <= 320:
            raise MotionReferencePackError(f"Motion duration is outside harness scale: {pattern_id}")
        if motion.get("easing") not in _ALLOWED_EASINGS:
            raise MotionReferencePackError(f"Unknown easing: {pattern_id}")
        if motion.get("reduced_motion") not in _ALLOWED_REDUCED:
            raise MotionReferencePackError(f"Missing reduced-motion behavior: {pattern_id}")
        if not pattern.get("guardrails"):
            raise MotionReferencePackError(f"Pattern needs guardrails: {pattern_id}")

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
