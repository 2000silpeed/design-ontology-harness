# Orchard — D2C Craft Snack Commerce Spec (playful-soft)

## 제품 개요
Orchard 는 D2C 크래프트 스낵·음료·가벼운 웰니스 푸드를 판매하는 **playful-soft 톤 consumer commerce** 이다.
Olipop / Magic Spoon / Poppi / Graza / Caraway 계열의 **product-grid · product-card · product-detail · variant-chip ·
add-to-cart-pill · quantity-stepper · cart-drawer · cart-line-item · checkout-form · shipping-step · payment-step ·
order-summary · review-card · emoji-reaction · empty-cart · gentle-toast · soft-dialog · bottom-sheet ·
gift-message-input · subscription-toggle** 을 warm Rose Quartz primary + Dark Salmon accent + Blanched Almond cream
surface 로 엮어 "친근한 크래프트 쇼핑" 경험을 제공한다. 이 프리셋은 "streetwear 드롭 bold commerce"
(commerce--bold-confident) 도 아니고 "모바일 패션 editorial commerce"(commerce--editorial-warm) 도 아닌,
**"warm pastel craft D2C consumer commerce"** 정체성이다. 한국어 UI 를 1급으로 지원한다.

## 사용자
- **D2C 크래프트 스낵·음료 쇼핑 고객**: rounded 상품 카드에서 감각적으로 고르고 gentle checkout 으로 구매
- **기프팅·구독 박스 고객**: 정기 배송 구성 변경, 선물 메시지 입력, 친근한 카피로 "부담 없이" 선물
- **소형 D2C 브랜드 운영자**: 작은 카탈로그 + 리뷰 / emoji 반응 + soft CTA 로 브랜드 정체성 유지

## 핵심 화면
1. **Home / Storefront** — hero(부드러운 일러스트) + featured product-grid + bestseller strip + 친근 CTA + 리뷰 스니펫
2. **Shop / Category** — product-grid(2–3열, 모바일 1–2열) + soft filter-chip(flavor / diet / price) + segment-filter(bestseller / new / gift)
3. **Product Detail** — product-gallery(소프트) + product-title + variant-chip(맛/사이즈) + quantity-stepper + add-to-cart-pill + gift-message-input(선택) + subscription-toggle(선택) + review-card stack + emoji-reaction
4. **Cart Drawer / Bottom Sheet** — cart line-item + quantity-stepper + gift-message-input + order summary + gentle CTA
5. **Checkout** — step 1 배송 주소(shipping-step) + step 2 결제(payment-step) + order-summary sticky + 친근 카피
6. **Order Confirm** — soft dialog + 감사 카피 + 배송 ETA + 재구매 CTA + 리뷰 유도
7. **Subscription Manage** — 정기 구성 / 다음 배송일 / 스킵 / 변경, rounded card stack
8. **Review / Community** — review-card + emoji-reaction + 리뷰 작성 bottom-sheet
9. **Empty Cart / Empty Wishlist** — illustration + 친근 카피 ("장바구니가 비어있어요. 다른 맛도 구경해 보세요") + CTA

