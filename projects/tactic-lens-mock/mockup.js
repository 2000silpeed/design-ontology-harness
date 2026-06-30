const titles = {
  library: "Library / Upload",
  queue: "Processing Queue",
  workspace: "Analysis Workspace",
  playbook: "Playbook",
  reports: "Reports",
};

const navButtons = Array.from(document.querySelectorAll("[data-view-target]"));
const jumpButtons = Array.from(document.querySelectorAll("[data-jump]"));
const views = Array.from(document.querySelectorAll("[data-view]"));
const viewTitle = document.querySelector("#viewTitle");

function showView(name) {
  views.forEach((view) => {
    view.classList.toggle("active", view.dataset.view === name);
  });
  navButtons.forEach((button) => {
    button.classList.toggle("active", button.dataset.viewTarget === name);
  });
  if (viewTitle) viewTitle.textContent = titles[name] || "TacticLens";
}

navButtons.forEach((button) => {
  button.addEventListener("click", () => showView(button.dataset.viewTarget));
});

jumpButtons.forEach((button) => {
  button.addEventListener("click", () => showView(button.dataset.jump));
});

const videoFile = document.querySelector("#videoFile");
const fileName = document.querySelector("#fileName");

if (videoFile && fileName) {
  videoFile.addEventListener("change", () => {
    const file = videoFile.files && videoFile.files[0];
    if (file) fileName.textContent = file.name;
  });
}

document.querySelectorAll(".swatch").forEach((button) => {
  button.addEventListener("click", () => {
    document.querySelectorAll(".swatch").forEach((item) => item.classList.remove("active"));
    button.classList.add("active");
  });
});
