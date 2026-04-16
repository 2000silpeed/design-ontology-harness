import type { ReactNode } from "react";

type SiteHeaderProps = {
  children: ReactNode;
};

export function SiteHeader({ children }: SiteHeaderProps) {
  return (
    <header
      role="banner"
      style={{
        position: "sticky",
        top: 0,
        zIndex: 50,
        background: "var(--color-surface)",
        borderBottom: "1px solid var(--color-border)",
        backdropFilter: "saturate(1.2) blur(6px)",
        transition:
          "border-color var(--duration-180) var(--ease-standard), background var(--duration-180) var(--ease-standard)",
      }}
    >
      <div
        style={{
          maxWidth: "1120px",
          marginLeft: "auto",
          marginRight: "auto",
          height: "64px",
          paddingLeft: "var(--space-24)",
          paddingRight: "var(--space-24)",
          display: "flex",
          alignItems: "center",
          gap: "var(--space-24)",
        }}
      >
        {children}
      </div>
    </header>
  );
}
