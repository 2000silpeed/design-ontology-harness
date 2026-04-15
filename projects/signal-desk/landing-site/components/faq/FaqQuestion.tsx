import type { ReactNode } from "react";

type Props = {
  children: ReactNode;
};

function Chevron() {
  return (
    <svg
      aria-hidden="true"
      className="faq-chevron"
      width="20"
      height="20"
      viewBox="0 0 20 20"
      fill="none"
      style={{
        flexShrink: 0,
        color: "var(--color-text-muted)",
        transition: "transform var(--duration-180) var(--ease-standard)",
      }}
    >
      <path
        d="M5 7.5L10 12.5L15 7.5"
        stroke="currentColor"
        strokeWidth="1.75"
        strokeLinecap="round"
        strokeLinejoin="round"
      />
    </svg>
  );
}

export function FaqQuestion({ children }: Props): ReactNode {
  return (
    <summary
      className="faq-question"
      style={{
        display: "flex",
        alignItems: "center",
        justifyContent: "space-between",
        gap: "var(--space-24)",
        cursor: "pointer",
        listStyle: "none",
        paddingTop: "var(--space-16)",
        paddingBottom: "var(--space-16)",
        paddingLeft: "var(--space-16)",
        paddingRight: "var(--space-16)",
        fontFamily: "var(--font-heading)",
        fontSize: "var(--text-lg)",
        lineHeight: "var(--leading-comfortable)",
        fontWeight: 500,
        color: "var(--color-text)",
        borderRadius: "var(--radius-md)",
        transition: "background var(--duration-180) var(--ease-standard)",
      }}
    >
      <span>{children}</span>
      <Chevron />
    </summary>
  );
}
