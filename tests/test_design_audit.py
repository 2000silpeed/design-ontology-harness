from __future__ import annotations

import json
import subprocess
import sys
from dataclasses import replace
from pathlib import Path

import pytest
import design_ontology_harness.design_audit as design_audit_module

from design_ontology_harness.design_audit import (
    AuditCheck,
    AuditConfigError,
    DesignAuditReport,
    _path_glob_matches,
    apply_audit_suppressions,
    load_audit_config,
    run_design_audit,
)
from design_ontology_harness.implementation_linter import ImplementationIssue
from design_ontology_harness.style_fingerprint import (
    extract_style_fingerprint,
    register_fingerprint,
)


REPO_ROOT = Path(__file__).resolve().parent.parent


def _issue(code: str, path: str) -> ImplementationIssue:
    return ImplementationIssue(
        code=code,
        path=path,
        line=4,
        column=2,
        message="test finding",
        snippet="test finding",
    )


def _write_clean_target(tmp_path: Path, name: str = "target") -> Path:
    target = tmp_path / name
    artifact = target / "design-system"
    artifact.mkdir(parents=True)
    (artifact / "tokens.css").write_text(
        """
        :root {
          --ds-color-canvas: #15130f;
          --ds-color-ink: #f4eee4;
          --ds-color-accent: #d96a2b;
        }
        """,
        encoding="utf-8",
    )
    (target / "index.html").write_text(
        "<html><head><link rel='stylesheet' href='styles.css'></head><body><main>Audit</main></body></html>",
        encoding="utf-8",
    )
    (target / "styles.css").write_text(
        "body { background: var(--ds-color-canvas); color: var(--ds-color-ink); }",
        encoding="utf-8",
    )
    return target


def test_suppressions_match_code_and_path_and_keep_provenance() -> None:
    issues = [_issue("DS001", "src/legacy.css"), _issue("DS002", "src/legacy.css")]
    visible, suppressed, used = apply_audit_suppressions(
        issues,
        [
            {
                "code": "DS001",
                "paths": ["src/**"],
                "reason": "Legacy vendor stylesheet is being migrated in a tracked task.",
                "owner": "design-platform",
            }
        ],
    )

    assert [item.code for item in visible] == ["DS002"]
    assert suppressed[0]["code"] == "DS001"
    assert suppressed[0]["suppression"]["reason"].startswith("Legacy vendor")
    assert used == {0}


def test_audit_config_requires_schema_and_reason(tmp_path: Path) -> None:
    config = tmp_path / "audit.json"
    config.write_text(
        json.dumps(
            {
                "schema_version": "design-ontology.audit-config/v1",
                "ignore_rules": [{"code": "DS001", "paths": ["src/**"]}],
            }
        ),
        encoding="utf-8",
    )

    with pytest.raises(AuditConfigError, match="reason"):
        load_audit_config(tmp_path, config_path=config)


def test_audit_config_rejects_wildcard_rule_ids_and_repository_wide_globs(
    tmp_path: Path,
) -> None:
    config = tmp_path / "audit.json"
    config.write_text(
        json.dumps(
            {
                "schema_version": "design-ontology.audit-config/v1",
                "ignore_rules": [
                    {
                        "code": "*",
                        "paths": ["**/*"],
                        "reason": "This would silence every implementation finding.",
                    }
                ],
            }
        ),
        encoding="utf-8",
    )

    with pytest.raises(AuditConfigError, match="exact uppercase rule id"):
        load_audit_config(tmp_path, config_path=config)


def test_audit_check_rejects_unknown_or_required_skipped_status() -> None:
    with pytest.raises(ValueError, match="unsupported"):
        AuditCheck(name="bad", status="error")
    with pytest.raises(ValueError, match="required audit check"):
        AuditCheck(name="bad", status="skipped")


