"""Unified, provenance-friendly implementation design audit.

The harness already has focused gates for implementation linting, style
divergence, and authored component contracts.  This module composes those
gates into one CI-friendly report and adds explicit, reviewable suppressions.

Suppressions are deliberately kept above the raw implementation linter.  A
caller can still use ``lint_implementation`` as a strict primitive, while the
audit command can document an intentional exception without losing the raw
finding or its location.
"""

from __future__ import annotations

import fnmatch
import hashlib
import importlib.metadata
import json
import re
import subprocess
from dataclasses import asdict, dataclass, field
from datetime import date, datetime, timezone
from functools import lru_cache
from pathlib import Path
from typing import Any

from .component_contracts import load_and_validate_component_contracts
from .craft_rules import (
    CRAFT_RULESET_VERSION,
    build_punch_list,
    manual_review_coverage,
    reference_studies,
    severity_counts,
)
from .implementation_linter import (
    IMPLEMENTATION_LINT_RULESET_VERSION,
    ImplementationIssue,
    lint_implementation,
)
from .style_fingerprint import (
    DEFAULT_COMPARE_LIMIT,
    DEFAULT_SIMILARITY_THRESHOLD,
    StyleFingerprint,
    check_and_register_fingerprint,
    check_style_divergence,
    extract_style_fingerprint,
)


AUDIT_CONFIG_SCHEMA_VERSION = "design-ontology.audit-config/v1"
AUDIT_REPORT_SCHEMA_VERSION = "design-ontology.audit-report/v1"
DEFAULT_AUDIT_CONFIG = Path(".design-ontology") / "audit.json"
DEFAULT_STYLE_REGISTRY = Path("registry") / "style_fingerprints.json"
VALID_CHECK_STATUSES = {"pass", "fail", "skipped"}
EXACT_RULE_CODE_RE = re.compile(r"^[A-Z][A-Z0-9]*(?:-[A-Z0-9]+)*$")
NON_SUPPRESSIBLE_IMPLEMENTATION_RULES = {"DS000"}


class AuditConfigError(ValueError):
    """Raised when a tracked audit configuration cannot be trusted."""


@dataclass
class AuditCheck:
    name: str
    status: str
    required: bool = True
    issues: list[dict[str, Any]] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
    details: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if self.status not in VALID_CHECK_STATUSES:
            raise ValueError(f"unsupported audit check status: {self.status}")
        if self.status == "skipped" and self.required:
            raise ValueError(f"required audit check cannot be skipped: {self.name}")

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass
class DesignAuditReport:
    target_repo: str
    project_dir: str
    project_id: str
    config_path: str | None
    checks: list[AuditCheck] = field(default_factory=list)
    suppressed_issues: list[dict[str, Any]] = field(default_factory=list)
    unused_ignore_rules: list[dict[str, Any]] = field(default_factory=list)
    provenance: dict[str, Any] = field(default_factory=dict)
    registration: dict[str, Any] = field(default_factory=dict)
    schema_version: str = AUDIT_REPORT_SCHEMA_VERSION

    @property
    def ok(self) -> bool:
        return bool(self.checks) and all(
            check.status == "pass" or (check.status == "skipped" and not check.required)
            for check in self.checks
        )

    def to_dict(self) -> dict[str, Any]:
        punch_list = build_punch_list(self.checks)
        return {
            "schema_version": self.schema_version,
            "target_repo": self.target_repo,
            "project_dir": self.project_dir,
            "project_id": self.project_id,
            "config_path": self.config_path,
            "ok": self.ok,
            "checks": [check.to_dict() for check in self.checks],
            "punch_list": punch_list,
            "severity_counts": severity_counts(punch_list),
            "suppressed_issues": self.suppressed_issues,
            "unused_ignore_rules": self.unused_ignore_rules,
            "manual_review_coverage": manual_review_coverage(),
            "provenance": self.provenance,
            "registration": self.registration,
            "reference_studies": reference_studies(),
            "scope": {
                "claim": "static implementation audit",
                "production_readiness": False,
                "production_gate": "verify-production-ui",
            },
            "summary": {
                "check_count": len(self.checks),
                "failed_checks": sum(check.status == "fail" for check in self.checks),
                "skipped_checks": sum(check.status == "skipped" for check in self.checks),
                "issue_count": len(punch_list),
                "normalized_issue_count": len(punch_list),
                "raw_issue_count": (
                    sum(len(check.issues) for check in self.checks)
                    + len(self.suppressed_issues)
                ),
                "suppressed_issue_count": len(self.suppressed_issues),
                "unused_ignore_rule_count": len(self.unused_ignore_rules),
                "required_check_count": sum(check.required for check in self.checks),
                "required_check_failures": sum(
                    check.required and check.status != "pass" for check in self.checks
                ),
            },
        }


def resolve_audit_config_path(
    target_repo: Path,
    config_path: Path | None = None,
) -> Path:
    """Resolve the shared audit config without creating it."""

    target = target_repo.resolve()
    return (config_path if config_path is not None else target / DEFAULT_AUDIT_CONFIG).resolve()


