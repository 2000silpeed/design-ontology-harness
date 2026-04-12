from __future__ import annotations

import json
from pathlib import Path

from .utils import ensure_dir, write_json


def scaffold_agent_pack(
    target_repo: Path,
    artifact_dir: str = "design-system",
    targets: list[str] | None = None,
    force: bool = False,
) -> dict:
    targets = targets or ["codex", "claude"]
    normalized_targets = sorted({target.strip().lower() for target in targets if target.strip()})
    supported = {"codex", "claude"}
    unsupported = [target for target in normalized_targets if target not in supported]
    if unsupported:
        raise ValueError(f"Unsupported targets: {unsupported}")

    ensure_dir(target_repo)
    created: list[str] = []

    artifact_path = target_repo / artifact_dir
    ensure_dir(artifact_path)
    _write_if_allowed(
        artifact_path / "README.md",
        _artifact_readme(artifact_dir),
        force=force,
        created=created,
    )

    if "claude" in normalized_targets:
        _scaffold_claude_pack(target_repo, artifact_dir, force, created)
    if "codex" in normalized_targets:
        _scaffold_codex_pack(target_repo, artifact_dir, force, created)

    return {
        "target_repo": str(target_repo),
        "artifact_dir": artifact_dir,
        "targets": normalized_targets,
        "created": created,
    }


def _scaffold_claude_pack(target_repo: Path, artifact_dir: str, force: bool, created: list[str]) -> None:
    claude_dir = ensure_dir(target_repo / ".claude")
    skills_dir = ensure_dir(claude_dir / "skills")
    agents_dir = ensure_dir(claude_dir / "agents")

    implement_skill_dir = ensure_dir(skills_dir / "design-system-implement")
    architect_skill_dir = ensure_dir(skills_dir / "design-system-architect")

    _write_if_allowed(
        implement_skill_dir / "SKILL.md",
        _claude_implement_skill(artifact_dir),
        force=force,
        created=created,
    )
    _write_if_allowed(
        architect_skill_dir / "SKILL.md",
        _claude_architect_skill(artifact_dir),
        force=force,
        created=created,
    )
    _write_if_allowed(
        agents_dir / "design-system-architect.md",
        _claude_architect_agent(artifact_dir),
        force=force,
        created=created,
    )
    _write_if_allowed(
        agents_dir / "design-system-implementer.md",
        _claude_implementer_agent(artifact_dir),
        force=force,
        created=created,
    )

    refactor_skill_dir = ensure_dir(skills_dir / "design-system-refactor")
    _write_if_allowed(
        refactor_skill_dir / "SKILL.md",
        _claude_refactor_skill(artifact_dir),
        force=force,
        created=created,
    )
    _write_if_allowed(
        agents_dir / "design-system-refactor.md",
        _claude_refactor_agent(artifact_dir),
        force=force,
        created=created,
    )


