import type { ReactNode } from "react";
import { CtaHeadline } from "./CtaHeadline";
import { CtaSupportingText } from "./CtaSupportingText";
import { CtaButtonGroup } from "./CtaButtonGroup";

export function CtaSection(): ReactNode {
  return (
    <section
      aria-labelledby="cta-heading"
      style={{
        background: "var(--color-canvas)",
        paddingTop: "var(--space-64)",
        paddingBottom: "var(--space-96)",
        paddingLeft: "var(--space-24)",
        paddingRight: "var(--space-24)",
      }}
    >
      <div
        style={{
          maxWidth: "1120px",
          margin: "0 auto",
          background: "var(--color-brand-primary)",
          color: "var(--color-text-inverse)",
          borderRadius: "var(--radius-xl)",
          paddingTop: "var(--space-96)",
          paddingBottom: "var(--space-96)",
          paddingLeft: "var(--space-48)",
          paddingRight: "var(--space-48)",
          display: "grid",
          justifyItems: "center",
          rowGap: "var(--space-24)",
        }}
      >
        <CtaHeadline>첫 문장을 쓰는 순간부터 다릅니다</CtaHeadline>
        <CtaSupportingText>14일 무료 체험 · 신용카드 없이 시작</CtaSupportingText>
        <div style={{ marginTop: "var(--space-16)" }}>
          <CtaButtonGroup primaryLabel="무료로 시작" secondaryLabel="사용 사례 보기" />
        </div>
      </div>
    </section>
  );
}
