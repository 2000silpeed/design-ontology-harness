# Beacon — B2B/SaaS Minimal-Tech 마케팅 랜딩 Spec

## 제품 개요
Beacon 은 B2B/SaaS · devtools 팀이 빠르게 구성할 수 있는 **minimal-tech 톤 마케팅 랜딩 (marketing-landing)** 이다.
Linear / Vercel / Stripe / Railway / Supabase 계열의 **hero section + feature grid +
pricing · social proof · testimonial · faq accordion + landing cta section + site header + site footer**
를 한 페이지에서 정갈하게 조합해 방문자의 이해·신뢰·전환을 유도한다.
이 프리셋은 "대담한 스포츠 랜딩"이나 "매거진 에디토리얼"이 아니라 **"restrained SaaS landing"** 성향으로,
hairline borders · neutral hero surface · monochrome + restrained gold accent · geometric sans hierarchy 를
시각 정체성으로 고정한다. 한국어 UI 를 1급으로 지원한다.

## 사용자
- **B2B/SaaS 프로덕트 팀**: 성장/마케팅 엔지니어 — hero / pricing / faq 수정, feature grid 복제
- **개발자 도구 회사 마케터**: devtools 랜딩 제작 — social proof logo cloud + testimonial 중심
- **스타트업 초기 마케팅 리드**: 투명·정직 전환 페이지 — cta section + pricing 명료성

## 핵심 화면
1. **Hero** — site header + site nav + hero container + hero eyebrow + hero headline + hero subheadline + hero cta group + hero visual + hero trust strip
2. **Features** — feature section + feature grid + feature card + feature icon + feature title + feature description
3. **Social Proof** — logo cloud + customer logo + metric highlight + press quote
4. **Testimonials** — testimonial section + testimonial card + testimonial quote + testimonial author
5. **Pricing** — pricing card + feature comparison + upgrade banner (monthly/yearly toggle)
6. **FAQ + CTA** — faq section + faq item + faq question + faq answer + cta section + cta headline + cta supporting text + cta button group
7. **Site Footer** — site footer + footer column + footer link + footer legal + footer social

