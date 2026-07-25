from __future__ import annotations

import hashlib
import json
import subprocess
import sys
from pathlib import Path

from PIL import Image

from design_ontology_harness.adapters import load_preset_bundle
from design_ontology_harness.adapters.base import implementation_contract
from design_ontology_harness.implementation_linter import lint_implementation
from design_ontology_harness.synthesis import (
    APP_ICON_IDENTITY_POLICY,
    COLOR_MODE_PARITY_POLICY,
    COMMERCIAL_PRODUCT_REALISM_POLICY,
    HTML_PROTOTYPE_CONTRACT_POLICY,
    ICON_REFACTOR_POLICY,
    MOCKUP_VISUAL_SUBSTANCE_POLICY,
    REFERENCE_ABSORPTION_SCOPE,
    RESPONSIVE_RESILIENCE_POLICY,
    VISUAL_ASSET_MEDIUM_SELECTION_POLICY,
)


REPO_ROOT = Path(__file__).resolve().parent.parent


def _write_visual_asset_manifest(tmp_path: Path, *, status: str = "integrated") -> Path:
    generation_run_id = "019e2de5-941b-7971-98e3-6ed84372f36b"
    candidate_id = "ig_05e8553d24da513b016a07d77edabc8191bf7569ff5368de06"
    asset_path = tmp_path / "assets" / "hero.png"
    asset_path.parent.mkdir(parents=True, exist_ok=True)
    Image.new("RGB", (1600, 900), "#315c4b").save(asset_path)
    original_path = (
        tmp_path
        / ".codex"
        / "generated_images"
        / generation_run_id
        / f"{candidate_id}.png"
    )
    original_path.parent.mkdir(parents=True, exist_ok=True)
    Image.new("RGB", (1600, 900), "#315c4b").save(original_path)
    manifest_path = tmp_path / "public" / "generated" / "design-system" / "manifest.json"
    manifest_path.parent.mkdir(parents=True, exist_ok=True)
    prompt_slot = {
        "id": "visual-asset:hero",
        "slot": "hero-image",
        "label": "Evidence hero",
        "intended_for": ["component:evidence-hero"],
        "aspect_ratios": ["16:9"],
        "candidate_count": 2,
        "prompt": "Credible evidence review scene",
        "review_criteria": ["domain subject is clear"],
    }
    prompt_packet = {
        "schema_version": "design-ontology.visual-prompt-packet.v1",
        "project": "fieldnote",
        "brand": "Fieldnote",
        "slots": [prompt_slot],
    }
    packet_path = manifest_path.parent / "imagegen-prompt-packet.json"
    packet_path.write_text(json.dumps(prompt_packet), encoding="utf-8")
    packet_sha = hashlib.sha256(packet_path.read_bytes()).hexdigest()
    slot_sha = hashlib.sha256(
        json.dumps(
            prompt_slot,
            ensure_ascii=False,
            sort_keys=True,
            separators=(",", ":"),
        ).encode("utf-8")
    ).hexdigest()
    inventory_path = tmp_path / "build" / "system" / "blueprint" / "component_inventory.json"
    specs_path = tmp_path / "build" / "system" / "components" / "component_specs.json"
    inventory_path.parent.mkdir(parents=True, exist_ok=True)
    specs_path.parent.mkdir(parents=True, exist_ok=True)
    inventory_path.write_text(json.dumps({"components": [{"name": "evidence-hero"}]}), encoding="utf-8")
    specs_path.write_text(
        json.dumps({"specs": [{"name": "evidence-hero", "contract_status": "complete"}]}),
        encoding="utf-8",
    )
    manifest_path.write_text(json.dumps({
        "schema_version": "visual-asset-manifest/v2",
        "project": "fieldnote",
        "brand": "Fieldnote",
        "generator": {"id": "image-model:codex-imagegen", "api_fallback": "disabled"},
        "source_session": {"id": generation_run_id, "default_directory": str(original_path.parent), "preserve_originals": True},
        "prompt_packet": "imagegen-prompt-packet.json",
        "prompt_packet_sha256": packet_sha,
        "assets": [{
            "id": "visual-asset:hero",
            "label": "Evidence hero",
            "slot": "hero-image",
            "status": status,
            "asset_path": "assets/hero.png",
            "original_png_path": str(original_path),
            "original_sha256": hashlib.sha256(original_path.read_bytes()).hexdigest(),
            "format": "png",
            "dimensions": {"width": 1600, "height": 900, "aspect_ratio": "16:9"},
            "size_kb": round(asset_path.stat().st_size / 1024, 2),
            "sha256": hashlib.sha256(asset_path.read_bytes()).hexdigest(),
            "intended_for": ["component:evidence-hero"],
            "alt_text": "현장 증거 검토 장면",
            "prompt_summary": "Credible evidence review scene",
            "selection_reason": "도메인 정보가 가장 선명한 후보",
            "reviewed_criteria": ["domain subject is clear"],
            "review_criteria": ["domain subject is clear"],
            "review_gate_version": "visual-asset-review/v1",
            "generation_provenance_version": "visual-asset-generation-provenance/v1",
            "generator": "image-model:codex-imagegen",
            "generation_run_id": generation_run_id,
            "candidate_id": candidate_id,
            "prompt_packet_slot_id": "visual-asset:hero",
            "prompt_packet_sha256": packet_sha,
            "prompt_slot_sha256": slot_sha,
            "runtime_integration": {
                "gate": "implementation-reference/v1",
                "references": [{"path": "index.html", "line": 1, "kind": "img"}],
            },
        }],
    }), encoding="utf-8")
    return manifest_path


def test_token_bound_css_passes(tmp_path: Path):
    (tmp_path / "design-system").mkdir()
    (tmp_path / "design-system" / "tokens.css").write_text(
        ":root { --ds-color-primary: #0071A8; --ds-radius-sm: 4px; }\n",
        encoding="utf-8",
    )
    (tmp_path / "styles.css").write_text(
        """
        .panel {
          color: var(--ds-color-ink);
          background: color-mix(in srgb, var(--ds-color-surface-tint) 24%, var(--ds-color-surface));
          border-color: var(--ds-color-border);
          border-radius: var(--ds-radius-sm);
          font-family: var(--ds-font-ko);
        }
        .dot { border-radius: 999px; }
        """,
        encoding="utf-8",
    )

    report = lint_implementation(tmp_path)

    assert report.ok
    assert report.checked_files == ["styles.css"]


def test_flags_hardcoded_visual_values(tmp_path: Path):
    (tmp_path / "styles.css").write_text(
        """
        .bad {
          color: #123456;
          background: rgb(10, 20, 30);
          border-color: teal;
          border-radius: 8px;
          font-family: Inter, sans-serif;
        }
        """,
        encoding="utf-8",
    )

    report = lint_implementation(tmp_path)
    codes = {issue.code for issue in report.issues}

    assert not report.ok
    assert {"DS001", "DS002", "DS003", "DS010", "DS020"} <= codes


