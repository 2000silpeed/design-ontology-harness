import type { ReactNode } from "react";

export type FaqQuestionProps = {
  children: ReactNode;
};

export function FaqQuestion({ children }: FaqQuestionProps) {
  return (
    <span
      style={{
        flex: "1 1 auto",
        fontFamily: "var(--font-heading)",
        fontSize: "var(--text-lg)",
        lineHeight: "var(--leading-normal)",
        fontWeight: 600,
        color: "var(--color-text)",
      }}
    >
      {children}
    </span>
  );
}
