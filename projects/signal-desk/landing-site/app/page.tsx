const featureColumns = [
  {
    title: "Writing stays central",
    body: "에디터, 코멘트, 발행 일정이 서로를 가리지 않도록 한 화면 안에서 조용하게 이어집니다.",
    points: ["문서 중심 2-column workspace", "리뷰 패널은 보조 계층으로 후퇴", "강조는 단 하나의 CTA만"],
  },
  {
    title: "Editorial rhythm over dashboard noise",
    body: "숫자는 보여주되 화면의 리듬은 본문과 여백으로 잡습니다. 카드보다 문장, 장식보다 정렬이 먼저입니다.",
    points: ["낮은 elevation의 tinted cards", "thin divider 중심 hierarchy", "serif heading + humanist body"],
  },
  {
    title: "Built for small teams with taste",
    body: "작은 편집팀이 매일 쓰는 도구답게, 기능은 단단하고 인상은 고집 있게 남도록 설계했습니다.",
    points: ["명확한 상태와 predictable motion", "조용한 보조 액션", "다크 모드 포함한 동일한 질감"],
  },
];

const featureCards = [
  {
    eyebrow: "Workspace",
    title: "문서와 일정, 코멘트가 한 호흡으로 이어지는 에디토리얼 데스크",
    body: "탑바의 검색과 알림, 좌측 내비게이션, 우측 리뷰 패널이 서로 부딪히지 않도록 split-pane 리듬으로 구성했습니다.",
  },
  {
    eyebrow: "Review",
    title: "문장 단위 피드백이 거슬리지 않게 머무는 인라인 코멘트 흐름",
    body: "과한 컬러 블록 대신 따뜻한 tint와 얇은 divider로 코멘트의 존재감만 드러냅니다.",
  },
  {
    eyebrow: "Publishing",
    title: "오늘 써야 할 것과 이번 주에 나가야 할 것이 함께 보이는 발행 운영 레이어",
    body: "캘린더와 보드, 최근 활동을 동일한 typographic hierarchy 아래에 정리했습니다.",
  },
  {
    eyebrow: "Control",
    title: "키보드 중심 탐색과 command palette가 제품의 템포를 지켜줍니다",
    body: "빠른 이동은 강하게, 나머지 인터랙션은 조용하게. low-noise motion만 남겨 작업 리듬을 해치지 않습니다.",
  },
];

const testimonials = [
  {
    quote:
      "Signal Desk는 문서를 쓰는 감각을 해치지 않으면서도 팀의 속도를 올려줬어요. 업무 앱인데 편집 도구처럼 느껴집니다.",
    author: "서연정",
    role: "Managing Editor, Letterpress Weekly",
  },
  {
    quote:
      "코멘트와 발행 일정, 태그 관리가 한 화면에서 정리되니 ‘지금 무엇을 마감해야 하는가’가 아주 명확해졌습니다.",
    author: "Jamie Park",
    role: "Workflow Lead, Minuet Studio",
  },
  {
    quote:
      "과장된 생산성 UI가 아니라, 팀이 문장을 다듬는 리듬을 존중하는 운영 툴이라는 점이 좋았습니다.",
    author: "이서윤",
    role: "Content Director, Framehouse",
  },
];

const pricing = [
  {
    name: "Solo",
    price: "₩0",
    caption: "독립 창작자를 위한 시작점",
    featured: false,
    bullets: ["개인 workspace 1개", "기본 에디터와 캘린더", "최근 히스토리 30일"],
  },
  {
    name: "Studio",
    price: "₩19",
    caption: "작은 편집팀을 위한 기본 운영 플랜",
    featured: true,
    bullets: ["리뷰 워크플로우", "무제한 코멘트와 멘션", "팀 권한과 발행 운영"],
  },
  {
    name: "Agency",
    price: "₩49",
    caption: "브랜드 팀과 에이전시용 확장 플랜",
    featured: false,
    bullets: ["다중 workspace", "고급 권한 관리", "브랜드별 운영 템플릿"],
  },
];

const faqs = [
  {
    question: "문서 작성과 발행 일정이 정말 한 제품 안에서 같이 동작하나요?",
    answer:
      "네. 에디터, 리뷰, 일정, 보드가 분리된 도구처럼 보이지 않도록 같은 정보 계층 아래에 묶여 있습니다.",
  },
  {
    question: "팀이 작아도 권한과 리뷰 흐름을 세밀하게 나눌 수 있나요?",
    answer:
      "작성, 검토, 승인, 발행 역할을 나눌 수 있고, 댓글 스레드와 멘션은 문장 단위까지 연결됩니다.",
  },
  {
    question: "다크 모드에서도 에디토리얼 톤이 유지되나요?",
    answer:
      "밝은 모드의 종이 같은 질감과 낮은 elevation 계층을 다크 모드에서도 같은 원칙으로 변환하도록 설계했습니다.",
  },
  {
    question: "기존 노션/구글독스 기반 운영에서 옮겨오기 어렵지 않나요?",
    answer:
      "초기에는 기존 발행 구조를 유지한 채 일정, 리뷰, 명령형 탐색부터 천천히 옮길 수 있게 마이그레이션 흐름을 제공합니다.",
  },
];

const landingType = {
  display: "clamp(2.45rem, 5.1vw, 4.7rem)",
  section: "clamp(1.85rem, 3vw, 2.95rem)",
  cardTitle: "clamp(1.45rem, 2vw, 1.95rem)",
  quote: "clamp(1.35rem, 2.1vw, 1.9rem)",
  pricingTitle: "clamp(1.75rem, 2.4vw, 2.4rem)",
  pricingPrice: "clamp(2.65rem, 3.9vw, 3.5rem)",
  faq: "clamp(1.4rem, 2vw, 1.85rem)",
};

