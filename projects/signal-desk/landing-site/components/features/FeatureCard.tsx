import { FeatureIcon, type FeatureIconName } from "./FeatureIcon";
import { FeatureTitle } from "./FeatureTitle";
import { FeatureDescription } from "./FeatureDescription";

type Props = {
  iconName: FeatureIconName;
  title: string;
  description: string;
};

export function FeatureCard({ iconName, title, description }: Props) {
  return (
    <article
      className="sd-feature-card"
      style={{
        display: "flex",
        flexDirection: "column",
        alignItems: "flex-start",
        gap: "var(--space-16)",
        background: "var(--color-card-surface-default)",
        border: "1px solid var(--color-card-border-default)",
        borderRadius: "var(--radius-lg)",
        padding: "var(--space-32)",
        transition: "border-color var(--duration-180) var(--ease-standard)",
      }}
    >
      <FeatureIcon iconName={iconName} />
      <FeatureTitle>{title}</FeatureTitle>
      <FeatureDescription>{description}</FeatureDescription>
      <style>{`
        .sd-feature-card:hover { border-color: var(--color-card-border-hover) !important; }
      `}</style>
    </article>
  );
}
