"""Generate system_spec.md sections 18-20 from the ontology graph."""

from __future__ import annotations

from .graph_schema import DesignOntologyGraph, EdgeType, NodeType


_TOKEN_CATEGORY_LABEL = {
    NodeType.ColorToken: "color",
    NodeType.SpacingToken: "spacing",
    NodeType.RadiusToken: "radius",
    NodeType.MotionToken: "motion",
    NodeType.ElevationToken: "elevation",
    NodeType.FontFamily: "font",
}


def _token_pretty(category: str, label: str, slot: str | None) -> str:
    prefix = f"{category}.{label}" if category != "font" else f"font:{label}"
    return f"{prefix}→{slot}" if slot else prefix


def build_component_token_map_section(graph: DesignOntologyGraph) -> str:
    components = graph.get_nodes_by_type(NodeType.Component)
    if not components:
        return "No component-token mappings available."

    rows: list[str] = []
    rows.append("| Component | Tokens Used |")
    rows.append("|-----------|-------------|")

    for comp in sorted(components, key=lambda n: n.label):
        token_edges = list(graph.get_edges_from(comp.id, EdgeType.uses_token))
        token_edges += list(graph.get_edges_from(comp.id, EdgeType.uses_font))
        if not token_edges:
            continue

        token_labels: list[str] = []
        for edge in token_edges:
            node = graph.get_node(edge.target)
            if not node:
                continue
            category = _TOKEN_CATEGORY_LABEL.get(node.type, node.type.value.lower())
            slot = (edge.meta or {}).get("slot")
            token_labels.append(f"`{_token_pretty(category, node.label, slot)}`")

        if token_labels:
            rows.append(f"| {comp.label} | {', '.join(token_labels[:8])} |")

    if len(rows) <= 2:
        return "No component-token mappings emitted. Check build_component_token_layer."

    return "\n".join(rows)


def build_contrast_audit_section(graph: DesignOntologyGraph) -> str:
    contrast_edges = [e for e in graph.edges if e.type == EdgeType.contrast_pair]
    if not contrast_edges:
        return "No contrast pairs defined. Add `contrast_surfaces` to color_reference or verify palette_roles."

    rows: list[str] = []
    rows.append("| Background | Foreground | Ratio | Level |")
    rows.append("|------------|------------|-------|-------|")

    for edge in sorted(contrast_edges, key=lambda e: e.meta.get("ratio", 0), reverse=True):
        bg = graph.get_node(edge.source)
        fg = graph.get_node(edge.target)
        if not bg or not fg:
            continue
        ratio = edge.meta.get("ratio", 0)
        level = edge.meta.get("level", "fail")
        status = "pass" if level in ("AA", "AAA") else "large-only" if level == "AA-large" else "FAIL"
        rows.append(f"| {bg.label} | {fg.label} | {ratio:.2f}:1 | {level} ({status}) |")

    return "\n".join(rows)


def build_pattern_catalog_section(graph: DesignOntologyGraph) -> str:
    layout_patterns = graph.get_nodes_by_type(NodeType.LayoutPattern)
    interaction_patterns = graph.get_nodes_by_type(NodeType.InteractionPattern)

    if not layout_patterns and not interaction_patterns:
        return "No patterns cataloged."

    lines: list[str] = []

    if layout_patterns:
        lines.append("### Layout Patterns")
        lines.append("")
        for pattern in layout_patterns:
            comp_edges = graph.get_edges_from(pattern.id, EdgeType.composed_of)
            comp_names = []
            for edge in comp_edges:
                node = graph.get_node(edge.target)
                if node:
                    comp_names.append(node.label)
            comp_str = ", ".join(comp_names) if comp_names else "—"
            lines.append(f"- **{pattern.label}**: {comp_str}")

    if interaction_patterns:
        lines.append("")
        lines.append("### Interaction Patterns")
        lines.append("")
        for pattern in interaction_patterns:
            comp_edges = graph.get_edges_from(pattern.id, EdgeType.composed_of)
            comp_names = []
            for edge in comp_edges:
                node = graph.get_node(edge.target)
                if node:
                    comp_names.append(node.label)
            comp_str = ", ".join(comp_names) if comp_names else "—"
            lines.append(f"- **{pattern.label}**: {comp_str}")

    return "\n".join(lines)


