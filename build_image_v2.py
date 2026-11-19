#!/usr/bin/env python3
"""Draws the V2 one-image news front page for Thursday 19 November 2026.

Same verified stories and wording as V1, but every story now gets a small
drawn scene (flat editorial illustration, PIL only) instead of an icon.
All text is set in real fonts so nothing is garbled.
Output: front-page-v2.png beside this file (1024x1024).
"""
import math
import os
import random
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "front-page-v2.png")

S = 1024
PAPER = (250, 247, 240)
INK = (22, 19, 14)
MUTED = (104, 96, 84)
FAINT = (216, 209, 194)
RED = (176, 48, 28)
NAVY = (20, 38, 63)
CREAM = (243, 238, 226)
SUB = (58, 52, 44)

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


def tracked(draw, xy, text, font, fill, tracking=3):
    x, y = xy
    total = 0
    for ch in text:
        w = draw.textlength(ch, font=font)
        draw.text((x + total, y), ch, font=font, fill=fill)
        total += w + tracking
    return total - tracking if text else 0


def tracked_width(draw, text, font, tracking=3):
    if not text:
        return 0
    return sum(draw.textlength(ch, font=font) + tracking for ch in text) - tracking


def tracked_center(draw, cx, y, text, font, fill, tracking=3):
    total = tracked_width(draw, text, font, tracking)
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


def star(draw, cx, cy, r, fill, ratio=0.42, points=5):
    pts = []
    for i in range(points * 2):
        ang = -math.pi / 2 + i * math.pi / points
        rad = r if i % 2 == 0 else r * ratio
        pts.append((cx + rad * math.cos(ang), cy + rad * math.sin(ang)))
    draw.polygon(pts, fill=fill)


def flame(draw, cx, base, h, w, outer, inner):
    pts = [(cx, base - h), (cx + w * 0.40, base - h * 0.48),
           (cx + w * 0.50, base - h * 0.16), (cx + w * 0.28, base),
           (cx - w * 0.28, base), (cx - w * 0.50, base - h * 0.16),
           (cx - w * 0.38, base - h * 0.52)]
    draw.polygon(pts, fill=outer)
    pts2 = [(cx, base - h * 0.58), (cx + w * 0.24, base - h * 0.28),
            (cx + w * 0.26, base - h * 0.08), (cx + w * 0.13, base),
            (cx - w * 0.13, base), (cx - w * 0.26, base - h * 0.08),
            (cx - w * 0.22, base - h * 0.30)]
    draw.polygon(pts2, fill=inner)


# ------------------------------------------------------------ scene canvas
# Scenes are drawn at 2x and downscaled for smooth edges. Coordinates inside
# scene functions are fractions of the scene box: X(f), Y(f).
SS = 2


def make_scene(w, h, bg):
    img = Image.new("RGB", (w * SS, h * SS), bg)
    return img, ImageDraw.Draw(img)


def finish_scene(img, w, h):
    return img.resize((w, h), Image.LANCZOS)


def FX(w):
    return lambda f: f * w * SS


# ------------------------------------------------------------ tile scenes
def sc_hormuz(w, h):
    img, d = make_scene(w, h, (198, 215, 224))
    X, Y = FX(w), FX(h)
    d.rectangle([0, Y(0.55), X(1), Y(1)], fill=(36, 84, 104))            # sea
    d.polygon([(0, Y(0.55)), (X(0.17), Y(0.55)), (X(0.10), Y(0.74)), (0, Y(0.76))],
              fill=(219, 186, 128))                                       # headland L
    d.polygon([(X(1), Y(0.55)), (X(0.84), Y(0.55)), (X(0.91), Y(0.74)), (X(1), Y(0.76))],
              fill=(219, 186, 128))                                       # headland R
    d.ellipse([X(0.865), Y(0.06), X(0.945), Y(0.30)], fill=(250, 214, 120))  # sun
    # smoke behind flames
    d.ellipse([X(0.40), Y(0.13), X(0.60), Y(0.33)], fill=(178, 174, 168))
    d.ellipse([X(0.47), Y(0.05), X(0.63), Y(0.22)], fill=(188, 184, 178))
    d.ellipse([X(0.34), Y(0.22), X(0.50), Y(0.38)], fill=(168, 164, 158))
    # tanker
    d.rectangle([X(0.205), Y(0.585), X(0.795), Y(0.65)], fill=(96, 46, 32))   # deck
    d.polygon([(X(0.20), Y(0.65)), (X(0.80), Y(0.65)), (X(0.755), Y(0.815)),
               (X(0.245), Y(0.815))], fill=(128, 56, 38))                    # hull
    d.rectangle([X(0.20), Y(0.65), X(0.80), Y(0.685)], fill=(84, 34, 26))
    d.rectangle([X(0.665), Y(0.44), X(0.74), Y(0.585)], fill=(233, 227, 215))  # bridge
    for i in range(3):
        d.rectangle([X(0.678 + i * 0.02), Y(0.475), X(0.69 + i * 0.02), Y(0.51)],
                    fill=(40, 48, 58))
    d.line([X(0.27), Y(0.46), X(0.27), Y(0.585)], fill=INK, width=5)          # mast
    flame(d, X(0.44), Y(0.585), Y(0.30), X(0.075), (233, 106, 38), (250, 192, 64))
    flame(d, X(0.545), Y(0.585), Y(0.235), X(0.06), (233, 106, 38), (250, 192, 64))
    for x0, yy in [(0.07, 0.88), (0.30, 0.93), (0.60, 0.90), (0.83, 0.94)]:
        d.line([X(x0), Y(yy), X(x0 + 0.09), Y(yy)], fill=(218, 236, 240), width=4)
    return finish_scene(img, w, h)


