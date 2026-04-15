export function FooterLegal() {
  return (
    <div
      style={{
        gridColumn: "1 / -1",
        borderTop: "1px solid var(--color-border)",
        marginTop: "var(--space-32)",
        paddingTop: "var(--space-24)",
        display: "flex",
        flexWrap: "wrap",
        alignItems: "center",
        justifyContent: "space-between",
        gap: "var(--space-16)",
        fontFamily: "var(--font-mono)",
        fontSize: "var(--text-xs)",
        color: "var(--color-text-subtle)",
      }}
    >
      <p style={{ margin: 0 }}>
        © 2026 Signal Desk, Inc. · 독립 창작자를 위한 에디토리얼 업무 앱
      </p>
      <ul
        style={{
          listStyle: "none",
          padding: 0,
          margin: 0,
          display: "flex",
          gap: "var(--space-16)",
        }}
      >
        {[
          { label: "Privacy", href: "#privacy" },
          { label: "Terms", href: "#terms" },
          { label: "Imprint", href: "#imprint" },
        ].map((l) => (
          <li key={l.href}>
            <a
              href={l.href}
              style={{
                color: "var(--color-text-subtle)",
                textDecoration: "none",
                transition: "color var(--duration-180) var(--ease-standard)",
              }}
              className="footer-legal-link"
            >
              {l.label}
            </a>
          </li>
        ))}
      </ul>
      <style>{`
        .footer-legal-link:hover { color: var(--color-text); }
      `}</style>
    </div>
  );
}
