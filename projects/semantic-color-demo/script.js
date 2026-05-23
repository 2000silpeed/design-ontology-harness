function kw(role, name, hex, path, tags = []) {
  const [spectrum = "mixed", family = "semantic"] = path.split(".");

  return {
    role,
    name,
    hex,
    path,
    spectrum,
    family,
    mood: tags,
  };
}

const scenarios = {
  blue: {
    title: "딥 블루 cold luxury 웹 팔레트 후보",
    copy:
      "딥 블루 계열 브랜드 웹사이트를 원본 조합표가 아니라 화면 역할, 대비 이유, caveat로 재배치합니다.",
    signal: "digital_brand_website",
    mapFocus: "blue · cold depth · highlight air",
    contrast: "role/reason/caveat",
    warning:
      "첫 후보는 Semantic OS 프로토타입의 selected pattern입니다. 나머지는 같은 color keyword pool에서 대상별 후보로 확장한 변형입니다.",
    preview: {
      kicker: "Deep Blue Material",
      headline: "NOX METHOD",
      metricOne: "4",
      metricTwo: "6",
      metricThree: "OK",
    },
    candidatePalettes: [
      {
        name: "Source Pattern Anchor",
        note: "original deep-blue prototype roles",
        colors: [
          kw("anchor_background", "Navy Blue", "#000080", "blue.deep", ["신뢰", "권위", "집중"]),
          kw("depth_support", "Prussian Blue", "#003153", "blue.deep", ["고전", "예술", "집중"]),
          kw("interface_surface", "Classic Blue", "#0F4C81", "blue.pantone_trend", ["신뢰", "평온함", "지성"]),
          kw("highlight_air", "Ice Blue", "#D6EAF8", "blue.pastel", ["정제됨", "청결함", "섬세함"]),
          kw("proof_light", "Powder Blue", "#B0E0E6", "blue.pastel", ["부드러움", "균형감", "온화함"]),
        ],
      },
      {
        name: "Cerulean Interface",
        note: "clear blue with a colder action layer",
        colors: [
          kw("anchor_background", "Prussian Blue", "#003153", "blue.deep", ["고전", "집중"]),
          kw("depth_support", "Navy Blue", "#000080", "blue.deep", ["신뢰", "권위"]),
          kw("interface_surface", "Cerulean", "#2A52BE", "blue.standard", ["명료함", "신뢰"]),
          kw("highlight_air", "Ice Blue", "#D6EAF8", "blue.pastel", ["정제됨", "청결함"]),
          kw("edge_signal", "Super Sonic", "#0071A8", "blue.pantone_trend", ["혁신적", "역동적"]),
        ],
      },
      {
        name: "Architectural Glass",
        note: "matte depth and frosted highlight",
        colors: [
          kw("anchor_background", "Navy Blue", "#000080", "blue.deep", ["신뢰", "집중"]),
          kw("depth_support", "Classic Blue", "#0F4C81", "blue.pantone_trend", ["지성", "평온함"]),
          kw("interface_surface", "Ocean Blue", "#4F97A3", "blue.natural", ["신뢰", "정화", "깊이감"]),
          kw("highlight_air", "Misty Blue", "#B5C7EB", "blue.pastel", ["차분함", "사색적"]),
          kw("fine_line", "Ice Blue", "#D6EAF8", "blue.pastel", ["섬세함", "청결함"]),
        ],
      },
      {
        name: "Cold Luxury Editorial",
        note: "blue system with restrained violet proof",
        colors: [
          kw("anchor_background", "Prussian Blue", "#003153", "blue.deep", ["고전", "예술"]),
          kw("depth_support", "Midnight Violet", "#2E1A47", "violet.deep", ["고요함", "절제"]),
          kw("interface_surface", "Classic Blue", "#0F4C81", "blue.pantone_trend", ["신뢰", "지성"]),
          kw("highlight_air", "Ice Blue", "#D6EAF8", "blue.pastel", ["정제됨", "섬세함"]),
          kw("accent_proof", "Lavender Violet", "#967BB6", "violet.natural", ["평온함", "세련"]),
        ],
      },
      {
        name: "Technical Trust",
        note: "more interface-forward, less ceremonial",
        colors: [
          kw("anchor_background", "Classic Blue", "#0F4C81", "blue.pantone_trend", ["신뢰", "지성"]),
          kw("depth_support", "Prussian Blue", "#003153", "blue.deep", ["집중", "고전"]),
          kw("interface_surface", "Teal Blue", "#01889F", "blue.natural", ["개방감", "명료함"]),
          kw("highlight_air", "Powder Blue", "#B0E0E6", "blue.pastel", ["균형감", "온화함"]),
          kw("edge_signal", "Blue Atoll", "#00B1D2", "blue.pantone_trend", ["생기", "젊음"]),
        ],
      },
      {
        name: "Quiet Premium",
        note: "blue depth with a limited warm proof",
        colors: [
          kw("anchor_background", "Navy Blue", "#000080", "blue.deep", ["권위", "전문성"]),
          kw("depth_support", "Prussian Blue", "#003153", "blue.deep", ["고전", "집중"]),
          kw("interface_surface", "Classic Blue", "#0F4C81", "blue.pantone_trend", ["평온함", "지성"]),
          kw("highlight_air", "Ice Blue", "#D6EAF8", "blue.pastel", ["정제됨", "청결함"]),
          kw("proof_accent", "Copper", "#B87333", "orange.deep", ["고급스러움", "전통"]),
        ],
      },
    ],
    recommendations: [
      ["Navy Blue", "#000080", "blue.deep"],
      ["Prussian Blue", "#003153", "blue.deep"],
      ["Classic Blue", "#0F4C81", "blue.pantone_trend"],
      ["Ice Blue", "#D6EAF8", "blue.pastel"],
      ["Super Sonic", "#0071A8", "blue.pantone_trend"],
    ],
  },
  green: {
    title: "안정적인 그린 서비스 UI 팔레트 후보",
    copy:
      "그린 계열을 자연 사진처럼 고정하지 않고, 반복 업무용 서비스 UI의 표면 위계로 번역합니다.",
    signal: "digital_service_ui",
    mapFocus: "green · stable surface · action accent",
    contrast: "service hierarchy",
    warning:
      "그린 후보는 자연 이미지가 아니라 UI surface hierarchy로 봅니다. accessibility contrast는 component 단위로 다시 확인해야 합니다.",
    preview: {
      kicker: "Stable Green Interface",
      headline: "Service Operations",
      metricOne: "128",
      metricTwo: "94%",
      metricThree: "22",
    },
    candidatePalettes: [
      {
        name: "Source Pattern Anchor",
        note: "original stable-green prototype roles",
        colors: [
          kw("anchor_surface", "Forest Green", "#27503D", "green.deep", ["묵직함", "안정감", "신뢰"]),
          kw("structural_support", "Bottle Green", "#006A4E", "green.deep", ["절제됨", "균형", "신뢰"]),
          kw("quiet_background", "Celadon", "#ACE1AF", "green.pastel", ["자연스러움", "절제", "고요"]),
          kw("calm_border", "Cascade", "#76C1B1", "green.pantone_trend", ["정제된 청량감", "세련미", "안정감"]),
          kw("fresh_accent", "Arcadia", "#00A591", "green.pantone_trend", ["세련", "청량", "도시적"]),
        ],
      },
      {
        name: "Low Pressure Queue",
        note: "quiet operational surface",
        colors: [
          kw("anchor_surface", "Hunter Green", "#355E3B", "green.natural", ["중후함", "신뢰", "클래식"]),
          kw("structural_support", "Forest Green", "#27503D", "green.deep", ["묵직함", "안정감"]),
          kw("quiet_background", "Celadon", "#ACE1AF", "green.pastel", ["고요", "절제"]),
          kw("calm_border", "Moss Green", "#8A9A5B", "green.natural", ["차분함", "안정적인"]),
          kw("fresh_accent", "Arcadia", "#00A591", "green.pantone_trend", ["세련", "청량"]),
        ],
      },
      {
        name: "Modern Success State",
        note: "fresher selected state while keeping depth",
        colors: [
          kw("anchor_surface", "Bottle Green", "#006A4E", "green.deep", ["절제됨", "신뢰"]),
          kw("structural_support", "Fern Green", "#4F7942", "green.natural", ["차분함", "유연함"]),
          kw("quiet_background", "Mint Green", "#98FF98", "green.pastel", ["청량함", "신선함"]),
          kw("calm_border", "Cascade", "#76C1B1", "green.pantone_trend", ["안정감", "세련미"]),
          kw("fresh_accent", "Kelly Green", "#4CBB17", "green.standard", ["활력", "긍정성"]),
        ],
      },
      {
        name: "Audit Surface",
        note: "stronger trust with muted separators",
        colors: [
          kw("anchor_surface", "Forest Green", "#27503D", "green.deep", ["묵직함", "신뢰"]),
          kw("structural_support", "Hunter Green", "#355E3B", "green.natural", ["중후함", "클래식"]),
          kw("quiet_background", "Celadon", "#ACE1AF", "green.pastel", ["절제", "고요"]),
          kw("calm_border", "Olive Green", "#708238", "green.standard", ["내추럴", "안정감"]),
          kw("fresh_accent", "Emerald Green", "#50C878", "green.standard", ["고급스러움", "생명력"]),
        ],
      },
      {
        name: "Soft Admin",
        note: "lower cognitive pressure for dense tables",
        colors: [
          kw("anchor_surface", "Fern Green", "#4F7942", "green.natural", ["차분함", "안정감"]),
          kw("structural_support", "Bottle Green", "#006A4E", "green.deep", ["절제됨", "균형"]),
          kw("quiet_background", "Celadon", "#ACE1AF", "green.pastel", ["자연스러움", "고요"]),
          kw("calm_border", "Cascade", "#76C1B1", "green.pantone_trend", ["정제된 청량감", "세련미"]),
          kw("fresh_accent", "Greenery", "#88B04B", "green.pantone_trend", ["회복", "생명력"]),
        ],
      },
      {
        name: "Deep Service Shell",
        note: "more anchored shell for pro tools",
        colors: [
          kw("anchor_surface", "Bottle Green", "#006A4E", "green.deep", ["신뢰", "균형"]),
          kw("structural_support", "Forest Green", "#27503D", "green.deep", ["묵직함", "안정감"]),
          kw("quiet_background", "Moss Green", "#8A9A5B", "green.natural", ["차분함", "안정적인"]),
          kw("calm_border", "Celadon", "#ACE1AF", "green.pastel", ["절제", "고요"]),
          kw("fresh_accent", "Arcadia", "#00A591", "green.pantone_trend", ["도시적", "청량"]),
        ],
      },
    ],
    recommendations: [
      ["Forest Green", "#27503D", "green.deep"],
      ["Bottle Green", "#006A4E", "green.deep"],
      ["Celadon", "#ACE1AF", "green.pastel"],
      ["Cascade", "#76C1B1", "green.pantone_trend"],
      ["Arcadia", "#00A591", "green.pantone_trend"],
    ],
  },
  manga: {
    title: "만화 매거진 팝 에디토리얼 팔레트 후보",
    copy:
      "만화 매거진 사이트를 특정 피사체나 IP 스타일이 아니라 masthead, cover, page field, feature frame, attention flash로 번역합니다.",
    signal: "digital_manga_magazine",
    mapFocus: "red · violet · yellow",
    contrast: "pop editorial rhythm",
    warning:
      "고채도 색은 masthead, rank, stamp 같은 구조 영역에 제한해야 합니다. 전체 패널을 채우면 읽기 표면이 무너집니다.",
    preview: {
      kicker: "Pop Editorial Issue",
      headline: "KOMA WEEKLY",
      metricOne: "09",
      metricTwo: "24p",
      metricThree: "New",
    },
    candidatePalettes: [
      {
        name: "Source Pattern Anchor",
        note: "original manga magazine prototype roles",
        colors: [
          kw("masthead_energy", "Pure Red", "#FF0000", "red.standard", ["열정", "에너지", "주목성"]),
          kw("cover_signal", "Scarlet", "#FF2400", "red.standard", ["활기", "생동감", "열정"]),
          kw("paper_field", "Buttercream", "#F3E5AB", "yellow.pastel", ["부드러움", "따뜻함", "포근함"]),
          kw("feature_frame", "Ultra Violet", "#5F4B8B", "violet.pantone_trend", ["창의적", "신비감", "미래적"]),
          kw("attention_flash", "Illuminating", "#F5DF4D", "yellow.pantone_trend", ["긍정적", "활기찬", "낙관적"]),
        ],
      },
      {
        name: "Arcade Cover",
        note: "louder tabs with soft page field",
        colors: [
          kw("masthead_energy", "Scarlet", "#FF2400", "red.standard", ["활기", "생동감"]),
          kw("cover_signal", "Tangerine", "#F28500", "orange.standard", ["에너지", "활기"]),
          kw("paper_field", "Cornsilk", "#FFF8DC", "yellow.pastel", ["부드러움", "내추럴함"]),
          kw("feature_frame", "Royal Purple", "#6C3BAA", "violet.standard", ["품격", "권위"]),
          kw("attention_flash", "Lemon Yellow", "#FFF44F", "yellow.standard", ["경쾌함", "청량감"]),
        ],
      },
      {
        name: "Night Serial",
        note: "deeper frame for mystery serials",
        colors: [
          kw("masthead_energy", "Goji Berry", "#CC142F", "red.pantone_trend", ["생기", "감각적"]),
          kw("cover_signal", "Flame", "#F2552C", "orange.pantone_trend", ["열정적", "도전적"]),
          kw("paper_field", "Buttercream", "#F3E5AB", "yellow.pastel", ["포근함", "따뜻함"]),
          kw("feature_frame", "Midnight Violet", "#2E1A47", "violet.deep", ["고요함", "신비"]),
          kw("attention_flash", "Illuminating", "#F5DF4D", "yellow.pantone_trend", ["활기찬", "낙관적"]),
        ],
      },
      {
        name: "Creator Notes",
        note: "warmer interview and notes surface",
        colors: [
          kw("masthead_energy", "Ruby", "#E11F51", "red.standard", ["화려함", "세련"]),
          kw("cover_signal", "Coral Red", "#E44327", "red.natural", ["생동감", "자연스러움"]),
          kw("paper_field", "Peach Puff", "#FFDAB9", "orange.pastel", ["따뜻함", "부드러움"]),
          kw("feature_frame", "Byzantium", "#702963", "violet.deep", ["고전적", "신비로움"]),
          kw("attention_flash", "Goldenrod", "#DAA520", "yellow.standard", ["안정감", "고급스러움"]),
        ],
      },
      {
        name: "Weekly Pop",
        note: "fast-scan issue grid",
        colors: [
          kw("masthead_energy", "Pure Red", "#FF0000", "red.standard", ["주목성", "에너지"]),
          kw("cover_signal", "Living Coral", "#FF6F61", "orange.pantone_trend", ["생동감", "낙관적"]),
          kw("paper_field", "Naples Yellow", "#FADA5E", "yellow.pastel", ["부드러움", "온화함"]),
          kw("feature_frame", "Very Peri", "#6667AB", "violet.pantone_trend", ["창조", "변화"]),
          kw("attention_flash", "Illuminating", "#F5DF4D", "yellow.pantone_trend", ["긍정적", "활기찬"]),
        ],
      },
      {
        name: "Soft Pop Editorial",
        note: "less aggressive red, more readable field",
        colors: [
          kw("masthead_energy", "Crimson", "#BD2E4A", "red.standard", ["고급스러움", "강렬함"]),
          kw("cover_signal", "Coral Blush", "#F88379", "orange.pastel", ["감성적", "세련됨"]),
          kw("paper_field", "Buttercream", "#F3E5AB", "yellow.pastel", ["포근함", "따뜻함"]),
          kw("feature_frame", "Lavender Violet", "#967BB6", "violet.natural", ["평온함", "세련"]),
          kw("attention_flash", "Lemon Yellow", "#FFF44F", "yellow.standard", ["경쾌함", "청량감"]),
        ],
      },
    ],
    recommendations: [
      ["Pure Red", "#FF0000", "red.standard"],
      ["Scarlet", "#FF2400", "red.standard"],
      ["Buttercream", "#F3E5AB", "yellow.pastel"],
      ["Ultra Violet", "#5F4B8B", "violet.pantone_trend"],
      ["Illuminating", "#F5DF4D", "yellow.pantone_trend"],
    ],
  },
};

