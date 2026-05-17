from __future__ import annotations

import json
from pathlib import Path

from .graph_builders import (
    FREE_SOURCED_VISUAL_PROVIDER_RULES,
    LICENSED_VISUAL_PROVIDER_RULES,
    REFERENCE_ONLY_PROVIDER_RULES,
    SOURCED_VISUAL_ASSET_CANDIDATE_MANIFEST_PATH,
    SOURCED_VISUAL_ASSET_FALLBACK_POLICY,
    SOURCED_VISUAL_ASSET_RECORD_REQUIRED_FIELDS,
    VISUAL_ASSET_COMPATIBLE_MANIFEST_PATHS,
    VISUAL_ASSET_MANIFEST_PATH,
    VISUAL_ASSET_MANIFEST_REQUIRED_FIELDS,
    VISUAL_ASSET_MANIFEST_SCHEMA,
    VISUAL_ASSET_PROMPT_PACK_PATH,
    VISUAL_ASSET_RECORD_REQUIRED_FIELDS,
)
from .utils import ensure_dir


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

    rebuild_skill_dir = ensure_dir(skills_dir / "design-system-rebuild")
    _write_if_allowed(
        rebuild_skill_dir / "SKILL.md",
        _claude_rebuild_skill(artifact_dir),
        force=force,
        created=created,
    )
    _write_if_allowed(
        agents_dir / "design-system-rebuild.md",
        _claude_rebuild_agent(artifact_dir),
        force=force,
        created=created,
    )


