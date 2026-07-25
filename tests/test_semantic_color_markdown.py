import json
from pathlib import Path

import pytest

import design_ontology_harness.semantic_color_markdown as semantic_color_markdown
from design_ontology_harness.color_reference import resolve_color_reference
from design_ontology_harness.semantic_color_markdown import (
    SemanticColorMarkdownError,
    build_semantic_color_payload,
    extract_semantic_color_payload,
    extract_runtime_color_policy,
    load_ontology_from_color_reference,
    load_runtime_color_policy,
    pantone_coy_index,
    parse_color_reference_text,
    payload_sha256,
    replace_semantic_color_block,
    strip_semantic_color_block,
    sync_semantic_colors,
)
from design_ontology_harness.semantic_color_ontology import load_semantic_color_ontology
from design_ontology_harness.semantic_color_selector import ontology_keyword_lookup


REPO_ROOT = Path(__file__).resolve().parents[1]
COLOR_REFERENCE = REPO_ROOT / "docs" / "color-reference.md"
SEMANTIC_OS_GRAPH = (
    Path.home()
    / "ai-projects"
    / "semantic-os"
    / "domains"
    / "color"
    / "ontology"
    / "build"
    / "graph.json"
)


def _minimal_graph() -> dict:
    return {
        "built_at": "2026-07-11T00:00:00+00:00",
        "schema_version": "semantic-os-test-v1",
        "nodes": [
            {
                "space": "concept",
                "type": "ColorKeyword",
                "id": "color-keyword-test-blue",
                "properties": {
                    "label": "Test Blue",
                    "rgb_hex": "#123456",
                    "spectrum": "blue",
                    "family": "deep",
                    "category": "Deep Blues",
                    "source_path": "/Users/example/private.pdf",
                },
            },
            {
                "space": "concept",
                "type": "ColorPattern",
                "id": "pattern-test",
                "properties": {"label": "Test", "summary": "test pattern"},
            },
        ],
        "edges": [
            {
                "from": {"space": "concept", "id": "pattern-test"},
                "relation": "supports",
                "to": {"space": "concept", "id": "color-keyword-test-blue"},
            }
        ],
    }


def test_semantic_color_block_round_trip_preserves_visible_markdown():
    visible = "# Existing Reference\n\n## Deep Blues\n\n### Test Blue\n- **HEX**: #123456\n"
    payload = build_semantic_color_payload(_minimal_graph())
    rendered = replace_semantic_color_block(visible, payload)

    assert strip_semantic_color_block(rendered) == visible
    assert extract_semantic_color_payload(rendered) == payload
    assert payload["source"]["transport"] == "docs/color-reference.md"
    assert "source_path" not in json.dumps(payload)
    assert "/Users/" not in rendered


def test_semantic_color_block_rejects_checksum_tampering():
    payload = build_semantic_color_payload(_minimal_graph())
    rendered = replace_semantic_color_block("# Existing\n", payload)
    tampered = rendered.replace('"rgb_hex": "#123456"', '"rgb_hex": "#123457"', 1)

    with pytest.raises(SemanticColorMarkdownError, match="checksum mismatch"):
        extract_semantic_color_payload(tampered)


@pytest.mark.parametrize("checksum_token", ["g" + "f" * 63, "abc123"])
def test_custom_ontology_rejects_malformed_checksum_marker(
    tmp_path: Path, checksum_token: str
):
    text = COLOR_REFERENCE.read_text(encoding="utf-8")
    embedded = extract_semantic_color_payload(text)
    assert embedded is not None
    digest = payload_sha256(embedded)
    valid_marker = f"<!-- semantic-os-color-ontology:begin sha256={digest} -->"
    malformed_marker = (
        f"<!-- semantic-os-color-ontology:begin sha256={checksum_token} -->"
    )
    custom = tmp_path / "malformed-ontology.md"
    custom.write_text(text.replace(valid_marker, malformed_marker, 1), encoding="utf-8")

    with pytest.raises(SemanticColorMarkdownError, match="malformed SHA-256"):
        load_ontology_from_color_reference(custom)


