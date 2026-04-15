import { HeroContainer } from "@/components/hero/HeroContainer";
import { HeroEyebrow } from "@/components/hero/HeroEyebrow";
import { HeroHeadline } from "@/components/hero/HeroHeadline";
import { HeroSubheadline } from "@/components/hero/HeroSubheadline";
import { HeroCtaGroup } from "@/components/hero/HeroCtaGroup";
import { HeroVisual } from "@/components/hero/HeroVisual";
import { HeroTrustStrip } from "@/components/hero/HeroTrustStrip";
import { SocialProof } from "@/components/social-proof/SocialProof";
import { FeatureSection } from "@/components/features/FeatureSection";
import { TestimonialSection } from "@/components/testimonial/TestimonialSection";
import { PricingSection } from "@/components/pricing/PricingSection";
import { FaqSection } from "@/components/faq/FaqSection";
import { CtaSection } from "@/components/cta-section/CtaSection";

export default function Home() {
  return (
    <>
      <HeroContainer>
        <div>
          <HeroEyebrow>Editorial work OS</HeroEyebrow>
          <HeroHeadline>생각의 호흡을 지키는 업무 공간</HeroHeadline>
          <HeroSubheadline>
            글쓰기, 팀 협업, 발행 일정을 한 곳에서. 독립 창작자와 작은 편집팀을 위한 고집 있는 에디토리얼 업무 앱입니다.
          </HeroSubheadline>
          <HeroCtaGroup primaryLabel="무료로 시작" secondaryLabel="데모 영상 보기" />
          <HeroTrustStrip
            items={[
              "2,400명의 에디터가 사용",
              "월 1,200만 단어 작성",
              "AAA 접근성",
            ]}
          />
        </div>
        <HeroVisual />
      </HeroContainer>

      <SocialProof />
      <FeatureSection />
      <TestimonialSection />
      <PricingSection />
      <FaqSection />
      <CtaSection />
    </>
  );
}
