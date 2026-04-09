from __future__ import annotations

import json
from pathlib import Path
from urllib.parse import urlparse

import httpx

from .cli_shared import run_pipeline
from .models import DocumentRecord, ReferenceLink, SeedArticle, utc_now_iso
from .ontology import build_ontology_outputs
from .utils import ensure_dir, slugify, write_json, write_jsonl


def build_knowledge_base(
    client: httpx.Client,
    seed_urls: list[str],
    kb_dir: Path,
    max_sources: int | None,
    max_pages_per_source: int,
    max_depth: int,
) -> dict:
    ensure_dir(kb_dir)
    seeds_dir = ensure_dir(kb_dir / "seeds")

    all_seed_articles: list[dict] = []
    all_references: list[ReferenceLink] = []
    all_documents: list[DocumentRecord] = []
    seed_runs: list[dict] = []

    for index, seed_url in enumerate(seed_urls, start=1):
        parsed = urlparse(seed_url)
        seed_slug = slugify(f"{index}-{parsed.netloc}-{parsed.path or 'seed'}")
        seed_output_dir = ensure_dir(seeds_dir / seed_slug)
        result = run_pipeline(
            client=client,
            seed_url=seed_url,
            output_dir=seed_output_dir,
            brand_profile_path=None,
            max_sources=max_sources,
            max_pages_per_source=max_pages_per_source,
            max_depth=max_depth,
        )
        all_seed_articles.append(result["seed_article"].to_dict())
        all_references.extend(result["references"])
        all_documents.extend(result["documents"])
        seed_runs.append(
            {
                "seed_url": seed_url,
                "seed_slug": seed_slug,
                "output_dir": str(seed_output_dir),
                "reference_count": len(result["references"]),
                "document_count": len(result["documents"]),
            }
        )

    write_json(kb_dir / "all_seed_articles.json", {"items": all_seed_articles})
    write_jsonl(kb_dir / "references.jsonl", [reference.to_dict() for reference in all_references])
    write_jsonl(kb_dir / "all_documents.jsonl", [document.to_dict() for document in all_documents])
    build_ontology_outputs(kb_dir, all_references, all_documents)

    manifest = {
        "kind": "knowledge_base",
        "built_at": utc_now_iso(),
        "seed_count": len(seed_urls),
        "reference_count": len(all_references),
        "document_count": len(all_documents),
        "seeds": seed_runs,
        "settings": {
            "max_sources": max_sources,
            "max_pages_per_source": max_pages_per_source,
            "max_depth": max_depth,
        },
    }
    write_json(kb_dir / "kb_manifest.json", manifest)
    return manifest


def load_knowledge_base(kb_dir: Path) -> tuple[list[ReferenceLink], list[DocumentRecord], dict]:
    manifest_path = kb_dir / "kb_manifest.json"
    references_path = kb_dir / "references.jsonl"
    documents_path = kb_dir / "all_documents.jsonl"
    if not manifest_path.exists():
        raise ValueError(f"Missing kb_manifest.json in {kb_dir}")
    if not references_path.exists() or not documents_path.exists():
        raise ValueError(f"Knowledge base is incomplete in {kb_dir}")

    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    references = [
        ReferenceLink(**json.loads(line))
        for line in references_path.read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]
    documents = [
        DocumentRecord(**json.loads(line))
        for line in documents_path.read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]
    return references, documents, manifest
