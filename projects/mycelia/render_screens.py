"""Render Mycelia feature screens FROM the derived design system (token_schema.json).

This is the loop-closing step of the image-first workflow: the GPT Image 2 concept
screens drove the design system; here we implement real screens using ONLY the
derived tokens (exact hexes, type scale, component anatomy) and capture them to PNG.

No browser needed — drawn with Pillow so it runs without network egress. Fonts map
the design system's intent (humanist serif / humanist sans / mono) onto locally
available faces: IBM Plex Serif, Work Sans, Liberation Mono.
"""

from __future__ import annotations

import json
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

HERE = Path(__file__).resolve().parent
TOKENS = json.loads((HERE / "design-system" / "token_schema.json").read_text())
OUT = HERE / "render"
OUT.mkdir(exist_ok=True)

# --- tokens -> locals (read straight from the derived design system) ---------
C = TOKENS["color"]
INK = C["base"]["ink"]["value"]
PAPER = C["base"]["paper"]["value"]
RAISED = C["base"]["paper-raised"]["value"]
BARK = C["base"]["bark"]["value"]
FOREST = C["brand"]["forest"]["value"]
SPORE = C["brand"]["spore"]["value"]
SUCCESS = C["semantic"]["success"]["value"]
WARNING = C["semantic"]["warning"]["value"]
DANGER = C["semantic"]["danger"]["value"]
MUTED = C["semantic"]["text-muted"]["value"]

S = 2  # supersample factor for crisp anti-aliased output
W, H = 1600, 900

CANVAS = "/mnt/skills/examples/canvas-design/canvas-fonts"
LIB = "/usr/share/fonts/truetype/liberation"


def _f(path: str, size: int) -> ImageFont.FreeTypeFont:
    return ImageFont.truetype(path, size * S)


SERIF = lambda s: _f(f"{CANVAS}/IBMPlexSerif-Regular.ttf", s)
SERIF_B = lambda s: _f(f"{CANVAS}/IBMPlexSerif-Bold.ttf", s)
SERIF_I = lambda s: _f(f"{CANVAS}/IBMPlexSerif-Italic.ttf", s)
SANS = lambda s: _f(f"{CANVAS}/WorkSans-Regular.ttf", s)
SANS_B = lambda s: _f(f"{CANVAS}/WorkSans-Bold.ttf", s)
MONO = lambda s: _f(f"{LIB}/LiberationMono-Regular.ttf", s)


def new_canvas() -> tuple[Image.Image, ImageDraw.ImageDraw]:
    img = Image.new("RGB", (W * S, H * S), PAPER)
    return img, ImageDraw.Draw(img)


def px(*vals: float) -> tuple[int, ...]:
    return tuple(int(v * S) for v in vals)


def rrect(d, box, radius, fill=None, outline=None, width=1):
    d.rounded_rectangle(px(*box), radius=radius * S, fill=fill, outline=outline,
                        width=max(1, int(width * S)))


def text(d, xy, s, font, fill=INK, anchor="la", spacing=4):
    d.text(px(*xy), s, font=font, fill=fill, anchor=anchor, spacing=spacing * S)


def hairline(d, x0, y0, x1, y1, fill=BARK, width=1):
    d.line(px(x0, y0, x1, y1), fill=fill, width=max(1, int(width * S)))


def mushroom(d, cx, cy, scale, cap=INK, stem=RAISED, outline=INK):
    """Minimal ink line-drawing mushroom glyph."""
    cw = 26 * scale
    ch = 16 * scale
    # cap (half ellipse)
    d.pieslice(px(cx - cw, cy - ch, cx + cw, cy + ch), 180, 360, fill=cap, outline=outline,
               width=max(1, int(1.5 * S)))
    d.line(px(cx - cw, cy, cx + cw, cy), fill=outline, width=max(1, int(1.5 * S)))
    # stem
    sw = 9 * scale
    sh = 18 * scale
    d.rounded_rectangle(px(cx - sw, cy, cx + sw, cy + sh), radius=int(4 * scale) * S,
                        fill=stem, outline=outline, width=max(1, int(1.5 * S)))
    # gills hint
    for gx in (-12, -4, 4, 12):
        d.line(px(cx + gx * scale, cy - 1, cx + gx * scale, cy - ch * 0.55), fill=outline,
               width=max(1, int(S)))


