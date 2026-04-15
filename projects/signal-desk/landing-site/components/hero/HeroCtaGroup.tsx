type Props = {
  primaryLabel: string;
  secondaryLabel: string;
  primaryHref?: string;
  secondaryHref?: string;
};

export function HeroCtaGroup({
  primaryLabel,
  secondaryLabel,
  primaryHref = "#get-started",
  secondaryHref = "#demo",
}: Props) {
  return (
    <div
      style={{
        display: "flex",
        flexWrap: "wrap",
        gap: "var(--space-16)",
        marginBottom: "var(--space-32)",
      }}
    >
      <a
        href={primaryHref}
        className="hero-cta-primary"
        style={{
          display: "inline-flex",
          alignItems: "center",
          justifyContent: "center",
          minHeight: "48px",
          paddingInline: "var(--space-24)",
          borderRadius: "var(--radius-md)",
          background: "var(--color-button-primary-surface-default)",
          color: "var(--color-button-primary-text-default)",
          border: "1px solid var(--color-button-primary-border-default)",
          fontFamily: "var(--font-body)",
          fontSize: "var(--text-md)",
          fontWeight: 500,
          textDecoration: "none",
          transition:
            "background var(--duration-180) var(--ease-standard), border-color var(--duration-180) var(--ease-standard)",
        }}
      >
        {primaryLabel}
      </a>
      <a
        href={secondaryHref}
        className="hero-cta-secondary"
        style={{
          display: "inline-flex",
          alignItems: "center",
          justifyContent: "center",
          minHeight: "48px",
          paddingInline: "var(--space-24)",
          borderRadius: "var(--radius-md)",
          background: "var(--color-button-secondary-surface-default)",
          color: "var(--color-button-secondary-text-default)",
          border: "1px solid var(--color-button-secondary-border-default)",
          fontFamily: "var(--font-body)",
          fontSize: "var(--text-md)",
          fontWeight: 500,
          textDecoration: "none",
          transition:
            "background var(--duration-180) var(--ease-standard), border-color var(--duration-180) var(--ease-standard)",
        }}
      >
        {secondaryLabel}
      </a>
      <style>{`
        .hero-cta-primary:hover { background: var(--color-button-primary-surface-hover); }
        .hero-cta-primary:active { background: var(--color-button-primary-surface-active); }
        .hero-cta-secondary:hover {
          background: var(--color-button-secondary-surface-hover);
          border-color: var(--color-button-secondary-border-hover);
        }
        .hero-cta-secondary:active { background: var(--color-button-secondary-surface-active); }
      `}</style>
    </div>
  );
}