## UI 컴포넌트 (도출)
- **app-shell** — 상단 헤더 + 메인 + 모바일 하단 탭, rounded 12–16 surface
- **site-header** — 로고 + 검색 + 계정 + 장바구니 + 모바일 햄버거
- **topbar** — 프로모션 배너(무료배송 / 이벤트), rounded soft fill
- **mobile-tab-bar** — 홈 / 쇼핑 / 검색 / 카트 / 계정, rounded pill
- **breadcrumb** — 카테고리 경로 hierarchical, soft chevron
- **search-field** — 헤더 검색 + autocomplete, rounded
- **command-palette** — ⌘K 브랜드 내 검색(운영용, 옵션)
- **product-grid** — product-card grid (모바일 1–2, 데스크톱 2–4), gap 16–24, 스크롤 친화
- **product-card** — rounded-16 카드, 이미지 + 브랜드태그 + 상품명(Quicksand 600) + 가격(mono tabular-nums) + bestseller ribbon(Dark Salmon) + wishlist heart
- **product-gallery** — 상품 상세 이미지 carousel, rounded, dot indicator
- **product-title** — Quicksand 700 / Pretendard 700, 친근 톤
- **product-description** — body 본문, 친근 copy, emoji 혼용 자연스럽게
- **variant-chip** — rounded pill chip(맛 / 사이즈 / 색상), active Rose Quartz soft fill + Dark Salmon border
- **quantity-stepper** — − 1 + rounded buttons, mono 숫자 tabular-nums
- **add-to-cart-pill** — Rose Quartz soft fill + Quicksand 600, rounded-full, gentle hover 2% 상승
- **buy-now-button** — secondary, Dark Salmon outline, rounded-full
- **wishlist-heart** — 토글 heart 아이콘, optimistic animation, soft pop
- **bestseller-ribbon** — Dark Salmon 소프트 리본, rounded
- **discount-pill** — 할인 pill, Dark Salmon soft fill + mono 퍼센트
- **price-tag** — mono tabular-nums 가격, 할인 전/후 scrimline
- **rating-stars** — 5점 rating, rounded, warm 노란색(보조 accent variant)
- **review-card** — review body + emoji-reaction + 작성자 avatar, rounded-16
- **emoji-reaction** — 😋 👍 💛 ☺️ 리액션 버튼, soft hover
- **review-input** — 리뷰 작성 bottom-sheet, rounded textarea
- **filter-chip** — rounded pill chip, active Rose Quartz soft fill
- **filter-bar** — 상단 soft filter bar, segment-filter 통합
- **segment-filter** — bestseller / new / gift / subscribe 세그먼트 필터
- **sort-dropdown** — 정렬 드롭다운(popular / new / price), rounded select
- **pagination** — prev/next + page dot, mono tabular-nums
- **cart-drawer** — 우측 drawer(데스크톱) / bottom-sheet(모바일), rounded-top-24
- **cart-line-item** — 썸네일 + 상품명 + variant + quantity-stepper + 가격 + 삭제, soft divider
- **cart-empty** — 일러스트 + 친근 카피 + CTA
- **cart-subtotal** — 가격 mono + 쿠폰 input + 결제 CTA
- **checkout-form** — 배송 / 결제 stepper, 친근 label
- **shipping-step** — 주소 autocomplete + 배송 옵션 rounded card 선택
- **payment-step** — 결제 수단 rounded card 선택 + 카드 입력
- **order-summary** — sticky, 상품 요약 + 할인 + 합계 mono
- **promo-input** — 쿠폰 / 프로모션 코드 rounded input + apply CTA
- **gift-message-input** — 선물 메시지 textarea, 친근 placeholder ("따뜻한 한 줄을 적어보세요")
- **subscription-toggle** — 정기 구독 on/off rounded switch + 주기 dropdown
- **subscription-card** — 정기 구성 summary, 다음 배송일 + skip + 변경
- **order-confirm-dialog** — soft-dialog, 친근 감사 카피 + 배송 ETA + 재구매 CTA
- **order-status-pill** — 배송 상태(결제완료 / 출고 / 배송중 / 배송완료), soft pill
- **empty-state** — 비어있는 장바구니 / 위시리스트 / 검색 결과, 일러스트 + 친근 카피 + CTA
- **dashboard-card** — (운영용, 옵션) 소형 브랜드 운영자 소프트 대시보드
- **insight-card** — (운영용, 옵션) 매출 / 재구매 / 리뷰 인사이트
- **gentle-toast** — low-noise 성공/완료 toast, playful-soft 모션, Dark Salmon 성공
- **inline-alert** — 페이지 내 banner, rounded soft outline
- **banner** — 전역 상단 banner(무료배송 / 이벤트), rounded
- **soft-dialog** — rounded-16 dialog, 파괴적 액션도 부드럽게 confirm
- **bottom-sheet** — 모바일용 하단 sheet, rounded-top-24
- **confirm-dialog** — 삭제/위험 작업 confirm, soft danger
- **text-field** — 단일 줄 입력, rounded 12
- **textarea** — 여러 줄 입력, rounded 12
- **select** — 드롭다운 select
- **checkbox** — 체크박스
- **radio-group** — 라디오 그룹
- **form-section** — 폼 section 그룹 + label
- **form-actions** — 폼 하단 제출/취소 영역
- **avatar** — 친근 rounded avatar, illustration fallback
- **status-badge** — semantic badge(success/warning/danger/info) + soft variant
- **tag-pill** — 카테고리 rounded tag pill
- **primary-button** — Rose Quartz soft fill primary CTA, rounded-full, gentle hover 2% 상승
- **secondary-button** — Rose Quartz hairline outline, soft hover
- **ghost-button** — 텍스트 링크, soft hover underline
- **icon-button** — 아이콘 전용(heart / share / more), rounded
- **link-button** — 텍스트 링크 CTA
- **chip** — 선택/해제 rounded chip

