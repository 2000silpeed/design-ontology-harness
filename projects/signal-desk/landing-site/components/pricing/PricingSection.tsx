import type { ReactNode } from "react";
import { PricingCard } from "./PricingCard";
import { FeatureComparison } from "./FeatureComparison";

type Plan = {
  name: string;
  price: string;
  priceNote: string;
  features: string[];
  ctaLabel: string;
  featured?: boolean;
};

const PLANS: readonly Plan[] = [
  {
    name: "Solo",
    price: "₩0",
    priceNote: "월 · 개인",
    features: ["문서 50개", "기본 에디터", "단일 사용자", "커뮤니티 지원"],
    ctaLabel: "무료로 시작",
  },
  {
    name: "Studio",
    price: "₩19",
    priceNote: "월 · 사용자당",
    features: [
      "무제한 문서",
      "인라인 코멘트",
      "발행 일정 캘린더",
      "버전 히스토리",
      "다크 에디터",
    ],
    ctaLabel: "14일 무료 체험",
    featured: true,
  },
  {
    name: "Agency",
    price: "₩49",
    priceNote: "월 · 사용자당",
    features: [
      "Studio 전체 기능",
      "SSO + SAML",
      "감사 로그",
      "커스텀 도메인",
      "전담 에디터",
    ],
    ctaLabel: "영업팀 문의",
  },
];

export function PricingSection(): ReactNode {
  return (
    <section
      id="pricing"
      aria-labelledby="pricing-heading"
      style={{
        background: "var(--color-surface-muted)",
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
              letterSpacing: "0.12em",
              textTransform: "uppercase",
              color: "var(--color-brand-primary)",
            }}
          >
            Pricing
          </span>
          <h2
            id="pricing-heading"
            style={{
              fontFamily: "var(--font-heading)",
              fontSize: "var(--text-3xl)",
              lineHeight: "var(--leading-tight)",
              color: "var(--color-text)",
              margin: 0,
              fontWeight: 500,
            }}
          >
            정직한 가격, 열린 기능
          </h2>
          <p
            style={{
              fontFamily: "var(--font-body)",
              fontSize: "var(--text-lg)",
              lineHeight: "var(--leading-relaxed)",
              color: "var(--color-text-muted)",
              margin: 0,
            }}
          >
            혼자 쓰든 팀으로 쓰든 같은 에디터 경험. 필요한 만큼만 지불하고, 언제든 업그레이드하거나 해지할 수 있습니다.
          </p>
        </header>

        <div
          className="pricing-grid"
          style={{
            display: "grid",
            gridTemplateColumns: "1fr",
            gap: "var(--space-24)",
            alignItems: "stretch",
          }}
        >
          {PLANS.map((plan) => (
            <div key={plan.name} className={plan.featured ? "pricing-grid__cell pricing-grid__cell--featured" : "pricing-grid__cell"}>
              <PricingCard
                name={plan.name}
                price={plan.price}
                priceNote={plan.priceNote}
                features={plan.features}
                ctaLabel={plan.ctaLabel}
                featured={plan.featured}
              />
            </div>
          ))}
        </div>

        <FeatureComparison />
      </div>

      <style>{`
        .pricing-grid__cell { display: flex; }
        .pricing-grid__cell > * { width: 100%; }
        @media (min-width: 1040px) {
          .pricing-grid { grid-template-columns: repeat(3, minmax(0, 1fr)) !important; }
          .pricing-grid__cell--featured { margin-top: -16px; }
        }
      `}</style>
    </section>
  );
}
