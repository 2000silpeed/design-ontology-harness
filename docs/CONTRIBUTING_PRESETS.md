# 프리셋 기여 가이드 — Contributing Presets

> **기반 문서**: [`PLUGIN_PLAN.md`](./PLUGIN_PLAN.md) §11 라이프사이클 · §4.8 P3 로드맵, [`PRESET_AXES.md`](./PRESET_AXES.md) 축 체계
> **대상**: 외부 기여자가 `design-ontology-harness` 에 신규 **P3 프리셋**을 제안하는 절차
> **언어**: 한국어 primary, 주요 항목은 영문 병기 (English mirror sections below Korean)

---

## 1. 왜 프리셋을 기여하나

P0~P2 15종은 메인테이너가 큐레이팅했지만, 실제 수요는 훨씬 다양합니다. 당신이 만든 브랜드·프로젝트가
`app_mode × brand_tone` 조합 중 비어있는 셀을 채우면 — 다른 사용자는 4단계 질문 → `/design-start` 한 번으로
당신과 비슷한 감각의 디자인 시스템을 설치할 수 있습니다.

**기여가 가치 있는 경우**
- 기존 15종으로 커버되지 않는 조합 (예: `commerce--playful-soft`, `dashboard--bold-confident`)
- 공공 레퍼런스 기반의 재현 가능한 KB 시드
- 최소 1개 실제 프로젝트에 사용할 예정이거나, 이미 사용 중

**기여가 적절하지 않은 경우**
- 기존 프리셋 미세 변형 (색상만 다른 dashboard--minimal-tech)
- 특정 고객사 비공개 레퍼런스만 사용한 경우 (브랜드 도용 §9)
- 6개월 유지 약속이 어려운 경우

---

## 2. 기여 전 체크리스트 — Pre-flight Checklist

PR 제출 **전에** 모두 충족:

- [ ] `axis` 선택 완료 — 비어있는 셀을 §4 가이드로 확인
- [ ] `source_project` 준비 — `projects/<your-project>/` 생성 + brand_profile.json + spec.md
- [ ] KB 시드 최소 3개 (공공 레퍼런스만, `sources.json` 에 기록)
- [ ] 기존 15종과 HEX 3종(primary / accent / surface_tint) 2개 이상 겹침 없음
- [ ] `/design-start` 에서 자기 자신이 Top-1 로 나오는 자연어 쿼리 최소 1개 확보
- [ ] 6개월 owner 유지 동의 (PLAN §11.3)

---

## 3. 실전 5단계 절차 — 5-Step Workflow

### Step 1. 프로젝트 scaffold

```bash
uv run design-ontology init \
  --project-dir projects/<your-project> \
  --brand-name "<Your Brand>" \
  --product-summary "<한 줄 요약>" \
  --kb-dir kb/default
```

> **팁**: `--kb-dir kb/default` 을 같이 넘기면 Step 3 에서 KB 재빌드 없이 공유 KB 를 바로 쓸 수 있습니다.
> 이 플래그를 생략하면 `project_manifest.json` 의 `kb_dir` 이 `null` 로 남아 Step 3 에서
> `No kb_dir configured` 에러가 뜹니다. 그 경우 Step 3 명령에 `--kb-dir kb/default` 를 직접
>붙여도 되고, 또는 `project_manifest.json` 의 `kb_dir` 을 `../../kb/default` 로 수동 수정해도 됩니다.

### Step 2. brand_profile.json + spec.md 작성

`projects/<your-project>/brand_profile.json` 에 아래 최소 필드를 채웁니다 (scaffold 가 대부분 틀을
만들어 두고 `seeds` 빈 배열 · `color_reference.preferred_families` 빈 배열 · `visual_reference.query`
예시값을 남겨 두므로, 비어 있거나 예시 값인 항목만 교체하면 됩니다).

