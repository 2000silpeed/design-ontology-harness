import { FeatureGrid, type FeatureItem } from "./FeatureGrid";

const ITEMS: FeatureItem[] = [
  {
    iconName: "editor",
    title: "리치 텍스트 에디터",
    description: "블록 기반 구조, 슬래시 커맨드, 마크다운 호환으로 흐름을 끊지 않는 글쓰기 경험을 제공합니다.",
  },
  {
    iconName: "review",
    title: "인라인 코멘트 & 리뷰 워크플로우",
    description: "팀과 함께 문장 단위로 피드백을 남기고, 제안을 수락하거나 반려하며 편집을 마무리합니다.",
  },
  {
    iconName: "calendar",
    title: "발행 일정 관리",
    description: "캘린더에서 마감과 게재 일정을 한눈에 확인하고, 담당자와 상태를 함께 관리합니다.",
  },
  {
    iconName: "palette",
    title: "커맨드 팔레트",
    description: "키보드 단축키로 모든 작업을 실행하세요. 문서 이동, 서식, 검색까지 한 곳에서 해결됩니다.",
  },
  {
    iconName: "history",
    title: "편집 히스토리",
    description: "버전 비교, 변경 추적, 복원이 자연스럽게 이어져 긴 호흡의 원고도 안전하게 다듬을 수 있습니다.",
  },
  {
    iconName: "moon",
    title: "다크 에디터",
    description: "눈에 편한 야간 작성 모드로, 깊은 밤에도 문장에 집중할 수 있도록 돕습니다.",
  },
];

export function FeatureSection() {
  return (
    <section
      id="features"
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
              color: "var(--color-text-subtle)",
              textTransform: "uppercase",
              letterSpacing: "0.12em",
              fontWeight: 500,
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
              fontWeight: 500,
              letterSpacing: "-0.01em",
            }}
          >
            글쓰기와 협업을 하나의 리듬으로
          </h2>
          <p
            style={{
              margin: 0,
              fontFamily: "var(--font-body)",
              fontSize: "var(--text-lg)",
              lineHeight: "var(--leading-relaxed)",
              color: "var(--color-text-muted)",
            }}
          >
            Signal Desk는 에디터와 작가, 편집팀이 같은 문서를 같은 속도로 다듬을 수 있도록 설계되었습니다. 도구가 보이지 않도록, 문장이 앞에 서도록.
          </p>
        </header>

        <FeatureGrid items={ITEMS} />
      </div>
    </section>
  );
}