def sc_gaza(w, h):
    img, d = make_scene(w, h, (168, 192, 208))
    X, Y = FX(w), FX(h)
    d.rectangle([0, Y(0.34), X(1), Y(0.64)], fill=(233, 197, 150))
    d.rectangle([0, Y(0.64), X(1), Y(1)], fill=(242, 170, 108))
    d.ellipse([X(0.615), Y(0.40), X(0.79), Y(0.76)], fill=(246, 186, 104))
    d.ellipse([X(0.635), Y(0.44), X(0.77), Y(0.72)], fill=(252, 208, 112))
    rng = random.Random(7)
    towers = [(0.00, 0.07, 0.52), (0.06, 0.05, 0.68), (0.105, 0.06, 0.44),
              (0.16, 0.045, 0.78), (0.20, 0.06, 0.58), (0.255, 0.05, 0.86),
              (0.30, 0.065, 0.50), (0.36, 0.05, 0.72), (0.405, 0.055, 0.60),
              (0.455, 0.05, 0.90), (0.50, 0.06, 0.54), (0.555, 0.045, 0.76),
              (0.595, 0.06, 0.62), (0.65, 0.05, 0.84), (0.695, 0.06, 0.56),
              (0.75, 0.05, 0.70), (0.795, 0.055, 0.48), (0.845, 0.05, 0.80),
              (0.89, 0.06, 0.60), (0.945, 0.055, 0.66)]
    sil = (48, 54, 62)
    for bx, bw, bh in towers:
        d.rectangle([X(bx), Y(1 - bh), X(bx + bw), Y(1)], fill=sil)
        for _ in range(rng.randint(1, 3)):
            wx = bx + rng.uniform(0.008, bw - 0.014)
            wy = 1 - bh + rng.uniform(0.05, bh - 0.12)
            d.rectangle([X(wx), Y(wy), X(wx + 0.008), Y(wy + 0.055)],
                        fill=(245, 230, 190))
    return finish_scene(img, w, h)


def sc_bridge(w, h):
    img, d = make_scene(w, h, (198, 214, 224))
    X, Y = FX(w), FX(h)
    d.rectangle([0, Y(0.60), X(1), Y(1)], fill=(52, 98, 124))              # sea
    for px in (0.08, 0.24, 0.40, 0.56, 0.72, 0.88):
        d.rectangle([X(px), Y(0.56), X(px + 0.018), Y(0.94)], fill=(70, 80, 90))
    d.arc([X(0.355), Y(0.06), X(0.645), Y(0.60)], start=180, end=360,
          fill=(70, 80, 90), width=8)                                      # arch
    for hx, hy in [(0.435, 0.315), (0.50, 0.245), (0.565, 0.315)]:
        d.line([X(hx), Y(hy), X(hx), Y(0.535)], fill=(70, 80, 90), width=4)
    d.rectangle([0, Y(0.535), X(1), Y(0.575)], fill=(88, 98, 108))         # deck
    d.line([0, Y(0.535), X(1), Y(0.535)], fill=(205, 210, 215), width=3)
    d.ellipse([X(0.565), Y(0.10), X(0.70), Y(0.30)], fill=(172, 170, 166))  # smoke
    star(d, X(0.615), Y(0.40), Y(0.155), (238, 120, 40), ratio=0.45, points=8)
    star(d, X(0.615), Y(0.40), Y(0.09), (252, 202, 70), ratio=0.45, points=8)
    d.ellipse([X(0.60), Y(0.365), X(0.63), Y(0.435)], fill=(255, 246, 220))
    for x0, yy in [(0.10, 0.86), (0.42, 0.92), (0.78, 0.88)]:
        d.line([X(x0), Y(yy), X(x0 + 0.08), Y(yy)], fill=(216, 234, 240), width=4)
    return finish_scene(img, w, h)


