const links = [
  { label: "Features", href: "#features" },
  { label: "Pricing", href: "#pricing" },
  { label: "Journal", href: "#journal" },
  { label: "Changelog", href: "#changelog" },
];

export function SiteNav() {
  return (
    <>
      <nav
        aria-label="Primary"
        className="site-nav"
        style={{
          display: "none",
          alignItems: "center",
          gap: "var(--space-32)",
        }}
      >
        {links.map((l) => (
          <a
            key={l.href}
            href={l.href}
            className="site-nav-link"
            style={{
              position: "relative",
              fontFamily: "var(--font-body)",
              fontSize: "var(--text-sm)",
              color: "var(--color-nav-link-text-default)",
              textDecoration: "none",
              padding: "var(--space-8) 0",
              transition: "color var(--duration-180) var(--ease-standard)",
            }}
          >
            {l.label}
          </a>
        ))}
      </nav>
      <style>{`
        @media (min-width: 768px) {
          .site-nav { display: flex !important; }
        }
        .site-nav-link::after {
          content: "";
          position: absolute;
          left: 0;
          right: 0;
          bottom: 2px;
          height: 1px;
          background: var(--color-nav-link-indicator);
          transform: scaleX(0);
          transform-origin: left;
          transition: transform var(--duration-180) var(--ease-standard);
        }
        .site-nav-link:hover { color: var(--color-nav-link-text-hover); }
        .site-nav-link:hover::after { transform: scaleX(1); }
      `}</style>
    </>
  );
}
