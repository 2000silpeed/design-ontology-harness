const teams = {
  MEX: { name: "멕시코" },
  RSA: { name: "남아공" },
  KOR: { name: "대한민국" },
  CZE: { name: "체코" },
  CAN: { name: "캐나다" },
  SUI: { name: "스위스" },
  USA: { name: "미국" },
  PAR: { name: "파라과이" },
  BRA: { name: "브라질" },
  MAR: { name: "모로코" },
  NED: { name: "네덜란드" },
  JPN: { name: "일본" },
  FRA: { name: "프랑스" },
  SEN: { name: "세네갈" },
  ENG: { name: "잉글랜드" },
  CRO: { name: "크로아티아" }
};

const fixtures = [
  {
    id: "m01",
    number: "M01",
    date: "2026-06-11",
    dateLabel: "6월 11일 목요일",
    kickoff: "20:00",
    city: "멕시코시티",
    group: "A",
    home: "MEX",
    away: "RSA",
    venue: "Estadio Azteca",
    status: "scheduled",
    spotlight: true,
    note: "개막전은 개최국의 첫 20분 압박과 남아공의 전환 속도를 함께 본다.",
    points: ["개최국 초반 점유", "남아공의 빠른 전환", "세트피스 첫 수비"],
    prediction: { home: 48, draw: 27, away: 25, total: 18420, model: "멕시코 근소 우세", confidence: "보통" }
  },
  {
    id: "m02",
    number: "M02",
    date: "2026-06-12",
    dateLabel: "6월 12일 금요일",
    kickoff: "21:00",
    city: "과달라하라",
    group: "A",
    home: "KOR",
    away: "CZE",
    venue: "Estadio Akron",
    status: "scheduled",
    spotlight: true,
    note: "대한민국의 조별리그 첫 경기. 중원 압박과 전환 속도가 핵심이다.",
    points: ["대한민국의 전방 압박", "체코 세트피스 대응", "후반 교체 카드"],
    prediction: { home: 39, draw: 30, away: 31, total: 22108, model: "접전", confidence: "낮음" }
  },
  {
    id: "m03",
    number: "M03",
    date: "2026-06-12",
    dateLabel: "6월 12일 금요일",
    kickoff: "15:00",
    city: "토론토",
    group: "B",
    home: "CAN",
    away: "SUI",
    venue: "BMO Field",
    status: "scheduled",
    spotlight: false,
    note: "캐나다의 홈 분위기와 스위스의 조직력이 마주하는 경기다.",
    points: ["캐나다 측면 전개", "스위스 수비 간격", "홈 관중의 영향"],
    prediction: { home: 33, draw: 28, away: 39, total: 9640, model: "스위스 근소 우세", confidence: "보통" }
  },
  {
    id: "m04",
    number: "M04",
    date: "2026-06-13",
    dateLabel: "6월 13일 토요일",
    kickoff: "18:00",
    city: "로스앤젤레스",
    group: "D",
    home: "USA",
    away: "PAR",
    venue: "SoFi Stadium",
    status: "scheduled",
    spotlight: false,
    note: "공동 개최국 미국의 첫 경기. 압박 강도와 전환 수비를 비교한다.",
    points: ["미국의 홈 템포", "파라과이 세컨드볼", "초반 경고 관리"],
    prediction: { home: 44, draw: 29, away: 27, total: 17620, model: "미국 우세", confidence: "보통" }
  },
  {
    id: "m05",
    number: "M05",
    date: "2026-06-13",
    dateLabel: "6월 13일 토요일",
    kickoff: "13:00",
    city: "뉴욕 / 뉴저지",
    group: "C",
    home: "BRA",
    away: "MAR",
    venue: "MetLife Stadium",
    status: "scheduled",
    spotlight: true,
    note: "브라질의 개인 전개와 모로코의 구조적 수비가 맞붙는 주목 경기다.",
    points: ["브라질의 좌측 전개", "모로코 미드블록", "전환 뒤 첫 패스"],
    prediction: { home: 47, draw: 25, away: 28, total: 25104, model: "브라질 우세", confidence: "보통" }
  },
  {
    id: "m06",
    number: "M06",
    date: "2026-06-14",
    dateLabel: "6월 14일 일요일",
    kickoff: "17:00",
    city: "댈러스",
    group: "F",
    home: "NED",
    away: "JPN",
    venue: "AT&T Stadium",
    status: "scheduled",
    spotlight: true,
    note: "네덜란드의 빌드업과 일본의 압박 회피가 대비되는 경기다.",
    points: ["일본의 2선 침투", "센터백 전진", "후방 빌드업"],
    prediction: { home: 42, draw: 30, away: 28, total: 14872, model: "네덜란드 근소 우세", confidence: "낮음" }
  },
  {
    id: "m07",
    number: "M24",
    date: "2026-06-18",
    dateLabel: "6월 18일 목요일",
    kickoff: "20:00",
    city: "멕시코시티",
    group: "A",
    home: "MEX",
    away: "KOR",
    venue: "Estadio Azteca",
    status: "scheduled",
    spotlight: true,
    note: "대한민국의 두 번째 경기. 고지대 적응과 원정 분위기가 변수다.",
    points: ["대한민국 측면 수비", "멕시코의 홈 압박", "전반 실점 억제"],
    prediction: { home: 45, draw: 29, away: 26, total: 24510, model: "멕시코 근소 우세", confidence: "보통" }
  },
  {
    id: "m08",
    number: "S01",
    date: "2026-05-16",
    dateLabel: "샘플 결과",
    kickoff: "완료",
    city: "예시 경기",
    group: "I",
    home: "FRA",
    away: "SEN",
    venue: "정적 데모 기록",
    status: "sample-result",
    spotlight: true,
    note: "2026 공식 결과가 아닌, 결과 화면의 정보 구조를 검증하는 샘플이다.",
    points: ["기록 검수 상태", "조별 영향 요약", "공식 피드 연결 전"],
    prediction: { home: 52, draw: 26, away: 22, total: 19804, model: "프랑스 우세", confidence: "보통" },
    result: { homeScore: 2, awayScore: 1, scorers: "샘플 득점 기록 2건", impact: "I조 상위권 경쟁 샘플", verification: "기록 검수용 데모" }
  },
  {
    id: "m09",
    number: "S02",
    date: "2026-05-16",
    dateLabel: "샘플 결과",
    kickoff: "완료",
    city: "예시 경기",
    group: "L",
    home: "ENG",
    away: "CRO",
    venue: "정적 데모 기록",
    status: "sample-result",
    spotlight: true,
    note: "완료된 경기를 보는 경우, 예측 대신 결과와 의견의 문맥이 우선된다.",
    points: ["스코어 라인", "조별 순위 반영", "팬 반응"],
    prediction: { home: 43, draw: 31, away: 26, total: 20960, model: "잉글랜드 근소 우세", confidence: "낮음" },
    result: { homeScore: 1, awayScore: 1, scorers: "샘플 득점 기록 2건", impact: "L조 승점 분배 샘플", verification: "기록 검수용 데모" }
  }
];