const shell = document.querySelector(".app-shell");
const tabs = [...document.querySelectorAll(".scenario-tab")];
const briefTitle = document.querySelector("#briefTitle");
const briefCopy = document.querySelector("#briefCopy");
const briefSignal = document.querySelector("#briefSignal");
const briefMatched = document.querySelector("#briefMatched");
const contrastChip = document.querySelector("#contrastChip");
const previewKicker = document.querySelector("#previewKicker");
const previewHeadline = document.querySelector("#previewHeadline");
const metricOne = document.querySelector("#metricOne");
const metricTwo = document.querySelector("#metricTwo");
const metricThree = document.querySelector("#metricThree");
const paletteStrip = document.querySelector("#paletteStrip");
const matchList = document.querySelector("#matchList");
const warningPanel = document.querySelector("#warningPanel");
const warningCopy = document.querySelector("#warningCopy");
const recommendationList = document.querySelector("#recommendationList");
const mapFocus = document.querySelector("#mapFocus");
const candidateCount = document.querySelector("#candidateCount");
const candidateGrid = document.querySelector("#candidateGrid");

let activeScenarioKey = "blue";
let activePaletteIndex = 0;

function setThemeVars(colors) {
  const surface =
    colors.find((item) => /highlight|quiet_background|paper_field|surface/i.test(item.role)) ||
    colors[2] ||
    colors[0];

  shell.style.setProperty("--primary", colors[0].hex);
  shell.style.setProperty("--accent", colors[1]?.hex || colors[0].hex);
  shell.style.setProperty("--surface-tint", surface.hex);
}

