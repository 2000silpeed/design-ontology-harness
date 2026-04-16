import type { CSSProperties } from "react";
import styles from "./page.module.css";

const reviewCards = [
  {
    title: "Ashfall Protocol",
    genre: "Action RPG",
    platforms: ["PS5", "PC"],
    score: 91,
    verdict: "지금 사도 됨",
    summary:
      "보스전의 템포와 컷신 연출이 같이 설득하는 드문 케이스다. 품질 모드는 안정적이고, PC는 업스케일링 설정만 잘 잡으면 훌륭하다.",
    breakdown: [
      { label: "전투", value: 94 },
      { label: "서사", value: 86 },
      { label: "최적화", value: 89 },
    ],
    notes: ["컷신 밀도 우수", "패드 감각 좋음", "튜토리얼은 길다"],
  },
  {
    title: "Moon Harbor Rebuild",
    genre: "City Builder",
    platforms: ["PC", "Steam Deck"],
    score: 84,
    verdict: "주말 추천",
    summary:
      "관리 루프가 단정하고 휴대기기 적응력이 뛰어나다. 후반 경제 곡선은 조금 흔들리지만, 한동안 손에서 놓기 어려운 설계다.",
    breakdown: [
      { label: "시스템", value: 88 },
      { label: "UI", value: 84 },
      { label: "휴대성", value: 91 },
    ],
    notes: ["덱 최적화 우수", "폰트 가독성 안정", "후반 밸런스 보완"],
  },
  {
    title: "Iron Chorus Zero",
    genre: "Tactical Shooter",
    platforms: ["Xbox", "PC"],
    score: 72,
    verdict: "패치 대기",
    summary:
      "총을 쏘는 감각은 살아 있지만 프레임 페이싱과 저장 오류가 계속 발목을 잡는다. 아이디어는 좋고, 지금은 완성도를 기다릴 차례다.",
    breakdown: [
      { label: "손맛", value: 85 },
      { label: "안정성", value: 58 },
      { label: "완성도", value: 67 },
    ],
    notes: ["프레임 드랍 빈번", "저장 오류 보고", "코어 전투는 훌륭"],
  },
  {
    title: "Velvet Dungeon Tactics",
    genre: "Strategy RPG",
    platforms: ["Switch", "PC"],
    score: 67,
    verdict: "세일 대기",
    summary:
      "전투 규칙은 흥미롭지만 맵 정보를 읽는 데 시간이 너무 많이 든다. 장르 팬은 세일 시도 가능, 대부분은 더 다듬어진 대안을 먼저 보는 편이 낫다.",
    breakdown: [
      { label: "전술성", value: 82 },
      { label: "맵 정보", value: 54 },
      { label: "템포", value: 60 },
    ],
    notes: ["맵 정보 부족", "전술 구조는 좋음", "세일 구간이 적정"],
  },
];

const curatedQueues = [
  {
    title: "지금 할 게임",
    tone: "positive",
    items: [
      "Ashfall Protocol — 전투와 연출이 같이 서는 대형 신작",
      "Moon Harbor Rebuild — 휴대기기까지 챙긴 정돈된 운영 시뮬",
      "Rift Motel Stories — 4시간 컷의 강한 서사형 인디",
    ],
  },
  {
    title: "기다릴 게임",
    tone: "warning",
    items: [
      "Iron Chorus Zero — 프레임 페이싱 안정화 이후 재판단",
      "Velvet Dungeon Tactics — 30% 세일 이하에서 가치 상승",
      "Neon Relay Tour — 컨트롤 리맵 업데이트 확인 필요",
    ],
  },
  {
    title: "패치 후 재평가",
    tone: "neutral",
    items: [
      "Frostline Orders — 접근성 옵션 추가로 verdict 상향 검토",
      "Red Harbor Derby — 저장 안정성 패치 후 점수 재산정",
      "Signal Runner 2 — Steam Deck 전용 프로파일 검증 중",
    ],
  },
];

