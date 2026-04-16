export function HeroVisual() {
  return (
    <div
      aria-hidden="true"
      style={{
        position: "relative",
        width: "100%",
        aspectRatio: "4 / 3",
        borderRadius: "var(--radius-xl)",
        background:
          "linear-gradient(160deg, var(--color-surface-tint) 0%, var(--color-surface) 100%)",
        border: "1px solid var(--color-border)",
        boxShadow:
          "0 1px 2px rgba(0,0,0,0.04), 0 12px 32px -12px rgba(0,0,0,0.18)",
        padding: "var(--space-24)",
        overflow: "hidden",
      }}
    >
      <svg
        width="100%"
        height="100%"
        viewBox="0 0 320 240"
        role="img"
        aria-label="Glacier archive visualization"
        style={{ display: "block" }}
      >
        <defs>
          <linearGradient id="glacier-stack" x1="0" y1="0" x2="0" y2="1">
            <stop offset="0%" stopColor="var(--color-brand-primary)" stopOpacity="0.14" />
            <stop offset="100%" stopColor="var(--color-brand-primary)" stopOpacity="0.02" />
          </linearGradient>
        </defs>

        {/* Layered archive "chunks" */}
        <g>
          {[0, 1, 2, 3, 4].map((i) => (
            <rect
              key={i}
              x={28 + i * 6}
              y={36 + i * 28}
              width={264 - i * 12}
              height={22}
              rx={4}
              fill="url(#glacier-stack)"
              stroke="var(--color-brand-primary)"
              strokeWidth={1}
              strokeOpacity={0.3}
            />
          ))}
        </g>

        {/* Verification check badge */}
        <g transform="translate(228, 28)">
          <circle
            cx={24}
            cy={24}
            r={22}
            fill="var(--color-surface)"
            stroke="var(--color-brand-accent)"
            strokeWidth={1.5}
          />
          <path
            d="M14 24l7 7 13-14"
            stroke="var(--color-brand-accent)"
            strokeWidth={2.5}
            strokeLinecap="round"
            strokeLinejoin="round"
            fill="none"
          />
        </g>

        {/* SHA label */}
        <g transform="translate(28, 200)">
          <rect
            x={0}
            y={0}
            width={148}
            height={22}
            rx={4}
            fill="var(--color-surface)"
            stroke="var(--color-border)"
            strokeWidth={1}
          />
          <circle cx={12} cy={11} r={3} fill="var(--color-brand-accent)" />
          <text
            x={22}
            y={15}
            fontSize={10}
            fontFamily="var(--font-mono)"
            fill="var(--color-text-muted)"
          >
            SHA-256 verified
          </text>
        </g>
      </svg>
    </div>
  );
}
