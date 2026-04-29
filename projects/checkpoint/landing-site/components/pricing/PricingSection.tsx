import { PricingCard } from "./PricingCard";
import { FeatureComparison } from "./FeatureComparison";

type Plan = {
  planName: string;
  price: string;
  priceSuffix?: string;
  features: string[];
  ctaLabel: string;
  ctaHref?: string;
  featured?: boolean;
};

const PLANS: Plan[] = [
  {
    planName: "Starter",
    price: "₩0",
    priceSuffix: "/ 월",
    features: [
      "100GB 아카이브",
      "7일 보존",
      "SHA-256 검증",
      "커뮤니티 지원",
    ],
    ctaLabel: "무료로 시작",
    ctaHref: "#get-started",
  },
  {
    planName: "Team",
    price: "₩49",
    priceSuffix: "· 사용자/월",
    features: [
      "1TB 아카이브",
      "무제한 보존",
      "정책 엔진",
      "감사 로그 내보내기",
      "우선 지원",
    ],
    ctaLabel: "14일 무료 체험",
    ctaHref: "#trial",
    featured: true,
  },
  {
    planName: "Enterprise",
    price: "문의",
    features: [
      "무제한 아카이브",
      "SLA 99.99%",
      "SSO + SAML",
      "전담 엔지니어",
      "맞춤 계약",
    ],
    ctaLabel: "영업팀 문의",
    ctaHref: "#contact-sales",
  },
];

export function PricingSection() {
  return (
    <section
      aria-labelledby="pricing-heading"
      style={{
        position: "relative",
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
          alignItems: "stretch",
        }}
      >
        <header
          style={{
            display: "flex",
            flexDirection: "column",
            alignItems: "center",
            gap: "var(--space-16)",
            textAlign: "center",
            marginBottom: "var(--space-64)",
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
            요금제
          </span>
          <h2
            id="pricing-heading"
            style={{
              margin: 0,
              fontFamily: "var(--font-heading)",
              fontSize: "var(--text-4xl)",
              lineHeight: "var(--leading-tight)",
              fontWeight: 700,
              color: "var(--color-text)",
              maxWidth: "720px",
            }}
          >
            필요한 만큼만 지불하세요
          </h2>
          <p
            style={{
              margin: 0,
              maxWidth: "640px",
              fontFamily: "var(--font-body)",
              fontSize: "var(--text-lg)",
              lineHeight: "var(--leading-relaxed)",
              color: "var(--color-text-muted)",
            }}
          >
            무료로 시작하고, 팀이 성장하면 그에 맞춰 확장하세요. 모든 플랜에 체크섬 검증과 감사 로그가 포함됩니다.
          </p>
        </header>
        <div
          className="pricing-grid"
          style={{
            display: "grid",
            gridTemplateColumns: "minmax(0, 1fr)",
            gap: "var(--space-24)",
            alignItems: "stretch",
          }}
        >
          {PLANS.map((plan) => (
            <PricingCard key={plan.planName} {...plan} />
          ))}
        </div>
        <FeatureComparison />
      </div>
      <style>{`
        @media (min-width: 960px) {
          .pricing-grid {
            grid-template-columns: repeat(3, minmax(0, 1fr)) !important;
          }
        }
      `}</style>
    </section>
  );
}
