import { CustomerLogo } from "./CustomerLogo";

type Props = {
  names: string[];
};

export function LogoCloud({ names }: Props) {
  return (
    <div
      role="list"
      aria-label="고객사 로고"
      style={{
        display: "flex",
        flexWrap: "wrap",
        justifyContent: "center",
        alignItems: "center",
        columnGap: "var(--space-48)",
        rowGap: "var(--space-24)",
      }}
    >
      {names.map((name) => (
        <span role="listitem" key={name}>
          <CustomerLogo name={name} />
        </span>
      ))}
    </div>
  );
}
