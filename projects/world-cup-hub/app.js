const teams = {
  MEX: { name: "멕시코", short: "MEX", color: "var(--team-mex)" },
  RSA: { name: "남아공", short: "RSA", color: "var(--team-rsa)" },
  KOR: { name: "대한민국", short: "KOR", color: "var(--team-kor)" },
  CZE: { name: "체코", short: "CZE", color: "var(--team-cze)" },
  CAN: { name: "캐나다", short: "CAN", color: "var(--team-can)" },
  SUI: { name: "스위스", short: "SUI", color: "var(--team-sui)" },
  USA: { name: "미국", short: "USA", color: "var(--team-usa)" },
  PAR: { name: "파라과이", short: "PAR", color: "var(--team-par)" },
  BRA: { name: "브라질", short: "BRA", color: "var(--team-bra)" },
  MAR: { name: "모로코", short: "MAR", color: "var(--team-mar)" },
  NED: { name: "네덜란드", short: "NED", color: "var(--team-ned)" },
  JPN: { name: "일본", short: "JPN", color: "var(--team-jpn)" },
  ESP: { name: "스페인", short: "ESP", color: "var(--team-esp)" },
  CPV: { name: "카보베르데", short: "CPV", color: "var(--team-cpv)" },
  FRA: { name: "프랑스", short: "FRA", color: "var(--team-fra)" },
  SEN: { name: "세네갈", short: "SEN", color: "var(--team-sen)" },
  ARG: { name: "아르헨티나", short: "ARG", color: "var(--team-arg)" },
  ALG: { name: "알제리", short: "ALG", color: "var(--team-alg)" },
  ENG: { name: "잉글랜드", short: "ENG", color: "var(--team-eng)" },
  CRO: { name: "크로아티아", short: "CRO", color: "var(--team-cro)" }
};

