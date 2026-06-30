# TacticLens Harness Agent Brief

This project uses `design-ontology-harness` as a reusable system-authoring harness.

## What The Agent Should Do

1. Read `brand_profile.json`
2. Read `spec.md`
3. Read `seeds/seed_urls.txt`
4. Load the configured knowledge base
5. Produce custom system outputs into `build/`
6. Avoid copying any single reference system directly

## Success Criteria

- The outputs reflect a professional football video-analysis workspace, not a generic sports dashboard
- The system spec is useful for a real product team building upload, review, playbook, report, and tactical timeline flows
- Tokens and components are grounded in video review, pitch maps, tactical principles, confidence states, and human review queues
- Korean football-analysis terminology is treated as a first-class UI requirement
