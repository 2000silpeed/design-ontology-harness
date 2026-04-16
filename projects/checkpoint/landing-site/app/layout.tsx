import type { Metadata } from "next";
import { JetBrains_Mono } from "next/font/google";
import "./globals.css";
import { SiteHeader } from "@/components/site-header/SiteHeader";
import { SiteLogo } from "@/components/site-header/SiteLogo";
import { SiteNav } from "@/components/site-header/SiteNav";
import { SiteNavCta } from "@/components/site-header/SiteNavCta";
import { MobileMenuTrigger } from "@/components/site-header/MobileMenuTrigger";
import { SiteFooter } from "@/components/site-footer/SiteFooter";
import { FooterColumn } from "@/components/site-footer/FooterColumn";
import { FooterLink } from "@/components/site-footer/FooterLink";
import { FooterLegal } from "@/components/site-footer/FooterLegal";

const jetbrainsMono = JetBrains_Mono({
  variable: "--font-jetbrains-mono",
  subsets: ["latin"],
  display: "swap",
});

export const metadata: Metadata = {
  title: "Checkpoint — 살지 말지, 한 화면에서 끝내는 게임 리뷰",
  description:
    "콘솔과 PC 게임을 비평, 비교, 추천하는 에디토리얼 게임 리뷰 사이트. 리뷰, 패치 재평가, 플랫폼별 성능 메모를 한 화면에서 제공합니다.",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="ko" className={`${jetbrainsMono.variable} h-full antialiased`}>
      <body className="min-h-full flex flex-col bg-canvas text-text">
        <SiteHeader>
          <SiteLogo />
          <SiteNav />
          <SiteNavCta />
          <MobileMenuTrigger />
        </SiteHeader>
        <main className="flex-1">{children}</main>
        <SiteFooter>
          <FooterColumn title="Reviews">
            <FooterLink href="#reviews">Latest Reviews</FooterLink>
            <FooterLink href="#verdicts">Verdict Snapshot</FooterLink>
            <FooterLink href="#compare">Compare Board</FooterLink>
            <FooterLink href="#charts">Charts</FooterLink>
          </FooterColumn>
          <FooterColumn title="Tools">
            <FooterLink href="#compare">구매 판단 도구</FooterLink>
            <FooterLink href="#membership">멤버십</FooterLink>
            <FooterLink href="#newsletter">뉴스레터</FooterLink>
            <FooterLink href="#faq">FAQ</FooterLink>
          </FooterColumn>
          <FooterColumn title="Editorial">
            <FooterLink href="#methodology">방법론</FooterLink>
            <FooterLink href="#methodology">점수 체계</FooterLink>
            <FooterLink href="#reviews">플랫폼 커버리지</FooterLink>
            <FooterLink href="#about">에디터 노트</FooterLink>
          </FooterColumn>
          <FooterColumn title="Checkpoint">
            <FooterLink href="#about">About</FooterLink>
            <FooterLink href="#newsletter">Contact</FooterLink>
            <FooterLink href="#membership">Partnerships</FooterLink>
            <FooterLink href="#faq">Support</FooterLink>
          </FooterColumn>
          <FooterLegal />
        </SiteFooter>
      </body>
    </html>
  );
}
