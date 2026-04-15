import type { ReactNode } from "react";

type Props = {
  name: string;
  price: string;
  priceNote: string;
  features: string[];
  ctaLabel: string;
  ctaHref?: string;
  featured?: boolean;
};

function CheckIcon() {
  return (
    <svg
      aria-hidden="true"
      width="18"
      height="18"
      viewBox="0 0 20 20"
      fill="none"
      style={{
        flexShrink: 0,
        marginTop: "6px",
        color: "var(--color-brand-primary)",
      }}
    >
      <path
        d="M4 10.5L8 14.5L16 6"
        stroke="currentColor"
        strokeWidth="2"
        strokeLinecap="round"
        strokeLinejoin="round"
      />
    </svg>
  );
}

export function PricingCard({
  name,
  price,
  priceNote,
  features,
  ctaLabel,
  ctaHref = "#get-started",
  featured = false,
}: Props): ReactNode {
  const cardClass = featured ? "pricing-card pricing-card--featured" : "pricing-card";
  const buttonClass = featured ? "pricing-card-cta pricing-card-cta--primary" : "pricing-card-cta pricing-card-cta--secondary";

  return (
    <article
      className={cardClass}
      aria-label={`${name} plan`}
      style={{
        position: "relative",
        display: "flex",
        flexDirection: "column",
        gap: "var(--space-32)",
        background: "var(--color-card-surface-default)",
        border: featured
          ? "2px solid var(--color-brand-primary)"
          : "1px solid var(--color-card-border-default)",
        borderRadius: "var(--radius-xl)",
        paddingTop: "var(--space-48)",
        paddingBottom: "var(--space-48)",
        paddingLeft: "var(--space-32)",
        paddingRight: "var(--space-32)",
        transition:
          "border-color var(--duration-180) var(--ease-standard)",
      }}
    >
      {featured ? (
        <span
          aria-label="추천 플랜"
          style={{
            position: "absolute",
            top: "var(--space-16)",
            right: "var(--space-16)",
            background: "var(--color-brand-accent)",
            color: "var(--color-ink)",
            fontFamily: "var(--font-mono)",
            fontSize: "var(--text-xs)",
            letterSpacing: "0.08em",
            textTransform: "uppercase",
            paddingInline: "var(--space-12)",
            paddingBlock: "var(--space-4)",
            borderRadius: "var(--radius-pill)",
          }}
        >
          추천
        </span>
      ) : null}

      <header style={{ display: "flex", flexDirection: "column", gap: "var(--space-16)" }}>
        <h3
          style={{
            fontFamily: "var(--font-heading)",
            fontSize: "var(--text-2xl)",
            lineHeight: "var(--leading-tight)",
            color: "var(--color-text)",
            margin: 0,
            fontWeight: 500,
          }}
        >
          {name}
        </h3>
        <div style={{ display: "flex", flexDirection: "column", gap: "var(--space-4)" }}>
          <span
            style={{
              fontFamily: "var(--font-heading)",
              fontSize: "var(--text-3xl)",
              lineHeight: "var(--leading-tight)",
              color: "var(--color-text)",
              fontWeight: 500,
              fontVariantNumeric: "tabular-nums",
            }}
          >
            {price}
          </span>
          <span
            style={{
              fontFamily: "var(--font-mono)",
              fontSize: "var(--text-xs)",
              color: "var(--color-text-muted)",
              letterSpacing: "0.04em",
            }}
          >
            {priceNote}
          </span>
        </div>
      </header>

      <ul
        style={{
          listStyle: "none",
          padding: 0,
          margin: 0,
          display: "flex",
          flexDirection: "column",
          gap: "var(--space-12)",
        }}
      >
        {features.map((feature) => (
          <li
            key={feature}
            style={{
              display: "flex",
              alignItems: "flex-start",
              gap: "var(--space-12)",
              fontFamily: "var(--font-body)",
              fontSize: "var(--text-md)",
              lineHeight: "var(--leading-comfortable)",
              color: "var(--color-text)",
            }}
          >
            <CheckIcon />
            <span>{feature}</span>
          </li>
        ))}
      </ul>

      <a
        href={ctaHref}
        className={buttonClass}
        style={{
          display: "inline-flex",
          alignItems: "center",
          justifyContent: "center",
          minHeight: "48px",
          paddingInline: "var(--space-24)",
          borderRadius: "var(--radius-md)",
          fontFamily: "var(--font-body)",
          fontSize: "var(--text-md)",
          fontWeight: 500,
          textDecoration: "none",
          marginTop: "auto",
          transition:
            "background var(--duration-180) var(--ease-standard), border-color var(--duration-180) var(--ease-standard)",
        }}
      >
        {ctaLabel}
      </a>

      <style>{`
        .pricing-card-cta--primary {
          background: var(--color-button-primary-surface-default);
          color: var(--color-button-primary-text-default);
          border: 1px solid var(--color-button-primary-border-default);
        }
        .pricing-card-cta--primary:hover { background: var(--color-button-primary-surface-hover); }
        .pricing-card-cta--primary:active { background: var(--color-button-primary-surface-active); }
        .pricing-card-cta--secondary {
          background: var(--color-button-secondary-surface-default);
          color: var(--color-button-secondary-text-default);
          border: 1px solid var(--color-button-secondary-border-default);
        }
        .pricing-card-cta--secondary:hover {
          background: var(--color-button-secondary-surface-hover);
          border-color: var(--color-button-secondary-border-hover);
        }
        .pricing-card-cta--secondary:active { background: var(--color-button-secondary-surface-active); }
      `}</style>
    </article>
  );
}
