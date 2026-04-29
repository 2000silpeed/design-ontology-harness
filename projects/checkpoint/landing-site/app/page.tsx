import type { CSSProperties } from "react";

const spotlightStats = [
  { label: "이번 주 리뷰", value: "12", note: "신작 + DLC + 재평가" },
  { label: "패치 재검증", value: "34", note: "출시 후 성능 변화 추적" },
  { label: "플랫폼 메모", value: "5", note: "PS5, Xbox, Switch, PC, Deck" },
  { label: "평균 읽는 시간", value: "4분", note: "구매 판단 기준만 빠르게" },
];

const reviewCards = [
  {
    title: "Ashfall Protocol",
    genre: "Action RPG",
    platforms: ["PS5", "PC"],
    score: 91,
    verdict: "즉시 추천",
    summary:
      "보스전 설계와 성장 리듬이 뛰어나지만 초반 튜토리얼이 지나치게 길다. PS5 품질 모드는 안정적이고 PC는 업스케일링 의존도가 있다.",
    tags: ["전투 밀도", "컷신 퀄리티", "성능 양호"],
  },
  {
    title: "Moon Harbor Rebuild",
    genre: "City Builder",
    platforms: ["PC", "Steam Deck"],
    score: 84,
    verdict: "주말 추천",
    summary:
      "작업 루프가 매우 깔끔하고 휴대 기기 적응이 좋다. 후반부 경제 밸런스는 아직 손을 봐야 하지만 플레이 감각은 훌륭하다.",
    tags: ["덱 최적화", "UI 명확함", "후반 밸런스 보완"],
  },
  {
    title: "Iron Chorus Zero",
    genre: "Tactical Shooter",
    platforms: ["Xbox", "PC"],
    score: 72,
    verdict: "패치 대기",
    summary:
      "핵심 슈팅 감각은 살아 있지만 프레임 페이싱과 저장 오류가 잦다. 지금은 아이디어를 사는 느낌이고 완성도를 사는 단계는 아니다.",
    tags: ["프레임 문제", "저장 오류", "핵심 손맛"],
  },
  {
    title: "Velvet Dungeon Tactics",
    genre: "Strategy RPG",
    platforms: ["Switch", "PC"],
    score: 67,
    verdict: "세일 대기",
    summary:
      "전투 구조는 흥미롭지만 템포가 늘어지고 맵 정보 전달이 부족하다. 장르 팬이면 세일 시도 가능, 대부분은 더 다듬어진 대안을 먼저 볼 만하다.",
    tags: ["템포 이슈", "맵 가독성", "장르 팬 한정"],
  },
];

const methodologyPillars = [
  {
    title: "점수보다 근거가 먼저",
    body:
      "총점은 마지막에 보고, 본문 첫 화면에서는 장점과 단점, 플랫폼별 상태, 추천 대상을 먼저 읽게 설계했습니다.",
  },
  {
    title: "패치 이후도 끝까지 추적",
    body:
      "출시 직후 점수로 끝내지 않습니다. 프레임 안정화, 밸런스 패치, 접근성 옵션 추가가 있으면 verdict를 다시 엽니다.",
  },
  {
    title: "플랫폼 경험을 분리해서 기록",
    body:
      "같은 게임이어도 PS5와 PC, Steam Deck의 감상은 다를 수 있습니다. 성능과 UX 메모를 카드처럼 바로 비교하게 만듭니다.",
  },
];

const compareRows = [
  {
    title: "Ashfall Protocol",
    price: "₩69,800",
    playtime: "28h",
    performance: "안정적 60fps",
    accessibility: "자막 / 난도 / 색약 지원",
    verdict: "지금 사도 됨",
  },
  {
    title: "Moon Harbor Rebuild",
    price: "₩44,800",
    playtime: "22h",
    performance: "Steam Deck 우수",
    accessibility: "폰트 확대 / 키 리맵",
    verdict: "장르 팬 추천",
  },
  {
    title: "Iron Chorus Zero",
    price: "₩59,800",
    playtime: "18h",
    performance: "프레임 페이싱 이슈",
    accessibility: "기본 옵션만 제공",
    verdict: "패치 대기",
  },
  {
    title: "Velvet Dungeon Tactics",
    price: "₩49,800",
    playtime: "31h",
    performance: "전반적으로 양호",
    accessibility: "텍스트 대비 보완 필요",
    verdict: "세일 대기",
  },
];

const membershipPlans = [
  {
    name: "Free",
    price: "₩0",
    caption: "핵심 verdict를 빠르게 확인하는 기본 플랜",
    featured: false,
    bullets: ["주간 리뷰 다이제스트", "구매 판단 카드 열람", "기본 차트와 필터"],
  },
  {
    name: "Plus",
    price: "₩4,900",
    caption: "광고 없이 깊게 읽는 독자를 위한 플랜",
    featured: true,
    bullets: ["광고 없는 전체 리뷰", "패치 재평가 아카이브", "월간 구매 가이드 PDF"],
  },
  {
    name: "Collector",
    price: "₩9,900",
    caption: "시즌별 큐레이션과 오디오 코멘터리까지",
    featured: false,
    bullets: ["에디터 음성 코멘터리", "장르별 추천 리스트", "연말 베스트 북 포함"],
  },
];

const faqs = [
  {
    question: "점수는 패치 이후에도 바뀌나요?",
    answer:
      "바뀝니다. 출시 후 최적화나 밸런스 변화가 구매 판단에 영향을 주면 verdict 카드와 본문 상단 로그를 함께 갱신합니다.",
  },
  {
    question: "플랫폼별 성능 메모는 어디까지 다루나요?",
    answer:
      "프레임 안정성, 로딩, 컨트롤 감각, 휴대기기 적합성처럼 실제 플레이 경험을 바꾸는 요소를 중심으로 요약합니다.",
  },
  {
    question: "스포일러는 어떻게 구분하나요?",
    answer:
      "리뷰 첫 화면은 스포일러 없이 verdict와 구매 판단에 필요한 정보만 보여주고, 서사 관련 내용은 토글 아래로 분리합니다.",
  },
  {
    question: "추천 리스트에 제휴 링크가 포함되나요?",
    answer:
      "포함될 수 있지만 모든 verdict와 점수는 제휴 여부와 분리합니다. 구매 링크가 있는 경우에도 본문 기준은 동일합니다.",
  },
];

