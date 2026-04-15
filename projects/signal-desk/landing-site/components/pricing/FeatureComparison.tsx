import type { ReactNode } from "react";

type Row = {
  feature: string;
  values: [boolean, boolean, boolean];
};

const PLANS: readonly string[] = ["Solo", "Studio", "Agency"];

const ROWS: readonly Row[] = [
  { feature: "공동 편집", values: [false, true, true] },
  { feature: "댓글 / 리뷰", values: [false, true, true] },
  { feature: "버전 히스토리", values: [false, true, true] },
  { feature: "발행 일정", values: [false, true, true] },
  { feature: "마크다운 내보내기", values: [true, true, true] },
  { feature: "커스텀 도메인", values: [false, false, true] },
  { feature: "감사 로그", values: [false, false, true] },
  { feature: "전담 에디터 지원", values: [false, false, true] },
];

function IncludedIcon() {
  return (
    <svg
      aria-label="포함"
      role="img"
      width="18"
      height="18"
      viewBox="0 0 20 20"
      fill="none"
      style={{ color: "var(--color-brand-primary)", display: "inline-block", verticalAlign: "middle" }}
    >
      <path
        d="M4 10.5L8 14.5L16 6"
        stroke="currentColor"
        strokeWidth="2"
        strokeLinecap="round"
        strokeLinejoin="round"
      />
    </svg>
  );
}

function NotIncludedIcon() {
  return (
    <svg
      aria-label="미포함"
      role="img"
      width="18"
      height="18"
      viewBox="0 0 20 20"
      fill="none"
      style={{ color: "var(--color-text-subtle)", display: "inline-block", verticalAlign: "middle" }}
    >
      <path
        d="M5 10H15"
        stroke="currentColor"
        strokeWidth="2"
        strokeLinecap="round"
      />
    </svg>
  );
}

export function FeatureComparison(): ReactNode {
  return (
    <div
      className="feature-comparison"
      style={{
        marginTop: "var(--space-64)",
        border: "1px solid var(--color-border)",
        borderRadius: "var(--radius-lg)",
        background: "var(--color-surface)",
        overflowX: "auto",
      }}
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
            position: "absolute",
            width: "1px",
            height: "1px",
            padding: 0,
            margin: "-1px",
            overflow: "hidden",
            clip: "rect(0, 0, 0, 0)",
            whiteSpace: "nowrap",
            border: 0,
          }}
        >
          Signal Desk 플랜별 기능 비교표
        </caption>
        <thead>
          <tr>
            <th
              scope="col"
              style={{
                textAlign: "left",
                padding: "var(--space-16) var(--space-24)",
                fontFamily: "var(--font-heading)",
                fontSize: "var(--text-md)",
                fontWeight: 500,
                color: "var(--color-text)",
                background: "var(--color-surface-muted)",
                borderBottom: "1px solid var(--color-border)",
                position: "sticky",
                left: 0,
                zIndex: 1,
              }}
            >
              기능
            </th>
            {PLANS.map((plan) => (
              <th
                key={plan}
                scope="col"
                style={{
                  textAlign: "center",
                  padding: "var(--space-16) var(--space-24)",
                  fontFamily: "var(--font-heading)",
                  fontSize: "var(--text-md)",
                  fontWeight: 500,
                  color: "var(--color-text)",
                  background: "var(--color-surface-muted)",
                  borderBottom: "1px solid var(--color-border)",
                }}
              >
                {plan}
              </th>
            ))}
          </tr>
        </thead>
        <tbody>
          {ROWS.map((row, idx) => {
            const zebra = idx % 2 === 0 ? "var(--color-surface)" : "var(--color-surface-muted)";
            return (
              <tr key={row.feature}>
                <th
                  scope="row"
                  style={{
                    textAlign: "left",
                    padding: "var(--space-16) var(--space-24)",
                    fontFamily: "var(--font-body)",
                    fontSize: "var(--text-md)",
                    fontWeight: 400,
                    color: "var(--color-text)",
                    background: zebra,
                    borderBottom: "1px solid var(--color-border)",
                    position: "sticky",
                    left: 0,
                  }}
                >
                  {row.feature}
                </th>
                {row.values.map((value, vi) => (
                  <td
                    key={`${row.feature}-${PLANS[vi]}`}
                    style={{
                      textAlign: "center",
                      padding: "var(--space-16) var(--space-24)",
                      background: zebra,
                      borderBottom: "1px solid var(--color-border)",
                    }}
                  >
                    {value ? <IncludedIcon /> : <NotIncludedIcon />}
                  </td>
                ))}
              </tr>
            );
          })}
        </tbody>
      </table>
    </div>
  );
}
