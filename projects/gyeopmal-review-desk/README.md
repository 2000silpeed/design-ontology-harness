# Gyeopmal — UI 기본 규칙 참조 화면

한국어 번역 검수 대기열. 이 프로젝트는 제품 자체가 목적이 아니라 `docs/UI_BASE_RULES.md`의
기본 규칙(DS100~DS107)을 통과하는 화면이 실제로 어떻게 생겼는지 보여주는 참조 구현이다.
규칙만 있고 통과 사례가 없으면 에이전트가 볼 본보기가 없다.

한글 본문이 곧 제품인 도메인을 골랐다. 원문과 번역문을 나란히 읽는 화면은 행간·자간·줄바꿈이
어긋나면 대조 자체가 불가능해지므로, 조판 규칙을 장식이 아니라 기능으로 요구한다.

## 게이트 상태

```bash
uv run design-ontology lint-implementation --target-repo projects/gyeopmal-review-desk
# Implementation lint: OK (3 files checked, 0 issues)
```

`tests/test_ui_base_rules.py::test_reference_screen_passes_implementation_lint`가 이 상태를 고정한다.

## 규칙별 구현 지점

| 코드 | 어디서 볼 수 있는가 |
|---|---|
| `DS100` | 본문·원문·번역문·검수 의견이 모두 `var(--ds-leading-body)`(한글 1.6). 헤딩만 `--ds-leading-tight` |
| `DS101` | 상태 텍스트는 `--ds-color-ink`로 두고 색은 점에만 뒀다. 상태색은 `surface`에서만 4.5:1을 넘어서 `surface-muted` 위에 올리면 미달한다 |
| `DS102` | 컨트롤 테두리를 `--ds-color-border-strong`에 묶었다. 런타임 정책의 비텍스트 하한이 이 역할을 3:1 위로 유지한다. `border`(1.37:1)는 장식 구분선 전용 |
| `DS103` | 상태 점이 두 겹으로 구분된다. 옆에 글자 라벨이 붙고, 점 자체도 채움·테두리·회전으로 모양이 다르다 |
| `DS104` | display/heading/body 토큰이 모두 한 서체로 해석된다. 위계는 크기와 굵기(400/700)로만 만든다 |
| `DS105` | 한글 읽기 슬롯은 `var(--ds-tracking-body)`(0em). `.pane-eyebrow`만 uppercase + 0.08em으로 라틴 예외를 보여준다 |
| `DS106` | `word-break: var(--ds-wrap-word-break)` + `overflow-wrap: var(--ds-wrap-overflow)` |
| `DS107` | 읽는 텍스트에 `text-align: left` 명시 |
| `DS108` | `design-system/fonts.css`를 링크한다. Pretendard는 자체 호스팅, Source Code Pro는 Google Fonts |

## 증거

`screenshots/`의 3장은 같은 route에서 찍었다. 초기 테마는 `?theme=dark`로도 받는다.

- `desktop-light.png` — 1440px 라이트
- `desktop-dark.png` — 1440px 다크. 레이아웃은 같고 토큰 값만 바뀐다
- `mobile-light.png` — 390px. 상단 바가 두 줄로 접히고 한글이 어절 경계에서만 끊긴다

390px와 320px에서 `documentElement.scrollWidth`가 뷰포트보다 작고 초과 요소가 없다.

> headless Chrome의 `--window-size`를 좁게 주면 창 최소 폭으로 클램핑된 뒤 PNG만 잘려서
> 오버플로처럼 보인다. 좁은 폭 증거는 같은 출처의 iframe을 정확한 폭으로 띄워 측정·캡처했다.

## 서체 로딩

선언만 있고 로딩이 없으면 화면은 조용히 `system-ui`로 떨어지고 서체 결정이 무효가 된다.
`design-system/fonts.css`가 그 로딩을 담당하고 `index.html`이 링크한다.

```bash
node design-system/fonts/fetch-webfonts.mjs   # Pretendard woff2를 내려받는다
```

Pretendard는 자체 호스팅이라 오프라인에서도 렌더된다. Source Code Pro는 Google Fonts
`@import`이므로 원격 참조다. production 증거의 content tree를 엄격히 고정해야 하면 그 서체도
자체 호스팅으로 옮겨야 한다. 폰트 바이너리는 커밋하지 않는다.

## 재생성

```bash
uv run design-ontology run-project --project-dir projects/gyeopmal-review-desk --kb-dir kb/default
uv run design-ontology emit-tokens --project-dir projects/gyeopmal-review-desk
uv run design-ontology lint-implementation --target-repo projects/gyeopmal-review-desk
```

`design-system/tokens.css`는 생성 산출물이다. 손으로 고치지 말고 blueprint를 바꿔 다시 방출한다.
