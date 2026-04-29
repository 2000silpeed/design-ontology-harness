# Catalog Health Report — 2026 Q2

> **분기**: 2026-04-01 ~ 2026-06-30
> **발간일**: 2026-04-21 (2026 Q2 첫 리허설 발간)
> **생성자**: harness `0.1.0` · `uv run design-ontology catalog-health`
> **소스**: [`presets/CATALOG_HEALTH.md`](../presets/CATALOG_HEALTH.md) (항상 최신), [`docs/MAINTAINER_REVIEW_SOP.md`](./MAINTAINER_REVIEW_SOP.md) §11 실측 시간표

---

## 1. 분기 요약

| 지표 | Q1 말 (2026-03-31 기준) | Q2 리허설 (2026-04-21 기준) | Δ |
|---|---:|---:|---:|
| 누적 프리셋 | 15 | **20** | **+5** |
| P0 | 5 | 5 | — |
| P1 | 5 | 5 | — |
| P2 | 5 | 5 | — |
| P3 | 0 | **5** | **+5** |
| 셀 커버리지 (40셀 기준) | 15/40 (38%) | **20/40 (50%)** | +12 pt |
| Snapshot drift | 0 | 0 | — |
| Deprecation 후보 | 15 | 20 | +5 (전부 zero_hits · §3 참조) |
| Deprecated 프리셋 | 0 | 0 | — |
| Prune eligible (≥ 90d) | 0 | 0 | — |
| eval-matcher accuracy | 1.00 (50/50) | **1.00 (66/66)** | +16 labels |

**2026 Q2 도착** 시점부터 Phase 13-11-A/B/C 누적 **P3 커뮤니티 확장 경로 5 종** 이 완성. Phase 13-11-D 부터는 공개 홍보 이후 실제 외부 PR 접수 사이클로 전환.

## 2. 신규 접수 · 승격 이력

### 2026 Q2 신규 P3 (5 종, 전부 dogfood / maintainer-curated)

| Preset | Tier | Owner | Source Project | Phase | 날짜 |
|---|:---:|---|---|:---:|:---:|
| `dashboard--bold-confident` | P3 | `@maintainer-dogfood` | `lattice-dash` | 13-11-A | 2026-04-20 |
| `dashboard--playful-soft` | P3 | `@maintainer-dogfood` | `meadow` | 13-11-A | 2026-04-20 |
| `commerce--playful-soft` | P3 | `@alice-external` (persona) | `orchard` | 13-11-B | 2026-04-20 |
| `marketing-landing--editorial-warm` | P3 | `@bob-external` (persona) | `loom` | **13-11-C** | **2026-04-21** |
| `conversation-copilot--corporate-trust` | P3 | `@carol-external` (persona) | `mercer` | **13-11-C** | **2026-04-21** |

### 2026 Q2 승격 (0 건)

- Q2 중 dry-run 승격 시뮬레이션 5 회 (`promote-preset --target P2 --dry-run`), 전부 5-gate 통과했으나 실제 승격은 **Phase 13-11-D 까지 유예** — 실측 install_hits / match_hits 데이터 수집 기간 확보 우선.

## 3. Deprecation 후보 분석

**현재 20 종 전부** 가 deprecation 후보 (`zero_hits`) 로 집계된다. 원인:

- `presets/.metrics/install_hits.json` · `match_hits.json` 은 Phase 15-1 에 **빈 dict scaffold** 로만 생성됨. CLI 호출에서 자동 count 증가 hook 이 미구현 — 수동 입력도 0 건.
- 따라서 "설치·매칭 hit 0" 조건은 현재 **측정 파이프라인 부재** 에 기인한 것이지, 실제 사용자 무관심을 반영하지 않음.

### 결정

1. **Q2 에는 deprecation 실행 없음** — 실측 metric 부재 상태에서 zero_hits 만으로는 deprecation 기준 (PLAN §11.2) 을 충족한다고 볼 수 없음.
2. **Q3 부터 측정 파이프라인 도입 결정 대기** (§6 참조) — 실측 metric 축적 후 Q4 첫 정식 deprecation dry-run.

## 4. Priority Empty Cells (다음 분기 수요 예상)

2026-04-21 기준 `catalog-health` 가 자동 계산한 우선순위 상위 5 빈 셀:

