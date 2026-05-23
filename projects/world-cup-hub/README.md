# World Cup Hub

월드컵 일정, 결과, 승부예측, 팬 의견을 한 화면에서 다루는 한국어 스포츠 데이터 커뮤니티 MVP입니다.

## Harness Source

- `brand_profile.json`: 제품 정체성, 토큰 방향, 레퍼런스 seed
- `spec.md`: IA, 플로우, 컴포넌트 요구사항
- `seeds/seed_urls.txt`: FIFA 공식 일정 페이지와 스포츠 데이터 레퍼런스
- `build/system/`: `design-ontology run-project`가 생성한 블루프린트, 토큰, 컴포넌트 스펙

## Static MVP

- `index.html`: 앱 화면
- `design-system/tokens.css`: 원본 색상, radius, font, 팀 색상 토큰
- `styles.css`: 원본값 없이 `--ds-*` 토큰을 소비하는 UI 스타일, light 기본 모드 + dark 대응 모드
- `app.js`: 일정 필터, 경기 선택, 예측 투표, 의견 작성 인터랙션
- Inline SVG icon sprite: 일정, 경기장, 예측, 결과, 출처 같은 반복 UI 신호용 결정론적 아이콘 세트
- `assets/app-icon.svg`: favicon, web app manifest, app shell brand mark에 연결된 브랜드 특정 앱 아이콘
- `site.webmanifest`: 앱 아이콘과 theme metadata
- `assets/world-cup-command-center.webp`: Codex `image_gen`으로 생성해 workspace에 복사한 hero 이미지
- `public/generated/design-system/manifest.json`: 전역 visual asset manifest 계약에 맞춘 provenance 기록

## Commands

```bash
uv run design-ontology run-project --project-dir projects/world-cup-hub --kb-dir kb/default
python3 -m http.server 8780 --directory projects/world-cup-hub
```

Then open `http://127.0.0.1:8780`.

## Data Note

The harness seed references the official FIFA World Cup 2026 schedule page. The current MVP uses static demo data so the interaction model can be tested before live schedule/result APIs are wired.
