export function SiteNavCta() {
  return (
    <div
      className="hidden md:flex"
      style={{
        alignItems: "center",
        gap: "var(--space-12)",
      }}
    >
      <a
        href="#login"
        style={{
          display: "inline-flex",
          alignItems: "center",
          justifyContent: "center",
          minHeight: "44px",
          paddingLeft: "var(--space-12)",
          paddingRight: "var(--space-12)",
          color: "var(--color-text)",
          background: "transparent",
          border: "1px solid transparent",
          borderRadius: "var(--radius-md)",
          fontFamily: "var(--font-body)",
          fontSize: "var(--text-md)",
          fontWeight: 600,
          textDecoration: "none",
          transition:
            "color var(--duration-120) var(--ease-standard), background var(--duration-120) var(--ease-standard)",
        }}
        className="site-nav-cta-ghost"
      >
        로그인
      </a>
      <a
        href="#signup"
        style={{
          display: "inline-flex",
          alignItems: "center",
          justifyContent: "center",
          minHeight: "44px",
          paddingLeft: "var(--space-24)",
          paddingRight: "var(--space-24)",
          background: "var(--color-brand-primary)",
          color: "var(--color-text-inverse)",
          borderRadius: "var(--radius-md)",
          fontFamily: "var(--font-body)",
          fontSize: "var(--text-md)",
          fontWeight: 600,
          textDecoration: "none",
          border: "1px solid var(--color-brand-primary)",
          transition:
            "background var(--duration-120) var(--ease-standard), border-color var(--duration-120) var(--ease-standard)",
        }}
        className="site-nav-cta-filled"
      >
        시작하기
      </a>
      <style>{`
        .site-nav-cta-ghost:hover {
          color: var(--color-link-hover);
          background: var(--color-surface-muted);
        }
        .site-nav-cta-filled:hover {
          background: var(--color-link-hover);
          border-color: var(--color-link-hover);
        }
      `}</style>
    </div>
  );
}
