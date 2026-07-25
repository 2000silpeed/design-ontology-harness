from __future__ import annotations

import json
import tempfile
import unittest
from hashlib import sha256
from pathlib import Path

from design_ontology_harness.agent_packs import scaffold_agent_pack
from design_ontology_harness.agent_team import (
    ROLE_ORDER,
    TEAM_SCHEMA_VERSION,
    claude_specialist_agent,
    handoff_schema,
    team_contract,
    team_runbook,
    validate_agent_team,
    validate_handoff_payload,
)


def _digest(path: Path) -> str:
    return sha256(path.read_bytes()).hexdigest()


def _handoff_payload(
    *,
    run_id: str,
    created_at: str,
    artifact_path: str,
    output_digest: str,
    input_digest: str | None = None,
) -> dict[str, object]:
    return {
        "schema_version": "design-ontology-handoff/v1",
        "run_id": run_id,
        "created_at": created_at,
        "project": "sample",
        "from_role": "team-lead",
        "to_role": "ontology-compiler",
        "stage": "system",
        "status": "ready",
        "summary": "System artifact validation fixture.",
        "input_artifacts": [
            {"path": artifact_path, "sha256": input_digest or output_digest}
        ],
        "output_artifacts": [{"path": artifact_path, "sha256": output_digest}],
        "changed_paths": [artifact_path],
        "decisions": ["Keep historical handoff evidence immutable."],
        "gate_results": [
            {
                "command": "fixture gate",
                "status": "passed",
                "exit_code": 0,
                "evidence": "fixture passed",
            }
        ],
        "blockers": [],
        "risks": [],
        "next_action": "Validate the next stage.",
    }


def _write_handoff(root: Path, filename: str, payload: dict[str, object]) -> None:
    path = root / "design-system" / "handoffs" / filename
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


