const viewButtons = document.querySelectorAll("[data-view-target]");
const views = document.querySelectorAll("[data-view]");
const navItems = document.querySelectorAll(".bottom-nav .nav-item");
const toast = document.querySelector("[data-toast]");
const themeToggle = document.querySelector("[data-theme-toggle]");
const themeIcon = document.querySelector(".theme-icon use");

let toastTimer;

function showToast(message) {
  toast.textContent = message;
  toast.hidden = false;
  clearTimeout(toastTimer);
  toastTimer = setTimeout(() => {
    toast.hidden = true;
  }, 1700);
}

function setView(name) {
  views.forEach((view) => {
    view.classList.toggle("active", view.dataset.view === name);
  });

  navItems.forEach((item) => {
    const active = item.dataset.viewTarget === name;
    item.classList.toggle("active", active);
    if (active) {
      item.setAttribute("aria-current", "page");
    } else {
      item.removeAttribute("aria-current");
    }
  });

  document.querySelector(".screen-stack").scrollTo({ top: 0, behavior: "smooth" });
}

viewButtons.forEach((button) => {
  button.addEventListener("click", () => {
    setView(button.dataset.viewTarget);
  });
});

document.querySelectorAll(".save-toggle").forEach((button) => {
  button.addEventListener("click", () => {
    const next = button.getAttribute("aria-pressed") !== "true";
    button.setAttribute("aria-pressed", String(next));
    button.classList.toggle("saved", next);
    showToast(next ? "보관함에 저장했어요." : "저장을 해제했어요.");
  });
});

document.querySelectorAll(".genre-chip").forEach((chip) => {
  chip.addEventListener("click", () => {
    document.querySelectorAll(".genre-chip").forEach((item) => {
      item.classList.remove("active");
      item.setAttribute("aria-pressed", "false");
    });
    chip.classList.add("active");
    chip.setAttribute("aria-pressed", "true");
    showToast(`${chip.textContent.trim()} 작품만 모았어요.`);
  });
});

themeToggle.addEventListener("click", () => {
  const root = document.documentElement;
  const nextTheme = root.dataset.theme === "dark" ? "light" : "dark";
  root.dataset.theme = nextTheme;
  const dark = nextTheme === "dark";
  themeToggle.setAttribute("aria-label", dark ? "라이트 모드로 전환" : "다크 모드로 전환");
  themeIcon.setAttribute("href", dark ? "#icon-sun" : "#icon-moon");
  showToast(dark ? "밤 독서 모드로 바꿨어요." : "라이트 모드로 바꿨어요.");
});