```json
{
  "brand_name": "Your Brand",
  "brand_tone": "editorial-warm",
  "color_reference": {
    "path": "/Users/you/.../docs/color-reference.md",
    "preferred_families": ["Pastel Reds", "Pastel Oranges"],
    "palette_roles": {
      "primary": "Salmon",
      "accent": "Peach Puff",
      "surface_tint": "Buttercream"
    },
    "palette_strategy": { "mode": "brand-guided", "temperature": "warm", "contrast": "soft" }
  },
  "font_system": {
    "heading": { "name": "Quicksand", "weights": [500, 600, 700] },
    "body":    { "name": "Inter",     "weights": [400, 500, 600] },
    "mono":    { "name": "JetBrains Mono", "weights": [400, 500] },
    "korean":  { "name": "Pretendard", "weights": [400, 500, 600, 700] }
  },
  "product_summary": "...",
  "seeds": ["https://example.com/design-system", "https://example.com/public-brand-guide", "..."]
}
```

> **`palette_roles` 주의**: `primary` / `accent` / `surface_tint` 에 쓰는 이름은 반드시
> `docs/color-reference.md` 의 `### <Color Name>` 섹션에 등록된 이름과 **정확히 일치** 해야 합니다
> (case-insensitive). 존재하지 않는 이름을 쓰면 경고 없이 `preferred_families` 기반 유사 팔레트로
> 폴백되어 의도치 않은 HEX 가 선택될 수 있습니다. 등록된 이름 목록은 `grep "^### " docs/color-reference.md`
> 으로 확인하고, 새 색상을 도입하려면 해당 파일에 `### <Name>` 섹션을 추가한 PR 로 먼저 제안하세요.

> **`visual_reference.query` 주의**: scaffold 기본값은 `["editorial dashboard", "premium app UI"]`
> 예시여서 본인 프리셋 톤과 다를 수 있습니다. 실제 브랜드의 영감 키워드로 교체하세요.

`projects/<your-project>/spec.md` — 제품의 UX 패턴 / 대표 컴포넌트 / 사용자 플로우. `spec_analyzer` 가 이 텍스트에서
컴포넌트를 추출합니다.

**(선택) locale_pairings.json 동봉** — 한국어 UI 를 1급으로 지원한다면 Step 4 의 `--locale-pairings` 플래그에
사용할 파일을 `projects/<your-project>/locale_pairings.json` 으로 미리 준비해 두세요.

```json
{
  "ko": {
    "heading_font": "Pretendard",
    "body_font": "Pretendard",
    "mono_font": "JetBrains Mono",
    "notes": "한국어 UI 1급 — 주요 텍스트 keep-all line-height 1.5–1.6, 숫자 mono 영문 고정 tabular-nums"
  }
}
```

### Step 3. Blueprint 합성

```bash
uv run design-ontology run-project --project-dir projects/<your-project> --kb-dir kb/default
```

> Step 1 에서 `--kb-dir kb/default` 을 넘겼다면 `--kb-dir` 을 생략해도 됩니다.

산출물: `projects/<your-project>/build/system/` 아래 system_spec.md / token_schema.json / components/ 등.

### Step 4. 프리셋으로 승격 (P3 고정 + owner=기여자 handle)

```bash
uv run design-ontology build-preset \
  --project projects/<your-project> \
  --preset-id <app_mode>--<brand_tone> \
  --color-modes light,dark \
  --default-color-mode light \
  --tags <tag1>,<tag2>,ko \
  --owner "@your-github-handle" \
  --tier P3 \
  --description "<한 줄 설명>" \
  --locale-pairings projects/<your-project>/locale_pairings.json
```

> `--locale-pairings` 를 빠뜨리면 preview.md 의 `Locale Pairings` 섹션에 `ko` 페어링이 누락됩니다.
> 한국어 UI 를 표방한 프리셋이라면 이 플래그를 꼭 같이 넘기세요.

자동 생성: `presets/<id>/manifest.json` · `preview.md` · `content_hash`.

