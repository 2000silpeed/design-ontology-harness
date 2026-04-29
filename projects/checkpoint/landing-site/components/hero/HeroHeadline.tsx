type HeroHeadlineProps = {
  children: React.ReactNode;
  id?: string;
};

export function HeroHeadline({ children, id = "hero-headline" }: HeroHeadlineProps) {
  return (
    <h1
      id={id}
      style={{
        marginTop: "var(--space-24)",
        marginBottom: 0,
        fontFamily: "var(--font-heading)",
        fontSize: "var(--text-4xl)",
        fontWeight: 700,
        lineHeight: "var(--hangul-display-line-height-safe)",
        letterSpacing: "0em",
        color: "var(--color-text)",
        maxWidth: "16ch",
        wordBreak: "keep-all",
        overflowWrap: "normal",
        textWrap: "balance",
      }}
    >
      {children}
    </h1>
  );
}