def test_flags_token_bound_reference_palette_mixing(tmp_path: Path):
    (tmp_path / "styles.css").write_text(
        """
        :root {
          --chart-secondary: color-mix(in srgb, var(--ds-color-info) 52%, var(--ds-color-surface-tint));
          --sidebar-bg: color-mix(in srgb, var(--ds-color-info) 84%, var(--ds-color-ink) 16%);
          --panel-shadow: color-mix(in srgb, var(--ds-color-ink) 12%, transparent);
        }
        """,
        encoding="utf-8",
    )

    report = lint_implementation(tmp_path)
    codes = {issue.code for issue in report.issues}

    assert not report.ok
    assert {"DS030", "DS031"} <= codes


def test_flags_mobile_button_overflow_patterns(tmp_path: Path):
    (tmp_path / "styles.css").write_text(
        """
        .hero-actions {
          display: flex;
          flex-wrap: nowrap;
        }
        .cta-button {
          min-width: 360px;
          white-space: nowrap;
        }
        .page-shell {
          width: 100vw;
        }
        """,
        encoding="utf-8",
    )

    report = lint_implementation(tmp_path)
    codes = {issue.code for issue in report.issues}

    assert not report.ok
    assert {"DS040", "DS041", "DS042", "DS043"} <= codes


def test_flags_tailwind_mobile_button_overflow_patterns(tmp_path: Path):
    (tmp_path / "Button.tsx").write_text(
        """
        export function Button() {
          return <button className="cta-button min-w-[360px] whitespace-nowrap">긴 CTA 버튼 문구</button>
        }
        export function Shell() {
          return <main className="w-screen px-6" />
        }
        """,
        encoding="utf-8",
    )

    report = lint_implementation(tmp_path)
    codes = {issue.code for issue in report.issues}

    assert not report.ok
    assert {"DS040", "DS041", "DS043"} <= codes


def test_flags_emoji_used_as_ui_affordance(tmp_path: Path):
    (tmp_path / "Cards.tsx").write_text(
        """
        export function Actions() {
          return (
            <section>
              <button className="primary-button">🚀 시작하기</button>
              <article className="feature-card"><span className="feature-icon">🔥</span><h3>자동 분석</h3></article>
              <span className="status-badge">✅ 완료</span>
            </section>
          )
        }
        """,
        encoding="utf-8",
    )

    report = lint_implementation(tmp_path)
    codes = {issue.code for issue in report.issues}

    assert not report.ok
    assert "DS050" in codes


def test_flags_homogeneous_card_wall_risk(tmp_path: Path):
    (tmp_path / "index.html").write_text(
        """
        <main class="card-grid">
          <section class="hero-card"></section>
          <article class="metric-card"></article>
          <article class="metric-card"></article>
          <article class="feature-card"></article>
          <article class="feature-card"></article>
          <aside class="summary-panel"></aside>
          <aside class="detail-panel"></aside>
        </main>
        """,
        encoding="utf-8",
    )
    (tmp_path / "styles.css").write_text(
        """
        .hero-card, .metric-card, .feature-card, .summary-panel, .detail-panel {
          border: 1px solid var(--ds-color-border);
          border-radius: var(--ds-radius-md);
          background: var(--ds-color-surface);
        }
        .card-grid { display: grid; gap: 12px; }
        """,
        encoding="utf-8",
    )

    report = lint_implementation(tmp_path)
    codes = {issue.code for issue in report.issues}

    assert not report.ok
    assert "DS070" in codes


def test_flags_ad_hoc_node_link_placeholder_graph(tmp_path: Path):
    (tmp_path / "index.html").write_text(
        """
        <section class="trace-canvas" aria-label="근거 연결 미니맵">
          <span class="trace-node main">Answer</span>
          <span class="trace-node top">CH-078</span>
          <span class="trace-node law-node">하도급법</span>
          <i class="trace-line line-a"></i>
          <i class="trace-line line-b"></i>
        </section>
        """,
        encoding="utf-8",
    )
    (tmp_path / "styles.css").write_text(
        """
        .trace-canvas { position: relative; }
        .trace-node { position: absolute; border: var(--app-border); }
        .trace-line { position: absolute; height: 2px; transform: rotate(18deg); }
        """,
        encoding="utf-8",
    )

    report = lint_implementation(tmp_path)
    codes = {issue.code for issue in report.issues}

    assert not report.ok
    assert "DS082" in codes


def test_flags_freehand_svg_connector_graph_with_positioned_nodes(tmp_path: Path):
    (tmp_path / "index.html").write_text(
        """
        <section class="canvas-plane" aria-label="온보딩 그래프">
          <svg class="wires" viewBox="0 0 900 540">
            <path d="M165 154 C260 154 260 250 360 250" />
            <path d="M540 250 C650 250 650 156 760 156" />
            <path d="M540 250 C650 250 650 380 760 380" />
          </svg>
          <div class="flow-node start" style="left:58px;top:112px">시작</div>
          <div class="flow-node active" style="left:350px;top:208px">KYC 확인</div>
          <div class="flow-node" style="left:640px;top:114px">자동 승인</div>
        </section>
        """,
        encoding="utf-8",
    )
    (tmp_path / "styles.css").write_text(
        """
        .canvas-plane { position: relative; }
        .wires { position: absolute; inset: 0; }
        .flow-node { position: absolute; border: var(--app-border); }
        """,
        encoding="utf-8",
    )

    report = lint_implementation(tmp_path)
    codes = {issue.code for issue in report.issues}

    assert not report.ok
    assert "DS083" in codes


def test_flags_freehand_svg_connector_graph_with_arrowheads_but_no_edge_model(tmp_path: Path):
    (tmp_path / "index.html").write_text(
        """
        <section class="canvas-plane" aria-label="온보딩 그래프">
          <svg class="connector-layer" viewBox="0 0 900 540" aria-label="온보딩 흐름">
            <title>온보딩 흐름</title>
            <defs>
              <marker id="arrow" viewBox="0 0 10 10" refX="8" refY="5">
                <path d="M0 0 10 5 0 10Z" />
              </marker>
            </defs>
            <path d="M165 154 C260 154 260 250 360 250" marker-end="url(#arrow)" />
            <path d="M540 250 C650 250 650 156 760 156" marker-end="url(#arrow)" />
            <text x="272" y="205">가입 요청</text>
          </svg>
          <div class="flow-node start" style="left:58px;top:112px">시작</div>
          <div class="flow-node active" style="left:350px;top:208px">KYC 확인</div>
          <div class="flow-node" style="left:640px;top:114px">자동 승인</div>
        </section>
        """,
        encoding="utf-8",
    )

    report = lint_implementation(tmp_path)
    codes = {issue.code for issue in report.issues}

    assert not report.ok
    assert "DS083" in codes


