# Broadside — Bold-Confident Magazine/Opinion Spec

## 제품 개요
Broadside 는 정치·사회 opinion 저널 / bold 컬처·음악·영화 리뷰 매거진 /
declaration/manifesto 단일호 zine 을 위한 **bold-confident 톤 document-content
(문서/콘텐츠/레퍼런스 — long-form reading)** 이다.
The Atlantic / New Yorker / NY Times Magazine / Vice / Pitchfork / Guardian Long Read
계열의 **masthead · issue-header · issue-number · cover-story · opening-spread ·
kicker-eyebrow · feature-article · article-body · article-gallery · pull-quote ·
drop-cap · section-break · subscription-callout · table-of-contents ·
heading-anchor · footnote · reading-pane · prose-block · opinion-byline ·
manifesto-section · feature-grid-index · archive-index · issue-archive ·
reading-progress-bar** 를 한 시스템으로 묶어 "표지 → 이슈 TOC → 피처
article → opinion 코너 → 아카이브" 의 bold editorial reading flow 를 제공한다.
이 프리셋은 "editorial-warm 차분 매거진" 이나 "minimal reference docs" 가 아니라
**"saturated bold magazine / opinion feature / manifesto zine"** 성향으로,
saturated primary masthead · high-contrast cover · impact headline typography ·
oversized kicker eyebrow · full-bleed feature spread · bold pull-quote block ·
chunky divider rule · editorial number-heavy TOC · opinionated long-form spread 를
시각 정체성으로 고정한다. 한국어 UI 를 1급으로 지원한다.

## 사용자
- **정치·사회 opinion 저널 독자**: The Atlantic / New Yorker 성향 — cover-story + opinion-byline + manifesto-section + reading-progress-bar 중심 long-form article 체류
- **bold 컬처/음악/영화 리뷰 매거진 reader**: Pitchfork / Vice 성향 — feature-grid-index + article-gallery + pull-quote + drop-cap 이 돋보이는 feature-article 순례
- **manifesto/zine 구독자**: Gen Z 젊은 에디토리얼 — masthead + issue-header + issue-number + subscription-callout 중심 single-issue 탐독

## 핵심 화면
1. **Issue Cover** — masthead + issue-header + issue-number + cover-story hero + kicker-eyebrow + table-of-contents 진입 + feature-grid-index 미리보기
2. **Feature Article** — opening-spread + article-body + drop-cap + prose-block + pull-quote + byline + heading-anchor + footnote + section-break + article-gallery + reading-progress-bar
3. **Opinion / Manifesto** — manifesto-section + opinion-byline + feature-grid-index + reading-progress-bar + bold callout + subscription-callout
4. **Table of Contents** — table-of-contents + feature-grid-index + archive-index 진입 + issue-archive 링크
5. **Reading Flow** — article-gallery + reading-pane + heading-anchor + footnote + pull-quote + paragraph-block + prose-block
6. **Subscription** — subscription-callout + primary CTA + 이슈별 구독 혜택 안내
7. **Archive Index** — archive-index + issue-archive + issue-header list + issue-number 기반 연/호 필터

