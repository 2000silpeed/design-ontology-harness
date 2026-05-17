from __future__ import annotations

import json
from collections import Counter, defaultdict
from pathlib import Path

from .authoring import generate_system_pack
from .benchmark_kb import build_benchmark_context, save_benchmark_report
from .color_reference import resolve_color_reference
from .css_pipeline import load_css_extraction
from .font_reference import resolve_font_system
from .graph_builders import VISUAL_ASSET_COMPATIBLE_MANIFEST_PATHS
from .models import DocumentRecord, ReferenceLink
from .reference_context import build_design_context_pack
from .utils import ensure_dir, write_json
from .visual_reference import resolve_visual_reference

AI_SYNTHESIS_PRINCIPLES = [
    {
        "id": "no_fabricated_hex",
        "rule": "hex를 만들지 않는다",
        "detail": "AI는 색상 hex 값을 임의로 생성하지 않는다. 반드시 color_reference, CSS 추출, 브랜드 가이드 등 실증 소스에서 가져온 값만 사용한다.",
    },
    {
        "id": "no_fabricated_token_names",
        "rule": "토큰명을 만들지 않는다",
        "detail": "AI는 토큰 이름을 임의로 발명하지 않는다. 네이밍 패턴(core/semantic/component 레이어 규칙)은 정의하되, 구체적 토큰명은 실제 컴포넌트와 역할에서 도출한다.",
    },
    {
        "id": "interpretation_over_facts_only",
        "rule": "팩트 위에 해석만",
        "detail": "AI는 수집된 레퍼런스, 프로필, 온톨로지 증거 위에 해석과 구조화만 수행한다. 증거 없는 추론, 존재하지 않는 패턴 서술, 가상의 사용 사례 생성을 금지한다.",
    },
    {
        "id": "no_emoji_as_ui",
        "rule": "이모지를 UI 요소로 쓰지 않는다",
        "detail": "AI는 아이콘, 상태 표시, 버튼 장식, 네비게이션 지표 등 UI 컴포넌트 자리에 이모지(🎨 ✅ 🔥 ⚡ 🚀 ❌ ⭐ 📊 등)를 절대 넣지 않는다. 반드시 SVG 파일/아이콘 컴포넌트 또는 아이콘 라이브러리(Lucide, Heroicons, Phosphor, Tabler 등)를 사용한다. 리팩토링 중 카드, 버튼, 배지, 탭, 상태 표시, empty state에서 이모지를 발견하면 그대로 두지 말고 적절한 SVG 아이콘으로 교체한다. 이모지는 본문 콘텐츠(예: 블로그 텍스트, 사용자 입력)에서만 허용되며, 시스템 UI 요소로는 금지한다.",
    },
    {
        "id": "implement_components_directly",
        "rule": "컴포넌트를 직접 구현한다",
        "detail": "AI는 '임시 버튼', '플레이스홀더 카드', 'TODO 컴포넌트' 같은 반쪽 구현을 남기지 않는다. system_spec.md의 Component Strategy와 component_specs.md에 정의된 구조(anatomy), 상태(states), 토큰 바인딩, 접근성 규칙을 그대로 따라 완전한 컴포넌트를 구현한다. 기존 라이브러리 컴포넌트를 그냥 import해서 쓰는 대신, 디자인 시스템 토큰으로 스타일을 명시적으로 바인딩한다.",
    },
    {
        "id": "operational_surface_over_pitch_deck",
        "rule": "상용 제품 화면처럼 구성한다",
        "detail": "AI는 대시보드, 도구, 데이터 제품, 커뮤니티 제품을 피치덱식 히어로와 균일한 장식 카드 묶음으로 시작하지 않는다. 첫 화면은 사용자가 실제로 확인하거나 조작해야 하는 상태, 필터, 표/리스트, 출처, 업데이트 시각, 핵심 액션을 먼저 보여준다.",
    },
    {
        "id": "licensed_visual_assets_only",
        "rule": "검색 이미지는 라이선스가 검증될 때만 사용한다",
        "detail": "AI는 image_gen을 사용할 수 없거나 실제 사진성이 더 중요한 경우에만 sourced visual fallback을 사용한다. 무료 provider는 per-asset license metadata가 필요하고, paid provider는 license_proof/usage_scope/licensed_to가 필요하다. Reference-only provider는 형태와 밀도 참고만 가능하며 이미지를 구현 에셋으로 복사하지 않는다. source_url, download_url, provider, author, license, attribution_required, sha256, alt_text를 manifest에 기록하지 못하는 이미지는 구현에 넣지 않는다. 런타임 hotlink와 stock/search 이미지를 앱 아이콘·로고·상태 아이콘으로 쓰는 것을 금지한다.",
    },
]

REFERENCE_ABSORPTION_SCOPE = {
    "allowed": [
        "component morphology",
        "layout density",
        "panel/card proportions",
        "hierarchy rhythm",
        "interaction affordance patterns",
    ],
    "denied": [
        "color palette",
        "palette composition or derived secondary palettes",
        "typography family or scale",
        "semantic status colors",
        "product copy",
        "product data model",
        "navigation labels",
        "domain information architecture",
        "redistributable imagery unless explicitly licensed",
    ],
    "rule": "Visual references are morphology inputs only; tokens, component specs, and product IA remain authoritative.",
    "failure_patterns": [
        {
            "id": "token-bound-reference-palette-mixing",
            "trigger": "Implementation uses --ds-* tokens but recombines visual-reference-like dark rails, teal/blue secondaries, or status/tint roles into a new palette.",
            "rule": "Token binding is necessary but not sufficient; color role composition must still follow the ontology palette roles.",
            "prevention": "Derived colors may alias a semantic token or mix one semantic role with a neutral surface/transparent value. Do not mix multiple chromatic roles to create a local palette.",
            "technical_controls": ["IMPLEMENTATION_CONTRACT.md", "lint-implementation DS030", "lint-implementation DS031"],
        }
    ],
    "promotion_policy": {
        "id": "implementation-feedback-promotion",
        "rule": "When implementation review identifies a repeatable design-system failure, promote it into governance, generated artifacts, and lint checks before treating the current screen as complete.",
        "outputs": ["design_system_blueprint.governance", "system_spec.md", "system_ontology.json", "IMPLEMENTATION_CONTRACT.md"],
    },
}

