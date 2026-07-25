from __future__ import annotations

import hashlib
import json
import re
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


COMPONENT_RUNTIME_MANIFEST_SCHEMA = "component-runtime-manifest/v1"
COMPONENT_RUNTIME_EVIDENCE_SCHEMA = "component-runtime-evidence/v1"
LEGACY_COMPONENT_RUNTIME_MANIFEST_SCHEMA = "component-runtime-manifest/v0"
COMPONENT_RUNTIME_REPORT_SCHEMA = "component-runtime-conformance-report/v1"
DEFAULT_COMPONENT_RUNTIME_MANIFEST = Path(
    "build/system/production/component-runtime-manifest.json"
)
DEFAULT_COMPONENT_RUNTIME_EVIDENCE_ROOT = Path(
    "build/system/production/component-runtime"
)
COMPONENT_SOURCE_EXTENSIONS = {
    ".html",
    ".htm",
    ".js",
    ".mjs",
    ".cjs",
    ".ts",
    ".tsx",
    ".jsx",
    ".vue",
    ".svelte",
}


def validate_component_runtime_conformance(
    *,
    project_dir: Path,
    target_repo: Path,
    implementation_tree: dict[str, Any],
    manifest_path: Path | None = None,
    specs_path: Path | None = None,
    production_claim: bool = True,
) -> dict[str, Any]:
    """Validate explicit component-contract-to-runtime evidence.

    Production verification always calls this with ``production_claim=True``. A
    non-production caller may omit the manifest, or supply the explicit v0
    legacy marker, but the resulting report is deliberately unverified and not
    production eligible.
    """

    project = project_dir.resolve()
    target = target_repo.resolve()
    manifest = (
        manifest_path.resolve()
        if manifest_path is not None
        else project / DEFAULT_COMPONENT_RUNTIME_MANIFEST
    )
    specs = (
        specs_path.resolve()
        if specs_path is not None
        else project / "build" / "system" / "components" / "component_specs.json"
    )
    tree_sha = str(implementation_tree.get("sha256") or "")
    raw_runtime_files = implementation_tree.get("files")
    if not isinstance(raw_runtime_files, list):
        raw_runtime_files = []
    runtime_source_paths = {
        str(record.get("path") or "")
        for record in raw_runtime_files
        if isinstance(record, dict) and _required_string(record.get("path"))
    }
    latest_runtime_mtime_ns = int(
        implementation_tree.get("latest_runtime_mtime_ns") or 0
    )
    errors: list[str] = []
    warnings: list[str] = []

    if not manifest.is_file():
        if production_claim:
            errors.append(f"component runtime manifest not found: {manifest}")
        else:
            warnings.append(
                "component runtime manifest is absent; legacy compatibility is "
                "unverified and cannot support a production claim"
            )
        return _report(
            manifest=manifest,
            tree_sha=tree_sha,
            errors=errors,
            warnings=warnings,
            contract_count=0,
            mapped_component_count=0,
            verified_component_count=0,
            legacy_mode=not production_claim,
        )

    try:
        payload = _load_json_object(manifest)
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        return _report(
            manifest=manifest,
            tree_sha=tree_sha,
            errors=[str(exc)],
            warnings=[],
            contract_count=0,
            mapped_component_count=0,
            verified_component_count=0,
            legacy_mode=False,
        )

    schema_version = payload.get("schema_version")
    if schema_version == LEGACY_COMPONENT_RUNTIME_MANIFEST_SCHEMA:
        legacy_errors = _validate_legacy_manifest(payload)
        if production_claim:
            legacy_errors.append(
                "component-runtime-manifest/v0 is legacy-unverified and cannot "
                "support a production claim"
            )
        else:
            warnings.append(
                "component-runtime-manifest/v0 records legacy compatibility only; "
                "runtime conformance was not verified"
            )
        return _report(
            manifest=manifest,
            tree_sha=tree_sha,
            errors=legacy_errors,
            warnings=warnings,
            contract_count=0,
            mapped_component_count=0,
            verified_component_count=0,
            legacy_mode=True,
        )

    if schema_version != COMPONENT_RUNTIME_MANIFEST_SCHEMA:
        errors.append(
            "schema_version must be "
            f"{COMPONENT_RUNTIME_MANIFEST_SCHEMA} for runtime conformance"
        )
    if payload.get("production_claim") is not True:
        errors.append("production_claim must be true in a v1 component runtime manifest")
    if payload.get("legacy_policy") != "fail-closed":
        errors.append("legacy_policy must be fail-closed in a v1 component runtime manifest")
    if payload.get("implementation_tree_sha256") != tree_sha:
        errors.append(
            "implementation_tree_sha256 does not match the current runtime implementation"
        )
    _validate_fresh_evidence(
        checked_at=payload.get("checked_at"),
        artifact_path=manifest,
        latest_runtime_mtime_ns=latest_runtime_mtime_ns,
        prefix="manifest",
        errors=errors,
    )

    try:
        specs_payload = _load_json_object(specs)
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        errors.append(str(exc))
        specs_payload = {}
    raw_specs = specs_payload.get("specs")
    if not isinstance(raw_specs, list):
        errors.append("component_specs.specs must be a list")
        raw_specs = []

    contracts: dict[str, dict[str, Any]] = {}
    for index, contract in enumerate(raw_specs):
        prefix = f"component_specs.specs[{index}]"
        if not isinstance(contract, dict):
            errors.append(f"{prefix} must be an object")
            continue
        component_id = _required_string(contract.get("name"))
        if not component_id:
            errors.append(f"{prefix}.name is required")
            continue
        if component_id in contracts:
            errors.append(f"duplicate component contract: {component_id}")
            continue
        if contract.get("contract_status") != "complete":
            errors.append(f"{prefix} is not complete and cannot be runtime-verified")
        contracts[component_id] = contract

    raw_components = payload.get("components")
    if not isinstance(raw_components, list) or not raw_components:
        errors.append("components must be a non-empty list")
        raw_components = []

    mapped: dict[str, dict[str, Any]] = {}
    for index, record in enumerate(raw_components):
        prefix = f"components[{index}]"
        if not isinstance(record, dict):
            errors.append(f"{prefix} must be an object")
            continue
        component_id = _required_string(record.get("component_id"))
        if not component_id:
            errors.append(f"{prefix}.component_id is required")
            continue
        if component_id in mapped:
            errors.append(f"duplicate runtime component mapping: {component_id}")
            continue
        mapped[component_id] = record

    missing_components = sorted(set(contracts) - set(mapped))
    extra_components = sorted(set(mapped) - set(contracts))
    if missing_components:
        errors.append(
            "runtime manifest is missing component mappings: "
            + ", ".join(missing_components)
        )
    if extra_components:
        errors.append(
            "runtime manifest contains unknown component mappings: "
            + ", ".join(extra_components)
        )

    verified_count = 0
    for component_id in sorted(set(contracts) & set(mapped)):
        error_count_before = len(errors)
        _validate_component_mapping(
            component_id=component_id,
            contract=contracts[component_id],
            mapping=mapped[component_id],
            project=project,
            target=target,
            tree_sha=tree_sha,
            runtime_source_paths=runtime_source_paths,
            latest_runtime_mtime_ns=latest_runtime_mtime_ns,
            errors=errors,
        )
        if len(errors) == error_count_before:
            verified_count += 1

    return _report(
        manifest=manifest,
        tree_sha=tree_sha,
        errors=errors,
        warnings=warnings,
        contract_count=len(contracts),
        mapped_component_count=len(mapped),
        verified_component_count=verified_count,
        legacy_mode=False,
    )


