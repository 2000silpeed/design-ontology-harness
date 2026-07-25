import { useMemo, useState } from "react";
import {
  ArrowLeft,
  ArrowRight,
  BookmarkSimple,
  CaretRight,
  Clock,
  NewspaperClipping,
  Seat,
  SoccerBall,
  TelevisionSimple,
  User,
} from "@phosphor-icons/react";
import auFlag from "flag-icons/flags/4x3/au.svg";
import caFlag from "flag-icons/flags/4x3/ca.svg";
import egFlag from "flag-icons/flags/4x3/eg.svg";
import esFlag from "flag-icons/flags/4x3/es.svg";
import hrFlag from "flag-icons/flags/4x3/hr.svg";
import irFlag from "flag-icons/flags/4x3/ir.svg";
import jpFlag from "flag-icons/flags/4x3/jp.svg";
import krFlag from "flag-icons/flags/4x3/kr.svg";
import maFlag from "flag-icons/flags/4x3/ma.svg";
import mxFlag from "flag-icons/flags/4x3/mx.svg";
import plFlag from "flag-icons/flags/4x3/pl.svg";
import uyFlag from "flag-icons/flags/4x3/uy.svg";

const flagAssets = {
  au: auFlag,
  ca: caFlag,
  eg: egFlag,
  es: esFlag,
  hr: hrFlag,
  ir: irFlag,
  jp: jpFlag,
  kr: krFlag,
  ma: maFlag,
  mx: mxFlag,
  pl: plFlag,
  uy: uyFlag,
};

const fixtures = [
  { id: "aus-iran", time: "12:00", group: "A조 2차전", home: "이집트", away: "호주", homeCode: "EGY", awayCode: "AUS", homeFlag: "eg", awayFlag: "au", venue: "오션 뷰 스타디움", status: "경기 전" },
  { id: "mar-iran", time: "15:00", group: "B조 2차전", home: "모로코", away: "이란", homeCode: "MAR", awayCode: "IRN", homeFlag: "ma", awayFlag: "ir", venue: "사우스 포트 스타디움", status: "경기 전" },
  { id: "jpn-pol", time: "18:00", group: "D조 2차전", home: "일본", away: "폴란드", homeCode: "JPN", awayCode: "POL", homeFlag: "jp", awayFlag: "pl", venue: "시티 오브 글로브 스타디움", status: "경기 전" },
  { id: "kor-mex", time: "21:00", group: "C조 2차전", home: "대한민국", away: "멕시코", homeCode: "KOR", awayCode: "MEX", homeFlag: "kr", awayFlag: "mx", venue: "에스타디오 델 솔", city: "과달라하라", attendance: "41,500석", status: "경기 전" },
  { id: "esp-uru", time: "23:30", group: "E조 2차전", home: "스페인", away: "우루과이", homeCode: "ESP", awayCode: "URU", homeFlag: "es", awayFlag: "uy", venue: "에스타디오 리버사이드", status: "경기 전" },
  { id: "cro-can", time: "02:00+1", group: "F조 2차전", home: "크로아티아", away: "캐나다", homeCode: "CRO", awayCode: "CAN", homeFlag: "hr", awayFlag: "ca", venue: "노스 브리지 스타디움", status: "경기 전" },
];

const stageRows = [
  ["32강", "7.25 – 7.28"],
  ["16강", "7.31 – 8.03"],
  ["8강", "8.07 – 8.08"],
  ["준결승", "8.12 – 8.13"],
  ["결승", "8.16"],
];

const news = [
  ["13:45", "전술 프리뷰", "홍명보호, 멕시코전 승부의 키는 전환 속도", "박지훈 에디터"],
  ["12:20", "팀 뉴스", "손흥민, 멕시코전 선발 출격 전망", "이성모 기자"],
  ["11:10", "데이터 인사이트", "멕시코 상대로 유효한 빌드업 패턴 3가지", "김지우 데이터 에디터"],
  ["09:30", "칼럼", "대한민국의 조별리그 생존 시나리오", "정재원 칼럼니스트"],
];

