import { FeatureDescription } from "./FeatureDescription";
import { FeatureIcon, type FeatureIconName } from "./FeatureIcon";
import { FeatureTitle } from "./FeatureTitle";

type FeatureCardProps = {
  iconName: FeatureIconName;
  title: string;
  description: string;
};

export function FeatureCard({ iconName, title, description }: FeatureCardProps) {
  return (
    <article
      className="glacier-feature-card"
      style={{
        display: "flex",
        flexDirection: "column",
        gap: "var(--space-16)",
        background: "var(--color-surface)",
        border: "1px solid var(--color-border)",
        borderRadius: "var(--radius-lg)",
        padding: "var(--space-32)",
        transition:
          "border-color var(--duration-180) var(--ease-standard), transform var(--duration-180) var(--ease-standard)",
      }}
    >
      <FeatureIcon iconName={iconName} />
      <div
        style={{
          display: "flex",
          flexDirection: "column",
          gap: "var(--space-8)",
        }}
      >
        <FeatureTitle>{title}</FeatureTitle>
        <FeatureDescription>{description}</FeatureDescription>
      </div>
      <style>{`
        .glacier-feature-card:hover {
          border-color: var(--color-border-strong) !important;
        }
      `}</style>
    </article>
  );
}
