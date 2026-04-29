# Plugin 프리셋화 — 태스크 리스트 (v2)

> 기반 설계서: [`PLUGIN_PLAN.md`](./PLUGIN_PLAN.md) v2
> 관련: [`../TASK.md`](../TASK.md) (Phase 1~6 완료 전제)
> v2 변경: 코덱스 리뷰 전면 반영 (버전 계약 Phase 7로 승격, MVP 축소, 축 재설계, 프리뷰 격하)

---

## Phase 7: 프리셋 인프라 + 버전 계약 (harness 레포)

- [x] **7-1. 프리셋 매트릭스 스키마 정의 (v2 축 체계)**
  - 신규: `schemas/preset_matrix.schema.json`
  - 필드:
    - `app_modes[]` (8종)
    - `brand_tones[]` (5종)
    - `color_modes[]` (`light`, `dark`, `both`)
    - `presets[]`
  - 각 프리셋: `id`, `app_mode`, `brand_tone`, `color_modes[]`, `default_color_mode`, `tags[]`, `description`, `source_project`, `owner`, `preview_path`, `locale_pairings`, `tier`
  - id 규칙 검증: `{app_mode}--{brand_tone}` (JSON Schema pattern)
  - `default_color_mode`는 `color_modes`에 포함되어야 함 (conditional validation)

- [x] **7-2. 프리셋 `manifest.json` 버전 계약 1급 필드**
  - 신규 필드 (매니페스트 필수):
    - `schema_version` (산출물 내부 스키마)
    - `preset_api_version` (플러그인 소비 계약)
    - `generated_by_harness_version` (생성 시점 코어 버전)
    - `preview_version` (프리뷰 아티팩트 포맷)
    - `adapter_compatibility` (어댑터별 지원 semver range)
    - `content_hash` (sha256)
  - 신규: `presets/compatibility.json` — preset_api_version ↔ adapter 매트릭스

- [x] **7-3. 축 정의 확정 기록**
  - 신규: `presets/matrix.json` 초기 파일 (빈 presets, 축만)
  - 신규: `docs/PRESET_AXES.md` — app_mode 8종 / tone 5종 / tags 정책 근거

- [x] **7-4. 자연어 → 축·태그 매핑 사전**
  - 신규: `design_ontology_harness/preset_matcher/keywords.json`
  - 한국어/영어 → `app_mode` / `brand_tone` / `color_mode` / `tags`
  - 동의어, 반대어 포함

- [x] **7-5. 프리셋 빌드 스크립트**
  - 신규: `design_ontology_harness/preset_builder.py`
  - 입력: `projects/<name>/` + preset-id + app_mode/tone/color_modes/tags 지정
  - 동작:
    1. `build/system/` → `presets/<preset-id>/` 복사
    2. `manifest.json` 생성 (7-2 필드 전부)
    3. `preview.md` 텍스트 프리뷰 자동 생성 (색상 스와치 / 서체 / 대표 컴포넌트 3개 / 주의사항)
    4. `content_hash` 계산
  - CLI: `uv run design-ontology build-preset --project signal-desk --preset-id document-content--editorial-warm`

- [x] **7-6. 프리셋 검증기 (버전 계약 포함)**
  - 신규: `design_ontology_harness/preset_validator.py`
  - 체크:
    - 필수 파일, token_schema JSON schema
    - id 규칙 (`{app_mode}--{brand_tone}`)
    - manifest 4개 버전 필드 존재 + semver 유효성
    - `preset_api_version`이 현재 supported range 내인지
    - `adapter_compatibility`가 존재하는 어댑터를 참조하는지
    - matrix.json ↔ 실제 presets/ 일치
  - CLI: `uv run design-ontology validate-presets`

- [x] **7-7. Sync-time 호환성 Validator**
  - 신규: `scripts/check-plugin-compatibility.py`
  - 입력: harness presets/ + 대상 plugin 레포 경로
  - 동작:
    1. plugin 레포 `plugin.json`에서 지원 `preset_api_version` 범위 파싱
    2. harness 프리셋 각각의 version 필드와 비교
    3. 불일치 시 PR 생성 거부, 리포트 출력
  - `scripts/sync-plugin-presets.sh`에서 선행 호출

- [x] **7-8. 전체 재빌드 명령**
  - CLI: `uv run design-ontology rebuild-all-presets`
  - matrix.json 순회 → source_project 기반 재빌드
  - 실패 리포트 집약 출력

- [x] **7-9. `pyproject.toml` / `.gitignore` 업데이트**
  - `presets/`는 리포에 포함 (기존 `.gitignore`에서 제외되지 않음 확인)
  - `[tool.hatch.build]` include에 schemas/, presets/, scripts/, docs/ 추가
  - CLI 서브커맨드: `build-preset`, `validate-presets`, `rebuild-all-presets` 추가
  - `render-previews`는 Phase 12A에서 추가 예정

---

## Phase 8: P0 5종 프리셋 승격 + 텍스트 프리뷰

새 축 체계(v2)로 매핑. color_mode는 대부분 `["light","dark"]` 기본.

- [ ] **8-1. signal-desk → `document-content--editorial-warm`**
  - tags: `["reading-heavy","ko"]`
  - locale_pairings.ko: Pretendard + Lora
  - color_modes: `["light","dark"]`, default: `light`

- [ ] **8-2. colorfit → `commerce--editorial-warm`**
  - tags: `["fashion","mobile-first","ko"]`
  - mobile-web 제약 preview에 명시
  - color_modes: `["light"]`, default: `light`

- [ ] **8-3. premier-league → `marketing-landing--bold-confident`**
  - tags: `["sports"]`
  - 랜딩 중심 component 필터링
  - color_modes: `["light","dark"]`

- [ ] **8-4. glacier → `conversation-copilot--minimal-tech`**
  - tags: `["ai","ko"]`
  - color_modes: `["light","dark"]`

- [ ] **8-5. 신규 P0: `dashboard--minimal-tech`**
  - 새 프로젝트 `orbit` 생성
  - 키워드: clean, precise, neutral, technical
  - 시드: Linear, Height, Notion
  - tags: `["saas","ko"]`
  - locale_pairings.ko: Pretendard

- [ ] **8-6. P0 5종 텍스트 `preview.md` 작성**
  - 템플릿: 어떤 제품에 맞나 / Color Tokens(light+dark) / Typography / 대표 컴포넌트 / 주의사항
  - PLAN §9.3 템플릿 준수

- [ ] **8-7. P0 5종 owner 지정**
  - `manifest.json`의 `owner` 필드 기본값 = 메인테이너

---

## Phase 9: 플러그인 레포 분리 + 뼈대

> 상태: 로컬 scaffold 완료 (2026-04-18). GitHub 공개 레포 생성/푸시는 사용자 승인 대기.

- [x] **9-1. 신규 레포 `design-ontology-plugin` 생성**
  - 로컬 경로 예시: `../design-ontology-plugin/`
  - MIT + SIL OFL(폰트) 라이선스
  - 초기 구조: `.claude-plugin/`, `skills/`, `agents/`, `presets/`, `adapters/{base,nextjs-tailwind-shadcn}/`, `scripts/`, `docs/`, `.github/workflows/`, `README.md`, `LICENSE`, `LICENSE-FONTS`, `.gitignore`
  - 지원 `preset_api_version` range를 `plugin.json`에 기록 (`>=1.0.0 <2.0.0`)

- [x] **9-2. `.claude-plugin/` manifest**
  - `plugin.json`: name=`design-ontology`, version=`0.1.0`, skills/agents 경로, `supported_preset_api: ">=1.0.0 <2.0.0"`, presets root, adapter default
  - `marketplace.json`: 공개 마켓플레이스 엔트리 (status=pre-alpha, categories/keywords)

- [x] **9-3. 기존 스킬 4종 이식**
  - `skills/design-system-{architect,implement,refactor,rebuild}/SKILL.md`
  - 수정: 각 스킬 맨 앞에 **Step 0 — 프리셋 계약 확인** 섹션 추가. `design-system/INSTALLED.json` + `design-system/manifest.json` 읽고 `preset_api_version` ↔ 플러그인 `supported_preset_api` 일치 확인 후에만 진행

- [x] **9-4. 에이전트 4종 이식**
  - `agents/design-system-{architect,implementer,refactor,rebuild}.md`
  - 프롬프트 상단에 "Preset contract check" 섹션 추가: `INSTALLED.json`/`manifest.json` 읽기, `preset_api_version` 검증, 불일치 시 즉시 중단

- [x] **9-5. 프리셋 sync 스크립트 (harness → plugin)**
  - 기존: `scripts/sync-plugin-presets.sh` (Phase 7-7 산출물)
  - 드라이런 리허설 검증: `./scripts/sync-plugin-presets.sh --plugin-repo ../design-ontology-plugin --dry-run` → `compatibility OK (5 preset manifests)` 통과

- [x] **9-6. harness CI sync 훅**
  - `.github/workflows/sync-plugin.yml`
  - `main` push 또는 수동 실행 시: 플러그인 레포 clone → `check-plugin-compatibility.py` 게이트 → 통과하면 `scripts/sync-plugin-presets.sh` 실행 → PR 생성 (gh 필요)
  - 필요 시크릿: `PLUGIN_REPO_TOKEN` (미구성 시 compatibility check만 수행하고 sync 단계 skip)
  - 필요 변수: `PLUGIN_REPO` (기본: `2000silpeed/design-ontology-plugin`)

- [x] **9-7. plugin 레포 자체 validator**
  - `design-ontology-plugin/.github/workflows/validate.yml`
  - PR/push 시: `.claude-plugin/` 매니페스트 존재, `supported_preset_api` 필드 확인, 모든 preset `preset_api_version`이 supported range 내인지 **2차 검증**, `skills/*/SKILL.md` 존재 여부

- [x] **9-8. 로컬 설치 가이드**
  - 신규: `docs/PLUGIN_LOCAL_DEV.md` (harness 쪽)
  - 미러: `design-ontology-plugin/docs/LOCAL_DEV.md`

---

## Phase 10: 스택 어댑터 (분할, MVP는 10A만)

### Phase 10A — MVP 필수 (alpha 전)

- [ ] **10A-1. 어댑터 베이스 인터페이스**
  - 신규: `design_ontology_harness/adapters/base.py`
  - 추상 `StackAdapter`: `detect()`, `render()`, `merge()`, `supported_preset_api`
  - 공통 유틸: tokens → CSS custom properties 변환기, 폰트 페어링 주입기

- [ ] **10A-2. `nextjs-tailwind-shadcn` 어댑터**
  - 출력:
    - `tailwind.config.ts` theme.extend
    - `app/globals.css` CSS 변수 + `[data-theme='dark']` (프리셋 color_modes에 `dark` 포함 시)
    - `components.json` shadcn 토큰 매핑
    - `design-system/` 복사
    - (ko) `public/fonts/PretendardVariable.woff2` + `@font-face`
  - 병합 로직: 기존 config 감지 시 extend
  - 충돌 시 `.ds-proposed`

- [ ] **10A-3. 한글 로케일 주입기**
  - `--locale ko`
  - Pretendard 자산 복사 + `@font-face` + `font-family` 등록

- [ ] **10A-4. 어댑터 자동 감지**
  - target_repo의 `package.json`, `tailwind.config.*`, `components.json`으로 적합도 계산

- [ ] **10A-5. MVP 어댑터 테스트**
  - 신규: `tests/test_adapter_nextjs_shadcn.py`
  - P0 5종 × light/dark round-trip
  - Tailwind config parse 검증, CSS 문법 검증

### Phase 10B — alpha 후

- [x] **10B-1. `raw-css-variables` 어댑터**
  - 출력: `design-system/tokens.css` (`:root` + `[data-theme='dark']` + `@media prefers-color-scheme`) / `design-system/fonts.css` (ko) / Pretendard 스캐폴드 3종 / `design-system/README.md` / preset mirror
  - 프레임워크 무관. user repo 최상위 절대 기록 안 함
  - 공통화: `design_system_mirror_ops()` 를 `adapters/base.py` 로 승격 (Next 어댑터도 동일 헬퍼 사용)

- [x] **10B-2. 10B 테스트**
  - `tests/test_adapter_raw_css.py` 14 케이스 (registry / compat / P0×mode round-trip / ko+non-ko locale / detect / merge idempotent + fallback)
  - 전체 66 passed (기존 52 + 신규 14)

### Phase 10C — 수요 검증 후

- [ ] **10C-1. `vite-tailwind` 어댑터**
  - 출력: `tailwind.config.ts` + `src/index.css`

- [ ] **10C-2. 10C 테스트**

---

## Phase 11: `/design-start` UX (MVP 핵심)

- [x] **11-1. 매칭 스킬 `design-start`**
  - 신규: `plugin/skills/design-start/SKILL.md`
  - 4단계 질문 플로우 (PLAN §5.1):
    1. app_mode 선택
    2. brand_tone 선택
    3. color_mode 선택
    4. 스택 선택 (MVP는 Next+shadcn만 가용)
    5. 한글 locale 확인
  - 자연어 fallback (PLAN §5.2)

- [x] **11-2. 매칭 엔진 (coarse bucket)**
  - 신규: `design_ontology_harness/preset_matcher/engine.py`
  - raw_score 계산 (PLAN §8.2)
  - **출력은 High/Medium/Low 3버킷** (소수점 금지)
  - Top-3 반환, Low만 있으면 fallback 문구

- [x] **11-3. 텍스트 프리뷰 인라인 렌더**
  - 스킬이 `presets/<id>/preview.md`를 인라인 출력
  - 색상은 `⬛ ⬜` + HEX 조합 (터미널 가독)

- [x] **11-4. 설치 실행**
  - 프리셋 복사 + 어댑터 실행 + `.claude/skills/`, `.claude/agents/` 설치
  - 설치 요약 (무엇이 어디에) 출력
  - 버전 기록: target_repo `design-system/INSTALLED.json`에 `preset_id`, `preset_api_version`, `adapter`, `harness_version`, 설치 timestamp

- [x] **11-5. `design-customize` 스킬**
  - 신규: `plugin/skills/design-customize/SKILL.md`
  - 프리셋 복사본 → `projects/<user-name>/` → `brand_profile.json` 편집 가이드
  - 재합성 명령: `uv run design-ontology run-project ...`

---

## 🎯 여기서 MVP Alpha 종료. 이후는 Beta/GA.

---

## Phase 12: 프리뷰 — 텍스트 우선, 스크린샷 선택

### Phase 12A — MVP 포함 (Phase 7-5에 이미 생성)

- [x] **12A-1. 텍스트 프리뷰 템플릿** (Phase 7-5에서 자동 생성)
- [x] **12A-2. 텍스트 프리뷰 품질 검토 스크립트**
  - 신규: `design_ontology_harness/preview_linter.py`
  - 빈 섹션, 누락된 스와치, 서체 누락 탐지 (E001–E008 / W001–W003, stdlib 만)
  - CLI: `uv run design-ontology lint-previews [--preset-id <id>]` (error 있으면 exit 1)
  - 선택 연동: `uv run design-ontology validate-presets --include-preview-lint` (기본 비활성)
  - 테스트: `tests/test_preview_linter.py` 16 케이스 + CLI round-trip

### Phase 12B — alpha 후, P0만

- [ ] **12B-1. 프리셋 데모 페이지 생성기**
  - 신규: `design_ontology_harness/preview_renderer.py`
  - 프리셋 `component_specs.json` → 정적 HTML (**어댑터 출력 기반, 가짜 렌더러 금지**)
  - **2종 레이아웃**: hero, components grid
  - dark는 프리셋이 지원할 때만 각 뷰에 variant

