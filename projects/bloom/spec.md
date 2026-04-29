# Bloom — 친근한 소셜 피드 커뮤니티 Spec

## 제품 개요
Bloom 은 친구·이웃·취미 커뮤니티를 위한 **playful-soft 톤 소셜 피드 · 스레드 · 프레즌스 · 알림**
플랫폼이다. Threads / Bluesky / Mastodon / Tumblr 계열의 **community feed** 를 지향하며,
**feed item + post card + thread view + reaction bar + follow button + notification center +
presence indicator** 를 한 화면에서 부드럽게 엮어 가볍게 근황을 나누고 친근하게 반응하는
흐름을 제공한다. 이 프리셋은 "관리 대시보드/매거진"이 아니라 **"친근한 커뮤니티 피드"** 성향으로,
같은 community-feed app_mode 안에서 rounded corners · 파스텔 surface · 이모지 반응 · 소프트
알림을 시각 정체성으로 고정한다. 한국어 UI 를 1급으로 지원한다.

## 사용자
- **일반 사용자**: 친구/이웃과 가벼운 근황, 이모지 반응, quick reply
- **크리에이터**: 팬덤·취미 커뮤니티에서 글·이미지·코멘트, 팔로우/언팔
- **커뮤니티 운영자**: 관심사 기반 마이크로 커뮤니티, 알림 센터·피드 정리

## 핵심 화면
1. **Home Feed** — timeline stream + composer + infinite scroll + pull-to-refresh
2. **Thread Detail** — post card + reply composer + comment thread + reaction bar
3. **Profile** — avatar cluster + bio + posts + follow button + presence indicator
4. **Notification Center** — grouped notifications + notification item + presence dot
5. **Messages Inbox** — DM thread list + quick reply + presence indicator (optional)
6. **Compose** — soft dialog + quick post + media + mention autocomplete + tag pill

## UI 컴포넌트 (도출)
- **feed-item** — timeline stream 의 기본 단위, 친근한 avatar + post card wrap
- **post-card** — rounded post card, 본문 + 이미지 + 이모지 반응 + 스레드 미리보기
- **thread-view** — 부모 post + reply list + composer 를 한 페이지에 연결하는 thread
- **reply-composer** — 친근한 quick reply 입력기, 이모지 picker + mention autocomplete
- **comment-thread** — nested comment thread, depth 2 까지 들여쓰기, soft divider
- **reaction-bar** — 좋아요/하트/축하/웃음 등 이모지 reaction bubble, optimistic update
- **follow-button** — rounded follow toggle, 친근한 micro-interaction, presence 연동
- **presence-indicator** — avatar 우하단 presence dot, online/idle/offline 3 상태
- **notification-center** — 알림 모아보기 패널, grouped notifications, swipe archive
- **notification-item** — 개별 알림 (mention / reply / follow / reaction) + presence dot
- **avatar-cluster** — 여러 아바타 겹쳐 보여주는 reaction/참여자 요약
- **timeline-stream** — infinite scroll feed stream, pull-to-refresh, optimistic insert
- **mention-highlight** — @mention 텍스트 강조 + tap 시 프로필 미리보기
- **tag-pill** — rounded tag pill, 해시태그/토픽/카테고리 표시
- **share-sheet** — 친근한 bottom sheet 공유 패널, 소셜 경로 별 shortcut
- **empty-feed-illustration** — empty state illustration, 친근 톤 copy
- **gentle-toast** — low-noise 성공/완료 toast, playful-soft 모션
- **soft-dialog** — rounded-16 dialog, 파괴적 액션도 부드럽게 묻는 톤
- **avatar** — 친근한 rounded avatar, 기본 illustration fallback
- **comment-input** — 댓글 입력 영역, emoji picker + mention
- **mention-popup** — @멘션 자동완성 팝업
- **emoji-picker** — 이모지 reaction / 본문 삽입용 picker
- **search-field** — 피드/태그/사용자 검색 입력
- **tabs** — 피드 필터 (All / Following / Topics) 탭 전환
- **badge** — 알림/새 글 카운트 뱃지

