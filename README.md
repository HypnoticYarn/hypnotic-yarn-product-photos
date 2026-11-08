# Hypnotic Yarn product photos

Processed Color Bar product photos used on hypnoticyarn.com.

- `color-bar/<color>/<color>-<fingering|dk>-<n>-<shot>.png`
- Photo order on every listing: 1 100g standing, 2 50g standing, 3 20g standing, 4 100g lying, 5 close-up
- 1080 x 1080 on white. Standing skeins fill 80% of the height, lying skeins 84% of the width, one light even shadow.
- Only resizing, approved color corrections and a plain shadow. Nothing redrawn or generated.

## Original Brushed Merino photos

- `originals/brushed-merino/<color>/` holds the original Brushed Merino Lace Weight photos for 47 colors, exactly as first shot: one close-up (`<color>-brushed-merino-closeup.png`) and the skein photos (`<color>-brushed-merino-skein-<n>.png`).
- These are not color-corrected or reframed yet. They are the starting files for the Brushed Merino correction pass; nothing in `originals/` is used on the site.
- Toffee has three close-ups. Private Label and Shortbread already have corrected photos in `brushed-merino/`.

## Winter set photos

- `winter-sets/<palette>/<palette>-<fingering|dk>-<mini|50g|100g>-set.jpg` (Winter palette sets) and `winter-sets/<name>-winter-<sock-set|color-quartet>-<fingering|dk>.jpg`
- Made by `scripts/winter_set_photos.py` from the Color Bar photos above: only resized and placed on white, each color's name under its skein. 2160 x 2160 JPEG.
- Layout (Cheryl, Nov 8, 2026): five-skein sets three over two, Sock Sets the main skein over its two minis, Color Quartets two over two.
- Swatch photos (Cheryl, Nov 8, 2026): `winter-sets/<palette>/<palette>-<weight>-swatches.jpg` and `winter-sets/<name>-winter-<sock-set|color-quartet>-<weight>-swatches.jpg`. Each color's own close-up photo in a circle, same layouts and names. Listing photo order matches the Color Bar listings: 100g set, 50g set, Mini set, then the swatch photo last (Sock Sets and Color Quartets: set photo, then swatch).
- `winter-sets/sources/` holds set-photo-only stand-ins for a Color Bar photo (the script uses them in place of the `color-bar/` file). Now: `shortbread-dk-3-20g.png`, the Shortbread DK minis with the gray cut-out outline and old shadow removed by `scripts/clean_outline.py` (background only, yarn untouched, plain light shadow added). The Color Bar listing photo itself is unchanged.