def test_allows_semantic_svg_workflow_graph(tmp_path: Path):
    (tmp_path / "index.html").write_text(
        """
        <section class="canvas-plane" aria-label="온보딩 그래프">
          <svg class="workflow-graph" viewBox="0 0 900 540" role="img" aria-labelledby="workflow-title workflow-desc">
            <title id="workflow-title">온보딩 정책 워크플로</title>
            <desc id="workflow-desc">시작은 KYC 확인으로 이동하고 위험 등급에 따라 분기된다.</desc>
            <defs>
              <marker id="edge-arrow" viewBox="0 0 10 10" refX="8" refY="5">
                <path d="M0 0 10 5 0 10Z" />
              </marker>
            </defs>
            <path data-edge-id="start-to-kyc" data-from="start" data-to="kyc" d="M240 208 C292 208 308 258 360 258" marker-end="url(#edge-arrow)" />
            <text x="272" y="205">가입 요청</text>
            <g data-node-id="start"><rect width="180" height="76" /><text>시작</text></g>
            <g data-node-id="kyc"><rect width="180" height="76" /><text>KYC 확인</text></g>
          </svg>
        </section>
        """,
        encoding="utf-8",
    )

    report = lint_implementation(tmp_path)
    codes = {issue.code for issue in report.issues}

    assert "DS082" not in codes
    assert "DS083" not in codes


def test_flags_complex_mock_surface_without_product_contract(tmp_path: Path):
    (tmp_path / "index.html").write_text(
        """
        <main>
          <section class="placeholder-chart mock-chart">
            <div class="bar"></div>
            <div class="bar tall"></div>
            <div class="bar short"></div>
          </section>
        </main>
        """,
        encoding="utf-8",
    )

    report = lint_implementation(tmp_path)
    codes = {issue.code for issue in report.issues}

    assert not report.ok
    assert "DS084" in codes


def test_allows_complex_surface_with_runtime_model_source_and_state(tmp_path: Path):
    (tmp_path / "index.html").write_text(
        """
        <main>
          <section
            class="chart-surface"
            data-runtime-surface="chart-layer"
            data-model="revenue-series"
            data-source="sample:billing-ledger"
            data-state="selected"
          >
            <div class="bar" data-item-id="q1" data-value="42" data-label="1분기"></div>
            <div class="bar" data-item-id="q2" data-value="68" data-label="2분기"></div>
          </section>
        </main>
        """,
        encoding="utf-8",
    )

    report = lint_implementation(tmp_path)
    codes = {issue.code for issue in report.issues}

    assert "DS084" not in codes


def test_flags_marked_html_prototype_without_state_set(tmp_path: Path):
    (tmp_path / "index.html").write_text(
        """
        <main data-product-prototype="ops-console">
          <section
            class="chart-surface"
            data-runtime-surface="chart-layer"
            data-model="incident-volume"
            data-source="sample:incidents"
          >
            <div class="bar" data-item-id="p1" data-value="12">12</div>
          </section>
          <button>필터</button>
          <button>승인</button>
          <button>내보내기</button>
          <button>동기화</button>
        </main>
        """,
        encoding="utf-8",
    )

    report = lint_implementation(tmp_path)
    codes = {issue.code for issue in report.issues}

    assert not report.ok
    assert "DS085" in codes


def test_allows_marked_html_prototype_with_state_set(tmp_path: Path):
    (tmp_path / "index.html").write_text(
        """
        <main
          data-product-prototype="ops-console"
          data-prototype-state-set="default,selected,loading,empty,error"
        >
          <section
            class="chart-surface"
            data-runtime-surface="chart-layer"
            data-model="incident-volume"
            data-source="sample:incidents"
            data-state="selected"
          >
            <div class="bar" data-item-id="p1" data-value="12">12</div>
          </section>
        </main>
        """,
        encoding="utf-8",
    )
    (tmp_path / "styles.css").write_text(
        """
        .chart-surface {
          display: grid;
          grid-template-columns: minmax(0, 1fr);
          gap: 12px;
          padding: 16px;
          border: 1px solid var(--ds-color-border);
          border-radius: var(--ds-radius-md);
          background: var(--ds-color-surface);
          color: var(--ds-color-ink);
        }
        """,
        encoding="utf-8",
    )

    report = lint_implementation(tmp_path)
    codes = {issue.code for issue in report.issues}

    assert "DS085" not in codes
    assert "DS086" not in codes


def test_flags_metadata_only_html_prototype_without_surface_styling(tmp_path: Path):
    (tmp_path / "index.html").write_text(
        """
        <main
          data-product-prototype="ops-console"
          data-prototype-state-set="default,selected,loading,empty,error"
        >
          <section
            class="chart-surface"
            data-runtime-surface="chart-layer"
            data-model="incident-volume"
            data-source="sample:incidents"
            data-state="selected"
          >
            <h1>사고 처리량</h1>
            <div data-item-id="p1" data-value="12">12</div>
            <div data-item-id="p2" data-value="24">24</div>
          </section>
          <button data-state="selected">필터</button>
          <button data-state="pending">승인</button>
        </main>
        """,
        encoding="utf-8",
    )

    report = lint_implementation(tmp_path)
    codes = {issue.code for issue in report.issues}

    assert not report.ok
    assert "DS084" not in codes
    assert "DS085" not in codes
    assert "DS086" in codes


def test_allows_evidence_ledger_instead_of_node_link_placeholder(tmp_path: Path):
    (tmp_path / "index.html").write_text(
        """
        <section class="evidence-ledger" aria-label="답변, chunk, 법령 검증 ledger">
          <div class="ledger-row ledger-head">
            <span>검증 항목</span><span>의결서 chunk</span><span>법령 보강</span><span>상태</span>
          </div>
          <div class="ledger-row">
            <strong>기술자료 제공 요구</strong><span>DOC-066cf416-CH-078</span><span>하도급법</span><mark>원문 확인</mark>
          </div>
        </section>
        """,
        encoding="utf-8",
    )
    (tmp_path / "styles.css").write_text(
        """
        .evidence-ledger { display: grid; border: var(--app-border); }
        .ledger-row { display: grid; grid-template-columns: 1fr 1fr 1fr auto; }
        """,
        encoding="utf-8",
    )

    report = lint_implementation(tmp_path)
    codes = {issue.code for issue in report.issues}

    assert "DS082" not in codes


def test_flags_icon_starved_interactive_surface(tmp_path: Path):
    (tmp_path / "design-system").mkdir()
    (tmp_path / "index.html").write_text(
        """
        <main>
          <nav><button>저장</button><button>공유</button></nav>
          <section class="filter-toolbar">
            <button class="filter-chip">아침</button>
            <button class="filter-chip">저녁</button>
            <button class="status-badge">활성</button>
            <button class="primary-action">장소 기록</button>
          </section>
        </main>
        """,
        encoding="utf-8",
    )

    report = lint_implementation(tmp_path)
    codes = {issue.code for issue in report.issues}

    assert not report.ok
    assert "DS071" in codes


