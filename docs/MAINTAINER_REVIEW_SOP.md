# Maintainer Review SOP — 외부 프리셋 PR 리뷰 절차

> **범위**: 공개 플러그인 레포 (`design-ontology-plugin`) 에 도착한 신규 P3 프리셋 PR 을 접수→리뷰→머지→반영 하는 메인테이너 절차.
> **대상 독자**: design-ontology-harness / design-ontology-plugin 메인테이너.
> **언어**: 한국어 primary + 영문 mirror (섹션 말미).
> **기반 문서**: [`CONTRIBUTING_PRESETS.md`](./CONTRIBUTING_PRESETS.md) (기여자 관점) · [`PLUGIN_PLAN.md`](./PLUGIN_PLAN.md) §11 라이프사이클 · [`PLUGIN_LOCAL_DEV.md`](./PLUGIN_LOCAL_DEV.md) (로컬 sync).
> **전제**: GitHub Actions `validate.yml` + `community-preset-check` 2 job 통과를 확인한 뒤 사람 리뷰에 진입한다.

---

## 0. 전체 흐름 요약 (≈ 21 분)

```
PR 도착
 ├─ a. 자동 체크 확인             (30 초)
 ├─ b. 기여자 프로필 확인          (2 분)
 ├─ c. 브랜드 IP 스팟체크          (5 분)
 ├─ d. HEX + 셀 중복 수동 검증     (3 분)
 ├─ e. preview.md + Style Capsule 확인 (3 분)
 ├─ f. self-match cross-validate  (2 분)
 ├─ g. 소스 디렉토리 구조 확인     (1 분)
 ├─ h. 병합 + rebuild + matrix    (5 분)
 ├─ i. owner 등록 통지             (1 분)
 └─ j. 실패 시 복구                (시나리오별)
```

**총 예상 시간: 22 분 / PR** — 실측치는 Phase 13-11-C-2 dogfood 결과로 갱신 (§11).

---

## 1. 단계별 절차

### a. PR 접수 직후 자동 체크 확인 (≤ 30초)

```bash
gh pr view <PR#> --repo 2000silpeed/design-ontology-plugin --json statusCheckRollup
```

**체크리스트**

- [ ] `validate-presets` job green — plugin 매니페스트 + preset_api_version range + skills/agents 파리티
- [ ] `community-preset-check` job green — harness `scripts/validate-community-preset.py` errors=0
- [ ] PR 본문 `validate-community-preset.py` 출력 붙여넣기 존재 (warnings 있으면 사유 기재)
- [ ] PR 제목 `feat(preset): <app_mode>--<brand_tone>` 또는 그에 준하는 한글 제목

**실패 시** → §j 시나리오 1 (workflow 실패).

### b. 기여자 프로필 간이 확인 (≤ 2분)

- [ ] GitHub handle 유효 (`@<handle>` 이 실제 계정, 프로필에 활동 이력)
- [ ] 이전 contribution 이력 확인 — 같은 조직 내 기존 PR, design-ontology 관련 이슈 댓글 활동
- [ ] PR 템플릿 "Owner 책임 확인" 4 체크박스 전부 체크됨 (6 개월 유지 / 2주 이내 피드백 / minor bump 대응 / snapshot 대응)
- [ ] 의심 신호 없음 — bot 계정·스팸·fork spam 아님

**실패 시** → PR 에 댓글로 "owner 책임 체크리스트 빠진 항목 보완 부탁드립니다" 남기고 대기.

### c. 브랜드 IP 스팟체크 (≤ 5분)

`projects/<source-project>/brand_profile.json.seeds` + `presets/<id>/sources.json.seeds` 3–6 개 URL 열어보기.

- [ ] 시드 URL 3 개 이상이 실제 public 레퍼런스 (sign-in wall, 비공개 Figma 없음)
- [ ] 로고·마크·캐릭터 자산이 프리셋에 포함되지 않음 (`grep -rnE '\.svg$|logo|trademark' presets/<id>/`)
- [ ] 경쟁사 팔레트 직접 복제 없음 — Core HEX 3 종이 시드 브랜드의 **공식 가이드 HEX 와 일치하지 않음** (영감은 OK, pixel-perfect copy 는 NG)
- [ ] brand_profile.json 의 `brand_name` 이 실재하는 타사 브랜드명과 동일하지 않음 (가상·조어 권장)

**실패 시** → §j 시나리오 4 (브랜드 IP 의심).

### d. HEX + 셀 중복 수동 검증 (≤ 3분)

