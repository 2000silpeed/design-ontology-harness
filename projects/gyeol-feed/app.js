const appShell = document.querySelector(".app-shell");
const strandTokens = document.querySelectorAll(".strand-token");
const newPostsPill = document.querySelector("[data-new-posts]");
const composeButton = document.querySelector("[data-compose]");
const composeToast = document.querySelector("[data-compose-toast]");
const saveButtons = document.querySelectorAll("[data-save]");

/* strand rail: 결 전환 (프로토타입에서는 활성 표시만 이동) */
strandTokens.forEach((token) => {
  token.addEventListener("click", () => {
    strandTokens.forEach((item) => {
      const hasUnread = item.querySelector(".strand-count");
      item.dataset.state = hasUnread ? "unread" : "default";
      item.removeAttribute("aria-current");
    });
    token.dataset.state = "active";
    token.setAttribute("aria-current", "true");
    appShell.dataset.state = "catching-up";
    window.setTimeout(() => {
      appShell.dataset.state = "default";
    }, 600);
  });
});

/* 저장 토글 */
saveButtons.forEach((button) => {
  button.addEventListener("click", () => {
    const active = button.dataset.state === "active";
    button.dataset.state = active ? "default" : "active";
    button.innerHTML = button.innerHTML.replace(active ? "저장됨" : "저장", active ? "저장" : "저장됨");
    if (window.lucide) window.lucide.createIcons();
  });
});

/* compose: 프로토타입 경계 안내 */
let toastTimer = null;
composeButton.addEventListener("click", () => {
  composeButton.dataset.state = "pressed";
  appShell.dataset.state = "composing";
  composeToast.dataset.state = "visible";
  window.clearTimeout(toastTimer);
  toastTimer = window.setTimeout(() => {
    composeToast.dataset.state = "hidden";
    composeButton.dataset.state = "default";
    appShell.dataset.state = "default";
  }, 1700);
});

/* 새 글 도착 알림: 3초 뒤 등장, 탭하면 최상단으로 */
window.setTimeout(() => {
  newPostsPill.dataset.state = "visible";
}, 3000);

newPostsPill.addEventListener("click", () => {
  newPostsPill.dataset.state = "hidden";
  window.scrollTo({ top: 0, behavior: "smooth" });
});

if (window.lucide) {
  window.lucide.createIcons();
}
