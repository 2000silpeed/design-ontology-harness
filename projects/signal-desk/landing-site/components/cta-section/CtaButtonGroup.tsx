import type { ReactNode } from "react";

type Props = {
  primaryLabel: string;
  secondaryLabel: string;
  primaryHref?: string;
  secondaryHref?: string;
};

export function CtaButtonGroup({
  primaryLabel,
  secondaryLabel,
  primaryHref = "#get-started",
  secondaryHref = "#use-cases",
}: Props): ReactNode {
  return (
    <div
      style={{
        display: "flex",
        flexWrap: "wrap",
        justifyContent: "center",
        gap: "var(--space-16)",
      }}
    >
      <a
        href={primaryHref}
        className="cta-btn-primary"
        style={{
          display: "inline-flex",
          alignItems: "center",
          justifyContent: "center",
          minHeight: "48px",
          paddingInline: "var(--space-24)",
          borderRadius: "var(--radius-md)",
          background: "var(--color-surface)",
          color: "var(--color-brand-primary)",
          border: "1px solid transparent",
          fontFamily: "var(--font-body)",
          fontSize: "var(--text-md)",
          fontWeight: 500,
          textDecoration: "none",
          transition:
            "background var(--duration-180) var(--ease-standard), color var(--duration-180) var(--ease-standard)",
        }}
      >
        {primaryLabel}
      </a>
      <a
        href={secondaryHref}
        className="cta-btn-secondary"
        style={{
          display: "inline-flex",
          alignItems: "center",
          justifyContent: "center",
          minHeight: "48px",
          paddingInline: "var(--space-24)",
          borderRadius: "var(--radius-md)",
          background: "transparent",
          color: "var(--color-text-inverse)",
          border: "1px solid var(--color-text-inverse)",
          fontFamily: "var(--font-body)",
          fontSize: "var(--text-md)",
          fontWeight: 500,
          textDecoration: "none",
          transition:
            "background var(--duration-180) var(--ease-standard), color var(--duration-180) var(--ease-standard)",
        }}
      >
        {secondaryLabel}
      </a>
      <style>{`
        .cta-btn-primary:hover { background: var(--color-button-secondary-surface-hover); }
        .cta-btn-secondary:hover {
          background: var(--color-surface-tint);
          color: var(--color-ink);
        }
      `}</style>
    </div>
  );
}
