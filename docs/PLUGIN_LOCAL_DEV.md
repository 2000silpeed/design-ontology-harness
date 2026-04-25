# Plugin Local Dev (harness side)

Quick guide for iterating on the plugin **before** the public marketplace listing exists.

Companion doc in the plugin repo: `design-ontology-plugin/docs/LOCAL_DEV.md` (kept in sync).

> **External preset contributors**: if you landed here to add a P3 preset, read
> [`CONTRIBUTING_PRESETS.md`](./CONTRIBUTING_PRESETS.md) first. This document is
> harness maintainers' view; the contributor path (5 steps + `build-sources` +
> PR template) lives in CONTRIBUTING_PRESETS.md.

---

## Layout assumption

```
~/ai-projects/
├── design-ontology-harness/    # this repo — presets generator
└── design-ontology-plugin/     # sibling — public plugin repo
```

Adjust paths below if your layout differs.

---

## 0. Prerequisites (first-time external contributors)

| Requirement | Check |
|---|---|
| Python 3.11+ | `python3 --version` |
| [`uv`](https://docs.astral.sh/uv/) (package manager, replaces pip/venv) | `uv --version` |
| `git` | `git --version` |
| Optional: `gh` CLI for PR creation | `gh --version` |

First invocation:

```bash
cd ~/ai-projects/design-ontology-harness
uv run design-ontology --help          # first run triggers dependency sync (~30s–2min)
uv run --with pytest pytest tests/ -v  # verifies your local checkout is green
```

The harness bundles a shared KB snapshot at `kb/default/` (checked into git).
Contributors **do not** need to run `build-kb` — point `run-project` and
`init` at `--kb-dir kb/default` and you are ready to go.

---

## 1. One-time setup (harness maintainers)

Clone (or scaffold) the plugin repo next to the harness:

```bash
cd ~/ai-projects
# Once the public repo exists:
# git clone git@github.com:<org>/design-ontology-plugin.git
# Until then, Phase 9 scaffolds the repo locally — it already lives at
#   ~/ai-projects/design-ontology-plugin
```

Verify the harness can read it:

```bash
python3 scripts/check-plugin-compatibility.py \
  --plugin-repo ~/ai-projects/design-ontology-plugin
```

Expected last line: `compatibility OK`.

---

## 2. Dry-run a sync

```bash
./scripts/sync-plugin-presets.sh \
  --plugin-repo ~/ai-projects/design-ontology-plugin \
  --dry-run
```

This runs the compatibility gate only — it never touches files or git. Use it after:
- editing any `presets/*/manifest.json`
- changing `presets/compatibility.json`
- updating the plugin's `.claude-plugin/plugin.json` `supported_preset_api`
- adding a new preset

Failure cases the gate catches:
- `preset_api_version` outside the plugin's supported range
- missing `preset_api_version` field
- `presets/compatibility.json` missing `supported_preset_api_range`
- plugin `supported_preset_api` malformed

---

## 3. Full local sync (no GitHub)

The production sync opens a PR. Locally, you usually just want the files copied into the plugin working tree so you can test skills/agents end-to-end.

### Option A — skip git, just rsync

```bash
PLUGIN=~/ai-projects/design-ontology-plugin

# Gate first
python3 scripts/check-plugin-compatibility.py --plugin-repo "$PLUGIN"

rsync -a --delete presets/ "$PLUGIN/presets/"
[[ -d adapters/base ]] && rsync -a --delete adapters/base/ "$PLUGIN/adapters/base/"
[[ -d adapters/nextjs-tailwind-shadcn ]] && rsync -a --delete adapters/nextjs-tailwind-shadcn/ "$PLUGIN/adapters/nextjs-tailwind-shadcn/"
```

### Option B — use the full script against a local branch

```bash
# In the plugin repo, make sure `origin/main` exists locally (can point at an
# empty upstream branch during early development):
( cd ~/ai-projects/design-ontology-plugin && git init -q && git commit --allow-empty -m init -q && git branch -M main )

# Then run the script without --dry-run. It will create a `sync/...` branch
# inside the plugin repo and (if gh is installed + configured) open a PR.
```

---

## 4. Installing the plugin into a test project

While the plugin is local-only, use `/plugin install` with a filesystem path.

```text
/plugin marketplace add file:///Users/<you>/ai-projects/design-ontology-plugin
/plugin install design-ontology
```

Claude Code resolves skills from `.claude-plugin/plugin.json`. Re-run `/plugin install` after major changes.

---

## 5. Iteration loop

```
edit harness presets/
  ↓
./scripts/sync-plugin-presets.sh --plugin-repo $PLUGIN --dry-run
  ↓ (gate passes)
rsync or full sync
  ↓
open a test repo → /plugin install design-ontology → /design-start
  ↓
adjust skill/agent prompts in plugin repo directly
```

Skill + agent prompts live in the plugin repo and are **authored there**. The sync script only overwrites `presets/` and `adapters/` — it will never clobber `skills/` or `agents/`.

---

## 6. Version contract reminders

- Every preset manifest requires all four version fields: `schema_version`, `preset_api_version`, `generated_by_harness_version`, `preview_version`.
- Plugin `supported_preset_api` range must contain every preset's `preset_api_version`.
- When bumping `preset_api_version` (breaking): bump the plugin `supported_preset_api` at the same PR, or the gate blocks sync.
- `presets/compatibility.json` in the harness is the single source of truth for `current_preset_api_version` and `supported_preset_api_range`.

---

## 7. Troubleshooting

| Symptom | Likely cause | Fix |
|---------|--------------|-----|
| `plugin.json missing 'supported_preset_api'` | Plugin manifest drift | Re-add the field in `.claude-plugin/plugin.json` |
| `plugin.json.supported_preset_api '...' is not a valid range` | Typo (e.g. `>= 1.0.0`) | Remove spaces inside bound, use `>=1.0.0 <2.0.0` |
| Gate passes but sync PR creation fails | `gh` auth missing | Run `gh auth login` or pass `--dry-run` |
| `checked 0 preset manifest(s)` | Presets not generated yet | Run Phase 8 (`uv run design-ontology build-preset ...`) |
| Skill changes not picked up | Cached install | Re-run `/plugin install design-ontology` in the test project |
