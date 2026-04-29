"""Preset matching engine — Phase 11-1.

Contract (PLUGIN_PLAN §8):

    raw_score(preset) = match(app_mode)*0.5
                      + match(brand_tone)*0.35
                      + tag_overlap*0.15

    bucket:
        High   — top1 raw_score ≥ 0.8 AND gap(top1 - top2) ≥ 0.15
        Medium — raw_score ≥ 0.6 or High conditions not met
        Low    — raw_score < 0.6

Top-3 are returned. If only Low results exist, callers should surface the
fallback message — the engine itself does not hide any result.

Inputs:
    MatchQuery(app_mode?, brand_tone?, color_mode?, tags[], stack?, locale?,
               free_text?)
Outputs:
    list[MatchResult(preset_id, raw_score, bucket, rationale[], missing_signals[])]

Natural-language free_text is resolved via `keywords.json` only — no LLM
calls, no external APIs. Extracted axes/tags merge with explicit fields
(explicit wins on conflict).
"""

from __future__ import annotations

import json
import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Iterable, Literal

from . import load_keywords

Bucket = Literal["High", "Medium", "Low"]

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
MATRIX_PATH = REPO_ROOT / "presets" / "matrix.json"


@dataclass
class MatchQuery:
    app_mode: str | None = None
    brand_tone: str | None = None
    color_mode: str | None = None
    tags: list[str] = field(default_factory=list)
    stack: str | None = None
    locale: str | None = None
    free_text: str | None = None


@dataclass
class MatchResult:
    preset_id: str
    raw_score: float
    bucket: Bucket
    rationale: list[str] = field(default_factory=list)
    missing_signals: list[str] = field(default_factory=list)
    app_mode: str = ""
    brand_tone: str = ""
    color_modes: list[str] = field(default_factory=list)
    tags: list[str] = field(default_factory=list)
    description: str = ""
    deprecated: bool = False
    deprecated_replacement: str | None = None

    def to_dict(self) -> dict:
        data = {
            "preset_id": self.preset_id,
            "raw_score": round(self.raw_score, 4),
            "bucket": self.bucket,
            "rationale": list(self.rationale),
            "missing_signals": list(self.missing_signals),
            "app_mode": self.app_mode,
            "brand_tone": self.brand_tone,
            "color_modes": list(self.color_modes),
            "tags": list(self.tags),
            "description": self.description,
        }
        if self.deprecated:
            data["deprecated"] = True
            if self.deprecated_replacement:
                data["deprecated_replacement"] = self.deprecated_replacement
        return data


def _load_matrix(path: Path | None = None) -> dict:
    p = path or MATRIX_PATH
    return json.loads(p.read_text(encoding="utf-8"))


def _compile_patterns(entries: Iterable[str]) -> list[re.Pattern]:
    return [re.compile(re.escape(term), re.IGNORECASE) for term in entries if term]


def extract_axes_from_text(text: str, keywords: dict | None = None) -> dict:
    """Resolve free text → {app_mode, brand_tone, color_mode, tags[]}.

    Picks the highest-hit-count match per axis. Ties are broken by first
    alphabetical id for stability. Tags accumulate every hit.
    """

    kw = keywords or load_keywords()
    lowered = text.lower() if text else ""

    def _best(axis_block: dict[str, list[str]]) -> tuple[str | None, int, list[str]]:
        best_id: str | None = None
        best_count = 0
        rationale: list[str] = []
        for axis_id in sorted(axis_block.keys()):
            terms = axis_block[axis_id]
            patterns = _compile_patterns(terms)
            hits = [term for term, pat in zip(terms, patterns) if pat.search(lowered)]
            if not hits:
                continue
            if len(hits) > best_count:
                best_count = len(hits)
                best_id = axis_id
                rationale = hits
        return best_id, best_count, rationale

    app_mode, _, app_rat = _best(kw.get("app_mode", {}))
    brand_tone, _, tone_rat = _best(kw.get("brand_tone", {}))
    color_mode, _, _ = _best(kw.get("color_mode", {}))

    tags: list[str] = []
    for tag_id in sorted(kw.get("tags", {}).keys()):
        patterns = _compile_patterns(kw["tags"][tag_id])
        if any(pat.search(lowered) for pat in patterns):
            tags.append(tag_id)

    return {
        "app_mode": app_mode,
        "brand_tone": brand_tone,
        "color_mode": color_mode,
        "tags": tags,
        "_rationale": {
            "app_mode": app_rat,
            "brand_tone": tone_rat,
        },
    }


