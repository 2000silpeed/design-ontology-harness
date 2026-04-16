export function SiteLogo() {
  return (
    <a
      href="/"
      aria-label="Checkpoint 홈"
      style={{
        display: "inline-flex",
        alignItems: "center",
        gap: "var(--space-8)",
        textDecoration: "none",
        color: "var(--color-text)",
        fontFamily: "var(--font-heading)",
        fontSize: "var(--text-lg)",
        fontWeight: 700,
        letterSpacing: "-0.01em",
      }}
      >
      <svg
        width="24"
        height="24"
        viewBox="0 0 24 24"
        fill="none"
        aria-hidden="true"
        focusable="false"
      >
        <rect
          x="2"
          y="2"
          width="20"
          height="20"
          rx="6"
          fill="color-mix(in srgb, var(--color-brand-accent) 18%, var(--color-surface))"
          stroke="var(--color-border)"
        />
        <path
          d="M16.75 7.5H10.5C8.57 7.5 7 9.07 7 11s1.57 3.5 3.5 3.5h6.25"
          stroke="var(--color-brand-accent)"
          strokeWidth="2.2"
          strokeLinecap="round"
          strokeLinejoin="round"
        />
        <circle cx="17.25" cy="12" r="1.75" fill="var(--color-surface-tint)" />
      </svg>
      <span>Checkpoint</span>
    </a>
  );
}
