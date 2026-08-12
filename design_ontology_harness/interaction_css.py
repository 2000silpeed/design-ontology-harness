"""Render selected interaction patterns as implementable CSS.

Selection used to end at a JSON file. Implementations then hand-wrote whatever
motion they felt like, so changing the selection changed nothing on screen. This
module closes that gap: the chosen patterns become a real stylesheet that binds
only to ``--ds-*`` tokens, and the linter can compare what was selected against
what the implementation actually uses.

Selector contract
-----------------
An element opts into a pattern with ``data-interaction`` (a space-separated
list, matched with ``~=``) and reports its state with ``data-state``::

    <li data-interaction="staged-enter" data-state="content-enter">
    <button data-interaction="determinate-bar" data-state="loading">
"""

from __future__ import annotations

from typing import Any

INTERACTIONS_BLOCK_START = "/* design-ontology:interactions:START */"
INTERACTIONS_BLOCK_END = "/* design-ontology:interactions:END */"

_DURATION_TOKENS = {80: "--ds-duration-80", 120: "--ds-duration-120", 180: "--ds-duration-180",
                    240: "--ds-duration-240", 320: "--ds-duration-320"}
_LOOP_TOKENS = {1200: "--ds-loop-fast", 1600: "--ds-loop-medium", 2400: "--ds-loop-slow"}


def pattern_slug(pattern_id: str) -> str:
    """``interaction:staged-enter`` -> ``staged-enter``."""
    return str(pattern_id).split(":", 1)[-1]


def _duration_token(duration_ms: int, kind: str) -> str:
    table = _LOOP_TOKENS if kind == "loop" else _DURATION_TOKENS
    if duration_ms in table:
        return table[duration_ms]
    # Snap to the nearest declared step rather than emitting a literal, so the
    # stylesheet can never introduce an off-scale value.
    nearest = min(table, key=lambda step: abs(step - duration_ms))
    return table[nearest]


#: Per-pattern rule bodies. ``{sel}`` is the pattern's attribute selector,
#: ``{duration}`` and ``{easing}`` are token references.
_PATTERN_CSS: dict[str, str] = {
    "interaction:immediate-swap": """
{sel} {{ transition: none; }}
""",
    "interaction:staged-enter": """
{sel} {{ opacity: 0; transform: translateY(4px); }}
{sel}[data-state~="content-enter"],
{sel}[data-state~="filtered"] {{
  opacity: 1;
  transform: none;
  transition: opacity {duration} {easing}, transform {duration} {easing};
}}
{sel}:nth-child(2) {{ transition-delay: var(--ds-duration-80); }}
{sel}:nth-child(3) {{ transition-delay: var(--ds-duration-120); }}
{sel}:nth-child(n+4) {{ transition-delay: var(--ds-duration-180); }}
""",
    "interaction:inline-expand": """
{sel} {{ overflow: clip; }}
{sel} > [data-expandable] {{ opacity: 0; transform: translateY(-2px); }}
{sel}[data-state~="open"] > [data-expandable],
{sel}[data-state~="focused"] > [data-expandable] {{
  opacity: 1;
  transform: none;
  transition: opacity {duration} {easing}, transform {duration} {easing};
}}
""",
    "interaction:result-reveal": """
{sel} {{ opacity: 0; }}
{sel}[data-state~="content-enter"] {{
  opacity: 1;
  transition: opacity {duration} {easing};
}}
""",
    "interaction:weight-shift": """
{sel} {{
  font-weight: 450;
  color: var(--ds-color-ink-muted);
  transition: color {duration} {easing};
}}
{sel}[data-state~="selected"],
{sel}[data-state~="current"] {{ font-weight: 650; color: var(--ds-color-ink); }}
""",
    "interaction:surface-lift": """
{sel} {{
  box-shadow: none;
  transition: box-shadow {duration} {easing}, border-color {duration} {easing};
}}
{sel}[data-state~="selected"],
{sel}[data-state~="attention"] {{
  border-color: var(--ds-color-border-strong);
  box-shadow: var(--ds-elevation-lg);
}}
""",
    "interaction:attention-border": """
{sel} {{
  border-color: var(--ds-color-border);
  transition: border-color {duration} {easing};
}}
{sel}[data-state~="attention"],
{sel}[data-state~="selected"] {{ border-color: var(--ds-color-accent); }}
""",
    "interaction:determinate-bar": """
{sel} {{ overflow: hidden; background: var(--ds-color-surface-muted); }}
{sel} > [data-progress-fill] {{
  display: block;
  block-size: 100%;
  inline-size: 100%;
  transform: scaleX(var(--ds-progress-value, 0));
  transform-origin: left center;
  background: var(--ds-color-accent);
  transition: transform {duration} {easing};
}}
""",
    "interaction:skeleton-placeholder": """
{sel} {{
  background: linear-gradient(
    90deg,
    var(--ds-color-surface-muted) 0%,
    var(--ds-color-surface) 50%,
    var(--ds-color-surface-muted) 100%
  );
  background-size: 200% 100%;
  animation: ds-skeleton-sweep {duration} {easing} infinite;
}}
@keyframes ds-skeleton-sweep {{
  from {{ background-position: 200% 0; }}
  to {{ background-position: -200% 0; }}
}}
""",
    "interaction:dot-progress": """
{sel} {{ display: inline-flex; gap: var(--ds-space-2); }}
{sel} > [data-dot] {{
  opacity: .3;
  animation: ds-dot-progress {duration} {easing} infinite;
}}
{sel} > [data-dot]:nth-child(2) {{ animation-delay: var(--ds-duration-120); }}
{sel} > [data-dot]:nth-child(3) {{ animation-delay: var(--ds-duration-240); }}
@keyframes ds-dot-progress {{
  0%, 100% {{ opacity: .3; }}
  50% {{ opacity: 1; }}
}}
""",
    "interaction:context-crossfade": """
{sel} {{ transition: opacity {duration} {easing}; }}
{sel}[data-state~="exiting"] {{ opacity: 0; }}
{sel}[data-state~="current"],
{sel}[data-state~="filtered"] {{ opacity: 1; }}
""",
    "interaction:anchored-shift": """
{sel} {{ position: relative; }}
{sel} > [data-anchor] {{
  position: absolute;
  inset-block-end: 0;
  transition: transform {duration} {easing};
}}
""",
    "interaction:showcase-morphology": """
{sel} {{ opacity: 0; transform: translateY(8px); }}
{sel}[data-state~="content-enter"],
{sel}[data-state~="current"] {{
  opacity: 1;
  transform: none;
  transition: opacity {duration} {easing}, transform {duration} {easing};
}}
""",
}

