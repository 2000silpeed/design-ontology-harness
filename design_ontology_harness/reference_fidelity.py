from __future__ import annotations

import hashlib
import json
from datetime import datetime
from pathlib import Path
from typing import Any


CONTRACT_SCHEMA = "reference-fidelity-contract/v1"
REVIEW_SCHEMA = "reference-fidelity-review-artifact/v1"
LOOP_SCHEMA = "reference-fidelity-loop/v1"

DEFAULT_CONTRACT_PATH = Path("design-system/reference-fidelity-contract.json")
DEFAULT_REPORT_PATH = Path("build/system/production/reference-fidelity/latest_loop_report.json")

ALLOWED_DIMENSIONS = {
    "composition",
    "morphology",
    "density",
    "hierarchy",
    "contextual_linkage",
    "task_visibility",
    "responsive_translation",
}

# These remain owned by the brief, Semantic OS, authored type system, or asset policy.
# A visual reference can never become authoritative for them.
REQUIRED_PROHIBITED_SCOPES = {
    "palette",
    "typography",
    "information_architecture",
    "product_copy",
    "logos",
    "redistributable_assets",
}


def load_json(path: Path) -> dict[str, Any]:
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise ValueError(f"JSON artifact not found: {path}") from exc
    except json.JSONDecodeError as exc:
        raise ValueError(f"JSON artifact is invalid: {path}: {exc}") from exc
    if not isinstance(payload, dict):
        raise ValueError(f"JSON artifact root must be an object: {path}")
    return payload


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def validate_reference_fidelity_contract(
    contract_path: Path,
    *,
    project_dir: Path,
) -> tuple[list[str], dict[str, Any]]:
    errors: list[str] = []
    project = project_dir.resolve()
    resolved_contract = contract_path.resolve()
    try:
        contract = load_json(resolved_contract)
    except ValueError as exc:
        return [str(exc)], {}

    if contract.get("schema_version") != CONTRACT_SCHEMA:
        errors.append(f"contract.schema_version must be {CONTRACT_SCHEMA}")
    if len(str(contract.get("contract_id") or "").strip()) < 3:
        errors.append("contract.contract_id is required")

    authority = contract.get("authority")
    if not isinstance(authority, dict):
        errors.append("contract.authority must be an object")
        authority = {}
    if authority.get("source_order") != "brief-and-ontology-before-reference":
        errors.append(
            "contract.authority.source_order must be brief-and-ontology-before-reference"
        )
    prohibited = _string_set(authority.get("prohibited_similarity_scopes"))
    missing_prohibitions = REQUIRED_PROHIBITED_SCOPES - prohibited
    if missing_prohibitions:
        errors.append(
            "contract.authority.prohibited_similarity_scopes is missing: "
            + ", ".join(sorted(missing_prohibitions))
        )

    brief_evidence = _validate_hashed_file_reference(
        contract.get("brief"),
        base=project,
        prefix="contract.brief",
        errors=errors,
    )

    references = contract.get("references")
    if not isinstance(references, list) or not references:
        errors.append("contract.references must be a non-empty list")
        references = []
    reference_evidence: list[dict[str, Any]] = []
    for index, reference in enumerate(references):
        evidence = _validate_hashed_file_reference(
            reference,
            base=project,
            prefix=f"contract.references[{index}]",
            errors=errors,
        )
        if evidence:
            reference_evidence.append(evidence)

    gate = contract.get("gate")
    if not isinstance(gate, dict):
        errors.append("contract.gate must be an object")
        gate = {}
    threshold = _bounded_score(gate.get("threshold"), "contract.gate.threshold", errors)
    max_iterations = gate.get("max_iterations")
    if not isinstance(max_iterations, int) or isinstance(max_iterations, bool) or not 1 <= max_iterations <= 10:
        errors.append("contract.gate.max_iterations must be an integer from 1 to 10")
        max_iterations = 3

    metrics = contract.get("metrics")
    if not isinstance(metrics, list) or not metrics:
        errors.append("contract.metrics must be a non-empty list")
        metrics = []
    metric_records: dict[str, dict[str, Any]] = {}
    total_weight = 0.0
    for index, raw_metric in enumerate(metrics):
        prefix = f"contract.metrics[{index}]"
        if not isinstance(raw_metric, dict):
            errors.append(f"{prefix} must be an object")
            continue
        metric_id = str(raw_metric.get("id") or "").strip()
        if not metric_id:
            errors.append(f"{prefix}.id is required")
            continue
        if metric_id in metric_records:
            errors.append(f"{prefix}.id must be unique")
            continue
        dimension = str(raw_metric.get("dimension") or "").strip()
        if dimension not in ALLOWED_DIMENSIONS:
            errors.append(
                f"{prefix}.dimension {dimension or '<missing>'!r} must be one of "
                f"{', '.join(sorted(ALLOWED_DIMENSIONS))}"
            )
        statement = str(raw_metric.get("statement") or "").strip()
        if len(statement) < 24:
            errors.append(f"{prefix}.statement must record a concrete approved invariant")
        source_quote = str(raw_metric.get("source_quote") or "").strip()
        if len(source_quote) < 12:
            errors.append(f"{prefix}.source_quote must bind the invariant to authored evidence")
        weight = raw_metric.get("weight")
        if not isinstance(weight, int | float) or isinstance(weight, bool) or float(weight) <= 0:
            errors.append(f"{prefix}.weight must be greater than zero")
            weight = 0.0
        minimum_score = _bounded_score(
            raw_metric.get("minimum_score"), f"{prefix}.minimum_score", errors
        )
        critical = raw_metric.get("critical")
        if not isinstance(critical, bool):
            errors.append(f"{prefix}.critical must be a boolean")
            critical = False
        metric_records[metric_id] = {
            "id": metric_id,
            "dimension": dimension,
            "statement": statement,
            "source_quote": source_quote,
            "weight": float(weight),
            "minimum_score": minimum_score,
            "critical": critical,
        }
        total_weight += float(weight)
    if metric_records and not any(metric["critical"] for metric in metric_records.values()):
        errors.append("contract.metrics must contain at least one critical invariant")
    if metric_records and total_weight <= 0:
        errors.append("contract.metrics total weight must be greater than zero")

    return errors, {
        "contract": contract,
        "contract_path": str(resolved_contract),
        "contract_sha256": sha256_file(resolved_contract),
        "brief": brief_evidence,
        "references": reference_evidence,
        "reference_sha256": sorted(
            evidence["sha256"] for evidence in reference_evidence if evidence.get("sha256")
        ),
        "metrics": metric_records,
        "threshold": threshold,
        "max_iterations": max_iterations,
    }


