export function HeroTrustStrip({ items }: { items: string[] }) {
  return (
    <ul
      role="list"
      style={{
        display: "flex",
        flexWrap: "wrap",
        alignItems: "center",
        gap: "var(--space-12)",
        padding: 0,
        margin: 0,
        listStyle: "none",
        fontFamily: "var(--font-mono)",
        fontSize: "var(--text-xs)",
        color: "var(--color-text-muted)",
        letterSpacing: "0.04em",
      }}
    >
      {items.map((item, i) => (
        <li
          key={item}
          style={{ display: "inline-flex", alignItems: "center", gap: "var(--space-12)" }}
        >
          <span>{item}</span>
          {i < items.length - 1 ? (
            <span aria-hidden="true" style={{ color: "var(--color-text-subtle)" }}>
              ·
            </span>
          ) : null}
        </li>
      ))}
    </ul>
  );
}
