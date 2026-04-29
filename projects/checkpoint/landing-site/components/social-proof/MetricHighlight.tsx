type MetricHighlightProps = {
  value: string;
  label: string;
};

export function MetricHighlight({ value, label }: MetricHighlightProps) {
  return (
    <div
      style={{
        display: "flex",
        flexDirection: "column",
        alignItems: "center",
        gap: "var(--space-8)",
        paddingTop: "var(--space-16)",
        paddingBottom: "var(--space-16)",
        paddingLeft: "var(--space-24)",
        paddingRight: "var(--space-24)",
        textAlign: "center",
      }}
    >
      <span
        style={{
          fontFamily: "var(--font-heading)",
          fontSize: "var(--text-4xl)",
          lineHeight: "var(--leading-tight)",
          color: "var(--color-text)",
          fontWeight: 600,
          letterSpacing: "0em",
        }}
      >
        {value}
      </span>
      <span
        style={{
          fontFamily: "var(--font-body)",
          fontSize: "var(--text-sm)",
          color: "var(--color-text-muted)",
          lineHeight: "var(--leading-normal)",
        }}
      >
        {label}
      </span>
    </div>
  );
}
