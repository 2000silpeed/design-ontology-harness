const appShell = document.querySelector(".app-shell");
const toast = document.querySelector("#toast");
const commandDialog = document.querySelector("#commandDialog");
const runsBody = document.querySelector("#runsBody");
const reviewList = document.querySelector("#reviewList");
const graphCanvas = document.querySelector("#graphCanvas");

const agentDetails = {
  researcher: {
    title: "리서처",
    subtitle: "지원 에이전트 / Claude 3.5 / v2.9",
    risk: "정상",
    riskClass: "clear",
    owner: "Mina Park",
    policy: "지원 데이터 읽기 전용",
  },
  planner: {
    title: "플래너",
    subtitle: "엔지니어링 에이전트 / GPT-4.1 / v3.8",
    risk: "주의",
    riskClass: "watch",
    owner: "Devon Lee",
    policy: "PII 쓰기 승인",
  },
  jira: {
    title: "Jira 작성기",
    subtitle: "도구 연동 / 제한된 쓰기 권한",
    risk: "정상",
    riskClass: "clear",
    owner: "Platform Tools",
    policy: "티켓 쓰기 범위",
  },
  "support-triage": {
    title: "지원 분류",
    subtitle: "지원 에이전트 / GPT-4.1 mini / v4.2",
    risk: "정상",
    riskClass: "clear",
    owner: "Support Ops",
    policy: "고객 메시지 가드",
  },
  coder: {
    title: "코더",
    subtitle: "엔지니어링 에이전트 / GPT-4.1 / v5.1",
    risk: "주의",
    riskClass: "watch",
    owner: "Devon Lee",
    policy: "저장소 쓰기 승인",
  },
  policy: {
    title: "PII 게이트",
    subtitle: "거버넌스 정책 / 프로덕션 적용",
    risk: "높음",
    riskClass: "high",
    owner: "Security Ops",
    policy: "승인 2건 지연",
  },
  revenue: {
    title: "CRM 업데이트",
    subtitle: "매출 에이전트 / Llama 3.1 / v2.4",
    risk: "정상",
    riskClass: "clear",
    owner: "Revenue Systems",
    policy: "CRM 필드 허용 목록",
  },
  summarizer: {
    title: "요약기",
    subtitle: "지원 에이전트 / Claude 3.5 / v3.1",
    risk: "정상",
    riskClass: "clear",
    owner: "Mina Park",
    policy: "외부 쓰기 작업 없음",
  },
  "data-warehouse": {
    title: "웨어하우스 쿼리",
    subtitle: "데이터 도구 / 민감 테이블 접근",
    risk: "높음",
    riskClass: "high",
    owner: "Data Platform",
    policy: "PII 읽기 검토",
  },
};

const runs = [
  { id: "run_8f2c1a7d", agent: "플래너", owner: "Devon", status: "success", risk: "watch", policy: "검토 완료", queue: "2분", model: "gpt" },
  { id: "run_7b9e2c1f", agent: "지원 분류", owner: "Mina", status: "success", risk: "clear", policy: "통과", queue: "4분", model: "gpt" },
  { id: "run_3c4d5e6f", agent: "코더", owner: "Devon", status: "blocked", risk: "high", policy: "담당자 필요", queue: "11분", model: "gpt" },
  { id: "run_9a7b1c2d", agent: "웨어하우스 쿼리", owner: "Data", status: "waiting", risk: "high", policy: "PII 게이트", queue: "18분", model: "llama" },
  { id: "run_1e2f3a4b", agent: "리서처", owner: "Mina", status: "success", risk: "clear", policy: "통과", queue: "6분", model: "claude" },
  { id: "run_4a1c8b5e", agent: "CRM 업데이트", owner: "Revenue", status: "waiting", risk: "watch", policy: "검토자", queue: "13분", model: "llama" },
  { id: "run_6d9f0e2a", agent: "요약기", owner: "Support", status: "success", risk: "clear", policy: "통과", queue: "1분", model: "claude" },
];

