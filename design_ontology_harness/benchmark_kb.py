"""Benchmark KB — 35개 실서비스 디자인 시스템 레퍼런스.

Stripe, Vercel, Linear 등 검증된 디자인 시스템의 핵심 특성을 정리한
벤치마크 데이터. 합성 품질 비교/검증에 사용.
"""

from __future__ import annotations

from pathlib import Path

from .utils import ensure_dir, write_json

BENCHMARK_SYSTEMS: list[dict] = [
    {
        "id": "stripe",
        "name": "Stripe",
        "url": "https://stripe.com",
        "category": "fintech",
        "keywords": ["trustworthy", "precise", "calm"],
        "token_traits": ["8pt grid", "4-layer token", "semantic color"],
        "typography": {"heading": "Inter Display", "body": "Inter", "mono": "Source Code Pro"},
        "color_strategy": "neutral-dominant with purple accent",
        "component_count_range": "80-120",
        "notable": ["dashboard-first", "data-dense UI", "global design language"],
    },
    {
        "id": "vercel",
        "name": "Vercel / Geist",
        "url": "https://vercel.com/geist",
        "category": "devtool",
        "keywords": ["minimal", "precise", "fast"],
        "token_traits": ["CSS custom properties", "dark-first", "monochrome base"],
        "typography": {"heading": "Geist", "body": "Geist", "mono": "Geist Mono"},
        "color_strategy": "monochrome with blue accent",
        "component_count_range": "60-80",
        "notable": ["developer-facing", "high contrast dark mode", "minimal decoration"],
    },
    {
        "id": "linear",
        "name": "Linear",
        "url": "https://linear.app",
        "category": "productivity",
        "keywords": ["fast", "calm", "precise"],
        "token_traits": ["tight spacing", "gradient accent", "semantic naming"],
        "typography": {"heading": "Inter", "body": "Inter", "mono": "JetBrains Mono"},
        "color_strategy": "dark with gradient accents",
        "component_count_range": "50-70",
        "notable": ["keyboard-first", "command palette", "speed obsession"],
    },
    {
        "id": "github-primer",
        "name": "GitHub Primer",
        "url": "https://primer.style",
        "category": "devtool",
        "keywords": ["trustworthy", "accessible", "systematic"],
        "token_traits": ["design token JSON", "theme-aware", "color modes"],
        "typography": {"heading": "Mona Sans", "body": "Mona Sans", "mono": "Monaspace"},
        "color_strategy": "semantic color scales with theme modes",
        "component_count_range": "100-150",
        "notable": ["open source", "Figma/code parity", "accessibility-first"],
    },
    {
        "id": "shopify-polaris",
        "name": "Shopify Polaris",
        "url": "https://polaris.shopify.com",
        "category": "commerce",
        "keywords": ["trustworthy", "editorial", "inclusive"],
        "token_traits": ["Figma tokens", "semantic layers", "responsive scale"],
        "typography": {"heading": "Inter", "body": "Inter", "mono": "IBM Plex Mono"},
        "color_strategy": "green accent with warm neutrals",
        "component_count_range": "70-100",
        "notable": ["merchant-focused", "content guidelines", "pattern library"],
    },
    {
        "id": "atlassian",
        "name": "Atlassian Design System",
        "url": "https://atlassian.design",
        "category": "productivity",
        "keywords": ["trustworthy", "bold", "accessible"],
        "token_traits": ["design tokens", "elevation system", "spacing scale"],
        "typography": {"heading": "Charlie Display", "body": "Inter", "mono": "Source Code Pro"},
        "color_strategy": "blue accent with semantic states",
        "component_count_range": "80-120",
        "notable": ["enterprise-scale", "accessibility guidelines", "brand evolution"],
    },
    {
        "id": "figma",
        "name": "Figma UI2",
        "url": "https://figma.com",
        "category": "creative-tool",
        "keywords": ["precise", "playful", "accessible"],
        "token_traits": ["variables system", "color modes", "responsive"],
        "typography": {"heading": "Inter", "body": "Inter", "mono": "Roboto Mono"},
        "color_strategy": "dark UI with colorful accents",
        "component_count_range": "50-80",
        "notable": ["design tool for designers", "real-time collaboration UI"],
    },
    {
        "id": "notion",
        "name": "Notion",
        "url": "https://notion.so",
        "category": "productivity",
        "keywords": ["calm", "editorial", "flexible"],
        "token_traits": ["content-first spacing", "block model", "simple token set"],
        "typography": {"heading": "Inter", "body": "Inter", "mono": "SFMono"},
        "color_strategy": "minimal with soft pastels",
        "component_count_range": "40-60",
        "notable": ["block-based editor", "template system", "custom databases"],
    },
    {
        "id": "slack",
        "name": "Slack",
        "url": "https://slack.com",
        "category": "communication",
        "keywords": ["friendly", "accessible", "trustworthy"],
        "token_traits": ["semantic color", "density modes", "platform-specific"],
        "typography": {"heading": "Slack Lato", "body": "Lato", "mono": "Menlo"},
        "color_strategy": "aubergine brand with semantic states",
        "component_count_range": "60-90",
        "notable": ["real-time messaging", "emoji-rich", "workspace theming"],
    },
    {
        "id": "material-design",
        "name": "Google Material Design 3",
        "url": "https://m3.material.io",
        "category": "platform",
        "keywords": ["accessible", "systematic", "expressive"],
        "token_traits": ["dynamic color", "motion system", "shape system"],
        "typography": {"heading": "Roboto", "body": "Roboto", "mono": "Roboto Mono"},
        "color_strategy": "dynamic color from seed with tonal palettes",
        "component_count_range": "40-60",
        "notable": ["cross-platform", "Material You personalization", "comprehensive guidelines"],
    },
    {
        "id": "apple-hig",
        "name": "Apple Human Interface Guidelines",
        "url": "https://developer.apple.com/design",
        "category": "platform",
        "keywords": ["precise", "trustworthy", "refined"],
        "token_traits": ["system colors", "SF Symbols", "dynamic type"],
        "typography": {"heading": "SF Pro Display", "body": "SF Pro Text", "mono": "SF Mono"},
        "color_strategy": "system semantic colors with vibrancy",
        "component_count_range": "50-80",
        "notable": ["platform-native", "accessibility excellence", "haptic integration"],
    },
    {
        "id": "spotify",
        "name": "Spotify Encore",
        "url": "https://spotify.design",
        "category": "entertainment",
        "keywords": ["bold", "expressive", "editorial"],
        "token_traits": ["responsive spacing", "dark-first", "gradient system"],
        "typography": {"heading": "Spotify Mix", "body": "Spotify Mix", "mono": "monospace"},
        "color_strategy": "green accent on dark with album art colors",
        "component_count_range": "50-70",
        "notable": ["music-driven", "album art integration", "bold typography"],
    },
    {
        "id": "airbnb",
        "name": "Airbnb DLS",
        "url": "https://airbnb.design",
        "category": "marketplace",
        "keywords": ["warm", "trustworthy", "inclusive"],
        "token_traits": ["spacing units", "animation tokens", "color palette"],
        "typography": {"heading": "Cereal", "body": "Cereal", "mono": "monospace"},
        "color_strategy": "rausch red accent with warm neutrals",
        "component_count_range": "60-80",
        "notable": ["photo-centric", "trust & safety patterns", "global localization"],
    },
    {
        "id": "uber",
        "name": "Uber Base Web",
        "url": "https://baseweb.design",
        "category": "transport",
        "keywords": ["precise", "accessible", "bold"],
        "token_traits": ["theme provider", "overrides pattern", "responsive"],
        "typography": {"heading": "Uber Move", "body": "Uber Move", "mono": "Uber Move Mono"},
        "color_strategy": "black primary with minimal accent",
        "component_count_range": "50-70",
        "notable": ["open source", "override-friendly", "map integration patterns"],
    },
    {
        "id": "twilio-paste",
        "name": "Twilio Paste",
        "url": "https://paste.twilio.design",
        "category": "devtool",
        "keywords": ["accessible", "trustworthy", "systematic"],
        "token_traits": ["design tokens", "theme-first", "a11y primitives"],
        "typography": {"heading": "TwilioSans", "body": "Inter", "mono": "Fira Code"},
        "color_strategy": "red accent with comprehensive semantic scale",
        "component_count_range": "80-120",
        "notable": ["accessibility champion", "inclusive design", "developer-focused"],
    },
    {
        "id": "ibm-carbon",
        "name": "IBM Carbon",
        "url": "https://carbondesignsystem.com",
        "category": "enterprise",
        "keywords": ["trustworthy", "precise", "systematic"],
        "token_traits": ["spacing scale", "type scale", "icon system"],
        "typography": {"heading": "IBM Plex Sans", "body": "IBM Plex Sans", "mono": "IBM Plex Mono"},
        "color_strategy": "blue accent with gray palette and semantic states",
        "component_count_range": "80-100",
        "notable": ["enterprise-grade", "data visualization", "multi-framework"],
    },
    {
        "id": "ant-design",
        "name": "Ant Design",
        "url": "https://ant.design",
        "category": "enterprise",
        "keywords": ["systematic", "precise", "trustworthy"],
        "token_traits": ["design token", "CSS-in-JS", "theme customization"],
        "typography": {"heading": "PingFang SC", "body": "PingFang SC", "mono": "SFMono"},
        "color_strategy": "blue accent with functional color system",
        "component_count_range": "60-80",
        "notable": ["CJK-optimized", "enterprise data patterns", "locale support"],
    },
    {
        "id": "chakra",
        "name": "Chakra UI",
        "url": "https://chakra-ui.com",
        "category": "component-library",
        "keywords": ["accessible", "flexible", "composable"],
        "token_traits": ["theme tokens", "responsive styles", "color mode"],
        "typography": {"heading": "Inter", "body": "Inter", "mono": "Menlo"},
        "color_strategy": "teal accent with comprehensive color scales",
        "component_count_range": "40-60",
        "notable": ["composable primitives", "accessibility-first", "style props"],
    },
    {
        "id": "radix",
        "name": "Radix UI + Themes",
        "url": "https://radix-ui.com",
        "category": "component-library",
        "keywords": ["accessible", "composable", "minimal"],
        "token_traits": ["CSS variables", "color scales", "responsive props"],
        "typography": {"heading": "Inter", "body": "Inter", "mono": "monospace"},
        "color_strategy": "12-step color scales with automatic contrast",
        "component_count_range": "30-50",
        "notable": ["headless primitives", "automatic accessibility", "unstyled + themed"],
    },
    {
        "id": "discord",
        "name": "Discord",
        "url": "https://discord.com",
        "category": "communication",
        "keywords": ["playful", "bold", "fast"],
        "token_traits": ["dark-first", "custom properties", "density modes"],
        "typography": {"heading": "gg sans", "body": "gg sans", "mono": "Consolas"},
        "color_strategy": "blurple accent on dark with vibrant status colors",
        "component_count_range": "50-70",
        "notable": ["gaming community", "real-time voice/video", "custom emoji system"],
    },
    {
        "id": "tailwind",
        "name": "Tailwind UI / Catalyst",
        "url": "https://tailwindui.com",
        "category": "component-library",
        "keywords": ["minimal", "flexible", "composable"],
        "token_traits": ["utility-first", "design token config", "responsive"],
        "typography": {"heading": "Inter", "body": "Inter", "mono": "monospace"},
        "color_strategy": "configurable palette with semantic intent",
        "component_count_range": "50-80",
        "notable": ["utility-first CSS", "headless UI", "copy-paste components"],
    },
    {
        "id": "adobe-spectrum",
        "name": "Adobe Spectrum",
        "url": "https://spectrum.adobe.com",
        "category": "creative-tool",
        "keywords": ["precise", "accessible", "trustworthy"],
        "token_traits": ["design tokens", "DNA system", "express/spectrum split"],
        "typography": {"heading": "Adobe Clean", "body": "Adobe Clean", "mono": "Source Code Pro"},
        "color_strategy": "gray spectrum with blue accent and express variants",
        "component_count_range": "70-100",
        "notable": ["multi-product", "spectrum/express duality", "cross-platform"],
    },
    {
        "id": "microsoft-fluent",
        "name": "Microsoft Fluent 2",
        "url": "https://fluent2.microsoft.design",
        "category": "platform",
        "keywords": ["accessible", "systematic", "trustworthy"],
        "token_traits": ["design tokens", "alias system", "global/alias/component"],
        "typography": {"heading": "Segoe UI Variable", "body": "Segoe UI Variable", "mono": "Cascadia Code"},
        "color_strategy": "brand blue with tint/shade system and high contrast mode",
        "component_count_range": "60-90",
        "notable": ["cross-platform", "accessibility modes", "Teams/Office integration"],
    },
    {
        "id": "hashicorp-helios",
        "name": "HashiCorp Helios",
        "url": "https://helios.hashicorp.design",
        "category": "devtool",
        "keywords": ["trustworthy", "systematic", "precise"],
        "token_traits": ["design tokens", "semantic color", "icon system"],
        "typography": {"heading": "Gilroy", "body": "Metro", "mono": "Fira Code"},
        "color_strategy": "multi-product brand colors with shared semantic layer",
        "component_count_range": "50-70",
        "notable": ["multi-product family", "developer documentation focus"],
    },
    {
        "id": "gitlab-pajamas",
        "name": "GitLab Pajamas",
        "url": "https://design.gitlab.com",
        "category": "devtool",
        "keywords": ["accessible", "trustworthy", "systematic"],
        "token_traits": ["design tokens", "semantic color", "responsive"],
        "typography": {"heading": "Inter", "body": "Inter", "mono": "JetBrains Mono"},
        "color_strategy": "purple/orange brand with semantic layer",
        "component_count_range": "60-80",
        "notable": ["open source DS", "contribution guidelines", "accessibility focus"],
    },
    {
        "id": "wise",
        "name": "Wise (TransferWise) Neptune",
        "url": "https://wise.com",
        "category": "fintech",
        "keywords": ["trustworthy", "calm", "bold"],
        "token_traits": ["design tokens", "responsive spacing", "motion system"],
        "typography": {"heading": "Wise Sans", "body": "Wise Sans", "mono": "monospace"},
        "color_strategy": "green accent with bright illustrations",
        "component_count_range": "50-70",
        "notable": ["trust-first", "currency display patterns", "global localization"],
    },
    {
        "id": "revolut",
        "name": "Revolut",
        "url": "https://revolut.com",
        "category": "fintech",
        "keywords": ["bold", "fast", "precise"],
        "token_traits": ["dark-first", "gradient system", "motion tokens"],
        "typography": {"heading": "Basier Circle", "body": "Basier Circle", "mono": "monospace"},
        "color_strategy": "dark base with vibrant gradients",
        "component_count_range": "40-60",
        "notable": ["fintech premium feel", "card-centric", "super app patterns"],
    },
    {
        "id": "resend",
        "name": "Resend",
        "url": "https://resend.com",
        "category": "devtool",
        "keywords": ["minimal", "precise", "fast"],
        "token_traits": ["CSS variables", "dark-first", "monochrome"],
        "typography": {"heading": "Inter", "body": "Inter", "mono": "Berkeley Mono"},
        "color_strategy": "monochrome with minimal accent",
        "component_count_range": "20-30",
        "notable": ["developer-focused", "email-centric", "minimal UI"],
    },
    {
        "id": "cal-com",
        "name": "Cal.com",
        "url": "https://cal.com",
        "category": "productivity",
        "keywords": ["calm", "trustworthy", "accessible"],
        "token_traits": ["CSS variables", "theme system", "responsive"],
        "typography": {"heading": "Cal Sans", "body": "Inter", "mono": "monospace"},
        "color_strategy": "neutral base with scheduling-specific semantic colors",
        "component_count_range": "40-60",
        "notable": ["open source", "scheduling patterns", "embed-friendly"],
    },
    {
        "id": "supabase",
        "name": "Supabase",
        "url": "https://supabase.com",
        "category": "devtool",
        "keywords": ["bold", "fast", "accessible"],
        "token_traits": ["CSS variables", "dark-first", "responsive"],
        "typography": {"heading": "Inter", "body": "Inter", "mono": "Source Code Pro"},
        "color_strategy": "green accent on dark with code-centric palette",
        "component_count_range": "40-60",
        "notable": ["dashboard-heavy", "SQL editor patterns", "open source"],
    },
    {
        "id": "planetscale",
        "name": "PlanetScale",
        "url": "https://planetscale.com",
        "category": "devtool",
        "keywords": ["precise", "fast", "bold"],
        "token_traits": ["CSS variables", "dark mode", "monochrome base"],
        "typography": {"heading": "Inter", "body": "Inter", "mono": "JetBrains Mono"},
        "color_strategy": "orange accent on monochrome base",
        "component_count_range": "30-50",
        "notable": ["database dashboard", "schema visualization", "branching UX"],
    },
    {
        "id": "arc-browser",
        "name": "Arc Browser (The Browser Company)",
        "url": "https://arc.net",
        "category": "browser",
        "keywords": ["playful", "bold", "expressive"],
        "token_traits": ["user-chosen palette", "sidebar-first", "vibrancy"],
        "typography": {"heading": "SF Pro", "body": "SF Pro", "mono": "SF Mono"},
        "color_strategy": "user-customizable tint with gradient system",
        "component_count_range": "30-50",
        "notable": ["sidebar navigation", "space concept", "user personalization"],
    },
    {
        "id": "raycast",
        "name": "Raycast",
        "url": "https://raycast.com",
        "category": "productivity",
        "keywords": ["fast", "precise", "minimal"],
        "token_traits": ["dark-first", "command-driven", "icon system"],
        "typography": {"heading": "Inter", "body": "Inter", "mono": "JetBrains Mono"},
        "color_strategy": "dark base with extension-scoped colors",
        "component_count_range": "30-40",
        "notable": ["launcher-first", "keyboard-driven", "extension ecosystem"],
    },
    {
        "id": "lemon-squeezy",
        "name": "Lemon Squeezy",
        "url": "https://lemonsqueezy.com",
        "category": "commerce",
        "keywords": ["playful", "warm", "bold"],
        "token_traits": ["bright palette", "rounded shapes", "animation-rich"],
        "typography": {"heading": "General Sans", "body": "General Sans", "mono": "monospace"},
        "color_strategy": "yellow/lemon accent with warm gradients",
        "component_count_range": "30-50",
        "notable": ["indie creator focus", "checkout patterns", "playful brand"],
    },
    {
        "id": "toss",
        "name": "Toss (비바리퍼블리카)",
        "url": "https://toss.im",
        "category": "fintech",
        "keywords": ["calm", "trustworthy", "precise"],
        "token_traits": ["spacing system", "motion system", "semantic color"],
        "typography": {"heading": "Toss Product Sans", "body": "Toss Product Sans", "mono": "monospace"},
        "color_strategy": "blue accent with conservative semantic palette",
        "component_count_range": "60-80",
        "notable": ["Korean fintech", "super app patterns", "trust-first design", "motion excellence"],
    },
]


