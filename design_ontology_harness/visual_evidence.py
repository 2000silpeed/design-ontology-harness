from __future__ import annotations

import hashlib
import json
import re
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from PIL import Image, ImageChops


BROWSER_EVIDENCE_BUNDLE_SCHEMA = "production-browser-evidence-bundle/v1"
BROWSER_OBSERVATION_SCHEMA = "production-browser-observation/v1"
LEGACY_RUNTIME_CHECK_SCHEMA = "production-ui-runtime-check/v1"
DEFAULT_BROWSER_EVIDENCE_BUNDLE = Path(
    "build/system/production/browser-evidence-bundle.json"
)
REQUIRED_BROWSER_OBSERVATION_KINDS = {
    "screenshot",
    "dom",
    "state",
    "console",
    "interaction",
    "overflow",
    "accessibility",
    "component-runtime",
}
IAB_PRODUCER_KIND = "codex-desktop-in-app-browser"
IAB_TOOL = "in-app-browser"
IAB_SKILLS = {"browser:browser", "browser:control-in-app-browser"}
LOWER_SHA256_RE = re.compile(r"^[a-f0-9]{64}$")


@dataclass(frozen=True)
class VisualComparisonReport:
    before_path: str
    after_path: str
    before_sha256: str
    after_sha256: str
    before_size: tuple[int, int]
    after_size: tuple[int, int]
    min_change_ratio: float
    changed_pixels: int
    total_pixels: int
    change_ratio: float
    ok: bool
    reason: str

    def to_dict(self) -> dict:
        return asdict(self)


def compare_visuals(
    before_path: Path,
    after_path: Path,
    *,
    min_change_ratio: float = 0.001,
) -> VisualComparisonReport:
    before = before_path.resolve()
    after = after_path.resolve()
    before_sha = _sha256(before)
    after_sha = _sha256(after)

    with Image.open(before) as before_image_raw, Image.open(after) as after_image_raw:
        before_image = before_image_raw.convert("RGBA")
        after_image = after_image_raw.convert("RGBA")
        before_size = before_image.size
        after_size = after_image.size

        if before_sha == after_sha:
            total_pixels = before_size[0] * before_size[1]
            return VisualComparisonReport(
                before_path=str(before),
                after_path=str(after),
                before_sha256=before_sha,
                after_sha256=after_sha,
                before_size=before_size,
                after_size=after_size,
                min_change_ratio=min_change_ratio,
                changed_pixels=0,
                total_pixels=total_pixels,
                change_ratio=0.0,
                ok=False,
                reason="Screenshots are byte-identical; visual change is not evidenced.",
            )

        if before_size != after_size:
            before_pixels = before_size[0] * before_size[1]
            after_pixels = after_size[0] * after_size[1]
            return VisualComparisonReport(
                before_path=str(before),
                after_path=str(after),
                before_sha256=before_sha,
                after_sha256=after_sha,
                before_size=before_size,
                after_size=after_size,
                min_change_ratio=min_change_ratio,
                changed_pixels=0,
                total_pixels=max(before_pixels, after_pixels),
                change_ratio=0.0,
                ok=False,
                reason="Screenshot dimensions differ; the pair is not comparable evidence. Capture the same route, state, viewport, and framing.",
            )

        diff = ImageChops.difference(before_image, after_image)
        diff_pixels = diff.get_flattened_data() if hasattr(diff, "get_flattened_data") else diff.getdata()
        changed_pixels = sum(1 for pixel in diff_pixels if pixel != (0, 0, 0, 0))
        total_pixels = before_size[0] * before_size[1]
        change_ratio = changed_pixels / total_pixels if total_pixels else 0.0
        ok = change_ratio >= min_change_ratio
        reason = (
            f"Screenshots differ across {change_ratio:.3%} of pixels."
            if ok
            else f"Screenshots differ across only {change_ratio:.3%} of pixels; below the {min_change_ratio:.3%} evidence threshold."
        )

    return VisualComparisonReport(
        before_path=str(before),
        after_path=str(after),
        before_sha256=before_sha,
        after_sha256=after_sha,
        before_size=before_size,
        after_size=after_size,
        min_change_ratio=min_change_ratio,
        changed_pixels=changed_pixels,
        total_pixels=total_pixels,
        change_ratio=change_ratio,
        ok=ok,
        reason=reason,
    )


