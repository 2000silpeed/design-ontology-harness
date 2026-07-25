from __future__ import annotations

import hashlib
import json
import os
import subprocess
from datetime import datetime, timedelta, timezone
from pathlib import Path

import pytest
from PIL import Image, ImageDraw

from design_ontology_harness.aesthetic_loop import (
    DEFAULT_METRICS,
    build_aesthetic_ontology,
    run_self_improvement_loop,
)
from design_ontology_harness.component_runtime import (
    COMPONENT_RUNTIME_EVIDENCE_SCHEMA,
    COMPONENT_RUNTIME_MANIFEST_SCHEMA,
    DEFAULT_COMPONENT_RUNTIME_MANIFEST,
)
from design_ontology_harness.production_verifier import (
    _runtime_implementation_tree,
    _validate_aesthetic_report,
    record_screenshot_evidence,
    validate_screenshot_manifest,
    verify_production_ui,
)
from design_ontology_harness.visual_evidence import (
    BROWSER_EVIDENCE_BUNDLE_SCHEMA,
    BROWSER_OBSERVATION_SCHEMA,
    DEFAULT_BROWSER_EVIDENCE_BUNDLE,
    IAB_PRODUCER_KIND,
    IAB_TOOL,
)


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _write_json(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")


def _make_screenshots(project: Path) -> list[Path]:
    project.mkdir(parents=True, exist_ok=True)
    runtime_entry = project / "index.html"
    if not runtime_entry.exists():
        runtime_entry.write_text("<main>Evidence review</main>", encoding="utf-8")
    paths: list[Path] = []
    for theme in ("light", "dark"):
        palette = (
            {
                "canvas": "#E9EEF5",
                "surface": "#FFFFFF",
                "ink": "#172033",
                "muted": "#65738B",
                "line": "#C5CFDC",
                "accent": "#2457A7",
            }
            if theme == "light"
            else {
                "canvas": "#101622",
                "surface": "#1B2535",
                "ink": "#F4F7FB",
                "muted": "#A5B1C4",
                "line": "#344258",
                "accent": "#79A8F2",
            }
        )
        for label, size in (("mobile", (390, 844)), ("desktop", (1280, 800))):
            image = Image.new("RGB", size, palette["canvas"])
            draw = ImageDraw.Draw(image)
            width, height = size
            draw.rectangle((0, 0, width, 66), fill=palette["surface"])
            draw.rectangle((22, 20, 46, 44), fill=palette["accent"])
            draw.text((58, 24), "FIELDNOTE / REVIEW DESK", fill=palette["ink"])
            draw.line((0, 65, width, 65), fill=palette["line"], width=2)
            left = 24
            if label == "desktop":
                draw.rectangle((0, 66, 218, height), fill=palette["surface"])
                for index, item in enumerate(("Evidence", "Decisions", "Sources", "History")):
                    y = 104 + index * 48
                    draw.text((28, y), item, fill=palette["ink"] if index == 0 else palette["muted"])
                left = 248
            content_width = width - left - 24
            draw.text((left, 94), "Evidence review", fill=palette["ink"])
            draw.text((left, 120), "3 sources linked / decision pending", fill=palette["muted"])
            card_height = 136 if label == "desktop" else 150
            for index in range(3):
                top = 158 + index * (card_height + 18)
                right = left + content_width
                draw.rounded_rectangle(
                    (left, top, right, top + card_height),
                    radius=12,
                    fill=palette["surface"],
                    outline=palette["line"],
                    width=2,
                )
                draw.rectangle((left + 18, top + 20, left + 58, top + 60), fill=palette["accent"])
                draw.text((left + 74, top + 20), f"Source {index + 1} / verified", fill=palette["ink"])
                draw.line((left + 74, top + 47, right - 24, top + 47), fill=palette["line"], width=3)
                draw.line((left + 22, top + 82, right - 68, top + 82), fill=palette["muted"], width=2)
                draw.line((left + 22, top + 103, right - 118, top + 103), fill=palette["line"], width=2)
            button_top = min(height - 70, 158 + 3 * (card_height + 18))
            draw.rounded_rectangle(
                (left, button_top, min(width - 24, left + 184), button_top + 44),
                radius=8,
                fill=palette["accent"],
            )
            draw.text((left + 18, button_top + 14), "Record decision", fill=palette["surface"])
            path = project / "screenshots" / f"{theme}-{label}.png"
            path.parent.mkdir(parents=True, exist_ok=True)
            image.save(path)
            paths.append(path)
    return paths


def _ensure_git_head(project: Path) -> str:
    project.mkdir(parents=True, exist_ok=True)
    subprocess.run(["git", "init", "-q", str(project)], check=True)
    subprocess.run(["git", "-C", str(project), "add", "."], check=True)
    subprocess.run(
        [
            "git",
            "-C",
            str(project),
            "-c",
            "user.name=Production Gate Test",
            "-c",
            "user.email=production-gate@example.test",
            "commit",
            "-qm",
            "fixture implementation",
        ],
        check=True,
    )
    return subprocess.run(
        ["git", "-C", str(project), "rev-parse", "HEAD"],
        check=True,
        text=True,
        capture_output=True,
    ).stdout.strip()


def _record_all(project: Path, screenshots: list[Path]) -> Path:
    implementation_sha = _ensure_git_head(project)
    manifest = project / "build" / "system" / "production" / "screenshots.json"
    for path in screenshots:
        theme = "light" if "light-" in path.name else "dark"
        record_screenshot_evidence(
            manifest_path=manifest,
            project=project.name,
            target_repo=project,
            screenshot_path=path,
            route="/review",
            state="evidence-selected",
            theme=theme,
            implementation_sha=implementation_sha,
        )
    return manifest


def _artifact_reference(project: Path, relative_path: str, payload: dict) -> dict[str, str]:
    path = project / relative_path
    _write_json(path, payload)
    return {"path": relative_path, "sha256": _sha256(path)}


def _runtime_checks(project: Path, screenshots: list[Path], *, suffix: str) -> list[dict]:
    viewports = sorted({Image.open(path).size for path in screenshots})
    implementation_tree = _runtime_implementation_tree(project)
    checked_at = datetime.now(timezone.utc).isoformat(timespec="microseconds")
    interaction_run = f"interaction-{suffix}"
    overflow_run = f"overflow-{suffix}"
    accessibility_run = f"accessibility-{suffix}"
    interaction_artifact = _artifact_reference(
        project,
        f"build/system/production/evidence/{interaction_run}.json",
        {
            "schema_version": "production-ui-runtime-check/v1",
            "kind": "interaction",
            "run_id": interaction_run,
            "implementation_tree_sha256": implementation_tree["sha256"],
            "checked_at": checked_at,
            "route_state_coverage": [{"route": "/review", "state": "evidence-selected"}],
            "assertions": [
                {"name": "evidence card selection updates the selected state", "passed": True},
                {"name": "record decision retains keyboard focus", "passed": True},
            ],
        },
    )
    overflow_artifact = _artifact_reference(
        project,
        f"build/system/production/evidence/{overflow_run}.json",
        {
            "schema_version": "production-ui-runtime-check/v1",
            "kind": "overflow",
            "run_id": overflow_run,
            "implementation_tree_sha256": implementation_tree["sha256"],
            "checked_at": checked_at,
            "viewport_coverage": [
                {"width": width, "height": height}
                for width, height in viewports
            ],
            "max_horizontal_overflow_px": 0,
            "assertions": [
                {"name": f"scrollWidth equals clientWidth at {width}x{height}", "passed": True}
                for width, height in viewports
            ],
        },
    )
    accessibility_artifact = _artifact_reference(
        project,
        f"build/system/production/evidence/{accessibility_run}.json",
        {
            "schema_version": "production-ui-runtime-check/v1",
            "kind": "accessibility",
            "run_id": accessibility_run,
            "implementation_tree_sha256": implementation_tree["sha256"],
            "checked_at": checked_at,
            "standard": "WCAG 2.2 AA",
            "automated_violations": 0,
            "assertions": [
                {"name": "axe-core serious and critical violations", "passed": True},
                {"name": "form and landmark names are exposed", "passed": True},
            ],
            "keyboard_assertions": [
                {"name": "tab order reaches evidence cards and decision action", "passed": True}
            ],
        },
    )
    return [
        {
            "kind": "interaction",
            "run_id": interaction_run,
            "status": "passed",
            "method": "Playwright pointer and keyboard state walkthrough",
            "artifact": interaction_artifact,
        },
        {
            "kind": "overflow",
            "run_id": overflow_run,
            "status": "passed",
            "method": "Browser scrollWidth and clientWidth assertions",
            "artifact": overflow_artifact,
        },
        {
            "kind": "accessibility",
            "run_id": accessibility_run,
            "status": "passed",
            "method": "axe-core scan plus manual keyboard assertions",
            "artifact": accessibility_artifact,
        },
    ]


def _aesthetic_report(project: Path, screenshots: list[Path], *, source: str) -> dict:
    ontology = build_aesthetic_ontology({"brand_name": "Fieldnote"})
    scores = {
        metric_id: round(8.4 + (index % 5) * 0.12, 2)
        for index, metric_id in enumerate(DEFAULT_METRICS)
    }
    screenshot_hashes = sorted(_sha256(path) for path in screenshots)
    suffix = source.replace("-", "_")
    run_id = f"review-{suffix}-20260712"
    review_artifact = _artifact_reference(
        project,
        f"build/system/production/evidence/{run_id}.json",
        {
            "schema_version": "production-ui-review-artifact/v1",
            "run_id": run_id,
            "screenshot_sha256": screenshot_hashes,
            "metric_findings": {
                metric_id: {
                    "score": score,
                    "note": (
                        f"{metric_id} was checked against all route, theme, and viewport renders; "
                        f"the recorded score is {score:.2f}."
                    ),
                }
                for metric_id, score in scores.items()
            },
        },
    )
    review_run = {
        "run_id": run_id,
        "source": source,
        "reviewer": "codex-visual-qa" if source == "multimodal-review" else "screenshot-heuristic-v1",
        "method": (
            "Structured side-by-side multimodal review of every route/theme/viewport render"
            if source == "multimodal-review"
            else "Deterministic screenshot feature analysis across the complete render matrix"
        ),
        "reviewed_at": "2026-07-12T12:00:00+09:00",
        "screenshot_sha256": screenshot_hashes,
        "artifact": review_artifact,
    }
    if source == "multimodal-review":
        review_run["model"] = "gpt-5-codex"
    evidence = {
        metric_id: [{
            "source": source,
            "reviewer": review_run["reviewer"],
            "method": review_run["method"],
            "artifact": review_artifact["path"],
        }]
        for metric_id in DEFAULT_METRICS
    }
    return run_self_improvement_loop(
        {
            "design_id": "fieldnote-review",
            "score_scale": 10,
            "source_screenshots": [str(path) for path in screenshots],
            "measurement_protocol": {
                "production_review": {
                    "schema_version": "production-ui-review/v1",
                    "review_runs": [review_run],
                    "runtime_checks": _runtime_checks(project, screenshots, suffix=suffix),
                }
            },
            "metrics": scores,
            "metric_evidence": evidence,
        },
        ontology,
        threshold=0.82,
    )


def _write_component_contract(project: Path) -> None:
    components = project / "build" / "system" / "components"
    components.mkdir(parents=True, exist_ok=True)
    payload = {
        "brand": "Fieldnote",
        "total_components": 1,
        "specs": [{
            "name": "evidence-review",
            "family": "content",
            "contract_version": "component-contract/v1",
            "contract_status": "complete",
            "contract_provenance": "spec-detected",
            "anatomy": {
                "parts": ["root", "evidence-list", "source-record", "decision-action"],
                "states": ["evidence-loaded", "decision-recorded", "empty", "error", "focus-visible"],
            },
            "state_model": {
                "domain_states": ["evidence-loaded", "decision-recorded", "empty", "error"],
                "interaction_states": ["focus-visible"],
                "all_states": ["evidence-loaded", "decision-recorded", "empty", "error", "focus-visible"],
            },
            "variants": {
                "axes": ["state"],
                "default": "evidence-loaded",
                "constraints": ["Decision action is available only when evidence is loaded."],
            },
            "props": {
                "state": {"type": "enum", "values": ["evidence-loaded", "decision-recorded", "empty", "error"]},
                "evidence": {"type": "EvidenceRecord[]", "required": True},
            },
            "interaction": {
                "events": ["select-evidence", "record-decision", "retry-load"],
                "state_transitions": [
                    {"from": "evidence-loaded", "event": "record-decision", "to": "decision-recorded"}
                ],
                "focus_behavior": "Keep visible focus on the selected source and return it after recording.",
                "state_coverage": ["evidence-loaded", "decision-recorded", "empty", "error"],
            },
            "data_contract": {
                "domain_object": "evidence-review",
                "required_fields": ["evidence_id", "source_name", "provenance", "decision_status"],
                "provenance_required": True,
                "empty_state_required": True,
            },
            "responsive": {
                "required_widths_px": [390, 1280],
                "control_rules": ["Stack source metadata and keep the decision action in flow below 480px."],
                "container_behavior": "Reflow the desktop rail into a single-column evidence list.",
            },
            "content_rules": [
                "Show source identity and provenance beside every evidence record.",
                "Use an explicit pending state until a decision is recorded.",
            ],
            "dos_and_donts": {
                "do": ["Keep decision status visible after submission."],
                "dont": ["Do not present unsourced evidence as verified."],
            },
            "tokens": {"surface": "var(--ds-color-surface)", "text": "var(--ds-color-ink)"},
            "accessibility": [
                "Expose the evidence collection as a labelled region.",
                "Announce decision status changes with a polite live region.",
            ],
        }],
    }
    (components / "component_specs.json").write_text(json.dumps(payload), encoding="utf-8")
    design_system = project / "design-system"
    design_system.mkdir()
    (design_system / "tokens.css").write_text(
        """:root {
          --ds-color-canvas: #F2F4F7;
          --ds-color-surface: #FFFFFF;
          --ds-color-ink: #111827;
          --ds-color-primary: #2457A7;
          --ds-color-accent: #A76624;
          --ds-space-px-24: 24px;
          --ds-radius-sm: 2px;
          --ds-font-body: Inter, system-ui, sans-serif;
        }""",
        encoding="utf-8",
    )
    (project / "index.html").write_text(
        (
            '<link rel="stylesheet" href="./app.css">'
            '<main data-component-id="evidence-review" data-component-part="root" '
            'data-product-surface="evidence-review" data-model="evidence-decision" '
            'data-source="verified-source-records" data-state="evidence-loaded" '
            'data-component-state="evidence-loaded">'
            '<ul data-component-part="evidence-list">'
            '<li data-component-part="source-record">Verified source</li>'
            '</ul><button data-component-part="decision-action">Record decision</button>'
            '</main>'
        ),
        encoding="utf-8",
    )
    (project / "app.css").write_text(
        """main { display: grid; padding: var(--ds-space-px-24); color: var(--ds-color-ink); background: var(--ds-color-surface); }""",
        encoding="utf-8",
    )


def _write_component_runtime_manifest(project: Path) -> Path:
    specs = json.loads(
        (project / "build/system/components/component_specs.json").read_text(
            encoding="utf-8"
        )
    )
    contract = specs["specs"][0]
    component_id = contract["name"]
    tree = _runtime_implementation_tree(project)
    checked_at = datetime.now(timezone.utc).isoformat(timespec="microseconds")
    component_marker = {
        "source_path": "index.html",
        "attribute": "data-component-id",
        "value": component_id,
    }
    part_markers = [
        {
            "part": part,
            "source_path": "index.html",
            "attribute": "data-component-part",
            "value": part,
        }
        for part in contract["anatomy"]["parts"]
    ]
    assertion = [{"id": "playwright-observation", "passed": True}]
    transitions = contract["interaction"]["state_transitions"]
    interaction_scenarios = []
    for event in contract["interaction"]["events"]:
        scenario = {
            "scenario_id": f"interaction-{event}",
            "event": event,
            "route": "/review",
            "assertions": assertion,
            "focus_assertions": assertion,
        }
        transition = next(
            (
                candidate
                for candidate in transitions
                if isinstance(candidate, dict) and candidate.get("event") == event
            ),
            None,
        )
        if transition is not None:
            scenario["transition"] = transition
        interaction_scenarios.append(scenario)
    evidence = {
        "schema_version": COMPONENT_RUNTIME_EVIDENCE_SCHEMA,
        "component_id": component_id,
        "implementation_tree_sha256": tree["sha256"],
        "checked_at": checked_at,
        "dom": {
            "component_marker": component_marker,
            "part_markers": part_markers,
        },
        "state_scenarios": [
            {
                "scenario_id": f"state-{state}",
                "state": state,
                "route": "/review",
                "observed_marker": {
                    "attribute": "data-component-state",
                    "value": state,
                },
                "assertions": assertion,
            }
            for state in contract["state_model"]["all_states"]
        ],
        "interaction_scenarios": interaction_scenarios,
        "responsive_scenarios": [
            {
                "scenario_id": f"responsive-{width}",
                "width_px": width,
                "covered_rules": contract["responsive"]["control_rules"],
                "container_behavior": contract["responsive"]["container_behavior"],
                "assertions": assertion,
            }
            for width in contract["responsive"]["required_widths_px"]
        ],
        "contract_coverage": {
            "props": list(contract["props"]),
            "data_fields": contract["data_contract"]["required_fields"],
            "content_rules": contract["content_rules"],
            "accessibility_rules": contract["accessibility"],
            "do_rules": contract["dos_and_donts"]["do"],
            "dont_rules": contract["dos_and_donts"]["dont"],
            "variant_axes": contract["variants"]["axes"],
            "default_variant": contract["variants"]["default"],
            "provenance_observed": True,
            "empty_state_observed": True,
        },
    }
    evidence_path = (
        project
        / "build/system/production/component-runtime"
        / f"{component_id}.json"
    )
    _write_json(evidence_path, evidence)
    manifest_path = project / DEFAULT_COMPONENT_RUNTIME_MANIFEST
    _write_json(
        manifest_path,
        {
            "schema_version": COMPONENT_RUNTIME_MANIFEST_SCHEMA,
            "production_claim": True,
            "legacy_policy": "fail-closed",
            "implementation_tree_sha256": tree["sha256"],
            "checked_at": checked_at,
            "components": [
                {
                    "component_id": component_id,
                    "source_paths": [
                        {
                            "path": "index.html",
                            "sha256": _sha256(project / "index.html"),
                        }
                    ],
                    "component_marker": component_marker,
                    "part_markers": part_markers,
                    "evidence": {
                        "path": (
                            "build/system/production/component-runtime/"
                            f"{component_id}.json"
                        ),
                        "sha256": _sha256(evidence_path),
                    },
                }
            ],
        },
    )
    return manifest_path


def _write_browser_evidence_bundle(
    project: Path,
    *,
    screenshot_manifest: Path,
    component_runtime_manifest: Path,
    schema_overrides: dict[str, str] | None = None,
) -> tuple[Path, dict[str, Path]]:
    schema_overrides = schema_overrides or {}
    tree = _runtime_implementation_tree(project)
    screenshot_report = _validated_screenshots(project, screenshot_manifest)
    component_manifest = json.loads(
        component_runtime_manifest.read_text(encoding="utf-8")
    )
    route_states = sorted(
        {
            (record["route"], record["state"])
            for record in screenshot_report["screenshots"]
        }
    )
    route_state_coverage = [
        {"route": route, "state": state} for route, state in route_states
    ]
    viewports = sorted(
        {
            (record["viewport"]["width"], record["viewport"]["height"])
            for record in screenshot_report["screenshots"]
        }
    )
    component_ids = [
        record["component_id"] for record in component_manifest["components"]
    ]
    component_evidence_sha = [
        record["evidence"]["sha256"]
        for record in component_manifest["components"]
    ]
    producer = {
        "kind": IAB_PRODUCER_KIND,
        "tool": IAB_TOOL,
        "skill": "browser:browser",
        "tool_version": "iab-fixture-v1",
        "agent_run_id": "codex-production-qa-fixture-001",
    }
    session_id = "iab-session-fixture-001"
    observed_at = datetime.now(timezone.utc)
    started_at = datetime.fromtimestamp(
        tree["latest_runtime_mtime_ns"] / 1_000_000_000,
        timezone.utc,
    ) + timedelta(microseconds=1)
    observed_iso = observed_at.isoformat(timespec="microseconds")
    observations: list[dict] = []
    raw_paths: dict[str, Path] = {}

    for index, record in enumerate(screenshot_report["screenshots"]):
        path = Path(record["path"])
        observations.append(
            {
                "observation_id": f"screenshot-{index}",
                "kind": "screenshot",
                "browser_session_id": session_id,
                "producer_agent_run_id": producer["agent_run_id"],
                "implementation_tree_sha256": tree["sha256"],
                "observed_at": observed_iso,
                "route": record["route"],
                "state": record["state"],
                "theme": record["theme"],
                "viewport": record["viewport"],
                "artifact": {
                    "root": "project",
                    "path": path.relative_to(project).as_posix(),
                    "sha256": record["sha256"],
                    "media_type": "image/png",
                },
            }
        )

    observation_data = {
        "dom": {
            "route_state_coverage": route_state_coverage,
            "snapshots": [
                {
                    "route": route,
                    "state": state,
                    "selector": "[data-component-id]",
                    "node_count": 4,
                    "content": f'<main data-component-id="evidence-review" data-state="{state}"></main>',
                    "snapshot_sha256": hashlib.sha256(
                        f'<main data-component-id="evidence-review" data-state="{state}"></main>'.encode()
                    ).hexdigest(),
                }
                for route, state in route_states
            ],
        },
        "state": {
            "route_state_coverage": route_state_coverage,
            "observations": [
                {
                    "route": route,
                    "state": state,
                    "selector": "[data-component-state]",
                    "visible": True,
                }
                for route, state in route_states
            ],
        },
        "console": {
            "route_state_coverage": route_state_coverage,
            "messages": [],
            "error_count": 0,
        },
        "interaction": {
            "route_state_coverage": route_state_coverage,
            "events": [
                {
                    "action": "click",
                    "target": "[data-component-part=decision-action]",
                    "before_state": "evidence-loaded",
                    "after_state": "decision-recorded",
                    "passed": True,
                }
            ],
        },
        "overflow": {
            "measurements": [
                {
                    "width": width,
                    "height": height,
                    "scroll_width": width,
                    "client_width": width,
                    "horizontal_overflow_px": 0,
                }
                for width, height in viewports
            ]
        },
        "accessibility": {
            "route_state_coverage": route_state_coverage,
            "standard": "WCAG 2.2 AA",
            "violations": [],
            "keyboard_checks": [
                {
                    "action": "Tab and Enter",
                    "target": "decision action",
                    "passed": True,
                }
            ],
        },
        "component-runtime": {
            "component_ids": component_ids,
            "evidence_sha256": component_evidence_sha,
            "dom_observation_ids": ["dom-observation"],
            "state_observation_ids": ["state-observation"],
            "interaction_observation_ids": ["interaction-observation"],
        },
    }
    for kind, data in observation_data.items():
        observation_id = f"{kind}-observation"
        raw_payload = {
            "schema_version": schema_overrides.get(
                kind, BROWSER_OBSERVATION_SCHEMA
            ),
            "observation_id": observation_id,
            "kind": kind,
            "browser_session_id": session_id,
            "implementation_tree_sha256": tree["sha256"],
            "observed_at": observed_iso,
            "producer": producer,
            "data": data,
        }
        raw_path = (
            project
            / "build/system/production/browser-observations"
            / f"{kind}.json"
        )
        _write_json(raw_path, raw_payload)
        raw_paths[kind] = raw_path
        observations.append(
            {
                "observation_id": observation_id,
                "kind": kind,
                "browser_session_id": session_id,
                "producer_agent_run_id": producer["agent_run_id"],
                "implementation_tree_sha256": tree["sha256"],
                "observed_at": observed_iso,
                "artifact": {
                    "root": "project",
                    "path": raw_path.relative_to(project).as_posix(),
                    "sha256": _sha256(raw_path),
                    "media_type": "application/json",
                },
            }
        )

    bundle_path = project / DEFAULT_BROWSER_EVIDENCE_BUNDLE
    _write_json(
        bundle_path,
        {
            "schema_version": BROWSER_EVIDENCE_BUNDLE_SCHEMA,
            "bundle_id": "browser-bundle-fixture-001",
            "project": project.name,
            "recorded_at": observed_iso,
            "implementation_tree": {
                "algorithm": tree["algorithm"],
                "sha256": tree["sha256"],
                "file_count": tree["file_count"],
            },
            "producer": producer,
            "browser_session": {
                "session_id": session_id,
                "target_url": "http://127.0.0.1:8780/review",
                "user_agent": "Codex Desktop IAB fixture",
                "started_at": started_at.isoformat(timespec="microseconds"),
                "ended_at": observed_iso,
            },
            "screenshot_manifest": {
                "root": "project",
                "path": screenshot_manifest.relative_to(project).as_posix(),
                "sha256": _sha256(screenshot_manifest),
                "media_type": "application/json",
            },
            "component_runtime_manifest": {
                "root": "project",
                "path": component_runtime_manifest.relative_to(project).as_posix(),
                "sha256": _sha256(component_runtime_manifest),
                "media_type": "application/json",
            },
            "observations": observations,
        },
    )
    return bundle_path, raw_paths


def _validated_screenshots(project: Path, manifest: Path) -> dict:
    report = validate_screenshot_manifest(manifest, project=project.name, target_repo=project)
    assert report["ok"], report["errors"]
    return report


def test_screenshot_manifest_requires_symmetric_route_state_theme_viewports(tmp_path: Path) -> None:
    project = tmp_path / "fieldnote"
    screenshots = _make_screenshots(project)
    manifest = _record_all(project, screenshots)

    report = _validated_screenshots(project, manifest)
    assert report["resolved_implementation_sha"] == report["implementation_sha"]

    payload = json.loads(manifest.read_text(encoding="utf-8"))
    payload["screenshots"] = payload["screenshots"][:-1]
    manifest.write_text(json.dumps(payload), encoding="utf-8")
    report = validate_screenshot_manifest(manifest, project=project.name, target_repo=project)
    assert not report["ok"]
    assert any("needs both mobile and desktop" in error for error in report["errors"])
    assert any("lacks symmetric theme coverage" in error for error in report["errors"])


def test_screenshot_manifest_rejects_runtime_mutation_after_capture(tmp_path: Path) -> None:
    project = tmp_path / "fieldnote"
    screenshots = _make_screenshots(project)
    manifest = _record_all(project, screenshots)
    assert validate_screenshot_manifest(
        manifest,
        project=project.name,
        target_repo=project,
    )["ok"]

    runtime_entry = project / "index.html"
    runtime_entry.write_text("<main>Different uncommitted runtime</main>", encoding="utf-8")
    newest_screenshot = max(path.stat().st_mtime_ns for path in screenshots)
    os.utime(runtime_entry, ns=(newest_screenshot + 1_000_000, newest_screenshot + 1_000_000))

    report = validate_screenshot_manifest(
        manifest,
        project=project.name,
        target_repo=project,
    )

    assert not report["ok"]
    assert any("implementation_tree.sha256" in error for error in report["errors"])
    assert any("older than the current runtime implementation" in error for error in report["errors"])


def test_screenshot_recorder_rejects_capture_older_than_runtime(tmp_path: Path) -> None:
    project = tmp_path / "fieldnote"
    screenshots = _make_screenshots(project)
    runtime_entry = project / "index.html"
    newest_screenshot = max(path.stat().st_mtime_ns for path in screenshots)
    os.utime(runtime_entry, ns=(newest_screenshot + 1_000_000, newest_screenshot + 1_000_000))
    implementation_sha = _ensure_git_head(project)

    with pytest.raises(ValueError, match="screenshot is older than the runtime implementation"):
        record_screenshot_evidence(
            manifest_path=project / "build/system/production/screenshots.json",
            project=project.name,
            target_repo=project,
            screenshot_path=screenshots[0],
            route="/review",
            state="evidence-selected",
            theme="light",
            implementation_sha=implementation_sha,
        )


def test_runtime_tree_follows_local_page_assets_and_excludes_evidence(tmp_path: Path) -> None:
    project = tmp_path / "fieldnote"
    (project / "assets").mkdir(parents=True)
    (project / "public/generated/design-system").mkdir(parents=True)
    (project / "build/system/production/evidence").mkdir(parents=True)
    (project / "index.html").write_text(
        """
        <link rel="stylesheet" href="./styles.css?v=3">
        <link rel="manifest" href="./site.webmanifest#app">
        <img src="/assets/hero.webp?crop=wide" alt="">
        <img srcset="./assets/hero.webp 1x, ./assets/retina.webp 2x" alt="">
        <script src=./app.js?v=4></script>
        """,
        encoding="utf-8",
    )
    (project / "app.js").write_text("document.body.dataset.ready = 'true';", encoding="utf-8")
    (project / "styles.css").write_text(
        ".hero { background-image: url(./assets/background.png?v=2); }",
        encoding="utf-8",
    )
    (project / "site.webmanifest").write_text(
        json.dumps({"icons": [{"src": "./assets/app-icon.svg#mask"}]}),
        encoding="utf-8",
    )
    for name, color in (
        ("hero.webp", "#123456"),
        ("retina.webp", "#193857"),
        ("background.png", "#234567"),
        ("unused.png", "#345678"),
    ):
        Image.new("RGB", (20, 20), color).save(project / "assets" / name)
    (project / "assets/app-icon.svg").write_text("<svg/>", encoding="utf-8")
    (project / "public/generated/design-system/manifest.json").write_text(
        json.dumps(
            {
                "assets": [
                    {
                        "status": "integrated",
                        "asset_path": "assets/hero.webp",
                        "original_png_path": "/outside/provenance-only.png",
                    }
                ]
            }
        ),
        encoding="utf-8",
    )
    (project / "build/system/production/evidence/stale.json").write_text("{}", encoding="utf-8")

    tree = _runtime_implementation_tree(project)
    paths = {record["path"] for record in tree["files"]}

    assert paths == {
        "assets/app-icon.svg",
        "assets/background.png",
        "assets/hero.webp",
        "assets/retina.webp",
        "app.js",
        "index.html",
        "public/generated/design-system/manifest.json",
        "site.webmanifest",
        "styles.css",
    }
    assert "assets/unused.png" not in paths
    assert not any(path.startswith("build/") for path in paths)


def test_runtime_tree_supports_dist_only_deployments(tmp_path: Path) -> None:
    project = tmp_path / "dist-app"
    (project / "dist/assets").mkdir(parents=True)
    (project / "dist/index.html").write_text(
        '<script src="./assets/app.js?v=1"></script>',
        encoding="utf-8",
    )
    (project / "dist/assets/app.js").write_text("document.body.dataset.ready = 'true';", encoding="utf-8")
    (project / "build/system/production/evidence").mkdir(parents=True)
    (project / "build/system/production/evidence/check.json").write_text("{}", encoding="utf-8")

    tree = _runtime_implementation_tree(project)
    paths = {record["path"] for record in tree["files"]}

    assert paths == {"dist/assets/app.js", "dist/index.html"}


def test_runtime_tree_rejects_mutable_remote_runtime_dependencies(tmp_path: Path) -> None:
    project = tmp_path / "remote-app"
    project.mkdir()
    (project / "index.html").write_text(
        '<script src=https://cdn.example.test/app.js?v=latest></script>',
        encoding="utf-8",
    )

    with pytest.raises(ValueError, match="remote runtime reference cannot be content-bound"):
        _runtime_implementation_tree(project)


def test_screenshot_evidence_rejects_flat_color_capture(tmp_path: Path) -> None:
    project = tmp_path / "fieldnote"
    screenshot = project / "screenshots" / "blank.png"
    screenshot.parent.mkdir(parents=True)
    Image.new("RGB", (390, 844), "#F2F4F7").save(screenshot)

    with pytest.raises(ValueError, match="minimum visual information"):
        record_screenshot_evidence(
            manifest_path=project / "screenshots.json",
            project=project.name,
            target_repo=project,
            screenshot_path=screenshot,
            route="/review",
            state="evidence-selected",
            theme="light",
            implementation_sha="unverified",
        )


def test_bare_multimodal_source_label_cannot_substantiate_scores(tmp_path: Path) -> None:
    project = tmp_path / "fieldnote"
    screenshots = _make_screenshots(project)
    manifest = _record_all(project, screenshots)
    screenshot_report = _validated_screenshots(project, manifest)
    report = _aesthetic_report(project, screenshots, source="multimodal-review")
    report["measurement_protocol"].pop("production_review")
    report_path = project / "aesthetic.json"
    _write_json(report_path, report)

    errors, _ = _validate_aesthetic_report(
        report_path,
        screenshot_paths=set(screenshot_report["resolved_paths"]),
        screenshot_records=screenshot_report["screenshots"],
        target_repo=project,
    )
    assert any("production_review is required" in error for error in errors)


def test_semantic_metrics_require_verified_multimodal_review(tmp_path: Path) -> None:
    project = tmp_path / "fieldnote"
    screenshots = _make_screenshots(project)
    manifest = _record_all(project, screenshots)
    screenshot_report = _validated_screenshots(project, manifest)
    report_path = project / "aesthetic.json"

    _write_json(report_path, _aesthetic_report(project, screenshots, source="automated"))
    errors, _ = _validate_aesthetic_report(
        report_path,
        screenshot_paths=set(screenshot_report["resolved_paths"]),
        screenshot_records=screenshot_report["screenshots"],
        target_repo=project,
    )
    assert any("semantic industry-fit metrics" in error for error in errors)
    assert any("multimodal review run" in error for error in errors)

    _write_json(report_path, _aesthetic_report(project, screenshots, source="multimodal-review"))
    errors, _ = _validate_aesthetic_report(
        report_path,
        screenshot_paths=set(screenshot_report["resolved_paths"]),
        screenshot_records=screenshot_report["screenshots"],
        target_repo=project,
    )
    assert not errors


def test_runtime_interaction_overflow_and_accessibility_evidence_is_blocking(tmp_path: Path) -> None:
    project = tmp_path / "fieldnote"
    screenshots = _make_screenshots(project)
    manifest = _record_all(project, screenshots)
    screenshot_report = _validated_screenshots(project, manifest)
    report = _aesthetic_report(project, screenshots, source="multimodal-review")
    runtime_checks = report["measurement_protocol"]["production_review"]["runtime_checks"]
    report["measurement_protocol"]["production_review"]["runtime_checks"] = [
        check for check in runtime_checks if check["kind"] != "accessibility"
    ]
    report_path = project / "aesthetic.json"
    _write_json(report_path, report)

    errors, _ = _validate_aesthetic_report(
        report_path,
        screenshot_paths=set(screenshot_report["resolved_paths"]),
        screenshot_records=screenshot_report["screenshots"],
        target_repo=project,
    )
    assert any("missing runtime checks: accessibility" in error for error in errors)


def test_runtime_check_artifacts_bind_to_current_tree_and_freshness(tmp_path: Path) -> None:
    project = tmp_path / "fieldnote"
    screenshots = _make_screenshots(project)
    manifest = _record_all(project, screenshots)
    screenshot_report = _validated_screenshots(project, manifest)
    report = _aesthetic_report(project, screenshots, source="multimodal-review")
    runtime_check = report["measurement_protocol"]["production_review"]["runtime_checks"][0]
    artifact_path = project / runtime_check["artifact"]["path"]
    payload = json.loads(artifact_path.read_text(encoding="utf-8"))
    payload["implementation_tree_sha256"] = "forged-tree"
    payload["checked_at"] = "1970-01-01T00:00:00+00:00"
    _write_json(artifact_path, payload)
    runtime_check["artifact"]["sha256"] = _sha256(artifact_path)
    report_path = project / "aesthetic.json"
    _write_json(report_path, report)

    errors, _ = _validate_aesthetic_report(
        report_path,
        screenshot_paths=set(screenshot_report["resolved_paths"]),
        screenshot_records=screenshot_report["screenshots"],
        target_repo=project,
    )

    assert any("implementation_tree_sha256" in error for error in errors)
    assert any("checked_at is older" in error for error in errors)

    tree = _runtime_implementation_tree(project)
    payload["implementation_tree_sha256"] = tree["sha256"]
    payload["checked_at"] = datetime.now(timezone.utc).isoformat(timespec="microseconds")
    _write_json(artifact_path, payload)
    runtime_check["artifact"]["sha256"] = _sha256(artifact_path)
    stale_mtime = tree["latest_runtime_mtime_ns"] - 1
    os.utime(artifact_path, ns=(stale_mtime, stale_mtime))
    _write_json(report_path, report)

    errors, _ = _validate_aesthetic_report(
        report_path,
        screenshot_paths=set(screenshot_report["resolved_paths"]),
        screenshot_records=screenshot_report["screenshots"],
        target_repo=project,
    )

    assert any("artifact file is older" in error for error in errors)


def test_review_hash_coverage_must_match_screenshot_manifest(tmp_path: Path) -> None:
    project = tmp_path / "fieldnote"
    screenshots = _make_screenshots(project)
    manifest = _record_all(project, screenshots)
    screenshot_report = _validated_screenshots(project, manifest)
    report = _aesthetic_report(project, screenshots, source="multimodal-review")
    review_run = report["measurement_protocol"]["production_review"]["review_runs"][0]
    review_run["screenshot_sha256"] = review_run["screenshot_sha256"][:-1]
    report_path = project / "aesthetic.json"
    _write_json(report_path, report)

    errors, _ = _validate_aesthetic_report(
        report_path,
        screenshot_paths=set(screenshot_report["resolved_paths"]),
        screenshot_records=screenshot_report["screenshots"],
        target_repo=project,
    )
    assert any("do not cover every screenshot SHA" in error for error in errors)
    assert any("artifact screenshot hashes do not match" in error for error in errors)


def test_verify_production_ui_combines_all_release_gates(tmp_path: Path) -> None:
    project = tmp_path / "fieldnote"
    project.mkdir()
    _write_component_contract(project)
    screenshots = _make_screenshots(project)
    screenshot_manifest = _record_all(project, screenshots)
    aesthetic_path = project / "build" / "system" / "aesthetic" / "latest_loop_report.json"
    _write_json(
        aesthetic_path,
        _aesthetic_report(project, screenshots, source="multimodal-review"),
    )
    component_runtime_manifest = _write_component_runtime_manifest(project)
    browser_bundle, _ = _write_browser_evidence_bundle(
        project,
        screenshot_manifest=screenshot_manifest,
        component_runtime_manifest=component_runtime_manifest,
    )

    report = verify_production_ui(
        project_dir=project,
        target_repo=project,
        screenshot_manifest_path=screenshot_manifest,
        aesthetic_report_path=aesthetic_path,
        registry_path=tmp_path / "style-registry.json",
    )

    assert report["ok"], report["errors"]
    assert {gate["name"] for gate in report["gates"]} == {
        "component_contracts",
        "component_runtime_conformance",
        "implementation_lint",
        "screenshot_evidence",
        "browser_evidence_bundle",
        "aesthetic_evidence",
        "style_divergence",
    }

    approved_direction = project / "design-system" / "references" / "selected-direction.md"
    approved_direction.parent.mkdir(parents=True, exist_ok=True)
    approved_direction.write_text("# Approved direction\n", encoding="utf-8")
    missing_fidelity_contract = verify_production_ui(
        project_dir=project,
        target_repo=project,
        screenshot_manifest_path=screenshot_manifest,
        aesthetic_report_path=aesthetic_path,
        registry_path=tmp_path / "style-registry.json",
    )
    fidelity_gate = next(
        gate
        for gate in missing_fidelity_contract["gates"]
        if gate["name"] == "reference_fidelity"
    )
    assert not fidelity_gate["ok"]
    assert any("contract.json is missing" in error for error in fidelity_gate["errors"])
    approved_direction.unlink()

    browser_bundle.unlink()
    missing_browser_evidence = verify_production_ui(
        project_dir=project,
        target_repo=project,
        screenshot_manifest_path=screenshot_manifest,
        aesthetic_report_path=aesthetic_path,
        registry_path=tmp_path / "style-registry.json",
    )
    browser_gate = next(
        gate
        for gate in missing_browser_evidence["gates"]
        if gate["name"] == "browser_evidence_bundle"
    )
    assert not missing_browser_evidence["ok"]
    assert not browser_gate["ok"]
    assert any("bundle not found" in error for error in browser_gate["errors"])

    _write_browser_evidence_bundle(
        project,
        screenshot_manifest=screenshot_manifest,
        component_runtime_manifest=component_runtime_manifest,
    )

    component_runtime_manifest.unlink()
    blocked = verify_production_ui(
        project_dir=project,
        target_repo=project,
        screenshot_manifest_path=screenshot_manifest,
        aesthetic_report_path=aesthetic_path,
        registry_path=tmp_path / "style-registry.json",
    )
    runtime_gate = next(
        gate
        for gate in blocked["gates"]
        if gate["name"] == "component_runtime_conformance"
    )
    assert not blocked["ok"]
    assert not runtime_gate["ok"]
    assert any("manifest not found" in error for error in runtime_gate["errors"])


def test_legacy_runtime_check_v1_fails_closed_as_browser_evidence(
    tmp_path: Path,
) -> None:
    project = tmp_path / "fieldnote"
    project.mkdir()
    _write_component_contract(project)
    screenshots = _make_screenshots(project)
    screenshot_manifest = _record_all(project, screenshots)
    aesthetic_path = (
        project / "build" / "system" / "aesthetic" / "latest_loop_report.json"
    )
    _write_json(
        aesthetic_path,
        _aesthetic_report(project, screenshots, source="multimodal-review"),
    )
    component_runtime_manifest = _write_component_runtime_manifest(project)
    _write_browser_evidence_bundle(
        project,
        screenshot_manifest=screenshot_manifest,
        component_runtime_manifest=component_runtime_manifest,
        schema_overrides={"interaction": "production-ui-runtime-check/v1"},
    )

    report = verify_production_ui(
        project_dir=project,
        target_repo=project,
        screenshot_manifest_path=screenshot_manifest,
        aesthetic_report_path=aesthetic_path,
        registry_path=tmp_path / "style-registry.json",
    )
    browser_gate = next(
        gate
        for gate in report["gates"]
        if gate["name"] == "browser_evidence_bundle"
    )

    assert not report["ok"]
    assert not browser_gate["ok"]
    assert any(
        "legacy-unverified and fails closed" in error
        for error in browser_gate["errors"]
    )


def test_browser_bundle_rejects_raw_observation_from_another_session(
    tmp_path: Path,
) -> None:
    project = tmp_path / "fieldnote"
    project.mkdir()
    _write_component_contract(project)
    screenshots = _make_screenshots(project)
    screenshot_manifest = _record_all(project, screenshots)
    aesthetic_path = (
        project / "build" / "system" / "aesthetic" / "latest_loop_report.json"
    )
    _write_json(
        aesthetic_path,
        _aesthetic_report(project, screenshots, source="multimodal-review"),
    )
    component_runtime_manifest = _write_component_runtime_manifest(project)
    bundle_path, raw_paths = _write_browser_evidence_bundle(
        project,
        screenshot_manifest=screenshot_manifest,
        component_runtime_manifest=component_runtime_manifest,
    )
    raw_interaction = json.loads(
        raw_paths["interaction"].read_text(encoding="utf-8")
    )
    raw_interaction["browser_session_id"] = "iab-session-forged-002"
    _write_json(raw_paths["interaction"], raw_interaction)
    bundle = json.loads(bundle_path.read_text(encoding="utf-8"))
    interaction_record = next(
        record
        for record in bundle["observations"]
        if record["kind"] == "interaction"
    )
    interaction_record["artifact"]["sha256"] = _sha256(raw_paths["interaction"])
    _write_json(bundle_path, bundle)

    report = verify_production_ui(
        project_dir=project,
        target_repo=project,
        screenshot_manifest_path=screenshot_manifest,
        aesthetic_report_path=aesthetic_path,
        registry_path=tmp_path / "style-registry.json",
    )
    browser_gate = next(
        gate
        for gate in report["gates"]
        if gate["name"] == "browser_evidence_bundle"
    )

    assert not browser_gate["ok"]
    assert any(
        "artifact browser_session_id does not match"
        in error
        for error in browser_gate["errors"]
    )