RESPONSIVE_RESILIENCE_POLICY = {
    "id": "responsive-resilience",
    "rule": "Every generated or refactored UI must preserve horizontal fit at mobile widths before visual polish is considered complete.",
    "viewport_contract": {
        "required_widths_px": [320, 360, 390, 430, 768, 1024, 1440],
        "pass_condition": "document.documentElement.scrollWidth <= window.innerWidth and all primary controls remain reachable without horizontal scrolling.",
    },
    "control_rules": [
        "Buttons, CTA groups, tabs, filter chips, and toolbar actions must not rely on fixed px widths or mobile-hostile min-width values.",
        "Every button-like control needs max-inline-size: 100%; controls inside flex/grid parents need min-inline-size: 0 so labels can shrink or wrap.",
        "Action rows must wrap or stack at narrow widths; two-button rows need a <=480px fallback before implementation is complete.",
        "Long Korean CTA labels must be tested with real copy. Prefer wrapping/stacking over clipping, overflow hidden, or forcing white-space: nowrap.",
        "Horizontal rails, tickers, score strips, and carousels must not reveal partially clipped text. Either size cards so visible items are complete, or use compact labels such as icon+code in the rail and move full names to the detailed surface.",
        "Do not use width: 100vw inside padded containers; it commonly creates horizontal scroll. Use width: 100%, max-width: 100%, or a documented full-bleed pattern.",
        "Never hide body overflow-x as the fix for a layout bug; remove the overflowing width/min-width instead.",
    ],
    "failure_patterns": [
        {
            "id": "mobile-control-overflow",
            "trigger": "A button, CTA, tab, chip, or action group extends beyond a 320-430px viewport or requires sideways scrolling.",
            "rule": "Controls must fit, wrap, or stack within their container at mobile widths.",
            "prevention": "Ban fixed/min-width px sizing on button-like controls unless paired with max-inline-size: 100%, min-inline-size: 0, and a mobile wrap/stack fallback.",
            "technical_controls": ["system_spec.md Responsive Resilience", "components/component_specs.md button notes", "lint-implementation DS040", "lint-implementation DS042", "viewport screenshot QA"],
        },
        {
            "id": "viewport-horizontal-overflow",
            "trigger": "The page has horizontal scroll at mobile widths because a section, grid, or full-bleed element exceeds the viewport.",
            "rule": "No generated screen is complete while scrollWidth exceeds innerWidth on supported mobile viewports.",
            "prevention": "Avoid 100vw in padded containers, use minmax(0, 1fr) for grids, set min-width: 0 on flex/grid children, and verify 320/360/390/430px screenshots.",
            "technical_controls": ["system_spec.md viewport contract", "lint-implementation DS041", "lint-implementation DS043", "Playwright mobile viewport check"],
        },
        {
            "id": "horizontal-rail-label-clipping",
            "trigger": "A horizontal ticker, score strip, carousel, or date rail shows ellipsized/cropped labels or exposes a partial next card with clipped readable text.",
            "rule": "Scrollable rails may hint that more content exists, but visible text inside each rendered item must be complete and legible.",
            "prevention": "Use whole-card column math at tablet/desktop breakpoints; at mobile widths show one full card or remove full names from the rail. Split dense scan labels from descriptive names, and preserve full names in aria-labels or detail panels.",
            "technical_controls": ["system_spec.md Responsive Resilience", "component_specs.md rail/ticker notes", "viewport screenshot QA", "Playwright element scrollWidth<=clientWidth checks"],
        },
    ],
    "outputs": ["design_system_blueprint.governance", "system_spec.md", "token_schema.json", "component_specs.md", "IMPLEMENTATION_CONTRACT.md", "lint-implementation"],
}

COLOR_MODE_PARITY_POLICY = {
    "id": "color-mode-parity",
    "rule": "Every generated or refactored product UI must ship a normal light mode and a dark mode unless the user explicitly requests a single-mode artifact.",
    "required_modes": ["light", "dark"],
    "default_mode": "light",
    "implementation_rules": [
        "Use light mode as the default :root or app-default token set; dark mode must be an override such as [data-theme=\"dark\"].",
        "Do not build dark-only surfaces for dashboards, tools, landing pages, or prototypes unless explicitly requested.",
        "Every semantic surface/text/border/accent role needs a light and dark value or a documented derivation.",
        "Theme toggles, preview links, screenshots, or QA scripts must verify both modes when the implementation has a UI shell.",
        "Do not solve dark mode by inverting the entire page; define mode-specific semantic tokens and keep imagery/icons legible in both modes.",
    ],
    "failure_patterns": [
        {
            "id": "dark-only-implementation",
            "trigger": "A generated UI defines only dark surfaces or color-scheme: dark without a light/default token mode.",
            "rule": "Normal light mode is required alongside dark mode.",
            "prevention": "Define :root light tokens, add [data-theme=\"dark\"] overrides, and verify both modes before completion.",
            "technical_controls": ["system_spec.md Color Mode Parity", "system_ontology.json ColorMode", "lint-implementation DS060", "light/dark screenshot QA"],
        },
        {
            "id": "theme-token-drift",
            "trigger": "Light and dark modes use unrelated local colors instead of paired semantic roles.",
            "rule": "Mode values must map through the same semantic token roles.",
            "prevention": "Keep mode differences inside artifact token files such as design-system/tokens.css; components should consume the same semantic variables in both modes.",
            "technical_controls": ["token_schema.json semantic roles", "IMPLEMENTATION_CONTRACT.md", "lint-implementation DS061"],
        },
    ],
    "outputs": ["design_system_blueprint.governance", "system_spec.md", "system_ontology.json", "token_schema.json", "IMPLEMENTATION_CONTRACT.md", "agent_packs", "lint-implementation"],
}

