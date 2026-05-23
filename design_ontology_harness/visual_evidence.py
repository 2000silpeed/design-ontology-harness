from __future__ import annotations

import hashlib
import json
from dataclasses import asdict, dataclass
from pathlib import Path

from PIL import Image, ImageChops


@dataclass(frozen=True)
class VisualComparisonReport:
    before_path: str
    after_path: str
    before_sha256: str
    after_sha256: str
    before_size: tuple[int, int]
    after_size: tuple[int, int]
    min_change_ratio: float
    changed_pixels: int
    total_pixels: int
    change_ratio: float
    ok: bool
    reason: str

    def to_dict(self) -> dict:
        return asdict(self)


def compare_visuals(
    before_path: Path,
    after_path: Path,
    *,
    min_change_ratio: float = 0.001,
) -> VisualComparisonReport:
    before = before_path.resolve()
    after = after_path.resolve()
    before_sha = _sha256(before)
    after_sha = _sha256(after)

    with Image.open(before) as before_image_raw, Image.open(after) as after_image_raw:
        before_image = before_image_raw.convert("RGBA")
        after_image = after_image_raw.convert("RGBA")
        before_size = before_image.size
        after_size = after_image.size

        if before_sha == after_sha:
            total_pixels = before_size[0] * before_size[1]
            return VisualComparisonReport(
                before_path=str(before),
                after_path=str(after),
                before_sha256=before_sha,
                after_sha256=after_sha,
                before_size=before_size,
                after_size=after_size,
                min_change_ratio=min_change_ratio,
                changed_pixels=0,
                total_pixels=total_pixels,
                change_ratio=0.0,
                ok=False,
                reason="Screenshots are byte-identical; visual change is not evidenced.",
            )

        if before_size != after_size:
            before_pixels = before_size[0] * before_size[1]
            after_pixels = after_size[0] * after_size[1]
            return VisualComparisonReport(
                before_path=str(before),
                after_path=str(after),
                before_sha256=before_sha,
                after_sha256=after_sha,
                before_size=before_size,
                after_size=after_size,
                min_change_ratio=min_change_ratio,
                changed_pixels=max(before_pixels, after_pixels),
                total_pixels=max(before_pixels, after_pixels),
                change_ratio=1.0,
                ok=True,
                reason="Screenshot dimensions differ; review framing plus visual content before claiming improvement.",
            )

        diff = ImageChops.difference(before_image, after_image)
        diff_pixels = diff.get_flattened_data() if hasattr(diff, "get_flattened_data") else diff.getdata()
        changed_pixels = sum(1 for pixel in diff_pixels if pixel != (0, 0, 0, 0))
        total_pixels = before_size[0] * before_size[1]
        change_ratio = changed_pixels / total_pixels if total_pixels else 0.0
        ok = change_ratio >= min_change_ratio
        reason = (
            f"Screenshots differ across {change_ratio:.3%} of pixels."
            if ok
            else f"Screenshots differ across only {change_ratio:.3%} of pixels; below the {min_change_ratio:.3%} evidence threshold."
        )

    return VisualComparisonReport(
        before_path=str(before),
        after_path=str(after),
        before_sha256=before_sha,
        after_sha256=after_sha,
        before_size=before_size,
        after_size=after_size,
        min_change_ratio=min_change_ratio,
        changed_pixels=changed_pixels,
        total_pixels=total_pixels,
        change_ratio=change_ratio,
        ok=ok,
        reason=reason,
    )


def format_visual_comparison(report: VisualComparisonReport) -> str:
    status = "OK" if report.ok else "FAIL"
    return "\n".join(
        [
            f"Visual comparison: {status}",
            f"- before: {report.before_path}",
            f"- after: {report.after_path}",
            f"- before_sha256: {report.before_sha256}",
            f"- after_sha256: {report.after_sha256}",
            f"- before_size: {report.before_size[0]}x{report.before_size[1]}",
            f"- after_size: {report.after_size[0]}x{report.after_size[1]}",
            f"- changed_pixels: {report.changed_pixels}/{report.total_pixels} ({report.change_ratio:.3%})",
            f"- min_change_ratio: {report.min_change_ratio:.3%}",
            f"- reason: {report.reason}",
        ]
    )


def format_visual_comparison_json(report: VisualComparisonReport) -> str:
    return json.dumps(report.to_dict(), ensure_ascii=False, indent=2)


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()
