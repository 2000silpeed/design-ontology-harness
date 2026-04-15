import type { Metadata } from "next";
import { Noto_Serif_KR, Source_Code_Pro } from "next/font/google";
import localFont from "next/font/local";
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
import { FooterSocial } from "@/components/site-footer/FooterSocial";

const notoSerifKr = Noto_Serif_KR({
  variable: "--font-noto-serif-kr",
  subsets: ["latin"],
  weight: ["400", "500", "600", "700"],
  display: "swap",
});

const sourceCodePro = Source_Code_Pro({
  variable: "--font-source-code-pro",
  subsets: ["latin"],
  display: "swap",
});

const pretendard = localFont({
  variable: "--font-pretendard",
  display: "swap",
  src: [
    {
      path: "../public/fonts/PretendardVariable.woff2",
      weight: "45 920",
      style: "normal",
    },
  ],
});

export const metadata: Metadata = {
  title: "Signal Desk — 생각의 호흡을 지키는 업무 공간",
  description:
    "독립 창작자와 작은 편집팀을 위한 고집 있는 에디토리얼 업무 앱. 글쓰기, 팀 협업, 발행 일정을 한 곳에서.",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html
      lang="ko"
      className={`${notoSerifKr.variable} ${pretendard.variable} ${sourceCodePro.variable} h-full antialiased`}
    >
      <body className="min-h-full flex flex-col">
        <SiteHeader>
          <SiteLogo />
          <SiteNav />
          <SiteNavCta />
          <MobileMenuTrigger />
        </SiteHeader>
        <main className="flex-1">{children}</main>
        <SiteFooter>
          <FooterColumn title="Product">
            <FooterLink href="#features">Features</FooterLink>
            <FooterLink href="#journal">Journal</FooterLink>
            <FooterLink href="#pricing">Pricing</FooterLink>
            <FooterLink href="#changelog">Changelog</FooterLink>
          </FooterColumn>
          <FooterColumn title="Resources">
            <FooterLink href="#guides">Guides</FooterLink>
            <FooterLink href="#handbook">Handbook</FooterLink>
            <FooterLink href="#case-studies">Case studies</FooterLink>
            <FooterLink href="#support">Support</FooterLink>
          </FooterColumn>
          <FooterColumn title="Company">
            <FooterLink href="#about">About</FooterLink>
            <FooterLink href="#manifesto">Manifesto</FooterLink>
            <FooterLink href="#hiring">Hiring</FooterLink>
            <FooterLink href="#contact">Contact</FooterLink>
          </FooterColumn>
          <FooterColumn title="Legal">
            <FooterLink href="#terms">Terms</FooterLink>
            <FooterLink href="#privacy">Privacy</FooterLink>
            <FooterLink href="#imprint">Imprint</FooterLink>
          </FooterColumn>
          <FooterSocial />
          <FooterLegal />
        </SiteFooter>
      </body>
    </html>
  );
}
