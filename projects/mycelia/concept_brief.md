# Mycelia — Concept Brief

> Image-first site design. Follow `docs/SITE_DESIGN_WORKFLOW.md`. Do NOT copy
> colors/fonts/tokens/layouts from `presets/*`, existing `projects/*`, or
> `tests/fixtures/*`. The ontology is grounding only.

## 1. Project understanding

- **Product (one line):** 시민과학 버섯 채집가를 위한 사진 식별 + 야외 채집 기록 + 종 도감 커뮤니티 웹앱.
- **Primary users:** 아마추어 채집가, 균류 애호가, 시민과학 데이터 기여자, 자연 교육자.
- **Tone:** 차분하고 박물지(natural-history)스러운, 신뢰감 있고 손맛 있는, 과시적이지 않은.
- **Anti-keywords:** neon, glassmorphism, default-tailwind-blue, emoji icons, dark techy dashboard, saas-gradient.

### Feature surfaces (one image per surface)

- `identify` — 사진 업로드 후 종 식별 결과 화면 (후보 종 목록 + 신뢰도 + 안전성 경고)
- `field-map` — 채집 위치 지도 + 주변 관찰 기록 핀 + 필터
- `logbook` — 내 채집 일지 + 선택한 종의 도감 상세

## 2. Design concept

- **Concept name:** Field Guide Naturalism
- **One sentence:** 빈티지 균류 도감(letterpress field guide)의 종이 질감과 잉크 라인 일러스트를, 정확하고 차분한 현대 웹 인터페이스로 재해석한다.
- **Adjectives (3–5):** earthy, archival, precise, tactile, calm
- **Anti-patterns:** 형광/네온 강조색, 글래스모피즘, 기본 Tailwind 블루, 이모지 아이콘, 다크 테크 대시보드, 과한 그라데이션.

(Validated against ontology mood vocabulary: 자연/신뢰/전문성/안정 계열. 컨셉을 프리셋에서
고르지 않고 제품 성격에서 직접 도출.)

## 3. Color set

See `color_set.json`. Earthy naturalist palette: 깊은 숲 녹색을 dominant action으로,
따뜻한 종이 톤을 base surface로, 단일 포자(spore) 앰버를 accent로. 상태색은 자연 톤 안에서
구분되도록 채도를 절제. 이 색상이 4단계 이미지 프롬프트의 색 지침이 된다.

## 4–6

- 4: 각 surface를 GPT Image 2(`gpt_image_2`, 16:9, 2k, high)로 생성 → `generated/` + `screen_plan.json`
- 5: 생성 화면에서 `design-system/`(토큰·컴포넌트·폰트) 역도출
- 6: 온톨로지로 grounding/검증 후 `check-site-design`