def _effective_query(query: MatchQuery) -> tuple[MatchQuery, dict]:
    """Merge explicit MatchQuery fields with free-text extraction.

    Explicit fields always win. Tags are union-merged.
    """

    extracted: dict = {}
    rationale_from_text: dict = {}
    if query.free_text:
        extracted = extract_axes_from_text(query.free_text)
        rationale_from_text = extracted.get("_rationale", {})

    merged_tags = list(dict.fromkeys(list(query.tags) + list(extracted.get("tags") or [])))

    effective = MatchQuery(
        app_mode=query.app_mode or extracted.get("app_mode"),
        brand_tone=query.brand_tone or extracted.get("brand_tone"),
        color_mode=query.color_mode or extracted.get("color_mode"),
        tags=merged_tags,
        stack=query.stack,
        locale=query.locale,
        free_text=query.free_text,
    )
    return effective, rationale_from_text


def _bucket_for(top_score: float, second_score: float) -> Bucket:
    if top_score >= 0.8 and (top_score - second_score) >= 0.15:
        return "High"
    if top_score >= 0.6:
        return "Medium"
    return "Low"


def _score_preset(preset: dict, q: MatchQuery) -> tuple[float, list[str], list[str]]:
    """Return (raw_score, rationale, missing_signals) for one preset."""

    rationale: list[str] = []
    missing: list[str] = []

    app_match = 0.0
    if q.app_mode:
        if preset.get("app_mode") == q.app_mode:
            app_match = 1.0
            rationale.append(f"app_mode 일치: {q.app_mode}")
        else:
            rationale.append(
                f"app_mode 불일치: 요청 {q.app_mode} vs 프리셋 {preset.get('app_mode')}"
            )
    else:
        missing.append("app_mode")

    tone_match = 0.0
    if q.brand_tone:
        if preset.get("brand_tone") == q.brand_tone:
            tone_match = 1.0
            rationale.append(f"brand_tone 일치: {q.brand_tone}")
        else:
            rationale.append(
                f"brand_tone 불일치: 요청 {q.brand_tone} vs 프리셋 {preset.get('brand_tone')}"
            )
    else:
        missing.append("brand_tone")

    tag_overlap = 0.0
    preset_tags = set(preset.get("tags") or [])
    if q.tags:
        overlap = set(q.tags) & preset_tags
        if overlap:
            tag_overlap = len(overlap) / max(len(q.tags), 1)
            rationale.append(f"tag 매칭: {sorted(overlap)}")
        else:
            rationale.append(f"tag 매칭 없음 (요청 {sorted(q.tags)})")
    elif preset_tags:
        # No requested tags, but preset has tags — neutral, no penalty.
        pass

    # Color-mode is a filter, not a score contributor per PLAN §8.2.
    # If user asked for a color_mode the preset does not support, zero the whole score.
    if q.color_mode and q.color_mode != "both":
        supported = set(preset.get("color_modes") or [])
        if q.color_mode not in supported:
            rationale.append(
                f"color_mode 미지원: 요청 {q.color_mode} vs 지원 {sorted(supported)}"
            )
            return 0.0, rationale, missing
        else:
            rationale.append(f"color_mode 지원: {q.color_mode}")

    # Locale: if user asked for a specific locale, require locale_pairings entry.
    # Not a scorer — informational rationale only.
    if q.locale and q.locale != "en":
        if q.locale in (preset.get("locale_pairings") or {}):
            rationale.append(f"locale 페어링 있음: {q.locale}")
        else:
            rationale.append(f"locale 페어링 없음 ({q.locale}) — 폰트 기본값 사용")

    raw = app_match * 0.5 + tone_match * 0.35 + tag_overlap * 0.15
    return raw, rationale, missing