@pytest.mark.parametrize(
    "partial",
    [
        "<!-- semantic-os-color-ontology:begin sha256=" + "0" * 64 + " -->",
        "<!-- semantic-os-color-ontology:end -->",
        "```semantic-color-ontology+json",
    ],
)
def test_partial_ontology_namespace_never_uses_local_fallback(
    tmp_path: Path, partial: str
):
    custom = tmp_path / "partial-ontology.md"
    custom.write_text(
        "# Cards only\n\n## Blues\n\n### Test Blue\n- **HEX**: #123456\n\n"
        f"{partial}\n",
        encoding="utf-8",
    )

    with pytest.raises(SemanticColorMarkdownError, match="namespace is present"):
        load_ontology_from_color_reference(custom)


def test_marker_free_cards_only_reference_retains_local_ontology_fallback(
    tmp_path: Path,
):
    custom = tmp_path / "cards-only.md"
    custom.write_text(
        "# Cards only\n\n## Blues\n\n### Test Blue\n- **HEX**: #123456\n",
        encoding="utf-8",
    )

    ontology, parsed = load_ontology_from_color_reference(custom)

    assert parsed["semantic_ontology_sha256"] is None
    assert ontology["source"]["repo"] == "local-markdown"
    assert ontology["source"]["local_extension_count"] == 1
    assert ontology_keyword_lookup(ontology)["test blue"]["hex"] == "#123456"


def test_sync_semantic_colors_is_deterministic_and_check_detects_drift(tmp_path: Path):
    source = tmp_path / "graph.json"
    reference = tmp_path / "color-reference.md"
    snapshot = tmp_path / "ontology.json"
    source.write_text(json.dumps(_minimal_graph()), encoding="utf-8")
    reference.write_text(
        "# Existing Reference\n\n## Deep Blues\n\n### Test Blue\n- **HEX**: #123456\n",
        encoding="utf-8",
    )

    first = sync_semantic_colors(
        source_path=source,
        color_reference_output=reference,
        ontology_output=snapshot,
    )
    first_text = reference.read_text(encoding="utf-8")
    current = sync_semantic_colors(
        source_path=source,
        color_reference_output=reference,
        ontology_output=snapshot,
        check=True,
    )
    second = sync_semantic_colors(
        source_path=source,
        color_reference_output=reference,
        ontology_output=snapshot,
    )

    assert first["payload_sha256"] == second["payload_sha256"]
    assert reference.read_text(encoding="utf-8") == first_text
    assert current["ok"] is True
    graph = json.loads(source.read_text(encoding="utf-8"))
    graph["nodes"][0]["properties"]["rgb_hex"] = "#654321"
    source.write_text(json.dumps(graph), encoding="utf-8")
    stale = sync_semantic_colors(
        source_path=source,
        color_reference_output=reference,
        ontology_output=snapshot,
        check=True,
    )
    assert stale["ok"] is False
    assert stale["changed"] is True


@pytest.mark.skipif(not SEMANTIC_OS_GRAPH.exists(), reason="local Semantic OS checkout unavailable")
def test_committed_markdown_snapshot_matches_local_semantic_os_graph():
    expected = build_semantic_color_payload(
        json.loads(SEMANTIC_OS_GRAPH.read_text(encoding="utf-8"))
    )
    embedded = extract_semantic_color_payload(COLOR_REFERENCE.read_text(encoding="utf-8"))

    assert embedded is not None
    assert payload_sha256(embedded) == payload_sha256(expected)
    assert embedded["node_count"] == 358
    assert embedded["edge_count"] == 1227


def test_default_runtime_ontology_comes_from_markdown_and_merges_local_cards():
    ontology = load_semantic_color_ontology()
    lookup = ontology_keyword_lookup(ontology)

    assert ontology["source"]["authority"] == "semantic-os-synced-markdown"
    assert ontology["source"]["reference_path"] == "docs/color-reference.md"
    assert ontology["source"]["local_extension_count"] == 2
    assert lookup["rose quartz"]["semantic_node_id"] == (
        "color-keyword-pantone-coy-2016-rose-quartz"
    )
    assert lookup["dark salmon"]["source_type"] == "markdown-local-extension"
    assert lookup["blanched almond"]["source_type"] == "markdown-local-extension"