const matches = [
  {
    id: "m01",
    no: 1,
    group: "A",
    iso: "2026-06-11T20:00:00-06:00",
    localLabel: "6월 11일 20:00 · 멕시코시티",
    home: "MEX",
    away: "RSA",
    venue: "Estadio Azteca",
    city: "Mexico City",
    status: "scheduled",
    note: "개막전. 2010 남아공 대회 개막전과 같은 매치업.",
    points: ["개최국의 첫 경기 압박", "남아공의 역습 속도", "초반 세트피스 집중도"],
    prediction: { home: 48, draw: 27, away: 25, votes: 18420, confidence: "보통", model: "멕시코 근소 우세" }
  },
  {
    id: "m02",
    no: 2,
    group: "A",
    iso: "2026-06-11T21:00:00-06:00",
    localLabel: "6월 11일 21:00 · 과달라하라",
    home: "KOR",
    away: "CZE",
    venue: "Estadio Akron",
    city: "Guadalajara",
    status: "scheduled",
    note: "대한민국의 조별리그 첫 경기. 중원 압박과 전환 속도가 핵심.",
    points: ["대한민국의 전방 압박 효율", "체코의 장신 공격수 대응", "후반 교체 카드 타이밍"],
    prediction: { home: 39, draw: 30, away: 31, votes: 22108, confidence: "낮음", model: "접전" }
  },
  {
    id: "m03",
    no: 3,
    group: "B",
    iso: "2026-06-12T15:00:00-04:00",
    localLabel: "6월 12일 15:00 · 토론토",
    home: "CAN",
    away: "SUI",
    venue: "BMO Field",
    city: "Toronto",
    status: "scheduled",
    note: "캐나다의 홈 분위기와 스위스의 조직력이 맞붙는 경기.",
    points: ["캐나다 측면 전개", "스위스 수비 간격", "홈 응원 에너지"],
    prediction: { home: 33, draw: 28, away: 39, votes: 9640, confidence: "보통", model: "스위스 근소 우세" }
  },
  {
    id: "m04",
    no: 4,
    group: "D",
    iso: "2026-06-12T18:00:00-07:00",
    localLabel: "6월 12일 18:00 · 로스앤젤레스",
    home: "USA",
    away: "PAR",
    venue: "SoFi Stadium",
    city: "Los Angeles",
    status: "scheduled",
    note: "공동 개최국 미국의 첫 경기. 압박 강도와 전환 수비가 관전 포인트.",
    points: ["미국의 홈 템포", "파라과이의 세컨볼", "초반 경고 관리"],
    prediction: { home: 44, draw: 29, away: 27, votes: 17620, confidence: "보통", model: "미국 우세" }
  },
  {
    id: "m05",
    no: 5,
    group: "C",
    iso: "2026-06-13T13:00:00-04:00",
    localLabel: "6월 13일 13:00 · 뉴욕/뉴저지",
    home: "BRA",
    away: "MAR",
    venue: "MetLife Stadium",
    city: "New York / New Jersey",
    status: "scheduled",
    note: "브라질의 개인 전개와 모로코의 구조적 수비가 만나는 빅매치.",
    points: ["브라질의 좌측 overload", "모로코의 미드블록", "전환 후 첫 패스"],
    prediction: { home: 47, draw: 25, away: 28, votes: 25104, confidence: "보통", model: "브라질 우세" }
  },
  {
    id: "m06",
    no: 6,
    group: "F",
    iso: "2026-06-14T17:00:00-05:00",
    localLabel: "6월 14일 17:00 · 댈러스",
    home: "NED",
    away: "JPN",
    venue: "AT&T Stadium",
    city: "Dallas",
    status: "scheduled",
    note: "네덜란드의 피지컬 빌드업과 일본의 빠른 압박 회피가 충돌한다.",
    points: ["일본의 2선 침투", "네덜란드 센터백 전진", "후방 빌드업 실수 억제"],
    prediction: { home: 42, draw: 30, away: 28, votes: 14872, confidence: "낮음", model: "네덜란드 근소 우세" }
  },
  {
    id: "m07",
    no: 7,
    group: "H",
    iso: "2026-06-15T15:00:00-04:00",
    localLabel: "6월 15일 15:00 · 마이애미",
    home: "ESP",
    away: "CPV",
    venue: "Hard Rock Stadium",
    city: "Miami",
    status: "scheduled",
    note: "스페인의 점유와 카보베르데의 수비 전환이 대비되는 경기.",
    points: ["스페인의 하프스페이스 점유", "카보베르데의 첫 압박 회피", "세트피스 집중"],
    prediction: { home: 61, draw: 22, away: 17, votes: 12880, confidence: "높음", model: "스페인 우세" }
  },
  {
    id: "m08",
    no: 8,
    group: "I",
    iso: "2026-06-16T14:00:00-04:00",
    localLabel: "6월 16일 14:00 · 뉴욕/뉴저지",
    home: "FRA",
    away: "SEN",
    venue: "MetLife Stadium",
    city: "New York / New Jersey",
    status: "scheduled",
    note: "강력한 우승 후보와 아프리카 강호의 첫 라운드 매치.",
    points: ["프랑스의 속공 루트", "세네갈의 중앙 압박", "풀백 뒷공간 관리"],
    prediction: { home: 52, draw: 26, away: 22, votes: 19804, confidence: "보통", model: "프랑스 우세" }
  },
  {
    id: "m09",
    no: 9,
    group: "J",
    iso: "2026-06-16T18:00:00-05:00",
    localLabel: "6월 16일 18:00 · 캔자스시티",
    home: "ARG",
    away: "ALG",
    venue: "Arrowhead Stadium",
    city: "Kansas City",
    status: "scheduled",
    note: "아르헨티나의 점유 리듬과 알제리의 압박 대응이 관건.",
    points: ["아르헨티나의 10번 공간", "알제리의 측면 역습", "중원 파울 관리"],
    prediction: { home: 55, draw: 25, away: 20, votes: 23290, confidence: "보통", model: "아르헨티나 우세" }
  },
  {
    id: "m10",
    no: 10,
    group: "L",
    iso: "2026-06-17T15:00:00-04:00",
    localLabel: "6월 17일 15:00 · 토론토",
    home: "ENG",
    away: "CRO",
    venue: "BMO Field",
    city: "Toronto",
    status: "scheduled",
    note: "토너먼트급 긴장감의 조별리그 빅매치.",
    points: ["잉글랜드의 전방 조합", "크로아티아의 템포 조절", "후반 체력전"],
    prediction: { home: 43, draw: 31, away: 26, votes: 20960, confidence: "낮음", model: "잉글랜드 근소 우세" }
  },
  {
    id: "m11",
    no: 24,
    group: "A",
    iso: "2026-06-18T20:00:00-06:00",
    localLabel: "6월 18일 20:00 · 멕시코시티",
    home: "MEX",
    away: "KOR",
    venue: "Estadio Azteca",
    city: "Mexico City",
    status: "scheduled",
    note: "대한민국의 두 번째 경기. 원정 분위기와 고지대 적응이 변수.",
    points: ["대한민국의 측면 수비", "멕시코의 홈 압박", "전반 실점 억제"],
    prediction: { home: 45, draw: 29, away: 26, votes: 24510, confidence: "보통", model: "멕시코 근소 우세" }
  },
  {
    id: "m12",
    no: 43,
    group: "A",
    iso: "2026-06-24T20:00:00-06:00",
    localLabel: "6월 24일 20:00 · 몬테레이",
    home: "RSA",
    away: "KOR",
    venue: "Estadio BBVA",
    city: "Monterrey",
    status: "scheduled",
    note: "조별리그 최종전. 순위와 3위 진출 경우의 수가 동시에 걸릴 수 있다.",
    points: ["대한민국의 득실 관리", "남아공의 전환 속도", "동시 경기 스코어 체크"],
    prediction: { home: 27, draw: 31, away: 42, votes: 21104, confidence: "낮음", model: "대한민국 근소 우세" }
  },
  {
    id: "m13",
    no: 44,
    group: "A",
    iso: "2026-06-24T20:00:00-06:00",
    localLabel: "6월 24일 20:00 · 멕시코시티",
    home: "CZE",
    away: "MEX",
    venue: "Estadio Azteca",
    city: "Mexico City",
    status: "scheduled",
    note: "Group A 동시 최종전. 다른 경기와 함께 순위가 요동칠 수 있다.",
    points: ["체코의 세트피스", "멕시코의 볼 점유", "동시 경기 득실 변수"],
    prediction: { home: 29, draw: 31, away: 40, votes: 14780, confidence: "낮음", model: "멕시코 근소 우세" }
  }
];

