import type { ReactNode } from "react";

export type FaqAnswerProps = {
  children: ReactNode;
};

export function FaqAnswer({ children }: FaqAnswerProps) {
  return (
    <div
      style={{
        paddingTop: "var(--space-12)",
        paddingBottom: "var(--space-8)",
        paddingRight: "var(--space-32)",
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
