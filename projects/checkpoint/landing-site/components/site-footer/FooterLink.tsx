type FooterLinkProps = {
  href: string;
  children: string;
};

export function FooterLink({ href, children }: FooterLinkProps) {
  return (
    <li>
      <a
        href={href}
        style={{
          display: "inline-block",
          color: "var(--color-text-muted)",
          textDecoration: "none",
          fontFamily: "var(--font-body)",
          fontSize: "var(--text-md)",
          transition: "color var(--duration-120) var(--ease-standard)",
        }}
        className="footer-link"
      >
        {children}
      </a>
      <style>{`
        .footer-link:hover {
          color: var(--color-text);
        }
        .footer-link:focus-visible {
          text-decoration: underline;
          text-underline-offset: 4px;
        }
      `}</style>
    </li>
  );
}
