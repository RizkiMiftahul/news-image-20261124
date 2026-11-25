#!/usr/bin/env python3
"""Render v2 of the front page summing up Tuesday 24 November 2026.

Improvements over v1: far larger type so every headline stays legible when
the page is shrunk to ~300px, a dominant lead panel, four secondary panels
in a 2x2 grid with one short headline and one detail line each, and a
footer strip carrying the remaining stories. Geometry is budgeted to the
1024px page: masthead 148, lead 330, grid 2x218+10, footer ~78.
Deterministic: fixed geometry, vendored fonts, no clocks, no randomness.
"""
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parent
W = H = 1024
PAPER = (247, 243, 234)
INK = (26, 26, 26)
RED = (178, 32, 42)
SEA = (46, 96, 148)
SKY = (196, 220, 240)
WHITE = (255, 255, 255)
GREY = (90, 90, 90)

SERIF = "DejaVuSerif-Bold.ttf"
SANSB = "DejaVuSans-Bold.ttf"
SANS = "DejaVuSans.ttf"


def font(name, size):
    return ImageFont.truetype(str(ROOT / "fonts" / name), size)


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


def block(draw, x, y, text, fnt, fill, max_w, leading=1.1):
    for line in wrap(draw, text, fnt, max_w):
        draw.text((x, y), line, font=fnt, fill=fill)
        y += int(fnt.size * leading)
    return y


# ---------------------------------------------------------------- scenes
def scene_lead(w, h):
    """Sea, a warship, a naval drone and an explosion."""
    im = Image.new("RGB", (w, h), SKY)
    d = ImageDraw.Draw(im)
    d.rectangle([0, h * 0.42, w, h], fill=SEA)
    for i in range(6):
        y = int(h * 0.55 + i * h * 0.08)
        d.line([0, y, w, y], fill=(90, 140, 185), width=3)
    d.polygon([(w * 0.52, h * 0.50), (w * 0.94, h * 0.44), (w * 0.90, h * 0.62),
               (w * 0.56, h * 0.66)], fill=(70, 74, 82))
    d.rectangle([w * 0.64, h * 0.32, w * 0.78, h * 0.48], fill=(88, 92, 102))
    d.rectangle([w * 0.70, h * 0.22, w * 0.74, h * 0.32], fill=(88, 92, 102))
    for r, c in [(40, (255, 140, 40)), (28, (255, 190, 60)), (17, (255, 230, 150))]:
        d.ellipse([w * 0.585 - r, h * 0.52 - r, w * 0.585 + r, h * 0.52 + r], fill=c)
    for i, r in enumerate([20, 28, 38]):
        cx, cy = w * 0.585 + i * 22, h * 0.36 - i * 22
        d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(105, 105, 110))
    d.polygon([(w * 0.10, h * 0.68), (w * 0.30, h * 0.63), (w * 0.34, h * 0.72),
               (w * 0.14, h * 0.76)], fill=(30, 34, 40))
    d.polygon([(w * 0.30, h * 0.63), (w * 0.40, h * 0.58), (w * 0.34, h * 0.72)], fill=(30, 34, 40))
    for i in range(3):
        d.line([w * 0.02, h * (0.76 + i * 0.06), w * 0.15, h * (0.74 + i * 0.06)],
               fill=(220, 235, 245), width=3)
    return im


def scene_chip(w, h):
    im = Image.new("RGB", (w, h), (16, 42, 74))
    d = ImageDraw.Draw(im)
    d.rectangle([w * 0.30, h * 0.14, w * 0.70, h * 0.86], fill=(30, 120, 70), outline=(220, 230, 220), width=4)
    for i in range(5):
        yy = h * (0.24 + i * 0.13)
        d.line([w * 0.30, yy, w * 0.16, yy], fill=(230, 200, 90), width=4)
        d.line([w * 0.70, yy, w * 0.84, yy], fill=(230, 200, 90), width=4)
    d.rectangle([w * 0.41, h * 0.32, w * 0.59, h * 0.68], fill=(12, 60, 34))
    d.text((w * 0.5, h * 0.5), "AI", font=font(SANSB, 38), fill=WHITE, anchor="mm")
    d.polygon([(w * 0.84, h * 0.78), (w * 0.92, h * 0.44), (w * 0.97, h * 0.78)], fill=(60, 200, 110))
    return im