def run_reference_fidelity_loop(
    *,
    contract_path: Path,
    review_artifact_paths: list[Path],
    project_dir: Path,
    expected_screenshot_sha256: set[str] | None = None,
    implementation_tree_sha256: str | None = None,
) -> dict[str, Any]:
    contract_errors, contract_evidence = validate_reference_fidelity_contract(
        contract_path,
        project_dir=project_dir,
    )
    if contract_errors:
        raise ValueError("; ".join(contract_errors))
    if not review_artifact_paths:
        raise ValueError("At least one reference fidelity review artifact is required.")

    iterations: list[dict[str, Any]] = []
    seen_screenshot_sets: set[tuple[str, ...]] = set()
    seen_runtime_trees: set[str] = set()
    max_iterations = int(contract_evidence["max_iterations"])
    if len(review_artifact_paths) > max_iterations:
        raise ValueError(
            f"Review artifact count exceeds contract.gate.max_iterations ({max_iterations})."
        )

    for index, review_path in enumerate(review_artifact_paths, start=1):
        review = load_json(review_path.resolve())
        errors, evaluation = _evaluate_review_artifact(
            review,
            review_path=review_path.resolve(),
            contract_evidence=contract_evidence,
        )
        if errors:
            raise ValueError("; ".join(errors))
        screenshot_key = tuple(evaluation["screenshot_sha256"])
        if screenshot_key in seen_screenshot_sets:
            raise ValueError(
                "Each correction iteration must use a fresh screenshot SHA set; "
                f"iteration {index} reuses prior evidence."
            )
        seen_screenshot_sets.add(screenshot_key)
        runtime_tree = evaluation["implementation_tree_sha256"]
        if runtime_tree in seen_runtime_trees:
            raise ValueError(
                "Each correction iteration must use a fresh runtime-tree SHA; "
                f"iteration {index} reuses prior implementation evidence."
            )
        seen_runtime_trees.add(runtime_tree)
        evaluation["iteration_id"] = f"iteration-{index}"
        iterations.append(evaluation)

    latest = iterations[-1]
    if expected_screenshot_sha256 is not None and set(latest["screenshot_sha256"]) != expected_screenshot_sha256:
        raise ValueError("Latest review screenshot hashes do not match the validated screenshot manifest.")
    if implementation_tree_sha256 is not None and latest["implementation_tree_sha256"] != implementation_tree_sha256:
        raise ValueError("Latest review implementation tree does not match the current runtime tree.")

    passed = bool(latest["passed"])
    exhausted = not passed and len(iterations) >= max_iterations
    return {
        "schema_version": LOOP_SCHEMA,
        "contract": {
            "path": _relative_or_absolute(Path(contract_evidence["contract_path"]), project_dir.resolve()),
            "sha256": contract_evidence["contract_sha256"],
        },
        "threshold": contract_evidence["threshold"],
        "max_iterations": max_iterations,
        "status": "passed" if passed else ("exhausted" if exhausted else "blocked"),
        "passed": passed,
        "ready_to_release": passed,
        "selected_iteration": latest["iteration_id"] if passed else None,
        "iterations": iterations,
        "next_iteration_brief": None if passed else _build_correction_brief(latest),
    }


