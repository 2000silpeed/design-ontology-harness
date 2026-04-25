# Loom — 독립 뉴스레터·매거진 Editorial-Warm Marketing Landing Spec

## 제품 개요
Loom 은 독립 뉴스레터 발행인 · 1인 퍼블리셔 · 소규모 편집팀이 바로 쓸 수 있는 **editorial-warm 톤 마케팅 랜딩 (marketing-landing)** 이다.
Stratechery · Ghost Publisher · Every · Substack · The Verge Newsletters 계열의 **hero + featured issue + issue archive
strip + pricing table + subscribe cta + testimonial + author profile + faq accordion + site header + site footer** 를
warm Ochre Yellow primary + Rust copper accent + Wheat cream surface 로 엮어 **reading-first editorial 감성** 을 유지
하면서도 구독 전환 퍼널을 명확히 배치한다. 이 프리셋은 "B2B SaaS 미니멀 랜딩"(marketing-landing--minimal-tech, beacon) 도
아니고 "스포츠 bold 랜딩"(marketing-landing--bold-confident, premier-league) 도 아닌,
**"editorial-warm newsletter publisher landing"** 정체성이다. 한국어 UI 를 1급으로 지원한다.

## 사용자
- **독립 뉴스레터 발행인**: 본인 문체와 맞는 warm editorial 랜딩을 1일 만에 셋업, pricing + issue archive 로 구독 유도
- **독립 매거진·퍼블리셔**: 발행 주기 issue pipeline + pricing + author profile 을 한 페이지에 정돈하는 소규모 편집팀
- **뉴스레터 전환 최적화 담당자**: hero copy / pricing toggle / social proof / testimonial / faq / cta 배치 실험으로 구독 전환 개선

## 핵심 화면
1. **Hero** — site-header + hero-eyebrow + hero-headline(Fraunces 600 · Pretendard 700) + hero-subheadline + hero-subscribe-form + hero-trust-strip(구독자 수 + publisher 로고 스트립)
2. **Featured Issue** — featured-issue-card(최근 발행 + cover thumb + 발행일 + author avatar) + featured-issue-excerpt + read-full-issue link
3. **Issue Archive Strip** — issue-archive-strip + issue-card grid (2–3 카드 노출) + archive-cta(전체 아카이브 보기)
4. **Features / Why Subscribe** — reason-section + reason-card × 3 (editorial voice / archive access / community) + warm icon + reason-title
5. **Testimonials** — testimonial-section + testimonial-card × 3–4 + testimonial-quote(Fraunces italic) + testimonial-author
6. **Pricing** — pricing-section + pricing-toggle(monthly / yearly) + pricing-card × 2–3(highlighted tier 1 개 ochre fill) + pricing-feature-list + pricing-cta
7. **Author Profile** — author-card + author-portrait + author-bio(Pretendard 본문 line-height 1.7) + author-social-links
8. **FAQ + CTA** — faq-section + faq-item accordion × 6–8 + cta-banner(warm background + subscribe-cta rust fill)
9. **Site Footer** — site-footer + footer-column(about / archive / subscribe / legal) + footer-newsletter-preview