def test_custom_markdown_value_controls_automatic_palette_selection(tmp_path: Path):
    embedded = extract_semantic_color_payload(COLOR_REFERENCE.read_text(encoding="utf-8"))
    assert embedded is not None
    custom = tmp_path / "custom-color-reference.md"
    visible = """# Custom Semantic Color Reference

## Deep Blues

### Navy Blue
- **HEX**: #112233
- **CMYK**: C 90%, M 80%, Y 60%, K 70%
- **톤/무드**: 신뢰, 권위, 집중, 전문성
- **활용**: custom synchronized navy authority
"""
    custom.write_text(replace_semantic_color_block(visible, embedded), encoding="utf-8")

    resolved, issues = resolve_color_reference(
        {
            "path": str(custom),
            "palette_strategy": {
                "mode": "brand-guided",
                "candidate_count": 5,
                "temperature": "neutral",
                "contrast": "balanced",
                "surface_style": "grounded",
            },
        },
        tmp_path,
        {
            "brand_name": "Midnight Ledger",
            "product_summary": "deep blue cold luxury website for a precise trusted brand",
            "brand_keywords": ["deep", "blue", "luxury", "trustworthy", "precise"],
            "visual_keywords": ["navy blue editorial panels", "ice blue highlights"],
            "product_primitives": ["brand website", "editorial panels"],
        },
    )

    assert not issues
    assert resolved is not None
    assert resolved["selection_mode"] == "semantic-os-markdown"
    assert (
        resolved["semantic_color_selection"]["selection_method"]
        == "semantic-os-markdown-search-per-run"
    )
    navy = next(
        item
        for item in resolved["active_palette"]["roles"].values()
        if item["semantic_node_id"] == "color-keyword-navy-blue"
    )
    assert navy["hex"] == "#112233"
    loaded, _ = load_ontology_from_color_reference(custom)
    assert ontology_keyword_lookup(loaded)["navy blue"]["hex"] == "#112233"


def test_wheel_force_includes_markdown_authority():
    pyproject = (REPO_ROOT / "pyproject.toml").read_text(encoding="utf-8")
    assert '"docs/color-reference.md" = "design_ontology_harness/resources/color-reference.md"' in pyproject


def test_visible_cards_and_generated_coy_identity_index_are_complete():
    text = COLOR_REFERENCE.read_text(encoding="utf-8")
    parsed = parse_color_reference_text(text, source_path=str(COLOR_REFERENCE))
    embedded = parsed["semantic_ontology"]

    assert len(parsed["colors"]) == 87
    assert len(parsed["pantone_coy_index"]) == 29
    assert len({item["semantic_node_id"] for item in parsed["pantone_coy_index"]}) == 29
    assert {item["year"] for item in parsed["pantone_coy_index"]} == set(range(2000, 2027))
    assert sum(item["year"] == 2016 for item in parsed["pantone_coy_index"]) == 2
    assert sum(item["year"] == 2021 for item in parsed["pantone_coy_index"]) == 2
    assert parsed["pantone_coy_index"] == pantone_coy_index(embedded)

    card_hexes = {item["hex"] for item in parsed["colors"]}
    embedded_only = {
        item["hex"] for item in parsed["pantone_coy_index"] if item["hex"] not in card_hexes
    }
    assert len(embedded_only) == 22
    assert all(item["source_reference_id"] for item in parsed["pantone_coy_index"])


