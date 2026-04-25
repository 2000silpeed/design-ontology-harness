# Design Ontology Plugin — 설계서 (v2)

> 상태: 코덱스 리뷰 전면 반영 (2026-04-18)
> 범위: design-ontology-harness를 **별도 레포의 Claude Code 공개 플러그인**으로 패키징하고, 단계적으로 30+ 프리셋 라이브러리로 확장
> 관련 문서: [`PLUGIN_TASKS.md`](./PLUGIN_TASKS.md), [`ARCHITECTURE.md`](./ARCHITECTURE.md), [`../TASK.md`](../TASK.md)

---

## 1. 배경과 문제

현재 harness는 이미 강력한 파이프라인을 갖추고 있다.

```
공식 KB 크롤 → 브랜드 프로필 매칭 → 색상·서체 자동 결정
→ 온톨로지 그래프 → system_spec.md / token_schema.json / component_specs
→ (선택) Visual Reference → (선택) 에이전트 팩 scaffold
```

하지만 **초보자 관점**에서는 여전히 아래 허들이 크다.

1. `build-kb`를 돌리는 데 5~15분, 실패 시 재시도 비용
2. `brand_profile.json`을 "잘" 쓰려면 디자인 용어를 알고 있어야 함
3. `spec.md` 작성이 또 다른 진입장벽
4. 이미 완성도 높은 기존 4개 프로젝트 산출물을 **매번 처음부터 재생성**
5. 산출물을 실제 프레임워크에 붙이는 마지막 단계가 수작업

### 핵심 인사이트

> "이미 잘 만들어진 산출물이 있다면, 초보자는 그걸 **고르기만** 해야 한다."

파이프라인은 **프리셋 생성기**로, 플러그인은 **프리셋 소비자**로 역할을 분리한다.

### 코덱스 리뷰 반영 원칙 (v2)

1. MVP는 **어댑터 1개 + 텍스트 프리뷰 + P0 5종**으로 축소. 3개 어댑터·90장 스크린샷·30+ 프리셋을 동시 구축하지 않음
2. **버전 계약을 매니페스트 1급 필드로** 끌어올림 (sync 드리프트 방지)
3. **프리셋 축 재설계**: `product_type`(혼재) → `app_mode` + `tone` + `tags` + `color_mode`
4. **Playwright 스크린샷은 선택적 폴리시**. MVP는 텍스트 + 색·서체 스와치

---

## 2. 목표 / 비목표

### 목표

1. **Claude Code Plugin 공개 배포** — `/plugin marketplace add` → `/plugin install design-ontology` 한 줄
2. **단계적 프리셋 확장**: P0 5 → P1 10 → P2 15 → P3 30+
3. **3~4개 질문 매칭 UX** — `/design-start`
4. **버전 계약 기반의 안정적 harness↔plugin sync**
5. **한국어 사용자 1급 지원** — Pretendard 한글 페어링, `--locale ko`
6. **기존 파이프라인과 공존** — 고급 사용자는 여전히 `build-kb` / `run-project`

### 비목표 (명시적 배제)

- 플러그인 내 KB 실시간 재빌드
- Remotion/영상 등 UI 외 영역
- 파이썬 코어 재구현
- **60 조합 선제 생성** — 실수요 중심 단계 확장
- **MVP에서 스크린샷 자동화 + 다중 어댑터 동시 구축**

---

## 3. 아키텍처

### 3.1 두 레포 구조

```
┌──────────────────────────────────────┐        ┌──────────────────────────────────────┐
│ design-ontology-harness (이 레포)    │        │ design-ontology-plugin (신규 공개)   │
│   역할: 프리셋 생성기 + 원본 소스    │ sync   │   역할: Claude Code 플러그인 배포본   │
│                                      │ ─────▶ │                                      │
│   design_ontology_harness/           │        │   .claude-plugin/                    │
│   projects/                          │        │   skills/                            │
│   presets/  ← 원본 산출물            │        │   agents/                            │
│   scripts/sync-plugin-presets.sh     │        │   presets/  ← sync 복사본             │
│                                      │        │   adapters/                          │
└──────────────────────────────────────┘        └──────────────────────────────────────┘
                                                               │
                                                               │ /plugin install
                                                               ▼
                                                     ┌──────────────────────┐
                                                     │  사용자 프로젝트     │
                                                     └──────────────────────┘
```

