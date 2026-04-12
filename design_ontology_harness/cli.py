from __future__ import annotations

import argparse
import json
import shutil
from pathlib import Path

import httpx

from .agent_packs import scaffold_agent_pack
from .cli_shared import run_pipeline
from .kb import build_knowledge_base, load_knowledge_base
from .models import DocumentRecord, ReferenceLink
from .scaffold import load_project, resolve_kb_dir, scaffold_project
from .seed_article import fetch_seed_article
from .synthesis import build_blueprint, load_brand_profile
from .utils import ensure_dir, write_json, write_jsonl


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Design ontology harness")
    subparsers = parser.add_subparsers(dest="command", required=True)

    run_parser = subparsers.add_parser("run", help="Run the full pipeline")
    run_parser.add_argument("--seed-url", required=True, help="Seed URL. Can be a curated article or a direct design-system URL.")
    run_parser.add_argument("--output-dir", default="data", help="Directory for outputs")
    run_parser.add_argument(
        "--brand-profile",
        default=None,
        help="Optional path to a JSON brand profile for custom blueprint synthesis",
    )
    run_parser.add_argument("--max-sources", type=int, default=None, help="Optional cap")
    run_parser.add_argument("--max-pages-per-source", type=int, default=3)
    run_parser.add_argument("--max-depth", type=int, default=1)

    kb_parser = subparsers.add_parser("build-kb", help="Build a reusable knowledge base from one or more seed URLs")
    kb_parser.add_argument("--kb-dir", required=True, help="Output directory for the knowledge base")
    kb_parser.add_argument(
        "--seed-url",
        action="append",
        dest="seed_urls",
        default=[],
        help="Seed URL to ingest. Can be a curated article or a direct design-system URL. Can be passed multiple times.",
    )
    kb_parser.add_argument("--seeds-file", default=None, help="Optional file containing seed URLs")
    kb_parser.add_argument("--max-sources", type=int, default=None)
    kb_parser.add_argument("--max-pages-per-source", type=int, default=2)
    kb_parser.add_argument("--max-depth", type=int, default=1)

    init_parser = subparsers.add_parser("init", help="Scaffold a reusable harness project")
    init_parser.add_argument("--project-dir", required=True, help="Directory for the new project")
    init_parser.add_argument("--brand-name", required=True, help="Brand or product name")
    init_parser.add_argument("--system-name", default=None, help="Optional system name")
    init_parser.add_argument("--product-summary", default=None, help="Optional one-line product summary")
    init_parser.add_argument(
        "--seed-url",
        action="append",
        dest="seed_urls",
        default=[],
        help="Optional initial seed URL. Can be a curated article or a direct design-system URL. Can be passed multiple times.",
    )
    init_parser.add_argument("--kb-dir", default=None, help="Optional default knowledge base path to store in the project manifest")
    init_parser.add_argument("--force", action="store_true", help="Allow writing into a non-empty directory")

    agent_pack_parser = subparsers.add_parser("init-agent-pack", help="Scaffold Codex and/or Claude Code integrations into an implementation repo")
    agent_pack_parser.add_argument("--target-repo", required=True, help="Implementation repository path")
    agent_pack_parser.add_argument("--artifact-dir", default="design-system", help="Directory inside the target repo where synced design-system artifacts live")
    agent_pack_parser.add_argument(
        "--targets",
        default="codex,claude",
        help="Comma-separated targets: codex, claude, or both",
    )
    agent_pack_parser.add_argument("--force", action="store_true", help="Overwrite existing integration files")

    seed_parser = subparsers.add_parser("extract-seed", help="Only extract references")
    seed_parser.add_argument("--seed-url", required=True, help="Seed URL. Can be a curated article or a direct design-system URL.")
    seed_parser.add_argument("--output-dir", default="data", help="Directory for outputs")

    synth_parser = subparsers.add_parser("synthesize", help="Build a custom blueprint from existing crawl outputs")
    synth_parser.add_argument("--output-dir", default="data", help="Directory for outputs")
    synth_parser.add_argument("--brand-profile", required=True, help="Path to a JSON brand profile")

    project_parser = subparsers.add_parser("run-project", help="Run a scaffolded harness project against an existing KB")
    project_parser.add_argument("--project-dir", required=True, help="Project directory created by init")
    project_parser.add_argument("--kb-dir", default=None, help="Optional override for the knowledge base path")

    return parser


