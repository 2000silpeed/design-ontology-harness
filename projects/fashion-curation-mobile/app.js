const appShell = document.querySelector(".app-shell");
const compassField = document.getElementById("compassField");
const compassHandle = document.getElementById("compassHandle");
const handleReadout = document.getElementById("handleReadout");
const directionRead = document.getElementById("directionRead");
const confirmation = document.querySelector("[data-confirmation]");
const saveButton = document.querySelector("[data-save-calibration]");
const shortlistButton = document.querySelector("[data-shortlist-accent]");
const accentButtons = document.querySelectorAll(".accent-swatch");
const accentCount = document.querySelector("[data-accent-count]");
const restraintNote = document.querySelector(".restraint-note");
const meters = {
  restraint: [document.getElementById("meterRestraint"), document.getElementById("meterRestraintValue")],
  contrast: [document.getElementById("meterContrast"), document.getElementById("meterContrastValue")],
  walk: [document.getElementById("meterWalk"), document.getElementById("meterWalkValue")],
};

const accentNotes = {
  "청록 니트 스카프": "청록 스카프 하나면 셔츠의 선은 유지되고 얼굴 주변만 정리됩니다.",
  "와인 레더 벨트": "와인 벨트는 허리선을 또렷하게 만들지만 대비가 조금 강해집니다.",
  "애프리콧 삭스": "애프리콧 삭스는 발목만 밝혀서 보행성 손해 없이 포인트를 만듭니다.",
};

let selectedAccent = "청록 니트 스카프";
const coord = { quiet: 62, sharp: 41 };

const FIELD_W = 320;
const FIELD_H = 200;
const svgParts = {
  glow: document.getElementById("handleGlow"),
  crossX: document.getElementById("crosshairX"),
  crossY: document.getElementById("crosshairY"),
  outer: document.getElementById("handleOuter"),
  dot: document.getElementById("handleDot"),
  ticks: document.getElementById("axisTicks"),
};

function buildAxisTicks() {
  if (!svgParts.ticks) return;
  const ns = "http://www.w3.org/2000/svg";
  for (let i = 1; i < 10; i += 1) {
    const x = (FIELD_W / 10) * i;
    const bottom = document.createElementNS(ns, "line");
    bottom.setAttribute("x1", x);
    bottom.setAttribute("y1", FIELD_H - (i % 5 === 0 ? 7 : 4));
    bottom.setAttribute("x2", x);
    bottom.setAttribute("y2", FIELD_H);
    svgParts.ticks.appendChild(bottom);

    const y = (FIELD_H / 10) * i;
    const left = document.createElementNS(ns, "line");
    left.setAttribute("x1", 0);
    left.setAttribute("y1", y);
    left.setAttribute("x2", i % 5 === 0 ? 7 : 4);
    left.setAttribute("y2", y);
    svgParts.ticks.appendChild(left);
  }
}

function syncInstrument(x, y) {
  svgParts.glow.setAttribute("cx", x);
  svgParts.glow.setAttribute("cy", y);
  svgParts.outer.setAttribute("cx", x);
  svgParts.outer.setAttribute("cy", y);
  svgParts.dot.setAttribute("cx", x);
  svgParts.dot.setAttribute("cy", y);
  svgParts.crossX.setAttribute("x1", x);
  svgParts.crossX.setAttribute("y1", y);
  svgParts.crossX.setAttribute("x2", x);
  svgParts.crossX.setAttribute("y2", FIELD_H);
  svgParts.crossY.setAttribute("x1", 0);
  svgParts.crossY.setAttribute("y1", y);
  svgParts.crossY.setAttribute("x2", x);
  svgParts.crossY.setAttribute("y2", y);
}

