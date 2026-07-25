from __future__ import annotations

import hashlib
import json
import math
import re
import shutil
from copy import deepcopy
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from PIL import Image, UnidentifiedImageError

from .graph_builders import (
    VISUAL_ASSET_GENERATION_PROVENANCE_VERSION,
    VISUAL_ASSET_MANIFEST_SCHEMA,
    VISUAL_IMAGE_GENERATOR_ID,
)
from .utils import slugify, write_json


SUPPORTED_FORMATS = {"PNG", "JPEG", "WEBP"}
FINAL_STATUSES = {"accepted", "integrated"}
PROMPT_CONTRACT_MIGRATION_SCHEMA = "visual-asset-prompt-contract-migration/v1"
PROMPT_CONTRACT_FIELDS = (
    "prompt_packet_sha256",
    "prompt_packet_slot_id",
    "prompt_slot_sha256",
    "prompt_summary",
    "review_criteria",
)
LEGACY_MANIFEST_SCHEMAS = {"visual-asset-manifest/v1", "1.0"}
GENERATION_PROVENANCE_FIELDS = {
    "generation_provenance_version",
    "generator",
    "generation_run_id",
    "candidate_id",
}
GENERATION_RUN_ID_PATTERN = re.compile(
    r"^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$"
)
GENERATION_CANDIDATE_ID_PATTERN = re.compile(r"^ig_[0-9a-f]{50}$")
FREE_SOURCED_PROVIDERS = {"openverse", "wikimedia-commons", "unsplash", "pexels"}
LICENSED_SOURCED_PROVIDERS = {
    "adobe-stock",
    "shutterstock",
    "getty-images",
    "istock",
    "envato-elements",
    "local-licensed-file",
}
REFERENCE_ONLY_PROVIDERS = {"lazyweb", "mobbin", "dribbble", "behance", "awwwards"}
GENERATED_ASSET_REQUIRED_FIELDS = {
    "id",
    "label",
    "slot",
    "status",
    "asset_path",
    "original_png_path",
    "format",
    "dimensions",
    "size_kb",
    "sha256",
    "intended_for",
    "alt_text",
    "prompt_summary",
}
SOURCED_ASSET_REQUIRED_FIELDS = {
    "id",
    "label",
    "slot",
    "status",
    "acquisition_mode",
    "asset_path",
    "source_url",
    "download_url",
    "provider",
    "author",
    "license",
    "attribution_required",
    "sha256",
    "intended_for",
    "alt_text",
    "selection_reason",
}


@dataclass(slots=True)
class RegisteredVisualAsset:
    manifest_path: Path
    asset_path: Path
    asset_id: str
    sha256: str
    width: int
    height: int
    status: str