const updateLog = [
  {
    label: "오늘 14:20",
    title: "Iron Chorus Zero 패치 1.03 확인",
    body: "저장 오류는 줄었지만 보스전 프레임 드랍은 여전히 남아 있어 verdict는 유지했습니다.",
  },
  {
    label: "어제 22:05",
    title: "Moon Harbor Rebuild Deck 프로파일 추가",
    body: "휴대 환경에서 UI 밀도가 잘 유지되는지 다시 측정하고 카드 메모를 보강했습니다.",
  },
  {
    label: "4월 15일",
    title: "상반기 액션 RPG 구매 가이드 갱신",
    body: "플레이타임, 성능 모드, 접근성 옵션을 한 표로 다시 정리해 비교 보드를 업데이트했습니다.",
  },
];

const compareRows = [
  {
    title: "Ashfall Protocol",
    price: "₩69,800",
    playtime: "28h",
    performance: "안정적 60fps",
    support: "자막 / 난도 / 색약 지원",
    verdict: "지금 사도 됨",
  },
  {
    title: "Moon Harbor Rebuild",
    price: "₩44,800",
    playtime: "22h",
    performance: "Steam Deck 우수",
    support: "폰트 확대 / 키 리맵",
    verdict: "장르 팬 추천",
  },
  {
    title: "Iron Chorus Zero",
    price: "₩59,800",
    playtime: "18h",
    performance: "프레임 페이싱 이슈",
    support: "기본 옵션만 제공",
    verdict: "패치 대기",
  },
  {
    title: "Velvet Dungeon Tactics",
    price: "₩49,800",
    playtime: "31h",
    performance: "전반적 양호",
    support: "텍스트 대비 보완 필요",
    verdict: "세일 대기",
  },
];

const rankingList = [
  { rank: "01", title: "Ashfall Protocol", score: 91, status: "Must Play", delta: "+3" },
  { rank: "02", title: "Rift Motel Stories", score: 89, status: "Strong Buy", delta: "NEW" },
  { rank: "03", title: "Moon Harbor Rebuild", score: 84, status: "Weekend Pick", delta: "+1" },
  { rank: "04", title: "Frostline Orders", score: 83, status: "Re-Evaluated", delta: "+4" },
  { rank: "05", title: "Velvet Dungeon Tactics", score: 67, status: "Sale Watch", delta: "-2" },
];

const releaseRadar = [
  { date: "04.18", title: "Glass Canyon GT", note: "레이싱 / PS5 / 검토 대기" },
  { date: "04.23", title: "Mora Signal", note: "공포 / PC / 체험판 인상 강함" },
  { date: "04.26", title: "Frontline Atlas", note: "전략 / Xbox / 접근성 옵션 확인" },
  { date: "05.02", title: "Night Terminal", note: "액션 / 멀티플랫폼 / 성능 비교 예정" },
];

const searchSignals = [
  "플랫폼별 성능",
  "패치 후 재평가",
  "올해 최고 평점",
  "Steam Deck 추천",
  "30시간 이하 캠페인",
];

const methodologyPillars = [
  {
    title: "점수보다 근거를 먼저 둡니다",
    body:
      "카드 첫 화면에서 장점과 단점, 플랫폼 메모, 추천 대상을 먼저 읽고 마지막에 총점을 보게 설계했습니다.",
  },
  {
    title: "패치 이후도 같은 비중으로 다룹니다",
    body:
      "출시 주의 평가는 임시 verdict일 수 있습니다. 최적화와 접근성 변화가 있으면 같은 화면에서 다시 업데이트합니다.",
  },
  {
    title: "플랫폼 경험을 분리해 기록합니다",
    body:
      "PS5와 PC, Steam Deck은 같은 게임이 아닐 때가 많습니다. 성능과 UX 메모를 구매 결정용 언어로 분리합니다.",
  },
];

const heroMetrics = [
  { label: "주간 리뷰", value: "12", detail: "신작 + DLC + 재평가" },
  { label: "패치 추적", value: "34", detail: "출시 후 성능 변화 기록" },
  { label: "플랫폼 메모", value: "5", detail: "PS5, Xbox, Switch, PC, Deck" },
  { label: "평균 독서", value: "4분", detail: "구매 판단 기준만 빠르게" },
];

