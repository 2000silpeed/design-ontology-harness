import { CtaHeadline } from "./CtaHeadline";
import { CtaSupportingText } from "./CtaSupportingText";
import { CtaButtonGroup } from "./CtaButtonGroup";

export function CtaSection() {
  return (
    <section
      aria-labelledby="cta-heading"
      style={{
        position: "relative",
        paddingTop: "var(--space-64)",
        paddingBottom: "var(--space-96)",
        paddingLeft: "var(--space-24)",
        paddingRight: "var(--space-24)",
        background: "var(--color-canvas)",
      }}
    >
      <div
        style={{
          maxWidth: "1120px",
          marginLeft: "auto",
          marginRight: "auto",
        }}
      >
        <div
          style={{
            position: "relative",
            background: "var(--color-brand-primary)",
            borderRadius: "var(--radius-xl)",
            paddingTop: "var(--space-96)",
            paddingBottom: "var(--space-96)",
            paddingLeft: "var(--space-48)",
            paddingRight: "var(--space-48)",
            display: "flex",
            flexDirection: "column",
            alignItems: "flex-start",
            gap: "var(--space-24)",
            overflow: "hidden",
          }}
        >
          <CtaHeadline>지금 첫 아카이브를 만들어보세요</CtaHeadline>
          <CtaSupportingText>
            30일 무료 체험 · 신용카드 없이 시작 · 5분 만에 첫 복원 리허설까지
          </CtaSupportingText>
          <CtaButtonGroup
            primaryLabel="무료로 시작"
            primaryHref="#get-started"
            secondaryLabel="문서 보기"
            secondaryHref="#docs"
          />
        </div>
      </div>
    </section>
  );
}