def register_generated_visual_asset(
    *,
    project_dir: Path,
    manifest_path: Path,
    asset_id: str,
    source_path: Path,
    alt_text: str,
    selection_reason: str,
    reviewed_criteria: list[str],
    label: str | None = None,
    intended_for: list[str] | None = None,
    original_png_path: str | None = None,
    session_id: str,
) -> RegisteredVisualAsset:
    if not alt_text.strip():
        raise ValueError("alt_text is required for accepted visual assets")
    if not selection_reason.strip():
        raise ValueError("selection_reason is required for accepted visual assets")
    reviewed_criteria = [item.strip() for item in reviewed_criteria if item.strip()]
    if not reviewed_criteria:
        raise ValueError("at least one reviewed_criterion is required for accepted visual assets")
    if not session_id.strip():
        raise ValueError("session_id is required for generated visual assets")
    if not source_path.is_file():
        raise ValueError(f"source image not found: {source_path}")

    manifest = _load_manifest(manifest_path)
    assets = manifest.get("assets")
    if not isinstance(assets, list):
        raise ValueError("manifest.assets must be a list")
    record = next((item for item in assets if isinstance(item, dict) and item.get("id") == asset_id), None)
    if record is None:
        raise ValueError(f"asset id not found in manifest: {asset_id}")
    if record.get("status") != "planned":
        raise ValueError("only planned visual asset slots can accept a new generated candidate")
    prompt_errors, prompt_slots = _validate_prompt_packet_contract(
        manifest,
        manifest_path=manifest_path,
        project_dir=project_dir,
    )
    if prompt_errors:
        raise ValueError("invalid prompt packet contract: " + "; ".join(prompt_errors))
    prompt_slot = prompt_slots.get(asset_id)
    if prompt_slot is None:
        raise ValueError(f"asset id is not linked to a prompt packet slot: {asset_id}")
    if prompt_slot.get("active_generation") is False:
        raise ValueError("inactive legacy prompt slots cannot accept a new generated candidate")
    prompt_link_errors = _prompt_record_link_errors(
        record,
        prompt_slot=prompt_slot,
        manifest=manifest,
        prefix=f"asset {asset_id}",
    )
    if prompt_link_errors:
        raise ValueError("invalid asset prompt linkage: " + "; ".join(prompt_link_errors))
    required_review = [str(item) for item in record.get("review_criteria", []) if item]
    missing_review = [item for item in required_review if item not in reviewed_criteria]
    if missing_review:
        raise ValueError("all review criteria must be confirmed: " + "; ".join(missing_review))

    try:
        with Image.open(source_path) as image:
            image.verify()
        with Image.open(source_path) as image:
            image_format = str(image.format or "").upper()
            width, height = image.size
    except (UnidentifiedImageError, OSError) as exc:
        raise ValueError(f"invalid image file: {source_path}") from exc
    if image_format not in SUPPORTED_FORMATS:
        raise ValueError(f"unsupported image format {image_format}; use PNG, JPEG, or WebP")
    expected_ratios = [str(item) for item in record.get("expected_aspect_ratios", []) if item]
    if expected_ratios and not any(_aspect_ratio_matches(ratio, (width, height), tolerance=0.05) for ratio in expected_ratios):
        raise ValueError(
            f"image aspect ratio {width}:{height} does not match the planned ratios: "
            + ", ".join(expected_ratios)
        )
    if original_png_path and Path(original_png_path).suffix.lower() != ".png":
        raise ValueError("original_png_path must point to the preserved PNG generation output")
    if image_format != "PNG" and not original_png_path:
        raise ValueError("non-PNG derivatives require original_png_path provenance")
    original_path = Path(original_png_path).expanduser().resolve() if original_png_path else source_path.resolve()
    if not original_path.is_file():
        raise ValueError(f"original PNG generation output not found: {original_path}")
    try:
        with Image.open(original_path) as original_image:
            original_format = str(original_image.format or "").upper()
    except (UnidentifiedImageError, OSError) as exc:
        raise ValueError(f"original generation output is not a readable PNG: {original_path}") from exc
    if original_format != "PNG":
        raise ValueError("original generation output must be PNG")
    generation_run_id, candidate_id = _codex_generation_identity(original_path)
    if session_id.strip() != generation_run_id:
        raise ValueError(
            "session_id must match the generation run encoded by original_png_path: "
            + generation_run_id
        )

    targets = intended_for if intended_for is not None else record.get("intended_for", [])
    targets = [str(target) for target in targets if target]
    digest = _sha256(source_path)
    extension = {"PNG": ".png", "JPEG": ".jpg", "WEBP": ".webp"}[image_format]
    asset_stem = slugify(label or str(record.get("label") or record.get("slot") or asset_id))
    assets_dir = project_dir / "assets"
    assets_dir.mkdir(parents=True, exist_ok=True)
    destination = assets_dir / f"{asset_stem}-{digest[:10]}{extension}"
    if source_path.resolve() != destination.resolve():
        shutil.copy2(source_path, destination)

    divisor = math.gcd(width, height)
    record.update({
        "label": label or record.get("label") or asset_stem.replace("-", " ").title(),
        "status": "accepted",
        "acquisition_mode": "generated",
        "asset_path": destination.relative_to(project_dir).as_posix(),
        "original_png_path": str(original_path),
        "original_sha256": _sha256(original_path),
        "format": image_format.lower().replace("jpeg", "jpg"),
        "dimensions": {
            "width": width,
            "height": height,
            "aspect_ratio": f"{width // divisor}:{height // divisor}",
        },
        "size_kb": round(destination.stat().st_size / 1024, 2),
        "sha256": digest,
        "intended_for": targets,
        "alt_text": alt_text.strip(),
        "selection_reason": selection_reason.strip(),
        "reviewed_criteria": reviewed_criteria,
        "review_gate_version": "visual-asset-review/v1",
        "generation_provenance_version": VISUAL_ASSET_GENERATION_PROVENANCE_VERSION,
        "generator": VISUAL_IMAGE_GENERATOR_ID,
        "generation_run_id": generation_run_id,
        "candidate_id": candidate_id,
    })
    manifest["schema_version"] = VISUAL_ASSET_MANIFEST_SCHEMA
    manifest.setdefault("project", project_dir.name)
    manifest.setdefault("brand", project_dir.name)
    manifest["generator"] = {
        "id": VISUAL_IMAGE_GENERATOR_ID,
        "api_fallback": "disabled",
    }
    source_session = manifest.setdefault("source_session", {})
    source_session["id"] = session_id.strip()
    source_session["default_directory"] = str(original_path.parent)
    source_session["preserve_originals"] = True
    write_json(manifest_path, manifest)

    return RegisteredVisualAsset(
        manifest_path=manifest_path,
        asset_path=destination,
        asset_id=asset_id,
        sha256=digest,
        width=width,
        height=height,
        status="accepted",
    )


