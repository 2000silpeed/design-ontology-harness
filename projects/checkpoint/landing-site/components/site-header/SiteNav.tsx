const NAV_ITEMS = [
  { label: "Reviews", href: "#reviews" },
  { label: "Compare", href: "#compare" },
  { label: "Method", href: "#methodology" },
  { label: "Membership", href: "#membership" },
];

export function SiteNav() {
  return (
    <nav
      aria-label="Primary"
      className="hidden md:block"
      style={{
        flex: 1,
      }}
    >
      <ul
        style={{
          display: "flex",
          alignItems: "center",
          gap: "var(--space-24)",
          listStyle: "none",
          margin: 0,
          padding: 0,
        }}
      >
        {NAV_ITEMS.map((item) => (
          <li key={item.href}>
            <a
              href={item.href}
              style={{
                display: "inline-flex",
                alignItems: "center",
                height: "44px",
                paddingLeft: "var(--space-4)",
                paddingRight: "var(--space-4)",
                color: "var(--color-text-muted)",
                textDecoration: "none",
                fontFamily: "var(--font-body)",
                fontSize: "var(--text-md)",
                fontWeight: 500,
                transition:
                  "color var(--duration-120) var(--ease-standard)",
              }}
              className="site-nav-link"
            >
              {item.label}
            </a>
          </li>
        ))}
      </ul>
      <style>{`
        .site-nav-link:hover {
          color: var(--color-link-hover);
          text-decoration: underline;
          text-underline-offset: 4px;
          text-decoration-thickness: 1px;
        }
      `}</style>
    </nav>
  );
}