def format_visual_comparison(report: VisualComparisonReport) -> str:
    status = "OK" if report.ok else "FAIL"
    return "\n".join(
        [
            f"Visual comparison: {status}",
            f"- before: {report.before_path}",
            f"- after: {report.after_path}",
            f"- before_sha256: {report.before_sha256}",
            f"- after_sha256: {report.after_sha256}",
            f"- before_size: {report.before_size[0]}x{report.before_size[1]}",
            f"- after_size: {report.after_size[0]}x{report.after_size[1]}",
            f"- changed_pixels: {report.changed_pixels}/{report.total_pixels} ({report.change_ratio:.3%})",
            f"- min_change_ratio: {report.min_change_ratio:.3%}",
            f"- reason: {report.reason}",
        ]
    )


def format_visual_comparison_json(report: VisualComparisonReport) -> str:
    return json.dumps(report.to_dict(), ensure_ascii=False, indent=2)


def validate_browser_evidence_bundle(
    bundle_path: Path,
    *,
    project_dir: Path,
    target_repo: Path,
    implementation_tree: dict[str, Any],
    screenshot_manifest_path: Path,
    screenshot_report: dict[str, Any],
    component_runtime_manifest_path: Path,
    component_runtime_report: dict[str, Any],
) -> dict[str, Any]:
    """Validate one browser-produced evidence session against the frozen runtime.

    This function only validates files emitted by an agent-controlled browser
    session. It deliberately does not launch or impersonate Codex Desktop's
    privileged in-app Browser backend.
    """

    errors: list[str] = []
    project = project_dir.resolve()
    target = target_repo.resolve()
    bundle = bundle_path.resolve()
    tree_sha = str(implementation_tree.get("sha256") or "")
    latest_runtime_mtime_ns = int(
        implementation_tree.get("latest_runtime_mtime_ns") or 0
    )
    roots = {"project": project, "target-repo": target}

    if not bundle.is_file():
        return _browser_evidence_report(
            bundle_path=bundle,
            errors=[
                "browser evidence bundle not found; production QA must capture a "
                "fresh Codex Desktop in-app Browser session"
            ],
        )
    production_root = (project / "build/system/production").resolve()
    if not bundle.is_relative_to(production_root):
        errors.append(
            "browser evidence bundle must be registered under build/system/production"
        )
    try:
        payload = json.loads(bundle.read_text(encoding="utf-8"))
    except (OSError, UnicodeDecodeError, json.JSONDecodeError) as exc:
        return _browser_evidence_report(
            bundle_path=bundle,
            errors=[f"browser evidence bundle is not readable JSON: {exc}"],
        )
    if not isinstance(payload, dict):
        return _browser_evidence_report(
            bundle_path=bundle,
            errors=["browser evidence bundle JSON root must be an object"],
        )

    if payload.get("schema_version") != BROWSER_EVIDENCE_BUNDLE_SCHEMA:
        errors.append(
            f"schema_version must be {BROWSER_EVIDENCE_BUNDLE_SCHEMA}; "
            "legacy narrative runtime checks cannot support a production claim"
        )
    bundle_id = _required_string(payload.get("bundle_id"))
    if len(bundle_id) < 8:
        errors.append("bundle_id must be a stable non-trivial identifier")
    if payload.get("project") != project.name:
        errors.append(f"project must be {project.name}")

    declared_tree = payload.get("implementation_tree")
    if not isinstance(declared_tree, dict):
        errors.append("implementation_tree must be an object")
        declared_tree = {}
    for field in ("algorithm", "sha256", "file_count"):
        if declared_tree.get(field) != implementation_tree.get(field):
            errors.append(
                f"implementation_tree.{field} does not match the current runtime tree"
            )
    if not tree_sha:
        errors.append("current runtime tree has no sha256 digest")

    producer = payload.get("producer")
    if not isinstance(producer, dict):
        errors.append("producer must be an object")
        producer = {}
    if producer.get("kind") != IAB_PRODUCER_KIND:
        errors.append(f"producer.kind must be {IAB_PRODUCER_KIND}")
    if producer.get("tool") != IAB_TOOL:
        errors.append(f"producer.tool must be {IAB_TOOL}")
    if producer.get("skill") not in IAB_SKILLS:
        errors.append(
            "producer.skill must identify the Codex in-app Browser skill"
        )
    if len(_required_string(producer.get("tool_version"))) < 1:
        errors.append("producer.tool_version is required")
    agent_run_id = _required_string(producer.get("agent_run_id"))
    if len(agent_run_id) < 8:
        errors.append("producer.agent_run_id must identify the QA agent run")

    session = payload.get("browser_session")
    if not isinstance(session, dict):
        errors.append("browser_session must be an object")
        session = {}
    session_id = _required_string(session.get("session_id"))
    if not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9._:-]{7,127}", session_id):
        errors.append("browser_session.session_id must be an opaque 8..128 character id")
    target_url = _required_string(session.get("target_url"))
    if not target_url.startswith(("http://", "https://", "file://")):
        errors.append("browser_session.target_url must be an http(s) or file URL")
    if len(_required_string(session.get("user_agent"))) < 3:
        errors.append("browser_session.user_agent is required")
    started_at = _parse_timestamp(session.get("started_at"))
    ended_at = _parse_timestamp(session.get("ended_at"))
    if started_at is None:
        errors.append("browser_session.started_at must include an ISO-8601 timezone")
    if ended_at is None:
        errors.append("browser_session.ended_at must include an ISO-8601 timezone")
    if started_at is not None and ended_at is not None and ended_at < started_at:
        errors.append("browser_session.ended_at must not precede started_at")
    if started_at is not None and _timestamp_ns(started_at) < latest_runtime_mtime_ns:
        errors.append("browser session started before the latest runtime implementation")
    recorded_at = _parse_timestamp(payload.get("recorded_at"))
    if recorded_at is None:
        errors.append("recorded_at must include an ISO-8601 timezone")
    elif ended_at is not None and recorded_at < ended_at:
        errors.append("recorded_at must not precede browser_session.ended_at")
    if bundle.stat().st_mtime_ns < latest_runtime_mtime_ns:
        errors.append("browser evidence bundle file is older than the runtime implementation")

    screenshot_manifest = _resolve_bound_artifact(
        payload.get("screenshot_manifest"),
        roots=roots,
        expected_path=screenshot_manifest_path.resolve(),
        latest_runtime_mtime_ns=latest_runtime_mtime_ns,
        prefix="screenshot_manifest",
        errors=errors,
    )
    component_manifest = _resolve_bound_artifact(
        payload.get("component_runtime_manifest"),
        roots=roots,
        expected_path=component_runtime_manifest_path.resolve(),
        latest_runtime_mtime_ns=latest_runtime_mtime_ns,
        prefix="component_runtime_manifest",
        errors=errors,
    )
    for field in ("screenshot_manifest", "component_runtime_manifest"):
        reference = payload.get(field)
        if (
            isinstance(reference, dict)
            and reference.get("media_type") != "application/json"
        ):
            errors.append(f"{field}.media_type must be application/json")
    if not screenshot_report.get("ok"):
        errors.append("validated screenshot evidence is required before browser binding")
    if not component_runtime_report.get("ok"):
        errors.append("valid component-runtime conformance is required before browser binding")
    if component_runtime_report.get("production_eligible") is not True:
        errors.append("component-runtime evidence is not production eligible")

    expected_component_ids: set[str] = set()
    expected_component_evidence_sha: set[str] = set()
    if component_manifest is not None:
        expected_component_ids, expected_component_evidence_sha = (
            _component_runtime_binding(
                component_manifest,
                project=project,
                tree_sha=tree_sha,
                latest_runtime_mtime_ns=latest_runtime_mtime_ns,
                errors=errors,
            )
        )

    expected_screenshots = {
        str(record.get("sha256")): record
        for record in screenshot_report.get("screenshots", [])
        if isinstance(record, dict) and record.get("sha256")
    }
    expected_route_states = {
        (str(record.get("route") or ""), str(record.get("state") or ""))
        for record in screenshot_report.get("screenshots", [])
        if isinstance(record, dict)
    }
    expected_viewports = {
        (
            int((record.get("viewport") or {}).get("width") or 0),
            int((record.get("viewport") or {}).get("height") or 0),
        )
        for record in screenshot_report.get("screenshots", [])
        if isinstance(record, dict)
    }

    raw_observations = payload.get("observations")
    if not isinstance(raw_observations, list) or not raw_observations:
        errors.append("observations must be a non-empty list")
        raw_observations = []
    observations: dict[str, dict[str, Any]] = {}
    observations_by_kind: dict[str, list[str]] = {}
    screenshot_hashes: set[str] = set()
    for index, observation in enumerate(raw_observations):
        prefix = f"observations[{index}]"
        if not isinstance(observation, dict):
            errors.append(f"{prefix} must be an object")
            continue
        observation_id = _required_string(observation.get("observation_id"))
        kind = _required_string(observation.get("kind"))
        if len(observation_id) < 3:
            errors.append(f"{prefix}.observation_id is required")
            continue
        if observation_id in observations:
            errors.append(f"{prefix}.observation_id duplicates {observation_id}")
            continue
        if kind not in REQUIRED_BROWSER_OBSERVATION_KINDS:
            errors.append(f"{prefix}.kind is not a supported browser observation")
            continue
        if observation.get("browser_session_id") != session_id:
            errors.append(f"{prefix}.browser_session_id does not match the bundle session")
        if observation.get("producer_agent_run_id") != agent_run_id:
            errors.append(f"{prefix}.producer_agent_run_id does not match the producer")
        if observation.get("implementation_tree_sha256") != tree_sha:
            errors.append(f"{prefix}.implementation_tree_sha256 does not match the runtime")
        observed_at = _parse_timestamp(observation.get("observed_at"))
        if observed_at is None:
            errors.append(f"{prefix}.observed_at must include an ISO-8601 timezone")
        else:
            if started_at is not None and observed_at < started_at:
                errors.append(f"{prefix}.observed_at precedes the browser session")
            if ended_at is not None and observed_at > ended_at:
                errors.append(f"{prefix}.observed_at follows the browser session")
            if _timestamp_ns(observed_at) < latest_runtime_mtime_ns:
                errors.append(f"{prefix}.observed_at is older than the runtime implementation")
        artifact_path = _resolve_bound_artifact(
            observation.get("artifact"),
            roots=roots,
            expected_path=None,
            latest_runtime_mtime_ns=latest_runtime_mtime_ns,
            prefix=f"{prefix}.artifact",
            errors=errors,
        )
        observations[observation_id] = {
            "kind": kind,
            "record": observation,
            "artifact_path": artifact_path,
            "payload": None,
        }
        observations_by_kind.setdefault(kind, []).append(observation_id)
        if artifact_path is None:
            continue
        if kind == "screenshot":
            declared_media = _required_string(
                (observation.get("artifact") or {}).get("media_type")
            )
            if not declared_media.startswith("image/"):
                errors.append(f"{prefix}.artifact.media_type must be image/*")
            screenshot_sha = _required_string(
                (observation.get("artifact") or {}).get("sha256")
            )
            expected = expected_screenshots.get(screenshot_sha)
            if expected is None:
                errors.append(f"{prefix} does not match a validated screenshot SHA")
                continue
            if screenshot_sha in screenshot_hashes:
                errors.append(f"{prefix} duplicates a screenshot SHA observation")
            if artifact_path != Path(str(expected.get("path"))).resolve():
                errors.append(f"{prefix}.artifact.path does not match the screenshot manifest")
            for field in ("route", "state", "theme"):
                if observation.get(field) != expected.get(field):
                    errors.append(f"{prefix}.{field} does not match the screenshot manifest")
            if observation.get("viewport") != expected.get("viewport"):
                errors.append(f"{prefix}.viewport does not match the screenshot manifest")
            screenshot_hashes.add(screenshot_sha)
            continue

        declared_media = _required_string(
            (observation.get("artifact") or {}).get("media_type")
        )
        if declared_media != "application/json":
            errors.append(f"{prefix}.artifact.media_type must be application/json")
        raw_payload = _load_browser_observation(
            artifact_path,
            observation=observation,
            producer=producer,
            session_id=session_id,
            tree_sha=tree_sha,
            prefix=prefix,
            errors=errors,
        )
        observations[observation_id]["payload"] = raw_payload
        if raw_payload:
            _validate_browser_observation_data(
                raw_payload,
                kind=kind,
                expected_route_states=expected_route_states,
                expected_viewports=expected_viewports,
                prefix=prefix,
                errors=errors,
            )

    if screenshot_hashes != set(expected_screenshots):
        errors.append(
            "screenshot observations must cover every validated screenshot SHA exactly"
        )
    missing_kinds = REQUIRED_BROWSER_OBSERVATION_KINDS - set(observations_by_kind)
    if missing_kinds:
        errors.append(
            "browser evidence is missing observation kinds: "
            + ", ".join(sorted(missing_kinds))
        )
    for kind in sorted(REQUIRED_BROWSER_OBSERVATION_KINDS - {"screenshot"}):
        count = len(observations_by_kind.get(kind, []))
        if count != 1:
            errors.append(f"browser evidence requires exactly one aggregate {kind} observation")

    component_observation_ids = observations_by_kind.get("component-runtime", [])
    if len(component_observation_ids) == 1:
        component_payload = observations[component_observation_ids[0]].get("payload")
        if isinstance(component_payload, dict):
            data = component_payload.get("data")
            if not isinstance(data, dict):
                data = {}
            if _string_set(data.get("component_ids")) != expected_component_ids:
                errors.append(
                    "component-runtime observation component_ids do not match the manifest"
                )
            if _string_set(data.get("evidence_sha256")) != expected_component_evidence_sha:
                errors.append(
                    "component-runtime observation evidence_sha256 do not match the manifest"
                )
            for field, expected_kind in (
                ("dom_observation_ids", "dom"),
                ("state_observation_ids", "state"),
                ("interaction_observation_ids", "interaction"),
            ):
                linked = _string_set(data.get(field))
                if not linked:
                    errors.append(f"component-runtime observation {field} must not be empty")
                for linked_id in linked:
                    if observations.get(linked_id, {}).get("kind") != expected_kind:
                        errors.append(
                            f"component-runtime observation {field} contains an unknown "
                            f"{expected_kind} observation: {linked_id}"
                        )

    return _browser_evidence_report(
        bundle_path=bundle,
        errors=errors,
        bundle_id=bundle_id,
        producer_kind=_required_string(producer.get("kind")),
        browser_session_id=session_id,
        implementation_tree_sha256=tree_sha,
        observation_count=len(raw_observations),
        observation_kinds=sorted(observations_by_kind),
        screenshot_sha256=sorted(screenshot_hashes),
        component_ids=sorted(expected_component_ids),
        bound_screenshot_manifest=str(screenshot_manifest) if screenshot_manifest else None,
        bound_component_runtime_manifest=(
            str(component_manifest) if component_manifest else None
        ),
    )