def promote_generated_visual_asset(
    *,
    project_dir: Path,
    manifest_path: Path,
    asset_id: str,
    intended_for: list[str] | None = None,
) -> RegisteredVisualAsset:
    manifest = _load_manifest(manifest_path)
    original_manifest = deepcopy(manifest)
    assets = manifest.get("assets")
    if not isinstance(assets, list):
        raise ValueError("manifest.assets must be a list")
    record = next((item for item in assets if isinstance(item, dict) and item.get("id") == asset_id), None)
    if record is None:
        raise ValueError(f"asset id not found in manifest: {asset_id}")
    if record.get("status") != "accepted":
        raise ValueError("only accepted assets can be promoted to integrated")
    targets = intended_for if intended_for is not None else record.get("intended_for", [])
    targets = [str(target) for target in targets if target]
    if not targets:
        raise ValueError("integrated assets require at least one intended_for target")
    try:
        record["intended_for"] = targets
        write_json(manifest_path, manifest)
        accepted_report = validate_visual_asset_manifest(
            manifest_path,
            project_dir=project_dir,
            strict_production=True,
        )
        if not accepted_report["ok"]:
            raise ValueError(
                "cannot promote invalid asset: " + "; ".join(accepted_report["errors"])
            )

        from .implementation_linter import find_runtime_visual_asset_references

        runtime_references = find_runtime_visual_asset_references(
            project_dir,
            str(record["asset_path"]),
        )
        if not runtime_references:
            raise ValueError(
                "cannot promote asset before its workspace copy is referenced by runtime implementation code: "
                + str(record["asset_path"])
            )

        record["runtime_integration"] = {
            "gate": "implementation-reference/v1",
            "references": runtime_references,
        }
        record["status"] = "integrated"
        write_json(manifest_path, manifest)
        report = validate_visual_asset_manifest(
            manifest_path,
            project_dir=project_dir,
            require_integrated=True,
            strict_production=True,
        )
        if not report["ok"]:
            raise ValueError("cannot promote invalid asset: " + "; ".join(report["errors"]))
    except (ValueError, OSError):
        write_json(manifest_path, original_manifest)
        raise
    asset_path = project_dir / str(record["asset_path"])
    dimensions = record["dimensions"]
    return RegisteredVisualAsset(
        manifest_path=manifest_path,
        asset_path=asset_path,
        asset_id=asset_id,
        sha256=str(record["sha256"]),
        width=int(dimensions["width"]),
        height=int(dimensions["height"]),
        status="integrated",
    )