function renderCalibration() {
  compassHandle.style.left = `${coord.quiet}%`;
  compassHandle.style.top = `${100 - coord.sharp}%`;
  syncInstrument((coord.quiet / 100) * FIELD_W, ((100 - coord.sharp) / 100) * FIELD_H);
  handleReadout.textContent = Math.round(coord.quiet);
  compassHandle.setAttribute(
    "aria-label",
    `현재 취향 좌표: 조용함 ${Math.round(coord.quiet)}, 선명함 ${Math.round(coord.sharp)}. 드래그하거나 방향키로 이동`
  );

  const softness = coord.quiet >= 50 ? "soft" : "crisp";
  const contrastWord = coord.sharp >= 50 ? "high contrast" : "contrast";
  directionRead.textContent = `${softness} ${contrastWord}`;

  setMeter("restraint", Math.round(100 - coord.sharp * 0.7));
  setMeter("contrast", Math.round(coord.sharp));
  setMeter("walk", Math.round(90 - coord.sharp * 0.55));
}

function setMeter(name, value) {
  const [fill, label] = meters[name];
  fill.style.width = `${value}%`;
  label.textContent = value;
  const row = fill.closest(".meter-row");
  if (name === "walk") {
    row.dataset.state = value < 60 ? "warning" : "default";
  }
}

function showConfirmation(message) {
  confirmation.textContent = message;
  confirmation.dataset.state = "visible";
  window.clearTimeout(showConfirmation.timer);
  showConfirmation.timer = window.setTimeout(() => {
    confirmation.dataset.state = "hidden";
  }, 1900);
}

/* compass handle: pointer drag */
let dragging = false;

compassHandle.addEventListener("pointerdown", (event) => {
  dragging = true;
  compassHandle.dataset.state = "dragging";
  appShell.dataset.state = "calibrating";
  svgParts.outer.setAttribute("r", 18);
  compassHandle.setPointerCapture(event.pointerId);
});

compassHandle.addEventListener("pointermove", (event) => {
  if (!dragging) return;
  const rect = compassField.getBoundingClientRect();
  coord.quiet = Math.min(94, Math.max(6, ((event.clientX - rect.left) / rect.width) * 100));
  coord.sharp = Math.min(94, Math.max(6, 100 - ((event.clientY - rect.top) / rect.height) * 100));
  renderCalibration();
});

compassHandle.addEventListener("pointerup", () => {
  dragging = false;
  compassHandle.dataset.state = "default";
  appShell.dataset.state = "default";
  svgParts.outer.setAttribute("r", 15);
});

compassHandle.addEventListener("keydown", (event) => {
  const step = 4;
  if (event.key === "ArrowLeft") coord.quiet -= step;
  else if (event.key === "ArrowRight") coord.quiet += step;
  else if (event.key === "ArrowUp") coord.sharp += step;
  else if (event.key === "ArrowDown") coord.sharp -= step;
  else return;
  event.preventDefault();
  coord.quiet = Math.min(94, Math.max(6, coord.quiet));
  coord.sharp = Math.min(94, Math.max(6, coord.sharp));
  renderCalibration();
});

/* accent tray: single bounded choice */
accentButtons.forEach((button, index) => {
  button.addEventListener("click", () => {
    accentButtons.forEach((item) => {
      item.dataset.state = "default";
      item.setAttribute("aria-checked", "false");
    });
    button.dataset.state = "selected";
    button.setAttribute("aria-checked", "true");
    selectedAccent = button.dataset.accent;
    accentCount.textContent = `${index + 1} / 3`;
    restraintNote.textContent = accentNotes[selectedAccent];
  });
});

/* decision dock */
saveButton.addEventListener("click", () => {
  saveButton.dataset.state = "saved";
  appShell.dataset.state = "saved";
  showConfirmation(`좌표 저장 · 조용함 ${Math.round(coord.quiet)} / 선명함 ${Math.round(coord.sharp)}`);
  window.setTimeout(() => {
    saveButton.dataset.state = "default";
    appShell.dataset.state = "default";
  }, 2100);
});

shortlistButton.addEventListener("click", () => {
  showConfirmation(`${selectedAccent}를 후보에 담았어요`);
});

buildAxisTicks();
renderCalibration();

if (window.lucide) {
  window.lucide.createIcons();
}