def _validate_component_mapping(
    *,
    component_id: str,
    contract: dict[str, Any],
    mapping: dict[str, Any],
    project: Path,
    target: Path,
    tree_sha: str,
    runtime_source_paths: set[str],
    latest_runtime_mtime_ns: int,
    errors: list[str],
) -> None:
    prefix = f"component[{component_id}]"
    source_records = _load_component_sources(
        mapping.get("source_paths"),
        target=target,
        runtime_source_paths=runtime_source_paths,
        prefix=f"{prefix}.source_paths",
        errors=errors,
    )
    component_marker = mapping.get("component_marker")
    _validate_source_marker(
        component_marker,
        expected_attribute="data-component-id",
        expected_value=component_id,
        source_records=source_records,
        prefix=f"{prefix}.component_marker",
        errors=errors,
    )

    anatomy = _object(contract.get("anatomy"))
    expected_parts = set(_string_list(anatomy.get("parts")))
    part_markers = mapping.get("part_markers")
    if not isinstance(part_markers, list):
        errors.append(f"{prefix}.part_markers must be a list")
        part_markers = []
    seen_parts: set[str] = set()
    for index, marker in enumerate(part_markers):
        marker_prefix = f"{prefix}.part_markers[{index}]"
        part = _required_string(marker.get("part")) if isinstance(marker, dict) else ""
        if not part:
            errors.append(f"{marker_prefix}.part is required")
            continue
        if part in seen_parts:
            errors.append(f"{marker_prefix}.part duplicates {part}")
        seen_parts.add(part)
        _validate_source_marker(
            marker,
            expected_attribute="data-component-part",
            expected_value=part,
            source_records=source_records,
            prefix=marker_prefix,
            errors=errors,
        )
    missing_parts = sorted(expected_parts - seen_parts)
    unknown_parts = sorted(seen_parts - expected_parts)
    if missing_parts:
        errors.append(f"{prefix} is missing anatomy part markers: {', '.join(missing_parts)}")
    if unknown_parts:
        errors.append(f"{prefix} declares unknown anatomy part markers: {', '.join(unknown_parts)}")

    artifact = _load_component_evidence(
        mapping.get("evidence"),
        project=project,
        prefix=f"{prefix}.evidence",
        errors=errors,
    )
    if not artifact:
        return
    if artifact.get("schema_version") != COMPONENT_RUNTIME_EVIDENCE_SCHEMA:
        errors.append(
            f"{prefix}.evidence schema_version must be {COMPONENT_RUNTIME_EVIDENCE_SCHEMA}"
        )
    if artifact.get("component_id") != component_id:
        errors.append(f"{prefix}.evidence component_id does not match")
    if artifact.get("implementation_tree_sha256") != tree_sha:
        errors.append(
            f"{prefix}.evidence implementation_tree_sha256 does not match the runtime implementation"
        )
    artifact_path = artifact.get("_artifact_path")
    if isinstance(artifact_path, Path):
        _validate_fresh_evidence(
            checked_at=artifact.get("checked_at"),
            artifact_path=artifact_path,
            latest_runtime_mtime_ns=latest_runtime_mtime_ns,
            prefix=f"{prefix}.evidence",
            errors=errors,
        )

    dom = artifact.get("dom")
    if not isinstance(dom, dict):
        errors.append(f"{prefix}.evidence.dom must be an object")
        dom = {}
    if _marker_identity(dom.get("component_marker")) != _marker_identity(component_marker):
        errors.append(f"{prefix}.evidence DOM component marker does not match the manifest")
    evidence_part_markers = dom.get("part_markers")
    if _part_marker_identities(evidence_part_markers) != _part_marker_identities(part_markers):
        errors.append(f"{prefix}.evidence DOM part markers do not match the manifest")

    _validate_state_scenarios(
        artifact.get("state_scenarios"),
        contract=contract,
        prefix=f"{prefix}.evidence.state_scenarios",
        errors=errors,
    )
    _validate_interaction_scenarios(
        artifact.get("interaction_scenarios"),
        contract=contract,
        prefix=f"{prefix}.evidence.interaction_scenarios",
        errors=errors,
    )
    _validate_responsive_scenarios(
        artifact.get("responsive_scenarios"),
        contract=contract,
        prefix=f"{prefix}.evidence.responsive_scenarios",
        errors=errors,
    )
    _validate_contract_coverage(
        artifact.get("contract_coverage"),
        contract=contract,
        prefix=f"{prefix}.evidence.contract_coverage",
        errors=errors,
    )