def sc_horn(w, h):
    img, d = make_scene(w, h, (240, 232, 208))
    X, Y = FX(w), FX(h)
    d.polygon([(0, 0), (X(0.30), 0), (X(0.15), Y(0.32)), (0, Y(0.44))],
              fill=(168, 196, 208))                                        # Red Sea
    d.polygon([(X(1), Y(0.16)), (X(1), Y(1)), (X(0.85), Y(1)), (X(0.90), Y(0.55)),
               (X(0.95), Y(0.30))], fill=(168, 196, 208))                  # ocean
    land = [(0.30, 0.04), (0.47, 0.17), (0.62, 0.29), (0.865, 0.335),
            (0.80, 0.55), (0.66, 0.88), (0.52, 0.96), (0.40, 0.70),
            (0.30, 0.45), (0.255, 0.20)]
    d.polygon([(X(a), Y(b)) for a, b in land], fill=(222, 188, 124),
              outline=INK, width=3)
    border = [(0.335, 0.375), (0.42, 0.335), (0.50, 0.315), (0.565, 0.325)]
    for i in range(len(border) - 1):
        (ax, ay), (bx, by) = border[i], border[i + 1]
        for t0 in (0.0, 0.5):
            d.line([X(ax + (bx - ax) * t0), Y(ay + (by - ay) * t0),
                    X(ax + (bx - ax) * (t0 + 0.32)), Y(ay + (by - ay) * (t0 + 0.32))],
                   fill=INK, width=3)
    def pin(cx, cy, fill):
        d.polygon([(X(cx - 0.026), Y(cy - 0.10)), (X(cx + 0.026), Y(cy - 0.10)),
                   (X(cx), Y(cy + 0.13))], fill=fill)
        d.ellipse([X(cx - 0.032), Y(cy - 0.235), X(cx + 0.032), Y(cy - 0.09)],
                  fill=fill)
        d.ellipse([X(cx - 0.012), Y(cy - 0.185), X(cx + 0.012), Y(cy - 0.135)],
                  fill=CREAM)
    pin(0.435, 0.30, RED)
    pin(0.455, 0.50, NAVY)
    d.ellipse([X(0.075), Y(0.68), X(0.135), Y(0.86)], outline=INK, width=3)
    star(d, X(0.105), Y(0.77), Y(0.055), INK, ratio=0.30, points=4)
    return finish_scene(img, w, h)


def sc_court(w, h):
    img, d = make_scene(w, h, (206, 218, 226))
    X, Y = FX(w), FX(h)
    d.rectangle([0, Y(0.86), X(1), Y(1)], fill=(150, 158, 166))
    d.polygon([(X(0.20), Y(0.315)), (X(0.80), Y(0.315)), (X(0.50), Y(0.125))],
              fill=(56, 64, 76))                                           # pediment
    # scales emblem inside the pediment
    cx, cy = X(0.50), Y(0.24)
    d.line([cx, cy - Y(0.07), cx, cy + Y(0.062)], fill=CREAM, width=4)
    d.line([cx - X(0.058), cy - Y(0.052), cx + X(0.058), cy - Y(0.052)],
           fill=CREAM, width=4)
    for sx in (-0.058, 0.058):
        d.line([cx + X(sx), cy - Y(0.052), cx + X(sx) - X(0.021), cy + Y(0.032)],
               fill=CREAM, width=3)
        d.line([cx + X(sx), cy - Y(0.052), cx + X(sx) + X(0.021), cy + Y(0.032)],
               fill=CREAM, width=3)
        d.arc([cx + X(sx) - X(0.027), cy + Y(0.008), cx + X(sx) + X(0.027),
               cy + Y(0.068)], start=0, end=180, fill=RED, width=5)
    d.rectangle([X(0.225), Y(0.315), X(0.775), Y(0.375)], fill=(210, 214, 218),
                outline=(120, 128, 138), width=2)                          # entablature
    d.rectangle([X(0.24), Y(0.375), X(0.76), Y(0.795)], fill=(188, 196, 204))
    for cxf in (0.295, 0.395, 0.50, 0.605, 0.705):
        d.rectangle([X(cxf - 0.023), Y(0.40), X(cxf + 0.023), Y(0.78)],
                    fill=(244, 240, 230), outline=(120, 128, 138), width=2)
        d.rectangle([X(cxf - 0.030), Y(0.375), X(cxf + 0.030), Y(0.405)],
                    fill=(244, 240, 230), outline=(120, 128, 138), width=2)
    d.rectangle([X(0.472), Y(0.64), X(0.528), Y(0.795)], fill=(70, 76, 84))  # door
    d.rectangle([X(0.22), Y(0.795), X(0.78), Y(0.845)], fill=(172, 178, 186))
    d.rectangle([X(0.19), Y(0.845), X(0.81), Y(0.885)], fill=(160, 166, 174))
    return finish_scene(img, w, h)


