from __future__ import annotations

import re
from pathlib import Path

from .models import DocumentRecord, ReferenceLink
from .utils import ensure_dir, write_json, write_jsonl

CONCEPTS = [
    {"id": "design_system", "label": "Design System", "terms": ["design system", "디자인 시스템", "design language"]},
    {"id": "style_guide", "label": "Style Guide", "terms": ["style guide", "스타일 가이드", "brand guide", "design guide"]},
    {"id": "design_token", "label": "Design Token", "terms": ["design token", "token", "토큰"]},
    {"id": "component", "label": "Component", "terms": ["component", "components", "컴포넌트"]},
    {"id": "pattern", "label": "Pattern", "terms": ["pattern", "patterns", "패턴"]},
    {"id": "foundation", "label": "Foundation", "terms": ["foundation", "foundations", "기초", "기반"]},
    {"id": "color", "label": "Color", "terms": ["color", "colour", "색상", "컬러"]},
    {"id": "typography", "label": "Typography", "terms": ["typography", "font", "fonts", "타이포그래피", "폰트"]},
    {"id": "iconography", "label": "Iconography", "terms": ["iconography", "icon", "icons", "아이콘"]},
    {"id": "spacing", "label": "Spacing", "terms": ["spacing", "space", "간격", "spacing scale"]},
    {"id": "layout", "label": "Layout", "terms": ["layout", "grid", "레이아웃", "그리드"]},
    {"id": "motion", "label": "Motion", "terms": ["motion", "animation", "모션", "애니메이션"]},
    {"id": "accessibility", "label": "Accessibility", "terms": ["accessibility", "a11y", "접근성"]},
    {"id": "content", "label": "Content", "terms": ["content", "copywriting", "writing", "콘텐츠"]},
    {"id": "brand", "label": "Brand", "terms": ["brand", "branding", "브랜드", "logo"]},
    {
        "id": "imagery",
        "label": "Imagery",
        "terms": ["imagery", "visual asset", "generated image", "image generation", "illustration", "media asset"],
    },
    {
        "id": "product_realism",
        "label": "Commercial Product Realism",
        "terms": [
            "commercial UI",
            "production UI",
            "real product",
            "operational UI",
            "operational density",
            "data provenance",
            "status variation",
            "live operations",
        ],
    },
]


def build_ontology_outputs(
    output_dir: Path,
    references: list[ReferenceLink],
    crawled_documents: list[DocumentRecord],
) -> None:
    ontology_dir = ensure_dir(output_dir / "ontology")
    write_json(ontology_dir / "concepts.json", {"concepts": CONCEPTS})

    evidence_rows: list[dict] = []
    relation_rows: list[dict] = []

    reference_map = {reference.curated_title: reference for reference in references}

    for document in crawled_documents:
        if document.error:
            continue
        matched_concepts = _match_concepts(document)
        for match in matched_concepts:
            evidence_rows.append(
                {
                    "source_label": document.source_label,
                    "reference_slug": document.reference_slug,
                    "document_url": document.final_url,
                    "concept_id": match["concept_id"],
                    "concept_label": match["concept_label"],
                    "matched_term": match["matched_term"],
                    "evidence_text": match["evidence_text"],
                }
            )
            relation_rows.append(
                {
                    "subject": f"source:{document.reference_slug}",
                    "predicate": "covers",
                    "object": f"concept:{match['concept_id']}",
                    "evidence_url": document.final_url,
                    "evidence_text": match["evidence_text"],
                }
            )

        reference = reference_map.get(document.source_label)
        if reference:
            relation_rows.append(
                {
                    "subject": f"article:{reference.source_article_url}",
                    "predicate": "curates",
                    "object": f"source:{document.reference_slug}",
                    "evidence_url": reference.source_article_url,
                    "evidence_text": reference.curated_title,
                }
            )

    write_jsonl(ontology_dir / "evidence.jsonl", evidence_rows)
    write_jsonl(ontology_dir / "relations.jsonl", relation_rows)


def _match_concepts(document: DocumentRecord) -> list[dict]:
    text_chunks = []
    if document.title:
        text_chunks.append(document.title)
    text_chunks.extend(document.headings[:20])
    text_chunks.extend(document.text.splitlines()[:120])

    matches: list[dict] = []
    seen: set[tuple[str, str]] = set()

    for chunk in text_chunks:
        lowered = chunk.lower()
        for concept in CONCEPTS:
            for term in concept["terms"]:
                if re.search(rf"(?<!\w){re.escape(term.lower())}(?!\w)", lowered):
                    key = (concept["id"], chunk)
                    if key in seen:
                        continue
                    seen.add(key)
                    matches.append(
                        {
                            "concept_id": concept["id"],
                            "concept_label": concept["label"],
                            "matched_term": term,
                            "evidence_text": chunk,
                        }
                    )
                    break
    return matches