def test_generated_coy_catalog_is_single_deterministic_sync_block(tmp_path: Path):
    source = tmp_path / "graph.json"
    reference = tmp_path / "color-reference.md"
    snapshot = tmp_path / "ontology.json"
    graph = _minimal_graph()
    graph["nodes"].append(
        {
            "space": "concept",
            "type": "ColorKeyword",
            "id": "color-keyword-pantone-coy-2023-viva-magenta",
            "properties": {
                "label": "Viva Magenta (Pantone COY 2023)",
                "color_name": "Viva Magenta",
                "coy_year": 2023,
                "category": "Pantone Color of the Year",
                "rgb_hex": "#BB2649",
                "spectrum": "red",
                "source_reference_id": "ref-pantone-coy-announcements",
            },
        }
    )
    source.write_text(json.dumps(graph), encoding="utf-8")
    reference.write_text("# Reference\n", encoding="utf-8")

    sync_semantic_colors(
        source_path=source,
        color_reference_output=reference,
        ontology_output=snapshot,
    )
    first = reference.read_bytes()
    sync_semantic_colors(
        source_path=source,
        color_reference_output=reference,
        ontology_output=snapshot,
    )
    second = reference.read_bytes()

    assert first == second
    assert second.count(b"semantic-os-color-catalog:begin") == 1
    assert second.count(b"semantic-os-color-catalog:end") == 1
    assert second.count(b"color-keyword-pantone-coy-2023-viva-magenta") == 2  # index + payload

    reference.write_text(
        reference.read_text(encoding="utf-8").replace("`#BB2649`", "`#BB2648`", 1),
        encoding="utf-8",
    )
    stale = sync_semantic_colors(
        source_path=source,
        color_reference_output=reference,
        ontology_output=snapshot,
        check=True,
    )
    assert stale["ok"] is False

    # Repair authored-table drift, then prove a real source change can advance both
    # generated blocks without treating the old, internally consistent digest as corrupt.
    sync_semantic_colors(
        source_path=source,
        color_reference_output=reference,
        ontology_output=snapshot,
    )
    graph["nodes"][-1]["properties"]["rgb_hex"] = "#BB264A"
    source.write_text(json.dumps(graph), encoding="utf-8")
    sync_semantic_colors(
        source_path=source,
        color_reference_output=reference,
        ontology_output=snapshot,
    )
    updated_text = reference.read_text(encoding="utf-8")
    updated_payload = extract_semantic_color_payload(updated_text)
    assert updated_payload is not None
    updated_digest = payload_sha256(updated_payload)
    assert (
        f"<!-- semantic-os-color-catalog:begin sha256={updated_digest} -->"
        in updated_text
    )
    assert (
        f"<!-- semantic-os-color-ontology:begin sha256={updated_digest} -->"
        in updated_text
    )
    assert updated_text.count("`#BB264A`") == 1
    assert '"rgb_hex": "#BB264A"' in updated_text
    current = sync_semantic_colors(
        source_path=source,
        color_reference_output=reference,
        ontology_output=snapshot,
        check=True,
    )
    assert current["ok"] is True


@pytest.mark.parametrize("checksum_token", ["g" + "f" * 63, "abc123"])
def test_catalog_rejects_malformed_checksum_marker(
    tmp_path: Path, checksum_token: str
):
    text = COLOR_REFERENCE.read_text(encoding="utf-8")
    embedded = extract_semantic_color_payload(text)
    assert embedded is not None
    digest = payload_sha256(embedded)
    valid_marker = f"<!-- semantic-os-color-catalog:begin sha256={digest} -->"
    malformed_marker = f"<!-- semantic-os-color-catalog:begin sha256={checksum_token} -->"
    custom = tmp_path / "malformed-catalog.md"
    custom.write_text(text.replace(valid_marker, malformed_marker, 1), encoding="utf-8")

    with pytest.raises(SemanticColorMarkdownError, match="malformed SHA-256"):
        parse_color_reference_text(custom.read_text(encoding="utf-8"))


def test_catalog_rejects_valid_form_checksum_that_differs_from_embedded_payload():
    text = COLOR_REFERENCE.read_text(encoding="utf-8")
    embedded = extract_semantic_color_payload(text)
    assert embedded is not None
    digest = payload_sha256(embedded)
    wrong_digest = ("0" if digest[0] != "0" else "1") + digest[1:]
    corrupted = text.replace(
        f"<!-- semantic-os-color-catalog:begin sha256={digest} -->",
        f"<!-- semantic-os-color-catalog:begin sha256={wrong_digest} -->",
        1,
    )

    with pytest.raises(SemanticColorMarkdownError, match="checksum mismatch"):
        parse_color_reference_text(corrupted)


@pytest.mark.parametrize("sentinel", ["begin", "end"])
def test_partial_catalog_namespace_is_rejected(sentinel: str):
    text = COLOR_REFERENCE.read_text(encoding="utf-8")
    embedded = extract_semantic_color_payload(text)
    assert embedded is not None
    digest = payload_sha256(embedded)
    marker = (
        f"<!-- semantic-os-color-catalog:begin sha256={digest} -->"
        if sentinel == "begin"
        else "<!-- semantic-os-color-catalog:end -->"
    )

    with pytest.raises(SemanticColorMarkdownError, match="namespace is present"):
        parse_color_reference_text(text.replace(marker, "", 1))