const seedOpinions = [
  { id: "o1", matchId: "m02", author: "bluepress", text: "첫 경기라 전반 20분 실점 억제가 더 중요해 보여요.", tags: ["KOR", "전술"], likes: 42, status: "loaded" },
  { id: "o2", matchId: "m02", author: "seoul-wing", text: "체코가 세트피스 강하면 코너킥 허용 수부터 줄여야 할 듯합니다.", tags: ["관전 포인트"], likes: 31, status: "loaded" },
  { id: "o3", matchId: "m01", author: "azteca-note", text: "개막전은 경기력만큼 분위기 관리가 중요하다고 봅니다.", tags: ["개막전"], likes: 57, status: "loaded" },
  { id: "o4", matchId: "m07", author: "redline", text: "멕시코전은 후반 교체 타이밍이 진짜 승부처일 것 같아요.", tags: ["KOR", "예측"], likes: 25, status: "loaded" },
  { id: "o5", matchId: "m05", author: "atlas", text: "브라질과 모로코는 조별리그여도 긴장감이 클 매치업입니다.", tags: ["주목 경기"], likes: 66, status: "loaded" }
];

const standingsA = [
  { code: "MEX", played: 0, points: 0, gd: "0", qualification: "진출권 경쟁" },
  { code: "KOR", played: 0, points: 0, gd: "0", qualification: "2위권 도전" },
  { code: "CZE", played: 0, points: 0, gd: "0", qualification: "접전권" },
  { code: "RSA", played: 0, points: 0, gd: "0", qualification: "이변 후보" }
];

const MAX_OPINION_LENGTH = 280;
const qaValue = new URLSearchParams(window.location.search).get("qa") || "";
const qaState = qaValue.includes(":") ? qaValue.split(":", 2) : null;

const state = {
  selectedMatchId: "m02",
  activeDate: "all",
  activeGroup: "all",
  activeStatus: "all",
  tickerFilter: "all",
  query: "",
  favoriteOnly: false,
  sortAscending: true,
  activeSection: "dashboard",
  theme: readStored("fixture-desk-theme", "light"),
  favorites: readStored("fixture-desk-favorites", { KOR: true }),
  votes: readStored("fixture-desk-votes", {}),
  draftVotes: {},
  opinions: readStored("fixture-desk-opinions", []),
  predictionStatus: "open-unselected",
  composerValue: "",
  composerConsent: false,
  composerTag: "관전 포인트",
  composerStatus: "empty",
  visualStatus: "planned",
  sourceStatus: "demo-data",
  discussionRulesExpanded: false
};

if (qaValue === "fixture-empty") {
  state.query = "일치하지 않는 fixture";
}

const element = {
  root: document.querySelector(".fixture-desk"),
  tickerItems: document.querySelector("#tickerItems"),
  dateRail: document.querySelector("#dateRail"),
  groupFilters: document.querySelector("#groupFilters"),
  scheduleRows: document.querySelector("#scheduleRows"),
  search: document.querySelector("#teamSearch"),
  searchCount: document.querySelector("#searchCount"),
  clearSearch: document.querySelector("#clearSearch"),
  sortDirection: document.querySelector("#sortDirection"),
  matchDetail: document.querySelector("#matchDetail"),
  predictionPanel: document.querySelector("#predictionPanel"),
  resultSummary: document.querySelector("#resultSummary"),
  standings: document.querySelector("#standings"),
  discussionThread: document.querySelector("#discussionThread"),
  opinionComposer: document.querySelector("#opinionComposer"),
  sourceLedger: document.querySelector("#sourceLedger"),
  visualContext: document.querySelector("#visualContext"),
  themeToggle: document.querySelector("#themeToggle"),
  favoriteOnly: document.querySelector("#favoriteOnly"),
  koreaMetric: document.querySelector("#koreaMetric"),
  visibleFixtureCount: document.querySelector("#visibleFixtureCount"),
  selectedFixtureMetric: document.querySelector("#selectedFixtureMetric"),
  fixtureDensitySummary: document.querySelector("#fixtureDensitySummary"),
  groupSpreadSummary: document.querySelector("#groupSpreadSummary")
};

function readStored(key, fallback) {
  try {
    const parsed = JSON.parse(window.localStorage.getItem(key));
    return parsed ?? fallback;
  } catch {
    return fallback;
  }
}

function store(key, value) {
  try {
    window.localStorage.setItem(key, JSON.stringify(value));
    return true;
  } catch {
    return false;
  }
}

function escapeHTML(value) {
  return String(value)
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;")
    .replaceAll("'", "&apos;");
}

function selectedFixture() {
  return fixtures.find((fixture) => fixture.id === state.selectedMatchId) || fixtures[0];
}

function teamName(code) {
  return teams[code]?.name || code;
}

function allOpinions() {
  return [...seedOpinions, ...state.opinions];
}

function fixtureOpinionCount(fixtureId) {
  return allOpinions().filter((opinion) => opinion.matchId === fixtureId).length;
}

function matchesFilters(fixture) {
  const query = state.query.trim().toLocaleLowerCase("ko-KR");
  const searchable = [
    fixture.group,
    fixture.city,
    fixture.venue,
    fixture.home,
    fixture.away,
    teamName(fixture.home),
    teamName(fixture.away)
  ].join(" ").toLocaleLowerCase("ko-KR");
  const dateMatch = state.activeDate === "all" || fixture.date === state.activeDate;
  const groupMatch = state.activeGroup === "all" || fixture.group === state.activeGroup;
  const statusMatch = state.activeStatus === "all" || fixture.status === state.activeStatus;
  const queryMatch = !query || searchable.includes(query);
  const favoriteMatch = !state.favoriteOnly || state.favorites[fixture.home] || state.favorites[fixture.away];
  return dateMatch && groupMatch && statusMatch && queryMatch && favoriteMatch;
}

function filteredFixtures() {
  return fixtures
    .filter(matchesFilters)
    .sort((left, right) => {
      if (left.status !== right.status) {
        return left.status === "sample-result" ? 1 : -1;
      }
      const a = `${left.date}-${left.kickoff}`;
      const b = `${right.date}-${right.kickoff}`;
      return state.sortAscending ? a.localeCompare(b) : b.localeCompare(a);
    });
}

function syncSelectedFixtureToVisible() {
  const visible = filteredFixtures();
  if (!visible.length || visible.some((fixture) => fixture.id === state.selectedMatchId)) return;
  const nextFixture = visible[0];
  state.selectedMatchId = nextFixture.id;
  state.predictionStatus = state.votes[nextFixture.id]
    ? "saved"
    : state.draftVotes[nextFixture.id]
      ? "open-selected"
      : "open-unselected";
  state.composerStatus = "empty";
  state.discussionRulesExpanded = false;
}

function tickerFixtures() {
  return fixtures.filter((fixture) => {
    if (state.tickerFilter === "korea") return fixture.home === "KOR" || fixture.away === "KOR";
    if (state.tickerFilter === "spotlight") return fixture.spotlight;
    if (state.tickerFilter === "opening") return fixture.date >= "2026-06-11" && fixture.date <= "2026-06-14";
    return true;
  });
}

function fixtureStateLabel(fixture) {
  return fixture.status === "sample-result" ? "샘플 결과" : "예정 · 데모";
}