def get_benchmark_systems() -> list[dict]:
    return BENCHMARK_SYSTEMS


def get_benchmark_by_keywords(keywords: list[str]) -> list[dict]:
    normalized = [kw.lower() for kw in keywords]
    scored: list[tuple[int, dict]] = []
    for system in BENCHMARK_SYSTEMS:
        score = sum(1 for kw in system["keywords"] if kw.lower() in normalized)
        if score > 0:
            scored.append((score, system))
    scored.sort(key=lambda x: -x[0])
    return [system for _, system in scored]


def get_benchmark_by_category(category: str) -> list[dict]:
    return [s for s in BENCHMARK_SYSTEMS if s["category"] == category.lower()]


def build_benchmark_context(brand_profile: dict) -> dict:
    keywords = brand_profile.get("brand_keywords", [])
    matched = get_benchmark_by_keywords(keywords)
    top_matches = matched[:5]
    all_keywords_used = set()
    for system in BENCHMARK_SYSTEMS:
        all_keywords_used.update(system["keywords"])

    typography_patterns: dict[str, int] = {}
    color_strategies: list[str] = []
    for system in top_matches:
        typo = system.get("typography", {})
        body_font = typo.get("body", "")
        if body_font:
            typography_patterns[body_font] = typography_patterns.get(body_font, 0) + 1
        color_strategies.append(system["color_strategy"])

    return {
        "matched_systems": [
            {
                "id": s["id"],
                "name": s["name"],
                "category": s["category"],
                "keywords": s["keywords"],
                "color_strategy": s["color_strategy"],
                "notable": s["notable"],
            }
            for s in top_matches
        ],
        "total_benchmark_count": len(BENCHMARK_SYSTEMS),
        "common_typography_in_matches": dict(sorted(
            typography_patterns.items(), key=lambda x: -x[1]
        )),
        "color_strategy_patterns": color_strategies,
        "industry_keywords": sorted(all_keywords_used),
    }


def save_benchmark_report(output_dir: Path, brand_profile: dict) -> dict:
    context = build_benchmark_context(brand_profile)
    out = ensure_dir(output_dir / "benchmark")
    write_json(out / "benchmark_context.json", context)
    write_json(out / "all_systems.json", {"systems": BENCHMARK_SYSTEMS, "count": len(BENCHMARK_SYSTEMS)})
    return context