## 인터랙션 원칙
- **gentle add-to-cart**: add-to-cart-pill 탭 시 soft-pop (150ms) + gentle-toast "장바구니에 담았어요" + 장바구니 뱃지 증가 애니메이션
- **rounded variant chip**: variant-chip 전환 시 Rose Quartz soft fill 전환 (120ms ease-out), 품절 variant 는 dim + strike-through
- **quantity-stepper optimistic**: − / + 탭 즉시 수량 반영 + 서버 반영 실패 시 soft rollback + inline-alert
- **emoji-reaction**: 리뷰에 emoji 탭 → 즉시 반영 optimistic, soft scale 1.15 → 1.0 bounce (prefers-reduced-motion 존중)
- **wishlist heart**: 토글 시 Dark Salmon pop + soft particle (reduced-motion 존중)
- **cart-drawer slide**: 장바구니 우측 slide-in(데스크톱) / bottom-sheet slide-up(모바일), 180–240ms ease-out
- **gift-message-input**: 포커스 시 rounded soft outline + 친근 placeholder 페이드
- **subscription-toggle**: switch 토글 soft fill 전환 + 주기 dropdown 자동 노출
- **checkout soft progress**: stepper 단계 전환 gentle slide + sticky order-summary 재계산 fade
- **empty-state illustration**: 친근 카피 + CTA, decorative 만 (기능 있는 text 는 별도)
- **pull-to-refresh**: 모바일 피드/리스트 상단 스와이프 → 새로고침 soft bounce
- **파괴적 액션**(장바구니 전체 삭제, 정기구독 해지)은 soft-dialog 로 부드럽게 confirm
- **이모지 혼용**: 한국어 본문 + 이모지 혼용 자연스럽게, review / gift-message 는 이모지 1급
- **전반 motion**: 120–240ms ease-out, rounded bounce 살짝, decorative animation 최소