function teamBadge(code, { selected = false } = {}) {
  const favorite = Boolean(state.favorites[code]);
  const badgeState = selected ? "selected" : favorite ? "favorite" : "default";
  return `
    <span class="team-badge" data-component-id="team-badge" data-component-part="flag-shape" data-component-state="${badgeState}" data-favorite="${favorite}">
      <span class="sr-only" data-component-part="flag-shape" aria-hidden="true"></span>
      <span class="team-code" data-component-part="team-code">${escapeHTML(code)}</span>
      <span class="team-name" data-component-part="accessible-team-name">${escapeHTML(teamName(code))}</span>
      <span data-component-part="favorite-marker-optional">${favorite ? "관심" : ""}</span>
      <button class="team-favorite" type="button" data-action="toggle-favorite" data-team="${escapeHTML(code)}" data-component-part="favorite-toggle" aria-pressed="${favorite}" aria-label="${escapeHTML(teamName(code))} 관심 팀 전환">${favorite ? "해제" : "관심"}</button>
    </span>
  `;
}

function renderMetrics() {
  const visible = filteredFixtures();
  const scheduled = visible.filter((fixture) => fixture.status === "scheduled");
  const days = ["2026-06-11", "2026-06-12", "2026-06-13", "2026-06-14", "2026-06-18"];
  const groups = ["A", "B", "C", "D", "F"];
  const koreaFixture = fixtures.find((fixture) => fixture.home === "KOR" || fixture.away === "KOR");
  element.visibleFixtureCount.textContent = String(visible.length);
  element.selectedFixtureMetric.textContent = selectedFixture().number;
  if (koreaFixture) element.koreaMetric.textContent = `${koreaFixture.dateLabel.replace("요일", "")}`;
  element.fixtureDensitySummary.textContent = scheduled.length
    ? `현재 필터 기준 예정 경기의 날짜별 분포: ${days.map((day) => {
      const count = scheduled.filter((fixture) => fixture.date === day).length;
      const label = fixtures.find((fixture) => fixture.date === day)?.dateLabel || day;
      return `${label} ${count}경기`;
    }).join(", ")}.`
    : "현재 필터에는 예정 경기가 없습니다.";
  element.groupSpreadSummary.textContent = scheduled.length
    ? `현재 필터 기준 예정 경기의 조별 분포: ${groups.map((group) => `${group}조 ${scheduled.filter((fixture) => fixture.group === group).length}경기`).join(", ")}.`
    : "현재 필터에는 예정 경기가 없습니다.";
}

function renderTicker() {
  const list = tickerFixtures();
  const tickerRoot = document.querySelector('[data-component-id="match-ticker"]');
  tickerRoot.dataset.componentState = list.length ? `${state.tickerFilter}-filter` : "empty-filter";
  tickerRoot.dataset.selectedMatchId = state.selectedMatchId;
  element.tickerItems.innerHTML = list.length
    ? list.map((fixture) => `
        <button
          class="ticker-item"
          type="button"
          data-action="select-match"
          data-match-id="${fixture.id}"
          data-component-part="match-ticker-item"
          aria-pressed="${fixture.id === state.selectedMatchId}"
          aria-label="${escapeHTML(fixture.number)} ${escapeHTML(fixture.dateLabel)}, ${escapeHTML(teamName(fixture.home))} 대 ${escapeHTML(teamName(fixture.away))}, ${escapeHTML(fixture.kickoff)} ${escapeHTML(fixture.city)}"
        >
          <small>${escapeHTML(fixture.number)}</small>
          <span class="ticker-match"><strong>${escapeHTML(teamName(fixture.home))} — ${escapeHTML(teamName(fixture.away))}</strong></span>
          <span class="ticker-kickoff">${escapeHTML(fixture.kickoff)}</span>
        </button>
      `).join("")
    : '<p class="thread-meta">선택한 묶음에 경기가 없습니다.</p>';
  document.querySelectorAll("[data-ticker-filter]").forEach((button) => {
    button.setAttribute("aria-pressed", String(button.dataset.tickerFilter === state.tickerFilter));
  });
}

function renderDateRail() {
  const dates = [...new Map(fixtures.filter((fixture) => fixture.status !== "sample-result").map((fixture) => [fixture.date, fixture.dateLabel])).entries()];
  const controls = dates.map(([date, label]) => {
    const count = fixtures.filter((fixture) => fixture.date === date).length;
    return `
      <button class="date-button" type="button" data-action="select-date" data-date="${date}" data-component-part="date-label" aria-pressed="${state.activeDate === date}">
        <span>${escapeHTML(label)}</span><small data-component-part="match-count">${count}경기</small><span data-component-part="active-marker" aria-hidden="true"></span>
      </button>
    `;
  }).join("");
  element.dateRail.innerHTML = `
    <button type="button" data-action="select-date" data-date="all" data-component-part="all-dates-action" aria-pressed="${state.activeDate === "all"}">전체 날짜</button>
    ${controls}
  `;
  const dateRoot = document.querySelector('[data-component-id="date-rail"]');
  dateRoot.dataset.componentState = state.activeDate === "all" ? "all-dates" : "date-selected";
}

function renderGroupFilters() {
  const groups = ["all", "A", "B", "C", "D", "F", "I", "L", "H"];
  element.groupFilters.innerHTML = groups.map((group) => {
    const count = group === "all" ? fixtures.length : fixtures.filter((fixture) => fixture.group === group).length;
    const disabled = group !== "all" && count === 0;
    const selected = state.activeGroup === group;
    const componentState = disabled ? "disabled-no-fixtures" : selected ? "selected" : "unselected";
    return `
      <button
        type="button"
        data-component-id="group-filter-chip"
        data-component-part="selected-surface"
        data-component-state="${componentState}"
        data-action="select-group"
        data-group="${group}"
        aria-pressed="${selected}"
        ${disabled ? "disabled" : ""}
      ><span data-component-part="chip-label">${group === "all" ? "전체 조" : `${group}조`}</span><small data-component-part="match-count-optional">${count}</small></button>
    `;
  }).join("");
}

function renderSearch() {
  const results = filteredFixtures().length;
  element.search.value = state.query;
  element.searchCount.textContent = `${results}개 경기`;
  element.clearSearch.hidden = !state.query;
  const searchRoot = document.querySelector('[data-component-id="team-search-field"]');
  if (!state.query) searchRoot.dataset.componentState = "empty";
  else searchRoot.dataset.componentState = results ? "results-found" : "no-results";
  element.favoriteOnly.setAttribute("aria-pressed", String(state.favoriteOnly));
  element.favoriteOnly.textContent = state.favoriteOnly ? "관심 팀만" : "관심 팀";
  document.querySelectorAll("[data-status-filter]").forEach((button) => {
    button.setAttribute("aria-pressed", String(button.dataset.statusFilter === state.activeStatus));
  });
}

