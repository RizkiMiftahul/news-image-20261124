#!/usr/bin/env python3
"""Render the front page that sums up the world news of Tuesday 24 November 2026.

Draws one 1024x1024 editorial page with PIL: a masthead naming the day, one
lead story (Ukrainian naval drones sinking a Russian warship off Libya) and
six secondary stories plus a footer strip. Each scene is drawn on its own
sub-image and pasted in, so nothing bleeds across panels. Deterministic:
fixed geometry, vendored fonts, no clocks, no randomness.
"""
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parent
W = H = 1024
PAPER = (247, 243, 234)
INK = (26, 26, 26)
RED = (178, 32, 42)
SEA = (58, 110, 160)
WHITE = (255, 255, 255)


def font(name, size):
    return ImageFont.truetype(str(ROOT / "fonts" / name), size)


SERIF = "DejaVuSerif-Bold.ttf"
SANSB = "DejaVuSans-Bold.ttf"
SANS = "DejaVuSans.ttf"


def wrap(draw, text, fnt, max_w):
    words, lines, cur = text.split(), [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if draw.textlength(t, font=fnt) <= max_w:
            cur = t
        else:
            lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def text_block(draw, x, y, text, fnt, fill, max_w, leading=1.12):
    for line in wrap(draw, text, fnt, max_w):
        draw.text((x, y), line, font=fnt, fill=fill)
        y += int(fnt.size * leading)
    return y


def panel(draw, x, y, w, h):
    draw.rectangle([x, y, x + w, y + h], outline=INK, width=3)


def scene_canvas(w, h, bg):
    img = Image.new("RGB", (int(w), int(h)), bg)
    return img, ImageDraw.Draw(img)


# ---------------------------------------------------------------- scenes
def scene_warship(w, h):
    img, d = scene_canvas(w, h, (196, 222, 240))
    d.rectangle([0, h * 0.62, w, h], fill=SEA)
    d.text((10, 6), "BENGHAZI · LIBYA", font=font(SANSB, 17), fill=INK)
    sx, sy = w * 0.50, h * 0.50
    d.polygon([(sx, sy + 24), (sx + 180, sy + 24), (sx + 158, sy + 48), (sx + 16, sy + 48)], fill=(70, 74, 82))
    d.rectangle([sx + 38, sy - 6, sx + 112, sy + 24], fill=(86, 90, 100))
    d.rectangle([sx + 120, sy - 20, sx + 138, sy + 24], fill=(86, 90, 100))
    d.line([sx + 56, sy - 6, sx + 56, sy - 30], fill=INK, width=4)
    cx, cy = sx + 168, sy + 6
    for r, col in ((27, (240, 120, 40)), (18, (246, 178, 60)), (10, (250, 226, 130))):
        d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=col)
    for i, (dx, dy) in enumerate(((0.05, 0.72), (0.19, 0.82), (0.33, 0.70))):
        px, py = w * dx, h * dy
        d.polygon([(px, py), (px + 44, py + 6), (px + 38, py + 15), (px + 6, py + 13)], fill=(30, 34, 40))
        d.line([px - 24, py + 9, px, py + 7], fill=WHITE, width=3)
    return img


def scene_chip(w, h):
    img, d = scene_canvas(w, h, (24, 34, 54))
    cx, cy, s = w / 2, h / 2, 26
    for t in (-0.6, 0.0, 0.6):
        d.line([cx + t * s, cy - s - 9, cx + t * s, cy - s], fill=(240, 190, 60), width=4)
        d.line([cx + t * s, cy + s, cx + t * s, cy + s + 9], fill=(240, 190, 60), width=4)
        d.line([cx - s - 9, cy + t * s, cx - s, cy + t * s], fill=(240, 190, 60), width=4)
        d.line([cx + s, cy + t * s, cx + s + 9, cy + t * s], fill=(240, 190, 60), width=4)
    d.rectangle([cx - s, cy - s, cx + s, cy + s], fill=(52, 120, 200), outline=WHITE, width=2)
    d.text((cx, cy - 13), "AI", font=font(SANSB, 24), fill=WHITE, anchor="ma")
    return img


