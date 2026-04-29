# Drop — B2C Bold-Confident Commerce Spec

## 제품 개요
Drop 은 젊은 B2C 소비자 (스트리트웨어 / 스니커 드롭 / 게이밍 머천다이즈 / bold beauty / 스포츠 굿즈)
를 타깃으로 하는 **bold-confident 톤 commerce (커머스/쇼핑)** 이다.
Nike / Supreme / Kith / Ssense / Musinsa / 29cm 계열의 **drop banner · countdown timer +
product grid · product detail · product gallery · variant/size selector +
cart drawer · cart item · quantity stepper · cart summary +
checkout step · address form · payment form · promo code input · order summary** 를
일관된 한 브랜드로 묶어 "드롭 기다림 → 발견 → 구매"의 흥분을 전달한다.
이 프리셋은 "에디토리얼 패션 매거진"이나 "차분한 B2B SaaS 랜딩"이 아니라
**"saturated streetwear drop commerce"** 성향으로,
saturated primary hero · high-contrast headline · dense product grid · impact typography ·
purple accent callout · full-bleed drop banner · bold price tag · countdown timer chip 를
시각 정체성으로 고정한다. 한국어 UI 를 1급으로 지원한다.

## 사용자
- **스트리트웨어/스니커 드롭 팬**: Gen Z / 밀레니얼 — drop banner + countdown + 제품 그리드 + add-to-cart
- **게이밍/e스포츠 머천다이즈 소비자**: 한정판 머치 드롭 + variant selector + size selector 반복 구매
- **bold beauty · 스포츠 굿즈 모바일 쇼핑 사용자**: 모바일 product detail + cart drawer + checkout step 전환

## 핵심 화면
1. **Home / Drop** — site header + hero drop banner + countdown timer + featured drop grid + category pill row
2. **Product Listing (제품 그리드)** — category pill + filter sidebar + sort dropdown + product grid + product card + pagination
3. **Product Detail (제품 상세)** — breadcrumb + product gallery + image thumbnail + product title + price tag + discount badge + variant selector + size selector + color swatch selector + add-to-cart button + wishlist toggle + cross-sell product grid
4. **Cart Drawer (장바구니)** — cart drawer + cart item + quantity stepper + cart summary + promo code input + checkout CTA + empty cart state
5. **Checkout (체크아웃)** — checkout step progress + address form + payment form + promo code input + order summary + place-order CTA
6. **Account / Wishlist** — wishlist toggle grid + order history list + address book
7. **Site Footer** — site footer + footer column + footer link + footer legal + footer social

