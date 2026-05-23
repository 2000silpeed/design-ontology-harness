from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

from PIL import Image, ImageDraw

from design_ontology_harness.aesthetic_loop import DEFAULT_METRICS
from design_ontology_harness.screenshot_aesthetic import score_screenshots
from design_ontology_harness.utils import write_json


REPO_ROOT = Path(__file__).resolve().parent.parent


def _make_ui_screenshot(path: Path, *, size: tuple[int, int] = (640, 420)) -> None:
    image = Image.new("RGB", size, "#F5F8F8")
    draw = ImageDraw.Draw(image)
    width, height = size
    draw.rectangle((0, 0, width, 56), fill="#FFFFFF", outline="#D7E2E5")
    draw.rectangle((16, 78, width * 0.64, height - 72), fill="#EEF6F7", outline="#C8DDE2")
    draw.rectangle((width * 0.68, 78, width - 20, height - 72), fill="#FFFFFF", outline="#D7E2E5")
    draw.rounded_rectangle((32, 96, 150, 156), radius=24, fill="#B8DDE3", outline="#5AA3AD")
    draw.rounded_rectangle((210, 116, 390, 168), radius=24, fill="#F4E5CF", outline="#CFA56F")
    draw.line((48, height - 126, width * 0.62, height - 188), fill="#5AA3AD", width=6)
    for index in range(4):
        y = 96 + index * 38
        draw.rounded_rectangle((width * 0.70, y, width - 42, y + 24), radius=4, fill="#EEF6F7", outline="#C8DDE2")
    for index, color in enumerate(["#7A5C3E", "#A58362", "#4D6F55"]):
        x = int(width * 0.70) + index * 52
        draw.rectangle((x, height - 144, x + 42, height - 94), fill=color)
    image.save(path)


def test_score_screenshots_generates_full_candidate_metrics(tmp_path: Path):
    screenshot = tmp_path / "screen.png"
    _make_ui_screenshot(screenshot)

    candidate = score_screenshots(
        [screenshot],
        brand_profile={
            "brand_name": "Alley Sense",
            "brand_keywords": ["quiet", "sensory", "trustworthy"],
            "product_primitives": ["map pin layer", "place detail sheet"],
        },
    )

    assert set(DEFAULT_METRICS) <= set(candidate["metrics"])
    assert all(1 <= value <= 10 for value in candidate["metrics"].values())
    assert candidate["automated_feature_report"]["screenshots"][0]["width"] == 640
    assert candidate["automated_feature_report"]["aggregate"]["count"] == 1


def test_score_screenshots_includes_brand_contract_metrics(tmp_path: Path):
    screenshot = tmp_path / "screen.png"
    _make_ui_screenshot(screenshot)

    candidate = score_screenshots(
        [screenshot],
        brand_profile={
            "brand_name": "Alley Sense",
            "brand_keywords": ["quiet"],
            "anti_keywords": ["generic-map"],
            "product_primitives": ["map pin layer"],
            "accessibility_targets": ["WCAG 2.2 AA"],
        },
    )

    metric_ids = set(candidate["metrics"])

    assert any(metric_id.startswith("brand_keyword:quiet") for metric_id in metric_ids)
    assert any(metric_id.startswith("anti_keyword:generic-map") for metric_id in metric_ids)
    assert any(metric_id.startswith("product_primitive:map-pin-layer") for metric_id in metric_ids)
    assert any(metric_id.startswith("accessibility_target:wcag-2-2-aa") for metric_id in metric_ids)


def test_cli_score_screenshot_writes_candidate_and_loop_report(tmp_path: Path):
    screenshot = tmp_path / "screen.png"
    candidate_path = tmp_path / "candidate.json"
    report_path = tmp_path / "report.json"
    brand_profile = tmp_path / "brand_profile.json"
    _make_ui_screenshot(screenshot)
    write_json(
        brand_profile,
        {
            "brand_name": "Alley Sense",
            "system_name": "Alley Sense System",
            "product_summary": "서울 골목 장소 추천 지도",
            "brand_keywords": ["quiet", "sensory", "trustworthy"],
            "product_primitives": ["map pin layer", "place detail sheet"],
        },
    )

    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "design_ontology_harness.cli",
            "score-screenshot",
            "--screenshot",
            str(screenshot),
            "--brand-profile",
            str(brand_profile),
            "--output",
            str(candidate_path),
            "--run-loop",
            "--threshold",
            "0.50",
            "--report-output",
            str(report_path),
        ],
        cwd=REPO_ROOT,
        text=True,
        capture_output=True,
        check=False,
    )

    assert result.returncode == 0
    assert candidate_path.exists()
    assert report_path.exists()
    assert "Screenshot aesthetic candidate generated" in result.stdout
    assert json.loads(report_path.read_text(encoding="utf-8"))["ready_to_execute"]