def _scaffold_codex_pack(target_repo: Path, artifact_dir: str, force: bool, created: list[str]) -> None:
    plugin_root = ensure_dir(target_repo / "plugins" / "design-system-harness")
    ensure_dir(plugin_root / ".codex-plugin")
    skills_root = ensure_dir(plugin_root / "skills")
    architect_dir = ensure_dir(skills_root / "design-system-architect")
    implementer_dir = ensure_dir(skills_root / "design-system-implementer")
    plugin_agents_dir = ensure_dir(plugin_root / "agents")
    marketplace_dir = ensure_dir(target_repo / ".agents" / "plugins")

    plugin_manifest = {
        "name": "design-system-harness",
        "version": "0.1.0",
        "description": "Skills for applying design-system-harness outputs inside an implementation repository.",
        "author": {
            "name": "Design Ontology Harness",
        },
        "license": "MIT",
        "keywords": [
            "design-system",
            "tokens",
            "ui",
            "codex",
            "skills",
        ],
        "skills": "./skills/",
        "interface": {
            "displayName": "Design System Harness",
            "shortDescription": "Apply design-system artifacts inside a real implementation repo",
            "longDescription": "Provides Codex skills for reading design-system artifacts and implementing tokens, components, and UI changes that stay aligned with your system spec.",
            "developerName": "Design Ontology Harness",
            "category": "Coding",
            "capabilities": ["Interactive", "Write"],
            "defaultPrompt": [
                "Implement UI changes using the local design-system artifacts and component inventory"
            ],
            "screenshots": [],
            "brandColor": "#6B7B8D",
        },
    }

    marketplace = {
        "name": "Local Plugins",
        "interface": {"displayName": "Local Plugins"},
        "plugins": [
            {
                "name": "design-system-harness",
                "source": {
                    "source": "local",
                    "path": "./plugins/design-system-harness",
                },
                "policy": {
                    "installation": "AVAILABLE",
                    "authentication": "ON_INSTALL",
                },
                "category": "Coding",
            }
        ],
    }

    _write_if_allowed(
        plugin_root / ".codex-plugin" / "plugin.json",
        json.dumps(plugin_manifest, ensure_ascii=False, indent=2) + "\n",
        force=force,
        created=created,
    )
    _write_if_allowed(
        architect_dir / "SKILL.md",
        _codex_architect_skill(artifact_dir),
        force=force,
        created=created,
    )
    _write_if_allowed(
        implementer_dir / "SKILL.md",
        _codex_implementer_skill(artifact_dir),
        force=force,
        created=created,
    )
    _write_if_allowed(
        plugin_agents_dir / "openai.yaml",
        _codex_plugin_openai_yaml(),
        force=force,
        created=created,
    )
    _write_if_allowed(
        marketplace_dir / "marketplace.json",
        json.dumps(marketplace, ensure_ascii=False, indent=2) + "\n",
        force=force,
        created=created,
    )


def _artifact_readme(artifact_dir: str) -> str:
    return f"""# Design System Artifacts

Place generated artifacts from `design-ontology-harness` in this directory.

Expected files:

- `system_spec.md`
- `token_schema.json`
- `component_inventory.json`
- `system_ontology.json`
- `components/component_specs.json` (optional, from build-components)
- `components/component_specs.md` (optional, human-readable version)

Important usage rule:

- treat these artifacts as alignment inputs, not a license for a full-shell rewrite
- preserve existing product features and entry points unless an explicit migration is requested
- validate supported themes and responsive states when applying visual refactors

Recommended sync source:

- a harness project output such as `build/system/blueprint/*`

Recommended mapping:

- `build/system/blueprint/system_spec.md` -> `{artifact_dir}/system_spec.md`
- `build/system/blueprint/token_schema.json` -> `{artifact_dir}/token_schema.json`
- `build/system/blueprint/component_inventory.json` -> `{artifact_dir}/component_inventory.json`
- `build/system/blueprint/system_ontology.json` -> `{artifact_dir}/system_ontology.json`
- `build/system/components/` -> `{artifact_dir}/components/`
"""


def _claude_architect_skill(artifact_dir: str) -> str:
    return f"""---
name: design-system-architect
description: Align implementation plans and UI decisions with the project's design-system artifacts. Use when deciding token structure, component families, primitives, or rollout order.
allowed-tools: Read Glob Grep Bash
paths:
  - "{artifact_dir}/**"
  - "src/**"
  - "app/**"
  - "components/**"
  - "styles/**"
---

When this skill is active:

1. Read `{artifact_dir}/system_spec.md` first.
2. Read `{artifact_dir}/token_schema.json` and `{artifact_dir}/component_inventory.json`.
3. If present, use `{artifact_dir}/system_ontology.json` to understand relations between principles, token categories, and component families.
4. Translate user requests into:
   - affected principles
   - affected token categories
   - affected component families
   - required implementation order
5. Favor extending existing primitives over inventing new components.
6. Explicitly guard against anti-keywords from the system spec.
7. Preserve existing user-facing entry points and feature surfaces unless the user explicitly asks for a structural change.
8. Prefer incremental rollout plans over full-shell rewrites.
9. If `token_schema.json` contains a curated color reference or palette roles, treat that as the starting point for semantic color decisions.

If any artifact file is missing, say exactly which file is missing and recommend syncing artifacts from the harness repo before implementation.
"""


