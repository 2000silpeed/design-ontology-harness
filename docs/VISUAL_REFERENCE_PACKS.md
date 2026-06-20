# Visual Reference Packs

Visual Reference Pack은 Omnigen뿐 아니라 웹 크롤링 결과, Lazyweb export, Figma export, Pinterest-assisted capture, 사용자가 모아 둔 스크린샷 폴더를 같은 형식으로 다루기 위한 패키지입니다.

이미지를 전부 본체에 넣지 않아도 됩니다. 기본은 `metadata`입니다. 필요할 때만 `copy`, `symlink`, `download`로 로컬 에셋을 붙입니다.

## Pack 구조

```text
reference-pack/
  pack.json
  assets.jsonl
  index.sqlite
  checksums.json
  assets/
```

`assets.jsonl`의 각 줄은 하나의 reference asset입니다.

```json
{
  "asset_id": "web-crawl:remote-crm-dashboard:abc123",
  "provider_id": "web-crawl",
  "category": "dashboard",
  "label": "Remote CRM dashboard",
  "tags": ["crm", "dashboard", "table"],
  "source_url": "https://example.com/case-study",
  "download_url": "https://cdn.example.com/crm-dashboard.png",
  "local_path": null,
  "usage_scope": "reference-analysis-only",
  "redistribution_allowed": false,
  "provenance_level": "referenced"
}
```

`local_path`가 있으면 `analyze-visuals`에서 실제 이미지 분석 대상으로 들어갑니다. `source_url`만 있는 lazy record는 Design Context Pack에는 남지만, 색상·서체·IA·copy의 근거가 되지는 않습니다.

## Local Folder Pack

```bash
uv run design-ontology build-reference-pack \
  --pack-id crm-local-screens \
  --source-dir references/crm-screens \
  --provider-id local-screenshots \
  --category dashboard \
  --tags "crm,analytics,table" \
  --materialize copy
```

`--materialize metadata`는 파일을 복사하지 않고 경로와 메타데이터만 기록합니다. 다른 사람도 같은 pack을 쓰게 하려면 `copy`나 별도 archive 배포가 더 안전합니다.

## Web Crawl / Lazy Pack

```bash
uv run design-ontology build-reference-pack \
  --pack-id crm-web-research \
  --source-url https://example.com/case-study \
  --category web-reference \
  --tags "public-web,reference-only" \
  --materialize metadata
```

이 경우 pack에는 page URL과 image URL이 기록됩니다. 원본 이미지를 저장하지 않기 때문에 배포가 가볍고, 라이선스가 불명확한 이미지를 실수로 재배포할 위험도 줄어듭니다.

검색 기반으로 넣을 때는 사용자가 찾은 공개 gallery/search URL을 `--source-url`에 넣습니다.

```bash
uv run design-ontology build-reference-pack \
  --pack-id public-dashboard-web-search \
  --source-url https://saasinterface.com/pages/dashboard/ \
  --source-url https://www.geckoboard.com/dashboard-examples/ \
  --provider-id public-web-search \
  --category web-reference \
  --tags "public-web,reference-only" \
  --materialize metadata \
  --max-assets 80
```

공통 `--tags`에는 검색어를 넣지 않는 편이 좋습니다. 예를 들어 모든 asset에 `dashboard`, `crm`, `saas`를 붙이면 자동 선별 점수가 비슷해져 로고나 CTA 이미지가 위로 올라올 수 있습니다. 공통 tag는 출처와 사용 정책만 나타내고, 실제 선별은 `--query`에 맡기는 편이 안정적입니다.

원본까지 내려받아 내부 pack으로 만들려면:

```bash
uv run design-ontology build-reference-pack \
  --pack-id crm-web-internal \
  --source-url https://example.com/case-study \
  --materialize download
```

다운로드한 이미지는 여전히 `reference-analysis-only`입니다. 실제 제품 에셋으로 쓰려면 별도의 license metadata와 attribution을 남겨야 합니다.

## Manifest Pack

크롤러, Lazyweb, Figma export, 다른 도구가 만든 JSON/JSONL을 pack으로 묶을 수 있습니다.

```bash
uv run design-ontology build-reference-pack \
  --pack-id lazyweb-crm-pack \
  --asset-manifest exports/lazyweb-crm-assets.jsonl \
  --provider-id lazyweb \
  --category dashboard
```

## 사용

설치된 pack 목록:

```bash
uv run design-ontology list-reference-packs
```

프로젝트에 reference 선별:

```bash
uv run design-ontology select-visual-references \
  --project-dir projects/my-app \
  --pack crm-web-research \
  --query "crm analytics dashboard contacts table" \
  --count 12 \
  --sync-sources
```

선택 결과를 눈으로 검수:

```bash
uv run design-ontology export-reference-gallery \
  --pack crm-web-research \
  --selection projects/my-app/build/visuals/visual_reference_pack_selection.json \
  --output projects/my-app/reference-gallery.html
```

그 다음은 기존 흐름과 같습니다.

```bash
uv run design-ontology analyze-visuals --project-dir projects/my-app
uv run design-ontology run-project --project-dir projects/my-app
```

## 권장 원칙

- Public pack은 `metadata + thumbnail` 중심으로 작게 유지합니다.
- 라이선스가 불명확한 웹 이미지는 `source_url`, `download_url`, metadata만 둡니다.
- 사용자가 직접 제공한 스크린샷이나 내부 레퍼런스는 `copy` pack으로 묶을 수 있습니다.
- Omnigen vault는 그대로 둘 수 있고, 필요하면 같은 pack 형식으로 변환할 수 있습니다.
- Pack 선택 결과는 `visual_reference_pack_selection.json`에 남겨 재현성을 확보합니다.