def validate_visual_asset_manifest(
    manifest_path: Path,
    *,
    project_dir: Path,
    require_integrated: bool = False,
    strict_production: bool | None = None,
) -> dict[str, Any]:
    strict_production = require_integrated if strict_production is None else strict_production
    errors: list[str] = []
    warnings: list[str] = []
    try:
        manifest = _load_manifest(manifest_path)
    except (ValueError, json.JSONDecodeError) as exc:
        return {"ok": False, "errors": [str(exc)], "warnings": [], "asset_count": 0, "integrated_count": 0}

    for field in ("schema_version", "project", "brand", "generator", "source_session", "assets"):
        if field not in manifest:
            errors.append(f"manifest missing required field: {field}")
    schema_version = manifest.get("schema_version")
    if schema_version not in {VISUAL_ASSET_MANIFEST_SCHEMA, *LEGACY_MANIFEST_SCHEMAS}:
        errors.append(
            f"manifest schema_version must be {VISUAL_ASSET_MANIFEST_SCHEMA}"
        )
    elif schema_version in LEGACY_MANIFEST_SCHEMAS:
        warnings.append(
            f"legacy schema_version {schema_version} is accepted only for planned or sourced records; "
            f"rewrite generated final assets to {VISUAL_ASSET_MANIFEST_SCHEMA}"
        )
    assets = manifest.get("assets") if isinstance(manifest.get("assets"), list) else []
    if not isinstance(manifest.get("assets"), list):
        errors.append("manifest.assets must be a list")

    integrated_count = 0
    generated_final_count = 0
    prompt_errors, prompt_slots = _validate_prompt_packet_contract(
        manifest,
        manifest_path=manifest_path,
        project_dir=project_dir,
    )
    prompt_contract_reported = False
    component_contract_ids: set[str] = set()
    has_final_assets = any(
        isinstance(item, dict) and item.get("status") in FINAL_STATUSES
        for item in assets
    )
    if strict_production and has_final_assets:
        component_contract_ids, component_contract_errors = _load_component_contract_ids(project_dir)
        errors.extend(component_contract_errors)
    for index, record in enumerate(assets):
        prefix = f"assets[{index}]"
        if not isinstance(record, dict):
            errors.append(f"{prefix} must be an object")
            continue
        is_sourced = (
            record.get("acquisition_mode") == "sourced"
            or str(record.get("id") or "").startswith("sourced-visual-asset:")
        )
        required_fields = SOURCED_ASSET_REQUIRED_FIELDS if is_sourced else GENERATED_ASSET_REQUIRED_FIELDS
        if not is_sourced and schema_version == VISUAL_ASSET_MANIFEST_SCHEMA:
            required_fields = required_fields | GENERATION_PROVENANCE_FIELDS
        missing = sorted(required_fields - set(record))
        if missing:
            errors.append(f"{prefix} missing fields: {', '.join(missing)}")
        status = record.get("status")
        if status == "integrated":
            integrated_count += 1
        if status not in {"planned", "accepted", "integrated", "rejected"}:
            errors.append(f"{prefix} has invalid status: {status}")
        if status not in FINAL_STATUSES:
            continue
        if not is_sourced:
            generated_final_count += 1
            if schema_version != VISUAL_ASSET_MANIFEST_SCHEMA:
                errors.append(
                    f"{prefix} must use {VISUAL_ASSET_MANIFEST_SCHEMA} when status={status}"
                )
        final_value_fields = ["asset_path", "sha256", "alt_text"]
        if is_sourced:
            final_value_fields.extend(["source_url", "download_url", "provider", "author", "license", "selection_reason"])
        else:
            final_value_fields.extend(["format", "dimensions", "size_kb", "prompt_summary"])
        for field in final_value_fields:
            if not record.get(field):
                errors.append(f"{prefix}.{field} is required when status={status}")
        if status == "integrated" and not record.get("intended_for"):
            errors.append(f"{prefix}.intended_for is required when status=integrated")
        if is_sourced:
            provider = str(record.get("provider") or "").lower()
            if provider in REFERENCE_ONLY_PROVIDERS:
                errors.append(f"{prefix}.provider {provider} is reference-only and cannot become a runtime asset")
            elif provider in LICENSED_SOURCED_PROVIDERS:
                for field in ("license_proof", "usage_scope", "licensed_to"):
                    if not record.get(field):
                        errors.append(f"{prefix}.{field} is required for licensed provider {provider}")
            elif provider not in FREE_SOURCED_PROVIDERS:
                errors.append(f"{prefix}.provider is not in the runtime asset allowlist: {provider}")
            if record.get("attribution_required") and not record.get("attribution_text"):
                errors.append(f"{prefix}.attribution_text is required when attribution_required=true")
        if not is_sourced:
            has_current_review = record.get("review_gate_version") == "visual-asset-review/v1"
            if has_current_review:
                if not record.get("selection_reason"):
                    errors.append(f"{prefix}.selection_reason is required when status={status}")
                if not record.get("reviewed_criteria"):
                    errors.append(f"{prefix}.reviewed_criteria is required when status={status}")
                required_review = [str(item) for item in record.get("review_criteria", []) if item]
                confirmed_review = [str(item) for item in record.get("reviewed_criteria", []) if item]
                missing_review = [item for item in required_review if item not in confirmed_review]
                if missing_review:
                    errors.append(
                        f"{prefix}.reviewed_criteria does not confirm every prompt review criterion: "
                        + "; ".join(missing_review)
                    )
            else:
                message = f"{prefix} is a legacy generated asset without visual-asset-review/v1 evidence"
                (errors if strict_production else warnings).append(message)

            if prompt_errors and not prompt_contract_reported:
                target = errors if strict_production else warnings
                target.extend(f"prompt packet contract: {error}" for error in prompt_errors)
                prompt_contract_reported = True
            slot_id = str(record.get("prompt_packet_slot_id") or "")
            slot = prompt_slots.get(slot_id)
            prompt_link_errors = _prompt_record_link_errors(
                record,
                prompt_slot=slot,
                manifest=manifest,
                prefix=prefix,
            )
            if prompt_link_errors:
                (errors if strict_production else warnings).extend(prompt_link_errors)
            prompt_migration_errors = _prompt_contract_migration_errors(
                record,
                prompt_slot=slot,
                manifest=manifest,
                manifest_path=manifest_path,
                project_dir=project_dir,
                prefix=prefix,
            )
            errors.extend(prompt_migration_errors)

            errors.extend(_validate_original_png(record, prefix=prefix))
            errors.extend(
                _validate_generation_provenance(
                    record,
                    manifest=manifest,
                    prefix=prefix,
                )
            )

        if strict_production and status in FINAL_STATUSES:
            targets = [str(target) for target in record.get("intended_for", []) if target]
            invalid_targets = [target for target in targets if target not in component_contract_ids]
            if not targets:
                errors.append(f"{prefix}.intended_for must reference at least one component contract")
            elif invalid_targets:
                errors.append(
                    f"{prefix}.intended_for contains targets without an actual component contract: "
                    + ", ".join(invalid_targets)
                )
            if status == "integrated":
                runtime_integration = record.get("runtime_integration") or {}
                if (
                    runtime_integration.get("gate") != "implementation-reference/v1"
                    or not runtime_integration.get("references")
                ):
                    errors.append(
                        f"{prefix}.runtime_integration must record implementation-reference/v1 evidence"
                    )
        relative_path = record.get("asset_path")
        if not relative_path:
            continue
        candidate = (project_dir / str(relative_path)).resolve()
        try:
            candidate.relative_to(project_dir.resolve())
        except ValueError:
            errors.append(f"{prefix}.asset_path must stay inside the project directory")
            continue
        if not candidate.is_file():
            errors.append(f"{prefix}.asset_path does not exist: {relative_path}")
            continue
        actual_digest = _sha256(candidate)
        if record.get("sha256") and record["sha256"] != actual_digest:
            errors.append(f"{prefix}.sha256 does not match the workspace copy")
        try:
            with Image.open(candidate) as image:
                actual_size = image.size
            dimensions = record.get("dimensions") or {}
            if dimensions and (dimensions.get("width"), dimensions.get("height")) != actual_size:
                errors.append(f"{prefix}.dimensions do not match the workspace copy")
            actual_format = str(image.format or "").lower().replace("jpeg", "jpg")
            if record.get("format") and record.get("format") != actual_format:
                errors.append(f"{prefix}.format does not match the workspace copy")
            declared_ratio = dimensions.get("aspect_ratio") if dimensions else None
            if declared_ratio and not _aspect_ratio_matches(declared_ratio, actual_size):
                errors.append(f"{prefix}.dimensions.aspect_ratio does not match the workspace copy")
            actual_size_kb = round(candidate.stat().st_size / 1024, 2)
            declared_size_kb = record.get("size_kb")
            size_tolerance = max(4.0, actual_size_kb * 0.05)
            if (
                declared_size_kb is not None
                and abs(float(declared_size_kb) - actual_size_kb) > size_tolerance
            ):
                errors.append(f"{prefix}.size_kb does not match the workspace copy")
        except (UnidentifiedImageError, OSError):
            errors.append(f"{prefix}.asset_path is not a readable image")

    if generated_final_count and not (manifest.get("source_session") or {}).get("id"):
        errors.append("source_session.id is required when accepted or integrated generated assets exist")

    if require_integrated and integrated_count == 0:
        errors.append("at least one integrated visual asset is required")
    if not assets:
        warnings.append("manifest contains no visual asset slots")
    return {
        "ok": not errors,
        "errors": errors,
        "warnings": warnings,
        "asset_count": len(assets),
        "integrated_count": integrated_count,
    }