ICON_REFACTOR_POLICY = {
    "id": "emoji-to-svg-refactor",
    "rule": "During UI refactors, emoji-looking UI affordances must be replaced with SVG-based icons instead of preserved as text glyphs.",
    "targets": ["button", "card", "badge", "tab", "navigation item", "status indicator", "empty state", "toast", "banner"],
    "replacement_order": [
        "Use the project's existing icon library when one is already installed and stylistically compatible.",
        "Reuse existing local SVG/icon components when available.",
        "Create a simple local SVG file or SVG component when no suitable icon exists.",
    ],
    "implementation_rules": [
        "Keep SVG stroke/fill bound to currentColor or design tokens, not hard-coded palette values.",
        "Decorative SVG icons use aria-hidden=\"true\"; semantic icons get an accessible label or adjacent text.",
        "Store new SVG assets in the nearest existing icons/assets directory; create a minimal icons directory only when none exists.",
        "Do not replace user-generated emoji content, chat text, blog body, or emoji-picker data.",
        "Do not use emoji as a placeholder while searching for a proper icon.",
    ],
    "failure_patterns": [
        {
            "id": "emoji-ui-affordance",
            "trigger": "A button, card, nav item, badge, status indicator, or empty state uses an emoji as its icon or visual marker.",
            "rule": "UI affordances must use SVG files/components or an approved icon library, never emoji glyphs.",
            "prevention": "Replace the emoji with an appropriate existing icon, imported icon, or locally authored SVG with token-bound color and accessible semantics.",
            "technical_controls": ["component_specs.md Non-negotiable", "design-system-refactor skill", "lint-implementation DS050"],
        }
    ],
    "outputs": ["system_spec.md", "component_specs.md", "IMPLEMENTATION_CONTRACT.md", "agent_packs", "lint-implementation"],
}

APP_ICON_IDENTITY_POLICY = {
    "id": "brand-app-icon-identity",
    "rule": "Every app or website implementation must include a brand-specific app icon identity asset; generic initial-letter tiles are not acceptable as final app icons.",
    "required_assets": [
        {
            "id": "identity-asset:app-icon",
            "label": "Brand app icon",
            "required": True,
            "formats": ["svg source", "favicon", "web app manifest icon when applicable"],
            "targets": ["favicon", "app shell brand mark", "web app manifest", "mobile home-screen icon"],
            "description": "A compact identity mark that encodes the product domain, brand palette, and interaction posture without relying on generic initials.",
        }
    ],
    "implementation_rules": [
        "Do not ship a plain initials tile such as WC, AI, DS, or App as the final app icon unless the brand system explicitly defines that lettermark.",
        "The app icon must use the brand palette, visual keywords, and product primitives as evidence for shape language.",
        "Use a deterministic SVG source for the primary app icon; generated raster imagery may support marketing visuals but must not replace the identity icon source.",
        "Wire the app icon into favicon/link metadata and the visible app-shell brand mark when the implementation has one.",
        "Keep small-size legibility: the icon must remain recognizable at 32px and in a 44px navigation mark.",
    ],
    "failure_patterns": [
        {
            "id": "generic-initials-app-icon",
            "trigger": "A favicon, app-shell mark, or web app icon uses generic initials or placeholder text instead of a brand-specific identity asset.",
            "rule": "App icons are required brand identity assets, not temporary text badges.",
            "prevention": "Create or reuse a brand-specific SVG app icon, wire it to favicon/manifest/app-shell surfaces, and document it in the ontology.",
            "technical_controls": ["system_spec.md Brand Identity Assets", "system_ontology.json BrandIdentityAsset", "IMPLEMENTATION_CONTRACT.md", "viewport screenshot QA"],
        }
    ],
    "outputs": ["brand_profile", "system_spec.md", "system_ontology.json", "IMPLEMENTATION_CONTRACT.md", "agent_packs", "lint-implementation"],
}

