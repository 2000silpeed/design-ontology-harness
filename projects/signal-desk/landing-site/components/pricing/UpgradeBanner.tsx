import type { ReactNode } from "react";

type Props = {
  message: string;
  actionLabel?: string;
  actionHref?: string;
};

function StarIcon() {
  return (
    <svg
      aria-hidden="true"
      width="18"
      height="18"
      viewBox="0 0 20 20"
      fill="none"
      style={{ flexShrink: 0, color: "var(--color-feedback-warning-text)" }}
    >
      <path
        d="M10 2L12.2451 7.0557L17.7553 7.6459L13.6351 11.3443L14.7553 16.7541L10 14.0557L5.24472 16.7541L6.36487 11.3443L2.24472 7.6459L7.75492 7.0557L10 2Z"
        stroke="currentColor"
        strokeWidth="1.6"
        strokeLinejoin="round"
      />
    </svg>
  );
}

export function UpgradeBanner({ message, actionLabel, actionHref = "#pricing" }: Props): ReactNode {
  return (
    <div
      role="status"
      style={{
        display: "flex",
        alignItems: "center",
        gap: "var(--space-12)",
        background: "var(--color-feedback-warning-surface)",
        color: "var(--color-feedback-warning-text)",
        borderLeft: "3px solid var(--color-feedback-warning-border)",
        borderRadius: "var(--radius-lg)",
        padding: "var(--space-16) var(--space-24)",
        fontFamily: "var(--font-body)",
        fontSize: "var(--text-sm)",
        lineHeight: "var(--leading-comfortable)",
      }}
    >
      <StarIcon />
      <span style={{ flex: 1 }}>{message}</span>
      {actionLabel ? (
        <a
          href={actionHref}
          style={{
            fontFamily: "var(--font-body)",
            fontSize: "var(--text-sm)",
            fontWeight: 500,
            color: "var(--color-feedback-warning-text)",
            textDecoration: "underline",
            textUnderlineOffset: "3px",
            transition: "color var(--duration-180) var(--ease-standard)",
          }}
        >
          {actionLabel}
        </a>
      ) : null}
    </div>
  );
}