def _load_manifest(path: Path) -> dict[str, Any]:
    if not path.is_file():
        raise ValueError(f"visual asset manifest not found: {path}")
    payload = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ValueError("visual asset manifest must be a JSON object")
    return payload


def _validate_prompt_packet_contract(
    manifest: dict[str, Any],
    *,
    manifest_path: Path,
    project_dir: Path,
) -> tuple[list[str], dict[str, dict[str, Any]]]:
    errors: list[str] = []
    relative_path = manifest.get("prompt_packet")
    declared_digest = manifest.get("prompt_packet_sha256")
    if not relative_path:
        return ["manifest.prompt_packet is required"], {}
    if not declared_digest:
        errors.append("manifest.prompt_packet_sha256 is required")
    candidate = (manifest_path.parent / str(relative_path)).resolve()
    try:
        candidate.relative_to(project_dir.resolve())
    except ValueError:
        errors.append("manifest.prompt_packet must stay inside the project directory")
        return errors, {}
    if not candidate.is_file():
        errors.append(f"manifest.prompt_packet does not exist: {relative_path}")
        return errors, {}
    actual_digest = _sha256(candidate)
    if declared_digest and declared_digest != actual_digest:
        errors.append("manifest.prompt_packet_sha256 does not match the prompt packet")
    try:
        packet = json.loads(candidate.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, UnicodeDecodeError) as exc:
        errors.append(f"manifest.prompt_packet is unreadable: {exc}")
        return errors, {}
    if not isinstance(packet, dict):
        errors.append("manifest.prompt_packet must contain a JSON object")
        return errors, {}
    if packet.get("schema_version") != "design-ontology.visual-prompt-packet.v1":
        errors.append("manifest.prompt_packet has an unsupported schema_version")
    slots: dict[str, dict[str, Any]] = {}
    for slot in packet.get("slots", []):
        if not isinstance(slot, dict) or not slot.get("id"):
            errors.append("manifest.prompt_packet contains a slot without an id")
            continue
        slot_id = str(slot["id"])
        if slot_id in slots:
            errors.append(f"manifest.prompt_packet contains duplicate slot id: {slot_id}")
            continue
        slots[slot_id] = slot
    return errors, slots


