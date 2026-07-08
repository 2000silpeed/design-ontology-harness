"""Reference-backed baseline component policy.

The harness treats public design systems as evidence for taxonomy and state
coverage, not as implementation source to copy. Astryx gives us breadth and
agent-oriented component docs; Vercel Geist gives us a compact developer-tool
baseline. This module keeps that decision explicit and shared across analyzers.
"""

from __future__ import annotations

from copy import deepcopy
from typing import Any


REFERENCE_COMPONENT_SYSTEMS: tuple[dict[str, Any], ...] = (
    {
        "id": "astryx",
        "name": "Astryx",
        "url": "https://astryx.atmeta.com/components",
        "role": "broad React component taxonomy, templates, themes, and agent-ready docs",
        "use_for": [
            "component family breadth",
            "state and anatomy coverage hints",
            "agent documentation and CLI workflow patterns",
        ],
    },
    {
        "id": "geist",
        "name": "Vercel Geist",
        "url": "https://vercel.com/geist/introduction",
        "role": "compact developer-tool UI baseline with precise, minimal interaction patterns",
        "use_for": [
            "developer-console primitives",
            "compact monochrome surface behavior",
            "accessibility and async state coverage labels",
        ],
    },
)


REFERENCE_ABSORPTION_POLICY: dict[str, Any] = {
    "allowed": [
        "component names and taxonomy",
        "family grouping",
        "state coverage hints",
        "interaction and accessibility labels",
        "token category ideas",
    ],
    "denied": [
        "verbatim docs beyond short labels",
        "brand logos or protected imagery",
        "site-specific IA or product copy",
        "implementation source code unless the project license and target use allow it",
    ],
    "rule": "Use Astryx and Geist as taxonomy and behavior evidence; implement with local primitives and local tokens.",
}


FAMILY_SPECS: dict[str, dict[str, Any]] = {
    "button": {"states": ["default", "hover", "active", "disabled", "loading"], "priority": "high"},
    "input": {"states": ["default", "focus", "error", "disabled", "selected"], "priority": "high"},
    "navigation": {"states": ["default", "active", "hover", "collapsed"], "priority": "high"},
    "feedback": {"states": ["info", "success", "warning", "danger", "loading"], "priority": "high"},
    "overlay": {"states": ["closed", "opening", "open"], "priority": "medium"},
    "surface": {"states": ["default", "hover", "selected", "disabled"], "priority": "medium"},
    "content": {"states": ["default", "hover", "selected"], "priority": "medium"},
    "layout": {"states": ["default", "responsive"], "priority": "high"},
    "editorial": {"states": ["default", "selected", "editing"], "priority": "high"},
    "data-display": {"states": ["default", "sorted", "filtered", "empty", "loading"], "priority": "high"},
    "marketing": {"states": ["default", "hover", "in-view"], "priority": "high"},
    "workflow": {"states": ["pending", "active", "blocked", "approved"], "priority": "high"},
    "document": {"states": ["default", "selected", "commenting", "resolved"], "priority": "high"},
    "copilot-chat": {"states": ["default", "loading", "complete", "error"], "priority": "high"},
    "copilot-artifact": {"states": ["default", "loading", "verified", "error"], "priority": "high"},
}