def scene_building(w, h):
    im = Image.new("RGB", (w, h), (64, 58, 66))
    d = ImageDraw.Draw(im)
    d.rectangle([w * 0.20, h * 0.06, w * 0.80, h * 0.94], fill=(120, 112, 108))
    for r in range(4):
        for c in range(4):
            x, y = w * (0.25 + c * 0.13), h * (0.14 + r * 0.20)
            d.rectangle([x, y, x + w * 0.085, y + h * 0.12], fill=(240, 200, 90))
    d.ellipse([w * 0.40, h * 0.36, w * 0.64, h * 0.68], fill=(28, 26, 28))
    d.polygon([(0, h), (w * 0.3, h * 0.82), (w * 0.55, h)], fill=(96, 90, 88))
    d.polygon([(w * 0.55, h), (w * 0.8, h * 0.86), (w, h)], fill=(96, 90, 88))
    for i, r in enumerate([15, 22, 32]):
        cx, cy = w * 0.52 + i * 24, h * 0.30 - i * 20
        d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(140, 138, 140))
    return im


def scene_jet(w, h):
    im = Image.new("RGB", (w, h), (150, 178, 205))
    d = ImageDraw.Draw(im)
    d.rectangle([0, h * 0.80, w, h], fill=(168, 148, 118))
    d.polygon([(w * 0.12, h * 0.32), (w * 0.62, h * 0.24), (w * 0.88, h * 0.34),
               (w * 0.60, h * 0.40), (w * 0.30, h * 0.42)], fill=(40, 44, 52))
    d.polygon([(w * 0.40, h * 0.40), (w * 0.52, h * 0.56), (w * 0.62, h * 0.40)], fill=(40, 44, 52))
    d.polygon([(w * 0.14, h * 0.32), (w * 0.08, h * 0.18), (w * 0.24, h * 0.26)], fill=(40, 44, 52))
    for bx in (0.24, 0.52, 0.76):
        for i, r in enumerate([13, 21, 31]):
            cx, cy = w * bx + i * 7, h * 0.72 - i * 28
            d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(110, 108, 106))
        d.rectangle([w * bx - 5, h * 0.70, w * bx + 5, h * 0.82], fill=(255, 150, 50))
    return im


def scene_tanker(w, h):
    im = Image.new("RGB", (w, h), SEA)
    d = ImageDraw.Draw(im)
    for i in range(6):
        y = int(h * 0.12 + i * h * 0.15)
        d.line([0, y, w, y], fill=(90, 140, 185), width=3)
    d.polygon([(w * 0.08, h * 0.50), (w * 0.88, h * 0.50), (w * 0.82, h * 0.68),
               (w * 0.14, h * 0.68)], fill=(150, 52, 44))
    d.rectangle([w * 0.14, h * 0.38, w * 0.74, h * 0.50], fill=(196, 190, 182))
    for i in range(4):
        x = w * (0.18 + i * 0.14)
        d.ellipse([x, h * 0.38, x + w * 0.10, h * 0.50], fill=(170, 164, 156))
    d.rectangle([w * 0.76, h * 0.24, w * 0.84, h * 0.50], fill=(90, 92, 98))
    cx, cy, r = w * 0.88, h * 0.84, 20
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(24, 26, 30))
    for dx, dy in [(-24, 0), (24, 0), (0, -24), (0, 24), (-17, -17), (17, -17), (-17, 17), (17, 17)]:
        d.line([cx, cy, cx + dx, cy + dy], fill=(24, 26, 30), width=5)
    return im