def _validate_original_png(record: dict[str, Any], *, prefix: str) -> list[str]:
    errors: list[str] = []
    raw_path = record.get("original_png_path")
    if not raw_path:
        return [f"{prefix}.original_png_path is required for generated assets"]
    path = Path(str(raw_path)).expanduser().resolve()
    if not path.is_file():
        return [f"{prefix}.original_png_path does not exist: {raw_path}"]
    try:
        with Image.open(path) as image:
            image_format = str(image.format or "").upper()
    except (UnidentifiedImageError, OSError):
        return [f"{prefix}.original_png_path is not a readable PNG"]
    if image_format != "PNG":
        errors.append(f"{prefix}.original_png_path must be a PNG")
    declared_digest = record.get("original_sha256")
    if not declared_digest:
        errors.append(f"{prefix}.original_sha256 is required")
    elif declared_digest != _sha256(path):
        errors.append(f"{prefix}.original_sha256 does not match the original PNG")
    return errors


def _validate_generation_provenance(
    record: dict[str, Any],
    *,
    manifest: dict[str, Any],
    prefix: str,
) -> list[str]:
    errors: list[str] = []
    for field in sorted(GENERATION_PROVENANCE_FIELDS):
        if not record.get(field):
            errors.append(f"{prefix}.{field} is required for accepted or integrated generated assets")
    if record.get("generation_provenance_version") != VISUAL_ASSET_GENERATION_PROVENANCE_VERSION:
        errors.append(
            f"{prefix}.generation_provenance_version must be "
            f"{VISUAL_ASSET_GENERATION_PROVENANCE_VERSION}"
        )
    if record.get("generator") != VISUAL_IMAGE_GENERATOR_ID:
        errors.append(f"{prefix}.generator must be {VISUAL_IMAGE_GENERATOR_ID}")

    manifest_generator = manifest.get("generator")
    manifest_generator_id = (
        manifest_generator.get("id")
        if isinstance(manifest_generator, dict)
        else manifest_generator
    )
    if manifest_generator_id != record.get("generator"):
        errors.append(f"{prefix}.generator does not match manifest.generator.id")

    raw_path = record.get("original_png_path")
    if not raw_path:
        return errors
    original_path = Path(str(raw_path)).expanduser().resolve()
    try:
        expected_run_id, expected_candidate_id = _codex_generation_identity(original_path)
    except ValueError as exc:
        errors.append(f"{prefix}.original_png_path has invalid Codex generation provenance: {exc}")
        return errors
    if record.get("generation_run_id") != expected_run_id:
        errors.append(
            f"{prefix}.generation_run_id does not match original_png_path"
        )
    if record.get("candidate_id") != expected_candidate_id:
        errors.append(f"{prefix}.candidate_id does not match original_png_path")
    return errors


def _codex_generation_identity(original_path: Path) -> tuple[str, str]:
    if original_path.suffix.lower() != ".png":
        raise ValueError("original output must be a PNG")
    generation_dir = original_path.parent
    if generation_dir.parent.name != "generated_images":
        raise ValueError(
            "path must match $CODEX_HOME/generated_images/<generation-run-id>/<candidate-id>.png"
        )
    generation_run_id = generation_dir.name
    candidate_id = original_path.stem
    if not GENERATION_RUN_ID_PATTERN.fullmatch(generation_run_id):
        raise ValueError("generation run id is not a Codex run identifier")
    if not GENERATION_CANDIDATE_ID_PATTERN.fullmatch(candidate_id):
        raise ValueError("candidate id is not a Codex image_gen call identifier")
    return generation_run_id, candidate_id


def _prompt_record_link_errors(
    record: dict[str, Any],
    *,
    prompt_slot: dict[str, Any] | None,
    manifest: dict[str, Any],
    prefix: str,
) -> list[str]:
    errors: list[str] = []
    slot_id = str(record.get("prompt_packet_slot_id") or "")
    if not slot_id:
        errors.append(f"{prefix}.prompt_packet_slot_id is required")
    elif prompt_slot is None:
        errors.append(f"{prefix}.prompt_packet_slot_id is not present in the prompt packet")
    else:
        if record.get("prompt_slot_sha256") != _canonical_sha256(prompt_slot):
            errors.append(f"{prefix}.prompt_slot_sha256 does not match its prompt packet slot")
        if record.get("prompt_summary") != prompt_slot.get("prompt"):
            errors.append(f"{prefix}.prompt_summary does not match its prompt packet slot")
    if record.get("prompt_packet_sha256") != manifest.get("prompt_packet_sha256"):
        errors.append(f"{prefix}.prompt_packet_sha256 does not match the manifest")
    return errors