function renderSchedule() {
  const list = filteredFixtures();
  const scheduleRoot = document.querySelector('[data-component-id="schedule-table"]');
  scheduleRoot.dataset.componentState = list.length ? (state.query || state.activeDate !== "all" || state.activeGroup !== "all" || state.activeStatus !== "all" ? "filtered" : "scheduled") : "empty";
  element.sortDirection.textContent = state.sortAscending ? "오름차순" : "내림차순";
  element.scheduleRows.innerHTML = list.length ? list.map((fixture) => {
    const selected = fixture.id === state.selectedMatchId;
    return `
      <tr data-component-part="fixture-row" data-match-id="${fixture.id}" data-selected="${selected}" data-component-state="${selected ? "selected-row" : fixture.status}">
        <td class="kickoff-cell" data-component-part="kickoff-cell" data-label="킥오프"><strong>${escapeHTML(fixture.dateLabel)}</strong><small>${escapeHTML(fixture.kickoff)} · ${escapeHTML(fixture.city)}</small></td>
        <td data-component-part="team-pair-cell" data-mobile-full="true" data-label="대진"><div class="team-pair">${teamBadge(fixture.home, { selected })}${teamBadge(fixture.away, { selected })}</div></td>
        <td data-component-part="group-cell" data-label="조 · 상태"><span class="fixture-group">${escapeHTML(fixture.group)}조</span><span class="fixture-status ${fixture.status === "sample-result" ? "is-sample" : ""}">${fixtureStateLabel(fixture)}</span></td>
        <td data-component-part="venue-cell" data-label="경기장"><span class="fixture-venue">${escapeHTML(fixture.venue)}</span></td>
        <td data-component-part="prediction-cell" data-label="팬 예상"><span class="fixture-prediction">${escapeHTML(fixture.prediction.model)}<br />팬 ${fixture.prediction.home}% · 무 ${fixture.prediction.draw}%</span></td>
        <td data-component-part="opinion-count-cell" data-label="의견"><span class="fixture-opinions">${fixtureOpinionCount(fixture.id)}개 의견</span></td>
        <td data-mobile-full="true" data-label="선택"><button class="row-select" type="button" data-action="select-match" data-match-id="${fixture.id}" aria-current="${selected ? "true" : "false"}">문맥 보기</button></td>
      </tr>
    `;
  }).join("") : `
    <tr class="empty-row" data-component-part="empty-row"><td colspan="7">현재 필터에는 일치하는 경기가 없습니다. 검색어 또는 필터를 조정해 주세요.</td></tr>
  `;
}

function renderMatchDetail() {
  const fixture = selectedFixture();
  const detailState = fixture.status === "sample-result" ? "sample-result" : "scheduled-predictable";
  const action = fixture.status === "sample-result"
    ? '<button class="primary-action" type="button" data-action="open-results" data-component-part="contextual-action">결과 문맥 보기</button>'
    : '<button class="primary-action" type="button" data-action="start-prediction" data-component-part="contextual-action">이 경기 예측하기</button>';
  element.matchDetail.innerHTML = `
    <section class="rail-section" data-component-id="match-detail-panel" data-component-part="match-identity" data-component-state="${detailState}" aria-labelledby="detailHeading">
      <div class="rail-heading">
        <div><p class="eyebrow">SELECTED MATCH</p><h2 id="detailHeading">${escapeHTML(fixture.number)} · ${escapeHTML(fixture.group)}조</h2></div>
        <span class="status-badge ${fixture.status === "sample-result" ? "is-sample" : "is-scheduled"}" data-component-part="status-badge">${fixtureStateLabel(fixture)}</span>
      </div>
      <p class="match-number">${escapeHTML(fixture.dateLabel)} · ${escapeHTML(fixture.kickoff)} · ${escapeHTML(fixture.city)}</p>
      <div class="versus-row" data-component-part="team-versus-row">${teamBadge(fixture.home, { selected: true })}<span class="versus-token">VS</span>${teamBadge(fixture.away, { selected: true })}</div>
      <p class="fixture-meta" data-component-part="kickoff-and-venue">${escapeHTML(fixture.venue)} · ${escapeHTML(fixture.city)}</p>
      <ul class="watch-list" data-component-part="watch-points">${fixture.points.map((point) => `<li>${escapeHTML(point)}</li>`).join("")}</ul>
      <p class="fixture-meta news-note" data-component-part="news-note">${escapeHTML(fixture.note)}</p>
      <div class="rail-actions">${action}<button class="secondary-action" type="button" data-action="focus-community">의견으로 이동</button><button class="secondary-action" type="button" data-action="inspect-news-source">출처 확인</button></div>
    </section>
  `;
}

function predictionChoiceName(choice, fixture) {
  if (choice === "home") return `${teamName(fixture.home)} 승`;
  if (choice === "away") return `${teamName(fixture.away)} 승`;
  return "무승부";
}

function renderPrediction() {
  const fixture = selectedFixture();
  const savedChoice = state.votes[fixture.id] || "";
  const selectedChoice = state.draftVotes[fixture.id] || savedChoice;
  const locked = fixture.status === "sample-result";
  const panelState = locked ? "locked-kickoff" : state.predictionStatus;
  const options = ["home", "draw", "away"].map((choice) => `
    <label class="prediction-option" data-component-part="poll-option">
      <input type="radio" name="prediction" value="${choice}" ${selectedChoice === choice ? "checked" : ""} ${locked ? "disabled" : ""} />
      <span>${escapeHTML(predictionChoiceName(choice, fixture))}</span>
      <strong>${fixture.prediction[choice]}%</strong>
    </label>
  `).join("");
  const saveLabel = state.predictionStatus === "saving" ? "저장 중" : state.predictionStatus === "saved" ? "저장됨" : "내 예측 저장";
  element.predictionPanel.innerHTML = `
    <section id="predictions" class="rail-section" data-component-id="prediction-panel" data-component-part="prediction-heading" data-component-state="${panelState}" aria-labelledby="predictionHeading">
      <div class="rail-heading"><div><p class="eyebrow">FAN FORECAST</p><h2 id="predictionHeading">팬 예상</h2></div><span class="confidence-badge is-${fixture.prediction.confidence === "높음" ? "high" : "medium"}" data-component-part="model-confidence-badge">모델 신뢰 ${escapeHTML(fixture.prediction.confidence)}</span></div>
      <form class="prediction-form" id="predictionForm">
        <fieldset data-component-part="choice-group"><legend>베팅이 아닌 팬 관점의 승부예측</legend><div class="prediction-options" data-component-part="home-draw-away-actions">${options}</div></fieldset>
        <div class="prediction-distribution" data-component-part="probability-distribution">
          <div class="distribution-line"><span>${escapeHTML(fixture.home)}</span><span class="distribution-track"><span style="inline-size: ${fixture.prediction.home}%"></span></span><strong>${fixture.prediction.home}%</strong></div>
          <div class="distribution-line is-draw"><span>무</span><span class="distribution-track"><span style="inline-size: ${fixture.prediction.draw}%"></span></span><strong>${fixture.prediction.draw}%</strong></div>
          <div class="distribution-line is-away"><span>${escapeHTML(fixture.away)}</span><span class="distribution-track"><span style="inline-size: ${fixture.prediction.away}%"></span></span><strong>${fixture.prediction.away}%</strong></div>
        </div>
        <canvas id="predictionChart" class="prediction-canvas" width="260" height="44" aria-label="${escapeHTML(fixture.number)} 팬 예상 분포"></canvas>
        <div class="prediction-summary"><p data-component-part="fan-total">팬 참여 ${fixture.prediction.total.toLocaleString("ko-KR")}명 · 정적 데모 집계</p><p data-component-part="model-opinion"><strong>모델 의견</strong> ${escapeHTML(fixture.prediction.model)}</p><p data-component-part="my-selection">내 선택: ${selectedChoice ? escapeHTML(predictionChoiceName(selectedChoice, fixture)) : "아직 선택하지 않음"}</p><p class="lock-notice" data-component-part="lock-notice">${locked ? "샘플 완료 경기는 읽기 전용입니다." : savedChoice ? "저장된 예측입니다. 선택을 바꾸면 다시 저장할 수 있습니다." : "예측은 이 데모 브라우저에만 저장됩니다."}</p></div>
        <div class="composer-actions"><button class="prediction-save" type="submit" ${locked || !selectedChoice || state.predictionStatus === "saving" ? "disabled" : ""}>${saveLabel}</button>${state.predictionStatus === "save-error" ? '<button class="secondary-action" type="button" data-action="retry-prediction">다시 저장</button>' : ""}</div>
      </form>
    </section>
  `;
}