export default function Home() {
  return (
    <div
      style={{
        background:
          "radial-gradient(circle at top left, color-mix(in srgb, var(--color-brand-accent) 28%, transparent) 0, transparent 34%), linear-gradient(180deg, var(--color-canvas) 0%, #f4ede4 48%, #efe5d8 100%)",
      }}
    >
      <HeroSection />
      <MetricsBand />
      <EditorialStatement />
      <FeatureGallery />
      <TestimonialSection />
      <PricingSection />
      <FaqSection />
      <ClosingSection />
    </div>
  );
}

function HeroSection() {
  return (
    <section
      style={{
        maxWidth: "1380px",
        margin: "0 auto",
        padding: "56px 24px 32px",
      }}
    >
      <div
        style={{
          display: "grid",
          gap: "32px",
          alignItems: "start",
        }}
        className="lg:grid-cols-[minmax(0,0.88fr)_minmax(620px,1.12fr)]"
      >
        <div style={{ display: "grid", gap: "24px", minWidth: 0 }}>
          <div style={{ display: "grid", gap: "16px" }}>
            <span
              style={{
                width: "fit-content",
                padding: "8px 12px",
                borderRadius: "999px",
                border: "1px solid color-mix(in srgb, var(--color-brand-primary) 18%, var(--color-border))",
                background: "color-mix(in srgb, var(--color-surface) 80%, var(--color-brand-accent) 20%)",
                color: "var(--color-link)",
                fontSize: "12px",
                letterSpacing: "0.16em",
                textTransform: "uppercase",
                fontWeight: 700,
              }}
            >
              Editorial work OS
            </span>
            <div style={{ display: "grid", gap: "18px", maxWidth: "640px" }}>
              <h1
                style={{
                  margin: 0,
                  fontFamily: "var(--font-heading)",
                  fontSize: landingType.display,
                  lineHeight: 1.02,
                  letterSpacing: "-0.05em",
                  wordBreak: "keep-all",
                  overflowWrap: "normal",
                  textWrap: "balance",
                  color: "var(--color-text)",
                }}
              >
                생각의 호흡을 지키는 업무 공간
              </h1>
              <p
                style={{
                  margin: 0,
                  maxWidth: "560px",
                  fontSize: "clamp(1rem, 1.45vw, 1.12rem)",
                  lineHeight: 1.72,
                  wordBreak: "keep-all",
                  overflowWrap: "normal",
                  color: "var(--color-text-muted)",
                }}
              >
                글쓰기, 팀 협업, 발행 일정을 한 곳에서. 독립 창작자와 작은 편집팀을
                위한 고집 있는 에디토리얼 업무 앱입니다. 숫자를 더 많이 보여주기보다,
                지금 써야 할 것과 검토해야 할 것을 더 정확히 보이게 만듭니다.
              </p>
            </div>
          </div>

          <div
            style={{
              display: "flex",
              flexWrap: "wrap",
              gap: "14px",
              alignItems: "center",
            }}
          >
            <a
              href="#pricing"
              style={heroPrimaryButton}
            >
              무료로 시작
            </a>
            <a
              href="#journal"
              style={heroSecondaryButton}
            >
              사용 사례 보기
            </a>
          </div>

          <div
            style={{
              display: "grid",
              gap: "18px",
              paddingTop: "8px",
            }}
          >
            <div
              style={{
                display: "flex",
                flexWrap: "wrap",
                gap: "14px 20px",
                color: "var(--color-text-subtle)",
                fontSize: "12px",
                letterSpacing: "0.12em",
                textTransform: "uppercase",
              }}
            >
              <span>2,400명의 에디터가 사용</span>
              <span>월 1,200만 단어 작성</span>
              <span>AAA 접근성</span>
            </div>

            <div
              style={{
                display: "grid",
                gap: "14px",
                maxWidth: "580px",
                padding: "18px 20px",
                borderRadius: "20px",
                border: "1px solid var(--color-border)",
                background:
                  "linear-gradient(180deg, color-mix(in srgb, var(--color-surface) 86%, var(--color-brand-accent) 14%) 0%, color-mix(in srgb, var(--color-surface) 96%, transparent) 100%)",
                boxShadow: "0 16px 44px rgba(58, 36, 18, 0.06)",
              }}
            >
              <div
                style={{
                  display: "flex",
                  alignItems: "baseline",
                  justifyContent: "space-between",
                  gap: "16px",
                }}
              >
                <span
                  style={{
                    fontSize: "12px",
                    letterSpacing: "0.16em",
                    textTransform: "uppercase",
                    color: "var(--color-text-subtle)",
                  }}
                >
                  This week&apos;s editorial desk
                </span>
                <span
                  style={{
                    fontSize: "13px",
                    color: "var(--color-link)",
                    fontWeight: 600,
                  }}
                >
                  Low-noise review flow
                </span>
              </div>
              <div
                style={{
                  display: "grid",
                  gap: "10px",
                }}
                className="sm:grid-cols-3"
              >
                <MetricCard value="14" label="이번 주 발행" />
                <MetricCard value="06" label="검토 대기" />
                <MetricCard value="92%" label="마감 준수율" />
              </div>
            </div>
          </div>
        </div>

        <HeroWorkspace />
      </div>
    </section>
  );
}