## UI 컴포넌트 (도출)
- **site-header** — sticky site header, drop 로고 + category nav + search bar + cart icon + wishlist icon
- **site-logo** — 드롭 브랜드 로고
- **site-nav** — 주요 카테고리 내비게이션 (New Drop / 의류 / 신발 / 액세서리 / Sale)
- **search-bar** — commerce 검색 입력, keyword / 제품명 / SKU, autocomplete dropdown
- **cart-icon** — 헤더 우측 cart 아이콘 (수량 배지)
- **wishlist-icon** — 헤더 우측 wishlist 아이콘
- **mobile-menu-trigger** — 모바일 햄버거 메뉴
- **hero-banner** — full-bleed drop banner, saturated primary (Crimson) surface, large product hero image
- **drop-banner** — hero drop 전용 banner — drop name + countdown + CTA + impact typography
- **countdown-timer** — drop countdown timer chip (D-day / H / M / S, mono tabular-nums, 퍼플 accent)
- **category-pill** — 카테고리 필터 pill row (New / 의류 / 신발 / 액세서리 / Sale)
- **featured-category-tile** — 홈 featured category tile (large product image + category label)
- **lookbook-hero** — 에디토리얼 lookbook tile (full-bleed image + overlay copy)
- **product-grid** — dense product grid 2×3 (mobile) ~ 4×N (desktop), hairline gap
- **product-card** — 개별 product card — thumbnail + product title + price tag + discount badge + quick-view trigger
- **image-thumbnail** — 제품 썸네일 이미지, aspect-ratio fixed, hover zoom
- **product-title** — product 제목, heading 600, 한글 Pretendard keep-all
- **price-tag** — bold price tag (mono tabular-nums), 한정판은 Crimson 강조
- **original-price-strikethrough** — 할인 시 원가 strikethrough (muted mono)
- **discount-badge** — 할인율 badge (mono -NN% / SALE / HOT / DROP 라벨)
- **quick-view-modal** — 제품 grid 위에서 뜨는 quick-view modal (product gallery 축소판 + 주요 variant + add-to-cart)
- **wishlist-toggle** — heart toggle (Royal Purple accent, optimistic update)
- **product-gallery** — 제품 상세 gallery, 메인 이미지 + thumbnail rail, swipe/keyboard 지원
- **product-hero-image** — large product hero image (제품 상세 상단 full-bleed)
- **variant-selector** — variant (색상/사이즈/모델) 선택기 — segmented chip group
- **size-selector** — size selector chip (S / M / L / XL / 숫자), 품절 state
- **color-swatch-selector** — color swatch chip, 선택 ring 강조
- **add-to-cart-button** — primary CTA, saturated Crimson fill + impact label, add-to-cart animation
- **breadcrumb** — 카테고리 계층 breadcrumb
- **cross-sell-grid** — 제품 상세 하단 추천 product grid (함께 구매 / 비슷한 상품)
- **cart-drawer** — cart drawer slide-in (우측에서 슬라이드), backdrop dim
- **cart-item** — 장바구니 상품 (thumbnail + 제품 title + variant + price + quantity stepper + 삭제)
- **quantity-stepper** — quantity stepper (- / n / +, mono tabular-nums)
- **cart-summary** — cart summary (소계 + 배송비 + 할인 + 총액, mono tabular-nums)
- **promo-code-input** — promo code input + apply 버튼 + flash feedback (성공/실패)
- **checkout-step** — checkout step progress (배송 → 결제 → 확인, stepper + active/완료/대기)
- **checkout-step-progress** — 상단 step indicator bar
- **address-form** — 배송지 form (수령인 / 전화 / 주소 / 요청사항)
- **payment-form** — 결제 form (카드 / 간편결제 / 무통장 선택 + 카드 입력)
- **order-summary** — 주문 요약 (cart item 축소 + 배송비 + 할인 + 총액)
- **empty-cart-state** — empty cart 안내 illustration + "계속 쇼핑하기" CTA
- **filter-sidebar** — 카테고리/가격/브랜드/사이즈/색상 필터 사이드바
- **sort-dropdown** — 정렬 dropdown (신상품 / 인기순 / 가격 낮은순 / 가격 높은순)
- **pagination** — 페이지 네비게이션 (prev / 1 2 3 / next), infinite scroll fallback
- **primary-button** — saturated Crimson primary CTA (add-to-cart / 구매하기 / 결제하기), bold label
- **secondary-button** — ghost secondary CTA (계속 쇼핑 / 취소), hairline border
- **ghost-button** — tertiary ghost (텍스트 링크 스타일 액션)
- **icon-button** — 아이콘 전용 버튼 (wishlist heart / share)
- **toast** — 일시적 add-to-cart / promo 성공/실패 toast, impact entry
- **modal-dialog** — 확인 / 삭제 / 사이즈 가이드 modal
- **site-footer** — 사이트 전역 하단 컨테이너
- **footer-column** — 링크 그룹 컬럼 (Shop / Help / Brand / Legal)
- **footer-link** — 개별 링크
- **footer-legal** — 저작권 · 통신판매업 고지
- **footer-social** — 소셜 링크 아이콘 그룹

