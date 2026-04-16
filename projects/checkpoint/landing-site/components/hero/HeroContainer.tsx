import type { ReactNode } from "react";

type HeroContainerProps = {
  children: ReactNode;
};

export function HeroContainer({ children }: HeroContainerProps) {
  return (
    <section
      aria-labelledby="hero-headline"
      style={{
        position: "relative",
        background: "var(--color-canvas)",
        paddingTop: "var(--space-96)",
        paddingBottom: "var(--space-96)",
        paddingLeft: "var(--space-24)",
        paddingRight: "var(--space-24)",
        overflow: "hidden",
      }}
    >
      <div
        style={{
          maxWidth: "1120px",
          marginLeft: "auto",
          marginRight: "auto",
          display: "grid",
          gridTemplateColumns: "minmax(0, 1fr)",
          gap: "var(--space-64)",
          alignItems: "center",
        }}
        className="hero-grid"
      >
        {children}
      </div>
      <style>{`
        @media (min-width: 960px) {
          .hero-grid {
            grid-template-columns: minmax(0, 1.1fr) minmax(0, 0.9fr) !important;
          }
        }
      `}</style>
    </section>
  );
}