function HeroWorkspace() {
  return (
    <div
      style={{
        position: "relative",
        padding: "18px",
        borderRadius: "32px",
        border: "1px solid color-mix(in srgb, var(--color-brand-primary) 16%, var(--color-border))",
        background:
          "linear-gradient(180deg, color-mix(in srgb, var(--color-surface) 74%, var(--color-brand-accent) 26%) 0%, color-mix(in srgb, var(--color-surface-muted) 88%, white 12%) 100%)",
        boxShadow: "0 30px 80px rgba(72, 44, 19, 0.12)",
        overflow: "hidden",
      }}
    >
      <div
        style={{
          position: "absolute",
          inset: "20px 20px auto auto",
          width: "180px",
          height: "180px",
          borderRadius: "999px",
          background:
            "radial-gradient(circle, color-mix(in srgb, var(--color-brand-accent) 60%, transparent) 0%, transparent 72%)",
          opacity: 0.6,
          pointerEvents: "none",
        }}
      />

      <div
        style={{
          display: "grid",
          gap: "16px",
        }}
      >
        <div
          style={{
            display: "flex",
            alignItems: "center",
            justifyContent: "space-between",
            gap: "12px",
            padding: "8px 8px 0",
          }}
        >
          <div style={{ display: "flex", gap: "8px" }}>
            <Dot tone="var(--color-brand-primary)" />
            <Dot tone="var(--color-brand-accent)" />
            <Dot tone="color-mix(in srgb, var(--color-text-subtle) 44%, white)" />
          </div>
          <span
            style={{
              fontSize: "12px",
              letterSpacing: "0.16em",
              textTransform: "uppercase",
              color: "var(--color-text-subtle)",
            }}
          >
            Split-pane editorial workspace
          </span>
        </div>

        <div
          style={{
            display: "grid",
            gap: "14px",
          }}
          className="md:grid-cols-[132px_minmax(0,1.2fr)_188px]"
        >
          <Panel tone="muted" minHeight={520}>
            <div style={{ display: "grid", gap: "18px" }}>
              <SmallLabel>Workspace</SmallLabel>
              <SidebarItem active>이번 주 발행</SidebarItem>
              <SidebarItem>Journal board</SidebarItem>
              <SidebarItem>Team review</SidebarItem>
              <SidebarItem>Schedule</SidebarItem>
              <SidebarItem>Library</SidebarItem>
              <SidebarItem>Settings</SidebarItem>
              <div
                style={{
                  marginTop: "18px",
                  paddingTop: "18px",
                  borderTop: "1px solid var(--color-border)",
                  display: "grid",
                  gap: "10px",
                }}
              >
                <SmallLabel>Today&apos;s cue</SmallLabel>
                <p style={sidebarNote}>
                  메인 CTA는 단 하나만 강조하고, 나머지 액션은 조용하게 후퇴시킵니다.
                </p>
              </div>
            </div>
          </Panel>

          <Panel minHeight={520}>
            <div style={{ display: "grid", gap: "18px" }}>
              <div
                style={{
                  display: "flex",
                  flexWrap: "wrap",
                  alignItems: "center",
                  justifyContent: "space-between",
                  gap: "12px",
                }}
              >
                <div style={{ display: "grid", gap: "6px" }}>
                  <SmallLabel>Draft</SmallLabel>
                  <h2
                      style={{
                        margin: 0,
                        fontFamily: "var(--font-heading)",
                      fontSize: "clamp(1.3rem, 1.8vw, 1.75rem)",
                      lineHeight: 1.02,
                        color: "var(--color-text)",
                      }}
                  >
                    작은 팀이 하나로 리듬을 맞추는 법
                  </h2>
                </div>
                <div
                  style={{
                    padding: "10px 14px",
                    borderRadius: "999px",
                    background: "color-mix(in srgb, var(--color-brand-accent) 26%, var(--color-surface))",
                    border: "1px solid color-mix(in srgb, var(--color-brand-primary) 12%, var(--color-border))",
                    color: "var(--color-link)",
                    fontSize: "13px",
                    fontWeight: 600,
                  }}
                >
                  Review ready
                </div>
              </div>

              <div
                style={{
                  display: "grid",
                  gap: "14px",
                  padding: "24px",
                  borderRadius: "24px",
                  background:
                    "linear-gradient(180deg, color-mix(in srgb, white 80%, var(--color-brand-accent) 20%) 0%, var(--color-surface) 100%)",
                  border: "1px solid color-mix(in srgb, var(--color-brand-primary) 10%, var(--color-border))",
                }}
              >
                <RuleLine />
                <p style={editorLinePrimary}>좋은 팀은 더 많은 탭을 여는 팀이 아니라,</p>
                <p style={editorLineAccent}>같은 문장 위에서 같은 타이밍으로 움직이는 팀이다.</p>
                <RuleLine narrow />
                <p style={editorBody}>
                  Signal Desk는 글쓰기, 검토, 일정 조율이 서로 다른 화면에서 갈라지지 않도록
                  설계되었습니다. 글은 중앙에 머물고, 일정과 코멘트는 같은 문맥 위로 조용히
                  겹쳐집니다.
                </p>
                <div
                  style={{
                    display: "grid",
                    gap: "12px",
                  }}
                  className="sm:grid-cols-2"
                >
                  <MiniCard label="Inline comments" body="문장 위에 얹히되 본문 흐름을 깨지 않는 리뷰." />
                  <MiniCard label="Publishing board" body="칸반과 일정이 같은 편집 템포로 이어지는 운영 레이어." />
                </div>
              </div>
            </div>
          </Panel>

          <Panel tone="muted" minHeight={520}>
            <div style={{ display: "grid", gap: "18px" }}>
              <SmallLabel>Review panel</SmallLabel>
              <ReviewCard
                title="민지 · Features Editor"
                body="히어로 문단 둘째 줄은 더 짧게 끊는 편이 읽기 좋습니다. CTA는 지금 톤이면 충분히 강합니다."
              />
              <ReviewCard
                title="Jae · Managing Editor"
                body="신뢰 라인은 좋지만 수치를 더 많이 늘리기보다 핵심 세 개만 유지하는 편이 Signal Desk답습니다."
              />
              <ReviewCard
                title="Publisher"
                body="이번 주 목요일 발행 슬롯 확보. 리뷰 반영 후 바로 예약 가능합니다."
              />
            </div>
          </Panel>
        </div>
      </div>
    </div>
  );
}

