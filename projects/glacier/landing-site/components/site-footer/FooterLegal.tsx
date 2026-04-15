const LEGAL_LINKS = [
  { label: "Privacy", href: "#privacy" },
  { label: "Terms", href: "#terms" },
  { label: "Security", href: "#security" },
];

export function FooterLegal() {
  return (
    <div
      style={{
        gridColumn: "1 / -1",
        borderTop: "1px solid var(--color-border)",
        paddingTop: "var(--space-24)",
        marginTop: "var(--space-16)",
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
      <span>© 2026 Glacier, Inc.</span>
      <ul
        style={{
          display: "flex",
          flexWrap: "wrap",
          gap: "var(--space-16)",
          listStyle: "none",
          margin: 0,
          padding: 0,
        }}
      >
        {LEGAL_LINKS.map((item) => (
          <li key={item.href}>
            <a
              href={item.href}
              style={{
                color: "var(--color-text-subtle)",
                textDecoration: "none",
                transition:
                  "color var(--duration-120) var(--ease-standard)",
              }}
              className="footer-legal-link"
            >
              {item.label}
            </a>
          </li>
        ))}
      </ul>
      <style>{`
        .footer-legal-link:hover {
          color: var(--color-text);
        }
      `}</style>
    </div>
  );
}
