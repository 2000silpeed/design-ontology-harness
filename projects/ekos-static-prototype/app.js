const fixturePaths = {
  workflows: "./fixtures/workflows.json",
  failed: "./fixtures/source-package-failed.json",
  passed: "./fixtures/source-package-passed.json",
  decision: "./fixtures/decision-report-delivery-delay.json",
  trace: "./fixtures/evidence-trace-delivery-delay.json",
  review: "./fixtures/review-request.json"
};

const state = {
  fixtures: {}
};

document.addEventListener("DOMContentLoaded", async () => {
  await loadFixtures();
  renderWorkflows();
  renderSourceTables();
  renderMissingSources();
  renderDecisionReport();
  renderEvidenceTrace();
  renderReviewRequest();
  bindNavigation();
  refreshIcons();
});

async function loadFixtures() {
  const entries = await Promise.all(
    Object.entries(fixturePaths).map(async ([key, path]) => {
      const response = await fetch(path);
      if (!response.ok) {
        throw new Error(`Unable to load fixture: ${path}`);
      }
      return [key, await response.json()];
    })
  );
  state.fixtures = Object.fromEntries(entries);
}

function bindNavigation() {
  document.querySelectorAll("[data-go]").forEach((button) => {
    button.addEventListener("click", () => {
      const target = button.getAttribute("data-go");
      if (target) {
        setScreen(target);
      }
    });
  });
}

function setScreen(screenName) {
  document.querySelectorAll(".screen").forEach((screen) => {
    screen.classList.toggle("active", screen.dataset.screen === screenName);
  });

  document.querySelectorAll(".nav-item").forEach((item) => {
    item.classList.toggle("active", item.dataset.go === screenName);
  });

  document.body.dataset.state = screenName;
  window.scrollTo({ top: 0, behavior: "smooth" });
  refreshIcons();
}

function renderWorkflows() {
  const grid = document.querySelector("#workflow-grid");
  const workflows = state.fixtures.workflows.workflows;

  grid.innerHTML = workflows
    .map((workflow) => {
      const statusClass = normalizeStatusClass(workflow.status);
      const disabled = workflow.status === "configured" ? "" : "disabled";
      const cta = workflow.status === "configured" ? "검토 시작" : "준비 중";
      const futureClass = workflow.status === "configured" ? "" : "future";

      return `
        <article class="workflow-card ${futureClass}" data-model="workflow" data-item-id="${escapeHtml(workflow.workflow_id)}">
          <div>
            <p class="eyebrow">${escapeHtml(workflow.category_label || workflow.workflow_id)}</p>
            <h3>${escapeHtml(workflow.name)}</h3>
            <p>${escapeHtml(workflow.description)}</p>
          </div>
          <dl class="workflow-meta">
            <div><dt>필요 데이터</dt><dd>${workflow.required_source_package.length}개 항목</dd></div>
            <div><dt>업무 담당</dt><dd>${escapeHtml(workflow.process_owner)}</dd></div>
            <div><dt>결과</dt><dd>${escapeHtml(workflow.result_summary)}</dd></div>
          </dl>
          <div class="workflow-card-footer">
            <span class="status-badge ${statusClass}">${escapeHtml(workflow.status_label)}</span>
            <button class="secondary-button" type="button" data-go="case-input" ${disabled}>
              <i data-lucide="arrow-right" aria-hidden="true"></i>
              ${cta}
            </button>
          </div>
        </article>
      `;
    })
    .join("");

  bindNavigation();
}

function renderSourceTables() {
  renderAliasRows("#failed-source-table", state.fixtures.failed.aliases);
  renderAliasRows("#passed-source-table", state.fixtures.passed.aliases);
}

function renderAliasRows(selector, aliases) {
  const target = document.querySelector(selector);
  target.innerHTML = aliases
    .map((alias) => {
      const resultClass = normalizeStatusClass(alias.result);
      const readinessClass = normalizeStatusClass(alias.readiness);
      return `
        <article class="source-row" data-model="source-alias" data-item-id="${escapeHtml(alias.alias)}">
          <strong>${escapeHtml(alias.label || alias.alias)}</strong>
          <span class="status-badge ${readinessClass}">${escapeHtml(alias.readiness_label || alias.readiness)}</span>
          <p>${escapeHtml(alias.why_it_matters)}</p>
          <span class="status-badge ${resultClass}">${escapeHtml(alias.result_label || alias.result)}</span>
        </article>
      `;
    })
    .join("");
}

function renderMissingSources() {
  const grid = document.querySelector("#missing-source-grid");
  const sources = state.fixtures.failed.missing_sources;

  grid.innerHTML = sources
    .map((source) => `
      <article class="missing-card" data-model="missing-source" data-item-id="${escapeHtml(source.alias)}">
        <div>
          <p class="eyebrow">${escapeHtml(source.alias)}</p>
          <h3>${escapeHtml(source.label)}</h3>
          <p>${escapeHtml(source.why_needed)}</p>
        </div>
        <section>
          <h4>가능한 입력</h4>
          <ul class="source-list">
            ${source.accepted_sources.map((item) => `<li>${escapeHtml(item)}</li>`).join("")}
          </ul>
        </section>
        <section>
          <h4>필요 항목</h4>
          <ul class="field-list">
            ${source.required_fields.map((item) => `<li>${escapeHtml(item)}</li>`).join("")}
          </ul>
        </section>
        <div class="workflow-meta">
          <div><dt>담당 권장</dt><dd>${escapeHtml(source.suggested_owner)}</dd></div>
          <div><dt>신뢰 기준</dt><dd>${escapeHtml(source.trust_level)}</dd></div>
        </div>
        <button class="secondary-button" type="button" data-go="source-package-passed">
          <i data-lucide="upload" aria-hidden="true"></i>
          ${escapeHtml(source.upload_option)}
        </button>
      </article>
    `)
    .join("");

  bindNavigation();
}