> 프리셋이 생성된 직후 `presets/matrix.json` 의 `presets[]` 배열에도 같은 id 로 **수동 엔트리**
> 를 추가해야 합니다. matrix.json 에 없으면 `validate-presets` 는 통과해도 `match-preset` 이 해당
> 프리셋을 후보로 띄우지 않습니다. 기존 17종 엔트리를 복사해서 id/app_mode/brand_tone/tags/owner/tier 만 교체하세요.

### Step 4.5. `build-sources` 로 sources.json 자동 생성 (Phase 15-9)

```bash
uv run design-ontology build-sources --preset-id <your-id> --force
```

`brand_profile.json` 의 `seeds` 필드 + `visual_reference.source_references` + `spec.md` 의 markdown
링크를 병합하여 `presets/<your-id>/sources.json` 을 자동 작성합니다. dedup · URL 정규화 · 도메인 기반
`kind` 추론이 포함됩니다.

**자동 `kind` 분류 기준** (도메인 화이트리스트, 미매칭은 `article` fallback)

| kind | 대표 도메인 |
|------|-------------|
| `design-system` | `linear.app`, `stripe.com`, `vercel.com`, `shadcn`, `material.io`, `polaris.shopify.com`, `atlassian.design`, `ant.design`, `mui.com`, `radix-ui.com`, `chakra-ui.com`, `pretendard.com` … |
| `visual-reference` | `figma.com`, `framer.com`, `excalidraw.com`, `tldraw.com`, `dribbble.com`, `pinterest.com`, `are.na`, `behance.net` … |
| `brand-guide` | `brand.uber.com`, `brand.airbnb.com`, `brand.slack.com`, `logo.clearbit.com` … |
| `reference-docs` | `docs.stripe.com`, `vercel.com/docs`, `developer.mozilla.org`, `docs.github.com`, `nextjs.org/docs`, `react.dev` … |
| `article` | 위 도메인 목록에 포함되지 않는 모든 URL |

**시드 < 3 warning 이 뜨면?**
- `brand_profile.json.seeds` 에 공공 레퍼런스 URL 을 수동으로 2–3개 더 추가
- 또는 `spec.md` 의 "참고" 섹션에 markdown 링크 `[title](url)` 형태로 추가
- 그 후 `build-sources --force` 재실행 — 시드 ≥ 3 이어야 Step 5 self-test 및 P3 → P2 승급 게이트 통과

**`sources.json` 예시 (자동 생성 결과물)**

```json
{
  "preset_id": "dashboard--playful-soft",
  "source_project": "meadow",
  "seeds": [
    {
      "url": "https://cal.com",
      "kind": "design-system",
      "title": "Cal.com",
      "notes": "booking scheduling admin references"
    },
    {
      "url": "https://flo.health",
      "kind": "visual-reference",
      "title": "Flo",
      "notes": "wellness health tracker references"
    },
    ...
  ],
  "pretendard_font_license": "SIL OFL 1.1",
  "created_at": "2026-04-20T22:12:34Z"
}
```

`brand_profile.seeds` 는 문자열 배열 `["https://..."]` 도 되고 객체 배열 `[{url, kind, title, notes}]`
도 됩니다. 객체 형태로 `kind` 를 명시하면 도메인 화이트리스트 fallback 대신 지정값이 사용됩니다.

### Step 5. 자체 검증 → PR 제출

```bash
# 구조/버전 계약 검증
uv run design-ontology validate-presets

# preview.md 템플릿 검증
uv run design-ontology lint-previews --preset-id <your-id>

# 커뮤니티 전용 검증 (HEX 겹침 / 셀 중복 / self-match)
python3 scripts/validate-community-preset.py --preset-id <your-id>

# 매칭 확인 (자연어 → 자기 자신 Top-1)
uv run design-ontology match-preset --free-text "<your natural-language query>"
```

**Exit code 해석**
- `errors=0, warnings=0` → green, 바로 PR 가능
- `errors=0, warnings>0` → merge 가능 (warnings 는 리뷰어 재량). PR 본문에 사유를 적어주세요.
- `errors>0` → merge 불가. 출력된 메시지에 따라 수정 후 재실행.