function renderResultSummary() {
  const fixture = selectedFixture();
  const resultState = fixture.result ? "sample-result" : "no-results";
  element.resultSummary.innerHTML = fixture.result ? `
    <section class="result-section" data-component-id="result-summary-card" data-component-part="result-status" data-component-state="${resultState}" aria-labelledby="resultHeading">
      <div class="result-heading"><div><p class="eyebrow">RESULT LEDGER</p><h2 id="resultHeading">샘플 결과</h2></div><span class="verification-label is-demo" data-component-part="record-verification">${escapeHTML(fixture.result.verification)}</span></div>
      <div class="scoreline" data-component-part="team-scoreline"><span>${escapeHTML(teamName(fixture.home))}</span><strong>${fixture.result.homeScore} : ${fixture.result.awayScore}</strong><span>${escapeHTML(teamName(fixture.away))}</span></div>
      <p class="result-copy" data-component-part="scorer-summary">${escapeHTML(fixture.result.scorers)}</p><p class="result-copy" data-component-part="group-impact">${escapeHTML(fixture.result.impact)}</p>
      <button class="secondary-action" type="button" data-action="inspect-result-source">출처 상태 보기</button>
    </section>
  ` : `
    <section class="result-section" data-component-id="result-summary-card" data-component-part="result-status" data-component-state="${resultState}" aria-labelledby="resultHeading">
      <div class="result-heading"><div><p class="eyebrow">RESULT LEDGER</p><h2 id="resultHeading">결과 대기</h2></div><span class="verification-label is-demo" data-component-part="record-verification">정적 데모</span></div>
      <p class="result-copy" data-component-part="scorer-summary">선택한 예정 경기는 공식 결과가 없습니다.</p><p class="result-copy" data-component-part="group-impact">결과가 확정되면 조별 영향이 이 위치에 표시됩니다.</p><span class="scoreline" data-component-part="team-scoreline">결과 없음</span>
      <button class="secondary-action" type="button" data-action="inspect-result-source">출처 상태 보기</button>
    </section>
  `;
}

function renderStandings() {
  element.standings.innerHTML = `
    <section class="standings-section" data-component-id="standings-table" data-component-part="caption" data-component-state="pre-tournament-zeroed" aria-labelledby="standingsHeading">
      <div class="section-heading"><div><p class="eyebrow">GROUP A</p><h2 id="standingsHeading">조별 흐름</h2></div><button class="quiet-action" type="button" data-action="inspect-qualification-rule">진출 규칙</button></div>
      <div class="standings-table"><table><caption class="sr-only">A조 정적 데모 순위</caption><thead><tr><th scope="col" data-component-part="rank-column">순위</th><th scope="col" data-component-part="team-column">팀</th><th scope="col" data-component-part="played-column">경기</th><th scope="col" data-component-part="points-column">승점</th><th scope="col" data-component-part="goal-difference-column">득실</th><th scope="col" data-component-part="qualification-column">상태</th></tr></thead><tbody>${standingsA.map((row, index) => `<tr><td data-label="순위">${index + 1}</td><td data-label="팀"><button data-action="select-standings-team" data-team="${row.code}">${escapeHTML(teamName(row.code))}</button></td><td data-label="경기">${row.played}</td><td data-label="승점">${row.points}</td><td data-label="득실">${row.gd}</td><td data-label="상태">${escapeHTML(row.qualification)}</td></tr>`).join("")}</tbody></table></div>
      <p class="standings-copy" data-component-part="source-note">대회 전 정적 데모 · 공식 순위 피드 연결 전</p>
    </section>
  `;
}

function renderDiscussion() {
  const fixture = selectedFixture();
  const opinions = allOpinions().filter((opinion) => opinion.matchId === fixture.id);
  const threadState = opinions.length ? "loaded" : "empty-pre-match";
  const rules = state.discussionRulesExpanded
    ? '<p id="discussionRules" class="thread-rule-copy">신고된 의견은 즉시 비공개가 아니라 운영 검토 상태로 전환합니다. 경기와 무관한 비하·혐오·개인 공격은 숨김 처리될 수 있습니다.</p>'
    : "";
  element.discussionThread.innerHTML = `
    <section id="community" class="rail-section" data-component-id="discussion-thread" data-component-part="thread-heading" data-component-state="${threadState}" aria-labelledby="discussionHeading">
      <div class="rail-heading"><div><p class="eyebrow">FAN NOTES</p><h2 id="discussionHeading">${escapeHTML(fixture.number)} 의견</h2></div><span class="thread-meta">${opinions.length}개</span></div>
      <ul class="opinion-list" data-component-part="opinion-list">${opinions.length ? opinions.map((opinion) => `
        <li class="opinion-item ${opinion.status === "hidden-by-moderation" ? "is-hidden" : ""}" data-opinion-id="${opinion.id}" data-component-state="${opinion.status || "loaded"}">
          <div class="opinion-topline"><strong class="opinion-author" data-component-part="opinion-author">${escapeHTML(opinion.author)}</strong><span class="moderation-state" data-component-part="moderation-state">${opinion.status === "reported" ? "신고 접수" : opinion.status === "hidden-by-moderation" ? "운영 검토로 숨김" : "공개"}</span></div>
          <p class="opinion-body" data-component-part="opinion-body">${escapeHTML(opinion.text)}</p>
          <div class="tag-list" data-component-part="tag-list">${opinion.tags.map((tag) => `<span class="tag">${escapeHTML(tag)}</span>`).join("")}</div>
          <div class="opinion-actions"><button class="opinion-action" type="button" data-action="like-opinion" data-opinion-id="${opinion.id}" data-component-part="like-action">좋아요 ${opinion.likes}</button><button class="opinion-action" type="button" data-action="report-opinion" data-opinion-id="${opinion.id}" data-component-part="report-action">신고</button></div>
        </li>
      `).join("") : '<li data-component-part="empty-state" class="thread-meta">첫 의견을 남겨 이 경기의 관전 포인트를 시작해 주세요.</li>'}</ul>
      <button class="thread-rule-action" type="button" data-action="expand-hidden-reason" aria-expanded="${state.discussionRulesExpanded}" aria-controls="discussionRules">${state.discussionRulesExpanded ? "운영 기준 접기" : "운영 기준 보기"}</button>
      ${rules}
    </section>
  `;
}

