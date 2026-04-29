type CustomerLogoProps = {
  name: string;
};

export function CustomerLogo({ name }: CustomerLogoProps) {
  return (
    <span
      className="glacier-customer-logo"
      style={{
        display: "inline-flex",
        alignItems: "center",
        gap: "var(--space-8)",
        fontFamily: "var(--font-mono)",
        fontSize: "var(--text-md)",
        color: "var(--color-text-subtle)",
        letterSpacing: "0em",
        filter: "grayscale(1)",
        opacity: 0.85,
        transition:
          "filter var(--duration-180) var(--ease-standard), opacity var(--duration-180) var(--ease-standard), color var(--duration-180) var(--ease-standard)",
      }}
    >
      <svg
        width="10"
        height="10"
        viewBox="0 0 10 10"
        fill="none"
        aria-hidden="true"
      >
        <circle cx="5" cy="5" r="2" fill="currentColor" />
      </svg>
      <span>{name}</span>
      <style>{`
        .glacier-customer-logo:hover {
          filter: grayscale(0.3) !important;
          opacity: 1 !important;
          color: var(--color-text-muted) !important;
        }
      `}</style>
    </span>
  );
}