const seedOpinions = [
  { id: "o1", matchId: "m02", author: "bluepress", text: "첫 경기라 무리한 라인보다 전반 20분 실점 억제가 더 중요해 보여요.", tags: ["KOR", "전술"], likes: 42, time: "12분 전" },
  { id: "o2", matchId: "m02", author: "seoul-wing", text: "체코가 세트피스 강하면 코너킥 허용 수부터 줄여야 할 듯.", tags: ["관전포인트"], likes: 31, time: "28분 전" },
  { id: "o3", matchId: "m01", author: "azteca-note", text: "개막전은 경기력보다 분위기 관리가 반은 먹고 들어간다고 봅니다.", tags: ["개막전"], likes: 57, time: "44분 전" },
  { id: "o4", matchId: "m11", author: "redline", text: "멕시코전은 후반 교체 타이밍이 진짜 승부처일 것 같아요.", tags: ["KOR", "예측"], likes: 25, time: "1시간 전" },
  { id: "o5", matchId: "m05", author: "atlas", text: "브라질-모로코는 조별리그인데 거의 16강 텐션.", tags: ["빅매치"], likes: 66, time: "2시간 전" }
];

const standingsA = [
  { team: "MEX", played: 0, points: 0, forecast: "진출권 경쟁" },
  { team: "KOR", played: 0, points: 0, forecast: "2위권 도전" },
  { team: "CZE", played: 0, points: 0, forecast: "접전권" },
  { team: "RSA", played: 0, points: 0, forecast: "이변 후보" }
];

const state = {
  selectedMatchId: "m02",
  activeDate: "all",
  activeGroup: "all",
  activeStatus: "all",
  tickerFilter: "all",
  query: "",
  theme: readStore("wch:theme", "light"),
  votes: readStore("wch:votes", {}),
  opinions: readStore("wch:opinions", [])
};

const elements = {
  daysUntil: document.querySelector("#daysUntil"),
  voteTotal: document.querySelector("#voteTotal"),
  tickerRail: document.querySelector("#tickerRail"),
  favoriteMatch: document.querySelector("#favoriteMatch"),
  dateRail: document.querySelector("#dateRail"),
  groupFilters: document.querySelector("#groupFilters"),
  scheduleRows: document.querySelector("#scheduleRows"),
  matchDetail: document.querySelector("#matchDetail"),
  insightRail: document.querySelector("#insightRail"),
  predictionPanel: document.querySelector("#predictionPanel"),
  resultsList: document.querySelector("#resultsList"),
  standingsRows: document.querySelector("#standingsRows"),
  discussionThread: document.querySelector("#discussionThread"),
  threadCount: document.querySelector("#threadCount"),
  search: document.querySelector("#matchSearch"),
  opinionForm: document.querySelector("#opinionForm"),
  opinionText: document.querySelector("#opinionText"),
  themeToggle: document.querySelector("[data-theme-toggle]")
};

function readStore(key, fallback) {
  try {
    return JSON.parse(localStorage.getItem(key)) ?? fallback;
  } catch {
    return fallback;
  }
}

function writeStore(key, value) {
  localStorage.setItem(key, JSON.stringify(value));
}