def load_audit_config(
    target_repo: Path,
    *,
    config_path: Path | None = None,
) -> tuple[dict[str, Any], Path | None]:
    """Load and validate audit suppressions.

    The config is optional.  Once present, it is strict: malformed entries
    fail the audit rather than silently broadening an exception.
    """

    path = resolve_audit_config_path(target_repo, config_path)
    if not path.is_file():
        if config_path is not None:
            raise AuditConfigError(f"audit config not found: {path}")
        return {"schema_version": AUDIT_CONFIG_SCHEMA_VERSION, "ignore_rules": []}, None

    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise AuditConfigError(f"invalid audit config {path}: {exc}") from exc
    if not isinstance(payload, dict):
        raise AuditConfigError(f"audit config must be a JSON object: {path}")
    if payload.get("schema_version") != AUDIT_CONFIG_SCHEMA_VERSION:
        raise AuditConfigError(
            f"audit config schema_version must be {AUDIT_CONFIG_SCHEMA_VERSION}: {path}"
        )

    rules = payload.get("ignore_rules", [])
    if not isinstance(rules, list):
        raise AuditConfigError("audit config ignore_rules must be a list")
    seen_rules: set[tuple[str, tuple[str, ...]]] = set()
    for index, rule in enumerate(rules):
        prefix = f"ignore_rules[{index}]"
        if not isinstance(rule, dict):
            raise AuditConfigError(f"{prefix} must be an object")
        code = rule.get("code")
        paths = rule.get("paths")
        reason = rule.get("reason")
        if not isinstance(code, str) or not EXACT_RULE_CODE_RE.fullmatch(code.strip()):
            raise AuditConfigError(
                f"{prefix}.code must be one exact uppercase rule id; wildcards are not allowed"
            )
        normalized_code = code.strip()
        if not normalized_code.startswith("DS"):
            raise AuditConfigError(
                f"{prefix}.code must name an implementation-lint DS rule; audit integrity "
                "and contract gates are not suppressible"
            )
        if normalized_code in NON_SUPPRESSIBLE_IMPLEMENTATION_RULES:
            raise AuditConfigError(f"{prefix}.code {normalized_code} is not suppressible")
        if not isinstance(paths, list) or not paths or any(
            not isinstance(item, str) or not item.strip() for item in paths
        ):
            raise AuditConfigError(f"{prefix}.paths must contain at least one path glob")
        normalized_paths = tuple(item.strip().replace("\\", "/") for item in paths)
        for path_glob in normalized_paths:
            _validate_path_glob(path_glob, prefix=prefix)
        if not isinstance(reason, str) or len(reason.strip()) < 8:
            raise AuditConfigError(f"{prefix}.reason must explain the intentional exception")
        expires_on = rule.get("expires_on")
        if expires_on is not None:
            if not isinstance(expires_on, str) or not re.fullmatch(
                r"\d{4}-\d{2}-\d{2}", expires_on
            ):
                raise AuditConfigError(
                    f"{prefix}.expires_on must be an ISO date (YYYY-MM-DD)"
                )
            try:
                expiry = date.fromisoformat(expires_on)
            except ValueError as exc:
                raise AuditConfigError(
                    f"{prefix}.expires_on must be an ISO date (YYYY-MM-DD)"
                ) from exc
            if expiry < datetime.now(timezone.utc).date():
                raise AuditConfigError(f"{prefix} expired on {expiry.isoformat()}")
        identity = (normalized_code, normalized_paths)
        if identity in seen_rules:
            raise AuditConfigError(f"{prefix} duplicates an earlier code/path rule")
        seen_rules.add(identity)
        rule["code"] = normalized_code
        rule["paths"] = list(normalized_paths)

    return payload, path


def _validate_path_glob(path_glob: str, *, prefix: str) -> None:
    candidate = Path(path_glob)
    segments = path_glob.split("/")
    if (
        candidate.is_absolute()
        or re.match(r"^[A-Za-z]:/", path_glob)
        or any(segment in {"", ".", ".."} for segment in segments)
    ):
        raise AuditConfigError(f"{prefix}.paths must stay within the target repository")
    has_recursive_wildcard = "**" in segments
    has_literal_scope = any(re.search(r"[^*?\[\]]", segment) for segment in segments)
    if (has_recursive_wildcard and not has_literal_scope) or segments == ["*"]:
        raise AuditConfigError(f"{prefix}.paths may not suppress the entire repository")
    if any(marker in segments[0] for marker in ("*", "?", "[")):
        raise AuditConfigError(
            f"{prefix}.paths must start with a literal top-level path segment"
        )
    if path_glob.count("[") != path_glob.count("]"):
        raise AuditConfigError(f"{prefix}.paths contains an unbalanced bracket glob")
    if "\x00" in path_glob:
        raise AuditConfigError(f"{prefix}.paths contains a NUL byte")


def _issue_dict(issue: ImplementationIssue) -> dict[str, Any]:
    return issue.to_dict()