- [ ] **12B-2. Playwright 캡처**
  - 의존성: `playwright-python`
  - 신규: `design_ontology_harness/preview_capture.py`
  - 1440×900 데스크톱만 (모바일 보류)
  - 결정론 가드: `document.fonts.ready`, 애니메이션 off, 고정 seed
  - 대상: **P0 5종 × 2장 = 10장** (+ 다크 지원 시 각 변형)
  - CLI: `uv run design-ontology render-previews --screenshots --tier P0`

- [ ] **12B-3. 변경 감지 재캡처**
  - `content_hash` 변경 시에만 재캡처
  - CI 캐시

- [ ] **12B-4. Fallback**
  - Playwright 실패/미설치 → 텍스트 프리뷰 자동 사용
  - 플러그인도 스크린샷 없으면 텍스트 표시

---

## Phase 13: 프리셋 확장 (P1 → P2 → P3)

### P1 (+5, 누적 10) — 🎯 P1 완료

- [x] **13-1. `dashboard--corporate-trust`** [tags: fintech]
- [x] **13-2. `monitoring-ops--minimal-tech`** [tags: devtools, ko]
- [x] **13-3. `document-content--minimal-tech`** [tags: reference-docs, devtools]
- [x] **13-4. `community-feed--playful-soft`**
- [x] **13-5. `canvas-tool--minimal-tech`** [tags: creative]

### P2 (+5, 누적 15)

- [x] **13-6. `marketing-landing--minimal-tech`** [tags: saas, devtools, ko]
- [x] **13-7. `commerce--bold-confident`** [tags: ecommerce, streetwear, ko]
- [x] **13-8. `conversation-copilot--editorial-warm`**
- [x] **13-9. `document-content--bold-confident`**
- [x] **13-10. `dashboard--editorial-warm`**

### P3 (+15 이상, 누적 30+)

- [ ] **13-11. P3 후보군 기여 접수**
  - PLAN §4.8 리스트 기준
  - 커뮤니티 기여 허용
  - 각 프리셋 `sources.json` 필수 (KB 시드 기록)

