const appShell = document.querySelector(".app-shell");
const toast = document.querySelector("#toast");
const commandDialog = document.querySelector("#commandDialog");
const runsBody = document.querySelector("#runsBody");
const reviewList = document.querySelector("#reviewList");
const graphCanvas = document.querySelector("#graphCanvas");

const agentDetails = {
  researcher: {
    title: "Researcher",
    subtitle: "Support agent / Claude 3.5 / v2.9",
    risk: "Clear",
    riskClass: "clear",
    owner: "Mina Park",
    policy: "Read-only support data",
  },
  planner: {
    title: "Planner",
    subtitle: "Engineering agent / GPT-4.1 / v3.8",
    risk: "Watch",
    riskClass: "watch",
    owner: "Devon Lee",
    policy: "PII write approval",
  },
  jira: {
    title: "Jira writer",
    subtitle: "Tool integration / limited write scope",
    risk: "Clear",
    riskClass: "clear",
    owner: "Platform Tools",
    policy: "Ticket write scope",
  },
  "support-triage": {
    title: "Support triage",
    subtitle: "Support agent / GPT-4.1 mini / v4.2",
    risk: "Clear",
    riskClass: "clear",
    owner: "Support Ops",
    policy: "Customer message guard",
  },
  coder: {
    title: "Coder",
    subtitle: "Engineering agent / GPT-4.1 / v5.1",
    risk: "Watch",
    riskClass: "watch",
    owner: "Devon Lee",
    policy: "Repository write approval",
  },
  policy: {
    title: "PII gate",
    subtitle: "Governance policy / production enforced",
    risk: "High",
    riskClass: "high",
    owner: "Security Ops",
    policy: "Two approvals stale",
  },
  revenue: {
    title: "CRM updater",
    subtitle: "Revenue agent / Llama 3.1 / v2.4",
    risk: "Clear",
    riskClass: "clear",
    owner: "Revenue Systems",
    policy: "CRM field whitelist",
  },
  summarizer: {
    title: "Summarizer",
    subtitle: "Support agent / Claude 3.5 / v3.1",
    risk: "Clear",
    riskClass: "clear",
    owner: "Mina Park",
    policy: "No external write actions",
  },
  "data-warehouse": {
    title: "Warehouse query",
    subtitle: "Data tool / sensitive table access",
    risk: "High",
    riskClass: "high",
    owner: "Data Platform",
    policy: "PII read review",
  },
};

const runs = [
  { id: "run_8f2c1a7d", agent: "Planner", owner: "Devon", status: "success", risk: "watch", policy: "reviewed", queue: "2m", model: "gpt" },
  { id: "run_7b9e2c1f", agent: "Support triage", owner: "Mina", status: "success", risk: "clear", policy: "passed", queue: "4m", model: "gpt" },
  { id: "run_3c4d5e6f", agent: "Coder", owner: "Devon", status: "blocked", risk: "high", policy: "needs owner", queue: "11m", model: "gpt" },
  { id: "run_9a7b1c2d", agent: "Warehouse query", owner: "Data", status: "waiting", risk: "high", policy: "PII gate", queue: "18m", model: "llama" },
  { id: "run_1e2f3a4b", agent: "Researcher", owner: "Mina", status: "success", risk: "clear", policy: "passed", queue: "6m", model: "claude" },
  { id: "run_4a1c8b5e", agent: "CRM updater", owner: "Revenue", status: "waiting", risk: "watch", policy: "reviewer", queue: "13m", model: "llama" },
  { id: "run_6d9f0e2a", agent: "Summarizer", owner: "Support", status: "success", risk: "clear", policy: "passed", queue: "1m", model: "claude" },
];

const reviews = [
  { title: "PII export request", meta: "Warehouse query -> Planner / reviewer stale 18m", action: "Assign" },
  { title: "Repository write escalation", meta: "Coder wants protected branch access", action: "Review" },
  { title: "CRM owner mismatch", meta: "Revenue agent handoff lacks business owner", action: "Fix" },
  { title: "Prompt version drift", meta: "Planner v3.8 differs from approved policy pack", action: "Diff" },
  { title: "Incident packet missing", meta: "Support triage run lacks audit attachment", action: "Attach" },
];

