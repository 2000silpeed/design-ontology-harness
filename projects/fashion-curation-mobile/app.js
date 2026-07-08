const accentButtons = document.querySelectorAll(".accent-swatch");
const contrastSlider = document.querySelector("[data-contrast-slider]");
const contrastValue = document.querySelector("[data-contrast-value]");
const temperatureLabel = document.querySelector("[data-temperature-label]");
const confirmation = document.querySelector("[data-confirmation]");
const restraintNote = document.querySelector("[data-restraint-note]");
const saveButton = document.querySelector("[data-save-calibration]");
const shortlistButton = document.querySelector("[data-shortlist-accent]");
const compassHandle = document.querySelector("[data-compass-handle]");

const accentNotes = {
  "청록 실크": "청록 실크 하나면 셔츠의 선은 유지되고 얼굴 주변만 정리됩니다.",
  "와인 벨트": "와인 벨트는 허리선을 또렷하게 만들지만 대비가 조금 강해집니다.",
  "라임 니트": "라임 니트는 분위기를 밝히지만 오늘 좌표에서는 포인트가 커집니다.",
};

let selectedAccent = "청록 실크";

function showConfirmation(message) {
  confirmation.textContent = message;
  confirmation.classList.add("is-visible");
  window.clearTimeout(showConfirmation.timer);
  showConfirmation.timer = window.setTimeout(() => {
    confirmation.classList.remove("is-visible");
  }, 1900);
}

accentButtons.forEach((button, index) => {
  button.addEventListener("click", () => {
    accentButtons.forEach((item) => item.classList.remove("is-selected"));
    button.classList.add("is-selected");
    selectedAccent = button.dataset.accent;
    temperatureLabel.textContent = button.dataset.tone;
    restraintNote.textContent = accentNotes[selectedAccent];
    document.querySelector("[data-accent-count]").textContent = `${index + 1} / 3`;
  });
});

contrastSlider.addEventListener("input", (event) => {
  const value = event.target.value;
  contrastValue.textContent = value;
  compassHandle.style.left = `${38 + Number(value) * 0.34}%`;
  compassHandle.querySelector("span").textContent = value;
  compassHandle.setAttribute("aria-label", `현재 취향 좌표: contrast ${value}`);
});

saveButton.addEventListener("click", () => {
  showConfirmation("현재 취향 좌표를 저장했습니다.");
});

shortlistButton.addEventListener("click", () => {
  showConfirmation(`${selectedAccent}을 후보에 담았습니다.`);
});

if (window.lucide) {
  window.lucide.createIcons();
}