BASELINE_COMPONENTS: dict[str, dict[str, Any]] = {
    "primary-button": {
        "family": "button",
        "role": "Primary action button for the most important local action.",
        "reference_components": ["Astryx Button", "Geist Button"],
    },
    "secondary-button": {
        "family": "button",
        "role": "Secondary action button with lower emphasis than the primary action.",
        "reference_components": ["Astryx Button", "Geist Button"],
    },
    "icon-button": {
        "family": "button",
        "role": "Icon-only action with explicit accessible name and stable hit target.",
        "reference_components": ["Astryx Icon Button", "Geist Copy Button", "Geist Dots Menu"],
    },
    "text-field": {
        "family": "input",
        "role": "Single-line text input with label, helper, error, disabled, and readonly states.",
        "reference_components": ["Astryx Text Input", "Geist Input"],
    },
    "select": {
        "family": "input",
        "role": "Single-value option selector for bounded choices.",
        "reference_components": ["Astryx Selector", "Geist Select"],
    },
    "checkbox": {
        "family": "input",
        "role": "Boolean or multi-select input with checked, unchecked, mixed, and disabled states.",
        "reference_components": ["Astryx Checkbox Input", "Geist Checkbox"],
    },
    "switch": {
        "family": "input",
        "role": "Immediate on/off preference control.",
        "reference_components": ["Astryx Switch", "Geist Switch"],
    },
    "segmented-control": {
        "family": "input",
        "role": "Small mutually exclusive mode switcher.",
        "reference_components": ["Astryx Segmented Control", "Geist Toggle"],
    },
    "breadcrumbs": {
        "family": "navigation",
        "role": "Hierarchy trail for deep product areas.",
        "reference_components": ["Astryx Breadcrumbs", "Geist Breadcrumbs"],
    },
    "tabs": {
        "family": "navigation",
        "role": "Peer view switcher for related panels.",
        "reference_components": ["Astryx Tabs", "Geist Tabs"],
    },
    "pagination": {
        "family": "navigation",
        "role": "Paged data navigation for tables and long lists.",
        "reference_components": ["Astryx Pagination", "Geist Pagination"],
    },
    "badge": {
        "family": "feedback",
        "role": "Compact status, category, or count label.",
        "reference_components": ["Astryx Badge", "Geist Badge"],
    },
    "inline-alert": {
        "family": "feedback",
        "role": "Inline message for contextual info, success, warning, and error states.",
        "reference_components": ["Astryx Banner", "Geist Banner", "Geist Note"],
    },
    "empty-state": {
        "family": "feedback",
        "role": "Actionable empty or zero-result state.",
        "reference_components": ["Astryx Empty State", "Geist Empty State"],
    },
    "toast": {
        "family": "feedback",
        "role": "Temporary non-blocking feedback after a completed action.",
        "reference_components": ["Astryx Toast", "Geist Toast"],
    },
    "status-dot": {
        "family": "feedback",
        "role": "Small operational status indicator paired with visible text.",
        "reference_components": ["Astryx Status Dot", "Geist Status Dot"],
    },
    "dialog": {
        "family": "overlay",
        "role": "Modal decision or focused task surface.",
        "reference_components": ["Astryx Dialog", "Geist Modal"],
    },
    "popover": {
        "family": "overlay",
        "role": "Anchored transient surface for short forms or contextual controls.",
        "reference_components": ["Astryx Popover", "Geist Context Menu"],
    },
    "tooltip": {
        "family": "overlay",
        "role": "Short accessible explanation for icon-only or compact controls.",
        "reference_components": ["Astryx Tooltip", "Geist Tooltip"],
    },
    "data-table": {
        "family": "data-display",
        "role": "Sortable, filterable record table with row actions and empty/loading states.",
        "reference_components": ["Astryx Table", "Geist Table"],
    },
    "list": {
        "family": "data-display",
        "role": "Stacked item collection with stable row rhythm.",
        "reference_components": ["Astryx List", "Geist Entity"],
    },
    "metadata-list": {
        "family": "data-display",
        "role": "Key-value detail list for records, settings, and source facts.",
        "reference_components": ["Astryx Metadata List", "Geist Description"],
    },
    "app-shell": {
        "family": "layout",
        "role": "Responsive product shell that owns primary navigation and page chrome.",
        "reference_components": ["Astryx App Shell", "Geist Grid"],
    },
    "grid": {
        "family": "layout",
        "role": "Responsive layout grid with min-width-safe tracks.",
        "reference_components": ["Astryx Grid", "Geist Grid"],
    },
    "section": {
        "family": "layout",
        "role": "Named page region with controlled spacing and heading relationship.",
        "reference_components": ["Astryx Section", "Geist Grid"],
    },
    "divider": {
        "family": "layout",
        "role": "Hairline separation between related regions.",
        "reference_components": ["Astryx Divider", "Geist Separator"],
    },
}


BASELINE_FAMILY_COMPONENTS: dict[str, tuple[str, ...]] = {
    "button": ("primary-button", "secondary-button", "icon-button"),
    "input": ("text-field", "select", "checkbox", "switch", "segmented-control"),
    "navigation": ("breadcrumbs", "tabs", "pagination"),
    "feedback": ("badge", "inline-alert", "empty-state", "toast", "status-dot"),
    "overlay": ("dialog", "popover", "tooltip"),
    "data-display": ("data-table", "list", "metadata-list"),
    "layout": ("app-shell", "grid", "section", "divider"),
}


CONTEXTUAL_COMPONENTS: dict[str, dict[str, Any]] = {
    "ghost-button": {"replacement": "secondary-button", "reason": "variant, not a baseline component"},
    "link-button": {"replacement": "link", "reason": "content/link primitive, not an action baseline"},
    "cta-button": {"replacement": "primary-button", "reason": "marketing emphasis variant"},
    "mobile-topbar": {"replacement": "app-shell or top-nav", "reason": "platform-specific navigation"},
    "mobile-tab-bar": {"replacement": "tabs", "reason": "mobile-specific navigation variant"},
    "back-button": {"replacement": "breadcrumbs", "reason": "flow-specific control"},
    "bottom-sheet": {"replacement": "dialog or drawer", "reason": "mobile-specific overlay variant"},
    "modal-dialog": {"replacement": "dialog", "reason": "duplicate naming"},
}


def core_baseline_components() -> list[dict[str, Any]]:
    """Return the always-on component seed for spec analysis."""

    names = ("primary-button", "secondary-button", "icon-button")
    components: list[dict[str, Any]] = []
    for name in names:
        component = deepcopy(BASELINE_COMPONENTS[name])
        component["name"] = name
        components.append(component)
    return components


def baseline_component_meta(name: str) -> dict[str, Any]:
    """Return metadata for a baseline component name."""

    component = deepcopy(BASELINE_COMPONENTS.get(name, {}))
    if component:
        component["name"] = name
    return component


def reference_baseline_summary() -> dict[str, Any]:
    """Serializable summary stored in generated component inventories."""

    return {
        "schema_version": "component-reference-baseline/v1",
        "systems": [dict(system) for system in REFERENCE_COMPONENT_SYSTEMS],
        "absorption_policy": deepcopy(REFERENCE_ABSORPTION_POLICY),
        "core_components": list(BASELINE_FAMILY_COMPONENTS["button"]),
        "contextual_not_baseline": deepcopy(CONTEXTUAL_COMPONENTS),
    }