def _rule_matches(issue: dict[str, Any], rule: dict[str, Any]) -> bool:
    if str(issue.get("code", "")) != str(rule["code"]):
        return False
    path = str(issue.get("path", ""))
    return any(_path_glob_matches(path, pattern) for pattern in rule["paths"])


def _path_glob_matches(path: str, pattern: str) -> bool:
    """Match POSIX paths with ``*`` confined to one segment and ``**`` recursive."""

    path_parts = tuple(part for part in path.replace("\\", "/").split("/") if part)
    pattern_parts = tuple(pattern.split("/"))

    @lru_cache(maxsize=None)
    def match(path_index: int, pattern_index: int) -> bool:
        if pattern_index == len(pattern_parts):
            return path_index == len(path_parts)
        segment = pattern_parts[pattern_index]
        if segment == "**":
            return match(path_index, pattern_index + 1) or (
                path_index < len(path_parts) and match(path_index + 1, pattern_index)
            )
        return (
            path_index < len(path_parts)
            and fnmatch.fnmatchcase(path_parts[path_index], segment)
            and match(path_index + 1, pattern_index + 1)
        )

    return match(0, 0)


def apply_audit_suppressions(
    issues: list[ImplementationIssue],
    rules: list[dict[str, Any]],
) -> tuple[list[ImplementationIssue], list[dict[str, Any]], set[int]]:
    """Partition raw issues and preserve evidence for every suppressed finding."""

    visible: list[ImplementationIssue] = []
    suppressed: list[dict[str, Any]] = []
    used_rule_indexes: set[int] = set()
    for issue in issues:
        issue_data = _issue_dict(issue)
        match_index = next(
            (index for index, rule in enumerate(rules) if _rule_matches(issue_data, rule)),
            None,
        )
        if match_index is None:
            visible.append(issue)
            continue
        used_rule_indexes.add(match_index)
        suppressed.append(
            {
                **issue_data,
                "suppression": {
                    "rule_index": match_index,
                    "code": rules[match_index]["code"],
                    "paths": rules[match_index]["paths"],
                    "reason": rules[match_index]["reason"],
                    "owner": rules[match_index].get("owner"),
                    "ticket": rules[match_index].get("ticket"),
                    "expires_on": rules[match_index].get("expires_on"),
                },
            }
        )
    return visible, suppressed, used_rule_indexes


def _component_paths(project_dir: Path) -> tuple[Path, Path] | None:
    specs_path = project_dir / "build" / "system" / "components" / "component_specs.json"
    if not specs_path.is_file():
        return None
    tokens_path = project_dir / "design-system" / "tokens.css"
    return specs_path, tokens_path


def _run_contract_check(
    project_dir: Path,
    *,
    require_contracts: bool,
) -> AuditCheck:
    paths = _component_paths(project_dir)
    if paths is None:
        message = (
            "component_specs.json not found under build/system/components; "
            "provide --project-dir or use --require-contracts"
        )
        return AuditCheck(
            name="component-contracts",
            status="fail" if require_contracts else "skipped",
            required=require_contracts,
            warnings=[message] if not require_contracts else [],
            issues=[
                {
                    "code": "AUDIT-CONTRACTS-MISSING",
                    "path": str(project_dir),
                    "line": 0,
                    "column": 0,
                    "message": message,
                    "snippet": str(project_dir),
                    "severity": "error",
                }
            ]
            if require_contracts
            else [],
        )

    specs_path, tokens_path = paths
    for path in (specs_path, tokens_path):
        resolved = path.resolve()
        if not resolved.is_relative_to(project_dir.resolve()):
            return AuditCheck(
                name="component-contracts",
                status="fail",
                required=True,
                issues=[
                    {
                        "code": "AUDIT-CONTRACTS-INVALID",
                        "path": path.relative_to(project_dir).as_posix(),
                        "line": 1,
                        "column": 1,
                        "message": "Component contract input resolves outside the project directory.",
                        "snippet": str(resolved),
                        "severity": "error",
                    }
                ],
            )
    try:
        details = load_and_validate_component_contracts(
            specs_path,
            tokens_path=tokens_path,
            strict_authored=True,
        )
    except (OSError, TypeError, ValueError, AttributeError, json.JSONDecodeError) as exc:
        return AuditCheck(
            name="component-contracts",
            status="fail",
            required=True,
            issues=[
                {
                    "code": "AUDIT-CONTRACTS-INVALID",
                    "path": specs_path.relative_to(project_dir).as_posix(),
                    "line": 1,
                    "column": 1,
                    "message": str(exc),
                    "snippet": str(specs_path),
                    "severity": "error",
                }
            ],
        )
    return AuditCheck(
        name="component-contracts",
        status="pass" if details.get("ok") else "fail",
        required=True,
        issues=[
            {
                "code": "AUDIT-CONTRACTS-INVALID",
                "path": specs_path.relative_to(project_dir).as_posix(),
                "line": 1,
                "column": 1,
                "message": error,
                "snippet": error,
                "severity": "error",
            }
            for error in details.get("errors", [])
        ],
        warnings=list(details.get("warnings", [])),
        details={
            **details,
            "specs_path": specs_path.relative_to(project_dir).as_posix(),
            "tokens_path": (
                tokens_path.relative_to(project_dir).as_posix()
            ),
        },
    )