def main() -> None:
    args = build_parser().parse_args()
    output_dir = ensure_dir(Path(args.output_dir)) if hasattr(args, "output_dir") else None

    if args.command == "init":
        result = scaffold_project(
            project_dir=Path(args.project_dir),
            brand_name=args.brand_name,
            system_name=args.system_name,
            product_summary=args.product_summary,
            seed_urls=args.seed_urls,
            kb_dir=args.kb_dir,
            force=args.force,
        )
        print(f"[init] 프로젝트 생성 완료: {result['project_dir']}")
        print(f"  -> brand_profile.json 을 열어 브랜드 정보를 입력하세요.")
        return

    if args.command == "init-agent-pack":
        scaffold_agent_pack(
            target_repo=Path(args.target_repo),
            artifact_dir=args.artifact_dir,
            targets=[item.strip() for item in args.targets.split(",") if item.strip()],
            force=args.force,
        )
        print(f"[init-agent-pack] 에이전트 팩 생성 완료: {args.target_repo}")
        return

    headers = {
        "User-Agent": "Mozilla/5.0 (compatible; DesignOntologyHarness/0.1)",
    }
    with httpx.Client(headers=headers, follow_redirects=True) as client:
        if args.command == "build-kb":
            seed_urls = list(args.seed_urls)
            if args.seeds_file:
                seeds_file = Path(args.seeds_file)
                seed_urls.extend(
                    [
                        line.strip()
                        for line in seeds_file.read_text(encoding="utf-8").splitlines()
                        if line.strip() and not line.strip().startswith("#")
                    ]
                )
            if not seed_urls:
                raise SystemExit("Provide at least one --seed-url or a --seeds-file.")
            print(f"[build-kb] {len(seed_urls)}개 시드 URL에서 KB 빌드 시작...")
            manifest = build_knowledge_base(
                client=client,
                seed_urls=seed_urls,
                kb_dir=Path(args.kb_dir),
                max_sources=args.max_sources,
                max_pages_per_source=args.max_pages_per_source,
                max_depth=args.max_depth,
            )
            print(f"[build-kb] KB 빌드 완료: {args.kb_dir}")
            print(f"  -> 시드: {manifest['seed_count']}개 | 레퍼런스: {manifest['reference_count']}개 | 문서: {manifest['document_count']}개")
            return

        if args.command == "extract-seed":
            seed_article = fetch_seed_article(client, args.seed_url)
            write_json(output_dir / "seed_article.json", seed_article.to_dict())
            write_jsonl(
                output_dir / "references.jsonl",
                [reference.to_dict() for reference in seed_article.references],
            )
            print(f"[extract-seed] 시드 추출 완료: {seed_article.title}")
            print(f"  -> 레퍼런스 {len(seed_article.references)}개 발견 ({output_dir})")
            return

        if args.command == "synthesize":
            brand_profile = load_brand_profile(Path(args.brand_profile))
            references_path = output_dir / "references.jsonl"
            documents_path = output_dir / "all_documents.jsonl"
            if not references_path.exists() or not documents_path.exists():
                raise SystemExit("Run the crawl pipeline first so references and documents exist.")

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
            build_blueprint(output_dir, brand_profile, references, documents)
            print(f"[synthesize] 블루프린트 재생성 완료 ({output_dir}/blueprint/)")
            return

        if args.command == "run-project":
            project_dir = Path(args.project_dir)
            manifest = load_project(project_dir)
            kb_dir = resolve_kb_dir(project_dir, manifest, args.kb_dir)
            references, documents, kb_manifest = load_knowledge_base(kb_dir)
            brand_profile_path = project_dir / manifest["brand_profile"]
            brand_profile = load_brand_profile(brand_profile_path)
            _warn_placeholder_profile(brand_profile)
            build_root = ensure_dir(project_dir / manifest.get("build_dir", "build"))
            output_dir = ensure_dir(build_root / "system")
            write_jsonl(output_dir / "references.jsonl", [reference.to_dict() for reference in references])
            write_jsonl(output_dir / "all_documents.jsonl", [document.to_dict() for document in documents])
            if (kb_dir / "ontology").exists():
                shutil.copytree(kb_dir / "ontology", output_dir / "ontology", dirs_exist_ok=True)
            build_blueprint(
                output_dir=output_dir,
                brand_profile=brand_profile,
                references=references,
                documents=documents,
            )
            write_json(
                build_root / "project_summary.json",
                {
                    "project_dir": str(project_dir),
                    "kb_dir": str(kb_dir),
                    "reference_count": len(references),
                    "document_count": len(documents),
                    "kb_built_at": kb_manifest.get("built_at"),
                    "output_dir": str(output_dir),
                },
            )
            print(f"[run-project] 시스템 산출물 생성 완료: {output_dir}/blueprint/")
            print(f"  -> 레퍼런스: {len(references)}개 | 문서: {len(documents)}개")
            print(f"  -> system_spec.md 를 확인하세요.")
            return

        result = run_pipeline(
            client=client,
            seed_url=args.seed_url,
            output_dir=output_dir,
            brand_profile_path=Path(args.brand_profile) if args.brand_profile else None,
            max_sources=args.max_sources,
            max_pages_per_source=args.max_pages_per_source,
            max_depth=args.max_depth,
        )
        print(f"[run] 파이프라인 완료: {output_dir}")
        print(f"  -> 레퍼런스: {len(result['references'])}개 | 문서: {len(result['documents'])}개")
        if args.brand_profile:
            print(f"  -> 블루프린트: {output_dir}/blueprint/")


_PLACEHOLDER_PATTERNS = [
    "Describe your",
    "Describe the",
    "List the core",
]


def _warn_placeholder_profile(profile: dict) -> None:
    found = []
    for key, value in profile.items():
        if key.startswith("_"):
            continue
        texts = []
        if isinstance(value, str):
            texts = [value]
        elif isinstance(value, list):
            texts = [item for item in value if isinstance(item, str)]
        for text in texts:
            if any(pattern in text for pattern in _PLACEHOLDER_PATTERNS):
                found.append(key)
                break
    if found:
        print(f"[warning] brand_profile.json에 아직 기본값이 남아 있는 항목: {', '.join(found)}")
        print(f"  -> 실제 브랜드 정보를 입력해야 의미 있는 산출물이 나옵니다.")


if __name__ == "__main__":
    main()
