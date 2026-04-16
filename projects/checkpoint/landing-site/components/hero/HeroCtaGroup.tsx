type HeroCtaGroupProps = {
  primaryLabel: string;
  primaryHref?: string;
  secondaryLabel: string;
  secondaryHref?: string;
};

export function HeroCtaGroup({
  primaryLabel,
  primaryHref = "#get-started",
  secondaryLabel,
  secondaryHref = "#book-demo",
}: HeroCtaGroupProps) {
  return (
    <div
      role="group"
      aria-label="Primary call to action"
      style={{
        marginTop: "var(--space-32)",
        display: "flex",
        flexWrap: "wrap",
        gap: "var(--space-16)",
        alignItems: "center",
      }}
    >
      <a
        href={primaryHref}
        className="hero-cta-primary"
        style={{
          display: "inline-flex",
          alignItems: "center",
          justifyContent: "center",
          gap: "var(--space-8)",
          minHeight: "44px",
          paddingTop: "var(--space-12)",
          paddingBottom: "var(--space-12)",
          paddingLeft: "var(--space-24)",
          paddingRight: "var(--space-24)",
          background: "var(--color-brand-primary)",
          color: "var(--color-text-inverse)",
          borderRadius: "var(--radius-md)",
          fontFamily: "var(--font-body)",
          fontSize: "var(--text-md)",
          fontWeight: 600,
          textDecoration: "none",
          border: "1px solid var(--color-brand-primary)",
          transitionProperty: "background-color, transform, box-shadow",
          transitionDuration: "var(--duration-180)",
          transitionTimingFunction: "var(--ease-standard)",
        }}
      >
        <span>{primaryLabel}</span>
        <svg
          width="16"
          height="16"
          viewBox="0 0 16 16"
          fill="none"
          aria-hidden="true"
        >
          <path
            d="M3.5 8h9M8.5 4l4 4-4 4"
            stroke="currentColor"
            strokeWidth="1.75"
            strokeLinecap="round"
            strokeLinejoin="round"
          />
        </svg>
      </a>
      <a
        href={secondaryHref}
        className="hero-cta-secondary"
        style={{
          display: "inline-flex",
          alignItems: "center",
          justifyContent: "center",
          gap: "var(--space-8)",
          minHeight: "44px",
          paddingTop: "var(--space-12)",
          paddingBottom: "var(--space-12)",
          paddingLeft: "var(--space-24)",
          paddingRight: "var(--space-24)",
          background: "var(--color-surface)",
          color: "var(--color-text)",
          borderRadius: "var(--radius-md)",
          fontFamily: "var(--font-body)",
          fontSize: "var(--text-md)",
          fontWeight: 600,
          textDecoration: "none",
          border: "1px solid var(--color-border-strong)",
          transitionProperty: "background-color, border-color, transform",
          transitionDuration: "var(--duration-180)",
          transitionTimingFunction: "var(--ease-standard)",
        }}
      >
        <svg
          width="16"
          height="16"
          viewBox="0 0 16 16"
          fill="none"
          aria-hidden="true"
        >
          <rect
            x="2"
            y="3"
            width="12"
            height="11"
            rx="1.5"
            stroke="currentColor"
            strokeWidth="1.5"
          />
          <path
            d="M2 6h12M5.5 1.5v3M10.5 1.5v3"
            stroke="currentColor"
            strokeWidth="1.5"
            strokeLinecap="round"
          />
        </svg>
        <span>{secondaryLabel}</span>
      </a>
      <style>{`
        .hero-cta-primary:hover {
          background: var(--color-link-hover);
          border-color: var(--color-link-hover);
        }
        .hero-cta-primary:active {
          transform: translateY(1px);
        }
        .hero-cta-secondary:hover {
          background: var(--color-surface-muted);
          border-color: var(--color-brand-primary);
        }
        .hero-cta-secondary:active {
          transform: translateY(1px);
        }
      `}</style>
    </div>
  );
}
