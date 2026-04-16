import type { ReactNode } from "react";

type TestimonialQuoteProps = {
  children: ReactNode;
};

export function TestimonialQuote({ children }: TestimonialQuoteProps) {
  return (
    <blockquote
      style={{
        margin: 0,
        display: "flex",
        flexDirection: "column",
        gap: "var(--space-12)",
        position: "relative",
      }}
    >
      <svg
        width="28"
        height="24"
        viewBox="0 0 28 24"
        fill="none"
        aria-hidden="true"
        style={{ color: "var(--color-surface-tint)" }}
      >
        <path
          d="M6 22c-2.8 0-5-2.3-5-5.2 0-5.6 3.9-11 9.6-13.8l1.8 2.8C8.8 7.8 6.4 10.9 6 13.6c.4-.1.9-.2 1.4-.2 2.8 0 5 2.3 5 5.2S9.2 22 6.4 22H6Zm15.6 0c-2.8 0-5-2.3-5-5.2C16.6 11.2 20.5 5.8 26.2 3l1.8 2.8C24.4 7.8 22 10.9 21.6 13.6c.4-.1.9-.2 1.4-.2 2.8 0 5 2.3 5 5.2S24.8 22 22 22h-.4Z"
          fill="currentColor"
        />
      </svg>
      <p
        style={{
          margin: 0,
          fontFamily: "var(--font-heading)",
          fontSize: "var(--text-lg)",
          lineHeight: "var(--leading-relaxed)",
          color: "var(--color-text)",
          fontWeight: 500,
        }}
      >
        {children}
      </p>
    </blockquote>
  );
}