def header(d, active="Identify"):
    rrect(d, (0, 0, W, 64), 0, fill=RAISED)
    hairline(d, 0, 64, W, 64, fill=BARK, width=1)
    mushroom(d, 40, 30, 0.7)
    text(d, (66, 20), "Mycelia", SERIF_B(24), fill=INK)
    links = ["Identify", "Field Map", "Logbook", "Community"]
    x = W - 64
    for name in reversed(links):
        f = SANS_B(15) if name == active else SANS(15)
        w = d.textlength(name, font=f) / S
        text(d, (x - w, 24), name, f, fill=INK if name == active else MUTED)
        if name == active:
            d.line(px(x - w, 50, x, 50), fill=SPORE, width=int(2.5 * S))
        x -= w + 36


def chip(d, x, y, label, kind):
    color = {"success": SUCCESS, "warning": WARNING, "danger": DANGER}[kind]
    f = SANS_B(12)
    w = d.textlength(label, font=f) / S + 22
    rrect(d, (x, y, x + w, y + 22), 11, fill=None, outline=color, width=1.5)
    d.ellipse(px(x + 9, y + 9, x + 13, y + 13), fill=color)
    text(d, (x + 18, y + 5), label, f, fill=color)
    return w


def confidence_bar(d, x, y, w, pct):
    rrect(d, (x, y, x + w, y + 6), 3, fill="#E7DEC9")
    rrect(d, (x, y, x + w * pct / 100, y + 6), 3, fill=FOREST)
    text(d, (x + w + 10, y - 6), f"{pct}%", MONO(13), fill=FOREST, anchor="la")


def button(d, x, y, w, label):
    rrect(d, (x, y, x + w, y + 44), 8, fill=FOREST)
    text(d, (x + w / 2, y + 22), label, SANS_B(15), fill=RAISED, anchor="mm")


def finish(img, name):
    img = img.resize((W, H), Image.LANCZOS)
    path = OUT / name
    img.save(path)
    return path


# --------------------------------------------------------------------------- #
# Screen 1: identify
# --------------------------------------------------------------------------- #
def render_identify():
    img, d = new_canvas()
    header(d, active="Identify")
    text(d, (48, 92), "Identify a find", SERIF_B(28), fill=INK)
    text(d, (48, 132), "3 candidate matches from your photo — check edibility before anything else.",
         SANS(15), fill=MUTED)

    # left photo panel
    rrect(d, (48, 176, 560, 700), 10, fill=RAISED, outline=BARK, width=1)
    rrect(d, (72, 200, 536, 600), 8, fill="#EDE4D2")
    mushroom(d, 304, 380, 3.2)
    text(d, (72, 624), "your_upload.jpg", MONO(13), fill=MUTED)
    text(d, (72, 652), "Forest floor · 17 Jun 2026 · 540m", SANS(14), fill=INK)

    # right candidate list
    cards = [
        ("Cantharellus cibarius", "Golden chanterelle", 92, "Edible · verified", "success", True),
        ("Hygrophoropsis aurantiaca", "False chanterelle", 61, "Unverified", "warning", False),
        ("Omphalotus olearius", "Jack-o'-lantern", 38, "Poisonous", "danger", False),
    ]
    y = 176
    for latin, common, pct, tag, kind, top in cards:
        rrect(d, (584, y, 1552, y + 156), 10, fill=RAISED, outline=BARK, width=1)
        if top:
            rrect(d, (584, y, 590, y + 156), 0, fill=SPORE)
            text(d, (612, y + 18), "TOP MATCH", SANS_B(11), fill=SPORE)
        rrect(d, (612, y + 44, 720, y + 140), 8, fill="#EDE4D2")
        mushroom(d, 666, y + 86, 1.5)
        text(d, (744, y + (44 if top else 26)), latin, SERIF_I(22), fill=INK)
        text(d, (744, y + (76 if top else 58)), common, SANS(15), fill=MUTED)
        confidence_bar(d, 744, y + (112 if top else 96), 360, pct)
        chip(d, 1180, y + (44 if top else 30), tag, kind)
        y += 172

    button(d, 584, y + 4, 240, "Save to logbook")
    text(d, (840, y + 16), "Safety: never eat a find based on an app alone.", SANS(13), fill=DANGER)
    return finish(img, "identify.png")