COMMERCIAL_PRODUCT_REALISM_POLICY = {
    "id": "commercial-product-realism",
    "rule": "Product and data UIs must feel operated, not generated: lead with real workflow state, data density, provenance, and asymmetric hierarchy instead of pitch-deck hero composition.",
    "applies_to": [
        "dashboard",
        "tool",
        "sports data product",
        "community product",
        "operational surface",
        "B2B/SaaS product UI",
    ],
    "diagnosis": [
        "AI-looking screens often use a large cinematic hero, symmetric card grids, generic metric tiles, and equally polished panels before the actual task surface appears.",
        "Commercial sports and data products feel more credible because they expose compact live modules, filters, list/table rows, timestamps, source labels, status variation, and editorial or utility rails.",
        "Generated raster imagery becomes suspicious when it dominates a workflow screen and is not tied to actual product state, team identity, venue context, or inspectable content.",
    ],
    "required_signals": [
        "first-viewport task surface",
        "compact data/list/table module where the domain expects scanning",
        "clear primary action or filter path",
        "status variation such as live, final, upcoming, delayed, empty, error, or source-updated",
        "source labels, timestamps, sample/demo labels, or data provenance for exact numbers",
        "domain-specific identity assets such as team crests, app icon, venue/match labels, or object imagery when applicable",
        "national flag identity marks for country-based tournaments, paired with code/name text for scanability and accessibility",
        "reference-backed domain morphology such as score strips, compact rails, tables, tabs, and editorial sidebars before major realism refactors",
    ],
    "successful_patterns": [
        {
            "id": "same-domain-reference-before-redesign",
            "rule": "Before a realism pass, collect same-domain commercial references and current-state screenshots.",
            "implementation": "Use reference screenshots to extract morphology only: module order, density, rail/table rhythm, status texture, and hierarchy.",
            "verification": "A research report or design-context pack exists, and implementation notes name what was absorbed and what was not copied.",
        },
        {
            "id": "operational-header-before-hero-media",
            "rule": "Sports/data products open with operational status and task controls, not a cinematic hero.",
            "implementation": "Use compact status strips, date/filter rails, next match/current item, source labels, and primary task surfaces above decorative imagery.",
            "verification": "First viewport contains inspectable data/state modules before or alongside any generated visual context.",
        },
        {
            "id": "score-ticker-as-scan-surface",
            "rule": "Match tickers are scan surfaces; they should favor compact identity and state over full descriptive copy.",
            "implementation": "Use flag/code or icon/code labels, status chips, short prediction/result labels, and whole-card scroll math. Move full names and explanations to detail panels or aria-labels.",
            "verification": "Ticker item text does not clip at 390, 1024, or 1440px, and full match names remain available in detail views or accessibility labels.",
        },
        {
            "id": "national-flag-code-identity",
            "rule": "Country-based tournament UIs use national flag identity marks plus team codes/names as the primary recognition layer.",
            "implementation": "Use deterministic local SVG/CSS flag marks or licensed flag assets; pair with FIFA/IOC-style codes in dense rails and names in detailed surfaces.",
            "verification": "No emoji flags are used as UI icons; flag colors are represented through design-system tokens such as --ds-color-* rather than local raw colors.",
        },
        {
            "id": "source-ledger-and-sample-labeling",
            "rule": "Exact-looking sports metrics, predictions, and schedules need visible provenance.",
            "implementation": "Add source ledger, updated-at labels, sample/demo labels, and clear separation between official fixtures/results and MVP sample predictions/opinions.",
            "verification": "Numbers and predictions have source/update/sample context in the first screen or nearby metadata.",
        },
        {
            "id": "editorial-insight-side-rail",
            "rule": "Sports hubs benefit from an asymmetric side rail for context, fan pulse, and editorial watch points.",
            "implementation": "Pair the primary schedule/table with a sticky or stacked rail containing selected match, country tracking, fan reaction, and group implication cards.",
            "verification": "Primary task remains dominant while the rail provides contextual depth without becoming a homogeneous card wall.",
        },
        {
            "id": "visual-context-secondary",
            "rule": "Generated or atmospheric imagery supports venue/domain context but does not replace the product workflow.",
            "implementation": "Keep generated images small or secondary in operational products; use them to reinforce venue/command-center mood after schedule/status surfaces are visible.",
            "verification": "The image is not the largest first-viewport object in dashboards/tools unless the user explicitly requests a landing page.",
        },
        {
            "id": "dual-mode-screenshot-qa",
            "rule": "Light mode is the default product mode and dark mode remains available; both need screenshot QA.",
            "implementation": "Bind components to paired semantic tokens and capture at least light mode plus dark mode when theme support exists.",
            "verification": "The implementation includes :root light tokens, dark overrides, and viewport screenshots or checks for both modes.",
        },
        {
            "id": "brand-app-icon-as-required-identity",
            "rule": "App icon identity is part of product completeness, not optional polish.",
            "implementation": "Create or discover a brand-specific deterministic SVG app icon, wire favicon/manifest/app-shell, and avoid generic initials such as WC unless explicitly defined by the brand.",
            "verification": "BrandIdentityAsset is present in the ontology and the icon is visible in browser/app shell surfaces.",
        },
    ],
    "implementation_rules": [
        "For dashboards, tools, sports/data products, and community products, do not make the first screen read like a marketing landing page unless the user explicitly asks for a landing page.",
        "Replace oversized hero pitches with an operational header: current status, primary workflow, filters/date rail, next item, or live summary.",
        "Use compact rows, tables, rails, tabs, and status chips when the domain task is scanning or comparison; reserve large cards for true summaries or repeated content items.",
        "Avoid homogeneous card walls where every module has the same weight, radius, tint, icon treatment, and spacing. Create an explicit hierarchy between primary task, secondary rail, and supporting modules.",
        "Exact metrics, model outputs, poll counts, odds, rankings, or match data need source/update context or a visible sample/demo label.",
        "Generated or decorative imagery must support the domain object, venue, person, product, or state. It must not replace data, navigation, controls, or the first operational surface.",
        "Use asymmetry and real product rhythm: some dense modules, some editorial/context rails, some compact controls, and visible state variation.",
        "For country-based sports competitions, represent teams with deterministic SVG/CSS flag marks plus text codes or names. Do not use platform emoji flags as UI icons, and do not default to generic colored letter badges when national identity is the primary domain signal.",
        "Flag colors and domain identity marks are design-system tokens. Do not create implementation-local --flag-* or raw color values in component CSS; use --ds-color-* or generated asset metadata.",
        "When a product UI is judged AI-looking, gather at least two same-domain commercial references and convert only observed morphology into the implementation: module order, density, status texture, rail/table patterns, and state hierarchy. Do not copy competitor copy, data, palette, or navigation taxonomy.",
    ],
    "failure_patterns": [
        {
            "id": "pitch-deck-dashboard-shell",
            "trigger": "A dashboard, tool, sports/data, or community UI opens with an oversized marketing hero, broad slogan, and feature cards before the real workflow or data surface.",
            "rule": "Operational products must lead with the user's live task or inspectable product state, not a pitch-deck composition.",
            "prevention": "Start with a compact command header, status strip, active filters/date rail, table/list, or primary workflow module; move marketing copy lower or remove it.",
            "technical_controls": ["system_spec.md Commercial Product Realism", "system_ontology.json GovernanceRule", "IMPLEMENTATION_CONTRACT.md", "agent_packs", "visual QA"],
        },
        {
            "id": "homogeneous-card-wall",
            "trigger": "The first viewport is dominated by equally weighted cards with similar radius, shadow, icon chips, label style, and spacing.",
            "rule": "Commercial product UIs need hierarchy, density variation, and task-led asymmetry.",
            "prevention": "Promote one primary workflow module, compress secondary data into rows/tables/rails, and vary module scale only when the information architecture justifies it.",
            "technical_controls": ["system_spec.md Component Strategy", "component_specs.md module hierarchy notes", "visual QA"],
        },
        {
            "id": "decorative-ai-hero-over-data",
            "trigger": "A cinematic generated image or decorative visual dominates a product workflow where users need schedules, results, controls, or status first.",
            "rule": "Generated imagery supports product context but does not outrank the operational surface.",
            "prevention": "Make imagery secondary, domain-specific, and connected to real content; prioritize score strips, tables, filters, or domain objects in the first viewport.",
            "technical_controls": ["system_spec.md Generated Visual Asset Plan", "system_spec.md Commercial Product Realism", "image manifest review"],
        },
        {
            "id": "synthetic-metric-copy",
            "trigger": "The UI shows precise-looking numbers, predictions, rankings, poll counts, or operational claims without source, timestamp, sample/demo labeling, or data provenance.",
            "rule": "Credible product data must expose provenance or clearly identify itself as sample/demo data.",
            "prevention": "Add source/update labels, sample badges, data-footnote components, or remove exact-looking fabricated values until real data is available.",
            "technical_controls": ["system_spec.md Content/Data Provenance", "component_specs.md data footnote", "copy review"],
        },
        {
            "id": "missing-operational-state-texture",
            "trigger": "Lists, cards, schedules, feeds, or dashboards have only ideal/default states and no live/final/empty/error/delayed/source-updated variation.",
            "rule": "Commercial interfaces reveal operational state texture through varied statuses and edge cases.",
            "prevention": "Design and implement realistic domain states before final visual polish; include at least the states required by component_specs.md and product primitives.",
            "technical_controls": ["component_specs.md states", "system_ontology.json ComponentState", "scenario QA"],
        },
        {
            "id": "reference-free-realism-refactor",
            "trigger": "A screen receives 'AI-looking' or 'not commercial enough' feedback and the next iteration changes styling from taste alone without collecting same-domain commercial references.",
            "rule": "Commercial realism fixes must be evidence-backed: reference data informs morphology, while ontology tokens, component specs, and product goals remain authoritative.",
            "prevention": "Capture a current-state screenshot, collect at least two same-domain references, summarize observed patterns, and implement the relevant density, rail, table, status, or hierarchy changes without copying protected content.",
            "technical_controls": ["Reference Intelligence", "Commercial Product Realism", "visual QA screenshots", "implementation feedback promotion"],
        },
        {
            "id": "generic-national-team-badges",
            "trigger": "A country-based sports UI represents national teams only as generic colored badges, initials, or abstract crests while flags are the expected recognition layer.",
            "rule": "National-team products should expose flag identity marks as the primary visual cue, with text codes/names retained for scanability and accessibility.",
            "prevention": "Use local deterministic SVG/CSS flag marks or licensed flag assets paired with team codes. Avoid emoji flags and avoid replacing readable text with image-only flags.",
            "technical_controls": ["Commercial Product Realism", "Brand Identity Assets", "icon_refactor_policy", "visual QA screenshots"],
        },
        {
            "id": "untokenized-domain-identity-colors",
            "trigger": "A UI introduces local flag, team, league, venue, or domain identity colors directly inside implementation CSS instead of design-system tokens.",
            "rule": "Domain identity colors are still governed design tokens; component CSS consumes token roles rather than inventing local palette variables.",
            "prevention": "Promote domain identity colors into token files as --ds-color-* or documented asset metadata, then bind components to those variables.",
            "technical_controls": ["lint-implementation DS003", "token_schema.json", "Commercial Product Realism", "Brand Identity Assets"],
        },
    ],
    "outputs": ["design_system_blueprint.governance", "system_spec.md", "system_ontology.json", "IMPLEMENTATION_CONTRACT.md", "agent_packs", "visual QA"],
}

