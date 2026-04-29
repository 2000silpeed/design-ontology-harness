# Lattice — 개발자 API 레퍼런스 · 기술 문서 플랫폼 Spec

## 제품 개요
Lattice 는 개발자를 위한 **minimal-tech 톤 API 레퍼런스 · 기술 문서 플랫폼**이다.
Linear Docs / Stripe Docs / Vercel Docs / MDN 계열의 **reference documentation** 을 지향하며,
**article body + table of contents + code block + api reference table + callout** 을 한 페이지에서
정밀하게 조합해 개발자가 빠르게 스캔하고 참조할 수 있는 reading flow 를 제공한다.
이 프리셋은 "매거진/에세이"가 아니라 **"reference / technical guide"** 성향으로
editorial-warm 과 같은 `document-content` app_mode 를 공유하지만 방향이 정반대다.
한국어 UI 를 1급으로 지원한다.

## 사용자
- **API 를 통합하는 외부 개발자**: endpoint·parameter·response 레퍼런스를 빠르게 스캔
- **SDK/라이브러리 학습 개발자**: tutorial/guide article body 따라가며 code block 복사
- **내부 플랫폼 엔지니어 / DevEx**: internal reference documentation 편집·버전 관리

## 핵심 화면
1. **Landing** — hero + quick start + code example — documentation entry point
2. **Guide** — long-form article body + sticky table of contents + heading anchor + prev/next pager
3. **API Reference** — endpoint + method + parameter table + response schema + inline code
4. **Tutorial** — step-by-step article flow + code block + callout tips/warnings
5. **Changelog** — versioned article list + diff summary + version switcher
6. **Search Results** — ⌘K fuzzy search, title + breadcrumb + snippet

## UI 컴포넌트 (도출)
- **article-body** — long-form prose block with heading anchor + footnote support
- **prose-block** — reading pane rendering markdown article content
- **table-of-contents** — TOC sidebar, anchor-linked heading outline, sticky, collapsible
- **heading-anchor** — h1~h6 heading with `#id` anchor + copy-link icon
- **code-block** — syntax-highlighted code block with copy button, language tab, line number
- **inline-code** — inline code span with mono font + subtle background
- **api-reference-table** — endpoint/method/status/type parameter table, dense, mono-first
- **parameter-table** — structured parameter list (name / type / required / description)
- **callout** — admonition (info / warning / tip / danger) block inside article body
- **admonition-block** — alias of callout, used for technical notes
- **search-chrome** — ⌘K command palette + fuzzy search + recent + keyboard nav
- **version-switcher** — dropdown for doc version (v1 / v2 / latest / nightly)
- **breadcrumbs** — doc path trail (Docs / Section / Article)
- **prev-next-pager** — bottom of article, previous and next reference link
- **footnote** — numbered reference footnote inside article body
- **link-card** — related article card with title + summary
- **sidebar-nav** — left navigation, 2-level, collapsible, current article highlight
- **language-tab** — code block language switcher (ts / python / curl / go)
- **reading-pane** — main article reading column, measured width 65–75ch
- **edit-on-github** — external link to source of the article
- **dialog** — confirm/ack dialog for destructive authoring action
- **toast** — low-noise notification (copy success, save done)
- **tabs** — in-article tabs (example variant / language)
- **dropdown-menu** — keyboard-first menu for version switch / language pick
- **empty-state** — zero-result fallback for search / filter
- **pagination** — for changelog / long article list

## 인터랙션 원칙
- **search-first**: ⌘K 로 어디서든 검색 진입, 결과는 title + breadcrumb + snippet
- **anchor-linked headings**: 모든 heading 은 `#id` anchor, 호버 시 link 아이콘 노출
- **copy-code inline**: code block 오른쪽 상단 copy button, 성공 시 low-noise toast
- **keyboard next/prev**: `j`/`k` article 내 heading 이동, `←`/`→` prev/next article
- **version switcher**: 상단 고정, latest / stable / nightly 명시
- **edit on github**: article 하단 고정 링크
- **sidebar collapse**: narrow viewport 에서 TOC/sidebar 접기
- **language tab switch**: code block 내 language 전환 시 전역 sync (모든 code block 동시 전환)
- **low-motion**: transition 120–200ms, hover/focus 미묘, decorative animation 금지
- **파괴적 액션**(doc delete, version unpin)은 dialog 2단계 + keyboard confirm

## 색상 전략
- **cool neutral surface** — off-white, 장시간 reading 피로감 최소화
- **primary**: **Iris Violet (#5A4FCF)** — 정제된 지적 톤, heading anchor·link·active nav 강조
- **accent**: **Cerulean (#2A52BE)** — inline-code 링크·action button·external link 안정적 블루
- **surface_tint**: **Lavender Mist (#E6E6FA)** — code block 배경·callout info 바탕, 쿨 파스텔
- **semantic**: success / warning / danger / info 4 role — callout/admonition 에 매핑
- **monochromatic + single accent** — editorial-warm 의 warm palette 와 반대 방향
- **dark mode**: deep cool neutral surface (not pure black) + tuned mono syntax palette
- **syntax-highlight palette**: keyword / string / comment / number / function — dark/light 두 세트

## 타이포그래피
- **heading**: **Inter** (영문) / **Pretendard** (한글) — geometric sans, serif 금지
- **body**: **Inter / Pretendard** — reading measure 65–75ch, line-height 1.7 (ko 1.8)
- **mono**: **JetBrains Mono** — code block / inline-code / api-reference-table 필수
- **scale**: xs(12) / sm(14) / md(16) / lg(18) / xl(22) / 2xl(28) / 3xl(36)
- **heading scale**: h1(2xl-3xl) / h2(xl) / h3(lg) / h4(md bold)
- **body line-height**: 1.7 (reference) / 1.8 (ko long-form)
- **mono inline size**: 0.92em, subtle background + padding
- **tabular-nums**: api-reference-table 숫자·version 번호
- **code block**: JetBrains Mono 14–15px, line-height 1.6, 들여쓰기 2space 가정

## 접근성
- WCAG 2.2 AA (본문 대비 4.5:1, UI 3:1)
- heading anchor 는 keyboard focusable, skip-to-content link 필수
- callout 은 아이콘 + 텍스트 라벨 이중 (색맹 대응)
- code block copy button aria-label + success toast 음성 공지
- search ⌘K 는 aria-live 결과 수, keyboard trap 금지
- 링크 under reading pane: hover 만으로 구분 불가 → underline 유지

## 한글 대응
- Pretendard variable (woff2) 번들, heading/body 공용
- 한글 본문 line-height **1.8**, letter-spacing -1%
- word-break: **keep-all**, overflow-wrap: break-word
- code block / api-reference-table 는 mono 영문 고정, 한글 혼용 줄 tabular-nums
- 한국어 callout 라벨: "참고 / 주의 / 경고 / 팁" + 영문 "info / warning / danger / tip" 병기 허용
- TOC 한글 heading 은 Pretendard 500, 반드시 anchor id 는 영문/숫자 slug

## 주의사항
- 이 프리셋은 **document-content--minimal-tech (P1, reference-docs/devtools)** — reference documentation 특화
- "에디토리얼 매거진 · long-form essay · reading comfort magazine" 은 `document-content--editorial-warm` 사용
- 대시보드/관리자 제품은 `dashboard--minimal-tech`, 실시간 모니터링은 `monitoring-ops--minimal-tech`
- 이미지 기반 힌트는 advisory, 구조적 결정은 spec + KB 우선
- 실제 백엔드 (API 서버, 검색 엔진, auth, git integration) 는 프리셋 범위 외 — 시각·문서 시스템만 다룸
