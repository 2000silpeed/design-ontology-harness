type Props = {
  value: string;
  label: string;
};

export function MetricHighlight({ value, label }: Props) {
  return (
    <div
      style={{
        display: "flex",
        flexDirection: "column",
        alignItems: "flex-start",
        gap: "var(--space-8)",
        paddingTop: "var(--space-16)",
        borderTop: "1px solid var(--color-border)",
        minWidth: "180px",
      }}
    >
      <span
        style={{
          fontFamily: "var(--font-heading)",
          fontSize: "var(--text-3xl)",
          lineHeight: "var(--leading-tight)",
          color: "var(--color-text)",
          fontWeight: 500,
          letterSpacing: "-0.01em",
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
