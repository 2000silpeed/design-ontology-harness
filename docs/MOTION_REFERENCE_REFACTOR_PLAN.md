# VibeCoding 모션 레퍼런스 — 점검 결과와 리팩토링 계획

작성일: 2026-08-12
대상 저장소: `design-ontology-harness`
관련 커밋: `706e606`(팩 추가) `4d2a5d3`(대시보드 픽스처) `587cb73`(interaction resolver) `cb90a71` `1f6112c`(Memory Garden)

> **진행 상황 (2026-08-12)** — 단계 0~7 전부 완료, 테스트 680 통과.
> 파일럿 두 개는 lint clean이고, 남은 항목은 §9 끝에 정리했다.

## 0. 한 줄 결론

팩은 만들어졌지만 **선택 엔진도, 토큰 방출기도, 구현 CSS도 그것을 읽지 않는다.**
그래서 5개 사이트에서 뽑은 후보는 "최적을 고르기 위한 풀"이 아니라 테스트만 통과하는 고립된 fixture로 남았고,
정작 화면의 모션은 `token_emitter.py`에 하드코딩된 상수 두 개(`120ms` / `180ms`)로 전 프로젝트가 수렴했다.
의도와 정반대 결과다.

## 1. 지금 무엇이 어디에 있나

| 산출물 | 경로 | 상태 |
|---|---|---|
| 팩 데이터 | `design_ontology_harness/resources/vibecoding-motion-reference.json` | 소스 5 · 패턴 5 · 규칙 5, `status: draft` |
| 로더/검증기 | `design_ontology_harness/motion_reference.py` | 프로덕션 코드에서 **import 0회** (테스트만 사용) |
| 문서 | `docs/VIBECODING_MOTION_REFERENCE_PACK.md` | 파이프라인 연결 언급 없음 |
| 파일럿 A | `projects/orbit/motion-fixture/` | 팩을 읽지 않고 자체 CSS 변수로 재구현 |
| 파일럿 B | `projects/memory-garden/` | 선택 결과 JSON은 있으나 화면에 도달하지 않음 |

## 2. 실측 증거

전 프로젝트 CSS/HTML을 훑은 수치다. 판단이 아니라 측정값이다.

**모션 토큰 참조 횟수: 0**

```
find projects -name "*.css" -o -name "*.html" | xargs grep -oh "var(--ds-\(duration\|ease\)[^)]*)"
→ 결과 없음
```

색(`--ds-color-*`), 서체(`--ds-font-*`), 라운딩(`--ds-radius-*`)은 린터가 하드코딩을 실패 처리하는데,
모션 토큰만 방출되고 아무도 쓰지 않는다. `tokens.css`의 모션 3줄은 죽은 선언이다.

**대신 리터럴이 복제됐다**

| 값 | 등장 | 비고 |
|---|---:|---|
| `cubic-bezier(0.2, 0, 0, 1)` | 39회 | `--ds-ease-standard`와 같은 값을 var() 대신 복붙 |
| `180ms` | 43회 | emitter 하드코딩 값 |
| `120ms` | 40회 | emitter 하드코딩 값 |
| `160ms` | 15회 | 어느 스케일에도 없는 값 |
| `ease` / `ease-in-out` / `ease-in` / `ease-out` | 71회 | 토큰 밖 임의 easing |
| `140/150/200/220/300/4400ms` | 10회 | 스케일 밖 |

180/120에 압도적으로 몰린 것은 취향이 수렴한 게 아니라 **선택지가 그 둘뿐이었기 때문**이다.
`token_emitter.py:541-543`이 duration 두 개와 easing 한 개만 하드코딩으로 내보낸다.

**게이트가 이 경로에 적용되지 않았다**

팩의 대시보드 파일럿에 기존 린터를 돌려본 결과:

```
uv run design-ontology lint-implementation --target-repo projects/orbit/motion-fixture
→ DS111 4건 (reduced-motion 폴백 없는 애니메이션)
   DS001/DS002/DS003 다수 (하드코딩 색)
   DS010 (하드코딩 서체) · DS020 3건 (하드코딩 radius) · DS043
```

