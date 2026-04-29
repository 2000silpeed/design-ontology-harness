"""Stack adapters — render presets into framework-specific outputs.

Each adapter translates a preset bundle (presets/<id>/) into a list of file
operations against a target repo. The base module defines the common contract;
concrete adapters live in their own modules.
"""

from __future__ import annotations

from .base import (
    ApplyReport,
    FileOp,
    PresetBundle,
    StackAdapter,
    load_preset_bundle,
    tokens_for_mode,
)

__all__ = [
    "ApplyReport",
    "FileOp",
    "PresetBundle",
    "StackAdapter",
    "load_preset_bundle",
    "tokens_for_mode",
    "get_adapter",
    "list_adapters",
]


def _registry() -> dict:
    # Deferred import to avoid cycles; concrete adapters import from .base.
    from .nextjs_tailwind_shadcn import NextjsTailwindShadcnAdapter
    from .raw_css_variables import RawCssVariablesAdapter
    from .vite_tailwind import ViteTailwindAdapter

    return {
        NextjsTailwindShadcnAdapter.id: NextjsTailwindShadcnAdapter,
        RawCssVariablesAdapter.id: RawCssVariablesAdapter,
        ViteTailwindAdapter.id: ViteTailwindAdapter,
    }


def list_adapters() -> list[str]:
    return sorted(_registry().keys())


def get_adapter(adapter_id: str) -> type[StackAdapter]:
    registry = _registry()
    if adapter_id not in registry:
        raise KeyError(
            f"Unknown adapter '{adapter_id}'. Available: {', '.join(sorted(registry))}"
        )
    return registry[adapter_id]