def _claude_implement_skill(artifact_dir: str) -> str:
    return f"""---
name: design-system-implement
description: Implement or refactor UI code to match the project's design-system artifacts. Use when building tokens, components, styles, or screens based on the generated design-system outputs.
allowed-tools: Read Glob Grep Bash Edit Write
paths:
  - "{artifact_dir}/**"
  - "src/**"
  - "app/**"
  - "components/**"
  - "styles/**"
---

Before making changes:

1. Read `{artifact_dir}/system_spec.md`.
2. Read `{artifact_dir}/token_schema.json`.
3. Read `{artifact_dir}/component_inventory.json`.

Implementation rules:

- Treat the design-system artifacts as the source of truth.
- Keep implementation aligned with the product's brand keywords and anti-keywords.
- Implement high-priority component families before medium-priority families.
- Reuse or extend primitives before adding net-new components.
- Preserve existing features, navigation entry points, and data flows unless removal is explicitly requested.
- Keep supported themes, breakpoints, and critical interaction states working while refactoring.
- Prefer semantic tokens over one-off hardcoded colors so theme support survives future changes.
- Default to the smallest viable surface refactor; do not rewrite the whole shell unless the task explicitly calls for it.
- If `token_schema.json` includes a curated color reference or palette roles, align color decisions to that input before inventing a new palette.
- Update nearby documentation or tests when implementation meaningfully changes.
- NEVER change layout properties (display, flex-direction, grid-template, position, width, height).
- NEVER change font-size or line-height to "fit the token scale." Existing sizes are tuned to the layout. Only replace when the token resolves to the exact same px. If no match, keep original + TODO.
- NEVER round spacing values to the nearest token — if no exact match, leave as-is with a TODO.

When finishing:

- State which artifact files guided the implementation.
- Mention any gaps between the requested UI and the current system artifacts.
- Mention any feature, theme, or layout risks that still need manual verification.
"""


def _claude_architect_agent(artifact_dir: str) -> str:
    return f"""---
name: design-system-architect
description: Design-system planning specialist. Use for token strategy, component architecture, rollout planning, and decisions that must stay aligned with `{artifact_dir}` artifacts.
tools: Read, Glob, Grep, Bash
model: sonnet
color: blue
---

You are a design-system architecture specialist.

Your job is to translate product work into a design-system implementation plan that respects the project's generated artifacts.

Always:

1. Read `{artifact_dir}/system_spec.md` first.
2. Then read `{artifact_dir}/token_schema.json` and `{artifact_dir}/component_inventory.json`.
3. Map the request to:
   - principles
   - token categories
   - component families
   - rollout order
4. Prefer extending existing primitives over introducing new abstractions.
5. Call out conflicts with anti-keywords or missing artifacts.
6. Treat existing screens and interaction entry points as constraints, not disposable implementation details.
7. Recommend incremental rollout steps before proposing a shell-level rewrite.
8. If the token schema includes curated palette roles, use those roles as the default color direction in the plan.

You are primarily a planning and alignment agent, not an implementation agent.
"""


def _claude_implementer_agent(artifact_dir: str) -> str:
    return f"""---
name: design-system-implementer
description: UI implementation specialist for code changes that must follow the project's design-system artifacts in `{artifact_dir}`.
tools: Read, Glob, Grep, Bash, Edit, Write
model: sonnet
color: green
---

You are a design-system implementation specialist.

Before editing code:

1. Read `{artifact_dir}/system_spec.md`.
2. Read `{artifact_dir}/token_schema.json`.
3. Read `{artifact_dir}/component_inventory.json`.

Implementation rules:

- Keep code aligned with system principles.
- Use the token schema to name and organize variables or theme values.
- Use the component inventory to decide whether to create, extend, or defer a component.
- Preserve existing feature surfaces and task-completion paths unless the user explicitly wants a structural redesign.
- Maintain supported themes and responsive layouts; avoid introducing hardcoded colors that only work in one mode.
- Prefer local, reversible refactors over all-at-once shell rewrites.
- If token_schema includes curated palette roles or selected reference colors, preserve that color direction while implementing.
- If the request falls outside the current system artifacts, state the gap clearly instead of inventing an ungrounded pattern.
- NEVER change layout properties, element sizes, or text-flow properties (font-size, line-height, white-space, word-break) unless explicitly requested.
- NEVER change font-size to match a token scale — existing sizes are already tuned to the layout. Only replace when the token is the exact same px value. "Fitting the scale" is a design change, not a refactor.
- When replacing spacing/sizing values with tokens, only use exact matches — never round to the nearest token value.
"""