def test_flags_undeclared_handmade_icon_sprite(tmp_path: Path):
    (tmp_path / "design-system").mkdir()
    (tmp_path / "design-system" / "brand_profile.json").write_text(
        '{"product_summary": "콘텐츠 앱"}',
        encoding="utf-8",
    )
    (tmp_path / "index.html").write_text(
        """
        <svg class="icon-sprite" aria-hidden="true">
          <symbol id="icon-home" viewBox="0 0 24 24"><path d="M3 9h18v12H3z" /></symbol>
          <symbol id="icon-search" viewBox="0 0 24 24"><path d="M10 10h8v8h-8z" /></symbol>
          <symbol id="icon-user" viewBox="0 0 24 24"><path d="M12 4h1v1h-1z" /></symbol>
          <symbol id="icon-bell" viewBox="0 0 24 24"><path d="M5 5h14v14H5z" /></symbol>
        </svg>
        <nav>
          <button class="nav-item"><svg class="icon"><use href="#icon-home" /></svg>홈</button>
          <button class="nav-item"><svg class="icon"><use href="#icon-search" /></svg>검색</button>
        </nav>
        """,
        encoding="utf-8",
    )

    report = lint_implementation(tmp_path)
    codes = {issue.code for issue in report.issues}

    assert not report.ok
    assert "DS080" in codes


def test_allows_declared_lucide_icon_sprite(tmp_path: Path):
    (tmp_path / "design-system").mkdir()
    (tmp_path / "design-system" / "brand_profile.json").write_text(
        '{"product_summary": "콘텐츠 앱"}',
        encoding="utf-8",
    )
    (tmp_path / "index.html").write_text(
        """
        <svg class="icon-sprite" data-icon-set="lucide" aria-hidden="true">
          <symbol id="icon-home" viewBox="0 0 24 24"><path d="M3 9h18v12H3z" /></symbol>
          <symbol id="icon-search" viewBox="0 0 24 24"><path d="M10 10h8v8h-8z" /></symbol>
          <symbol id="icon-user" viewBox="0 0 24 24"><path d="M12 4h1v1h-1z" /></symbol>
          <symbol id="icon-bell" viewBox="0 0 24 24"><path d="M5 5h14v14H5z" /></symbol>
        </svg>
        <nav>
          <button class="nav-item"><svg class="icon"><use href="#icon-home" /></svg>홈</button>
          <button class="nav-item"><svg class="icon"><use href="#icon-search" /></svg>검색</button>
        </nav>
        """,
        encoding="utf-8",
    )

    report = lint_implementation(tmp_path)
    codes = {issue.code for issue in report.issues}

    assert "DS080" not in codes


def test_flags_missing_domain_visual_substance(tmp_path: Path):
    (tmp_path / "design-system").mkdir()
    (tmp_path / "design-system" / "brand_profile.json").write_text(
        '{"product_summary": "서울 장소와 골목을 추천하는 지도 앱"}',
        encoding="utf-8",
    )
    (tmp_path / "index.html").write_text(
        """
        <main>
          <button class="filter-chip"><svg class="icon"><use href="#icon-clock" /></svg>아침</button>
          <button class="filter-chip"><svg class="icon"><use href="#icon-clock" /></svg>저녁</button>
          <button class="primary-action"><svg class="icon"><use href="#icon-plus" /></svg>장소 기록</button>
          <section class="result-list">
            <div class="place-row">서촌 골목</div>
            <div class="place-row">을지로 골목</div>
          </section>
        </main>
        """,
        encoding="utf-8",
    )

    report = lint_implementation(tmp_path)
    codes = {issue.code for issue in report.issues}

    assert not report.ok
    assert "DS072" in codes


def test_flags_low_information_inline_domain_svg(tmp_path: Path):
    (tmp_path / "design-system").mkdir()
    (tmp_path / "design-system" / "brand_profile.json").write_text(
        '{"product_summary": "서울 장소와 골목을 추천하는 지도 앱"}',
        encoding="utf-8",
    )
    (tmp_path / "index.html").write_text(
        """
        <main>
          <section class="map-visual">
            <svg class="alley-map" viewBox="0 0 200 120" role="img" aria-label="골목 그림">
              <path d="M10 90h180" />
              <path d="M24 32h50v58H24Z" />
              <path d="M126 24h44v66h-44Z" />
              <circle cx="92" cy="58" r="12" />
            </svg>
          </section>
          <figure class="place-illustration">서촌 장소</figure>
        </main>
        """,
        encoding="utf-8",
    )

    report = lint_implementation(tmp_path)
    codes = {issue.code for issue in report.issues}

    assert not report.ok
    assert "DS073" in codes


def test_allows_semantic_inline_domain_svg(tmp_path: Path):
    (tmp_path / "design-system").mkdir()
    (tmp_path / "design-system" / "brand_profile.json").write_text(
        '{"product_summary": "서울 장소와 골목을 추천하는 지도 앱"}',
        encoding="utf-8",
    )
    (tmp_path / "index.html").write_text(
        """
        <main>
          <section class="map-visual">
            <svg class="alley-map" viewBox="0 0 200 120" role="img" aria-labelledby="mapTitle mapDesc">
              <title id="mapTitle">서촌 산책선 지도</title>
              <desc id="mapDesc">서점, 찻집, 계단을 감각 신호와 연결한 지도</desc>
              <g data-subject="paper-alley">
                <path d="M10 90h180" />
                <path d="M24 32h50v58H24Z" />
                <path d="M126 24h44v66h-44Z" />
                <circle cx="92" cy="58" r="12" />
                <text x="24" y="28">서점 골목</text>
              </g>
            </svg>
          </section>
          <figure class="place-illustration">서촌 장소</figure>
        </main>
        """,
        encoding="utf-8",
    )

    report = lint_implementation(tmp_path)
    codes = {issue.code for issue in report.issues}

    assert "DS073" not in codes


def test_flags_ad_hoc_sketch_domain_visual(tmp_path: Path):
    (tmp_path / "design-system").mkdir()
    (tmp_path / "design-system" / "brand_profile.json").write_text(
        '{"product_summary": "서울 장소와 골목을 추천하는 지도 앱"}',
        encoding="utf-8",
    )
    (tmp_path / "index.html").write_text(
        """
        <main>
          <section class="map-visual">
            <svg class="place-sketch" viewBox="0 0 200 120" role="img" aria-labelledby="mapTitle mapDesc">
              <title id="mapTitle">골목 그림</title>
              <desc id="mapDesc">즉흥 스케치</desc>
              <g data-subject="alley">
                <path d="M10 90h180" />
                <path d="M24 32h50v58H24Z" />
                <path d="M126 24h44v66h-44Z" />
                <circle cx="92" cy="58" r="12" />
                <text x="24" y="28">서점 골목</text>
              </g>
            </svg>
          </section>
          <figure class="place-visual">서촌 장소</figure>
        </main>
        """,
        encoding="utf-8",
    )

    report = lint_implementation(tmp_path)
    codes = {issue.code for issue in report.issues}

    assert not report.ok
    assert "DS074" in codes


