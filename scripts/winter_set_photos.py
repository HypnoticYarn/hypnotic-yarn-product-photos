"""Winter set listing photos (Nov 2026).
Builds each set photo from the processed Color Bar photos in color-bar/ (only resized and placed on white,
nothing edited), names under each skein in DM Sans, layout approved by Cheryl Nov 8, 2026:
five skeins = three over two, Sock Set = main skein over two minis, Color Quartet = two over two.
Square 2160 x 2160 JPEG on pure white."""
import json, os, re, sys
from PIL import Image, ImageChops, ImageDraw, ImageFont
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CB = os.path.join(ROOT, 'color-bar')
OUT = os.path.join(ROOT, 'winter-sets')
FONT = os.path.expanduser('~/.fonts/DMSans[opsz,wght].ttf')
INK = (61, 47, 42)
S = 2160

def slug(c):
    return {'Undead & Fabulous': 'undead-fabulous'}.get(c, re.sub(r'[^a-z0-9]+', '-', c.lower()).strip('-'))

def font(sz, wght=450):
    f = ImageFont.truetype(FONT, sz)
    try: f.set_variation_by_axes([14, wght])
    except Exception: pass
    return f

def load(color, base, shot):
    im = Image.open(f'{CB}/{slug(color)}/{slug(color)}-{base}-{shot}.png').convert('RGB')
    # lift the faint near-white halo to pure white so no crop edges show (shadow core untouched)
    L = im.convert('L')
    t = L.point(lambda v: 0 if v < 238 else (255 if v >= 251 else int((v - 238) / 13 * 255)))
    im = Image.composite(Image.new('RGB', im.size, (255, 255, 255)), im, t)
    g = im.convert('L').point(lambda v: 255 if v < 248 else 0)
    l, _, r, _ = g.getbbox()
    pad = 14
    return im.crop((max(0, l - pad), 90, min(1080, r + pad), 1022))  # shared top/bottom: one scale for every skein

def compose(items, rows, out):
    """items: [(label, Image)], rows: e.g. [3, 2]"""
    canvas = Image.new('RGB', (S, S), (255, 255, 255))
    fz = int(S * 0.022); F = font(fz)
    label_h = int(fz * 1.9); gap = int(S * 0.012); rgap = int(S * 0.02); margin = int(S * 0.045)
    groups, i = [], 0
    for n in rows: groups.append(items[i:i + n]); i += n
    H0 = items[0][1].height
    aw = S - 2 * margin; ah = S - 2 * margin - (len(groups) - 1) * rgap
    s = min(min((aw - gap * (len(g) - 1)) / sum(im.width for _, im in g) for g in groups), (ah / len(groups) - label_h) / H0)
    row_h = int(H0 * s) + label_h
    y = (S - (row_h * len(groups) + (len(groups) - 1) * rgap)) // 2
    dr = ImageDraw.Draw(canvas)
    for g in groups:
        ws = [int(im.width * s) for _, im in g]
        x = (S - (sum(ws) + gap * (len(g) - 1))) // 2
        for (lab, im), w in zip(g, ws):
            im2 = im.resize((w, int(H0 * s)), Image.LANCZOS)
            reg = canvas.crop((x, y, x + w, y + im2.height))
            canvas.paste(ImageChops.multiply(reg, im2), (x, y))
            tw = dr.textlength(lab, font=F)
            dr.text((x + (w - tw) / 2, y + im2.height + int(fz * 0.35)), lab, font=F, fill=INK)
            x += w + gap
        y += row_h + rgap
    canvas.save(out, quality=90, optimize=True, subsampling=0)

if __name__ == '__main__':
    spec = json.load(open(sys.argv[1]))   # [{"file":..., "items":[[label,color,shot],...], "rows":[3,2], "base":"fingering"}]
    for job in spec:
        items = [(lab, load(col, job['base'], shot)) for lab, col, shot in job['items']]
        os.makedirs(os.path.dirname(os.path.join(OUT, job['file'])), exist_ok=True)
        compose(items, job['rows'], os.path.join(OUT, job['file']))
        print(job['file'])
