import type { ReactNode } from "react";

export type UpgradeBannerProps = {
  message: ReactNode;
  actionLabel?: string;
  actionHref?: string;
};

export function UpgradeBanner({
  message,
  actionLabel,
  actionHref = "#upgrade",
}: UpgradeBannerProps) {
  return (
    <div
      role="status"
      aria-live="polite"
      style={{
        display: "flex",
        flexWrap: "wrap",
        alignItems: "center",
        gap: "var(--space-16)",
        background: "var(--color-surface-tint)",
        color: "var(--color-brand-primary)",
        borderRadius: "var(--radius-lg)",
        paddingTop: "var(--space-12)",
        paddingBottom: "var(--space-12)",
        paddingLeft: "var(--space-24)",
        paddingRight: "var(--space-24)",
        border: "1px solid var(--color-border)",
      }}
    >
      <svg
        width="20"
        height="20"
        viewBox="0 0 20 20"
        fill="none"
        aria-hidden="true"
        style={{ color: "var(--color-brand-primary)", flexShrink: 0 }}
      >
        <path
          d="M10 2.5l2.4 4.9 5.4.8-3.9 3.8.9 5.4L10 14.9l-4.8 2.5.9-5.4-3.9-3.8 5.4-.8z"
          stroke="currentColor"
          strokeWidth="1.5"
          strokeLinecap="round"
          strokeLinejoin="round"
        />
      </svg>
      <p
        style={{
          margin: 0,
          flex: "1 1 auto",
          fontFamily: "var(--font-body)",
          fontSize: "var(--text-md)",
          lineHeight: "var(--leading-normal)",
          fontWeight: 500,
          color: "var(--color-brand-primary)",
        }}
      >
        {message}
      </p>
      {actionLabel ? (
        <a
          href={actionHref}
          style={{
            display: "inline-flex",
            alignItems: "center",
            gap: "var(--space-4)",
            color: "var(--color-brand-primary)",
            fontFamily: "var(--font-body)",
            fontSize: "var(--text-md)",
            fontWeight: 700,
            textDecoration: "underline",
            textUnderlineOffset: "3px",
          }}
        >
          {actionLabel}
          <svg
            width="14"
            height="14"
            viewBox="0 0 16 16"
            fill="none"
            aria-hidden="true"
          >
            <path
              d="M3.5 8h9M8.5 4l4 4-4 4"
              stroke="currentColor"
              strokeWidth="1.75"
              strokeLinecap="round"
              strokeLinejoin="round"
            />
          </svg>
        </a>
      ) : null}
    </div>
  );
}