function escapeHtml(value) {
  return String(value)
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;")
    .replaceAll("'", "&#x27;");
}

function getTeam(code) {
  return teams[code];
}

function teamBadge(code) {
  const team = getTeam(code);
  return `
    <span class="team-badge flag-badge flag-${code.toLowerCase()}" style="--team-color:${team.color}" aria-label="${escapeHtml(team.name)} 국기">
      <span class="flag-shape" aria-hidden="true"></span>
      <span class="team-code">${team.short}</span>
    </span>
  `;
}

function icon(name, className = "ui-icon") {
  return `<svg class="${className}" aria-hidden="true"><use href="#icon-${name}" /></svg>`;
}

function applyTheme() {
  const theme = state.theme === "dark" ? "dark" : "light";
  const nextTheme = theme === "dark" ? "light" : "dark";
  document.documentElement.dataset.theme = theme;
  if (!elements.themeToggle) return;
  elements.themeToggle.setAttribute("aria-label", `${nextTheme === "dark" ? "다크" : "일반"} 모드로 전환`);
  elements.themeToggle.innerHTML = `
    ${icon(nextTheme === "dark" ? "moon" : "sun")}
    <span>${nextTheme === "dark" ? "다크" : "일반"}</span>
  `;
}

function dateKey(match) {
  return new Intl.DateTimeFormat("en-CA", {
    timeZone: "Asia/Seoul",
    year: "numeric",
    month: "2-digit",
    day: "2-digit"
  }).format(new Date(match.iso));
}

function formatKst(iso) {
  const date = new Date(iso);
  return new Intl.DateTimeFormat("ko-KR", {
    timeZone: "Asia/Seoul",
    month: "2-digit",
    day: "2-digit",
    weekday: "short",
    hour: "2-digit",
    minute: "2-digit"
  }).format(date);
}

function shortDateLabel(key) {
  if (key === "all") return "전체";
  const date = new Date(`${key}T00:00:00+09:00`);
  return new Intl.DateTimeFormat("ko-KR", {
    timeZone: "Asia/Seoul",
    month: "2-digit",
    day: "2-digit",
    weekday: "short"
  }).format(date);
}

function statusLabel(status) {
  return {
    scheduled: "예정",
    live: "진행",
    "sample-result": "샘플 결과"
  }[status] ?? status;
}

function matchFlavor(match) {
  const isKorea = [match.home, match.away].includes("KOR");
  const isOpening = match.no === 1;
  const isHighInterest = match.prediction.votes >= 20000;
  if (isOpening) return { label: "개막전", className: "safe" };
  if (isKorea) return { label: "대한민국 추적", className: "safe" };
  if (isHighInterest) return { label: "팬 관심", className: "" };
  return { label: statusLabel(match.status), className: "muted" };
}

function isOpeningWeek(match) {
  return dateKey(match) <= "2026-06-17";
}

function isSpotlight(match) {
  return [match.home, match.away].includes("KOR") || match.no === 1 || match.prediction.votes >= 20000;
}

function selectedMatch() {
  return matches.find((match) => match.id === state.selectedMatchId) ?? matches[0];
}

function predictionWithLocal(match) {
  const baseVotes = match.prediction.votes;
  const raw = {
    home: Math.round((match.prediction.home / 100) * baseVotes),
    draw: Math.round((match.prediction.draw / 100) * baseVotes),
    away: Math.round((match.prediction.away / 100) * baseVotes)
  };
  const localPick = state.votes[match.id];
  if (localPick) raw[localPick] += 1;
  const total = raw.home + raw.draw + raw.away;
  return {
    home: Math.round((raw.home / total) * 100),
    draw: Math.round((raw.draw / total) * 100),
    away: Math.round((raw.away / total) * 100),
    total
  };
}

function allOpinions() {
  return [...state.opinions, ...seedOpinions];
}

function updateSummary() {
  const opening = new Date("2026-06-11T20:00:00-06:00");
  const now = new Date();
  const days = Math.max(0, Math.ceil((opening - now) / 86400000));
  elements.daysUntil.textContent = `D-${days}`;
  const localVoteCount = Object.keys(state.votes).length;
  const seedTotal = matches.reduce((sum, match) => sum + match.prediction.votes, 0);
  elements.voteTotal.textContent = (seedTotal + localVoteCount).toLocaleString("ko-KR");
}

function tickerMatches() {
  const filtered = matches.filter((match) => {
    if (state.tickerFilter === "korea") return [match.home, match.away].includes("KOR");
    if (state.tickerFilter === "spotlight") return isSpotlight(match);
    if (state.tickerFilter === "opening") return isOpeningWeek(match);
    return true;
  });
  return filtered.slice(0, 10);
}

