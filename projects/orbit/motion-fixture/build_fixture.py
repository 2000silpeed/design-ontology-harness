"""Regenerate this fixture's interaction contract.

The fixture demonstrates what the resolver picks for a dense operational
dashboard, using the same code path a real project uses. Run it from the repo
root after changing the candidate packs or the CSS generator:

    uv run python projects/orbit/motion-fixture/build_fixture.py
"""

from __future__ import annotations

from pathlib import Path

from design_ontology_harness.interaction_css import (
    build_interaction_contract_md,
    build_interactions_css,
)
from design_ontology_harness.interaction_resolver import resolve_interaction_patterns

FIXTURE_DIR = Path(__file__).resolve().parent

# A dashboard's surfaces, named the way a real brand profile would name them.
COMPONENT_STATES = {
    "signal-list": ["content-enter", "filtered"],
    "signal-card": ["selected", "attention-required"],
    "refresh-action": ["loading", "processing"],
    "status-chip": ["current", "attention-required"],
    "range-tabs": ["current", "selected"],
}


def main() -> None:
    selection = resolve_interaction_patterns(
        product_intent="monitor live signals and decide what needs attention",
        component_states=COMPONENT_STATES,
        accessibility_targets=["WCAG 2.2 AA", "reduced motion"],
        motion_budget=2,
        density="dense",
        # Pinned so the committed fixture is reproducible; real projects leave
        # this unset and let the tie-break vary.
        variation_seed=7,
    )
    (FIXTURE_DIR / "interactions.css").write_text(
        build_interactions_css(selection, "orbit-motion-fixture"), encoding="utf-8"
    )
    (FIXTURE_DIR / "INTERACTION.md").write_text(
        build_interaction_contract_md(selection, "orbit-motion-fixture"), encoding="utf-8"
    )
    for item in selection["selected"]:
        print(f"{item['axis']:11} {item['id']}")


if __name__ == "__main__":
    main()