def test_flags_wrong_medium_svg_for_comic_media_slot(tmp_path: Path):
    (tmp_path / "design-system").mkdir()
    (tmp_path / "design-system" / "brand_profile.json").write_text(
        '{"product_summary": "모바일 만화 잡지 앱", "visual_keywords": ["comic", "webtoon", "cover"]}',
        encoding="utf-8",
    )
    (tmp_path / "index.html").write_text(
        """
        <main>
          <section class="issue-cover comic-cover">
            <img class="cover-visual" src="./assets/cover-lunar.svg" alt="만화 잡지 표지" />
          </section>
          <section class="panel-preview">
            <img src="./assets/panel-strip.svg" alt="웹툰 컷 미리보기" />
          </section>
        </main>
        """,
        encoding="utf-8",
    )

    report = lint_implementation(tmp_path)
    codes = {issue.code for issue in report.issues}

    assert not report.ok
    assert "DS079" in codes


def test_allows_svg_for_identity_and_diagram_slots(tmp_path: Path):
    (tmp_path / "design-system").mkdir()
    (tmp_path / "design-system" / "brand_profile.json").write_text(
        '{"product_summary": "모바일 만화 잡지 앱", "visual_keywords": ["comic", "webtoon", "cover"]}',
        encoding="utf-8",
    )
    (tmp_path / "index.html").write_text(
        """
        <main>
          <img class="app-icon" src="./assets/app-icon.svg" alt="앱 아이콘" />
          <img class="reading-map diagram" src="./assets/episode-map.svg" alt="회차 흐름 다이어그램" />
          <article class="comic-cover">
            <img class="cover-visual" src="./assets/cover-lunar.png" alt="만화 잡지 표지" />
          </article>
        </main>
        """,
        encoding="utf-8",
    )

    report = lint_implementation(tmp_path)
    codes = {issue.code for issue in report.issues}

    assert "DS079" not in codes


def test_flags_svg_when_raster_only_directive_is_active(tmp_path: Path):
    (tmp_path / "index.html").write_text(
        """
        <html>
          <head>
            <meta name="visual-asset-medium" content="raster-only; no-svg; png-webp-jpeg-assets" />
            <link rel="icon" href="./assets/app-icon.svg" type="image/svg+xml" />
          </head>
          <body>
            <svg class="icon-sprite"><symbol id="icon-home"></symbol></svg>
            <img class="agent-avatar" src="./assets/agent.svg" alt="AI avatar" />
          </body>
        </html>
        """,
        encoding="utf-8",
    )

    report = lint_implementation(tmp_path)
    codes = {issue.code for issue in report.issues}

    assert not report.ok
    assert "DS081" in codes


def test_allows_png_assets_when_raster_only_directive_is_active(tmp_path: Path):
    (tmp_path / "index.html").write_text(
        """
        <html>
          <head>
            <meta name="visual-asset-medium" content="raster-only; no-svg; png-webp-jpeg-assets" />
            <link rel="icon" href="./assets/app-icon.png" type="image/png" />
          </head>
          <body>
            <img class="icon" src="./assets/icons/home.png" alt="" />
            <img class="agent-avatar" src="./assets/agent.webp" alt="AI avatar" />
          </body>
        </html>
        """,
        encoding="utf-8",
    )

    report = lint_implementation(tmp_path)
    codes = {issue.code for issue in report.issues}

    assert "DS081" not in codes


def test_flags_ambiguous_mock_runtime_surface(tmp_path: Path):
    (tmp_path / "design-system").mkdir()
    (tmp_path / "design-system" / "brand_profile.json").write_text(
        '{"product_summary": "서울 장소와 골목을 추천하는 지도 앱"}',
        encoding="utf-8",
    )
    (tmp_path / "index.html").write_text(
        """
        <main>
          <section class="map-visual schematic-map">
            <div class="placeholder-map">서촌 감각 도식</div>
          </section>
          <figure class="place-visual">장소 이미지</figure>
        </main>
        """,
        encoding="utf-8",
    )

    report = lint_implementation(tmp_path)
    codes = {issue.code for issue in report.issues}

    assert not report.ok
    assert "DS075" in codes


def test_allows_declared_runtime_surface(tmp_path: Path):
    (tmp_path / "design-system").mkdir()
    (tmp_path / "design-system" / "brand_profile.json").write_text(
        '{"product_summary": "서울 장소와 골목을 추천하는 지도 앱"}',
        encoding="utf-8",
    )
    (tmp_path / "index.html").write_text(
        """
        <main>
          <section class="map-visual" data-runtime-surface="map-sdk-layer">
            <div class="real-map">서촌 지도 레이어</div>
          </section>
          <figure class="place-visual" data-runtime-surface="generated-place-photo">장소 이미지</figure>
        </main>
        """,
        encoding="utf-8",
    )

    report = lint_implementation(tmp_path)
    codes = {issue.code for issue in report.issues}

    assert "DS075" not in codes


def test_flags_media_runtime_surface_without_asset(tmp_path: Path):
    (tmp_path / "design-system").mkdir()
    (tmp_path / "design-system" / "brand_profile.json").write_text(
        '{"product_summary": "서울 장소와 골목을 추천하는 지도 앱"}',
        encoding="utf-8",
    )
    (tmp_path / "index.html").write_text(
        """
        <main>
          <section class="map-visual" data-runtime-surface="map-sdk-layer">
            <div class="real-map">서촌 지도 레이어</div>
          </section>
          <section class="place-media-surface" data-runtime-surface="place-media-evidence">
            <figure class="place-photo">패턴만 있는 장소 사진 슬롯</figure>
          </section>
        </main>
        """,
        encoding="utf-8",
    )

    report = lint_implementation(tmp_path)
    codes = {issue.code for issue in report.issues}

    assert not report.ok
    assert "DS076" in codes


def test_allows_media_runtime_surface_with_image_asset(tmp_path: Path):
    (tmp_path / "design-system").mkdir()
    (tmp_path / "design-system" / "brand_profile.json").write_text(
        '{"product_summary": "서울 장소와 골목을 추천하는 지도 앱"}',
        encoding="utf-8",
    )
    (tmp_path / "index.html").write_text(
        """
        <main>
          <section class="map-visual" data-runtime-surface="map-sdk-layer">
            <div class="real-map">서촌 지도 레이어</div>
          </section>
          <section class="place-media-surface" data-runtime-surface="place-media-evidence">
            <figure class="place-photo"><img src="./assets/place.png" alt="장소 사진" /></figure>
          </section>
        </main>
        """,
        encoding="utf-8",
    )

    report = lint_implementation(tmp_path)
    codes = {issue.code for issue in report.issues}

    assert "DS076" not in codes


def test_flags_individual_media_tile_without_asset(tmp_path: Path):
    (tmp_path / "design-system").mkdir()
    (tmp_path / "design-system" / "brand_profile.json").write_text(
        '{"product_summary": "서울 장소와 골목을 추천하는 지도 앱"}',
        encoding="utf-8",
    )
    (tmp_path / "index.html").write_text(
        """
        <main>
          <section class="place-media-surface" data-runtime-surface="place-media-evidence">
            <figure class="place-photo"><img src="./assets/place.png" alt="장소 사진" /></figure>
            <figure class="texture-card">패턴만 남은 질감 카드</figure>
          </section>
        </main>
        """,
        encoding="utf-8",
    )

    report = lint_implementation(tmp_path)
    codes = {issue.code for issue in report.issues}

    assert not report.ok
    assert "DS078" in codes