def test_catalog_absence_is_allowed_but_catalog_without_ontology_is_rejected(
    tmp_path: Path,
):
    embedded = extract_semantic_color_payload(COLOR_REFERENCE.read_text(encoding="utf-8"))
    assert embedded is not None
    cards = "# Custom\n\n## Blues\n\n### Test Blue\n- **HEX**: #123456\n"
    ontology_only = replace_semantic_color_block(cards, embedded)
    custom = tmp_path / "ontology-without-catalog.md"
    custom.write_text(ontology_only, encoding="utf-8")

    loaded, parsed = load_ontology_from_color_reference(custom)
    assert parsed["semantic_ontology"] is not None
    assert loaded["source"]["authority"] == "semantic-os-synced-markdown"

    digest = payload_sha256(embedded)
    catalog_only = "\n".join(
        [
            cards.rstrip(),
            f"<!-- semantic-os-color-catalog:begin sha256={digest} -->",
            "<details></details>",
            "<!-- semantic-os-color-catalog:end -->",
            "",
        ]
    )
    custom.write_text(catalog_only, encoding="utf-8")
    with pytest.raises(SemanticColorMarkdownError, match="requires a checksum-verified"):
        load_ontology_from_color_reference(custom)


def test_sync_rejects_malformed_catalog_without_appending_a_duplicate(tmp_path: Path):
    source = tmp_path / "graph.json"
    reference = tmp_path / "color-reference.md"
    snapshot = tmp_path / "ontology.json"
    source.write_text(json.dumps(_minimal_graph()), encoding="utf-8")
    reference.write_text("# Reference\n", encoding="utf-8")
    sync_semantic_colors(
        source_path=source,
        color_reference_output=reference,
        ontology_output=snapshot,
    )
    embedded = extract_semantic_color_payload(reference.read_text(encoding="utf-8"))
    assert embedded is not None
    digest = payload_sha256(embedded)
    corrupted = reference.read_text(encoding="utf-8").replace(
        f"<!-- semantic-os-color-catalog:begin sha256={digest} -->",
        "<!-- semantic-os-color-catalog:begin sha256=abc123 -->",
        1,
    )
    reference.write_text(corrupted, encoding="utf-8")

    with pytest.raises(SemanticColorMarkdownError, match="malformed SHA-256"):
        sync_semantic_colors(
            source_path=source,
            color_reference_output=reference,
            ontology_output=snapshot,
        )

    unchanged = reference.read_text(encoding="utf-8")
    assert unchanged == corrupted
    assert unchanged.count("semantic-os-color-catalog:begin") == 1
    assert unchanged.count("semantic-os-color-catalog:end") == 1


def test_runtime_policy_is_checksum_verified_and_not_a_color_keyword():
    text = COLOR_REFERENCE.read_text(encoding="utf-8")
    policy = extract_runtime_color_policy(text)
    assert policy is not None
    assert policy == load_runtime_color_policy()
    assert policy["authority"]["kind"] == "typed-runtime-role-policy"
    assert all(
        item["kind"] in {"runtime-role-default", "derived-runtime-role"}
        for item in policy["light_roles"].values()
    )
    assert "ColorKeyword" not in {item["kind"] for item in policy["light_roles"].values()}

    tampered = text.replace('"value": "#F59E0B"', '"value": "#F59E0C"', 1)
    with pytest.raises(SemanticColorMarkdownError, match="policy checksum mismatch"):
        extract_runtime_color_policy(tampered)


@pytest.mark.parametrize("damage", ["dark-key", "chrome-value", "target-value"])
def test_runtime_policy_rejects_checksum_valid_structural_damage(damage: str):
    policy = load_runtime_color_policy()
    broken = json.loads(json.dumps(policy))
    if damage == "dark-key":
        broken["dark_derivation"].pop("chromatic_lightness_range")
    elif damage == "chrome-value":
        broken["chrome_roles"]["chrome_ink"]["value"] = "not-a-hex"
    else:
        broken["dark_derivation"]["role_lightness_targets"]["canvas"] = True
    digest = payload_sha256(broken)
    text = "\n".join(
        [
            f"<!-- design-ontology-runtime-color-policy:begin sha256={digest} -->",
            "```design-ontology-runtime-color-policy+json",
            json.dumps(broken, ensure_ascii=False, indent=2, sort_keys=True),
            "```",
            "<!-- design-ontology-runtime-color-policy:end -->",
        ]
    )

    with pytest.raises(SemanticColorMarkdownError, match="Runtime (color|chrome|dark)"):
        extract_runtime_color_policy(text)