## 색상 전략
- **warm pastel surface** — Blanched Almond 소프트 베이스 + rose highlight, 장시간 쇼핑 열람 피로감 최소
- **primary**: **Rose Quartz (#F7CAC9)** — warm pastel pink (Pantone 13-1520), primary-button / variant-chip active / add-to-cart-pill / cart-drawer header / subscription-toggle on / site-header accent
- **accent**: **Dark Salmon (#E9967A)** — warm terracotta-salmon, discount-pill / bestseller-ribbon / gentle-toast 성공 / review heart / gift-message highlight / featured product badge
- **surface_tint**: **Blanched Almond (#FFEBCD)** — cream warm near-white, product-card hover surface / cart drawer bg tint / empty-state illustration / bottom-sheet handle area / promo banner bg
- **semantic**: success(Dark Salmon soft variant) / warning(soft amber) / danger(soft coral deeper) / info(Rose Quartz variant) 4 role — gentle-toast · badge 에 매핑
- **rounded-first** — 모든 컴포넌트 corner radius 12–16, button radius full 기본, product-card radius 16, cart-drawer radius-top 24
- **soft shadow** — 0 2px 8px rgba(0,0,0,0.04) / 0 4px 12px rgba(0,0,0,0.06), 깊은 elevation 금지
- **dark mode**: warm deep neutral (not pure black) + 채도 낮춘 Rose Quartz / Dark Salmon + Blanched Almond soft border
- **bold-confident (drop) / editorial-warm (colorfit) 와 전면 차별화** — warm pink + terracotta + cream pastel, 동일 app_mode (commerce) 에서 톤 차별
- **bloom (community-feed--playful-soft) / meadow (dashboard--playful-soft) 와도 HEX 겹침 0** — 동일 brand_tone (playful-soft) 에서 app_mode 차별
- **기존 17종 프리셋 HEX 와 겹침 0** — Rose Quartz #F7CAC9 / Dark Salmon #E9967A / Blanched Almond #FFEBCD 조합

## 타이포그래피
- **heading**: **Quicksand** (영문, rounded sans) / **Pretendard** (한글) — geometric impact 금지, serif 금지, page-title / product-title / section-header / add-to-cart-pill / price headline
- **body**: **Inter / Pretendard** — product-description / review / cart line / checkout label / filter-chip 본문, line-height 1.5–1.6 (commerce soft) / ko 1.6
- **mono**: **JetBrains Mono** — price / discount / quantity / order number / shipping ETA, tabular-nums 영문 고정, 최소 사용
- **scale**: xs(12) / sm(13) / md(14) / lg(16) / xl(20) / 2xl(24) / 3xl(32) / 4xl(40)
- **page-title**: 2xl–3xl (24–32px), Quicksand 700, letter-spacing 0
- **product-title (card)**: lg–xl (16–20px), Quicksand 600
- **product-title (detail)**: 2xl–3xl (24–32px), Quicksand 700
- **section-header**: xl–2xl (20–24px), Quicksand 700
- **price headline**: xl–2xl (20–24px), Quicksand 700 mono tabular-nums
- **price (card)**: md–lg (14–16px), mono 500 tabular-nums
- **review body**: sm–md (13–14px), body 400–500, line-height 1.6 keep-all
- **filter-chip**: xs–sm (12–13px), body 500 rounded pill
- **add-to-cart-pill**: md–lg (14–16px), Quicksand 600
- **한글 line-height**: 1.5 (product-card dense), 1.6 (product-description / review / checkout / gift-message), keep-all
- **tabular-nums**: price / discount / quantity / order-number / shipping-eta / rating count 전용
- **rounded warmth** — page-title / product-title / section-header 는 Quicksand 700 letter-spacing 0 (impact 대신 warmth)

## 접근성
- WCAG 2.2 AA (본문 대비 4.5:1, UI 3:1)
- Rose Quartz 위 텍스트는 near-black (파스텔 위 어두운 글자), 짙은 primary-button 은 white 텍스트 4.5:1 확보
- Dark Salmon 위 텍스트는 near-black (파스텔 위 어두운 글자)
- add-to-cart-pill focus 는 Dark Salmon outline + 2px offset (키보드 가시성)
- variant-chip 은 색 단독 금지 — 맛/사이즈 텍스트 라벨 + 품절 시 텍스트 명시
- quantity-stepper 는 −/+ 버튼에 aria-label + 숫자 textfield role="spinbutton"
- wishlist-heart 는 aria-pressed + 텍스트 대체 ("위시리스트에 추가됨")
- review-card emoji-reaction 은 role="group" + 각 버튼 aria-label 텍스트
- cart-drawer 는 focus trap + ESC 닫기
- soft-dialog 는 focus trap + ESC 취소
- gentle-toast 는 aria-live="polite"
- prefers-reduced-motion 존중 — add-to-cart pop, wishlist particle, emoji bounce 제거
- subscription-toggle 은 role="switch" + aria-checked
- gift-message-input 은 글자 수 카운터 + 한도 안내 aria-describedby

## 한글 대응
- Pretendard variable (woff2) 번들, heading(보조) / body 공용
- 한글 product-title / product-description / review / cart-line / checkout-label / filter-chip line-height **1.5–1.6**, letter-spacing 0
- page-title / section-header 는 Pretendard 700 letter-spacing 0 (rounded warmth)
- word-break: **keep-all**, overflow-wrap: break-word
- price / discount / quantity / order-number / shipping-eta 는 mono 영문 고정(한글 혼용 금지), tabular-nums
- 한국어 라벨: "상품 / 맛 / 사이즈 / 장바구니 / 결제 / 배송 / 정기구독 / 선물 메시지 / 리뷰" + 영문 "product / flavor / size / cart / checkout / shipping / subscription / gift / review" 병기 허용
- 친근 카피 톤: "장바구니에 담았어요" / "맛있는 하루 되세요" / "따뜻한 한 줄을 적어보세요" (enterprise 어휘 회피)

## 참고 (참고 레퍼런스 — public D2C craft)
- [Olipop](https://drinkolipop.com) — warm pastel 프리바이오틱 소다 D2C 스토어프론트
- [Magic Spoon](https://magicspoon.com) — rounded D2C 시리얼 + 친근 copy
- [Poppi](https://drinkpoppi.com) — 프리바이오틱 소다 rounded subscription
- [Graza](https://graza.co) — craft olive oil, 친근 D2C
- [Caraway](https://www.caraway.com) — warm pastel cookware D2C

## 주의사항
- 이 프리셋은 **commerce--playful-soft (P3)** — D2C 크래프트 스낵/음료/컨슈머 상품 특화
- "streetwear 드롭 bold commerce" 는 `commerce--bold-confident`
- "모바일 패션 editorial 커머스" 는 `commerce--editorial-warm`
- "consumer wellness habit admin" 은 `dashboard--playful-soft` (Meadow) — 운영/관리자용이며 쇼핑이 아님
- "친근 소셜 피드·쓰레드·알림" 은 `community-feed--playful-soft` (Bloom)
- 이미지 기반 힌트는 advisory — 구조는 spec + KB 우선
- 실제 백엔드(auth / order / payment / shipping / subscription engine) 는 프리셋 범위 외 — commerce chrome + visual system 만 다룸