const typeScale = {
  hero: "40px",
  section: "30px",
  cardTitle: "20px",
  stat: "34px",
};

const primaryButton: CSSProperties = {
  display: "inline-flex",
  alignItems: "center",
  justifyContent: "center",
  minHeight: "48px",
  padding: "0 22px",
  borderRadius: "999px",
  background: "var(--color-brand-accent)",
  color: "var(--color-text-inverse)",
  textDecoration: "none",
  fontFamily: "var(--font-heading)",
  fontSize: "15px",
  fontWeight: 700,
  border: "1px solid var(--color-brand-accent)",
  transition:
    "transform var(--duration-180) var(--ease-standard), background var(--duration-180) var(--ease-standard), border-color var(--duration-180) var(--ease-standard)",
};

const secondaryButton: CSSProperties = {
  display: "inline-flex",
  alignItems: "center",
  justifyContent: "center",
  minHeight: "48px",
  padding: "0 22px",
  borderRadius: "999px",
  background: "transparent",
  color: "var(--color-text)",
  textDecoration: "none",
  fontFamily: "var(--font-heading)",
  fontSize: "15px",
  fontWeight: 700,
  border: "1px solid color-mix(in srgb, var(--color-brand-accent) 30%, var(--color-border))",
  transition:
    "transform var(--duration-180) var(--ease-standard), border-color var(--duration-180) var(--ease-standard), background var(--duration-180) var(--ease-standard)",
};

const panelStyle: CSSProperties = {
  border: "1px solid var(--color-border)",
  background: "linear-gradient(180deg, rgba(16,23,34,0.92) 0%, rgba(10,14,21,0.98) 100%)",
  boxShadow: "0 18px 60px rgba(0, 0, 0, 0.32)",
  borderRadius: "24px",
};

const lightPanelStyle: CSSProperties = {
  border: "1px solid rgba(231,236,243,0.08)",
  background: "linear-gradient(180deg, rgba(244,247,251,0.08) 0%, rgba(255,255,255,0.03) 100%)",
  borderRadius: "22px",
};

export default function Home() {
  return (
    <div>
      <HeroSection />
      <MetricsBand />
      <ReviewSection />
      <CompareSection />
      <MethodologySection />
      <MembershipSection />
      <FaqSection />
      <ClosingSection />
      <style>{`
        .checkpoint-card,
        .checkpoint-plan,
        .checkpoint-surface {
          transition:
            transform var(--duration-240) var(--ease-standard),
            border-color var(--duration-180) var(--ease-standard),
            box-shadow var(--duration-240) var(--ease-standard);
        }
        .checkpoint-card:hover,
        .checkpoint-plan:hover,
        .checkpoint-surface:hover {
          transform: translateY(-4px);
          border-color: var(--color-border-strong);
          box-shadow: 0 18px 54px rgba(0, 0, 0, 0.24);
        }
        .checkpoint-primary:hover {
          transform: translateY(-2px);
          background: var(--color-link-hover);
          border-color: var(--color-link-hover);
        }
        .checkpoint-secondary:hover {
          transform: translateY(-2px);
          background: color-mix(in srgb, var(--color-brand-accent) 10%, transparent);
          border-color: color-mix(in srgb, var(--color-brand-accent) 52%, var(--color-border));
        }
      `}</style>
    </div>
  );
}

function HeroSection() {
  return (
    <section
      id="about"
      style={{
        maxWidth: "1280px",
        margin: "0 auto",
        padding: "40px 24px 32px",
      }}
    >
      <div
        style={{
          display: "grid",
          gap: "32px",
          alignItems: "stretch",
        }}
        className="lg:grid-cols-2"
      >
        <div
          style={{
            display: "grid",
            gap: "26px",
            alignContent: "center",
            minWidth: 0,
            paddingTop: "18px",
          }}
        >
          <div style={{ display: "grid", gap: "18px" }}>
            <span
              style={{
                width: "fit-content",
                padding: "8px 12px",
                borderRadius: "999px",
                border: "1px solid color-mix(in srgb, var(--color-brand-accent) 26%, var(--color-border))",
                background:
                  "color-mix(in srgb, var(--color-brand-accent) 10%, rgba(255,255,255,0.02))",
                color: "var(--color-brand-accent)",
                fontSize: "12px",
                fontWeight: 800,
                letterSpacing: "0em",
                textTransform: "uppercase",
              }}
            >
              Editorial Game Reviews
            </span>
            <div style={{ display: "grid", gap: "18px", maxWidth: "680px" }}>
              <h1
                style={{
                  margin: 0,
                  fontFamily: "var(--font-heading)",
                  fontSize: typeScale.hero,
                  lineHeight: "var(--hangul-display-line-height-safe)",
                  letterSpacing: "0em",
                  wordBreak: "keep-all",
                  overflowWrap: "normal",
                  textWrap: "balance",
                }}
              >
                살지 말지, 한 화면에서 끝내는 게임 리뷰
              </h1>
              <p
                style={{
                  margin: 0,
                  maxWidth: "600px",
                  fontSize: "16px",
                  lineHeight: 1.78,
                  color: "var(--color-text-muted)",
                  wordBreak: "keep-all",
                  overflowWrap: "normal",
                }}
              >
                Checkpoint는 점수만 던지는 사이트가 아닙니다. 총평, 플랫폼별 성능,
                패치 이후 상태, 추천 대상까지 한 리듬으로 정리해 지금 사도 되는지
                바로 판단하게 만듭니다.
              </p>
            </div>
          </div>

          <div
            style={{
              display: "flex",
              flexWrap: "wrap",
              gap: "14px",
            }}
          >
            <a href="#reviews" style={primaryButton} className="checkpoint-primary">
              이번 주 리뷰 보기
            </a>
            <a href="#membership" style={secondaryButton} className="checkpoint-secondary">
              멤버십 살펴보기
            </a>
          </div>

          <div
            style={{
              display: "grid",
              gap: "14px",
            }}
          >
            <div
              style={{
                display: "flex",
                flexWrap: "wrap",
                gap: "10px",
              }}
            >
              {["패치 후 재평가", "플랫폼별 성능 메모", "스포일러 구간 분리"].map((item) => (
                <span
                  key={item}
                  style={{
                    display: "inline-flex",
                    alignItems: "center",
                    gap: "8px",
                    padding: "9px 12px",
                    borderRadius: "999px",
                    background: "rgba(255,255,255,0.03)",
                    border: "1px solid rgba(255,255,255,0.08)",
                    color: "var(--color-text-muted)",
                    fontSize: "13px",
                    lineHeight: 1.2,
                  }}
                >
                  <span
                    aria-hidden="true"
                    style={{
                      width: "6px",
                      height: "6px",
                      borderRadius: "999px",
                      background: "var(--color-brand-accent)",
                    }}
                  />
                  {item}
                </span>
              ))}
            </div>

            <div
              style={{
                display: "grid",
                gap: "12px",
                padding: "16px 18px",
                borderRadius: "20px",
                border: "1px solid rgba(255,255,255,0.08)",
                background:
                  "linear-gradient(135deg, rgba(255,90,54,0.12) 0%, rgba(93,214,255,0.05) 48%, rgba(166,255,77,0.08) 100%)",
              }}
            >
              <span
                style={{
                  fontFamily: "var(--font-mono)",
                  fontSize: "12px",
                  color: "var(--color-text-subtle)",
                  textTransform: "uppercase",
                  letterSpacing: "0em",
                }}
              >
                Friday Snapshot
              </span>
              <p
                style={{
                  margin: 0,
                  fontFamily: "var(--font-heading)",
                  fontSize: "22px",
                  lineHeight: 1.34,
                  letterSpacing: "0em",
                  wordBreak: "keep-all",
                  overflowWrap: "normal",
                }}
              >
                이번 주는 액션 RPG가 강했고, 전술 슈터는 아직 패치를 더 기다려야
                합니다.
              </p>
            </div>
          </div>
        </div>

        <HeroBoard />
      </div>
    </section>
  );
}

