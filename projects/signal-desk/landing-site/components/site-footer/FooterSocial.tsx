const items = [
  {
    label: "Instagram",
    href: "https://instagram.com",
    path: (
      <>
        <rect x="3" y="3" width="12" height="12" rx="3" stroke="currentColor" strokeWidth="1.4" fill="none" />
        <circle cx="9" cy="9" r="3" stroke="currentColor" strokeWidth="1.4" fill="none" />
        <circle cx="13" cy="5" r="0.8" fill="currentColor" />
      </>
    ),
  },
  {
    label: "Twitter",
    href: "https://twitter.com",
    path: (
      <path
        d="M3 3 L8 10 L3 15 M15 3 L10 10 L15 15"
        stroke="currentColor"
        strokeWidth="1.4"
        strokeLinecap="round"
        fill="none"
      />
    ),
  },
  {
    label: "RSS",
    href: "/rss.xml",
    path: (
      <>
        <path d="M4 4 a11 11 0 0 1 11 11" stroke="currentColor" strokeWidth="1.4" fill="none" strokeLinecap="round" />
        <path d="M4 9 a6 6 0 0 1 6 6" stroke="currentColor" strokeWidth="1.4" fill="none" strokeLinecap="round" />
        <circle cx="5" cy="14" r="1.2" fill="currentColor" />
      </>
    ),
  },
];

export function FooterSocial() {
  return (
    <ul
      style={{
        listStyle: "none",
        padding: 0,
        margin: 0,
        display: "flex",
        alignItems: "center",
        gap: "var(--space-8)",
        gridColumn: "1 / -1",
        marginTop: "var(--space-16)",
      }}
    >
      {items.map((item) => (
        <li key={item.label}>
          <a
            href={item.href}
            target="_blank"
            rel="noopener noreferrer"
            aria-label={item.label}
            className="footer-social-link"
            style={{
              display: "inline-flex",
              alignItems: "center",
              justifyContent: "center",
              width: "40px",
              height: "40px",
              borderRadius: "var(--radius-md)",
              color: "var(--color-text-muted)",
              border: "1px solid var(--color-border)",
              background: "var(--color-surface)",
              transition:
                "color var(--duration-180) var(--ease-standard), border-color var(--duration-180) var(--ease-standard)",
            }}
          >
            <svg width="18" height="18" viewBox="0 0 18 18" fill="none" aria-hidden="true">
              {item.path}
            </svg>
          </a>
        </li>
      ))}
      <style>{`
        .footer-social-link:hover {
          color: var(--color-text);
          border-color: var(--color-border-strong);
        }
      `}</style>
    </ul>
  );
}