function MetricsBand() {
  return (
    <section style={{ padding: "28px 24px 32px" }}>
      <div
        style={{
          maxWidth: "1280px",
          margin: "0 auto",
          borderTop: "1px solid color-mix(in srgb, var(--color-border) 70%, transparent)",
          borderBottom: "1px solid color-mix(in srgb, var(--color-border) 70%, transparent)",
          padding: "18px 0",
        }}
      >
        <div
          style={{
            display: "grid",
            gap: "14px",
            color: "var(--color-text-subtle)",
            fontSize: "12px",
            letterSpacing: "0.14em",
            textTransform: "uppercase",
          }}
          className="md:grid-cols-[220px_repeat(5,minmax(0,1fr))]"
        >
          <span>Made for editorial operators</span>
          <span>Issue calendar</span>
          <span>Review states</span>
          <span>Type journal</span>
          <span>Low-noise motion</span>
          <span>Warm paper surfaces</span>
        </div>
      </div>
    </section>
  );
}

function EditorialStatement() {
  return (
    <section id="journal" style={{ padding: "56px 24px 32px" }}>
      <div
        style={{
          maxWidth: "1280px",
          margin: "0 auto",
          display: "grid",
          gap: "26px",
        }}
      >
        <div
          style={{
            display: "grid",
            gap: "18px",
            maxWidth: "780px",
          }}
        >
          <SectionEyebrow>Why it feels different</SectionEyebrow>
          <h2 style={sectionHeading}>
            글쓰기와 운영이 하나의 리듬으로
            <br />
            이어지게 만드는 제품
          </h2>
          <p style={sectionBody}>
            대부분의 협업 도구는 정보는 많지만 템포가 없습니다. Signal Desk는 반대로,
            화면의 밀도보다 문장과 검토의 흐름을 먼저 설계합니다. 그래서 내비게이션은
            고정되고, 리뷰는 한 단계 뒤로 물러나며, 중요한 숫자도 과장되지 않은 카드 위에
            앉습니다.
          </p>
        </div>

        <div
          style={{
            display: "grid",
            gap: "16px",
          }}
          className="lg:grid-cols-3"
        >
          {featureColumns.map((item) => (
            <article key={item.title} style={editorialColumnCard}>
              <div style={{ display: "grid", gap: "14px" }}>
                <h3 style={columnTitle}>{item.title}</h3>
                <p style={columnBody}>{item.body}</p>
              </div>
              <ul style={columnList}>
                {item.points.map((point) => (
                  <li key={point} style={columnListItem}>
                    {point}
                  </li>
                ))}
              </ul>
            </article>
          ))}
        </div>
      </div>
    </section>
  );
}

function FeatureGallery() {
  return (
    <section id="features" style={{ padding: "40px 24px 40px" }}>
      <div
        style={{
          maxWidth: "1280px",
          margin: "0 auto",
          display: "grid",
          gap: "18px",
        }}
      >
        <div
          style={{
            display: "flex",
            flexWrap: "wrap",
            alignItems: "end",
            justifyContent: "space-between",
            gap: "18px",
          }}
        >
          <div style={{ display: "grid", gap: "12px", maxWidth: "740px" }}>
            <SectionEyebrow>Feature composition</SectionEyebrow>
            <h2 style={sectionHeading}>과장 대신 편집 감각으로 재배치한 4개의 핵심 장면</h2>
          </div>
          <p
            style={{
              margin: 0,
              maxWidth: "360px",
              color: "var(--color-text-muted)",
              lineHeight: 1.7,
            }}
          >
            모든 블록은 같은 paper tint 위에서 움직이지만, 정보의 성격에 따라 여백과
            강조 비율만 달라집니다.
          </p>
        </div>

        <div
          style={{
            display: "grid",
            gap: "16px",
          }}
          className="lg:grid-cols-2"
        >
          {featureCards.map((card, index) => (
            <article
              key={card.title}
              style={{
                ...featureCardStyle,
                minHeight: index === 0 ? "340px" : "280px",
              }}
            >
              <div style={{ display: "grid", gap: "14px" }}>
                <SectionEyebrow compact>{card.eyebrow}</SectionEyebrow>
                <h3 style={featureCardTitle}>{card.title}</h3>
                <p style={featureCardBody}>{card.body}</p>
              </div>
              <div style={featureIllustration}>
                <div style={featureLineWide} />
                <div style={featureLineMedium} />
                <div style={featureSplitGrid}>
                  <span style={chipStyle}>Schedule</span>
                  <span style={chipStyle}>Review</span>
                  <span style={chipStyle}>Draft</span>
                </div>
              </div>
            </article>
          ))}
        </div>
      </div>
    </section>
  );
}

