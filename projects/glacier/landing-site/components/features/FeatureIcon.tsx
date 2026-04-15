export type FeatureIconName =
  | "checksum"
  | "policy"
  | "audit"
  | "restore"
  | "replicate"
  | "api";

type FeatureIconProps = {
  iconName: FeatureIconName;
};

function renderPath(iconName: FeatureIconName) {
  switch (iconName) {
    case "checksum":
      return (
        <g>
          <path d="M3 7h14M3 13h14M7 3v14M13 3v14" />
        </g>
      );
    case "policy":
      return (
        <g>
          <path d="M10 2.5 3.5 5v5c0 4 2.8 6.6 6.5 7.5 3.7-.9 6.5-3.5 6.5-7.5V5L10 2.5Z" />
          <path d="m7.5 10 1.8 1.8L13 8" />
        </g>
      );
    case "audit":
      return (
        <g>
          <path d="M4 4h12v12H4z" />
          <path d="m6.5 8 1.5 1.5L11 6.5M6.5 13l1.5 1.5L11 11.5" />
          <path d="M13 9h1.5M13 14h1.5" />
        </g>
      );
    case "restore":
      return (
        <g>
          <path d="M3.5 10a6.5 6.5 0 1 0 1.9-4.6" />
          <path d="M3 3v4h4" />
        </g>
      );
    case "replicate":
      return (
        <g>
          <path d="M3 7h9v9H3z" />
          <path d="M6 4h9v9" />
          <path d="M9 1h9v9" />
        </g>
      );
    case "api":
      return (
        <g>
          <path d="m6 6-4 4 4 4" />
          <path d="m14 6 4 4-4 4" />
          <path d="m11 4-2 12" />
        </g>
      );
    default:
      return null;
  }
}

export function FeatureIcon({ iconName }: FeatureIconProps) {
  return (
    <div
      aria-hidden="true"
      style={{
        width: "40px",
        height: "40px",
        display: "inline-flex",
        alignItems: "center",
        justifyContent: "center",
        background: "var(--color-surface-tint)",
        color: "var(--color-brand-primary)",
        borderRadius: "var(--radius-md)",
      }}
    >
      <svg
        width="20"
        height="20"
        viewBox="0 0 20 20"
        fill="none"
        stroke="currentColor"
        strokeWidth="1.75"
        strokeLinecap="round"
        strokeLinejoin="round"
      >
        {renderPath(iconName)}
      </svg>
    </div>
  );
}
