import type { ReactNode } from "react";

export function HeroContainer({ children }: { children: ReactNode }) {
  return (
    <section
      aria-labelledby="hero-headline"
      style={{
        background: "var(--color-canvas)",
        paddingTop: "var(--space-96)",
        paddingBottom: "var(--space-64)",
        paddingLeft: "var(--space-24)",
        paddingRight: "var(--space-24)",
      }}
    >
      <div
        style={{
          maxWidth: "1200px",
          margin: "0 auto",
          display: "grid",
          gridTemplateColumns: "repeat(12, minmax(0, 1fr))",
          columnGap: "var(--space-32)",
          rowGap: "var(--space-48)",
          alignItems: "center",
        }}
        className="hero-grid"
      >
        <div style={{ gridColumn: "1 / -1" }} className="hero-text-col">
          {Array.isArray(children) ? children[0] : children}
        </div>
        {Array.isArray(children) && children[1] ? (
          <div style={{ gridColumn: "1 / -1" }} className="hero-visual-col">
            {children[1]}
          </div>
        ) : null}
      </div>
      <style>{`
        @media (min-width: 768px) {
          .hero-text-col { grid-column: 1 / span 7 !important; }
          .hero-visual-col { grid-column: 8 / span 5 !important; }
        }
      `}</style>
    </section>
  );
}