파일럿은 린트를 통과한 적이 없다. `styles.css`에 `prefers-reduced-motion` 블록 자체가 없는데,
이는 팩이 스스로 필수(`severity: required`)로 정한 `a11y:motion-reduce` 규칙 위반이다.

## 3. 왜 "반영이 안 되는" 것처럼 보이나 — 네 갈래로 갈라진 모션 소스

모션 값이 서로 모르는 네 곳에 따로 산다.

```
① 팩 JSON            duration 120/180/240 · easing 4종 · reduced 3종
                     └─ 읽는 프로덕션 코드 없음
② interaction_resolver.py:29-79
                     motion_cost 정수(1~2)만 · duration/easing 없음
                     팩은 advisory_reference 문자열로만 참조
③ token_emitter.py:541-543
                     --ds-duration-120 / -180 / --ds-ease-standard 하드코딩
④ 구현 CSS          전부 리터럴, ①②③ 어느 것도 참조 안 함
```

①을 고쳐도 ②는 안 바뀌고, ②가 무엇을 골라도 ③은 그대로이며, ③이 무엇을 내보내도 ④는 리터럴을 쓴다.
**어느 층을 수정해도 화면이 바뀌지 않는 구조다.** 사용자가 체감한 "반영 안 됨"의 물리적 실체가 이것이다.

### 3.1 선택 결과가 화면에 도달하지 않는 지점

`projects/memory-garden/preview/index.html:94-100`이 선택 JSON을 fetch해 `data-interaction` 속성에 붙인다.
그런데 그 속성을 소비하는 CSS는 `styles.css:124` **한 줄뿐**이고, 그마저도

- CSS에 있는 규칙: `season-transition`
- 이번 실행이 실제로 고른 것: `async-care-progress`, `care-emphasis`

선택된 두 패턴에 대응하는 규칙은 존재하지 않는다. 무엇을 고르든 화면은 동일하다.
게다가 fetch 기반이라 `file://`로 열면 CORS로 실패하고 `catch`에서 빈 문자열이 들어간다.

### 3.2 후보 풀이 한 프로젝트에 묶여 있다

`interaction_resolver.py`의 `CANDIDATES`가 `applies_to`로 지목하는 컴포넌트는
`living-timeline`, `season-lens`, `memory-seed-composer`, `decision-stone-editor`, `return-ritual-prompt`, `context-drawer` —
전부 Memory Garden 고유 이름이다. 다른 프로젝트에서 돌리면 `covered_components`가 비어
`no-compatible-candidate`로 떨어진다.

실제로 46개 프로젝트 중 `interaction_selection.json`을 가진 곳은 **memory-garden 1개**다.

## 4. "최적 선택"이 성립하지 않는 이유

결정론적 템플릿을 피하려고 만든 장치인데, 최적화 루프의 네 조건이 모두 비어 있다.

**고를 것이 없다.** 후보 5개가 각기 다른 컴포넌트/상태를 담당해서 사실상 경쟁하지 않는다.
Memory Garden 실행 로그를 보면 5개 중 5개가 스코어링을 통과했고 상위 2개가 채택됐다.
동점자 중 무작위 선택(`random.SystemRandom()`)이 일어나긴 하지만, 축마다 후보가 하나씩이라 선택의 여지가 없다.

**고른 결과를 볼 수 없다.** 3.1에서 본 대로 선택이 구현으로 내려가지 않는다.
A를 골랐을 때와 B를 골랐을 때의 화면이 같으면 비교 자체가 불가능하다.

**어느 쪽이 나았는지 판정하지 않는다.** `aesthetic_loop.py`의 평가 차원은
`visual_harmony` / `clarity` / `brand_fit` / `emotional_appeal` / `craft_quality` / `novelty` 6개인데
interaction·motion 차원이 없다. 모션이 좋았는지 나빴는지 점수화되지 않는다.

**학습이 누적되지 않는다.** 선택은 매 실행 무작위로 흔들리는데 결과 기록이 없어서
좋았던 선택이 다음 실행의 사전확률로 이어지지 않는다. 발산만 있고 수렴 신호가 없다.