function TestimonialSection() {
  return (
    <section style={{ padding: "54px 24px 36px" }}>
      <div
        style={{
          maxWidth: "1280px",
          margin: "0 auto",
          display: "grid",
          gap: "18px",
        }}
      >
        <div style={{ display: "grid", gap: "12px", maxWidth: "760px" }}>
          <SectionEyebrow>What editors say</SectionEyebrow>
          <h2 style={sectionHeading}>에디터가 이 제품을 좋아하는 이유는, 더 화려해서가 아니라 더 정갈해서입니다.</h2>
        </div>
        <div
          style={{
            display: "grid",
            gap: "16px",
          }}
          className="lg:grid-cols-3"
        >
          {testimonials.map((item) => (
            <article key={item.author} style={testimonialCard}>
              <p style={testimonialQuote}>&ldquo;{item.quote}&rdquo;</p>
              <div style={{ display: "grid", gap: "4px" }}>
                <strong style={{ color: "var(--color-text)" }}>{item.author}</strong>
                <span style={{ color: "var(--color-text-subtle)", fontSize: "14px" }}>{item.role}</span>
              </div>
            </article>
          ))}
        </div>
      </div>
    </section>
  );
}

function PricingSection() {
  return (
    <section id="pricing" style={{ padding: "48px 24px 44px" }}>
      <div
        style={{
          maxWidth: "1280px",
          margin: "0 auto",
          display: "grid",
          gap: "20px",
        }}
      >
        <div style={{ display: "grid", gap: "12px", maxWidth: "760px" }}>
          <SectionEyebrow>Open pricing</SectionEyebrow>
          <h2 style={sectionHeading}>정직한 가격, 열린 기능</h2>
          <p style={sectionBody}>
            혼자 쓰는 사람부터 작은 편집팀, 에이전시까지. 과장된 엔터프라이즈 포장보다
            실제 운영 리듬에 맞는 구조를 먼저 제안합니다.
          </p>
        </div>
        <div
          style={{
            display: "grid",
            gap: "16px",
          }}
          className="lg:grid-cols-3"
        >
          {pricing.map((tier) => (
            <article
              key={tier.name}
              style={{
                ...pricingCard,
                background: tier.featured
                  ? "linear-gradient(180deg, color-mix(in srgb, var(--color-brand-accent) 18%, var(--color-surface)) 0%, var(--color-surface) 100%)"
                  : "color-mix(in srgb, var(--color-surface) 94%, var(--color-brand-accent) 6%)",
                borderColor: tier.featured
                  ? "color-mix(in srgb, var(--color-brand-primary) 26%, var(--color-border))"
                  : "var(--color-border)",
                boxShadow: tier.featured ? "0 20px 60px rgba(85, 45, 17, 0.1)" : "none",
              }}
            >
              <div style={{ display: "grid", gap: "14px" }}>
                <div
                  style={{
                    display: "flex",
                    alignItems: "center",
                    justifyContent: "space-between",
                    gap: "10px",
                  }}
                >
                  <h3 style={pricingTitle}>{tier.name}</h3>
                  {tier.featured ? (
                    <span style={featuredPill}>Recommended</span>
                  ) : null}
                </div>
                <div style={{ display: "grid", gap: "4px" }}>
                  <div style={{ display: "flex", alignItems: "baseline", gap: "8px" }}>
                    <strong style={pricingPrice}>{tier.price}</strong>
                    <span style={{ color: "var(--color-text-subtle)" }}>/ user / month</span>
                  </div>
                  <p style={pricingCaption}>{tier.caption}</p>
                </div>
              </div>
              <ul style={pricingList}>
                {tier.bullets.map((item) => (
                  <li key={item} style={pricingListItem}>
                    {item}
                  </li>
                ))}
              </ul>
            </article>
          ))}
        </div>
      </div>
    </section>
  );
}

function FaqSection() {
  return (
    <section style={{ padding: "48px 24px 56px" }}>
      <div
        style={{
          maxWidth: "1280px",
          margin: "0 auto",
          display: "grid",
          gap: "18px",
        }}
      >
        <div style={{ display: "grid", gap: "12px", maxWidth: "760px" }}>
          <SectionEyebrow>Frequently asked</SectionEyebrow>
          <h2 style={sectionHeading}>작은 팀이 가장 자주 묻는 질문</h2>
        </div>
        <div
          style={{
            display: "grid",
            gap: "14px",
          }}
          className="lg:grid-cols-2"
        >
          {faqs.map((item) => (
            <article key={item.question} style={faqCard}>
              <h3 style={faqQuestion}>{item.question}</h3>
              <p style={faqAnswer}>{item.answer}</p>
            </article>
          ))}
        </div>
      </div>
    </section>
  );
}