KEYWORD_PRINCIPLES = {
    "calm": {
        "name": "Calm by Default",
        "rule": "기본 상태는 조용해야 하고, 강조는 정말 필요할 때만 사용합니다.",
        "implications": ["채도 낮은 기본 팔레트", "모션은 짧고 낮은 진폭", "화면당 핵심 액션 수 제한"],
    },
    "precise": {
        "name": "Precision Over Ornament",
        "rule": "장식보다 정보의 정렬, 상태의 정확성, 반응의 일관성을 우선합니다.",
        "implications": ["명확한 상태 규칙", "촘촘한 spacing scale", "컴포넌트 변형 최소화"],
    },
    "editorial": {
        "name": "Editorial Hierarchy",
        "rule": "타이포그래피와 여백으로 위계를 만들고, 장식은 의미를 돕는 범위에서만 사용합니다.",
        "implications": ["텍스트 중심 레이아웃", "강한 heading rhythm", "콘텐츠 읽기 흐름 우선"],
    },
    "trustworthy": {
        "name": "Trust Through Consistency",
        "rule": "예측 가능한 인터랙션과 안정적인 시각 언어로 신뢰를 쌓습니다.",
        "implications": ["일관된 disabled/error/success 패턴", "접근성 기준 우선", "위험 액션 명시적 구분"],
    },
    "bold": {
        "name": "Bold with Discipline",
        "rule": "강한 개성은 허용하되 구조를 해치지 않는 선에서 통제합니다.",
        "implications": ["강한 accent 색상 1개 중심", "대형 헤드라인 제한적 사용", "캠페인성 요소와 제품 UI 분리"],
    },
}