def run_design_audit(
    target_repo: Path,
    *,
    project_dir: Path | None = None,
    project_id: str | None = None,
    artifact_dir: str = "design-system",
    config_path: Path | None = None,
    registry_path: Path | None = None,
    threshold: float = DEFAULT_SIMILARITY_THRESHOLD,
    limit: int = DEFAULT_COMPARE_LIMIT,
    include_divergence: bool = True,
    include_contracts: bool = True,
    require_contracts: bool = False,
    register_on_pass: bool = False,
) -> DesignAuditReport:
    """Run the implementation gates as one deterministic audit."""

    target = target_repo.resolve()
    if not target.is_dir():
        raise ValueError(f"target repository is not a directory: {target}")
    project = (project_dir or target_repo).resolve()
    if project_dir is not None and not project.is_dir():
        raise ValueError(f"project directory is not a directory: {project}")
    if not 0.0 < threshold <= 1.0:
        raise ValueError("style similarity threshold must be greater than 0 and at most 1")
    if limit <= 0:
        raise ValueError("style comparison limit must be a positive integer")
    artifact_path = Path(artifact_dir)
    if (
        not artifact_dir.strip()
        or artifact_path.is_absolute()
        or any(part in {"", ".", ".."} for part in artifact_path.parts)
    ):
        raise ValueError("artifact directory must be a relative path inside the target")
    resolved_project_id = (project_id or target.name).strip()
    if not resolved_project_id or any(ord(char) < 32 for char in resolved_project_id):
        raise ValueError("project id must be a non-empty printable string")
    if not include_contracts and require_contracts:
        raise ValueError("--skip-contracts cannot be combined with --require-contracts")
    if not include_divergence and register_on_pass:
        raise ValueError("--skip-divergence cannot be combined with --register-on-pass")

    # Validate every root/nested generated artifact directory before the linter
    # can resolve tokens or font CSS through it.
    _artifact_roots(target, artifact_dir)
    _validate_project_inputs(project)
    project_input_paths = _project_input_paths(project)
    project_read_evidence = _file_set_evidence(project, project_input_paths)["files"]

    config, resolved_config = load_audit_config(target, config_path=config_path)
    rules = config.get("ignore_rules", [])
    divergence_registry = (registry_path or DEFAULT_STYLE_REGISTRY).resolve()
    auxiliary_input_paths = _implementation_input_paths(
        target,
        checked_files=[],
        artifact_dir=artifact_dir,
    )
    auxiliary_read_evidence = _file_set_evidence(
        target,
        auxiliary_input_paths,
    )["files"]

    implementation = lint_implementation(target, artifact_dir=artifact_dir)
    visible, suppressed, used_rules = apply_audit_suppressions(implementation.issues, rules)
    implementation_issues = [_issue_dict(issue) for issue in visible]
    runtime_files = list(implementation.substantive_files)
    if not runtime_files:
        implementation_issues.append(
            {
                "code": "AUDIT-IMPLEMENTATION-EMPTY",
                "path": ".",
                "line": 1,
                "column": 1,
                "message": "No supported implementation files were found under the target repository.",
                "snippet": str(target),
                "severity": "error",
            }
        )
    implementation_check = AuditCheck(
        name="implementation-lint",
        status="pass" if not implementation_issues else "fail",
        required=True,
        issues=implementation_issues,
        details={
            "target_repo": implementation.target_repo,
            "artifact_dir": implementation.artifact_dir,
            "checked_files": implementation.checked_files,
            "runtime_files": runtime_files,
            "ruleset_version": implementation.ruleset_version,
            "raw_issue_count": len(implementation.issues),
            "visible_issue_count": len(visible),
            "suppressed_issue_count": len(suppressed),
        },
    )
    checks = [implementation_check]
    fingerprint: StyleFingerprint | None = None
    style_source_files: list[str] = []
    style_read_evidence: dict[str, dict[str, Any]] = {}
    compared_registry_sha256: str | None = None

    if include_divergence:
        try:
            fingerprint = extract_style_fingerprint(
                target,
                project_name=resolved_project_id,
                read_evidence=style_read_evidence,
            )
            style_source_files = list(fingerprint.source_files)
            divergence = check_style_divergence(
                project,
                registry_path=divergence_registry,
                threshold=threshold,
                limit=limit,
                fingerprint=fingerprint,
            )
            compared_registry_sha256 = str(
                divergence.get("registry_snapshot_sha256") or ""
            ) or None
            divergence_issues = _divergence_issues(divergence)
            divergence_check = AuditCheck(
                name="style-divergence",
                status="pass" if divergence.get("verdict") == "ok" else "fail",
                required=True,
                issues=divergence_issues,
                warnings=list(divergence.get("warnings", [])),
                details=divergence,
            )
            checks.append(divergence_check)
        except (FileNotFoundError, OSError, TypeError, ValueError, AttributeError) as exc:
            checks.append(
                AuditCheck(
                    name="style-divergence",
                    status="fail",
                    required=True,
                    issues=[
                        {
                            "code": "AUDIT-DIVERGENCE-ERROR",
                            "path": ".",
                            "line": 1,
                            "column": 1,
                            "message": str(exc),
                            "snippet": str(divergence_registry),
                            "severity": "error",
                        }
                    ],
                    details={"registry_path": str(divergence_registry)},
                )
            )
    else:
        checks.append(
            AuditCheck(
                name="style-divergence",
                status="skipped",
                required=False,
                warnings=["disabled by --skip-divergence"],
            )
        )

    if include_contracts:
        checks.append(
            _run_contract_check(project, require_contracts=require_contracts)
        )
    else:
        checks.append(
            AuditCheck(
                name="component-contracts",
                status="skipped",
                required=False,
                warnings=["disabled by --skip-contracts"],
            )
        )

    unused = [
        {
            "rule_index": index,
            "code": rule["code"],
            "paths": rule["paths"],
            "reason": rule["reason"],
            "owner": rule.get("owner"),
            "ticket": rule.get("ticket"),
            "expires_on": rule.get("expires_on"),
        }
        for index, rule in enumerate(rules)
        if index not in used_rules
    ]
    report = DesignAuditReport(
        target_repo=str(target),
        project_dir=str(project),
        project_id=resolved_project_id,
        config_path=str(resolved_config) if resolved_config else None,
        checks=checks,
        suppressed_issues=suppressed,
        unused_ignore_rules=unused,
        provenance=_build_provenance(
            target=target,
            project=project,
            checked_files=implementation.checked_files,
            style_source_files=style_source_files,
            implementation_read_evidence=implementation.input_evidence,
            style_read_evidence=list(style_read_evidence.values()),
            auxiliary_input_paths=auxiliary_input_paths,
            auxiliary_read_evidence=auxiliary_read_evidence,
            project_input_paths=project_input_paths,
            project_read_evidence=project_read_evidence,
            artifact_dir=artifact_dir,
            config_path=resolved_config,
            registry_path=divergence_registry,
            compared_registry_sha256=compared_registry_sha256,
            options={
                "artifact_dir": artifact_dir,
                "project_id": resolved_project_id,
                "threshold": threshold,
                "limit": limit,
                "include_divergence": include_divergence,
                "include_contracts": include_contracts,
                "require_contracts": require_contracts,
                "register_on_pass": register_on_pass,
            },
        ),
        registration={
            "requested": register_on_pass,
            "performed": False,
            "registry_path": str(divergence_registry),
        },
    )

    if register_on_pass and report.ok and fingerprint is not None:
        try:
            registration_check, entry = check_and_register_fingerprint(
                project,
                registry_path=divergence_registry,
                fingerprint=fingerprint,
                threshold=threshold,
                limit=limit,
                note="registered after complete unified design audit pass",
            )
            report.registration["registry_recheck"] = registration_check
            if entry is None:
                report.checks.append(
                    AuditCheck(
                        name="style-registration",
                        status="fail",
                        required=True,
                        issues=_divergence_issues(registration_check),
                        warnings=[
                            "registry changed after the initial divergence check; registration was withheld"
                        ],
                        details=registration_check,
                    )
                )
                report.registration["reason"] = (
                    "style divergence no longer passed under the registry write lock"
                )
            else:
                report.registration.update(
                    {
                        "performed": True,
                        "entry": entry,
                        "registry_after": _file_evidence(divergence_registry),
                    }
                )
        except (OSError, TypeError, ValueError, AttributeError) as exc:
            report.checks.append(
                AuditCheck(
                    name="style-registration",
                    status="fail",
                    required=True,
                    issues=[
                        {
                            "code": "AUDIT-REGISTRATION-ERROR",
                            "path": str(divergence_registry),
                            "line": 1,
                            "column": 1,
                            "message": str(exc),
                            "snippet": str(divergence_registry),
                            "severity": "error",
                        }
                    ],
                )
            )
            report.registration["error"] = str(exc)
    elif register_on_pass and not report.ok:
        report.registration["reason"] = "overall audit did not pass"
    return report


