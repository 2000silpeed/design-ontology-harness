from __future__ import annotations

from pathlib import Path

import httpx

from .crawler import CrawlConfig, RobotsCache, crawl_reference
from .css_pipeline import run_css_extraction
from .ontology import build_ontology_outputs
from .seed_article import fetch_seed_article
from .synthesis import build_blueprint, load_brand_profile
from .utils import ensure_dir, write_json, write_jsonl


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

    crawl_errors = []
    for index, reference in enumerate(references, start=1):
        label = reference.curated_title or reference.href
        print(f"  [{index}/{len(references)}] 크롤링: {label[:60]}")
        documents, manifest = crawl_reference(
            client=client,
            robots=robots,
            reference=reference,
            config=crawl_config,
        )
        all_documents.extend(documents)
        manifests.append(manifest.to_dict())
        if manifest.error_count > 0:
            crawl_errors.append((label, manifest.error_count, manifest.errors))

    write_json(output_dir / "crawl_manifests.json", {"manifests": manifests})
    write_jsonl(
        output_dir / "all_documents.jsonl",
        [document.to_dict() for document in all_documents],
    )
    ok_count = sum(1 for doc in all_documents if not doc.error)
    err_count = len(all_documents) - ok_count
    print(f"  크롤링 완료: 성공 {ok_count}건 / 실패 {err_count}건")
    if crawl_errors:
        print(f"  실패한 소스:")
        for label, count, errors in crawl_errors:
            print(f"    - {label[:50]}: {count}건 에러")
            for error in errors[:2]:
                print(f"      {error.get('url', '')} -> {error.get('reason', '')}")

    build_ontology_outputs(output_dir, references, all_documents)

    css_crawl_dirs = sorted((output_dir / "crawls").glob("*/css")) if (output_dir / "crawls").exists() else []
    if css_crawl_dirs:
        all_css = ""
        for css_dir in css_crawl_dirs:
            for css_file in sorted(css_dir.glob("*.css")):
                all_css += css_file.read_text(encoding="utf-8", errors="replace") + "\n"
        if all_css.strip():
            first_doc_html = ""
            for doc in all_documents:
                if not doc.error and doc.depth == 0:
                    html_path = output_dir / "crawls" / doc.reference_slug / "documents.jsonl"
                    break
            css_result = run_css_extraction(all_css)
            css_out = ensure_dir(output_dir / "css_extraction")
            write_json(css_out / "resolved_tokens.json", css_result["var_resolution"])
            write_json(css_out / "brand_candidates.json", css_result["brand_colors"])
            write_json(css_out / "typography.json", css_result["typography"])
            write_json(css_out / "alias_layer.json", css_result["alias_layer"])
            var_info = css_result["var_resolution"]
            brand_info = css_result["brand_colors"]["summary"]
            typo_info = css_result["typography"]["stats"]
            print(f"  CSS 추출: var {var_info['resolved_count']}/{var_info['total_vars']}개 | 브랜드색 {brand_info['total_candidates']}개 | 타이포 {typo_info['scale_entries']}개")

    if brand_profile_path:
        brand_profile = load_brand_profile(brand_profile_path)
        build_blueprint(output_dir, brand_profile, references, all_documents)
    return {
        "seed_article": seed_article,
        "references": references,
        "documents": all_documents,
    }
