import type { ReactNode } from "react";

type SiteFooterProps = {
  children: ReactNode;
};

export function SiteFooter({ children }: SiteFooterProps) {
  return (
    <footer
      role="contentinfo"
      style={{
        background: "var(--color-surface-muted)",
        borderTop: "1px solid var(--color-border)",
        color: "var(--color-text-muted)",
        paddingTop: "var(--space-64)",
        paddingBottom: "var(--space-32)",
        paddingLeft: "var(--space-24)",
        paddingRight: "var(--space-24)",
      }}
    >
      <div
        style={{
          maxWidth: "1120px",
          marginLeft: "auto",
          marginRight: "auto",
          display: "grid",
          gridTemplateColumns: "minmax(0, 1fr)",
          gap: "var(--space-48)",
        }}
        className="site-footer-grid"
      >
        {children}
      </div>
      <style>{`
        @media (min-width: 768px) {
          .site-footer-grid {
            grid-template-columns: repeat(4, minmax(0, 1fr)) !important;
          }
        }
      `}</style>
    </footer>
  );
}
