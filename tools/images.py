#!/usr/bin/env python3
"""
One-time image pipeline for the Arielle Innou Coaching site.

    python3 tools/images.py <folder of original photos> <folder with Fraunces.ttf, FrauncesItalic.ttf, Manrope.ttf>

For every photo in PHOTOS it writes assets/img/<name>-1600.webp (and -800.webp when the
original is wider than 800px), records its size, placeholder colour and focal point
(fx/fy, in %) in tools/image-meta.json, and draws the social share cards (assets/img/og/)
and the favicons/logos (assets/brand/). Crops everywhere on the site centre on fx/fy,
so faces stay in frame at every screen size.
"""
import json
import math
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter, ImageFont, ImageOps

ROOT = Path(__file__).resolve().parent.parent
IMG = ROOT / "assets" / "img"
BRAND = ROOT / "assets" / "brand"

# name: (source file, crop box or None, fx %, fy %)
PHOTOS = {
    "arielle-portrait": ("Portrait-Photo-1.png", (404, 160, 1326, 1392), 50, 24),
    "arielle-seated": ("Meet-Arielle-Annou-Your-Coach.jpg", (470, 0, 1500, 1356), 40, 14),
    "arielle-garden": ("4960f532-83eb-4258-be06-22e7506dae36.jpg", None, 38, 42),
    "arielle-estate": ("3c22f92f-c1ff-4f4a-a5f9-742d04eedbaa.jpg", None, 46, 42),
    "arielle-celebration": ("IMG_5611-rotated.jpg", None, 45, 36),
    "arielle-circle": ("IMG_3653.jpg", None, 50, 34),
    "arielle-chapel": ("Arielle-Innou-Story-of-Resilience-1.jpg", None, 50, 45),
    "women-together": ("15.jpg", None, 50, 32),
    "women-joy": ("21.jpg", None, 50, 40),
    "leaders": ("25.jpg", None, 52, 28),
    "sisterhood": ("3.jpg", None, 50, 46),
    "meditation": ("About-Arielle-Innou.jpg", (0, 0, 1650, 1467), 42, 55),
    "new-chapter": ("Life-and-Relationship-Coaching-with-Arielle.jpg", None, 50, 30),
    "retreat-pavilion": ("03EE1BC7-6573-41CC-9493-75F47DCC878C.jpg", None, 50, 58),
    "retreat-statue": ("74208271-2c5c-47fd-81df-59cdc327cf60.jpg", None, 50, 45),
    "retreat-chapel": ("IMG_1589.jpg", None, 50, 45),
    "retreat-pool": ("IMG_1928.jpg", None, 50, 55),
    "retreat-path": ("IMG_2970.jpg", None, 50, 60),
    "retreat-gardens": ("IMG_7712.jpg", None, 55, 45),
    "retreat-poolside": ("IMG_8144.jpg", None, 42, 50),
    "retreat-firepit": ("d07cbffc-ea5c-4695-9287-4287a30f4060.jpg", None, 50, 55),
    "retreat-terrace": ("IMG_1928.jpg", (0, 0, 640, 480), 50, 50),
}
PHOTOS.pop("retreat-terrace")  # duplicate of retreat-pool, kept out

PLUM = (43, 26, 61)
IVORY = (247, 242, 236)
LILAC = (185, 163, 214)
MINT = (188, 227, 222)


def save_webp(im, path, q=80):
    im.save(path, "WEBP", quality=q, method=6)


def placeholder(im):
    c = im.convert("RGB").resize((1, 1), Image.LANCZOS).getpixel((0, 0))
    return "#%02x%02x%02x" % c


def process_photos(src):
    meta = {}
    for name, (file, box, fx, fy) in PHOTOS.items():
        im = Image.open(src / file)
        im = ImageOps.exif_transpose(im).convert("RGB")
        if box:
            im = im.crop(box)
        w, h = im.size
        big = im if w <= 1600 else im.resize((1600, round(h * 1600 / w)), Image.LANCZOS)
        save_webp(big, IMG / f"{name}-1600.webp", 80)
        if w > 800:
            save_webp(im.resize((800, round(h * 800 / w)), Image.LANCZOS), IMG / f"{name}-800.webp", 78)
        meta[name] = {"w": w, "h": h, "c": placeholder(im), "fx": fx, "fy": fy}
        print(f"  {name}: {w}x{h}")
    (ROOT / "tools" / "image-meta.json").write_text(json.dumps(meta, indent=1) + "\n")
    return meta


# ---------------------------------------------------------------- lotus mark
def bez(p0, p1, p2, p3, n=40):
    out = []
    for i in range(n + 1):
        t = i / n
        a = (1 - t) ** 3
        b = 3 * (1 - t) ** 2 * t
        c = 3 * (1 - t) * t ** 2
        d = t ** 3
        out.append((a * p0[0] + b * p1[0] + c * p2[0] + d * p3[0], a * p0[1] + b * p1[1] + c * p2[1] + d * p3[1]))
    return out


# Same petals as LOTUS_PATHS in tools/build.py (viewBox 0 0 64 40).
PETALS = [
    [((32, 35), (23, 26), (24, 12), (32, 2)), ((32, 2), (40, 12), (41, 26), (32, 35))],
    [((31, 35), (19, 32), (13, 21), (15, 8)), ((15, 8), (26, 12), (31.5, 22), (31, 35))],
    [((33, 35), (45, 32), (51, 21), (49, 8)), ((49, 8), (38, 12), (32.5, 22), (33, 35))],
    [((30, 36), (18, 38), (6, 32), (1, 22)), ((1, 22), (14, 19), (25, 24), (30, 36))],
    [((34, 36), (46, 38), (58, 32), (63, 22)), ((63, 22), (50, 19), (39, 24), (34, 36))],
]