def build_generated_visual_asset_section(graph: DesignOntologyGraph) -> str:
    assets = graph.get_nodes_by_type(NodeType.GeneratedVisualAsset)
    if not assets:
        return "No generated visual asset slots defined."

    lines: list[str] = []
    contract = graph.get_node("governance:generated-visual-asset-contract")
    if contract:
        lines.append(
            f"- **Contract**: `{contract.meta.get('schema_version', 'visual-asset-manifest/v1')}` / "
            f"preferred manifest `{contract.meta.get('preferred_manifest_path', 'public/generated/design-system/manifest.json')}`"
        )
        compatible_paths = contract.meta.get("compatible_manifest_paths") or []
        if compatible_paths:
            lines.append(f"- **Compatible paths**: {', '.join(f'`{path}`' for path in compatible_paths)}")
        lines.append(
            "- **Execution**: built-in Codex `image_gen`; workspace copy required; original generated PNG preserved in manifest; API fallback disabled."
        )
        required_fields = contract.meta.get("asset_record_required_fields") or []
        if required_fields:
            lines.append(f"- **Required asset record fields**: {', '.join(f'`{field}`' for field in required_fields[:14])}")
        lines.append("")

    integrated_assets = [
        asset for asset in assets
        if asset.meta.get("integrated") or asset.meta.get("asset_path")
    ]
    if integrated_assets:
        lines.append("### Integrated Assets")
        lines.append("")
        lines.append("| Asset | Slot | Workspace Path | Alt Text |")
        lines.append("|-------|------|----------------|----------|")
        for asset in sorted(integrated_assets, key=lambda n: n.label):
            slot = asset.meta.get("slot", "—")
            path = asset.meta.get("asset_path", "—")
            alt_text = asset.meta.get("alt_text", "—")
            lines.append(f"| {asset.label} | {slot} | `{path}` | {alt_text} |")
        lines.append("")

    rows: list[str] = []
    rows.append("| Asset Slot | Generator | Intended For | Manifest | Failure Policy |")
    rows.append("|------------|-----------|--------------|----------|----------------|")

    for asset in sorted(assets, key=lambda n: n.label):
        model = "—"
        for edge in graph.get_edges_from(asset.id, EdgeType.generated_with):
            node = graph.get_node(edge.target)
            if node:
                model = node.label
                break

        targets: list[str] = []
        for edge in graph.get_edges_from(asset.id, EdgeType.intended_for):
            node = graph.get_node(edge.target)
            if node:
                targets.append(node.label)

        manifest = asset.meta.get("manifest_path", "—")
        failure_policy = asset.meta.get("fallback_policy", "—")
        intended_for = ", ".join(targets[:6]) if targets else ", ".join(asset.meta.get("intended_for", [])[:6])
        if not intended_for:
            intended_for = asset.meta.get("activation", "optional")
        rows.append(f"| {asset.label} | {model} | {intended_for} | `{manifest}` | {failure_policy} |")

    lines.extend(rows)
    return "\n".join(lines)


