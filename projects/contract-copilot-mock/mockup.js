const root = document.documentElement;
const toggle = document.querySelector("#themeToggle");

toggle?.addEventListener("click", () => {
  const nextTheme = root.dataset.theme === "dark" ? "light" : "dark";
  root.dataset.theme = nextTheme;
});