function ClosingSection() {
  return (
    <section style={{ padding: "0 24px 84px" }}>
      <div
        style={{
          maxWidth: "1280px",
          margin: "0 auto",
          padding: "40px clamp(24px, 4vw, 48px)",
          borderRadius: "36px",
          border: "1px solid color-mix(in srgb, var(--color-brand-primary) 18%, var(--color-border))",
          background:
            "linear-gradient(135deg, color-mix(in srgb, var(--color-brand-primary) 92%, white 8%) 0%, color-mix(in srgb, var(--color-brand-primary) 68%, var(--color-brand-accent) 32%) 100%)",
          color: "var(--color-text-inverse)",
          boxShadow: "0 28px 70px rgba(85, 45, 17, 0.16)",
        }}
      >
        <div
          style={{
            display: "grid",
            gap: "24px",
            alignItems: "center",
          }}
          className="lg:grid-cols-[minmax(0,1fr)_auto]"
        >
          <div style={{ display: "grid", gap: "14px", maxWidth: "700px" }}>
            <span
              style={{
                fontSize: "12px",
                letterSpacing: "0.16em",
                textTransform: "uppercase",
                opacity: 0.8,
              }}
            >
              Final call
            </span>
            <h2
              style={{
                margin: 0,
                fontFamily: "var(--font-heading)",
                fontSize: "clamp(2.4rem, 5vw, 4.8rem)",
                lineHeight: 0.95,
                letterSpacing: "-0.04em",
              }}
            >
              첫 문장을 쓰는 순간부터
              <br />
              다르게 느껴질 겁니다.
            </h2>
            <p
              style={{
                margin: 0,
                maxWidth: "520px",
                fontSize: "17px",
                lineHeight: 1.7,
                color: "rgba(255,255,255,0.84)",
              }}
            >
              14일 무료 체험, 신용카드 없이 시작. 작은 팀의 편집 리듬을 해치지 않는 운영
              도구가 어떤 느낌인지 직접 확인해보세요.
            </p>
          </div>
          <div style={{ display: "flex", flexWrap: "wrap", gap: "12px" }}>
            <a href="#pricing" style={closingPrimaryButton}>
              무료로 시작
            </a>
            <a href="#journal" style={closingSecondaryButton}>
              사례 보기
            </a>
          </div>
        </div>
      </div>
    </section>
  );
}

function MetricCard({ value, label }: { value: string; label: string }) {
  return (
    <div
      style={{
        padding: "16px 18px",
        borderRadius: "18px",
        border: "1px solid var(--color-border)",
        background: "color-mix(in srgb, var(--color-surface) 88%, var(--color-brand-accent) 12%)",
        display: "grid",
        gap: "4px",
      }}
    >
      <strong
        style={{
          fontFamily: "var(--font-heading)",
          fontSize: "32px",
          lineHeight: 1,
          color: "var(--color-text)",
        }}
      >
        {value}
      </strong>
      <span style={{ color: "var(--color-text-subtle)", fontSize: "13px" }}>{label}</span>
    </div>
  );
}

function Panel({
  children,
  tone = "default",
  minHeight,
}: {
  children: React.ReactNode;
  tone?: "default" | "muted";
  minHeight: number;
}) {
  return (
    <div
      style={{
        minHeight,
        padding: "18px",
        borderRadius: "24px",
        border: "1px solid var(--color-border)",
        background:
          tone === "muted"
            ? "linear-gradient(180deg, color-mix(in srgb, var(--color-surface) 88%, var(--color-brand-accent) 12%) 0%, color-mix(in srgb, var(--color-surface) 96%, transparent) 100%)"
            : "linear-gradient(180deg, color-mix(in srgb, var(--color-surface) 97%, var(--color-brand-accent) 3%) 0%, var(--color-surface) 100%)",
        boxShadow: tone === "muted" ? "inset 0 1px 0 rgba(255,255,255,0.65)" : "0 8px 32px rgba(71, 41, 18, 0.04)",
      }}
    >
      {children}
    </div>
  );
}

function SidebarItem({
  children,
  active = false,
}: {
  children: React.ReactNode;
  active?: boolean;
}) {
  return (
    <div
      style={{
        padding: "12px 14px",
        borderRadius: "16px",
        border: active
          ? "1px solid color-mix(in srgb, var(--color-brand-primary) 16%, var(--color-border))"
          : "1px solid transparent",
        background: active
          ? "color-mix(in srgb, var(--color-surface) 76%, var(--color-brand-accent) 24%)"
          : "transparent",
        color: active ? "var(--color-text)" : "var(--color-text-muted)",
        fontWeight: active ? 600 : 500,
      }}
    >
      {children}
    </div>
  );
}

function ReviewCard({ title, body }: { title: string; body: string }) {
  return (
    <div
      style={{
        padding: "16px",
        borderRadius: "18px",
        border: "1px solid var(--color-border)",
        background: "var(--color-surface)",
        display: "grid",
        gap: "8px",
      }}
    >
      <strong style={{ color: "var(--color-text)", fontSize: "14px" }}>{title}</strong>
      <p style={{ margin: 0, color: "var(--color-text-muted)", lineHeight: 1.65, fontSize: "14px" }}>
        {body}
      </p>
    </div>
  );
}

function MiniCard({ label, body }: { label: string; body: string }) {
  return (
    <div
      style={{
        padding: "16px",
        borderRadius: "18px",
        background: "color-mix(in srgb, var(--color-surface-muted) 78%, white 22%)",
        border: "1px solid var(--color-border)",
        display: "grid",
        gap: "8px",
      }}
    >
      <strong style={{ color: "var(--color-text)", fontSize: "14px" }}>{label}</strong>
      <p style={{ margin: 0, color: "var(--color-text-muted)", fontSize: "14px", lineHeight: 1.6 }}>
        {body}
      </p>
    </div>
  );
}

function Dot({ tone }: { tone: string }) {
  return (
    <span
      style={{
        width: "10px",
        height: "10px",
        borderRadius: "999px",
        background: tone,
        display: "inline-block",
      }}
    />
  );
}

function RuleLine({ narrow = false }: { narrow?: boolean }) {
  return (
    <div
      style={{
        width: narrow ? "44%" : "100%",
        height: "1px",
        background: "linear-gradient(90deg, var(--color-border-strong) 0%, transparent 100%)",
      }}
    />
  );
}