# --------------------------------------------------------------------------- #
# Screen 2: field-map
# --------------------------------------------------------------------------- #
def render_field_map():
    img, d = new_canvas()
    header(d, active="Field Map")

    # left filter sidebar
    rrect(d, (0, 64, 300, H), 0, fill=RAISED)
    hairline(d, 300, 64, 300, H, fill=BARK, width=1)
    text(d, (32, 92), "Filters", SERIF_B(20), fill=INK)
    groups = [("Season", ["Spring", "Summer", "Autumn"], 2),
              ("Habitat", ["Conifer", "Deciduous", "Meadow"], 0),
              ("Edibility", ["Edible", "Unverified", "Toxic"], 0)]
    y = 140
    for title, opts, checked in groups:
        text(d, (32, y), title, SANS_B(14), fill=INK)
        y += 30
        for i, opt in enumerate(opts):
            box = (32, y, 50, y + 18)
            on = i == checked
            rrect(d, box, 4, fill=FOREST if on else None, outline=FOREST if on else BARK, width=1.5)
            if on:
                d.line(px(36, y + 9, 40, y + 13), fill=RAISED, width=int(2 * S))
                d.line(px(40, y + 13, 47, y + 4), fill=RAISED, width=int(2 * S))
            text(d, (60, y + 1), opt, SANS(14), fill=INK if on else MUTED)
            y += 28
        y += 18

    # map area (muted topographic paper, not blue)
    rrect(d, (300, 64, W, H), 0, fill="#E7E0CC")
    for r in range(80, 900, 70):
        d.ellipse(px(560 - r, 470 - r * 0.6, 560 + r, 470 + r * 0.6), outline="#D8CEB2",
                  width=max(1, int(S)))
    for r in range(60, 520, 64):
        d.ellipse(px(1240 - r, 300 - r * 0.6, 1240 + r, 300 + r * 0.6), outline="#D8CEB2",
                  width=max(1, int(S)))
    hairline(d, 300, 470, W, 470, fill="#D8CEB2", width=1)

    pins = [(620, 430, FOREST, False), (980, 600, FOREST, False),
            (1180, 320, FOREST, False), (760, 560, SPORE, True)]
    for cx, cy, col, sel in pins:
        d.ellipse(px(cx - 5, cy - 5, cx + 5, cy + 5), fill="#00000022")
        mushroom(d, cx, cy - 18, 0.7, cap=col, stem=RAISED, outline=col if not sel else INK)
        if sel:
            d.ellipse(px(cx - 22, cy - 40, cx + 22, cy + 6), outline=SPORE, width=int(2 * S))

    # floating sighting card
    cx0, cy0 = 1120, 520
    d.rounded_rectangle(px(cx0 + 4, cy0 + 8, cx0 + 444, cy0 + 220), radius=10 * S, fill="#00000018")
    rrect(d, (cx0, cy0, cx0 + 440, cy0 + 212), 10, fill=RAISED, outline=BARK, width=1)
    rrect(d, (cx0 + 20, cy0 + 20, cx0 + 132, cy0 + 132), 8, fill="#EDE4D2")
    mushroom(d, cx0 + 76, cy0 + 76, 1.4)
    text(d, (cx0 + 152, cy0 + 24), "Cantharellus cibarius", SERIF_I(20), fill=INK)
    text(d, (cx0 + 152, cy0 + 56), "Golden chanterelle", SANS(14), fill=MUTED)
    text(d, (cx0 + 152, cy0 + 86), "14 Jun 2026 · by A. Park", MONO(13), fill=MUTED)
    chip(d, cx0 + 152, cy0 + 120, "Edible · verified", "success")
    text(d, (cx0 + 20, cy0 + 160), "Conifer floor, north-facing slope.", SANS(14), fill=INK)
    return finish(img, "field-map.png")


