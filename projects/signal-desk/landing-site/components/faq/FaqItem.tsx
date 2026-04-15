import type { ReactNode } from "react";
import { FaqQuestion } from "./FaqQuestion";
import { FaqAnswer } from "./FaqAnswer";

type Props = {
  question: string;
  answer: string;
};

export function FaqItem({ question, answer }: Props): ReactNode {
  return (
    <details
      className="faq-item"
      style={{
        borderBottom: "1px solid var(--color-border)",
      }}
    >
      <FaqQuestion>{question}</FaqQuestion>
      <FaqAnswer>{answer}</FaqAnswer>
    </details>
  );
}