def sc_cop31(w, h):
    img, d = make_scene(w, h, (210, 226, 232))
    X, Y = FX(w), FX(h)
    for i in range(8):                                                     # sun rays
        ang = i * math.pi / 4 + 0.2
        d.line([X(0.865) + 62 * math.cos(ang), Y(0.20) + 62 * math.sin(ang),
                X(0.865) + 84 * math.cos(ang), Y(0.20) + 84 * math.sin(ang)],
               fill=(240, 150, 50), width=6)
    d.ellipse([X(0.865) - 42, Y(0.20) - 42, X(0.865) + 42, Y(0.20) + 42],
              fill=(248, 178, 64))
    # globe with circular mask
    gr = 92
    globe = Image.new("RGB", (gr * 2, gr * 2), (64, 118, 178))
    gd = ImageDraw.Draw(globe)
    green, tan = (96, 164, 96), (206, 186, 120)
    gd.ellipse([18, 38, 78, 82], fill=green)                                # N America
    gd.polygon([(58, 84), (84, 84), (74, 132), (56, 116)], fill=green)     # S America
    gd.ellipse([92, 62, 128, 122], fill=green)                              # Africa
    gd.ellipse([96, 34, 126, 56], fill=tan)                                 # Europe
    gd.polygon([(126, 30), (176, 44), (162, 84), (128, 66)], fill=green)   # Asia
    gd.ellipse([140, 118, 170, 136], fill=tan)                              # Australia
    gd.ellipse([52, 2, 132, 22], fill=(240, 246, 250))                      # ice cap
    mask = Image.new("L", (gr * 2, gr * 2), 0)
    ImageDraw.Draw(mask).ellipse([0, 0, gr * 2, gr * 2], fill=255)
    img.paste(globe, (int(X(0.35) - gr), int(Y(0.54) - gr)), mask)
    d.ellipse([X(0.35) - gr, Y(0.54) - gr, X(0.35) + gr, Y(0.54) + gr],
              outline=(30, 60, 92), width=3)
    # thermometer
    d.rounded_rectangle([X(0.678), Y(0.13), X(0.722), Y(0.72)], radius=16,
                        fill=(248, 248, 246), outline=INK, width=4)
    d.rectangle([X(0.692), Y(0.28), X(0.708), Y(0.80)], fill=RED)
    d.ellipse([X(0.70) - 30, Y(0.80) - 30, X(0.70) + 30, Y(0.80) + 30],
              fill=RED, outline=INK, width=4)
    for ty in (0.24, 0.38, 0.52):
        d.line([X(0.735), Y(ty), X(0.765), Y(ty)], fill=INK, width=4)
    return finish_scene(img, w, h)


def sc_voyager(w, h):
    img, d = make_scene(w, h, (10, 14, 34))
    X, Y = FX(w), FX(h)
    rng = random.Random(11)
    for _ in range(80):
        sx, sy = rng.uniform(0, w * SS), rng.uniform(0, h * SS)
        r = rng.choice([1.6, 2.2, 3.0])
        col = (255, 255, 255) if rng.random() > 0.3 else (178, 198, 255)
        d.ellipse([sx - r, sy - r, sx + r, sy + r], fill=col)
    # dashed path from probe to Earth
    p0, p1, p2 = (X(0.33), Y(0.46)), (X(0.62), Y(0.16)), (X(0.885), Y(0.27))
    prev = None
    for i in range(41):
        t = i / 40
        bx = (1 - t) ** 2 * p0[0] + 2 * (1 - t) * t * p1[0] + t ** 2 * p2[0]
        by = (1 - t) ** 2 * p0[1] + 2 * (1 - t) * t * p1[1] + t ** 2 * p2[1]
        if prev and i % 3:
            d.line([prev[0], prev[1], bx, by], fill=(140, 170, 220), width=3)
        prev = (bx, by)
    d.ellipse([X(0.885) - 17, Y(0.27) - 17, X(0.885) + 17, Y(0.27) + 17],
              fill=(84, 140, 220))                                          # Earth
    d.ellipse([X(0.885) - 6, Y(0.27) - 10, X(0.885) + 8, Y(0.27) + 2],
              fill=(96, 190, 130))
    # probe: bus, booms, big dish
    d.line([X(0.225), Y(0.60), X(0.055), Y(0.86)], fill=(130, 130, 138), width=7)
    for t in (0.3, 0.55, 0.8):
        bx = X(0.225) + (X(0.055) - X(0.225)) * t
        by = Y(0.60) + (Y(0.86) - Y(0.60)) * t
        d.line([bx - 9, by, bx + 9, by], fill=(150, 150, 158), width=5)
    d.line([X(0.30), Y(0.62), X(0.60), Y(0.90)], fill=(178, 182, 190), width=3)
    d.rectangle([X(0.175), Y(0.575), X(0.265), Y(0.715)], fill=(186, 158, 92),
                outline=(240, 226, 180), width=3)                           # bus
    d.ellipse([X(0.30) - 100, Y(0.50) - 76, X(0.30) + 100, Y(0.50) + 76],
              fill=(226, 228, 230), outline=(16, 18, 26), width=4)          # dish
    d.ellipse([X(0.30) - 62, Y(0.50) - 46, X(0.30) + 62, Y(0.50) + 46],
              outline=(168, 172, 180), width=4)
    d.line([X(0.30), Y(0.50), X(0.415), Y(0.315)], fill=(52, 56, 64), width=6)
    d.rectangle([X(0.405), Y(0.29), X(0.435), Y(0.335)], fill=(52, 56, 64))
    return finish_scene(img, w, h)