let activeRunFilter = "all";

function renderSparklines() {
  document.querySelectorAll(".sparkline").forEach((sparkline) => {
    const values = (sparkline.dataset.bars || "")
      .split(",")
      .map((value) => Number(value.trim()))
      .filter((value) => Number.isFinite(value));
    sparkline.innerHTML = values
      .map((value) => `<i style="height:${Math.max(4, value)}%"></i>`)
      .join("");
  });
}

function statusClass(status) {
  if (status === "blocked") return "blocked";
  if (status === "waiting") return "waiting";
  return "success";
}

function riskLabel(risk) {
  if (risk === "high") return "High";
  if (risk === "watch") return "Watch";
  return "Clear";
}

function statusLabel(status) {
  if (status === "blocked") return "Blocked";
  if (status === "waiting") return "Waiting";
  return "Success";
}

function runMatchesFilters(run) {
  const searchValue = document.querySelector("#runSearch").value.trim().toLowerCase();
  const modelValue = document.querySelector("#modelFilter").value;
  const matchesSearch = !searchValue || `${run.id} ${run.agent} ${run.owner} ${run.policy}`.toLowerCase().includes(searchValue);
  const matchesModel = modelValue === "all" || run.model === modelValue;
  const matchesTab =
    activeRunFilter === "all" ||
    (activeRunFilter === "blocked" && run.status === "blocked") ||
    (activeRunFilter === "human" && run.status === "waiting") ||
    (activeRunFilter === "risk" && run.risk === "high");
  return matchesSearch && matchesModel && matchesTab;
}

function renderRuns() {
  const filteredRuns = runs.filter(runMatchesFilters);
  if (!filteredRuns.length) {
    runsBody.innerHTML = `<tr><td colspan="7">No runs match the current filters.</td></tr>`;
    return;
  }
  runsBody.innerHTML = filteredRuns
    .map(
      (run) => `
        <tr data-agent="${run.agent.toLowerCase().replace(/\s+/g, "-")}">
          <td>${run.id}</td>
          <td>${run.agent}</td>
          <td>${run.owner}</td>
          <td><span class="status-badge ${statusClass(run.status)}">${statusLabel(run.status)}</span></td>
          <td>${riskLabel(run.risk)}</td>
          <td>${run.policy}</td>
          <td>${run.queue}</td>
        </tr>
      `,
    )
    .join("");
}

function renderReviews() {
  reviewList.innerHTML = reviews
    .map(
      (item) => `
        <div class="review-item">
          <div>
            <strong>${item.title}</strong>
            <p>${item.meta}</p>
          </div>
          <button class="button secondary" data-review-action="${item.action}">${item.action}</button>
        </div>
      `,
    )
    .join("");
}

function showToast(message) {
  toast.textContent = message;
  toast.classList.add("show");
  clearTimeout(showToast.timer);
  showToast.timer = setTimeout(() => toast.classList.remove("show"), 2600);
}

function updateDrawer(agentKey) {
  const detail = agentDetails[agentKey];
  if (!detail) return;
  document.querySelector("#drawerTitle").textContent = detail.title;
  document.querySelector("#drawerSubtitle").textContent = detail.subtitle;
  document.querySelector("#drawerOwner").textContent = detail.owner;
  document.querySelector("#drawerPolicy").textContent = detail.policy;
  const risk = document.querySelector("#drawerRisk");
  risk.textContent = detail.risk;
  risk.className = `risk-pill ${detail.riskClass}`;
}

function applyGraphFilters() {
  const team = document.querySelector("#teamFilter").value;
  const risk = document.querySelector("#riskFilter").value;
  document.querySelectorAll(".node").forEach((node) => {
    const teamMatches = team === "all" || node.dataset.team === team;
    const riskMatches = risk === "all" || node.dataset.risk === risk;
    node.classList.toggle("dimmed", !(teamMatches && riskMatches));
  });
}

