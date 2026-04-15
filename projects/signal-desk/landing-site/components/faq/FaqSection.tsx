import type { ReactNode } from "react";
import { FaqItem } from "./FaqItem";

type Entry = { question: string; answer: string };

const ITEMS: readonly Entry[] = [
  {
    question: "글자수 제한이 있나요?",
    answer:
      "모든 플랜에서 문서당 글자수 제한이 없습니다. Solo는 문서 개수만 50개로 제한됩니다.",
  },
  {
    question: "오프라인에서 작성할 수 있나요?",
    answer: "네, 로컬 저장소에 자동 저장되며 온라인 복구 시 자동 동기화됩니다.",
  },
  {
    question: "마크다운으로 내보낼 수 있나요?",
    answer: "네, 모든 문서는 Markdown, HTML, PDF로 내보낼 수 있습니다.",
  },
  {
    question: "버전 관리는 어떻게 되나요?",
    answer:
      "30초마다 자동 스냅샷이 저장되며 최대 1년간 모든 버전을 복원할 수 있습니다.",
  },
  {
    question: "팀원을 초대하려면?",
    answer:
      "Studio 이상 플랜에서 워크스페이스 설정의 '멤버 초대'로 이메일을 보낼 수 있습니다.",
  },
  {
    question: "결제는 어떻게 하나요?",
    answer:
      "카드 결제와 계좌이체를 지원하며, 연간 결제 시 두 달을 무료로 제공합니다.",
  },
  {
    question: "해지할 수 있나요?",
    answer: "언제든지 해지할 수 있으며, 결제한 기간은 끝까지 사용 가능합니다.",
  },
  {
    question: "다른 도구에서 데이터를 가져올 수 있나요?",
    answer: "Notion, Google Docs, Markdown 파일에서 직접 가져올 수 있습니다.",
  },
  {
    question: "한국어 외 언어도 지원하나요?",
    answer: "현재 한국어, 영어, 일본어를 지원합니다.",
  },
  {
    question: "접근성은 어떻게 되나요?",
    answer:
      "WCAG 2.2 AAA 기준을 준수하며, 스크린 리더와 키보드 내비게이션을 완전히 지원합니다.",
  },
];

export function FaqSection(): ReactNode {
  return (
    <section
      id="faq"
      aria-labelledby="faq-heading"
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
          maxWidth: "760px",
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
          }}
        >
          <span
            style={{
              fontFamily: "var(--font-mono)",
              fontSize: "var(--text-xs)",
              letterSpacing: "0.12em",
              textTransform: "uppercase",
              color: "var(--color-brand-primary)",
            }}
          >
            Questions
          </span>
          <h2
            id="faq-heading"
            style={{
              fontFamily: "var(--font-heading)",
              fontSize: "var(--text-3xl)",
              lineHeight: "var(--leading-tight)",
              color: "var(--color-text)",
              margin: 0,
              fontWeight: 500,
            }}
          >
            자주 묻는 질문
          </h2>
        </header>

        <div
          style={{
            display: "flex",
            flexDirection: "column",
            gap: "var(--space-16)",
          }}
        >
          {ITEMS.map((item) => (
            <FaqItem key={item.question} question={item.question} answer={item.answer} />
          ))}
        </div>
      </div>

      <style>{`
        .faq-item > .faq-question::-webkit-details-marker { display: none; }
        .faq-item > .faq-question { list-style: none; }
        .faq-item > .faq-question:hover { background: var(--color-surface-muted); }
        .faq-item[open] > .faq-question .faq-chevron { transform: rotate(180deg); }
      `}</style>
    </section>
  );
}
