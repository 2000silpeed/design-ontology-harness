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
          <HeroEyebrow>Long-term code and data archive</HeroEyebrow>
          <HeroHeadline>Every byte, verified forever</HeroHeadline>
          <HeroSubheadline>
            플랫폼 엔지니어와 SRE를 위한 장기 아카이브. 모든 청크에 SHA-256
            검증, 정책 기반 보존, 완전한 감사 로그를 기본으로 제공합니다.
          </HeroSubheadline>
          <HeroCtaGroup
            primaryLabel="무료로 시작"
            secondaryLabel="데모 예약"
          />
          <HeroTrustStrip
            items={[
              "SOC 2 Type II 인증",
              "99.999999999% 내구성",
              "50PB 운영",
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
