const shopDrawer = document.querySelector("[data-shop-drawer]");
const drawerTitle = document.querySelector("[data-drawer-title]");
const drawerFit = document.querySelector("[data-drawer-fit]");
const drawerPrice = document.querySelector("[data-drawer-price]");
const signalSummary = document.querySelector(".signal-summary");
const toast = document.querySelector("[data-toast]");

const refreshIcons = () => {
  if (window.lucide) {
    window.lucide.createIcons();
  }
};

const updateSignals = () => {
  const activeSignals = [...document.querySelectorAll(".taste-chip.is-active")]
    .map((chip) => chip.dataset.signal)
    .slice(0, 3);

  signalSummary.textContent = activeSignals.length
    ? activeSignals.join(" · ")
    : "신호 없음";
};

const setDrawerExpanded = (expanded) => {
  shopDrawer.classList.toggle("is-expanded", expanded);
  document.querySelectorAll("[data-open-shop]").forEach((button) => {
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

document.querySelectorAll(".taste-chip").forEach((chip) => {
  chip.addEventListener("click", () => {
    chip.classList.toggle("is-active");
    updateSignals();
  });
});

document.querySelectorAll(".mode-button").forEach((button) => {
  button.addEventListener("click", () => {
    document
      .querySelectorAll(".mode-button")
      .forEach((mode) => mode.classList.remove("is-active"));
    button.classList.add("is-active");
  });
});

document.querySelectorAll(".garment-row").forEach((row) => {
  row.addEventListener("click", () => {
    document
      .querySelectorAll(".garment-row")
      .forEach((item) => item.classList.remove("is-selected"));
    row.classList.add("is-selected");
    drawerTitle.textContent = row.dataset.title;
    drawerFit.textContent = row.dataset.fit;
    drawerPrice.textContent = row.dataset.price;
    setDrawerExpanded(true);
  });
});

document.querySelectorAll(".row-action").forEach((button) => {
  button.addEventListener("click", (event) => {
    event.stopPropagation();
    showToast("아이템을 클로젯에 저장했습니다.");
  });
});

document.querySelectorAll("[data-open-shop]").forEach((button) => {
  button.addEventListener("click", () => {
    setDrawerExpanded(!shopDrawer.classList.contains("is-expanded"));
  });
});

document.querySelectorAll(".size-row button").forEach((button) => {
  button.addEventListener("click", () => {
    document
      .querySelectorAll(".size-row button")
      .forEach((size) => size.classList.remove("is-active"));
    button.classList.add("is-active");
  });
});

document.querySelector("[data-save-edit]").addEventListener("click", () => {
  showToast("오늘의 에딧을 저장했습니다.");
});

document.querySelectorAll(".alternative-tile").forEach((tile) => {
  tile.addEventListener("click", () => {
    document
      .querySelectorAll(".alternative-tile")
      .forEach((item) => item.classList.remove("is-active"));
    tile.classList.add("is-active");
  });
});

updateSignals();
refreshIcons();