### 3.2 플러그인 레포 내부 구조

```
design-ontology-plugin/
├── .claude-plugin/
│   ├── marketplace.json
│   └── plugin.json            # 플러그인 단일 semver
├── skills/
│   ├── design-start/
│   ├── design-customize/
│   ├── design-rebuild/
│   ├── design-refactor/
│   ├── design-implement/
│   └── design-architect/
├── agents/
│   └── design-system-*.md
├── presets/
│   ├── matrix.json            # 축 + 프리셋 인덱스
│   ├── compatibility.json     # preset_api_version 매트릭스
│   └── <preset-id>/
│       ├── manifest.json      # 버전 계약 4개 필드 포함
│       ├── brand_profile.json
│       ├── system_spec.md
│       ├── token_schema.json
│       ├── component_inventory.json
│       ├── components/
│       ├── system_ontology.json
│       ├── preview.md         # 텍스트 프리뷰 (기본)
│       └── preview/           # (선택) P0만 정적 이미지
├── adapters/
│   ├── base/
│   └── nextjs-tailwind-shadcn/   # MVP: 이 1개만
├── scripts/
├── LICENSE
└── README.md
```

### 3.3 버전 계약 (1급 필드)

각 프리셋 `manifest.json`:

```json
{
  "id": "dashboard--minimal-tech",
  "schema_version": "1.0.0",
  "preset_api_version": "1.0.0",
  "generated_by_harness_version": "0.8.2",
  "preview_version": "1.0.0",
  "adapter_compatibility": {
    "nextjs-tailwind-shadcn": ">=0.1.0",
    "raw-css-variables": ">=0.1.0"
  },
  "source_project": "orbit",
  "source_commit": "abc1234",
  "content_hash": "sha256:...",
  "app_mode": "dashboard",
  "brand_tone": "minimal-tech",
  "color_modes": ["light", "dark"],
  "default_color_mode": "light",
  "tags": ["saas", "ko"],
  "locale_pairings": {...}
}
```

4개 버전 필드의 역할:

| 필드 | 의미 | 변경 트리거 |
|------|------|-------------|
| `schema_version` | 산출물 내부 스키마 (token_schema.json 등) | 산출물 구조 변경 |
| `preset_api_version` | 플러그인 소비 계약 | 매니페스트 필드 추가/삭제 |
| `generated_by_harness_version` | 생성 시점 Python 코어 버전 | 매 빌드마다 |
| `preview_version` | 프리뷰 아티팩트 형식 | 텍스트/스크린샷 포맷 변경 |

sync-time validator는 `compatibility.json`과 플러그인 `plugin.json`의 지원 범위를 비교해 미지원 버전의 preset은 PR 생성을 거부한다.

### 3.4 Sync 방식

- harness CI가 `presets/` 빌드 + validator 통과 시에만 plugin 레포로 PR 자동 생성
- PR 본문에 compatibility 리포트 첨부 (각 프리셋의 version 필드 diff)
- 플러그인 레포 CI가 두 번째 validator로 재확인
- 플러그인 단일 semver (`0.x.y`) 릴리스 시 `marketplace.json` 자동 동기화

---

## 4. 프리셋 매트릭스 (재설계)

### 4.1 축 1 — `app_mode` (8종)

제품 도메인이 아닌 **정보구조/상호작용 모드**로 분류. 도메인은 `tags`에서 표현.

| ID | 라벨 | 대표 UX |
|----|------|---------|
| `dashboard` | 대시보드/관리자 | sidebar, data table, KPI card, filter chrome |
| `document-content` | 문서/콘텐츠/레퍼런스 | reading flow, TOC, article, long-form |
| `marketing-landing` | 마케팅/랜딩 | hero, pricing, social proof, CTA |
| `commerce` | 커머스/쇼핑 | product grid, detail, cart, checkout |
| `conversation-copilot` | 대화형/코파일럿 | chat, prompt, artifact, thread |
| `canvas-tool` | 캔버스/크리에이티브 도구 | canvas, layer panel, inspector |
| `community-feed` | 소셜/피드 | feed, thread, presence, notifications |
| `monitoring-ops` | 모니터링/운영 | chart grid, alert list, dense table, status |

