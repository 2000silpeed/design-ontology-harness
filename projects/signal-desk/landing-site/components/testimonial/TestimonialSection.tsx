import { TestimonialCard } from "./TestimonialCard";

const TESTIMONIALS = [
  {
    quote:
      "문장이 흐르는 리듬을 방해하지 않는 첫 에디터였어요. 댓글도 각주처럼 자연스럽게 붙습니다.",
    name: "서지안",
    role: "Editor-in-Chief",
    company: "이음 매거진",
  },
  {
    quote:
      "출간 일정을 캘린더에서 바로 관리하니 편집팀 회의 시간이 절반으로 줄었어요.",
    name: "Jamie Park",
    role: "Managing Editor",
    company: "Paperwork",
  },
  {
    quote: "버전 히스토리가 너무 예뻐서 가끔 예전 문장을 다시 읽습니다.",
    name: "이도현",
    role: "Independent Writer",
    company: "Freelance",
  },
];

export function TestimonialSection() {
  return (
    <section
      aria-labelledby="testimonial-heading"
      style={{
        background: "var(--color-canvas)",
        paddingTop: "var(--space-96)",
        paddingBottom: "var(--space-96)",
        paddingLeft: "var(--space-24)",
        paddingRight: "var(--space-24)",
      }}
    >
      <div
        style={{
          maxWidth: "1200px",
          margin: "0 auto",
          display: "flex",
          flexDirection: "column",
          gap: "var(--space-64)",
        }}
      >
        <header
          style={{
            display: "flex",
            flexDirection: "column",
            gap: "var(--space-16)",
            maxWidth: "720px",
          }}
        >
          <span
            style={{
              fontFamily: "var(--font-mono)",
              fontSize: "var(--text-xs)",
              color: "var(--color-text-subtle)",
              textTransform: "uppercase",
              letterSpacing: "0.12em",
              fontWeight: 500,
            }}
          >
            Voices
          </span>
          <h2
            id="testimonial-heading"
            style={{
              margin: 0,
              fontFamily: "var(--font-heading)",
              fontSize: "var(--text-3xl)",
              lineHeight: "var(--leading-tight)",
              color: "var(--color-text)",
              fontWeight: 500,
              letterSpacing: "-0.01em",
            }}
          >
            에디터들이 하는 말
          </h2>
        </header>

        <div
          className="sd-testimonial-grid"
          style={{
            display: "grid",
            gridTemplateColumns: "1fr",
            gap: "var(--space-32)",
          }}
        >
          {TESTIMONIALS.map((t) => (
            <TestimonialCard
              key={t.name}
              quote={t.quote}
              name={t.name}
              role={t.role}
              company={t.company}
            />
          ))}
        </div>
      </div>
      <style>{`
        @media (min-width: 1040px) {
          .sd-testimonial-grid { grid-template-columns: repeat(3, minmax(0, 1fr)) !important; }
        }
      `}</style>
    </section>
  );
}
