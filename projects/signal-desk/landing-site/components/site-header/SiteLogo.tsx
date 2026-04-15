export function SiteLogo() {
  return (
    <a
      href="/"
      aria-label="Signal Desk home"
      style={{
        display: "inline-flex",
        alignItems: "center",
        gap: "var(--space-8)",
        textDecoration: "none",
        color: "var(--color-text)",
      }}
    >
      <svg
        width="20"
        height="24"
        viewBox="0 0 20 24"
        fill="none"
        aria-hidden="true"
      >
        <line
          x1="6"
          y1="4"
          x2="6"
          y2="22"
          stroke="var(--color-brand-primary)"
          strokeWidth="2"
          strokeLinecap="round"
        />
        <path
          d="M6 4 Q12 4 14 8"
          stroke="var(--color-brand-primary)"
          strokeWidth="2"
          strokeLinecap="round"
          fill="none"
        />
        <circle cx="14" cy="8" r="2" fill="var(--color-brand-accent)" />
      </svg>
      <span
        style={{
          fontFamily: "var(--font-heading)",
          fontSize: "var(--text-lg)",
          fontWeight: 500,
          color: "var(--color-text)",
          letterSpacing: "-0.005em",
        }}
      >
        Signal Desk
      </span>
    </a>
  );
}
