from __future__ import annotations

import re
from pathlib import Path
from typing import Any


TOKEN_REFERENCE_RE = re.compile(r"var\(\s*(--[a-zA-Z0-9-]+)")
TOKEN_DECLARATION_RE = re.compile(r"(?m)^\s*(--ds-[a-zA-Z0-9-]+)\s*:")
REQUIRED_SPEC_FIELDS = {
    "name",
    "family",
    "contract_version",
    "contract_status",
    "contract_provenance",
    "anatomy",
    "state_model",
    "variants",
    "props",
    "interaction",
    "data_contract",
    "responsive",
    "content_rules",
    "dos_and_donts",
    "tokens",
    "accessibility",
}
CONTRACT_VERSION = "component-contract/v1"
CONTRACT_STATUSES = {"complete", "needs-authoring"}
PRIMITIVE_RECONCILIATION_VERSION = "product-primitive-reconciliation/v1"


def _non_empty_string(value: Any) -> bool:
    return isinstance(value, str) and bool(value.strip())


def _string_list(value: Any) -> list[str]:
    if not isinstance(value, list):
        return []
    return [item.strip() for item in value if isinstance(item, str) and item.strip()]


def _validate_authored_token_bindings(
    spec: dict[str, Any],
    *,
    prefix: str,
    errors: list[str],
) -> None:
    if spec.get("token_provenance") != "authored-input":
        errors.append(f"{prefix}.token_provenance must be authored-input")
    tokens = spec.get("tokens")
    if not isinstance(tokens, dict) or not tokens:
        return
    anatomy = spec.get("anatomy") if isinstance(spec.get("anatomy"), dict) else {}
    parts = set(_string_list(anatomy.get("parts")))
    states = set(_string_list(anatomy.get("states")))
    targeted_parts: set[str] = set()
    targeted_states: set[str] = set()
    for slot, value in tokens.items():
        slot_prefix = f"{prefix}.tokens.{slot}"
        if not isinstance(slot, str):
            errors.append(f"{prefix}.tokens slot names must be strings")
            continue
        segments = slot.split(".")
        if len(segments) < 3 or segments[0] not in {"component", "part", "state"}:
            errors.append(f"{slot_prefix} has an invalid authored target")
            continue
        scope, target = segments[0], segments[1]
        if scope == "part":
            targeted_parts.add(target)
            if target not in parts:
                errors.append(f"{slot_prefix} targets unknown anatomy part {target}")
        elif scope == "state":
            targeted_states.add(target)
            if target not in states:
                errors.append(f"{slot_prefix} targets unknown state {target}")
        if not isinstance(value, str) or re.search(
            r"var\(\s*--ds-[a-zA-Z0-9-]+", value
        ) is None:
            errors.append(f"{slot_prefix} must reference an emitted --ds-* token")
    if not targeted_parts:
        errors.append(f"{prefix}.tokens must target at least one anatomy part")
    if not targeted_states:
        errors.append(f"{prefix}.tokens must target at least one state")


