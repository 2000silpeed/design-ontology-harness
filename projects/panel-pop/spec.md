# Panel Pop — Mobile Comic Magazine App Spec

## 제품 개요
Panel Pop은 주간 만화 잡지를 모바일 앱처럼 훑고 읽는 서비스다. 홈은 현재 이슈의 표지, 신작 연재, 짧은 컷 미리보기, 작가 코멘터리, 이어보기 큐를 한 화면에 배치한다. 목표는 웹툰 뷰어처럼 기능적인 동시에 잡지 표지처럼 편집된 인상을 주는 playful-soft document-content 시스템이다.

## 사용자
- **짧게 훑는 독자**: 이동 중 홈에서 이번 주 신작, 추천 단편, 이어보기를 빠르게 확인한다.
- **연재 팔로워**: 관심 작품의 새 회차, 저장 상태, 읽은 위치를 관리한다.
- **잡지형 탐색자**: 테마 기획, 작가 인터뷰, 독자 투표, 아카이브 이슈를 잡지처럼 둘러본다.

## 핵심 화면
1. **Home / Issue Rack**
   - mobile app shell + top utility bar + theme toggle + notification badge
   - issue cover hero: 이번 주 표지, issue number, cover story, CTA
   - weekly issue rail: 지난/다음 이슈 cover carousel
   - genre chip filter: 신작, 단편, 판타지, 일상, 인터뷰
   - episode card list: 작품명, 회차, 읽기 시간, 저장 버튼, 업데이트 배지
   - bottom navigation: 홈, 연재, 보관함, 검색, 내 서재

2. **Featured Story**
   - cover story hero + panel preview strip + creator note
   - speech bubble tag로 편집부 추천 이유 표시
   - reader progress chip과 continue reading sheet
   - 관련 에피소드, 작가 인터뷰, 독자 코멘트 진입

3. **Serial Reader**
   - vertical reading pane + panel image sequence
   - sticky reader progress bar
   - save episode button, next episode CTA, brightness/theme toggle
   - creator note expandable sheet

4. **Library / Bookmarks**
   - saved series grid
   - reading queue list
   - downloaded issue placeholder
   - update notification settings

5. **Search / Archive**
   - search field with genre chips
   - archive issue list
   - creator index and tag filters

## UI 컴포넌트
- **mobile-app-shell**: 390px 중심의 mobile frame, safe-area padding, no horizontal overflow
- **top-utility-bar**: brand mark, issue label, notification icon, theme toggle
- **issue-cover-hero**: cover art, issue number, headline, subtitle, primary CTA, save action
- **weekly-issue-rail**: whole-card horizontal rail, visible card text complete, no clipped labels
- **manga-cover-card**: cover thumbnail, series title, genre, freshness badge, progress marker
- **episode-card**: compact row/card hybrid, episode number, title, reading time, save button
- **panel-preview-strip**: 3-4 comic panels, tap target, caption, progress affordance
- **genre-chip**: filter chip with active/pressed/disabled states
- **speech-bubble-tag**: editor note, creator quote, recommendation reason
- **creator-note-sheet**: expandable note panel, byline, timestamp, close/fold action
- **reader-progress-bar**: top progress indicator, numeric percent optional
- **continue-reading-sheet**: bottom sheet with current series and next CTA
- **bookmark-library-card**: saved series and update state
- **bottom-navigation**: 5 route icons, active state, badge, accessible labels
- **search-field**: mobile search input, clear button, suggestions
- **soft-toast**: saved/read/unread status feedback

## 인터랙션 원칙
- Cover swipe는 160-220ms ease-out으로 부드럽게 이동하고 prefers-reduced-motion에서는 즉시 전환한다.
- Episode card save는 optimistic state로 즉시 저장 배지를 보여준다.
- Panel preview는 카드 크기를 고정해 이미지 로딩이나 hover/focus 상태가 레이아웃을 흔들지 않는다.
- Bottom navigation은 320px에서도 5개 항목이 텍스트와 아이콘을 겹치지 않는다.
- Genre chip rail은 모바일에서 가로 스크롤을 허용하되 visible chip label은 완전히 보여야 한다.
- Theme toggle은 light/dark semantic token만 전환하고 컴포넌트 로컬 색을 새로 만들지 않는다.

## 색상과 타이포 적용
- primary: Periwinkle — active tab, hero background, progress, focus ring
- accent: Living Coral — 신작/저장/CTA, speech-bubble emphasis
- surface_tint: Buttercream — magazine paper surface, issue rail background
- supporting cool blue/teal은 info 또는 tiny badge에 한정한다.
- 한글 제목은 Pretendard 800-900, 본문과 설명은 Pretendard 400-600, 숫자는 JetBrains Mono tabular-nums.

## 접근성
- WCAG 2.2 AA contrast를 지킨다.
- 모든 icon-only button은 aria-label을 갖는다.
- bottom navigation은 nav landmark와 route label을 갖는다.
- progress bar는 role="progressbar"와 aria-valuenow를 갖는다.
- cover art와 panel art에는 내용 기반 alt text를 제공한다.
- 모바일 viewport 320, 360, 390, 430px에서 horizontal scroll이 없어야 한다.

## 구현 목업 범위
- 정적 HTML/CSS/JS mobile mockup으로 home, featured, library 탭을 구현한다.
- 실제 만화 IP를 사용하지 않고 original generated comic cover / panel assets로 시각 실체를 만든다.
- 표지와 컷 미리보기는 완성된 만화 잡지 자산처럼 보여야 하며, 단순 기하학 SVG, 낙서형 placeholder, 저정보량 도식은 실패로 간주한다.
- 하네스 산출물의 tokens.css와 component spec을 우선하고, 외부 레퍼런스 palette/font/copy는 복제하지 않는다.
