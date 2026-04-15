import type { ReactNode } from "react";

export function HeroEyebrow({ children }: { children: ReactNode }) {
  return (
    <p
      style={{
        fontFamily: "var(--font-mono)",
        fontSize: "var(--text-xs)",
        color: "var(--color-text-subtle)",
        textTransform: "uppercase",
        letterSpacing: "0.12em",
        margin: 0,
        marginBottom: "var(--space-16)",
      }}
    >
      {children}
    </p>
  );
}
