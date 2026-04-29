type HeroTrustStripProps = {
  items: string[];
};

export function HeroTrustStrip({ items }: HeroTrustStripProps) {
  return (
    <div
      style={{
        marginTop: "var(--space-48)",
        paddingTop: "var(--space-24)",
        borderTop: "1px solid var(--color-border)",
      }}
    >
      <p
        style={{
          margin: 0,
          marginBottom: "var(--space-12)",
          fontFamily: "var(--font-mono)",
          fontSize: "var(--text-xs)",
          letterSpacing: "0em",
          textTransform: "uppercase",
          color: "var(--color-text-subtle)",
        }}
      >
        Trusted by platform teams
      </p>
      <ul
        role="list"
        style={{
          listStyle: "none",
          margin: 0,
          padding: 0,
          display: "flex",
          flexWrap: "wrap",
          gap: "var(--space-24)",
          alignItems: "center",
        }}
      >
        {items.map((item, idx) => (
          <li
            key={idx}
            style={{
              display: "inline-flex",
              alignItems: "center",
              gap: "var(--space-8)",
              fontFamily: "var(--font-body)",
              fontSize: "var(--text-sm)",
              color: "var(--color-text-muted)",
              fontWeight: 500,
            }}
          >
            <svg
              width="14"
              height="14"
              viewBox="0 0 16 16"
              fill="none"
              aria-hidden="true"
            >
              <path
                d="M8 1.5l5.5 2.25v4c0 3.5-2.3 6.4-5.5 7.25-3.2-.85-5.5-3.75-5.5-7.25v-4L8 1.5z"
                stroke="var(--color-brand-primary)"
                strokeWidth="1.5"
                strokeLinejoin="round"
                fill="var(--color-surface-tint)"
              />
              <path
                d="M5.75 8.25l1.75 1.75L10.5 6.5"
                stroke="var(--color-brand-primary)"
                strokeWidth="1.75"
                strokeLinecap="round"
                strokeLinejoin="round"
              />
            </svg>
            <span>{item}</span>
          </li>
        ))}
      </ul>
    </div>
  );
}
