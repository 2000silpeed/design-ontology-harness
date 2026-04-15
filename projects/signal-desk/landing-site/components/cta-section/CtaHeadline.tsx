import type { ReactNode } from "react";

type Props = { children: ReactNode };

export function CtaHeadline({ children }: Props): ReactNode {
  return (
    <h2
      id="cta-heading"
      style={{
        fontFamily: "var(--font-heading)",
        fontSize: "var(--text-3xl)",
        lineHeight: "var(--leading-tight)",
        color: "var(--color-text-inverse)",
        margin: 0,
        fontWeight: 500,
        textAlign: "center",
      }}
    >
      {children}
    </h2>
  );
}
