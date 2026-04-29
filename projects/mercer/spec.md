# Mercer — 금융·보험 Enterprise AI Chatbot Corporate-Trust Spec

## 제품 개요
Mercer 는 금융·보험 기업이 고객 상담 AI 챗봇을 규제·감사 맥락에서 구축·배포하는 **corporate-trust 톤 conversation-copilot**
builder 이다. ChatGPT Enterprise / Anthropic Claude for Enterprise / Stripe Dialog / Salesforce Einstein / Intercom Fin
계열의 **workspace + thread + chat message + prompt composer + compliance-artifact panel + audit-trail timeline +
policy-check badge + citation footnote + reviewer handoff + workspace-header** 를 Super Sonic bright enterprise blue
primary + Copper warm accent + Powder Blue soft surface 로 엮어 **규제·감사 친화 enterprise chat** 경험을 제공한다.
이 프리셋은 "AI 글쓰기 editorial copilot"(conversation-copilot--editorial-warm, quill) 도 아니고 "중립 AI
워크스페이스"(conversation-copilot--minimal-tech, glacier) 도 아닌, **"enterprise compliance chatbot"** 정체성이다.
한국어 UI 를 1급으로 지원한다.

## 사용자
- **금융·보험 고객 상담 operations 담당자**: 규제 내 AI 상담 응답을 검토·배포, thread / audit-trail 로 히스토리 관리
- **컴플라이언스 · 감사 담당자**: AI 상담 응답의 policy-check 배지 / audit-trail 타임라인 / retention 지표 / citation footnote 를 규제 보고에 인용
- **엔터프라이즈 IT/플랫폼팀**: 사내 SSO / DLP / data retention 정책과 연결된 배포 · workspace 관리

## 핵심 화면
1. **Workspace Home** — workspace-header + project-switcher + org-name + SSO-indicator + thread-list-sidebar + welcome / empty state
2. **Thread View (Chat)** — thread-header + message-stream + ai-message + user-message + streaming-cursor + prompt-composer + suggestion-chips + citation footnote
3. **Compliance Artifact Panel** — artifact-panel (right drawer) + artifact-title + policy-check-badge + compliance-summary + citation-list + reviewer-chip
4. **Audit Trail Timeline** — audit-trail section + audit-trail-step + audit-timestamp(mono) + reviewer-id + policy-id + action-type (sent / reviewed / published)
5. **Policy Check Modal** — compliance-warning-modal + policy-summary + matched-rules + override-path + cancel/proceed buttons
6. **Reviewer Handoff** — reviewer-assignment chip + reviewer-list + approval-status + decision timeline
7. **Source Reference Card** — source-reference-card + citation-title + citation-url + policy-tag + data-retention-indicator
8. **Data Retention Settings** — retention-panel + retention-slider(90 / 365 / custom days) + encryption-badge + deletion-schedule
9. **Empty Conversation State** — empty-illustration (copper subtle) + starter-prompt-list + 프롬프트 가이드라인 링크