def scene_building(w, h):
    img, d = scene_canvas(w, h, (226, 205, 178))
    bx, by, bw, bh = w * 0.32, h * 0.16, w * 0.40, h * 0.80
    d.rectangle([bx, by, bx + bw, by + bh], fill=(150, 138, 122))
    for r in range(3):
        for c in range(3):
            wx, wy = bx + 10 + c * (bw - 20) / 3, by + 9 + r * (bh - 18) / 3
            d.rectangle([wx, wy, wx + 14, wy + 11], fill=(250, 226, 140))
    d.polygon([(bx + bw - 38, by), (bx + bw, by), (bx + bw, by + 30), (bx + bw - 16, by + 16)], fill=(226, 205, 178))
    d.line([bx - 8, by + bh, bx + bw + 14, by + bh], fill=(110, 96, 80), width=5)
    return img


def scene_gaza(w, h):
    img, d = scene_canvas(w, h, (214, 200, 182))
    d.rectangle([0, h * 0.68, w, h], fill=(168, 152, 128))
    for i, bx in enumerate((0.06, 0.36, 0.64)):
        bw, bh = w * 0.26, h * (0.46 - 0.08 * i)
        d.rectangle([w * bx, h * 0.68 - bh, w * bx + bw, h * 0.68], fill=(128, 116, 100))
    jx, jy = w * 0.58, h * 0.14
    d.polygon([(jx, jy), (jx + 58, jy + 9), (jx + 8, jy + 18)], fill=(60, 62, 68))
    d.line([jx - 54, jy + 22, jx + 2, jy + 12], fill=(245, 245, 245), width=4)
    d.line([jx - 40, jy + 34, jx + 8, jy + 19], fill=(245, 245, 245), width=3)
    return img


def scene_tanker(w, h):
    img, d = scene_canvas(w, h, (178, 210, 228))
    d.rectangle([0, h * 0.58, w, h], fill=SEA)
    tx, ty = w * 0.08, h * 0.36
    d.polygon([(tx, ty + 18), (tx + w * 0.60, ty + 18), (tx + w * 0.54, ty + 38), (tx + 9, ty + 38)], fill=(150, 44, 44))
    d.rectangle([tx + 14, ty, tx + w * 0.50, ty + 18], fill=(210, 210, 205))
    d.rectangle([tx + w * 0.50, ty - 12, tx + w * 0.56, ty + 18], fill=(90, 90, 90))
    mx, my = w * 0.84, h * 0.74
    d.ellipse([mx - 14, my - 14, mx + 14, my + 14], fill=(30, 30, 34))
    for dx, dy in ((0, -20), (14, -14), (20, 0), (-14, -14), (-20, 0), (0, 20)):
        d.line([mx, my, mx + dx, my + dy], fill=(30, 30, 34), width=4)
    return img


def scene_globe(w, h):
    img, d = scene_canvas(w, h, (30, 62, 96))
    cx, cy, r = w / 2, h / 2, h * 0.40
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(64, 140, 96), outline=WHITE, width=2)
    d.line([cx - r * 0.7, cy - r * 0.45, cx - r * 0.1, cy + r * 0.12, cx + r * 0.3, cy - r * 0.28,
            cx + r * 0.62, cy + r * 0.42], fill=RED, width=5)
    return img


def scene_bus(w, h):
    img, d = scene_canvas(w, h, (206, 214, 220))
    d.rectangle([0, h * 0.76, w, h], fill=(120, 122, 126))
    bx, by, bw, bh = w * 0.13, h * 0.24, w * 0.72, h * 0.44
    d.rectangle([bx, by, bx + bw, by + bh], fill=(226, 160, 44))
    for i in range(5):
        d.rectangle([bx + 10 + i * (bw - 20) / 5, by + 8, bx + 10 + (i + 0.7) * (bw - 20) / 5, by + 24], fill=(210, 232, 244))
    for wx in (bx + bw * 0.24, bx + bw * 0.76):
        d.ellipse([wx - 12, by + bh - 6, wx + 12, by + bh + 12], fill=(30, 30, 30))
    d.polygon([(bx + bw, by + 5), (bx + bw + 13, by + bh - 8), (bx + bw, by + bh - 8)], fill=(190, 60, 50))
    return img


