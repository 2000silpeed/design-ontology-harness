# Visual Reference Validation Report

## 목적

Phase 6의 남은 검증 항목을 마무리하기 위해, 두 개의 샘플 프로젝트에서 아래 세 시나리오를 비교했다.

1. `without visual reference`
2. `with local visual reference`
3. `with pinterest-assisted query set`

검증 프로젝트:

- `signal-desk`: editorial 성향이 강한 workspace + landing surface
- `glacier`: dense enterprise dashboard + technical landing surface

## 검증 방법

비교 시 기존 샘플 빌드를 덮어쓰지 않기 위해 임시 복제본을 `tmp/visual_validation` 아래에 만들고 실행했다.

실행 흐름:

```bash
python -m design_ontology_harness.cli analyze-visuals --project-dir projects/signal-desk
python -m design_ontology_harness.cli analyze-visuals --project-dir projects/glacier

python -m design_ontology_harness.cli run-project --project-dir tmp/visual_validation/<project>/no-visual --kb-dir kb/default
python -m design_ontology_harness.cli run-project --project-dir tmp/visual_validation/<project>/local-visual --kb-dir kb/default

python -m design_ontology_harness.cli generate-visual-queries \
  --project-dir tmp/visual_validation/<project>/local-visual \
  --spec tmp/visual_validation/<project>/local-visual/spec.md \
  --output-dir tmp/visual_validation/<project>/local-visual/build/visuals
```

로컬 visual reference는 각 프로젝트에 추가한 SVG reference 세트를 사용했다.

- `signal-desk`: [editorial-dashboard-split-pane.svg](../projects/signal-desk/references/visual/editorial-dashboard-split-pane.svg), [landing-hero-serif-trust-strip.svg](../projects/signal-desk/references/visual/landing-hero-serif-trust-strip.svg)
- `glacier`: [ops-dashboard-verified-grid.svg](../projects/glacier/references/visual/ops-dashboard-verified-grid.svg), [audit-log-dense-table.svg](../projects/glacier/references/visual/audit-log-dense-table.svg)

## 결과 요약

### Signal Desk

| Scenario | Density | Surface Language | Tone Alignment | Card Hierarchy / Component Emphasis |
|---|---|---|---|---|
| without visual reference | 없음 | 없음 | KB + brand keyword만 사용 | visual hint 없음 |
| with local visual reference | `airy` | `tinted` | `editorial` typography mood | low-elevation tinted cards, split-pane/navigation emphasis, restrained data-display hierarchy |
| with pinterest-assisted query set | query 16개 생성 | editorial / document writing / kanban / review panel 축 강화 | 검색 단계부터 editorial, calm, trustworthy tone 보강 | `pinterest_assist_plan.json`에 guardrail 4종 포함 |

대표 query:

- `editorial precise content authoring editor ui`
- `calm trustworthy document writing interface`
- `editorial text-first data review table ui`
- `editorial precise kanban board ui`

로컬 visual을 연결했을 때 `design_system_blueprint.json`에 아래가 채워졌다.

- density: `airy`
- surface style: `tinted`
- typography mood: `editorial`
- top layout cue: `dashboard-grid`
- component style hints: `cards`, `data_display`, `navigation`, `typography`

카드/위계 방향은 다음처럼 분화되었다.

- cards: `low-elevation tinted cards`
- typography: headline rhythm과 본문 리듬 대비를 키우는 editorial hierarchy
- data-display: thin divider + restrained accent 중심

### Glacier

| Scenario | Density | Surface Language | Tone Alignment | Card Hierarchy / Component Emphasis |
|---|---|---|---|---|
| without visual reference | 없음 | 없음 | KB + brand keyword만 사용 | visual hint 없음 |
| with local visual reference | `dense` | `flat` | `utilitarian` typography mood | flat cards, thin divider 중심 hierarchy, compact nav/filter density |
| with pinterest-assisted query set | query 16개 생성 | data review / ops control / pricing / FAQ 축 강화 | precise, minimal, technical tone 반영 | `pinterest_assist_plan.json`에 guardrail 4종 포함 |

대표 query:

- `precise structured data review table ui`
- `minimal clean operations control panel`
- `dense data tables structured form layout`
- `text-first hierarchy saas landing hero`

로컬 visual을 연결했을 때 `design_system_blueprint.json`에 아래가 채워졌다.

- density: `dense`
- surface style: `flat`
- typography mood: `utilitarian`
- top layout cue: `dashboard-grid`
- component style hints: `cards`, `data_display`, `navigation`, `typography`

카드/위계 방향은 다음처럼 분화되었다.

- cards: shadow보다 flush plane + thin divider 중심
- navigation: compact scope indication 우선
- typography: scale 차이를 줄이고 label 정렬 정확도를 우선
- data-display: chart/table framing을 촘촘하게 유지

## 비교 관찰

1. 같은 KB를 써도 local visual reference가 들어오면 visual language가 실제로 분화된다.
   Signal Desk는 `airy + tinted + editorial`, Glacier는 `dense + flat + utilitarian`으로 분리됐다.

2. 차이는 단순 mood 설명이 아니라 component hint까지 내려온다.
   `component_specs.md`에는 `card_elevation_tendency`, `filter_nav_density`, `chart_panel_framing`, `cta_prominence` 같은 adaptation hint가 들어가고 `provenance=inferred`가 함께 기록된다.

3. baseline인 `without visual reference`에서는 visual language 섹션이 비어 있다.
   즉 기존 KB/spec 기반 산출물은 유지되지만, density / surface / card hierarchy 같은 표현 계층 정보는 보강되지 않는다.

4. Pinterest-assisted 단계는 truth source가 아니라 search-assist 역할로 동작한다.
   plan/manifest에는 아래 guardrail이 함께 생성된다.
   `auth-and-dynamic-loading`, `volatile-search-results`, `copyright-and-redistribution`, `robots-and-access-constraints`

## 결론

- `V-13`: 샘플 프로젝트 2종 검증 완료
- `V-14`: without / with local visual / with pinterest-assisted query 비교 리포트 완료

현재 구현은 다음을 만족한다.

- 공식 KB와 spec은 구조적 source of truth로 유지
- local visual reference는 density / surface / tone / hierarchy를 보강
- Pinterest는 query 생성과 선택 보조에 머무르고, 직접 분석 입력은 여전히 로컬 파일에 고정
- image-derived signal은 `observed` / `inferred` / `unverified` provenance 문맥으로 추적 가능
