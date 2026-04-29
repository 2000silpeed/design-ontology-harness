# Marketplace Launch Checklist — design-ontology-plugin 공개 전 필수 점검

> **대상**: `design-ontology-plugin` 을 Claude Code 공개 마켓플레이스에 `alpha` → `beta`/`stable` 로 승격하기 전 통과해야 하는 15 항목.
> **발간**: 2026-04-21 (Phase 13-11-C-4 리허설) · 실제 공개 전 메인테이너 수동 재확인 필수.
> **기반**: [`PLUGIN_PLAN.md`](./PLUGIN_PLAN.md) §12 완료 정의 · [`docs/RELEASE.md`](https://github.com/2000silpeed/design-ontology-plugin/blob/main/docs/RELEASE.md)
> **공개 전제**: Phase 13-11-C 시점 harness `0.1.0` + plugin `0.1.0` + 20 presets (P0×5 · P1×5 · P2×5 · P3×5) + validate.yml + release.yml 전부 green.

---

## 요약 상태판 (2026-04-29 기준)

| # | 항목 | 상태 | 실행 |
|:---:|---|:---:|---|
| 1 | 라이선스 MIT + OFL | ✅ | 파일 존재 확인 완료 |
| 2 | Plugin README 3 분 Quick Start | ✅ | 20종 카탈로그 기준 로컬 문서 재검증 완료 |
| 3 | validate.yml workflow green | ✅ | public repo run `25115751357` success |
| 4 | 20 presets validate-community-preset pass | ✅ | 13-11-C-4-b 에서 일괄 실행 완료 |
| 5 | plugin/marketplace/CHANGELOG version 정합성 | ✅ | 13-11-C-4-b 에서 자동 검증 완료 |
| 6 | CATALOG.md 20 카드 렌더 완결 | ✅ | scripts/build-catalog.py 재생성 후 육안 확인 |
| 7 | DEMO_SCRIPTS.md 시나리오 재검증 | ✅ | `scripts/verify-demo-scripts.py` 6/6 Top-1 High |
| 8 | release.yml 실제 실행 | ✅ | `v0.1.0` tag push → run `25115752943` success + GitHub Release 생성 |
| 9 | 이슈 템플릿 3종 존재 | ✅ | preset-feedback / new-preset-request / bug-report |
| 10 | CODE_OF_CONDUCT.md 추가 | ✅ | harness/plugin 양쪽 mirror 완료 |
| 11 | response SLA 명시 | ✅ | plugin README 2주/4주 SLA 명시 |
| 12 | marketplace.json.status alpha → beta 결정 | ⏳ | alpha 유지, 공개 1주 후 beta 판단 |
| 13 | Pretendard 런타임 fetch + OFL 고지 | ✅ | woff2 미커밋 정책 + LICENSE-FONTS 고지 |
| 14 | 보안 스캔 (secret 누출 · hardcoded token) | ✅ | `scripts/security-scan-launch.py` high-confidence scan 통과 |
| 15 | 첫 1 주 후폭풍 대응 플랜 | ✅ | triage cadence + FAQ/Discussions 시작 정책 문서화 |

**통과 14 종 · 사후 판단 대기 1 종**. 공개 GitHub run history 와 `v0.1.0` tag/release 는 2026-04-29 에 실제 실행 완료했습니다. 남은 항목은 공개 1주 후 `alpha → beta` 판단입니다.

---

## 1. 라이선스 — MIT (코드) + SIL OFL 1.1 (Pretendard)

- [x] plugin 레포 루트 `LICENSE` (MIT, Copyright design-ontology contributors) 존재
- [x] plugin 레포 루트 `LICENSE-FONTS` (SIL OFL 1.1 + OFL §2 재배포 고지) 존재
- [x] plugin README License 섹션 한국어 + 영문 병기 + `scripts.sil.org/OFL` 링크
- [x] harness README "플러그인 배포" 섹션에 OFL §2 한 줄 명시
- [ ] 공개 시점 `LICENSE` 의 `<YEAR>` 값 자동 검증 (현재 2026 고정) — 매년 1월 수동 업데이트

**스크립트 점검**:
```bash
PLUGIN_REPO=${PLUGIN_REPO:-../design-ontology-plugin}
test -f "$PLUGIN_REPO/LICENSE"
test -f "$PLUGIN_REPO/LICENSE-FONTS"
grep -q "MIT" "$PLUGIN_REPO/LICENSE"
grep -q "SIL Open Font License" "$PLUGIN_REPO/LICENSE-FONTS"
```

## 2. Plugin README 3 분 Quick Start 로컬 재검증

- [x] README 예시 명령어가 실제 CLI 과 일치 (오타 0)
- [x] 설치 후 생성 파일 트리 (README 예시) 와 어댑터 산출물 정책 일치
- [x] 한국어 UI 옵션 (`/design-start` 중 한글 Y) 선택 시 Pretendard fetch script + OFL notice 가 생성됨
- [x] 로컬 path marketplace 기준으로 Quick Start 문서 재검증
- [x] 공개 URL 기준 신규 환경 검증 — [`2000silpeed/design-ontology-plugin`](https://github.com/2000silpeed/design-ontology-plugin) public repo 접근 확인

**실행 제약**: 공개 레포가 없는 현 상태에서는 로컬 path marketplace (`file:///...`) 로 대체 검증. 공개 후 URL 기반 재검증 필수.

## 3. validate.yml workflow 최근 30 일 main green

- [x] `.github/workflows/validate.yml` 2 job (`validate-presets` + `community-preset-check`) 존재
- [x] 최근 30 일 main 브랜치 모든 커밋에서 green — `gh run list --repo 2000silpeed/design-ontology-plugin --branch main --limit 30`
- [x] 실패 run 없음

**실행 결과**: public repo [`2000silpeed/design-ontology-plugin`](https://github.com/2000silpeed/design-ontology-plugin) 생성 후 push run `25115751357` success. Node 20 deprecation annotation 만 있고 job failure 는 없음.

## 4. 20 presets 모두 validate-community-preset.py 통과

- [x] Phase 13-11-C-4-b 에서 일괄 실행 (`scripts/run-community-validator-all.sh`) — 20/20 pass
- [x] warnings 는 HEX 1 겹침 3 건 (commerce--editorial-warm / loom Wheat / mercer Powder Blue) 외 없음
- [x] errors 0

**결과 보관 위치**: [`tmp/community-validator-report-YYYY-MM-DD.txt`](../tmp/) (git-ignored)

## 5. plugin.json.version ↔ marketplace.json.version ↔ CHANGELOG 상단 정합성

- [x] Phase 13-11-C-4-b `scripts/check-version-consistency.py` 실행 → 3-way `0.1.0` 일치
- [x] 태그 push 전 로컬 재실행 — `scripts/check-version-consistency.py`
- [x] 실제 `gh release create` 직전 public 레포에서 재실행

## 6. docs/CATALOG.md 20 카드 렌더 완결성

- [x] scripts/build-catalog.py 재생성 → 20 presets, P3 · 5 preset(s) 섹션 렌더
- [x] 각 카드에 Core HEX 스와치 / Typography / 대표 컴포넌트 top-3 / locale_pairings / links 존재
- [x] At a glance 및 app_mode × brand_tone 매트릭스 자동 갱신

**스크립트 점검**:
```bash
PLUGIN_REPO=${PLUGIN_REPO:-../design-ontology-plugin}
grep -c "^#### " "$PLUGIN_REPO/docs/CATALOG.md"   # 기대값 ≥ 20
grep -c "Core HEX" "$PLUGIN_REPO/docs/CATALOG.md" # 기대값 ≥ 18 (color_reference 설정된 것만)
```

## 7. DEMO_SCRIPTS.md 6 시나리오 (3 한국어 + 3 영문) 재검증

- [x] 각 free-text/질문형 입력 → 예상 Top-1 과 실제 matcher 결과 비교
- [x] bucket 등급 (High / Medium / Low) 일치
- [x] `monitoring-ops` 단일 톤 보강으로 SRE observability demo High 매칭 확인

**실행**: `scripts/verify-demo-scripts.py --demo-path ../design-ontology-plugin/docs/DEMO_SCRIPTS.md`

## 8. release.yml 실제 실행

- [x] `.github/workflows/release.yml` 존재 + `workflow_dispatch` 지원
- [x] `git tag -a v0.1.0` → push → workflow 발동 확인
- [x] CHANGELOG 자동 PR 생성 경로 확인 — 기존 `CHANGELOG.md` 에 `v0.1.0` 이 있어 변경 없음
- [x] `gh release create` 실제 호출 + notes 포매팅 확인

**실행 결과**: release run `25115752943` success, GitHub Release [`v0.1.0`](https://github.com/2000silpeed/design-ontology-plugin/releases/tag/v0.1.0) 생성 완료.

## 9. 이슈 템플릿 3 종

- [x] `.github/ISSUE_TEMPLATE/preset-feedback.yml` — preset_id dropdown 20 종 동기화 완료
- [x] `.github/ISSUE_TEMPLATE/new-preset-request.yml` — app_mode × brand_tone 드롭다운
- [x] `.github/ISSUE_TEMPLATE/bug-report.yml` — reproduction / expected / actual
- [x] `.github/ISSUE_TEMPLATE/config.yml` — `blank_issues_enabled: false` + contact_links
- [x] preset-feedback dropdown 의 preset_id 목록이 최신 20 종과 동기화 — `scripts/sync-issue-template-presets.py --check`

## 10. Code of Conduct — Contributor Covenant v2.1

- [x] plugin 레포에 `CODE_OF_CONDUCT.md` (Contributor Covenant v2.1 취지, 한국어 + 영문) 추가
- [x] harness 레포에 같은 파일 mirror
- [x] plugin README 의 "Code of Conduct" 섹션에 CoC 링크
- [x] 위반 제보 채널 명시 (plugin issue tracker, 민감한 제보는 비공개 채널 요청)

**템플릿**: https://www.contributor-covenant.org/version/2/1/code_of_conduct/

## 11. Response SLA

- [x] plugin README 에 **"이슈/PR 2 주 이내 1차 반응, 4 주 이내 리뷰 완료"** 명시
- [x] 메인테이너 부재 시 지연될 수 있음을 명시

## 12. marketplace.json.status 전환

- [x] 현재 `status: "alpha"` — 13-11-C 기준 적절
- [ ] **공개 1 주 후** 유저 접수가 0 건이 아닐 때 `beta` 로 승격 (내부 품질은 확신하나 외부 검증 필요)
- [ ] `beta` 에서 1 분기 후 deprecation/prune dry-run 완료 + P3 → P2 실제 승급 1 회 후 `stable` 검토

## 13. Pretendard 폰트 자산

- [x] woff2 바이너리는 repo 에 커밋하지 않음 (runtime fetch 정책)
- [x] `@font-face` 자동 주입 로직 (adapters/nextjs-tailwind-shadcn + raw-css-variables 양쪽)
- [x] `LICENSE-FONTS` 에 OFL §2 재배포 고지 포함
- [x] plugin README License 섹션 한국어 + 영문 병기
- [x] fetch script 대상 URL 은 `orioncactus/pretendard@v1.3.9` jsDelivr 고정

## 14. 공개 전 보안 스캔

- [x] `scripts/security-scan-launch.py` 실행 → high-confidence secret 탐지 0 건
- [x] `.env` / `.env.local` 은 git-ignore 대상
- [x] hardcoded token prefix / private key block 없음
- [x] `.github/workflows/*.yml` 의 secrets 참조가 모두 `${{ secrets.* }}` 형태
- [x] contributor GitHub handle (@bob-external / @carol-external 등) 이 실재하는 공개 계정이 아닌 합성 페르소나인지 명시적 문서화 → CATALOG_HEALTH_2026Q2.md §2 에 이미 `(persona)` 표기

## 15. 첫 1 주 후폭풍 대응 플랜

- [x] **알림 채널 설정**: GitHub issue notification 을 1차 채널로 사용
- [x] **이슈 triage 시간 블록**: 공개 후 첫 1 주는 매일 1 회 (30 분) 이슈 리뷰
- [x] **FAQ 선행 작성**: README Quick Start / LOCAL_DEV / RELEASE / DEMO_SCRIPTS 로 설치 실패·한글 폰트·어댑터 fallback 경로 안내
- [x] **커뮤니티 채널 검토**: 초기에는 GitHub Issues + Discussions 로 시작
- [x] **1 주 후 회고**: public 공개 7 일 뒤 이슈 수 · PR 수 · 부정적 피드백 · 승급 조정 필요 여부 기록

---

## 부록 A. 공개 D-day 실행 순서

```
D-3: 항목 10 (CoC) + 11 (SLA) 문서 추가 PR 머지
D-2: 항목 14 (보안 스캔) + 항목 9 (issue template preset_id 동기화)
D-1: 항목 2 (Quick Start 로컬 재검증) + 항목 7 (DEMO_SCRIPTS 재검증)
D-0: 항목 5 (version 3-way) 재확인 → git tag v0.1.0 → release.yml 자동 실행
     → marketplace 에 `/plugin marketplace add github:2000silpeed/design-ontology-plugin` 공식 안내
D+1~7: 항목 15 (후폭풍 triage) 매일 1 회
D+7: 1 주 회고 + 항목 12 (alpha → beta) 결정
```

## 부록 B. 변경 이력

| 날짜 | 버전 | 내용 |
|------|------|------|
| 2026-04-21 | 1.0 | Phase 13-11-C-4 리허설 — 15 항목 초판 + 13-11-C-4-b 일부 실측 반영 (항목 4, 5, 6 completed). |
| 2026-04-29 | 1.1 | Phase 14/15 로컬 마감 — CoC/SLA/issue-template sync/demo verify/security scan 완료, 외부 GitHub 실행 항목만 대기 상태로 분리. |
| 2026-04-29 | 1.2 | Public plugin repo 생성, `main` push, validate workflow success, `v0.1.0` tag/release success. 남은 항목은 공개 1주 후 alpha→beta 판단 1건. |