> fintech/ai/sports/fashion/gov/devtools는 **tags**로 분리. 같은 `dashboard`라도 `tags: ["fintech"]`와 `tags: ["devtools"]`가 달라질 수 있다.

### 4.2 축 2 — `brand_tone` (5종)

코덱스 지적에 따라 color-mode를 빼고 5종으로 축소.

| ID | 라벨 | 키워드 | 팔레트 성향 |
|----|------|--------|------------|
| `minimal-tech` | 미니멀 테크 | clean, neutral, precise | 무채색 + 제한된 accent |
| `editorial-warm` | 에디토리얼 웜 | serif, calm, editorial | warm neutral + muted accent |
| `bold-confident` | 대담한 | high-contrast, energetic | saturated primary |
| `playful-soft` | 플레이풀 소프트 | rounded, friendly | pastel + rounded |
| `corporate-trust` | 기업/신뢰 | conservative, trustworthy | navy/deep blue |

**삭제**: `premium-dark` — "premium"은 톤 어휘가 맞지만 "dark"는 색상 모드. 섞여 있어 중복 프리셋을 만든다. 다크 프리미엄 느낌은 `minimal-tech` + `color_mode: "dark"` + 메탈릭 accent 태그로 표현.

### 4.3 축 3 — `color_mode` (프리셋 속성, 1~3종)

프리셋 매니페스트 필드. ID에는 포함하지 않는다.

- `light` — 라이트만
- `dark` — 다크만
- `both` — 라이트 + 다크 둘 다 (대부분의 프리셋 기본값)

`default_color_mode`로 초기값 지정.

### 4.4 축 4 — `tags` (자유 태그)

도메인/스타일/로케일 qualifier. 매칭 신호 보조.

`fintech`, `ai`, `sports`, `fashion`, `devtools`, `reading-heavy`, `reference-docs`, `mobile-first`, `ko`, `en`, `dense`, `airy` 등.

### 4.5 프리셋 ID 규칙

```
{app_mode}--{brand_tone}
예: dashboard--minimal-tech
예: document-content--editorial-warm
```

`color_mode`와 `tags`는 **속성**. ID에 섞지 않는다.

### 4.6 어댑터 (축 5, 프리셋 외부)

런타임 조합. 프리셋과 직교.

| 순위 | ID | MVP 여부 |
|------|-----|---------|
| 1 | `nextjs-tailwind-shadcn` | **MVP 포함** |
| 2 | `raw-css-variables` | MVP 이후 (10B) |
| 3 | `vite-tailwind` | 수요 검증 후 (10C) |

### 4.7 로케일 옵션 (한글 1급)

- `editorial-warm`, `minimal-tech`, `corporate-trust`: **Pretendard 기본 번들**
- 매니페스트 `locale_pairings.ko` 필드에 서체 페어링 기록
- 어댑터 `--locale ko` 플래그로 폰트 자산 주입

### 4.8 커버리지 로드맵 (30+)

| 티어 | 누적 | 범위 | 마일스톤 |
|------|-----|------|----------|
| P0 | 5 | 기존 4프로젝트 승격 + dashboard 신규 | M2 |
| P1 | 10 | 수요 상위 5종 신규 | M5 |
| P2 | 15 | 톤 다변화 5종 | M6 |
| P3 | 30+ | 실수요·커뮤니티 기여 | M7+ |

#### P0 (MVP, 5종)

| 프리셋 ID | 기원 | tags |
|-----------|------|------|
| `document-content--editorial-warm` | `signal-desk` 승격 | `["reading-heavy","ko"]` |
| `commerce--editorial-warm` | `colorfit` 승격 | `["fashion","mobile-first","ko"]` |
| `marketing-landing--bold-confident` | `premier-league` 승격 | `["sports"]` |
| `conversation-copilot--minimal-tech` | `glacier` 승격 | `["ai","ko"]` |
| `dashboard--minimal-tech` | 신규 (코드네임 `orbit`) | `["saas","ko"]` |

#### P1 (+5, 누적 10)

`dashboard--corporate-trust` [fintech], `monitoring-ops--minimal-tech`, `document-content--minimal-tech` [reference-docs, devtools], `community-feed--playful-soft`, `canvas-tool--minimal-tech` [creative]

