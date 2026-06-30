# TacticLens YouTube Video Design System v0.1

## 1. Positioning

TacticLens 유튜브 영상은 축구 경기를 감상평으로 소비하는 채널이 아니라, 특정 팀의 전술 의도와 실제 이행 여부를 장면 근거로 설명하는 분석 콘텐츠다.

핵심 화면 언어는 **영상 프레임 + 피치맵 + 전술 체크 카드**다. 시청자는 처음 5초 안에 이 영상이 "전술 분석"이라는 것을 알아야 하고, 30초 안에 오늘의 질문을 이해해야 한다.

## 2. Audience

- 축구 전술을 더 깊게 보고 싶은 일반 시청자
- 유소년/아마추어 코치
- 분석관 지망생
- 경기 리뷰를 콘텐츠로 만드는 크리에이터
- 전술 앱 TacticLens의 잠재 사용자

## 3. Channel Tone

- **Precise**: 장면, 시간, 위치, 원칙을 구체적으로 말한다.
- **Coach-like**: 비난보다 수정 포인트를 중심으로 말한다.
- **Evidence-first**: 결론보다 근거 장면을 먼저 보여준다.
- **Calm intensity**: 스포츠 채널의 에너지는 유지하되 과한 예능식 자막은 피한다.

## 4. Visual Identity

### Core Palette

- **Pitch Green** `#50C878`: 성공 이행, 대상 팀, 긍정적 움직임
- **Tracking Cyan** `#00B1D2`: 선수 추적, 이동 경로, 활성 장면
- **Coach Amber** `#FFBF00`: 오늘의 질문, 검수 필요, 코칭 포인트
- **Error Crimson** `#BD2E4A`: 원칙 미이행, 수비 붕괴, 위험 구간
- **Analysis Navy** `#061116`: 기본 배경, 타이틀 카드, 자막 바
- **Chalk White** `#F8F8F4`: 라인, 제목, 본문 텍스트

### Usage Ratio

- Navy/dark surface: 55%
- Video or pitch map image: 25%
- Chalk white text/line: 10%
- Green/cyan tactical marks: 7%
- Amber/crimson emphasis: 3%

한 화면이 녹색으로만 읽히면 안 된다. 피치 언어는 유지하되, 채널 아이덴티티는 dark analysis room + cyan/amber evidence marks로 잡는다.

## 5. Typography

### Font Stack

- Heading: Space Grotesk 700
- Korean UI/Text: Pretendard 500/600/700
- Timecode/Data: JetBrains Mono 500/700

### Text Rules

- 썸네일 제목은 2줄 이하.
- 한 줄 최대 9~11자 수준으로 끊는다.
- 한글 제목은 자간 0, 억지 줄바꿈 금지.
- 숫자, 시간대, 포메이션은 mono를 사용한다.
- 자막은 2줄 이하, 한 줄 18자 안팎을 권장한다.

## 6. Thumbnail System

### Thumbnail Goal

클릭을 위한 자극보다 "오늘 무엇을 분석하는지"를 즉시 보여준다.

### Layout Types

1. **Tactical Question**
   - 좌측 55%: 큰 제목
   - 우측 45%: 피치맵/선수 라인/경기 장면
   - 상단: 짧은 series label

2. **Failure Moment**
   - 중앙: 장면 캡처
   - 빨간 원/라인으로 붕괴 지점 표시
   - 제목은 하단 2줄

3. **Pattern Breakdown**
   - 배경: 단순화 피치맵
   - 전술 구조: 3-2, 4-4-2, rest defense 같은 도식
   - 제목: "왜 통했나" / "왜 무너졌나" 식의 질문형

### Thumbnail Copy Examples

- `4-4-2 압박, 왜 무너졌나`
- `후방 3-2 빌드업의 핵심`
- `역압박 5초 룰이 깨진 장면`
- `풀백 안쪽 진입, 진짜 효과 있었나`

### Don't

- 베팅 배당판처럼 보이는 숫자 나열
- 선수 얼굴만 크게 두고 전술 정보가 없는 썸네일
- 빨강/노랑만 과하게 쓰는 위기 조장형 썸네일
- 작은 텍스트 4줄 이상

## 7. In-Video Components

### Opening Hook

길이: 0:00-0:08

구조:

- 0:00-0:02 경기 장면 또는 피치맵 한 컷
- 0:02-0:05 오늘의 질문
- 0:05-0:08 분석할 전술 원칙 1개 표시

### Title Card

길이: 2초 이하.

필수 요소:

- episode title
- match context
- target team
- tactical question

### Lower Third

용도:

- 전술 용어 설명
- 선수/역할 설명
- 분석 구간 표시

규칙:

- 좌측 하단 고정
- 2줄 이하
- cyan label + white body
- 5초 이상 지속하지 않음

### Tactical Overlay

요소:

- 선수 위치 dot
- 이동 경로 line
- 압박 방향 arrow
- 원칙 성공/실패 badge
- timecode

규칙:

- 한 장면에 강조 색은 2개 이하
- 성공은 green, active tracking은 cyan, 문제는 amber 또는 crimson
- 오버레이는 영상 원본을 가리지 않도록 60~85% opacity

### Chapter Card

용도:

- 빌드업
- 압박
- 전환
- 수비 블록
- 리포트 요약

구조:

- chapter number
- phase label
- one-line claim
- small pitch icon or tactical line

### Evidence Card

영상 중간에 3~5초 보여주는 근거 카드.

필수 정보:

- timestamp
- principle
- execution result
- confidence or review status

## 8. Caption System

### Korean Caption

- 위치: 하단 safe area 중앙
- 크기: 1080p 기준 52~64px
- 줄 수: 최대 2줄
- 배경: navy 78% opacity 또는 text shadow
- 강조 단어: amber 또는 cyan underline

### English Term Pairing

처음 나오는 전문 용어는 한 번만 병기한다.

예:

- 역압박 (counter-press)
- 잔류 수비 (rest defense)
- 압박 트리거 (press trigger)

## 9. Motion Language

### Timing

- Overlay fade: 140ms
- Line draw: 260~420ms
- Chapter card in/out: 280ms
- Caption pop: 120ms
- Thumbnail/hero motion: 사용하지 않음

### Easing

- 기본: ease-out
- 라인 그리기: cubic-bezier(0.2, 0.8, 0.2, 1)
- 과한 bounce 금지

### Motion Rules

- 전술 라인은 설명 타이밍에 맞춰 그려진다.
- 선수 dot은 점프하지 않고 짧은 이동 trail을 남긴다.
- 실패 장면은 흔들림 효과보다 amber/crimson marker로 표현한다.

## 10. Video Formats

### Long-form 16:9

- 1920x1080
- safe margin: 96px
- caption bottom margin: 88px
- lower third max width: 760px

### Shorts 9:16

- 1080x1920
- key visual center 70%
- caption max width: 860px
- 상단 250px, 하단 330px UI safe area 유지
- 피치맵은 세로형 crop 전용 템플릿 사용

### Square 1:1

- 1080x1080
- 제목과 피치맵을 분리하지 말고 stacked layout 사용

## 11. Episode Structure

### Standard Breakdown

1. Hook
2. Match context
3. Tactical principle
4. Evidence clip 1
5. Pitch map explanation
6. Evidence clip 2
7. What changed
8. Coaching takeaway
9. Summary card

### Video Length Targets

- Shorts: 35~55초
- Quick breakdown: 4~6분
- Deep analysis: 8~14분

## 12. Voice and Script Rules

### Good

- "이 장면에서 8번의 전진이 1.2초 늦습니다."
- "압박 방향은 맞았지만, 반대 풀백의 잔류 위치가 비었습니다."
- "성공 장면과 실패 장면을 나란히 보겠습니다."

### Avoid

- "그냥 수비가 별로였습니다."
- "역대급 참사"
- "무조건 이 전술이 답입니다."
- "AI가 분석했으니 맞습니다."

## 13. Production Components

- Thumbnail
- Opening hook
- Title card
- Chapter card
- Lower third
- Tactical overlay
- Timecode badge
- Principle check card
- Evidence card
- Split-screen comparison
- Summary card
- End screen

## 14. QA Standard

영상 업로드 전 다음을 확인한다.

- 제목이 5초 안에 읽히는가
- 첫 장면이 오늘의 질문을 보여주는가
- 모든 전술 주장에 장면 근거가 있는가
- 자막이 모바일에서 잘리는가
- 색상만으로 성공/실패를 구분하고 있지 않은가
- Shorts에서 YouTube UI에 핵심 텍스트가 가려지지 않는가