**자연어 쿼리 작성 팁**
- `warm` / `calm` / `bold` / `minimal` 등 다른 `brand_tone` 의 키워드와 충돌하지 않도록 2–4 단어를 조합하세요.
  예: `commerce--playful-soft` 라면 `"warm pastel"` 보다 `"rounded consumer playful d2c"` 가 self-match 에 유리합니다
  (keywords.json 의 `editorial-warm` 엔트리에 `warm` 이 포함되어 있어 `warm` 단독은 자주 editorial 로 끌립니다).

모두 통과하면 PR 생성 → 자동 검증 workflow → 메인테이너 리뷰 → 머지.

---

## 4. Axis 선택 가이드 — Picking an Axis Cell

축 체계는 `app_mode` (8종 × 고정) × `brand_tone` (5종 × 고정) = 40 셀. `color_mode` 와 `tags` 는 속성.

### 4.1 현재 18종이 채운 셀 (2026-04-20 기준)

|                     | minimal-tech | editorial-warm | bold-confident | playful-soft | corporate-trust |
|---------------------|:---:|:---:|:---:|:---:|:---:|
| dashboard           | **P0** | **P2** | **P3** | **P3** | **P1** |
| document-content    | **P1** | **P0** | **P2** | — | — |
| marketing-landing   | **P2** | — | **P0** | — | — |
| commerce            | — | **P0** | **P2** | **P3** | — |
| conversation-copilot| **P0** | **P2** | — | — | — |
| canvas-tool         | **P1** | — | — | — | — |
| community-feed      | — | — | — | **P1** | — |
| monitoring-ops      | **P1** | — | — | — | — |

### 4.2 우선순위 Top-8 빈 셀 (P3 수요 예상 기반, PLAN §4.8)

> Phase 13-11-A / 13-11-B 에서 `dashboard--bold-confident` · `dashboard--playful-soft` · `commerce--playful-soft`
> 가 P3 로 채워지며 top-10 에서 3칸이 빠졌습니다. 최신 우선순위는 `uv run design-ontology catalog-health` 출력
> 의 `priority_empty_cells` 를 직접 확인하세요.

| 순위 | 조합 | 쓰임새 힌트 |
|:---:|---|---|
| 1 | `commerce--minimal-tech` | B2B/테크 커머스 (Stripe 스타일 결제, 개발자 대상 API 상점) |
| 2 | `marketing-landing--editorial-warm` | 에디토리얼 톤 랜딩 (뉴스레터·출판·문화재단) |
| 3 | `marketing-landing--playful-soft` | 컨슈머 랜딩 (D2C 스낵·생활용품) |
| 4 | `conversation-copilot--corporate-trust` | 엔터프라이즈 챗봇 (금융·보험 AI 상담) |
| 5 | `document-content--corporate-trust` | 엔터프라이즈 docs (금융·헬스케어 규정 문서) |
| 6 | `monitoring-ops--corporate-trust` | 엔터프라이즈 observability (규제·감사 컨텍스트) |
| 7 | `canvas-tool--bold-confident` | 크리에이터 전용 bold 캔버스 (스트리머·밈·숏폼) |
| 8 | `dashboard--playful-soft` 외 추가 태그 변형 | 다른 도메인 (habit/학습/가계부) — P3 tag 차별화 필요 |

### 4.3 어떤 조합을 고를지 판단 기준

1. **당신의 실제 프로젝트**가 어떤 셀에 가장 가까운지 — `/design-start --free-text "<설명>"` 을 돌려봅니다.
   Top-1 이 Low 버킷이면 빈 셀을 채울 기회입니다.
2. **Top-8** 에 포함된 조합이면 수요 예상이 높으므로 승급도 빠릅니다.
3. **이미 P0/P1/P2 로 채워진 셀**에 또 기여하는 건 원칙적으로 받지 않습니다 (중복 경고 §5).
   단, 확연히 다른 서브도메인 (예: 기존 `commerce--editorial-warm` [fashion] vs `commerce--editorial-warm` [luxury-gourmet])
   은 **P3 로만** 수락되며 태그로 차별화해야 합니다.

