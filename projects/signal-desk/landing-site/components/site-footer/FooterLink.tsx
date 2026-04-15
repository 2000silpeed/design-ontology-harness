import type { ReactNode } from "react";

export function FooterLink({
  href,
  children,
}: {
  href: string;
  children: ReactNode;
}) {
  return (
    <li>
      <a
        href={href}
        className="footer-link"
        style={{
          display: "inline-block",
          fontSize: "var(--text-sm)",
          color: "var(--color-text-muted)",
          textDecoration: "none",
          padding: "var(--space-8) 0",
          transition: "color var(--duration-180) var(--ease-standard)",
        }}
      >
        {children}
      </a>
      <style>{`
        .footer-link:hover { color: var(--color-text); }
      `}</style>
    </li>
  );
}
