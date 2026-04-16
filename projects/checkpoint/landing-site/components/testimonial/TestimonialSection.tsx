import { TestimonialCard } from "./TestimonialCard";

type Testimonial = {
  quote: string;
  name: string;
  role: string;
  company: string;
};

const TESTIMONIALS: Testimonial[] = [
  {
    quote: "복원 실패 리허설에서 처음으로 100% 통과했습니다.",
    name: "김민준",
    role: "Platform Lead",
    company: "Northstar",
  },
  {
    quote: "감사 로그 덕분에 SOC 2 심사가 절반으로 줄었어요.",
    name: "Erika Wolff",
    role: "Head of Infra",
    company: "Acme Labs",
  },
  {
    quote: "정책 엔진 하나로 분산된 백업 룰을 다 걷어냈습니다.",
    name: "박소연",
    role: "SRE Manager",
    company: "Keystone",
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
          maxWidth: "1120px",
          marginLeft: "auto",
          marginRight: "auto",
          display: "flex",
          flexDirection: "column",
          gap: "var(--space-64)",
        }}
      >
        <div
          style={{
            display: "flex",
            flexDirection: "column",
            gap: "var(--space-16)",
            maxWidth: "640px",
          }}
        >
          <span
            style={{
              display: "inline-flex",
              alignItems: "center",
              alignSelf: "flex-start",
              paddingTop: "var(--space-8)",
              paddingBottom: "var(--space-8)",
              paddingLeft: "var(--space-12)",
              paddingRight: "var(--space-12)",
              background: "var(--color-surface-tint)",
              color: "var(--color-brand-primary)",
              borderRadius: "var(--radius-pill)",
              fontFamily: "var(--font-mono)",
              fontSize: "var(--text-xs)",
              fontWeight: 600,
              letterSpacing: "0.08em",
              textTransform: "uppercase",
              lineHeight: "var(--leading-tight)",
            }}
          >
            Testimonials
          </span>
          <h2
            id="testimonial-heading"
            style={{
              margin: 0,
              fontFamily: "var(--font-heading)",
              fontSize: "var(--text-3xl)",
              lineHeight: "var(--leading-tight)",
              color: "var(--color-text)",
              fontWeight: 700,
              letterSpacing: "-0.015em",
            }}
          >
            SRE와 플랫폼 팀의 신뢰
          </h2>
        </div>

        <div
          className="glacier-testimonial-grid"
          style={{
            display: "grid",
            gridTemplateColumns: "minmax(0, 1fr)",
            gap: "var(--space-24)",
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
          <style>{`
            @media (min-width: 720px) {
              .glacier-testimonial-grid {
                grid-template-columns: repeat(2, minmax(0, 1fr)) !important;
              }
            }
            @media (min-width: 1040px) {
              .glacier-testimonial-grid {
                grid-template-columns: repeat(3, minmax(0, 1fr)) !important;
              }
            }
          `}</style>
        </div>
      </div>
    </section>
  );
}
