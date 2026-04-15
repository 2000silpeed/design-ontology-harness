export function HeroVisual() {
  return (
    <div
      aria-hidden="true"
      style={{
        position: "relative",
        width: "100%",
        aspectRatio: "4 / 5",
        background: "var(--color-surface-muted)",
        border: "1px solid var(--color-border)",
        borderRadius: "var(--radius-lg)",
        overflow: "hidden",
        padding: "var(--space-24)",
      }}
    >
      <svg
        viewBox="0 0 400 500"
        width="100%"
        height="100%"
        style={{ display: "block" }}
      >
        <defs>
          <pattern id="sd-lines" width="400" height="28" patternUnits="userSpaceOnUse">
            <line
              x1="0"
              y1="27"
              x2="400"
              y2="27"
              stroke="var(--color-border)"
              strokeWidth="1"
            />
          </pattern>
        </defs>
        <rect
          x="50"
          y="70"
          width="300"
          height="380"
          rx="8"
          fill="var(--color-surface)"
          stroke="var(--color-border)"
          strokeWidth="1"
        />
        <rect
          x="38"
          y="58"
          width="300"
          height="380"
          rx="8"
          fill="var(--color-surface)"
          stroke="var(--color-border)"
          strokeWidth="1"
          opacity="0.5"
        />
        <rect x="70" y="100" width="260" height="320" fill="url(#sd-lines)" />
        <line
          x1="92"
          y1="100"
          x2="92"
          y2="420"
          stroke="var(--color-brand-accent)"
          strokeWidth="1"
        />
        <rect x="110" y="118" width="180" height="10" fill="var(--color-ink-subtle)" opacity="0.55" />
        <rect x="110" y="146" width="200" height="10" fill="var(--color-ink-subtle)" opacity="0.45" />
        <rect x="110" y="174" width="140" height="10" fill="var(--color-ink-subtle)" opacity="0.35" />
        <rect
          x="110"
          y="212"
          width="210"
          height="78"
          fill="var(--color-surface-muted)"
          stroke="var(--color-border)"
          strokeWidth="1"
          rx="4"
        />
        <text
          x="122"
          y="244"
          fontFamily="var(--font-heading)"
          fontSize="16"
          fill="var(--color-text)"
          fontStyle="italic"
        >
          “생각의 호흡을
        </text>
        <text
          x="122"
          y="268"
          fontFamily="var(--font-heading)"
          fontSize="16"
          fill="var(--color-text)"
          fontStyle="italic"
        >
          지키는 업무 공간.”
        </text>
        <rect x="110" y="308" width="160" height="8" fill="var(--color-ink-subtle)" opacity="0.35" />
        <rect x="110" y="328" width="190" height="8" fill="var(--color-ink-subtle)" opacity="0.3" />
        <rect x="110" y="348" width="120" height="8" fill="var(--color-ink-subtle)" opacity="0.3" />
        <path
          d="M 252 358 q 14 -6 24 6 q -10 8 -24 -6 z"
          fill="var(--color-brand-primary)"
        />
        <circle cx="288" cy="366" r="4" fill="var(--color-brand-primary)" />
        <line
          x1="288"
          y1="370"
          x2="288"
          y2="392"
          stroke="var(--color-brand-primary)"
          strokeWidth="2"
        />
      </svg>
    </div>
  );
}
