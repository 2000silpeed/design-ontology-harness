from __future__ import annotations

import json
from pathlib import Path
from urllib.parse import urlparse

import httpx

from .cli_shared import run_pipeline
from .css_pipeline import run_css_extraction
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
    seed_errors: list[dict] = []

    for index, seed_url in enumerate(seed_urls, start=1):
        parsed = urlparse(seed_url)
        seed_slug = slugify(f"{index}-{parsed.netloc}-{parsed.path or 'seed'}")
        seed_output_dir = ensure_dir(seeds_dir / seed_slug)
        try:
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
                    "seed_kind": result["seed_article"].seed_kind,
                    "seed_title": result["seed_article"].title,
                    "output_dir": str(seed_output_dir),
                    "reference_count": len(result["references"]),
                    "document_count": len(result["documents"]),
                    "status": "ok",
                }
            )
        except Exception as exc:
            error_message = str(exc)
            seed_errors.append(
                {
                    "seed_url": seed_url,
                    "seed_slug": seed_slug,
                    "error": error_message,
                }
            )
            seed_runs.append(
                {
                    "seed_url": seed_url,
                    "seed_slug": seed_slug,
                    "seed_kind": "error",
                    "seed_title": "",
                    "output_dir": str(seed_output_dir),
                    "reference_count": 0,
                    "document_count": 0,
                    "status": "error",
                    "error": error_message,
                }
            )

    write_json(kb_dir / "all_seed_articles.json", {"items": all_seed_articles})
    write_jsonl(kb_dir / "references.jsonl", [reference.to_dict() for reference in all_references])
    write_jsonl(kb_dir / "all_documents.jsonl", [document.to_dict() for document in all_documents])
    build_ontology_outputs(kb_dir, all_references, all_documents)
    _merge_css_extraction(kb_dir, seeds_dir)

    manifest = {
        "kind": "knowledge_base",
        "built_at": utc_now_iso(),
        "seed_count": len(seed_urls),
        "reference_count": len(all_references),
        "document_count": len(all_documents),
        "seeds": seed_runs,
        "seed_error_count": len(seed_errors),
        "seed_errors": seed_errors,
        "settings": {
            "max_sources": max_sources,
            "max_pages_per_source": max_pages_per_source,
            "max_depth": max_depth,
        },
    }
    write_json(kb_dir / "kb_manifest.json", manifest)
    return manifest


def _merge_css_extraction(kb_dir: Path, seeds_dir: Path) -> None:
    """Collect all .css files crawled across all seeds and re-run extraction at KB root."""
    all_css_parts: list[str] = []
    css_file_count = 0

    for css_dir in sorted(seeds_dir.glob("*/crawls/*/css")):
        for css_file in sorted(css_dir.glob("*.css")):
            try:
                all_css_parts.append(css_file.read_text(encoding="utf-8", errors="replace"))
                css_file_count += 1
            except OSError:
                continue

    if not all_css_parts:
        print(f"  [kb] CSS 병합 건너뜀: 수집된 CSS 파일이 없습니다")
        return

    all_css = "\n".join(all_css_parts)
    css_result = run_css_extraction(all_css)

    css_out = ensure_dir(kb_dir / "css_extraction")
    write_json(css_out / "resolved_tokens.json", css_result["var_resolution"])
    write_json(css_out / "brand_candidates.json", css_result["brand_colors"])
    write_json(css_out / "typography.json", css_result["typography"])
    write_json(css_out / "alias_layer.json", css_result["alias_layer"])
    summary = {
        "css_file_count": css_file_count,
        "var_resolution": {
            "total_vars": css_result["var_resolution"]["total_vars"],
            "resolved_count": css_result["var_resolution"]["resolved_count"],
            "unresolved_count": css_result["var_resolution"]["unresolved_count"],
        },
        "brand_colors": css_result["brand_colors"]["summary"],
        "typography": css_result["typography"]["stats"],
        "alias_layer": css_result["alias_layer"]["stats"],
    }
    write_json(css_out / "extraction_summary.json", summary)

    var_info = css_result["var_resolution"]
    brand_info = css_result["brand_colors"]["summary"]
    typo_info = css_result["typography"]["stats"]
    print(
        f"  [kb] CSS 병합: {css_file_count}개 파일 | "
        f"var {var_info['resolved_count']}/{var_info['total_vars']}개 | "
        f"브랜드색 {brand_info['total_candidates']}개 | "
        f"타이포 {typo_info['scale_entries']}개"
    )


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