def _load_component_sources(
    value: Any,
    *,
    target: Path,
    runtime_source_paths: set[str],
    prefix: str,
    errors: list[str],
) -> dict[str, dict[str, Any]]:
    if not isinstance(value, list) or not value:
        errors.append(f"{prefix} must be a non-empty list")
        return {}
    records: dict[str, dict[str, Any]] = {}
    for index, record in enumerate(value):
        record_prefix = f"{prefix}[{index}]"
        if not isinstance(record, dict):
            errors.append(f"{record_prefix} must be an object")
            continue
        raw_path = _required_string(record.get("path"))
        if not raw_path:
            errors.append(f"{record_prefix}.path is required")
            continue
        path = _resolve_relative_path(
            root=target,
            raw_path=raw_path,
            prefix=f"{record_prefix}.path",
            errors=errors,
        )
        if path is None:
            continue
        relative = path.relative_to(target).as_posix()
        if relative in records:
            errors.append(f"{record_prefix}.path duplicates {relative}")
            continue
        if path.suffix.lower() not in COMPONENT_SOURCE_EXTENSIONS:
            errors.append(
                f"{record_prefix}.path must identify a runtime component source file"
            )
        if relative not in runtime_source_paths:
            errors.append(
                f"{record_prefix}.path is not included in the current runtime implementation tree"
            )
        if not path.is_file():
            errors.append(f"{record_prefix}.path does not exist: {relative}")
            continue
        expected_sha = _required_string(record.get("sha256"))
        actual_sha = _sha256(path)
        if not re.fullmatch(r"[a-f0-9]{64}", expected_sha):
            errors.append(f"{record_prefix}.sha256 must be a lowercase SHA-256 digest")
        elif expected_sha != actual_sha:
            errors.append(f"{record_prefix}.sha256 does not match {relative}")
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            errors.append(f"{record_prefix}.path must be UTF-8 text: {relative}")
            text = ""
        records[relative] = {"path": path, "sha256": actual_sha, "text": text}
    return records