def _prompt_contract_migration_errors(
    record: dict[str, Any],
    *,
    prompt_slot: dict[str, Any] | None,
    manifest: dict[str, Any],
    manifest_path: Path,
    project_dir: Path,
    prefix: str,
) -> list[str]:
    """Validate append-only evidence when a final asset's prompt plan evolves.

    Current linkage remains strict: a migration never excuses a record whose
    fields do not match the current packet. The migration chain proves the
    prior packet/slot contract by keeping raw, content-addressed copies inside
    the project.
    """
    errors: list[str] = []
    migrations = record.get("prompt_contract_migrations")
    is_legacy = bool(
        prompt_slot
        and (
            prompt_slot.get("active_generation") is False
            or isinstance(prompt_slot.get("legacy_contract"), dict)
        )
    )
    if migrations is None:
        if is_legacy:
            errors.append(f"{prefix}.prompt_contract_migrations is required for a legacy prompt slot")
        return errors
    if not isinstance(migrations, list) or not migrations:
        errors.append(f"{prefix}.prompt_contract_migrations must be a non-empty list")
        return errors

    current = _prompt_contract_from_record(record)
    previous_to: dict[str, Any] | None = None
    for index, migration in enumerate(migrations):
        migration_prefix = f"{prefix}.prompt_contract_migrations[{index}]"
        if not isinstance(migration, dict):
            errors.append(f"{migration_prefix} must be an object")
            continue
        if migration.get("schema_version") != PROMPT_CONTRACT_MIGRATION_SCHEMA:
            errors.append(
                f"{migration_prefix}.schema_version must be {PROMPT_CONTRACT_MIGRATION_SCHEMA}"
            )
        if not isinstance(migration.get("reason"), str) or not migration["reason"].strip():
            errors.append(f"{migration_prefix}.reason is required")
        source = migration.get("from")
        target = migration.get("to")
        if not isinstance(source, dict) or not isinstance(target, dict):
            errors.append(f"{migration_prefix}.from and .to must be prompt-contract objects")
            continue
        errors.extend(_prompt_contract_shape_errors(source, prefix=f"{migration_prefix}.from"))
        errors.extend(_prompt_contract_shape_errors(target, prefix=f"{migration_prefix}.to"))
        if source == target:
            errors.append(f"{migration_prefix}.from and .to must differ")
        if previous_to is not None and source != previous_to:
            errors.append(f"{migration_prefix}.from must equal the previous migration .to")
        previous_to = target
        errors.extend(
            _prompt_contract_archive_errors(
                migration.get("archive"),
                source=source,
                manifest_path=manifest_path,
                project_dir=project_dir,
                prefix=f"{migration_prefix}.archive",
            )
        )

    if previous_to is not None and previous_to != current:
        errors.append(f"{prefix}.prompt_contract_migrations final .to must equal the current record contract")
    if prompt_slot is not None:
        expected = _prompt_contract_for_slot(
            prompt_slot,
            prompt_packet_sha256=str(manifest.get("prompt_packet_sha256") or ""),
        )
        if current != expected:
            errors.append(
                f"{prefix}.prompt_contract_migrations current record contract does not match the prompt packet"
            )
    return errors


def _prompt_contract_shape_errors(contract: dict[str, Any], *, prefix: str) -> list[str]:
    errors: list[str] = []
    for field in PROMPT_CONTRACT_FIELDS:
        if field not in contract:
            errors.append(f"{prefix}.{field} is required")
    for field in ("prompt_packet_sha256", "prompt_slot_sha256"):
        value = contract.get(field)
        if not isinstance(value, str) or not re.fullmatch(r"[a-f0-9]{64}", value):
            errors.append(f"{prefix}.{field} must be a lowercase sha256")
    for field in ("prompt_packet_slot_id", "prompt_summary"):
        value = contract.get(field)
        if not isinstance(value, str) or not value.strip():
            errors.append(f"{prefix}.{field} is required")
    criteria = contract.get("review_criteria")
    if not isinstance(criteria, list) or not all(isinstance(item, str) and item.strip() for item in criteria):
        errors.append(f"{prefix}.review_criteria must be a list of non-empty strings")
    return errors


