const rooms = {
  launch: {
    title: "런칭 준비방",
    avatar: "런",
    tone: "blue",
    summary: "런칭 전 점검은 결제 문구, 고객지원 매크로, 모바일 입력창 높이만 남았습니다.",
    messages: [
      { type: "day", text: "오늘" },
      {
        author: "민재",
        avatar: "민",
        tone: "green",
        time: "09:21",
        text: "가격표 링크는 새 문서로 바꿨습니다. 공지에는 무료 체험 종료일만 한 번 더 확인하면 됩니다.",
      },
      {
        author: "모아봇",
        avatar: "봇",
        tone: "amber",
        time: "09:28",
        text: "어제 이후 대화 42개를 정리했습니다. 남은 작업은 결제 문구, 고객지원 매크로, 모바일 QA입니다.",
      },
      {
        type: "system",
        text: "고객지원팀이 환불 안내 매크로 검토를 요청했습니다.",
        action: "요청 보기",
      },
      {
        author: "수진",
        avatar: "수",
        mine: true,
        time: "09:42",
        text: "모바일 입력창 높이는 오늘 안에 다시 볼게요. 공지는 이 버전으로 공유해도 됩니다.",
      },
    ],
  },
  support: {
    title: "고객지원 분류",
    avatar: "지",
    tone: "green",
    summary: "환불 문의는 3건만 남았고, 가격표 링크 오류가 반복 문의의 원인입니다.",
    messages: [
      { type: "day", text: "오늘" },
      {
        author: "지윤",
        avatar: "지",
        tone: "green",
        time: "09:02",
        text: "환불 문의 3건은 민재에게 넘겼습니다. 공통 원인은 예전 가격표 링크였습니다.",
      },
      {
        author: "수진",
        avatar: "수",
        mine: true,
        time: "09:18",
        text: "링크 교체 후에도 같은 문의가 들어오면 이 방에 바로 붙여주세요.",
      },
    ],
  },
  design: {
    title: "디자인 리뷰",
    avatar: "디",
    tone: "neutral",
    summary: "채팅 입력창, 빈 상태, 첨부 파일 행의 모바일 정렬을 확인 중입니다.",
    messages: [
      { type: "day", text: "오늘" },
      {
        author: "서연",
        avatar: "서",
        time: "08:47",
        text: "모바일에서 첨부 버튼과 보내기 버튼 간격이 좁아 보입니다. 12px 정도 여유를 주면 좋겠습니다.",
      },
      {
        author: "수진",
        avatar: "수",
        mine: true,
        time: "08:56",
        text: "좋아요. 입력창 최소 높이와 버튼 터치 영역을 같이 맞추겠습니다.",
      },
    ],
  },
  infra: {
    title: "인프라 알림",
    avatar: "인",
    tone: "amber",
    summary: "서울 리전 지연은 정상 범위로 돌아왔고, 추가 장애 알림은 없습니다.",
    messages: [
      { type: "day", text: "오늘" },
      {
        author: "알림",
        avatar: "인",
        tone: "amber",
        time: "08:30",
        text: "서울 리전 평균 응답 시간이 220ms에서 96ms로 돌아왔습니다.",
      },
    ],
  },
  sales: {
    title: "세일즈 문의",
    avatar: "세",
    tone: "red",
    summary: "가격표 링크와 팀 플랜 제한 안내가 세일즈 문의의 핵심입니다.",
    messages: [
      { type: "day", text: "오늘" },
      {
        author: "하민",
        avatar: "하",
        tone: "red",
        time: "08:12",
        text: "가격표 링크를 새 버전으로 바꿔야 합니다. 팀 플랜 제한 문구도 고객이 헷갈려 합니다.",
      },
      {
        author: "수진",
        avatar: "수",
        mine: true,
        time: "08:19",
        text: "링크는 반영했고, 제한 문구는 런칭 준비방에서 한 번 더 확인하겠습니다.",
      },
    ],
  },
};

const roomButtons = Array.from(document.querySelectorAll(".room-item"));
const messageList = document.querySelector("#messageList");
const roomTitle = document.querySelector("#roomTitle");
const detailSummary = document.querySelector(".panel-card p");
const composer = document.querySelector("#composer");
const messageInput = document.querySelector("#messageInput");
const themeToggle = document.querySelector("#themeToggle");
const app = document.querySelector(".app");
const shareButton = document.querySelector("#shareButton");
const toast = document.querySelector("#toast");
const commandDialog = document.querySelector("#commandDialog");
const commandInput = document.querySelector("#commandInput");
const commandList = document.querySelector("#commandList");
const openCommand = document.querySelector("#openCommand");
const roomSearch = document.querySelector("#roomSearch");