## 인터랙션 원칙
- **add-to-cart animation**: add-to-cart 클릭 시 상품 이미지가 헤더 cart 아이콘으로 parabolic 이동 + 수량 badge bump
- **quick-view modal**: product grid 에서 quick-view 아이콘 클릭 시 modal 오픈 (scroll lock, ESC 닫힘)
- **size selector chip**: size chip tap 시 selected ring 강조, 품절 사이즈는 disabled + 취소선
- **wishlist toggle heart**: heart 아이콘 tap 시 fill 전환 (Royal Purple accent) + optimistic update, 실패 시 reset
- **drop countdown timer**: mono tabular-nums 로 D-H-M-S 표시, 0 도달 시 hero banner state 전환 (pre → live)
- **quantity stepper**: -/+ 버튼 + 직접 입력, 재고 한도 clamp + debounce
- **cart drawer slide-in**: 우측에서 280–360px drawer 슬라이드, backdrop dim, ESC/backdrop tap 닫힘
- **checkout step progress**: active step saturated Crimson fill, 완료 step check 아이콘 + 클릭으로 back-step 가능
- **promo code input flash**: 적용 성공 시 총액 숫자 tabular-nums 숫자 카운트 애니메이션 + green flash, 실패 시 shake
- **hero scroll-snap banner**: hero drop 배너는 scroll-snap 으로 이전/다음 drop 로테이션, motion-reduced 모드 존중
- **impact motion**: 전반 150–220ms ease-out-expo (bold-confident 특유 에너제틱 모션), prefers-reduced-motion 존중
- **bold hover**: 버튼 hover 는 색상 강화 + 1–2px 상승, 그림자 강조