def validate_reference_fidelity_report(
    report_path: Path,
    *,
    contract_path: Path,
    project_dir: Path,
    screenshot_sha256: set[str],
    implementation_tree_sha256: str,
) -> tuple[list[str], dict[str, Any]]:
    errors: list[str] = []
    try:
        report = load_json(report_path.resolve())
    except ValueError as exc:
        return [str(exc)], {}
    if report.get("schema_version") != LOOP_SCHEMA:
        errors.append(f"reference fidelity report schema_version must be {LOOP_SCHEMA}")

    contract_errors, contract_evidence = validate_reference_fidelity_contract(
        contract_path,
        project_dir=project_dir,
    )
    errors.extend(contract_errors)
    if contract_errors:
        return errors, {"report_path": str(report_path.resolve())}

    report_contract = report.get("contract")
    if not isinstance(report_contract, dict):
        errors.append("reference fidelity report contract reference is required")
    elif report_contract.get("sha256") != contract_evidence["contract_sha256"]:
        errors.append("reference fidelity report contract hash does not match the current contract")

    raw_iterations = report.get("iterations")
    if not isinstance(raw_iterations, list) or not raw_iterations:
        errors.append("reference fidelity report iterations must be a non-empty list")
        raw_iterations = []
    if len(raw_iterations) > int(contract_evidence["max_iterations"]):
        errors.append("reference fidelity report exceeds the contract iteration limit")

    recomputed: list[dict[str, Any]] = []
    seen_screenshot_sets: set[tuple[str, ...]] = set()
    seen_runtime_trees: set[str] = set()
    for index, iteration in enumerate(raw_iterations, start=1):
        prefix = f"reference fidelity report iterations[{index - 1}]"
        if not isinstance(iteration, dict):
            errors.append(f"{prefix} must be an object")
            continue
        artifact = iteration.get("artifact")
        artifact_path = _load_hashed_json_artifact(
            artifact,
            base=project_dir.resolve(),
            prefix=f"{prefix}.artifact",
            errors=errors,
        )
        if artifact_path is None:
            continue
        artifact_payload = load_json(artifact_path)
        artifact_errors, evaluation = _evaluate_review_artifact(
            artifact_payload,
            review_path=artifact_path,
            contract_evidence=contract_evidence,
        )
        errors.extend(f"{prefix}: {error}" for error in artifact_errors)
        if artifact_errors:
            continue
        evaluation["iteration_id"] = f"iteration-{index}"
        for field in (
            "iteration_id",
            "score",
            "passed",
            "screenshot_sha256",
            "implementation_tree_sha256",
            "metric_failures",
            "critical_failures",
        ):
            if iteration.get(field) != evaluation.get(field):
                errors.append(f"{prefix}.{field} does not match its hashed review artifact")
        screenshot_key = tuple(evaluation["screenshot_sha256"])
        if screenshot_key in seen_screenshot_sets:
            errors.append(f"{prefix} reuses a prior screenshot SHA set")
        seen_screenshot_sets.add(screenshot_key)
        runtime_tree = evaluation["implementation_tree_sha256"]
        if runtime_tree in seen_runtime_trees:
            errors.append(f"{prefix} reuses a prior runtime-tree SHA")
        seen_runtime_trees.add(runtime_tree)
        recomputed.append(evaluation)

    latest = recomputed[-1] if recomputed else {}
    if set(latest.get("screenshot_sha256") or []) != screenshot_sha256:
        errors.append("latest reference fidelity review does not cover the current screenshot manifest")
    if latest.get("implementation_tree_sha256") != implementation_tree_sha256:
        errors.append("latest reference fidelity review does not bind the current runtime tree")
    latest_passed = bool(latest.get("passed"))
    if report.get("passed") is not latest_passed or report.get("ready_to_release") is not latest_passed:
        errors.append("reference fidelity report release state does not match the latest review")
    expected_selected = latest.get("iteration_id") if latest_passed else None
    if report.get("selected_iteration") != expected_selected:
        errors.append("reference fidelity report selected_iteration is invalid")
    if not latest_passed:
        errors.append("approved-reference fidelity gate is blocked")

    return errors, {
        "report_path": str(report_path.resolve()),
        "contract_path": str(contract_path.resolve()),
        "contract_sha256": contract_evidence["contract_sha256"],
        "iteration_count": len(recomputed),
        "latest_iteration": latest.get("iteration_id"),
        "latest_score": latest.get("score"),
        "metric_failures": latest.get("metric_failures") or [],
        "critical_failures": latest.get("critical_failures") or [],
    }


