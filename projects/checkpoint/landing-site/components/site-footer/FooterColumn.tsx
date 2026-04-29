import type { ReactNode } from "react";

type FooterColumnProps = {
  title: string;
  children: ReactNode;
};

export function FooterColumn({ title, children }: FooterColumnProps) {
  return (
    <div
      style={{
        display: "flex",
        flexDirection: "column",
        gap: "var(--space-16)",
      }}
    >
      <h2
        style={{
          margin: 0,
          fontFamily: "var(--font-heading)",
          fontSize: "var(--text-sm)",
          fontWeight: 700,
          color: "var(--color-text)",
          textTransform: "uppercase",
          letterSpacing: "0em",
        }}
      >
        {title}
      </h2>
      <ul
        style={{
          listStyle: "none",
          margin: 0,
          padding: 0,
          display: "flex",
          flexDirection: "column",
          gap: "var(--space-12)",
        }}
      >
        {children}
      </ul>
    </div>
  );
}
