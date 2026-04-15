type Props = {
  name: string;
};

export function CustomerLogo({ name }: Props) {
  return (
    <span
      className="sd-customer-logo"
      style={{
        fontFamily: "var(--font-heading)",
        fontSize: "var(--text-md)",
        color: "var(--color-text-subtle)",
        letterSpacing: "0.04em",
        fontWeight: 500,
        opacity: 0.7,
        transition:
          "opacity var(--duration-180) var(--ease-standard), color var(--duration-180) var(--ease-standard)",
        whiteSpace: "nowrap",
      }}
    >
      {name}
      <style>{`
        .sd-customer-logo:hover { opacity: 1 !important; color: var(--color-text) !important; }
      `}</style>
    </span>
  );
}