function scoreAccent(score: number) {
  if (score >= 88) {
    return {
      surface: "rgba(166, 255, 77, 0.16)",
      border: "rgba(166, 255, 77, 0.34)",
      text: "var(--color-brand-accent)",
    };
  }
  if (score >= 80) {
    return {
      surface: "rgba(93, 214, 255, 0.14)",
      border: "rgba(93, 214, 255, 0.34)",
      text: "var(--color-info)",
    };
  }
  if (score >= 70) {
    return {
      surface: "rgba(255, 159, 28, 0.14)",
      border: "rgba(255, 159, 28, 0.32)",
      text: "var(--color-warning)",
    };
  }
  return {
    surface: "rgba(255, 56, 100, 0.14)",
    border: "rgba(255, 56, 100, 0.3)",
    text: "var(--color-danger)",
  };
}

function verdictTone(verdict: string) {
  if (verdict.includes("지금")) {
    return styles.verdictBuy;
  }
  if (verdict.includes("추천")) {
    return styles.verdictInfo;
  }
  if (verdict.includes("패치")) {
    return styles.verdictWarn;
  }
  return styles.verdictDanger;
}

function SectionIntro({
  eyebrow,
  title,
  description,
}: {
  eyebrow: string;
  title: string;
  description: string;
}) {
  return (
    <div className={styles.sectionIntro}>
      <span className={styles.sectionEyebrow}>{eyebrow}</span>
      <div className={styles.sectionCopy}>
        <h2 className={styles.sectionTitle}>{title}</h2>
        <p className={styles.sectionDescription}>{description}</p>
      </div>
    </div>
  );
}

function ReviewCard({
  title,
  genre,
  platforms,
  score,
  verdict,
  summary,
  breakdown,
  notes,
}: (typeof reviewCards)[number]) {
  const tone = scoreAccent(score);
  const scoreStyle = {
    "--score-surface": tone.surface,
    "--score-border": tone.border,
    "--score-text": tone.text,
  } as CSSProperties;

  return (
    <article className={styles.reviewCard}>
      <div className={styles.reviewHeader}>
        <div className={styles.reviewMetaBlock}>
          <span className={styles.reviewMetaLabel}>{genre}</span>
          <h3 className={styles.reviewTitle}>{title}</h3>
        </div>
        <div className={styles.scoreBadge} style={scoreStyle}>
          <span className={styles.scoreValue}>{score}</span>
          <span className={styles.scoreCaption}>Score</span>
        </div>
      </div>

      <div className={styles.platformRow}>
        {platforms.map((platform) => (
          <span key={platform} className={styles.platformTag}>
            {platform}
          </span>
        ))}
        <span className={`${styles.verdictPill} ${verdictTone(verdict)}`}>{verdict}</span>
      </div>

      <p className={styles.reviewSummary}>{summary}</p>

      <div className={styles.breakdownList}>
        {breakdown.map((item) => (
          <div key={item.label} className={styles.breakdownItem}>
            <div className={styles.breakdownLabelRow}>
              <span>{item.label}</span>
              <span>{item.value}</span>
            </div>
            <div className={styles.breakdownTrack}>
              <span className={styles.breakdownFill} style={{ width: `${item.value}%` }} />
            </div>
          </div>
        ))}
      </div>

      <div className={styles.noteList}>
        {notes.map((note) => (
          <span key={note} className={styles.noteTag}>
            {note}
          </span>
        ))}
      </div>
    </article>
  );
}