function renderTicker() {
  document.querySelectorAll("[data-ticker-filter]").forEach((button) => {
    button.classList.toggle("active", button.dataset.tickerFilter === state.tickerFilter);
  });

  const cards = tickerMatches();
  if (!cards.length) {
    elements.tickerRail.innerHTML = `<div class="empty-state compact-empty">조건에 맞는 경기 티커가 없습니다.</div>`;
    return;
  }

  elements.tickerRail.innerHTML = cards.map((match) => {
    const flavor = matchFlavor(match);
    const selected = state.selectedMatchId === match.id;
    const homeTeam = getTeam(match.home);
    const awayTeam = getTeam(match.away);
    return `
      <button class="ticker-card ${selected ? "selected" : ""}" type="button" data-select-match="${match.id}" aria-label="${escapeHtml(homeTeam.name)} vs ${escapeHtml(awayTeam.name)} · ${escapeHtml(flavor.label)} · ${escapeHtml(match.prediction.model)}">
        <span class="ticker-date">${shortDateLabel(dateKey(match))}</span>
        <span class="ticker-teams">
          ${teamBadge(match.home)}
          <span class="vs">vs</span>
          ${teamBadge(match.away)}
        </span>
        <span class="ticker-bottom">
          <span class="status-badge ${flavor.className}">${flavor.label}</span>
          <span>${escapeHtml(match.prediction.model)}</span>
        </span>
      </button>
    `;
  }).join("");
}

function renderFavorite() {
  const nextKorea = matches.find((match) => [match.home, match.away].includes("KOR"));
  const opponent = nextKorea.home === "KOR" ? getTeam(nextKorea.away) : getTeam(nextKorea.home);
  elements.favoriteMatch.innerHTML = `
    <div class="teams">
      ${teamBadge(nextKorea.home)}
      <span>${escapeHtml(getTeam(nextKorea.home).name)}</span>
      <span class="vs">vs</span>
      ${teamBadge(nextKorea.away)}
      <span>${escapeHtml(getTeam(nextKorea.away).name)}</span>
    </div>
    <dl class="detail-meta">
      <div><span class="meta-icon">${icon("clock")}</span><dt>내 시간</dt><dd>${formatKst(nextKorea.iso)} KST</dd></div>
      <div><span class="meta-icon">${icon("ball")}</span><dt>상대</dt><dd>${escapeHtml(opponent.name)}</dd></div>
      <div><span class="meta-icon">${icon("venue")}</span><dt>경기장</dt><dd>${escapeHtml(nextKorea.venue)}</dd></div>
      <div><span class="meta-icon">${icon("chart")}</span><dt>팬 전망</dt><dd>${escapeHtml(nextKorea.prediction.model)}</dd></div>
    </dl>
    <button class="secondary-button" type="button" data-select-match="${nextKorea.id}">경기 열기</button>
  `;
}

function renderInsightRail() {
  const match = selectedMatch();
  const nextKorea = matches.find((item) => [item.home, item.away].includes("KOR"));
  const topOpinion = [...allOpinions()].sort((a, b) => b.likes - a.likes)[0];
  const selectedOpinions = allOpinions().filter((opinion) => opinion.matchId === match.id);
  const threadLabel = `${selectedOpinions.length}개 의견`;
  const groupRows = standingsA.map((row) => `${getTeam(row.team).name}: ${row.forecast}`);

  elements.insightRail.innerHTML = `
    <article class="insight-item">
      <h3>${icon("star")}선택 경기</h3>
      <p>${escapeHtml(match.note)}</p>
      <div class="insight-meta">
        <span>${escapeHtml(match.prediction.model)}</span>
        <span>${threadLabel}</span>
      </div>
    </article>
    <article class="insight-item">
      <h3>${icon("pulse")}대한민국 추적</h3>
      <p>${escapeHtml(nextKorea.note)}</p>
      <span class="status-badge safe">${shortDateLabel(dateKey(nextKorea))}</span>
    </article>
    <article class="insight-item">
      <h3>${icon("message")}팬 반응</h3>
      <p>${escapeHtml(topOpinion.text)}</p>
      <div class="insight-meta">
        <span>${escapeHtml(topOpinion.author)}</span>
        <span>${topOpinion.likes} 좋아요</span>
      </div>
    </article>
    <article class="insight-item">
      <h3>${icon("bracket")}Group A 경우의 수</h3>
      <ul>
        ${groupRows.map((row) => `<li>${escapeHtml(row)}</li>`).join("")}
      </ul>
    </article>
  `;
}