#### P2 (+5, 누적 15)

`marketing-landing--minimal-tech`, `commerce--bold-confident`, `conversation-copilot--editorial-warm`, `document-content--bold-confident`, `dashboard--editorial-warm`

#### P3 (+15 이상, 누적 30+)

`dashboard--bold-confident`, `dashboard--playful-soft`, `commerce--minimal-tech`, `commerce--playful-soft`, `marketing-landing--editorial-warm`, `marketing-landing--playful-soft`, `conversation-copilot--corporate-trust`, `document-content--corporate-trust`, `monitoring-ops--corporate-trust`, `monitoring-ops--bold-confident`, `canvas-tool--bold-confident`, `community-feed--minimal-tech`, `community-feed--editorial-warm`, ... (수요/기여 기반 추가)

각 프리셋은 `color_mode: "both"`가 기본. 특정 톤은 dark 기본(`minimal-tech + dark-default` 등)으로 변형 가능.

---

## 5. 사용자 플로우

### 5.1 경로 A — 기본 (4단계 질문)

```
사용자:  /design-start
Claude:  1) 뭘 만들고 있어요? (app_mode 8종)
사용자:  ① 대시보드
Claude:  2) 분위기는? (tone 5종)
사용자:  ① 미니멀 테크
Claude:  3) 색상 모드?
         ① 라이트 + 다크 (기본)
         ② 다크 우선
         ③ 라이트만
사용자:  ①
Claude:  4) 기술 스택?
         ① Next + Tailwind + shadcn  (지원)
         ② (예정) Raw CSS Variables / Vite+Tailwind
사용자:  ①
Claude:  5) 한글 UI인가요? [Y/n]
사용자:  Y
Claude:  매칭: ⭐ dashboard--minimal-tech  (신뢰도: High)
         대안: document-content--minimal-tech (Medium)
         [텍스트 프리뷰 출력]
         설치 대상 요약:
           • design-system/
           • tailwind.config.ts (extend)
           • app/globals.css (CSS vars + dark mode)
           • components.json
           • public/fonts/PretendardVariable.woff2
         설치할까요?
사용자:  네
```

### 5.2 경로 B — 자연어 한 줄

```
사용자:  /design-start "AI 글쓰기, 차분하고 editorial, 다크 기본, Next+shadcn, 한글"
Claude:  매칭: conversation-copilot--editorial-warm × dark-default × nextjs-tailwind-shadcn (High)
         대안: conversation-copilot--minimal-tech (Medium),
              document-content--editorial-warm (Medium)
```

### 5.3 경로 C — 고급 커스터마이징

```
사용자:  /design-customize dashboard--minimal-tech
Claude:  프리셋 복사본을 projects/my-app/에 생성했습니다.
         brand_profile.json 수정 → uv run design-ontology run-project 로 재합성.
```

---

## 6. 기존 코어와의 관계

| 레이어 | 역할 | 사용자 |
|--------|------|--------|
| **Python Core (이 레포)** | 프리셋 생성기 | 메인테이너, 고급 사용자 |
| **Preset Library (이 레포 `presets/`)** | 원본 산출물 카탈로그 | 플러그인 sync 대상 |
| **Plugin Repo (별도)** | 매칭, 설치, 실행 | 일반 사용자 |

### 메인테이너 워크플로우

```bash
uv run design-ontology build-preset \
  --project projects/signal-desk \
  --preset-id document-content--editorial-warm

uv run design-ontology rebuild-all-presets
uv run design-ontology validate-presets       # 버전 계약 검증
uv run design-ontology render-previews --text # 텍스트 프리뷰
uv run design-ontology render-previews --screenshots --tier P0  # P0만 스크린샷
./scripts/sync-plugin-presets.sh              # harness → plugin PR
```

### 기존 `init-agent-pack` 운명

- 단기: 유지. 프로젝트 단위 스킬 주입
- 장기: "선택된 프리셋 + 어댑터 출력만 target repo에 복사"로 역할 축소

---

## 7. 스택 어댑터

### 7.1 MVP 범위 (코덱스 반영)

**어댑터는 1개만 MVP에 포함**. 나머지는 alpha 이후.

