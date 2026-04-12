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
