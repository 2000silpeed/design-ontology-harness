import { TestimonialQuote } from "./TestimonialQuote";
import { TestimonialAuthor } from "./TestimonialAuthor";

type Props = {
  quote: string;
  name: string;
  role: string;
  company: string;
};

export function TestimonialCard({ quote, name, role, company }: Props) {
  return (
    <article
      className="sd-testimonial-card"
      style={{
        display: "flex",
        flexDirection: "column",
        justifyContent: "space-between",
        gap: "var(--space-32)",
        background: "var(--color-card-surface-default)",
        border: "1px solid var(--color-card-border-default)",
        borderRadius: "var(--radius-xl)",
        padding: "var(--space-32)",
        transition: "border-color var(--duration-180) var(--ease-standard)",
      }}
    >
      <TestimonialQuote>{quote}</TestimonialQuote>
      <TestimonialAuthor name={name} role={role} company={company} />
      <style>{`
        .sd-testimonial-card:hover { border-color: var(--color-card-border-hover) !important; }
      `}</style>
    </article>
  );
}
