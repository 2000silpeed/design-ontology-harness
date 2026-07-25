from __future__ import annotations

import subprocess
import sys
from pathlib import Path

from PIL import Image

from design_ontology_harness.visual_evidence import compare_visuals


REPO_ROOT = Path(__file__).resolve().parent.parent


def test_compare_visuals_fails_for_identical_screenshots(tmp_path: Path):
    before = tmp_path / "before.png"
    after = tmp_path / "after.png"
    Image.new("RGBA", (10, 10), (255, 255, 255, 255)).save(before)
    Image.new("RGBA", (10, 10), (255, 255, 255, 255)).save(after)

    report = compare_visuals(before, after)

    assert not report.ok
    assert report.before_sha256 == report.after_sha256
    assert report.changed_pixels == 0
    assert report.change_ratio == 0.0


def test_compare_visuals_passes_when_pixel_delta_exceeds_threshold(tmp_path: Path):
    before = tmp_path / "before.png"
    after = tmp_path / "after.png"
    Image.new("RGBA", (10, 10), (255, 255, 255, 255)).save(before)
    revised = Image.new("RGBA", (10, 10), (255, 255, 255, 255))
    for x in range(5):
        for y in range(10):
            revised.putpixel((x, y), (0, 0, 0, 255))
    revised.save(after)

    report = compare_visuals(before, after, min_change_ratio=0.1)

    assert report.ok
    assert report.before_sha256 != report.after_sha256
    assert report.changed_pixels == 50
    assert report.change_ratio == 0.5


def test_compare_visuals_rejects_different_viewport_dimensions(tmp_path: Path):
    before = tmp_path / "before.png"
    after = tmp_path / "after.png"
    Image.new("RGBA", (1280, 720), (255, 255, 255, 255)).save(before)
    Image.new("RGBA", (390, 844), (0, 0, 0, 255)).save(after)

    report = compare_visuals(before, after)

    assert not report.ok
    assert report.change_ratio == 0.0
    assert "not comparable" in report.reason


def test_cli_compare_visuals_exits_nonzero_for_identical_screenshots(tmp_path: Path):
    before = tmp_path / "before.png"
    after = tmp_path / "after.png"
    Image.new("RGBA", (10, 10), (255, 255, 255, 255)).save(before)
    Image.new("RGBA", (10, 10), (255, 255, 255, 255)).save(after)

    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "design_ontology_harness.cli",
            "compare-visuals",
            "--before",
            str(before),
            "--after",
            str(after),
        ],
        cwd=REPO_ROOT,
        text=True,
        capture_output=True,
        check=False,
    )

    assert result.returncode == 1
    assert "byte-identical" in result.stdout
