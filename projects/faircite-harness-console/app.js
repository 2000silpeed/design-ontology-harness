const shell = document.querySelector(".console-shell");
const viewButtons = [...document.querySelectorAll("[data-view-target]")];
const modeButtons = [...document.querySelectorAll("[data-mode-target]")];
const diagnosisForm = document.querySelector("#diagnosisForm");
const scenarioInput = document.querySelector("#scenarioInput");
const scenarioLabel = document.querySelector("#scenarioLabel");
const modeKicker = document.querySelector("#modeKicker");
const diagnosisTitle = document.querySelector("#diagnosisTitle");
const resultTitle = document.querySelector("#resultTitle");
const riskList = document.querySelector("#riskList");
const answerText = document.querySelector("#answerText");
const similarityText = document.querySelector("#similarityText");
const runNote = document.querySelector("#runNote");

const modeState = {
  compliance: {
    kicker: "compliance mode",
    title: "자사 리스크 진단",
    label: "주요 행위",
    result: "상위 리스크 매트릭스",
    sample: "협력사에 도면과 원가자료를 요청하고, 유사 부품 개발 검토 회의에서 해당 자료를 참조했다.",
    badge: "매우 유사 4건",
    answer: "기술자료 제공 요구와 목적 외 활용 정황이 함께 나타난 의결서 chunk가 검색됐습니다. 결과는 참고용 진단이며 법률 자문이 아닙니다.",
    rows: [
      ["기술자료 부당 요구·유용", "매우 유사 4건", "86%", "high"],
      ["부당 단가 인하", "유사 3건", "61%", "medium"],
      ["서면 미발급·보존의무", "약하게 유사 2건", "42%", "low"],
    ],
  },
  shield: {
    kicker: "shield mode",
    title: "상황 진단",
    label: "어떤 일을 겪으셨나요?",
    result: "공정위가 인정한 유사 패턴",
    sample: "본사가 갑자기 필수품목 공급 가격을 올렸고, 다른 곳에서 사면 계약 해지를 검토하겠다고 말했다.",
    badge: "유사 6건",
    answer: "필수품목 공급조건 변경과 거래상 지위 남용이 함께 언급된 유사 의결서가 검색됐습니다. 현재 상황의 위법성 판단이 아니라 유사사례 비교입니다.",
    rows: [
      ["필수품목 강매·구입 강제", "유사 6건", "78%", "high"],
      ["가맹금·공급가 변경", "유사 4건", "64%", "medium"],
      ["영업지역 침해", "판단 어려움 1건", "27%", "low"],
    ],
  },
  paired: {
    kicker: "paired case demo",
    title: "쌍대 케이스 입력",
    label: "같은 사건에서 비교할 행위",
    result: "두 시점의 의미 변환",
    sample: "원사업자가 협력사의 도면과 제조공정 자료를 요구했고 이후 내부 개발 회의에서 유사 부품의 설계 근거로 검토했다.",
    badge: "동일 chunk 사용",
    answer: "동일한 의결서 chunk가 컴플라이언스 모드에서는 예방 체크리스트로, 권익보호 모드에서는 사실관계 정리 항목으로 변환됩니다.",
    rows: [
      ["컴플라이언스 시점", "예방 체크 5개", "72%", "high"],
      ["권익보호 시점", "확인사항 4개", "66%", "medium"],
      ["공통 근거", "chunk 5개", "91%", "low"],
    ],
  },
};

function renderRiskRows(rows) {
  riskList.innerHTML = rows
    .map(
      ([label, count, value, tone]) => `
        <div class="risk-row ${tone}">
          <span>${label}</span>
          <strong>${count}</strong>
          <i style="--value: ${value}"></i>
        </div>
      `,
    )
    .join("");
}

function setView(surface) {
  shell.dataset.view = surface;
  viewButtons.forEach((button) => {
    button.classList.toggle("active", button.dataset.viewTarget === surface);
  });
}

function setMode(mode) {
  const state = modeState[mode];
  shell.dataset.mode = mode;
  modeButtons.forEach((button) => {
    button.classList.toggle("active", button.dataset.modeTarget === mode);
  });
  modeKicker.textContent = state.kicker;
  diagnosisTitle.textContent = state.title;
  scenarioLabel.textContent = state.label;
  resultTitle.textContent = state.result;
  scenarioInput.value = state.sample;
  similarityText.textContent = state.badge;
  answerText.textContent = state.answer;
  renderRiskRows(state.rows);

  if (mode === "paired") {
    setView("paired");
  } else if (shell.dataset.view === "paired") {
    setView("diagnosis");
  }
}

viewButtons.forEach((button) => {
  button.addEventListener("click", () => setView(button.dataset.viewTarget));
});

modeButtons.forEach((button) => {
  button.addEventListener("click", () => setMode(button.dataset.modeTarget));
});

diagnosisForm.addEventListener("submit", (event) => {
  event.preventDefault();
  const time = new Date().toLocaleTimeString("ko-KR", {
    hour: "2-digit",
    minute: "2-digit",
  });
  runNote.textContent = `검색 완료 ${time} · chunk 5개 연결`;
});

document.querySelector("#sampleButton").addEventListener("click", () => {
  const mode = shell.dataset.mode || "compliance";
  scenarioInput.value = modeState[mode].sample;
  runNote.textContent = "샘플 입력 로드";
});

document.querySelector("#clearInput").addEventListener("click", () => {
  scenarioInput.value = "";
  sessionStorage.clear();
  runNote.textContent = "입력 삭제 완료";
});

document.querySelector("#swapButton").addEventListener("click", () => {
  const grid = document.querySelector(".paired-grid");
  [...grid.children].reverse().forEach((node) => grid.appendChild(node));
});

document.querySelectorAll(".case-row, .pattern-tile").forEach((button) => {
  button.addEventListener("click", () => {
    const selector = button.classList.contains("case-row") ? ".case-row" : ".pattern-tile";
    document.querySelectorAll(selector).forEach((item) => item.classList.remove("active"));
    button.classList.add("active");
  });
});

setMode("compliance");
setView("diagnosis");

if (window.lucide) {
  window.lucide.createIcons();
} else {
  window.addEventListener("load", () => window.lucide?.createIcons());
}
