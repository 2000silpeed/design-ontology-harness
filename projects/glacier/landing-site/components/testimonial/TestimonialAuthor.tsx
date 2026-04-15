type TestimonialAuthorProps = {
  name: string;
  role: string;
  company: string;
};

export function TestimonialAuthor({ name, role, company }: TestimonialAuthorProps) {
  return (
    <cite
      style={{
        display: "flex",
        flexDirection: "column",
        gap: "var(--space-2)",
        fontFamily: "var(--font-body)",
        fontSize: "var(--text-sm)",
        fontStyle: "normal",
        lineHeight: "var(--leading-normal)",
      }}
    >
      <span
        style={{
          color: "var(--color-text)",
          fontWeight: 600,
        }}
      >
        {name}
      </span>
      <span
        style={{
          color: "var(--color-text-muted)",
        }}
      >
        {role} · {company}
      </span>
    </cite>
  );
}
