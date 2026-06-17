"""Render the raw-CSS Mycelia screens to PNG with a real CSS engine.

WeasyPrint lays out the HTML/CSS (tokens.css + app.css) to a single 1600x900
PDF page; PyMuPDF rasterizes it to PNG at 2x. No browser required, so it runs
without network egress.
"""

from __future__ import annotations

from pathlib import Path

import fitz  # PyMuPDF
from weasyprint import HTML

HERE = Path(__file__).resolve().parent
OUT = HERE.parent / "render"
OUT.mkdir(exist_ok=True)
SCREENS = ["identify", "field-map", "logbook"]
ZOOM = 2.0


def render(name: str) -> Path:
    html_path = HERE / f"{name}.html"
    pdf_bytes = HTML(filename=str(html_path), base_url=str(HERE)).write_pdf()
    doc = fitz.open(stream=pdf_bytes, filetype="pdf")
    page = doc[0]
    pix = page.get_pixmap(matrix=fitz.Matrix(ZOOM, ZOOM), alpha=False)
    out = OUT / f"html-{name}.png"
    pix.save(out)
    doc.close()
    return out


if __name__ == "__main__":
    for screen in SCREENS:
        print(render(screen))