function HeroBoard() {
  return (
    <div
      style={{
        ...panelStyle,
        padding: "22px",
        display: "grid",
        gap: "18px",
        minHeight: "100%",
        position: "relative",
        overflow: "hidden",
      }}
      className="checkpoint-surface"
    >
      <div
        aria-hidden="true"
        style={{
          position: "absolute",
          inset: 0,
          background:
            "radial-gradient(circle at 15% 0%, rgba(255,90,54,0.26), transparent 26%), radial-gradient(circle at 88% 12%, rgba(166,255,77,0.18), transparent 24%)",
          pointerEvents: "none",
        }}
      />
      <div
        style={{
          position: "relative",
          display: "flex",
          flexWrap: "wrap",
          gap: "10px",
          alignItems: "center",
        }}
      >
        {["All", "PS5", "PC", "Steam Deck", "Patch Watch"].map((filter, index) => (
          <span
            key={filter}
            style={{
              padding: "8px 12px",
              borderRadius: "999px",
              background:
                index === 0
                  ? "var(--color-brand-accent)"
                  : "color-mix(in srgb, var(--color-surface-elevated) 80%, transparent)",
              color: index === 0 ? "var(--color-text-inverse)" : "var(--color-text-muted)",
              fontFamily: "var(--font-heading)",
              fontSize: "13px",
              fontWeight: 700,
              border:
                index === 0
                  ? "1px solid var(--color-brand-accent)"
                  : "1px solid rgba(255,255,255,0.08)",
            }}
          >
            {filter}
          </span>
        ))}
      </div>

      <div
        style={{
          position: "relative",
          display: "grid",
          gap: "18px",
        }}
        className="xl:grid-cols-[minmax(0,1.15fr)_minmax(260px,0.85fr)]"
      >
        <div
          style={{
            ...lightPanelStyle,
            padding: "18px",
            display: "grid",
            gap: "16px",
            minWidth: 0,
          }}
        >
          <div
            style={{
              minHeight: "220px",
              borderRadius: "18px",
              padding: "18px",
              display: "grid",
              alignContent: "space-between",
              background:
                "linear-gradient(135deg, rgba(255,90,54,0.85) 0%, rgba(96,41,32,0.78) 44%, rgba(8,11,16,0.92) 100%)",
            }}
          >
            <div
              style={{
                display: "flex",
                justifyContent: "space-between",
                alignItems: "start",
                gap: "16px",
              }}
            >
              <div style={{ display: "grid", gap: "8px" }}>
                <span
                  style={{
                    fontFamily: "var(--font-mono)",
                    fontSize: "12px",
                    color: "rgba(244,247,251,0.78)",
                    textTransform: "uppercase",
                    letterSpacing: "0em",
                  }}
                >
                  Cover Story
                </span>
                <strong
                  style={{
                    fontFamily: "var(--font-heading)",
                    fontSize: "28px",
                    lineHeight: 1.12,
                    letterSpacing: "0em",
                  }}
                >
                  Ashfall
                  <br />
                  Protocol
                </strong>
              </div>
              <div
                style={{
                  width: "78px",
                  height: "78px",
                  borderRadius: "50%",
                  background: "rgba(8,11,16,0.74)",
                  border: "1px solid rgba(255,255,255,0.12)",
                  display: "grid",
                  placeItems: "center",
                  textAlign: "center",
                }}
              >
                <span
                  style={{
                    fontFamily: "var(--font-heading)",
                    fontSize: "30px",
                    fontWeight: 800,
                    lineHeight: 1.1,
                  }}
                >
                  91
                </span>
              </div>
            </div>

            <div style={{ display: "grid", gap: "10px" }}>
              <div style={{ display: "flex", flexWrap: "wrap", gap: "8px" }}>
                {["PS5", "PC", "즉시 추천"].map((item) => (
                  <span
                    key={item}
                    style={{
                      padding: "7px 10px",
                      borderRadius: "999px",
                      background: "rgba(8,11,16,0.42)",
                      border: "1px solid rgba(255,255,255,0.12)",
                      fontSize: "12px",
                      color: "rgba(244,247,251,0.82)",
                    }}
                  >
                    {item}
                  </span>
                ))}
              </div>
              <p
                style={{
                  margin: 0,
                  maxWidth: "32ch",
                  color: "rgba(244,247,251,0.9)",
                  fontSize: "14px",
                  lineHeight: 1.7,
                }}
              >
                전투는 공격적이고, 컷신은 과장 없이 세련됐습니다. 구매 판단에 필요한
                건 거의 다 갖췄고, 지금은 설명보다 플레이가 먼저 설득합니다.
              </p>
            </div>
          </div>

          <div
            style={{
              display: "grid",
              gap: "12px",
            }}
            className="md:grid-cols-3"
          >
            {[
              ["Patch Watch", "Iron Chorus Zero", "프레임 페이싱 업데이트 대기"],
              ["Deck Check", "Moon Harbor Rebuild", "핸드헬드에서 UI 손실 거의 없음"],
              ["Buy Window", "Velvet Dungeon", "세일가 30% 아래에서 가치 상승"],
            ].map(([label, title, body]) => (
              <div
                key={label}
                style={{
                  padding: "14px",
                  borderRadius: "16px",
                  background: "rgba(255,255,255,0.03)",
                  border: "1px solid rgba(255,255,255,0.07)",
                  display: "grid",
                  gap: "8px",
                }}
              >
                <span
                  style={{
                    fontFamily: "var(--font-mono)",
                    fontSize: "11px",
                    letterSpacing: "0em",
                    textTransform: "uppercase",
                    color: "var(--color-text-subtle)",
                  }}
                >
                  {label}
                </span>
                <strong
                  style={{
                    fontFamily: "var(--font-heading)",
                    fontSize: "16px",
                    lineHeight: 1.15,
                  }}
                >
                  {title}
                </strong>
                <p
                  style={{
                    margin: 0,
                    color: "var(--color-text-muted)",
                    fontSize: "13px",
                    lineHeight: 1.6,
                  }}
                >
                  {body}
                </p>
              </div>
            ))}
          </div>
        </div>

        <div style={{ display: "grid", gap: "16px" }}>
          {[
            {
              label: "Confidence Radar",
              value: "Strong Buy",
              note: "이번 주 에디터 합의가 가장 높은 verdict",
            },
            {
              label: "Patch Queue",
              value: "3 titles",
              note: "다음 재평가 후보에 올라간 신작 수",
            },
            {
              label: "Platform Split",
              value: "Deck rising",
              note: "휴대형 최적화가 구매 판단을 더 자주 바꾸는 중",
            },
          ].map((item, index) => (
            <div
              key={item.label}
              style={{
                ...lightPanelStyle,
                padding: "18px",
                display: "grid",
                gap: "10px",
                alignContent: "start",
                minHeight: index === 0 ? "180px" : "auto",
              }}
            >
              <span
                style={{
                  fontFamily: "var(--font-mono)",
                  fontSize: "11px",
                  letterSpacing: "0em",
                  textTransform: "uppercase",
                  color: "var(--color-text-subtle)",
                }}
              >
                {item.label}
              </span>
              <strong
                style={{
                  fontFamily: "var(--font-heading)",
                  fontSize: "24px",
                  lineHeight: 1.16,
                  letterSpacing: "0em",
                }}
              >
                {item.value}
              </strong>
              <p
                style={{
                  margin: 0,
                  fontSize: "14px",
                  lineHeight: 1.7,
                  color: "var(--color-text-muted)",
                }}
              >
                {item.note}
              </p>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}

function MetricsBand() {
  return (
    <section
      id="charts"
      style={{
        maxWidth: "1280px",
        margin: "0 auto",
        padding: "12px 24px 0",
      }}
    >
      <div
        style={{
          display: "grid",
          gap: "14px",
        }}
        className="md:grid-cols-2 xl:grid-cols-4"
      >
        {spotlightStats.map((item, index) => (
          <div
            key={item.label}
            id={index === 0 ? "verdicts" : undefined}
            style={{
              ...lightPanelStyle,
              padding: "22px 20px",
              display: "grid",
              gap: "10px",
            }}
            className="checkpoint-card"
          >
            <span
              style={{
                fontFamily: "var(--font-mono)",
                fontSize: "12px",
                letterSpacing: "0em",
                textTransform: "uppercase",
                color: "var(--color-text-subtle)",
              }}
            >
              {item.label}
            </span>
            <strong
              style={{
                fontFamily: "var(--font-heading)",
                fontSize: typeScale.stat,
                lineHeight: 1.05,
                letterSpacing: "0em",
              }}
            >
              {item.value}
            </strong>
            <p
              style={{
                margin: 0,
                fontSize: "14px",
                color: "var(--color-text-muted)",
                lineHeight: 1.65,
              }}
            >
              {item.note}
            </p>
          </div>
        ))}
      </div>
    </section>
  );
}

function ReviewSection() {
  return (
    <section
      id="reviews"
      style={{
        maxWidth: "1280px",
        margin: "0 auto",
        padding: "92px 24px 0",
      }}
    >
      <SectionHeading
        eyebrow="Latest Reviews"
        title="점수 카드보다 먼저, 구매 판단에 필요한 맥락"
        body="이번 주 리뷰는 카드 한 장만 훑어도 장르, 플랫폼, 구매 타이밍, 주요 리스크가 보이도록 구성했습니다."
      />

      <div
        style={{
          display: "grid",
          gap: "18px",
          marginTop: "28px",
        }}
        className="md:grid-cols-2 xl:grid-cols-4"
      >
        {reviewCards.map((review) => (
          <article
            key={review.title}
            style={{
              ...panelStyle,
              padding: "18px",
              display: "grid",
              gap: "16px",
            }}
            className="checkpoint-card"
          >
            <div
              style={{
                minHeight: "168px",
                borderRadius: "18px",
                padding: "16px",
                display: "grid",
                alignContent: "space-between",
                background: reviewGradient(review.score),
              }}
            >
              <div
                style={{
                  display: "flex",
                  justifyContent: "space-between",
                  gap: "12px",
                }}
              >
                <span
                  style={{
                    padding: "7px 10px",
                    borderRadius: "999px",
                    background: "rgba(8,11,16,0.42)",
                    border: "1px solid rgba(255,255,255,0.12)",
                    color: "rgba(244,247,251,0.82)",
                    fontSize: "12px",
                  }}
                >
                  {review.genre}
                </span>
                <ScoreBadge score={review.score} />
              </div>
              <div style={{ display: "grid", gap: "8px" }}>
                <strong
                  style={{
                    fontFamily: "var(--font-heading)",
                    fontSize: "24px",
                    lineHeight: 1.14,
                    letterSpacing: "0em",
                    color: "#f4f7fb",
                  }}
                >
                  {review.title}
                </strong>
                <span
                  style={{
                    fontFamily: "var(--font-mono)",
                    fontSize: "11px",
                    letterSpacing: "0em",
                    textTransform: "uppercase",
                    color: "rgba(244,247,251,0.74)",
                  }}
                >
                  {review.verdict}
                </span>
              </div>
            </div>

            <div style={{ display: "grid", gap: "12px" }}>
              <div style={{ display: "flex", flexWrap: "wrap", gap: "8px" }}>
                {review.platforms.map((platform) => (
                  <span
                    key={platform}
                    style={{
                      padding: "6px 10px",
                      borderRadius: "999px",
                      background: "rgba(166,255,77,0.08)",
                      border: "1px solid rgba(166,255,77,0.15)",
                      color: "var(--color-brand-accent)",
                      fontSize: "12px",
                      fontWeight: 700,
                    }}
                  >
                    {platform}
                  </span>
                ))}
              </div>
              <p
                style={{
                  margin: 0,
                  color: "var(--color-text-muted)",
                  fontSize: "14px",
                  lineHeight: 1.72,
                }}
              >
                {review.summary}
              </p>
              <div style={{ display: "flex", flexWrap: "wrap", gap: "8px" }}>
                {review.tags.map((tag) => (
                  <span
                    key={tag}
                    style={{
                      padding: "5px 9px",
                      borderRadius: "999px",
                      background: "rgba(255,255,255,0.04)",
                      color: "var(--color-text-subtle)",
                      fontSize: "12px",
                    }}
                  >
                    {tag}
                  </span>
                ))}
              </div>
            </div>
          </article>
        ))}
      </div>
    </section>
  );
}

function CompareSection() {
  return (
    <section
      id="compare"
      style={{
        maxWidth: "1280px",
        margin: "0 auto",
        padding: "96px 24px 0",
      }}
    >
      <div
        style={{
          display: "grid",
          gap: "22px",
          alignItems: "start",
        }}
        className="xl:grid-cols-[minmax(0,0.8fr)_minmax(0,1.2fr)]"
      >
        <div style={{ display: "grid", gap: "18px" }}>
          <SectionHeading
            eyebrow="Compare Board"
            title="지금 사도 되는지, 아니면 세일과 패치를 기다릴지"
            body="게임 리뷰에서 정말 중요한 건 취향 설명만이 아닙니다. 가격, 플레이타임, 성능, 접근성, 패치 가능성까지 나란히 볼 수 있어야 합니다."
          />

          <div
            style={{
              ...panelStyle,
              padding: "20px",
              display: "grid",
              gap: "14px",
            }}
            className="checkpoint-surface"
          >
            {[
              ["Strong Buy", "완성도와 플레이 감각이 이미 구매 비용을 정당화할 때"],
              ["Wait for Patch", "좋은 뼈대가 있지만 기술적 이슈가 아직 구매를 막을 때"],
              ["Sale Only", "장르 팬에겐 의미가 있지만 전체 추천까진 아닐 때"],
            ].map(([title, body], index) => (
              <div
                key={title}
                style={{
                  display: "grid",
                  gap: "6px",
                  paddingTop: index === 0 ? 0 : "14px",
                  borderTop: index === 0 ? "none" : "1px solid rgba(255,255,255,0.08)",
                }}
              >
                <strong
                  style={{
                    fontFamily: "var(--font-heading)",
                    fontSize: "18px",
                    lineHeight: 1.1,
                  }}
                >
                  {title}
                </strong>
                <p
                  style={{
                    margin: 0,
                    color: "var(--color-text-muted)",
                    fontSize: "14px",
                    lineHeight: 1.65,
                  }}
                >
                  {body}
                </p>
              </div>
            ))}
          </div>
        </div>

        <div
          style={{
            ...panelStyle,
            padding: "18px",
            overflow: "hidden",
          }}
          className="checkpoint-surface"
        >
          <div
            style={{
              display: "grid",
              gap: "10px",
            }}
          >
            <div
              style={{
                display: "grid",
                gap: "10px",
                padding: "0 4px 10px",
                borderBottom: "1px solid rgba(255,255,255,0.08)",
                color: "var(--color-text-subtle)",
                fontFamily: "var(--font-mono)",
                fontSize: "11px",
                letterSpacing: "0em",
                textTransform: "uppercase",
              }}
              className="md:grid-cols-[1.45fr_0.8fr_0.75fr_1fr_1.1fr_0.9fr]"
            >
              <span>Title</span>
              <span>Price</span>
              <span>Time</span>
              <span>Performance</span>
              <span>Accessibility</span>
              <span>Verdict</span>
            </div>

            {compareRows.map((row) => (
              <div
                key={row.title}
                style={{
                  display: "grid",
                  gap: "10px",
                  padding: "14px 4px",
                  borderBottom: "1px solid rgba(255,255,255,0.07)",
                  alignItems: "center",
                }}
                className="md:grid-cols-[1.45fr_0.8fr_0.75fr_1fr_1.1fr_0.9fr]"
              >
                <div style={{ display: "grid", gap: "4px" }}>
                  <strong
                    style={{
                      fontFamily: "var(--font-heading)",
                      fontSize: "18px",
                      lineHeight: 1.1,
                    }}
                  >
                    {row.title}
                  </strong>
                  <span
                    style={{
                      color: "var(--color-text-subtle)",
                      fontSize: "12px",
                    }}
                  >
                    구매 판단 카드 갱신됨
                  </span>
                </div>
                <span style={tableCellStyle}>{row.price}</span>
                <span style={tableCellStyle}>{row.playtime}</span>
                <span style={tableCellStyle}>{row.performance}</span>
                <span style={tableCellStyle}>{row.accessibility}</span>
                <span
                  style={{
                    ...tableCellStyle,
                    width: "fit-content",
                    padding: "7px 10px",
                    borderRadius: "999px",
                    background: verdictBackground(row.verdict),
                    color: verdictColor(row.verdict),
                    border: `1px solid ${verdictBorder(row.verdict)}`,
                  }}
                >
                  {row.verdict}
                </span>
              </div>
            ))}
          </div>
        </div>
      </div>
    </section>
  );
}

function MethodologySection() {
  return (
    <section
      id="methodology"
      style={{
        maxWidth: "1280px",
        margin: "0 auto",
        padding: "96px 24px 0",
      }}
    >
      <SectionHeading
        eyebrow="Methodology"
        title="게임을 예쁘게 소개하는 대신, 끝까지 책임지는 비평"
        body="Checkpoint의 구조는 잡지형 무드와 데이터형 판단을 섞습니다. 큰 카피로 기대감을 만들고, 바로 아래에서는 리스크와 근거를 카드와 표로 끊어 읽게 합니다."
      />

      <div
        style={{
          display: "grid",
          gap: "18px",
          marginTop: "28px",
        }}
        className="lg:grid-cols-3"
      >
        {methodologyPillars.map((pillar) => (
          <div
            key={pillar.title}
            style={{
              ...panelStyle,
              padding: "22px",
              display: "grid",
              gap: "12px",
            }}
            className="checkpoint-card"
          >
            <strong
              style={{
                fontFamily: "var(--font-heading)",
                fontSize: typeScale.cardTitle,
                lineHeight: 1.2,
                letterSpacing: "0em",
              }}
            >
              {pillar.title}
            </strong>
            <p
              style={{
                margin: 0,
                color: "var(--color-text-muted)",
                fontSize: "15px",
                lineHeight: 1.78,
              }}
            >
              {pillar.body}
            </p>
          </div>
        ))}
      </div>

      <div
        style={{
          ...panelStyle,
          padding: "22px",
          marginTop: "18px",
          display: "grid",
          gap: "18px",
        }}
        className="checkpoint-surface"
      >
        <div
          style={{
            display: "flex",
            flexWrap: "wrap",
            justifyContent: "space-between",
            gap: "16px",
            alignItems: "end",
          }}
        >
          <div style={{ display: "grid", gap: "8px", maxWidth: "680px" }}>
            <span
              style={{
                fontFamily: "var(--font-mono)",
                fontSize: "12px",
                letterSpacing: "0em",
                textTransform: "uppercase",
                color: "var(--color-text-subtle)",
              }}
            >
              Scoring Rubric
            </span>
            <strong
              style={{
                fontFamily: "var(--font-heading)",
                fontSize: "28px",
                lineHeight: 1.2,
                letterSpacing: "0em",
                wordBreak: "keep-all",
                overflowWrap: "normal",
              }}
            >
              총점은 네 가지 질문의 합계입니다.
            </strong>
          </div>
          <span
            style={{
              padding: "8px 12px",
              borderRadius: "999px",
              border: "1px solid rgba(166,255,77,0.18)",
              color: "var(--color-brand-accent)",
              background: "rgba(166,255,77,0.07)",
              fontSize: "13px",
              fontWeight: 700,
            }}
          >
            score != hype
          </span>
        </div>

        <div
          style={{
            display: "grid",
            gap: "14px",
          }}
          className="md:grid-cols-2 xl:grid-cols-4"
        >
          {[
            ["전투 / 조작", "게임의 핵심 리듬이 반복 플레이를 버티는가"],
            ["서사 / 페이싱", "컷신과 플레이 구간이 서로의 템포를 해치지 않는가"],
            ["최적화 / 접근성", "플랫폼별 성능과 옵션이 실제 경험을 지탱하는가"],
            ["시간 대비 가치", "지불한 비용만큼 기억에 남는 선택이 있는가"],
          ].map(([title, body]) => (
            <div
              key={title}
              style={{
                padding: "16px",
                borderRadius: "18px",
                border: "1px solid rgba(255,255,255,0.07)",
                background: "rgba(255,255,255,0.03)",
                display: "grid",
                gap: "8px",
              }}
            >
              <strong
                style={{
                  fontFamily: "var(--font-heading)",
                  fontSize: "18px",
                  lineHeight: 1.1,
                }}
              >
                {title}
              </strong>
              <p
                style={{
                  margin: 0,
                  color: "var(--color-text-muted)",
                  fontSize: "14px",
                  lineHeight: 1.65,
                }}
              >
                {body}
              </p>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
}

function MembershipSection() {
  return (
    <section
      id="membership"
      style={{
        maxWidth: "1280px",
        margin: "0 auto",
        padding: "96px 24px 0",
      }}
    >
      <SectionHeading
        eyebrow="Membership"
        title="광고보다 오래 남는 비평을 위해"
        body="무료로도 충분히 둘러볼 수 있지만, 더 깊은 리뷰와 패치 재평가 아카이브, 큐레이션 북은 멤버십에서 제공합니다."
      />

      <div
        style={{
          display: "grid",
          gap: "18px",
          marginTop: "28px",
        }}
        className="md:grid-cols-3"
      >
        {membershipPlans.map((plan) => (
          <div
            key={plan.name}
            style={{
              ...panelStyle,
              padding: "22px",
              display: "grid",
              gap: "18px",
              borderColor: plan.featured
                ? "color-mix(in srgb, var(--color-brand-accent) 30%, var(--color-border))"
                : "var(--color-border)",
              background: plan.featured
                ? "linear-gradient(180deg, rgba(166,255,77,0.08) 0%, rgba(16,23,34,0.98) 100%)"
                : panelStyle.background,
            }}
            className="checkpoint-plan"
          >
            <div style={{ display: "grid", gap: "8px" }}>
              <div
                style={{
                  display: "flex",
                  justifyContent: "space-between",
                  gap: "16px",
                  alignItems: "center",
                }}
              >
                <strong
                  style={{
                    fontFamily: "var(--font-heading)",
                    fontSize: "var(--text-xl)",
                    lineHeight: 1.16,
                  }}
                >
                  {plan.name}
                </strong>
                {plan.featured ? (
                  <span
                    style={{
                      padding: "7px 10px",
                      borderRadius: "999px",
                      background: "var(--color-brand-accent)",
                      color: "var(--color-text-inverse)",
                      fontSize: "12px",
                      fontWeight: 800,
                    }}
                  >
                    Editor Pick
                  </span>
                ) : null}
              </div>
              <div style={{ display: "flex", alignItems: "end", gap: "8px" }}>
                <span
                  style={{
                    fontFamily: "var(--font-heading)",
                    fontSize: "44px",
                    lineHeight: 1.05,
                    letterSpacing: "0em",
                  }}
                >
                  {plan.price}
                </span>
                <span
                  style={{
                    paddingBottom: "8px",
                    color: "var(--color-text-subtle)",
                    fontSize: "14px",
                  }}
                >
                  / month
                </span>
              </div>
              <p
                style={{
                  margin: 0,
                  color: "var(--color-text-muted)",
                  fontSize: "14px",
                  lineHeight: 1.68,
                }}
              >
                {plan.caption}
              </p>
            </div>

            <div style={{ display: "grid", gap: "10px" }}>
              {plan.bullets.map((bullet) => (
                <div
                  key={bullet}
                  style={{
                    display: "flex",
                    gap: "10px",
                    alignItems: "start",
                    color: "var(--color-text-muted)",
                    fontSize: "14px",
                    lineHeight: 1.6,
                  }}
                >
                  <span
                    aria-hidden="true"
                    style={{
                      marginTop: "7px",
                      width: "6px",
                      height: "6px",
                      borderRadius: "999px",
                      background: plan.featured
                        ? "var(--color-brand-accent)"
                        : "var(--color-text-subtle)",
                    }}
                  />
                  {bullet}
                </div>
              ))}
            </div>

            <a
              href="#newsletter"
              style={plan.featured ? primaryButton : secondaryButton}
              className={plan.featured ? "checkpoint-primary" : "checkpoint-secondary"}
            >
              {plan.featured ? "Plus 시작" : "알림 받기"}
            </a>
          </div>
        ))}
      </div>
    </section>
  );
}

function FaqSection() {
  return (
    <section
      id="faq"
      style={{
        maxWidth: "1280px",
        margin: "0 auto",
        padding: "96px 24px 0",
      }}
    >
      <SectionHeading
        eyebrow="FAQ"
        title="게임 리뷰 사이트가 실제로 해줘야 하는 질문들"
        body="Checkpoint는 감상문과 소비 판단 사이에 있는 회색지대를 메우는 쪽에 더 가깝습니다."
      />

      <div
        style={{
          display: "grid",
          gap: "18px",
          marginTop: "28px",
        }}
        className="md:grid-cols-2"
      >
        {faqs.map((faq) => (
          <div
            key={faq.question}
            style={{
              ...panelStyle,
              padding: "22px",
              display: "grid",
              gap: "12px",
            }}
            className="checkpoint-card"
          >
            <strong
              style={{
                fontFamily: "var(--font-heading)",
                fontSize: "22px",
                lineHeight: 1.24,
                letterSpacing: "0em",
              }}
            >
              {faq.question}
            </strong>
            <p
              style={{
                margin: 0,
                color: "var(--color-text-muted)",
                fontSize: "15px",
                lineHeight: 1.78,
              }}
            >
              {faq.answer}
            </p>
          </div>
        ))}
      </div>
    </section>
  );
}

function ClosingSection() {
  return (
    <section
      id="newsletter"
      style={{
        maxWidth: "1280px",
        margin: "0 auto",
        padding: "96px 24px 96px",
      }}
    >
      <div
        style={{
          ...panelStyle,
          padding: "28px",
          overflow: "hidden",
          position: "relative",
        }}
      >
        <div
          aria-hidden="true"
          style={{
            position: "absolute",
            inset: 0,
            background:
              "radial-gradient(circle at 18% 0%, rgba(255,90,54,0.24), transparent 28%), radial-gradient(circle at 88% 28%, rgba(166,255,77,0.18), transparent 24%)",
            pointerEvents: "none",
          }}
        />
        <div
          style={{
            position: "relative",
            display: "grid",
            gap: "26px",
            alignItems: "center",
          }}
          className="xl:grid-cols-[minmax(0,0.95fr)_minmax(360px,0.75fr)]"
        >
          <div style={{ display: "grid", gap: "16px", maxWidth: "720px" }}>
            <span
              style={{
                width: "fit-content",
                padding: "8px 12px",
                borderRadius: "999px",
                background: "rgba(166,255,77,0.08)",
                border: "1px solid rgba(166,255,77,0.18)",
                color: "var(--color-brand-accent)",
                fontSize: "12px",
                fontWeight: 800,
                letterSpacing: "0em",
                textTransform: "uppercase",
              }}
            >
              Weekly Digest
            </span>
            <h2
              style={{
                margin: 0,
                fontFamily: "var(--font-heading)",
                fontSize: "38px",
                lineHeight: "var(--hangul-display-line-height-safe)",
                letterSpacing: "0em",
                wordBreak: "keep-all",
                overflowWrap: "normal",
                textWrap: "balance",
              }}
            >
              금요일 아침, 이번 주에 살 게임만 남겨서 보냅니다.
            </h2>
            <p
              style={{
                margin: 0,
                color: "var(--color-text-muted)",
                fontSize: "15px",
                lineHeight: 1.78,
                maxWidth: "52ch",
              }}
            >
              화려한 카피보다 구매 판단, 긴 본문보다 verdict 요약, 업데이트 후 변경된
              점수까지. Checkpoint 뉴스레터는 게임을 더 많이 사게 만드는 대신 덜
              후회하게 만드는 쪽을 목표로 합니다.
            </p>
          </div>

          <div
            style={{
              ...lightPanelStyle,
              padding: "20px",
              display: "grid",
              gap: "14px",
            }}
          >
            <div
              style={{
                display: "grid",
                gap: "6px",
              }}
            >
              <strong
                style={{
                  fontFamily: "var(--font-heading)",
                  fontSize: "var(--text-xl)",
                  lineHeight: 1.05,
                }}
              >
                이번 주 다이제스트에 포함되는 것
              </strong>
              <p
                style={{
                  margin: 0,
                  color: "var(--color-text-muted)",
                  fontSize: "14px",
                  lineHeight: 1.68,
                }}
              >
                6개 verdict 카드, 패치로 바뀐 평가, 주말 추천작, 세일 대기 체크리스트
              </p>
            </div>

            <div
              style={{
                display: "grid",
                gap: "10px",
                padding: "14px",
                borderRadius: "16px",
                background: "rgba(255,255,255,0.03)",
                border: "1px solid rgba(255,255,255,0.07)",
              }}
            >
              <span
                style={{
                  color: "var(--color-text-subtle)",
                  fontSize: "13px",
                }}
              >
                your@email.com
              </span>
              <a href="#membership" style={primaryButton} className="checkpoint-primary">
                무료로 받아보기
              </a>
            </div>

            <span
              style={{
                color: "var(--color-text-subtle)",
                fontSize: "12px",
                lineHeight: 1.6,
              }}
            >
              광고보다 비평을 우선합니다. 언제든 구독 해지할 수 있습니다.
            </span>
          </div>
        </div>
      </div>
    </section>
  );
}

function SectionHeading({
  eyebrow,
  title,
  body,
}: {
  eyebrow: string;
  title: string;
  body: string;
}) {
  return (
    <div style={{ display: "grid", gap: "14px", maxWidth: "720px" }}>
      <span
        style={{
          fontFamily: "var(--font-mono)",
          fontSize: "12px",
          letterSpacing: "0em",
          textTransform: "uppercase",
          color: "var(--color-text-subtle)",
        }}
      >
        {eyebrow}
      </span>
      <h2
        style={{
          margin: 0,
          fontFamily: "var(--font-heading)",
          fontSize: typeScale.section,
          lineHeight: "var(--hangul-display-line-height-safe)",
          letterSpacing: "0em",
          wordBreak: "keep-all",
          overflowWrap: "normal",
          textWrap: "balance",
        }}
      >
        {title}
      </h2>
      <p
        style={{
          margin: 0,
          color: "var(--color-text-muted)",
          fontSize: "15px",
          lineHeight: 1.78,
          wordBreak: "keep-all",
          overflowWrap: "normal",
        }}
      >
        {body}
      </p>
    </div>
  );
}

function ScoreBadge({ score }: { score: number }) {
  return (
    <span
      style={{
        minWidth: "52px",
        height: "52px",
        padding: "0 12px",
        display: "inline-flex",
        alignItems: "center",
        justifyContent: "center",
        borderRadius: "999px",
        background: verdictBackground(score >= 85 ? "지금 사도 됨" : score >= 75 ? "장르 팬 추천" : score >= 70 ? "패치 대기" : "세일 대기"),
        border: `1px solid ${verdictBorder(score >= 85 ? "지금 사도 됨" : score >= 75 ? "장르 팬 추천" : score >= 70 ? "패치 대기" : "세일 대기")}`,
        color: verdictColor(score >= 85 ? "지금 사도 됨" : score >= 75 ? "장르 팬 추천" : score >= 70 ? "패치 대기" : "세일 대기"),
        fontFamily: "var(--font-heading)",
        fontSize: "20px",
        fontWeight: 800,
        letterSpacing: "0em",
      }}
    >
      {score}
    </span>
  );
}

function reviewGradient(score: number) {
  if (score >= 85) {
    return "linear-gradient(135deg, rgba(255,90,54,0.92) 0%, rgba(67,28,22,0.88) 48%, rgba(8,11,16,0.96) 100%)";
  }

  if (score >= 75) {
    return "linear-gradient(135deg, rgba(93,214,255,0.72) 0%, rgba(20,67,84,0.84) 44%, rgba(8,11,16,0.96) 100%)";
  }

  return "linear-gradient(135deg, rgba(127,138,154,0.7) 0%, rgba(37,45,58,0.88) 48%, rgba(8,11,16,0.96) 100%)";
}

function verdictBackground(verdict: string) {
  if (verdict.includes("지금")) {
    return "rgba(166,255,77,0.14)";
  }

  if (verdict.includes("장르")) {
    return "rgba(93,214,255,0.14)";
  }

  if (verdict.includes("패치")) {
    return "rgba(255,159,28,0.14)";
  }

  return "rgba(255,90,54,0.14)";
}

function verdictBorder(verdict: string) {
  if (verdict.includes("지금")) {
    return "rgba(166,255,77,0.28)";
  }

  if (verdict.includes("장르")) {
    return "rgba(93,214,255,0.28)";
  }

  if (verdict.includes("패치")) {
    return "rgba(255,159,28,0.28)";
  }

  return "rgba(255,90,54,0.28)";
}

function verdictColor(verdict: string) {
  if (verdict.includes("지금")) {
    return "var(--color-brand-accent)";
  }

  if (verdict.includes("장르")) {
    return "var(--color-info)";
  }

  if (verdict.includes("패치")) {
    return "var(--color-warning)";
  }

  return "var(--color-surface-tint)";
}

const tableCellStyle: CSSProperties = {
  color: "var(--color-text-muted)",
  fontSize: "14px",
  lineHeight: 1.6,
};
