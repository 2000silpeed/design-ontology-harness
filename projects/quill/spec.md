# Quill — Editorial-Warm Writing Copilot Spec

## 제품 개요
Quill 은 에세이 / 뉴스레터 / 저널 writing 과 reading-analysis 를 돕는
**editorial-warm 톤 conversation-copilot (대화형/코파일럿)** 이다.
Lex / Jasper / Sudowrite / Notion AI / Ulysses / Substack 계열의
**chat · prompt · assistant message · user message · streaming cursor +
message artifact · artifact preview panel · draft document · outline sidebar ·
heading anchor · revision timeline · tone slider · reading-mode toggle +
prompt composer · suggestion card · mention chip · thread header ·
new thread button · regenerate button · stop-generation button ·
inline citation · citation footnote · quote block · paragraph block ·
empty conversation state** 를 한 시스템으로 묶어
"드래프트 대화 → 아티팩트 리뷰 → 편집 마감"의 차분한 editorial 워크플로우를 제공한다.
이 프리셋은 "minimal-tech AI 코파일럿"이나 "playful 챗봇"이 아니라
**"calm editorial writing copilot"** 성향으로,
warm neutral surface · serif heading pair · muted editorial accent ·
reading-first layout · calm writing canvas · soft cream surface ·
muted warm divider · restrained bibliographic chrome · long-form artifact preview 를
시각 정체성으로 고정한다. 한국어 UI 를 1급으로 지원한다.

## 사용자
- **에세이 / 뉴스레터 / 블로그 작가**: 긴 호흡으로 드래프트를 대화하며 다듬는 writing partner — prompt composer → message artifact → artifact preview panel → revision timeline
- **저널 / 독서 노트 / 북 리뷰 사용자**: reading-first reading-mode toggle + citation footnote 기반 재구성 — chat thread + inline citation + quote block
- **매거진 / 에디토리얼 에디터**: AI 드래프트 + tone slider 조정 + 편집 아티팩트 리뷰 — artifact preview panel + outline sidebar + heading anchor

## 핵심 화면
1. **Home / New Thread** — thread list + new thread button + empty conversation state + reading-mode toggle + suggestion card (start with an essay / newsletter / journal)
2. **Conversation** — chat thread + user message + assistant message + streaming cursor + typing indicator + inline citation + regenerate button + stop-generation button + prompt composer
3. **Artifact (Draft)** — message artifact + artifact preview panel + draft document + outline sidebar + heading anchor + revision timeline + tone slider + citation footnote + quote block + paragraph block + reading-mode toggle
4. **Prompt Composer** — prompt composer (multiline) + suggestion card (essay starter / newsletter starter / tone preset) + mention chip (@thread / @citation / @note) + attach note
5. **Library / Drafts** — draft document list + thread header + reading pane + citation shelf
6. **Settings** — tone preference + citation style + reading-mode default + locale
7. **Empty / Onboarding** — empty conversation state + gentle onboarding suggestion card + new thread button