function renderComposer() {
  const fixture = selectedFixture();
  const composerState = state.composerStatus;
  element.opinionComposer.innerHTML = `
    <section class="rail-section" data-component-id="opinion-composer" data-component-part="visible-label" data-component-state="${composerState}" aria-labelledby="composerHeading">
      <p class="eyebrow">WRITE A NOTE</p><h2 id="composerHeading" class="sr-only">의견 작성</h2>
      <form id="opinionForm"><label for="opinionText" data-component-part="visible-label">${escapeHTML(fixture.number)}에 의견 남기기</label><p class="context-hint" data-component-part="context-hint">상대를 낮추지 않고, 경기 장면과 근거를 중심으로 적어 주세요.</p>
      <textarea id="opinionText" class="composer-input" data-component-part="text-input" maxlength="${MAX_OPINION_LENGTH}" placeholder="예: 전반에는 수비 간격을 먼저 안정시키는 편이 좋아 보여요.">${escapeHTML(state.composerValue)}</textarea>
      <div class="composer-meta"><span data-component-part="character-count">${state.composerValue.length}/${MAX_OPINION_LENGTH}</span><select id="opinionTag" class="tag-select" data-component-part="tag-selector" aria-label="의견 태그"><option>관전 포인트</option><option>전술</option><option>대한민국</option><option>예측</option></select></div>
      <p class="moderation-copy" data-component-part="moderation-copy">국적 비하, 선수 개인 공격, 혐오 표현은 운영 기준에 따라 숨김 처리될 수 있습니다.</p>
      <label class="consent-line"><input id="moderationConsent" type="checkbox" data-component-part="moderation-consent" ${state.composerConsent ? "checked" : ""} />운영 기준에 동의하고 공개 의견을 작성합니다.</label>
      <div class="composer-actions"><button class="composer-submit" type="submit" data-component-part="submit-action" ${state.composerValue.trim() && state.composerConsent && composerState !== "submitting" ? "" : "disabled"}>의견 등록</button></div><p class="submission-status" data-component-part="submission-status" aria-live="polite">${composerMessage()}</p></form>
    </section>
  `;
  const tag = document.querySelector("#opinionTag");
  if (tag) tag.value = state.composerTag;
}

function composerMessage() {
  if (state.composerStatus === "submitted") return "의견이 이 브라우저의 데모 목록에 추가됐습니다.";
  if (state.composerStatus === "submit-error") return "저장하지 못했습니다. 작성한 문장은 유지됩니다.";
  if (state.composerStatus === "invalid") return "문장과 운영 기준 동의를 확인해 주세요.";
  return "";
}

function renderSourceLedger() {
  const sourceLabel = state.sourceStatus === "awaiting-official" ? "원문 확인 필요" : "정적 데모";
  element.sourceLedger.innerHTML = `
    <section class="ledger-section" data-runtime-surface="source-ledger" data-component-id="source-ledger" data-component-part="ledger-heading" data-component-state="${state.sourceStatus}" aria-labelledby="sourceHeading">
      <div class="ledger-heading"><div><p class="eyebrow">SOURCE LEDGER</p><h2 id="sourceHeading">데이터 출처</h2></div><span class="verification-label is-demo" data-component-part="verification-state">${sourceLabel}</span></div>
      <dl class="ledger-list" data-component-part="source-row-list">
        <div><dt data-component-part="domain-label">일정</dt><dd><a href="https://www.fifa.com/en/tournaments/mens/worldcup/canadamexicousa2026/articles/match-schedule-fixtures-results-teams-stadiums" data-component-part="source-name">FIFA 공식 일정 원문</a><br /><span data-component-part="data-mode">정적 fixture seed · 원문과 대조 필요</span> · <span data-component-part="updated-at">2026-05-16 KST</span></dd></div>
        <div><dt data-component-part="domain-label">결과</dt><dd><span data-component-part="source-name">공식 결과 연결 전</span><br /><span data-component-part="data-mode">샘플 결과는 UI 검증용</span></dd></div>
        <div><dt data-component-part="domain-label">팬 의견</dt><dd><span data-component-part="source-name">정적 예시와 이 브라우저의 로컬 입력</span><br /><span data-component-part="data-mode">서버 저장 없음</span></dd></div>
      </dl>
    </section>
  `;
}

function renderVisualContext() {
  const visualCopy = state.visualStatus === "asset-missing"
    ? "세부 fixture 맥락 이미지 후보는 현재 검수 전이라 화면에 노출하지 않습니다. 일정표 흐름은 이미지 없이 계속 사용할 수 있습니다."
    : "선택 방향 이미지는 형태 검토용 레퍼런스이며 런타임 자산이 아닙니다. fixture 맥락 raster는 검수 후에만 이 영역에 연결됩니다.";
  element.visualContext.innerHTML = `
    <section class="visual-section" data-component-id="generated-visual-context" data-component-part="visual-label" data-component-state="${state.visualStatus}" aria-labelledby="visualHeading">
      <div class="visual-heading"><div><p class="eyebrow">VISUAL PROVENANCE</p><h2 id="visualHeading">시각 자산 상태</h2></div><span class="visual-label" data-component-part="visual-label">${state.visualStatus === "asset-missing" ? "로드 보류" : "계획됨"}</span></div>
      <dl class="visual-record" data-component-part="generated-image"><div><dt>상태</dt><dd data-component-part="descriptive-alt">검수 전 생성 자산은 사용자 화면에 표시하지 않음</dd></div><div><dt>설명</dt><dd data-component-part="context-caption">${escapeHTML(visualCopy)}</dd></div><div><dt>근거</dt><dd data-component-part="provenance-reference">Semantic OS 토큰 · Fixture Compass 방향 문서 · 검수 전 asset registry</dd></div></dl>
      <button class="visual-action" type="button" data-action="check-asset">자산 로드 점검</button>
    </section>
  `;
}

function renderAll() {
  element.root.dataset.selectedMatchId = state.selectedMatchId;
  renderMetrics();
  renderTicker();
  renderDateRail();
  renderGroupFilters();
  renderSearch();
  renderSchedule();
  renderMatchDetail();
  renderPrediction();
  renderResultSummary();
  renderStandings();
  renderDiscussion();
  renderComposer();
  renderSourceLedger();
  renderVisualContext();
  updateNavigation();
  applyQaState();
  window.requestAnimationFrame(drawCharts);
}

function updateNavigation() {
  document.querySelectorAll("[data-section]").forEach((button) => {
    button.setAttribute("aria-current", button.dataset.section === state.activeSection ? "page" : "false");
  });
  document.querySelectorAll('[data-component-id="app-shell"]').forEach((node) => {
    if (node.classList.contains("fixture-desk")) node.dataset.componentState = state.activeSection === "schedule" ? "schedule-focused" : state.activeSection === "predictions" ? "prediction-focused" : state.activeSection === "community" ? "community-focused" : "dashboard";
  });
  document.querySelector('[data-component-id="top-navigation"]')?.setAttribute("data-component-state", `${state.activeSection}-active`);
}

function applyQaState() {
  if (!qaState) return;
  const [componentId, componentState] = qaState;
  document.querySelectorAll(`[data-component-id="${componentId}"]`).forEach((node) => {
    node.setAttribute("data-component-state", componentState);
  });
}

function restoreFocus(selector) {
  window.requestAnimationFrame(() => document.querySelector(selector)?.focus());
}

