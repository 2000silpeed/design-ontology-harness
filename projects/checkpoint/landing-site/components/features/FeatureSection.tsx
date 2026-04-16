import { FeatureGrid, type FeatureItem } from "./FeatureGrid";

const FEATURE_ITEMS: FeatureItem[] = [
  {
    iconName: "checksum",
    title: "체크섬 기반 검증",
    description: "모든 청크에 SHA-256 검증, 복원 시 자동 재확인",
  },
  {
    iconName: "policy",
    title: "보존 정책 엔진",
    description: "법적 보존, 규제 대응, 자동 만료 규칙",
  },
  {
    iconName: "audit",
    title: "감사 로그",
    description: "누가 언제 무엇에 접근했는지 전부 기록",
  },
  {
    iconName: "restore",
    title: "빠른 복원",
    description: "인덱스 기반 부분 복원, 전체 복원 모두 지원",
  },
  {
    iconName: "replicate",
    title: "다중 리전 복제",
    description: "재해 복구를 위한 지역 간 자동 복제",
  },
  {
    iconName: "api",
    title: "개발자 친화 API",
    description: "CLI, REST API, Terraform provider 제공",
  },
];

export function FeatureSection() {
  return (
    <section
      aria-labelledby="features-heading"
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
            Features
          </span>
          <h2
            id="features-heading"
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
            모든 아카이브를 검증 가능하게
          </h2>
          <p
            style={{
              margin: 0,
              fontFamily: "var(--font-body)",
              fontSize: "var(--text-md)",
              lineHeight: "var(--leading-relaxed)",
              color: "var(--color-text-muted)",
            }}
          >
            모든 청크, 모든 정책, 모든 접근까지 추적합니다.
          </p>
        </div>

        <FeatureGrid items={FEATURE_ITEMS} />
      </div>
    </section>
  );
}
