---
name: design-ontology-mockup-builder
description: Build a professional app mockup UI from a product concept using the design-ontology-harness pipeline with enforced token binding and cross-project style divergence gates. Use when the user asks to create a mockup/prototype UI for an app concept, when generated mockups keep repeating the same components/colors/fonts, or after design-ontology-concept-author has produced brand_profile.json. This skill replaces free-hand mockup styling — the implementing LLM must consume generated tokens.css and pass lint-implementation and check-style-divergence before declaring the mockup done.
---

# Design Ontology Mockup Builder

## Why this skill exists

과거 목업들은 blueprint가 프로젝트마다 다른 팔레트를 생성했는데도, 구현 단계에서
LLM이 자기 기본 미감(크림/페이퍼 배경 + 옥스블러드 + 틸 + 시트론 + 세리프 디스플레이 +
Pretendard/Noto Serif KR)으로 회귀해 매번 같은 화면이 나왔다.

이 스킬의 규칙은 하나다: **구현 LLM은 시각 결정을 하지 않는다. blueprint가 한 결정을
tokens.css로 소비하고, 게이트를 통과할 때까지 끝난 것이 아니다.**

## Workflow (순서 고정)

### 0. 컨셉 저작 확인

`projects/<name>/brand_profile.json`에 `application_concept`, `layout_skeleton`,
`design_differentiation`, `component_decision`이 없거나 generic하면 먼저
`design-ontology-concept-author` 스킬로 저작한다. 이 단계는 IA와 컴포넌트의
반복을 막는다. 이 스킬은 그 다음 단계인 시각 반복을 막는다.

### 1. Blueprint 생성

```bash
uv run design-ontology run-project --project-dir projects/<name> --kb-dir kb/default
```

### 2. 토큰 방출 (필수 — 건너뛰면 실패)

```bash
uv run design-ontology emit-tokens --project-dir projects/<name>
```

`projects/<name>/design-system/tokens.css`가 생성된다. 여기의 `--ds-color-*`,
`--ds-color-brand-*`, `--ds-font-*`, `--ds-radius-*`, `--ds-space-*`가 유일한
시각 진실 소스다.

### 3. 사전 발산 점검 (설계 전에 읽기)

```bash
uv run design-ontology check-style-divergence --project-dir projects/<이전-유사-프로젝트> --json
cat registry/style_fingerprints.json
```

레지스트리에서 최근 프로젝트들의 surface tone / accent hue / 폰트 페어링을 확인하고,
이번 구현이 그 조합을 다시 만들지 않도록 방향을 정한다.

### 4. 구현 규칙

HTML/CSS 구현 시:

- `<link rel="stylesheet" href="./design-system/tokens.css" />`를 가장 먼저 링크한다.
- 구현 CSS에는 **hex, rgb(), named color, 하드코딩 font-family, 하드코딩 border-radius를
  쓰지 않는다.** 모두 `var(--ds-*)`로 바인딩한다. 파생색은
  `color-mix(in srgb, var(--ds-color-primary) 12%, var(--ds-color-surface))` 형태로 만든다.
- 배경은 `--ds-color-canvas`/`--ds-color-surface`, 주 액션은 `--ds-color-primary`,
  포인트는 `--ds-color-accent` 또는 `--ds-color-brand-*`를 쓴다. blueprint가 고른
  색이 마음에 안 들어도 바꾸지 않는다 — 바꾸고 싶으면 brand_profile의
  `color_reference`를 수정하고 1번부터 다시 돌린다.
- 폰트는 `--ds-font-heading`/`--ds-font-body`만 쓴다. tokens.css에 없는 서체를
  CDN에서 추가로 불러오지 않는다. 특히 **tokens.css가 세리프를 지정하지 않았다면
  Noto Serif KR 같은 세리프 디스플레이 액센트를 임의로 추가하는 것을 금지한다.**
- 레이아웃과 컴포넌트는 `brand_profile.component_decision.core_components`와
  `layout_skeleton.first_screen_contract`를 따른다. `rejected_components`와
  `avoid_layouts`는 실제 금지 목록이다.

금지 목록 (알려진 수렴 attractor — tokens.css가 명시적으로 지정한 경우만 예외):