# --------------------------------------------------------------------------- #
# Screen 3: logbook + species detail
# --------------------------------------------------------------------------- #
def render_logbook():
    img, d = new_canvas()
    header(d, active="Logbook")

    # left timeline list
    text(d, (48, 92), "My logbook", SERIF_B(28), fill=INK)
    text(d, (48, 134), "24 finds logged", SANS(14), fill=MUTED)
    finds = [("Golden chanterelle", "14 Jun 2026", "Pine ridge", True),
             ("Birch bolete", "02 Jun 2026", "River birch stand", False),
             ("Fly agaric", "28 May 2026", "Spruce edge", False),
             ("Morel", "19 Apr 2026", "Old orchard", False),
             ("Oyster mushroom", "11 Apr 2026", "Fallen beech", False)]
    y = 176
    for name, date, loc, active in finds:
        if active:
            rrect(d, (40, y - 8, 540, y + 64), 8, fill=RAISED, outline=BARK, width=1)
        rrect(d, (56, y, 104, y + 48), 8, fill="#EDE4D2")
        mushroom(d, 80, y + 24, 0.95)
        text(d, (120, y + 2), name, SANS_B(16), fill=INK)
        text(d, (120, y + 26), loc, SANS(13), fill=MUTED)
        text(d, (404, y + 4), date, MONO(13), fill=MUTED)
        y += 84
        if not active:
            hairline(d, 56, y - 18, 540, y - 18, fill=BARK, width=1)

    # right species detail (field-guide page)
    rrect(d, (588, 92, 1552, 856), 10, fill=RAISED, outline=BARK, width=1)
    rrect(d, (620, 124, 1060, 520), 8, fill="#EDE4D2")
    mushroom(d, 840, 322, 4.0)
    text(d, (620, 540), "Cantharellus cibarius", SERIF_B(34), fill=INK)
    text(d, (620, 586), "Golden chanterelle", SANS(17), fill=MUTED)
    chip(d, 620, 624, "Edible · verified", "success")

    tax = [("Family", "Cantharellaceae"), ("Genus", "Cantharellus"),
           ("Cap", "5–10 cm, egg-yellow, wavy"), ("Habitat", "Conifer & beech floor"),
           ("Season", "Jun – Oct")]
    ty = 124
    for k, v in tax:
        text(d, (1100, ty), k, SANS_B(13), fill=MUTED)
        text(d, (1100, ty + 20), v, SANS(15), fill=INK)
        hairline(d, 1100, ty + 52, 1520, ty + 52, fill=BARK, width=1)
        ty += 70

    # seasonal availability bar chart
    text(d, (620, 676), "Seasonal availability", SANS_B(14), fill=INK)
    months = ["J", "F", "M", "A", "M", "J", "J", "A", "S", "O", "N", "D"]
    vals = [0, 0, 0, 0, 1, 3, 4, 5, 5, 4, 1, 0]
    bx = 620
    for m, v in zip(months, vals):
        bh = v * 16
        col = FOREST if v >= 2 else BARK
        rrect(d, (bx, 760 - bh, bx + 40, 760), 3, fill=col if v else "#E7DEC9")
        text(d, (bx + 20, 768), m, MONO(12), fill=MUTED, anchor="ma")
        bx += 56

    button(d, 1300, 690, 220, "Add observation")
    return finish(img, "logbook.png")


if __name__ == "__main__":
    paths = [render_identify(), render_field_map(), render_logbook()]
    for p in paths:
        print(p)
