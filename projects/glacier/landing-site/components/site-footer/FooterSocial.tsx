import type { ReactNode } from "react";

type SocialItem = {
  label: string;
  href: string;
  icon: ReactNode;
};

const SOCIAL_ITEMS: SocialItem[] = [
  {
    label: "GitHub",
    href: "https://github.com/",
    icon: (
      <svg
        width="18"
        height="18"
        viewBox="0 0 24 24"
        fill="currentColor"
        aria-hidden="true"
        focusable="false"
      >
        <path d="M12 .5C5.73.5.5 5.73.5 12c0 5.08 3.29 9.39 7.86 10.91.58.1.79-.25.79-.56v-2.2c-3.2.7-3.87-1.37-3.87-1.37-.52-1.33-1.28-1.69-1.28-1.69-1.04-.72.08-.7.08-.7 1.15.08 1.76 1.18 1.76 1.18 1.03 1.77 2.71 1.26 3.37.96.1-.75.4-1.26.73-1.55-2.55-.29-5.23-1.28-5.23-5.71 0-1.26.45-2.29 1.18-3.1-.12-.29-.51-1.46.11-3.04 0 0 .97-.31 3.18 1.18a11 11 0 0 1 5.79 0c2.2-1.49 3.17-1.18 3.17-1.18.63 1.58.24 2.75.12 3.04.74.81 1.18 1.84 1.18 3.1 0 4.44-2.69 5.41-5.25 5.69.41.36.77 1.06.77 2.14v3.17c0 .31.21.67.8.56C20.22 21.39 23.5 17.08 23.5 12 23.5 5.73 18.27.5 12 .5z" />
      </svg>
    ),
  },
  {
    label: "LinkedIn",
    href: "https://linkedin.com/",
    icon: (
      <svg
        width="18"
        height="18"
        viewBox="0 0 24 24"
        fill="currentColor"
        aria-hidden="true"
        focusable="false"
      >
        <path d="M20.45 20.45h-3.55v-5.57c0-1.33-.02-3.04-1.85-3.04-1.85 0-2.14 1.45-2.14 2.94v5.67H9.36V9h3.41v1.56h.05c.48-.9 1.64-1.85 3.37-1.85 3.6 0 4.27 2.37 4.27 5.45v6.29zM5.34 7.43a2.06 2.06 0 1 1 0-4.12 2.06 2.06 0 0 1 0 4.12zM7.12 20.45H3.56V9h3.56v11.45zM22.23 0H1.77C.79 0 0 .77 0 1.72v20.56C0 23.23.79 24 1.77 24h20.45c.98 0 1.78-.77 1.78-1.72V1.72C24 .77 23.2 0 22.23 0z" />
      </svg>
    ),
  },
  {
    label: "X (Twitter)",
    href: "https://twitter.com/",
    icon: (
      <svg
        width="18"
        height="18"
        viewBox="0 0 24 24"
        fill="currentColor"
        aria-hidden="true"
        focusable="false"
      >
        <path d="M18.244 2H21.5l-7.19 8.21L22.5 22h-6.59l-5.16-6.74L4.9 22H1.64l7.69-8.78L1.5 2h6.75l4.66 6.16L18.24 2zm-1.16 18h1.82L7.02 4H5.1l11.98 16z" />
      </svg>
    ),
  },
];

export function FooterSocial() {
  return (
    <div
      style={{
        gridColumn: "1 / -1",
        display: "flex",
        alignItems: "center",
        gap: "var(--space-12)",
      }}
    >
      {SOCIAL_ITEMS.map((item) => (
        <a
          key={item.label}
          href={item.href}
          aria-label={item.label}
          target="_blank"
          rel="noopener noreferrer"
          style={{
            display: "inline-flex",
            alignItems: "center",
            justifyContent: "center",
            width: "40px",
            height: "40px",
            borderRadius: "var(--radius-md)",
            border: "1px solid var(--color-border)",
            color: "var(--color-text-muted)",
            background: "var(--color-surface)",
            transition:
              "color var(--duration-120) var(--ease-standard), border-color var(--duration-120) var(--ease-standard)",
          }}
          className="footer-social-link"
        >
          {item.icon}
        </a>
      ))}
      <style>{`
        .footer-social-link:hover {
          color: var(--color-text);
          border-color: var(--color-border-strong);
        }
      `}</style>
    </div>
  );
}
