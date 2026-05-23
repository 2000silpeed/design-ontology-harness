# Design System Seed Refresh Research

Date: 2026-05-23

## TL;DR

이번 업데이트는 “요즘 참고할 만한 공식 디자인 시스템” 중 현재 하네스의 `build-kb`가 바로 읽을 수 있는 후보를 우선 반영했다. Cloudscape, Paste, Garden, Helios, Forma 36, Nord, Modus, Shopify Polaris Web Components는 모두 1-page smoke에서 seed/reference/document 생성에 성공했고 CSS 토큰도 추출됐다.

## Added To Immediate KB Seeds

- AWS Cloudscape: cloud-console, data-heavy, ops workflow 참고에 강함.
- Twilio Paste: 접근성, composable primitives, patterns/page templates 구조가 좋음.
- Zendesk Garden: Garden 9 기준 components, tokens, theming coverage가 넓음.
- HashiCorp Helios: infra/devtool 제품군에 맞는 foundations/content/components/patterns 구성이 좋음.
- Contentful Forma 36: v5 refresh, tokens/components/playground, content-platform workflow에 적합.
- Nord Design System: healthcare/service product에 맞는 calm/a11y tone과 web components.
- Trimble Modus 2.0: enterprise/industrial SaaS, components/patterns/templates와 AI flow guidance.
- Shopify Polaris Web Components: React-era Polaris 대신 현재 Shopify Admin-native web component reference로 승격.

## Kept In Watchlist

- Salesforce SLDS 2: Winter '26 GA와 agentic/dark-mode 방향성이 중요하므로 benchmark에는 추가했지만, official public docs access가 변동적이라 browser-required watchlist에 유지.
- Material 3, Apple HIG, Adobe Spectrum: 여전히 high-value platform references지만 JS/browser-backed capture가 더 안정적.

## Lazyweb Visual Notes

Lazyweb desktop search에서 Apple HIG, Figma Design Systems, Origami docs, Windmill component guidelines 같은 문서형 UI가 반복적으로 잡혔다. 공통 패턴은 왼쪽 탐색, foundations/patterns/components 분리, 검색 중심 docs, component live examples, design-token entry point였다.

See `references/lazyweb-references.md` for the selected visual-reference metadata.

## Source Highlights

- Cloudscape exposes foundations, components, patterns, demos, Gen AI, and testing/development guides.
- Paste documents foundations, content, patterns, page templates, components, primitives, tokens, theme and customization layers.
- Garden 9 exposes foundations, design tokens, theming, and a broad component catalog.
- Forma 36 v5 added updated components plus accessibility improvements such as contrast, larger hit areas, and keyboard navigation.
- Shopify Polaris moved toward unified web components across Admin, Checkout, and Customer Accounts in 2025.

## Implementation Changes

- Added 8 crawler-friendly official URLs to `seeds/professional-design-systems.txt`.
- Removed legacy `polaris-react.shopify.com` from browser-required watchlist.
- Moved 11 existing 0-document professional seeds to the browser-required/source-refresh watchlist after full-pack smoke.
- Updated benchmark KB to include Cloudscape, Garden, Forma 36, Nord, Modus, and SLDS 2.
- Updated README and seed-pack docs to reflect 60 immediate seeds and 37 browser-required watchlist entries.
- Added seed-pack regression tests for duplicates, newly promoted URLs, and benchmark coverage.

Validation after cleanup: `build-kb --seeds-file seeds/professional-design-systems.txt --max-pages-per-source 1 --max-depth 0` produced seed 60 / reference 60 / document 60.

## Sources

- https://cloudscape.design/get-started/
- https://paste.twilio.design/introduction/about-paste
- https://garden.zendesk.com/components/
- https://helios.hashicorp.design/
- https://f36.contentful.com/
- https://www.contentful.com/developers/changelog/forma-36-v5-of-contentfuls-design-system-is-now-live/
- https://nordhealth.design/components/
- https://modus.trimble.com/
- https://shopify.dev/docs/api/app-home/web-components
- https://www.shopify.com/partners/blog/polaris-unified-and-for-the-web
- https://www.salesforce.com/blog/experience-design-with-slds-2/
