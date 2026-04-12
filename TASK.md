# insane-design 뽑아먹기 태스크

> 소스: https://github.com/fivetaku/insane-design
> 목표: 우리 designSystem에 실전 검증된 CSS 추출/분석 역량 통합

## Phase 1: 지식 흡수 (즉시 가능)

- [x] **1-1. pitfalls.md 14가지 함정 반영**
  - 대상: `color_reference.py`, `font_reference.py`
  - 핵심: 브랜드키트≠UI색, logo wall 오염, variable font 비표준 weight 등
  - 우리 레퍼런스 매칭 로직에 가드레일 추가

- [x] **1-2. AI 원칙 3가지 synthesis에 반영**
  - "hex를 만들지 않는다" / "토큰명을 만들지 않는다" / "팩트 위에 해석만"
  - 대상: `synthesis.py` 프롬프트/로직

## Phase 2: CSS 추출 파이프라인 (중기)

- [x] **2-1. var_resolver 통합**
  - CSS `var()` 체인 재귀 해결 + 순환 참조 감지
  - 우리 crawler.py 뒤에 파이프라인 연결

- [x] **2-2. brand_candidates 통합**
  - 시멘틱 변수 + selector 역할 + 빈도 기반 브랜드 색상 추출
  - SVG 로고 필터링, saturation 계산 로직 포함

- [x] **2-3. typo_extractor 통합**
  - CSS 커스텀 프로퍼티에서 타이포그래피 스케일 자동 추출
  - heading/text/display 카테고리 자동 분류

- [x] **2-4. alias_layer 통합**
  - 시멘틱 토큰 tier 분류 (core → util → action → component)
  - 우리 token_schema.json 구조와 매핑

## Phase 3: 수집 강화 (중기)

- [x] **3-1. 5-tier fallback 수집 체인**
  - httpx 기본 → Mobile UA → Jina Reader → Playwright → 중단
  - 우리 crawler.py의 수집 견고성 대폭 향상

- [x] **3-2. CSS 파일 병렬 다운로드**
  - HTML에서 `<link rel="stylesheet">` 추출 → 8개 동시 다운로드
  - 크롤 후 CSS 추출 파이프라인 자동 실행 연결

## Phase 4: 산출물 강화 (장기)

- [x] **4-1. design.md 16섹션 템플릿 병합**
  - system_spec.md 12→16섹션 확장
  - 추가: Quick Start, DO/DON'T, Drop-in CSS, CSS Extraction Summary

- [x] **4-2. 35개 실서비스 예시 KB 통합**
  - Stripe, Vercel, Linear, Toss 등 35개 실서비스 벤치마크 데이터
  - 키워드 매칭으로 유사 시스템 자동 탐색 + CLI `benchmark` 명령 추가
  - 합성 시 자동으로 benchmark context가 blueprint에 포함

## Phase 5: 진짜 온톨로지 그래프 (장기)

> 목표: 컬러, 서체, 컴포넌트, 패턴이 유기적으로 연결되는 관계 그래프
> 현재 ontology.py는 키워드 매칭일 뿐. 20개 노드 타입 + 24개 관계 타입의 진짜 그래프로 진화.

- [x] **O-1. 그래프 스키마 정의** (0.5일)
  - `graph_schema.py` 신규 생성
  - NodeType 20종: Brand, Principle, ColorPalette, ColorToken, ColorMode, FontFamily, TypeScaleEntry, SpacingToken, RadiusToken, MotionToken, ElevationToken, ComponentFamily, Component, ComponentState, LayoutPattern, InteractionPattern, AccessibilityRule, ProductPrimitive, SourceReference, BenchmarkSystem
  - EdgeType 24종: expresses, constrains, belongs_to_palette, derived_from, overrides_in_mode, contrast_pair, pairs_with, uses_font, member_of_family, has_state, uses_token, state_modifies_token, uses_type_scale, supports, implements, composed_of, requires, inspired_by, similar_to, references_font 등
  - OntologyNode, OntologyEdge, DesignOntologyGraph 데이터클래스
  - 그래프 쿼리 메서드 (get_nodes_by_type, get_edges_from/to)

- [x] **O-2. 코어 빌더 — brand, foundation, component** (1-2일)
  - `graph_builders.py` 신규 생성
  - `build_brand_layer`: brand_profile → Brand + Principle 노드, expresses 엣지
  - `build_foundation_layer`: token_schema → Spacing/Radius/Motion/Elevation 토큰 노드
  - `build_component_layer`: component_inventory → ComponentFamily + Component + ComponentState 노드, member_of_family + has_state + supports 엣지
  - `build_full_ontology_graph()` 오케스트레이터 함수
  - `authoring.py`의 `build_system_ontology()` 대체 연결

