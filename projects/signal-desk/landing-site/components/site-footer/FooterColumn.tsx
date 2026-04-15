import type { ReactNode } from "react";

export function FooterColumn({
  title,
  children,
}: {
  title: string;
  children: ReactNode;
}) {
  return (
    <div>
      <h3
        style={{
          fontFamily: "var(--font-heading)",
          fontSize: "var(--text-sm)",
          color: "var(--color-text)",
          textTransform: "uppercase",
          letterSpacing: "0.06em",
          margin: 0,
          marginBottom: "var(--space-16)",
          fontWeight: 500,
        }}
      >
        {title}
      </h3>
      <ul
        style={{
          listStyle: "none",
          padding: 0,
          margin: 0,
          display: "flex",
          flexDirection: "column",
          fontFamily: "var(--font-body)",
        }}
      >
        {children}
      </ul>
    </div>
  );
}
