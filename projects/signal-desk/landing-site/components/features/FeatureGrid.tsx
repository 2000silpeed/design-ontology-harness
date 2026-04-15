import { FeatureCard } from "./FeatureCard";
import type { FeatureIconName } from "./FeatureIcon";

export type FeatureItem = {
  iconName: FeatureIconName;
  title: string;
  description: string;
};

type Props = {
  items: FeatureItem[];
};

export function FeatureGrid({ items }: Props) {
  return (
    <div
      className="sd-feature-grid"
      style={{
        display: "grid",
        gridTemplateColumns: "1fr",
        gap: "var(--space-32)",
      }}
    >
      {items.map((item) => (
        <FeatureCard
          key={item.title}
          iconName={item.iconName}
          title={item.title}
          description={item.description}
        />
      ))}
      <style>{`
        @media (min-width: 720px) {
          .sd-feature-grid { grid-template-columns: repeat(2, minmax(0, 1fr)) !important; }
        }
        @media (min-width: 1040px) {
          .sd-feature-grid { grid-template-columns: repeat(3, minmax(0, 1fr)) !important; }
        }
      `}</style>
    </div>
  );
}