| 순위 | 셀 | 다음 분기 기여 권장도 |
|:---:|---|---|
| 3 | `commerce--minimal-tech` | 🔥 높음 — B2B/테크 커머스 (Stripe-style 결제·API 상점) 수요 예상 |
| 6 | `marketing-landing--playful-soft` | 🔥 높음 — 컨슈머 랜딩 (D2C 스낵·생활용품) |
| 8 | `document-content--corporate-trust` | 중간 — 엔터프라이즈 docs (금융·헬스케어 규정 문서) |
| 9 | `monitoring-ops--corporate-trust` | 중간 — 엔터프라이즈 observability (규제·감사 컨텍스트) |
| 10 | `canvas-tool--bold-confident` | 낮음 — 크리에이터 전용 bold 캔버스 (스트리머·밈·숏폼) |

**분기 priority 제안** (`commerce--minimal-tech` / `marketing-landing--playful-soft` 2 종을 Q3 우선 집중) — Phase 13-11-D 에서 실제 외부 기여자 또는 maintainer-dogfood 로 채우는 것을 권장.

## 5. Q3 P3 → P2 승급 계획

| 후보 | 현재 Tier | 예상 승급 시점 | 조건 |
|---|:---:|:---:|---|
| `dashboard--bold-confident` | P3 | **2026-07** | install_hits ≥ 1 · match_hits ≥ 3 · 커뮤니티 피드백 1 건 이상 (Q2 말까지 측정 파이프라인 가동 필수) |
| `dashboard--playful-soft` | P3 | **2026-07** | 동일 조건 |
| `commerce--playful-soft` | P3 | **2026-08** | 위 + owner `@alice-external` 6 개월 마일스톤 (2026-10) 전 승격 여부 리뷰 |
| `marketing-landing--editorial-warm` | P3 | **2026-08** | 신규 (Q2 접수), 6 개월 owner 유지 후 2026-10 승격 후보 |
| `conversation-copilot--corporate-trust` | P3 | **2026-08** | 동일 |

**승급 순서 원칙**: 먼저 승격 시 `sources.json strict` gate 를 거치므로, 6 개월 내 owner handle 이 deprecation/transfer 되는 경우 우선순위 재조정. 모든 승격은 `uv run design-ontology promote-preset <id> --target P2` (dry-run 우선 → 실행) 로 수행.

## 6. 측정 파이프라인 (install_hits / match_hits) 도입 결정

Phase 15-1 에서 `presets/.metrics/` scaffold 는 완성됐지만 자동 count hook 이 미구현 — Q3 도입 여부를 이 묶음에서 결정.

### 옵션

| 옵션 | 구현 위치 | 난이도 | 성능 영향 | 개인정보 영향 |
|---|---|:---:|:---:|:---:|
| **(i) match-preset CLI 자동 카운트** | `design_ontology_harness/cli.py` match-preset handler | 낮음 | 각 CLI 호출마다 JSON append (< 1 ms) | 로컬 파일만, 외부 전송 없음 |
| **(ii) plugin `/design-start` skill 완료 시 카운트** | plugin 레포 skill 측 | 중간 | skill 종료시 1 write | plugin 사용자 로컬만, opt-in 가능 |
| **(iii) install-preset CLI 자동 카운트** | `design_ontology_harness/preset_installer.py` | 낮음 | INSTALLED.json 기록과 동시에 1 write | 로컬만 |

### 결정 (2026-04-21, Q2 리허설)

- **이 묶음 (Phase 13-11-C) 에서는 구현 보류** — 파일만 scaffold 유지.
- **Phase 16 후보** 로 승계. 이유: (i)+(iii) 조합이 자연스러우나, metric 집계 · 프라이버시 정책 · plugin-harness 간 sync 전략을 한 묶음에서 설계해야 일관됨. 13-11-C 의 scope 은 아님.
- 그 사이 공개 마켓플레이스 등록 (Phase 15 최종) 은 "metric 부재 OK" 상태에서 진행 — deprecation 로직만 zero_hits 기준을 "Q4 시작 이후 적용" 으로 늦추어 발동.

## 7. catalog-health CI 자동화 제안

현재 `uv run design-ontology catalog-health` 는 수동 실행. Q3 부터 CI 로 주 1 회 자동 실행해 drift 감지 + 분기 리포트 자동 발간 지원.

### 설계

- **파일**: `.github/workflows/catalog-health.yml` (harness 레포 측)
- **트리거**: `schedule` cron `0 9 * * 1` (월요일 09:00 UTC) + `workflow_dispatch`
- **단계**:
  1. `actions/checkout@v4`
  2. `uv sync`
  3. `uv run design-ontology catalog-health --output presets/CATALOG_HEALTH.md`
  4. `git diff --exit-code presets/CATALOG_HEALTH.md` — diff 있으면 PR 자동 생성 (아래 5), 없으면 skip
  5. `peter-evans/create-pull-request@v6` — 브랜치 `chore/catalog-health-YYYY-MM-DD`, 제목 `chore(catalog-health): weekly refresh YYYY-MM-DD`, body 에 diff summary
