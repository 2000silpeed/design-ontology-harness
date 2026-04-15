import type { ReactNode } from "react";

export type CtaHeadlineProps = {
  id?: string;
  children: ReactNode;
};

export function CtaHeadline({ id = "cta-heading", children }: CtaHeadlineProps) {
  return (
    <h2
      id={id}
      style={{
        margin: 0,
        fontFamily: "var(--font-heading)",
        fontSize: "var(--text-4xl)",
        lineHeight: "var(--leading-tight)",
        fontWeight: 700,
        color: "var(--color-text-inverse)",
        maxWidth: "720px",
      }}
    >
      {children}
    </h2>
  );
}