def _claude_refactor_skill(artifact_dir: str) -> str:
    return f"""---
name: design-system-refactor
description: AI가 만든 UI 코드를 디자인 시스템 스펙에 맞게 자동 리팩토링합니다. /design-refactor 로 실행하세요.
allowed-tools: Read Glob Grep Bash Edit Write
paths:
  - "{artifact_dir}/**"
  - "src/**"
  - "app/**"
  - "components/**"
  - "styles/**"
  - "lib/**"
---

# Design System Refactor

AI가 생성한 UI 코드나 급하게 만든 프로토타입을, 디자인 시스템 스펙 기준으로 체계적으로 리팩토링합니다.

## 실행 절차

### Phase 1: 스펙 로드

1. `{artifact_dir}/component_specs.json` 또는 `{artifact_dir}/components/component_specs.json`을 읽습니다.
   - 없으면 `{artifact_dir}/component_inventory.json`을 읽습니다.
2. `{artifact_dir}/token_schema.json`을 읽습니다.
3. `{artifact_dir}/system_spec.md`를 읽어 브랜드 키워드, 안티 키워드, 디자인 원칙을 파악합니다.

이 세 파일이 리팩토링의 기준입니다. 파일이 없으면 어떤 파일이 빠졌는지 알리고 멈춥니다.

### Phase 2: 코드베이스 스캔

1. `src/`, `app/`, `components/` 에서 UI 컴포넌트 파일을 찾습니다.
   - React: `*.tsx`, `*.jsx`
   - Vue: `*.vue`
   - Svelte: `*.svelte`
2. 각 파일에서 아래 문제를 탐지합니다:

**토큰 위반**
- 하드코딩된 색상값 (`#fff`, `rgb(...)`, `bg-blue-500` 등)
- 하드코딩된 spacing (`margin: 12px`, `p-3` 등 — 토큰 scale에 없는 값)
- 하드코딩된 font-size, border-radius
- 인라인 스타일에 직접 값 사용

**컴포넌트 구조 위반**
- 스펙에 정의된 상태(states)가 빠져 있는 컴포넌트
- anatomy에 정의된 필수 파트가 없는 컴포넌트
- variant 없이 조건부로 스타일 하드코딩

**접근성 위반**
- button에 role/aria 속성 누락
- input에 label 연결 누락
- modal에 focus trap 누락
- 이미지에 alt 누락
- 터치 영역 44px 미만

**브랜드 위반**
- 안티 키워드에 해당하는 시각적 패턴 (예: "noisy" 안티키워드인데 과한 그림자/애니메이션)
- 브랜드 키워드와 충돌하는 인터랙션 (예: "calm"인데 bounce 애니메이션)

### Phase 3: 리팩토링 실행

탐지된 문제를 **우선순위 순서**로 수정합니다:

1. **접근성 위반** (가장 먼저 — 법적/윤리적 요구사항)
2. **토큰 하드코딩** (시스템의 기반)
3. **컴포넌트 구조** (누락된 상태/파트 추가)
4. **브랜드 정합성** (시각적 미세 조정)

각 수정은:
- 한 파일씩 순차적으로 처리
- 수정 전후를 설명
- 기존 기능을 깨뜨리지 않는 범위에서만 변경
- 확신이 없는 변경은 TODO 주석으로 남김

### Phase 4: 리포트

리팩토링 완료 후 요약을 출력합니다:

```
## 리팩토링 결과

### 수정 완료
- [파일명]: 토큰 위반 3건, 접근성 위반 1건 수정
- [파일명]: 컴포넌트 구조 보완 (disabled 상태 추가)

### 수동 확인 필요
- [파일명]: 색상 팔레트 적용 확인 필요
- [파일명]: 반응형 레이아웃 테스트 필요

### 스펙 미커버
- [컴포넌트명]: 스펙에 없는 컴포넌트 — component_specs에 추가 필요
```

## 수정 규칙

### 토큰 교체 예시

```tsx
// Before (하드코딩)
<div className="bg-white text-gray-900 p-4 rounded-lg shadow-md">

// After (토큰 기반)
<div className="bg-surface-default text-text-primary p-spacing-16 rounded-radius-md shadow-elevation-raised">
```

### 상태 추가 예시

```tsx
// Before (상태 누락)
function Button({{ children }}) {{
  return <button>{{children}}</button>
}}

// After (스펙 기반 상태)
function Button({{ children, variant = "primary", size = "md", disabled, loading }}) {{
  return (
    <button
      disabled={{disabled || loading}}
      aria-busy={{loading}}
      aria-disabled={{disabled}}
      className={{buttonStyles({{ variant, size, disabled, loading }})}}
    >
      {{loading ? <Spinner /> : children}}
    </button>
  )
}}
```

### 접근성 추가 예시

```tsx
// Before
<input placeholder="이름" />

// After
<label htmlFor="name">이름</label>
<input id="name" aria-required="true" />
```

## 레이아웃 보호 규칙 (최우선)

리팩토링은 **기존 화면의 레이아웃과 텍스트 흐름을 절대 깨뜨리지 않는 범위**에서만 진행합니다.

### 절대 건드리지 않는 것

- `display`, `flex-direction`, `grid-template-columns`, `position`, `float` 등 **레이아웃 속성**
- `width`, `height`, `max-width`, `min-height` 등 **박스 크기**
- `overflow`, `text-overflow`, `white-space`, `word-break` 등 **텍스트 줄바꿈 제어**
- `line-clamp`, `-webkit-line-clamp` 등 **말줄임 처리**
- `gap`, `margin`, `padding` 중 **레이아웃 간격에 영향을 주는 값** (단, 토큰으로 1:1 교체는 허용)

### 안전한 교체만 허용

```
허용: color: #334155 → color: var(--text-primary)
허용: background: #fff → background: var(--surface-default)
허용: border: 1px solid #e5e7eb → border: 1px solid var(--border-default)
허용: border-radius: 8px → border-radius: var(--radius-md)
허용: font-weight: 600 → font-weight: var(--font-weight-semibold)
허용: box-shadow: 0 1px 3px ... → box-shadow: var(--elevation-raised)

금지: padding: 12px 16px → padding: 16px 24px (크기가 바뀌면 레이아웃 깨짐)
금지: display: flex → display: grid (레이아웃 변경)
금지: width: 100% → width: auto (크기 변경)
금지: font-size: 14px → font-size: 16px (줄바꿈 위치가 바뀜)
금지: line-height: 1.4 → line-height: 1.75 (텍스트 높이가 바뀜)
```

### font-size / line-height: 원칙적으로 바꾸지 않음

**기존 코드의 font-size는 이미 화면에 맞게 조정된 값입니다.**
토큰 스케일(xs=12, sm=13, md=15, lg=21...)에 기계적으로 맞추려고
기존 14px → 15px, 16px → 21px 같은 변경을 하면 안 됩니다.

이런 일이 실제로 발생합니다:
- 카드 제목 16px → 18px(lg)로 올림 → 한 줄이 두 줄로 넘침 → 카드 높이 깨짐
- 배지 텍스트 11px → 12px(xs)로 올림 → 배지 폭 증가 → 줄 끝에서 밀려남
- 리스트 아이템 13px → 14px → padding 그대로인데 글자가 커져서 뭉쳐 보임
- 가격 텍스트 15px → 16px → 옆 요소와 정렬 어긋남

**리팩토링에서 font-size를 바꾸는 것은 디자인 변경이지 리팩토링이 아닙니다.**

허용되는 경우:
```
font-size: 14px → var(--text-sm)   (단, --text-sm이 정확히 14px일 때만)
font-size: 16px → var(--text-md)   (단, --text-md가 정확히 16px일 때만)
```

금지되는 경우:
```
font-size: 14px → var(--text-md)   (md가 15px이면 × — 1px 차이라도 안 됨)
font-size: 16px → var(--text-lg)   (lg가 21px이면 × — "스케일에 맞추려고" 키우면 안 됨)
font-size: 11px → var(--text-xs)   (xs가 12px이면 × — 배지/뱃지 크기가 바뀜)
```

토큰 스케일에 정확히 맞는 값이 없으면:
```
// 토큰 스케일에 14px가 없음 — 원본 유지
font-size: 14px; /* TODO: token scale에 없는 값, 커스텀 토큰 추가 검토 */
```

line-height도 동일하게 적용합니다.
**토큰이 코드에 맞춰야지, 코드가 토큰에 맞추면 안 됩니다.**

### spacing 교체 시 주의

- `padding`/`margin` 교체는 spacing scale에서 **정확히 같은 값**이 있을 때만 1:1 교체
- spacing scale에 없는 값(14px, 18px, 22px 등)은 교체하지 않고 TODO로 남김
- 절대로 "가장 가까운 값"으로 반올림하지 않음 — 1px 차이로도 레이아웃이 깨질 수 있음
- 특히 **보더나 구분선이 없는 반복 요소**(리스트, 카드 나열)는 spacing이 유일한 시각적 구분 — 더 신중하게
- 배지/뱃지의 padding을 키우면 배지 자체 크기가 바뀌고 주변 정렬에 영향 — 원본 유지

### 리팩토링 후 자가 검증

매 파일 수정 후 아래를 확인합니다:

1. **줄바꿈 불변**: 텍스트의 줄바꿈 위치가 바뀌지 않았는가?
2. **박스 크기 불변**: 수정 전후로 요소의 width/height가 동일한가?
3. **간격 불변**: 요소 사이 간격이 달라지지 않았는가?
4. **넘침 없음**: 텍스트나 요소가 컨테이너를 벗어나지 않는가?
5. **뭉침 없음**: 보더 없는 목록에서 아이템 간 시각적 구분이 유지되는가?
6. **정렬 유지**: 인접 요소 간 baseline/vertical 정렬이 바뀌지 않았는가?

확신이 없으면 **수정하지 않고** 리포트에 "수동 확인 필요" 항목으로 남깁니다.

## 금지 사항

- 기존 기능이나 라우팅을 변경하지 않음
- 스펙에 없는 새 컴포넌트를 발명하지 않음
- 전체 파일을 리라이트하지 않음 — 문제가 있는 부분만 수정
- 테마/다크모드 지원이 있으면 깨뜨리지 않음
- 동작하는 로직을 건드리지 않음 — 시각적/구조적 레이어만 수정
- **레이아웃 속성을 변경하지 않음** — 색상/보더/그림자/radius만 토큰으로 교체
- **font-size/line-height를 함부로 바꾸지 않음** — 줄바꿈이 바뀔 수 있음
- **spacing을 반올림하지 않음** — 정확히 같은 값의 토큰이 없으면 교체하지 않음
"""