| 순위 | 어댑터 | 시점 |
|------|--------|------|
| 1 | `nextjs-tailwind-shadcn` | Phase 10A (MVP) |
| 2 | `raw-css-variables` | Phase 10B (alpha 후) |
| 3 | `vite-tailwind` | Phase 10C (수요 검증 시) |

### 7.2 공통 인터페이스

```python
class StackAdapter(ABC):
    id: str
    version: str
    supported_preset_api: str   # semver range
    def detect(self, target_repo: Path) -> float: ...
    def render(self, preset: Preset, target: Path,
               color_mode: str, locale: str = "en") -> list[FileOp]: ...
    def merge(self, op: FileOp, existing: Path) -> FileOp: ...
```

### 7.3 `nextjs-tailwind-shadcn` (MVP 유일 어댑터)

| 생성/수정 | 내용 |
|-----------|------|
| `tailwind.config.ts` | theme.extend (색상·서체·radius·spacing) |
| `app/globals.css` | CSS 변수 + dark mode (`[data-theme='dark']`) |
| `components.json` | shadcn 토큰 매핑 |
| `design-system/` | 프리셋 산출물 복사본 |
| `public/fonts/` (ko) | Pretendard 주입 |

### 7.4 충돌 정책

- 파일 존재 → 병합 시도 (tailwind `theme.extend` 등)
- 병합 불가 → `<file>.ds-proposed` + 경고
- 사용자 코드 절대 덮어쓰지 않음

---

## 8. 매칭 엔진

### 8.1 신호

| 신호원 | 가중치 |
|--------|-------|
| 질문 답변 (app_mode / tone / color_mode / stack) | 0.6 |
| 자연어 키워드 → 축·태그 매핑 | 0.3 |
| 사용자 프로젝트 감지 (package.json, framework) | 0.1 |

### 8.2 점수 (coarse bucket)

```
raw_score(preset) =
    match(app_mode)   * 0.5 +
    match(brand_tone) * 0.35 +
    tag_overlap       * 0.15
```

raw_score는 내부용. **사용자에겐 소수점이 아니라 3단계 bucket으로 표시**:

| 버킷 | 조건 |
|------|------|
| **High** | 1등 preset의 raw_score ≥ 0.8 이고 2등과 격차 ≥ 0.15 |
| **Medium** | raw_score ≥ 0.6 또는 1/2등 격차 < 0.15 |
| **Low** | raw_score < 0.6 |

Top-3 제시. Low만 있으면 "정확한 매칭 없음, 가장 가까운 대안" 문구로 fallback.

### 8.3 키워드 → 축·태그 사전 (샘플)

```json
{
  "app_mode": {
    "대시보드|dashboard|admin|console": "dashboard",
    "문서|docs|article|reading|블로그|매거진": "document-content",
    "랜딩|landing|marketing|홈페이지": "marketing-landing",
    "커머스|쇼핑|shop|commerce|store": "commerce",
    "AI|챗봇|copilot|assistant|chat": "conversation-copilot",
    "figma|canvas|에디터|editor|creative": "canvas-tool",
    "피드|feed|community|social|쓰레드": "community-feed",
    "monitoring|모니터링|ops|alert|dashboard 운영": "monitoring-ops"
  },
  "brand_tone": {
    "미니멀|minimal|clean|neutral": "minimal-tech",
    "editorial|serif|차분|calm|warm": "editorial-warm",
    "bold|대담|강렬": "bold-confident",
    "친근|rounded|귀여|playful": "playful-soft",
    "corporate|신뢰|conservative|trust": "corporate-trust"
  },
  "color_mode": { "dark|다크|어두운": "dark", "light|라이트|밝은": "light" },
  "tags": {
    "fintech|금융|결제|송금": "fintech",
    "ai|gpt|llm": "ai",
    "devtools|개발자 도구": "devtools",
    "한글|korean|ko": "ko"
  }
}
```

---

## 9. 프리뷰 렌더링 (텍스트 우선, 스크린샷은 선택)

### 9.1 코덱스 반영

스크린샷은 숨은 비용 1위로 지적됐다. MVP는 **텍스트 프리뷰**로 출발하고, 스크린샷 자동화는 P0 5종에만 제한적으로 도입한다.

### 9.2 레벨