def _divergence_issues(report: dict[str, Any]) -> list[dict[str, Any]]:
    fingerprint = report.get("fingerprint") or {}
    source_files = fingerprint.get("source_files") or ["."]
    path = str(source_files[0])
    issues: list[dict[str, Any]] = []
    for attractor in report.get("attractor_matches") or []:
        issues.append(
            {
                "code": "AUDIT-STYLE-ATTRACTOR",
                "path": path,
                "line": 1,
                "column": 1,
                "message": str(attractor.get("label") or "Known style attractor matched"),
                "snippet": str(attractor.get("description") or attractor.get("id") or ""),
                "severity": "error",
            }
        )
    for comparison in report.get("too_similar_to") or []:
        reasons = comparison.get("reasons") or []
        similarity = float(comparison.get("similarity") or 0.0)
        issues.append(
            {
                "code": "AUDIT-STYLE-REPEAT",
                "path": path,
                "line": 1,
                "column": 1,
                "message": (
                    f"Structural/style fingerprint repeats {comparison.get('project_b')} "
                    f"(similarity={similarity:.2f})."
                ),
                "snippet": "; ".join(str(reason) for reason in reasons),
                "severity": "error",
            }
        )
    if report.get("verdict") == "fail" and not issues:
        issues.append(
            {
                "code": "AUDIT-STYLE-REPEAT",
                "path": path,
                "line": 1,
                "column": 1,
                "message": "Style divergence failed without a normalized comparison record.",
                "snippet": json.dumps(report, ensure_ascii=False, sort_keys=True),
                "severity": "error",
            }
        )
    return issues


