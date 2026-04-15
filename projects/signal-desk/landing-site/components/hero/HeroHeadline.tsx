import type { ReactNode } from "react";

export function HeroHeadline({ children }: { children: ReactNode }) {
  return (
    <>
      <h1
        id="hero-headline"
        className="hero-headline"
        style={{
          fontFamily: "var(--font-heading)",
          fontWeight: 500,
          lineHeight: "var(--leading-tight)",
          color: "var(--color-text)",
          margin: 0,
          marginBottom: "var(--space-24)",
          fontSize: "var(--text-3xl)",
          letterSpacing: "-0.01em",
        }}
      >
        {children}
      </h1>
      <style>{`
        @media (min-width: 768px) {
          .hero-headline { font-size: var(--text-5xl) !important; }
        }
      `}</style>
    </>
  );
}
