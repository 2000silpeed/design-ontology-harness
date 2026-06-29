# Agent Org Network

Agent Org Network is a design-system harness project for an operational console
that maps AI agents, human owners, tools, handoffs, policies, and run health
across an organization.

## Files

- `brand_profile.json`: product identity, visual direction, and reference settings
- `spec.md`: product screens, data objects, interactions, and component needs
- `seeds/seed_urls.txt`: curated reference entry points
- `project_manifest.json`: project metadata
- `agent_brief.md`: instructions for human or agent collaborators
- `build/`: generated outputs, ignored by git

## How To Run

```bash
uv run design-ontology curate-omnigen-references \
  --project-dir projects/agent-org-network \
  --vault-dir ~/.omnigen-vault \
  --query "multi agent orchestration dashboard agent task console tool timeline workflow DAG model evaluation org network graph policy table" \
  --count 12 \
  --max-per-subject 1 \
  --max-ocr-chars 160

uv run design-ontology run-project --project-dir projects/agent-org-network
```

## Review Points

1. Check `build/visuals/omnigen_reference_gallery.html` for reference quality.
2. Review `build/visuals/design_context_pack.json` for density and layout cues.
3. Review `build/system/blueprint/system_spec.md` after synthesis.
4. Keep the final product grounded in graph, table, timeline, ownership, and policy state.
