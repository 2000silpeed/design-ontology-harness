"use client";

import type { ReactNode } from "react";
import { FaqQuestion } from "./FaqQuestion";
import { FaqAnswer } from "./FaqAnswer";

export type FaqItemProps = {
  question: string;
  answer: ReactNode;
  defaultOpen?: boolean;
};

export function FaqItem({ question, answer, defaultOpen = false }: FaqItemProps) {
  return (
    <details
      className="faq-item"
      open={defaultOpen}
      style={{
        background: "var(--color-surface)",
        border: "1px solid var(--color-border)",
        borderRadius: "var(--radius-lg)",
        paddingLeft: "var(--space-24)",
        paddingRight: "var(--space-24)",
        transitionProperty: "border-color, background-color",
        transitionDuration: "var(--duration-180)",
        transitionTimingFunction: "var(--ease-standard)",
      }}
    >
      <summary
        style={{
          listStyle: "none",
          cursor: "pointer",
          display: "flex",
          alignItems: "center",
          justifyContent: "space-between",
          gap: "var(--space-16)",
          paddingTop: "var(--space-24)",
          paddingBottom: "var(--space-24)",
          outline: "none",
        }}
      >
        <FaqQuestion>{question}</FaqQuestion>
        <span
          className="faq-item-indicator"
          aria-hidden="true"
          style={{
            flexShrink: 0,
            display: "inline-flex",
            alignItems: "center",
            justifyContent: "center",
            width: "32px",
            height: "32px",
            borderRadius: "var(--radius-pill)",
            background: "var(--color-surface-muted)",
            color: "var(--color-brand-primary)",
            transitionProperty: "transform, background-color",
            transitionDuration: "var(--duration-180)",
            transitionTimingFunction: "var(--ease-standard)",
          }}
        >
          <svg width="16" height="16" viewBox="0 0 16 16" fill="none">
            <path
              d="M4 6l4 4 4-4"
              stroke="currentColor"
              strokeWidth="1.75"
              strokeLinecap="round"
              strokeLinejoin="round"
            />
          </svg>
        </span>
      </summary>
      <FaqAnswer>{answer}</FaqAnswer>
      <style>{`
        .faq-item > summary::-webkit-details-marker {
          display: none;
        }
        .faq-item:hover {
          border-color: var(--color-brand-primary);
        }
        .faq-item[open] .faq-item-indicator {
          transform: rotate(180deg);
          background: var(--color-surface-tint);
        }
      `}</style>
    </details>
  );
}