def build_brand_identity_asset_section(graph: DesignOntologyGraph) -> str:
    assets = graph.get_nodes_by_type(NodeType.BrandIdentityAsset)
    if not assets:
        return "No brand identity assets defined."

    lines: list[str] = []
    policy = graph.get_node("governance:brand-app-icon-identity")
    if policy:
        lines.append(f"- **Policy**: {policy.meta.get('rule', 'Brand-specific app icon required.')}")
        rules = policy.meta.get("implementation_rules") or []
        if rules:
            lines.append("- **Implementation rules**:")
            for rule in rules[:6]:
                lines.append(f"  - {rule}")
        failure_edges = graph.get_edges_from(policy.id, EdgeType.prevents)
        if failure_edges:
            lines.append("- **Promoted failure patterns**:")
            for edge in failure_edges[:6]:
                failure = graph.get_node(edge.target)
                if failure:
                    lines.append(f"  - {failure.label}: {failure.meta.get('prevention', '')}")
        lines.append("")

    lines.append("| Asset | Required | Workspace Path | Targets | Formats |")
    lines.append("|-------|----------|----------------|---------|---------|")
    for asset in sorted(assets, key=lambda n: n.label):
        required = "yes" if asset.meta.get("required") else "no"
        path = asset.meta.get("asset_path") or asset.meta.get("favicon_path") or "—"
        targets = ", ".join(asset.meta.get("targets", [])[:6]) or "—"
        formats = ", ".join(asset.meta.get("formats", [])[:4]) or "—"
        lines.append(f"| {asset.label} | {required} | `{path}` | {targets} | {formats} |")

    return "\n".join(lines)


def build_reference_intelligence_section(graph: DesignOntologyGraph) -> str:
    providers = graph.get_nodes_by_type(NodeType.ReferenceProvider)
    cards = graph.get_nodes_by_type(NodeType.DesignContextCard)
    pack_nodes = graph.get_nodes_by_type(NodeType.DesignContextPack)
    if not providers and not cards and not pack_nodes:
        return "No reference intelligence pack defined."

    lines: list[str] = []
    if pack_nodes:
        pack = pack_nodes[0]
        lines.append(
            f"- **Activation**: {pack.meta.get('activation_state', 'planned')} / "
            f"research gaps: {pack.meta.get('research_gap_count', 0)}"
        )
        if pack.meta.get("allowed"):
            lines.append(f"- **Allowed from references**: {', '.join(pack.meta.get('allowed', [])[:6])}")
        if pack.meta.get("denied"):
            lines.append(f"- **Denied from references**: {', '.join(pack.meta.get('denied', [])[:6])}")
        lines.append("")

    if providers:
        lines.append("| Provider | Status | Access | Role |")
        lines.append("|----------|--------|--------|------|")
        for provider in sorted(providers, key=lambda node: node.label):
            lines.append(
                f"| {provider.label} | {provider.meta.get('status', 'n/a')} | "
                f"{provider.meta.get('access_mode', 'n/a')} | {provider.meta.get('truth_role', 'reference')} |"
            )
        lines.append("")

    if cards:
        lines.append("| Context | Provider | Provenance | Allowed Use |")
        lines.append("|---------|----------|------------|-------------|")
        for card in sorted(cards, key=lambda node: node.label)[:12]:
            provider_edges = graph.get_edges_from(card.id, EdgeType.provided_by)
            provider = "—"
            if provider_edges:
                provider_node = graph.get_node(provider_edges[0].target)
                if provider_node:
                    provider = provider_node.label
            flows = ", ".join(card.meta.get("flows", [])[:3]) or "general"
            morphology = ", ".join(card.meta.get("morphology", [])[:3]) or "general"
            lines.append(
                f"| {card.label} | {provider} | {card.meta.get('provenance_level', 'planned')} | "
                f"flows: {flows}; morphology: {morphology} |"
            )

    return "\n".join(lines)


def build_graph_spec_sections(graph: DesignOntologyGraph) -> str:
    return f"""## 18. Component-Token Map

{build_component_token_map_section(graph)}

## 19. Contrast Audit

{build_contrast_audit_section(graph)}

## 20. Pattern Catalog

{build_pattern_catalog_section(graph)}

## 21. Brand Identity Assets

{build_brand_identity_asset_section(graph)}

## 22. Generated Visual Asset Plan

{build_generated_visual_asset_section(graph)}

## 23. Reference Intelligence Pack

{build_reference_intelligence_section(graph)}
"""