- [x] **13-11-A. P3 첫 프리셋 2종 self-contribution + build-sources 자동화 경로 안내** (dogfooding)
  - 신규 2종 P3 프리셋 — catalog-health priority_empty_cells top-10 #1/#2 셀:
    - `dashboard--bold-confident` (owner=`@maintainer-dogfood`, source `projects/lattice-dash/`, Ultra Violet #5F4B8B + Illuminating #F5DF4D + Creamsicle #FFD7A0, Retool/Appsmith/Stripe Radar/PostHog/Plausible/Mixpanel 시드 6건)
    - `dashboard--playful-soft` (owner=`@maintainer-dogfood`, source `projects/meadow/`, Periwinkle #8E9AF1 + Peach Puff #FFDAB9 + Mauve #E0B0FF, Cal.com/Notion/Flo/Finch/Calm/Headspace 시드 6건)
  - `spec_analyzer.py` UI_PATTERNS 에 "growth analytics admin" / "wellness habit tracking" 2 패턴 신규 — activation-funnel/cohort-matrix/referral-widget/retention-chart/conversion-funnel/experiment-panel/goal-tracker/user-list/ticket-queue/alert-list/segment-filter/filter-bar (growth) + streak-indicator/habit-calendar/wellness-score/mood-check/mood-chart/session-tracker/session-timeline/goal-grid/dashboard-card (wellness), 기존 15종 spec 에서 신규 term 0 hit 사전 검증. `keywords.json` dashboard app_mode 에 startup/growth/activation/retention/cohort/wellness/habit/tracking 어휘 + tags 에 startup/growth/cohort/referral/consumer/wellness/habit/tracking/mindful 신규.
  - `docs/CONTRIBUTING_PRESETS.md` Step 4.5 신규 섹션 — `build-sources --preset-id <id>` 사용법, 도메인 화이트리스트 kind 분류 테이블, 시드 < 3 warning 보완 절차, sources.json 예시. §5.3 가이드 (공공 레퍼런스 / 최소 3개 / kind 명시 / http(s) 시작 / 중복 dedup). §6 승급 조건 P3 에 "sources.json + seeds ≥ 3" 명시 + P2 에 "promote-preset --dry-run 5 gate" 명시. English Mirror 섹션 Step 2·Step 4.5 병기.
  - `preset_matcher/eval.py` 라벨 50 → 54 (+4 B2C 스타트업 vivid bold / startup admin activation / consumer wellness habit playful / soft wellness dashboard pastel) — 각 High Top-1 자기 자신. 대조군 50건 회귀 0. `tests/test_preset_matcher.py` 와 `tests/test_build_catalog.py` 하드코딩 숫자 50→54, 15→17 갱신.
  - 어댑터 round-trip smoke: Next+shadcn (light, ko) / raw-css (dark, ko) 4종 모두 OK, primary HEX globals.css/tokens.css 반영 (#5F4B8B / #8E9AF1). rebuild-all-presets 17/17 OK. build-sources --all --force 17/17 OK (6 시드 신규 2종, 전체 warn 0). snapshot fixture `pytest --update-snapshots` 1회 갱신 (신규 2종 + 기존 15종 sources.json 포함 content_hash 의도적 drift — 이후 회귀 0).
  - `promote-preset dashboard--bold-confident --target P2 --dry-run` / `promote-preset dashboard--playful-soft --target P2 --dry-run` — 5 gate (validate-presets 17 OK / lint-previews clean / adapter-round-trip Next+Raw / sources.json present strict / self-match Top-1 score=1.000) 모두 통과, manifest/matrix 변경 0. P3 → P2 sources.json strict gate 동작 확인.
  - `scripts/build-catalog.py` 재생성 → plugin `docs/CATALOG.md` (15 → 17 presets, P3 · 2 preset(s) 섹션 신규, credits 섹션 per-preset seed index 17 entries + aggregated references 확장).
  - **검증**: 전체 테스트 **181 → 185 passed** (+0 신규 테스트 추가, 기존 숫자 assert 갱신만), validate-presets 17/17 OK, lint-previews 17/17 OK, rebuild-all-presets 17/17 OK, build-sources 17/17 OK, eval-matcher **1.00 (54/54)** 유지, snapshot regression 0건, catalog-health 17종 / 42% coverage / deprecated 0 / deprecation 후보 17 / prune_eligible 0 / priority top-10 에서 2셀 제거 (top-8 출력 확인), prune-preset dashboard--bold-confident --dry-run → "not deprecated" error (안전장치 유지). validate-community-preset.py dashboard--bold-confident / dashboard--playful-soft 양쪽 HEX overlap 0 / 셀 중복 0 / self-match Top-1 (both ✓ all checks passed). check-plugin-compatibility.py adapter drift none + preset count 15→17. 플러그인 레포 `docs/CATALOG.md` 만 재생성 (의도적 diff — P3 카드 2장 + credits 섹션 확장) — push/tag/커밋 미실행. 다음 묶음 후보: Phase 13-11-B (실제 외부 기여자 1명 P3 PR 접수 — PR 템플릿 workflow 실전 검증 + PLUGIN_LOCAL_DEV 안내 검증) 또는 Phase 15 최종 마감 (마켓플레이스 공개 / 첫 릴리스 tag push 준비 / 플러그인 레포 public 전환 승인).

- [x] **13-11-B. 외부 기여자 페르소나 end-to-end 시뮬레이션 + commerce--playful-soft 수락** (2026-04-20)
  - 페르소나 `@alice-external` — CONTRIBUTING_PRESETS.md 만 참조, harness 내부 지식 차단. `projects/orchard/` (D2C 크래프트 스낵 commerce) 생성 → Step 1~5 실주행 → 마찰점 수집.
  - 신규 P3 프리셋 `commerce--playful-soft` — owner=`@alice-external`, source `projects/orchard/`, Rose Quartz #F7CAC9 + Dark Salmon #E9967A + Blanched Almond #FFEBCD, Olipop/Magic Spoon/Poppi/Graza/Caraway 5 시드 (전부 visual-reference kind). 기존 17종 HEX 겹침 0, bloom/meadow playful-soft 2종과 전면 차별화 (pink+terracotta+cream vs coral+mint+cornsilk / periwinkle+peach+mauve).
  - 마찰점 10건 발굴 + 즉시 패치:
    1. `init` 명령이 `--kb-dir` 힌트 없이 호출되면 Step 3 `run-project` 가 `No kb_dir configured` 에러로 막힘 → CONTRIBUTING Step 1 에 `--kb-dir kb/default` 플래그 예시 추가 + Step 3 에도 동일 플래그 병기.
    2. `init` scaffold 의 `visual_reference.query` 기본값 `["editorial dashboard", "premium app UI"]` 는 playful-soft / commerce 기여자에게 부적합 — CONTRIBUTING Step 2 에 "scaffold 기본값을 본인 브랜드 톤에 맞게 교체" 안내 추가.
    3. `init` scaffold brand_profile.json 에 `seeds: []` 필드가 없어 기여자가 누락할 가능성 → `scaffold.py:40-52` 에 `"seeds": []` 1줄 추가하여 근본 수정.
    4. `palette_roles` 가 `docs/color-reference.md` 에 등록되지 않은 이름을 받으면 경고 없이 `preferred_families` 기반 유사 팔레트로 폴백 — 의도 HEX 와 다른 결과. CONTRIBUTING Step 2 에 "palette_roles 이름은 `grep '^### ' docs/color-reference.md` 로 확인" 명시 + Rose Quartz / Dark Salmon / Blanched Almond 를 `docs/color-reference.md` Pastel Reds/Oranges/Yellows 섹션에 정식 등록 (3 entries 추가, 각 HEX/CMYK/톤/무드/활용/배색/출처 포함).
    5. `build-preset` 호출에 `--locale-pairings` 플래그가 빠지면 preview.md `Locale Pairings` 섹션이 누락 — CONTRIBUTING Step 4 예시 명령어에 `--locale-pairings projects/<your>/locale_pairings.json` 포함 + JSON 스니펫 예시 추가.
    6. matrix.json 에 신규 preset 엔트리를 **수동**으로 추가해야 matcher 가 후보로 인식 — CONTRIBUTING Step 4 말미에 경고 + PR 템플릿 체크박스 신규 추가.
    7. `validate-community-preset.py` 의 exit code / warning vs error 해석 기준이 없음 — CONTRIBUTING Step 5 에 3단계 table (errors=0 warnings=0 green, errors=0 warnings>0 review 재량, errors>0 block) 추가.
    8. 자연어 쿼리의 `warm` 키워드가 `brand_tone=editorial-warm` 로 끌림 (keywords.json) — CONTRIBUTING Step 5 에 "다른 톤 키워드 (warm/bold/minimal) 와 충돌하지 않는 2–4 단어 조합" 팁 추가.
    9. CONTRIBUTING §4 의 "현재 15종이 채운 셀" 표와 "Top-10 빈 셀" 이 18종 스냅샷으로 stale — 18종 기준 매트릭스 / Top-8 로 갱신 + `catalog-health` 활용 안내 추가 (실시간 우선순위 확인).
    10. PLUGIN_LOCAL_DEV.md 가 외부 기여자 관점 가이드가 없음 — 상단에 "External contributors → CONTRIBUTING_PRESETS.md" 배너 + §0 Prerequisites 섹션 (Python/uv/git + 첫 실행 `uv run design-ontology --help` + pytest 검증 + `kb/default` 공유 KB 안내) 신규 추가.
  - `spec_analyzer.py` UI_PATTERNS 에 "playful commerce" 1 패턴 신규 — add-to-cart-pill/rounded-variant-chip/rounded product-card/soft product-card/review-card/emoji-reaction/bestseller-ribbon/gift-message-input/subscription-toggle/subscription-card/consumer-toast/gentle-checkout/rounded-cart-drawer/empty-cart-illustration 13 term, orchard 외 기존 17종 spec 에서 신규 term 0 hit 사전 검증 (회귀 방지). `keywords.json` commerce app_mode 에 d2c/craft/snack/consumer/subscription/gifting 어휘 + tags 에 d2c/craft/snack/subscription/gift 5개 신규.
  - `preset_matcher/eval.py` 라벨 54 → 58 (+4 크래프트 D2C 커머스 친근 pastel / rounded consumer playful commerce soft d2c / 귀여운 D2C 스낵 쇼핑몰 친근 / pastel craft ecommerce playful d2c consumer rounded) — 각 High Top-1 자기 자신. 대조군 54건 회귀 0 (기존 쿼리 전부 유지). `tests/test_preset_matcher.py` 하드코딩 54→58, `test_build_catalog.py` 17→18 갱신. `test_color_mode_filter_zeroes_unsupported` 는 commerce--playful-soft 가 기존 대비 commerce--editorial-warm 의 순위를 +1 밀어내어 top_k 5→10 으로 조정 (score 의미는 동일 — raw_score=0 어설션 유지).
  - 어댑터 round-trip smoke: Next+shadcn (light, ko) / raw-css (dark, ko) 모두 OK, primary #F7CAC9 globals.css / tokens.css 반영. rebuild-all-presets 18/18 OK. build-sources --all --force 18/18 OK (commerce--playful-soft 5 visual-reference 시드, 전체 warn 0). snapshot fixture `pytest --update-snapshots` 1회 갱신 (신규 1종 + 기존 17종 content_hash drift — 이후 회귀 0).
  - `promote-preset commerce--playful-soft --target P2 --dry-run` 5 gate (validate-presets 18 OK / lint-previews clean / adapter-round-trip Next+Raw / sources.json strict from_tier=P3 / self-match Top-1 score=1.000) 모두 통과, manifest/matrix 변경 0.
  - PR 템플릿 workflow 로컬 dry-run — `/tmp/plugin-workflow-sim/` 에 main 17-preset baseline + alice-pr 브랜치 (+commerce--playful-soft) 시뮬레이션 → `git diff --name-status origin/main...HEAD` 로 신규 manifest 감지 (id 추출 `commerce--playful-soft`) → harness clone 후 `validate-community-preset.py --preset-id` 실행 → 3 check 모두 pass. PR 템플릿 체크리스트 2개 신규 추가 (`build-sources` seeds ≥ 3 + matrix.json 엔트리 수동 추가) + 기존 체크박스 8개 상세화 (Step 1 kb-dir / Step 2 palette_roles / Step 4 locale-pairings 인용 + 자연어 쿼리 키워드 충돌 주의).
  - `scripts/build-catalog.py` 재생성 → plugin `docs/CATALOG.md` (17 → 18 presets, `P3 · 3 preset(s)` 섹션 확장, credits 섹션 commerce--playful-soft 카드 + 5 시드 index 추가).
  - **검증**: 전체 테스트 **185 → 189 passed** (+0 신규 테스트, eval labels +4 간접 반영 + 기존 숫자 assert 갱신 + color_mode_filter top_k 조정), validate-presets 18/18 OK, lint-previews 18/18 OK, rebuild-all-presets 18/18 OK, build-sources 18/18 OK (seeds warn 0), eval-matcher **1.00 (58/58)** 유지, snapshot regression 0건, catalog-health 18종 / 45% coverage / deprecated 0 / deprecation 후보 18 / prune_eligible 0 / priority top-7 (top-10 중 commerce--playful-soft = #4 제거 확인). validate-community-preset.py commerce--playful-soft HEX overlap 0 (primary/accent/surface_tint 3 role 모두 unique) / 셀 중복 0 (commerce--playful-soft 초기 셀) / self-match Top-1 (✓ all checks passed). 플러그인 레포 workflow community-preset-check job 로컬 시뮬레이션 3 단계 전부 작동. check-plugin-compatibility.py adapter drift none + preset count 17→18. 플러그인 레포 `docs/CATALOG.md` + `.github/PULL_REQUEST_TEMPLATE/community-preset.md` 만 수정 — push/tag/커밋 미실행. 다음 묶음 후보: Phase 13-11-C (실제 GitHub PR 대기 모드 — 공개 홍보 후 외부 기여자 수집) 또는 Phase 15 최종 마감 (마켓플레이스 public 전환 + v0.1.0 tag push + GA 확정).

- [x] **13-11-C. 메인테이너 리뷰 SOP + 가상 기여자 2명 dogfood + Q2 catalog-health 리허설 + 마켓플레이스 체크리스트** (2026-04-21)
  - (C-1) 메인테이너 리뷰 SOP 수립 — 신규 `docs/MAINTAINER_REVIEW_SOP.md` (한국어 primary + 영문 mirror). 10 단계 절차 (a. 자동 체크 30 s / b. 기여자 프로필 2 m / c. 브랜드 IP 5 m / d. HEX + 셀 중복 3 m / e. preview.md 육안 2 m / f. self-match cross-validate 2 m / g. 소스 구조 1 m / h. 병합 + rebuild + matrix + plugin CATALOG 5 m / i. owner 통지 1 m / j. 실패 복구 5 시나리오) + 두 PR 동시 접수 처리 순서 + 경계 패턴 + 편의 스크립트 로드맵 + 실측 시간 데이터 §11. owner_since 1급 필드 승격은 Phase 13-11-D 이후 로드맵으로 유예 — 현재는 `manifest.generated_at` 을 근사치로 사용 (오차 ≤ 1 주) + PR 본문 댓글로 재평가 예정일 기록.
  - (C-2) 가상 기여자 2 명 end-to-end dogfood — `@bob-external` 의 `marketing-landing--editorial-warm` (source `projects/loom/`, Ochre Yellow #CB9D06 + Rust #B7410E + Wheat #F5DEB3 — editorial-warm 4 종 중 cream surface 공통 톤을 유지하되 primary/accent 차별화, Stratechery/Ghost/Every/Substack/The Verge Newsletters 5 시드) + `@carol-external` 의 `conversation-copilot--corporate-trust` (source `projects/mercer/`, Super Sonic #0071A8 + Copper #B87333 + Powder Blue #B0E0E6 — ledger Prussian Blue/Bronze Gold/Ice Blue corporate-trust 와 전면 차별화, ChatGPT Enterprise/Anthropic Enterprise/Stripe Dialog/Salesforce Einstein/Intercom Fin 5 시드). 두 프리셋 모두 HEX 1-겹침 warning 만 (bob = signal-desk Wheat / carol = beacon Powder Blue, 둘 다 다른 brand_tone 축이라 안전). `preset_matcher/keywords.json` hotfix 4 entry 추가 — marketing-landing 에 "퍼블리셔 / publisher / 뉴스레터 랜딩 / publisher landing / subscribe landing" 등 14 개 신규 + conversation-copilot 에 엔터프라이즈/regulatory chatbot 7 개 + corporate-trust 에 enterprise/compliance 9 개 + tags 에 publisher/enterprise/compliance 3 개 신규. bob 초기 self-match 2/3 실패 → keywords hotfix 후 3/3 High, carol 3/3 High 유지, 대조군 12 종 회귀 0. `preset_matcher/eval.py` 라벨 58 → 66 (+8 bob/carol 각 4 개) 100% Top-1 유지. SOP §11 에 실측 시간 + 관찰점 5 건 (keywords 튜닝 필수 · HEX 1 겹침 1 분 내 판정 · preview 대표 컴포넌트 오염 · matrix.json auto-upsert · post-merge 9 단계) 병기.
  - (C-3) 2026 Q2 catalog-health 리허설 리포트 — 신규 `docs/CATALOG_HEALTH_2026Q2.md`. 분기 요약 (P3 0 → 5, coverage 38% → 50%, eval labels 50 → 66) · 신규 접수 5 종 이력 · deprecation 후보 전수 zero_hits 원인 (install_hits/match_hits 측정 파이프라인 부재) · priority top-5 빈 셀 · Q3 P3 → P2 승급 계획 · 측정 파이프라인 도입 결정 (Phase 16 로 유예 - scope 분리) · catalog-health CI workflow 제안 · 관찰점 4 건 · Q3 액션 아이템 6. 신규 `.github/workflows/catalog-health.yml` harness 레포 측 (월 09:00 UTC cron + workflow_dispatch, `uv sync` → catalog-health → diff 있으면 `peter-evans/create-pull-request@v6` 로 PR 자동 생성, contents:write + pull-requests:write). workflow 실행은 사용자 승인 대기.
  - (C-4) 마켓플레이스 공개 직전 체크리스트 — 신규 `docs/MARKETPLACE_LAUNCH_CHECKLIST.md` 15 항목 (라이선스 · README Quick Start · validate.yml 30일 green · 20 presets validator pass · version 3-way 정합성 · CATALOG.md 렌더 · DEMO_SCRIPTS 재검증 · release.yml 시뮬레이션 · 이슈 템플릿 · CoC · SLA · marketplace status · Pretendard 자산 · 보안 스캔 · 후폭풍 대응) + D-day 실행 순서 부록. 현재 상태 9 통과 / 5 경고 / 1 미완 (CoC). (C-4-b) 2 항목 즉시 실행: 신규 `scripts/check-version-consistency.py` stdlib only — plugin.json / marketplace.json / CHANGELOG 3-way 검증 실행 → all match on 0.1.0. `validate-community-preset.py` 20 일괄 실행 → 18 "all checks passed" + 2 "no errors (warnings — glacier/orbit source 공유 기존 HEX overlap, 예상된 케이스)" = 20/20 errors=0. 결과는 `tmp/community-validator-report-2026-04-21.txt` 에 보관.
  - **검증**: 전체 테스트 **189 → 197 passed** (+0 신규 테스트, eval labels 58 → 66 + test_preset_matcher assert 58→66 + test_build_catalog assert 18→20 + snapshot fixture 20 entries 갱신), validate-presets 20/20 OK, lint-previews 20/20 OK (errors=0 warnings=0), rebuild-all-presets 20/20 OK, build-sources --all --force 20/20 OK (20 sources.json 전부 seeds ≥ 3 warn 0), eval-matcher **1.00 (66/66)** confusion 공집합, snapshot regression 0건, catalog-health 20종 / 50% coverage / deprecated 0 / deprecation 후보 20 / prune_eligible 0 / priority top-5 (commerce--minimal-tech #3 · marketing-landing--playful-soft #6 · document-content--corporate-trust #8 · monitoring-ops--corporate-trust #9 · canvas-tool--bold-confident #10 — loom 은 #2 자리 채워서 top-5 에서 제거, mercer 는 #7 자리 채워서 제거), validate-community-preset.py 20/20 통과 (18 all checks passed + 2 warnings only), check-plugin-compatibility.py adapter drift none + preset count 18 → 20 compatibility OK, check-version-consistency.py 3-way match 0.1.0. promote-preset dry-run `marketing-landing--editorial-warm --target P2` + `conversation-copilot--corporate-trust --target P2` 양쪽 5 gate (validate / lint / adapter round-trip Next+Raw / sources.json strict from_tier=P3 / self-match Top-1 score=1.000) 모두 통과, manifest/matrix 변경 0. 플러그인 레포 `docs/CATALOG.md` 재생성 (20 presets, P3 · 5 preset(s) 섹션 확장, credits 섹션 loom + mercer 카드 + 10 시드 index 추가) — push/tag/커밋 미실행. 다음 묶음 후보: Phase 13-11-D (실제 GitHub PR 1–2 건 수집 대기 — 공개 홍보 이후 외부 기여자 실수요 접수, 완전 수동 큐레이션 + 실측 metric 시작) / Phase 15 최종 마감 (마켓플레이스 public 전환 + v0.1.0 tag push + GA 확정 + release.yml 첫 실행) / Phase 16 (install_hits/match_hits 측정 파이프라인 + Q3 catalog-health 실측 발간).

- [x] **13-12. 커뮤니티 프리셋 기여 가이드**
  - `docs/CONTRIBUTING_PRESETS.md` (한국어 primary + 영문 mirror) — 5단계 절차, axis 선택 가이드, top-10 빈 셀, HEX/셀 중복 체크 절차, 승급/오너십/deprecation 정책
  - `scripts/validate-community-preset.py` (stdlib only) — preset_validator + preview_linter 재사용 + HEX 겹침 warning + 셀 중복 warning + self-match error. CLI `--preset-id` / `--diff-mode`
  - `tests/test_validate_community_preset.py` 6 케이스 (pass / hex 중복 / 셀 중복 / 필수 파일 누락 / self-match 실패 / CLI exit code)
  - `design-ontology-plugin/.github/PULL_REQUEST_TEMPLATE/community-preset.md` (checklist + owner 책임 + 브랜드 IP 선언)
  - `design-ontology-plugin/.github/workflows/validate.yml` 확장 — PR 에서 신규 preset manifest 감지 시 harness 레포 clone → `validate-community-preset.py` 실행

---

## Phase 14: 공개 배포 / 문서

- [x] **14-1. plugin 레포 README**
  - 3분 Quick Start + 자연어 한 줄 예시
  - 프리셋 카탈로그 요약 매트릭스 (app_mode × brand_tone) + `docs/CATALOG.md` 링크
  - 어댑터 매트릭스 (Next/raw-css/vite beta) + 충돌 정책 (.ds-proposed)
  - 한글 1급 지원 섹션 (Pretendard + keep-all/tabular-nums + locale_pairings.ko 목록)
  - 설치 후 생성 파일 트리 + 버전 계약 표 + 라이선스 (MIT + SIL OFL)

- [x] **14-2. harness 레포 README 갱신**
  - 상단 유도 배너: "그냥 프리셋을 쓰고 싶다면 → plugin 레포"
  - "플러그인 vs 하네스" 결정표 (6행)
  - "플러그인 배포" 섹션: 카탈로그 요약 + 메인테이너 5스텝 워크플로우 + 버전 계약 4필드 표 + sync 파이프라인 다이어그램
  - "Phase 진행 상태" 표 (1~15, Phase 14/15 done)

- [x] **14-3. 프리셋 카탈로그 + 자동 생성 스크립트**
  - 신규 (harness): `scripts/build-catalog.py` stdlib only
    - matrix.json + 각 preset manifest.json + preview.md 파싱 (regex + section 스캐너)
    - `PreviewBlock` dataclass: summary / core_colors / semantic_colors / typography / components / cautions
    - 출력: At a glance · Filter axes 표 · app_mode × brand_tone 매트릭스 · tier 별 카드 (P0/P1/P2/P3)
    - 각 카드: preset_id · tier · app_mode · brand_tone · default_color_mode · color_modes · tags · source_project · owner · Core HEX + `⬛`/`⬜` 스와치 (luminance 기반) · Typography (heading/body/mono/korean) · locale_pairings · 대표 컴포넌트 top-3 · 추천 용도 · 주의사항 · links
  - 신규 (plugin): `docs/CATALOG.md` 자동 생성 (초기 15종 · 이후 20종으로 재생성)
  - 테스트: `tests/test_build_catalog.py` 5 케이스 (parse / swatch luminance / render / CLI)

- [x] **14-4. 공개 마켓플레이스 등록 준비**
  - `.claude-plugin/marketplace.json` status: `pre-alpha` → **`alpha`**
  - categories 확장 (5종: design-systems, frontend, ui, tokens, internationalization)
  - keywords 확장 (7 → 22, app_mode 8종 + brand_tone 5종 전부 포함)
  - source.repository 기본값 설정 (`2000silpeed/design-ontology-plugin`)
  - summary/description 에 "20 curated presets" / P0/P1/P2/P3 수치 반영
  - 실제 github public + `/plugin marketplace add` 실행은 사용자 승인 대기

- [x] **14-5. 데모 시나리오 문서**
  - 신규 (plugin): `docs/DEMO_SCRIPTS.md` (영상/GIF 대신 텍스트 시나리오)
  - 한국어 3종: 한국어 SaaS 대시보드 · AI 글쓰기 코파일럿 · 패션 모바일 커머스
  - 영문 3종: Developer docs · Streetwear drop ecommerce · SRE observability
  - 각 시나리오: free-text 입력 → 예상 matcher Top-3 출력 → install 명령 → 결과 파일 트리 + 다음 단계
  - 후속 영상 촬영 가이드 (1080p · one-take · voiceover 불필요)

- [x] **14-6. 릴리스 자동화 wiring**
  - 신규: `.github/workflows/release.yml`
    - 트리거: tag push `v*.*.*` + `workflow_dispatch`
    - 스텝: plugin.json/marketplace.json version ↔ tag 정합성 검증 → preset_api_version range 2차 검증 → conventional commits 기반 카테고리별 릴리스 노트 생성 (`feat`/`fix`/`chore`/`docs`/`test`/`refactor`/Other) → CHANGELOG.md 상단 삽입 + 자동 PR → `gh release create`
    - 권한: `contents: write` (기본 GITHUB_TOKEN 충분)
  - 신규: `CHANGELOG.md` v0.1.0 initial (Phase 7~13-10 누적 산출물 전부 기록)
  - 신규: `docs/RELEASE.md` 릴리스 절차 + SemVer 정책 + 롤백 가이드 + 실패 모드 표
  - 2026-04-29 실제 `v0.1.0` tag push / `gh release create` 실행 완료 — release run `25115752943` success

- [x] **14-7. 공개 직전 로컬 gate 마감**
  - plugin README 15종 표기를 20종(P0×5/P1×5/P2×5/P3×5) 기준으로 갱신
  - plugin `docs/CATALOG.md` 재생성 + `presets/` 로컬 scaffold 동기화
  - `scripts/verify-demo-scripts.py` 신규 — 6개 DEMO_SCRIPTS 시나리오 Top-1/버킷 자동 검증
  - `monitoring-ops` 단일 tone query 보강 — SRE observability demo 가 `Low` fallback 으로 떨어지지 않도록 matcher 보정
  - 공개 GitHub run history / tag push / gh release 는 2026-04-29 public repo 생성 후 실제 실행 완료

---

## Phase 15: 라이프사이클 정책 운영 (PLAN §11 구현)

- [x] **15-1. `catalog-health` 리포트**
  - 신규 CLI: `uv run design-ontology catalog-health [--json] [--output <path>] [--metrics-dir] [--snapshot-fixture]`
  - 지표 (per-preset): tier, app_mode, brand_tone, tags, owner, generated_by_harness_version, version_drift_minor, content_hash, last_rebuilt_at, preview_lint_status (OK/WARN/ERROR), install_hits, match_hits, snapshot_drift, deprecation_reasons
  - 지표 (전체): tier 분포, 셀 커버리지 (8×5), priority empty cells top-10, deprecation 후보, snapshot_drift_count
  - 신규: `design_ontology_harness/catalog_health.py` (stdlib only) — `compute_health()` / `format_markdown()` / `format_summary()`
  - 신규: `presets/.metrics/{install_hits,match_hits}.json` 빈 dict scaffold + `README.md` (수동 입력, Phase 15-4 pruning 입력)
  - 출력: `presets/CATALOG_HEALTH.md` 자동 생성 (초기 15종 기준 38% coverage / 15 deprecation 후보, 이후 20종 기준으로 재계산). version_drift 는 pyproject.toml `[project] version` 동적 로딩.

- [x] **15-2. 승급 파이프라인**
  - `design_ontology_harness/preset_ops.py` — `promote_preset(preset_id, target_tier, *, dry_run, presets_root)` + 5단계 게이트 (validate-presets / lint-previews / adapter round-trip (Next + Raw) / sources.json / self-match Top-1)
  - CLI: `uv run design-ontology promote-preset <id> [--target P0|P1|P2] [--dry-run]` — 성공 시 manifest 에 `tier` / `promoted_at` / `promoted_from` 업데이트 + matrix.json tier 동기화
  - sources.json gate: `from_tier == "P3"` 일 때만 strict (기존 15종 legacy 승급은 warning), 신규 커뮤니티 P3→P2 승급에만 필수
  - 어댑터 round-trip: `_ROUND_TRIP_ADAPTERS = (nextjs-tailwind-shadcn, raw-css-variables)` 임시 target repo 에 설치 시도 (적어도 1개 통과)
  - 테스트: `tests/test_preset_ops_promote.py` 6 케이스 (happy path / dry-run / validate 실패 차단 / self-match 실패 차단 / 이미 top → error / 하향 target → error)

- [x] **15-3. Deprecation 파이프라인**
  - `design_ontology_harness/preset_ops.py` — `deprecate_preset(preset_id, *, reason, replacement, force, presets_root)` — manifest 에 `deprecated_at` / `deprecation_reason` / `deprecated_replacement` 기록
  - reason: `zero_hits | version_lag | snapshot_drift | owner_abandoned | manual` + `manual:<자유텍스트>` 패턴
  - CLI: `uv run design-ontology deprecate-preset <id> --reason <reason> [--replacement <id>] [--force]`
  - matcher 숨김: `match_presets(..., include_deprecated=False)` (기본값) — CLI `match-preset --include-deprecated` 플래그 + `MatchResult.deprecated` / `deprecated_replacement` 노출 + rationale 에 "deprecated (reason), 대체: <id>" 주입 + 결과 라벨 `🗑️ deprecated`
  - eval.py / validate-community-preset.py 는 `include_deprecated=True` 로 호출 — eval 50/50 회귀 유지
  - schemas/preset_manifest.schema.json 확장: `promoted_at` / `promoted_from` / `deprecated_at` / `deprecation_reason` / `deprecated_replacement` 선택 필드 추가 + reason 정규식 패턴 + replacement preset_id 패턴
  - preset_validator: deprecation 필드 내부 일관성 (reason 없으면 error, 잘못된 reason 패턴 error, replacement 가 실재 preset 참조하는지 + self-reference 금지)
  - catalog_health: preset 엔트리에 `deprecated_at` / `deprecation_reason` / `deprecated_replacement` 노출 + 전역 `deprecated_count` / `deprecated_presets` 추가, `## Deprecated` 섹션을 active 카탈로그와 분리, 이미 deprecated 된 프리셋은 deprecation_candidates 에서 제외
  - 테스트: `tests/test_preset_ops_deprecate.py` 6 케이스 (manifest 필드 기록 / matcher 숨김 + include_deprecated 복원 / 재호출 차단 + --force 갱신 / invalid reason / missing replacement / catalog_health Deprecated 섹션)

- [x] **15-4. 분기별 pruning**
  - `design_ontology_harness/preset_ops.py` — `prune_preset(preset_id, *, confirm, dry_run, presets_root, min_deprecated_age_days=90)` 4단계 게이트 (deprecated / age ≥ 90d / install+match hits 0 / --confirm). 성공 시 `presets/<id>/` rmtree + matrix.json entry 제거 + `tests/fixtures/preset_snapshots.json` entry 제거. `find_prune_eligible()` 헬퍼.
  - CLI: `uv run design-ontology prune-preset <id> [--confirm] [--dry-run] [--min-age-days N] [--all] [--presets-dir]` — 기본 dry-run, 실삭제는 --confirm 필수, --all 은 catalog_health.prune_eligible 일괄 처리
  - `catalog_health` 에 per-preset `deprecated_age_days` / `prune_eligible` / `prune_blocked_reasons` + 전역 `prune_eligible_count` / `prune_eligible_presets` + `## Prune Eligible` 섹션 추가
  - 테스트: `tests/test_preset_ops_prune.py` 9 케이스 (happy path / 4개 gate 실패 / dry-run 무변화 / min-age 오버라이드 / find_prune_eligible / catalog_health 통합)

- [x] **15-5. 프리셋 snapshot 회귀 테스트**
  - 신규: `tests/test_preset_snapshots.py` — matrix.json 의 모든 프리셋 manifest.content_hash 를 `tests/fixtures/preset_snapshots.json` 와 비교
  - 신규: `tests/conftest.py` — `--update-snapshots` pytest 플래그 + `update_snapshots` fixture
  - 실패 시 안내: drift 항목 + `pytest tests/test_preset_snapshots.py --update-snapshots` 갱신 명령
  - 초기 snapshot fixture: 15종 sha256 (build-preset 출력 그대로)
  - catalog_health 연동: snapshot fixture vs 현재 manifest 비교 → 프리셋별 `snapshot_drift: bool` + 전역 `snapshot_drift_count`

- [x] **15-6. 매칭 품질 평가**
  - 라벨 데이터 30 → 50 건 확장 — 기존 15종 모두 커버 + 모호/경쟁/한영 mixed/tag 우세/adversarial "editor" edge case 포함 (정답 dataset 은 `design_ontology_harness/preset_matcher/eval.py` 에 canonical 로 상주, 테스트는 import)
  - threshold 80% → **85%** 상향 (`test_top_1_accuracy_threshold`)
  - `design_ontology_harness/preset_matcher/eval.py` 신규 — `run_eval()` + `EvalResult` + confusion_pairs top-5 출력
  - CLI `uv run design-ontology eval-matcher [--verbose] [--threshold 0.85]` — accuracy 미달 시 exit 1
  - 현재 accuracy **1.00 (50/50)**, confusion 공집합 — 추가 keywords 튜닝 불필요 (기존 30건 전부 유지, 회귀 제로 확인)

- [x] **15-7. 어댑터 버전 호환성**
  - `preset_validator.py` — 각 preset 의 `adapter_compatibility[<adapter>]` range 가 해당 어댑터의 현재 `ADAPTER_VERSION` (StackAdapter.version 클래스 속성) 을 포함하는지 교차 검증. 불포함 시 `[<preset>] adapter '<id>' current=X.Y.Z outside range <range>` error
  - `validate_all(..., adapter_versions=...)` override 인자 — 테스트에서 drift 시뮬레이션용
  - `scripts/check-plugin-compatibility.py` — 기존 preset_api_version 체크에 adapter 현재 버전 추가, 리포트 말미에 `Adapter drift:` 섹션 (없으면 "none — every preset range covers the current adapter version", 있으면 각 위반 라인 + VIOLATIONS 총합에 합산)
  - 테스트: `tests/test_preset_validator.py` 4 케이스 (범위 내 통과 / 범위 밖 error / 잘못된 range error / 실제 15종 catalog 통과 guardrail)

- [x] **15-8. 피드백 채널**
  - plugin 레포 `.github/ISSUE_TEMPLATE/` 신규 3종 (GitHub Issue Forms 스펙):
    - `preset-feedback.yml` — preset_id dropdown 20종 + use_case / problem / expected / context_link
    - `new-preset-request.yml` — app_mode × brand_tone dropdown + use_case / references / ko 필요 / 본인 기여 가능
    - `bug-report.yml` — reproduction / expected / actual / env (yaml render) / logs (text render)
  - `.github/ISSUE_TEMPLATE/config.yml` — `blank_issues_enabled: false` + contact_links (CONTRIBUTING_PRESETS · Discussions placeholder)
  - plugin README "피드백 & 이슈" 섹션 추가 — 한국어 primary + 영문 병기
  - harness README 상단 배너에 "피드백·이슈는 plugin 레포로" 한 줄 추가

- [x] **15-9. 라이선스/크레딧**
  - `preset_ops.build_sources_json(preset_id, ...)` — brand_profile.seeds + visual_reference.source_references + spec.md markdown 링크 → dedup + 도메인 화이트리스트 기반 kind 추론 (`design-system` / `visual-reference` / `brand-guide` / `reference-docs` / `article`) → `presets/<id>/sources.json` 생성. `build_sources_for_all()` 일괄 헬퍼.
  - CLI: `uv run design-ontology build-sources [--preset-id <id>] [--all] [--force] [--projects-root projects]` — kind 분포 + 시드 개수 요약, 시드 < 3 일 경우 warning.
  - 초기 15종 프리셋 전부 sources.json 생성 (3~6 시드/건), `brand_profile.json` 에 `seeds` 필드 일괄 추가 (orbit/signal-desk/glacier/colorfit/premier-league/ledger/pulse/lattice/bloom/atelier/beacon/drop/quill/broadside/curator).
  - 신규 스키마: `schemas/preset_sources.schema.json` + `preset_validator` 에서 sources.json 존재 시 필수 필드 (preset_id/source_project/seeds[]/pretendard_font_license/created_at) + 각 seed (url/kind/title 필수, url은 http(s):// 시작) 검증 추가.
  - Pretendard SIL OFL 고지 정비: `adapters/base.py._pretendard_license` 에 "재배포 시 이 고지 유지 필수 (OFL §2)" 한국어/영어 문구 추가. plugin `LICENSE-FONTS` 한국어 + 영문 병기 (재제작자 고지 · 상표권 · 번들 정책 · 재배포 체크리스트). plugin README License 섹션 한국어/영문 병기 + `scripts.sil.org/OFL` 링크. harness README "플러그인 배포" 섹션에 Pretendard 런타임 fetch + OFL §2 한 줄 추가.
  - `scripts/build-catalog.py` 에 `## KB Sources & Credits` 섹션 추가 — per-preset seed 개수/kind 분포 테이블 + aggregated URL → referenced presets 테이블 + 번들 서체 (Pretendard/Inter/JetBrains Mono) 라이선스 subsection.

- [x] **15-10. 운영 launch gate 정리**
  - 신규 `CODE_OF_CONDUCT.md` harness/plugin mirror — Contributor Covenant v2.1 취지 + 한국어 요약
  - plugin README 에 2주 1차 반응 / 4주 리뷰 완료 SLA 추가
  - 신규 `scripts/sync-issue-template-presets.py` — preset-feedback dropdown 을 matrix.json 20종과 동기화
  - 신규 `scripts/security-scan-launch.py` — high-confidence secret prefix/private key block scan
  - `docs/MARKETPLACE_LAUNCH_CHECKLIST.md` 2026-04-29 기준 갱신: 통과 14종, 공개 1주 후 beta 판단 1종 대기

---

## 의존 순서 (v2, 병렬 주장 삭제)

```
Phase 7 (인프라 + 버전 계약)
        │
        ▼
Phase 8 (P0 5종 + 텍스트 프리뷰)
        │
        ▼
Phase 9 (plugin 레포 + 스킬/에이전트 이식)
        │
        ▼
Phase 10A (Next+shadcn 어댑터 1종만)
        │
        ▼
Phase 11 (/design-start UX) ──── 🎯 MVP ALPHA
        │
        ▼
Phase 12B (P0 선택적 스크린샷)
        │
        ▼
Phase 10B / 10C (나머지 어댑터 2종)
        │
        ▼
Phase 13 (P1 → P2 → P3)
        │
        ▼
Phase 14 (공개 배포)
        │
        ▼
Phase 15 (라이프사이클 정책 운영, 지속)
```

**임계 경로**: 7 → 8 → 9 → 10A → 11 (MVP)
**Phase 10 ↔ Phase 12 병렬 가능 주장은 삭제** — 코덱스 지적대로 프리뷰가 어댑터 출력을 반영해야 "진짜", 그렇지 않으면 synthetic. 순차 의존.

---

## 진행 기록

| 날짜 | 태스크 | 상태 |
|------|--------|------|
| 2026-04-29 | **Public plugin release 완료**: `2000silpeed/design-ontology-plugin` public GitHub repo 생성, plugin mirror initial commit `f79fa29` main push, `v0.1.0` annotated tag push. GitHub Actions `validate` run `25115751357` success, `release` run `25115752943` success, GitHub Release `https://github.com/2000silpeed/design-ontology-plugin/releases/tag/v0.1.0` 생성 완료. harness main 에는 Phase 14/15 마감 커밋 `321fb29` + 실제 repo URL 반영 커밋 `c8ae79d` push 완료. 남은 항목은 공개 1주 후 marketplace status `alpha → beta` 판단. | done |
| 2026-04-29 | **Phase 14/15 로컬 마감 완료**: Phase 14 공개 배포 gate 와 Phase 15 운영 gate 를 현 상태 기준으로 닫음. plugin README/marketplace 설명을 20 presets 기준으로 갱신, `presets/` 로컬 scaffold + CATALOG 재동기화, preset-feedback issue template 을 matrix.json 20종과 자동 동기화. 신규 스크립트 3종 `verify-demo-scripts.py` / `sync-issue-template-presets.py` / `security-scan-launch.py` 추가. DEMO_SCRIPTS 6종 Top-1 전부 High 검증, SRE observability query 는 단일 app_mode tone 추론으로 `monitoring-ops--minimal-tech` High 매칭. harness/plugin `CODE_OF_CONDUCT.md` mirror 추가, plugin README SLA(2주 1차 반응 / 4주 리뷰 완료) 명시. `MARKETPLACE_LAUNCH_CHECKLIST.md` 를 로컬 통과 12종 / 외부 실행 대기 3종(public run history, 실제 tag/release, alpha→beta 사후 판단) 으로 먼저 분리했고, 이어진 public release 단계에서 앞의 2개 외부 항목을 실제 완료 처리. | done |
| 2026-04-18 | PLUGIN_PLAN.md v1 초안 | done |
| 2026-04-18 | PLUGIN_TASKS.md v1 초안 | done |
| 2026-04-18 | v1 결정 반영 (30+, 별도 레포, 어댑터 A/C/B, 스크린샷, 공개, 단일 semver) | done |
| 2026-04-18 | 코덱스 consult 리뷰 수행 (295K tokens) | done |
| 2026-04-18 | **v2 전면 반영**: 버전 계약 Phase 7 승격, MVP 어댑터 1개로 축소, 프리뷰 텍스트 우선, 축 재설계(app_mode 8 + tone 5 + color_mode + tags), 매칭 coarse bucket, Phase 10/12 분할, 라이프사이클 정책 신설 | done |
| 2026-04-18 | **Phase 7 완료**: 스키마 3종(matrix/manifest/compatibility), matrix.json 축 정의, keywords 사전, preset_builder/validator, semver_range 유틸, sync 스크립트, CLI 3종(build-preset/validate-presets/rebuild-all-presets) | done |
| 2026-04-18 | **Phase 9 로컬 scaffold 완료**: `../design-ontology-plugin/` 로컬 레포 + `.claude-plugin/plugin.json`·`marketplace.json` + 스킬 4종·에이전트 4종 이식(프리셋 계약 확인 섹션 포함) + harness/plugin 양쪽 CI 워크플로우 + `docs/PLUGIN_LOCAL_DEV.md` + `docs/LOCAL_DEV.md`. sync dry-run(5 manifest) OK. GitHub 공개 레포 생성은 승인 대기. | done |
| 2026-04-18 | **Phase 11 MVP alpha 완료**: 매칭 엔진(`preset_matcher/engine.py`, raw_score + 3-bucket) + 설치 오케스트레이터(`preset_installer.py`, INSTALLED.json + idempotent re-install) + customize ops(`customize_ops.py`) + CLI 3종(`match-preset`/`install-preset`/`customize-preset`). 플러그인 `/design-start`·`/design-customize` 스킬 이식 + plugin.json 등록. 테스트 52 passed(기존 26 + 11-5 26). `/tmp/install-smoke`에 dashboard--minimal-tech 설치 round-trip OK. | done |
| 2026-04-18 | **Phase 10B 완료**: `raw-css-variables` 어댑터 (design-system/tokens.css + fonts.css[ko] + Pretendard 스캐폴드 + README) 추가 + 레지스트리 등록. `design_system_mirror_ops()` 를 base.py 로 공통화해 Next/Raw 어댑터 공유. `tests/test_adapter_raw_css.py` 14 케이스 추가, 전체 66 passed. `/tmp/raw-css-smoke` 설치 스모크 OK (noop + --force 재적용 확인, user repo 최상위 파일 0건). | done |
| 2026-04-18 | **Phase 12A-2 완료**: `preview_linter.py` (E001–E008 / W001–W003, stdlib only) + `lint-previews` CLI + `validate-presets --include-preview-lint` 선택 플래그. P0 5종 errors=[] / warnings=[] 통과. 합성 fixture 기반 `tests/test_preview_linter.py` 16 케이스 (룰별 + CLI round-trip) 추가, 전체 97 passed (기존 81 + 신규 16). | done |
| 2026-04-19 | **Phase 13-1 완료**: `dashboard--corporate-trust` [tags: fintech, ko] P1 신규 프리셋. 신규 source project `projects/ledger/` (Prussian Blue + Bronze Gold + Ice Blue 팔레트, Stripe/Brex/Mercury 시드). kb/default 공유 재사용. preview.md 7 HEX swatch + 3 컴포넌트 + Pretendard ko 통과. validate/lint 6종 전부 OK, match-preset "fintech 대시보드 보수적 신뢰 한글" → High(1.0). Next+shadcn / raw-css 어댑터 round-trip OK. `tests/test_preset_matcher.py` fintech 라벨 2건 추가 + 모호 케이스 disambiguation, 전체 99 passed (기존 97 + 신규 2). | done |
| 2026-04-19 | **Phase 13-2 완료**: `monitoring-ops--minimal-tech` [tags: devtools, ko, default_color_mode=dark] P1 2호 프리셋. 신규 source project `projects/pulse/` (Azure Blue #007FFF + Emerald Green + Ice Blue 팔레트, Grafana/Datadog/Honeycomb 시드). kb/default 공유. preview.md 7 HEX + 대표 컴포넌트 inline-alert/chart-container/chart-tooltip 3개 (monitoring-ops signature_keywords "alert"/"chart" 매칭) + Pretendard ko 통과. validate/lint 7종 OK, match-preset `--app-mode monitoring-ops --brand-tone minimal-tech` → High(1.0), "observability grafana 스타일 devtools" → Medium Top-1. Next+shadcn (dark) / raw-css (light) 어댑터 round-trip OK — primary `#007FFF` tokens.css/globals.css 반영. `keywords.json` monitoring-ops 에 grafana/datadog/prometheus/incident/oncall 브랜드 키워드 확장. `tests/test_preset_matcher.py` 라벨 2건 추가, 전체 101 passed (기존 99 + 신규 2). 누적 프리셋 7종. | done |
| 2026-04-19 | **Phase 13-4 완료**: `community-feed--playful-soft` [tags: social, community, ko, default_color_mode=light] P1 4호 프리셋. 신규 source project `projects/bloom/` (Coral Blush #F88379 + Mint Green #98FF98 + Cornsilk #FFF8DC 팔레트 — 기존 8종 HEX 겹침 0, warm pastel + rounded sans 로 minimal-tech/corporate-trust 정반대 방향, Threads/Bluesky/Mastodon/Are.na/Tumblr 시드). `spec_analyzer.py` UI_PATTERNS 에 community-feed 전용 2 패턴 추가 ("community feed" / "presence and notifications") — feed-item/post-card/thread-view/reply-composer/reaction-bar/follow-button/timeline-stream/avatar-cluster/tag-pill/share-sheet/empty-feed-illustration/gentle-toast/soft-dialog/presence-indicator/notification-center/notification-item/mention-highlight 등 17개 신규 컴포넌트 매핑. 기존 8종 spec 에서 신규 term 0 hit 사전 검증 — rebuild 후 기존 preview 대표 컴포넌트 drift 없음. `keywords.json` tags 에 social/community 확장. preview.md 대표 컴포넌트 feed-item/thread-view/comment-thread (community-feed signature_keywords "feed"/"thread"/"comment" 매칭) + 7 HEX swatch + Pretendard ko 통과. validate/lint 9종 OK, match-preset "소셜 피드 친근 파스텔 커뮤니티" / "social feed thread playful rounded soft" / `--app-mode community-feed --brand-tone playful-soft` 모두 High Top-1. 대조군 "에디토리얼 매거진" / "document reading blog, warm" / "API 레퍼런스 개발자 미니멀" / "fintech 대시보드 신뢰 한글" 모두 High Top-1 유지 — 회귀 없음. Next+shadcn (light) / raw-css (dark) 어댑터 round-trip OK — primary `#F88379` globals.css/tokens.css 반영. `tests/test_preset_matcher.py` 라벨 2건 추가, 전체 105 passed (기존 103 + 신규 2). 누적 프리셋 9종. | done |
| 2026-04-19 | **Phase 13-3 완료**: `document-content--minimal-tech` [tags: reference-docs, devtools, ko, default_color_mode=light] P1 3호 프리셋. 신규 source project `projects/lattice/` (Iris Violet #5A4FCF + Cerulean #2A52BE + Lavender Mist #E6E6FA 팔레트 — 기존 7종 Navy/Azure/Prussian blue 와 HEX 겹침 없는 Violet 계열 차별화, Linear/Stripe/Vercel/MDN docs 시드). `spec_analyzer.py` UI_PATTERNS 에 reference-docs 전용 4 패턴 추가 ("reference documentation"/"code documentation"/"callout and admonition"/"api reference") — article-body/table-of-contents/heading-anchor/prose-block/reading-pane/footnote/code-block/inline-code/callout/api-reference-table/parameter-table/version-switcher 등 17개 신규 컴포넌트 매핑. 기존 6종 spec 에서 신규 term 0 hit 검증 — editorial-warm/monitoring-ops 등 기존 preview 변경 없음. preview.md 대표 컴포넌트 article-body/prose-block/table-of-contents (document-content signature_keywords "article"/"prose"/"toc" 매칭) + 7 HEX swatch + Pretendard ko 통과. validate/lint 8종 OK, match-preset "API 레퍼런스 개발자 미니멀" / "stripe docs reference minimal devtools" / `--app-mode document-content --brand-tone minimal-tech --tags reference-docs,devtools` 모두 High Top-1. 대조군 "에디토리얼 매거진" / "document reading blog, warm" 여전히 editorial-warm High 유지. Next+shadcn (light) / raw-css (dark) 어댑터 round-trip OK — primary `#5A4FCF` globals.css/tokens.css 반영. `tests/test_preset_matcher.py` 라벨 2건 추가, 전체 103 passed (기존 101 + 신규 2). 누적 프리셋 8종. | done |
| 2026-04-19 | **Phase 13-5 완료** 🎯 **P1 tier 완료 (누적 10종)**: `canvas-tool--minimal-tech` [tags: creative, ko, default_color_mode=light] P1 5호 프리셋. 신규 source project `projects/atelier/` (Cobalt Violet #804AA8 + Amber #FFBF00 + Misty Blue #B5C7EB 팔레트 — 기존 9종 Navy/Azure/Iris Violet/Bronze/Coral/Prussian 등과 HEX 겹침 0, 차분한 cool purple + Figma-esque vivid amber accent + 보라 섞인 뉴트럴 블루 surface 조합으로 minimal-tech 정체성 유지하며 차별화, Figma/Framer/Excalidraw/tldraw/Rive/Spline 시드). `spec_analyzer.py` UI_PATTERNS 에 canvas-tool 전용 2 패턴 추가 ("canvas workspace"/"design tool chrome") — canvas-workspace/ruler/snap-guide/grid-overlay/selection-handle/zoom-control/minimap/layer-panel/layer-item/layer-thumbnail/inspector-panel/property-row/toolbar-group/contextual-toolbar/asset-library/asset-card/export-panel/format-selector/keyboard-shortcut-cheatsheet 등 19개 신규 컴포넌트 매핑. 기존 9종 spec 에서 신규 term 18종 0 hit 사전 검증 — rebuild 후 9종 preview 대표 컴포넌트 회귀 0. preview.md 대표 컴포넌트 layer-panel/layer-item/inspector-panel (canvas-tool signature_keywords "layer"/"inspector"/"panel" 매칭) + 7 HEX swatch + Pretendard ko 통과. validate/lint 10종 OK, match-preset "피그마 스타일 캔버스 에디터 minimal" / "figma canvas editor design tool minimal creative" / `--app-mode canvas-tool --brand-tone minimal-tech` 모두 High Top-1. 대조군 9종 (에디토리얼 매거진 / API 레퍼런스 / fintech 대시보드 / 소셜 피드 / 한국어 SaaS / grafana observability) 모두 기존 매칭 유지 — 회귀 없음. Next+shadcn (light, ko) / raw-css (dark, ko) 어댑터 round-trip OK — primary `#804AA8` globals.css/tokens.css 반영. `tests/test_preset_matcher.py` 라벨 2건 추가, 전체 107 passed (기존 105 + 신규 2). 누적 프리셋 10종 = **P1 5종 전부 done**. | done |
| 2026-04-19 | **Phase 13-7 완료** (P2 tier 2/5, 누적 12종): `commerce--bold-confident` [tags: ecommerce, streetwear, ko, default_color_mode=light] P2 2호 프리셋. commerce app_mode 의 두 번째 프리셋 (기존 editorial-warm 1종만 있었고, bold-confident 톤은 commerce 첫 등장). marketing-landing 에 이은 bold-confident 톤 2종째. 신규 source project `projects/drop/` (Crimson #BD2E4A + Royal Purple #6C3BAA + Buttercream #F3E5AB 팔레트 — 기존 11종 프리셋 HEX 와 겹침 0, premier-league bold #E90052/#00FF85/#FFD700 회피하면서 bold-confident 정체성 유지, 젊은 streetwear/drop 정서, Nike/Supreme/Kith/Ssense/Musinsa/29cm 시드). `spec_analyzer.py` UI_PATTERNS 에 commerce 전용 3 패턴 추가 ("product catalog" / "cart and checkout" / "drop and merchandising") — product-grid/product-card/product-detail/product-gallery/product-hero-image/image-thumbnail/variant-selector/size-selector/color-swatch-selector/add-to-cart-button/quick-view-modal/wishlist-toggle/price-tag/original-price-strikethrough/discount-badge/cross-sell-grid/category-pill/filter-sidebar/sort-dropdown/cart-drawer/cart-item/cart-summary/quantity-stepper/checkout-step/checkout-step-progress/address-form/payment-form/promo-code-input/order-summary/empty-cart-state/drop-banner/countdown-timer/lookbook-hero/featured-category-tile/hero-banner 등 35개 신규 컴포넌트 매핑. 기존 11종 spec 에서 신규 term 0 hit 사전 검증 — rebuild 후 11종 preview 대표 컴포넌트 drift 0. preview.md 대표 컴포넌트 product-detail / quick-view-modal / product-grid (commerce signature_keywords "product"/"detail"/"grid" 매칭) + 7 HEX swatch (Core 3 + Semantic 4) + Pretendard ko 통과. validate/lint 12종 OK, match-preset "스트리트웨어 커머스 드롭 bold 강렬 쇼핑몰" / "bold streetwear drop ecommerce shopping high-contrast" / `--app-mode commerce --brand-tone bold-confident` 모두 High Top-1. 대조군 11종 ("fashion 쇼핑몰 editorial" → commerce--editorial-warm High · "스포츠 랜딩 페이지 bold" → marketing-landing--bold-confident High · "B2B SaaS 마케팅 랜딩 미니멀" · "에디토리얼 매거진" · "API 레퍼런스 개발자 미니멀" · "fintech 대시보드 신뢰 한글" · "SRE 모니터링 alert observability" · "한국어 SaaS 대시보드" · "AI 챗봇 다크" · "소셜 피드 친근 파스텔 커뮤니티" · "피그마 캔버스 에디터 미니멀 creative") 모두 기존 Top-1 preset_id 유지 — commerce 키워드 + editorial 톤 / bold 키워드 + 랜딩 app_mode 양쪽 회귀 위험 지점 모두 정상. Next+shadcn (light, ko) / raw-css (dark, ko) 어댑터 round-trip OK — primary `#BD2E4A` globals.css/tokens.css 반영. rebuild-all-presets 12/12 OK. `tests/test_preset_matcher.py` 라벨 2건 추가, 전체 111 passed (기존 109 + 신규 2). 누적 프리셋 12종. | done |
| 2026-04-19 | **Phase 13-8 완료** (P2 tier 3/5, 누적 13종): `conversation-copilot--editorial-warm` [tags: writing, editorial, ko, default_color_mode=light] P2 3호 프리셋. conversation-copilot app_mode 의 두 번째 프리셋 (기존 minimal-tech 1종만 있었고, editorial-warm 톤은 conversation-copilot 첫 등장). editorial-warm 톤은 document-content / commerce 에 이어 3종째. 신규 source project `projects/quill/` (Marsala #964F4C primary + Moss Green #8A9A5B accent + Flax #EEDC82 surface_tint 팔레트 — 기존 12종 프리셋 HEX 와 겹침 0, signal-desk editorial-warm Ochre/Terracotta/Wheat 및 drop Crimson/Royal Purple/Buttercream 과 전면 차별화, deep warm wine + muted sage + warm paper 조합으로 editorial-warm 톤 유지하며 writing/reading-first 정체성 확보, Lex/Jasper/Sudowrite/Notion AI/Ulysses/Substack 시드). `spec_analyzer.py` UI_PATTERNS 에 writing copilot 전용 2 패턴 추가 ("writing artifact" / "conversation copilot chrome") — message-artifact/artifact-preview-panel/draft-document/outline-sidebar/revision-timeline/tone-slider/reading-mode-toggle/citation-footnote/quote-block/paragraph-block + prompt-composer/streaming-cursor/typing-indicator/inline-citation/regenerate-button/stop-generation-button/mention-chip/suggestion-card/thread-header/new-thread-button/empty-conversation-state 등 21개 신규 컴포넌트 매핑. 기존 12종 spec 에서 신규 term 20종 0 hit 사전 검증 — rebuild 후 12종 preview 대표 컴포넌트 drift 0. preview.md 대표 컴포넌트 message-artifact / prompt-composer / chat-message (conversation-copilot signature_keywords "artifact"/"prompt"/"chat"/"message" 매칭) + 7 HEX swatch (Core 3 + Semantic 4) + Pretendard ko 통과. validate/lint 13종 OK, match-preset "AI 글쓰기 코파일럿 차분 에디토리얼 editorial 한글" / "writing copilot editorial warm serif calm essay drafting" / `--app-mode conversation-copilot --brand-tone editorial-warm` 모두 High Top-1. `keywords.json` conversation-copilot 에 writing 어휘 확장 (글쓰기/에세이/뉴스레터/writing/essay/newsletter/drafting) + tags 에 writing / editorial 신규. `engine.py` tie-break 에 tier 순서 우선 (P0 > P1 > P2 > P3) 도입 — 동점 상황에서 P0 default preset 이 우선 picking 되도록 (예: 톤 신호 없는 "copilot chat dark" → conversation-copilot--minimal-tech P0 유지). 대조군 14종 ("AI 챗봇 다크" / "copilot chat dark" → minimal-tech · "에디토리얼 매거진" / "document reading blog, warm" → document-content--editorial-warm · "fashion 쇼핑몰 editorial" → commerce--editorial-warm · "스트리트웨어 드롭 커머스 bold" · "스포츠 랜딩 bold" · "B2B SaaS 마케팅 랜딩 미니멀" · "API 레퍼런스 개발자 미니멀" · "fintech 대시보드 신뢰 한글" · "SRE 모니터링 alert observability" · "한국어 SaaS 대시보드" · "소셜 피드 친근 파스텔 커뮤니티" · "피그마 캔버스 에디터 미니멀 creative") 모두 기존 Top-1 preset_id 유지 — conversation-copilot 두 톤 분기 + editorial 3종 간 app_mode 분기 회귀 없음. Next+shadcn (light, ko) / raw-css (dark, ko) 어댑터 round-trip OK — primary `#964F4C` globals.css/tokens.css 반영. rebuild-all-presets 13/13 OK. `tests/test_preset_matcher.py` 라벨 2건 추가, 전체 113 passed (기존 111 + 신규 2). 누적 프리셋 13종. | done |
| 2026-04-19 | **Phase 13-9 완료** (P2 tier 4/5, 누적 14종): `document-content--bold-confident` [tags: magazine, opinion, ko, default_color_mode=light] P2 4호 프리셋. document-content app_mode 의 세 번째 프리셋 (editorial-warm P0 + minimal-tech P1 에 이어 bold-confident 톤 첫 등장). bold-confident 톤은 marketing-landing / commerce 에 이어 3종째. 신규 source project `projects/broadside/` (Classic Blue #0F4C81 primary + Goji Berry #CC142F accent + Flame #F2552C surface_tint 팔레트 — 기존 13종 프리셋 core HEX 와 겹침 0, premier-league Vivid Pink/Spring Green/Gold 및 drop Crimson/Royal Purple/Buttercream 과 전면 차별화, Pantone Trend Blues/Reds/Oranges 조합으로 deep saturated editorial magazine cover 감성 확보, The Atlantic/New Yorker/NY Times Magazine/Vice/Pitchfork/Guardian Long Read 시드). `spec_analyzer.py` UI_PATTERNS 에 magazine/opinion long-form 전용 2 패턴 추가 ("bold editorial magazine" / "opinion long-form") — masthead/issue-header/issue-number/cover-story/opening-spread/feature-article/kicker-eyebrow/pull-quote/drop-cap/section-break/article-gallery/subscription-callout + opinion-byline/manifesto-section/feature-grid-index/archive-index/issue-archive/reading-progress-bar/credit-line 등 19개 신규 컴포넌트 매핑. 기존 13종 spec 에서 신규 term 0 hit 사전 검증 (byline-row 는 KB editorial content block 기본 컴포넌트라 별개 유지) — rebuild 후 13종 preview 대표 컴포넌트 drift 0. `feature-article` / `reading-progress-bar` role 에 signature keyword (heading-anchor / prose-block / reading-pane 등) 보강으로 preview 대표 컴포넌트가 feature-article / reading-progress-bar / article-body 로 잡혀 lattice P1 preview (article-body/prose-block/table-of-contents) 와 magazine 정체성 차별화. preview.md 7 HEX swatch (Core 3 + Semantic 4) + Pretendard ko 통과. validate/lint 14종 OK, match-preset "대담한 매거진 에디토리얼 opinion bold 강렬 한글" / "bold magazine editorial opinion zine saturated feature" / `--app-mode document-content --brand-tone bold-confident` 모두 High Top-1. `keywords.json` document-content app_mode 에 editorial/opinion/zine/long-form/longform/manifesto 및 한국어 오피니언/매니페스토/선언/롱폼/에디토리얼 확장, tags 에 magazine / opinion 신규 추가, editorial-warm brand_tone 에서 영문 "magazine" 제거 (한글 "잡지" 유지) — "editorial" substring 이 canvas-tool "editor" 에 오염되는 tie-break 문제 해결. 대조군 18종 ("에디토리얼 매거진" / "document reading blog, warm" / "calm magazine editorial serif" 모두 document-content--editorial-warm High 유지 · "API 레퍼런스 개발자 미니멀" / "technical docs reference minimal developer" → document-content--minimal-tech High 유지 · "스포츠 랜딩 페이지 bold" → marketing-landing--bold-confident · "스트리트웨어 드롭 커머스 bold" → commerce--bold-confident · "fashion 쇼핑몰 editorial" → commerce--editorial-warm · "AI 글쓰기 코파일럿 차분 editorial" → conversation-copilot--editorial-warm · "AI 챗봇 다크" / "copilot chat dark" → conversation-copilot--minimal-tech · "fintech 대시보드 신뢰" → dashboard--corporate-trust · "SRE 모니터링 alert observability" → monitoring-ops--minimal-tech · "한국어 SaaS 대시보드" → dashboard--minimal-tech · "소셜 피드 친근 파스텔 커뮤니티" → community-feed--playful-soft · "피그마 캔버스 에디터 미니멀 creative" / "figma canvas editor design tool minimal creative" → canvas-tool--minimal-tech · "B2B SaaS 마케팅 랜딩 미니멀" → marketing-landing--minimal-tech) 모두 기존 Top-1 preset_id 유지 — document-content 3종간 tone 축 분기 + bold-confident 3종간 app_mode 축 분기 회귀 없음. Next+shadcn (light, ko) / raw-css (dark, ko) 어댑터 round-trip OK — primary `#0F4C81` globals.css/tokens.css 반영. rebuild-all-presets 14/14 OK. `tests/test_preset_matcher.py` 라벨 2건 추가, 전체 115 passed (기존 113 + 신규 2). 누적 프리셋 14종. | done |
| 2026-04-20 | **Phase 14 완료** 🎯 **공개 배포 준비 done**: (14-1) plugin README 대폭 보강 — 3분 Quick Start · 카탈로그 요약 매트릭스 · 어댑터 매트릭스 · 한글 1급 지원 · 설치 후 파일 트리 · 버전 계약. (14-2) harness README 갱신 — 유도 배너 · 플러그인 vs 하네스 결정표 · 카탈로그 요약 · 메인테이너 5스텝 워크플로우 · 버전 계약 4필드 · sync 파이프라인 · Phase 진행 상태. (14-3) `scripts/build-catalog.py` stdlib only 신규 — matrix.json + manifest + preview.md 파싱 (regex + section 스캐너) → `docs/CATALOG.md` 자동 생성 (15종 · 459 lines, At a glance · Filter axes · app_mode×brand_tone 매트릭스 · P0/P1/P2 카드). `PreviewBlock` dataclass. Core HEX 스와치 (⬛/⬜ luminance). 테스트 `tests/test_build_catalog.py` 5 케이스 (parse / swatch / render / CLI), 전체 122 passed (기존 117 + 신규 5). validate/lint/rebuild 15/15 OK, sync --dry-run compatibility OK. (14-4) plugin `.claude-plugin/marketplace.json` status pre-alpha → **alpha** 승격, categories 3→5, keywords 7→22 (app_mode 8 + brand_tone 5 전부 포함), source.repository 기본값. (14-5) plugin `docs/DEMO_SCRIPTS.md` 신규 — 한국어 3 (SaaS 대시보드 / AI 글쓰기 / 패션 커머스) + 영문 3 (devtools docs / streetwear drop / SRE observability), 각 free-text → matcher Top-3 → install 명령 → 결과 파일 트리. (14-6) plugin `.github/workflows/release.yml` 신규 — tag push → version 검증 → preset_api 2차 검증 → conventional commits 노트 생성 → CHANGELOG PR → `gh release create`. `CHANGELOG.md` v0.1.0 initial. `docs/RELEASE.md` 절차 + SemVer + 롤백 + 실패 모드. 실제 tag push / public repo 전환 / marketplace add 는 사용자 수동 승인 대기. | done |
| 2026-04-20 | **Phase 13-10 완료** 🎯 **P2 tier 완료 (누적 15종)**: `dashboard--editorial-warm` [tags: editorial, publishing, ko, default_color_mode=light] P2 5호 프리셋. dashboard app_mode 의 세 번째 프리셋 (minimal-tech P0 orbit + corporate-trust P1 ledger 에 이어 editorial-warm 톤 첫 등장). editorial-warm 톤은 document-content (signal-desk) + commerce (colorfit) + conversation-copilot (quill) 에 이어 4종째. 신규 source project `projects/curator/` (Aubergine #614051 primary + Naples Yellow #FADA5E accent + Blush #F9C0C4 surface_tint 팔레트 — 기존 14종 프리셋 core HEX 와 겹침 0, signal-desk Ochre/Terracotta/Wheat 및 quill Marsala/Moss/Flax 와 완전 차별화, purple-forward deep violet-brown + creamy warm yellow + soft pink cream 조합으로 boutique newsroom / 출판사 editorial admin 색 스토리 확립, Ghost/Substack/Medium/Readwise/Notion/Buttondown 시드). `spec_analyzer.py` UI_PATTERNS 에 editorial dashboard 전용 2 패턴 추가 ("editorial curation dashboard" / "publishing workflow") — curation-queue/editorial-calendar/draft-status-pill/article-preview-pane/contributor-roster/editorial-analytics-kpi/reading-analytics-kpi/archive-shelf/tag-taxonomy-manager + publishing-pipeline/issue-planner/pipeline-stage/schedule-cell/editorial-workflow/assign-reviewer/publish-scheduler/content-status-timeline 등 17개 신규 컴포넌트 매핑. 기존 14종 spec 에서 신규 term 0 hit 사전 검증 — rebuild 후 14종 preview 대표 컴포넌트 drift 0. editorial-dashboard 컴포넌트 role 에 dashboard signature keywords (sidebar/nav/table/filter/kpi/card) 자연스럽게 포함 — preview 대표 컴포넌트가 curation-queue (6점) / archive-shelf (6점) / issue-planner (6점) 로 선정되어 dashboard--minimal-tech (sidebar-nav/stat-card/insight-card) / dashboard--corporate-trust (sidebar-nav/data-table/filter-chip) 와 완전 차별화. preview.md 7 HEX swatch (Core 3 + Semantic 4) + Pretendard ko 통과. validate/lint 15종 OK, match-preset "편집 매거진 운영 대시보드 차분한 warm 한글" / "editorial publishing dashboard newsroom curation calm warm" / `--app-mode dashboard --brand-tone editorial-warm` 모두 High Top-1. `keywords.json` dashboard app_mode 에 publishing/newsroom/curation/퍼블리싱/큐레이션/뉴스룸/편집부/편집 운영/editor-dashboard/editorial-admin/publishing dashboard 등 editorial-publishing 운영 어휘 확장 — "editor" substring 이 canvas-tool app_mode 에 "editorial" 을 오염시키던 tie-break 문제 해결 (dashboard 힛 ≥ 2 로 canvas-tool 1 힛 초과). tags 에 publishing 신규 추가 (출판/퍼블리싱/publishing/pub). 대조군 28종 ("한국어 SaaS 대시보드" → dashboard--minimal-tech · "admin panel console neutral minimal" → dashboard--minimal-tech · "fintech 대시보드 신뢰" → dashboard--corporate-trust · "에디토리얼 매거진" / "document reading blog, warm" / "calm magazine editorial serif" → document-content--editorial-warm · "대담한 매거진 opinion bold" → document-content--bold-confident · "API 레퍼런스 개발자 미니멀" → document-content--minimal-tech · "스포츠 랜딩 bold" → marketing-landing--bold-confident · "B2B SaaS 마케팅 랜딩 미니멀" → marketing-landing--minimal-tech · "스트리트웨어 드롭 커머스 bold" → commerce--bold-confident · "fashion 쇼핑몰 editorial" → commerce--editorial-warm · "AI 글쓰기 코파일럿 차분 editorial" → conversation-copilot--editorial-warm · "AI 챗봇 다크" / "copilot chat dark" → conversation-copilot--minimal-tech · "SRE 모니터링 observability" → monitoring-ops--minimal-tech · "소셜 피드 친근 파스텔" → community-feed--playful-soft · "피그마 캔버스 에디터 creative" → canvas-tool--minimal-tech) 모두 기존 Top-1 preset_id 유지 — dashboard 3종간 tone 축 분기 + editorial-warm 4종간 app_mode 축 분기 회귀 없음. Next+shadcn (light, ko) / raw-css (dark, ko) 어댑터 round-trip OK — primary `#614051` globals.css/tokens.css 반영. rebuild-all-presets 15/15 OK. `tests/test_preset_matcher.py` 라벨 2건 추가, 전체 117 passed (기존 115 + 신규 2). 누적 프리셋 15종 = **P2 5종 전부 done**. 다음 세션부터 Phase 13-11 (P3 커뮤니티 확장) 또는 Phase 14 (공개 배포 / README / 카탈로그 / 릴리스 자동화) 로 전환. | done |
| 2026-04-20 | **Phase 13-11-A 완료** 🎯 **P3 첫 프리셋 2종 self-contribution (dogfooding) + build-sources 자동화 경로 CONTRIBUTING 안내**: catalog-health priority_empty_cells top-10 #1/#2 셀을 메인테이너가 기여자 페르소나(owner=`@maintainer-dogfood`)로 합성 — `dashboard--bold-confident` (source `projects/lattice-dash/`, Ultra Violet #5F4B8B primary + Illuminating #F5DF4D accent + Creamsicle #FFD7A0 surface_tint, Retool/Appsmith/Stripe Radar/PostHog/Plausible/Mixpanel 시드 6건, 기존 15종 HEX 겹침 0 — bold-confident 3종 (premier-league Vivid Pink/Spring Green/Gold · drop Crimson/Royal Purple/Buttercream · broadside Classic Blue/Goji Berry/Flame) 과 전면 차별화, "startup admin purple + yellow activation" 정체성) + `dashboard--playful-soft` (source `projects/meadow/`, Periwinkle #8E9AF1 primary + Peach Puff #FFDAB9 accent + Mauve #E0B0FF surface_tint, Cal.com/Notion/Flo/Finch/Calm/Headspace 시드 6건, 기존 15종 HEX 겹침 0 — bloom playful-soft community-feed Coral Blush/Mint Green/Cornsilk 와 전면 차별화, "consumer wellness mindful pastel" 정체성). `spec_analyzer.py` UI_PATTERNS 에 2 패턴 신규 — "growth analytics admin" (activation-funnel/cohort-matrix/referral-widget/retention-chart/conversion-funnel/experiment-panel/goal-tracker/user-list/ticket-queue/alert-list/segment-filter/filter-bar 12개) + "wellness habit tracking" (streak-indicator/habit-calendar/wellness-score/mood-check/mood-chart/session-tracker/session-timeline/goal-grid/dashboard-card 9개). 기존 15종 spec.md 에서 신규 term 0 hit 사전 검증 — rebuild 후 회귀 0. wellness 컴포넌트 role 에 data-table/kpi-card/dashboard-card 참조 추가로 dashboard signature keyword 6/6 매칭 → preview picker 가 meadow 에서 dashboard-card/streak-indicator/habit-calendar 대표 컴포넌트 선정 (wellness 정체성 유지). lattice-dash preview 는 activation-funnel/experiment-panel/goal-tracker (growth admin 정체성). `keywords.json` dashboard app_mode 에 startup/growth/activation/retention/cohort/wellness/habit/tracking/consumer/b2c 한영 어휘 + tags 에 startup/growth/cohort/referral/consumer/wellness/habit/tracking/mindful 신규. `preset_matcher/eval.py` 라벨 50→54 (+4 — B2C 스타트업 vivid bold / startup admin bold-confident activation retention / consumer wellness habit tracker playful / soft wellness dashboard pastel) 각 High Top-1 자기 자신, 대조군 50건 회귀 0. `tests/test_preset_matcher.py` + `tests/test_build_catalog.py` 하드코딩 숫자 50→54 / 15→17 갱신. `docs/CONTRIBUTING_PRESETS.md` Step 4.5 신규 섹션 — `build-sources --preset-id` 사용법 + 도메인 화이트리스트 kind 테이블 (design-system/visual-reference/brand-guide/reference-docs/article fallback) + 시드 < 3 warning 보완 + sources.json 예시 JSON + brand_profile.seeds 문자열/객체 2가지 허용. §5.3 신규 가이드 (공공 레퍼런스 / 최소 3개 / kind 명시 / http(s) / dedup). §6 승급 조건 P3 "sources.json + seeds ≥ 3" + P2 "promote-preset --dry-run 5 gate" 명시. English Mirror Step 2·4.5 병기. 어댑터 round-trip Next+shadcn (light, ko) / raw-css (dark, ko) 4종 모두 installed — primary HEX globals.css/tokens.css 반영 확인 (#5F4B8B / #8E9AF1 / #F5DF4D / #FFDAB9). rebuild-all-presets 17/17 OK, build-sources --all --force 17/17 OK (6 시드 신규 2종 · 전체 warn 0), snapshot fixture `pytest --update-snapshots` 1회 갱신. `promote-preset dashboard--bold-confident --target P2 --dry-run` / `promote-preset dashboard--playful-soft --target P2 --dry-run` — 5 gate (validate-presets 17 OK / lint-previews clean / adapter-round-trip Next@0.1.0 + Raw@0.1.0 both installed / sources.json present strict from_tier=P3 / self-match Top-1 score=1.000 bucket=High) 모두 통과, manifest/matrix 변경 0. `scripts/build-catalog.py` 재생성 → plugin `docs/CATALOG.md` (15→17 presets, `### P3 · 2 preset(s)` 섹션 신규, credits per-preset seed index 17 entries + aggregated references 확장). **검증**: 전체 테스트 **181 → 185 passed** (+0 신규 테스트, 기존 assert 숫자 갱신만 50→54 / 15→17), validate-presets 17/17 OK, lint-previews 17/17 OK (errors=0 warnings=0), rebuild-all-presets 17/17 OK, build-sources 17/17 OK, eval-matcher **1.00 (54/54)** 유지 · confusion 공집합, snapshot regression 0건, catalog-health 17종 / 셀 커버리지 17/40 (42%) / deprecated 0 / deprecation 후보 17 / prune_eligible 0 / priority top-10 에서 2셀 제거 (top-8 출력 3번부터 시작 확인), `prune-preset dashboard--bold-confident --dry-run` → "manifest has no deprecated_at" error (안전장치 유지), `validate-community-preset.py` dashboard--bold-confident / dashboard--playful-soft 양쪽 HEX overlap 0 · 셀 중복 0 · self-match Top-1 (both `✓ all checks passed`), `check-plugin-compatibility.py` adapter drift none (Next/Raw/Vite @ 0.1.0) · preset count 17 · compatibility OK. 플러그인 레포 `docs/CATALOG.md` 만 재생성 (의도적 diff — P3 카드 2장 + credits 섹션 확장) — push/tag/커밋 미실행. 다음 묶음 후보: Phase 13-11-B (실제 외부 기여자 1명 P3 PR 접수 — PR 템플릿 workflow 실전 검증) 또는 Phase 15 최종 마감 (마켓플레이스 공개 / 첫 릴리스 tag push 준비). | done |
| 2026-04-20 | **Phase 15-4 + 15-9 완료** 🎯 **외부 P3 기여 수락 전 마지막 운영 루프 마감 — 분기별 pruning 자동화 + 라이선스·크레딧 일괄 정비**: (15-4) `preset_ops.prune_preset(preset_id, *, confirm, dry_run, presets_root, metrics_dir, snapshot_fixture_path, min_deprecated_age_days=90)` — 4단계 게이트 (a. manifest.deprecated_at 존재 / b. 90일+ 경과 / c. install+match hits 0 / d. --confirm when dry_run=False). 성공 시 `presets/<id>/` shutil.rmtree + matrix.json entry 제거 + snapshot fixture (`tests/fixtures/preset_snapshots.json`) entry 제거 — 세 곳 모두 원자적 삭제 (pruning 후 validate-presets matrix↔disk round-trip 통과). `find_prune_eligible()` 헬퍼 — catalog-health 의 prune_eligible 리스트와 동일 조건. CLI `uv run design-ontology prune-preset <id> [--confirm] [--dry-run] [--min-age-days N] [--all] [--presets-dir] [--metrics-dir] [--snapshot-fixture]` — 기본 dry-run, --all 은 eligible 일괄 처리, --min-age-days 는 테스트/분기 조정용 오버라이드. `catalog_health` 에 per-preset `deprecated_age_days` / `prune_eligible` / `prune_blocked_reasons` + 전역 `prune_eligible_count` / `prune_eligible_presets` / `prune_min_deprecated_age_days` + `## Prune Eligible` 마크다운 섹션 (## Deprecated 바로 뒤) + format_summary 한 줄. 테스트 `tests/test_preset_ops_prune.py` 9 케이스 (happy path / not deprecated / under-age / hits>0 / missing --confirm / dry-run 무변화 / min-age=0 override / find_prune_eligible aged vs under-age / catalog_health 통합). (15-9) `preset_ops.build_sources_json(preset_id, *, presets_root, projects_root, force, write)` — brand_profile.seeds (list[str] or list[dict]) + visual_reference.source_references + spec.md markdown 링크 (regex `\[text\](url)`) → dedup + 도메인 화이트리스트 기반 kind 추론 (design-system: linear.app/stripe.com/vercel.com/shadcn/material.io 등 / visual-reference: figma.com/framer.com/dribbble.com/pinterest.com 등 / brand-guide: brand.* 서브도메인 / reference-docs: docs.stripe.com/developer.mozilla.org 등 / 미매칭은 article fallback) → sources.json 구조체 (preset_id/source_project/seeds[]/pretendard_font_license/created_at). `build_sources_for_all()` 일괄 헬퍼. CLI `uv run design-ontology build-sources [--preset-id <id>] [--all] [--force] [--projects-root projects] [--presets-dir]` — 시드 < 3 일 경우 warning (fatal 아님), kind 분포 + 누적 요약. 15종 프로젝트 `brand_profile.json` 에 `seeds` 필드 일괄 신규 추가 — orbit (Linear/Height/Notion) · signal-desk (Ghost Design/Medium Design/NYT Spotlight/Readwise) · glacier (Anthropic/Claude/ChatGPT) · colorfit (Musinsa/29CM/SSENSE) · premier-league (Premier League/FIFA/NBA) · ledger (Stripe/Brex/Mercury/Ramp) · pulse (Grafana/Datadog/Honeycomb/Prometheus) · lattice (Linear Docs/Stripe Docs/Vercel Docs/MDN) · bloom (Threads/Bluesky/Mastodon/Are.na/Tumblr) · atelier (Figma/Framer/Excalidraw/tldraw/Rive/Spline) · beacon (Linear/Vercel/Stripe/Railway/Supabase) · drop (Nike/Supreme/Kith/SSENSE/Musinsa/29CM) · quill (Lex/Jasper/Sudowrite/Notion AI/Ulysses/Substack) · broadside (Atlantic/New Yorker/NYT Magazine/Vice/Pitchfork/Guardian) · curator (Ghost/Substack/Medium/Readwise/Notion/Buttondown). `build-sources --all --force` 로 15/15 sources.json 생성 (3~6 시드/건, 전부 ≥ 3 시드 warning 0). 신규 스키마 `schemas/preset_sources.schema.json` (draft/simple — 커뮤니티 기여 부담 최소화). preset_validator 에 sources.json 존재 시 구조 검증 (preset_id/source_project/seeds[]/pretendard_font_license/created_at 필수 + 각 seed url/kind/title 필수 + url http(s):// 시작). Pretendard SIL OFL 1.1 고지 완전성 정비 — (a) `adapters/base.py._pretendard_license` 에 "재배포 시 이 고지 유지 필수 (OFL §2)" 한글/영문 문구 추가, (b) plugin `LICENSE-FONTS` 전면 재작성 (Korean + English 병기, 원 제작자 · 라이선스 · 고지 유지 의무 · 상표권 · 번들 정책 · 재배포 체크리스트), (c) plugin README License 섹션 한국어 + 영문 병기 + `scripts.sil.org/OFL` 링크 + sources.json 참조 명시, (d) harness README "플러그인 배포" 섹션에 Pretendard 런타임 fetch + OFL §2 한 줄 추가. `scripts/build-catalog.py` 에 `## KB Sources & Credits` 섹션 자동 생성 — `_render_credits_section()` + `_load_sources()` 헬퍼, per-preset seed index 테이블 (seeds 개수 + kind 분포 + sources.json 링크) + aggregated references 테이블 (URL → referenced presets, 공유 시드는 "N+ presets" 라벨) + bundled fonts subsection (Pretendard/Inter/JetBrains Mono 각 SIL OFL 1.1 링크). plugin `docs/CATALOG.md` 재생성 → 크레딧 섹션 추가된 의도적 diff. **검증**: 전체 테스트 **172 → 181 passed** (+9 prune), validate-presets 15/15 OK (sources.json 스키마 체크 포함), lint-previews 15/15 OK, rebuild-all-presets 15/15 OK + build-sources --all --force 후 snapshot fixture `pytest --update-snapshots` 로 1회 갱신 (sources.json 이 content_hash 에 포함되는 의도적 drift — 이후 회귀 0), eval-matcher **1.00 (50/50)** 유지, snapshot regression 0건, catalog-health 15종 / 38% coverage / deprecated 0 / deprecation 후보 15 / prune_eligible 0 (deprecated 없으므로). 안전장치 스모크: `prune-preset commerce--bold-confident --dry-run` → "not deprecated" error → `deprecate-preset` 후 → `prune-preset --dry-run` → "age=0d<90d, 89d remaining" error → `--min-age-days 0` 로 dry-run pass 확인 (파일 변경 0) → manifest deprecation 필드 3종 복구 → snapshot 회귀 0. `check-plugin-compatibility.py` adapter versions 3종 Adapter drift none + compatibility OK. `validate-community-preset.py dashboard--minimal-tech` self-test pass (기존 HEX overlap warning은 예상 — 같은 source 공유 프리셋 간 core palette 겹침). 플러그인 레포 수정: `LICENSE-FONTS` 전면 재작성 + README License 섹션 + `docs/CATALOG.md` (크레딧 섹션 추가) — push/tag/커밋 미실행. 다음 묶음 후보: Phase 13-11-A (실제 P3 첫 프리셋 2종 dogfooding — build-sources 자동화 경로를 CONTRIBUTING_PRESETS.md 에 안내) 또는 Phase 15 최종 마감 (마켓플레이스 공개 / 첫 릴리스 tag push 준비). | done |
| 2026-04-20 | **Phase 15-2 + 15-3 + 15-7 완료** 🎯 **외부 P3 기여 수락 전 라이프사이클 조작 도구 완성**: (15-2) `preset_ops.promote_preset(preset_id, target_tier, *, dry_run, presets_root)` — 5단계 게이트 (validate-presets / lint-previews / adapter round-trip Next+Raw / sources.json / self-match Top-1) + manifest 에 `tier` / `promoted_at` / `promoted_from` 업데이트 + matrix.json tier 동기화. CLI `uv run design-ontology promote-preset <id> [--target] [--dry-run]` — 실패 시 exit 1, dry-run 은 체크 실행하되 파일 변경 없음. sources.json gate 는 `from_tier == "P3"` 일 때만 strict — 기존 15종 legacy 승급은 warning. (15-3) `preset_ops.deprecate_preset(preset_id, *, reason, replacement, force)` — manifest 에 `deprecated_at` / `deprecation_reason` / `deprecated_replacement` 기록. reason 은 `zero_hits | version_lag | snapshot_drift | owner_abandoned | manual` enum + `manual:<자유텍스트>` 패턴. CLI `uv run design-ontology deprecate-preset <id> --reason <reason> [--replacement <id>] [--force]`. `match_presets(..., include_deprecated=False)` 기본값 — deprecated 프리셋 자동 숨김, `MatchResult.deprecated` / `deprecated_replacement` + rationale "deprecated (reason), 대체: <id>" 주입 + 결과 라벨 `🗑️`. CLI `match-preset --include-deprecated` 플래그 추가. `eval.py.run_eval()` + `scripts/validate-community-preset.py` 는 `include_deprecated=True` 로 호출해 50/50 라벨 라운드-트립 유지. schemas/preset_manifest.schema.json 확장 (promoted_at/promoted_from/deprecated_at/deprecation_reason/deprecated_replacement 5 필드 + regex pattern). preset_validator 에 deprecation 필드 내부 일관성 검사 (reason enum+manual prefix / replacement 가 실재하는 preset / self-reference 금지). catalog_health 에 `deprecated_count` / `deprecated_presets` + `## Deprecated` 섹션 분리 + 이미 deprecated 된 프리셋은 `deprecation_candidates` 에서 제외 + Per-Preset Metrics 에 🗑️ 마커. (15-7) `preset_validator.validate_all(..., adapter_versions=...)` — 각 preset `adapter_compatibility[<adapter>]` range 가 해당 어댑터의 `StackAdapter.version` (0.1.0) 을 포함하는지 교차 검증 — 불포함 시 `adapter '<id>' current=X.Y.Z outside range <range>` error. `scripts/check-plugin-compatibility.py` 리포트에 `Adapter drift:` 섹션 추가 (없으면 "none", 있으면 위반 라인 + VIOLATIONS 합산). **검증**: 전체 테스트 **156 → 172 passed** (+6 promote · +6 deprecate · +4 validator). validate-presets 15/15 OK, lint-previews 15/15 OK, rebuild-all-presets 15/15 OK (snapshot fixture 회귀 0), eval-matcher **1.00 (50/50)** 유지, snapshot regression 0건. `uv run design-ontology promote-preset dashboard--corporate-trust --target P0 --dry-run` → P1→P0 모든 게이트 통과, 파일 변경 없음 확인. `uv run design-ontology deprecate-preset dashboard--minimal-tech --reason "manual:smoke" --force` → `match-preset "한국어 SaaS 대시보드"` 에서 dashboard--minimal-tech 제외 + `--include-deprecated` 로 `🗑️ deprecated (manual:smoke)` rationale 노출 확인 후 manifest 3 필드 제거로 원상 복구, snapshot 회귀 0. `scripts/check-plugin-compatibility.py` adapter versions 3종 (Next/Raw/Vite @ 0.1.0) Adapter drift none. validate-community-preset.py dashboard--minimal-tech self-test pass. build-catalog → plugin `docs/CATALOG.md` diff 0. catalog-health 15종 / 38% coverage / deprecated 0건 / deprecation 후보 15건. 플러그인 레포는 이번 묶음에서 소스 수정 없음 (build-catalog 재생성 byte-identical). 다음 묶음 후보: Phase 13-11-A (실제 P3 첫 프리셋 2종 dogfooding) / Phase 15-4 (분기별 pruning 자동화) / Phase 15-9 (라이선스/크레딧 정비). | done |
| 2026-04-20 | **Phase 15-1 + 15-5 + 15-8 완료** 🎯 **외부 P3 기여 수락 전 운영 루프 완성**: (15-1) `design_ontology_harness/catalog_health.py` stdlib only 신규 — `compute_health()` / `format_markdown()` / `format_summary()`, 프리셋별 (tier·app_mode·brand_tone·tags·owner·generated_by_harness_version·version_drift_minor·content_hash·last_rebuilt_at·preview_lint_status·install_hits·match_hits·snapshot_drift·deprecation_reasons) + 전체 (tier 분포·셀 커버리지 8×5=40·priority empty cells top-10·deprecation 후보·snapshot_drift_count) 지표 집계. CLI `uv run design-ontology catalog-health [--json] [--output] [--metrics-dir] [--snapshot-fixture]` — 기본 `presets/CATALOG_HEALTH.md` 자동 출력 + stdout 6~12줄 요약. version_drift 는 pyproject.toml `[project] version` 동적 로딩 (하드코딩 없음). `presets/.metrics/{install_hits,match_hits}.json` scaffold 빈 dict + README (수동 입력 원칙, Phase 15-4 pruning 입력). preset_validator iteration 에 hidden 디렉토리 (`.metrics`) 제외 필터 추가. (15-5) `tests/test_preset_snapshots.py` + `tests/conftest.py --update-snapshots` 플래그 + `tests/fixtures/preset_snapshots.json` 15 entries 초기 시드 (build-preset 출력). drift 발견 시 안내 문구 + `--update-snapshots` 갱신 경로. catalog_health 와 연동 — snapshot fixture vs 현재 manifest.content_hash 비교 → 프리셋별 `snapshot_drift: bool` + 전역 카운트. drift 시뮬레이션 (sha256:DRIFT 강제 주입) → 테스트 실패 + 안내 출력 확인 후 원상 복구. (15-8) plugin `.github/ISSUE_TEMPLATE/` 3종 yml + config.yml — preset-feedback (preset_id dropdown 15 + use_case/problem/expected) · new-preset-request (app_mode × brand_tone dropdown + references/ko 필요/기여 가능 여부) · bug-report (reproduction/expected/actual/env yaml/logs text). config.yml `blank_issues_enabled: false` + contact_links (CONTRIBUTING_PRESETS · Discussions placeholder). plugin README 하단 "피드백 & 이슈" 섹션 (한국어 primary + 영문 병기 표). harness README 상단 배너 한 줄 추가. **검증**: 전체 테스트 **149 → 156 passed** (+6 catalog_health · +1 snapshot), validate-presets 15/15 OK, lint-previews 15/15 OK, rebuild-all-presets 15/15 OK (snapshot fixture 회귀 0), eval-matcher **1.00 (50/50)**, validate-community-preset.py self-test pass, build-catalog → plugin `docs/CATALOG.md` diff 0, catalog-health 첫 실행 → 15종 / 38% coverage / 15 deprecation 후보 (전부 install·match 0 hit, 정상). 플러그인 레포 (.github/ISSUE_TEMPLATE/ + README) 수정했지만 사용자 지시대로 push/tag/커밋 실행은 미수행. 다음 묶음 후보: Phase 15-2 + 15-3 + 15-7 (라이프사이클 조작 도구 — promote/deprecate/adapter 호환성 게이트). | done |
| 2026-04-20 | **Phase 13-12 + 15-6 완료** 🎯 **외부 P3 기여 수락 전 내부 품질 선방어**: (13-12) `docs/CONTRIBUTING_PRESETS.md` 신규 — 한국어 primary + 영문 mirror, 5단계 절차, axis 선택 가이드, top-10 빈 셀, HEX/셀 중복 체크 절차, 승급/오너십/deprecation 정책. `scripts/validate-community-preset.py` stdlib only 신규 — preset_validator + preview_linter 재사용 + HEX 3종 겹침 warning (>=2) + 셀 중복 warning (P0/P1/P2 기존) + self-match Top-1 error. CLI `--preset-id` / `--diff-mode` (git diff 기반 CI 자동 감지). `tests/test_validate_community_preset.py` 6 케이스 (pass / hex 중복 / 셀 중복 / 필수 파일 누락 / self-match 실패 / CLI exit code) 전부 통과. plugin `.github/PULL_REQUEST_TEMPLATE/community-preset.md` 신규 — checkbox (axis/KB 시드/HEX 중복/self-match/preview.md/owner 6개월 유지/브랜드 IP 선언). plugin `.github/workflows/validate.yml` `community-preset-check` job 추가 — PR 에서 신규 preset manifest 감지 시 harness 레포 clone → 스크립트 실행. (15-6) 라벨 데이터 30 → 50 건 확장, canonical 위치를 `design_ontology_harness/preset_matcher/eval.py` 로 이관 (tests 는 import), threshold 80→85% 상향, `run_eval()` + `EvalResult` + confusion_pairs top-5 + CLI `eval-matcher [--verbose]` 추가. 현재 accuracy **1.00 (50/50)**, confusion 공집합 — 튜닝 불필요, 기존 30건 전부 Top-1 유지, 회귀 제로. 전체 테스트 **122 → 149 passed** (+27), validate-presets 15/15 OK, lint-previews 15/15 OK, rebuild-all-presets 15/15 OK, eval-matcher 1.00, validate-community-preset.py self-test OK (기존 프리셋은 예상대로 HEX overlap warning — 같은 source 기반 프리셋끼리 core palette 공유), build-catalog.py 재생성 → plugin `docs/CATALOG.md` diff 0. plugin 레포 파일도 수정 (PR 템플릿 + validate.yml) 하지만 사용자 지시대로 push/tag/커밋 실행은 미수행. 다음 세션부터 외부 P3 기여 수락 가능. | done |
| 2026-04-19 | **Phase 13-6 완료** 🎯 **P2 tier 진입 (누적 11종)**: `marketing-landing--minimal-tech` [tags: saas, devtools, ko, default_color_mode=light] P2 1호 프리셋. marketing-landing app_mode 의 두 번째 프리셋 (기존 bold-confident 1종만 있었고, minimal-tech 톤은 첫 등장). 신규 source project `projects/beacon/` (Teal Blue #01889F + Goldenrod #DAA520 + Powder Blue #B0E0E6 팔레트 — 기존 minimal-tech 5종 Navy #000080 / Azure #007FFF / Iris Violet #5A4FCF / Cobalt Violet #804AA8 / Prussian Blue #003153 과 HEX 겹침 0, cool teal primary + restrained warm gold CTA accent + 파스텔 powder-blue neutral hero surface 조합으로 minimal-tech 정체성 유지하면서 B2B/SaaS 마케팅 어휘 차별화, Linear/Vercel/Stripe/Railway/Supabase 시드). `spec_analyzer.py` 확장 없음 — 기존 marketing-landing 패턴 9종 (hero section / feature grid / social proof / testimonial / faq accordion / landing cta section / site footer / site header / pricing and plans) 으로 충분히 매칭됐음 (hero/pricing/cta/testimonial/feature/footer 어휘 전부 detection). preview.md 대표 컴포넌트 hero-cta-group / primary-button / hero-container (marketing-landing signature_keywords "hero"/"cta" 매칭) + 7 HEX swatch + Pretendard ko 통과. validate/lint 11종 OK, match-preset "B2B SaaS 마케팅 랜딩 미니멀 깔끔" / "minimal saas landing page hero pricing clean" / `--app-mode marketing-landing --brand-tone minimal-tech` 모두 High Top-1. 대조군 10종 (스포츠 랜딩 bold / 에디토리얼 매거진 / API 레퍼런스 / fintech 대시보드 / 한국어 SaaS / AI 챗봇 / 소셜 피드 / 피그마 캔버스 / fashion 쇼핑몰 / SRE 모니터링) 모두 기존 Top-1 preset_id 유지 — saas 태그 부여했음에도 "한국어 SaaS 대시보드" 는 dashboard--minimal-tech Top-1 유지 (app_mode 축 가중치 0.5 가 dominant). Next+shadcn (light, ko) / raw-css (dark, ko) 어댑터 round-trip OK — primary `#01889F` globals.css/tokens.css 반영. `tests/test_preset_matcher.py` 라벨 2건 추가, 전체 109 passed (기존 107 + 신규 2). | done |
| 2026-04-21 | **Phase 13-11-C 완료** 🎯 **공개 홍보 전 운영 SOP 수립 + 가상 기여자 2명 dogfood + Q2 리허설 + 마켓플레이스 체크리스트 (누적 20종, P3 · 5)**: (C-1) 신규 `docs/MAINTAINER_REVIEW_SOP.md` (한/영) — 10 단계 리뷰 절차 (a. 자동 체크 30 s / b. 기여자 프로필 2 m / c. 브랜드 IP 5 m / d. HEX + 셀 중복 3 m / e. preview.md 육안 2 m / f. self-match cross-validate 2 m / g. 소스 구조 1 m / h. 병합 + rebuild + matrix + plugin CATALOG 5 m / i. owner 통지 1 m / j. 실패 5 시나리오) + 두 PR 동시 접수 처리 + 경계 패턴 + 편의 스크립트 로드맵 + 실측 시간 §11. owner_since 1급 필드 승격은 Phase 16 으로 유예 (manifest.generated_at 근사치 + PR 댓글로 충분). (C-2) 가상 기여자 2명 end-to-end — `@bob-external` `marketing-landing--editorial-warm` (source `projects/loom/`, Ochre Yellow #CB9D06 + Rust #B7410E + Wheat #F5DEB3 — editorial-warm 4종 cream surface 공통 톤 유지하되 primary/accent 차별화, Stratechery/Ghost/Every/Substack/The Verge 5 시드) + `@carol-external` `conversation-copilot--corporate-trust` (source `projects/mercer/`, Super Sonic #0071A8 + Copper #B87333 + Powder Blue #B0E0E6 — ledger Prussian Blue/Bronze Gold/Ice Blue corporate-trust 와 전면 차별화, ChatGPT Enterprise/Anthropic Enterprise/Stripe Dialog/Salesforce Einstein/Intercom Fin 5 시드). `preset_matcher/keywords.json` hotfix — marketing-landing 14 (퍼블리셔/publisher/뉴스레터 랜딩/publisher landing/subscribe landing 등) · conversation-copilot 7 (엔터프라이즈/regulatory chatbot) · corporate-trust 9 (enterprise/compliance/audit/regulated) · tags 3 (publisher/enterprise/compliance) = 33 신규. bob 초기 self-match 2/3 실패 (editor substring canvas-tool 오염 + alphabetical tie-break) → hotfix 후 3/3 High, carol 3/3 High, 대조군 12종 회귀 0. `preset_matcher/eval.py` 라벨 58 → 66 (+8 bob/carol 각 4) 100% Top-1 유지. SOP §11 에 실측 관찰점 5건 기록 (keywords 튜닝 필수 · HEX 1 겹침 1분 내 판정 · preview 대표 컴포넌트 오염 · matrix.json auto-upsert 로 conflict 불필요 · post-merge 9 단계 실측). (C-3) 신규 `docs/CATALOG_HEALTH_2026Q2.md` 리허설 발간 — 분기 Q1말→Q2 (프리셋 15→20 / P3 0→5 / coverage 38%→50% / eval 50→66 / deprecation 후보 15→20) + 신규 접수 5종 이력 + deprecation 후보 전수 zero_hits 원인 (install_hits/match_hits 측정 파이프라인 부재) + priority top-5 빈 셀 + Q3 P3→P2 승급 계획 5종 + 측정 파이프라인 Phase 16 유예 결정 + catalog-health CI 제안 + 관찰점 4 + Q3 액션 아이템 6. 신규 `.github/workflows/catalog-health.yml` harness 측 (월 09:00 UTC cron + workflow_dispatch, `uv sync` → catalog-health → diff 있으면 peter-evans/create-pull-request@v6 로 PR 자동 생성, contents:write + pull-requests:write 권한). workflow 실행은 사용자 승인 대기. (C-4) 신규 `docs/MARKETPLACE_LAUNCH_CHECKLIST.md` 15 항목 (라이선스 · Quick Start · validate.yml 30일 · 20 presets validator · version 3-way · CATALOG.md 20 카드 · DEMO_SCRIPTS 재검증 · release.yml 시뮬레이션 · 이슈 템플릿 · CoC · SLA · marketplace status · Pretendard · 보안 스캔 · 후폭풍) + D-day 실행 순서 부록. 현재 상태 9 통과/5 경고/1 미완 (CoC). (C-4-b) 2 항목 즉시 실행 — 신규 `scripts/check-version-consistency.py` (stdlib only, plugin.json/marketplace.json/CHANGELOG 3-way) → 3-way match on **0.1.0**, `validate-community-preset.py` 20종 일괄 → 20/20 errors=0 (18 all checks passed + 2 warnings-only 예상 glacier/orbit source 공유 기존 overlap), 결과 `tmp/community-validator-report-2026-04-21.txt`. **검증**: 전체 테스트 **189 → 197 passed** (+0 신규 테스트, eval 58→66 · test_preset_matcher 58→66 · test_build_catalog 18→20 · snapshot fixture 20 entries 갱신), validate-presets 20/20 OK, lint-previews 20/20 OK (errors=0 warnings=0), rebuild-all-presets 20/20 OK, build-sources --all --force 20/20 OK (전부 seeds ≥ 3 warn 0), eval-matcher **1.00 (66/66)** confusion 공집합, snapshot regression 0건, catalog-health 20종 / 셀 커버리지 20/40 (50%) / deprecated 0 / deprecation 후보 20 / prune_eligible 0 / priority top-5 (commerce--minimal-tech #3 · marketing-landing--playful-soft #6 · document-content--corporate-trust #8 · monitoring-ops--corporate-trust #9 · canvas-tool--bold-confident #10 — loom #2 · mercer #7 자리 채워서 top-10 에서 2셀 제거 확인), validate-community-preset.py 20종 일괄 20/20 통과, check-plugin-compatibility.py adapter drift none + preset count 18→20 compatibility OK, check-version-consistency.py 3-way match 0.1.0. promote-preset dry-run `marketing-landing--editorial-warm --target P2` + `conversation-copilot--corporate-trust --target P2` 양쪽 5 gate (validate / lint / adapter round-trip Next@0.1.0+Raw@0.1.0 both installed / sources.json strict from_tier=P3 / self-match Top-1 score=1.000 bucket=High) 모두 통과, manifest/matrix 변경 0. scripts/build-catalog.py 재생성 → plugin `docs/CATALOG.md` (18→20 presets, P3 · 5 preset(s) 섹션 확장, credits loom+mercer 카드 + 10 시드 index 추가) — push/tag/커밋 미실행. 다음 묶음 후보: Phase 13-11-D (실제 GitHub PR 1–2건 수집 대기 — 공개 홍보 이후 외부 기여자 실수요 접수 · 완전 수동 큐레이션 + 실측 metric 시작) / Phase 15 최종 마감 (마켓플레이스 public 전환 + v0.1.0 tag push + GA 확정 + release.yml 첫 실행) / Phase 16 (install_hits/match_hits 측정 파이프라인 + Q3 catalog-health 실측 발간 + owner_since 1급 필드 schema 1.0.1 minor bump). | done |