def test_allows_explicit_pending_media_tile_without_asset(tmp_path: Path):
    (tmp_path / "design-system").mkdir()
    (tmp_path / "design-system" / "brand_profile.json").write_text(
        '{"product_summary": "서울 장소와 골목을 추천하는 지도 앱"}',
        encoding="utf-8",
    )
    (tmp_path / "index.html").write_text(
        """
        <main>
          <section class="place-media-surface" data-runtime-surface="place-media-evidence">
            <figure class="place-photo"><img src="./assets/place.png" alt="장소 사진" /></figure>
            <figure class="texture-card" data-state="pending">수집 대기</figure>
          </section>
        </main>
        """,
        encoding="utf-8",
    )

    report = lint_implementation(tmp_path)
    codes = {issue.code for issue in report.issues}

    assert "DS078" not in codes


def test_runtime_raster_passes_when_file_and_integrated_manifest_match(tmp_path: Path):
    _write_visual_asset_manifest(tmp_path)
    (tmp_path / "index.html").write_text(
        '<main><img src="./assets/hero.png" alt="현장 증거 검토 장면" /></main>',
        encoding="utf-8",
    )

    report = lint_implementation(tmp_path)
    codes = {issue.code for issue in report.issues}

    assert not ({"DS087", "DS088", "DS089"} & codes)


def test_runtime_raster_fails_when_missing_or_not_integrated(tmp_path: Path):
    _write_visual_asset_manifest(tmp_path, status="accepted")
    (tmp_path / "index.html").write_text(
        '<main><img src="./assets/hero.png" alt="현장 증거 검토 장면" />'
        '<img src="./assets/missing.png" alt="누락 이미지" /></main>',
        encoding="utf-8",
    )

    report = lint_implementation(tmp_path)
    asset_issues = [issue for issue in report.issues if issue.code == "DS088"]

    assert len(asset_issues) == 2
    assert any("not registered" in issue.message for issue in asset_issues)
    assert any("does not resolve" in issue.message for issue in asset_issues)


def test_runtime_raster_fails_for_invalid_manifest_and_unused_integration(tmp_path: Path):
    manifest_path = _write_visual_asset_manifest(tmp_path)
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    manifest["assets"][0]["sha256"] = "tampered"
    manifest_path.write_text(json.dumps(manifest), encoding="utf-8")
    (tmp_path / "index.html").write_text("<main>텍스트 전용 화면</main>", encoding="utf-8")

    report = lint_implementation(tmp_path)
    codes = {issue.code for issue in report.issues}

    assert "DS087" in codes

    manifest["assets"][0]["sha256"] = hashlib.sha256((tmp_path / "assets" / "hero.png").read_bytes()).hexdigest()
    manifest_path.write_text(json.dumps(manifest), encoding="utf-8")
    report = lint_implementation(tmp_path)
    assert "DS088" in {issue.code for issue in report.issues}


def test_runtime_raster_rejects_hotlinks_agent_paths_and_empty_alt(tmp_path: Path):
    _write_visual_asset_manifest(tmp_path)
    (tmp_path / "index.html").write_text(
        """
        <main>
          <img src="./assets/hero.png" alt="" />
          <img src="https://images.example/remote.png" alt="원격 이미지" />
          <img src="$CODEX_HOME/generated_images/session/source.png" alt="로컬 원본" />
        </main>
        """,
        encoding="utf-8",
    )

    report = lint_implementation(tmp_path)
    unsafe = [issue for issue in report.issues if issue.code == "DS089"]

    assert len(unsafe) == 3


def test_flags_generic_initials_brand_mark_without_app_icon(tmp_path: Path):
    (tmp_path / "design-system").mkdir()
    (tmp_path / "index.html").write_text(
        """
        <header>
          <span class="brand-mark">AS</span>
        </header>
        """,
        encoding="utf-8",
    )

    report = lint_implementation(tmp_path)
    codes = {issue.code for issue in report.issues}

    assert not report.ok
    assert "DS077" in codes


def test_allows_wired_app_icon_brand_mark(tmp_path: Path):
    (tmp_path / "design-system").mkdir()
    (tmp_path / "index.html").write_text(
        """
        <head>
          <link rel="icon" href="./assets/app-icon.svg" type="image/svg+xml" />
          <link rel="manifest" href="./manifest.webmanifest" />
        </head>
        <header>
          <span class="brand-mark"><img src="./assets/app-icon.svg" alt="" /></span>
        </header>
        """,
        encoding="utf-8",
    )

    report = lint_implementation(tmp_path)
    codes = {issue.code for issue in report.issues}

    assert "DS077" not in codes


def test_allows_emoji_in_user_generated_content_context(tmp_path: Path):
    (tmp_path / "Post.tsx").write_text(
        """
        export function Post() {
          return <article className="blog-body">오늘 기분은 😊 입니다.</article>
        }
        export const emojiPickerOptions = ["🔥", "✅", "🚀"]
        """,
        encoding="utf-8",
    )

    report = lint_implementation(tmp_path)

    assert report.ok


def test_flags_dark_only_color_mode(tmp_path: Path):
    (tmp_path / "styles.css").write_text(
        """
        :root {
          color-scheme: dark;
          --ds-color-canvas: #061116;
        }
        """,
        encoding="utf-8",
    )

    report = lint_implementation(tmp_path)
    codes = {issue.code for issue in report.issues}

    assert not report.ok
    assert "DS060" in codes


def test_allows_light_and_dark_color_modes(tmp_path: Path):
    (tmp_path / "styles.css").write_text(
        """
        :root {
          color-scheme: light;
          --ds-color-canvas: var(--brand-light);
        }
        [data-theme="dark"] {
          color-scheme: dark;
          --ds-color-canvas: var(--brand-dark);
        }
        """,
        encoding="utf-8",
    )

    report = lint_implementation(tmp_path)
    codes = {issue.code for issue in report.issues}

    assert "DS060" not in codes


def test_excludes_design_system_but_flags_managed_blocks_in_implementation(tmp_path: Path):
    (tmp_path / "design-system").mkdir()
    (tmp_path / "design-system" / "tokens.css").write_text(
        ":root { --ds-color-primary: #0071A8; }\n",
        encoding="utf-8",
    )
    (tmp_path / "app.css").write_text(
        """
        /* design-ontology:START */
        :root { --ds-color-primary: #0071A8; }
        body { font-family: Inter, sans-serif; color: #111111; border-radius: 8px; }
        /* design-ontology:END */

        .user {
          color: var(--ds-color-ink);
          border-radius: var(--ds-radius-sm);
          font-family: var(--ds-font-body);
        }
        """,
        encoding="utf-8",
    )

    report = lint_implementation(tmp_path)
    codes = {issue.code for issue in report.issues}

    assert not report.ok
    assert "DS061" in codes
    assert "DS001" not in codes
    assert report.checked_files == ["app.css"]