여기에 더해 **모션은 발산 게이트의 사각지대**다.
`style_fingerprint.py`에는 `motion` / `animation` / `duration` / `easing` 문자열이 **0회** 등장한다.
지문에 잡히는 축은 surface tone, accent hue, 폰트 페어링, radius, separation, composition뿐이라
모든 프로젝트가 동일한 `180ms + cubic-bezier(0.2,0,0,1)`을 써도 `check-style-divergence`는 통과시킨다.
색과 서체의 수렴은 막으면서 모션의 수렴은 감지조차 못 하는 상태다.

## 5. 상용 수준 / AI 느낌 제거 관점에서 본 결함

선택 축 자체가 목표와 어긋나 있다. 현재 후보의 변별 속성은 `motion_cost`(1 또는 2)와 컴포넌트/상태 매칭뿐인데,
상용 사이트와 AI가 만든 사이트를 가르는 것은 그 축이 아니다. 실제로 갈리는 지점은 다음과 같다.

- **인과성** — 지금 왜 움직이는가. 상태가 바뀌어서 움직이는 모션과, 그냥 살아 있어 보이려고 움직이는 모션.
- **위계** — 한 화면에 주된 움직임 하나와 미세한 보조 반응. AI 결과물은 모든 요소가 동등하게 움직인다.
- **진입/퇴장 비대칭** — 상용은 들어올 때와 나갈 때 속도가 다르다. 현재 팩의 easing 4종은 이를 표현할 수 있는데 구현에서 전혀 쓰이지 않는다.
- **정지 상태의 완성도** — 모션을 다 끄고도 위계가 읽히는가. 움직임으로 빈약한 레이아웃을 덮는 것이 AI 느낌의 핵심 원인이다.
- **장식 루프 부재** — 현재 코드베이스에 `infinite` 선언이 31개 있고, `memory-garden/preview/effects.css:13`의 `focus-breathe 2.8s ease-in-out infinite`는 팩이 정한 duration 상한(320ms)과 `attention-border` 가드레일("기본 장식으로 쓰지 말 것")을 동시에 위반한다. 그런데 reduced-motion 폴백이 있어서 린터 DS111은 통과한다.

팩에는 이 축들이 없다. `duration_ms` / `easing` / `reduced_motion` 세 필드만으로는 "상용답게"를 선택할 수 없다.

부수적으로 **팩 스키마 자체의 결함**도 있다. `motion_reference.py:80`이 duration을 `0 <= d <= 320`으로 강제하는데,
로딩 루프는 본래 1초 이상이 정상이다(`dot-wave 1.2s`, `progress-sweep 1.6s`).
그래서 파일럿은 팩을 따를 수 없어 팩 밖에서 구현했다. 전이(transition)와 루프(loop)의 시간 예산을 분리해야 한다.

## 6. 리팩토링 계획

효과 순으로 배치했다. 1~2는 모든 프로젝트에 즉시 영향을 주고, 3~4가 "반영 안 됨"의 근본 해결이며, 5~6이 최적 선택 루프를 닫는다.

### 단계 0 — 소스 확정 (교착 해소)

지금 5개 소스 모두 `canonical_url: null` / `license_status: unverified`라 팩이 `draft`에 묶여 있고,
문서는 draft를 승격하지 말라고 못박아서 파이프라인에 붙일 수 없는 자기참조 교착 상태다.

각 사이트의 정식 URL과 라이선스를 확인해 `reference-only`로 승격한다.
어휘와 형태를 참조하는 데에는 코드 재배포 권한이 필요 없으므로 `verified`까지 갈 필요는 없다.

### 단계 1 — 모션을 blueprint 소유로 이관 ★

`token_emitter.py:538-544`의 하드코딩 3줄을 제거하고, 색·서체·spacing과 동일하게 blueprint의
`motion_system`에서 방출한다. 내보낼 것:

```
--ds-duration-80 / -120 / -180 / -240 / -320      전이 예산
--ds-loop-slow / -medium / -fast                  루프 예산 (별도 네임스페이스)
--ds-ease-standard / -enter / -exit / -emphasized  4종 전부
--ds-motion-reduced-strategy                       static | opacity-only | skip
```

구현 CSS가 참조할 값이 생기는 것이 핵심이다. 지금은 쓰고 싶어도 쓸 값이 없어서 리터럴로 회귀한다.

