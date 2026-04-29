type PressQuoteProps = {
  quote: string;
  source: string;
};

export function PressQuote({ quote, source }: PressQuoteProps) {
  return (
    <blockquote
      style={{
        margin: 0,
        paddingLeft: "var(--space-24)",
        paddingTop: "var(--space-8)",
        paddingBottom: "var(--space-8)",
        borderLeft: "2px solid var(--color-border-strong)",
        maxWidth: "640px",
        marginLeft: "auto",
        marginRight: "auto",
      }}
    >
      <p
        style={{
          margin: 0,
          fontFamily: "var(--font-body)",
          fontSize: "var(--text-md)",
          lineHeight: "var(--leading-relaxed)",
          color: "var(--color-text-muted)",
          fontStyle: "italic",
        }}
      >
        {quote}
      </p>
      <cite
        style={{
          display: "block",
          marginTop: "var(--space-8)",
          fontFamily: "var(--font-mono)",
          fontSize: "var(--text-xs)",
          color: "var(--color-text-subtle)",
          fontStyle: "normal",
          letterSpacing: "0em",
          textTransform: "uppercase",
        }}
      >
        {source}
      </cite>
    </blockquote>
  );
}
