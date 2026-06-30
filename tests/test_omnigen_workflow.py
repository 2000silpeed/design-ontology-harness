import base64
import json
import sqlite3
from pathlib import Path

from design_ontology_harness.omnigen_references import IMAGE_COLUMNS
from design_ontology_harness.omnigen_workflow import curate_omnigen_reference_artifacts


PNG_1X1 = base64.b64decode(
    "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mP8z8BQDwAFgwJ/"
    "l8WnXwAAAABJRU5ErkJggg=="
)


def test_curate_omnigen_reference_artifacts_selects_syncs_and_analyzes(tmp_path: Path) -> None:
    vault_dir = tmp_path / "vault"
    project_dir = tmp_path / "project"
    vault_dir.mkdir()
    project_dir.mkdir()
    index_path = vault_dir / "index.sqlite"
    _create_omnigen_index(index_path)

    agent_ui = _write_png(vault_dir, "images/ai-agent-ui/agent-console.png")
    pricing = _write_png(vault_dir, "images/web-design/pricing.png")
    _insert_image(
        index_path,
        id=1,
        category="ai-agent-ui",
        subject="an agent task console with tool timeline",
        style="dense agent workspace",
        palette="neutral blue",
        mood="operational",
        rel_path="images/ai-agent-ui/agent-console.png",
        abs_path=str(agent_ui),
        sha256="sha-agent",
        phash="phash-agent",
    )
    _insert_image(
        index_path,
        id=2,
        category="web-design",
        subject="a pricing page with three plan cards",
        style="marketing page",
        palette="warm neutral",
        mood="calm",
        rel_path="images/web-design/pricing.png",
        abs_path=str(pricing),
        sha256="sha-pricing",
        phash="phash-pricing",
    )

    brand_profile_path = project_dir / "brand_profile.json"
    brand_profile_path.write_text(
        json.dumps(
            {
                "brand_name": "Agent Bench",
                "system_name": "Agent Bench System",
                "product_summary": "Agent task console for reviewing tool timelines.",
                "brand_keywords": ["clear", "operational"],
                "visual_keywords": ["dashboard", "agent console"],
                "product_primitives": ["task queue", "tool timeline"],
                "visual_reference": {
                    "mode": "local-images",
                    "query": ["agent task console"],
                    "sources": [],
                    "preferred_count": 4,
                    "extraction_policy": "advisory-only",
                },
            }
        ),
        encoding="utf-8",
    )

    result = curate_omnigen_reference_artifacts(
        brand_profile_path=brand_profile_path,
        project_dir=project_dir,
        vault_dir=vault_dir,
        query="agent task console",
        count=1,
    )

    selected = result["selection_manifest"]["selected"]
    assert selected[0]["category"] == "ai-agent-ui"
    assert (project_dir / selected[0]["selected_relative_path"]).exists()
    assert result["gallery_path"].exists()
    assert result["workflow_summary_path"].exists()
    assert (project_dir / "build" / "visuals" / "visual_reference_report.json").exists()
    assert (project_dir / "build" / "visuals" / "design_context_pack.json").exists()

    updated_profile = json.loads(brand_profile_path.read_text(encoding="utf-8"))
    sources = updated_profile["visual_reference"]["sources"]
    assert len(sources) == 1
    assert sources[0]["provider_id"] == "omnigen-vault"
    assert sources[0]["path"] == selected[0]["selected_relative_path"]

    workflow_summary = json.loads(result["workflow_summary_path"].read_text(encoding="utf-8"))
    assert workflow_summary["selected_count"] == 1
    assert workflow_summary["coverage"]["image_count"] == 1
    assert workflow_summary["design_context_activation"]


def _create_omnigen_index(path: Path) -> None:
    typed_columns = []
    for column in IMAGE_COLUMNS:
        if column in {"id", "width", "height", "bytes", "rating", "ocr_char_count"}:
            typed_columns.append(f"{column} integer")
        else:
            typed_columns.append(f"{column} text")
    with sqlite3.connect(path) as connection:
        connection.execute(f"create table images ({', '.join(typed_columns)})")


def _insert_image(path: Path, **overrides: object) -> None:
    row = {
        "id": 0,
        "category": "app-design",
        "subject": "",
        "style": "",
        "lighting": "",
        "palette": "",
        "composition": "",
        "mood": "",
        "variant": "",
        "prompt": "",
        "revised_prompt": "",
        "rel_path": "",
        "abs_path": "",
        "width": 1536,
        "height": 1024,
        "size_label": "1536x1024",
        "bytes": len(PNG_1X1),
        "sha256": "",
        "bucket": "landscape",
        "phash": "",
        "thumb_rel": "",
        "thumb_abs": "",
        "rating": 0,
        "ocr_char_count": 0,
        "ocr_text": "",
        "status": "active",
        "tags": json.dumps(["ui", "dashboard"]),
        "created_at": "2026-06-20T00:00:00Z",
    }
    row.update(overrides)
    columns = list(IMAGE_COLUMNS)
    values = [row[column] for column in columns]
    placeholders = ",".join("?" for _ in columns)
    with sqlite3.connect(path) as connection:
        connection.execute(
            f"insert into images ({', '.join(columns)}) values ({placeholders})",
            values,
        )


def _write_png(root: Path, rel_path: str) -> Path:
    path = root / rel_path
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(PNG_1X1)
    return path