function renderDecisionReport() {
  const report = state.fixtures.decision;
  const manager = report.manager_view;

  document.querySelector("#allowed-action").textContent = manager.current_allowed_action;
  document.querySelector("#blocked-action").textContent = manager.blocked_action;
  document.querySelector("#why-blocked-copy").textContent = manager.why_blocked;
  document.querySelector("#next-action-copy").textContent = manager.required_next_action;

  const labels = {
    allows_now: "현재 허용되는 일",
    blocks_now: "현재 막힌 일",
    why: "왜 막혔나",
    required_human_action: "다음 조치",
    review_status: "검토 상태"
  };

  const sections = document.querySelector("#report-sections");
  sections.innerHTML = Object.entries(report.sections)
    .map(([key, items]) => `
      <section class="report-section" data-model="decision-report-section" data-item-id="${escapeHtml(key)}">
        <h3>${escapeHtml(labels[key] || key)}</h3>
        <ul>
          ${items.map((item) => `<li>${escapeHtml(item)}</li>`).join("")}
        </ul>
      </section>
    `)
    .join("");
}

function renderEvidenceTrace() {
  const trace = state.fixtures.trace;
  const evidenceList = document.querySelector("#evidence-list");

  evidenceList.innerHTML = trace.evidence_objects
    .map((evidence) => `
      <article class="evidence-item" data-model="evidence-object" data-item-id="${escapeHtml(evidence.evidence_id)}">
        <header>
          <h4>${escapeHtml(evidence.evidence_id)}</h4>
          <span class="status-badge ${normalizeStatusClass(evidence.freshness)}">${escapeHtml(evidence.freshness_label || evidence.freshness)}</span>
        </header>
        <p><strong>의미:</strong> ${escapeHtml(evidence.business_meaning)}</p>
        <p><strong>데이터 출처:</strong> ${escapeHtml(evidence.source_alias_label || evidence.source_alias)} / ${escapeHtml(evidence.source_kind)}</p>
        <p><strong>판단 영향:</strong> ${escapeHtml(evidence.decision_impact)}</p>
      </article>
    `)
    .join("");

  renderDefinitionList("#packet-provenance", trace.packet_provenance);
  renderPolicyAuthority(trace);
}

function renderPolicyAuthority(trace) {
  const target = document.querySelector("#policy-authority");
  target.innerHTML = [
    ["Policy mapping", trace.policy_mapping],
    ["Approval matrix entry", trace.approval_matrix_entry]
  ]
    .map(([title, data]) => `
      <article class="policy-card" data-model="policy-authority-card">
        <h4>${escapeHtml(title)}</h4>
        <dl>
          ${Object.entries(data)
            .map(([key, value]) => `
              <div>
                <dt>${escapeHtml(key)}</dt>
                <dd>${escapeHtml(String(value))}</dd>
              </div>
            `)
            .join("")}
        </dl>
      </article>
    `)
    .join("");
}

function renderReviewRequest() {
  const review = state.fixtures.review;
  const note = document.querySelector("#review-note");
  note.placeholder = review.reviewer_note_placeholder;

  renderDefinitionList("#review-meta", {
    검토자: review.assigned_reviewer,
    필요_역할: review.required_role,
    검토_상태: review.packet_status_label || review.packet_status,
    경계: review.boundary_copy
  });

  const actions = document.querySelector("#review-actions");
  actions.innerHTML = review.actions
    .map((action) => `
      <article class="review-action ${action.enabled ? "" : "disabled"}" data-model="review-action" data-item-id="${escapeHtml(action.action_id)}">
        <header>
          <h4>${escapeHtml(action.label)}</h4>
          <span class="status-badge ${action.enabled ? "ready" : "blocked"}">${action.enabled ? "가능" : "비활성"}</span>
        </header>
        <p>${escapeHtml(action.meaning)}</p>
      </article>
    `)
    .join("");
}

function renderDefinitionList(selector, data) {
  const target = document.querySelector(selector);
  target.innerHTML = Object.entries(data)
    .map(([key, value]) => `
      <dt>${escapeHtml(key)}</dt>
      <dd>${escapeHtml(String(value))}</dd>
    `)
    .join("");
}

function normalizeStatusClass(value) {
  const normalized = String(value).toLowerCase().replace(/[^a-z0-9]+/g, "-");
  if (normalized.includes("missing")) return "missing";
  if (normalized.includes("부족")) return "missing";
  if (normalized.includes("fail")) return "fail";
  if (normalized.includes("실패")) return "fail";
  if (normalized.includes("stale")) return "blocked";
  if (normalized.includes("오래")) return "blocked";
  if (normalized.includes("review")) return "review";
  if (normalized.includes("검토")) return "review";
  if (normalized.includes("partial")) return "partial";
  if (normalized.includes("일부")) return "partial";
  if (normalized.includes("manual")) return "manual";
  if (normalized.includes("draft")) return "draft";
  if (normalized.includes("needs-validation")) return "needs-validation";
  if (normalized.includes("pass")) return "pass";
  if (normalized.includes("통과")) return "pass";
  if (normalized.includes("ready")) return "ready";
  if (normalized.includes("확인")) return "ready";
  if (normalized.includes("configured")) return "configured";
  return normalized;
}

function escapeHtml(value) {
  return String(value)
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;")
    .replaceAll("'", "&apos;");
}

function refreshIcons() {
  if (window.lucide) {
    window.lucide.createIcons();
  }
}