def test_suppression_globs_are_path_segment_aware() -> None:
    assert _path_glob_matches("src/file.css", "src/*.css")
    assert not _path_glob_matches("src/deep/file.css", "src/*.css")
    assert _path_glob_matches("src/file.css", "src/**/*.css")
    assert _path_glob_matches("src/deep/file.css", "src/**/*.css")


def test_audit_config_rejects_equivalent_blanket_glob_and_audit_rule(tmp_path: Path) -> None:
    config = tmp_path / "audit.json"
    config.write_text(
        json.dumps(
            {
                "schema_version": "design-ontology.audit-config/v1",
                "ignore_rules": [
                    {
                        "code": "DS001",
                        "paths": ["**/**"],
                        "reason": "This would still silence the complete repository.",
                    }
                ],
            }
        ),
        encoding="utf-8",
    )
    with pytest.raises(AuditConfigError, match="entire repository"):
        load_audit_config(tmp_path, config_path=config)

    config.write_text(
        json.dumps(
            {
                "schema_version": "design-ontology.audit-config/v1",
                "ignore_rules": [
                    {
                        "code": "DS001",
                        "paths": ["**/*.*"],
                        "reason": "An extension wildcard is still too broad without a literal prefix.",
                    }
                ],
            }
        ),
        encoding="utf-8",
    )
    with pytest.raises(AuditConfigError, match="literal top-level"):
        load_audit_config(tmp_path, config_path=config)

    config.write_text(
        json.dumps(
            {
                "schema_version": "design-ontology.audit-config/v1",
                "ignore_rules": [
                    {
                        "code": "AUDIT-CONTRACTS-MISSING",
                        "paths": ["src/**"],
                        "reason": "Integrity and contract checks must stay non-suppressible.",
                    }
                ],
            }
        ),
        encoding="utf-8",
    )
    with pytest.raises(AuditConfigError, match="implementation-lint DS rule"):
        load_audit_config(tmp_path, config_path=config)


def test_unified_audit_passes_with_tracked_exception_and_skips_missing_contracts(
    tmp_path: Path,
) -> None:
    (tmp_path / "src").mkdir()
    (tmp_path / "src" / "app.css").write_text(
        ".legacy { color: #ffffff; }\n",
        encoding="utf-8",
    )
    config_dir = tmp_path / ".design-ontology"
    config_dir.mkdir()
    (config_dir / "audit.json").write_text(
        json.dumps(
            {
                "schema_version": "design-ontology.audit-config/v1",
                "ignore_rules": [
                    {
                        "code": "DS001",
                        "paths": ["src/**"],
                        "reason": "Legacy CSS remains until the vendor migration lands.",
                    }
                ],
            }
        ),
        encoding="utf-8",
    )

    report = run_design_audit(
        tmp_path,
        include_divergence=False,
        require_contracts=False,
    )

    assert report.ok
    assert report.checks[0].status == "pass"
    assert report.checks[0].details["raw_issue_count"] == 1
    assert len(report.suppressed_issues) == 1
    assert report.to_dict()["summary"]["raw_issue_count"] == 1
    assert report.checks[1].status == "skipped"
    assert report.checks[2].status == "skipped"
    assert report.unused_ignore_rules == []


def test_unified_audit_fails_on_visible_issue_and_required_contract_gap(tmp_path: Path) -> None:
    (tmp_path / "app.css").write_text("body { color: #ffffff; }\n", encoding="utf-8")

    report = run_design_audit(
        tmp_path,
        include_divergence=False,
        require_contracts=True,
    )

    assert not report.ok
    assert report.checks[0].status == "fail"
    assert report.checks[2].status == "fail"
    assert report.checks[2].issues[0]["code"] == "AUDIT-CONTRACTS-MISSING"