**catalog-health 활용**

```bash
uv run design-ontology catalog-health
```

출력의 `## Priority Empty Cells` 섹션이 실시간 우선순위 top-10 을 보여줍니다. §4.2 표는 스냅샷이므로
분기마다 달라질 수 있습니다 — 기여 전에는 catalog-health 출력을 기준 삼으세요. 특히 `priority` 수치가
낮을수록 (1에 가까울수록) P2 승급 속도가 빠릅니다.

---

## 5. "이미 비슷한 프리셋이 있나" 체크 절차 — Duplicate Check

### 5.1 HEX 겹침 확인

```bash
# 모든 기존 preview.md 에서 Core HEX 3종 일괄 출력 (stdlib grep)
for p in presets/*/; do
  id=$(basename "$p")
  [[ "$id" == *.* ]] && continue
  [ -f "$p/preview.md" ] || continue
  echo "=== $id ==="
  awk '/^### Core/{flag=1;next} /^### /{flag=0} flag' "$p/preview.md" | \
    grep -E "^\s*-\s*(primary|accent|surface_tint)" || true
done
```

또는 plugin 레포 `docs/CATALOG.md` 의 Core HEX 블록 육안 확인. 마지막으로
`python3 scripts/validate-community-preset.py --preset-id <your-id>` 의 `NOTES` 에 Core HEX 가 찍히므로
PR 전 가장 확실한 검증입니다.

**판정 기준**
- `primary` / `accent` / `surface_tint` 3 role 중 **2개 이상**이 기존 프리셋과 동일 HEX → warning (머지는 가능하지만 리뷰어 권한으로 팔레트 조정 요청).
- 1개만 겹치면 통과지만 가능하면 palette_roles 를 조정하는 쪽이 카탈로그 가독성에 좋습니다.
- 동일 `brand_tone` 내 (예: playful-soft 3종) 에서는 특히 엄격히 차별화하세요 — 사용자가 선택 시 색만으로도 구분이 가야 합니다.

### 5.2 셀 중복 확인

```bash
uv run design-ontology match-preset \
  --app-mode <your-app-mode> \
  --brand-tone <your-brand-tone> \
  --top 3
```

동일 `{app_mode, brand_tone}` 조합이 이미 P0/P1/P2 에 존재하면 Top-1 이 해당 프리셋으로 나옵니다. 그 경우:
- 태그로 차별화할 수 있으면 P3 로만 제출
- 차별점이 애매하면 다른 셀로 전환 권장

### 5.3 `sources.json` 가이드

- **공공 레퍼런스만** — Figma 유료/비공개 파일, 고객사 내부 디자인 시스템 URL 금지 (§9 브랜드 IP)
- **최소 3개** — P3 수락 하한. 적으면 build-sources 가 warning, P3 → P2 승급 게이트에서 strict error
- **kind 명시 권장** — 도메인 추론이 불확실하면 객체 형태 `{url, kind, title, notes}` 로 기입
- **URL 은 항상 `http(s)://` 로 시작** — validator 가 스킴 없는 URL 은 거부
- **중복 URL dedup** — build-sources 가 자동 처리 (같은 URL 이 brand_profile 과 spec.md 양쪽에 있어도 1회만 기록)

### 5.4 자동 검증

`scripts/validate-community-preset.py` 가 위 두 체크를 자동화합니다.

```bash
python3 scripts/validate-community-preset.py --preset-id <your-id>
```

- **Pass**: validator + preview_linter + HEX + 셀 중복 + self-match 모두 통과
- **Warning**: HEX 겹침 2개 이상 OR 셀 중복 (P3 는 중복 가능하되 경고)
- **Error**: validator/linter 실패 OR self-match Top-1 이 자기 자신이 아님

---

## 6. 승급 조건 — Promotion Criteria

PLAN §11.1 기준. P3 → P2 → P1 → marketplace-default 순으로 단계별 승급.

