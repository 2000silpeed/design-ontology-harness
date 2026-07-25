# EKOS Knowledge Intake

This folder is a self-contained harness project built on top of `design-ontology-harness`.

## Files

- `brand_profile.json`: your system identity and product context
- `seeds/seed_urls.txt`: curated reference entry points
- `project_manifest.json`: project metadata
- `agent_brief.md`: instructions for human or agent collaborators
- `build/`: generated outputs

## How To Run

이 프로젝트는 화면 명세의 상태색 계약(성공=Hunter Green, 경고=Goldenrod,
실패=Marsala, 정보/링크=Ocean Blue, Rust는 강조 전용)을 피드백 시맨틱 역할에
강제하고, 다크 모드 팔레트(ekos-design-system.html의 ink 테마 — 프러시안 심해 위
콘실크 잉크)를 수동 지정해야 하므로, 일반 run-project 대신 오버라이드 래퍼를 사용한다.

```bash
uv run python projects/ekos-knowledge-intake/run_synthesis.py
```

(일반 `uv run design-ontology run-project ...`를 쓰면 warning이 Rust로,
success/danger가 보조색으로 자동 유도되어 명세를 위반한다.)

설계 입력 원본: Enterprise-knowledge-Operating-System/docs/04-product/knowledge-intake-screen-spec.md
설치 대상: Enterprise-knowledge-Operating-System/design-system/ (preset `document-content--corporate-trust`, adapter `raw-css-variables`, locale ko)

## Recommended Flow

1. Fill in `brand_profile.json`
2. Set or override the KB path if needed
3. Run the project
4. Review `build/system/blueprint/system_spec.md`