def _build_provenance(
    *,
    target: Path,
    project: Path,
    checked_files: list[str],
    style_source_files: list[str],
    implementation_read_evidence: list[dict[str, Any]],
    style_read_evidence: list[dict[str, Any]],
    auxiliary_input_paths: list[str],
    auxiliary_read_evidence: list[dict[str, Any]],
    project_input_paths: list[str],
    project_read_evidence: list[dict[str, Any]],
    artifact_dir: str,
    config_path: Path | None,
    registry_path: Path,
    compared_registry_sha256: str | None,
    options: dict[str, Any],
) -> dict[str, Any]:
    implementation_inputs = _implementation_input_paths(
        target,
        checked_files=checked_files,
        artifact_dir=artifact_dir,
    )
    current_auxiliary_paths = _implementation_input_paths(
        target,
        checked_files=[],
        artifact_dir=artifact_dir,
    )
    if current_auxiliary_paths != auxiliary_input_paths:
        raise ValueError("audit auxiliary input set changed while enabled checks were running")
    if _project_input_paths(project) != project_input_paths:
        raise ValueError("audit project input set changed while enabled checks were running")
    target_inputs = sorted(set(implementation_inputs) | set(style_source_files))
    combined_read_evidence = _merge_read_evidence(
        implementation_read_evidence,
        style_read_evidence,
        auxiliary_read_evidence,
    )
    package_root = Path(__file__).resolve().parent
    return {
        "generated_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "tool": {
            "name": "design-ontology-harness",
            "version": _package_version(),
            "rulesets": {
                "implementation": IMPLEMENTATION_LINT_RULESET_VERSION,
                "craft_reporting": CRAFT_RULESET_VERSION,
            },
        },
        "target_git": _git_state(target),
        "project_git": _git_state(project),
        "project_input_snapshot": _file_set_evidence(
            project,
            project_input_paths,
            expected_evidence=_merge_read_evidence(project_read_evidence),
        ),
        "target_snapshot": _file_set_evidence(
            target,
            target_inputs,
            expected_evidence=combined_read_evidence,
        ),
        "implementation_input_snapshot": _file_set_evidence(
            target,
            implementation_inputs,
            expected_evidence=_merge_read_evidence(
                implementation_read_evidence,
                auxiliary_read_evidence,
            ),
        ),
        "style_source_snapshot": _file_set_evidence(
            target,
            style_source_files,
            expected_evidence=_merge_read_evidence(style_read_evidence),
        ),
        "ruleset_source_snapshot": _file_set_evidence(
            package_root,
            [
                path.relative_to(package_root).as_posix()
                for path in sorted(package_root.rglob("*.py"))
                if path.is_file()
            ],
        ),
        "config": _file_evidence(config_path),
        "registry_before": _registry_evidence(
            registry_path,
            compared_snapshot_sha256=compared_registry_sha256,
        ),
        "project_artifacts": [
            evidence
            for evidence in (
                _rooted_file_evidence(project, project / "brand_profile.json"),
                _rooted_file_evidence(
                    project,
                    project / "build" / "system" / "blueprint" / "design_system_blueprint.json"
                ),
                _rooted_file_evidence(
                    project,
                    project / "build" / "system" / "components" / "component_specs.json"
                ),
                _rooted_file_evidence(project, project / "design-system" / "tokens.css"),
            )
            if evidence is not None
        ],
        "options": options,
        "consistency": {
            "source_read_hashes_verified": True,
            "auxiliary_pre_post_hashes_verified": True,
            "capture": "read-time source sha256 and pre/post auxiliary sha256 verified after checks",
        },
    }