def test_implementation_contract_declares_reference_scope():
    bundle = load_preset_bundle(REPO_ROOT / "presets" / "conversation-copilot--corporate-trust")
    contract = implementation_contract(bundle)

    assert "Reference Absorption Scope" in contract
    assert "Allowed from visual references" in contract
    assert "Denied from visual references" in contract
    assert "color palette" in contract
    assert "palette composition or derived secondary palettes" in contract
    assert "Feedback Promotion Rule" in contract
    assert "Do not hard-code hex/rgb/hsl colors in implementation files" in contract
    assert "tokens.css" in contract
    assert "Color Mode Parity" in contract
    assert "normal light mode and dark mode" in contract
    assert "Responsive Resilience" in contract
    assert "320, 360, 390, 430" in contract
    assert "Buttons, CTAs, tabs, chips" in contract
    assert "Emoji-to-SVG Refactor" in contract
    assert "existing icon library" in contract
    assert "Icon And Visual Affordance Coverage" in contract
    assert "Visual Evidence And Screenshot Comparison" in contract
    assert "Mock Fidelity And Runtime Representation" in contract
    assert "HTML Prototype Contract" in contract
    assert "data-runtime-surface" in contract
    assert "data-product-surface" in contract
    assert "data-prototype-state-set" in contract
    assert "metadata-only" in contract
    assert "DS086" in contract
    assert "compare-visuals" in contract
    assert "image_gen" in contract
    assert "DS070" in contract
    assert "DS071" in contract
    assert "DS072" in contract
    assert "DS073" in contract
    assert "DS074" in contract
    assert "DS075" in contract
    assert "DS076" in contract
    assert "DS077" in contract
    assert "DS078" in contract
    assert "Visual Asset Medium Selection" in contract
    assert "wrong-medium SVG narrative media" in contract
    assert "DS079" in contract
    assert "DS080" in contract
    assert "DS081" in contract
    assert "DS084" in contract
    assert "DS085" in contract
    assert "DS086" in contract
    assert "raster-only/no-SVG" in contract
    assert "uv run design-ontology lint-implementation --target-repo ." in contract


def test_reference_absorption_scope_is_structured_for_ontology():
    assert "component morphology" in REFERENCE_ABSORPTION_SCOPE["allowed"]
    assert "layout density" in REFERENCE_ABSORPTION_SCOPE["allowed"]
    assert "color palette" in REFERENCE_ABSORPTION_SCOPE["denied"]
    assert "palette composition or derived secondary palettes" in REFERENCE_ABSORPTION_SCOPE["denied"]
    assert "typography family or scale" in REFERENCE_ABSORPTION_SCOPE["denied"]
    assert "product data model" in REFERENCE_ABSORPTION_SCOPE["denied"]
    assert REFERENCE_ABSORPTION_SCOPE["failure_patterns"][0]["id"] == "token-bound-reference-palette-mixing"
    assert REFERENCE_ABSORPTION_SCOPE["promotion_policy"]["id"] == "implementation-feedback-promotion"


def test_responsive_resilience_policy_is_structured_for_ontology():
    assert RESPONSIVE_RESILIENCE_POLICY["id"] == "responsive-resilience"
    assert 320 in RESPONSIVE_RESILIENCE_POLICY["viewport_contract"]["required_widths_px"]
    assert any("Buttons" in rule for rule in RESPONSIVE_RESILIENCE_POLICY["control_rules"])
    assert any("Horizontal rails" in rule for rule in RESPONSIVE_RESILIENCE_POLICY["control_rules"])
    pattern_ids = {item["id"] for item in RESPONSIVE_RESILIENCE_POLICY["failure_patterns"]}
    assert {"mobile-control-overflow", "viewport-horizontal-overflow", "horizontal-rail-label-clipping"} <= pattern_ids
    assert "lint-implementation" in RESPONSIVE_RESILIENCE_POLICY["outputs"]


def test_commercial_product_realism_success_patterns_are_structured_for_ontology():
    assert COMMERCIAL_PRODUCT_REALISM_POLICY["id"] == "commercial-product-realism"
    pattern_ids = {item["id"] for item in COMMERCIAL_PRODUCT_REALISM_POLICY["successful_patterns"]}
    assert "same-domain-reference-before-redesign" in pattern_ids
    assert "score-ticker-as-scan-surface" in pattern_ids
    assert "national-flag-code-identity" in pattern_ids
    assert "source-ledger-and-sample-labeling" in pattern_ids
    assert "editorial-insight-side-rail" in pattern_ids
    assert "dual-mode-screenshot-qa" in pattern_ids
    assert "brand-app-icon-as-required-identity" in pattern_ids
    failure_ids = {item["id"] for item in COMMERCIAL_PRODUCT_REALISM_POLICY["failure_patterns"]}
    assert "generic-national-team-badges" in failure_ids
    assert "untokenized-domain-identity-colors" in failure_ids
    assert "unverified-redesign-screenshot" in failure_ids
    card_wall = next(item for item in COMMERCIAL_PRODUCT_REALISM_POLICY["failure_patterns"] if item["id"] == "homogeneous-card-wall")
    assert "lint-implementation DS070" in card_wall["technical_controls"]
    unverified = next(item for item in COMMERCIAL_PRODUCT_REALISM_POLICY["failure_patterns"] if item["id"] == "unverified-redesign-screenshot")
    assert "compare-visuals" in unverified["technical_controls"]
    assert "compare-visuals" in COMMERCIAL_PRODUCT_REALISM_POLICY["outputs"]


def test_color_mode_parity_policy_is_structured_for_ontology():
    assert COLOR_MODE_PARITY_POLICY["id"] == "color-mode-parity"
    assert COLOR_MODE_PARITY_POLICY["required_modes"] == ["light", "dark"]
    assert COLOR_MODE_PARITY_POLICY["default_mode"] == "light"
    pattern_ids = {item["id"] for item in COLOR_MODE_PARITY_POLICY["failure_patterns"]}
    assert {"dark-only-implementation", "theme-token-drift"} <= pattern_ids
    assert "lint-implementation" in COLOR_MODE_PARITY_POLICY["outputs"]


def test_icon_refactor_policy_is_structured_for_ontology():
    assert ICON_REFACTOR_POLICY["id"] == "emoji-to-svg-refactor"
    assert "button" in ICON_REFACTOR_POLICY["targets"]
    assert any("existing icon library" in item for item in ICON_REFACTOR_POLICY["replacement_order"])
    assert "quality_floor" in ICON_REFACTOR_POLICY
    assert "Lucide" in ICON_REFACTOR_POLICY["quality_floor"]["approved_sources"]
    failure_ids = {item["id"] for item in ICON_REFACTOR_POLICY["failure_patterns"]}
    assert {"emoji-ui-affordance", "icon-starved-control-surface", "amateur-custom-svg-icon-set"} <= failure_ids
    assert "lint-implementation" in ICON_REFACTOR_POLICY["outputs"]


