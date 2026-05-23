from __future__ import annotations

import json
import hashlib
import re
from copy import deepcopy
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any

from .utils import ensure_dir, write_json


ONTOLOGY_SCHEMA_VERSION = "aesthetic-evaluation-ontology/v1"
LOOP_SCHEMA_VERSION = "aesthetic-self-improvement-loop/v1"
DEFAULT_THRESHOLD = 0.82
DEFAULT_MIN_DIMENSION_SCORE = 0.70
DEFAULT_MAX_ITERATIONS = 3
AESTHETIC_ONTOLOGY_RELATIVE_PATH = Path("blueprint") / "aesthetic_ontology.json"
AESTHETIC_CANDIDATE_TEMPLATE_RELATIVE_PATH = Path("aesthetic") / "candidate_template.json"
AESTHETIC_LOOP_POLICY_RELATIVE_PATH = Path("aesthetic") / "loop_policy.json"
AESTHETIC_LATEST_REPORT_RELATIVE_PATH = Path("aesthetic") / "latest_loop_report.json"


DEFAULT_DIMENSIONS = [
    {
        "id": "visual_harmony",
        "label": "Visual harmony",
        "weight": 0.24,
        "description": "How coherently color, type, spacing, and composition work together.",
        "metrics": [
            "color_harmony",
            "spacing_consistency",
            "typography_balance",
            "composition_order",
        ],
    },
    {
        "id": "clarity",
        "label": "Clarity",
        "weight": 0.20,
        "description": "How quickly the intended hierarchy, action, and information structure can be read.",
        "metrics": [
            "hierarchy_clarity",
            "contrast_legibility",
            "content_density_control",
            "task_focus",
        ],
    },
    {
        "id": "brand_fit",
        "label": "Brand fit",
        "weight": 0.18,
        "description": "How well the candidate expresses the intended brand posture and avoids anti-keywords.",
        "metrics": [
            "keyword_alignment",
            "tone_alignment",
            "domain_fit",
            "anti_keyword_avoidance",
        ],
    },
    {
        "id": "emotional_appeal",
        "label": "Emotional appeal",
        "weight": 0.14,
        "description": "How desirable, confident, and affectively appropriate the surface feels.",
        "metrics": [
            "desirability",
            "confidence_signal",
            "warmth_or_energy",
        ],
    },
    {
        "id": "craft_quality",
        "label": "Craft quality",
        "weight": 0.14,
        "description": "How polished and implementation-ready the candidate is across fit, tokens, and affordances.",
        "metrics": [
            "responsive_fit",
            "token_binding",
            "accessibility_baseline",
            "interaction_affordance",
            "asset_completeness",
        ],
    },
    {
        "id": "novelty",
        "label": "Novelty",
        "weight": 0.10,
        "description": "How distinctive the design is without breaking its product and brand constraints.",
        "metrics": [
            "distinctiveness",
            "reference_transformation",
            "memorability",
        ],
    },
]


