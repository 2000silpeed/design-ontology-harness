export function SiteNavCta() {
  return (
    <>
      <div
        className="site-nav-cta"
        style={{
          display: "none",
          alignItems: "center",
          gap: "var(--space-12)",
        }}
      >
        <a
          href="#login"
          className="nav-ghost"
          style={{
            display: "inline-flex",
            alignItems: "center",
            minHeight: "44px",
            paddingInline: "var(--space-16)",
            borderRadius: "var(--radius-md)",
            background: "var(--color-button-ghost-surface-default)",
            color: "var(--color-button-ghost-text-default)",
            fontFamily: "var(--font-body)",
            fontSize: "var(--text-sm)",
            fontWeight: 500,
            textDecoration: "none",
            transition:
              "background var(--duration-180) var(--ease-standard), color var(--duration-180) var(--ease-standard)",
          }}
        >
          로그인
        </a>
        <a
          href="#signup"
          className="nav-primary"
          style={{
            display: "inline-flex",
            alignItems: "center",
            minHeight: "44px",
            paddingInline: "var(--space-16)",
            borderRadius: "var(--radius-md)",
            background: "var(--color-button-primary-surface-default)",
            color: "var(--color-button-primary-text-default)",
            border: "1px solid var(--color-button-primary-border-default)",
            fontFamily: "var(--font-body)",
            fontSize: "var(--text-sm)",
            fontWeight: 500,
            textDecoration: "none",
            transition: "background var(--duration-180) var(--ease-standard)",
          }}
        >
          무료로 시작
        </a>
      </div>
      <style>{`
        @media (min-width: 768px) {
          .site-nav-cta { display: flex !important; }
        }
        .nav-ghost:hover {
          background: var(--color-button-ghost-surface-hover);
          color: var(--color-button-ghost-text-hover);
        }
        .nav-primary:hover { background: var(--color-button-primary-surface-hover); }
        .nav-primary:active { background: var(--color-button-primary-surface-active); }
      `}</style>
    </>
  );
}