## UI 컴포넌트 (도출)
- **masthead** — 제호(로고 타이포) · 이슈 번호 · 발행일 · 표지 링크를 모은 sticky masthead (saturated Electric Blue primary + 한글 Pretendard 900 heading)
- **issue-header** — 현재 이슈 권/호 · 발행일 · 주요 섹션 jump · kicker-eyebrow, 상단 full-bleed 또는 sticky
- **issue-number** — issue 번호 칩 (mono tabular-nums · Flame surface accent)
- **cover-story** — 표지 대표 feature — full-bleed hero image + kicker-eyebrow + impact headline + pull-quote preview + byline
- **opening-spread** — 기사 opening spread — 큰 여백 · drop-cap 시작 · pull-quote · 번호 섹션 break
- **feature-article** — feature article 본체 래퍼 — article-body + prose-block + pull-quote + drop-cap + section-break + article-gallery
- **kicker-eyebrow** — 기사 kicker / eyebrow (섹션 · 카테고리 · 이슈 라벨, letter-spacing tight, Flame accent)
- **cover-headline** — 표지 · 오프닝 headline (Playfair Display 900 / 한글 Pretendard 900, impact)
- **feature-subhead** — 기사 서브 헤드라인 (serif 700 + 한글 Pretendard 700)
- **article-body** — long-form article 본체 — prose-block + drop-cap + pull-quote + heading-anchor + footnote 를 품는 reading-first container (reading-pane 65–75ch 측정, line-height 1.5–1.7)
- **prose-block** — long-form prose reading block — 본문 문단 · list · blockquote (paragraph-block 집합, reading-pane 폭)
- **paragraph-block** — 본문 문단 블록 (reading-pane line-height 1.5–1.7)
- **pull-quote** — bold pull quote (oversized Playfair serif / 한글 Pretendard 900, Goji Berry vertical rule, 전 폭 또는 column 옆)
- **drop-cap** — 기사 첫 문단 drop cap initial letter (3–4 line, Goji Berry 또는 Flame accent)
- **byline** — 기사 byline row — 필자 이름 + 직함 + 발행일 + 읽기 시간, mono attribution
- **opinion-byline** — opinion 필자 byline — 사진 + 이름 + 직함 + SNS + manifesto tagline (bold variant)
- **credit-line** — 기사 하단 credit line — 사진/일러스트/에디터 크레딧 (mono, xs–sm)
- **section-break** — article 내 section-break — chunky divider rule + ornament glyph, Goji Berry line
- **callout** — inline callout (info/warning/tip/danger), 한글 본문과 시각적으로 분리
- **article-gallery** — 기사 내 이미지 갤러리 — full-bleed / caption / credit-line, 키보드 prev/next
- **heading-anchor** — h1~h6 heading 의 #id anchor — copy link, hover 시 Flame underline
- **footnote** — 기사 내 numbered footnote — mono 번호 + 본문 pop, 클릭 시 article 하단 footnote shelf 로 scroll-to
- **reading-pane** — article-body 의 main reading column — measured width 65–75ch, reading-first line-height
- **table-of-contents** — issue TOC — number-heavy tile · kicker-eyebrow · title · byline, 섹션 jump / heading-anchor 연계
- **feature-grid-index** — issue feature 그리드 인덱스 — large feature tile + number + title + byline + kicker-eyebrow
- **archive-index** — 전체 아카이브 인덱스 — year/issue 필터 + cover thumbnail + issue-number list
- **issue-archive** — 과거 이슈 아카이브 — cover thumbnail + issue-number + 발행일 + feature count
- **manifesto-section** — manifesto / declaration 섹션 — bold declaration 문단 + saturated accent surface + oversized serif
- **subscription-callout** — 구독 유도 callout — bold offer copy + primary CTA, article 하단 또는 sidebar
- **reading-progress-bar** — article 상단 reading progress bar — scroll-based, Goji Berry fill
- **primary-button** — saturated Electric Blue primary CTA (subscribe / read / share) — impact label
- **secondary-button** — ghost secondary CTA (save / archive) — hairline border
- **ghost-button** — 텍스트 링크형 tertiary
- **icon-button** — 아이콘 전용 (share / save / print)
- **toast** — 저장됨 / 구독됨 gentle toast (bold entry, 빠른 fade-out)
- **modal-dialog** — subscription / share modal
- **search-field** — article / issue / 필자 검색 (bold bordered)
- **autocomplete** — 검색 / 필자 / 이슈 autocomplete dropdown

## 인터랙션 원칙
- **bold entry hero reveal**: cover-story / opening-spread 진입 시 headline fade-in 150ms + kicker-eyebrow letter-spacing 확장 (prefers-reduced-motion 시 off)
- **sticky masthead scroll**: article reading 중 masthead 는 scroll 시 축소 sticky, issue-number 유지
- **pull-quote magnification**: pull-quote 는 뷰포트 중앙 진입 시 scale 1.02 + Goji Berry rule 강조 (prefers-reduced-motion 시 off)
- **section jump TOC**: table-of-contents 에서 heading-anchor 로 smooth scroll (native scroll-behavior)
- **feature scroll-snap**: feature-grid-index 의 타일은 큰 화면에서 scroll-snap 으로 탐색, 모바일은 stack
- **impact cover transition**: 다음 기사 진입 시 flash-to-next transition (150ms), motion-reduced 모드 존중
- **reading progress bar**: article-body scroll 위치 기반 Goji Berry fill, footnote 영역 도달 시 완료
- **footnote flash highlight**: footnote 번호 클릭 시 대상 footnote 행 Flame flash (short, reduce-motion 시 flash 대신 outline)
- **masthead focus ring bold**: 키보드 focus 시 Electric Blue 2px outline + 2px offset (masthead / issue-header / CTA)
- **bold share overlay**: share 버튼 → modal-dialog saturated primary overlay, ESC 닫힘
- **impact motion**: 전반 150–220ms ease-out-expo (bold-confident 에너제틱 모션), prefers-reduced-motion 존중
- **bold hover**: 버튼 hover 시 색상 강화 + 1–2px 상승 + Goji Berry underline