DEFAULT_METRICS = {
    "color_harmony": {
        "label": "Color harmony",
        "improvement": "Tighten the palette around one primary accent, one neutral surface ladder, and explicit semantic roles.",
        "expected_lift": 0.08,
    },
    "spacing_consistency": {
        "label": "Spacing consistency",
        "improvement": "Normalize page rhythm with shared spacing steps for section, cluster, and control gaps.",
        "expected_lift": 0.07,
    },
    "typography_balance": {
        "label": "Typography balance",
        "improvement": "Rebalance type hierarchy so headings, body, captions, and controls use distinct but restrained roles.",
        "expected_lift": 0.07,
    },
    "composition_order": {
        "label": "Composition order",
        "improvement": "Strengthen alignment, focal sequence, and proportional grouping before adding more decoration.",
        "expected_lift": 0.08,
    },
    "hierarchy_clarity": {
        "label": "Hierarchy clarity",
        "improvement": "Make the primary state, primary action, and next-best secondary action visible in the first scan.",
        "expected_lift": 0.09,
    },
    "contrast_legibility": {
        "label": "Contrast and legibility",
        "improvement": "Raise text/background and control/border contrast while preserving the selected token roles.",
        "expected_lift": 0.08,
    },
    "content_density_control": {
        "label": "Content density control",
        "improvement": "Reduce competing modules or group dense content into scannable rows, tables, rails, or panels.",
        "expected_lift": 0.07,
    },
    "task_focus": {
        "label": "Task focus",
        "improvement": "Move decorative or pitch-like content below the operational surface that supports the user's main task.",
        "expected_lift": 0.08,
    },
    "keyword_alignment": {
        "label": "Keyword alignment",
        "improvement": "Map the strongest brand keywords to visible choices in layout, tone, density, and component emphasis.",
        "expected_lift": 0.08,
    },
    "tone_alignment": {
        "label": "Tone alignment",
        "improvement": "Adjust copy weight, control styling, and visual temperature to match the intended voice.",
        "expected_lift": 0.06,
    },
    "domain_fit": {
        "label": "Domain fit",
        "improvement": "Add domain-native structures such as tables, maps, media, timelines, inspectors, or product objects where relevant.",
        "expected_lift": 0.08,
    },
    "anti_keyword_avoidance": {
        "label": "Anti-keyword avoidance",
        "improvement": "Remove visual tropes that match the brand profile's anti-keywords before polishing details.",
        "expected_lift": 0.06,
    },
    "desirability": {
        "label": "Desirability",
        "improvement": "Give the primary surface a more intentional visual reward: stronger imagery, tactile controls, or clearer payoff.",
        "expected_lift": 0.07,
    },
    "confidence_signal": {
        "label": "Confidence signal",
        "improvement": "Add evidence, provenance, precision, or stable UI states that make the surface feel trustworthy.",
        "expected_lift": 0.07,
    },
    "warmth_or_energy": {
        "label": "Warmth or energy",
        "improvement": "Tune motion, image choice, accent placement, or microcopy energy to the target audience.",
        "expected_lift": 0.06,
    },
    "responsive_fit": {
        "label": "Responsive fit",
        "improvement": "Verify mobile and desktop fit, then fix overflow, clipped labels, and unstable control sizing.",
        "expected_lift": 0.08,
    },
    "token_binding": {
        "label": "Token binding",
        "improvement": "Replace local visual constants with design-system tokens and keep semantic roles consistent.",
        "expected_lift": 0.06,
    },
    "accessibility_baseline": {
        "label": "Accessibility baseline",
        "improvement": "Check contrast, focus states, labels, and target sizes as part of visual polish, not after it.",
        "expected_lift": 0.07,
    },
    "interaction_affordance": {
        "label": "Interaction affordance",
        "improvement": "Make controls, filters, state chips, and navigation visually legible with icons, state, and hit-area clarity.",
        "expected_lift": 0.07,
    },
    "asset_completeness": {
        "label": "Asset completeness",
        "improvement": "Use concrete product, place, object, identity, or content assets where the domain expects visual substance.",
        "expected_lift": 0.08,
    },
    "distinctiveness": {
        "label": "Distinctiveness",
        "improvement": "Introduce one memorable composition or interaction pattern while keeping the rest of the system restrained.",
        "expected_lift": 0.06,
    },
    "reference_transformation": {
        "label": "Reference transformation",
        "improvement": "Absorb reference morphology without copying palette, copy, IA, or protected asset choices.",
        "expected_lift": 0.06,
    },
    "memorability": {
        "label": "Memorability",
        "improvement": "Create a recognizable signature in the first viewport through layout, identity asset, or product-native visual.",
        "expected_lift": 0.06,
    },
}

RESEARCH_BASIS = [
    {
        "id": "visawi",
        "label": "VisAWI",
        "construct": "perceived website visual aesthetics",
        "operational_use": "Map simplicity, diversity, colorfulness, and craftsmanship into visual system coherence metrics.",
        "source_url": "https://www.sciencedirect.com/science/article/pii/S1071581910000777",
    },
    {
        "id": "apid",
        "label": "APiD",
        "construct": "aesthetic pleasure in designed artifacts",
        "operational_use": "Keep a direct pleasure/desirability layer instead of only formal pixel metrics.",
        "source_url": "https://opus.lib.uts.edu.au/handle/10453/81276",
    },
    {
        "id": "beauvis",
        "label": "BeauVis",
        "construct": "aesthetic pleasure of visual representations",
        "operational_use": "Treat scores as comparative, context-bound judgments rather than universal beauty values.",
        "source_url": "https://arxiv.org/abs/2207.14147",
    },
    {
        "id": "aesthemos",
        "label": "AESTHEMOS",
        "construct": "aesthetic emotions",
        "operational_use": "Translate brand tone and target affect into measurable emotional-response proxies.",
        "source_url": "https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0178899",
    },
    {
        "id": "kansei",
        "label": "Kansei / semantic differential",
        "construct": "design element to impression mapping",
        "operational_use": "Use brand keywords and anti-keywords as semantic impression targets and boundaries.",
        "source_url": "https://www.mdpi.com/2073-8994/12/8/1340",
    },
]


