"""Remove a grey/greenish cut-out outline and old grey shadow around yarn (background only, yarn untouched),
then add the plain light shadow used on the other Color Bar photos. usage: clean_outline.py src out"""
import sys, numpy as np
from PIL import Image, ImageFilter
src, out = sys.argv[1:3]
x = np.asarray(Image.open(src).convert('RGB')).astype(float)
mx, mn = x.max(2), x.min(2)
chroma = mx - mn
bg = ((chroma <= 5) & (mn >= 190)) | ((x[..., 1] >= x[..., 0]) & (x[..., 1] >= x[..., 2]) & (mn >= 228))
bgi = Image.fromarray((bg * 255).astype(np.uint8)).filter(ImageFilter.MaxFilter(3)).filter(ImageFilter.MinFilter(3))
bg = np.asarray(bgi) > 127
yarn = ~bg
# keep only big connected yarn regions (drop specks)
alpha = Image.fromarray((yarn * 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(0.8))
a = np.asarray(alpha).astype(float) / 255
S = x.shape[0]
sh = Image.fromarray((yarn * 255).astype(np.uint8))
sh = sh.transform(sh.size, Image.AFFINE, (1, 0, -10, 0, 1, -12)).filter(ImageFilter.GaussianBlur(14))
s = np.asarray(sh).astype(float) / 255 * 0.16
base = 255 * (1 - s[..., None]) + np.array([150, 145, 142]) * s[..., None]
o = x * a[..., None] + base * (1 - a[..., None])
Image.fromarray(np.clip(o, 0, 255).astype(np.uint8)).save(out)