def _validate_source_marker(
    marker: Any,
    *,
    expected_attribute: str,
    expected_value: str,
    source_records: dict[str, dict[str, Any]],
    prefix: str,
    errors: list[str],
) -> None:
    if not isinstance(marker, dict):
        errors.append(f"{prefix} must be an object")
        return
    source_path = _required_string(marker.get("source_path"))
    attribute = _required_string(marker.get("attribute"))
    value = _required_string(marker.get("value"))
    if attribute != expected_attribute:
        errors.append(f"{prefix}.attribute must be {expected_attribute}")
    if value != expected_value:
        errors.append(f"{prefix}.value must be {expected_value}")
    source = source_records.get(source_path)
    if source is None:
        errors.append(f"{prefix}.source_path must reference a declared source path")
        return
    if attribute != expected_attribute or value != expected_value:
        return
    pattern = re.compile(
        rf"(?<![A-Za-z0-9_-]){re.escape(attribute)}\s*=\s*([\"']){re.escape(value)}\1"
    )
    if pattern.search(str(source.get("text") or "")) is None:
        errors.append(
            f"{prefix} is not present as an exact quoted DOM marker in {source_path}"
        )


def _load_component_evidence(
    reference: Any,
    *,
    project: Path,
    prefix: str,
    errors: list[str],
) -> dict[str, Any]:
    if not isinstance(reference, dict):
        errors.append(f"{prefix} must be an object")
        return {}
    raw_path = _required_string(reference.get("path"))
    if not raw_path:
        errors.append(f"{prefix}.path is required")
        return {}
    path = _resolve_relative_path(
        root=project,
        raw_path=raw_path,
        prefix=f"{prefix}.path",
        errors=errors,
    )
    if path is None:
        return {}
    evidence_root = (project / DEFAULT_COMPONENT_RUNTIME_EVIDENCE_ROOT).resolve()
    if not path.is_relative_to(evidence_root):
        errors.append(
            f"{prefix}.path must be under {DEFAULT_COMPONENT_RUNTIME_EVIDENCE_ROOT.as_posix()}"
        )
    if not path.is_file():
        errors.append(f"{prefix}.path does not exist: {raw_path}")
        return {}
    declared_sha = _required_string(reference.get("sha256"))
    actual_sha = _sha256(path)
    if not re.fullmatch(r"[a-f0-9]{64}", declared_sha):
        errors.append(f"{prefix}.sha256 must be a lowercase SHA-256 digest")
    elif declared_sha != actual_sha:
        errors.append(f"{prefix}.sha256 does not match the evidence artifact")
        return {}
    try:
        artifact = _load_json_object(path)
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        errors.append(str(exc))
        return {}
    artifact["_artifact_path"] = path
    return artifact