function SmallLabel({ children }: { children: React.ReactNode }) {
  return (
    <span
      style={{
        fontSize: "11px",
        letterSpacing: "0.16em",
        textTransform: "uppercase",
        color: "var(--color-text-subtle)",
      }}
    >
      {children}
    </span>
  );
}

function SectionEyebrow({
  children,
  compact = false,
}: {
  children: React.ReactNode;
  compact?: boolean;
}) {
  return (
    <span
      style={{
        width: "fit-content",
        padding: compact ? "0" : "7px 11px",
        borderRadius: compact ? 0 : "999px",
        border: compact ? "none" : "1px solid color-mix(in srgb, var(--color-brand-primary) 14%, var(--color-border))",
        background: compact ? "transparent" : "color-mix(in srgb, var(--color-surface) 82%, var(--color-brand-accent) 18%)",
        color: "var(--color-link)",
        fontSize: compact ? "11px" : "12px",
        letterSpacing: "0.16em",
        textTransform: "uppercase",
        fontWeight: 700,
      }}
    >
      {children}
    </span>
  );
}

const heroPrimaryButton: React.CSSProperties = {
  display: "inline-flex",
  alignItems: "center",
  justifyContent: "center",
  minHeight: "52px",
  padding: "0 22px",
  borderRadius: "999px",
  background: "var(--color-brand-primary)",
  color: "var(--color-text-inverse)",
  textDecoration: "none",
  fontWeight: 700,
  boxShadow: "0 14px 30px rgba(114, 62, 20, 0.18)",
};

const heroSecondaryButton: React.CSSProperties = {
  display: "inline-flex",
  alignItems: "center",
  justifyContent: "center",
  minHeight: "52px",
  padding: "0 22px",
  borderRadius: "999px",
  border: "1px solid var(--color-border-strong)",
  background: "color-mix(in srgb, var(--color-surface) 88%, var(--color-brand-accent) 12%)",
  color: "var(--color-text)",
  textDecoration: "none",
  fontWeight: 600,
};

const closingPrimaryButton: React.CSSProperties = {
  display: "inline-flex",
  alignItems: "center",
  justifyContent: "center",
  minHeight: "52px",
  padding: "0 22px",
  borderRadius: "999px",
  background: "rgba(255,255,255,0.96)",
  color: "var(--color-brand-primary)",
  textDecoration: "none",
  fontWeight: 700,
};

const closingSecondaryButton: React.CSSProperties = {
  display: "inline-flex",
  alignItems: "center",
  justifyContent: "center",
  minHeight: "52px",
  padding: "0 22px",
  borderRadius: "999px",
  border: "1px solid rgba(255,255,255,0.28)",
  background: "rgba(255,255,255,0.08)",
  color: "white",
  textDecoration: "none",
  fontWeight: 600,
};

const editorLinePrimary: React.CSSProperties = {
  margin: 0,
  fontFamily: "var(--font-heading)",
  fontSize: "clamp(1.45rem, 2.4vw, 2.15rem)",
  lineHeight: 1.12,
  wordBreak: "keep-all",
  overflowWrap: "normal",
  textWrap: "balance",
  color: "var(--color-text)",
};

const editorLineAccent: React.CSSProperties = {
  margin: 0,
  fontFamily: "var(--font-heading)",
  fontSize: "clamp(1.25rem, 2vw, 1.8rem)",
  lineHeight: 1.14,
  wordBreak: "keep-all",
  overflowWrap: "normal",
  textWrap: "balance",
  color: "var(--color-link)",
};

const editorBody: React.CSSProperties = {
  margin: 0,
  color: "var(--color-text-muted)",
  fontSize: "15px",
  lineHeight: 1.85,
};

const sidebarNote: React.CSSProperties = {
  margin: 0,
  color: "var(--color-text-muted)",
  fontSize: "14px",
  lineHeight: 1.65,
};

const sectionHeading: React.CSSProperties = {
  margin: 0,
  fontFamily: "var(--font-heading)",
  fontSize: landingType.section,
  lineHeight: 1.08,
  letterSpacing: "-0.04em",
  wordBreak: "keep-all",
  overflowWrap: "normal",
  textWrap: "balance",
  color: "var(--color-text)",
};

const sectionBody: React.CSSProperties = {
  margin: 0,
  color: "var(--color-text-muted)",
  fontSize: "16px",
  lineHeight: 1.72,
  wordBreak: "keep-all",
  overflowWrap: "normal",
};

const editorialColumnCard: React.CSSProperties = {
  padding: "24px",
  borderRadius: "24px",
  border: "1px solid var(--color-border)",
  background:
    "linear-gradient(180deg, color-mix(in srgb, var(--color-surface) 90%, var(--color-brand-accent) 10%) 0%, var(--color-surface) 100%)",
  display: "grid",
  gap: "18px",
  minHeight: "100%",
};

const columnTitle: React.CSSProperties = {
  margin: 0,
  fontFamily: "var(--font-heading)",
  fontSize: landingType.cardTitle,
  lineHeight: 1.08,
  wordBreak: "keep-all",
  overflowWrap: "normal",
  textWrap: "balance",
  color: "var(--color-text)",
};

const columnBody: React.CSSProperties = {
  margin: 0,
  color: "var(--color-text-muted)",
  lineHeight: 1.66,
  wordBreak: "keep-all",
  overflowWrap: "normal",
};

const columnList: React.CSSProperties = {
  margin: 0,
  padding: 0,
  listStyle: "none",
  display: "grid",
  gap: "10px",
};