def _prompt_contract_archive_errors(
    archive: Any,
    *,
    source: dict[str, Any],
    manifest_path: Path,
    project_dir: Path,
    prefix: str,
) -> list[str]:
    errors: list[str] = []
    if not isinstance(archive, dict):
        return [f"{prefix} is required"]
    raw_path = archive.get("path")
    if not isinstance(raw_path, str) or not raw_path.strip():
        return [f"{prefix}.path is required"]
    archive_path = (manifest_path.parent / raw_path).resolve()
    try:
        archive_path.relative_to(project_dir.resolve())
    except ValueError:
        return [f"{prefix}.path must stay inside the project directory"]
    if archive.get("packet_sha256") != source.get("prompt_packet_sha256"):
        errors.append(f"{prefix}.packet_sha256 must equal migration.from.prompt_packet_sha256")
    if archive.get("slot_id") != source.get("prompt_packet_slot_id"):
        errors.append(f"{prefix}.slot_id must equal migration.from.prompt_packet_slot_id")
    if not archive_path.is_file():
        return [*errors, f"{prefix}.path does not exist: {raw_path}"]
    if _sha256(archive_path) != source.get("prompt_packet_sha256"):
        errors.append(f"{prefix}.path sha256 does not match migration.from.prompt_packet_sha256")
        return errors
    try:
        packet = json.loads(archive_path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, UnicodeDecodeError) as exc:
        return [*errors, f"{prefix}.path is not readable JSON: {exc}"]
    if not isinstance(packet, dict):
        return [*errors, f"{prefix}.path must contain a JSON object"]
    archive_slot = next(
        (
            slot
            for slot in packet.get("slots", [])
            if isinstance(slot, dict)
            and slot.get("id") == source.get("prompt_packet_slot_id")
        ),
        None,
    )
    if archive_slot is None:
        return [*errors, f"{prefix}.path does not contain migration.from prompt slot"]
    if _canonical_sha256(archive_slot) != source.get("prompt_slot_sha256"):
        errors.append(f"{prefix}.path prompt slot sha256 does not match migration.from")
    if archive_slot.get("prompt") != source.get("prompt_summary"):
        errors.append(f"{prefix}.path prompt summary does not match migration.from")
    archive_criteria = [str(item) for item in archive_slot.get("review_criteria", []) if item]
    if archive_criteria != source.get("review_criteria"):
        errors.append(f"{prefix}.path review criteria do not match migration.from")
    return errors


def _prompt_contract_from_record(record: dict[str, Any]) -> dict[str, Any]:
    return {
        "prompt_packet_sha256": str(record.get("prompt_packet_sha256") or ""),
        "prompt_packet_slot_id": str(record.get("prompt_packet_slot_id") or ""),
        "prompt_slot_sha256": str(record.get("prompt_slot_sha256") or ""),
        "prompt_summary": str(record.get("prompt_summary") or ""),
        "review_criteria": [
            str(item) for item in record.get("review_criteria", []) if item
        ],
    }


def _prompt_contract_for_slot(
    prompt_slot: dict[str, Any],
    *,
    prompt_packet_sha256: str,
) -> dict[str, Any]:
    return {
        "prompt_packet_sha256": prompt_packet_sha256,
        "prompt_packet_slot_id": str(prompt_slot.get("id") or ""),
        "prompt_slot_sha256": _canonical_sha256(prompt_slot),
        "prompt_summary": str(prompt_slot.get("prompt") or ""),
        "review_criteria": [
            str(item) for item in prompt_slot.get("review_criteria", []) if item
        ],
    }


def _load_component_contract_ids(project_dir: Path) -> tuple[set[str], list[str]]:
    inventory_path = project_dir / "build" / "system" / "blueprint" / "component_inventory.json"
    specs_path = project_dir / "build" / "system" / "components" / "component_specs.json"
    errors: list[str] = []

    def load_components(path: Path, key: str) -> list[dict[str, Any]]:
        if not path.is_file():
            errors.append(f"component contract evidence not found: {path.relative_to(project_dir)}")
            return []
        try:
            payload = json.loads(path.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, UnicodeDecodeError) as exc:
            errors.append(f"component contract evidence is unreadable: {path.relative_to(project_dir)}: {exc}")
            return []
        records = payload.get(key) if isinstance(payload, dict) else None
        if not isinstance(records, list):
            errors.append(f"component contract evidence has no {key} list: {path.relative_to(project_dir)}")
            return []
        return [item for item in records if isinstance(item, dict)]

    inventory = load_components(inventory_path, "components")
    specs = load_components(specs_path, "specs")

    def ids(records: list[dict[str, Any]], *, require_complete: bool) -> set[str]:
        result: set[str] = set()
        for record in records:
            if require_complete and record.get("contract_status") != "complete":
                continue
            explicit = record.get("contract_id") or record.get("id")
            name = record.get("name")
            if explicit and str(explicit).startswith("component:"):
                result.add(str(explicit))
            if name:
                result.add(f"component:{slugify(str(name))}")
        return result

    inventory_ids = ids(inventory, require_complete=False)
    spec_ids = ids(specs, require_complete=True)
    contract_ids = inventory_ids & spec_ids
    if not contract_ids and not errors:
        errors.append("component inventory and complete component specs have no matching contract ids")
    return contract_ids, errors


def _canonical_sha256(payload: Any) -> str:
    encoded = json.dumps(
        payload,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _aspect_ratio_matches(
    declared: Any,
    actual_size: tuple[int, int],
    *,
    tolerance: float = 0.01,
) -> bool:
    try:
        left, right = str(declared).split(":", 1)
        declared_value = float(left) / float(right)
    except (ValueError, ZeroDivisionError):
        return False
    actual_value = actual_size[0] / actual_size[1]
    return abs(declared_value - actual_value) / actual_value <= tolerance