### 단계 2 — 린터에 모션 토큰 바인딩 규칙 추가

색(DS001)·서체(DS010)·라운딩(DS020)과 같은 등급으로 올린다.

- `DS112` 하드코딩 duration — `var(--ds-duration-*)` / `var(--ds-loop-*)` 사용 강제
- `DS113` 하드코딩 easing — `var(--ds-ease-*)` 사용 강제
- `DS114` 장식 루프 — `infinite` 선언은 로딩·진행 상태로 역할이 선언된 경우에만 허용

기존 리터럴 123건(180×43, 120×40, cubic-bezier×39 등)이 한꺼번에 걸리므로 마이그레이션 배치를 함께 준비한다.
신규 프로젝트부터 강제하고 기존은 경고로 두는 단계적 적용을 권한다.

### 단계 3 — 후보 풀을 팩에서 읽고, 프로젝트 독립으로 만들기

`interaction_resolver.py`의 `CANDIDATES` 하드코딩을 없애고 팩의 `patterns`를 후보로 로드한다.
이중 소스를 하나로 합치는 작업이다.

동시에 `applies_to`를 프로젝트 고유 컴포넌트명이 아니라 **역할 어휘**로 바꾼다.

```
현재: living-timeline, season-lens, memory-seed-composer, ...   (memory-garden 전용)
변경: list-surface, detail-panel, async-action, selection-target,
      status-region, showcase-surface, ...                       (모든 프로젝트 공통)
```

프로젝트 컴포넌트는 `component_specs`에서 역할로 매핑한다. 그래야 46개 프로젝트에서 후보가 매칭된다.

후보 수도 늘려야 한다. 지금은 축마다 하나라 경쟁이 없다. 최소한 **진입 · 강조 · 진행 · 전환** 네 축에 각 3~5개를 두어야
"동점자 중 무작위 선택"이 의미를 갖는다.

### 단계 4 — 선택을 구현에 강제 연결 ★

fetch + `data-interaction` 속성 방식을 버리고, 선택 결과를 빌드 산출물로 내보낸다.

- `design-system/interactions.css` — 선택된 패턴의 실제 CSS 규칙만 포함. 토큰만 참조.
- `INTERACTION.md` — 구현 에이전트가 읽는 계약. 무엇을 왜 골랐고 무엇을 쓰면 안 되는지.

린터 규칙을 함께 추가한다.

- `DS115` 선택된 패턴이 구현되지 않음
- `DS116` 선택되지 않은 패턴이 구현됨 (지금 memory-garden의 `season-transition`이 여기 걸린다)

이 단계가 끝나야 "선택을 바꾸면 화면이 바뀐다"가 성립한다.

### 단계 5 — 모션을 발산 게이트에 편입

`style_fingerprint.py`의 `StyleFingerprint`에 모션 지문을 추가한다.

```
duration_values_ms        분포
easing_signatures         종류와 빈도
has_decorative_loop       장식 루프 유무
transition_properties     무엇을 전이시키는가
enter_exit_asymmetry      진입/퇴장 속도 비율
```

그러면 "모든 프로젝트가 180ms + cubic-bezier(0.2,0,0,1)"이라는 현재의 수렴이 자동으로 검출된다.
색·서체에 이미 있는 anti-convergence 장치를 모션에 확장하는 것이므로 구조 변경은 필요 없다.

### 단계 6 — 평가 차원 추가로 루프 닫기 ★

`aesthetic_loop.py`의 `DEFAULT_DIMENSIONS`에 `interaction_quality`를 추가한다.
5절에서 정리한 축을 그대로 메트릭으로 쓴다.

```
causality           상태 변화에 결속된 모션인가
hierarchy           주 동작 하나 + 보조 미세반응인가
static_completeness 모션을 끈 상태에서 위계가 읽히는가
no_decoration_loop  장식 목적 무한 루프가 없는가
reduced_coverage    reduced-motion 대응이 선언된 전략과 일치하는가
```

그리고 선택된 후보 id를 평가 점수와 함께 registry에 기록한다.
다음 실행에서 이 기록을 사전확률로 사용하면, 무작위 발산이 **근거 있는 선택**으로 바뀐다.
결정론을 피하면서 최적에 수렴하는 구조가 여기서 완성된다.

