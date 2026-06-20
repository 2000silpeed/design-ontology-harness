from __future__ import annotations

import json
from pathlib import Path

from design_ontology_harness.adapters import load_preset_bundle
from design_ontology_harness.preset_builder import PRESETS_ROOT
from design_ontology_harness.style_capsule import render_style_markdown


def _load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def test_style_capsule_renders_agent_ready_governance() -> None:
    preset_dir = PRESETS_ROOT / "conversation-copilot--corporate-trust"
    bundle = load_preset_bundle(preset_dir)
    component_inventory = _load_json(preset_dir / "component_inventory.json")

    text = render_style_markdown(
        preset_id=bundle.id,
        manifest=bundle.manifest,
        brand_profile=bundle.brand_profile,
        blueprint=bundle.blueprint,
        token_schema=bundle.token_schema,
        component_inventory=component_inventory,
        component_specs=bundle.component_specs,
    )

    assert "Style Capsule" in text
    assert "DESIGN.md" in text
    assert "Visual references are morphology inputs only" in text
    assert "Token binding is necessary but not sufficient" in text
    assert "--ds-color-primary" in text
    assert "Pretendard" in text
    assert "lint-implementation" in text
    assert "token-bound-reference-palette-mixing" in text
    assert "Advanced Component Menu" in text
    assert "policy-matrix" in text
    assert "Design Context Pack" in text