function renderPalette(palette) {
  paletteStrip.innerHTML = palette
    .map(
      (item) => `
        <article class="palette-token">
          <span class="token-color" style="--token: ${item.hex}"></span>
          <span class="token-body">
            <span class="token-role">${item.role}</span>
            <strong class="token-name">${item.name}</strong>
            <span class="token-hex">${item.hex}</span>
          </span>
        </article>
      `,
    )
    .join("");
}

function renderMatches(palette) {
  matchList.innerHTML = palette
    .map((item) => {
      const tags = [...(item.mood || []).slice(0, 3), item.spectrum, item.family].filter(Boolean);

      return `
        <article class="match-item">
          <span class="match-swatch" style="--match: ${item.hex}" aria-hidden="true"></span>
          <div class="match-copy">
            <div class="match-title">
              <strong>${item.name}</strong>
              <span>${item.role}</span>
            </div>
            <p class="semantic-path">${item.path} · ${item.hex}</p>
            <div class="tag-row">
              ${tags.map((tag) => `<span>${tag}</span>`).join("")}
            </div>
          </div>
        </article>
      `;
    })
    .join("");
}

function renderRecommendations(items) {
  recommendationList.innerHTML = items
    .map(
      ([name, hex, path]) => `
        <span class="rec-chip" style="--rec: ${hex}">
          <strong>${name}</strong>
          <small>${path}</small>
        </span>
      `,
    )
    .join("");
}

