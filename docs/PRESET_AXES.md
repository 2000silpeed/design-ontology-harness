# Preset Axes — 근거 문서 (v1)

> 근거: [`PLUGIN_PLAN.md`](./PLUGIN_PLAN.md) §4 프리셋 매트릭스 (재설계)
> 스키마: [`../schemas/preset_matrix.schema.json`](../schemas/preset_matrix.schema.json)
> 소스 축 정의: [`../presets/matrix.json`](../presets/matrix.json)

축 체계는 **v2 코덱스 리뷰 반영** 결과. `product_type`(10) 단일 축 → `app_mode` + `brand_tone` + `color_mode` + `tags` 4축으로 분리.

---

## 축 1 — `app_mode` (8종, 고정)

**정보구조/상호작용 모드**로 분류. 도메인(fintech, ai, sports 등)은 `tags`에서 표현.

| ID | 라벨 | 대표 UX |
|----|------|---------|
| `dashboard` | 대시보드/관리자 | sidebar, data-table, kpi-card, filter-chrome |
| `document-content` | 문서/콘텐츠/레퍼런스 | reading-flow, toc, article, long-form |
| `marketing-landing` | 마케팅/랜딩 | hero, pricing, social-proof, cta |
| `commerce` | 커머스/쇼핑 | product-grid, product-detail, cart, checkout |
| `conversation-copilot` | 대화형/코파일럿 | chat, prompt, artifact, thread |
| `canvas-tool` | 캔버스/크리에이티브 도구 | canvas, layer-panel, inspector |
| `community-feed` | 소셜/피드 | feed, thread, presence, notifications |
| `monitoring-ops` | 모니터링/운영 | chart-grid, alert-list, dense-table, status |

### 왜 8종인가

- **정보 밀도/상호작용 패턴이 명확히 다른 단위**로만 축을 나눔. `shopping cart`와 `product grid`는 같은 `commerce` 모드
- **도메인은 태그로 분리**: `dashboard + tags:[fintech]`와 `dashboard + tags:[devtools]`는 같은 `app_mode`, 다른 질감
- 8종을 넘어가면 매칭 UX에서 선택 피로 증가 (PLAN §5.1 4단계 질문)

---

## 축 2 — `brand_tone` (5종, 고정)

시각/감성 톤. color-mode를 뺀 순수 톤 5종.

| ID | 라벨 | 키워드 | 팔레트 성향 |
|----|------|--------|------------|
| `minimal-tech` | 미니멀 테크 | clean, neutral, precise | 무채색 + 제한된 accent |
| `editorial-warm` | 에디토리얼 웜 | serif, calm, editorial | warm neutral + muted accent |
| `bold-confident` | 대담한 | high-contrast, energetic | saturated primary |
| `playful-soft` | 플레이풀 소프트 | rounded, friendly | pastel + rounded |
| `corporate-trust` | 기업/신뢰 | conservative, trustworthy | navy/deep blue |

### v1에서 삭제된 톤

- `premium-dark` — "premium"은 톤 어휘, "dark"는 색상 모드. 축이 섞여 중복 프리셋 유발. 다크 프리미엄 느낌은 `minimal-tech + color_mode: "dark"` + 메탈릭 accent 태그로 표현.

---

## 축 3 — `color_mode` (프리셋 속성)

ID에 포함하지 않음. manifest 필드.

- `light` — 라이트만 지원
- `dark` — 다크만 지원
- **`both`** (기본) — 라이트 + 다크 둘 다

`default_color_mode`로 초기값 지정. `default_color_mode`는 반드시 `color_modes` 배열에 포함되어야 함 (스키마 conditional validation).

---

## 축 4 — `tags` (자유)

도메인/스타일/로케일 qualifier. 매칭 신호 보조.

**권장 태그 (오픈셋, 예시만)**: `fintech`, `ai`, `sports`, `fashion`, `devtools`, `reading-heavy`, `reference-docs`, `mobile-first`, `ko`, `en`, `dense`, `airy`, `saas`, `creative`

태그는 enum이 아니며, 매칭 엔진이 자연어 키워드와 overlap 점수로 사용.

---

## ID 규칙

```
{app_mode}--{brand_tone}
예: dashboard--minimal-tech
예: document-content--editorial-warm
```

**검증 레이어 2단**:

1. JSON Schema `pattern`에서 형식 검증 (8 × 5 = 40 조합 전수 regex)
2. `preset_validator.py`에서 `id == f"{app_mode}--{brand_tone}"` 교차 검증

`color_mode`와 `tags`는 속성이므로 ID에 섞지 않음.

---

## 매트릭스 크기

- 이론 최대: 8 × 5 = **40 조합** × color_mode 변형
- 실제 로드맵: P0 5 → P1 10 → P2 15 → P3 30+ (PLUGIN_PLAN.md §4.8)
- **40을 선제 생성하지 않음**. 실수요 기반 단계 확장. 라이프사이클 정책(§11)으로 pruning.

---

## 변경 절차

축 확장/축소는 **contract breaking change**.

1. `schemas/preset_matrix.schema.json` enum 수정 → `matrix_version` minor 또는 major bump
2. `presets/compatibility.json`의 `current_preset_api_version` bump
3. 모든 기존 프리셋 `manifest.json` 재빌드 (`rebuild-all-presets`)
4. `docs/PRESET_AXES.md` 갱신 + 이 섹션에 변경 기록 추가

### 변경 기록

| 날짜 | 변경 | preset_api_version |
|------|------|--------------------|
| 2026-04-18 | 초기 제정 (app_mode 8, brand_tone 5, color_mode 3) | 1.0.0 |