def test_default_sync_fails_closed_when_runtime_policy_is_missing(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
):
    source = tmp_path / "graph.json"
    reference = tmp_path / "color-reference.md"
    source.write_text(json.dumps(_minimal_graph()), encoding="utf-8")
    reference.write_text("# Missing Policy\n", encoding="utf-8")
    monkeypatch.setattr(
        semantic_color_markdown,
        "DEFAULT_COLOR_REFERENCE_PATH",
        reference,
    )

    with pytest.raises(SemanticColorMarkdownError, match="missing its typed runtime"):
        sync_semantic_colors(
            source_path=source,
            color_reference_output=reference,
            ontology_output=None,
        )


@pytest.mark.parametrize(
    "checksum_token",
    [
        "g" + "f" * 63,
        "abc123",
    ],
)
def test_custom_policy_rejects_malformed_checksum_marker(
    tmp_path: Path, checksum_token: str
):
    text = COLOR_REFERENCE.read_text(encoding="utf-8")
    policy = extract_runtime_color_policy(text)
    assert policy is not None
    valid_digest = payload_sha256(policy)
    custom = tmp_path / "custom-color-reference.md"
    custom.write_text(text.replace(valid_digest, checksum_token, 1), encoding="utf-8")

    with pytest.raises(SemanticColorMarkdownError, match="malformed SHA-256"):
        load_runtime_color_policy(custom)


def test_marker_free_custom_reference_inherits_package_policy(tmp_path: Path):
    custom = tmp_path / "cards-only.md"
    custom.write_text(
        "# Cards only\n\n## Blues\n\n### Test Blue\n- **HEX**: #123456\n",
        encoding="utf-8",
    )

    inherited = load_runtime_color_policy(custom)
    assert inherited["inheritance"]["mode"] == "package-default"
    assert inherited["schema_version"] == "design-ontology-harness/runtime-color-policy-v1"


def test_normal_custom_policy_block_loads_without_inheritance(tmp_path: Path):
    custom = tmp_path / "self-contained.md"
    custom.write_text(COLOR_REFERENCE.read_text(encoding="utf-8"), encoding="utf-8")

    loaded = load_runtime_color_policy(custom)
    assert loaded == load_runtime_color_policy()
    assert "inheritance" not in loaded


@pytest.mark.parametrize(
    "partial",
    [
        "<!-- design-ontology-runtime-color-policy:end -->",
        "```design-ontology-runtime-color-policy+json",
    ],
)
def test_partial_runtime_policy_namespace_never_falls_back(
    tmp_path: Path, partial: str
):
    custom = tmp_path / "partial-policy.md"
    custom.write_text(f"# Broken policy\n\n{partial}\n", encoding="utf-8")

    with pytest.raises(SemanticColorMarkdownError, match="namespace is present"):
        load_runtime_color_policy(custom)


def test_card_provenance_category_alignment_and_local_extension_topology():
    ontology, parsed = load_ontology_from_color_reference(COLOR_REFERENCE)
    cards = {item["name"]: item for item in parsed["colors"]}
    assert cards["Hunter Green"]["family"] == "Natural Greens"
    assert cards["Teal Blue"]["family"] == "Natural Blues"
    assert cards["Rose Quartz"]["semantic_node_id"] == (
        "color-keyword-pantone-coy-2016-rose-quartz"
    )
    assert cards["Rose Quartz"]["ontology_category"] == "Pantone Color of the Year"
    assert cards["Creamsicle"]["source_citations"] == ["2", "3"]
    assert cards["Buttercream"]["source_citations"] == ["3", "4"]
    assert all(item["source_reference_ids"] for item in parsed["colors"])
    assert all(item["source_provenance"] for item in parsed["colors"])

    nodes = {node["id"]: node for node in ontology["nodes"]}
    assert "ref-docs-color-reference-local-extensions" in nodes
    for node_id, topic_id in (
        ("color-keyword-local-dark-salmon", "topic-color-orange-spectrum"),
        ("color-keyword-local-blanched-almond", "topic-color-yellow-spectrum"),
    ):
        assert nodes[node_id]["properties"]["source_type"] == "markdown-local-extension"
        outgoing = [
            edge
            for edge in ontology["edges"]
            if edge["from"]["id"] == node_id
        ]
        assert any(edge["relation"] == "cites" for edge in outgoing)
        assert any(
            edge["relation"] == "belongs_to_topic" and edge["to"]["id"] == topic_id
            for edge in outgoing
        )
    assert ontology["node_count"] == 361
    assert ontology["edge_count"] == 1235