def test_mockup_visual_substance_policy_flags_low_information_svg():
    failure_ids = {item["id"] for item in MOCKUP_VISUAL_SUBSTANCE_POLICY["failure_patterns"]}
    assert "low-information-inline-svg-visual" in failure_ids
    assert "amateur-ad-hoc-illustration" in failure_ids
    assert "ambiguous-mock-runtime-surface" in failure_ids
    assert "media-runtime-surface-without-asset" in failure_ids
    assert "media-tile-without-asset" in failure_ids
    low_info = next(item for item in MOCKUP_VISUAL_SUBSTANCE_POLICY["failure_patterns"] if item["id"] == "low-information-inline-svg-visual")
    assert "lint-implementation DS073" in low_info["technical_controls"]
    amateur = next(item for item in MOCKUP_VISUAL_SUBSTANCE_POLICY["failure_patterns"] if item["id"] == "amateur-ad-hoc-illustration")
    assert "lint-implementation DS074" in amateur["technical_controls"]
    assert "image_gen" in amateur["prevention"]
    ambiguous = next(item for item in MOCKUP_VISUAL_SUBSTANCE_POLICY["failure_patterns"] if item["id"] == "ambiguous-mock-runtime-surface")
    assert "lint-implementation DS075" in ambiguous["technical_controls"]
    media = next(item for item in MOCKUP_VISUAL_SUBSTANCE_POLICY["failure_patterns"] if item["id"] == "media-runtime-surface-without-asset")
    assert "lint-implementation DS076" in media["technical_controls"]
    tile = next(item for item in MOCKUP_VISUAL_SUBSTANCE_POLICY["failure_patterns"] if item["id"] == "media-tile-without-asset")
    assert "lint-implementation DS078" in tile["technical_controls"]


def test_html_prototype_contract_policy_is_structured_for_ontology():
    assert HTML_PROTOTYPE_CONTRACT_POLICY["id"] == "html-prototype-contract"
    assert "static HTML mockups" in HTML_PROTOTYPE_CONTRACT_POLICY["applies_to"]
    assert any("data-runtime-surface" in item for item in HTML_PROTOTYPE_CONTRACT_POLICY["required_contracts"])
    failure_ids = {item["id"] for item in HTML_PROTOTYPE_CONTRACT_POLICY["failure_patterns"]}
    assert "complex-mock-surface-without-contract" in failure_ids
    assert "single-state-html-prototype" in failure_ids
    assert "metadata-only-html-prototype" in failure_ids
    assert len(HTML_PROTOTYPE_CONTRACT_POLICY["improvement_loop"]) == 5
    complex_surface = next(
        item for item in HTML_PROTOTYPE_CONTRACT_POLICY["failure_patterns"]
        if item["id"] == "complex-mock-surface-without-contract"
    )
    single_state = next(
        item for item in HTML_PROTOTYPE_CONTRACT_POLICY["failure_patterns"]
        if item["id"] == "single-state-html-prototype"
    )
    metadata_only = next(
        item for item in HTML_PROTOTYPE_CONTRACT_POLICY["failure_patterns"]
        if item["id"] == "metadata-only-html-prototype"
    )
    assert "lint-implementation DS084" in complex_surface["technical_controls"]
    assert "lint-implementation DS085" in single_state["technical_controls"]
    assert "lint-implementation DS086" in metadata_only["technical_controls"]
    assert "data-prototype-state-set" in single_state["prevention"]
    assert "lint-implementation" in HTML_PROTOTYPE_CONTRACT_POLICY["outputs"]


def test_visual_asset_medium_selection_policy_is_structured_for_ontology():
    assert VISUAL_ASSET_MEDIUM_SELECTION_POLICY["id"] == "visual-asset-medium-selection"
    override_ids = {item["id"] for item in VISUAL_ASSET_MEDIUM_SELECTION_POLICY["directive_overrides"]}
    assert "user-raster-asset-directive" in override_ids
    raster_override = next(
        item for item in VISUAL_ASSET_MEDIUM_SELECTION_POLICY["directive_overrides"]
        if item["id"] == "user-raster-asset-directive"
    )
    assert raster_override["required_medium"] == "project-local raster image asset"
    assert "svg" in raster_override["denied_formats"]
    assert any("Classify the slot" in item for item in VISUAL_ASSET_MEDIUM_SELECTION_POLICY["decision_sequence"])
    family_ids = {item["id"] for item in VISUAL_ASSET_MEDIUM_SELECTION_POLICY["slot_families"]}
    assert "high-fidelity-narrative-media" in family_ids
    assert "identity-control-technical-vector" in family_ids
    assert "user-specified-raster-assets" in family_ids
    failure_ids = {item["id"] for item in VISUAL_ASSET_MEDIUM_SELECTION_POLICY["failure_patterns"]}
    assert "wrong-medium-svg-for-narrative-media" in failure_ids
    assert "user-raster-directive-svg-violation" in failure_ids
    wrong_medium = next(
        item for item in VISUAL_ASSET_MEDIUM_SELECTION_POLICY["failure_patterns"]
        if item["id"] == "wrong-medium-svg-for-narrative-media"
    )
    raster_violation = next(
        item for item in VISUAL_ASSET_MEDIUM_SELECTION_POLICY["failure_patterns"]
        if item["id"] == "user-raster-directive-svg-violation"
    )
    assert "lint-implementation DS079" in wrong_medium["technical_controls"]
    assert "lint-implementation DS081" in raster_violation["technical_controls"]
    assert "system_ontology.json" in VISUAL_ASSET_MEDIUM_SELECTION_POLICY["outputs"]


def test_app_icon_identity_policy_is_structured_for_ontology():
    assert APP_ICON_IDENTITY_POLICY["id"] == "brand-app-icon-identity"
    assert APP_ICON_IDENTITY_POLICY["required_assets"][0]["id"] == "identity-asset:app-icon"
    assert "favicon" in APP_ICON_IDENTITY_POLICY["required_assets"][0]["targets"]
    assert APP_ICON_IDENTITY_POLICY["failure_patterns"][0]["id"] == "generic-initials-app-icon"
    assert "lint-implementation DS077" in APP_ICON_IDENTITY_POLICY["failure_patterns"][0]["technical_controls"]
    failure_ids = {item["id"] for item in APP_ICON_IDENTITY_POLICY["failure_patterns"]}
    assert "low-quality-app-icon-identity" in failure_ids
    assert "system_ontology.json" in APP_ICON_IDENTITY_POLICY["outputs"]


def test_cli_exits_nonzero_on_implementation_violation(tmp_path: Path):
    (tmp_path / "styles.css").write_text(
        ".bad { color: #123456; }\n",
        encoding="utf-8",
    )

    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "design_ontology_harness.cli",
            "lint-implementation",
            "--target-repo",
            str(tmp_path),
        ],
        cwd=REPO_ROOT,
        text=True,
        capture_output=True,
        check=False,
    )

    assert result.returncode == 1
    assert "DS001" in result.stdout
