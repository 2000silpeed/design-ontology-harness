type Props = {
  text: string;
  cite: string;
};

export function PressQuote({ text, cite }: Props) {
  return (
    <blockquote
      style={{
        margin: 0,
        borderLeft: "2px solid var(--color-border-strong)",
        paddingLeft: "var(--space-16)",
        display: "flex",
        flexDirection: "column",
        gap: "var(--space-8)",
        maxWidth: "640px",
      }}
    >
      <p
        style={{
          margin: 0,
          fontFamily: "var(--font-heading)",
          fontStyle: "italic",
          fontSize: "var(--text-md)",
          lineHeight: "var(--leading-relaxed)",
          color: "var(--color-text-muted)",
          fontWeight: 400,
        }}
      >
        {text}
      </p>
      <cite
        style={{
          fontFamily: "var(--font-mono)",
          fontSize: "var(--text-xs)",
          color: "var(--color-text-subtle)",
          fontStyle: "normal",
          letterSpacing: "0.04em",
          textTransform: "uppercase",
        }}
      >
        {cite}
      </cite>
    </blockquote>
  );
}
