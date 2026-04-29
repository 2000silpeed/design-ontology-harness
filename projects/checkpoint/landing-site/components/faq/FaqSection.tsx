import { FaqItem } from "./FaqItem";

type Faq = {
  question: string;
  answer: string;
};

const FAQS: Faq[] = [
  {
    question: "보관 기간에 제한이 있나요?",
    answer:
      "모든 플랜에서 무제한 보존 정책을 지원하며, 자동 만료 규칙도 정의할 수 있습니다.",
  },
  {
    question: "복원 속도는 얼마나 빠른가요?",
    answer:
      "인덱스 기반 부분 복원은 초 단위, 전체 복원은 데이터 크기에 비례합니다.",
  },
  {
    question: "암호화는 어떻게 처리되나요?",
    answer:
      "모든 청크는 AES-256으로 암호화되며, 고객 관리 키(BYOK)를 지원합니다.",
  },
  {
    question: "감사 로그는 어디에 저장되나요?",
    answer:
      "쓰기 전용 append-only 저장소에 별도 보관되며, 7년 보존이 기본입니다.",
  },
  {
    question: "SOC 2와 ISO 27001 인증이 있나요?",
    answer: "네, SOC 2 Type II와 ISO 27001 인증을 모두 보유하고 있습니다.",
  },
  {
    question: "리전 선택이 가능한가요?",
    answer: "한국, 일본, 싱가포르, 미국, 유럽 리전을 선택할 수 있습니다.",
  },
  {
    question: "데이터 이그레스 비용이 있나요?",
    answer:
      "같은 리전 내 복원은 무료이며, 리전 간 복원만 별도 과금됩니다.",
  },
  {
    question: "삭제는 즉시 반영되나요?",
    answer:
      "보존 정책에 따라 다르며, 법적 보존 중인 데이터는 만료까지 삭제할 수 없습니다.",
  },
];

export function FaqSection() {
  return (
    <section
      aria-labelledby="faq-heading"
      style={{
        position: "relative",
        background: "var(--color-surface)",
        paddingTop: "var(--space-96)",
        paddingBottom: "var(--space-96)",
        paddingLeft: "var(--space-24)",
        paddingRight: "var(--space-24)",
      }}
    >
      <div
        style={{
          maxWidth: "760px",
          marginLeft: "auto",
          marginRight: "auto",
          display: "flex",
          flexDirection: "column",
          gap: "var(--space-48)",
        }}
      >
        <header
          style={{
            display: "flex",
            flexDirection: "column",
            alignItems: "center",
            gap: "var(--space-16)",
            textAlign: "center",
          }}
        >
          <span
            style={{
              display: "inline-flex",
              alignItems: "center",
              gap: "var(--space-8)",
              paddingTop: "var(--space-4)",
              paddingBottom: "var(--space-4)",
              paddingLeft: "var(--space-12)",
              paddingRight: "var(--space-12)",
              borderRadius: "var(--radius-pill)",
              background: "var(--color-surface-tint)",
              color: "var(--color-brand-primary)",
              fontFamily: "var(--font-body)",
              fontSize: "var(--text-xs)",
              fontWeight: 700,
              letterSpacing: "0em",
              textTransform: "uppercase",
            }}
          >
            FAQ
          </span>
          <h2
            id="faq-heading"
            style={{
              margin: 0,
              fontFamily: "var(--font-heading)",
              fontSize: "var(--text-4xl)",
              lineHeight: "var(--leading-tight)",
              fontWeight: 700,
              color: "var(--color-text)",
            }}
          >
            자주 묻는 질문
          </h2>
          <p
            style={{
              margin: 0,
              maxWidth: "560px",
              fontFamily: "var(--font-body)",
              fontSize: "var(--text-lg)",
              lineHeight: "var(--leading-relaxed)",
              color: "var(--color-text-muted)",
            }}
          >
            보관, 복원, 보안, 컴플라이언스에 대해 가장 많이 받는 질문을 모았습니다.
          </p>
        </header>
        <div
          style={{
            display: "flex",
            flexDirection: "column",
            gap: "var(--space-12)",
          }}
        >
          {FAQS.map((item, index) => (
            <FaqItem
              key={item.question}
              question={item.question}
              answer={item.answer}
              defaultOpen={index === 0}
            />
          ))}
        </div>
      </div>
    </section>
  );
}
