# Catalog Health Report

> Generated at `2026-08-10T10:15:40Z` · harness `0.2.0`

## Overview

- 누적 프리셋: **25**
- Tier 분포: P0 5 · P1 5 · P2 5 · P3 10
- 셀 커버리지: 25/40 (= 62%)
- Snapshot drift: 0건
- Deprecation 후보: 25건
- Deprecated 프리셋: 0건
- Prune eligible: 0건 (deprecated ≥ 90일 + hits 0)

## Priority Empty Cells (Top-10)

| Priority | Cell |
|---|---|
| 3 | `commerce--minimal-tech` |
| 6 | `marketing-landing--playful-soft` |
| 10 | `canvas-tool--bold-confident` |

## Empty Cells (full list)

| Cell | Priority |
|---|---|
| `commerce--minimal-tech` | 3 |
| `marketing-landing--playful-soft` | 6 |
| `canvas-tool--bold-confident` | 10 |
| `canvas-tool--editorial-warm` | — |
| `canvas-tool--playful-soft` | — |
| `commerce--corporate-trust` | — |
| `community-feed--bold-confident` | — |
| `community-feed--corporate-trust` | — |
| `community-feed--editorial-warm` | — |
| `community-feed--minimal-tech` | — |
| `conversation-copilot--bold-confident` | — |
| `conversation-copilot--playful-soft` | — |
| `marketing-landing--corporate-trust` | — |
| `monitoring-ops--editorial-warm` | — |
| `monitoring-ops--playful-soft` | — |

## Deprecation Candidates

| Preset | Tier | Install | Match | Drift | Lint | Reasons |
|---|---|---|---|---|---|---|
| `canvas-tool--corporate-trust` | P3 | 0 | 0 | 0 | OK | zero_hits |
| `canvas-tool--minimal-tech` | P1 | 0 | 0 | 0 | OK | zero_hits |
| `commerce--bold-confident` | P2 | 0 | 0 | 0 | OK | zero_hits |
| `commerce--editorial-warm` | P0 | 0 | 0 | 0 | OK | zero_hits |
| `commerce--playful-soft` | P3 | 0 | 0 | 0 | OK | zero_hits |
| `community-feed--playful-soft` | P1 | 0 | 0 | 0 | OK | zero_hits |
| `conversation-copilot--corporate-trust` | P3 | 0 | 0 | 0 | OK | zero_hits |
| `conversation-copilot--editorial-warm` | P2 | 0 | 0 | 0 | OK | zero_hits |
| `conversation-copilot--minimal-tech` | P0 | 0 | 0 | 0 | OK | zero_hits |
| `dashboard--bold-confident` | P3 | 0 | 0 | 0 | OK | zero_hits |
| `dashboard--corporate-trust` | P1 | 0 | 0 | 0 | OK | zero_hits |
| `dashboard--editorial-warm` | P2 | 0 | 0 | 0 | OK | zero_hits |
| `dashboard--minimal-tech` | P0 | 0 | 0 | 0 | OK | zero_hits |
| `dashboard--playful-soft` | P3 | 0 | 0 | 0 | OK | zero_hits |
| `document-content--bold-confident` | P2 | 0 | 0 | 0 | OK | zero_hits |
| `document-content--corporate-trust` | P3 | 0 | 0 | 0 | OK | zero_hits |
| `document-content--editorial-warm` | P0 | 0 | 0 | 0 | OK | zero_hits |
| `document-content--minimal-tech` | P1 | 0 | 0 | 0 | OK | zero_hits |
| `document-content--playful-soft` | P3 | 0 | 0 | 0 | OK | zero_hits |
| `marketing-landing--bold-confident` | P0 | 0 | 0 | 0 | OK | zero_hits |
| `marketing-landing--editorial-warm` | P3 | 0 | 0 | 0 | OK | zero_hits |
| `marketing-landing--minimal-tech` | P2 | 0 | 0 | 0 | OK | zero_hits |
| `monitoring-ops--bold-confident` | P3 | 0 | 0 | 0 | OK | zero_hits |
| `monitoring-ops--corporate-trust` | P3 | 0 | 0 | 0 | OK | zero_hits |
| `monitoring-ops--minimal-tech` | P1 | 0 | 0 | 0 | OK | zero_hits |