## UI 컴포넌트 (도출)
- **site-header** — sticky on scroll site header, logo + nav + subscribe CTA
- **site-logo** — 브랜드 로고, hero/footer 공용
- **site-nav** — 섹션 링크 (Issues / Pricing / About / Archive)
- **site-nav-cta** — 헤더 우측 subscribe 버튼 (warm ochre fill)
- **mobile-menu-trigger** — 모바일 햄버거 메뉴
- **hero-container** — warm neutral hero surface, wheat tint 은은, 하단 hairline
- **hero-eyebrow** — 카테고리/로마자 issue-number 라벨 (rust small chip)
- **hero-headline** — 핵심 가치 제안, Fraunces 600 / Pretendard 700, 한글은 keep-all
- **hero-subheadline** — headline 보강 본문, Inter 400 / Pretendard 400, line-height 1.6
- **hero-subscribe-form** — email capture input + primary subscribe cta + privacy note
- **hero-trust-strip** — 구독자 수 · 대표 publisher 로고 축소 스트립
- **featured-issue-card** — 최근 발행 강조 카드, issue-cover thumb + issue-title(Fraunces 600) + 발행일(mono) + author avatar + issue-excerpt
- **featured-issue-excerpt** — 첫 두 문단, line-height 1.7 reading-first
- **read-full-issue** — "전체 읽기" rust link with chevron
- **issue-archive-strip** — 최근 3 개 발행 카드 가로 스트립 + 전체 아카이브 CTA
- **issue-card** — 단일 issue 카드 — cover thumb + title + 발행일(mono tabular-nums) + 소요 시간 + rounded Wheat surface
- **issue-archive-grid** — 전체 아카이브 페이지용 grid (이 랜딩에는 strip 만 노출)
- **archive-cta** — "전체 아카이브 보기" rust accent link
- **reason-section** — 구독 이유 섹션 컨테이너 + section-header
- **reason-card** — 이유 단일 카드 — icon + title + description, warm Wheat hover
- **reason-icon** — 24px stroke, Ochre/Rust tint, 장식 최소
- **reason-title** — Fraunces 600, 한글 Pretendard 600
- **reason-description** — Inter 400 본문, keep-all line-height 1.6
- **testimonial-section** — testimonial 섹션 컨테이너 + warm quote-mark 오픈 장식
- **testimonial-card** — muted warm card, quote + author + role + 회사 로고
- **testimonial-quote** — Fraunces italic 본문, Pretendard 400 italic fallback, line-height 1.7
- **testimonial-author** — 이름 / 역할 / 매체, small muted
- **pricing-section** — pricing 섹션 컨테이너 + headline + 요금 정책 짧은 문단
- **pricing-toggle** — monthly / yearly 토글, active 탭 ochre underline
- **pricing-card** — thin pricing card, plan-name + price(mono tabular-nums, 큰 글자) + feature-list + cta
- **pricing-card-highlighted** — 추천 tier, warm ochre 테두리 + soft Wheat 배경 + "추천" 라벨
- **pricing-feature-list** — 체크 아이콘 + feature 라벨, 포함/미포함 구분
- **pricing-cta** — tier 별 primary 버튼, highlighted 는 rust fill
- **author-section** — author-card 섹션 컨테이너
- **author-card** — portrait + bio + social links
- **author-portrait** — 원형 포트레이트, warm shadow, 64–96 px
- **author-bio** — 4–6 줄, line-height 1.7, reading-first
- **author-social-links** — 소셜 아이콘 row (X, email, rss, about page)
- **faq-section** — FAQ 섹션 컨테이너 + section-header
- **faq-item** — accordion item, 클릭 시 slide-down
- **faq-question** — 질문 헤더, Fraunces 500 / Pretendard 600, chevron 회전
- **faq-answer** — 답변 본문, Pretendard keep-all line-height 1.6
- **cta-banner** — 전환 유도 밴드, Wheat surface + subscribe-cta rust fill + 한 줄 headline
- **subscribe-cta** — primary subscribe 버튼, ochre fill + rust hover, large tap target
- **cta-supporting-text** — cta 주변 작은 카피 ("무료 체험 없이 바로 구독", "언제든 해지")
- **email-capture-input** — 이메일 input, hairline border + focus ochre ring
- **privacy-note** — 이메일 폼 하단 privacy 문구, small muted
- **social-proof-logo-strip** — 구독자 회사 또는 언론사 로고 스트립, monochrome
- **site-footer** — footer container, warm neutral bg
- **footer-column** — about / archive / subscribe / legal 칼럼
- **footer-newsletter-preview** — 최근 발행 2 개 preview + 구독 링크
- **footer-social** — 소셜 아이콘 row (footer 용)
- **footer-legal** — 이용 약관 / 개인정보처리방침 / RSS
- **issue-number-chip** — hero / archive 공용 issue-number 미니 chip, mono
- **read-time-chip** — 예상 읽기 시간 chip, small muted

## 인터랙션 · 모션
- **hover fade** — 카드/버튼 hover 시 2–4% brightness 상승, transition 120 ms
- **subscribe cta pulse** — primary subscribe 버튼 가벼운 warm ring pulse (6 s once per load)
- **pricing toggle slide** — monthly / yearly 토글 시 underline slide 200 ms ease
- **faq accordion slide** — 열림/닫힘 180 ms, chevron rotate
- **testimonial carousel** — 가로 swipe 또는 dots navigation, 자동 재생 없음
- **issue strip hover** — issue-card hover 시 warm shadow 미세 증가 + title underline
- **focus ring** — 전 컴포넌트 focus 시 warm Ochre 2 px outline + 2 px offset

