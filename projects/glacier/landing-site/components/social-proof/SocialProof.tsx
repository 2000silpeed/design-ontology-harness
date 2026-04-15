import { LogoCloud } from "./LogoCloud";
import { MetricHighlight } from "./MetricHighlight";
import { PressQuote } from "./PressQuote";

const CUSTOMER_NAMES = [
  "Acme Labs",
  "Northstar",
  "Merit",
  "Circuit",
  "Parallel",
  "Keystone",
];

const METRICS = [
  { value: "50 PB", label: "관리 중인 아카이브" },
  { value: "99.99%", label: "복원 성공률" },
  { value: "0건", label: "무결성 위반 사고" },
];

export function SocialProof() {
  return (
    <section
      aria-labelledby="social-proof-heading"
      style={{
        background: "var(--color-canvas)",
        paddingTop: "var(--space-96)",
        paddingBottom: "var(--space-96)",
        paddingLeft: "var(--space-24)",
        paddingRight: "var(--space-24)",
      }}
    >
      <div
        style={{
          maxWidth: "1120px",
          marginLeft: "auto",
          marginRight: "auto",
          display: "flex",
          flexDirection: "column",
          gap: "var(--space-64)",
        }}
      >
        <h2
          id="social-proof-heading"
          style={{
            margin: 0,
            textAlign: "center",
            fontFamily: "var(--font-heading)",
            fontSize: "var(--text-sm)",
            fontWeight: 500,
            color: "var(--color-text-muted)",
            letterSpacing: "0.08em",
            textTransform: "uppercase",
          }}
        >
          엔지니어링 팀이 선택한 아카이브
        </h2>

        <LogoCloud names={CUSTOMER_NAMES} />

        <div
          style={{
            display: "grid",
            gridTemplateColumns: "repeat(auto-fit, minmax(180px, 1fr))",
            gap: "var(--space-32)",
            alignItems: "start",
          }}
        >
          {METRICS.map((metric) => (
            <MetricHighlight
              key={metric.value}
              value={metric.value}
              label={metric.label}
            />
          ))}
        </div>

        <PressQuote
          quote={"\u201C규제 대응과 복원 신뢰도를 동시에 잡는 유일한 선택\u201D"}
          source="TechRadar"
        />
      </div>
    </section>
  );
}
