# Seed Packs

이 저장소는 이제 블로그형 큐레이션 글만이 아니라, 실제 디자인 시스템 사이트 URL 자체를 seed로 받을 수 있습니다.

그래서 seed는 두 층으로 관리하는 것을 권장합니다.

## 1. Immediate KB Seeds

파일: `seeds/professional-design-systems.txt`

용도:

- 현재 하네스에서 바로 `build-kb`에 넣어도 되는 공식 디자인 시스템 URL
- direct reference seed 방식으로 KB의 1급 입력이 됨

포함 기준:

- 공식 URL
- foundations / components / patterns / accessibility 같은 구조적 문서 진입점이 존재함
- 현재 크롤러가 HTML에서 유의미한 텍스트를 읽을 가능성이 높음

검증:

- 2026-04-13 기준 `uv run design-ontology build-kb --seeds-file seeds/professional-design-systems.txt --max-pages-per-source 1 --max-depth 0` 스모크 테스트 통과
- 결과: seed 13개 / reference 13개 / document 13개 / seed error 0개

## 2. Browser-Required Watchlist

파일: `seeds/browser-required-official-design-systems.txt`

용도:

- 공식적으로 매우 가치 있는 레퍼런스지만
- 현재의 requests + BeautifulSoup 크롤러에서는 텍스트가 거의 없거나
- JavaScript 렌더링 / 로그인 / 제한된 접근 방식 때문에 KB 품질이 낮을 수 있는 사이트

예:

- Material 3
- Apple Human Interface Guidelines
- Adobe Spectrum
- Salesforce Lightning Design System
- SAP Design System (현재 기본 httpx 요청에서 403 가능)
- Department for Education Design System (현재 robots.txt 차단)

## Recommended Usage

### Build a high-signal professional KB

```bash
uv run design-ontology build-kb \
  --kb-dir kb/professional \
  --seeds-file seeds/professional-design-systems.txt
```

### Use that KB in a project

```bash
uv run design-ontology init \
  --project-dir projects/my-app \
  --brand-name "My App" \
  --product-summary "What this product is for" \
  --kb-dir ../../kb/professional

uv run design-ontology run-project --project-dir projects/my-app
```

## Practical Rule

- 지금 당장 KB 품질이 중요한 경우: `professional-design-systems.txt`
- 브라우저 기반 수집기까지 붙일 계획이 있는 경우: `browser-required-official-design-systems.txt`도 함께 관리

## Current Professional Seed Pack

### Product / enterprise

- Atlassian Design
- GitHub Primer
- IBM Carbon
- Microsoft Fluent 2
- Clarity
- Elastic UI
- Mozilla Protocol

### Government / public service

- U.S. Web Design System
- GOV.UK Design System
- NHS Design System
- DWP Design System
- NHS App Design System
- MOD.UK Design System
