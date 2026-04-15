# Glacier 상세 설계서

Glacier는 장기 코드·데이터 아카이브 서비스입니다. 핵심은 보관, 검증된 복원, 감사 로그 세 축입니다.

## 메인 대시보드
- 좌측 사이드바 네비게이션 (Archives, Restores, Audit, Settings)
- 상단 통계 카드 4개 — 총 아카이브 수, 보관 용량, 최근 복원 성공률, 검증 실패 건수
- 최근 아카이브 데이터 테이블 — 이름, 크기, 체크섬, 상태, 생성 시각, 액션
- 빠른 작업을 위한 command palette (⌘K)

## Archives 화면
- 좌측 필터 사이드바 (프로젝트, 상태, 기간, 태그)
- 중앙 리스트 테이블 — 체크박스 다중 선택, 정렬, 가상 스크롤
- 우측 상세 드로어 — 메타데이터, 청크 목록, 체크섬, 복원 버튼
- 툴바 — 새 아카이브, 일괄 다운로드, 보존 정책 편집

## Restore 워크플로우
- 단계별 마법사 폼 (Source → Target → Verify → Confirm)
- 각 단계에 진행률 표시
- 복원 작업 큐 화면 — 실행 중, 대기, 완료, 실패 상태 탭
- 상세 로그 뷰 (가상 스크롤, 검색, 필터)

## 감사 로그 (Audit)
- 타임라인 기반 리스트 — 행위자, 동작, 대상, 결과, 타임스탬프
- 고급 필터 (날짜 범위, 행위자, 동작 유형)
- 변경 내역 diff 뷰
- CSV / JSON 내보내기 버튼

## 설정 화면
- 프로필 편집 폼 (이름, 이메일, 아바타)
- 팀 멤버 관리 테이블 (역할, 권한, 마지막 접속)
- API 키 관리 (생성, 회수, 권한 범위)
- 알림 설정 (이메일, Slack, 웹훅 체크박스)
- 보존 정책 편집 폼

## 공통 요구사항
- 다크 모드 필수
- 키보드 내비게이션 완전 지원
- 에러 상태에 구체적 복구 가이드
- 대량 데이터 처리를 위한 가상 스크롤, 무한 로드
- 모든 파괴적 동작(삭제, 복원)은 확인 모달

---

# Glacier 랜딩 페이지 설계

Glacier 공식 사이트(glacier.dev)의 랜딩 페이지. 목적은 플랫폼 엔지니어·SRE가 10초 안에 "검증된 복원이 가능한 장기 아카이브"라는 가치를 이해하고 가입 플로우로 전환하는 것.

## 사이트 헤더 (Site Header)
- 상단 고정 마케팅 헤더 (고정 높이 64px, 스크롤 시 미세한 border-bottom)
- 좌측: 사이트 로고
- 중앙: 주요 섹션 내비게이션 링크 (Product, Docs, Pricing, Changelog)
- 우측: 로그인 링크 + 시작하기 CTA 버튼
- 모바일: 햄버거 메뉴 트리거로 변환

## 히어로 섹션 (Hero Section)
- 랜딩 상단 어보브 더 폴드 영역
- 헤드라인 위에 카테고리 eyebrow 텍스트 ("Long-term code & data archive")
- 메인 헤드라인: 핵심 가치 제안 — "Every byte, verified forever"
- 서브 헤드라인: 2~3줄의 보강 카피 (장기 보관, 검증된 복원, 감사 로그)
- primary CTA ("무료로 시작") + secondary CTA ("데모 예약") 버튼 그룹
- 우측 또는 하단: 제품 스크린샷이나 아키텍처 일러스트 (hero visual)
- 히어로 바로 아래: 신뢰 라인 — "SOC 2 Type II 인증 · 99.999999999% 내구성"

## 사회적 증거 (Social Proof)
- 히어로 바로 아래의 로고 클라우드 — "Trusted by engineering teams at" + 고객사 로고 6~8개
- 주요 지표 하이라이트 3개 — "50PB 아카이브 관리", "99.99% 복원 성공률", "0건 데이터 유실"
- 언론 인용 또는 어워드 스트립 (선택)

## 기능 섹션 (Feature Grid)
- 3-column feature grid로 핵심 기능 6개 소개
- 각 기능 카드: 아이콘 + 제목 + 2~3줄 설명
- 예시 기능:
  1. **체크섬 기반 검증** — 모든 청크에 SHA-256 검증, 복원 시 자동 재확인
  2. **보존 정책 엔진** — 법적 보존, 규제 대응, 자동 만료 규칙
  3. **감사 로그** — 누가 언제 무엇에 접근했는지 전부 기록
  4. **빠른 복원** — 인덱스 기반 부분 복원, 전체 복원 모두 지원
  5. **다중 리전 복제** — 재해 복구를 위한 지역 간 자동 복제
  6. **개발자 친화 API** — CLI, REST API, Terraform provider 제공

## 사용 후기 (Testimonial)
- 3개의 고객 추천사 카드를 카루셀 또는 3-column으로 표시
- 각 카드: 인용 본문 + 작성자 이름/직책/회사
- 회사 로고를 카드 상단 또는 하단에 배치

## 가격 및 플랜 (Pricing)
- 3개 플랜 비교 (Starter / Team / Enterprise)
- 각 pricing-card: 플랜 이름, 월 요금, 주요 기능 목록, CTA 버튼
- Team 플랜을 "추천" 뱃지로 강조
- 카드 아래 기능 비교 테이블 (feature-comparison) — 상세 비교

## 자주 묻는 질문 (FAQ)
- 8~10개의 자주 묻는 질문을 아코디언으로 표시
- 각 FAQ 항목은 클릭 시 펼쳐짐, 한 번에 여러 개 펼침 허용
- 주요 질문 카테고리: 보안, 가격, 복원, 데이터 삭제, 규제 준수

## 최종 CTA 섹션 (Landing CTA Section)
- 푸터 바로 위 큰 전환 유도 섹션
- 배경: 브랜드 primary 색상 surface
- CTA 헤드라인 + 서포팅 카피 + primary/secondary 버튼 그룹
- 예: "지금 첫 아카이브를 만들어보세요 — 30일 무료 체험"

## 사이트 푸터 (Site Footer)
- 4~5개 링크 컬럼 (Product, Resources, Company, Legal)
- 각 컬럼 내 footer-link 5~8개
- 하단: 저작권, 법적 고지, 언어 전환, 소셜 링크 아이콘
- 다크 모드 친화 색상

## 랜딩 페이지 요구사항
- Core Web Vitals: LCP < 2.5s, CLS < 0.1, INP < 200ms
- 모든 이미지는 AVIF/WebP + lazy load
- 폰트 FOIT 방지 — Spoqa Han Sans Neo preload + font-display: swap
- 헤더/히어로는 초기 HTML에 인라인, 그 외 섹션은 IntersectionObserver로 fade-in
- 키보드로 모든 CTA·FAQ·네비 접근 가능
- prefers-reduced-motion 존중
- 다크 모드와 라이트 모드 둘 다 지원