def _validate_primitive_reconciliation(
    specs_data: dict[str, Any],
    *,
    specs_by_name: dict[str, dict[str, Any]],
    errors: list[str],
) -> tuple[int, int]:
    expected = _string_list(specs_data.get("product_primitives"))
    if len(expected) != len(set(expected)):
        errors.append("product_primitives must not contain duplicates")
    if specs_data.get("primitive_reconciliation_version") != PRIMITIVE_RECONCILIATION_VERSION:
        errors.append(
            "primitive_reconciliation_version must be "
            f"{PRIMITIVE_RECONCILIATION_VERSION} for authored contracts"
        )
    records = specs_data.get("primitive_reconciliation")
    if not isinstance(records, list):
        errors.append("primitive_reconciliation must be a list for authored contracts")
        records = []
    seen: set[str] = set()
    waivers = 0
    for index, record in enumerate(records):
        prefix = f"primitive_reconciliation[{index}]"
        if not isinstance(record, dict):
            errors.append(f"{prefix} must be an object")
            continue
        primitive = str(record.get("primitive") or "").strip()
        if not primitive:
            errors.append(f"{prefix}.primitive is required")
            continue
        if primitive in seen:
            errors.append(f"{prefix}.primitive duplicates {primitive}")
        seen.add(primitive)
        resolution = record.get("resolution")
        reason = str(record.get("reason") or "").strip()
        if resolution not in {"component", "anatomy", "waiver"}:
            errors.append(f"{prefix}.resolution must be component, anatomy, or waiver")
            continue
        if not reason:
            errors.append(f"{prefix}.reason is required")
        if resolution == "waiver":
            waivers += 1
            if len(reason) < 16:
                errors.append(f"{prefix}.reason must substantiate the waiver")
            if record.get("component") or record.get("anatomy_parts"):
                errors.append(f"{prefix} waiver must not claim runtime coverage")
            waiver = record.get("waiver")
            if not isinstance(waiver, dict):
                errors.append(f"{prefix}.waiver must be a structured object")
                continue
            for field in ("kind", "decision_source"):
                if not _non_empty_string(waiver.get(field)):
                    errors.append(f"{prefix}.waiver.{field} is required")
            if waiver.get("approval_status") != "approved":
                errors.append(f"{prefix}.waiver.approval_status must be approved")
            replacements = _string_list(waiver.get("replacement_components"))
            if not replacements:
                errors.append(
                    f"{prefix}.waiver.replacement_components must not be empty"
                )
            unknown_replacements = sorted(set(replacements) - set(specs_by_name))
            if unknown_replacements:
                errors.append(
                    f"{prefix}.waiver.replacement_components contains unknown components: "
                    + ", ".join(unknown_replacements)
                )
            continue
        component_name = str(record.get("component") or "").strip()
        component = specs_by_name.get(component_name)
        if component is None:
            errors.append(f"{prefix}.component is not an authored contract")
            continue
        if resolution == "anatomy":
            anatomy_parts = _string_list(record.get("anatomy_parts"))
            if not anatomy_parts:
                errors.append(f"{prefix}.anatomy_parts must not be empty")
            available = set(
                _string_list(
                    (component.get("anatomy") or {}).get("parts")
                    if isinstance(component.get("anatomy"), dict)
                    else []
                )
            )
            unknown = sorted(set(anatomy_parts) - available)
            if unknown:
                errors.append(
                    f"{prefix}.anatomy_parts contains unknown parts: "
                    + ", ".join(unknown)
                )
    missing = sorted(set(expected) - seen)
    unknown = sorted(seen - set(expected))
    if missing:
        errors.append("primitive_reconciliation is missing: " + ", ".join(missing))
    if unknown:
        errors.append(
            "primitive_reconciliation contains unknown primitives: "
            + ", ".join(unknown)
        )
    return len(seen), waivers


