# -*- coding: utf-8 -*-
"""Logo: przytnij, usuń białe tło, rozdziel sygnet (góra) od napisu (dół)."""
from PIL import Image, ImageChops

im = Image.open('logo_kabichemie.jpg').convert('RGB')
bg = Image.new('RGB', im.size, (255, 255, 255))
im = im.crop(ImageChops.difference(im, bg).getbbox()).convert('RGBA')

# białe tło -> przezroczyste
px = list(im.getdata())
out = []
for r, g, b, a in px:
    m = min(r, g, b)
    if r > 244 and g > 244 and b > 244:
        out.append((r, g, b, 0))
    elif m > 228:
        out.append((r, g, b, int((255 - m) * 11)))
    else:
        out.append((r, g, b, 255))
im.putdata(out)
W, H = im.size
im.save('src/assets/logo.png')

# zawartość w wierszach (z kanału alfa) -> znajdź przerwę między sygnetem a napisem
alpha = list(im.split()[3].getdata())
rowfill = [sum(1 for x in alpha[y * W:(y + 1) * W] if x > 40) for y in range(H)]
band = range(int(H * 0.50), int(H * 0.72))
split = min(band, key=lambda y: rowfill[y])
print('rozmiar:', (W, H), 'linia podziału y =', split)

def crop_trim(box, name):
    part = im.crop(box)
    bb = part.getbbox()
    part = part.crop(bb)
    part.save('src/assets/' + name)
    print(' ', name, part.size)

crop_trim((0, 0, W, split), 'logo-mark.png')          # sygnet (spirala)
crop_trim((0, split, W, H), 'logo-word.png')          # napis KABICHEMIE + WATER TREATMENT