function selectMatch(matchId, { focusSelector = "" } = {}) {
  if (!fixtures.some((fixture) => fixture.id === matchId)) return;
  state.selectedMatchId = matchId;
  state.predictionStatus = state.votes[matchId] ? "saved" : state.draftVotes[matchId] ? "open-selected" : "open-unselected";
  state.composerStatus = "empty";
  renderAll();
  if (focusSelector) restoreFocus(focusSelector);
}

function focusSection(section) {
  state.activeSection = section;
  updateNavigation();
  const targetId = section === "dashboard" ? "statusHeading" : section === "schedule" ? "scheduleHeading" : section === "results" ? "resultHeading" : section === "predictions" ? "predictionHeading" : "discussionHeading";
  const target = document.querySelector(`#${targetId}`);
  if (target) {
    target.setAttribute("tabindex", "-1");
    target.scrollIntoView({ behavior: "smooth", block: "start" });
    target.focus({ preventScroll: true });
  }
}

function syncThemeToggle(componentState = `${state.theme}-active`) {
  element.themeToggle.dataset.componentState = componentState;
  element.themeToggle.setAttribute("aria-label", `${state.theme === "dark" ? "라이트" : "다크"} 테마로 전환`);
  element.themeToggle.querySelector('[data-component-part="next-theme-label"]').textContent = state.theme === "dark" ? "라이트 테마" : "다크 테마";
}

function toggleTheme() {
  state.theme = document.documentElement.dataset.theme === "dark" ? "light" : "dark";
  document.documentElement.dataset.theme = state.theme;
  const persisted = store("fixture-desk-theme", state.theme);
  syncThemeToggle(persisted ? `${state.theme}-active` : "preference-unavailable");
  window.requestAnimationFrame(drawCharts);
}

function drawCharts() {
  drawFixtureDensity();
  drawGroupSpread();
  drawPredictionDistribution();
}

function tokenValue(name) {
  return window.getComputedStyle(document.documentElement).getPropertyValue(name).trim();
}

function contextFor(id) {
  const canvas = document.querySelector(`#${id}`);
  return canvas instanceof HTMLCanvasElement ? canvas.getContext("2d") : null;
}

function drawFixtureDensity() {
  const ctx = contextFor("fixtureDensityChart");
  if (!ctx) return;
  const canvas = ctx.canvas;
  const days = ["2026-06-11", "2026-06-12", "2026-06-13", "2026-06-14", "2026-06-18"];
  const scheduled = filteredFixtures().filter((fixture) => fixture.status === "scheduled");
  const counts = days.map((day) => scheduled.filter((fixture) => fixture.date === day).length);
  const max = Math.max(...counts, 1);
  ctx.clearRect(0, 0, canvas.width, canvas.height);
  ctx.fillStyle = tokenValue("--ds-color-border");
  ctx.fillRect(0, canvas.height - 1, canvas.width, 1);
  counts.forEach((count, index) => {
    const width = 18;
    const gap = 12;
    const height = count ? Math.max(4, (count / max) * 30) : 0;
    if (!height) return;
    ctx.fillStyle = index === 1 ? tokenValue("--ds-color-success") : tokenValue("--ds-color-primary");
    ctx.fillRect(8 + index * (width + gap), canvas.height - height - 4, width, height);
  });
}

function drawGroupSpread() {
  const ctx = contextFor("groupSpreadChart");
  if (!ctx) return;
  const canvas = ctx.canvas;
  const scheduled = filteredFixtures().filter((fixture) => fixture.status === "scheduled");
  const groups = ["A", "B", "C", "D", "F"];
  const counts = groups.map((group) => scheduled.filter((fixture) => fixture.group === group).length);
  const max = Math.max(...counts, 1);
  ctx.clearRect(0, 0, canvas.width, canvas.height);
  ctx.fillStyle = tokenValue("--ds-color-border");
  ctx.fillRect(0, canvas.height - 1, canvas.width, 1);
  counts.forEach((count, index) => {
    const width = 18;
    const gap = 12;
    const height = count ? Math.max(4, (count / max) * 30) : 0;
    if (!height) return;
    const group = groups[index];
    ctx.fillStyle = state.activeGroup === group ? tokenValue("--ds-color-success") : tokenValue("--ds-color-primary");
    ctx.fillRect(8 + index * (width + gap), canvas.height - height - 4, width, height);
  });
}

function drawPredictionDistribution() {
  const ctx = contextFor("predictionChart");
  if (!ctx) return;
  const canvas = ctx.canvas;
  const fixture = selectedFixture();
  const values = [fixture.prediction.home, fixture.prediction.draw, fixture.prediction.away];
  const colors = [tokenValue("--ds-color-primary"), tokenValue("--ds-color-warning"), tokenValue("--ds-color-success")];
  ctx.clearRect(0, 0, canvas.width, canvas.height);
  let x = 0;
  values.forEach((value, index) => {
    const width = Math.round((value / 100) * canvas.width);
    ctx.fillStyle = colors[index];
    ctx.fillRect(x, 8, width, 28);
    x += width;
  });
}

function updateComposerState() {
  if (!state.composerValue) state.composerStatus = "empty";
  else if (state.composerValue.length >= MAX_OPINION_LENGTH) state.composerStatus = "limit-reached";
  else if (state.composerConsent) state.composerStatus = "typing-valid";
  else state.composerStatus = "invalid";
}

function submitPrediction() {
  const fixture = selectedFixture();
  const choice = state.draftVotes[fixture.id] || state.votes[fixture.id] || document.querySelector('input[name="prediction"]:checked')?.value;
  if (!choice || fixture.status === "sample-result") return;
  state.predictionStatus = "saving";
  renderPrediction();
  restoreFocus(".prediction-save");
  window.setTimeout(() => {
    if (qaValue === "prediction-panel:save-error") {
      state.predictionStatus = "save-error";
    } else {
      state.votes[fixture.id] = choice;
      delete state.draftVotes[fixture.id];
      store("fixture-desk-votes", state.votes);
      state.predictionStatus = "saved";
    }
    renderPrediction();
    restoreFocus(".prediction-save");
  }, 420);
}

function submitOpinion() {
  if (!state.composerValue.trim() || !state.composerConsent) {
    state.composerStatus = "invalid";
    renderComposer();
    restoreFocus(state.composerValue.trim() ? "#moderationConsent" : "#opinionText");
    return;
  }
  state.composerStatus = "submitting";
  renderComposer();
  restoreFocus(".composer-submit");
  window.setTimeout(() => {
    if (qaValue === "opinion-composer:submit-error") {
      state.composerStatus = "submit-error";
      renderComposer();
      restoreFocus(".composer-submit");
      return;
    }
    state.opinions.unshift({
      id: `local-${Date.now()}`,
      matchId: state.selectedMatchId,
      author: "내 메모",
      text: state.composerValue.trim(),
      tags: [state.composerTag],
      likes: 0,
      status: "loaded"
    });
    store("fixture-desk-opinions", state.opinions);
    state.composerValue = "";
    state.composerConsent = false;
    state.composerStatus = "submitted";
    renderDiscussion();
    renderComposer();
    restoreFocus("#opinionText");
  }, 360);
}

document.documentElement.dataset.theme = state.theme === "dark" ? "dark" : "light";
syncThemeToggle();