def _evaluate_review_artifact(
    review: dict[str, Any],
    *,
    review_path: Path,
    contract_evidence: dict[str, Any],
) -> tuple[list[str], dict[str, Any]]:
    errors: list[str] = []
    if review.get("schema_version") != REVIEW_SCHEMA:
        errors.append(f"review.schema_version must be {REVIEW_SCHEMA}")
    if review.get("contract_sha256") != contract_evidence["contract_sha256"]:
        errors.append("review.contract_sha256 does not match the current contract")
    if _string_set(review.get("reference_sha256")) != set(contract_evidence["reference_sha256"]):
        errors.append("review.reference_sha256 does not match the approved reference set")
    implementation_tree = str(review.get("implementation_tree_sha256") or "")
    if not _is_sha256(implementation_tree):
        errors.append("review.implementation_tree_sha256 must be a SHA-256 digest")
    screenshot_hashes = _string_set(review.get("screenshot_sha256"))
    if not screenshot_hashes or any(not _is_sha256(value) for value in screenshot_hashes):
        errors.append("review.screenshot_sha256 must contain SHA-256 digests")
    if review.get("source") != "multimodal-review":
        errors.append("review.source must be multimodal-review")
    if len(str(review.get("reviewer") or "").strip()) < 3:
        errors.append("review.reviewer is required")
    if len(str(review.get("model") or "").strip()) < 3:
        errors.append("review.model is required")
    if len(str(review.get("method") or "").strip()) < 32:
        errors.append("review.method must describe the paired comparison procedure")
    if not _is_timezone_timestamp(review.get("reviewed_at")):
        errors.append("review.reviewed_at must be an ISO-8601 timestamp with a timezone")

    metric_contracts = contract_evidence["metrics"]
    raw_findings = review.get("metric_findings")
    if not isinstance(raw_findings, dict):
        errors.append("review.metric_findings must be an object")
        raw_findings = {}
    finding_ids = {str(metric_id) for metric_id in raw_findings}
    expected_ids = set(metric_contracts)
    if finding_ids != expected_ids:
        missing = expected_ids - finding_ids
        unexpected = finding_ids - expected_ids
        if missing:
            errors.append("review.metric_findings is missing: " + ", ".join(sorted(missing)))
        if unexpected:
            errors.append("review.metric_findings contains unknown metrics: " + ", ".join(sorted(unexpected)))

    weighted_score = 0.0
    total_weight = 0.0
    normalized_findings: dict[str, dict[str, Any]] = {}
    metric_failures: list[str] = []
    critical_failures: list[str] = []
    observations: set[str] = set()
    for metric_id, metric in metric_contracts.items():
        prefix = f"review.metric_findings.{metric_id}"
        finding = raw_findings.get(metric_id)
        if not isinstance(finding, dict):
            continue
        score = _bounded_score(finding.get("score"), f"{prefix}.score", errors)
        observation = str(finding.get("observation") or "").strip()
        if len(observation) < 40:
            errors.append(f"{prefix}.observation must record concrete paired-image evidence")
        observations.add(observation)
        passed = score >= float(metric["minimum_score"])
        expected_status = "passed" if passed else "failed"
        if finding.get("status") != expected_status:
            errors.append(f"{prefix}.status must be {expected_status} for the recorded score")
        remediation = str(finding.get("remediation") or "").strip()
        if not passed and len(remediation) < 24:
            errors.append(f"{prefix}.remediation is required for a failed invariant")
        normalized_findings[metric_id] = {
            "score": score,
            "status": expected_status,
            "observation": observation,
            "remediation": remediation,
        }
        weight = float(metric["weight"])
        weighted_score += score * weight
        total_weight += weight
        if not passed:
            metric_failures.append(metric_id)
            if metric["critical"]:
                critical_failures.append(metric_id)
    if len(normalized_findings) >= 3 and len(observations) < len(normalized_findings):
        errors.append("review.metric_findings must contain distinct observations")

    score = round(weighted_score / total_weight, 4) if total_weight else 0.0
    passed = (
        not errors
        and score >= float(contract_evidence["threshold"])
        and not metric_failures
        and not critical_failures
    )
    return errors, {
        "artifact": {
            "path": _relative_or_absolute(review_path, Path(contract_evidence["contract_path"]).parent.parent),
            "sha256": sha256_file(review_path),
        },
        "reviewed_at": review.get("reviewed_at"),
        "reviewer": review.get("reviewer"),
        "model": review.get("model"),
        "method": review.get("method"),
        "implementation_tree_sha256": implementation_tree,
        "screenshot_sha256": sorted(screenshot_hashes),
        "reference_sha256": sorted(_string_set(review.get("reference_sha256"))),
        "score": score,
        "threshold": contract_evidence["threshold"],
        "passed": passed,
        "metric_failures": sorted(metric_failures),
        "critical_failures": sorted(critical_failures),
        "metric_findings": normalized_findings,
    }