- [x] **O-3. 컬러 + 타이포 그래프** (1-2일)
  - `build_color_layer`:
    - color_reference → ColorPalette + ColorToken(core) 노드, belongs_to_palette 엣지
    - alias_layer → ColorToken(semantic/component) 노드, derived_from 엣지 (var chain)
    - WCAG contrast ratio 계산 → contrast_pair 엣지 (ratio + AA/AAA/fail 판정)
    - ColorMode 노드 + overrides_in_mode 엣지
  - `build_typography_layer`:
    - font_reference → FontFamily 노드, pairs_with 엣지 (heading↔body)
    - typo_extractor → TypeScaleEntry 노드, uses_font 엣지
  - 컬러↔컴포넌트 연결: alias_layer component tier → uses_token 엣지

- [x] **O-4. 패턴 + 접근성 + 벤치마크 레이어** (1일)
  - `build_pattern_layer`:
    - PRIMITIVE_COMPONENTS → LayoutPattern/InteractionPattern 노드
    - implements 엣지 (component → pattern), composed_of 엣지 (pattern → component)
  - `build_accessibility_layer`:
    - 8개 접근성 규칙 노드 (contrast-aa, keyboard-nav, label-association 등)
    - requires 엣지 (interactive component → keyboard-nav, input → label, surface/text pair → contrast-aa)
  - `build_benchmark_layer`:
    - benchmark_kb 35개 → BenchmarkSystem 노드
    - inspired_by 엣지 (brand → matched systems)
    - similar_to 엣지 (system ↔ system, Jaccard similarity)
    - references_font 엣지 (system → FontFamily)

- [x] **O-5. system_spec.md 그래프 기반 섹션** (1일)
  - 17. **Component-Token Map**: 컴포넌트별 사용 토큰 테이블 (uses_token 엣지에서 도출)
  - 18. **Contrast Audit**: surface/text 조합별 대비 비율 + AA/AAA 판정 (contrast_pair 엣지)
  - 19. **Pattern Catalog**: 레이아웃/인터랙션 패턴 목록 + 구성 컴포넌트 (composed_of 엣지)
  - system_spec.md 16→19섹션 확장

- [x] **O-6. 기존 ontology.py 정리** (0.5일)
  - ontology.py는 크롤 증거 수집용으로 유지 (문서→개념 키워드 매칭)
  - authoring.py의 `build_system_ontology()` 제거, `build_full_ontology_graph()`로 완전 교체
  - system_ontology.json 출력 포맷을 그래프 구조로 변경

### 그래프 구조 요약

```
                    Brand
                   ╱     ╲
            expresses    inspired_by
               ╱              ╲
         Principle         BenchmarkSystem ──references_font──▶ FontFamily
            │                                                      │
       constrains                                             pairs_with
         ╱    ╲                                                    │
  ColorPalette  ComponentFamily ◀──member_of_family── Component   FontFamily
       │              │                                  │  │  │
  belongs_to       has_state                             │  │  │
       │              │                                  │  │  │
   ColorToken    ComponentState                          │  │  │
    │  │  │           │                                  │  │  │
    │  │  └─contrast_pair─┘                              │  │  │
    │  │                                                 │  │  │
    │  derived_from (var chain)            uses_token ◀──┘  │  │
    │                                 uses_type_scale ◀─────┘  │
    overrides_in_mode ──▶ ColorMode    implements ◀────────────┘
                                            │
                                     InteractionPattern
                                            │
                                      composed_of
                                            │
                                       Component
```

### 기존 모듈 → 그래프 빌더 데이터 소스

| 기존 모듈 | 생성하는 노드/엣지 |
|-----------|-------------------|
| color_reference.py | ColorPalette, ColorToken (palette roles) |
| var_resolver.py | derived_from 엣지 (CSS var chain) |
| alias_layer.py | ColorToken tier 분류, uses_token 엣지 |
| brand_candidates.py | ColorToken (CSS 빈도 기반) |
| font_reference.py | FontFamily, pairs_with 엣지 |
| typo_extractor.py | TypeScaleEntry (CSS 추출) |
| authoring.py | Component, ComponentFamily, states |
| benchmark_kb.py | BenchmarkSystem, inspired_by 엣지 |

---

## 진행 기록

| 날짜 | 태스크 | 상태 |
|------|--------|------|
| 2026-04-12 | 분석 완료, 태스크 작성 | done |
| 2026-04-12 | 1-1 pitfalls 가드레일 반영 | done |
| 2026-04-12 | 1-2 AI 원칙 3가지 synthesis 반영 | done |
| 2026-04-12 | 2-1 var_resolver 통합 | done |
| 2026-04-12 | 2-2 brand_candidates 통합 | done |
| 2026-04-12 | 2-3 typo_extractor 통합 | done |
| 2026-04-12 | 2-4 alias_layer 통합 | done |
| 2026-04-12 | 3-1 5-tier fallback 수집 체인 | done |
| 2026-04-12 | 3-2 CSS 파일 병렬 다운로드 | done |
| 2026-04-12 | 4-1 16섹션 템플릿 병합 | done |
| 2026-04-12 | 4-2 35개 실서비스 벤치마크 KB | done |
| 2026-04-12 | Phase 5 온톨로지 그래프 (O-1~O-6) | done |