def _validate_state_scenarios(
    value: Any,
    *,
    contract: dict[str, Any],
    prefix: str,
    errors: list[str],
) -> None:
    state_model = _object(contract.get("state_model"))
    expected_states = set(_string_list(state_model.get("all_states")))
    if not isinstance(value, list) or not value:
        errors.append(f"{prefix} must be a non-empty list")
        value = []
    covered: set[str] = set()
    scenario_ids: set[str] = set()
    for index, scenario in enumerate(value):
        scenario_prefix = f"{prefix}[{index}]"
        if not isinstance(scenario, dict):
            errors.append(f"{scenario_prefix} must be an object")
            continue
        _validate_scenario_id(scenario, scenario_ids, scenario_prefix, errors)
        state = _required_string(scenario.get("state"))
        route = _required_string(scenario.get("route"))
        if not state:
            errors.append(f"{scenario_prefix}.state is required")
        else:
            covered.add(state)
        if not route:
            errors.append(f"{scenario_prefix}.route is required")
        marker = scenario.get("observed_marker")
        if not isinstance(marker, dict):
            errors.append(f"{scenario_prefix}.observed_marker must be an object")
        else:
            if marker.get("attribute") != "data-component-state":
                errors.append(
                    f"{scenario_prefix}.observed_marker.attribute must be data-component-state"
                )
            if marker.get("value") != state:
                errors.append(
                    f"{scenario_prefix}.observed_marker.value must match the state"
                )
        if not _all_assertions_pass(scenario.get("assertions")):
            errors.append(f"{scenario_prefix}.assertions must be non-empty and all pass")
    missing = sorted(expected_states - covered)
    unknown = sorted(covered - expected_states)
    if missing:
        errors.append(f"{prefix} does not cover states: {', '.join(missing)}")
    if unknown:
        errors.append(f"{prefix} contains unknown states: {', '.join(unknown)}")


def _validate_interaction_scenarios(
    value: Any,
    *,
    contract: dict[str, Any],
    prefix: str,
    errors: list[str],
) -> None:
    interaction = _object(contract.get("interaction"))
    expected_events = set(_string_list(interaction.get("events")))
    raw_transitions = interaction.get("state_transitions")
    if not isinstance(raw_transitions, list):
        raw_transitions = []
    expected_transitions = {
        _contract_item_key(item)
        for item in raw_transitions
        if isinstance(item, str | dict)
    }
    if not isinstance(value, list) or not value:
        errors.append(f"{prefix} must be a non-empty list")
        value = []
    covered_events: set[str] = set()
    covered_transitions: set[str] = set()
    scenario_ids: set[str] = set()
    for index, scenario in enumerate(value):
        scenario_prefix = f"{prefix}[{index}]"
        if not isinstance(scenario, dict):
            errors.append(f"{scenario_prefix} must be an object")
            continue
        _validate_scenario_id(scenario, scenario_ids, scenario_prefix, errors)
        event = _required_string(scenario.get("event"))
        route = _required_string(scenario.get("route"))
        if not event:
            errors.append(f"{scenario_prefix}.event is required")
        else:
            covered_events.add(event)
        if not route:
            errors.append(f"{scenario_prefix}.route is required")
        if not _all_assertions_pass(scenario.get("assertions")):
            errors.append(f"{scenario_prefix}.assertions must be non-empty and all pass")
        if not _all_assertions_pass(scenario.get("focus_assertions")):
            errors.append(
                f"{scenario_prefix}.focus_assertions must be non-empty and all pass"
            )
        transition = scenario.get("transition")
        if transition is not None:
            if not isinstance(transition, str | dict):
                errors.append(f"{scenario_prefix}.transition must be a string or object")
            else:
                if (
                    isinstance(transition, dict)
                    and _required_string(transition.get("event"))
                    and transition.get("event") != event
                ):
                    errors.append(
                        f"{scenario_prefix}.transition event must match the scenario event"
                    )
                covered_transitions.add(_contract_item_key(transition))
    missing_events = sorted(expected_events - covered_events)
    unknown_events = sorted(covered_events - expected_events)
    missing_transitions = sorted(expected_transitions - covered_transitions)
    unknown_transitions = sorted(covered_transitions - expected_transitions)
    if missing_events:
        errors.append(f"{prefix} does not cover events: {', '.join(missing_events)}")
    if unknown_events:
        errors.append(f"{prefix} contains unknown events: {', '.join(unknown_events)}")
    if missing_transitions:
        errors.append(
            f"{prefix} does not cover contract transitions: {len(missing_transitions)} missing"
        )
    if unknown_transitions:
        errors.append(
            f"{prefix} contains transitions outside the contract: {len(unknown_transitions)}"
        )