## UI 컴포넌트 (도출)
- **thread-list** — 좌측 thread 목록, 대화 단위 editorial 목차
- **thread-header** — 현재 thread 의 제목 · 작성 시점 · 작성자 · 아카이브 토글
- **new-thread-button** — 새 대화 시작 버튼 (warm accent)
- **empty-conversation-state** — empty state 일러스트 + "새 드래프트를 시작해 보세요" 카피 + suggestion card
- **chat-thread** — 단일 thread 내 user/assistant message 목록, reading-first line-height
- **chat-message** — 메시지 말풍선 (editorial warm bubble, serif heading + sans body)
- **assistant-message** — assistant 측 메시지 (soft cream surface, Marsala name label, streaming cursor slot)
- **user-message** — user 측 메시지 (quoted 인용 스타일, muted warm divider)
- **streaming-cursor** — 응답 생성 중 blinking cursor (calm fade, prefers-reduced-motion 존중)
- **typing-indicator** — "Quill is thinking…" typing dots
- **prompt-composer** — 멀티라인 prompt composer (수납형 grow, 한글 IME keep-all)
- **suggestion-card** — prompt 시작 시 editorial 시작 카드 (에세이 초안 / 뉴스레터 드래프트 / 저널 리뷰)
- **mention-chip** — @thread / @citation / @note mention 칩 (muted warm fill)
- **regenerate-button** — 응답 재생성 버튼 (ghost serif label)
- **stop-generation-button** — 응답 중단 버튼 (muted danger ghost)
- **inline-citation** — 본문 내 citation 번호/괄호 링크 (hover tooltip)
- **citation-footnote** — 아티팩트 하단 주석 · 인용 출처 목록
- **quote-block** — 인용문 블록 (serif italic, muted vertical rule)
- **paragraph-block** — 본문 문단 블록 (reading pane line-height 1.6–1.7)
- **message-artifact** — 메시지 내 아티팩트 진입 카드 (드래프트 미리보기 + 열기 CTA)
- **artifact-preview-panel** — 우측 패널 아티팩트 미리보기 (draft document + outline sidebar + revision timeline)
- **draft-document** — 에세이/뉴스레터/저널 드래프트 문서 본체 (reading-first, 65–75ch 측정)
- **outline-sidebar** — heading anchor 기반 outline 목차, 접기/펼치기
- **heading-anchor** — 드래프트 heading 옆 anchor 링크 (복사)
- **revision-timeline** — 드래프트 리비전 세로 타임라인 (시간 순, diff preview 진입)
- **tone-slider** — calm ↔ warm / formal ↔ casual 두 축 tone slider (아티팩트 재작성 트리거)
- **reading-mode-toggle** — reading mode (wide/narrow / serif/sans / line-height) toggle
- **editor-toolbar** — artifact editor toolbar (bold/italic/quote/heading/list/link, editorial restrained)
- **inline-format-menu** — 텍스트 선택 시 floating 포맷 메뉴
- **slash-command-menu** — `/` 입력 시 block 타입 + AI 제안 menu
- **block-controls** — block hover 시 이동/삭제/재작성 controls
- **primary-button** — warm Marsala primary CTA (서브틀한 editorial, 대담 금지)
- **secondary-button** — ghost secondary (hairline 테두리)
- **ghost-button** — 텍스트 링크형 tertiary
- **icon-button** — 아이콘 전용 (regenerate / stop / copy)
- **toast** — 저장됨 / 복사됨 gentle toast (slow fade)
- **modal-dialog** — 설정 / 삭제 확인 modal (calm)
- **thread-list-item** — thread 목록 단위 (thread 제목 + 마지막 메시지 미리보기 + 시각)
- **search-field** — thread / draft 검색 (editorial restrained)
- **autocomplete** — mention / slash / citation autocomplete dropdown
- **site-footer** — editorial footer (about / privacy / credits)

## 인터랙션 원칙
- **calm streaming cursor**: assistant 응답 streaming 중 blinking cursor 는 slow fade (300–500ms), prefers-reduced-motion 모드에서는 정적
- **gentle prompt composer**: 줄바꿈 Shift+Enter, 제출 Enter (IME 조합 중 제출 방지), warm focus ring
- **writing artifact side panel**: chat thread 에서 artifact 카드 클릭 시 우측 artifact preview panel slide-in (slow fade 300ms), backdrop 없음 (editorial 동시 편집)
- **draft revision timeline**: revision timeline hover 시 diff preview, click 시 restore 확인 dialog
- **outline collapse toggle**: outline sidebar 의 heading 그룹 접기/펼치기, 키보드 Left/Right navigate
- **citation footnote hover**: inline citation hover 시 풍선 footnote 내용, tap 시 아래 citation shelf 로 scroll-to
- **reading-mode toggle**: artifact 상단 reading-mode toggle 로 wide ↔ narrow / serif ↔ sans / line-height 1.6 ↔ 1.8 전환, 로컬 저장
- **slow fade transition**: 150–260ms ease-out (editorial calm 모션), 급격한 bounce 금지
- **warm focus ring**: focus ring 은 Marsala 대비 muted warm ring (2px outline, 2px offset)
- **muted mention chip**: mention 삽입 시 chip fill 은 accent Moss Green 의 low-alpha tint, 텍스트는 본문 컬러 유지
- **regenerate / stop-generation**: assistant message 상단 호버 툴바에 regenerate/stop 아이콘, 생성 중 stop 만 활성
- **prefers-reduced-motion**: streaming cursor / slide-in / fade / timeline hover 애니메이션 모두 제거

