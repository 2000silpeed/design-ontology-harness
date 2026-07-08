# Tinge Design System

## Brand Idea

Tinge is a style calibration tool. The interface should feel like tuning color, silhouette, and restraint before shopping. It is quiet, direct, and a little editorial, but it must stay tool-like.

## Structure

- `occasion-pulse`: today's external constraints.
- `style-compass`: the primary decision object.
- `closet-tape`: owned garment memory.
- `silhouette-preview`: calibrated outfit direction.
- `accent-tray`: bounded missing-piece candidates.
- `decision-dock`: save or shortlist one accent.

## Visual Language

시각 값의 단일 진실 소스는 `design-system/tokens.css`다 (`emit-tokens`로 blueprint에서 생성).
구현 CSS는 `var(--ds-*)`만 소비하고, 여기에 색·서체 이름을 다시 쓰지 않는다.

- Palette: blueprint active palette — deep green anchor, teal fresh accent, quiet green tint.
  Supporting colors(claret, prussian blue, lavender, apricot)는 옷장 원단 표현에만 쓴다.
- Typography: Pretendard 단일 서체, weight 대비로 위계. 세리프 디스플레이 액센트 금지
  (tokens.css가 지정하지 않는 한).
- Surfaces are layered with fine borders and firm spacing. Avoid a wall of cards.
- Imagery must reveal garments, fabric, or silhouette, not abstract decoration.
- 검증: `lint-implementation` + `check-style-divergence`를 통과해야 완료로 간주한다.

## Component Contract

`brand_profile.component_decision.core_components` is the source of truth for actual implementation components. Product primitives describe product surfaces only; they must not choose components by rule.

Astryx and Geist are used only for state, anatomy, accessibility, and coverage checks.
