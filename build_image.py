#!/usr/bin/env python3
"""Draws the one-image news front page for Thursday 19 November 2026.

Renders a 1024x1024 PNG with PIL only: flat editorial design, all text set
in real fonts so nothing is garbled. Output: front-page.png beside this file.
"""
import math
import os
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "front-page.png")

S = 1024
PAPER = (250, 247, 240)
INK = (22, 19, 14)
MUTED = (104, 96, 84)
FAINT = (216, 209, 194)
RED = (176, 48, 28)
NAVY = (20, 38, 63)
NAVY_LINE = (64, 92, 128)
CREAM = (243, 238, 226)
CIRCLE_BG = (240, 234, 219)

NOTO = "/usr/share/fonts/truetype/noto/NotoSans-%s.ttf"
SERIF_B = "/usr/share/fonts/truetype/liberation/LiberationSerif-Bold.ttf"


def f_black(size):
    return ImageFont.truetype(NOTO % "Black", size)


def f_bold(size):
    return ImageFont.truetype(NOTO % "Bold", size)


def f_reg(size):
    return ImageFont.truetype(NOTO % "Regular", size)


def f_serif(size):
    return ImageFont.truetype(SERIF_B, size)


img = Image.new("RGB", (S, S), PAPER)
d = ImageDraw.Draw(img)

M = 46                      # page margin
CW = S - 2 * M              # content width


def tracked(draw, xy, text, font, fill, tracking=3, anchor_left=True):
    """Draw letter-spaced text; returns total width."""
    x, y = xy
    total = 0
    for ch in text:
        w = draw.textlength(ch, font=font)
        draw.text((x + total, y), ch, font=font, fill=fill)
        total += w + tracking
    return total - tracking if text else 0


def tracked_center(draw, cx, y, text, font, fill, tracking=3):
    total = 0
    for ch in text:
        total += draw.textlength(ch, font=font) + tracking
    total -= tracking if text else 0
    tracked(draw, (cx - total / 2, y), text, font, fill, tracking)
    return total