## UI 컴포넌트 (도출)
- **workspace-header** — sticky top, brand-logo + workspace-name + project-switcher + org-name + SSO-indicator + account-menu
- **workspace-logo** — brand logo area, neutral enterprise
- **workspace-name** — 조직 고유 workspace 이름 (Pretendard 700)
- **project-switcher** — 다수 프로젝트 (예: 보험 VS 대출 VS 카드) 전환 dropdown
- **org-name** — 조직 이름 표기, small muted
- **sso-indicator** — "okta" / "azure ad" / "ping" 로고 + connected 상태 인디케이터
- **account-menu** — 우측 상단 account avatar + dropdown (profile / policies / logout)
- **thread-list-sidebar** — 좌측 사이드바, thread-item stack + new-thread-button + search
- **thread-list-item** — 개별 thread 미리보기, 제목 + last-message + timestamp(mono) + policy-check 배지 유무
- **thread-search** — 사이드바 상단 search input
- **new-thread-button** — 좌측 상단 "새 대화" primary 버튼 (Super Sonic fill)
- **thread-header** — 대화창 상단 header, thread-title + policy-scope + assigned-reviewer + actions (export / copy / archive)
- **message-stream** — 대화 스트림 컨테이너, 메시지 시간순 스크롤
- **user-message** — 사용자 메시지 bubble, neutral border + 오른쪽 정렬
- **ai-message** — AI 응답 bubble, Super Sonic 미세 accent 좌측 stripe + policy-check badge 인라인
- **streaming-cursor** — AI 응답 중 caret 깜박임
- **prompt-composer** — 하단 input, multi-line + toolbar (첨부, 프롬프트 템플릿, 규제 선택)
- **prompt-attach-button** — 파일/문서 첨부
- **prompt-template-picker** — 저장된 프롬프트 템플릿 선택 dropdown
- **regulation-selector** — "KYC" / "보험약관" / "AML" 등 규제 스코프 선택 chip
- **suggestion-chips** — prompt-composer 위 추천 프롬프트 chip row
- **regenerate-button** — ai-message 아래 "다시 생성" 작은 버튼
- **stop-generation-button** — 스트리밍 중 "중단" 버튼
- **citation-footnote** — ai-message 하단 각주 번호, 클릭 시 source-reference-card popover
- **source-reference-card** — 출처 문서 카드, title + url + excerpt + policy-tag + retention-indicator
- **source-reference-list** — artifact-panel 내 여러 출처 목록
- **compliance-artifact-panel** — 우측 drawer, AI 응답을 compliance-artifact 로 승격 + 검토 흐름
- **artifact-panel-header** — 제목 + close + "승인 요청" 버튼
- **artifact-title** — compliance artifact 제목, Pretendard 700
- **artifact-summary** — artifact 요약 본문, Pretendard 본문 line-height 1.5
- **compliance-summary** — "이 응답은 KYC 규정 3.2.1 참조" 류 요약 블록
- **policy-check-badge** — ai-message / artifact 옆 policy 일치 배지, green = pass / copper = warning / red = fail
- **matched-rules-list** — 적용된 규정 목록 (policy-id + 버전 + 요약)
- **audit-trail-section** — artifact 또는 thread 의 감사 로그 컨테이너
- **audit-trail-step** — 단일 감사 step, action-type + actor + timestamp(mono) + policy-id
- **audit-timestamp** — 감사 timestamp, mono tabular-nums
- **reviewer-chip** — 검토자 assigned chip, avatar + 이름 + 역할
- **reviewer-assignment-panel** — 검토자 선정 panel, 리스트에서 선택
- **approval-status** — "검토 대기 / 승인 / 반려" 상태 표시, badge + icon
- **compliance-warning-modal** — 고위험 정책 충돌 시 나타나는 경고 모달
- **policy-summary** — 모달 내 정책 요약
- **matched-rules-accordion** — 매칭된 규정 상세, expand
- **override-path-link** — 예외 승인 경로 안내 link (warning copper)
- **modal-action-buttons** — cancel / proceed (proceed 는 disabled 기본)
- **retention-panel** — data retention 설정 panel
- **retention-slider** — 90 / 180 / 365 / custom 슬라이더
- **retention-label** — retention 일수 표시 (mono tabular-nums)
- **encryption-badge** — 암호화 방식 뱃지 (TLS / at-rest / HSM)
- **deletion-schedule** — 자동 삭제 예정 timestamp
- **empty-conversation-state** — 새 thread 빈 상태, copper illustration + starter prompt + 가이드라인 link
- **starter-prompt-list** — 빈 상태 추천 프롬프트 3–5 개
- **guideline-link** — "정책 가이드라인" link, Super Sonic
- **toast-notification** — "검토 완료" / "감사 기록 저장" 소프트 알림
- **focus-ring** — 전 컴포넌트 focus 시 Super Sonic 2 px outline + 2 px offset
- **breadcrumb** — workspace > project > thread, Pretendard 400 muted
- **shortcut-chip** — keyboard shortcut 안내 chip (mono)
- **data-classification-badge** — PII / non-PII / internal 분류 배지
- **compliance-version-chip** — 적용된 정책 버전 (mono, 예: v2.4.1)

## 인터랙션 · 모션
- **streaming cursor blink** — AI 응답 중 caret 1 Hz blink, motion-reduce 시 정적 caret
- **policy check reveal** — ai-message 완료 시 policy-check 배지 slide-in (200 ms)
- **artifact drawer slide** — 우측 drawer 열림/닫힘 220 ms ease
- **modal warning fade** — compliance warning modal 140 ms fade + subtle shake (고위험 신호)
- **thread switch fade** — thread 전환 시 내용 영역 100 ms fade 후 load
- **focus ring** — Super Sonic 2 px outline + 2 px offset
- **keyboard shortcuts** — ⌘N (새 대화) / ⌘K (thread 검색) / ⌘Enter (전송) / ⌘Shift+A (audit-trail 보기)

