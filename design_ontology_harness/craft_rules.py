"""Human-readable metadata for implementation-audit findings.

The implementation linter remains the executable source of truth.  This
module only gives its stable rule ids names, impact levels, and repair hints
so the unified audit can expose a ranked punch list without running a second
scanner or changing CI blocking semantics.
"""

from __future__ import annotations

import hashlib
import json
from dataclasses import asdict, dataclass
from typing import Any, Iterable


CRAFT_RULESET_VERSION = "design-ontology.craft-rules/v1"
HALLMARK_REFERENCE_REVISION = "13ac0ec7e148655948100b6396439e481361d690"
HALLMARK_REFERENCE_URL = (
    "https://github.com/Nutlope/hallmark/commit/"
    f"{HALLMARK_REFERENCE_REVISION}"
)

SEVERITY_ORDER = {"critical": 0, "major": 1, "minor": 2}


@dataclass(frozen=True)
class CraftRule:
    tell: str
    category: str
    severity: str
    fix: str
    informed_by: str | None = None


RULES: dict[str, CraftRule] = {
    "DS000": CraftRule(
        tell="Unreadable implementation source",
        category="audit-integrity",
        severity="critical",
        fix="Restore a readable UTF-8 source file or exclude the non-source artifact explicitly.",
    ),
    "DS070": CraftRule(
        tell="Homogeneous card wall",
        category="structure",
        severity="major",
        fix="Promote one primary workflow surface and vary the remaining content grammar.",
    ),
    "DS090": CraftRule(
        tell="Document callout grammar in product UI",
        category="visual-language",
        severity="major",
        fix="Replace the side rule with product-native hierarchy, status, or placement.",
    ),
    "DS091": CraftRule(
        tell="Radius monoculture",
        category="visual-language",
        severity="major",
        fix="Reserve rounding for surfaces that need elevation or interaction and use at most two steps.",
    ),
    "DS092": CraftRule(
        tell="Hedged font-weight hierarchy",
        category="typography",
        severity="minor",
        fix="Anchor hierarchy to a smaller intentional set of weights, sizes, and spacing roles.",
    ),
    "DS093": CraftRule(
        tell="Compressed type scale",
        category="typography",
        severity="major",
        fix="Introduce one clear display tier and remove redundant intermediate sizes.",
    ),
    "DS094": CraftRule(
        tell="Placeholder product copy",
        category="content-integrity",
        severity="critical",
        fix="Use supplied domain data or an explicitly labelled unresolved placeholder.",
    ),
    "DS095": CraftRule(
        tell="CSS-painted instrument surface",
        category="visual-substance",
        severity="major",
        fix="Use a semantic SVG, canvas, chart, or data-backed product surface.",
    ),
    "DS096": CraftRule(
        tell="Decorative edge-bar emphasis",
        category="visual-language",
        severity="major",
        fix="Use a short label, glyph, dot, or subtle surface treatment instead of a full-height stripe.",
    ),
    "DS109": CraftRule(
        tell="Unbounded transition",
        category="motion",
        severity="major",
        fix="Name only the properties that should animate.",
        informed_by="Hallmark reference study",
    ),
    "DS110": CraftRule(
        tell="Layout-property transition",
        category="motion",
        severity="critical",
        fix="Animate transform or opacity and keep layout geometry stable.",
        informed_by="Hallmark reference study",
    ),
    "DS111": CraftRule(
        tell="Animation without reduced-motion coverage",
        category="accessibility",
        severity="critical",
        fix="Add a prefers-reduced-motion fallback that removes spatial motion.",
        informed_by="Hallmark reference study",
    ),
    "AUDIT-STYLE-ATTRACTOR": CraftRule(
        tell="Default-attractor sameness",
        category="structure",
        severity="critical",
        fix="Change the structural grammar supported by the brief, not only palette or type.",
        informed_by="Hallmark reference study",
    ),
    "AUDIT-STYLE-REPEAT": CraftRule(
        tell="Repeated structural fingerprint",
        category="structure",
        severity="critical",
        fix="Choose a materially different composition, separation grammar, or workflow surface.",
        informed_by="Hallmark reference study",
    ),
    "AUDIT-DIVERGENCE-ERROR": CraftRule(
        tell="Style-divergence gate could not run",
        category="audit-integrity",
        severity="critical",
        fix="Repair the target or registry input and rerun the enabled gate.",
    ),
    "AUDIT-IMPLEMENTATION-EMPTY": CraftRule(
        tell="No implementation source was audited",
        category="audit-integrity",
        severity="critical",
        fix="Point --target-repo at the runtime source tree and rerun the audit.",
    ),
    "AUDIT-REGISTRATION-ERROR": CraftRule(
        tell="Style fingerprint registration failed",
        category="audit-integrity",
        severity="critical",
        fix="Repair the registry path or payload and rerun the complete audit.",
    ),
    "AUDIT-CONTRACTS-MISSING": CraftRule(
        tell="Required component contracts are missing",
        category="component-contract",
        severity="critical",
        fix="Compile and validate the authored component contract artifacts.",
    ),
    "AUDIT-CONTRACTS-INVALID": CraftRule(
        tell="Component contracts are invalid",
        category="component-contract",
        severity="critical",
        fix="Correct the authored contract source and regenerate its compiled artifact.",
    ),
}