@dataclass(frozen=True)
class MetricScore:
    metric_id: str
    label: str
    raw_value: float | None
    score: float
    present: bool

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class DimensionScore:
    dimension_id: str
    label: str
    weight: float
    score: float
    metric_scores: list[MetricScore] = field(default_factory=list)
    missing_metrics: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        data = asdict(self)
        data["metric_scores"] = [metric.to_dict() for metric in self.metric_scores]
        return data


@dataclass(frozen=True)
class AestheticAction:
    action_id: str
    dimension_id: str
    metric_id: str
    priority: int
    expected_lift: float
    instruction: str

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class AestheticEvaluation:
    iteration_id: str
    design_id: str
    score: float
    score_100: float
    threshold: float
    min_dimension_score: float
    passed: bool
    status: str
    coverage_ratio: float
    dimension_scores: list[DimensionScore]
    missing_metrics: list[str]
    actions: list[AestheticAction]

    def to_dict(self) -> dict[str, Any]:
        data = asdict(self)
        data["dimension_scores"] = [dimension.to_dict() for dimension in self.dimension_scores]
        data["actions"] = [action.to_dict() for action in self.actions]
        return data


def load_json(path: Path) -> dict[str, Any]:
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError(f"JSON root must be an object: {path}")
    return data


def build_aesthetic_ontology(
    brand_profile: dict[str, Any] | None = None,
    custom_ontology: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Build the scoring ontology used by the aesthetic self-improvement gate."""

    if custom_ontology:
        ontology = deepcopy(custom_ontology)
    else:
        ontology = {
            "schema_version": ONTOLOGY_SCHEMA_VERSION,
            "dimensions": deepcopy(DEFAULT_DIMENSIONS),
            "metrics": deepcopy(DEFAULT_METRICS),
            "relations": [
                {"source": "DesignCandidate", "relation": "evaluated_by", "target": "AestheticDimension"},
                {"source": "AestheticDimension", "relation": "measured_by", "target": "AestheticMetric"},
                {"source": "AestheticMetric", "relation": "improved_by", "target": "ImprovementAction"},
                {"source": "AestheticEvaluation", "relation": "gates", "target": "Execution"},
            ],
        }

    brand_profile = brand_profile or {}
    brand_contract = build_brand_aesthetic_contract(brand_profile)
    if brand_contract["dimensions"]:
        ontology.setdefault("dimensions", [])
        ontology.setdefault("metrics", {})
        ontology["dimensions"].extend(deepcopy(brand_contract["dimensions"]))
        ontology["metrics"].update(deepcopy(brand_contract["metrics"]))
    ontology.setdefault("schema_version", ONTOLOGY_SCHEMA_VERSION)
    ontology["context"] = {
        "brand_name": brand_profile.get("brand_name"),
        "system_name": brand_profile.get("system_name"),
        "product_summary": brand_profile.get("product_summary"),
        "audiences": list(brand_profile.get("audiences", []) or []),
        "brand_keywords": list(brand_profile.get("brand_keywords", []) or []),
        "anti_keywords": list(brand_profile.get("anti_keywords", []) or []),
        "tone_of_voice": list(brand_profile.get("tone_of_voice", []) or []),
        "product_primitives": list(brand_profile.get("product_primitives", []) or []),
    }
    ontology["brand_aesthetic_contract"] = brand_contract
    ontology["interpretation_rule"] = (
        "Scores represent observed or reviewed response proxies in a declared context; "
        "they are not universal beauty claims."
    )
    return ontology


def build_brand_aesthetic_contract(brand_profile: dict[str, Any] | None) -> dict[str, Any]:
    brand_profile = brand_profile or {}
    metrics: dict[str, dict[str, Any]] = {}
    dimensions: list[dict[str, Any]] = []

    brand_terms = _terms_from_profile(brand_profile, "brand_keywords")[:8]
    tone_terms = _terms_from_profile(brand_profile, "tone_of_voice")[:5]
    semantic_metric_ids = []
    for term in brand_terms:
        metric_id = _brand_metric_id("brand_keyword", term)
        metrics[metric_id] = {
            "label": f"Expresses brand keyword: {term}",
            "improvement": f"Make '{term}' visible through palette, density, component rhythm, imagery, and microcopy choices.",
            "expected_lift": 0.07,
            "source": "brand_profile.brand_keywords",
            "target_value": term,
        }
        semantic_metric_ids.append(metric_id)
    for term in tone_terms:
        metric_id = _brand_metric_id("brand_tone", term)
        metrics[metric_id] = {
            "label": f"Expresses tone of voice: {term}",
            "improvement": f"Tune hierarchy, copy weight, and interaction tone so the surface feels '{term}'.",
            "expected_lift": 0.06,
            "source": "brand_profile.tone_of_voice",
            "target_value": term,
        }
        semantic_metric_ids.append(metric_id)
    if semantic_metric_ids:
        dimensions.append(
            {
                "id": "brand_semantic_fit",
                "label": "Brand semantic fit",
                "weight": 0.22,
                "description": "Kansei-style alignment between brand/tone words and the perceived design impression.",
                "metrics": semantic_metric_ids,
                "research_basis": ["kansei", "aesthemos"],
            }
        )

    anti_terms = _terms_from_profile(brand_profile, "anti_keywords")[:8]
    visual_reference = brand_profile.get("visual_reference") or {}
    avoid_terms = _normalize_text_list(visual_reference.get("avoid_patterns"))[:6]
    boundary_metric_ids = []
    for term in anti_terms:
        metric_id = _brand_metric_id("anti_keyword", term)
        metrics[metric_id] = {
            "label": f"Avoids anti-keyword: {term}",
            "improvement": f"Remove cues that make the product read as '{term}'.",
            "expected_lift": 0.07,
            "source": "brand_profile.anti_keywords",
            "target_value": term,
        }
        boundary_metric_ids.append(metric_id)
    for term in avoid_terms:
        metric_id = _brand_metric_id("avoid_pattern", term)
        metrics[metric_id] = {
            "label": f"Avoids visual pattern: {term}",
            "improvement": f"Replace '{term}' with brand-owned morphology and token-governed visual choices.",
            "expected_lift": 0.07,
            "source": "brand_profile.visual_reference.avoid_patterns",
            "target_value": term,
        }
        boundary_metric_ids.append(metric_id)
    if boundary_metric_ids:
        dimensions.append(
            {
                "id": "brand_boundary_fit",
                "label": "Brand boundary fit",
                "weight": 0.16,
                "description": "How well the design avoids explicitly forbidden brand impressions and visual tropes.",
                "metrics": boundary_metric_ids,
                "research_basis": ["kansei"],
            }
        )

    primitive_terms = _terms_from_profile(brand_profile, "product_primitives")[:10]
    must_include_terms = _normalize_text_list(visual_reference.get("must_include"))[:6]
    product_metric_ids = []
    for term in primitive_terms:
        metric_id = _brand_metric_id("product_primitive", term)
        metrics[metric_id] = {
            "label": f"Embodies product primitive: {term}",
            "improvement": f"Represent '{term}' as a first-class product surface, not as generic decoration.",
            "expected_lift": 0.08,
            "source": "brand_profile.product_primitives",
            "target_value": term,
        }
        product_metric_ids.append(metric_id)
    for term in must_include_terms:
        metric_id = _brand_metric_id("must_include", term)
        metrics[metric_id] = {
            "label": f"Includes required visual/system signal: {term}",
            "improvement": f"Make '{term}' visible and scannable in the main workflow.",
            "expected_lift": 0.08,
            "source": "brand_profile.visual_reference.must_include",
            "target_value": term,
        }
        product_metric_ids.append(metric_id)
    if product_metric_ids:
        dimensions.append(
            {
                "id": "product_ontology_fit",
                "label": "Product ontology fit",
                "weight": 0.22,
                "description": "How clearly product primitives and ontology-required signals appear in the design.",
                "metrics": product_metric_ids,
                "research_basis": ["beauvis", "kansei"],
            }
        )

    audience_terms = _terms_from_profile(brand_profile, "audiences")[:5]
    accessibility_terms = _terms_from_profile(brand_profile, "accessibility_targets")[:5]
    context_metric_ids = []
    for term in audience_terms:
        metric_id = _brand_metric_id("audience_need", term)
        metrics[metric_id] = {
            "label": f"Fits audience context: {term}",
            "improvement": f"Adjust density, language, workflow order, and controls for '{term}'.",
            "expected_lift": 0.06,
            "source": "brand_profile.audiences",
            "target_value": term,
        }
        context_metric_ids.append(metric_id)
    for term in accessibility_terms:
        metric_id = _brand_metric_id("accessibility_target", term)
        metrics[metric_id] = {
            "label": f"Supports accessibility target: {term}",
            "improvement": f"Verify '{term}' with contrast, sizing, focus, motion, and alternate-view checks.",
            "expected_lift": 0.07,
            "source": "brand_profile.accessibility_targets",
            "target_value": term,
        }
        context_metric_ids.append(metric_id)
    if context_metric_ids:
        dimensions.append(
            {
                "id": "audience_context_fit",
                "label": "Audience context fit",
                "weight": 0.12,
                "description": "How well the design serves declared users, platforms, and accessibility floors.",
                "metrics": context_metric_ids,
                "research_basis": ["visawi", "aesthemos"],
            }
        )

    return {
        "schema_version": "brand-aesthetic-contract/v1",
        "brand_name": brand_profile.get("brand_name"),
        "system_name": brand_profile.get("system_name"),
        "research_basis": RESEARCH_BASIS,
        "dimensions": dimensions,
        "metrics": metrics,
        "rule": (
            "Brand-owned aesthetic quality is evaluated as fit to declared semantic targets, "
            "explicit boundaries, product ontology, audience context, and visual craft."
        ),
    }


def build_candidate_template(
    brand_profile: dict[str, Any] | None,
    ontology: dict[str, Any],
    *,
    design_id: str | None = None,
    score_scale: int = 10,
) -> dict[str, Any]:
    brand_profile = brand_profile or {}
    resolved_design_id = (
        design_id
        or brand_profile.get("system_name")
        or brand_profile.get("brand_name")
        or "design-candidate"
    )
    metric_ids = [
        metric_id
        for dimension in ontology.get("dimensions", [])
        for metric_id in dimension.get("metrics", [])
        if isinstance(metric_id, str)
    ]
    metrics_catalog = ontology.get("metrics", {}) or {}
    return {
        "schema_version": "aesthetic-candidate/v1",
        "design_id": resolved_design_id,
        "score_scale": score_scale,
        "measurement_protocol": {
            "recommended_panel": "3+ reviewers or one structured AI/human review pass with evidence notes",
            "rating_method": "Likert-style 1..10 score per metric; 10 means excellent fit for the declared context.",
            "evidence_rule": "Attach screenshot paths, reviewer notes, or automated checks before treating scores as final.",
        },
        "metrics": {metric_id: None for metric_id in metric_ids},
        "metric_guidance": {
            metric_id: {
                "label": (metrics_catalog.get(metric_id) or {}).get("label", metric_id),
                "improvement": (metrics_catalog.get(metric_id) or {}).get("improvement"),
            }
            for metric_id in metric_ids
        },
        "iterations": [],
    }


def build_loop_policy(
    *,
    threshold: float = DEFAULT_THRESHOLD,
    min_dimension_score: float = DEFAULT_MIN_DIMENSION_SCORE,
    max_iterations: int = DEFAULT_MAX_ITERATIONS,
) -> dict[str, Any]:
    return {
        "schema_version": LOOP_SCHEMA_VERSION,
        "gate": {
            "ready_to_execute_requires": [
                f"overall_score >= {threshold}",
                f"every_dimension_score >= {min_dimension_score}",
            ],
            "threshold": threshold,
            "min_dimension_score": min_dimension_score,
            "max_iterations": max_iterations,
            "blocked_exit_code": 1,
        },
        "loop": [
            "score current candidate against aesthetic_ontology.json",
            "if blocked, apply next_iteration_brief actions to a revised candidate",
            "append the revised measurement to candidate.iterations",
            "rerun aesthetic-loop until the gate opens or max_iterations is exhausted",
        ],
    }


def write_aesthetic_project_artifacts(
    output_dir: Path,
    brand_profile: dict[str, Any],
    *,
    ontology: dict[str, Any] | None = None,
    threshold: float = DEFAULT_THRESHOLD,
    min_dimension_score: float = DEFAULT_MIN_DIMENSION_SCORE,
    max_iterations: int = DEFAULT_MAX_ITERATIONS,
) -> dict[str, str]:
    ontology = ontology or build_aesthetic_ontology(brand_profile)
    ontology_path = output_dir / AESTHETIC_ONTOLOGY_RELATIVE_PATH
    template_path = output_dir / AESTHETIC_CANDIDATE_TEMPLATE_RELATIVE_PATH
    policy_path = output_dir / AESTHETIC_LOOP_POLICY_RELATIVE_PATH

    ensure_dir(ontology_path.parent)
    ensure_dir(template_path.parent)
    write_json(ontology_path, ontology)
    write_json(template_path, build_candidate_template(brand_profile, ontology))
    write_json(
        policy_path,
        build_loop_policy(
            threshold=threshold,
            min_dimension_score=min_dimension_score,
            max_iterations=max_iterations,
        ),
    )
    return {
        "ontology_path": str(ontology_path),
        "candidate_template_path": str(template_path),
        "loop_policy_path": str(policy_path),
    }


def evaluate_candidate(
    candidate: dict[str, Any],
    ontology: dict[str, Any],
    *,
    threshold: float = DEFAULT_THRESHOLD,
    min_dimension_score: float = DEFAULT_MIN_DIMENSION_SCORE,
    iteration_index: int = 1,
) -> AestheticEvaluation:
    design_id = str(candidate.get("design_id") or ontology.get("context", {}).get("brand_name") or "design-candidate")
    iteration_id = str(candidate.get("iteration_id") or candidate.get("id") or f"iteration-{iteration_index}")
    score_scale = _score_scale(candidate)
    metrics = _candidate_metrics(candidate)
    dimension_overrides = _candidate_dimension_scores(candidate)
    metric_catalog = ontology.get("metrics", {})

    dimension_scores: list[DimensionScore] = []
    total_weight = 0.0
    weighted_score = 0.0
    present_metric_count = 0
    expected_metric_count = 0
    missing_metrics: list[str] = []

    for raw_dimension in ontology.get("dimensions", []):
        dimension = dict(raw_dimension)
        dimension_id = str(dimension.get("id") or "")
        if not dimension_id:
            continue
        label = str(dimension.get("label") or dimension_id)
        weight = float(dimension.get("weight") or 0.0)
        metric_ids = [str(metric_id) for metric_id in dimension.get("metrics", [])]
        expected_metric_count += len(metric_ids)

        metric_scores: list[MetricScore] = []
        present_scores: list[float] = []
        dimension_missing: list[str] = []
        for metric_id in metric_ids:
            raw_value = _as_number(metrics.get(metric_id))
            present = raw_value is not None
            metric_score = _normalize_score(raw_value, score_scale) if present else 0.0
            label = str((metric_catalog.get(metric_id) or {}).get("label") or metric_id)
            metric_scores.append(
                MetricScore(
                    metric_id=metric_id,
                    label=label,
                    raw_value=raw_value,
                    score=metric_score,
                    present=present,
                )
            )
            if present:
                present_metric_count += 1
                present_scores.append(metric_score)
            else:
                dimension_missing.append(metric_id)
                missing_metrics.append(metric_id)

        override_value = _as_number(dimension_overrides.get(dimension_id))
        if override_value is not None:
            dimension_score = _normalize_score(override_value, score_scale)
        elif present_scores:
            dimension_score = sum(present_scores) / len(present_scores)
        else:
            dimension_score = 0.0

        dimension_scores.append(
            DimensionScore(
                dimension_id=dimension_id,
                label=str(dimension.get("label") or dimension_id),
                weight=weight,
                score=dimension_score,
                metric_scores=metric_scores,
                missing_metrics=dimension_missing,
            )
        )
        total_weight += weight
        weighted_score += dimension_score * weight

    final_score = weighted_score / total_weight if total_weight else 0.0
    coverage_ratio = present_metric_count / expected_metric_count if expected_metric_count else 1.0
    weak_dimensions = [dimension for dimension in dimension_scores if dimension.score < min_dimension_score]
    passed = final_score >= threshold and not weak_dimensions
    status = "passed" if passed else "needs_revision"
    actions = recommend_actions(
        dimension_scores,
        ontology,
        min_dimension_score=min_dimension_score,
        target_score=max(min_dimension_score, threshold),
    )

    return AestheticEvaluation(
        iteration_id=iteration_id,
        design_id=design_id,
        score=round(final_score, 4),
        score_100=round(final_score * 100, 2),
        threshold=threshold,
        min_dimension_score=min_dimension_score,
        passed=passed,
        status=status,
        coverage_ratio=round(coverage_ratio, 4),
        dimension_scores=dimension_scores,
        missing_metrics=missing_metrics,
        actions=actions,
    )


def recommend_actions(
    dimension_scores: list[DimensionScore],
    ontology: dict[str, Any],
    *,
    min_dimension_score: float = DEFAULT_MIN_DIMENSION_SCORE,
    target_score: float | None = None,
    max_actions: int = 6,
) -> list[AestheticAction]:
    metrics = ontology.get("metrics", {})
    action_target = min(max(target_score or min_dimension_score, min_dimension_score), 1.0)
    candidates: list[tuple[float, str, str, str, float]] = []
    for dimension in dimension_scores:
        dimension_deficit = max(action_target - dimension.score, 0.0)
        for metric in dimension.metric_scores:
            metric_deficit = max(action_target - metric.score, 0.0)
            if not metric.present:
                metric_deficit = max(metric_deficit, 0.2)
            if dimension_deficit <= 0 and metric_deficit <= 0:
                continue
            metric_info = metrics.get(metric.metric_id) or {}
            expected_lift = float(metric_info.get("expected_lift") or 0.05)
            instruction = str(metric_info.get("improvement") or f"Improve {metric.metric_id}.")
            priority_score = dimension_deficit + metric_deficit + expected_lift
            candidates.append(
                (
                    priority_score,
                    dimension.dimension_id,
                    metric.metric_id,
                    instruction,
                    expected_lift,
                )
            )

    candidates.sort(key=lambda item: (-item[0], item[1], item[2]))
    actions: list[AestheticAction] = []
    seen_dimensions: dict[str, int] = {}
    for _, dimension_id, metric_id, instruction, expected_lift in candidates:
        if seen_dimensions.get(dimension_id, 0) >= 2:
            continue
        action_id = f"{dimension_id}:{metric_id}"
        actions.append(
            AestheticAction(
                action_id=action_id,
                dimension_id=dimension_id,
                metric_id=metric_id,
                priority=len(actions) + 1,
                expected_lift=expected_lift,
                instruction=instruction,
            )
        )
        seen_dimensions[dimension_id] = seen_dimensions.get(dimension_id, 0) + 1
        if len(actions) >= max_actions:
            break
    return actions


def run_self_improvement_loop(
    candidate_payload: dict[str, Any],
    ontology: dict[str, Any],
    *,
    threshold: float = DEFAULT_THRESHOLD,
    min_dimension_score: float = DEFAULT_MIN_DIMENSION_SCORE,
    max_iterations: int = DEFAULT_MAX_ITERATIONS,
    auto_apply_estimates: bool = False,
) -> dict[str, Any]:
    max_iterations = max(1, max_iterations)
    candidates = _candidate_iterations(candidate_payload)
    if not candidates:
        candidates = [candidate_payload]

    design_id = str(candidate_payload.get("design_id") or candidates[0].get("design_id") or "design-candidate")
    evaluations: list[AestheticEvaluation] = []
    selected: AestheticEvaluation | None = None
    working_candidate = deepcopy(candidates[0])

    for index in range(1, max_iterations + 1):
        if index <= len(candidates):
            current_candidate = deepcopy(candidates[index - 1])
        elif auto_apply_estimates and evaluations:
            current_candidate = _apply_estimated_actions(working_candidate, evaluations[-1].actions)
        else:
            break
        current_candidate.setdefault("design_id", design_id)
        evaluation = evaluate_candidate(
            current_candidate,
            ontology,
            threshold=threshold,
            min_dimension_score=min_dimension_score,
            iteration_index=index,
        )
        evaluations.append(evaluation)
        working_candidate = current_candidate
        if evaluation.passed:
            selected = evaluation
            break

    final_evaluation = selected or evaluations[-1]
    passed = bool(selected)
    status = "passed" if passed else "blocked"
    exhausted = not passed and len(evaluations) >= max_iterations
    if exhausted:
        status = "exhausted"

    return {
        "schema_version": LOOP_SCHEMA_VERSION,
        "design_id": design_id,
        "threshold": threshold,
        "min_dimension_score": min_dimension_score,
        "max_iterations": max_iterations,
        "auto_apply_estimates": auto_apply_estimates,
        "passed": passed,
        "ready_to_execute": passed,
        "status": status,
        "execution_gate": {
            "state": "open" if passed else "blocked",
            "reason": (
                f"{final_evaluation.iteration_id} scored {final_evaluation.score_100:.2f}, "
                f"meeting threshold {threshold * 100:.2f}."
                if passed
                else (
                    f"{final_evaluation.iteration_id} scored {final_evaluation.score_100:.2f}; "
                    f"requires {threshold * 100:.2f} and every dimension >= {min_dimension_score * 100:.2f}."
                )
            ),
        },
        "selected_iteration": final_evaluation.iteration_id if passed else None,
        "iterations": [evaluation.to_dict() for evaluation in evaluations],
        "next_iteration_brief": None if passed else build_next_iteration_brief(final_evaluation),
        "ontology": ontology,
    }


def build_next_iteration_brief(evaluation: AestheticEvaluation) -> dict[str, Any]:
    weak_dimensions = sorted(
        [
            {
                "dimension_id": dimension.dimension_id,
                "label": dimension.label,
                "score": round(dimension.score, 4),
            }
            for dimension in evaluation.dimension_scores
            if dimension.score < evaluation.min_dimension_score
        ],
        key=lambda item: item["score"],
    )
    actions = [action.to_dict() for action in evaluation.actions]
    return {
        "source_iteration": evaluation.iteration_id,
        "focus_dimensions": weak_dimensions,
        "actions": actions,
        "acceptance_criteria": [
            f"Overall aesthetic score >= {evaluation.threshold * 100:.2f}.",
            f"Every dimension score >= {evaluation.min_dimension_score * 100:.2f}.",
            "Re-run the aesthetic loop after the revised candidate is measured.",
        ],
    }


def format_loop_report(report: dict[str, Any]) -> str:
    status = "PASS" if report.get("passed") else "BLOCKED"
    lines = [
        f"Aesthetic self-improvement loop: {status}",
        f"- design_id: {report.get('design_id')}",
        f"- threshold: {float(report.get('threshold', 0.0)) * 100:.2f}",
        f"- gate: {report.get('execution_gate', {}).get('state')}",
        f"- reason: {report.get('execution_gate', {}).get('reason')}",
    ]
    lines.append("- iterations:")
    for evaluation in report.get("iterations", []):
        mark = "PASS" if evaluation.get("passed") else "FAIL"
        lines.append(
            f"  - {evaluation.get('iteration_id')}: {evaluation.get('score_100'):.2f} "
            f"({mark}, coverage {float(evaluation.get('coverage_ratio', 0.0)) * 100:.1f}%)"
        )

    brief = report.get("next_iteration_brief")
    if brief:
        lines.append("- next actions:")
        for action in brief.get("actions", [])[:6]:
            lines.append(
                f"  - P{action.get('priority')} {action.get('dimension_id')}/{action.get('metric_id')}: "
                f"{action.get('instruction')}"
            )
    return "\n".join(lines)


def _candidate_iterations(candidate_payload: dict[str, Any]) -> list[dict[str, Any]]:
    iterations = candidate_payload.get("iterations")
    if not isinstance(iterations, list):
        return []
    return [item for item in iterations if isinstance(item, dict)]


def _candidate_metrics(candidate: dict[str, Any]) -> dict[str, Any]:
    for key in ("metrics", "scores", "metric_scores"):
        value = candidate.get(key)
        if isinstance(value, dict):
            return value
    return {}


def _candidate_dimension_scores(candidate: dict[str, Any]) -> dict[str, Any]:
    for key in ("dimension_scores", "dimensions"):
        value = candidate.get(key)
        if isinstance(value, dict):
            return value
    return {}


def _score_scale(candidate: dict[str, Any]) -> float:
    for key in ("score_scale", "scale"):
        value = _as_number(candidate.get(key))
        if value and value > 0:
            return value
    metrics = _candidate_metrics(candidate)
    numeric_values = [_as_number(value) for value in metrics.values()]
    max_value = max((value for value in numeric_values if value is not None), default=1.0)
    return 1.0 if max_value <= 1.0 else 10.0


def _normalize_score(value: float | None, score_scale: float) -> float:
    if value is None:
        return 0.0
    if value <= 1.0 and score_scale <= 1.0:
        return min(max(value, 0.0), 1.0)
    if value <= 1.0 and score_scale > 1.0:
        return min(max(value, 0.0), 1.0)
    return min(max(value / score_scale, 0.0), 1.0)


def _as_number(value: Any) -> float | None:
    if isinstance(value, bool) or value is None:
        return None
    if isinstance(value, int | float):
        return float(value)
    if isinstance(value, str):
        try:
            return float(value.strip())
        except ValueError:
            return None
    return None


def _apply_estimated_actions(candidate: dict[str, Any], actions: list[AestheticAction]) -> dict[str, Any]:
    revised = deepcopy(candidate)
    metrics = dict(_candidate_metrics(revised))
    score_scale = _score_scale(revised)
    for action in actions:
        current = _as_number(metrics.get(action.metric_id))
        if current is None:
            current = 0.0
        current_normalized = _normalize_score(current, score_scale)
        next_normalized = min(current_normalized + action.expected_lift, 1.0)
        metrics[action.metric_id] = round(next_normalized * score_scale, 4)
    revised["metrics"] = metrics
    revised["iteration_id"] = f"{candidate.get('iteration_id', 'estimated')}-estimated"
    revised["estimated_from_actions"] = [action.action_id for action in actions]
    return revised


def _terms_from_profile(brand_profile: dict[str, Any], key: str) -> list[str]:
    value = brand_profile.get(key)
    if isinstance(value, str):
        return _normalize_text_list([value])
    return _normalize_text_list(value)


def _normalize_text_list(values: object) -> list[str]:
    if not isinstance(values, list):
        return []
    seen: set[str] = set()
    normalized: list[str] = []
    for value in values:
        text = re.sub(r"\s+", " ", str(value)).strip()
        if not text:
            continue
        key = text.lower()
        if key in seen:
            continue
        seen.add(key)
        normalized.append(text)
    return normalized


def _brand_metric_id(prefix: str, value: str) -> str:
    raw = value.strip().lower()
    slug = re.sub(r"[^a-z0-9가-힣]+", "-", raw).strip("-")
    if len(slug) > 36:
        slug = slug[:36].strip("-")
    digest = hashlib.sha1(value.encode("utf-8")).hexdigest()[:8]
    return f"{prefix}:{slug or 'item'}-{digest}"
