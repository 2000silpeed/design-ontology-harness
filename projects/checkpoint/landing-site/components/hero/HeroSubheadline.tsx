type HeroSubheadlineProps = {
  children: React.ReactNode;
};

export function HeroSubheadline({ children }: HeroSubheadlineProps) {
  return (
    <p
      style={{
        marginTop: "var(--space-24)",
        marginBottom: 0,
        fontFamily: "var(--font-body)",
        fontSize: "var(--text-lg)",
        lineHeight: "var(--leading-relaxed)",
        color: "var(--color-text-muted)",
        maxWidth: "54ch",
      }}
    >
      {children}
    </p>
  );
}