let activeRoom = "launch";
let toastTimer;

function avatarClass(tone) {
  return ["avatar", tone || ""].filter(Boolean).join(" ");
}

function renderMessages(roomKey) {
  const room = rooms[roomKey];
  messageList.innerHTML = "";
  roomTitle.textContent = room.title;
  detailSummary.textContent = room.summary;

  room.messages.forEach((message) => {
    if (message.type === "day") {
      const divider = document.createElement("div");
      divider.className = "day-divider";
      divider.textContent = message.text;
      messageList.append(divider);
      return;
    }

    if (message.type === "system") {
      const item = document.createElement("article");
      item.className = "message system";
      item.innerHTML = `
        <div class="system-card">
          <p>${message.text}</p>
          <button class="button secondary" type="button">${message.action}</button>
        </div>
      `;
      messageList.append(item);
      return;
    }

    const item = document.createElement("article");
    item.className = `message${message.mine ? " mine" : ""}`;
    item.innerHTML = `
      <span class="${avatarClass(message.mine ? "compact" : message.tone)}">${message.avatar}</span>
      <div class="message-body">
        <div class="message-meta">
          <strong>${message.author}</strong>
          <span>${message.time}</span>
        </div>
        <div class="bubble">${message.text}</div>
      </div>
    `;
    messageList.append(item);
  });

  requestAnimationFrame(() => {
    messageList.scrollTop = messageList.scrollHeight;
  });
}

function setActiveRoom(roomKey) {
  activeRoom = roomKey;
  roomButtons.forEach((button) => {
    button.classList.toggle("active", button.dataset.room === roomKey);
  });
  renderMessages(roomKey);
}

function showToast(text) {
  toast.querySelector("span").textContent = text;
  toast.classList.add("show");
  window.clearTimeout(toastTimer);
  toastTimer = window.setTimeout(() => toast.classList.remove("show"), 2200);
}

function renderCommandList(filter = "") {
  const query = filter.trim().toLowerCase();
  const entries = Object.entries(rooms).filter(([, room]) => room.title.toLowerCase().includes(query));
  commandList.innerHTML = "";
  entries.forEach(([key, room]) => {
    const button = document.createElement("button");
    button.className = "command-item";
    button.type = "button";
    button.innerHTML = `<strong>${room.title}</strong><span>대화방으로 이동</span>`;
    button.addEventListener("click", () => {
      setActiveRoom(key);
      commandDialog.close();
    });
    commandList.append(button);
  });
}

roomButtons.forEach((button) => {
  button.addEventListener("click", () => setActiveRoom(button.dataset.room));
});

composer.addEventListener("submit", (event) => {
  event.preventDefault();
  const value = messageInput.value.trim();
  if (!value) return;
  rooms[activeRoom].messages.push({
    author: "수진",
    avatar: "수",
    mine: true,
    time: "방금",
    text: value,
  });
  messageInput.value = "";
  renderMessages(activeRoom);
});

messageInput.addEventListener("input", () => {
  messageInput.style.height = "auto";
  messageInput.style.height = `${Math.min(messageInput.scrollHeight, 150)}px`;
});

themeToggle.addEventListener("click", () => {
  const isDark = app.dataset.theme === "dark";
  app.dataset.theme = isDark ? "light" : "dark";
  themeToggle.querySelector("span").textContent = isDark ? "다크 모드" : "라이트 모드";
});

shareButton.addEventListener("click", () => showToast("요약 링크를 복사했습니다."));

openCommand.addEventListener("click", () => {
  renderCommandList();
  commandDialog.showModal();
  commandInput.focus();
});

commandInput.addEventListener("input", () => renderCommandList(commandInput.value));

roomSearch.addEventListener("input", () => {
  const query = roomSearch.value.trim().toLowerCase();
  roomButtons.forEach((button) => {
    const text = button.innerText.toLowerCase();
    button.hidden = query && !text.includes(query);
  });
});

renderCommandList();
renderMessages(activeRoom);

if (window.lucide) {
  window.lucide.createIcons();
}