def load_brand_profile(path: Path) -> dict:
    profile = json.loads(path.read_text(encoding="utf-8"))
    reference_config = profile.get("color_reference")
    if reference_config:
        resolved_reference, issues = resolve_color_reference(reference_config, path.parent, profile)
        if resolved_reference:
            profile["_resolved_color_reference"] = resolved_reference
        if issues:
            profile["_color_reference_issues"] = issues

    font_config = profile.get("font_reference")
    if font_config is None or font_config is True:
        profile["_resolved_font_system"] = resolve_font_system(profile)

    visual_config = profile.get("visual_reference")
    if visual_config:
        resolved_visual_reference, issues = resolve_visual_reference(visual_config, path.parent, profile)
        if resolved_visual_reference:
            profile["_resolved_visual_reference"] = resolved_visual_reference
        if issues:
            profile["_visual_reference_issues"] = issues
        profile["_design_context_pack"] = build_design_context_pack(
            profile,
            resolved_visual_reference if resolved_visual_reference else {},
        )

    generated_visual_asset_manifests = discover_generated_visual_asset_manifests(path.parent)
    if generated_visual_asset_manifests:
        profile["_generated_visual_asset_manifests"] = generated_visual_asset_manifests

    identity_assets = discover_brand_identity_assets(path.parent, profile)
    if identity_assets:
        profile["_identity_assets"] = identity_assets

    return profile


def discover_brand_identity_assets(project_dir: Path, profile: dict | None = None) -> list[dict]:
    """Discover project-local brand identity assets that should be promoted into ontology."""
    profile = profile or {}
    assets: list[dict] = []
    seen_ids: set[str] = set()

    for asset in profile.get("identity_assets", []):
        if not isinstance(asset, dict):
            continue
        asset_id = str(asset.get("id") or "identity-asset:app-icon")
        seen_ids.add(asset_id)
        assets.append(asset)

    app_icon_candidates = [
        "assets/app-icon.svg",
        "public/app-icon.svg",
        "app-icon.svg",
        "favicon.svg",
    ]
    manifest_candidates = [
        "site.webmanifest",
        "manifest.webmanifest",
        "public/site.webmanifest",
        "public/manifest.webmanifest",
    ]
    app_icon_path = next((path for path in app_icon_candidates if (project_dir / path).exists()), None)
    if app_icon_path and "identity-asset:app-icon" not in seen_ids:
        manifest_path = next((path for path in manifest_candidates if (project_dir / path).exists()), None)
        targets = ["favicon", "app shell brand mark"]
        if manifest_path:
            targets.append("web app manifest")
        assets.append({
            "id": "identity-asset:app-icon",
            "label": "Brand app icon",
            "slot": "app-icon",
            "required": True,
            "integrated": True,
            "asset_path": app_icon_path,
            "manifest_path": manifest_path,
            "format": "svg",
            "targets": targets,
            "description": "Project-local app icon discovered from common brand identity asset paths.",
            "discovered_from": "common-app-icon-path",
        })

    return assets


def discover_generated_visual_asset_manifests(project_dir: Path) -> list[dict]:
    """Load project-local generated or sourced visual asset manifests for ontology promotion."""
    manifests: list[dict] = []
    seen_paths: set[Path] = set()

    for relative_path in VISUAL_ASSET_COMPATIBLE_MANIFEST_PATHS:
        manifest_path = (project_dir / relative_path).resolve()
        if manifest_path in seen_paths or not manifest_path.exists():
            continue
        seen_paths.add(manifest_path)
        try:
            raw_manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            continue
        if not isinstance(raw_manifest, dict):
            continue
        assets = raw_manifest.get("assets")
        if not isinstance(assets, list) or not assets:
            continue

        manifests.append({
            "path": relative_path,
            "absolute_path": str(manifest_path),
            "schema_version": raw_manifest.get("schema_version"),
            "project": raw_manifest.get("project"),
            "brand": raw_manifest.get("brand"),
            "generator": raw_manifest.get("generator") or {},
            "source_session": raw_manifest.get("source_session") or {},
            "assets": [asset for asset in assets if isinstance(asset, dict)],
        })

    return manifests