class AgentTeamTests(unittest.TestCase):
    def test_scaffold_creates_shared_contract_and_runtime_parity(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            result = scaffold_agent_pack(root, targets=["codex", "claude"])

            contract_path = root / "design-system" / "agent-team.json"
            contract = json.loads(contract_path.read_text(encoding="utf-8"))
            self.assertEqual(TEAM_SCHEMA_VERSION, contract["schema_version"])
            self.assertEqual(list(ROLE_ORDER), [role["id"] for role in contract["roles"]])
            self.assertIn(str(contract_path), result["created"])
            marketplace = json.loads(
                (root / ".agents" / "plugins" / "marketplace.json").read_text(encoding="utf-8")
            )
            self.assertEqual("local-plugins", marketplace["name"])

            codex_skill = root / "plugins" / "design-system-harness" / "skills" / "design-ontology-team-orchestrator" / "SKILL.md"
            claude_skill = root / ".claude" / "skills" / "design-ontology-team-orchestrator" / "SKILL.md"
            self.assertTrue(codex_skill.is_file())
            self.assertTrue(claude_skill.is_file())
            self.assertEqual(codex_skill.read_text(encoding="utf-8"), claude_skill.read_text(encoding="utf-8"))

            for role in ROLE_ORDER[1:]:
                self.assertTrue((root / ".claude" / "agents" / f"design-{role}.md").is_file())
                self.assertTrue(
                    (
                        root
                        / "plugins"
                        / "design-system-harness"
                        / "skills"
                        / f"design-{role}"
                        / "SKILL.md"
                    ).is_file()
                )
                self.assertTrue(
                    (
                        root
                        / "plugins"
                        / "design-system-harness"
                        / "skills"
                        / f"design-{role}"
                        / "agents"
                        / "openai.yaml"
                    ).is_file()
                )

            production_qa_skill = (
                root
                / "plugins"
                / "design-system-harness"
                / "skills"
                / "design-production-qa"
                / "SKILL.md"
            ).read_text(encoding="utf-8")
            self.assertIn("browser:browser", production_qa_skill)
            self.assertIn("production-browser-evidence-bundle/v1", production_qa_skill)
            self.assertIn("production-browser-observation/v1", production_qa_skill)
            self.assertIn("legacy-unverified", production_qa_skill)
            self.assertIn("does not launch, control, or attest", production_qa_skill)

            self.assertTrue(
                (root / ".claude" / "skills" / "design-system-visual-assets" / "SKILL.md").is_file()
            )
            for skill_name in ("design-system-refactor", "design-system-rebuild"):
                self.assertTrue(
                    (
                        root
                        / "plugins"
                        / "design-system-harness"
                        / "skills"
                        / skill_name
                        / "SKILL.md"
                    ).is_file()
                )

            report = validate_agent_team(root)
            self.assertTrue(report["ok"], report["errors"])
            self.assertEqual(len(ROLE_ORDER), report["role_count"])

    def test_validate_reports_missing_runtime_adapter(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            scaffold_agent_pack(root, targets=["codex", "claude"])
            (root / ".claude" / "agents" / "design-production-qa.md").unlink()

            report = validate_agent_team(root)

            self.assertFalse(report["ok"])
            self.assertIn("missing: .claude/agents/design-production-qa.md", report["errors"])

    def test_validate_reports_missing_detailed_workflow_skill(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            scaffold_agent_pack(root, targets=["claude"])
            (root / ".claude" / "skills" / "design-system-visual-assets" / "SKILL.md").unlink()

            report = validate_agent_team(root, targets=["claude"])

            self.assertFalse(report["ok"])
            self.assertIn(
                "missing: .claude/skills/design-system-visual-assets/SKILL.md",
                report["errors"],
            )

    def test_codex_only_and_claude_only_packs_validate_independently(self) -> None:
        for target in ("codex", "claude"):
            with self.subTest(target=target), tempfile.TemporaryDirectory() as tmp:
                root = Path(tmp)
                scaffold_agent_pack(root, targets=[target])
                report = validate_agent_team(root, targets=[target])
                self.assertTrue(report["ok"], report["errors"])

    def test_repository_readme_explains_every_core_agent(self) -> None:
        readme = (Path(__file__).parents[1] / "README.md").read_text(encoding="utf-8")
        for role in team_contract()["roles"]:
            self.assertIn(role["title"], readme)

    def test_handoff_schema_requires_reproducible_evidence(self) -> None:
        required = set(handoff_schema()["required"])
        self.assertTrue(
            {"run_id", "created_at", "input_artifacts", "output_artifacts", "changed_paths", "gate_results"}
            <= required
        )
        gate_required = set(handoff_schema()["properties"]["gate_results"]["items"]["required"])
        self.assertEqual({"command", "status", "exit_code", "evidence"}, gate_required)
        artifact_required = set(handoff_schema()["$defs"]["artifact"]["required"])
        self.assertEqual({"path", "sha256"}, artifact_required)
        self.assertEqual(1, handoff_schema()["properties"]["input_artifacts"]["minItems"])
        self.assertEqual(1, handoff_schema()["properties"]["output_artifacts"]["minItems"])
        self.assertEqual(1, handoff_schema()["properties"]["gate_results"]["minItems"])

    def test_handoff_validator_accepts_evidence_and_rejects_bad_hash(self) -> None:
        payload = {
            "schema_version": "design-ontology-handoff/v1",
            "run_id": "team-test-001",
            "created_at": "2026-07-13T12:00:00+09:00",
            "project": "sample",
            "from_role": "brief-author",
            "to_role": "token-curator",
            "stage": "tokens-and-components",
            "status": "ready",
            "summary": "Concept inputs are ready for token authoring.",
            "input_artifacts": [{"path": "spec.md", "sha256": "a" * 64}],
            "output_artifacts": [{"path": "brand_profile.json", "sha256": "b" * 64}],
            "changed_paths": ["brand_profile.json"],
            "decisions": ["Use an external component contract file."],
            "gate_results": [
                {
                    "command": "uv run design-ontology validate-agent-team ...",
                    "status": "passed",
                    "exit_code": 0,
                    "evidence": "validator output",
                }
            ],
            "blockers": [],
            "risks": [],
            "next_action": "Resolve Semantic OS color roles.",
        }

        self.assertEqual([], validate_handoff_payload(payload))
        payload["input_artifacts"][0]["sha256"] = "BAD"
        self.assertIn(
            "input_artifacts[0].sha256 must be a lowercase SHA-256 digest",
            validate_handoff_payload(payload),
        )

    def test_handoff_validator_rejects_empty_evidence_and_invalid_stage_transition(self) -> None:
        payload = {
            "schema_version": "design-ontology-handoff/v1",
            "run_id": "team-test-002",
            "created_at": "2026-07-13T12:00:00+09:00",
            "project": "sample",
            "from_role": "release-governor",
            "to_role": "brief-author",
            "stage": "qa",
            "status": "ready",
            "summary": "Invalid transition fixture.",
            "input_artifacts": [],
            "output_artifacts": [],
            "changed_paths": [],
            "decisions": [],
            "gate_results": [],
            "blockers": [],
            "risks": [],
            "next_action": "This must not validate.",
        }

        errors = validate_handoff_payload(payload)

        self.assertIn(
            "roles release-governor -> brief-author are not an allowed transition for stage qa",
            errors,
        )
        self.assertIn("input_artifacts must contain at least one hashed artifact", errors)
        self.assertIn("output_artifacts must contain at least one hashed artifact", errors)
        self.assertIn("gate_results must contain at least one reproducible gate result", errors)

    def test_directory_validation_allows_same_run_handoff_to_supersede_stale_digest(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            scaffold_agent_pack(root, targets=["codex", "claude"])
            artifact = root / "system-artifact.json"
            artifact.write_text('{"version": 1}\n', encoding="utf-8")
            _write_handoff(
                root,
                "01-system.json",
                _handoff_payload(
                    run_id="same-run",
                    created_at="2026-07-13T12:00:00+09:00",
                    artifact_path="system-artifact.json",
                    output_digest=_digest(artifact),
                ),
            )

            artifact.write_text('{"version": 2}\n', encoding="utf-8")
            _write_handoff(
                root,
                "02-system.json",
                _handoff_payload(
                    run_id="same-run",
                    created_at="2026-07-13T12:01:00+09:00",
                    artifact_path="system-artifact.json",
                    output_digest=_digest(artifact),
                ),
            )

            report = validate_agent_team(root)

            self.assertTrue(report["ok"], report["errors"])

    def test_directory_validation_allows_later_run_to_supersede_stale_digest(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            scaffold_agent_pack(root, targets=["codex", "claude"])
            artifact = root / "system-artifact.json"
            artifact.write_text('{"run": 1}\n', encoding="utf-8")
            _write_handoff(
                root,
                "run-one.json",
                _handoff_payload(
                    run_id="run-one",
                    created_at="2026-07-13T12:00:00+09:00",
                    artifact_path="system-artifact.json",
                    output_digest=_digest(artifact),
                ),
            )

            artifact.write_text('{"run": 2}\n', encoding="utf-8")
            _write_handoff(
                root,
                "run-two.json",
                _handoff_payload(
                    run_id="run-two",
                    created_at="2026-07-13T12:01:00+09:00",
                    artifact_path="system-artifact.json",
                    output_digest=_digest(artifact),
                ),
            )

            report = validate_agent_team(root)

            self.assertTrue(report["ok"], report["errors"])

    def test_directory_validation_checks_latest_record_independently_per_artifact(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            scaffold_agent_pack(root, targets=["codex", "claude"])
            first = root / "first-artifact.json"
            second = root / "second-artifact.json"
            first.write_text('{"version": 1}\n', encoding="utf-8")
            second.write_text('{"version": 1}\n', encoding="utf-8")
            _write_handoff(
                root,
                "01-first.json",
                _handoff_payload(
                    run_id="run-one",
                    created_at="2026-07-13T12:00:00+09:00",
                    artifact_path="first-artifact.json",
                    output_digest=_digest(first),
                ),
            )
            _write_handoff(
                root,
                "02-second.json",
                _handoff_payload(
                    run_id="run-two",
                    created_at="2026-07-13T12:01:00+09:00",
                    artifact_path="second-artifact.json",
                    output_digest=_digest(second),
                ),
            )
            first.write_text('{"version": 2}\n', encoding="utf-8")

            report = validate_agent_team(root)

            self.assertFalse(report["ok"])
            self.assertTrue(
                any(
                    "sha256 does not match current file: first-artifact.json" in error
                    for error in report["errors"]
                ),
                report["errors"],
            )
            self.assertFalse(
                any("second-artifact.json" in error for error in report["errors"]),
                report["errors"],
            )

    def test_directory_validation_breaks_timestamp_ties_by_path_then_artifact_order(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            scaffold_agent_pack(root, targets=["codex", "claude"])
            artifact = root / "system-artifact.json"
            artifact.write_text('{"version": 1}\n', encoding="utf-8")
            stale_digest = _digest(artifact)
            _write_handoff(
                root,
                "a-handoff.json",
                _handoff_payload(
                    run_id="run-one",
                    created_at="2026-07-13T12:00:00+09:00",
                    artifact_path="system-artifact.json",
                    output_digest=stale_digest,
                ),
            )

            artifact.write_text('{"version": 2}\n', encoding="utf-8")
            _write_handoff(
                root,
                "z-handoff.json",
                _handoff_payload(
                    run_id="run-two",
                    created_at="2026-07-13T12:00:00+09:00",
                    artifact_path="system-artifact.json",
                    input_digest=stale_digest,
                    output_digest=_digest(artifact),
                ),
            )

            report = validate_agent_team(root)

            self.assertTrue(report["ok"], report["errors"])

    def test_direct_handoff_validation_keeps_stale_digest_check_strict(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            artifact = root / "system-artifact.json"
            artifact.write_text('{"version": 1}\n', encoding="utf-8")
            payload = _handoff_payload(
                run_id="direct-check",
                created_at="2026-07-13T12:00:00+09:00",
                artifact_path="system-artifact.json",
                output_digest=_digest(artifact),
            )
            artifact.write_text('{"version": 2}\n', encoding="utf-8")

            errors = validate_handoff_payload(payload, target_repo=root)

            self.assertIn(
                "input_artifacts[0].sha256 does not match current file: system-artifact.json",
                errors,
            )
            self.assertIn(
                "output_artifacts[0].sha256 does not match current file: system-artifact.json",
                errors,
            )

    def test_parallel_authors_use_separate_files_and_concept_gate_precedes_contracts(self) -> None:
        contract = team_contract()
        roles = {role["id"]: role for role in contract["roles"]}
        token_writes = " ".join(roles["token-curator"]["writes"])
        component_writes = " ".join(roles["component-author"]["writes"])
        concept_stage = next(stage for stage in contract["stages"] if stage["id"] == "concept")

        self.assertIn("brand_profile.json", token_writes)
        self.assertNotIn("brand_profile.json", component_writes)
        self.assertIn("component-contracts.json", component_writes)
        self.assertNotIn("fully authored", concept_stage["exit_gate"])
        self.assertNotIn(
            "validate-component-contracts",
            " ".join(roles["component-author"].get("required_commands", [])),
        )
        self.assertIn(
            "validate-component-contracts",
            " ".join(roles["ontology-compiler"].get("required_commands", [])),
        )

    def test_commands_follow_stage_order_and_asset_integration_boundary(self) -> None:
        roles = {role["id"]: role for role in team_contract()["roles"]}
        token_commands = " ".join(roles["token-curator"].get("required_commands", []))
        compiler_commands = " ".join(roles["ontology-compiler"].get("required_commands", []))
        visual_commands = " ".join(roles["visual-asset-producer"].get("required_commands", []))
        implementer_commands = " ".join(roles["ui-implementer"].get("required_commands", []))

        self.assertNotIn("emit-tokens", token_commands)
        self.assertIn("emit-tokens", compiler_commands)
        self.assertNotIn("--require-integrated", visual_commands)
        self.assertIn("--require-integrated", implementer_commands)
        self.assertIn("--project-dir <implementation-repo>", implementer_commands)

    def test_codex_shell_prompt_preserves_skill_name(self) -> None:
        root = Path(__file__).parents[1]
        readme = (root / "README.md").read_text(encoding="utf-8")

        for text in (readme, team_runbook()):
            self.assertIn("codex 'Use $design-ontology-team-orchestrator", text)
            self.assertNotIn('codex "Use $design-ontology-team-orchestrator', text)

    def test_claude_auditors_and_release_can_write_evidence_but_not_edit_product_code(self) -> None:
        for role in ("reference-fidelity-auditor", "production-qa", "release-governor"):
            agent = claude_specialist_agent(role)
            tools_line = next(line for line in agent.splitlines() if line.startswith("tools:"))
            self.assertIn("Write", tools_line)
            self.assertNotIn("Edit", tools_line)

    def test_fidelity_stage_blocks_direct_implementation_to_qa_bypass(self) -> None:
        base = {
            "schema_version": "design-ontology-handoff/v1",
            "run_id": "fidelity-transition-test",
            "created_at": "2026-07-14T12:00:00+09:00",
            "project": "sample",
            "status": "ready",
            "summary": "Transition evidence.",
            "input_artifacts": [{"path": "input.json", "sha256": "a" * 64}],
            "output_artifacts": [{"path": "output.json", "sha256": "b" * 64}],
            "changed_paths": ["output.json"],
            "decisions": ["Keep the paired review independent."],
            "gate_results": [{
                "command": "reference-fidelity-loop",
                "status": "passed",
                "exit_code": 0,
                "evidence": "paired review passed",
            }],
            "blockers": [],
            "risks": [],
            "next_action": "Continue to the next owner.",
        }

        to_fidelity = dict(
            base,
            from_role="ui-implementer",
            to_role="reference-fidelity-auditor",
            stage="fidelity",
        )
        to_qa = dict(
            base,
            from_role="reference-fidelity-auditor",
            to_role="production-qa",
            stage="qa",
        )
        bypass = dict(
            base,
            from_role="ui-implementer",
            to_role="production-qa",
            stage="qa",
        )

        self.assertEqual([], validate_handoff_payload(to_fidelity))
        self.assertEqual([], validate_handoff_payload(to_qa))
        self.assertTrue(any("not an allowed transition" in error for error in validate_handoff_payload(bypass)))

    def test_readme_documents_semantic_markdown_and_cross_runtime_imagegen_handoff(self) -> None:
        readme = (Path(__file__).parents[1] / "README.md").read_text(encoding="utf-8")
        self.assertIn("docs/color-reference.md", readme)
        self.assertIn("Codex의 `image_gen`", readme)
        self.assertIn("SHA-256", readme)


if __name__ == "__main__":
    unittest.main()
