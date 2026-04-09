from __future__ import annotations

from pathlib import Path

import httpx

from .crawler import CrawlConfig, RobotsCache, crawl_reference
from .ontology import build_ontology_outputs
from .seed_article import fetch_seed_article
from .synthesis import build_blueprint, load_brand_profile
from .utils import write_json, write_jsonl


def run_pipeline(
    client: httpx.Client,
    seed_url: str,
    output_dir: Path,
    brand_profile_path: Path | None,
    max_sources: int | None,
    max_pages_per_source: int,
    max_depth: int,
) -> dict:
    seed_article = fetch_seed_article(client, seed_url)
    references = seed_article.references[:max_sources] if max_sources else seed_article.references

    write_json(output_dir / "seed_article.json", seed_article.to_dict())
    write_jsonl(
        output_dir / "references.jsonl",
        [reference.to_dict() for reference in references],
    )

    robots = RobotsCache(client)
    all_documents = []
    manifests = []

    crawl_config = CrawlConfig(
        output_dir=output_dir,
        max_pages_per_source=max_pages_per_source,
        max_depth=max_depth,
    )

    for reference in references:
        documents, manifest = crawl_reference(
            client=client,
            robots=robots,
            reference=reference,
            config=crawl_config,
        )
        all_documents.extend(documents)
        manifests.append(manifest.to_dict())

    write_json(output_dir / "crawl_manifests.json", {"manifests": manifests})
    write_jsonl(
        output_dir / "all_documents.jsonl",
        [document.to_dict() for document in all_documents],
    )
    build_ontology_outputs(output_dir, references, all_documents)
    if brand_profile_path:
        brand_profile = load_brand_profile(brand_profile_path)
        build_blueprint(output_dir, brand_profile, references, all_documents)
    return {
        "seed_article": seed_article,
        "references": references,
        "documents": all_documents,
    }
