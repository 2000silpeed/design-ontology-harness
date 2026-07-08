const shopSheet = document.querySelector("[data-shop-sheet]");
const sheetTitle = document.querySelector("[data-sheet-title]");
const sheetFit = document.querySelector("[data-sheet-fit]");
const sheetPrice = document.querySelector("[data-sheet-price]");
const signalSummary = document.querySelector("[data-signal-summary]");
const toast = document.querySelector("[data-toast]");

const createIcons = () => {
  if (window.lucide) {
    window.lucide.createIcons();
  }
};

const updateSignalSummary = () => {
  const active = [...document.querySelectorAll(".signal-node.is-active")]
    .map((node) => node.dataset.signal)
    .slice(0, 3);
  signalSummary.textContent = active.length ? active.join(" · ") : "신호 없음";
};

const setSheetExpanded = (expanded) => {
  shopSheet.classList.toggle("is-expanded", expanded);
  document.querySelectorAll("[data-toggle-shop]").forEach((button) => {
    button.setAttribute("aria-expanded", String(expanded));
  });
};

const showToast = (message) => {
  toast.textContent = message;
  toast.classList.add("is-visible");
  window.clearTimeout(showToast.timer);
  showToast.timer = window.setTimeout(() => {
    toast.classList.remove("is-visible");
  }, 1900);
};

const selectGarment = (itemKey) => {
  const row = document.querySelector(`.garment-row[data-item="${itemKey}"]`);
  if (!row) return;

  document
    .querySelectorAll(".garment-row")
    .forEach((item) => item.classList.remove("is-selected"));
  row.classList.add("is-selected");
  sheetTitle.textContent = row.dataset.title;
  sheetFit.textContent = row.dataset.fit;
  sheetPrice.textContent = row.dataset.price;
};

document.querySelectorAll(".signal-node").forEach((node) => {
  node.addEventListener("click", () => {
    node.classList.toggle("is-active");
    updateSignalSummary();
  });
});

document.querySelectorAll(".garment-row").forEach((row) => {
  row.addEventListener("click", () => {
    selectGarment(row.dataset.item);
    setSheetExpanded(true);
  });
});

document.querySelectorAll("[data-select-item]").forEach((pin) => {
  pin.addEventListener("click", () => {
    selectGarment(pin.dataset.selectItem);
    setSheetExpanded(true);
  });
});

document.querySelectorAll(".row-icon").forEach((button) => {
  button.addEventListener("click", (event) => {
    event.stopPropagation();
    showToast("아이템을 옷장에 저장했습니다.");
  });
});

document.querySelectorAll("[data-toggle-shop]").forEach((button) => {
  button.addEventListener("click", () => {
    setSheetExpanded(!shopSheet.classList.contains("is-expanded"));
  });
});

document.querySelectorAll(".size-chips button").forEach((button) => {
  button.addEventListener("click", () => {
    document
      .querySelectorAll(".size-chips button")
      .forEach((size) => size.classList.remove("is-active"));
    button.classList.add("is-active");
  });
});

document.querySelector("[data-save-look]").addEventListener("click", () => {
  showToast("오늘의 보드를 저장했습니다.");
});

document.querySelectorAll(".alternative").forEach((button) => {
  button.addEventListener("click", () => {
    document
      .querySelectorAll(".alternative")
      .forEach((item) => item.classList.remove("is-active"));
    button.classList.add("is-active");
  });
});

updateSignalSummary();
createIcons();