## 색상 전략
- **primary**: **Crimson (#BD2E4A)** — saturated blood red, drop banner / add-to-cart primary-button / price tag(세일) / checkout-step active / toast 성공
- **accent**: **Royal Purple (#6C3BAA)** — bold vivid purple, countdown-timer / drop label / wishlist heart / secondary CTA focus / discount-badge
- **surface_tint**: **Buttercream (#F3E5AB)** — warm cream surface, hero 보조 surface / featured category tile background / empty cart state / lookbook-hero 오버레이 대비 surface
- **semantic**: success(할인 적용) / warning(재고 임박) / danger(품절/에러) / info(배송 안내) 4 role
- **high-contrast headline** — 헤드라인은 near-black + saturated Crimson accent, hairline 차분한 톤 금지
- **dense product grid** — 제품 카드 간 gap 은 hairline 보다 약간 넓은 commerce dense (8–12px)
- **full-bleed drop banner** — hero banner 는 full-bleed, saturated primary 가 방문 즉시 임팩트
- **bold price tag** — price tag 는 heading 600 mono tabular-nums, 세일가는 Crimson 강조 + 원가 strikethrough
- **countdown timer chip** — countdown 은 Royal Purple chip + mono tabular-nums
- **dark mode**: deep cool neutral black surface + tuned Crimson/Royal Purple 채도 낮춤, product image 는 원본 유지
- **기존 11종 프리셋 HEX (#E90052 / #00FF85 / #FFD700 / #01889F / #DAA520 / #B0E0E6 / #000080 / #007FFF / #5A4FCF / #804AA8 / #F88379 / #003153 등) 와 HEX 겹침 0**

## 타이포그래피
- **heading**: **Space Grotesk** (영문) / **Pretendard** (한글) — geometric sans with impact, drop banner / hero headline / product title / price tag, serif 금지
- **body**: **Inter / Pretendard** — product description / cart item / checkout step / filter label, line-height 1.4–1.5 (commerce dense)
- **mono**: **JetBrains Mono** — price / original price / discount percent / countdown timer / quantity / order total — tabular-nums 영문 고정
- **scale**: xs(11) / sm(12) / md(14) / lg(16) / xl(18) / 2xl(24) / 3xl(32) / 4xl(48) / 5xl(64)
- **hero drop banner**: 4xl–5xl (48–64px), heading 700, letter-spacing tight, impact
- **product title (그리드)**: md–lg (14–16px), heading 600
- **product title (상세)**: 2xl–3xl (24–32px), heading 700
- **price tag**: lg–xl (16–18px) mono tabular-nums 700, 세일가는 Crimson
- **discount badge**: xs–sm (11–12px) mono tabular-nums 600
- **countdown timer**: xl–2xl (18–24px) mono tabular-nums 600
- **cart item title**: md (14px) body 500, 한글 keep-all line-height 1.4
- **checkout step label**: sm–md (12–14px) heading 600
- **한글 line-height**: 1.4 (product grid / cart dense), 1.5 (product detail 본문), keep-all
- **tabular-nums**: price / original price / discount percent / quantity / cart summary / countdown 전용
- **impact headline** — drop banner 는 letter-spacing 약간 tight, 한글은 letter-spacing 0

## 접근성
- WCAG 2.2 AA (본문 대비 4.5:1, UI 3:1, saturated primary 위 텍스트는 화이트로 대비 확보)
- add-to-cart-button focus 는 Royal Purple outline + 2px offset (키보드 가시성)
- size-selector / color-swatch-selector 는 role="radiogroup", 각 chip role="radio" + aria-checked
- quantity-stepper 는 aria-label="수량" + 증감 버튼 aria-label
- cart-drawer 는 role="dialog" + aria-modal + focus trap + ESC 닫힘
- checkout-step-progress 는 role="progressbar" + aria-valuenow
- product-gallery 는 키보드 좌/우 thumbnail 네비, alt 필수
- promo-code-input 은 aria-live="polite" 로 성공/실패 피드백
- countdown-timer 는 aria-live="off" + 시각 외 텍스트 대체 (예: "3일 남음")
- wishlist-toggle 은 aria-pressed, 색상만이 아닌 icon shape 변화로도 상태 구분
- prefers-reduced-motion 존중 — add-to-cart parabolic, drawer slide, scroll-snap, flash shake 제거
- mobile-menu-trigger 는 aria-expanded + focus trap

## 한글 대응
- Pretendard variable (woff2) 번들, heading/body 공용
- 한글 drop banner / product title line-height **1.4–1.5**, letter-spacing 0
- 한글 cart item / checkout / footer legal line-height **1.5**
- word-break: **keep-all**, overflow-wrap: break-word
- price / original price / discount percent / quantity / order total 은 mono 영문 고정 (한글 혼용 금지), tabular-nums
- 한국어 라벨: "장바구니 / 결제하기 / 배송지 / 주문 요약 / 프로모 코드 / 재고 임박 / 품절 / 드롭 알림" + 영문 "cart / checkout / shipping / order summary / promo code / low stock / sold out / drop notify" 병기 허용
- add-to-cart CTA 는 "장바구니 담기 (Add to cart)" 형태의 이중 표기 허용

## 주의사항
- 이 프리셋은 **commerce--bold-confident (P2)** — 젊은 B2C 스트리트웨어/드롭 커머스 특화
- "편안한 에디토리얼 패션 커머스" 는 `commerce--editorial-warm`
- "대담 스포츠 랜딩 (제품 판매 아님)" 은 `marketing-landing--bold-confident`
- "차분한 B2B SaaS 랜딩" 은 `marketing-landing--minimal-tech`
- "관리 대시보드" 는 `dashboard--minimal-tech`
- "API 레퍼런스" 는 `document-content--minimal-tech`
- "AI 코파일럿 채팅" 은 `conversation-copilot--minimal-tech`
- "캔버스 · 디자인 도구" 는 `canvas-tool--minimal-tech`
- "소셜 피드" 는 `community-feed--playful-soft`
- 이미지 기반 힌트는 advisory, 구조적 결정은 spec + KB 우선
- 실제 결제 게이트웨이 / 재고 관리 / 주문 관리 백엔드 (Stripe / PG / ERP) 는 프리셋 범위 외 — commerce chrome 만 다룸
