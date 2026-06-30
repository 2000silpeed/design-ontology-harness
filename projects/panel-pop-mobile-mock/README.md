# Panel Pop Mobile Mock

모바일 만화 잡지 앱 `Panel Pop`의 하네스 적용 목업입니다.

## 열기

정적 파일이라 브라우저에서 바로 열 수 있습니다.

```text
projects/panel-pop-mobile-mock/index.html
```

## Design System

`document-content--playful-soft` 프리셋을 raw CSS variables 어댑터로 설치했습니다.

```bash
uv run design-ontology install-preset \
  --preset-id document-content--playful-soft \
  --target-repo projects/panel-pop-mobile-mock \
  --adapter raw-css-variables \
  --color-mode light \
  --locale ko \
  --force
```

구현 전 기준 파일:

1. `design-system/IMPLEMENTATION_CONTRACT.md`
2. `design-system/STYLE.md`
3. `design-system/system_spec.md`
4. `design-system/token_schema.json`
5. `design-system/components/component_specs.md`

## 구성

- `index.html`: 모바일 앱 구조
- `styles.css`: 설치된 디자인 토큰 기반 목업 스타일
- `mockup.js`: 탭 전환, 저장 상태, 테마 전환, 토스트
- `assets/*.png`: imagegen으로 만든 original comic cover / panel visual assets
- `assets/*.svg`: 앱 아이콘과 이전 deterministic vector fallback