def match_presets(
    query: MatchQuery,
    *,
    matrix_path: Path | None = None,
    top_k: int = 3,
    include_deprecated: bool = False,
) -> list[MatchResult]:
    """Rank every preset in matrix.json against the query.

    Returns up to `top_k` results, sorted by raw_score descending. Bucket
    assignment uses the full sorted list (so top1 gap is measured against
    the true runner-up, not the K-th result).

    ``include_deprecated`` defaults to ``False`` so ``/design-start`` and the
    CLI hide retired presets. ``run_eval`` / ``validate-community-preset.py``
    pass ``True`` to keep the label space complete.
    """

    matrix = _load_matrix(matrix_path)
    presets = matrix.get("presets", [])
    if not presets:
        return []

    deprecation_info = _load_deprecation_info(matrix_path)

    if not include_deprecated and deprecation_info:
        presets = [p for p in presets if p["id"] not in deprecation_info]

    effective, _rationale_from_text = _effective_query(query)

    scored: list[tuple[float, dict, list[str], list[str]]] = []
    for preset in presets:
        raw, rationale, missing = _score_preset(preset, effective)
        scored.append((raw, preset, rationale, missing))

    tier_order = {"P0": 0, "P1": 1, "P2": 2, "P3": 3}
    scored.sort(
        key=lambda item: (
            -item[0],
            tier_order.get(item[1].get("tier", "P3"), 3),
            item[1]["id"],
        )
    )

    top_score = scored[0][0] if scored else 0.0
    second_score = scored[1][0] if len(scored) > 1 else 0.0
    top_bucket = _bucket_for(top_score, second_score)

    results: list[MatchResult] = []
    for rank, (raw, preset, rationale, missing) in enumerate(scored[:top_k]):
        if rank == 0:
            bucket: Bucket = top_bucket
        else:
            # Runners-up: Medium if ≥0.6, else Low. Never label them High.
            bucket = "Medium" if raw >= 0.6 else "Low"
        info = deprecation_info.get(preset["id"]) or {}
        if info:
            replacement = info.get("deprecated_replacement")
            note = (
                f"deprecated ({info.get('deprecation_reason') or 'no reason'})"
                + (f", 대체: {replacement}" if replacement else "")
            )
            rationale = [note, *rationale]
        results.append(
            MatchResult(
                preset_id=preset["id"],
                raw_score=raw,
                bucket=bucket,
                rationale=rationale,
                missing_signals=missing,
                app_mode=preset.get("app_mode", ""),
                brand_tone=preset.get("brand_tone", ""),
                color_modes=list(preset.get("color_modes") or []),
                tags=list(preset.get("tags") or []),
                description=preset.get("description", ""),
                deprecated=bool(info),
                deprecated_replacement=info.get("deprecated_replacement"),
            )
        )
    return results


def _load_deprecation_info(matrix_path: Path | None) -> dict[str, dict]:
    """Scan manifest.json for every preset in the matrix, collect any
    ``deprecated_at`` entries. Returns ``{preset_id: {reason, replacement}}``.
    Empty dict if nothing is deprecated (the common case).
    """

    root = (matrix_path or MATRIX_PATH).parent
    matrix = _load_matrix(matrix_path)
    info: dict[str, dict] = {}
    for preset in matrix.get("presets", []):
        preset_id = preset.get("id")
        if not preset_id:
            continue
        manifest_path = root / preset_id / "manifest.json"
        if not manifest_path.exists():
            continue
        try:
            manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            continue
        if not manifest.get("deprecated_at"):
            continue
        info[preset_id] = {
            "deprecated_at": manifest.get("deprecated_at"),
            "deprecation_reason": manifest.get("deprecation_reason"),
            "deprecated_replacement": manifest.get("deprecated_replacement"),
        }
    return info


def format_results(results: list[MatchResult], *, max_rationale: int = 4) -> str:
    """Pretty-print Top-N match results for CLI humans."""

    if not results:
        return "(매칭된 프리셋이 없습니다 — matrix.json 비어있음)"

    lines: list[str] = []
    if all(r.bucket == "Low" for r in results):
        lines.append("⚠️  정확한 매칭 없음 — 가장 가까운 대안을 제시합니다.\n")

    for rank, result in enumerate(results, start=1):
        badge = {"High": "⭐", "Medium": "◎", "Low": "△"}.get(result.bucket, "·")
        deprecated_suffix = "  🗑️ deprecated" if result.deprecated else ""
        lines.append(
            f"{rank}. {badge} {result.preset_id}  [{result.bucket}]{deprecated_suffix}  "
            f"(app_mode={result.app_mode}, brand_tone={result.brand_tone})"
        )
        if result.description:
            lines.append(f"   · {result.description}")
        if result.color_modes:
            lines.append(f"   · color_modes: {', '.join(result.color_modes)}")
        if result.tags:
            lines.append(f"   · tags: {', '.join(result.tags)}")
        for note in result.rationale[:max_rationale]:
            lines.append(f"   - {note}")
        if result.missing_signals:
            lines.append(f"   ? 미지정 신호: {', '.join(result.missing_signals)}")
        lines.append("")
    return "\n".join(lines).rstrip()