def _implementation_input_paths(
    target: Path,
    *,
    checked_files: list[str],
    artifact_dir: str,
) -> list[str]:
    """Include non-source artifacts read by implementation lint in provenance."""

    relative_paths = set(checked_files)
    tree_roots = [
        *_artifact_roots(target, artifact_dir),
        target / "public" / "generated" / "design-system",
    ]
    for tree_root in tree_roots:
        if not tree_root.exists():
            continue
        for path in tree_root.rglob("*"):
            if not path.is_file():
                continue
            resolved = path.resolve()
            if not resolved.is_relative_to(target):
                raise ValueError(f"implementation lint input resolves outside target: {path}")
            relative_paths.add(resolved.relative_to(target).as_posix())
    candidates = [
        target / artifact_dir / "tokens.css",
        target / "public" / "generated" / "design-system" / "manifest.json",
        target / "design-system" / "generated_visual_assets.json",
        target / "brand_profile.json",
        target / "build" / "system" / "blueprint" / "component_inventory.json",
        target / "build" / "system" / "components" / "component_specs.json",
    ]
    for candidate in candidates:
        resolved = candidate.resolve()
        if candidate.is_file() and not resolved.is_relative_to(target):
            raise ValueError(
                f"implementation lint input resolves outside target: {candidate} -> {resolved}"
            )
        if resolved.is_file() and resolved.is_relative_to(target):
            relative_paths.add(resolved.relative_to(target).as_posix())
    for manifest_path in candidates[1:3]:
        if not manifest_path.is_file():
            continue
        try:
            manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        except (OSError, UnicodeDecodeError, json.JSONDecodeError):
            continue
        assets = manifest.get("assets") if isinstance(manifest, dict) else None
        if not isinstance(assets, list):
            continue
        for asset in assets:
            if not isinstance(asset, dict) or not asset.get("asset_path"):
                continue
            asset_path = (target / str(asset["asset_path"])).resolve()
            if asset_path.is_file() and not asset_path.is_relative_to(target):
                raise ValueError(
                    "visual asset input resolves outside target: "
                    f"{asset['asset_path']} -> {asset_path}"
                )
            if asset_path.is_file() and asset_path.is_relative_to(target):
                relative_paths.add(asset_path.relative_to(target).as_posix())
    return sorted(relative_paths)


def _artifact_roots(target: Path, artifact_dir: str) -> list[Path]:
    """Return all root and nested artifact dirs, rejecting symlink escapes."""

    target = target.resolve()
    artifact_parts = Path(artifact_dir).parts
    if not artifact_parts:
        return []
    roots: set[Path] = set()
    for candidate in target.rglob(artifact_parts[-1]):
        if not candidate.is_dir():
            continue
        relative_parts = candidate.relative_to(target).parts
        if tuple(relative_parts[-len(artifact_parts) :]) != artifact_parts:
            continue
        resolved = candidate.resolve()
        if not resolved.is_relative_to(target):
            raise ValueError(
                f"artifact directory resolves outside target: {candidate} -> {resolved}"
            )
        roots.add(resolved)
    return sorted(roots)


def _validate_project_inputs(project: Path) -> None:
    project = project.resolve()
    for path in (
        project / "brand_profile.json",
        project / "build" / "system" / "blueprint" / "component_inventory.json",
        project / "build" / "system" / "blueprint" / "design_system_blueprint.json",
        project / "build" / "system" / "components" / "component_specs.json",
        project / "design-system" / "tokens.css",
    ):
        if path.is_file() and not path.resolve().is_relative_to(project):
            raise ValueError(
                f"project audit input resolves outside project: {path} -> {path.resolve()}"
            )


def _project_input_paths(project: Path) -> list[str]:
    project = project.resolve()
    paths = (
        project / "brand_profile.json",
        project / "build" / "system" / "blueprint" / "component_inventory.json",
        project / "build" / "system" / "blueprint" / "design_system_blueprint.json",
        project / "build" / "system" / "components" / "component_specs.json",
        project / "design-system" / "tokens.css",
    )
    return sorted(
        path.resolve().relative_to(project).as_posix()
        for path in paths
        if path.is_file()
    )


def _merge_read_evidence(
    *groups: list[dict[str, Any]],
) -> dict[str, dict[str, Any]]:
    merged: dict[str, dict[str, Any]] = {}
    for group in groups:
        for record in group:
            relative = str(record.get("path") or "")
            digest = str(record.get("sha256") or "")
            if not relative or not re.fullmatch(r"[a-f0-9]{64}", digest):
                raise ValueError("audit gate returned malformed read-time input evidence")
            previous = merged.get(relative)
            if previous is not None and previous.get("sha256") != digest:
                raise ValueError(
                    f"audit input changed between enabled checks: {relative}"
                )
            merged[relative] = dict(record)
    return merged