def _validate_responsive_scenarios(
    value: Any,
    *,
    contract: dict[str, Any],
    prefix: str,
    errors: list[str],
) -> None:
    responsive = _object(contract.get("responsive"))
    raw_widths = responsive.get("required_widths_px")
    if not isinstance(raw_widths, list):
        raw_widths = []
    expected_widths = {
        width
        for width in raw_widths
        if isinstance(width, int) and not isinstance(width, bool)
    }
    expected_rules = set(_string_list(responsive.get("control_rules")))
    expected_container = _required_string(responsive.get("container_behavior"))
    if not isinstance(value, list) or not value:
        errors.append(f"{prefix} must be a non-empty list")
        value = []
    covered_widths: set[int] = set()
    covered_rules: set[str] = set()
    scenario_ids: set[str] = set()
    for index, scenario in enumerate(value):
        scenario_prefix = f"{prefix}[{index}]"
        if not isinstance(scenario, dict):
            errors.append(f"{scenario_prefix} must be an object")
            continue
        _validate_scenario_id(scenario, scenario_ids, scenario_prefix, errors)
        width = scenario.get("width_px")
        if not isinstance(width, int) or isinstance(width, bool) or width <= 0:
            errors.append(f"{scenario_prefix}.width_px must be a positive integer")
        else:
            covered_widths.add(width)
        if not _all_assertions_pass(scenario.get("assertions")):
            errors.append(f"{scenario_prefix}.assertions must be non-empty and all pass")
        covered_rules.update(_string_list(scenario.get("covered_rules")))
        if scenario.get("container_behavior") != expected_container:
            errors.append(
                f"{scenario_prefix}.container_behavior must match the component contract"
            )
    missing_widths = sorted(expected_widths - covered_widths)
    missing_rules = sorted(expected_rules - covered_rules)
    unknown_rules = sorted(covered_rules - expected_rules)
    if missing_widths:
        errors.append(
            f"{prefix} does not cover required widths: "
            + ", ".join(str(width) for width in missing_widths)
        )
    if missing_rules:
        errors.append(f"{prefix} does not cover control rules: {len(missing_rules)} missing")
    if unknown_rules:
        errors.append(
            f"{prefix} contains control rules outside the contract: {len(unknown_rules)}"
        )


def _validate_contract_coverage(
    value: Any,
    *,
    contract: dict[str, Any],
    prefix: str,
    errors: list[str],
) -> None:
    if not isinstance(value, dict):
        errors.append(f"{prefix} must be an object")
        value = {}
    data_contract = _object(contract.get("data_contract"))
    variants = _object(contract.get("variants"))
    dos_and_donts = _object(contract.get("dos_and_donts"))
    props = _object(contract.get("props"))
    expected_sets = {
        "props": set(props),
        "data_fields": set(_string_list(data_contract.get("required_fields"))),
        "content_rules": set(_string_list(contract.get("content_rules"))),
        "accessibility_rules": set(_string_list(contract.get("accessibility"))),
        "do_rules": set(_string_list(dos_and_donts.get("do"))),
        "dont_rules": set(_string_list(dos_and_donts.get("dont"))),
        "variant_axes": set(_string_list(variants.get("axes"))),
    }
    for field, expected in expected_sets.items():
        actual = set(_string_list(value.get(field)))
        missing = expected - actual
        unknown = actual - expected
        if missing:
            errors.append(f"{prefix}.{field} is missing {len(missing)} contract item(s)")
        if unknown:
            errors.append(f"{prefix}.{field} contains {len(unknown)} unknown item(s)")
    if value.get("default_variant") != variants.get("default"):
        errors.append(f"{prefix}.default_variant must match the component contract")
    if data_contract.get("provenance_required") is True and value.get(
        "provenance_observed"
    ) is not True:
        errors.append(f"{prefix}.provenance_observed must be true")
    if data_contract.get("empty_state_required") is True and value.get(
        "empty_state_observed"
    ) is not True:
        errors.append(f"{prefix}.empty_state_observed must be true")