# ---------------------------------------------------------------- page
def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    M = 36

    # masthead
    d.text((W / 2, 24), "THE WORLD IN ONE IMAGE", font=font(SERIF, 58), fill=INK, anchor="ma")
    d.line([M, 106, W - M, 106], fill=INK, width=5)
    d.line([M, 114, W - M, 114], fill=INK, width=2)
    d.rectangle([M, 124, W - M, 172], fill=INK)
    d.text((W / 2, 133), "TUESDAY  ·  24 NOVEMBER 2026", font=font(SANSB, 33), fill=WHITE, anchor="ma")

    # lead story
    ly, lh = 188, 292
    panel(d, M, ly, W - 2 * M, lh)
    img.paste(scene_warship(430, lh - 12), (M + 6, ly + 6))
    tx = M + 458
    d.text((tx, ly + 16), "LEAD STORY — EUROPE / MEDITERRANEAN", font=font(SANSB, 19), fill=RED)
    y = text_block(d, tx, ly + 48, "UKRAINE'S NAVAL DRONES SINK RUSSIAN WARSHIP OFF LIBYA",
                   font(SERIF, 37), INK, W - M - tx - 14, 1.08)
    text_block(d, tx, y + 8, "Sea drones strike a Russian vessel at the Benghazi base; "
               "the UN mission demands an investigation.",
               font(SANS, 21), INK, W - M - tx - 14, 1.18)

    # two rows of three secondary stories
    stories = [
        (scene_chip, "TECHNOLOGY",
         "HUANG RETURNS TO NVIDIA",
         "Reinstated after Trump's push; stock leaps ~30%, Senate Democrats vow an inquiry."),
        (scene_building, "UKRAINE",
         "RUSSIA HITS ZAPORIZHZHIA HOMES",
         "Overnight strike on an apartment block kills 2, wounds 40 — four of them children."),
        (scene_gaza, "MIDDLE EAST",
         "GAZA STRIKES KILL HAMAS SECURITY CHIEF",
         "Israeli jets kill internal-security director Naeem Abu Nahel and five others."),
        (scene_tanker, "ENERGY / GULF",
         "TANKERS HIT MINES IN HORMUZ",
         "Iran defies the US naval blockade and refuses talks until its conditions are met."),
        (scene_globe, "CLIMATE",
         "COP31 TALKS COLLAPSE WITH NO DEAL",
         "The climate summit ends without an agreement on phasing out fossil fuels."),
        (scene_bus, "UNITED ARAB EMIRATES",
         "BUS CRASH KILLS 13 IN RAS AL KHAIMAH",
         "Crash in the northern emirate leaves 13 dead and 14 injured."),
    ]
    col_w = (W - 2 * M - 2 * 16) // 3
    for row in range(2):
        ry = 496 + row * 212
        for col in range(3):
            scene, tag, head, body = stories[row * 3 + col]
            x = M + col * (col_w + 16)
            panel(d, x, ry, col_w, 196)
            img.paste(scene(col_w - 10, 70), (x + 5, ry + 5))
            d.text((x + 12, ry + 82), tag, font=font(SANSB, 14), fill=RED)
            y = text_block(d, x + 12, ry + 100, head, font(SANSB, 19), INK, col_w - 24, 1.08)
            text_block(d, x + 12, y + 3, body, font(SANS, 15), INK, col_w - 24, 1.14)

    # footer strip
    fy = 496 + 2 * 212 + 8
    d.rectangle([M, fy, W - M, H - 22], fill=(238, 231, 216), outline=INK, width=3)
    d.text((M + 14, fy + 7), "ALSO TODAY", font=font(SANSB, 16), fill=RED)
    text_block(d, M + 14, fy + 30,
               "Oregon & Virginia sue SpaceX over Grok's sexual images  ·  Britain wins the 2035 "
               "Women's World Cup  ·  Super Bowl LXI will screen live in IMAX cinemas  ·  Fighting "
               "in DR Congo traps Ebola teams in Ituri",
               font(SANS, 17), INK, W - 2 * M - 28, 1.18)

    out = ROOT / "assets" / "entry.png"
    img.save(out, format="PNG", optimize=True)
    print(out, out.stat().st_size, "bytes")


if __name__ == "__main__":
    main()