function renderDateRail() {
  const keys = [...new Set(matches.map(dateKey))].sort();
  const buttons = [
    `<button class="date-button ${state.activeDate === "all" ? "active" : ""}" type="button" data-date-filter="all"><strong>전체</strong><span>${matches.length}경기</span></button>`,
    ...keys.map((key) => {
      const count = matches.filter((match) => dateKey(match) === key).length;
      return `<button class="date-button ${state.activeDate === key ? "active" : ""}" type="button" data-date-filter="${key}"><strong>${shortDateLabel(key)}</strong><span>${count}경기</span></button>`;
    })
  ];
  elements.dateRail.innerHTML = buttons.join("");
}

function renderGroupFilters() {
  const groups = ["all", ..."ABCDEFGHIJKL"];
  elements.groupFilters.innerHTML = groups.map((group) => {
    const label = group === "all" ? "전체 조" : `Group ${group}`;
    return `<button class="chip ${state.activeGroup === group ? "active" : ""}" type="button" data-group-filter="${group}">${label}</button>`;
  }).join("");
}

function filteredMatches() {
  const query = state.query.trim().toLowerCase();
  return matches.filter((match) => {
    const teamNames = `${getTeam(match.home).name} ${getTeam(match.away).name} ${match.home} ${match.away}`.toLowerCase();
    const haystack = `${teamNames} ${match.group} ${match.venue} ${match.city} ${match.note}`.toLowerCase();
    return (
      (state.activeDate === "all" || dateKey(match) === state.activeDate) &&
      (state.activeGroup === "all" || match.group === state.activeGroup) &&
      (state.activeStatus === "all" || match.status === state.activeStatus) &&
      (!query || haystack.includes(query))
    );
  });
}

function renderSchedule() {
  const rows = filteredMatches();
  if (!rows.length) {
    elements.scheduleRows.innerHTML = `
      <tr>
        <td colspan="6">
          <div class="empty-state">조건에 맞는 경기 샘플이 없습니다. 다른 날짜나 조를 선택해 보세요.</div>
        </td>
      </tr>
    `;
    return;
  }
  elements.scheduleRows.innerHTML = rows.map((match) => {
    const prediction = predictionWithLocal(match);
    const selected = state.selectedMatchId === match.id;
    const homeTeam = getTeam(match.home);
    const awayTeam = getTeam(match.away);
    const top = [
      { key: "home", label: homeTeam.name, value: prediction.home },
      { key: "draw", label: "무승부", value: prediction.draw },
      { key: "away", label: awayTeam.name, value: prediction.away }
    ].sort((a, b) => b.value - a.value)[0];
    const threadCount = allOpinions().filter((opinion) => opinion.matchId === match.id).length;
    const selectionLabel = `${homeTeam.name} 대 ${awayTeam.name} 경기${selected ? ", 현재 선택됨" : " 선택"}`;
    return `
      <tr class="schedule-row ${selected ? "selected" : ""}">
        <td>
          <div class="time-cell">
            <strong>${formatKst(match.iso)}</strong>
            <span>${escapeHtml(match.localLabel)}</span>
          </div>
        </td>
        <td>
          <button
            class="matchup schedule-match-button"
            type="button"
            data-select-match="${match.id}"
            data-selection-surface="schedule"
            aria-label="${escapeHtml(selectionLabel)}"
            aria-pressed="${selected}"
          >
            <span class="teams">
              ${teamBadge(match.home)}
              <span>${escapeHtml(homeTeam.name)}</span>
              <span class="vs">vs</span>
              ${teamBadge(match.away)}
              <span>${escapeHtml(awayTeam.name)}</span>
            </span>
            <span class="match-note">${escapeHtml(match.note)}</span>
          </button>
        </td>
        <td><span class="group-pill">${match.group}</span></td>
        <td>
          <div class="venue-cell">
            ${icon("venue")}
            <div>${escapeHtml(match.venue)}<br><span class="match-note">${escapeHtml(match.city)}</span></div>
          </div>
        </td>
        <td>
          <div class="prediction-mini">
            <span>${escapeHtml(top.label)} ${top.value}%</span>
            <div class="mini-bar"><i style="--value:${top.value}%"></i></div>
          </div>
        </td>
        <td>${threadCount}</td>
      </tr>
    `;
  }).join("");
}