## 색상 전략
- **primary**: **Electric Blue (#7DF9FF)** — saturated high-voltage blue, masthead / cover-story hero / feature-article headline impact 라인 / primary-button / reading-progress-bar fill 변형
- **accent**: **Goji Berry (#C23B22)** — Pantone Trend 짙은 구기자 적색, pull-quote vertical rule / drop-cap / section-break ornament / opinion-byline accent / subscription-callout CTA fill / reading-progress-bar fill
- **surface_tint**: **Flame (#E25822)** — 밝은 불꽃 오렌지, kicker-eyebrow / issue-number chip / footnote flash / manifesto-section surface pop
- **semantic**: success(구독 완료) / warning(베타) / danger(에러) / info(이슈 안내) 4 role
- **saturated primary masthead** — masthead 는 Electric Blue primary + 한글 Pretendard 900 impact
- **high-contrast cover** — cover-story 는 near-black headline + saturated accent, 중간 muted 톤 금지
- **impact headline typography** — headline 은 Playfair Display 900 / 한글 Pretendard 900, letter-spacing tight
- **oversized kicker eyebrow** — kicker-eyebrow 는 크고 letter-spacing 확장, uppercase 또는 한글 bold
- **full-bleed feature spread** — opening-spread 는 full-bleed image + drop-cap + pull-quote 조합
- **bold pull-quote block** — pull-quote 는 oversized serif + Goji Berry vertical rule, article 흐름 강제 전환
- **chunky divider rule** — section-break 은 굵은 divider rule + ornament glyph (hairline 금지)
- **editorial number-heavy TOC** — table-of-contents / feature-grid-index 는 large number + kicker + title + byline
- **opinionated long-form spread** — opinion / manifesto 섹션은 bold declaration 문단 + accent surface
- **dark mode**: deep cool black surface + tuned Electric Blue/Goji Berry 채도 낮춤, paragraph/prose 는 near-white 로 대비 확보
- **기존 13종 프리셋 HEX 와 HEX 겹침 0**

## 타이포그래피
- **heading**: **Playfair Display** (영문) / **Pretendard** (한글) — bold-confident magazine display serif — masthead / cover-story headline / feature-article h1 / pull-quote, Lora (signal-desk) 및 Source Serif Pro (quill) 와 차별화, 한글은 Pretendard 900 letter-spacing tight
- **body**: **Inter / Pretendard** — article-body / prose-block / paragraph-block / outline / subscription-callout, line-height 1.5–1.7 (long-form reading-first)
- **mono**: **JetBrains Mono** — issue-number / credit-line / byline attribution / citation footnote number / reading-progress % / tabular-nums 영문 고정
- **scale**: xs(11) / sm(12) / md(14) / lg(16) / xl(18) / 2xl(24) / 3xl(32) / 4xl(48) / 5xl(64) / 6xl(80)
- **masthead / cover headline**: 5xl–6xl (64–80px), heading 900 serif, letter-spacing tight, impact
- **feature-article h1**: 4xl (48px), heading 700 serif
- **opening-spread drop-cap**: 6xl (80px) leading-none, heading 900, 3–4 line initial letter
- **pull-quote**: 2xl–3xl (24–32px), heading 700 serif italic 또는 한글 Pretendard 900
- **kicker-eyebrow**: sm–md (12–14px), heading 600 letter-spacing 0.12em uppercase 또는 한글 bold
- **article-body paragraph**: lg (16px), body 400, line-height 1.7 reading-mode
- **prose-block list / blockquote**: md–lg (14–16px)
- **byline / opinion-byline**: sm (12px) body 500 + mono attribution
- **footnote**: sm (12px) body 400 + mono number tabular-nums
- **credit-line**: xs (11px) mono tabular-nums
- **issue-number**: sm–md (12–14px) mono tabular-nums 600
- **reading-progress %**: xs (11px) mono tabular-nums
- **한글 line-height**: 1.5 (masthead · cover headline · pull-quote · feature-subhead), 1.6–1.7 (article-body · prose-block · paragraph-block, long-form reading-first), keep-all
- **tabular-nums**: issue-number / credit-line / footnote number / reading-progress / byline 발행일 전용
- **impact letter-spacing** — 영문 masthead/headline 은 tight (-0.02em~-0.04em), 한글은 letter-spacing 0

## 접근성
- WCAG 2.2 AA (본문 대비 4.5:1, UI 3:1, saturated primary 위 텍스트는 near-white 또는 near-black 확보)
- masthead / issue-header 는 role="banner" + aria-label="매거진 제호"
- table-of-contents 는 role="navigation" + aria-label="이슈 목차"
- article-body 는 role="article" + aria-labelledby=feature-article h1
- reading-pane 은 role="main"
- heading-anchor 는 키보드 focus 가능 + aria-label="링크 복사"
- pull-quote 는 role="blockquote" + cite 속성 (발화자 있을 때)
- footnote 는 aria-describedby 로 본문 anchor 연결, tap 시 footnote shelf focus
- reading-progress-bar 는 role="progressbar" + aria-valuemin/max/now
- subscription-callout CTA 는 aria-describedby 로 혜택 안내 연결
- article-gallery 는 키보드 좌/우 thumbnail 네비 + alt 필수
- manifesto-section 은 role="region" + aria-label 로 섹션 구분
- modal-dialog 는 role="dialog" + aria-modal + focus trap + ESC 닫힘
- prefers-reduced-motion 존중 — hero reveal / pull-quote magnification / footnote flash / impact transition 애니메이션 제거

## 한글 대응
- Pretendard variable (woff2) 번들, body/heading 공용, heading 은 Pretendard 900 letter-spacing tight
- 한글 article-body / prose-block / paragraph-block line-height **1.6–1.7**, reading-first, keep-all
- 한글 masthead / cover headline / pull-quote line-height **1.4–1.5**, letter-spacing 0, keep-all
- word-break: **keep-all**, overflow-wrap: break-word
- issue-number / credit-line / footnote number / reading-progress / 발행일 숫자 는 mono 영문 고정 (한글 혼용 금지), tabular-nums
- 한국어 라벨: "이슈 / 호 / 표지 기사 / 피처 / 오피니언 / 선언 / 아카이브 / 구독 / 인용 / 주석" + 영문 "issue / cover story / feature / opinion / manifesto / archive / subscribe / pull-quote / footnote" 병기 허용
- masthead 제호는 한글 Pretendard 900 bold impact 사용 가능 (로고 타이포 직접 제작 시 대체)

## 주의사항
- 이 프리셋은 **document-content--bold-confident (P2)** — bold-confident 톤 magazine/opinion long-form 특화
- "차분한 에디토리얼 매거진 / 에세이 블로그" 는 `document-content--editorial-warm`
- "개발자 API 레퍼런스 · 기술 문서" 는 `document-content--minimal-tech`
- "대담 스포츠 랜딩 페이지" 는 `marketing-landing--bold-confident`
- "스트리트웨어 드롭 커머스 bold" 는 `commerce--bold-confident`
- "fashion editorial commerce" 는 `commerce--editorial-warm`
- "B2B SaaS 마케팅 랜딩 미니멀" 은 `marketing-landing--minimal-tech`
- "AI 글쓰기 코파일럿 차분 editorial" 은 `conversation-copilot--editorial-warm`
- "일반 AI 챗봇 미니멀" 은 `conversation-copilot--minimal-tech`
- "fintech 대시보드 신뢰" 는 `dashboard--corporate-trust`
- "일반 SaaS 대시보드" 는 `dashboard--minimal-tech`
- "SRE / observability 모니터링" 은 `monitoring-ops--minimal-tech`
- "소셜 피드 친근" 은 `community-feed--playful-soft`
- "캔버스 · 디자인 도구" 는 `canvas-tool--minimal-tech`
- 이미지 기반 힌트는 advisory, 구조적 결정은 spec + KB 우선
- 실제 CMS / editorial 워크플로우 백엔드 / 구독 결제 게이트웨이는 프리셋 범위 외 — magazine chrome 만 다룸