| 단계 | 조건 |
|------|------|
| **P3** (초기 수락) | `validate-presets` + `lint-previews` + `validate-community-preset.py` 모두 통과, **`sources.json` 존재 + seeds ≥ 3**, owner 지정, 6개월 유지 동의 |
| **P2** | 위 + 텍스트 프리뷰 검토자 1명 승인, 최소 1회 실제 사용자 프로젝트 설치 검증, `promote-preset --target P2 --dry-run` 5 gate (validate / lint / adapter round-trip Next+Raw / sources.json strict / self-match Top-1) 모두 통과 |
| **P1** | 위 + `sources.json` KB 시드 기록 검토, 어댑터 2개 round-trip 테스트 통과, 분기별 설치·매칭 hit 증가 추세 |
| **marketplace-default** | 위 + 메인테이너 리뷰 + snapshot 회귀 테스트 통과 + 문서/카탈로그 강조 등재 |

승급은 메인테이너가 분기별로 `catalog-health` 리포트를 보며 결정합니다. 기여자가 직접 요청할 수 있지만 자동 보장은 아닙니다.

---

## 7. Owner 책임 — Maintainer Responsibilities

프리셋 `manifest.json` 의 `owner` 필드에 GitHub handle 이 기록됩니다.

**6개월 유지 기간 중**
- 피드백 이슈 (해당 프리셋 언급) 에 2주 이내 반응
- harness 가 새 minor 버전을 릴리스하면 (`generated_by_harness_version` 업데이트) 4주 이내 rebuild PR 제출 또는 메인테이너에게 권한 위임
- snapshot 회귀 테스트 실패 시 수정 또는 파이프라인 보완 제안

6개월 후 재평가 — 승급 / 유지 / deprecation 중 하나. 기여자가 owner 를 포기하면 메인테이너가 넘겨받거나 deprecation 절차로 이동합니다.

---

## 8. Deprecation 기준 — Sunset Policy

PLAN §11.2. 아래 중 **하나라도** 해당되면 deprecated 마킹.

- 6개월간 설치·매칭 hit 0 (사용자가 한 번도 선택하지 않음)
- `generated_by_harness_version` 이 현재 harness 의 2 minor 버전 이상 뒤처짐
- snapshot 회귀 테스트 3회 연속 실패

**절차**

1. Deprecated 표시 (`manifest.deprecated_at`, `deprecation_reason` 추가) → `/design-start` 에서 숨김 처리
2. 다음 분기 catalog-health 에서 최종 검토
3. 문제 없으면 삭제 (`presets/<id>/` 제거 + `matrix.json` 엔트리 제거)

기여자가 반대 의견이 있으면 deprecation PR 에 댓글로 알려주세요.

---

## 9. Code of Conduct & 브랜드 도용 금지 — CoC & Brand IP

### 9.1 공공 레퍼런스만 사용

- **허용**: Material Design, Stripe, Linear, shadcn, Vercel, Ghost 등 공개 디자인 시스템 문서
- **허용**: 브랜드 가이드를 오픈소스·퍼블릭 라이선스로 공개한 회사 자료
- **금지**: 특정 고객사의 비공개 Figma / 내부 디자인 문서
- **금지**: 경쟁사 디자인의 직접적 HEX·토큰 복제 (영감은 OK, 복사는 NG)

### 9.2 브랜드 로고·마크 금지

프리셋은 **토큰 + 컴포넌트 사양**만 담습니다. 로고, 브랜드 마크, 캐릭터, 상표권 자산은 프리셋에 포함하지 않습니다.

### 9.3 Code of Conduct