function renderMatchDetail() {
  const match = selectedMatch();
  elements.matchDetail.innerHTML = `
    <div class="panel-heading">
      <div>
        <p class="eyebrow">match ${match.no}</p>
        <h2 id="match-title">${escapeHtml(getTeam(match.home).name)} vs ${escapeHtml(getTeam(match.away).name)}</h2>
      </div>
      <span class="status-badge ${match.status === "live" ? "live" : ""}">${statusLabel(match.status)}</span>
    </div>
    <div class="match-detail">
      <div class="teams">
        ${teamBadge(match.home)}
        <span>${escapeHtml(getTeam(match.home).name)}</span>
        <span class="vs">vs</span>
        ${teamBadge(match.away)}
        <span>${escapeHtml(getTeam(match.away).name)}</span>
      </div>
      <dl class="detail-meta">
        <div><span class="meta-icon">${icon("clock")}</span><dt>킥오프</dt><dd>${formatKst(match.iso)} KST</dd></div>
        <div><span class="meta-icon">${icon("whistle")}</span><dt>현지 시간</dt><dd>${escapeHtml(match.localLabel)}</dd></div>
        <div><span class="meta-icon">${icon("venue")}</span><dt>경기장</dt><dd>${escapeHtml(match.venue)}</dd></div>
        <div><span class="meta-icon">${icon("bracket")}</span><dt>조</dt><dd>Group ${match.group}</dd></div>
      </dl>
      <ul class="talking-points">
        ${match.points.map((point) => `<li>${escapeHtml(point)}</li>`).join("")}
      </ul>
      <button class="primary-button" type="button" data-scroll-target="predictions">예측 보기</button>
    </div>
  `;
}

function renderPrediction() {
  const match = selectedMatch();
  const prediction = predictionWithLocal(match);
  const localPick = state.votes[match.id];
  const bars = [
    { key: "home", label: getTeam(match.home).name, value: prediction.home, color: "var(--ds-color-success)" },
    { key: "draw", label: "무승부", value: prediction.draw, color: "var(--ds-color-warning)" },
    { key: "away", label: getTeam(match.away).name, value: prediction.away, color: "var(--ds-color-info)" }
  ];
  elements.predictionPanel.innerHTML = `
    <article class="prediction-card">
      <h3 class="card-title">${icon("vote")}<span>${escapeHtml(getTeam(match.home).name)} vs ${escapeHtml(getTeam(match.away).name)}</span></h3>
      <p>팬 투표 ${prediction.total.toLocaleString("ko-KR")}개 기준. 편집자 모델 의견: ${escapeHtml(match.prediction.model)} · 신뢰도 ${escapeHtml(match.prediction.confidence)}</p>
      <div class="probability-list">
        ${bars.map((bar) => `
          <div class="probability-item">
            <span>${escapeHtml(bar.label)}</span>
            <div class="probability-track"><i style="--value:${bar.value}%;--bar-color:${bar.color}"></i></div>
            <strong>${bar.value}%</strong>
          </div>
        `).join("")}
      </div>
      <div class="vote-actions" aria-label="승부예측 선택">
        ${bars.map((bar) => `<button class="${localPick === bar.key ? "active" : ""}" type="button" data-vote="${bar.key}">${escapeHtml(bar.label)}</button>`).join("")}
      </div>
    </article>
  `;
}

function renderResults() {
  elements.resultsList.innerHTML = `
    <article class="result-card">
      <div class="scoreline">
        <span class="score-label">${icon("source")}<span>2026 본선 공식 결과</span></span>
        <span>대기</span>
      </div>
      <p>현재는 대회 전 상태라 공식 본선 결과가 없습니다. 경기 종료 후에는 스코어, 득점 요약, 조별 순위 영향이 이 영역에 쌓입니다.</p>
      <span class="status-badge muted">2026-05-16 기준</span>
    </article>
    <article class="result-card">
      <div class="scoreline">
        <span class="score-label">${icon("ball")}<span>샘플 UI</span></span>
        <span>2 - 1</span>
      </div>
      <p>결과 카드의 표시 방식만 확인하기 위한 샘플입니다. 공식 경기 결과가 아니며 실제 데이터 연동 시 자동으로 교체됩니다.</p>
      <span class="status-badge">조별 영향 요약 자리</span>
    </article>
  `;
}

function renderStandings() {
  elements.standingsRows.innerHTML = standingsA.map((row) => `
    <tr>
      <td>
        <div class="team-name">
          ${teamBadge(row.team)}
          <span>${escapeHtml(getTeam(row.team).name)}</span>
        </div>
      </td>
      <td>${row.played}</td>
      <td>${row.points}</td>
      <td>${escapeHtml(row.forecast)}</td>
    </tr>
  `).join("");
}