function initGraph() {
  document.querySelectorAll(".node").forEach((node) => {
    node.addEventListener("click", () => {
      document.querySelectorAll(".node").forEach((item) => item.classList.remove("selected"));
      node.classList.add("selected");
      updateDrawer(node.dataset.agent);
      showToast(`${node.querySelector("strong").textContent} selected`);
    });
  });
  document.querySelector("#teamFilter").addEventListener("change", applyGraphFilters);
  document.querySelector("#riskFilter").addEventListener("change", applyGraphFilters);
  document.querySelector("#traceCritical").addEventListener("click", () => {
    graphCanvas.classList.toggle("trace");
    showToast(graphCanvas.classList.contains("trace") ? "Critical handoff path highlighted" : "Critical path cleared");
  });
  document.querySelectorAll("[data-graph-view]").forEach((button) => {
    button.addEventListener("click", () => {
      document.querySelectorAll("[data-graph-view]").forEach((item) => item.classList.remove("active"));
      button.classList.add("active");
      showToast(`${button.textContent} graph view active`);
    });
  });
}

function initRuns() {
  document.querySelector("#runSearch").addEventListener("input", renderRuns);
  document.querySelector("#modelFilter").addEventListener("change", renderRuns);
  document.querySelector("#refreshButton").addEventListener("click", () => showToast("Run queue refreshed"));
  document.querySelectorAll("[data-run-filter]").forEach((button) => {
    button.addEventListener("click", () => {
      activeRunFilter = button.dataset.runFilter;
      document.querySelectorAll("[data-run-filter]").forEach((item) => item.classList.remove("active"));
      button.classList.add("active");
      renderRuns();
    });
  });
  runsBody.addEventListener("click", (event) => {
    const row = event.target.closest("tr");
    if (!row || !row.dataset.agent) return;
    showToast(`${row.cells[0].textContent} audit trail opened`);
  });
}

function initActions() {
  document.querySelector("#themeToggle").addEventListener("click", (event) => {
    const isDark = appShell.dataset.theme === "dark";
    appShell.dataset.theme = isDark ? "light" : "dark";
    event.currentTarget.textContent = isDark ? "Dark mode" : "Light mode";
  });
  document.querySelector("#commandButton").addEventListener("click", () => commandDialog.showModal());
  document.addEventListener("keydown", (event) => {
    if ((event.metaKey || event.ctrlKey) && event.key.toLowerCase() === "k") {
      event.preventDefault();
      commandDialog.showModal();
    }
  });
  document.querySelector("#reviewButton").addEventListener("click", () => showToast("5 policy gates queued for review"));
  document.querySelector("#assignButton").addEventListener("click", () => showToast("Reviewer assigned to PII gate"));
  document.querySelector("#diffButton").addEventListener("click", () => showToast("Prompt and tool diff opened"));
  reviewList.addEventListener("click", (event) => {
    const button = event.target.closest("button");
    if (!button) return;
    showToast(`${button.dataset.reviewAction} action queued`);
  });
  commandDialog.addEventListener("close", () => {
    if (commandDialog.returnValue) showToast(`${commandDialog.returnValue} command queued`);
    commandDialog.returnValue = "";
  });
  document.querySelectorAll(".nav-item").forEach((button) => {
    button.addEventListener("click", () => {
      document.querySelectorAll(".nav-item").forEach((item) => item.classList.remove("active"));
      button.classList.add("active");
      showToast(`${button.dataset.section} section selected`);
    });
  });
  document.querySelector("#globalSearch").addEventListener("input", (event) => {
    const value = event.target.value.trim();
    if (value.length > 2) {
      document.querySelector("#runSearch").value = value;
      renderRuns();
    }
  });
}

renderSparklines();
renderRuns();
renderReviews();
initGraph();
initRuns();
initActions();
