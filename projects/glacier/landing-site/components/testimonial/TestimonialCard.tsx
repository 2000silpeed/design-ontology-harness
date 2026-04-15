import { TestimonialAuthor } from "./TestimonialAuthor";
import { TestimonialQuote } from "./TestimonialQuote";

type TestimonialCardProps = {
  quote: string;
  name: string;
  role: string;
  company: string;
};

export function TestimonialCard({
  quote,
  name,
  role,
  company,
}: TestimonialCardProps) {
  return (
    <article
      style={{
        display: "flex",
        flexDirection: "column",
        gap: "var(--space-24)",
        justifyContent: "space-between",
        background: "var(--color-surface)",
        border: "1px solid var(--color-border)",
        borderRadius: "var(--radius-xl)",
        padding: "var(--space-32)",
      }}
    >
      <TestimonialQuote>{quote}</TestimonialQuote>
      <TestimonialAuthor name={name} role={role} company={company} />
    </article>
  );
}
