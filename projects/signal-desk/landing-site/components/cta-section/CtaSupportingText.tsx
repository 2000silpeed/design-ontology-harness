import type { ReactNode } from "react";

type Props = { children: ReactNode };

export function CtaSupportingText({ children }: Props): ReactNode {
  return (
    <p
      style={{
        fontFamily: "var(--font-body)",
        fontSize: "var(--text-lg)",
        lineHeight: "var(--leading-relaxed)",
        color: "var(--color-text-inverse)",
        opacity: 0.85,
        margin: 0,
        textAlign: "center",
      }}
    >
      {children}
    </p>
  );
}
