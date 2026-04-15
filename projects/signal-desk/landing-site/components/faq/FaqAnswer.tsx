import type { ReactNode } from "react";

type Props = {
  children: ReactNode;
};

export function FaqAnswer({ children }: Props): ReactNode {
  return (
    <div
      style={{
        paddingLeft: "var(--space-16)",
        paddingRight: "var(--space-16)",
        paddingBottom: "var(--space-16)",
        fontFamily: "var(--font-body)",
        fontSize: "var(--text-md)",
        lineHeight: "var(--leading-relaxed)",
        color: "var(--color-text-muted)",
      }}
    >
      {children}
    </div>
  );
}
