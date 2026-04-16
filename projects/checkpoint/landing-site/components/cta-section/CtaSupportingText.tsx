import type { ReactNode } from "react";

export type CtaSupportingTextProps = {
  children: ReactNode;
};

export function CtaSupportingText({ children }: CtaSupportingTextProps) {
  return (
    <p
      style={{
        margin: 0,
        maxWidth: "640px",
        fontFamily: "var(--font-body)",
        fontSize: "var(--text-lg)",
        lineHeight: "var(--leading-relaxed)",
        color: "var(--color-surface-tint)",
      }}
    >
      {children}
    </p>
  );
}