def _browser_evidence_report(
    *,
    bundle_path: Path,
    errors: list[str],
    bundle_id: str = "",
    producer_kind: str = "",
    browser_session_id: str = "",
    implementation_tree_sha256: str = "",
    observation_count: int = 0,
    observation_kinds: list[str] | None = None,
    screenshot_sha256: list[str] | None = None,
    component_ids: list[str] | None = None,
    bound_screenshot_manifest: str | None = None,
    bound_component_runtime_manifest: str | None = None,
) -> dict[str, Any]:
    return {
        "schema_version": "production-browser-evidence-validation/v1",
        "ok": not errors,
        "errors": errors,
        "bundle_path": str(bundle_path),
        "bundle_id": bundle_id,
        "producer_kind": producer_kind,
        "browser_session_id": browser_session_id,
        "implementation_tree_sha256": implementation_tree_sha256,
        "observation_count": observation_count,
        "observation_kinds": observation_kinds or [],
        "screenshot_sha256": screenshot_sha256 or [],
        "component_ids": component_ids or [],
        "bound_screenshot_manifest": bound_screenshot_manifest,
        "bound_component_runtime_manifest": bound_component_runtime_manifest,
    }


def _resolve_bound_artifact(
    reference: Any,
    *,
    roots: dict[str, Path],
    expected_path: Path | None,
    latest_runtime_mtime_ns: int,
    prefix: str,
    errors: list[str],
) -> Path | None:
    if not isinstance(reference, dict):
        errors.append(f"{prefix} must be an artifact reference object")
        return None
    root_name = _required_string(reference.get("root"))
    root = roots.get(root_name)
    if root is None:
        errors.append(f"{prefix}.root must be project or target-repo")
        return None
    raw_path = _required_string(reference.get("path"))
    if not raw_path or Path(raw_path).is_absolute():
        errors.append(f"{prefix}.path must be a repository-relative path")
        return None
    resolved = (root / raw_path).resolve()
    if not resolved.is_relative_to(root):
        errors.append(f"{prefix}.path escapes its declared root")
        return None
    if expected_path is not None and resolved != expected_path:
        errors.append(f"{prefix}.path does not match the configured evidence path")
    if not resolved.is_file():
        errors.append(f"{prefix}.path does not exist: {raw_path}")
        return None
    declared_sha = _required_string(reference.get("sha256"))
    if not LOWER_SHA256_RE.fullmatch(declared_sha):
        errors.append(f"{prefix}.sha256 must be a lowercase SHA-256 digest")
    elif _sha256(resolved) != declared_sha:
        errors.append(f"{prefix}.sha256 does not match the artifact")
        return None
    if resolved.stat().st_mtime_ns < latest_runtime_mtime_ns:
        errors.append(f"{prefix}.path is older than the current runtime implementation")
    return resolved