```bash
# 전체 카탈로그 Core HEX 일람
for p in presets/*/; do
  id=$(basename "$p")
  [[ "$id" == *.* ]] && continue
  [ -f "$p/preview.md" ] || continue
  echo "=== $id ==="
  awk '/^### Core/{flag=1;next} /^### /{flag=0} flag' "$p/preview.md" | \
    grep -E "^\s*-\s*(primary|accent|surface_tint)" || true
done

# 신규 프리셋 vs 동일 brand_tone 군 상세 비교
python3 scripts/validate-community-preset.py --preset-id <new-id>
```

**판정**
- [ ] primary · accent · surface_tint 3 role 중 기존 프리셋과 **2 개 이상 동일 HEX** → warning/reject 판단 (동일 brand_tone 군 내라면 특히 엄격)
- [ ] 1 개 겹침은 통과 (warning 만) — PR 본문 사유 기재 여부 확인
- [ ] `{app_mode, brand_tone}` 셀 중복 없음 — 중복이면 태그로 확연히 차별화된 서브도메인이어야 P3 수락 가능

**실패 시** → §j 시나리오 2 (HEX 2 개 이상 겹침) — 기여자에게 팔레트 조정 요청.

### e. preview.md + Style Capsule 렌더 육안 확인 (≤ 3분)

`gh pr view <PR#> --web` 또는 로컬 체크아웃에서 `less presets/<id>/preview.md` 로 5 섹션 육안 확인:

- [ ] `## 어떤 제품에 맞나` — 제품 적합성 한 문단 + bullet 3–5 개
- [ ] `## Color Tokens (light)` / `## Color Tokens (dark)` (color_mode 지원 시) — HEX 스와치 ≥ 7 개 (Core 3 + Semantic 4)
- [ ] `## Typography` — heading/body/mono/korean 서체 명시 + locale_pairings 노트
- [ ] `## 대표 컴포넌트` — 3 개, parts + states 기록
- [ ] `## 주의사항` — 이 프리셋과 맞지 않는 경우 + 대안 프리셋 링크

**실패 시** → PR 댓글로 "preview.md 의 `<섹션>` 이 비어있습니다. `uv run design-ontology lint-previews --preset-id <id>` 통과시켜 주세요" 요청.

추가로 `less presets/<id>/STYLE.md` 또는 `less presets/<id>/DESIGN.md` 로 스타일 캡슐을 확인합니다.

- [ ] `Authority Order`가 존재하고 external visual references가 마지막 순서
- [ ] `Color Roles`에 `--ds-color-*` 토큰이 포함됨
- [ ] `Reference Governance`에 allowed/denied absorption scope가 포함됨
- [ ] `Token binding is necessary but not sufficient` 문구가 포함됨
- [ ] `Agent Preflight`에 `lint-implementation` 명령이 포함됨

**실패 시** → `build-preset` 재실행 또는 `style_capsule.py` 렌더러 수정 요청. `STYLE.md`만 수동 수정하지 않습니다.

### f. self-match Top-1 복수 쿼리 cross-validate (≤ 2분)

기여자가 제출한 쿼리 1 개 + 메인테이너가 즉석 작성하는 1–2 개를 교차로 실행.

```bash
# 기여자 쿼리
uv run design-ontology match-preset --free-text "<contributor query>"

# 메인테이너 즉석 쿼리 2 개 (app_mode 키워드 + brand_tone 키워드 조합)
uv run design-ontology match-preset --free-text "<maintainer query 1>"
uv run design-ontology match-preset --free-text "<maintainer query 2>"

# 축 기반 직접 확인
uv run design-ontology match-preset \
  --app-mode <app_mode> --brand-tone <brand_tone> --top 3
```

- [ ] 3 개 쿼리 전부에서 **Top-1 이 신규 프리셋** (bucket 은 High 이상)
- [ ] 기존 프리셋 대조군 (가까운 셀 2–3 개 — 같은 app_mode 다른 tone · 같은 tone 다른 app_mode) 에 회귀 없음

**실패 시** → §j 시나리오 3 (self-match 실패). 기여자에게 "자연어 쿼리를 기여자 수정 → 재검증" 요청하거나, matcher keywords 보강이 필요한 경우 별도 maintainer PR 로 분리.

### g. 소스 디렉토리 구조 확인 (≤ 1분)

