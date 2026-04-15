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
        fontSize: "var(--text-5xl)",
        fontWeight: 700,
        lineHeight: "var(--leading-tight)",
        letterSpacing: "-0.02em",
        color: "var(--color-text)",
        maxWidth: "16ch",
      }}
    >
      {children}
    </h1>
  );
}