def test_existing_contract_specs_require_emitted_tokens(tmp_path: Path) -> None:
    target = _write_clean_target(tmp_path)
    project = tmp_path / "project"
    specs = project / "build" / "system" / "components" / "component_specs.json"
    specs.parent.mkdir(parents=True)
    specs.write_text("{}", encoding="utf-8")

    report = run_design_audit(
        target,
        project_dir=project,
        include_divergence=False,
    )

    contract = next(check for check in report.checks if check.name == "component-contracts")
    assert contract.status == "fail"
    assert "tokens" in contract.issues[0]["message"]


def test_enabled_divergence_error_fails_closed_for_empty_target(tmp_path: Path) -> None:
    report = run_design_audit(tmp_path, include_contracts=False)

    assert not report.ok
    assert report.checks[0].issues[0]["code"] == "AUDIT-IMPLEMENTATION-EMPTY"
    assert report.checks[1].status == "fail"
    assert report.checks[1].issues[0]["code"] == "AUDIT-DIVERGENCE-ERROR"


def test_divergence_failure_is_normalized_into_ranked_punch_list(tmp_path: Path) -> None:
    target = _write_clean_target(tmp_path)
    registry = tmp_path / "registry.json"
    prior = replace(extract_style_fingerprint(target), project="prior-project")
    register_fingerprint(registry, prior)

    report = run_design_audit(
        target,
        registry_path=registry,
        include_contracts=False,
    )
    payload = report.to_dict()

    assert not report.ok
    divergence = next(check for check in report.checks if check.name == "style-divergence")
    assert divergence.status == "fail"
    assert divergence.issues
    assert {item["rule_id"] for item in payload["punch_list"]} & {
        "AUDIT-STYLE-ATTRACTOR",
        "AUDIT-STYLE-REPEAT",
    }
    assert payload["severity_counts"]["critical"] >= 1


def test_registration_waits_for_complete_audit_pass(tmp_path: Path) -> None:
    target = _write_clean_target(tmp_path)
    (target / "bad.css").write_text(".bad { color: #ffffff; }", encoding="utf-8")
    registry = tmp_path / "registry.json"

    report = run_design_audit(
        target,
        registry_path=registry,
        include_contracts=False,
        register_on_pass=True,
    )

    assert not report.ok
    assert report.registration["performed"] is False
    assert report.registration["reason"] == "overall audit did not pass"
    assert not registry.exists()


def test_registration_runs_after_complete_audit_pass(tmp_path: Path) -> None:
    target = _write_clean_target(tmp_path)
    registry = tmp_path / "registry.json"

    report = run_design_audit(
        target,
        project_id="stable-project",
        registry_path=registry,
        include_contracts=False,
        register_on_pass=True,
    )

    assert report.ok
    assert report.registration["performed"] is True
    assert registry.is_file()
    payload = json.loads(registry.read_text(encoding="utf-8"))
    assert payload["entries"][0]["project"] == "stable-project"


def test_audit_provenance_binds_inputs_and_declares_manual_coverage(tmp_path: Path) -> None:
    target = _write_clean_target(tmp_path)
    report = run_design_audit(
        target,
        registry_path=tmp_path / "registry.json",
        include_contracts=False,
    )
    payload = report.to_dict()

    snapshot = payload["provenance"]["target_snapshot"]
    assert snapshot["file_count"] == 3
    assert len(snapshot["sha256"]) == 64
    assert payload["provenance"]["implementation_input_snapshot"]["file_count"] == 3
    assert payload["provenance"]["style_source_snapshot"]["file_count"] == 3
    assert payload["provenance"]["ruleset_source_snapshot"]["file_count"] >= 5
    assert payload["provenance"]["tool"]["rulesets"]["implementation"].endswith("/v2")
    assert (
        payload["provenance"]["registry_before"]["compared_snapshot_sha256"]
        == payload["checks"][1]["details"]["registry_snapshot_sha256"]
    )
    assert payload["manual_review_coverage"]
    assert payload["scope"]["production_readiness"] is False
    assert payload["reference_studies"][0]["revision"].startswith("13ac0ec7")


