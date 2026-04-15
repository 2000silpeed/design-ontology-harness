import type { ReactNode } from "react";

export function SiteFooter({ children }: { children: ReactNode }) {
  return (
    <footer
      role="contentinfo"
      style={{
        background: "var(--color-surface-muted)",
        borderTop: "1px solid var(--color-border)",
        padding: "var(--space-64) var(--space-24) var(--space-32)",
      }}
    >
      <div
        className="site-footer-inner"
        style={{
          maxWidth: "1200px",
          margin: "0 auto",
          display: "grid",
          gridTemplateColumns: "1fr",
          columnGap: "var(--space-32)",
          rowGap: "var(--space-48)",
        }}
      >
        {children}
      </div>
      <style>{`
        @media (min-width: 768px) {
          .site-footer-inner {
            grid-template-columns: repeat(4, minmax(0, 1fr)) !important;
          }
        }
      `}</style>
    </footer>
  );
}