def sc_gta(w, h):
    img, d = make_scene(w, h, (40, 34, 70))
    X, Y = FX(w), FX(h)
    d.rectangle([0, Y(0.30), X(1), Y(0.52)], fill=(104, 46, 92))
    d.rectangle([0, Y(0.52), X(1), Y(0.66)], fill=(198, 86, 88))
    d.rectangle([0, Y(0.60), X(1), Y(0.66)], fill=(244, 146, 84))
    d.ellipse([X(0.50) - 38, Y(0.66) - 38, X(0.50) + 38, Y(0.66) + 38],
              fill=(252, 196, 100))                                         # sun
    sil = (30, 24, 46)
    for bx, bw, bh in [(0.0, 0.10, 0.42), (0.09, 0.07, 0.30), (0.85, 0.06, 0.36),
                       (0.90, 0.10, 0.46)]:
        d.rectangle([X(bx), Y(0.66 - bh), X(bx + bw), Y(0.66)], fill=sil)
    rng = random.Random(3)
    for bx, bw, bh in [(0.0, 0.10, 0.42), (0.09, 0.07, 0.30), (0.85, 0.06, 0.36),
                       (0.90, 0.10, 0.46)]:
        for _ in range(4):
            wx = bx + rng.uniform(0.01, bw - 0.02)
            wy = 0.66 - bh + rng.uniform(0.03, bh - 0.05)
            col = (255, 110, 190) if rng.random() > 0.5 else (110, 230, 255)
            d.rectangle([X(wx), Y(wy), X(wx + 0.010), Y(wy + 0.035)], fill=col)
    def palm(cx, scale=1.0):
        base_y, top_y = Y(0.99), Y(0.66 - 0.30 * scale)
        pts = [(X(cx) + (X(cx + 0.022 * scale) - X(cx)) * t +
                10 * math.sin(t * 2.2) * scale, base_y + (top_y - base_y) * t)
               for t in (0, 0.25, 0.5, 0.75, 1.0)]
        d.line(pts, fill=(20, 16, 30), width=int(11 * scale), joint="curve")
        tx, ty = pts[-1]
        for ang in (-160, -115, -70, -25, 15):
            ex = tx + math.cos(math.radians(ang)) * 52 * scale
            ey = ty + math.sin(math.radians(ang)) * 26 * scale + 12 * scale
            mx = tx + math.cos(math.radians(ang)) * 28 * scale
            my = ty + math.sin(math.radians(ang)) * 22 * scale - 6 * scale
            d.line([(tx, ty), (mx, my), (ex, ey)], fill=(20, 16, 30),
                   width=int(7 * scale), joint="curve")
    palm(0.085, 1.0)
    palm(0.925, 1.0)
    palm(0.175, 0.62)
    d.polygon([(X(0.335), Y(0.66)), (X(0.665), Y(0.66)), (X(1), Y(1)), (0, Y(1))],
              fill=(26, 22, 38))                                            # road
    d.line([X(0.335), Y(0.66), 0, Y(1)], fill=(255, 110, 190), width=4)
    d.line([X(0.665), Y(0.66), X(1), Y(1)], fill=(110, 230, 255), width=4)
    for yy, ww in [(0.845, 0.007), (0.905, 0.011), (0.965, 0.016)]:
        d.polygon([(X(0.5 - ww), Y(yy)), (X(0.5 + ww), Y(yy)),
                   (X(0.5 + ww * 1.3), Y(yy + 0.028)), (X(0.5 - ww * 1.3), Y(yy + 0.028))],
                  fill=(250, 230, 170))
    # sports car, side profile facing right
    body = [(0.315, 0.90), (0.310, 0.765), (0.350, 0.745), (0.420, 0.605),
            (0.520, 0.588), (0.575, 0.735), (0.675, 0.79), (0.688, 0.90)]
    d.line([X(0.315), Y(0.955), X(0.688), Y(0.955)], fill=(205, 70, 150), width=9)
    d.line([X(0.315), Y(0.955), X(0.688), Y(0.955)], fill=(255, 140, 210), width=3)
    d.polygon([(X(a), Y(b)) for a, b in body], fill=(13, 11, 22))
    win = [(0.435, 0.72), (0.465, 0.618), (0.515, 0.608), (0.550, 0.72)]
    d.polygon([(X(a), Y(b)) for a, b in win], fill=(96, 150, 180))
    for wx in (0.375, 0.615):
        d.ellipse([X(wx) - 27, Y(0.905) - 27, X(wx) + 27, Y(0.905) + 27],
                  fill=(8, 8, 12), outline=(110, 230, 255), width=5)
    d.rectangle([X(0.310), Y(0.79), X(0.322), Y(0.815)], fill=(255, 60, 60))
    return finish_scene(img, w, h)


