type Cell = boolean | string;

type Row = {
  feature: string;
  values: [Cell, Cell, Cell];
};

const PLANS = ["Starter", "Team", "Enterprise"] as const;

const ROWS: Row[] = [
  { feature: "아카이브 용량", values: ["100GB", "1TB", "무제한"] },
  { feature: "보존 기간", values: ["7일", "무제한", "무제한"] },
  { feature: "SHA-256 체크섬", values: [true, true, true] },
  { feature: "정책 엔진", values: [false, true, true] },
  { feature: "감사 로그 내보내기", values: [false, true, true] },
  { feature: "SSO / SAML", values: [false, false, true] },
  { feature: "전담 엔지니어", values: [false, false, true] },
  { feature: "맞춤 SLA", values: [false, false, true] },
];

function CheckIcon() {
  return (
    <svg
      width="18"
      height="18"
      viewBox="0 0 18 18"
      fill="none"
      aria-hidden="true"
      style={{ color: "var(--color-brand-primary)" }}
    >
      <path
        d="M3.75 9.5l3.25 3.25L14.25 5.25"
        stroke="currentColor"
        strokeWidth="1.75"
        strokeLinecap="round"
        strokeLinejoin="round"
      />
    </svg>
  );
}

function DashIcon() {
  return (
    <svg
      width="18"
      height="18"
      viewBox="0 0 18 18"
      fill="none"
      aria-hidden="true"
      style={{ color: "var(--color-text-subtle)" }}
    >
      <path
        d="M4 9h10"
        stroke="currentColor"
        strokeWidth="1.75"
        strokeLinecap="round"
      />
    </svg>
  );
}

function renderCell(value: Cell) {
  if (value === true) {
    return (
      <>
        <CheckIcon />
        <span className="sr-only">포함</span>
      </>
    );
  }
  if (value === false) {
    return (
      <>
        <DashIcon />
        <span className="sr-only">미포함</span>
      </>
    );
  }
  return <span>{value}</span>;
}

export function FeatureComparison() {
  return (
    <div
      role="region"
      aria-label="요금제 기능 비교"
      style={{
        marginTop: "var(--space-64)",
        width: "100%",
        overflowX: "auto",
        border: "1px solid var(--color-border)",
        borderRadius: "var(--radius-xl)",
        background: "var(--color-surface)",
      }}
      className="feature-comparison-scroll"
    >
      <table
        style={{
          width: "100%",
          minWidth: "640px",
          borderCollapse: "collapse",
          fontFamily: "var(--font-body)",
          fontSize: "var(--text-md)",
          color: "var(--color-text)",
        }}
      >
        <caption
          style={{
            captionSide: "top",
            textAlign: "left",
            padding: "var(--space-24) var(--space-24) var(--space-16)",
            fontFamily: "var(--font-heading)",
            fontSize: "var(--text-lg)",
            fontWeight: 700,
            color: "var(--color-text)",
          }}
        >
          플랜별 기능 비교
          <span
            style={{
              display: "block",
              marginTop: "var(--space-4)",
              fontFamily: "var(--font-body)",
              fontSize: "var(--text-sm)",
              fontWeight: 400,
              color: "var(--color-text-muted)",
            }}
          >
            8개 항목 기준 요약
          </span>
        </caption>
        <thead>
          <tr style={{ borderTop: "1px solid var(--color-border)" }}>
            <th
              scope="col"
              style={{
                position: "sticky",
                left: 0,
                zIndex: 1,
                background: "var(--color-surface-muted)",
                textAlign: "left",
                padding: "var(--space-16) var(--space-24)",
                fontFamily: "var(--font-body)",
                fontSize: "var(--text-sm)",
                fontWeight: 600,
                color: "var(--color-text-muted)",
                letterSpacing: "0.04em",
                textTransform: "uppercase",
                borderBottom: "1px solid var(--color-border)",
              }}
            >
              기능
            </th>
            {PLANS.map((plan) => (
              <th
                key={plan}
                scope="col"
                style={{
                  background: "var(--color-surface-muted)",
                  textAlign: "center",
                  padding: "var(--space-16) var(--space-24)",
                  fontFamily: "var(--font-body)",
                  fontSize: "var(--text-sm)",
                  fontWeight: 700,
                  color: "var(--color-text)",
                  borderBottom: "1px solid var(--color-border)",
                }}
              >
                {plan}
              </th>
            ))}
          </tr>
        </thead>
        <tbody>
          {ROWS.map((row, index) => (
            <tr
              key={row.feature}
              style={{
                background:
                  index % 2 === 0
                    ? "var(--color-surface)"
                    : "var(--color-canvas)",
              }}
            >
              <th
                scope="row"
                style={{
                  position: "sticky",
                  left: 0,
                  zIndex: 1,
                  background: "inherit",
                  textAlign: "left",
                  padding: "var(--space-16) var(--space-24)",
                  fontFamily: "var(--font-body)",
                  fontSize: "var(--text-md)",
                  fontWeight: 500,
                  color: "var(--color-text)",
                  borderBottom: "1px solid var(--color-border)",
                }}
              >
                {row.feature}
              </th>
              {row.values.map((value, i) => (
                <td
                  key={`${row.feature}-${i}`}
                  style={{
                    textAlign: "center",
                    padding: "var(--space-16) var(--space-24)",
                    borderBottom: "1px solid var(--color-border)",
                    verticalAlign: "middle",
                  }}
                >
                  <span
                    style={{
                      display: "inline-flex",
                      alignItems: "center",
                      justifyContent: "center",
                      color: "var(--color-text)",
                    }}
                  >
                    {renderCell(value)}
                  </span>
                </td>
              ))}
            </tr>
          ))}
        </tbody>
      </table>
      <style>{`
        .feature-comparison-scroll .sr-only {
          position: absolute;
          width: 1px;
          height: 1px;
          padding: 0;
          margin: -1px;
          overflow: hidden;
          clip: rect(0, 0, 0, 0);
          white-space: nowrap;
          border: 0;
        }
      `}</style>
    </div>
  );
}
