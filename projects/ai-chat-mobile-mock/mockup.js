const screens = Array.from(document.querySelectorAll("[data-screen]"));
const messageList = document.querySelector("[data-message-list]");
const typingBubble = document.querySelector("[data-typing]");

const promptReplies = {
  summary: {
    agent: "strategist",
    name: "전략가 AI",
    avatar: "./assets/strategist.png",
    text: "현재 방향은 명확합니다. 결정 보조를 약속하고, 근거 확인을 신뢰 장치로 두며, 실행 CTA는 따로 분리합니다.",
  },
  risk: {
    agent: "guardian",
    name: "가디언 AI",
    avatar: "./assets/guardian.png",
    text: "주의할 표현은 두 가지입니다. 결과 보장을 암시하는 문장과 사용자의 판단을 대체한다는 뉘앙스를 피해야 합니다.",
  },
  copy: {
    agent: "maker",
    name: "메이커 AI",
    avatar: "./assets/maker.png",
    text: "헤드라인 초안: 중요한 결정을 근거와 함께 다시 확인하세요. CTA는 “근거 보기”와 “실행하기”로 나누겠습니다.",
    right: true,
  },
};

function showScreen(name) {
  screens.forEach((screen) => {
    screen.classList.toggle("active", screen.dataset.screen === name);
  });

  document.querySelectorAll("[data-tab]").forEach((tab) => {
    tab.classList.toggle("active", tab.dataset.tab === name);
  });

  if (name === "chat") {
    requestAnimationFrame(scrollMessages);
  }
}

function scrollMessages() {
  if (!messageList) return;
  messageList.scrollTop = messageList.scrollHeight;
}

function createMessage({ agent, name, avatar, text, right = false }) {
  const article = document.createElement("article");
  article.className = `message agent-${agent}${right ? " is-right" : ""}`;

  const img = document.createElement("img");
  img.className = "avatar";
  img.src = avatar;
  img.alt = "";

  const block = document.createElement("div");
  block.className = "bubble-block";

  const sender = document.createElement("span");
  sender.className = "sender";
  sender.textContent = name;

  const bubble = document.createElement("p");
  bubble.className = "bubble";
  bubble.textContent = text;

  const time = document.createElement("time");
  const now = new Date();
  time.dateTime = now.toISOString();
  time.textContent = now.toLocaleTimeString("ko-KR", { hour: "2-digit", minute: "2-digit", hour12: false });

  block.append(sender, bubble, time);
  article.append(img, block);
  return article;
}

function addReply(reply) {
  if (!messageList || !typingBubble) return;
  typingBubble.insertAdjacentElement("beforebegin", createMessage(reply));
  scrollMessages();
}

document.addEventListener("click", (event) => {
  const openChat = event.target.closest("[data-open-chat]");
  if (openChat) {
    showScreen("chat");
    return;
  }

  const back = event.target.closest("[data-back]");
  if (back) {
    showScreen("chats");
    return;
  }

  const tab = event.target.closest("[data-tab]");
  if (tab) {
    showScreen(tab.dataset.tab);
    return;
  }

  const prompt = event.target.closest("[data-prompt]");
  if (prompt) {
    addReply(promptReplies[prompt.dataset.prompt]);
  }
});

document.querySelector("[data-composer]")?.addEventListener("submit", (event) => {
  event.preventDefault();
  const input = event.currentTarget.elements.prompt;
  const text = input.value.trim();
  if (!text) return;

  addReply({
    agent: "researcher",
    name: "리서처 AI",
    avatar: "./assets/researcher.png",
    text: `"${text}" 기준으로 근거를 다시 묶겠습니다. 최근 대화에서는 신뢰 장치와 실행 분리가 가장 자주 연결됩니다.`,
  });

  input.value = "";
});

scrollMessages();