def sc_quake(w, h):
    img, d = make_scene(w, h, (206, 220, 228))
    X, Y = FX(w), FX(h)
    rng = random.Random(5)
    towers = [(0.02, 0.10, 0.52, (104, 116, 128)), (0.13, 0.08, 0.66, (172, 120, 88)),
              (0.22, 0.11, 0.44, (120, 132, 144)), (0.34, 0.09, 0.74, (96, 108, 122)),
              (0.44, 0.12, 0.56, (178, 164, 132)), (0.57, 0.08, 0.68, (110, 124, 138)),
              (0.66, 0.10, 0.48, (164, 110, 84)), (0.77, 0.09, 0.62, (100, 114, 128)),
              (0.87, 0.11, 0.54, (126, 138, 150))]
    for bx, bw, bh, col in towers:
        d.rectangle([X(bx), Y(0.82 - bh), X(bx + bw), Y(0.82)], fill=col)
        rows = int(bh / 0.11)
        for r in range(rows):
            for c in range(int(bw / 0.028)):
                if rng.random() > 0.35:
                    wx = bx + 0.012 + c * 0.028
                    wy = 0.82 - bh + 0.045 + r * 0.11
                    d.rectangle([X(wx), Y(wy), X(wx + 0.014), Y(wy + 0.05)],
                                fill=(62, 68, 78))
    d.rectangle([0, Y(0.82), X(1), Y(1)], fill=(74, 66, 58))               # ground
    crack = [(0.0, 0.905), (0.10, 0.868), (0.20, 0.928), (0.31, 0.878),
             (0.42, 0.918), (0.52, 0.872), (0.63, 0.93), (0.74, 0.885),
             (0.85, 0.918), (0.93, 0.878), (1.0, 0.908)]
    d.line([(X(a), Y(b)) for a, b in crack], fill=(226, 74, 38), width=7,
           joint="curve")
    branch = [(0.47, 0.90), (0.495, 0.862), (0.478, 0.83), (0.50, 0.80)]
    d.line([(X(a), Y(b)) for a, b in branch], fill=(226, 74, 38), width=5,
           joint="curve")
    d.arc([X(0.245), Y(0.02), X(0.315), Y(0.16)], start=250, end=60,
          fill=(90, 96, 104), width=5)                                     # shake arcs
    d.arc([X(0.665), Y(0.06), X(0.735), Y(0.20)], start=120, end=290,
          fill=(90, 96, 104), width=5)
    return finish_scene(img, w, h)


