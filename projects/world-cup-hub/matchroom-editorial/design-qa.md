# Design QA

## Comparison target

- Source visual truth: `/Users/sungwoon/ai-projects/design-ontology-harness/projects/world-cup-hub/matchroom-editorial/qa/source-option-1.png`
- Implementation URL: `http://127.0.0.1:4173/?fixture=kor-mex`
- Implementation top screenshot: `/Users/sungwoon/ai-projects/design-ontology-harness/projects/world-cup-hub/matchroom-editorial/qa/implementation-final.jpeg`
- Implementation bottom screenshot: `/Users/sungwoon/ai-projects/design-ontology-harness/projects/world-cup-hub/matchroom-editorial/qa/implementation-bottom.jpeg`
- Source viewport: 1487 × 1058
- Browser evidence viewport: 1530 × 768, captured as top and bottom states because the available browser window is shorter than the source frame.
- State: 대한민국 vs 멕시코, C조 2차전, 경기 전, 21:00.

The full-frame source and the browser capture do not have the same height. Fidelity was therefore judged from normalized region comparisons rather than from false pixel-level precision across mismatched crops.

## Evidence

- Full-view comparison: `/Users/sungwoon/ai-projects/design-ontology-harness/projects/world-cup-hub/matchroom-editorial/qa/comparison-final.jpg`
- Focused header, hero, analysis, and right-rail comparison: `/Users/sungwoon/ai-projects/design-ontology-harness/projects/world-cup-hub/matchroom-editorial/qa/comparison-top-focused.jpg`
- Focused schedule comparison: `/Users/sungwoon/ai-projects/design-ontology-harness/projects/world-cup-hub/matchroom-editorial/qa/comparison-bottom-focused.jpg`

Focused comparisons were required because the dense analysis labels and the bottom schedule are too small to judge reliably in the full-view pair.

## Findings

No actionable P0, P1, or P2 differences remain.

- Fonts and typography: Barlow Condensed recreates the compressed wordmark, time, and data treatment; Noto Sans KR provides stable Korean rhythm and weights. The display hierarchy, labels, and small data text remain legible without wrapping in the target desktop state.
- Spacing and layout rhythm: the header, stage rail, selected-match desk, right editorial rail, and bottom timeline retain the source order and proportions. Hairline borders, square surfaces, and low-elevation treatment match the editorial reference.
- Colors and visual tokens: warm paper, near-black ink, tournament red, muted green, and neutral dividers map directly to the source. The implementation introduces no gradients, glass effects, or unrelated dashboard colors.
- Image quality and asset fidelity: team flags use bundled `flag-icons` SVG assets, cropped into the tall reference slots. This intentionally replaces the generated mock's inaccurate abstract color bars with real flags while preserving their scale and position. UI icons come from one Phosphor family. No placeholder images or handwritten SVG assets are present.
- Copy and content: the central KOR–MEX match, fixture times, editorial headlines, match context, and schedule content match the selected concept. Dynamic team names, group labels, Korean particles, and URL fixture state update together.
- Accessibility: controls are semantic buttons, flag images have alt text, formation views have accessible labels, bookmark controls expose pressed state, and red/green are paired with text rather than used alone.
- Responsiveness: desktop layout matches the selected source. The implementation also provides explicit tablet and mobile reflow rules; these are outside the selected desktop visual truth and are not claimed as a pixel-matched secondary source.

## Interaction checks

- Selecting a fixture from the right rail updates the hero teams, kickoff, group, context, matchup rows, and URL fixture parameter.
- Selecting a fixture from the bottom timeline uses the same state path.
- Previous and next fixture controls wrap through the six-match schedule.
- Top navigation, stage groups, knockout stages, and bookmark controls expose active/selected state.
- Production build completed successfully with Vite.

## Comparison history

### Pass 1

- P0/P1/P2 findings: none.
- Residual P3: the browser evidence is split across top and bottom captures because the available live browser window is shorter than the source canvas. Region-normalized comparisons cover every visible source section.
- Intentional difference: real SVG flags replace the source mock's abstract and, for Korea, inaccurate flag-color bar.
- Post-check fix: bookmark buttons gained explicit `aria-pressed`; fixture selection gained a shareable query-string state; dynamic group labels, formation labels, and Korean particles were corrected.

## Follow-up polish

- P3: a future capture from an exact 1487 × 1058 or 1440 × 1024 browser viewport would allow a stricter full-frame pixel comparison, but no visible section or core interaction is currently missing.

final result: passed