```bash
ls projects/<source-project>/
wc -l projects/<source-project>/spec.md
jq '.palette_roles // {}' projects/<source-project>/brand_profile.json
uv run design-ontology sync-semantic-colors \
  --source ../semantic-os/domains/color/ontology/build/graph.json \
  --color-reference-output docs/color-reference.md \
  --ontology-output design_ontology_harness/resources/semantic_color_ontology.json \
  --check
```

- [ ] `projects/<source-project>/` 에 `brand_profile.json` + `spec.md` + (선택) `locale_pairings.json` + `project_manifest.json` 모두 존재
- [ ] `spec.md` ≥ 150 라인 (너무 얇으면 component 추출이 부실 — 현재 P3 선례 평균 170–185 라인)
- [ ] `sync-semantic-colors --check` 통과: `docs/color-reference.md`의 embedded graph·checksum이 source graph와 일치하고, 보이는 색상 카드는 동기화 과정에서 그대로 보존됨
- [ ] `brand_profile.color_reference.palette_roles.{primary,accent,surface_tint}`의 이름이 보이는 카드 + embedded `ColorKeyword` 이름 공간에서 해석됨 (case-insensitive)
- [ ] Semantic OS에 없는 색은 출처·사용 범위가 기록된 Markdown-only 로컬 확장으로 표시됨
- [ ] `brand_profile.seeds` ≥ 3 개의 URL — `sources.json.seeds` 와 일치

**실패 시** → palette role 오타는 기여자 수정을 요청하고, graph/checksum drift는 메인테이너가 `sync-semantic-colors`로 재생성한 별도 PR에서 해결.

### h. 병합 후 rebuild + matrix sync (≤ 5분)

**병합 직후 메인테이너 로컬에서 수행** (harness 레포).

```bash
# 1) harness main 을 최신으로
git checkout main && git pull

# 2) 전체 재빌드 (새 프리셋 포함)
uv run design-ontology rebuild-all-presets --projects-root projects

# 3) 소스 재생성
uv run design-ontology build-sources --all --force

# 4) 전체 검증
uv run design-ontology validate-presets
uv run design-ontology lint-previews
uv run --with pytest pytest tests/ -v

# 5) eval-matcher 회귀 확인 (≥ 0.85)
uv run design-ontology eval-matcher

# 6) catalog-health 갱신 → commit 에 포함
uv run design-ontology catalog-health

# 7) snapshot fixture 갱신 (새 preset content_hash 추가)
uv run --with pytest pytest tests/test_preset_snapshots.py --update-snapshots

# 8) plugin 레포 CATALOG.md 재생성
PLUGIN_REPO=${PLUGIN_REPO:-../design-ontology-plugin}
python3 scripts/build-catalog.py \
  --output "$PLUGIN_REPO/docs/CATALOG.md"

# 9) plugin 레포 compatibility 재확인
python3 scripts/check-plugin-compatibility.py \
  --plugin-repo "$PLUGIN_REPO"
```

- [ ] rebuild-all N/N OK
- [ ] build-sources N/N OK (warn 0)
- [ ] validate-presets + lint-previews 모두 pass
- [ ] tests 전체 pass (신규 프리셋으로 라벨 +4 추가되면 카운트 상승 정상)
- [ ] eval-matcher accuracy ≥ 0.85 (자동 게이트)
- [ ] catalog-health 에 신규 프리셋 + coverage % 반영
- [ ] snapshot fixture 갱신 후 `tests/test_preset_snapshots.py` pass
- [ ] plugin `docs/CATALOG.md` diff 확인 → 커밋 가능 상태

**실패 시** → §j 시나리오 5 (머지 후 회귀).

### i. Owner 등록 통지 (≤ 1분)

**현재 정책 (2026-04-21)**: manifest.generated_at 을 `owner_since` 근사치로 사용.
PR 본문에 **머지된 ISO 날짜를 댓글로 기록** — 6 개월 재평가 타이머 시작점.

```markdown
@<handle> 머지 완료 — 2026-04-21 기준 owner 6 개월 유지 기간 시작.
재평가 예정일: 2026-10-21. 그 사이 piece-specific 이슈가 뜨면 2 주 이내 반응 부탁드립니다.
```

- [ ] PR 에 머지 날짜 + 재평가 예정일 댓글 등록
- [ ] 메인테이너 전용 트래커 (추후 `docs/OWNER_TRACKER.md` 또는 GitHub Project) 에 entry 추가 (Phase 15 후속)

> **1급 필드 승격 여부**: `owner_since` 를 `manifest.json` 에 optional 필드로 추가하는 안은 §13 에서 roadmap 에 등록. 현재는 `generated_at` 근사로 충분 (오차 ≤ 1 주) + PR 본문 댓글로 보완.

