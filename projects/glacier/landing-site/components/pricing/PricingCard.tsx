import type { ReactNode } from "react";

export type PricingCardProps = {
  planName: string;
  price: string;
  priceSuffix?: string;
  features: string[];
  ctaLabel: string;
  ctaHref?: string;
  featured?: boolean;
  footnote?: ReactNode;
};

export function PricingCard({
  planName,
  price,
  priceSuffix,
  features,
  ctaLabel,
  ctaHref = "#get-started",
  featured = false,
  footnote,
}: PricingCardProps) {
  return (
    <article
      aria-label={`${planName} 요금제`}
      style={{
        position: "relative",
        display: "flex",
        flexDirection: "column",
        gap: "var(--space-24)",
        background: "var(--color-surface)",
        border: featured
          ? "2px solid var(--color-brand-primary)"
          : "1px solid var(--color-border)",
        borderRadius: "var(--radius-xl)",
        paddingTop: "var(--space-32)",
        paddingBottom: "var(--space-32)",
        paddingLeft: "var(--space-24)",
        paddingRight: "var(--space-24)",
        transitionProperty: "border-color, transform, box-shadow",
        transitionDuration: "var(--duration-180)",
        transitionTimingFunction: "var(--ease-standard)",
      }}
    >
      {featured ? (
        <span
          aria-label="추천 플랜"
          style={{
            position: "absolute",
            top: "calc(-1 * var(--space-12))",
            right: "var(--space-24)",
            display: "inline-flex",
            alignItems: "center",
            gap: "var(--space-4)",
            background: "var(--color-brand-accent)",
            color: "var(--color-text-inverse)",
            paddingTop: "var(--space-4)",
            paddingBottom: "var(--space-4)",
            paddingLeft: "var(--space-12)",
            paddingRight: "var(--space-12)",
            borderRadius: "var(--radius-pill)",
            fontFamily: "var(--font-body)",
            fontSize: "var(--text-xs)",
            fontWeight: 700,
            letterSpacing: "0.04em",
            textTransform: "uppercase",
          }}
        >
          추천
        </span>
      ) : null}
      <header
        style={{
          display: "flex",
          flexDirection: "column",
          gap: "var(--space-8)",
        }}
      >
        <h3
          style={{
            margin: 0,
            fontFamily: "var(--font-heading)",
            fontSize: "var(--text-xl)",
            lineHeight: "var(--leading-tight)",
            fontWeight: 700,
            color: "var(--color-text)",
          }}
        >
          {planName}
        </h3>
        <p
          style={{
            margin: 0,
            display: "flex",
            alignItems: "baseline",
            gap: "var(--space-4)",
            fontFamily: "var(--font-heading)",
            fontSize: "var(--text-3xl)",
            lineHeight: "var(--leading-tight)",
            fontWeight: 700,
            color: "var(--color-text)",
          }}
        >
          <span>{price}</span>
          {priceSuffix ? (
            <span
              style={{
                fontFamily: "var(--font-body)",
                fontSize: "var(--text-sm)",
                fontWeight: 500,
                color: "var(--color-text-muted)",
              }}
            >
              {priceSuffix}
            </span>
          ) : null}
        </p>
      </header>
      <ul
        style={{
          listStyle: "none",
          margin: 0,
          padding: 0,
          display: "flex",
          flexDirection: "column",
          gap: "var(--space-12)",
          flexGrow: 1,
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
            <svg
              width="18"
              height="18"
              viewBox="0 0 18 18"
              fill="none"
              aria-hidden="true"
              style={{
                flexShrink: 0,
                marginTop: "2px",
                color: "var(--color-brand-primary)",
              }}
            >
              <path
                d="M3.75 9.5l3.25 3.25L14.25 5.25"
                stroke="currentColor"
                strokeWidth="1.75"
                strokeLinecap="round"
                strokeLinejoin="round"
              />
            </svg>
            <span>{feature}</span>
          </li>
        ))}
      </ul>
      <a
        href={ctaHref}
        className={featured ? "pricing-cta-primary" : "pricing-cta-secondary"}
        style={{
          display: "inline-flex",
          alignItems: "center",
          justifyContent: "center",
          gap: "var(--space-8)",
          minHeight: "44px",
          paddingTop: "var(--space-12)",
          paddingBottom: "var(--space-12)",
          paddingLeft: "var(--space-24)",
          paddingRight: "var(--space-24)",
          background: featured
            ? "var(--color-brand-primary)"
            : "var(--color-surface)",
          color: featured
            ? "var(--color-text-inverse)"
            : "var(--color-text)",
          border: featured
            ? "1px solid var(--color-brand-primary)"
            : "1px solid var(--color-border-strong)",
          borderRadius: "var(--radius-md)",
          fontFamily: "var(--font-body)",
          fontSize: "var(--text-md)",
          fontWeight: 600,
          textDecoration: "none",
          transitionProperty: "background-color, border-color, transform",
          transitionDuration: "var(--duration-180)",
          transitionTimingFunction: "var(--ease-standard)",
        }}
      >
        {ctaLabel}
      </a>
      {footnote ? (
        <p
          style={{
            margin: 0,
            fontFamily: "var(--font-body)",
            fontSize: "var(--text-xs)",
            color: "var(--color-text-subtle)",
            textAlign: "center",
          }}
        >
          {footnote}
        </p>
      ) : null}
      <style>{`
        .pricing-cta-primary:hover {
          background: var(--color-link-hover);
          border-color: var(--color-link-hover);
        }
        .pricing-cta-primary:active {
          transform: translateY(1px);
        }
        .pricing-cta-secondary:hover {
          background: var(--color-surface-muted);
          border-color: var(--color-brand-primary);
        }
        .pricing-cta-secondary:active {
          transform: translateY(1px);
        }
      `}</style>
    </article>
  );
}