#: How each reduced-motion strategy neutralises a pattern.
_REDUCED_CSS = {
    "static": "{sel}, {sel} > * {{ animation: none; transition: none; }}",
    "opacity-only": (
        "{sel}, {sel} > * {{ transform: none; animation: none; }}\n"
        "{sel} {{ transition-property: opacity; }}"
    ),
    "skip": "{sel}, {sel} > * {{ opacity: 1; transform: none; animation: none; transition: none; }}",
}

#: Patterns whose animation lives on a descendant need a selector-exact
#: fallback; a wildcard child selector does not count as a match.
_PATTERN_REDUCED_CSS: dict[str, str] = {
    "interaction:skeleton-placeholder": (
        "{sel} {{ animation: none; background: var(--ds-color-surface-muted); }}"
    ),
    "interaction:dot-progress": (
        "{sel} > [data-dot] {{ animation: none; opacity: 1; }}\n"
        "{sel} > [data-dot]:nth-child(2),\n"
        "{sel} > [data-dot]:nth-child(3) {{ animation-delay: 0s; }}"
    ),
}


def build_interactions_css(selection: dict[str, Any], project: str) -> str:
    """Render the selected patterns as a token-bound stylesheet."""

    selected = selection.get("selected") or []
    lines = [
        INTERACTIONS_BLOCK_START,
        f"/* project: {project} — generated by design-ontology emit-tokens */",
        "/* 선택된 인터랙션 패턴만 여기 있습니다. 구현은 이 계약을 벗어나지 않습니다. */",
        "/* 요소 사용법: data-interaction=\"<slug>\" + data-state=\"<state>\" */",
    ]
    if not selected:
        lines.append("/* 선택된 패턴 없음 — 이 제품 표면에는 모션 계약이 없습니다. */")
        lines.append(INTERACTIONS_BLOCK_END)
        return "\n".join(lines) + "\n"

    reduced_blocks: list[str] = []
    unrenderable: list[str] = []
    for item in selected:
        pattern_id = item["id"]
        template = _PATTERN_CSS.get(pattern_id)
        if template is None:
            # Never drop a selection silently: a pattern with no rule body means
            # the selection and the stylesheet have drifted apart, which is the
            # exact failure this file exists to prevent.
            unrenderable.append(pattern_id)
            continue
        slug = pattern_slug(pattern_id)
        selector = f'[data-interaction~="{slug}"]'
        duration = f'var({_duration_token(int(item.get("duration_ms", 180)), item.get("motion_kind", "transition"))})'
        easing = f'var(--ds-ease-{item.get("easing", "standard")})'

        lines.append("")
        lines.append(f'/* {item.get("axis", "?")} · {pattern_id} — {item.get("rationale", "")} */')
        lines.append(
            template.format(sel=selector, duration=duration, easing=easing).strip()
        )

        strategy = item.get("reduced_motion", "static")
        reduced_template = _PATTERN_REDUCED_CSS.get(
            pattern_id, _REDUCED_CSS.get(strategy, _REDUCED_CSS["static"])
        )
        reduced_blocks.append(reduced_template.format(sel=selector))

    if reduced_blocks:
        lines.append("")
        lines.append("@media (prefers-reduced-motion: reduce) {")
        for block in reduced_blocks:
            for row in block.splitlines():
                lines.append(f"  {row}")
        lines.append("}")

    if unrenderable:
        lines.append("")
        lines.append("/* !! 선택됐지만 렌더링 규칙이 없는 패턴:")
        for pattern_id in unrenderable:
            lines.append(f"   - {pattern_id}")
        lines.append(
            "   blueprint를 다시 합성하거나 interaction_css.py에 규칙을 추가하세요. */"
        )

    lines.append(INTERACTIONS_BLOCK_END)
    return "\n".join(lines) + "\n"


