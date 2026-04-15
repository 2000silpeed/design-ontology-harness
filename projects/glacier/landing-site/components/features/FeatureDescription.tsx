import type { ReactNode } from "react";

type FeatureDescriptionProps = {
  children: ReactNode;
};

export function FeatureDescription({ children }: FeatureDescriptionProps) {
  return (
    <p
      style={{
        margin: 0,
        fontFamily: "var(--font-body)",
        fontSize: "var(--text-sm)",
        lineHeight: "var(--leading-comfortable)",
        color: "var(--color-text-muted)",
      }}
    >
      {children}
    </p>
  );
}
