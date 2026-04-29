import type { ReactNode } from "react";

type FeatureTitleProps = {
  children: ReactNode;
};

export function FeatureTitle({ children }: FeatureTitleProps) {
  return (
    <h3
      style={{
        margin: 0,
        fontFamily: "var(--font-heading)",
        fontSize: "var(--text-lg)",
        lineHeight: "var(--leading-tight)",
        color: "var(--color-text)",
        fontWeight: 600,
        letterSpacing: "0em",
      }}
    >
      {children}
    </h3>
  );
}
