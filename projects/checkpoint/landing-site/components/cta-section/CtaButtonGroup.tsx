export type CtaButtonGroupProps = {
  primaryLabel: string;
  primaryHref?: string;
  secondaryLabel: string;
  secondaryHref?: string;
};

export function CtaButtonGroup({
  primaryLabel,
  primaryHref = "#get-started",
  secondaryLabel,
  secondaryHref = "#docs",
}: CtaButtonGroupProps) {
  return (
    <div
      role="group"
      aria-label="최종 행동 유도"
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
        className="cta-section-primary"
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
          color: "var(--color-brand-primary)",
          borderRadius: "var(--radius-md)",
          fontFamily: "var(--font-body)",
          fontSize: "var(--text-md)",
          fontWeight: 700,
          textDecoration: "none",
          border: "1px solid var(--color-surface)",
          transitionProperty: "background-color, transform, box-shadow",
          transitionDuration: "var(--duration-180)",
          transitionTimingFunction: "var(--ease-standard)",
        }}
      >
        <span>{primaryLabel}</span>
        <svg width="16" height="16" viewBox="0 0 16 16" fill="none" aria-hidden="true">
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
        className="cta-section-secondary"
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
          background: "transparent",
          color: "var(--color-text-inverse)",
          borderRadius: "var(--radius-md)",
          fontFamily: "var(--font-body)",
          fontSize: "var(--text-md)",
          fontWeight: 600,
          textDecoration: "none",
          border: "1px solid var(--color-text-inverse)",
          transitionProperty: "background-color, border-color, transform",
          transitionDuration: "var(--duration-180)",
          transitionTimingFunction: "var(--ease-standard)",
        }}
      >
        <svg width="16" height="16" viewBox="0 0 16 16" fill="none" aria-hidden="true">
          <path
            d="M3 2.5h7l3 3v8a1 1 0 01-1 1H3a1 1 0 01-1-1v-10a1 1 0 011-1z"
            stroke="currentColor"
            strokeWidth="1.5"
            strokeLinejoin="round"
          />
          <path
            d="M5 8.5h6M5 11h4"
            stroke="currentColor"
            strokeWidth="1.5"
            strokeLinecap="round"
          />
        </svg>
        <span>{secondaryLabel}</span>
      </a>
      <style>{`
        .cta-section-primary:hover {
          background: var(--color-surface-muted);
          border-color: var(--color-surface-muted);
        }
        .cta-section-primary:active {
          transform: translateY(1px);
        }
        .cta-section-secondary:hover {
          background: var(--color-surface-tint);
          color: var(--color-brand-primary);
          border-color: var(--color-surface-tint);
        }
        .cta-section-secondary:active {
          transform: translateY(1px);
        }
      `}</style>
    </div>
  );
}