# ---------------------------------------------------------------- layout
def panel(page, x, y, w, h, scene, kick, head, sub):
    page.paste(scene(w, 86), (x, y))
    d = ImageDraw.Draw(page)
    d.rectangle([x, y, x + w, y + h], outline=INK, width=3)
    ty = y + 94
    d.text((x + 14, ty), kick, font=font(SANSB, 25), fill=RED)
    ty += 31
    ty = block(d, x + 14, ty, head, font(SANSB, 29), INK, w - 28, 1.08)
    block(d, x + 14, ty + 3, sub, font(SANS, 20), GREY, w - 28, 1.1)


def main():
    page = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(page)

    # masthead (0..148)
    d.text((W // 2, 14), "THE WORLD IN ONE IMAGE", font=font(SERIF, 56),
           fill=INK, anchor="ma")
    d.rectangle([0, 86, W, 140], fill=INK)
    d.text((W // 2, 97), "TUESDAY  ·  24 NOVEMBER 2026", font=font(SANSB, 33),
           fill=WHITE, anchor="ma")

    # lead story (148..448)
    lx, ly, lw = 24, 148, W - 48
    page.paste(scene_lead(lw, 115), (lx, ly))
    d = ImageDraw.Draw(page)
    d.rectangle([lx, ly, lx + lw, ly + 308], outline=INK, width=4)
    ty = ly + 120
    d.text((lx + 18, ty), "BENGHAZI, LIBYA — WAR AT SEA", font=font(SANSB, 29), fill=RED)
    ty += 36
    ty = block(d, lx + 18, ty, "UKRAINE'S NAVAL DRONES SINK RUSSIAN WARSHIP",
               font(SANSB, 42), INK, lw - 36, 1.06)
    block(d, lx + 18, ty + 4,
          "Sea drones strike a Russian warship at its Libyan base; the UN mission demands a probe.",
          font(SANS, 24), GREY, lw - 36, 1.1)

    # 2x2 secondary grid (458..934)
    gx, gy, gw, gh, gap = 24, 464, 482, 234, 10
    panel(page, gx, gy, gw, gh, scene_chip, "SANTA CLARA — TECH",
          "HUANG BACK AT NVIDIA",
          "Back as CEO after Trump's push; shares jump about 30%, Senate vows inquiry.")
    panel(page, gx + gw + gap, gy, gw, gh, scene_building, "ZAPORIZHZHIA — UKRAINE",
          "STRIKE HITS APARTMENT BLOCK",
          "Overnight strike: 2 dead, 40 wounded.")
    panel(page, gx, gy + gh + gap, gw, gh, scene_jet, "GAZA — MIDDLE EAST",
          "ISRAEL KILLS HAMAS CHIEF",
          "Airstrikes kill Hamas security chief, 5 others.")
    panel(page, gx + gw + gap, gy + gh + gap, gw, gh, scene_tanker, "STRAIT OF HORMUZ",
          "TANKERS HIT SEA MINES",
          "Tankers strike mines as Iran defies the US naval blockade.")

    # footer strip (944..1008)
    fy = 950
    d = ImageDraw.Draw(page)
    d.line([24, fy, W - 24, fy], fill=INK, width=3)
    d.text((24, fy + 10), "ALSO TODAY:", font=font(SANSB, 23), fill=RED)
    block(d, 208, fy + 10,
          "COP31 talks collapse, no fossil-fuel deal  ·  UAE bus crash kills 13  ·  States sue SpaceX over Grok  ·  UK hosts 2035 Women's World Cup",
          font(SANS, 23), INK, W - 232, 1.15)

    out = ROOT / "assets" / "entry.png"
    page.save(out, format="PNG", optimize=True)
    print(f"wrote {out} ({out.stat().st_size} bytes)")


if __name__ == "__main__":
    main()