const matchupNames = {
  KOR: [["황희찬", "LW"], ["황인범", "CM"], ["김민재", "CB"]],
  MEX: [["이르빙 로사노", "RW"], ["에드손 알바레스", "CM"], ["세사르 몬테스", "CB"]],
};

function Flag({ code, label, tall = false }) {
  return <img className={`flag ${tall ? "flag--tall" : ""}`} src={flagAssets[code]} alt={`${label} 국기`} />;
}

function Header({ activeNav, onNavChange }) {
  return (
    <header className="topbar">
      <div className="brand-block">
        <div className="wordmark">MATCHROOM</div>
        <span className="brand-divider" />
        <span className="today-date">2026. 07. 14&nbsp;&nbsp;화요일</span>
      </div>
      <nav className="primary-nav" aria-label="주요 메뉴">
        {["오늘", "일정", "대진표", "팀"].map((item) => (
          <button key={item} className={activeNav === item ? "active" : ""} onClick={() => onNavChange(item)}>{item}</button>
        ))}
      </nav>
      <button className="time-panel" aria-label="시간대 선택">
        <span className="time-kicker">현지 시간</span>
        <strong>14:32</strong>
        <span className="time-zone"><Clock size={16} weight="regular" /> GMT+2</span>
      </button>
    </header>
  );
}

function StageSidebar({ activeGroup, onGroupChange, activeStage, onStageChange }) {
  return (
    <aside className="stage-sidebar">
      <button className="tournament-title">2026 국제축구대회 <CaretRight size={16} /></button>
      <div className="group-block">
        <strong>조별리그</strong>
        <span>7.11 – 7.23</span>
        <div className="group-list" aria-label="조 선택">
          {Array.from({ length: 12 }, (_, i) => `${String.fromCharCode(65 + i)}조`).map((group) => (
            <button key={group} className={group === activeGroup ? "active" : ""} onClick={() => onGroupChange(group)}>{group}</button>
          ))}
        </div>
      </div>
      <div className="stage-list">
        {stageRows.map(([stage, date]) => (
          <button key={stage} className={activeStage === stage ? "active" : ""} onClick={() => onStageChange(stage)}>
            <strong>{stage}</strong><span>{date}</span>
          </button>
        ))}
      </div>
      <button className="news-link"><NewspaperClipping size={20} /> 뉴스 &amp; 인사이트</button>
    </aside>
  );
}

function hasFinalConsonant(word) {
  const last = word.charCodeAt(word.length - 1);
  return last >= 0xac00 && last <= 0xd7a3 && (last - 0xac00) % 28 !== 0;
}

function topicParticle(word) {
  return hasFinalConsonant(word) ? "은" : "는";
}

function FormationMap({ side, team }) {
  const positions = side === "home"
    ? [[50, 10], [18, 34], [50, 34], [82, 34], [10, 66], [38, 64], [66, 64], [90, 66], [28, 88], [72, 88]]
    : [[50, 10], [15, 38], [42, 36], [70, 38], [90, 50], [28, 68], [62, 68], [12, 88], [50, 88], [88, 88]];
  return (
    <div className={`formation-map formation-map--${side}`} role="img" aria-label={`${team} 예상 포메이션 위치`}>
      <span className="goal-line" />
      {positions.map(([x, y], index) => <i key={index} style={{ left: `${x}%`, top: `${y}%` }} />)}
    </div>
  );
}

function FormDots({ values }) {
  return <div className="form-dots">{values.map((value, index) => <span key={index} className={value.toLowerCase()}>{value}</span>)}</div>;
}

