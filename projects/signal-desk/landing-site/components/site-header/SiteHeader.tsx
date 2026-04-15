import type { ReactNode } from "react";

export function SiteHeader({ children }: { children: ReactNode }) {
  return (
    <header
      role="banner"
      style={{
        position: "sticky",
        top: 0,
        zIndex: 40,
        background: "color-mix(in srgb, var(--color-surface-elevated) 90%, transparent)",
        backdropFilter: "blur(10px)",
        WebkitBackdropFilter: "blur(10px)",
        borderBottom: "1px solid var(--color-border)",
      }}
    >
      <div
        style={{
          maxWidth: "1200px",
          margin: "0 auto",
          height: "64px",
          padding: "0 var(--space-24)",
          display: "flex",
          alignItems: "center",
          justifyContent: "space-between",
          gap: "var(--space-24)",
        }}
      >
        {children}
      </div>
    </header>
  );
}