| 레벨 | 구성 | 생성 | MVP 포함 |
|------|------|------|----------|
| **Text** | 개요 / 추천 용도 / **색상 스와치 HEX 블록** / 서체 샘플 문구 / 대표 컴포넌트 3개 / 주의사항 | `build-preset` 시 자동 | ✅ |
| **Static Screenshot (P0)** | hero + components 2장 (dark는 color_mode가 지원할 때만) | 별도 명령, P0만 | ⚠️ alpha 후 |
| **Full Screenshot Suite** | P0~P3 전체 × 3장 × 2뷰포트 | 선택적 | ❌ (장기 검토) |

### 9.3 Text 프리뷰 템플릿

```markdown
# dashboard--minimal-tech

## 어떤 제품에 맞나
- SaaS 관리자/운영 대시보드
- 고밀도 데이터 테이블 필요
- 테크/중립 톤

## Color Tokens (light)
- primary:   #0A7CFF ⬛
- surface:   #FFFFFF ⬜
- text:      #0F172A
- border:    #E2E8F0
- accent:    #6366F1

## Color Tokens (dark)
- primary:   #3B82F6
- surface:   #0B1220
- ...

## Typography
- heading: Inter / Pretendard (ko) — 600 / 700
- body:    Inter / Pretendard (ko) — 400 / 500

## 대표 컴포넌트
- DataTable (sortable, sticky header, dense)
- KPI Card (numeric emphasis, trend indicator)
- Sidebar Nav (2-level, collapsible)

## 주의사항
- editorial 성격이 필요하면 `document-content--editorial-warm`
- 랜딩에는 부적합
```

### 9.4 Static Screenshot 파이프라인 (Phase 12B, alpha 이후)

- 대상: **P0 5종만**
- 장수: **2장** (hero + components)
- 다크는 프리셋이 지원할 때만 추가
- 뷰포트: 1440×900 (데스크톱만, 모바일은 보류)
- Playwright 결정론 가드: 폰트 `document.fonts.ready` 대기, 애니메이션 OFF, 고정 seed
- 실패 시 → 텍스트 프리뷰로 자동 fallback

---

## 10. 리스크 / 트레이드오프

| 리스크 | 영향 | 완화 |
|--------|------|------|
| 프리셋 30+ 품질 유지 비용 | 허접한 프리셋 누적 | 단계 확장 + 승급 기준 + **deprecation 정책** (§11 참조) |
| 스크린샷 유지 비용 | 폰트 레이스·브라우저 drift | MVP에서 제외, P0만 alpha 후 도입 |
| harness↔plugin 드리프트 | "sync 성공인데 배포 불가" | 버전 계약 4필드 + sync-time validator (Phase 7) |
| 매칭 신뢰도 과잉 정밀 | fake precision | 3-bucket (High/Medium/Low) 표시 |
| shadcn copy-paste 충돌 | 기존 컴포넌트와 충돌 | 어댑터가 기존 감지 시 토큰만 주입, 생성 스킵 |
| 공개 마켓플레이스 악용 | 브랜드 도용 프리뷰 | MIT + 크레딧 명시, preview 생성 소스 공개 |
| 한글 서체 라이선스 | Pretendard 번들 | SIL OFL 준수, LICENSE-FONTS 분리 |
| MVP를 작게 잡을 때의 FOMO | 어댑터 1개로 충분한가? | alpha 후 2개 추가 순차 배포 |

---

## 11. 프리셋 라이프사이클 정책 (신설)

30+ 프리셋을 "정크 드로워"로 만들지 않기 위한 명시 정책.

### 11.1 승급 기준 (P1 → marketplace-default)

다음을 모두 만족해야 marketplace-default 등급:

- 버전 계약 4필드 통과
- 텍스트 프리뷰 존재 + 검토자 1명 승인
- 어댑터 1개 이상에서 round-trip 테스트 통과
- `sources.json`에 KB 시드 기록
- 최소 1회 실제 사용자 프로젝트에 설치 검증

### 11.2 Deprecation 기준

- 6개월간 설치·매칭 hit 0
- `generated_by_harness_version`이 현재 harness의 2 minor 버전 이상 뒤처짐
- snapshot 회귀 테스트 실패 3회 연속

### 11.3 오너십

- 각 프리셋 `manifest.json`에 `owner` 필드 (기본: 메인테이너)
- 커뮤니티 기여 프리셋은 기여자가 owner로 6개월 유지 후 재평가