def _file_set_evidence(
    root: Path,
    relative_paths: list[str],
    *,
    expected_evidence: dict[str, dict[str, Any]] | None = None,
) -> dict[str, Any]:
    root = root.resolve()
    records: list[dict[str, Any]] = []
    for relative in sorted(set(relative_paths)):
        path = (root / relative).resolve()
        if not path.is_relative_to(root):
            raise ValueError(f"audit input resolves outside evidence root: {relative} -> {path}")
        if not path.is_file():
            raise ValueError(f"audit input disappeared before provenance capture: {relative}")
        record = {
            "path": relative,
            "sha256": _sha256(path),
            "size_bytes": path.stat().st_size,
        }
        expected = (expected_evidence or {}).get(relative)
        if expected is not None and (
            expected.get("sha256") != record["sha256"]
            or expected.get("size_bytes") != record["size_bytes"]
        ):
            raise ValueError(f"audit input changed after it was read: {relative}")
        records.append(record)
    missing_expected = set(expected_evidence or {}) - {record["path"] for record in records}
    if missing_expected:
        raise ValueError(
            "read-time audit inputs were omitted from provenance: "
            + ", ".join(sorted(missing_expected))
        )
    canonical = json.dumps(
        records,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")
    return {
        "algorithm": "sha256-audit-file-set-v1",
        "sha256": hashlib.sha256(canonical).hexdigest(),
        "file_count": len(records),
        "files": records,
    }


def _file_evidence(path: Path | None) -> dict[str, Any] | None:
    if path is None or not path.is_file():
        return None
    resolved = path.resolve()
    return {
        "path": str(resolved),
        "sha256": _sha256(resolved),
        "size_bytes": resolved.stat().st_size,
    }


def _rooted_file_evidence(root: Path, path: Path) -> dict[str, Any] | None:
    if not path.is_file():
        return None
    resolved_root = root.resolve()
    resolved = path.resolve()
    if not resolved.is_relative_to(resolved_root):
        raise ValueError(f"audit evidence input resolves outside root: {path} -> {resolved}")
    return _file_evidence(resolved)


def _registry_evidence(
    path: Path,
    *,
    compared_snapshot_sha256: str | None = None,
) -> dict[str, Any]:
    evidence = _file_evidence(path) or {"path": str(path.resolve()), "sha256": None}
    evidence["compared_snapshot_sha256"] = compared_snapshot_sha256
    evidence["entry_count"] = None
    if not path.is_file():
        return evidence
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeDecodeError, json.JSONDecodeError):
        return evidence
    entries = payload.get("entries") if isinstance(payload, dict) else None
    evidence["entry_count"] = len(entries) if isinstance(entries, list) else None
    return evidence


def _git_state(target: Path) -> dict[str, Any]:
    result: dict[str, Any] = {
        "repository": False,
        "head": None,
        "branch": None,
        "dirty": None,
    }
    try:
        head = _git(target, "rev-parse", "HEAD")
    except OSError:
        return result
    if head is None:
        return result
    result.update(
        {
            "repository": True,
            "head": head,
            "branch": _git(target, "rev-parse", "--abbrev-ref", "HEAD"),
            "dirty": bool(_git(target, "status", "--porcelain")),
        }
    )
    return result


def _git(target: Path, *args: str) -> str | None:
    completed = subprocess.run(
        ["git", "-C", str(target), *args],
        text=True,
        capture_output=True,
        check=False,
    )
    if completed.returncode != 0:
        return None
    return completed.stdout.strip()


def _package_version() -> str:
    try:
        return importlib.metadata.version("design-ontology-harness")
    except importlib.metadata.PackageNotFoundError:
        return "unknown"


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def format_audit_report(report: DesignAuditReport) -> str:
    verdict = "PASS" if report.ok else "FAIL"
    lines = [f"Design audit: {verdict} ({report.target_repo})"]
    for check in report.checks:
        requirement = "required" if check.required else "optional"
        lines.append(
            f"  [{check.status.upper()}] {check.name}: "
            f"{len(check.issues)} issues ({requirement})"
        )
        for warning in check.warnings:
            lines.append(f"    [WARN] {warning}")

    punch_list = build_punch_list(report.checks)
    if punch_list:
        lines.append("Ranked punch list:")
        for finding in punch_list:
            where = finding["where"]
            location = f"{where['path']}:{where['line']}:{where['column']}"
            lines.append(
                f"  [{finding['severity'].upper()}] [{finding['rule_id']}] "
                f"{finding['tell']} — {location}"
            )
            lines.append(f"    Fix: {finding['fix']}")
    counts = severity_counts(punch_list)
    lines.append(
        f"  {counts['critical']} critical · {counts['major']} major · {counts['minor']} minor"
    )
    if report.suppressed_issues:
        lines.append(f"  [SUPPRESSED] {len(report.suppressed_issues)} issue(s) with tracked reasons")
    if report.unused_ignore_rules:
        lines.append(f"  [WARN] {len(report.unused_ignore_rules)} ignore rule(s) matched nothing")
    if report.registration.get("requested"):
        state = "registered" if report.registration.get("performed") else "not registered"
        lines.append(f"  [REGISTRY] {state}: {report.registration.get('registry_path')}")
    lines.append(
        "  [SCOPE] Static audit only; rendered/manual coverage remains with "
        "reference-fidelity and verify-production-ui."
    )
    return "\n".join(lines)


def format_audit_json(report: DesignAuditReport) -> str:
    return json.dumps(report.to_dict(), ensure_ascii=False, indent=2)


def format_audit_error_json(exc: Exception) -> str:
    return json.dumps(
        {
            "schema_version": "design-ontology.audit-error/v1",
            "ok": False,
            "error": {
                "type": exc.__class__.__name__,
                "message": str(exc),
            },
        },
        ensure_ascii=False,
        indent=2,
    )
