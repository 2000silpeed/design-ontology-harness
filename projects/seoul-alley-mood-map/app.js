const places = [
  {
    id: "paper",
    name: "서촌 종이 골목",
    area: "서촌",
    type: "서점 골목",
    score: 92,
    time: "늦은 오후",
    mood: "차분 · 집중",
    confidence: "관찰 근거 높음",
    updated: "오늘 16:20",
    summary: "낮은 대화음, 종이 냄새, 오래된 목재 진열대가 이어지는 짧은 골목입니다.",
    tradeoff: "좌석은 적지만 산책 후 짧게 머물기 좋음",
    signals: ["노란빛", "낮은 소음", "종이 질감"],
    meters: {
      light: 84,
      sound: 28,
      crowding: 36,
      texture: 76
    },
    relations: [
      ["Place", "hasSensorySignal", "오후 노란빛"],
      ["Place", "supportsMood", "차분"],
      ["Place", "worksBestAt", "늦은 오후"],
      ["Evidence", "supports", "사용자 기록 6개"]
    ]
  },
  {
    id: "tea",
    name: "필운동 차분한 찻길",
    area: "서촌",
    type: "카페 주변",
    score: 86,
    time: "아침",
    mood: "정리 · 대화",
    confidence: "사용자 기록 기반",
    updated: "어제 09:10",
    summary: "작은 찻집과 낮은 담장이 붙어 있어 아침 햇빛과 잔잔한 발소리가 잘 남습니다.",
    tradeoff: "오후에는 대기 줄이 생길 수 있음",
    signals: ["아침빛", "발소리", "낮은 담장"],
    meters: {
      light: 72,
      sound: 34,
      crowding: 52,
      texture: 68
    },
    relations: [
      ["Place", "hasSensorySignal", "아침빛"],
      ["Place", "supportsMood", "정리"],
      ["Place", "worksBestAt", "아침"],
      ["Evidence", "supports", "방문 메모 4개"]
    ]
  },
  {
    id: "rain",
    name: "수성동 비 오는 계단",
    area: "서촌",
    type: "공원 진입로",
    score: 81,
    time: "비 오는 날",
    mood: "사색 · 숨은",
    confidence: "최근 기록 없음",
    updated: "12일 전",
    summary: "물소리와 돌계단 질감이 강한 길입니다. 기록은 오래됐지만 비 오는 날 선호가 높습니다.",
    tradeoff: "길이 미끄러워 짧은 이동에 적합",
    signals: ["물소리", "돌 질감", "낮은 인파"],
    meters: {
      light: 48,
      sound: 42,
      crowding: 22,
      texture: 88
    },
    relations: [
      ["Place", "hasSensorySignal", "물소리"],
      ["Place", "supportsMood", "사색"],
      ["Place", "worksBestAt", "비 오는 날"],
      ["Evidence", "supports", "오래된 사용자 기록"]
    ]
  }
];

const labels = {
  light: "빛",
  sound: "소리",
  crowding: "혼잡",
  texture: "질감"
};

let selectedPlace = places[0];

function icon(name) {
  return `<svg class="icon" aria-hidden="true"><use href="#${name}" /></svg>`;
}

function signalIcon(signal) {
  if (signal.includes("빛")) return "icon-sun";
  if (signal.includes("소리") || signal.includes("발소리")) return "icon-sound";
  if (signal.includes("종이")) return "icon-book";
  if (signal.includes("물") || signal.includes("비")) return "icon-rain";
  if (signal.includes("돌")) return "icon-stairs";
  if (signal.includes("담장") || signal.includes("인파")) return "icon-eye";
  return "icon-leaf";
}

function renderPlaceList() {
  const list = document.querySelector("#placeList");
  list.innerHTML = places
    .map(
      (place) => `
        <article class="place-row ${place.id === selectedPlace.id ? "active" : ""}">
          <button type="button" data-place="${place.id}" aria-pressed="${place.id === selectedPlace.id}">
            <span class="row-index">${String(places.indexOf(place) + 1).padStart(2, "0")}</span>
            <span class="place-row-main">
              <span class="place-row-title">
                <strong>${place.name}</strong>
                <small>${place.area} · ${place.type}</small>
              </span>
              <span class="signal-row">
                ${place.signals.map((signal) => `<span>${icon(signalIcon(signal))}${signal}</span>`).join("")}
              </span>
              <span class="place-row-foot">
                <span>${icon("icon-clock")}${place.time}</span>
                <span>${place.confidence}</span>
              </span>
            </span>
            <span class="match-score">${place.score}%</span>
          </button>
        </article>
      `
    )
    .join("");
}

function renderDetail() {
  document.querySelector("#detailName").textContent = selectedPlace.name;
  document.querySelector("#detailScore").textContent = `${selectedPlace.score}%`;
  document.querySelector("#detailSummary").textContent = selectedPlace.summary;
  document.querySelector("#evidenceState").textContent = selectedPlace.confidence;
  document.querySelector("#updatedState").textContent = selectedPlace.updated;

  document.querySelector("#sensoryMeters").innerHTML = Object.entries(selectedPlace.meters)
    .map(
      ([key, value]) => `
        <div class="sensory-meter">
          <div>
            <span>${labels[key]}</span>
            <strong>${value}</strong>
          </div>
          <i aria-hidden="true"><b style="--level:${value}%"></b></i>
        </div>
      `
    )
    .join("");

  document.querySelector("#ontologySummary").innerHTML = `
    <strong>${selectedPlace.name}</strong>
    <span>${selectedPlace.type} · ${selectedPlace.mood}</span>
    <p>${selectedPlace.tradeoff}</p>
  `;

  document.querySelector("#relationList").innerHTML = selectedPlace.relations
    .map(
      ([source, relation, target]) => `
        <div class="relation-row">
          <span>${source}</span>
          <b>${relation}</b>
          <strong>${target}</strong>
        </div>
      `
    )
    .join("");
}

function selectPlace(id) {
  const next = places.find((place) => place.id === id);
  if (!next) return;
  selectedPlace = next;
  renderPlaceList();
  renderDetail();
  document.querySelectorAll(".map-pin").forEach((pin) => {
    pin.classList.toggle("active", pin.dataset.place === id);
    pin.setAttribute("aria-pressed", pin.dataset.place === id ? "true" : "false");
  });
}

document.addEventListener("click", (event) => {
  const target = event.target.closest("[data-place]");
  if (target) selectPlace(target.dataset.place);
});

renderPlaceList();
renderDetail();
