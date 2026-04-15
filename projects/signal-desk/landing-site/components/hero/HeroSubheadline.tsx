import type { ReactNode } from "react";

export function HeroSubheadline({ children }: { children: ReactNode }) {
  return (
    <p
      style={{
        fontFamily: "var(--font-body)",
        fontSize: "var(--text-lg)",
        lineHeight: "var(--leading-relaxed)",
        color: "var(--color-text-muted)",
        maxWidth: "58ch",
        margin: 0,
        marginBottom: "var(--space-32)",
      }}
    >
      {children}
    </p>
  );
}