def selected_pattern_slugs(selection: dict[str, Any]) -> set[str]:
    return {pattern_slug(item["id"]) for item in selection.get("selected") or []}


def all_pattern_slugs() -> set[str]:
    return {pattern_slug(pattern_id) for pattern_id in _PATTERN_CSS}


def build_interaction_contract_md(selection: dict[str, Any], project: str) -> str:
    """Render the human-facing contract implementers read before writing UI."""

    selected = selection.get("selected") or []
    rows = [
        f"# {project} — 인터랙션 계약",
        "",
        "`design-system/interactions.css`가 이 계약의 실행 가능한 형태입니다.",
        "선택되지 않은 패턴을 구현하거나 여기 없는 모션을 추가하면 린터가 막습니다.",
        "",
        f"- 선택 방식: `{selection.get('selection_mode', 'unknown')}`",
        f"- 변동 시드: `{selection.get('variation_seed')}`",
        "",
    ]
    if not selected:
        rows.append("선택된 패턴이 없습니다. 이 표면은 모션 없이 구현합니다.")
        return "\n".join(rows) + "\n"

    rows.append("## 선택된 패턴")
    rows.append("")
    for item in selected:
        slug = pattern_slug(item["id"])
        rows.append(f"### {item.get('axis')} · `{slug}`")
        rows.append("")
        rows.append(item.get("rationale", ""))
        rows.append("")
        rows.append(f"- 마크업: `data-interaction=\"{slug}\"`")
        rows.append(
            f"- 모션: {item.get('duration_ms')}ms · `{item.get('easing')}` · "
            f"reduced-motion `{item.get('reduced_motion')}`"
        )
        rows.append(f"- 적용 역할: {', '.join(item.get('covered_roles') or []) or '—'}")
        rows.append(f"- 근거 팩: `{item.get('pack_id')}`")
        guardrails = item.get("guardrails") or []
        if guardrails:
            rows.append("- 가드레일:")
            rows.extend(f"  - {rule}" for rule in guardrails)
        rows.append("")

    considered = selection.get("candidates_considered") or []
    losing = [item for item in considered if item["id"] not in {row["id"] for row in selected}]
    if losing:
        rows.append("## 검토했지만 선택하지 않은 후보")
        rows.append("")
        for item in losing:
            rows.append(
                f"- `{pattern_slug(item['id'])}` ({item.get('axis')}, 점수 {item.get('score')})"
            )
        rows.append("")

    return "\n".join(rows) + "\n"