# ------------------------------------------------------------ lead scene
def sc_lead(w, h):
    """Summit scene at 2x: Shenzhen skyline, three flag poles, long table.
    Text (captions, names) is drawn later on the main canvas."""
    img, d = make_scene(w, h, NAVY)
    X, Y = FX(w), FX(h)
    rng = random.Random(9)
    # skyline silhouette along the bottom, behind the table
    sil = (13, 25, 43)
    blocks = [(0.00, 0.09, 0.115), (0.08, 0.07, 0.17), (0.14, 0.10, 0.095),
              (0.23, 0.06, 0.145), (0.285, 0.09, 0.11), (0.365, 0.07, 0.185),
              (0.425, 0.10, 0.085), (0.515, 0.06, 0.13), (0.565, 0.09, 0.10),
              (0.735, 0.07, 0.16), (0.795, 0.10, 0.095), (0.885, 0.06, 0.135),
              (0.935, 0.065, 0.11)]
    for bx, bw, bh in blocks:
        d.rectangle([X(bx), Y(0.795 - bh), X(bx + bw), Y(0.795)], fill=sil)
    # tapered tower (Ping An-like) with a spire, in the gap between names
    d.polygon([(X(0.70), Y(0.795)), (X(0.708), Y(0.50)), (X(0.732), Y(0.50)),
               (X(0.74), Y(0.795))], fill=sil)
    d.line([X(0.72), Y(0.50), X(0.72), Y(0.445)], fill=sil, width=5)
    for bx, bw, bh in blocks:
        for _ in range(rng.randint(1, 3)):
            wx = bx + rng.uniform(0.008, bw - 0.016)
            wy = 0.795 - bh + rng.uniform(0.015, bh - 0.03)
            d.rectangle([X(wx), Y(wy), X(wx + 0.009), Y(wy + 0.02)],
                        fill=(240, 230, 190))
    # long summit table
    d.rectangle([X(0.06), Y(0.795), X(0.94), Y(0.858)], fill=(166, 128, 84))
    d.line([X(0.06), Y(0.795), X(0.94), Y(0.795)], fill=(198, 160, 106), width=5)
    d.rectangle([X(0.06), Y(0.858), X(0.94), Y(0.872)], fill=(120, 90, 58))
    # flag poles + flags
    poles = [0.215, 0.50, 0.785]
    for px in poles:
        d.line([X(px), Y(0.27), X(px), Y(0.795)], fill=(226, 222, 210), width=6)
        d.ellipse([X(px) - 7, Y(0.27) - 7, X(px) + 7, Y(0.27) + 7],
                  fill=(232, 184, 76))
    FW_, FH_ = 0.225, 0.20
    # USA
    fx, fy = X(poles[0]), Y(0.275)
    fw, fh = X(FW_), Y(FH_)
    d.rectangle([fx, fy, fx + fw, fy + fh], fill=(255, 255, 255))
    for i in range(7):
        yy = fy + i * (fh / 13) * 2
        d.rectangle([fx, yy, fx + fw, yy + fh / 13], fill=(178, 34, 52))
    d.rectangle([fx, fy, fx + fw * 0.44, fy + fh * 7 / 13], fill=(60, 59, 110))
    for r in range(4):
        for c in range(5):
            star(d, fx + 12 + c * (fw * 0.44 - 22) / 4,
                 fy + 10 + r * (fh * 7 / 13 - 18) / 3, 4.5, (255, 255, 255))
    d.rectangle([fx, fy, fx + fw, fy + fh], outline=(10, 20, 36), width=3)
    # China
    fx = X(poles[1])
    d.rectangle([fx, fy, fx + fw, fy + fh], fill=(222, 41, 16))
    star(d, fx + fw * 0.20, fy + fh * 0.30, fh * 0.21, (255, 222, 0))
    for dx, dy in [(0.44, 0.10), (0.50, 0.26), (0.50, 0.44), (0.44, 0.60)]:
        star(d, fx + fw * dx, fy + fh * dy, fh * 0.075, (255, 222, 0))
    d.rectangle([fx, fy, fx + fw, fy + fh], outline=(10, 20, 36), width=3)
    # Russia
    fx = X(poles[2])
    d.rectangle([fx, fy, fx + fw, fy + fh / 3], fill=(255, 255, 255))
    d.rectangle([fx, fy + fh / 3, fx + fw, fy + 2 * fh / 3], fill=(0, 57, 166))
    d.rectangle([fx, fy + 2 * fh / 3, fx + fw, fy + fh], fill=(213, 43, 30))
    d.rectangle([fx, fy, fx + fw, fy + fh], outline=(10, 20, 36), width=3)
    return finish_scene(img, w, h)


# ------------------------------------------------------------ page
img = Image.new("RGB", (S, S), PAPER)
d = ImageDraw.Draw(img)
M = 40
CW = S - 2 * M

# masthead
d.rectangle([0, 0, S, 8], fill=INK)
y = 14
tracked_center(d, S / 2, y, "THE WORLD IN ONE DAY", f_serif(42), INK, tracking=6)
y += 58
tracked_center(d, S / 2, y, "ONE IMAGE · THE DAY'S ESSENTIAL NEWS",
               f_bold(13), MUTED, tracking=4)
y += 26
d.line([M, y, S - M, y], fill=INK, width=3)
d.line([M, y + 5, S - M, y + 5], fill=INK, width=1)

# date band
y += 14
tracked_center(d, S / 2, y, "THURSDAY, 19 NOVEMBER 2026", f_black(44), INK,
               tracking=2)
y += 58
d.line([M, y, S - M, y], fill=INK, width=3)

# lead story
lead_y = y + 12
LEAD_H = 194
PANEL_W = 430
img.paste(sc_lead(PANEL_W, LEAD_H), (M, lead_y))
tracked_center(d, M + PANEL_W / 2, lead_y + 12, "THREE PRESIDENTS · ONE TABLE",
               f_bold(13), CREAM, tracking=3)
for frac, name in [(0.215 + 0.1125, "TRUMP"), (0.50 + 0.1125, "XI JINPING"),
                   (0.785 + 0.1125, "PUTIN")]:
    tracked_center(d, M + PANEL_W * frac, lead_y + 98, name, f_bold(13),
                   CREAM, tracking=2)
tracked_center(d, M + PANEL_W / 2, lead_y + LEAD_H - 24,
               "APEC SUMMIT — SHENZHEN, CHINA", f_bold(12), CREAM, tracking=2)