### 단계 7 — 파일럿 재작업

`orbit/motion-fixture`와 `memory-garden`을 새 경로로 다시 통과시킨다.
`lint-implementation` clean을 커밋 조건으로 걸어서, 파일럿이 게이트를 우회하는 현재 상황을 반복하지 않는다.

## 7. 검증 방법

각 단계가 실제로 작동했는지 확인하는 명령이다.

```bash
# 단계 1-2: 모션 토큰이 방출되고 참조되는가
uv run design-ontology emit-tokens --project-dir projects/<p>
grep -c "var(--ds-duration" projects/<p>/**/*.css      # 0이 아니어야 함
uv run design-ontology lint-implementation --target-repo projects/<p>

# 단계 3-4: 선택을 바꾸면 화면이 바뀌는가
uv run design-ontology synthesize --project-dir projects/<p> --variation-seed 1
diff <(cat projects/<p>/design-system/interactions.css) /tmp/seed1.css
uv run design-ontology synthesize --project-dir projects/<p> --variation-seed 2
# interactions.css가 달라져야 함

# 단계 5: 수렴이 검출되는가
uv run design-ontology fingerprint-style --project-dir projects/<p>
uv run design-ontology check-style-divergence --project-dir projects/<p>

# 단계 6: 평가가 되먹임되는가
uv run design-ontology aesthetic-loop --project-dir projects/<p> --candidate candidate.json
```

## 8. 우선순위 요약

| 순위 | 단계 | 해결하는 문제 | 영향 범위 |
|---|---|---|---|
| 1 | 1 · 2 | 모션 상수 수렴, 토큰 미사용 | 전 프로젝트 |
| 2 | 4 · 3 | 선택이 화면에 반영되지 않음 | 파이프라인 근본 |
| 3 | 6 · 5 | 최적 선택 루프 부재, AI 느낌 | 목표 직결 |
| 4 | 0 · 7 | 팩 승격 교착, 파일럿 부채 | 정리 |

단계 0은 언제든 병행 가능하고, 나머지는 위 순서를 지키는 편이 낫다.
특히 단계 1 없이 단계 4를 하면 `interactions.css`가 다시 리터럴로 채워진다.

## 9. 실행 결과 (2026-08-12)

### 완료

**단계 1 — 모션이 blueprint 소유가 됐다.**
`motion_reference.py`가 모션 시스템(전이 스케일 5단계, loop 예산 3단계, easing 4종,
reduced 전략)을 소유하고 `token_emitter.py`는 그것을 방출만 한다. 하드코딩 3줄은 사라졌다.
찾는 과정에서 **다섯 번째 모션 소스**가 드러났다: `component_specs.py`의 컴포넌트 계약이
`var(--duration-180)`을 지시하는데 방출되는 토큰은 `--ds-duration-180`이었다. 접두사가
달라 참조가 해석되지 않았고, 그래서 구현이 리터럴로 되돌아갔다. 네임스페이스를 `--ds-`로
통일했고, 이 불일치가 다시 생기지 않도록 회귀 테스트를 걸었다.

**단계 2 — DS112/113/114 추가.** 로컬 별칭을 따라가 `--ds-*`로 끝나지 않으면 사설
스케일로 판정한다. `orbit/motion-fixture`가 자체 `--duration-*`을 정의해 우회하던 경로가
이제 잡힌다.

**단계 3 — 후보 풀이 팩에서 온다.** 하드코딩 후보를 없애고 두 팩(하네스 기준 9개 +
vibecoding 4개 = 13개)에서 로드한다. `applies_to`를 프로젝트 고유 컴포넌트명에서 역할
어휘로 바꿔, 이제 어떤 프로젝트에서도 매칭된다. 축마다 최대 하나만 선택해 "한 화면에 주된
움직임 하나"를 구조로 만들었다. dense 표면은 `immediate-swap`(80ms)을, spacious 표면은
`staged-enter`(180ms)를 고르는 것을 확인했다.