def _scaffold_codex_pack(target_repo: Path, artifact_dir: str, force: bool, created: list[str]) -> None:
    plugin_root = ensure_dir(target_repo / "plugins" / "design-system-harness")
    ensure_dir(plugin_root / ".codex-plugin")
    skills_root = ensure_dir(plugin_root / "skills")
    architect_dir = ensure_dir(skills_root / "design-system-architect")
    implementer_dir = ensure_dir(skills_root / "design-system-implementer")
    visual_assets_dir = ensure_dir(skills_root / "design-system-visual-assets")
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
            "imagery",
            "codex",
            "skills",
        ],
        "skills": "./skills/",
        "interface": {
            "displayName": "Design System Harness",
            "shortDescription": "Apply design-system artifacts inside a real implementation repo",
            "longDescription": "Provides Codex skills for reading design-system artifacts, implementing tokens/components, creating brand-aligned generated imagery with the built-in Codex image_gen skill, and using license-verified sourced visual fallback when generation is unavailable or real-world photography is more appropriate. API and CLI image fallbacks are disabled.",
            "developerName": "Design Ontology Harness",
            "category": "Coding",
            "capabilities": ["Interactive", "Write"],
            "defaultPrompt": [
                "Implement UI changes using the local design-system artifacts and component inventory",
                "Ship normal light mode and dark mode together unless a single mode is explicitly requested",
                "When a screen needs professional imagery, use Codex image_gen first; if unavailable, use license-verified sourced visual fallback without API fallback",
                "Treat favicon, app-shell mark, and web manifest icon as required brand-specific identity assets",
                "For dashboards, tools, sports/data, and community products, lead with operational product surfaces instead of pitch-deck heroes or homogeneous card walls",
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
        visual_assets_dir / "SKILL.md",
        _codex_visual_asset_skill(artifact_dir),
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
- `STYLE.md` / `DESIGN.md`
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
- `presets/<id>/STYLE.md` -> `{artifact_dir}/STYLE.md`
- `presets/<id>/DESIGN.md` -> `{artifact_dir}/DESIGN.md`
- `build/system/blueprint/token_schema.json` -> `{artifact_dir}/token_schema.json`
- `build/system/blueprint/component_inventory.json` -> `{artifact_dir}/component_inventory.json`
- `build/system/blueprint/system_ontology.json` -> `{artifact_dir}/system_ontology.json`
- `build/system/components/` -> `{artifact_dir}/components/`
"""


def _script_aware_typography_guidance() -> str:
    return """
## Script-aware typography

If `system_spec.md` or `token_schema.json` contains typography `script_guardrails`, treat that as the default-safe implementation baseline, not optional polish.

- For Korean-first UI or marketing copy, default to `word-break: keep-all` plus `overflow-wrap: normal`.
- Use `text-wrap: balance` on major headings when browser support allows it.
- Avoid forced `<br/>` in Korean headlines until desktop/mobile wrapping is verified with real copy.
- For wide or serif Hangul display fonts, start one type step smaller than English-first hero comps and only scale up after wrap review.
- Respect font-specific line-height and letter-spacing guidance from the artifacts instead of reusing English defaults.
"""


def _responsive_resilience_guidance() -> str:
    return """
## Responsive resilience

Treat mobile fit as a contract, not a final polish pass.

- Verify changed screens at 320, 360, 390, 430, 768, and desktop widths.
- A screen is not complete if `document.documentElement.scrollWidth > window.innerWidth`.
- Buttons, CTAs, tabs, chips, and toolbar actions must keep `max-inline-size: 100%`; controls inside flex/grid parents need `min-inline-size: 0`.
- Avoid fixed `width` / `min-width` px values on button-like controls. If a large CTA width is intentional, add a <=480px wrap or stack fallback.
- Action rows must use `flex-wrap: wrap` or switch to a vertical stack on narrow viewports.
- Do not use `width: 100vw` inside padded containers, and do not hide `overflow-x` on `body` as the fix for an overflowing control.
- Test Korean CTA labels with realistic copy; prefer wrapping or stacking over clipping and `white-space: nowrap`.
"""


def _color_mode_parity_guidance() -> str:
    return """
## Color mode parity

Normal light mode and dark mode travel together unless the user explicitly asks for a single-mode artifact.

- Use light mode as the default `:root` or app-default token set.
- Add dark mode as an override such as `[data-theme="dark"]`, a theme provider, or equivalent framework mode.
- Components consume the same semantic variables in both modes; only token values change.
- Do not ship dark-only dashboards, tools, landing pages, or prototypes.
- Verify both modes with screenshots or DOM checks when the implementation has a visible UI shell.
"""


def _commercial_product_realism_guidance() -> str:
    return """
## Commercial product realism

For dashboards, tools, sports/data products, and community products, the first viewport should feel like an operated product, not a pitch deck.

- Lead with the active task surface: status strip, filters/date rail, table/list rows, next item, source/update label, or primary workflow.
- Do not open product UIs with an oversized marketing hero, generic slogan, and equally weighted feature cards unless the user explicitly asks for a landing page.
- Avoid homogeneous card walls. Promote one primary workflow module, compress secondary information into rows/tables/rails, and vary density only when the information architecture justifies it.
- Exact numbers, predictions, rankings, poll counts, odds, or operational claims need source/update context or a visible sample/demo label.
- Generated or decorative imagery must support the domain object, venue, person, product, or state; it must not outrank data, navigation, controls, or the first operational surface.
- Include realistic state texture: live/final/upcoming/delayed/empty/error/source-updated as appropriate for the domain.
"""


def _emoji_to_svg_refactor_guidance() -> str:
    return """
## Emoji-to-SVG refactor

When refactoring existing UI, do not merely report emoji UI affordances. Replace them.

- Scan buttons, cards, badges, tabs, nav items, status indicators, empty states, toasts, and banners for emoji-looking icons or visual markers.
- Prefer the project's existing icon library when it is already installed and visually compatible.
- Reuse existing local SVG/icon components when available.
- If no suitable icon exists, create a simple local SVG file or SVG component in the nearest existing icons/assets directory.
- Bind SVG stroke/fill to `currentColor` or design tokens, not hard-coded colors.
- Decorative icons use `aria-hidden="true"`; semantic icons need an accessible label or adjacent visible text.
- Do not replace user-generated emoji content, chat text, blog body, or emoji-picker data.
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

1. Read `{artifact_dir}/STYLE.md` or `{artifact_dir}/DESIGN.md` first when present.
2. Read `{artifact_dir}/system_spec.md`.
3. Read `{artifact_dir}/token_schema.json` and `{artifact_dir}/component_inventory.json`.
4. If present, use `{artifact_dir}/system_ontology.json` to understand relations between principles, token categories, and component families.
5. Translate user requests into:
   - affected principles
   - affected token categories
   - affected component families
   - required implementation order
6. Favor extending existing primitives over inventing new components.
7. Explicitly guard against anti-keywords from the system spec.
8. Preserve existing user-facing entry points and feature surfaces unless the user explicitly asks for a structural change.
9. Prefer incremental rollout plans over full-shell rewrites.
10. If `token_schema.json` contains a curated color reference or palette roles, treat that as the starting point for semantic color decisions.
11. If typography artifacts include script guardrails, account for their line-break and type-scale rules before proposing hero or landing compositions.
12. Treat responsive resilience as a planning constraint: buttons and action groups need a mobile wrap/stack strategy before implementation begins.
13. For dashboard/tool/data/community products, plan the first viewport around the operational task surface before considering hero imagery or feature cards.

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

1. Read `{artifact_dir}/IMPLEMENTATION_CONTRACT.md` when present.
2. Read `{artifact_dir}/STYLE.md` or `{artifact_dir}/DESIGN.md` when present.
3. Read `{artifact_dir}/system_spec.md`.
4. Read `{artifact_dir}/token_schema.json`.
5. Read `{artifact_dir}/component_inventory.json`.

Implementation rules:

- Treat the design-system artifacts as the source of truth.
- Keep implementation aligned with the product's brand keywords and anti-keywords.
- Implement high-priority component families before medium-priority families.
- Reuse or extend primitives before adding net-new components.
- Preserve existing features, navigation entry points, and data flows unless removal is explicitly requested.
- Keep supported themes, breakpoints, and critical interaction states working while refactoring.
- Use semantic tokens only; raw color values belong in `{artifact_dir}` token artifacts, not implementation files.
- Always include both normal light mode and dark mode unless the task explicitly asks for one mode only.
- Default to the smallest viable surface refactor; do not rewrite the whole shell unless the task explicitly calls for it.
- If `token_schema.json` includes a curated color reference or palette roles, align color decisions to that input before inventing a new palette.
- Visual references are morphology inputs only. Do not absorb reference palettes, type scales, navigation labels, domain IA, or product copy.
- Token binding is necessary but not sufficient: never recombine `--ds-*` roles into a new reference-like palette.
- If user/reviewer feedback exposes a repeatable failure pattern, promote it into governance docs or lint rules before calling the screen complete.
- For dashboards, tools, sports/data products, and community products, lead with operational substance instead of pitch-deck hero composition.
- Update nearby documentation or tests when implementation meaningfully changes.
- NEVER change layout properties (display, flex-direction, grid-template, position, width, height).
- NEVER change font-size or line-height to "fit the token scale." Existing sizes are tuned to the layout. Only replace when the token resolves to the exact same px. If no match, keep original + TODO.
- NEVER round spacing values to the nearest token — if no exact match, leave as-is with a TODO.
- **NEVER use emojis as UI icons, state indicators, button decorations, or navigation markers** (no 🎨 ✅ 🔥 ⚡ 🚀 ❌ ⭐ 📊 etc.). Always implement proper SVG icon components or import from Lucide / Heroicons / Phosphor / Tabler. Emojis are only allowed inside user-generated content (blog text, user input) — never as part of the design system itself.
- **NEVER leave half-finished components** like "TODO component", "placeholder card", "temp button". Read `{artifact_dir}/components/component_specs.md` and implement the full anatomy, states, and token bindings defined there.
- **NEVER use bare library components (e.g., default `<Button>` from a UI lib) without binding design tokens.** Every component must have its colors, spacing, radius, and typography wired to the token system. If you import from a library, wrap it and override styles with CSS variables from the token schema.

{_script_aware_typography_guidance()}

{_color_mode_parity_guidance()}

{_commercial_product_realism_guidance()}

{_responsive_resilience_guidance()}

{_emoji_to_svg_refactor_guidance()}

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

1. Read `{artifact_dir}/STYLE.md` or `{artifact_dir}/DESIGN.md` first when present.
2. Read `{artifact_dir}/system_spec.md`.
3. Then read `{artifact_dir}/token_schema.json` and `{artifact_dir}/component_inventory.json`.
4. Map the request to:
   - principles
   - token categories
   - component families
   - rollout order
5. Prefer extending existing primitives over introducing new abstractions.
6. Call out conflicts with anti-keywords or missing artifacts.
7. Treat existing screens and interaction entry points as constraints, not disposable implementation details.
8. Recommend incremental rollout steps before proposing a shell-level rewrite.
9. If the token schema includes curated palette roles, use those roles as the default color direction in the plan.
10. If typography script guardrails exist, reflect them in line length, headline scale, and Korean copy layout decisions.
11. Include the mobile overflow prevention strategy for button/action groups when planning responsive screens.
12. For dashboard/tool/data/community products, make the first viewport task-led and provenance-aware, not a marketing hero plus card wall.

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

1. Read `{artifact_dir}/IMPLEMENTATION_CONTRACT.md` when present.
2. Read `{artifact_dir}/STYLE.md` or `{artifact_dir}/DESIGN.md` when present.
3. Read `{artifact_dir}/system_spec.md`.
4. Read `{artifact_dir}/token_schema.json`.
5. Read `{artifact_dir}/component_inventory.json`.

Implementation rules:

- Keep code aligned with system principles.
- Use the token schema to name and organize variables or theme values.
- Use the component inventory to decide whether to create, extend, or defer a component.
- Preserve existing feature surfaces and task-completion paths unless the user explicitly wants a structural redesign.
- Maintain supported themes and responsive layouts; do not introduce hardcoded color values in implementation files.
- Prefer local, reversible refactors over all-at-once shell rewrites.
- If token_schema includes curated palette roles or selected reference colors, preserve that color direction while implementing.
- If the request falls outside the current system artifacts, state the gap clearly instead of inventing an ungrounded pattern.
- Treat favicon, app-shell mark, and web manifest icon as required brand-specific identity assets, not generic initials tiles.
- For dashboards, tools, sports/data products, and community products, lead with operational product state, filters, tables/lists, and provenance before decorative imagery.
- NEVER change layout properties, element sizes, or text-flow properties (font-size, line-height, white-space, word-break) unless explicitly requested.
- NEVER change font-size to match a token scale — existing sizes are already tuned to the layout. Only replace when the token is the exact same px value. "Fitting the scale" is a design change, not a refactor.
- When replacing spacing/sizing values with tokens, only use exact matches — never round to the nearest token value.

{_script_aware_typography_guidance()}

{_commercial_product_realism_guidance()}

{_responsive_resilience_guidance()}
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

**이모지 UI 위반**
- 버튼, 카드, 배지, 탭, 네비게이션, 상태 표시, empty state에 이모지가 아이콘처럼 쓰임
- 이모지를 그대로 두거나 텍스트 glyph로 스타일링하는 임시 처리

**상용 제품 리얼리즘 위반**
- 대시보드/도구/데이터 제품이 실제 작업 표면보다 큰 히어로, 슬로건, 균일한 카드벽으로 시작함
- 정확한 수치, 예측, 순위, 운영 상태가 출처/업데이트 시각/샘플 라벨 없이 확정 데이터처럼 보임
- 생성 이미지가 표, 필터, 상태, 내비게이션보다 더 큰 비중을 차지함

{_emoji_to_svg_refactor_guidance()}

{_commercial_product_realism_guidance()}

### Phase 3: 리팩토링 실행

탐지된 문제를 **우선순위 순서**로 수정합니다:

1. **접근성 위반** (가장 먼저 — 법적/윤리적 요구사항)
2. **이모지 UI 교체** (버튼/카드/상태 아이콘을 SVG 파일·컴포넌트 또는 아이콘 라이브러리로 교체)
3. **토큰 하드코딩** (시스템의 기반)
4. **컴포넌트 구조** (누락된 상태/파트 추가)
5. **브랜드 정합성** (시각적 미세 조정)

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

1. Read `{artifact_dir}/STYLE.md` or `{artifact_dir}/DESIGN.md` when present.
2. Read `{artifact_dir}/component_specs.json` or `{artifact_dir}/components/component_specs.json`.
   - Fallback: `{artifact_dir}/component_inventory.json`
3. Read `{artifact_dir}/token_schema.json`.
4. Read `{artifact_dir}/system_spec.md`.

These artifacts are your source of truth. If any core file is missing, report which files are needed.

## What to fix (in priority order)

1. **Accessibility violations**: missing roles, aria attributes, labels, focus management, touch targets
2. **Hardcoded tokens**: colors (#hex, rgb, tailwind color classes), spacing (px values not on scale), font sizes, border-radius, shadows → replace with semantic tokens
3. **Missing component states**: components that lack states defined in the spec (disabled, loading, error, hover, focus)
4. **Missing anatomy parts**: components missing required parts from the spec (e.g., button without loading spinner slot)
5. **Emoji UI affordances**: emoji glyphs used as button/card/badge/status/nav icons → replace with SVG files/components or an approved icon library
6. **Brand misalignment**: visual patterns that conflict with brand keywords or match anti-keywords

{_emoji_to_svg_refactor_guidance()}

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


def _claude_rebuild_skill(artifact_dir: str) -> str:
    return f"""---
name: design-system-rebuild
description: 기존 화면의 기능을 보존하면서 디자인 시스템 스펙 기반으로 화면을 새로 구성합니다. /design-rebuild 로 실행하세요.
allowed-tools: Read Glob Grep Bash Edit Write
paths:
  - "{artifact_dir}/**"
  - "src/**"
  - "app/**"
  - "components/**"
  - "styles/**"
  - "lib/**"
---

# Design System Rebuild

기존 AI 생성 UI나 프로토타입을 디자인 시스템 스펙 기반으로 **처음부터 다시 구성**합니다.
Refactor(토큰 교체)와 다릅니다 — 레이아웃, 타이포그래피 위계, 색상 구성, 컴포넌트 구조를 모두 재설계합니다.

## Refactor vs Rebuild 차이

| | Refactor | **Rebuild** |
|---|---|---|
| 목표 | 기존 코드에 토큰 연결 | **화면 전체를 스펙 기반으로 재구성** |
| 레이아웃 | 건드리지 않음 | **스펙에 맞게 재설계** |
| 서체 | 변수명만 교체 | **위계 자체를 재구성** |
| 여백 | 같은 값만 교체 | **리듬과 호흡을 재설계** |
| 임팩트 | 작음 (안전) | **크게 달라 보임 (변환)** |

## 실행 절차

### Phase 1: 스펙 로드

1. `{artifact_dir}/system_spec.md` — 디자인 원칙, 브랜드 키워드, 안티 키워드
2. `{artifact_dir}/token_schema.json` — 토큰 체계 (color, typography, spacing, motion)
3. `{artifact_dir}/components/component_specs.json` — 컴포넌트별 상세 스펙
4. `{artifact_dir}/component_inventory.json` — 컴포넌트 패밀리

특히 아래 정보를 반드시 추출합니다:
- **color palette**: primary, accent, surface, semantic states (이 색상을 실제로 사용)
- **typography**: heading/body/mono 서체, type scale, line-height (이 서체와 크기를 실제로 적용)
- **design principles**: 예를 들어 "calm" → 절제된 모션, "bold" → 강한 대비
- **component anatomy**: 각 컴포넌트의 필수 파트와 상태

### Phase 2: 기존 화면 분석

대상 파일을 읽고 **기능 목록**만 추출합니다 (시각적 구현은 버림):

```
기능 추출 예시:
- 이 화면은 "리그 순위표"를 보여줌
- 데이터: 순위, 팀명, 경기수, 승/무/패, 골득실, 승점, 최근 5경기
- 인터랙션: 컬럼 정렬, 시즌 필터
- 상태: 로딩, 빈 상태, 에러
- 네비게이션: 상단 탭, 팀 클릭 시 상세 이동
```

기존 코드의 시각적 결정(색상, 여백, 서체 크기, 레이아웃)은 참고하지 않습니다.
오직 **"이 화면이 무엇을 하는가"**만 파악합니다.

### Phase 3: 디자인 시스템 기반 재구성

추출한 기능을 디자인 시스템 스펙으로 다시 만듭니다.

#### 3-1. 색상 적용

system_spec.md의 Color Reference에서 가져온 palette를 실제로 사용합니다:
- **배경**: canvas/surface/surface_tint 토큰 — dark mode first면 어두운 surface
- **텍스트**: ink/ink_muted 토큰 — 위계에 따라 primary/secondary 구분
- **강조**: primary/accent 컬러 — CTA, 활성 상태, 하이라이트에만 사용
- **상태**: success/warning/danger/info — semantic state에만 사용
- **보더**: border/border_subtle — 구조를 드러내되 과하지 않게

절대로 Tailwind 기본 색상(blue-500, gray-100 등)을 쓰지 않습니다.
CSS 변수 또는 프로젝트의 토큰 시스템으로 적용합니다.

#### 3-2. 타이포그래피 위계

system_spec.md의 Typography System에서:
- **heading 서체**: 페이지 제목, 섹션 헤더에 적용
- **body 서체**: 본문, UI 라벨에 적용
- **mono 서체**: 데이터, 코드, 숫자에 적용
- **type scale**: 각 위치의 font-size를 scale에서 선택
- **line-height**: preset에 따라 적용

위계 구성 원칙:
```
페이지 제목: heading font, 2xl-3xl, weight 800
섹션 제목:   heading font, xl, weight 700
카드 제목:   body font, lg, weight 600
본문:        body font, md, weight 400
캡션/라벨:   body font, sm, weight 500, uppercase + letter-spacing (optional)
데이터 숫자: mono 또는 tabular figures, lg-2xl, weight 700-800
```

{_script_aware_typography_guidance()}

{_commercial_product_realism_guidance()}

{_responsive_resilience_guidance()}

#### 3-3. 여백과 리듬

spacing scale을 활용해 시각적 리듬을 만듭니다:
```
페이지 패딩:    spacing-24 ~ spacing-32
섹션 간 간격:   spacing-24 ~ spacing-32
카드 내부 패딩:  spacing-16 ~ spacing-24
요소 간 간격:   spacing-8 ~ spacing-16
인라인 간격:    spacing-4 ~ spacing-8
```

리듬 원칙:
- 큰 단위는 작은 단위의 배수 (8→16→32)
- 관련 요소는 가깝게, 다른 그룹은 멀게 (근접성 원칙)
- 빈 공간을 두려워하지 않기 — 여백이 위계를 만듬

#### 3-4. 레이아웃 구성

화면 유형별 레이아웃 패턴:
```
대시보드:    운영 헤더/상태 스트립 → 필터/날짜 레일 → 핵심 표·리스트 → 보조 요약 카드
목록/피드:   상단 필터/검색 → 반복 카드/행 → 페이지네이션
상세 페이지:  헤더(제목+메타) → 메인 콘텐츠 → 사이드 정보 → 관련 항목
설정:       좌측 메뉴 → 우측 폼 섹션
```

#### 3-5. 컴포넌트 구성

component_specs.json의 각 컴포넌트를:
- anatomy에 정의된 파트를 모두 포함
- states에 정의된 상태를 모두 처리
- accessibility에 정의된 속성을 모두 적용
- 브랜드 적용 규칙을 반영

#### 3-6. 인터랙션과 모션

```
hover:      opacity 변화 또는 background shift (brand keyword에 따라)
transition: 120-200ms ease-out (calm이면 느리게, energetic이면 빠르게)
loading:    skeleton 또는 spinner (컴포넌트 스펙에 따라)
focus:      focus-ring 토큰 (접근성 필수)
```

### Phase 4: 코드 작성

재구성한 화면을 실제 코드로 작성합니다.

작성 규칙:
- 프로젝트의 기존 프레임워크/라이브러리를 사용 (React, Vue, Svelte 등)
- CSS 변수 또는 프로젝트의 토큰 시스템을 통해 스펙 값 적용
- 컴포넌트 분리: 재사용 가능한 단위로 분리 (하나의 거대한 파일 금지)
- TypeScript를 사용 중이면 props 타입 정의
- 접근성 속성 반드시 포함 (role, aria, label, scope 등)

### Phase 5: 검증 및 리포트

```
## Rebuild 결과

### 재구성된 화면
- [화면명]: [주요 변경 사항]

### 적용된 디자인 시스템 요소
- Color: [사용한 palette roles]
- Typography: [heading/body/mono 서체 + scale]
- Components: [스펙 기반으로 구성한 컴포넌트 목록]
- Accessibility: [적용한 접근성 속성]

### 보존된 기능
- [기존 기능이 그대로 동작하는지 확인 목록]

### 수동 확인 필요
- [실제 데이터로 테스트 필요한 항목]
- [반응형 확인 필요한 breakpoint]
```

## 금지 사항

- 기존 기능을 제거하거나 빠뜨리지 않음 — 모든 데이터와 인터랙션을 보존
- 라우팅이나 API 호출 로직을 변경하지 않음
- 스펙에 없는 장식적 요소를 추가하지 않음 (그라데이션, 글로우 등 — 스펙에 있으면 OK)
- 안티 키워드에 해당하는 시각적 패턴을 사용하지 않음
- 접근성을 빠뜨리지 않음 — rebuild는 접근성이 더 좋아져야 함
- **이모지를 UI 요소로 사용하지 않음** (🎨 ✅ 🔥 ⚡ 🚀 ❌ ⭐ 📊 등). 아이콘 자리에는 반드시 SVG 컴포넌트 또는 Lucide/Heroicons/Phosphor/Tabler 라이브러리 사용. 이모지는 본문 콘텐츠(사용자 입력, 블로그 텍스트)에서만 허용.
- **반쪽 구현 금지** — "TODO 컴포넌트", "임시 버튼", "플레이스홀더 카드"를 남기지 않음. component_specs.json의 anatomy/states/tokens를 그대로 따라 완전히 구현.
- **라이브러리 기본 컴포넌트 금지** — `<Button>` 같은 라이브러리 컴포넌트를 기본 스타일로 그냥 쓰지 않음. 반드시 디자인 토큰으로 색상, spacing, radius, typography를 명시적으로 바인딩.
"""


def _claude_rebuild_agent(artifact_dir: str) -> str:
    return f"""---
name: design-system-rebuild
description: 디자인 시스템 스펙 기반으로 화면을 새로 구성하는 에이전트. 기존 기능은 보존하되 시각적 품질을 근본적으로 높입니다.
tools: Read, Glob, Grep, Bash, Edit, Write
model: sonnet
color: purple
---

You are a design-system rebuild specialist.

Your job is to take existing screens and rebuild them from scratch using the project's design system specifications. This is NOT refactoring (token swapping) — this is redesign with the full design system applied.

## What makes this different from refactoring

Refactoring: `color: #3b82f6` → `color: var(--accent)` (same layout, different variable)
**Rebuild**: The entire visual composition is reconstructed — layout, typography hierarchy, color usage, spacing rhythm, component structure — all driven by the design system spec.

## Startup

1. Read `{artifact_dir}/STYLE.md` or `{artifact_dir}/DESIGN.md` when present.
2. Read `{artifact_dir}/system_spec.md` — extract brand keywords, principles, color palette, typography system
3. Read `{artifact_dir}/token_schema.json` — get the actual token values
4. Read `{artifact_dir}/components/component_specs.json` — component anatomy, states, accessibility
5. If color palette exists, use those EXACT colors (not Tailwind defaults)
6. If typography system exists, use those EXACT fonts and scale

## Process

1. **Analyze existing screen**: Extract ONLY the functional requirements (what data, what actions, what states). Ignore all visual decisions.
2. **Design with the system**: Apply the full design system — palette, typography hierarchy, spacing rhythm, component specs, accessibility
3. **Write code**: Rebuild the screen using the project's framework, applying design system tokens throughout
4. **Verify**: Confirm all original functionality is preserved, all accessibility rules applied

## Key principles

- The design system palette IS the color scheme — never fall back to Tailwind defaults
- Typography hierarchy creates visual importance — heading font for titles, body for content, mono for data
- Spacing creates rhythm — consistent scale, proximity groups related items, whitespace creates hierarchy
- Components follow the spec — all anatomy parts, all states, all accessibility attributes
- Anti-keywords are hard constraints — if "cluttered" is anti, ensure generous whitespace
- Brand keywords drive visual decisions — "bold" means strong contrast, "calm" means subtle transitions
- Commercial product realism matters — operational product screens lead with real workflow state, filters, data rows, and provenance before hero imagery or feature-card grids

{_script_aware_typography_guidance()}

{_commercial_product_realism_guidance()}

{_responsive_resilience_guidance()}

## What to preserve from existing code

- All data bindings and state management
- All API calls and data fetching logic
- All routing and navigation targets
- All event handlers and business logic
- All conditional rendering logic

## What to replace

- All visual styling (colors, spacing, typography, shadows, borders, radius)
- Layout composition (grid structure, card arrangements, section ordering)
- Component structure (anatomy, states, accessibility)
- Visual hierarchy (what's prominent, what's secondary, what's subtle)
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

- `{artifact_dir}/IMPLEMENTATION_CONTRACT.md`
- `{artifact_dir}/STYLE.md` or `{artifact_dir}/DESIGN.md`
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
8. If typography script guardrails exist, incorporate them into headline scale, measure, and Korean copy wrapping decisions up front.
9. Plan button/action-group mobile behavior up front: wrap, stack, or prove it fits at 320px without horizontal scroll.
10. Plan light/default and dark mode token coverage up front; light is the default mode.
11. Treat the app icon as a required brand identity asset, not a generic initials tile.
12. For dashboard/tool/data/community products, plan the first viewport around operational state, filters, data rows, and provenance before hero imagery.
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

- `{artifact_dir}/IMPLEMENTATION_CONTRACT.md`
- `{artifact_dir}/STYLE.md` or `{artifact_dir}/DESIGN.md`
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
7. Use semantic tokens only; keep raw surface or text color values in design-system artifacts.
8. Update nearby documentation or tests when behavior or structure changes.
9. Respect curated palette roles and reference colors recorded in the token schema when choosing UI colors.
10. Visual references are morphology inputs only; do not absorb reference palettes, type scales, navigation labels, domain IA, or product copy.
11. Token binding is necessary but not sufficient: never recombine `--ds-*` roles into a new reference-like palette.
12. Promote repeatable user/reviewer feedback into governance docs or lint rules before calling a screen complete.
13. **ALWAYS ship normal light mode and dark mode together** unless the user explicitly asks for one mode only. Light mode is the default token set; dark mode is an override.
14. **NEVER use emojis as UI icons, state indicators, or button decorations** (no 🎨 ✅ 🔥 ⚡ 🚀 ❌ ⭐ 📊). Always implement SVG icon components or import from Lucide / Heroicons / Phosphor / Tabler. Emojis only belong in user-generated content, never in system UI.
15. **NEVER leave half-finished components** ("TODO", "placeholder", "temp"). Read `{artifact_dir}/components/component_specs.md` and implement the full anatomy, states, and token bindings.
16. **NEVER use bare library components without token binding.** If you import from a UI library, wrap it and override colors, spacing, radius, and typography using tokens from the schema.
17. **NEVER ship generic initials tiles as final app icons.** Favicon, app-shell marks, and web manifests need brand-specific SVG identity assets.
18. **NEVER let dashboard/tool/data/community products open like pitch decks** unless the user explicitly asks for a landing page. Lead with operational state, filters, tables/lists, and source/update context.

{_script_aware_typography_guidance()}

{_color_mode_parity_guidance()}

{_commercial_product_realism_guidance()}

{_responsive_resilience_guidance()}

{_emoji_to_svg_refactor_guidance()}

## Output Expectations

- State which artifact files informed the implementation.
- Mention any gap between the requested UI and the current system artifacts.
- Call out any remaining feature-regression or theme-regression risk.
"""


def _codex_visual_asset_skill(artifact_dir: str) -> str:
    compatible_manifest_paths = "\n".join(
        f"   - `{path}`" for path in VISUAL_ASSET_COMPATIBLE_MANIFEST_PATHS
    )
    manifest_fields = "\n".join(
        f"   - `{field}`" for field in VISUAL_ASSET_MANIFEST_REQUIRED_FIELDS
    )
    asset_record_fields = "\n".join(
        f"   - `{field}`" for field in VISUAL_ASSET_RECORD_REQUIRED_FIELDS
    )
    sourced_asset_record_fields = "\n".join(
        f"   - `{field}`" for field in SOURCED_VISUAL_ASSET_RECORD_REQUIRED_FIELDS
    )
    free_provider_list = ", ".join(f"`{provider['label']}`" for provider in FREE_SOURCED_VISUAL_PROVIDER_RULES)
    licensed_provider_list = ", ".join(f"`{provider['label']}`" for provider in LICENSED_VISUAL_PROVIDER_RULES)
    reference_only_provider_list = ", ".join(f"`{provider['label']}`" for provider in REFERENCE_ONLY_PROVIDER_RULES)
    return f"""---
name: design-system-visual-assets
description: Generate or source professional brand-aligned imagery for Codex implementations. Use when a screen, landing page, empty state, editorial hero, or product section needs raster imagery that matches the local design-system artifacts.
---

# Design System Visual Assets

Use this skill when the implementation would look more professional with generated or sourced raster imagery instead of flat placeholder blocks, generic gradients, emoji, or stock-like decoration.

## Required Inputs

Read these files first when they exist:

- `{artifact_dir}/STYLE.md` or `{artifact_dir}/DESIGN.md`
- `{artifact_dir}/system_spec.md`
- `{artifact_dir}/token_schema.json`
- `{artifact_dir}/component_inventory.json`
- `{artifact_dir}/visual_reference_report.json`
- `{artifact_dir}/components/component_specs.md`

If `visual_reference_report.json` is missing, infer image direction from `system_spec.md`, brand keywords, anti-keywords, palette roles, typography mood, and product domain. State that the image direction is ungrounded by visual references.

## When To Generate Images

Generate imagery for:

- landing or editorial heroes that need a first-viewport visual signal
- product, venue, object, or media cards that benefit from real visual substance
- empty states, onboarding panels, or feature sections where illustration clarifies the product
- case-study or article covers where the system spec calls for editorial treatment

Do not generate imagery for:

- icons, logos, button glyphs, tabs, toggles, or status markers
- app icons, favicons, or app-shell brand marks; these are deterministic brand identity assets, not generated raster imagery
- components that should be built with CSS, SVG primitives, or an icon library
- dashboard/tool/data-product first viewports where users need tables, schedules, filters, live state, or provenance before decorative visuals
- copyrighted characters, real brands, real people, or identifiable private locations unless the user explicitly provided licensed source material
- purely atmospheric blurred backgrounds that do not reveal the product, state, place, or object

## Acquisition Order

1. Prefer Codex built-in `image_gen` when a brand-specific synthetic image is appropriate.
2. Use sourced visual fallback when `image_gen` is unavailable, fails, or the screen needs real-world photographic evidence more than generated imagery.
3. If neither path can meet the manifest and license contract, leave a prompt/candidate pack and report that imagery was not integrated.

Never switch to CLI, SDK runner, or OpenAI image API fallback unless the user explicitly asks for that different path.

## Codex Imagegen Workflow

When Codex exposes the built-in `image_gen` tool through the installed imagegen skill:

1. Use the built-in `image_gen` path. Do not invoke CLI mode, SDK runners, or OpenAI API fallback.
2. Generate 2-4 candidates for each major image slot with one built-in call per candidate or variant.
3. Base prompts on the artifact files, not on generic style words.
4. Include concrete subject matter, composition, camera/illustration treatment, palette constraints, density, material language, and anti-keywords.
5. Prefer usable aspect ratios:
   - hero: `16:9`, `3:2`, or wide responsive crop
   - card thumbnail: `4:3` or `1:1`
   - editorial cover: `4:5` or `3:4`
6. Copy accepted project-bound assets into the workspace before code references them. Preserve the original `$CODEX_HOME/generated_images/<session-id>/...` PNG path in the manifest when available, but never make runtime code depend on that agent-local path.
7. Write or update the visual asset manifest using schema `{VISUAL_ASSET_MANIFEST_SCHEMA}`.

Preferred manifest path:

- `{VISUAL_ASSET_MANIFEST_PATH}`

Compatible manifest paths:

{compatible_manifest_paths}

Required top-level manifest fields:

{manifest_fields}

Required asset record fields:

{asset_record_fields}

If the built-in imagegen path is unavailable or fails, do not pretend an image was generated and do not call an API fallback. Move to the sourced visual fallback below, or create a ready-to-run prompt pack at `{VISUAL_ASSET_PROMPT_PACK_PATH}` or the nearest existing docs/assets directory, then report that generation was skipped.

## Sourced Visual Fallback

Use this fallback for free/rights-clear visual search, not for another image generation provider.

Provider tiers:

- Free sourced providers: {free_provider_list}
- Licensed providers: {licensed_provider_list}
- Reference-only providers: {reference_only_provider_list}

Tier rules:

- Free sourced provider images can become runtime assets only when per-asset license metadata is recorded.
- Licensed provider images can become runtime assets only when user-supplied purchase/license proof, usage scope, and licensed-to metadata are recorded.
- Reference-only provider images are for morphology, density, hierarchy, and flow research only. Do not copy them into runtime assets.

Selection rules:

1. Search for 3-8 candidates that match the product domain, subject, crop, and visual role.
2. Reject any candidate without source URL, download URL, provider, author/creator, license label, and attribution requirement.
3. Reject paid-provider results unless the user supplied license proof or the asset is already licensed for this project.
4. Reject reference-only results as runtime assets; summarize their morphology only.
5. Reject results with unclear rights, recognizable private people, copyrighted characters, third-party logos, or brand endorsement risk unless the user supplied permission.
6. Copy the accepted asset into the workspace before implementation references it. Do not hotlink remote search/CDN URLs.
7. Record source metadata in `{VISUAL_ASSET_MANIFEST_PATH}` with acquisition mode `sourced`.
8. Optionally keep reviewed-but-not-used candidates in `{SOURCED_VISUAL_ASSET_CANDIDATE_MANIFEST_PATH}`.

Sourced fallback policy:

- `{SOURCED_VISUAL_ASSET_FALLBACK_POLICY}`

Required sourced asset record fields:

{sourced_asset_record_fields}

Sourced visual assets are still not valid replacements for icons, logos, app icons, favicons, button glyphs, status markers, or flags unless the exact asset license and identity use are explicitly approved.

## Prompt Recipe

Build prompts with this structure:

```text
Professional product image for [brand/product/screen], [specific subject], [composition], [visual material], [palette from token_schema], [density and surface cues from visual_reference_report], [lighting/camera or illustration treatment], no logos, no readable copyrighted UI, no stock-photo feel, no emoji, no generic gradient background.
```

For Korean-first products, include Hangul-safe composition constraints:

- leave quiet negative space where Korean headings may sit
- avoid dense texture behind text
- keep faces/objects away from likely text columns
- avoid tiny embedded text inside the generated image

## Integration Rules

- Add generated images through the framework's normal image component when one exists.
- Provide meaningful `alt` text for content images; use empty alt only for truly decorative images.
- Use CSS/object-fit and art direction so the important subject remains visible on mobile and desktop.
- Do not let images replace accessible text, data, controls, or navigation.
- Do not let images outrank the operational product surface in dashboards, tools, sports/data products, or community products.
- Keep palette and crop behavior aligned with tokens and responsive breakpoints.
- Keep generated and sourced assets in the same manifest, but distinguish them with `acquisition_mode`.
- For sourced assets, include visible or documented attribution whenever `attribution_required` is true.
- Verify desktop and mobile screenshots after integration; check that images render, crop cleanly, and do not obscure text.

## Output Expectations

- List generated and/or sourced assets and their intended slots.
- Mention the Codex `image_gen` prompt basis or the sourced visual query/provider basis.
- Mention any manual review needed for licensing, attribution, realism, or content fit.
"""


def _codex_plugin_openai_yaml() -> str:
    return """display_name: Design System Harness
short_description: Apply local design-system artifacts and brand imagery inside implementation repos
default_prompt: Implement UI changes using the design-system artifacts in this repository; lead dashboard/tool/data products with operational surfaces; use Codex image_gen first for professional imagery, then license-verified sourced visual fallback when needed, without API fallback
"""


def _write_if_allowed(path: Path, content: str, force: bool, created: list[str]) -> None:
    if path.exists() and not force:
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")
    created.append(str(path))