def _validate_fresh_evidence(
    *,
    checked_at: Any,
    artifact_path: Path,
    latest_runtime_mtime_ns: int,
    prefix: str,
    errors: list[str],
) -> None:
    checked_ns = _timestamp_ns(checked_at)
    if checked_ns is None:
        errors.append(f"{prefix}.checked_at must be an ISO-8601 timestamp with a timezone")
    elif checked_ns < latest_runtime_mtime_ns:
        errors.append(f"{prefix}.checked_at is older than the runtime implementation")
    if artifact_path.stat().st_mtime_ns < latest_runtime_mtime_ns:
        errors.append(f"{prefix} file is older than the runtime implementation")


def _validate_legacy_manifest(payload: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    if payload.get("mode") != "legacy-unverified":
        errors.append("legacy component runtime manifest mode must be legacy-unverified")
    if payload.get("production_eligible") is not False:
        errors.append("legacy component runtime manifest production_eligible must be false")
    return errors


def _report(
    *,
    manifest: Path,
    tree_sha: str,
    errors: list[str],
    warnings: list[str],
    contract_count: int,
    mapped_component_count: int,
    verified_component_count: int,
    legacy_mode: bool,
) -> dict[str, Any]:
    verified = not errors and not legacy_mode
    return {
        "schema_version": COMPONENT_RUNTIME_REPORT_SCHEMA,
        "ok": not errors,
        "verified": verified,
        "production_eligible": verified,
        "legacy_mode": legacy_mode,
        "manifest_path": str(manifest),
        "implementation_tree_sha256": tree_sha,
        "contract_count": contract_count,
        "mapped_component_count": mapped_component_count,
        "verified_component_count": verified_component_count,
        "errors": errors,
        "warnings": warnings,
    }


def _load_json_object(path: Path) -> dict[str, Any]:
    if not path.is_file():
        raise ValueError(f"required JSON evidence not found: {path}")
    payload = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ValueError(f"JSON evidence must be an object: {path}")
    return payload


def _resolve_relative_path(
    *, root: Path, raw_path: str, prefix: str, errors: list[str]
) -> Path | None:
    if Path(raw_path).is_absolute():
        errors.append(f"{prefix} must be relative")
        return None
    path = (root / raw_path).resolve()
    if not path.is_relative_to(root):
        errors.append(f"{prefix} escapes its evidence root")
        return None
    return path


def _validate_scenario_id(
    scenario: dict[str, Any],
    seen: set[str],
    prefix: str,
    errors: list[str],
) -> None:
    scenario_id = _required_string(scenario.get("scenario_id"))
    if not scenario_id:
        errors.append(f"{prefix}.scenario_id is required")
    elif scenario_id in seen:
        errors.append(f"{prefix}.scenario_id duplicates {scenario_id}")
    seen.add(scenario_id)


def _marker_identity(value: Any) -> tuple[str, str, str] | None:
    if not isinstance(value, dict):
        return None
    return (
        _required_string(value.get("source_path")),
        _required_string(value.get("attribute")),
        _required_string(value.get("value")),
    )


def _part_marker_identities(value: Any) -> set[tuple[str, str, str, str]]:
    if not isinstance(value, list):
        return set()
    return {
        (
            _required_string(marker.get("part")),
            _required_string(marker.get("source_path")),
            _required_string(marker.get("attribute")),
            _required_string(marker.get("value")),
        )
        for marker in value
        if isinstance(marker, dict)
    }


def _contract_item_key(value: str | dict[str, Any]) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def _all_assertions_pass(value: Any) -> bool:
    return (
        isinstance(value, list)
        and bool(value)
        and all(
            isinstance(assertion, dict)
            and _required_string(assertion.get("id"))
            and assertion.get("passed") is True
            for assertion in value
        )
    )


def _timestamp_ns(value: Any) -> int | None:
    if not isinstance(value, str) or not value.strip():
        return None
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        return None
    if parsed.tzinfo is None:
        return None
    return int(parsed.astimezone(timezone.utc).timestamp() * 1_000_000_000)


def _required_string(value: Any) -> str:
    return value.strip() if isinstance(value, str) else ""


def _object(value: Any) -> dict[str, Any]:
    return value if isinstance(value, dict) else {}


def _string_list(value: Any) -> list[str]:
    if not isinstance(value, list):
        return []
    return [item.strip() for item in value if isinstance(item, str) and item.strip()]


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()