## UI 컴포넌트 (도출)
- **site-header** — sticky on scroll site header, 로고 + nav + CTA 묶음
- **site-logo** — 브랜드 로고 영역, hero/footer 공용
- **site-nav** — 주요 섹션 내비게이션 링크 (Features / Pricing / Docs / Blog)
- **site-nav-cta** — 헤더 우측 CTA 버튼 (로그인 / 무료로 시작하기)
- **mobile-menu-trigger** — 모바일 햄버거 메뉴 버튼
- **hero-container** — neutral hero surface, powder-blue tint, hairline section divider
- **hero-eyebrow** — headline 위 카테고리/레이블 텍스트 (goldenrod mini pill)
- **hero-headline** — 핵심 가치 제안 headline, geometric sans 600, 한글은 Pretendard keep-all
- **hero-subheadline** — headline 보강 subhead, 본문 400, line-height 1.5
- **hero-cta-group** — primary(goldenrod) / secondary(ghost) CTA 버튼 묶음, focus highlight
- **hero-visual** — 우측/하단 제품 스크린샷 또는 low-contrast illustration
- **hero-trust-strip** — hero 하단 신뢰 라인 (사용자 수, 평가, 고객 로고 축소판)
- **feature-section** — feature 섹션 컨테이너와 섹션 헤더 (eyebrow + headline + subhead)
- **feature-grid** — compact feature grid, 3×2 또는 2×3, hairline divider
- **feature-card** — 개별 feature card — feature icon + feature title + feature description
- **feature-icon** — 기능 상징 아이콘, 20–24px stroke icon, teal tint
- **feature-title** — feature card 제목, geometric sans 600, 16–18px
- **feature-description** — feature card 본문 설명, 14px, 한글 keep-all line-height 1.6
- **logo-cloud** — social proof logo cloud, 고객/파트너 로고 나열, subtle marquee
- **customer-logo** — 개별 고객사 로고 아이템, monochrome + hover restore
- **metric-highlight** — 주요 지표 카드 (MRR, NPS, 이탈률) — mono tabular-nums 강조
- **press-quote** — 언론 인용 또는 어워드 스트립 (TechCrunch, Product Hunt 등)
- **testimonial-section** — testimonial 섹션 컨테이너
- **testimonial-card** — muted testimonial card — quote + author + 회사 로고
- **testimonial-quote** — 추천사 본문 텍스트, 14–16px, line-height 1.6
- **testimonial-author** — 작성자 이름/직책/회사, 12–13px, muted color
- **pricing-card** — thin pricing card — plan name + price (mono tabular-nums) + feature list + CTA button
- **feature-comparison** — 플랜 간 기능 비교 테이블, hairline row, 체크/대시 인디케이터
- **upgrade-banner** — 업그레이드 유도 배너 (annual 전환 할인)
- **faq-section** — FAQ 섹션 컨테이너와 섹션 헤더
- **faq-item** — 접고 펼 수 있는 개별 FAQ 항목 (accordion expand)
- **faq-question** — FAQ 질문 헤더 (클릭 가능한 트리거, chevron 회전)
- **faq-answer** — FAQ 답변 본문, 한글 keep-all
- **cta-section** — 전환 유도 CTA 섹션 컨테이너 — powder-blue surface tint
- **cta-headline** — 전환 유도 headline, geometric sans 700
- **cta-supporting-text** — CTA 보강 카피
- **cta-button-group** — primary(goldenrod) / secondary(ghost) CTA 묶음
- **site-footer** — 사이트 전역 하단 컨테이너 — multi-column
- **footer-column** — 링크 그룹을 담는 세로 컬럼 (Product / Company / Resources / Legal)
- **footer-link** — 푸터 내 개별 링크, muted + underline on hover
- **footer-legal** — 저작권·법적 고지 영역, 12px muted
- **footer-social** — 소셜 링크 아이콘 그룹 (GitHub, X, LinkedIn)
- **primary-button** — primary CTA (goldenrod fill + teal text), keyboard focus ring
- **secondary-button** — ghost secondary CTA (hairline border)
- **pricing toggle** — monthly/yearly 토글 (yearly 할인 뱃지)
- **anchor-scroll-link** — hero/features/pricing 섹션 앵커 스크롤 링크
- **cookie-consent-banner** — 하단 쿠키 배너 (muted, dismissible)
- **dropdown-menu** — site-nav 의 Docs/Resources 드롭다운 메뉴

## 인터랙션 원칙
- **sticky site header on scroll**: 스크롤 시 header 가 부드럽게 shrink + hairline 강조
- **anchor scroll to section**: hero CTA / site-nav 링크는 scroll-snap 기반 anchor scroll
- **pricing toggle (monthly/yearly)**: yearly 선택 시 가격 숫자 tabular-nums 스왑, discount 뱃지 fade-in
- **faq accordion expand**: faq-item 클릭 시 chevron 180° 회전 + answer fade-in (120ms)
- **scroll-snap section**: 데스크톱에서 section 간 soft snap, motion-reduced 모드 존중
- **cta button focus highlight**: keyboard focus 시 goldenrod outline + offset, 접근성 우선
- **logo marquee subtle motion**: logo cloud 느린 marquee, hover 시 pause
- **hover-only secondary CTA**: 보조 CTA 는 hover 시에만 underline — 저소음
- **low-motion**: 전반 120–200ms ease-out, decorative animation 금지, prefers-reduced-motion 존중
- 모바일에서 mobile-menu-trigger 탭 시 full-screen drawer menu 슬라이드