def _component_runtime_binding(
    manifest_path: Path,
    *,
    project: Path,
    tree_sha: str,
    latest_runtime_mtime_ns: int,
    errors: list[str],
) -> tuple[set[str], set[str]]:
    try:
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    except (OSError, UnicodeDecodeError, json.JSONDecodeError):
        errors.append("component_runtime_manifest must be readable JSON")
        return set(), set()
    if not isinstance(manifest, dict):
        errors.append("component_runtime_manifest JSON root must be an object")
        return set(), set()
    if manifest.get("schema_version") != "component-runtime-manifest/v1":
        errors.append("component_runtime_manifest must use component-runtime-manifest/v1")
    if manifest.get("implementation_tree_sha256") != tree_sha:
        errors.append("component_runtime_manifest is not bound to the current runtime tree")
    component_ids: set[str] = set()
    evidence_sha: set[str] = set()
    components = manifest.get("components")
    if not isinstance(components, list) or not components:
        errors.append("component_runtime_manifest.components must be a non-empty list")
        return component_ids, evidence_sha
    for index, component in enumerate(components):
        prefix = f"component_runtime_manifest.components[{index}]"
        if not isinstance(component, dict):
            errors.append(f"{prefix} must be an object")
            continue
        component_id = _required_string(component.get("component_id"))
        if not component_id:
            errors.append(f"{prefix}.component_id is required")
        else:
            component_ids.add(component_id)
        evidence = component.get("evidence")
        if not isinstance(evidence, dict):
            errors.append(f"{prefix}.evidence must be an artifact reference")
            continue
        raw_path = _required_string(evidence.get("path"))
        declared_sha = _required_string(evidence.get("sha256"))
        path = (project / raw_path).resolve()
        if not raw_path or Path(raw_path).is_absolute() or not path.is_relative_to(project):
            errors.append(f"{prefix}.evidence.path must stay inside the project")
            continue
        if not path.is_file():
            errors.append(f"{prefix}.evidence.path does not exist: {raw_path}")
            continue
        if not LOWER_SHA256_RE.fullmatch(declared_sha):
            errors.append(f"{prefix}.evidence.sha256 must be a lowercase SHA-256 digest")
        elif _sha256(path) != declared_sha:
            errors.append(f"{prefix}.evidence.sha256 does not match the artifact")
            continue
        if path.stat().st_mtime_ns < latest_runtime_mtime_ns:
            errors.append(f"{prefix}.evidence.path is older than the runtime implementation")
        evidence_sha.add(declared_sha)
    return component_ids, evidence_sha