const reviews = [
  { title: "PII 내보내기 요청", meta: "웨어하우스 쿼리 -> 플래너 / 검토자 18분 지연", action: "배정" },
  { title: "저장소 쓰기 권한 상승", meta: "코더가 보호 브랜치 접근을 요청함", action: "검토" },
  { title: "CRM 담당자 불일치", meta: "매출 에이전트 핸드오프에 업무 담당자가 없음", action: "수정" },
  { title: "프롬프트 버전 차이", meta: "플래너 v3.8이 승인된 정책 팩과 다름", action: "비교" },
  { title: "사고 패킷 누락", meta: "지원 분류 실행에 감사 첨부가 없음", action: "첨부" },
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
  if (risk === "high") return "높음";
  if (risk === "watch") return "주의";
  return "정상";
}

function statusLabel(status) {
  if (status === "blocked") return "차단";
  if (status === "waiting") return "대기";
  return "성공";
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
    runsBody.innerHTML = `<tr><td colspan="7">현재 필터에 맞는 실행이 없습니다.</td></tr>`;
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
      showToast(`${node.querySelector("strong").textContent} 선택됨`);
    });
  });
  document.querySelector("#teamFilter").addEventListener("change", applyGraphFilters);
  document.querySelector("#riskFilter").addEventListener("change", applyGraphFilters);
  document.querySelector("#traceCritical").addEventListener("click", () => {
    graphCanvas.classList.toggle("trace");
    showToast(graphCanvas.classList.contains("trace") ? "병목 경로만 남겼습니다" : "전체 핸드오프를 다시 표시했습니다");
  });
  document.querySelectorAll("[data-graph-view]").forEach((button) => {
    button.addEventListener("click", () => {
      document.querySelectorAll("[data-graph-view]").forEach((item) => item.classList.remove("active"));
      button.classList.add("active");
      showToast(`${button.textContent} 보기로 전환했습니다`);
    });
  });
}

function initRuns() {
  document.querySelector("#runSearch").addEventListener("input", renderRuns);
  document.querySelector("#modelFilter").addEventListener("change", renderRuns);
  document.querySelector("#refreshButton").addEventListener("click", () => showToast("실행 큐를 새로고침했습니다"));
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
    showToast(`${row.cells[0].textContent} 감사 추적을 열었습니다`);
  });
}

function initActions() {
  document.querySelector("#themeToggle").addEventListener("click", (event) => {
    const isDark = appShell.dataset.theme === "dark";
    appShell.dataset.theme = isDark ? "light" : "dark";
    event.currentTarget.textContent = isDark ? "다크 모드" : "라이트 모드";
  });
  document.querySelector("#commandButton").addEventListener("click", () => commandDialog.showModal());
  document.addEventListener("keydown", (event) => {
    if ((event.metaKey || event.ctrlKey) && event.key.toLowerCase() === "k") {
      event.preventDefault();
      commandDialog.showModal();
    }
  });
  document.querySelector("#reviewButton").addEventListener("click", () => showToast("정책 게이트 5건을 검토 큐에 올렸습니다"));
  document.querySelector("#assignButton").addEventListener("click", () => showToast("PII 게이트에 검토자를 배정했습니다"));
  document.querySelector("#diffButton").addEventListener("click", () => showToast("프롬프트와 도구 변경점을 열었습니다"));
  reviewList.addEventListener("click", (event) => {
    const button = event.target.closest("button");
    if (!button) return;
    showToast(`${button.dataset.reviewAction} 작업을 큐에 올렸습니다`);
  });
  commandDialog.addEventListener("close", () => {
    if (commandDialog.returnValue) showToast(`${commandDialog.returnValue} 명령을 큐에 올렸습니다`);
    commandDialog.returnValue = "";
  });
  document.querySelectorAll(".nav-item").forEach((button) => {
    button.addEventListener("click", () => {
      document.querySelectorAll(".nav-item").forEach((item) => item.classList.remove("active"));
      button.classList.add("active");
      showToast(`${button.dataset.section} 섹션을 선택했습니다`);
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
