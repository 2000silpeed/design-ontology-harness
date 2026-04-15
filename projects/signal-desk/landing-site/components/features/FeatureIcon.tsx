export type FeatureIconName =
  | "editor"
  | "review"
  | "calendar"
  | "palette"
  | "history"
  | "moon";

type Props = {
  iconName: FeatureIconName;
};

function IconSvg({ name }: { name: FeatureIconName }) {
  const common = {
    width: 22,
    height: 22,
    viewBox: "0 0 24 24",
    fill: "none",
    stroke: "var(--color-brand-primary)",
    strokeWidth: 1.5,
    strokeLinecap: "round" as const,
    strokeLinejoin: "round" as const,
    "aria-hidden": true,
  };

  switch (name) {
    case "editor":
      return (
        <svg {...common}>
          <path d="M4 5h12" />
          <path d="M4 10h16" />
          <path d="M4 15h10" />
          <path d="M15 18l5-5 2 2-5 5H15v-2z" />
        </svg>
      );
    case "review":
      return (
        <svg {...common}>
          <path d="M4 5h16v11H9l-5 4V5z" />
          <path d="M8 10h8" />
          <path d="M8 13h5" />
        </svg>
      );
    case "calendar":
      return (
        <svg {...common}>
          <rect x="3.5" y="5" width="17" height="15" rx="2" />
          <path d="M3.5 10h17" />
          <path d="M8 3v4" />
          <path d="M16 3v4" />
          <circle cx="12" cy="15" r="1" fill="var(--color-brand-primary)" stroke="none" />
        </svg>
      );
    case "palette":
      return (
        <svg {...common}>
          <rect x="3.5" y="4.5" width="17" height="15" rx="2" />
          <path d="M7 9h10" />
          <path d="M7 12h6" />
          <path d="M14.5 15h3" />
        </svg>
      );
    case "history":
      return (
        <svg {...common}>
          <path d="M3.5 12a8.5 8.5 0 1 0 2.6-6.1" />
          <path d="M3.5 4v4.5H8" />
          <path d="M12 8v4.5l3 2" />
        </svg>
      );
    case "moon":
      return (
        <svg {...common}>
          <path d="M20 14.5A8 8 0 0 1 9.5 4a8 8 0 1 0 10.5 10.5z" />
        </svg>
      );
  }
}

export function FeatureIcon({ iconName }: Props) {
  return (
    <span
      aria-hidden="true"
      style={{
        display: "inline-flex",
        alignItems: "center",
        justifyContent: "center",
        width: "40px",
        height: "40px",
        background: "var(--color-surface-muted)",
        borderRadius: "var(--radius-md)",
        flexShrink: 0,
      }}
    >
      <IconSvg name={iconName} />
    </span>
  );
}
