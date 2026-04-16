type HeroEyebrowProps = {
  children: React.ReactNode;
};

export function HeroEyebrow({ children }: HeroEyebrowProps) {
  return (
    <div
      style={{
        display: "inline-flex",
        alignItems: "center",
        gap: "var(--space-8)",
        paddingTop: "var(--space-8)",
        paddingBottom: "var(--space-8)",
        paddingLeft: "var(--space-12)",
        paddingRight: "var(--space-12)",
        background: "var(--color-surface-tint)",
        color: "var(--color-brand-primary)",
        borderRadius: "var(--radius-pill)",
        fontFamily: "var(--font-mono)",
        fontSize: "var(--text-xs)",
        fontWeight: 600,
        letterSpacing: "0.08em",
        textTransform: "uppercase",
        lineHeight: "var(--leading-tight)",
      }}
    >
      <svg
        width="12"
        height="12"
        viewBox="0 0 16 16"
        fill="none"
        aria-hidden="true"
      >
        <circle
          cx="8"
          cy="8"
          r="3"
          fill="currentColor"
        />
        <circle
          cx="8"
          cy="8"
          r="6.5"
          stroke="currentColor"
          strokeWidth="1"
          opacity="0.4"
        />
      </svg>
      <span>{children}</span>
    </div>
  );
}