## 색상 전략
- **neutral hero surface** — 무채색 베이스 + Powder Blue surface tint 로 차분한 hero chrome
- **primary**: **Teal Blue (#01889F)** — cool 계열 minimal-tech, site-header 링크 hover · active CTA outline
- **accent**: **Goldenrod (#DAA520)** — restrained warm gold, primary CTA button fill · pricing featured plan 강조 · metric highlight 숫자
- **surface_tint**: **Powder Blue (#B0E0E6)** — 부드러운 파스텔 cool, hero surface / cta-section / logo cloud 배경 / section divider
- **semantic**: success / warning / danger / info 4 role — upgrade-banner · form feedback 매핑
- **monochrome + restrained accent** — 랜딩 전반은 무채색, 강조는 teal + gold 단일
- **hairline borders** — 1px subtle border (low-contrast section divider), 깊은 elevation / drop shadow 금지
- **dark mode**: deep cool neutral surface (not pure black) + tuned teal + gold 채도 낮춤
- **기존 minimal-tech 5종 (Navy / Azure / Iris Violet / Cobalt Violet / Prussian Blue) 과 정체성 차별화**

## 타이포그래피
- **heading**: **Inter** (영문) / **Pretendard** (한글) — geometric sans, serif 금지
- **body**: **Inter / Pretendard** — hero subheadline / feature description / testimonial quote / faq answer 공용, line-height 1.5
- **mono**: **JetBrains Mono** — pricing 숫자 / metric highlight / 할인율 필수, tabular-nums 영문 고정
- **scale**: xs(11) / sm(12) / md(14) / lg(16) / xl(18) / 2xl(24) / 3xl(32) / 4xl(48)
- **hero headline**: 3xl–4xl (32–48px), heading 700, line-height 1.1–1.2
- **feature title**: lg (16–18px), heading 600
- **pricing price**: 3xl (32px) mono tabular-nums, currency/billing period 는 sm muted
- **faq question**: lg (16px) heading 600, answer 는 md (14px) body
- **한글 line-height**: 1.5 (hero/feature/pricing/testimonial), 1.6 (faq/legal long-form)
- **tabular-nums**: pricing / metric highlight / 할인율 숫자
- **emoji 자제**: 마케팅 랜딩 chrome 에서 이모지 사용 최소

## 접근성
- WCAG 2.2 AA (본문 대비 4.5:1, UI 3:1)
- cta button focus 는 goldenrod outline + 2px offset (키보드 가시성)
- site-nav 링크는 tab 순서 논리적, skip-to-main-content 링크 최상단
- faq accordion 은 aria-expanded + 키보드 enter/space 확장 지원
- pricing toggle 은 role="switch" + aria-checked, 키보드 toggle
- testimonial-card 의 인용구는 blockquote 시맨틱 + cite
- hero-visual 이미지는 alt 또는 aria-hidden 결정, 장식 이미지는 role="presentation"
- logo-cloud 은 목록 시맨틱 (ul/li), 각 로고 aria-label = "고객사명"
- prefers-reduced-motion 존중 — scroll-snap / marquee / fade-in 제거
- mobile-menu-trigger 는 aria-expanded + focus trap

## 한글 대응
- Pretendard variable (woff2) 번들, heading/body 공용
- 한글 hero headline / feature title line-height **1.5**, letter-spacing -1%
- 한글 faq answer / footer legal long-form line-height **1.6**
- word-break: **keep-all**, overflow-wrap: break-word
- pricing 숫자 / metric highlight / 할인율 은 mono 영문 고정 (한글 혼용 금지), tabular-nums
- 한국어 라벨: "기능 / 가격 / 고객사 / 후기 / 자주 묻는 질문 / 시작하기" + 영문 "features / pricing / customers / testimonials / faq / get started" 병기 허용
- hero CTA 는 "무료로 시작하기 (Get started free)" 형태의 이중 표기 허용

## 주의사항
- 이 프리셋은 **marketing-landing--minimal-tech (P2, saas/devtools)** — B2B/SaaS 최소 마케팅 랜딩 특화
- "대담·스포츠 랜딩" 은 `marketing-landing--bold-confident`
- "관리 대시보드 · 데이터 테이블" 은 `dashboard--minimal-tech`
- "API 레퍼런스 · 기술 문서" 는 `document-content--minimal-tech`
- "AI 코파일럿 채팅" 은 `conversation-copilot--minimal-tech`
- "운영 모니터링 · alert" 은 `monitoring-ops--minimal-tech`
- "캔버스 · 디자인 도구" 는 `canvas-tool--minimal-tech`
- "소셜 피드" 는 `community-feed--playful-soft`
- 이미지 기반 힌트는 advisory, 구조적 결정은 spec + KB 우선
- 실제 결제/구독/회원가입 백엔드 (billing, auth, analytics) 는 프리셋 범위 외 — 마케팅 chrome 만 다룸