tx = M + PANEL_W + 24
tw = S - M - tx
tracked(d, (tx, lead_y), "LEAD STORY", f_bold(15), RED, tracking=4)
hy = lead_y + 24
head_f = f_black(33)
for line in wrap(d, "Trump, Xi & Putin Hold First-Ever Trilateral Summit",
                 head_f, tw):
    d.text((tx, hy), line, font=head_f, fill=INK)
    hy += 39
hy += 4
sub_f = f_reg(17)
for line in wrap(d, "Nuclear arms control, Ukraine and Iran top the agenda "
                    "at the APEC summit in Shenzhen.", sub_f, tw):
    d.text((tx, hy), line, font=sub_f, fill=SUB)
    hy += 22
assert hy <= lead_y + LEAD_H + 4, f"lead text overflows: {hy} vs {lead_y + LEAD_H}"

grid_top = lead_y + LEAD_H + 18
d.line([M, grid_top - 9, S - M, grid_top - 9], fill=INK, width=3)

# tiles
TILES = [
    ("STRAIT OF HORMUZ", sc_hormuz,
     "Tankers Ablaze in the Strait of Hormuz",
     "Iran says 3 hit mines; US struck Qeshm"),
    ("GAZA", sc_gaza,
     "Israel Launches Ground Operation in Central Gaza",
     "Calls grow to let aid reach flooded Gaza"),
    ("CRIMEA", sc_bridge,
     "Ukraine Strikes the Crimean Bridge Again",
     "Bridge linking Russia with Crimea hit"),
    ("HORN OF AFRICA", sc_horn,
     "Ethiopia–Eritrea Clashes Raise Fears of War",
     "Border fighting threatens a wider war"),
    ("THE HAGUE", sc_court,
     "World Court Rules on Myanmar Genocide Case",
     "Rohingya judgment at The Hague"),
    ("ANTALYA, TÜRKIYE", sc_cop31,
     "COP31 Talks Stall Over Climate Finance",
     "Final days in Antalya, Türkiye"),
    ("DEEP SPACE", sc_voyager,
     "Voyager 1 Is Now One Light-Day From Earth",
     "NASA's farthest probe, 26 billion km out"),
    ("WORLDWIDE", sc_gta,
     "GTA VI Launches After a 13-Year Wait",
     "Rockstar's sequel lands to rave reviews"),
    ("KUMAMOTO, JAPAN", sc_quake,
     "Magnitude 5.7 Quake Jolts Kumamoto",
     "No tsunami warning issued"),
]

COLS, ROWS = 3, 3
GUT = 26
tile_w = int((CW - (COLS - 1) * GUT) / COLS)
SCENE_H = 58
tile_h = 150
ROW_GAP = 8
tag_f = f_bold(12)
tile_head_f = f_bold(19)

for idx, (loc, scene_fn, head, sub) in enumerate(TILES):
    r, c = divmod(idx, COLS)
    x0 = M + c * (tile_w + GUT)
    y0 = grid_top + r * (tile_h + ROW_GAP)
    img.paste(scene_fn(tile_w, SCENE_H), (x0, y0))
    d.rectangle([x0, y0, x0 + tile_w - 1, y0 + SCENE_H - 1], outline=INK, width=2)
    tracked(d, (x0 + 1, y0 + SCENE_H + 7), loc, tag_f, RED, tracking=2)
    hy = y0 + SCENE_H + 26
    head_lines = wrap(d, head, tile_head_f, tile_w)
    assert len(head_lines) <= 2, f"headline wraps to {len(head_lines)}: {head}"
    for line in head_lines:
        d.text((x0, hy), line, font=tile_head_f, fill=INK)
        hy += 23
    size = 14
    while size > 11 and d.textlength(sub, font=f_reg(size)) > tile_w:
        size -= 1
    sub_lines = wrap(d, sub, f_reg(size), tile_w)
    assert len(sub_lines) == 1, f"sub wraps: {sub}"
    d.text((x0, y0 + tile_h - 19), sub_lines[0], font=f_reg(size), fill=MUTED)

grid_bottom = grid_top + ROWS * tile_h + (ROWS - 1) * ROW_GAP

# ticker
tick_y = grid_bottom + 14
d.rectangle([0, tick_y, S, tick_y + 56], fill=INK)
tracked_center(d, S / 2, tick_y + 7,
               "ALSO TODAY — VAN GOGH SELLS FOR A RECORD $190.4M",
               f_bold(15), CREAM, tracking=1)
tracked_center(d, S / 2, tick_y + 32,
               "JEFFRIES SET TO BE FIRST BLACK US HOUSE SPEAKER · PEW: "
               "MUSLIMS TO OUTNUMBER CHRISTIANS BY 2035",
               f_reg(13), (206, 198, 182), tracking=1)
d.text((S / 2, tick_y + 68), "Compiled from the day's reporting",
       font=f_reg(12), fill=MUTED, anchor="ma")

img.save(OUT, optimize=True)
print("wrote", OUT, img.size, os.path.getsize(OUT), "bytes")