function renderCandidatePalettes(scenario, activeIndex) {
  candidateCount.textContent = `${scenario.candidatePalettes.length} palettes · 5 roles each`;
  candidateGrid.innerHTML = scenario.candidatePalettes
    .map(
      (palette, index) => `
        <button class="candidate-card ${index === activeIndex ? "is-active" : ""}" type="button" data-palette-index="${index}">
          <span class="candidate-topline">
            <strong>${palette.name}</strong>
            <small>#${String(index + 1).padStart(2, "0")}</small>
          </span>
          <span class="candidate-note">${palette.note}</span>
          <span class="candidate-swatches" aria-hidden="true">
            ${palette.colors.map((item) => `<span style="--candidate: ${item.hex}"></span>`).join("")}
          </span>
          <span class="candidate-roles">
            ${palette.colors.map((item) => `<small>${item.role}</small>`).join("")}
          </span>
        </button>
      `,
    )
    .join("");
}

function applyPalette(index) {
  const scenario = scenarios[activeScenarioKey];
  const palette = scenario.candidatePalettes[index];

  activePaletteIndex = index;
  setThemeVars(palette.colors);
  renderPalette(palette.colors);
  renderMatches(palette.colors);
  renderCandidatePalettes(scenario, index);
  briefMatched.textContent = `${scenario.candidatePalettes.length} palettes · ${palette.colors.length} roles`;

  if (scenario.warning) {
    warningCopy.textContent = scenario.warning;
    warningPanel.hidden = false;
  } else {
    warningPanel.hidden = true;
  }
}