## Deprecated

- ✅ 현재 deprecated 프리셋 없음

## Prune Eligible

> `deprecated_at` 이후 90일 이상 경과 + install/match hits 0 인 프리셋. `uv run design-ontology prune-preset <id> --confirm` 으로 실삭제.

- ✅ 현재 prune 대상 없음

## Per-Preset Metrics

| Preset | Tier | Owner | Harness ver | Drift | Lint | Install | Match | Snapshot |
|---|---|---|---|---|---|---|---|---|
| `canvas-tool--corporate-trust` | P3 | 2000silpeed | 0.2.0 | 0 | OK | 0 | 0 | · |
| `canvas-tool--minimal-tech` | P1 | maintainer | 0.2.0 | 0 | OK | 0 | 0 | · |
| `commerce--bold-confident` | P2 | maintainer | 0.2.0 | 0 | OK | 0 | 0 | · |
| `commerce--editorial-warm` | P0 | maintainer | 0.2.0 | 0 | OK | 0 | 0 | · |
| `commerce--playful-soft` | P3 | @alice-external | 0.2.0 | 0 | OK | 0 | 0 | · |
| `community-feed--playful-soft` | P1 | maintainer | 0.2.0 | 0 | OK | 0 | 0 | · |
| `conversation-copilot--corporate-trust` | P3 | @carol-external | 0.2.0 | 0 | OK | 0 | 0 | · |
| `conversation-copilot--editorial-warm` | P2 | maintainer | 0.2.0 | 0 | OK | 0 | 0 | · |
| `conversation-copilot--minimal-tech` | P0 | maintainer | 0.2.0 | 0 | OK | 0 | 0 | · |
| `dashboard--bold-confident` | P3 | @maintainer-dogfood | 0.2.0 | 0 | OK | 0 | 0 | · |
| `dashboard--corporate-trust` | P1 | sungwoon | 0.2.0 | 0 | OK | 0 | 0 | · |
| `dashboard--editorial-warm` | P2 | maintainer | 0.2.0 | 0 | OK | 0 | 0 | · |
| `dashboard--minimal-tech` | P0 | maintainer | 0.2.0 | 0 | OK | 0 | 0 | · |
| `dashboard--playful-soft` | P3 | @maintainer-dogfood | 0.2.0 | 0 | OK | 0 | 0 | · |
| `document-content--bold-confident` | P2 | maintainer | 0.2.0 | 0 | OK | 0 | 0 | · |
| `document-content--corporate-trust` | P3 | 2000silpeed | 0.2.0 | 0 | OK | 0 | 0 | · |
| `document-content--editorial-warm` | P0 | maintainer | 0.2.0 | 0 | OK | 0 | 0 | · |
| `document-content--minimal-tech` | P1 | maintainer | 0.2.0 | 0 | OK | 0 | 0 | · |
| `document-content--playful-soft` | P3 | codex | 0.2.0 | 0 | OK | 0 | 0 | · |
| `marketing-landing--bold-confident` | P0 | maintainer | 0.2.0 | 0 | OK | 0 | 0 | · |
| `marketing-landing--editorial-warm` | P3 | @bob-external | 0.2.0 | 0 | OK | 0 | 0 | · |
| `marketing-landing--minimal-tech` | P2 | maintainer | 0.2.0 | 0 | OK | 0 | 0 | · |
| `monitoring-ops--bold-confident` | P3 | codex | 0.2.0 | 0 | OK | 0 | 0 | · |
| `monitoring-ops--corporate-trust` | P3 | codex | 0.2.0 | 0 | OK | 0 | 0 | · |
| `monitoring-ops--minimal-tech` | P1 | maintainer | 0.2.0 | 0 | OK | 0 | 0 | · |

## Sources

- install hits: `/home/runner/work/design-ontology-harness/design-ontology-harness/presets/.metrics/install_hits.json`
- match hits: `/home/runner/work/design-ontology-harness/design-ontology-harness/presets/.metrics/match_hits.json`
- snapshot fixture: `/home/runner/work/design-ontology-harness/design-ontology-harness/tests/fixtures/preset_snapshots.json`