**단계 4 — 선택이 CSS가 된다.** `interactions.css` + `INTERACTION.md`를 방출하고
DS115/DS116으로 선택과 구현의 일치를 강제한다. 생성기 자체가 자기 린터를 통과하지 못해
(stagger delay 리터럴, `inline-size` 전이, 자식 선택자 reduced-motion 누락) 8건을 고쳤다.

**단계 5 — 모션이 지문에 들어갔다.** `duration_values_ms`, `easing_signatures`,
`transition_properties`, `has_decorative_loop`, `enter_exit_asymmetry`를 추출하고
`compare_fingerprints`가 `motion_similarity`를 낸다. memory-garden의 2800ms 무한
호흡 애니메이션이 `has_decorative_loop=True`로 잡힌다.

**단계 6 — 루프가 닫혔다.** `interaction_quality` 차원(causality, hierarchy,
static_completeness, no_decoration_loop, reduced_coverage)을 추가하고 가중치를
재배분했다(합계 1.0). `interaction_outcomes.py`가 리뷰 점수를 기록하고, 관측 2회
이상인 패턴만 prior가 되어 동점을 가른다. `record-interaction-outcome` CLI로 기록한다.

이 과정에서 정직성 문제를 하나 처리했다. 스크린샷 채점기는 정지 이미지를 보므로
모션 인과성이나 장식 루프를 판정할 수 없다. `static_completeness`(모션을 껐을 때 위계가
남는가)만 실제로 측정하고 나머지는 중립값 + 명시적 note로 두었으며, 스크린샷 경로의
평가 게이트에서는 `interaction_quality` 차원을 아예 제외했다. 측정할 수 없는 축으로
게이트를 세우면 항상 막히거나 거짓 통과를 만든다.

### 단계 0 — 완료

5개 소스 전부 URL이 확정돼 팩이 `draft`를 벗어나 `reviewed`가 됐다.

| 소스 | URL | 상태 |
|---|---|---|
| Originkit | `https://www.originkit.dev` | inspected · reference-only |
| Magic UI (Border Beam) | `https://magicui.design` | inspected · **verified** (MIT) |
| MotionSites | `https://motionsites.ai` | inspected · reference-only · **유료** |
| Dot Matrix | `https://dotmatrix.zzzzshawn.cloud` | inspected · reference-only |
| VibeHub | `https://vibe-hub.org` | inspected · reference-only |

확인 과정에서 하나가 바뀌었다. "Border Beam"은 독립 패키지가 아니라 **Magic UI**의 컴포넌트였다
(사용자가 준 링크는 `magicui.design/docs/components/globe`). Magic UI는 MIT라 유일하게
`verified`이지만, 이 팩은 여전히 컴포넌트 코드가 아니라 어포던스와 상태 결속만 저장한다.

**MotionSites는 유료 상품이다.** 히어로 섹션 프롬프트를 파는 freemium 서비스이므로 프롬프트
전문·조각·미리보기 미디어를 저장소에 들이면 안 된다. `governance:license-before-reuse`가
이 경우를 위해 존재한다.

`stable`은 아직 비워 뒀다. 보수적인 reference-only 경계를 적용하는 대신 각 라이선스 전문을
실제로 읽어야 주장할 수 있는 상태다.

### 단계 7 — 완료

**`orbit/motion-fixture` 재작성.** 자체 `--duration-*` 변수와 하드코딩 색·서체·라운딩을
버리고 orbit의 `design-system/tokens.css`와 생성된 `interactions.css`를 링크한다.
대시보드 맥락이라 resolver가 enter 축에 `immediate-swap`(모션 없음)을 골랐고, fixture는
그 선택을 그대로 보여준다. `build_fixture.py`로 계약을 재생성할 수 있다. 위반 23건 → 0건.

**`memory-garden` 재합성.** blueprint가 v2 선택과 `motion_system`을 갖게 됐고
`interactions.css`가 실제로 채워졌다. 색상 결정은 바뀌지 않았다(`tokens.css` diff는 모션
토큰 11줄 추가뿐). preview는 `data-interaction` + `data-state` 계약으로 옮겼고,
`effects.css`는 상태 색상만 남기고 모션을 계약에 넘겼다.