## 색상 전략
- **primary**: **Marsala (#964F4C)** — 와인-브라운 deep warm editorial primary, primary-button / new-thread-button / regenerate-button / toast 성공 라벨 / thread-header 강조
- **accent**: **Moss Green (#8A9A5B)** — muted sage accent, inline-citation / mention-chip fill / tone-slider 활성 track / outline-sidebar active heading
- **surface_tint**: **Flax (#EEDC82)** — 크리미 warm paper surface, assistant-message 말풍선 soft fill / artifact-preview-panel 베이스 / empty-conversation-state 일러스트 배경
- **semantic**: success(저장됨) / warning(tone slider 주의) / danger(stop-generation 경고) / info(citation 안내) 4 role
- **warm neutral surface** — 전역 surface 는 near-white warm neutral (cream-tinted), editorial canvas 유지
- **muted editorial accent** — accent 는 saturation 낮은 Moss, 대담 금지
- **reading-first layout** — 본문 prose 는 65–75ch, line-height 1.6–1.7, 큰 여백
- **restrained bibliographic chrome** — thread-header / editor-toolbar / footer 는 hairline + serif label, 아이콘 최소
- **long-form artifact preview** — artifact preview panel 은 full-width draft document + outline sidebar + revision timeline, reading-first
- **dark mode**: deep warm brown surface + tuned Marsala/Moss 채도 낮춤, paragraph/prose 는 warm off-white 로 대비 확보
- **기존 12종 프리셋 HEX 와 HEX 겹침 0**

## 타이포그래피
- **heading**: **Source Serif Pro** (영문) / **Pretendard** (한글) — editorial serif heading, 드래프트 제목 / thread 제목 / artifact heading, Lora (signal-desk) 와 차별화
- **body**: **Inter / Pretendard** — chat message body / prompt composer / paragraph block / outline text, line-height 1.6–1.7 (reading-first)
- **mono**: **JetBrains Mono** — inline code / citation footnote number / revision timestamp / tone slider value, tabular-nums 영문 고정
- **scale**: xs(11) / sm(12) / md(14) / lg(16) / xl(18) / 2xl(20) / 3xl(24) / 4xl(32) / 5xl(40)
- **thread header (드래프트 제목)**: 2xl–3xl (20–24px), heading 600 serif
- **artifact heading (h1)**: 3xl–4xl (24–32px), heading 700 serif, reading-mode wide 에서는 4xl
- **chat message body**: md–lg (14–16px), body 400–500, line-height 1.6
- **assistant-message name label**: sm (12px) heading 600 serif, Marsala 텍스트
- **paragraph-block (드래프트 본문)**: lg (16px), body 400, line-height 1.7 reading-mode
- **quote-block**: md–lg (14–16px), body italic 400, serif variant, muted rule 좌측
- **prompt composer**: md (14px), body 400, line-height 1.6
- **inline-citation**: xs–sm (11–12px) sup mono
- **citation-footnote**: sm (12px) body 400 + mono number
- **revision-timeline timestamp**: xs (11px) mono tabular-nums
- **tone-slider label**: sm (12px) body 500
- **한글 line-height**: 1.6 (chat message), 1.7 (artifact paragraph block, reading-first), keep-all
- **tabular-nums**: revision timestamp / citation footnote number / tone slider value / token count 전용
- **editorial restraint** — heading letter-spacing 0, body letter-spacing 0, 대담 금지

## 접근성
- WCAG 2.2 AA (본문 대비 4.5:1, UI 3:1, Marsala 위 텍스트는 warm off-white 확보)
- prompt-composer 는 textarea + aria-label="대화 입력" + aria-multiline + IME 조합 중 Enter 제출 방지
- streaming-cursor 는 aria-live="polite" + "Quill 응답 생성 중" 텍스트 대체
- artifact-preview-panel 은 role="complementary" + aria-label="드래프트 미리보기"
- outline-sidebar 는 role="navigation" + aria-label="드래프트 목차"
- heading-anchor 는 키보드 focus 가능 + aria-label="링크 복사"
- revision-timeline 은 role="list" + 각 revision 은 role="listitem" + aria-current
- tone-slider 는 role="slider" + aria-valuemin/max/now + 키보드 arrow
- reading-mode-toggle 은 role="group" + 내부 radio 선택
- inline-citation 은 aria-describedby 로 footnote 연결
- regenerate-button / stop-generation-button 은 aria-busy 연동 (생성 중 stop 만 활성)
- modal-dialog 는 role="dialog" + aria-modal + focus trap + ESC 닫힘
- mention-chip 은 role="link" + 프로필 피어뷰 aria-haspopup
- prefers-reduced-motion 존중 — streaming cursor / slide-in / fade / timeline hover 애니메이션 제거
- empty-conversation-state 는 heading + 설명 + CTA, 일러스트는 aria-hidden

## 한글 대응
- Pretendard variable (woff2) 번들, heading/body 공용 (한글 명조 heading 번들은 복잡성 회피, editorial 감성은 Source Serif Pro + Pretendard pairing 으로 확보)
- 한글 chat message / artifact paragraph block line-height **1.6–1.7**, keep-all
- 한글 thread header / artifact heading line-height **1.4**, keep-all, letter-spacing 0
- word-break: **keep-all**, overflow-wrap: break-word
- citation footnote number / revision timestamp / tone slider value / token count 는 mono 영문 고정 (한글 혼용 금지), tabular-nums
- 한국어 라벨: "새 대화 / 드래프트 / 아티팩트 / 리비전 / 톤 / 읽기 모드 / 인용 / 주석 / 재생성 / 중단" + 영문 "new thread / draft / artifact / revision / tone / reading mode / citation / footnote / regenerate / stop" 병기 허용
- prompt composer placeholder: "어떤 드래프트를 함께 쓰고 싶으신가요? (Draft together)"

## 주의사항
- 이 프리셋은 **conversation-copilot--editorial-warm (P2)** — 차분한 editorial writing/reading AI copilot 특화
- "minimal-tech AI 코파일럿 / 일반 챗봇" 은 `conversation-copilot--minimal-tech`
- "에디토리얼 매거진 · long-form reading · essay blog" 는 `document-content--editorial-warm`
- "fashion editorial commerce" 는 `commerce--editorial-warm`
- "개발자 reference docs" 는 `document-content--minimal-tech`
- "B2B SaaS 마케팅 랜딩" 은 `marketing-landing--minimal-tech`
- "스트리트웨어 드롭 커머스" 는 `commerce--bold-confident`
- "스포츠 랜딩" 은 `marketing-landing--bold-confident`
- "fintech 대시보드" 는 `dashboard--corporate-trust`
- "일반 SaaS 대시보드" 는 `dashboard--minimal-tech`
- "SRE / observability 모니터링" 은 `monitoring-ops--minimal-tech`
- "소셜 피드" 는 `community-feed--playful-soft`
- "캔버스 · 디자인 도구" 는 `canvas-tool--minimal-tech`
- 이미지 기반 힌트는 advisory, 구조적 결정은 spec + KB 우선
- 실제 LLM 호출 / 스트리밍 백엔드 / vector store / citation 검색 엔진은 프리셋 범위 외 — copilot chrome 만 다룸
