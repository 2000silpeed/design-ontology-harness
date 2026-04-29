#!/usr/bin/env bash
# Sync harness presets/ to the design-ontology-plugin repo.
#
# 1. Run sync-time compatibility validator (hard gate)
# 2. On pass: copy presets/ + adapters/base/ + adapter MVP to plugin clone
# 3. Create PR with compatibility report in body
#
# Usage:
#   scripts/sync-plugin-presets.sh --plugin-repo <path> [--branch <name>]

set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
PLUGIN_REPO=""
BRANCH="sync/harness-presets-$(date -u +%Y%m%d-%H%M%S)"
DRY_RUN=0

usage() {
  cat <<EOF
Usage: $(basename "$0") --plugin-repo <path> [--branch <name>] [--dry-run]

Runs scripts/check-plugin-compatibility.py first. If the check fails, the sync
is aborted and no files are copied.
EOF
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    --plugin-repo)
      PLUGIN_REPO="$2"
      shift 2
      ;;
    --branch)
      BRANCH="$2"
      shift 2
      ;;
    --dry-run)
      DRY_RUN=1
      shift
      ;;
    -h|--help)
      usage
      exit 0
      ;;
    *)
      echo "unknown flag: $1" >&2
      usage
      exit 2
      ;;
  esac
done

if [[ -z "$PLUGIN_REPO" ]]; then
  echo "error: --plugin-repo is required" >&2
  usage
  exit 2
fi

if [[ ! -d "$PLUGIN_REPO" ]]; then
  echo "error: plugin-repo not a directory: $PLUGIN_REPO" >&2
  exit 2
fi

echo "[sync] harness root: $REPO_ROOT"
echo "[sync] plugin repo:  $PLUGIN_REPO"

# Step 1 — compatibility gate
REPORT_FILE="$(mktemp -t sync-report.XXXXXX)"
trap 'rm -f "$REPORT_FILE"' EXIT

set +e
python3 "$REPO_ROOT/scripts/check-plugin-compatibility.py" \
  --plugin-repo "$PLUGIN_REPO" \
  --presets-dir "$REPO_ROOT/presets" \
  | tee "$REPORT_FILE"
COMPAT_RC=${PIPESTATUS[0]}
set -e

if [[ "$COMPAT_RC" -ne 0 ]]; then
  echo "[sync] compatibility check FAILED (rc=$COMPAT_RC). Aborting."
  exit "$COMPAT_RC"
fi
echo "[sync] compatibility check PASSED"

if [[ "$DRY_RUN" -eq 1 ]]; then
  echo "[sync] dry-run: skipping copy + git + PR"
  exit 0
fi

# Step 2 — branch + copy
pushd "$PLUGIN_REPO" >/dev/null
git fetch origin
git checkout -B "$BRANCH" origin/main

mkdir -p presets adapters
# Exclude operational metadata (Phase 15-1): catalog-health output is harness-only,
# .metrics/ install·match counters are local manual scoreboards.
rsync -a --delete \
  --exclude '.metrics' \
  --exclude 'CATALOG_HEALTH.md' \
  "$REPO_ROOT/presets/" "./presets/"
if [[ -d "$REPO_ROOT/adapters/base" ]]; then
  rsync -a --delete "$REPO_ROOT/adapters/base/" "./adapters/base/"
fi
if [[ -d "$REPO_ROOT/adapters/nextjs-tailwind-shadcn" ]]; then
  rsync -a --delete "$REPO_ROOT/adapters/nextjs-tailwind-shadcn/" "./adapters/nextjs-tailwind-shadcn/"
fi

git add presets adapters
if git diff --cached --quiet; then
  echo "[sync] no changes to commit. exiting."
  popd >/dev/null
  exit 0
fi

git commit -m "chore(sync): update presets + adapters from harness"

# Step 3 — push + PR (requires gh)
if command -v gh >/dev/null 2>&1; then
  git push -u origin "$BRANCH"
  gh pr create \
    --title "chore(sync): update presets from harness" \
    --body "$(printf 'Automated sync from design-ontology-harness.\n\n## Compatibility report\n\n```\n%s\n```\n' "$(cat "$REPORT_FILE")")" \
    --base main
else
  echo "[sync] gh not found. Branch '$BRANCH' committed locally. Push/PR manually."
fi

popd >/dev/null
echo "[sync] done."
