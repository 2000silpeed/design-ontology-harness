const fixturePaths = {
  workflows: "./fixtures/workflows.json",
  flows: "./fixtures/workflow-flows.json"
};

const state = {
  fixtures: {},
  selectedWorkflow: "delivery_delay_confirmation"
};

document.addEventListener("DOMContentLoaded", async () => {
  await loadFixtures();
  initializeRouteState();
  renderWorkflows();
  renderSelectedWorkflow();
  bindNavigation();
  setInitialScreenFromRoute();
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

function initializeRouteState() {
  const params = new URLSearchParams(window.location.search);
  const workflowId = params.get("workflow");
  if (workflowId && state.fixtures.flows.flows[workflowId]) {
    state.selectedWorkflow = workflowId;
  }
}

function setInitialScreenFromRoute() {
  const params = new URLSearchParams(window.location.search);
  const screen = params.get("screen");
  if (screen && document.querySelector(`[data-screen="${CSS.escape(screen)}"]`)) {
    setScreen(screen);
  }
}

function bindNavigation() {
  document.querySelectorAll("[data-go]").forEach((button) => {
    if (button.dataset.bound === "true") {
      return;
    }
    button.dataset.bound = "true";
    button.addEventListener("click", () => {
      const workflowId = button.getAttribute("data-select-workflow");
      if (workflowId) {
        state.selectedWorkflow = workflowId;
        renderSelectedWorkflow();
      }
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

  document.querySelectorAll("[data-progress-screens]").forEach((item) => {
    const screens = item.dataset.progressScreens.split(/\s+/);
    item.classList.toggle("active", screens.includes(screenName));
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
        <article
          class="workflow-card ${futureClass}"
          data-model="workflow"
          data-item-id="${escapeHtml(workflow.workflow_id)}"
          data-clickable="${workflow.status === "configured" ? "true" : "false"}"
          tabindex="${workflow.status === "configured" ? "0" : "-1"}"
        >
          <div>
            <p class="eyebrow">${escapeHtml(workflow.category_label || workflow.workflow_id)}</p>
            <h3>${escapeHtml(workflow.name)}</h3>
            <p>${escapeHtml(workflow.review_purpose || workflow.description)}</p>
          </div>
          <section>
            <h4>판단 가능한 작업</h4>
            <ul class="mini-list">
              ${(workflow.decision_actions || [workflow.result_summary])
                .map((item) => `<li>${escapeHtml(item)}</li>`)
                .join("")}
            </ul>
          </section>
          <section>
            <h4>필요 데이터 묶음</h4>
            <ul class="field-list">
              ${(workflow.required_data_labels || workflow.required_source_package)
                .map((item) => `<li>${escapeHtml(item)}</li>`)
                .join("")}
            </ul>
          </section>
          <dl class="workflow-meta">
            <div><dt>담당 조직</dt><dd>${escapeHtml(workflow.process_owner)}</dd></div>
            <div><dt>설정 버전</dt><dd>${escapeHtml(workflow.config_version)}</dd></div>
            <div><dt>현재 상태</dt><dd>${escapeHtml(workflow.status_label)}</dd></div>
          </dl>
          <div class="workflow-card-footer">
            <span class="status-badge ${statusClass}">${escapeHtml(workflow.status_label)}</span>
            <button class="secondary-button" type="button" data-go="case-input" data-select-workflow="${escapeHtml(workflow.workflow_id)}" ${disabled}>
              <i data-lucide="arrow-right" aria-hidden="true"></i>
              ${cta}
            </button>
          </div>
        </article>
      `;
    })
    .join("");

  bindNavigation();
  bindWorkflowCards();
}

function bindWorkflowCards() {
  document.querySelectorAll(".workflow-card[data-clickable='true']").forEach((card) => {
    if (card.dataset.bound === "true") {
      return;
    }
    card.dataset.bound = "true";
    card.addEventListener("click", (event) => {
      if (event.target.closest("button")) {
        return;
      }
      state.selectedWorkflow = card.dataset.itemId;
      renderSelectedWorkflow();
      setScreen("case-input");
    });
    card.addEventListener("keydown", (event) => {
      if (event.key !== "Enter" && event.key !== " ") {
        return;
      }
      event.preventDefault();
      state.selectedWorkflow = card.dataset.itemId;
      renderSelectedWorkflow();
      setScreen("case-input");
    });
  });
}

function renderSelectedWorkflow() {
  renderCaseInput();
  renderSourceTables();
  renderMissingSources();
  renderDecisionReport();
  renderEvidenceTrace();
  renderReviewRequest();
  updateSelectedWorkflowMarkers();
  refreshIcons();
}

function getSelectedFlow() {
  return state.fixtures.flows.flows[state.selectedWorkflow] ||
    state.fixtures.flows.flows.delivery_delay_confirmation;
}

function getSelectedWorkflow() {
  return state.fixtures.workflows.workflows.find(
    (workflow) => workflow.workflow_id === state.selectedWorkflow
  ) || state.fixtures.workflows.workflows[0];
}

function updateSelectedWorkflowMarkers() {
  const flow = getSelectedFlow();
  const workflow = getSelectedWorkflow();
  document.querySelector("#topbar-case").textContent = flow.case.primary_object;
  document.querySelector("#screen-case-input").dataset.state = flow.case.screen_state;

  document.querySelectorAll(".workflow-card").forEach((card) => {
    card.classList.toggle("selected", card.dataset.itemId === workflow.workflow_id);
  });
}

function renderCaseInput() {
  const flow = getSelectedFlow();
  const form = document.querySelector("#case-form");
  form.innerHTML = `
    ${flow.case_inputs
      .map((field) => `
        <label>
          <span>${escapeHtml(field.label)}</span>
          <input
            type="text"
            value="${escapeHtml(field.value || "")}"
            placeholder="${escapeHtml(field.placeholder || "")}"
            aria-label="${escapeHtml(field.label)}"
          />
        </label>
      `)
      .join("")}
    <div class="action-row">
      <button class="primary-button" type="button" data-go="source-package-failed">
        <i data-lucide="search-check" aria-hidden="true"></i>
        필요 데이터 확인
      </button>
    </div>
  `;

  document.querySelector("#workflow-guidance-title").textContent = flow.guidance.title;
  document.querySelector("#workflow-guidance-copy").textContent = flow.guidance.copy;
  document.querySelector("#workflow-guidance-bullets").innerHTML = flow.guidance.bullets
    .map((item) => `<li>${escapeHtml(item)}</li>`)
    .join("");

  bindNavigation();
}

function renderSourceTables() {
  const flow = getSelectedFlow();
  document.querySelector("#failed-title").textContent = flow.failed.title;
  document.querySelector("#failed-subtitle").textContent = flow.failed.subtitle;
  document.querySelector("#failed-source-heading").textContent = flow.failed.source_heading;
  document.querySelector("#failed-missing-title").textContent = flow.failed.missing_title;
  document.querySelector("#failed-missing-summary").textContent = flow.failed.missing_summary;
  document.querySelector("#failed-missing-reason").textContent = flow.failed.missing_reason;
  document.querySelector("#failed-summary-conclusion").textContent =
    flow.failed.conclusion || flow.failed.title;
  document.querySelector("#failed-summary-reason").textContent =
    flow.failed.reason || flow.failed.subtitle;
  document.querySelector("#failed-business-impact").textContent =
    flow.failed.business_impact || flow.failed.missing_reason;
  document.querySelector("#missing-title").textContent = flow.failed.missing_screen_title;
  document.querySelector("#missing-lead").textContent = flow.failed.missing_screen_lead;
  document.querySelector("#passed-title").textContent = flow.passed.title;
  document.querySelector("#passed-subtitle").textContent = flow.passed.subtitle;
  document.querySelector("#passed-source-heading").textContent = flow.passed.source_heading;
  document.querySelector("#passed-warning").textContent =
    flow.passed.warning || "데이터가 충분하다는 뜻이지, 업무가 승인되었다는 뜻은 아닙니다.";
  renderPassedSummary(flow.passed);

  renderAliasRows("#failed-source-table", flow.failed.aliases);
  renderAliasRows("#passed-source-table", flow.passed.aliases);
}

function renderAliasRows(selector, aliases) {
  const target = document.querySelector(selector);
  target.innerHTML = `
    <div class="source-row source-header" aria-hidden="true">
      <strong>데이터 항목</strong>
      <strong>상태</strong>
      <strong>업무 영향</strong>
      <strong>담당</strong>
      <strong>다음 조치</strong>
    </div>
    ${aliases
    .map((alias) => {
      const readinessClass = normalizeStatusClass(alias.readiness);
      return `
        <article class="source-row" data-model="source-alias" data-item-id="${escapeHtml(alias.alias)}">
          <strong>${escapeHtml(alias.label || alias.alias)}</strong>
          <span class="status-badge ${readinessClass}">${escapeHtml(alias.readiness_label || alias.readiness)}</span>
          <p>${escapeHtml(alias.business_impact || alias.why_it_matters)}</p>
          <p>${escapeHtml(alias.owner || "업무 담당")}</p>
          <p>${escapeHtml(alias.next_action || alias.result_label || alias.result)}</p>
        </article>
      `;
    })
    .join("")}
  `;
}

function renderPassedSummary(passed) {
  const target = document.querySelector("#passed-summary-grid");
  const items = passed.summary_cards || [
    ["데이터 완성도", "필수 항목 확인"],
    ["승인 상태", "승인 아님"],
    ["남은 조치", "담당자 검토 필요"]
  ];
  target.innerHTML = items
    .map((item) => `
      <article class="status-summary-card">
        <span>${escapeHtml(item[0])}</span>
        <strong>${escapeHtml(item[1])}</strong>
      </article>
    `)
    .join("");
}

function renderMissingSources() {
  const grid = document.querySelector("#missing-source-grid");
  const sources = getSelectedFlow().failed.missing_sources;

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
          <div><dt>막히는 작업</dt><dd>${escapeHtml(source.blocked_action || "승인 준비 작업")}</dd></div>
          <div><dt>적용 후 결과</dt><dd>${escapeHtml(source.expected_result || "판단 가능 여부를 다시 확인합니다.")}</dd></div>
        </div>
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
  const flow = getSelectedFlow();
  const report = flow.decision;
  const manager = report.manager_view;

  document.querySelector("#decision-primary-object").textContent = flow.case.primary_object;
  document.querySelector("#decision-conclusion").textContent =
    manager.conclusion || manager.current_allowed_action;
  document.querySelector("#allowed-action").textContent = manager.current_allowed_action;
  document.querySelector("#blocked-action").textContent = manager.blocked_action;
  document.querySelector("#why-blocked-copy").textContent = manager.why_blocked;
  document.querySelector("#next-action-copy").textContent = manager.required_next_action;
  document.querySelector("#decision-reasons-list").innerHTML = (manager.reasons || [])
    .map((item) => `<li>${escapeHtml(item)}</li>`)
    .join("");
  renderDecisionCards(report.cards || []);
  renderTimeline("#decision-timeline", flow.status_history || []);

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

function renderDecisionCards(cards) {
  const target = document.querySelector("#decision-card-grid");
  const fallbackCards = [
    {
      title: "업무 영향",
      body: "승인 준비 단계로 넘기기 전에 추가 확인이 필요합니다."
    },
    {
      title: "검토 상태",
      body: "담당자 검토 기록이 없어 검토 필요 상태입니다."
    }
  ];
  target.innerHTML = (cards.length ? cards : fallbackCards)
    .map((card) => `
      <article class="decision-info-card">
        <p class="eyebrow">${escapeHtml(card.category || "검토 정보")}</p>
        <h3>${escapeHtml(card.title)}</h3>
        <p>${escapeHtml(card.body)}</p>
      </article>
    `)
    .join("");
}

function renderEvidenceTrace() {
  const trace = getSelectedFlow().trace;
  const evidenceList = document.querySelector("#evidence-list");

  evidenceList.innerHTML = trace.evidence_objects
    .map((evidence) => `
      <article class="evidence-item" data-model="evidence-object" data-item-id="${escapeHtml(evidence.evidence_id)}">
        <header>
          <div>
            <p class="eyebrow">근거 ID · ${escapeHtml(evidence.evidence_id)}</p>
            <h4>${escapeHtml(evidence.label || evidence.evidence_id)}</h4>
          </div>
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
  renderTraceVisual(trace.visual_flow || []);
  renderTraceTables(trace, getSelectedFlow().status_history || []);
}

function renderTraceVisual(steps) {
  const target = document.querySelector("#trace-visual-flow");
  const fallback = ["데이터 확인", "최신성 확인", "정책 기준", "차단 사유", "검토 필요"];
  target.innerHTML = (steps.length ? steps : fallback)
    .map((step) => `<span>${escapeHtml(step)}</span>`)
    .join("");
}

function renderTraceTables(trace, history) {
  renderOpsTable("#used-data-table", ["데이터", "출처", "최신성", "판단 영향"], (trace.evidence_objects || []).map((item) => [
    item.source_alias_label || item.source_alias,
    item.source_kind,
    item.freshness_label || item.freshness,
    item.decision_impact
  ]));
  renderOpsTable("#trace-history-table", ["시각", "이력", "상태"], history.map((item) => [
    item.time,
    item.event,
    item.status
  ]));
}

function renderOpsTable(selector, headers, rows) {
  const target = document.querySelector(selector);
  const gridStyle = `grid-template-columns: repeat(${headers.length}, minmax(0, 1fr));`;
  target.innerHTML = `
    <div class="ops-table-row ops-table-header" style="${gridStyle}">
      ${headers.map((header) => `<strong>${escapeHtml(header)}</strong>`).join("")}
    </div>
    ${rows
      .map((row) => `
        <div class="ops-table-row" style="${gridStyle}">
          ${row.map((cell) => `<span>${escapeHtml(cell)}</span>`).join("")}
        </div>
      `)
      .join("")}
  `;
}

function renderPolicyAuthority(trace) {
  const target = document.querySelector("#policy-authority");
  target.innerHTML = [
    ["정책 기준", trace.policy_mapping],
    ["승인 기준", trace.approval_matrix_entry]
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
  const flow = getSelectedFlow();
  const review = flow.review;
  const note = document.querySelector("#review-note");
  note.placeholder = review.reviewer_note_placeholder;
  document.querySelector("#review-primary-object").textContent = flow.case.primary_object;

  renderDefinitionList("#review-meta", {
    검토자: review.assigned_reviewer,
    필요_역할: review.required_role,
    요청_사유: review.request_reason || "업무 판단 경계 확인",
    검토_상태: review.packet_status_label || review.packet_status,
    경계: review.boundary_copy
  });
  document.querySelector("#review-checklist").innerHTML = (review.pre_review_checklist || [])
    .map((item) => `<li>${escapeHtml(item)}</li>`)
    .join("");
  renderTimeline("#review-history-list", flow.status_history || []);

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

function renderTimeline(selector, items) {
  const target = document.querySelector(selector);
  target.innerHTML = items
    .map((item) => `
      <li>
        <time>${escapeHtml(item.time)}</time>
        <span>${escapeHtml(item.event)}</span>
        <strong>${escapeHtml(item.status)}</strong>
      </li>
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
