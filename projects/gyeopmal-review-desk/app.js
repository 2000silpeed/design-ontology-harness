const root = document.documentElement;
const shell = document.querySelector(".app-shell");
const themeToggle = document.querySelector(".theme-toggle");
const rows = Array.from(document.querySelectorAll(".ledger-row"));

function applyTheme(mode) {
  root.setAttribute("data-theme", mode);
  const nextIsDark = mode === "dark";
  themeToggle.setAttribute("aria-pressed", String(nextIsDark));
  themeToggle.dataset.themeTarget = nextIsDark ? "light" : "dark";
  themeToggle.lastChild.textContent = nextIsDark ? " 밝은 화면" : " 어두운 화면";
}

themeToggle.addEventListener("click", () => {
  applyTheme(themeToggle.dataset.themeTarget);
});

rows.forEach((row) => {
  row.querySelector(".ledger-row-button").addEventListener("click", () => {
    rows.forEach((other) => {
      other.removeAttribute("aria-current");
      if (other.dataset.state === "reviewing") {
        other.dataset.state = "resolved";
      }
    });
    row.dataset.state = "reviewing";
    row.setAttribute("aria-current", "true");
    shell.dataset.state = "reviewing";
  });
});

// 라이트/다크 증거 스크린샷을 같은 route에서 찍을 수 있도록 초기 모드를 URL로도 받는다.
const requestedTheme = new URLSearchParams(window.location.search).get("theme");
applyTheme(
  (requestedTheme || root.getAttribute("data-theme")) === "dark" ? "dark" : "light",
);
