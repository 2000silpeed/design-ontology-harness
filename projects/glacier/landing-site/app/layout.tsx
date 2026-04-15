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
import { FooterSocial } from "@/components/site-footer/FooterSocial";
import { FooterLegal } from "@/components/site-footer/FooterLegal";

const jetbrainsMono = JetBrains_Mono({
  variable: "--font-jetbrains-mono",
  subsets: ["latin"],
  display: "swap",
});

export const metadata: Metadata = {
  title: "Glacier — Every byte, verified forever",
  description:
    "Long-term code and data archive for engineering teams. Verified restores, audit logs, and retention policies you can trust.",
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
          <FooterColumn title="Product">
            <FooterLink href="#features">Features</FooterLink>
            <FooterLink href="#pricing">Pricing</FooterLink>
            <FooterLink href="#changelog">Changelog</FooterLink>
            <FooterLink href="#api">API</FooterLink>
          </FooterColumn>
          <FooterColumn title="Resources">
            <FooterLink href="#docs">Docs</FooterLink>
            <FooterLink href="#guides">Guides</FooterLink>
            <FooterLink href="#status">Status</FooterLink>
            <FooterLink href="#support">Support</FooterLink>
          </FooterColumn>
          <FooterColumn title="Company">
            <FooterLink href="#about">About</FooterLink>
            <FooterLink href="#careers">Careers</FooterLink>
            <FooterLink href="#blog">Blog</FooterLink>
            <FooterLink href="#press">Press</FooterLink>
          </FooterColumn>
          <FooterColumn title="Legal">
            <FooterLink href="#terms">Terms</FooterLink>
            <FooterLink href="#privacy">Privacy</FooterLink>
            <FooterLink href="#security">Security</FooterLink>
            <FooterLink href="#dpa">DPA</FooterLink>
          </FooterColumn>
          <FooterSocial />
          <FooterLegal />
        </SiteFooter>
      </body>
    </html>
  );
}