### j. 실패 시 복구 시나리오

#### 시나리오 1 — GitHub Actions workflow 실패

- `validate-presets` job 실패 → manifest.json 구조 에러. `uv run design-ontology validate-presets` 로 로컬 재현 → 기여자에게 에러 메시지 그대로 전달.
- `community-preset-check` job 실패 → HEX/cell/self-match 중 하나. workflow log 의 `::group::<preset_id>` 안쪽 exit code 확인 → 기여자에게 구체적 수정 지시.
- harness 레포 경로 404 (checkout 실패) → `.github/workflows/validate.yml` 의 `HARNESS_REPO` vars 확인. 메인테이너 조치 필요.

#### 시나리오 2 — HEX 2 개 이상 겹침

기여자에게 댓글:
```
HEX 겹침 {N} 개 감지 (details: primary=<hex> same as <preset-id>, accent=<hex> same as <preset-id>).
docs/color-reference.md 에서 동일 `brand_tone` 군에서 아직 안 쓴 색을 골라 palette_roles 를 조정하거나,
공용 신규 색이 필요하면 Semantic OS graph에 `ColorKeyword`를 먼저 반영한 뒤 `sync-semantic-colors`로 동기화해 주세요.
프로젝트 전용 색은 출처와 사용 범위를 밝힌 Markdown-only 로컬 확장으로 분리해야 합니다.
참고: 동일 brand_tone 군 내 0–1 겹침이 권장.
```
→ 기여자 수정 PR 푸시 → §a 부터 다시.

#### 시나리오 3 — self-match Top-1 실패

- matcher 가 기여자 프리셋을 Top-1 으로 잡지 못함 → 1 순위: 쿼리 표현 개선 (다른 톤의 키워드 `warm`/`bold`/`minimal` 와 충돌 회피) 을 기여자에게 요청.
- 쿼리 개선으로도 통과 안 하면 → matcher `keywords.json` 보강 필요. 메인테이너가 **별도 PR** 로 keyword 추가, 기여자 PR 은 그 뒤에 rebase.

#### 시나리오 4 — 브랜드 IP 의심

- 시드 URL 이 sign-in wall / 비공개 자료로 의심 → 기여자에게 다른 공개 레퍼런스로 교체 요청.
- Core HEX 가 실재 브랜드의 공식 HEX 와 pixel-perfect 일치 → 팔레트 조정 요청. 필요 시 CoC 섹션 9.1 상기.
- 로고·마크 파일이 preset 디렉토리에 포함 → 즉시 PR close + `rm` 후 재제출 요청.

#### 시나리오 5 — 머지 후 회귀

- `rebuild-all-presets` 실패 → 기여자의 `brand_profile.json` 에 필수 필드 누락일 가능성. 로컬에서 `uv run design-ontology run-project --project-dir projects/<name>` 로 재현 후 hotfix PR.
- `eval-matcher` accuracy < 0.85 → 신규 라벨이 기존 프리셋을 오분류시켰을 가능성. `--verbose` 실행으로 confusion pair 확인 → keywords 조정 hotfix.
- `test_preset_snapshots.py` drift → 의도적이면 `--update-snapshots` 로 갱신, 의도적이 아니면 빌드 로직 확인.
- 어느 경우든 **main 브랜치 revert 보다 hotfix PR** 우선 (rebuild 실패가 기여자 귀책이 아닐 수 있음).

---

## 2. 두 기여자 PR 동시 접수 시 처리 순서

**케이스**: Phase 13-11-C-2 dogfood 처럼 2–3 시간 간격으로 2 PR 도착.

1. **두 PR 각각 §a–g 독립 리뷰** — 서로 머지 순서에 의존하지 않도록.
2. **먼저 머지한 PR 이 §h 를 완주** — 반드시 catalog-health + snapshot fixture + plugin CATALOG.md 까지.
3. **두 번째 PR rebase** on main → 기여자가 본인 브랜치 `git rebase origin/main` 수행 (matrix.json + snapshot fixture 충돌 가능) → conflict 해결 → force-push.
4. **두 번째 PR 도 §h 완주** — rebuild-all 에 양쪽 프리셋 전부 포함.
5. **하나의 분기 catalog-health 리포트 섹션에 두 프리셋 기록** — `docs/CATALOG_HEALTH_YYYYQn.md` 신규 승급/접수 항목에 동시 등재.