def _claude_refactor_agent(artifact_dir: str) -> str:
    return f"""---
name: design-system-refactor
description: AI가 만든 UI를 디자인 시스템 스펙 기반으로 자동 리팩토링하는 에이전트. 토큰 위반, 접근성 누락, 브랜드 불일치를 찾아서 수정합니다.
tools: Read, Glob, Grep, Bash, Edit, Write
model: sonnet
color: orange
---

You are a design-system refactoring specialist.

Your job is to take existing UI code (often AI-generated or prototyped quickly) and systematically refactor it to match the project's design system specifications.

## Startup

1. Read `{artifact_dir}/component_specs.json` or `{artifact_dir}/components/component_specs.json`.
   - Fallback: `{artifact_dir}/component_inventory.json`
2. Read `{artifact_dir}/token_schema.json`.
3. Read `{artifact_dir}/system_spec.md`.

These three files are your source of truth. If any are missing, report which files are needed.

## What to fix (in priority order)

1. **Accessibility violations**: missing roles, aria attributes, labels, focus management, touch targets
2. **Hardcoded tokens**: colors (#hex, rgb, tailwind color classes), spacing (px values not on scale), font sizes, border-radius, shadows → replace with semantic tokens
3. **Missing component states**: components that lack states defined in the spec (disabled, loading, error, hover, focus)
4. **Missing anatomy parts**: components missing required parts from the spec (e.g., button without loading spinner slot)
5. **Brand misalignment**: visual patterns that conflict with brand keywords or match anti-keywords

## Rules

- Fix one file at a time, explain what you changed and why
- Never break existing functionality — only change the visual/structural layer
- Never invent components not in the spec
- Never rewrite entire files — surgical fixes only
- If unsure, leave a TODO comment instead of guessing
- Preserve dark mode / theme support if present
- After finishing, produce a summary report listing: fixed items, items needing manual review, and components not covered by the spec

## Layout Protection (highest priority)

Refactoring must NEVER break existing layout or text flow.

**Safe to replace** (value-for-value swaps only):
- color, background-color, border-color → token
- border-radius → token (same px value)
- box-shadow → token
- font-weight → token
- opacity, transition → token

**NEVER change**:
- display, flex-direction, grid-template, position, float
- width, height, max-width, min-height
- overflow, white-space, word-break, text-overflow, line-clamp
- font-size (unless exact same px exists in token scale)
- line-height (unless exact same ratio exists in token scale)
- padding/margin (unless exact same px exists in spacing scale — NEVER round to nearest)

If no exact token match exists, leave the value as-is and add a TODO comment.
One pixel of rounding can break text wrapping and card layouts.

**Typography Rule**: Do NOT change font-size or line-height to "fit the token scale."
Existing font sizes are already tuned to the layout. Changing 14px→15px or 16px→18px
to match a token scale causes text wrapping changes, card height breakage, and badge
misalignment. Only replace with a token when the token resolves to the EXACT same px value.
If no exact match exists, keep the original value and add a TODO comment.
"""


