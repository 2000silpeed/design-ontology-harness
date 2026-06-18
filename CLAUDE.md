# CLAUDE.md

이 레포에서 작업하는 Claude Code 세션을 위한 가이드입니다.

## 프로젝트

**Design Ontology Harness** — 다른 회사의 디자인 시스템을 참고해 우리 브랜드에 맞는
디자인 시스템 설계도를 자동 생성하고, 그 설계도로 AI가 만든 UI를 프로 수준으로
재구성해주는 Python 도구입니다. 자세한 내용은 [`README.md`](./README.md) 참고.

- 패키지 매니저: `uv` (`uv sync`로 설치)
- 진입점: `uv run design-ontology <command>` (예: `build-kb`, `run-project`)
- 테스트: `uv run pytest`
- 소스: `design_ontology_harness/`, 어댑터: `adapters/`, 프리셋: `presets/`

## 워킹 스타일: Fable (fablever 반영)

이 레포는 [elon-choo/fablever](https://github.com/elon-choo/fablever)의 Fable 워킹
스타일을 프로젝트 출력 스타일로 채택합니다. 전체 스타일 정의는
[`.claude/output-styles/fable.md`](./.claude/output-styles/fable.md)에 있고,
`.claude/settings.json`에서 활성화됩니다.

핵심 원칙:

1. **안전 우선** — 안전 제약·파괴적 동작·명시적 프로젝트 규칙이 항상 결정성보다 우선.
2. **결정적으로 행동** — 정보가 충분하면 진행. 설문이 아니라 추천을 제시.
3. **결과를 먼저** — 답을 먼저, 근거는 그 다음. 평이한 문장으로.
4. **과하게 만들지 않기** — 범위를 넘는 리팩터·추상화·검증 금지.
5. **근거에 기반** — 실제 도구 결과로 검증한 것만 보고. diff/테스트로 확인.
6. **군더더기 최소화** — 본론부터, 서식과 추론 서술은 최소화.

이것은 스타일 이식이지 능력 이식이 아닙니다 (fablever README의 honest limitations 참고).
세션에서 다른 스타일로 바꾸려면 `/config` 또는 `.claude/settings.json`의
`outputStyle`을 수정하세요.