function selectScenario(key) {
  const scenario = scenarios[key];
  activeScenarioKey = key;
  activePaletteIndex = 0;

  tabs.forEach((tab) => {
    const active = tab.dataset.scenario === key;
    tab.classList.toggle("is-active", active);
    tab.setAttribute("aria-selected", String(active));
  });

  shell.dataset.theme = key;
  briefTitle.textContent = scenario.title;
  briefCopy.textContent = scenario.copy;
  briefSignal.textContent = scenario.signal;
  contrastChip.textContent = scenario.contrast;
  previewKicker.textContent = scenario.preview.kicker;
  previewHeadline.textContent = scenario.preview.headline;
  metricOne.textContent = scenario.preview.metricOne;
  metricTwo.textContent = scenario.preview.metricTwo;
  metricThree.textContent = scenario.preview.metricThree;
  mapFocus.textContent = scenario.mapFocus;

  renderRecommendations(scenario.recommendations);
  applyPalette(0);
}

tabs.forEach((tab) => {
  tab.addEventListener("click", () => selectScenario(tab.dataset.scenario));
});

candidateGrid.addEventListener("click", (event) => {
  const card = event.target.closest("[data-palette-index]");

  if (!card) {
    return;
  }

  applyPalette(Number(card.dataset.paletteIndex));
});

selectScenario("blue");