def build_blueprint(
    output_dir: Path,
    brand_profile: dict,
    references: list[ReferenceLink],
    documents: list[DocumentRecord],
) -> dict:
    blueprint_dir = ensure_dir(output_dir / "blueprint")
    concept_counts = _count_concepts(output_dir / "ontology" / "evidence.jsonl")
    source_coverage = _count_source_coverage(output_dir / "ontology" / "evidence.jsonl")
    prioritized_concepts = [
        {"concept_id": concept_id, "count": count}
        for concept_id, count in concept_counts.most_common(8)
    ]
    principle_keywords = brand_profile.get("brand_keywords", [])[:4]
    principles = [
        _principle_from_keyword(keyword)
        for keyword in principle_keywords
    ]

    blueprint = {
        "brand_name": brand_profile.get("brand_name", "Unnamed Brand"),
        "system_name": brand_profile.get("system_name", "Unnamed System"),
        "product_summary": brand_profile.get("product_summary", ""),
        "positioning": {
            "audiences": brand_profile.get("audiences", []),
            "brand_keywords": brand_profile.get("brand_keywords", []),
            "anti_keywords": brand_profile.get("anti_keywords", []),
            "tone_of_voice": brand_profile.get("tone_of_voice", []),
            "platforms": brand_profile.get("platforms", []),
            "accessibility_targets": brand_profile.get("accessibility_targets", []),
        },
        "principles": principles,
        "reference_strategy": {
            "seed_article": references[0].source_article_url if references else None,
            "top_sources_by_concept_coverage": [
                {"source_label": label, "covered_concepts": sorted(list(concepts))}
                for label, concepts in sorted(
                    source_coverage.items(),
                    key=lambda item: (-len(item[1]), item[0]),
                )[:8]
            ],
            "rule": "레퍼런스는 그대로 복제하지 않고, 원칙과 구조만 가져와 브랜드 아이덴티티에 맞게 재구성합니다.",
        },
        "token_strategy": _build_token_strategy(brand_profile, prioritized_concepts),
        "component_strategy": _build_component_strategy(brand_profile, prioritized_concepts),
        "color_reference": brand_profile.get("_resolved_color_reference"),
        "visual_reference": brand_profile.get("_resolved_visual_reference"),
        "visual_reference_issues": brand_profile.get("_visual_reference_issues", []),
        "design_context_pack": brand_profile.get("_design_context_pack"),
        "identity_assets": brand_profile.get("_identity_assets", []),
        "generated_visual_assets": brand_profile.get("_generated_visual_asset_manifests", []),
        "visual_language": (brand_profile.get("_resolved_visual_reference") or {}).get("visual_motifs"),
        "layout_cues": (brand_profile.get("_resolved_visual_reference") or {}).get("layout_cues"),
        "component_style_hints": (brand_profile.get("_resolved_visual_reference") or {}).get("component_style_hints"),
        "candidate_component_archetypes": (brand_profile.get("_resolved_visual_reference") or {}).get("candidate_component_archetypes"),
        "reference_mood_summary": (brand_profile.get("_resolved_visual_reference") or {}).get("reference_mood_summary"),
        "font_system": brand_profile.get("_resolved_font_system"),
        "css_extraction": load_css_extraction(output_dir),
        "governance": {
            "source_of_truth": [
                "brand profile",
                "design tokens",
                "component specs",
                "usage rules",
                "existing product surfaces and task flows"
            ],
            "change_policy": [
                "새 컴포넌트보다 기존 primitive 확장을 우선",
                "예외 케이스는 variant로 흡수 가능한지 먼저 검토",
                "브랜드 키워드와 anti-keyword를 위반하면 추가하지 않음"
            ],
            "implementation_guardrails": [
                "기존 핵심 화면, 진입점, 작업 흐름은 명시적 승인 없이 제거하거나 숨기지 않음",
                "전면 셸 리라이트보다 토큰 -> primitive -> feature surface 순서의 점진적 롤아웃을 우선",
                "새 시각 규칙은 지원 대상 테마와 breakpoint 전체에서 먼저 검증",
                "일반(light) 모드와 dark 모드를 함께 제공하고, light를 기본 :root 또는 앱 기본값으로 둠",
                "모바일 320/360/390/430px에서 horizontal scroll 또는 버튼/CTA 잘림이 있으면 완료로 보지 않음",
                "버튼·CTA·탭·필터칩·툴바 액션은 fixed width/min-width에 의존하지 않고 wrap 또는 stack fallback을 가져야 함",
                "padded container 안에서 width: 100vw를 쓰지 않음 — width: 100%, max-width: 100%, documented full-bleed 패턴을 우선",
                "기존 데이터 밀도와 업무 완료 경로를 유지한 상태에서 시각 품질을 높이는 방향을 우선",
                "기능 위치 변경, 정보 구조 변경, 패널 제거는 별도의 migration plan이 있을 때만 수행",
                "레퍼런스는 형태·밀도·컴포넌트 비례만 흡수하고, 색 조합·폰트 스케일·도메인 IA는 토큰과 제품 온톨로지를 따른다",
                "토큰을 사용하더라도 status/tint/info 역할을 섞어 레퍼런스처럼 보이는 새 팔레트를 만들지 않는다",
                "구현 중 사용자·리뷰어가 반복 가능한 실패 패턴을 지적하면 현재 화면 수정에 그치지 않고 governance/contract/linter로 승격한다",
                "상용 제품형 화면은 피치덱식 히어로/균일 카드벽보다 실제 작업 표면, 데이터 밀도, 상태, 필터, 출처를 첫 화면에 우선 배치한다",
                "데이터·스포츠·운영 UI에서 정확한 수치, 예측, 순위, 투표수는 출처/업데이트 시각/샘플 라벨 없이 확정값처럼 보이게 하지 않는다",
                "생성 이미지와 장식 비주얼은 도메인 맥락을 보조해야 하며 일정, 결과, 표, 필터, 상태 같은 핵심 작업 표면을 압도하지 않는다",
                "Codex image_gen이 실패하거나 실제 사진성이 더 중요해 sourced visual fallback을 사용할 때는 라이선스/저작자/출처/attribution/sha256을 manifest에 기록하고 프로젝트 에셋으로 복사한 뒤 사용한다",
                "유료 stock provider는 구매·구독·프로젝트 라이선스 증빙이 없으면 구현 에셋으로 승격하지 않고, reference-only provider는 형태·밀도·flow 참고로만 사용한다",
                "라이선스 메타데이터가 없는 검색 이미지를 사용하지 않고, 런타임 코드가 원격 검색/CDN URL을 hotlink하지 않는다",
                "아이콘 자리에 이모지(🎨 ✅ 🔥 등)를 넣지 않음 — 리팩토링 중 발견하면 SVG 파일/아이콘 컴포넌트 또는 아이콘 라이브러리로 교체",
                "favicon, 앱 셸 브랜드 마크, 웹 manifest에는 브랜드 특정 앱 아이콘을 사용하고 일반 이니셜 타일을 최종 아이콘으로 남기지 않음",
                "컴포넌트는 component_specs.md의 anatomy/states/token binding을 그대로 따라 완전히 구현",
                "'TODO 컴포넌트', '임시 버튼', '플레이스홀더 카드' 같은 반쪽 구현을 남기지 않음"
            ],
            "ai_synthesis_principles": AI_SYNTHESIS_PRINCIPLES,
            "reference_absorption_scope": REFERENCE_ABSORPTION_SCOPE,
            "color_mode_parity_policy": COLOR_MODE_PARITY_POLICY,
            "responsive_resilience_policy": RESPONSIVE_RESILIENCE_POLICY,
            "icon_refactor_policy": ICON_REFACTOR_POLICY,
            "app_icon_identity_policy": APP_ICON_IDENTITY_POLICY,
            "commercial_product_realism_policy": COMMERCIAL_PRODUCT_REALISM_POLICY,
            "feedback_promotion_policy": REFERENCE_ABSORPTION_SCOPE["promotion_policy"],
        },
        "ontology_targets": prioritized_concepts,
        "benchmark": build_benchmark_context(brand_profile),
    }

    if blueprint["visual_reference"]:
        write_json(blueprint_dir / "visual_reference_report.json", blueprint["visual_reference"])
    if blueprint.get("design_context_pack"):
        write_json(blueprint_dir / "design_context_pack.json", blueprint["design_context_pack"])
    save_benchmark_report(output_dir, brand_profile)
    write_json(blueprint_dir / "design_system_blueprint.json", blueprint)
    generate_system_pack(output_dir, brand_profile, blueprint, references, documents)
    return blueprint