export default function Home() {
  return (
    <div className={styles.page}>
      <section className={styles.hero} id="top">
        <div className={styles.heroLead}>
          <div className={styles.heroCopy}>
            <span className={styles.issueTag}>Issue 16 / 구매 판단 특집</span>
            <h1 className={styles.heroTitle}>
              살지 말지,
              <br />
              첫 화면에서 끝내는
              <br />
              게임 리뷰 홈
            </h1>
            <p className={styles.heroDescription}>
              Checkpoint는 총점만 던지지 않습니다. 대표 리뷰, 플랫폼별 성능 메모,
              패치 로그, 비교표, 랭킹까지 한 장에 압축해 지금 사도 되는지 바로
              판단하게 만듭니다.
            </p>
          </div>

          <div className={styles.heroActions}>
            <a href="#reviews" className={styles.primaryAction}>
              이번 주 리뷰 보기
            </a>
            <a href="#compare" className={styles.secondaryAction}>
              구매 판단 표로 이동
            </a>
          </div>

          <div className={styles.heroSignals}>
            {[
              "패치 후 재평가",
              "플랫폼별 성능 메모",
              "카드 + 표 혼합 레이아웃",
              "스포일러 없는 verdict",
            ].map((item) => (
              <span key={item} className={styles.signalPill}>
                {item}
              </span>
            ))}
          </div>

          <div className={styles.metricsGrid}>
            {heroMetrics.map((metric) => (
              <article key={metric.label} className={styles.metricCard}>
                <span className={styles.metricLabel}>{metric.label}</span>
                <strong className={styles.metricValue}>{metric.value}</strong>
                <p className={styles.metricDetail}>{metric.detail}</p>
              </article>
            ))}
          </div>
        </div>

        <div className={styles.heroBoard}>
          <div className={styles.toolbarRow}>
            {["All", "PS5", "PC", "Steam Deck", "Patch Watch"].map((item, index) => (
              <span
                key={item}
                className={index === 0 ? styles.toolbarChipActive : styles.toolbarChip}
              >
                {item}
              </span>
            ))}
          </div>

          <div className={styles.heroBoardGrid}>
            <article className={styles.coverStory}>
              <div className={styles.coverArt}>
                <div className={styles.coverGlow} />
                <div className={styles.coverText}>
                  <span className={styles.coverEyebrow}>Cover Story</span>
                  <h2 className={styles.coverTitle}>Ashfall Protocol</h2>
                  <p className={styles.coverDeck}>
                    공격적 전투와 침착한 연출이 같이 서는 액션 RPG. 품질 모드는
                    안정적이고, 설명보다 플레이가 먼저 설득합니다.
                  </p>
                </div>
                <div className={styles.coverScore}>
                  <span className={styles.coverScoreValue}>91</span>
                  <span className={styles.coverScoreLabel}>Must Play</span>
                </div>
              </div>

              <div className={styles.coverMetaRow}>
                <div>
                  <span className={styles.metaLabel}>Platform</span>
                  <strong>PS5 / PC</strong>
                </div>
                <div>
                  <span className={styles.metaLabel}>Buy Window</span>
                  <strong>지금 사도 됨</strong>
                </div>
                <div>
                  <span className={styles.metaLabel}>Patch Log</span>
                  <strong>1.02 안정화 확인</strong>
                </div>
              </div>
            </article>

            <div className={styles.sideStack}>
              <article className={styles.signalPanel}>
                <div className={styles.panelHeader}>
                  <span className={styles.panelEyebrow}>Quick Verdict</span>
                  <span className={`${styles.verdictPill} ${styles.verdictBuy}`}>Strong Buy</span>
                </div>
                <ul className={styles.bulletList}>
                  <li>전투 리듬과 컷신 퀄리티가 같이 설득함</li>
                  <li>PC는 업스케일링 조정 전제, 콘솔은 매우 안정적</li>
                  <li>튜토리얼 구간만 넘기면 강한 몰입 유지</li>
                </ul>
              </article>

              <article className={styles.logPanel}>
                <div className={styles.panelHeader}>
                  <span className={styles.panelEyebrow}>오늘의 업데이트</span>
                  <a href="#methodology" className={styles.inlineLink}>
                    기준 보기
                  </a>
                </div>
                <div className={styles.logList}>
                  {updateLog.slice(0, 2).map((item) => (
                    <div key={item.title} className={styles.logItem}>
                      <span className={styles.logLabel}>{item.label}</span>
                      <strong>{item.title}</strong>
                      <p>{item.body}</p>
                    </div>
                  ))}
                </div>
              </article>
            </div>
          </div>
        </div>
      </section>

      <section className={styles.section} id="reviews">
        <SectionIntro
          eyebrow="Latest Reviews"
          title="최신 리뷰 카드와 에디터 큐레이션을 한 흐름으로"
          description="카드에서 verdict와 플랫폼 상태를 먼저 읽고, 오른쪽 큐레이션 레일에서 지금 할 게임과 기다릴 게임을 바로 나눠봅니다."
        />

        <div className={styles.contentGrid}>
          <div className={styles.reviewGrid}>
            {reviewCards.map((card) => (
              <ReviewCard key={card.title} {...card} />
            ))}
          </div>

          <aside className={styles.sideRail}>
            <div className={styles.railStack}>
              {curatedQueues.map((queue) => (
                <article key={queue.title} className={styles.railPanel}>
                  <div className={styles.panelHeader}>
                    <span className={styles.panelEyebrow}>{queue.title}</span>
                    <span
                      className={`${styles.queueTone} ${
                        queue.tone === "positive"
                          ? styles.queuePositive
                          : queue.tone === "warning"
                            ? styles.queueWarning
                            : styles.queueNeutral
                      }`}
                    />
                  </div>
                  <ul className={styles.queueList}>
                    {queue.items.map((item) => (
                      <li key={item}>{item}</li>
                    ))}
                  </ul>
                </article>
              ))}

              <article className={styles.railPanel}>
                <div className={styles.panelHeader}>
                  <span className={styles.panelEyebrow}>Recent Updates</span>
                  <span className={styles.panelCounter}>03</span>
                </div>
                <div className={styles.timeline}>
                  {updateLog.map((item) => (
                    <div key={item.title} className={styles.timelineItem}>
                      <span className={styles.timelineLabel}>{item.label}</span>
                      <strong>{item.title}</strong>
                      <p>{item.body}</p>
                    </div>
                  ))}
                </div>
              </article>
            </div>
          </aside>
        </div>
      </section>

      <section className={styles.section} id="compare">
        <SectionIntro
          eyebrow="Compare Board"
          title="가격, 플레이타임, 접근성, 성능을 한 표에서"
          description="구매 판단 도구는 단순한 가격 비교가 아니라, 플랫폼 경험과 접근성 옵션까지 한 번에 읽히도록 설계했습니다."
        />

        <div className={styles.compareGrid}>
          <article className={styles.tableCard}>
            <div className={styles.panelHeader}>
              <span className={styles.panelEyebrow}>구매 판단 표</span>
              <span className={styles.panelCounter}>4 Games</span>
            </div>
            <div className={styles.tableWrap}>
              <table className={styles.compareTable}>
                <thead>
                  <tr>
                    <th>게임</th>
                    <th>가격</th>
                    <th>플레이타임</th>
                    <th>성능</th>
                    <th>접근성</th>
                    <th>판단</th>
                  </tr>
                </thead>
                <tbody>
                  {compareRows.map((row) => (
                    <tr key={row.title}>
                      <td>{row.title}</td>
                      <td>{row.price}</td>
                      <td>{row.playtime}</td>
                      <td>{row.performance}</td>
                      <td>{row.support}</td>
                      <td>
                        <span className={`${styles.verdictPill} ${verdictTone(row.verdict)}`}>
                          {row.verdict}
                        </span>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </article>

          <div className={styles.compareSide}>
            <article className={styles.rankCard} id="rankings">
              <div className={styles.panelHeader}>
                <span className={styles.panelEyebrow}>이번 달 랭킹</span>
                <a href="#newsletter" className={styles.inlineLink}>
                  전체 목록 받기
                </a>
              </div>
              <ol className={styles.rankingList}>
                {rankingList.map((item) => (
                  <li key={item.rank} className={styles.rankingItem}>
                    <div className={styles.rankingLead}>
                      <span className={styles.rankNumber}>{item.rank}</span>
                      <div>
                        <strong>{item.title}</strong>
                        <p>{item.status}</p>
                      </div>
                    </div>
                    <div className={styles.rankingMeta}>
                      <strong>{item.score}</strong>
                      <span>{item.delta}</span>
                    </div>
                  </li>
                ))}
              </ol>
            </article>

            <article className={styles.releaseCard}>
              <div className={styles.panelHeader}>
                <span className={styles.panelEyebrow}>Release Radar</span>
                <span className={styles.panelCounter}>Next 14 Days</span>
              </div>
              <div className={styles.releaseList}>
                {releaseRadar.map((item) => (
                  <div key={item.title} className={styles.releaseItem}>
                    <span className={styles.releaseDate}>{item.date}</span>
                    <div>
                      <strong>{item.title}</strong>
                      <p>{item.note}</p>
                    </div>
                  </div>
                ))}
              </div>
            </article>
          </div>
        </div>
      </section>

      <section className={styles.section} id="discover">
        <SectionIntro
          eyebrow="Search + Discovery"
          title="검색과 발견도 구매 판단 언어로 정리합니다"
          description="장르, 플랫폼, 플레이타임, 최근 패치 여부를 섞어 빠르게 좁혀 들어가도록 설계한 샘플 탐색 영역입니다."
        />

        <div className={styles.discoveryGrid}>
          <article className={styles.searchCard}>
            <div className={styles.searchBar}>
              <span className={styles.searchIcon} />
              <span className={styles.searchPlaceholder}>게임명, 스튜디오, 장르, 플랫폼으로 검색</span>
              <kbd className={styles.searchShortcut}>/</kbd>
            </div>

            <div className={styles.filterToolbar}>
              {["PS5", "PC", "Steam Deck", "80점 이상", "30시간 이하", "최근 패치"].map((item) => (
                <span key={item} className={styles.filterChip}>
                  {item}
                </span>
              ))}
            </div>

            <div className={styles.discoveryBody}>
              <div className={styles.discoveryPanel}>
                <span className={styles.panelEyebrow}>최근 검색</span>
                <div className={styles.signalCloud}>
                  {searchSignals.map((item) => (
                    <span key={item} className={styles.signalPill}>
                      {item}
                    </span>
                  ))}
                </div>
              </div>

              <div className={styles.discoveryPanel}>
                <span className={styles.panelEyebrow}>추천 조합</span>
                <div className={styles.discoveryCards}>
                  <article className={styles.discoverySnippet}>
                    <strong>퇴근 후 2시간 컷</strong>
                    <p>짧은 캠페인 + 강한 verdict + 덱 적응성 중심</p>
                  </article>
                  <article className={styles.discoverySnippet}>
                    <strong>세일 전 대기열</strong>
                    <p>세일 가치가 큰 작품만 따로 묶어 가격 창을 추적</p>
                  </article>
                  <article className={styles.discoverySnippet}>
                    <strong>패치 재평가 모음</strong>
                    <p>출시 초기 verdict에서 얼마나 회복됐는지 로그로 비교</p>
                  </article>
                </div>
              </div>
            </div>
          </article>

          <article className={styles.methodCard} id="methodology">
            <div className={styles.panelHeader}>
              <span className={styles.panelEyebrow}>Editorial Method</span>
              <span className={styles.panelCounter}>3 Rules</span>
            </div>
            <div className={styles.methodGrid}>
              {methodologyPillars.map((item) => (
                <article key={item.title} className={styles.methodItem}>
                  <strong>{item.title}</strong>
                  <p>{item.body}</p>
                </article>
              ))}
            </div>
          </article>
        </div>
      </section>

      <section className={styles.section} id="newsletter">
        <div className={styles.newsletterCard}>
          <div className={styles.newsletterCopy}>
            <span className={styles.sectionEyebrow}>Weekly Digest</span>
            <h2 className={styles.newsletterTitle}>
              금요일마다
              <br />
              “지금 살 게임 / 기다릴 게임”만 정리해 보냅니다
            </h2>
            <p className={styles.newsletterText}>
              새 리뷰, 패치 로그, 가격 구간 메모를 한 장으로 받아보고 싶다면
              다이제스트에 등록하세요. 광고보다 판단을 먼저 보내는 게 Checkpoint의
              원칙입니다.
            </p>
          </div>

          <div className={styles.newsletterActions}>
            <div className={styles.formRow}>
              <label className={styles.inputField}>
                <span className={styles.inputLabel}>이메일</span>
                <input type="email" placeholder="you@example.com" className={styles.input} />
              </label>
              <button type="button" className={styles.primaryAction}>
                다이제스트 받기
              </button>
            </div>
            <p className={styles.formMeta}>
              스포일러 없는 verdict 요약과 패치 재평가 로그만 보내며, 언제든
              구독을 해지할 수 있습니다.
            </p>
          </div>
        </div>
      </section>
    </div>
  );
}