- 크림/아이보리/페이퍼 임의 배경 (#FFF8-#FDF5 계열 웜 틴트)
- 옥스블러드·버건디 primary + 틸 secondary + 시트론 하이라이트 조합
- 세리프 디스플레이 헤드라인 + 산세리프 본문의 "에디토리얼" 페어링
- 화이트 배경 + 인디고/바이올렛 단일 액센트의 범용 SaaS 대시보드 룩
- 모든 정보를 라운드 카드 + 칩(pill) 나열로 처리하는 표면 문법

### 5. 검증 게이트 (모두 통과해야 완료)

```bash
# 1. 토큰 바인딩 강제 — 하드코딩 색/폰트/radius가 있으면 실패
uv run design-ontology lint-implementation --target-repo projects/<name>

# 2. 교차 프로젝트 발산 게이트 — 최근 산출물·기본 미감과 너무 비슷하면 실패
uv run design-ontology check-style-divergence --project-dir projects/<name> --register-on-pass

# 3. 스크린샷 QA — 390px 모바일 뷰포트 캡처 후 심미 점수 확인
uv run design-ontology score-screenshot --screenshot <path> --project-dir projects/<name>
```

`check-style-divergence`가 실패하면 리포트의 `[FIX]` 제안을 따른다. 이때 색을
손으로 바꾸지 말고, `brand_profile.json`의 `color_reference.palette_strategy`
(prefer_moods/avoid_moods/temperature)나 `visual_keywords`를 수정한 뒤
`run-project → emit-tokens`를 다시 돌려 tokens.css 자체를 바꾼다.

### 5.7. 구성 문법 (craft rules — 미감을 결정하는 것은 토큰이 아니라 이 규칙들)

**타입 스케일: 극단 대비, 중간 크기 금지.**
- 한 화면의 텍스트는 3계층이면 충분하다: 디스플레이(1.75rem+), 본문(0.9375rem 내외),
  마이크로 라벨(0.6875rem 내외, uppercase + letter-spacing 0.08em+).
- 1.1~1.4rem의 어중간한 볼드를 여러 곳에 뿌리는 것이 아마추어 신호 1순위다.
  중간 크기가 필요해 보이면 본문 크기 + weight 대비로 해결한다.
- weight도 2개면 충분하다 (예: 400/700). 500·600을 섞어 쓰지 않는다.
- `--ds-font-display`가 있으면 브랜드 스테이트먼트·에디토리얼 문장·히어로 숫자에만
  쓴다. UI 라벨과 버튼에는 절대 쓰지 않는다.

**표면: 보더 카드 벽 금지, 여백과 라인으로 분리.**
- 모든 섹션을 1px 보더 라운드 카드로 감싸지 않는다. 섹션 구분의 기본값은
  여백(간격 2배 점프)과 헤어라인 1개다.
- 박스가 정당한 곳은 실제 조작 대상(입력, 선택지, 컨트롤)뿐이다.
- 라운딩은 한 화면에 2단계까지만 (예: sm과 pill). 모든 요소에 md를 바르지 않는다.

**이미지 중심 도메인 (chrome_strategy: achromatic-photographic):**
- 사진은 풀블리드 또는 컨테이너 가득. 사진에 라운드 카드 프레임을 씌우지 않는다.
- UI 크롬은 무채색 유지. 유채색은 `--ds-color-accent`(restrained_accent) 하나를
  화면당 한 곳 이하로만 사용한다. 버튼 기본색은 ink(블랙).
- 텍스트를 사진 위에 올릴 때는 스크림(ink→transparent gradient)으로 대비를 확보한다.

**밀도 리듬:** 화면 전체가 균일한 밀도면 위계가 없는 것이다. 주인공 표면(히어로,
주 조작 대상)은 크고 성기게, 보조 정보는 작고 촘촘하게 — 대비가 리듬을 만든다.

**문서 문법 유출 금지:** Markdown/블로그 습관이 앱 UI에 새어 들어오는 패턴들 —
`border-left` 세로 바 인용구(blockquote callout), 안내문을 감싸는 admonition 박스,
글머리 기호 리스트로 나열한 UI 텍스트. 앱의 안내 문구는 장식 없는 muted 캡션이
기본값이다. 강조가 필요하면 배치(위치·여백)로 해결하고 장식을 더하지 않는다.

**계기·차트·좌표 표면은 실제 렌더링 매체로:** CSS 배경 그라디언트로 격자를 흉내 내고
absolutely-positioned 점을 올리는 것은 박스 아트다. 좌표 필드, 게이지, 차트, 미니맵
같은 표면은 **하나의 좌표계를 가진 inline SVG**(격자 + 틱 마크 + 크로스헤어 + 상태
글로우를 같은 viewBox 안에서) 또는 canvas/차트 라이브러리로 렌더링한다. 인터랙션은
투명 히트 영역(버튼)이 받고 JS가 SVG 속성을 갱신한다. `<title>`과 의미 있는 구조를
포함해 low-information SVG 규칙(DS086류)에 걸리지 않게 한다.

**위 규칙 중 다음은 lint-implementation이 기계적으로 강제한다 (위반 시 FAIL):**

| 코드 | 잡는 것 |
|---|---|
| DS090 | note/callout류 셀렉터의 border-left 인용구 바 (문서 문법 유출) |
| DS091 | radius 단일 토큰 도배 (라운딩 모노컬처) |
| DS092 | font-weight 500+600 동시 사용 (중간 굵기 헤징) |
| DS093 | 디스플레이 계층 없는 압축 타입 스케일 (max < 1.5rem) |
| DS094 | lorem/항목 N류 채움말 카피 |
| DS095 | CSS 그라디언트로 그림 흉내 낸 격자 필드 (계기 표면 박스 아트) |

### 6. 완성도 기준 (프로페셔널 목업의 최소선)

- 모든 상태가 있는 화면: 컴포넌트별 `states` 필드에 선언된 상태 중 최소 2개가
  실제 마크업에 존재해야 한다 (예: default + active).
- 진짜 데이터 밀도: lorem ipsum, "항목 1/2/3" 금지. 도메인 객체의 실제 이름과
  현실적인 값으로 채운다.
- 한글 조판: `word-break: keep-all`, 320px에서 가로 스크롤 없음, 44px 터치 타깃.
- 이미지가 필요한 표면은 회색 placeholder 박스가 아니라 실제 에셋 또는 CSS로
  의미 있는 시각 처리를 한다 (linter의 media tile 규칙 참조).

## 실패 시 대응

| 증상 | 대응 |
|---|---|
| lint-implementation DS001/DS010 다수 | 구현 CSS에서 하드코딩 값을 var(--ds-*)로 치환. tokens.css에 없는 역할이 필요하면 emit-tokens 출력에 역할을 추가하는 게 아니라 blueprint를 다시 생성 |
| divergence FAIL: attractor | 기본 미감으로 회귀한 것. tokens.css를 실제로 소비했는지 확인 — 대부분 tokens.css를 링크만 하고 안 쓴 경우 |
| divergence FAIL: too-similar | brand_profile의 palette_strategy·visual_keywords를 다른 계열로 수정 후 재생성 |
| blueprint 팔레트가 제품과 안 맞음 | styles.css에서 즉흥 수정 금지. color_reference의 preferred_families/prefer_moods를 수정하고 run-project 재실행 |
