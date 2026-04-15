export function SiteLogo() {
  return (
    <a
      href="/"
      aria-label="Glacier 홈"
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
        width="22"
        height="22"
        viewBox="0 0 22 22"
        fill="none"
        aria-hidden="true"
        focusable="false"
      >
        <rect
          x="2"
          y="4"
          width="18"
          height="4"
          rx="1"
          fill="var(--color-brand-primary)"
        />
        <rect
          x="4"
          y="10"
          width="14"
          height="4"
          rx="1"
          fill="var(--color-brand-primary)"
          opacity="0.7"
        />
        <rect
          x="6"
          y="16"
          width="10"
          height="3"
          rx="1"
          fill="var(--color-brand-primary)"
          opacity="0.4"
        />
      </svg>
      <span>Glacier</span>
    </a>
  );
}
