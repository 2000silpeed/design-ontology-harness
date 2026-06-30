const appShell = document.querySelector(".app-shell");
const modeButtons = [...document.querySelectorAll("[data-mode-target]")];
const navButtons = [...document.querySelectorAll("[data-panel]")];
const diagnosisForm = document.querySelector("#diagnosisForm");
const scenarioInput = document.querySelector("#scenarioInput");
const loadSampleButton = document.querySelector("#loadSample");
const clearInputsButton = document.querySelector("#clearInputs");
const runStatus = document.querySelector("#runStatus");
const modeEyebrow = document.querySelector("#modeEyebrow");
const modeTitle = document.querySelector("#modeTitle");
const promptLabel = document.querySelector("#promptLabel");
const resultTitle = document.querySelector("#resultTitle");
const riskMatrix = document.querySelector("#riskMatrix");
const answerText = document.querySelector("#answerText");
const similarityBadge = document.querySelector("#similarityBadge");
const swapCaseView = document.querySelector("#swapCaseView");

const modeCopy = {
  compliance: {
    eyebrow: "compliance mode",
    title: "자사 리스크 진단",
    prompt: "주요 행위",
    sample:
      "협력사에 도면과 원가자료를 요청하고, 유사 부품 개발 검토 회의에서 해당 자료를 참조했다.",
    result: "상위 리스크 매트릭스",
    badge: "매우 유사 4건",
    answer:
      "기술자료 제공 요구와 목적 외 활용 정황이 함께 나타난 의결서 chunk가 검색됐습니다. 결과는 참고용 진단이며 법률 자문이 아닙니다.",
    rows: [
      ["기술자료 부당 요구·유용", "매우 유사 4건", "86%", "high"],
      ["부당 단가 인하", "유사 3건", "61%", "medium"],
      ["서면 미발급·보존의무", "약하게 유사 2건", "42%", "low"],
    ],
  },
  shield: {
    eyebrow: "shield mode",
    title: "상황 진단",
    prompt: "어떤 일을 겪으셨나요?",
    sample:
      "본사가 갑자기 필수품목 공급 가격을 올렸고, 다른 곳에서 사면 계약 해지를 검토하겠다고 말했다.",
    result: "공정위가 인정한 유사 패턴",
    badge: "유사 6건",
    answer:
      "필수품목 공급조건 변경과 거래상 지위 남용이 함께 언급된 유사 의결서가 검색됐습니다. 현재 상황의 위법성 판단이 아니라 유사사례 비교입니다.",
    rows: [
      ["필수품목 강매·구입 강제", "유사 6건", "78%", "high"],
      ["가맹금·공급가 변경", "유사 4건", "64%", "medium"],
      ["영업지역 침해", "판단 어려움 1건", "27%", "low"],
    ],
  },
  dual: {
    eyebrow: "paired case demo",
    title: "쌍대 케이스 입력",
    prompt: "같은 사건에서 비교할 행위",
    sample:
      "원사업자가 협력사의 도면과 제조공정 자료를 요구했고 이후 내부 개발 회의에서 유사 부품의 설계 근거로 검토했다.",
    result: "두 시점의 의미 변환",
    badge: "동일 chunk 사용",
    answer:
      "동일한 의결서 chunk가 컴플라이언스 모드에서는 예방 체크리스트로, 권익보호 모드에서는 사실관계 정리 항목으로 변환됩니다.",
    rows: [
      ["컴플라이언스 시점", "예방 체크 5개", "72%", "high"],
      ["권익보호 시점", "확인사항 4개", "66%", "medium"],
      ["공통 근거", "chunk 5개", "91%", "low"],
    ],
  },
};

function setMode(mode) {
  appShell.dataset.mode = mode;
  modeButtons.forEach((button) => {
    button.classList.toggle("active", button.dataset.modeTarget === mode);
  });

  const copy = modeCopy[mode];
  modeEyebrow.textContent = copy.eyebrow;
  modeTitle.textContent = copy.title;
  promptLabel.textContent = copy.prompt;
  resultTitle.textContent = copy.result;
  scenarioInput.value = copy.sample;
  answerText.textContent = copy.answer;
  similarityBadge.textContent = copy.badge;
  renderRows(copy.rows);

  if (mode === "dual") {
    setPanel("dual");
  } else if (appShell.dataset.panel === "dual") {
    setPanel("diagnosis");
  }
}

function renderRows(rows) {
  riskMatrix.innerHTML = rows
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

function setPanel(panel) {
  appShell.dataset.panel = panel === "diagnosis" ? "" : panel;
  navButtons.forEach((button) => {
    button.classList.toggle("active", button.dataset.panel === panel);
  });
}

modeButtons.forEach((button) => {
  button.addEventListener("click", () => setMode(button.dataset.modeTarget));
});

navButtons.forEach((button) => {
  button.addEventListener("click", () => setPanel(button.dataset.panel));
});

diagnosisForm.addEventListener("submit", (event) => {
  event.preventDefault();
  const now = new Date();
  const time = now.toLocaleTimeString("ko-KR", { hour: "2-digit", minute: "2-digit" });
  runStatus.textContent = `검색 완료 ${time} · chunk 5개 연결`;
  document.querySelectorAll(".source-card").forEach((card, index) => {
    card.classList.toggle("active", index === 0);
  });
});

loadSampleButton.addEventListener("click", () => {
  const mode = appShell.dataset.mode || "compliance";
  scenarioInput.value = modeCopy[mode].sample;
  runStatus.textContent = "샘플 입력 로드";
});

clearInputsButton.addEventListener("click", () => {
  scenarioInput.value = "";
  localStorage.removeItem("faircite-draft");
  sessionStorage.clear();
  runStatus.textContent = "입력 삭제 완료";
});

scenarioInput.addEventListener("input", () => {
  localStorage.setItem("faircite-draft", scenarioInput.value);
});

document.querySelectorAll(".case-item").forEach((button) => {
  button.addEventListener("click", () => {
    document.querySelectorAll(".case-item").forEach((item) => item.classList.remove("active"));
    button.classList.add("active");
    similarityBadge.textContent = button.dataset.case === "hhi" ? "매우 유사 4건" : "유사 3건";
  });
});

document.querySelectorAll(".pattern-card").forEach((button) => {
  button.addEventListener("click", () => {
    document.querySelectorAll(".pattern-card").forEach((item) => item.classList.remove("active"));
    button.classList.add("active");
  });
});

swapCaseView.addEventListener("click", () => {
  document.querySelector(".dual-grid").classList.toggle("is-swapped");
  const cards = [...document.querySelectorAll(".dual-card")];
  cards.reverse().forEach((card) => document.querySelector(".dual-grid").appendChild(card));
});

window.addEventListener("DOMContentLoaded", () => {
  const draft = localStorage.getItem("faircite-draft");
  if (draft) {
    scenarioInput.value = draft;
  }

  setMode("compliance");
  setPanel("diagnosis");

  if (window.lucide) {
    window.lucide.createIcons();
  }
});
