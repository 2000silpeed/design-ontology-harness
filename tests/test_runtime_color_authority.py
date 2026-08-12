import json
import re
from pathlib import Path

import pytest

from design_ontology_harness.semantic_color_markdown import (
    SemanticColorMarkdownError,
    extract_runtime_color_policy,
    load_runtime_color_policy,
    payload_sha256,
    runtime_role_values,
)
from design_ontology_harness.token_emitter import emit_project_tokens


REPO_ROOT = Path(__file__).resolve().parents[1]
WORLD_CUP_PROJECT = REPO_ROOT / "projects" / "world-cup-hub"
HEX_DECLARATION_RE = re.compile(r"(?m)^\s*(--[a-zA-Z0-9-]+)\s*:\s*(#[0-9A-Fa-f]{6});")
COLOR_DECLARATION_RE = re.compile(
    r"(?m)^\s*--ds-color-([a-zA-Z0-9-]+)\s*:\s*(#[0-9A-Fa-f]{6});"
)


def _selector_color_values(css: str, selector: str) -> dict[str, str]:
    match = re.search(rf"{re.escape(selector)}\s*\{{(?P<body>.*?)\n\}}", css, re.DOTALL)
    assert match is not None, f"missing selector: {selector}"
    return {
        role: value.upper()
        for role, value in COLOR_DECLARATION_RE.findall(match.group("body"))
    }


def _relative_luminance(value: str) -> float:
    channels = [int(value[index : index + 2], 16) / 255 for index in (1, 3, 5)]
    linear = [
        channel / 12.92
        if channel <= 0.04045
        else ((channel + 0.055) / 1.055) ** 2.4
        for channel in channels
    ]
    return 0.2126 * linear[0] + 0.7152 * linear[1] + 0.0722 * linear[2]


def _contrast_ratio(foreground: str, background: str) -> float:
    lighter, darker = sorted(
        (_relative_luminance(foreground), _relative_luminance(background)),
        reverse=True,
    )
    return (lighter + 0.05) / (darker + 0.05)


def _write_emitter_fixture(project: Path) -> None:
    blueprint_dir = project / "build" / "system" / "blueprint"
    blueprint_dir.mkdir(parents=True)
    (blueprint_dir / "design_system_blueprint.json").write_text(
        json.dumps(
            {
                "color_reference": {
                    "expanded_palette": {
                        "semantic_roles": {
                            "brand_primary": {"hex": "#0F4C81"},
                            "brand_accent": {"hex": "#50C878"},
                            "info": {"hex": "#000080"},
                            "success": {"hex": "#27503D"},
                            "warning": {"hex": "#B87333"},
                            "danger": {"hex": "#4A0404"},
                        }
                    }
                }
            }
        ),
        encoding="utf-8",
    )
    (blueprint_dir / "token_schema.json").write_text(
        json.dumps(
            {
                "categories": {
                    "color": {
                        "reference_palette": {
                            "active_palette": {
                                "roles": {
                                    "primary": {"hex": "#0F4C81"},
                                    "accent": {"hex": "#50C878"},
                                }
                            }
                        }
                    }
                }
            }
        ),
        encoding="utf-8",
    )


