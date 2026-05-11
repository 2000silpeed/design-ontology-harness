const titles = {
  home: "우리 반 광장",
  clubs: "동아리 방",
  gallery: "작품 자랑",
  safety: "안전 약속",
};

const navButtons = Array.from(document.querySelectorAll("[data-view-target]"));
const jumpButtons = Array.from(document.querySelectorAll("[data-jump]"));
const views = Array.from(document.querySelectorAll("[data-view]"));
const viewTitle = document.querySelector("#viewTitle");
const postText = document.querySelector("#postText");
const composerStatus = document.querySelector("#composerStatus");
const postRequest = document.querySelector("#postRequest");

function showView(name) {
  views.forEach((view) => {
    view.classList.toggle("active", view.dataset.view === name);
  });
  navButtons.forEach((button) => {
    button.classList.toggle("active", button.dataset.viewTarget === name);
  });
  if (viewTitle) viewTitle.textContent = titles[name] || "새싹광장";
}

navButtons.forEach((button) => {
  button.addEventListener("click", () => showView(button.dataset.viewTarget));
});

jumpButtons.forEach((button) => {
  button.addEventListener("click", () => showView(button.dataset.jump));
});

document.querySelectorAll("[data-focus-composer]").forEach((button) => {
  button.addEventListener("click", () => {
    showView("home");
    if (postText) postText.focus();
  });
});

document.querySelectorAll(".tag-choice").forEach((button) => {
  button.addEventListener("click", () => {
    document.querySelectorAll(".tag-choice").forEach((item) => item.classList.remove("active"));
    button.classList.add("active");
  });
});

document.querySelectorAll("[data-reaction]").forEach((button) => {
  button.addEventListener("click", () => {
    const count = button.querySelector("span");
    const current = Number.parseInt(count.textContent, 10);
    button.classList.toggle("active");
    count.textContent = String(current + (button.classList.contains("active") ? 1 : -1));
  });
});

if (postRequest && postText && composerStatus) {
  postRequest.addEventListener("click", () => {
    const hasText = postText.value.trim().length > 0;
    composerStatus.textContent = hasText
      ? "게시 요청이 선생님 확인함으로 이동했어요."
      : "짧은 인사라도 적으면 게시 요청을 보낼 수 있어요.";
    composerStatus.classList.toggle("success", hasText);
    if (hasText) postText.value = "";
  });
}
