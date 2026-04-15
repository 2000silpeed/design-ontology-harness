import type { ReactNode } from "react";

export function TestimonialQuote({ children }: { children: ReactNode }) {
  return (
    <blockquote
      className="sd-testimonial-quote"
      style={{
        margin: 0,
        position: "relative",
        paddingTop: "var(--space-24)",
        fontFamily: "var(--font-heading)",
        fontSize: "var(--text-lg)",
        lineHeight: "var(--leading-relaxed)",
        color: "var(--color-text)",
        fontWeight: 400,
      }}
    >
      {children}
      <style>{`
        .sd-testimonial-quote::before {
          content: "\\201C";
          position: absolute;
          top: -8px;
          left: -4px;
          font-family: var(--font-heading);
          font-size: var(--text-3xl);
          line-height: 1;
          color: var(--color-brand-primary);
          font-weight: 500;
        }
      `}</style>
    </blockquote>
  );
}