## 인터랙션 원칙
- **pull-to-refresh**: 피드 상단 스와이프 → 새 게시물 soft bounce 로 insert
- **optimistic reaction**: 이모지 탭 시 즉시 반영, 실패 시 gentle rollback + toast
- **quick reply**: reply composer 는 thread 안에서 바로 열림, 모달 대체 지양
- **emoji picker**: 모든 reaction/comment 위치에서 emoji picker 호출 가능
- **presence indicator**: avatar 옆 dot — online/idle/offline 색 + 라벨 이중 표시
- **follow toggle**: follow/unfollow 는 즉시 반영, 애니메이션 120–200ms
- **notification center**: 상단 bell → 패널 slide-down, grouped by type
- **swipe archive**: 알림/메시지 좌스와이프 → archive, 우스와이프 → unread
- **mention autocomplete**: `@` 입력 시 drop-up popup, 키보드 화살표 이동
- **soft motion**: 전반 120–240ms ease-out, rounded bounce 살짝, decorative animation 최소
- **파괴적 액션**(post 삭제, account block)은 soft dialog 로 부드럽게 confirm
- **이모지 혼용**: 한국어 본문 + 이모지 혼용 자연스럽게 — line-height 1.7

## 색상 전략
- **warm pastel surface** — cornsilk 크리미 베이스, 장시간 피드 열람 피로감 최소화
- **primary**: **Coral Blush (#F88379)** — 파스텔 웜 코랄, reaction 강조 · primary CTA
- **accent**: **Mint Green (#98FF98)** — 쿨 파스텔 그린 보색, presence dot · healthy 상태
- **surface_tint**: **Cornsilk (#FFF8DC)** — 크리미 웜 파스텔 배경, post card wrap
- **semantic**: success / warning / danger / info 4 role — gentle-toast · badge 에 매핑
- **rounded-first** — 모든 컴포넌트 corner radius 12–16, button radius full 기본
- **soft shadow** — 0 2px 6px rgba(0,0,0,0.06), 깊은 elevation 금지
- **dark mode**: warm deep neutral (not pure black) + 채도 낮춘 coral/mint + 부드러운 border
- **minimal-tech · corporate-trust 의 cool/무채색 팔레트와 정반대 방향**

## 타이포그래피
- **heading**: **Nunito** (영문, rounded sans) / **Pretendard** (한글) — geometric sans 금지
- **body**: **Inter / Pretendard** — 피드 본문 편안, line-height 1.6 (ko 1.7)
- **mono**: **JetBrains Mono** — 최소 사용 (reaction count / timestamp tabular-nums)
- **scale**: xs(12) / sm(14) / md(16) / lg(18) / xl(22) / 2xl(28)
- **heading scale**: h1(2xl) / h2(xl) / h3(lg) / h4(md semibold)
- **body line-height**: 1.6 (en) / 1.7 (ko long-form)
- **emoji 혼용**: 한글 본문 + 이모지 혼용 자연스럽게, emoji 크기 1em 기본

## 접근성
- WCAG 2.2 AA (본문 대비 4.5:1, UI 3:1)
- presence indicator 는 색 + 텍스트 라벨 (online/idle/offline) 이중
- reaction bar 는 aria-label 로 이모지 의미 음성 공지
- notification item 은 keyboard focusable, swipe archive 는 버튼 대안 제공
- soft dialog 는 focus trap + esc 취소
- emoji picker 는 키보드 grid navigation 지원

## 한글 대응
- Pretendard variable (woff2) 번들, heading/body 공용
- 한글 본문 line-height **1.7**, letter-spacing -1%
- word-break: **keep-all**, overflow-wrap: break-word
- reaction count / timestamp 는 tabular-nums (JetBrains Mono 영문 숫자)
- 한국어 alert 라벨: "알림 / 언급 / 답글 / 팔로우" + 이모지 아이콘 병기 허용
- mention `@` 는 영문/숫자 slug 기본, 표시 이름은 한글 지원

## 주의사항
- 이 프리셋은 **community-feed--playful-soft (P1, social/ko)** — 친근 소셜 피드 특화
- "매거진·long-form reading·editorial essay" 는 `document-content--editorial-warm`
- "관리 대시보드·데이터 테이블" 은 `dashboard--minimal-tech`
- "AI 코파일럿 채팅" 은 `conversation-copilot--minimal-tech`
- 이미지 기반 힌트는 advisory, 구조적 결정은 spec + KB 우선
- 실제 백엔드 (auth, feed ranking, moderation, push notification) 는 프리셋 범위 외 — 시각 시스템만 다룸