이 프로젝트는 [Contributor Covenant](https://www.contributor-covenant.org/) v2.1 을 따릅니다 (CoC 문서는 별도 추가 예정).
위반 제보는 이슈 또는 메인테이너 직접 연락.

---

## 10. 자주 묻는 질문 — FAQ

**Q. 한국어 외 locale 도 기여할 수 있나요?**
A. 가능합니다. `locale_pairings.<lang>` 필드에 폰트 페어링을 기록하세요. ja/zh-CN 등은 P3 단계에서 수요 검증 후 확장.

**Q. 내 프리셋이 Top-10 빈 셀이 아닌데 기여해도 되나요?**
A. 괜찮습니다. Top-10 은 수요 예상 상위일 뿐, 나머지 빈 셀도 P3 로 전부 수락합니다. 다만 승급은 수요 기반.

**Q. 어댑터 지원은 기여자가 해야 하나요?**
A. 아니요. 기여는 프리셋 산출물만. 어댑터 (`nextjs-tailwind-shadcn` / `raw-css-variables`) 는 메인테이너가 유지합니다.
단 기여자 프리셋이 두 어댑터 모두에서 round-trip 테스트를 통과해야 합니다 (자동화됨).

**Q. preview.md 를 수동으로 수정해도 되나요?**
A. `build-preset` 재실행 시 덮어쓰기됩니다. 대표 컴포넌트·스와치 순서를 바꾸고 싶으면 `preset_builder.py` / spec.md 를 조정하세요.

**Q. PR 이 리뷰 대기 상태로 오래 걸리면?**
A. 메인테이너가 분기별 catalog-health 리포트와 함께 일괄 리뷰합니다. 긴급하면 이슈로 알려주세요.

---

## English Mirror — Key Sections

### Why contribute a preset
You're adding a curated design system that other users pick via `/design-start` in one step. Best candidates: empty cells
in the `app_mode × brand_tone` matrix (§4) and presets grounded in **public references** you can cite.

### 5-step workflow (summary)
1. `uv run design-ontology init --project-dir projects/<your-project> --brand-name "..." --product-summary "..." --kb-dir kb/default` (pass `--kb-dir kb/default` here, or again on the Step 3 command, to avoid the `No kb_dir configured` error).
2. Fill in `brand_profile.json` (color_reference + `palette_roles` using names from `docs/color-reference.md` + font_system + **`seeds` array with ≥3 public URLs**) + write `spec.md`. Drop a `locale_pairings.json` next to them if the preset claims Korean support. **Important**: `palette_roles.primary/accent/surface_tint` must reference named entries in `docs/color-reference.md` — unknown names silently fall back to nearest family color and can surprise you with HEX overlap.
3. `uv run design-ontology run-project --project-dir projects/<your-project> --kb-dir kb/default` → synthesizes blueprint under `build/system/`
4. `uv run design-ontology build-preset --project ... --preset-id <app_mode>--<brand_tone> --owner @handle --tier P3 --locale-pairings projects/<your-project>/locale_pairings.json` (skip `--locale-pairings` only if the preset is English-only). Then manually add a matching entry to `presets/matrix.json` — matcher ignores presets that are not in the matrix.
4.5. `uv run design-ontology build-sources --preset-id <your-id> --force` → auto-generates `presets/<id>/sources.json` from `brand_profile.seeds` + `visual_reference.source_references` + markdown links in `spec.md`; dedup + domain-based `kind` inference (`design-system` / `visual-reference` / `brand-guide` / `reference-docs` / `article` fallback). Warns if seeds < 3.
5. Run `validate-presets`, `lint-previews`, `scripts/validate-community-preset.py`, `match-preset` — submit PR when all pass. `errors=0` is required; warnings are reviewer discretion. Pick self-match queries that avoid other tones' keywords (e.g. `"warm"` pulls toward editorial-warm).

### Ownership
6-month maintenance commitment. Respond to preset-specific issues within 2 weeks, rebuild on harness minor bumps within
4 weeks, keep snapshot tests green. Re-evaluated after 6 months for promotion / continuation / deprecation.

### Deprecation triggers (any one)
- Zero installs and zero match hits for 6 months
- `generated_by_harness_version` lags current harness by ≥2 minor versions
- Snapshot regression test fails 3 times in a row

### Brand IP
Only public design-system references. No private Figma files, no logos / marks / trademarks bundled into a preset, no
direct palette copies of competitors. Inspiration is welcome, duplication is not.

---

**피드백 / 문의**: 이슈 트래커 or `@maintainer` 멘션.