## Color Token 의도
- **primary #0071A8 Super Sonic** — new-thread-button fill / prompt-composer send button / ai-message left stripe / policy-check pass 배지 fill / workspace-header nav active underline
- **accent #B87333 Copper** — reviewer-chip accent / audit-trail step dot (완료) / compliance warning subtle indicator / citation-footnote hover / empty-state illustration primary stroke
- **surface_tint #B0E0E6 Powder Blue** — thread-list-sidebar surface / compliance-artifact-panel tint / empty-state background / toast-notification background
- **semantic**: success moss-green / warning copper / error rust-red / info powder-blue neutral

## Typography 의도
- **heading (Inter 500/600/700)** — workspace-name / thread-title / artifact-title / policy-check label / audit-trail section-header
- **body (Inter 400/500)** — chat-message body / artifact-summary / audit-trail description / policy-summary / compliance-summary
- **mono (JetBrains Mono 400/500)** — policy-id / audit-timestamp / citation footnote 번호 / retention days / record-id / compliance-version / reviewer-id
- **korean (Pretendard 400/500/600/700)** — chat-message / artifact paragraph / policy-check label / audit description, keep-all line-height 1.5–1.6 (enterprise), workspace-header / thread-title 는 Pretendard 700

## 접근성
- WCAG 2.2 AA 준수, Super Sonic 위 텍스트 대비 ≥ 4.5:1 (white on Super Sonic), Copper 위 텍스트 대비 ≥ 4.5:1
- 키보드 전용 네비게이션 — 모든 모달 / drawer / 메뉴 / 슬라이더 tab/enter/space/arrow 조작
- 스크린리더 focus order workspace-header → thread-sidebar → thread-header → message-stream → prompt-composer → artifact-drawer
- prefers-reduced-motion 지원 — blink / slide / fade / shake 전부 축소
- 규정 warning modal 은 focus trap 필수

## 회피 패턴
- playful pastel consumer chat (bloom / orchard 영역)
- streetwear drop 패턴
- editorial magazine cover-heavy 구성
- d2c product grid / commerce 제품 판매 화면
- glassmorphism 과도
- social feed casual chat
- marketing landing pricing-focused 화면 (landing 은 별도 프리셋)

## 참고 레퍼런스
- [ChatGPT Enterprise](https://openai.com/chatgpt/enterprise) — 엔터프라이즈 AI workspace · thread · admin console 참조
- [Anthropic Claude for Enterprise](https://www.anthropic.com/enterprise) — compliance / SSO / retention 가이드
- [Stripe Dialog](https://stripe.com/docs/dialog) — 엔터프라이즈 대화 UI / artifact 참조
- [Salesforce Einstein](https://www.salesforce.com/products/einstein/overview/) — CRM AI assistant audit-trail / policy-check / reviewer handoff
- [Intercom Fin](https://www.intercom.com/fin) — customer support AI citation / source reference / compliance-artifact

## 결정 로그
- **corporate-trust 톤 선택 이유**: 금융·보험 도메인은 규제·감사 맥락에서 신뢰·정돈이 핵심. minimal-tech 는 너무 neutral, editorial-warm 은 writing-first 톤, playful-soft / bold-confident 는 enterprise 맥락 부적합.
- **primary Super Sonic 선택 이유**: 기존 corporate-trust (ledger) 의 Prussian Blue 는 dashboard 운영 톤으로 이미 점유됨. enterprise chat 맥락의 Super Sonic bright blue 는 "혁신적 · 신뢰 · 전문" 삼박자를 잡으면서 차별화 확보.
- **surface_tint Powder Blue 선택 (1 겹침 허용)**: Ice Blue 는 ledger+pulse 이중 점유, Misty Blue 는 atelier 점유로 회피. Powder Blue 는 beacon 과 1 겹침이나 beacon 은 marketing-landing--minimal-tech 로 app_mode+brand_tone 축 전부 달라 사용자가 셀 혼동 위험 없음.
- **accent Copper 선택 이유**: 기존 ledger Bronze Gold 와 유사 계열이지만 Copper 는 bronze 보다 warm-red 쪽으로 치우쳐 enterprise "warning / reviewer attention" 시그널로 기능. Bronze 는 dashboard 운영 안정감, Copper 는 chat 맥락의 "검토 필요" 경고 톤.
- **font Inter + Pretendard**: 규제 맥락에서 serif 는 지양 (Fraunces 류는 editorial-warm quill 영역). Inter sans + Pretendard 조합으로 enterprise 정돈감 확보.
