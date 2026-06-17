# Mycelia — raw-CSS implementation

Real HTML/CSS implementation of the Mycelia design system (step 5–6 output),
used to produce the rendered result images in `../render/html-*.png`.

## Files

- `tokens.css` — CSS variables generated from `../design-system/token_schema.json`
  (exact hexes, type families, radius, elevation) + `@font-face` for the bundled
  faces that stand in for the system's serif / sans / mono intent.
- `app.css` — component styles (header, cards, chips, confidence bar, filters,
  map, timeline, species detail) built only on the tokens.
- `identify.html`, `field-map.html`, `logbook.html` — the three feature surfaces.
- `fonts/` — bundled faces: IBM Plex Serif (display), Work Sans (body),
  Liberation Mono (mono).
- `render_html.py` — renders each HTML to PNG with a real CSS engine.

## Render

No browser is needed (this environment blocks the Chromium download). WeasyPrint
lays out the HTML/CSS to a 1600×900 PDF page; PyMuPDF rasterizes it at 2×.

```bash
uv pip install weasyprint pymupdf   # render-time only deps
uv run python projects/mycelia/site/render_html.py
# -> projects/mycelia/render/html-{identify,field-map,logbook}.png
```

Fonts map the system intent onto bundled faces; swap the `@font-face` `src` to
the real Spectral / Source Sans 3 web fonts in an online build.