def draw_lotus(draw, cx, cy, width, fill, line=None):
    """Outer petals first, centre petal last; each outlined in the background colour so they read apart."""
    s = width / 64
    for i in (3, 4, 1, 2, 0):
        pts = []
        for seg in PETALS[i]:
            pts += bez(*seg)
        draw.polygon([(cx + (x - 32) * s, cy + (y - 20) * s) for x, y in pts], fill=fill,
                     outline=line, width=max(1, round(width / 52)) if line else 0)


def icon(size, rounded=True, pad=0.2):
    k = 4  # supersample
    S = size * k
    im = Image.new("RGBA", (S, S), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    if rounded:
        d.rounded_rectangle((0, 0, S - 1, S - 1), radius=int(S * 0.22), fill=PLUM + (255,))
    else:
        d.rectangle((0, 0, S, S), fill=PLUM + (255,))
    draw_lotus(d, S / 2, S * 0.5, S * (1 - pad * 2), IVORY + (255,), PLUM + (255,))
    return im.resize((size, size), Image.LANCZOS)


def brand_files(src):
    icon(48).save(BRAND / "favicon-48.png")
    icon(180, rounded=False, pad=0.17).save(BRAND / "apple-touch-icon.png")
    icon(512, rounded=False, pad=0.2).save(BRAND / "icon-512.png")
    icon(256).save(ROOT / "favicon.ico", sizes=[(16, 16), (32, 32), (48, 48)])
    # The original logos (white for dark backgrounds, colour for light), trimmed.
    for file, out in [("Arielle-Innou-MARKWH@3x-scaled.png", "logo-white.png"), ("Arielle-Innou-Color-Logo@3x-scaled.png", "logo-color.png")]:
        im = Image.open(src / file).convert("RGBA")
        im = im.crop(im.getbbox())
        im = im.resize((900, round(im.height * 900 / im.width)), Image.LANCZOS)
        im.save(BRAND / out, optimize=True)


# ---------------------------------------------------------------- share cards
OG = {
    "home": ("arielle-seated", "Clear, confident,", "and in control again."),
    "about": ("arielle-portrait", "Welcome, I am", "Arielle Innou Nahmias."),
    "life": ("new-chapter", "It’s not too late", "to feel like you again."),
    "corporate": ("leaders", "Empowered teams.", "A workplace that works."),
    "retreats": ("sisterhood", "The Sanctuary", "Navigator."),
    "contact": ("arielle-garden", "Let’s start your", "next chapter."),
}


def cover(im, w, h, fx, fy):
    s = max(w / im.width, h / im.height)
    im = im.resize((math.ceil(im.width * s), math.ceil(im.height * s)), Image.LANCZOS)
    x = min(max(0, im.width * fx / 100 - w / 2), im.width - w)
    y = min(max(0, im.height * fy / 100 - h / 2), im.height - h)
    return im.crop((int(x), int(y), int(x) + w, int(y) + h))


def og_cards(meta, fonts):
    serif = fonts / "Fraunces.ttf"
    italic = fonts / "FrauncesItalic.ttf"
    sans = fonts / "Manrope.ttf"
    for key, (photo, l1, l2) in OG.items():
        card = Image.new("RGB", (1200, 630), PLUM)
        m = meta[photo]
        src = Image.open(IMG / f"{photo}-1600.webp").convert("RGB")
        pic = cover(src, 520, 630, m["fx"], m["fy"])
        mask = Image.new("L", (520, 630), 0)
        ImageDraw.Draw(mask).rounded_rectangle((0, 40, 480, 630 + 300), radius=240, fill=255)
        card.paste(pic, (680, 0), mask.filter(ImageFilter.GaussianBlur(0.6)))
        d = ImageDraw.Draw(card)
        draw_lotus(d, 102, 104, 92, LILAC, PLUM)
        f_label = ImageFont.truetype(str(sans), 22)
        try:
            f_label.set_variation_by_axes([600])
        except Exception:
            pass
        d.text((72, 168), "ARIELLE INNOU COACHING", font=f_label, fill=MINT, spacing=4)
        f1 = ImageFont.truetype(str(serif), 66)
        f2 = ImageFont.truetype(str(italic), 66)
        d.text((72, 300), l1, font=f1, fill=IVORY)
        d.text((72, 382), l2, font=f2, fill=LILAC)
        d.text((72, 540), "Life, relationship & corporate coaching · Toronto", font=ImageFont.truetype(str(sans), 24), fill=(214, 204, 224))
        card.save(IMG / "og" / f"{key}.jpg", quality=86, optimize=True)
        print(f"  og/{key}.jpg")


if __name__ == "__main__":
    if len(sys.argv) < 3:
        sys.exit(__doc__)
    src, fonts = Path(sys.argv[1]), Path(sys.argv[2])
    IMG.mkdir(parents=True, exist_ok=True)
    (IMG / "og").mkdir(exist_ok=True)
    BRAND.mkdir(parents=True, exist_ok=True)
    meta = process_photos(src)
    brand_files(src)
    og_cards(meta, fonts)