def _build_correction_brief(iteration: dict[str, Any]) -> dict[str, Any]:
    actions = []
    for metric_id in iteration.get("metric_failures") or []:
        finding = (iteration.get("metric_findings") or {}).get(metric_id) or {}
        actions.append(
            {
                "metric_id": metric_id,
                "observation": finding.get("observation"),
                "required_change": finding.get("remediation"),
            }
        )
    return {
        "source_iteration": iteration.get("iteration_id"),
        "actions": actions,
        "acceptance_criteria": [
            "Apply the failed invariant corrections without copying prohibited reference scopes.",
            "Freeze a new runtime tree and capture a fresh screenshot SHA set.",
            "Run a new paired multimodal review against the unchanged approved contract and reference hashes.",
        ],
    }


def _validate_hashed_file_reference(
    reference: Any,
    *,
    base: Path,
    prefix: str,
    errors: list[str],
) -> dict[str, Any]:
    if not isinstance(reference, dict):
        errors.append(f"{prefix} must be an object")
        return {}
    raw_path = str(reference.get("path") or "").strip()
    expected_sha = str(reference.get("sha256") or "").strip()
    if not raw_path:
        errors.append(f"{prefix}.path is required")
        return {}
    if not _is_sha256(expected_sha):
        errors.append(f"{prefix}.sha256 must be a SHA-256 digest")
    try:
        path = _resolve_within(base, raw_path)
    except ValueError as exc:
        errors.append(f"{prefix}.path {exc}")
        return {}
    if not path.is_file():
        errors.append(f"{prefix}.path does not exist: {raw_path}")
        return {}
    actual_sha = sha256_file(path)
    if expected_sha != actual_sha:
        errors.append(f"{prefix}.sha256 does not match: {raw_path}")
    return {"path": str(path), "sha256": actual_sha}


def _load_hashed_json_artifact(
    reference: Any,
    *,
    base: Path,
    prefix: str,
    errors: list[str],
) -> Path | None:
    evidence = _validate_hashed_file_reference(
        reference,
        base=base,
        prefix=prefix,
        errors=errors,
    )
    return Path(evidence["path"]) if evidence else None


def _resolve_within(base: Path, raw_path: str) -> Path:
    root = base.resolve()
    candidate = Path(raw_path)
    resolved = candidate.resolve() if candidate.is_absolute() else (root / candidate).resolve()
    try:
        resolved.relative_to(root)
    except ValueError as exc:
        raise ValueError(f"must stay inside {root}") from exc
    return resolved


def _relative_or_absolute(path: Path, base: Path) -> str:
    try:
        return path.resolve().relative_to(base.resolve()).as_posix()
    except ValueError:
        return str(path.resolve())


def _bounded_score(value: Any, prefix: str, errors: list[str]) -> float:
    if not isinstance(value, int | float) or isinstance(value, bool):
        errors.append(f"{prefix} must be a number from 0 to 1")
        return 0.0
    score = float(value)
    if not 0.0 <= score <= 1.0:
        errors.append(f"{prefix} must be a number from 0 to 1")
        return 0.0
    return score


def _string_set(value: Any) -> set[str]:
    if not isinstance(value, list):
        return set()
    return {str(item).strip() for item in value if isinstance(item, str) and item.strip()}


def _is_sha256(value: str) -> bool:
    return len(value) == 64 and all(character in "0123456789abcdef" for character in value)


def _is_timezone_timestamp(value: Any) -> bool:
    if not isinstance(value, str) or not value.strip():
        return False
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        return False
    return parsed.tzinfo is not None
