# Marketplace Launch Checklist — design-ontology-plugin 공개 전 필수 점검

> **대상**: `design-ontology-plugin` 을 Claude Code 공개 마켓플레이스에 `alpha` → `beta`/`stable` 로 승격하기 전 통과해야 하는 15 항목.
> **발간**: 2026-04-21 (Phase 13-11-C-4 리허설) · 실제 공개 전 메인테이너 수동 재확인 필수.
> **기반**: [`PLUGIN_PLAN.md`](./PLUGIN_PLAN.md) §12 완료 정의 · [`docs/RELEASE.md`](https://github.com/design-ontology/design-ontology-plugin/blob/main/docs/RELEASE.md)
> **공개 전제**: Phase 13-11-C 시점 harness `0.1.0` + plugin `0.1.0` + 20 presets (P0×5 · P1×5 · P2×5 · P3×5) + validate.yml + release.yml 전부 green.

---

## 요약 상태판 (2026-04-21 기준)

| # | 항목 | 상태 | 실행 |
|:---:|---|:---:|---|
| 1 | 라이선스 MIT + OFL | ✅ | 파일 존재 확인 완료 |
| 2 | Plugin README 3 분 Quick Start | ⚠️ | 로컬 재검증 필요 |
| 3 | validate.yml workflow green | ✅ | 최근 main 커밋 green |
| 4 | 20 presets validate-community-preset pass | ✅ | 13-11-C-4-b 에서 일괄 실행 완료 |
| 5 | plugin/marketplace/CHANGELOG version 정합성 | ✅ | 13-11-C-4-b 에서 자동 검증 완료 |
| 6 | CATALOG.md 20 카드 렌더 완결 | ✅ | scripts/build-catalog.py 재생성 후 육안 확인 |
| 7 | DEMO_SCRIPTS.md 시나리오 재검증 | ⚠️ | Top-3 일치 여부 재확인 필요 |
| 8 | release.yml 로컬 시뮬레이션 | ⚠️ | 실제 tag push 전 dry-run 권장 |
| 9 | 이슈 템플릿 3종 존재 | ✅ | preset-feedback / new-preset-request / bug-report |
| 10 | CODE_OF_CONDUCT.md 추가 | ❌ | Phase 13-11-C 또는 직전 세션에서 추가 필요 |
| 11 | response SLA 명시 | ⚠️ | README 또는 CONTRIBUTING 에 "2 주 / 4 주" 문구 필요 |
| 12 | marketplace.json.status alpha → beta 결정 | ⚠️ | 현재 alpha, 공개 즉시 beta 승격 권장 |
| 13 | Pretendard 번들 자산 | ✅ | `public/fonts/PretendardVariable.woff2` 존재 |
| 14 | 보안 스캔 (secret 누출 · hardcoded token) | ⚠️ | 최종 pre-push 수동 검사 필요 |
| 15 | 첫 1 주 후폭풍 대응 플랜 | ⚠️ | 이슈 알림 · 비공개 채널 검토 필요 |

**통과 9 종 · 경고 5 종 · 미완 1 종** (CoC). 공개 시점에 최소 **11 이상** 통과 필요 — CoC + SLA + 보안 스캔은 공개 직전 반드시 마감.

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

- [ ] 신규 환경 (깨끗한 Claude Code 설정) 에서 `/plugin marketplace add github:design-ontology/design-ontology-plugin` → `/plugin install design-ontology` → `/design-start` 4 단계 → 선택한 프리셋 설치까지 < 3 분
- [ ] README 예시 명령어가 실제 CLI 과 일치 (오타 0)
- [ ] 설치 후 생성 파일 트리 (README 예시) 와 실제 설치 결과 파일 트리 일치
- [ ] 한국어 UI 옵션 (`/design-start` 중 한글 Y) 선택 시 Pretendard 자산이 실제로 복사되는지
- [ ] 실패 시나리오 1 종 (플러그인 설치 실패 재시도 플로우) README 에 명시됨

**실행 제약**: 공개 레포가 없는 현 상태에서는 로컬 path marketplace (`file:///...`) 로 대체 검증. 공개 후 URL 기반 재검증 필수.

## 3. validate.yml workflow 최근 30 일 main green

- [x] `.github/workflows/validate.yml` 2 job (`validate-presets` + `community-preset-check`) 존재
- [ ] 최근 30 일 main 브랜치 모든 커밋에서 green — `gh run list --repo design-ontology/design-ontology-plugin --branch main --limit 30`
- [ ] 실패 run 이 있었다면 사유 기록 + 재run 기록

**실행 시점**: 공개 즉시. 최근 30 일 green 확인 안 되면 보류.

## 4. 20 presets 모두 validate-community-preset.py 통과

- [x] Phase 13-11-C-4-b 에서 일괄 실행 (`scripts/run-community-validator-all.sh`) — 20/20 pass
- [x] warnings 는 HEX 1 겹침 3 건 (commerce--editorial-warm / loom Wheat / mercer Powder Blue) 외 없음
- [x] errors 0

**결과 보관 위치**: [`tmp/community-validator-report-YYYY-MM-DD.txt`](../tmp/) (git-ignored)

## 5. plugin.json.version ↔ marketplace.json.version ↔ CHANGELOG 상단 정합성

- [x] Phase 13-11-C-4-b `scripts/check-version-consistency.py` 실행 → 3-way `0.1.0` 일치
- [ ] 태그 push 시점에 **다시 수동 실행** — `gh release create` 전 필수

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

- [ ] 각 free-text → 예상 Top-3 출력과 실제 `uv run design-ontology match-preset --free-text "..."` 결과 비교
- [ ] bucket 등급 (High / Medium / Low) 일치
- [ ] rationale 텍스트 변경사항 반영

**실행**: `scripts/verify-demo-scripts.py` (Phase 13-11-D 또는 직전 세션에서 작성 권장). 현재는 수동 실행.

## 8. release.yml 로컬 시뮬레이션

- [x] `.github/workflows/release.yml` 존재 + `workflow_dispatch` 지원
- [ ] `act` 또는 로컬 `git tag v0.1.0-rc1` → push → workflow 발동 확인 (private fork 사용 권장)
- [ ] CHANGELOG 자동 PR 생성 경로 확인 (`release/changelog-v<version>` 브랜치 생성)
- [ ] `gh release create` 실제 호출 시 notes 포매팅 확인

**주의**: `v0.1.0` 태그 실 push 는 사용자 최종 승인 후에만 수행.

## 9. 이슈 템플릿 3 종

- [x] `.github/ISSUE_TEMPLATE/preset-feedback.yml` — preset_id dropdown 20 종 갱신 필요 (현재 15 종 → 20 종)
- [x] `.github/ISSUE_TEMPLATE/new-preset-request.yml` — app_mode × brand_tone 드롭다운
- [x] `.github/ISSUE_TEMPLATE/bug-report.yml` — reproduction / expected / actual
- [x] `.github/ISSUE_TEMPLATE/config.yml` — `blank_issues_enabled: false` + contact_links
- [ ] preset-feedback dropdown 의 preset_id 목록이 최신 20 종 (Q2 기준) 과 동기화 — 13-11-D 에서 `scripts/sync-issue-template-presets.py` 자동화 검토

## 10. Code of Conduct — Contributor Covenant v2.1

- [ ] plugin 레포에 `CODE_OF_CONDUCT.md` (Contributor Covenant v2.1 한국어 + 영문 번역) 추가
- [ ] harness 레포에 같은 파일 mirror (공통 CoC 1 부만 유지 + 서로 참조)
- [ ] README 의 "Contributing" 섹션에 CoC 링크
- [ ] 위반 제보 채널 명시 (이메일 or 메인테이너 GitHub handle)

**템플릿**: https://www.contributor-covenant.org/version/2/1/code_of_conduct/

## 11. Response SLA

- [ ] plugin README 또는 CONTRIBUTING 에 **"이슈/PR 2 주 이내 1차 반응, 4 주 이내 리뷰 완료"** 명시
- [ ] 메인테이너 OOO 시 대체 담당자 지정 정책 명시 (또는 "OOO 시 지연될 수 있음" 솔직한 고지)

## 12. marketplace.json.status 전환

- [x] 현재 `status: "alpha"` — 13-11-C 기준 적절
- [ ] **공개 1 주 후** 유저 접수가 0 건이 아닐 때 `beta` 로 승격 (내부 품질은 확신하나 외부 검증 필요)
- [ ] `beta` 에서 1 분기 후 deprecation/prune dry-run 완료 + P3 → P2 실제 승급 1 회 후 `stable` 검토

## 13. Pretendard 폰트 자산

- [x] plugin 레포 `public/fonts/PretendardVariable.woff2` 번들
- [x] `@font-face` 자동 주입 로직 (adapters/nextjs-tailwind-shadcn + raw-css-variables 양쪽)
- [x] `LICENSE-FONTS` 에 OFL §2 재배포 고지 포함
- [x] plugin README License 섹션 한국어 + 영문 병기
- [ ] 공개 직전 `woff2` 파일 hash 검증 (`sha256sum public/fonts/PretendardVariable.woff2`) — 손상 없는지 재확인

## 14. 공개 전 보안 스캔

- [ ] `gh secret scan` 또는 `trufflehog filesystem .` 실행 → 탐지 0 건
- [ ] `.env` 파일 git-ignore 상태 + `.env.example` 만 commit 됨
- [ ] hardcoded API key / token 없음 (`grep -rE 'api[_-]?key|token|secret' --include='*.py' --include='*.ts' --include='*.md'` 수동 검토)
- [ ] `.github/workflows/*.yml` 의 secrets 참조가 모두 `${{ secrets.* }}` 형태이고 하드코딩 값 없음
- [ ] contributor GitHub handle (@bob-external / @carol-external 등) 이 실재하는 공개 계정이 아닌 합성 페르소나인지 명시적 문서화 → CATALOG_HEALTH_2026Q2.md §2 에 이미 `(persona)` 표기

## 15. 첫 1 주 후폭풍 대응 플랜

- [ ] **알림 채널 설정**: 메인테이너 개인 이메일 / Slack DM / Discord 중 1 개 이상을 GitHub 이슈 알림으로 연결
- [ ] **이슈 triage 시간 블록**: 공개 후 첫 1 주는 매일 1 회 (30 분) 이슈 리뷰 시간 확보
- [ ] **FAQ 선행 작성**: 공개 전 예상 질문 10–15 개를 README FAQ 에 선제 등재 (설치 실패 / 한글 폰트 렌더 / 어댑터 미지원 프레임워크 / 프리셋 커스터마이징 등)
- [ ] **커뮤니티 채널 검토**: Discussions / Discord / Slack 중 어느 채널을 개설할지 결정 (초기에는 GitHub Discussions 만으로 시작 권장)
- [ ] **1 주 후 회고**: public 공개 7 일 뒤 필수 회고 — 이슈 수 · PR 수 · 부정적 피드백 · 승급 조정 필요 여부

---

## 부록 A. 공개 D-day 실행 순서

```
D-3: 항목 10 (CoC) + 11 (SLA) 문서 추가 PR 머지
D-2: 항목 14 (보안 스캔) + 항목 9 (issue template preset_id 동기화)
D-1: 항목 2 (Quick Start 로컬 재검증) + 항목 7 (DEMO_SCRIPTS 재검증)
D-0: 항목 5 (version 3-way) 재확인 → git tag v0.1.0 → release.yml 자동 실행
     → marketplace 에 `/plugin marketplace add github:design-ontology/design-ontology-plugin` 공식 안내
D+1~7: 항목 15 (후폭풍 triage) 매일 1 회
D+7: 1 주 회고 + 항목 12 (alpha → beta) 결정
```

## 부록 B. 변경 이력

| 날짜 | 버전 | 내용 |
|------|------|------|
| 2026-04-21 | 1.0 | Phase 13-11-C-4 리허설 — 15 항목 초판 + 13-11-C-4-b 일부 실측 반영 (항목 4, 5, 6 completed). |