def test_emitter_uses_typed_policy_for_complete_light_and_dark_roles(tmp_path) -> None:
    project = tmp_path / "world-cup-token-fixture"
    _write_emitter_fixture(project)

    css = emit_project_tokens(project).read_text(encoding="utf-8")
    light = _selector_color_values(css, ":root")
    dark = _selector_color_values(css, 'html[data-theme="dark"]')
    policy = load_runtime_color_policy()
    runtime_values = runtime_role_values()

    assert f"sha256={payload_sha256(policy)}" in css
    assert set(runtime_values) <= set(light)
    assert set(runtime_values) <= set(dark)
    # The policy owns the role set and the inverse ink. Everything else may be
    # chosen from the project palette, and neutrals with no palette candidate
    # are derived from the brand hue rather than dropped to one shared grey —
    # they still have to clear the contrast floors asserted below.
    assert light["ink-inverse"] == runtime_values["ink-inverse"]
    assert light["ink-muted"] != runtime_values["ink-muted"], (
        "neutrals must not fall back to the stock grey when a brand hue exists"
    )
    assert light["primary"] == "#0F4C81"
    assert light["brand-accent"] == "#50C878"
    assert light["accent"] != light["brand-accent"]
    assert dark["canvas"] != light["canvas"]

    for mode in (light, dark):
        for foreground, background in (
            ("ink", "canvas"),
            ("ink-muted", "surface"),
            ("ink-subtle", "surface"),
        ):
            assert _contrast_ratio(mode[foreground], mode[background]) >= 4.5

    light_contrast_floor = policy["light_contrast_floor"]
    for foreground in light_contrast_floor["chromatic_roles"]:
        for background in light_contrast_floor["background_roles"]:
            assert _contrast_ratio(light[foreground], light[background]) >= 4.5

    contrast_floor = policy["dark_derivation"]["contrast_floor"]
    for foreground in contrast_floor["chromatic_roles"]:
        for background in contrast_floor["background_roles"]:
            assert _contrast_ratio(dark[foreground], dark[background]) >= 4.5

    # WCAG 1.4.11 — 컨트롤 경계 역할은 두 모드 모두에서 3:1을 넘어야 한다.
    for mode, floor in (
        (light, policy["non_text_contrast_floor"]),
        (dark, policy["dark_derivation"]["non_text_contrast_floor"]),
    ):
        for boundary in floor["adjusted_roles"]:
            for background in floor["background_roles"]:
                assert _contrast_ratio(mode[boundary], mode[background]) >= 3.0

    # 장식용 divider는 하한 대상이 아니다. border까지 끌어올리면 모든 구분선이
    # 진해져서 시각 체계가 무너지고, WCAG가 요구하는 범위도 아니다.
    assert "border" not in policy["non_text_contrast_floor"]["adjusted_roles"]
    assert _contrast_ratio(light["border"], light["surface"]) < 3.0


def test_world_cup_runtime_theme_has_no_local_application_hex() -> None:
    theme = (WORLD_CUP_PROJECT / "design-system" / "runtime-theme.css").read_text(
        encoding="utf-8"
    )
    declarations = HEX_DECLARATION_RE.findall(theme)

    assert declarations
    assert all(name.startswith("--identity-") for name, _ in declarations)
    assert "--ds-color-primary:" not in theme
    assert "--ds-color-accent:" not in theme
    assert "--ds-color-canvas:" not in theme
    assert "--ds-color-ink:" not in theme
    assert "--ds-color-body-start: var(--ds-color-canvas);" in theme
    assert "--ds-color-safe-ink: var(--ds-color-success);" in theme
    assert "--team-kor: var(--identity-team-kor);" in theme
    assert "--ds-color-flag-a: var(--identity-flag-red);" in theme


def test_world_cup_identity_exception_is_scoped_and_redundant() -> None:
    profile = json.loads((WORLD_CUP_PROJECT / "brand_profile.json").read_text(encoding="utf-8"))
    color_reference = profile["color_reference"]
    authority = color_reference["runtime_authority"]
    identity = color_reference["identity_color_exception"]

    assert authority["mode"] == "semantic-os-markdown"
    assert authority["local_ui_hex"] == "forbidden"
    assert identity["namespace"] == "--identity-*"
    assert identity["status_semantics"] == "forbidden"
    assert "team code" in identity["redundant_cue"]


@pytest.mark.parametrize(
    "floor_path",
    [
        ("dark_derivation", "contrast_floor"),
        ("light_contrast_floor",),
        ("dark_derivation", "non_text_contrast_floor"),
        ("non_text_contrast_floor",),
    ],
)
def test_runtime_policy_rejects_missing_contrast_floor(
    floor_path: tuple[str, ...],
) -> None:
    policy = load_runtime_color_policy()
    owner = policy
    for key in floor_path[:-1]:
        owner = owner[key]
    owner.pop(floor_path[-1])
    digest = payload_sha256(policy)
    text = "\n".join(
        [
            f"<!-- design-ontology-runtime-color-policy:begin sha256={digest} -->",
            "```design-ontology-runtime-color-policy+json",
            json.dumps(policy, ensure_ascii=False, indent=2, sort_keys=True),
            "```",
            "<!-- design-ontology-runtime-color-policy:end -->",
        ]
    )

    with pytest.raises(SemanticColorMarkdownError, match="WCAG contrast floor"):
        extract_runtime_color_policy(text)