MANUAL_REVIEW_COVERAGE: tuple[dict[str, Any], ...] = (
    {
        "id": "philosophy-hierarchy-specificity-restraint",
        "status": "deferred-to-production-evidence",
        "evidence_kind": "multimodal-aesthetic-review",
        "routed_gate": "apply-aesthetic-review / verify-production-ui",
        "reason": "Intent, hierarchy, specificity, and restraint are visual judgments, not static-code facts.",
    },
    {
        "id": "viewport-fold-overflow-and-clickable-wrap",
        "status": "deferred-to-production-evidence",
        "evidence_kind": "browser",
        "routed_gate": "production-browser-evidence-bundle / verify-production-ui",
        "reason": "Computed layout at mobile widths and 1280x800 requires a rendered browser session.",
    },
    {
        "id": "interaction-and-component-state-coverage",
        "status": "deferred-to-production-evidence",
        "evidence_kind": "component-runtime",
        "routed_gate": "component-runtime-conformance / verify-production-ui",
        "reason": "Focus, active, disabled, loading, error, and transition behavior require runtime evidence.",
    },
    {
        "id": "approved-reference-fidelity",
        "status": "conditional-production-stage",
        "evidence_kind": "paired-multimodal-review",
        "routed_gate": "reference-fidelity-loop",
        "reason": "Only projects with an approved reference contract enter the independent fidelity stage.",
    },
)


def manual_review_coverage() -> list[dict[str, Any]]:
    return [dict(item) for item in MANUAL_REVIEW_COVERAGE]


def reference_studies() -> list[dict[str, Any]]:
    return [
        {
            "name": "Nutlope/hallmark",
            "revision": HALLMARK_REFERENCE_REVISION,
            "url": HALLMARK_REFERENCE_URL,
            "license": "MIT",
            "role": "advisory taxonomy and reporting reference; not a runtime dependency or design authority",
            "adopted": [
                "severity-ranked named findings",
                "structural fingerprint emphasis",
                "bounded motion checks",
                "explicit separation of static and rendered review coverage",
            ],
        }
    ]


def build_punch_list(checks: Iterable[Any]) -> list[dict[str, Any]]:
    findings_by_fingerprint: dict[str, dict[str, Any]] = {}
    for check in checks:
        check_name = str(getattr(check, "name", "unknown"))
        for issue in getattr(check, "issues", []):
            if not isinstance(issue, dict):
                continue
            finding = _normalize_finding(check_name, issue)
            findings_by_fingerprint.setdefault(finding["fingerprint"], finding)
    return sorted(
        findings_by_fingerprint.values(),
        key=lambda item: (
            SEVERITY_ORDER.get(item["severity"], 99),
            item["where"]["path"],
            item["where"]["line"],
            item["rule_id"],
        ),
    )


def _normalize_finding(check_name: str, issue: dict[str, Any]) -> dict[str, Any]:
    rule_id = str(issue.get("code") or "AUDIT-UNKNOWN")
    meta = RULES.get(rule_id)
    severity = meta.severity if meta else _fallback_severity(issue)
    path = str(issue.get("path") or ".")
    line = _positive_int(issue.get("line"), default=1)
    column = _positive_int(issue.get("column"), default=1)
    message = str(issue.get("message") or rule_id)
    snippet = str(issue.get("snippet") or "")
    fingerprint_payload = {
        "rule_id": rule_id,
        "check": check_name,
        "path": path,
        "line": line,
        "column": column,
        "message": message,
        "snippet": snippet,
    }
    fingerprint = hashlib.sha256(
        json.dumps(
            fingerprint_payload,
            ensure_ascii=False,
            sort_keys=True,
            separators=(",", ":"),
        ).encode("utf-8")
    ).hexdigest()
    return {
        "rule_id": rule_id,
        "tell": meta.tell if meta else _fallback_tell(message, rule_id),
        "category": meta.category if meta else _fallback_category(check_name),
        "severity": severity,
        "severity_source": "rule-catalog" if meta else "default-major",
        "blocking": True,
        "check": check_name,
        "where": {"path": path, "line": line, "column": column},
        "evidence_kind": _evidence_kind(check_name),
        "evidence": snippet,
        "rationale": message,
        "fix": meta.fix if meta else message,
        "fingerprint": fingerprint,
        "informed_by": meta.informed_by if meta else None,
    }


def severity_counts(findings: Iterable[dict[str, Any]]) -> dict[str, int]:
    counts = {name: 0 for name in SEVERITY_ORDER}
    for finding in findings:
        severity = str(finding.get("severity") or "")
        if severity in counts:
            counts[severity] += 1
    return counts


def rule_catalog() -> dict[str, dict[str, Any]]:
    return {rule_id: asdict(meta) for rule_id, meta in sorted(RULES.items())}


def _fallback_severity(issue: dict[str, Any]) -> str:
    raw = str(issue.get("severity") or "error").lower()
    return "minor" if raw in {"info", "warning", "warn"} else "major"


def _fallback_tell(message: str, rule_id: str) -> str:
    first_clause = message.split(";", 1)[0].strip().rstrip(".")
    return first_clause or f"Implementation finding {rule_id}"


def _fallback_category(check_name: str) -> str:
    return {
        "implementation-lint": "implementation-contract",
        "style-divergence": "structure",
        "component-contracts": "component-contract",
        "style-registration": "audit-integrity",
    }.get(check_name, "audit")


def _evidence_kind(check_name: str) -> str:
    return {
        "implementation-lint": "static",
        "style-divergence": "fingerprint",
        "component-contracts": "contract",
        "style-registration": "registry",
    }.get(check_name, "static")


def _positive_int(value: Any, *, default: int) -> int:
    try:
        parsed = int(value)
    except (TypeError, ValueError):
        return default
    return parsed if parsed > 0 else default