function renderDiscussion() {
  const match = selectedMatch();
  const opinions = allOpinions().filter((opinion) => opinion.matchId === match.id);
  elements.threadCount.textContent = `${opinions.length}개`;
  if (!opinions.length) {
    elements.discussionThread.innerHTML = `<div class="empty-state">아직 이 경기에는 의견이 없습니다. 첫 관전 포인트를 남겨보세요.</div>`;
    return;
  }
  elements.discussionThread.innerHTML = opinions.map((opinion) => `
    <article class="opinion-card">
      <header>
        <strong>${escapeHtml(opinion.author)}</strong>
        <span>${escapeHtml(opinion.time)}</span>
      </header>
      <p>${escapeHtml(opinion.text)}</p>
      <div class="opinion-tags">
        ${opinion.tags.map((tag) => `<span class="tag">${escapeHtml(tag)}</span>`).join("")}
        <span class="tag">${opinion.likes} 좋아요</span>
      </div>
    </article>
  `).join("");
}

function renderAll() {
  updateSummary();
  renderTicker();
  renderFavorite();
  renderDateRail();
  renderGroupFilters();
  renderSchedule();
  renderMatchDetail();
  renderInsightRail();
  renderPrediction();
  renderResults();
  renderStandings();
  renderDiscussion();
}

document.addEventListener("click", (event) => {
  const themeButton = event.target.closest("[data-theme-toggle]");
  if (themeButton) {
    state.theme = state.theme === "dark" ? "light" : "dark";
    writeStore("wch:theme", state.theme);
    applyTheme();
    return;
  }

  const dateButton = event.target.closest("[data-date-filter]");
  if (dateButton) {
    state.activeDate = dateButton.dataset.dateFilter;
    renderAll();
    return;
  }

  const groupButton = event.target.closest("[data-group-filter]");
  if (groupButton) {
    state.activeGroup = groupButton.dataset.groupFilter;
    renderAll();
    return;
  }

  const statusButton = event.target.closest("[data-status-filter]");
  if (statusButton) {
    state.activeStatus = statusButton.dataset.statusFilter;
    document.querySelectorAll("[data-status-filter]").forEach((button) => {
      button.classList.toggle("active", button === statusButton);
    });
    renderSchedule();
    return;
  }

  const tickerButton = event.target.closest("[data-ticker-filter]");
  if (tickerButton) {
    state.tickerFilter = tickerButton.dataset.tickerFilter;
    renderTicker();
    return;
  }

  const selectButton = event.target.closest("[data-select-match]");
  if (selectButton) {
    const matchId = selectButton.dataset.selectMatch;
    const selectionSurface = selectButton.dataset.selectionSurface;
    state.selectedMatchId = matchId;
    renderTicker();
    renderSchedule();
    renderMatchDetail();
    renderInsightRail();
    renderPrediction();
    renderDiscussion();
    if (selectionSurface) {
      requestAnimationFrame(() => {
        const replacement = [...document.querySelectorAll("[data-selection-surface]")]
          .find((control) => control.dataset.selectionSurface === selectionSurface && control.dataset.selectMatch === matchId);
        replacement?.focus({ preventScroll: true });
      });
    }
    return;
  }

  const voteButton = event.target.closest("[data-vote]");
  if (voteButton) {
    state.votes[state.selectedMatchId] = voteButton.dataset.vote;
    writeStore("wch:votes", state.votes);
    renderAll();
    return;
  }

  const scrollButton = event.target.closest("[data-scroll-target]");
  if (scrollButton) {
    const target = document.querySelector(`#${scrollButton.dataset.scrollTarget}`);
    if (target) target.scrollIntoView({ behavior: "smooth", block: "start" });
    document.querySelectorAll(".nav-button").forEach((button) => {
      button.classList.toggle("active", button.dataset.scrollTarget === scrollButton.dataset.scrollTarget);
    });
  }
});

elements.search.addEventListener("input", (event) => {
  state.query = event.target.value;
  renderSchedule();
});

elements.opinionForm.addEventListener("submit", (event) => {
  event.preventDefault();
  const text = elements.opinionText.value.trim();
  if (!text) return;
  state.opinions.unshift({
    id: `local-${Date.now()}`,
    matchId: state.selectedMatchId,
    author: "나",
    text,
    tags: ["내 의견"],
    likes: 0,
    time: "방금"
  });
  writeStore("wch:opinions", state.opinions);
  elements.opinionText.value = "";
  renderInsightRail();
  renderDiscussion();
});

applyTheme();
renderAll();