여기서 원래 문제의 진원지를 제거했다. preview는 `interaction_selection.json`을 런타임에
fetch해 속성만 붙이고 있었다 — 무엇을 고르든 화면이 같았던 이유다. 이제 계약이 링크된
스타일시트로 오고, 같은 안티패턴이던 `design_language_selection` fetch도 마크업에 구웠다.
`file://`에서 나던 콘솔 에러도 사라졌다.

두 파일럿 모두 `lint-implementation` **OK**, 콘솔 에러 0, 렌더링 확인 완료.

**리터럴 마이그레이션.** 앞서 센 123건은 `build/kb/` 크롤 CSS와 `node_modules`가 섞인
수치였다. 실제 구현 CSS의 대상은 14건이었고 다음과 같이 정리했다.

| 프로젝트 | 처리 |
|---|---|
| gyeol-feed · agent-org-desk · fashion-curation-mobile | `0.25s ease` 4건 → `var(--ds-duration-240) var(--ds-ease-standard)` |
| signal-desk · glacier | 대상 아님 — reduced-motion 블록의 `.01ms !important` 관용구 |
| ai-chat-mobile-mock · ekos-static-prototype | blueprint가 없어 모션 토큰 자체가 없다. 재합성 전까지 보류 |

blueprint를 가진 36개 프로젝트는 `emit-tokens`를 다시 돌려 전체 모션 스케일을 갖췄다.

## 10. 후속 — 팔레트 수렴 (2026-08-12)

새 파이프라인으로 두 프로젝트(`shotline-desk` dense, `slowread-archive` spacious)를
end-to-end로 뽑아 검증했다. 모션과 레이아웃은 맥락에 따라 정확히 갈렸다.

| | shotline (dense) | slowread (spacious) |
|---|---|---|
| enter | `immediate-swap` 80ms | `staged-enter` 180ms |
| progress | `skeleton-placeholder` | **선택 안 됨** (async 상태 없음) |
| transition | `context-crossfade` | `anchored-shift` |
| 서체 | Pretendard + IBM Plex Mono | Noto Serif KR + Pretendard |

그런데 발산 게이트가 두 프로젝트를 `TOO-SIMILAR`(0.64)로 잡았다. **색이 수렴했다.**

### 원인

중성 역할(canvas/surface/border/ink)에 팔레트 후보가 없으면
`_runtime_policy_role()`이 고정 표에서 값을 가져왔다. 그 표는 Tailwind slate 계열
(`#F7F8FA` canvas, `#0F172A` ink, `#D6DDE6` border)이고, 생성된 blueprint는 역할을
`anchor_surface`·`paper_field` 같은 제품 의미 이름으로 붙이는 탓에 표준 semantic role
매핑이 거의 걸리지 않아 대부분의 프로젝트가 같은 회색을 실었다.

모든 화면이 같은 회색 위에 같은 잉크를 쓰는 것이 생성물 티의 가장 큰 원인이다.

### 처리

`_neutral_role()`이 브랜드 hue로 물들인 중성 램프를 만든다. 팔레트에 쓸 만한 중성색이
있으면 그대로 쓰고, 없을 때만 파생한다.

```
녹색 브랜드   canvas=#F8F9F9  border=#DDE2DF  ink=#1A211E
보라 브랜드   canvas=#F3F3F4  border=#D7D8DD  ink=#212229
앵커 없음     canvas=#F9F9F9  border=#DFDFDF  ink=#1D1D1D   (무채색으로 후퇴)
```

밝기 사다리는 브랜드 성격(`paper` / `clinical` / `deep`)에 따라 다르다. paper는 캔버스가
더 어둡고 surface가 순백이 아니다. tint는 중성으로 읽힐 만큼 낮게 유지하되, 화면 전체의
온도가 브랜드를 따라간다.

색 권한도 정리했다. 정책은 역할 집합과 `ink-inverse`를 소유하고, 상태색은 팔레트 우선,
중성색은 브랜드 파생이다. 텍스트 단계는 대비 보정에 기대지 않고 자체로 4.5:1을,
`border-strong`은 3:1을 넘도록 사다리를 잡았다.

결과: 발산 게이트 **OK** (0.64 → 0.61), 두 목업 모두 lint clean, 테스트 680 통과.

### 후속 2 — 중성색을 온톨로지가 소유하게 (2026-08-12)