def test_implementation_provenance_changes_with_artifact_font_inputs(tmp_path: Path) -> None:
    target = _write_clean_target(tmp_path)
    fonts = target / "design-system" / "fonts.css"
    fonts.write_text("/* font fetch pending */", encoding="utf-8")
    before = run_design_audit(
        target,
        include_divergence=False,
        include_contracts=False,
    ).to_dict()["provenance"]["implementation_input_snapshot"]["sha256"]

    fonts.write_text(
        '@font-face { font-family: "Example"; src: url("fonts/example.woff2"); }',
        encoding="utf-8",
    )
    after = run_design_audit(
        target,
        include_divergence=False,
        include_contracts=False,
    ).to_dict()["provenance"]["implementation_input_snapshot"]["sha256"]

    assert before != after


def test_implementation_provenance_includes_nested_artifact_inputs(tmp_path: Path) -> None:
    target = _write_clean_target(tmp_path)
    nested = target / "second-mockup"
    nested_artifact = nested / "design-system"
    nested_artifact.mkdir(parents=True)
    nested_tokens = nested_artifact / "tokens.css"
    nested_tokens.write_text(
        ":root { --ds-color-surface: #ffffff; --ds-color-ink: #111111; }",
        encoding="utf-8",
    )
    (nested / "index.html").write_text("<main class='nested'>Nested</main>", encoding="utf-8")
    (nested / "styles.css").write_text(
        ".nested { color: var(--ds-color-ink); }",
        encoding="utf-8",
    )

    before_payload = run_design_audit(
        target,
        include_divergence=False,
        include_contracts=False,
    ).to_dict()
    before_snapshot = before_payload["provenance"]["implementation_input_snapshot"]
    assert "second-mockup/design-system/tokens.css" in {
        item["path"] for item in before_snapshot["files"]
    }

    nested_tokens.write_text(
        ":root { --ds-color-surface: #ffffff; --ds-color-ink: #eeeeee; }",
        encoding="utf-8",
    )
    after_snapshot = run_design_audit(
        target,
        include_divergence=False,
        include_contracts=False,
    ).to_dict()["provenance"]["implementation_input_snapshot"]

    assert before_snapshot["sha256"] != after_snapshot["sha256"]