def _count_concepts(evidence_path: Path) -> Counter:
    counts: Counter = Counter()
    if not evidence_path.exists():
        return counts
    for line in evidence_path.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        row = json.loads(line)
        counts[row["concept_id"]] += 1
    return counts


def _count_source_coverage(evidence_path: Path) -> dict[str, set[str]]:
    coverage: dict[str, set[str]] = defaultdict(set)
    if not evidence_path.exists():
        return coverage
    for line in evidence_path.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        row = json.loads(line)
        coverage[row["source_label"]].add(row["concept_id"])
    return coverage


def _principle_from_keyword(keyword: str) -> dict:
    normalized = keyword.lower().strip()
    if normalized in KEYWORD_PRINCIPLES:
        principle = KEYWORD_PRINCIPLES[normalized]
        return {
            "keyword": keyword,
            "name": principle["name"],
            "rule": principle["rule"],
            "implications": principle["implications"],
        }
    return {
        "keyword": keyword,
        "name": keyword.title(),
        "rule": f"`{keyword}`를 시각적 선택과 인터랙션 선택의 기본 기준으로 삼습니다.",
        "implications": [
            f"{keyword}와 충돌하는 컴포넌트 변형은 만들지 않기",
            f"{keyword}를 토큰 네이밍과 문서화 기준에 반영하기",
        ],
    }


def _build_token_strategy(brand_profile: dict, prioritized_concepts: list[dict]) -> dict:
    visual_keywords = brand_profile.get("visual_keywords", [])
    interaction_keywords = brand_profile.get("interaction_keywords", [])
    concept_ids = {item["concept_id"] for item in prioritized_concepts}

    return {
        "color": {
            "goal": "브랜드 개성을 드러내되 UI 전체를 지배하지 않는 팔레트",
            "rules": [
                "brand color는 1개의 primary accent를 중심으로 설계",
                "semantic color는 brand color와 분리해서 유지",
                "contrast ratio는 접근성 목표를 우선",
                "지원하는 theme 모드마다 semantic surface/text/border 쌍을 함께 정의",
                "하드코딩 색상보다 semantic token 적용을 우선"
            ],
        },
        "typography": {
            "goal": "정보 구조와 브랜드 톤을 동시에 전달하는 타입 시스템",
            "rules": [
                "heading/body/caption 역할을 토큰으로 고정",
                "텍스트 길이가 긴 화면에서 리듬이 무너지지 않도록 line-height를 계층별로 정의",
                "편집형 제품이면 typography scale을 먼저 확정"
            ],
            "signal": "typography" in concept_ids or "editorial" in [kw.lower() for kw in brand_profile.get("brand_keywords", [])],
        },
        "spacing": {
            "goal": "밀도와 여백의 성격을 제품 전반에서 일관되게 유지",
            "rules": [
                "4pt 또는 8pt 기반 scale을 정하고 예외 사용을 제한",
                "컴포넌트 내부 spacing과 레이아웃 spacing을 분리",
            ],
        },
        "motion": {
            "goal": "상태 변화를 설명하는 수준의 모션만 허용",
            "rules": [
                "transition duration/easing을 토큰화",
                "주의 환기용 모션과 구조적 모션을 구분"
            ],
            "brand_signal": interaction_keywords,
        },
        "visual_keywords": visual_keywords,
    }


def _build_component_strategy(brand_profile: dict, prioritized_concepts: list[dict]) -> dict:
    primitives = brand_profile.get("product_primitives", [])
    concept_ids = {item["concept_id"] for item in prioritized_concepts}
    required_families = ["button", "input", "navigation", "feedback", "overlay"]
    if "data tables" in [primitive.lower() for primitive in primitives]:
        required_families.append("data-display")
    if "rich text editor" in [primitive.lower() for primitive in primitives]:
        required_families.append("editorial")

    return {
        "product_primitives": primitives,
        "required_component_families": required_families,
        "rules": [
            "primitive 단위로 책임을 먼저 정의하고 컴포넌트는 그 위에 매핑",
            "variant proliferation을 막기 위해 상태와 강조 레벨을 먼저 표준화",
            "브랜드 표현은 surface, emphasis, typography에서 주고 구조는 안정적으로 유지",
            "기존 기능 진입점은 유지한 채 내부 구현과 시각 언어부터 교체",
            "전체 셸을 한 번에 다시 그리기보다 feature surface 단위로 순차 적용"
        ],
        "concept_alignment": sorted(concept_ids),
    }
