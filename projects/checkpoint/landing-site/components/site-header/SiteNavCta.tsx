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
        href="#newsletter"
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
        다이제스트
      </a>
      <a
        href="#newsletter"
        style={{
          display: "inline-flex",
          alignItems: "center",
          justifyContent: "center",
          minHeight: "44px",
          paddingLeft: "var(--space-24)",
          paddingRight: "var(--space-24)",
          background: "var(--color-brand-accent)",
          color: "var(--color-text-inverse)",
          borderRadius: "var(--radius-md)",
          fontFamily: "var(--font-body)",
          fontSize: "var(--text-md)",
          fontWeight: 600,
          textDecoration: "none",
          border: "1px solid var(--color-brand-accent)",
          transition:
            "background var(--duration-120) var(--ease-standard), border-color var(--duration-120) var(--ease-standard)",
        }}
        className="site-nav-cta-filled"
      >
        금요일 요약 받기
      </a>
      <style>{`
        .site-nav-cta-ghost:hover {
          color: var(--color-text);
          background: color-mix(in srgb, var(--color-brand-accent) 12%, transparent);
        }
        .site-nav-cta-filled:hover {
          background: #c4ff88;
          border-color: #c4ff88;
        }
      `}</style>
    </div>
  );
}
