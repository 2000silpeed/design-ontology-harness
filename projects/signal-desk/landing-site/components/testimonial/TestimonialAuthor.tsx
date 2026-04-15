type Props = {
  name: string;
  role: string;
  company: string;
};

export function TestimonialAuthor({ name, role, company }: Props) {
  return (
    <cite
      style={{
        fontStyle: "normal",
        display: "flex",
        flexDirection: "column",
        gap: "var(--space-2)",
      }}
    >
      <span
        style={{
          fontFamily: "var(--font-heading)",
          fontSize: "var(--text-sm)",
          color: "var(--color-text)",
          fontWeight: 500,
          letterSpacing: "0.01em",
        }}
      >
        {name}
      </span>
      <span
        style={{
          fontFamily: "var(--font-body)",
          fontSize: "var(--text-xs)",
          color: "var(--color-text-muted)",
          lineHeight: "var(--leading-normal)",
        }}
      >
        {role} · {company}
      </span>
    </cite>
  );
}
