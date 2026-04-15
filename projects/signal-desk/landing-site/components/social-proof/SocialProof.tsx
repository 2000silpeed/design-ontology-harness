import { LogoCloud } from "./LogoCloud";
import { MetricHighlight } from "./MetricHighlight";
import { PressQuote } from "./PressQuote";

const LOGOS = [
  "이음 매거진",
  "Quire Studio",
  "Type Journal",
  "Paperwork",
  "Margin House",
  "Foregrounds",
];

const METRICS = [
  { value: "2,400+", label: "활성 에디터" },
  { value: "1,200만", label: "월간 작성 단어" },
  { value: "99.9%", label: "연간 가동률" },
];

const PRESS_QUOTE = {
  text: "에디터의 언어를 이해하는 유일한 워크스페이스",
  cite: "Type Journal, 2025",
};

export function SocialProof() {
  return (
    <section
      aria-labelledby="social-proof-heading"
      style={{
        background: "var(--color-canvas)",
        paddingTop: "var(--space-64)",
        paddingBottom: "var(--space-64)",
        paddingLeft: "var(--space-24)",
        paddingRight: "var(--space-24)",
      }}
    >
      <div
        style={{
          maxWidth: "1200px",
          margin: "0 auto",
          display: "flex",
          flexDirection: "column",
          alignItems: "stretch",
          gap: "var(--space-48)",
        }}
      >
        <h2
          id="social-proof-heading"
          style={{
            margin: 0,
            textAlign: "center",
            fontFamily: "var(--font-mono)",
            fontSize: "var(--text-xs)",
            color: "var(--color-text-subtle)",
            textTransform: "uppercase",
            letterSpacing: "0.12em",
            fontWeight: 500,
          }}
        >
          신뢰받는 콘텐츠 팀의 도구
        </h2>

        <LogoCloud names={LOGOS} />

        <div
          className="sd-metric-row"
          style={{
            display: "grid",
            gridTemplateColumns: "1fr",
            gap: "var(--space-32)",
          }}
        >
          {METRICS.map((m) => (
            <MetricHighlight key={m.label} value={m.value} label={m.label} />
          ))}
        </div>

        <div style={{ display: "flex", justifyContent: "center" }}>
          <PressQuote text={PRESS_QUOTE.text} cite={PRESS_QUOTE.cite} />
        </div>
      </div>
      <style>{`
        @media (min-width: 720px) {
          .sd-metric-row { grid-template-columns: repeat(3, minmax(0, 1fr)) !important; }
        }
      `}</style>
    </section>
  );
}
