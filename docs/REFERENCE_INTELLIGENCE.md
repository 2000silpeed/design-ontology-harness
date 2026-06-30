# Reference Intelligence

Reference Intelligence is the layer that turns external visual research into
ontology-safe design context. It exists so agents can learn from real screens
without copying their palette, typography, IA, copy, or assets.

## What It Adds

- `Design Context Pack`: provider-neutral research artifact generated from
  `visual_reference`, query suggestions, and configured providers.
- `ReferenceProvider` ontology nodes: local images, Pinterest-assisted capture,
  Lazyweb MCP/export, Figma export, Playwright website inspection, or other future providers.
- `DesignContextCard` ontology nodes: selected screenshots or planned research
  queries with flow and morphology tags.
- Governance: every provider and context card repeats the allowed/denied
  absorption scope.

## Provider Model

Configure providers inside `brand_profile.visual_reference`:

```json
{
  "visual_reference": {
    "mode": "local-images",
    "sources": ["references/visual"],
    "reference_providers": [
      {
        "provider_id": "lazyweb",
        "status": "active",
        "access_mode": "mcp",
        "truth_role": "real app flow and screen corpus provider"
      }
    ],
    "sources": [
      {
        "kind": "lazyweb",
        "label": "Remote contractor compliance dashboard",
        "url": "https://remote.com/global-hr/contractor-of-record",
        "tags": ["compliance", "dashboard", "approval", "card"]
      }
    ]
  }
}
```

`lazyweb` is allowed as a provider plan even when the MCP is not connected.
`enabled: true` alone keeps it `suggested`; use `status: "active"` only after a
real MCP search/export produced selected references. Lazyweb source URLs become
`external-reference` context cards, and query strings are stripped before they
are written into the design context pack.

## Authority Rule

External references are last in the authority order. They may influence:

- component morphology
- layout density
- panel/card proportions
- hierarchy rhythm
- interaction affordance patterns
- flow pattern labels

Use `inspect-reference-site` when a live website should become this kind of
reference context. The command records screenshots, topology, behaviors, assets,
and computed-style evidence, but the same authority rule still applies.

They must not influence:

- color palette or palette composition
- typography scale
- domain IA
- product copy
- redistributable imagery unless explicitly licensed

## Outputs

When a project has `visual_reference`, the harness writes:

- `build/system/blueprint/design_context_pack.json`
- `build/system/blueprint/design_system_blueprint.json`
- `build/system/blueprint/system_ontology.json`
- `build/system/blueprint/system_spec.md`

The `analyze-visuals` and `generate-visual-queries` commands also write
`build/visuals/design_context_pack.json` for early review.