hue 파생은 고정 회색보다 낫지만 온톨로지를 우회한 계산이었다. semantic-os의 color
도메인이 색을 소유해야 맞다. 다만 그 도메인은 REFERENCE X 기반 **브랜드 색 아카이브**라
채도 있는 색 위주였고, 저채도 ColorKeyword가 4개(밝기 0.32/0.40/0.58/0.93)뿐이라
중성 램프의 8단계를 채우지 못했다.

**semantic-os에 UI neutral ramp 22 cards를 추가했다.** warm(33°)·cool(218°)·true(무채)
세 램프 × paper·veil·line·edge·muted·ink 여섯 단계, 그리고 정책 2장과 토픽·레퍼런스.
REFERENCE X나 Pantone이 아니라 WCAG 대비 요구에서 계산으로 도출한 값임을 출처에 명시했다.
muted·ink는 자기 배경에서 4.5:1, edge는 3:1을 자체로 넘긴다.

그런데 램프가 세 온도뿐이라 두 프로젝트가 같은 cool 램프를 골랐다. 그래서 분업을 나눴다:
**온톨로지가 계단(명도·채도 구조)을 소유하고, 브랜드가 색조를 소유한다.** 고른 계단의
L·S를 유지한 채 hue만 브랜드로 바꾸면 램프 수와 무관하게 프로젝트마다 다른 중성색이 된다.
출처는 `Cool Paper (UI neutral) · 브랜드 색조`로 남는다.

결과: 중성 역할 **12/14가 온톨로지 출처, 파생 0개**. 하네스의 `border_strong` 밝기 하한은
53%로 낮췄다 — 3:1을 자체로 넘기는 계단은 58%보다 어두워서, 하한을 그대로 두면 접근성을
만족하는 온톨로지 색이 배제된다.

### 후속 3 — 지문이 잘못 세던 두 축 (2026-08-12)

중성색을 고친 뒤에도 게이트가 FAIL(0.65)이었고, 원인은 지문 자체의 결함이었다.

**`surface_tone`이 실제 톤을 버리고 있었다.** `:root`와 `html[data-theme="dark"]`가
둘 다 있으면 측정한 톤을 `dual-theme`으로 덮어썼는데, `emit-tokens`는 항상 두 블록을
만든다. 결과적으로 모든 프로젝트가 같은 값을 갖고, 그 축이 아무것도 구분하지 못하면서
유사도에는 0.22를 계속 더했다. 다크 지원은 `supports_dark_theme` 필드로 분리하고 톤은
측정값을 유지하게 했다. 재계산하니 18개 프로젝트가 neutral-light 11 · cool-tinted 3 ·
dark 2 · warm-paper 1 · rose-tinted 1로 갈렸다.

**accent 지문이 CSS의 모든 채도 색을 담고 있었다.** 상태색, link, 텍스트색(Moss Green),
다크 모드 값까지 들어가서 토큰을 제대로 쓰는 프로젝트일수록 서로 닮아 보였다. 빨강이
위험을 뜻하는 건 의미가 정한 것이라 공유가 수렴이 아니다. 이제 `:root` 블록의
`--ds-color-(primary|accent|brand-*|support-*)`만 센다. 디자인 시스템 토큰이 없는
수작업 CSS는 기존 스캔으로 후퇴해 attractor 검출이 계속 동작한다.

결과: `slowread-archive` vs `shotline-desk` 유사도 **0.65 → 0.34**, 두 프로젝트 모두
발산 게이트 **OK**. 등록된 18개 프로젝트를 새 방식으로 재지문했다.

### 남은 작업

**팔레트 시드는 불필요했다.** 두 번 연속 합성해 확인한 결과 색 선택은 이미 결정론적이다
(색 모듈에 난수가 없다). 앞서 값이 달라진 것은 코드 변경 때문이었다.

`ai-chat-mobile-mock`과 `ekos-static-prototype`은 blueprint가 없어 토큰 바인딩 자체가
불가능하다. 두 목업을 계속 쓸 것이라면 먼저 프로젝트를 합성해야 하고, 아니라면 정리
대상으로 두는 편이 낫다. 판단이 필요한 항목이라 임의로 진행하지 않았다.
