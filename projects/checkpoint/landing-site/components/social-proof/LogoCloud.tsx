import { CustomerLogo } from "./CustomerLogo";

type LogoCloudProps = {
  names: string[];
};

export function LogoCloud({ names }: LogoCloudProps) {
  return (
    <div
      role="list"
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
        <div role="listitem" key={name}>
          <CustomerLogo name={name} />
        </div>
      ))}
    </div>
  );
}