- **권한**: `contents: write` · `pull-requests: write`
- **실행 환경**: ubuntu-latest · Python 3.11 · `uv` 설치 step (`astral-sh/setup-uv@v5`)

### 주의

- `peter-evans/create-pull-request@v6` 의 `token` 은 기본 `GITHUB_TOKEN` 으로 충분 (자기 레포 PR 생성).
- 빈 diff 일 때 no-op 되도록 `if: always() && steps.diff.outputs.changed == 'true'` 조건 필요.
- snapshot fixture 갱신은 별도 — 이 workflow 는 `--update-snapshots` 를 호출하지 않음 (의도적).

**실행은 사용자 승인 대기** — 이번 묶음에서는 workflow 파일만 작성, push 미실행.

## 8. 2026 Q2 관찰점 (dogfood 기반)

1. **matcher keywords.json 은 실전 기여자 쿼리로 누적 튜닝이 필수** — Phase 13-11-C 에서 bob (`marketing-landing--editorial-warm`) 초기 쿼리 2/3 실패 → keywords 14 + 7 + 9 + 3 (총 33) 신규 추가로 3/3 High 회복. `publisher` / `enterprise` / `compliance` 같은 도메인 어휘가 기존 사전에 없었음.
2. **HEX 풀 소진 신호** — editorial-warm warm cream surface_tint 군 (Cornsilk/Flax/Buttercream/Naples Yellow/Blanched Almond/Peach Puff/Wheat/Creamsicle) 이 전부 사용됨. 다음 Q3 editorial-warm 신규 접수 시 **신규 color-reference.md 등록 선행 PR 유도** 필요 — CONTRIBUTING §5.1 에 이미 반영, SOP §j 시나리오 2 가 이를 다룸.
3. **동점 alphabetical tie-break 주의** — 쿼리 내 모호 키워드 (예: "editorial" 속 "editor" canvas-tool 오염, "newsletter" conversation-copilot vs marketing-landing) 상황에서 engine.py `_best()` 의 `sorted(axis_block.keys())` 는 canvas-tool/commerce 같은 사전 순 앞 쪽 app_mode 가 유리 — keywords.json 에 **phrasal disambiguator** 추가가 유일한 해결책. Q3 까지 2차 감사 (전체 4-word mixed query 50 종 실행) 검토.
4. **preview.md 대표 컴포넌트 오염** — loom preview top-3 에 broadside(magazine) / drop(commerce) 정체성 컴포넌트가 섞임. spec_analyzer UI_PATTERNS 에 "editorial newsletter landing" 추가로 해결 가능, Phase 13-11-D 또는 Q3 선순위.

## 9. 다음 분기 액션 아이템

| # | 액션 | 담당 | 목표 기한 |
|:---:|---|---|:---:|
| 1 | Phase 16 install_hits/match_hits 측정 파이프라인 구현 | harness 메인테이너 | 2026-07-15 |
| 2 | catalog-health CI workflow (월 1 회) 승인 + 활성화 | harness 메인테이너 | 2026-07-01 |
| 3 | spec_analyzer UI_PATTERNS 에 "editorial newsletter landing" 패턴 추가 (loom preview 개선) | harness 메인테이너 | 2026-07-15 |
| 4 | 첫 외부 P3 PR 1–2 건 접수 (Phase 13-11-D) — SOP 실전 검증 | 공개 홍보 · 메인테이너 | 2026-06-30 |
| 5 | Q3 catalog-health 2026Q3 리포트 (정식 첫 발간) | harness 메인테이너 | 2026-07-07 |
| 6 | P3 → P2 첫 실제 승격 (현재 5 종 중 metric 기준 충족 1–2 종) | harness 메인테이너 | 2026-08 |

---

## 부록 A. 최신 Per-Preset Metrics (2026-04-21)

현재 catalog 20 종 전체 지표는 항상 `presets/CATALOG_HEALTH.md` 에서 확인 (이 리포트 발간 시점 스냅샷):

- 전부 `install_hits=0` / `match_hits=0` / `drift=0` / `lint=OK` / `snapshot=·`.
- 따라서 per-preset table 은 `CATALOG_HEALTH.md` 를 참조 링크로 대체 (중복 발간 방지).

## 부록 B. 변경 이력

| 날짜 | 버전 | 내용 |
|------|------|------|
| 2026-04-21 | Q2 rehearsal | 초판 — Phase 13-11-C-3 리허설 발간. Q3 정식 발간 시 이 파일을 template 으로 사용. |