document.addEventListener("click", (event) => {
  const button = event.target.closest("button");
  if (!button) return;
  if (button.dataset.section) {
    focusSection(button.dataset.section);
    return;
  }
  if (button.dataset.tickerFilter) {
    state.tickerFilter = button.dataset.tickerFilter;
    renderTicker();
    restoreFocus(`[data-ticker-filter="${button.dataset.tickerFilter}"]`);
    return;
  }
  if (button.dataset.action === "select-match") {
    const focusSelector = button.classList.contains("row-select")
      ? `[data-match-id="${button.dataset.matchId}"].row-select`
      : `#tickerItems [data-match-id="${button.dataset.matchId}"]`;
    selectMatch(button.dataset.matchId, { focusSelector });
    return;
  }
  if (button.dataset.action === "select-date") {
    state.activeDate = button.dataset.date;
    syncSelectedFixtureToVisible();
    renderAll();
    restoreFocus(`[data-action="select-date"][data-date="${button.dataset.date}"]`);
    return;
  }
  if (button.dataset.action === "select-group") {
    state.activeGroup = button.dataset.group;
    syncSelectedFixtureToVisible();
    renderAll();
    restoreFocus(`[data-action="select-group"][data-group="${button.dataset.group}"]`);
    return;
  }
  if (button.dataset.statusFilter) {
    state.activeStatus = button.dataset.statusFilter;
    syncSelectedFixtureToVisible();
    renderAll();
    restoreFocus(`[data-status-filter="${button.dataset.statusFilter}"]`);
    return;
  }
  if (button.id === "favoriteOnly") {
    state.favoriteOnly = !state.favoriteOnly;
    syncSelectedFixtureToVisible();
    renderAll();
    restoreFocus("#favoriteOnly");
    return;
  }
  if (button.dataset.action === "toggle-favorite") {
    const code = button.dataset.team;
    state.favorites[code] = !state.favorites[code];
    if (!state.favorites[code]) delete state.favorites[code];
    store("fixture-desk-favorites", state.favorites);
    if (state.favoriteOnly) syncSelectedFixtureToVisible();
    renderAll();
    restoreFocus(`[data-action="toggle-favorite"][data-team="${code}"]`);
    return;
  }
  if (button.id === "sortKickoff") {
    state.sortAscending = !state.sortAscending;
    renderSchedule();
    restoreFocus("#sortKickoff");
    return;
  }
  if (button.id === "clearSearch") {
    state.query = "";
    syncSelectedFixtureToVisible();
    renderAll();
    window.requestAnimationFrame(() => element.search.focus());
    return;
  }
  if (button.id === "ledgerJump" || button.dataset.action === "inspect-news-source" || button.dataset.action === "inspect-result-source" || button.dataset.action === "inspect-source") {
    const sourceHeading = document.querySelector("#sourceHeading");
    sourceHeading?.setAttribute("tabindex", "-1");
    sourceHeading?.scrollIntoView({ behavior: "smooth", block: "center" });
    window.setTimeout(() => sourceHeading?.focus(), 250);
    return;
  }
  if (button.dataset.action === "start-prediction") {
    focusSection("predictions");
    return;
  }
  if (button.dataset.action === "open-results") {
    focusSection("results");
    return;
  }
  if (button.dataset.action === "focus-community") {
    focusSection("community");
    return;
  }
  if (button.dataset.action === "retry-prediction") {
    state.predictionStatus = "open-selected";
    renderPrediction();
    restoreFocus(".prediction-save");
    return;
  }
  if (button.dataset.action === "like-opinion" || button.dataset.action === "report-opinion") {
    const opinion = allOpinions().find((item) => item.id === button.dataset.opinionId);
    if (!opinion) return;
    if (button.dataset.action === "like-opinion") {
      opinion.likes += 1;
      opinion.status = "opinion-liked";
    } else {
      opinion.status = "reported";
    }
    renderDiscussion();
    restoreFocus(`[data-action="${button.dataset.action}"][data-opinion-id="${button.dataset.opinionId}"]`);
    return;
  }
  if (button.dataset.action === "expand-hidden-reason") {
    state.discussionRulesExpanded = !state.discussionRulesExpanded;
    renderDiscussion();
    restoreFocus("[data-action='expand-hidden-reason']");
    return;
  }
  if (button.dataset.action === "select-standings-team") {
    state.query = teamName(button.dataset.team);
    state.activeSection = "schedule";
    syncSelectedFixtureToVisible();
    renderAll();
    window.requestAnimationFrame(() => element.search.focus());
    return;
  }
  if (button.dataset.action === "inspect-qualification-rule") {
    state.sourceStatus = "awaiting-official";
    renderSourceLedger();
    return;
  }
  if (button.dataset.action === "check-asset") {
    state.visualStatus = "asset-missing";
    renderVisualContext();
  }
});

element.search.addEventListener("input", (event) => {
  state.query = event.target.value;
  syncSelectedFixtureToVisible();
  renderAll();
  window.requestAnimationFrame(() => {
    element.search.focus();
    element.search.setSelectionRange(state.query.length, state.query.length);
  });
});

document.addEventListener("submit", (event) => {
  if (event.target.id === "searchForm") {
    event.preventDefault();
    return;
  }
  if (event.target.id === "predictionForm") {
    event.preventDefault();
    submitPrediction();
    return;
  }
  if (event.target.id === "opinionForm") {
    event.preventDefault();
    submitOpinion();
  }
});

document.addEventListener("change", (event) => {
  if (event.target.matches('input[name="prediction"]')) {
    state.draftVotes[selectedFixture().id] = event.target.value;
    state.predictionStatus = "open-selected";
    renderPrediction();
    restoreFocus(`input[name="prediction"][value="${event.target.value}"]`);
  }
  if (event.target.id === "moderationConsent") {
    state.composerConsent = event.target.checked;
    updateComposerState();
    renderComposer();
    restoreFocus("#moderationConsent");
  }
  if (event.target.id === "opinionTag") {
    state.composerTag = event.target.value;
  }
});

document.addEventListener("input", (event) => {
  if (event.target.id === "opinionText") {
    state.composerValue = event.target.value.slice(0, MAX_OPINION_LENGTH);
    updateComposerState();
    renderComposer();
    window.requestAnimationFrame(() => {
      const input = document.querySelector("#opinionText");
      input?.focus();
      input?.setSelectionRange(state.composerValue.length, state.composerValue.length);
    });
  }
});

document.addEventListener("keydown", (event) => {
  const dateButton = event.target.closest?.("[data-action='select-date']");
  if (dateButton && ["ArrowRight", "ArrowLeft"].includes(event.key)) {
    const buttons = [...document.querySelectorAll("[data-action='select-date']")];
    const index = buttons.indexOf(dateButton);
    const next = event.key === "ArrowRight" ? buttons[index + 1] || buttons[0] : buttons[index - 1] || buttons.at(-1);
    event.preventDefault();
    next.focus();
  }
  const navButton = event.target.closest?.("[data-section]");
  if (navButton && ["ArrowRight", "ArrowLeft"].includes(event.key)) {
    const buttons = [...document.querySelectorAll("[data-section]")];
    const index = buttons.indexOf(navButton);
    const next = event.key === "ArrowRight" ? buttons[index + 1] || buttons[0] : buttons[index - 1] || buttons.at(-1);
    event.preventDefault();
    next.focus();
  }
});

element.themeToggle.addEventListener("click", toggleTheme);

renderAll();
