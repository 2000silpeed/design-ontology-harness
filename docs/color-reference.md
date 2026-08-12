# REFERENCE X Vol.1 - Color Reference

<!-- design-ontology-runtime-color-policy:begin sha256=d4f8fc709c8599e384efcba2eb6e2d19458f50c55701ad335609d560737c65db -->
<details>
<summary>Typed runtime color role policy</summary>

이 정책은 UI의 중립색·상태색·크롬 기본값과 다크 모드 파생 규칙을 정의합니다. `ColorKeyword`가 아니라 런타임 역할 정책입니다. 프로젝트가 선택한 브랜드 원색 좌표는 `brand-*` 역할에 그대로 보존하고, 실제 시맨틱 런타임 역할에는 아래 대비 하한을 적용합니다.

```design-ontology-runtime-color-policy+json
{
  "authority": {
    "distinction": "Runtime role defaults and derivation rules are not ColorKeyword nodes.",
    "kind": "typed-runtime-role-policy",
    "source_reference_id": "docs-color-reference-runtime-role-policy",
    "transport": "docs/color-reference.md"
  },
  "chrome_roles": {
    "chrome_canvas": {
      "kind": "runtime-chrome-role",
      "mood": "미세 그레이 캔버스",
      "name": "Chrome Canvas",
      "source_reference_id": "docs-color-reference-runtime-role-policy",
      "usage": "앱 배경. 표면과 1단계 분리.",
      "value": "#FAFAFA"
    },
    "chrome_ink": {
      "kind": "runtime-chrome-role",
      "mood": "무채색 크롬 잉크. 텍스트와 primary action을 담당",
      "name": "Chrome Ink",
      "source_reference_id": "docs-color-reference-runtime-role-policy",
      "usage": "본문, 헤딩, 블랙 CTA. 상품 이미지가 컬러를 담당하므로 크롬은 무채색을 유지한다.",
      "value": "#141414"
    },
    "chrome_line": {
      "kind": "runtime-chrome-role",
      "mood": "헤어라인",
      "name": "Chrome Line",
      "source_reference_id": "docs-color-reference-runtime-role-policy",
      "usage": "구분선, 보더. 그림자보다 라인 분리를 우선.",
      "value": "#E5E5E5"
    },
    "chrome_muted": {
      "kind": "runtime-chrome-role",
      "mood": "보조 텍스트 그레이",
      "name": "Chrome Muted",
      "source_reference_id": "docs-color-reference-runtime-role-policy",
      "usage": "메타 정보, 캡션, 비활성 라벨.",
      "value": "#737373"
    },
    "chrome_paper": {
      "kind": "runtime-chrome-role",
      "mood": "순백 표면",
      "name": "Chrome Paper",
      "source_reference_id": "docs-color-reference-runtime-role-policy",
      "usage": "카드/시트 표면. 사진의 색이 그대로 읽히는 바탕.",
      "value": "#FFFFFF"
    }
  },
  "citation_aliases": {
    "1": "ref-reference-x-vol1-color",
    "2": "ref-reference-x-vol1-color",
    "3": "ref-reference-x-vol1-color",
    "4": "ref-reference-x-vol1-color",
    "5": "ref-reference-x-vol1-color",
    "6": "ref-reference-x-vol1-color"
  },
  "dark_derivation": {
    "chromatic_lightness_delta": 0.18,
    "chromatic_lightness_range": [
      0.42,
      0.72
    ],
    "chromatic_min_saturation": 0.45,
    "contrast_floor": {
      "adjustment_target_role": "ink",
      "background_roles": [
        "surface",
        "ink-inverse"
      ],
      "chromatic_roles": [
        "primary",
        "accent",
        "link-hover",
        "info",
        "success",
        "warning",
        "danger",
        "link"
      ],
      "kind": "wcag-contrast-floor",
      "minimum_ratio": 4.5
    },
    "kind": "derived-runtime-role-policy",
    "method": "hsl-role-targets",
    "neutral_max_saturation": 0.12,
    "non_text_contrast_floor": {
      "adjusted_roles": [
        "border-strong"
      ],
      "adjustment_target_role": "ink",
      "background_roles": [
        "surface",
        "canvas",
        "surface-muted"
      ],
      "kind": "wcag-contrast-floor",
      "minimum_ratio": 3.0,
      "scope": "non-text-ui-component-boundary"
    },
    "role_lightness_targets": {
      "border": 0.2,
      "border-strong": 0.28,
      "canvas": 0.06,
      "ink": 0.94,
      "ink-inverse": 0.1,
      "ink-muted": 0.72,
      "ink-subtle": 0.56,
      "surface": 0.09,
      "surface-elevated": 0.11,
      "surface-muted": 0.13,
      "surface-tint": 0.22
    }
  },
  "light_contrast_floor": {
    "adjustment_target_role": "ink",
    "background_roles": [
      "surface",
      "ink-inverse"
    ],
    "chromatic_roles": [
      "primary",
      "accent",
      "link-hover",
      "info",
      "success",
      "warning",
      "danger",
      "link"
    ],
    "kind": "wcag-contrast-floor",
    "minimum_ratio": 4.5
  },
  "light_roles": {
    "accent": {
      "kind": "runtime-role-default",
      "source_reference_id": "docs-color-reference-runtime-role-policy",
      "value": "#F59E0B"
    },
    "border": {
      "kind": "runtime-role-default",
      "source_reference_id": "docs-color-reference-runtime-role-policy",
      "value": "#D6DDE6"
    },
    "border-strong": {
      "kind": "runtime-role-default",
      "source_reference_id": "docs-color-reference-runtime-role-policy",
      "value": "#9AA6B2"
    },
    "canvas": {
      "kind": "runtime-role-default",
      "source_reference_id": "docs-color-reference-runtime-role-policy",
      "value": "#F7F8FA"
    },
    "danger": {
      "kind": "runtime-role-default",
      "source_reference_id": "docs-color-reference-runtime-role-policy",
      "value": "#B91C1C"
    },
    "info": {
      "kind": "runtime-role-default",
      "source_reference_id": "docs-color-reference-runtime-role-policy",
      "value": "#2F6FEB"
    },
    "ink": {
      "kind": "runtime-role-default",
      "source_reference_id": "docs-color-reference-runtime-role-policy",
      "value": "#0F172A"
    },
    "ink-inverse": {
      "kind": "runtime-role-default",
      "source_reference_id": "docs-color-reference-runtime-role-policy",
      "value": "#FFFFFF"
    },
    "ink-muted": {
      "kind": "runtime-role-default",
      "source_reference_id": "docs-color-reference-runtime-role-policy",
      "value": "#475569"
    },
    "ink-subtle": {
      "kind": "runtime-role-default",
      "source_reference_id": "docs-color-reference-runtime-role-policy",
      "value": "#64748B"
    },
    "link": {
      "derived_from": "primary",
      "kind": "derived-runtime-role",
      "source_reference_id": "docs-color-reference-runtime-role-policy"
    },
    "link-hover": {
      "derived_from": "link",
      "kind": "derived-runtime-role",
      "source_reference_id": "docs-color-reference-runtime-role-policy"
    },
    "primary": {
      "kind": "runtime-role-default",
      "source_reference_id": "docs-color-reference-runtime-role-policy",
      "value": "#2563EB"
    },
    "success": {
      "kind": "runtime-role-default",
      "source_reference_id": "docs-color-reference-runtime-role-policy",
      "value": "#15803D"
    },
    "surface": {
      "kind": "runtime-role-default",
      "source_reference_id": "docs-color-reference-runtime-role-policy",
      "value": "#FFFFFF"
    },
    "surface-elevated": {
      "derived_from": "surface",
      "kind": "derived-runtime-role",
      "source_reference_id": "docs-color-reference-runtime-role-policy"
    },
    "surface-muted": {
      "kind": "runtime-role-default",
      "source_reference_id": "docs-color-reference-runtime-role-policy",
      "value": "#EEF1F6"
    },
    "surface-tint": {
      "kind": "runtime-role-default",
      "source_reference_id": "docs-color-reference-runtime-role-policy",
      "value": "#E0E7FF"
    },
    "warning": {
      "kind": "runtime-role-default",
      "source_reference_id": "docs-color-reference-runtime-role-policy",
      "value": "#B45309"
    }
  },
  "non_text_contrast_floor": {
    "adjusted_roles": [
      "border-strong"
    ],
    "adjustment_target_role": "ink",
    "background_roles": [
      "surface",
      "canvas",
      "surface-muted"
    ],
    "kind": "wcag-contrast-floor",
    "minimum_ratio": 3.0,
    "scope": "non-text-ui-component-boundary"
  },
  "schema_version": "design-ontology-harness/runtime-color-policy-v1"
}
```

</details>
<!-- design-ontology-runtime-color-policy:end -->

## Standard Reds

### Pure Red
- **HEX**: #FF0000
- **CMYK**: C 0%, M 95%, Y 96%, K 0%
- **톤/무드**: 순수 원색 레드 계열, 고채도와 중명도의 강렬한 톤 / 열정, 에너지, 주목성, 상징적, 강렬함
- **활용**: 모든 컬러 체계의 중심축이자 원색 중 가장 상징적인 색. 디지털 환경의 UI 포인트 컬러, 경고, 알림 등에 사용되며 브랜딩에서 강한 메시지나 행동 유도(CTA)에 적합함.
- **배색**: `#FFFFFF` `#000000` `#F5E3C3` `#1A2E47` `#BDBDBD`
- **출처**: [1]

### Scarlet
- **HEX**: #FF2400
- **CMYK**: C 0%, M 91%, Y 96%, K 0%
- **톤/무드**: 강렬한 주황빛 레드 계열, 고채도와 고명도의 따뜻한 톤 / 활기, 생동감, 열정, 역동성, 주목성
- **활용**: 퓨어 레드보다 따뜻하고 오렌지에 가까운 색으로 에너지가 강하고 시각적 임팩트가 큼. 긍정적이고 낙천적인 인상을 주며 브랜드, 패션, 스포츠 디자인에서 활력 강조용으로 사용됨.
- **배색**: `#FFFFFF` `#1C2A44` `#F4E1C1` `#3B3B3B` `#C7E8D1` `#D4AF37`
- **출처**: [1]

### Crimson
- **HEX**: #BD2E4A
- **CMYK**: C 20%, M 97%, Y 61%, K 11%
- **톤/무드**: 짙은 레드 계열, 중채도와 저명도의 깊은 톤 / 고급스러움, 강렬함, 감정적, 웅장함, 고전적
- **활용**: 일반적인 레드보다 어둡고 무게감이 있으며 진중함과 정서적 깊이를 지님. 전통적이면서 강한 존재감으로 포멀한 인상을 연출함. 예술, 패션, 와인, 클래식 분야에서 주로 사용됨.
- **배색**: `#FFFFFF` `#D4AF37` `#F5E3C3` `#3B3B3B` `#EAD9B7`
- **출처**: [1]

### Ruby
- **HEX**: #E11F51
- **CMYK**: C 11%, M 96%, Y 55%, K 2%
- **톤/무드**: 채도 높은 레드 핑크 계열, 중명도 이상의 비교적 밝은 톤 / 화려함, 관능, 세련, 에너지, 주목성
- **활용**: 레드와 핑크의 경계에서 투명감이 느껴지는 색. 감정 자극이 강해 패션, 뷰티, 럭셔리 카테고리에서 빈번히 사용되며 금속성, 새틴 질감과 결합 시 효과가 극대화됨.
- **배색**: `#FFFFFF` `#1C2A44` `#F3C1CF` `#3B3B3B` `#D4AF37` `#2AA6A1`
- **출처**: [1]

## Natural Reds

### Coral Red
- **HEX**: #E44327
- **CMYK**: C 10%, M 85%, Y 89%, K 0%
- **톤/무드**: 오렌지와 레드, 핑크 계열의 기미를 띠는 밝은 톤 / 생동감, 건강함, 자연스러움, 긍정적
- **활용**: 산호의 따뜻한 느낌을 내세우며 오렌지 레드 계열로 분류됨. 자연광 아래의 온기를 띠며 활력을 전달함. 패션, 식음료, 자연주의 브랜딩에서 시각적 거부감 없이 생동감을 표현함.
- **배색**: `#F8EFE7` `#8C7A4E` `#87CEEB` `#D7B89C` `#2E2E2E` `#A9D9C1`
- **출처**: [1]

### Terracotta
- **HEX**: #E2725B
- **CMYK**: C 12%, M 66%, Y 62%, K 2%
- **톤/무드**: 붉은 흙빛 계열, 오렌지 브라운이 섞인 따뜻한 중채 레드 / 안정감, 따뜻함, 자연스러움, 감성적
- **활용**: 토기나 점토의 붉은 빛에서 유래된 흙색 계열로 자연과 인간의 연결성을 상징함. 라이프스타일, 리빙, 인테리어 브랜드에서 감성적 내추럴 무드로 사용되며 다층적 색감이 특징임.
- **배색**: `#DCC7AA` `#8A8D58` `#B3A497` `#F5EBDD` `#9AB3C4` `#3D3D3D`
- **출처**: [1]

### Rose Red
- **HEX**: #C21E56
- **CMYK**: C 20%, M 99%, Y 45%, K 9%
- **톤/무드**: 중간 명도의 레드와 핑크 사이, 맑고 따뜻한 장미빛 톤 / 로맨틱, 감성적, 생동감, 부드러움
- **활용**: 자연 속 장미의 붉음을 닮은 색으로 생명력과 낭만을 상징함. 일반적 레드의 강렬함보다 부드러운 느낌을 강조하며 뷰티, 패션, 패키징 분야에서 사랑과 우아함을 전달할 때 사용됨.
- **배색**: `#FAF3E5` `#A7B89F` `#98AFC7` `#D8B9A3` `#434343` `#F08080`
- **출처**: [1]

## Deep Reds

### Oxblood
- **HEX**: #4A0404
- **CMYK**: C 45%, M 100%, Y 82%, K 70%
- **톤/무드**: 붉은 와인빛의 브라운 레드, 거의 블랙에 가까운 딥톤 / 고급스러움, 성숙함, 강렬함, 깊은 감정
- **활용**: 황소의 피라는 어원에서 유래된 강인한 상징성을 지닌 컬러. 와인보다 딥한 브라운에 가까워 중후하며 럭셔리, 클래식, 빈티지 브랜드에서 권위감과 정체성을 강화할 때 사용됨.
- **배색**: `#F6F2EC` `#B1A295` `#C58B88` `#C19A4B` `#6B6A41` `#2E2E2E`
- **출처**: [1]

### Claret
- **HEX**: #7F1734
- **CMYK**: C 30%, M 100%, Y 58%, K 40%
- **톤/무드**: 중명도의 루비 와인색, 붉은빛이 도는 퍼플 레드 / 세련됨, 관능적, 품격 있는, 고급스러운
- **활용**: 프랑스산 적포도주에서 유래된 컬러로 와인의 깊은 붉은빛을 함축함. 옥스블러드보다 덜 어둡고 상그리아보다 절제된 우아함이 느껴지며 고급 브랜드나 향수, 주얼리 분야에 자주 사용됨.
- **배색**: `#D8BFAA` `#2E2E2E` `#D4979B` `#7C6746` `#F3EFEA` `#C9A54E`
- **출처**: [1]

### Sangria
- **HEX**: #9C1F4B
- **CMYK**: C 27%, M 100%, Y 44%, K 20%
- **톤/무드**: 보라빛이 섞인 붉은 와인색, 따뜻하고 풍부한 중명도 레드 / 관능적, 생동감 있는, 여유로운, 감각적
- **활용**: 스페인 전통 와인 음료에서 유래된 색으로 과일의 달콤함과 깊이를 동시에 품음. 클라렛보다 붉은빛이 강하고 옥스블러드보다 생기가 강조되어 편안하고 낭만적인 인상을 줌.
- **배색**: `#D9C5A0` `#F5E9D9` `#7B8B65` `#667C93` `#E2725B` `#2F2F2F`
- **출처**: [1]

## Pastel Reds

### Salmon
- **HEX**: #FA8072
- **CMYK**: C 2%, M 62%, Y 48%, K 0%
- **톤/무드**: 밝고 따뜻한 핑크 오렌지 톤 / 따뜻함, 부드러움, 친근함, 자연스러움
- **활용**: 연어살 색에서 유래된 자연스러운 핑크빛 오렌지 컬러. 붉은 계열 중에서도 자극이 거의 없고 감정적으로 온화한 인상을 형성함. 피부 톤에 가까워 화장품이나 포근함을 전달하는 감성 컬러로 적합함.
- **배색**: `#FDF6EC` `#B9C5A0` `#8BA8C9` `#414141` `#E4C9A1` `#F5F5F5`
- **출처**: [1]

### Blush
- **HEX**: #F9C0C4
- **CMYK**: C 2%, M 32%, Y 13%, K 0%
- **톤/무드**: 아주 연한 핑크 톤, 미세한 살구빛이 섞인 고명도 파스텔 / 섬세함, 순수함, 따뜻한 감정, 부드러움
- **활용**: 얼굴에 피어오르는 홍조를 닮은 색으로 감정의 미세한 떨림을 시각화함. 살몬보다 채도와 명도가 높아 더 여성적이고 공기감이 느껴짐. 안정적인 감정 표현과 브랜드 친화력을 높이는 역할.
- **배색**: `#FAF7F2` `#D8D8D8` `#B7C3A5` `#E5CBB0` `#A3B9D2` `#B08672`
- **출처**: [1]

## Pantone Trend Reds

### Rose Quartz
- **HEX**: #F7CAC9
- **CMYK**: C 0%, M 18%, Y 19%, K 3%
- **톤/무드**: 고명도, 저채도, 살구빛이 섞인 파스텔 핑크 / 부드러움, 친근함, 따뜻함, 크래프트, 달콤한 소비자 감성
- **활용**: 팬톤 2016 올해의 색상 Rose Quartz 로 선정된 핑크 톤. 연어빛 웜 베이스에 순수한 공기감이 섞여 있으며 D2C 컨슈머 스낵 · 유아용품 · 웰니스 푸드 등 playful-soft commerce 에서 primary 팔레트 로 적합. Blush 보다 살짝 코랄기가 돌아 친근함을 강조.
- **배색**: `#FFEBCD` `#E9967A` `#B0E0E6` `#3F3F3F` `#F5DEB3` `#D9D9D9`
- **Semantic ID**: `color-keyword-pantone-coy-2016-rose-quartz`
- **Ontology Family**: `pantone_trend`
- **Ontology Category**: `Pantone Color of the Year`
- **출처 ID**: `ref-pantone-coy-announcements`

### Marsala
- **HEX**: #964F4C
- **CMYK**: C 29%, M 72%, Y 59%, K 26%
- **톤/무드**: 적갈색 계열, 와인과 브라운 사이의 중후한 톤 / 성숙함, 안정감, 관능적, 가을/겨울, 클래식
- **활용**: 단순한 레드가 아닌 시간이 숙성된 레드라 표현될 만큼 딥한 컬러. 디지털보다는 오프라인 패키지나 브랜드 톤에 적합하며 와인/푸드/패션 카테고리에서 강력하게 쓰임.
- **배색**: `#D4AF37` `#F5F5DC` `#D9C2AD` `#A39887` `#B8860B` `#9C9B7A`
- **출처**: [2]

### Grenadine
- **HEX**: #DC4C46
- **CMYK**: C 13%, M 82%, Y 70%, K 3%
- **톤/무드**: 밝고 따뜻한 레드 오렌지 계열, 중채도 이상의 밝은 톤 / 활력, 열정, 관능, 현대적
- **활용**: 과일 그레나딘 시럽의 붉은빛에서 유래된 컬러로 즉각적인 시각적 임팩트를 지님. 오렌지와 레드의 경계에서 밝고 따뜻한 인상이 형성되어 패션, 디지털 브랜드 등에서 주목성 포인트로 활용됨.
- **배색**: `#FFFFFF` `#2F2F2F` `#E8D9CA` `#2E8A87` `#C9A44B` `#D1D1D1`
- **출처**: [2]

### Goji Berry
- **HEX**: #CC142F
- **CMYK**: C 16%, M 100%, Y 80%, K 7%
- **톤/무드**: 중명도의 레드 계열, 약간의 와인 색감이 도는 밝은 레드 톤 / 생기, 세련됨, 감각적, 젊음
- **활용**: 팬톤이 대담하면서도 자연적인 에너지 컬러로 제시한 붉은 톤. 마르살라보다 밝고 채도가 높으며 그레나딘보다 감정적 깊이가 있음. 과일 고지베리의 건강함과 생동감을 전달하며 뷰티 산업에 적합함.
- **배색**: `#33EBD0` `#111184` `#FFFFE3` `#696969` `#EFBF04` `#6CC142`
- **출처**: [2]

## Standard Oranges

### Pure Orange
- **HEX**: #FFA500
- **CMYK**: C 0%, M 42%, Y 94%, K 0%
- **톤/무드**: 순수 오렌지 계열, 고채도 중명도 / 활력, 낙관, 따뜻함, 개방감
- **활용**: 빨간 계열의 에너지와 노란 계열의 낙관이 만난 밸런스 톤. 채도가 높아 주목성이 매우 강함. 대면적 사용 시 피로감을 줄 수 있어 비율 조절이 필요함.
- **배색**: `#14213D` `#138A8A` `#B3B3B3` `#FFF6E5` `#6A7DA8` `#2E6B4E`
- **출처**: [2]

### Tangerine
- **HEX**: #F28500
- **CMYK**: C 5%, M 97%, Y 98%, K 0%
- **톤/무드**: 고채도 중명도 오렌지, 약간의 레드 계열 포함 / 따뜻함, 에너지, 활기, 긍정적 낙관
- **활용**: 레드보다 부드럽고 옐로보다 강한 중간 색. 태양빛이 내리쬐는 따뜻한 인상을 주며 생명력이 느껴짐. 식음료, 패션, 테크 브랜드의 메인 포인트로 자주 사용됨.
- **배색**: `#36454F` `#FFF8E1` `#0D5C63` `#708238` `#0047AB` `#EED6A0`
- **출처**: [2]

### Ochre
- **HEX**: #CC7722
- **CMYK**: C 18%, M 60%, Y 94%, K 6%
- **톤/무드**: 중명도, 중채도, 흙기 섞인 따뜻한 오렌지 / 안정감, 내추럴, 신뢰감, 지속성
- **활용**: 토양 및 목재의 질감과 맞닿은 자연 기반 톤. 주황의 활기를 유지하면서도 과하지 않은 차분함이 특징. 디지털과 인쇄 등 모든 재질에서 존재감이 높고 안정적인 브랜딩에 강점이 있음.
- **배색**: `#1C2E4A` `#4C7A77` `#D7B899` `#F3E9DA` `#6E7B8B` `#B6B995`
- **출처**: [2]

## Natural Oranges

### Apricot
- **HEX**: #FFB27F
- **CMYK**: C 1%, M 38%, Y 51%, K 0%
- **톤/무드**: 밝은 명도, 낮은 채도, 살짝 핑크빛이 도는 부드러운 오렌지 / 따뜻함, 부드러움, 친근함, 여유, 자연스러움
- **활용**: 살구 빛에서 유래된 온화한 컬러. 주황의 활기를 보존하면서 부드러운 감정선을 형성함. 브랜딩 영역에서 심리적 안정감을 제공하기 용이함.
- **배색**: `#F8F3ED` `#B9B4A5` `#9A9E56` `#F88379` `#6B90B4` `#7E5A45`
- **출처**: [2]

### Persimmon
- **HEX**: #EC5800
- **CMYK**: C 6%, M 76%, Y 100%, K 0%
- **톤/무드**: 명도, 고채도, 오렌지와 레드 사이의 진한 웜톤 / 생동감, 따뜻함, 안정감, 자연의 활기
- **활용**: 감의 껍질빛에서 유래된 오렌지 레드 톤. 오렌지의 활력과 레드의 깊이를 동시에 지님. 가을, 전통, 핸드크래프트 계열의 색조와 조화로움이 높음.
- **배색**: `#DCC9B6` `#C49E72` `#8A8653` `#2B3A4B` `#F4EEDF` `#5A3825`
- **출처**: [2]

### Pumpkin
- **HEX**: #FF7518
- **CMYK**: C 0%, M 65%, Y 90%, K 0%
- **톤/무드**: 중명도와 중채도, 오렌지와 브라운 사이의 따뜻한 톤 / 풍요로움, 활기, 따뜻한 계절감, 안정된 에너지
- **활용**: 햇살에 비친 복숭아 빛에서 유래된 온화한 컬러. 주황의 활기를 보존하면서 부드러운 감정선을 형성. 브랜딩 영역에서 심리적 안정감을 제공하기 용이함.
- **배색**: `#F6F1E7` `#6B5B3E` `#D3A635` `#2E4C2F` `#A69C8F` `#3B3B3B`
- **출처**: [2]

## Deep Oranges

### Rust
- **HEX**: #B7410E
- **CMYK**: C 21%, M 84%, Y 100%, K 10%
- **톤/무드**: 저명도, 중채도, 오렌지와 브라운의 중간 영역 / 빈티지, 견고함, 따뜻한 노스탤지어, 공예적 감성
- **활용**: 금속 산화에서 비롯된 시간의 흐름을 상징하는 색. 브라운의 안정감과 오렌지의 온기를 동시에 지님. 빈티지 스타일, 가죽 제품 등에 자주 활용됨.
- **배색**: `#D8C4A5` `#3B3B3B` `#A7B29C` `#F4EEE2` `#354B68` `#8C5230`
- **출처**: [2]

### Copper
- **HEX**: #B87333
- **CMYK**: C 22%, M 57%, Y 85%, K 13%
- **톤/무드**: 저명도, 중채도, 오렌지와 레드 브라운 사이의 금속성 톤 / 고급스러움, 따뜻함, 전통적 질감, 세련된 무게감
- **활용**: 금속 구리에서 유래된 깊은 오렌지 브라운 계열. 광택이 없는 매트한 구리빛은 고급스러우면서도 내추럴한 인상을 줌. 패키지, 인테리어 산업 제품에서 프리미엄 라인에 주로 사용됨.
- **배색**: `#F6F1E7` `#6B6F74` `#7B7753` `#2C2C2C` `#C26748` `#D7BA99`
- **출처**: [2]

### Burnt Orange
- **HEX**: #CC5500
- **CMYK**: C 17%, M 76%, Y 100%, K 6%
- **톤/무드**: 저명도, 중고채도, 오렌지와 브라운이 섞인 짙은 톤 / 따뜻함, 향수, 빈티지, 성숙함
- **활용**: 이름 그대로 '태운 오렌지색'으로 따뜻한 에너지와 깊이를 동시에 가진 색. 햇볕에 그을린 듯한 톤으로 시간의 흔적을 표현함. 패션, 인테리어 등에서 성숙한 계절감과 균형을 줄 때 사용됨.
- **배색**: `#F4EEE2` `#B59F74` `#2E3C53` `#7C6F4B` `#D8C4A5` `#A89F95`
- **출처**: [2]

## Pastel Oranges

### Peach Puff
- **HEX**: #FFDAB9
- **CMYK**: C 0%, M 18%, Y 27%, K 0%
- **톤/무드**: 고명도, 저채도, 오렌지와 핑크 사이의 파스텔 계열 / 따뜻함, 부드러움, 순수함, 친근함, 생기
- **활용**: 인간적인 온기와 생동감을 상징하는 대표적 파스텔 톤. 형광빛 없이 자연스러운 살구색 계열로 피부 톤과 가장 조화로운 웜 계열 중 하나. 패션, 뷰티 브랜딩에서 포근함과 신뢰감을 표현할 때 사용.
- **배색**: `#FAF6F0` `#D7D7D7` `#F4A6A1` `#AEE1CD` `#9C7358` `#D8B4E2`
- **출처**: [2]

### Coral Blush
- **HEX**: #F88379
- **CMYK**: C 3%, M 61%, Y 45%, K 0%
- **톤/무드**: 고명도와 중저채도, 핑크와 오렌지 사이의 따뜻한 색조 / 감성적, 따뜻함, 세련됨, 우아함
- **활용**: 피치보다 한층 더 로맨틱한 방향의 오렌지 톤으로 핑크와 코랄이 섬세하게 섞인 색. 피부 톤과 자연스럽게 어우러지며 친근하면서도 고급스러운 인상을 줌. 패션, 뷰티, 웨딩 브랜딩에서 자주 쓰임.
- **배색**: `#FAF7F4` `#C48B8B` `#B8A79A` `#B4C1A1` `#AFA8A0` `#C9DCE8`
- **출처**: [2]

### Creamsicle
- **HEX**: #FFD7A0
- **CMYK**: C 2%, M 19%, Y 40%, K 0%
- **톤/무드**: 고명도, 저채도, 크리미하고 부드러운 오렌지 계열 / 부드러움, 경쾌함, 청량함, 달콤함
- **활용**: 바닐라 크림과 오렌지를 섞은 듯한 따뜻한 파스텔 톤. 밝고 가벼운 인상으로 시각적 피로도가 적으며 젊고 생동감 있는 이미지에 적합함. 코랄 블러시와 마찬가지로 패션 및 뷰티 분야에서 자주 활용됨.
- **배색**: `#FFFFFF` `#C7E9CF` `#E3C9A8` `#F7A589` `#A9C4D8` `#CFC6BA`
- **출처**: [2, 3]

### Dark Salmon
- **HEX**: #E9967A
- **CMYK**: C 0%, M 36%, Y 48%, K 9%
- **톤/무드**: 중명도, 중채도, 테라코타 기가 섞인 웜 살몬 톤 / 따뜻함, 크래프트, 친근함, 세련된 노스탤지어
- **활용**: CSS 표준 색상 이름 "Dark Salmon" 에 해당하는 Pastel/Natural Orange 경계의 웜 톤. Salmon 보다 한 단계 깊이와 테라코타 기가 돌아 craft D2C 상품 패키지 · bestseller ribbon · discount pill · gentle-toast 성공 등 consumer commerce accent 로 적합. Pastel Pink primary 와 합쳐 warm pastel commerce playful-soft 톤을 완성.
- **배색**: `#F7CAC9` `#FFEBCD` `#3F3F3F` `#F5F5F5` `#D7C4A3` `#FAF8F2`
- **Semantic ID**: `color-keyword-local-dark-salmon`
- **Spectrum**: `orange`
- **Ontology Family**: `local_extension`
- **Ontology Category**: `Pastel Oranges`
- **Source Type**: `markdown-local-extension`
- **출처**: [2] `ref-docs-color-reference-local-extensions`

## Pantone Trend Oranges

### Living Coral
- **HEX**: #FF6F61
- **CMYK**: C 0%, M 69%, Y 56%, K 0%
- **톤/무드**: 중명도, 중채도, 선명한 코랄 계열의 오렌지 톤 / 생동감, 따뜻함, 낙관적
- **활용**: 디지털 기술과 소셜 미디어가 일상에 자리 잡으며 느끼는 피로감에 대한 반작용으로 정의됨. 분홍빛과 주황빛이 공존하며 생명력과 교감의 이미지를 전달. 바다 산호에서 영감을 받아 자연과 기술이 공존하는 감성을 표현.
- **배색**: `#E8D4C5` `#A8E3D2` `#D6C5B2` `#F9F5EF` `#5078A0` `#A8A77D`
- **출처**: [3]

### Flame
- **HEX**: #F2552C
- **CMYK**: C 4%, M 78%, Y 84%, K 0%
- **톤/무드**: 중명도, 고채도, 강렬한 레드 & 오렌지 계열 / 열정적, 활발함, 도전적, 파워풀
- **활용**: 강렬한 빛 속의 에너지 움직임을 상징하는 컬러로 스포츠 브랜드 아이덴티티에 자주 활용됨. 붉은기와 황색이 섞인 동적 밸런스가 특징이며 광고 및 디지털 UI에서 CTA 컬러로도 효과적임.
- **배색**: `#111111` `#F8F5EF` `#4C4C4C` `#5C7BAA` `#D9B68C` `#1F3044`
- **출처**: [3]

### Chili Oil
- **HEX**: #944537
- **CMYK**: C 28%, M 77%, Y 74%, K 28%
- **톤/무드**: 저명도, 저채도, 레드 브라운 계열의 딥한 오렌지 톤 / 고급스러움, 안정감, 따뜻함, 자연
- **활용**: 매운 조미료의 색감에서 착안된 컬러로 붉은 열기와 흙빛 온기가 조화된 자연 중심형 톤. 인테리어 산업과 가죽, 모직 소재에서 강점이 있으며 디지털에서도 따뜻한 온 톤 배색으로 고급 무드 형성 가능.
- **배색**: `#F4F1EC` `#C79A6D` `#6C7150` `#D7A5A0` `#5A5E5E` `#E8DCC7`
- **출처**: [3]

## Standard Yellows

### Lemon Yellow
- **HEX**: #FFF44F
- **CMYK**: C 8%, M 0%, Y 74%, K 0%
- **톤/무드**: 고명도, 고채도, 순황색 축에 가까운 옐로 톤 / 경쾌함, 낙관, 청량감, 에너지
- **활용**: 가장 직관적으로 '노란색'으로 인식되는 기준 축. 빛, 주의, 활력을 상징하며 즉시 주목을 끌어올림. UI/표지/사인 등 가시성 중심 매체에 효과적이며 인쇄 시 백색 대비로 밝기 체감 극대화됨.
- **배색**: `#1E2A45` `#3E3E3E` `#6EC1E4` `#2E6B3F` `#F9F5EF` `#FF7E47`
- **출처**: [3]

### Goldenrod
- **HEX**: #DAA520
- **CMYK**: C 16%, M 35%, Y 93%, K 3%
- **톤/무드**: 중명도, 중채도, 옐로 오렌지 계열 / 따뜻함, 안정감, 고급스러움, 빈티지 감성
- **활용**: 황금빛이 감도는 중명도 계열의 옐로 오렌지 톤으로 밝은 옐로와 달리 중후한 인상을 주는 컬러. 특히 패션, 리빙 분야에서 '따뜻하지만 과하지 않은' 노란빛 포인트로 활용. 부드럽고 세련된 무드 형성.
- **배색**: `#F6F4E6` `#6B705C` `#8B5A2B` `#7A9EAF` `#3F3F3F` `#5C1A1B`
- **출처**: [3]

### Amber
- **HEX**: #FFBF00
- **CMYK**: C 4%, M 28%, Y 92%, K 0%
- **톤/무드**: 중명도, 중채도, 대중적인 옐로 오렌지 계열의 톤 / 따뜻함, 세련됨, 고급스러움, 안정감
- **활용**: 금속적 광택이 느껴지는 황금빛 오렌지 계열. 노랑의 밝음과 오렌지의 따뜻함이 절묘하게 균형을 이루는 색. 깊은 색감으로 인해 자연적이면서도 고급스러운 인상을 줄 수 있어 브랜딩에서 품격을 전달할 때 활용.
- **배색**: `#F5F2E9` `#004E4E` `#7A4419` `#5C5C66` `#5E6B3A` `#1A2633`
- **출처**: [3]

## Natural Yellows

### Mustard Yellow
- **HEX**: #FFCE1B
- **CMYK**: C 5%, M 20%, Y 88%, K 0%
- **톤/무드**: 중명도, 중채도, 따뜻한 옐로 브라운 계열의 톤 / 빈티지, 따뜻함, 편안함, 내추럴 클래식
- **활용**: 노랑에 브라운이 살짝 섞인 따뜻한 톤. 밝은 옐로의 경쾌함과는 다르게 묵직하고 클래식한 인상을 줌. 내추럴 우드나 올리브 그린과 조합이 좋으며 차분하고 성숙한 분위기 연출. 레트로와 현대적 세련미 공존.
- **배색**: `#F6F4E6` `#1A2A40` `#8B5A2B` `#6B705C` `#3F3F3F` `#C46C45`
- **출처**: [3]

### Wheat
- **HEX**: #F5DEB3
- **CMYK**: C 6%, M 13%, Y 33%, K 0%
- **톤/무드**: 중명도, 저채도, 베이지 옐로 계열의 따뜻한 톤 / 따뜻함, 자연스러움, 부드러움, 안정감
- **활용**: 밀의 색감에서 유래된 컬러로 햇살에 말린 볏짚처럼 은은하고 따뜻한 기운을 지님. 옐로의 생동감보다는 베이지의 안정감이 상대적으로 우세하며 자연스러운 질감 표현에 강점을 가짐. 그래픽, 패션 등에서 고급스러운 톤을 만들 때 사용.
- **배색**: `#7A8450` `#8B5A2B` `#D7AFAF` `#AFC8D9` `#FAF8F2` `#4C4C4C`
- **출처**: [3]

### Flax
- **HEX**: #EEDC82
- **CMYK**: C 12%, M 11%, Y 58%, K 0%
- **톤/무드**: 중명도, 저채도, 따뜻한 베이지 옐로 계열 / 절제, 온기, 내추럴, 따뜻함, 클래식
- **활용**: 아마 섬유의 자연색에서 유래된 컬러로 미세한 황금빛이 감도는 베이지 계열의 내추럴 톤. 광택 없는 건조한 질감 덕분에 고급스러움과 실용성이 동시에 느껴짐. 안정적이고 절제된 느낌을 주며 클래식한 무드 연출에 좋음.
- **배색**: `#B6B1A9` `#7B805A` `#9A6B43` `#A7C7E7` `#C46C45` `#3F3F3F`
- **출처**: [3]

## Deep Yellows

### Ochre Yellow
- **HEX**: #CB9D06
- **CMYK**: C 21%, M 36%, Y 100%, K 6%
- **톤/무드**: 중명도, 중채도, 골든 옐로 + 흙기 섞인 옐로 브라운 계열 / 따뜻함, 견고함, 전통미, 안정감, 고전적 깊이
- **활용**: 흙과 광물에서 추출된 황토 안료색. 자연과 전통을 상징하는 고전적 계열. 순수한 옐로보다 더 깊고 성숙하며 햇빛에 바랜 금빛과 토양의 무게감을 동시에 품고 있음. 빈티지한 웜톤의 핵심.
- **배색**: `#F2E8C6` `#6C7150` `#C2704B` `#27334A` `#9A8F7A` `#4B3D2A`
- **출처**: [3]

### Bronze Gold
- **HEX**: #A97132
- **CMYK**: C 26%, M 54%, Y 86%, K 18%
- **톤/무드**: 중저명도, 중채도, 딥한 브라운 옐로 톤 / 중후함, 고급스러움, 클래식함
- **활용**: 금속의 브론즈 광택과 황금빛이 결합된 색으로 한층 묵직하고 깊이감이 느껴짐. 인테리어 분야에서 빈티지한 금속 질감과 결합되어 클래식한 고급 인상을 주며 전통성과 품격을 표현하는 데 적합함.
- **배색**: `#4A4A4A` `#F4F0E6` `#2C4F3B` `#1C2E4A` `#B85C38` `#D8C3A5`
- **출처**: [3]

## Pastel Yellows

### Naples Yellow
- **HEX**: #FADA5E
- **CMYK**: C 7%, M 13%, Y 71%, K 0%
- **톤/무드**: 고명도, 저채도, 크리미한 라이트 옐로 톤 / 부드러움, 따뜻함, 온화함, 예술적 감성
- **활용**: 르네상스 시대 회화에서 자주 사용된 전통 안료 컬러로 백색과 황색이 섞인 따뜻한 파스텔 톤. 회화나 인테리어에서는 빛을 머금은 듯한 채광감을 표현함. 미니멀하고 감성적인 온 톤 배색에 자주 활용됨.
- **배색**: `#B9B4A6` `#C1C381` `#A7B7C7` `#C97E63` `#F8F5E9` `#2B2B2B`
- **출처**: [3]

### Cornsilk
- **HEX**: #FFF8DC
- **CMYK**: C 2%, M 2%, Y 16%, K 0%
- **톤/무드**: 고명도, 저채도, 크리미한 옐로 베이스 계열의 톤 / 따뜻함, 부드러움, 내추럴함, 포근함
- **활용**: 옥수수 껍질의 섬세한 황빛에서 유래된 색으로 화이트에 가까운 고명도 옐로. 인테리어 및 패션에서는 따뜻한 감성의 베이지 톤으로 많이 활용됨. 높은 대비감의 사용 대신 따뜻한 여백이나 자연스러운 질감 표현에 이상적임.
- **배색**: `#B89C7D` `#B6C7D6` `#BEE9AE` `#D9B8A8` `#7B8B55` `#D49B7A`
- **출처**: [3]

### Buttercream
- **HEX**: #F3E5AB
- **CMYK**: C 8%, M 8%, Y 40%, K 0%
- **톤/무드**: 고명도, 저채도, 크리미한 웜 옐로 톤 / 부드러움, 따뜻함, 포근함, 달콤함
- **활용**: 버터를 머랭처럼 부드럽게 푼 듯한 따뜻한 옐로 베이스 계열. 화이트보다 포근하고 베이지보다 크리미한 중간 지점을 형성함. 그래픽 분야에서 소프트 미니멀리즘의 대표 색으로 사용됨.
- **배색**: `#C4B8A2` `#D5A48E` `#B9A873` `#A7BBCF` `#D39C7D` `#3D3D3D`
- **출처**: [3, 4]

### Blanched Almond
- **HEX**: #FFEBCD
- **CMYK**: C 0%, M 8%, Y 20%, K 0%
- **톤/무드**: 고명도, 저채도, 크리미한 아이보리-크림 톤 / 포근함, 자연스러움, 부드러움, 크래프트
- **활용**: CSS 표준 색상 "Blanched Almond" 에 해당하는 화이트 근접 크림 계열. Cornsilk 보다 옐로기가 적고 Wheat 보다 명도가 높아 화이트에 가장 가까운 웜 surface tone. D2C craft commerce cart drawer · empty state · promo banner · bottom sheet handle 등 surface_tint 로 사용 시 피로감 없이 따뜻함 전달. Rose Quartz + Dark Salmon 팔레트와 자연스러운 warm pastel 삼각 구성을 이룸.
- **배색**: `#F7CAC9` `#E9967A` `#F5F5F5` `#3F3F3F` `#D7C4A3` `#FAF8F2`
- **Semantic ID**: `color-keyword-local-blanched-almond`
- **Spectrum**: `yellow`
- **Ontology Family**: `local_extension`
- **Ontology Category**: `Pastel Yellows`
- **Source Type**: `markdown-local-extension`
- **출처**: [3] `ref-docs-color-reference-local-extensions`

## Pantone Trend Yellows

### Illuminating
- **HEX**: #F5DF4D
- **CMYK**: C 11%, M 9%, Y 76%, K 0%
- **톤/무드**: 고명도, 중채도, 선명하면서 부드러운 라이트 옐로 톤 / 긍정적, 활기찬, 낙관적, 희망적인, 감각적인
- **활용**: 팬톤이 2021년 올해의 색상으로 선정한 컬러로 희망과 회복력을 상징함. 불확실한 시대 속 빛과 에너지를 상징하는 색으로 주목받음. 차분한 그레이나 크리미 베이지 조합으로 감각적인 느낌 표현.
- **배색**: `#939597` `#C7B199` `#A3C7E5` `#F6F1E7` `#474747` `#F0846A`
- **출처**: [4]

### Honey Gold
- **HEX**: #DDB67D
- **CMYK**: C 16%, M 29%, Y 55%, K 2%
- **톤/무드**: 중명도, 중채도, 따뜻한 골드 계열의 옐로 톤 / 안정감, 품격, 여유, 가을의 온기
- **활용**: 햇빛에 익은 꿀빛 같은 톤으로 노란색과 갈색 사이의 완벽한 균형을 이룸. 단순한 명랑함보다 성숙한 온기를 전달하며 브라운, 베이지, 테라코타 톤과의 조합으로 부드러운 조화를 보임. 그래픽 디자인에서 럭셔리 분위기 시각화.
- **배색**: `#9A7C6A` `#FFF8E7` `#C26842` `#757539` `#3F3F3F` `#7FA8B8`
- **출처**: [4]

### Autumn Blaze
- **HEX**: #D1933F
- **CMYK**: C 16%, M 44%, Y 82%, K 4%
- **톤/무드**: 중명도, 중채도, 브라운 오렌지 골드 계열 / 따뜻함, 온기, 성숙함, 자연스러움, 가을의 깊이
- **활용**: 가을 낙엽이 햇빛에 비친 듯한 황금빛 오렌지로 옐로와 브라운 중간에 위치한 웜톤. 따뜻한 감성과 신뢰감을 전달하는 톤으로 활용. 인테리어에서 자연 친화적이면서 클래식 & 럭셔리 분위기 표현.
- **배색**: `#F4EAD2` `#76723E` `#585C61` `#B78A5C` `#D6A8A0` `#3D5A5C`
- **출처**: [4]

## Standard Greens

### Emerald Green
- **HEX**: #50C878
- **CMYK**: C 66%, M 0%, Y 69%, K 0%
- **톤/무드**: 중명도, 중채도의 대중적인 청록 계열 / 고급스러움, 생명력, 세련된 안정감, 청량한 자연성
- **활용**: 보석 '에메랄드'에서 유래한 클래식 그린 톤. 뛰어난 중명도 녹색 컬러로 신뢰와 활력을 상징하며 자연, 테크놀로지, 모던 디자인에 두루 쓰임. 프리미엄 감성 브랜딩에 자주 등장함.
- **배색**: `#F8F8F4` `#3C3C3C` `#C5A100` `#1A2E45` `#E5B9B5` `#D9C6A5`
- **출처**: [4]

### Kelly Green
- **HEX**: #4CBB17
- **CMYK**: C 68%, M 0%, Y 100%, K 0%
- **톤/무드**: 고명도, 고채도, 전통적인 순녹색 계열 / 활력, 생동감, 긍정성, 에너지, 명료함
- **활용**: 자연의 순수한 녹색을 직접적으로 표현한 표준 톤. 다양한 산업 분야에 쓰이며 신뢰와 역동성을 함께 전달함. 자연친화적 브랜딩이나 젊은 소비자 타깃 브랜드에 적합함.
- **배색**: `#FFFFFF` `#1C2E4A` `#FFD6B0` `#3E3E3E` `#F6D64A` `#C8B49A`
- **출처**: [4]

### Olive Green
- **HEX**: #708238
- **CMYK**: C 58%, M 32%, Y 92%, K 16%
- **톤/무드**: 중명도, 저채도의 그린 & 브라운 중간 톤 / 내추럴, 빈티지, 안정감, 따뜻함, 실용성
- **활용**: 올리브 잎과 열매에서 유래한 색으로 브라운 계열이 섞여 묵직한 온기를 줌. 자연적 안정감과 현실감을 강조하며 우드, 리넨, 스톤 재질과의 조화가 차분함. 환경 및 지속가능성 키워드와 잘 어울림.
- **배색**: `#F6F2E6` `#C66B3D` `#D8C7A0` `#3D3D3D` `#1E2F4D` `#C95C32`
- **출처**: [4]

## Natural Greens

### Moss Green
- **HEX**: #8A9A5B
- **CMYK**: C 50%, M 26%, Y 74%, K 8%
- **톤/무드**: 저명도, 저채도의 그린-브라운 혼합 톤 / 자연적, 차분함, 안정적인, 빈티지
- **활용**: 이끼에서 비롯된 자연계의 그린 톤. 빛이 적은 숲속의 음영을 닮음. 브라운 계열이 섞여 있어 토양, 습기, 이끼의 질감을 연상시키며 생명력보다는 안정과 지속성을 상징. 유기농, 환경보호 이미지에 적합함.
- **배색**: `#B3AFA3` `#C76B50` `#D6CBB2` `#4B3B2F` `#C7C99E` `#F5F3EB`
- **출처**: [4]

### Fern Green
- **HEX**: #4F7942
- **CMYK**: C 70%, M 33%, Y 87%, K 18%
- **톤/무드**: 중명도, 중채도의 내추럴 그린 / 차분함, 안정감, 유연함
- **활용**: 양치식물(Fern)의 잎사귀 색감에서 유래. 모스 그린보다 밝고 투명한 생명감을 지님. 자연형 녹색에 가깝고 브라운기가 적어 청량함이 강함. 지속가능성, 차분함, 조화의 이미지를 브랜딩할 때 사용.
- **배색**: `#E8DDC3` `#C2C9A8` `#C66B3D` `#F5F3EB` `#3B3B3B` `#D6C49B`
- **출처**: [4]

### Hunter Green
- **HEX**: #355E3B
- **CMYK**: C 77%, M 39%, Y 85%, K 34%
- **톤/무드**: 저명도, 중고채도의 다크 그린 계열 / 중후함, 신뢰, 클래식, 깊이감, 균형감
- **활용**: 사냥복에서 유래된 전통색으로 영국 귀족 사냥 문화의 고급스러움과 실용성을 상징. 포레스트 그린보다 약간 더 청색 기운이 섞여 정제된 도시적 느낌과 클래식한 감각을 지님. 가죽, 브론즈, 베이지 톤과 함께 빈티지 무드 연출.
- **배색**: `#EDE7D4` `#C49A3A` `#6B2E2E` `#3A3A3A` `#D4C3A1` `#C4C29A`
- **Semantic ID**: `color-keyword-hunter-green`
- **출처**: [4]

## Deep Greens

### Forest Green
- **HEX**: #27503D
- **CMYK**: C 80%, M 40%, Y 75%, K 45%
- **톤/무드**: 저명도, 고채도의 딥 그린 계열 / 묵직함, 안정감, 신뢰, 자연적 깊이
- **활용**: 밝은 그린이 생동감을 준다면 포레스트 그린은 침착함과 심리적 안정을 전달함. 지속성, 신뢰를 상징하는 색으로 자주 사용되며 다크 브라운, 브래스 톤과 조합해 고급스럽고 절제된 내추럴 무드 연출 가능.
- **배색**: `#F5F5EE` `#7A5137` `#1B2E4A` `#C9A552` `#3C3C3C` `#D6C7A4`
- **출처**: [4]

### Bottle Green
- **HEX**: #006A4E
- **CMYK**: C 87%, M 33%, Y 77%, K 25%
- **톤/무드**: 저명도, 중저채도, 청록기 섞인 다크 그린 / 절제됨, 균형, 신뢰, 빈티지, 고급스러움
- **활용**: 유리병의 짙은 녹색빛에서 유래. 청색이 살짝 섞여 냉정함과 절제된 고급스러움이 묻어남. 인공적인 세련미와 균형감을 강조하며 다크 우드, 브래스, 아이보리 계열과 조합해 클래식한 분위기 연출에 적합.
- **배색**: `#F3EFE7` `#C79E46` `#682A2B` `#D6C7A3` `#5B6166` `#9E6B3E`
- **출처**: [4]

## Pastel Greens

### Mint Green
- **HEX**: #98FF98
- **CMYK**: C 42%, M 0%, Y 56%, K 0%
- **톤/무드**: 고명도, 저채도의 쿨 파스텔 그린 톤 / 청량함, 신선함, 현대적 감성, 부드러움
- **활용**: 박하 잎의 밝고 시원한 색감에서 유래. 순수한 녹색보다 한층 더 가볍고 청량함. 병원, 가공용 인테리어, 가전제품 등에 자주 사용되었으며 현재는 청량한 웰니스 톤의 대표 색상임.
- **배색**: `#FFFFFF` `#F8B7A3` `#D1D5D8` `#E7D8B1` `#204E72` `#F9F4AF`
- **출처**: [4]

### Celadon
- **HEX**: #ACE1AF
- **CMYK**: C 38%, M 0%, Y 41%, K 0%
- **톤/무드**: 중명도, 저채도의 그레이시 그린 계열 / 자연스러움, 절제, 고요, 전통미, 단아함
- **활용**: 동양 도자기의 대표색으로 잿빛을 머금은 옅은 녹청색. 맑은 유약이 식으면서 생기는 은은한 색조로 빛의 각도에 따라 푸른빛, 회녹빛이 다르게 드러남. 현대 디자인에서도 공예적 감성과 자연적 안정감을 표현할 때 사용.
- **배색**: `#F7F3E8` `#D7C9A3` `#B28B67` `#C9CFCB` `#D9A6A1` `#4C5854`
- **출처**: [4]

## Pantone Trend Greens

### Greenery
- **HEX**: #88B04B
- **CMYK**: C 54%, M 16%, Y 85%, K 1%
- **톤/무드**: 중명도, 중채도의 옐로기반 그린 톤 / 회복, 생명력, 청춘, 균형, 리프레시
- **활용**: 2017년 팬톤 올해의 컬러. 전 세계적으로 지속가능성과 자연 회귀의 상징이 됨. 신선한 잎사귀가 막 돋아나는 순간의 연녹색으로 도시화된 삶에 활력을 불어넣음. 옐로 베이스 덕분에 따뜻한 온 톤 배색과 잘 어울림.
- **배색**: `#F7F5E8` `#D8C7A0` `#A77E5A` `#A7C5BD` `#4A4F47` `#F0E46C`
- **출처**: [4, 5]

### Arcadia
- **HEX**: #00A591
- **CMYK**: C 78%, M 13%, Y 52%, K 1%
- **톤/무드**: 중명도, 중채도의 블루 그린 계열 / 세련, 청량, 도시적, 미래지향, 균형
- **활용**: 팬톤 2018 봄 트렌드 팔레트 컬러. 현대적이면서 자연적인 균형을 상징하는 감각적인 블루톤 그린. 기존 그린보다 푸른 기운이 강해 도시적 세련미와 디지털 청량감을 가짐. 에코 모던 키워드 및 럭셔리함 표현에 적합.
- **배색**: `#F5F5F5` `#BFC6C4` `#F88379` `#D5B895` `#1D3A4C` `#C5E5D0`
- **출처**: [5]

### Cascade
- **HEX**: #76C1B1
- **CMYK**: C 57%, M 7%, Y 37%, K 0%
- **톤/무드**: 중명도, 저채도 쿨톤 민트 그린 계열 / 정제된 청량감, 세련미, 안정감, 포근함
- **활용**: Green Ash보다 한층 푸른빛이 강하고 회색 기운이 살짝 감도는 워터리 틸 톤. 자연과 테크놀로지가 교차하는 이미지. 휴식 속의 기술이라는 컨셉으로 패션 및 인테리어 브랜드에서 빈번히 활용됨.
- **배색**: `#F5F5F5` `#B0A89E` `#D6C4A3` `#C8E2E0` `#D19C7C` `#4E4B45`
- **출처**: [5]

## Standard Blues

### Cerulean
- **HEX**: #2A52BE
- **CMYK**: C 89%, M 71%, Y 0%, K 0%
- **톤/무드**: 중명도, 중채도, 스탠다드한 청색 계열 / 안정감, 명료함, 신뢰, 여유, 시각적 청량감
- **활용**: 하늘이 맑게 갠 순간의 짙은 푸른색에서 유래. 자연광 아래에서 탁하지 않고 균형감 있는 톤을 유지함. 그래픽, 패션, 공간 디자인 등에서 '신뢰와 안정'의 상징으로 자주 쓰임. 과도한 감정선을 배제한 객관적 색상.
- **배색**: `#D9D9D9` `#F7F5EB` `#A9BFA1` `#D7C4A3` `#FFFFFF` `#FFB59E`
- **출처**: [5]

### Azure Blue
- **HEX**: #007FFF
- **CMYK**: C 81%, M 51%, Y 0%, K 0%
- **톤/무드**: 고명도, 고채도, 쿨톤의 청량한 블루 / 개방감, 에너지, 명료함, 신선함, 혁신
- **활용**: 지중해의 청명한 하늘에서 유래한 퓨어 블루. 가장 이상적인 하늘색으로 평가됨. 웹/앱 UI 디자인에서 버튼, 하이라이트 등 사용자 주목 포인트 컬러로 쓰이며 열린 사고와 테크놀로지를 상징함.
- **배색**: `#D9CBB3` `#444C57` `#FEE440` `#BCE0EE` `#FFFFFF` `#F45B69`
- **출처**: [5]

## Natural Blues

### Teal Blue
- **HEX**: #01889F
- **CMYK**: C 82%, M 30%, Y 31%, K 7%
- **톤/무드**: 중명도, 중채도, 쿨톤의 감각적인 청록색 계열 / 개방감, 에너지, 명료함, 신선함, 감각적
- **활용**: 바다와 숲의 경계에서 느껴지는 자연의 심도 있는 색감. 블루의 냉정함과 그린의 따뜻함이 교차하며 그래픽 디자인에서 전문적인 인상을 줌. 우드 톤이나 브론즈 계열과 결합해 고급스럽고 감성적인 분위기 완성.
- **배색**: `#F8F5E1` `#D66B4D` `#D8C7A0` `#333333` `#E0B03B` `#D7A7A1`
- **Semantic ID**: `color-keyword-teal-blue`
- **출처**: [5]

### Sky Blue
- **HEX**: #87CEEB
- **CMYK**: C 49%, M 5%, Y 7%, K 0%
- **톤/무드**: 고명도, 중채도의 밝은 쿨톤 / 청량함, 평화, 유연함, 긍정, 맑음
- **활용**: 대기 중 산란광의 자연스러운 푸른빛을 재현한 색. 자연광에서의 개방감을 시각적으로 구현함. UI/UX에서는 피로감 없는 인터페이스 컬러로 활용됨. 화이트, 우드 톤과 함께 사용 시 정서적 안정감을 극대화함.
- **배색**: `#F5F5F5` `#E6DBB8` `#333333` `#D8A7A7` `#B6E3C1` `#CFC7B5`
- **출처**: [5]

### Ocean Blue
- **HEX**: #4F97A3
- **CMYK**: C 70%, M 26%, Y 33%, K 5%
- **톤/무드**: 중명도, 중채도, 매트한 청록색 계열 / 신뢰, 정화, 깊이감, 유연함, 안정감
- **활용**: 빛에 따라 푸른색과 청록빛이 동시에 드러나는 것이 특징. 사용 분야에 따라 스펙트럼이 다를 수 있지만 다양한 산업 분야에 감각적으로 사용 가능. 브랜딩에서 지속가능성 키워드로 자주 쓰임.
- **배색**: `#F7F7F7` `#E77A64` `#D8C7A0` `#60727B` `#9FD6C2` `#203A4A`
- **출처**: [5]

## Deep Blues

### Navy Blue
- **HEX**: #000080
- **CMYK**: C 100%, M 99%, Y 23%, K 8%
- **톤/무드**: 저명도, 중채도, 차가운 온도감이 강한 블루 계열 / 신뢰, 권위, 집중, 전문성, 절제된 우아함
- **활용**: 영국 해군의 제복 색에서 유래. 세계적으로 전통, 질서, 규율을 상징. 지속적 신뢰감과 전문적 안정감을 표현하며 제복, 금융 등 공공 기관의 시각 아이덴티티에 널리 사용됨. 세련된 무드 완성.
- **배색**: `#FFFFFF` `#D6C6A6` `#D4AF37` `#E97E68` `#708090` `#B0C4DE`
- **출처**: [5]

### Prussian Blue
- **HEX**: #003153
- **CMYK**: C 93%, M 68%, Y 42%, K 35%
- **톤/무드**: 저명도, 저채도, 녹색 기가 약하게 섞인 중성 쿨톤 / 고전, 예술, 집중, 권위, 깊이감
- **활용**: 18세기 초 독일에서 합성된 안료로 최초의 합성 블루. 네이비보다 묵직하고 인디고보다 정제된 느낌. 디지털과 인쇄 양쪽 모두에서 깊이감과 고급스러움을 표현할 때 사용됨.
- **배색**: `#F5F3E7` `#C69C59` `#B8CBD0` `#B35A28` `#8A8E80` `#D4A6A6`
- **출처**: [5]

## Pastel Blues

### Ice Blue
- **HEX**: #D6EAF8
- **CMYK**: C 18%, M 3%, Y 2%, K 0%
- **톤/무드**: 고명도, 저채도, 밝고 청량한 블루 계열 / 정제됨, 청결함, 섬세함, 평온, 투명
- **활용**: 차가운 공기와 투명한 얼음빛을 연상시키는 밝은 블루 톤. 화이트와 블루의 경계선에서 공간의 깊이와 여백감을 강조함. 청결한 이미지를 전달할 때 유용하며 감정 밀도가 낮아 객관적이고 중립적인 활용도가 높음.
- **배색**: `#FFFFFF` `#3E3E3E` `#D9C8A9` `#2E4E68` `#F6D5D6` `#C0C0C0`
- **출처**: [5]

### Powder Blue
- **HEX**: #B0E0E6
- **CMYK**: C 34%, M 1%, Y 12%, K 0%
- **톤/무드**: 중명도, 저채도, 뉴트럴 톤 / 부드러움, 균형감, 온화함, 정제된 따뜻함
- **활용**: 이름 그대로 파우더처럼 부드럽고 은은한 하늘색. 1950-60년대 파스텔 컬러 트렌드의 대표색으로 레트로 감성과 모던 감성의 경계를 가짐. 화이트 & 그레이와 결합 시 청량하면서 부드러운 인상 유지 가능.
- **배색**: `#F7F3E9` `#C4C4C4` `#D7C4A3` `#2C3E50` `#CBB9E4` `#F2C1C2`
- **출처**: [5]

### Misty Blue
- **HEX**: #B5C7EB
- **CMYK**: C 32%, M 17%, Y 0%, K 0%
- **톤/무드**: 중명도, 저채도, 보라색이 섞인 뉴트럴 블루 톤 / 차분함, 사색적, 몽환적, 잔잔함, 감정의 여운
- **활용**: 이름처럼 안개가 낀 듯한 부드러운 푸른빛. 블루의 신뢰감과 바이올렛의 감성적 온기가 동시에 느껴짐. 빛에 따라 다르게 보이는 색으로 감정 층위가 깊은 디자인에 쓰이며 문학적, 예술적 무드에 어울림.
- **배색**: `#F9F9F6` `#C4C3D0` `#D4A5A5` `#6A7BA2` `#D8C6A2` `#2C3456`
- **출처**: [5]

## Pantone Trend Blues

### Classic Blue
- **HEX**: #0F4C81
- **CMYK**: C 97%, M 72%, Y 24%, K 9%
- **톤/무드**: 중명도, 중채도, 클래식한 딥 블루 톤 / 신뢰, 평온함, 지성, 안정감
- **활용**: 팬톤 2020년 올해의 컬러. 불안정한 시대 속 '안정과 확신'을 상징함. 시대의 불확실함 속에서도 변치 않는 신뢰감을 전달하며 브랜드 아이덴티티에서는 전문성, 지속가능성을 형성함. 패션, 인테리어에서 세련된 미니멀리즘으로 사용.
- **배색**: `#FFFFFF` `#BEB7A4` `#D7C4A3` `#F88379` `#E1AD01` `#B87333`
- **출처**: [5]

### Super Sonic
- **HEX**: #0071A8
- **CMYK**: C 88%, M 50%, Y 15%, K 3%
- **톤/무드**: 고명도, 중고채도, 브라이트 블루(Bright Blue) 톤 / 혁신적, 미래지향적, 역동적, 청량감, 에너지
- **활용**: 기술, 속도, 청량함을 상징하는 하이테크 블루. 메탈릭 계열이나 브라이트 톤과 함께 쓰여 세련미와 미래적 감각 강조. IT 및 스포츠 브랜드에서 퍼포먼스 이미지 시각화에 자주 활용됨. UI/UX에서 하이라이트 포인트로 사용.
- **배색**: `#FFFFFF` `#D3D3D3` `#FFD43B` `#2B2B2B` `#FF6B6B` `#C0C0C0`
- **출처**: [5]

### Blue Atoll
- **HEX**: #00B1D2
- **CMYK**: C 74%, M 12%, Y 17%, K 0%
- **톤/무드**: 중명도, 고채도, 청량한 트로피컬 블루 톤 / 생기, 젊음, 휴양, 청량함, 모던함
- **활용**: 바하마 해변의 수면색을 연상시키는 컬러. 맑고 투명한 느낌 속에 약간의 아쿠아톤 그린이 섞여 있음. 스탠다드 블루보다 활기 있고 부드러워 접목성이 좋음. 리조트, 여름 패션, 아웃도어 브랜딩의 대표색.
- **배색**: `#F9F5E8` `#4A4A4A` `#FFE156` `#FF6F61` `#1E3A5F` `#A8E6CF`
- **출처**: [6]

## Standard Violets

### Cobalt Violet
- **HEX**: #804AA8
- **CMYK**: C 64%, M 81%, Y 0%, K 0%
- **톤/무드**: 중명도, 중채도의 쿨 퍼플 톤 / 안정감, 차분함, 예술적, 신비감
- **활용**: 회화나 인상주의 회화에서 자주 사용된 대표적 예술색. 차가운 보랏빛이지만 청색 비율이 높아 깊이감이 있음. 과도하게 화려하지 않으며 품위와 지성을 전달하는 색감.
- **배색**: `#BEB5A7` `#E6BE8A` `#3A4374` `#D8A7B1` `#F7F3E9` `#9C8E52`
- **출처**: [6]

### Royal Purple
- **HEX**: #6C3BAA
- **CMYK**: C 74%, M 86%, Y 0%, K 0%
- **톤/무드**: 중명도, 고채도의 따뜻한 웜 퍼플 톤 / 장엄함, 품격, 권위, 카리스마
- **활용**: 역사적으로 왕실과 귀족 계급의 상징으로 사용된 컬러. 자주색 안료의 희소성에서 비롯된 고급감과 상징성이 특징. 현대에는 리더십과 영향력, 세련됨 등을 표현하는 대표 색상.
- **배색**: `#F7E7CE` `#50C878` `#C0C0C0` `#FFFDD0` `#1A1A40` `#65000B`
- **출처**: [6]

## Natural Violets

### Lavender Violet
- **HEX**: #967BB6
- **CMYK**: C 50%, M 57%, Y 4%, K 0%
- **톤/무드**: 고명도, 중저채도, 베이직 퍼플 계열 / 부드러움, 평온함, 세련, 낭만, 안정감
- **활용**: 보라색 중에서 가장 부드러운 계열. 흰색이 많이 섞인 베이직한 퍼플의 대표 색상. 라벤더 꽃에서 유래해 심리적으로 진정, 휴식, 정화를 연상시킴. 다양한 산업 분야 및 브랜드 아이덴티티에서 차분한 감성 활용.
- **배색**: `#D9D9D9` `#FFF9E9` `#A8B79D` `#E6A6B0` `#444444` `#A7C7E7`
- **출처**: [6]

### Lilac Violet
- **HEX**: #C8A2C8
- **CMYK**: C 25%, M 41%, Y 5%, K 0%
- **톤/무드**: 중명도, 저채도, 그레이(Gray) 기반 웜 퍼플 톤 / 낭만적, 청초함, 감정적 여유, 몽환적
- **활용**: 라벤더보다 조금 더 따뜻하고 부드러운 회색기 섞인 퍼플 톤. 라일락 꽃잎 색을 바탕으로 사랑과 순수한 감정의 상징으로 쓰임. 빈티지 감성, 로맨틱 무드, 봄 시즌 테마에서 자주 사용됨.
- **배색**: `#FDFBF7` `#B5C7EB` `#DCC7AA` `#A0B7A3` `#BEB8AF` `#5B3256`
- **출처**: [6]

### Iris Violet
- **HEX**: #5A4FCF
- **CMYK**: C 80%, M 74%, Y 0%, K 0%
- **톤/무드**: 중명도, 고채도, 쿨 퍼플 톤 / 신선함, 예술적, 정제된 생동감, 상징적 존재감
- **활용**: 아이리스(붓꽃) 꽃잎에서 유래된 중채도의 블루빛 퍼플 계열. 푸른 계열이 강해 라벤더보다 명료하고 시각적으로 선명함. 예술, 철학적 상징성이 높은 컬러로 지적이고 이상적인 이미지 표현 시 사용.
- **배색**: `#D8D8D8` `#CAB7E1` `#FFF5E5` `#333333` `#5C8A6B` `#E8C2AF`
- **출처**: [6]

## Deep Violets

### Aubergine
- **HEX**: #614051
- **CMYK**: C 56%, M 73%, Y 43%, K 38%
- **톤/무드**: 저명도, 중채도, 뉴트럴 베이스의 퍼플 톤 / 고혹적, 성숙함, 미스터리, 예술적, 긴장감
- **활용**: 가지(Eggplant) 껍질에서 유래된 컬러로 브라운 계열이 섞인 딥 퍼플 톤. 일반 퍼플보다 붉은 기가 섞여 따뜻한 깊이를 지니며 빛에 따라 보라, 브라운, 버건디로 변화함. 럭셔리 및 하이엔드 브랜드 포인트로 활용.
- **배색**: `#B6A7A2` `#7A8450` `#E9CBA7` `#D8A7B1` `#C4A74B` `#F39D1E`
- **출처**: [6]

### Byzantium
- **HEX**: #702963
- **CMYK**: C 62%, M 99%, Y 26%, K 18%
- **톤/무드**: 저명도, 중고채도의 웜 퍼플 톤 / 고전적, 신비로움, 황홀함, 예술적 품격
- **활용**: 비잔티움 제국의 미술, 건축에서 유래된 컬러. 보라와 자주 사이의 중간대, 제국적 품위를 상징하는 보라빛 레드 톤. 왕권, 예술, 영성을 표현하기 위해 사용되던 역사적 배경. 라벤더보다 깊고 고혹적임.
- **배색**: `#C6A664` `#F9E7C4` `#2F2F2F` `#6A75A8` `#8D8752` `#D9A8A3`
- **출처**: [6]

### Midnight Violet
- **HEX**: #2E1A47
- **CMYK**: C 84%, M 90%, Y 32%, K 32%
- **톤/무드**: 저명도, 저채도, 쿨 베이스 딥 퍼플 톤 / 고요함, 신비, 절제된 감정, 내면적 깊이
- **활용**: 자정의 어둠 속 희미하게 남은 보랏빛을 연상시키는 컬러. 블루와 퍼플의 경계선에 존재하며 정온함과 사색을 떠올리게 함. 우아하며 차분한 무드. 디지털 환경에서는 다크 모드 계열 배경 컬러로 사용됨.
- **배색**: `#C5A8E0` `#BFD4E9` `#D1AE4F` `#67623C` `#C2C2C2` `#D8A5A5`
- **출처**: [6]

## Pastel Violets

### Periwinkle
- **HEX**: #8E9AF1
- **CMYK**: C 51%, M 38%, Y 0%, K 0%
- **톤/무드**: 중명도, 저채도, 푸른빛이 감도는 웜 퍼플 톤 / 부드러움, 몽환, 순수함, 세련된 차분함
- **활용**: 블루와 라벤더의 경계에 있는 컬러로 보라의 감성적 깊이와 블루의 차분함을 동시에 품음. 페리윙클 플라워에서 유래. 자연광 아래서는 라일락빛이 감돌고 실내광에서는 블루로 보이는 특성이 있음. 디지털 파스텔 퍼플로 분류됨.
- **배색**: `#E1E1E1` `#D7C5EA` `#AFC8E4` `#EFD8C5` `#3C3C44` `#FFF5D9`
- **출처**: [6]

### Mauve
- **HEX**: #E0B0FF
- **CMYK**: C 21%, M 34%, Y 0%, K 0%
- **톤/무드**: 중명도, 저채도, 웜과 쿨 중간 베이스 퍼플 톤 / 낭만적, 세련됨, 회상적, 빈티지 무드
- **활용**: 19세기 최초의 합성 염료로 탄생한 컬러. 산업혁명 시대의 '인공색'이자 동시에 패션 컬러 혁명의 시작점. 보라빛이 감도는 그레이시 핑크로 라벤더보다 부드럽고 로즈보다 쿨한 미묘한 톤을 지님.
- **배색**: `#F4E3C1` `#D2A4A8` `#767B91` `#8B7C65` `#CFCFCF`
- **출처**: [6]

### Lavender Mist
- **HEX**: #E6E6FA
- **CMYK**: C 11%, M 9%, Y 0%, K 0%
- **톤/무드**: 고명도, 저채도, 쿨톤의 파스텔 계열 퍼플 / 청명함, 정화, 몽환, 세련된 차분함
- **활용**: 가장 순화된 라벤더 계열로 보라의 감성과 흰빛의 청량함이 혼합된 정서 안정형 컬러. 잭슨 폴록의 회화에서 유래. 웰니스, 뷰티 브랜드 등에서 자주 쓰이며 화이트, 실버, 소프트 블루와 자연스러운 톤 연계 가능.
- **배색**: `#F7F6F0` `#C0C0C0` `#C7DAF0` `#F5D7DC` `#444444` `#D7CBEF`
- **출처**: [6]

## Pantone Trend Violets

### Ultra Violet
- **HEX**: #5F4B8B
- **CMYK**: C 76%, M 79%, Y 15%, K 3%
- **톤/무드**: 중명도, 중고채도, 파란빛이 섞인 깊고 복합적인 퍼플 / 창의적, 신비감, 미래적, 실험적
- **활용**: 2018년 팬톤 올해의 컬러. 영감과 비전을 상징하는 퍼플 스펙트럼의 중심축. 블루와 레드의 중간에 있는 컬러이기 때문에 이성(blue)과 감성(red)의 조화를 의미. 사고의 확장과 감정의 심화 부분을 동시에 담음.
- **배색**: `#C5C5C5` `#F7CAC9` `#1C1F4A` `#BCA7E0` `#FF6F61` `#F5F5F5`
- **출처**: [6]

### Very Peri
- **HEX**: #6667AB
- **CMYK**: C 71%, M 64%, Y 6%, K 0%
- **톤/무드**: 중명도, 중채도, 역동적이고 따뜻한 페리윙클 퍼플 톤 / 창조, 낙관적, 변화, 실험적
- **활용**: 팬톤이 2022년 올해의 컬러로 직접 개발한 최초의 색. 기존 팬톤 컬러 중 없던 새로운 보라 계열로 디지털 전환 시대의 창의성과 자신감을 상징. 브랜드 리뉴얼, UI, 패션 컬렉션 등에서 새로운 시작을 암시함.
- **배색**: `#F9F9F9` `#F88379` `#4A90E2` `#B8A4D0` `#444444` `#C7E7D5`
- **출처**: [6]

### Grape Compote
- **HEX**: #6B5876
- **CMYK**: C 63%, M 66%, Y 32%, K 16%
- **톤/무드**: 저명도, 중저채도, 뉴트럴 베이스의 차분한 퍼플 톤 / 차분, 세련, 내면적, 성숙함
- **활용**: 팬톤 2020 F/W 트렌드 컬러. 화려함 대신 내면의 평온과 성숙한 감정을 표현. 짙은 자두빛과 브라운 잔영이 섞인 색조로 지적이면서 안정적인 분위기 연출에 탁월. 패션, 인테리어, 코스메틱에서 깊이 있는 미니멀함 표현.
- **배색**: `#E5D9CC` `#D8A7B1` `#3E3E3E` `#A2A08F` `#B3ABB7` `#F3F1EE`
- **출처**: [6]

<!-- semantic-os-color-catalog:begin sha256=4041facc76b5557979f38a27688d349378caece64d143eb409fc78890a9903b9 -->
<details>
<summary>Pantone Color of the Year identity index — 29 nodes</summary>

이 표는 `sync-semantic-colors`가 내장 그래프에서 생성합니다. HEX 중복 여부와 무관하게 각 Semantic ID를 하나의 독립된 색상 정체성으로 다룹니다.

| Year | Color | HEX | Spectrum | Pantone | Semantic ID | Source |
| ---: | --- | --- | --- | --- | --- | --- |
| 2000 | Cerulean (Pantone COY 2000) | `#9BB7D6` | blue | 15-4020 | `color-keyword-pantone-coy-2000-cerulean` | `ref-pantone-coy-announcements` |
| 2001 | Fuchsia Rose (Pantone COY 2001) | `#C94476` | red | 17-2031 | `color-keyword-pantone-coy-2001-fuchsia-rose` | `ref-pantone-coy-announcements` |
| 2002 | True Red (Pantone COY 2002) | `#C02034` | red | 19-1664 | `color-keyword-pantone-coy-2002-true-red` | `ref-pantone-coy-announcements` |
| 2003 | Aqua Sky (Pantone COY 2003) | `#7AC5C5` | blue | 14-4811 | `color-keyword-pantone-coy-2003-aqua-sky` | `ref-pantone-coy-announcements` |
| 2004 | Tigerlily (Pantone COY 2004) | `#E4583E` | orange | 17-1456 | `color-keyword-pantone-coy-2004-tigerlily` | `ref-pantone-coy-announcements` |
| 2005 | Blue Turquoise (Pantone COY 2005) | `#4FB0AE` | blue | 15-5217 | `color-keyword-pantone-coy-2005-blue-turquoise` | `ref-pantone-coy-announcements` |
| 2006 | Sand Dollar (Pantone COY 2006) | `#DECDBF` | yellow | 13-1106 | `color-keyword-pantone-coy-2006-sand-dollar` | `ref-pantone-coy-announcements` |
| 2007 | Chili Pepper (Pantone COY 2007) | `#9C1B31` | red | 19-1557 | `color-keyword-pantone-coy-2007-chili-pepper` | `ref-pantone-coy-announcements` |
| 2008 | Blue Iris (Pantone COY 2008) | `#595CA1` | violet | 18-3943 | `color-keyword-pantone-coy-2008-blue-iris` | `ref-pantone-coy-announcements` |
| 2009 | Mimosa (Pantone COY 2009) | `#F0BF59` | yellow | 14-0848 | `color-keyword-pantone-coy-2009-mimosa` | `ref-pantone-coy-announcements` |
| 2010 | Turquoise (Pantone COY 2010) | `#41B6AB` | blue | 15-5519 | `color-keyword-pantone-coy-2010-turquoise` | `ref-pantone-coy-announcements` |
| 2011 | Honeysuckle (Pantone COY 2011) | `#DA4F70` | red | 18-2120 | `color-keyword-pantone-coy-2011-honeysuckle` | `ref-pantone-coy-announcements` |
| 2012 | Tangerine Tango (Pantone COY 2012) | `#F05442` | orange | 17-1463 | `color-keyword-pantone-coy-2012-tangerine-tango` | `ref-pantone-coy-announcements` |
| 2013 | Emerald (Pantone COY 2013) | `#009473` | green | 17-5641 | `color-keyword-pantone-coy-2013-emerald` | `ref-pantone-coy-announcements` |
| 2014 | Radiant Orchid (Pantone COY 2014) | `#B565A7` | violet | 18-3224 | `color-keyword-pantone-coy-2014-radiant-orchid` | `ref-pantone-coy-announcements` |
| 2015 | Marsala (Pantone COY 2015) | `#955251` | red | 18-1438 | `color-keyword-pantone-coy-2015-marsala` | `ref-pantone-coy-announcements` |
| 2016 | Rose Quartz (Pantone COY 2016) | `#F7CAC9` | red | 13-1520 | `color-keyword-pantone-coy-2016-rose-quartz` | `ref-pantone-coy-announcements` |
| 2016 | Serenity (Pantone COY 2016) | `#92A8D1` | blue | 15-3919 | `color-keyword-pantone-coy-2016-serenity` | `ref-pantone-coy-announcements` |
| 2017 | Greenery (Pantone COY 2017) | `#88B04B` | green | 15-0343 | `color-keyword-pantone-coy-2017-greenery` | `ref-pantone-coy-announcements` |
| 2018 | Ultra Violet (Pantone COY 2018) | `#5F4B8B` | violet | 18-3838 | `color-keyword-pantone-coy-2018-ultra-violet` | `ref-pantone-coy-announcements` |
| 2019 | Living Coral (Pantone COY 2019) | `#FF6F61` | orange | 16-1546 | `color-keyword-pantone-coy-2019-living-coral` | `ref-pantone-coy-announcements` |
| 2020 | Classic Blue (Pantone COY 2020) | `#0F4C81` | blue | 19-4052 | `color-keyword-pantone-coy-2020-classic-blue` | `ref-pantone-coy-announcements` |
| 2021 | Illuminating (Pantone COY 2021) | `#F5DF4D` | yellow | 13-0647 | `color-keyword-pantone-coy-2021-illuminating` | `ref-pantone-coy-announcements` |
| 2021 | Ultimate Gray (Pantone COY 2021) | `#939597` | neutral | 17-5104 | `color-keyword-pantone-coy-2021-ultimate-gray` | `ref-pantone-coy-announcements` |
| 2022 | Very Peri (Pantone COY 2022) | `#6667AB` | violet | 17-3938 | `color-keyword-pantone-coy-2022-very-peri` | `ref-pantone-coy-announcements` |
| 2023 | Viva Magenta (Pantone COY 2023) | `#BB2649` | red | 18-1750 | `color-keyword-pantone-coy-2023-viva-magenta` | `ref-pantone-coy-announcements` |
| 2024 | Peach Fuzz (Pantone COY 2024) | `#FFBE98` | orange | 13-1023 | `color-keyword-pantone-coy-2024-peach-fuzz` | `ref-pantone-coy-announcements` |
| 2025 | Mocha Mousse (Pantone COY 2025) | `#A47864` | orange | 17-1230 | `color-keyword-pantone-coy-2025-mocha-mousse` | `ref-pantone-coy-announcements` |
| 2026 | Cloud Dancer (Pantone COY 2026) | `#F0EEE9` | neutral | 11-4201 | `color-keyword-pantone-coy-2026-cloud-dancer` | `ref-pantone-coy-announcements` |

</details>
<!-- semantic-os-color-catalog:end -->

<!-- semantic-os-color-ontology:begin sha256=4041facc76b5557979f38a27688d349378caece64d143eb409fc78890a9903b9 -->
<details>
<summary>Semantic OS 컬러 온톨로지 스냅샷 — 380 nodes, 1266 edges, 308 keywords (131 with HEX)</summary>

이 블록은 `sync-semantic-colors`가 생성합니다. 직접 수정하지 마세요.
원본: `semantic-os/domains/color/ontology/build/graph.json` · built_at: `2026-08-12T14:03:22.155766+00:00` · sha256: `4041facc76b5557979f38a27688d349378caece64d143eb409fc78890a9903b9`

```semantic-color-ontology+json
{
 "edge_count": 1266,
 "edges": [
  {
   "from": {
    "id": "topic-color-pantone-trend",
    "space": "concept"
   },
   "relation": "cites",
   "to": {
    "id": "ref-pantone-coy-announcements",
    "space": "resource"
   }
  },
  {
   "from": {
    "id": "system-pantone-matching-system",
    "space": "concept"
   },
   "relation": "cites",
   "to": {
    "id": "ref-pantone-coy-announcements",
    "space": "resource"
   }
  },
  {
   "from": {
    "id": "system-pantone-matching-system",
    "space": "concept"
   },
   "relation": "belongs_to_topic",
   "to": {
    "id": "topic-color-basic-systems",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "guideline-pantone-library-no-wholesale-import",
    "space": "concept"
   },
   "relation": "belongs_to_topic",
   "to": {
    "id": "topic-color-pantone-trend",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "guideline-pantone-library-no-wholesale-import",
    "space": "concept"
   },
   "relation": "cites",
   "to": {
    "id": "ref-pantone-coy-announcements",
    "space": "resource"
   }
  },
  {
   "from": {
    "id": "guideline-pantone-hex-screen-approximation",
    "space": "concept"
   },
   "relation": "belongs_to_topic",
   "to": {
    "id": "topic-color-pantone-trend",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "guideline-pantone-hex-screen-approximation",
    "space": "concept"
   },
   "relation": "cites",
   "to": {
    "id": "ref-pantone-coy-announcements",
    "space": "resource"
   }
  },
  {
   "from": {
    "id": "guideline-pantone-hex-screen-approximation",
    "space": "concept"
   },
   "relation": "supports",
   "to": {
    "id": "guideline-color-values-are-reference-not-absolute",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "heuristic-trend-color-reads-with-era-context",
    "space": "concept"
   },
   "relation": "belongs_to_topic",
   "to": {
    "id": "topic-color-application",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "heuristic-trend-color-reads-with-era-context",
    "space": "concept"
   },
   "relation": "cites",
   "to": {
    "id": "ref-reference-x-vol1-color",
    "space": "resource"
   }
  },
  {
   "from": {
    "id": "pattern-coy-timeline-as-era-anchor",
    "space": "concept"
   },
   "relation": "belongs_to_topic",
   "to": {
    "id": "topic-color-pantone-trend",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "pattern-coy-timeline-as-era-anchor",
    "space": "concept"
   },
   "relation": "cites",
   "to": {
    "id": "ref-pantone-coy-announcements",
    "space": "resource"
   }
  },
  {
   "from": {
    "id": "pattern-coy-timeline-as-era-anchor",
    "space": "concept"
   },
   "relation": "requires",
   "to": {
    "id": "guideline-pantone-library-no-wholesale-import",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "pattern-coy-timeline-as-era-anchor",
    "space": "concept"
   },
   "relation": "requires",
   "to": {
    "id": "guideline-pantone-hex-screen-approximation",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "color-keyword-pantone-coy-2000-cerulean",
    "space": "concept"
   },
   "relation": "belongs_to_topic",
   "to": {
    "id": "topic-color-pantone-trend",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "color-keyword-pantone-coy-2000-cerulean",
    "space": "concept"
   },
   "relation": "cites",
   "to": {
    "id": "ref-pantone-coy-announcements",
    "space": "resource"
   }
  },
  {
   "from": {
    "id": "color-keyword-pantone-coy-2000-cerulean",
    "space": "concept"
   },
   "relation": "belongs_to_topic",
   "to": {
    "id": "topic-color-blue-spectrum",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "color-keyword-pantone-coy-2000-cerulean",
    "space": "concept"
   },
   "relation": "requires",
   "to": {
    "id": "guideline-pantone-hex-screen-approximation",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "color-keyword-pantone-coy-2001-fuchsia-rose",
    "space": "concept"
   },
   "relation": "belongs_to_topic",
   "to": {
    "id": "topic-color-pantone-trend",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "color-keyword-pantone-coy-2001-fuchsia-rose",
    "space": "concept"
   },
   "relation": "cites",
   "to": {
    "id": "ref-pantone-coy-announcements",
    "space": "resource"
   }
  },
  {
   "from": {
    "id": "color-keyword-pantone-coy-2001-fuchsia-rose",
    "space": "concept"
   },
   "relation": "belongs_to_topic",
   "to": {
    "id": "topic-color-red-spectrum",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "color-keyword-pantone-coy-2001-fuchsia-rose",
    "space": "concept"
   },
   "relation": "requires",
   "to": {
    "id": "guideline-pantone-hex-screen-approximation",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "color-keyword-pantone-coy-2002-true-red",
    "space": "concept"
   },
   "relation": "belongs_to_topic",
   "to": {
    "id": "topic-color-pantone-trend",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "color-keyword-pantone-coy-2002-true-red",
    "space": "concept"
   },
   "relation": "cites",
   "to": {
    "id": "ref-pantone-coy-announcements",
    "space": "resource"
   }
  },
  {
   "from": {
    "id": "color-keyword-pantone-coy-2002-true-red",
    "space": "concept"
   },
   "relation": "belongs_to_topic",
   "to": {
    "id": "topic-color-red-spectrum",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "color-keyword-pantone-coy-2002-true-red",
    "space": "concept"
   },
   "relation": "requires",
   "to": {
    "id": "guideline-pantone-hex-screen-approximation",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "color-keyword-pantone-coy-2003-aqua-sky",
    "space": "concept"
   },
   "relation": "belongs_to_topic",
   "to": {
    "id": "topic-color-pantone-trend",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "color-keyword-pantone-coy-2003-aqua-sky",
    "space": "concept"
   },
   "relation": "cites",
   "to": {
    "id": "ref-pantone-coy-announcements",
    "space": "resource"
   }
  },
  {
   "from": {
    "id": "color-keyword-pantone-coy-2003-aqua-sky",
    "space": "concept"
   },
   "relation": "belongs_to_topic",
   "to": {
    "id": "topic-color-blue-spectrum",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "color-keyword-pantone-coy-2003-aqua-sky",
    "space": "concept"
   },
   "relation": "requires",
   "to": {
    "id": "guideline-pantone-hex-screen-approximation",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "color-keyword-pantone-coy-2004-tigerlily",
    "space": "concept"
   },
   "relation": "belongs_to_topic",
   "to": {
    "id": "topic-color-pantone-trend",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "color-keyword-pantone-coy-2004-tigerlily",
    "space": "concept"
   },
   "relation": "cites",
   "to": {
    "id": "ref-pantone-coy-announcements",
    "space": "resource"
   }
  },
  {
   "from": {
    "id": "color-keyword-pantone-coy-2004-tigerlily",
    "space": "concept"
   },
   "relation": "belongs_to_topic",
   "to": {
    "id": "topic-color-orange-spectrum",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "color-keyword-pantone-coy-2004-tigerlily",
    "space": "concept"
   },
   "relation": "requires",
   "to": {
    "id": "guideline-pantone-hex-screen-approximation",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "color-keyword-pantone-coy-2004-tigerlily",
    "space": "concept"
   },
   "relation": "same_as",
   "to": {
    "id": "color-keyword-ext-tigerlily",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "color-keyword-pantone-coy-2005-blue-turquoise",
    "space": "concept"
   },
   "relation": "belongs_to_topic",
   "to": {
    "id": "topic-color-pantone-trend",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "color-keyword-pantone-coy-2005-blue-turquoise",
    "space": "concept"
   },
   "relation": "cites",
   "to": {
    "id": "ref-pantone-coy-announcements",
    "space": "resource"
   }
  },
  {
   "from": {
    "id": "color-keyword-pantone-coy-2005-blue-turquoise",
    "space": "concept"
   },
   "relation": "belongs_to_topic",
   "to": {
    "id": "topic-color-blue-spectrum",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "color-keyword-pantone-coy-2005-blue-turquoise",
    "space": "concept"
   },
   "relation": "requires",
   "to": {
    "id": "guideline-pantone-hex-screen-approximation",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "color-keyword-pantone-coy-2006-sand-dollar",
    "space": "concept"
   },
   "relation": "belongs_to_topic",
   "to": {
    "id": "topic-color-pantone-trend",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "color-keyword-pantone-coy-2006-sand-dollar",
    "space": "concept"
   },
   "relation": "cites",
   "to": {
    "id": "ref-pantone-coy-announcements",
    "space": "resource"
   }
  },
  {
   "from": {
    "id": "color-keyword-pantone-coy-2006-sand-dollar",
    "space": "concept"
   },
   "relation": "belongs_to_topic",
   "to": {
    "id": "topic-color-yellow-spectrum",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "color-keyword-pantone-coy-2006-sand-dollar",
    "space": "concept"
   },
   "relation": "requires",
   "to": {
    "id": "guideline-pantone-hex-screen-approximation",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "color-keyword-pantone-coy-2007-chili-pepper",
    "space": "concept"
   },
   "relation": "belongs_to_topic",
   "to": {
    "id": "topic-color-pantone-trend",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "color-keyword-pantone-coy-2007-chili-pepper",
    "space": "concept"
   },
   "relation": "cites",
   "to": {
    "id": "ref-pantone-coy-announcements",
    "space": "resource"
   }
  },
  {
   "from": {
    "id": "color-keyword-pantone-coy-2007-chili-pepper",
    "space": "concept"
   },
   "relation": "belongs_to_topic",
   "to": {
    "id": "topic-color-red-spectrum",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "color-keyword-pantone-coy-2007-chili-pepper",
    "space": "concept"
   },
   "relation": "requires",
   "to": {
    "id": "guideline-pantone-hex-screen-approximation",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "color-keyword-pantone-coy-2008-blue-iris",
    "space": "concept"
   },
   "relation": "belongs_to_topic",
   "to": {
    "id": "topic-color-pantone-trend",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "color-keyword-pantone-coy-2008-blue-iris",
    "space": "concept"
   },
   "relation": "cites",
   "to": {
    "id": "ref-pantone-coy-announcements",
    "space": "resource"
   }
  },
  {
   "from": {
    "id": "color-keyword-pantone-coy-2008-blue-iris",
    "space": "concept"
   },
   "relation": "belongs_to_topic",
   "to": {
    "id": "topic-color-violet-spectrum",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "color-keyword-pantone-coy-2008-blue-iris",
    "space": "concept"
   },
   "relation": "requires",
   "to": {
    "id": "guideline-pantone-hex-screen-approximation",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "color-keyword-pantone-coy-2009-mimosa",
    "space": "concept"
   },
   "relation": "belongs_to_topic",
   "to": {
    "id": "topic-color-pantone-trend",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "color-keyword-pantone-coy-2009-mimosa",
    "space": "concept"
   },
   "relation": "cites",
   "to": {
    "id": "ref-pantone-coy-announcements",
    "space": "resource"
   }
  },
  {
   "from": {
    "id": "color-keyword-pantone-coy-2009-mimosa",
    "space": "concept"
   },
   "relation": "belongs_to_topic",
   "to": {
    "id": "topic-color-yellow-spectrum",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "color-keyword-pantone-coy-2009-mimosa",
    "space": "concept"
   },
   "relation": "requires",
   "to": {
    "id": "guideline-pantone-hex-screen-approximation",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "color-keyword-pantone-coy-2010-turquoise",
    "space": "concept"
   },
   "relation": "belongs_to_topic",
   "to": {
    "id": "topic-color-pantone-trend",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "color-keyword-pantone-coy-2010-turquoise",
    "space": "concept"
   },
   "relation": "cites",
   "to": {
    "id": "ref-pantone-coy-announcements",
    "space": "resource"
   }
  },
  {
   "from": {
    "id": "color-keyword-pantone-coy-2010-turquoise",
    "space": "concept"
   },
   "relation": "belongs_to_topic",
   "to": {
    "id": "topic-color-blue-spectrum",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "color-keyword-pantone-coy-2010-turquoise",
    "space": "concept"
   },
   "relation": "requires",
   "to": {
    "id": "guideline-pantone-hex-screen-approximation",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "color-keyword-pantone-coy-2011-honeysuckle",
    "space": "concept"
   },
   "relation": "belongs_to_topic",
   "to": {
    "id": "topic-color-pantone-trend",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "color-keyword-pantone-coy-2011-honeysuckle",
    "space": "concept"
   },
   "relation": "cites",
   "to": {
    "id": "ref-pantone-coy-announcements",
    "space": "resource"
   }
  },
  {
   "from": {
    "id": "color-keyword-pantone-coy-2011-honeysuckle",
    "space": "concept"
   },
   "relation": "belongs_to_topic",
   "to": {
    "id": "topic-color-red-spectrum",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "color-keyword-pantone-coy-2011-honeysuckle",
    "space": "concept"
   },
   "relation": "requires",
   "to": {
    "id": "guideline-pantone-hex-screen-approximation",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "color-keyword-pantone-coy-2012-tangerine-tango",
    "space": "concept"
   },
   "relation": "belongs_to_topic",
   "to": {
    "id": "topic-color-pantone-trend",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "color-keyword-pantone-coy-2012-tangerine-tango",
    "space": "concept"
   },
   "relation": "cites",
   "to": {
    "id": "ref-pantone-coy-announcements",
    "space": "resource"
   }
  },
  {
   "from": {
    "id": "color-keyword-pantone-coy-2012-tangerine-tango",
    "space": "concept"
   },
   "relation": "belongs_to_topic",
   "to": {
    "id": "topic-color-orange-spectrum",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "color-keyword-pantone-coy-2012-tangerine-tango",
    "space": "concept"
   },
   "relation": "requires",
   "to": {
    "id": "guideline-pantone-hex-screen-approximation",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "color-keyword-pantone-coy-2013-emerald",
    "space": "concept"
   },
   "relation": "belongs_to_topic",
   "to": {
    "id": "topic-color-pantone-trend",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "color-keyword-pantone-coy-2013-emerald",
    "space": "concept"
   },
   "relation": "cites",
   "to": {
    "id": "ref-pantone-coy-announcements",
    "space": "resource"
   }
  },
  {
   "from": {
    "id": "color-keyword-pantone-coy-2013-emerald",
    "space": "concept"
   },
   "relation": "belongs_to_topic",
   "to": {
    "id": "topic-color-green-spectrum",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "color-keyword-pantone-coy-2013-emerald",
    "space": "concept"
   },
   "relation": "requires",
   "to": {
    "id": "guideline-pantone-hex-screen-approximation",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "color-keyword-pantone-coy-2014-radiant-orchid",
    "space": "concept"
   },
   "relation": "belongs_to_topic",
   "to": {
    "id": "topic-color-pantone-trend",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "color-keyword-pantone-coy-2014-radiant-orchid",
    "space": "concept"
   },
   "relation": "cites",
   "to": {
    "id": "ref-pantone-coy-announcements",
    "space": "resource"
   }
  },
  {
   "from": {
    "id": "color-keyword-pantone-coy-2014-radiant-orchid",
    "space": "concept"
   },
   "relation": "belongs_to_topic",
   "to": {
    "id": "topic-color-violet-spectrum",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "color-keyword-pantone-coy-2014-radiant-orchid",
    "space": "concept"
   },
   "relation": "requires",
   "to": {
    "id": "guideline-pantone-hex-screen-approximation",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "color-keyword-pantone-coy-2014-radiant-orchid",
    "space": "concept"
   },
   "relation": "same_as",
   "to": {
    "id": "color-keyword-ext-radiant-orchid",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "color-keyword-pantone-coy-2015-marsala",
    "space": "concept"
   },
   "relation": "belongs_to_topic",
   "to": {
    "id": "topic-color-pantone-trend",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "color-keyword-pantone-coy-2015-marsala",
    "space": "concept"
   },
   "relation": "cites",
   "to": {
    "id": "ref-pantone-coy-announcements",
    "space": "resource"
   }
  },
  {
   "from": {
    "id": "color-keyword-pantone-coy-2015-marsala",
    "space": "concept"
   },
   "relation": "belongs_to_topic",
   "to": {
    "id": "topic-color-red-spectrum",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "color-keyword-pantone-coy-2015-marsala",
    "space": "concept"
   },
   "relation": "requires",
   "to": {
    "id": "guideline-pantone-hex-screen-approximation",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "color-keyword-pantone-coy-2015-marsala",
    "space": "concept"
   },
   "relation": "same_as",
   "to": {
    "id": "color-keyword-marsala",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "color-keyword-pantone-coy-2016-rose-quartz",
    "space": "concept"
   },
   "relation": "belongs_to_topic",
   "to": {
    "id": "topic-color-pantone-trend",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "color-keyword-pantone-coy-2016-rose-quartz",
    "space": "concept"
   },
   "relation": "cites",
   "to": {
    "id": "ref-pantone-coy-announcements",
    "space": "resource"
   }
  },
  {
   "from": {
    "id": "color-keyword-pantone-coy-2016-rose-quartz",
    "space": "concept"
   },
   "relation": "belongs_to_topic",
   "to": {
    "id": "topic-color-red-spectrum",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "color-keyword-pantone-coy-2016-rose-quartz",
    "space": "concept"
   },
   "relation": "requires",
   "to": {
    "id": "guideline-pantone-hex-screen-approximation",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "color-keyword-pantone-coy-2016-serenity",
    "space": "concept"
   },
   "relation": "belongs_to_topic",
   "to": {
    "id": "topic-color-pantone-trend",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "color-keyword-pantone-coy-2016-serenity",
    "space": "concept"
   },
   "relation": "cites",
   "to": {
    "id": "ref-pantone-coy-announcements",
    "space": "resource"
   }
  },
  {
   "from": {
    "id": "color-keyword-pantone-coy-2016-serenity",
    "space": "concept"
   },
   "relation": "belongs_to_topic",
   "to": {
    "id": "topic-color-blue-spectrum",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "color-keyword-pantone-coy-2016-serenity",
    "space": "concept"
   },
   "relation": "requires",
   "to": {
    "id": "guideline-pantone-hex-screen-approximation",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "color-keyword-pantone-coy-2017-greenery",
    "space": "concept"
   },
   "relation": "belongs_to_topic",
   "to": {
    "id": "topic-color-pantone-trend",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "color-keyword-pantone-coy-2017-greenery",
    "space": "concept"
   },
   "relation": "cites",
   "to": {
    "id": "ref-pantone-coy-announcements",
    "space": "resource"
   }
  },
  {
   "from": {
    "id": "color-keyword-pantone-coy-2017-greenery",
    "space": "concept"
   },
   "relation": "belongs_to_topic",
   "to": {
    "id": "topic-color-green-spectrum",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "color-keyword-pantone-coy-2017-greenery",
    "space": "concept"
   },
   "relation": "requires",
   "to": {
    "id": "guideline-pantone-hex-screen-approximation",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "color-keyword-pantone-coy-2017-greenery",
    "space": "concept"
   },
   "relation": "same_as",
   "to": {
    "id": "color-keyword-greenery",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "color-keyword-pantone-coy-2018-ultra-violet",
    "space": "concept"
   },
   "relation": "belongs_to_topic",
   "to": {
    "id": "topic-color-pantone-trend",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "color-keyword-pantone-coy-2018-ultra-violet",
    "space": "concept"
   },
   "relation": "cites",
   "to": {
    "id": "ref-pantone-coy-announcements",
    "space": "resource"
   }
  },
  {
   "from": {
    "id": "color-keyword-pantone-coy-2018-ultra-violet",
    "space": "concept"
   },
   "relation": "belongs_to_topic",
   "to": {
    "id": "topic-color-violet-spectrum",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "color-keyword-pantone-coy-2018-ultra-violet",
    "space": "concept"
   },
   "relation": "requires",
   "to": {
    "id": "guideline-pantone-hex-screen-approximation",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "color-keyword-pantone-coy-2018-ultra-violet",
    "space": "concept"
   },
   "relation": "same_as",
   "to": {
    "id": "color-keyword-ultra-violet",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "color-keyword-pantone-coy-2019-living-coral",
    "space": "concept"
   },
   "relation": "belongs_to_topic",
   "to": {
    "id": "topic-color-pantone-trend",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "color-keyword-pantone-coy-2019-living-coral",
    "space": "concept"
   },
   "relation": "cites",
   "to": {
    "id": "ref-pantone-coy-announcements",
    "space": "resource"
   }
  },
  {
   "from": {
    "id": "color-keyword-pantone-coy-2019-living-coral",
    "space": "concept"
   },
   "relation": "belongs_to_topic",
   "to": {
    "id": "topic-color-orange-spectrum",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "color-keyword-pantone-coy-2019-living-coral",
    "space": "concept"
   },
   "relation": "requires",
   "to": {
    "id": "guideline-pantone-hex-screen-approximation",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "color-keyword-pantone-coy-2019-living-coral",
    "space": "concept"
   },
   "relation": "same_as",
   "to": {
    "id": "color-keyword-living-coral",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "color-keyword-pantone-coy-2020-classic-blue",
    "space": "concept"
   },
   "relation": "belongs_to_topic",
   "to": {
    "id": "topic-color-pantone-trend",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "color-keyword-pantone-coy-2020-classic-blue",
    "space": "concept"
   },
   "relation": "cites",
   "to": {
    "id": "ref-pantone-coy-announcements",
    "space": "resource"
   }
  },
  {
   "from": {
    "id": "color-keyword-pantone-coy-2020-classic-blue",
    "space": "concept"
   },
   "relation": "belongs_to_topic",
   "to": {
    "id": "topic-color-blue-spectrum",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "color-keyword-pantone-coy-2020-classic-blue",
    "space": "concept"
   },
   "relation": "requires",
   "to": {
    "id": "guideline-pantone-hex-screen-approximation",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "color-keyword-pantone-coy-2020-classic-blue",
    "space": "concept"
   },
   "relation": "same_as",
   "to": {
    "id": "color-keyword-classic-blue",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "color-keyword-pantone-coy-2021-ultimate-gray",
    "space": "concept"
   },
   "relation": "belongs_to_topic",
   "to": {
    "id": "topic-color-pantone-trend",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "color-keyword-pantone-coy-2021-ultimate-gray",
    "space": "concept"
   },
   "relation": "cites",
   "to": {
    "id": "ref-pantone-coy-announcements",
    "space": "resource"
   }
  },
  {
   "from": {
    "id": "color-keyword-pantone-coy-2021-ultimate-gray",
    "space": "concept"
   },
   "relation": "requires",
   "to": {
    "id": "guideline-pantone-hex-screen-approximation",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "color-keyword-pantone-coy-2021-illuminating",
    "space": "concept"
   },
   "relation": "belongs_to_topic",
   "to": {
    "id": "topic-color-pantone-trend",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "color-keyword-pantone-coy-2021-illuminating",
    "space": "concept"
   },
   "relation": "cites",
   "to": {
    "id": "ref-pantone-coy-announcements",
    "space": "resource"
   }
  },
  {
   "from": {
    "id": "color-keyword-pantone-coy-2021-illuminating",
    "space": "concept"
   },
   "relation": "belongs_to_topic",
   "to": {
    "id": "topic-color-yellow-spectrum",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "color-keyword-pantone-coy-2021-illuminating",
    "space": "concept"
   },
   "relation": "requires",
   "to": {
    "id": "guideline-pantone-hex-screen-approximation",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "color-keyword-pantone-coy-2021-illuminating",
    "space": "concept"
   },
   "relation": "same_as",
   "to": {
    "id": "color-keyword-illuminating",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "color-keyword-pantone-coy-2022-very-peri",
    "space": "concept"
   },
   "relation": "belongs_to_topic",
   "to": {
    "id": "topic-color-pantone-trend",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "color-keyword-pantone-coy-2022-very-peri",
    "space": "concept"
   },
   "relation": "cites",
   "to": {
    "id": "ref-pantone-coy-announcements",
    "space": "resource"
   }
  },
  {
   "from": {
    "id": "color-keyword-pantone-coy-2022-very-peri",
    "space": "concept"
   },
   "relation": "belongs_to_topic",
   "to": {
    "id": "topic-color-violet-spectrum",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "color-keyword-pantone-coy-2022-very-peri",
    "space": "concept"
   },
   "relation": "requires",
   "to": {
    "id": "guideline-pantone-hex-screen-approximation",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "color-keyword-pantone-coy-2022-very-peri",
    "space": "concept"
   },
   "relation": "same_as",
   "to": {
    "id": "color-keyword-very-peri",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "color-keyword-pantone-coy-2023-viva-magenta",
    "space": "concept"
   },
   "relation": "belongs_to_topic",
   "to": {
    "id": "topic-color-pantone-trend",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "color-keyword-pantone-coy-2023-viva-magenta",
    "space": "concept"
   },
   "relation": "cites",
   "to": {
    "id": "ref-pantone-coy-announcements",
    "space": "resource"
   }
  },
  {
   "from": {
    "id": "color-keyword-pantone-coy-2023-viva-magenta",
    "space": "concept"
   },
   "relation": "belongs_to_topic",
   "to": {
    "id": "topic-color-red-spectrum",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "color-keyword-pantone-coy-2023-viva-magenta",
    "space": "concept"
   },
   "relation": "requires",
   "to": {
    "id": "guideline-pantone-hex-screen-approximation",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "color-keyword-pantone-coy-2024-peach-fuzz",
    "space": "concept"
   },
   "relation": "belongs_to_topic",
   "to": {
    "id": "topic-color-pantone-trend",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "color-keyword-pantone-coy-2024-peach-fuzz",
    "space": "concept"
   },
   "relation": "cites",
   "to": {
    "id": "ref-pantone-coy-announcements",
    "space": "resource"
   }
  },
  {
   "from": {
    "id": "color-keyword-pantone-coy-2024-peach-fuzz",
    "space": "concept"
   },
   "relation": "belongs_to_topic",
   "to": {
    "id": "topic-color-orange-spectrum",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "color-keyword-pantone-coy-2024-peach-fuzz",
    "space": "concept"
   },
   "relation": "requires",
   "to": {
    "id": "guideline-pantone-hex-screen-approximation",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "color-keyword-pantone-coy-2025-mocha-mousse",
    "space": "concept"
   },
   "relation": "belongs_to_topic",
   "to": {
    "id": "topic-color-pantone-trend",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "color-keyword-pantone-coy-2025-mocha-mousse",
    "space": "concept"
   },
   "relation": "cites",
   "to": {
    "id": "ref-pantone-coy-announcements",
    "space": "resource"
   }
  },
  {
   "from": {
    "id": "color-keyword-pantone-coy-2025-mocha-mousse",
    "space": "concept"
   },
   "relation": "belongs_to_topic",
   "to": {
    "id": "topic-color-orange-spectrum",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "color-keyword-pantone-coy-2025-mocha-mousse",
    "space": "concept"
   },
   "relation": "requires",
   "to": {
    "id": "guideline-pantone-hex-screen-approximation",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "color-keyword-pantone-coy-2026-cloud-dancer",
    "space": "concept"
   },
   "relation": "belongs_to_topic",
   "to": {
    "id": "topic-color-pantone-trend",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "color-keyword-pantone-coy-2026-cloud-dancer",
    "space": "concept"
   },
   "relation": "cites",
   "to": {
    "id": "ref-pantone-coy-announcements",
    "space": "resource"
   }
  },
  {
   "from": {
    "id": "color-keyword-pantone-coy-2026-cloud-dancer",
    "space": "concept"
   },
   "relation": "requires",
   "to": {
    "id": "guideline-pantone-hex-screen-approximation",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "pattern-brief-palette-deep-blue-cold-luxury-web",
    "space": "concept"
   },
   "relation": "belongs_to_topic",
   "to": {
    "id": "topic-color-palette-abstraction-policy",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "pattern-brief-palette-deep-blue-cold-luxury-web",
    "space": "concept"
   },
   "relation": "cites",
   "to": {
    "id": "ref-reference-x-vol1-color",
    "space": "resource"
   }
  },
  {
   "from": {
    "id": "pattern-brief-palette-deep-blue-cold-luxury-web",
    "space": "concept"
   },
   "relation": "requires",
   "to": {
    "id": "guideline-no-palette-table-reconstruction",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "pattern-brief-palette-deep-blue-cold-luxury-web",
    "space": "concept"
   },
   "relation": "requires",
   "to": {
    "id": "pattern-safe-palette-output-contract",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "pattern-brief-palette-deep-blue-cold-luxury-web",
    "space": "concept"
   },
   "relation": "requires",
   "to": {
    "id": "pattern-color-keyword-to-tone-archive",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "pattern-brief-palette-deep-blue-cold-luxury-web",
    "space": "concept"
   },
   "relation": "pairs_well_with",
   "to": {
    "id": "pattern-tone-archive-preserves-transferability",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "pattern-brief-palette-deep-blue-cold-luxury-web",
    "space": "concept"
   },
   "relation": "pairs_well_with",
   "to": {
    "id": "guideline-do-not-bind-color-to-fixed-subject",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "pattern-brief-palette-deep-blue-cold-luxury-web",
    "space": "concept"
   },
   "relation": "requires",
   "to": {
    "id": "color-keyword-navy-blue",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "pattern-brief-palette-deep-blue-cold-luxury-web",
    "space": "concept"
   },
   "relation": "requires",
   "to": {
    "id": "color-keyword-prussian-blue",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "pattern-brief-palette-deep-blue-cold-luxury-web",
    "space": "concept"
   },
   "relation": "requires",
   "to": {
    "id": "color-keyword-classic-blue",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "pattern-brief-palette-deep-blue-cold-luxury-web",
    "space": "concept"
   },
   "relation": "requires",
   "to": {
    "id": "color-keyword-ice-blue",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "pattern-brief-palette-stable-green-ui-surface",
    "space": "concept"
   },
   "relation": "belongs_to_topic",
   "to": {
    "id": "topic-color-palette-abstraction-policy",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "pattern-brief-palette-stable-green-ui-surface",
    "space": "concept"
   },
   "relation": "cites",
   "to": {
    "id": "ref-reference-x-vol1-color",
    "space": "resource"
   }
  },
  {
   "from": {
    "id": "pattern-brief-palette-stable-green-ui-surface",
    "space": "concept"
   },
   "relation": "requires",
   "to": {
    "id": "guideline-no-palette-table-reconstruction",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "pattern-brief-palette-stable-green-ui-surface",
    "space": "concept"
   },
   "relation": "requires",
   "to": {
    "id": "pattern-safe-palette-output-contract",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "pattern-brief-palette-stable-green-ui-surface",
    "space": "concept"
   },
   "relation": "requires",
   "to": {
    "id": "pattern-color-keyword-to-tone-archive",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "pattern-brief-palette-stable-green-ui-surface",
    "space": "concept"
   },
   "relation": "pairs_well_with",
   "to": {
    "id": "pattern-tone-archive-preserves-transferability",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "pattern-brief-palette-stable-green-ui-surface",
    "space": "concept"
   },
   "relation": "pairs_well_with",
   "to": {
    "id": "guideline-do-not-bind-color-to-fixed-subject",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "pattern-brief-palette-stable-green-ui-surface",
    "space": "concept"
   },
   "relation": "requires",
   "to": {
    "id": "color-keyword-forest-green",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "pattern-brief-palette-stable-green-ui-surface",
    "space": "concept"
   },
   "relation": "requires",
   "to": {
    "id": "color-keyword-bottle-green",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "pattern-brief-palette-stable-green-ui-surface",
    "space": "concept"
   },
   "relation": "requires",
   "to": {
    "id": "color-keyword-celadon",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "pattern-brief-palette-stable-green-ui-surface",
    "space": "concept"
   },
   "relation": "requires",
   "to": {
    "id": "color-keyword-cascades",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "pattern-brief-palette-stable-green-ui-surface",
    "space": "concept"
   },
   "relation": "requires",
   "to": {
    "id": "color-keyword-arcadia",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "pattern-brief-palette-manga-magazine-pop-editorial",
    "space": "concept"
   },
   "relation": "belongs_to_topic",
   "to": {
    "id": "topic-color-palette-abstraction-policy",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "pattern-brief-palette-manga-magazine-pop-editorial",
    "space": "concept"
   },
   "relation": "cites",
   "to": {
    "id": "ref-reference-x-vol1-color",
    "space": "resource"
   }
  },
  {
   "from": {
    "id": "pattern-brief-palette-manga-magazine-pop-editorial",
    "space": "concept"
   },
   "relation": "requires",
   "to": {
    "id": "guideline-no-palette-table-reconstruction",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "pattern-brief-palette-manga-magazine-pop-editorial",
    "space": "concept"
   },
   "relation": "requires",
   "to": {
    "id": "pattern-safe-palette-output-contract",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "pattern-brief-palette-manga-magazine-pop-editorial",
    "space": "concept"
   },
   "relation": "requires",
   "to": {
    "id": "pattern-color-keyword-to-tone-archive",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "pattern-brief-palette-manga-magazine-pop-editorial",
    "space": "concept"
   },
   "relation": "pairs_well_with",
   "to": {
    "id": "pattern-tone-archive-preserves-transferability",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "pattern-brief-palette-manga-magazine-pop-editorial",
    "space": "concept"
   },
   "relation": "pairs_well_with",
   "to": {
    "id": "guideline-do-not-bind-color-to-fixed-subject",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "pattern-brief-palette-manga-magazine-pop-editorial",
    "space": "concept"
   },
   "relation": "requires",
   "to": {
    "id": "color-keyword-pure-red",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "pattern-brief-palette-manga-magazine-pop-editorial",
    "space": "concept"
   },
   "relation": "requires",
   "to": {
    "id": "color-keyword-scarlet",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "pattern-brief-palette-manga-magazine-pop-editorial",
    "space": "concept"
   },
   "relation": "requires",
   "to": {
    "id": "color-keyword-buttercream",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "pattern-brief-palette-manga-magazine-pop-editorial",
    "space": "concept"
   },
   "relation": "requires",
   "to": {
    "id": "color-keyword-ultra-violet",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "pattern-brief-palette-manga-magazine-pop-editorial",
    "space": "concept"
   },
   "relation": "requires",
   "to": {
    "id": "color-keyword-illuminating",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "pattern-brief-palette-coy-mocha-warm-editorial",
    "space": "concept"
   },
   "relation": "belongs_to_topic",
   "to": {
    "id": "topic-color-palette-abstraction-policy",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "pattern-brief-palette-coy-mocha-warm-editorial",
    "space": "concept"
   },
   "relation": "belongs_to_topic",
   "to": {
    "id": "topic-color-pantone-trend",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "pattern-brief-palette-coy-mocha-warm-editorial",
    "space": "concept"
   },
   "relation": "cites",
   "to": {
    "id": "ref-reference-x-vol1-color",
    "space": "resource"
   }
  },
  {
   "from": {
    "id": "pattern-brief-palette-coy-mocha-warm-editorial",
    "space": "concept"
   },
   "relation": "cites",
   "to": {
    "id": "ref-pantone-coy-announcements",
    "space": "resource"
   }
  },
  {
   "from": {
    "id": "pattern-brief-palette-coy-mocha-warm-editorial",
    "space": "concept"
   },
   "relation": "requires",
   "to": {
    "id": "guideline-no-palette-table-reconstruction",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "pattern-brief-palette-coy-mocha-warm-editorial",
    "space": "concept"
   },
   "relation": "requires",
   "to": {
    "id": "pattern-safe-palette-output-contract",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "pattern-brief-palette-coy-mocha-warm-editorial",
    "space": "concept"
   },
   "relation": "requires",
   "to": {
    "id": "pattern-color-keyword-to-tone-archive",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "pattern-brief-palette-coy-mocha-warm-editorial",
    "space": "concept"
   },
   "relation": "requires",
   "to": {
    "id": "guideline-pantone-hex-screen-approximation",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "pattern-brief-palette-coy-mocha-warm-editorial",
    "space": "concept"
   },
   "relation": "requires",
   "to": {
    "id": "guideline-extended-keywords-name-anchor-only",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "pattern-brief-palette-coy-mocha-warm-editorial",
    "space": "concept"
   },
   "relation": "requires",
   "to": {
    "id": "color-keyword-pantone-coy-2025-mocha-mousse",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "pattern-brief-palette-coy-mocha-warm-editorial",
    "space": "concept"
   },
   "relation": "requires",
   "to": {
    "id": "color-keyword-copper",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "pattern-brief-palette-coy-mocha-warm-editorial",
    "space": "concept"
   },
   "relation": "requires",
   "to": {
    "id": "color-keyword-terracotta",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "pattern-brief-palette-coy-mocha-warm-editorial",
    "space": "concept"
   },
   "relation": "requires",
   "to": {
    "id": "color-keyword-cornsilk",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "pattern-brief-palette-coy-mocha-warm-editorial",
    "space": "concept"
   },
   "relation": "requires",
   "to": {
    "id": "color-keyword-ext-sandstone",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "pattern-brief-palette-coy-mocha-warm-editorial",
    "space": "concept"
   },
   "relation": "requires",
   "to": {
    "id": "color-keyword-ext-dune",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "pattern-brief-palette-coy-mocha-warm-editorial",
    "space": "concept"
   },
   "relation": "requires",
   "to": {
    "id": "color-keyword-ext-maple",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "guideline-color-brief-design-novelty",
    "space": "concept"
   },
   "relation": "belongs_to_topic",
   "to": {
    "id": "topic-color-palette-abstraction-policy",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "guideline-color-brief-design-novelty",
    "space": "concept"
   },
   "relation": "supports",
   "to": {
    "id": "pattern-tone-archive-preserves-transferability",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "guideline-color-brief-design-novelty",
    "space": "concept"
   },
   "relation": "supports",
   "to": {
    "id": "guideline-sample-images-validate-method-not-content",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "pattern-brief-palette-midnight-listening-lounge",
    "space": "concept"
   },
   "relation": "belongs_to_topic",
   "to": {
    "id": "topic-color-palette-abstraction-policy",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "pattern-brief-palette-midnight-listening-lounge",
    "space": "concept"
   },
   "relation": "cites",
   "to": {
    "id": "ref-reference-x-vol1-color",
    "space": "resource"
   }
  },
  {
   "from": {
    "id": "pattern-brief-palette-midnight-listening-lounge",
    "space": "concept"
   },
   "relation": "requires",
   "to": {
    "id": "guideline-no-palette-table-reconstruction",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "pattern-brief-palette-midnight-listening-lounge",
    "space": "concept"
   },
   "relation": "requires",
   "to": {
    "id": "pattern-safe-palette-output-contract",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "pattern-brief-palette-midnight-listening-lounge",
    "space": "concept"
   },
   "relation": "requires",
   "to": {
    "id": "pattern-color-keyword-to-tone-archive",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "pattern-brief-palette-midnight-listening-lounge",
    "space": "concept"
   },
   "relation": "requires",
   "to": {
    "id": "guideline-color-brief-design-novelty",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "pattern-brief-palette-midnight-listening-lounge",
    "space": "concept"
   },
   "relation": "requires",
   "to": {
    "id": "color-keyword-midnight-violet",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "pattern-brief-palette-midnight-listening-lounge",
    "space": "concept"
   },
   "relation": "requires",
   "to": {
    "id": "color-keyword-byzantium",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "pattern-brief-palette-midnight-listening-lounge",
    "space": "concept"
   },
   "relation": "requires",
   "to": {
    "id": "color-keyword-honey-gold",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "pattern-brief-palette-midnight-listening-lounge",
    "space": "concept"
   },
   "relation": "requires",
   "to": {
    "id": "color-keyword-lavender-mist",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "pattern-brief-palette-aquarium-depth-descent",
    "space": "concept"
   },
   "relation": "belongs_to_topic",
   "to": {
    "id": "topic-color-palette-abstraction-policy",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "pattern-brief-palette-aquarium-depth-descent",
    "space": "concept"
   },
   "relation": "cites",
   "to": {
    "id": "ref-reference-x-vol1-color",
    "space": "resource"
   }
  },
  {
   "from": {
    "id": "pattern-brief-palette-aquarium-depth-descent",
    "space": "concept"
   },
   "relation": "requires",
   "to": {
    "id": "guideline-no-palette-table-reconstruction",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "pattern-brief-palette-aquarium-depth-descent",
    "space": "concept"
   },
   "relation": "requires",
   "to": {
    "id": "pattern-safe-palette-output-contract",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "pattern-brief-palette-aquarium-depth-descent",
    "space": "concept"
   },
   "relation": "requires",
   "to": {
    "id": "pattern-color-keyword-to-tone-archive",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "pattern-brief-palette-aquarium-depth-descent",
    "space": "concept"
   },
   "relation": "requires",
   "to": {
    "id": "guideline-color-brief-design-novelty",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "pattern-brief-palette-aquarium-depth-descent",
    "space": "concept"
   },
   "relation": "requires",
   "to": {
    "id": "color-keyword-prussian-blue",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "pattern-brief-palette-aquarium-depth-descent",
    "space": "concept"
   },
   "relation": "requires",
   "to": {
    "id": "color-keyword-classic-blue",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "pattern-brief-palette-aquarium-depth-descent",
    "space": "concept"
   },
   "relation": "requires",
   "to": {
    "id": "color-keyword-blue-atoll",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "pattern-brief-palette-aquarium-depth-descent",
    "space": "concept"
   },
   "relation": "requires",
   "to": {
    "id": "color-keyword-ice-blue",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "pattern-brief-palette-deep-blue-cold-luxury-web",
    "space": "concept"
   },
   "relation": "requires",
   "to": {
    "id": "guideline-palette-not-three-color-pick",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "pattern-brief-palette-deep-blue-cold-luxury-web",
    "space": "concept"
   },
   "relation": "requires",
   "to": {
    "id": "pattern-palette-role-combination-matrix",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "pattern-brief-palette-deep-blue-cold-luxury-web",
    "space": "concept"
   },
   "relation": "requires",
   "to": {
    "id": "pattern-palette-combination-to-component-token-grid",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "pattern-brief-palette-stable-green-ui-surface",
    "space": "concept"
   },
   "relation": "requires",
   "to": {
    "id": "guideline-palette-not-three-color-pick",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "pattern-brief-palette-stable-green-ui-surface",
    "space": "concept"
   },
   "relation": "requires",
   "to": {
    "id": "pattern-palette-role-combination-matrix",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "pattern-brief-palette-stable-green-ui-surface",
    "space": "concept"
   },
   "relation": "requires",
   "to": {
    "id": "pattern-palette-combination-to-component-token-grid",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "pattern-brief-palette-manga-magazine-pop-editorial",
    "space": "concept"
   },
   "relation": "requires",
   "to": {
    "id": "guideline-palette-not-three-color-pick",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "pattern-brief-palette-manga-magazine-pop-editorial",
    "space": "concept"
   },
   "relation": "requires",
   "to": {
    "id": "pattern-palette-role-combination-matrix",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "pattern-brief-palette-manga-magazine-pop-editorial",
    "space": "concept"
   },
   "relation": "requires",
   "to": {
    "id": "pattern-palette-combination-to-component-token-grid",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "pattern-brief-palette-coy-mocha-warm-editorial",
    "space": "concept"
   },
   "relation": "requires",
   "to": {
    "id": "guideline-palette-not-three-color-pick",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "pattern-brief-palette-coy-mocha-warm-editorial",
    "space": "concept"
   },
   "relation": "requires",
   "to": {
    "id": "pattern-palette-role-combination-matrix",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "pattern-brief-palette-coy-mocha-warm-editorial",
    "space": "concept"
   },
   "relation": "requires",
   "to": {
    "id": "pattern-palette-combination-to-component-token-grid",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "pattern-brief-palette-midnight-listening-lounge",
    "space": "concept"
   },
   "relation": "requires",
   "to": {
    "id": "guideline-palette-not-three-color-pick",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "pattern-brief-palette-midnight-listening-lounge",
    "space": "concept"
   },
   "relation": "requires",
   "to": {
    "id": "pattern-palette-role-combination-matrix",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "pattern-brief-palette-midnight-listening-lounge",
    "space": "concept"
   },
   "relation": "requires",
   "to": {
    "id": "pattern-palette-combination-to-component-token-grid",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "pattern-brief-palette-aquarium-depth-descent",
    "space": "concept"
   },
   "relation": "requires",
   "to": {
    "id": "guideline-palette-not-three-color-pick",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "pattern-brief-palette-aquarium-depth-descent",
    "space": "concept"
   },
   "relation": "requires",
   "to": {
    "id": "pattern-palette-role-combination-matrix",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "pattern-brief-palette-aquarium-depth-descent",
    "space": "concept"
   },
   "relation": "requires",
   "to": {
    "id": "pattern-palette-combination-to-component-token-grid",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "layer-color-reference-x-v1",
    "space": "resource"
   },
   "relation": "contains",
   "to": {
    "id": "topic-color-reference-keywords",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "layer-color-reference-x-v1",
    "space": "resource"
   },
   "relation": "contains",
   "to": {
    "id": "topic-color-basic-systems",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "layer-color-reference-x-v1",
    "space": "resource"
   },
   "relation": "contains",
   "to": {
    "id": "topic-color-emotion-mechanism",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "layer-color-reference-x-v1",
    "space": "resource"
   },
   "relation": "contains",
   "to": {
    "id": "topic-color-red-spectrum",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "layer-color-reference-x-v1",
    "space": "resource"
   },
   "relation": "contains",
   "to": {
    "id": "topic-color-orange-spectrum",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "layer-color-reference-x-v1",
    "space": "resource"
   },
   "relation": "contains",
   "to": {
    "id": "topic-color-yellow-spectrum",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "layer-color-reference-x-v1",
    "space": "resource"
   },
   "relation": "contains",
   "to": {
    "id": "topic-color-green-spectrum",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "layer-color-reference-x-v1",
    "space": "resource"
   },
   "relation": "contains",
   "to": {
    "id": "topic-color-blue-spectrum",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "layer-color-reference-x-v1",
    "space": "resource"
   },
   "relation": "contains",
   "to": {
    "id": "topic-color-violet-spectrum",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "layer-color-reference-x-v1",
    "space": "resource"
   },
   "relation": "contains",
   "to": {
    "id": "topic-color-application",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "layer-color-reference-x-v1",
    "space": "resource"
   },
   "relation": "cites",
   "to": {
    "id": "ref-reference-x-vol1-color",
    "space": "resource"
   }
  },
  {
   "from": {
    "id": "system-rgb-additive",
    "space": "concept"
   },
   "relation": "belongs_to_topic",
   "to": {
    "id": "topic-color-basic-systems",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "system-rgb-additive",
    "space": "concept"
   },
   "relation": "cites",
   "to": {
    "id": "ref-reference-x-vol1-color",
    "space": "resource"
   }
  },
  {
   "from": {
    "id": "system-cmyk-subtractive",
    "space": "concept"
   },
   "relation": "belongs_to_topic",
   "to": {
    "id": "topic-color-basic-systems",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "system-cmyk-subtractive",
    "space": "concept"
   },
   "relation": "cites",
   "to": {
    "id": "ref-reference-x-vol1-color",
    "space": "resource"
   }
  },
  {
   "from": {
    "id": "system-srgb-reference",
    "space": "concept"
   },
   "relation": "belongs_to_topic",
   "to": {
    "id": "topic-color-basic-systems",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "system-srgb-reference",
    "space": "concept"
   },
   "relation": "cites",
   "to": {
    "id": "ref-reference-x-vol1-color",
    "space": "resource"
   }
  },
  {
   "from": {
    "id": "system-coated-gracol-2006",
    "space": "concept"
   },
   "relation": "belongs_to_topic",
   "to": {
    "id": "topic-color-basic-systems",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "system-coated-gracol-2006",
    "space": "concept"
   },
   "relation": "cites",
   "to": {
    "id": "ref-reference-x-vol1-color",
    "space": "resource"
   }
  },
  {
   "from": {
    "id": "metric-concept-clarity",
    "space": "concept"
   },
   "relation": "belongs_to_topic",
   "to": {
    "id": "topic-color-application",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "metric-concept-clarity",
    "space": "concept"
   },
   "relation": "cites",
   "to": {
    "id": "ref-reference-x-vol1-color",
    "space": "resource"
   }
  },
  {
   "from": {
    "id": "metric-saturation",
    "space": "concept"
   },
   "relation": "belongs_to_topic",
   "to": {
    "id": "topic-color-application",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "metric-saturation",
    "space": "concept"
   },
   "relation": "cites",
   "to": {
    "id": "ref-reference-x-vol1-color",
    "space": "resource"
   }
  },
  {
   "from": {
    "id": "metric-symbolism",
    "space": "concept"
   },
   "relation": "belongs_to_topic",
   "to": {
    "id": "topic-color-application",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "metric-symbolism",
    "space": "concept"
   },
   "relation": "cites",
   "to": {
    "id": "ref-reference-x-vol1-color",
    "space": "resource"
   }
  },
  {
   "from": {
    "id": "metric-trendiness",
    "space": "concept"
   },
   "relation": "belongs_to_topic",
   "to": {
    "id": "topic-color-application",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "metric-trendiness",
    "space": "concept"
   },
   "relation": "cites",
   "to": {
    "id": "ref-reference-x-vol1-color",
    "space": "resource"
   }
  },
  {
   "from": {
    "id": "metric-imagery-depth",
    "space": "concept"
   },
   "relation": "belongs_to_topic",
   "to": {
    "id": "topic-color-application",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "metric-imagery-depth",
    "space": "concept"
   },
   "relation": "cites",
   "to": {
    "id": "ref-reference-x-vol1-color",
    "space": "resource"
   }
  },
  {
   "from": {
    "id": "metric-versatility",
    "space": "concept"
   },
   "relation": "belongs_to_topic",
   "to": {
    "id": "topic-color-application",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "metric-versatility",
    "space": "concept"
   },
   "relation": "cites",
   "to": {
    "id": "ref-reference-x-vol1-color",
    "space": "resource"
   }
  },
  {
   "from": {
    "id": "metric-visibility",
    "space": "concept"
   },
   "relation": "belongs_to_topic",
   "to": {
    "id": "topic-color-application",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "metric-visibility",
    "space": "concept"
   },
   "relation": "cites",
   "to": {
    "id": "ref-reference-x-vol1-color",
    "space": "resource"
   }
  },
  {
   "from": {
    "id": "metric-stability",
    "space": "concept"
   },
   "relation": "belongs_to_topic",
   "to": {
    "id": "topic-color-application",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "metric-stability",
    "space": "concept"
   },
   "relation": "cites",
   "to": {
    "id": "ref-reference-x-vol1-color",
    "space": "resource"
   }
  },
  {
   "from": {
    "id": "heuristic-reference-keyword-controls-design-direction",
    "space": "concept"
   },
   "relation": "belongs_to_topic",
   "to": {
    "id": "topic-color-reference-keywords",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "heuristic-reference-keyword-controls-design-direction",
    "space": "concept"
   },
   "relation": "cites",
   "to": {
    "id": "ref-reference-x-vol1-color",
    "space": "resource"
   }
  },
  {
   "from": {
    "id": "heuristic-color-read-before-form",
    "space": "concept"
   },
   "relation": "belongs_to_topic",
   "to": {
    "id": "topic-color-emotion-mechanism",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "heuristic-color-read-before-form",
    "space": "concept"
   },
   "relation": "cites",
   "to": {
    "id": "ref-reference-x-vol1-color",
    "space": "resource"
   }
  },
  {
   "from": {
    "id": "guideline-rgb-cmyk-split-by-output-medium",
    "space": "concept"
   },
   "relation": "belongs_to_topic",
   "to": {
    "id": "topic-color-basic-systems",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "guideline-rgb-cmyk-split-by-output-medium",
    "space": "concept"
   },
   "relation": "cites",
   "to": {
    "id": "ref-reference-x-vol1-color",
    "space": "resource"
   }
  },
  {
   "from": {
    "id": "guideline-color-values-are-reference-not-absolute",
    "space": "concept"
   },
   "relation": "belongs_to_topic",
   "to": {
    "id": "topic-color-basic-systems",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "guideline-color-values-are-reference-not-absolute",
    "space": "concept"
   },
   "relation": "cites",
   "to": {
    "id": "ref-reference-x-vol1-color",
    "space": "resource"
   }
  },
  {
   "from": {
    "id": "pattern-spectrum-family-keyword-stack",
    "space": "concept"
   },
   "relation": "belongs_to_topic",
   "to": {
    "id": "topic-color-reference-keywords",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "pattern-spectrum-family-keyword-stack",
    "space": "concept"
   },
   "relation": "cites",
   "to": {
    "id": "ref-reference-x-vol1-color",
    "space": "resource"
   }
  },
  {
   "from": {
    "id": "pattern-color-card-triad-swatch-reading-metrics",
    "space": "concept"
   },
   "relation": "belongs_to_topic",
   "to": {
    "id": "topic-color-application",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "pattern-color-card-triad-swatch-reading-metrics",
    "space": "concept"
   },
   "relation": "cites",
   "to": {
    "id": "ref-reference-x-vol1-color",
    "space": "resource"
   }
  },
  {
   "from": {
    "id": "guideline-mood-tags-before-palette-expansion",
    "space": "concept"
   },
   "relation": "belongs_to_topic",
   "to": {
    "id": "topic-color-emotion-mechanism",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "guideline-mood-tags-before-palette-expansion",
    "space": "concept"
   },
   "relation": "cites",
   "to": {
    "id": "ref-reference-x-vol1-color",
    "space": "resource"
   }
  },
  {
   "from": {
    "id": "pattern-color-keyword-to-design-brief",
    "space": "concept"
   },
   "relation": "belongs_to_topic",
   "to": {
    "id": "topic-color-reference-keywords",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "pattern-color-keyword-to-design-brief",
    "space": "concept"
   },
   "relation": "cites",
   "to": {
    "id": "ref-reference-x-vol1-color",
    "space": "resource"
   }
  },
  {
   "from": {
    "id": "pattern-spectrum-family-keyword-stack",
    "space": "concept"
   },
   "relation": "requires",
   "to": {
    "id": "heuristic-reference-keyword-controls-design-direction",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "pattern-color-card-triad-swatch-reading-metrics",
    "space": "concept"
   },
   "relation": "requires",
   "to": {
    "id": "guideline-color-values-are-reference-not-absolute",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "guideline-rgb-cmyk-split-by-output-medium",
    "space": "concept"
   },
   "relation": "pairs_well_with",
   "to": {
    "id": "guideline-color-values-are-reference-not-absolute",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "pattern-color-keyword-to-design-brief",
    "space": "concept"
   },
   "relation": "requires",
   "to": {
    "id": "guideline-mood-tags-before-palette-expansion",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "guideline-rgb-cmyk-split-by-output-medium",
    "space": "concept"
   },
   "relation": "requires",
   "to": {
    "id": "system-rgb-additive",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "guideline-rgb-cmyk-split-by-output-medium",
    "space": "concept"
   },
   "relation": "requires",
   "to": {
    "id": "system-cmyk-subtractive",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "guideline-color-values-are-reference-not-absolute",
    "space": "concept"
   },
   "relation": "requires",
   "to": {
    "id": "system-srgb-reference",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "guideline-color-values-are-reference-not-absolute",
    "space": "concept"
   },
   "relation": "requires",
   "to": {
    "id": "system-coated-gracol-2006",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "color-keyword-pure-red",
    "space": "concept"
   },
   "relation": "belongs_to_topic",
   "to": {
    "id": "topic-color-red-spectrum",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "color-keyword-pure-red",
    "space": "concept"
   },
   "relation": "cites",
   "to": {
    "id": "ref-reference-x-vol1-color",
    "space": "resource"
   }
  },
  {
   "from": {
    "id": "color-keyword-pure-red",
    "space": "concept"
   },
   "relation": "requires",
   "to": {
    "id": "system-srgb-reference",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "color-keyword-pure-red",
    "space": "concept"
   },
   "relation": "requires",
   "to": {
    "id": "system-coated-gracol-2006",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "color-keyword-scarlet",
    "space": "concept"
   },
   "relation": "belongs_to_topic",
   "to": {
    "id": "topic-color-red-spectrum",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "color-keyword-scarlet",
    "space": "concept"
   },
   "relation": "cites",
   "to": {
    "id": "ref-reference-x-vol1-color",
    "space": "resource"
   }
  },
  {
   "from": {
    "id": "color-keyword-scarlet",
    "space": "concept"
   },
   "relation": "requires",
   "to": {
    "id": "system-srgb-reference",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "color-keyword-scarlet",
    "space": "concept"
   },
   "relation": "requires",
   "to": {
    "id": "system-coated-gracol-2006",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "color-keyword-crimson",
    "space": "concept"
   },
   "relation": "belongs_to_topic",
   "to": {
    "id": "topic-color-red-spectrum",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "color-keyword-crimson",
    "space": "concept"
   },
   "relation": "cites",
   "to": {
    "id": "ref-reference-x-vol1-color",
    "space": "resource"
   }
  },
  {
   "from": {
    "id": "color-keyword-crimson",
    "space": "concept"
   },
   "relation": "requires",
   "to": {
    "id": "system-srgb-reference",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "color-keyword-crimson",
    "space": "concept"
   },
   "relation": "requires",
   "to": {
    "id": "system-coated-gracol-2006",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "color-keyword-ruby",
    "space": "concept"
   },
   "relation": "belongs_to_topic",
   "to": {
    "id": "topic-color-red-spectrum",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "color-keyword-ruby",
    "space": "concept"
   },
   "relation": "cites",
   "to": {
    "id": "ref-reference-x-vol1-color",
    "space": "resource"
   }
  },
  {
   "from": {
    "id": "color-keyword-ruby",
    "space": "concept"
   },
   "relation": "requires",
   "to": {
    "id": "system-srgb-reference",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "color-keyword-ruby",
    "space": "concept"
   },
   "relation": "requires",
   "to": {
    "id": "system-coated-gracol-2006",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "color-keyword-coral-red",
    "space": "concept"
   },
   "relation": "belongs_to_topic",
   "to": {
    "id": "topic-color-red-spectrum",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "color-keyword-coral-red",
    "space": "concept"
   },
   "relation": "cites",
   "to": {
    "id": "ref-reference-x-vol1-color",
    "space": "resource"
   }
  },
  {
   "from": {
    "id": "color-keyword-coral-red",
    "space": "concept"
   },
   "relation": "requires",
   "to": {
    "id": "system-srgb-reference",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "color-keyword-coral-red",
    "space": "concept"
   },
   "relation": "requires",
   "to": {
    "id": "system-coated-gracol-2006",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "color-keyword-terracotta",
    "space": "concept"
   },
   "relation": "belongs_to_topic",
   "to": {
    "id": "topic-color-red-spectrum",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "color-keyword-terracotta",
    "space": "concept"
   },
   "relation": "cites",
   "to": {
    "id": "ref-reference-x-vol1-color",
    "space": "resource"
   }
  },
  {
   "from": {
    "id": "color-keyword-terracotta",
    "space": "concept"
   },
   "relation": "requires",
   "to": {
    "id": "system-srgb-reference",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "color-keyword-terracotta",
    "space": "concept"
   },
   "relation": "requires",
   "to": {
    "id": "system-coated-gracol-2006",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "color-keyword-rose-red",
    "space": "concept"
   },
   "relation": "belongs_to_topic",
   "to": {
    "id": "topic-color-red-spectrum",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "color-keyword-rose-red",
    "space": "concept"
   },
   "relation": "cites",
   "to": {
    "id": "ref-reference-x-vol1-color",
    "space": "resource"
   }
  },
  {
   "from": {
    "id": "color-keyword-rose-red",
    "space": "concept"
   },
   "relation": "requires",
   "to": {
    "id": "system-srgb-reference",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "color-keyword-rose-red",
    "space": "concept"
   },
   "relation": "requires",
   "to": {
    "id": "system-coated-gracol-2006",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "color-keyword-oxblood",
    "space": "concept"
   },
   "relation": "belongs_to_topic",
   "to": {
    "id": "topic-color-red-spectrum",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "color-keyword-oxblood",
    "space": "concept"
   },
   "relation": "cites",
   "to": {
    "id": "ref-reference-x-vol1-color",
    "space": "resource"
   }
  },
  {
   "from": {
    "id": "color-keyword-oxblood",
    "space": "concept"
   },
   "relation": "requires",
   "to": {
    "id": "system-srgb-reference",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "color-keyword-oxblood",
    "space": "concept"
   },
   "relation": "requires",
   "to": {
    "id": "system-coated-gracol-2006",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "color-keyword-claret",
    "space": "concept"
   },
   "relation": "belongs_to_topic",
   "to": {
    "id": "topic-color-red-spectrum",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "color-keyword-claret",
    "space": "concept"
   },
   "relation": "cites",
   "to": {
    "id": "ref-reference-x-vol1-color",
    "space": "resource"
   }
  },
  {
   "from": {
    "id": "color-keyword-claret",
    "space": "concept"
   },
   "relation": "requires",
   "to": {
    "id": "system-srgb-reference",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "color-keyword-claret",
    "space": "concept"
   },
   "relation": "requires",
   "to": {
    "id": "system-coated-gracol-2006",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "color-keyword-sangria",
    "space": "concept"
   },
   "relation": "belongs_to_topic",
   "to": {
    "id": "topic-color-red-spectrum",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "color-keyword-sangria",
    "space": "concept"
   },
   "relation": "cites",
   "to": {
    "id": "ref-reference-x-vol1-color",
    "space": "resource"
   }
  },
  {
   "from": {
    "id": "color-keyword-sangria",
    "space": "concept"
   },
   "relation": "requires",
   "to": {
    "id": "system-srgb-reference",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "color-keyword-sangria",
    "space": "concept"
   },
   "relation": "requires",
   "to": {
    "id": "system-coated-gracol-2006",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "color-keyword-salmon",
    "space": "concept"
   },
   "relation": "belongs_to_topic",
   "to": {
    "id": "topic-color-red-spectrum",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "color-keyword-salmon",
    "space": "concept"
   },
   "relation": "cites",
   "to": {
    "id": "ref-reference-x-vol1-color",
    "space": "resource"
   }
  },
  {
   "from": {
    "id": "color-keyword-salmon",
    "space": "concept"
   },
   "relation": "requires",
   "to": {
    "id": "system-srgb-reference",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "color-keyword-salmon",
    "space": "concept"
   },
   "relation": "requires",
   "to": {
    "id": "system-coated-gracol-2006",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "color-keyword-blush",
    "space": "concept"
   },
   "relation": "belongs_to_topic",
   "to": {
    "id": "topic-color-red-spectrum",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "color-keyword-blush",
    "space": "concept"
   },
   "relation": "cites",
   "to": {
    "id": "ref-reference-x-vol1-color",
    "space": "resource"
   }
  },
  {
   "from": {
    "id": "color-keyword-blush",
    "space": "concept"
   },
   "relation": "requires",
   "to": {
    "id": "system-srgb-reference",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "color-keyword-blush",
    "space": "concept"
   },
   "relation": "requires",
   "to": {
    "id": "system-coated-gracol-2006",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "color-keyword-marsala",
    "space": "concept"
   },
   "relation": "belongs_to_topic",
   "to": {
    "id": "topic-color-red-spectrum",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "color-keyword-marsala",
    "space": "concept"
   },
   "relation": "cites",
   "to": {
    "id": "ref-reference-x-vol1-color",
    "space": "resource"
   }
  },
  {
   "from": {
    "id": "color-keyword-marsala",
    "space": "concept"
   },
   "relation": "requires",
   "to": {
    "id": "system-srgb-reference",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "color-keyword-marsala",
    "space": "concept"
   },
   "relation": "requires",
   "to": {
    "id": "system-coated-gracol-2006",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "color-keyword-grenadine",
    "space": "concept"
   },
   "relation": "belongs_to_topic",
   "to": {
    "id": "topic-color-red-spectrum",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "color-keyword-grenadine",
    "space": "concept"
   },
   "relation": "cites",
   "to": {
    "id": "ref-reference-x-vol1-color",
    "space": "resource"
   }
  },
  {
   "from": {
    "id": "color-keyword-grenadine",
    "space": "concept"
   },
   "relation": "requires",
   "to": {
    "id": "system-srgb-reference",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "color-keyword-grenadine",
    "space": "concept"
   },
   "relation": "requires",
   "to": {
    "id": "system-coated-gracol-2006",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "color-keyword-goji-berry",
    "space": "concept"
   },
   "relation": "belongs_to_topic",
   "to": {
    "id": "topic-color-red-spectrum",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "color-keyword-goji-berry",
    "space": "concept"
   },
   "relation": "cites",
   "to": {
    "id": "ref-reference-x-vol1-color",
    "space": "resource"
   }
  },
  {
   "from": {
    "id": "color-keyword-goji-berry",
    "space": "concept"
   },
   "relation": "requires",
   "to": {
    "id": "system-srgb-reference",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "color-keyword-goji-berry",
    "space": "concept"
   },
   "relation": "requires",
   "to": {
    "id": "system-coated-gracol-2006",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "color-keyword-pure-orange",
    "space": "concept"
   },
   "relation": "belongs_to_topic",
   "to": {
    "id": "topic-color-orange-spectrum",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "color-keyword-pure-orange",
    "space": "concept"
   },
   "relation": "cites",
   "to": {
    "id": "ref-reference-x-vol1-color",
    "space": "resource"
   }
  },
  {
   "from": {
    "id": "color-keyword-pure-orange",
    "space": "concept"
   },
   "relation": "requires",
   "to": {
    "id": "system-srgb-reference",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "color-keyword-pure-orange",
    "space": "concept"
   },
   "relation": "requires",
   "to": {
    "id": "system-coated-gracol-2006",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "color-keyword-tangerine",
    "space": "concept"
   },
   "relation": "belongs_to_topic",
   "to": {
    "id": "topic-color-orange-spectrum",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "color-keyword-tangerine",
    "space": "concept"
   },
   "relation": "cites",
   "to": {
    "id": "ref-reference-x-vol1-color",
    "space": "resource"
   }
  },
  {
   "from": {
    "id": "color-keyword-tangerine",
    "space": "concept"
   },
   "relation": "requires",
   "to": {
    "id": "system-srgb-reference",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "color-keyword-tangerine",
    "space": "concept"
   },
   "relation": "requires",
   "to": {
    "id": "system-coated-gracol-2006",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "color-keyword-ochre",
    "space": "concept"
   },
   "relation": "belongs_to_topic",
   "to": {
    "id": "topic-color-orange-spectrum",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "color-keyword-ochre",
    "space": "concept"
   },
   "relation": "cites",
   "to": {
    "id": "ref-reference-x-vol1-color",
    "space": "resource"
   }
  },
  {
   "from": {
    "id": "color-keyword-ochre",
    "space": "concept"
   },
   "relation": "requires",
   "to": {
    "id": "system-srgb-reference",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "color-keyword-ochre",
    "space": "concept"
   },
   "relation": "requires",
   "to": {
    "id": "system-coated-gracol-2006",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "color-keyword-apricot",
    "space": "concept"
   },
   "relation": "belongs_to_topic",
   "to": {
    "id": "topic-color-orange-spectrum",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "color-keyword-apricot",
    "space": "concept"
   },
   "relation": "cites",
   "to": {
    "id": "ref-reference-x-vol1-color",
    "space": "resource"
   }
  },
  {
   "from": {
    "id": "color-keyword-apricot",
    "space": "concept"
   },
   "relation": "requires",
   "to": {
    "id": "system-srgb-reference",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "color-keyword-apricot",
    "space": "concept"
   },
   "relation": "requires",
   "to": {
    "id": "system-coated-gracol-2006",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "color-keyword-persimmon",
    "space": "concept"
   },
   "relation": "belongs_to_topic",
   "to": {
    "id": "topic-color-orange-spectrum",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "color-keyword-persimmon",
    "space": "concept"
   },
   "relation": "cites",
   "to": {
    "id": "ref-reference-x-vol1-color",
    "space": "resource"
   }
  },
  {
   "from": {
    "id": "color-keyword-persimmon",
    "space": "concept"
   },
   "relation": "requires",
   "to": {
    "id": "system-srgb-reference",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "color-keyword-persimmon",
    "space": "concept"
   },
   "relation": "requires",
   "to": {
    "id": "system-coated-gracol-2006",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "color-keyword-pumpkin",
    "space": "concept"
   },
   "relation": "belongs_to_topic",
   "to": {
    "id": "topic-color-orange-spectrum",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "color-keyword-pumpkin",
    "space": "concept"
   },
   "relation": "cites",
   "to": {
    "id": "ref-reference-x-vol1-color",
    "space": "resource"
   }
  },
  {
   "from": {
    "id": "color-keyword-pumpkin",
    "space": "concept"
   },
   "relation": "requires",
   "to": {
    "id": "system-srgb-reference",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "color-keyword-pumpkin",
    "space": "concept"
   },
   "relation": "requires",
   "to": {
    "id": "system-coated-gracol-2006",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "color-keyword-rust",
    "space": "concept"
   },
   "relation": "belongs_to_topic",
   "to": {
    "id": "topic-color-orange-spectrum",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "color-keyword-rust",
    "space": "concept"
   },
   "relation": "cites",
   "to": {
    "id": "ref-reference-x-vol1-color",
    "space": "resource"
   }
  },
  {
   "from": {
    "id": "color-keyword-rust",
    "space": "concept"
   },
   "relation": "requires",
   "to": {
    "id": "system-srgb-reference",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "color-keyword-rust",
    "space": "concept"
   },
   "relation": "requires",
   "to": {
    "id": "system-coated-gracol-2006",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "color-keyword-copper",
    "space": "concept"
   },
   "relation": "belongs_to_topic",
   "to": {
    "id": "topic-color-orange-spectrum",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "color-keyword-copper",
    "space": "concept"
   },
   "relation": "cites",
   "to": {
    "id": "ref-reference-x-vol1-color",
    "space": "resource"
   }
  },
  {
   "from": {
    "id": "color-keyword-copper",
    "space": "concept"
   },
   "relation": "requires",
   "to": {
    "id": "system-srgb-reference",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "color-keyword-copper",
    "space": "concept"
   },
   "relation": "requires",
   "to": {
    "id": "system-coated-gracol-2006",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "color-keyword-burnt-orange",
    "space": "concept"
   },
   "relation": "belongs_to_topic",
   "to": {
    "id": "topic-color-orange-spectrum",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "color-keyword-burnt-orange",
    "space": "concept"
   },
   "relation": "cites",
   "to": {
    "id": "ref-reference-x-vol1-color",
    "space": "resource"
   }
  },
  {
   "from": {
    "id": "color-keyword-burnt-orange",
    "space": "concept"
   },
   "relation": "requires",
   "to": {
    "id": "system-srgb-reference",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "color-keyword-burnt-orange",
    "space": "concept"
   },
   "relation": "requires",
   "to": {
    "id": "system-coated-gracol-2006",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "color-keyword-peach-puff",
    "space": "concept"
   },
   "relation": "belongs_to_topic",
   "to": {
    "id": "topic-color-orange-spectrum",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "color-keyword-peach-puff",
    "space": "concept"
   },
   "relation": "cites",
   "to": {
    "id": "ref-reference-x-vol1-color",
    "space": "resource"
   }
  },
  {
   "from": {
    "id": "color-keyword-peach-puff",
    "space": "concept"
   },
   "relation": "requires",
   "to": {
    "id": "system-srgb-reference",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "color-keyword-peach-puff",
    "space": "concept"
   },
   "relation": "requires",
   "to": {
    "id": "system-coated-gracol-2006",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "color-keyword-coral-blush",
    "space": "concept"
   },
   "relation": "belongs_to_topic",
   "to": {
    "id": "topic-color-orange-spectrum",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "color-keyword-coral-blush",
    "space": "concept"
   },
   "relation": "cites",
   "to": {
    "id": "ref-reference-x-vol1-color",
    "space": "resource"
   }
  },
  {
   "from": {
    "id": "color-keyword-coral-blush",
    "space": "concept"
   },
   "relation": "requires",
   "to": {
    "id": "system-srgb-reference",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "color-keyword-coral-blush",
    "space": "concept"
   },
   "relation": "requires",
   "to": {
    "id": "system-coated-gracol-2006",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "color-keyword-creamsicle",
    "space": "concept"
   },
   "relation": "belongs_to_topic",
   "to": {
    "id": "topic-color-orange-spectrum",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "color-keyword-creamsicle",
    "space": "concept"
   },
   "relation": "cites",
   "to": {
    "id": "ref-reference-x-vol1-color",
    "space": "resource"
   }
  },
  {
   "from": {
    "id": "color-keyword-creamsicle",
    "space": "concept"
   },
   "relation": "requires",
   "to": {
    "id": "system-srgb-reference",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "color-keyword-creamsicle",
    "space": "concept"
   },
   "relation": "requires",
   "to": {
    "id": "system-coated-gracol-2006",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "color-keyword-living-coral",
    "space": "concept"
   },
   "relation": "belongs_to_topic",
   "to": {
    "id": "topic-color-orange-spectrum",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "color-keyword-living-coral",
    "space": "concept"
   },
   "relation": "cites",
   "to": {
    "id": "ref-reference-x-vol1-color",
    "space": "resource"
   }
  },
  {
   "from": {
    "id": "color-keyword-living-coral",
    "space": "concept"
   },
   "relation": "requires",
   "to": {
    "id": "system-srgb-reference",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "color-keyword-living-coral",
    "space": "concept"
   },
   "relation": "requires",
   "to": {
    "id": "system-coated-gracol-2006",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "color-keyword-flame",
    "space": "concept"
   },
   "relation": "belongs_to_topic",
   "to": {
    "id": "topic-color-orange-spectrum",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "color-keyword-flame",
    "space": "concept"
   },
   "relation": "cites",
   "to": {
    "id": "ref-reference-x-vol1-color",
    "space": "resource"
   }
  },
  {
   "from": {
    "id": "color-keyword-flame",
    "space": "concept"
   },
   "relation": "requires",
   "to": {
    "id": "system-srgb-reference",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "color-keyword-flame",
    "space": "concept"
   },
   "relation": "requires",
   "to": {
    "id": "system-coated-gracol-2006",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "color-keyword-chili-oil",
    "space": "concept"
   },
   "relation": "belongs_to_topic",
   "to": {
    "id": "topic-color-orange-spectrum",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "color-keyword-chili-oil",
    "space": "concept"
   },
   "relation": "cites",
   "to": {
    "id": "ref-reference-x-vol1-color",
    "space": "resource"
   }
  },
  {
   "from": {
    "id": "color-keyword-chili-oil",
    "space": "concept"
   },
   "relation": "requires",
   "to": {
    "id": "system-srgb-reference",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "color-keyword-chili-oil",
    "space": "concept"
   },
   "relation": "requires",
   "to": {
    "id": "system-coated-gracol-2006",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "color-keyword-lemon-yellow",
    "space": "concept"
   },
   "relation": "belongs_to_topic",
   "to": {
    "id": "topic-color-yellow-spectrum",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "color-keyword-lemon-yellow",
    "space": "concept"
   },
   "relation": "cites",
   "to": {
    "id": "ref-reference-x-vol1-color",
    "space": "resource"
   }
  },
  {
   "from": {
    "id": "color-keyword-lemon-yellow",
    "space": "concept"
   },
   "relation": "requires",
   "to": {
    "id": "system-srgb-reference",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "color-keyword-lemon-yellow",
    "space": "concept"
   },
   "relation": "requires",
   "to": {
    "id": "system-coated-gracol-2006",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "color-keyword-goldenrod",
    "space": "concept"
   },
   "relation": "belongs_to_topic",
   "to": {
    "id": "topic-color-yellow-spectrum",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "color-keyword-goldenrod",
    "space": "concept"
   },
   "relation": "cites",
   "to": {
    "id": "ref-reference-x-vol1-color",
    "space": "resource"
   }
  },
  {
   "from": {
    "id": "color-keyword-goldenrod",
    "space": "concept"
   },
   "relation": "requires",
   "to": {
    "id": "system-srgb-reference",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "color-keyword-goldenrod",
    "space": "concept"
   },
   "relation": "requires",
   "to": {
    "id": "system-coated-gracol-2006",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "color-keyword-amber",
    "space": "concept"
   },
   "relation": "belongs_to_topic",
   "to": {
    "id": "topic-color-yellow-spectrum",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "color-keyword-amber",
    "space": "concept"
   },
   "relation": "cites",
   "to": {
    "id": "ref-reference-x-vol1-color",
    "space": "resource"
   }
  },
  {
   "from": {
    "id": "color-keyword-amber",
    "space": "concept"
   },
   "relation": "requires",
   "to": {
    "id": "system-srgb-reference",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "color-keyword-amber",
    "space": "concept"
   },
   "relation": "requires",
   "to": {
    "id": "system-coated-gracol-2006",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "color-keyword-mustard-yellow",
    "space": "concept"
   },
   "relation": "belongs_to_topic",
   "to": {
    "id": "topic-color-yellow-spectrum",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "color-keyword-mustard-yellow",
    "space": "concept"
   },
   "relation": "cites",
   "to": {
    "id": "ref-reference-x-vol1-color",
    "space": "resource"
   }
  },
  {
   "from": {
    "id": "color-keyword-mustard-yellow",
    "space": "concept"
   },
   "relation": "requires",
   "to": {
    "id": "system-srgb-reference",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "color-keyword-mustard-yellow",
    "space": "concept"
   },
   "relation": "requires",
   "to": {
    "id": "system-coated-gracol-2006",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "color-keyword-wheat",
    "space": "concept"
   },
   "relation": "belongs_to_topic",
   "to": {
    "id": "topic-color-yellow-spectrum",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "color-keyword-wheat",
    "space": "concept"
   },
   "relation": "cites",
   "to": {
    "id": "ref-reference-x-vol1-color",
    "space": "resource"
   }
  },
  {
   "from": {
    "id": "color-keyword-wheat",
    "space": "concept"
   },
   "relation": "requires",
   "to": {
    "id": "system-srgb-reference",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "color-keyword-wheat",
    "space": "concept"
   },
   "relation": "requires",
   "to": {
    "id": "system-coated-gracol-2006",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "color-keyword-flax",
    "space": "concept"
   },
   "relation": "belongs_to_topic",
   "to": {
    "id": "topic-color-yellow-spectrum",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "color-keyword-flax",
    "space": "concept"
   },
   "relation": "cites",
   "to": {
    "id": "ref-reference-x-vol1-color",
    "space": "resource"
   }
  },
  {
   "from": {
    "id": "color-keyword-flax",
    "space": "concept"
   },
   "relation": "requires",
   "to": {
    "id": "system-srgb-reference",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "color-keyword-flax",
    "space": "concept"
   },
   "relation": "requires",
   "to": {
    "id": "system-coated-gracol-2006",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "color-keyword-ochre-yellow",
    "space": "concept"
   },
   "relation": "belongs_to_topic",
   "to": {
    "id": "topic-color-yellow-spectrum",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "color-keyword-ochre-yellow",
    "space": "concept"
   },
   "relation": "cites",
   "to": {
    "id": "ref-reference-x-vol1-color",
    "space": "resource"
   }
  },
  {
   "from": {
    "id": "color-keyword-ochre-yellow",
    "space": "concept"
   },
   "relation": "requires",
   "to": {
    "id": "system-srgb-reference",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "color-keyword-ochre-yellow",
    "space": "concept"
   },
   "relation": "requires",
   "to": {
    "id": "system-coated-gracol-2006",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "color-keyword-bronze-gold",
    "space": "concept"
   },
   "relation": "belongs_to_topic",
   "to": {
    "id": "topic-color-yellow-spectrum",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "color-keyword-bronze-gold",
    "space": "concept"
   },
   "relation": "cites",
   "to": {
    "id": "ref-reference-x-vol1-color",
    "space": "resource"
   }
  },
  {
   "from": {
    "id": "color-keyword-bronze-gold",
    "space": "concept"
   },
   "relation": "requires",
   "to": {
    "id": "system-srgb-reference",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "color-keyword-bronze-gold",
    "space": "concept"
   },
   "relation": "requires",
   "to": {
    "id": "system-coated-gracol-2006",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "color-keyword-naples-yellow",
    "space": "concept"
   },
   "relation": "belongs_to_topic",
   "to": {
    "id": "topic-color-yellow-spectrum",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "color-keyword-naples-yellow",
    "space": "concept"
   },
   "relation": "cites",
   "to": {
    "id": "ref-reference-x-vol1-color",
    "space": "resource"
   }
  },
  {
   "from": {
    "id": "color-keyword-naples-yellow",
    "space": "concept"
   },
   "relation": "requires",
   "to": {
    "id": "system-srgb-reference",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "color-keyword-naples-yellow",
    "space": "concept"
   },
   "relation": "requires",
   "to": {
    "id": "system-coated-gracol-2006",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "color-keyword-cornsilk",
    "space": "concept"
   },
   "relation": "belongs_to_topic",
   "to": {
    "id": "topic-color-yellow-spectrum",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "color-keyword-cornsilk",
    "space": "concept"
   },
   "relation": "cites",
   "to": {
    "id": "ref-reference-x-vol1-color",
    "space": "resource"
   }
  },
  {
   "from": {
    "id": "color-keyword-cornsilk",
    "space": "concept"
   },
   "relation": "requires",
   "to": {
    "id": "system-srgb-reference",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "color-keyword-cornsilk",
    "space": "concept"
   },
   "relation": "requires",
   "to": {
    "id": "system-coated-gracol-2006",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "color-keyword-buttercream",
    "space": "concept"
   },
   "relation": "belongs_to_topic",
   "to": {
    "id": "topic-color-yellow-spectrum",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "color-keyword-buttercream",
    "space": "concept"
   },
   "relation": "cites",
   "to": {
    "id": "ref-reference-x-vol1-color",
    "space": "resource"
   }
  },
  {
   "from": {
    "id": "color-keyword-buttercream",
    "space": "concept"
   },
   "relation": "requires",
   "to": {
    "id": "system-srgb-reference",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "color-keyword-buttercream",
    "space": "concept"
   },
   "relation": "requires",
   "to": {
    "id": "system-coated-gracol-2006",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "color-keyword-illuminating",
    "space": "concept"
   },
   "relation": "belongs_to_topic",
   "to": {
    "id": "topic-color-yellow-spectrum",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "color-keyword-illuminating",
    "space": "concept"
   },
   "relation": "cites",
   "to": {
    "id": "ref-reference-x-vol1-color",
    "space": "resource"
   }
  },
  {
   "from": {
    "id": "color-keyword-illuminating",
    "space": "concept"
   },
   "relation": "requires",
   "to": {
    "id": "system-srgb-reference",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "color-keyword-illuminating",
    "space": "concept"
   },
   "relation": "requires",
   "to": {
    "id": "system-coated-gracol-2006",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "color-keyword-honey-gold",
    "space": "concept"
   },
   "relation": "belongs_to_topic",
   "to": {
    "id": "topic-color-yellow-spectrum",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "color-keyword-honey-gold",
    "space": "concept"
   },
   "relation": "cites",
   "to": {
    "id": "ref-reference-x-vol1-color",
    "space": "resource"
   }
  },
  {
   "from": {
    "id": "color-keyword-honey-gold",
    "space": "concept"
   },
   "relation": "requires",
   "to": {
    "id": "system-srgb-reference",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "color-keyword-honey-gold",
    "space": "concept"
   },
   "relation": "requires",
   "to": {
    "id": "system-coated-gracol-2006",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "color-keyword-autumn-blaze",
    "space": "concept"
   },
   "relation": "belongs_to_topic",
   "to": {
    "id": "topic-color-yellow-spectrum",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "color-keyword-autumn-blaze",
    "space": "concept"
   },
   "relation": "cites",
   "to": {
    "id": "ref-reference-x-vol1-color",
    "space": "resource"
   }
  },
  {
   "from": {
    "id": "color-keyword-autumn-blaze",
    "space": "concept"
   },
   "relation": "requires",
   "to": {
    "id": "system-srgb-reference",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "color-keyword-autumn-blaze",
    "space": "concept"
   },
   "relation": "requires",
   "to": {
    "id": "system-coated-gracol-2006",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "color-keyword-emerald-green",
    "space": "concept"
   },
   "relation": "belongs_to_topic",
   "to": {
    "id": "topic-color-green-spectrum",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "color-keyword-emerald-green",
    "space": "concept"
   },
   "relation": "cites",
   "to": {
    "id": "ref-reference-x-vol1-color",
    "space": "resource"
   }
  },
  {
   "from": {
    "id": "color-keyword-emerald-green",
    "space": "concept"
   },
   "relation": "requires",
   "to": {
    "id": "system-srgb-reference",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "color-keyword-emerald-green",
    "space": "concept"
   },
   "relation": "requires",
   "to": {
    "id": "system-coated-gracol-2006",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "color-keyword-kelly-green",
    "space": "concept"
   },
   "relation": "belongs_to_topic",
   "to": {
    "id": "topic-color-green-spectrum",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "color-keyword-kelly-green",
    "space": "concept"
   },
   "relation": "cites",
   "to": {
    "id": "ref-reference-x-vol1-color",
    "space": "resource"
   }
  },
  {
   "from": {
    "id": "color-keyword-kelly-green",
    "space": "concept"
   },
   "relation": "requires",
   "to": {
    "id": "system-srgb-reference",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "color-keyword-kelly-green",
    "space": "concept"
   },
   "relation": "requires",
   "to": {
    "id": "system-coated-gracol-2006",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "color-keyword-olive-green",
    "space": "concept"
   },
   "relation": "belongs_to_topic",
   "to": {
    "id": "topic-color-green-spectrum",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "color-keyword-olive-green",
    "space": "concept"
   },
   "relation": "cites",
   "to": {
    "id": "ref-reference-x-vol1-color",
    "space": "resource"
   }
  },
  {
   "from": {
    "id": "color-keyword-olive-green",
    "space": "concept"
   },
   "relation": "requires",
   "to": {
    "id": "system-srgb-reference",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "color-keyword-olive-green",
    "space": "concept"
   },
   "relation": "requires",
   "to": {
    "id": "system-coated-gracol-2006",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "color-keyword-moss-green",
    "space": "concept"
   },
   "relation": "belongs_to_topic",
   "to": {
    "id": "topic-color-green-spectrum",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "color-keyword-moss-green",
    "space": "concept"
   },
   "relation": "cites",
   "to": {
    "id": "ref-reference-x-vol1-color",
    "space": "resource"
   }
  },
  {
   "from": {
    "id": "color-keyword-moss-green",
    "space": "concept"
   },
   "relation": "requires",
   "to": {
    "id": "system-srgb-reference",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "color-keyword-moss-green",
    "space": "concept"
   },
   "relation": "requires",
   "to": {
    "id": "system-coated-gracol-2006",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "color-keyword-fern-green",
    "space": "concept"
   },
   "relation": "belongs_to_topic",
   "to": {
    "id": "topic-color-green-spectrum",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "color-keyword-fern-green",
    "space": "concept"
   },
   "relation": "cites",
   "to": {
    "id": "ref-reference-x-vol1-color",
    "space": "resource"
   }
  },
  {
   "from": {
    "id": "color-keyword-fern-green",
    "space": "concept"
   },
   "relation": "requires",
   "to": {
    "id": "system-srgb-reference",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "color-keyword-fern-green",
    "space": "concept"
   },
   "relation": "requires",
   "to": {
    "id": "system-coated-gracol-2006",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "color-keyword-forest-green",
    "space": "concept"
   },
   "relation": "belongs_to_topic",
   "to": {
    "id": "topic-color-green-spectrum",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "color-keyword-forest-green",
    "space": "concept"
   },
   "relation": "cites",
   "to": {
    "id": "ref-reference-x-vol1-color",
    "space": "resource"
   }
  },
  {
   "from": {
    "id": "color-keyword-forest-green",
    "space": "concept"
   },
   "relation": "requires",
   "to": {
    "id": "system-srgb-reference",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "color-keyword-forest-green",
    "space": "concept"
   },
   "relation": "requires",
   "to": {
    "id": "system-coated-gracol-2006",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "color-keyword-hunter-green",
    "space": "concept"
   },
   "relation": "belongs_to_topic",
   "to": {
    "id": "topic-color-green-spectrum",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "color-keyword-hunter-green",
    "space": "concept"
   },
   "relation": "cites",
   "to": {
    "id": "ref-reference-x-vol1-color",
    "space": "resource"
   }
  },
  {
   "from": {
    "id": "color-keyword-hunter-green",
    "space": "concept"
   },
   "relation": "requires",
   "to": {
    "id": "system-srgb-reference",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "color-keyword-hunter-green",
    "space": "concept"
   },
   "relation": "requires",
   "to": {
    "id": "system-coated-gracol-2006",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "color-keyword-bottle-green",
    "space": "concept"
   },
   "relation": "belongs_to_topic",
   "to": {
    "id": "topic-color-green-spectrum",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "color-keyword-bottle-green",
    "space": "concept"
   },
   "relation": "cites",
   "to": {
    "id": "ref-reference-x-vol1-color",
    "space": "resource"
   }
  },
  {
   "from": {
    "id": "color-keyword-bottle-green",
    "space": "concept"
   },
   "relation": "requires",
   "to": {
    "id": "system-srgb-reference",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "color-keyword-bottle-green",
    "space": "concept"
   },
   "relation": "requires",
   "to": {
    "id": "system-coated-gracol-2006",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "color-keyword-mint-green",
    "space": "concept"
   },
   "relation": "belongs_to_topic",
   "to": {
    "id": "topic-color-green-spectrum",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "color-keyword-mint-green",
    "space": "concept"
   },
   "relation": "cites",
   "to": {
    "id": "ref-reference-x-vol1-color",
    "space": "resource"
   }
  },
  {
   "from": {
    "id": "color-keyword-mint-green",
    "space": "concept"
   },
   "relation": "requires",
   "to": {
    "id": "system-srgb-reference",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "color-keyword-mint-green",
    "space": "concept"
   },
   "relation": "requires",
   "to": {
    "id": "system-coated-gracol-2006",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "color-keyword-celadon",
    "space": "concept"
   },
   "relation": "belongs_to_topic",
   "to": {
    "id": "topic-color-green-spectrum",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "color-keyword-celadon",
    "space": "concept"
   },
   "relation": "cites",
   "to": {
    "id": "ref-reference-x-vol1-color",
    "space": "resource"
   }
  },
  {
   "from": {
    "id": "color-keyword-celadon",
    "space": "concept"
   },
   "relation": "requires",
   "to": {
    "id": "system-srgb-reference",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "color-keyword-celadon",
    "space": "concept"
   },
   "relation": "requires",
   "to": {
    "id": "system-coated-gracol-2006",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "color-keyword-greenery",
    "space": "concept"
   },
   "relation": "belongs_to_topic",
   "to": {
    "id": "topic-color-green-spectrum",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "color-keyword-greenery",
    "space": "concept"
   },
   "relation": "cites",
   "to": {
    "id": "ref-reference-x-vol1-color",
    "space": "resource"
   }
  },
  {
   "from": {
    "id": "color-keyword-greenery",
    "space": "concept"
   },
   "relation": "requires",
   "to": {
    "id": "system-srgb-reference",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "color-keyword-greenery",
    "space": "concept"
   },
   "relation": "requires",
   "to": {
    "id": "system-coated-gracol-2006",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "color-keyword-arcadia",
    "space": "concept"
   },
   "relation": "belongs_to_topic",
   "to": {
    "id": "topic-color-green-spectrum",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "color-keyword-arcadia",
    "space": "concept"
   },
   "relation": "cites",
   "to": {
    "id": "ref-reference-x-vol1-color",
    "space": "resource"
   }
  },
  {
   "from": {
    "id": "color-keyword-arcadia",
    "space": "concept"
   },
   "relation": "requires",
   "to": {
    "id": "system-srgb-reference",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "color-keyword-arcadia",
    "space": "concept"
   },
   "relation": "requires",
   "to": {
    "id": "system-coated-gracol-2006",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "color-keyword-cascades",
    "space": "concept"
   },
   "relation": "belongs_to_topic",
   "to": {
    "id": "topic-color-green-spectrum",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "color-keyword-cascades",
    "space": "concept"
   },
   "relation": "cites",
   "to": {
    "id": "ref-reference-x-vol1-color",
    "space": "resource"
   }
  },
  {
   "from": {
    "id": "color-keyword-cascades",
    "space": "concept"
   },
   "relation": "requires",
   "to": {
    "id": "system-srgb-reference",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "color-keyword-cascades",
    "space": "concept"
   },
   "relation": "requires",
   "to": {
    "id": "system-coated-gracol-2006",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "color-keyword-cerulean",
    "space": "concept"
   },
   "relation": "belongs_to_topic",
   "to": {
    "id": "topic-color-blue-spectrum",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "color-keyword-cerulean",
    "space": "concept"
   },
   "relation": "cites",
   "to": {
    "id": "ref-reference-x-vol1-color",
    "space": "resource"
   }
  },
  {
   "from": {
    "id": "color-keyword-cerulean",
    "space": "concept"
   },
   "relation": "requires",
   "to": {
    "id": "system-srgb-reference",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "color-keyword-cerulean",
    "space": "concept"
   },
   "relation": "requires",
   "to": {
    "id": "system-coated-gracol-2006",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "color-keyword-azure-blue",
    "space": "concept"
   },
   "relation": "belongs_to_topic",
   "to": {
    "id": "topic-color-blue-spectrum",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "color-keyword-azure-blue",
    "space": "concept"
   },
   "relation": "cites",
   "to": {
    "id": "ref-reference-x-vol1-color",
    "space": "resource"
   }
  },
  {
   "from": {
    "id": "color-keyword-azure-blue",
    "space": "concept"
   },
   "relation": "requires",
   "to": {
    "id": "system-srgb-reference",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "color-keyword-azure-blue",
    "space": "concept"
   },
   "relation": "requires",
   "to": {
    "id": "system-coated-gracol-2006",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "color-keyword-sky-blue",
    "space": "concept"
   },
   "relation": "belongs_to_topic",
   "to": {
    "id": "topic-color-blue-spectrum",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "color-keyword-sky-blue",
    "space": "concept"
   },
   "relation": "cites",
   "to": {
    "id": "ref-reference-x-vol1-color",
    "space": "resource"
   }
  },
  {
   "from": {
    "id": "color-keyword-sky-blue",
    "space": "concept"
   },
   "relation": "requires",
   "to": {
    "id": "system-srgb-reference",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "color-keyword-sky-blue",
    "space": "concept"
   },
   "relation": "requires",
   "to": {
    "id": "system-coated-gracol-2006",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "color-keyword-teal-blue",
    "space": "concept"
   },
   "relation": "belongs_to_topic",
   "to": {
    "id": "topic-color-blue-spectrum",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "color-keyword-teal-blue",
    "space": "concept"
   },
   "relation": "cites",
   "to": {
    "id": "ref-reference-x-vol1-color",
    "space": "resource"
   }
  },
  {
   "from": {
    "id": "color-keyword-teal-blue",
    "space": "concept"
   },
   "relation": "requires",
   "to": {
    "id": "system-srgb-reference",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "color-keyword-teal-blue",
    "space": "concept"
   },
   "relation": "requires",
   "to": {
    "id": "system-coated-gracol-2006",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "color-keyword-ocean-blue",
    "space": "concept"
   },
   "relation": "belongs_to_topic",
   "to": {
    "id": "topic-color-blue-spectrum",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "color-keyword-ocean-blue",
    "space": "concept"
   },
   "relation": "cites",
   "to": {
    "id": "ref-reference-x-vol1-color",
    "space": "resource"
   }
  },
  {
   "from": {
    "id": "color-keyword-ocean-blue",
    "space": "concept"
   },
   "relation": "requires",
   "to": {
    "id": "system-srgb-reference",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "color-keyword-ocean-blue",
    "space": "concept"
   },
   "relation": "requires",
   "to": {
    "id": "system-coated-gracol-2006",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "color-keyword-navy-blue",
    "space": "concept"
   },
   "relation": "belongs_to_topic",
   "to": {
    "id": "topic-color-blue-spectrum",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "color-keyword-navy-blue",
    "space": "concept"
   },
   "relation": "cites",
   "to": {
    "id": "ref-reference-x-vol1-color",
    "space": "resource"
   }
  },
  {
   "from": {
    "id": "color-keyword-navy-blue",
    "space": "concept"
   },
   "relation": "requires",
   "to": {
    "id": "system-srgb-reference",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "color-keyword-navy-blue",
    "space": "concept"
   },
   "relation": "requires",
   "to": {
    "id": "system-coated-gracol-2006",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "color-keyword-prussian-blue",
    "space": "concept"
   },
   "relation": "belongs_to_topic",
   "to": {
    "id": "topic-color-blue-spectrum",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "color-keyword-prussian-blue",
    "space": "concept"
   },
   "relation": "cites",
   "to": {
    "id": "ref-reference-x-vol1-color",
    "space": "resource"
   }
  },
  {
   "from": {
    "id": "color-keyword-prussian-blue",
    "space": "concept"
   },
   "relation": "requires",
   "to": {
    "id": "system-srgb-reference",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "color-keyword-prussian-blue",
    "space": "concept"
   },
   "relation": "requires",
   "to": {
    "id": "system-coated-gracol-2006",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "color-keyword-ice-blue",
    "space": "concept"
   },
   "relation": "belongs_to_topic",
   "to": {
    "id": "topic-color-blue-spectrum",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "color-keyword-ice-blue",
    "space": "concept"
   },
   "relation": "cites",
   "to": {
    "id": "ref-reference-x-vol1-color",
    "space": "resource"
   }
  },
  {
   "from": {
    "id": "color-keyword-ice-blue",
    "space": "concept"
   },
   "relation": "requires",
   "to": {
    "id": "system-srgb-reference",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "color-keyword-ice-blue",
    "space": "concept"
   },
   "relation": "requires",
   "to": {
    "id": "system-coated-gracol-2006",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "color-keyword-powder-blue",
    "space": "concept"
   },
   "relation": "belongs_to_topic",
   "to": {
    "id": "topic-color-blue-spectrum",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "color-keyword-powder-blue",
    "space": "concept"
   },
   "relation": "cites",
   "to": {
    "id": "ref-reference-x-vol1-color",
    "space": "resource"
   }
  },
  {
   "from": {
    "id": "color-keyword-powder-blue",
    "space": "concept"
   },
   "relation": "requires",
   "to": {
    "id": "system-srgb-reference",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "color-keyword-powder-blue",
    "space": "concept"
   },
   "relation": "requires",
   "to": {
    "id": "system-coated-gracol-2006",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "color-keyword-misty-blue",
    "space": "concept"
   },
   "relation": "belongs_to_topic",
   "to": {
    "id": "topic-color-blue-spectrum",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "color-keyword-misty-blue",
    "space": "concept"
   },
   "relation": "cites",
   "to": {
    "id": "ref-reference-x-vol1-color",
    "space": "resource"
   }
  },
  {
   "from": {
    "id": "color-keyword-misty-blue",
    "space": "concept"
   },
   "relation": "requires",
   "to": {
    "id": "system-srgb-reference",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "color-keyword-misty-blue",
    "space": "concept"
   },
   "relation": "requires",
   "to": {
    "id": "system-coated-gracol-2006",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "color-keyword-classic-blue",
    "space": "concept"
   },
   "relation": "belongs_to_topic",
   "to": {
    "id": "topic-color-blue-spectrum",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "color-keyword-classic-blue",
    "space": "concept"
   },
   "relation": "cites",
   "to": {
    "id": "ref-reference-x-vol1-color",
    "space": "resource"
   }
  },
  {
   "from": {
    "id": "color-keyword-classic-blue",
    "space": "concept"
   },
   "relation": "requires",
   "to": {
    "id": "system-srgb-reference",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "color-keyword-classic-blue",
    "space": "concept"
   },
   "relation": "requires",
   "to": {
    "id": "system-coated-gracol-2006",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "color-keyword-super-sonic",
    "space": "concept"
   },
   "relation": "belongs_to_topic",
   "to": {
    "id": "topic-color-blue-spectrum",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "color-keyword-super-sonic",
    "space": "concept"
   },
   "relation": "cites",
   "to": {
    "id": "ref-reference-x-vol1-color",
    "space": "resource"
   }
  },
  {
   "from": {
    "id": "color-keyword-super-sonic",
    "space": "concept"
   },
   "relation": "requires",
   "to": {
    "id": "system-srgb-reference",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "color-keyword-super-sonic",
    "space": "concept"
   },
   "relation": "requires",
   "to": {
    "id": "system-coated-gracol-2006",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "color-keyword-blue-atoll",
    "space": "concept"
   },
   "relation": "belongs_to_topic",
   "to": {
    "id": "topic-color-blue-spectrum",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "color-keyword-blue-atoll",
    "space": "concept"
   },
   "relation": "cites",
   "to": {
    "id": "ref-reference-x-vol1-color",
    "space": "resource"
   }
  },
  {
   "from": {
    "id": "color-keyword-blue-atoll",
    "space": "concept"
   },
   "relation": "requires",
   "to": {
    "id": "system-srgb-reference",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "color-keyword-blue-atoll",
    "space": "concept"
   },
   "relation": "requires",
   "to": {
    "id": "system-coated-gracol-2006",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "color-keyword-cobalt-violet",
    "space": "concept"
   },
   "relation": "belongs_to_topic",
   "to": {
    "id": "topic-color-violet-spectrum",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "color-keyword-cobalt-violet",
    "space": "concept"
   },
   "relation": "cites",
   "to": {
    "id": "ref-reference-x-vol1-color",
    "space": "resource"
   }
  },
  {
   "from": {
    "id": "color-keyword-cobalt-violet",
    "space": "concept"
   },
   "relation": "requires",
   "to": {
    "id": "system-srgb-reference",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "color-keyword-cobalt-violet",
    "space": "concept"
   },
   "relation": "requires",
   "to": {
    "id": "system-coated-gracol-2006",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "color-keyword-royal-purple",
    "space": "concept"
   },
   "relation": "belongs_to_topic",
   "to": {
    "id": "topic-color-violet-spectrum",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "color-keyword-royal-purple",
    "space": "concept"
   },
   "relation": "cites",
   "to": {
    "id": "ref-reference-x-vol1-color",
    "space": "resource"
   }
  },
  {
   "from": {
    "id": "color-keyword-royal-purple",
    "space": "concept"
   },
   "relation": "requires",
   "to": {
    "id": "system-srgb-reference",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "color-keyword-royal-purple",
    "space": "concept"
   },
   "relation": "requires",
   "to": {
    "id": "system-coated-gracol-2006",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "color-keyword-lavender-violet",
    "space": "concept"
   },
   "relation": "belongs_to_topic",
   "to": {
    "id": "topic-color-violet-spectrum",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "color-keyword-lavender-violet",
    "space": "concept"
   },
   "relation": "cites",
   "to": {
    "id": "ref-reference-x-vol1-color",
    "space": "resource"
   }
  },
  {
   "from": {
    "id": "color-keyword-lavender-violet",
    "space": "concept"
   },
   "relation": "requires",
   "to": {
    "id": "system-srgb-reference",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "color-keyword-lavender-violet",
    "space": "concept"
   },
   "relation": "requires",
   "to": {
    "id": "system-coated-gracol-2006",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "color-keyword-lilac-violet",
    "space": "concept"
   },
   "relation": "belongs_to_topic",
   "to": {
    "id": "topic-color-violet-spectrum",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "color-keyword-lilac-violet",
    "space": "concept"
   },
   "relation": "cites",
   "to": {
    "id": "ref-reference-x-vol1-color",
    "space": "resource"
   }
  },
  {
   "from": {
    "id": "color-keyword-lilac-violet",
    "space": "concept"
   },
   "relation": "requires",
   "to": {
    "id": "system-srgb-reference",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "color-keyword-lilac-violet",
    "space": "concept"
   },
   "relation": "requires",
   "to": {
    "id": "system-coated-gracol-2006",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "color-keyword-iris-violet",
    "space": "concept"
   },
   "relation": "belongs_to_topic",
   "to": {
    "id": "topic-color-violet-spectrum",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "color-keyword-iris-violet",
    "space": "concept"
   },
   "relation": "cites",
   "to": {
    "id": "ref-reference-x-vol1-color",
    "space": "resource"
   }
  },
  {
   "from": {
    "id": "color-keyword-iris-violet",
    "space": "concept"
   },
   "relation": "requires",
   "to": {
    "id": "system-srgb-reference",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "color-keyword-iris-violet",
    "space": "concept"
   },
   "relation": "requires",
   "to": {
    "id": "system-coated-gracol-2006",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "color-keyword-aubergine",
    "space": "concept"
   },
   "relation": "belongs_to_topic",
   "to": {
    "id": "topic-color-violet-spectrum",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "color-keyword-aubergine",
    "space": "concept"
   },
   "relation": "cites",
   "to": {
    "id": "ref-reference-x-vol1-color",
    "space": "resource"
   }
  },
  {
   "from": {
    "id": "color-keyword-aubergine",
    "space": "concept"
   },
   "relation": "requires",
   "to": {
    "id": "system-srgb-reference",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "color-keyword-aubergine",
    "space": "concept"
   },
   "relation": "requires",
   "to": {
    "id": "system-coated-gracol-2006",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "color-keyword-byzantium",
    "space": "concept"
   },
   "relation": "belongs_to_topic",
   "to": {
    "id": "topic-color-violet-spectrum",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "color-keyword-byzantium",
    "space": "concept"
   },
   "relation": "cites",
   "to": {
    "id": "ref-reference-x-vol1-color",
    "space": "resource"
   }
  },
  {
   "from": {
    "id": "color-keyword-byzantium",
    "space": "concept"
   },
   "relation": "requires",
   "to": {
    "id": "system-srgb-reference",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "color-keyword-byzantium",
    "space": "concept"
   },
   "relation": "requires",
   "to": {
    "id": "system-coated-gracol-2006",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "color-keyword-midnight-violet",
    "space": "concept"
   },
   "relation": "belongs_to_topic",
   "to": {
    "id": "topic-color-violet-spectrum",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "color-keyword-midnight-violet",
    "space": "concept"
   },
   "relation": "cites",
   "to": {
    "id": "ref-reference-x-vol1-color",
    "space": "resource"
   }
  },
  {
   "from": {
    "id": "color-keyword-midnight-violet",
    "space": "concept"
   },
   "relation": "requires",
   "to": {
    "id": "system-srgb-reference",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "color-keyword-midnight-violet",
    "space": "concept"
   },
   "relation": "requires",
   "to": {
    "id": "system-coated-gracol-2006",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "color-keyword-periwinkle",
    "space": "concept"
   },
   "relation": "belongs_to_topic",
   "to": {
    "id": "topic-color-violet-spectrum",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "color-keyword-periwinkle",
    "space": "concept"
   },
   "relation": "cites",
   "to": {
    "id": "ref-reference-x-vol1-color",
    "space": "resource"
   }
  },
  {
   "from": {
    "id": "color-keyword-periwinkle",
    "space": "concept"
   },
   "relation": "requires",
   "to": {
    "id": "system-srgb-reference",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "color-keyword-periwinkle",
    "space": "concept"
   },
   "relation": "requires",
   "to": {
    "id": "system-coated-gracol-2006",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "color-keyword-mauve",
    "space": "concept"
   },
   "relation": "belongs_to_topic",
   "to": {
    "id": "topic-color-violet-spectrum",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "color-keyword-mauve",
    "space": "concept"
   },
   "relation": "cites",
   "to": {
    "id": "ref-reference-x-vol1-color",
    "space": "resource"
   }
  },
  {
   "from": {
    "id": "color-keyword-mauve",
    "space": "concept"
   },
   "relation": "requires",
   "to": {
    "id": "system-srgb-reference",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "color-keyword-mauve",
    "space": "concept"
   },
   "relation": "requires",
   "to": {
    "id": "system-coated-gracol-2006",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "color-keyword-lavender-mist",
    "space": "concept"
   },
   "relation": "belongs_to_topic",
   "to": {
    "id": "topic-color-violet-spectrum",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "color-keyword-lavender-mist",
    "space": "concept"
   },
   "relation": "cites",
   "to": {
    "id": "ref-reference-x-vol1-color",
    "space": "resource"
   }
  },
  {
   "from": {
    "id": "color-keyword-lavender-mist",
    "space": "concept"
   },
   "relation": "requires",
   "to": {
    "id": "system-srgb-reference",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "color-keyword-lavender-mist",
    "space": "concept"
   },
   "relation": "requires",
   "to": {
    "id": "system-coated-gracol-2006",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "color-keyword-ultra-violet",
    "space": "concept"
   },
   "relation": "belongs_to_topic",
   "to": {
    "id": "topic-color-violet-spectrum",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "color-keyword-ultra-violet",
    "space": "concept"
   },
   "relation": "cites",
   "to": {
    "id": "ref-reference-x-vol1-color",
    "space": "resource"
   }
  },
  {
   "from": {
    "id": "color-keyword-ultra-violet",
    "space": "concept"
   },
   "relation": "requires",
   "to": {
    "id": "system-srgb-reference",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "color-keyword-ultra-violet",
    "space": "concept"
   },
   "relation": "requires",
   "to": {
    "id": "system-coated-gracol-2006",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "color-keyword-very-peri",
    "space": "concept"
   },
   "relation": "belongs_to_topic",
   "to": {
    "id": "topic-color-violet-spectrum",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "color-keyword-very-peri",
    "space": "concept"
   },
   "relation": "cites",
   "to": {
    "id": "ref-reference-x-vol1-color",
    "space": "resource"
   }
  },
  {
   "from": {
    "id": "color-keyword-very-peri",
    "space": "concept"
   },
   "relation": "requires",
   "to": {
    "id": "system-srgb-reference",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "color-keyword-very-peri",
    "space": "concept"
   },
   "relation": "requires",
   "to": {
    "id": "system-coated-gracol-2006",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "color-keyword-grape-compote",
    "space": "concept"
   },
   "relation": "belongs_to_topic",
   "to": {
    "id": "topic-color-violet-spectrum",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "color-keyword-grape-compote",
    "space": "concept"
   },
   "relation": "cites",
   "to": {
    "id": "ref-reference-x-vol1-color",
    "space": "resource"
   }
  },
  {
   "from": {
    "id": "color-keyword-grape-compote",
    "space": "concept"
   },
   "relation": "requires",
   "to": {
    "id": "system-srgb-reference",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "color-keyword-grape-compote",
    "space": "concept"
   },
   "relation": "requires",
   "to": {
    "id": "system-coated-gracol-2006",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "guideline-extended-keywords-name-anchor-only",
    "space": "concept"
   },
   "relation": "belongs_to_topic",
   "to": {
    "id": "topic-color-reference-keywords",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "guideline-extended-keywords-name-anchor-only",
    "space": "concept"
   },
   "relation": "cites",
   "to": {
    "id": "ref-reference-x-vol1-color",
    "space": "resource"
   }
  },
  {
   "from": {
    "id": "color-keyword-ext-carmine",
    "space": "concept"
   },
   "relation": "belongs_to_topic",
   "to": {
    "id": "topic-color-red-spectrum",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "color-keyword-ext-carmine",
    "space": "concept"
   },
   "relation": "cites",
   "to": {
    "id": "ref-reference-x-vol1-color",
    "space": "resource"
   }
  },
  {
   "from": {
    "id": "color-keyword-ext-carmine",
    "space": "concept"
   },
   "relation": "requires",
   "to": {
    "id": "guideline-extended-keywords-name-anchor-only",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "color-keyword-ext-vermilion",
    "space": "concept"
   },
   "relation": "belongs_to_topic",
   "to": {
    "id": "topic-color-red-spectrum",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "color-keyword-ext-vermilion",
    "space": "concept"
   },
   "relation": "cites",
   "to": {
    "id": "ref-reference-x-vol1-color",
    "space": "resource"
   }
  },
  {
   "from": {
    "id": "color-keyword-ext-vermilion",
    "space": "concept"
   },
   "relation": "requires",
   "to": {
    "id": "guideline-extended-keywords-name-anchor-only",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "color-keyword-ext-cinnabar",
    "space": "concept"
   },
   "relation": "belongs_to_topic",
   "to": {
    "id": "topic-color-red-spectrum",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "color-keyword-ext-cinnabar",
    "space": "concept"
   },
   "relation": "cites",
   "to": {
    "id": "ref-reference-x-vol1-color",
    "space": "resource"
   }
  },
  {
   "from": {
    "id": "color-keyword-ext-cinnabar",
    "space": "concept"
   },
   "relation": "requires",
   "to": {
    "id": "guideline-extended-keywords-name-anchor-only",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "color-keyword-ext-cardinal",
    "space": "concept"
   },
   "relation": "belongs_to_topic",
   "to": {
    "id": "topic-color-red-spectrum",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "color-keyword-ext-cardinal",
    "space": "concept"
   },
   "relation": "cites",
   "to": {
    "id": "ref-reference-x-vol1-color",
    "space": "resource"
   }
  },
  {
   "from": {
    "id": "color-keyword-ext-cardinal",
    "space": "concept"
   },
   "relation": "requires",
   "to": {
    "id": "guideline-extended-keywords-name-anchor-only",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "color-keyword-ext-firebrick",
    "space": "concept"
   },
   "relation": "belongs_to_topic",
   "to": {
    "id": "topic-color-red-spectrum",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "color-keyword-ext-firebrick",
    "space": "concept"
   },
   "relation": "cites",
   "to": {
    "id": "ref-reference-x-vol1-color",
    "space": "resource"
   }
  },
  {
   "from": {
    "id": "color-keyword-ext-firebrick",
    "space": "concept"
   },
   "relation": "requires",
   "to": {
    "id": "guideline-extended-keywords-name-anchor-only",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "color-keyword-ext-candy-apple",
    "space": "concept"
   },
   "relation": "belongs_to_topic",
   "to": {
    "id": "topic-color-red-spectrum",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "color-keyword-ext-candy-apple",
    "space": "concept"
   },
   "relation": "cites",
   "to": {
    "id": "ref-reference-x-vol1-color",
    "space": "resource"
   }
  },
  {
   "from": {
    "id": "color-keyword-ext-candy-apple",
    "space": "concept"
   },
   "relation": "requires",
   "to": {
    "id": "guideline-extended-keywords-name-anchor-only",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "color-keyword-ext-alizarin-crimson",
    "space": "concept"
   },
   "relation": "belongs_to_topic",
   "to": {
    "id": "topic-color-red-spectrum",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "color-keyword-ext-alizarin-crimson",
    "space": "concept"
   },
   "relation": "cites",
   "to": {
    "id": "ref-reference-x-vol1-color",
    "space": "resource"
   }
  },
  {
   "from": {
    "id": "color-keyword-ext-alizarin-crimson",
    "space": "concept"
   },
   "relation": "requires",
   "to": {
    "id": "guideline-extended-keywords-name-anchor-only",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "color-keyword-ext-tomato",
    "space": "concept"
   },
   "relation": "belongs_to_topic",
   "to": {
    "id": "topic-color-red-spectrum",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "color-keyword-ext-tomato",
    "space": "concept"
   },
   "relation": "cites",
   "to": {
    "id": "ref-reference-x-vol1-color",
    "space": "resource"
   }
  },
  {
   "from": {
    "id": "color-keyword-ext-tomato",
    "space": "concept"
   },
   "relation": "requires",
   "to": {
    "id": "guideline-extended-keywords-name-anchor-only",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "color-keyword-ext-chili",
    "space": "concept"
   },
   "relation": "belongs_to_topic",
   "to": {
    "id": "topic-color-red-spectrum",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "color-keyword-ext-chili",
    "space": "concept"
   },
   "relation": "cites",
   "to": {
    "id": "ref-reference-x-vol1-color",
    "space": "resource"
   }
  },
  {
   "from": {
    "id": "color-keyword-ext-chili",
    "space": "concept"
   },
   "relation": "requires",
   "to": {
    "id": "guideline-extended-keywords-name-anchor-only",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "color-keyword-ext-maroon",
    "space": "concept"
   },
   "relation": "belongs_to_topic",
   "to": {
    "id": "topic-color-red-spectrum",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "color-keyword-ext-maroon",
    "space": "concept"
   },
   "relation": "cites",
   "to": {
    "id": "ref-reference-x-vol1-color",
    "space": "resource"
   }
  },
  {
   "from": {
    "id": "color-keyword-ext-maroon",
    "space": "concept"
   },
   "relation": "requires",
   "to": {
    "id": "guideline-extended-keywords-name-anchor-only",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "color-keyword-ext-cherry",
    "space": "concept"
   },
   "relation": "belongs_to_topic",
   "to": {
    "id": "topic-color-red-spectrum",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "color-keyword-ext-cherry",
    "space": "concept"
   },
   "relation": "cites",
   "to": {
    "id": "ref-reference-x-vol1-color",
    "space": "resource"
   }
  },
  {
   "from": {
    "id": "color-keyword-ext-cherry",
    "space": "concept"
   },
   "relation": "requires",
   "to": {
    "id": "guideline-extended-keywords-name-anchor-only",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "color-keyword-ext-garnet",
    "space": "concept"
   },
   "relation": "belongs_to_topic",
   "to": {
    "id": "topic-color-red-spectrum",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "color-keyword-ext-garnet",
    "space": "concept"
   },
   "relation": "cites",
   "to": {
    "id": "ref-reference-x-vol1-color",
    "space": "resource"
   }
  },
  {
   "from": {
    "id": "color-keyword-ext-garnet",
    "space": "concept"
   },
   "relation": "requires",
   "to": {
    "id": "guideline-extended-keywords-name-anchor-only",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "color-keyword-ext-blood-red",
    "space": "concept"
   },
   "relation": "belongs_to_topic",
   "to": {
    "id": "topic-color-red-spectrum",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "color-keyword-ext-blood-red",
    "space": "concept"
   },
   "relation": "cites",
   "to": {
    "id": "ref-reference-x-vol1-color",
    "space": "resource"
   }
  },
  {
   "from": {
    "id": "color-keyword-ext-blood-red",
    "space": "concept"
   },
   "relation": "requires",
   "to": {
    "id": "guideline-extended-keywords-name-anchor-only",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "color-keyword-ext-coke-red",
    "space": "concept"
   },
   "relation": "belongs_to_topic",
   "to": {
    "id": "topic-color-red-spectrum",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "color-keyword-ext-coke-red",
    "space": "concept"
   },
   "relation": "cites",
   "to": {
    "id": "ref-reference-x-vol1-color",
    "space": "resource"
   }
  },
  {
   "from": {
    "id": "color-keyword-ext-coke-red",
    "space": "concept"
   },
   "relation": "requires",
   "to": {
    "id": "guideline-extended-keywords-name-anchor-only",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "color-keyword-ext-ferrari-red",
    "space": "concept"
   },
   "relation": "belongs_to_topic",
   "to": {
    "id": "topic-color-red-spectrum",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "color-keyword-ext-ferrari-red",
    "space": "concept"
   },
   "relation": "cites",
   "to": {
    "id": "ref-reference-x-vol1-color",
    "space": "resource"
   }
  },
  {
   "from": {
    "id": "color-keyword-ext-ferrari-red",
    "space": "concept"
   },
   "relation": "requires",
   "to": {
    "id": "guideline-extended-keywords-name-anchor-only",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "color-keyword-ext-fire-engine-red",
    "space": "concept"
   },
   "relation": "belongs_to_topic",
   "to": {
    "id": "topic-color-red-spectrum",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "color-keyword-ext-fire-engine-red",
    "space": "concept"
   },
   "relation": "cites",
   "to": {
    "id": "ref-reference-x-vol1-color",
    "space": "resource"
   }
  },
  {
   "from": {
    "id": "color-keyword-ext-fire-engine-red",
    "space": "concept"
   },
   "relation": "requires",
   "to": {
    "id": "guideline-extended-keywords-name-anchor-only",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "color-keyword-ext-ruby-red",
    "space": "concept"
   },
   "relation": "belongs_to_topic",
   "to": {
    "id": "topic-color-red-spectrum",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "color-keyword-ext-ruby-red",
    "space": "concept"
   },
   "relation": "cites",
   "to": {
    "id": "ref-reference-x-vol1-color",
    "space": "resource"
   }
  },
  {
   "from": {
    "id": "color-keyword-ext-ruby-red",
    "space": "concept"
   },
   "relation": "requires",
   "to": {
    "id": "guideline-extended-keywords-name-anchor-only",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "color-keyword-ext-madder",
    "space": "concept"
   },
   "relation": "belongs_to_topic",
   "to": {
    "id": "topic-color-red-spectrum",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "color-keyword-ext-madder",
    "space": "concept"
   },
   "relation": "cites",
   "to": {
    "id": "ref-reference-x-vol1-color",
    "space": "resource"
   }
  },
  {
   "from": {
    "id": "color-keyword-ext-madder",
    "space": "concept"
   },
   "relation": "requires",
   "to": {
    "id": "guideline-extended-keywords-name-anchor-only",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "color-keyword-ext-amaranth",
    "space": "concept"
   },
   "relation": "belongs_to_topic",
   "to": {
    "id": "topic-color-red-spectrum",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "color-keyword-ext-amaranth",
    "space": "concept"
   },
   "relation": "cites",
   "to": {
    "id": "ref-reference-x-vol1-color",
    "space": "resource"
   }
  },
  {
   "from": {
    "id": "color-keyword-ext-amaranth",
    "space": "concept"
   },
   "relation": "requires",
   "to": {
    "id": "guideline-extended-keywords-name-anchor-only",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "color-keyword-ext-coquelicot",
    "space": "concept"
   },
   "relation": "belongs_to_topic",
   "to": {
    "id": "topic-color-red-spectrum",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "color-keyword-ext-coquelicot",
    "space": "concept"
   },
   "relation": "cites",
   "to": {
    "id": "ref-reference-x-vol1-color",
    "space": "resource"
   }
  },
  {
   "from": {
    "id": "color-keyword-ext-coquelicot",
    "space": "concept"
   },
   "relation": "requires",
   "to": {
    "id": "guideline-extended-keywords-name-anchor-only",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "color-keyword-ext-redwood",
    "space": "concept"
   },
   "relation": "belongs_to_topic",
   "to": {
    "id": "topic-color-red-spectrum",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "color-keyword-ext-redwood",
    "space": "concept"
   },
   "relation": "cites",
   "to": {
    "id": "ref-reference-x-vol1-color",
    "space": "resource"
   }
  },
  {
   "from": {
    "id": "color-keyword-ext-redwood",
    "space": "concept"
   },
   "relation": "requires",
   "to": {
    "id": "guideline-extended-keywords-name-anchor-only",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "color-keyword-ext-rust-red",
    "space": "concept"
   },
   "relation": "belongs_to_topic",
   "to": {
    "id": "topic-color-red-spectrum",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "color-keyword-ext-rust-red",
    "space": "concept"
   },
   "relation": "cites",
   "to": {
    "id": "ref-reference-x-vol1-color",
    "space": "resource"
   }
  },
  {
   "from": {
    "id": "color-keyword-ext-rust-red",
    "space": "concept"
   },
   "relation": "requires",
   "to": {
    "id": "guideline-extended-keywords-name-anchor-only",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "color-keyword-ext-wine-red",
    "space": "concept"
   },
   "relation": "belongs_to_topic",
   "to": {
    "id": "topic-color-red-spectrum",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "color-keyword-ext-wine-red",
    "space": "concept"
   },
   "relation": "cites",
   "to": {
    "id": "ref-reference-x-vol1-color",
    "space": "resource"
   }
  },
  {
   "from": {
    "id": "color-keyword-ext-wine-red",
    "space": "concept"
   },
   "relation": "requires",
   "to": {
    "id": "guideline-extended-keywords-name-anchor-only",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "color-keyword-ext-rosewood",
    "space": "concept"
   },
   "relation": "belongs_to_topic",
   "to": {
    "id": "topic-color-red-spectrum",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "color-keyword-ext-rosewood",
    "space": "concept"
   },
   "relation": "cites",
   "to": {
    "id": "ref-reference-x-vol1-color",
    "space": "resource"
   }
  },
  {
   "from": {
    "id": "color-keyword-ext-rosewood",
    "space": "concept"
   },
   "relation": "requires",
   "to": {
    "id": "guideline-extended-keywords-name-anchor-only",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "color-keyword-ext-mahogany",
    "space": "concept"
   },
   "relation": "belongs_to_topic",
   "to": {
    "id": "topic-color-red-spectrum",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "color-keyword-ext-mahogany",
    "space": "concept"
   },
   "relation": "cites",
   "to": {
    "id": "ref-reference-x-vol1-color",
    "space": "resource"
   }
  },
  {
   "from": {
    "id": "color-keyword-ext-mahogany",
    "space": "concept"
   },
   "relation": "requires",
   "to": {
    "id": "guideline-extended-keywords-name-anchor-only",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "color-keyword-ext-auburn",
    "space": "concept"
   },
   "relation": "belongs_to_topic",
   "to": {
    "id": "topic-color-red-spectrum",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "color-keyword-ext-auburn",
    "space": "concept"
   },
   "relation": "cites",
   "to": {
    "id": "ref-reference-x-vol1-color",
    "space": "resource"
   }
  },
  {
   "from": {
    "id": "color-keyword-ext-auburn",
    "space": "concept"
   },
   "relation": "requires",
   "to": {
    "id": "guideline-extended-keywords-name-anchor-only",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "color-keyword-ext-carnelian",
    "space": "concept"
   },
   "relation": "belongs_to_topic",
   "to": {
    "id": "topic-color-red-spectrum",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "color-keyword-ext-carnelian",
    "space": "concept"
   },
   "relation": "cites",
   "to": {
    "id": "ref-reference-x-vol1-color",
    "space": "resource"
   }
  },
  {
   "from": {
    "id": "color-keyword-ext-carnelian",
    "space": "concept"
   },
   "relation": "requires",
   "to": {
    "id": "guideline-extended-keywords-name-anchor-only",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "color-keyword-ext-cantaloupe",
    "space": "concept"
   },
   "relation": "belongs_to_topic",
   "to": {
    "id": "topic-color-orange-spectrum",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "color-keyword-ext-cantaloupe",
    "space": "concept"
   },
   "relation": "cites",
   "to": {
    "id": "ref-reference-x-vol1-color",
    "space": "resource"
   }
  },
  {
   "from": {
    "id": "color-keyword-ext-cantaloupe",
    "space": "concept"
   },
   "relation": "requires",
   "to": {
    "id": "guideline-extended-keywords-name-anchor-only",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "color-keyword-ext-amber-glow",
    "space": "concept"
   },
   "relation": "belongs_to_topic",
   "to": {
    "id": "topic-color-orange-spectrum",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "color-keyword-ext-amber-glow",
    "space": "concept"
   },
   "relation": "cites",
   "to": {
    "id": "ref-reference-x-vol1-color",
    "space": "resource"
   }
  },
  {
   "from": {
    "id": "color-keyword-ext-amber-glow",
    "space": "concept"
   },
   "relation": "requires",
   "to": {
    "id": "guideline-extended-keywords-name-anchor-only",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "color-keyword-ext-saffron",
    "space": "concept"
   },
   "relation": "belongs_to_topic",
   "to": {
    "id": "topic-color-orange-spectrum",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "color-keyword-ext-saffron",
    "space": "concept"
   },
   "relation": "cites",
   "to": {
    "id": "ref-reference-x-vol1-color",
    "space": "resource"
   }
  },
  {
   "from": {
    "id": "color-keyword-ext-saffron",
    "space": "concept"
   },
   "relation": "requires",
   "to": {
    "id": "guideline-extended-keywords-name-anchor-only",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "color-keyword-ext-butterscotch",
    "space": "concept"
   },
   "relation": "belongs_to_topic",
   "to": {
    "id": "topic-color-orange-spectrum",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "color-keyword-ext-butterscotch",
    "space": "concept"
   },
   "relation": "cites",
   "to": {
    "id": "ref-reference-x-vol1-color",
    "space": "resource"
   }
  },
  {
   "from": {
    "id": "color-keyword-ext-butterscotch",
    "space": "concept"
   },
   "relation": "requires",
   "to": {
    "id": "guideline-extended-keywords-name-anchor-only",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "color-keyword-ext-marigold",
    "space": "concept"
   },
   "relation": "belongs_to_topic",
   "to": {
    "id": "topic-color-orange-spectrum",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "color-keyword-ext-marigold",
    "space": "concept"
   },
   "relation": "cites",
   "to": {
    "id": "ref-reference-x-vol1-color",
    "space": "resource"
   }
  },
  {
   "from": {
    "id": "color-keyword-ext-marigold",
    "space": "concept"
   },
   "relation": "requires",
   "to": {
    "id": "guideline-extended-keywords-name-anchor-only",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "color-keyword-ext-amberlight",
    "space": "concept"
   },
   "relation": "belongs_to_topic",
   "to": {
    "id": "topic-color-orange-spectrum",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "color-keyword-ext-amberlight",
    "space": "concept"
   },
   "relation": "cites",
   "to": {
    "id": "ref-reference-x-vol1-color",
    "space": "resource"
   }
  },
  {
   "from": {
    "id": "color-keyword-ext-amberlight",
    "space": "concept"
   },
   "relation": "requires",
   "to": {
    "id": "guideline-extended-keywords-name-anchor-only",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "color-keyword-ext-copperfield",
    "space": "concept"
   },
   "relation": "belongs_to_topic",
   "to": {
    "id": "topic-color-orange-spectrum",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "color-keyword-ext-copperfield",
    "space": "concept"
   },
   "relation": "cites",
   "to": {
    "id": "ref-reference-x-vol1-color",
    "space": "resource"
   }
  },
  {
   "from": {
    "id": "color-keyword-ext-copperfield",
    "space": "concept"
   },
   "relation": "requires",
   "to": {
    "id": "guideline-extended-keywords-name-anchor-only",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "color-keyword-ext-tangelo",
    "space": "concept"
   },
   "relation": "belongs_to_topic",
   "to": {
    "id": "topic-color-orange-spectrum",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "color-keyword-ext-tangelo",
    "space": "concept"
   },
   "relation": "cites",
   "to": {
    "id": "ref-reference-x-vol1-color",
    "space": "resource"
   }
  },
  {
   "from": {
    "id": "color-keyword-ext-tangelo",
    "space": "concept"
   },
   "relation": "requires",
   "to": {
    "id": "guideline-extended-keywords-name-anchor-only",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "color-keyword-ext-mango",
    "space": "concept"
   },
   "relation": "belongs_to_topic",
   "to": {
    "id": "topic-color-orange-spectrum",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "color-keyword-ext-mango",
    "space": "concept"
   },
   "relation": "cites",
   "to": {
    "id": "ref-reference-x-vol1-color",
    "space": "resource"
   }
  },
  {
   "from": {
    "id": "color-keyword-ext-mango",
    "space": "concept"
   },
   "relation": "requires",
   "to": {
    "id": "guideline-extended-keywords-name-anchor-only",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "color-keyword-ext-mandarin",
    "space": "concept"
   },
   "relation": "belongs_to_topic",
   "to": {
    "id": "topic-color-orange-spectrum",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "color-keyword-ext-mandarin",
    "space": "concept"
   },
   "relation": "cites",
   "to": {
    "id": "ref-reference-x-vol1-color",
    "space": "resource"
   }
  },
  {
   "from": {
    "id": "color-keyword-ext-mandarin",
    "space": "concept"
   },
   "relation": "requires",
   "to": {
    "id": "guideline-extended-keywords-name-anchor-only",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "color-keyword-ext-papaya",
    "space": "concept"
   },
   "relation": "belongs_to_topic",
   "to": {
    "id": "topic-color-orange-spectrum",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "color-keyword-ext-papaya",
    "space": "concept"
   },
   "relation": "cites",
   "to": {
    "id": "ref-reference-x-vol1-color",
    "space": "resource"
   }
  },
  {
   "from": {
    "id": "color-keyword-ext-papaya",
    "space": "concept"
   },
   "relation": "requires",
   "to": {
    "id": "guideline-extended-keywords-name-anchor-only",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "color-keyword-ext-kumquat",
    "space": "concept"
   },
   "relation": "belongs_to_topic",
   "to": {
    "id": "topic-color-orange-spectrum",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "color-keyword-ext-kumquat",
    "space": "concept"
   },
   "relation": "cites",
   "to": {
    "id": "ref-reference-x-vol1-color",
    "space": "resource"
   }
  },
  {
   "from": {
    "id": "color-keyword-ext-kumquat",
    "space": "concept"
   },
   "relation": "requires",
   "to": {
    "id": "guideline-extended-keywords-name-anchor-only",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "color-keyword-ext-sunset-orange",
    "space": "concept"
   },
   "relation": "belongs_to_topic",
   "to": {
    "id": "topic-color-orange-spectrum",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "color-keyword-ext-sunset-orange",
    "space": "concept"
   },
   "relation": "cites",
   "to": {
    "id": "ref-reference-x-vol1-color",
    "space": "resource"
   }
  },
  {
   "from": {
    "id": "color-keyword-ext-sunset-orange",
    "space": "concept"
   },
   "relation": "requires",
   "to": {
    "id": "guideline-extended-keywords-name-anchor-only",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "color-keyword-ext-tigerlily",
    "space": "concept"
   },
   "relation": "belongs_to_topic",
   "to": {
    "id": "topic-color-orange-spectrum",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "color-keyword-ext-tigerlily",
    "space": "concept"
   },
   "relation": "cites",
   "to": {
    "id": "ref-reference-x-vol1-color",
    "space": "resource"
   }
  },
  {
   "from": {
    "id": "color-keyword-ext-tigerlily",
    "space": "concept"
   },
   "relation": "requires",
   "to": {
    "id": "guideline-extended-keywords-name-anchor-only",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "color-keyword-ext-spice-orange",
    "space": "concept"
   },
   "relation": "belongs_to_topic",
   "to": {
    "id": "topic-color-orange-spectrum",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "color-keyword-ext-spice-orange",
    "space": "concept"
   },
   "relation": "cites",
   "to": {
    "id": "ref-reference-x-vol1-color",
    "space": "resource"
   }
  },
  {
   "from": {
    "id": "color-keyword-ext-spice-orange",
    "space": "concept"
   },
   "relation": "requires",
   "to": {
    "id": "guideline-extended-keywords-name-anchor-only",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "color-keyword-ext-ginger",
    "space": "concept"
   },
   "relation": "belongs_to_topic",
   "to": {
    "id": "topic-color-orange-spectrum",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "color-keyword-ext-ginger",
    "space": "concept"
   },
   "relation": "cites",
   "to": {
    "id": "ref-reference-x-vol1-color",
    "space": "resource"
   }
  },
  {
   "from": {
    "id": "color-keyword-ext-ginger",
    "space": "concept"
   },
   "relation": "requires",
   "to": {
    "id": "guideline-extended-keywords-name-anchor-only",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "color-keyword-ext-honeycomb",
    "space": "concept"
   },
   "relation": "belongs_to_topic",
   "to": {
    "id": "topic-color-orange-spectrum",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "color-keyword-ext-honeycomb",
    "space": "concept"
   },
   "relation": "cites",
   "to": {
    "id": "ref-reference-x-vol1-color",
    "space": "resource"
   }
  },
  {
   "from": {
    "id": "color-keyword-ext-honeycomb",
    "space": "concept"
   },
   "relation": "requires",
   "to": {
    "id": "guideline-extended-keywords-name-anchor-only",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "color-keyword-ext-sorbet",
    "space": "concept"
   },
   "relation": "belongs_to_topic",
   "to": {
    "id": "topic-color-orange-spectrum",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "color-keyword-ext-sorbet",
    "space": "concept"
   },
   "relation": "cites",
   "to": {
    "id": "ref-reference-x-vol1-color",
    "space": "resource"
   }
  },
  {
   "from": {
    "id": "color-keyword-ext-sorbet",
    "space": "concept"
   },
   "relation": "requires",
   "to": {
    "id": "guideline-extended-keywords-name-anchor-only",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "color-keyword-ext-amber-clay",
    "space": "concept"
   },
   "relation": "belongs_to_topic",
   "to": {
    "id": "topic-color-orange-spectrum",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "color-keyword-ext-amber-clay",
    "space": "concept"
   },
   "relation": "cites",
   "to": {
    "id": "ref-reference-x-vol1-color",
    "space": "resource"
   }
  },
  {
   "from": {
    "id": "color-keyword-ext-amber-clay",
    "space": "concept"
   },
   "relation": "requires",
   "to": {
    "id": "guideline-extended-keywords-name-anchor-only",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "color-keyword-ext-maple",
    "space": "concept"
   },
   "relation": "belongs_to_topic",
   "to": {
    "id": "topic-color-orange-spectrum",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "color-keyword-ext-maple",
    "space": "concept"
   },
   "relation": "cites",
   "to": {
    "id": "ref-reference-x-vol1-color",
    "space": "resource"
   }
  },
  {
   "from": {
    "id": "color-keyword-ext-maple",
    "space": "concept"
   },
   "relation": "requires",
   "to": {
    "id": "guideline-extended-keywords-name-anchor-only",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "color-keyword-ext-golden-apricot",
    "space": "concept"
   },
   "relation": "belongs_to_topic",
   "to": {
    "id": "topic-color-orange-spectrum",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "color-keyword-ext-golden-apricot",
    "space": "concept"
   },
   "relation": "cites",
   "to": {
    "id": "ref-reference-x-vol1-color",
    "space": "resource"
   }
  },
  {
   "from": {
    "id": "color-keyword-ext-golden-apricot",
    "space": "concept"
   },
   "relation": "requires",
   "to": {
    "id": "guideline-extended-keywords-name-anchor-only",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "color-keyword-ext-dune",
    "space": "concept"
   },
   "relation": "belongs_to_topic",
   "to": {
    "id": "topic-color-orange-spectrum",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "color-keyword-ext-dune",
    "space": "concept"
   },
   "relation": "cites",
   "to": {
    "id": "ref-reference-x-vol1-color",
    "space": "resource"
   }
  },
  {
   "from": {
    "id": "color-keyword-ext-dune",
    "space": "concept"
   },
   "relation": "requires",
   "to": {
    "id": "guideline-extended-keywords-name-anchor-only",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "color-keyword-ext-canyon-clay",
    "space": "concept"
   },
   "relation": "belongs_to_topic",
   "to": {
    "id": "topic-color-orange-spectrum",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "color-keyword-ext-canyon-clay",
    "space": "concept"
   },
   "relation": "cites",
   "to": {
    "id": "ref-reference-x-vol1-color",
    "space": "resource"
   }
  },
  {
   "from": {
    "id": "color-keyword-ext-canyon-clay",
    "space": "concept"
   },
   "relation": "requires",
   "to": {
    "id": "guideline-extended-keywords-name-anchor-only",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "color-keyword-ext-harvest-gold",
    "space": "concept"
   },
   "relation": "belongs_to_topic",
   "to": {
    "id": "topic-color-orange-spectrum",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "color-keyword-ext-harvest-gold",
    "space": "concept"
   },
   "relation": "cites",
   "to": {
    "id": "ref-reference-x-vol1-color",
    "space": "resource"
   }
  },
  {
   "from": {
    "id": "color-keyword-ext-harvest-gold",
    "space": "concept"
   },
   "relation": "requires",
   "to": {
    "id": "guideline-extended-keywords-name-anchor-only",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "color-keyword-ext-copper-dust",
    "space": "concept"
   },
   "relation": "belongs_to_topic",
   "to": {
    "id": "topic-color-orange-spectrum",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "color-keyword-ext-copper-dust",
    "space": "concept"
   },
   "relation": "cites",
   "to": {
    "id": "ref-reference-x-vol1-color",
    "space": "resource"
   }
  },
  {
   "from": {
    "id": "color-keyword-ext-copper-dust",
    "space": "concept"
   },
   "relation": "requires",
   "to": {
    "id": "guideline-extended-keywords-name-anchor-only",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "color-keyword-ext-sandstone",
    "space": "concept"
   },
   "relation": "belongs_to_topic",
   "to": {
    "id": "topic-color-orange-spectrum",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "color-keyword-ext-sandstone",
    "space": "concept"
   },
   "relation": "cites",
   "to": {
    "id": "ref-reference-x-vol1-color",
    "space": "resource"
   }
  },
  {
   "from": {
    "id": "color-keyword-ext-sandstone",
    "space": "concept"
   },
   "relation": "requires",
   "to": {
    "id": "guideline-extended-keywords-name-anchor-only",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "color-keyword-ext-autumn-glow",
    "space": "concept"
   },
   "relation": "belongs_to_topic",
   "to": {
    "id": "topic-color-orange-spectrum",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "color-keyword-ext-autumn-glow",
    "space": "concept"
   },
   "relation": "cites",
   "to": {
    "id": "ref-reference-x-vol1-color",
    "space": "resource"
   }
  },
  {
   "from": {
    "id": "color-keyword-ext-autumn-glow",
    "space": "concept"
   },
   "relation": "requires",
   "to": {
    "id": "guideline-extended-keywords-name-anchor-only",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "color-keyword-ext-sunset-mist",
    "space": "concept"
   },
   "relation": "belongs_to_topic",
   "to": {
    "id": "topic-color-orange-spectrum",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "color-keyword-ext-sunset-mist",
    "space": "concept"
   },
   "relation": "cites",
   "to": {
    "id": "ref-reference-x-vol1-color",
    "space": "resource"
   }
  },
  {
   "from": {
    "id": "color-keyword-ext-sunset-mist",
    "space": "concept"
   },
   "relation": "requires",
   "to": {
    "id": "guideline-extended-keywords-name-anchor-only",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "color-keyword-ext-gold-ochre",
    "space": "concept"
   },
   "relation": "belongs_to_topic",
   "to": {
    "id": "topic-color-orange-spectrum",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "color-keyword-ext-gold-ochre",
    "space": "concept"
   },
   "relation": "cites",
   "to": {
    "id": "ref-reference-x-vol1-color",
    "space": "resource"
   }
  },
  {
   "from": {
    "id": "color-keyword-ext-gold-ochre",
    "space": "concept"
   },
   "relation": "requires",
   "to": {
    "id": "guideline-extended-keywords-name-anchor-only",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "color-keyword-ext-warm-terracotta",
    "space": "concept"
   },
   "relation": "belongs_to_topic",
   "to": {
    "id": "topic-color-orange-spectrum",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "color-keyword-ext-warm-terracotta",
    "space": "concept"
   },
   "relation": "cites",
   "to": {
    "id": "ref-reference-x-vol1-color",
    "space": "resource"
   }
  },
  {
   "from": {
    "id": "color-keyword-ext-warm-terracotta",
    "space": "concept"
   },
   "relation": "requires",
   "to": {
    "id": "guideline-extended-keywords-name-anchor-only",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "color-keyword-ext-canary-yellow",
    "space": "concept"
   },
   "relation": "belongs_to_topic",
   "to": {
    "id": "topic-color-yellow-spectrum",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "color-keyword-ext-canary-yellow",
    "space": "concept"
   },
   "relation": "cites",
   "to": {
    "id": "ref-reference-x-vol1-color",
    "space": "resource"
   }
  },
  {
   "from": {
    "id": "color-keyword-ext-canary-yellow",
    "space": "concept"
   },
   "relation": "requires",
   "to": {
    "id": "guideline-extended-keywords-name-anchor-only",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "color-keyword-ext-golden-yellow",
    "space": "concept"
   },
   "relation": "belongs_to_topic",
   "to": {
    "id": "topic-color-yellow-spectrum",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "color-keyword-ext-golden-yellow",
    "space": "concept"
   },
   "relation": "cites",
   "to": {
    "id": "ref-reference-x-vol1-color",
    "space": "resource"
   }
  },
  {
   "from": {
    "id": "color-keyword-ext-golden-yellow",
    "space": "concept"
   },
   "relation": "requires",
   "to": {
    "id": "guideline-extended-keywords-name-anchor-only",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "color-keyword-ext-maize",
    "space": "concept"
   },
   "relation": "belongs_to_topic",
   "to": {
    "id": "topic-color-yellow-spectrum",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "color-keyword-ext-maize",
    "space": "concept"
   },
   "relation": "cites",
   "to": {
    "id": "ref-reference-x-vol1-color",
    "space": "resource"
   }
  },
  {
   "from": {
    "id": "color-keyword-ext-maize",
    "space": "concept"
   },
   "relation": "requires",
   "to": {
    "id": "guideline-extended-keywords-name-anchor-only",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "color-keyword-ext-jonquil",
    "space": "concept"
   },
   "relation": "belongs_to_topic",
   "to": {
    "id": "topic-color-yellow-spectrum",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "color-keyword-ext-jonquil",
    "space": "concept"
   },
   "relation": "cites",
   "to": {
    "id": "ref-reference-x-vol1-color",
    "space": "resource"
   }
  },
  {
   "from": {
    "id": "color-keyword-ext-jonquil",
    "space": "concept"
   },
   "relation": "requires",
   "to": {
    "id": "guideline-extended-keywords-name-anchor-only",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "color-keyword-ext-sand-yellow",
    "space": "concept"
   },
   "relation": "belongs_to_topic",
   "to": {
    "id": "topic-color-yellow-spectrum",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "color-keyword-ext-sand-yellow",
    "space": "concept"
   },
   "relation": "cites",
   "to": {
    "id": "ref-reference-x-vol1-color",
    "space": "resource"
   }
  },
  {
   "from": {
    "id": "color-keyword-ext-sand-yellow",
    "space": "concept"
   },
   "relation": "requires",
   "to": {
    "id": "guideline-extended-keywords-name-anchor-only",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "color-keyword-ext-goldfinch",
    "space": "concept"
   },
   "relation": "belongs_to_topic",
   "to": {
    "id": "topic-color-yellow-spectrum",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "color-keyword-ext-goldfinch",
    "space": "concept"
   },
   "relation": "cites",
   "to": {
    "id": "ref-reference-x-vol1-color",
    "space": "resource"
   }
  },
  {
   "from": {
    "id": "color-keyword-ext-goldfinch",
    "space": "concept"
   },
   "relation": "requires",
   "to": {
    "id": "guideline-extended-keywords-name-anchor-only",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "color-keyword-ext-vanilla",
    "space": "concept"
   },
   "relation": "belongs_to_topic",
   "to": {
    "id": "topic-color-yellow-spectrum",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "color-keyword-ext-vanilla",
    "space": "concept"
   },
   "relation": "cites",
   "to": {
    "id": "ref-reference-x-vol1-color",
    "space": "resource"
   }
  },
  {
   "from": {
    "id": "color-keyword-ext-vanilla",
    "space": "concept"
   },
   "relation": "requires",
   "to": {
    "id": "guideline-extended-keywords-name-anchor-only",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "color-keyword-ext-straw",
    "space": "concept"
   },
   "relation": "belongs_to_topic",
   "to": {
    "id": "topic-color-yellow-spectrum",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "color-keyword-ext-straw",
    "space": "concept"
   },
   "relation": "cites",
   "to": {
    "id": "ref-reference-x-vol1-color",
    "space": "resource"
   }
  },
  {
   "from": {
    "id": "color-keyword-ext-straw",
    "space": "concept"
   },
   "relation": "requires",
   "to": {
    "id": "guideline-extended-keywords-name-anchor-only",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "color-keyword-ext-lemonade",
    "space": "concept"
   },
   "relation": "belongs_to_topic",
   "to": {
    "id": "topic-color-yellow-spectrum",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "color-keyword-ext-lemonade",
    "space": "concept"
   },
   "relation": "cites",
   "to": {
    "id": "ref-reference-x-vol1-color",
    "space": "resource"
   }
  },
  {
   "from": {
    "id": "color-keyword-ext-lemonade",
    "space": "concept"
   },
   "relation": "requires",
   "to": {
    "id": "guideline-extended-keywords-name-anchor-only",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "color-keyword-ext-sunshine",
    "space": "concept"
   },
   "relation": "belongs_to_topic",
   "to": {
    "id": "topic-color-yellow-spectrum",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "color-keyword-ext-sunshine",
    "space": "concept"
   },
   "relation": "cites",
   "to": {
    "id": "ref-reference-x-vol1-color",
    "space": "resource"
   }
  },
  {
   "from": {
    "id": "color-keyword-ext-sunshine",
    "space": "concept"
   },
   "relation": "requires",
   "to": {
    "id": "guideline-extended-keywords-name-anchor-only",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "color-keyword-ext-pale-daffodil",
    "space": "concept"
   },
   "relation": "belongs_to_topic",
   "to": {
    "id": "topic-color-yellow-spectrum",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "color-keyword-ext-pale-daffodil",
    "space": "concept"
   },
   "relation": "cites",
   "to": {
    "id": "ref-reference-x-vol1-color",
    "space": "resource"
   }
  },
  {
   "from": {
    "id": "color-keyword-ext-pale-daffodil",
    "space": "concept"
   },
   "relation": "requires",
   "to": {
    "id": "guideline-extended-keywords-name-anchor-only",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "color-keyword-ext-desert-gold",
    "space": "concept"
   },
   "relation": "belongs_to_topic",
   "to": {
    "id": "topic-color-yellow-spectrum",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "color-keyword-ext-desert-gold",
    "space": "concept"
   },
   "relation": "cites",
   "to": {
    "id": "ref-reference-x-vol1-color",
    "space": "resource"
   }
  },
  {
   "from": {
    "id": "color-keyword-ext-desert-gold",
    "space": "concept"
   },
   "relation": "requires",
   "to": {
    "id": "guideline-extended-keywords-name-anchor-only",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "color-keyword-ext-golden-haze",
    "space": "concept"
   },
   "relation": "belongs_to_topic",
   "to": {
    "id": "topic-color-yellow-spectrum",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "color-keyword-ext-golden-haze",
    "space": "concept"
   },
   "relation": "cites",
   "to": {
    "id": "ref-reference-x-vol1-color",
    "space": "resource"
   }
  },
  {
   "from": {
    "id": "color-keyword-ext-golden-haze",
    "space": "concept"
   },
   "relation": "requires",
   "to": {
    "id": "guideline-extended-keywords-name-anchor-only",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "color-keyword-ext-harvest-gold",
    "space": "concept"
   },
   "relation": "belongs_to_topic",
   "to": {
    "id": "topic-color-yellow-spectrum",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "color-keyword-ext-honeycomb",
    "space": "concept"
   },
   "relation": "belongs_to_topic",
   "to": {
    "id": "topic-color-yellow-spectrum",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "color-keyword-ext-sunflower",
    "space": "concept"
   },
   "relation": "belongs_to_topic",
   "to": {
    "id": "topic-color-yellow-spectrum",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "color-keyword-ext-sunflower",
    "space": "concept"
   },
   "relation": "cites",
   "to": {
    "id": "ref-reference-x-vol1-color",
    "space": "resource"
   }
  },
  {
   "from": {
    "id": "color-keyword-ext-sunflower",
    "space": "concept"
   },
   "relation": "requires",
   "to": {
    "id": "guideline-extended-keywords-name-anchor-only",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "color-keyword-ext-amber-gold",
    "space": "concept"
   },
   "relation": "belongs_to_topic",
   "to": {
    "id": "topic-color-yellow-spectrum",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "color-keyword-ext-amber-gold",
    "space": "concept"
   },
   "relation": "cites",
   "to": {
    "id": "ref-reference-x-vol1-color",
    "space": "resource"
   }
  },
  {
   "from": {
    "id": "color-keyword-ext-amber-gold",
    "space": "concept"
   },
   "relation": "requires",
   "to": {
    "id": "guideline-extended-keywords-name-anchor-only",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "color-keyword-ext-flaxseed",
    "space": "concept"
   },
   "relation": "belongs_to_topic",
   "to": {
    "id": "topic-color-yellow-spectrum",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "color-keyword-ext-flaxseed",
    "space": "concept"
   },
   "relation": "cites",
   "to": {
    "id": "ref-reference-x-vol1-color",
    "space": "resource"
   }
  },
  {
   "from": {
    "id": "color-keyword-ext-flaxseed",
    "space": "concept"
   },
   "relation": "requires",
   "to": {
    "id": "guideline-extended-keywords-name-anchor-only",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "color-keyword-ext-light-khaki",
    "space": "concept"
   },
   "relation": "belongs_to_topic",
   "to": {
    "id": "topic-color-yellow-spectrum",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "color-keyword-ext-light-khaki",
    "space": "concept"
   },
   "relation": "cites",
   "to": {
    "id": "ref-reference-x-vol1-color",
    "space": "resource"
   }
  },
  {
   "from": {
    "id": "color-keyword-ext-light-khaki",
    "space": "concept"
   },
   "relation": "requires",
   "to": {
    "id": "guideline-extended-keywords-name-anchor-only",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "color-keyword-ext-blond",
    "space": "concept"
   },
   "relation": "belongs_to_topic",
   "to": {
    "id": "topic-color-yellow-spectrum",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "color-keyword-ext-blond",
    "space": "concept"
   },
   "relation": "cites",
   "to": {
    "id": "ref-reference-x-vol1-color",
    "space": "resource"
   }
  },
  {
   "from": {
    "id": "color-keyword-ext-blond",
    "space": "concept"
   },
   "relation": "requires",
   "to": {
    "id": "guideline-extended-keywords-name-anchor-only",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "color-keyword-ext-candlelight",
    "space": "concept"
   },
   "relation": "belongs_to_topic",
   "to": {
    "id": "topic-color-yellow-spectrum",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "color-keyword-ext-candlelight",
    "space": "concept"
   },
   "relation": "cites",
   "to": {
    "id": "ref-reference-x-vol1-color",
    "space": "resource"
   }
  },
  {
   "from": {
    "id": "color-keyword-ext-candlelight",
    "space": "concept"
   },
   "relation": "requires",
   "to": {
    "id": "guideline-extended-keywords-name-anchor-only",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "color-keyword-ext-honeydew",
    "space": "concept"
   },
   "relation": "belongs_to_topic",
   "to": {
    "id": "topic-color-yellow-spectrum",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "color-keyword-ext-honeydew",
    "space": "concept"
   },
   "relation": "cites",
   "to": {
    "id": "ref-reference-x-vol1-color",
    "space": "resource"
   }
  },
  {
   "from": {
    "id": "color-keyword-ext-honeydew",
    "space": "concept"
   },
   "relation": "requires",
   "to": {
    "id": "guideline-extended-keywords-name-anchor-only",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "color-keyword-ext-solar-flare",
    "space": "concept"
   },
   "relation": "belongs_to_topic",
   "to": {
    "id": "topic-color-yellow-spectrum",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "color-keyword-ext-solar-flare",
    "space": "concept"
   },
   "relation": "cites",
   "to": {
    "id": "ref-reference-x-vol1-color",
    "space": "resource"
   }
  },
  {
   "from": {
    "id": "color-keyword-ext-solar-flare",
    "space": "concept"
   },
   "relation": "requires",
   "to": {
    "id": "guideline-extended-keywords-name-anchor-only",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "color-keyword-ext-sunshine-gold",
    "space": "concept"
   },
   "relation": "belongs_to_topic",
   "to": {
    "id": "topic-color-yellow-spectrum",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "color-keyword-ext-sunshine-gold",
    "space": "concept"
   },
   "relation": "cites",
   "to": {
    "id": "ref-reference-x-vol1-color",
    "space": "resource"
   }
  },
  {
   "from": {
    "id": "color-keyword-ext-sunshine-gold",
    "space": "concept"
   },
   "relation": "requires",
   "to": {
    "id": "guideline-extended-keywords-name-anchor-only",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "color-keyword-ext-dijon",
    "space": "concept"
   },
   "relation": "belongs_to_topic",
   "to": {
    "id": "topic-color-yellow-spectrum",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "color-keyword-ext-dijon",
    "space": "concept"
   },
   "relation": "cites",
   "to": {
    "id": "ref-reference-x-vol1-color",
    "space": "resource"
   }
  },
  {
   "from": {
    "id": "color-keyword-ext-dijon",
    "space": "concept"
   },
   "relation": "requires",
   "to": {
    "id": "guideline-extended-keywords-name-anchor-only",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "color-keyword-ext-saffron",
    "space": "concept"
   },
   "relation": "belongs_to_topic",
   "to": {
    "id": "topic-color-yellow-spectrum",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "color-keyword-ext-corn-yellow",
    "space": "concept"
   },
   "relation": "belongs_to_topic",
   "to": {
    "id": "topic-color-yellow-spectrum",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "color-keyword-ext-corn-yellow",
    "space": "concept"
   },
   "relation": "cites",
   "to": {
    "id": "ref-reference-x-vol1-color",
    "space": "resource"
   }
  },
  {
   "from": {
    "id": "color-keyword-ext-corn-yellow",
    "space": "concept"
   },
   "relation": "requires",
   "to": {
    "id": "guideline-extended-keywords-name-anchor-only",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "color-keyword-ext-honey",
    "space": "concept"
   },
   "relation": "belongs_to_topic",
   "to": {
    "id": "topic-color-yellow-spectrum",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "color-keyword-ext-honey",
    "space": "concept"
   },
   "relation": "cites",
   "to": {
    "id": "ref-reference-x-vol1-color",
    "space": "resource"
   }
  },
  {
   "from": {
    "id": "color-keyword-ext-honey",
    "space": "concept"
   },
   "relation": "requires",
   "to": {
    "id": "guideline-extended-keywords-name-anchor-only",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "color-keyword-ext-butter",
    "space": "concept"
   },
   "relation": "belongs_to_topic",
   "to": {
    "id": "topic-color-yellow-spectrum",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "color-keyword-ext-butter",
    "space": "concept"
   },
   "relation": "cites",
   "to": {
    "id": "ref-reference-x-vol1-color",
    "space": "resource"
   }
  },
  {
   "from": {
    "id": "color-keyword-ext-butter",
    "space": "concept"
   },
   "relation": "requires",
   "to": {
    "id": "guideline-extended-keywords-name-anchor-only",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "color-keyword-ext-curry",
    "space": "concept"
   },
   "relation": "belongs_to_topic",
   "to": {
    "id": "topic-color-yellow-spectrum",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "color-keyword-ext-curry",
    "space": "concept"
   },
   "relation": "cites",
   "to": {
    "id": "ref-reference-x-vol1-color",
    "space": "resource"
   }
  },
  {
   "from": {
    "id": "color-keyword-ext-curry",
    "space": "concept"
   },
   "relation": "requires",
   "to": {
    "id": "guideline-extended-keywords-name-anchor-only",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "color-keyword-ext-banana",
    "space": "concept"
   },
   "relation": "belongs_to_topic",
   "to": {
    "id": "topic-color-yellow-spectrum",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "color-keyword-ext-banana",
    "space": "concept"
   },
   "relation": "cites",
   "to": {
    "id": "ref-reference-x-vol1-color",
    "space": "resource"
   }
  },
  {
   "from": {
    "id": "color-keyword-ext-banana",
    "space": "concept"
   },
   "relation": "requires",
   "to": {
    "id": "guideline-extended-keywords-name-anchor-only",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "color-keyword-ext-chartreuse-yellow",
    "space": "concept"
   },
   "relation": "belongs_to_topic",
   "to": {
    "id": "topic-color-yellow-spectrum",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "color-keyword-ext-chartreuse-yellow",
    "space": "concept"
   },
   "relation": "cites",
   "to": {
    "id": "ref-reference-x-vol1-color",
    "space": "resource"
   }
  },
  {
   "from": {
    "id": "color-keyword-ext-chartreuse-yellow",
    "space": "concept"
   },
   "relation": "requires",
   "to": {
    "id": "guideline-extended-keywords-name-anchor-only",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "color-keyword-ext-aloe",
    "space": "concept"
   },
   "relation": "belongs_to_topic",
   "to": {
    "id": "topic-color-green-spectrum",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "color-keyword-ext-aloe",
    "space": "concept"
   },
   "relation": "cites",
   "to": {
    "id": "ref-reference-x-vol1-color",
    "space": "resource"
   }
  },
  {
   "from": {
    "id": "color-keyword-ext-aloe",
    "space": "concept"
   },
   "relation": "requires",
   "to": {
    "id": "guideline-extended-keywords-name-anchor-only",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "color-keyword-ext-basil-green",
    "space": "concept"
   },
   "relation": "belongs_to_topic",
   "to": {
    "id": "topic-color-green-spectrum",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "color-keyword-ext-basil-green",
    "space": "concept"
   },
   "relation": "cites",
   "to": {
    "id": "ref-reference-x-vol1-color",
    "space": "resource"
   }
  },
  {
   "from": {
    "id": "color-keyword-ext-basil-green",
    "space": "concept"
   },
   "relation": "requires",
   "to": {
    "id": "guideline-extended-keywords-name-anchor-only",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "color-keyword-ext-avocado",
    "space": "concept"
   },
   "relation": "belongs_to_topic",
   "to": {
    "id": "topic-color-green-spectrum",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "color-keyword-ext-avocado",
    "space": "concept"
   },
   "relation": "cites",
   "to": {
    "id": "ref-reference-x-vol1-color",
    "space": "resource"
   }
  },
  {
   "from": {
    "id": "color-keyword-ext-avocado",
    "space": "concept"
   },
   "relation": "requires",
   "to": {
    "id": "guideline-extended-keywords-name-anchor-only",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "color-keyword-ext-asparagus",
    "space": "concept"
   },
   "relation": "belongs_to_topic",
   "to": {
    "id": "topic-color-green-spectrum",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "color-keyword-ext-asparagus",
    "space": "concept"
   },
   "relation": "cites",
   "to": {
    "id": "ref-reference-x-vol1-color",
    "space": "resource"
   }
  },
  {
   "from": {
    "id": "color-keyword-ext-asparagus",
    "space": "concept"
   },
   "relation": "requires",
   "to": {
    "id": "guideline-extended-keywords-name-anchor-only",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "color-keyword-ext-beryl-green",
    "space": "concept"
   },
   "relation": "belongs_to_topic",
   "to": {
    "id": "topic-color-green-spectrum",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "color-keyword-ext-beryl-green",
    "space": "concept"
   },
   "relation": "cites",
   "to": {
    "id": "ref-reference-x-vol1-color",
    "space": "resource"
   }
  },
  {
   "from": {
    "id": "color-keyword-ext-beryl-green",
    "space": "concept"
   },
   "relation": "requires",
   "to": {
    "id": "guideline-extended-keywords-name-anchor-only",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "color-keyword-ext-chartreuse",
    "space": "concept"
   },
   "relation": "belongs_to_topic",
   "to": {
    "id": "topic-color-green-spectrum",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "color-keyword-ext-chartreuse",
    "space": "concept"
   },
   "relation": "cites",
   "to": {
    "id": "ref-reference-x-vol1-color",
    "space": "resource"
   }
  },
  {
   "from": {
    "id": "color-keyword-ext-chartreuse",
    "space": "concept"
   },
   "relation": "requires",
   "to": {
    "id": "guideline-extended-keywords-name-anchor-only",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "color-keyword-ext-cactus",
    "space": "concept"
   },
   "relation": "belongs_to_topic",
   "to": {
    "id": "topic-color-green-spectrum",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "color-keyword-ext-cactus",
    "space": "concept"
   },
   "relation": "cites",
   "to": {
    "id": "ref-reference-x-vol1-color",
    "space": "resource"
   }
  },
  {
   "from": {
    "id": "color-keyword-ext-cactus",
    "space": "concept"
   },
   "relation": "requires",
   "to": {
    "id": "guideline-extended-keywords-name-anchor-only",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "color-keyword-ext-eucalyptus",
    "space": "concept"
   },
   "relation": "belongs_to_topic",
   "to": {
    "id": "topic-color-green-spectrum",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "color-keyword-ext-eucalyptus",
    "space": "concept"
   },
   "relation": "cites",
   "to": {
    "id": "ref-reference-x-vol1-color",
    "space": "resource"
   }
  },
  {
   "from": {
    "id": "color-keyword-ext-eucalyptus",
    "space": "concept"
   },
   "relation": "requires",
   "to": {
    "id": "guideline-extended-keywords-name-anchor-only",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "color-keyword-ext-jade",
    "space": "concept"
   },
   "relation": "belongs_to_topic",
   "to": {
    "id": "topic-color-green-spectrum",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "color-keyword-ext-jade",
    "space": "concept"
   },
   "relation": "cites",
   "to": {
    "id": "ref-reference-x-vol1-color",
    "space": "resource"
   }
  },
  {
   "from": {
    "id": "color-keyword-ext-jade",
    "space": "concept"
   },
   "relation": "requires",
   "to": {
    "id": "guideline-extended-keywords-name-anchor-only",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "color-keyword-ext-juniper",
    "space": "concept"
   },
   "relation": "belongs_to_topic",
   "to": {
    "id": "topic-color-green-spectrum",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "color-keyword-ext-juniper",
    "space": "concept"
   },
   "relation": "cites",
   "to": {
    "id": "ref-reference-x-vol1-color",
    "space": "resource"
   }
  },
  {
   "from": {
    "id": "color-keyword-ext-juniper",
    "space": "concept"
   },
   "relation": "requires",
   "to": {
    "id": "guideline-extended-keywords-name-anchor-only",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "color-keyword-ext-khaki-green",
    "space": "concept"
   },
   "relation": "belongs_to_topic",
   "to": {
    "id": "topic-color-green-spectrum",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "color-keyword-ext-khaki-green",
    "space": "concept"
   },
   "relation": "cites",
   "to": {
    "id": "ref-reference-x-vol1-color",
    "space": "resource"
   }
  },
  {
   "from": {
    "id": "color-keyword-ext-khaki-green",
    "space": "concept"
   },
   "relation": "requires",
   "to": {
    "id": "guideline-extended-keywords-name-anchor-only",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "color-keyword-ext-loden",
    "space": "concept"
   },
   "relation": "belongs_to_topic",
   "to": {
    "id": "topic-color-green-spectrum",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "color-keyword-ext-loden",
    "space": "concept"
   },
   "relation": "cites",
   "to": {
    "id": "ref-reference-x-vol1-color",
    "space": "resource"
   }
  },
  {
   "from": {
    "id": "color-keyword-ext-loden",
    "space": "concept"
   },
   "relation": "requires",
   "to": {
    "id": "guideline-extended-keywords-name-anchor-only",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "color-keyword-ext-malachite",
    "space": "concept"
   },
   "relation": "belongs_to_topic",
   "to": {
    "id": "topic-color-green-spectrum",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "color-keyword-ext-malachite",
    "space": "concept"
   },
   "relation": "cites",
   "to": {
    "id": "ref-reference-x-vol1-color",
    "space": "resource"
   }
  },
  {
   "from": {
    "id": "color-keyword-ext-malachite",
    "space": "concept"
   },
   "relation": "requires",
   "to": {
    "id": "guideline-extended-keywords-name-anchor-only",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "color-keyword-ext-matcha",
    "space": "concept"
   },
   "relation": "belongs_to_topic",
   "to": {
    "id": "topic-color-green-spectrum",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "color-keyword-ext-matcha",
    "space": "concept"
   },
   "relation": "cites",
   "to": {
    "id": "ref-reference-x-vol1-color",
    "space": "resource"
   }
  },
  {
   "from": {
    "id": "color-keyword-ext-matcha",
    "space": "concept"
   },
   "relation": "requires",
   "to": {
    "id": "guideline-extended-keywords-name-anchor-only",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "color-keyword-ext-meadow",
    "space": "concept"
   },
   "relation": "belongs_to_topic",
   "to": {
    "id": "topic-color-green-spectrum",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "color-keyword-ext-meadow",
    "space": "concept"
   },
   "relation": "cites",
   "to": {
    "id": "ref-reference-x-vol1-color",
    "space": "resource"
   }
  },
  {
   "from": {
    "id": "color-keyword-ext-meadow",
    "space": "concept"
   },
   "relation": "requires",
   "to": {
    "id": "guideline-extended-keywords-name-anchor-only",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "color-keyword-ext-moss-gray",
    "space": "concept"
   },
   "relation": "belongs_to_topic",
   "to": {
    "id": "topic-color-green-spectrum",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "color-keyword-ext-moss-gray",
    "space": "concept"
   },
   "relation": "cites",
   "to": {
    "id": "ref-reference-x-vol1-color",
    "space": "resource"
   }
  },
  {
   "from": {
    "id": "color-keyword-ext-moss-gray",
    "space": "concept"
   },
   "relation": "requires",
   "to": {
    "id": "guideline-extended-keywords-name-anchor-only",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "color-keyword-ext-palm-leaf",
    "space": "concept"
   },
   "relation": "belongs_to_topic",
   "to": {
    "id": "topic-color-green-spectrum",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "color-keyword-ext-palm-leaf",
    "space": "concept"
   },
   "relation": "cites",
   "to": {
    "id": "ref-reference-x-vol1-color",
    "space": "resource"
   }
  },
  {
   "from": {
    "id": "color-keyword-ext-palm-leaf",
    "space": "concept"
   },
   "relation": "requires",
   "to": {
    "id": "guideline-extended-keywords-name-anchor-only",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "color-keyword-ext-pea-green",
    "space": "concept"
   },
   "relation": "belongs_to_topic",
   "to": {
    "id": "topic-color-green-spectrum",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "color-keyword-ext-pea-green",
    "space": "concept"
   },
   "relation": "cites",
   "to": {
    "id": "ref-reference-x-vol1-color",
    "space": "resource"
   }
  },
  {
   "from": {
    "id": "color-keyword-ext-pea-green",
    "space": "concept"
   },
   "relation": "requires",
   "to": {
    "id": "guideline-extended-keywords-name-anchor-only",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "color-keyword-ext-peridot",
    "space": "concept"
   },
   "relation": "belongs_to_topic",
   "to": {
    "id": "topic-color-green-spectrum",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "color-keyword-ext-peridot",
    "space": "concept"
   },
   "relation": "cites",
   "to": {
    "id": "ref-reference-x-vol1-color",
    "space": "resource"
   }
  },
  {
   "from": {
    "id": "color-keyword-ext-peridot",
    "space": "concept"
   },
   "relation": "requires",
   "to": {
    "id": "guideline-extended-keywords-name-anchor-only",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "color-keyword-ext-pine",
    "space": "concept"
   },
   "relation": "belongs_to_topic",
   "to": {
    "id": "topic-color-green-spectrum",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "color-keyword-ext-pine",
    "space": "concept"
   },
   "relation": "cites",
   "to": {
    "id": "ref-reference-x-vol1-color",
    "space": "resource"
   }
  },
  {
   "from": {
    "id": "color-keyword-ext-pine",
    "space": "concept"
   },
   "relation": "requires",
   "to": {
    "id": "guideline-extended-keywords-name-anchor-only",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "color-keyword-ext-sage-green",
    "space": "concept"
   },
   "relation": "belongs_to_topic",
   "to": {
    "id": "topic-color-green-spectrum",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "color-keyword-ext-sage-green",
    "space": "concept"
   },
   "relation": "cites",
   "to": {
    "id": "ref-reference-x-vol1-color",
    "space": "resource"
   }
  },
  {
   "from": {
    "id": "color-keyword-ext-sage-green",
    "space": "concept"
   },
   "relation": "requires",
   "to": {
    "id": "guideline-extended-keywords-name-anchor-only",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "color-keyword-ext-seafoam",
    "space": "concept"
   },
   "relation": "belongs_to_topic",
   "to": {
    "id": "topic-color-green-spectrum",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "color-keyword-ext-seafoam",
    "space": "concept"
   },
   "relation": "cites",
   "to": {
    "id": "ref-reference-x-vol1-color",
    "space": "resource"
   }
  },
  {
   "from": {
    "id": "color-keyword-ext-seafoam",
    "space": "concept"
   },
   "relation": "requires",
   "to": {
    "id": "guideline-extended-keywords-name-anchor-only",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "color-keyword-ext-spruce",
    "space": "concept"
   },
   "relation": "belongs_to_topic",
   "to": {
    "id": "topic-color-green-spectrum",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "color-keyword-ext-spruce",
    "space": "concept"
   },
   "relation": "cites",
   "to": {
    "id": "ref-reference-x-vol1-color",
    "space": "resource"
   }
  },
  {
   "from": {
    "id": "color-keyword-ext-spruce",
    "space": "concept"
   },
   "relation": "requires",
   "to": {
    "id": "guideline-extended-keywords-name-anchor-only",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "color-keyword-ext-tea-green",
    "space": "concept"
   },
   "relation": "belongs_to_topic",
   "to": {
    "id": "topic-color-green-spectrum",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "color-keyword-ext-tea-green",
    "space": "concept"
   },
   "relation": "cites",
   "to": {
    "id": "ref-reference-x-vol1-color",
    "space": "resource"
   }
  },
  {
   "from": {
    "id": "color-keyword-ext-tea-green",
    "space": "concept"
   },
   "relation": "requires",
   "to": {
    "id": "guideline-extended-keywords-name-anchor-only",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "color-keyword-ext-verdant",
    "space": "concept"
   },
   "relation": "belongs_to_topic",
   "to": {
    "id": "topic-color-green-spectrum",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "color-keyword-ext-verdant",
    "space": "concept"
   },
   "relation": "cites",
   "to": {
    "id": "ref-reference-x-vol1-color",
    "space": "resource"
   }
  },
  {
   "from": {
    "id": "color-keyword-ext-verdant",
    "space": "concept"
   },
   "relation": "requires",
   "to": {
    "id": "guideline-extended-keywords-name-anchor-only",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "color-keyword-ext-viridian",
    "space": "concept"
   },
   "relation": "belongs_to_topic",
   "to": {
    "id": "topic-color-green-spectrum",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "color-keyword-ext-viridian",
    "space": "concept"
   },
   "relation": "cites",
   "to": {
    "id": "ref-reference-x-vol1-color",
    "space": "resource"
   }
  },
  {
   "from": {
    "id": "color-keyword-ext-viridian",
    "space": "concept"
   },
   "relation": "requires",
   "to": {
    "id": "guideline-extended-keywords-name-anchor-only",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "color-keyword-ext-willow",
    "space": "concept"
   },
   "relation": "belongs_to_topic",
   "to": {
    "id": "topic-color-green-spectrum",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "color-keyword-ext-willow",
    "space": "concept"
   },
   "relation": "cites",
   "to": {
    "id": "ref-reference-x-vol1-color",
    "space": "resource"
   }
  },
  {
   "from": {
    "id": "color-keyword-ext-willow",
    "space": "concept"
   },
   "relation": "requires",
   "to": {
    "id": "guideline-extended-keywords-name-anchor-only",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "color-keyword-ext-wasabi",
    "space": "concept"
   },
   "relation": "belongs_to_topic",
   "to": {
    "id": "topic-color-green-spectrum",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "color-keyword-ext-wasabi",
    "space": "concept"
   },
   "relation": "cites",
   "to": {
    "id": "ref-reference-x-vol1-color",
    "space": "resource"
   }
  },
  {
   "from": {
    "id": "color-keyword-ext-wasabi",
    "space": "concept"
   },
   "relation": "requires",
   "to": {
    "id": "guideline-extended-keywords-name-anchor-only",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "color-keyword-ext-artichoke",
    "space": "concept"
   },
   "relation": "belongs_to_topic",
   "to": {
    "id": "topic-color-green-spectrum",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "color-keyword-ext-artichoke",
    "space": "concept"
   },
   "relation": "cites",
   "to": {
    "id": "ref-reference-x-vol1-color",
    "space": "resource"
   }
  },
  {
   "from": {
    "id": "color-keyword-ext-artichoke",
    "space": "concept"
   },
   "relation": "requires",
   "to": {
    "id": "guideline-extended-keywords-name-anchor-only",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "color-keyword-ext-pistache",
    "space": "concept"
   },
   "relation": "belongs_to_topic",
   "to": {
    "id": "topic-color-green-spectrum",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "color-keyword-ext-pistache",
    "space": "concept"
   },
   "relation": "cites",
   "to": {
    "id": "ref-reference-x-vol1-color",
    "space": "resource"
   }
  },
  {
   "from": {
    "id": "color-keyword-ext-pistache",
    "space": "concept"
   },
   "relation": "requires",
   "to": {
    "id": "guideline-extended-keywords-name-anchor-only",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "color-keyword-ext-pistachio",
    "space": "concept"
   },
   "relation": "belongs_to_topic",
   "to": {
    "id": "topic-color-green-spectrum",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "color-keyword-ext-pistachio",
    "space": "concept"
   },
   "relation": "cites",
   "to": {
    "id": "ref-reference-x-vol1-color",
    "space": "resource"
   }
  },
  {
   "from": {
    "id": "color-keyword-ext-pistachio",
    "space": "concept"
   },
   "relation": "requires",
   "to": {
    "id": "guideline-extended-keywords-name-anchor-only",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "color-keyword-ext-aegean",
    "space": "concept"
   },
   "relation": "belongs_to_topic",
   "to": {
    "id": "topic-color-blue-spectrum",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "color-keyword-ext-aegean",
    "space": "concept"
   },
   "relation": "cites",
   "to": {
    "id": "ref-reference-x-vol1-color",
    "space": "resource"
   }
  },
  {
   "from": {
    "id": "color-keyword-ext-aegean",
    "space": "concept"
   },
   "relation": "requires",
   "to": {
    "id": "guideline-extended-keywords-name-anchor-only",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "color-keyword-ext-arctic",
    "space": "concept"
   },
   "relation": "belongs_to_topic",
   "to": {
    "id": "topic-color-blue-spectrum",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "color-keyword-ext-arctic",
    "space": "concept"
   },
   "relation": "cites",
   "to": {
    "id": "ref-reference-x-vol1-color",
    "space": "resource"
   }
  },
  {
   "from": {
    "id": "color-keyword-ext-arctic",
    "space": "concept"
   },
   "relation": "requires",
   "to": {
    "id": "guideline-extended-keywords-name-anchor-only",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "color-keyword-ext-capri",
    "space": "concept"
   },
   "relation": "belongs_to_topic",
   "to": {
    "id": "topic-color-blue-spectrum",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "color-keyword-ext-capri",
    "space": "concept"
   },
   "relation": "cites",
   "to": {
    "id": "ref-reference-x-vol1-color",
    "space": "resource"
   }
  },
  {
   "from": {
    "id": "color-keyword-ext-capri",
    "space": "concept"
   },
   "relation": "requires",
   "to": {
    "id": "guideline-extended-keywords-name-anchor-only",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "color-keyword-ext-denim",
    "space": "concept"
   },
   "relation": "belongs_to_topic",
   "to": {
    "id": "topic-color-blue-spectrum",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "color-keyword-ext-denim",
    "space": "concept"
   },
   "relation": "cites",
   "to": {
    "id": "ref-reference-x-vol1-color",
    "space": "resource"
   }
  },
  {
   "from": {
    "id": "color-keyword-ext-denim",
    "space": "concept"
   },
   "relation": "requires",
   "to": {
    "id": "guideline-extended-keywords-name-anchor-only",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "color-keyword-ext-delft",
    "space": "concept"
   },
   "relation": "belongs_to_topic",
   "to": {
    "id": "topic-color-blue-spectrum",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "color-keyword-ext-delft",
    "space": "concept"
   },
   "relation": "cites",
   "to": {
    "id": "ref-reference-x-vol1-color",
    "space": "resource"
   }
  },
  {
   "from": {
    "id": "color-keyword-ext-delft",
    "space": "concept"
   },
   "relation": "requires",
   "to": {
    "id": "guideline-extended-keywords-name-anchor-only",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "color-keyword-ext-marine",
    "space": "concept"
   },
   "relation": "belongs_to_topic",
   "to": {
    "id": "topic-color-blue-spectrum",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "color-keyword-ext-marine",
    "space": "concept"
   },
   "relation": "cites",
   "to": {
    "id": "ref-reference-x-vol1-color",
    "space": "resource"
   }
  },
  {
   "from": {
    "id": "color-keyword-ext-marine",
    "space": "concept"
   },
   "relation": "requires",
   "to": {
    "id": "guideline-extended-keywords-name-anchor-only",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "color-keyword-ext-baltic",
    "space": "concept"
   },
   "relation": "belongs_to_topic",
   "to": {
    "id": "topic-color-blue-spectrum",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "color-keyword-ext-baltic",
    "space": "concept"
   },
   "relation": "cites",
   "to": {
    "id": "ref-reference-x-vol1-color",
    "space": "resource"
   }
  },
  {
   "from": {
    "id": "color-keyword-ext-baltic",
    "space": "concept"
   },
   "relation": "requires",
   "to": {
    "id": "guideline-extended-keywords-name-anchor-only",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "color-keyword-ext-glacier",
    "space": "concept"
   },
   "relation": "belongs_to_topic",
   "to": {
    "id": "topic-color-blue-spectrum",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "color-keyword-ext-glacier",
    "space": "concept"
   },
   "relation": "cites",
   "to": {
    "id": "ref-reference-x-vol1-color",
    "space": "resource"
   }
  },
  {
   "from": {
    "id": "color-keyword-ext-glacier",
    "space": "concept"
   },
   "relation": "requires",
   "to": {
    "id": "guideline-extended-keywords-name-anchor-only",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "color-keyword-ext-lagoon",
    "space": "concept"
   },
   "relation": "belongs_to_topic",
   "to": {
    "id": "topic-color-blue-spectrum",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "color-keyword-ext-lagoon",
    "space": "concept"
   },
   "relation": "cites",
   "to": {
    "id": "ref-reference-x-vol1-color",
    "space": "resource"
   }
  },
  {
   "from": {
    "id": "color-keyword-ext-lagoon",
    "space": "concept"
   },
   "relation": "requires",
   "to": {
    "id": "guideline-extended-keywords-name-anchor-only",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "color-keyword-ext-cyan",
    "space": "concept"
   },
   "relation": "belongs_to_topic",
   "to": {
    "id": "topic-color-blue-spectrum",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "color-keyword-ext-cyan",
    "space": "concept"
   },
   "relation": "cites",
   "to": {
    "id": "ref-reference-x-vol1-color",
    "space": "resource"
   }
  },
  {
   "from": {
    "id": "color-keyword-ext-cyan",
    "space": "concept"
   },
   "relation": "requires",
   "to": {
    "id": "guideline-extended-keywords-name-anchor-only",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "color-keyword-ext-peacock",
    "space": "concept"
   },
   "relation": "belongs_to_topic",
   "to": {
    "id": "topic-color-blue-spectrum",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "color-keyword-ext-peacock",
    "space": "concept"
   },
   "relation": "cites",
   "to": {
    "id": "ref-reference-x-vol1-color",
    "space": "resource"
   }
  },
  {
   "from": {
    "id": "color-keyword-ext-peacock",
    "space": "concept"
   },
   "relation": "requires",
   "to": {
    "id": "guideline-extended-keywords-name-anchor-only",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "color-keyword-ext-azure-mist",
    "space": "concept"
   },
   "relation": "belongs_to_topic",
   "to": {
    "id": "topic-color-blue-spectrum",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "color-keyword-ext-azure-mist",
    "space": "concept"
   },
   "relation": "cites",
   "to": {
    "id": "ref-reference-x-vol1-color",
    "space": "resource"
   }
  },
  {
   "from": {
    "id": "color-keyword-ext-azure-mist",
    "space": "concept"
   },
   "relation": "requires",
   "to": {
    "id": "guideline-extended-keywords-name-anchor-only",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "color-keyword-ext-royal",
    "space": "concept"
   },
   "relation": "belongs_to_topic",
   "to": {
    "id": "topic-color-blue-spectrum",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "color-keyword-ext-royal",
    "space": "concept"
   },
   "relation": "cites",
   "to": {
    "id": "ref-reference-x-vol1-color",
    "space": "resource"
   }
  },
  {
   "from": {
    "id": "color-keyword-ext-royal",
    "space": "concept"
   },
   "relation": "requires",
   "to": {
    "id": "guideline-extended-keywords-name-anchor-only",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "color-keyword-ext-skyfall",
    "space": "concept"
   },
   "relation": "belongs_to_topic",
   "to": {
    "id": "topic-color-blue-spectrum",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "color-keyword-ext-skyfall",
    "space": "concept"
   },
   "relation": "cites",
   "to": {
    "id": "ref-reference-x-vol1-color",
    "space": "resource"
   }
  },
  {
   "from": {
    "id": "color-keyword-ext-skyfall",
    "space": "concept"
   },
   "relation": "requires",
   "to": {
    "id": "guideline-extended-keywords-name-anchor-only",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "color-keyword-ext-blueprint",
    "space": "concept"
   },
   "relation": "belongs_to_topic",
   "to": {
    "id": "topic-color-blue-spectrum",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "color-keyword-ext-blueprint",
    "space": "concept"
   },
   "relation": "cites",
   "to": {
    "id": "ref-reference-x-vol1-color",
    "space": "resource"
   }
  },
  {
   "from": {
    "id": "color-keyword-ext-blueprint",
    "space": "concept"
   },
   "relation": "requires",
   "to": {
    "id": "guideline-extended-keywords-name-anchor-only",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "color-keyword-ext-horizon",
    "space": "concept"
   },
   "relation": "belongs_to_topic",
   "to": {
    "id": "topic-color-blue-spectrum",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "color-keyword-ext-horizon",
    "space": "concept"
   },
   "relation": "cites",
   "to": {
    "id": "ref-reference-x-vol1-color",
    "space": "resource"
   }
  },
  {
   "from": {
    "id": "color-keyword-ext-horizon",
    "space": "concept"
   },
   "relation": "requires",
   "to": {
    "id": "guideline-extended-keywords-name-anchor-only",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "color-keyword-ext-polar",
    "space": "concept"
   },
   "relation": "belongs_to_topic",
   "to": {
    "id": "topic-color-blue-spectrum",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "color-keyword-ext-polar",
    "space": "concept"
   },
   "relation": "cites",
   "to": {
    "id": "ref-reference-x-vol1-color",
    "space": "resource"
   }
  },
  {
   "from": {
    "id": "color-keyword-ext-polar",
    "space": "concept"
   },
   "relation": "requires",
   "to": {
    "id": "guideline-extended-keywords-name-anchor-only",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "color-keyword-ext-deep-sea",
    "space": "concept"
   },
   "relation": "belongs_to_topic",
   "to": {
    "id": "topic-color-blue-spectrum",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "color-keyword-ext-deep-sea",
    "space": "concept"
   },
   "relation": "cites",
   "to": {
    "id": "ref-reference-x-vol1-color",
    "space": "resource"
   }
  },
  {
   "from": {
    "id": "color-keyword-ext-deep-sea",
    "space": "concept"
   },
   "relation": "requires",
   "to": {
    "id": "guideline-extended-keywords-name-anchor-only",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "color-keyword-ext-arctic-shadow",
    "space": "concept"
   },
   "relation": "belongs_to_topic",
   "to": {
    "id": "topic-color-blue-spectrum",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "color-keyword-ext-arctic-shadow",
    "space": "concept"
   },
   "relation": "cites",
   "to": {
    "id": "ref-reference-x-vol1-color",
    "space": "resource"
   }
  },
  {
   "from": {
    "id": "color-keyword-ext-arctic-shadow",
    "space": "concept"
   },
   "relation": "requires",
   "to": {
    "id": "guideline-extended-keywords-name-anchor-only",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "color-keyword-ext-true-blue",
    "space": "concept"
   },
   "relation": "belongs_to_topic",
   "to": {
    "id": "topic-color-blue-spectrum",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "color-keyword-ext-true-blue",
    "space": "concept"
   },
   "relation": "cites",
   "to": {
    "id": "ref-reference-x-vol1-color",
    "space": "resource"
   }
  },
  {
   "from": {
    "id": "color-keyword-ext-true-blue",
    "space": "concept"
   },
   "relation": "requires",
   "to": {
    "id": "guideline-extended-keywords-name-anchor-only",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "color-keyword-ext-pacific",
    "space": "concept"
   },
   "relation": "belongs_to_topic",
   "to": {
    "id": "topic-color-blue-spectrum",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "color-keyword-ext-pacific",
    "space": "concept"
   },
   "relation": "cites",
   "to": {
    "id": "ref-reference-x-vol1-color",
    "space": "resource"
   }
  },
  {
   "from": {
    "id": "color-keyword-ext-pacific",
    "space": "concept"
   },
   "relation": "requires",
   "to": {
    "id": "guideline-extended-keywords-name-anchor-only",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "color-keyword-ext-arctic-dawn",
    "space": "concept"
   },
   "relation": "belongs_to_topic",
   "to": {
    "id": "topic-color-blue-spectrum",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "color-keyword-ext-arctic-dawn",
    "space": "concept"
   },
   "relation": "cites",
   "to": {
    "id": "ref-reference-x-vol1-color",
    "space": "resource"
   }
  },
  {
   "from": {
    "id": "color-keyword-ext-arctic-dawn",
    "space": "concept"
   },
   "relation": "requires",
   "to": {
    "id": "guideline-extended-keywords-name-anchor-only",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "color-keyword-ext-storm",
    "space": "concept"
   },
   "relation": "belongs_to_topic",
   "to": {
    "id": "topic-color-blue-spectrum",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "color-keyword-ext-storm",
    "space": "concept"
   },
   "relation": "cites",
   "to": {
    "id": "ref-reference-x-vol1-color",
    "space": "resource"
   }
  },
  {
   "from": {
    "id": "color-keyword-ext-storm",
    "space": "concept"
   },
   "relation": "requires",
   "to": {
    "id": "guideline-extended-keywords-name-anchor-only",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "color-keyword-ext-cobalt-blue",
    "space": "concept"
   },
   "relation": "belongs_to_topic",
   "to": {
    "id": "topic-color-blue-spectrum",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "color-keyword-ext-cobalt-blue",
    "space": "concept"
   },
   "relation": "cites",
   "to": {
    "id": "ref-reference-x-vol1-color",
    "space": "resource"
   }
  },
  {
   "from": {
    "id": "color-keyword-ext-cobalt-blue",
    "space": "concept"
   },
   "relation": "requires",
   "to": {
    "id": "guideline-extended-keywords-name-anchor-only",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "color-keyword-ext-air-force",
    "space": "concept"
   },
   "relation": "belongs_to_topic",
   "to": {
    "id": "topic-color-blue-spectrum",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "color-keyword-ext-air-force",
    "space": "concept"
   },
   "relation": "cites",
   "to": {
    "id": "ref-reference-x-vol1-color",
    "space": "resource"
   }
  },
  {
   "from": {
    "id": "color-keyword-ext-air-force",
    "space": "concept"
   },
   "relation": "requires",
   "to": {
    "id": "guideline-extended-keywords-name-anchor-only",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "color-keyword-ext-tidal",
    "space": "concept"
   },
   "relation": "belongs_to_topic",
   "to": {
    "id": "topic-color-blue-spectrum",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "color-keyword-ext-tidal",
    "space": "concept"
   },
   "relation": "cites",
   "to": {
    "id": "ref-reference-x-vol1-color",
    "space": "resource"
   }
  },
  {
   "from": {
    "id": "color-keyword-ext-tidal",
    "space": "concept"
   },
   "relation": "requires",
   "to": {
    "id": "guideline-extended-keywords-name-anchor-only",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "color-keyword-ext-nordic",
    "space": "concept"
   },
   "relation": "belongs_to_topic",
   "to": {
    "id": "topic-color-blue-spectrum",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "color-keyword-ext-nordic",
    "space": "concept"
   },
   "relation": "cites",
   "to": {
    "id": "ref-reference-x-vol1-color",
    "space": "resource"
   }
  },
  {
   "from": {
    "id": "color-keyword-ext-nordic",
    "space": "concept"
   },
   "relation": "requires",
   "to": {
    "id": "guideline-extended-keywords-name-anchor-only",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "color-keyword-ext-vapor",
    "space": "concept"
   },
   "relation": "belongs_to_topic",
   "to": {
    "id": "topic-color-blue-spectrum",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "color-keyword-ext-vapor",
    "space": "concept"
   },
   "relation": "cites",
   "to": {
    "id": "ref-reference-x-vol1-color",
    "space": "resource"
   }
  },
  {
   "from": {
    "id": "color-keyword-ext-vapor",
    "space": "concept"
   },
   "relation": "requires",
   "to": {
    "id": "guideline-extended-keywords-name-anchor-only",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "color-keyword-ext-jetstream",
    "space": "concept"
   },
   "relation": "belongs_to_topic",
   "to": {
    "id": "topic-color-blue-spectrum",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "color-keyword-ext-jetstream",
    "space": "concept"
   },
   "relation": "cites",
   "to": {
    "id": "ref-reference-x-vol1-color",
    "space": "resource"
   }
  },
  {
   "from": {
    "id": "color-keyword-ext-jetstream",
    "space": "concept"
   },
   "relation": "requires",
   "to": {
    "id": "guideline-extended-keywords-name-anchor-only",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "color-keyword-ext-indigo-blue",
    "space": "concept"
   },
   "relation": "belongs_to_topic",
   "to": {
    "id": "topic-color-blue-spectrum",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "color-keyword-ext-indigo-blue",
    "space": "concept"
   },
   "relation": "cites",
   "to": {
    "id": "ref-reference-x-vol1-color",
    "space": "resource"
   }
  },
  {
   "from": {
    "id": "color-keyword-ext-indigo-blue",
    "space": "concept"
   },
   "relation": "requires",
   "to": {
    "id": "guideline-extended-keywords-name-anchor-only",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "color-keyword-ext-amethyst",
    "space": "concept"
   },
   "relation": "belongs_to_topic",
   "to": {
    "id": "topic-color-violet-spectrum",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "color-keyword-ext-amethyst",
    "space": "concept"
   },
   "relation": "cites",
   "to": {
    "id": "ref-reference-x-vol1-color",
    "space": "resource"
   }
  },
  {
   "from": {
    "id": "color-keyword-ext-amethyst",
    "space": "concept"
   },
   "relation": "requires",
   "to": {
    "id": "guideline-extended-keywords-name-anchor-only",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "color-keyword-ext-heliotrope",
    "space": "concept"
   },
   "relation": "belongs_to_topic",
   "to": {
    "id": "topic-color-violet-spectrum",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "color-keyword-ext-heliotrope",
    "space": "concept"
   },
   "relation": "cites",
   "to": {
    "id": "ref-reference-x-vol1-color",
    "space": "resource"
   }
  },
  {
   "from": {
    "id": "color-keyword-ext-heliotrope",
    "space": "concept"
   },
   "relation": "requires",
   "to": {
    "id": "guideline-extended-keywords-name-anchor-only",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "color-keyword-ext-orchid",
    "space": "concept"
   },
   "relation": "belongs_to_topic",
   "to": {
    "id": "topic-color-violet-spectrum",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "color-keyword-ext-orchid",
    "space": "concept"
   },
   "relation": "cites",
   "to": {
    "id": "ref-reference-x-vol1-color",
    "space": "resource"
   }
  },
  {
   "from": {
    "id": "color-keyword-ext-orchid",
    "space": "concept"
   },
   "relation": "requires",
   "to": {
    "id": "guideline-extended-keywords-name-anchor-only",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "color-keyword-ext-mulberry",
    "space": "concept"
   },
   "relation": "belongs_to_topic",
   "to": {
    "id": "topic-color-violet-spectrum",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "color-keyword-ext-mulberry",
    "space": "concept"
   },
   "relation": "cites",
   "to": {
    "id": "ref-reference-x-vol1-color",
    "space": "resource"
   }
  },
  {
   "from": {
    "id": "color-keyword-ext-mulberry",
    "space": "concept"
   },
   "relation": "requires",
   "to": {
    "id": "guideline-extended-keywords-name-anchor-only",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "color-keyword-ext-plum",
    "space": "concept"
   },
   "relation": "belongs_to_topic",
   "to": {
    "id": "topic-color-violet-spectrum",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "color-keyword-ext-plum",
    "space": "concept"
   },
   "relation": "cites",
   "to": {
    "id": "ref-reference-x-vol1-color",
    "space": "resource"
   }
  },
  {
   "from": {
    "id": "color-keyword-ext-plum",
    "space": "concept"
   },
   "relation": "requires",
   "to": {
    "id": "guideline-extended-keywords-name-anchor-only",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "color-keyword-ext-violet-storm",
    "space": "concept"
   },
   "relation": "belongs_to_topic",
   "to": {
    "id": "topic-color-violet-spectrum",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "color-keyword-ext-violet-storm",
    "space": "concept"
   },
   "relation": "cites",
   "to": {
    "id": "ref-reference-x-vol1-color",
    "space": "resource"
   }
  },
  {
   "from": {
    "id": "color-keyword-ext-violet-storm",
    "space": "concept"
   },
   "relation": "requires",
   "to": {
    "id": "guideline-extended-keywords-name-anchor-only",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "color-keyword-ext-mystic-violet",
    "space": "concept"
   },
   "relation": "belongs_to_topic",
   "to": {
    "id": "topic-color-violet-spectrum",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "color-keyword-ext-mystic-violet",
    "space": "concept"
   },
   "relation": "cites",
   "to": {
    "id": "ref-reference-x-vol1-color",
    "space": "resource"
   }
  },
  {
   "from": {
    "id": "color-keyword-ext-mystic-violet",
    "space": "concept"
   },
   "relation": "requires",
   "to": {
    "id": "guideline-extended-keywords-name-anchor-only",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "color-keyword-ext-digital-lavender",
    "space": "concept"
   },
   "relation": "belongs_to_topic",
   "to": {
    "id": "topic-color-violet-spectrum",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "color-keyword-ext-digital-lavender",
    "space": "concept"
   },
   "relation": "cites",
   "to": {
    "id": "ref-reference-x-vol1-color",
    "space": "resource"
   }
  },
  {
   "from": {
    "id": "color-keyword-ext-digital-lavender",
    "space": "concept"
   },
   "relation": "requires",
   "to": {
    "id": "guideline-extended-keywords-name-anchor-only",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "color-keyword-ext-dusty-lilac",
    "space": "concept"
   },
   "relation": "belongs_to_topic",
   "to": {
    "id": "topic-color-violet-spectrum",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "color-keyword-ext-dusty-lilac",
    "space": "concept"
   },
   "relation": "cites",
   "to": {
    "id": "ref-reference-x-vol1-color",
    "space": "resource"
   }
  },
  {
   "from": {
    "id": "color-keyword-ext-dusty-lilac",
    "space": "concept"
   },
   "relation": "requires",
   "to": {
    "id": "guideline-extended-keywords-name-anchor-only",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "color-keyword-ext-radiant-orchid",
    "space": "concept"
   },
   "relation": "belongs_to_topic",
   "to": {
    "id": "topic-color-violet-spectrum",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "color-keyword-ext-radiant-orchid",
    "space": "concept"
   },
   "relation": "cites",
   "to": {
    "id": "ref-reference-x-vol1-color",
    "space": "resource"
   }
  },
  {
   "from": {
    "id": "color-keyword-ext-radiant-orchid",
    "space": "concept"
   },
   "relation": "requires",
   "to": {
    "id": "guideline-extended-keywords-name-anchor-only",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "color-keyword-ext-boysenberry",
    "space": "concept"
   },
   "relation": "belongs_to_topic",
   "to": {
    "id": "topic-color-violet-spectrum",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "color-keyword-ext-boysenberry",
    "space": "concept"
   },
   "relation": "cites",
   "to": {
    "id": "ref-reference-x-vol1-color",
    "space": "resource"
   }
  },
  {
   "from": {
    "id": "color-keyword-ext-boysenberry",
    "space": "concept"
   },
   "relation": "requires",
   "to": {
    "id": "guideline-extended-keywords-name-anchor-only",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "color-keyword-ext-tyrian-purple",
    "space": "concept"
   },
   "relation": "belongs_to_topic",
   "to": {
    "id": "topic-color-violet-spectrum",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "color-keyword-ext-tyrian-purple",
    "space": "concept"
   },
   "relation": "cites",
   "to": {
    "id": "ref-reference-x-vol1-color",
    "space": "resource"
   }
  },
  {
   "from": {
    "id": "color-keyword-ext-tyrian-purple",
    "space": "concept"
   },
   "relation": "requires",
   "to": {
    "id": "guideline-extended-keywords-name-anchor-only",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "color-keyword-ext-wisteria",
    "space": "concept"
   },
   "relation": "belongs_to_topic",
   "to": {
    "id": "topic-color-violet-spectrum",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "color-keyword-ext-wisteria",
    "space": "concept"
   },
   "relation": "cites",
   "to": {
    "id": "ref-reference-x-vol1-color",
    "space": "resource"
   }
  },
  {
   "from": {
    "id": "color-keyword-ext-wisteria",
    "space": "concept"
   },
   "relation": "requires",
   "to": {
    "id": "guideline-extended-keywords-name-anchor-only",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "color-keyword-ext-lavender-gray",
    "space": "concept"
   },
   "relation": "belongs_to_topic",
   "to": {
    "id": "topic-color-violet-spectrum",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "color-keyword-ext-lavender-gray",
    "space": "concept"
   },
   "relation": "cites",
   "to": {
    "id": "ref-reference-x-vol1-color",
    "space": "resource"
   }
  },
  {
   "from": {
    "id": "color-keyword-ext-lavender-gray",
    "space": "concept"
   },
   "relation": "requires",
   "to": {
    "id": "guideline-extended-keywords-name-anchor-only",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "color-keyword-ext-french-lilac",
    "space": "concept"
   },
   "relation": "belongs_to_topic",
   "to": {
    "id": "topic-color-violet-spectrum",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "color-keyword-ext-french-lilac",
    "space": "concept"
   },
   "relation": "cites",
   "to": {
    "id": "ref-reference-x-vol1-color",
    "space": "resource"
   }
  },
  {
   "from": {
    "id": "color-keyword-ext-french-lilac",
    "space": "concept"
   },
   "relation": "requires",
   "to": {
    "id": "guideline-extended-keywords-name-anchor-only",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "color-keyword-ext-raisin-purple",
    "space": "concept"
   },
   "relation": "belongs_to_topic",
   "to": {
    "id": "topic-color-violet-spectrum",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "color-keyword-ext-raisin-purple",
    "space": "concept"
   },
   "relation": "cites",
   "to": {
    "id": "ref-reference-x-vol1-color",
    "space": "resource"
   }
  },
  {
   "from": {
    "id": "color-keyword-ext-raisin-purple",
    "space": "concept"
   },
   "relation": "requires",
   "to": {
    "id": "guideline-extended-keywords-name-anchor-only",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "color-keyword-ext-opera-mauve",
    "space": "concept"
   },
   "relation": "belongs_to_topic",
   "to": {
    "id": "topic-color-violet-spectrum",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "color-keyword-ext-opera-mauve",
    "space": "concept"
   },
   "relation": "cites",
   "to": {
    "id": "ref-reference-x-vol1-color",
    "space": "resource"
   }
  },
  {
   "from": {
    "id": "color-keyword-ext-opera-mauve",
    "space": "concept"
   },
   "relation": "requires",
   "to": {
    "id": "guideline-extended-keywords-name-anchor-only",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "color-keyword-ext-pansy-purple",
    "space": "concept"
   },
   "relation": "belongs_to_topic",
   "to": {
    "id": "topic-color-violet-spectrum",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "color-keyword-ext-pansy-purple",
    "space": "concept"
   },
   "relation": "cites",
   "to": {
    "id": "ref-reference-x-vol1-color",
    "space": "resource"
   }
  },
  {
   "from": {
    "id": "color-keyword-ext-pansy-purple",
    "space": "concept"
   },
   "relation": "requires",
   "to": {
    "id": "guideline-extended-keywords-name-anchor-only",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "color-keyword-ext-berry-bliss",
    "space": "concept"
   },
   "relation": "belongs_to_topic",
   "to": {
    "id": "topic-color-violet-spectrum",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "color-keyword-ext-berry-bliss",
    "space": "concept"
   },
   "relation": "cites",
   "to": {
    "id": "ref-reference-x-vol1-color",
    "space": "resource"
   }
  },
  {
   "from": {
    "id": "color-keyword-ext-berry-bliss",
    "space": "concept"
   },
   "relation": "requires",
   "to": {
    "id": "guideline-extended-keywords-name-anchor-only",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "color-keyword-ext-berry-wine",
    "space": "concept"
   },
   "relation": "belongs_to_topic",
   "to": {
    "id": "topic-color-violet-spectrum",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "color-keyword-ext-berry-wine",
    "space": "concept"
   },
   "relation": "cites",
   "to": {
    "id": "ref-reference-x-vol1-color",
    "space": "resource"
   }
  },
  {
   "from": {
    "id": "color-keyword-ext-berry-wine",
    "space": "concept"
   },
   "relation": "requires",
   "to": {
    "id": "guideline-extended-keywords-name-anchor-only",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "color-keyword-ext-purple-basil",
    "space": "concept"
   },
   "relation": "belongs_to_topic",
   "to": {
    "id": "topic-color-violet-spectrum",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "color-keyword-ext-purple-basil",
    "space": "concept"
   },
   "relation": "cites",
   "to": {
    "id": "ref-reference-x-vol1-color",
    "space": "resource"
   }
  },
  {
   "from": {
    "id": "color-keyword-ext-purple-basil",
    "space": "concept"
   },
   "relation": "requires",
   "to": {
    "id": "guideline-extended-keywords-name-anchor-only",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "color-keyword-ext-deep-magenta",
    "space": "concept"
   },
   "relation": "belongs_to_topic",
   "to": {
    "id": "topic-color-violet-spectrum",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "color-keyword-ext-deep-magenta",
    "space": "concept"
   },
   "relation": "cites",
   "to": {
    "id": "ref-reference-x-vol1-color",
    "space": "resource"
   }
  },
  {
   "from": {
    "id": "color-keyword-ext-deep-magenta",
    "space": "concept"
   },
   "relation": "requires",
   "to": {
    "id": "guideline-extended-keywords-name-anchor-only",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "color-keyword-ext-blue-violet",
    "space": "concept"
   },
   "relation": "belongs_to_topic",
   "to": {
    "id": "topic-color-violet-spectrum",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "color-keyword-ext-blue-violet",
    "space": "concept"
   },
   "relation": "cites",
   "to": {
    "id": "ref-reference-x-vol1-color",
    "space": "resource"
   }
  },
  {
   "from": {
    "id": "color-keyword-ext-blue-violet",
    "space": "concept"
   },
   "relation": "requires",
   "to": {
    "id": "guideline-extended-keywords-name-anchor-only",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "color-keyword-ext-fuchsia-purple",
    "space": "concept"
   },
   "relation": "belongs_to_topic",
   "to": {
    "id": "topic-color-violet-spectrum",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "color-keyword-ext-fuchsia-purple",
    "space": "concept"
   },
   "relation": "cites",
   "to": {
    "id": "ref-reference-x-vol1-color",
    "space": "resource"
   }
  },
  {
   "from": {
    "id": "color-keyword-ext-fuchsia-purple",
    "space": "concept"
   },
   "relation": "requires",
   "to": {
    "id": "guideline-extended-keywords-name-anchor-only",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "color-keyword-ext-grape-juice",
    "space": "concept"
   },
   "relation": "belongs_to_topic",
   "to": {
    "id": "topic-color-violet-spectrum",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "color-keyword-ext-grape-juice",
    "space": "concept"
   },
   "relation": "cites",
   "to": {
    "id": "ref-reference-x-vol1-color",
    "space": "resource"
   }
  },
  {
   "from": {
    "id": "color-keyword-ext-grape-juice",
    "space": "concept"
   },
   "relation": "requires",
   "to": {
    "id": "guideline-extended-keywords-name-anchor-only",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "color-keyword-ext-wine-berry",
    "space": "concept"
   },
   "relation": "belongs_to_topic",
   "to": {
    "id": "topic-color-violet-spectrum",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "color-keyword-ext-wine-berry",
    "space": "concept"
   },
   "relation": "cites",
   "to": {
    "id": "ref-reference-x-vol1-color",
    "space": "resource"
   }
  },
  {
   "from": {
    "id": "color-keyword-ext-wine-berry",
    "space": "concept"
   },
   "relation": "requires",
   "to": {
    "id": "guideline-extended-keywords-name-anchor-only",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "color-keyword-ext-berry-bloom",
    "space": "concept"
   },
   "relation": "belongs_to_topic",
   "to": {
    "id": "topic-color-violet-spectrum",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "color-keyword-ext-berry-bloom",
    "space": "concept"
   },
   "relation": "cites",
   "to": {
    "id": "ref-reference-x-vol1-color",
    "space": "resource"
   }
  },
  {
   "from": {
    "id": "color-keyword-ext-berry-bloom",
    "space": "concept"
   },
   "relation": "requires",
   "to": {
    "id": "guideline-extended-keywords-name-anchor-only",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "color-keyword-ext-purple-haze",
    "space": "concept"
   },
   "relation": "belongs_to_topic",
   "to": {
    "id": "topic-color-violet-spectrum",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "color-keyword-ext-purple-haze",
    "space": "concept"
   },
   "relation": "cites",
   "to": {
    "id": "ref-reference-x-vol1-color",
    "space": "resource"
   }
  },
  {
   "from": {
    "id": "color-keyword-ext-purple-haze",
    "space": "concept"
   },
   "relation": "requires",
   "to": {
    "id": "guideline-extended-keywords-name-anchor-only",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "color-keyword-ext-heather-violet",
    "space": "concept"
   },
   "relation": "belongs_to_topic",
   "to": {
    "id": "topic-color-violet-spectrum",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "color-keyword-ext-heather-violet",
    "space": "concept"
   },
   "relation": "cites",
   "to": {
    "id": "ref-reference-x-vol1-color",
    "space": "resource"
   }
  },
  {
   "from": {
    "id": "color-keyword-ext-heather-violet",
    "space": "concept"
   },
   "relation": "requires",
   "to": {
    "id": "guideline-extended-keywords-name-anchor-only",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "color-keyword-ext-twilight-lavender",
    "space": "concept"
   },
   "relation": "belongs_to_topic",
   "to": {
    "id": "topic-color-violet-spectrum",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "color-keyword-ext-twilight-lavender",
    "space": "concept"
   },
   "relation": "cites",
   "to": {
    "id": "ref-reference-x-vol1-color",
    "space": "resource"
   }
  },
  {
   "from": {
    "id": "color-keyword-ext-twilight-lavender",
    "space": "concept"
   },
   "relation": "requires",
   "to": {
    "id": "guideline-extended-keywords-name-anchor-only",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "layer-color-reference-x-v1",
    "space": "resource"
   },
   "relation": "contains",
   "to": {
    "id": "topic-color-palette-abstraction-policy",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "guideline-no-palette-table-reconstruction",
    "space": "concept"
   },
   "relation": "belongs_to_topic",
   "to": {
    "id": "topic-color-palette-abstraction-policy",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "guideline-no-palette-table-reconstruction",
    "space": "concept"
   },
   "relation": "cites",
   "to": {
    "id": "ref-reference-x-vol1-color",
    "space": "resource"
   }
  },
  {
   "from": {
    "id": "guideline-no-palette-table-reconstruction",
    "space": "concept"
   },
   "relation": "requires",
   "to": {
    "id": "guideline-reference-images-are-tonal-evidence-not-assets",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "pattern-palette-by-role-and-contrast-not-table-row",
    "space": "concept"
   },
   "relation": "belongs_to_topic",
   "to": {
    "id": "topic-color-palette-abstraction-policy",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "pattern-palette-by-role-and-contrast-not-table-row",
    "space": "concept"
   },
   "relation": "cites",
   "to": {
    "id": "ref-reference-x-vol1-color",
    "space": "resource"
   }
  },
  {
   "from": {
    "id": "pattern-palette-by-role-and-contrast-not-table-row",
    "space": "concept"
   },
   "relation": "requires",
   "to": {
    "id": "pattern-color-keyword-to-tone-archive",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "pattern-palette-by-role-and-contrast-not-table-row",
    "space": "concept"
   },
   "relation": "requires",
   "to": {
    "id": "guideline-mood-tags-before-palette-expansion",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "guideline-palette-pair-edges-require-transformative-brief",
    "space": "concept"
   },
   "relation": "belongs_to_topic",
   "to": {
    "id": "topic-color-palette-abstraction-policy",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "guideline-palette-pair-edges-require-transformative-brief",
    "space": "concept"
   },
   "relation": "cites",
   "to": {
    "id": "ref-reference-x-vol1-color",
    "space": "resource"
   }
  },
  {
   "from": {
    "id": "guideline-palette-pair-edges-require-transformative-brief",
    "space": "concept"
   },
   "relation": "requires",
   "to": {
    "id": "guideline-no-palette-table-reconstruction",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "guideline-palette-pair-edges-require-transformative-brief",
    "space": "concept"
   },
   "relation": "pairs_well_with",
   "to": {
    "id": "pattern-tone-archive-preserves-transferability",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "heuristic-palette-abstraction-review-gate",
    "space": "concept"
   },
   "relation": "belongs_to_topic",
   "to": {
    "id": "topic-color-palette-abstraction-policy",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "heuristic-palette-abstraction-review-gate",
    "space": "concept"
   },
   "relation": "cites",
   "to": {
    "id": "ref-reference-x-vol1-color",
    "space": "resource"
   }
  },
  {
   "from": {
    "id": "heuristic-palette-abstraction-review-gate",
    "space": "concept"
   },
   "relation": "requires",
   "to": {
    "id": "guideline-no-palette-table-reconstruction",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "heuristic-palette-abstraction-review-gate",
    "space": "concept"
   },
   "relation": "requires",
   "to": {
    "id": "pattern-palette-by-role-and-contrast-not-table-row",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "pattern-safe-palette-output-contract",
    "space": "concept"
   },
   "relation": "belongs_to_topic",
   "to": {
    "id": "topic-color-palette-abstraction-policy",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "pattern-safe-palette-output-contract",
    "space": "concept"
   },
   "relation": "cites",
   "to": {
    "id": "ref-reference-x-vol1-color",
    "space": "resource"
   }
  },
  {
   "from": {
    "id": "pattern-safe-palette-output-contract",
    "space": "concept"
   },
   "relation": "requires",
   "to": {
    "id": "guideline-palette-pair-edges-require-transformative-brief",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "pattern-safe-palette-output-contract",
    "space": "concept"
   },
   "relation": "requires",
   "to": {
    "id": "heuristic-palette-abstraction-review-gate",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "pattern-safe-palette-output-contract",
    "space": "concept"
   },
   "relation": "pairs_well_with",
   "to": {
    "id": "guideline-rgb-cmyk-split-by-output-medium",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "guideline-palette-not-three-color-pick",
    "space": "concept"
   },
   "relation": "belongs_to_topic",
   "to": {
    "id": "topic-color-palette-abstraction-policy",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "guideline-palette-not-three-color-pick",
    "space": "concept"
   },
   "relation": "requires",
   "to": {
    "id": "pattern-palette-by-role-and-contrast-not-table-row",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "guideline-palette-not-three-color-pick",
    "space": "concept"
   },
   "relation": "requires",
   "to": {
    "id": "pattern-safe-palette-output-contract",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "pattern-palette-role-combination-matrix",
    "space": "concept"
   },
   "relation": "belongs_to_topic",
   "to": {
    "id": "topic-color-palette-abstraction-policy",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "pattern-palette-role-combination-matrix",
    "space": "concept"
   },
   "relation": "requires",
   "to": {
    "id": "guideline-palette-not-three-color-pick",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "pattern-palette-role-combination-matrix",
    "space": "concept"
   },
   "relation": "requires",
   "to": {
    "id": "guideline-no-palette-table-reconstruction",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "pattern-palette-role-combination-matrix",
    "space": "concept"
   },
   "relation": "pairs_well_with",
   "to": {
    "id": "guideline-rgb-cmyk-split-by-output-medium",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "pattern-palette-combination-to-component-token-grid",
    "space": "concept"
   },
   "relation": "belongs_to_topic",
   "to": {
    "id": "topic-color-palette-abstraction-policy",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "pattern-palette-combination-to-component-token-grid",
    "space": "concept"
   },
   "relation": "requires",
   "to": {
    "id": "pattern-palette-role-combination-matrix",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "pattern-palette-combination-to-component-token-grid",
    "space": "concept"
   },
   "relation": "requires",
   "to": {
    "id": "pattern-safe-palette-output-contract",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "pattern-sample-board-separates-anchor-and-usage",
    "space": "concept"
   },
   "relation": "belongs_to_topic",
   "to": {
    "id": "topic-color-tone-archive",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "pattern-sample-board-separates-anchor-and-usage",
    "space": "concept"
   },
   "relation": "cites",
   "to": {
    "id": "ref-reference-x-vol1-color",
    "space": "resource"
   }
  },
  {
   "from": {
    "id": "pattern-sample-board-separates-anchor-and-usage",
    "space": "concept"
   },
   "relation": "requires",
   "to": {
    "id": "pattern-color-keyword-to-tone-archive",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "guideline-do-not-bind-color-to-fixed-subject",
    "space": "concept"
   },
   "relation": "belongs_to_topic",
   "to": {
    "id": "topic-color-tone-archive",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "guideline-do-not-bind-color-to-fixed-subject",
    "space": "concept"
   },
   "relation": "cites",
   "to": {
    "id": "ref-reference-x-vol1-color",
    "space": "resource"
   }
  },
  {
   "from": {
    "id": "guideline-do-not-bind-color-to-fixed-subject",
    "space": "concept"
   },
   "relation": "requires",
   "to": {
    "id": "guideline-reference-images-are-tonal-evidence-not-assets",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "pattern-tone-archive-preserves-transferability",
    "space": "concept"
   },
   "relation": "belongs_to_topic",
   "to": {
    "id": "topic-color-tone-archive",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "pattern-tone-archive-preserves-transferability",
    "space": "concept"
   },
   "relation": "cites",
   "to": {
    "id": "ref-reference-x-vol1-color",
    "space": "resource"
   }
  },
  {
   "from": {
    "id": "pattern-tone-archive-preserves-transferability",
    "space": "concept"
   },
   "relation": "requires",
   "to": {
    "id": "guideline-do-not-bind-color-to-fixed-subject",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "pattern-tone-archive-preserves-transferability",
    "space": "concept"
   },
   "relation": "requires",
   "to": {
    "id": "pattern-tone-archive-reference-image-roles",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "guideline-sample-images-validate-method-not-content",
    "space": "concept"
   },
   "relation": "belongs_to_topic",
   "to": {
    "id": "topic-color-tone-archive",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "guideline-sample-images-validate-method-not-content",
    "space": "concept"
   },
   "relation": "cites",
   "to": {
    "id": "ref-reference-x-vol1-color",
    "space": "resource"
   }
  },
  {
   "from": {
    "id": "guideline-sample-images-validate-method-not-content",
    "space": "concept"
   },
   "relation": "requires",
   "to": {
    "id": "guideline-do-not-bind-color-to-fixed-subject",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "heuristic-samples-validate-usage-grammar-not-every-keyword",
    "space": "concept"
   },
   "relation": "belongs_to_topic",
   "to": {
    "id": "topic-color-tone-archive",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "heuristic-samples-validate-usage-grammar-not-every-keyword",
    "space": "concept"
   },
   "relation": "cites",
   "to": {
    "id": "ref-reference-x-vol1-color",
    "space": "resource"
   }
  },
  {
   "from": {
    "id": "heuristic-samples-validate-usage-grammar-not-every-keyword",
    "space": "concept"
   },
   "relation": "requires",
   "to": {
    "id": "pattern-color-keyword-to-tone-archive",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "layer-color-reference-x-v1",
    "space": "resource"
   },
   "relation": "contains",
   "to": {
    "id": "topic-color-tone-archive",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "heuristic-keyword-image-use-over-hex-fill",
    "space": "concept"
   },
   "relation": "belongs_to_topic",
   "to": {
    "id": "topic-color-tone-archive",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "heuristic-keyword-image-use-over-hex-fill",
    "space": "concept"
   },
   "relation": "cites",
   "to": {
    "id": "ref-reference-x-vol1-color",
    "space": "resource"
   }
  },
  {
   "from": {
    "id": "guideline-anchor-color-is-not-flat-fill",
    "space": "concept"
   },
   "relation": "belongs_to_topic",
   "to": {
    "id": "topic-color-tone-archive",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "guideline-anchor-color-is-not-flat-fill",
    "space": "concept"
   },
   "relation": "cites",
   "to": {
    "id": "ref-reference-x-vol1-color",
    "space": "resource"
   }
  },
  {
   "from": {
    "id": "guideline-anchor-color-is-not-flat-fill",
    "space": "concept"
   },
   "relation": "pairs_well_with",
   "to": {
    "id": "guideline-color-values-are-reference-not-absolute",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "guideline-reference-images-are-tonal-evidence-not-assets",
    "space": "concept"
   },
   "relation": "belongs_to_topic",
   "to": {
    "id": "topic-color-tone-archive",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "guideline-reference-images-are-tonal-evidence-not-assets",
    "space": "concept"
   },
   "relation": "cites",
   "to": {
    "id": "ref-reference-x-vol1-color",
    "space": "resource"
   }
  },
  {
   "from": {
    "id": "pattern-color-keyword-to-tone-archive",
    "space": "concept"
   },
   "relation": "belongs_to_topic",
   "to": {
    "id": "topic-color-tone-archive",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "pattern-color-keyword-to-tone-archive",
    "space": "concept"
   },
   "relation": "cites",
   "to": {
    "id": "ref-reference-x-vol1-color",
    "space": "resource"
   }
  },
  {
   "from": {
    "id": "pattern-color-keyword-to-tone-archive",
    "space": "concept"
   },
   "relation": "requires",
   "to": {
    "id": "heuristic-keyword-image-use-over-hex-fill",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "pattern-color-keyword-to-tone-archive",
    "space": "concept"
   },
   "relation": "requires",
   "to": {
    "id": "guideline-anchor-color-is-not-flat-fill",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "pattern-color-keyword-to-tone-archive",
    "space": "concept"
   },
   "relation": "requires",
   "to": {
    "id": "pattern-tonal-ramp-from-anchor-hex",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "pattern-color-keyword-to-tone-archive",
    "space": "concept"
   },
   "relation": "requires",
   "to": {
    "id": "pattern-tone-archive-reference-image-roles",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "pattern-tone-archive-reference-image-roles",
    "space": "concept"
   },
   "relation": "belongs_to_topic",
   "to": {
    "id": "topic-color-tone-archive",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "pattern-tone-archive-reference-image-roles",
    "space": "concept"
   },
   "relation": "cites",
   "to": {
    "id": "ref-reference-x-vol1-color",
    "space": "resource"
   }
  },
  {
   "from": {
    "id": "pattern-tone-archive-reference-image-roles",
    "space": "concept"
   },
   "relation": "requires",
   "to": {
    "id": "guideline-reference-images-are-tonal-evidence-not-assets",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "pattern-tonal-ramp-from-anchor-hex",
    "space": "concept"
   },
   "relation": "belongs_to_topic",
   "to": {
    "id": "topic-color-tone-archive",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "pattern-tonal-ramp-from-anchor-hex",
    "space": "concept"
   },
   "relation": "cites",
   "to": {
    "id": "ref-reference-x-vol1-color",
    "space": "resource"
   }
  },
  {
   "from": {
    "id": "pattern-tonal-ramp-from-anchor-hex",
    "space": "concept"
   },
   "relation": "requires",
   "to": {
    "id": "guideline-anchor-color-is-not-flat-fill",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "topic-color-ui-neutral-ramp",
    "space": "concept"
   },
   "relation": "cites",
   "to": {
    "id": "ref-ui-neutral-ramp-contrast-derived",
    "space": "resource"
   }
  },
  {
   "from": {
    "id": "policy-ui-neutral-ramp-temperature-follows-brand",
    "space": "concept"
   },
   "relation": "belongs_to_topic",
   "to": {
    "id": "topic-color-ui-neutral-ramp",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "policy-ui-neutral-ramp-contrast-before-taste",
    "space": "concept"
   },
   "relation": "belongs_to_topic",
   "to": {
    "id": "topic-color-ui-neutral-ramp",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "color-keyword-ui-neutral-warm-paper",
    "space": "concept"
   },
   "relation": "belongs_to_topic",
   "to": {
    "id": "topic-color-ui-neutral-ramp",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "color-keyword-ui-neutral-warm-paper",
    "space": "concept"
   },
   "relation": "cites",
   "to": {
    "id": "ref-ui-neutral-ramp-contrast-derived",
    "space": "resource"
   }
  },
  {
   "from": {
    "id": "color-keyword-ui-neutral-warm-veil",
    "space": "concept"
   },
   "relation": "belongs_to_topic",
   "to": {
    "id": "topic-color-ui-neutral-ramp",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "color-keyword-ui-neutral-warm-veil",
    "space": "concept"
   },
   "relation": "cites",
   "to": {
    "id": "ref-ui-neutral-ramp-contrast-derived",
    "space": "resource"
   }
  },
  {
   "from": {
    "id": "color-keyword-ui-neutral-warm-line",
    "space": "concept"
   },
   "relation": "belongs_to_topic",
   "to": {
    "id": "topic-color-ui-neutral-ramp",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "color-keyword-ui-neutral-warm-line",
    "space": "concept"
   },
   "relation": "cites",
   "to": {
    "id": "ref-ui-neutral-ramp-contrast-derived",
    "space": "resource"
   }
  },
  {
   "from": {
    "id": "color-keyword-ui-neutral-warm-edge",
    "space": "concept"
   },
   "relation": "belongs_to_topic",
   "to": {
    "id": "topic-color-ui-neutral-ramp",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "color-keyword-ui-neutral-warm-edge",
    "space": "concept"
   },
   "relation": "cites",
   "to": {
    "id": "ref-ui-neutral-ramp-contrast-derived",
    "space": "resource"
   }
  },
  {
   "from": {
    "id": "color-keyword-ui-neutral-warm-muted",
    "space": "concept"
   },
   "relation": "belongs_to_topic",
   "to": {
    "id": "topic-color-ui-neutral-ramp",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "color-keyword-ui-neutral-warm-muted",
    "space": "concept"
   },
   "relation": "cites",
   "to": {
    "id": "ref-ui-neutral-ramp-contrast-derived",
    "space": "resource"
   }
  },
  {
   "from": {
    "id": "color-keyword-ui-neutral-warm-ink",
    "space": "concept"
   },
   "relation": "belongs_to_topic",
   "to": {
    "id": "topic-color-ui-neutral-ramp",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "color-keyword-ui-neutral-warm-ink",
    "space": "concept"
   },
   "relation": "cites",
   "to": {
    "id": "ref-ui-neutral-ramp-contrast-derived",
    "space": "resource"
   }
  },
  {
   "from": {
    "id": "color-keyword-ui-neutral-cool-paper",
    "space": "concept"
   },
   "relation": "belongs_to_topic",
   "to": {
    "id": "topic-color-ui-neutral-ramp",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "color-keyword-ui-neutral-cool-paper",
    "space": "concept"
   },
   "relation": "cites",
   "to": {
    "id": "ref-ui-neutral-ramp-contrast-derived",
    "space": "resource"
   }
  },
  {
   "from": {
    "id": "color-keyword-ui-neutral-cool-veil",
    "space": "concept"
   },
   "relation": "belongs_to_topic",
   "to": {
    "id": "topic-color-ui-neutral-ramp",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "color-keyword-ui-neutral-cool-veil",
    "space": "concept"
   },
   "relation": "cites",
   "to": {
    "id": "ref-ui-neutral-ramp-contrast-derived",
    "space": "resource"
   }
  },
  {
   "from": {
    "id": "color-keyword-ui-neutral-cool-line",
    "space": "concept"
   },
   "relation": "belongs_to_topic",
   "to": {
    "id": "topic-color-ui-neutral-ramp",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "color-keyword-ui-neutral-cool-line",
    "space": "concept"
   },
   "relation": "cites",
   "to": {
    "id": "ref-ui-neutral-ramp-contrast-derived",
    "space": "resource"
   }
  },
  {
   "from": {
    "id": "color-keyword-ui-neutral-cool-edge",
    "space": "concept"
   },
   "relation": "belongs_to_topic",
   "to": {
    "id": "topic-color-ui-neutral-ramp",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "color-keyword-ui-neutral-cool-edge",
    "space": "concept"
   },
   "relation": "cites",
   "to": {
    "id": "ref-ui-neutral-ramp-contrast-derived",
    "space": "resource"
   }
  },
  {
   "from": {
    "id": "color-keyword-ui-neutral-cool-muted",
    "space": "concept"
   },
   "relation": "belongs_to_topic",
   "to": {
    "id": "topic-color-ui-neutral-ramp",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "color-keyword-ui-neutral-cool-muted",
    "space": "concept"
   },
   "relation": "cites",
   "to": {
    "id": "ref-ui-neutral-ramp-contrast-derived",
    "space": "resource"
   }
  },
  {
   "from": {
    "id": "color-keyword-ui-neutral-cool-ink",
    "space": "concept"
   },
   "relation": "belongs_to_topic",
   "to": {
    "id": "topic-color-ui-neutral-ramp",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "color-keyword-ui-neutral-cool-ink",
    "space": "concept"
   },
   "relation": "cites",
   "to": {
    "id": "ref-ui-neutral-ramp-contrast-derived",
    "space": "resource"
   }
  },
  {
   "from": {
    "id": "color-keyword-ui-neutral-true-paper",
    "space": "concept"
   },
   "relation": "belongs_to_topic",
   "to": {
    "id": "topic-color-ui-neutral-ramp",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "color-keyword-ui-neutral-true-paper",
    "space": "concept"
   },
   "relation": "cites",
   "to": {
    "id": "ref-ui-neutral-ramp-contrast-derived",
    "space": "resource"
   }
  },
  {
   "from": {
    "id": "color-keyword-ui-neutral-true-veil",
    "space": "concept"
   },
   "relation": "belongs_to_topic",
   "to": {
    "id": "topic-color-ui-neutral-ramp",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "color-keyword-ui-neutral-true-veil",
    "space": "concept"
   },
   "relation": "cites",
   "to": {
    "id": "ref-ui-neutral-ramp-contrast-derived",
    "space": "resource"
   }
  },
  {
   "from": {
    "id": "color-keyword-ui-neutral-true-line",
    "space": "concept"
   },
   "relation": "belongs_to_topic",
   "to": {
    "id": "topic-color-ui-neutral-ramp",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "color-keyword-ui-neutral-true-line",
    "space": "concept"
   },
   "relation": "cites",
   "to": {
    "id": "ref-ui-neutral-ramp-contrast-derived",
    "space": "resource"
   }
  },
  {
   "from": {
    "id": "color-keyword-ui-neutral-true-edge",
    "space": "concept"
   },
   "relation": "belongs_to_topic",
   "to": {
    "id": "topic-color-ui-neutral-ramp",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "color-keyword-ui-neutral-true-edge",
    "space": "concept"
   },
   "relation": "cites",
   "to": {
    "id": "ref-ui-neutral-ramp-contrast-derived",
    "space": "resource"
   }
  },
  {
   "from": {
    "id": "color-keyword-ui-neutral-true-muted",
    "space": "concept"
   },
   "relation": "belongs_to_topic",
   "to": {
    "id": "topic-color-ui-neutral-ramp",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "color-keyword-ui-neutral-true-muted",
    "space": "concept"
   },
   "relation": "cites",
   "to": {
    "id": "ref-ui-neutral-ramp-contrast-derived",
    "space": "resource"
   }
  },
  {
   "from": {
    "id": "color-keyword-ui-neutral-true-ink",
    "space": "concept"
   },
   "relation": "belongs_to_topic",
   "to": {
    "id": "topic-color-ui-neutral-ramp",
    "space": "concept"
   }
  },
  {
   "from": {
    "id": "color-keyword-ui-neutral-true-ink",
    "space": "concept"
   },
   "relation": "cites",
   "to": {
    "id": "ref-ui-neutral-ramp-contrast-derived",
    "space": "resource"
   }
  }
 ],
 "node_count": 380,
 "nodes": [
  {
   "id": "ref-pantone-coy-announcements",
   "properties": {
    "copyright_handling": "공개 발표된 연도/이름/코드/근사 HEX 사실만 저장. PMS 전체 swatch 라이브러리는 라이선스 자산이므로 import하지 않는다.",
    "hex_basis": "Pantone 색은 물리 잉크 기준이므로 HEX/RGB는 화면 표시용 근사값이다.",
    "ingested_at": "2026-06-11",
    "label": "Pantone Color of the Year 공개 발표 (2000-2026)",
    "source_format": "public_web_announcements",
    "status": "cataloged",
    "url": "https://www.pantone.com/color-of-the-year"
   },
   "space": "resource",
   "type": "ColorReference"
  },
  {
   "id": "topic-color-pantone-trend",
   "properties": {
    "label": "Pantone Trend — Color of the Year 연표",
    "status": "cataloged",
    "summary": "Pantone Color of the Year 2000-2026 공개 연표를 시대별 트렌드 컬러 anchor로 보관하는 topic."
   },
   "space": "concept",
   "type": "ColorTopic"
  },
  {
   "id": "system-pantone-matching-system",
   "properties": {
    "label": "Pantone Matching System (PMS/TCX) spot color system",
    "source_reference_id": "ref-pantone-coy-announcements",
    "status": "cataloged",
    "summary": "Pantone은 그래픽용 PMS(C/U)와 패션/홈용 TCX/TPX 번호 체계를 가진 상용 spot color 시스템이다. swatch 라이브러리 전체는 라이선스 자산이며, 이 도메인은 공개 발표 사실(COY 등)만 카드화한다."
   },
   "space": "concept",
   "type": "ColorSystem"
  },
  {
   "id": "guideline-pantone-library-no-wholesale-import",
   "properties": {
    "label": "Pantone 라이브러리는 wholesale import하지 않는다",
    "source_reference_id": "ref-pantone-coy-announcements",
    "status": "cataloged",
    "summary": "PMS/TCX 전체 swatch 데이터(수천 색의 코드/값 표)는 Pantone의 라이선스 자산이다. palette abstraction policy와 같은 기준으로, 공개 발표 사실(Color of the Year, 공개 트렌드 리포트의 대표색)만 출처와 함께 카드화하고 전체 라이브러리 복제는 금지한다."
   },
   "space": "concept",
   "type": "ColorGuideline"
  },
  {
   "id": "guideline-pantone-hex-screen-approximation",
   "properties": {
    "label": "Pantone HEX는 화면 근사값이다",
    "source_reference_id": "ref-pantone-coy-announcements",
    "status": "cataloged",
    "summary": "Pantone 색의 정의는 물리 잉크/원단 기준이므로 카드의 HEX/RGB는 화면 표시용 근사값이다. 정확한 재현이 필요한 인쇄/생산은 공식 swatch와 매체별 proof로 확인한다."
   },
   "space": "concept",
   "type": "ColorGuideline"
  },
  {
   "id": "heuristic-trend-color-reads-with-era-context",
   "properties": {
    "label": "트렌드 컬러는 시대 맥락과 함께 읽는다",
    "method_only_abstraction": true,
    "source_pages_pdf": [
     310,
     311
    ],
    "source_reference_id": "ref-reference-x-vol1-color",
    "status": "cataloged",
    "summary": "REFERENCE X 4장(컬러 활용)은 트렌드 컬러를 연도 구간별 주목도와 기술/사회 배경, 산업 적용과 함께 읽는 방법을 보여준다. 이 카드는 그 읽기 방법만 추상화하며, 책의 시대별 분석 테이블 자체는 복제하지 않는다."
   },
   "space": "concept",
   "type": "ColorHeuristic"
  },
  {
   "id": "pattern-coy-timeline-as-era-anchor",
   "properties": {
    "label": "연도별 트렌드 질문은 COY 연표를 anchor로 쓴다",
    "source_reference_id": "ref-pantone-coy-announcements",
    "status": "cataloged",
    "summary": "특정 연도/시대의 트렌드 컬러 질문에는 paid source의 분석 테이블을 재현하는 대신 공개 Pantone Color of the Year 연표를 anchor로 쓰고, 적용 판단은 mood/medium caveat와 함께 답한다."
   },
   "space": "concept",
   "type": "ColorPattern"
  },
  {
   "id": "color-keyword-pantone-coy-2000-cerulean",
   "properties": {
    "applies_when": {
     "medium": [
      "digital",
      "print",
      "branding",
      "any"
     ],
     "spectrum": [
      "blue",
      "any"
     ]
    },
    "category": "Pantone Color of the Year",
    "color_name": "Cerulean",
    "coy_year": 2000,
    "family": "pantone_trend",
    "hex_basis": "public announcement screen approximation",
    "label": "Cerulean (Pantone COY 2000)",
    "not_a_rule": true,
    "pantone_code": "15-4020",
    "rgb_hex": "#9BB7D6",
    "source_reference_id": "ref-pantone-coy-announcements",
    "spectrum": "blue",
    "status": "cataloged",
    "summary": "PANTONE 15-4020 Cerulean is the publicly announced Pantone Color of the Year 2000. HEX is a screen approximation of a physical-ink standard. 책의 Cerulean keyword(#2A52BE, Standard Blues)와 이름은 같지만 좌표가 다른 별개 anchor다."
   },
   "space": "concept",
   "type": "ColorKeyword"
  },
  {
   "id": "color-keyword-pantone-coy-2001-fuchsia-rose",
   "properties": {
    "applies_when": {
     "medium": [
      "digital",
      "print",
      "branding",
      "any"
     ],
     "spectrum": [
      "red",
      "any"
     ]
    },
    "category": "Pantone Color of the Year",
    "color_name": "Fuchsia Rose",
    "coy_year": 2001,
    "family": "pantone_trend",
    "hex_basis": "public announcement screen approximation",
    "label": "Fuchsia Rose (Pantone COY 2001)",
    "not_a_rule": true,
    "pantone_code": "17-2031",
    "rgb_hex": "#C94476",
    "source_reference_id": "ref-pantone-coy-announcements",
    "spectrum": "red",
    "status": "cataloged",
    "summary": "PANTONE 17-2031 Fuchsia Rose is the publicly announced Pantone Color of the Year 2001. HEX is a screen approximation of a physical-ink standard."
   },
   "space": "concept",
   "type": "ColorKeyword"
  },
  {
   "id": "color-keyword-pantone-coy-2002-true-red",
   "properties": {
    "applies_when": {
     "medium": [
      "digital",
      "print",
      "branding",
      "any"
     ],
     "spectrum": [
      "red",
      "any"
     ]
    },
    "category": "Pantone Color of the Year",
    "color_name": "True Red",
    "coy_year": 2002,
    "family": "pantone_trend",
    "hex_basis": "public announcement screen approximation",
    "label": "True Red (Pantone COY 2002)",
    "not_a_rule": true,
    "pantone_code": "19-1664",
    "rgb_hex": "#C02034",
    "source_reference_id": "ref-pantone-coy-announcements",
    "spectrum": "red",
    "status": "cataloged",
    "summary": "PANTONE 19-1664 True Red is the publicly announced Pantone Color of the Year 2002. HEX is a screen approximation of a physical-ink standard."
   },
   "space": "concept",
   "type": "ColorKeyword"
  },
  {
   "id": "color-keyword-pantone-coy-2003-aqua-sky",
   "properties": {
    "applies_when": {
     "medium": [
      "digital",
      "print",
      "branding",
      "any"
     ],
     "spectrum": [
      "blue",
      "any"
     ]
    },
    "category": "Pantone Color of the Year",
    "color_name": "Aqua Sky",
    "coy_year": 2003,
    "family": "pantone_trend",
    "hex_basis": "public announcement screen approximation",
    "label": "Aqua Sky (Pantone COY 2003)",
    "not_a_rule": true,
    "pantone_code": "14-4811",
    "rgb_hex": "#7AC5C5",
    "source_reference_id": "ref-pantone-coy-announcements",
    "spectrum": "blue",
    "status": "cataloged",
    "summary": "PANTONE 14-4811 Aqua Sky is the publicly announced Pantone Color of the Year 2003. HEX is a screen approximation of a physical-ink standard."
   },
   "space": "concept",
   "type": "ColorKeyword"
  },
  {
   "id": "color-keyword-pantone-coy-2004-tigerlily",
   "properties": {
    "applies_when": {
     "medium": [
      "digital",
      "print",
      "branding",
      "any"
     ],
     "spectrum": [
      "orange",
      "any"
     ]
    },
    "category": "Pantone Color of the Year",
    "color_name": "Tigerlily",
    "coy_year": 2004,
    "family": "pantone_trend",
    "hex_basis": "public announcement screen approximation",
    "label": "Tigerlily (Pantone COY 2004)",
    "not_a_rule": true,
    "pantone_code": "17-1456",
    "rgb_hex": "#E4583E",
    "source_reference_id": "ref-pantone-coy-announcements",
    "spectrum": "orange",
    "status": "cataloged",
    "summary": "PANTONE 17-1456 Tigerlily is the publicly announced Pantone Color of the Year 2004. HEX is a screen approximation of a physical-ink standard."
   },
   "space": "concept",
   "type": "ColorKeyword"
  },
  {
   "id": "color-keyword-pantone-coy-2005-blue-turquoise",
   "properties": {
    "applies_when": {
     "medium": [
      "digital",
      "print",
      "branding",
      "any"
     ],
     "spectrum": [
      "blue",
      "any"
     ]
    },
    "category": "Pantone Color of the Year",
    "color_name": "Blue Turquoise",
    "coy_year": 2005,
    "family": "pantone_trend",
    "hex_basis": "public announcement screen approximation",
    "label": "Blue Turquoise (Pantone COY 2005)",
    "not_a_rule": true,
    "pantone_code": "15-5217",
    "rgb_hex": "#4FB0AE",
    "source_reference_id": "ref-pantone-coy-announcements",
    "spectrum": "blue",
    "status": "cataloged",
    "summary": "PANTONE 15-5217 Blue Turquoise is the publicly announced Pantone Color of the Year 2005. HEX is a screen approximation of a physical-ink standard."
   },
   "space": "concept",
   "type": "ColorKeyword"
  },
  {
   "id": "color-keyword-pantone-coy-2006-sand-dollar",
   "properties": {
    "applies_when": {
     "medium": [
      "digital",
      "print",
      "branding",
      "any"
     ],
     "spectrum": [
      "yellow",
      "any"
     ]
    },
    "category": "Pantone Color of the Year",
    "color_name": "Sand Dollar",
    "coy_year": 2006,
    "family": "pantone_trend",
    "hex_basis": "public announcement screen approximation",
    "label": "Sand Dollar (Pantone COY 2006)",
    "not_a_rule": true,
    "pantone_code": "13-1106",
    "rgb_hex": "#DECDBF",
    "source_reference_id": "ref-pantone-coy-announcements",
    "spectrum": "yellow",
    "status": "cataloged",
    "summary": "PANTONE 13-1106 Sand Dollar is the publicly announced Pantone Color of the Year 2006. HEX is a screen approximation of a physical-ink standard."
   },
   "space": "concept",
   "type": "ColorKeyword"
  },
  {
   "id": "color-keyword-pantone-coy-2007-chili-pepper",
   "properties": {
    "applies_when": {
     "medium": [
      "digital",
      "print",
      "branding",
      "any"
     ],
     "spectrum": [
      "red",
      "any"
     ]
    },
    "category": "Pantone Color of the Year",
    "color_name": "Chili Pepper",
    "coy_year": 2007,
    "family": "pantone_trend",
    "hex_basis": "public announcement screen approximation",
    "label": "Chili Pepper (Pantone COY 2007)",
    "not_a_rule": true,
    "pantone_code": "19-1557",
    "rgb_hex": "#9C1B31",
    "source_reference_id": "ref-pantone-coy-announcements",
    "spectrum": "red",
    "status": "cataloged",
    "summary": "PANTONE 19-1557 Chili Pepper is the publicly announced Pantone Color of the Year 2007. HEX is a screen approximation of a physical-ink standard."
   },
   "space": "concept",
   "type": "ColorKeyword"
  },
  {
   "id": "color-keyword-pantone-coy-2008-blue-iris",
   "properties": {
    "applies_when": {
     "medium": [
      "digital",
      "print",
      "branding",
      "any"
     ],
     "spectrum": [
      "violet",
      "any"
     ]
    },
    "category": "Pantone Color of the Year",
    "color_name": "Blue Iris",
    "coy_year": 2008,
    "family": "pantone_trend",
    "hex_basis": "public announcement screen approximation",
    "label": "Blue Iris (Pantone COY 2008)",
    "not_a_rule": true,
    "pantone_code": "18-3943",
    "rgb_hex": "#595CA1",
    "source_reference_id": "ref-pantone-coy-announcements",
    "spectrum": "violet",
    "status": "cataloged",
    "summary": "PANTONE 18-3943 Blue Iris is the publicly announced Pantone Color of the Year 2008. HEX is a screen approximation of a physical-ink standard."
   },
   "space": "concept",
   "type": "ColorKeyword"
  },
  {
   "id": "color-keyword-pantone-coy-2009-mimosa",
   "properties": {
    "applies_when": {
     "medium": [
      "digital",
      "print",
      "branding",
      "any"
     ],
     "spectrum": [
      "yellow",
      "any"
     ]
    },
    "category": "Pantone Color of the Year",
    "color_name": "Mimosa",
    "coy_year": 2009,
    "family": "pantone_trend",
    "hex_basis": "public announcement screen approximation",
    "label": "Mimosa (Pantone COY 2009)",
    "not_a_rule": true,
    "pantone_code": "14-0848",
    "rgb_hex": "#F0BF59",
    "source_reference_id": "ref-pantone-coy-announcements",
    "spectrum": "yellow",
    "status": "cataloged",
    "summary": "PANTONE 14-0848 Mimosa is the publicly announced Pantone Color of the Year 2009. HEX is a screen approximation of a physical-ink standard."
   },
   "space": "concept",
   "type": "ColorKeyword"
  },
  {
   "id": "color-keyword-pantone-coy-2010-turquoise",
   "properties": {
    "applies_when": {
     "medium": [
      "digital",
      "print",
      "branding",
      "any"
     ],
     "spectrum": [
      "blue",
      "any"
     ]
    },
    "category": "Pantone Color of the Year",
    "color_name": "Turquoise",
    "coy_year": 2010,
    "family": "pantone_trend",
    "hex_basis": "public announcement screen approximation",
    "label": "Turquoise (Pantone COY 2010)",
    "not_a_rule": true,
    "pantone_code": "15-5519",
    "rgb_hex": "#41B6AB",
    "source_reference_id": "ref-pantone-coy-announcements",
    "spectrum": "blue",
    "status": "cataloged",
    "summary": "PANTONE 15-5519 Turquoise is the publicly announced Pantone Color of the Year 2010. HEX is a screen approximation of a physical-ink standard."
   },
   "space": "concept",
   "type": "ColorKeyword"
  },
  {
   "id": "color-keyword-pantone-coy-2011-honeysuckle",
   "properties": {
    "applies_when": {
     "medium": [
      "digital",
      "print",
      "branding",
      "any"
     ],
     "spectrum": [
      "red",
      "any"
     ]
    },
    "category": "Pantone Color of the Year",
    "color_name": "Honeysuckle",
    "coy_year": 2011,
    "family": "pantone_trend",
    "hex_basis": "public announcement screen approximation",
    "label": "Honeysuckle (Pantone COY 2011)",
    "not_a_rule": true,
    "pantone_code": "18-2120",
    "rgb_hex": "#DA4F70",
    "source_reference_id": "ref-pantone-coy-announcements",
    "spectrum": "red",
    "status": "cataloged",
    "summary": "PANTONE 18-2120 Honeysuckle is the publicly announced Pantone Color of the Year 2011. HEX is a screen approximation of a physical-ink standard."
   },
   "space": "concept",
   "type": "ColorKeyword"
  },
  {
   "id": "color-keyword-pantone-coy-2012-tangerine-tango",
   "properties": {
    "applies_when": {
     "medium": [
      "digital",
      "print",
      "branding",
      "any"
     ],
     "spectrum": [
      "orange",
      "any"
     ]
    },
    "category": "Pantone Color of the Year",
    "color_name": "Tangerine Tango",
    "coy_year": 2012,
    "family": "pantone_trend",
    "hex_basis": "public announcement screen approximation",
    "label": "Tangerine Tango (Pantone COY 2012)",
    "not_a_rule": true,
    "pantone_code": "17-1463",
    "rgb_hex": "#F05442",
    "source_reference_id": "ref-pantone-coy-announcements",
    "spectrum": "orange",
    "status": "cataloged",
    "summary": "PANTONE 17-1463 Tangerine Tango is the publicly announced Pantone Color of the Year 2012. HEX is a screen approximation of a physical-ink standard."
   },
   "space": "concept",
   "type": "ColorKeyword"
  },
  {
   "id": "color-keyword-pantone-coy-2013-emerald",
   "properties": {
    "applies_when": {
     "medium": [
      "digital",
      "print",
      "branding",
      "any"
     ],
     "spectrum": [
      "green",
      "any"
     ]
    },
    "category": "Pantone Color of the Year",
    "color_name": "Emerald",
    "coy_year": 2013,
    "family": "pantone_trend",
    "hex_basis": "public announcement screen approximation",
    "label": "Emerald (Pantone COY 2013)",
    "not_a_rule": true,
    "pantone_code": "17-5641",
    "rgb_hex": "#009473",
    "source_reference_id": "ref-pantone-coy-announcements",
    "spectrum": "green",
    "status": "cataloged",
    "summary": "PANTONE 17-5641 Emerald is the publicly announced Pantone Color of the Year 2013. HEX is a screen approximation of a physical-ink standard."
   },
   "space": "concept",
   "type": "ColorKeyword"
  },
  {
   "id": "color-keyword-pantone-coy-2014-radiant-orchid",
   "properties": {
    "applies_when": {
     "medium": [
      "digital",
      "print",
      "branding",
      "any"
     ],
     "spectrum": [
      "violet",
      "any"
     ]
    },
    "category": "Pantone Color of the Year",
    "color_name": "Radiant Orchid",
    "coy_year": 2014,
    "family": "pantone_trend",
    "hex_basis": "public announcement screen approximation",
    "label": "Radiant Orchid (Pantone COY 2014)",
    "not_a_rule": true,
    "pantone_code": "18-3224",
    "rgb_hex": "#B565A7",
    "source_reference_id": "ref-pantone-coy-announcements",
    "spectrum": "violet",
    "status": "cataloged",
    "summary": "PANTONE 18-3224 Radiant Orchid is the publicly announced Pantone Color of the Year 2014. HEX is a screen approximation of a physical-ink standard."
   },
   "space": "concept",
   "type": "ColorKeyword"
  },
  {
   "id": "color-keyword-pantone-coy-2015-marsala",
   "properties": {
    "applies_when": {
     "medium": [
      "digital",
      "print",
      "branding",
      "any"
     ],
     "spectrum": [
      "red",
      "any"
     ]
    },
    "category": "Pantone Color of the Year",
    "color_name": "Marsala",
    "coy_year": 2015,
    "family": "pantone_trend",
    "hex_basis": "public announcement screen approximation",
    "label": "Marsala (Pantone COY 2015)",
    "not_a_rule": true,
    "pantone_code": "18-1438",
    "rgb_hex": "#955251",
    "source_reference_id": "ref-pantone-coy-announcements",
    "spectrum": "red",
    "status": "cataloged",
    "summary": "PANTONE 18-1438 Marsala is the publicly announced Pantone Color of the Year 2015. HEX is a screen approximation of a physical-ink standard."
   },
   "space": "concept",
   "type": "ColorKeyword"
  },
  {
   "id": "color-keyword-pantone-coy-2016-rose-quartz",
   "properties": {
    "applies_when": {
     "medium": [
      "digital",
      "print",
      "branding",
      "any"
     ],
     "spectrum": [
      "red",
      "any"
     ]
    },
    "category": "Pantone Color of the Year",
    "color_name": "Rose Quartz",
    "coy_year": 2016,
    "family": "pantone_trend",
    "hex_basis": "public announcement screen approximation",
    "label": "Rose Quartz (Pantone COY 2016)",
    "not_a_rule": true,
    "pantone_code": "13-1520",
    "rgb_hex": "#F7CAC9",
    "source_reference_id": "ref-pantone-coy-announcements",
    "spectrum": "red",
    "status": "cataloged",
    "summary": "PANTONE 13-1520 Rose Quartz is the publicly announced Pantone Color of the Year 2016. HEX is a screen approximation of a physical-ink standard."
   },
   "space": "concept",
   "type": "ColorKeyword"
  },
  {
   "id": "color-keyword-pantone-coy-2016-serenity",
   "properties": {
    "applies_when": {
     "medium": [
      "digital",
      "print",
      "branding",
      "any"
     ],
     "spectrum": [
      "blue",
      "any"
     ]
    },
    "category": "Pantone Color of the Year",
    "color_name": "Serenity",
    "coy_year": 2016,
    "family": "pantone_trend",
    "hex_basis": "public announcement screen approximation",
    "label": "Serenity (Pantone COY 2016)",
    "not_a_rule": true,
    "pantone_code": "15-3919",
    "rgb_hex": "#92A8D1",
    "source_reference_id": "ref-pantone-coy-announcements",
    "spectrum": "blue",
    "status": "cataloged",
    "summary": "PANTONE 15-3919 Serenity is the publicly announced Pantone Color of the Year 2016. HEX is a screen approximation of a physical-ink standard."
   },
   "space": "concept",
   "type": "ColorKeyword"
  },
  {
   "id": "color-keyword-pantone-coy-2017-greenery",
   "properties": {
    "applies_when": {
     "medium": [
      "digital",
      "print",
      "branding",
      "any"
     ],
     "spectrum": [
      "green",
      "any"
     ]
    },
    "category": "Pantone Color of the Year",
    "color_name": "Greenery",
    "coy_year": 2017,
    "family": "pantone_trend",
    "hex_basis": "public announcement screen approximation",
    "label": "Greenery (Pantone COY 2017)",
    "not_a_rule": true,
    "pantone_code": "15-0343",
    "rgb_hex": "#88B04B",
    "source_reference_id": "ref-pantone-coy-announcements",
    "spectrum": "green",
    "status": "cataloged",
    "summary": "PANTONE 15-0343 Greenery is the publicly announced Pantone Color of the Year 2017. HEX is a screen approximation of a physical-ink standard."
   },
   "space": "concept",
   "type": "ColorKeyword"
  },
  {
   "id": "color-keyword-pantone-coy-2018-ultra-violet",
   "properties": {
    "applies_when": {
     "medium": [
      "digital",
      "print",
      "branding",
      "any"
     ],
     "spectrum": [
      "violet",
      "any"
     ]
    },
    "category": "Pantone Color of the Year",
    "color_name": "Ultra Violet",
    "coy_year": 2018,
    "family": "pantone_trend",
    "hex_basis": "public announcement screen approximation",
    "label": "Ultra Violet (Pantone COY 2018)",
    "not_a_rule": true,
    "pantone_code": "18-3838",
    "rgb_hex": "#5F4B8B",
    "source_reference_id": "ref-pantone-coy-announcements",
    "spectrum": "violet",
    "status": "cataloged",
    "summary": "PANTONE 18-3838 Ultra Violet is the publicly announced Pantone Color of the Year 2018. HEX is a screen approximation of a physical-ink standard."
   },
   "space": "concept",
   "type": "ColorKeyword"
  },
  {
   "id": "color-keyword-pantone-coy-2019-living-coral",
   "properties": {
    "applies_when": {
     "medium": [
      "digital",
      "print",
      "branding",
      "any"
     ],
     "spectrum": [
      "orange",
      "any"
     ]
    },
    "category": "Pantone Color of the Year",
    "color_name": "Living Coral",
    "coy_year": 2019,
    "family": "pantone_trend",
    "hex_basis": "public announcement screen approximation",
    "label": "Living Coral (Pantone COY 2019)",
    "not_a_rule": true,
    "pantone_code": "16-1546",
    "rgb_hex": "#FF6F61",
    "source_reference_id": "ref-pantone-coy-announcements",
    "spectrum": "orange",
    "status": "cataloged",
    "summary": "PANTONE 16-1546 Living Coral is the publicly announced Pantone Color of the Year 2019. HEX is a screen approximation of a physical-ink standard."
   },
   "space": "concept",
   "type": "ColorKeyword"
  },
  {
   "id": "color-keyword-pantone-coy-2020-classic-blue",
   "properties": {
    "applies_when": {
     "medium": [
      "digital",
      "print",
      "branding",
      "any"
     ],
     "spectrum": [
      "blue",
      "any"
     ]
    },
    "category": "Pantone Color of the Year",
    "color_name": "Classic Blue",
    "coy_year": 2020,
    "family": "pantone_trend",
    "hex_basis": "public announcement screen approximation",
    "label": "Classic Blue (Pantone COY 2020)",
    "not_a_rule": true,
    "pantone_code": "19-4052",
    "rgb_hex": "#0F4C81",
    "source_reference_id": "ref-pantone-coy-announcements",
    "spectrum": "blue",
    "status": "cataloged",
    "summary": "PANTONE 19-4052 Classic Blue is the publicly announced Pantone Color of the Year 2020. HEX is a screen approximation of a physical-ink standard."
   },
   "space": "concept",
   "type": "ColorKeyword"
  },
  {
   "id": "color-keyword-pantone-coy-2021-ultimate-gray",
   "properties": {
    "applies_when": {
     "medium": [
      "digital",
      "print",
      "branding",
      "any"
     ],
     "spectrum": [
      "neutral",
      "any"
     ]
    },
    "category": "Pantone Color of the Year",
    "color_name": "Ultimate Gray",
    "coy_year": 2021,
    "family": "pantone_trend",
    "hex_basis": "public announcement screen approximation",
    "label": "Ultimate Gray (Pantone COY 2021)",
    "not_a_rule": true,
    "pantone_code": "17-5104",
    "rgb_hex": "#939597",
    "source_reference_id": "ref-pantone-coy-announcements",
    "spectrum": "neutral",
    "status": "cataloged",
    "summary": "PANTONE 17-5104 Ultimate Gray is the publicly announced Pantone Color of the Year 2021. HEX is a screen approximation of a physical-ink standard."
   },
   "space": "concept",
   "type": "ColorKeyword"
  },
  {
   "id": "color-keyword-pantone-coy-2021-illuminating",
   "properties": {
    "applies_when": {
     "medium": [
      "digital",
      "print",
      "branding",
      "any"
     ],
     "spectrum": [
      "yellow",
      "any"
     ]
    },
    "category": "Pantone Color of the Year",
    "color_name": "Illuminating",
    "coy_year": 2021,
    "family": "pantone_trend",
    "hex_basis": "public announcement screen approximation",
    "label": "Illuminating (Pantone COY 2021)",
    "not_a_rule": true,
    "pantone_code": "13-0647",
    "rgb_hex": "#F5DF4D",
    "source_reference_id": "ref-pantone-coy-announcements",
    "spectrum": "yellow",
    "status": "cataloged",
    "summary": "PANTONE 13-0647 Illuminating is the publicly announced Pantone Color of the Year 2021. HEX is a screen approximation of a physical-ink standard."
   },
   "space": "concept",
   "type": "ColorKeyword"
  },
  {
   "id": "color-keyword-pantone-coy-2022-very-peri",
   "properties": {
    "applies_when": {
     "medium": [
      "digital",
      "print",
      "branding",
      "any"
     ],
     "spectrum": [
      "violet",
      "any"
     ]
    },
    "category": "Pantone Color of the Year",
    "color_name": "Very Peri",
    "coy_year": 2022,
    "family": "pantone_trend",
    "hex_basis": "public announcement screen approximation",
    "label": "Very Peri (Pantone COY 2022)",
    "not_a_rule": true,
    "pantone_code": "17-3938",
    "rgb_hex": "#6667AB",
    "source_reference_id": "ref-pantone-coy-announcements",
    "spectrum": "violet",
    "status": "cataloged",
    "summary": "PANTONE 17-3938 Very Peri is the publicly announced Pantone Color of the Year 2022. HEX is a screen approximation of a physical-ink standard."
   },
   "space": "concept",
   "type": "ColorKeyword"
  },
  {
   "id": "color-keyword-pantone-coy-2023-viva-magenta",
   "properties": {
    "applies_when": {
     "medium": [
      "digital",
      "print",
      "branding",
      "any"
     ],
     "spectrum": [
      "red",
      "any"
     ]
    },
    "category": "Pantone Color of the Year",
    "color_name": "Viva Magenta",
    "coy_year": 2023,
    "family": "pantone_trend",
    "hex_basis": "public announcement screen approximation",
    "label": "Viva Magenta (Pantone COY 2023)",
    "not_a_rule": true,
    "pantone_code": "18-1750",
    "rgb_hex": "#BB2649",
    "source_reference_id": "ref-pantone-coy-announcements",
    "spectrum": "red",
    "status": "cataloged",
    "summary": "PANTONE 18-1750 Viva Magenta is the publicly announced Pantone Color of the Year 2023. HEX is a screen approximation of a physical-ink standard."
   },
   "space": "concept",
   "type": "ColorKeyword"
  },
  {
   "id": "color-keyword-pantone-coy-2024-peach-fuzz",
   "properties": {
    "applies_when": {
     "medium": [
      "digital",
      "print",
      "branding",
      "any"
     ],
     "spectrum": [
      "orange",
      "any"
     ]
    },
    "category": "Pantone Color of the Year",
    "color_name": "Peach Fuzz",
    "coy_year": 2024,
    "family": "pantone_trend",
    "hex_basis": "public announcement screen approximation",
    "label": "Peach Fuzz (Pantone COY 2024)",
    "not_a_rule": true,
    "pantone_code": "13-1023",
    "rgb_hex": "#FFBE98",
    "source_reference_id": "ref-pantone-coy-announcements",
    "spectrum": "orange",
    "status": "cataloged",
    "summary": "PANTONE 13-1023 Peach Fuzz is the publicly announced Pantone Color of the Year 2024. HEX is a screen approximation of a physical-ink standard."
   },
   "space": "concept",
   "type": "ColorKeyword"
  },
  {
   "id": "color-keyword-pantone-coy-2025-mocha-mousse",
   "properties": {
    "applies_when": {
     "medium": [
      "digital",
      "print",
      "branding",
      "any"
     ],
     "spectrum": [
      "orange",
      "any"
     ]
    },
    "category": "Pantone Color of the Year",
    "color_name": "Mocha Mousse",
    "coy_year": 2025,
    "family": "pantone_trend",
    "hex_basis": "public announcement screen approximation",
    "label": "Mocha Mousse (Pantone COY 2025)",
    "not_a_rule": true,
    "pantone_code": "17-1230",
    "rgb_hex": "#A47864",
    "source_reference_id": "ref-pantone-coy-announcements",
    "spectrum": "orange",
    "status": "cataloged",
    "summary": "PANTONE 17-1230 Mocha Mousse is the publicly announced Pantone Color of the Year 2025. HEX is a screen approximation of a physical-ink standard."
   },
   "space": "concept",
   "type": "ColorKeyword"
  },
  {
   "id": "color-keyword-pantone-coy-2026-cloud-dancer",
   "properties": {
    "applies_when": {
     "medium": [
      "digital",
      "print",
      "branding",
      "any"
     ],
     "spectrum": [
      "neutral",
      "any"
     ]
    },
    "category": "Pantone Color of the Year",
    "color_name": "Cloud Dancer",
    "coy_year": 2026,
    "family": "pantone_trend",
    "hex_basis": "public announcement screen approximation",
    "label": "Cloud Dancer (Pantone COY 2026)",
    "not_a_rule": true,
    "pantone_code": "11-4201",
    "rgb_hex": "#F0EEE9",
    "source_reference_id": "ref-pantone-coy-announcements",
    "spectrum": "neutral",
    "status": "cataloged",
    "summary": "PANTONE 11-4201 Cloud Dancer is the publicly announced Pantone Color of the Year 2026. HEX is a screen approximation of a physical-ink standard."
   },
   "space": "concept",
   "type": "ColorKeyword"
  },
  {
   "id": "pattern-brief-palette-deep-blue-cold-luxury-web",
   "properties": {
    "brief_match_terms": [
     "딥",
     "블루",
     "blue",
     "luxury",
     "웹",
     "website"
    ],
    "brief_match_weight": 8,
    "brief_question": "딥 블루 계열로 차갑고 고급스러운 브랜드 웹사이트를 만들되, 바다나 물로 고정하지 않고 색 사용 방식만 살린다.",
    "contrast_reasons": [
     "Navy Blue to Ice Blue creates high value contrast without leaving the cool spectrum.",
     "Prussian Blue and Classic Blue keep mood continuity while separating depth from interaction surfaces.",
     "Ice Blue acts as material light rather than a new subject cue."
    ],
    "example_source": "ref-reference-x-vol1-color",
    "label": "딥 블루 cold luxury 웹 팔레트 후보",
    "not_a_rule": true,
    "output_medium": "digital_brand_website",
    "palette_roles": [
     "anchor_background: Navy Blue #000080 — low-value base, trust, authority, restrained elegance",
     "depth_support: Prussian Blue #003153 — lowered-chroma depth for editorial panels and shadowed sections",
     "interface_surface: Classic Blue #0F4C81 — active surface, nav affordance, and calm intelligent signal",
     "highlight_air: Ice Blue #D6EAF8 — thin edge highlights, glass lines, and spacing breath"
    ],
    "prompt_avoid": [
     "Do not claim this palette appears as a row in the source.",
     "Do not copy page order, source images, or palette table layout."
    ],
    "prompt_do": [
     "Use Navy Blue as the deep base and keep Ice Blue as narrow light, not large fill.",
     "Separate Prussian Blue shadow panels from Classic Blue interactive emphasis.",
     "Describe materials as matte ceramic, brushed metal, frosted glass, and architectural shadow."
    ],
    "proof_caveats": [
     "This is an sRGB/digital-screen candidate, not a CMYK print proof.",
     "Avoid sea/water/literal night-sky imagery; keep the palette in surface, material, depth, and light behavior.",
     "Check contrast ratios if used for body text or small UI labels."
    ],
    "role_model": "brief_specific_candidate_not_source_row",
    "source_protection_checks": [
     "not_source_table_row",
     "role_reason_caveat_present",
     "no_page_order_or_table_structure",
     "low_volume_policy_test"
    ],
    "status": "cataloged",
    "summary": "딥 블루 계열 브랜드 웹사이트 brief를 위해 Navy Blue, Prussian Blue, Classic Blue, Ice Blue를 source row가 아니라 화면 역할과 대비 이유로 재배치한 테스트 팔레트다.",
    "topic": "topic-color-palette-abstraction-policy"
   },
   "space": "concept",
   "type": "ColorPattern"
  },
  {
   "id": "pattern-brief-palette-stable-green-ui-surface",
   "properties": {
    "brief_match_terms": [
     "그린",
     "green",
     "서비스",
     "service",
     "ui"
    ],
    "brief_match_weight": 8,
    "brief_question": "서비스 UI에서 그린 계열을 자연 사진처럼 따라하지 않고 안정적인 표면 톤으로 쓴다.",
    "contrast_reasons": [
     "Forest Green and Celadon provide value separation while keeping a stable green identity.",
     "Bottle Green adds structural depth; Arcadia adds a small modern signal without turning the UI into nature imagery.",
     "Cascade softens transitions between deep surfaces and pale panels."
    ],
    "example_source": "ref-reference-x-vol1-color",
    "label": "안정적인 그린 서비스 UI 팔레트 후보",
    "not_a_rule": true,
    "output_medium": "digital_service_ui",
    "palette_roles": [
     "anchor_surface: Forest Green #27503D — grounded primary surface and trust depth",
     "structural_support: Bottle Green #006A4E — restrained header/sidebar depth without blackening the interface",
     "quiet_background: Celadon #ACE1AF — muted soft field for empty states or calm panels",
     "calm_border: Cascade #76C1B1 — low-chroma boundary, tag, and secondary surface",
     "fresh_accent: Arcadia #00A591 — limited action accent for progress, success, or selected states"
    ],
    "prompt_avoid": [
     "Do not turn the palette into a rule that green requires nature photography.",
     "Do not claim this palette appears as a source table row."
    ],
    "prompt_do": [
     "Treat greens as surface hierarchy: deep anchor, structural support, quiet background, accent.",
     "Keep Arcadia small and functional so the palette remains stable rather than decorative.",
     "Use Celadon and Cascade for low-pressure fields, separators, and calm state changes."
    ],
    "proof_caveats": [
     "This is an interface tone candidate; accessibility contrast must be checked per component.",
     "Do not infer that green means plants, forest photography, wellness imagery, or any fixed subject.",
     "CMYK conversion is not covered by this UI candidate."
    ],
    "role_model": "brief_specific_candidate_not_source_row",
    "source_protection_checks": [
     "not_source_table_row",
     "role_reason_caveat_present",
     "no_page_order_or_table_structure",
     "low_volume_policy_test"
    ],
    "status": "cataloged",
    "summary": "자연 사진을 따라 하지 않는 서비스 UI brief를 위해 Forest Green, Bottle Green, Celadon, Cascade, Arcadia를 표면 역할과 대비 이유로 재배치한 테스트 팔레트다.",
    "topic": "topic-color-palette-abstraction-policy"
   },
   "space": "concept",
   "type": "ColorPattern"
  },
  {
   "id": "pattern-brief-palette-manga-magazine-pop-editorial",
   "properties": {
    "brief_match_terms": [
     "만화",
     "매거진",
     "웹진",
     "manga",
     "magazine",
     "comic",
     "editorial"
    ],
    "brief_match_weight": 10,
    "brief_question": "만화 매거진 사이트를 만들되 색상 샘플의 피사체나 원본 조합표를 따라 하지 않고, 에디토리얼 리듬과 연재 탐색 UX로 번역한다.",
    "contrast_reasons": [
     "Pure Red and Scarlet create high-chroma editorial urgency but stay in small structural zones rather than filling every panel.",
     "Buttercream keeps the reading field warm and light so dense comic cards do not collapse into noise.",
     "Ultra Violet gives feature depth, while Illuminating works only as a limited flash for issue labels and rankings."
    ],
    "example_source": "ref-reference-x-vol1-color",
    "label": "만화 매거진 팝 에디토리얼 팔레트 후보",
    "not_a_rule": true,
    "output_medium": "digital_manga_magazine",
    "palette_roles": [
     "masthead_energy: Pure Red #FF0000 — high-impact masthead stripe and issue urgency",
     "cover_signal: Scarlet #FF2400 — kinetic tabs, issue stamps, and hover states",
     "paper_field: Buttercream #F3E5AB — warm page field that keeps dense panels readable",
     "feature_frame: Ultra Violet #5F4B8B — editorial depth for feature blocks and serialized title panels",
     "attention_flash: Illuminating #F5DF4D — small callout bursts, rank labels, and release flags"
    ],
    "prompt_avoid": [
     "Do not claim this palette appears as a source table row.",
     "Do not make manga magazine equal to any fixed color rule or copied IP style."
    ],
    "prompt_do": [
     "Treat bright colors as editorial rhythm for masthead, ranking labels, tabs, and cover calls.",
     "Keep the reading surface warm and calm enough for many issue cards and chapter rows.",
     "Use custom abstract panels, speed lines, and speech shapes instead of copying manga characters or source images."
    ],
    "proof_caveats": [
     "This is a digital editorial candidate; print magazine proofing would need separate CMYK and paper tests.",
     "Do not infer that manga magazine design must always be red/yellow/violet; this is one pop-editorial test.",
     "Do not copy source page order, source combinations, or manga IP imagery."
    ],
    "role_model": "brief_specific_candidate_not_source_row",
    "source_protection_checks": [
     "not_source_table_row",
     "role_reason_caveat_present",
     "no_page_order_or_table_structure",
     "low_volume_policy_test"
    ],
    "status": "cataloged",
    "summary": "만화 매거진 사이트 brief를 위해 Pure Red, Scarlet, Buttercream, Ultra Violet, Illuminating을 원본 조합표가 아니라 masthead, cover, page field, feature frame, attention flash 역할로 재배치한 테스트 팔레트다.",
    "topic": "topic-color-palette-abstraction-policy"
   },
   "space": "concept",
   "type": "ColorPattern"
  },
  {
   "id": "pattern-brief-palette-coy-mocha-warm-editorial",
   "properties": {
    "brief_match_terms": [
     "모카",
     "mocha",
     "무스",
     "mousse",
     "포트폴리오",
     "portfolio",
     "올해의",
     "coy",
     "연도 무드"
    ],
    "brief_match_weight": 12,
    "brief_question": "2025년 모카 무스 무드의 따뜻한 에디토리얼 포트폴리오 웹사이트를 만들되, 커피나 디저트 사진으로 고정하지 않고 색 사용 방식만 살린다.",
    "contrast_reasons": [
     "Mocha Mousse to Cornsilk creates a soft value ramp that keeps the warm spectrum continuous from base to light.",
     "Copper separates structural depth from Terracotta interaction emphasis without leaving the warm-mineral mood.",
     "Cornsilk behaves as material paper light rather than a coffee or dessert subject cue."
    ],
    "coy_anchor": "color-keyword-pantone-coy-2025-mocha-mousse",
    "example_source": "ref-reference-x-vol1-color",
    "extended_keyword_anchors": [
     "color-keyword-ext-sandstone",
     "color-keyword-ext-dune",
     "color-keyword-ext-maple"
    ],
    "label": "COY 2025 모카 무스 warm editorial 웹 팔레트 후보",
    "not_a_rule": true,
    "output_medium": "digital_editorial_portfolio_website",
    "palette_roles": [
     "anchor_background: Mocha Mousse #A47864 — warm mineral base, grounded comfort, year-mood anchor (Pantone COY 2025, screen-approximate hex)",
     "depth_support: Copper #B87333 — metallic editorial depth for rules, frames, and section breaks",
     "interface_surface: Terracotta #E2725B — warm interactive emphasis for links, tags, and hover states",
     "highlight_air: Cornsilk #FFF8DC — paper light field for reading surfaces and spacing breath"
    ],
    "prompt_avoid": [
     "Do not claim this palette appears as a row in the source or as an official Pantone palette.",
     "Do not bind the year mood to coffee, chocolate, or dessert subjects.",
     "Do not present the COY hex as print-accurate; print work needs official swatch proof."
    ],
    "prompt_do": [
     "Use Mocha Mousse as the dominant grounded base and keep Cornsilk as wide reading light, not as a competing accent.",
     "Treat Copper as thin metallic structure (rules, frames, numerals) and Terracotta as the single interaction voice.",
     "Use name-only extended keywords Sandstone, Dune, Maple as texture and reference-search anchors, not as new hex values."
    ],
    "proof_caveats": [
     "This is an sRGB/digital-screen candidate; the Mocha Mousse hex is a public screen approximation of a physical Pantone standard, not an official digital coordinate.",
     "Avoid literal coffee/dessert/latte imagery; keep the palette in material, paper, light, and shadow behavior.",
     "Check contrast ratios before placing small body text on Terracotta or Copper surfaces."
    ],
    "role_model": "brief_specific_candidate_not_source_row",
    "source_protection_checks": [
     "not_source_table_row",
     "role_reason_caveat_present",
     "no_page_order_or_table_structure",
     "low_volume_policy_test"
    ],
    "status": "cataloged",
    "summary": "2025년 Pantone COY Mocha Mousse를 연도 무드 anchor로 두고, 책의 Copper/Terracotta/Cornsilk를 source row가 아니라 화면 역할과 대비 이유로 재배치한 연도 무드 기반 테스트 팔레트다. name-only extended keyword(Sandstone/Dune/Maple)는 텍스처/레퍼런스 검색 anchor로만 쓴다.",
    "topic": "topic-color-palette-abstraction-policy"
   },
   "space": "concept",
   "type": "ColorPattern"
  },
  {
   "id": "guideline-color-brief-design-novelty",
   "properties": {
    "applies_when": {
     "medium": [
      "digital",
      "any"
     ]
    },
    "label": "생성 사이트 샘플은 정책 증거이지 디자인 템플릿이 아니다",
    "source": "user feedback 2026-06-13 — 샘플은 참고사항이고 매번 새롭게",
    "status": "cataloged",
    "summary": "기존 generated brief artifacts(prototypes/*)는 palette abstraction policy를 통과한 증거 사례일 뿐이다. 새 브리프마다 그 브리프만의 미학 방향(톤, 타이포그래피, 레이아웃 콘셉트)을 먼저 새로 선언하고 설계한다. 기존 샘플 레이아웃 재사용은 사용자가 명시적으로 요청할 때만 한다. 온톨로지 계약(role/reason/caveat, contrast pairs, source 보호)은 유지하되 시각 디자인을 결정하지 않는다."
   },
   "space": "concept",
   "type": "ColorGuideline"
  },
  {
   "id": "pattern-brief-palette-midnight-listening-lounge",
   "properties": {
    "brief_match_terms": [
     "리스닝",
     "라운지",
     "심야",
     "lounge",
     "listening",
     "바이닐",
     "vinyl",
     "음악 감상"
    ],
    "brief_match_weight": 12,
    "brief_question": "심야 리스닝 라운지 웹사이트를 만들되, 클럽/네온으로 흐르지 않고 조용한 음악 감상 공간의 밤 공기와 램프 불빛만 살린다.",
    "contrast_reasons": [
     "Lavender Mist text on Midnight Violet (12.59) and Byzantium keeps the night mood while staying readable.",
     "Honey Gold is the only warm voice — one lamp in a violet room — so interaction cues stay unmistakable.",
     "Dark ink on Honey Gold and Lavender Mist surfaces separates action/light areas from the night ground."
    ],
    "design_mode": "fresh_per_brief",
    "example_source": "ref-reference-x-vol1-color",
    "label": "심야 리스닝 라운지 웹 팔레트 후보",
    "not_a_rule": true,
    "output_medium": "digital_listening_lounge_website",
    "palette_roles": [
     "anchor_background: Midnight Violet #2E1A47 — quiet night base, interior depth, restrained emotion",
     "depth_support: Byzantium #702963 — rich poster panels, session highlights, artistic depth",
     "interface_surface: Honey Gold #DDB67D — single warm lamp-light accent for actions, reservations, and now-playing cues",
     "highlight_air: Lavender Mist #E6E6FA — dreamlike pale light for body text and breathing space on dark ground"
    ],
    "prompt_avoid": [
     "Do not claim this palette appears as a row in the source.",
     "Do not bind the palette to neon club or DJ-culture subjects.",
     "Do not reuse prior prototype layouts; design is authored fresh per brief."
    ],
    "prompt_do": [
     "Keep Midnight Violet as the dominant night ground and let Lavender Mist behave as moonlit air, not large flat fill.",
     "Use Honey Gold sparingly as the single warm interaction voice (buttons, now-playing, reservation).",
     "Declare a fresh aesthetic direction for this brief; existing prototypes are policy evidence, not templates."
    ],
    "proof_caveats": [
     "This is an sRGB/digital-screen candidate, not a CMYK print proof.",
     "Avoid neon-club, DJ-booth, or literal vinyl-record-photo cliches as fixed subjects; keep the palette in air, lamp light, and surface behavior.",
     "Check contrast ratios again if Honey Gold is used under small body text."
    ],
    "role_model": "brief_specific_candidate_not_source_row",
    "source_protection_checks": [
     "not_source_table_row",
     "role_reason_caveat_present",
     "no_page_order_or_table_structure",
     "low_volume_policy_test"
    ],
    "status": "cataloged",
    "summary": "심야 리스닝 라운지(음악 감상 바) 웹사이트용 브리프를 위해 Midnight Violet, Byzantium, Honey Gold, Lavender Mist를 source row가 아니라 화면 역할과 대비 이유로 재배치한 테스트 팔레트다. 바이올렛 밤공기 위에 램프 불빛 하나만 warm 액센트로 두는 cross-spectrum 구성.",
    "topic": "topic-color-palette-abstraction-policy"
   },
   "space": "concept",
   "type": "ColorPattern"
  },
  {
   "id": "pattern-brief-palette-aquarium-depth-descent",
   "properties": {
    "brief_match_terms": [
     "아쿠아리움",
     "aquarium",
     "수족관",
     "해양",
     "심해",
     "해저",
     "ocean",
     "marine",
     "deep sea",
     "발광",
     "바다 생물"
    ],
    "brief_match_weight": 12,
    "brief_question": "아쿠아리움 랜딩페이지를 만들되, 파란 그라데이션과 물고기 일러스트 클리셰로 흐르지 않고 수심이 내려가는 빛의 변화와 발광 생물의 시안만 살린다.",
    "contrast_reasons": [
     "Ice Blue text on Prussian Blue (11.83) and Classic Blue (7.80) holds the underwater mood while staying readable.",
     "Blue Atoll is the only luminous voice — one bioluminescent glow in dark water — so interaction cues stay unmistakable (dark text 7.30).",
     "Depth is shown by the value drop from Ice Blue surface to Prussian Blue abyss, not by a literal blue-to-blue gradient cliche."
    ],
    "design_mode": "fresh_per_brief",
    "example_source": "ref-reference-x-vol1-color",
    "label": "아쿠아리움 수심 하강 랜딩 팔레트 후보",
    "not_a_rule": true,
    "output_medium": "digital_aquarium_landing_page",
    "palette_roles": [
     "anchor_background: Prussian Blue #003153 — abyssal base, deepest tank water, the dark you scroll down into",
     "depth_support: Classic Blue #0F4C81 — mid-water tank glass and gallery panels between surface and abyss",
     "interface_surface: Blue Atoll #00B1D2 — the single bioluminescent cyan accent for tickets, live-feed, and actions",
     "highlight_air: Ice Blue #D6EAF8 — surface light filtering down, body text and breathing space on deep ground"
    ],
    "prompt_avoid": [
     "Do not claim this palette appears as a row in the source.",
     "Do not fall back to flat blue gradients or cartoon-fish crowds.",
     "Do not reuse prior prototype layouts; design is authored fresh per brief."
    ],
    "prompt_do": [
     "Keep Prussian Blue as the abyssal ground and let Ice Blue behave as filtered surface light, not large flat fill.",
     "Use Blue Atoll sparingly as the single bioluminescent interaction voice (tickets, live feed, CTA).",
     "Declare a fresh aesthetic direction for this brief; existing prototypes are policy evidence, not templates."
    ],
    "proof_caveats": [
     "This is an sRGB/digital-screen candidate, not a CMYK print proof.",
     "Avoid cartoon-fish illustration crowds and flat blue gradients as fixed subjects; keep the palette in light, depth, and glass behavior.",
     "Re-check contrast if Blue Atoll is used under small body text."
    ],
    "role_model": "brief_specific_candidate_not_source_row",
    "source_protection_checks": [
     "not_source_table_row",
     "role_reason_caveat_present",
     "no_page_order_or_table_structure",
     "low_volume_policy_test"
    ],
    "status": "cataloged",
    "summary": "아쿠아리움 랜딩페이지를 위해 Prussian Blue, Classic Blue, Blue Atoll, Ice Blue를 source row가 아니라 화면 역할과 대비 이유로 재배치한 테스트 팔레트다. 스크롤로 수면에서 심해로 내려가는 수심 하강을 어두워지는 청색 바닥 + 발광 생물의 시안 한 줄기로 표현하는 구성.",
    "topic": "topic-color-palette-abstraction-policy"
   },
   "space": "concept",
   "type": "ColorPattern"
  },
  {
   "id": "layer-color-reference-x-v1",
   "properties": {
    "ingested_at": "2026-05-17",
    "purpose": "REFERENCE X Vol.1 컬러 자료를 원문 복제가 아닌 색상 정의/키워드/디자인 판단 카드로 추상화한 color 도메인 레이어.",
    "status": "promoted",
    "title": "Color Reference Layer v1"
   },
   "space": "resource",
   "type": "OntologyLayer"
  },
  {
   "id": "ref-reference-x-vol1-color",
   "properties": {
    "copyright_handling": "원문 OCR 전문/페이지 이미지/배색표 전체는 저장소에 커밋하지 않고, 온톨로지에는 페이지 근거가 있는 추상화 결과만 저장.",
    "ingested_at": "2026-05-17",
    "label": "REFERENCE X Vol.1 컬러",
    "page_count": 316,
    "source_format": "image_pdf",
    "status": "cataloged"
   },
   "space": "resource",
   "type": "ColorReference"
  },
  {
   "id": "topic-color-reference-keywords",
   "properties": {
    "core_question": "큰 색상명보다 세밀한 레퍼런스 키워드가 디자인 방향을 어떻게 바꾸는가.",
    "label": "Reference Keywords — 색을 부르는 언어와 검색 관점",
    "not_a_rule": true,
    "status": "cataloged"
   },
   "space": "concept",
   "type": "ColorTopic"
  },
  {
   "id": "topic-color-basic-systems",
   "properties": {
    "core_question": "디지털 화면과 인쇄 매체의 색상 체계를 분리해서 판단한다.",
    "label": "Color Systems — RGB/CMYK/sRGB/print profile",
    "not_a_rule": true,
    "status": "cataloged"
   },
   "space": "concept",
   "type": "ColorTopic"
  },
  {
   "id": "topic-color-emotion-mechanism",
   "properties": {
    "core_question": "색상/명도/채도가 감정 신호로 먼저 작동하는 방식을 다룬다.",
    "label": "Color Emotion Mechanism — 색과 감정의 시각 반응",
    "not_a_rule": true,
    "status": "cataloged"
   },
   "space": "concept",
   "type": "ColorTopic"
  },
  {
   "id": "topic-color-red-spectrum",
   "properties": {
    "core_question": "Standard/Natural/Deep/Pastel/Pantone red keyword archive.",
    "label": "Red Spectrum — 레드 계열 키워드",
    "not_a_rule": true,
    "status": "cataloged"
   },
   "space": "concept",
   "type": "ColorTopic"
  },
  {
   "id": "topic-color-orange-spectrum",
   "properties": {
    "core_question": "Standard/Natural/Deep/Pastel/Pantone orange keyword archive.",
    "label": "Orange Spectrum — 오렌지 계열 키워드",
    "not_a_rule": true,
    "status": "cataloged"
   },
   "space": "concept",
   "type": "ColorTopic"
  },
  {
   "id": "topic-color-yellow-spectrum",
   "properties": {
    "core_question": "Standard/Natural/Deep/Pastel/Pantone yellow keyword archive.",
    "label": "Yellow Spectrum — 옐로 계열 키워드",
    "not_a_rule": true,
    "status": "cataloged"
   },
   "space": "concept",
   "type": "ColorTopic"
  },
  {
   "id": "topic-color-green-spectrum",
   "properties": {
    "core_question": "Standard/Natural/Deep/Pastel/Pantone green keyword archive.",
    "label": "Green Spectrum — 그린 계열 키워드",
    "not_a_rule": true,
    "status": "cataloged"
   },
   "space": "concept",
   "type": "ColorTopic"
  },
  {
   "id": "topic-color-blue-spectrum",
   "properties": {
    "core_question": "Standard/Natural/Deep/Pastel/Pantone blue keyword archive.",
    "label": "Blue Spectrum — 블루 계열 키워드",
    "not_a_rule": true,
    "status": "cataloged"
   },
   "space": "concept",
   "type": "ColorTopic"
  },
  {
   "id": "topic-color-violet-spectrum",
   "properties": {
    "core_question": "Standard/Natural/Deep/Pastel/Pantone violet keyword archive.",
    "label": "Violet Spectrum — 바이올렛 계열 키워드",
    "not_a_rule": true,
    "status": "cataloged"
   },
   "space": "concept",
   "type": "ColorTopic"
  },
  {
   "id": "topic-color-application",
   "properties": {
    "core_question": "컬러 키워드를 브랜딩/디지털/인쇄/패키지/무드보드에 적용하는 판단.",
    "label": "Practical Applications — 트렌드와 변주",
    "not_a_rule": true,
    "status": "cataloged"
   },
   "space": "concept",
   "type": "ColorTopic"
  },
  {
   "id": "system-rgb-additive",
   "properties": {
    "label": "RGB additive color system",
    "not_a_rule": true,
    "output_medium": "digital_screen",
    "source_reference_id": "ref-reference-x-vol1-color",
    "status": "cataloged",
    "summary": "디지털 화면/빛 기반 매체에서 RGB 채널 조합으로 색을 정의한다."
   },
   "space": "concept",
   "type": "ColorSystem"
  },
  {
   "id": "system-cmyk-subtractive",
   "properties": {
    "label": "CMYK subtractive color system",
    "not_a_rule": true,
    "output_medium": "print",
    "source_reference_id": "ref-reference-x-vol1-color",
    "status": "cataloged",
    "summary": "종이/잉크/물리 인쇄 기반 매체에서 CMYK 근삿값으로 색을 관리한다."
   },
   "space": "concept",
   "type": "ColorSystem"
  },
  {
   "id": "system-srgb-reference",
   "properties": {
    "label": "sRGB reference basis",
    "not_a_rule": true,
    "output_medium": "digital_screen",
    "source_reference_id": "ref-reference-x-vol1-color",
    "status": "cataloged",
    "summary": "문서의 RGB 값은 sRGB 기준값으로 다루며 디스플레이마다 차이가 날 수 있다."
   },
   "space": "concept",
   "type": "ColorSystem"
  },
  {
   "id": "system-coated-gracol-2006",
   "properties": {
    "label": "Coated GRACoL 2006 CMYK conversion profile",
    "not_a_rule": true,
    "output_medium": "print",
    "source_reference_id": "ref-reference-x-vol1-color",
    "status": "cataloged",
    "summary": "문서의 CMYK 값은 Coated GRACoL 2006 프로파일 기반 근삿값으로 취급한다."
   },
   "space": "concept",
   "type": "ColorSystem"
  },
  {
   "id": "metric-concept-clarity",
   "properties": {
    "label": "Concept Clarity / 명료도",
    "source_reference_id": "ref-reference-x-vol1-color",
    "status": "cataloged",
    "summary": "색이 전달하는 정체성과 메시지의 명확함."
   },
   "space": "concept",
   "type": "ColorMetric"
  },
  {
   "id": "metric-saturation",
   "properties": {
    "label": "Saturation / 채도",
    "source_reference_id": "ref-reference-x-vol1-color",
    "status": "cataloged",
    "summary": "색의 선명함과 감각적 강도."
   },
   "space": "concept",
   "type": "ColorMetric"
  },
  {
   "id": "metric-symbolism",
   "properties": {
    "label": "Symbolism / 상징성",
    "source_reference_id": "ref-reference-x-vol1-color",
    "status": "cataloged",
    "summary": "색이 지닌 문화적 또는 심리적 의미의 깊이."
   },
   "space": "concept",
   "type": "ColorMetric"
  },
  {
   "id": "metric-trendiness",
   "properties": {
    "label": "Trendiness / 트렌드성",
    "source_reference_id": "ref-reference-x-vol1-color",
    "status": "cataloged",
    "summary": "시대적 흐름과 트렌드에 부합하는 감각적 최신성."
   },
   "space": "concept",
   "type": "ColorMetric"
  },
  {
   "id": "metric-imagery-depth",
   "properties": {
    "label": "Imagery Depth / 심상 깊이",
    "source_reference_id": "ref-reference-x-vol1-color",
    "status": "cataloged",
    "summary": "색이 불러오는 시각적 또는 감정적 이미지의 층위."
   },
   "space": "concept",
   "type": "ColorMetric"
  },
  {
   "id": "metric-versatility",
   "properties": {
    "label": "Versatility / 접목성",
    "source_reference_id": "ref-reference-x-vol1-color",
    "status": "cataloged",
    "summary": "다양한 용도나 매체에 적용 가능한 유연성."
   },
   "space": "concept",
   "type": "ColorMetric"
  },
  {
   "id": "metric-visibility",
   "properties": {
    "label": "Visibility / 가시성",
    "source_reference_id": "ref-reference-x-vol1-color",
    "status": "cataloged",
    "summary": "시각적으로 얼마나 눈에 잘 띄는가."
   },
   "space": "concept",
   "type": "ColorMetric"
  },
  {
   "id": "metric-stability",
   "properties": {
    "label": "Stability / 안정감",
    "source_reference_id": "ref-reference-x-vol1-color",
    "status": "cataloged",
    "summary": "색이 가져다주는 신뢰감과 일관성 유지 정도."
   },
   "space": "concept",
   "type": "ColorMetric"
  },
  {
   "id": "heuristic-reference-keyword-controls-design-direction",
   "properties": {
    "example_source": "ref-reference-x-vol1-color",
    "label": "레퍼런스 키워드가 디자인 방향을 결정한다",
    "not_a_rule": true,
    "source_page_pdf": 5,
    "status": "cataloged",
    "summary": "큰 색상명보다 세밀한 색상 키워드가 검색 결과, 무드, 적용 장면을 바꾼다. 색은 이름 붙이는 순간 디자인 관점이 된다.",
    "topic": "topic-color-reference-keywords"
   },
   "space": "concept",
   "type": "ColorHeuristic"
  },
  {
   "id": "heuristic-color-read-before-form",
   "properties": {
    "example_source": "ref-reference-x-vol1-color",
    "label": "색은 형태보다 먼저 감정 신호로 읽힌다",
    "not_a_rule": true,
    "source_page_pdf": 9,
    "status": "cataloged",
    "summary": "컬러 브리프에서는 형태/레이아웃 설명 전에 색상, 명도, 채도, 온도감이 주는 감정 반응을 먼저 정리한다.",
    "topic": "topic-color-emotion-mechanism"
   },
   "space": "concept",
   "type": "ColorHeuristic"
  },
  {
   "id": "guideline-rgb-cmyk-split-by-output-medium",
   "properties": {
    "example_source": "ref-reference-x-vol1-color",
    "label": "RGB와 CMYK는 산출 매체 기준으로 분리한다",
    "not_a_rule": true,
    "source_page_pdf": 9,
    "status": "cataloged",
    "summary": "디지털 산출물은 RGB/sRGB 기준, 인쇄 산출물은 CMYK/프로파일 기준으로 판단한다. 화면색을 인쇄색으로 그대로 기대하지 않는다.",
    "topic": "topic-color-basic-systems"
   },
   "space": "concept",
   "type": "ColorGuideline"
  },
  {
   "id": "guideline-color-values-are-reference-not-absolute",
   "properties": {
    "example_source": "ref-reference-x-vol1-color",
    "label": "색상 수치는 절댓값이 아니라 기준값이다",
    "not_a_rule": true,
    "source_page_pdf": 9,
    "status": "cataloged",
    "summary": "디스플레이와 출력 환경에 따라 색 차이가 생기므로 HEX/CMYK는 재현 기준점으로 쓰고, 최종 판단은 매체별 proof에서 확인한다.",
    "topic": "topic-color-basic-systems"
   },
   "space": "concept",
   "type": "ColorGuideline"
  },
  {
   "id": "pattern-spectrum-family-keyword-stack",
   "properties": {
    "example_source": "ref-reference-x-vol1-color",
    "label": "스펙트럼 → 패밀리 → 키워드로 색을 좁힌다",
    "not_a_rule": true,
    "source_page_pdf": 5,
    "status": "cataloged",
    "summary": "Red 같은 상위 스펙트럼에서 Standard/Natural/Deep/Pastel/Pantone 계열로 좁힌 뒤, 최종 키워드와 수치값을 선택한다.",
    "topic": "topic-color-reference-keywords"
   },
   "space": "concept",
   "type": "ColorPattern"
  },
  {
   "id": "pattern-color-card-triad-swatch-reading-metrics",
   "properties": {
    "example_source": "ref-reference-x-vol1-color",
    "label": "색상 카드는 swatch, reading, metrics 세 겹으로 읽는다",
    "not_a_rule": true,
    "source_page_pdf": 9,
    "status": "cataloged",
    "summary": "큰 색면과 수치값으로 색을 확인하고, reference reading으로 무드/적용 맥락을 잡은 뒤, 분석 지표로 쓰임새를 비교한다.",
    "topic": "topic-color-application"
   },
   "space": "concept",
   "type": "ColorPattern"
  },
  {
   "id": "guideline-mood-tags-before-palette-expansion",
   "properties": {
    "example_source": "ref-reference-x-vol1-color",
    "label": "팔레트 확장 전 mood tag를 먼저 잠근다",
    "not_a_rule": true,
    "source_page_pdf": 9,
    "status": "cataloged",
    "summary": "무드보드나 브랜드 컬러를 늘리기 전에 에너지, 안정, 깊이, 회복 같은 감정 태그를 먼저 고정하면 색상 후보가 흔들리지 않는다.",
    "topic": "topic-color-emotion-mechanism"
   },
   "space": "concept",
   "type": "ColorGuideline"
  },
  {
   "id": "pattern-color-keyword-to-design-brief",
   "properties": {
    "example_source": "ref-reference-x-vol1-color",
    "label": "컬러 키워드를 디자인 브리프의 검색어로 승격한다",
    "not_a_rule": true,
    "source_page_pdf": 5,
    "status": "cataloged",
    "summary": "색상 키워드를 단순 라벨이 아니라 레퍼런스 검색어, 무드 정의, 적용 매체 조건을 묶는 브리프 단위로 사용한다.",
    "topic": "topic-color-reference-keywords"
   },
   "space": "concept",
   "type": "ColorPattern"
  },
  {
   "id": "color-keyword-pure-red",
   "properties": {
    "applies_when": {
     "color_family": [
      "standard",
      "any"
     ],
     "medium": [
      "digital",
      "print",
      "branding",
      "any"
     ],
     "spectrum": [
      "red",
      "any"
     ]
    },
    "category": "Standard Reds",
    "cmyk": "C 0%, M 95%, Y 96%, K 0%",
    "cmyk_c": 0,
    "cmyk_k": 0,
    "cmyk_m": 95,
    "cmyk_profile": "Coated GRACoL 2006",
    "cmyk_y": 96,
    "extraction_method": "macOS Vision OCR + representative page visual checks; raw OCR not committed",
    "family": "standard",
    "label": "Pure Red",
    "metrics_page_pdf": 17,
    "mood_tags": [
     "열정",
     "에너지",
     "주목성",
     "상징적",
     "강렬함"
    ],
    "not_a_rule": true,
    "reference_reading_page_pdf": 16,
    "rgb_hex": "#FF0000",
    "source_page_pdf": 16,
    "source_reference_id": "ref-reference-x-vol1-color",
    "spectrum": "red",
    "spectrum_label_ko": "레드",
    "status": "cataloged",
    "summary": "Pure Red is a Standard Reds keyword in the red spectrum, defined from REFERENCE X Vol.1 with RGB/CMYK reference values and mood tags.",
    "swatch_page_pdf": 15,
    "tone_axes": [
     "mid_value",
     "high_chroma"
    ]
   },
   "space": "concept",
   "type": "ColorKeyword"
  },
  {
   "id": "color-keyword-scarlet",
   "properties": {
    "applies_when": {
     "color_family": [
      "standard",
      "any"
     ],
     "medium": [
      "digital",
      "print",
      "branding",
      "any"
     ],
     "spectrum": [
      "red",
      "any"
     ]
    },
    "category": "Standard Reds",
    "cmyk": "C 0%, M 91%, Y 96%, K 0%",
    "cmyk_c": 0,
    "cmyk_k": 0,
    "cmyk_m": 91,
    "cmyk_profile": "Coated GRACoL 2006",
    "cmyk_y": 96,
    "extraction_method": "macOS Vision OCR + representative page visual checks; raw OCR not committed",
    "family": "standard",
    "label": "Scarlet",
    "metrics_page_pdf": 20,
    "mood_tags": [
     "활기",
     "생동감",
     "열정",
     "역동성",
     "주목성"
    ],
    "not_a_rule": true,
    "reference_reading_page_pdf": 19,
    "rgb_hex": "#FF2400",
    "source_page_pdf": 19,
    "source_reference_id": "ref-reference-x-vol1-color",
    "spectrum": "red",
    "spectrum_label_ko": "레드",
    "status": "cataloged",
    "summary": "Scarlet is a Standard Reds keyword in the red spectrum, defined from REFERENCE X Vol.1 with RGB/CMYK reference values and mood tags.",
    "swatch_page_pdf": 18,
    "tone_axes": [
     "high_value",
     "high_chroma",
     "warm_bias"
    ]
   },
   "space": "concept",
   "type": "ColorKeyword"
  },
  {
   "id": "color-keyword-crimson",
   "properties": {
    "applies_when": {
     "color_family": [
      "standard",
      "any"
     ],
     "medium": [
      "digital",
      "print",
      "branding",
      "any"
     ],
     "spectrum": [
      "red",
      "any"
     ]
    },
    "category": "Standard Reds",
    "cmyk": "C 20%, M 97%, Y 61%, K 11%",
    "cmyk_c": 20,
    "cmyk_k": 11,
    "cmyk_m": 97,
    "cmyk_profile": "Coated GRACoL 2006",
    "cmyk_y": 61,
    "extraction_method": "macOS Vision OCR + representative page visual checks; raw OCR not committed",
    "family": "standard",
    "label": "Crimson",
    "metrics_page_pdf": 23,
    "mood_tags": [
     "고급스러움",
     "강렬함",
     "감정적",
     "웅장함",
     "고전적"
    ],
    "not_a_rule": true,
    "reference_reading_page_pdf": 22,
    "rgb_hex": "#BD2E4A",
    "source_page_pdf": 22,
    "source_reference_id": "ref-reference-x-vol1-color",
    "spectrum": "red",
    "spectrum_label_ko": "레드",
    "status": "cataloged",
    "summary": "Crimson is a Standard Reds keyword in the red spectrum, defined from REFERENCE X Vol.1 with RGB/CMYK reference values and mood tags.",
    "swatch_page_pdf": 21,
    "tone_axes": [
     "low_value",
     "mid_chroma"
    ]
   },
   "space": "concept",
   "type": "ColorKeyword"
  },
  {
   "id": "color-keyword-ruby",
   "properties": {
    "applies_when": {
     "color_family": [
      "standard",
      "any"
     ],
     "medium": [
      "digital",
      "print",
      "branding",
      "any"
     ],
     "spectrum": [
      "red",
      "any"
     ]
    },
    "category": "Standard Reds",
    "cmyk": "C 11%, M 96%, Y 55%, K 2%",
    "cmyk_c": 11,
    "cmyk_k": 2,
    "cmyk_m": 96,
    "cmyk_profile": "Coated GRACoL 2006",
    "cmyk_y": 55,
    "extraction_method": "macOS Vision OCR + representative page visual checks; raw OCR not committed",
    "family": "standard",
    "label": "Ruby",
    "metrics_page_pdf": 26,
    "mood_tags": [
     "화려함",
     "관능",
     "세련",
     "에너지",
     "주목성"
    ],
    "not_a_rule": true,
    "reference_reading_page_pdf": 25,
    "rgb_hex": "#E11F51",
    "source_page_pdf": 25,
    "source_reference_id": "ref-reference-x-vol1-color",
    "spectrum": "red",
    "spectrum_label_ko": "레드",
    "status": "cataloged",
    "summary": "Ruby is a Standard Reds keyword in the red spectrum, defined from REFERENCE X Vol.1 with RGB/CMYK reference values and mood tags.",
    "swatch_page_pdf": 24,
    "tone_axes": [
     "mid_value",
     "high_chroma"
    ]
   },
   "space": "concept",
   "type": "ColorKeyword"
  },
  {
   "id": "color-keyword-coral-red",
   "properties": {
    "applies_when": {
     "color_family": [
      "natural",
      "any"
     ],
     "medium": [
      "digital",
      "print",
      "branding",
      "any"
     ],
     "spectrum": [
      "red",
      "any"
     ]
    },
    "category": "Natural Reds",
    "cmyk": "C 10%, M 85%, Y 89%, K 0%",
    "cmyk_c": 10,
    "cmyk_k": 0,
    "cmyk_m": 85,
    "cmyk_profile": "Coated GRACoL 2006",
    "cmyk_y": 89,
    "extraction_method": "macOS Vision OCR + representative page visual checks; raw OCR not committed",
    "family": "natural",
    "label": "Coral Red",
    "metrics_page_pdf": 29,
    "mood_tags": [
     "생동감",
     "건강함",
     "자연스러움",
     "긍정적"
    ],
    "not_a_rule": true,
    "reference_reading_page_pdf": 28,
    "rgb_hex": "#E44327",
    "source_page_pdf": 28,
    "source_reference_id": "ref-reference-x-vol1-color",
    "spectrum": "red",
    "spectrum_label_ko": "레드",
    "status": "cataloged",
    "summary": "Coral Red is a Natural Reds keyword in the red spectrum, defined from REFERENCE X Vol.1 with RGB/CMYK reference values and mood tags.",
    "swatch_page_pdf": 27,
    "tone_axes": [
     "warm_bias"
    ]
   },
   "space": "concept",
   "type": "ColorKeyword"
  },
  {
   "id": "color-keyword-terracotta",
   "properties": {
    "applies_when": {
     "color_family": [
      "natural",
      "any"
     ],
     "medium": [
      "digital",
      "print",
      "branding",
      "any"
     ],
     "spectrum": [
      "red",
      "any"
     ]
    },
    "category": "Natural Reds",
    "cmyk": "C 12%, M 66%, Y 62%, K 2%",
    "cmyk_c": 12,
    "cmyk_k": 2,
    "cmyk_m": 66,
    "cmyk_profile": "Coated GRACoL 2006",
    "cmyk_y": 62,
    "extraction_method": "macOS Vision OCR + representative page visual checks; raw OCR not committed",
    "family": "natural",
    "label": "Terracotta",
    "metrics_page_pdf": 32,
    "mood_tags": [
     "안정감",
     "따뜻함",
     "자연스러움",
     "감성적"
    ],
    "not_a_rule": true,
    "reference_reading_page_pdf": 31,
    "rgb_hex": "#E2725B",
    "source_page_pdf": 31,
    "source_reference_id": "ref-reference-x-vol1-color",
    "spectrum": "red",
    "spectrum_label_ko": "레드",
    "status": "cataloged",
    "summary": "Terracotta is a Natural Reds keyword in the red spectrum, defined from REFERENCE X Vol.1 with RGB/CMYK reference values and mood tags.",
    "swatch_page_pdf": 30,
    "tone_axes": [
     "warm_bias",
     "earth_or_wine_bias"
    ]
   },
   "space": "concept",
   "type": "ColorKeyword"
  },
  {
   "id": "color-keyword-rose-red",
   "properties": {
    "applies_when": {
     "color_family": [
      "natural",
      "any"
     ],
     "medium": [
      "digital",
      "print",
      "branding",
      "any"
     ],
     "spectrum": [
      "red",
      "any"
     ]
    },
    "category": "Natural Reds",
    "cmyk": "C 20%, M 99%, Y 45%, K 9%",
    "cmyk_c": 20,
    "cmyk_k": 9,
    "cmyk_m": 99,
    "cmyk_profile": "Coated GRACoL 2006",
    "cmyk_y": 45,
    "extraction_method": "macOS Vision OCR + representative page visual checks; raw OCR not committed",
    "family": "natural",
    "label": "Rose Red",
    "metrics_page_pdf": 35,
    "mood_tags": [
     "로맨틱",
     "감성적",
     "생동감",
     "부드러움"
    ],
    "not_a_rule": true,
    "reference_reading_page_pdf": 34,
    "rgb_hex": "#C21E56",
    "source_page_pdf": 34,
    "source_reference_id": "ref-reference-x-vol1-color",
    "spectrum": "red",
    "spectrum_label_ko": "레드",
    "status": "cataloged",
    "summary": "Rose Red is a Natural Reds keyword in the red spectrum, defined from REFERENCE X Vol.1 with RGB/CMYK reference values and mood tags.",
    "swatch_page_pdf": 33,
    "tone_axes": [
     "mid_value",
     "warm_bias"
    ]
   },
   "space": "concept",
   "type": "ColorKeyword"
  },
  {
   "id": "color-keyword-oxblood",
   "properties": {
    "applies_when": {
     "color_family": [
      "deep",
      "any"
     ],
     "medium": [
      "digital",
      "print",
      "branding",
      "any"
     ],
     "spectrum": [
      "red",
      "any"
     ]
    },
    "category": "Deep Reds",
    "cmyk": "C 45%, M 100%, Y 82%, K 70%",
    "cmyk_c": 45,
    "cmyk_k": 70,
    "cmyk_m": 100,
    "cmyk_profile": "Coated GRACoL 2006",
    "cmyk_y": 82,
    "extraction_method": "macOS Vision OCR + representative page visual checks; raw OCR not committed",
    "family": "deep",
    "label": "Oxblood",
    "metrics_page_pdf": 38,
    "mood_tags": [
     "고급스러움",
     "성숙함",
     "강렬함",
     "깊은 감정"
    ],
    "not_a_rule": true,
    "reference_reading_page_pdf": 37,
    "rgb_hex": "#4A0404",
    "source_page_pdf": 37,
    "source_reference_id": "ref-reference-x-vol1-color",
    "spectrum": "red",
    "spectrum_label_ko": "레드",
    "status": "cataloged",
    "summary": "Oxblood is a Deep Reds keyword in the red spectrum, defined from REFERENCE X Vol.1 with RGB/CMYK reference values and mood tags.",
    "swatch_page_pdf": 36,
    "tone_axes": [
     "low_value",
     "earth_or_wine_bias"
    ]
   },
   "space": "concept",
   "type": "ColorKeyword"
  },
  {
   "id": "color-keyword-claret",
   "properties": {
    "applies_when": {
     "color_family": [
      "deep",
      "any"
     ],
     "medium": [
      "digital",
      "print",
      "branding",
      "any"
     ],
     "spectrum": [
      "red",
      "any"
     ]
    },
    "category": "Deep Reds",
    "cmyk": "C 30%, M 100%, Y 58%, K 40%",
    "cmyk_c": 30,
    "cmyk_k": 40,
    "cmyk_m": 100,
    "cmyk_profile": "Coated GRACoL 2006",
    "cmyk_y": 58,
    "extraction_method": "macOS Vision OCR + representative page visual checks; raw OCR not committed",
    "family": "deep",
    "label": "Claret",
    "metrics_page_pdf": 41,
    "mood_tags": [
     "세련됨",
     "관능적",
     "품격 있는",
     "고급스러운"
    ],
    "not_a_rule": true,
    "reference_reading_page_pdf": 40,
    "rgb_hex": "#7F1734",
    "source_page_pdf": 40,
    "source_reference_id": "ref-reference-x-vol1-color",
    "spectrum": "red",
    "spectrum_label_ko": "레드",
    "status": "cataloged",
    "summary": "Claret is a Deep Reds keyword in the red spectrum, defined from REFERENCE X Vol.1 with RGB/CMYK reference values and mood tags.",
    "swatch_page_pdf": 39,
    "tone_axes": [
     "mid_value",
     "low_value",
     "earth_or_wine_bias"
    ]
   },
   "space": "concept",
   "type": "ColorKeyword"
  },
  {
   "id": "color-keyword-sangria",
   "properties": {
    "applies_when": {
     "color_family": [
      "deep",
      "any"
     ],
     "medium": [
      "digital",
      "print",
      "branding",
      "any"
     ],
     "spectrum": [
      "red",
      "any"
     ]
    },
    "category": "Deep Reds",
    "cmyk": "C 27%, M 100%, Y 44%, K 20%",
    "cmyk_c": 27,
    "cmyk_k": 20,
    "cmyk_m": 100,
    "cmyk_profile": "Coated GRACoL 2006",
    "cmyk_y": 44,
    "extraction_method": "macOS Vision OCR + representative page visual checks; raw OCR not committed",
    "family": "deep",
    "label": "Sangria",
    "metrics_page_pdf": 44,
    "mood_tags": [
     "관능적",
     "생동감 있는",
     "여유로운",
     "감각적"
    ],
    "not_a_rule": true,
    "reference_reading_page_pdf": 43,
    "rgb_hex": "#9C1F4B",
    "source_page_pdf": 43,
    "source_reference_id": "ref-reference-x-vol1-color",
    "spectrum": "red",
    "spectrum_label_ko": "레드",
    "status": "cataloged",
    "summary": "Sangria is a Deep Reds keyword in the red spectrum, defined from REFERENCE X Vol.1 with RGB/CMYK reference values and mood tags.",
    "swatch_page_pdf": 42,
    "tone_axes": [
     "mid_value",
     "low_value",
     "warm_bias",
     "earth_or_wine_bias"
    ]
   },
   "space": "concept",
   "type": "ColorKeyword"
  },
  {
   "id": "color-keyword-salmon",
   "properties": {
    "applies_when": {
     "color_family": [
      "pastel",
      "any"
     ],
     "medium": [
      "digital",
      "print",
      "branding",
      "any"
     ],
     "spectrum": [
      "red",
      "any"
     ]
    },
    "category": "Pastel Reds",
    "cmyk": "C 2%, M 62%, Y 48%, K 0%",
    "cmyk_c": 2,
    "cmyk_k": 0,
    "cmyk_m": 62,
    "cmyk_profile": "Coated GRACoL 2006",
    "cmyk_y": 48,
    "extraction_method": "macOS Vision OCR + representative page visual checks; raw OCR not committed",
    "family": "pastel",
    "label": "Salmon",
    "metrics_page_pdf": 47,
    "mood_tags": [
     "따뜻함",
     "부드러움",
     "친근함",
     "자연스러움"
    ],
    "not_a_rule": true,
    "reference_reading_page_pdf": 46,
    "rgb_hex": "#FA8072",
    "source_page_pdf": 46,
    "source_reference_id": "ref-reference-x-vol1-color",
    "spectrum": "red",
    "spectrum_label_ko": "레드",
    "status": "cataloged",
    "summary": "Salmon is a Pastel Reds keyword in the red spectrum, defined from REFERENCE X Vol.1 with RGB/CMYK reference values and mood tags.",
    "swatch_page_pdf": 45,
    "tone_axes": [
     "high_value",
     "warm_bias",
     "pastel"
    ]
   },
   "space": "concept",
   "type": "ColorKeyword"
  },
  {
   "id": "color-keyword-blush",
   "properties": {
    "applies_when": {
     "color_family": [
      "pastel",
      "any"
     ],
     "medium": [
      "digital",
      "print",
      "branding",
      "any"
     ],
     "spectrum": [
      "red",
      "any"
     ]
    },
    "category": "Pastel Reds",
    "cmyk": "C 2%, M 32%, Y 13%, K 0%",
    "cmyk_c": 2,
    "cmyk_k": 0,
    "cmyk_m": 32,
    "cmyk_profile": "Coated GRACoL 2006",
    "cmyk_y": 13,
    "extraction_method": "macOS Vision OCR + representative page visual checks; raw OCR not committed",
    "family": "pastel",
    "label": "Blush",
    "metrics_page_pdf": 50,
    "mood_tags": [
     "섬세함",
     "순수함",
     "따뜻한 감정",
     "부드러움"
    ],
    "not_a_rule": true,
    "reference_reading_page_pdf": 49,
    "rgb_hex": "#F9C0C4",
    "source_page_pdf": 49,
    "source_reference_id": "ref-reference-x-vol1-color",
    "spectrum": "red",
    "spectrum_label_ko": "레드",
    "status": "cataloged",
    "summary": "Blush is a Pastel Reds keyword in the red spectrum, defined from REFERENCE X Vol.1 with RGB/CMYK reference values and mood tags.",
    "swatch_page_pdf": 48,
    "tone_axes": [
     "high_value",
     "pastel"
    ]
   },
   "space": "concept",
   "type": "ColorKeyword"
  },
  {
   "id": "color-keyword-marsala",
   "properties": {
    "applies_when": {
     "color_family": [
      "pantone_trend",
      "any"
     ],
     "medium": [
      "digital",
      "print",
      "branding",
      "any"
     ],
     "spectrum": [
      "red",
      "any"
     ]
    },
    "category": "Pantone Trend Reds",
    "cmyk": "C 29%, M 72%, Y 59%, K 26%",
    "cmyk_c": 29,
    "cmyk_k": 26,
    "cmyk_m": 72,
    "cmyk_profile": "Coated GRACoL 2006",
    "cmyk_y": 59,
    "extraction_method": "macOS Vision OCR + representative page visual checks; raw OCR not committed",
    "family": "pantone_trend",
    "label": "Marsala",
    "metrics_page_pdf": 53,
    "mood_tags": [
     "성숙함",
     "안정감",
     "관능적",
     "가을",
     "겨울",
     "클래식"
    ],
    "not_a_rule": true,
    "pantone_code": "Pantone 18-1438",
    "reference_reading_page_pdf": 52,
    "rgb_hex": "#964F4C",
    "source_page_pdf": 52,
    "source_reference_id": "ref-reference-x-vol1-color",
    "spectrum": "red",
    "spectrum_label_ko": "레드",
    "status": "cataloged",
    "summary": "Marsala is a Pantone Trend Reds keyword in the red spectrum, defined from REFERENCE X Vol.1 with RGB/CMYK reference values and mood tags.",
    "swatch_page_pdf": 51,
    "tone_axes": [
     "earth_or_wine_bias"
    ]
   },
   "space": "concept",
   "type": "ColorKeyword"
  },
  {
   "id": "color-keyword-grenadine",
   "properties": {
    "applies_when": {
     "color_family": [
      "pantone_trend",
      "any"
     ],
     "medium": [
      "digital",
      "print",
      "branding",
      "any"
     ],
     "spectrum": [
      "red",
      "any"
     ]
    },
    "category": "Pantone Trend Reds",
    "cmyk": "C 13%, M 82%, Y 70%, K 3%",
    "cmyk_c": 13,
    "cmyk_k": 3,
    "cmyk_m": 82,
    "cmyk_profile": "Coated GRACoL 2006",
    "cmyk_y": 70,
    "extraction_method": "macOS Vision OCR + representative page visual checks; raw OCR not committed",
    "family": "pantone_trend",
    "label": "Grenadine",
    "metrics_page_pdf": 56,
    "mood_tags": [
     "활력",
     "열정",
     "관능",
     "현대적"
    ],
    "not_a_rule": true,
    "pantone_code": "Pantone 17-1558",
    "reference_reading_page_pdf": 55,
    "rgb_hex": "#DC4C46",
    "source_page_pdf": 55,
    "source_reference_id": "ref-reference-x-vol1-color",
    "spectrum": "red",
    "spectrum_label_ko": "레드",
    "status": "cataloged",
    "summary": "Grenadine is a Pantone Trend Reds keyword in the red spectrum, defined from REFERENCE X Vol.1 with RGB/CMYK reference values and mood tags.",
    "swatch_page_pdf": 54,
    "tone_axes": [
     "high_value",
     "mid_chroma",
     "warm_bias"
    ]
   },
   "space": "concept",
   "type": "ColorKeyword"
  },
  {
   "id": "color-keyword-goji-berry",
   "properties": {
    "applies_when": {
     "color_family": [
      "pantone_trend",
      "any"
     ],
     "medium": [
      "digital",
      "print",
      "branding",
      "any"
     ],
     "spectrum": [
      "red",
      "any"
     ]
    },
    "category": "Pantone Trend Reds",
    "cmyk": "C 16%, M 100%, Y 80%, K 7%",
    "cmyk_c": 16,
    "cmyk_k": 7,
    "cmyk_m": 100,
    "cmyk_profile": "Coated GRACoL 2006",
    "cmyk_y": 80,
    "extraction_method": "macOS Vision OCR + representative page visual checks; raw OCR not committed",
    "family": "pantone_trend",
    "label": "Goji Berry",
    "metrics_page_pdf": 59,
    "mood_tags": [
     "생기",
     "세련됨",
     "감각적",
     "젊음"
    ],
    "not_a_rule": true,
    "pantone_code": "Pantone 18-1659",
    "reference_reading_page_pdf": 58,
    "rgb_hex": "#CC142F",
    "source_page_pdf": 58,
    "source_reference_id": "ref-reference-x-vol1-color",
    "spectrum": "red",
    "spectrum_label_ko": "레드",
    "status": "cataloged",
    "summary": "Goji Berry is a Pantone Trend Reds keyword in the red spectrum, defined from REFERENCE X Vol.1 with RGB/CMYK reference values and mood tags.",
    "swatch_page_pdf": 57,
    "tone_axes": [
     "mid_value",
     "earth_or_wine_bias"
    ]
   },
   "space": "concept",
   "type": "ColorKeyword"
  },
  {
   "id": "color-keyword-pure-orange",
   "properties": {
    "applies_when": {
     "color_family": [
      "standard",
      "any"
     ],
     "medium": [
      "digital",
      "print",
      "branding",
      "any"
     ],
     "spectrum": [
      "orange",
      "any"
     ]
    },
    "category": "Standard Oranges",
    "cmyk": "C 0%, M 42%, Y 94%, K 0%",
    "cmyk_c": 0,
    "cmyk_k": 0,
    "cmyk_m": 42,
    "cmyk_profile": "Coated GRACoL 2006",
    "cmyk_y": 94,
    "extraction_method": "macOS Vision OCR + representative page visual checks; raw OCR not committed",
    "family": "standard",
    "label": "Pure Orange",
    "metrics_page_pdf": 69,
    "mood_tags": [
     "활력",
     "낙관",
     "따뜻함",
     "개방감"
    ],
    "not_a_rule": true,
    "reference_reading_page_pdf": 68,
    "rgb_hex": "#FFA500",
    "source_page_pdf": 68,
    "source_reference_id": "ref-reference-x-vol1-color",
    "spectrum": "orange",
    "spectrum_label_ko": "오렌지",
    "status": "cataloged",
    "summary": "Pure Orange is a Standard Oranges keyword in the orange spectrum, defined from REFERENCE X Vol.1 with RGB/CMYK reference values and mood tags.",
    "swatch_page_pdf": 67,
    "tone_axes": [
     "mid_value",
     "high_chroma",
     "warm_bias"
    ]
   },
   "space": "concept",
   "type": "ColorKeyword"
  },
  {
   "id": "color-keyword-tangerine",
   "properties": {
    "applies_when": {
     "color_family": [
      "standard",
      "any"
     ],
     "medium": [
      "digital",
      "print",
      "branding",
      "any"
     ],
     "spectrum": [
      "orange",
      "any"
     ]
    },
    "category": "Standard Oranges",
    "cmyk": "C 5%, M 97%, Y 98%, K 0%",
    "cmyk_c": 5,
    "cmyk_k": 0,
    "cmyk_m": 97,
    "cmyk_profile": "Coated GRACoL 2006",
    "cmyk_y": 98,
    "extraction_method": "macOS Vision OCR + representative page visual checks; raw OCR not committed",
    "family": "standard",
    "label": "Tangerine",
    "metrics_page_pdf": 72,
    "mood_tags": [
     "따뜻함",
     "에너지",
     "활기",
     "긍정적 낙관"
    ],
    "not_a_rule": true,
    "reference_reading_page_pdf": 71,
    "rgb_hex": "#F28500",
    "source_page_pdf": 71,
    "source_reference_id": "ref-reference-x-vol1-color",
    "spectrum": "orange",
    "spectrum_label_ko": "오렌지",
    "status": "cataloged",
    "summary": "Tangerine is a Standard Oranges keyword in the orange spectrum, defined from REFERENCE X Vol.1 with RGB/CMYK reference values and mood tags.",
    "swatch_page_pdf": 70,
    "tone_axes": [
     "mid_value",
     "high_chroma",
     "warm_bias"
    ]
   },
   "space": "concept",
   "type": "ColorKeyword"
  },
  {
   "id": "color-keyword-ochre",
   "properties": {
    "applies_when": {
     "color_family": [
      "standard",
      "any"
     ],
     "medium": [
      "digital",
      "print",
      "branding",
      "any"
     ],
     "spectrum": [
      "orange",
      "any"
     ]
    },
    "category": "Standard Oranges",
    "cmyk": "C 18%, M 60%, Y 94%, K 6%",
    "cmyk_c": 18,
    "cmyk_k": 6,
    "cmyk_m": 60,
    "cmyk_profile": "Coated GRACoL 2006",
    "cmyk_y": 94,
    "extraction_method": "macOS Vision OCR + representative page visual checks; raw OCR not committed",
    "family": "standard",
    "label": "Ochre",
    "metrics_page_pdf": 75,
    "mood_tags": [
     "안정감",
     "내추럴",
     "신뢰감",
     "지속성"
    ],
    "not_a_rule": true,
    "reference_reading_page_pdf": 74,
    "rgb_hex": "#CC7722",
    "source_page_pdf": 74,
    "source_reference_id": "ref-reference-x-vol1-color",
    "spectrum": "orange",
    "spectrum_label_ko": "오렌지",
    "status": "cataloged",
    "summary": "Ochre is a Standard Oranges keyword in the orange spectrum, defined from REFERENCE X Vol.1 with RGB/CMYK reference values and mood tags.",
    "swatch_page_pdf": 73,
    "tone_axes": [
     "mid_value",
     "mid_chroma",
     "warm_bias",
     "earth_or_wine_bias"
    ]
   },
   "space": "concept",
   "type": "ColorKeyword"
  },
  {
   "id": "color-keyword-apricot",
   "properties": {
    "applies_when": {
     "color_family": [
      "natural",
      "any"
     ],
     "medium": [
      "digital",
      "print",
      "branding",
      "any"
     ],
     "spectrum": [
      "orange",
      "any"
     ]
    },
    "category": "Natural Oranges",
    "cmyk": "C 1%, M 38%, Y 51%, K 0%",
    "cmyk_c": 1,
    "cmyk_k": 0,
    "cmyk_m": 38,
    "cmyk_profile": "Coated GRACoL 2006",
    "cmyk_y": 51,
    "extraction_method": "macOS Vision OCR + representative page visual checks; raw OCR not committed",
    "family": "natural",
    "label": "Apricot",
    "metrics_page_pdf": 78,
    "mood_tags": [
     "따뜻함",
     "부드러움",
     "친근감",
     "여유",
     "자연스러움"
    ],
    "not_a_rule": true,
    "reference_reading_page_pdf": 77,
    "rgb_hex": "#FFB27F",
    "source_page_pdf": 77,
    "source_reference_id": "ref-reference-x-vol1-color",
    "spectrum": "orange",
    "spectrum_label_ko": "오렌지",
    "status": "cataloged",
    "summary": "Apricot is a Natural Oranges keyword in the orange spectrum, defined from REFERENCE X Vol.1 with RGB/CMYK reference values and mood tags.",
    "swatch_page_pdf": 76,
    "tone_axes": [
     "high_value",
     "low_chroma",
     "warm_bias"
    ]
   },
   "space": "concept",
   "type": "ColorKeyword"
  },
  {
   "id": "color-keyword-persimmon",
   "properties": {
    "applies_when": {
     "color_family": [
      "natural",
      "any"
     ],
     "medium": [
      "digital",
      "print",
      "branding",
      "any"
     ],
     "spectrum": [
      "orange",
      "any"
     ]
    },
    "category": "Natural Oranges",
    "cmyk": "C 6%, M 76%, Y 100%, K 0%",
    "cmyk_c": 6,
    "cmyk_k": 0,
    "cmyk_m": 76,
    "cmyk_profile": "Coated GRACoL 2006",
    "cmyk_y": 100,
    "extraction_method": "macOS Vision OCR + representative page visual checks; raw OCR not committed",
    "family": "natural",
    "label": "Persimmon",
    "metrics_page_pdf": 81,
    "mood_tags": [
     "생동감",
     "따뜻함",
     "안정감",
     "자연의 활기"
    ],
    "not_a_rule": true,
    "reference_reading_page_pdf": 80,
    "rgb_hex": "#EC5800",
    "source_page_pdf": 80,
    "source_reference_id": "ref-reference-x-vol1-color",
    "spectrum": "orange",
    "spectrum_label_ko": "오렌지",
    "status": "cataloged",
    "summary": "Persimmon is a Natural Oranges keyword in the orange spectrum, defined from REFERENCE X Vol.1 with RGB/CMYK reference values and mood tags.",
    "swatch_page_pdf": 79,
    "tone_axes": [
     "high_chroma",
     "warm_bias"
    ]
   },
   "space": "concept",
   "type": "ColorKeyword"
  },
  {
   "id": "color-keyword-pumpkin",
   "properties": {
    "applies_when": {
     "color_family": [
      "natural",
      "any"
     ],
     "medium": [
      "digital",
      "print",
      "branding",
      "any"
     ],
     "spectrum": [
      "orange",
      "any"
     ]
    },
    "canonical_label": "Pumpkin",
    "category": "Natural Oranges",
    "cmyk": "C 0%, M 65%, Y 90%, K 0%",
    "cmyk_c": 0,
    "cmyk_k": 0,
    "cmyk_m": 65,
    "cmyk_profile": "Coated GRACoL 2006",
    "cmyk_y": 90,
    "extraction_method": "macOS Vision OCR + representative page visual checks; raw OCR not committed",
    "family": "natural",
    "label": "Pumpkin",
    "metrics_page_pdf": 84,
    "mood_tags": [
     "풍요로움",
     "활기",
     "따뜻한 계절감",
     "안정된 에너지"
    ],
    "not_a_rule": true,
    "reference_reading_page_pdf": 83,
    "rgb_hex": "#FF7518",
    "source_label": "Pumkin",
    "source_label_note": "REFERENCE X page 83 spells the keyword as Pumkin; ontology keeps Pumpkin as canonical English spelling.",
    "source_page_pdf": 83,
    "source_reference_id": "ref-reference-x-vol1-color",
    "spectrum": "orange",
    "spectrum_label_ko": "오렌지",
    "status": "cataloged",
    "summary": "Pumpkin is a Natural Oranges keyword in the orange spectrum, defined from REFERENCE X Vol.1 with RGB/CMYK reference values and mood tags.",
    "swatch_page_pdf": 82,
    "tone_axes": [
     "mid_value",
     "mid_chroma",
     "warm_bias",
     "earth_or_wine_bias"
    ]
   },
   "space": "concept",
   "type": "ColorKeyword"
  },
  {
   "id": "color-keyword-rust",
   "properties": {
    "applies_when": {
     "color_family": [
      "deep",
      "any"
     ],
     "medium": [
      "digital",
      "print",
      "branding",
      "any"
     ],
     "spectrum": [
      "orange",
      "any"
     ]
    },
    "category": "Deep Oranges",
    "cmyk": "C 21%, M 84%, Y 100%, K 10%",
    "cmyk_c": 21,
    "cmyk_k": 10,
    "cmyk_m": 84,
    "cmyk_profile": "Coated GRACoL 2006",
    "cmyk_y": 100,
    "extraction_method": "macOS Vision OCR + representative page visual checks; raw OCR not committed",
    "family": "deep",
    "label": "Rust",
    "metrics_page_pdf": 87,
    "mood_tags": [
     "빈티지",
     "견고함",
     "따뜻한 노스탤지어",
     "공예적 감성"
    ],
    "not_a_rule": true,
    "reference_reading_page_pdf": 86,
    "rgb_hex": "#B7410E",
    "source_page_pdf": 86,
    "source_reference_id": "ref-reference-x-vol1-color",
    "spectrum": "orange",
    "spectrum_label_ko": "오렌지",
    "status": "cataloged",
    "summary": "Rust is a Deep Oranges keyword in the orange spectrum, defined from REFERENCE X Vol.1 with RGB/CMYK reference values and mood tags.",
    "swatch_page_pdf": 85,
    "tone_axes": [
     "low_value",
     "mid_chroma",
     "warm_bias",
     "earth_or_wine_bias"
    ]
   },
   "space": "concept",
   "type": "ColorKeyword"
  },
  {
   "id": "color-keyword-copper",
   "properties": {
    "applies_when": {
     "color_family": [
      "deep",
      "any"
     ],
     "medium": [
      "digital",
      "print",
      "branding",
      "any"
     ],
     "spectrum": [
      "orange",
      "any"
     ]
    },
    "category": "Deep Oranges",
    "cmyk": "C 22%, M 57%, Y 85%, K 13%",
    "cmyk_c": 22,
    "cmyk_k": 13,
    "cmyk_m": 57,
    "cmyk_profile": "Coated GRACoL 2006",
    "cmyk_y": 85,
    "extraction_method": "macOS Vision OCR + representative page visual checks; raw OCR not committed",
    "family": "deep",
    "label": "Copper",
    "metrics_page_pdf": 90,
    "mood_tags": [
     "고급스러움",
     "따뜻함",
     "전통적 질감",
     "세련된 무게감"
    ],
    "not_a_rule": true,
    "reference_reading_page_pdf": 89,
    "rgb_hex": "#B87333",
    "source_page_pdf": 89,
    "source_reference_id": "ref-reference-x-vol1-color",
    "spectrum": "orange",
    "spectrum_label_ko": "오렌지",
    "status": "cataloged",
    "summary": "Copper is a Deep Oranges keyword in the orange spectrum, defined from REFERENCE X Vol.1 with RGB/CMYK reference values and mood tags.",
    "swatch_page_pdf": 88,
    "tone_axes": [
     "low_value",
     "mid_chroma",
     "warm_bias",
     "earth_or_wine_bias"
    ]
   },
   "space": "concept",
   "type": "ColorKeyword"
  },
  {
   "id": "color-keyword-burnt-orange",
   "properties": {
    "applies_when": {
     "color_family": [
      "deep",
      "any"
     ],
     "medium": [
      "digital",
      "print",
      "branding",
      "any"
     ],
     "spectrum": [
      "orange",
      "any"
     ]
    },
    "category": "Deep Oranges",
    "cmyk": "C 17%, M 76%, Y 100%, K 6%",
    "cmyk_c": 17,
    "cmyk_k": 6,
    "cmyk_m": 76,
    "cmyk_profile": "Coated GRACoL 2006",
    "cmyk_y": 100,
    "extraction_method": "macOS Vision OCR + representative page visual checks; raw OCR not committed",
    "family": "deep",
    "label": "Burnt Orange",
    "metrics_page_pdf": 93,
    "mood_tags": [
     "따뜻함",
     "향수",
     "빈티지",
     "성숙함"
    ],
    "not_a_rule": true,
    "reference_reading_page_pdf": 92,
    "rgb_hex": "#CC5500",
    "source_page_pdf": 92,
    "source_reference_id": "ref-reference-x-vol1-color",
    "spectrum": "orange",
    "spectrum_label_ko": "오렌지",
    "status": "cataloged",
    "summary": "Burnt Orange is a Deep Oranges keyword in the orange spectrum, defined from REFERENCE X Vol.1 with RGB/CMYK reference values and mood tags.",
    "swatch_page_pdf": 91,
    "tone_axes": [
     "low_value",
     "high_chroma",
     "mid_chroma",
     "warm_bias",
     "earth_or_wine_bias"
    ]
   },
   "space": "concept",
   "type": "ColorKeyword"
  },
  {
   "id": "color-keyword-peach-puff",
   "properties": {
    "applies_when": {
     "color_family": [
      "pastel",
      "any"
     ],
     "medium": [
      "digital",
      "print",
      "branding",
      "any"
     ],
     "spectrum": [
      "orange",
      "any"
     ]
    },
    "category": "Pastel Oranges",
    "cmyk": "C 0%, M 18%, Y 27%, K 0%",
    "cmyk_c": 0,
    "cmyk_k": 0,
    "cmyk_m": 18,
    "cmyk_profile": "Coated GRACoL 2006",
    "cmyk_y": 27,
    "extraction_method": "macOS Vision OCR + representative page visual checks; raw OCR not committed",
    "family": "pastel",
    "label": "Peach Puff",
    "metrics_page_pdf": 96,
    "mood_tags": [
     "따뜻함",
     "부드러움",
     "순수함",
     "친근함",
     "생기"
    ],
    "not_a_rule": true,
    "reference_reading_page_pdf": 95,
    "rgb_hex": "#FFDAB9",
    "source_page_pdf": 95,
    "source_reference_id": "ref-reference-x-vol1-color",
    "spectrum": "orange",
    "spectrum_label_ko": "오렌지",
    "status": "cataloged",
    "summary": "Peach Puff is a Pastel Oranges keyword in the orange spectrum, defined from REFERENCE X Vol.1 with RGB/CMYK reference values and mood tags.",
    "swatch_page_pdf": 94,
    "tone_axes": [
     "high_value",
     "low_chroma",
     "warm_bias",
     "pastel"
    ]
   },
   "space": "concept",
   "type": "ColorKeyword"
  },
  {
   "id": "color-keyword-coral-blush",
   "properties": {
    "applies_when": {
     "color_family": [
      "pastel",
      "any"
     ],
     "medium": [
      "digital",
      "print",
      "branding",
      "any"
     ],
     "spectrum": [
      "orange",
      "any"
     ]
    },
    "category": "Pastel Oranges",
    "cmyk": "C 3%, M 61%, Y 45%, K 0%",
    "cmyk_c": 3,
    "cmyk_k": 0,
    "cmyk_m": 61,
    "cmyk_profile": "Coated GRACoL 2006",
    "cmyk_y": 45,
    "extraction_method": "macOS Vision OCR + representative page visual checks; raw OCR not committed",
    "family": "pastel",
    "label": "Coral Blush",
    "metrics_page_pdf": 99,
    "mood_tags": [
     "감성적",
     "따뜻함",
     "세련됨",
     "우아함"
    ],
    "not_a_rule": true,
    "reference_reading_page_pdf": 98,
    "rgb_hex": "#F88379",
    "source_page_pdf": 98,
    "source_reference_id": "ref-reference-x-vol1-color",
    "spectrum": "orange",
    "spectrum_label_ko": "오렌지",
    "status": "cataloged",
    "summary": "Coral Blush is a Pastel Oranges keyword in the orange spectrum, defined from REFERENCE X Vol.1 with RGB/CMYK reference values and mood tags.",
    "swatch_page_pdf": 97,
    "tone_axes": [
     "high_value",
     "mid_chroma",
     "low_chroma",
     "warm_bias",
     "pastel"
    ]
   },
   "space": "concept",
   "type": "ColorKeyword"
  },
  {
   "id": "color-keyword-creamsicle",
   "properties": {
    "applies_when": {
     "color_family": [
      "pastel",
      "any"
     ],
     "medium": [
      "digital",
      "print",
      "branding",
      "any"
     ],
     "spectrum": [
      "orange",
      "any"
     ]
    },
    "category": "Pastel Oranges",
    "cmyk": "C 2%, M 19%, Y 40%, K 0%",
    "cmyk_c": 2,
    "cmyk_k": 0,
    "cmyk_m": 19,
    "cmyk_profile": "Coated GRACoL 2006",
    "cmyk_y": 40,
    "extraction_method": "macOS Vision OCR + representative page visual checks; raw OCR not committed",
    "family": "pastel",
    "label": "Creamsicle",
    "metrics_page_pdf": 102,
    "mood_tags": [
     "부드러움",
     "경쾌함",
     "청량함",
     "달콤함"
    ],
    "not_a_rule": true,
    "reference_reading_page_pdf": 101,
    "rgb_hex": "#FFD7A0",
    "source_page_pdf": 101,
    "source_reference_id": "ref-reference-x-vol1-color",
    "spectrum": "orange",
    "spectrum_label_ko": "오렌지",
    "status": "cataloged",
    "summary": "Creamsicle is a Pastel Oranges keyword in the orange spectrum, defined from REFERENCE X Vol.1 with RGB/CMYK reference values and mood tags.",
    "swatch_page_pdf": 100,
    "tone_axes": [
     "high_value",
     "low_chroma",
     "warm_bias",
     "pastel"
    ]
   },
   "space": "concept",
   "type": "ColorKeyword"
  },
  {
   "id": "color-keyword-living-coral",
   "properties": {
    "applies_when": {
     "color_family": [
      "pantone_trend",
      "any"
     ],
     "medium": [
      "digital",
      "print",
      "branding",
      "any"
     ],
     "spectrum": [
      "orange",
      "any"
     ]
    },
    "category": "Pantone Trend Oranges",
    "cmyk": "C 0%, M 69%, Y 56%, K 0%",
    "cmyk_c": 0,
    "cmyk_k": 0,
    "cmyk_m": 69,
    "cmyk_profile": "Coated GRACoL 2006",
    "cmyk_y": 56,
    "extraction_method": "macOS Vision OCR + representative page visual checks; raw OCR not committed",
    "family": "pantone_trend",
    "label": "Living Coral",
    "metrics_page_pdf": 105,
    "mood_tags": [
     "생동감",
     "따뜻함",
     "낙관적"
    ],
    "not_a_rule": true,
    "pantone_code": "Pantone 16-1546",
    "reference_reading_page_pdf": 104,
    "rgb_hex": "#FF6F61",
    "source_page_pdf": 104,
    "source_reference_id": "ref-reference-x-vol1-color",
    "spectrum": "orange",
    "spectrum_label_ko": "오렌지",
    "status": "cataloged",
    "summary": "Living Coral is a Pantone Trend Oranges keyword in the orange spectrum, defined from REFERENCE X Vol.1 with RGB/CMYK reference values and mood tags.",
    "swatch_page_pdf": 103,
    "tone_axes": [
     "mid_value",
     "mid_chroma",
     "warm_bias"
    ]
   },
   "space": "concept",
   "type": "ColorKeyword"
  },
  {
   "id": "color-keyword-flame",
   "properties": {
    "applies_when": {
     "color_family": [
      "pantone_trend",
      "any"
     ],
     "medium": [
      "digital",
      "print",
      "branding",
      "any"
     ],
     "spectrum": [
      "orange",
      "any"
     ]
    },
    "category": "Pantone Trend Oranges",
    "cmyk": "C 4%, M 78%, Y 84%, K 0%",
    "cmyk_c": 4,
    "cmyk_k": 0,
    "cmyk_m": 78,
    "cmyk_profile": "Coated GRACoL 2006",
    "cmyk_y": 84,
    "extraction_method": "macOS Vision OCR + representative page visual checks; raw OCR not committed",
    "family": "pantone_trend",
    "label": "Flame",
    "metrics_page_pdf": 108,
    "mood_tags": [
     "열정적",
     "활발함",
     "도전적",
     "파워풀"
    ],
    "not_a_rule": true,
    "pantone_code": "Pantone 17-1462",
    "reference_reading_page_pdf": 107,
    "rgb_hex": "#F2552C",
    "source_page_pdf": 107,
    "source_reference_id": "ref-reference-x-vol1-color",
    "spectrum": "orange",
    "spectrum_label_ko": "오렌지",
    "status": "cataloged",
    "summary": "Flame is a Pantone Trend Oranges keyword in the orange spectrum, defined from REFERENCE X Vol.1 with RGB/CMYK reference values and mood tags.",
    "swatch_page_pdf": 106,
    "tone_axes": [
     "mid_value",
     "high_chroma",
     "warm_bias"
    ]
   },
   "space": "concept",
   "type": "ColorKeyword"
  },
  {
   "id": "color-keyword-chili-oil",
   "properties": {
    "applies_when": {
     "color_family": [
      "pantone_trend",
      "any"
     ],
     "medium": [
      "digital",
      "print",
      "branding",
      "any"
     ],
     "spectrum": [
      "orange",
      "any"
     ]
    },
    "category": "Pantone Trend Oranges",
    "cmyk": "C 28%, M 77%, Y 74%, K 28%",
    "cmyk_c": 28,
    "cmyk_k": 28,
    "cmyk_m": 77,
    "cmyk_profile": "Coated GRACoL 2006",
    "cmyk_y": 74,
    "extraction_method": "macOS Vision OCR + representative page visual checks; raw OCR not committed",
    "family": "pantone_trend",
    "label": "Chili Oil",
    "metrics_page_pdf": 111,
    "mood_tags": [
     "고급스러움",
     "안정감",
     "따뜻함",
     "자연"
    ],
    "not_a_rule": true,
    "pantone_code": "Pantone 18-1440",
    "reference_reading_page_pdf": 110,
    "rgb_hex": "#944537",
    "source_page_pdf": 110,
    "source_reference_id": "ref-reference-x-vol1-color",
    "spectrum": "orange",
    "spectrum_label_ko": "오렌지",
    "status": "cataloged",
    "summary": "Chili Oil is a Pantone Trend Oranges keyword in the orange spectrum, defined from REFERENCE X Vol.1 with RGB/CMYK reference values and mood tags.",
    "swatch_page_pdf": 109,
    "tone_axes": [
     "low_value",
     "low_chroma",
     "warm_bias",
     "earth_or_wine_bias"
    ]
   },
   "space": "concept",
   "type": "ColorKeyword"
  },
  {
   "id": "color-keyword-lemon-yellow",
   "properties": {
    "applies_when": {
     "color_family": [
      "standard",
      "any"
     ],
     "medium": [
      "digital",
      "print",
      "branding",
      "any"
     ],
     "spectrum": [
      "yellow",
      "any"
     ]
    },
    "category": "Standard Yellows",
    "cmyk": "C 8%, M 0%, Y 74%, K 0%",
    "cmyk_c": 8,
    "cmyk_k": 0,
    "cmyk_m": 0,
    "cmyk_profile": "Coated GRACoL 2006",
    "cmyk_y": 74,
    "extraction_method": "macOS Vision OCR + representative page visual checks; raw OCR not committed",
    "family": "standard",
    "label": "Lemon Yellow",
    "metrics_page_pdf": 121,
    "mood_tags": [
     "경쾌함",
     "낙관",
     "청량감",
     "에너지"
    ],
    "not_a_rule": true,
    "reference_reading_page_pdf": 120,
    "rgb_hex": "#FFF44F",
    "source_page_pdf": 120,
    "source_reference_id": "ref-reference-x-vol1-color",
    "spectrum": "yellow",
    "spectrum_label_ko": "옐로",
    "status": "cataloged",
    "summary": "Lemon Yellow is a Standard Yellows keyword in the yellow spectrum, defined from REFERENCE X Vol.1 with RGB/CMYK reference values and mood tags.",
    "swatch_page_pdf": 119,
    "tone_axes": [
     "high_value",
     "high_chroma",
     "warm_bias"
    ]
   },
   "space": "concept",
   "type": "ColorKeyword"
  },
  {
   "id": "color-keyword-goldenrod",
   "properties": {
    "applies_when": {
     "color_family": [
      "standard",
      "any"
     ],
     "medium": [
      "digital",
      "print",
      "branding",
      "any"
     ],
     "spectrum": [
      "yellow",
      "any"
     ]
    },
    "category": "Standard Yellows",
    "cmyk": "C 16%, M 35%, Y 93%, K 3%",
    "cmyk_c": 16,
    "cmyk_k": 3,
    "cmyk_m": 35,
    "cmyk_profile": "Coated GRACoL 2006",
    "cmyk_y": 93,
    "extraction_method": "macOS Vision OCR + representative page visual checks; raw OCR not committed",
    "family": "standard",
    "label": "Goldenrod",
    "metrics_page_pdf": 124,
    "mood_tags": [
     "따뜻함",
     "안정감",
     "고급스러움",
     "빈티지 감성"
    ],
    "not_a_rule": true,
    "reference_reading_page_pdf": 123,
    "rgb_hex": "#DAA520",
    "source_page_pdf": 123,
    "source_reference_id": "ref-reference-x-vol1-color",
    "spectrum": "yellow",
    "spectrum_label_ko": "옐로",
    "status": "cataloged",
    "summary": "Goldenrod is a Standard Yellows keyword in the yellow spectrum, defined from REFERENCE X Vol.1 with RGB/CMYK reference values and mood tags.",
    "swatch_page_pdf": 122,
    "tone_axes": [
     "mid_value",
     "mid_chroma",
     "warm_bias"
    ]
   },
   "space": "concept",
   "type": "ColorKeyword"
  },
  {
   "id": "color-keyword-amber",
   "properties": {
    "applies_when": {
     "color_family": [
      "standard",
      "any"
     ],
     "medium": [
      "digital",
      "print",
      "branding",
      "any"
     ],
     "spectrum": [
      "yellow",
      "any"
     ]
    },
    "category": "Standard Yellows",
    "cmyk": "C 4%, M 28%, Y 92%, K 0%",
    "cmyk_c": 4,
    "cmyk_k": 0,
    "cmyk_m": 28,
    "cmyk_profile": "Coated GRACoL 2006",
    "cmyk_y": 92,
    "extraction_method": "macOS Vision OCR + representative page visual checks; raw OCR not committed",
    "family": "standard",
    "label": "Amber",
    "metrics_page_pdf": 127,
    "mood_tags": [
     "따뜻함",
     "세련됨",
     "고급스러움",
     "안정감"
    ],
    "not_a_rule": true,
    "reference_reading_page_pdf": 126,
    "rgb_hex": "#FFBF00",
    "source_page_pdf": 126,
    "source_reference_id": "ref-reference-x-vol1-color",
    "spectrum": "yellow",
    "spectrum_label_ko": "옐로",
    "status": "cataloged",
    "summary": "Amber is a Standard Yellows keyword in the yellow spectrum, defined from REFERENCE X Vol.1 with RGB/CMYK reference values and mood tags.",
    "swatch_page_pdf": 125,
    "tone_axes": [
     "mid_value",
     "mid_chroma",
     "warm_bias"
    ]
   },
   "space": "concept",
   "type": "ColorKeyword"
  },
  {
   "id": "color-keyword-mustard-yellow",
   "properties": {
    "applies_when": {
     "color_family": [
      "natural",
      "any"
     ],
     "medium": [
      "digital",
      "print",
      "branding",
      "any"
     ],
     "spectrum": [
      "yellow",
      "any"
     ]
    },
    "category": "Natural Yellows",
    "cmyk": "C 5%, M 20%, Y 88%, K 0%",
    "cmyk_c": 5,
    "cmyk_k": 0,
    "cmyk_m": 20,
    "cmyk_profile": "Coated GRACoL 2006",
    "cmyk_y": 88,
    "extraction_method": "macOS Vision OCR + representative page visual checks; raw OCR not committed",
    "family": "natural",
    "label": "Mustard Yellow",
    "metrics_page_pdf": 130,
    "mood_tags": [
     "빈티지",
     "따뜻함",
     "편안함",
     "내추럴 클래식"
    ],
    "not_a_rule": true,
    "reference_reading_page_pdf": 129,
    "rgb_hex": "#FFCE1B",
    "source_page_pdf": 129,
    "source_reference_id": "ref-reference-x-vol1-color",
    "spectrum": "yellow",
    "spectrum_label_ko": "옐로",
    "status": "cataloged",
    "summary": "Mustard Yellow is a Natural Yellows keyword in the yellow spectrum, defined from REFERENCE X Vol.1 with RGB/CMYK reference values and mood tags.",
    "swatch_page_pdf": 128,
    "tone_axes": [
     "mid_value",
     "mid_chroma",
     "warm_bias",
     "earth_or_wine_bias"
    ]
   },
   "space": "concept",
   "type": "ColorKeyword"
  },
  {
   "id": "color-keyword-wheat",
   "properties": {
    "applies_when": {
     "color_family": [
      "natural",
      "any"
     ],
     "medium": [
      "digital",
      "print",
      "branding",
      "any"
     ],
     "spectrum": [
      "yellow",
      "any"
     ]
    },
    "category": "Natural Yellows",
    "cmyk": "C 6%, M 13%, Y 33%, K 0%",
    "cmyk_c": 6,
    "cmyk_k": 0,
    "cmyk_m": 13,
    "cmyk_profile": "Coated GRACoL 2006",
    "cmyk_y": 33,
    "extraction_method": "macOS Vision OCR + representative page visual checks; raw OCR not committed",
    "family": "natural",
    "label": "Wheat",
    "metrics_page_pdf": 133,
    "mood_tags": [
     "따뜻함",
     "자연스러움",
     "부드러움",
     "안정감"
    ],
    "not_a_rule": true,
    "reference_reading_page_pdf": 132,
    "rgb_hex": "#F5DEB3",
    "source_page_pdf": 132,
    "source_reference_id": "ref-reference-x-vol1-color",
    "spectrum": "yellow",
    "spectrum_label_ko": "옐로",
    "status": "cataloged",
    "summary": "Wheat is a Natural Yellows keyword in the yellow spectrum, defined from REFERENCE X Vol.1 with RGB/CMYK reference values and mood tags.",
    "swatch_page_pdf": 131,
    "tone_axes": [
     "mid_value",
     "low_chroma",
     "warm_bias"
    ]
   },
   "space": "concept",
   "type": "ColorKeyword"
  },
  {
   "id": "color-keyword-flax",
   "properties": {
    "applies_when": {
     "color_family": [
      "natural",
      "any"
     ],
     "medium": [
      "digital",
      "print",
      "branding",
      "any"
     ],
     "spectrum": [
      "yellow",
      "any"
     ]
    },
    "category": "Natural Yellows",
    "cmyk": "C 12%, M 11%, Y 58%, K 0%",
    "cmyk_c": 12,
    "cmyk_k": 0,
    "cmyk_m": 11,
    "cmyk_profile": "Coated GRACoL 2006",
    "cmyk_y": 58,
    "extraction_method": "macOS Vision OCR + representative page visual checks; raw OCR not committed",
    "family": "natural",
    "label": "Flax",
    "metrics_page_pdf": 136,
    "mood_tags": [
     "절제",
     "온기",
     "내추럴",
     "따뜻함",
     "클래식"
    ],
    "not_a_rule": true,
    "reference_reading_page_pdf": 135,
    "rgb_hex": "#EEDC82",
    "source_page_pdf": 135,
    "source_reference_id": "ref-reference-x-vol1-color",
    "spectrum": "yellow",
    "spectrum_label_ko": "옐로",
    "status": "cataloged",
    "summary": "Flax is a Natural Yellows keyword in the yellow spectrum, defined from REFERENCE X Vol.1 with RGB/CMYK reference values and mood tags.",
    "swatch_page_pdf": 134,
    "tone_axes": [
     "mid_value",
     "low_chroma",
     "warm_bias"
    ]
   },
   "space": "concept",
   "type": "ColorKeyword"
  },
  {
   "id": "color-keyword-ochre-yellow",
   "properties": {
    "applies_when": {
     "color_family": [
      "deep",
      "any"
     ],
     "medium": [
      "digital",
      "print",
      "branding",
      "any"
     ],
     "spectrum": [
      "yellow",
      "any"
     ]
    },
    "category": "Deep Yellows",
    "cmyk": "C 21%, M 36%, Y 100%, K 6%",
    "cmyk_c": 21,
    "cmyk_k": 6,
    "cmyk_m": 36,
    "cmyk_profile": "Coated GRACoL 2006",
    "cmyk_y": 100,
    "extraction_method": "macOS Vision OCR + representative page visual checks; raw OCR not committed",
    "family": "deep",
    "label": "Ochre Yellow",
    "metrics_page_pdf": 139,
    "mood_tags": [
     "따뜻함",
     "견고함",
     "전통미",
     "안정감",
     "고전적 깊이"
    ],
    "not_a_rule": true,
    "reference_reading_page_pdf": 138,
    "rgb_hex": "#CB9D06",
    "source_page_pdf": 138,
    "source_reference_id": "ref-reference-x-vol1-color",
    "spectrum": "yellow",
    "spectrum_label_ko": "옐로",
    "status": "cataloged",
    "summary": "Ochre Yellow is a Deep Yellows keyword in the yellow spectrum, defined from REFERENCE X Vol.1 with RGB/CMYK reference values and mood tags.",
    "swatch_page_pdf": 137,
    "tone_axes": [
     "mid_value",
     "low_value",
     "mid_chroma",
     "warm_bias",
     "earth_or_wine_bias"
    ]
   },
   "space": "concept",
   "type": "ColorKeyword"
  },
  {
   "id": "color-keyword-bronze-gold",
   "properties": {
    "applies_when": {
     "color_family": [
      "deep",
      "any"
     ],
     "medium": [
      "digital",
      "print",
      "branding",
      "any"
     ],
     "spectrum": [
      "yellow",
      "any"
     ]
    },
    "category": "Deep Yellows",
    "cmyk": "C 26%, M 54%, Y 86%, K 18%",
    "cmyk_c": 26,
    "cmyk_k": 18,
    "cmyk_m": 54,
    "cmyk_profile": "Coated GRACoL 2006",
    "cmyk_y": 86,
    "extraction_method": "macOS Vision OCR + representative page visual checks; raw OCR not committed",
    "family": "deep",
    "label": "Bronze Gold",
    "metrics_page_pdf": 142,
    "mood_tags": [
     "중후함",
     "고급스러움",
     "클래식함"
    ],
    "not_a_rule": true,
    "reference_reading_page_pdf": 141,
    "rgb_hex": "#A97132",
    "source_page_pdf": 141,
    "source_reference_id": "ref-reference-x-vol1-color",
    "spectrum": "yellow",
    "spectrum_label_ko": "옐로",
    "status": "cataloged",
    "summary": "Bronze Gold is a Deep Yellows keyword in the yellow spectrum, defined from REFERENCE X Vol.1 with RGB/CMYK reference values and mood tags.",
    "swatch_page_pdf": 140,
    "tone_axes": [
     "low_value",
     "mid_chroma",
     "warm_bias",
     "earth_or_wine_bias"
    ]
   },
   "space": "concept",
   "type": "ColorKeyword"
  },
  {
   "id": "color-keyword-naples-yellow",
   "properties": {
    "applies_when": {
     "color_family": [
      "pastel",
      "any"
     ],
     "medium": [
      "digital",
      "print",
      "branding",
      "any"
     ],
     "spectrum": [
      "yellow",
      "any"
     ]
    },
    "category": "Pastel Yellows",
    "cmyk": "C 7%, M 13%, Y 71%, K 0%",
    "cmyk_c": 7,
    "cmyk_k": 0,
    "cmyk_m": 13,
    "cmyk_profile": "Coated GRACoL 2006",
    "cmyk_y": 71,
    "extraction_method": "macOS Vision OCR + representative page visual checks; raw OCR not committed",
    "family": "pastel",
    "label": "Naples Yellow",
    "metrics_page_pdf": 145,
    "mood_tags": [
     "부드러움",
     "따뜻함",
     "온화함",
     "예술적 감성"
    ],
    "not_a_rule": true,
    "reference_reading_page_pdf": 144,
    "rgb_hex": "#FADA5E",
    "source_page_pdf": 144,
    "source_reference_id": "ref-reference-x-vol1-color",
    "spectrum": "yellow",
    "spectrum_label_ko": "옐로",
    "status": "cataloged",
    "summary": "Naples Yellow is a Pastel Yellows keyword in the yellow spectrum, defined from REFERENCE X Vol.1 with RGB/CMYK reference values and mood tags.",
    "swatch_page_pdf": 143,
    "tone_axes": [
     "high_value",
     "low_chroma",
     "warm_bias",
     "pastel"
    ]
   },
   "space": "concept",
   "type": "ColorKeyword"
  },
  {
   "id": "color-keyword-cornsilk",
   "properties": {
    "applies_when": {
     "color_family": [
      "pastel",
      "any"
     ],
     "medium": [
      "digital",
      "print",
      "branding",
      "any"
     ],
     "spectrum": [
      "yellow",
      "any"
     ]
    },
    "category": "Pastel Yellows",
    "cmyk": "C 2%, M 2%, Y 16%, K 0%",
    "cmyk_c": 2,
    "cmyk_k": 0,
    "cmyk_m": 2,
    "cmyk_profile": "Coated GRACoL 2006",
    "cmyk_y": 16,
    "extraction_method": "macOS Vision OCR + representative page visual checks; raw OCR not committed",
    "family": "pastel",
    "label": "Cornsilk",
    "metrics_page_pdf": 148,
    "mood_tags": [
     "따뜻함",
     "부드러움",
     "내추럴함",
     "포근함"
    ],
    "not_a_rule": true,
    "reference_reading_page_pdf": 147,
    "rgb_hex": "#FFF8DC",
    "source_page_pdf": 147,
    "source_reference_id": "ref-reference-x-vol1-color",
    "spectrum": "yellow",
    "spectrum_label_ko": "옐로",
    "status": "cataloged",
    "summary": "Cornsilk is a Pastel Yellows keyword in the yellow spectrum, defined from REFERENCE X Vol.1 with RGB/CMYK reference values and mood tags.",
    "swatch_page_pdf": 146,
    "tone_axes": [
     "high_value",
     "low_chroma",
     "warm_bias",
     "pastel"
    ]
   },
   "space": "concept",
   "type": "ColorKeyword"
  },
  {
   "id": "color-keyword-buttercream",
   "properties": {
    "applies_when": {
     "color_family": [
      "pastel",
      "any"
     ],
     "medium": [
      "digital",
      "print",
      "branding",
      "any"
     ],
     "spectrum": [
      "yellow",
      "any"
     ]
    },
    "category": "Pastel Yellows",
    "cmyk": "C 8%, M 8%, Y 40%, K 0%",
    "cmyk_c": 8,
    "cmyk_k": 0,
    "cmyk_m": 8,
    "cmyk_profile": "Coated GRACoL 2006",
    "cmyk_y": 40,
    "extraction_method": "macOS Vision OCR + representative page visual checks; raw OCR not committed",
    "family": "pastel",
    "label": "Buttercream",
    "metrics_page_pdf": 151,
    "mood_tags": [
     "부드러움",
     "따뜻함",
     "포근함",
     "달콤함"
    ],
    "not_a_rule": true,
    "reference_reading_page_pdf": 150,
    "rgb_hex": "#F3E5AB",
    "source_page_pdf": 150,
    "source_reference_id": "ref-reference-x-vol1-color",
    "spectrum": "yellow",
    "spectrum_label_ko": "옐로",
    "status": "cataloged",
    "summary": "Buttercream is a Pastel Yellows keyword in the yellow spectrum, defined from REFERENCE X Vol.1 with RGB/CMYK reference values and mood tags.",
    "swatch_page_pdf": 149,
    "tone_axes": [
     "high_value",
     "low_chroma",
     "warm_bias",
     "pastel"
    ]
   },
   "space": "concept",
   "type": "ColorKeyword"
  },
  {
   "id": "color-keyword-illuminating",
   "properties": {
    "applies_when": {
     "color_family": [
      "pantone_trend",
      "any"
     ],
     "medium": [
      "digital",
      "print",
      "branding",
      "any"
     ],
     "spectrum": [
      "yellow",
      "any"
     ]
    },
    "category": "Pantone Trend Yellows",
    "cmyk": "C 11%, M 9%, Y 76%, K 0%",
    "cmyk_c": 11,
    "cmyk_k": 0,
    "cmyk_m": 9,
    "cmyk_profile": "Coated GRACoL 2006",
    "cmyk_y": 76,
    "extraction_method": "macOS Vision OCR + representative page visual checks; raw OCR not committed",
    "family": "pantone_trend",
    "label": "Illuminating",
    "metrics_page_pdf": 154,
    "mood_tags": [
     "긍정적",
     "활기찬",
     "낙관적",
     "희망적인",
     "감각적인"
    ],
    "not_a_rule": true,
    "pantone_code": "Pantone 13-0647",
    "reference_reading_page_pdf": 153,
    "rgb_hex": "#F5DF4D",
    "source_page_pdf": 153,
    "source_reference_id": "ref-reference-x-vol1-color",
    "spectrum": "yellow",
    "spectrum_label_ko": "옐로",
    "status": "cataloged",
    "summary": "Illuminating is a Pantone Trend Yellows keyword in the yellow spectrum, defined from REFERENCE X Vol.1 with RGB/CMYK reference values and mood tags.",
    "swatch_page_pdf": 152,
    "tone_axes": [
     "high_value",
     "mid_chroma",
     "warm_bias"
    ]
   },
   "space": "concept",
   "type": "ColorKeyword"
  },
  {
   "id": "color-keyword-honey-gold",
   "properties": {
    "applies_when": {
     "color_family": [
      "pantone_trend",
      "any"
     ],
     "medium": [
      "digital",
      "print",
      "branding",
      "any"
     ],
     "spectrum": [
      "yellow",
      "any"
     ]
    },
    "category": "Pantone Trend Yellows",
    "cmyk": "C 16%, M 29%, Y 55%, K 2%",
    "cmyk_c": 16,
    "cmyk_k": 2,
    "cmyk_m": 29,
    "cmyk_profile": "Coated GRACoL 2006",
    "cmyk_y": 55,
    "extraction_method": "macOS Vision OCR + representative page visual checks; raw OCR not committed",
    "family": "pantone_trend",
    "label": "Honey Gold",
    "metrics_page_pdf": 157,
    "mood_tags": [
     "안정감",
     "품격",
     "여유",
     "가을의 온기"
    ],
    "not_a_rule": true,
    "pantone_code": "Pantone 15-1142",
    "reference_reading_page_pdf": 156,
    "rgb_hex": "#DDB67D",
    "source_page_pdf": 156,
    "source_reference_id": "ref-reference-x-vol1-color",
    "spectrum": "yellow",
    "spectrum_label_ko": "옐로",
    "status": "cataloged",
    "summary": "Honey Gold is a Pantone Trend Yellows keyword in the yellow spectrum, defined from REFERENCE X Vol.1 with RGB/CMYK reference values and mood tags.",
    "swatch_page_pdf": 155,
    "tone_axes": [
     "mid_value",
     "mid_chroma",
     "warm_bias"
    ]
   },
   "space": "concept",
   "type": "ColorKeyword"
  },
  {
   "id": "color-keyword-autumn-blaze",
   "properties": {
    "applies_when": {
     "color_family": [
      "pantone_trend",
      "any"
     ],
     "medium": [
      "digital",
      "print",
      "branding",
      "any"
     ],
     "spectrum": [
      "yellow",
      "any"
     ]
    },
    "category": "Pantone Trend Yellows",
    "cmyk": "C 16%, M 44%, Y 82%, K 4%",
    "cmyk_c": 16,
    "cmyk_k": 4,
    "cmyk_m": 44,
    "cmyk_profile": "Coated GRACoL 2006",
    "cmyk_y": 82,
    "extraction_method": "macOS Vision OCR + representative page visual checks; raw OCR not committed",
    "family": "pantone_trend",
    "label": "Autumn Blaze",
    "metrics_page_pdf": 160,
    "mood_tags": [
     "따뜻함",
     "온기",
     "성숙함",
     "자연스러움",
     "가을의 깊이"
    ],
    "not_a_rule": true,
    "pantone_code": "Pantone 15-1045",
    "reference_reading_page_pdf": 159,
    "rgb_hex": "#D1933F",
    "source_page_pdf": 159,
    "source_reference_id": "ref-reference-x-vol1-color",
    "spectrum": "yellow",
    "spectrum_label_ko": "옐로",
    "status": "cataloged",
    "summary": "Autumn Blaze is a Pantone Trend Yellows keyword in the yellow spectrum, defined from REFERENCE X Vol.1 with RGB/CMYK reference values and mood tags.",
    "swatch_page_pdf": 158,
    "tone_axes": [
     "mid_value",
     "mid_chroma",
     "warm_bias",
     "earth_or_wine_bias"
    ]
   },
   "space": "concept",
   "type": "ColorKeyword"
  },
  {
   "id": "color-keyword-emerald-green",
   "properties": {
    "applies_when": {
     "color_family": [
      "standard",
      "any"
     ],
     "medium": [
      "digital",
      "print",
      "branding",
      "any"
     ],
     "spectrum": [
      "green",
      "any"
     ]
    },
    "category": "Standard Greens",
    "cmyk": "C 66%, M 0%, Y 69%, K 0%",
    "cmyk_c": 66,
    "cmyk_k": 0,
    "cmyk_m": 0,
    "cmyk_profile": "Coated GRACoL 2006",
    "cmyk_y": 69,
    "extraction_method": "macOS Vision OCR + representative page visual checks; raw OCR not committed",
    "family": "standard",
    "label": "Emerald Green",
    "metrics_page_pdf": 171,
    "mood_tags": [
     "고급스러움",
     "생명력",
     "세련된 안정감",
     "청량한 자연성"
    ],
    "not_a_rule": true,
    "reference_reading_page_pdf": 170,
    "rgb_hex": "#50C878",
    "source_page_pdf": 170,
    "source_reference_id": "ref-reference-x-vol1-color",
    "spectrum": "green",
    "spectrum_label_ko": "그린",
    "status": "cataloged",
    "summary": "Emerald Green is a Standard Greens keyword in the green spectrum, defined from REFERENCE X Vol.1 with RGB/CMYK reference values and mood tags.",
    "swatch_page_pdf": 169,
    "tone_axes": [
     "mid_value",
     "mid_chroma"
    ]
   },
   "space": "concept",
   "type": "ColorKeyword"
  },
  {
   "id": "color-keyword-kelly-green",
   "properties": {
    "applies_when": {
     "color_family": [
      "standard",
      "any"
     ],
     "medium": [
      "digital",
      "print",
      "branding",
      "any"
     ],
     "spectrum": [
      "green",
      "any"
     ]
    },
    "category": "Standard Greens",
    "cmyk": "C 68%, M 0%, Y 100%, K 0%",
    "cmyk_c": 68,
    "cmyk_k": 0,
    "cmyk_m": 0,
    "cmyk_profile": "Coated GRACoL 2006",
    "cmyk_y": 100,
    "extraction_method": "macOS Vision OCR + representative page visual checks; raw OCR not committed",
    "family": "standard",
    "label": "Kelly Green",
    "metrics_page_pdf": 174,
    "mood_tags": [
     "활력",
     "생동감",
     "긍정성",
     "에너지",
     "명료함"
    ],
    "not_a_rule": true,
    "reference_reading_page_pdf": 173,
    "rgb_hex": "#4CBB17",
    "source_page_pdf": 173,
    "source_reference_id": "ref-reference-x-vol1-color",
    "spectrum": "green",
    "spectrum_label_ko": "그린",
    "status": "cataloged",
    "summary": "Kelly Green is a Standard Greens keyword in the green spectrum, defined from REFERENCE X Vol.1 with RGB/CMYK reference values and mood tags.",
    "swatch_page_pdf": 172,
    "tone_axes": [
     "high_value",
     "high_chroma"
    ]
   },
   "space": "concept",
   "type": "ColorKeyword"
  },
  {
   "id": "color-keyword-olive-green",
   "properties": {
    "applies_when": {
     "color_family": [
      "standard",
      "any"
     ],
     "medium": [
      "digital",
      "print",
      "branding",
      "any"
     ],
     "spectrum": [
      "green",
      "any"
     ]
    },
    "category": "Standard Greens",
    "cmyk": "C 58%, M 32%, Y 92%, K 16%",
    "cmyk_c": 58,
    "cmyk_k": 16,
    "cmyk_m": 32,
    "cmyk_profile": "Coated GRACoL 2006",
    "cmyk_y": 92,
    "extraction_method": "macOS Vision OCR + representative page visual checks; raw OCR not committed",
    "family": "standard",
    "label": "Olive Green",
    "metrics_page_pdf": 177,
    "mood_tags": [
     "내추럴",
     "빈티지",
     "안정감",
     "따뜻함",
     "실용성"
    ],
    "not_a_rule": true,
    "reference_reading_page_pdf": 176,
    "rgb_hex": "#708238",
    "source_page_pdf": 176,
    "source_reference_id": "ref-reference-x-vol1-color",
    "spectrum": "green",
    "spectrum_label_ko": "그린",
    "status": "cataloged",
    "summary": "Olive Green is a Standard Greens keyword in the green spectrum, defined from REFERENCE X Vol.1 with RGB/CMYK reference values and mood tags.",
    "swatch_page_pdf": 175,
    "tone_axes": [
     "mid_value",
     "low_chroma",
     "earth_or_wine_bias"
    ]
   },
   "space": "concept",
   "type": "ColorKeyword"
  },
  {
   "id": "color-keyword-moss-green",
   "properties": {
    "applies_when": {
     "color_family": [
      "natural",
      "any"
     ],
     "medium": [
      "digital",
      "print",
      "branding",
      "any"
     ],
     "spectrum": [
      "green",
      "any"
     ]
    },
    "category": "Natural Greens",
    "cmyk": "C 50%, M 26%, Y 74%, K 8%",
    "cmyk_c": 50,
    "cmyk_k": 8,
    "cmyk_m": 26,
    "cmyk_profile": "Coated GRACoL 2006",
    "cmyk_y": 74,
    "extraction_method": "macOS Vision OCR + representative page visual checks; raw OCR not committed",
    "family": "natural",
    "label": "Moss Green",
    "metrics_page_pdf": 180,
    "mood_tags": [
     "자연적",
     "차분함",
     "안정적인",
     "빈티지"
    ],
    "not_a_rule": true,
    "reference_reading_page_pdf": 179,
    "rgb_hex": "#8A9A5B",
    "source_page_pdf": 179,
    "source_reference_id": "ref-reference-x-vol1-color",
    "spectrum": "green",
    "spectrum_label_ko": "그린",
    "status": "cataloged",
    "summary": "Moss Green is a Natural Greens keyword in the green spectrum, defined from REFERENCE X Vol.1 with RGB/CMYK reference values and mood tags.",
    "swatch_page_pdf": 178,
    "tone_axes": [
     "low_value",
     "low_chroma",
     "earth_or_wine_bias"
    ]
   },
   "space": "concept",
   "type": "ColorKeyword"
  },
  {
   "id": "color-keyword-fern-green",
   "properties": {
    "applies_when": {
     "color_family": [
      "natural",
      "any"
     ],
     "medium": [
      "digital",
      "print",
      "branding",
      "any"
     ],
     "spectrum": [
      "green",
      "any"
     ]
    },
    "category": "Natural Greens",
    "cmyk": "C 70%, M 33%, Y 87%, K 18%",
    "cmyk_c": 70,
    "cmyk_k": 18,
    "cmyk_m": 33,
    "cmyk_profile": "Coated GRACoL 2006",
    "cmyk_y": 87,
    "extraction_method": "macOS Vision OCR + representative page visual checks; raw OCR not committed",
    "family": "natural",
    "label": "Fern Green",
    "metrics_page_pdf": 183,
    "mood_tags": [
     "차분함",
     "안정감",
     "유연함"
    ],
    "not_a_rule": true,
    "reference_reading_page_pdf": 182,
    "rgb_hex": "#4F7942",
    "source_page_pdf": 182,
    "source_reference_id": "ref-reference-x-vol1-color",
    "spectrum": "green",
    "spectrum_label_ko": "그린",
    "status": "cataloged",
    "summary": "Fern Green is a Natural Greens keyword in the green spectrum, defined from REFERENCE X Vol.1 with RGB/CMYK reference values and mood tags.",
    "swatch_page_pdf": 181,
    "tone_axes": [
     "mid_value",
     "mid_chroma"
    ]
   },
   "space": "concept",
   "type": "ColorKeyword"
  },
  {
   "id": "color-keyword-forest-green",
   "properties": {
    "applies_when": {
     "color_family": [
      "deep",
      "any"
     ],
     "medium": [
      "digital",
      "print",
      "branding",
      "any"
     ],
     "spectrum": [
      "green",
      "any"
     ]
    },
    "category": "Deep Greens",
    "cmyk": "C 80%, M 40%, Y 75%, K 45%",
    "cmyk_c": 80,
    "cmyk_k": 45,
    "cmyk_m": 40,
    "cmyk_profile": "Coated GRACoL 2006",
    "cmyk_y": 75,
    "extraction_method": "macOS Vision OCR + representative page visual checks; raw OCR not committed",
    "family": "deep",
    "label": "Forest Green",
    "metrics_page_pdf": 186,
    "mood_tags": [
     "묵직함",
     "안정감",
     "신뢰",
     "자연적 깊이"
    ],
    "not_a_rule": true,
    "reference_reading_page_pdf": 185,
    "rgb_hex": "#27503D",
    "source_page_pdf": 185,
    "source_reference_id": "ref-reference-x-vol1-color",
    "spectrum": "green",
    "spectrum_label_ko": "그린",
    "status": "cataloged",
    "summary": "Forest Green is a Deep Greens keyword in the green spectrum, defined from REFERENCE X Vol.1 with RGB/CMYK reference values and mood tags.",
    "swatch_page_pdf": 184,
    "tone_axes": [
     "low_value",
     "high_chroma"
    ]
   },
   "space": "concept",
   "type": "ColorKeyword"
  },
  {
   "id": "color-keyword-hunter-green",
   "properties": {
    "applies_when": {
     "color_family": [
      "natural",
      "any"
     ],
     "medium": [
      "digital",
      "print",
      "branding",
      "any"
     ],
     "spectrum": [
      "green",
      "any"
     ]
    },
    "category": "Natural Greens",
    "cmyk": "C 77%, M 39%, Y 85%, K 34%",
    "cmyk_c": 77,
    "cmyk_k": 34,
    "cmyk_m": 39,
    "cmyk_profile": "Coated GRACoL 2006",
    "cmyk_y": 85,
    "extraction_method": "macOS Vision OCR + representative page visual checks; raw OCR not committed",
    "family": "natural",
    "label": "Hunter Green",
    "metrics_page_pdf": 189,
    "mood_tags": [
     "중후함",
     "신뢰",
     "클래식",
     "깊이감",
     "균형감"
    ],
    "not_a_rule": true,
    "reference_reading_page_pdf": 188,
    "rgb_hex": "#355E3B",
    "source_page_pdf": 188,
    "source_reference_id": "ref-reference-x-vol1-color",
    "spectrum": "green",
    "spectrum_label_ko": "그린",
    "status": "cataloged",
    "summary": "Hunter Green is a Natural Greens keyword in the green spectrum, defined from REFERENCE X Vol.1 with RGB/CMYK reference values and mood tags.",
    "swatch_page_pdf": 187,
    "tone_axes": [
     "low_value",
     "high_chroma",
     "mid_chroma"
    ]
   },
   "space": "concept",
   "type": "ColorKeyword"
  },
  {
   "id": "color-keyword-bottle-green",
   "properties": {
    "applies_when": {
     "color_family": [
      "deep",
      "any"
     ],
     "medium": [
      "digital",
      "print",
      "branding",
      "any"
     ],
     "spectrum": [
      "green",
      "any"
     ]
    },
    "category": "Deep Greens",
    "cmyk": "C 87%, M 33%, Y 77%, K 25%",
    "cmyk_c": 87,
    "cmyk_k": 25,
    "cmyk_m": 33,
    "cmyk_profile": "Coated GRACoL 2006",
    "cmyk_y": 77,
    "extraction_method": "macOS Vision OCR + representative page visual checks; raw OCR not committed",
    "family": "deep",
    "label": "Bottle Green",
    "metrics_page_pdf": 192,
    "mood_tags": [
     "절제됨",
     "균형",
     "신뢰",
     "빈티지",
     "고급스러움"
    ],
    "not_a_rule": true,
    "reference_reading_page_pdf": 191,
    "rgb_hex": "#006A4E",
    "source_page_pdf": 191,
    "source_reference_id": "ref-reference-x-vol1-color",
    "spectrum": "green",
    "spectrum_label_ko": "그린",
    "status": "cataloged",
    "summary": "Bottle Green is a Deep Greens keyword in the green spectrum, defined from REFERENCE X Vol.1 with RGB/CMYK reference values and mood tags.",
    "swatch_page_pdf": 190,
    "tone_axes": [
     "low_value",
     "mid_chroma",
     "low_chroma"
    ]
   },
   "space": "concept",
   "type": "ColorKeyword"
  },
  {
   "id": "color-keyword-mint-green",
   "properties": {
    "applies_when": {
     "color_family": [
      "pastel",
      "any"
     ],
     "medium": [
      "digital",
      "print",
      "branding",
      "any"
     ],
     "spectrum": [
      "green",
      "any"
     ]
    },
    "category": "Pastel Greens",
    "cmyk": "C 42%, M 0%, Y 56%, K 0%",
    "cmyk_c": 42,
    "cmyk_k": 0,
    "cmyk_m": 0,
    "cmyk_profile": "Coated GRACoL 2006",
    "cmyk_y": 56,
    "extraction_method": "macOS Vision OCR + representative page visual checks; raw OCR not committed",
    "family": "pastel",
    "label": "Mint Green",
    "metrics_page_pdf": 195,
    "mood_tags": [
     "청량함",
     "신선함",
     "현대적 감성",
     "부드러움"
    ],
    "not_a_rule": true,
    "reference_reading_page_pdf": 194,
    "rgb_hex": "#98FF98",
    "source_page_pdf": 194,
    "source_reference_id": "ref-reference-x-vol1-color",
    "spectrum": "green",
    "spectrum_label_ko": "그린",
    "status": "cataloged",
    "summary": "Mint Green is a Pastel Greens keyword in the green spectrum, defined from REFERENCE X Vol.1 with RGB/CMYK reference values and mood tags.",
    "swatch_page_pdf": 193,
    "tone_axes": [
     "high_value",
     "low_chroma",
     "cool_bias",
     "pastel"
    ]
   },
   "space": "concept",
   "type": "ColorKeyword"
  },
  {
   "id": "color-keyword-celadon",
   "properties": {
    "applies_when": {
     "color_family": [
      "pastel",
      "any"
     ],
     "medium": [
      "digital",
      "print",
      "branding",
      "any"
     ],
     "spectrum": [
      "green",
      "any"
     ]
    },
    "category": "Pastel Greens",
    "cmyk": "C 38%, M 0%, Y 41%, K 0%",
    "cmyk_c": 38,
    "cmyk_k": 0,
    "cmyk_m": 0,
    "cmyk_profile": "Coated GRACoL 2006",
    "cmyk_y": 41,
    "extraction_method": "macOS Vision OCR + representative page visual checks; raw OCR not committed",
    "family": "pastel",
    "label": "Celadon",
    "metrics_page_pdf": 198,
    "mood_tags": [
     "자연스러움",
     "절제",
     "고요",
     "전통미",
     "단아함"
    ],
    "not_a_rule": true,
    "reference_reading_page_pdf": 197,
    "rgb_hex": "#ACE1AF",
    "source_page_pdf": 197,
    "source_reference_id": "ref-reference-x-vol1-color",
    "spectrum": "green",
    "spectrum_label_ko": "그린",
    "status": "cataloged",
    "summary": "Celadon is a Pastel Greens keyword in the green spectrum, defined from REFERENCE X Vol.1 with RGB/CMYK reference values and mood tags.",
    "swatch_page_pdf": 196,
    "tone_axes": [
     "mid_value",
     "low_chroma",
     "pastel"
    ]
   },
   "space": "concept",
   "type": "ColorKeyword"
  },
  {
   "id": "color-keyword-greenery",
   "properties": {
    "applies_when": {
     "color_family": [
      "pantone_trend",
      "any"
     ],
     "medium": [
      "digital",
      "print",
      "branding",
      "any"
     ],
     "spectrum": [
      "green",
      "any"
     ]
    },
    "category": "Pantone Trend Greens",
    "cmyk": "C 54%, M 16%, Y 85%, K 1%",
    "cmyk_c": 54,
    "cmyk_k": 1,
    "cmyk_m": 16,
    "cmyk_profile": "Coated GRACoL 2006",
    "cmyk_y": 85,
    "extraction_method": "macOS Vision OCR + representative page visual checks; raw OCR not committed",
    "family": "pantone_trend",
    "label": "Greenery",
    "metrics_page_pdf": 201,
    "mood_tags": [
     "회복",
     "생명력",
     "청춘",
     "균형",
     "리프레시"
    ],
    "not_a_rule": true,
    "pantone_code": "Pantone 15-0343",
    "reference_reading_page_pdf": 200,
    "rgb_hex": "#88B04B",
    "source_page_pdf": 200,
    "source_reference_id": "ref-reference-x-vol1-color",
    "spectrum": "green",
    "spectrum_label_ko": "그린",
    "status": "cataloged",
    "summary": "Greenery is a Pantone Trend Greens keyword in the green spectrum, defined from REFERENCE X Vol.1 with RGB/CMYK reference values and mood tags.",
    "swatch_page_pdf": 199,
    "tone_axes": [
     "mid_value",
     "mid_chroma",
     "warm_bias"
    ]
   },
   "space": "concept",
   "type": "ColorKeyword"
  },
  {
   "id": "color-keyword-arcadia",
   "properties": {
    "applies_when": {
     "color_family": [
      "pantone_trend",
      "any"
     ],
     "medium": [
      "digital",
      "print",
      "branding",
      "any"
     ],
     "spectrum": [
      "green",
      "any"
     ]
    },
    "category": "Pantone Trend Greens",
    "cmyk": "C 78%, M 13%, Y 52%, K 1%",
    "cmyk_c": 78,
    "cmyk_k": 1,
    "cmyk_m": 13,
    "cmyk_profile": "Coated GRACoL 2006",
    "cmyk_y": 52,
    "extraction_method": "macOS Vision OCR + representative page visual checks; raw OCR not committed",
    "family": "pantone_trend",
    "label": "Arcadia",
    "metrics_page_pdf": 204,
    "mood_tags": [
     "세련",
     "청량",
     "도시적",
     "미래지향",
     "균형"
    ],
    "not_a_rule": true,
    "pantone_code": "Pantone 16-5533",
    "reference_reading_page_pdf": 203,
    "rgb_hex": "#00A591",
    "source_page_pdf": 203,
    "source_reference_id": "ref-reference-x-vol1-color",
    "spectrum": "green",
    "spectrum_label_ko": "그린",
    "status": "cataloged",
    "summary": "Arcadia is a Pantone Trend Greens keyword in the green spectrum, defined from REFERENCE X Vol.1 with RGB/CMYK reference values and mood tags.",
    "swatch_page_pdf": 202,
    "tone_axes": [
     "mid_value",
     "mid_chroma",
     "cool_bias"
    ]
   },
   "space": "concept",
   "type": "ColorKeyword"
  },
  {
   "id": "color-keyword-cascades",
   "properties": {
    "applies_when": {
     "color_family": [
      "pantone_trend",
      "any"
     ],
     "medium": [
      "digital",
      "print",
      "branding",
      "any"
     ],
     "spectrum": [
      "green",
      "any"
     ]
    },
    "category": "Pantone Trend Greens",
    "cmyk": "C 57%, M 7%, Y 37%, K 0%",
    "cmyk_c": 57,
    "cmyk_k": 0,
    "cmyk_m": 7,
    "cmyk_profile": "Coated GRACoL 2006",
    "cmyk_y": 37,
    "extraction_method": "macOS Vision OCR + representative page visual checks; raw OCR not committed",
    "family": "pantone_trend",
    "label": "Cascade",
    "metrics_page_pdf": 207,
    "mood_tags": [
     "정제된 청량감",
     "세련미",
     "안정감",
     "포근함"
    ],
    "not_a_rule": true,
    "pantone_code": "Pantone 14-5713",
    "reference_reading_page_pdf": 206,
    "rgb_hex": "#76C1B1",
    "source_page_pdf": 206,
    "source_reference_id": "ref-reference-x-vol1-color",
    "spectrum": "green",
    "spectrum_label_ko": "그린",
    "status": "cataloged",
    "summary": "Cascade is a Pantone Trend Greens keyword in the green spectrum, defined from REFERENCE X Vol.1 with RGB/CMYK reference values and mood tags.",
    "swatch_page_pdf": 205,
    "tone_axes": [
     "mid_value",
     "low_chroma",
     "cool_bias"
    ]
   },
   "space": "concept",
   "type": "ColorKeyword"
  },
  {
   "id": "color-keyword-cerulean",
   "properties": {
    "applies_when": {
     "color_family": [
      "standard",
      "any"
     ],
     "medium": [
      "digital",
      "print",
      "branding",
      "any"
     ],
     "spectrum": [
      "blue",
      "any"
     ]
    },
    "category": "Standard Blues",
    "cmyk": "C 89%, M 71%, Y 0%, K 0%",
    "cmyk_c": 89,
    "cmyk_k": 0,
    "cmyk_m": 71,
    "cmyk_profile": "Coated GRACoL 2006",
    "cmyk_y": 0,
    "extraction_method": "macOS Vision OCR + representative page visual checks; raw OCR not committed",
    "family": "standard",
    "label": "Cerulean",
    "metrics_page_pdf": 217,
    "mood_tags": [
     "안정감",
     "명료함",
     "신뢰",
     "여유",
     "시각적 청량감"
    ],
    "not_a_rule": true,
    "reference_reading_page_pdf": 216,
    "rgb_hex": "#2A52BE",
    "source_page_pdf": 216,
    "source_reference_id": "ref-reference-x-vol1-color",
    "spectrum": "blue",
    "spectrum_label_ko": "블루",
    "status": "cataloged",
    "summary": "Cerulean is a Standard Blues keyword in the blue spectrum, defined from REFERENCE X Vol.1 with RGB/CMYK reference values and mood tags.",
    "swatch_page_pdf": 215,
    "tone_axes": [
     "mid_value",
     "mid_chroma"
    ]
   },
   "space": "concept",
   "type": "ColorKeyword"
  },
  {
   "id": "color-keyword-azure-blue",
   "properties": {
    "applies_when": {
     "color_family": [
      "standard",
      "any"
     ],
     "medium": [
      "digital",
      "print",
      "branding",
      "any"
     ],
     "spectrum": [
      "blue",
      "any"
     ]
    },
    "category": "Standard Blues",
    "cmyk": "C 81%, M 51%, Y 0%, K 0%",
    "cmyk_c": 81,
    "cmyk_k": 0,
    "cmyk_m": 51,
    "cmyk_profile": "Coated GRACoL 2006",
    "cmyk_y": 0,
    "extraction_method": "macOS Vision OCR + representative page visual checks; raw OCR not committed",
    "family": "standard",
    "label": "Azure Blue",
    "metrics_page_pdf": 220,
    "mood_tags": [
     "개방감",
     "에너지",
     "명료함",
     "신선함",
     "혁신"
    ],
    "not_a_rule": true,
    "reference_reading_page_pdf": 219,
    "rgb_hex": "#007FFF",
    "source_page_pdf": 219,
    "source_reference_id": "ref-reference-x-vol1-color",
    "spectrum": "blue",
    "spectrum_label_ko": "블루",
    "status": "cataloged",
    "summary": "Azure Blue is a Standard Blues keyword in the blue spectrum, defined from REFERENCE X Vol.1 with RGB/CMYK reference values and mood tags.",
    "swatch_page_pdf": 218,
    "tone_axes": [
     "high_value",
     "high_chroma",
     "cool_bias"
    ]
   },
   "space": "concept",
   "type": "ColorKeyword"
  },
  {
   "id": "color-keyword-sky-blue",
   "properties": {
    "applies_when": {
     "color_family": [
      "natural",
      "any"
     ],
     "medium": [
      "digital",
      "print",
      "branding",
      "any"
     ],
     "spectrum": [
      "blue",
      "any"
     ]
    },
    "category": "Natural Blues",
    "cmyk": "C 49%, M 5%, Y 7%, K 0%",
    "cmyk_c": 49,
    "cmyk_k": 0,
    "cmyk_m": 5,
    "cmyk_profile": "Coated GRACoL 2006",
    "cmyk_y": 7,
    "extraction_method": "macOS Vision OCR + representative page visual checks; raw OCR not committed",
    "family": "natural",
    "label": "Sky Blue",
    "metrics_page_pdf": 223,
    "mood_tags": [
     "청량함",
     "평화",
     "유연함",
     "긍정",
     "맑음"
    ],
    "not_a_rule": true,
    "reference_reading_page_pdf": 222,
    "rgb_hex": "#87CEEB",
    "source_page_pdf": 222,
    "source_reference_id": "ref-reference-x-vol1-color",
    "spectrum": "blue",
    "spectrum_label_ko": "블루",
    "status": "cataloged",
    "summary": "Sky Blue is a Natural Blues keyword in the blue spectrum, defined from REFERENCE X Vol.1 with RGB/CMYK reference values and mood tags.",
    "swatch_page_pdf": 221,
    "tone_axes": [
     "high_value",
     "mid_chroma",
     "cool_bias"
    ]
   },
   "space": "concept",
   "type": "ColorKeyword"
  },
  {
   "id": "color-keyword-teal-blue",
   "properties": {
    "applies_when": {
     "color_family": [
      "natural",
      "any"
     ],
     "medium": [
      "digital",
      "print",
      "branding",
      "any"
     ],
     "spectrum": [
      "blue",
      "any"
     ]
    },
    "category": "Natural Blues",
    "cmyk": "C 82%, M 30%, Y 31%, K 7%",
    "cmyk_c": 82,
    "cmyk_k": 7,
    "cmyk_m": 30,
    "cmyk_profile": "Coated GRACoL 2006",
    "cmyk_y": 31,
    "extraction_method": "macOS Vision OCR + representative page visual checks; raw OCR not committed",
    "family": "natural",
    "label": "Teal Blue",
    "metrics_page_pdf": 226,
    "mood_tags": [
     "개방감",
     "에너지",
     "명료함",
     "신선함",
     "감각적"
    ],
    "not_a_rule": true,
    "reference_reading_page_pdf": 225,
    "rgb_hex": "#01889F",
    "source_page_pdf": 225,
    "source_reference_id": "ref-reference-x-vol1-color",
    "spectrum": "blue",
    "spectrum_label_ko": "블루",
    "status": "cataloged",
    "summary": "Teal Blue is a Natural Blues keyword in the blue spectrum, defined from REFERENCE X Vol.1 with RGB/CMYK reference values and mood tags.",
    "swatch_page_pdf": 224,
    "tone_axes": [
     "mid_value",
     "mid_chroma",
     "cool_bias"
    ]
   },
   "space": "concept",
   "type": "ColorKeyword"
  },
  {
   "id": "color-keyword-ocean-blue",
   "properties": {
    "applies_when": {
     "color_family": [
      "natural",
      "any"
     ],
     "medium": [
      "digital",
      "print",
      "branding",
      "any"
     ],
     "spectrum": [
      "blue",
      "any"
     ]
    },
    "category": "Natural Blues",
    "cmyk": "C 70%, M 26%, Y 33%, K 5%",
    "cmyk_c": 70,
    "cmyk_k": 5,
    "cmyk_m": 26,
    "cmyk_profile": "Coated GRACoL 2006",
    "cmyk_y": 33,
    "extraction_method": "macOS Vision OCR + representative page visual checks; raw OCR not committed",
    "family": "natural",
    "label": "Ocean Blue",
    "metrics_page_pdf": 229,
    "mood_tags": [
     "신뢰",
     "정화",
     "깊이감",
     "유연함",
     "안정감"
    ],
    "not_a_rule": true,
    "reference_reading_page_pdf": 228,
    "rgb_hex": "#4F97A3",
    "source_page_pdf": 228,
    "source_reference_id": "ref-reference-x-vol1-color",
    "spectrum": "blue",
    "spectrum_label_ko": "블루",
    "status": "cataloged",
    "summary": "Ocean Blue is a Natural Blues keyword in the blue spectrum, defined from REFERENCE X Vol.1 with RGB/CMYK reference values and mood tags.",
    "swatch_page_pdf": 227,
    "tone_axes": [
     "mid_value",
     "mid_chroma"
    ]
   },
   "space": "concept",
   "type": "ColorKeyword"
  },
  {
   "id": "color-keyword-navy-blue",
   "properties": {
    "applies_when": {
     "color_family": [
      "deep",
      "any"
     ],
     "medium": [
      "digital",
      "print",
      "branding",
      "any"
     ],
     "spectrum": [
      "blue",
      "any"
     ]
    },
    "category": "Deep Blues",
    "cmyk": "C 100%, M 99%, Y 23%, K 8%",
    "cmyk_c": 100,
    "cmyk_k": 8,
    "cmyk_m": 99,
    "cmyk_profile": "Coated GRACoL 2006",
    "cmyk_y": 23,
    "extraction_method": "macOS Vision OCR + representative page visual checks; raw OCR not committed",
    "family": "deep",
    "label": "Navy Blue",
    "metrics_page_pdf": 232,
    "mood_tags": [
     "신뢰",
     "권위",
     "집중",
     "전문성",
     "절제된 우아함"
    ],
    "not_a_rule": true,
    "reference_reading_page_pdf": 231,
    "rgb_hex": "#000080",
    "source_page_pdf": 231,
    "source_reference_id": "ref-reference-x-vol1-color",
    "spectrum": "blue",
    "spectrum_label_ko": "블루",
    "status": "cataloged",
    "summary": "Navy Blue is a Deep Blues keyword in the blue spectrum, defined from REFERENCE X Vol.1 with RGB/CMYK reference values and mood tags.",
    "swatch_page_pdf": 230,
    "tone_axes": [
     "low_value",
     "mid_chroma",
     "cool_bias"
    ]
   },
   "space": "concept",
   "type": "ColorKeyword"
  },
  {
   "id": "color-keyword-prussian-blue",
   "properties": {
    "applies_when": {
     "color_family": [
      "deep",
      "any"
     ],
     "medium": [
      "digital",
      "print",
      "branding",
      "any"
     ],
     "spectrum": [
      "blue",
      "any"
     ]
    },
    "category": "Deep Blues",
    "cmyk": "C 93%, M 68%, Y 42%, K 35%",
    "cmyk_c": 93,
    "cmyk_k": 35,
    "cmyk_m": 68,
    "cmyk_profile": "Coated GRACoL 2006",
    "cmyk_y": 42,
    "extraction_method": "macOS Vision OCR + representative page visual checks; raw OCR not committed",
    "family": "deep",
    "label": "Prussian Blue",
    "metrics_page_pdf": 235,
    "mood_tags": [
     "고전",
     "예술",
     "집중",
     "권위",
     "깊이감"
    ],
    "not_a_rule": true,
    "reference_reading_page_pdf": 234,
    "rgb_hex": "#003153",
    "source_page_pdf": 234,
    "source_reference_id": "ref-reference-x-vol1-color",
    "spectrum": "blue",
    "spectrum_label_ko": "블루",
    "status": "cataloged",
    "summary": "Prussian Blue is a Deep Blues keyword in the blue spectrum, defined from REFERENCE X Vol.1 with RGB/CMYK reference values and mood tags.",
    "swatch_page_pdf": 233,
    "tone_axes": [
     "low_value",
     "low_chroma",
     "cool_bias"
    ]
   },
   "space": "concept",
   "type": "ColorKeyword"
  },
  {
   "id": "color-keyword-ice-blue",
   "properties": {
    "applies_when": {
     "color_family": [
      "pastel",
      "any"
     ],
     "medium": [
      "digital",
      "print",
      "branding",
      "any"
     ],
     "spectrum": [
      "blue",
      "any"
     ]
    },
    "category": "Pastel Blues",
    "cmyk": "C 18%, M 3%, Y 2%, K 0%",
    "cmyk_c": 18,
    "cmyk_k": 0,
    "cmyk_m": 3,
    "cmyk_profile": "Coated GRACoL 2006",
    "cmyk_y": 2,
    "extraction_method": "macOS Vision OCR + representative page visual checks; raw OCR not committed",
    "family": "pastel",
    "label": "Ice Blue",
    "metrics_page_pdf": 238,
    "mood_tags": [
     "정제됨",
     "청결함",
     "섬세함",
     "평온",
     "투명"
    ],
    "not_a_rule": true,
    "reference_reading_page_pdf": 237,
    "rgb_hex": "#D6EAF8",
    "source_page_pdf": 237,
    "source_reference_id": "ref-reference-x-vol1-color",
    "spectrum": "blue",
    "spectrum_label_ko": "블루",
    "status": "cataloged",
    "summary": "Ice Blue is a Pastel Blues keyword in the blue spectrum, defined from REFERENCE X Vol.1 with RGB/CMYK reference values and mood tags.",
    "swatch_page_pdf": 236,
    "tone_axes": [
     "high_value",
     "low_chroma",
     "cool_bias",
     "pastel"
    ]
   },
   "space": "concept",
   "type": "ColorKeyword"
  },
  {
   "id": "color-keyword-powder-blue",
   "properties": {
    "applies_when": {
     "color_family": [
      "pastel",
      "any"
     ],
     "medium": [
      "digital",
      "print",
      "branding",
      "any"
     ],
     "spectrum": [
      "blue",
      "any"
     ]
    },
    "category": "Pastel Blues",
    "cmyk": "C 34%, M 1%, Y 12%, K 0%",
    "cmyk_c": 34,
    "cmyk_k": 0,
    "cmyk_m": 1,
    "cmyk_profile": "Coated GRACoL 2006",
    "cmyk_y": 12,
    "extraction_method": "macOS Vision OCR + representative page visual checks; raw OCR not committed",
    "family": "pastel",
    "label": "Powder Blue",
    "metrics_page_pdf": 241,
    "mood_tags": [
     "부드러움",
     "균형감",
     "온화함",
     "정제된 따뜻함"
    ],
    "not_a_rule": true,
    "reference_reading_page_pdf": 240,
    "rgb_hex": "#B0E0E6",
    "source_page_pdf": 240,
    "source_reference_id": "ref-reference-x-vol1-color",
    "spectrum": "blue",
    "spectrum_label_ko": "블루",
    "status": "cataloged",
    "summary": "Powder Blue is a Pastel Blues keyword in the blue spectrum, defined from REFERENCE X Vol.1 with RGB/CMYK reference values and mood tags.",
    "swatch_page_pdf": 239,
    "tone_axes": [
     "mid_value",
     "low_chroma",
     "pastel"
    ]
   },
   "space": "concept",
   "type": "ColorKeyword"
  },
  {
   "id": "color-keyword-misty-blue",
   "properties": {
    "applies_when": {
     "color_family": [
      "pastel",
      "any"
     ],
     "medium": [
      "digital",
      "print",
      "branding",
      "any"
     ],
     "spectrum": [
      "blue",
      "any"
     ]
    },
    "category": "Pastel Blues",
    "cmyk": "C 32%, M 17%, Y 0%, K 0%",
    "cmyk_c": 32,
    "cmyk_k": 0,
    "cmyk_m": 17,
    "cmyk_profile": "Coated GRACoL 2006",
    "cmyk_y": 0,
    "extraction_method": "macOS Vision OCR + representative page visual checks; raw OCR not committed",
    "family": "pastel",
    "label": "Misty Blue",
    "metrics_page_pdf": 244,
    "mood_tags": [
     "차분함",
     "사색적",
     "몽환적",
     "잔잔함",
     "감정의 여운"
    ],
    "not_a_rule": true,
    "reference_reading_page_pdf": 243,
    "rgb_hex": "#B5C7EB",
    "source_page_pdf": 243,
    "source_reference_id": "ref-reference-x-vol1-color",
    "spectrum": "blue",
    "spectrum_label_ko": "블루",
    "status": "cataloged",
    "summary": "Misty Blue is a Pastel Blues keyword in the blue spectrum, defined from REFERENCE X Vol.1 with RGB/CMYK reference values and mood tags.",
    "swatch_page_pdf": 242,
    "tone_axes": [
     "mid_value",
     "low_chroma",
     "cool_bias",
     "pastel"
    ]
   },
   "space": "concept",
   "type": "ColorKeyword"
  },
  {
   "id": "color-keyword-classic-blue",
   "properties": {
    "applies_when": {
     "color_family": [
      "pantone_trend",
      "any"
     ],
     "medium": [
      "digital",
      "print",
      "branding",
      "any"
     ],
     "spectrum": [
      "blue",
      "any"
     ]
    },
    "category": "Pantone Trend Blues",
    "cmyk": "C 97%, M 72%, Y 24%, K 9%",
    "cmyk_c": 97,
    "cmyk_k": 9,
    "cmyk_m": 72,
    "cmyk_profile": "Coated GRACoL 2006",
    "cmyk_y": 24,
    "extraction_method": "macOS Vision OCR + representative page visual checks; raw OCR not committed",
    "family": "pantone_trend",
    "label": "Classic Blue",
    "metrics_page_pdf": 247,
    "mood_tags": [
     "신뢰",
     "평온함",
     "지성",
     "안정감"
    ],
    "not_a_rule": true,
    "pantone_code": "Pantone 19-4052",
    "reference_reading_page_pdf": 246,
    "rgb_hex": "#0F4C81",
    "source_page_pdf": 246,
    "source_reference_id": "ref-reference-x-vol1-color",
    "spectrum": "blue",
    "spectrum_label_ko": "블루",
    "status": "cataloged",
    "summary": "Classic Blue is a Pantone Trend Blues keyword in the blue spectrum, defined from REFERENCE X Vol.1 with RGB/CMYK reference values and mood tags.",
    "swatch_page_pdf": 245,
    "tone_axes": [
     "mid_value",
     "low_value",
     "mid_chroma",
     "cool_bias"
    ]
   },
   "space": "concept",
   "type": "ColorKeyword"
  },
  {
   "id": "color-keyword-super-sonic",
   "properties": {
    "applies_when": {
     "color_family": [
      "pantone_trend",
      "any"
     ],
     "medium": [
      "digital",
      "print",
      "branding",
      "any"
     ],
     "spectrum": [
      "blue",
      "any"
     ]
    },
    "category": "Pantone Trend Blues",
    "cmyk": "C 88%, M 50%, Y 15%, K 3%",
    "cmyk_c": 88,
    "cmyk_k": 3,
    "cmyk_m": 50,
    "cmyk_profile": "Coated GRACoL 2006",
    "cmyk_y": 15,
    "extraction_method": "macOS Vision OCR + representative page visual checks; raw OCR not committed",
    "family": "pantone_trend",
    "label": "Super Sonic",
    "metrics_page_pdf": 250,
    "mood_tags": [
     "혁신적",
     "미래지향적",
     "역동적",
     "청량감",
     "에너지"
    ],
    "not_a_rule": true,
    "pantone_code": "Pantone 18-4143",
    "reference_reading_page_pdf": 249,
    "rgb_hex": "#0071A8",
    "source_page_pdf": 249,
    "source_reference_id": "ref-reference-x-vol1-color",
    "spectrum": "blue",
    "spectrum_label_ko": "블루",
    "status": "cataloged",
    "summary": "Super Sonic is a Pantone Trend Blues keyword in the blue spectrum, defined from REFERENCE X Vol.1 with RGB/CMYK reference values and mood tags.",
    "swatch_page_pdf": 248,
    "tone_axes": [
     "high_value",
     "high_chroma",
     "mid_chroma",
     "cool_bias"
    ]
   },
   "space": "concept",
   "type": "ColorKeyword"
  },
  {
   "id": "color-keyword-blue-atoll",
   "properties": {
    "applies_when": {
     "color_family": [
      "pantone_trend",
      "any"
     ],
     "medium": [
      "digital",
      "print",
      "branding",
      "any"
     ],
     "spectrum": [
      "blue",
      "any"
     ]
    },
    "category": "Pantone Trend Blues",
    "cmyk": "C 74%, M 12%, Y 17%, K 0%",
    "cmyk_c": 74,
    "cmyk_k": 0,
    "cmyk_m": 12,
    "cmyk_profile": "Coated GRACoL 2006",
    "cmyk_y": 17,
    "extraction_method": "macOS Vision OCR + representative page visual checks; raw OCR not committed",
    "family": "pantone_trend",
    "label": "Blue Atoll",
    "metrics_page_pdf": 253,
    "mood_tags": [
     "생기",
     "젊음",
     "휴양",
     "청량함",
     "모던함"
    ],
    "not_a_rule": true,
    "pantone_code": "Pantone 16-4535",
    "reference_reading_page_pdf": 252,
    "rgb_hex": "#00B1D2",
    "source_page_pdf": 252,
    "source_reference_id": "ref-reference-x-vol1-color",
    "spectrum": "blue",
    "spectrum_label_ko": "블루",
    "status": "cataloged",
    "summary": "Blue Atoll is a Pantone Trend Blues keyword in the blue spectrum, defined from REFERENCE X Vol.1 with RGB/CMYK reference values and mood tags.",
    "swatch_page_pdf": 251,
    "tone_axes": [
     "mid_value",
     "high_chroma",
     "cool_bias"
    ]
   },
   "space": "concept",
   "type": "ColorKeyword"
  },
  {
   "id": "color-keyword-cobalt-violet",
   "properties": {
    "applies_when": {
     "color_family": [
      "standard",
      "any"
     ],
     "medium": [
      "digital",
      "print",
      "branding",
      "any"
     ],
     "spectrum": [
      "violet",
      "any"
     ]
    },
    "category": "Standard Violets",
    "cmyk": "C 64%, M 81%, Y 0%, K 0%",
    "cmyk_c": 64,
    "cmyk_k": 0,
    "cmyk_m": 81,
    "cmyk_profile": "Coated GRACoL 2006",
    "cmyk_y": 0,
    "extraction_method": "macOS Vision OCR + representative page visual checks; raw OCR not committed",
    "family": "standard",
    "label": "Cobalt Violet",
    "metrics_page_pdf": 263,
    "mood_tags": [
     "안정감",
     "차분함",
     "예술적",
     "신비감"
    ],
    "not_a_rule": true,
    "reference_reading_page_pdf": 262,
    "rgb_hex": "#804AA8",
    "source_page_pdf": 262,
    "source_reference_id": "ref-reference-x-vol1-color",
    "spectrum": "violet",
    "spectrum_label_ko": "바이올렛",
    "status": "cataloged",
    "summary": "Cobalt Violet is a Standard Violets keyword in the violet spectrum, defined from REFERENCE X Vol.1 with RGB/CMYK reference values and mood tags.",
    "swatch_page_pdf": 261,
    "tone_axes": [
     "mid_value",
     "mid_chroma",
     "cool_bias"
    ]
   },
   "space": "concept",
   "type": "ColorKeyword"
  },
  {
   "id": "color-keyword-royal-purple",
   "properties": {
    "applies_when": {
     "color_family": [
      "standard",
      "any"
     ],
     "medium": [
      "digital",
      "print",
      "branding",
      "any"
     ],
     "spectrum": [
      "violet",
      "any"
     ]
    },
    "category": "Standard Violets",
    "cmyk": "C 74%, M 86%, Y 0%, K 0%",
    "cmyk_c": 74,
    "cmyk_k": 0,
    "cmyk_m": 86,
    "cmyk_profile": "Coated GRACoL 2006",
    "cmyk_y": 0,
    "extraction_method": "macOS Vision OCR + representative page visual checks; raw OCR not committed",
    "family": "standard",
    "label": "Royal Purple",
    "metrics_page_pdf": 266,
    "mood_tags": [
     "장엄함",
     "품격",
     "권위",
     "카리스마"
    ],
    "not_a_rule": true,
    "reference_reading_page_pdf": 265,
    "rgb_hex": "#6C3BAA",
    "source_page_pdf": 265,
    "source_reference_id": "ref-reference-x-vol1-color",
    "spectrum": "violet",
    "spectrum_label_ko": "바이올렛",
    "status": "cataloged",
    "summary": "Royal Purple is a Standard Violets keyword in the violet spectrum, defined from REFERENCE X Vol.1 with RGB/CMYK reference values and mood tags.",
    "swatch_page_pdf": 264,
    "tone_axes": [
     "mid_value",
     "high_chroma",
     "warm_bias"
    ]
   },
   "space": "concept",
   "type": "ColorKeyword"
  },
  {
   "id": "color-keyword-lavender-violet",
   "properties": {
    "applies_when": {
     "color_family": [
      "natural",
      "any"
     ],
     "medium": [
      "digital",
      "print",
      "branding",
      "any"
     ],
     "spectrum": [
      "violet",
      "any"
     ]
    },
    "category": "Natural Violets",
    "cmyk": "C 50%, M 57%, Y 4%, K 0%",
    "cmyk_c": 50,
    "cmyk_k": 0,
    "cmyk_m": 57,
    "cmyk_profile": "Coated GRACoL 2006",
    "cmyk_y": 4,
    "extraction_method": "macOS Vision OCR + representative page visual checks; raw OCR not committed",
    "family": "natural",
    "label": "Lavender Violet",
    "metrics_page_pdf": 269,
    "mood_tags": [
     "부드러움",
     "평온함",
     "세련",
     "낭만",
     "안정감"
    ],
    "not_a_rule": true,
    "reference_reading_page_pdf": 268,
    "rgb_hex": "#967BB6",
    "source_page_pdf": 268,
    "source_reference_id": "ref-reference-x-vol1-color",
    "spectrum": "violet",
    "spectrum_label_ko": "바이올렛",
    "status": "cataloged",
    "summary": "Lavender Violet is a Natural Violets keyword in the violet spectrum, defined from REFERENCE X Vol.1 with RGB/CMYK reference values and mood tags.",
    "swatch_page_pdf": 267,
    "tone_axes": [
     "high_value",
     "mid_chroma",
     "low_chroma"
    ]
   },
   "space": "concept",
   "type": "ColorKeyword"
  },
  {
   "id": "color-keyword-lilac-violet",
   "properties": {
    "applies_when": {
     "color_family": [
      "natural",
      "any"
     ],
     "medium": [
      "digital",
      "print",
      "branding",
      "any"
     ],
     "spectrum": [
      "violet",
      "any"
     ]
    },
    "category": "Natural Violets",
    "cmyk": "C 25%, M 41%, Y 5%, K 0%",
    "cmyk_c": 25,
    "cmyk_k": 0,
    "cmyk_m": 41,
    "cmyk_profile": "Coated GRACoL 2006",
    "cmyk_y": 5,
    "extraction_method": "macOS Vision OCR + representative page visual checks; raw OCR not committed",
    "family": "natural",
    "label": "Lilac Violet",
    "metrics_page_pdf": 272,
    "mood_tags": [
     "낭만적",
     "청초함",
     "감정적 여유",
     "몽환적"
    ],
    "not_a_rule": true,
    "reference_reading_page_pdf": 271,
    "rgb_hex": "#C8A2C8",
    "source_page_pdf": 271,
    "source_reference_id": "ref-reference-x-vol1-color",
    "spectrum": "violet",
    "spectrum_label_ko": "바이올렛",
    "status": "cataloged",
    "summary": "Lilac Violet is a Natural Violets keyword in the violet spectrum, defined from REFERENCE X Vol.1 with RGB/CMYK reference values and mood tags.",
    "swatch_page_pdf": 270,
    "tone_axes": [
     "mid_value",
     "low_chroma",
     "warm_bias"
    ]
   },
   "space": "concept",
   "type": "ColorKeyword"
  },
  {
   "id": "color-keyword-iris-violet",
   "properties": {
    "applies_when": {
     "color_family": [
      "natural",
      "any"
     ],
     "medium": [
      "digital",
      "print",
      "branding",
      "any"
     ],
     "spectrum": [
      "violet",
      "any"
     ]
    },
    "category": "Natural Violets",
    "cmyk": "C 80%, M 74%, Y 0%, K 0%",
    "cmyk_c": 80,
    "cmyk_k": 0,
    "cmyk_m": 74,
    "cmyk_profile": "Coated GRACoL 2006",
    "cmyk_y": 0,
    "extraction_method": "macOS Vision OCR + representative page visual checks; raw OCR not committed",
    "family": "natural",
    "label": "Iris Violet",
    "metrics_page_pdf": 275,
    "mood_tags": [
     "신성함",
     "예술적",
     "정제된 생동감",
     "상징적 존재감"
    ],
    "not_a_rule": true,
    "reference_reading_page_pdf": 274,
    "rgb_hex": "#5A4FCF",
    "source_page_pdf": 274,
    "source_reference_id": "ref-reference-x-vol1-color",
    "spectrum": "violet",
    "spectrum_label_ko": "바이올렛",
    "status": "cataloged",
    "summary": "Iris Violet is a Natural Violets keyword in the violet spectrum, defined from REFERENCE X Vol.1 with RGB/CMYK reference values and mood tags.",
    "swatch_page_pdf": 273,
    "tone_axes": [
     "mid_value",
     "high_chroma",
     "cool_bias"
    ]
   },
   "space": "concept",
   "type": "ColorKeyword"
  },
  {
   "id": "color-keyword-aubergine",
   "properties": {
    "applies_when": {
     "color_family": [
      "deep",
      "any"
     ],
     "medium": [
      "digital",
      "print",
      "branding",
      "any"
     ],
     "spectrum": [
      "violet",
      "any"
     ]
    },
    "category": "Deep Violets",
    "cmyk": "C 56%, M 73%, Y 43%, K 38%",
    "cmyk_c": 56,
    "cmyk_k": 38,
    "cmyk_m": 73,
    "cmyk_profile": "Coated GRACoL 2006",
    "cmyk_y": 43,
    "extraction_method": "macOS Vision OCR + representative page visual checks; raw OCR not committed",
    "family": "deep",
    "label": "Aubergine",
    "metrics_page_pdf": 278,
    "mood_tags": [
     "고혹적",
     "성숙함",
     "미스터리",
     "예술적",
     "긴장감"
    ],
    "not_a_rule": true,
    "reference_reading_page_pdf": 277,
    "rgb_hex": "#614051",
    "source_page_pdf": 277,
    "source_reference_id": "ref-reference-x-vol1-color",
    "spectrum": "violet",
    "spectrum_label_ko": "바이올렛",
    "status": "cataloged",
    "summary": "Aubergine is a Deep Violets keyword in the violet spectrum, defined from REFERENCE X Vol.1 with RGB/CMYK reference values and mood tags.",
    "swatch_page_pdf": 276,
    "tone_axes": [
     "low_value",
     "mid_chroma"
    ]
   },
   "space": "concept",
   "type": "ColorKeyword"
  },
  {
   "id": "color-keyword-byzantium",
   "properties": {
    "applies_when": {
     "color_family": [
      "deep",
      "any"
     ],
     "medium": [
      "digital",
      "print",
      "branding",
      "any"
     ],
     "spectrum": [
      "violet",
      "any"
     ]
    },
    "category": "Deep Violets",
    "cmyk": "C 62%, M 99%, Y 26%, K 18%",
    "cmyk_c": 62,
    "cmyk_k": 18,
    "cmyk_m": 99,
    "cmyk_profile": "Coated GRACoL 2006",
    "cmyk_y": 26,
    "extraction_method": "macOS Vision OCR + representative page visual checks; raw OCR not committed",
    "family": "deep",
    "label": "Byzantium",
    "metrics_page_pdf": 281,
    "mood_tags": [
     "고전적",
     "신비로움",
     "황홀함",
     "예술적 품격"
    ],
    "not_a_rule": true,
    "reference_reading_page_pdf": 280,
    "rgb_hex": "#702963",
    "source_page_pdf": 280,
    "source_reference_id": "ref-reference-x-vol1-color",
    "spectrum": "violet",
    "spectrum_label_ko": "바이올렛",
    "status": "cataloged",
    "summary": "Byzantium is a Deep Violets keyword in the violet spectrum, defined from REFERENCE X Vol.1 with RGB/CMYK reference values and mood tags.",
    "swatch_page_pdf": 279,
    "tone_axes": [
     "low_value",
     "high_chroma",
     "mid_chroma",
     "warm_bias"
    ]
   },
   "space": "concept",
   "type": "ColorKeyword"
  },
  {
   "id": "color-keyword-midnight-violet",
   "properties": {
    "applies_when": {
     "color_family": [
      "deep",
      "any"
     ],
     "medium": [
      "digital",
      "print",
      "branding",
      "any"
     ],
     "spectrum": [
      "violet",
      "any"
     ]
    },
    "category": "Deep Violets",
    "cmyk": "C 84%, M 90%, Y 32%, K 32%",
    "cmyk_c": 84,
    "cmyk_k": 32,
    "cmyk_m": 90,
    "cmyk_profile": "Coated GRACoL 2006",
    "cmyk_y": 32,
    "extraction_method": "macOS Vision OCR + representative page visual checks; raw OCR not committed",
    "family": "deep",
    "label": "Midnight Violet",
    "metrics_page_pdf": 284,
    "mood_tags": [
     "고요함",
     "신비",
     "절제된 감정",
     "내면적 깊이"
    ],
    "not_a_rule": true,
    "reference_reading_page_pdf": 283,
    "rgb_hex": "#2E1A47",
    "source_page_pdf": 283,
    "source_reference_id": "ref-reference-x-vol1-color",
    "spectrum": "violet",
    "spectrum_label_ko": "바이올렛",
    "status": "cataloged",
    "summary": "Midnight Violet is a Deep Violets keyword in the violet spectrum, defined from REFERENCE X Vol.1 with RGB/CMYK reference values and mood tags.",
    "swatch_page_pdf": 282,
    "tone_axes": [
     "low_value",
     "low_chroma",
     "cool_bias"
    ]
   },
   "space": "concept",
   "type": "ColorKeyword"
  },
  {
   "id": "color-keyword-periwinkle",
   "properties": {
    "applies_when": {
     "color_family": [
      "pastel",
      "any"
     ],
     "medium": [
      "digital",
      "print",
      "branding",
      "any"
     ],
     "spectrum": [
      "violet",
      "any"
     ]
    },
    "category": "Pastel Violets",
    "cmyk": "C 51%, M 38%, Y 0%, K 0%",
    "cmyk_c": 51,
    "cmyk_k": 0,
    "cmyk_m": 38,
    "cmyk_profile": "Coated GRACoL 2006",
    "cmyk_y": 0,
    "extraction_method": "macOS Vision OCR + representative page visual checks; raw OCR not committed",
    "family": "pastel",
    "label": "Periwinkle",
    "metrics_page_pdf": 287,
    "mood_tags": [
     "부드러움",
     "몽환",
     "순수함",
     "세련된 차분함"
    ],
    "not_a_rule": true,
    "reference_reading_page_pdf": 286,
    "rgb_hex": "#8E9AF1",
    "source_page_pdf": 286,
    "source_reference_id": "ref-reference-x-vol1-color",
    "spectrum": "violet",
    "spectrum_label_ko": "바이올렛",
    "status": "cataloged",
    "summary": "Periwinkle is a Pastel Violets keyword in the violet spectrum, defined from REFERENCE X Vol.1 with RGB/CMYK reference values and mood tags.",
    "swatch_page_pdf": 285,
    "tone_axes": [
     "mid_value",
     "low_chroma",
     "warm_bias",
     "cool_bias",
     "pastel"
    ]
   },
   "space": "concept",
   "type": "ColorKeyword"
  },
  {
   "id": "color-keyword-mauve",
   "properties": {
    "applies_when": {
     "color_family": [
      "pastel",
      "any"
     ],
     "medium": [
      "digital",
      "print",
      "branding",
      "any"
     ],
     "spectrum": [
      "violet",
      "any"
     ]
    },
    "category": "Pastel Violets",
    "cmyk": "C 21%, M 34%, Y 0%, K 0%",
    "cmyk_c": 21,
    "cmyk_k": 0,
    "cmyk_m": 34,
    "cmyk_profile": "Coated GRACoL 2006",
    "cmyk_y": 0,
    "extraction_method": "macOS Vision OCR + representative page visual checks; raw OCR not committed",
    "family": "pastel",
    "label": "Mauve",
    "metrics_page_pdf": 290,
    "mood_tags": [
     "낭만적",
     "세련됨",
     "회상적",
     "빈티지 무드"
    ],
    "not_a_rule": true,
    "reference_reading_page_pdf": 289,
    "rgb_hex": "#E0B0FF",
    "source_page_pdf": 289,
    "source_reference_id": "ref-reference-x-vol1-color",
    "spectrum": "violet",
    "spectrum_label_ko": "바이올렛",
    "status": "cataloged",
    "summary": "Mauve is a Pastel Violets keyword in the violet spectrum, defined from REFERENCE X Vol.1 with RGB/CMYK reference values and mood tags.",
    "swatch_page_pdf": 288,
    "tone_axes": [
     "mid_value",
     "low_chroma",
     "pastel"
    ]
   },
   "space": "concept",
   "type": "ColorKeyword"
  },
  {
   "id": "color-keyword-lavender-mist",
   "properties": {
    "applies_when": {
     "color_family": [
      "pastel",
      "any"
     ],
     "medium": [
      "digital",
      "print",
      "branding",
      "any"
     ],
     "spectrum": [
      "violet",
      "any"
     ]
    },
    "category": "Pastel Violets",
    "cmyk": "C 11%, M 9%, Y 0%, K 0%",
    "cmyk_c": 11,
    "cmyk_k": 0,
    "cmyk_m": 9,
    "cmyk_profile": "Coated GRACoL 2006",
    "cmyk_y": 0,
    "extraction_method": "macOS Vision OCR + representative page visual checks; raw OCR not committed",
    "family": "pastel",
    "label": "Lavender Mist",
    "metrics_page_pdf": 293,
    "mood_tags": [
     "청명함",
     "정화",
     "몽환",
     "세련된 차분함"
    ],
    "not_a_rule": true,
    "reference_reading_page_pdf": 292,
    "rgb_hex": "#E6E6FA",
    "source_page_pdf": 292,
    "source_reference_id": "ref-reference-x-vol1-color",
    "spectrum": "violet",
    "spectrum_label_ko": "바이올렛",
    "status": "cataloged",
    "summary": "Lavender Mist is a Pastel Violets keyword in the violet spectrum, defined from REFERENCE X Vol.1 with RGB/CMYK reference values and mood tags.",
    "swatch_page_pdf": 291,
    "tone_axes": [
     "high_value",
     "low_chroma",
     "cool_bias",
     "pastel"
    ]
   },
   "space": "concept",
   "type": "ColorKeyword"
  },
  {
   "id": "color-keyword-ultra-violet",
   "properties": {
    "applies_when": {
     "color_family": [
      "pantone_trend",
      "any"
     ],
     "medium": [
      "digital",
      "print",
      "branding",
      "any"
     ],
     "spectrum": [
      "violet",
      "any"
     ]
    },
    "category": "Pantone Trend Violets",
    "cmyk": "C 76%, M 79%, Y 15%, K 3%",
    "cmyk_c": 76,
    "cmyk_k": 3,
    "cmyk_m": 79,
    "cmyk_profile": "Coated GRACoL 2006",
    "cmyk_y": 15,
    "extraction_method": "macOS Vision OCR + representative page visual checks; raw OCR not committed",
    "family": "pantone_trend",
    "label": "Ultra Violet",
    "metrics_page_pdf": 296,
    "mood_tags": [
     "창의적",
     "신비감",
     "미래적",
     "실험적"
    ],
    "not_a_rule": true,
    "pantone_code": "Pantone 18-3838",
    "reference_reading_page_pdf": 295,
    "rgb_hex": "#5F4B8B",
    "source_page_pdf": 295,
    "source_reference_id": "ref-reference-x-vol1-color",
    "spectrum": "violet",
    "spectrum_label_ko": "바이올렛",
    "status": "cataloged",
    "summary": "Ultra Violet is a Pantone Trend Violets keyword in the violet spectrum, defined from REFERENCE X Vol.1 with RGB/CMYK reference values and mood tags.",
    "swatch_page_pdf": 294,
    "tone_axes": [
     "mid_value",
     "high_chroma",
     "mid_chroma"
    ]
   },
   "space": "concept",
   "type": "ColorKeyword"
  },
  {
   "id": "color-keyword-very-peri",
   "properties": {
    "applies_when": {
     "color_family": [
      "pantone_trend",
      "any"
     ],
     "medium": [
      "digital",
      "print",
      "branding",
      "any"
     ],
     "spectrum": [
      "violet",
      "any"
     ]
    },
    "category": "Pantone Trend Violets",
    "cmyk": "C 71%, M 64%, Y 6%, K 0%",
    "cmyk_c": 71,
    "cmyk_k": 0,
    "cmyk_m": 64,
    "cmyk_profile": "Coated GRACoL 2006",
    "cmyk_y": 6,
    "extraction_method": "macOS Vision OCR + representative page visual checks; raw OCR not committed",
    "family": "pantone_trend",
    "label": "Very Peri",
    "metrics_page_pdf": 299,
    "mood_tags": [
     "창조",
     "낙관적",
     "변화",
     "실험적"
    ],
    "not_a_rule": true,
    "pantone_code": "Pantone 17-3938",
    "reference_reading_page_pdf": 298,
    "rgb_hex": "#6667AB",
    "source_page_pdf": 298,
    "source_reference_id": "ref-reference-x-vol1-color",
    "spectrum": "violet",
    "spectrum_label_ko": "바이올렛",
    "status": "cataloged",
    "summary": "Very Peri is a Pantone Trend Violets keyword in the violet spectrum, defined from REFERENCE X Vol.1 with RGB/CMYK reference values and mood tags.",
    "swatch_page_pdf": 297,
    "tone_axes": [
     "mid_value",
     "mid_chroma",
     "warm_bias"
    ]
   },
   "space": "concept",
   "type": "ColorKeyword"
  },
  {
   "id": "color-keyword-grape-compote",
   "properties": {
    "applies_when": {
     "color_family": [
      "pantone_trend",
      "any"
     ],
     "medium": [
      "digital",
      "print",
      "branding",
      "any"
     ],
     "spectrum": [
      "violet",
      "any"
     ]
    },
    "category": "Pantone Trend Violets",
    "cmyk": "C 63%, M 66%, Y 32%, K 16%",
    "cmyk_c": 63,
    "cmyk_k": 16,
    "cmyk_m": 66,
    "cmyk_profile": "Coated GRACoL 2006",
    "cmyk_y": 32,
    "extraction_method": "macOS Vision OCR + representative page visual checks; raw OCR not committed",
    "family": "pantone_trend",
    "label": "Grape Compote",
    "metrics_page_pdf": 302,
    "mood_tags": [
     "차분",
     "세련",
     "내면적",
     "성숙함"
    ],
    "not_a_rule": true,
    "pantone_code": "Pantone 18-3513",
    "reference_reading_page_pdf": 301,
    "rgb_hex": "#6B5876",
    "source_page_pdf": 301,
    "source_reference_id": "ref-reference-x-vol1-color",
    "spectrum": "violet",
    "spectrum_label_ko": "바이올렛",
    "status": "cataloged",
    "summary": "Grape Compote is a Pantone Trend Violets keyword in the violet spectrum, defined from REFERENCE X Vol.1 with RGB/CMYK reference values and mood tags.",
    "swatch_page_pdf": 300,
    "tone_axes": [
     "low_value",
     "mid_chroma",
     "low_chroma"
    ]
   },
   "space": "concept",
   "type": "ColorKeyword"
  },
  {
   "id": "guideline-extended-keywords-name-anchor-only",
   "properties": {
    "label": "Extended keyword는 이름 anchor로만 쓴다",
    "not_a_rule": false,
    "source_pages_pdf": [
     60,
     112,
     161,
     208,
     254,
     303
    ],
    "source_reference_id": "ref-reference-x-vol1-color",
    "status": "cataloged",
    "summary": "Other {Spectrum} Keywords 목록의 색상명은 원본에 RGB/CMYK/metrics가 없는 name-only 항목이다. 검색어/명명/스펙트럼 분류 anchor로만 쓰고, 색상값이 필요하면 84개 main keyword나 별도 공개 출처를 쓴다."
   },
   "space": "concept",
   "type": "ColorGuideline"
  },
  {
   "id": "color-keyword-ext-carmine",
   "properties": {
    "applies_when": {
     "medium": [
      "any"
     ],
     "spectrum": [
      "red",
      "any"
     ]
    },
    "category": "Other Red Keywords",
    "extraction_method": "macOS/Claude page-image reading of the Other Keywords list pages; raw OCR not committed",
    "family": "extended",
    "label": "Carmine",
    "not_a_rule": true,
    "source_page_pdf": 60,
    "source_pages_pdf": [
     60
    ],
    "source_reference_id": "ref-reference-x-vol1-color",
    "spectra": [
     "red"
    ],
    "spectrum": "red",
    "spectrum_label_ko": "레드",
    "status": "cataloged",
    "summary": "Carmine is a name-only extended keyword from the REFERENCE X Other Red Keywords list. The source gives no RGB/CMYK/metrics for it; use it as a search and naming anchor.",
    "values_in_source": false
   },
   "space": "concept",
   "type": "ColorKeyword"
  },
  {
   "id": "color-keyword-ext-vermilion",
   "properties": {
    "applies_when": {
     "medium": [
      "any"
     ],
     "spectrum": [
      "red",
      "any"
     ]
    },
    "category": "Other Red Keywords",
    "extraction_method": "macOS/Claude page-image reading of the Other Keywords list pages; raw OCR not committed",
    "family": "extended",
    "label": "Vermilion",
    "not_a_rule": true,
    "source_page_pdf": 60,
    "source_pages_pdf": [
     60
    ],
    "source_reference_id": "ref-reference-x-vol1-color",
    "spectra": [
     "red"
    ],
    "spectrum": "red",
    "spectrum_label_ko": "레드",
    "status": "cataloged",
    "summary": "Vermilion is a name-only extended keyword from the REFERENCE X Other Red Keywords list. The source gives no RGB/CMYK/metrics for it; use it as a search and naming anchor.",
    "values_in_source": false
   },
   "space": "concept",
   "type": "ColorKeyword"
  },
  {
   "id": "color-keyword-ext-cinnabar",
   "properties": {
    "applies_when": {
     "medium": [
      "any"
     ],
     "spectrum": [
      "red",
      "any"
     ]
    },
    "category": "Other Red Keywords",
    "extraction_method": "macOS/Claude page-image reading of the Other Keywords list pages; raw OCR not committed",
    "family": "extended",
    "label": "Cinnabar",
    "not_a_rule": true,
    "source_page_pdf": 60,
    "source_pages_pdf": [
     60
    ],
    "source_reference_id": "ref-reference-x-vol1-color",
    "spectra": [
     "red"
    ],
    "spectrum": "red",
    "spectrum_label_ko": "레드",
    "status": "cataloged",
    "summary": "Cinnabar is a name-only extended keyword from the REFERENCE X Other Red Keywords list. The source gives no RGB/CMYK/metrics for it; use it as a search and naming anchor.",
    "values_in_source": false
   },
   "space": "concept",
   "type": "ColorKeyword"
  },
  {
   "id": "color-keyword-ext-cardinal",
   "properties": {
    "applies_when": {
     "medium": [
      "any"
     ],
     "spectrum": [
      "red",
      "any"
     ]
    },
    "category": "Other Red Keywords",
    "extraction_method": "macOS/Claude page-image reading of the Other Keywords list pages; raw OCR not committed",
    "family": "extended",
    "label": "Cardinal",
    "not_a_rule": true,
    "source_page_pdf": 60,
    "source_pages_pdf": [
     60
    ],
    "source_reference_id": "ref-reference-x-vol1-color",
    "spectra": [
     "red"
    ],
    "spectrum": "red",
    "spectrum_label_ko": "레드",
    "status": "cataloged",
    "summary": "Cardinal is a name-only extended keyword from the REFERENCE X Other Red Keywords list. The source gives no RGB/CMYK/metrics for it; use it as a search and naming anchor.",
    "values_in_source": false
   },
   "space": "concept",
   "type": "ColorKeyword"
  },
  {
   "id": "color-keyword-ext-firebrick",
   "properties": {
    "applies_when": {
     "medium": [
      "any"
     ],
     "spectrum": [
      "red",
      "any"
     ]
    },
    "category": "Other Red Keywords",
    "extraction_method": "macOS/Claude page-image reading of the Other Keywords list pages; raw OCR not committed",
    "family": "extended",
    "label": "Firebrick",
    "not_a_rule": true,
    "source_page_pdf": 60,
    "source_pages_pdf": [
     60
    ],
    "source_reference_id": "ref-reference-x-vol1-color",
    "spectra": [
     "red"
    ],
    "spectrum": "red",
    "spectrum_label_ko": "레드",
    "status": "cataloged",
    "summary": "Firebrick is a name-only extended keyword from the REFERENCE X Other Red Keywords list. The source gives no RGB/CMYK/metrics for it; use it as a search and naming anchor.",
    "values_in_source": false
   },
   "space": "concept",
   "type": "ColorKeyword"
  },
  {
   "id": "color-keyword-ext-candy-apple",
   "properties": {
    "applies_when": {
     "medium": [
      "any"
     ],
     "spectrum": [
      "red",
      "any"
     ]
    },
    "category": "Other Red Keywords",
    "extraction_method": "macOS/Claude page-image reading of the Other Keywords list pages; raw OCR not committed",
    "family": "extended",
    "label": "Candy Apple",
    "not_a_rule": true,
    "source_page_pdf": 60,
    "source_pages_pdf": [
     60
    ],
    "source_reference_id": "ref-reference-x-vol1-color",
    "spectra": [
     "red"
    ],
    "spectrum": "red",
    "spectrum_label_ko": "레드",
    "status": "cataloged",
    "summary": "Candy Apple is a name-only extended keyword from the REFERENCE X Other Red Keywords list. The source gives no RGB/CMYK/metrics for it; use it as a search and naming anchor.",
    "values_in_source": false
   },
   "space": "concept",
   "type": "ColorKeyword"
  },
  {
   "id": "color-keyword-ext-alizarin-crimson",
   "properties": {
    "applies_when": {
     "medium": [
      "any"
     ],
     "spectrum": [
      "red",
      "any"
     ]
    },
    "category": "Other Red Keywords",
    "extraction_method": "macOS/Claude page-image reading of the Other Keywords list pages; raw OCR not committed",
    "family": "extended",
    "label": "Alizarin Crimson",
    "not_a_rule": true,
    "source_page_pdf": 60,
    "source_pages_pdf": [
     60
    ],
    "source_reference_id": "ref-reference-x-vol1-color",
    "spectra": [
     "red"
    ],
    "spectrum": "red",
    "spectrum_label_ko": "레드",
    "status": "cataloged",
    "summary": "Alizarin Crimson is a name-only extended keyword from the REFERENCE X Other Red Keywords list. The source gives no RGB/CMYK/metrics for it; use it as a search and naming anchor.",
    "values_in_source": false
   },
   "space": "concept",
   "type": "ColorKeyword"
  },
  {
   "id": "color-keyword-ext-tomato",
   "properties": {
    "applies_when": {
     "medium": [
      "any"
     ],
     "spectrum": [
      "red",
      "any"
     ]
    },
    "category": "Other Red Keywords",
    "extraction_method": "macOS/Claude page-image reading of the Other Keywords list pages; raw OCR not committed",
    "family": "extended",
    "label": "Tomato",
    "not_a_rule": true,
    "source_page_pdf": 60,
    "source_pages_pdf": [
     60
    ],
    "source_reference_id": "ref-reference-x-vol1-color",
    "spectra": [
     "red"
    ],
    "spectrum": "red",
    "spectrum_label_ko": "레드",
    "status": "cataloged",
    "summary": "Tomato is a name-only extended keyword from the REFERENCE X Other Red Keywords list. The source gives no RGB/CMYK/metrics for it; use it as a search and naming anchor.",
    "values_in_source": false
   },
   "space": "concept",
   "type": "ColorKeyword"
  },
  {
   "id": "color-keyword-ext-chili",
   "properties": {
    "applies_when": {
     "medium": [
      "any"
     ],
     "spectrum": [
      "red",
      "any"
     ]
    },
    "category": "Other Red Keywords",
    "extraction_method": "macOS/Claude page-image reading of the Other Keywords list pages; raw OCR not committed",
    "family": "extended",
    "label": "Chili",
    "not_a_rule": true,
    "source_page_pdf": 60,
    "source_pages_pdf": [
     60
    ],
    "source_reference_id": "ref-reference-x-vol1-color",
    "spectra": [
     "red"
    ],
    "spectrum": "red",
    "spectrum_label_ko": "레드",
    "status": "cataloged",
    "summary": "Chili is a name-only extended keyword from the REFERENCE X Other Red Keywords list. The source gives no RGB/CMYK/metrics for it; use it as a search and naming anchor.",
    "values_in_source": false
   },
   "space": "concept",
   "type": "ColorKeyword"
  },
  {
   "id": "color-keyword-ext-maroon",
   "properties": {
    "applies_when": {
     "medium": [
      "any"
     ],
     "spectrum": [
      "red",
      "any"
     ]
    },
    "category": "Other Red Keywords",
    "extraction_method": "macOS/Claude page-image reading of the Other Keywords list pages; raw OCR not committed",
    "family": "extended",
    "label": "Maroon",
    "not_a_rule": true,
    "source_page_pdf": 60,
    "source_pages_pdf": [
     60
    ],
    "source_reference_id": "ref-reference-x-vol1-color",
    "spectra": [
     "red"
    ],
    "spectrum": "red",
    "spectrum_label_ko": "레드",
    "status": "cataloged",
    "summary": "Maroon is a name-only extended keyword from the REFERENCE X Other Red Keywords list. The source gives no RGB/CMYK/metrics for it; use it as a search and naming anchor.",
    "values_in_source": false
   },
   "space": "concept",
   "type": "ColorKeyword"
  },
  {
   "id": "color-keyword-ext-cherry",
   "properties": {
    "applies_when": {
     "medium": [
      "any"
     ],
     "spectrum": [
      "red",
      "any"
     ]
    },
    "category": "Other Red Keywords",
    "extraction_method": "macOS/Claude page-image reading of the Other Keywords list pages; raw OCR not committed",
    "family": "extended",
    "label": "Cherry",
    "not_a_rule": true,
    "source_page_pdf": 60,
    "source_pages_pdf": [
     60
    ],
    "source_reference_id": "ref-reference-x-vol1-color",
    "spectra": [
     "red"
    ],
    "spectrum": "red",
    "spectrum_label_ko": "레드",
    "status": "cataloged",
    "summary": "Cherry is a name-only extended keyword from the REFERENCE X Other Red Keywords list. The source gives no RGB/CMYK/metrics for it; use it as a search and naming anchor.",
    "values_in_source": false
   },
   "space": "concept",
   "type": "ColorKeyword"
  },
  {
   "id": "color-keyword-ext-garnet",
   "properties": {
    "applies_when": {
     "medium": [
      "any"
     ],
     "spectrum": [
      "red",
      "any"
     ]
    },
    "category": "Other Red Keywords",
    "extraction_method": "macOS/Claude page-image reading of the Other Keywords list pages; raw OCR not committed",
    "family": "extended",
    "label": "Garnet",
    "not_a_rule": true,
    "source_page_pdf": 60,
    "source_pages_pdf": [
     60
    ],
    "source_reference_id": "ref-reference-x-vol1-color",
    "spectra": [
     "red"
    ],
    "spectrum": "red",
    "spectrum_label_ko": "레드",
    "status": "cataloged",
    "summary": "Garnet is a name-only extended keyword from the REFERENCE X Other Red Keywords list. The source gives no RGB/CMYK/metrics for it; use it as a search and naming anchor.",
    "values_in_source": false
   },
   "space": "concept",
   "type": "ColorKeyword"
  },
  {
   "id": "color-keyword-ext-blood-red",
   "properties": {
    "applies_when": {
     "medium": [
      "any"
     ],
     "spectrum": [
      "red",
      "any"
     ]
    },
    "category": "Other Red Keywords",
    "extraction_method": "macOS/Claude page-image reading of the Other Keywords list pages; raw OCR not committed",
    "family": "extended",
    "label": "Blood Red",
    "not_a_rule": true,
    "source_page_pdf": 60,
    "source_pages_pdf": [
     60
    ],
    "source_reference_id": "ref-reference-x-vol1-color",
    "spectra": [
     "red"
    ],
    "spectrum": "red",
    "spectrum_label_ko": "레드",
    "status": "cataloged",
    "summary": "Blood Red is a name-only extended keyword from the REFERENCE X Other Red Keywords list. The source gives no RGB/CMYK/metrics for it; use it as a search and naming anchor.",
    "values_in_source": false
   },
   "space": "concept",
   "type": "ColorKeyword"
  },
  {
   "id": "color-keyword-ext-coke-red",
   "properties": {
    "applies_when": {
     "medium": [
      "any"
     ],
     "spectrum": [
      "red",
      "any"
     ]
    },
    "category": "Other Red Keywords",
    "extraction_method": "macOS/Claude page-image reading of the Other Keywords list pages; raw OCR not committed",
    "family": "extended",
    "label": "Coke Red",
    "not_a_rule": true,
    "source_page_pdf": 60,
    "source_pages_pdf": [
     60
    ],
    "source_reference_id": "ref-reference-x-vol1-color",
    "spectra": [
     "red"
    ],
    "spectrum": "red",
    "spectrum_label_ko": "레드",
    "status": "cataloged",
    "summary": "Coke Red is a name-only extended keyword from the REFERENCE X Other Red Keywords list. The source gives no RGB/CMYK/metrics for it; use it as a search and naming anchor.",
    "values_in_source": false
   },
   "space": "concept",
   "type": "ColorKeyword"
  },
  {
   "id": "color-keyword-ext-ferrari-red",
   "properties": {
    "applies_when": {
     "medium": [
      "any"
     ],
     "spectrum": [
      "red",
      "any"
     ]
    },
    "category": "Other Red Keywords",
    "extraction_method": "macOS/Claude page-image reading of the Other Keywords list pages; raw OCR not committed",
    "family": "extended",
    "label": "Ferrari Red",
    "not_a_rule": true,
    "source_page_pdf": 60,
    "source_pages_pdf": [
     60
    ],
    "source_reference_id": "ref-reference-x-vol1-color",
    "spectra": [
     "red"
    ],
    "spectrum": "red",
    "spectrum_label_ko": "레드",
    "status": "cataloged",
    "summary": "Ferrari Red is a name-only extended keyword from the REFERENCE X Other Red Keywords list. The source gives no RGB/CMYK/metrics for it; use it as a search and naming anchor.",
    "values_in_source": false
   },
   "space": "concept",
   "type": "ColorKeyword"
  },
  {
   "id": "color-keyword-ext-fire-engine-red",
   "properties": {
    "applies_when": {
     "medium": [
      "any"
     ],
     "spectrum": [
      "red",
      "any"
     ]
    },
    "category": "Other Red Keywords",
    "extraction_method": "macOS/Claude page-image reading of the Other Keywords list pages; raw OCR not committed",
    "family": "extended",
    "label": "Fire Engine Red",
    "not_a_rule": true,
    "source_page_pdf": 60,
    "source_pages_pdf": [
     60
    ],
    "source_reference_id": "ref-reference-x-vol1-color",
    "spectra": [
     "red"
    ],
    "spectrum": "red",
    "spectrum_label_ko": "레드",
    "status": "cataloged",
    "summary": "Fire Engine Red is a name-only extended keyword from the REFERENCE X Other Red Keywords list. The source gives no RGB/CMYK/metrics for it; use it as a search and naming anchor.",
    "values_in_source": false
   },
   "space": "concept",
   "type": "ColorKeyword"
  },
  {
   "id": "color-keyword-ext-ruby-red",
   "properties": {
    "applies_when": {
     "medium": [
      "any"
     ],
     "spectrum": [
      "red",
      "any"
     ]
    },
    "category": "Other Red Keywords",
    "extraction_method": "macOS/Claude page-image reading of the Other Keywords list pages; raw OCR not committed",
    "family": "extended",
    "label": "Ruby Red",
    "not_a_rule": true,
    "source_page_pdf": 60,
    "source_pages_pdf": [
     60
    ],
    "source_reference_id": "ref-reference-x-vol1-color",
    "spectra": [
     "red"
    ],
    "spectrum": "red",
    "spectrum_label_ko": "레드",
    "status": "cataloged",
    "summary": "Ruby Red is a name-only extended keyword from the REFERENCE X Other Red Keywords list. The source gives no RGB/CMYK/metrics for it; use it as a search and naming anchor.",
    "values_in_source": false
   },
   "space": "concept",
   "type": "ColorKeyword"
  },
  {
   "id": "color-keyword-ext-madder",
   "properties": {
    "applies_when": {
     "medium": [
      "any"
     ],
     "spectrum": [
      "red",
      "any"
     ]
    },
    "category": "Other Red Keywords",
    "extraction_method": "macOS/Claude page-image reading of the Other Keywords list pages; raw OCR not committed",
    "family": "extended",
    "label": "Madder",
    "not_a_rule": true,
    "source_page_pdf": 60,
    "source_pages_pdf": [
     60
    ],
    "source_reference_id": "ref-reference-x-vol1-color",
    "spectra": [
     "red"
    ],
    "spectrum": "red",
    "spectrum_label_ko": "레드",
    "status": "cataloged",
    "summary": "Madder is a name-only extended keyword from the REFERENCE X Other Red Keywords list. The source gives no RGB/CMYK/metrics for it; use it as a search and naming anchor.",
    "values_in_source": false
   },
   "space": "concept",
   "type": "ColorKeyword"
  },
  {
   "id": "color-keyword-ext-amaranth",
   "properties": {
    "applies_when": {
     "medium": [
      "any"
     ],
     "spectrum": [
      "red",
      "any"
     ]
    },
    "category": "Other Red Keywords",
    "extraction_method": "macOS/Claude page-image reading of the Other Keywords list pages; raw OCR not committed",
    "family": "extended",
    "label": "Amaranth",
    "not_a_rule": true,
    "source_page_pdf": 60,
    "source_pages_pdf": [
     60
    ],
    "source_reference_id": "ref-reference-x-vol1-color",
    "spectra": [
     "red"
    ],
    "spectrum": "red",
    "spectrum_label_ko": "레드",
    "status": "cataloged",
    "summary": "Amaranth is a name-only extended keyword from the REFERENCE X Other Red Keywords list. The source gives no RGB/CMYK/metrics for it; use it as a search and naming anchor.",
    "values_in_source": false
   },
   "space": "concept",
   "type": "ColorKeyword"
  },
  {
   "id": "color-keyword-ext-coquelicot",
   "properties": {
    "applies_when": {
     "medium": [
      "any"
     ],
     "spectrum": [
      "red",
      "any"
     ]
    },
    "category": "Other Red Keywords",
    "extraction_method": "macOS/Claude page-image reading of the Other Keywords list pages; raw OCR not committed",
    "family": "extended",
    "label": "Coquelicot",
    "not_a_rule": true,
    "source_page_pdf": 60,
    "source_pages_pdf": [
     60
    ],
    "source_reference_id": "ref-reference-x-vol1-color",
    "spectra": [
     "red"
    ],
    "spectrum": "red",
    "spectrum_label_ko": "레드",
    "status": "cataloged",
    "summary": "Coquelicot is a name-only extended keyword from the REFERENCE X Other Red Keywords list. The source gives no RGB/CMYK/metrics for it; use it as a search and naming anchor.",
    "values_in_source": false
   },
   "space": "concept",
   "type": "ColorKeyword"
  },
  {
   "id": "color-keyword-ext-redwood",
   "properties": {
    "applies_when": {
     "medium": [
      "any"
     ],
     "spectrum": [
      "red",
      "any"
     ]
    },
    "category": "Other Red Keywords",
    "extraction_method": "macOS/Claude page-image reading of the Other Keywords list pages; raw OCR not committed",
    "family": "extended",
    "label": "Redwood",
    "not_a_rule": true,
    "source_page_pdf": 60,
    "source_pages_pdf": [
     60
    ],
    "source_reference_id": "ref-reference-x-vol1-color",
    "spectra": [
     "red"
    ],
    "spectrum": "red",
    "spectrum_label_ko": "레드",
    "status": "cataloged",
    "summary": "Redwood is a name-only extended keyword from the REFERENCE X Other Red Keywords list. The source gives no RGB/CMYK/metrics for it; use it as a search and naming anchor.",
    "values_in_source": false
   },
   "space": "concept",
   "type": "ColorKeyword"
  },
  {
   "id": "color-keyword-ext-rust-red",
   "properties": {
    "applies_when": {
     "medium": [
      "any"
     ],
     "spectrum": [
      "red",
      "any"
     ]
    },
    "category": "Other Red Keywords",
    "extraction_method": "macOS/Claude page-image reading of the Other Keywords list pages; raw OCR not committed",
    "family": "extended",
    "label": "Rust Red",
    "not_a_rule": true,
    "source_page_pdf": 60,
    "source_pages_pdf": [
     60
    ],
    "source_reference_id": "ref-reference-x-vol1-color",
    "spectra": [
     "red"
    ],
    "spectrum": "red",
    "spectrum_label_ko": "레드",
    "status": "cataloged",
    "summary": "Rust Red is a name-only extended keyword from the REFERENCE X Other Red Keywords list. The source gives no RGB/CMYK/metrics for it; use it as a search and naming anchor.",
    "values_in_source": false
   },
   "space": "concept",
   "type": "ColorKeyword"
  },
  {
   "id": "color-keyword-ext-wine-red",
   "properties": {
    "applies_when": {
     "medium": [
      "any"
     ],
     "spectrum": [
      "red",
      "any"
     ]
    },
    "category": "Other Red Keywords",
    "extraction_method": "macOS/Claude page-image reading of the Other Keywords list pages; raw OCR not committed",
    "family": "extended",
    "label": "Wine Red",
    "not_a_rule": true,
    "source_page_pdf": 60,
    "source_pages_pdf": [
     60
    ],
    "source_reference_id": "ref-reference-x-vol1-color",
    "spectra": [
     "red"
    ],
    "spectrum": "red",
    "spectrum_label_ko": "레드",
    "status": "cataloged",
    "summary": "Wine Red is a name-only extended keyword from the REFERENCE X Other Red Keywords list. The source gives no RGB/CMYK/metrics for it; use it as a search and naming anchor.",
    "values_in_source": false
   },
   "space": "concept",
   "type": "ColorKeyword"
  },
  {
   "id": "color-keyword-ext-rosewood",
   "properties": {
    "applies_when": {
     "medium": [
      "any"
     ],
     "spectrum": [
      "red",
      "any"
     ]
    },
    "category": "Other Red Keywords",
    "extraction_method": "macOS/Claude page-image reading of the Other Keywords list pages; raw OCR not committed",
    "family": "extended",
    "label": "Rosewood",
    "not_a_rule": true,
    "source_page_pdf": 60,
    "source_pages_pdf": [
     60
    ],
    "source_reference_id": "ref-reference-x-vol1-color",
    "spectra": [
     "red"
    ],
    "spectrum": "red",
    "spectrum_label_ko": "레드",
    "status": "cataloged",
    "summary": "Rosewood is a name-only extended keyword from the REFERENCE X Other Red Keywords list. The source gives no RGB/CMYK/metrics for it; use it as a search and naming anchor.",
    "values_in_source": false
   },
   "space": "concept",
   "type": "ColorKeyword"
  },
  {
   "id": "color-keyword-ext-mahogany",
   "properties": {
    "applies_when": {
     "medium": [
      "any"
     ],
     "spectrum": [
      "red",
      "any"
     ]
    },
    "category": "Other Red Keywords",
    "extraction_method": "macOS/Claude page-image reading of the Other Keywords list pages; raw OCR not committed",
    "family": "extended",
    "label": "Mahogany",
    "not_a_rule": true,
    "source_page_pdf": 60,
    "source_pages_pdf": [
     60
    ],
    "source_reference_id": "ref-reference-x-vol1-color",
    "spectra": [
     "red"
    ],
    "spectrum": "red",
    "spectrum_label_ko": "레드",
    "status": "cataloged",
    "summary": "Mahogany is a name-only extended keyword from the REFERENCE X Other Red Keywords list. The source gives no RGB/CMYK/metrics for it; use it as a search and naming anchor.",
    "values_in_source": false
   },
   "space": "concept",
   "type": "ColorKeyword"
  },
  {
   "id": "color-keyword-ext-auburn",
   "properties": {
    "applies_when": {
     "medium": [
      "any"
     ],
     "spectrum": [
      "red",
      "any"
     ]
    },
    "category": "Other Red Keywords",
    "extraction_method": "macOS/Claude page-image reading of the Other Keywords list pages; raw OCR not committed",
    "family": "extended",
    "label": "Auburn",
    "not_a_rule": true,
    "source_page_pdf": 60,
    "source_pages_pdf": [
     60
    ],
    "source_reference_id": "ref-reference-x-vol1-color",
    "spectra": [
     "red"
    ],
    "spectrum": "red",
    "spectrum_label_ko": "레드",
    "status": "cataloged",
    "summary": "Auburn is a name-only extended keyword from the REFERENCE X Other Red Keywords list. The source gives no RGB/CMYK/metrics for it; use it as a search and naming anchor.",
    "values_in_source": false
   },
   "space": "concept",
   "type": "ColorKeyword"
  },
  {
   "id": "color-keyword-ext-carnelian",
   "properties": {
    "applies_when": {
     "medium": [
      "any"
     ],
     "spectrum": [
      "red",
      "any"
     ]
    },
    "category": "Other Red Keywords",
    "extraction_method": "macOS/Claude page-image reading of the Other Keywords list pages; raw OCR not committed",
    "family": "extended",
    "label": "Carnelian",
    "not_a_rule": true,
    "source_page_pdf": 60,
    "source_pages_pdf": [
     60
    ],
    "source_reference_id": "ref-reference-x-vol1-color",
    "spectra": [
     "red"
    ],
    "spectrum": "red",
    "spectrum_label_ko": "레드",
    "status": "cataloged",
    "summary": "Carnelian is a name-only extended keyword from the REFERENCE X Other Red Keywords list. The source gives no RGB/CMYK/metrics for it; use it as a search and naming anchor.",
    "values_in_source": false
   },
   "space": "concept",
   "type": "ColorKeyword"
  },
  {
   "id": "color-keyword-ext-cantaloupe",
   "properties": {
    "applies_when": {
     "medium": [
      "any"
     ],
     "spectrum": [
      "orange",
      "any"
     ]
    },
    "category": "Other Orange Keywords",
    "extraction_method": "macOS/Claude page-image reading of the Other Keywords list pages; raw OCR not committed",
    "family": "extended",
    "label": "Cantaloupe",
    "not_a_rule": true,
    "source_page_pdf": 112,
    "source_pages_pdf": [
     112
    ],
    "source_reference_id": "ref-reference-x-vol1-color",
    "spectra": [
     "orange"
    ],
    "spectrum": "orange",
    "spectrum_label_ko": "오렌지",
    "status": "cataloged",
    "summary": "Cantaloupe is a name-only extended keyword from the REFERENCE X Other Orange Keywords list. The source gives no RGB/CMYK/metrics for it; use it as a search and naming anchor.",
    "values_in_source": false
   },
   "space": "concept",
   "type": "ColorKeyword"
  },
  {
   "id": "color-keyword-ext-amber-glow",
   "properties": {
    "applies_when": {
     "medium": [
      "any"
     ],
     "spectrum": [
      "orange",
      "any"
     ]
    },
    "category": "Other Orange Keywords",
    "extraction_method": "macOS/Claude page-image reading of the Other Keywords list pages; raw OCR not committed",
    "family": "extended",
    "label": "Amber Glow",
    "not_a_rule": true,
    "source_page_pdf": 112,
    "source_pages_pdf": [
     112
    ],
    "source_reference_id": "ref-reference-x-vol1-color",
    "spectra": [
     "orange"
    ],
    "spectrum": "orange",
    "spectrum_label_ko": "오렌지",
    "status": "cataloged",
    "summary": "Amber Glow is a name-only extended keyword from the REFERENCE X Other Orange Keywords list. The source gives no RGB/CMYK/metrics for it; use it as a search and naming anchor.",
    "values_in_source": false
   },
   "space": "concept",
   "type": "ColorKeyword"
  },
  {
   "id": "color-keyword-ext-saffron",
   "properties": {
    "applies_when": {
     "medium": [
      "any"
     ],
     "spectrum": [
      "orange",
      "any"
     ]
    },
    "category": "Other Orange Keywords",
    "extraction_method": "macOS/Claude page-image reading of the Other Keywords list pages; raw OCR not committed",
    "family": "extended",
    "label": "Saffron",
    "not_a_rule": true,
    "source_page_pdf": 112,
    "source_pages_pdf": [
     112,
     161
    ],
    "source_reference_id": "ref-reference-x-vol1-color",
    "spectra": [
     "orange",
     "yellow"
    ],
    "spectrum": "orange",
    "spectrum_label_ko": "오렌지",
    "status": "cataloged",
    "summary": "Saffron is a name-only extended keyword from the REFERENCE X Other Orange Keywords list. The source gives no RGB/CMYK/metrics for it; use it as a search and naming anchor.",
    "values_in_source": false
   },
   "space": "concept",
   "type": "ColorKeyword"
  },
  {
   "id": "color-keyword-ext-butterscotch",
   "properties": {
    "applies_when": {
     "medium": [
      "any"
     ],
     "spectrum": [
      "orange",
      "any"
     ]
    },
    "category": "Other Orange Keywords",
    "extraction_method": "macOS/Claude page-image reading of the Other Keywords list pages; raw OCR not committed",
    "family": "extended",
    "label": "Butterscotch",
    "not_a_rule": true,
    "source_page_pdf": 112,
    "source_pages_pdf": [
     112
    ],
    "source_reference_id": "ref-reference-x-vol1-color",
    "spectra": [
     "orange"
    ],
    "spectrum": "orange",
    "spectrum_label_ko": "오렌지",
    "status": "cataloged",
    "summary": "Butterscotch is a name-only extended keyword from the REFERENCE X Other Orange Keywords list. The source gives no RGB/CMYK/metrics for it; use it as a search and naming anchor.",
    "values_in_source": false
   },
   "space": "concept",
   "type": "ColorKeyword"
  },
  {
   "id": "color-keyword-ext-marigold",
   "properties": {
    "applies_when": {
     "medium": [
      "any"
     ],
     "spectrum": [
      "orange",
      "any"
     ]
    },
    "category": "Other Orange Keywords",
    "extraction_method": "macOS/Claude page-image reading of the Other Keywords list pages; raw OCR not committed",
    "family": "extended",
    "label": "Marigold",
    "not_a_rule": true,
    "source_page_pdf": 112,
    "source_pages_pdf": [
     112
    ],
    "source_reference_id": "ref-reference-x-vol1-color",
    "spectra": [
     "orange"
    ],
    "spectrum": "orange",
    "spectrum_label_ko": "오렌지",
    "status": "cataloged",
    "summary": "Marigold is a name-only extended keyword from the REFERENCE X Other Orange Keywords list. The source gives no RGB/CMYK/metrics for it; use it as a search and naming anchor.",
    "values_in_source": false
   },
   "space": "concept",
   "type": "ColorKeyword"
  },
  {
   "id": "color-keyword-ext-amberlight",
   "properties": {
    "applies_when": {
     "medium": [
      "any"
     ],
     "spectrum": [
      "orange",
      "any"
     ]
    },
    "category": "Other Orange Keywords",
    "extraction_method": "macOS/Claude page-image reading of the Other Keywords list pages; raw OCR not committed",
    "family": "extended",
    "label": "Amberlight",
    "not_a_rule": true,
    "source_page_pdf": 112,
    "source_pages_pdf": [
     112
    ],
    "source_reference_id": "ref-reference-x-vol1-color",
    "spectra": [
     "orange"
    ],
    "spectrum": "orange",
    "spectrum_label_ko": "오렌지",
    "status": "cataloged",
    "summary": "Amberlight is a name-only extended keyword from the REFERENCE X Other Orange Keywords list. The source gives no RGB/CMYK/metrics for it; use it as a search and naming anchor.",
    "values_in_source": false
   },
   "space": "concept",
   "type": "ColorKeyword"
  },
  {
   "id": "color-keyword-ext-copperfield",
   "properties": {
    "applies_when": {
     "medium": [
      "any"
     ],
     "spectrum": [
      "orange",
      "any"
     ]
    },
    "category": "Other Orange Keywords",
    "extraction_method": "macOS/Claude page-image reading of the Other Keywords list pages; raw OCR not committed",
    "family": "extended",
    "label": "Copperfield",
    "not_a_rule": true,
    "source_page_pdf": 112,
    "source_pages_pdf": [
     112
    ],
    "source_reference_id": "ref-reference-x-vol1-color",
    "spectra": [
     "orange"
    ],
    "spectrum": "orange",
    "spectrum_label_ko": "오렌지",
    "status": "cataloged",
    "summary": "Copperfield is a name-only extended keyword from the REFERENCE X Other Orange Keywords list. The source gives no RGB/CMYK/metrics for it; use it as a search and naming anchor.",
    "values_in_source": false
   },
   "space": "concept",
   "type": "ColorKeyword"
  },
  {
   "id": "color-keyword-ext-tangelo",
   "properties": {
    "applies_when": {
     "medium": [
      "any"
     ],
     "spectrum": [
      "orange",
      "any"
     ]
    },
    "category": "Other Orange Keywords",
    "extraction_method": "macOS/Claude page-image reading of the Other Keywords list pages; raw OCR not committed",
    "family": "extended",
    "label": "Tangelo",
    "not_a_rule": true,
    "source_page_pdf": 112,
    "source_pages_pdf": [
     112
    ],
    "source_reference_id": "ref-reference-x-vol1-color",
    "spectra": [
     "orange"
    ],
    "spectrum": "orange",
    "spectrum_label_ko": "오렌지",
    "status": "cataloged",
    "summary": "Tangelo is a name-only extended keyword from the REFERENCE X Other Orange Keywords list. The source gives no RGB/CMYK/metrics for it; use it as a search and naming anchor.",
    "values_in_source": false
   },
   "space": "concept",
   "type": "ColorKeyword"
  },
  {
   "id": "color-keyword-ext-mango",
   "properties": {
    "applies_when": {
     "medium": [
      "any"
     ],
     "spectrum": [
      "orange",
      "any"
     ]
    },
    "category": "Other Orange Keywords",
    "extraction_method": "macOS/Claude page-image reading of the Other Keywords list pages; raw OCR not committed",
    "family": "extended",
    "label": "Mango",
    "not_a_rule": true,
    "source_page_pdf": 112,
    "source_pages_pdf": [
     112
    ],
    "source_reference_id": "ref-reference-x-vol1-color",
    "spectra": [
     "orange"
    ],
    "spectrum": "orange",
    "spectrum_label_ko": "오렌지",
    "status": "cataloged",
    "summary": "Mango is a name-only extended keyword from the REFERENCE X Other Orange Keywords list. The source gives no RGB/CMYK/metrics for it; use it as a search and naming anchor.",
    "values_in_source": false
   },
   "space": "concept",
   "type": "ColorKeyword"
  },
  {
   "id": "color-keyword-ext-mandarin",
   "properties": {
    "applies_when": {
     "medium": [
      "any"
     ],
     "spectrum": [
      "orange",
      "any"
     ]
    },
    "category": "Other Orange Keywords",
    "extraction_method": "macOS/Claude page-image reading of the Other Keywords list pages; raw OCR not committed",
    "family": "extended",
    "label": "Mandarin",
    "not_a_rule": true,
    "source_page_pdf": 112,
    "source_pages_pdf": [
     112
    ],
    "source_reference_id": "ref-reference-x-vol1-color",
    "spectra": [
     "orange"
    ],
    "spectrum": "orange",
    "spectrum_label_ko": "오렌지",
    "status": "cataloged",
    "summary": "Mandarin is a name-only extended keyword from the REFERENCE X Other Orange Keywords list. The source gives no RGB/CMYK/metrics for it; use it as a search and naming anchor.",
    "values_in_source": false
   },
   "space": "concept",
   "type": "ColorKeyword"
  },
  {
   "id": "color-keyword-ext-papaya",
   "properties": {
    "applies_when": {
     "medium": [
      "any"
     ],
     "spectrum": [
      "orange",
      "any"
     ]
    },
    "category": "Other Orange Keywords",
    "extraction_method": "macOS/Claude page-image reading of the Other Keywords list pages; raw OCR not committed",
    "family": "extended",
    "label": "Papaya",
    "not_a_rule": true,
    "source_page_pdf": 112,
    "source_pages_pdf": [
     112
    ],
    "source_reference_id": "ref-reference-x-vol1-color",
    "spectra": [
     "orange"
    ],
    "spectrum": "orange",
    "spectrum_label_ko": "오렌지",
    "status": "cataloged",
    "summary": "Papaya is a name-only extended keyword from the REFERENCE X Other Orange Keywords list. The source gives no RGB/CMYK/metrics for it; use it as a search and naming anchor.",
    "values_in_source": false
   },
   "space": "concept",
   "type": "ColorKeyword"
  },
  {
   "id": "color-keyword-ext-kumquat",
   "properties": {
    "applies_when": {
     "medium": [
      "any"
     ],
     "spectrum": [
      "orange",
      "any"
     ]
    },
    "category": "Other Orange Keywords",
    "extraction_method": "macOS/Claude page-image reading of the Other Keywords list pages; raw OCR not committed",
    "family": "extended",
    "label": "Kumquat",
    "not_a_rule": true,
    "source_page_pdf": 112,
    "source_pages_pdf": [
     112
    ],
    "source_reference_id": "ref-reference-x-vol1-color",
    "spectra": [
     "orange"
    ],
    "spectrum": "orange",
    "spectrum_label_ko": "오렌지",
    "status": "cataloged",
    "summary": "Kumquat is a name-only extended keyword from the REFERENCE X Other Orange Keywords list. The source gives no RGB/CMYK/metrics for it; use it as a search and naming anchor.",
    "values_in_source": false
   },
   "space": "concept",
   "type": "ColorKeyword"
  },
  {
   "id": "color-keyword-ext-sunset-orange",
   "properties": {
    "applies_when": {
     "medium": [
      "any"
     ],
     "spectrum": [
      "orange",
      "any"
     ]
    },
    "category": "Other Orange Keywords",
    "extraction_method": "macOS/Claude page-image reading of the Other Keywords list pages; raw OCR not committed",
    "family": "extended",
    "label": "Sunset Orange",
    "not_a_rule": true,
    "source_page_pdf": 112,
    "source_pages_pdf": [
     112
    ],
    "source_reference_id": "ref-reference-x-vol1-color",
    "spectra": [
     "orange"
    ],
    "spectrum": "orange",
    "spectrum_label_ko": "오렌지",
    "status": "cataloged",
    "summary": "Sunset Orange is a name-only extended keyword from the REFERENCE X Other Orange Keywords list. The source gives no RGB/CMYK/metrics for it; use it as a search and naming anchor.",
    "values_in_source": false
   },
   "space": "concept",
   "type": "ColorKeyword"
  },
  {
   "id": "color-keyword-ext-tigerlily",
   "properties": {
    "applies_when": {
     "medium": [
      "any"
     ],
     "spectrum": [
      "orange",
      "any"
     ]
    },
    "category": "Other Orange Keywords",
    "extraction_method": "macOS/Claude page-image reading of the Other Keywords list pages; raw OCR not committed",
    "family": "extended",
    "label": "Tigerlily",
    "not_a_rule": true,
    "source_page_pdf": 112,
    "source_pages_pdf": [
     112
    ],
    "source_reference_id": "ref-reference-x-vol1-color",
    "spectra": [
     "orange"
    ],
    "spectrum": "orange",
    "spectrum_label_ko": "오렌지",
    "status": "cataloged",
    "summary": "Tigerlily is a name-only extended keyword from the REFERENCE X Other Orange Keywords list. The source gives no RGB/CMYK/metrics for it; use it as a search and naming anchor.",
    "values_in_source": false
   },
   "space": "concept",
   "type": "ColorKeyword"
  },
  {
   "id": "color-keyword-ext-spice-orange",
   "properties": {
    "applies_when": {
     "medium": [
      "any"
     ],
     "spectrum": [
      "orange",
      "any"
     ]
    },
    "category": "Other Orange Keywords",
    "extraction_method": "macOS/Claude page-image reading of the Other Keywords list pages; raw OCR not committed",
    "family": "extended",
    "label": "Spice Orange",
    "not_a_rule": true,
    "source_page_pdf": 112,
    "source_pages_pdf": [
     112
    ],
    "source_reference_id": "ref-reference-x-vol1-color",
    "spectra": [
     "orange"
    ],
    "spectrum": "orange",
    "spectrum_label_ko": "오렌지",
    "status": "cataloged",
    "summary": "Spice Orange is a name-only extended keyword from the REFERENCE X Other Orange Keywords list. The source gives no RGB/CMYK/metrics for it; use it as a search and naming anchor.",
    "values_in_source": false
   },
   "space": "concept",
   "type": "ColorKeyword"
  },
  {
   "id": "color-keyword-ext-ginger",
   "properties": {
    "applies_when": {
     "medium": [
      "any"
     ],
     "spectrum": [
      "orange",
      "any"
     ]
    },
    "category": "Other Orange Keywords",
    "extraction_method": "macOS/Claude page-image reading of the Other Keywords list pages; raw OCR not committed",
    "family": "extended",
    "label": "Ginger",
    "not_a_rule": true,
    "source_page_pdf": 112,
    "source_pages_pdf": [
     112
    ],
    "source_reference_id": "ref-reference-x-vol1-color",
    "spectra": [
     "orange"
    ],
    "spectrum": "orange",
    "spectrum_label_ko": "오렌지",
    "status": "cataloged",
    "summary": "Ginger is a name-only extended keyword from the REFERENCE X Other Orange Keywords list. The source gives no RGB/CMYK/metrics for it; use it as a search and naming anchor.",
    "values_in_source": false
   },
   "space": "concept",
   "type": "ColorKeyword"
  },
  {
   "id": "color-keyword-ext-honeycomb",
   "properties": {
    "applies_when": {
     "medium": [
      "any"
     ],
     "spectrum": [
      "orange",
      "any"
     ]
    },
    "category": "Other Orange Keywords",
    "extraction_method": "macOS/Claude page-image reading of the Other Keywords list pages; raw OCR not committed",
    "family": "extended",
    "label": "Honeycomb",
    "not_a_rule": true,
    "source_page_pdf": 112,
    "source_pages_pdf": [
     112,
     161
    ],
    "source_reference_id": "ref-reference-x-vol1-color",
    "spectra": [
     "orange",
     "yellow"
    ],
    "spectrum": "orange",
    "spectrum_label_ko": "오렌지",
    "status": "cataloged",
    "summary": "Honeycomb is a name-only extended keyword from the REFERENCE X Other Orange Keywords list. The source gives no RGB/CMYK/metrics for it; use it as a search and naming anchor.",
    "values_in_source": false
   },
   "space": "concept",
   "type": "ColorKeyword"
  },
  {
   "id": "color-keyword-ext-sorbet",
   "properties": {
    "applies_when": {
     "medium": [
      "any"
     ],
     "spectrum": [
      "orange",
      "any"
     ]
    },
    "category": "Other Orange Keywords",
    "extraction_method": "macOS/Claude page-image reading of the Other Keywords list pages; raw OCR not committed",
    "family": "extended",
    "label": "Sorbet",
    "not_a_rule": true,
    "source_page_pdf": 112,
    "source_pages_pdf": [
     112
    ],
    "source_reference_id": "ref-reference-x-vol1-color",
    "spectra": [
     "orange"
    ],
    "spectrum": "orange",
    "spectrum_label_ko": "오렌지",
    "status": "cataloged",
    "summary": "Sorbet is a name-only extended keyword from the REFERENCE X Other Orange Keywords list. The source gives no RGB/CMYK/metrics for it; use it as a search and naming anchor.",
    "values_in_source": false
   },
   "space": "concept",
   "type": "ColorKeyword"
  },
  {
   "id": "color-keyword-ext-amber-clay",
   "properties": {
    "applies_when": {
     "medium": [
      "any"
     ],
     "spectrum": [
      "orange",
      "any"
     ]
    },
    "category": "Other Orange Keywords",
    "extraction_method": "macOS/Claude page-image reading of the Other Keywords list pages; raw OCR not committed",
    "family": "extended",
    "label": "Amber Clay",
    "not_a_rule": true,
    "source_page_pdf": 112,
    "source_pages_pdf": [
     112
    ],
    "source_reference_id": "ref-reference-x-vol1-color",
    "spectra": [
     "orange"
    ],
    "spectrum": "orange",
    "spectrum_label_ko": "오렌지",
    "status": "cataloged",
    "summary": "Amber Clay is a name-only extended keyword from the REFERENCE X Other Orange Keywords list. The source gives no RGB/CMYK/metrics for it; use it as a search and naming anchor.",
    "values_in_source": false
   },
   "space": "concept",
   "type": "ColorKeyword"
  },
  {
   "id": "color-keyword-ext-maple",
   "properties": {
    "applies_when": {
     "medium": [
      "any"
     ],
     "spectrum": [
      "orange",
      "any"
     ]
    },
    "category": "Other Orange Keywords",
    "extraction_method": "macOS/Claude page-image reading of the Other Keywords list pages; raw OCR not committed",
    "family": "extended",
    "label": "Maple",
    "not_a_rule": true,
    "source_page_pdf": 112,
    "source_pages_pdf": [
     112
    ],
    "source_reference_id": "ref-reference-x-vol1-color",
    "spectra": [
     "orange"
    ],
    "spectrum": "orange",
    "spectrum_label_ko": "오렌지",
    "status": "cataloged",
    "summary": "Maple is a name-only extended keyword from the REFERENCE X Other Orange Keywords list. The source gives no RGB/CMYK/metrics for it; use it as a search and naming anchor.",
    "values_in_source": false
   },
   "space": "concept",
   "type": "ColorKeyword"
  },
  {
   "id": "color-keyword-ext-golden-apricot",
   "properties": {
    "applies_when": {
     "medium": [
      "any"
     ],
     "spectrum": [
      "orange",
      "any"
     ]
    },
    "category": "Other Orange Keywords",
    "extraction_method": "macOS/Claude page-image reading of the Other Keywords list pages; raw OCR not committed",
    "family": "extended",
    "label": "Golden Apricot",
    "not_a_rule": true,
    "source_page_pdf": 112,
    "source_pages_pdf": [
     112
    ],
    "source_reference_id": "ref-reference-x-vol1-color",
    "spectra": [
     "orange"
    ],
    "spectrum": "orange",
    "spectrum_label_ko": "오렌지",
    "status": "cataloged",
    "summary": "Golden Apricot is a name-only extended keyword from the REFERENCE X Other Orange Keywords list. The source gives no RGB/CMYK/metrics for it; use it as a search and naming anchor.",
    "values_in_source": false
   },
   "space": "concept",
   "type": "ColorKeyword"
  },
  {
   "id": "color-keyword-ext-dune",
   "properties": {
    "applies_when": {
     "medium": [
      "any"
     ],
     "spectrum": [
      "orange",
      "any"
     ]
    },
    "category": "Other Orange Keywords",
    "extraction_method": "macOS/Claude page-image reading of the Other Keywords list pages; raw OCR not committed",
    "family": "extended",
    "label": "Dune",
    "not_a_rule": true,
    "source_page_pdf": 112,
    "source_pages_pdf": [
     112
    ],
    "source_reference_id": "ref-reference-x-vol1-color",
    "spectra": [
     "orange"
    ],
    "spectrum": "orange",
    "spectrum_label_ko": "오렌지",
    "status": "cataloged",
    "summary": "Dune is a name-only extended keyword from the REFERENCE X Other Orange Keywords list. The source gives no RGB/CMYK/metrics for it; use it as a search and naming anchor.",
    "values_in_source": false
   },
   "space": "concept",
   "type": "ColorKeyword"
  },
  {
   "id": "color-keyword-ext-canyon-clay",
   "properties": {
    "applies_when": {
     "medium": [
      "any"
     ],
     "spectrum": [
      "orange",
      "any"
     ]
    },
    "category": "Other Orange Keywords",
    "extraction_method": "macOS/Claude page-image reading of the Other Keywords list pages; raw OCR not committed",
    "family": "extended",
    "label": "Canyon Clay",
    "not_a_rule": true,
    "source_page_pdf": 112,
    "source_pages_pdf": [
     112
    ],
    "source_reference_id": "ref-reference-x-vol1-color",
    "spectra": [
     "orange"
    ],
    "spectrum": "orange",
    "spectrum_label_ko": "오렌지",
    "status": "cataloged",
    "summary": "Canyon Clay is a name-only extended keyword from the REFERENCE X Other Orange Keywords list. The source gives no RGB/CMYK/metrics for it; use it as a search and naming anchor.",
    "values_in_source": false
   },
   "space": "concept",
   "type": "ColorKeyword"
  },
  {
   "id": "color-keyword-ext-harvest-gold",
   "properties": {
    "applies_when": {
     "medium": [
      "any"
     ],
     "spectrum": [
      "orange",
      "any"
     ]
    },
    "category": "Other Orange Keywords",
    "extraction_method": "macOS/Claude page-image reading of the Other Keywords list pages; raw OCR not committed",
    "family": "extended",
    "label": "Harvest Gold",
    "not_a_rule": true,
    "source_page_pdf": 112,
    "source_pages_pdf": [
     112,
     161
    ],
    "source_reference_id": "ref-reference-x-vol1-color",
    "spectra": [
     "orange",
     "yellow"
    ],
    "spectrum": "orange",
    "spectrum_label_ko": "오렌지",
    "status": "cataloged",
    "summary": "Harvest Gold is a name-only extended keyword from the REFERENCE X Other Orange Keywords list. The source gives no RGB/CMYK/metrics for it; use it as a search and naming anchor.",
    "values_in_source": false
   },
   "space": "concept",
   "type": "ColorKeyword"
  },
  {
   "id": "color-keyword-ext-copper-dust",
   "properties": {
    "applies_when": {
     "medium": [
      "any"
     ],
     "spectrum": [
      "orange",
      "any"
     ]
    },
    "category": "Other Orange Keywords",
    "extraction_method": "macOS/Claude page-image reading of the Other Keywords list pages; raw OCR not committed",
    "family": "extended",
    "label": "Copper Dust",
    "not_a_rule": true,
    "source_page_pdf": 112,
    "source_pages_pdf": [
     112
    ],
    "source_reference_id": "ref-reference-x-vol1-color",
    "spectra": [
     "orange"
    ],
    "spectrum": "orange",
    "spectrum_label_ko": "오렌지",
    "status": "cataloged",
    "summary": "Copper Dust is a name-only extended keyword from the REFERENCE X Other Orange Keywords list. The source gives no RGB/CMYK/metrics for it; use it as a search and naming anchor.",
    "values_in_source": false
   },
   "space": "concept",
   "type": "ColorKeyword"
  },
  {
   "id": "color-keyword-ext-sandstone",
   "properties": {
    "applies_when": {
     "medium": [
      "any"
     ],
     "spectrum": [
      "orange",
      "any"
     ]
    },
    "category": "Other Orange Keywords",
    "extraction_method": "macOS/Claude page-image reading of the Other Keywords list pages; raw OCR not committed",
    "family": "extended",
    "label": "Sandstone",
    "not_a_rule": true,
    "source_page_pdf": 112,
    "source_pages_pdf": [
     112
    ],
    "source_reference_id": "ref-reference-x-vol1-color",
    "spectra": [
     "orange"
    ],
    "spectrum": "orange",
    "spectrum_label_ko": "오렌지",
    "status": "cataloged",
    "summary": "Sandstone is a name-only extended keyword from the REFERENCE X Other Orange Keywords list. The source gives no RGB/CMYK/metrics for it; use it as a search and naming anchor.",
    "values_in_source": false
   },
   "space": "concept",
   "type": "ColorKeyword"
  },
  {
   "id": "color-keyword-ext-autumn-glow",
   "properties": {
    "applies_when": {
     "medium": [
      "any"
     ],
     "spectrum": [
      "orange",
      "any"
     ]
    },
    "category": "Other Orange Keywords",
    "extraction_method": "macOS/Claude page-image reading of the Other Keywords list pages; raw OCR not committed",
    "family": "extended",
    "label": "Autumn Glow",
    "not_a_rule": true,
    "source_page_pdf": 112,
    "source_pages_pdf": [
     112
    ],
    "source_reference_id": "ref-reference-x-vol1-color",
    "spectra": [
     "orange"
    ],
    "spectrum": "orange",
    "spectrum_label_ko": "오렌지",
    "status": "cataloged",
    "summary": "Autumn Glow is a name-only extended keyword from the REFERENCE X Other Orange Keywords list. The source gives no RGB/CMYK/metrics for it; use it as a search and naming anchor.",
    "values_in_source": false
   },
   "space": "concept",
   "type": "ColorKeyword"
  },
  {
   "id": "color-keyword-ext-sunset-mist",
   "properties": {
    "applies_when": {
     "medium": [
      "any"
     ],
     "spectrum": [
      "orange",
      "any"
     ]
    },
    "category": "Other Orange Keywords",
    "extraction_method": "macOS/Claude page-image reading of the Other Keywords list pages; raw OCR not committed",
    "family": "extended",
    "label": "Sunset Mist",
    "not_a_rule": true,
    "source_page_pdf": 112,
    "source_pages_pdf": [
     112
    ],
    "source_reference_id": "ref-reference-x-vol1-color",
    "spectra": [
     "orange"
    ],
    "spectrum": "orange",
    "spectrum_label_ko": "오렌지",
    "status": "cataloged",
    "summary": "Sunset Mist is a name-only extended keyword from the REFERENCE X Other Orange Keywords list. The source gives no RGB/CMYK/metrics for it; use it as a search and naming anchor.",
    "values_in_source": false
   },
   "space": "concept",
   "type": "ColorKeyword"
  },
  {
   "id": "color-keyword-ext-gold-ochre",
   "properties": {
    "applies_when": {
     "medium": [
      "any"
     ],
     "spectrum": [
      "orange",
      "any"
     ]
    },
    "category": "Other Orange Keywords",
    "extraction_method": "macOS/Claude page-image reading of the Other Keywords list pages; raw OCR not committed",
    "family": "extended",
    "label": "Gold Ochre",
    "not_a_rule": true,
    "source_page_pdf": 112,
    "source_pages_pdf": [
     112
    ],
    "source_reference_id": "ref-reference-x-vol1-color",
    "spectra": [
     "orange"
    ],
    "spectrum": "orange",
    "spectrum_label_ko": "오렌지",
    "status": "cataloged",
    "summary": "Gold Ochre is a name-only extended keyword from the REFERENCE X Other Orange Keywords list. The source gives no RGB/CMYK/metrics for it; use it as a search and naming anchor.",
    "values_in_source": false
   },
   "space": "concept",
   "type": "ColorKeyword"
  },
  {
   "id": "color-keyword-ext-warm-terracotta",
   "properties": {
    "applies_when": {
     "medium": [
      "any"
     ],
     "spectrum": [
      "orange",
      "any"
     ]
    },
    "category": "Other Orange Keywords",
    "extraction_method": "macOS/Claude page-image reading of the Other Keywords list pages; raw OCR not committed",
    "family": "extended",
    "label": "Warm Terracotta",
    "not_a_rule": true,
    "source_page_pdf": 112,
    "source_pages_pdf": [
     112
    ],
    "source_reference_id": "ref-reference-x-vol1-color",
    "spectra": [
     "orange"
    ],
    "spectrum": "orange",
    "spectrum_label_ko": "오렌지",
    "status": "cataloged",
    "summary": "Warm Terracotta is a name-only extended keyword from the REFERENCE X Other Orange Keywords list. The source gives no RGB/CMYK/metrics for it; use it as a search and naming anchor.",
    "values_in_source": false
   },
   "space": "concept",
   "type": "ColorKeyword"
  },
  {
   "id": "color-keyword-ext-canary-yellow",
   "properties": {
    "applies_when": {
     "medium": [
      "any"
     ],
     "spectrum": [
      "yellow",
      "any"
     ]
    },
    "category": "Other Yellow Keywords",
    "extraction_method": "macOS/Claude page-image reading of the Other Keywords list pages; raw OCR not committed",
    "family": "extended",
    "label": "Canary Yellow",
    "not_a_rule": true,
    "source_page_pdf": 161,
    "source_pages_pdf": [
     161
    ],
    "source_reference_id": "ref-reference-x-vol1-color",
    "spectra": [
     "yellow"
    ],
    "spectrum": "yellow",
    "spectrum_label_ko": "옐로",
    "status": "cataloged",
    "summary": "Canary Yellow is a name-only extended keyword from the REFERENCE X Other Yellow Keywords list. The source gives no RGB/CMYK/metrics for it; use it as a search and naming anchor.",
    "values_in_source": false
   },
   "space": "concept",
   "type": "ColorKeyword"
  },
  {
   "id": "color-keyword-ext-golden-yellow",
   "properties": {
    "applies_when": {
     "medium": [
      "any"
     ],
     "spectrum": [
      "yellow",
      "any"
     ]
    },
    "category": "Other Yellow Keywords",
    "extraction_method": "macOS/Claude page-image reading of the Other Keywords list pages; raw OCR not committed",
    "family": "extended",
    "label": "Golden Yellow",
    "not_a_rule": true,
    "source_page_pdf": 161,
    "source_pages_pdf": [
     161
    ],
    "source_reference_id": "ref-reference-x-vol1-color",
    "spectra": [
     "yellow"
    ],
    "spectrum": "yellow",
    "spectrum_label_ko": "옐로",
    "status": "cataloged",
    "summary": "Golden Yellow is a name-only extended keyword from the REFERENCE X Other Yellow Keywords list. The source gives no RGB/CMYK/metrics for it; use it as a search and naming anchor.",
    "values_in_source": false
   },
   "space": "concept",
   "type": "ColorKeyword"
  },
  {
   "id": "color-keyword-ext-maize",
   "properties": {
    "applies_when": {
     "medium": [
      "any"
     ],
     "spectrum": [
      "yellow",
      "any"
     ]
    },
    "category": "Other Yellow Keywords",
    "extraction_method": "macOS/Claude page-image reading of the Other Keywords list pages; raw OCR not committed",
    "family": "extended",
    "label": "Maize",
    "not_a_rule": true,
    "source_page_pdf": 161,
    "source_pages_pdf": [
     161
    ],
    "source_reference_id": "ref-reference-x-vol1-color",
    "spectra": [
     "yellow"
    ],
    "spectrum": "yellow",
    "spectrum_label_ko": "옐로",
    "status": "cataloged",
    "summary": "Maize is a name-only extended keyword from the REFERENCE X Other Yellow Keywords list. The source gives no RGB/CMYK/metrics for it; use it as a search and naming anchor.",
    "values_in_source": false
   },
   "space": "concept",
   "type": "ColorKeyword"
  },
  {
   "id": "color-keyword-ext-jonquil",
   "properties": {
    "applies_when": {
     "medium": [
      "any"
     ],
     "spectrum": [
      "yellow",
      "any"
     ]
    },
    "category": "Other Yellow Keywords",
    "extraction_method": "macOS/Claude page-image reading of the Other Keywords list pages; raw OCR not committed",
    "family": "extended",
    "label": "Jonquil",
    "not_a_rule": true,
    "source_page_pdf": 161,
    "source_pages_pdf": [
     161
    ],
    "source_reference_id": "ref-reference-x-vol1-color",
    "spectra": [
     "yellow"
    ],
    "spectrum": "yellow",
    "spectrum_label_ko": "옐로",
    "status": "cataloged",
    "summary": "Jonquil is a name-only extended keyword from the REFERENCE X Other Yellow Keywords list. The source gives no RGB/CMYK/metrics for it; use it as a search and naming anchor.",
    "values_in_source": false
   },
   "space": "concept",
   "type": "ColorKeyword"
  },
  {
   "id": "color-keyword-ext-sand-yellow",
   "properties": {
    "applies_when": {
     "medium": [
      "any"
     ],
     "spectrum": [
      "yellow",
      "any"
     ]
    },
    "category": "Other Yellow Keywords",
    "extraction_method": "macOS/Claude page-image reading of the Other Keywords list pages; raw OCR not committed",
    "family": "extended",
    "label": "Sand Yellow",
    "not_a_rule": true,
    "source_page_pdf": 161,
    "source_pages_pdf": [
     161
    ],
    "source_reference_id": "ref-reference-x-vol1-color",
    "spectra": [
     "yellow"
    ],
    "spectrum": "yellow",
    "spectrum_label_ko": "옐로",
    "status": "cataloged",
    "summary": "Sand Yellow is a name-only extended keyword from the REFERENCE X Other Yellow Keywords list. The source gives no RGB/CMYK/metrics for it; use it as a search and naming anchor.",
    "values_in_source": false
   },
   "space": "concept",
   "type": "ColorKeyword"
  },
  {
   "id": "color-keyword-ext-goldfinch",
   "properties": {
    "applies_when": {
     "medium": [
      "any"
     ],
     "spectrum": [
      "yellow",
      "any"
     ]
    },
    "category": "Other Yellow Keywords",
    "extraction_method": "macOS/Claude page-image reading of the Other Keywords list pages; raw OCR not committed",
    "family": "extended",
    "label": "Goldfinch",
    "not_a_rule": true,
    "source_page_pdf": 161,
    "source_pages_pdf": [
     161
    ],
    "source_reference_id": "ref-reference-x-vol1-color",
    "spectra": [
     "yellow"
    ],
    "spectrum": "yellow",
    "spectrum_label_ko": "옐로",
    "status": "cataloged",
    "summary": "Goldfinch is a name-only extended keyword from the REFERENCE X Other Yellow Keywords list. The source gives no RGB/CMYK/metrics for it; use it as a search and naming anchor.",
    "values_in_source": false
   },
   "space": "concept",
   "type": "ColorKeyword"
  },
  {
   "id": "color-keyword-ext-vanilla",
   "properties": {
    "applies_when": {
     "medium": [
      "any"
     ],
     "spectrum": [
      "yellow",
      "any"
     ]
    },
    "category": "Other Yellow Keywords",
    "extraction_method": "macOS/Claude page-image reading of the Other Keywords list pages; raw OCR not committed",
    "family": "extended",
    "label": "Vanilla",
    "not_a_rule": true,
    "source_page_pdf": 161,
    "source_pages_pdf": [
     161
    ],
    "source_reference_id": "ref-reference-x-vol1-color",
    "spectra": [
     "yellow"
    ],
    "spectrum": "yellow",
    "spectrum_label_ko": "옐로",
    "status": "cataloged",
    "summary": "Vanilla is a name-only extended keyword from the REFERENCE X Other Yellow Keywords list. The source gives no RGB/CMYK/metrics for it; use it as a search and naming anchor.",
    "values_in_source": false
   },
   "space": "concept",
   "type": "ColorKeyword"
  },
  {
   "id": "color-keyword-ext-straw",
   "properties": {
    "applies_when": {
     "medium": [
      "any"
     ],
     "spectrum": [
      "yellow",
      "any"
     ]
    },
    "category": "Other Yellow Keywords",
    "extraction_method": "macOS/Claude page-image reading of the Other Keywords list pages; raw OCR not committed",
    "family": "extended",
    "label": "Straw",
    "not_a_rule": true,
    "source_page_pdf": 161,
    "source_pages_pdf": [
     161
    ],
    "source_reference_id": "ref-reference-x-vol1-color",
    "spectra": [
     "yellow"
    ],
    "spectrum": "yellow",
    "spectrum_label_ko": "옐로",
    "status": "cataloged",
    "summary": "Straw is a name-only extended keyword from the REFERENCE X Other Yellow Keywords list. The source gives no RGB/CMYK/metrics for it; use it as a search and naming anchor.",
    "values_in_source": false
   },
   "space": "concept",
   "type": "ColorKeyword"
  },
  {
   "id": "color-keyword-ext-lemonade",
   "properties": {
    "applies_when": {
     "medium": [
      "any"
     ],
     "spectrum": [
      "yellow",
      "any"
     ]
    },
    "category": "Other Yellow Keywords",
    "extraction_method": "macOS/Claude page-image reading of the Other Keywords list pages; raw OCR not committed",
    "family": "extended",
    "label": "Lemonade",
    "not_a_rule": true,
    "source_page_pdf": 161,
    "source_pages_pdf": [
     161
    ],
    "source_reference_id": "ref-reference-x-vol1-color",
    "spectra": [
     "yellow"
    ],
    "spectrum": "yellow",
    "spectrum_label_ko": "옐로",
    "status": "cataloged",
    "summary": "Lemonade is a name-only extended keyword from the REFERENCE X Other Yellow Keywords list. The source gives no RGB/CMYK/metrics for it; use it as a search and naming anchor.",
    "values_in_source": false
   },
   "space": "concept",
   "type": "ColorKeyword"
  },
  {
   "id": "color-keyword-ext-sunshine",
   "properties": {
    "applies_when": {
     "medium": [
      "any"
     ],
     "spectrum": [
      "yellow",
      "any"
     ]
    },
    "category": "Other Yellow Keywords",
    "extraction_method": "macOS/Claude page-image reading of the Other Keywords list pages; raw OCR not committed",
    "family": "extended",
    "label": "Sunshine",
    "not_a_rule": true,
    "source_page_pdf": 161,
    "source_pages_pdf": [
     161
    ],
    "source_reference_id": "ref-reference-x-vol1-color",
    "spectra": [
     "yellow"
    ],
    "spectrum": "yellow",
    "spectrum_label_ko": "옐로",
    "status": "cataloged",
    "summary": "Sunshine is a name-only extended keyword from the REFERENCE X Other Yellow Keywords list. The source gives no RGB/CMYK/metrics for it; use it as a search and naming anchor.",
    "values_in_source": false
   },
   "space": "concept",
   "type": "ColorKeyword"
  },
  {
   "id": "color-keyword-ext-pale-daffodil",
   "properties": {
    "applies_when": {
     "medium": [
      "any"
     ],
     "spectrum": [
      "yellow",
      "any"
     ]
    },
    "category": "Other Yellow Keywords",
    "extraction_method": "macOS/Claude page-image reading of the Other Keywords list pages; raw OCR not committed",
    "family": "extended",
    "label": "Pale Daffodil",
    "not_a_rule": true,
    "source_page_pdf": 161,
    "source_pages_pdf": [
     161
    ],
    "source_reference_id": "ref-reference-x-vol1-color",
    "spectra": [
     "yellow"
    ],
    "spectrum": "yellow",
    "spectrum_label_ko": "옐로",
    "status": "cataloged",
    "summary": "Pale Daffodil is a name-only extended keyword from the REFERENCE X Other Yellow Keywords list. The source gives no RGB/CMYK/metrics for it; use it as a search and naming anchor.",
    "values_in_source": false
   },
   "space": "concept",
   "type": "ColorKeyword"
  },
  {
   "id": "color-keyword-ext-desert-gold",
   "properties": {
    "applies_when": {
     "medium": [
      "any"
     ],
     "spectrum": [
      "yellow",
      "any"
     ]
    },
    "category": "Other Yellow Keywords",
    "extraction_method": "macOS/Claude page-image reading of the Other Keywords list pages; raw OCR not committed",
    "family": "extended",
    "label": "Desert Gold",
    "not_a_rule": true,
    "source_page_pdf": 161,
    "source_pages_pdf": [
     161
    ],
    "source_reference_id": "ref-reference-x-vol1-color",
    "spectra": [
     "yellow"
    ],
    "spectrum": "yellow",
    "spectrum_label_ko": "옐로",
    "status": "cataloged",
    "summary": "Desert Gold is a name-only extended keyword from the REFERENCE X Other Yellow Keywords list. The source gives no RGB/CMYK/metrics for it; use it as a search and naming anchor.",
    "values_in_source": false
   },
   "space": "concept",
   "type": "ColorKeyword"
  },
  {
   "id": "color-keyword-ext-golden-haze",
   "properties": {
    "applies_when": {
     "medium": [
      "any"
     ],
     "spectrum": [
      "yellow",
      "any"
     ]
    },
    "category": "Other Yellow Keywords",
    "extraction_method": "macOS/Claude page-image reading of the Other Keywords list pages; raw OCR not committed",
    "family": "extended",
    "label": "Golden Haze",
    "not_a_rule": true,
    "source_page_pdf": 161,
    "source_pages_pdf": [
     161
    ],
    "source_reference_id": "ref-reference-x-vol1-color",
    "spectra": [
     "yellow"
    ],
    "spectrum": "yellow",
    "spectrum_label_ko": "옐로",
    "status": "cataloged",
    "summary": "Golden Haze is a name-only extended keyword from the REFERENCE X Other Yellow Keywords list. The source gives no RGB/CMYK/metrics for it; use it as a search and naming anchor.",
    "values_in_source": false
   },
   "space": "concept",
   "type": "ColorKeyword"
  },
  {
   "id": "color-keyword-ext-sunflower",
   "properties": {
    "applies_when": {
     "medium": [
      "any"
     ],
     "spectrum": [
      "yellow",
      "any"
     ]
    },
    "category": "Other Yellow Keywords",
    "extraction_method": "macOS/Claude page-image reading of the Other Keywords list pages; raw OCR not committed",
    "family": "extended",
    "label": "Sunflower",
    "not_a_rule": true,
    "source_page_pdf": 161,
    "source_pages_pdf": [
     161
    ],
    "source_reference_id": "ref-reference-x-vol1-color",
    "spectra": [
     "yellow"
    ],
    "spectrum": "yellow",
    "spectrum_label_ko": "옐로",
    "status": "cataloged",
    "summary": "Sunflower is a name-only extended keyword from the REFERENCE X Other Yellow Keywords list. The source gives no RGB/CMYK/metrics for it; use it as a search and naming anchor.",
    "values_in_source": false
   },
   "space": "concept",
   "type": "ColorKeyword"
  },
  {
   "id": "color-keyword-ext-amber-gold",
   "properties": {
    "applies_when": {
     "medium": [
      "any"
     ],
     "spectrum": [
      "yellow",
      "any"
     ]
    },
    "category": "Other Yellow Keywords",
    "extraction_method": "macOS/Claude page-image reading of the Other Keywords list pages; raw OCR not committed",
    "family": "extended",
    "label": "Amber Gold",
    "not_a_rule": true,
    "source_page_pdf": 161,
    "source_pages_pdf": [
     161
    ],
    "source_reference_id": "ref-reference-x-vol1-color",
    "spectra": [
     "yellow"
    ],
    "spectrum": "yellow",
    "spectrum_label_ko": "옐로",
    "status": "cataloged",
    "summary": "Amber Gold is a name-only extended keyword from the REFERENCE X Other Yellow Keywords list. The source gives no RGB/CMYK/metrics for it; use it as a search and naming anchor.",
    "values_in_source": false
   },
   "space": "concept",
   "type": "ColorKeyword"
  },
  {
   "id": "color-keyword-ext-flaxseed",
   "properties": {
    "applies_when": {
     "medium": [
      "any"
     ],
     "spectrum": [
      "yellow",
      "any"
     ]
    },
    "category": "Other Yellow Keywords",
    "extraction_method": "macOS/Claude page-image reading of the Other Keywords list pages; raw OCR not committed",
    "family": "extended",
    "label": "Flaxseed",
    "not_a_rule": true,
    "source_page_pdf": 161,
    "source_pages_pdf": [
     161
    ],
    "source_reference_id": "ref-reference-x-vol1-color",
    "spectra": [
     "yellow"
    ],
    "spectrum": "yellow",
    "spectrum_label_ko": "옐로",
    "status": "cataloged",
    "summary": "Flaxseed is a name-only extended keyword from the REFERENCE X Other Yellow Keywords list. The source gives no RGB/CMYK/metrics for it; use it as a search and naming anchor.",
    "values_in_source": false
   },
   "space": "concept",
   "type": "ColorKeyword"
  },
  {
   "id": "color-keyword-ext-light-khaki",
   "properties": {
    "applies_when": {
     "medium": [
      "any"
     ],
     "spectrum": [
      "yellow",
      "any"
     ]
    },
    "category": "Other Yellow Keywords",
    "extraction_method": "macOS/Claude page-image reading of the Other Keywords list pages; raw OCR not committed",
    "family": "extended",
    "label": "Light Khaki",
    "not_a_rule": true,
    "source_page_pdf": 161,
    "source_pages_pdf": [
     161
    ],
    "source_reference_id": "ref-reference-x-vol1-color",
    "spectra": [
     "yellow"
    ],
    "spectrum": "yellow",
    "spectrum_label_ko": "옐로",
    "status": "cataloged",
    "summary": "Light Khaki is a name-only extended keyword from the REFERENCE X Other Yellow Keywords list. The source gives no RGB/CMYK/metrics for it; use it as a search and naming anchor.",
    "values_in_source": false
   },
   "space": "concept",
   "type": "ColorKeyword"
  },
  {
   "id": "color-keyword-ext-blond",
   "properties": {
    "applies_when": {
     "medium": [
      "any"
     ],
     "spectrum": [
      "yellow",
      "any"
     ]
    },
    "category": "Other Yellow Keywords",
    "extraction_method": "macOS/Claude page-image reading of the Other Keywords list pages; raw OCR not committed",
    "family": "extended",
    "label": "Blond",
    "not_a_rule": true,
    "source_page_pdf": 161,
    "source_pages_pdf": [
     161
    ],
    "source_reference_id": "ref-reference-x-vol1-color",
    "spectra": [
     "yellow"
    ],
    "spectrum": "yellow",
    "spectrum_label_ko": "옐로",
    "status": "cataloged",
    "summary": "Blond is a name-only extended keyword from the REFERENCE X Other Yellow Keywords list. The source gives no RGB/CMYK/metrics for it; use it as a search and naming anchor.",
    "values_in_source": false
   },
   "space": "concept",
   "type": "ColorKeyword"
  },
  {
   "id": "color-keyword-ext-candlelight",
   "properties": {
    "applies_when": {
     "medium": [
      "any"
     ],
     "spectrum": [
      "yellow",
      "any"
     ]
    },
    "category": "Other Yellow Keywords",
    "extraction_method": "macOS/Claude page-image reading of the Other Keywords list pages; raw OCR not committed",
    "family": "extended",
    "label": "Candlelight",
    "not_a_rule": true,
    "source_page_pdf": 161,
    "source_pages_pdf": [
     161
    ],
    "source_reference_id": "ref-reference-x-vol1-color",
    "spectra": [
     "yellow"
    ],
    "spectrum": "yellow",
    "spectrum_label_ko": "옐로",
    "status": "cataloged",
    "summary": "Candlelight is a name-only extended keyword from the REFERENCE X Other Yellow Keywords list. The source gives no RGB/CMYK/metrics for it; use it as a search and naming anchor.",
    "values_in_source": false
   },
   "space": "concept",
   "type": "ColorKeyword"
  },
  {
   "id": "color-keyword-ext-honeydew",
   "properties": {
    "applies_when": {
     "medium": [
      "any"
     ],
     "spectrum": [
      "yellow",
      "any"
     ]
    },
    "category": "Other Yellow Keywords",
    "extraction_method": "macOS/Claude page-image reading of the Other Keywords list pages; raw OCR not committed",
    "family": "extended",
    "label": "Honeydew",
    "not_a_rule": true,
    "source_page_pdf": 161,
    "source_pages_pdf": [
     161
    ],
    "source_reference_id": "ref-reference-x-vol1-color",
    "spectra": [
     "yellow"
    ],
    "spectrum": "yellow",
    "spectrum_label_ko": "옐로",
    "status": "cataloged",
    "summary": "Honeydew is a name-only extended keyword from the REFERENCE X Other Yellow Keywords list. The source gives no RGB/CMYK/metrics for it; use it as a search and naming anchor.",
    "values_in_source": false
   },
   "space": "concept",
   "type": "ColorKeyword"
  },
  {
   "id": "color-keyword-ext-solar-flare",
   "properties": {
    "applies_when": {
     "medium": [
      "any"
     ],
     "spectrum": [
      "yellow",
      "any"
     ]
    },
    "category": "Other Yellow Keywords",
    "extraction_method": "macOS/Claude page-image reading of the Other Keywords list pages; raw OCR not committed",
    "family": "extended",
    "label": "Solar Flare",
    "not_a_rule": true,
    "source_page_pdf": 161,
    "source_pages_pdf": [
     161
    ],
    "source_reference_id": "ref-reference-x-vol1-color",
    "spectra": [
     "yellow"
    ],
    "spectrum": "yellow",
    "spectrum_label_ko": "옐로",
    "status": "cataloged",
    "summary": "Solar Flare is a name-only extended keyword from the REFERENCE X Other Yellow Keywords list. The source gives no RGB/CMYK/metrics for it; use it as a search and naming anchor.",
    "values_in_source": false
   },
   "space": "concept",
   "type": "ColorKeyword"
  },
  {
   "id": "color-keyword-ext-sunshine-gold",
   "properties": {
    "applies_when": {
     "medium": [
      "any"
     ],
     "spectrum": [
      "yellow",
      "any"
     ]
    },
    "category": "Other Yellow Keywords",
    "extraction_method": "macOS/Claude page-image reading of the Other Keywords list pages; raw OCR not committed",
    "family": "extended",
    "label": "Sunshine Gold",
    "not_a_rule": true,
    "source_page_pdf": 161,
    "source_pages_pdf": [
     161
    ],
    "source_reference_id": "ref-reference-x-vol1-color",
    "spectra": [
     "yellow"
    ],
    "spectrum": "yellow",
    "spectrum_label_ko": "옐로",
    "status": "cataloged",
    "summary": "Sunshine Gold is a name-only extended keyword from the REFERENCE X Other Yellow Keywords list. The source gives no RGB/CMYK/metrics for it; use it as a search and naming anchor.",
    "values_in_source": false
   },
   "space": "concept",
   "type": "ColorKeyword"
  },
  {
   "id": "color-keyword-ext-dijon",
   "properties": {
    "applies_when": {
     "medium": [
      "any"
     ],
     "spectrum": [
      "yellow",
      "any"
     ]
    },
    "category": "Other Yellow Keywords",
    "extraction_method": "macOS/Claude page-image reading of the Other Keywords list pages; raw OCR not committed",
    "family": "extended",
    "label": "Dijon",
    "not_a_rule": true,
    "source_page_pdf": 161,
    "source_pages_pdf": [
     161
    ],
    "source_reference_id": "ref-reference-x-vol1-color",
    "spectra": [
     "yellow"
    ],
    "spectrum": "yellow",
    "spectrum_label_ko": "옐로",
    "status": "cataloged",
    "summary": "Dijon is a name-only extended keyword from the REFERENCE X Other Yellow Keywords list. The source gives no RGB/CMYK/metrics for it; use it as a search and naming anchor.",
    "values_in_source": false
   },
   "space": "concept",
   "type": "ColorKeyword"
  },
  {
   "id": "color-keyword-ext-corn-yellow",
   "properties": {
    "applies_when": {
     "medium": [
      "any"
     ],
     "spectrum": [
      "yellow",
      "any"
     ]
    },
    "category": "Other Yellow Keywords",
    "extraction_method": "macOS/Claude page-image reading of the Other Keywords list pages; raw OCR not committed",
    "family": "extended",
    "label": "Corn Yellow",
    "not_a_rule": true,
    "source_page_pdf": 161,
    "source_pages_pdf": [
     161
    ],
    "source_reference_id": "ref-reference-x-vol1-color",
    "spectra": [
     "yellow"
    ],
    "spectrum": "yellow",
    "spectrum_label_ko": "옐로",
    "status": "cataloged",
    "summary": "Corn Yellow is a name-only extended keyword from the REFERENCE X Other Yellow Keywords list. The source gives no RGB/CMYK/metrics for it; use it as a search and naming anchor.",
    "values_in_source": false
   },
   "space": "concept",
   "type": "ColorKeyword"
  },
  {
   "id": "color-keyword-ext-honey",
   "properties": {
    "applies_when": {
     "medium": [
      "any"
     ],
     "spectrum": [
      "yellow",
      "any"
     ]
    },
    "category": "Other Yellow Keywords",
    "extraction_method": "macOS/Claude page-image reading of the Other Keywords list pages; raw OCR not committed",
    "family": "extended",
    "label": "Honey",
    "not_a_rule": true,
    "source_page_pdf": 161,
    "source_pages_pdf": [
     161
    ],
    "source_reference_id": "ref-reference-x-vol1-color",
    "spectra": [
     "yellow"
    ],
    "spectrum": "yellow",
    "spectrum_label_ko": "옐로",
    "status": "cataloged",
    "summary": "Honey is a name-only extended keyword from the REFERENCE X Other Yellow Keywords list. The source gives no RGB/CMYK/metrics for it; use it as a search and naming anchor.",
    "values_in_source": false
   },
   "space": "concept",
   "type": "ColorKeyword"
  },
  {
   "id": "color-keyword-ext-butter",
   "properties": {
    "applies_when": {
     "medium": [
      "any"
     ],
     "spectrum": [
      "yellow",
      "any"
     ]
    },
    "category": "Other Yellow Keywords",
    "extraction_method": "macOS/Claude page-image reading of the Other Keywords list pages; raw OCR not committed",
    "family": "extended",
    "label": "Butter",
    "not_a_rule": true,
    "source_page_pdf": 161,
    "source_pages_pdf": [
     161
    ],
    "source_reference_id": "ref-reference-x-vol1-color",
    "spectra": [
     "yellow"
    ],
    "spectrum": "yellow",
    "spectrum_label_ko": "옐로",
    "status": "cataloged",
    "summary": "Butter is a name-only extended keyword from the REFERENCE X Other Yellow Keywords list. The source gives no RGB/CMYK/metrics for it; use it as a search and naming anchor.",
    "values_in_source": false
   },
   "space": "concept",
   "type": "ColorKeyword"
  },
  {
   "id": "color-keyword-ext-curry",
   "properties": {
    "applies_when": {
     "medium": [
      "any"
     ],
     "spectrum": [
      "yellow",
      "any"
     ]
    },
    "category": "Other Yellow Keywords",
    "extraction_method": "macOS/Claude page-image reading of the Other Keywords list pages; raw OCR not committed",
    "family": "extended",
    "label": "Curry",
    "not_a_rule": true,
    "source_page_pdf": 161,
    "source_pages_pdf": [
     161
    ],
    "source_reference_id": "ref-reference-x-vol1-color",
    "spectra": [
     "yellow"
    ],
    "spectrum": "yellow",
    "spectrum_label_ko": "옐로",
    "status": "cataloged",
    "summary": "Curry is a name-only extended keyword from the REFERENCE X Other Yellow Keywords list. The source gives no RGB/CMYK/metrics for it; use it as a search and naming anchor.",
    "values_in_source": false
   },
   "space": "concept",
   "type": "ColorKeyword"
  },
  {
   "id": "color-keyword-ext-banana",
   "properties": {
    "applies_when": {
     "medium": [
      "any"
     ],
     "spectrum": [
      "yellow",
      "any"
     ]
    },
    "category": "Other Yellow Keywords",
    "extraction_method": "macOS/Claude page-image reading of the Other Keywords list pages; raw OCR not committed",
    "family": "extended",
    "label": "Banana",
    "not_a_rule": true,
    "source_page_pdf": 161,
    "source_pages_pdf": [
     161
    ],
    "source_reference_id": "ref-reference-x-vol1-color",
    "spectra": [
     "yellow"
    ],
    "spectrum": "yellow",
    "spectrum_label_ko": "옐로",
    "status": "cataloged",
    "summary": "Banana is a name-only extended keyword from the REFERENCE X Other Yellow Keywords list. The source gives no RGB/CMYK/metrics for it; use it as a search and naming anchor.",
    "values_in_source": false
   },
   "space": "concept",
   "type": "ColorKeyword"
  },
  {
   "id": "color-keyword-ext-chartreuse-yellow",
   "properties": {
    "applies_when": {
     "medium": [
      "any"
     ],
     "spectrum": [
      "yellow",
      "any"
     ]
    },
    "category": "Other Yellow Keywords",
    "extraction_method": "macOS/Claude page-image reading of the Other Keywords list pages; raw OCR not committed",
    "family": "extended",
    "label": "Chartreuse Yellow",
    "not_a_rule": true,
    "source_page_pdf": 161,
    "source_pages_pdf": [
     161
    ],
    "source_reference_id": "ref-reference-x-vol1-color",
    "spectra": [
     "yellow"
    ],
    "spectrum": "yellow",
    "spectrum_label_ko": "옐로",
    "status": "cataloged",
    "summary": "Chartreuse Yellow is a name-only extended keyword from the REFERENCE X Other Yellow Keywords list. The source gives no RGB/CMYK/metrics for it; use it as a search and naming anchor.",
    "values_in_source": false
   },
   "space": "concept",
   "type": "ColorKeyword"
  },
  {
   "id": "color-keyword-ext-aloe",
   "properties": {
    "applies_when": {
     "medium": [
      "any"
     ],
     "spectrum": [
      "green",
      "any"
     ]
    },
    "category": "Other Green Keywords",
    "extraction_method": "macOS/Claude page-image reading of the Other Keywords list pages; raw OCR not committed",
    "family": "extended",
    "label": "Aloe",
    "not_a_rule": true,
    "source_page_pdf": 208,
    "source_pages_pdf": [
     208
    ],
    "source_reference_id": "ref-reference-x-vol1-color",
    "spectra": [
     "green"
    ],
    "spectrum": "green",
    "spectrum_label_ko": "그린",
    "status": "cataloged",
    "summary": "Aloe is a name-only extended keyword from the REFERENCE X Other Green Keywords list. The source gives no RGB/CMYK/metrics for it; use it as a search and naming anchor.",
    "values_in_source": false
   },
   "space": "concept",
   "type": "ColorKeyword"
  },
  {
   "id": "color-keyword-ext-basil-green",
   "properties": {
    "applies_when": {
     "medium": [
      "any"
     ],
     "spectrum": [
      "green",
      "any"
     ]
    },
    "category": "Other Green Keywords",
    "extraction_method": "macOS/Claude page-image reading of the Other Keywords list pages; raw OCR not committed",
    "family": "extended",
    "label": "Basil Green",
    "not_a_rule": true,
    "source_page_pdf": 208,
    "source_pages_pdf": [
     208
    ],
    "source_reference_id": "ref-reference-x-vol1-color",
    "spectra": [
     "green"
    ],
    "spectrum": "green",
    "spectrum_label_ko": "그린",
    "status": "cataloged",
    "summary": "Basil Green is a name-only extended keyword from the REFERENCE X Other Green Keywords list. The source gives no RGB/CMYK/metrics for it; use it as a search and naming anchor.",
    "values_in_source": false
   },
   "space": "concept",
   "type": "ColorKeyword"
  },
  {
   "id": "color-keyword-ext-avocado",
   "properties": {
    "applies_when": {
     "medium": [
      "any"
     ],
     "spectrum": [
      "green",
      "any"
     ]
    },
    "category": "Other Green Keywords",
    "extraction_method": "macOS/Claude page-image reading of the Other Keywords list pages; raw OCR not committed",
    "family": "extended",
    "label": "Avocado",
    "not_a_rule": true,
    "source_page_pdf": 208,
    "source_pages_pdf": [
     208
    ],
    "source_reference_id": "ref-reference-x-vol1-color",
    "spectra": [
     "green"
    ],
    "spectrum": "green",
    "spectrum_label_ko": "그린",
    "status": "cataloged",
    "summary": "Avocado is a name-only extended keyword from the REFERENCE X Other Green Keywords list. The source gives no RGB/CMYK/metrics for it; use it as a search and naming anchor.",
    "values_in_source": false
   },
   "space": "concept",
   "type": "ColorKeyword"
  },
  {
   "id": "color-keyword-ext-asparagus",
   "properties": {
    "applies_when": {
     "medium": [
      "any"
     ],
     "spectrum": [
      "green",
      "any"
     ]
    },
    "category": "Other Green Keywords",
    "extraction_method": "macOS/Claude page-image reading of the Other Keywords list pages; raw OCR not committed",
    "family": "extended",
    "label": "Asparagus",
    "not_a_rule": true,
    "source_page_pdf": 208,
    "source_pages_pdf": [
     208
    ],
    "source_reference_id": "ref-reference-x-vol1-color",
    "spectra": [
     "green"
    ],
    "spectrum": "green",
    "spectrum_label_ko": "그린",
    "status": "cataloged",
    "summary": "Asparagus is a name-only extended keyword from the REFERENCE X Other Green Keywords list. The source gives no RGB/CMYK/metrics for it; use it as a search and naming anchor.",
    "values_in_source": false
   },
   "space": "concept",
   "type": "ColorKeyword"
  },
  {
   "id": "color-keyword-ext-beryl-green",
   "properties": {
    "applies_when": {
     "medium": [
      "any"
     ],
     "spectrum": [
      "green",
      "any"
     ]
    },
    "category": "Other Green Keywords",
    "extraction_method": "macOS/Claude page-image reading of the Other Keywords list pages; raw OCR not committed",
    "family": "extended",
    "label": "Beryl Green",
    "not_a_rule": true,
    "source_page_pdf": 208,
    "source_pages_pdf": [
     208
    ],
    "source_reference_id": "ref-reference-x-vol1-color",
    "spectra": [
     "green"
    ],
    "spectrum": "green",
    "spectrum_label_ko": "그린",
    "status": "cataloged",
    "summary": "Beryl Green is a name-only extended keyword from the REFERENCE X Other Green Keywords list. The source gives no RGB/CMYK/metrics for it; use it as a search and naming anchor.",
    "values_in_source": false
   },
   "space": "concept",
   "type": "ColorKeyword"
  },
  {
   "id": "color-keyword-ext-chartreuse",
   "properties": {
    "applies_when": {
     "medium": [
      "any"
     ],
     "spectrum": [
      "green",
      "any"
     ]
    },
    "category": "Other Green Keywords",
    "extraction_method": "macOS/Claude page-image reading of the Other Keywords list pages; raw OCR not committed",
    "family": "extended",
    "label": "Chartreuse",
    "not_a_rule": true,
    "source_page_pdf": 208,
    "source_pages_pdf": [
     208
    ],
    "source_reference_id": "ref-reference-x-vol1-color",
    "spectra": [
     "green"
    ],
    "spectrum": "green",
    "spectrum_label_ko": "그린",
    "status": "cataloged",
    "summary": "Chartreuse is a name-only extended keyword from the REFERENCE X Other Green Keywords list. The source gives no RGB/CMYK/metrics for it; use it as a search and naming anchor.",
    "values_in_source": false
   },
   "space": "concept",
   "type": "ColorKeyword"
  },
  {
   "id": "color-keyword-ext-cactus",
   "properties": {
    "applies_when": {
     "medium": [
      "any"
     ],
     "spectrum": [
      "green",
      "any"
     ]
    },
    "category": "Other Green Keywords",
    "extraction_method": "macOS/Claude page-image reading of the Other Keywords list pages; raw OCR not committed",
    "family": "extended",
    "label": "Cactus",
    "not_a_rule": true,
    "source_page_pdf": 208,
    "source_pages_pdf": [
     208
    ],
    "source_reference_id": "ref-reference-x-vol1-color",
    "spectra": [
     "green"
    ],
    "spectrum": "green",
    "spectrum_label_ko": "그린",
    "status": "cataloged",
    "summary": "Cactus is a name-only extended keyword from the REFERENCE X Other Green Keywords list. The source gives no RGB/CMYK/metrics for it; use it as a search and naming anchor.",
    "values_in_source": false
   },
   "space": "concept",
   "type": "ColorKeyword"
  },
  {
   "id": "color-keyword-ext-eucalyptus",
   "properties": {
    "applies_when": {
     "medium": [
      "any"
     ],
     "spectrum": [
      "green",
      "any"
     ]
    },
    "category": "Other Green Keywords",
    "extraction_method": "macOS/Claude page-image reading of the Other Keywords list pages; raw OCR not committed",
    "family": "extended",
    "label": "Eucalyptus",
    "not_a_rule": true,
    "source_page_pdf": 208,
    "source_pages_pdf": [
     208
    ],
    "source_reference_id": "ref-reference-x-vol1-color",
    "spectra": [
     "green"
    ],
    "spectrum": "green",
    "spectrum_label_ko": "그린",
    "status": "cataloged",
    "summary": "Eucalyptus is a name-only extended keyword from the REFERENCE X Other Green Keywords list. The source gives no RGB/CMYK/metrics for it; use it as a search and naming anchor.",
    "values_in_source": false
   },
   "space": "concept",
   "type": "ColorKeyword"
  },
  {
   "id": "color-keyword-ext-jade",
   "properties": {
    "applies_when": {
     "medium": [
      "any"
     ],
     "spectrum": [
      "green",
      "any"
     ]
    },
    "category": "Other Green Keywords",
    "extraction_method": "macOS/Claude page-image reading of the Other Keywords list pages; raw OCR not committed",
    "family": "extended",
    "label": "Jade",
    "not_a_rule": true,
    "source_page_pdf": 208,
    "source_pages_pdf": [
     208
    ],
    "source_reference_id": "ref-reference-x-vol1-color",
    "spectra": [
     "green"
    ],
    "spectrum": "green",
    "spectrum_label_ko": "그린",
    "status": "cataloged",
    "summary": "Jade is a name-only extended keyword from the REFERENCE X Other Green Keywords list. The source gives no RGB/CMYK/metrics for it; use it as a search and naming anchor.",
    "values_in_source": false
   },
   "space": "concept",
   "type": "ColorKeyword"
  },
  {
   "id": "color-keyword-ext-juniper",
   "properties": {
    "applies_when": {
     "medium": [
      "any"
     ],
     "spectrum": [
      "green",
      "any"
     ]
    },
    "category": "Other Green Keywords",
    "extraction_method": "macOS/Claude page-image reading of the Other Keywords list pages; raw OCR not committed",
    "family": "extended",
    "label": "Juniper",
    "not_a_rule": true,
    "source_page_pdf": 208,
    "source_pages_pdf": [
     208
    ],
    "source_reference_id": "ref-reference-x-vol1-color",
    "spectra": [
     "green"
    ],
    "spectrum": "green",
    "spectrum_label_ko": "그린",
    "status": "cataloged",
    "summary": "Juniper is a name-only extended keyword from the REFERENCE X Other Green Keywords list. The source gives no RGB/CMYK/metrics for it; use it as a search and naming anchor.",
    "values_in_source": false
   },
   "space": "concept",
   "type": "ColorKeyword"
  },
  {
   "id": "color-keyword-ext-khaki-green",
   "properties": {
    "applies_when": {
     "medium": [
      "any"
     ],
     "spectrum": [
      "green",
      "any"
     ]
    },
    "category": "Other Green Keywords",
    "extraction_method": "macOS/Claude page-image reading of the Other Keywords list pages; raw OCR not committed",
    "family": "extended",
    "label": "Khaki Green",
    "not_a_rule": true,
    "source_page_pdf": 208,
    "source_pages_pdf": [
     208
    ],
    "source_reference_id": "ref-reference-x-vol1-color",
    "spectra": [
     "green"
    ],
    "spectrum": "green",
    "spectrum_label_ko": "그린",
    "status": "cataloged",
    "summary": "Khaki Green is a name-only extended keyword from the REFERENCE X Other Green Keywords list. The source gives no RGB/CMYK/metrics for it; use it as a search and naming anchor.",
    "values_in_source": false
   },
   "space": "concept",
   "type": "ColorKeyword"
  },
  {
   "id": "color-keyword-ext-loden",
   "properties": {
    "applies_when": {
     "medium": [
      "any"
     ],
     "spectrum": [
      "green",
      "any"
     ]
    },
    "category": "Other Green Keywords",
    "extraction_method": "macOS/Claude page-image reading of the Other Keywords list pages; raw OCR not committed",
    "family": "extended",
    "label": "Loden",
    "not_a_rule": true,
    "source_page_pdf": 208,
    "source_pages_pdf": [
     208
    ],
    "source_reference_id": "ref-reference-x-vol1-color",
    "spectra": [
     "green"
    ],
    "spectrum": "green",
    "spectrum_label_ko": "그린",
    "status": "cataloged",
    "summary": "Loden is a name-only extended keyword from the REFERENCE X Other Green Keywords list. The source gives no RGB/CMYK/metrics for it; use it as a search and naming anchor.",
    "values_in_source": false
   },
   "space": "concept",
   "type": "ColorKeyword"
  },
  {
   "id": "color-keyword-ext-malachite",
   "properties": {
    "applies_when": {
     "medium": [
      "any"
     ],
     "spectrum": [
      "green",
      "any"
     ]
    },
    "category": "Other Green Keywords",
    "extraction_method": "macOS/Claude page-image reading of the Other Keywords list pages; raw OCR not committed",
    "family": "extended",
    "label": "Malachite",
    "not_a_rule": true,
    "source_page_pdf": 208,
    "source_pages_pdf": [
     208
    ],
    "source_reference_id": "ref-reference-x-vol1-color",
    "spectra": [
     "green"
    ],
    "spectrum": "green",
    "spectrum_label_ko": "그린",
    "status": "cataloged",
    "summary": "Malachite is a name-only extended keyword from the REFERENCE X Other Green Keywords list. The source gives no RGB/CMYK/metrics for it; use it as a search and naming anchor.",
    "values_in_source": false
   },
   "space": "concept",
   "type": "ColorKeyword"
  },
  {
   "id": "color-keyword-ext-matcha",
   "properties": {
    "applies_when": {
     "medium": [
      "any"
     ],
     "spectrum": [
      "green",
      "any"
     ]
    },
    "category": "Other Green Keywords",
    "extraction_method": "macOS/Claude page-image reading of the Other Keywords list pages; raw OCR not committed",
    "family": "extended",
    "label": "Matcha",
    "not_a_rule": true,
    "source_page_pdf": 208,
    "source_pages_pdf": [
     208
    ],
    "source_reference_id": "ref-reference-x-vol1-color",
    "spectra": [
     "green"
    ],
    "spectrum": "green",
    "spectrum_label_ko": "그린",
    "status": "cataloged",
    "summary": "Matcha is a name-only extended keyword from the REFERENCE X Other Green Keywords list. The source gives no RGB/CMYK/metrics for it; use it as a search and naming anchor.",
    "values_in_source": false
   },
   "space": "concept",
   "type": "ColorKeyword"
  },
  {
   "id": "color-keyword-ext-meadow",
   "properties": {
    "applies_when": {
     "medium": [
      "any"
     ],
     "spectrum": [
      "green",
      "any"
     ]
    },
    "category": "Other Green Keywords",
    "extraction_method": "macOS/Claude page-image reading of the Other Keywords list pages; raw OCR not committed",
    "family": "extended",
    "label": "Meadow",
    "not_a_rule": true,
    "source_page_pdf": 208,
    "source_pages_pdf": [
     208
    ],
    "source_reference_id": "ref-reference-x-vol1-color",
    "spectra": [
     "green"
    ],
    "spectrum": "green",
    "spectrum_label_ko": "그린",
    "status": "cataloged",
    "summary": "Meadow is a name-only extended keyword from the REFERENCE X Other Green Keywords list. The source gives no RGB/CMYK/metrics for it; use it as a search and naming anchor.",
    "values_in_source": false
   },
   "space": "concept",
   "type": "ColorKeyword"
  },
  {
   "id": "color-keyword-ext-moss-gray",
   "properties": {
    "applies_when": {
     "medium": [
      "any"
     ],
     "spectrum": [
      "green",
      "any"
     ]
    },
    "category": "Other Green Keywords",
    "extraction_method": "macOS/Claude page-image reading of the Other Keywords list pages; raw OCR not committed",
    "family": "extended",
    "label": "Moss Gray",
    "not_a_rule": true,
    "source_page_pdf": 208,
    "source_pages_pdf": [
     208
    ],
    "source_reference_id": "ref-reference-x-vol1-color",
    "spectra": [
     "green"
    ],
    "spectrum": "green",
    "spectrum_label_ko": "그린",
    "status": "cataloged",
    "summary": "Moss Gray is a name-only extended keyword from the REFERENCE X Other Green Keywords list. The source gives no RGB/CMYK/metrics for it; use it as a search and naming anchor.",
    "values_in_source": false
   },
   "space": "concept",
   "type": "ColorKeyword"
  },
  {
   "id": "color-keyword-ext-palm-leaf",
   "properties": {
    "applies_when": {
     "medium": [
      "any"
     ],
     "spectrum": [
      "green",
      "any"
     ]
    },
    "category": "Other Green Keywords",
    "extraction_method": "macOS/Claude page-image reading of the Other Keywords list pages; raw OCR not committed",
    "family": "extended",
    "label": "Palm Leaf",
    "not_a_rule": true,
    "source_page_pdf": 208,
    "source_pages_pdf": [
     208
    ],
    "source_reference_id": "ref-reference-x-vol1-color",
    "spectra": [
     "green"
    ],
    "spectrum": "green",
    "spectrum_label_ko": "그린",
    "status": "cataloged",
    "summary": "Palm Leaf is a name-only extended keyword from the REFERENCE X Other Green Keywords list. The source gives no RGB/CMYK/metrics for it; use it as a search and naming anchor.",
    "values_in_source": false
   },
   "space": "concept",
   "type": "ColorKeyword"
  },
  {
   "id": "color-keyword-ext-pea-green",
   "properties": {
    "applies_when": {
     "medium": [
      "any"
     ],
     "spectrum": [
      "green",
      "any"
     ]
    },
    "category": "Other Green Keywords",
    "extraction_method": "macOS/Claude page-image reading of the Other Keywords list pages; raw OCR not committed",
    "family": "extended",
    "label": "Pea Green",
    "not_a_rule": true,
    "source_page_pdf": 208,
    "source_pages_pdf": [
     208
    ],
    "source_reference_id": "ref-reference-x-vol1-color",
    "spectra": [
     "green"
    ],
    "spectrum": "green",
    "spectrum_label_ko": "그린",
    "status": "cataloged",
    "summary": "Pea Green is a name-only extended keyword from the REFERENCE X Other Green Keywords list. The source gives no RGB/CMYK/metrics for it; use it as a search and naming anchor.",
    "values_in_source": false
   },
   "space": "concept",
   "type": "ColorKeyword"
  },
  {
   "id": "color-keyword-ext-peridot",
   "properties": {
    "applies_when": {
     "medium": [
      "any"
     ],
     "spectrum": [
      "green",
      "any"
     ]
    },
    "category": "Other Green Keywords",
    "extraction_method": "macOS/Claude page-image reading of the Other Keywords list pages; raw OCR not committed",
    "family": "extended",
    "label": "Peridot",
    "not_a_rule": true,
    "source_page_pdf": 208,
    "source_pages_pdf": [
     208
    ],
    "source_reference_id": "ref-reference-x-vol1-color",
    "spectra": [
     "green"
    ],
    "spectrum": "green",
    "spectrum_label_ko": "그린",
    "status": "cataloged",
    "summary": "Peridot is a name-only extended keyword from the REFERENCE X Other Green Keywords list. The source gives no RGB/CMYK/metrics for it; use it as a search and naming anchor.",
    "values_in_source": false
   },
   "space": "concept",
   "type": "ColorKeyword"
  },
  {
   "id": "color-keyword-ext-pine",
   "properties": {
    "applies_when": {
     "medium": [
      "any"
     ],
     "spectrum": [
      "green",
      "any"
     ]
    },
    "category": "Other Green Keywords",
    "extraction_method": "macOS/Claude page-image reading of the Other Keywords list pages; raw OCR not committed",
    "family": "extended",
    "label": "Pine",
    "not_a_rule": true,
    "source_page_pdf": 208,
    "source_pages_pdf": [
     208
    ],
    "source_reference_id": "ref-reference-x-vol1-color",
    "spectra": [
     "green"
    ],
    "spectrum": "green",
    "spectrum_label_ko": "그린",
    "status": "cataloged",
    "summary": "Pine is a name-only extended keyword from the REFERENCE X Other Green Keywords list. The source gives no RGB/CMYK/metrics for it; use it as a search and naming anchor.",
    "values_in_source": false
   },
   "space": "concept",
   "type": "ColorKeyword"
  },
  {
   "id": "color-keyword-ext-sage-green",
   "properties": {
    "applies_when": {
     "medium": [
      "any"
     ],
     "spectrum": [
      "green",
      "any"
     ]
    },
    "category": "Other Green Keywords",
    "extraction_method": "macOS/Claude page-image reading of the Other Keywords list pages; raw OCR not committed",
    "family": "extended",
    "label": "Sage Green",
    "not_a_rule": true,
    "source_page_pdf": 208,
    "source_pages_pdf": [
     208
    ],
    "source_reference_id": "ref-reference-x-vol1-color",
    "spectra": [
     "green"
    ],
    "spectrum": "green",
    "spectrum_label_ko": "그린",
    "status": "cataloged",
    "summary": "Sage Green is a name-only extended keyword from the REFERENCE X Other Green Keywords list. The source gives no RGB/CMYK/metrics for it; use it as a search and naming anchor.",
    "values_in_source": false
   },
   "space": "concept",
   "type": "ColorKeyword"
  },
  {
   "id": "color-keyword-ext-seafoam",
   "properties": {
    "applies_when": {
     "medium": [
      "any"
     ],
     "spectrum": [
      "green",
      "any"
     ]
    },
    "category": "Other Green Keywords",
    "extraction_method": "macOS/Claude page-image reading of the Other Keywords list pages; raw OCR not committed",
    "family": "extended",
    "label": "Seafoam",
    "not_a_rule": true,
    "source_page_pdf": 208,
    "source_pages_pdf": [
     208
    ],
    "source_reference_id": "ref-reference-x-vol1-color",
    "spectra": [
     "green"
    ],
    "spectrum": "green",
    "spectrum_label_ko": "그린",
    "status": "cataloged",
    "summary": "Seafoam is a name-only extended keyword from the REFERENCE X Other Green Keywords list. The source gives no RGB/CMYK/metrics for it; use it as a search and naming anchor.",
    "values_in_source": false
   },
   "space": "concept",
   "type": "ColorKeyword"
  },
  {
   "id": "color-keyword-ext-spruce",
   "properties": {
    "applies_when": {
     "medium": [
      "any"
     ],
     "spectrum": [
      "green",
      "any"
     ]
    },
    "category": "Other Green Keywords",
    "extraction_method": "macOS/Claude page-image reading of the Other Keywords list pages; raw OCR not committed",
    "family": "extended",
    "label": "Spruce",
    "not_a_rule": true,
    "source_page_pdf": 208,
    "source_pages_pdf": [
     208
    ],
    "source_reference_id": "ref-reference-x-vol1-color",
    "spectra": [
     "green"
    ],
    "spectrum": "green",
    "spectrum_label_ko": "그린",
    "status": "cataloged",
    "summary": "Spruce is a name-only extended keyword from the REFERENCE X Other Green Keywords list. The source gives no RGB/CMYK/metrics for it; use it as a search and naming anchor.",
    "values_in_source": false
   },
   "space": "concept",
   "type": "ColorKeyword"
  },
  {
   "id": "color-keyword-ext-tea-green",
   "properties": {
    "applies_when": {
     "medium": [
      "any"
     ],
     "spectrum": [
      "green",
      "any"
     ]
    },
    "category": "Other Green Keywords",
    "extraction_method": "macOS/Claude page-image reading of the Other Keywords list pages; raw OCR not committed",
    "family": "extended",
    "label": "Tea Green",
    "not_a_rule": true,
    "source_page_pdf": 208,
    "source_pages_pdf": [
     208
    ],
    "source_reference_id": "ref-reference-x-vol1-color",
    "spectra": [
     "green"
    ],
    "spectrum": "green",
    "spectrum_label_ko": "그린",
    "status": "cataloged",
    "summary": "Tea Green is a name-only extended keyword from the REFERENCE X Other Green Keywords list. The source gives no RGB/CMYK/metrics for it; use it as a search and naming anchor.",
    "values_in_source": false
   },
   "space": "concept",
   "type": "ColorKeyword"
  },
  {
   "id": "color-keyword-ext-verdant",
   "properties": {
    "applies_when": {
     "medium": [
      "any"
     ],
     "spectrum": [
      "green",
      "any"
     ]
    },
    "category": "Other Green Keywords",
    "extraction_method": "macOS/Claude page-image reading of the Other Keywords list pages; raw OCR not committed",
    "family": "extended",
    "label": "Verdant",
    "not_a_rule": true,
    "source_page_pdf": 208,
    "source_pages_pdf": [
     208
    ],
    "source_reference_id": "ref-reference-x-vol1-color",
    "spectra": [
     "green"
    ],
    "spectrum": "green",
    "spectrum_label_ko": "그린",
    "status": "cataloged",
    "summary": "Verdant is a name-only extended keyword from the REFERENCE X Other Green Keywords list. The source gives no RGB/CMYK/metrics for it; use it as a search and naming anchor.",
    "values_in_source": false
   },
   "space": "concept",
   "type": "ColorKeyword"
  },
  {
   "id": "color-keyword-ext-viridian",
   "properties": {
    "applies_when": {
     "medium": [
      "any"
     ],
     "spectrum": [
      "green",
      "any"
     ]
    },
    "category": "Other Green Keywords",
    "extraction_method": "macOS/Claude page-image reading of the Other Keywords list pages; raw OCR not committed",
    "family": "extended",
    "label": "Viridian",
    "not_a_rule": true,
    "source_page_pdf": 208,
    "source_pages_pdf": [
     208
    ],
    "source_reference_id": "ref-reference-x-vol1-color",
    "spectra": [
     "green"
    ],
    "spectrum": "green",
    "spectrum_label_ko": "그린",
    "status": "cataloged",
    "summary": "Viridian is a name-only extended keyword from the REFERENCE X Other Green Keywords list. The source gives no RGB/CMYK/metrics for it; use it as a search and naming anchor.",
    "values_in_source": false
   },
   "space": "concept",
   "type": "ColorKeyword"
  },
  {
   "id": "color-keyword-ext-willow",
   "properties": {
    "applies_when": {
     "medium": [
      "any"
     ],
     "spectrum": [
      "green",
      "any"
     ]
    },
    "category": "Other Green Keywords",
    "extraction_method": "macOS/Claude page-image reading of the Other Keywords list pages; raw OCR not committed",
    "family": "extended",
    "label": "Willow",
    "not_a_rule": true,
    "source_page_pdf": 208,
    "source_pages_pdf": [
     208
    ],
    "source_reference_id": "ref-reference-x-vol1-color",
    "spectra": [
     "green"
    ],
    "spectrum": "green",
    "spectrum_label_ko": "그린",
    "status": "cataloged",
    "summary": "Willow is a name-only extended keyword from the REFERENCE X Other Green Keywords list. The source gives no RGB/CMYK/metrics for it; use it as a search and naming anchor.",
    "values_in_source": false
   },
   "space": "concept",
   "type": "ColorKeyword"
  },
  {
   "id": "color-keyword-ext-wasabi",
   "properties": {
    "applies_when": {
     "medium": [
      "any"
     ],
     "spectrum": [
      "green",
      "any"
     ]
    },
    "category": "Other Green Keywords",
    "extraction_method": "macOS/Claude page-image reading of the Other Keywords list pages; raw OCR not committed",
    "family": "extended",
    "label": "Wasabi",
    "not_a_rule": true,
    "source_page_pdf": 208,
    "source_pages_pdf": [
     208
    ],
    "source_reference_id": "ref-reference-x-vol1-color",
    "spectra": [
     "green"
    ],
    "spectrum": "green",
    "spectrum_label_ko": "그린",
    "status": "cataloged",
    "summary": "Wasabi is a name-only extended keyword from the REFERENCE X Other Green Keywords list. The source gives no RGB/CMYK/metrics for it; use it as a search and naming anchor.",
    "values_in_source": false
   },
   "space": "concept",
   "type": "ColorKeyword"
  },
  {
   "id": "color-keyword-ext-artichoke",
   "properties": {
    "applies_when": {
     "medium": [
      "any"
     ],
     "spectrum": [
      "green",
      "any"
     ]
    },
    "category": "Other Green Keywords",
    "extraction_method": "macOS/Claude page-image reading of the Other Keywords list pages; raw OCR not committed",
    "family": "extended",
    "label": "Artichoke",
    "not_a_rule": true,
    "source_page_pdf": 208,
    "source_pages_pdf": [
     208
    ],
    "source_reference_id": "ref-reference-x-vol1-color",
    "spectra": [
     "green"
    ],
    "spectrum": "green",
    "spectrum_label_ko": "그린",
    "status": "cataloged",
    "summary": "Artichoke is a name-only extended keyword from the REFERENCE X Other Green Keywords list. The source gives no RGB/CMYK/metrics for it; use it as a search and naming anchor.",
    "values_in_source": false
   },
   "space": "concept",
   "type": "ColorKeyword"
  },
  {
   "id": "color-keyword-ext-pistache",
   "properties": {
    "applies_when": {
     "medium": [
      "any"
     ],
     "spectrum": [
      "green",
      "any"
     ]
    },
    "category": "Other Green Keywords",
    "extraction_method": "macOS/Claude page-image reading of the Other Keywords list pages; raw OCR not committed",
    "family": "extended",
    "label": "Pistache",
    "not_a_rule": true,
    "source_page_pdf": 208,
    "source_pages_pdf": [
     208
    ],
    "source_reference_id": "ref-reference-x-vol1-color",
    "spectra": [
     "green"
    ],
    "spectrum": "green",
    "spectrum_label_ko": "그린",
    "status": "cataloged",
    "summary": "Pistache is a name-only extended keyword from the REFERENCE X Other Green Keywords list. The source gives no RGB/CMYK/metrics for it; use it as a search and naming anchor.",
    "values_in_source": false
   },
   "space": "concept",
   "type": "ColorKeyword"
  },
  {
   "id": "color-keyword-ext-pistachio",
   "properties": {
    "applies_when": {
     "medium": [
      "any"
     ],
     "spectrum": [
      "green",
      "any"
     ]
    },
    "category": "Other Green Keywords",
    "extraction_method": "macOS/Claude page-image reading of the Other Keywords list pages; raw OCR not committed",
    "family": "extended",
    "label": "Pistachio",
    "not_a_rule": true,
    "source_page_pdf": 208,
    "source_pages_pdf": [
     208
    ],
    "source_reference_id": "ref-reference-x-vol1-color",
    "spectra": [
     "green"
    ],
    "spectrum": "green",
    "spectrum_label_ko": "그린",
    "status": "cataloged",
    "summary": "Pistachio is a name-only extended keyword from the REFERENCE X Other Green Keywords list. The source gives no RGB/CMYK/metrics for it; use it as a search and naming anchor.",
    "values_in_source": false
   },
   "space": "concept",
   "type": "ColorKeyword"
  },
  {
   "id": "color-keyword-ext-aegean",
   "properties": {
    "applies_when": {
     "medium": [
      "any"
     ],
     "spectrum": [
      "blue",
      "any"
     ]
    },
    "category": "Other Blue Keywords",
    "extraction_method": "macOS/Claude page-image reading of the Other Keywords list pages; raw OCR not committed",
    "family": "extended",
    "label": "Aegean",
    "not_a_rule": true,
    "source_page_pdf": 254,
    "source_pages_pdf": [
     254
    ],
    "source_reference_id": "ref-reference-x-vol1-color",
    "spectra": [
     "blue"
    ],
    "spectrum": "blue",
    "spectrum_label_ko": "블루",
    "status": "cataloged",
    "summary": "Aegean is a name-only extended keyword from the REFERENCE X Other Blue Keywords list. The source gives no RGB/CMYK/metrics for it; use it as a search and naming anchor.",
    "values_in_source": false
   },
   "space": "concept",
   "type": "ColorKeyword"
  },
  {
   "id": "color-keyword-ext-arctic",
   "properties": {
    "applies_when": {
     "medium": [
      "any"
     ],
     "spectrum": [
      "blue",
      "any"
     ]
    },
    "category": "Other Blue Keywords",
    "extraction_method": "macOS/Claude page-image reading of the Other Keywords list pages; raw OCR not committed",
    "family": "extended",
    "label": "Arctic",
    "not_a_rule": true,
    "source_page_pdf": 254,
    "source_pages_pdf": [
     254
    ],
    "source_reference_id": "ref-reference-x-vol1-color",
    "spectra": [
     "blue"
    ],
    "spectrum": "blue",
    "spectrum_label_ko": "블루",
    "status": "cataloged",
    "summary": "Arctic is a name-only extended keyword from the REFERENCE X Other Blue Keywords list. The source gives no RGB/CMYK/metrics for it; use it as a search and naming anchor.",
    "values_in_source": false
   },
   "space": "concept",
   "type": "ColorKeyword"
  },
  {
   "id": "color-keyword-ext-capri",
   "properties": {
    "applies_when": {
     "medium": [
      "any"
     ],
     "spectrum": [
      "blue",
      "any"
     ]
    },
    "category": "Other Blue Keywords",
    "extraction_method": "macOS/Claude page-image reading of the Other Keywords list pages; raw OCR not committed",
    "family": "extended",
    "label": "Capri",
    "not_a_rule": true,
    "source_page_pdf": 254,
    "source_pages_pdf": [
     254
    ],
    "source_reference_id": "ref-reference-x-vol1-color",
    "spectra": [
     "blue"
    ],
    "spectrum": "blue",
    "spectrum_label_ko": "블루",
    "status": "cataloged",
    "summary": "Capri is a name-only extended keyword from the REFERENCE X Other Blue Keywords list. The source gives no RGB/CMYK/metrics for it; use it as a search and naming anchor.",
    "values_in_source": false
   },
   "space": "concept",
   "type": "ColorKeyword"
  },
  {
   "id": "color-keyword-ext-denim",
   "properties": {
    "applies_when": {
     "medium": [
      "any"
     ],
     "spectrum": [
      "blue",
      "any"
     ]
    },
    "category": "Other Blue Keywords",
    "extraction_method": "macOS/Claude page-image reading of the Other Keywords list pages; raw OCR not committed",
    "family": "extended",
    "label": "Denim",
    "not_a_rule": true,
    "source_page_pdf": 254,
    "source_pages_pdf": [
     254
    ],
    "source_reference_id": "ref-reference-x-vol1-color",
    "spectra": [
     "blue"
    ],
    "spectrum": "blue",
    "spectrum_label_ko": "블루",
    "status": "cataloged",
    "summary": "Denim is a name-only extended keyword from the REFERENCE X Other Blue Keywords list. The source gives no RGB/CMYK/metrics for it; use it as a search and naming anchor.",
    "values_in_source": false
   },
   "space": "concept",
   "type": "ColorKeyword"
  },
  {
   "id": "color-keyword-ext-delft",
   "properties": {
    "applies_when": {
     "medium": [
      "any"
     ],
     "spectrum": [
      "blue",
      "any"
     ]
    },
    "category": "Other Blue Keywords",
    "extraction_method": "macOS/Claude page-image reading of the Other Keywords list pages; raw OCR not committed",
    "family": "extended",
    "label": "Delft",
    "not_a_rule": true,
    "source_page_pdf": 254,
    "source_pages_pdf": [
     254
    ],
    "source_reference_id": "ref-reference-x-vol1-color",
    "spectra": [
     "blue"
    ],
    "spectrum": "blue",
    "spectrum_label_ko": "블루",
    "status": "cataloged",
    "summary": "Delft is a name-only extended keyword from the REFERENCE X Other Blue Keywords list. The source gives no RGB/CMYK/metrics for it; use it as a search and naming anchor.",
    "values_in_source": false
   },
   "space": "concept",
   "type": "ColorKeyword"
  },
  {
   "id": "color-keyword-ext-marine",
   "properties": {
    "applies_when": {
     "medium": [
      "any"
     ],
     "spectrum": [
      "blue",
      "any"
     ]
    },
    "category": "Other Blue Keywords",
    "extraction_method": "macOS/Claude page-image reading of the Other Keywords list pages; raw OCR not committed",
    "family": "extended",
    "label": "Marine",
    "not_a_rule": true,
    "source_page_pdf": 254,
    "source_pages_pdf": [
     254
    ],
    "source_reference_id": "ref-reference-x-vol1-color",
    "spectra": [
     "blue"
    ],
    "spectrum": "blue",
    "spectrum_label_ko": "블루",
    "status": "cataloged",
    "summary": "Marine is a name-only extended keyword from the REFERENCE X Other Blue Keywords list. The source gives no RGB/CMYK/metrics for it; use it as a search and naming anchor.",
    "values_in_source": false
   },
   "space": "concept",
   "type": "ColorKeyword"
  },
  {
   "id": "color-keyword-ext-baltic",
   "properties": {
    "applies_when": {
     "medium": [
      "any"
     ],
     "spectrum": [
      "blue",
      "any"
     ]
    },
    "category": "Other Blue Keywords",
    "extraction_method": "macOS/Claude page-image reading of the Other Keywords list pages; raw OCR not committed",
    "family": "extended",
    "label": "Baltic",
    "not_a_rule": true,
    "source_page_pdf": 254,
    "source_pages_pdf": [
     254
    ],
    "source_reference_id": "ref-reference-x-vol1-color",
    "spectra": [
     "blue"
    ],
    "spectrum": "blue",
    "spectrum_label_ko": "블루",
    "status": "cataloged",
    "summary": "Baltic is a name-only extended keyword from the REFERENCE X Other Blue Keywords list. The source gives no RGB/CMYK/metrics for it; use it as a search and naming anchor.",
    "values_in_source": false
   },
   "space": "concept",
   "type": "ColorKeyword"
  },
  {
   "id": "color-keyword-ext-glacier",
   "properties": {
    "applies_when": {
     "medium": [
      "any"
     ],
     "spectrum": [
      "blue",
      "any"
     ]
    },
    "category": "Other Blue Keywords",
    "extraction_method": "macOS/Claude page-image reading of the Other Keywords list pages; raw OCR not committed",
    "family": "extended",
    "label": "Glacier",
    "not_a_rule": true,
    "source_page_pdf": 254,
    "source_pages_pdf": [
     254
    ],
    "source_reference_id": "ref-reference-x-vol1-color",
    "spectra": [
     "blue"
    ],
    "spectrum": "blue",
    "spectrum_label_ko": "블루",
    "status": "cataloged",
    "summary": "Glacier is a name-only extended keyword from the REFERENCE X Other Blue Keywords list. The source gives no RGB/CMYK/metrics for it; use it as a search and naming anchor.",
    "values_in_source": false
   },
   "space": "concept",
   "type": "ColorKeyword"
  },
  {
   "id": "color-keyword-ext-lagoon",
   "properties": {
    "applies_when": {
     "medium": [
      "any"
     ],
     "spectrum": [
      "blue",
      "any"
     ]
    },
    "category": "Other Blue Keywords",
    "extraction_method": "macOS/Claude page-image reading of the Other Keywords list pages; raw OCR not committed",
    "family": "extended",
    "label": "Lagoon",
    "not_a_rule": true,
    "source_page_pdf": 254,
    "source_pages_pdf": [
     254
    ],
    "source_reference_id": "ref-reference-x-vol1-color",
    "spectra": [
     "blue"
    ],
    "spectrum": "blue",
    "spectrum_label_ko": "블루",
    "status": "cataloged",
    "summary": "Lagoon is a name-only extended keyword from the REFERENCE X Other Blue Keywords list. The source gives no RGB/CMYK/metrics for it; use it as a search and naming anchor.",
    "values_in_source": false
   },
   "space": "concept",
   "type": "ColorKeyword"
  },
  {
   "id": "color-keyword-ext-cyan",
   "properties": {
    "applies_when": {
     "medium": [
      "any"
     ],
     "spectrum": [
      "blue",
      "any"
     ]
    },
    "category": "Other Blue Keywords",
    "extraction_method": "macOS/Claude page-image reading of the Other Keywords list pages; raw OCR not committed",
    "family": "extended",
    "label": "Cyan",
    "not_a_rule": true,
    "source_page_pdf": 254,
    "source_pages_pdf": [
     254
    ],
    "source_reference_id": "ref-reference-x-vol1-color",
    "spectra": [
     "blue"
    ],
    "spectrum": "blue",
    "spectrum_label_ko": "블루",
    "status": "cataloged",
    "summary": "Cyan is a name-only extended keyword from the REFERENCE X Other Blue Keywords list. The source gives no RGB/CMYK/metrics for it; use it as a search and naming anchor.",
    "values_in_source": false
   },
   "space": "concept",
   "type": "ColorKeyword"
  },
  {
   "id": "color-keyword-ext-peacock",
   "properties": {
    "applies_when": {
     "medium": [
      "any"
     ],
     "spectrum": [
      "blue",
      "any"
     ]
    },
    "category": "Other Blue Keywords",
    "extraction_method": "macOS/Claude page-image reading of the Other Keywords list pages; raw OCR not committed",
    "family": "extended",
    "label": "Peacock",
    "not_a_rule": true,
    "source_page_pdf": 254,
    "source_pages_pdf": [
     254
    ],
    "source_reference_id": "ref-reference-x-vol1-color",
    "spectra": [
     "blue"
    ],
    "spectrum": "blue",
    "spectrum_label_ko": "블루",
    "status": "cataloged",
    "summary": "Peacock is a name-only extended keyword from the REFERENCE X Other Blue Keywords list. The source gives no RGB/CMYK/metrics for it; use it as a search and naming anchor.",
    "values_in_source": false
   },
   "space": "concept",
   "type": "ColorKeyword"
  },
  {
   "id": "color-keyword-ext-azure-mist",
   "properties": {
    "applies_when": {
     "medium": [
      "any"
     ],
     "spectrum": [
      "blue",
      "any"
     ]
    },
    "category": "Other Blue Keywords",
    "extraction_method": "macOS/Claude page-image reading of the Other Keywords list pages; raw OCR not committed",
    "family": "extended",
    "label": "Azure Mist",
    "not_a_rule": true,
    "source_page_pdf": 254,
    "source_pages_pdf": [
     254
    ],
    "source_reference_id": "ref-reference-x-vol1-color",
    "spectra": [
     "blue"
    ],
    "spectrum": "blue",
    "spectrum_label_ko": "블루",
    "status": "cataloged",
    "summary": "Azure Mist is a name-only extended keyword from the REFERENCE X Other Blue Keywords list. The source gives no RGB/CMYK/metrics for it; use it as a search and naming anchor.",
    "values_in_source": false
   },
   "space": "concept",
   "type": "ColorKeyword"
  },
  {
   "id": "color-keyword-ext-royal",
   "properties": {
    "applies_when": {
     "medium": [
      "any"
     ],
     "spectrum": [
      "blue",
      "any"
     ]
    },
    "category": "Other Blue Keywords",
    "extraction_method": "macOS/Claude page-image reading of the Other Keywords list pages; raw OCR not committed",
    "family": "extended",
    "label": "Royal",
    "not_a_rule": true,
    "source_page_pdf": 254,
    "source_pages_pdf": [
     254
    ],
    "source_reference_id": "ref-reference-x-vol1-color",
    "spectra": [
     "blue"
    ],
    "spectrum": "blue",
    "spectrum_label_ko": "블루",
    "status": "cataloged",
    "summary": "Royal is a name-only extended keyword from the REFERENCE X Other Blue Keywords list. The source gives no RGB/CMYK/metrics for it; use it as a search and naming anchor.",
    "values_in_source": false
   },
   "space": "concept",
   "type": "ColorKeyword"
  },
  {
   "id": "color-keyword-ext-skyfall",
   "properties": {
    "applies_when": {
     "medium": [
      "any"
     ],
     "spectrum": [
      "blue",
      "any"
     ]
    },
    "category": "Other Blue Keywords",
    "extraction_method": "macOS/Claude page-image reading of the Other Keywords list pages; raw OCR not committed",
    "family": "extended",
    "label": "Skyfall",
    "not_a_rule": true,
    "source_page_pdf": 254,
    "source_pages_pdf": [
     254
    ],
    "source_reference_id": "ref-reference-x-vol1-color",
    "spectra": [
     "blue"
    ],
    "spectrum": "blue",
    "spectrum_label_ko": "블루",
    "status": "cataloged",
    "summary": "Skyfall is a name-only extended keyword from the REFERENCE X Other Blue Keywords list. The source gives no RGB/CMYK/metrics for it; use it as a search and naming anchor.",
    "values_in_source": false
   },
   "space": "concept",
   "type": "ColorKeyword"
  },
  {
   "id": "color-keyword-ext-blueprint",
   "properties": {
    "applies_when": {
     "medium": [
      "any"
     ],
     "spectrum": [
      "blue",
      "any"
     ]
    },
    "category": "Other Blue Keywords",
    "extraction_method": "macOS/Claude page-image reading of the Other Keywords list pages; raw OCR not committed",
    "family": "extended",
    "label": "Blueprint",
    "not_a_rule": true,
    "source_page_pdf": 254,
    "source_pages_pdf": [
     254
    ],
    "source_reference_id": "ref-reference-x-vol1-color",
    "spectra": [
     "blue"
    ],
    "spectrum": "blue",
    "spectrum_label_ko": "블루",
    "status": "cataloged",
    "summary": "Blueprint is a name-only extended keyword from the REFERENCE X Other Blue Keywords list. The source gives no RGB/CMYK/metrics for it; use it as a search and naming anchor.",
    "values_in_source": false
   },
   "space": "concept",
   "type": "ColorKeyword"
  },
  {
   "id": "color-keyword-ext-horizon",
   "properties": {
    "applies_when": {
     "medium": [
      "any"
     ],
     "spectrum": [
      "blue",
      "any"
     ]
    },
    "category": "Other Blue Keywords",
    "extraction_method": "macOS/Claude page-image reading of the Other Keywords list pages; raw OCR not committed",
    "family": "extended",
    "label": "Horizon",
    "not_a_rule": true,
    "source_page_pdf": 254,
    "source_pages_pdf": [
     254
    ],
    "source_reference_id": "ref-reference-x-vol1-color",
    "spectra": [
     "blue"
    ],
    "spectrum": "blue",
    "spectrum_label_ko": "블루",
    "status": "cataloged",
    "summary": "Horizon is a name-only extended keyword from the REFERENCE X Other Blue Keywords list. The source gives no RGB/CMYK/metrics for it; use it as a search and naming anchor.",
    "values_in_source": false
   },
   "space": "concept",
   "type": "ColorKeyword"
  },
  {
   "id": "color-keyword-ext-polar",
   "properties": {
    "applies_when": {
     "medium": [
      "any"
     ],
     "spectrum": [
      "blue",
      "any"
     ]
    },
    "category": "Other Blue Keywords",
    "extraction_method": "macOS/Claude page-image reading of the Other Keywords list pages; raw OCR not committed",
    "family": "extended",
    "label": "Polar",
    "not_a_rule": true,
    "source_page_pdf": 254,
    "source_pages_pdf": [
     254
    ],
    "source_reference_id": "ref-reference-x-vol1-color",
    "spectra": [
     "blue"
    ],
    "spectrum": "blue",
    "spectrum_label_ko": "블루",
    "status": "cataloged",
    "summary": "Polar is a name-only extended keyword from the REFERENCE X Other Blue Keywords list. The source gives no RGB/CMYK/metrics for it; use it as a search and naming anchor.",
    "values_in_source": false
   },
   "space": "concept",
   "type": "ColorKeyword"
  },
  {
   "id": "color-keyword-ext-deep-sea",
   "properties": {
    "applies_when": {
     "medium": [
      "any"
     ],
     "spectrum": [
      "blue",
      "any"
     ]
    },
    "category": "Other Blue Keywords",
    "extraction_method": "macOS/Claude page-image reading of the Other Keywords list pages; raw OCR not committed",
    "family": "extended",
    "label": "Deep Sea",
    "not_a_rule": true,
    "source_page_pdf": 254,
    "source_pages_pdf": [
     254
    ],
    "source_reference_id": "ref-reference-x-vol1-color",
    "spectra": [
     "blue"
    ],
    "spectrum": "blue",
    "spectrum_label_ko": "블루",
    "status": "cataloged",
    "summary": "Deep Sea is a name-only extended keyword from the REFERENCE X Other Blue Keywords list. The source gives no RGB/CMYK/metrics for it; use it as a search and naming anchor.",
    "values_in_source": false
   },
   "space": "concept",
   "type": "ColorKeyword"
  },
  {
   "id": "color-keyword-ext-arctic-shadow",
   "properties": {
    "applies_when": {
     "medium": [
      "any"
     ],
     "spectrum": [
      "blue",
      "any"
     ]
    },
    "category": "Other Blue Keywords",
    "extraction_method": "macOS/Claude page-image reading of the Other Keywords list pages; raw OCR not committed",
    "family": "extended",
    "label": "Arctic Shadow",
    "not_a_rule": true,
    "source_page_pdf": 254,
    "source_pages_pdf": [
     254
    ],
    "source_reference_id": "ref-reference-x-vol1-color",
    "spectra": [
     "blue"
    ],
    "spectrum": "blue",
    "spectrum_label_ko": "블루",
    "status": "cataloged",
    "summary": "Arctic Shadow is a name-only extended keyword from the REFERENCE X Other Blue Keywords list. The source gives no RGB/CMYK/metrics for it; use it as a search and naming anchor.",
    "values_in_source": false
   },
   "space": "concept",
   "type": "ColorKeyword"
  },
  {
   "id": "color-keyword-ext-true-blue",
   "properties": {
    "applies_when": {
     "medium": [
      "any"
     ],
     "spectrum": [
      "blue",
      "any"
     ]
    },
    "category": "Other Blue Keywords",
    "extraction_method": "macOS/Claude page-image reading of the Other Keywords list pages; raw OCR not committed",
    "family": "extended",
    "label": "True Blue",
    "not_a_rule": true,
    "source_page_pdf": 254,
    "source_pages_pdf": [
     254
    ],
    "source_reference_id": "ref-reference-x-vol1-color",
    "spectra": [
     "blue"
    ],
    "spectrum": "blue",
    "spectrum_label_ko": "블루",
    "status": "cataloged",
    "summary": "True Blue is a name-only extended keyword from the REFERENCE X Other Blue Keywords list. The source gives no RGB/CMYK/metrics for it; use it as a search and naming anchor.",
    "values_in_source": false
   },
   "space": "concept",
   "type": "ColorKeyword"
  },
  {
   "id": "color-keyword-ext-pacific",
   "properties": {
    "applies_when": {
     "medium": [
      "any"
     ],
     "spectrum": [
      "blue",
      "any"
     ]
    },
    "category": "Other Blue Keywords",
    "extraction_method": "macOS/Claude page-image reading of the Other Keywords list pages; raw OCR not committed",
    "family": "extended",
    "label": "Pacific",
    "not_a_rule": true,
    "source_page_pdf": 254,
    "source_pages_pdf": [
     254
    ],
    "source_reference_id": "ref-reference-x-vol1-color",
    "spectra": [
     "blue"
    ],
    "spectrum": "blue",
    "spectrum_label_ko": "블루",
    "status": "cataloged",
    "summary": "Pacific is a name-only extended keyword from the REFERENCE X Other Blue Keywords list. The source gives no RGB/CMYK/metrics for it; use it as a search and naming anchor.",
    "values_in_source": false
   },
   "space": "concept",
   "type": "ColorKeyword"
  },
  {
   "id": "color-keyword-ext-arctic-dawn",
   "properties": {
    "applies_when": {
     "medium": [
      "any"
     ],
     "spectrum": [
      "blue",
      "any"
     ]
    },
    "category": "Other Blue Keywords",
    "extraction_method": "macOS/Claude page-image reading of the Other Keywords list pages; raw OCR not committed",
    "family": "extended",
    "label": "Arctic Dawn",
    "not_a_rule": true,
    "source_page_pdf": 254,
    "source_pages_pdf": [
     254
    ],
    "source_reference_id": "ref-reference-x-vol1-color",
    "spectra": [
     "blue"
    ],
    "spectrum": "blue",
    "spectrum_label_ko": "블루",
    "status": "cataloged",
    "summary": "Arctic Dawn is a name-only extended keyword from the REFERENCE X Other Blue Keywords list. The source gives no RGB/CMYK/metrics for it; use it as a search and naming anchor.",
    "values_in_source": false
   },
   "space": "concept",
   "type": "ColorKeyword"
  },
  {
   "id": "color-keyword-ext-storm",
   "properties": {
    "applies_when": {
     "medium": [
      "any"
     ],
     "spectrum": [
      "blue",
      "any"
     ]
    },
    "category": "Other Blue Keywords",
    "extraction_method": "macOS/Claude page-image reading of the Other Keywords list pages; raw OCR not committed",
    "family": "extended",
    "label": "Storm",
    "not_a_rule": true,
    "source_page_pdf": 254,
    "source_pages_pdf": [
     254
    ],
    "source_reference_id": "ref-reference-x-vol1-color",
    "spectra": [
     "blue"
    ],
    "spectrum": "blue",
    "spectrum_label_ko": "블루",
    "status": "cataloged",
    "summary": "Storm is a name-only extended keyword from the REFERENCE X Other Blue Keywords list. The source gives no RGB/CMYK/metrics for it; use it as a search and naming anchor.",
    "values_in_source": false
   },
   "space": "concept",
   "type": "ColorKeyword"
  },
  {
   "id": "color-keyword-ext-cobalt-blue",
   "properties": {
    "applies_when": {
     "medium": [
      "any"
     ],
     "spectrum": [
      "blue",
      "any"
     ]
    },
    "category": "Other Blue Keywords",
    "extraction_method": "macOS/Claude page-image reading of the Other Keywords list pages; raw OCR not committed",
    "family": "extended",
    "label": "Cobalt Blue",
    "not_a_rule": true,
    "source_page_pdf": 254,
    "source_pages_pdf": [
     254
    ],
    "source_reference_id": "ref-reference-x-vol1-color",
    "spectra": [
     "blue"
    ],
    "spectrum": "blue",
    "spectrum_label_ko": "블루",
    "status": "cataloged",
    "summary": "Cobalt Blue is a name-only extended keyword from the REFERENCE X Other Blue Keywords list. The source gives no RGB/CMYK/metrics for it; use it as a search and naming anchor.",
    "values_in_source": false
   },
   "space": "concept",
   "type": "ColorKeyword"
  },
  {
   "id": "color-keyword-ext-air-force",
   "properties": {
    "applies_when": {
     "medium": [
      "any"
     ],
     "spectrum": [
      "blue",
      "any"
     ]
    },
    "category": "Other Blue Keywords",
    "extraction_method": "macOS/Claude page-image reading of the Other Keywords list pages; raw OCR not committed",
    "family": "extended",
    "label": "Air Force",
    "not_a_rule": true,
    "source_page_pdf": 254,
    "source_pages_pdf": [
     254
    ],
    "source_reference_id": "ref-reference-x-vol1-color",
    "spectra": [
     "blue"
    ],
    "spectrum": "blue",
    "spectrum_label_ko": "블루",
    "status": "cataloged",
    "summary": "Air Force is a name-only extended keyword from the REFERENCE X Other Blue Keywords list. The source gives no RGB/CMYK/metrics for it; use it as a search and naming anchor.",
    "values_in_source": false
   },
   "space": "concept",
   "type": "ColorKeyword"
  },
  {
   "id": "color-keyword-ext-tidal",
   "properties": {
    "applies_when": {
     "medium": [
      "any"
     ],
     "spectrum": [
      "blue",
      "any"
     ]
    },
    "category": "Other Blue Keywords",
    "extraction_method": "macOS/Claude page-image reading of the Other Keywords list pages; raw OCR not committed",
    "family": "extended",
    "label": "Tidal",
    "not_a_rule": true,
    "source_page_pdf": 254,
    "source_pages_pdf": [
     254
    ],
    "source_reference_id": "ref-reference-x-vol1-color",
    "spectra": [
     "blue"
    ],
    "spectrum": "blue",
    "spectrum_label_ko": "블루",
    "status": "cataloged",
    "summary": "Tidal is a name-only extended keyword from the REFERENCE X Other Blue Keywords list. The source gives no RGB/CMYK/metrics for it; use it as a search and naming anchor.",
    "values_in_source": false
   },
   "space": "concept",
   "type": "ColorKeyword"
  },
  {
   "id": "color-keyword-ext-nordic",
   "properties": {
    "applies_when": {
     "medium": [
      "any"
     ],
     "spectrum": [
      "blue",
      "any"
     ]
    },
    "category": "Other Blue Keywords",
    "extraction_method": "macOS/Claude page-image reading of the Other Keywords list pages; raw OCR not committed",
    "family": "extended",
    "label": "Nordic",
    "not_a_rule": true,
    "source_page_pdf": 254,
    "source_pages_pdf": [
     254
    ],
    "source_reference_id": "ref-reference-x-vol1-color",
    "spectra": [
     "blue"
    ],
    "spectrum": "blue",
    "spectrum_label_ko": "블루",
    "status": "cataloged",
    "summary": "Nordic is a name-only extended keyword from the REFERENCE X Other Blue Keywords list. The source gives no RGB/CMYK/metrics for it; use it as a search and naming anchor.",
    "values_in_source": false
   },
   "space": "concept",
   "type": "ColorKeyword"
  },
  {
   "id": "color-keyword-ext-vapor",
   "properties": {
    "applies_when": {
     "medium": [
      "any"
     ],
     "spectrum": [
      "blue",
      "any"
     ]
    },
    "category": "Other Blue Keywords",
    "extraction_method": "macOS/Claude page-image reading of the Other Keywords list pages; raw OCR not committed",
    "family": "extended",
    "label": "Vapor",
    "not_a_rule": true,
    "source_page_pdf": 254,
    "source_pages_pdf": [
     254
    ],
    "source_reference_id": "ref-reference-x-vol1-color",
    "spectra": [
     "blue"
    ],
    "spectrum": "blue",
    "spectrum_label_ko": "블루",
    "status": "cataloged",
    "summary": "Vapor is a name-only extended keyword from the REFERENCE X Other Blue Keywords list. The source gives no RGB/CMYK/metrics for it; use it as a search and naming anchor.",
    "values_in_source": false
   },
   "space": "concept",
   "type": "ColorKeyword"
  },
  {
   "id": "color-keyword-ext-jetstream",
   "properties": {
    "applies_when": {
     "medium": [
      "any"
     ],
     "spectrum": [
      "blue",
      "any"
     ]
    },
    "category": "Other Blue Keywords",
    "extraction_method": "macOS/Claude page-image reading of the Other Keywords list pages; raw OCR not committed",
    "family": "extended",
    "label": "Jetstream",
    "not_a_rule": true,
    "source_page_pdf": 254,
    "source_pages_pdf": [
     254
    ],
    "source_reference_id": "ref-reference-x-vol1-color",
    "spectra": [
     "blue"
    ],
    "spectrum": "blue",
    "spectrum_label_ko": "블루",
    "status": "cataloged",
    "summary": "Jetstream is a name-only extended keyword from the REFERENCE X Other Blue Keywords list. The source gives no RGB/CMYK/metrics for it; use it as a search and naming anchor.",
    "values_in_source": false
   },
   "space": "concept",
   "type": "ColorKeyword"
  },
  {
   "id": "color-keyword-ext-indigo-blue",
   "properties": {
    "applies_when": {
     "medium": [
      "any"
     ],
     "spectrum": [
      "blue",
      "any"
     ]
    },
    "category": "Other Blue Keywords",
    "extraction_method": "macOS/Claude page-image reading of the Other Keywords list pages; raw OCR not committed",
    "family": "extended",
    "label": "Indigo Blue",
    "not_a_rule": true,
    "source_page_pdf": 254,
    "source_pages_pdf": [
     254
    ],
    "source_reference_id": "ref-reference-x-vol1-color",
    "spectra": [
     "blue"
    ],
    "spectrum": "blue",
    "spectrum_label_ko": "블루",
    "status": "cataloged",
    "summary": "Indigo Blue is a name-only extended keyword from the REFERENCE X Other Blue Keywords list. The source gives no RGB/CMYK/metrics for it; use it as a search and naming anchor.",
    "values_in_source": false
   },
   "space": "concept",
   "type": "ColorKeyword"
  },
  {
   "id": "color-keyword-ext-amethyst",
   "properties": {
    "applies_when": {
     "medium": [
      "any"
     ],
     "spectrum": [
      "violet",
      "any"
     ]
    },
    "category": "Other Violet Keywords",
    "extraction_method": "macOS/Claude page-image reading of the Other Keywords list pages; raw OCR not committed",
    "family": "extended",
    "label": "Amethyst",
    "not_a_rule": true,
    "source_page_pdf": 303,
    "source_pages_pdf": [
     303
    ],
    "source_reference_id": "ref-reference-x-vol1-color",
    "spectra": [
     "violet"
    ],
    "spectrum": "violet",
    "spectrum_label_ko": "바이올렛",
    "status": "cataloged",
    "summary": "Amethyst is a name-only extended keyword from the REFERENCE X Other Violet Keywords list. The source gives no RGB/CMYK/metrics for it; use it as a search and naming anchor.",
    "values_in_source": false
   },
   "space": "concept",
   "type": "ColorKeyword"
  },
  {
   "id": "color-keyword-ext-heliotrope",
   "properties": {
    "applies_when": {
     "medium": [
      "any"
     ],
     "spectrum": [
      "violet",
      "any"
     ]
    },
    "category": "Other Violet Keywords",
    "extraction_method": "macOS/Claude page-image reading of the Other Keywords list pages; raw OCR not committed",
    "family": "extended",
    "label": "Heliotrope",
    "not_a_rule": true,
    "source_page_pdf": 303,
    "source_pages_pdf": [
     303
    ],
    "source_reference_id": "ref-reference-x-vol1-color",
    "spectra": [
     "violet"
    ],
    "spectrum": "violet",
    "spectrum_label_ko": "바이올렛",
    "status": "cataloged",
    "summary": "Heliotrope is a name-only extended keyword from the REFERENCE X Other Violet Keywords list. The source gives no RGB/CMYK/metrics for it; use it as a search and naming anchor.",
    "values_in_source": false
   },
   "space": "concept",
   "type": "ColorKeyword"
  },
  {
   "id": "color-keyword-ext-orchid",
   "properties": {
    "applies_when": {
     "medium": [
      "any"
     ],
     "spectrum": [
      "violet",
      "any"
     ]
    },
    "category": "Other Violet Keywords",
    "extraction_method": "macOS/Claude page-image reading of the Other Keywords list pages; raw OCR not committed",
    "family": "extended",
    "label": "Orchid",
    "not_a_rule": true,
    "source_page_pdf": 303,
    "source_pages_pdf": [
     303
    ],
    "source_reference_id": "ref-reference-x-vol1-color",
    "spectra": [
     "violet"
    ],
    "spectrum": "violet",
    "spectrum_label_ko": "바이올렛",
    "status": "cataloged",
    "summary": "Orchid is a name-only extended keyword from the REFERENCE X Other Violet Keywords list. The source gives no RGB/CMYK/metrics for it; use it as a search and naming anchor.",
    "values_in_source": false
   },
   "space": "concept",
   "type": "ColorKeyword"
  },
  {
   "id": "color-keyword-ext-mulberry",
   "properties": {
    "applies_when": {
     "medium": [
      "any"
     ],
     "spectrum": [
      "violet",
      "any"
     ]
    },
    "category": "Other Violet Keywords",
    "extraction_method": "macOS/Claude page-image reading of the Other Keywords list pages; raw OCR not committed",
    "family": "extended",
    "label": "Mulberry",
    "not_a_rule": true,
    "source_page_pdf": 303,
    "source_pages_pdf": [
     303
    ],
    "source_reference_id": "ref-reference-x-vol1-color",
    "spectra": [
     "violet"
    ],
    "spectrum": "violet",
    "spectrum_label_ko": "바이올렛",
    "status": "cataloged",
    "summary": "Mulberry is a name-only extended keyword from the REFERENCE X Other Violet Keywords list. The source gives no RGB/CMYK/metrics for it; use it as a search and naming anchor.",
    "values_in_source": false
   },
   "space": "concept",
   "type": "ColorKeyword"
  },
  {
   "id": "color-keyword-ext-plum",
   "properties": {
    "applies_when": {
     "medium": [
      "any"
     ],
     "spectrum": [
      "violet",
      "any"
     ]
    },
    "category": "Other Violet Keywords",
    "extraction_method": "macOS/Claude page-image reading of the Other Keywords list pages; raw OCR not committed",
    "family": "extended",
    "label": "Plum",
    "not_a_rule": true,
    "source_page_pdf": 303,
    "source_pages_pdf": [
     303
    ],
    "source_reference_id": "ref-reference-x-vol1-color",
    "spectra": [
     "violet"
    ],
    "spectrum": "violet",
    "spectrum_label_ko": "바이올렛",
    "status": "cataloged",
    "summary": "Plum is a name-only extended keyword from the REFERENCE X Other Violet Keywords list. The source gives no RGB/CMYK/metrics for it; use it as a search and naming anchor.",
    "values_in_source": false
   },
   "space": "concept",
   "type": "ColorKeyword"
  },
  {
   "id": "color-keyword-ext-violet-storm",
   "properties": {
    "applies_when": {
     "medium": [
      "any"
     ],
     "spectrum": [
      "violet",
      "any"
     ]
    },
    "category": "Other Violet Keywords",
    "extraction_method": "macOS/Claude page-image reading of the Other Keywords list pages; raw OCR not committed",
    "family": "extended",
    "label": "Violet Storm",
    "not_a_rule": true,
    "source_page_pdf": 303,
    "source_pages_pdf": [
     303
    ],
    "source_reference_id": "ref-reference-x-vol1-color",
    "spectra": [
     "violet"
    ],
    "spectrum": "violet",
    "spectrum_label_ko": "바이올렛",
    "status": "cataloged",
    "summary": "Violet Storm is a name-only extended keyword from the REFERENCE X Other Violet Keywords list. The source gives no RGB/CMYK/metrics for it; use it as a search and naming anchor.",
    "values_in_source": false
   },
   "space": "concept",
   "type": "ColorKeyword"
  },
  {
   "id": "color-keyword-ext-mystic-violet",
   "properties": {
    "applies_when": {
     "medium": [
      "any"
     ],
     "spectrum": [
      "violet",
      "any"
     ]
    },
    "category": "Other Violet Keywords",
    "extraction_method": "macOS/Claude page-image reading of the Other Keywords list pages; raw OCR not committed",
    "family": "extended",
    "label": "Mystic Violet",
    "not_a_rule": true,
    "source_page_pdf": 303,
    "source_pages_pdf": [
     303
    ],
    "source_reference_id": "ref-reference-x-vol1-color",
    "spectra": [
     "violet"
    ],
    "spectrum": "violet",
    "spectrum_label_ko": "바이올렛",
    "status": "cataloged",
    "summary": "Mystic Violet is a name-only extended keyword from the REFERENCE X Other Violet Keywords list. The source gives no RGB/CMYK/metrics for it; use it as a search and naming anchor.",
    "values_in_source": false
   },
   "space": "concept",
   "type": "ColorKeyword"
  },
  {
   "id": "color-keyword-ext-digital-lavender",
   "properties": {
    "applies_when": {
     "medium": [
      "any"
     ],
     "spectrum": [
      "violet",
      "any"
     ]
    },
    "category": "Other Violet Keywords",
    "extraction_method": "macOS/Claude page-image reading of the Other Keywords list pages; raw OCR not committed",
    "family": "extended",
    "label": "Digital Lavender",
    "not_a_rule": true,
    "source_page_pdf": 303,
    "source_pages_pdf": [
     303
    ],
    "source_reference_id": "ref-reference-x-vol1-color",
    "spectra": [
     "violet"
    ],
    "spectrum": "violet",
    "spectrum_label_ko": "바이올렛",
    "status": "cataloged",
    "summary": "Digital Lavender is a name-only extended keyword from the REFERENCE X Other Violet Keywords list. The source gives no RGB/CMYK/metrics for it; use it as a search and naming anchor.",
    "values_in_source": false
   },
   "space": "concept",
   "type": "ColorKeyword"
  },
  {
   "id": "color-keyword-ext-dusty-lilac",
   "properties": {
    "applies_when": {
     "medium": [
      "any"
     ],
     "spectrum": [
      "violet",
      "any"
     ]
    },
    "category": "Other Violet Keywords",
    "extraction_method": "macOS/Claude page-image reading of the Other Keywords list pages; raw OCR not committed",
    "family": "extended",
    "label": "Dusty Lilac",
    "not_a_rule": true,
    "source_page_pdf": 303,
    "source_pages_pdf": [
     303
    ],
    "source_reference_id": "ref-reference-x-vol1-color",
    "spectra": [
     "violet"
    ],
    "spectrum": "violet",
    "spectrum_label_ko": "바이올렛",
    "status": "cataloged",
    "summary": "Dusty Lilac is a name-only extended keyword from the REFERENCE X Other Violet Keywords list. The source gives no RGB/CMYK/metrics for it; use it as a search and naming anchor.",
    "values_in_source": false
   },
   "space": "concept",
   "type": "ColorKeyword"
  },
  {
   "id": "color-keyword-ext-radiant-orchid",
   "properties": {
    "applies_when": {
     "medium": [
      "any"
     ],
     "spectrum": [
      "violet",
      "any"
     ]
    },
    "category": "Other Violet Keywords",
    "extraction_method": "macOS/Claude page-image reading of the Other Keywords list pages; raw OCR not committed",
    "family": "extended",
    "label": "Radiant Orchid",
    "not_a_rule": true,
    "source_page_pdf": 303,
    "source_pages_pdf": [
     303
    ],
    "source_reference_id": "ref-reference-x-vol1-color",
    "spectra": [
     "violet"
    ],
    "spectrum": "violet",
    "spectrum_label_ko": "바이올렛",
    "status": "cataloged",
    "summary": "Radiant Orchid is a name-only extended keyword from the REFERENCE X Other Violet Keywords list. The source gives no RGB/CMYK/metrics for it; use it as a search and naming anchor.",
    "values_in_source": false
   },
   "space": "concept",
   "type": "ColorKeyword"
  },
  {
   "id": "color-keyword-ext-boysenberry",
   "properties": {
    "applies_when": {
     "medium": [
      "any"
     ],
     "spectrum": [
      "violet",
      "any"
     ]
    },
    "category": "Other Violet Keywords",
    "duplicate_in_source_list": true,
    "extraction_method": "macOS/Claude page-image reading of the Other Keywords list pages; raw OCR not committed",
    "family": "extended",
    "label": "Boysenberry",
    "not_a_rule": true,
    "source_page_pdf": 303,
    "source_pages_pdf": [
     303
    ],
    "source_reference_id": "ref-reference-x-vol1-color",
    "spectra": [
     "violet"
    ],
    "spectrum": "violet",
    "spectrum_label_ko": "바이올렛",
    "status": "cataloged",
    "summary": "Boysenberry is a name-only extended keyword from the REFERENCE X Other Violet Keywords list. The source gives no RGB/CMYK/metrics for it; use it as a search and naming anchor.",
    "values_in_source": false
   },
   "space": "concept",
   "type": "ColorKeyword"
  },
  {
   "id": "color-keyword-ext-tyrian-purple",
   "properties": {
    "applies_when": {
     "medium": [
      "any"
     ],
     "spectrum": [
      "violet",
      "any"
     ]
    },
    "category": "Other Violet Keywords",
    "extraction_method": "macOS/Claude page-image reading of the Other Keywords list pages; raw OCR not committed",
    "family": "extended",
    "label": "Tyrian Purple",
    "not_a_rule": true,
    "source_page_pdf": 303,
    "source_pages_pdf": [
     303
    ],
    "source_reference_id": "ref-reference-x-vol1-color",
    "spectra": [
     "violet"
    ],
    "spectrum": "violet",
    "spectrum_label_ko": "바이올렛",
    "status": "cataloged",
    "summary": "Tyrian Purple is a name-only extended keyword from the REFERENCE X Other Violet Keywords list. The source gives no RGB/CMYK/metrics for it; use it as a search and naming anchor.",
    "values_in_source": false
   },
   "space": "concept",
   "type": "ColorKeyword"
  },
  {
   "id": "color-keyword-ext-wisteria",
   "properties": {
    "applies_when": {
     "medium": [
      "any"
     ],
     "spectrum": [
      "violet",
      "any"
     ]
    },
    "category": "Other Violet Keywords",
    "extraction_method": "macOS/Claude page-image reading of the Other Keywords list pages; raw OCR not committed",
    "family": "extended",
    "label": "Wisteria",
    "not_a_rule": true,
    "source_page_pdf": 303,
    "source_pages_pdf": [
     303
    ],
    "source_reference_id": "ref-reference-x-vol1-color",
    "spectra": [
     "violet"
    ],
    "spectrum": "violet",
    "spectrum_label_ko": "바이올렛",
    "status": "cataloged",
    "summary": "Wisteria is a name-only extended keyword from the REFERENCE X Other Violet Keywords list. The source gives no RGB/CMYK/metrics for it; use it as a search and naming anchor.",
    "values_in_source": false
   },
   "space": "concept",
   "type": "ColorKeyword"
  },
  {
   "id": "color-keyword-ext-lavender-gray",
   "properties": {
    "applies_when": {
     "medium": [
      "any"
     ],
     "spectrum": [
      "violet",
      "any"
     ]
    },
    "category": "Other Violet Keywords",
    "extraction_method": "macOS/Claude page-image reading of the Other Keywords list pages; raw OCR not committed",
    "family": "extended",
    "label": "Lavender Gray",
    "not_a_rule": true,
    "source_page_pdf": 303,
    "source_pages_pdf": [
     303
    ],
    "source_reference_id": "ref-reference-x-vol1-color",
    "spectra": [
     "violet"
    ],
    "spectrum": "violet",
    "spectrum_label_ko": "바이올렛",
    "status": "cataloged",
    "summary": "Lavender Gray is a name-only extended keyword from the REFERENCE X Other Violet Keywords list. The source gives no RGB/CMYK/metrics for it; use it as a search and naming anchor.",
    "values_in_source": false
   },
   "space": "concept",
   "type": "ColorKeyword"
  },
  {
   "id": "color-keyword-ext-french-lilac",
   "properties": {
    "applies_when": {
     "medium": [
      "any"
     ],
     "spectrum": [
      "violet",
      "any"
     ]
    },
    "category": "Other Violet Keywords",
    "extraction_method": "macOS/Claude page-image reading of the Other Keywords list pages; raw OCR not committed",
    "family": "extended",
    "label": "French Lilac",
    "not_a_rule": true,
    "source_page_pdf": 303,
    "source_pages_pdf": [
     303
    ],
    "source_reference_id": "ref-reference-x-vol1-color",
    "spectra": [
     "violet"
    ],
    "spectrum": "violet",
    "spectrum_label_ko": "바이올렛",
    "status": "cataloged",
    "summary": "French Lilac is a name-only extended keyword from the REFERENCE X Other Violet Keywords list. The source gives no RGB/CMYK/metrics for it; use it as a search and naming anchor.",
    "values_in_source": false
   },
   "space": "concept",
   "type": "ColorKeyword"
  },
  {
   "id": "color-keyword-ext-raisin-purple",
   "properties": {
    "applies_when": {
     "medium": [
      "any"
     ],
     "spectrum": [
      "violet",
      "any"
     ]
    },
    "category": "Other Violet Keywords",
    "extraction_method": "macOS/Claude page-image reading of the Other Keywords list pages; raw OCR not committed",
    "family": "extended",
    "label": "Raisin Purple",
    "not_a_rule": true,
    "source_page_pdf": 303,
    "source_pages_pdf": [
     303
    ],
    "source_reference_id": "ref-reference-x-vol1-color",
    "spectra": [
     "violet"
    ],
    "spectrum": "violet",
    "spectrum_label_ko": "바이올렛",
    "status": "cataloged",
    "summary": "Raisin Purple is a name-only extended keyword from the REFERENCE X Other Violet Keywords list. The source gives no RGB/CMYK/metrics for it; use it as a search and naming anchor.",
    "values_in_source": false
   },
   "space": "concept",
   "type": "ColorKeyword"
  },
  {
   "id": "color-keyword-ext-opera-mauve",
   "properties": {
    "applies_when": {
     "medium": [
      "any"
     ],
     "spectrum": [
      "violet",
      "any"
     ]
    },
    "category": "Other Violet Keywords",
    "extraction_method": "macOS/Claude page-image reading of the Other Keywords list pages; raw OCR not committed",
    "family": "extended",
    "label": "Opera Mauve",
    "not_a_rule": true,
    "source_page_pdf": 303,
    "source_pages_pdf": [
     303
    ],
    "source_reference_id": "ref-reference-x-vol1-color",
    "spectra": [
     "violet"
    ],
    "spectrum": "violet",
    "spectrum_label_ko": "바이올렛",
    "status": "cataloged",
    "summary": "Opera Mauve is a name-only extended keyword from the REFERENCE X Other Violet Keywords list. The source gives no RGB/CMYK/metrics for it; use it as a search and naming anchor.",
    "values_in_source": false
   },
   "space": "concept",
   "type": "ColorKeyword"
  },
  {
   "id": "color-keyword-ext-pansy-purple",
   "properties": {
    "applies_when": {
     "medium": [
      "any"
     ],
     "spectrum": [
      "violet",
      "any"
     ]
    },
    "category": "Other Violet Keywords",
    "extraction_method": "macOS/Claude page-image reading of the Other Keywords list pages; raw OCR not committed",
    "family": "extended",
    "label": "Pansy Purple",
    "not_a_rule": true,
    "source_page_pdf": 303,
    "source_pages_pdf": [
     303
    ],
    "source_reference_id": "ref-reference-x-vol1-color",
    "spectra": [
     "violet"
    ],
    "spectrum": "violet",
    "spectrum_label_ko": "바이올렛",
    "status": "cataloged",
    "summary": "Pansy Purple is a name-only extended keyword from the REFERENCE X Other Violet Keywords list. The source gives no RGB/CMYK/metrics for it; use it as a search and naming anchor.",
    "values_in_source": false
   },
   "space": "concept",
   "type": "ColorKeyword"
  },
  {
   "id": "color-keyword-ext-berry-bliss",
   "properties": {
    "applies_when": {
     "medium": [
      "any"
     ],
     "spectrum": [
      "violet",
      "any"
     ]
    },
    "category": "Other Violet Keywords",
    "extraction_method": "macOS/Claude page-image reading of the Other Keywords list pages; raw OCR not committed",
    "family": "extended",
    "label": "Berry Bliss",
    "not_a_rule": true,
    "source_page_pdf": 303,
    "source_pages_pdf": [
     303
    ],
    "source_reference_id": "ref-reference-x-vol1-color",
    "spectra": [
     "violet"
    ],
    "spectrum": "violet",
    "spectrum_label_ko": "바이올렛",
    "status": "cataloged",
    "summary": "Berry Bliss is a name-only extended keyword from the REFERENCE X Other Violet Keywords list. The source gives no RGB/CMYK/metrics for it; use it as a search and naming anchor.",
    "values_in_source": false
   },
   "space": "concept",
   "type": "ColorKeyword"
  },
  {
   "id": "color-keyword-ext-berry-wine",
   "properties": {
    "applies_when": {
     "medium": [
      "any"
     ],
     "spectrum": [
      "violet",
      "any"
     ]
    },
    "category": "Other Violet Keywords",
    "extraction_method": "macOS/Claude page-image reading of the Other Keywords list pages; raw OCR not committed",
    "family": "extended",
    "label": "Berry Wine",
    "not_a_rule": true,
    "source_page_pdf": 303,
    "source_pages_pdf": [
     303
    ],
    "source_reference_id": "ref-reference-x-vol1-color",
    "spectra": [
     "violet"
    ],
    "spectrum": "violet",
    "spectrum_label_ko": "바이올렛",
    "status": "cataloged",
    "summary": "Berry Wine is a name-only extended keyword from the REFERENCE X Other Violet Keywords list. The source gives no RGB/CMYK/metrics for it; use it as a search and naming anchor.",
    "values_in_source": false
   },
   "space": "concept",
   "type": "ColorKeyword"
  },
  {
   "id": "color-keyword-ext-purple-basil",
   "properties": {
    "applies_when": {
     "medium": [
      "any"
     ],
     "spectrum": [
      "violet",
      "any"
     ]
    },
    "category": "Other Violet Keywords",
    "extraction_method": "macOS/Claude page-image reading of the Other Keywords list pages; raw OCR not committed",
    "family": "extended",
    "label": "Purple Basil",
    "not_a_rule": true,
    "source_page_pdf": 303,
    "source_pages_pdf": [
     303
    ],
    "source_reference_id": "ref-reference-x-vol1-color",
    "spectra": [
     "violet"
    ],
    "spectrum": "violet",
    "spectrum_label_ko": "바이올렛",
    "status": "cataloged",
    "summary": "Purple Basil is a name-only extended keyword from the REFERENCE X Other Violet Keywords list. The source gives no RGB/CMYK/metrics for it; use it as a search and naming anchor.",
    "values_in_source": false
   },
   "space": "concept",
   "type": "ColorKeyword"
  },
  {
   "id": "color-keyword-ext-deep-magenta",
   "properties": {
    "applies_when": {
     "medium": [
      "any"
     ],
     "spectrum": [
      "violet",
      "any"
     ]
    },
    "category": "Other Violet Keywords",
    "extraction_method": "macOS/Claude page-image reading of the Other Keywords list pages; raw OCR not committed",
    "family": "extended",
    "label": "Deep Magenta",
    "not_a_rule": true,
    "source_page_pdf": 303,
    "source_pages_pdf": [
     303
    ],
    "source_reference_id": "ref-reference-x-vol1-color",
    "spectra": [
     "violet"
    ],
    "spectrum": "violet",
    "spectrum_label_ko": "바이올렛",
    "status": "cataloged",
    "summary": "Deep Magenta is a name-only extended keyword from the REFERENCE X Other Violet Keywords list. The source gives no RGB/CMYK/metrics for it; use it as a search and naming anchor.",
    "values_in_source": false
   },
   "space": "concept",
   "type": "ColorKeyword"
  },
  {
   "id": "color-keyword-ext-blue-violet",
   "properties": {
    "applies_when": {
     "medium": [
      "any"
     ],
     "spectrum": [
      "violet",
      "any"
     ]
    },
    "category": "Other Violet Keywords",
    "extraction_method": "macOS/Claude page-image reading of the Other Keywords list pages; raw OCR not committed",
    "family": "extended",
    "label": "Blue-Violet",
    "not_a_rule": true,
    "source_page_pdf": 303,
    "source_pages_pdf": [
     303
    ],
    "source_reference_id": "ref-reference-x-vol1-color",
    "spectra": [
     "violet"
    ],
    "spectrum": "violet",
    "spectrum_label_ko": "바이올렛",
    "status": "cataloged",
    "summary": "Blue-Violet is a name-only extended keyword from the REFERENCE X Other Violet Keywords list. The source gives no RGB/CMYK/metrics for it; use it as a search and naming anchor.",
    "values_in_source": false
   },
   "space": "concept",
   "type": "ColorKeyword"
  },
  {
   "id": "color-keyword-ext-fuchsia-purple",
   "properties": {
    "applies_when": {
     "medium": [
      "any"
     ],
     "spectrum": [
      "violet",
      "any"
     ]
    },
    "category": "Other Violet Keywords",
    "extraction_method": "macOS/Claude page-image reading of the Other Keywords list pages; raw OCR not committed",
    "family": "extended",
    "label": "Fuchsia Purple",
    "not_a_rule": true,
    "source_page_pdf": 303,
    "source_pages_pdf": [
     303
    ],
    "source_reference_id": "ref-reference-x-vol1-color",
    "spectra": [
     "violet"
    ],
    "spectrum": "violet",
    "spectrum_label_ko": "바이올렛",
    "status": "cataloged",
    "summary": "Fuchsia Purple is a name-only extended keyword from the REFERENCE X Other Violet Keywords list. The source gives no RGB/CMYK/metrics for it; use it as a search and naming anchor.",
    "values_in_source": false
   },
   "space": "concept",
   "type": "ColorKeyword"
  },
  {
   "id": "color-keyword-ext-grape-juice",
   "properties": {
    "applies_when": {
     "medium": [
      "any"
     ],
     "spectrum": [
      "violet",
      "any"
     ]
    },
    "category": "Other Violet Keywords",
    "extraction_method": "macOS/Claude page-image reading of the Other Keywords list pages; raw OCR not committed",
    "family": "extended",
    "label": "Grape Juice",
    "not_a_rule": true,
    "source_page_pdf": 303,
    "source_pages_pdf": [
     303
    ],
    "source_reference_id": "ref-reference-x-vol1-color",
    "spectra": [
     "violet"
    ],
    "spectrum": "violet",
    "spectrum_label_ko": "바이올렛",
    "status": "cataloged",
    "summary": "Grape Juice is a name-only extended keyword from the REFERENCE X Other Violet Keywords list. The source gives no RGB/CMYK/metrics for it; use it as a search and naming anchor.",
    "values_in_source": false
   },
   "space": "concept",
   "type": "ColorKeyword"
  },
  {
   "id": "color-keyword-ext-wine-berry",
   "properties": {
    "applies_when": {
     "medium": [
      "any"
     ],
     "spectrum": [
      "violet",
      "any"
     ]
    },
    "category": "Other Violet Keywords",
    "extraction_method": "macOS/Claude page-image reading of the Other Keywords list pages; raw OCR not committed",
    "family": "extended",
    "label": "Wine Berry",
    "not_a_rule": true,
    "source_page_pdf": 303,
    "source_pages_pdf": [
     303
    ],
    "source_reference_id": "ref-reference-x-vol1-color",
    "spectra": [
     "violet"
    ],
    "spectrum": "violet",
    "spectrum_label_ko": "바이올렛",
    "status": "cataloged",
    "summary": "Wine Berry is a name-only extended keyword from the REFERENCE X Other Violet Keywords list. The source gives no RGB/CMYK/metrics for it; use it as a search and naming anchor.",
    "values_in_source": false
   },
   "space": "concept",
   "type": "ColorKeyword"
  },
  {
   "id": "color-keyword-ext-berry-bloom",
   "properties": {
    "applies_when": {
     "medium": [
      "any"
     ],
     "spectrum": [
      "violet",
      "any"
     ]
    },
    "category": "Other Violet Keywords",
    "extraction_method": "macOS/Claude page-image reading of the Other Keywords list pages; raw OCR not committed",
    "family": "extended",
    "label": "Berry Bloom",
    "not_a_rule": true,
    "source_page_pdf": 303,
    "source_pages_pdf": [
     303
    ],
    "source_reference_id": "ref-reference-x-vol1-color",
    "spectra": [
     "violet"
    ],
    "spectrum": "violet",
    "spectrum_label_ko": "바이올렛",
    "status": "cataloged",
    "summary": "Berry Bloom is a name-only extended keyword from the REFERENCE X Other Violet Keywords list. The source gives no RGB/CMYK/metrics for it; use it as a search and naming anchor.",
    "values_in_source": false
   },
   "space": "concept",
   "type": "ColorKeyword"
  },
  {
   "id": "color-keyword-ext-purple-haze",
   "properties": {
    "applies_when": {
     "medium": [
      "any"
     ],
     "spectrum": [
      "violet",
      "any"
     ]
    },
    "category": "Other Violet Keywords",
    "extraction_method": "macOS/Claude page-image reading of the Other Keywords list pages; raw OCR not committed",
    "family": "extended",
    "label": "Purple Haze",
    "not_a_rule": true,
    "source_page_pdf": 303,
    "source_pages_pdf": [
     303
    ],
    "source_reference_id": "ref-reference-x-vol1-color",
    "spectra": [
     "violet"
    ],
    "spectrum": "violet",
    "spectrum_label_ko": "바이올렛",
    "status": "cataloged",
    "summary": "Purple Haze is a name-only extended keyword from the REFERENCE X Other Violet Keywords list. The source gives no RGB/CMYK/metrics for it; use it as a search and naming anchor.",
    "values_in_source": false
   },
   "space": "concept",
   "type": "ColorKeyword"
  },
  {
   "id": "color-keyword-ext-heather-violet",
   "properties": {
    "applies_when": {
     "medium": [
      "any"
     ],
     "spectrum": [
      "violet",
      "any"
     ]
    },
    "category": "Other Violet Keywords",
    "extraction_method": "macOS/Claude page-image reading of the Other Keywords list pages; raw OCR not committed",
    "family": "extended",
    "label": "Heather Violet",
    "not_a_rule": true,
    "source_page_pdf": 303,
    "source_pages_pdf": [
     303
    ],
    "source_reference_id": "ref-reference-x-vol1-color",
    "spectra": [
     "violet"
    ],
    "spectrum": "violet",
    "spectrum_label_ko": "바이올렛",
    "status": "cataloged",
    "summary": "Heather Violet is a name-only extended keyword from the REFERENCE X Other Violet Keywords list. The source gives no RGB/CMYK/metrics for it; use it as a search and naming anchor.",
    "values_in_source": false
   },
   "space": "concept",
   "type": "ColorKeyword"
  },
  {
   "id": "color-keyword-ext-twilight-lavender",
   "properties": {
    "applies_when": {
     "medium": [
      "any"
     ],
     "spectrum": [
      "violet",
      "any"
     ]
    },
    "category": "Other Violet Keywords",
    "extraction_method": "macOS/Claude page-image reading of the Other Keywords list pages; raw OCR not committed",
    "family": "extended",
    "label": "Twilight Lavender",
    "not_a_rule": true,
    "source_page_pdf": 303,
    "source_pages_pdf": [
     303
    ],
    "source_reference_id": "ref-reference-x-vol1-color",
    "spectra": [
     "violet"
    ],
    "spectrum": "violet",
    "spectrum_label_ko": "바이올렛",
    "status": "cataloged",
    "summary": "Twilight Lavender is a name-only extended keyword from the REFERENCE X Other Violet Keywords list. The source gives no RGB/CMYK/metrics for it; use it as a search and naming anchor.",
    "values_in_source": false
   },
   "space": "concept",
   "type": "ColorKeyword"
  },
  {
   "id": "topic-color-palette-abstraction-policy",
   "properties": {
    "core_question": "유료 레퍼런스의 조합/응용 데이터를 원문 재구성 없이 어떤 수준까지 카드와 edge로 만들 수 있는가.",
    "label": "Palette Abstraction Policy — 배색/조합 데이터를 안전하게 추상화하는 기준",
    "not_a_rule": true,
    "status": "cataloged"
   },
   "space": "concept",
   "type": "ColorTopic"
  },
  {
   "id": "guideline-no-palette-table-reconstruction",
   "properties": {
    "example_source": "ref-reference-x-vol1-color",
    "label": "배색표를 재구성할 수 있는 수준의 pair 목록은 만들지 않는다",
    "not_a_rule": true,
    "prompt_avoid": [
     "paid source의 조합표 전체를 edge 목록으로 옮기기",
     "특정 page의 palette row를 같은 순서/구조로 재생성하기",
     "사용자가 원문 없이도 조합표를 복원할 수 있는 덤프 만들기"
    ],
    "prompt_do": [
     "조합을 개별 source row가 아니라 역할, 대비, 무드, 매체 조건으로 요약한다",
     "source page provenance는 유지하되 원본 순서와 테이블 구조는 재현하지 않는다",
     "공개 산출물에는 후보 조합의 이유와 caveat를 자체 문장으로 설명한다"
    ],
    "source_observation": "REFERENCE X는 색상 키워드와 응용 맥락을 제공하지만, 온톨로지는 원문 표나 페이지를 복원 가능한 데이터베이스로 만들지 않는다.",
    "status": "cataloged",
    "summary": "paid source의 조합표, 페이지 배열, 순서, 행/열 구조를 그대로 되살릴 수 있는 palette_pair edge 묶음은 온톨로지에 넣지 않는다.",
    "topic": "topic-color-palette-abstraction-policy"
   },
   "space": "concept",
   "type": "ColorGuideline"
  },
  {
   "id": "pattern-palette-by-role-and-contrast-not-table-row",
   "properties": {
    "example_source": "ref-reference-x-vol1-color",
    "label": "팔레트는 table row가 아니라 역할과 대비 관계로 추상화한다",
    "not_a_rule": true,
    "source_observation": "색상 키워드의 사용법은 source table을 복사하는 대신 tone archive와 application metrics를 통해 응용 가능한 관계로 바꿔야 한다.",
    "status": "cataloged",
    "structure_steps": [
     "anchor keyword의 spectrum, family, mood tags를 확인한다",
     "두 번째 색은 source row가 아니라 contrast role로 정의한다",
     "관계는 anchor/accent/background/support/neutral처럼 기능명으로 기록한다",
     "조합 이유는 mood continuity, value contrast, temperature balance, material fit 중 하나 이상으로 설명한다",
     "원본 page 순서나 표 구조를 보존하지 않는다"
    ],
    "success_signals": [
     "원본 PDF 없이도 좋은 디자인 판단은 가능하지만 원본 표는 복원되지 않는다",
     "같은 정책을 다른 색상/매체에 전이할 수 있다",
     "edge가 색상 이름 나열보다 사용 이유를 더 많이 담는다"
    ],
    "summary": "안전한 팔레트 지식은 \"이 색과 저 색이 한 행에 있었다\"가 아니라 anchor/accent/background, warm/cool, high/low value, saturation contrast 같은 사용 역할로 표현한다.",
    "topic": "topic-color-palette-abstraction-policy"
   },
   "space": "concept",
   "type": "ColorPattern"
  },
  {
   "id": "guideline-palette-pair-edges-require-transformative-brief",
   "properties": {
    "example_source": "ref-reference-x-vol1-color",
    "label": "palette_pair edge는 변형된 brief와 함께만 추가한다",
    "not_a_rule": true,
    "prompt_avoid": [
     "출처 조합을 이유 없이 adopted pair로 승격하기",
     "모든 keyword에 대해 기계적으로 pair edge 만들기",
     "CMYK/RGB proof 없이 인쇄 재현까지 보증하기"
    ],
    "prompt_do": [
     "pair edge마다 output medium, color roles, contrast reason, caveat를 함께 기록한다",
     "색상 조합을 \"추천\"보다 \"brief-specific candidate\"로 표시한다",
     "같은 pair가 다른 맥락에서 다르게 작동할 수 있음을 남긴다"
    ],
    "source_observation": "조합 관계를 온톨로지에 넣을 때는 source fact를 단순 복사하지 않고, 사용 목적과 매체 조건을 결합한 판단 카드로 변환해야 한다.",
    "status": "cataloged",
    "summary": "두 색의 직접 pair edge는 브랜드/화면/인쇄/제품 같은 새로운 산출 맥락에서 역할, 대비, 위험, proof 조건이 함께 설명될 때만 추가한다.",
    "topic": "topic-color-palette-abstraction-policy"
   },
   "space": "concept",
   "type": "ColorGuideline"
  },
  {
   "id": "heuristic-palette-abstraction-review-gate",
   "properties": {
    "example_source": "ref-reference-x-vol1-color",
    "label": "팔레트 edge 추가 전 복원 가능성 검사를 먼저 한다",
    "not_a_rule": true,
    "prompt_avoid": [
     "coverage 목표 때문에 조합표를 대량 edge화하기",
     "source-protection review 없이 자동 추출을 돌리기"
    ],
    "source_observation": "source-backed color domain은 구조화 추상화가 목적이며, paid source의 대체 데이터셋이 되는 순간 정책 위반이다.",
    "status": "cataloged",
    "structure_steps": [
     "edge 묶음이 원본 table의 coverage를 얼마나 복원하는지 확인한다",
     "순서, grouping, exact pair 목록이 원본과 너무 가까우면 중단한다",
     "role/contrast/brief 기반으로 충분히 변형됐는지 확인한다",
     "필요한 경우 문서에는 정책 결정만 남기고 pair edge 추가를 보류한다"
    ],
    "summary": "새 palette/combination edge 묶음은 \"이 데이터를 모으면 원본 표나 페이지 배열을 상당 부분 재구성할 수 있는가\"를 먼저 확인한 뒤 추가한다.",
    "topic": "topic-color-palette-abstraction-policy"
   },
   "space": "concept",
   "type": "ColorHeuristic"
  },
  {
   "id": "pattern-safe-palette-output-contract",
   "properties": {
    "example_source": "ref-reference-x-vol1-color",
    "label": "안전한 팔레트 답변은 후보, 이유, caveat, proof 조건을 함께 낸다",
    "not_a_rule": true,
    "source_observation": "color Ask는 source-backed anchor를 쓰되, paid source의 row/table을 답변으로 재현하지 않는 출력 계약을 가져야 한다.",
    "status": "cataloged",
    "structure_steps": [
     "anchor keyword와 mood target을 먼저 확인한다",
     "palette candidate는 2-4개 역할로 제한한다",
     "각 색의 role과 contrast reason을 자체 문장으로 설명한다",
     "RGB/CMYK caveat와 proof 필요 여부를 붙인다",
     "source table 또는 page image를 복제하지 않는다고 명시한다"
    ],
    "success_signals": [
     "답변이 디자인 판단으로 유용하다",
     "원본 palette table을 대체하거나 복원하지 않는다",
     "매체별 위험과 proof 조건이 같이 보인다"
    ],
    "summary": "팔레트 질문에는 원본 조합표를 열거하지 않고, 후보 색상 역할과 사용 이유, 매체별 caveat, 추가 proof 조건을 함께 제시한다.",
    "topic": "topic-color-palette-abstraction-policy"
   },
   "space": "concept",
   "type": "ColorPattern"
  },
  {
   "id": "guideline-palette-not-three-color-pick",
   "properties": {
    "label": "팔레트 적용은 대표 3색 선택으로 끝내지 않는다",
    "not_a_rule": true,
    "prompt_avoid": [
     "primary/secondary/accent 3색만 정하고 나머지 UI role을 임의로 채우기",
     "대비가 낮은 조합을 body text나 작은 버튼 라벨에 쓰기",
     "paid source 조합표 전체를 pair edge로 복제하기"
    ],
    "prompt_do": [
     "선택된 palette_roles 전체를 대상으로 role x role 조합표를 만든다",
     "각 조합마다 사용 위치, 대비 등급, 금지 위치를 기록한다",
     "text-capable 조합과 decorative-only 조합을 구분한다",
     "component/state token에 조합을 내려보내 실제 화면에서 쓰이게 한다"
    ],
    "source_observation": "사용자 피드백 2026-06-15 — 색상 조합은 컬러 3개만 선택하는 것이 아니라 모든 적용 조합을 만들어야 한다.",
    "status": "cataloged",
    "summary": "UI나 웹 산출물에서 색상은 primary/secondary/accent 3개만 고르고 끝나는 것이 아니라, 선택된 모든 palette role이 서로 만나는 조합까지 설계해야 한다. 배경, 표면, 텍스트, 보더, CTA, focus, error/success, 데이터 표시가 어떤 색 조합을 쓰는지 role matrix로 정리한다.",
    "topic": "topic-color-palette-abstraction-policy"
   },
   "space": "concept",
   "type": "ColorGuideline"
  },
  {
   "id": "pattern-palette-role-combination-matrix",
   "properties": {
    "caveat": [
     "이 matrix는 선택된 brief palette 내부 조합을 설계하는 계약이며, paid source의 모든 원본 palette combination을 복원하는 데이터셋이 아니다."
    ],
    "label": "Palette role-combination matrix",
    "not_a_rule": true,
    "status": "cataloged",
    "structure_steps": [
     "palette_roles를 role, name, hex, behavior로 파싱한다",
     "모든 unordered role pair를 생성한다",
     "상대 luminance/contrast ratio를 계산해 text-capable, large-ui-only, decorative-only로 분류한다",
     "각 pair에 recommended_use, avoid_use, component/state targets를 붙인다",
     "matrix를 generation_brief.json과 design-system capsule에 저장한다"
    ],
    "success_signals": [
     "n개 role이면 n*(n-1)/2개 조합이 빠짐없이 존재한다",
     "낮은 대비 조합도 사라지지 않고 decorative/border/background 전용으로 제한된다",
     "component token이 hard-coded hex가 아니라 matrix의 role pair를 참조한다"
    ],
    "summary": "선택된 팔레트의 모든 role pair를 만들고, 각 조합을 text-capable, large-ui-only, decorative-only 같은 적용 등급으로 분류한다. 이 matrix는 원본 조합표 복제가 아니라 산출물 내부의 색상 적용 계약이다.",
    "topic": "topic-color-palette-abstraction-policy"
   },
   "space": "concept",
   "type": "ColorPattern"
  },
  {
   "id": "pattern-palette-combination-to-component-token-grid",
   "properties": {
    "label": "Palette combinations become component token grid",
    "not_a_rule": true,
    "status": "cataloged",
    "structure_steps": [
     "text-capable pair는 foreground/background token 후보로 배정한다",
     "large-ui-only pair는 큰 버튼, 배지, 그래픽 라벨, 아이콘 표면에만 쓴다",
     "decorative-only pair는 인접 표면, 보더, shadow tint, chart fill, section rhythm으로 제한한다",
     "focus/error/success/selected/disabled 같은 상태별 조합을 명시한다",
     "구현 검증에서 실제 CSS 변수와 component state가 matrix pair를 참조하는지 확인한다"
    ],
    "success_signals": [
     "컴포넌트 상태색이 임의 HEX가 아니라 palette role pair에서 온다",
     "화면 전반의 조합이 한두 accent에 몰리지 않는다",
     "대비 실패 조합이 사용 금지 위치에 명시된다"
    ],
    "summary": "role-combination matrix의 조합을 background/surface/text/border/accent/focus/status/data 같은 UI token grid로 내려보내 Button, Card, Input, Table, Toast, Skeleton 등 component state에 실제 적용한다.",
    "topic": "topic-color-palette-abstraction-policy"
   },
   "space": "concept",
   "type": "ColorPattern"
  },
  {
   "id": "pattern-sample-board-separates-anchor-and-usage",
   "properties": {
    "example_source": "ref-reference-x-vol1-color",
    "label": "샘플 보드는 anchor color와 usage image를 분리한다",
    "not_a_rule": true,
    "source_observation": "사용자 제공 샘플 전체에서 swatch와 RGB/CMYK는 기준 정보이고, 하단 이미지들은 그 색의 사용 방식과 톤 범위를 보여주는 별도 층으로 반복된다.",
    "status": "cataloged",
    "structure_steps": [
     "anchor swatch와 reference values를 먼저 확인한다",
     "이미지 생성/검색에는 anchor를 그대로 크게 칠하지 않는다",
     "여러 이미지 예시를 통해 light, shadow, texture, composition, material, distance를 분리해 읽는다",
     "최종 산출에서는 색상값보다 usage layer가 더 중요하게 작동한다"
    ],
    "summary": "REFERENCE X식 샘플은 색상칩/수치값을 기준점으로 두고, 별도의 이미지 묶음으로 그 색이 실제 시각 환경에서 어떻게 변주되는지 보여준다.",
    "topic": "topic-color-tone-archive"
   },
   "space": "concept",
   "type": "ColorPattern"
  },
  {
   "id": "guideline-do-not-bind-color-to-fixed-subject",
   "properties": {
    "example_source": "ref-reference-x-vol1-color",
    "label": "색상 키워드를 특정 피사체에 고정하지 않는다",
    "not_a_rule": true,
    "prompt_avoid": [
     "violet means flower 같은 고정 연결 만들기",
     "blue means water 같은 고정 연결 만들기",
     "샘플 이미지의 피사체를 정답처럼 반복하기"
    ],
    "prompt_do": [
     "subject category보다 tone behavior를 먼저 적는다",
     "같은 색상 키워드를 여러 피사체와 매체에 적용 가능하게 유지한다",
     "light, shadow, texture, surface, atmosphere, scale 같은 사용 축을 분리한다"
    ],
    "source_observation": "사용자 피드백에 따라 샘플 이미지는 피사체 mapping이 아니라 color usage grammar로 해석한다.",
    "status": "cataloged",
    "summary": "샘플에 꽃, 물, 금속, 공간, 패턴 같은 이미지가 보이더라도 그것은 해당 색의 고정 대상이 아니다. 중요한 것은 색이 빛, 질감, 명도차, 거리감, 장면 분위기로 번역되는 방식이다.",
    "topic": "topic-color-tone-archive"
   },
   "space": "concept",
   "type": "ColorGuideline"
  },
  {
   "id": "pattern-tone-archive-preserves-transferability",
   "properties": {
    "example_source": "ref-reference-x-vol1-color",
    "label": "톤 아카이브는 피사체를 바꿔도 색 사용법이 유지되게 한다",
    "not_a_rule": true,
    "reference_image_roles": [
     "light_behavior",
     "shadow_behavior",
     "texture_density",
     "material_surface",
     "atmospheric_depth",
     "scale_and_crop"
    ],
    "source_observation": "남은 샘플은 여러 spectrum에서 같은 문법이 반복된다는 점을 보여준다. 색상별 정답 피사체보다 전이 가능한 사용 축이 중요하다.",
    "status": "cataloged",
    "success_signals": [
     "같은 색상 키워드가 서로 다른 피사체에서도 같은 톤 논리를 유지한다",
     "샘플 피사체를 바꿔도 색의 감정과 질감 방향이 유지된다",
     "anchor color가 작은 기준점으로 남고 이미지 전체는 관련 톤장으로 읽힌다"
    ],
    "summary": "좋은 색상 온톨로지는 특정 사진 피사체를 따라가지 않고, 그 색의 명도 범위, 채도 운용, 질감 밀도, 광원 성격, 배경 대비를 다른 장면에도 옮길 수 있게 만든다.",
    "topic": "topic-color-tone-archive"
   },
   "space": "concept",
   "type": "ColorPattern"
  },
  {
   "id": "guideline-sample-images-validate-method-not-content",
   "properties": {
    "example_source": "ref-reference-x-vol1-color",
    "label": "샘플 이미지는 내용이 아니라 방법을 검증한다",
    "not_a_rule": true,
    "prompt_avoid": [
     "샘플 피사체를 색상별 규칙으로 승격하기",
     "원본 이미지 구도와 소재를 반복하기"
    ],
    "prompt_do": [
     "swatch-to-image translation method를 유지한다",
     "subject matter는 brief/context에 따라 바꿀 수 있게 둔다",
     "color usage를 tonal ramp, texture, light, contrast, material로 설명한다"
    ],
    "source_observation": "사용자 제공 추가 샘플은 색상별 이미지 피사체가 아니라 샘플 보드의 사용 방식 이해를 위해 제공됐다.",
    "status": "cataloged",
    "summary": "샘플 이미지의 내용물을 온톨로지 규칙으로 만들지 않는다. 검증해야 할 것은 색상칩에서 이미지 톤으로 확장하는 절차, 즉 기준값과 사용 이미지 사이의 관계다.",
    "topic": "topic-color-tone-archive"
   },
   "space": "concept",
   "type": "ColorGuideline"
  },
  {
   "id": "heuristic-samples-validate-usage-grammar-not-every-keyword",
   "properties": {
    "example_source": "ref-reference-x-vol1-color",
    "label": "샘플은 사용 문법을 검증하지만 모든 키워드의 최종 색 검증은 아니다",
    "not_a_rule": true,
    "prompt_avoid": [
     "샘플 일부만 보고 모든 keyword의 이미지 톤을 proof 완료로 선언하기"
    ],
    "prompt_do": [
     "구조 설계에는 현재 샘플을 충분한 근거로 사용한다",
     "production-facing 색 검증에는 keyword별 page/sample spot-check를 별도 단계로 둔다"
    ],
    "source_observation": "사용자 제공 샘플은 여러 spectrum에서 같은 구조를 반복하지만, 모든 84개 keyword의 개별 이미지 예시를 전수 검증한 것은 아니다.",
    "status": "cataloged",
    "summary": "warm/cool/violet 샘플 묶음은 REFERENCE X의 사용 방식, 즉 swatch에서 tone archive로 확장하는 문법을 충분히 보여준다. 다만 각 ColorKeyword의 개별 톤 정확도는 필요 시 spectrum/family별 spot-check로 분리한다.",
    "topic": "topic-color-tone-archive"
   },
   "space": "concept",
   "type": "ColorHeuristic"
  },
  {
   "id": "topic-color-tone-archive",
   "properties": {
    "core_question": "색상 키워드를 단색 면이 아니라 빛, 질감, 그림자, 인접색, 장면 분위기로 어떻게 확장하는가.",
    "label": "Tone Archive — 색상 키워드를 이미지 톤으로 번역하는 방식",
    "not_a_rule": true,
    "status": "cataloged"
   },
   "space": "concept",
   "type": "ColorTopic"
  },
  {
   "id": "heuristic-keyword-image-use-over-hex-fill",
   "properties": {
    "example_source": "ref-reference-x-vol1-color",
    "label": "색상 키워드는 HEX 채움보다 이미지 사용법을 먼저 지시한다",
    "not_a_rule": true,
    "prompt_avoid": [
     "화면 전체를 anchor HEX 한 색으로 채우기",
     "원본 레퍼런스 페이지나 이미지 구도 복제",
     "HEX와 CMYK를 재현 보증값처럼 쓰기"
    ],
    "prompt_do": [
     "anchor HEX를 작은 기준점으로 쓰고 이미지 대부분은 관련 톤 범위로 구성한다",
     "highlights, shadows, haze, material texture, adjacent neutrals를 함께 지정한다",
     "같은 spectrum/family 안에서 자연스럽게 이동하는 색 변주를 허용한다"
    ],
    "source_observation": "사용자 제공 샘플 페이지에서 각 키워드는 swatch 아래 여러 이미지 예시로 톤 범위를 보여준다.",
    "status": "cataloged",
    "summary": "색상값은 기준 좌표이고, 실제 레퍼런스 이미지는 그 좌표가 만드는 톤 범위, 빛의 방향, 재질, 장면 맥락을 보여준다.",
    "topic": "topic-color-tone-archive"
   },
   "space": "concept",
   "type": "ColorHeuristic"
  },
  {
   "id": "guideline-anchor-color-is-not-flat-fill",
   "properties": {
    "example_source": "ref-reference-x-vol1-color",
    "label": "anchor color는 단색 채움이 아니라 톤 중심점이다",
    "not_a_rule": true,
    "source_observation": "제공 샘플은 키워드별 대표색과 함께 자연/재질/공간 이미지를 병치해 anchor 주변의 톤장을 설명한다.",
    "status": "cataloged",
    "success_signals": [
     "anchor color가 눈에 보이지만 이미지가 평면 swatch처럼 보이지 않는다",
     "하이라이트와 그림자가 anchor color의 성격을 유지한다",
     "같은 키워드로 서로 다른 장면/재질 이미지를 설명할 수 있다"
    ],
    "summary": "Copper나 Burnt Orange 같은 키워드는 하나의 면색이 아니라 어두운 그림자, 따뜻한 하이라이트, 먼지 낀 중간톤, 재질 반사를 묶는 중심점으로 써야 한다.",
    "tone_range": [
     "anchor_hex",
     "lower_value_shadow",
     "warmer_highlight",
     "muted_mid_tone",
     "adjacent_neutral"
    ],
    "topic": "topic-color-tone-archive"
   },
   "space": "concept",
   "type": "ColorGuideline"
  },
  {
   "id": "guideline-reference-images-are-tonal-evidence-not-assets",
   "properties": {
    "example_source": "ref-reference-x-vol1-color",
    "label": "레퍼런스 이미지는 복제 대상이 아니라 톤 증거다",
    "not_a_rule": true,
    "prompt_avoid": [
     "원본 이미지의 피사체, 구도, 페이지 배열을 재현하기",
     "레퍼런스를 저작권 있는 asset처럼 저장하기"
    ],
    "prompt_do": [
     "reference image role을 자연 풍경, 재질 클로즈업, 오브젝트/패션, 공간/인테리어처럼 분리한다",
     "역할별로 빛, 표면, 거리감, 대비를 언어화한다"
    ],
    "source_observation": "사용자 제공 샘플은 키워드별로 여러 이미지 예시를 배치하지만, 온톨로지는 이미지 자체가 아니라 역할과 읽는 법만 저장한다.",
    "status": "cataloged",
    "summary": "자료 속 이미지는 그대로 따라 그릴 대상이 아니라, 색상 키워드가 어떤 빛, 재질, 공간, 감정 범위로 작동하는지 보여주는 증거로 읽는다.",
    "topic": "topic-color-tone-archive"
   },
   "space": "concept",
   "type": "ColorGuideline"
  },
  {
   "id": "pattern-color-keyword-to-tone-archive",
   "properties": {
    "example_source": "ref-reference-x-vol1-color",
    "label": "색상 키워드 → 톤 아카이브로 확장한다",
    "not_a_rule": true,
    "source_observation": "제공 샘플의 반복 구조는 swatch와 수치값 아래에 여러 이미지 예시를 두어 키워드의 톤 범위를 설명한다.",
    "status": "cataloged",
    "structure_steps": [
     "ColorKeyword의 spectrum/family/category를 확인한다",
     "anchor HEX와 CMYK를 기준 좌표로만 둔다",
     "tone_axes에서 명도/채도/온도/earth_or_wine_bias 같은 확장 방향을 읽는다",
     "mood_tags를 장면/재질/빛 언어로 번역한다",
     "3-5개의 reference image role을 만든다",
     "최종 prompt에는 anchor color보다 tone atmosphere를 더 크게 쓴다"
    ],
    "summary": "ColorKeyword를 찾은 뒤 swatch/RGB/CMYK에서 멈추지 않고, tone axes와 mood tags를 이용해 톤 램프, 광원, 그림자, 재질, 장면 역할을 생성한다.",
    "topic": "topic-color-tone-archive"
   },
   "space": "concept",
   "type": "ColorPattern"
  },
  {
   "id": "pattern-tone-archive-reference-image-roles",
   "properties": {
    "example_source": "ref-reference-x-vol1-color",
    "label": "톤 아카이브는 여러 reference image role로 구성한다",
    "not_a_rule": true,
    "reference_image_roles": [
     "atmosphere_landscape",
     "material_texture",
     "object_or_fashion",
     "interior_or_space",
     "abstract_light_or_shadow"
    ],
    "source_observation": "제공 샘플은 키워드별로 단일 예시가 아니라 복수 이미지 예시를 세로로 배치해 사용 범위를 보여준다.",
    "status": "cataloged",
    "success_signals": [
     "같은 색상 키워드가 서로 다른 피사체에서도 같은 톤 정체성을 유지한다",
     "이미지 세트가 palette table이 아니라 mood archive처럼 읽힌다"
    ],
    "summary": "하나의 색상 키워드에는 자연 풍경, 재질 표면, 오브젝트/패션, 공간/인테리어, 추상 질감 같은 서로 다른 이미지 역할을 붙여 톤의 적용 폭을 보여준다.",
    "topic": "topic-color-tone-archive"
   },
   "space": "concept",
   "type": "ColorPattern"
  },
  {
   "id": "pattern-tonal-ramp-from-anchor-hex",
   "properties": {
    "example_source": "ref-reference-x-vol1-color",
    "label": "anchor HEX에서 tonal ramp를 파생한다",
    "not_a_rule": true,
    "prompt_do": [
     "tonal ramp를 먼저 정하고 anchor color는 강조점 또는 중심점으로 둔다",
     "이미지의 밝은 부분과 어두운 부분도 같은 키워드의 성격을 유지하게 한다"
    ],
    "source_observation": "제공 샘플의 실제 이미지는 대표색 하나보다 넓은 계열색과 명암을 포함한다.",
    "status": "cataloged",
    "summary": "하나의 HEX를 그대로 확대하지 않고, 어두운 저명도, 기준색, 따뜻한/차가운 하이라이트, 탁한 중간톤, 주변 중립색으로 톤 램프를 만든다.",
    "tone_range": [
     "deep_shadow",
     "anchor_mid_tone",
     "warm_highlight",
     "desaturated_haze",
     "adjacent_neutral"
    ],
    "topic": "topic-color-tone-archive"
   },
   "space": "concept",
   "type": "ColorPattern"
  },
  {
   "id": "ref-ui-neutral-ramp-contrast-derived",
   "properties": {
    "copyright_handling": "REFERENCE X나 Pantone 같은 유료/외부 출처의 색이 아니다. 대비 기준을 만족하는 명도 계단을 직접 계산한 값이며 복제 대상이 아니다.",
    "derivation": "WCAG 2.2 대비 요구(본문 4.5:1, 비텍스트 UI 3:1)와 화면 표면 역할에서 계산으로 도출.",
    "ingested_at": "2026-08-12",
    "label": "UI Neutral Ramp — 대비 기준에서 도출한 화면 중성 계단",
    "source_format": "derived_specification",
    "status": "cataloged",
    "summary": "브랜드 색 아카이브는 채도 있는 색을 다루지만 화면은 배경·경계·글자를 담당할 저채도 계단을 따로 필요로 한다. 이 레퍼런스는 그 빈자리를 채운다."
   },
   "space": "resource",
   "type": "ColorReference"
  },
  {
   "id": "topic-color-ui-neutral-ramp",
   "properties": {
    "core_question": "브랜드 색과 별개로, 화면 표면과 텍스트를 지탱하는 중성색을 어떤 온도와 명도 계단으로 고를 것인가.",
    "label": "UI Neutral Ramp — 화면의 배경·경계·글자를 담당하는 중성 계단",
    "not_a_rule": true,
    "status": "cataloged"
   },
   "space": "concept",
   "type": "ColorTopic"
  },
  {
   "id": "policy-ui-neutral-ramp-temperature-follows-brand",
   "properties": {
    "applies_when": {
     "medium": [
      "digital",
      "any"
     ]
    },
    "label": "중성색의 온도는 브랜드를 따라간다",
    "not_a_rule": false,
    "reason": "모든 제품이 같은 회색 배경에 같은 잉크를 쓰면 생성물 티가 난다. 중성색은 면적이 가장 넓어서 화면의 인상을 실제로 결정한다.",
    "statement": "화면 전체를 덮는 중성색은 브랜드와 무관한 기본 회색이 아니라, 브랜드 색조에 맞춘 온도(warm/cool/true)를 고른다.",
    "status": "cataloged"
   },
   "space": "concept",
   "type": "ColorPolicy"
  },
  {
   "id": "policy-ui-neutral-ramp-contrast-before-taste",
   "properties": {
    "applies_when": {
     "medium": [
      "digital",
      "any"
     ]
    },
    "label": "중성 계단은 취향보다 대비를 먼저 만족한다",
    "not_a_rule": false,
    "reason": "보정으로 구제해야 하는 계단은 팔레트가 바뀔 때마다 다시 어긋난다. 계단 자체가 기준을 넘으면 조합이 바뀌어도 안전하다.",
    "statement": "muted·ink 단계는 자기 배경에서 4.5:1, edge 단계는 3:1을 자체로 넘긴다. 사후 보정에 기대지 않는다.",
    "status": "cataloged"
   },
   "space": "concept",
   "type": "ColorPolicy"
  },
  {
   "id": "color-keyword-ui-neutral-warm-paper",
   "properties": {
    "applies_when": {
     "medium": [
      "digital",
      "any"
     ],
     "spectrum": [
      "neutral",
      "any"
     ]
    },
    "category": "UI Neutral Ramp",
    "color_name": "Warm Paper",
    "family": "ui_neutral.warm",
    "hex_basis": "contrast-derived screen value",
    "label": "Warm Paper (UI neutral)",
    "not_a_rule": true,
    "ramp_step": "paper",
    "rgb_hex": "#F8F6F5",
    "source_reference_id": "ref-ui-neutral-ramp-contrast-derived",
    "spectrum": "neutral",
    "status": "cataloged",
    "summary": "따뜻한 기미가 도는 화면 바탕. 종이 느낌의 읽기 표면이나 공예·에디토리얼 성격의 제품에서 가장 넓은 면적을 담당한다.",
    "ui_role": "canvas"
   },
   "space": "concept",
   "type": "ColorKeyword"
  },
  {
   "id": "color-keyword-ui-neutral-warm-veil",
   "properties": {
    "applies_when": {
     "medium": [
      "digital",
      "any"
     ],
     "spectrum": [
      "neutral",
      "any"
     ]
    },
    "category": "UI Neutral Ramp",
    "color_name": "Warm Veil",
    "family": "ui_neutral.warm",
    "hex_basis": "contrast-derived screen value",
    "label": "Warm Veil (UI neutral)",
    "not_a_rule": true,
    "ramp_step": "veil",
    "rgb_hex": "#EDEBE8",
    "source_reference_id": "ref-ui-neutral-ramp-contrast-derived",
    "spectrum": "neutral",
    "status": "cataloged",
    "summary": "바탕보다 한 단 눌린 표면. 입력 필드 배경, 비활성 영역, 표의 교차 행처럼 물러나야 하는 면에 쓴다.",
    "ui_role": "surface-muted"
   },
   "space": "concept",
   "type": "ColorKeyword"
  },
  {
   "id": "color-keyword-ui-neutral-warm-line",
   "properties": {
    "applies_when": {
     "medium": [
      "digital",
      "any"
     ],
     "spectrum": [
      "neutral",
      "any"
     ]
    },
    "category": "UI Neutral Ramp",
    "color_name": "Warm Line",
    "family": "ui_neutral.warm",
    "hex_basis": "contrast-derived screen value",
    "label": "Warm Line (UI neutral)",
    "not_a_rule": true,
    "ramp_step": "line",
    "rgb_hex": "#DCD7D1",
    "source_reference_id": "ref-ui-neutral-ramp-contrast-derived",
    "spectrum": "neutral",
    "status": "cataloged",
    "summary": "영역을 나누는 장식선. 구분이 목적이지 강조가 아니므로 대비를 낮게 유지한다.",
    "ui_role": "border"
   },
   "space": "concept",
   "type": "ColorKeyword"
  },
  {
   "id": "color-keyword-ui-neutral-warm-edge",
   "properties": {
    "applies_when": {
     "medium": [
      "digital",
      "any"
     ],
     "spectrum": [
      "neutral",
      "any"
     ]
    },
    "category": "UI Neutral Ramp",
    "color_name": "Warm Edge",
    "family": "ui_neutral.warm",
    "hex_basis": "contrast-derived screen value",
    "label": "Warm Edge (UI neutral)",
    "not_a_rule": true,
    "ramp_step": "edge",
    "rgb_hex": "#988C7E",
    "source_reference_id": "ref-ui-neutral-ramp-contrast-derived",
    "spectrum": "neutral",
    "status": "cataloged",
    "summary": "버튼과 입력창의 경계. WCAG 1.4.11이 요구하는 비텍스트 3:1을 자체로 넘기므로 컨트롤 테두리에 바로 쓸 수 있다.",
    "ui_role": "border-strong"
   },
   "space": "concept",
   "type": "ColorKeyword"
  },
  {
   "id": "color-keyword-ui-neutral-warm-muted",
   "properties": {
    "applies_when": {
     "medium": [
      "digital",
      "any"
     ],
     "spectrum": [
      "neutral",
      "any"
     ]
    },
    "category": "UI Neutral Ramp",
    "color_name": "Warm Muted",
    "family": "ui_neutral.warm",
    "hex_basis": "contrast-derived screen value",
    "label": "Warm Muted (UI neutral)",
    "not_a_rule": true,
    "ramp_step": "muted",
    "rgb_hex": "#726658",
    "source_reference_id": "ref-ui-neutral-ramp-contrast-derived",
    "spectrum": "neutral",
    "status": "cataloged",
    "summary": "보조 텍스트. 캡션, 메타 정보, 설명문에 쓰며 본문 대비 4.5:1을 넘긴다.",
    "ui_role": "ink-muted"
   },
   "space": "concept",
   "type": "ColorKeyword"
  },
  {
   "id": "color-keyword-ui-neutral-warm-ink",
   "properties": {
    "applies_when": {
     "medium": [
      "digital",
      "any"
     ],
     "spectrum": [
      "neutral",
      "any"
     ]
    },
    "category": "UI Neutral Ramp",
    "color_name": "Warm Ink",
    "family": "ui_neutral.warm",
    "hex_basis": "contrast-derived screen value",
    "label": "Warm Ink (UI neutral)",
    "not_a_rule": true,
    "ramp_step": "ink",
    "rgb_hex": "#2C2721",
    "source_reference_id": "ref-ui-neutral-ramp-contrast-derived",
    "spectrum": "neutral",
    "status": "cataloged",
    "summary": "본문 글자. 순검정보다 부드러워 긴 글에서 눈이 덜 피로하고, 따뜻한 바탕과 색조가 맞는다.",
    "ui_role": "ink"
   },
   "space": "concept",
   "type": "ColorKeyword"
  },
  {
   "id": "color-keyword-ui-neutral-cool-paper",
   "properties": {
    "applies_when": {
     "medium": [
      "digital",
      "any"
     ],
     "spectrum": [
      "neutral",
      "any"
     ]
    },
    "category": "UI Neutral Ramp",
    "color_name": "Cool Paper",
    "family": "ui_neutral.cool",
    "hex_basis": "contrast-derived screen value",
    "label": "Cool Paper (UI neutral)",
    "not_a_rule": true,
    "ramp_step": "paper",
    "rgb_hex": "#F5F6F7",
    "source_reference_id": "ref-ui-neutral-ramp-contrast-derived",
    "spectrum": "neutral",
    "status": "cataloged",
    "summary": "푸른 기미가 도는 화면 바탕. 도구·운영 화면이나 기술 제품에서 화면을 차분하게 눌러준다.",
    "ui_role": "canvas"
   },
   "space": "concept",
   "type": "ColorKeyword"
  },
  {
   "id": "color-keyword-ui-neutral-cool-veil",
   "properties": {
    "applies_when": {
     "medium": [
      "digital",
      "any"
     ],
     "spectrum": [
      "neutral",
      "any"
     ]
    },
    "category": "UI Neutral Ramp",
    "color_name": "Cool Veil",
    "family": "ui_neutral.cool",
    "hex_basis": "contrast-derived screen value",
    "label": "Cool Veil (UI neutral)",
    "not_a_rule": true,
    "ramp_step": "veil",
    "rgb_hex": "#E8EAED",
    "source_reference_id": "ref-ui-neutral-ramp-contrast-derived",
    "spectrum": "neutral",
    "status": "cataloged",
    "summary": "바탕보다 한 단 눌린 차가운 표면. 밀집한 데이터 화면에서 행과 패널을 구분한다.",
    "ui_role": "surface-muted"
   },
   "space": "concept",
   "type": "ColorKeyword"
  },
  {
   "id": "color-keyword-ui-neutral-cool-line",
   "properties": {
    "applies_when": {
     "medium": [
      "digital",
      "any"
     ],
     "spectrum": [
      "neutral",
      "any"
     ]
    },
    "category": "UI Neutral Ramp",
    "color_name": "Cool Line",
    "family": "ui_neutral.cool",
    "hex_basis": "contrast-derived screen value",
    "label": "Cool Line (UI neutral)",
    "not_a_rule": true,
    "ramp_step": "line",
    "rgb_hex": "#D2D5DB",
    "source_reference_id": "ref-ui-neutral-ramp-contrast-derived",
    "spectrum": "neutral",
    "status": "cataloged",
    "summary": "차가운 구분선. 표와 목록이 많은 화면에서 격자를 만들되 시선을 끌지 않는다.",
    "ui_role": "border"
   },
   "space": "concept",
   "type": "ColorKeyword"
  },
  {
   "id": "color-keyword-ui-neutral-cool-edge",
   "properties": {
    "applies_when": {
     "medium": [
      "digital",
      "any"
     ],
     "spectrum": [
      "neutral",
      "any"
     ]
    },
    "category": "UI Neutral Ramp",
    "color_name": "Cool Edge",
    "family": "ui_neutral.cool",
    "hex_basis": "contrast-derived screen value",
    "label": "Cool Edge (UI neutral)",
    "not_a_rule": true,
    "ramp_step": "edge",
    "rgb_hex": "#818895",
    "source_reference_id": "ref-ui-neutral-ramp-contrast-derived",
    "spectrum": "neutral",
    "status": "cataloged",
    "summary": "차가운 컨트롤 경계. 비텍스트 3:1을 자체로 넘기므로 버튼·입력창 테두리에 바로 쓴다.",
    "ui_role": "border-strong"
   },
   "space": "concept",
   "type": "ColorKeyword"
  },
  {
   "id": "color-keyword-ui-neutral-cool-muted",
   "properties": {
    "applies_when": {
     "medium": [
      "digital",
      "any"
     ],
     "spectrum": [
      "neutral",
      "any"
     ]
    },
    "category": "UI Neutral Ramp",
    "color_name": "Cool Muted",
    "family": "ui_neutral.cool",
    "hex_basis": "contrast-derived screen value",
    "label": "Cool Muted (UI neutral)",
    "not_a_rule": true,
    "ramp_step": "muted",
    "rgb_hex": "#5A6270",
    "source_reference_id": "ref-ui-neutral-ramp-contrast-derived",
    "spectrum": "neutral",
    "status": "cataloged",
    "summary": "차가운 보조 텍스트. 상태 라벨과 메타 정보에 쓰며 본문 대비를 넘긴다.",
    "ui_role": "ink-muted"
   },
   "space": "concept",
   "type": "ColorKeyword"
  },
  {
   "id": "color-keyword-ui-neutral-cool-ink",
   "properties": {
    "applies_when": {
     "medium": [
      "digital",
      "any"
     ],
     "spectrum": [
      "neutral",
      "any"
     ]
    },
    "category": "UI Neutral Ramp",
    "color_name": "Cool Ink",
    "family": "ui_neutral.cool",
    "hex_basis": "contrast-derived screen value",
    "label": "Cool Ink (UI neutral)",
    "not_a_rule": true,
    "ramp_step": "ink",
    "rgb_hex": "#21252B",
    "source_reference_id": "ref-ui-neutral-ramp-contrast-derived",
    "spectrum": "neutral",
    "status": "cataloged",
    "summary": "차가운 본문 글자. 도구 화면의 조밀한 텍스트에서 또렷하되 검게 눌리지 않는다.",
    "ui_role": "ink"
   },
   "space": "concept",
   "type": "ColorKeyword"
  },
  {
   "id": "color-keyword-ui-neutral-true-paper",
   "properties": {
    "applies_when": {
     "medium": [
      "digital",
      "any"
     ],
     "spectrum": [
      "neutral",
      "any"
     ]
    },
    "category": "UI Neutral Ramp",
    "color_name": "True Paper",
    "family": "ui_neutral.true",
    "hex_basis": "contrast-derived screen value",
    "label": "True Paper (UI neutral)",
    "not_a_rule": true,
    "ramp_step": "paper",
    "rgb_hex": "#F6F6F6",
    "source_reference_id": "ref-ui-neutral-ramp-contrast-derived",
    "spectrum": "neutral",
    "status": "cataloged",
    "summary": "색조 없는 바탕. 이미지나 제품 사진이 색을 담당해서 화면 크롬은 물러나야 할 때 고른다.",
    "ui_role": "canvas"
   },
   "space": "concept",
   "type": "ColorKeyword"
  },
  {
   "id": "color-keyword-ui-neutral-true-veil",
   "properties": {
    "applies_when": {
     "medium": [
      "digital",
      "any"
     ],
     "spectrum": [
      "neutral",
      "any"
     ]
    },
    "category": "UI Neutral Ramp",
    "color_name": "True Veil",
    "family": "ui_neutral.true",
    "hex_basis": "contrast-derived screen value",
    "label": "True Veil (UI neutral)",
    "not_a_rule": true,
    "ramp_step": "veil",
    "rgb_hex": "#EBEBEB",
    "source_reference_id": "ref-ui-neutral-ramp-contrast-derived",
    "spectrum": "neutral",
    "status": "cataloged",
    "summary": "색조 없는 눌린 표면. 콘텐츠가 색을 책임지는 화면에서 배경 단계만 만든다.",
    "ui_role": "surface-muted"
   },
   "space": "concept",
   "type": "ColorKeyword"
  },
  {
   "id": "color-keyword-ui-neutral-true-line",
   "properties": {
    "applies_when": {
     "medium": [
      "digital",
      "any"
     ],
     "spectrum": [
      "neutral",
      "any"
     ]
    },
    "category": "UI Neutral Ramp",
    "color_name": "True Line",
    "family": "ui_neutral.true",
    "hex_basis": "contrast-derived screen value",
    "label": "True Line (UI neutral)",
    "not_a_rule": true,
    "ramp_step": "line",
    "rgb_hex": "#D6D6D6",
    "source_reference_id": "ref-ui-neutral-ramp-contrast-derived",
    "spectrum": "neutral",
    "status": "cataloged",
    "summary": "색조 없는 구분선. 어떤 브랜드 색과도 충돌하지 않는다.",
    "ui_role": "border"
   },
   "space": "concept",
   "type": "ColorKeyword"
  },
  {
   "id": "color-keyword-ui-neutral-true-edge",
   "properties": {
    "applies_when": {
     "medium": [
      "digital",
      "any"
     ],
     "spectrum": [
      "neutral",
      "any"
     ]
    },
    "category": "UI Neutral Ramp",
    "color_name": "True Edge",
    "family": "ui_neutral.true",
    "hex_basis": "contrast-derived screen value",
    "label": "True Edge (UI neutral)",
    "not_a_rule": true,
    "ramp_step": "edge",
    "rgb_hex": "#8B8B8B",
    "source_reference_id": "ref-ui-neutral-ramp-contrast-derived",
    "spectrum": "neutral",
    "status": "cataloged",
    "summary": "색조 없는 컨트롤 경계. 비텍스트 3:1을 넘기며 어떤 배경 온도에도 붙는다.",
    "ui_role": "border-strong"
   },
   "space": "concept",
   "type": "ColorKeyword"
  },
  {
   "id": "color-keyword-ui-neutral-true-muted",
   "properties": {
    "applies_when": {
     "medium": [
      "digital",
      "any"
     ],
     "spectrum": [
      "neutral",
      "any"
     ]
    },
    "category": "UI Neutral Ramp",
    "color_name": "True Muted",
    "family": "ui_neutral.true",
    "hex_basis": "contrast-derived screen value",
    "label": "True Muted (UI neutral)",
    "not_a_rule": true,
    "ramp_step": "muted",
    "rgb_hex": "#656565",
    "source_reference_id": "ref-ui-neutral-ramp-contrast-derived",
    "spectrum": "neutral",
    "status": "cataloged",
    "summary": "색조 없는 보조 텍스트. 브랜드 색이 강할 때 텍스트가 경쟁하지 않게 한다.",
    "ui_role": "ink-muted"
   },
   "space": "concept",
   "type": "ColorKeyword"
  },
  {
   "id": "color-keyword-ui-neutral-true-ink",
   "properties": {
    "applies_when": {
     "medium": [
      "digital",
      "any"
     ],
     "spectrum": [
      "neutral",
      "any"
     ]
    },
    "category": "UI Neutral Ramp",
    "color_name": "True Ink",
    "family": "ui_neutral.true",
    "hex_basis": "contrast-derived screen value",
    "label": "True Ink (UI neutral)",
    "not_a_rule": true,
    "ramp_step": "ink",
    "rgb_hex": "#262626",
    "source_reference_id": "ref-ui-neutral-ramp-contrast-derived",
    "spectrum": "neutral",
    "status": "cataloged",
    "summary": "색조 없는 본문 글자. 순검정의 눈부심 없이 최대 대비에 가깝다.",
    "ui_role": "ink"
   },
   "space": "concept",
   "type": "ColorKeyword"
  }
 ],
 "schema_version": "design-ontology-harness/semantic-color-ontology-compact-v1",
 "source": {
  "built_at": "2026-08-12T14:03:22.155766+00:00",
  "copyright_handling": "Imported as abstracted color ontology nodes; no raw OCR, page images, or reconstructable source tables are included.",
  "path": "domains/color/ontology/build/graph.json",
  "repo": "semantic-os",
  "source_graph_sha256": "871f35eb6dd835996ece07e0748e06026db75d5e0cb8d45f7c2ba33ed398ca9e",
  "source_schema_version": "default-video-production-ontology-v1",
  "transport": "docs/color-reference.md"
 }
}
```

</details>
<!-- semantic-os-color-ontology:end -->