def validate_component_contracts(
    specs_data: dict[str, Any],
    *,
    token_css: str | None = None,
    strict_authored: bool = True,
) -> dict[str, Any]:
    errors: list[str] = []
    warnings: list[str] = []
    specs = specs_data.get("specs")
    if not isinstance(specs, list):
        return {
            "ok": False,
            "errors": ["component_specs.specs must be a list"],
            "warnings": [],
            "component_count": 0,
            "needs_authoring_count": 0,
        }

    declared_tokens = set(TOKEN_DECLARATION_RE.findall(token_css or ""))
    seen_names: set[str] = set()
    authored_specs_by_name: dict[str, dict[str, Any]] = {}
    authored_contract_count = 0
    needs_authoring = 0
    for index, spec in enumerate(specs):
        prefix = f"specs[{index}]"
        if not isinstance(spec, dict):
            errors.append(f"{prefix} must be an object")
            continue
        name = str(spec.get("name") or "")
        if not name:
            errors.append(f"{prefix}.name is required")
        elif name in seen_names:
            errors.append(f"duplicate component contract: {name}")
        seen_names.add(name)
        missing = sorted(REQUIRED_SPEC_FIELDS - set(spec))
        if missing:
            errors.append(f"{prefix} missing fields: {', '.join(missing)}")

        if spec.get("contract_version") != CONTRACT_VERSION:
            errors.append(f"{prefix}.contract_version must be {CONTRACT_VERSION}")
        status = spec.get("contract_status")
        if status not in CONTRACT_STATUSES:
            errors.append(f"{prefix}.contract_status must be complete or needs-authoring")
        provenance = spec.get("contract_provenance")
        if not _non_empty_string(provenance):
            errors.append(f"{prefix}.contract_provenance must not be empty")
        is_complete = status == "complete"
        if is_complete and spec.get("contract_issues"):
            errors.append(f"{prefix}.contract_issues must be empty when contract_status is complete")

        anatomy = spec.get("anatomy") or {}
        parts = anatomy.get("parts") if isinstance(anatomy, dict) else None
        states = anatomy.get("states") if isinstance(anatomy, dict) else None
        if not _string_list(parts):
            errors.append(f"{prefix}.anatomy.parts must not be empty")
        if not _string_list(states):
            errors.append(f"{prefix}.anatomy.states must not be empty")

        state_model = spec.get("state_model") or {}
        if not isinstance(state_model, dict):
            errors.append(f"{prefix}.state_model must be a structured object")
            state_model = {}
        for field in ("domain_states", "interaction_states", "all_states"):
            if not isinstance(state_model.get(field), list):
                errors.append(f"{prefix}.state_model.{field} must be a list")
        domain_states = _string_list(state_model.get("domain_states"))
        interaction_states = _string_list(state_model.get("interaction_states"))
        all_states = _string_list(state_model.get("all_states"))
        if is_complete and not domain_states:
            errors.append(f"{prefix}.state_model.domain_states must not be empty for complete contracts")
        if any(state not in (states or []) for state in domain_states):
            errors.append(f"{prefix} loses authored domain states in anatomy.states")
        if any(state not in all_states for state in domain_states):
            errors.append(f"{prefix} loses authored domain states in state_model.all_states")
        if any(state not in all_states for state in interaction_states):
            errors.append(f"{prefix} loses interaction states in state_model.all_states")

        if status == "needs-authoring":
            needs_authoring += 1
            details = "; ".join(spec.get("contract_issues") or ["authoring fields incomplete"])
            message = f"{name or prefix} needs component authoring: {details}"
            if strict_authored:
                errors.append(message)
            else:
                warnings.append(message)

        if provenance == "llm-authored":
            authored_contract_count += 1
            if name:
                authored_specs_by_name[name] = spec
            if not spec.get("supports_primitive"):
                errors.append(f"{prefix}.supports_primitive is required for authored components")
            if is_complete and not domain_states:
                errors.append(f"{prefix}.state_model.domain_states is required for authored components")
            if is_complete or strict_authored:
                _validate_authored_token_bindings(spec, prefix=prefix, errors=errors)

        for field in ("variants", "props", "interaction", "data_contract", "responsive"):
            if not isinstance(spec.get(field), dict):
                errors.append(f"{prefix}.{field} must be a structured object")

        variants = spec.get("variants") if isinstance(spec.get("variants"), dict) else {}
        props = spec.get("props") if isinstance(spec.get("props"), dict) else {}
        interaction = spec.get("interaction") if isinstance(spec.get("interaction"), dict) else {}
        data_contract = spec.get("data_contract") if isinstance(spec.get("data_contract"), dict) else {}
        responsive = spec.get("responsive") if isinstance(spec.get("responsive"), dict) else {}
        content_rules = spec.get("content_rules")
        dos_and_donts = spec.get("dos_and_donts")
        accessibility = spec.get("accessibility")

        if not isinstance(content_rules, list):
            errors.append(f"{prefix}.content_rules must be a list")
        if not isinstance(dos_and_donts, dict):
            errors.append(f"{prefix}.dos_and_donts must be a structured object")
            dos_and_donts = {}
        if not isinstance(accessibility, list):
            errors.append(f"{prefix}.accessibility must be a list")

        if is_complete:
            if not props:
                errors.append(f"{prefix}.props must not be empty for complete contracts")
            if not _non_empty_string(variants.get("default")):
                errors.append(f"{prefix}.variants.default is required for complete contracts")
            if not isinstance(variants.get("axes"), list):
                errors.append(f"{prefix}.variants.axes must be a list")
            if not isinstance(variants.get("constraints"), list):
                errors.append(f"{prefix}.variants.constraints must be a list")

            events = _string_list(interaction.get("events"))
            if not events:
                errors.append(f"{prefix}.interaction.events must not be empty for complete contracts")
            if not isinstance(interaction.get("state_transitions"), list):
                errors.append(f"{prefix}.interaction.state_transitions must be a list")
            if not _non_empty_string(interaction.get("focus_behavior")):
                errors.append(f"{prefix}.interaction.focus_behavior is required for complete contracts")
            state_coverage = _string_list(interaction.get("state_coverage"))
            if not state_coverage:
                errors.append(f"{prefix}.interaction.state_coverage must not be empty for complete contracts")
            elif any(state not in state_coverage for state in domain_states):
                errors.append(f"{prefix}.interaction.state_coverage must include every domain state")

            if not _non_empty_string(data_contract.get("domain_object")):
                errors.append(f"{prefix}.data_contract.domain_object is required for complete contracts")
            if not _string_list(data_contract.get("required_fields")):
                errors.append(f"{prefix}.data_contract.required_fields must not be empty for complete contracts")
            for field in ("provenance_required", "empty_state_required"):
                if not isinstance(data_contract.get(field), bool):
                    errors.append(f"{prefix}.data_contract.{field} must be a boolean")

            widths = responsive.get("required_widths_px")
            if not isinstance(widths, list) or not widths or any(
                not isinstance(width, int) or isinstance(width, bool) or width <= 0 for width in widths
            ):
                errors.append(f"{prefix}.responsive.required_widths_px must contain positive integers")
            if not _string_list(responsive.get("control_rules")):
                errors.append(f"{prefix}.responsive.control_rules must not be empty for complete contracts")
            if not _non_empty_string(responsive.get("container_behavior")):
                errors.append(f"{prefix}.responsive.container_behavior is required for complete contracts")

            if not _string_list(content_rules):
                errors.append(f"{prefix}.content_rules must not be empty for complete contracts")
            if not _string_list(dos_and_donts.get("do")):
                errors.append(f"{prefix}.dos_and_donts.do must not be empty for complete contracts")
            if not _string_list(dos_and_donts.get("dont")):
                errors.append(f"{prefix}.dos_and_donts.dont must not be empty for complete contracts")
            if not _string_list(accessibility):
                errors.append(f"{prefix}.accessibility must not be empty for complete contracts")

        tokens = spec.get("tokens") or {}
        if not isinstance(tokens, dict) or not tokens:
            message = f"{prefix}.tokens must not be empty"
            if (
                provenance == "llm-authored"
                and status == "needs-authoring"
                and not strict_authored
            ):
                warnings.append(message)
            else:
                errors.append(message)
            continue
        for slot, value in tokens.items():
            for token in TOKEN_REFERENCE_RE.findall(str(value)):
                if not token.startswith("--ds-"):
                    errors.append(f"{prefix}.tokens.{slot} uses legacy token {token}")
                elif token_css is not None and token not in declared_tokens:
                    errors.append(f"{prefix}.tokens.{slot} references missing emitted token {token}")

    reconciliation_count = 0
    waiver_count = 0
    if authored_contract_count:
        reconciliation_count, waiver_count = _validate_primitive_reconciliation(
            specs_data,
            specs_by_name=authored_specs_by_name,
            errors=errors,
        )

    if token_css is None:
        warnings.append("tokens.css was not supplied; emitted token resolution was not verified")
    return {
        "ok": not errors,
        "errors": errors,
        "warnings": warnings,
        "component_count": len(specs),
        "needs_authoring_count": needs_authoring,
        "declared_token_count": len(declared_tokens),
        "authored_contract_count": authored_contract_count,
        "primitive_reconciliation_count": reconciliation_count,
        "primitive_waiver_count": waiver_count,
    }


def load_and_validate_component_contracts(
    specs_path: Path,
    *,
    tokens_path: Path | None = None,
    strict_authored: bool = True,
) -> dict[str, Any]:
    import json

    if not specs_path.is_file():
        raise ValueError(f"component specs not found: {specs_path}")
    payload = json.loads(specs_path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ValueError("component specs must be a JSON object")
    token_css = None
    if tokens_path is not None:
        if not tokens_path.is_file():
            raise ValueError(f"emitted tokens not found: {tokens_path}")
        token_css = tokens_path.read_text(encoding="utf-8")
    return validate_component_contracts(
        payload,
        token_css=token_css,
        strict_authored=strict_authored,
    )
