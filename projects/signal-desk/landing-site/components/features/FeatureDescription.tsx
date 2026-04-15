import type { ReactNode } from "react";

export function FeatureDescription({ children }: { children: ReactNode }) {
  return (
    <p
      style={{
        margin: 0,
        fontFamily: "var(--font-body)",
        fontSize: "var(--text-sm)",
        color: "var(--color-text-muted)",
        lineHeight: "var(--leading-comfortable)",
      }}
    >
      {children}
    </p>
  );
}