**matrix.json merge conflict 대응**
- 같은 배열에 다른 entry 추가 형태면 Git 자동 머지 실패 → 둘 다 keep 하는 쪽으로 수동 해결.
- `snapshot_fixture` (JSON dict) 는 두 entry 모두 keep.
- `plugin/docs/CATALOG.md` 는 auto-generated → 두 번째 PR 에서 재실행하여 덮어쓰기.

---

## 3. 리뷰 시 경계해야 할 패턴 (체크리스트 초과 신호)

다음 신호 중 2 개 이상이면 **P3 수락 보류** + 별도 discussion issue 로 전환:

- 시드가 모두 한 조직/기업 내부 자료 (예: 전부 한 회사의 브랜드 가이드 페이지)
- palette_roles가 기여자 본인이 추가한 로컬 확장에만 근거하면서 출처·사용 범위가 없음 (self-referential 팔레트, 검증 곤란)
- preset_id 의 `brand_tone` 선택이 시드 브랜드의 실제 톤과 크게 다름 (ex. Stripe 시드로 playful-soft 주장)
- spec.md 내용이 일반론 복붙 수준이고 도메인 특화 컴포넌트 1–2 개밖에 없음
- PR 본문 self-match 출력 bucket 이 Medium 이하로 제출됨

---

## 4. 메인테이너 편의 스크립트 (향후 로드맵)

Phase 13-11-D 이후 도입 후보 — 현재는 수동 절차.

| 이름 | 목적 | 우선순위 |
|------|------|---------|
| `scripts/review-pr.sh <PR#>` | §a–g 를 한 번에 돌리고 체크리스트 Markdown 출력 | P1 |
| `scripts/owner-tracker.py` | 머지된 PR 의 owner_since + 재평가 예정일 추적 | P1 |
| `manifest.owner_since` 필드 | 1급 필드 승격 — schema 1.0.1 minor bump | P2 |
| `scripts/post-merge-sync.sh` | §h 의 9 단계를 한 번에 실행 + diff summary | P2 |

---

## 5. English Mirror — Key Sections

### Flow summary

```
PR arrives → (a) automated checks green → (b) contributor profile sanity
→ (c) brand IP spot-check → (d) HEX/cell overlap → (e) preview.md + Style Capsule eyeballing
→ (f) self-match cross-validate → (g) source project layout → (h) merge + rebuild
→ (i) owner notification → (j) recovery playbook if anything failed
```

Total ≈ 22 minutes per PR; actual dogfood numbers live in §11.

### Merge → rebuild sequence (maintainer local, harness repo)

1. `rebuild-all-presets --projects-root projects`
2. `build-sources --all --force`
3. `validate-presets` + `lint-previews`
4. `pytest tests/ -v`
5. `eval-matcher` (threshold 0.85)
6. `catalog-health`
7. `pytest tests/test_preset_snapshots.py --update-snapshots`
8. `scripts/build-catalog.py --output <plugin>/docs/CATALOG.md`
9. `scripts/check-plugin-compatibility.py --plugin-repo <plugin>`

### Failure playbook (quick ref)

- Workflow fails → reproduce locally with the same command, tell the contributor.
- HEX ≥ 2 overlap → ask for palette rework; shared colors go upstream to Semantic OS and are synced, while project-only colors require an explicit Markdown-only extension with provenance.
- self-match fails → try query rewording; if still failing, open a maintainer PR for `keywords.json`.
- Brand IP doubt → request public seeds, reject pixel-perfect palette copies.
- Post-merge regression → hotfix PR over revert (contributor may not be at fault).

---

## 11. 실측 시간 데이터 (Phase 13-11-C-2 dogfood)

Phase 13-11-C-2 에서 가상 기여자 2 명 (`@bob-external` marketing-landing--editorial-warm + `@carol-external` conversation-copilot--corporate-trust) PR 을 assume 하여 SOP 를 2 회 적용한 실측치.