def _load_browser_observation(
    path: Path,
    *,
    observation: dict[str, Any],
    producer: dict[str, Any],
    session_id: str,
    tree_sha: str,
    prefix: str,
    errors: list[str],
) -> dict[str, Any]:
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeDecodeError, json.JSONDecodeError):
        errors.append(f"{prefix}.artifact must be readable JSON")
        return {}
    if not isinstance(payload, dict):
        errors.append(f"{prefix}.artifact JSON root must be an object")
        return {}
    schema_version = payload.get("schema_version")
    if schema_version == LEGACY_RUNTIME_CHECK_SCHEMA:
        errors.append(
            f"{prefix}.artifact uses {LEGACY_RUNTIME_CHECK_SCHEMA}; narrative "
            "passed=true JSON is legacy-unverified and fails closed for production"
        )
        return {}
    if schema_version != BROWSER_OBSERVATION_SCHEMA:
        errors.append(
            f"{prefix}.artifact schema_version must be {BROWSER_OBSERVATION_SCHEMA}"
        )
    for field in (
        "observation_id",
        "kind",
        "browser_session_id",
        "implementation_tree_sha256",
        "observed_at",
    ):
        if payload.get(field) != observation.get(field):
            errors.append(f"{prefix}.artifact {field} does not match the bundle record")
    if payload.get("browser_session_id") != session_id:
        errors.append(f"{prefix}.artifact browser_session_id does not match the session")
    if payload.get("implementation_tree_sha256") != tree_sha:
        errors.append(
            f"{prefix}.artifact implementation_tree_sha256 does not match the runtime"
        )
    raw_producer = payload.get("producer")
    if not isinstance(raw_producer, dict):
        errors.append(f"{prefix}.artifact producer must be an object")
    else:
        for field in ("kind", "tool", "skill", "tool_version", "agent_run_id"):
            if raw_producer.get(field) != producer.get(field):
                errors.append(f"{prefix}.artifact producer.{field} does not match")
    if not isinstance(payload.get("data"), dict):
        errors.append(f"{prefix}.artifact data must be an object")
    return payload