def test_audit_rejects_input_change_between_gate_read_and_provenance(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    target = _write_clean_target(tmp_path)
    original_extract = design_audit_module.extract_style_fingerprint

    def extract_then_mutate(*args, **kwargs):
        fingerprint = original_extract(*args, **kwargs)
        (target / "styles.css").write_text(
            "body { transition: all 100ms; }",
            encoding="utf-8",
        )
        return fingerprint

    monkeypatch.setattr(
        design_audit_module,
        "extract_style_fingerprint",
        extract_then_mutate,
    )

    with pytest.raises(ValueError, match="changed after it was read"):
        run_design_audit(
            target,
            registry_path=tmp_path / "registry.json",
            include_contracts=False,
        )


def test_audit_rejects_contradictory_gate_options(tmp_path: Path) -> None:
    with pytest.raises(ValueError, match="skip-contracts"):
        run_design_audit(
            tmp_path,
            include_divergence=False,
            include_contracts=False,
            require_contracts=True,
        )
    with pytest.raises(ValueError, match="skip-divergence"):
        run_design_audit(
            tmp_path,
            include_divergence=False,
            include_contracts=False,
            register_on_pass=True,
        )


def test_audit_rejects_non_ui_only_target(tmp_path: Path) -> None:
    (tmp_path / "vite.config.ts").write_text(
        "export default { server: { port: 3000 } };",
        encoding="utf-8",
    )

    report = run_design_audit(
        tmp_path,
        include_divergence=False,
        include_contracts=False,
    )

    assert not report.ok
    assert report.checks[0].issues[0]["code"] == "AUDIT-IMPLEMENTATION-EMPTY"


@pytest.mark.parametrize(
    ("name", "content"),
    [
        ("styles.css", "/* no implementation */"),
        ("App.tsx", "export {};"),
        ("index.html", "<!-- no implementation -->"),
    ],
)
def test_audit_rejects_non_substantive_runtime_file(
    tmp_path: Path,
    name: str,
    content: str,
) -> None:
    (tmp_path / name).write_text(content, encoding="utf-8")

    report = run_design_audit(
        tmp_path,
        include_divergence=False,
        include_contracts=False,
    )

    assert not report.ok
    assert report.checks[0].issues[0]["code"] == "AUDIT-IMPLEMENTATION-EMPTY"


def test_audit_fails_closed_on_unreadable_implementation_source(tmp_path: Path) -> None:
    (tmp_path / "bad.css").write_bytes(b"\xff\xfe\x00")

    report = run_design_audit(
        tmp_path,
        include_divergence=False,
        include_contracts=False,
    )

    assert not report.ok
    assert {issue["code"] for issue in report.checks[0].issues} == {
        "AUDIT-IMPLEMENTATION-EMPTY",
        "DS000",
    }


def test_audit_rejects_source_symlink_outside_target(tmp_path: Path) -> None:
    outside = tmp_path / "outside.css"
    outside.write_text(".external { color: var(--ds-color-ink); }", encoding="utf-8")
    target = tmp_path / "target"
    target.mkdir()
    (target / "link.css").symlink_to(outside)

    report = run_design_audit(
        target,
        include_divergence=False,
        include_contracts=False,
    )

    assert not report.ok
    assert {issue["code"] for issue in report.checks[0].issues} == {
        "AUDIT-IMPLEMENTATION-EMPTY",
        "DS000",
    }


def test_report_schema_is_distinct_and_punch_list_deduplicates() -> None:
    duplicate = _issue("DS001", "src/app.css").to_dict()
    report = DesignAuditReport(
        target_repo="/tmp/target",
        project_dir="/tmp/project",
        project_id="project",
        config_path=None,
        checks=[
            AuditCheck(
                name="implementation-lint",
                status="fail",
                issues=[duplicate, duplicate],
            )
        ],
    )

    payload = report.to_dict()
    assert payload["schema_version"] == "design-ontology.audit-report/v1"
    assert len(payload["punch_list"]) == 1
    assert payload["punch_list"][0]["severity_source"] == "default-major"
    assert payload["severity_counts"]["major"] == 1
    assert payload["summary"]["normalized_issue_count"] == 1
    assert payload["summary"]["raw_issue_count"] == 2


def test_cli_emits_machine_readable_unified_audit(tmp_path: Path) -> None:
    (tmp_path / "app.css").write_text("body { color: #ffffff; }\n", encoding="utf-8")
    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "design_ontology_harness.cli",
            "audit-implementation",
            "--target-repo",
            str(tmp_path),
            "--skip-divergence",
            "--skip-contracts",
            "--json",
        ],
        cwd=REPO_ROOT,
        text=True,
        capture_output=True,
        check=False,
    )

    assert result.returncode == 1
    payload = json.loads(result.stdout)
    assert payload["schema_version"] == "design-ontology.audit-report/v1"
    assert payload["checks"][0]["name"] == "implementation-lint"
    assert payload["checks"][0]["status"] == "fail"


def test_cli_emits_machine_readable_execution_error(tmp_path: Path) -> None:
    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "design_ontology_harness.cli",
            "audit-implementation",
            "--target-repo",
            str(tmp_path),
            "--config",
            str(tmp_path / "missing.json"),
            "--skip-divergence",
            "--skip-contracts",
            "--json",
        ],
        cwd=REPO_ROOT,
        text=True,
        capture_output=True,
        check=False,
    )

    assert result.returncode == 2
    payload = json.loads(result.stdout)
    assert payload["schema_version"] == "design-ontology.audit-error/v1"
    assert payload["ok"] is False
    assert payload["error"]["type"] == "AuditConfigError"