def wrap(draw, text, font, maxw):
    words = text.split()
    lines, cur = [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if draw.textlength(t, font=font) <= maxw or not cur:
            cur = t
        else:
            lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def star(draw, cx, cy, r, fill):
    pts = []
    for i in range(10):
        ang = -math.pi / 2 + i * math.pi / 5
        rad = r if i % 2 == 0 else r * 0.42
        pts.append((cx + rad * math.cos(ang), cy + rad * math.sin(ang)))
    draw.polygon(pts, fill=fill)


# ---------------------------------------------------------------- masthead
d.rectangle([0, 0, S, 10], fill=INK)
y = 30
tracked_center(d, S / 2, y, "THE WORLD IN ONE DAY", f_serif(46), INK, tracking=6)
y += 66
tracked_center(d, S / 2, y, "ONE IMAGE · THE DAY'S ESSENTIAL NEWS", f_bold(15), MUTED, tracking=4)
y += 34
d.line([M, y, S - M, y], fill=INK, width=3)
d.line([M, y + 5, S - M, y + 5], fill=INK, width=1)

# ---------------------------------------------------------------- date band
y += 18
date_f = f_black(49)
tracked_center(d, S / 2, y, "THURSDAY, 19 NOVEMBER 2026", date_f, INK, tracking=2)
y += 68
d.line([M, y, S - M, y], fill=INK, width=3)

# ---------------------------------------------------------------- lead story
lead_y = y + 24
PANEL_W = 388
PANEL_H = 236
d.rectangle([M, lead_y, M + PANEL_W, lead_y + PANEL_H], fill=NAVY)
tracked_center(d, M + PANEL_W / 2, lead_y + 18, "THREE PRESIDENTS · ONE TABLE",
               f_bold(14), CREAM, tracking=3)

# three flags in the panel
FW, FH = 106, 70
fy = lead_y + 56
gap = (PANEL_W - 3 * FW) / 4
flags_x = [M + gap + i * (FW + gap) for i in range(3)]

# USA: stripes + blue canton
fx = flags_x[0]
d.rectangle([fx, fy, fx + FW, fy + FH], fill=(255, 255, 255))
for i in range(7):
    yy = fy + i * (FH / 13) * 2
    d.rectangle([fx, yy, fx + FW, yy + FH / 13], fill=(178, 34, 52))
d.rectangle([fx, fy, fx + FW * 0.44, fy + FH * 7 / 13], fill=(60, 59, 110))
for r in range(4):
    for c in range(5):
        cx = fx + 6 + c * (FW * 0.44 - 10) / 4
        cy = fy + 6 + r * (FH * 7 / 13 - 10) / 3
        star(d, cx, cy, 2.6, (255, 255, 255))
d.rectangle([fx, fy, fx + FW, fy + FH], outline=NAVY_LINE, width=1)

# China: red field, one big star + four small
fx = flags_x[1]
d.rectangle([fx, fy, fx + FW, fy + FH], fill=(222, 41, 16))
star(d, fx + 22, fy + 20, 11, (255, 222, 0))
for i, (dx, dy) in enumerate([(44, 8), (50, 20), (50, 33), (44, 45)]):
    star(d, fx + dx, fy + dy, 4.5, (255, 222, 0))
d.rectangle([fx, fy, fx + FW, fy + FH], outline=NAVY_LINE, width=1)

# Russia: white / blue / red thirds
fx = flags_x[2]
d.rectangle([fx, fy, fx + FW, fy + FH / 3], fill=(255, 255, 255))
d.rectangle([fx, fy + FH / 3, fx + FW, fy + 2 * FH / 3], fill=(0, 57, 166))
d.rectangle([fx, fy + 2 * FH / 3, fx + FW, fy + FH], fill=(213, 43, 30))
d.rectangle([fx, fy, fx + FW, fy + FH], outline=NAVY_LINE, width=1)

for fx, name in zip(flags_x, ["UNITED STATES", "CHINA", "RUSSIA"]):
    tracked_center(d, fx + FW / 2, fy + FH + 12, name, f_bold(13), CREAM, tracking=2)
tracked_center(d, M + PANEL_W / 2, lead_y + PANEL_H - 34,
               "APEC SUMMIT — SHENZHEN, CHINA", f_bold(14), CREAM, tracking=3)

# lead text column
tx = M + PANEL_W + 30
tw = S - M - tx
tracked(d, (tx, lead_y + 2), "LEAD STORY", f_bold(16), RED, tracking=4)
hy = lead_y + 34
head_f = f_black(38)
for line in wrap(d, "Trump, Xi & Putin Hold First-Ever Trilateral Summit", head_f, tw):
    d.text((tx, hy), line, font=head_f, fill=INK)
    hy += 46
hy += 6
sub_f = f_reg(20)
for line in wrap(d, "Nuclear arms control, Ukraine and Iran top the agenda "
                    "at the APEC summit in Shenzhen.", sub_f, tw):
    d.text((tx, hy), line, font=sub_f, fill=(58, 52, 44))
    hy += 27

grid_top = lead_y + PANEL_H + 22
d.line([M, grid_top - 11, S - M, grid_top - 11], fill=INK, width=3)

# ---------------------------------------------------------------- icons
def icon_flame(d, cx, cy):
    pts = [(cx, cy - 17), (cx + 8, cy - 4), (cx + 11, cy + 4), (cx + 7, cy + 13),
           (cx, cy + 16), (cx - 7, cy + 13), (cx - 11, cy + 4), (cx - 6, cy - 5)]
    d.polygon(pts, outline=RED, width=4)
    d.line([cx - 14, cy + 22, cx - 5, cy + 19, cx + 3, cy + 22, cx + 12, cy + 19],
           fill=NAVY, width=3)


def icon_advance(d, cx, cy):
    for i in range(3):
        ox = cx - 14 + i * 11
        d.line([ox, cy - 12, ox + 9, cy, ox, cy + 12], fill=RED, width=4, joint="curve")
    d.line([cx - 17, cy + 20, cx + 18, cy + 20], fill=NAVY, width=3)


def icon_bridge(d, cx, cy):
    d.arc([cx - 19, cy - 16, cx + 19, cy + 22], start=180, end=360, fill=RED, width=4)
    d.line([cx - 20, cy + 12, cx + 20, cy + 12], fill=NAVY, width=4)
    for dx in (-12, 0, 12):
        d.line([cx + dx, cy - 6, cx + dx, cy + 12], fill=NAVY, width=3)


def icon_clash(d, cx, cy):
    d.line([cx - 18, cy - 8, cx - 3, cy - 8], fill=RED, width=4)
    d.polygon([(cx - 3, cy - 13), (cx - 3, cy - 3), (cx + 4, cy - 8)], fill=RED)
    d.line([cx + 18, cy + 8, cx + 3, cy + 8], fill=NAVY, width=4)
    d.polygon([(cx + 3, cy + 3), (cx + 3, cy + 13), (cx - 4, cy + 8)], fill=NAVY)
    d.line([cx, cy - 18, cx - 3, cy - 4, cx + 2, cy + 6, cx, cy + 18], fill=INK, width=3)


def icon_scales(d, cx, cy):
    d.line([cx, cy - 17, cx, cy + 14], fill=INK, width=4)
    d.line([cx - 16, cy - 12, cx + 16, cy - 12], fill=INK, width=4)
    for sx in (-16, 16):
        d.line([cx + sx, cy - 12, cx + sx - 6, cy + 4], fill=RED, width=3)
        d.line([cx + sx, cy - 12, cx + sx + 6, cy + 4], fill=RED, width=3)
        d.arc([cx + sx - 8, cy - 2, cx + sx + 8, cy + 12], start=0, end=180, fill=RED, width=3)
    d.line([cx - 10, cy + 18, cx + 10, cy + 18], fill=INK, width=4)


def icon_thermo(d, cx, cy):
    d.rounded_rectangle([cx - 5, cy - 19, cx + 5, cy + 8], radius=5, outline=RED, width=4)
    d.ellipse([cx - 9, cy + 4, cx + 9, cy + 22], outline=RED, width=4)
    d.ellipse([cx - 4, cy + 9, cx + 4, cy + 17], fill=RED)
    d.line([cx, cy + 8, cx, cy - 12], fill=RED, width=4)
    for i in range(3):
        yy = cy - 12 + i * 8
        d.line([cx + 8, yy, cx + 14, yy], fill=NAVY, width=3)


def icon_probe(d, cx, cy):
    # dish: a bowl arc with a feed stem, signal arcs above
    d.arc([cx - 15, cy - 6, cx + 13, cy + 22], start=180, end=360, fill=INK, width=4)
    d.line([cx - 1, cy + 8, cx - 1, cy - 4], fill=INK, width=3)
    d.ellipse([cx - 3, cy - 7, cx + 1, cy - 3], fill=RED)
    d.line([cx - 8, cy + 15, cx - 12, cy + 21], fill=INK, width=3)
    d.line([cx + 6, cy + 15, cx + 10, cy + 21], fill=INK, width=3)
    for r in (7, 13):
        d.arc([cx - 1 - r, cy - 12 - r, cx - 1 + r, cy - 12 + r], start=200, end=340, fill=RED, width=3)


def icon_pad(d, cx, cy):
    d.rounded_rectangle([cx - 19, cy - 12, cx + 19, cy + 12], radius=9, outline=INK, width=4)
    d.line([cx - 13, cy - 5, cx - 13, cy + 5], fill=RED, width=4)
    d.line([cx - 18, cy, cx - 8, cy], fill=RED, width=4)
    d.ellipse([cx + 7, cy - 7, cx + 12, cy - 2], fill=NAVY)
    d.ellipse([cx + 12, cy + 1, cx + 17, cy + 6], fill=RED)


def icon_seismic(d, cx, cy):
    pts = [(cx - 19, cy), (cx - 11, cy), (cx - 7, cy - 13), (cx - 2, cy + 15),
           (cx + 3, cy - 8), (cx + 7, cy), (cx + 19, cy)]
    d.line(pts, fill=RED, width=4, joint="curve")
    d.line([cx - 19, cy + 19, cx + 19, cy + 19], fill=NAVY, width=3)


# ---------------------------------------------------------------- tiles
TILES = [
    ("CONFLICT · THE GULF", icon_flame,
     "Tankers Ablaze in the Strait of Hormuz",
     "Iran says 3 hit mines; US struck Qeshm"),
    ("MIDDLE EAST", icon_advance,
     "Israel Launches Ground Operation in Central Gaza",
     "Calls grow to let aid reach flooded Gaza"),
    ("UKRAINE WAR", icon_bridge,
     "Ukraine Strikes the Crimean Bridge Again",
     "Bridge linking Russia with Crimea hit"),
    ("AFRICA", icon_clash,
     "Ethiopia–Eritrea Clashes Raise Fears of War",
     "Border fighting threatens a wider war"),
    ("WORLD COURT", icon_scales,
     "World Court Rules on Myanmar Genocide Case",
     "Rohingya judgment at The Hague"),
    ("CLIMATE", icon_thermo,
     "COP31 Talks Stall Over Climate Finance",
     "Final days in Antalya, Türkiye"),
    ("SPACE", icon_probe,
     "Voyager 1 Is Now One Light-Day From Earth",
     "NASA's farthest probe, 26 billion km out"),
    ("GAMING", icon_pad,
     "GTA VI Launches After a 13-Year Wait",
     "Rockstar's sequel lands to rave reviews"),
    ("JAPAN", icon_seismic,
     "Magnitude 5.7 Quake Jolts Kumamoto",
     "No tsunami warning issued"),
]

COLS, ROWS = 3, 3
GUT = 26
tile_w = (CW - (COLS - 1) * GUT) / COLS
tile_h = 122
ROW_GAP = 12
grid_h = ROWS * tile_h + (ROWS - 1) * ROW_GAP
tag_f = f_bold(13)
tile_head_f = f_bold(20)
tile_sub_f = f_reg(15)

for r in range(1, ROWS):
    yy = grid_top + r * (tile_h + ROW_GAP) - ROW_GAP // 2
    d.line([M, yy, S - M, yy], fill=FAINT, width=1)

for idx, (tag, icon, head, sub) in enumerate(TILES):
    r, c = divmod(idx, COLS)
    x0 = M + c * (tile_w + GUT)
    y0 = grid_top + r * (tile_h + ROW_GAP)
    ccx, ccy = x0 + 21, y0 + 21
    d.ellipse([ccx - 21, ccy - 21, ccx + 21, ccy + 21], fill=CIRCLE_BG)
    icon(d, ccx, ccy)
    tracked(d, (x0 + 52, y0 + 13), tag, tag_f, RED, tracking=2)
    hy = y0 + 50
    for line in wrap(d, head, tile_head_f, tile_w)[:2]:
        d.text((x0, hy), line, font=tile_head_f, fill=INK)
        hy += 25
    sub_lines = wrap(d, sub, tile_sub_f, tile_w)
    assert len(sub_lines) == 1, f"sub wraps to {len(sub_lines)} lines: {sub}"
    d.text((x0, hy + 2), sub_lines[0], font=tile_sub_f, fill=MUTED)

# ---------------------------------------------------------------- ticker
tick_y = grid_top + grid_h + 16
d.rectangle([0, tick_y, S, tick_y + 60], fill=INK)
tick_f = f_bold(16)
tracked_center(d, S / 2, tick_y + 8,
               "ALSO TODAY — VAN GOGH SELLS FOR A RECORD $190.4M",
               tick_f, CREAM, tracking=1)
tracked_center(d, S / 2, tick_y + 34,
               "JEFFRIES SET TO BE FIRST BLACK US HOUSE SPEAKER · PEW: MUSLIMS TO OUTNUMBER CHRISTIANS BY 2035",
               f_reg(14), (206, 198, 182), tracking=1)
d.text((S / 2, tick_y + 70), "Compiled from the day's reporting",
       font=f_reg(12), fill=MUTED, anchor="ma")

img.save(OUT, optimize=True)
print("wrote", OUT, os.path.getsize(OUT), "bytes")