function MatchDesk({ match }) {
  const isPrimary = match.id === "kor-mex";
  const homeNames = isPrimary ? matchupNames.KOR : [[`${match.home} 공격수`, "FW"], [`${match.home} 미드필더`, "CM"], [`${match.home} 수비수`, "CB"]];
  const awayNames = isPrimary ? matchupNames.MEX : [[`${match.away} 공격수`, "FW"], [`${match.away} 미드필더`, "CM"], [`${match.away} 수비수`, "CB"]];

  return (
    <main className="match-desk">
      <div className="match-meta">
        <span>조별리그 {match.group}</span>
        <span className="venue-meta"><Seat size={21} /> {match.venue}{match.city ? `, ${match.city}` : ""} <User size={19} /> {match.attendance || "38,200석"}</span>
      </div>

      <section className="score-hero" aria-label="선택 경기">
        <div className="team team--home">
          <Flag code={match.homeFlag} label={match.home} tall />
          <div><h1>{match.home}</h1><strong>{match.homeCode}</strong></div>
        </div>
        <div className="kickoff">
          <span>{match.status}</span>
          <strong>{match.time.replace("+1", "")}</strong>
          <small>{match.time.includes("+1") ? "내일" : "오늘"}</small>
        </div>
        <div className="team team--away">
          <div><h1>{match.away}</h1><strong>{match.awayCode}</strong></div>
          <Flag code={match.awayFlag} label={match.away} tall />
        </div>
      </section>

      <div className="officials">
        <span><SoccerBall size={20} /> 주심 · 다니엘 실베트 (GER)</span>
        <span><TelevisionSimple size={20} /> VAR · 바스티안 단케르트 (NED)</span>
      </div>

      <section className="analysis-grid">
        <div className="analysis-cell recent-form">
          <h2>최근 5경기 폼</h2>
          <div className="form-team"><strong>{match.homeCode}</strong><FormDots values={["W", "D", "W", "W", "L"]} /></div>
          <div className="form-team"><strong>{match.awayCode}</strong><FormDots values={["W", "W", "D", "L", "W"]} /></div>
        </div>
        <div className="analysis-cell predicted">
          <h2>예상 포메이션</h2>
          <div className="formation-label"><strong>{match.homeCode}</strong><span>4–2–3–1</span></div>
          <FormationMap side="home" team={match.home} />
          <div className="formation-label formation-label--away"><strong>{match.awayCode}</strong><span>4–3–3</span></div>
          <FormationMap side="away" team={match.away} />
        </div>
        <div className="analysis-cell key-matchups">
          <h2>키 매치업</h2>
          {homeNames.map(([name, position], index) => (
            <div className="matchup" key={name}>
              <span><strong>{name}</strong><small>{position}</small></span>
              <b>VS</b>
              <span className="away-player"><strong>{awayNames[index][0]}</strong><small>{awayNames[index][1]}</small></span>
            </div>
          ))}
        </div>
        <div className="analysis-cell standings">
          <h2>조별리그 상황</h2>
          <p>{match.group.slice(0, 2)} 순위 (1차전 기준)</p>
          {[['스웨덴', '3', '+2'], [match.away, '3', '+1'], [match.home, '0', '−1'], ['가나', '0', '−2']].map((row, index) => (
            <div key={row[0]} className={index === 2 ? "standing-row active" : "standing-row"}>
              <span>{index + 1}</span><strong>{row[0]}</strong><b>{row[1]}</b><small>{row[2]}</small>
            </div>
          ))}
        </div>
      </section>

      <section className="editorial-row">
        <div><h2>한 줄 맥락</h2><p>2연패는 탈락의 문턱. {match.home}{topicParticle(match.home)} 승점 3점이 절실한 경기입니다.</p></div>
        <div className="editor-note"><h2>에디터 노트</h2><blockquote>빠른 전환과 측면의 과감한 1대1 돌파가 {match.away} 수비를 흔들 수 있는 열쇠.</blockquote><cite>– MATCHROOM 에디터 박지훈</cite></div>
      </section>
    </main>
  );
}