def _codex_architect_skill(artifact_dir: str) -> str:
    return f"""---
name: design-system-architect
description: Plan token structure, component architecture, and rollout order using the repository's design-system artifacts. Use when the task requires alignment decisions before implementation.
---

# Design System Architect

Use this skill when working on planning or architectural questions related to the local design system.

## Required Inputs

Read these files first when they exist:

- `{artifact_dir}/system_spec.md`
- `{artifact_dir}/token_schema.json`
- `{artifact_dir}/component_inventory.json`
- `{artifact_dir}/system_ontology.json`

## Workflow

1. Identify the relevant principles from `system_spec.md`.
2. Map the request to token categories and component families.
3. Prefer extending an existing primitive over introducing a new abstraction.
4. Call out any conflict with anti-keywords or missing system coverage.
5. Preserve existing surface structure and user flows unless the task explicitly asks to replace them.
6. Produce a concise, incremental implementation plan the coding agent can follow.
7. Use curated palette roles from the token schema as the default color direction when available.
"""


def _codex_implementer_skill(artifact_dir: str) -> str:
    return f"""---
name: design-system-implementer
description: Implement UI changes that must follow the repository's design-system artifacts. Use when editing tokens, components, styles, or screens so implementation stays aligned with the generated system.
---

# Design System Implementer

Use this skill when making code changes in the implementation repository.

## Required Inputs

Read these files first when they exist:

- `{artifact_dir}/system_spec.md`
- `{artifact_dir}/token_schema.json`
- `{artifact_dir}/component_inventory.json`

## Implementation Rules

1. Treat the design-system artifacts as the source of truth.
2. Keep implementation aligned with brand keywords and anti-keywords.
3. Implement high-priority families before medium-priority families.
4. Reuse or extend primitives before adding net-new components.
5. Preserve existing features, entry points, and task flows unless removal is explicitly requested.
6. Keep supported themes and responsive layouts working during refactors.
7. Use semantic tokens before introducing hardcoded surface or text colors.
8. Update nearby documentation or tests when behavior or structure changes.
9. Respect curated palette roles and reference colors recorded in the token schema when choosing UI colors.

## Output Expectations

- State which artifact files informed the implementation.
- Mention any gap between the requested UI and the current system artifacts.
- Call out any remaining feature-regression or theme-regression risk.
"""


def _codex_plugin_openai_yaml() -> str:
    return """display_name: Design System Harness
short_description: Apply local design-system artifacts inside implementation repos
default_prompt: Implement UI changes using the design-system artifacts in this repository
"""


def _write_if_allowed(path: Path, content: str, force: bool, created: list[str]) -> None:
    if path.exists() and not force:
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")
    created.append(str(path))