def _validate_browser_observation_data(
    payload: dict[str, Any],
    *,
    kind: str,
    expected_route_states: set[tuple[str, str]],
    expected_viewports: set[tuple[int, int]],
    prefix: str,
    errors: list[str],
) -> None:
    data = payload.get("data")
    if not isinstance(data, dict):
        return
    if kind in {"dom", "state", "console", "interaction", "accessibility"}:
        coverage = _route_state_coverage(data.get("route_state_coverage"))
        if coverage != expected_route_states:
            errors.append(
                f"{prefix}.artifact route_state_coverage does not match the screenshots"
            )
    if kind == "dom":
        snapshots = data.get("snapshots")
        if not isinstance(snapshots, list) or not snapshots:
            errors.append(f"{prefix}.artifact DOM snapshots must be a non-empty list")
        else:
            for index, snapshot in enumerate(snapshots):
                if not isinstance(snapshot, dict):
                    errors.append(f"{prefix}.artifact snapshots[{index}] must be an object")
                    continue
                if not _required_string(snapshot.get("selector")):
                    errors.append(f"{prefix}.artifact snapshots[{index}].selector is required")
                if not isinstance(snapshot.get("node_count"), int) or snapshot.get("node_count", 0) < 1:
                    errors.append(f"{prefix}.artifact snapshots[{index}].node_count must be positive")
                content = snapshot.get("content")
                declared_sha = _required_string(snapshot.get("snapshot_sha256"))
                if not isinstance(content, str) or not content.strip():
                    errors.append(
                        f"{prefix}.artifact snapshots[{index}].content must preserve the raw DOM snapshot"
                    )
                elif hashlib.sha256(content.encode("utf-8")).hexdigest() != declared_sha:
                    errors.append(
                        f"{prefix}.artifact snapshots[{index}].snapshot_sha256 does not match content"
                    )
    elif kind == "state":
        states = data.get("observations")
        if not isinstance(states, list) or not states:
            errors.append(f"{prefix}.artifact state observations must be non-empty")
        elif not all(
            isinstance(item, dict)
            and _required_string(item.get("state"))
            and _required_string(item.get("selector"))
            and item.get("visible") is True
            for item in states
        ):
            errors.append(
                f"{prefix}.artifact state observations must name visible selector states"
            )
    elif kind == "console":
        messages = data.get("messages")
        if not isinstance(messages, list):
            errors.append(f"{prefix}.artifact console messages must be a list")
            messages = []
        error_messages = [
            item
            for item in messages
            if isinstance(item, dict) and item.get("level") == "error"
        ]
        error_count = data.get("error_count")
        if not isinstance(error_count, int) or isinstance(error_count, bool):
            errors.append(f"{prefix}.artifact console error_count must be an integer")
        elif error_count != len(error_messages) or error_count != 0:
            errors.append(f"{prefix}.artifact console must contain zero browser errors")
    elif kind == "interaction":
        events = data.get("events")
        if not isinstance(events, list) or not events:
            errors.append(f"{prefix}.artifact interaction events must be non-empty")
        elif not all(
            isinstance(event, dict)
            and _required_string(event.get("action"))
            and _required_string(event.get("target"))
            and _required_string(event.get("before_state"))
            and _required_string(event.get("after_state"))
            and event.get("passed") is True
            for event in events
        ):
            errors.append(
                f"{prefix}.artifact interaction events need target, before/after state, and passed=true"
            )
    elif kind == "overflow":
        measurements = data.get("measurements")
        if not isinstance(measurements, list) or not measurements:
            errors.append(f"{prefix}.artifact overflow measurements must be non-empty")
            measurements = []
        coverage: set[tuple[int, int]] = set()
        for index, measurement in enumerate(measurements):
            if not isinstance(measurement, dict):
                errors.append(f"{prefix}.artifact measurements[{index}] must be an object")
                continue
            width = measurement.get("width")
            height = measurement.get("height")
            scroll_width = measurement.get("scroll_width")
            client_width = measurement.get("client_width")
            overflow = measurement.get("horizontal_overflow_px")
            if (
                not isinstance(width, int)
                or isinstance(width, bool)
                or not isinstance(height, int)
                or isinstance(height, bool)
            ):
                errors.append(f"{prefix}.artifact measurements[{index}] needs integer viewport dimensions")
                continue
            coverage.add((width, height))
            if (
                not _is_number(scroll_width)
                or not _is_number(client_width)
                or not _is_number(overflow)
            ):
                errors.append(f"{prefix}.artifact measurements[{index}] needs numeric widths")
            elif scroll_width > client_width or overflow > 0:
                errors.append(f"{prefix}.artifact measurements[{index}] reports horizontal overflow")
        if coverage != expected_viewports:
            errors.append(
                f"{prefix}.artifact overflow viewport coverage does not match the screenshots"
            )
    elif kind == "accessibility":
        if "wcag" not in _required_string(data.get("standard")).lower():
            errors.append(f"{prefix}.artifact accessibility standard must declare WCAG")
        violations = data.get("violations")
        if not isinstance(violations, list):
            errors.append(f"{prefix}.artifact accessibility violations must be a list")
        elif violations:
            errors.append(f"{prefix}.artifact accessibility violations must be empty")
        keyboard = data.get("keyboard_checks")
        if not isinstance(keyboard, list) or not keyboard:
            errors.append(f"{prefix}.artifact keyboard_checks must be non-empty")
        elif not all(
            isinstance(item, dict)
            and _required_string(item.get("action"))
            and _required_string(item.get("target"))
            and item.get("passed") is True
            for item in keyboard
        ):
            errors.append(
                f"{prefix}.artifact keyboard_checks need action, target, and passed=true"
            )
    elif kind == "component-runtime":
        for field in (
            "component_ids",
            "evidence_sha256",
            "dom_observation_ids",
            "state_observation_ids",
            "interaction_observation_ids",
        ):
            if not _string_set(data.get(field)):
                errors.append(f"{prefix}.artifact {field} must be a non-empty string list")


def _route_state_coverage(value: Any) -> set[tuple[str, str]]:
    if not isinstance(value, list):
        return set()
    return {
        (_required_string(item.get("route")), _required_string(item.get("state")))
        for item in value
        if isinstance(item, dict)
        and _required_string(item.get("route"))
        and _required_string(item.get("state"))
    }


def _string_set(value: Any) -> set[str]:
    if not isinstance(value, list):
        return set()
    return {
        item.strip()
        for item in value
        if isinstance(item, str) and item.strip()
    }


def _parse_timestamp(value: Any) -> datetime | None:
    if not isinstance(value, str) or not value.strip():
        return None
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        return None
    if parsed.tzinfo is None:
        return None
    return parsed.astimezone(timezone.utc)


def _timestamp_ns(value: datetime) -> int:
    return int(value.timestamp() * 1_000_000_000)


def _required_string(value: Any) -> str:
    return value.strip() if isinstance(value, str) else ""


def _is_number(value: Any) -> bool:
    return isinstance(value, int | float) and not isinstance(value, bool)


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()
