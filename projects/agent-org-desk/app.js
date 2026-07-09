const appShell = document.querySelector(".app-shell");
const queueItems = document.querySelectorAll(".queue-item");
const approveButton = document.querySelector("[data-approve]");
const escalateButton = document.querySelector("[data-escalate]");
const answerDraft = document.querySelector(".answer-draft");
const draftState = document.querySelector("[data-draft-state]");
const actionNote = document.querySelector("[data-action-note]");
const toast = document.querySelector("[data-toast]");

/* 점수 바: data-score를 폭으로 반영 */
document.querySelectorAll(".score-fill").forEach((fill) => {
  fill.style.width = `${fill.dataset.score}%`;
});

/* 큐 선택 (프로토타입: 선택 표시만 이동) */
queueItems.forEach((item) => {
  item.addEventListener("click", () => {
    queueItems.forEach((other) => {
      if (other.dataset.state === "selected") other.dataset.state = "default";
      other.removeAttribute("aria-current");
    });
    item.dataset.state = "selected";
    item.setAttribute("aria-current", "true");
  });
});

let toastTimer = null;

function showToast(message) {
  toast.textContent = message;
  toast.dataset.state = "visible";
  window.clearTimeout(toastTimer);
  toastTimer = window.setTimeout(() => {
    toast.dataset.state = "hidden";
  }, 2200);
}

approveButton.addEventListener("click", () => {
  const approved = approveButton.dataset.state === "approved";
  if (approved) return;
  approveButton.dataset.state = "approved";
  approveButton.textContent = "승인됨";
  answerDraft.dataset.state = "approved";
  draftState.textContent = "승인 · 공동 답변 · 출처 2";
  actionNote.textContent = "전송 대기열 등록 · 정정은 언제든 append-only로 가능합니다.";
  appShell.dataset.state = "approved";
  showToast("답변이 승인되어 전송 대기열에 들어갔습니다");
});

escalateButton.addEventListener("click", () => {
  showToast("매니저 판정함으로 이동했습니다 — 질문은 버려지지 않습니다");
});

if (window.lucide) {
  window.lucide.createIcons();
}
