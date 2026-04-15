import type { ReactNode } from "react";

export function FeatureTitle({ children }: { children: ReactNode }) {
  return (
    <h3
      style={{
        margin: 0,
        fontFamily: "var(--font-heading)",
        fontSize: "var(--text-lg)",
        fontWeight: 500,
        lineHeight: "var(--leading-tight)",
        color: "var(--color-text)",
        letterSpacing: "-0.005em",
      }}
    >
      {children}
    </h3>
  );
}