| 단계 | 예상 | 실측 bob | 실측 carol | 메모 |
|------|-----:|---------:|-----------:|------|
| a. 자동 체크 | 30 s | 25 s | 30 s | workflow log UI 에서 2 job 확인 |
| b. 기여자 프로필 | 2 m | 1.5 m | 1.5 m | new handle 은 프로필 링크 + PR 본문 기록으로 충분 |
| c. 브랜드 IP | 5 m | 4 m | 6 m | carol 은 enterprise chatbot 레퍼런스 검증에 1 분 추가 |
| d. HEX + 셀 | 3 m | 4 m | 5 m | carol 은 신규 color 등록 PR 선행 필요 판단 1 분 추가, bob 은 wheat 1 겹침 warning 사유 검토 |
| e. preview.md + Style Capsule | 3 m | 2 m | 2 m | 기존 dogfood는 5 섹션 검사 기준, Style Capsule 추가 후 +1 m 예상 |
| f. self-match | 2 m | 2 m | 3 m | carol 은 `corporate ai chatbot enterprise trust` 쿼리에 keywords tie-break 확인 |
| g. 소스 구조 | 1 m | 1 m | 1 m | loom/mercer 모두 scaffold 표준 |
| h. rebuild + sync | 5 m | 5.5 m | 5.5 m | rebuild-all 20/20 + eval 66/66 + snapshot update |
| i. owner 통지 | 1 m | 1 m | 1 m | 재평가일 2026-10-21 동일 |
| **총합** | **22 m** | **~21 m** | **~25 m** | carol 은 신규 color 등록으로 +4 m |

**관찰점 (Phase 13-11-C-2 실측)**
1. **HEX 1 겹침 warning** 은 판단 시간 1 분 이내 — 동일 brand_tone 군 내가 아니면 warning 사유 기재만 요구하면 충분.
   - bob (Wheat #F5DEB3 ↔ signal-desk 겹침): editorial-warm 4 종 중 cream-paper 공통 톤 공유, primary/accent 차별화로 통과
   - carol (Powder Blue #B0E0E6 ↔ beacon 겹침): marketing-landing/minimal-tech ↔ conversation-copilot/corporate-trust 의 app_mode+tone 축 둘 다 다름 → 셀 혼동 위험 없음
2. **self-match cross-validate 3 쿼리 중 2개 실패 → keywords.json hotfix 필요** (§j 시나리오 3 실전 적용):
   - bob 기여자 쿼리 "독립 뉴스레터 editorial 랜딩 퍼블리셔 warm" 초기 Top-1 = canvas-tool [Low] (editor substring + 동점 alphabetical tie-break)
   - 해결: `keywords.json` marketing-landing 에 "퍼블리셔 / publisher / 뉴스레터 랜딩 / publisher landing / subscribe landing" 등 14 개 신규 키워드 추가 + conversation-copilot 에 엔터프라이즈/regulatory chatbot 7 개 + corporate-trust 에 enterprise/compliance 9 개 + tags 에 publisher/enterprise/compliance 3 개 신규.
   - 보강 후 bob 3/3 Top-1 High, carol 3/3 Top-1 High.
3. **preview.md 대표 컴포넌트 오염** (§e) — bob preview 의 대표 컴포넌트 top-3 에 `cover-story`(broadside magazine) · `drop-banner`(commerce drop) 가 섞여 들어감. marketing-landing 정체성이 약하게 잡힘 — spec_analyzer UI_PATTERNS 에 "editorial newsletter landing" 패턴 추가로 해결 가능하나 이번 묶음에서는 보류 (preview 3 개 중 1 개는 hero-cta-group 으로 정체성은 유지).
4. **2 PR 동시 접수 시나리오**: dry-run 으로 bob 먼저 처리 → carol rebase 시뮬레이션. matrix.json 은 `_upsert_matrix_entry` 가 자동으로 2 entry 모두 keep 으로 머지 → 수동 conflict 해결 불필요. snapshot fixture 도 update-snapshots 로 일괄 갱신.
5. **post-merge §h 9 단계 실측**: rebuild-all 20/20 OK · build-sources 20/20 OK (warn 0) · validate 20/20 · lint 20/20 · tests **189 → 197 passed** (+8) · eval-matcher **1.00 (58/58 → 66/66)** · catalog-health **18 → 20** 종 / 45% → 50% coverage / deprecated 0 / prune_eligible 0 · snapshot regression 0 · plugin CATALOG.md auto-regenerated (20 presets, P3 · 5 section).

---

## 12. 변경 이력

| 날짜 | 버전 | 내용 |
|------|------|------|
| 2026-04-21 | 1.0 | 초판 — Phase 13-11-C-1 에서 SOP 10 단계 + 실패 시나리오 5 종 + English mirror 작성. Phase 13-11-C-2 dogfood 2 PR 실측치 §11 에 병기. |

---

**유지 책임**: harness/plugin 양 레포 메인테이너. 절차가 바뀌면 이 문서 먼저 업데이트 → `docs/CONTRIBUTING_PRESETS.md` 의 §6 승급 조건과 단면 확인.