function RightRail({ selectedId, onSelect, bookmarks, onToggleBookmark }) {
  const upcoming = fixtures.slice(2, 6);
  return (
    <aside className="right-rail">
      <section className="upcoming-section">
        <div className="rail-heading"><h2>다가오는 경기</h2><button>모두 보기 <CaretRight size={15} /></button></div>
        {upcoming.map((item) => (
          <button key={item.id} className={`upcoming-row ${item.id === selectedId ? "active" : ""}`} onClick={() => onSelect(item.id)}>
            <span className="upcoming-meta">{item.time}&nbsp;&nbsp;&nbsp; {item.group}</span>
            <span className="upcoming-teams"><strong>{item.home}</strong><b>VS</b><strong>{item.away}</strong><CaretRight size={17} /></span>
            <span>{item.venue}</span>
          </button>
        ))}
      </section>
      <section className="news-section">
        <div className="rail-heading"><h2>지금 주목할 경기</h2></div>
        {news.map(([time, category, title, author], index) => (
          <article className="news-item" key={title}>
            <div><span className="news-meta">{time}&nbsp;&nbsp; {category}</span><h3>{title}</h3><p>{author}</p></div>
            <button aria-label={`${title} 북마크`} aria-pressed={bookmarks.has(index)} className={bookmarks.has(index) ? "bookmarked" : ""} onClick={() => onToggleBookmark(index)}><BookmarkSimple size={21} weight={bookmarks.has(index) ? "fill" : "regular"} /></button>
          </article>
        ))}
      </section>
    </aside>
  );
}

function BottomSchedule({ selectedId, onSelect }) {
  return (
    <section className="bottom-schedule">
      <div className="schedule-heading">
        <h2>오늘의 경기 일정</h2>
        <span>전체 시간: 현지 시간 (GMT+2)</span>
      </div>
      <div className="timeline-axis" aria-hidden="true">
        {["12:00", "15:00", "18:00", "21:00", "00:00", "03:00"].map((time) => <span key={time}>{time}</span>)}
      </div>
      <div className="fixture-carousel">
        <button className="round-arrow" onClick={() => {
          const current = fixtures.findIndex((f) => f.id === selectedId);
          onSelect(fixtures[(current - 1 + fixtures.length) % fixtures.length].id);
        }} aria-label="이전 경기"><ArrowLeft size={22} /></button>
        <div className="fixture-cards">
          {fixtures.map((item) => (
            <button key={item.id} className={`fixture-card ${item.id === selectedId ? "active" : ""}`} onClick={() => onSelect(item.id)}>
              <span>{item.group}</span>
              <strong><b>{item.home}</b><small>VS</small><b>{item.away}</b></strong>
              <time>{item.time}</time>
              <em>{item.venue}</em>
              <i>{item.status}</i>
            </button>
          ))}
        </div>
        <button className="round-arrow" onClick={() => {
          const current = fixtures.findIndex((f) => f.id === selectedId);
          onSelect(fixtures[(current + 1) % fixtures.length].id);
        }} aria-label="다음 경기"><ArrowRight size={22} /></button>
      </div>
    </section>
  );
}

export function App() {
  const [activeNav, setActiveNav] = useState("오늘");
  const [activeGroup, setActiveGroup] = useState("C조");
  const [activeStage, setActiveStage] = useState("");
  const [selectedId, setSelectedId] = useState(() => new URLSearchParams(window.location.search).get("fixture") || "kor-mex");
  const [bookmarks, setBookmarks] = useState(new Set());
  const selectedMatch = useMemo(() => fixtures.find((item) => item.id === selectedId) ?? fixtures[3], [selectedId]);

  const selectFixture = (id) => {
    const fixture = fixtures.find((item) => item.id === id);
    setSelectedId(id);
    window.history.replaceState({}, "", `${window.location.pathname}?fixture=${id}`);
    if (fixture) setActiveGroup(fixture.group.slice(0, 2));
  };

  const toggleBookmark = (index) => {
    setBookmarks((current) => {
      const next = new Set(current);
      if (next.has(index)) next.delete(index); else next.add(index);
      return next;
    });
  };

  return (
    <div className="app-shell">
      <Header activeNav={activeNav} onNavChange={setActiveNav} />
      <div className="workspace">
        <StageSidebar activeGroup={activeGroup} onGroupChange={setActiveGroup} activeStage={activeStage} onStageChange={setActiveStage} />
        <MatchDesk match={selectedMatch} />
        <RightRail selectedId={selectedId} onSelect={selectFixture} bookmarks={bookmarks} onToggleBookmark={toggleBookmark} />
      </div>
      <BottomSchedule selectedId={selectedId} onSelect={selectFixture} />
      <div className="interaction-status" aria-live="polite">{activeNav} 화면 · {activeGroup} · {selectedMatch.home} 대 {selectedMatch.away}</div>
    </div>
  );
}
