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

## Phase 6: Visual Reference Harness (Pinterest-assisted) (중기-장기)

> 목표: 공식 디자인 시스템 KB만으로는 잡기 어려운 "조형 언어"를 보강한다.
> 단, 이미지에서 실제 CSS를 복원하려 하지 않고, visual motif / layout cue / component styling hint를 추출하는 방향으로 간다.
> Pinterest는 최종 truth source가 아니라 "시각 레퍼런스 탐색기"로 사용한다.

### 핵심 원칙

- [ ] **V-0. truth source 분리 원칙 고정**
  - 공식 KB / spec / brand_profile / color_reference는 구조적 근거
  - visual reference는 감성, 레이아웃 밀도, 표면 처리, 타이포 분위기 보강용
  - 이미지에서 추출한 값은 `observed`, `inferred`, `unverified` 레벨로 provenance를 남김
  - system_spec.md에 "image-derived hints are advisory" 문구 명시

### Stage A: 로컬 이미지 기반 visual_reference (우선 구현)

- [x] **V-1. brand_profile 스키마 확장**
  - 대상: `schemas/brand_profile.schema.json`, `config/brand_profile.example.json`
  - `visual_reference` 필드 추가:
    - `mode`: `local-images` | `pinterest-assisted`
    - `query`: 검색어 후보 배열
    - `sources`: 로컬 이미지 경로 목록
    - `preferred_count`
    - `weights.layout / component_shape / color_balance / typography_mood / surface_style`
    - `extraction_policy`: `advisory-only` | `allow-token-suggestions`
  - `notes`, `must_include`, `avoid_patterns` 같은 가드레일도 포함

- [x] **V-2. visual_reference 파서 및 정규화 모듈 추가**
  - 신규: `design_ontology_harness/visual_reference.py`
  - 입력:
    - 로컬 이미지 파일
    - PNG/JPG/WebP
    - 스크린샷 묶음 디렉터리
  - 출력:
    - `visual_reference_report.json`
    - 이미지별 메타데이터, 출처, 해상도, aspect ratio
    - 중복/유사 이미지 그룹핑

- [x] **V-3. 이미지 기반 시각 규칙 추출기**
  - 추출 항목:
    - dominant / supporting / neutral / accent 비중
    - surface style: flat / tinted / elevated / outlined
    - corner style: sharp / medium / round / pill
    - density: airy / balanced / dense
    - typography mood: editorial / utilitarian / premium / playful
    - layout rhythm: strict grid / card mosaic / split pane / feed / dashboard
  - 출력:
    - `visual_motifs.json`
    - `layout_cues.json`
    - `component_style_hints.json`

- [x] **V-4. 컴포넌트 archetype 탐지**
  - 이미지에서 추정 가능한 archetype만 다룸:
    - top nav
    - sidebar
    - dashboard cards
    - KPI tiles
    - table/list
    - form field
    - modal/drawer
    - chat/panel
  - 실제 구현 구조는 spec/component inventory로 확정
  - 이미지 기반 추정 결과는 `candidate_component_archetypes`로만 기록

### Stage B: Pinterest-assisted 검색/수집 보조

- [ ] **V-5. brand_profile + spec 기반 검색어 생성기**
  - 대상: `spec_analyzer.py` 또는 신규 `visual_queries.py`
  - 입력:
    - `brand_keywords`
    - `anti_keywords`
    - `product_primitives`
    - `spec.md`
  - 출력:
    - Pinterest/이미지 검색용 query 10~20개
    - 예: `editorial fintech dashboard`, `warm premium onboarding flow`, `dense operations control panel`

- [ ] **V-6. Pinterest 보조 수집 모드 설계**
  - 1차 목표는 "직접 크롤링"이 아니라 "검색 보조 + 선택 보조"
  - 구현 방향:
    - 사용자가 Pinterest에서 이미지 저장/스크린샷 추출
    - 하네스는 그 로컬 이미지를 분석
  - 2차 목표:
    - Playwright 기반 보조 검색
    - query별 보드/핀 후보 스냅샷 생성
    - 최종 채택은 사용자 또는 에이전트가 명시적으로 고정