## Color Token 의도
- **primary #CB9D06 Ochre Yellow** — hero headline 강조 highlight / subscribe-cta fill / pricing-highlighted tier 테두리 / pricing-feature-list 체크 아이콘 / link underline
- **accent #B7410E Rust** — testimonial-quote 장식 quote-mark / pricing-card-highlighted cta fill / author-role chip / issue-count counter / cta-banner subscribe hover
- **surface_tint #F5DEB3 Wheat** — hero soft band / pricing-card-highlighted 배경 / testimonial-card / issue-card / cta-banner 배경
- **semantic**: success warm moss / warning ochre high / error rust deep / info wheat neutral

## Typography 의도
- **heading**: Fraunces 600/700 (editorial serif-ish variable) — hero-headline / featured-issue-title / testimonial-quote / pricing-tier-title / faq-question
- **body**: Inter 400/500 — 모든 본문 / pricing-description / reason-description / faq-answer / author-bio
- **mono**: JetBrains Mono 400/500 — 가격 숫자 / issue 번호 / 발행일 / 구독자 수 / 읽기 시간
- **korean (Pretendard 400/500/600/700)**: heading/body 공용 — keep-all line-height 1.6–1.7 (reading-first), headline 700 letter-spacing 0

## 접근성
- WCAG 2.2 AA 준수, Ochre/Rust 위 텍스트 대비 ≥ 4.5:1 (dark text on Wheat surface, white on Rust cta)
- 키보드 전용 네비게이션 — subscribe form / pricing toggle / faq accordion / testimonial carousel 전부 tab/enter/space 조작 가능
- 스크린리더 focus order hero → featured → archive → reasons → testimonials → pricing → author → faq → cta → footer
- prefers-reduced-motion 지원 — pulse / slide / fade 모두 축소

## 회피 패턴
- bold saturated sports hero (premier-league 영역)
- streetwear drop countdown / bold impact hero
- fintech dense data table
- SRE dark monitoring console
- playful pastel d2c product grid
- glassmorphism 과도한 장식
- corporate navy enterprise checkout

## 참고 레퍼런스
- [Stratechery](https://stratechery.com) — 독립 뉴스레터 대표 사례, 단일 강조 pricing tier
- [Ghost](https://ghost.org) — 독립 퍼블리셔 CMS, warm editorial 랜딩 + pricing + newsletter preview
- [Every](https://every.to) — 멀티 저자 뉴스레터, warm editorial hero + featured issue archive + pricing
- [Substack](https://substack.com) — 뉴스레터 플랫폼, subscribe cta + pricing 모델 참조
- [The Verge Newsletters](https://www.theverge.com/newsletters) — 대형 매체 뉴스레터 허브, issue card + category chip + subscribe form

## 결정 로그
- **editorial-warm 톤 선택 이유**: 독립 뉴스레터 · 매거진의 reading-first 감성을 유지하면서도 B2C consumer 가 아닌 "저자/출판사" 정체성을 전달하기 위함. minimal-tech 는 너무 tech 톤, bold-confident 는 너무 자극적.
- **primary Ochre Yellow 선택 이유**: 기존 editorial-warm 3 종 (signal-desk / quill / curator) 이 warm brown / marsala / aubergine 계열을 사용 — Ochre Yellow 로 노란 계열 editorial 정체성을 신규 확보하면서 동일 tone 군 내 차별화.
- **surface_tint Wheat 선택 이유 (1 겹침 허용)**: editorial-warm 톤에서 cream 계열 surface 는 serif reading paper 감성 핵심. signal-desk 의 Wheat 과 1 겹침은 editorial-warm 공통 paper 정체성으로 용인 (primary/accent 로 충분 차별화).
- **font Fraunces + Pretendard**: 영문 editorial serif-ish + 한글 Pretendard 조합으로 reading-first 확보. Pretendard-serif 가 없으므로 한글은 Pretendard 500 italic-ish fallback.
