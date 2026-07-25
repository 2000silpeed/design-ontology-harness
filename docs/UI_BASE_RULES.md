# UI Base Rules

이 문서는 하네스가 구현물에 기본으로 요구하는 가독성 하한을 정의한다. 토큰 바인딩은 값의 출처를 증명할 뿐이고, 바인딩된 값이 실제로 읽히는지는 따로 판정해야 한다. 그 판정을 `lint-implementation`의 `DS100`~`DS107`이 맡는다.

기준선은 Adham Dannaway의 [UI design tips](https://www.adhamdannaway.com/blog/ui-design/ui-design-tips) 16개 항목이다. 그중 라틴 조판 전제에 기대는 항목은 그대로 옮기지 않고 한글 기준으로 치환했다.

## 이미 다른 규칙이 강제하는 항목

새 코드를 만들지 않았다. 원문 팁과 대응 규칙만 기록한다.

| 원문 팁 | 대응 |
|---|---|
| 색을 목적 있게 쓴다 | `DS001`/`DS002`/`DS003` — 하드코딩 색 금지, `--ds-color-*` 강제 |
| 순수 검정을 피한다 | 런타임 `ink` 역할이 `#0F172A` (`docs/color-reference.md`) |
| regular/bold만 쓴다 | `DS092` — 500과 600을 한 화면에서 함께 쓰는 것 차단 |
| 명확한 시각 위계를 만든다 | `DS093` — display tier 없는 압축 타입스케일 차단 |
| 불필요한 스타일을 제거한다 | `DS090`(콜아웃 인용 바), `DS096`(엣지 세로 바), `DS091`(radius monoculture) |
| 일관성을 유지한다 | 토큰 바인딩 체계 전체 |

## 기본 규칙

| 코드 | 판정 | 임계값 | 예외 |
|---|---|---|---|
| `DS100` | 본문 슬롯의 `line-height` | 라틴 1.5 / 한글 1.6 | display·헤딩·라벨·수치 슬롯 |
| `DS101` | 같은 블록의 전경/배경 토큰 대비비 | 4.5:1, 큰 텍스트 3:1 | 배경을 상속받는 블록(판정 불가) |
| `DS102` | 컨트롤 경계선 대비비 | 3:1 | 테두리 토큰 = 배경 토큰인 채움형 컨트롤, 장식용 divider |
| `DS103` | 상태 표시등의 상태 구분 단서 | 색 외 단서 1개 이상 | 글자·글리프가 인접한 표시등, 형태·테두리가 다른 변형 |
| `DS104` | 한 **화면**의 텍스트 서체 수 | 2종 이하 | mono, 한글/라틴 로케일 페어링 |
| `DS105` | 한글 읽기 슬롯의 `letter-spacing` | -0.02em ~ 0 | `text-transform: uppercase` 선언이 있는 블록, 워드마크·날짜·수치 슬롯 |
| `DS106` | 한글 표면의 줄바꿈 계약 | `word-break: keep-all` 존재 | 한글이 없는 구현 |
| `DS107` | `text-align: justify` | 사용 금지 | 없음 |

### 대비비 판정 방식

`DS101`과 `DS102`는 설치된 `design-system/tokens.css`를 읽어 `var(--ds-color-*)`를 실제 hex로 해석한 뒤 WCAG 상대휘도로 계산한다. `html[data-theme="dark"]` 블록의 오버라이드까지 반영하므로, 라이트에서만 통과하고 다크에서 무너지는 쌍도 걸린다.

큰 텍스트 완화(3:1)는 같은 블록에서 `font-size`가 확인될 때만 적용한다. 24px(1.5rem) 이상이거나, 18px(1.125rem) 이상이면서 `font-weight`가 700 이상인 경우다.

`DS102`가 컨트롤 셀렉터에만 적용되는 이유는 WCAG 1.4.11의 범위 때문이다. 카드 경계선처럼 컨트롤 식별에 필요하지 않은 선은 대상이 아니다. 반대로 입력창과 고스트 버튼의 경계선은 그 컨트롤을 식별하는 유일한 단서이므로 3:1을 넘겨야 한다.

### 경계색 역할 분리

런타임 색 정책이 두 역할을 다르게 취급한다.

- `--ds-color-border` — 장식용 헤어라인. 하한 대상이 아니다. 카드 테두리, 행 구분선, 섹션 분리선용이다. 컨트롤 경계에 쓰면 `DS102`가 걸린다.
- `--ds-color-border-strong` — 컨트롤 경계. `non_text_contrast_floor`가 `surface`·`canvas`·`surface-muted` 세 배경 모두에서 3:1 위로 유지한다. 폼 필드, 버튼, 셀렉트, 토글의 테두리는 이 역할에 묶는다.

이 분리가 없으면 두 선택지밖에 없다. 모든 구분선을 진하게 만들어 시각 체계를 망치거나, 컨트롤 경계를 포기하거나. WCAG는 전자를 요구하지 않는다.

두 하한은 `docs/color-reference.md`의 checksum 검증된 정책 블록에 있고, 라이트와 `dark_derivation` 양쪽에 선언된다. 정책을 고치면 checksum도 다시 계산해야 한다.

### 판정 단위

`DS104`는 화면 단위로 센다. HTML 진입점과 그것이 링크한 스타일시트를 한 묶음으로 보고, 프레임워크 앱처럼 링크 태그가 없으면 전체를 한 화면으로 본다. 한 프로젝트에 독립된 목업 여러 개가 있을 때 전부 합산하면 각자 2종씩 쓰는 화면 셋이 3종 위반으로 잡힌다.

`DS100`은 셀렉터 이름이 아니라 블록 안의 실제 `font-size`로 본문 여부를 가른다. 28px(1.75rem) 이상은 display 조판이고 좁은 행간이 정답이다. `clamp()`는 하한을 기준으로 본다. 이름이 `.thumb-copy strong`이어도 92px 헤드라인은 본문이 아니다.

## 한글 표면 판정

한글 여부는 파일 단위가 아니라 **구현 단위**로 본다. 한글 카피는 마크업에 있고 조판은 스타일시트에 있어서, 파일별로 나누면 정작 규칙이 필요한 CSS가 라틴으로 분류된다.

판정 기준은 소스 자체의 한글 검출이다. 관리 블록(`design-ontology:START`~`END`)과 주석을 지운 뒤 한글 20자 이상이면 한글 표면으로 본다. 주석 한 줄에 한글이 섞였다고 규칙이 바뀌지 않는다.

## 라틴 전제가 깨지는 항목

원문 팁 3개는 한글에 대응물이 없다. 그대로 옮기면 무의미하거나 해롭다.

**x-height가 큰 서체를 고른다.** 한글에는 x-height 개념이 없다. 판단 기준은 자소 균형과 작은 크기에서의 가독성이다. `design_ontology_harness/font_reference.py`의 `KOREAN_TYPOGRAPHY_PROFILES`가 서체별로 이 값을 들고 있고, `korean_context.small_size`가 각 서체의 하한 크기를 기록한다. 규칙으로 코드화하지 않고 서체 선택 단계의 판단 근거로 둔다.

**대문자 사용을 자제한다.** 한글에는 대소문자가 없다. 한글에서 같은 실패를 만드는 것은 양수 자간이다. 어절 덩어리가 풀리면 읽기 단위가 무너진다. 그래서 `DS105`는 대문자가 아니라 자간을 본다. 역방향으로, `text-transform: uppercase` 선언이 있는 블록은 라틴 전용 슬롯이라는 증거로 읽고 자간 규칙에서 면제한다. 한글에 uppercase는 아무 효과가 없는 선언이기 때문이다.

`text-transform: uppercase` 자체를 금지하지는 않는다. 하네스가 `component_specs.py`에서 일부 컴포넌트에 이 선언을 직접 생성하므로, 금지 규칙을 만들면 생성물이 자기 린트에 걸린다.

**행간 1.5 이상.** 한글은 받침이 베이스라인 아래로 내려가서 같은 `font-size`에서 실제 자면 높이가 라틴보다 크다. 1.5는 한글 본문에서 답답하다. 서체별 권장 범위는 `KOREAN_TYPOGRAPHY_PROFILES`의 `body_line_height`에 있고(Pretendard 1.6-1.7, Noto Serif KR 1.7-1.9 등), 규칙의 하한은 그 최솟값인 1.6으로 잡았다.

**줄바꿈 계약(원문에 없는 항목).** `word-break: keep-all`이 없으면 한글이 어절 중간에서 잘린다. 라틴에는 없는 실패 모드라 원문에 항목이 없지만, 한글 기본 규칙에서는 빠질 수 없다. `resolve_font_system`이 이미 `script_guardrails.wrap`으로 이 계약을 만들고 있었고, `DS106`이 그것을 구현 단계까지 전달한다.

## 토큰

`emit-tokens`가 규칙과 같은 하한으로 본문 조판 기본값을 방출한다. 구현은 숫자를 직접 쓰지 않고 이 토큰을 소비하면 된다.

```css
--ds-leading-tight: 1.2;      /* display 전용 */
--ds-leading-body: 1.6;       /* 본문 기본. 한글이면 1.6, 라틴이면 1.5 하한 */
--ds-leading-relaxed: 1.75;
--ds-tracking-body: 0em;      /* 한글은 서체 권장 자간(양수는 0으로 고정), 라틴은 normal */
--ds-wrap-word-break: keep-all;  /* 한글 프로젝트만 */
--ds-wrap-overflow: normal;      /* 한글 프로젝트만 */
```

`--ds-leading-body`의 하한은 `implementation_linter`의 `BODY_LINE_HEIGHT_FLOOR`와 `BODY_LINE_HEIGHT_FLOOR_HANGUL`을 그대로 가져온다. 생성기가 게이트보다 낮은 값을 내보내면 자기 산출물이 자기 린트에 걸리므로, 상수는 한 곳에만 둔다.

한글 프로젝트의 값은 `script_guardrails.body_font`와 `script_guardrails.wrap.body`에서 온다. 서체를 바꾸면 토큰 값도 따라 바뀐다.

## 실행

```bash
uv run design-ontology emit-tokens --project-dir projects/<name>
uv run design-ontology lint-implementation --target-repo <implementation-repo>
```

## 규칙이 걸렸을 때

- `DS100`이 나오면 값을 살짝 올리는 데서 멈추지 말고 `var(--ds-leading-body)`로 바인딩한다. 개별 숫자를 손보면 다음 화면에서 같은 일이 반복된다.
- `DS101`이 다크에서만 나오면 텍스트 색을 흐리게 조정하지 말고, 두 모드 모두에서 하한을 넘는 ink 역할로 다시 지정한다.
- `DS102`가 나오면 경계선 두께를 키우지 말고 `--ds-color-border-strong`으로 바꾼다. 정책이 그 역할을 3:1 위로 유지하므로 구현에서 색을 새로 만들 필요가 없다. 토큰을 다시 방출하지 않은 프로젝트라면 `emit-tokens`를 먼저 돌린다.
- `DS103`이 나오면 색을 더 진하게 만들지 말고 형태나 글자를 추가한다.
- `DS105`, `DS106`이 나오면 개별 블록을 고치는 대신 본문 슬롯이 `--ds-tracking-body`와 `--ds-wrap-*`를 소비하는지 확인한다.