- [ ] **V-7. Pinterest 전용 리스크 가드레일**
  - 로그인 필요 / 동적 로딩 / 결과 변경성 / 저작권 이슈 문서화
  - 직접 asset 다운로드보다 screenshot/reference URL 저장 우선
  - 재배포 금지, "참고용 분석"임을 명시
  - robots / 접근 제약이 있으면 graceful fallback

### Stage C: synthesis 및 산출물 통합

- [x] **V-8. synthesis에 visual reference 결합**
  - 대상: `synthesis.py`
  - `load_brand_profile()`에서 `_resolved_visual_reference` 생성
  - blueprint에 아래 항목 추가:
    - `visual_language`
    - `layout_cues`
    - `component_style_hints`
    - `reference_mood_summary`
  - 공식 KB와 충돌 시 KB 우선, visual reference는 보조로만 사용

- [x] **V-9. authoring 산출물 확장**
  - 대상: `authoring.py`
  - `system_spec.md`에 신규 섹션 추가:
    - Visual Direction
    - Layout Rhythm
    - Surface & Edge Language
    - Image-derived Component Hints
  - `token_schema.json`에는 직접 토큰을 만들기보다
    - candidate surface styles
    - radius bias
    - density bias
    - emphasis strategy
    - icon/container preference
    - color balance hints
    - 정도를 넣음

- [x] **V-10. component_specs 연계**
  - 대상: `component_specs.py`
  - 이미지 기반 규칙으로 컴포넌트별 adaptation hint 추가:
    - card elevation 성향
    - border vs fill 중심 여부
    - CTA prominence 강도
    - filter/nav 밀도
    - chart panel framing 방식
  - 단, anatomy / states / accessibility는 spec과 KB 근거 유지

### Stage D: CLI / 문서 / 운영 흐름

- [x] **V-11. CLI 확장**
  - 후보 명령:
    - `analyze-visuals --brand-profile ...`
    - `generate-visual-queries --brand-profile ... --spec ...`
  - `run-project` 안에서 자동 실행할지, 독립 단계로 둘지 결정
  - 초기는 독립 단계 권장:
    - `build-kb`
    - `analyze-visuals`
    - `run-project`

- [ ] **V-12. README / workflow 문서화**
  - "공식 KB + visual references" 이중 입력 구조 설명
  - Pinterest는 필수가 아니라 선택적 보조 레이어라고 명시
  - 로컬 이미지 기반 시작 흐름을 Quick Start에 추가

### Stage E: 검증 및 샘플

- [ ] **V-13. 샘플 프로젝트 2종 검증**
  - `signal-desk` 같은 정보 밀도 높은 dashboard
  - `brand/landing` 성격이 강한 marketing surface
  - 같은 KB라도 visual reference에 따라 다른 visual direction이 나오는지 비교

- [ ] **V-14. 결과 비교 리포트**
  - without visual reference
  - with local visual reference
  - with pinterest-assisted query set
  - 차이:
    - density
    - surface language
    - card hierarchy
    - tone alignment
    - component emphasis

### 구현 우선순위

1. `V-1` ~ `V-4`: 로컬 이미지 기반 visual_reference 해석기
2. `V-8` ~ `V-10`: synthesis / authoring / component specs 통합
3. `V-11` ~ `V-12`: CLI 및 문서화
4. `V-5` ~ `V-7`: Pinterest-assisted 검색 보조
5. `V-13` ~ `V-14`: 샘플 검증 리포트

### 완료 정의

- 사용자가 Pinterest 이미지를 직접 URL로 넣지 않아도, 저장한 스크린샷/레퍼런스 이미지만으로 visual direction을 분석할 수 있다.
- `brand_profile + spec + official KB + local visual references` 조합으로 산출물이 생성된다.
- system_spec.md가 "무슨 컴포넌트를 만들지"뿐 아니라 "어떤 조형 언어로 구현할지"까지 설명한다.
- Pinterest는 필수 의존성이 아니라 선택적 보조 채널로 유지된다.

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
| 2026-04-15 | Phase 6 Visual Reference Harness 상세 계획 수립 | done |
| 2026-04-15 | V-1~V-2 visual_reference 스키마/파서/정규화 모듈 구현 | done |
| 2026-04-15 | V-3 visual motifs / layout cues / component style hints 구현 | done |
| 2026-04-15 | V-4 visual archetype 추출 + component inventory 연결 | done |
| 2026-04-15 | V-8~V-9 synthesis / system_spec / token_schema 통합 | done |