### 11.4 분기별 가지치기

- 분기마다 `catalog-health` 리포트 생성
- 하위 성과 프리셋 deprecated 이동 → 다음 분기 삭제

---

## 12. 완료 정의

### 12.1 MVP (alpha, Phase 11 종료 시점)

1. 공개 레포 `design-ontology-plugin` 초기 커밋 + 마켓플레이스 등록
2. P0 5종 프리셋 번들 (텍스트 프리뷰 포함)
3. 어댑터 `nextjs-tailwind-shadcn` 1종
4. `/design-start` 4단계 질문 + coarse-bucket 매칭
5. 한글 로케일 지원 (Pretendard 자동 페어링)
6. 버전 계약 4필드 + sync-time validator

### 12.2 Beta (Phase 13 종료 시점)

7. 어댑터 2종 추가 (`raw-css-variables`, `vite-tailwind`)
8. P1~P2 10종 추가 (누적 15)
9. P0 선택적 스크린샷 (hero + components 2장)
10. 프리셋 라이프사이클 정책 운영 (오너십, deprecation, pruning)

### 12.3 GA (Phase 14 종료 시점)

11. P3 확장 (누적 30+)
12. 커뮤니티 기여 경로 문서화
13. 릴리스 자동화 (tag push → marketplace 동기화)

---

## 13. 마일스톤 (재구성)

| M | 산출물 | 예상 기간 |
|---|--------|----------|
| M1 | 프리셋 인프라 + **버전 계약** + validator | 3일 |
| M2 | P0 5종 승격 + 텍스트 프리뷰 | 2일 |
| M3 | plugin 레포 + 스킬/에이전트 이식 + sync 훅 | 2일 |
| M4 | `nextjs-tailwind-shadcn` 어댑터 1종 | 2일 |
| M5 | `/design-start` UX + 매칭 엔진 → **MVP alpha** | 2일 |
| M6 | 어댑터 2종 추가 (`raw-css`, `vite-tailwind`) + P1 | 3~4일 |
| M7 | P0 선택적 스크린샷 + P2 | 3일 |
| M8 | 라이프사이클 정책 + P3 + 공개 GA | 5~7일 |

---

## 14. 결정 기록

### 14.1 1차 확정 (2026-04-18, v1)

| 항목 | 결정 |
|------|------|
| 프리셋 규모 | 30+ (P0~P3 단계 확장) |
| 레포 구조 | 별도 레포 `design-ontology-plugin` |
| 어댑터 우선순위 | ① nextjs-tailwind-shadcn ② raw-css-variables ③ vite-tailwind |
| 한글 지원 | Pretendard 기본 번들, `--locale ko` |
| 프리뷰 | Playwright 스크린샷 3장 |
| 마켓플레이스 | 공개 |
| 버저닝 | 플러그인 단일 semver |
| 라이선스 | MIT + SIL OFL (Pretendard) |

### 14.2 2차 리비전 (2026-04-18, v2 — 코덱스 리뷰 전면 반영)

| 변경 항목 | 변경 내용 |
|----------|----------|
| **MVP 범위 축소** | 어댑터 3개 → **1개만**(`nextjs-tailwind-shadcn`) |
| **프리뷰 격하** | Playwright 3장 기본 → **텍스트 프리뷰 기본**, P0만 선택적 스크린샷 2장 |
| **축 재설계** | `product_type`(10) → **`app_mode`**(8) + **`tags`**(자유) |
| **브랜드 톤 축소** | 6 → 5 (`premium-dark` 삭제) |
| **color_mode 분리** | 별도 속성으로 분리, ID 외부 |
| **버전 계약 승격** | Phase 15 → **Phase 7** 1급 필드 (4개 버전) |
| **매칭 신뢰도 표시** | 0.98 소수점 → **High/Medium/Low** 3버킷 |
| **Phase 10 분할** | 10A/10B/10C (Next만 MVP) |
| **Phase 12 분할** | 12A 텍스트 / 12B 선택적 스크린샷 |
| **라이프사이클 정책 신설** | §11 승급/deprecation/오너십/가지치기 |
| **Phase 10↔12 병렬 삭제** | 실제 병렬 아님 → 순차로 의존 명시 |