const columnListItem: React.CSSProperties = {
  paddingTop: "10px",
  borderTop: "1px solid color-mix(in srgb, var(--color-border) 70%, transparent)",
  color: "var(--color-text)",
  fontSize: "14px",
};

const featureCardStyle: React.CSSProperties = {
  padding: "24px",
  borderRadius: "28px",
  border: "1px solid var(--color-border)",
  background:
    "linear-gradient(180deg, color-mix(in srgb, var(--color-surface) 88%, var(--color-brand-accent) 12%) 0%, var(--color-surface) 100%)",
  display: "grid",
  gap: "22px",
  alignContent: "space-between",
  boxShadow: "0 16px 40px rgba(64, 34, 15, 0.05)",
};

const featureCardTitle: React.CSSProperties = {
  margin: 0,
  fontFamily: "var(--font-heading)",
  fontSize: landingType.cardTitle,
  lineHeight: 1.08,
  wordBreak: "keep-all",
  overflowWrap: "normal",
  textWrap: "balance",
  color: "var(--color-text)",
};

const featureCardBody: React.CSSProperties = {
  margin: 0,
  color: "var(--color-text-muted)",
  lineHeight: 1.66,
  wordBreak: "keep-all",
  overflowWrap: "normal",
};

const featureIllustration: React.CSSProperties = {
  padding: "18px",
  borderRadius: "22px",
  background: "color-mix(in srgb, var(--color-surface-muted) 76%, white 24%)",
  border: "1px solid color-mix(in srgb, var(--color-brand-primary) 10%, var(--color-border))",
  display: "grid",
  gap: "12px",
};

const featureLineWide: React.CSSProperties = {
  height: "16px",
  width: "72%",
  borderRadius: "999px",
  background: "color-mix(in srgb, var(--color-text) 12%, white)",
};

const featureLineMedium: React.CSSProperties = {
  height: "10px",
  width: "48%",
  borderRadius: "999px",
  background: "color-mix(in srgb, var(--color-text) 8%, white)",
};

const featureSplitGrid: React.CSSProperties = {
  display: "flex",
  flexWrap: "wrap",
  gap: "10px",
};

const chipStyle: React.CSSProperties = {
  display: "inline-flex",
  alignItems: "center",
  justifyContent: "center",
  minHeight: "34px",
  padding: "0 14px",
  borderRadius: "999px",
  border: "1px solid var(--color-border)",
  background: "var(--color-surface)",
  color: "var(--color-text-muted)",
  fontSize: "13px",
};

const testimonialCard: React.CSSProperties = {
  padding: "24px",
  borderRadius: "24px",
  border: "1px solid var(--color-border)",
  background: "color-mix(in srgb, var(--color-surface) 96%, var(--color-brand-accent) 4%)",
  display: "grid",
  gap: "18px",
};

const testimonialQuote: React.CSSProperties = {
  margin: 0,
  fontFamily: "var(--font-heading)",
  fontSize: landingType.quote,
  lineHeight: 1.28,
  wordBreak: "keep-all",
  overflowWrap: "normal",
  textWrap: "balance",
  color: "var(--color-text)",
};

const pricingCard: React.CSSProperties = {
  padding: "24px",
  borderRadius: "28px",
  border: "1px solid var(--color-border)",
  display: "grid",
  gap: "20px",
};

const pricingTitle: React.CSSProperties = {
  margin: 0,
  fontFamily: "var(--font-heading)",
  fontSize: landingType.pricingTitle,
  lineHeight: 1.04,
  color: "var(--color-text)",
};

const featuredPill: React.CSSProperties = {
  padding: "8px 12px",
  borderRadius: "999px",
  background: "var(--color-brand-primary)",
  color: "var(--color-text-inverse)",
  fontSize: "12px",
  letterSpacing: "0.14em",
  textTransform: "uppercase",
  fontWeight: 700,
};

const pricingPrice: React.CSSProperties = {
  fontFamily: "var(--font-heading)",
  fontSize: landingType.pricingPrice,
  lineHeight: 0.98,
  color: "var(--color-text)",
};

const pricingCaption: React.CSSProperties = {
  margin: 0,
  color: "var(--color-text-muted)",
  lineHeight: 1.7,
  wordBreak: "keep-all",
  overflowWrap: "normal",
};

const pricingList: React.CSSProperties = {
  margin: 0,
  padding: 0,
  listStyle: "none",
  display: "grid",
  gap: "10px",
};

const pricingListItem: React.CSSProperties = {
  paddingTop: "10px",
  borderTop: "1px solid color-mix(in srgb, var(--color-border) 76%, transparent)",
  color: "var(--color-text)",
};

const faqCard: React.CSSProperties = {
  padding: "22px",
  borderRadius: "24px",
  border: "1px solid var(--color-border)",
  background:
    "linear-gradient(180deg, color-mix(in srgb, var(--color-surface) 94%, var(--color-brand-accent) 6%) 0%, var(--color-surface) 100%)",
  display: "grid",
  gap: "12px",
};

const faqQuestion: React.CSSProperties = {
  margin: 0,
  fontFamily: "var(--font-heading)",
  fontSize: landingType.faq,
  lineHeight: 1.14,
  wordBreak: "keep-all",
  overflowWrap: "normal",
  textWrap: "balance",
  color: "var(--color-text)",
};

const faqAnswer: React.CSSProperties = {
  margin: 0,
  color: "var(--color-text-muted)",
  lineHeight: 1.72,
  wordBreak: "keep-all",
  overflowWrap: "normal",
};
